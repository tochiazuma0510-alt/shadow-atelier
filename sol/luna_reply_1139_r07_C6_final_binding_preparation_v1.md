# Task1139 - C6 final binding preparation

F1. READY_FOR_ROOT_INPUT (preparation only). Read Task1139/Task1110, applicable AGENTS.md, latest dialogue T-70, and the C binding consumers as raw text. Formal restored inventory five fields and the final P6 opaque pin remain absent. No binder or final source was created; normal admission remains closed at C line 686. No receipt acceptance or launch readiness is inferred.

The baseline is `%TEMP%/shadow-atelier-audit163/task1125/search/check_d972_r07_fixed_lambda_cycle_batch_v6.py`: **427740 B / a5c449721663940ed2155f90980eb7422999cbaa6af466512e95a0819cd02f58**. Its public range map `%TEMP%/shadow-atelier-audit163/task1125/public-opaque-current-ranges-v1.json` is **146590 B / bd744394ef0f17d90b3ba3ad57525cceb2406b132916548d6a3c9a3afc957396**. Both raw pins match.

F2. Exactly two RHS substitutions suffice; annotations and newlines stay unchanged. Offsets are zero-based bytes of the pinned baseline.

| Binding | Line | Old interval | Required replacement |
|---|---:|---|---|
| `THIRD_BATCH_INVENTORY_REGISTRATION` | 264 | `[21826,21830)` = `None` | One-line ASCII dictionary with exactly `files`, `file_bytes`, `directories`, `files_sha256`, `directories_sha256` |
| `CURRENT_PRODUCER_REGISTRATION` | 265 | `[21886,21890)` = `None` | One-line ASCII dictionary with exactly `file`, `bytes`, `sha256` |

Both old RHS hashes are `dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91`. Before substitution, pin the explicitly root-supplied registration and P-pin input files by bytes/SHA. Reject absent, extra, duplicate, or wrongly typed fields. Counts/bytes must be ordinary nonnegative integers (exclude bool/float/null/string); hashes must be lowercase 64-hex strings. Require P `file` exactly `search/d972_r07_fixed_lambda_cycle_batch_v6.py`. Use only root's accepted formal fields and opaque P tuple; never derive inventory from cached/acquisition metadata or read P body. These input-shape checks do not establish the full typed receipt.

F3. Binding consumers need no edits:

- Direct references: inventory at 264/686/2656; P pin at 265/686/721. The unchanged 686 guard precedes normal admission.
- Formal inventory: `AcceptedInputs` 704 creates `PinnedTree`; 829-857 checks sorted unique names, all actual directories and every file's full hash. The 737 -> 2797 -> 2656 -> 2632-2650 chain binds all five registered fields, ordinary types, total file bytes, canonical full-file-array hash and canonical directory-array hash. No historical registry value is substituted.
- P: 668-672 checks exact descriptor keys/types and public path; 721 compares the complete opaque tuple. The 725-744 closure authenticates actual source bytes; 776-780 and 4724 authenticate them again at exit. This describes existing runtime code; none was executed here.
- Propagation: 3477-3494 binds accepted `code` into layout/source/owner; 3548-3554 and 4622-4629 compare the corresponding complete/partial root records. The 4275-4287 consumer compares parents/code before/after inventories. No serializer, historical P/C pin, or runtime guard change is needed.

F4. Exact future raw construction, with `B` the baseline and `I`, `P` the validated one-line replacement bytes:

`final = B[0:21826] || I || B[21830:21886] || P || B[21890:427740]`.

Let `delta = len(I) + len(P) - 8`. Final bytes are `427740 + delta`; PREAMBLE remains at offset 0 with `26217 + delta` bytes and a newly measured hash. All other 164 public region offsets gain `delta`, while their lengths/hashes and all line coordinates remain unchanged. Raw .NET hashing confirmed all 165 current regions, contiguous coverage to EOF, and all 24 retained current regions (4 old loaders + 20 bodies). The earliest retained offset is 28956, so neither replacement intersects a retained region. Keep every old historical registry and retained source byte verbatim.

After actual inputs arrive, create only new files under `%TEMP%/shadow-atelier-audit163/task1139/`: final `search/check_d972_r07_fixed_lambda_cycle_batch_v6.py`, exact two-region raw delta/full-source pin, and public opaque 165-region/retained24 coordinates. Use `FileMode.CreateNew`; assert the exact concatenation, unchanged complement and all retained hashes. Carry the previous public baseline/history records unchanged. Final receipt adoption, independent final read, repository placement and Git/GHA remain root work; this preparation adds no approval gate.

F5. Reproduction of the raw locations/pins and region counts (PowerShell/.NET only):

