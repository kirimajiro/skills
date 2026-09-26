# flux-2-klein-9b — t2i 判定シート

- 基準モデル: GPT-Image 2.5
- 判定日: 2026-09-24（vs krea-2-turbo）、2026-09-26（enhanced vs raw、vs 基準）
- 判定者: リポジトリ所有者
- ワークフロー設定（steps / guidance / sampler / 解像度）: steps 8 / cfg 1 / euler / Flux2Scheduler / 約 1 MP（1:1 1024x1024、3:2 1216x816、2:3 816x1216、3:4 864x1152、16:9 1344x752）。seed 1（`_local/flux-2-klein-9b/t2i/run.json`）
- セッション（`_local/pairwise/`、git 管理外。各 85 問）:
  - `ab_krea-2-turbo_flux-2-klein-9b_20260924-1600` — vs krea-2-turbo（enhanced 同士。flux は B 側なので勝敗を反転）。引き分け 34
  - `raw-enh_flux-2-klein-9b_20260924-1715` — enhanced vs raw。約 10 分、引き分け 41
  - `vs-baseline_flux-2-klein-9b_gpt-image-2-5_20260924-1715` — vs GPT-Image 2.5 raw。引き分け 10

## 観点別プロファイル

セルは flux-2-klein-9b の勝率（勝 / 分 / 負、n）。引き分けは 0.5 勝、`*` は n が 3 未満。

| aspect | vs krea-2-turbo | raw vs enhanced | vs baseline (gpt-image-2-5) |
|---|---|---|---|
| texture 質感の本物感 | 0.57 (5/6/3, n=14) | 0.61 (6/5/3, n=14) | 0.04 (0/1/13, n=14) |
| detail ディテールとグランジ | 0.62 (2/1/1, n=4) | 0.25 (1/0/3, n=4) | 0.00 (0/0/4, n=4) |
| text 文字の正確さ | 0.50 (1/3/1, n=5) | 0.50 (0/5/0, n=5) | 0.10 (0/1/4, n=5) |
| layout 文字とレイアウト | 0.38 (0/3/1, n=4) | 0.50 (0/4/0, n=4) | 0.25 (0/2/2, n=4) |
| structure 構造物とパース | 0.12 (0/1/3, n=4) | 0.75 (2/2/0, n=4) | 0.12 (0/1/3, n=4) |
| anatomy 人体・手指・ポーズ | 0.28 (2/1/6, n=9) | 0.50 (2/5/2, n=9) | 0.00 (0/0/9, n=9) |
| skin 肌と表情 | 0.25 (1/0/3, n=4) | 0.25 (0/2/2, n=4) | 0.00 (0/0/4, n=4) |
| context 補完の文脈適合 | 0.69 (4/3/1, n=8) | 0.31 (2/1/5, n=8) | 0.00 (0/0/8, n=8) |
| style 画風の成立 | 0.36 (2/1/4, n=7) | 0.50 (1/5/1, n=7) | 0.00 (0/0/7, n=7) |
| organic 有機物の自然さ | 0.50 (1/0/1, n=2 *) | 0.25 (0/1/1, n=2 *) | 0.00 (0/0/2, n=2 *) |
| composition 構図とショット | 0.50 (0/8/0, n=8) | 0.56 (2/5/1, n=8) | 0.19 (0/3/5, n=8) |
| light 光と素材 | 0.64 (5/4/2, n=11) | 0.68 (6/3/2, n=11) | 0.09 (0/2/9, n=11) |
| culture 文化的な正しさ | 0.50 (1/1/1, n=3) | 0.50 (1/1/1, n=3) | 0.00 (0/0/3, n=3) |
| fidelity 要素の揃い方 | 0.50 (0/2/0, n=2 *) | 0.50 (0/2/0, n=2 *) | 0.00 (0/0/2, n=2 *) |

## enhance の効き

- 上げた観点: structure (+0.25, n=4), light (+0.18, n=11), texture (+0.11, n=14), composition (+0.06, n=8)
- 下げた観点: detail (-0.25, n=4), organic (-0.25, n=2), skin (-0.25, n=4), context (-0.19, n=8)
- 変わらない観点: text (n=5), layout (n=4), anatomy (n=9), style (n=7), culture (n=3), fidelity (n=2)

