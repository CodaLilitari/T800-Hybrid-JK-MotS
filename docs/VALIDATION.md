# Validation record

The final v1.0.1 models, internally labeled V7, contain the leg piston repair and an exact restoration of every non-leg section to v1.0.0. Source and installer checks passed. Bounded final-model runtime checks passed with indexed materials: original hand in JK 1.01 and holding curl in MotS. Archive verification requirements are described separately below.

## v1.0.1 model identity

| Hand choice | SHA-256 |
| --- | --- |
| Original hand, repaired leg pistons | `00a0b7f4876a7ae1e03159dc46ad6a390405e62328dd16f731ad08dbfa2ce90d` |
| Holding curl, repaired leg pistons | `970329404b446c5ad9b5dd68cb75355ced109c53b6fb8e57c085db151a322e6a` |

“Original” refers to the hand pose. Both choices include the same leg repair and restored original neck. The two files differ only in their right-hand mesh 10 blocks across the four LODs.

| Variant | LOD0 triangles | LOD1 | LOD2 | LOD3 |
| --- | ---: | ---: | ---: | ---: |
| Original hand | 4,258 | 3,396 | 2,355 | 1,316 |
| Holding curl | 4,258 | 3,448 | 2,472 | 1,501 |

The per-mesh maxima are **306 vertices, 587 UV coordinates and 399 faces**, below the respective **512 / 768 / 512** limits.

## v1.0.1 source and asset checks — complete

### Exact scope and neck restoration

The final V7 files start from the corresponding approved v1.0.0 models. Only hip and thigh mesh blocks **0, 6 and 12 at each of four LODs** are replaced with the validated leg-repair blocks. Independent reconstruction reproduces each entire final byte stream exactly from those inputs. Reversing the twelve leg substitutions reproduces each complete v1.0.0 file.

This proves exact preservation of all non-leg meshes and every header, hierarchy, material-list and other record. It restores the entire original neck and cables, head placement, skull including its original LOD3, face, eyes, jaw, ears, torso, clavicles, arms, hands, UVs and material assignments. The experimental neck redesign is excluded. **Original neck animation behavior is retained; this release does not claim a neck-cable fix.**

The original piston shell faces now follow their corresponding thighs. Narrow closed continuations seat their upper ends inside hip guides. These leg meshes and their hierarchy are byte-identical to the earlier validated leg candidate, so its source seating, topology and stock-animation bounds apply directly. The remaining intermediate neck geometry and its validation claims are not part of V7.

### Native model checks

- Native parsing and the Blender-Sith parser read all four geosets and all 24 hierarchy nodes. The approved hand choices remain exact.
- Indices, finite coordinates, degeneracy, face normals, geometry limits and hierarchy compatibility pass. The pre-existing unused empty mesh 16 is omitted only from an explicit validation view; the authored model retains it exactly. The generic aggregate validator is not described as an unqualified pass.
- All 16 leg parts added across the four LODs are closed, manifold and consistently wound, with positive volume. Original decorative surfaces elsewhere are not claimed to be watertight.
- Every mesh radius covers its vertices. The original global model radius **0.144252** is retained and covers the maximum bind-space vertex radius **0.124270833 native units**. No header-bound adjustment was needed.
- The coarsest hip/thigh region uses the repaired next-finer source meshes where the old proxy fused the damaged parts. The original coarsest head and every other non-leg LOD are restored exactly.
- All 20 public MAT files retain v1.0.0 bytes. Indexed materials remain genuine 8-bit assets for the separate JK and MotS default palettes. RGB565 materials retain the supplied r4 bytes. Source dimensions and all four mip levels are preserved.

### Leg seating and animation bounds

The owned stock MotS player PUP references 63 distinct keys; adding standing saber block gives **64 files**. Both ends of every native position/deltaPosition interval, plus bind, provide **1,081 left-thigh and 1,069 right-thigh position samples**. This checks complete linear translation intervals, beyond selected screenshot poses.

