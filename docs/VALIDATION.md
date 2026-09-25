# Validation record

Prepared September 25, 2026. These are the boundaries of the work performed for this release.

## Runtime observations

Tests ran the original game executables in a private Debian 12 / Wine 8 i386 environment with Xvfb and Mesa llvmpipe. The test profiles selected **1280×960, 8bpp**, with **3D acceleration unchecked** in the actual game display menu. The game engines and COGs were not modified. Native DirectPlay components were used inside the private Wine prefix to make hosting work.

| Game and variant | Observed |
| --- | --- |
| Original JK 1.01; indexed; original hand | Multiplayer character preview and hosted multiplayer rendering. |
| Original MotS `JKM.EXE`; indexed; original hand | Multiplayer character preview and hosted multiplayer rendering. |
| Original JK 1.01; indexed; holding curl | T-800 selected and saved; hosted Canyon Oasis; third-person body/arms; movement; Bryar firing (ammo 50 → 44 and visible projectile); saber idle and swing. |
| Original MotS `JKM.EXE`; indexed; holding curl | T-800 selected and saved; hosted Tibanna Mining Outpost; third-person body/arms; forward movement; saber attack. |
| RGB565 materials, both poses | Assets and packaging checked. Earlier original-hand renderer observations do not establish a multiplayer pass. The holding-curl RGB565 variant has no runtime test. |

The two holding-curl runs ended through intentional test-harness shutdown after observation. They were not recorded as game crashes. Game screenshots in the README come from those runs.

Only one hosted player was required and tested. There was **no second connected client**. No full native Windows/GPU matrix, complete weapon/animation survey, custom-palette survey, or network synchronization certification is claimed. Tests do not establish every runtime LOD transition.

## Asset checks

- Native 3DO parsing, hierarchy and geometry limits checked for all four detail levels.
- All five MATs checked for format, dimensions and four mip levels.
- Original RGB565 MATs retain the supplied r4 bytes; indexed assets were generated for each game's default palette.
- Animation edits preserve tracks, timing and markers while raising allocation to 24 nodes where required.
- The original-hand model changes only the empty node reference from the supplied r4 model.
- The holding-curl model preserves every byte outside the four hand mesh blocks. Mesh counts, fixed palm/wrist, rigid segment lengths and collision observations were checked; pre-existing proximal joint overlaps remain.
- Blender-Sith parser read all four geosets. Blender `bpy` 5.1.2 import/save/reopen checked the editable geoset-0 scene.

## Model identity

| Asset | SHA-256 |
| --- | --- |
| Original-hand playable 3DO | `adbd2daa4aadf485e964f2e421bf3974223c0af5eb12969a0a6761df35bd3a40` |
| Optional holding-curl 3DO | `52c0ecc7e7d6b531f5f41528a99f9dd686ea826f498b8e35a076488279054b92` |

The release's `SHA256SUMS.txt` inventories the public files. Installer asset hashes are recorded in `tools/asset-hashes.json`. Installed files receive a local receipt for verification and guarded removal.

## Public packaging

The public release ships custom assets and tools. Stock animation and registry resources are built locally from an owned game installation. Private development logs, account conversations, game executables, original resource archives, DLLs, profiles and saves are excluded.

The standalone public installer was checked against the completed local packages in all **eight combinations**: two games × two poses × two material formats. Every generated resource matched byte for byte: **512 files for each JK variant** and **710 for each MotS variant**. Build reports and installation receipts are additional bookkeeping files.

All eight install → verify → uninstall cycles passed. Existing-destination refusal, modified-file refusal before any deletion, and unrelated-file preservation passed for each variant. A total of 25 refusal checks passed. All four source game archives retained their hashes. Both PowerShell wrappers parsed with Windows PowerShell 5.1; the install/remove wrapper ran successfully, and the launcher accepted the generated receipt and reached the correct executable/arguments with process creation intercepted for this packaging check.
