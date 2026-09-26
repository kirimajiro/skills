---
name: qwen-image-2-1
description: Create, rewrite, and refine prompts for Qwen-Image-2.1 using affirmative descriptions of the desired result. Use for text-to-image, single-image editing, multi-reference composition, transparent RGBA assets, photography, and anime prompt requests targeting this model.
---

# Qwen-Image-2.1 Prompt Design

Turn the user's visual intent into a ready-to-use prompt. Express the desired image through observable properties, explicit reference roles, and concise preservation instructions. This skill covers prompt authoring; image generation and installation follow the user's requested scope and available environment.

## Establish the task

Resolve three independent axes from the request:

| Axis | Choices |
| --- | --- |
| Operation | Text-to-image (t2i), single-image editing (i2i), multi-image editing or composition (multi i2i) |
| Output | Scene with a background, transparent RGBA asset |
| Appearance | Photography, anime, or another requested medium |

Combine the relevant guidance. For example, a transparent anime character assembled from references uses multi i2i, RGBA, and anime instructions together.

For editing, inspect available reference images and bind instructions to their visible contents. Ask for a missing image or a consequential unresolved choice when needed. Use reasonable defaults for minor artistic choices and identify assumptions briefly when they affect the result.

Preserve the user's subject, counts, colors, spatial relationships, exact display text, and requested style. Scale elaboration to the task: a local edit needs a focused directive; a new scene benefits from composition and lighting design.

## Write affirmative visual instructions

Describe what occupies each relevant region and how it should look. Translate exclusions into the intended replacement state. Apply this approach to both prompts and accompanying guidance.

| Intent | Affirmative formulation |
| --- | --- |
| Simplify a background | A uniform warm-gray background surrounds the subject with generous open space. |
| Fit the entire subject | The subject is visible from the top of the head to the soles, with margins above and below. |
| Fix the subject count | Exactly two people stand side by side at the center of the frame. |
| Retain facial identity | Preserve the person's facial identity and expression from the input image. |
| Prepare space for later typography | The upper third is a continuous cream-colored area reserved for a headline. |
| Create transparency | The surroundings and openings between the handles are fully transparent. |
| Finish an annotated region | Render the marked area with colors and textures continuous with the surrounding scene. |
| Produce natural skin | The skin shows subtle pores, gentle tonal variation, and soft highlights. |

Prioritize affirmative descriptions over naming unwanted objects or visual defects. Preserve exact user-supplied text intended to appear inside the image, including its original wording and language.

Choose mutually compatible conditions. Bind each attribute to its subject. Express abstract quality goals through framing, materials, lighting, linework, or tonal treatment.

Use English prompt prose by default and retain the original language of text rendered inside the image. Follow an explicit user preference for another prompt language. Explain in the user's conversational language.

## Text-to-image

Describe the finished image in declarative prose. A useful order is:

1. Medium, subject, and count.
2. Action, pose, expression, and orientation.
3. Framing, placement, viewpoint, and open space.
4. Background and foreground relationships.
5. Materials, palette, lighting, and overall mood.

Select the details that determine the requested result. Keep output dimensions and aspect ratio in the application's settings or a separate settings note.

For rendered text, provide the exact string in straight double quotes, its position, relative size, color, and type style. Describe separate lines individually. For later typesetting, specify the reserved region's appearance and dimensions within the composition.

Example:

```text
An editorial photograph of a single ivory ceramic coffee cup on a dark walnut table. The cup sits in the lower-right area of the frame, viewed slightly from above, with its handle pointing right. A thin curl of steam rises from the coffee. The upper-left area is a broad expanse of softly blurred warm-brown background, suitable for a headline. Soft morning light enters from the left, revealing the ceramic glaze and wood grain. The palette combines warm cream, deep brown, and muted amber.
```

Optional typography addition:

```text
In the upper-left area, a large dark-brown headline reads "Morning Ritual", set in a restrained serif typeface.
```

## Single-image editing

Lead with the operation, then describe the changed attribute and the features to preserve. Refer to retained content by identity, role, or location. Concentrate appearance detail on the edited object.

Distinguish these intents:

