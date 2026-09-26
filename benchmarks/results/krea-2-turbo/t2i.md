# krea-2-turbo — t2i 判定シート

- 基準モデル: GPT-Image 2.5
- 判定日: 2026-09-24
- 判定者: リポジトリ所有者
- ワークフロー設定（steps / guidance / sampler / 解像度）: steps 8 / cfg 1 / euler / simple / 約 1 MP（1:1 1024x1024、3:2 1216x816、2:3 816x1216、3:4 864x1152、16:9 1344x752）。seed 1（`_local/krea-2-turbo/t2i/run.json`）
- セッション（`_local/pairwise/`、git 管理外。各 85 問）:
  - `ab_krea-2-turbo_flux-2-klein-9b_20260924-1600` — vs flux-2-klein-9b（enhanced 同士）。約 20 分、引き分け 34
  - `raw-enh_krea-2-turbo_20260924-1600` — enhanced vs raw。約 18 分、引き分け 54
  - `vs-baseline_krea-2-turbo_gpt-image-2-5_20260924-1600` — vs GPT-Image 2.5 raw。約 4 分、引き分け 14

## 観点別プロファイル

セルは krea-2-turbo の勝率（勝 / 分 / 負、n）。引き分けは 0.5 勝、`*` は n が 3 未満。

| aspect | vs flux-2-klein-9b | raw vs enhanced | vs baseline (gpt-image-2-5) |
|---|---|---|---|
| texture 質感の本物感 | 0.43 (3/6/5, n=14) | 0.32 (1/7/6, n=14) | 0.11 (0/3/11, n=14) |
| detail ディテールとグランジ | 0.38 (1/1/2, n=4) | 0.62 (1/3/0, n=4) | 0.00 (0/0/4, n=4) |
| text 文字の正確さ | 0.50 (1/3/1, n=5) | 0.40 (0/4/1, n=5) | 0.10 (0/1/4, n=5) |
| layout 文字とレイアウト | 0.62 (1/3/0, n=4) | 0.38 (0/3/1, n=4) | 0.12 (0/1/3, n=4) |
| structure 構造物とパース | 0.88 (3/1/0, n=4) | 0.50 (0/4/0, n=4) | 0.12 (0/1/3, n=4) |
| anatomy 人体・手指・ポーズ | 0.72 (6/1/2, n=9) | 0.56 (3/4/2, n=9) | 0.11 (0/2/7, n=9) |
| skin 肌と表情 | 0.75 (3/0/1, n=4) | 0.38 (0/3/1, n=4) | 0.00 (0/0/4, n=4) |
| context 補完の文脈適合 | 0.31 (1/3/4, n=8) | 0.56 (2/5/1, n=8) | 0.00 (0/0/8, n=8) |
| style 画風の成立 | 0.64 (4/1/2, n=7) | 0.57 (2/4/1, n=7) | 0.14 (0/2/5, n=7) |
| organic 有機物の自然さ | 0.50 (1/0/1, n=2 *) | 0.75 (1/1/0, n=2 *) | 0.00 (0/0/2, n=2 *) |
| composition 構図とショット | 0.50 (0/8/0, n=8) | 0.56 (1/7/0, n=8) | 0.12 (0/2/6, n=8) |
| light 光と素材 | 0.36 (2/4/5, n=11) | 0.41 (2/5/4, n=11) | 0.09 (0/2/9, n=11) |
| culture 文化的な正しさ | 0.50 (1/1/1, n=3) | 0.67 (1/2/0, n=3) | 0.00 (0/0/3, n=3) |
| fidelity 要素の揃い方 | 0.50 (0/2/0, n=2 *) | 0.50 (0/2/0, n=2 *) | 0.00 (0/0/2, n=2 *) |

## enhance の効き

- 上げた観点: organic (+0.25, n=2), culture (+0.17, n=3), detail (+0.12, n=4), style (+0.07, n=7), context (+0.06, n=8), composition (+0.06, n=8), anatomy (+0.06, n=9)
- 下げた観点: texture (-0.18, n=14), layout (-0.12, n=4), skin (-0.12, n=4), text (-0.10, n=5), light (-0.09, n=11)
- 変わらない観点: structure (n=4), fidelity (n=2)

