# Illustration prompts

Graphite/charcoal illustration prompts for *Pulses and Pathways*.

| File | Kind | Target | Status |
| --- | --- | --- | --- |
| [`medical_shared_style.md`](medical_shared_style.md) | Medical shared rules | (linked from each medical prompt) | — |
| [`accident.md`](accident.md) | Workshop workflow | `accident_sketch.png` | **Needs three-pass regen** |
| [`accident_pass_0_base.md`](accident_pass_0_base.md) | Workshop pass 0 | `accident_pass_0_base.png` | Pose/rag/saw; no wound |
| [`accident_pass_1_anatomy.md`](accident_pass_1_anatomy.md) | Workshop pass 1 | `accident_pass_1_anatomy.png` | Add wound at rag; no blood |
| [`accident_pass_2_blood.md`](accident_pass_2_blood.md) | Workshop pass 2 | `accident_pass_2_blood.png` | Edit pass 1; add arterial evidence |
| [`01_title_page.md`](01_title_page.md) | Medical | `title_page_sketch_*.jpg` | Matches |
| [`02_exposure.md`](02_exposure.md) | Medical | `exposure_sketch.png` | Regenerated |
| [`03_clamping.md`](03_clamping.md) | Medical | `clamping_sketch_*.jpg` | Matches |
| [`04_suturing.md`](04_suturing.md) | Medical | `suturing_sketch_*.jpg` | Matches |
| [`05_doppler.md`](05_doppler.md) | Medical | duplex screen SVGs `09a`/`09b` (+ optional field JPG) | Screen SVGs in play; prompt retargeted from pencil Doppler |
| [`06_closure.md`](06_closure.md) | Medical | `closure_sketch_*.jpg` | Matches |
| [`07_stenosis_cutaway.md`](07_stenosis_cutaway.md) | Medical (labeled) | `stenosis_cutaway.jpg` | Keep labels; **regen for crisp type** |
| [`08_vascular_tree.md`](08_vascular_tree.md) | Medical | `vascular_tree.jpg` | Matches |
| [`09_velocity_profile_vessel.md`](09_velocity_profile_vessel.md) | Procedural script | `velocity_profile_vessel.png` | `build_velocity_profile_vessel.py` embeds into `02c_velocity_profile.svg` |
| [`10_wellhead_choke.md`](10_wellhead_choke.md) | Engineering (labeled) | `choke_sketch.png` → Fig. 5 via `05_wellhead_choke.svg` | Installed |

Medical plates link to [`medical_shared_style.md`](medical_shared_style.md) and specify the patient’s **left** forearm. The wellhead choke is a labeled **engineering** plate exception (like stenosis cutaway). The workshop accident uses a repeatable three-pass workflow: lock the left volar-ulnar camera surface and rag anchor, add the non-bloody wound at that anchor, then add the clinically necessary pulse pattern.
