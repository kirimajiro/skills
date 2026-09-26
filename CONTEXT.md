# CONTEXT — ドメイン用語集

このプロジェクトで使う用語の正。新しい用語が生まれたらここに定義してから使う。同義語に流れない。

## 成果物

- **スキル**: `skills/<plugin-name>/` に置く、対象モデル向けプロンプト組み立ての指示書一式。無印と軽量版からなる
- **無印**: `SKILL.md`。フロンティアモデルの LLM（Claude Code / Codex 等）向けの通常スキル。プラグインとして読まれるのはこのファイルだけ。スキルの正
- **軽量版**: `SKILL-lite-<mode>.md`。27B 級の汎用 LLM を ComfyUI 等の LLM ノードで動かすときに system prompt としてそのまま貼るファイル。frontmatter なし、単発変換の契約。無印から導出する
- **mode**: 軽量版を分けるときの操作単位。`t2i`（text-to-image）/ `i2i`（画像編集・複数参照）等
- **プラグイン**: marketplace.json に登録する配布単位。1プラグイン = 1スキル = 1モデル
- **モデル**: プラグイン分割の粒度。バージョンや派生名まで含めて一意に特定する（例: `qwen-image-2-1`、`flux-2-klein`）。同じファミリーでも生い立ちが違えば別モデル
- **plugin-name**: モデルを一意に特定する英小文字ハイフン区切り slug。フォルダ名・SKILL.md の `name`・marketplace.json の `name` で一致させる
- **references**: スキルが実行時に読む参照資料（`skills/<plugin-name>/references/`）。常時読まれる SKILL.md 本文から逃がした資料
- **marketplace.json**: `.claude-plugin/marketplace.json`。配布するプラグイン一覧の正。`description` は SKILL.md の description を写す

## 対象モデル

- **対象モデル**: スキルがプロンプトを組み立てる先のクリエイティブ用AI。画像・動画・音楽・3D を横断する
- **一次情報**: 対象モデルの公式ドキュメント・公式ガイド・公式リリースノート・公式の prompt enhancer の system prompt。仕様は一次情報で確認し、出典を残す
- **肯定形の記述**: 避けたいものを挙げず、望む状態を描写するプロンプトの書き方。このプロジェクトの無印・軽量版に共通する方針

## 検証

- **構造検証**: Claude が行う検証。frontmatter・参照ファイルの実在・marketplace.json との整合・軽量版の契約と無印との整合・pruning 観点
- **実試行**: ユーザーが対象モデル（軽量版は ComfyUI 上の LLM ノード）でスキルを試すこと。Claude は試行手順を提示し、結果報告を受けて完了とする
- **完了**: 構造検証と実試行の両方を通したこと

## ベンチマーク

- **問題用紙**: `benchmarks/t2i/` `benchmarks/i2i/` の1ファイル。汎用プロンプトと「見るもの」を持つ。`id` は変えない
- **汎用プロンプト**: どのモデルにもそのまま渡せる英語・1〜3文・品質タグなしのプロンプト。問題用紙の正
- **raw / enhanced**: 同じ問題用紙を、汎用プロンプトそのまま（raw）と、そのモデルのスキルで書き直したもの（enhanced）の2通りで流す。差が enhance と品質タグの要否を示す
- **切り口（dimension）**: 問題用紙が見たい能力の分類。一覧は `benchmarks/README.md`
- **観点（aspect）**: 一対比較の設問の分類。リポジトリ共通の ID（texture / text / anatomy 等）を持ち、一覧は `benchmarks/README.md` の観点セット。問題用紙の `pairwise:` が、その問題用紙で問う観点と設問文を持つ
- **一対比較**: t2i の判定方式。同じ問題用紙の 2 枚を並べ、観点ごとの設問に 左 / 右 / 引き分け で答える。順位付けではなく、観点別の勝率からモデルの強みを浮かび上がらせる
- **セッション**: 一対比較の 1 回分。1 モード（A vs B / raw vs enhanced / vs 基準）× 全問題用紙。ID は `<mode>_<a>[_<b>]_<日時>`、結果は `benchmarks/_local/pairwise/<session-id>.json`
- **感想戦**: セッション後に判定者の雑感を聞き、観点・問題用紙 ID に結び付けて判定シートに書く工程。利用者向けの成果物はここから生まれる
- **5軸**: i2i の判定ルーブリック。実行 / 保持 / 転写 / 整合 / 品質、各軸 0 / 1 / 2。t2i は一対比較に置き換えた
- **判定シート**: `benchmarks/results/<model-slug>/<mode>.md`。t2i は観点別プロファイル・enhance の効き・感想戦・スキル改善候補・enhance 済みプロンプトを置く（雛形 `benchmarks/results/TEMPLATE-t2i.md`）。i2i は 5軸の判定と考察。感想戦（i2i は考察）が利用者向けの成果物
- **基本データ**: `benchmarks/results/<model-slug>/README.md`。公式名・ネイティブ i2i 対応・上限などを出典付きで書く。i2i の問題用紙はここでネイティブ i2i 対応と確認できたモデルにだけ流す
- **基準モデル**: vs-baseline モードと i2i「品質」軸の比較対象。ローカルモデルの力量の物差しで、用途の使い分けの根拠にはしない。現時点は GPT-Image 2.5
- **model-slug**: 判定シートのフォルダ名。スキルがあるモデルは plugin-name と同じ。基準モデルなどスキルがないモデルも同じ規則で付ける（例: `gpt-image-2-5`）
- **参照画像（refs）**: i2i の問題用紙が使う固定画像。`benchmarks/refs/` に仕様と画像を置く。自前生成の架空の人物・物品に限る

## 進行管理

- **effort**: `tasks/<slug>/` の1ディレクトリ。エピックに相当
- **チケット**: `tasks/<slug>/issues/NN-<slug>.md`。1ファイル = 1タスク
- **board**: `tasks/README.md`。進行中ストーリーの優先順だけを書く
- **frontier**: effort 内の open・unblocked・unclaimed なチケットのうち番号最小のもの。「次」はここから導出する
