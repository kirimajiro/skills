# qwen-image-2-1 — t2i 判定シート

- 基準モデル: GPT-Image 2.5
- 判定日: 2026-09-24
- 判定者: リポジトリ所有者
- ワークフロー設定（steps / guidance / sampler / 解像度）: steps 25 / cfg 1 / euler / simple / 約 1 MP（1:1 1024x1024、3:2 1216x816、2:3 816x1216、3:4 864x1152、16:9 1344x752）。seed 1（`_local/qwen-image-2-1/t2i/run.json`）
- 最良の付け方: enhanced 行も raw との差で付けている（ルーブリックの「enhanced でも基準モデルに追いつくか」は krea-2-turbo・flux-2-klein-9b から適用）

## 集計

| ID | variant | 忠実 | 補完 | 最良 | 多様 | 品質 | 備考 |
|----|---------|---|---|---|---|---|------|
| t2i-01 | raw | 2 | 0 | 0 |  | 0 |  |
| t2i-01 | enhanced | 2 | 1 | 1 |  | 1 |  |
| t2i-02 | raw | 2 | 1 | 1 |  | 0 |  |
| t2i-02 | enhanced | 2 | 2 | 2 |  | 2 |  |
| t2i-03 | raw | 2 | 0 | 0 |  | 0 |  |
| t2i-03 | enhanced | 2 | 2 | 1 |  | 1 |  |
| t2i-04 | raw | 2 | 1 | 1 |  | 0 |  |
| t2i-04 | enhanced | 2 | 2 | 2 |  | 1 |  |
| t2i-05 | raw | 2 | 1 | 1 |  | 0 |  |
| t2i-05 | enhanced | 2 | 1 | 1 |  | 1 |  |
| t2i-06 | raw | 2 | 0 | 0 |  | 0 |  |
| t2i-06 | enhanced | 2 | 1 | 1 |  | 1 | 日本語は得意そう、日本語の文字のレイアウトはダサい |
| t2i-07 | raw | 2 | 2 | 1 |  | 1 |  |
| t2i-07 | enhanced | 2 | 2 | 1 |  | 1 |  |
| t2i-08 | raw | 2 | 0 | 0 |  | 0 | ポーズ、四肢指崩れ、鏡、どれを取っても劣悪 |
| t2i-08 | enhanced | 2 | 0 | 0 |  | 0 | ポーズ、四肢指崩れ、鏡、どれを取っても劣悪 |
| t2i-09 | raw | 2 | 2 | 1 |  | 1 |  |
| t2i-09 | enhanced | 2 | 2 | 1 |  | 1 | 生成AI感のある肌の質感がある |
| t2i-10 | raw | 2 | 2 | 1 |  | 0 |  |
| t2i-10 | enhanced | 2 | 2 | 0 |  | 0 | 繰り返しのある無機物の描画がまったくおかしい。直線が引けない、歪みが酷い、等の問題がある |
| t2i-11 | raw | 1 | 1 | 0 |  | 0 |  |
| t2i-11 | enhanced | 0 | 0 | 0 |  | 0 | エンジンのように無機物で連続した造形のあるものは形がいびつになり不可。 |
| t2i-12 | raw | 2 | 2 | 1 |  | 1 |  |
| t2i-12 | enhanced | 2 | 2 | 2 |  | 1 | 有機物の違和感は少ない。 |
| t2i-13 | raw | 2 | 2 | 1 |  | 1 |  |
| t2i-13 | enhanced | 2 | 2 | 2 |  | 1 | 副題で示した人物は小さく描写される |
| t2i-14 | raw | 2 | 0 | 0 |  | 1 | 左手と右手が別人のように見える |
| t2i-14 | enhanced | 2 | 1 | 1 |  | 1 | POVショット感が強調されていて悪くはない |
| t2i-15 | raw | 2 | 0 | 1 |  | 1 | アイソメトリックの部屋からベッドがはみ出している |
| t2i-15 | enhanced | 2 | 1 | 1 |  | 1 | 余白が大きめで対象物が小さいが悪くはない |
| t2i-16 | raw | 2/2/2/2 | 1/0/0/0 | 0/0/1/0 |  | 0/1/1/0 | 写真/アニメ/油彩/フラットの順。詳細は問題用紙ごとの記録 |
| t2i-16 | enhanced | 2/2/2/2 | 1/1/0/0 | 1/1/0/0 |  | 0/1/0/0 | 写真/アニメ/油彩/フラットの順。詳細は問題用紙ごとの記録 |
| t2i-17 | raw | 2 | 0 | 1 |  | 1 | ある程度小さい人物はいびつになる、パッと見の雰囲気だけの画像 |
| t2i-17 | enhanced | 2 | 0 | 1 |  | 1 | しめ縄の太さがいびつ、階段の手すりもいびつ、木の枝の生え方もおかしい、踊り場の鳥居と奥の神社が合体しているように見える、日本の写真の事前訓練はしている様だが十分でない |
| t2i-18 | raw | 2 | 0 | 0 |  | 0 | 石畳、電線、シャッター、窓の格子などどれをとってもいびつ、提灯の位置もおかしい |
| t2i-18 | enhanced | 2 | 0 | 0 |  | 0 | 商店街の天井のアーチ状のガラス窓の骨組みがいびつ、提灯や看板の文字はどれも文字になっていない |
| t2i-19 | raw | 2 | 2 | 2 |  | 1 |  |
| t2i-19 | enhanced | 2 | 2 | 2 |  | 1 | 立体としておかしいが雰囲気は遜色ない。水滴などシズル感の書き足し補完がない |
| t2i-20 | raw | 2 | 1 | 0 |  | 1 | ラーメン見えない、麺が白っぽい。スチル用としては商品写真の麺の見せ方ではない。 |
| t2i-20 | enhanced | 2 | 2 | 1 |  | 1 | 美味しそうに見えるが麺が乾いていて汁に浸かっていないのでおかしい。 |
| t2i-21 | raw | 2 | 0 | 1 |  | 0 | ラフな感じのポスター。 |
| t2i-21 | enhanced | 2 | 0 | 0 |  | 0 | ポスターとしてのデザインは0点に近い |
| t2i-22 | raw | 2 | 1 | 1 |  | 0 | 紐の交差がおかしい |
| t2i-22 | enhanced | 2 | 2 | 1 |  | 1 | 余白も含めて悪くない |
| t2i-23 | raw | 1 | 0 | 1 |  | 0 | 女性の顔がぶさいく？電車の高架がくずれている、傘も壊れている、パースがおかしい |
| t2i-23 | enhanced | 1 | 1 | 0 |  | 0 | パースがおかしい |