The hip guides were generated from those positions with a small padding. Independent parsing of the exported leg geometry verifies that all required endpoint positions are strictly inside every guide face plane, with a minimum margin of approximately **0.000375255 native units**. Export rounding produces tiny deviations from exact convexity (maximum measured vertex/plane deviation approximately **0.0000000525**). The positive endpoint margin is much larger, and the linear intervals remain within the same face-plane bounds. Local thigh rotation does not move the continuation's endpoint away from its joint origin.

Each continuation axis crosses an actual original piston cap surface with strictly interior triangle coordinates. Each guide overlaps the original closed hip volume at every LOD, with verified positive interior clearance. These checks separately address the original piston end, its animated seating and the guide's attachment to the pelvis.

A source pose regression covers **64 keys × 16 samples = 1,024 poses**, or **2,048 endpoint tests**. Every sample retains positive guide seating; the minimum exported margin is **0.0003752517 native units**. Eight global yaw angles change the measured margin by less than **0.00000000000000001 native units**. The exact V7 leg blocks and hierarchy retain this measured geometry without alteration; the regression is carried by byte identity, not mislabeled as a new V7 runtime test.

### Source visual review and toolchain

Matched-camera textured source renders with explicit backface culling were inspected for leg stand, run, crouch and turn, with close isolated views of both upper mounts. The small bright guide edge inside the pelvic opening is a deliberate addition. These exact leg meshes are retained in V7.

Source geometry and interval checks do not certify every PUP priority mixture, custom KEY, light/camera condition or continuous runtime LOD transition. Native-unit measurements do not assume a physical millimetre scale.

Blender-Sith's parser reads all four geosets; its Blender scene importer imports geoset 0. The project copy matched upstream HEAD [`ecc9013`](https://github.com/smlu/blender-sith/commit/ecc90131bcfdeabd400225e8a72ce94cbff1ec5c) when checked on September 27 local time (September 28 UTC), one commit newer than `v1.0.0-rc4`. Import/save/reopen of the editable scene was checked with Blender `bpy` 5.1.2; that earlier scene round trip is separate from the final V7 native parser check.

## v1.0.1 runtime observations

The completed JK observation uses the original-hand V7 hash above; MotS uses the holding-curl V7 hash. Each row preserves its game, hand, material and model-revision scope.

| Evidence set | Status and permitted interpretation |
| --- | --- |
| Final V7; original JK 1.01; indexed; original hand | **Passed bounded check:** T-800 selection, single-host multiplayer in Canyon Oasis, restored neck and textured body/leg rendering, short movement and turns, crouch/down-look poses, and a visible saber attack. Display menu confirmed 1280×960, 8bpp and 3D acceleration unchecked. |
| Final V7; original MotS `JKM.EXE`; indexed; holding curl | **Passed bounded check:** single-host multiplayer in a private test level derived from Tibanna Mining Outpost, restored neck and leg rendering, a short forward run, crouch, left/right turns, up/down aim, several external-camera angles, and a visible saber swing with wall impact. Display menu confirmed 1280×960, 8bpp and 3D acceleration unchecked. |
| Original-neck MotS weapon appearance survey | Covers all **16 portable selections plus mounted EWEB**, with scoped mode checked separately. Neck, arms and hands match the restored geometry. It predates the leg-only patch and is not an all-weapons observation of the V7 hashes. |
| README game images | Both show final V7: JK original hand in Canyon Oasis, and MotS holding curl in the private test level. The hand-pose comparison remains the labeled v1.0.0 source render because its hand geometry is unchanged. |
| V7 RGB565 runtime | **No final-hash runtime result recorded here.** Material and installer checks are complete and separate. |

Portable selections include fists, lightsaber, Bryar and BlasTech pistols, normal and scoped Stormtrooper rifle, thermal detonator, flash bomb, bowcaster, repeater, ordinary and seeking rail detonators, proximity and manual sequencers, concussion rifle and carbonite gun. Mounted EWEB is a separate observation; rider contact is imperfect. Intermediate neck experiments are excluded from the release and their runtime observations are not presented as V7 validation.

