# 06 基準モデルで i2i の問題用紙を流す

Type: prototype
Status: resolved
Blocked by: 01, 02

## 目的

基本データでネイティブ i2i 対応が確認できた場合に、GPT-Image 2.5 で i2i 7 件を raw で生成し、`benchmarks/results/gpt-image-2-5/i2i.md` に判定を記録する。非対応なら resolved にして理由を Answer に書く。

## 受け入れ条件

- Given 対応の確認、When 7 件を生成する、Then 集計表の 7 行が埋まっている

## Comments

- 2026-09-24: 基本データでネイティブ i2i 対応を確認済み（チケット 01）。`run_gptimg.py --i2i` を追加し、ユーザー承認のうえ API 経路（images.edit、`gpt-image-2.5-sunburst-2026-09-08`、high、問題用紙の refs を `--ref` で渡す）で 7 件を raw 生成。拒否なし、実費 ≈ $0.32。`_local/gpt-image-2-5/i2i/`、判定シート冒頭に固定条件を記入。判定用の作業用紙は同フォルダの `eval-sheet.md`。Codex 経路は model が固定できない（flare 相当・size は希望のみ）ため不採用
- 2026-09-24: ユーザーが 7 件を判定（作業用紙 `_local/gpt-image-2-5/i2i/eval-sheet.md`）、`results/gpt-image-2-5/i2i.md` の集計 7 行と考察に転記。全軸 2。差が出るのは raw のポーズ転写（Qwen は 2 人合成、基準は成立）とアウトペイント（両者とも再構成）

