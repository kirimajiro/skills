---
id: t2i-04
dimension: long-instruction
samples: 4
aspect: 3:2
summary: 公園のベンチに 3 人（黄レインコート＋黒傘 / 青デニム＋文庫本 / 緑パーカー＋紙コップ）、全員が本を見る
pairwise:
  - aspect: anatomy
    q: 手と持ち物の接触・関節・ポーズが自然なのはどちらか
  - aspect: skin
    q: 3 人の表情と本への視線に説得力があるのはどちらか
  - aspect: context
    q: ベンチ・公園・天候の補完が場面に合っているのはどちらか
---
# 04 ベンチの三人（長い指示への忠実さ: 属性の結び付け）

## Generic prompt

```text
Three young adults sit on a park bench. The person on the left wears a yellow raincoat and holds a closed black umbrella. The person in the middle wears a blue denim jacket and reads a paperback book. The person on the right wears a green hoodie and holds a white paper coffee cup. All three are looking at the book.
```

## 見るもの

- 人数がちょうど3人か
- 服の色と持ち物が人物ごとに正しく結び付いているか
- 3人の視線が本に向いているか
- 手と持ち物の接触の自然さ
