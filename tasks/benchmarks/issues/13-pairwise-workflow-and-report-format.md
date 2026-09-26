# 13 一対比較の手順と判定シートの後継書式を定め、感想戦からレポートを作る流れを README に書く

Type: task
Story: pairwise
Status: resolved
Blocked by: 10, 12

## 目的

「LLM がビルドを実行 → 判定者がブラウザで 2 択 → JSON → LLM がスクリプトで集計 → チャットで雑感をヒアリング → レポート完成」の流れを `benchmarks/README.md` の手順にし、判定シート `results/<model-slug>/t2i.md` の書式を 5 軸から一対比較の後継書式に置き換える。5 軸のシートは今後書かない（今回の結果は git が担う）。

## 手順

1. `benchmarks/README.md` を書き換える
   - 「手順」の 5〜6 を一対比較に置き換える: build（チケット 11）→ 判定 → JSON を `_local/pairwise/` に保存 → `pairwise_report.py`（チケット 12）→ 感想戦 → レポート
   - 「尺度」「ルーブリック（t2i・5軸）」の節を外し、「観点セット」（チケット 10）と「集計の読み方」（勝率・n・引き分け）を置く。i2i の 5 軸はチケット 15 まで残す
   - 「構成」に `_local/pairwise/` と `scripts/pairwise_*.py` を足す。`make_compare.py` / `transcribe_eval.py` と作業用紙は一対比較に置き換わるので構成から外し `.trash/` へ
2. 判定シートの後継書式を決め、`results/<model-slug>/t2i.md` のテンプレートとして書く
   - 冒頭: 基準モデル・判定日・判定者・ワークフロー設定・使ったセッション（ID とモード）
   - 観点別プロファイル（`pairwise_report.py` の表を貼る）
   - enhance の効き（上げた観点・下げた観点）
   - 感想戦: 判定者の雑感（JSON の notes とチャットでのヒアリング）と、それを Claude が観点・問題用紙 ID に結び付けて整理したもの。ここが利用者向けの成果物
   - スキル改善候補: enhance が下げた観点と問題用紙 ID
   - enhanced プロンプトの一覧は残す（生成の再現に要る）
3. 感想戦の進め方を README に書く: Claude は集計を提示してから、観点ごとに「勝った / 負けた理由」「意外だった点」「用途としてどうか」を 1 往復ずつ聞く。1 問ずつのウィザードにしない（`tasks/lessons.md` w3qn）。ヒアリングは AskUserQuestion か通常のチャットで、判定者の言葉をそのまま感想戦の節に写す
4. `results/README.md`（横断比較）の書式も「観点 × モデル」の表に改め、セルは勝率ベースの一言にする。実際の書き換えはチケット 14 の結果で行う
5. `docs/README.md` の「判定シート」の更新ルールと `CONTEXT.md` の「判定シート」の定義を後継書式に合わせる

## 受け入れ条件

- Given `benchmarks/README.md`、When 手順を読む、Then build → 判定 → 集計 → 感想戦 → レポートが順に書かれ、5 軸の t2i ルーブリックがない
- Given 判定シートのテンプレート、When 新しいモデルを判定する、Then 観点別プロファイル・enhance の効き・感想戦・スキル改善候補・enhanced プロンプトの節が揃う
- Given 旧ツール（compare / eval-sheet / transcribe）、When 構成を見る、Then README から消え、スクリプトは `.trash/` にある

## Comments

## Answer

- `benchmarks/README.md` を書き換えた: 手順 5〜9 を build → 判定 → 集計 → 感想戦 → 判定シートに置き換え、「一対比較（t2i）」の節（モード・画面と操作・集計の読み方・観点セット）を置き、5 軸は i2i だけに残した。構成から compare / eval-sheet / transcribe を外し、`_local/pairwise/` と `pairwise_*.py` を足した
- 判定シートの後継書式は `benchmarks/results/TEMPLATE-t2i.md`。Enhanced prompts の節は `run_t2i.py` の `load_enhanced` が読む形（`### <id>` + text ブロック）を維持する
- 横断比較 `results/README.md` は観点 × モデルの表に改め、krea と flux を ab セッションから埋めた（flux は反転）。qwen は未実施と明記
- `docs/README.md` の判定シートの更新ルールと `CONTEXT.md` の判定シート・基準モデルの定義を後継書式に合わせた
- 旧ツール（make_compare.py / transcribe_eval.py）と作業用紙・見比べ画像は `.trash/pairwise-superseded-20260924/` へ
