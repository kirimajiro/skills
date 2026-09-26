# qwen-image-2-1 — 基本データ

確認日: 2026-09-23。出典は `docs/research/2026-09_qwen-image-2-1-prompt-enhancer.md`（公式 README の要約）。

| 項目 | 値 |
|------|-----|
| 公式名 | Qwen-Image-2.1 |
| 提供元 | Alibaba Qwen |
| スキル | `skills/qwen-image-2-1/`（無印・軽量版 t2i / i2i） |
| ネイティブ i2i | 対応（単一画像編集・複数参照。i2i 問題用紙の対象） |
| 参照画像の上限 | 10 枚 |
| ネイティブ解像度 | 2048×2048 |
| 対応比率 | 1:1 / 4:3 / 3:4 / 3:2 / 2:3 / 16:9 / 9:16 |
| RGBA 出力 | 対応（公式ラッパー文あり） |
| 既定ステップ | 40 |
| 公式 prompt enhancer | Qwen-Image-2.1-PE-T2I / PE-I2I（本ベンチマークでは使わず、このプロジェクトのスキルで enhance する） |

## 判定シート

- [t2i.md](t2i.md)
- [i2i.md](i2i.md)
