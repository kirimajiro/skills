---
id: t2i-01
dimension: short-instruction
samples: 8
aspect: 3:2
summary: 雨の夜の路地（指示はこれだけ）
pairwise:
  - aspect: context
    q: 指示にない人物・店・看板の補完が雨の路地の場面に合っているのはどちらか
  - aspect: light
    q: 路面の反射・雨の筋・街灯の光の扱いが自然なのはどちらか
  - aspect: texture
    q: 壁・路面が 3D っぽくなく本物の写真に見えるのはどちらか
---
# 01 雨の夜の路地（短い指示での補完力）

## Generic prompt

```text
A rainy night alley.
```

## 見るもの

- 時間帯・光源（街灯・看板・反射）をどう補完したか
- 路面の反射と雨の表現
- 人物や店の有無をどう判断したか
- 8枚の構図・視点が単調でないか
