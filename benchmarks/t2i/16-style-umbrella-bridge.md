---
id: t2i-16
dimension: style-range
samples: 2 × 4 variants
aspect: 3:4
variants: [photograph, 2D anime illustration, oil painting, flat vector illustration]
summary: 石橋に立つ赤い傘の若い女性、小雨。画風を 4 通りで（写真 / アニメ / 油彩 / フラット）
pairwise:
  - aspect: style
    q: 指示した画風として成立しているのはどちらか
  - aspect: texture
    q: その画風の素材感（粒子・線と塗り・筆致・面）が本物らしいのはどちらか
  - aspect: anatomy
    q: 女性の姿と傘の持ち方が自然なのはどちらか
---
# 16 赤い傘の女性を4つの画風で（画風の幅）

## Generic prompt

```text
A {style} of a young woman with a red umbrella standing on a stone bridge in light rain.
```

`{style}` を各 variant に置き換えて 1 プロンプトずつ流す。

## 見るもの

- 画風ごとに成立しているか（写真らしさ・アニメの線と塗り・油彩の筆致・フラットの面）
- 主題と赤い傘が全画風で維持されるか
- 苦手な画風の特定
- 画風間で構図が引きずられていないか