再判定（スキル v1.1.0、`raw-enh_flux-2-klein-9b_20260927-0041`、書き直した 10 枚が入る 13 問題・41 設問）:

- 同じ 10 枚での enhanced 勝率: context 0.00 → 0.70（3/1/1, n=5）、detail 0.00 → 0.83（n=3）、skin 0.17 → 0.67（n=3）、style 0.50 → 0.75（n=4）
- 判定者の雑感: どうしても脂っこい感じの絵作りになる傾向がある。enh してもしなくても、破綻しやすいのが難点。色々描き込みたい場合には使えるモデルかもしれないが、Krea 2 と比較して積極的に画質面で Flux.2 [klein] を使う理由は特にないと思う
- enhanced が負けた残り: 05（text・context）、07（anatomy・composition）、09（skin・texture）

## 感想戦

- 判定者の雑感（セッションの notes）:
  - vs krea-2-turbo: そこまで大差は無いが、クローズアップやパースの正確さになるとBの方がどうしても劣って見える。（B = flux）
  - enhanced vs raw: flux-2-klein-9bは想像力が豊かで、それによってより自然なスタイルや構図が出ることがあるが、指示文に無いので出したもの自体が破綻しているケースが多い。例えば雨の窓の外にある車は途切れている様に見えるし、公園の3人は傘の縮尺がおかしい、バイクのエンジンも構造として変、などです。
  - vs 基準: （雑感欄は空）
- ヒアリング（判定者の言葉）:
  - 強い観点の理由（vs krea、krea 側の感想戦から）: flux はパース・クローズアップが崩れる。krea は光が平板で、グランジ（汚れ・経年）が出ない
  - 基準との差: krea と同じで、情報量の少ない題材だけ差が小さい。flux はアニメ・フラットでも基準に負ける（krea は引き分けた）
  - 用途について: 基本的に生成性能でローカル vs フロンティアで使い分けることはしない（プロジェクトに応じた使い分け）。あくまで vs としたのはローカルモデルの力量を測るため
- Claude の整理:
  - 得意（vs krea）: context 0.69（t2i-01・03・05・10 で勝ち。場面の書き込みが豊か）、light 0.64（01・17・19・20・23。反射・逆光・シズル）、detail 0.62（03・11。グランジが出る）、texture 0.57（03・05・16 oil / photo・20）。写真らしい質感と場面の想像力が krea に勝る
  - 不得意（vs krea）: structure 0.12（08 鏡像・10 駅・11 エンジンで負け）、anatomy 0.28（07・08・14・16 anime / flat / oil）、skin 0.25（02・08・09）、style 0.36（06 筆文字・15 3D レンダー・16 anime / flat）。パースとクローズアップで崩れ、指示にない要素を足すときにその要素自体が破綻する（14 の窓の外の車、04 の傘の縮尺、11 のエンジン構造）
  - enhance の効き: 85 問中 41 が引き分け。上げたのは structure（08・15）、light（01・10・17・18・19・20）、texture（01・11・16 anime / photo・19・20）、composition（19・23）で、光と質感の指示は効く。下げたのは context −0.19（02・03・04・05・17 で enhanced が負け。enhance で足した要素が破綻する）、detail（03・07・11）、skin（02・09）、organic（13）。enhanced が全観点で負けた問題用紙は 03 市場の屋台と 13 渓谷、全観点で勝ったのは 01・16 photograph・19
  - 基準モデルとの差: 引き分けは 05 カフェの文字・レイアウト、15 アイソメトリック（composition・structure）、22 余白の商品写真（全観点）、07・20 の構図、17 の光に出た。krea が引き分けた 16 anime・12 キツネ・14 POV は flux は負け。写実の質感・光（texture 0.04、light 0.09）と人物（anatomy・skin 0.00）は基準に遠く、情報量の少ない題材だけ差が小さい

## スキル改善候補

