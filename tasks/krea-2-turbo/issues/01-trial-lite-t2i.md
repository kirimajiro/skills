# 01 軽量版 t2i の実試行

Type: prototype
Status: open

## 目的

`skills/krea-2-turbo/SKILL-lite-t2i.md` が 27B 級の汎用 LLM の system prompt として「最終プロンプトだけを返す」契約を守り、出力が Krea 2 Turbo で狙いどおりに描けるかを確かめる。

## 試行手順（ユーザー）

1. ComfyUI の LLM ノードに 27B 級の汎用 LLM を載せ、`SKILL-lite-t2i.md` の中身をそのまま system prompt に貼る（ワークフロー内蔵の Krea 製 enhancer は使わない）
2. ユーザーメッセージとして次の4件を順に入れ、返ってきたプロンプトをそのまま Krea 2 Turbo（8 steps / cfg 0）に渡す
   - `a cat riding a bicycle, retro cartoon illustration`（例そのまま。契約と画風ヒントの保持）
   - `雨の夜の東京の路地、ネオン、傘をさした女性の後ろ姿`（日本語入力 → 英語プロンプト。指示にない小物を足していないか）
   - `photo of a red fox in tall grass at golden hour`（媒体指定の維持）
   - `カフェのメニュー看板、"本日のコーヒー ¥500" を大きく`（日本語の表示テキストを引用符内で保持）
3. 各件で見るもの
   - 出力がプロンプトのみか（前置き・見出し・箇条書き・質問が混ざっていないか）
   - 依頼にない物・人物・具体的な色や素材を発明していないか
   - 媒体・画風が一つに決まっているか
   - 生成画像が依頼と一致するか。文字は綴りまで

## 受け入れ条件

- Given 上記4件の入力、When system prompt を貼った LLM に渡す、Then 4件とも出力がプロンプトのみで、表示テキストの文字列が一致する
- Given 返ってきたプロンプト、When Krea 2 Turbo で生成する、Then 4件中3件以上で主題・媒体・配置が依頼どおりになる

## Comments
