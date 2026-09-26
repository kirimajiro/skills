# krea-2-turbo — 基本データ

確認日: 2026-09-23。出典は `docs/research/2026-09_krea-2-prompting.md`（公式モデルカード・README・技術レポートの要約）。

| 項目 | 値 |
|------|-----|
| 公式名 | Krea 2 Turbo |
| 提供元 | Krea.ai, Inc.（公開日 2026-06-22） |
| 系譜 | Krea 自社の 12B dense DiT をゼロから学習。テキストエンコーダ Qwen3-VL-4B-Instruct、VAE は Qwen Image VAE。Qwen-Image の重み由来ではない |
| 変種 | Raw（未蒸留・学習用、52 steps / CFG 3.5）と Turbo（TDM 蒸留、8 steps / guidance 0.0 / mu 1.15） |
| スキル | `skills/krea-2-turbo/`（無印・軽量版 t2i） |
| ネイティブ i2i | 非対応（モデルカード・README とも text-to-image のみ。i2i 問題用紙の対象外） |
| 参照画像の上限 | 入力なし（krea.ai のスタイル参照・ムードボードはサービス機能で、公開重みには含まれない） |
| ネイティブ解像度 | 1024〜2048 px（各辺 16 の倍数にパディング） |
| 対応比率 | 任意の幅・高さを指定可（公式に比率一覧はない） |
| RGBA 出力 | 非対応（公式記載なし） |
| ネガティブプロンプト | 効かない（guidance 0）。ワークフローの cfg 1 は CFG 無効と同義 |
| ライセンス | 重みは Krea 2 Community License（商用は opensource@krea.ai。条項詳細は未検証）。コードは Apache 2.0 |
| 公式 prompt enhancer | ComfyUI テンプレート同梱の system instruction（Krea 製）。本ベンチマークでは使わず、このプロジェクトのスキルで enhance する |

## 判定シート

- [t2i.md](t2i.md)
