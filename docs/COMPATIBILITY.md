# Compatibility and hand behavior

## Multiplayer integration

The model has 24 hierarchy nodes. Original player KEY resources allocate 18 or 19 records. The local builder raises `JOINTS` to at least 24 while preserving animation tracks, markers, timing and other bytes. This provides valid storage for the added child nodes. It also derives the multiplayer model registry and display string from the installed game.

Node 18's mesh reference is set to `-1`; its referenced mesh was already empty at every detail level. All other original-hand geometry, hierarchy values, UVs and materials retain the supplied r4 state.

Original-hand model triangle totals are **4,112 / 3,250 / 2,209 / 1,111**. Holding-curl totals are **4,112 / 3,302 / 2,326 / 1,296**, because it uses the posed close hand at all four body detail levels. The body outside the four hand mesh blocks is byte-identical between the two poses.

This is a selectable multiplayer model. There are no campaign-player replacement aliases (`ky.3do`, `kk.3do`, or `mj.3do`). Other mods that change the same animation, registry or menu resources require a compatibility merge. Do not stack them blindly in the same mod folder.

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
