# qwen-image-2-1 — i2i 判定シート

- 基準モデル: GPT-Image 2.5
- 判定日: 2026-09-24
- 判定者: リポジトリ所有者
- ワークフロー設定（steps / guidance / sampler / 解像度）: 

## 集計

| ID | variant | 実行 | 保持 | 転写 | 整合 | 品質 | 備考 |
|----|---------|---|---|---|---|---|------|
| i2i-01 | raw | 2 | 2 | 2 | 2 | 2 |  |
| i2i-01 | enhanced | 2 | 2 | 2 | 2 | 2 | 難易度が低かったせいか遜色ない。QI2.1自体がImage Editに力を入れているのかもしれない |
| i2i-02 | raw | 2 | 2 | 2 | 2 | 2 |  |
| i2i-02 | enhanced | 2 | 2 | 2 | 2 | 2 | 難易度が低かったせいか遜色ない。 |
| i2i-03 | raw | 2 | 2 | 2 | 2 | 2 |  |
| i2i-03 | enhanced | 2 | 2 | 2 | 2 | 2 | 難易度が低かったせいか遜色ない。 |
| i2i-04 | raw | 0 | 0 | 0 | 0 |  | ポーズは移らず、ref-03 の人物を隣に並べた 2 人合成になった |
| i2i-04 | enhanced | 2 | 2 | 2 | 2 | 2 | 難易度が低かったせいか遜色ない。 |
| i2i-05 | raw | 2 | 2 | 2 | 1 | 1 |  |
| i2i-05 | enhanced | 2 | 2 | 2 | 1 | 1 | アウトペイントでもパースの狂いは発生する。パッと見は綺麗。 |
| i2i-06 | raw | 2 | 2 | 2 | 2 | 2 |  |
| i2i-06 | enhanced | 2 | 1 | 2 | 1 | 1 | 首の傾きなどはrawの方が良い |
| i2i-07 | raw | 0 | 1 | 0 | 0 | 1 | 2人になってしまった |
| i2i-07 | enhanced | 2 | 2 | 2 | 2 | 2 | QI2.1の方が基準モデルよりもポーズに忠実 |

## 問題用紙ごとの記録

### i2i-01 実写をアニメイラストに（画風変換）

問題用紙: `../../i2i/01-style-photo-to-anime.md`　画像: `../../_local/qwen-image-2-1/i2i/01-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
Change the rendering style of the input photograph to a 2D anime illustration with clean linework and soft cel shading. Preserve the person's pose, facial features, hairstyle, clothing, and the layout of the background. Simplify the background into painted flat tones consistent with the anime style.
```

備考: enhanced: 難易度が低かったせいか遜色ない。QI2.1自体がImage Editに力を入れているのかもしれない


### i2i-02 画像2の衣服を画像1の人物に着せる（衣服転写）

問題用紙: `../../i2i/02-clothing-transfer.md`　画像: `../../_local/qwen-image-2-1/i2i/02-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
Use <image1> as the base image. Replace the person's outer clothing with the coat from <image2>, preserving its cut, fabric, mustard-yellow color, and large dark buttons. Keep the person's facial identity, hairstyle, body pose, hands, and the original background and framing from <image1>. Adjust the coat's scale, folds, and shading to fit the person's pose and the existing light direction.
```

備考: enhanced: 難易度が低かったせいか遜色ない。


### i2i-03 人物写真からキャラクターシート（三面図）

問題用紙: `../../i2i/03-character-sheet.md`　画像: `../../_local/qwen-image-2-1/i2i/03-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
Create a character sheet of the person in the input image: three full-body views standing side by side in a row on a plain white background, showing the front view on the left, the side view in the middle, and the back view on the right. Preserve the person's facial identity, hairstyle, body proportions, and clothing across all three views. Use even, soft studio lighting and the same scale for each view.
```

備考: enhanced: 難易度が低かったせいか遜色ない。


### i2i-04 画像2のポーズを画像1の人物に（ポーズ転写）

問題用紙: `../../i2i/04-pose-transfer.md`　画像: `../../_local/qwen-image-2-1/i2i/04-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
Use <image1> as the base image and <image2> only as a pose reference. Change the person's pose to match the pose of the person in <image2>: seated on a plain wooden stool with the legs crossed at the knee, the right hand raised beside the head in an open-palm wave, and the left hand resting on the knee, facing the camera with a friendly smile. The image shows exactly one person, the person from <image1>, with the same facial identity, hairstyle, white t-shirt, blue jeans, and white sneakers, on the original plain light-gray background and framing from <image1>. Adjust the clothing's folds and shadows to the seated pose, with the stool's feet on the floor.
```

備考: raw: ポーズは移らず、ref-03 の人物を隣に並べた 2 人合成になった / enhanced: 難易度が低かったせいか遜色ない。


### i2i-05 左右へのアウトペイント

問題用紙: `../../i2i/05-outpaint.md`　画像: `../../_local/qwen-image-2-1/i2i/05-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
Extend the input image to the left and right into a wide 16:9 format. Continue the scene on both sides with the same buildings, street surface, objects, perspective, colors, and lighting, so the new areas read as one continuous photograph. Keep the person, the framing of the original area, and everything inside it exactly as they are.
```

備考: enhanced: アウトペイントでもパースの狂いは発生する。パッと見は綺麗。


### i2i-06 顔のクローズアップを作る

問題用紙: `../../i2i/06-close-up.md`　画像: `../../_local/qwen-image-2-1/i2i/06-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
Create a close-up portrait of the person in the input image, framed from the shoulders up with the face filling the frame. Preserve the person's facial identity, expression, hairstyle, and the direction and quality of the original lighting. Keep the background as a softly blurred continuation of the original.
```

備考: enhanced: 首の傾きなどはrawの方が良い


### i2i-07 画像2のヨガのポーズを画像1の人物に（難しいポーズ転写）

問題用紙: `../../i2i/07-yoga-pose-transfer.md`　画像: `../../_local/qwen-image-2-1/i2i/07-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
Use <image1> as the base image. Change the person's pose to match the yoga pose of the person in <image2>: standing on the left leg, the right leg bent and raised behind with the right hand holding the raised foot, the left arm extended straight forward, and the torso leaning slightly forward. Keep the person's facial identity, hairstyle, white t-shirt, blue jeans, white sneakers, and the original plain light-gray background and framing from <image1>. Adjust the clothing's stretch, folds, and shadows to the new pose, with the standing foot firmly on the floor.
```

備考: raw: 2人になってしまった / enhanced: QI2.1の方が基準モデルよりもポーズに忠実


## 考察

判定は 1 枚 run（seed 1）に基づく。ワークフローは参照付きの画像編集で、キャンバス延長やマスクは使っていない。

- 得意: 人、スタイル転写、3面図など。画風変換・衣服転写・三面図・クローズアップは raw でも基準モデルと同等
- 不得意: 人から人へのポーズ転写。raw は i2i-04・07 で 2 人を並べる合成になり、ポーズの言語化と「人物は 1 人だけ」の指定（enhanced）で初めて成立する。i2i-05 のアウトペイントは基準モデルと同じく情景の再構成になり、パースが崩れる
- enhance の要否: 必要。難しいポーズ転写では必須。単純な編集では raw で足りる
- 基準モデルとの差: かなり少なく実用的。i2i-07 では Qwen の enhanced の方がポーズに忠実
- enhanced が raw より劣った ID（軸の点数比較）: i2i-06: 保持・整合・品質。判定者の所感: クローズアップショットは顔の傾きなどで装飾的な記述があったせいかrawの方が良かった。