## 問題用紙ごとの記録

### t2i-01 雨の夜の路地（短い指示での補完力）

問題用紙: `../../t2i/01-short-rainy-alley.md`　画像: `../../_local/qwen-image-2-1/t2i/01-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of a narrow city alley on a rainy night. Wet asphalt fills the lower half of the frame, reflecting the warm orange glow of a single street lamp on the left and the cool blue of a small shop sign further down on the right. Brick walls line both sides, with a fire escape and a few stacked crates near the right wall. Fine rain streaks through the lamplight, and a thin mist softens the far end of the alley. The palette combines deep blue-black shadows, warm amber highlights, and muted brick red.
```

備考: 特記なし


### t2i-02 老いた漁師の肖像（短い指示での補完力）

問題用紙: `../../t2i/02-short-old-fisherman.md`　画像: `../../_local/qwen-image-2-1/t2i/02-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
An editorial portrait photograph of an elderly fisherman, framed from the chest up, facing the camera with a calm, weathered expression. Deep wrinkles and sun-darkened skin show fine texture, and a short gray beard covers his jaw. He wears a faded navy knit cap and a yellow oilskin jacket with the collar turned up. Behind him, a harbor with moored wooden boats falls softly out of focus. Overcast daylight from the front-left reveals the texture of his skin and the sheen of the wet jacket. The palette is muted sea-gray, navy, and worn yellow.
```

