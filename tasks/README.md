# board — ストーリーの優先順

進行中ストーリーの優先順だけを書く。チケット番号・「次はこれ」は書かない。

- 「次」の導出: 最上位ストーリー → そのeffortのfrontier（open・unblocked・unclaimedなチケットの番号最小）
- `Status: claimed` のチケットがあれば、frontierより先にそれを再開する
- 更新するのは、ストーリーの開始・完了・優先順の変更があったときだけ

## 進行中（優先順）

1. Qwen-Image-2.1 スキルの軽量版を実試行で確かめる — [qwen-image-2-1](qwen-image-2-1/issues/)
2. Krea 2 Turbo スキルの軽量版を実試行で確かめる — [krea-2-turbo](krea-2-turbo/issues/)（`Story:` なしのチケット）
3. FLUX.2 [klein] 9B スキルの軽量版を実試行で確かめる — [flux-2-klein-9b](flux-2-klein-9b/issues/)（`Story:` なしのチケット）
4. 一対比較を i2i に広げる — [benchmarks](benchmarks/issues/)（`Story: pairwise` のチケット。Krea 2 はネイティブ i2i 非対応のため据え置き）

## 完了・引き渡し済み

- flux-2-klein-9b のスキルを一対比較の結果で見直す — [flux-2-klein-9b](flux-2-klein-9b/issues/)（2026-09-27。v1.1.0 で context 0.00 → 0.70）
- krea-2-turbo のスキルを一対比較の結果で見直す — [krea-2-turbo](krea-2-turbo/issues/)（2026-09-27。v1.1.0 で texture 0.00 → 0.75）
- ベンチマークを qwen-image-2-1・krea-2-turbo・flux-2-klein-9b と基準モデルで一巡させる — [benchmarks](benchmarks/issues/)（2026-09-24。横断比較は `benchmarks/results/README.md`）
