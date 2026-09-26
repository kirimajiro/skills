# benchmarks — モデルの得意不得意を掴む定型プロンプト

生成モデルに同じ問題用紙を流し、人が判定する。t2i は一対比較（同じ問題用紙の 2 枚を並べ、観点ごとに 2 択で答える）、i2i は 5 軸のルーブリック。目的は利用者がモデルの得意不得意を掴むことであり、順位付けではない。

## 構成

```
benchmarks/
  README.md                 この文書（手順・一対比較・観点セット・命名）
  t2i/NN-<slug>.md          問題用紙（text-to-image）。汎用プロンプト・見るもの・pairwise（観点と設問）
  i2i/NN-<slug>.md          問題用紙（画像編集）。汎用指示と使う参照画像
  refs/                     i2i 用の固定参照画像とその仕様（refs/README.md）
  results/README.md         横断比較（観点 × モデルの表と用途別の所見）
  results/TEMPLATE-t2i.md   t2i 判定シートの雛形
  results/<model-slug>/     モデルごとの基本データと判定シート
    README.md               基本データ（公式名・ネイティブ i2i 対応・上限・出典）
    t2i.md                  t2i 判定シート（観点別プロファイル・感想戦・enhance 済みプロンプト）
    i2i.md                  i2i 判定シート（ネイティブ i2i 対応モデルのみ）
  _local/<model-slug>/      生成画像の置き場。git 管理外
  _local/pairwise/          一対比較の HTML・セッション JSON・集計 Markdown。git 管理外
  scripts/                  run_t2i.py / run_i2i.py / run_gptimg.py（生成）、pairwise_build.py + pairwise_template.html（一対比較の HTML）、pairwise_report.py（セッション JSON → Markdown 集計）
```

## 手順

1. **基本データを書く**: `results/<model-slug>/README.md` に公式名・バージョン・ネイティブ i2i 対応の有無・参照枚数上限・ネイティブ解像度・RGBA 対応を、公式の一次情報の出典付きで書く。i2i の問題用紙は、ここでネイティブ i2i 対応と確認できたモデルにだけ流す
2. **enhance 済みプロンプトを作る**: そのモデルのスキル（`skills/<plugin-name>/SKILL.md`）で各問題用紙の汎用プロンプトを書き直し、判定シートの「Enhanced prompts」に貼る。スキルがないモデル（基準モデル等）は汎用プロンプトのみ流す
3. **生成する**: 問題用紙ごとに `raw`（汎用プロンプトそのまま）と `enhanced`（enhance 済み）を seed 1 で 1 枚ずつ生成する。raw と enhanced は同じ seed にして対で見比べる。サイズは問題用紙の `aspect` に最も近い対応比率を約 1 MP で使い、ワークフロー設定（steps / guidance / sampler / 解像度）は判定シートの冒頭に記録する。品質タグ・ネガティブプロンプトは付けない。モデルが要求する定型（RGBA ラッパー等）はスキルが enhance 側に入れる
4. **画像を置く**: `_local/<model-slug>/<mode>/<NN>-<slug>-<variant>_<seed 5桁>.png`（例: `_local/qwen-image-2-1/t2i/01-short-rainy-alley-enhanced_00001.png`）。サブフォルダを切らず 1 階層に並べる。ComfyUI なら `scripts/run_t2i.py` が 3 と 4 をまとめて行う（下記）
5. **一対比較を build する（t2i）**: Claude が `scripts/pairwise_build.py` を 3 モードで実行し、`_local/pairwise/<session-id>.html` を作る（下記「一対比較」）
6. **判定する**: 判定者が HTML をブラウザで開き、設問ごとに 左 / 右 / 引き分け を答える。終了画面で雑感を書き、JSON をダウンロードして `_local/pairwise/` に置く。i2i は問題用紙の「見るもの」を参照しながら 5 軸で判定シートに記入する
7. **集計する**: Claude が `scripts/pairwise_report.py` でセッション JSON を合算し、`_local/pairwise/report-<model-slug>.md` に出す
8. **感想戦**: Claude が集計の要点（強い観点・弱い観点・enhance の効き・引き分けの偏り）を提示してから、観点のまとまりごとに 1 往復で聞く: 勝った / 負けた理由、意外だった点、用途としてどうか。1 問ずつのウィザードにしない。ヒアリングは AskUserQuestion か通常のチャットで、判定者の言葉はそのまま判定シートに写す
9. **判定シートを書く**: `results/TEMPLATE-t2i.md` を写して `results/<model-slug>/t2i.md` を書き、`results/README.md` の観点 × モデル表と用途別の所見を更新する。enhance が下げた観点は問題用紙 ID 付きで「スキル改善候補」に残し、必要ならそのモデルの effort にチケットを起こす

