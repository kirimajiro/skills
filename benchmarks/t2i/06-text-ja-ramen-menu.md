---
id: t2i-06
dimension: text-ja
samples: 4
aspect: 3:4
summary: ラーメン店のメニュー板。1 行目「本日のおすすめ」、2 行目「味噌ラーメン ¥900」、黒の筆文字
pairwise:
  - aspect: text
    q: 漢字・かなの字形と "¥900" が崩れていないのはどちらか
  - aspect: style
    q: 筆文字らしさが出ているのはどちらか
  - aspect: layout
    q: 2 行の配置とメニュー板としての設計が良いのはどちらか
---
# 06 ラーメン店のメニュー（日本語テキスト）

## Generic prompt

```text
A ramen shop menu board on a wall. The board reads "本日のおすすめ" on the first line and "味噌ラーメン ¥900" on the second line, in black brush-style characters on a cream background.
```

## 見るもの

- 漢字・かなの字形が崩れていないか
- 2行に分かれているか
- ¥ と数字
- 筆文字らしさ
