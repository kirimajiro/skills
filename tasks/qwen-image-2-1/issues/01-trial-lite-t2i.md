# 01 軽量版 t2i の実試行

Type: prototype
Status: resolved

## 目的

`skills/qwen-image-2-1/SKILL-lite-t2i.md` が 27B 級の汎用 LLM の system prompt として「最終プロンプトだけを返す」契約を守り、出力が Qwen-Image-2.1 で狙いどおりに描けるかを確かめる。

## 試行手順（ユーザー）

1. ComfyUI の LLM ノード（comfyui-llm-session `LLMSessionChatSimpleNode`、Qwen3.8-27B GGUF）で、`config_path` に `scripts/make_llm_config.py` が生成した `qwen-image-2-1-t2i.json` を指す（軽量版が system prompt に入る）。トグル付き WF は `benchmarks/_local/image_qwen_image_2_1_LLM_config-toggle.json`。依頼文は WF の「Image Generation Instructions」の primitive に入れる
2. ユーザーメッセージとして次の4件を順に入れ、返ってきたプロンプトをそのまま Qwen-Image-2.1 の t2i に渡す
   - `coffee cup product shot, leave room for a headline top-left`（例そのまま。契約の確認）
   - `雨の夜の東京の路地、ネオン、傘をさした女性の後ろ姿`（日本語入力 → 英語プロンプト）
   - `sticker of a corgi wearing sunglasses, transparent png`（RGBA ラッパーの確認）
   - `カフェのメニュー看板、"本日のコーヒー ¥500" を大きく`（日本語の表示テキストを引用符内で保持）
3. 各件で見るもの
   - 出力がプロンプトのみか（前置き・見出し・説明・質問が混ざっていないか）
   - 固定要素（数・色・位置・表示テキスト）が落ちていないか
   - 生成画像が依頼と一致するか。RGBA は明背景と暗背景に重ねて透過を確認

## 受け入れ条件

- Given 上記4件の入力、When system prompt を貼った LLM に渡す、Then 4件とも出力がプロンプトのみで、表示テキストの文字列が一致する
- Given 返ってきたプロンプト、When Qwen-Image-2.1 で生成する、Then 4件中3件以上で主題・数・配置が依頼どおりになる

## Comments
- 2026-09-27 Claude: 軽量版の貼り方を config 運用（README 導入方法）に変更。ユーザーが再 export した WF で `config_path` ← Switch（true = t2i）、user message = 見出し + 依頼文のみになっていることを確認。まず軽く 2〜3 件で試す
- 2026-09-27 ユーザー: トグル付き WF（config = `qwen-image-2-1-t2i.json`、Qwen3.8-27B thinking low、KSampler 25 steps / cfg 1、1024x1024）で日本語の依頼 3 件を実行。出力は `ComfyUI/output/Bench/lite-trial/qwen-image-2-1-t2i_0000{1,2,3}.png`（PNG メタデータに依頼と LLM 出力が残る）
  - 「コーヒーカップの商品写真、左上に見出しを入れる余白を空けて」→ 英語プロンプトのみ。カップは右下寄り・左上 2/3 を空ける指示あり。画像はカップがやや中央寄りだが左上は空いている
  - 「カフェのメニュー看板、"本日のコーヒー ¥500" を大きく」→ 引用符内の日本語を保持。LLM が「本日のコーヒー」と「¥500」の 2 行に分けて指定し、画像もその 2 行で字形は崩れず
  - 「サングラスをかけたコーギーのステッカー、透過 PNG」→ RGBA の定型（"This is an RGBA image with transparency … background is transparent"）が入り、画像は RGBA で背景透過
  - 3 件とも前置き・見出し・説明・質問なし（契約どおり）。保存ノードの `filename_prefix` が末尾スラッシュだと上書きされるため `Bench/lite-trial/qwen-image-2-1-t2i` に変更
  - 観察: 出力 1・2 に "The palette combines …" のパレット文が入る。krea / flux では v1.1.0 で禁止した書き方だが、Qwen では一対比較未実施のため未判定
- 2026-09-27 ユーザー: 4 件目「雨の夜の東京の路地、ネオン、傘をさした女性の後ろ姿」を 3:4（896x1184）で実行（`_00004.png`）。プロンプトのみの英語出力。雨・夜・東京の路地・ネオン・傘・後ろ姿の 6 要素は保持。画像も後ろ姿・透明傘・ネオン・濡れた路面で成立
  - 観察: 依頼にない要素として "a single hanging lantern in the upper right"（画像にも出る）、"cobblestone"、"dark coat"、"translucent umbrella" を足している。軽量版の「新しい物を足さない」規則に対しては提灯が逸脱。パレット文（"Cool blue-gray tones dominate…"）も 1〜2 件目と同様に入る

## Answer

- 契約: 4 件とも出力はプロンプトのみ（前置き・見出し・説明・質問なし）。日本語の依頼から英語プロンプトが出て、引用符内の日本語「本日のコーヒー ¥500」は保持（LLM が 2 行に分割）。RGBA の定型は入り、画像も透過。受け入れ条件（4 件とも契約どおり・3 件以上で主題と配置が一致）を満たす
- 貼り方: system prompt は config 運用（`scripts/make_llm_config.py` → `qwen-image-2-1-t2i.json`、`config_path` で切替）。WF は `benchmarks/_local/image_qwen_image_2_1_LLM_config-toggle.json`
- 改善候補（未判定。Qwen で一対比較を回すなら raw-enh で確かめる）: パレット文（1・2・4 件目）と依頼にない小物の追加（4 件目の提灯）。krea / flux の v1.1.0 と同じ規則を Qwen の無印・軽量版にも入れる案

