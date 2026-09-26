# 09 第1ラウンド判定: 3モデル × raw / enhanced（seed 1）を基準モデルと見比べて判定し、横断比較をまとめる

Type: task
Status: resolved
Blocked by: 04

## 前提（着手前に確認する）

- `benchmarks/_local/<model-slug>/t2i/` に次が揃っていること。なければ欠けているものを先に生成する（ComfyUI の 3 モデルは `benchmarks/README.md` の `run_t2i.py` の手順、基準モデルはチケット 04）
  - `qwen-image-2-1`: raw 26 枚・enhanced 26 枚（8 steps 相当の設定は `run.json` 参照）
  - `krea-2-turbo`: raw 26・enhanced 26（8 steps / CFG 無効）
  - `flux-2-klein-9b`: raw 26・enhanced 26（8 steps / cfg 1）
  - `gpt-image-2-5`: raw 26（基準モデル。enhanced はない）
- ルーブリックと尺度は `benchmarks/README.md`。問題用紙の「見るもの」は `benchmarks/t2i/<NN>-<slug>.md`
- 各モデルの enhanced プロンプトは `benchmarks/results/<model-slug>/t2i.md` の各節にある

## 目的

利用者が 3 モデルの得意不得意を掴めるように、問題用紙 23 件を 5 軸で判定し、モデルごとの考察と横断比較を書く。判定の正は人（ユーザー）で、Claude は一次判定と記録・集計を担う。

## 手順

1. **見比べの道具を作る**: `benchmarks/scripts/contact_sheet.py` を新規作成する。依存なし（標準ライブラリのみ）で、問題用紙ごとに 1 ページ、列 = モデル（gpt-image-2-5 / qwen-image-2-1 / krea-2-turbo / flux-2-klein-9b）、行 = raw / enhanced の格子で画像を相対パス参照し、問題用紙の汎用プロンプトと「見るもの」を添えた HTML を `benchmarks/_local/contact/index.html` に書く。git 管理外なので画像の相対パスは `../<model-slug>/t2i/...` になる
2. **Claude の一次判定**: 問題用紙ごとに Claude が該当画像（4 モデル分、最大 8 枚）を Read で見て、「見るもの」に照らし、モデル × variant ごとに 5 軸の案（0 / 1 / 2）と備考（根拠を一言）を出す。軸の扱い:
   - 忠実・補完: 画像と指示文を照らす
   - 最良: 同じモデルの raw と enhanced の差で判断（raw で十分なら 2、enhanced でないと崩れるなら raw を 0〜1）
   - 多様: seed 1 のみなので空欄。備考に「1 seed」と書く
   - 品質: 同じ問題用紙の gpt-image-2-5 の raw と見比べて相対で付ける
3. **ユーザーの確定**: 5 件ずつまとめて提示し、ユーザーが確認・修正する（AskUserQuestion を使ってよい。1 回に 1 件ずつ止めない）。確定したものだけ判定シートに書く
4. **記録**: 各 `results/<model-slug>/t2i.md` の集計表（raw / enhanced の行）と該当節の備考に書き込む。冒頭の判定日・判定者・ワークフロー設定（`_local/<model-slug>/t2i/run.json`）も埋める。基準モデルの判定シートは「品質」の基準そのものなので 5 軸は付けず、忠実・補完の所見だけ備考に書く
5. **考察**: 各判定シート末尾の「考察」に、得意・不得意（切り口ごと）、enhance と品質タグの要否（最良軸の傾向）、基準モデルとの差を書く
6. **横断比較**: `benchmarks/results/README.md` を新規作成し、「切り口 × モデル」の表（各セルはその切り口の問題用紙の enhanced 判定を要約した 0〜2 と一言）と、用途別にどのモデルを選ぶかの所見を書く。`docs/README.md` の索引と `benchmarks/README.md` の構成にこのファイルを追加する
7. **スキルへの還元**: 「enhanced が raw より劣る」「3 モデルとも同じ切り口で崩れる」「enhanced プロンプトが指示を落としている」を見つけたら、該当スキルの改善候補として本チケットの Comments に問題用紙 ID と症状を列挙する。スキルの修正は別チケットにする

## 受け入れ条件

- Given 4 モデルの画像、When 判定する、Then 3 モデル分の判定シートで集計表の全行（raw / enhanced × 26）の 忠実・補完・最良・品質 が埋まり、多様は空欄で備考に「1 seed」とある
- Given 判定結果、When 考察を書く、Then 3 モデルの判定シートに考察があり、`benchmarks/results/README.md` に切り口 × モデルの表と用途別の所見がある
- Given 判定中に見つかったスキル改善候補、When 記録する、Then Comments に問題用紙 ID 付きで列挙されている

## Comments

## 申し送り（2026-09-24。チケット 07・08・09 の判定を新規セッションで行うための引き継ぎ）

### 現状
- 4 モデルの t2i 画像はすべて `_local/<model-slug>/t2i/` に揃っている（qwen / krea / flux は raw 26・enhanced 26、gpt-image-2-5 は raw 26）。各フォルダの `run.json` に設定がある
- 判定済み: qwen-image-2-1 の t2i と i2i、gpt-image-2-5 の i2i（各 `results/<model-slug>/*.md`）。未判定: krea-2-turbo t2i（07）、flux-2-klein-9b t2i（08）、gpt-image-2-5 t2i の所見（09 の手順 4）
- ユーザーの希望は「モデル単位で全画像を一括判定」。チケット 09 の手順 2〜3（Claude の一次判定を 5 件ずつ確定）は、ユーザーが望めば行い、望まなければ作業用紙方式に置き換える。着手時に確認する