備考: 特記なし


### t2i-03 市場の屋台（長い指示への忠実さ: 数と順序）

問題用紙: `../../t2i/03-long-market-stall.md`　画像: `../../_local/qwen-image-2-1/t2i/03-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of a wooden market stall viewed straight on at counter height. Exactly three wicker baskets stand in a row on the counter: the left basket is filled with red apples, the middle basket with green pears, and the right basket with yellow lemons. A handwritten chalkboard sign leans against the front of the counter on the right side. A red-and-white striped awning stretches across the top of the frame behind the stall. Soft morning daylight from the left brings out the weave of the baskets and the wood grain. Warm reds, greens, and yellows sit against the natural brown of the wood.
```

備考: 特記なし


### t2i-04 ベンチの三人（長い指示への忠実さ: 属性の結び付け）

問題用紙: `../../t2i/04-long-three-friends.md`　画像: `../../_local/qwen-image-2-1/t2i/04-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of exactly three young adults sitting side by side on a wooden park bench, framed from the knees up at eye level. The person on the left wears a yellow raincoat and holds a closed black umbrella upright between the knees. The person in the middle wears a blue denim jacket and holds an open paperback book in both hands. The person on the right wears a green hoodie and holds a white paper coffee cup. All three look down at the book in the middle person's hands. Behind them, green park trees fall softly out of focus. Overcast daylight gives even, soft shadows.
```

備考: 特記なし


### t2i-05 カフェの看板（英語テキスト）

問題用紙: `../../t2i/05-text-en-cafe-sign.md`　画像: `../../_local/qwen-image-2-1/t2i/05-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of a small cafe storefront viewed straight on from across the sidewalk. Above the glass door, a wooden sign reads "Blue Heron Coffee" in white serif letters, centered and spanning most of the sign's width. To the left of the entrance, a small chalkboard on an easel reads "Open 7am – 4pm" in white handwritten chalk letters. The facade is painted deep teal with brass door hardware, and potted plants stand on either side of the door. Late afternoon sunlight from the right warms the wood and casts soft shadows on the sidewalk.
```

備考: 特記なし


### t2i-06 ラーメン店のメニュー（日本語テキスト）

問題用紙: `../../t2i/06-text-ja-ramen-menu.md`　画像: `../../_local/qwen-image-2-1/t2i/06-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of a ramen shop menu board mounted on a plaster wall, viewed straight on. The cream-colored board has two lines of black brush-style characters: the first line reads "本日のおすすめ" in medium size, and the second line below it reads "味噌ラーメン ¥900" in larger characters. The board has a thin dark wooden frame. Warm tungsten light from above-left gives the cream surface a gentle gradient and reveals the paper texture.
```

備考: enhanced: 日本語は得意そう、日本語の文字のレイアウトはダサい


### t2i-07 空中のスケートボーダー（人体・動きのあるポーズ）

問題用紙: `../../t2i/07-pose-skateboard-air.md`　画像: `../../_local/qwen-image-2-1/t2i/07-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of a skateboarder suspended in mid-air above a concrete half-pipe, captured from a low angle at the lip of the ramp. The rider's knees are tucked, one hand grips the middle of the board's edge, and the other arm extends outward for balance. The rider wears a black helmet, a gray t-shirt, and loose dark pants, and looks down toward the landing. The half-pipe's curved wall fills the lower part of the frame, with a clear blue sky above. Bright midday sunlight from the upper right casts a sharp shadow of the rider onto the concrete.
```

備考: 特記なし


### t2i-08 リフトする二人のダンサー（人体の絡みと表情）

問題用紙: `../../t2i/08-pose-two-dancers.md`　画像: `../../_local/qwen-image-2-1/t2i/08-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of two adult dancers in a bright rehearsal studio. One dancer lifts the other at the waist, the lifted dancer's arms stretched outward and one leg extended behind, both with wide joyful smiles. They wear simple gray and black practice clothes. A wide wall mirror behind them reflects their backs and the wooden floor, with a barre running along the mirror. Soft daylight from tall windows on the left fills the room and leaves gentle shadows on the floor.
```

