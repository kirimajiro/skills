# Krea 2 / Krea 2 Turbo の公式情報（スキルと基本データの根拠）

確認日: 2026-09-23。要約であり逐語ではない。数値・構文を転記するときは出典で再確認する。

## 出典

- 公式モデルカード（Turbo）: https://huggingface.co/krea/Krea-2-Turbo
- 公式モデルカード（Raw）: https://huggingface.co/krea/Krea-2-Raw
- 公式リポジトリ README: https://github.com/krea-ai/krea-2
- 公式プロンプトガイド: https://raw.githubusercontent.com/krea-ai/krea-2/main/docs/prompting.md
- 公式テクニカルレポート: https://www.krea.ai/blog/krea-2-technical-report
- 公式オープンソース案内: https://www.krea.ai/krea-2-open-source
- 公式ブログ（探索的プロンプティング）: https://www.krea.ai/blog/explorative-prompting-krea-2
- 公式ブログ（スタイル参照・ムードボード）: https://www.krea.ai/blog/krea-2-deep-dive-walkthrough
- ComfyUI 公式ブログ（ネイティブ対応）: https://blog.comfy.org/p/krea-2-open-source-models-are-now
- ComfyUI 公式テンプレートに同梱の Prompt Enhancer system instruction（ローカルの API JSON `30:18` に転記されている。Krea チーム提供）

## 系譜とアーキテクチャ

- Krea 初の自社基盤モデル。約 12B（技術レポートでは 12.9B）の dense DiT、28 ブロック、幅 6144、single-stream、GQA + gated sigmoid attention、SwiGLU 4x、3D axial RoPE
- テキストエンコーダは Qwen3-VL-4B-Instruct。複数層の特徴を集約する独自機構（multi-layer feature aggregation）。ComfyUI では CLIPLoader type `krea2`
- VAE は Qwen Image VAE（初期／公開モデル）。大型モデルでは FLUX 2 VAE も使う
- Qwen-Image の重みに基づくモデルではなく、VAE とテキストエンコーダ系統を共有するだけ。「ゼロから構築」と公式が明記
- 事前学習に AI 生成画像を使わない。多段キャプション（OCR 抽出＋長文説明）を多様な長さ・形式に整形して学習 → 長い自然文プロンプトと相性がよい
- RL の報酬にテキスト描画報酬を含む

## Raw と Turbo

- **Raw**: 蒸留・後学習なしの基盤チェックポイント。fine-tune / LoRA 学習向け。推奨 52 steps / CFG 3.5 / 約 1K
- **Turbo**: Trajectory Distribution Matching（TDM）による guidance・timestep 蒸留。推奨 **8 steps / guidance 0.0 / mu 1.15**、解像度 1K〜2K（各辺は 16 の倍数にパディング）。CFG が無効なのでネガティブプロンプトは効かない（モデルカード例: `guidance_scale=0.0`）
- 公式の勧め: 「Raw で学習し Turbo で生成」
- 公開日 2026-06-22。ComfyUI は v0.26.0（2026-06-23）で標準ノードのみで対応

## i2i・参照画像

- モデルカード・README とも **text-to-image のみ**。画像編集・img2img・参照画像入力は公開重みには含まれない
- krea.ai のサービス上の「スタイル参照（最大4枚、強度 20〜80%）」「ムードボード」は技術レポートに記載があるが、プラットフォーム機能であり公開重みの入力仕様ではない（オープンソース版での提供は未検証）
- 結論: ベンチマークの i2i 問題用紙の対象外。スキルも t2i のみ

## プロンプトの公式ガイダンス

- 自然文（会話的な記述）で書く。タグ列ではない
- 「長く詳細なプロンプトが最良の結果を出すが、最小限のプロンプトでも高品質」（prompting.md）。ComfyUI ブログも「Detailed, long prompts give the best quality」
- 描画する文字は引用符で囲む（"For text rendering, we recommend putting quotes around the words to be rendered."）
- 公式例の構成順: 主題・場面 → 画風・媒体 → 属性の詳細 → 雰囲気・環境 → 光と色 → 構図・視点。最短例は約 10 語、最長は 200 語超の油彩調の記述
- 探索的プロンプティング（公式ブログ）: まず曖昧な短いプロンプト（例 "a cat riding a bicycle"）で幅を見て、気に入った方向に画風ヒントをカンマで足す（例 "a cat riding a bicycle, retro cartoon illustration"、"…, dreamy cinematic scene"）。モデルは特定の既定美学を押し付けない（"unopinionated"）ので、lo-fi VHS のような画風も丸めずに出す
- 公式 Prompt Enhancer の規則（ComfyUI テンプレート同梱）: 忠実さ最優先（主題・動作・色・位置関係を保持し、示唆のない物や人物を足さない）／主体ごとに属性と動作をまとめる／画風・媒体・構図・光は内部で 2〜3 案から選ぶ／文字は正確に引用符で／過剰指定を避ける（入力が支持しない具体的な服・色・素材を発明しない）／1 段落・箇条書きなし／既に詳細な入力は軽く磨くだけ／ユーザーが媒体を指定したら守る
- 技術レポート: 「密なプロンプトが確実に良い結果を出すが、利用者は学習時のキャプションに似た文を書かない」ため、意図を上書きせずに視覚的方向を補う prompt expander を用意した。本プロジェクトではこの役割をスキルが担い、ワークフロー内蔵の enhancer は使わない

## ライセンス

- モデル重み: 「Krea 2 Community License」（モデルカード）。商用ライセンスは opensource@krea.ai 経由（README）。条項の詳細は未検証
- リポジトリのコード: Apache License 2.0（LICENSE.md）

## スキルでの読み替え

- 肯定形の記述（本プロジェクト共通）は、CFG 無効でネガティブが効かない Turbo と特に相性がよい
- 「過剰指定を避ける」を Qwen スキルとの差として取り込む: 依頼が支持しない小物・色・素材を発明せず、代わりに画風・媒体・光・構図の方向付けで密度を出す
- 依頼が曖昧なときは探索モード（画風ヒント違いの短いプロンプトを 2〜3 本）を提示し、選ばれた方向を密な 1 段落に育てる
