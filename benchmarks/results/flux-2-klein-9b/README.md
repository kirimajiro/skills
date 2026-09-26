# flux-2-klein-9b — 基本データ

確認日: 2026-09-23。出典は `docs/research/2026-09_flux-2-klein-prompting.md`（BFL 公式ブログ・モデルカード・README・プロンプトガイド・ComfyUI 公式チュートリアルの要約）。

| 項目 | 値 |
|------|-----|
| 公式名 | FLUX.2 [klein] 9B（蒸留版。ワークフローの `flux-2-klein-9b-fp8.safetensors` は ComfyUI 公式配布の蒸留版と一致） |
| 提供元 | Black Forest Labs（公開日 2026-01-15） |
| 系譜 | FLUX.2 ファミリーの小型モデル。9B rectified flow transformer + Qwen3-8B テキストエンコーダ（`qwen_3_8b_fp8mixed`）。step・guidance 蒸留で 4 steps。蒸留元の FLUX.2 変種は公式に明記なし（未検証） |
| 変種 | 4B 蒸留 / 4B base / 9B 蒸留 / 9B base。base は蒸留なしで 50 steps / guidance 4.0、出力の多様性が高い |
| スキル | `skills/flux-2-klein-9b/`（無印・軽量版 t2i / i2i） |
| ネイティブ i2i | 対応（t2i・単一参照編集・複数参照生成を同じ重みで。i2i 問題用紙の対象）。ComfyUI 公式に 9B 用 Image Edit テンプレートあり |
| 参照画像の上限 | 4 枚（BFL 公式プロンプトガイド） |
| ネイティブ解像度 | 公式例は 1024×1024。対応比率の一覧は公式になし（未検証）。ComfyUI テンプレートは約 1MP |
| RGBA 出力 | 非対応（公式記載なし） |
| ネガティブプロンプト | 蒸留版は guidance 1.0 が公式推奨で CFG が実質効かない。公式プロンプトガイドにネガティブの記載なし |
| 公式推奨設定 | 蒸留版 4 steps / guidance 1.0。base 50 steps / guidance 4.0 |
| ワークフローの設定 | Flux2Scheduler **8 steps** / CFGGuider **cfg 1** / euler。公式推奨は 4 steps / guidance 1.0 だが、4 steps では破綻が多く 8 steps の方が安定するため（2026-09-23、問題用紙 02 で 4 / 8 / 20 steps を比較）8 steps を既定にした。cfg は公式どおり 1 |
| VAE | ワークフローは `full_encoder_small_decoder.safetensors`。ComfyUI 公式一覧は `flux2-vae.safetensors`（軽量デコーダ版と推定。未検証） |
| ライセンス | 9B は FLUX Non-Commercial License（フィルタか人手レビューの併用を要求）。4B は Apache 2.0 |
| 公式 prompt enhancer | FLUX.2 [dev] 向けに Mistral-Small による prompt upsampling が README にある。klein 向けの記載はなく、本ベンチマークではこのプロジェクトのスキルで enhance する |

## 判定シート

- [t2i.md](t2i.md)
- [i2i.md](i2i.md)