備考: raw: ポーズ、四肢指崩れ、鏡、どれを取っても劣悪 / enhanced: ポーズ、四肢指崩れ、鏡、どれを取っても劣悪


### t2i-09 驚いた顔のクローズアップ（ショット: クローズアップ＋表情）

問題用紙: `../../t2i/09-closeup-surprised-face.md`　画像: `../../_local/qwen-image-2-1/t2i/09-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A close-up photograph of a middle-aged woman's face filling the frame, with a surprised expression: eyes wide open, eyebrows raised, and mouth slightly open. Fine lines around her eyes and natural skin texture with subtle pores are visible. Her dark hair with a few gray strands is pulled back. Soft window light from the left models her cheekbones and leaves a gentle catchlight in each eye. The background is a plain, softly blurred neutral gray.
```

備考: enhanced: 生成AI感のある肌の質感がある


### t2i-10 ガラスと鉄骨の駅コンコース（無機物: 建築）

問題用紙: `../../t2i/10-arch-station-interior.md`　画像: `../../_local/qwen-image-2-1/t2i/10-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of the interior of a modern train station concourse with a sweeping curved roof of glass panels held by white steel ribs. The viewpoint is at floor level looking down the length of the hall, so the ribs converge toward the far end. A few commuters walk across the polished stone floor in the middle distance, small against the height of the roof. Morning sunlight streams through the glass from the upper right, laying long bright bands and soft shadows across the floor. The palette is white, pale gray, and warm morning gold.
```

備考: enhanced: 繰り返しのある無機物の描画がまったくおかしい。直線が引けない、歪みが酷い、等の問題がある


### t2i-11 ビンテージバイクのエンジン（無機物: 機械）

問題用紙: `../../t2i/11-machine-motorcycle-engine.md`　画像: `../../_local/qwen-image-2-1/t2i/11-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A close-up photograph of a vintage motorcycle engine resting on a wooden workshop bench. The finned aluminum cylinder occupies the center of the frame, with a chrome exhaust pipe curving out from its base toward the lower left and a polished chrome valve cover on top. Oil stains, small scratches, and bolts with worn edges show the age of the metal. Scattered tools and a rag lie on the bench behind it, softly out of focus. A single work lamp from the upper left brings out the brushed aluminum and the mirror-like chrome highlights.
```

備考: enhanced: エンジンのように無機物で連続した造形のあるものは形がいびつになり不可。


### t2i-12 草原のキツネ（有機物: 動物）

問題用紙: `../../t2i/12-animal-red-fox.md`　画像: `../../_local/qwen-image-2-1/t2i/12-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A wildlife photograph of a single red fox standing in tall golden grass, facing the camera with ears upright and alert amber eyes. The fox's rust-orange coat shows individual strands of fur, with white fur on the chest and black on the lower legs. Its full body is visible, positioned slightly right of center, with the bushy tail curving behind. The background is a meadow falling into soft focus. Low golden-hour sunlight from behind and to the left outlines the fur with a warm rim light and casts long shadows through the grass.
```

備考: enhanced: 有機物の違和感は少ない。


### t2i-13 雨上がりの渓谷（有機物: 自然＋ショット: ワイド）

問題用紙: `../../t2i/13-nature-wide-valley.md`　画像: `../../_local/qwen-image-2-1/t2i/13-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A wide landscape photograph of a forested mountain valley just after rain, seen from a high viewpoint on a trail. Dense green conifers cover the slopes on both sides, and a silver river winds along the valley floor far below. In the lower-left foreground, a single hiker with a red backpack walks along the trail, small against the scale of the valley. Wisps of low cloud drift between the ridges, and the far peaks fade into pale blue haze. Diffused light from an overcast sky keeps the greens deep and saturated.
```

備考: enhanced: 副題で示した人物は小さく描写される


### t2i-14 コーヒーを持つ自分の手（ショット: POV）