| Intent | Design approach |
| --- | --- |
| Modify the existing picture | Specify the change and preserve the surrounding content, framing, and relevant lighting. |
| Create a new picture of the subject | Preserve the subject's identity and actively design the new setting, pose, composition, and lighting. |
| Change the rendering style | Specify the new medium and retain the requested character features, content, and layout. |

Example:

```text
Replace the person's jacket with a dark navy linen blazer. Preserve the person's facial identity, hairstyle, expression, pose, hands, and all other clothing and accessories. Retain the original background, framing, and lighting. Match the blazer's folds and shading to the existing body pose and light direction.
```

For local edits, identify the target by location, visible annotation, or supplied mask. Treat annotation marks as editing guides and describe the finished appearance of their region. Match mask polarity and input handling to the chosen workflow.

Example:

```text
Replace the bag marked by the red circle with a small black leather shoulder bag. Preserve the person's pose, clothing, and the surrounding scene. Render the annotated area as a finished photographic region, with colors and textures continuous with its surroundings.
```

For fidelity-sensitive work, recommend comparing the result with the original at faces, logos, lettering, outlines, and other important details.

## Transparent RGBA output

Use the official recommended wrapper, replacing the middle description with the requested asset:

```text
This is an RGBA image with transparency. A small orange fox mascot wearing a teal scarf, shown in full body in a cheerful standing pose. Clean dark outlines, simple cel shading, and a clearly readable silhouette. The entire tail, ears, and feet are visible, with generous transparent margins around the character. The image has alpha channel and the background is transparent.
```

Specify the visible foreground, transparent surrounding regions, internal openings, and framing margins. For translucent materials, describe the desired partial transparency and edge transitions. Distinguish shading on the object from a cast shadow on a supporting surface.

Extraction example:

```text
Extract the handbag from the input photograph as an isolated RGBA asset. Preserve its original shape, color, stitching, hardware, printed markings, and surface shading. The handbag forms the visible foreground. The surrounding area, the space beneath the bag, and the openings between the handles are fully transparent.
```

Transparent-image edit example:

```text
Change the character's expression to a joyful smile. Preserve the character design, pose, colors, outline style, and existing transparent background. Keep the output as an RGBA image with an alpha channel.
```

When implementation advice is relevant, specify alpha-preserving output processing and an appropriate format such as PNG. Verify actual transparency by compositing the export over light and dark backgrounds, checking outlines, hair, openings, and translucent surfaces.

## Multiple reference images

Assign a role to each input and map it to its actual input order. Distinguish the base canvas from identity, garment, object, and style references. Specify the attributes transferred from each source.

The official editing prompt enhancer uses `<image1>`, `<image2>`, and subsequent numbered tags. Use this convention when supported by the target workflow; adapt to an explicitly documented interface convention when necessary.

Example role map:

| Input | Role | Contribution |
| --- | --- | --- |
| image1 | Base canvas | Person, pose, background, framing |
| image2 | Garment reference | Jacket cut, fabric, color, fastenings |
| image3 | Product reference | Handbag shape and hardware |

Example:

```text
Use <image1> as the base image. Replace the person's jacket with the jacket from <image2>, preserving its cut, fabric, color, and fastenings. Place the handbag from <image3> in the person's right hand. Here, right refers to the person's own right side. Preserve the handbag's shape and hardware. Keep the facial identity, hairstyle, body pose, background, and framing from <image1>. Adjust the transferred items' scale, folds, lighting, and contact shadows to fit the person naturally.
```

For a newly composed scene, treat the inputs as identity or asset sources and design a shared setting:

```text
Create one group photograph of exactly two people. Use <image1> as the identity reference for the person on the left and <image2> as the identity reference for the person on the right. Both people stand side by side, facing the camera, in front of a plain warm-gray studio backdrop. Preserve each person's distinct facial identity and hairstyle. Use consistent soft studio lighting and a shared camera perspective.
```

The model's advertised capacity is up to ten reference images. Match the actual input count to the current service or workflow limit. Check current implementation documentation when giving operational limits.

## Photography treatment

Specify photographic genre, framing, viewpoint, light source and direction, focus placement, surface texture, and color treatment. Treat lens and aperture values as visual cues and accompany them with the desired perspective or depth of field.

