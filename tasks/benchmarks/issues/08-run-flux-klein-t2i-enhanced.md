# 08 flux-2-klein-9b で t2i の raw と enhanced を流して判定する

Type: prototype
Status: resolved

## 目的

`benchmarks/results/flux-2-klein-9b/t2i.md` を埋める。raw 25 枚とスキルで書いた enhanced 26 枚を生成し、対で 5軸を判定して考察を書く。

## 手順（ユーザー）

1. ComfyUI を起動し、API JSON（`benchmarks/_local/image_flux2_text_to_image_9b.json`）が現在のワークフローと一致していることを確認する
2. 設定は 8 steps / cfg 1 / euler に決定済み（問題用紙 02 で 4 / 8 / 20 steps を比較し、4 は破綻が多く 8 が安定）。API JSON は `_local/image_flux2_text_to_image_9b.json` に反映済み。判定シート冒頭にこの設定を書く。ComfyUI 側のワークフローも同じ値に揃えておく
3. `python benchmarks/scripts/run_t2i.py --model flux-2-klein-9b --api-json benchmarks/_local/image_flux2_text_to_image_9b.json`（raw / enhanced 各 26 枚。enhanced だけなら `--variants enhanced`）
4. `_local/flux-2-klein-9b/t2i/run.json` の設定を判定シート冒頭に写す
5. 「見るもの」を参照して 5軸を 0 / 1 / 2 で判定し、集計表と備考に記入する
6. 末尾の考察に、得意・不得意、enhance の要否、qwen-image-2-1・krea-2-turbo および基準モデルとの差を書く

## 受け入れ条件

- Given 23 件 × raw / enhanced、When 判定する、Then 集計表の 46 行が埋まり、考察が書かれている
- Given 判定結果、When enhanced が raw より劣る問題用紙がある、Then その ID をスキル改善の候補として Comments に列挙する

## Comments
- 2026-09-24: t2i-23 の enhanced プロンプトをスキルで作成して判定シートに追記し、ユーザーが ComfyUI で 23 番の raw / enhanced を生成。`_local/flux-2-klein-9b/t2i/` に raw 26・enhanced 26 の計 52 枚が揃った。残りは判定（集計表 46 行・考察）
- 申し送り（2026-09-24、判定は新規セッションで実施）: 判定の進め方・転記の手順・注意点はチケット 09 の Comments「申し送り」にまとめた。Qwen の判定（チケット 03）と同じ「作業用紙 → 転記」方式で行う
- 2026-09-24 判定完了: 07 と同じ手順（見比べ画像 → 作業用紙 → `scripts/transcribe_eval.py` で `results/flux-2-klein-9b/t2i.md` へ転記）。enhanced 行の最良は「enhanced でも基準モデルに追いつくか」で付け直し（12・17・19・22 のみ 1）。考察は判定者のメモを土台に備考から肉付けした
- スキル改善候補: t2i-16 2D anime illustration（忠実。橋の上に立っていない）。点は落ちないが enhanced で質感が悪化: t2i-01（明るすぎ）・t2i-04（色調補正過多）・t2i-09（プラスチック感）・t2i-15（3D 質感）。判定者の所見は「レンズ・f 値などカメラ設定語に過剰反応する」で、スキルのカメラ指定の扱いが改善点