The final JK run reverified **513 source/overlay files** and preserved its original executable and installed mod. No game crash was observed and no new debug warnings appeared relative to the earlier comparison run. The bounded test ended through a requested harness shutdown, not a normal in-game quit; its tagged processes and private display lock were cleared. The selected movement screenshot was captured after movement, so it is not presented as a frozen running pose or proof of every mechanical contact angle.

The final MotS run bound its installed model to the exact holding-curl hash and verified its stock source, copied game files and preserved original executable. After the run, **711 overlay members** were reverified: the 710 mod resources and one private test-level archive. The sampled actions used a 0.2-second forward run, 0.4-second crouch and 0.25-second turns in each direction. The primary attack was an observed saber swing and wall hit. The restored original neck and leg surfaces remained visible at the sampled game scale and camera angles. The test level changes placements while retaining stock COG bytes and is not distributed in the release. The run recorded no failure and ended through a requested bounded stop; the game, Wine, private display and audio processes ended, and its temporary media mount was removed successfully.

Stock weapon models retain their separate flesh-colored hands, and first-person views remain the stock game views. Scoped rifle mode forces first person and intercepts the ordinary camera toggle; no third-person scoped grip is inferred. Empty trigger-only sequencer state and every weapon's firing/alternate-fire animation are outside the passive appearance survey.

Runtime observations use original game executables in isolated Debian 12 / Wine 8 i386 sessions with Xvfb and Mesa llvmpipe, without a graphics wrapper. Both completed checks used software rendering as confirmed in the game menus. Only one hosted player was required. There is no second-client result or full Windows/GPU/network, colormap or multiplayer-synchronization certification. Sampled rendering and actions do not establish every animation, weapon, map, mechanical contact angle or runtime LOD transition. Original neck animation behavior remains by request.

## v1.0.1 installer checks

The frozen V7 models were tested through the unchanged public installer in an isolated copy of the release files. The two models and their asset-manifest entries were updated there; the existing installer, launchers and all 20 MAT files were preserved. The installer continues to derive the required 24-node KEY allocation and multiplayer registry/string resources locally from an owned game installation. The leg patch adds no animation-resource change.

The V7 packaging gate passed all **eight combinations**: two games × two hand poses × two material formats.

| Builds | Game resources per build | Byte-identical resources | Only changed game resource |
| --- | ---: | ---: | --- |
| JK: both hands × indexed/RGB565 | 512 | 511 | `3do/t800hy4.3do`, matching the selected frozen V7 hash |
| MotS: both hands × indexed/RGB565 | 710 | 709 | `3do/t800hy4.3do`, matching the selected frozen V7 hash |

Every other game resource remained byte-identical, including the five selected MATs and stock-derived animation/registry/string resources. Stable build-report semantics were preserved. All 20 public MAT files and all three public installer/launcher scripts retained their v1.0.0 bytes.

Representative **install → verify → uninstall** cycles passed for each game with indexed holding-curl assets. The installed receipts contained the exact frozen curl-model hash. Owned files were removed and unrelated files both inside and beside the installation were preserved. These two lifecycle runs complement the eight build/hash comparisons; they are not described as eight repeated lifecycle runs. All four source game archives retained their before/after hashes. No game process was started by this installer gate.

### Release archive verification requirements

Before publication, build the ZIP from the reviewed Git release commit. Require a successful archive CRC check, the exact expected member list, and byte-for-byte equality between every archived file and the corresponding committed file. Verify the internal checksum manifest and the separate SHA-256 checksum sidecar for the ZIP. These requirements apply to the finished archive; the installer checks above are a separate result.

The release checksum manifest covers the public files, and the asset manifest covers two models and 20 MATs. Installed files receive a local receipt for verification and guarded removal. Original game archives, executable/DLL files, profiles, saves, test fixtures, raw review conversations and development logs remain outside the public release.

## Historical v1.0.0 validation — September 25, 2026

