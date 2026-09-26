# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `tasks/`.

## Conventions

- One effort per directory: `tasks/<slug>/`
- The spec (if any) is `tasks/<slug>/spec.md`
- Issues are one file per ticket at `tasks/<slug>/issues/<NN>-<slug>.md`, numbered from `01` — never a single combined tickets file
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## Work-item hierarchy (epic / story / task)

格納階層は作らず、既存の構造に写像する。

- **エピック** = effort（`tasks/<slug>/` の1ディレクトリ）。全体像はwayfinderのmapが担う
- **ストーリー** = チケット先頭の `Story:` 行。ストーリーは入れ物（サブディレクトリ・親チケット）にしない。特定ストーリーに属さないチケットは `Story:` 行を書かない（=共通）
- **タスク** = チケット1ファイル
- ストーリーが1つのeffortに収まらないほど育ったら、入れ子にせず独立したeffortへ昇格させる（a fresh effort, not a resumption）

## Board

`tasks/README.md` がboard。**進行中ストーリーの優先順だけ**を書く。

- チケット番号・「次はこれ」は書かない。「次」は保存せず、boardの最上位ストーリー → そのeffortのfrontierスキャンで毎回導出する
- `Status: claimed` のチケットは中断中の作業として、frontierより先に再開する
- 更新するのは、ストーリーの開始・完了・優先順の変更があったときだけ

## When a skill says "publish to the issue tracker"

Create a new file under `tasks/<slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `tasks/<effort>/map.md` — the Notes / Decisions-so-far / Fog body.
- **Child ticket**: `tasks/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Story:` line (optional) records the story; a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `tasks/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.

## このリポジトリ固有の読み替え

- `prototype`-type tickets mean **実試行**: the user runs the skill's prompt on the target model and reports what came back. Claude writes the trial procedure (which prompt, which model, what to look at) in the ticket body; the user's report goes under `## Comments`. Feed the result back into the skill (`SKILL.md` / `references/`), not into a log.
- `research`-type tickets are `/research` runs against the target model's official documentation. Save the result to `docs/research/` and link it from the ticket's `## Answer`.
- `Story:` の値はプラグイン名（モデルファミリー）と揃える。1 effort に収まる間は省略してよい。
