---
id: i2i-04
refs: [ref-01, ref-03]
samples: 4
aspect: follow ref-01
---
# 04 画像2のポーズを画像1の人物に（ポーズ転写）

## 入力

- image1: `refs/ref-01.png`
- image2: `refs/ref-03.png`

## Generic instruction

```text
Make the person in image 1 take the pose of the person in image 2, keeping the original clothing and background.
```

## 見るもの

- 腕・脚・頭の位置が ref-03 のポーズと一致するか
- 顔・服・背景の保持
- ref-03 の人物の外見が混入していないか
- 新しいポーズでの服の皺・影の整合
