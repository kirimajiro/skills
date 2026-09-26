# 01 基準モデル GPT-Image 2.5 の基本データを確認する

Type: research
Status: resolved

## 目的

`benchmarks/results/gpt-image-2-5/README.md` の未検証項目（公式名・編集 API の有無と参照枚数・解像度と比率・RGBA）を公式ドキュメントで確認し、出典 URL 付きで埋める。ネイティブ i2i 対応が確認できなければ、基準モデルの i2i 判定シートは使わない。

## 受け入れ条件

- Given 公式ドキュメント、When 各項目を確認する、Then 基本データの表がすべて埋まり、各行に出典 URL がある
- Given ネイティブ i2i 対応の結論、When i2i.md を扱う、Then 対応なら残し、非対応なら `.trash/` に移して README から外す

## Comments

- 2026-09-23: developers.openai.com（モデルページ・画像生成ガイド・API リファレンス・料金・changelog）で確認し、`docs/research/2026-09_gpt-image-2-5-api.md` に要約、`results/gpt-image-2-5/README.md` の表を埋めた。ネイティブ i2i は `v1/images/edits`（参照 16 枚・mask）で対応と確認したので i2i.md は残す。未検証のまま残した項目: 2.5 での `input_fidelity` の受理、透過背景の GA 明言、gpt-image-2 との quality 段階の対応。openai.com のブログ本文と platform.openai.com は取得不可（403）。/research スキルが未導入のため調査ファイルは手書き（同じ書式）

