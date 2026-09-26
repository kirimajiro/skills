# gpt-image-2-5 — 基本データ（基準モデル）

確認日: 2026-09-23。出典は `docs/research/2026-09_gpt-image-2-5-api.md`（developers.openai.com のモデルページ・画像生成ガイド・API リファレンス・料金ページの要約）。

| 項目 | 値 |
|------|-----|
| 公式名 | GPT Image 2.5 Sunburst（"Our most capable model for image generation and editing"）。高速版の GPT Image 2.5 Flare は使わない |
| 提供元 | OpenAI（OpenAI Images API） |
| モデル ID | `gpt-image-2.5-sunburst-2026-09-08`（`gpt-image-2.5-sunburst` の既定スナップショットに固定） |
| 経路 | OpenAI Images API（`benchmarks/scripts/run_gptimg.py`。生成スクリプトは非公開、契約は同スクリプトの docstring） |
| スキル | なし（raw のみ流す） |
| ネイティブ i2i | 対応（`v1/images/edits`。参照画像・mask による inpainting）。i2i の問題用紙の対象 |
| 参照画像の上限 | 16 枚（`input_fidelity` を 2.5 が受理するかは未検証） |
| ネイティブ解像度 / 対応比率 | プリセット `1024x1024` / `1536x1024` / `1024x1536` / `auto`。カスタムは両辺 16 の倍数・比率 1:3〜3:1・単辺 3840 px 以下・総画素 655,360〜8,294,400（2560x1440 超は experimental） |
| quality | `low` / `medium` / `high` / `xhigh` / `max` / `auto`（`xhigh` / `max` は 2.5 系のみ。既定 `auto`） |
| RGBA 出力 | 対応（`background: transparent` + `png` / `webp`。2.5 での GA 明言は未確認） |
| seed | なし（API にパラメータがない。再現性はスナップショット固定のみ） |
| 料金 | トークン課金: image output $30/M、text input $5/M。品質 × サイズの公式な枚単価表はなく、実費はレスポンスの `usage` で確認する |
| レート制限 | Tier 1: 100,000 TPM / 5 images per minute |

## 判定シート

- [t2i.md](t2i.md)
- [i2i.md](i2i.md)
