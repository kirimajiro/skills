# 05 qwen-image-2-1 で i2i の問題用紙を流して判定する

Type: prototype
Status: resolved
Blocked by: 02

## 目的

`benchmarks/results/qwen-image-2-1/i2i.md` を埋める。参照画像を固定した後、raw と enhanced の対で 7 件を生成し、5軸（実行 / 保持 / 転写 / 整合 / 品質）を判定する。

## 受け入れ条件

- Given 7 件 × raw / enhanced、When 判定する、Then 集計表の 14 行が埋まり、考察が書かれている

## Comments

- 2026-09-24: `run_i2i.py` を作成（参照画像のアップロード、1 枚参照時の image_2 除去、follow ref-01 は入力サイズ・他は SIZES）。ワークフローは `_local/image_qwen_image_2_1_image_edit.json`。6 件 × raw / enhanced を生成後、ユーザーの指摘で (1) 難しいポーズ転写 i2i-07（ref-04 ダンサーのポーズ、cand 3）を追加、(2) i2i-04 は raw / enhanced とも 2 人を並べる合成になったため enhanced をポーズの言語化＋「人物は 1 人だけ」の肯定形に書き直し、(3) i2i-05 は無地背景では延長が無意味なため情景の参照 ref-05（カフェ前、cand 4）に差し替え。差し替え前の画像は `.trash/i2i-superseded-20260924/`
- 2026-09-24: 7 件 × raw / enhanced をユーザーが判定（作業用紙 `_local/qwen-image-2-1/i2i/eval-sheet.md`）、`results/qwen-image-2-1/i2i.md` の集計 14 行・備考・考察に転記。スキル改善候補: i2i-06（enhanced が保持・整合・品質で raw を下回る。顔の傾き等の装飾的な記述が原因の可能性）。i2i-04 raw は 2 人合成のため判定者が 0 に修正（品質は空欄）

