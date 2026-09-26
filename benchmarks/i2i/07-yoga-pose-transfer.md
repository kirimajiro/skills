---
id: i2i-07
refs: [ref-01, ref-04]
samples: 4
aspect: follow ref-01
---
# 07 画像2のヨガのポーズを画像1の人物に（難しいポーズ転写）

i2i-04 の発展。片脚立ちで体幹が傾き、腕と脚が交差するポーズなので、関節の位置・重心・服の変形を同時に要求する。

## 入力

- image1: `refs/ref-01.png`
- image2: `refs/ref-04.png`

## Generic instruction

```text
Make the person in image 1 take the yoga pose of the person in image 2, keeping the original clothing and background.
```

## 見るもの

- 片脚立ち・掴んだ足・前に伸ばした腕が ref-04 のポーズと一致するか（左右が入れ替わっていないか）
- 重心と接地（軸足が床に乗っているか、体が傾きに見合っているか）
- 顔の同一性・T シャツとジーンズ・背景の保持。ref-04 の人物の外見やヨガマットが混入していないか
- 新しいポーズでの服の伸び・皺・影の整合
