# docs — ドキュメントインデックス

このリポジトリの資料の索引。資料種別ごとの更新ルールと命名規則もここに置く。何をどこに書くかは AGENTS.md の「記録の行き先」に従う。

## 索引

| 資料 | 内容 |
|------|------|
| `../README.md` | プロジェクト概要・フォルダ構成・導入方法・Git運用 |
| `../CONTEXT.md` | ドメイン用語集（用語の正） |
| `../.claude-plugin/marketplace.json` | 配布するプラグインの一覧（正） |
| `../skills/<plugin-name>/` | 無印スキル（`SKILL.md`）・軽量版（`SKILL-lite-<mode>.md`）・実行時の参照資料（`references/`） |
| `../benchmarks/` | ベンチマーク: 問題用紙（`t2i/` `i2i/`）・参照画像（`refs/`）・モデル別の基本データと判定シート（`results/`）。手順・一対比較・観点セットは `../benchmarks/README.md`、モデル横断の比較は `../benchmarks/results/README.md` |
| `adr/` | 非自明な判断の記録（ADR）。運用は `adr/README.md` |
| `research/` | /research の調査結果（対象モデルの公式仕様・ガイド） |
| `agents/` | エージェント向け規約（issue-tracker / triage-labels / domain） |
| `../tasks/` | 進行管理: board（`tasks/README.md`）・effort の map・チケット・lessons |

## 資料種別の更新ルール

- **SKILL.md・README**: 常に最新の状態だけを書く。旧記述・取り消し線・変更履歴の節を本文に残さない。経緯は git と marketplace.json の version が担う
- **調査結果**: 対象モデルの公式ドキュメント等の一次情報に限り、出典 URL と確認日を残す。仕様が変わったら同じファイルを書き換え、古い版を残さない
- **ADR**: 決定を覆すときは旧 ADR を書き換えず新しい ADR を起こし、旧 ADR のステータスを「廃止（superseded by NNNN）」にする
- **用語集**: 新しい用語が生まれたら `CONTEXT.md` に定義してから使う。同義語に流れない
- **marketplace.json**: `description` は SKILL.md の description を写す。スキルを変えたら `version` を上げる
- **問題用紙**: 汎用プロンプトを変えると既存の判定が無効になる。`id` は変えず、判定シートの該当行を消す。参照画像も一度固定したら差し替えない
- **判定シート**: 判定は日付・判定者・ワークフロー設定・セッション ID とともに残す。t2i は雛形 `../benchmarks/results/TEMPLATE-t2i.md` に従い、Enhanced prompts の節は `run_t2i.py` が読むので形を変えない。基準モデルを変えたら冒頭の基準モデル名を更新し、古い判定は基準名付きで残す

## 命名規則

| 種別 | 規則 | 例 |
|------|------|-----|
| プラグイン / スキル | `../skills/<plugin-name>/`（モデルを一意に特定する英小文字ハイフン区切り。バージョン・派生を含む） | `../skills/qwen-image-2-1/SKILL.md` |
| 軽量版 | `../skills/<plugin-name>/SKILL-lite-<mode>.md`（mode は `t2i` / `i2i` 等の操作単位） | `../skills/qwen-image-2-1/SKILL-lite-t2i.md` |
| ADR | `adr/NNNN-<slug>.md`（連番 4 桁 + 英小文字ハイフン区切り） | `adr/0001-one-plugin-per-model-including-version.md` |
| 調査結果 | `research/YYYY-MM_<topic-slug>.md` | `research/2026-09_qwen-image-2-1-prompt-enhancer.md` |
| チケット | `../tasks/<effort>/issues/<NN>-<slug>.md`（`01` から連番） | `../tasks/qwen-image-2-1/issues/01-trial-lite-t2i.md` |
| 問題用紙 | `../benchmarks/<mode>/<NN>-<slug>.md`（`id` は `<mode>-<NN>`。変えない） | `../benchmarks/t2i/05-text-en-cafe-sign.md` |
| 判定シート | `../benchmarks/results/<model-slug>/<mode>.md`。基本データは同フォルダの `README.md` | `../benchmarks/results/qwen-image-2-1/t2i.md` |
| 生成画像（ローカル） | `../benchmarks/_local/<model-slug>/<mode>/<NN>-<slug>-<variant>_<seed 5桁>.png`（1階層にフラット。連番 = seed） | `../benchmarks/_local/qwen-image-2-1/t2i/01-short-rainy-alley-enhanced_00003.png` |
