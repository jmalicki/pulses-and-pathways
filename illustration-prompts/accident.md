# Accident — repeatable three-pass workflow

**Final target:** `accident_sketch.png`  
**Beat:** Mark recounts the table-saw accident that divided his left ulnar
artery.  
**Audience:** Vascular surgeons and petroleum engineers reading *Pulses and
Pathways*.  
**Status:** Needs regeneration.

This is a restrained clinical narrative, not gore. The wound location and
pulsatile blood establish the emergency that leads to left ulnar-artery
exploration, proximal and distal control, and repair.

## Why three passes

Later passes edit the exact approved output of the prior pass:

1. [`accident_pass_0_base.md`](accident_pass_0_base.md) locks the clean pose,
   shared forearm view, rag path, saw mechanics, room, and style.
2. [`accident_pass_1_anatomy.md`](accident_pass_1_anatomy.md) adds only the
   non-bloody laceration.
3. [`accident_pass_2_blood.md`](accident_pass_2_blood.md) adds only the landed
   blood evidence and one live arterial pulse.

Do not combine the prompts or regenerate the scene in Pass 1 or Pass 2.

## Pass 0 — clean base

1. Run the prompt in
   [`accident_pass_0_base.md`](accident_pass_0_base.md).
2. Attach `clamping_sketch_1786259348177.jpg` and
   `suturing_sketch_1786259361282.jpg` as style-only references.
3. Save the untouched result as `accident_pass_0_base.png`.
4. Audit in this order:

### Gate 1 — the forearm

- Raised arm is anatomical LEFT and continuous with the LEFT shoulder/upper
  arm; rag hand is anatomical RIGHT and continuous with the RIGHT shoulder.
- No crossed-limb attachment: the inspected forearm is not joined to the right
  upper arm.
- The arm bends upward: proximal elbow end lower, distal wrist end higher.
- Camera sees a broad ventral-ulnar surface rather than its edge.
- Mark visibly looks at that same surface.
- Forearm is the central dominant anatomical plane.
- Mark’s anatomical RIGHT lateral / dextral body plane is nearly square to the
  camera; sternum and belt buckle point image-right, not toward the lens;
  frontal chest and pelvis do not dominate.
- Clean target patch is 3–4 cm long and 10–14 cm above the wrist.
- Rag is at the proximal/elbow-side end of the visible segment, with its edge
  13–16 cm above the wrist and approximately 2–3 cm proximal to the patch
  center.
- RIGHT hand visibly moves the rag distal/wristward.
- Rag and hands block neither Mark’s view nor the camera’s view.
- Mark is standing.
- No wound, blood, or red appears.

Reject immediately if Gate 1 fails. A good saw, room, or style cannot compensate
for a hidden, edge-on, straight, or lowered ventral forearm.

### Gate 2 — the saw

- One full-length narrow groove is visible in one continuous rail.
- Groove and dado stack are both ¼ inch / 6.35 mm wide and visibly match.
- Exposed crown shows two parallel dado plates, not one thin saw blade.
- Groove is 12–14 mm deep in 30–38 mm stock with solid wood beneath.
- Cutter is 8 inches in diameter with only 12–14 mm exposed.
- Broad guard hood and separate thin splitter/riving-knife plate are removed
  and visible.
- Thin splitter plate is visibly narrower than the dado stack.

### Gate 3 — room and style

- One back wall and one right wall meet at exactly one coherent corner.
- Premium steel storage reads clearly without dense clutter.
- Drawing is a moderately shaded courtroom sketch with 50–55 percent open
  cream paper, not a filtered photograph.

Do not continue until all three gates pass.

## Pass 1 — non-bloody laceration

1. Attach `accident_pass_0_base.png`.
2. Run the prompt in
   [`accident_pass_1_anatomy.md`](accident_pass_1_anatomy.md).
3. Save the untouched result as `accident_pass_1_anatomy.png`.
4. Reject unless:

- Pass 0 geometry remains unchanged.
- One 3–4 cm irregular laceration appears 10–14 cm above the wrist on the LEFT
  ventral-ulnar / little-finger-side surface.
- Wound is immediately distal to the fixed rag and remains visible to both Mark
  and camera.
- Deepest segment is at the ulnar border and tapers in the pull-away direction.
- Radial/thumb side remains intact.
- No blood or red appears.

## Pass 2 — arterial evidence

1. Attach `accident_pass_1_anatomy.png`.
2. Run the prompt in
   [`accident_pass_2_blood.md`](accident_pass_2_blood.md).
3. Save the untouched result as `accident_pass_2_blood.png`.
4. Reject unless:

- Pass 1 geometry and wound remain unchanged.
- Mark and camera still see the wound; rag remains proximal and unseated.
- Four prior pulse marks and one modest smear appear on or around the saw.
- Exactly one live proximal systolic pulse travels toward camera approximately
  20–30 degrees off-axis.
- Live column is 5–10 cm; total throw is 15–25 cm.
- Distal stump does not pulse.
- Total blood remains 15–30 ml and visually restrained.
- No continuous stream, second jet, giant pool, or graphic tissue detail
  appears.

## Promote the approved image

After all gates pass:

1. Copy `accident_pass_2_blood.png` to `accident_sketch.png`.
2. Keep all numbered pass files for audit and repetition.
3. Record generator, model, and date:

   - Pass 0: pending
   - Pass 1: pending
   - Pass 2: pending
   - Final approval: pending

## Clinical continuity

- LEFT ventral-ulnar wound → left ulnar-artery exposure.
- Deepest focal segment → complete ulnar-artery transection.
- Proximal live pulse → emergency proximal control.
- Non-pulsatile distal end → distal control.
- Two divided ends → assessment and arterial repair.
- Rag approaching from proximal side → direct pressure is beginning but has
  not hidden the diagnostic wound.
- BP 138/82 and HR 96 → 0.625-second beat interval; four landed pulses plus one
  live airborne pulse.