## ComfyUI で自動生成する（scripts/run_t2i.py）

ComfyUI の HTTP API に問題用紙 × variant × seed を順に投入し、画像を `_local/` に取り込む。標準ライブラリのみで動く。

1. ComfyUI でワークフローを作り、Dev mode を有効にして「Export (API)」で API 形式の JSON を `_local/` に保存する
2. スクリプト冒頭の `NODE_MAPS` に model-slug ごとのノード id と入力名を足す（prompt / negative / width / height / seed / filename_prefix / KSampler。ない入力は省略可）。起動時に JSON と照合し、食い違えば止まる
3. まず小さく試す: `python benchmarks/scripts/run_t2i.py --model <model-slug> --api-json <json> --only 01`
4. 本番: `--only` を外して実行する。`--variants enhanced` で enhanced だけ、`--seeds 4` で seed 1〜4、`--seeds sheet` で問題用紙の `samples` 枚。既に画像があるものは飛ばすので、中断しても再実行で続きから回る。`--dry-run` で投入計画だけ表示できる
   - ComfyUI の連番を seed に一致させるため、ComfyUI の output 側 `Bench/<model-slug>/t2i/` に同じプレフィックスの古いファイルを残さない。食い違うとスクリプトが警告する
5. 実行後、`_local/<model-slug>/t2i/run.json` に設定（steps / cfg / sampler / scheduler / サイズ表）が残るので、判定シートの冒頭に写す

## 基準モデルを API で生成する（scripts/run_gptimg.py）

GPT-Image 2.5 は ComfyUI ではなく OpenAI Images API で生成する。API を叩く生成スクリプト（`generate.py`）はリポジトリ所有者の非公開ツールでこのリポジトリには含めない。求める CLI 契約は `run_gptimg.py` 冒頭の docstring に書いてあるので、同じ契約のスクリプトを用意して `--generate-py` か環境変数 `GPTIMG_GENERATE_PY` で渡す。`run_gptimg.py` は問題用紙ごとにプロンプトを逐語でファイルに書き、生成スクリプトを 1 枚ずつ呼んで `_local/gpt-image-2-5/t2i/` に同じ命名で置く。raw のみ。model / quality / size 表はスクリプト冒頭で固定し、`run.json` に各画像の実トークン数とともに残る。

1. リポジトリルートに dotenvx 暗号化の `.env`（`OPENAI_API_KEY`）を置き、`uv` と `dotenvx` を PATH に通す
2. `python benchmarks/scripts/run_gptimg.py --dry-run` で枚数と概算費用を確認してから、`--dry-run` を外して実行する（`--only 09` で 1 枚だけ）。既にある画像は飛ばす。moderation で拒否された問題用紙は `run.json` の `refused` に残り、欠番になる
3. i2i の問題用紙は `--i2i` で回す（raw のみ。問題用紙の `refs` を images.edit の参照として渡し、`_local/gpt-image-2-5/i2i/` に置く）。ComfyUI 側の i2i は `scripts/run_i2i.py`（参照画像は `refs/` から自動アップロード。`--model` と `--api-json` は run_t2i.py と同じ）
4. i2i の参照画像の候補は `--refs 4` で作る（`refs/README.md` の仕様ごとに 4 枚、768x1024、`_local/gpt-image-2-5/refs/`）。選んだ 1 枚を `refs/ref-NN.png` にコピーして固定する

## 一対比較（t2i）

判定者はブラウザで 1 画面 1 設問の 2 択を繰り返す。どちらが A / B かは設問ごとにランダムに入れ替わり、モデル名は終了画面まで出ない。ツールは標準ライブラリだけで動き、HTML は CDN なしの単一ファイルで `file://` で開く。

