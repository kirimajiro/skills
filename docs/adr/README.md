# ADR — 非自明な判断の記録

一行の注記に収まらない非自明な判断を記録する。対象例: プラグイン分割の粒度、スキルの命名・description の方針、対象モデルの選定・除外、references への切り出し基準。

## 命名

`NNNN-<slug>.md`（連番4桁 + 英小文字ハイフン区切り）。例: `0001-one-plugin-per-model-family.md`

## 書式

- 冒頭にタイトル / ステータス（提案・採用・廃止）/ 日付
- 本文は 背景（Context）→ 決定（Decision）→ 影響（Consequences）
- 決定を覆すときは旧ADRを書き換えず、新しいADRを起こし、旧ADRのステータスを「廃止（superseded by NNNN）」にする
