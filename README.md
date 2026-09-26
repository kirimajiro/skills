# kirimajiro-skills

Creative Skills.md Collection — クリエイティブ用AI（画像・動画・音楽・3D）のモデルごとに、適切なプロンプトを組み立てさせる Claude Code / Codex 向けスキル集。

## 目的

日々進化するクリエイティブ用AIに対して、モデルごとの公式仕様・一次情報に基づいたプロンプト指示をスキルとして管理し、プラグインとして配布する。同じファミリーでも生い立ちが違えば有効なプロンプトは変わるため、プラグインはバージョン・派生まで含めたモデル単位で分ける。

## フォルダ構成

```
.claude-plugin/marketplace.json        配布するプラグインの一覧（正）
skills/<plugin-name>/SKILL.md          無印: フロンティアモデルの LLM 向けスキル本体（1プラグイン = 1モデル）
skills/<plugin-name>/SKILL-lite-*.md   軽量版: ComfyUI 等の LLM ノードに貼る system prompt（27B 級 LLM 向け）
skills/<plugin-name>/references/       スキルが実行時に読む参照資料
scripts/make_llm_config.py             軽量版を system prompt にした LLM ノード用 config を生成する
benchmarks/                            モデルの得意不得意を掴む定型プロンプトと判定シート（手順は benchmarks/README.md）
AGENTS.md                              エージェント向け指示書
CONTEXT.md                             用語集
docs/                                  ADR・調査結果・エージェント向け規約（索引は docs/README.md）
tasks/                                 進行管理（board・effort・チケット・lessons）
```

## 導入方法

無印スキル（Claude Code）:

```
/plugin marketplace add kirimajiro/skills
/plugin install <plugin-name>@kirimajiro-skills
```

軽量版（ComfyUI 等の LLM ノード）: `skills/<plugin-name>/SKILL-lite-<mode>.md` の中身を LLM ノードの system prompt にする。ユーザーメッセージに雑な依頼を入れると、最終プロンプトだけが返る。27B 級の汎用 LLM を想定している。

- system prompt を貼れるノードなら、ファイルの中身をそのまま貼る
- system prompt を config ファイルから読むノード（comfyui-llm-session の `LLMSessionChatSimpleNode` 等）なら、`scripts/make_llm_config.py` で `<plugin-name>-<mode>.json` を生成し、ワークフローの `config_path` で切り替える。軽量版を更新したら再実行する

```
python scripts/make_llm_config.py --base <既存の config.json> --out-dir <ComfyUI>/user/llm-configs
```

## スキル一覧

| プラグイン | 対象モデル | 軽量版 |
|-----------|-----------|--------|
| `qwen-image-2-1` | Qwen-Image-2.1（t2i / 編集 / 複数参照 / RGBA） | `t2i`, `i2i` |
| `krea-2-turbo` | Krea 2 Turbo（t2i のみ。8 steps・guidance 0 の蒸留モデル） | `t2i` |
| `flux-2-klein-9b` | FLUX.2 [klein] 9B（t2i / 単一参照編集 / 複数参照 4 枚まで。4 steps・guidance 1 の蒸留モデル。非商用ライセンス） | `t2i`, `i2i` |

## ベンチマーク

`benchmarks/` に、どのモデルにもそのまま渡せる汎用プロンプトの問題用紙（t2i 22件・i2i 6件）と、モデルごとの判定シートを置く。各モデルは汎用プロンプトそのまま（raw）と、そのモデルのスキルで書き直したもの（enhanced）の両方を流し、5軸を 0 / 1 / 2 で人が判定する。生成画像はリポジトリに含めない。手順・ルーブリックは `benchmarks/README.md`。

基準モデル（GPT-Image 2.5）の生成に使う OpenAI Images API のスクリプトはリポジトリ所有者の非公開ツールで、ここには含めない。同じ CLI 契約のスクリプトを用意すれば `benchmarks/scripts/run_gptimg.py` から使える（契約は同スクリプト冒頭の docstring）。判定シート（`benchmarks/results/`）と進行管理（`tasks/`）は作業記録ごと公開している。

## Git運用

- ブランチは `main` のみ。所有者が直接コミットする
- スキル（`SKILL.md`・軽量版）を変えたら同じコミットで marketplace.json の `version` を上げる（semver）
- 生成画像（`benchmarks/_local/`）・`.trash/`・`.env`・`.env.keys` はコミットしない（`.gitignore`）

## ライセンス

MIT（`LICENSE`）。対象モデル自体のライセンス（FLUX.2 [klein] 9B の非商用ライセンス等）はモデル側に従う。
