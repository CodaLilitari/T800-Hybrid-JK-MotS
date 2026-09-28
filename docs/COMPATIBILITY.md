# Compatibility and hand behavior

## Multiplayer integration

The model has 24 hierarchy nodes. Original player KEY resources allocate 18 or 19 records. The local builder raises `JOINTS` to at least 24 while preserving animation tracks, markers, timing and other bytes. This provides valid storage for the added child nodes. It also derives the multiplayer model registry and display string from the installed game.

Node 18's mesh reference is set to `-1`; its referenced mesh was already empty at every detail level. The v1.0.1 leg-only patch retains the playable 24-node hierarchy, all joint positions and pivots exactly. The original-hand option is the approved original **hand pose on the body with repaired leg pistons**.

Frozen V7 triangle totals are **4,258 / 3,396 / 2,355 / 1,316** for the original hand and **4,258 / 3,448 / 2,472 / 1,501** for the holding curl. The curl uses its posed close hand at all four body detail levels. The models differ only in the four right-hand mesh 10 blocks. The largest individual mesh has **306 vertices, 587 UV coordinates and 399 faces**, below the respective **512 / 768 / 512** limits.

This is a selectable multiplayer model. There are no campaign-player replacement aliases (`ky.3do`, `kk.3do`, or `mj.3do`). Other mods that change the same animation, registry or menu resources require a compatibility merge. Do not stack them blindly in the same mod folder.

## Leg piston repair; original neck restored

The leg piston shells originally included complementary faces on independently animated hip and thigh parts. Those original faces now move together with each thigh. Narrow closed continuations connect their upper ends into compact hip guides, whose dimensions account for stock thigh translations. The visible guide edge inside the pelvic opening is a deliberate geometry addition.

Only hip and thigh mesh blocks 0, 6 and 12 change from v1.0.0. Every other mesh block is restored byte-for-byte, including the original neck and cables, skull at all four detail levels, head placement, torso, clavicles, arms and both hand options. The experimental neck supports and shape changes are excluded. **Original neck animation behavior is retained; no neck-cable repair is claimed.**

All four native LODs remain. The coarsest hip/thigh region uses the repaired next-finer source meshes because the original coarse proxy fused the split parts. The original coarsest skull is restored exactly. Parser coverage of all four LODs does not establish every runtime transition.

The leg checks cover the stock MotS player animation domain. Arbitrary custom KEYs can move joints outside that domain and are not covered. Existing animation tracks and COG/engine behavior are unchanged.

**Final V7 runtime passed bounded checks with indexed materials: original hand in JK 1.01 and holding curl in MotS.** See [VALIDATION.md](VALIDATION.md) for exact hashes, observed actions, source and installer checks, and earlier weapon-survey scope. RGB565 remains package-checked.

## Materials

The five RGB565 MAT files retain the supplied r4 bytes. The indexed variants were quantized separately against JK's and MotS's default colormaps. They retain the source dimensions and all four mip levels. A custom level colormap can change their colors.

## Optional hand pose

The holding curl moves 116 existing close-hand vertices in 15 rigid groups; 126 vertices remain fixed. Palm, wrist, attachment and the original mesh topology/UVs are preserved. The close hand still has 242 vertices and 247 triangles. No cover, added hand face or finger scaling was introduced.

The result is a compact open grip. The fingertip row remains somewhat planar; it is not intended to read as a tightly clenched fist. The original hand remains the default installation option.

## Why a stock flesh-colored weapon hand can remain

In the original games, the external weapon model contains its own hand faces alongside the gun or saber hilt. Changing the player-body hand does not remove those faces. Replacing the shared weapon model or material would affect other skins that use it; first-person views are separate as well.

No supported per-skin removal route was established without engine, COG or shared-weapon changes. The holding curl is a pose choice, not a reliable concealment mechanism. Those shared resources remain unchanged here.

Relevant historical Massassi discussions:

- [Invisible hand](https://forums.massassi.net/Editing_Forums/Jedi_Knight_and_Mysteries_of_the_Sith_Editing_Forum/thread_32774_page_1.html)
- [Empty Hands](https://forums.massassi.net/Editing_Forums/Jedi_Knight_and_Mysteries_of_the_Sith_Editing_Forum/thread_53913_page_1.html)
- [First-person problems](https://forums.massassi.net/Editing_Forums/Jedi_Knight_and_Mysteries_of_the_Sith_Editing_Forum/thread_35188_page_1.html)

These informed the investigation alongside local resource and engine-source inspection; they are not a claim that every discussion describes a skin-specific solution.
