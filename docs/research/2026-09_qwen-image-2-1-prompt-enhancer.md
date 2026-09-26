# Qwen-Image-2.1 公式 prompt enhancer の規約（軽量版の根拠）

確認日: 2026-09-23。要約であり逐語ではない。数値・構文を転記するときは出典で再確認する。

## 出典

- README（prompt rewriting / RGBA / 参照枚数 / 推論設定）: https://raw.githubusercontent.com/QwenLM/Qwen-Image-2.1/main/README.md
- T2I enhancer の system prompt: https://huggingface.co/Qwen/Qwen-Image-2.1-PE-T2I/raw/main/system_prompt.txt
- I2I enhancer の system prompt: https://huggingface.co/Qwen/Qwen-Image-2.1-PE-I2I/raw/main/system_prompt.txt

## README から

- 公式 enhancer は T2I 用 `Qwen/Qwen-Image-2.1-PE-T2I` と編集用 `Qwen/Qwen-Image-2.1-PE-I2I` の2モデル。出力は `rewritten_prompt` と `wh_ratio` を含む JSON
- RGBA ラッパー: 冒頭 "This is an RGBA image with transparency." 末尾 "The image has alpha channel and the background is transparent."
- 参照画像は最大 10 枚
- 既定ステップ 40、ネイティブ解像度 2048×2048、対応比率 1:1 / 4:3 / 3:4 / 3:2 / 2:3 / 16:9 / 9:16

## T2I enhancer の要点

- 役割は「完成した絵を見て報告する観察者」。現在形・三人称で、指示語（create / ensure）や品質語（masterpiece）を使わない
- 手順: 固定要素と自由要素の分離 → 比率決定（`wh_ratio` にのみ書く）→ 媒体・主題・色を含む冒頭文 → 要素の棚卸し → 領域ごとの描写（位置語を多用）→ 表示テキストは straight double quotes で逐語 → 光源の一文 → 全体の締めの一文
- 記述は常に英語。画像内テキストは元の文字体系を保つ。色・素材は修飾語付き（deep navy / brushed metal）。数は列挙し「several」を避ける
- 長さの目安は約 20 文・400〜500 語。出力は単一行の JSON

## I2I enhancer の要点

- 名指しした属性だけを明確に変え、それ以外は入力の忠実度で保つ。保持対象は外観を再描写せず「種類・位置・役割」で指し、包括的な保持句で締める
- 顔の同一性・身につけた物・製品の意匠・描画媒体は明示されない限り不変
- 曖昧さは最も妥当な読みに決めて断定する。頼まれていない修正はしない
- 複数入力は `<image1>` `<image2>` 形式が必須。どれがキャンバスで、各画像から何を取るかを明示する
- 出力は `rewritten_prompt` / `wh_ratio` / `ratio_follow` の JSON。比率はプロンプト本文に書かない

## 軽量版での読み替え

- ComfyUI の LLM ノードでは出力をそのままテキストエンコーダに渡すため、JSON ではなくプロンプト本文のみを返す契約にした。比率・サイズはワークフロー設定に委ね、プロンプトに含めない点は公式と同じ
- 公式 enhancer の観察者視点・逐語の表示テキスト・`<image1>` タグ・保持句の書き方を取り込み、このプロジェクトの「肯定形の記述」を上乗せした
