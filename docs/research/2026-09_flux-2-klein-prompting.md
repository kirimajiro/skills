# FLUX.2 [klein] の公式情報（スキルと基本データの根拠）

確認日: 2026-09-23。要約であり逐語ではない。数値・構文を転記するときは出典で再確認する。

## 出典

- BFL 公式ブログ（発表）: https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence
- 公式モデルカード（9B 蒸留）: https://huggingface.co/black-forest-labs/FLUX.2-klein-9B
- 公式モデルカード（9B 蒸留 FP8）: https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8
- 公式モデルカード（9B base・未蒸留）: https://huggingface.co/black-forest-labs/FLUX.2-klein-base-9B
- 公式モデルカード（4B 蒸留）: https://huggingface.co/black-forest-labs/FLUX.2-klein-4B
- 公式リポジトリ README: https://github.com/black-forest-labs/flux2
- BFL 公式プロンプトガイド（索引）: https://docs.bfl.ml/guides/prompting_summary
- 同 Prompting Basics: https://docs.bfl.ml/guides/prompting_unified_basics
- 同 Building a Good Prompt: https://docs.bfl.ml/guides/prompting_unified_building
- 同 Style, Aesthetics & Text: https://docs.bfl.ml/guides/prompting_unified_style
- 同 Typography & Design: https://docs.bfl.ml/guides/usecases_t2i_typography_design
- 同 JSON Structured Prompting: https://docs.bfl.ml/guides/usecases_t2i_json_prompting
- 同 Editing Overview / Single-Reference / Multi-Reference: https://docs.bfl.ml/guides/prompting_editing_overview ・ https://docs.bfl.ml/guides/prompting_editing_single_reference ・ https://docs.bfl.ml/guides/prompting_editing_multi_reference
- ComfyUI 公式チュートリアル: https://docs.comfy.org/tutorials/flux/flux-2-klein
- ComfyUI 公式ブログ: https://blog.comfy.org/p/flux2-klein-4b-fast-local-image-editing

## 系譜と変種

- FLUX.2 [klein] は Black Forest Labs の FLUX.2 ファミリーの小型モデル。公開日 2026-01-15。「生成と編集を1つのコンパクトなアーキテクチャに統合」し、t2i・単一参照編集・複数参照生成を同じ重みで行う
- 4 変種: **4B 蒸留** / **4B base** / **9B 蒸留** / **9B base**。9B は「9B rectified flow transformer + 8B Qwen3 text embedder」。4B のテキストエンコーダは ComfyUI の配布ファイル名から Qwen3-4B（`qwen_3_4b.safetensors`）
- 蒸留版は step 蒸留＋guidance 蒸留で **4 steps**、公式コード例は `num_inference_steps=4, guidance_scale=1.0`。base は「step・guidance 蒸留なしで学習」し「蒸留版より出力の多様性が高い」、公式コード例は `num_inference_steps=50, guidance_scale=4.0`。README: 「本番・リアルタイムは蒸留版、fine-tune / LoRA は base（約 50 steps）」
- どの FLUX.2 変種（dev / pro / flex）から蒸留したかは公式に明記なし（未検証）。FLUX.2 [dev] は 32B
- FP8 / NVFP4 版を NVIDIA と共同で提供。9B は約 29GB VRAM（bf16）、4B は約 13GB
- ComfyUI 公式の 9B 用ファイル名: 蒸留 `flux-2-klein-9b-fp8.safetensors`、base `flux-2-klein-base-9b-fp8.safetensors`、テキストエンコーダ `qwen_3_8b_fp8mixed.safetensors`、VAE `flux2-vae.safetensors`。ユーザーのワークフローの拡散モデル名は蒸留版と一致する。VAE `full_encoder_small_decoder.safetensors` は公式チュートリアルの一覧にない（軽量デコーダ版と推定。未検証）
- ComfyUI 公式ブログの目安: 9B 蒸留 4 steps 約 2 秒（RTX 5090）、9B base 50 steps 約 35 秒

## 推奨設定と CFG

- 蒸留版: 4 steps / guidance 1.0（CFG 実質無効）。base: 50 steps / guidance 4.0
- ユーザーのワークフロー（Flux2Scheduler 20 steps、CFGGuider cfg 5、euler）は蒸留版チェックポイントに base 相当の設定を当てている。公式推奨と異なるため、ベンチマークの基本データに明記し、設定変更の要否はユーザー判断に委ねる
- 解像度: 公式例は 1024×1024。対応比率の一覧は公式に見当たらない（未検証）。ComfyUI のテンプレートは 1MP 前後

## i2i・参照画像

- 公開重み（蒸留・base とも）は「Text-to-Image ✅ / Single-ref Editing ✅ / Multi-ref Editing ✅」（README）
- BFL プロンプトガイド: **FLUX.2 [klein] の参照画像は最大 4 枚**（[max/pro/flex] は API 8 枚、[dev] は推奨 6 枚）
- ComfyUI 公式テンプレートに 9B / 4B とも Image Edit（base・蒸留）が用意されている
- 結論: ベンチマークの i2i 問題用紙の対象。スキルも t2i と i2i の両方を持つ

