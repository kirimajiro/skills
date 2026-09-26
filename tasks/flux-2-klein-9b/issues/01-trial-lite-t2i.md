# 01 軽量版 t2i の実試行

Type: prototype
Status: open

## 目的

`skills/flux-2-klein-9b/SKILL-lite-t2i.md` が 27B 級の汎用 LLM の system prompt として「最終プロンプトだけを返す」契約を守り、出力が FLUX.2 [klein] 9B で狙いどおりに描けるかを確かめる。

## 試行手順（ユーザー）

1. ComfyUI の LLM ノードに 27B 級の汎用 LLM を載せ、`SKILL-lite-t2i.md` の中身をそのまま system prompt に貼る
2. ユーザーメッセージとして次の4件を順に入れ、返ってきたプロンプトをそのまま FLUX.2 [klein] 9B に渡す
   - `coffee cup product shot, leave room for a headline top-left`（例そのまま。契約の確認）
   - `雨の夜の東京の路地、ネオン、傘をさした女性の後ろ姿`（日本語入力 → 英語プロンプト。主題が環境より先に来ているか）
   - `photo of a red fox in tall grass at golden hour`（媒体指定の維持とカメラ語彙）
   - `カフェのメニュー看板、"本日のコーヒー ¥500" を大きく`（日本語の表示テキストを引用符内で保持し、短く前に置いているか）
3. 各件で見るもの
   - 出力がプロンプトのみか（前置き・見出し・箇条書き・質問が混ざっていないか）
   - 30〜80 語程度に収まり、品質修飾語の積み重ねがないか
   - 依頼にない物・人物を発明していないか
   - 生成画像が依頼と一致するか。文字は綴りまで

## 受け入れ条件

- Given 上記4件の入力、When system prompt を貼った LLM に渡す、Then 4件とも出力がプロンプトのみで、表示テキストの文字列が一致する
- Given 返ってきたプロンプト、When FLUX.2 [klein] 9B で生成する、Then 4件中3件以上で主題・媒体・配置が依頼どおりになる

## Comments