問題用紙: `../../t2i/14-pov-hands-coffee.md`　画像: `../../_local/qwen-image-2-1/t2i/14-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A first-person photograph looking down at my own two hands holding a white ceramic mug of coffee, thumbs resting on the rim, the mug centered in the lower half of the frame. Beyond the mug, an open laptop and a lined notebook with a pen lie on a light oak desk. The upper part of the frame shows a window with raindrops on the glass and a blurred gray street outside. Soft daylight from the window in front lights the hands and the desk.
```

備考: raw: 左手と右手が別人のように見える / enhanced: POVショット感が強調されていて悪くはない


### t2i-15 アイソメトリックのワンルーム（ショット: アイソメトリック）

問題用紙: `../../t2i/15-isometric-room.md`　画像: `../../_local/qwen-image-2-1/t2i/15-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
An isometric 3D render of a small cozy studio apartment, cut away so the interior is fully visible from above at a 45-degree angle, centered on a plain white background. Inside: a single bed with a blue blanket against the back-left wall, a wooden desk with a computer monitor and chair against the back-right wall, a tall bookshelf filled with colorful books beside the desk, a leafy potted plant in the front corner, and a window on the back-left wall. The floor is warm oak. Soft even studio lighting with gentle shadows gives the scene a clean miniature look.
```

備考: raw: アイソメトリックの部屋からベッドがはみ出している / enhanced: 余白が大きめで対象物が小さいが悪くはない


### t2i-16 赤い傘の女性を4つの画風で（画風の幅）