## プロンプトの公式ガイダンス（FLUX ファミリー共通、FLUX.2 に適用）

- **自然文**。「キーワードの羅列ではなく、要素の関係と視覚的方向が伝わる文」。英語が最も正確（学習データの大半が英語）
- **構造 > 長さ**。「最長のプロンプトを書くことが目的ではなく、明確な構造を与えること」。テンプレート: `[SUBJECT], [LOCATION], [STYLE], [CAMERA SETTINGS], [LIGHTING], [COLORS], [EFFECT], [ADDITIONAL ELEMENTS]`（厳密な公式ではなく出発点。全枠を埋める必要はない）
- **順序**: 画像の種類 → 主題（具体的に）→ 場所 → 画風 → カメラ設定 → 光 → 色 → 効果 → 補助要素。「主題と動作から始め、雰囲気・文脈・方向付けは画像を良くするときだけ足す」
- **主題を環境より先に**書く（"Person with strong expression, forest fire background, close-up shot" の順が、環境を先に書くより引きで撮られにくい）
- **長さの目安**: 短 10〜30 語（素早い反復）／中 30〜80 語（日常の大半）／長 80〜300+ 語（多主体の複雑な場面）。「短く始め、画像を変える語だけ足す」
- **具体的な描写は効き、埋め草は害**。"highly detailed" などの品質修飾語の積み重ねを避ける
- **写真表現**: カメラ機種・レンズ・フィルム名を具体的に（"Shot on Fujifilm X-T5, 35mm f/1.4" は "professional photo" より効く）。光は 光源／質／方向／色温度 で写真用語的に書く
- **画風**: 画風名を明示し、末尾に "Style: … Mood: …" の注記を置く書き方も公式例にある。2 つの美学の融合も可
- **文字描画**: 正確な文字列を引用符で囲む／配置を明示（"above the door"）／書体（serif / sans-serif / script / display）と大小の階層を書く／**短く**（長い文字列は崩れる）／文字の指定は前の方に置く／ブランド色は HEX（"'ACME' in color #FF5733"）
- **色**: HEX コードでの色指定を公式が推奨（use case: HEX Color Code Prompting）
- **JSON 構造化プロンプト**: 本番・自動化・多主体の複雑な場面向けに公式が用意（scene / subjects[description, position, action] / style / color_palette / lighting / mood / background / composition / camera）。探索や単純な場面は自然文が良い
- **ネガティブプロンプト**: 公式ガイドに記載なし。蒸留版は guidance 1.0 で CFG が実質効かないため、本プロジェクト共通の肯定形の記述で書く
- モデルカードの限界の注記: 「プロンプト追従はプロンプトの書き方に強く左右される」
- **反復**: 「単純な版から始め、合っている点・違う点を見て、重要な細部を一度に一つ直す」

## 編集（i2i）の公式ガイダンス

- 「何を変え、何を変えないかを明示する」。"Change the shirt color to red" / "Replace the background with a sunset beach" / "Turn this into an oil painting" のように直接の指示で書く
- 保持は明示する: "keep everything else unchanged" / "Change nothing else"
- 曖昧語（"make it better", "improve the lighting", "fix"）は効かない
- 複数参照は **"image 1", "image 2"** と番号で参照し、各画像の役割を述べる（"Use Image 2 as the location. Insert only the ice skates from Image 1"、"Keep the pose, lighting, and overall composition of Image 1 unchanged"）
- 色・素材は HEX で指定可（"Change the cow's white fur to #8bc4bb"）。画像内の文字の変更は要素名と新しい文字列（"Change the text on the neon sign to 'zum Schlappen'"）
- 画風変換は目標の媒体を具体的に（"oil painting with thick, textured brushstrokes"）

## ライセンス

- **9B（蒸留・base とも）: FLUX Non-Commercial License**（旧称 FLUX [dev] Non-Commercial License）。モデルカードは「フィルタか人手のレビューを併用すること」を求める
- **4B（蒸留・base とも）: Apache 2.0**（商用可）
- リポジトリのコード: 公式 README 参照（未検証）

## スキルでの読み替え

- 公式の順序（画像の種類 → 主題 → 場所 → 画風 → カメラ → 光 → 色）と「主題を環境より先に」を無印・軽量版の骨格にする
- 「構造 > 長さ」「埋め草は害」を Qwen・Krea との差として取り込む: 中程度の長さ（30〜80 語）を既定にし、多主体の場面だけ長くする
- 写真は機種・レンズ・フィルム名を手掛かりに、文字は短く・引用符・書体・配置・HEX を明示
- 編集は "image 1 / image 2" と "keep everything else unchanged" の公式語法に合わせる。参照は最大 4 枚
- 蒸留版は guidance 1.0 で CFG が効かないので、ネガティブに頼らず肯定形で書く
- 4B にも同じ指針が適用できる（公式ガイドはファミリー共通、アーキテクチャと編集機能も同じ）。差はライセンスとテキストエンコーダの大きさ
