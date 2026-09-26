# 12 セッション JSON を集計する `scripts/pairwise_report.py` を作る

Type: task
Story: pairwise
Status: resolved
Blocked by: 11

## 目的

判定者がダウンロードしたセッション JSON（1 つ以上）を読み、観点別・問題用紙別の集計を Markdown で出す。ライブラリ非依存。LLM はこの出力を土台に感想戦（チケット 13）を行う。

## 仕様

```
python benchmarks/scripts/pairwise_report.py benchmarks/_local/pairwise/*.json [--model krea-2-turbo] [--out -]
```

- 入力: 複数の JSON。同じモデルが登場するセッションをまとめて、そのモデルの「強みのプロファイル」を出す
- 出力（Markdown、stdout か `--out`）:
  - セッション一覧（モード・対戦相手・件数・日付）
  - 観点別プロファイル表: 行 = 観点、列 = 対戦相手（vs B / raw vs enhanced / vs 基準）。セルは「A の勝率（勝 / 分 / 負、n）」。n が 3 未満のセルは印を付ける
  - raw vs enhanced の効き: enhance が上げた観点と下げた観点（勝率 0.5 からの差の順）
  - 問題用紙別の一覧: 問題用紙 × 観点で A が勝った / 負けた / 引き分けを記号で並べ、負けが集中した問題用紙を末尾に列挙する
  - 雑感（JSON の notes）をそのまま転記
- 集計は勝率のみ（引き分け 0.5 勝）。Elo / Bradley-Terry は使わない（順位付けが目的ではないため）
- 同じ問題用紙・観点・対戦の組が複数セッションにあれば合算する

## 受け入れ条件

- Given 11 で作った JSON を 2 つ以上、When 実行する、Then 観点別プロファイル表・enhance の効き・問題用紙別一覧・雑感が 1 つの Markdown に出る
- Given 件数が少ないセル、When 表を見る、Then n が明記され、3 未満に印がある
- Given Windows の cp932 コンソール、When `PYTHONIOENCODING=utf-8` なしで実行する、Then 落ちずにファイル出力できる（`--out` を使う）

## Comments

## Answer

- `scripts/pairwise_report.py`。観点の並びと日本語名は `pairwise_build.aspect_table()`（README の観点セット表）から取る
- モデルが B 側のセッションは勝敗を反転して「そのモデルの勝率」に揃える。raw-enh は A = enhanced なので反転しない
- 問題用紙別の記号は o / = / x（ASCII。stdout が cp932 でも読める）。負けが集中した問題用紙は「負け 2 以上かつ負け > 勝ち」で列挙
- 検証: node のスタブで作った 3 セッション（ab / raw-enh / vs-baseline、各 85 問）を合算し、4 節が 1 つの Markdown に出ること、`--model` で B 側を指定すると勝率が 1 - x になること、`PYTHONIOENCODING=cp932` の stdout で落ちないことを確認