再判定（スキル v1.1.0、`raw-enh_krea-2-turbo_20260927-0023`、書き直した 8 枚が入る 11 問題・38 設問）:

- 同じ 8 枚での enhanced 勝率: texture 0.00 → 0.75（4/4/0, n=8）、light 0.17 → 0.58（3/1/2, n=6）、skin 0.25 → 1.00（n=2）、context 0.50 → 0.83（n=3）
- 判定者の雑感: 前のよりも自然に出ている様に感じます。enh が劣っているということは無いと思います
- enhanced が負けた残り: 16 photograph（style・anatomy）、23（light）。いずれも n=1

## 感想戦

- 判定者の雑感（セッションの notes）:
  - vs flux-2-klein-9b: そこまで大差は無いが、クローズアップやパースの正確さになるとBの方がどうしても劣って見える。（B = flux）
  - enhanced vs raw: 比較的安定感のあるモデルであると感じた。
  - vs 基準: これは仕方ない。GPT-Image 2.5の圧勝。ただし情報量が少なく人間が見慣れていないものは違和感の差が少ない。またGPT-Image 2.5は生成前にリーズニングが入るので情報過多になりやすい。
- ヒアリング（判定者の言葉）:
  - 強い観点の理由: flux はパース・クローズアップが崩れる
  - 弱い観点の理由: krea は光が平板（反射・逆光が弱い）、krea はグランジ（汚れ・経年）が出ない
  - enhance について: enhance は質感を CG 寄りにしている。enhance は場面の補完には効いている。Krea のスキルはもっと改善の余地があると思う。今回の評価を踏まえて研究→スキル改善ができるかも知れない
  - 用途について: 基本的に生成性能でローカル vs フロンティアで使い分けることはしない（プロジェクトに応じた使い分け）。あくまで vs としたのはローカルモデルの力量を測るため
- Claude の整理:
  - 得意（vs flux）: structure 0.88（t2i-08 鏡像・10 駅コンコース・11 エンジンで勝ち）、skin 0.75（02・08・09）、anatomy 0.72（07・08・14・16 anime / flat / oil）、style 0.64（06 筆文字・15 3D レンダー・16 anime / flat）、layout 0.62（06）。flux の崩れはパースとクローズアップに出る
  - 不得意（vs flux）: context 0.31（01・03・05・10 で負け。場面の書き込みが薄い）、light 0.36（01・19・20・23。反射・逆光・シズルが平板）、detail 0.38（03・11。グランジが出ない）、texture 0.43（03・05・16 oil / photo・20）
  - enhance の効き: 85 問中 54 が引き分けで、raw のまま安定して出る。下げたのは texture −0.18（01・02・09・16 photograph・20 で enhanced が負け。質感の描写語が CG 寄りにする）、layout（21）、skin（09。中年の指定が 60 代に寄る）、text（23）、light（10・09・13・23）。上げたのは context（02・17）、organic（12）、detail（03）、culture（18）、style（06・16 oil）で、場面の補完には効く。enhanced が全観点で負けた問題用紙は 16 photograph
  - 基準モデルとの差: 引き分けは 15 アイソメトリック（全観点）、22 余白の商品写真（全観点）、16 anime（style・texture）、12 キツネ（texture・light）、14 POV の手指、21 ポスターの文字に出た。情報量が少ない題材（アイソメ・フラット・アニメ・余白）と、人が見慣れていない自然物では差が小さい。写実の質感・光・肌（texture 0.11、light 0.09、skin 0.00）と場面の補完（context 0.00）は基準に遠い

## スキル改善候補

- 対応済み（v1.1.0、`tasks/krea-2-turbo/issues/02`）: texture・light・skin — パレット文・仕上げ語・soft/even 既定・年齢の手がかりをやめて解消
- style / anatomy: t2i-16 photograph — v1.1.0 でも enhanced が負ける（n=1）。写真画風で「framed from the knees up」と背景ボケの指定が姿勢を崩している可能性
- light: t2i-23 — 構造を保った軽い磨きでも raw に負ける（n=1）。omnibus は raw のままでよい可能性
- layout: t2i-21 — ポスターは指示で改善しない（判定者の判断で課題にしない）

