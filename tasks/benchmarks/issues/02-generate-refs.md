# 02 i2i 用の参照画像 3 枚を生成して固定する

Type: prototype
Status: resolved

## 目的

`benchmarks/refs/README.md` の仕様 3 件（ref-01 人物A・ref-02 コート・ref-03 人物B）を基準モデルで生成し、`benchmarks/refs/<id>.png`（長辺 1024px）として固定する。

## 手順（ユーザー）

1. 仕様のプロンプトを GPT-Image 2.5 に渡し、各 4 枚ほど生成する
2. 仕様に最も合う 1 枚を選ぶ。ref-01 は全身が切れておらず正面・腕が体側にあること、ref-02 は正面のコート単体、ref-03 は座位で片手を上げていること
3. PNG で保存し、`refs/README.md` の「未生成」を消す

## 受け入れ条件

- Given 3 枚の PNG、When `benchmarks/refs/` に置く、Then i2i の問題用紙 6 件がすべて参照先を持つ

## Comments

- 2026-09-24: `run_gptimg.py --refs 4` を追加し、ユーザー承認のうえ 3 仕様 × 4 枚 = 12 枚を 768x1024（3:4・長辺 1024）で生成。model は t2i と同じ `gpt-image-2.5-sunburst-2026-09-08`、quality high。拒否なし、実費 ≈ $0.43（1,204 output tokens / 枚）。候補は `_local/gpt-image-2-5/refs/ref-NN-cand_0000K.png`、一覧は同フォルダの `contact-sheet.png`。ユーザーの選定待ち
- 2026-09-24: ユーザーが各 cand_00004 を選定（理由は `refs/README.md` の生成記録に記載）。`benchmarks/refs/ref-01〜03.png`（768x1024）として固定し、README の「未生成」を消した。i2i の問題用紙 6 件の参照先が揃った

