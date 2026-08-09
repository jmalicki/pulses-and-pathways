# Wellhead choke — engineering illustration prompt

**Target:** `choke_sketch.png` (or `.jpg`); shown in the play via `05_wellhead_choke.svg` as **Fig. 5**.  
**Use:** Embedded in Act 2 after Mark’s choke / stenosis bridge (`act_2_pressure_and_flow.md`).  
**Kind:** Labeled engineering plate (exception like `07_stenosis_cutaway.md`).

Copy everything under **Prompt** into the image model as-is. Do not invent alternate geometries.

---

## Prompt

Graphite/charcoal on cream paper. Grayscale only—no color. Two equal side-by-side panels. Nothing in the frame except the two cutaways and the titles/labels named below. No background, manifold, gauges, signature, or watermark.

Font: Georgia only (bold for titles, regular for labels). Small, print-sharp. Thin straight charcoal leader lines. No handwriting, no other fonts.

LABELS — exact whitelist (mandatory; nothing else):

- Panel titles only: "Fixed bean choke" (left) and "Adjustable choke" (right).
- Left panel leaders, all four required, spelling exact: Bean | Blanking cap | Inlet | Outlet
- Right panel leaders, all five required, spelling exact: Needle | Seat | Handwheel | Inlet | Outlet
- Do NOT label any other word.

SHARED BODY (both panels): a simple pipe **T** cutaway—like a plumbing tee—not a cross, not a valve with a fat chamber.

```text
        TOP access
            │
            │     ← vertical run: same pipe diameter top to bottom
   INLET ───┤     ← side branch only; far side of vertical pipe is flush ID wall
            │
         OUTLET
```

Geometry rules:

- Vertical run is one straight pipe of **constant diameter** from top access down to Outlet. Outer and inner walls are flush/cylindrical—**no gigantic bulge**, no thick boss, no swollen chamber opposite the Inlet.
- Inlet is a side branch of similar pipe diameter joining that vertical run. Where they meet is a normal tee junction.
- Opposite the Inlet: just the **far inner wall of the vertical pipe**, continuous and flush with the pipe above and below the junction. Not a protruding block wall. Not a fourth port.
- Exactly three openings: Inlet (left), Outlet (bottom), Top access (top). No 4-way. Same outline both panels.

BEAN / SEAT HEIGHT (both panels—do not ignore):

- In the upper outlet leg, draw a clear **bean box**: a threaded cylindrical pocket machined into the outlet bore at the T junction—the receptacle the bean/seat screws into. Show the box as a distinct short chamber/threads in the outlet ID, not just a floating plug in open pipe.
- Bean (left) and Seat (right) screw **down into that bean box** in the outlet.
- Their **top faces must be at or below the horizontal centerline of the Inlet**—most of the bean/seat body is **below** that centerline, down inside the outlet-leg bean box.
- Do **not** float them high in the upper vertical run under the blanking cap/handwheel. Leave clear empty bore in the top half above the inlet centerline (access space only).

LEFT PANEL — Fixed bean choke (cutaway):

- BEAN: short threaded cylinder, hole through inlet face (UP) to outlet face (DOWN). Screwed fully into the **bean box in the outlet**. Height rule above. Show threads engaging the box.
- Inlet reaches the bean’s top face; ONLY path to Outlet is through the bean hole. No bypass around the bean or around the box.
- BLANKING CAP on top access only.

RIGHT PANEL — Adjustable choke (cutaway):

- SEAT: same **bean box in the outlet**, same height rule. Seat screws into that box like the bean. Inlet face UP, outlet face DOWN.
- SEAT bore is a **cone** (tapered hole). NEEDLE tip is a matching **cone** of the same taper—the two cones nest. Draw them mating; do not use a cylindrical needle in a cylindrical seat.
- HANDWHEEL on top. Turning the wheel is what moves the needle: show **stem threads way up at the top**, in the topworks under/near the handwheel—that is how rotation becomes axial travel. No drive threads down by the seat.
- NEEDLE extends down into the seat cone, partly open so a clear annular gap remains. Stem unlabeled.
- Length invariant: the visible **threaded stem length between the top of the choke body and the handwheel** must be **slightly more** than the axial distance from the **seat to the bottom tip of the needle** (needle–seat engagement depth). They can look almost equal; if unsure, give a bit more thread up top than needle-into-seat below.
- ONLY path through the matching cones past the needle. No bypass. No flow out the top.

FORBIDDEN: 4-way cross; pipe opposite Inlet; bulging/swollen wall opposite Inlet; bean or seat floating in open bore with no threaded outlet pocket/bean box; bean or seat sitting high above inlet midline; mismatched needle/seat tapers; drive threads at the seat instead of at the top; top thread length shorter than needle-to-seat depth; bypass; colors; extra labels.
