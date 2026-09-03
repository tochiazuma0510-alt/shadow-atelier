# Sol(max) Task744 - independent audit of grade-two maps checker v4

## Verdict

```text
VERDICT=PASS_GRADE2_MAPS_CHECKER_V4_SAFE_FOR_GHA
SAFE_TO_DISPATCH_GHA=yes
CLASSIFICATION=FINITE_CHECKER_RECEIPT_KEY_REPAIR
ACTUAL_MAP_CHECK=DEFERRED_TO_GHA
ACTUAL_MAP_ARTIFACT=NOT_YET_ACCEPTED
GRADE2_DECISION=NOT_RUN
verified=false
```

The v490 repair is exactly the finite source-side coverage-receipt key
repair that was requested.  No release-critical finite blocker was found.
This authorizes only a future inert GHA build/check against fresh output; it
does not accept an actual map artifact or promote any grade-two claim.

## Exact audited inputs

All listed files are LF-only (`CR=0`) and have a final LF.

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `sol/sol_task_744_audit_r07_grade2_maps_checker_v4.txt` | `1535` | `32` | yes | `cd4e2b997129ef0e6319963366ef7713af813c2a6d640e2be54c5b9a50ed1c41` |
| `sol/proof_r07_grade2_maps_coverage_receipt_schema_v490.md` | `1412` | `38` | yes | `e322c8e5546fc51e2d65e1fc85fa988bd92ce4475b3992aaf505fdfc668f48e4` |
| `search/d972_r07_grade2_forward_adjoint_maps_v3.py` | `46179` | `989` | yes | `7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84` |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v3.py` | `49727` | `1013` | yes | `d334b3cea69a2505a5c57794cedb9f40701881bf2801757606491dcd5d6feec6` |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v4.py` | `49643` | `1013` | yes | `7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29` |
| `sol/luna_reply_741_r07_grade2_maps_checker_receipt_v4.md` | `2792` | `76` | yes | `cd73e4db862f5fbbc7972232ade9f560d607f203ee0862ff13ee4e072937b3f1` |
| `sol/sol_reply_736_audit_r07_grade2_maps_v3.md` | `6467` | `146` | yes | `de9f285340e12fc2b40046c928d94fe9b6dea914de38f5f141aeffc2452ec603` |

The reply's own post-seal digest is necessarily supplied externally.

## 1. Mechanical v3-to-v4 boundary - PASS

Raw `fc /n` comparison has four hunks only: the checker PASS marker, the
four result-key literals in `verify_coverage`, their four validation lookup
literals, and the four corresponding literals in the selftest expected
dictionary.

A token comparison found equal token counts (`11943` each), an identical
token-type sequence, and exactly 13 changed token values:

```text
1 x R07_GRADE2_FORWARD_ADJOINT_MAPS_V3_CHECKER_PASS
 -> R07_GRADE2_FORWARD_ADJOINT_MAPS_V4_CHECKER_PASS

3 x source_tags        -> tags
3 x source_components  -> components
3 x source_monomials   -> monomials
3 x source_psl_indices -> psl_indices
```

For each source key, two occurrences are in `verify_coverage` (result
construction and validation lookup) and one is in the selftest expected
dictionary.  An in-memory normalization applying exactly those replacements
to v3 was byte-for-byte equal to v4.  Its replacement counts were
`1 + 4*2 + 4*1 = 13`.  Removing the twelve seven-byte `source_` prefixes
accounts exactly for the file-size change `49727 - 84 = 49643`; the marker
replacement is length preserving.  Thus there is no hidden whitespace or
non-token change.

The parsed top-level AST has 89 nodes in each file with the same ordered node
labels.  Exactly three nodes differ:

```text
Assign:PASS_MARKER
FunctionDef:verify_coverage
FunctionDef:selftest
```

The other 86 top-level nodes are AST-identical, with no added or removed
node.  In particular, all quotient/action arithmetic, coordinate encoding,
sparse reduction, actor/B enumeration, parsing, transpose, inverse,
manifest/roster/source validation, artifact comparison, safe output, and CLI
logic are unchanged.  Within the two changed functions the byte
normalization above shows that only the named string literals differ; no
value expression or control flow changed.

Both checker versions retain exactly:

```text
PRODUCER_PATH   = search/d972_r07_grade2_forward_adjoint_maps_v3.py
PRODUCER_SHA256 = 7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84
PRODUCER_MARKER = R07_GRADE2_FORWARD_ADJOINT_MAPS_V3_CANDIDATE
SCHEMA          = d972.r07.grade2.forward-adjoint-maps.v3
```

The actual producer bytes have precisely that SHA-256.  The checker still
hashes that path before resolving or opening an artifact, and never imports
or executes the producer.

## 2. Field-for-field live coverage comparison - PASS

