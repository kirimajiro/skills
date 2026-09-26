# flux-2-klein-9b — i2i 判定シート

- 基準モデル: GPT-Image 2.5
- 判定日: 
- 判定者: 
- ワークフロー設定（steps / guidance / sampler / 解像度）: 

## 集計

| ID | variant | 実行 | 保持 | 転写 | 整合 | 品質 | 備考 |
|----|---------|---|---|---|---|---|------|
| i2i-01 | raw |  |  |  |  |  |  |
| i2i-01 | enhanced |  |  |  |  |  |  |
| i2i-02 | raw |  |  |  |  |  |  |
| i2i-02 | enhanced |  |  |  |  |  |  |
| i2i-03 | raw |  |  |  |  |  |  |
| i2i-03 | enhanced |  |  |  |  |  |  |
| i2i-04 | raw |  |  |  |  |  |  |
| i2i-04 | enhanced |  |  |  |  |  |  |
| i2i-05 | raw |  |  |  |  |  |  |
| i2i-05 | enhanced |  |  |  |  |  |  |
| i2i-06 | raw |  |  |  |  |  |  |
| i2i-06 | enhanced |  |  |  |  |  |  |

## 問題用紙ごとの記録

### i2i-01 実写をアニメイラストに（画風変換）

問題用紙: `../../i2i/01-style-photo-to-anime.md`　画像: `../../_local/flux-2-klein-9b/i2i/`

Enhanced prompt:

```text
Turn image 1 into a 2D anime illustration with clean linework and soft cel shading. Keep the person's pose, facial features, hairstyle, clothing, and the background layout unchanged; simplify the background into painted flat tones in the same anime style.
```

備考:


### i2i-02 画像2の衣服を画像1の人物に着せる（衣服転写）

問題用紙: `../../i2i/02-clothing-transfer.md`　画像: `../../_local/flux-2-klein-9b/i2i/`

Enhanced prompt:

```text
Dress the person in image 1 in the mustard-yellow wool overcoat from image 2, keeping its cut, large dark buttons, and fabric. Keep the person's face, hairstyle, pose, hands, background, and framing from image 1 unchanged. Fit the coat to the pose with natural folds and shading that match the existing light.
```

備考:


### i2i-03 人物写真からキャラクターシート（三面図）

問題用紙: `../../i2i/03-character-sheet.md`　画像: `../../_local/flux-2-klein-9b/i2i/`

Enhanced prompt:

```text
Create a character sheet of the person in image 1: three full-body views standing in a row on a plain white background, front view on the left, side view in the middle, back view on the right. Keep the face, hairstyle, body proportions, and clothing identical across all three views, at the same scale, with soft even studio lighting.
```

備考:


### i2i-04 画像2のポーズを画像1の人物に（ポーズ転写）

問題用紙: `../../i2i/04-pose-transfer.md`　画像: `../../_local/flux-2-klein-9b/i2i/`

Enhanced prompt:

```text
Change the pose of the person in image 1 to match the pose of the person in image 2, including the position of the arms, legs, and head. Keep the person's face, hairstyle, clothing, background, and framing from image 1 unchanged; adjust the clothing's folds and shadows to the new pose.
```

備考:


### i2i-05 左右へのアウトペイント

問題用紙: `../../i2i/05-outpaint.md`　画像: `../../_local/flux-2-klein-9b/i2i/`

Enhanced prompt:

```text
Extend image 1 to the left and right into a wide 16:9 frame, continuing the same background surface, colors, and lighting on both sides. Keep the person and everything in the original area exactly unchanged.
```

備考:


### i2i-06 顔のクローズアップを作る

問題用紙: `../../i2i/06-close-up.md`　画像: `../../_local/flux-2-klein-9b/i2i/`

Enhanced prompt:

```text
Create a close-up portrait of the person in image 1, framed from the shoulders up with the face filling the frame. Keep the same face, expression, hairstyle, and the direction and quality of the original lighting; the background stays a softly blurred continuation of the original.
```

備考:


## 考察

（得意・不得意、enhance と品質タグの要否、基準モデルとの差）
