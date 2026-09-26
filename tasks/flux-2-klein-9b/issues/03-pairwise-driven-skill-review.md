# 03 一対比較の結果からスキルの補完と描写語の書き方を見直す

Type: research
Story: skill-review
Status: resolved

## 背景

一対比較（`benchmarks/results/flux-2-klein-9b/t2i.md`、2026-09-26）で、enhanced が raw より下がった観点が出た。判定者の雑感は「想像力が豊かで自然なスタイルや構図が出ることがあるが、指示文に無いので出したもの自体が破綻しているケースが多い」。

## 目的

enhance が下げた観点を、FLUX.2 [klein] の公式プロンプトガイド（`docs/research/`）と enhanced プロンプトの実文を照らして原因を切り分け、`skills/flux-2-klein-9b/SKILL.md`（と軽量版）の書き方を直す。

## 対象

- context（−0.19）: t2i-02, 03, 04, 05, 17 — enhance で足した場面の要素（小物・人物・天候）が破綻する。足す要素を減らし、指示にある要素の描写に絞る
- detail（−0.25）: t2i-03, 07, 11 — raw のほうがグランジ・機構の書き込みが自然
- skin（−0.25）: t2i-02, 09 — クローズアップの肌。カメラ設定語（レンズ・f 値）の扱い
- organic: t2i-13 — 樹木・地形が enhanced で単調
- anatomy: t2i-16 anime, 23 — enhanced でポーズと手指が崩れる

## 手順

1. 対象の enhanced プロンプトと raw を並べ、enhanced だけにある語（足した要素・描写語・カメラ設定語）を観点ごとに列挙する
2. 公式ガイドで推奨・非推奨の書き方を確認し（/research。既存の `docs/research/` にあれば再調査しない）、疑わしい語の扱いを決める
3. SKILL.md の該当節を直し、軽量版に反映する。marketplace.json の version を上げる
4. 直したスキルで対象の問題用紙だけ enhanced を作り直し、`raw-enh` の `--only` セッションで再判定する（実試行）

## 受け入れ条件

- Given 修正後のスキルで作った enhanced、When `--mode raw-enh --only 02,03,04,05,17` を判定する、Then context の勝率が 0.5 以上になる
- Given 修正内容、When SKILL.md を読む、Then 変更の理由（why）は本文から読み取れるか ADR にある

## Comments
- 2026-09-27 Claude: 手順 1〜3 完了
  - 分析: enhanced だけにある要素は (a) 依頼にない小物・服・色・設定の発明（02・04・05・07・11・13・16・17）、(b) overcast / soft even / diffused の既定化（02・04・09・13・16）、(c) パレット文・仕上げ語（02・03・11・13）、(d) レンズ・絞りの数値（02・04・09・11・13・17）、(e) 依頼にない構図の固定（04・05・16）。判定者の雑感「指示文に無いので出したもの自体が破綻」と (a) が一致。方向のある光を書いた 01・10・17・19・20 では enhanced が勝ち、diffused の 13 で負け
  - 修正（SKILL.md / SKILL-lite-t2i.md、marketplace.json v1.1.0）: 過剰指定を避ける規則を追加（服・小物・色・構図・姿勢の発明禁止。密度は既にある表面の状態・光・動作で出す）／色は物の色・質感は素材の状態としパレット文と仕上げ語を禁止（HEX はブランド色・ポスターに限る）／光は光源・方向・硬さとその結果で書き overcast / diffused を既定にしない／漁師の例文と軽量版のコーヒー例を書き換え。レンズ数値はユーザー判断で公式どおり維持
  - 再判定の準備: 02・03・04・05・07・09・11・13・16 anime・17 の enhanced を v1.1.0 で書き直し判定シートに反映。旧 enhanced 画像 10 枚は `.trash/flux-2-klein-9b-enhanced-v1.0.0/` へ
- 実試行（ユーザー）:
  1. ComfyUI を起動し、`python benchmarks/scripts/run_t2i.py --model flux-2-klein-9b --api-json benchmarks/_local/image_flux2_text_to_image_9b.json --only 02,03,04,05,07,09,11,13,16,17 --variants enhanced`（既存の 16 photo / oil / flat は飛ばされる）
  2. Claude が `pairwise_build.py --mode raw-enh --a flux-2-klein-9b --only 02,03,04,05,07,09,11,13,16,17` で HTML を作る。判定して JSON を `_local/pairwise/` に置く
  3. `pairwise_report.py` で context の勝率を見る（受け入れ条件: 0.5 以上）
- 2026-09-27 ユーザー: 再判定（`raw-enh_flux-2-klein-9b_20260927-0041`、13 問題・41 設問）。「この比較ではっきり差が分かりました」。雑感: 「どうしても脂っこい感じの絵作りになる傾向がある。enh してもしなくても、破綻しやすいのが難点。色々描き込みたい場合には使えるモデルかもしれないが、Krea 2 と比較して積極的に画質面で Flux.2 [klein] を使う理由は特にないと思う」

## Answer

- 原因: enhance が依頼にない服・小物・色・構図を発明し、その要素が破綻していた。加えて overcast / diffused の既定化とパレット文・仕上げ語が質感と光を平板にしていた
- 修正: SKILL.md / SKILL-lite-t2i.md v1.1.0（過剰指定を避ける規則、色と質感は物理的事実、光は光源と硬さとその結果）。レンズ数値は公式どおり維持
- 結果（同じ 10 枚、v1.0.0 → v1.1.0 の enhanced 勝率）: context 0.00 → 0.70（0/0/5 → 3/1/1）、detail 0.00 → 0.83、skin 0.17 → 0.67、style 0.50 → 0.75。受け入れ条件（context 0.5 以上）を満たす
- 残り: 05（text・context）、07（anatomy・composition）、09（skin・texture）で enhanced が負ける。09 はレンズ・絞りの数値を残した肌のクローズアップで、2 回とも負け。次に見直すならここ（ユーザー判断で今回は維持）

