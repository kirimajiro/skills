# 02 一対比較の結果からスキルの質感・光の書き方を見直す

Type: research
Story: skill-review
Status: resolved

## 背景

一対比較（`benchmarks/results/krea-2-turbo/t2i.md`、2026-09-24）で、enhanced が raw より下がった観点が出た。判定者の所感は「enhance は質感を CG 寄りにしている」「場面の補完には効いている」「Krea のスキルはもっと改善の余地がある」。

## 目的

enhance が下げた観点を、Krea 2 Turbo の公式プロンプトガイド（`docs/research/`）と enhanced プロンプトの実文を照らして原因を切り分け、`skills/krea-2-turbo/SKILL.md`（と軽量版）の書き方を直す。

## 対象

- texture（−0.18）: t2i-01, 02, 09, 16 photograph, 20 — enhanced のほうが 3D・CG 寄りに見える。素材・光の描写語（"glossy", "mirrors", パレット指定など）が原因か
- light（−0.09）: t2i-09, 10, 13, 23 — 反射・逆光・空気感が平板になる
- skin: t2i-09 — 「中年」の指定が 60 代に寄る
- layout: t2i-21 — 指示するほど単調になる
- text: t2i-23 — enhanced で文字が崩れる／指定外の文字が増える

## 手順

1. 上記の enhanced プロンプト（判定シートの Enhanced prompts）と raw を並べ、enhanced だけにある語を観点ごとに列挙する
2. 公式ガイドで推奨・非推奨の書き方を確認し（/research。既存の `docs/research/` にあれば再調査しない）、疑わしい語の扱いを決める
3. SKILL.md の該当節を直し、軽量版に反映する。marketplace.json の version を上げる
4. 直したスキルで対象の問題用紙だけ enhanced を作り直し、`raw-enh` の `--only` セッションで再判定する（実試行）

## 受け入れ条件

- Given 修正後のスキルで作った enhanced、When `--mode raw-enh --only 01,02,09,16,20` を判定する、Then texture の勝率が 0.5 以上になる
- Given 修正内容、When SKILL.md を読む、Then 変更の理由（why）は本文から読み取れるか ADR にある

## Comments
- 2026-09-26 Claude: 手順 1〜3 完了
  - 分析: enhanced だけにある要素は (a) パレット文（01・02・10・16・21）、(b) 艶・仕上げ語（01・02・09・20）、(c) soft/even/overcast の既定化（02・09・13・16・20・21）、(d) 依頼にない姿勢・視線・年齢の手がかり（02・09・16）、(e) 構造化入力の 1 段落化（23）。判定者の備考（3D 感・光が平板・60 歳代に見える）と一致。公式ガイドはパレット指定・仕上げ語を勧めていない（`docs/research/2026-09_krea-2-prompting.md`）
  - 修正（SKILL.md / SKILL-lite-t2i.md、marketplace.json v1.1.0）: 色は物の色・質感は素材の状態として書きパレット文と仕上げ語を禁止（ポスター・フラットの限定パレットは例外）／光は光源・方向・硬さとその結果で書き soft/even を既定にしない／過剰指定の例に姿勢・視線・年齢を追加／詳細な入力は段落と見出しを保つ／漁師の例文と軽量版の例 2 件を書き換え。ポスター（21 layout）はユーザー判断で対象外
  - 再判定の準備: 01・02・09・10・13・16 photograph・20・23 の enhanced を v1.1.0 で書き直し判定シートに反映。旧 enhanced 画像 8 枚は `.trash/krea-2-turbo-enhanced-v1.0.0/` へ
- 実試行（ユーザー）:
  1. ComfyUI を起動し、`python benchmarks/scripts/run_t2i.py --model krea-2-turbo --api-json benchmarks/_local/image_krea2_turbo_t2i.json --only 01,02,09,10,13,16,20,23 --variants enhanced`（既存の 16 anime / oil / flat は飛ばされる）
  2. `python benchmarks/scripts/pairwise_build.py --mode raw-enh --a krea-2-turbo --only 01,02,09,10,13,16,20,23` で HTML を作り、判定して JSON を `_local/pairwise/` に置く
  3. `python benchmarks/scripts/pairwise_report.py benchmarks/_local/pairwise/raw-enh_krea-2-turbo_<新しい日時>.json --out ...` で texture・light の勝率を見る（受け入れ条件: texture 0.5 以上）
- 2026-09-27 ユーザー: 再判定（`raw-enh_krea-2-turbo_20260927-0023`、11 問題・38 設問）。雑感: 「前のよりも自然に出ている様に感じます。enh が劣っているということは無いと思います」（変更していない 16 anime / oil / flat の評価差は無視）

## Answer

- 原因: enhance が足していたパレット文・艶や仕上げ語・soft/even の既定・依頼にない姿勢や年齢の手がかりが、質感を均一で CG 寄りにし光を平板にしていた。公式ガイドはこれらを勧めていない
- 修正: SKILL.md / SKILL-lite-t2i.md v1.1.0（色は物の色、質感は素材の状態、光は光源と硬さとその結果、過剰指定の例を拡張、詳細入力は段落を保つ）
- 結果（同じ 8 枚、v1.0.0 → v1.1.0 の enhanced 勝率）: texture 0.00 → 0.75（0/0/5 → 4/4/0）、light 0.17 → 0.58、skin 0.25 → 1.00、context 0.50 → 0.83。受け入れ条件（texture 0.5 以上）を満たす
- 残り: 16 photograph は style・anatomy で enhanced が負け（n=1）、23 は light で負け（n=1）。判定シートのスキル改善候補に残す。ポスター（21）は対象外

