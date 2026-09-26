---
id: t2i-02
dimension: short-instruction
samples: 8
aspect: 3:4
summary: 老いた漁師の肖像（指示はこれだけ）
pairwise:
  - aspect: skin
    q: 皺・日焼け・髭と表情に年齢の説得力があるのはどちらか
  - aspect: context
    q: 服装と背景（港・海・船）の補完が漁師らしいのはどちらか
  - aspect: texture
    q: 肌・髭・服の質感が CG っぽくなく本物に見えるのはどちらか
---
# 02 老いた漁師の肖像（短い指示での補完力）

## Generic prompt

```text
Portrait of an old fisherman.
```

## 見るもの

- 年齢の表現（皺・日焼け・髭）
- 服装と背景（港・海・船）の補完
- 表情と向きの多様性
- raw で品質が出るか（品質タグの要否）
