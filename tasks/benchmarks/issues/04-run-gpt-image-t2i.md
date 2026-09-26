# 04 基準モデル GPT-Image 2.5 で t2i の問題用紙を流す

Type: prototype
Status: resolved
Blocked by: 01

## 目的

「品質」軸の見比べ基準として、GPT-Image 2.5 で t2i 23 件（画風の変種 4 つを含めて 26 枚）を raw で生成し、他モデルと同じ命名で `benchmarks/_local/gpt-image-2-5/t2i/` に置く。生成はユーザーの非公開生成スクリプト（OpenAI Images API 経由）で行う。ComfyUI ではないので `run_t2i.py` は使わない。

## 固定する条件（変えない。判定シート冒頭と基本データに書く）

| 項目 | 値 | 理由 |
|------|-----|------|
| 経路 | `--via api` | 既定の `codex` 経路は size / quality / model を制御できない |
| model | `gpt-image-2.5-sunburst` の日付付きスナップショット（例 `gpt-image-2.5-sunburst-2026-09-08`。実在する ID をチケット 01 で確認して書く） | `flare` は高速版で基準に向かない。スナップショット固定で再現性を保つ |
| quality | `high`（ユーザーが `xhigh` を選んだらそれで統一） | 26 枚で揃える |
| size | 1:1 → `1024x1024`、3:2 → `1536x1024`、2:3 → `1024x1536`、3:4 → `864x1152`、16:9 → `1344x752` | プリセットにない比率はカスタム（両辺 16 の倍数・655,360 px 以上）。2K / 4K プリセットは使わない |
| プロンプト | 問題用紙の汎用プロンプトを逐語。`-f` でファイル渡し | 引用符・¥・日本語を含むため。書き換え・品質語の追加は禁止（`references/prompting.md` は使わない） |
| seed | なし（API に seed がない） | 判定シートに「seed なし」と書く |
| 出力名 | `--name <NN>-<slug>-raw_00001`（t2i-16 は `16-style-umbrella-bridge-raw-<variant-slug>_00001`） | `--name` はそのまま stem になる。他モデルの `_local` と同じ並びにする |

## 手順

1. チケット 01 を先に済ませ、`benchmarks/results/gpt-image-2-5/README.md` の基本データ（公式名・モデル ID・対応サイズ・ネイティブ i2i・参照枚数・RGBA）を公式ドキュメントの出典付きで埋める
2. 既存の `_local/gpt-image-2-5/t2i/` を確認する。すでにある画像（ユーザーが 1024x1536 で先行生成した t2i-23 等）が上の固定条件と同じ model / quality なら残し、違えば `.trash/` に移す
3. `benchmarks/scripts/run_gptimg.py` を新規作成する（標準ライブラリのみ）。役割は `run_t2i.py` の GPT-Image 版:
   - `benchmarks/t2i/[0-9][0-9]-*.md` から id / slug / aspect / variants / 汎用プロンプトを読む（`run_t2i.py` の `load_sheets` を流用してよい）
   - 問題用紙ごとにプロンプトを一時ファイル（`_local/gpt-image-2-5/prompts/<stem>.txt`、UTF-8）に書き、プラグインの `scripts/generate.py` を `--via api -f <file> --out-dir <abs _local/gpt-image-2-5/t2i> --model <id> --size <size> --quality <q> --name <stem>` で 1 枚ずつ呼ぶ
   - 呼び出しは `dotenvx run -- uv run <generate.py> ...`（暗号化 `.env` はリポジトリルートのものを使う）。`.env.keys` は読まない
   - 既に出力ファイルがあれば飛ばす。`--only` と `--dry-run` を付ける。実行後に `_local/gpt-image-2-5/t2i/run.json` に model / quality / size 表を書く
4. **コストの明示承認を取ってから実行する**。`--dry-run` で 26 枚の計画と概算費用（1 枚 0.01〜0.3 ドル）を示し、ユーザーが承認したら一括で回す。プラグインは明示起動専用（自動起動禁止）だが、ユーザーが計画を見て承認した一括実行はその趣旨に沿う
5. 生成後、26 ファイルの名前が他モデルの `_local` と一致することを確認し、判定シート `results/gpt-image-2-5/t2i.md` の冒頭に生成日・model ID・quality・size 表・「seed なし」を書く
6. 途中で拒否（moderation）された問題用紙があれば、書き換えずに Comments に ID と理由を記録し、その枚は欠番として次に進む

## 受け入れ条件

- Given 26 枚の raw 生成、When `_local/gpt-image-2-5/t2i/` に置く、Then 他モデルと同じ 26 のファイル名が揃い、`run.json` と判定シート冒頭に固定条件が書かれている
- Given 実行前、When 計画を示す、Then ユーザーの明示承認なしに API を呼んでいない

## Comments

- 2026-09-23: `scripts/run_gptimg.py` を作成（`run_t2i.py` の `load_sheets` / `jobs_for` を import）。dry-run で 26 枚・名前は flux-2-klein-9b の raw 名と一致（23 番は他モデル未生成）。`_local/gpt-image-2-5/` は未作成で先行生成の画像はなかった。手順 3 の「プラグインのスキルディレクトリに cd」は v1.x の前提で、導入済みの v2.1.0 はプロジェクトルートの dotenvx `.env` を読む仕様（`references/setup.md` B-2）なので、cwd はリポジトリルートのまま呼ぶ。model は `gpt-image-2.5-sunburst-2026-09-08`（公式ページで実在確認）、quality は `high`。公式の枚単価表は 2.5 にはないため概算はプラグイン記載の非公式値（26 枚で約 $1.6、上限の目安 $5）。ユーザーの承認待ちで API は未呼び出し
- 2026-09-23: ユーザー承認のうえ t2i-09 を 1 枚流して実費を確認（1,756 output tokens ≈ $0.053）後、残り 25 枚を一括実行。26 枚すべて生成、moderation 拒否なし、欠番なし。各 PNG の実寸は size 表どおり。実費合計 ≈ $1.07（output 35,396 tokens。大きいサイズほど画素あたりのトークンが少なく、画素比の概算 $1.65 より安い）。所要 987 秒。ファイル名は flux-2-klein-9b の raw 25 枚と一致し、23 番のみ他モデルが未生成。`run.json` と `results/gpt-image-2-5/t2i.md` 冒頭に固定条件を記入、`benchmarks/README.md` にランナーの節を追加。判定はチケット 09 で行う

