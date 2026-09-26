# <model-slug> — t2i 判定シート

- 基準モデル: GPT-Image 2.5
- 判定日: YYYY-MM-DD
- 判定者: リポジトリ所有者
- ワークフロー設定（steps / guidance / sampler / 解像度）: `_local/<model-slug>/t2i/run.json` から写す。seed 1
- セッション（`_local/pairwise/`、git 管理外）:
  - `ab_<a>_<b>_<日時>` — vs <b>（enhanced 同士）
  - `raw-enh_<a>_<日時>` — enhanced vs raw
  - `vs-baseline_<a>_<基準>_<日時>` — vs 基準モデル raw

## 観点別プロファイル

`pairwise_report.py` の表を貼る。セルはこのモデルの勝率（勝 / 分 / 負、n）。引き分けは 0.5 勝、`*` は n が 3 未満。

| aspect | vs <b> | raw vs enhanced | vs baseline |
|---|---|---|---|

## enhance の効き

`pairwise_report.py` の Enhance effect を写す。

- 上げた観点:
- 下げた観点:
- 変わらない観点:

## 感想戦

判定者の言葉はそのまま写し、Claude の整理は観点 ID と問題用紙 ID に結び付ける。ここが利用者向けの成果物。

- 判定者の雑感（セッションの notes）:
  - vs <b>:
  - enhanced vs raw:
  - vs 基準:
- ヒアリング（観点のまとまりごとに 1 往復。判定者の言葉）:
  - 強い観点の理由:
  - 弱い観点の理由:
  - enhance について:
  - 用途について:
- Claude の整理:
  - 得意（対戦相手に対して勝率が高い観点と、それが出た問題用紙）:
  - 不得意:
  - enhance の効き（引き分けの多さ、上げた・下げた観点と問題用紙）:
  - 基準モデルとの差（引き分けが出た問題用紙から、差が小さい題材）:

## スキル改善候補

enhance が下げた観点と、enhanced が負けた問題用紙。チケットを起こしたらリンクする。

- <aspect>: t2i-NN, t2i-NN — 何が起きているか

## Enhanced prompts

`run_t2i.py` がここから enhanced プロンプトを読む。`### <id>` 見出しと ` ```text ` ブロックの形を変えない。画風の variant を持つ問題用紙は `Enhanced prompts（variant ごと）:` の下に `- <style>` と text ブロックを対で並べる。

### t2i-01 雨の夜の路地（短い指示での補完力）

問題用紙: `../../t2i/01-short-rainy-alley.md`

Enhanced prompt:

```text
...
```
