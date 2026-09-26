---
name: krea-2-turbo
description: Write, expand, and refine text-to-image prompts for Krea 2 Turbo (Krea's open-weights 12B model) as dense natural-language prose with a single committed style direction. Use this whenever the user mentions Krea 2, Krea 2 Turbo, Krea 2 Raw, the krea2 ComfyUI workflow, or wants prompts for an aesthetic-first, style-flexible image model, including exploratory prompting, photography, illustration, painting, and posters with rendered text. Also use it to hand over the lightweight system prompt for a local LLM node.
---

# Krea 2 Turbo Prompt Design

Turn the user's visual intent into a ready-to-use prompt for Krea 2 Turbo. This skill covers prompt authoring for text-to-image only; image generation, model files, and workflow settings follow the user's environment.

## Know the model

Krea 2 is Krea's own 12B diffusion transformer, trained from scratch on real photographs and artwork, with a Qwen3-VL text encoder that reads ordinary sentences. These traits shape every prompt:

- **Prose, not tags.** The model was trained on long captions of varying length. Dense, natural-language paragraphs give the best results, and a short sentence still produces a coherent image.
- **Guidance-free.** Turbo is distilled to run 8 steps with guidance 0. There is no classifier-free guidance, so a negative prompt has no effect. Everything the image should contain has to be stated affirmatively.
- **Unopinionated aesthetics.** The model does not push a house style. A style hint such as "retro cartoon illustration" or "grainy lo-fi VHS still" is rendered faithfully instead of being smoothed toward photorealism. The flip side: an unspecified style is a genuine open choice, so commit to one.
- **Text in quotes.** Words to render inside the image go in straight double quotes; the model treats quoted text as literal.
- **Text-to-image only.** The open weights take no input image. Style references and moodboards exist only in the Krea app; a request for editing or references needs a different model.

## Establish the task

Resolve two axes from the request:

| Axis | Choices |
| --- | --- |
| Intent clarity | Exploratory (the user has a subject but no committed look) or specified (subject, look, and constraints are known) |
| Appearance | Photograph, illustration, painting, 3D render, or another named medium; unstated means you choose one and say so |

For an exploratory request, use the exploration mode below. For a specified request, write one dense prompt. Ask only when a missing choice would change the whole image (for example the medium of a brand key visual); otherwise pick a reasonable default and name the assumption in one line.

Preserve every fixed element the user gave: subject, counts, colors, spatial relationships, named medium, and exact display text.

## Write dense natural-language prose

One cohesive paragraph, present tense, describing the finished picture. Typical order, taken from the official examples:

1. Primary subject and scene.
2. Medium and visual style.
3. Attributes of each subject, grouped with that subject.
4. Environment and atmosphere.
5. Lighting and how it lands on the materials.
6. Framing, perspective, and composition.

Rules that matter for this model:

- **Faithfulness first.** Keep the user's subjects, actions, colors, and layout. Add no new objects, props, characters, or animals unless the request clearly implies them.
- **Group attributes with their owner.** "A woman in a mustard-yellow windbreaker holds a paper cup" binds cleanly; a loose list of adjectives drifts between subjects.
- **Ground poses and layout.** Say where things are and how they touch: "sits on the left end of the bench, both hands around the mug".
- **Avoid over-specification.** Do not invent highly specific clothing, colors, materials, or props the request does not support, and do not add a pose, gaze, expression, or age marker ("faces slightly away", "a calm expression", "fine lines and a few gray strands") the request did not give. Spend the words on medium, the state of the surfaces that are already there, light, and composition instead; those give density without changing the user's picture.
- **Colors and surfaces are physical facts, not a grade.** Name a color as the color of a thing ("a red umbrella", "brick walls") and describe a surface by its state: worn, wet, scuffed, dusty, creased. Do not write palette or finish sentences such as "…make up the palette", "muted sea-gray and navy tones", "glossy sheen", or "clean and printed-looking" for a photograph or scene; they pull the render toward an even, plastic look. A limited palette stated for a poster or flat illustration is a design fact and stays.
- **Light has a source and contrast.** Say where the light comes from, how hard it is, and what it does to the surfaces: a hard-edged shadow under a brim, a specular streak on wet asphalt, a rim along hair. When the request leaves the light open, choose a light with direction and contrast; do not default to "soft, even", "overcast", or "diffused".
- **Say what is there.** Turn any exclusion into the state that replaces it: "a plain warm-gray backdrop fills the frame behind her" instead of "no background clutter".
- **Respect a stated medium.** "Photo of", "illustration of", "painting of", "3D render of" in the request are kept as given.
- **Already detailed input** gets a light polish, not a rewrite. Keep the user's phrasing and direction, including paragraph breaks and section labels such as "Foreground:" or "Lighting:".
- Write the prompt in English unless the user asks otherwise; keep quoted display text in its original language.

Length: about 60 to 120 words for a simple subject, up to about 200 for a dense scene. Longer is fine when every sentence adds a visible element.

Example (specified request, "editorial portrait of an old fisherman"):

```text
An editorial portrait photograph of an elderly fisherman, framed from the chest up. Deep weather lines cross his sun-darkened face and a short gray beard covers his jaw; he wears a faded knit cap and a creased, salt-stained oilskin jacket with the collar turned up. Behind him a harbor with moored wooden boats falls out of focus. Low sun from the front-left rakes across his face so that each line casts its own small shadow, and it throws hard highlights off the wet folds of the jacket.
```

## Exploration mode

When the user has a subject but no committed look, follow the official workflow: start vague, look at the spread, then narrow.

1. Offer the bare subject as the first prompt, for example `a cat riding a bicycle`, and explain that Krea 2 returns genuinely different interpretations from a short prompt.
2. Offer two or three style branches as short prompts with a comma-appended hint, each in a different direction: `a cat riding a bicycle, retro cartoon illustration` / `a cat riding a bicycle, dreamy cinematic scene` / `a cat riding a bicycle, extremely grainy lo-fi VHS still`.
3. When the user picks a branch, expand it into one dense paragraph using the rules above, keeping the chosen hint as the medium sentence.

Keep exploration prompts short on purpose; density is for the committed direction.

## Rendered text

Give the exact string in straight double quotes, then its placement, relative size, color, and lettering style. Describe separate lines separately. Keep the user's spelling, punctuation, and language.

```text
A concert poster with a deep blue background. Across the top, a large headline reads "Midnight Jazz" in cream bold serif capitals. In the center a gold silhouette of a saxophone player leans back mid-solo. Along the bottom the date "Oct 12" sits in smaller cream sans-serif letters. Flat, even lighting keeps the limited palette of deep blue, cream, and gold clean and printed-looking.
```

For a region reserved for later typesetting, describe it as a continuous area of one color with its size and position in the frame.

## Photography treatment

Name the genre (editorial, product, street, wildlife), the framing and viewpoint, where focus sits, the light source with its direction and hardness, and the state of the surfaces (wear, wetness, dust, fingerprints). Lens and aperture numbers work only as cues beside the visual effect they produce, such as "shallow depth of field". For product shots, state the supporting surface and how the object meets it.

## Illustration and painting treatment

Name the illustration type or painting medium and the marks that define it: line weight and shading method for illustration, brushwork and impasto for painting, solid fills and a limited palette for flat vector. Because the model renders unfamiliar styles faithfully, a precise style noun ("risograph print", "gouache storyboard panel", "2D anime key visual with cel shading") does more than a stack of quality adjectives. Keep character proportions, costume, palette, and background treatment stylistically consistent.

## Workflow settings, kept out of the prompt

Turbo runs at 8 steps, guidance 0.0, timestep shift mu 1.15, from 1024 to 2048 px per side with dimensions padded to multiples of 16. Raw uses about 52 steps and guidance 3.5 and is meant for training, not generation. Give these as a separate settings note; the prompt describes the picture only.

## Deliver and refine

Provide a copy-ready prompt in the requested format, plus a settings note when useful. Label authored examples as starting points; describe generation results only after seeing them.

Before delivery, check:

- The medium and style are stated once and match the request or the chosen exploration branch.
- Every subject the user named is present with its own attributes; nothing was added that the request does not support.
- Each sentence describes something present in the image; no negations.
- Colors belong to things and light has a source and contrast; there is no palette or finish sentence.
- Quoted display text matches the user's characters exactly.
- Size, aspect ratio, and steps are in the settings note, not in the prompt.

During iteration, translate feedback into a concrete visible change and adjust one group of conditions at a time, keeping the seed fixed when the workflow allows it. Change the medium sentence to shift the whole look; change lighting and composition sentences to shift mood without changing content.

## Lightweight variant for local LLM nodes

When the user wants a prompt rewriter inside ComfyUI or another workflow tool on a local general-purpose LLM (27B-class; smaller models do not follow the instructions reliably), hand over `SKILL-lite-t2i.md` instead of this skill. It is a complete English system prompt with no frontmatter, pasted as-is into the LLM node. It takes the user's rough request as the user message and returns the finished prompt only. There is no i2i variant because the open weights are text-to-image only.

Keep the lite file in step with this skill when it changes.

## Sources and scope

Official sources establish the architecture, Turbo settings, prose-first prompting, quoted text, and the exploratory workflow. The treatments above are practical authoring guidance; judge them by the generated results.

- [Model card: Krea 2 Turbo](https://huggingface.co/krea/Krea-2-Turbo)
- [Official repository and settings](https://github.com/krea-ai/krea-2)
- [Official prompting guide](https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md)
- [Technical report](https://www.krea.ai/blog/krea-2-technical-report)
- [Exploratory prompting guide](https://www.krea.ai/blog/explorative-prompting-krea-2)
- [Prompting guide: exploration, style references, moodboards](https://www.krea.ai/blog/krea-2-deep-dive-walkthrough)
- [ComfyUI support announcement](https://blog.comfy.org/p/krea-2-open-source-models-are-now)
