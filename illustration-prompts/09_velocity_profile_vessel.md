# Velocity-profile vessel

## Targets

- Procedural (geometry-locked, used by SVG): `../velocity_profile_vessel.png`
- AI alternate: `../velocity_profile_vessel_ai.png`
- Flattened figure: `../02c_velocity_profile.png`
- SVG overlay: [`../02c_velocity_profile.svg`](../02c_velocity_profile.svg)

---

## Generate (procedural — preferred for SVG arrows)

```bash
python3 illustration-prompts/build_velocity_profile_vessel.py
```

Locked: `CX=200 CY=200 R=150` in the 400×400 image → page `(220, 290)`, `R=150`.

---

## AI prompt (raster alternate)

Medical textbook graphite illustration on cream textured paper. Square composition. Exact centered circular cross-section of a small blood vessel lumen. Thick graphite-hatched vessel wall forming a clean round ring. Inside the lumen: about 25 red blood cells as soft cartoon biconcave discs in restrained deep red, naturally scattered with varied orientations and slight jitter, whole cells only fully inside the lumen with clear gap from the wall, not cut by the wall, not arranged on rings. No dotted circles, no arrows, no graph, no labels, no text, no equations, no watermark. Hand-drawn pencil look, not photoreal, not flat vector. Empty cream paper around the vessel.

**Note:** AI output is not geometry-locked. Use the procedural PNG under the SVG if rings/arrows must land exactly.
