---
id: t2i-05
dimension: text-en
samples: 4
aspect: 3:2
summary: 小さなカフェの店先。木の看板に "Blue Heron Coffee"、黒板に "Open 7am – 4pm"
pairwise:
  - aspect: text
    q: "Blue Heron Coffee" と "Open 7am – 4pm" の綴り・記号が正確なのはどちらか
  - aspect: layout
    q: 看板と黒板の配置・書体が店先として成立しているのはどちらか
  - aspect: texture
    q: 木・壁・ガラスの質感が本物に見えるのはどちらか
  - aspect: context
    q: 店先の小物（席・植物・照明）の補完がカフェらしいのはどちらか
---
# 05 カフェの看板（英語テキスト）

## Generic prompt

```text
A storefront of a small cafe. The wooden sign above the door reads "Blue Heron Coffee" in white serif letters. A smaller chalkboard by the entrance reads "Open 7am – 4pm".
```

## 見るもの

- "Blue Heron Coffee" の綴りと大文字小文字
- "Open 7am – 4pm" の綴り・記号
- 2つの文字列が混ざらず別の面に載っているか
- セリフ体・手書きチョークの書体指定
