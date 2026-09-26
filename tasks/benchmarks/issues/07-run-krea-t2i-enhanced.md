# 07 krea-2-turbo で t2i の enhanced を流して判定する

Type: prototype
Status: resolved

## 目的

`benchmarks/results/krea-2-turbo/t2i.md` の enhanced 行を埋める。raw は既に流せる状態なので、スキルで書いた enhanced 26 枚を追加し、raw と対で 5軸を判定して考察を書く。

## 手順（ユーザー）

1. ComfyUI を起動し、API JSON（`benchmarks/_local/image_krea2_turbo_t2i.json`）が現在のワークフローと一致していることを確認する
2. `python benchmarks/scripts/run_t2i.py --model krea-2-turbo --api-json benchmarks/_local/image_krea2_turbo_t2i.json --variants enhanced`（26 枚。raw 未実施なら `--variants raw,enhanced`）
3. `_local/krea-2-turbo/t2i/run.json` の設定（8 steps / cfg 1 は CFG 無効と同義）を判定シート冒頭に写す
4. 「見るもの」を参照して 5軸を 0 / 1 / 2 で判定し、集計表と備考に記入する
5. 末尾の考察に、得意・不得意、enhance の要否、qwen-image-2-1 および基準モデルとの差を書く

## 受け入れ条件

- Given 23 件 × raw / enhanced、When 判定する、Then 集計表の 46 行が埋まり、考察が書かれている
- Given 判定結果、When enhanced が raw より劣る問題用紙がある、Then その ID をスキル改善の候補として Comments に列挙する

## Comments
- 2026-09-24: t2i-23 の enhanced プロンプトをスキルで作成して判定シートに追記し、ユーザーが ComfyUI で 23 番の raw / enhanced を生成。`_local/krea-2-turbo/t2i/` に raw 26・enhanced 26 の計 52 枚が揃った。残りは判定（集計表 46 行・考察）
- 申し送り（2026-09-24、判定は新規セッションで実施）: 判定の進め方・転記の手順・注意点はチケット 09 の Comments「申し送り」にまとめた。Qwen の判定（チケット 03）と同じ「作業用紙 → 転記」方式で行う
- 2026-09-24 判定完了: `scripts/make_compare.py` で見比べ画像 26 枚、`_local/krea-2-turbo/t2i/eval-sheet.md` に判定者が 5 軸を記入し、`scripts/transcribe_eval.py` で `results/krea-2-turbo/t2i.md` へ転記（集計 46 行・備考・冒頭の設定・考察）。enhanced 行の最良は判定者の指示で「enhanced でも基準モデルに追いつくか」に付け直し（既定 0、AskUserQuestion で 26 行を個別確認。12・22 のみ 1）。考察メモは空欄だったため備考から Claude が起こし、判定者の確認待ち
- スキル改善候補（enhanced が raw より劣った ID。忠実・補完・品質の比較）: t2i-20（補完・品質。麺がスープから浮き出る）。点は落ちないが enhanced で「膝上」の指定が顔の見切れを生む t2i-04 も候補

