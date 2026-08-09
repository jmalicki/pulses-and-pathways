# Accident — repeatable two-pass workflow

**Final target:** `accident_sketch.png`  
**Beat:** Act 1 open—while the regional block sets, Mark recounts the table-saw
accident that divided his left ulnar artery.  
**Audience:** Vascular surgeons and petroleum engineers reading *Pulses and
Pathways*. Anatomy and arterial physics must withstand clinical scrutiny.  
**Status:** Needs regeneration using the two passes below.

This plate is not gore, horror, or injury fetishism. It is the restrained
diagnostic setup for the operation shown in the following plates: exploration
of the left volar-ulnar distal forearm, proximal and distal vascular control,
assessment of the divided ends, and arterial repair. The wound location and
pulsatile blood are necessary clinical facts, not decorative violence.

## Why two passes

Single-pass generations repeatedly traded one requirement for another:
mirrored/right-arm anatomy, radial rather than ulnar injury, continuous streams
instead of systolic pulses, or incorrect saw geometry. The split workflow locks
the difficult spatial facts before adding blood:

1. [`accident_pass_1_anatomy.md`](accident_pass_1_anatomy.md) creates the full
   grayscale scene with the correctly placed injury but **no blood**.
2. [`accident_pass_2_blood.md`](accident_pass_2_blood.md) edits that exact image
   and adds only the earlier saw evidence and one live arterial pulse.

Do not combine the prompts. Do not ask pass 2 to regenerate the scene.

## Repeatable procedure

### Pass 1: anatomy and scene

1. Copy the prompt from
   [`accident_pass_1_anatomy.md`](accident_pass_1_anatomy.md).
2. Generate without a reference image.
3. Save the unmodified result as `accident_pass_1_anatomy.png`.
4. Reject and rerun pass 1 unless all are true:
   - injured arm is anatomical LEFT;
   - the left little finger is identifiable;
   - wound is on that same volar-ulnar/pinky border;
   - right hand holds the clean rag;
   - subject is centered, arm raised, and stepped back;
   - guard and riving knife are visibly removed;
   - intact board has a visible-bottom blind partial groove;
   - no blood or red appears anywhere.

Do not proceed to pass 2 with a laterality, anatomy, pose, or saw error. Pass 2
is not allowed to repair the base composition.

### Pass 2: blood and pulse physics

1. Attach `accident_pass_1_anatomy.png` as the image to edit.
2. Copy the prompt from
   [`accident_pass_2_blood.md`](accident_pass_2_blood.md).
3. Save the untouched result as `accident_pass_2_blood.png`.
4. Reject and rerun pass 2 unless all are true:
   - pass 1 geometry and anatomy remain unchanged;
   - a modest smear and four landed pulse marks appear on/around the saw;
   - exactly one live proximal systolic pulse is airborne;
   - coherent column is 5–10 cm; total throw is 15–25 cm;
   - distal stump has no pulse;
   - rag shows incomplete beginning pressure;
   - no continuous stream, second jet, giant pool, or graphic tissue detail.

### Promote the approved image

Only after both quality gates pass:

1. Copy `accident_pass_2_blood.png` to `accident_sketch.png`.
2. Keep both numbered pass files so the generation can be audited or repeated.
3. Record the generator/model and date here:

   - Pass 1: pending
   - Pass 2: pending
   - Final approval: pending

## Clinical continuity

- Left volar-ulnar wound → left ulnar-artery exposure.
- Proximal systolic pulse → emergency proximal hemorrhage control.
- Non-pulsatile distal end → distal control.
- Two divided ends → assessment and arterial repair.
- Rag beginning pressure → active bleeding not yet controlled.
- BP 138/82 and HR 96 → 0.625-second beat interval; four earlier landed pulses
  plus exactly one live airborne pulse in the chosen frozen instant.
