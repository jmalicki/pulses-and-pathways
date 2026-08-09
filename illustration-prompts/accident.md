# Accident — repeatable three-pass workflow

**Final target:** `accident_sketch.png`  
**Beat:** Act 1 open—while the regional block sets, Mark recounts the table-saw
accident that divided his left ulnar artery.  
**Audience:** Vascular surgeons and petroleum engineers reading *Pulses and
Pathways*. Anatomy and arterial physics must withstand clinical scrutiny.  
**Status:** Needs regeneration using the three passes below.

This plate is not gore, horror, or injury fetishism. It is the restrained
diagnostic setup for the operation shown in the following plates: exploration
of the left volar-ulnar mid-to-distal forearm, proximal and distal vascular control,
assessment of the divided ends, and arterial repair. The wound location and
pulsatile blood are necessary clinical facts, not decorative violence.

## Why three passes

Single-pass generations repeatedly traded one requirement for another:
mirrored/right-arm anatomy, radial rather than ulnar injury, continuous streams
instead of systolic pulses, or incorrect saw geometry. The split workflow locks
the difficult spatial facts before adding the wound or blood:

1. [`accident_pass_0_base.md`](accident_pass_0_base.md) creates a clean
   grayscale scene with **no wound or blood**. It locks the camera-visible
   volar-ulnar surface and anchors the clean rag at the future injury site.
2. [`accident_pass_1_anatomy.md`](accident_pass_1_anatomy.md) edits that exact
   image to add the non-bloody laceration immediately distal/image-above the
   fixed rag and guiding RIGHT index finger.
3. [`accident_pass_2_blood.md`](accident_pass_2_blood.md) edits Pass 1 and adds
   only the earlier saw evidence and one live arterial pulse.

Do not combine the prompts. Each later pass edits the exact approved output of
the prior pass and may not regenerate the scene.

## Repeatable procedure

### Pass 0: clean pose, rag anchor, and saw

1. Copy the prompt from
   [`accident_pass_0_base.md`](accident_pass_0_base.md).
2. Attach `clamping_sketch_1786259348177.jpg` and
   `suturing_sketch_1786259361282.jpg` as style-only references.
3. Save the unmodified result as `accident_pass_0_base.png`.
4. Reject and rerun Pass 0 unless all are true:
   - raised arm is anatomical LEFT;
   - left palm and all five digits are identifiable;
   - thumb is image-left and little finger is image-right;
   - camera clearly sees the volar-ulnar mid-to-distal forearm;
   - clean rag’s leading edge sits on that little-finger-side surface 13–16 cm
     above the wrist;
   - RIGHT index finger guides it toward an exposed distal/image-above patch;
   - subject is centered, arm raised, and stepped back;
   - guard and riving knife are visibly removed;
   - cutter visibly reads as a narrow ¼-inch dado stack, not one thin blade or
     a broad ¾-inch stack;
   - display-cabinet upper rail has a full-length deep glass track with a
     visible flat bottom and solid wood remaining beneath;
   - style reads as a skilled live courtroom sketch with gestural contours,
     selective hatching, open paper, and loose edges—not photorealistic
     graphite rendering;
   - no wound, blood, or red appears anywhere.

Do not proceed with a mirrored arm, radial-side rag, hidden ulnar surface, or
incorrect saw.

### Pass 1: add the laceration

1. Copy the prompt from
   [`accident_pass_1_anatomy.md`](accident_pass_1_anatomy.md).
2. Attach `accident_pass_0_base.png` as the image to edit.
3. Save the unmodified result as `accident_pass_1_anatomy.png`.
4. Reject and rerun pass 1 unless all are true:
   - Pass 0 geometry remains unchanged;
   - injured arm is anatomical LEFT;
   - the left little finger is identifiable;
   - rag has not moved;
   - wound is immediately distal/image-above that rag and guiding index finger
     on the same volar-ulnar border;
   - wound sits 10–14 cm above wrist on the camera-facing mid-to-distal
     forearm, not at the wrist joint;
   - rag is moving into place but does not yet cover the wound;
   - wound is irregular and slightly oblique, deepest at the ulnar border and
     tapering in the pull-away direction—not a smooth knife incision;
   - no blood or red appears anywhere.

Do not proceed to Pass 2 with a laterality, rag-anchor, or wound-placement
error. Pass 2 is not allowed to move the rag or wound.

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
   - rag is visibly moving into pressure position but has not seated or hidden
     the wound;
   - no continuous stream, second jet, giant pool, or graphic tissue detail.

### Promote the approved image

Only after both quality gates pass:

1. Copy `accident_pass_2_blood.png` to `accident_sketch.png`.
2. Keep all numbered pass files so the generation can be audited or repeated.
3. Record the generator/model and date here:

   - Pass 0: pending
   - Pass 1: pending
   - Pass 2: pending
   - Final approval: pending

## Clinical continuity

- Left volar-ulnar wound → left ulnar-artery exposure.
- Deepest irregular saw segment → complete ulnar-artery transection.
- Proximal systolic pulse → emergency proximal hemorrhage control.
- Non-pulsatile distal end → distal control.
- Two divided ends → assessment and arterial repair.
- Rag moving into pressure position → wound and active bleed still visible just
  before compression seats.
- BP 138/82 and HR 96 → 0.625-second beat interval; four earlier landed pulses
  plus exactly one live airborne pulse in the chosen frozen instant.