## Enhanced prompts

`run_t2i.py` がここから enhanced プロンプトを読む。`### <id>` 見出しと ` ```text ` ブロックの形を変えない。

スキル v1.1.0（パレット文・仕上げ語をやめ、光を光源と硬さで書く）で書き直したもの: 01・02・09・10・13・16 photograph・20・23。ほかは v1.0.0。再判定は `tasks/krea-2-turbo/issues/02`。

### t2i-01 雨の夜の路地（短い指示での補完力）

問題用紙: `../../t2i/01-short-rainy-alley.md`

Enhanced prompt:

```text
A photograph of a narrow city alley on a rainy night, seen straight down its length at eye level. Rain-soaked asphalt, patched and cracked, fills the lower half of the frame, and brick walls stained with damp and old grime rise close on both sides. A single street lamp on the left throws hard white highlights across the wet ground and a long streak of reflection toward the camera, while a small sign further down on the right adds a second, cooler reflection. Rain streaks show in the lamplight, and the far end of the alley falls into darkness and drifting mist.
```

### t2i-02 老いた漁師の肖像（短い指示での補完力）

問題用紙: `../../t2i/02-short-old-fisherman.md`

Enhanced prompt:

```text
An editorial portrait photograph of an elderly fisherman, framed from the chest up. Deep weather lines cross his sun-darkened face and a short gray beard covers his jaw; he wears a faded knit cap and a creased, salt-stained oilskin jacket with the collar turned up. Behind him a harbor with moored wooden boats falls out of focus. Low sun from the front-left rakes across his face so that each line casts its own small shadow, and it throws hard highlights off the wet folds of the jacket.
```

### t2i-03 市場の屋台（長い指示への忠実さ: 数と順序）

問題用紙: `../../t2i/03-long-market-stall.md`

Enhanced prompt:

```text
A photograph of a wooden market stall seen straight on at counter height. Exactly three wicker baskets stand in a row on the counter: the left basket is full of red apples, the middle basket full of green pears, and the right basket full of yellow lemons. A handwritten chalkboard sign leans against the front of the counter on the right side, and a red-and-white striped awning stretches across the top of the frame behind the stall. Soft morning daylight from the left picks out the weave of the baskets and the grain of the wood, with the fruit colors bright against the natural brown.
```

### t2i-04 ベンチの三人（長い指示への忠実さ: 属性の結び付け）

問題用紙: `../../t2i/04-long-three-friends.md`

Enhanced prompt:

```text
A photograph of exactly three young adults sitting side by side on a wooden park bench, framed from the knees up at eye level. The person on the left wears a yellow raincoat and holds a closed black umbrella upright between the knees; the person in the middle wears a blue denim jacket and holds an open paperback book in both hands; the person on the right wears a green hoodie and holds a white paper coffee cup. All three look down at the book in the middle person's hands. Green park trees fall softly out of focus behind them under even, overcast daylight.
```

### t2i-05 カフェの看板（英語テキスト）

問題用紙: `../../t2i/05-text-en-cafe-sign.md`

Enhanced prompt:

```text
A photograph of a small cafe storefront seen straight on from across the sidewalk. Above the glass door, a wooden sign reads "Blue Heron Coffee" in white serif letters centered across its width. To the left of the entrance, a small chalkboard on an easel reads "Open 7am – 4pm" in white handwritten chalk lettering. The facade is painted deep teal with brass door hardware, and potted plants stand on either side of the door. Late afternoon sunlight from the right warms the wood and lays soft shadows across the sidewalk.
```

### t2i-06 ラーメン店のメニュー（日本語テキスト）

問題用紙: `../../t2i/06-text-ja-ramen-menu.md`

Enhanced prompt:

```text
A photograph of a ramen shop menu board mounted on a plaster wall, seen straight on. The cream-colored board carries two lines of black brush-style characters: the first line reads "本日のおすすめ" in medium size, and the second line below it reads "味噌ラーメン ¥900" in larger characters. A thin dark wooden frame surrounds the board. Warm tungsten light from the upper left gives the cream surface a gentle gradient and reveals its paper texture.
```

### t2i-07 空中のスケートボーダー（人体・動きのあるポーズ）

問題用紙: `../../t2i/07-pose-skateboard-air.md`

Enhanced prompt:

```text
An action photograph of a skateboarder suspended in mid-air above a concrete half-pipe, shot from a low angle at the lip of the ramp. The rider's knees are tucked, one hand grips the middle of the board's edge, and the other arm reaches out for balance, eyes on the landing below. The curved gray wall of the half-pipe fills the lower part of the frame and a clear blue sky fills the rest. Hard midday sunlight from the upper right throws a sharp shadow of the rider onto the concrete and freezes every detail of the motion.
```

### t2i-08 リフトする二人のダンサー（人体の絡みと表情）

問題用紙: `../../t2i/08-pose-two-dancers.md`

Enhanced prompt:

```text
A photograph of two adult dancers in a bright rehearsal studio. One dancer lifts the other at the waist; the lifted dancer's arms stretch outward and one leg extends behind, and both wear wide joyful smiles and simple practice clothes. A wide wall mirror behind them reflects their backs and the wooden floor, with a barre running along the glass. Soft daylight from tall windows on the left fills the room and leaves gentle shadows on the floor, framed from the front at chest height so the full lift is visible.
```

### t2i-09 驚いた顔のクローズアップ（ショット: クローズアップ＋表情）

問題用紙: `../../t2i/09-closeup-surprised-face.md`

Enhanced prompt:

```text
A close-up photograph of a middle-aged woman's face filling the frame with a surprised expression: eyes wide open, eyebrows raised, and mouth slightly open. Her skin keeps its natural texture, sharp in focus, with faint creases where the expression pulls it. Natural window light comes from the left, bright on that cheek and forehead and falling off across the nose into a soft-edged shadow on the far side of her face, with a small window reflection in each eye.
```

### t2i-10 ガラスと鉄骨の駅コンコース（無機物: 建築）

問題用紙: `../../t2i/10-arch-station-interior.md`

Enhanced prompt:

```text
A photograph of the interior of a modern train station concourse with a sweeping curved roof of glass panels held by steel ribs, seen from floor level looking down the length of the hall so the ribs converge toward the far end. A few commuters walk across the stone floor in the middle distance, small against the height of the roof. Low morning sun comes through the glass from the upper right, so each rib casts a hard, sharply defined shadow onto the floor and the opposite wall, and the floor throws back a bright reflected streak where the light hits it.
```

### t2i-11 ビンテージバイクのエンジン（無機物: 機械）

問題用紙: `../../t2i/11-machine-motorcycle-engine.md`

Enhanced prompt:

```text
A close-up photograph of a vintage motorcycle engine resting on a wooden workshop bench. The finned aluminum cylinder sits in the center of the frame, a chrome exhaust pipe curves out from its base toward the lower left, and a polished chrome valve cover crowns the top. Oil stains, fine scratches, and worn bolt heads show the age of the metal, while the bench behind falls softly out of focus. A single work lamp from the upper left picks out the brushed aluminum and the mirror-bright chrome highlights.
```

### t2i-12 草原のキツネ（有機物: 動物）

問題用紙: `../../t2i/12-animal-red-fox.md`

Enhanced prompt:

```text
A wildlife photograph of a single red fox standing in tall golden grass and looking toward the camera with ears upright and alert amber eyes. Its rust-orange coat shows individual strands of fur, white on the chest and black on the lower legs, and its full body is visible slightly right of center with the bushy tail curving behind. The meadow behind falls into soft focus. Low golden-hour sunlight from behind and to the left rims the fur with warm light and throws long shadows through the grass.
```

### t2i-13 雨上がりの渓谷（有機物: 自然＋ショット: ワイド）

問題用紙: `../../t2i/13-nature-wide-valley.md`

Enhanced prompt:

```text
A wide landscape photograph of a forested mountain valley just after rain, seen from a high viewpoint on a trail. Conifers cover the slopes on both sides, their wet needles dark, and a river winds along the valley floor far below. In the lower-left foreground a single hiker walks along the trail, small against the scale of the valley. Low cloud drifts between the ridges and the far peaks fade into haze. Sun breaks through the clearing sky from the right, lighting the near slope and the hiker while the far side of the valley stays in cloud shadow, and the wet rocks on the trail catch its highlights.
```

### t2i-14 コーヒーを持つ自分の手（ショット: POV）

問題用紙: `../../t2i/14-pov-hands-coffee.md`

Enhanced prompt:

```text
A first-person photograph looking down at my own two hands holding a ceramic mug of coffee, thumbs resting on the rim, the mug centered in the lower half of the frame. Beyond the mug, an open laptop and a notebook lie on the desk. The upper part of the frame shows a window with raindrops on the glass and a blurred gray street outside. Soft daylight from the window ahead lights the hands and the desk surface, with the mug in sharp focus and the window softly blurred.
```

### t2i-15 アイソメトリックのワンルーム（ショット: アイソメトリック）

問題用紙: `../../t2i/15-isometric-room.md`

Enhanced prompt:

```text
A clean isometric 3D render of a small cozy studio apartment, cut away so the interior is fully visible from above at a 45-degree angle and centered on a plain white background. Inside are a single bed against the back-left wall, a wooden desk with a computer and chair against the back-right wall, a tall bookshelf beside the desk, a leafy potted plant in the front corner, and a window in the back-left wall. Soft, even studio lighting with gentle shadows gives the room a tidy miniature look with a warm wood floor.
```

### t2i-16 赤い傘の女性を4つの画風で（画風の幅）

問題用紙: `../../t2i/16-style-umbrella-bridge.md`

Enhanced prompts（variant ごと）:

- photograph

```text
A photograph of a young woman holding a red umbrella and standing on a stone bridge in light rain, framed from the knees up. The bridge's stone parapet is worn and darkened by the wet, with rain beading on its top edge, and the river and trees behind her fall out of focus. Daylight comes through thin cloud from the upper right, bright enough to put a highlight along the wet stone and the top of the umbrella and to drop a soft-edged shadow at her feet, and fine rain shows against the darker trees.
```

- 2D anime illustration

```text
A 2D anime illustration of a young woman holding a red umbrella and standing on an old stone bridge in light rain, framed from the knees up. Clean linework and soft cel shading define the figure, and rain falls as fine pale streaks across the scene. The stone bridge and the blurred green trees behind her are painted in muted tones so the red umbrella stands out, under soft overcast light.
```

- oil painting

```text
An oil painting of a young woman holding a red umbrella and standing on an old stone bridge in light rain, framed from the knees up. Visible brushstrokes and thick impasto describe the wet stone and her coat, while the river and trees behind her are loosely suggested in muted greens and grays. Soft overcast light and a restrained palette make the red umbrella the single focal point.
```

- flat vector illustration

```text
A flat vector illustration of a young woman holding a red umbrella and standing on a stone bridge in light rain, framed from the knees up. Simple geometric shapes, solid fills without gradients, and a limited palette of gray, muted green, and bright red build the scene, with rain drawn as short diagonal lines. The composition is clean and centered with generous open sky above.
```

### t2i-17 初詣の神社（日本の文化の知識）

問題用紙: `../../t2i/17-japan-shrine-newyear.md`

Enhanced prompt:

```text
A photograph of a Japanese Shinto shrine on New Year's morning. A red torii gate stands in the foreground with a thick shimenawa rope and white paper streamers across its top, and a wide stone staircase climbs to the main hall behind it. Japanese visitors in kimono, the left side folded over the right, climb the steps, and paper lanterns hang along the approach. Crisp winter morning sunlight from the right throws long shadows down the steps, with bare trees framing the scene.
```

### t2i-18 夕暮れの商店街（日本の風景の知識）

問題用紙: `../../t2i/18-japan-shotengai.md`

Enhanced prompt:

```text
A photograph of a covered shopping arcade in a Japanese town at dusk. The arched glass roof runs down the center of the frame and hanging shop signs with Japanese characters line both sides. On the right, an izakaya's red paper lantern glows beside a noren curtain; on the left, a bicycle leans against a closed metal shutter. A few pedestrians walk in the distance. Fluorescent shop lights and the warm lantern mix with the cool blue of dusk entering from the far end of the arcade.
```

### t2i-19 逆光の香水瓶（素材・質感・光: プロダクト）

問題用紙: `../../t2i/19-product-perfume-backlit.md`

Enhanced prompt:

```text
A product photograph of a clear glass perfume bottle with a polished gold cap standing on a wet black stone surface, centered in the frame. Backlight from behind the bottle glows through the liquid and refracts along its edges, while a soft rim light traces the left and right contours of the glass. The wet stone reflects the base of the bottle and its highlights, and the background falls to deep black with a faint warm halo behind the bottle.
```

### t2i-20 湯気の立つ豚骨ラーメン（素材・質感・光: フード）

問題用紙: `../../t2i/20-food-ramen-steam.md`

Enhanced prompt:

```text
A food photograph of a bowl of tonkotsu ramen on a dark wooden counter, shot from a 45-degree angle. Noodles sit submerged in the cloudy pale broth, with slices of chashu pork, a soft-boiled egg cut in half with its yolk showing, and chopped green onions arranged on top, and steam rises from the surface. Hard light from a window at the upper left puts a bright highlight on the broth's surface and the fat on the pork, lights the steam from behind, and leaves the scratched, oil-darkened wood of the counter in shadow behind the bowl.
```

### t2i-21 ジャズナイトのポスター（レイアウト: ポスターの雰囲気）

問題用紙: `../../t2i/21-poster-layout-jazz.md`

Enhanced prompt:

```text
A concert poster with a deep blue background. Across the top, a large headline reads "Midnight Jazz" in cream bold serif capitals, centered. In the center a gold silhouette of a saxophone player leans back mid-solo. Along the bottom the date "Oct 12" sits in smaller cream sans-serif letters, centered. Flat, even lighting and a subtle paper grain keep the limited palette of deep blue, cream, and gold clean and printed-looking.
```

### t2i-22 余白を残した靴の商品写真（レイアウト: 余白の効き）

問題用紙: `../../t2i/22-blank-space-product.md`

Enhanced prompt:

```text
A product photograph of a pair of white running shoes standing side by side on a plain light-gray background, placed in the lower-right quarter of the frame and seen from a slight three-quarter angle. The left two-thirds of the image is a continuous, uniform light-gray area with nothing in it, left open for text. Soft studio light from the upper left gives the shoes gentle shadows on the surface and keeps the background even.
```

### t2i-23 雨の東京の商店街（総合: 一本で多くの切り口を同時に試す）

問題用紙: `../../t2i/23-omnibus-tokyo-rain-street.md`

Enhanced prompt:

```text
Editorial portrait photograph, 35mm full-frame look, f/2.8, rainy evening in a dense Tokyo shopping street.

Foreground (near, sharply in focus): a wet steel railing and a hanging red paper lantern partially framing the left edge, and a small handwritten cafe chalkboard reading exactly "OPEN 'til 2AM" in white chalk.

Subject (mid-ground): a woman in her late 20s with short black hair, wearing a translucent yellow rain poncho over a charcoal blazer, caught mid-stride while twisting her torso to look back over her right shoulder; her left hand raises a clear umbrella, her right hand holds a paper coffee cup near her chin, and one foot is lifted off the wet pavement. Her face is lit by neon and she is laughing with her eyes half-closed.

Background (far): a crowd of forty or more blurred pedestrians with umbrellas forming a repeating pattern that recedes down the street; a row of vending machines and a rusted pedestrian bridge (inorganic); ginkgo trees with wet yellow leaves and potted plants on balconies (organic). A large illuminated billboard high on a building reads exactly "NIGHT MARKET 11.22" in bold condensed white type on red.

Lighting: mixed neon (magenta and cyan) with hard reflections in the puddles, shallow depth of field, slight motion blur only in the crowd. Photorealistic with natural skin texture; the two quoted strings are the only text in the picture.
```