The bounded comparison instantiated the producer `Context` and checker
`IndependentContext` separately, then used their respective enumeration and
sparse-reduction paths.  For both registered cases, producer and checker had
`raw_count=36288`, canonical row count `36288`, and identical canonical
records.  Their independently computed coverage dictionaries had equal key
sets and equal values field-for-field.

For nonphysical `T_fwd_a0_t0`:

```json
{"components":[0,1],"destination_components":[0,1],"destination_coordinates":36288,"destination_monomials":[0,1,2,3,4,5],"destination_psl_indices":504,"monomials":[0,1,2,3,4,5],"psl_indices":504,"source_coordinates":36288,"tags":[0,1,2,3,4,5]}
```

For physical `B_fwd_a0`:

```json
{"components":[0,1],"destination_blocks":[0,1],"destination_characters":[0],"destination_components":[0,1],"destination_coordinates":12096,"destination_monomials":[0,1,2,3,4,5],"destination_psl_indices":504,"monomials":[0,1,2,3,4,5],"psl_indices":504,"source_coordinates":36288,"tags":[0,1,2,3,4,5]}
```

These are `producer == checker` outputs, not values copied from one
implementation to the other.  The nonphysical destination decode remains
`component/monomial/psl = tuple[1]/[2]/[3]`; the physical decode remains
`tuple[2]/[3]/[4]`, with character and block at `tuple[0]/[1]`.  The token
audit also shows zero changes to any `destination_*` key or value expression.

## 3. Bounded compile/selftest and live mutation - PASS

The bytecode cache was external to the repository:

```powershell
$env:PYTHONPYCACHEPREFIX = Join-Path $env:TEMP 'task744-pycache'
python -m py_compile search/check_d972_r07_grade2_forward_adjoint_maps_v4.py
python -B search/check_d972_r07_grade2_forward_adjoint_maps_v4.py --selftest
```

Results:

```text
py_compile: exit 0, wall 0.299424 s
selftest:   exit 0, wall 1.208527 s, internal 0.9972827000310645 s
fixture=PASS
fixture_rejection_count=13
producer_sha256=7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84
both_inverse_pairs=true
nontrivial_prefix=true
verified=false
```

The live selftest path at checker-v4 lines 787--803 still constructs all four
actual character-zero actor maps via
`actor_records -> reduce_sparse`, sends the 36,288-row actor-zero map to the
production `verify_coverage`, and compares the complete returned dictionary.
This is not a tiny substitute.

The mutation at lines 955--966 also remains on that same actual map.  An
additional bounded probe reproduced it exactly: all 36,288 source
coordinates were preserved, destination monomials changed from
`[0,1,2,3,4,5]` to `[0,1,2,3,4]`, and the live helper rejected with
`RuntimeError: coverage_cases`.  The normal selftest's total of 13
rejections confirms that this branch remains integrated with the other
parser/type/pin/output fixtures.

## 4. Resource and slow-path inspection - PASS

Because the complete token-type sequence is unchanged and all differences
are string literals, v4 cannot introduce a new import, call, loop,
comprehension, allocation, retry, concurrency primitive, or scan.  Direct
inspection agrees:

- map storage remains sparse dictionaries/lists of triples;
- `sparse_apply` and the selftest probes allocate only one-dimensional
  `O(width)` vectors, not a dense map matrix;
- there is no thread, process, executor, async, retry, or polling path;
- the exact-roster `directory.iterdir()` one-level scan and the bounded
  output-parent ancestor walk are pre-existing and unchanged;
- no unrelated build-scale or repeated-scan path was added.

No enhancement is requested.

## Commands and limitations

The read-only/mechanical commands were:

```text
cmd /d /c fc.exe /n search\check_d972_r07_grade2_forward_adjoint_maps_v3.py search\check_d972_r07_grade2_forward_adjoint_maps_v4.py
python -B -    # stdin ast.parse/tokenize comparison and exact in-memory normalization
python -B -    # stdin independent producer/checker T and B enumeration/coverage comparison
python -B -    # stdin live malformed-monomial mutation probe
Get-FileHash -Algorithm SHA256 plus byte-level LF/CR/final-byte counting
```

The comparison scripts wrote no files.  No producer `--emit`, checker
`--check`, real 40-table build, actual artifact opening, GHA, workflow, git,
Lean, grade-two decision, A0, COMMON, compatible-lift, fake, or Ihara
operation was run.  The dynamic universe was deliberately bounded to the
same character-zero `T_fwd_a0_t0` and `B_fwd_a0` cases used in the structural
receipt, plus the specified malformed T mutation.  Actual artifact and
build-scale resource behavior therefore remain for GHA.  Accordingly this
finite audit is cross-check evidence only and `verified=false`.

```json
{"SAFE_TO_DISPATCH_GHA":"yes","verdict":"PASS_GRADE2_MAPS_CHECKER_V4_SAFE_FOR_GHA","verified":false}
```