- 対応済み（v1.1.0、`tasks/flux-2-klein-9b/issues/03`）: context・detail・skin — 依頼にない小物・服・色・構図の発明をやめ、光を光源と硬さで書き、パレット文をやめて解消
- skin / texture: t2i-09 — レンズ・絞りの数値を付けた肌のクローズアップは v1.1.0 でも enhanced が負ける（2 回連続）。数値をやめる案は未検証
- text / context: t2i-05 — 看板の文字は raw のほうが正確（n=1）
- anatomy / composition: t2i-07 — 空中のポーズとローアングルは raw のほうが成立（n=1）

## Enhanced prompts

`run_t2i.py` がここから enhanced プロンプトを読む。`### <id>` 見出しと ` ```text ` ブロックの形を変えない。

スキル v1.1.0（依頼にない小物・服・色・構図を発明しない、光は光源と硬さで書く、パレット文をやめる）で書き直したもの: 02・03・04・05・07・09・11・13・16 anime・17。ほかは v1.0.0。再判定は `tasks/flux-2-klein-9b/issues/03`。

### t2i-01 雨の夜の路地（短い指示での補完力）

問題用紙: `../../t2i/01-short-rainy-alley.md`

Enhanced prompt:

```text
Street photograph of a narrow city alley at night in heavy rain, wet asphalt reflecting a single warm street lamp on the left and a small blue shop sign farther down on the right. Brick walls close in on both sides with a fire escape and stacked crates near the right wall. Shot on a 35mm lens at eye level looking straight down the alley, thin mist softening the far end. Deep blue-black shadows, amber highlights, muted brick red.
```

### t2i-02 老いた漁師の肖像（短い指示での補完力）

問題用紙: `../../t2i/02-short-old-fisherman.md`

Enhanced prompt:

```text
Editorial portrait photograph of an elderly fisherman, chest-up. Deep wrinkles and sun-darkened skin, a short gray beard, a knit cap and an oilskin jacket with the collar turned up, the jacket creased and salt-stained from use. A harbor with moored wooden boats sits out of focus behind him. Shot on an 85mm lens at f/2, low sun from the front-left raking across his face so each wrinkle casts a small shadow and the wet folds of the jacket throw hard highlights.
```

### t2i-03 市場の屋台（長い指示への忠実さ: 数と順序）

問題用紙: `../../t2i/03-long-market-stall.md`

Enhanced prompt:

```text
Photograph of a wooden market stall with exactly three wicker baskets in a row on the counter: the left basket holds red apples, the middle basket holds green pears, and the right basket holds yellow lemons. A handwritten chalkboard sign leans against the counter on the right. Behind the stall a red-and-white striped awning spans the top of the frame. The counter's wood is scuffed and darkened where hands and crates have rubbed it, and the wicker shows loose, frayed strands. Morning sun from the left throws the baskets' shadows across the counter and lights the fruit from the side.
```

### t2i-04 ベンチの三人（長い指示への忠実さ: 属性の結び付け）

問題用紙: `../../t2i/04-long-three-friends.md`

Enhanced prompt:

```text
Candid photograph of exactly three young adults sitting side by side on a park bench. The person on the left wears a yellow raincoat and holds a closed black umbrella. The person in the middle wears a blue denim jacket and reads a paperback book. The person on the right wears a green hoodie and holds a white paper coffee cup. All three look at the book. Park trees stand out of focus behind them. Shot on a 35mm lens, daylight from the upper left, bright on the yellow raincoat and leaving a shadow under the bench.
```

### t2i-05 カフェの看板（英語テキスト）

問題用紙: `../../t2i/05-text-en-cafe-sign.md`

Enhanced prompt:

```text
Storefront photograph of a small cafe. Above the door, a wooden sign reads "Blue Heron Coffee" in white serif letters. By the entrance, a smaller chalkboard reads "Open 7am – 4pm" in white handwritten chalk. The wooden sign is weathered, its paint worn thin at the edges, and the doorstep is scuffed. Late afternoon sun from the right rakes across the facade, leaving a hard shadow line beside the door frame and a bright edge on the sign's lettering.
```

### t2i-06 ラーメン店のメニュー（日本語テキスト）

問題用紙: `../../t2i/06-text-ja-ramen-menu.md`

Enhanced prompt:

```text
Photograph of a ramen shop menu board mounted on a plaster wall, straight on. The cream board carries two lines of black brush-style lettering: the first line reads "本日のおすすめ" in medium size, the second line below reads "味噌ラーメン ¥900" in larger characters. A thin dark wooden frame surrounds the board. Warm tungsten light from the upper left, a gentle gradient across the cream surface with visible paper texture.
```

### t2i-07 空中のスケートボーダー（人体・動きのあるポーズ）

問題用紙: `../../t2i/07-pose-skateboard-air.md`

Enhanced prompt:

```text
Action sports photograph of a skateboarder in mid-air above a concrete half-pipe, one hand gripping the edge of the board, knees tucked, the other arm out for balance, shot from a low angle at the lip of the ramp. The concrete is scuffed and streaked with wheel marks and the board's grip tape is worn. Bright midday sun from the upper right throws a hard, sharp-edged shadow of the skater onto the concrete and catches the edge of the board.
```

### t2i-08 リフトする二人のダンサー（人体の絡みと表情）

問題用紙: `../../t2i/08-pose-two-dancers.md`

Enhanced prompt:

```text
Photograph of two adult dancers in a bright rehearsal studio, one lifting the other at the waist, the lifted dancer's arms spread wide and one leg extended behind, both laughing with wide joyful smiles. Simple gray and black practice clothes. A wide wall mirror behind them reflects their backs and the wooden floor, a barre running along it. Soft daylight from tall windows on the left, gentle shadows on the floor, 35mm lens at mid-distance.
```

### t2i-09 驚いた顔のクローズアップ（ショット: クローズアップ＋表情）

問題用紙: `../../t2i/09-closeup-surprised-face.md`

Enhanced prompt:

```text
Close-up portrait photograph of a middle-aged woman's face filling the frame with a surprised expression: eyes wide open, eyebrows raised, mouth slightly open. Her skin keeps its natural texture, sharp in focus, with creases where the expression pulls it. Shot on an 85mm lens at f/2.8. Natural window light from the left, bright on that cheek and forehead and falling off across the nose into a soft-edged shadow on the far side of her face, with a small window reflection in each eye.
```

### t2i-10 ガラスと鉄骨の駅コンコース（無機物: 建築）

問題用紙: `../../t2i/10-arch-station-interior.md`

Enhanced prompt:

```text
Architectural photograph of a modern train station concourse interior with a sweeping curved roof of glass panels held by white steel ribs. Wide-angle 24mm lens from floor level looking down the length of the hall, the ribs converging toward the far end. A few commuters walk across the polished stone floor in the middle distance, small against the height of the roof. Morning sunlight streams through the glass from the upper right, laying long bright bands across the floor. White, pale gray, warm morning gold.
```

### t2i-11 ビンテージバイクのエンジン（無機物: 機械）

問題用紙: `../../t2i/11-machine-motorcycle-engine.md`

Enhanced prompt:

```text
Close-up photograph of a vintage motorcycle engine on a workshop bench, showing the finned cylinder in the center, the exhaust pipe curving away from its base, and chrome parts on top. Oil stains, fine scratches, and worn bolt heads show its age, with grime packed between the cooling fins and dull patches on the chrome. A single work lamp from the upper left puts hard highlights on the chrome and leaves deep shadows between the fins.
```

### t2i-12 草原のキツネ（有機物: 動物）

問題用紙: `../../t2i/12-animal-red-fox.md`

Enhanced prompt:

```text
Wildlife photograph of a single red fox standing in tall golden grass, facing the camera with ears upright and alert amber eyes. Rust-orange coat with individual strands of fur, white chest, black lower legs, bushy tail curving behind, full body slightly right of center. Telephoto 300mm lens with the meadow falling into soft focus. Low golden-hour sun from behind and to the left rims the fur with warm light and throws long shadows through the grass.
```

### t2i-13 雨上がりの渓谷（有機物: 自然＋ショット: ワイド）

問題用紙: `../../t2i/13-nature-wide-valley.md`

Enhanced prompt:

```text
Wide landscape photograph of a forested mountain valley just after rain, taken from a high viewpoint on a trail, with a river winding along the valley floor far below and a single hiker walking the trail in the lower-left foreground, small against the valley. Wet conifers cover both slopes, low cloud drifts between the ridges, and the far peaks fade into haze. 24mm lens. Sun breaking through from the right lights the near slope and the hiker while the far side of the valley stays in cloud shadow, and the wet rocks on the trail catch its highlights.
```

### t2i-14 コーヒーを持つ自分の手（ショット: POV）

問題用紙: `../../t2i/14-pov-hands-coffee.md`

Enhanced prompt:

```text
First-person point-of-view photograph looking down at my own two hands holding a white ceramic mug of coffee, thumbs on the rim, the mug centered in the lower half of the frame. Beyond it an open laptop and a lined notebook with a pen rest on a light oak desk. The upper frame shows a window with raindrops on the glass and a blurred gray street outside. Soft daylight from the window ahead lights the hands and the desk.
```

### t2i-15 アイソメトリックのワンルーム（ショット: アイソメトリック）

問題用紙: `../../t2i/15-isometric-room.md`

Enhanced prompt:

```text
Isometric 3D render of a small cozy studio apartment, cut away so the whole interior is visible from above at a 45-degree angle, centered on a plain white background. A single bed with a blue blanket against the back-left wall, a wooden desk with a computer monitor and chair against the back-right wall, a tall bookshelf full of colorful books beside the desk, a leafy potted plant in the front corner, and a window on the back-left wall. Warm oak floor, soft even studio lighting with gentle shadows, clean miniature look.
```

### t2i-16 赤い傘の女性を4つの画風で（画風の幅）

問題用紙: `../../t2i/16-style-umbrella-bridge.md`

Enhanced prompts（variant ごと）:

- photograph

```text
Photograph of a young woman holding a red umbrella, standing on an old stone bridge in light rain, framed from the knees up. Beige trench coat, face turned slightly away from the camera. Raindrops dot the wet stone parapet; the river and trees behind her fall softly out of focus. Shot on a 50mm lens at f/2, overcast daylight, soft even light, with the red umbrella as the strongest color against gray stone and muted green.
```

- 2D anime illustration

```text
2D anime illustration of a young woman holding a red umbrella and standing on a stone bridge in light rain. Clean linework and cel shading, rain drawn as fine pale streaks, the stone of the bridge drawn with a few worn, darker blocks where it is wet. Trees behind her are simplified into soft shapes. Light comes from the upper left through the clouds, with a cel-shaded shadow under the umbrella across her shoulders and a highlight along its top edge.
```

- oil painting

```text
Oil painting of a young woman holding a red umbrella, standing on an old stone bridge in light rain, framed from the knees up. Visible brushstrokes and thick impasto describe her beige coat and the wet stone; the river and trees behind are loosely suggested in muted greens and grays. Soft overcast light and a limited palette make the red umbrella the focal point.
```

- flat vector illustration

```text
Flat vector illustration of a young woman holding a red umbrella, standing on a stone bridge in light rain, framed from the knees up. Simple geometric shapes and solid flat fills, a limited palette of gray, muted green, beige, and bright red. Rain drawn as short diagonal lines, a clean composition with generous open sky.
```

### t2i-17 初詣の神社（日本の文化の知識）

問題用紙: `../../t2i/17-japan-shrine-newyear.md`

Enhanced prompt:

```text
Travel photograph of a Japanese Shinto shrine on New Year's morning. A red torii gate stands in the foreground and people in kimono climb the stone steps behind it, each kimono folded left over right; paper lanterns hang along the approach. The torii's paint is worn at the base and the stone steps are dark with morning damp. Low winter sun from the right throws long, hard-edged shadows of the visitors down the steps and lights the lanterns from the side.
```

### t2i-18 夕暮れの商店街（日本の風景の知識）

問題用紙: `../../t2i/18-japan-shotengai.md`

Enhanced prompt:

```text
Street photograph of a covered shopping arcade in a Japanese town at dusk. The arched glass roof runs down the center of the frame and hanging shop signs with Japanese characters line both sides. On the right an izakaya's red paper lantern glows beside a noren curtain; on the left a bicycle leans against a closed metal shutter. A few pedestrians walk in the distance. Fluorescent shop light and the warm lantern mix with cool blue dusk from the far end, 35mm lens at eye level.
```

### t2i-19 逆光の香水瓶（素材・質感・光: プロダクト）

問題用紙: `../../t2i/19-product-perfume-backlit.md`

Enhanced prompt:

```text
Product photograph of a clear glass perfume bottle with a polished gold cap standing on a wet black stone surface, centered. Backlight glows through the pale amber liquid and refracts along its faceted edges while a soft rim light traces the left and right contours of the glass. The wet stone mirrors the base and the highlights. 100mm macro lens, deep black background fading to a faint warm halo behind the bottle.
```

### t2i-20 湯気の立つ豚骨ラーメン（素材・質感・光: フード）

問題用紙: `../../t2i/20-food-ramen-steam.md`

Enhanced prompt:

```text
Food photograph of a bowl of tonkotsu ramen on a dark wooden counter, shot from a 45-degree angle. Creamy pale broth with a nest of noodles, two slices of chashu pork, a soft-boiled egg cut in half with an orange yolk, and a scattering of chopped green onions, thin steam rising from the surface. Wooden chopsticks rest on the rim. Warm light from the upper left brings out the glossy sheen of the broth and the fat on the pork; the background falls into soft dark focus, 50mm lens.
```

### t2i-21 ジャズナイトのポスター（レイアウト: ポスターの雰囲気）

問題用紙: `../../t2i/21-poster-layout-jazz.md`

Enhanced prompt:

```text
Concert poster design on a deep blue background. Large headline text "Midnight Jazz" across the top in cream bold serif capitals, centered. In the middle, a gold silhouette of a saxophone player in profile leaning back mid-solo. Small date text "Oct 12" at the bottom in cream sans-serif letters, centered. Limited palette of deep blue #1B2A49, cream #F2E8D5, and gold #C9A227, subtle paper grain, flat even lighting for a printed look.
```

### t2i-22 余白を残した靴の商品写真（レイアウト: 余白の効き）

問題用紙: `../../t2i/22-blank-space-product.md`

Enhanced prompt:

```text
Product photograph of a pair of white running shoes standing side by side on a plain light-gray background, placed in the lower-right quarter of the frame and viewed from a slight three-quarter angle. The left two-thirds of the image is a continuous, uniform light-gray area kept open for text. Soft studio light from the upper left, gentle shadows under the shoes, 50mm lens.
```

### t2i-23 雨の東京の商店街（総合: 一本で多くの切り口を同時に試す）

問題用紙: `../../t2i/23-omnibus-tokyo-rain-street.md`

Enhanced prompt:

```text
Editorial portrait photograph of a woman in her late twenties with short black hair, caught mid-stride on a rainy evening in a dense Tokyo shopping street, twisting her torso to look back over her right shoulder and laughing with her eyes half-closed. She wears a translucent yellow rain poncho over a charcoal blazer; her left hand raises a clear umbrella, her right hand holds a paper coffee cup near her chin, and one foot is lifted off the wet pavement. In the sharp near foreground, a wet steel railing and a hanging red paper lantern partially frame the left edge, and a small handwritten cafe chalkboard reads "OPEN 'til 2AM" in white chalk. Far behind her, a crowd of forty or more blurred pedestrians with umbrellas forms a repeating pattern receding down the street, beside a row of vending machines and a rusted pedestrian bridge; ginkgo trees with wet yellow leaves and potted plants on balconies line the street. A large illuminated billboard high on a building reads "NIGHT MARKET 11.22" in bold condensed white type on red. Shot on a 35mm full-frame lens at f/2.8 with shallow depth of field; the foreground and the woman are sharp while the crowd carries slight motion blur. Mixed magenta and cyan neon lights her face and reflects in the puddles, her skin keeps natural texture, and the two quoted strings are the only text in the picture.
```
