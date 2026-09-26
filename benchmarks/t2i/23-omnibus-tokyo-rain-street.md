---
id: t2i-23
dimension: omnibus
samples: 4
aspect: 2:3
summary: 雨の夜の東京の商店街、35mm f/2.8 のエディトリアル写真。振り返る女性・透明傘・紙コップ、看板 2 種、傘の群衆、ネオン
pairwise:
  - aspect: text
    q: "OPEN 'til 2AM" と "NIGHT MARKET 11.22" が正確で、指定外の文字が出ていないのはどちらか
  - aspect: anatomy
    q: 右肩越しの振り返り・左手の傘・右手のカップ・浮いた片足と手指が成立しているのはどちらか
  - aspect: fidelity
    q: 主題の指定（黒のショート・黄色の透明ポンチョ・チャコールのブレザー・目を細めた笑顔）が揃っているのはどちらか
  - aspect: fidelity
    q: 背景の指定（傘の群衆 40 人以上・自販機・歩道橋・黄葉の銀杏・鉢植え）が揃っているのはどちらか
  - aspect: composition
    q: 前景がシャープで背景の群衆だけがボケと動きブレになる三層が成立しているのはどちらか
  - aspect: light
    q: マゼンタとシアンのネオン・水たまりの反射・顔への照り返しが出ているのはどちらか
  - aspect: culture
    q: 東京の商店街として違和感がないのはどちらか
---
# 23 雨の東京の商店街（総合: 一本で多くの切り口を同時に試す）

ユーザー提供の定型プロンプト（2026-09-23）。前景・中景・背景の三層、表示テキスト 2 種、ひねりのある動きのポーズ、40 人以上の群衆、無機物と有機物、混合ネオン光と浅い被写界深度を一度に要求する。個別の切り口で 2 を取るモデルでも、同時要求で何が最初に崩れるかを見る。原文どおり保持し、末尾の否定形もそのまま流す（enhanced 側はスキルが肯定形に書き直す）。

## Generic prompt

```text
Editorial portrait photograph, 35mm full-frame look, f/2.8, rainy evening in a dense Tokyo shopping street.

Foreground (near, sharply in focus): a wet steel railing and a hanging red paper lantern partially framing the left edge, and a small handwritten cafe chalkboard reading exactly "OPEN 'til 2AM" in white chalk.

Subject (mid-ground): a woman in her late 20s with short black hair, wearing a translucent yellow rain poncho over a charcoal blazer, caught mid-stride while twisting her torso to look back over her right shoulder; her left hand raises a clear umbrella, her right hand holds a paper coffee cup near her chin, and one foot is lifted off the wet pavement. Her face is lit by neon and she is laughing with her eyes half-closed.

Background (far): a crowd of forty or more blurred pedestrians with umbrellas forming a repeating pattern that recedes down the street; a row of vending machines and a rusted pedestrian bridge (inorganic); ginkgo trees with wet yellow leaves and potted plants on balconies (organic). A large illuminated billboard high on a building reads exactly "NIGHT MARKET 11.22" in bold condensed white type on red.

Lighting: mixed neon (magenta and cyan) with reflections in puddles, shallow depth of field, slight motion blur only in the crowd. Photorealistic, natural skin texture, no watermark, no extra text beyond the two quoted strings.
```

## 見るもの

- 表示テキスト: "OPEN 'til 2AM"（アポストロフィと小文字）と "NIGHT MARKET 11.22" が正確か。指定外の文字が看板・ネオンに出ていないか
- ポーズ: 歩行中の右肩越しの振り返り、左手の透明傘、右手のカップ、片足が浮いているか。手指と関節の破綻
- 三層の被写界深度: 前景（手すり・提灯・黒板）がシャープ、背景の群衆だけがボケと動きブレになっているか
- 群衆の数と反復（40 人以上）、自販機・歩道橋（無機物）と銀杏・鉢植え（有機物）の両立
- 光: マゼンタとシアンのネオン、水たまりの反射、顔がネオンで照らされているか
- 崩れる順番: 個別の切り口で取れているモデルが、同時要求でどこから落とすか
