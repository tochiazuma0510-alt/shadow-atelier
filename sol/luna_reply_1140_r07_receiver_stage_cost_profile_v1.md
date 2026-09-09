Luna Task1140: the single authorized v3 metadata profile completed with native exit 0. Largest wall cost was ObserveTree; largest CPU cost was ExpectedInventory. All seven stage endings were durably saved as they completed.

| Stage / original call line | Wall seconds | CPU seconds |
| --- | ---: | ---: |
| 1 CheckPin outer / R370 | 1.985100 | 1.843750 |
| 2 ReadRegistrations / R371 | 0.462059 | 0.500000 |
| 3 ExpectedInventory / R372 | 145.734827 | 136.703125 |
| 4 ObserveTree / R373 | 183.618488 | 125.796875 |
| 5 Missing-directory metadata / R374-375 | 1.046173 | 1.031250 |
| 6 WholeZIP outer / R376 | 65.064218 | 64.015625 |
| 7 AuthenticateDirectoryEvidence / R377 | 111.643235 | 109.734375 |
| Sum of stage intervals | 509.554100 | 439.625000 |

Each stage includes its nested calls; nested costs were not measured separately. Timer record writes are outside the intervals. PID13240 continued concurrently. These data do not identify a single cause of the earlier 638.9175606 versus 665.567737 second intervals or establish a full reception ETA.

The first expensive completed stage was ExpectedInventory, original body R311-340, reported immediately at 00:12:16 JST. One unimplemented candidate is recorded: derive the full in-memory model from the validated partial model plus the two pinned root self-descriptors, instead of repeating InventoryModel over all existing rows at R333 after R326. It still needs a separate equivalence review preserving typed descriptors/paths, OrdinalIgnoreCase file/directory collisions, ordinal arrays, nonempty ancestor sets, rejection behavior and every later fresh hash/boundary. Exact-name dictionary absence is insufficient. No nested speedup or savings estimate is claimed. No repair source was written.

Baseline old74 is 48246 B / 95651f413ed0181c4b04437cce6e37f3752254d81bfab8ef90b82e841290c9a8. R12-368 was extracted verbatim; original R369-379 retained its seven statements and return with timers inserted. Original output/approval/restoration/after-scan main R380-513 was excluded. The four original sibling JSON files were copied byte-for-byte; all eight v3 direct metadata pins, outer ZIP and complete expected inventory were registered before launch. Source/closure/profile/sibling pins remained unchanged after the run. FullPin count was 11439, including 11437 actual files; that counter excludes PinnedJSON hashes and ZIP entry StreamPin calls.

Evidence base: `%TEMP%/shadow-atelier-audit163/task1140/`.

- `profile-source-registration-v1.json`: 8012 B / a9b42fcabe6ceec861c11faeeeb322a009a9d63e76fb84d968898fe803ac8745.
- `profile-input-registration-v1.json`: 10402 B / 4045c0b9c87513ab62bdbe4b269be8d3751c58a2714ff96d6bbe4bca01db911b.
- `profile-final-v1.json`: 3102 B / 8da103d405cb3148dfef1b8c2d9312aa25efcb25541c8ed5afbcddc58c34fd79.
- `stages-v1.jsonl`: 4154 B / b8348b9a90d0ad3481d53f0cb1420ee269ec5ffe67c36d89e51616020dd367bf; seven `stage-N-v1.json` files were saved before the next stage.
- `final-handback-v1.json`: 10098 B / 715bb96813dece8793b999b099e94ebc3f766d53e88177d23ff0ef4043efad70; includes every stage pin, native identity and the single candidate pin.

Native PID3968, process start 2026-09-09T15:09:47.1843586Z, profile end 15:18:17.4182622Z (2026-09-10 00:09:47-00:18:17 JST), exec session56650, launch chunk14ca25, exit0 chunk e2920a. PowerShell 5.1.19041.6456 / Framework 4.0.30319.42000. No retry, additional parent profile, restoration, full receiver launch, Git/GHA/network/credentials, mathematical source execution/import/AST or operation on PID13240/watcher10572 was performed. This is timing evidence only; the continuing root receiver remains the path to formal completion.

TASK1140_VERDICT: ONE_READONLY_PROFILE_COMPLETE; ONE_CANDIDATE_UNIMPLEMENTED; NOT_A_FORMAL_RECEIPT