Example:

```text
An editorial portrait photograph of an adult woman seated beside a cafe window, framed from the waist up at eye level. She looks slightly away from the camera with a relaxed expression. Soft daylight from the left creates gentle shadows across her face. Focus rests on her eyes, while the cafe interior falls softly out of focus. Her skin retains subtle natural texture, and the weave of her cream cotton shirt remains visible. The colors are restrained and warm, with gentle highlight roll-off.
```

For product photography, state the intended focus coverage, material response, readable markings, and contact with the supporting surface. Example focus clause: "The entire product is sharply rendered from front to back, while the distant background remains softly blurred."

## Anime treatment

Specify the illustration type, line weight, shading method, character proportions, hair silhouette, costume, palette, background treatment, and expression. Keep these choices stylistically coherent.

Example:

```text
A 2D anime key visual of a young adult courier standing on a rooftop at dusk. She has short dark-blue hair, amber eyes, and a mustard-yellow windbreaker over charcoal trousers. Her full body is visible, positioned slightly left of center, with her jacket hem moving in the breeze. Fine controlled linework and crisp two-tone cel shading define the character. A softly painted city skyline fills the background in muted lavender and coral. Warm rim light outlines her hair and shoulders, while her face remains clearly readable.
```

Character editing example:

```text
Change the character's expression to a confident smile and raise the character's own right hand in a greeting gesture. Preserve the original character design, facial proportions, hairstyle, costume details, color palette, linework, and cel-shading style. Retain the original background and framing.
```

For recurring characters, use an accepted image as the identity and design reference. For turnarounds, expression sheets, or storyboards, specify panel count, layout, reading order, and the pose or expression in each panel.

## Deliver and refine

Provide a copy-ready prompt in the requested format. Add a compact input-role map for multi-image work and separate output settings when useful. Match explanation length to the user's request. Label newly authored examples as starting points; describe observed generation results only after actual inspection.

Before delivery, check:

- The operation, output type, and visual style match the request.
- Each sentence describes a desired state, a positive operation, or a preservation target.
- Counts, positions, attributes, and reference roles are consistent.
- Quoted display text matches the user's intended characters.
- Framing and lighting conditions work together.
- Technical settings are distinguished from visual descriptions.

During iteration, translate feedback into a concrete target state. Adjust one coherent group of conditions at a time, keeping the seed and settings stable when the workflow supports them. Prioritize subject and count, then composition, lighting, and surface detail.

Official prompt-enhancement models are an optional expansion route. Review expanded prompts for alignment with the user's subject, constraints, and intended level of scene detail.

## Lightweight variants for local LLM nodes

When the user wants a prompt rewriter that runs inside ComfyUI or another workflow tool on a local general-purpose LLM (27B-class; smaller models do not follow the instructions reliably), hand over the matching sibling file instead of this skill. Each is a complete English system prompt with no frontmatter, pasted as-is into the LLM node. It takes the user's rough request as the user message and returns the finished prompt only.

| File | Mode |
| --- | --- |
| `SKILL-lite-t2i.md` | Text-to-image, including transparent RGBA assets |
| `SKILL-lite-i2i.md` | Single-image editing, multi-reference composition, RGBA extraction |

They apply the same affirmative-description and preservation principles as this skill. Keep them in step when this skill changes.

## Sources and scope

The official sources establish capabilities, the RGBA wrapper, and prompt-enhancement conventions. The examples and photography/anime recipes above are practical authoring guidance. Affirmative phrasing is the preferred writing method for this skill; assess its effectiveness through the actual generated results.

- [Official announcement](https://qwen.ai/blog?id=qwen-image-2.1)
- [Official repository and RGBA guidance](https://github.com/QwenLM/Qwen-Image-2.1)
- [Official prompt rewriting workflow](https://github.com/QwenLM/Qwen-Image-2.1#prompt-rewriting)
- [T2I prompt enhancer instructions](https://huggingface.co/Qwen/Qwen-Image-2.1-PE-T2I/blob/main/system_prompt.txt)
- [I2I prompt enhancer instructions](https://huggingface.co/Qwen/Qwen-Image-2.1-PE-I2I/blob/main/system_prompt.txt)