### 判定の進め方（qwen で実証済み。1 問ずつのウィザードはユーザーが不要と判断した）
1. 比較画像を作る: `uv run --with pillow python` で問題用紙ごとに「対象モデル raw / enhanced / GPT-Image 2.5 raw（基準）」を横並びにした PNG を `_local/<model-slug>/t2i/compare/<NN>-<slug>.png` に置く（t2i-16 は画風ごとに 4 枚）。qwen の compare が見本
2. 作業用紙を作る: `_local/<model-slug>/t2i/eval-sheet.md`。qwen の `_local/qwen-image-2-1/t2i/eval-sheet.md` を雛形にし、raw の日本語要約と「見るもの」はそのまま流用、「enhanced が足した要素」だけ対象モデルの enhanced プロンプト（`results/<model-slug>/t2i.md`）から書き直す。表は raw / enhanced × 忠実・補完・最良・品質・備考。多様の列は置かない（1 枚 run）。末尾に考察メモ欄（得意 / 不得意 / enhance の要否 / 基準との差 / enhanced が劣った ID）
3. ユーザーが記入し「終わった」と言ったら、スクリプトで転記する。転記先は `results/<model-slug>/t2i.md`: 集計表 46 行（多様は空欄、t2i-16 は「写真/アニメ/油彩/フラット」の順に 4 値をスラッシュ区切り、備考に順序を明記）、各問題用紙の「備考:」（raw / enhanced 別に転記）、画像パスを平置き命名に直す、冒頭の判定日・判定者（「リポジトリ所有者」）・ワークフロー設定（run.json から）、考察（ユーザーのメモを土台に肉付け）。enhanced が raw より点を落とした ID を軸ごとに機械抽出し、考察とチケットの Comments に「スキル改善候補」として列挙する
4. チケットを resolved にし、Comments に経緯を 1 段落で残す

### 注意点（このセッションで踏んだもの）
- ユーザーの Markdown エディタは表を整形して各セルに空白を詰める。転記の正規表現は `\| (raw|enhanced)\s*\| (\d)\s*\| ...` のように空白を許容する。qwen の転記スクリプトはチケット 03 の会話内のみで、ファイルとして残していない。再利用するなら `benchmarks/scripts/` に切り出してよい
- ユーザーは待ち時間に作業用紙を記入することがある。派生ファイル（別モデルの用紙など）を作る前に必ず読み直し、記入済みの用紙をコピー元にしない
- Windows の cp932 コンソールで日本語や記号を print すると落ちる。Python は `PYTHONIOENCODING=utf-8` を付けて実行する
- Bash ツールの heredoc はバックスラッシュ 2 つを 1 つに潰す（この行の通り、書いた直後に化ける）。正規表現を含む Python はファイルに書いてから実行するか、Edit/Write ツールで書く
- Pillow は標準環境にない。`uv run --with pillow python - <<EOF` で使う
- 基準モデルの t2i 判定シート（`results/gpt-image-2-5/t2i.md`）は品質軸の基準そのものなので、5 軸は付けず忠実・補完の所見だけ備考に書く（09 の手順 4）
- ComfyUI の連番は `_00001.png`（末尾アンダースコアなし）で出る。ランナーはどちらも受ける

## 完了（2026-09-24）
- 判定者の希望で手順 1〜3 を置き換えた: contact_sheet.py は作らず `scripts/make_compare.py`（対象 raw / enhanced / 基準 raw の横並び PNG）で見比べ、Claude の一次判定と 5 件ずつの確定は行わず作業用紙方式（チケット 07・08）で判定した
- 基準モデルの判定シート `results/gpt-image-2-5/t2i.md` は 5 軸を付けず、忠実・補完の所見を Claude が下書きして備考に書いた（判定者の確認前）
- 横断比較 `results/README.md` を新規作成（切り口 × モデルの表、用途別の所見、enhance の要否、共通して崩れる切り口）。`docs/README.md` の索引と `benchmarks/README.md` の構成に追加
- 最良軸の付け方を判定者の指示で変更: enhanced 行は「enhanced でも基準モデルに追いつくか」（既定 0）。`benchmarks/README.md` のルーブリックに追記。qwen-image-2-1 の enhanced 行の最良は旧解釈のまま
- スキル改善候補（問題用紙 ID と症状）:
  - krea-2-turbo: t2i-20（enhanced で麺がスープから浮く。補完・品質が raw より低下）、t2i-04（「膝上」で顔が見切れる傾向）
  - flux-2-klein-9b: t2i-16 anime（enhanced で橋の上に立たない）、t2i-01 / 04 / 09 / 15（レンズ・f 値などカメラ設定語で明るさ・色調・肌が過剰になる）
  - qwen-image-2-1: チケット 03 の列挙のとおり（t2i-10・11・16 油彩・21・23）
  - 3 モデル共通で崩れる切り口: text-ja（06）と看板の日本語（17・18）、ポスターのレイアウト（21）。enhance では埋まらないモデル側の限界
  - 基準モデル: 指定外の文字を足す（03・05・10・11・14・15・20・21・23）、余白（22）と数（10・23）の指示を守らない
