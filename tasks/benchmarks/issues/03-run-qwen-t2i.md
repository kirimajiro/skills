# 03 qwen-image-2-1 で t2i の問題用紙を流して判定する

Type: prototype
Status: resolved

## 目的

`benchmarks/results/qwen-image-2-1/t2i.md` を埋める。raw と enhanced の対で 23 件を生成し、5軸を判定し、考察を書く。

## 手順（ユーザー）

1. ComfyUI を起動し、API 形式の JSON（`benchmarks/_local/image_qwen_image_2_1_t2i.json`）が現在のワークフローと一致していることを確認する
2. 小さく試す: `python benchmarks/scripts/run_t2i.py --model qwen-image-2-1 --api-json benchmarks/_local/image_qwen_image_2_1_t2i.json --only 01`。`_local/qwen-image-2-1/t2i/01-short-rainy-alley-raw_00001.png` と `01-short-rainy-alley-enhanced_00001.png` ができることを確認する（ComfyUI の output 側は `Bench/qwen-image-2-1/t2i/` に同名＋末尾 `_` で並ぶ）
3. 本番: `--only` を外して実行する（raw / enhanced 各 26 枚。中断しても再実行で続きから回る）。「多様」軸を見る問題用紙だけ `--only 01,02,07,08 --seeds 4` で追加する
4. `_local/qwen-image-2-1/t2i/run.json` の設定を判定シート冒頭に写す
5. 「見るもの」を参照して 5軸を 0 / 1 / 2 で判定し、集計表と備考に記入する
6. 末尾の考察に、得意・不得意、enhance の要否、基準モデルとの差を書く

## 受け入れ条件

- Given 23 件 × raw / enhanced、When 判定する、Then 集計表の 46 行がすべて埋まり、考察が書かれている
- Given 判定結果、When enhanced が raw より劣る問題用紙がある、Then その問題用紙 ID をスキル改善の候補として Comments に列挙する

## Comments

- 2026-09-24: t2i-23 の enhanced プロンプトをスキルで作成して判定シートに追記し、ユーザーが ComfyUI で 23 番の raw / enhanced を生成（全 52 枚が揃った）。seed 1〜4 の追加は見送り（多様は空欄）。ユーザーが `_local/qwen-image-2-1/t2i/eval-sheet.md`（作業用紙）に 1 枚 run で 5 軸を記入し、`results/qwen-image-2-1/t2i.md` の集計表 46 行・各備考・考察に転記した
- スキル改善候補（enhanced が raw より点を落とした ID、軸の比較）: t2i-10（最良）、t2i-11（忠実・補完）、t2i-16 oil painting（最良・品質）、t2i-21（最良）、t2i-23（最良）。判定者の所感では enhanced が明確に劣った印象はなく、無機物・パース・ポスターの弱さはモデル側の限界で enhance では埋まらない、という見立て

