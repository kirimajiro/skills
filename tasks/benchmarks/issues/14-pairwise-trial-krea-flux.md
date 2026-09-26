# 14 一対比較を krea-2-turbo と flux-2-klein-9b で回し、感想戦からレポートを作る

Type: prototype
Story: pairwise
Status: resolved
Blocked by: 13

## 目的

ツール一式（10〜13）を実際の判定で使い、判定シートを後継書式で書き直す。ツールの使いにくさ・観点の過不足・集計の読みにくさを見つけて 11〜13 に戻す。

## 手順（ユーザー）

画像はすべて `_local/` に生成済み。ComfyUI と API は不要。

1. Claude が build する（3 セッション。1 セッション約 23 問 × 2〜4 設問）
   - `--mode ab --a krea-2-turbo --b flux-2-klein-9b`（enhanced 同士、基準は hide）
   - `--mode raw-enh --a krea-2-turbo`
   - `--mode vs-baseline --a krea-2-turbo`
2. ブラウザで各 HTML を開いて答え、終了画面で雑感を入れ、JSON を `benchmarks/_local/pairwise/` に保存する
3. 「終わった」と Claude に伝える。Claude が `pairwise_report.py` で集計し、感想戦（観点ごとに 1 往復）を行い、`results/krea-2-turbo/t2i.md` を後継書式で書き直す
4. 余力があれば `--mode raw-enh --a flux-2-klein-9b` と `--mode vs-baseline --a flux-2-klein-9b` も回し、`results/flux-2-klein-9b/t2i.md` も書き直す

## 見るもの（ツールの改善点）

- 1 セッションの所要時間と、途中で止めたくなった箇所
- 設問が「見るもの」に対して足りない・重複する・言い回しが判断しにくい観点
- 引き分けが多い観点（設問が効いていない）
- 終了画面の集計だけで自分の印象と一致するか。雑感欄に何を書きたくなったか

## 受け入れ条件

- Given 3 セッションの JSON、When 集計と感想戦を行う、Then `results/krea-2-turbo/t2i.md` が後継書式で埋まり、`results/README.md` の横断表が観点 × モデルに書き換わる
- Given 使ってみた所感、When Comments に書く、Then 11〜13 への改善点が問題用紙 ID・観点 ID 付きで列挙され、必要ならチケットを起こしている
- Given enhance が下げた観点、When スキル改善候補を書く、Then 問題用紙 ID と観点 ID が Comments にある

## Comments

- 2026-09-24 Claude: 3 セッションをビルド済み。ブラウザで `file://` で開き、終了画面の JSON を同じフォルダに保存する
  - `benchmarks/_local/pairwise/ab_krea-2-turbo_flux-2-klein-9b_20260924-1600.html`
  - `benchmarks/_local/pairwise/raw-enh_krea-2-turbo_20260924-1600.html`
  - `benchmarks/_local/pairwise/vs-baseline_krea-2-turbo_gpt-image-2-5_20260924-1600.html`
  - 集計: `python benchmarks/scripts/pairwise_report.py benchmarks/_local/pairwise/*.json --out <file>`
- 2026-09-24 ユーザー: 3 セッション完了。「とても良いツールになっていました」。所要は ab 約 20 分（引き分け 34/85）、raw-enh 約 18 分（54/85）、vs-baseline 約 4 分（14/85）
- 2026-09-24 Claude: 集計と感想戦を経て `results/krea-2-turbo/t2i.md` を後継書式で書き直し、`results/README.md` を観点 × モデルに書き換えた
- ツールの改善点（ユーザー所感）: 「特になし。このまま使える」「プロンプトは常に表示」「画像の上の左右のテキストは不要」「設問を左右中央にした方が目線移動が少ないかも」→ いずれもテンプレートに反映済み
- 集計の改善（Claude）: 「負けが集中した問題用紙」は対戦ごとに列挙するよう変更（vs 基準が全問に該当して読めなかった）
- 観点の過不足: 設問で迷った観点の報告なし。composition は vs flux で 8/8 引き分け（差が出ない観点）。organic・fidelity は n=2 で `*` 付き。次回の観点見直し時に organic の設問を 13 以外にも足すか検討
- スキル改善候補（enhance が下げた観点と問題用紙 ID）: texture: t2i-01, 02, 09, 16 photograph, 20 / light: 09, 10, 13, 23 / skin: 09 / layout: 21 / text: 23。→ `tasks/krea-2-turbo/issues/02-pairwise-driven-skill-review.md` を起票
- 2026-09-24 Claude: 手順 4 の flux 主体セッションをビルド済み（判定待ち）。判定後に `pairwise_report.py --model flux-2-klein-9b` で集計し、`results/flux-2-klein-9b/t2i.md` を後継書式に書き直す
  - `benchmarks/_local/pairwise/raw-enh_flux-2-klein-9b_20260924-1715.html`
- 2026-09-26 ユーザー: flux の vs-baseline を判定（引き分け 10/85、勝ち 0。雑感欄は空）。JSON は `_local/pairwise/` に配置。感想戦（vs 基準）: 「krea と同じで、情報量の少ない題材だけ差が小さい」「flux はアニメ・フラットでも基準に負ける（krea は引き分けた）」。raw-enh は続けて実施し、flux の判定シートはその後に書く
- 2026-09-26 ユーザー: flux の raw-enh を判定（引き分け 41/85、約 10 分）。雑感: 「flux-2-klein-9b は想像力が豊かで、より自然なスタイルや構図が出ることがあるが、指示文に無いので出したもの自体が破綻しているケースが多い（14 の窓の外の車、04 の傘の縮尺、11 のエンジン構造）」。判定中に雑感を思い出せない問題 → 終了画面に見返しギャラリーを追加し `--rebuild` で既存 HTML に再適用（11 へのフィードバック、反映済み）
- 2026-09-26 Claude: `results/flux-2-klein-9b/t2i.md` を後継書式で書き直し（旧 5 軸は `.trash/pairwise-superseded-20260924/flux-2-klein-9b-t2i-5axis.md`）、`results/README.md` に flux vs 基準の列と enhance の効きを追記。スキル改善候補（context: 02・03・04・05・17 / detail: 03・07・11 / skin: 02・09 / organic: 13 / anatomy: 16 anime・23）→ `tasks/flux-2-klein-9b/issues/03-pairwise-driven-skill-review.md`