```powershell
$cPath = Join-Path $env:TEMP 'shadow-atelier-audit163/task1125/search/check_d972_r07_fixed_lambda_cycle_batch_v6.py'
$rPath = Join-Path $env:TEMP 'shadow-atelier-audit163/task1125/public-opaque-current-ranges-v1.json'
Get-Item -LiteralPath $cPath,$rPath | Select-Object FullName,Length
Get-FileHash -LiteralPath $cPath,$rPath -Algorithm SHA256
$cRaw = [IO.File]::ReadAllBytes($cPath)
[Text.Encoding]::UTF8.GetString($cRaw,21826,4)
[Text.Encoding]::UTF8.GetString($cRaw,21886,4)
$rObj = Get-Content -LiteralPath $rPath -Encoding UTF8 -Raw | ConvertFrom-Json
$rObj.regions.Count
$rObj.retained.regions | Group-Object group | Select-Object Name,Count
$cHash = [Security.Cryptography.SHA256]::Create()
foreach ($q in @($rObj.regions) + @($rObj.retained.regions.current)) {
  $digest = [BitConverter]::ToString($cHash.ComputeHash($cRaw,[int]$q.offset,[int]$q.bytes)).Replace('-','').ToLowerInvariant()
  if ($digest -cne $q.sha256) { throw 'raw region mismatch' }
}
$cHash.Dispose()
rg -n 'THIRD_BATCH_INVENTORY_REGISTRATION|CURRENT_PRODUCER_REGISTRATION' -- $cPath
```

No mathematical source execution/import/AST/compile/selftest, P private read, network, credentials, process operation, or implementation edit occurred. The root-adopted C public selftest GHA34220805430/1 is carried from the task only; it was not repeated. No commit or run was produced. Operational deviation: the initial independent read batch included read-only `git status --short` before Task1139's stricter no-Git clause had been read. No Git mutation occurred and no further Git command was used. This reply is the only task-created workspace file.

TASK1139_VERDICT: READY_FOR_ROOT_FORMAL5_AND_FINAL_P_OPAQUE_PIN; TWO_RHS_ONLY; FINAL_SOURCE_NOT_CREATED; NORMAL_GUARD_CLOSED; SOURCE_EXECUTION_0

F6. Follow-up source-only delivery (2026-09-10 JST). Root requested an activation-ready metadata binder while Task1137 full RECEIVE continues. Formal/native completion and final P adoption are still absent. The following immutable files were created under `%TEMP%/shadow-atelier-audit163/task1139/` without executing the binder:

| Authoritative file | Bytes | SHA256 |
|---|---:|---|
| `bind-final-c6-metadata-v2.ps1` | 15083 | `23e375d6ff87e54d18de5dd323a4da54a0f9ad1385a48a9bc70a33232a54c937` |
| `bind-final-c6-metadata-contract-v1.md` | 5710 | `95a042fe71ba95105fc389a41483cfa7378a1bc9be0ac31960cb776947cc45d9` |

`bind-final-c6-metadata-v1.ps1` is an immutable superseded construction draft (15088 B / `8280e8270c5d17f5d930445cde45e8a94d36e0dbeaab0e94b1983aae6d3dfd4e`). Use v2 only. The v2 source contains 225 LF and zero non-ASCII bytes. Pins and these byte properties were inspected as data; no parser, binder, or mathematical source was executed. Reproduce pins with `Get-FileHash -LiteralPath <file> -Algorithm SHA256` and sizes with `(Get-Item -LiteralPath <file>).Length`.

F7. The mandatory CLI accepts explicitly pinned formal5, P-descriptor and root-adoption JSON triples. The contract specifies strict flat JSON: exactly five / three / fifteen keys respectively, duplicate/extra/wrong-type rejection, ordinary nonnegative Int64 counts, lowercase hashes, and unescaped forward-slash local path strings. The root-adoption document joins the actual formal5/P-pin files and an actual completed public handback JSON file by absolute path/bytes/SHA, requires the frozen parent run/attempt/artifact, and states `FULL_FORMAL_NATIVE_COMPLETE_AND_FINAL_P_ADOPTED`. The handback is hashed as opaque public metadata, not interpreted as an independent completion proof. Root remains responsible for the truth and adoption of its completed receipt. The P executable's file field is never opened.

All input pin/type checks, construction, reverse byte equality, LF counts, original/final EOF and region hashes finish before any output is created. The exact two RHS replacements remain the only C edits. Existing source-author schema literals are carried unchanged; raw textual edits update only source/current pins, PREAMBLE bytes/hash, and current offsets. Historical JSON bytes and all other C bytes are preserved. No selftest is repeated.

F8. On later root activation only, the binder creates a fresh version directory below Task1139 with the final C source, full-source pin, exact forward/reverse base64 raw delta, full public165/retained24 map, and a binding receipt written last. Every file uses CreateNew; existing versions are rejected. The result is `BOUND_METADATA_ONLY`, with C source execution 0, P source opened false, and verified false. This delivery adds no approval gate and performs no placement or launch.

Current state: binder execution 0; C execution/import/compile/AST/selftest 0; P private access 0; final C file not materialized; normal baseline guard remains closed. No Git/GHA/network/credential/process operation was used in this follow-up. Only the designated reply was appended in the workspace; the three new immutable files are outside the repository. Source/contract pins were sent to root for static review.

TASK1139_VERDICT: METADATA_BINDER_SOURCE_V2_READY_FOR_ROOT_STATIC_REVIEW; AWAIT_ACTUAL_COMPLETED_HANDBACK_AND_FINAL_P; BINDER_EXECUTION_0; FINAL_C_NOT_CREATED
