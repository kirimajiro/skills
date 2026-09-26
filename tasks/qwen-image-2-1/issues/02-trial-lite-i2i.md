# 02 軽量版 i2i の実試行

Type: prototype
Status: open

## 目的

`skills/qwen-image-2-1/SKILL-lite-i2i.md` が 27B 級の汎用 LLM の system prompt として「編集指示プロンプトだけを返す」契約を守り、`<image1>` 形式の参照タグと保持指示が Qwen-Image-2.1 の編集で効くかを確かめる。

## 試行手順（ユーザー）

1. ComfyUI の LLM ノードに 27B 級の汎用 LLM を載せ、`SKILL-lite-i2i.md` の中身をそのまま system prompt に貼る
2. ユーザーメッセージとして次の4件を順に入れ、返ってきたプロンプトをそのまま Qwen-Image-2.1 の編集ワークフローに渡す
   - `change the jacket to a navy blazer`（人物写真1枚。例そのまま。契約の確認）
   - `背景を白いスタジオにして`（人物写真1枚。日本語入力 → 肯定形の置き換え記述）
   - `image1 is the model, image2 is the dress. put the dress on her`（2枚。参照タグとロールの確認）
   - `この子を笑顔にして`（透過 PNG のキャラ画像1枚。透過維持の確認）
3. 各件で見るもの
   - 出力がプロンプトのみか（前置き・見出し・説明・質問が混ざっていないか）
   - 保持指示（顔・ポーズ・背景・構図）が入っているか。複数枚で `<image1>` `<image2>` が正しい順で使われているか
   - 生成画像で、指定した箇所だけが変わり、顔の同一性が保たれているか

## 受け入れ条件

- Given 上記4件の入力、When system prompt を貼った LLM に渡す、Then 4件とも出力がプロンプトのみで、複数枚の件は `<image1>` `<image2>` のタグで参照している
- Given 返ってきたプロンプト、When Qwen-Image-2.1 で編集する、Then 4件中3件以上で指定箇所だけが変わり、顔の同一性が保たれる

## Comments