### モード

```
python benchmarks/scripts/pairwise_build.py --mode ab --a <model-slug> --b <model-slug> [--variant enhanced|raw] [--baseline show|hide]
python benchmarks/scripts/pairwise_build.py --mode raw-enh --a <model-slug> [--baseline show|hide]
python benchmarks/scripts/pairwise_build.py --mode vs-baseline --a <model-slug> [--variant enhanced|raw]
共通: [--only 05,06,21] [--seed 1] [--out <html>]
```

| モード | A | B | 見たいもの |
|---|---|---|---|
| `ab` | `--a` の enhanced（`--variant raw` で raw） | `--b` の同じ variant | ローカル A vs B で観点ごとにどちらが優れるか |
| `raw-enh` | `--a` の enhanced | `--a` の raw | enhance（スキル）がどの観点を上げ、どの観点を下げるか |
| `vs-baseline` | `--a` の enhanced | 基準モデルの raw | ローカルモデルの力量の物差し。用途の使い分けの根拠にはしない（使い分けはプロジェクトに応じて決める） |

- `--baseline show`: ab / raw-enh のとき、基準モデルの画像を「この観点で目指すところ」の参考として脇に小さく出す（画面のボタンで隠せる）。既定は hide
- セッション ID は `<mode>_<a>[_<b>]_<YYYYMMDD-HHMM>`。1 セッション = 1 モード × 全問題用紙（`--only` で絞れる）。t2i-16 は画風ごとに別の問題として出る
- 画像が欠けている問題用紙はスキップし、起動時に一覧を出す。左右の入れ替えはセッション ID から決まるので、同じ HTML を開き直しても変わらない
- `--rebuild <html>`: テンプレートを直したあと、既存の HTML にセッション ID と左右の割り当てを保ったまま再適用する（回答は `localStorage` に残っているので続きから開ける）
- 新しいモデルを判定するときの標準は 3 セッション: `ab`（既存のローカルモデルと）、`raw-enh`、`vs-baseline`。1 セッション 85 問で 5〜20 分

### 画面と操作

- 上部に問題用紙の見出し・日本語 1 行要約・汎用プロンプト・設問・進捗。中央に左右 2 枚（クリックで拡大）
- ← 左が良い / → 右が良い / Space 引き分け / Backspace 直前の回答を修正
- 回答は `localStorage` に逐次保存され、同じ HTML を開き直すと続きから
- 終了画面: 観点別の集計（A の勝率と件数）、問題用紙別の見返しギャラリー（2 枚と回答を並べ、A / B のモデル名を開示。雑感を書く前に見返す用）、雑感の入力欄（全体 1 つと観点ごと任意）、「JSON をダウンロード」

### 集計

```
python benchmarks/scripts/pairwise_report.py benchmarks/_local/pairwise/*.json [--model <model-slug>] --out benchmarks/_local/pairwise/report-<model-slug>.md
```

- 出力: セッション一覧 / 観点別プロファイル（行 = 観点、列 = 対戦）/ enhance の効き / 問題用紙別（o 勝ち・= 引き分け・x 負け）と負けが集中した問題用紙 / 雑感の転記
- 勝率 = (勝 + 0.5 × 分) / n。Elo や Bradley-Terry は使わない（順位付けが目的ではないため）。n が 3 未満のセルには `*`
- モデルが B 側のセッションは勝敗を反転して「そのモデルの勝率」に揃える。同じ問題用紙・観点・対戦の組が複数セッションにあれば合算する
- 読み方: 引き分けが多い観点は「その対戦では差が出ない観点」。raw-enh の勝率 > 0.5 は enhance が効いた観点、< 0.5 は enhance が下げた観点（スキル改善候補）
- Windows の cp932 コンソールでは `--out` でファイルに出す（stdout は文字化けするが落ちない）

### 観点セット

観点の ID はリポジトリ全体で共通で、問題用紙の frontmatter `pairwise:` が「その問題用紙で問う観点と設問文」を持つ。設問文の言い回しは問題用紙ごとに自由。1 問題用紙 3〜4 観点、omnibus は 7。

