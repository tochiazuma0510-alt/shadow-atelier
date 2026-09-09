# Task1138 reply - P6 final binding prepared

F1. The remaining P source change is exactly two raw token replacements. A separate binder is unnecessary for these two tokens; the pending patch sheet is `%TEMP%/shadow-atelier-audit163/task1138/P6-final-binding-pending-raw-patches-v1.json` (**13445 B / 670ac6961170aa788a82c9d3333ca9ecf17ca8f12e499ffd08eb00e6bde3fbc6**). It records exact old spans, three unchanged-span hashes, named pending inputs and source/range update rules. No bound or dummy P source has been created.

Baseline rehashed: `%TEMP%/shadow-atelier-audit163/task1109/d972_r07_fixed_lambda_cycle_batch_v6.py`, **453749 B / 75401d4ded04e00187e9a45bfe87603309473a7c6625e6747ecf5c3bf4caa0d7**. Current line586 remains `BATCH_V5_INVENTORY_REGISTRATION = None`; line588 remains `IMPLEMENTATION_COMPLETE = False`.

F2. Exact pending patches (zero-based byte offsets)

| Offset / old bytes | Actual old token | Replacement after authentic root input |
| --- | --- | --- |
| 32326 / 4, line586 | `None` | `{"files":<FILES>,"file_bytes":<FILE_BYTES>,"directories":<DIRECTORIES>,"files_sha256":"<FILES_SHA256>","directories_sha256":"<DIRECTORIES_SHA256>"}` |
| 32458 / 5, line588 | `False` | `True` at root final binding |

The angle-bracket names are pending inputs, not fabricated values or executable source. Root supplies the authentic five-field registration file and its expected bytes/SHA; pin first, require exactly five unique fields, ordinary integers >=1 for the three counts (never bool or coercion), and lowercase 64-hex strings for the two list hashes. A file pin alone does not establish formal receipt validity. Public C source pin is not an input to P.

F3. The actual consumer is `authenticate_batch_v5_parent` line3528, reached from `authenticate_acceptance` line3777. The latter first reconstructs the whole actual inventory and compares it with the acceptance parent at lines3752-3753. `batch_v5_inventory_registration` lines3001-3012 then checks exact five keys/types and all five values: file count, sum of file bytes, directory count, and SHA256 of each complete canonical list. `integer` rejects bool; `canonical` uses ASCII compact JSON, sorted keys and one final LF. No consumer function or schema change is needed.

`run_actual` line5611 is the only guard consumer and remains closed before output creation. The existing fifth-group fixtures at lines6516/6521 pass their own local registration, so formal binding adds no fixture edits or rerun here. Task1138's root-adopted GHA34228241894/1 result is not being rerun or extended.

F4. Let N be the actual one-line registration literal's ASCII byte length, with no LF. Total delta is N-5 and final source bytes are 453744+N. All 6721 line numbers/LF remain unchanged. Of the published 177 source regions, only `<prefix>` changes content: offset0, bytes32599+N, newly measured SHA. The other 176 regions retain raw bytes/hash/line numbers and shift offsets by N-5; apply the same shift to all 37 retained-body, four original-loader and 25 native-reader current descriptors. Keep all prior/baseline descriptors unchanged. The patch sheet pins the existing public range file and specifies exact full-EOF forward/reverse reconstruction.

On the actual follow-up, write the source, exact raw delta, full pins and updated public opaque ranges with CreateNew under task1138. Root must propagate the new P descriptor to `acceptance.code.producer` and exterior driver/WF pins: P's `authenticate_code`/`checked_descriptor` compare that descriptor with the actual source bytes; there is no extra literal P self-hash to patch. This is the existing root binding step, not a new approval gate. No unresolved P source consumer was found; the formal registration with expected bytes/SHA remains the missing input.

F5. Preparation used only own P raw text, hashes and public metadata. No P import/execution/AST/compile/selftest, C private body, mathematical calculation, network, credential access, process action, deployment or GHA action occurred. At startup I issued one read-only `git status --short` concurrently with reading Task1138, before seeing its no-Git restriction; no subsequent Git command or Git mutation was performed. Only this reply and the pending patch sheet were created; root can perform the final worktree audit. The P baseline remains guardclosed and unchanged.

TASK1138_VERDICT: FINAL_BINDING_PATCHES_PREPARED_GUARDCLOSED_FORMAL_INPUT_PENDING
