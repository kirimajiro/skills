# refs — i2i 用の固定参照画像

i2i の問題用紙が使う参照画像。全員が同じ画像で試せるように、少数に限ってリポジトリに置く（生成画像をローカルに置く原則の例外）。実在の人物ではなく、以下の仕様で自前生成した架空の人物・物品に限る。

## 生成手順

1. 基準モデル（GPT-Image 2.5）で各仕様のプロンプトを流し、仕様に最も合う 1 枚を選ぶ
2. 長辺 1024px の PNG にして `refs/<id>.png` として保存する
3. 一度固定したら差し替えない。差し替えるときは i2i の既存判定を無効にし、判定シートの該当行を消す

## 生成記録

- 生成日: 2026-09-24。基準モデル `gpt-image-2.5-sunburst-2026-09-08`、quality high、size 768x1024、プロンプトは下記仕様を逐語（`benchmarks/scripts/run_gptimg.py --refs 4` で各 4 枚を生成し、ユーザーが 1 枚ずつ選定）
- 選定の目安: ref-01 は平均的な体型で上下の余白が均等、ref-02 はコートの両端に縫い目があり転写の目印になる、ref-03 は髪型に特徴があり、スツールは真正面で形状を推論しにくく、下側のつま先が浮いていてポーズ転写の目印になる
- ref-04 は 2026-09-24 に同じ条件で 4 枚生成して選定（cand 3）。下半身の向きが分かりやすく、顔が斜め前を向いて表情が見え、足と手の指がはっきり見えるため
- ref-05 は 2026-09-24 に同じ条件で 4 枚生成して選定（cand 4）。左端の自転車と右端の椅子が切れており、日除けの文字と店内の奥行きで延長の連続性を見やすい

## 仕様

### ref-01

- 役割: 人物A（基準となる全身の人物写真。i2i の image1）
- 比率: 3:4
- ファイル: `refs/ref-01.png`

```text
A full-body photograph of a young adult woman with shoulder-length black hair, wearing a plain white t-shirt, blue jeans, and white sneakers, standing straight facing the camera with arms relaxed at her sides and a neutral friendly expression, on a plain light-gray studio background with soft even lighting.
```

### ref-02

- 役割: 衣服（転写元のコート。i2i-02 の image2）
- 比率: 3:4
- ファイル: `refs/ref-02.png`

```text
A product photograph of a mustard-yellow wool overcoat with large dark buttons on a wooden hanger, hanging against a plain white background, front view, soft even lighting.
```

### ref-03

- 役割: 人物B（ポーズの転写元。i2i-04 の image2）
- 比率: 3:4
- ファイル: `refs/ref-03.png`

```text
A full-body photograph of a middle-aged man with short gray hair, wearing a dark green sweater and gray trousers, sitting on a wooden stool with legs crossed, one hand raised in a wave and the other resting on his knee, on a plain light-gray studio background with soft even lighting.
```

### ref-04

- 役割: 人物C（難しいポーズの転写元。i2i-07 の image2）
- 比率: 3:4
- ファイル: `refs/ref-04.png`

```text
A full-body photograph of a young adult woman with long blonde hair tied in a ponytail, wearing a dark teal sports top and black leggings, barefoot, performing the yoga dancer pose: standing on her left leg, her right leg bent and raised behind her with her right hand holding the raised foot, her left arm extended straight forward, torso leaning slightly forward, on a plain light-gray studio background with soft even lighting.
```

### ref-05

- 役割: 情景（アウトペイントの元画像。i2i-05 の image1）。無地背景では延長が無意味なので、左右の端で切れた物が続きを要求する構図にする
- 比率: 3:4
- ファイル: `refs/ref-05.png`

```text
A photograph of a young adult man with short brown hair, wearing a gray sweater, sitting at a small round cafe table on a cobblestone street outside a cafe, holding a coffee cup. Behind him, the cafe facade with a striped awning, a large window, and a wooden door. A bicycle leaning against the wall is cut off at the left edge of the frame, and a row of potted plants is cut off at the right edge, so the scene clearly continues beyond both sides. Warm late-afternoon sunlight from the left.
```