| ID | 観点 | 見るもの |
|---|---|---|
| texture | 質感の本物感 | 3D・CG っぽくなく、本物の写真（絵）に見えるか |
| detail | ディテールとグランジ | 汚れ・傷・経年・書き込みの説得力 |
| text | 文字の正確さ | 指示した文字列・字形の正確さ |
| layout | 文字とレイアウト | 文字の配置・全体の設計 |
| structure | 構造物とパース | 直線・遠近・機構・鏡像の整合 |
| anatomy | 人体・手指・ポーズ | 関節・手指・持ち物との接触・ポーズの自然さ |
| skin | 肌と表情 | 肌の質感と表情の説得力 |
| context | 補完の文脈適合 | 指示にない要素が場面に合っているか |
| style | 画風の成立 | 指示した画風として成立しているか |
| organic | 有機物の自然さ | 動物・植物・地形の描写 |
| composition | 構図とショット | 指示した視点・寄り・奥行き・投影の成立 |
| light | 光と素材 | 逆光・艶・透過・反射・空気感 |
| culture | 文化的な正しさ | 日本の意匠・風俗として違和感がないか |
| fidelity | 要素の揃い方 | 多要素の指示のうち、どちらに多く揃っているか（omnibus 用） |

## ルーブリック（i2i・5軸）

各軸を 0 / 1 / 2 でつける。0 不可 = 大半の生成が軸の要件を満たさない、1 条件付き = 満たす生成と満たさない生成が混ざる（選べば使える）、2 良 = 大半の生成が満たす。

| 軸 | 略称 | 見るもの |
|----|------|---------|
| 指示された編集の実行 | 実行 | 指示した変更がはっきり起きているか |
| 指示外の保持 | 保持 | 顔の同一性・背景・構図・描画媒体など、指示していない部分が保たれているか |
| 参照の転写精度 | 転写 | 参照画像から取るもの（衣服・ポーズ・画風）が正確に移っているか。参照1枚の問題用紙では同一性の保持で代替する |
| 整合と自然さ | 整合 | 光・縮尺・接地・遠近が元画像と合い、継ぎ目が見えないか |
| フロンティア比の品質 | 品質 | 基準モデルの結果と比べてどの程度か |

## 基準モデル

現時点の基準は GPT-Image 2.5。基準モデルでも同じ問題用紙を一度 raw で生成し、`_local/gpt-image-2-5/` に置く（基本データは `results/gpt-image-2-5/`）。基準を変えたら判定シートの冒頭に基準モデル名を書き、古い判定は基準名付きで残す。

## 問題用紙の書式

frontmatter に `id` / `dimension`（切り口）/ `samples` / `aspect` / `summary`（汎用プロンプトの日本語 1 行要約。一対比較の画面に出す）/ `pairwise`（観点 ID と設問文の一覧。観点セット参照）、本文に汎用プロンプト（英語・1〜3文・品質タグなし）と「見るもの」（日本語）。i2i は使う参照画像を `refs` に列挙する。切り口は `t2i/` の一覧を参照。汎用プロンプトを変えたら、既存の判定は無効になるので、問題用紙の `id` は変えずに判定シートの該当行を消す。

## 切り口（dimension）

| dimension | 見たい能力 |
|-----------|-----------|
| short-instruction | 短い指示での補完力 |
| long-instruction | 長い指示への忠実さ（数・属性・位置の結び付け） |
| text-en / text-ja | テキスト描画（英語 / 日本語） |
| human-pose | 人体・ポーズ・表情 |
| inorganic | 無機物の描写力（建物・機械） |
| organic | 有機物の描写力（動物・自然） |
| shot | ショット種別（ワイド・クローズアップ・POV・アイソメトリック） |
| style-range | 画風の幅（写真・アニメ・絵画・フラット） |
| japan-culture | 日本の風景・文化の知識 |
| material-light | 素材・質感・光（プロダクト・フード） |
| layout | レイアウト（ポスターの雰囲気・余白の効き） |
| omnibus | 総合（一本のプロンプトで多くの切り口を同時に要求し、崩れる順番を見る） |
