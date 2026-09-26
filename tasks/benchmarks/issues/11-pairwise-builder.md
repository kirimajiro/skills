# 11 一対比較の静的 HTML を生成する `scripts/pairwise_build.py` を作る

Type: task
Story: pairwise
Status: resolved
Blocked by: 10

## 目的

ライブラリ非依存の Python スクリプトが、問題用紙の `pairwise:` と `_local/` の画像一覧から、単一の静的 HTML（サーバー不要、`file://` で開く）を生成する。判定者はブラウザで 1 画面 1 設問の 2 択を繰り返し、最後に観点別の集計を画面で見て、雑感を入力し、JSON をダウンロードする。LLM（Claude / Codex）はスクリプトを実行するだけで、HTML を書かない。

## 仕様

### 起動

```
python benchmarks/scripts/pairwise_build.py --mode ab --a krea-2-turbo --b flux-2-klein-9b [--variant enhanced] [--baseline show|hide]
python benchmarks/scripts/pairwise_build.py --mode raw-enh --a krea-2-turbo [--baseline show|hide]
python benchmarks/scripts/pairwise_build.py --mode vs-baseline --a krea-2-turbo [--variant enhanced]
[--only 05,06,21] [--out benchmarks/_local/pairwise/<session-id>.html]
```

- `--mode ab`: ローカル A vs B（既定は enhanced 同士。`--variant raw` で raw 同士）
- `--mode raw-enh`: 同一モデルの raw vs enhanced
- `--mode vs-baseline`: ローカル A（enhanced）vs 基準モデル raw
- `--baseline show`: ab / raw-enh のとき、基準モデルの画像を「この観点で目指すところ」の参考として脇に小さく表示する（トグルで隠せる）。既定は hide
- セッション ID は `<mode>_<a>[_<b>]_<YYYYMMDD-HHMM>`。1 セッション = 1 モード × 全問題用紙（`--only` で絞れる）
- t2i-16 は画風ごとに別の問題として扱う（4 問）
- 画像は `../<model-slug>/t2i/<NN>-<slug>-<variant>_00001.png` の相対パスで参照する（HTML は `_local/pairwise/` に置く）

### 画面

- 上部: 問題用紙の見出しと汎用プロンプトの要約（日本語 1 行。作業用紙の raw 要約を流用してよい）、設問（`pairwise[].q`）、進捗（n / N）
- 中央: 左右 2 枚。どちらが A / B かは設問ごとにランダムに入れ替え、モデル名は出さない（ブラインド）。クリックで拡大
- 脇: `--baseline show` のときだけ基準モデルの画像（小）。トグルで非表示
- 入力: 左 / 右 / 引き分け（キー: ← → スペース）。戻るで直前を修正できる
- 出題順: 問題用紙の順に、その問題用紙の設問を順に出す（同じペアを設問ごとに見せる）。設問の順は固定
- 途中保存: `localStorage` に回答を逐次保存し、同じ HTML を開き直すと続きから
- 終了画面: 観点別の集計（A の勝率と件数。引き分けは 0.5 勝）と問題用紙別の一覧、そこで初めて A / B のモデル名を開示。その下に雑感の入力欄（全体 1 つと、観点ごとに任意）。「JSON をダウンロード」で `<session-id>.json` を落とす

### JSON 書式

```json
{
  "session": {"id": "...", "mode": "ab", "a": {"model": "krea-2-turbo", "variant": "enhanced"}, "b": {"model": "flux-2-klein-9b", "variant": "enhanced"}, "baseline_shown": false, "created": "2026-09-25T10:00:00", "finished": "..."},
  "answers": [
    {"problem": "t2i-05", "style": null, "aspect": "text", "q": "...", "left": "a", "right": "b", "choice": "left|right|tie", "ms": 4200}
  ],
  "notes": {"overall": "...", "by_aspect": {"text": "..."}}
}
```

### 実装の制約

- 生成側・HTML 側とも外部ライブラリ・CDN なし。HTML/CSS/JS はスクリプト内のテンプレート（またはスクリプトと同じフォルダの `pairwise_template.html`）に置く
- frontmatter の読み取りは標準ライブラリだけで行う（既存の `run_t2i.py` の読み方に合わせる）
- Windows の cp932 コンソールで落ちないよう、標準出力に日本語を出さないか `PYTHONIOENCODING=utf-8` 前提を README に書く
- 画像が欠けている問題用紙はスキップし、起動時に一覧を出す

## 受け入れ条件

- Given 10 の `pairwise:` 付き問題用紙と 3 モデル＋基準の画像、When 3 つのモードで build する、Then それぞれの HTML が `file://` で開き、画像が表示され、キー操作だけで最後まで進める
- Given 途中でブラウザを閉じる、When 同じ HTML を開き直す、Then 続きから再開できる
- Given 全設問に答える、When 終了画面を見る、Then 観点別の勝率と件数、モデル名の開示、雑感欄、JSON のダウンロードがある
- Given ダウンロードした JSON、When 書式を見る、Then 上記の schema に一致する

## Comments

## Answer

- `scripts/pairwise_build.py` + `scripts/pairwise_template.html`（テンプレートは別ファイル。`/*__DATA__*/null` をセッション JSON に置換）。3 モード・`--only`・`--baseline show`・`--out` を仕様どおり実装
- 左右のランダム入れ替えはビルド時にセッション ID を seed に決めるので、開き直しても入れ替えが変わらない
- raw-enh は A = enhanced・B = raw に固定（「A の勝率 > 0.5 = enhance が効いた」と読めるように）
- 検証: 3 モードでビルドし、埋め込み画像パス 26 件がすべて実在。HTML の JS は node のスタブ DOM で回答・保存・戻る・終了画面・JSON 生成まで通した。ブラウザでの見た目とキー操作の実確認はチケット 14 の実試行で行う（Claude 側の Chrome 拡張が未接続のため）
