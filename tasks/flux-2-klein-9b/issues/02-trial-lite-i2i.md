# 02 軽量版 i2i の実試行

Type: prototype
Status: open

## 目的

`skills/flux-2-klein-9b/SKILL-lite-i2i.md` が 27B 級の汎用 LLM の system prompt として「編集指示プロンプトだけを返す」契約を守り、"image 1 / image 2" の参照と保持句が FLUX.2 [klein] 9B の編集で効くかを確かめる。

## 試行手順（ユーザー）

1. ComfyUI 公式の FLUX.2 Klein 9B Image Edit（蒸留）テンプレートを開き、LLM ノードに 27B 級の汎用 LLM を載せて `SKILL-lite-i2i.md` を system prompt に貼る
2. ユーザーメッセージとして次の4件を順に入れ、返ってきたプロンプトをそのまま編集ワークフローに渡す
   - `change the jacket to a navy blazer`（人物写真1枚。例そのまま）
   - `背景を白いスタジオにして`（人物写真1枚。肯定形の置き換え記述）
   - `image 1 is the model, image 2 is the dress. put the dress on her`（2枚。参照番号とロール）
   - `この子を笑顔にして`（キャラ画像1枚。保持句）
3. 各件で見るもの
   - 出力がプロンプトのみか
   - 変更と保持句（keep … unchanged）の両方があるか。複数枚で "image 1" "image 2" が正しい順で使われているか
   - 生成画像で、指定した箇所だけが変わり、顔の同一性が保たれているか

## 受け入れ条件

- Given 上記4件の入力、When system prompt を貼った LLM に渡す、Then 4件とも出力がプロンプトのみで、複数枚の件は "image 1" "image 2" で参照している
- Given 返ってきたプロンプト、When FLUX.2 [klein] 9B で編集する、Then 4件中3件以上で指定箇所だけが変わり、顔の同一性が保たれる

## Comments