問題用紙: `../../t2i/16-style-umbrella-bridge.md`　画像: `../../_local/qwen-image-2-1/t2i/16-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompts（variant ごと）:

- photograph

```text
A photograph of a young woman holding a red umbrella, standing on an old stone bridge in light rain, framed from the knees up. She wears a beige trench coat and faces slightly away from the camera. Raindrops dot the wet stone parapet, and the river and trees behind her fall softly out of focus. Overcast daylight gives soft, even light, with the red umbrella as the strongest color against gray stone and muted green.
```

- 2D anime illustration

```text
A 2D anime illustration of a young woman holding a red umbrella, standing on an old stone bridge in light rain, framed from the knees up. She has shoulder-length dark hair and wears a beige trench coat. Clean linework and soft cel shading define the figure, with rain drawn as fine pale streaks. The stone bridge and blurred green trees behind her are painted in muted tones, so the red umbrella stands out.
```

- oil painting

```text
An oil painting of a young woman holding a red umbrella, standing on an old stone bridge in light rain, framed from the knees up. Visible brushstrokes and thick impasto describe her beige coat and the wet stone. The river and trees behind her are loosely suggested in muted greens and grays. Soft overcast light and a limited palette make the red umbrella the focal point.
```

- flat vector illustration

```text
A flat vector illustration of a young woman holding a red umbrella, standing on a stone bridge in light rain, framed from the knees up. Simple geometric shapes, solid fills without gradients, and a limited palette of gray, muted green, beige, and bright red. Rain is shown as short diagonal lines. The composition is clean with generous open sky.
```

判定（画風別）:

| 画風 | variant | 忠実 | 補完 | 最良 | 品質 | 備考 |
|---|---|---|---|---|---|---|
| photograph | raw | 2 | 1 | 0 | 0 | 服装や髪型が韓国の伝統のファッション？橋の構造がおかしい、ポーズも意味不明 |
| photograph | enhanced | 2 | 1 | 1 | 0 | 橋の石が橋らしく見えない、背景に写る護岸もいびつ |
| 2D anime illustration | raw | 2 | 0 | 0 | 1 | 消失点、橋と人物のサイズ感、背景の描き方、雨の方向、どれを取ってもおかしい |
| 2D anime illustration | enhanced | 2 | 1 | 1 | 1 | 橋の遠近感がおかしい |
| oil painting | raw | 2 | 0 | 1 | 1 | モネのような画風、→下にサインらしき物が入る |
| oil painting | enhanced | 2 | 0 | 0 | 0 | 橋の遠近感と人物の立ち位置の違和感が強い、雨の描き方が子供のイラストのよう |
| flat vector illustration | raw | 2 | 0 | 0 | 0 |  |
| flat vector illustration | enhanced | 2 | 0 | 0 | 0 | 粗雑で使い物にならない |

備考: 苦手な画風はフラットベクターと油彩。写真も橋の構造が崩れる


### t2i-17 初詣の神社（日本の文化の知識）

問題用紙: `../../t2i/17-japan-shrine-newyear.md`　画像: `../../_local/qwen-image-2-1/t2i/17-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of a Japanese Shinto shrine on New Year's morning. A red torii gate stands in the foreground, and a wide stone staircase leads up to the main hall behind it. Japanese people in kimono climb the steps, with the kimono's left side folded over the right, some carrying small handbags. Paper lanterns hang along the approach, and a thick shimenawa rope with white paper streamers spans the gate. Crisp winter morning sunlight from the right casts long shadows on the steps, and bare trees frame the scene.
```

備考: raw: ある程度小さい人物はいびつになる、パッと見の雰囲気だけの画像 / enhanced: しめ縄の太さがいびつ、階段の手すりもいびつ、木の枝の生え方もおかしい、踊り場の鳥居と奥の神社が合体しているように見える、日本の写真の事前訓練はしている様だが十分でない


### t2i-18 夕暮れの商店街（日本の風景の知識）

問題用紙: `../../t2i/18-japan-shotengai.md`　画像: `../../_local/qwen-image-2-1/t2i/18-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A photograph of a covered shopping arcade in a Japanese town at dusk. The arched glass roof runs down the center of the frame, and hanging shop signs with Japanese characters line both sides. On the right, an izakaya's red paper lantern glows beside a noren curtain. On the left, a bicycle leans against a closed metal shutter. A few pedestrians walk in the distance. Fluorescent shop lights and the warm lantern mix with the cool blue of dusk entering from the far end of the arcade.
```

備考: raw: 石畳、電線、シャッター、窓の格子などどれをとってもいびつ、提灯の位置もおかしい / enhanced: 商店街の天井のアーチ状のガラス窓の骨組みがいびつ、提灯や看板の文字はどれも文字になっていない


### t2i-19 逆光の香水瓶（素材・質感・光: プロダクト）

問題用紙: `../../t2i/19-product-perfume-backlit.md`　画像: `../../_local/qwen-image-2-1/t2i/19-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A product photograph of a clear glass perfume bottle with a polished gold cap, standing on a wet black stone surface, centered in the frame. Backlight from behind the bottle glows through the pale amber liquid and refracts along its faceted edges, while a soft rim light traces the left and right contours of the glass. The wet stone reflects the bottle's base and the highlights. The background is deep black, fading to a faint warm halo behind the bottle.
```

備考: enhanced: 立体としておかしいが雰囲気は遜色ない。水滴などシズル感の書き足し補完がない


### t2i-20 湯気の立つ豚骨ラーメン（素材・質感・光: フード）

問題用紙: `../../t2i/20-food-ramen-steam.md`　画像: `../../_local/qwen-image-2-1/t2i/20-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A food photograph of a bowl of tonkotsu ramen on a dark wooden counter, shot from a 45-degree angle. The creamy pale broth holds a nest of noodles, two slices of chashu pork, a soft-boiled egg cut in half showing its orange yolk, and a scattering of chopped green onions. Thin steam rises from the surface. A pair of wooden chopsticks rests on the bowl's rim. Warm light from the upper left brings out the glossy sheen of the broth and the fat on the pork, and the background falls into soft dark focus.
```

備考: raw: ラーメン見えない、麺が白っぽい。スチル用としては商品写真の麺の見せ方ではない。 / enhanced: 美味しそうに見えるが麺が乾いていて汁に浸かっていないのでおかしい。


### t2i-21 ジャズナイトのポスター（レイアウト: ポスターの雰囲気）

問題用紙: `../../t2i/21-poster-layout-jazz.md`　画像: `../../_local/qwen-image-2-1/t2i/21-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A concert poster with a deep blue background. At the top, a large headline reads "Midnight Jazz" in cream-colored bold serif letters, centered. In the middle, a gold silhouette of a saxophone player in profile, leaning back mid-performance. At the bottom, the date "Oct 12" in smaller cream sans-serif letters, centered. The palette is limited to deep blue, cream, and gold, with a subtle paper grain across the poster. Flat, even lighting keeps the colors uniform.
```

備考: raw: ラフな感じのポスター。 / enhanced: ポスターとしてのデザインは0点に近い


### t2i-22 余白を残した靴の商品写真（レイアウト: 余白の効き）

問題用紙: `../../t2i/22-blank-space-product.md`　画像: `../../_local/qwen-image-2-1/t2i/22-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
A product photograph of a pair of white running shoes standing side by side on a plain light-gray background, placed in the lower-right quarter of the frame and viewed from a slight three-quarter angle. The left two-thirds of the image is a continuous, uniform light-gray area with no objects, reserved for text. Soft studio light from the upper left gives the shoes gentle shadows on the surface.
```

備考: raw: 紐の交差がおかしい / enhanced: 余白も含めて悪くない


### t2i-23 雨の東京の商店街（総合: 一本で多くの切り口を同時に試す）

問題用紙: `../../t2i/23-omnibus-tokyo-rain-street.md`　画像: `../../_local/qwen-image-2-1/t2i/23-*` （raw / enhanced 各 `_00001.png`）

Enhanced prompt:

```text
An editorial portrait photograph with a 35mm full-frame look and shallow depth of field, taken on a rainy evening in a dense Tokyo shopping street. In the near foreground, sharply in focus, a wet steel railing and a hanging red paper lantern partially frame the left edge, and a small handwritten cafe chalkboard reads exactly "OPEN 'til 2AM" in white chalk. In the mid-ground, a woman in her late twenties with short black hair wears a translucent yellow rain poncho over a charcoal blazer. She is caught mid-stride, twisting her torso to look back over her right shoulder; her left hand raises a clear umbrella, her right hand holds a paper coffee cup near her chin, and one foot is lifted off the wet pavement. Her face is lit by neon, and she is laughing with her eyes half-closed. In the far background, a crowd of forty or more blurred pedestrians with umbrellas forms a repeating pattern that recedes down the street, beside a row of vending machines and a rusted pedestrian bridge; ginkgo trees with wet yellow leaves and potted plants on balconies line the street. A large illuminated billboard high on a building reads exactly "NIGHT MARKET 11.22" in bold condensed white type on a red panel. Mixed magenta and cyan neon light reflects in puddles. The foreground and the woman are sharp, while the crowd shows slight motion blur and soft focus. Her skin retains natural texture, and the only text in the image is the two quoted strings.
```

備考: raw: 女性の顔がぶさいく？電車の高架がくずれている、傘も壊れている、パースがおかしい / enhanced: パースがおかしい


## 考察

判定は 1 枚 run（seed 1）に基づく。

- 得意: それっぽく作ること。有機物（動物・自然・肌）と短い指示の補完は破綻が少なく、雰囲気は基準モデルに近づく
- 不得意: 無機物、小さな人物、パース、小さい文字、イラスト。連続した造形の無機物（エンジン・鉄骨・アーケード）は形がいびつになり、直線と遠近が取れない。小さく描かれた人物・文字は崩れる。日本語の字形自体は出るがレイアウトは弱い
- enhance と品質タグの要否: 必要だがそれでも限界がある。enhanced は補完と最良を 1 段上げることが多いが、無機物・パース・ポスターの弱さは enhance では埋まらない
- 基準モデルとの差: 基準モデルとの差は全体的にかなり感じる。写実系でもパースが取れない問題、無機物がかけないなど乖離が大きい。
- enhanced が raw より劣った ID（軸の点数比較。判定者の所感は「特に感じ無かった。」）: t2i-10: 最良、t2i-11: 忠実・補完、t2i-16（oil painting）: 最良・品質、t2i-21: 最良、t2i-23: 最良
