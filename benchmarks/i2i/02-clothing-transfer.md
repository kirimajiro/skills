---
id: i2i-02
refs: [ref-01, ref-02]
samples: 4
aspect: follow ref-01
---
# 02 画像2の衣服を画像1の人物に着せる（衣服転写）

## 入力

- image1: `refs/ref-01.png`
- image2: `refs/ref-02.png`

## Generic instruction

```text
Dress the person in image 1 in the jacket from image 2.
```

## 見るもの

- コートの形・色・ボタンが ref-02 どおりか
- 顔・髪・ポーズ・背景の保持
- コートが体に沿っているか（皺・縮尺）
- 元の服が残っていないか
