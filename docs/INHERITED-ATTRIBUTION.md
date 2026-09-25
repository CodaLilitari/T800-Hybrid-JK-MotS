# Attribution and source boundaries

The supplied original GLB identifies:

- Author: Jonn (https://sketchfab.com/Sketchfab_apk_gratis)
- Title: T 800 low poly (PORT/P3D)
- Model source: https://sketchfab.com/3d-models/t-800-low-poly-portp3d-ce8c971d7b4240229bbebed9b53198b6
- Declared licence: CC-BY-4.0 (https://creativecommons.org/licenses/by/4.0/)
- Generator: Sketchfab-16.75.0

Those are the file's supplied metadata, not an independent verification of
original authorship, upstream port permissions, or the character/franchise rights.
No endorsement by the model author, franchise rights holders or game makers is
implied. Preserve this attribution and the source notice in modified distributions.

Primary conversion checkpoint: Red's user-supplied `t800_jk_v2.zip`. Its original
README and earlier native inputs were preserved in prior checkpoints; this r3
package carries the accepted r2 snapshot instead. Red described fitting to JKE
Kyle's skeleton without including JKE geometry or textures. That description is
not an independently repeated comparison against JKE in this package.

Hybrid integration: Lilitari / Lily, prepared in ChatGPT, September 23, 2026.
Changes: tapered chest narrowing/flattening; rigid head/jaw offset with support
extension; optical extraction and restoration in distant LODs; appended eye
child; forward-lens UVs and a small procedural red MAT with face extra light;
zero-normal front/back separation; radius repair; bounded far-distance hip/hand
proxies; unique material filenames; validated native readback and GLB exports.

Red V3 contributes an implementation idea (eye face extra light), not an asset.
No SFM geometry or texture is included. No generated atlas image is included.
The earlier Lily geometry file supplies proportion guidance, not transplanted
rig/mesh or texture data. The inherited source metadata are retained above. The current r3 input hashes appear in `baseline/INPUT_HASHES.json`.

## Revision r2 / head pilot P1

Lilitari / Lily, September 23, 2026: reduced the previous added neck extension by
32.857%, preserving all core hierarchy fields and existing mesh/UV topology;
authored a surface-normal-based baked chrome pilot using the existing head
material's panel details; added separate geometry-only and textured inspection
exports and native-file comparisons. No new third-party geometry, texture source,
SFM component or image-generated atlas was added. Those r2 hash/reference filenames refer to the prior package. This r3 package
retains the source notice above and its own exact approved-input snapshot.

## Revision r3: compact neck, frozen accepted head P1

Lilitari / Lily, September 23, 2026: geometry-only shortening from the accepted
r2 head-pilot checkpoint. Rigid skull/jaw/eye translation, compressed existing
neck/support band, updated support normals and mesh bounds. No new texture,
source model or SFM asset is added. All five active MATs are copied unchanged.

## Current revision r4: small neck correction and body finish matching

The paragraphs above are the inherited source/revision notice. The current r4
baseline is `baseline/accepted_r3.3do` plus its five accepted MATs, hash-locked in
`baseline/INPUT_HASHES.json`. References above to an r2 snapshot describe r3's
history, not the current baseline file.

Lilitari / Lily, September 23, 2026: lowered the r3 skull/jaw/eyes by another
0.0009 torso-local units with consistent support compression, while keeping all
hierarchy/UV/topology records. Authored surface-aware torso/arm/leg chrome finishes
using the approved P1 head's tonal method. Approved head and lens MATs remain
byte-identical. No SFM source or generated atlas artwork is included or sampled.
