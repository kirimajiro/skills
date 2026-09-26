---
name: flux-2-klein-9b
description: Write, structure, and refine prompts for FLUX.2 [klein] 9B (Black Forest Labs' distilled 4-step model with the Qwen3-8B text encoder), including single-reference and multi-reference editing prompts that address inputs as "image 1", "image 2". Use this whenever the user mentions FLUX.2, FLUX.2 klein, klein 9B or 4B, the flux2 ComfyUI workflow, or wants prompts for a fast local model that follows structured prose, renders short quoted text, and edits images from up to four references. Also use it to hand over the lightweight system prompts for a local LLM node.
---

# FLUX.2 [klein] 9B Prompt Design

Turn the user's visual intent into a ready-to-use prompt for FLUX.2 [klein] 9B. This skill covers prompt authoring for text-to-image and image editing; image generation, model files, and workflow settings follow the user's environment. The same guidance applies to the 4B variant, which shares the architecture and editing features and differs in license (Apache 2.0) and a smaller Qwen3-4B text encoder.

## Know the model

FLUX.2 [klein] is Black Forest Labs' compact FLUX.2 model. The 9B checkpoint is a 9B rectified-flow transformer with an 8B Qwen3 text encoder, step- and guidance-distilled to 4 inference steps. These traits shape every prompt:

- **Structure over length.** The official guidance is explicit: the goal is a clear structure, not the longest prompt. Concrete detail helps; filler such as stacked quality adjectives hurts. Most prompts land at 30 to 80 words; only dense multi-subject scenes need 80 to 300.
- **Subject before environment.** Naming the subject and its action first keeps the framing on the subject; leading with the environment pulls the camera back.
- **Guidance-distilled.** The distilled checkpoint runs at guidance 1.0, so classifier-free guidance is effectively off and a negative prompt does nothing. Everything the image should contain is stated affirmatively.
- **Photographic vocabulary works.** Naming a camera body, lens, film stock, or lighting setup produces more authentic photographs than "professional photo".
- **Short quoted text.** Words to render go in straight double quotes with placement and lettering style. Short strings render well; long strings break. Brand colors can be given as hex codes.
- **Generation and editing in one model.** The open weights take zero to four reference images. Edits are written as direct instructions that name the change and state what stays unchanged.
- **Prompt following depends on prompting style.** The model card lists this as a limitation, which is why the structure below matters more than for larger models.

## Establish the task

Resolve three axes from the request:

| Axis | Choices |
| --- | --- |
| Operation | Text-to-image, single-reference edit, multi-reference composition (up to four inputs) |
| Appearance | Photograph, illustration, painting, 3D render, or another named medium; unstated means you choose one and say so |
| Complexity | Simple subject (short or medium prompt) or dense multi-subject scene (long prompt or JSON) |

For editing, inspect the available reference images and bind instructions to their visible contents. Ask only when a missing image or choice would change the whole result; otherwise pick a reasonable default and name the assumption in one line.

Preserve every fixed element the user gave: subject, counts, colors, spatial relationships, named medium, and exact display text.

## Text-to-image: structured prose

Write one paragraph of English prose in the present tense, in the official order:

1. Image type (portrait, landscape, product photograph, poster, isometric render).
2. Subject with concrete details and its action or state.
3. Location or context.
4. Style and medium.
5. Camera settings, when photographic (lens, aperture, film stock, viewpoint).
6. Lighting: source, direction, hardness, and what it does to the surfaces.
7. Colors, as the colors of things (hex codes for brand colors and posters).
8. Effects and supporting elements.

Not every slot is needed every time. Rules that matter for this model:

- **Start with the subject.** "Portrait photograph of an elderly fisherman, chest-up, weathered face …" and only then the harbor behind him.
- **Concrete descriptors, no filler.** "Rust-orange coat with individual strands of fur" beats "highly detailed beautiful fox". Drop repeated quality words entirely. The descriptors belong to elements the request already contains.
- **Avoid over-specification.** Do not invent clothing, props, colors, materials, or a fixed framing ("from the knees up", "straight on", "centered") that the request does not support, and do not add a pose, gaze, or expression it did not give. The model renders what it is told, and an invented element is the one most likely to come out broken. Get density from the state of the surfaces that are already there (worn, wet, scuffed, oil-stained), the light, and the action.
- **Colors and surfaces are physical facts, not a grade.** Name a color as the color of a thing ("a red umbrella") and a surface by its state. Do not write palette or finish sentences such as "muted sea-gray and navy tones", "deep saturated greens", or "mirror-bright chrome" for a photograph or scene; they flatten the render. Hex codes stay for brand colors and poster palettes.
- **Light has a source and contrast.** Say where the light comes from, how hard it is, and what it does to the surfaces: a hard-edged shadow on the concrete, a highlight streak on wet paint, a rim along fur. When the request leaves the light open, choose a light with direction and contrast; do not default to "overcast", "soft even", or "diffused".
- **Bind attributes to their owner and place things in the frame.** "The person on the left wears a yellow raincoat and holds a closed black umbrella"; "the upper-left area is open background".
- **Say what is there.** Turn any exclusion into the state that replaces it: "a plain light-gray backdrop fills the frame" instead of "no background clutter".
- **Photographs get camera language.** Name a lens and aperture ("85mm at f/2"), a film stock or camera when the look calls for it, and describe the light photographically.
- **Named styles get style nouns.** "2D anime illustration with clean linework and cel shading", "oil painting with thick impasto", "flat vector illustration with solid fills". A "Style: … Mood: …" note at the end is an accepted official form for a mood-driven brief.
- **Length follows complexity.** 10 to 30 words for quick concepts, 30 to 80 for most requests, 80 to 300 for multi-subject scenes. Add words only when they change the image.
- Write the prompt in English unless the user asks otherwise; keep quoted display text in its original language.

Example (specified request, "editorial portrait of an old fisherman"):

```text
Editorial portrait photograph of an elderly fisherman, chest-up. Deep wrinkles and sun-darkened skin, a short gray beard, a knit cap and an oilskin jacket with the collar turned up, the jacket creased and salt-stained from use. A harbor with moored wooden boats sits out of focus behind him. Shot on an 85mm lens at f/2, low sun from the front-left raking across his face so each wrinkle casts a small shadow and the wet folds of the jacket throw hard highlights.
```

### JSON prompting for dense scenes

For production pipelines or scenes with several subjects that need independent iteration, the official docs offer a structured JSON form. Use it only when the user works in a pipeline or asks for it; natural prose is better for exploration. Keys: `scene`, `subjects` (each with `description`, `position`, `action`), `style`, `color_palette` (hex codes), `lighting`, `mood`, `background`, `composition`, `camera` (angle, lens, depth of field).

## Rendered text

Give the exact string in straight double quotes, then its placement relative to visible elements, its size in the hierarchy (large headline, medium subheading, small body copy), its color, and its lettering style (serif, sans-serif, script, display, neon, chalk, raised chrome). Put the text specification early in the prompt. Keep each string short and describe separate lines separately. Brand colors can be hex codes.

```text
Concert poster design on a deep blue background. Large headline text "Midnight Jazz" across the top in cream bold serif capitals, centered. In the middle, a gold silhouette of a saxophone player in profile leaning back mid-solo. Small date text "Oct 12" at the bottom in cream sans-serif letters, centered. Limited palette of deep blue, cream #F2E8D5, and gold #C9A227, subtle paper grain, flat even lighting.
```

For a region reserved for later typesetting, describe it as a continuous area of one color with its size and position in the frame.

## Photography treatment

Name the genre (editorial, product, street, wildlife, macro), the framing and viewpoint, the lens and aperture, where focus sits, the light source with its direction and hardness, the state of the surfaces (wear, wetness, dust, fingerprints), and a film stock when the look calls for it. For product shots, state the supporting surface and how the object meets it.

## Illustration and painting treatment

Name the illustration type or painting medium and the marks that define it: line weight and shading method for illustration, brushwork and impasto for painting, solid fills and a limited palette for flat vector, cutaway and viewing angle for isometric renders. Keep character proportions, costume, palette, and background treatment stylistically consistent.

## Single-reference editing

Write a direct instruction that names the change, then states what stays the same. The official examples are short: "Change the shirt color to red", "Replace the background with a sunset beach", "Turn this into an oil painting". Add a preservation clause such as "keep everything else unchanged" whenever the request touches part of the image.

- Refer to the input as "the image" or "image 1".
- Identify the target by location or visible annotation; describe the finished appearance of the edited region.
- Style transfer names the target medium concretely ("oil painting with thick, textured brushstrokes") and keeps content and layout.
- A new picture of the subject (character sheet, close-up, new setting) keeps the face, hairstyle, and clothing and actively describes the new framing.
- Colors and materials can be hex codes; text edits name the element and the new string in quotes.
- Avoid "make it better", "enhance", "fix": they carry no instruction.

```text
Dress the person in image 1 in the mustard-yellow wool overcoat from image 2, keeping its cut, large dark buttons, and fabric. Keep the person's face, hairstyle, pose, hands, background, and framing from image 1 unchanged. Fit the coat to the pose with natural folds and shading that match the existing light.
```

## Multi-reference composition

Address inputs as "image 1", "image 2", up to "image 4" in the order they are supplied, and give each a role: which image is the base whose composition survives, and what is taken from each other image (garment, object, pose, style, location). Say what is preserved from the base ("Keep the pose, lighting, and overall composition of image 1 unchanged"). Match transferred items to the base with scale, folds, contact shadows, and light direction.

```text
Use image 2 as the location. Place the person from image 1 standing on the left third of the scene, keeping their face, hairstyle, and clothing unchanged. Match the lighting and perspective of image 2 with a soft contact shadow on the ground.
```

## Workflow settings, kept out of the prompt

The distilled 9B checkpoint is documented at 4 steps and guidance 1.0; the base checkpoint at about 50 steps and guidance 4.0. Give resolution, aspect ratio, steps, guidance, and reference count as a separate settings note; the prompt describes the picture only.

## Deliver and refine

Provide a copy-ready prompt in the requested format, a role map for multi-reference work, and a settings note when useful. Label authored examples as starting points; describe generation results only after seeing them.

Before delivery, check:

- The subject and its action come first, before the environment.
- Image type, medium, and style are stated once and match the request.
- Every element the user named is present with its own attributes; nothing was added that the request does not support: no invented clothing, props, colors, or framing.
- Colors belong to things and light has a source and contrast; there is no palette or finish sentence.
- Each sentence describes something present; no negations.
- Quoted display text is short, matches the user's characters exactly, and carries placement and lettering style.
- Edits name the change and what stays unchanged; references are addressed as "image N" with roles.
- Size, aspect ratio, steps, and guidance are in the settings note, not in the prompt.

During iteration, follow the official loop: start simple, check what came out right and wrong, change one important detail at a time with the seed fixed.

## Lightweight variants for local LLM nodes

When the user wants a prompt rewriter inside ComfyUI or another workflow tool on a local general-purpose LLM (27B-class; smaller models do not follow the instructions reliably), hand over the matching sibling file instead of this skill. Each is a complete English system prompt with no frontmatter, pasted as-is into the LLM node. It takes the user's rough request as the user message and returns the finished prompt only.

| File | Mode |
| --- | --- |
| `SKILL-lite-t2i.md` | Text-to-image |
| `SKILL-lite-i2i.md` | Single-reference editing and multi-reference composition (up to four inputs) |

Keep them in step with this skill when it changes.

## Sources and scope

Official sources establish the variants and settings, the editing capability and reference limit, the structured-prose guidance, the text-rendering rules, and the "image N" editing convention. The treatments above are practical authoring guidance; judge them by the generated results.

- [Announcement: FLUX.2 [klein]](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence)
- [Model card: FLUX.2-klein-9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B)
- [Model card: FLUX.2-klein-base-9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-base-9B)
- [Official repository](https://github.com/black-forest-labs/flux2)
- [Prompting guide: basics](https://docs.bfl.ml/guides/prompting_unified_basics)
- [Prompting guide: building a good prompt](https://docs.bfl.ml/guides/prompting_unified_building)
- [Prompting guide: style, aesthetics and text](https://docs.bfl.ml/guides/prompting_unified_style)
- [Prompting guide: typography and design](https://docs.bfl.ml/guides/usecases_t2i_typography_design)
- [Prompting guide: JSON structured prompting](https://docs.bfl.ml/guides/usecases_t2i_json_prompting)
- [Prompting guide: editing overview, single and multi reference](https://docs.bfl.ml/guides/prompting_editing_overview)
- [ComfyUI tutorial: FLUX.2 Klein](https://docs.comfy.org/tutorials/flux/flux-2-klein)
