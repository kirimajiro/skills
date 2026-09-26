# GPT-Image 2.5（Sunburst / Flare）の公式情報（基準モデルの基本データの根拠）

確認日: 2026-09-23。要約であり逐語ではない。数値・構文を転記するときは出典で再確認する。openai.com のブログ本文と platform.openai.com は取得できなかったため、出典は developers.openai.com に限る。

## 出典

- モデル一覧: https://developers.openai.com/api/docs/models
- モデルページ（Sunburst）: https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst
- モデルページ（Flare）: https://developers.openai.com/api/docs/models/gpt-image-2.5-flare
- モデルページ（GPT Image 2）: https://developers.openai.com/api/docs/models/gpt-image-2
- 画像生成ガイド: https://developers.openai.com/api/docs/guides/image-generation
- 画像プロンプトガイド: https://developers.openai.com/api/docs/guides/image-prompting
- API リファレンス（generate）: https://developers.openai.com/api/reference/python/resources/images/methods/generate
- API リファレンス（edit）: https://developers.openai.com/api/reference/python/resources/images/methods/edit
- 料金: https://developers.openai.com/api/docs/pricing
- コスト計算機: https://developers.openai.com/api/docs/guides/image-cost-calculator
- 変更履歴: https://developers.openai.com/api/docs/changelog

## 名称とモデル ID

- 公式名は GPT Image 2.5 Sunburst / GPT Image 2.5 Flare。Sunburst は "Our most capable model for image generation and editing."、Flare は速度最適化の小型モデル（"image quality comparable to GPT Image 2"）。Sunburst は "higher image quality than GPT Image 2"
- API ID: `gpt-image-2.5-sunburst`（既定スナップショット `gpt-image-2.5-sunburst-2026-09-08`）、`gpt-image-2.5-flare`（`gpt-image-2.5-flare-2026-09-08`）。従来モデルは `gpt-image-2`（`gpt-image-2-2026-04-21`）
- ガイドの使い分け: "Choose Sunburst for workflows where editing precision matters most, and Flare for fast, high-quality everyday image generation."
- Images API の `model` の既定値は 2.5 ではない（edit のリファレンスでは `gpt-image-1.5`）。ベンチマークでは `--model` を明示する

## エンドポイントと編集（ネイティブ i2i）

- 両 2.5 モデルとも `v1/images/generations` と `v1/images/edits` に対応。Batch API は `gpt-image-2` のみ
- edit の `image` は "You can provide up to 16 images."。`mask` は PNG 4MB 未満で、複数画像のときは最初の画像に適用（inpainting）
- `input_fidelity`: リファレンスは "`gpt-image-2` and `gpt-image-2-2026-04-21` ignore this parameter." とのみ書く。2.5 が受理するかは未検証（ガイド本文に記述なし）

## size

- プリセット: `1024x1024` / `1536x1024` / `1024x1536` / `auto`
- カスタム `WIDTHxHEIGHT`: "Width and height must be multiples of 16, the aspect ratio must be between 1:3 and 3:1, and neither edge may exceed 3840 pixels. The total pixel count must be between 655,360 and 8,294,400 (4K). Resolutions above `2560x1440` are experimental."
- ベンチマークで使うカスタム値の検算（公式の個別例示ではなく規則への照合）: `864x1152`（3:4、995,328 px）と `1344x752`（約 16:9、1,010,688 px）は規則を満たす

## quality・背景・moderation・seed

- quality: `low` / `medium` / `high` / `xhigh` / `max` / `auto`。`xhigh` と `max` は 2.5 系で追加。既定は `auto`。gpt-image-2 の段階との対応表は公式にない（"Use xhigh or max only when they improve an unmet quality requirement within your latency budget."）
- 透過背景: `background: "transparent"` と `output_format` `png` / `webp`。jpeg 不可。2.5 での GA 明言は見つからず（gpt-image-2 は 2026-08-20 に preview）
- moderation: `auto`（既定）/ `low`
- seed: generate / edit のパラメータ一覧に存在しない（再現性はスナップショット固定のみ）

## 料金とレート制限

- トークン単価（2.5 両モデルと gpt-image-2 で同じ。"Token rates match GPT Image 2."）: text input $5.00/M（cached $1.25）、image input $8.00/M（cached $2.00）、image output $30.00/M
- 品質 × サイズの枚単価の公式表はない。コスト計算機は "The GPT Image 2 calculator does not estimate GPT Image 2.5 token consumption." のため 2.5 には使えない。実費はレスポンスの `usage.output_tokens`（`output_tokens_details.image_tokens`）で確認する
- レート制限（2.5 両モデル同一）: Tier 1 は 100,000 TPM / 5 images per minute、Tier 2 は 250,000 / 20、Tier 3 は 800,000 / 50