The observations, model hashes and packaging counts below apply to **v1.0.0 only**. Current README captions identify each image's model revision. Claims that the original model changed only its empty node reference describe that earlier revision, not the v1.0.1 body repair.

### Runtime observations

Tests ran the original game executables in a private Debian 12 / Wine 8 i386 environment with Xvfb and Mesa llvmpipe. The test profiles selected **1280×960, 8bpp**, with **3D acceleration unchecked** in the actual game display menu. The game engines and COGs were not modified. Native DirectPlay components were used inside the private Wine prefix to make hosting work.

| Game and variant | Observed |
| --- | --- |
| Original JK 1.01; indexed; original hand | Multiplayer character preview and hosted multiplayer rendering. |
| Original MotS `JKM.EXE`; indexed; original hand | Multiplayer character preview and hosted multiplayer rendering. |
| Original JK 1.01; indexed; holding curl | T-800 selected and saved; hosted Canyon Oasis; third-person body/arms; movement; Bryar firing (ammo 50 → 44 and visible projectile); saber idle and swing. |
| Original MotS `JKM.EXE`; indexed; holding curl | T-800 selected and saved; hosted Tibanna Mining Outpost; third-person body/arms; forward movement; saber attack. |
| RGB565 materials, both poses | Assets and packaging checked. Earlier original-hand renderer observations do not establish a multiplayer pass. The holding-curl RGB565 variant has no runtime test. |

The two holding-curl runs ended through intentional test-harness shutdown after observation. They were not recorded as game crashes. Historical v1.0.0 screenshot examples originate from those runs.

Only one hosted player was required and tested. There was **no second connected client**. No full native Windows/GPU matrix, complete weapon/animation survey, custom-palette survey, or network synchronization certification is claimed. Tests do not establish every runtime LOD transition.

### Asset checks

- Native 3DO parsing, hierarchy and geometry limits checked for all four detail levels.
- All five MATs checked for format, dimensions and four mip levels.
- Original RGB565 MATs retain the supplied r4 bytes; indexed assets were generated for each game's default palette.
- Animation edits preserve tracks, timing and markers while raising allocation to 24 nodes where required.
- The original-hand model changes only the empty node reference from the supplied r4 model.
- The holding-curl model preserves every byte outside the four hand mesh blocks. Mesh counts, fixed palm/wrist, rigid segment lengths and collision observations were checked; pre-existing proximal joint overlaps remain.
- Blender-Sith parser read all four geosets. Blender `bpy` 5.1.2 import/save/reopen checked the editable geoset-0 scene.

### Model identity

| Asset | SHA-256 |
| --- | --- |
| Original-hand playable 3DO | `adbd2daa4aadf485e964f2e421bf3974223c0af5eb12969a0a6761df35bd3a40` |
| Optional holding-curl 3DO | `52c0ecc7e7d6b531f5f41528a99f9dd686ea826f498b8e35a076488279054b92` |

The release's `SHA256SUMS.txt` inventories the public files. Installer asset hashes are recorded in `tools/asset-hashes.json`. Installed files receive a local receipt for verification and guarded removal.

### Public packaging

The public release ships custom assets and tools. Stock animation and registry resources are built locally from an owned game installation. Private development logs, account conversations, game executables, original resource archives, DLLs, profiles and saves are excluded.

The standalone public installer was checked against the completed local packages in all **eight combinations**: two games × two poses × two material formats. Every generated resource matched byte for byte: **512 files for each JK variant** and **710 for each MotS variant**. Build reports and installation receipts are additional bookkeeping files.

All eight install → verify → uninstall cycles passed. Existing-destination refusal, modified-file refusal before any deletion, and unrelated-file preservation passed for each variant. A total of 25 refusal checks passed. All four source game archives retained their hashes. Both PowerShell wrappers parsed with Windows PowerShell 5.1; the install/remove wrapper ran successfully, and the launcher accepted the generated receipt and reached the correct executable/arguments with process creation intercepted for this packaging check.
