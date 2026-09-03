# Sol(max) Task736 - independent finite audit of grade-two maps v3

## Verdict

`PASS_GRADE2_MAPS_V3_SAFE_FOR_GHA`

`SAFE_TO_DISPATCH_GHA=yes`

The finite nonphysical destination-coverage repair is correct on the live
production helper in both independent programs. No release-critical finite
blocker was found. This authorizes only a future inert GHA build/check; it is
not an accepted map artifact or a grade-two decision. `verified=false`.

## Authenticated receipts

| file | bytes | LF | final LF | SHA-256 |
|---|---:|---:|---|---|
| `search/d972_r07_grade2_forward_adjoint_maps_v3.py` | 46,179 | 989 | yes | `7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84` |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v3.py` | 49,727 | 1,013 | yes | `d334b3cea69a2505a5c57794cedb9f40701881bf2801757606491dcd5d6feec6` |
| v2 producer baseline | 44,667 | 959 | yes | `fdcb9a8ca9804179f350500c02203cdde550498b5cc5912ff1b0bde1d92e4d84` |
| v2 checker baseline | 48,459 | 988 | yes | `e388300c88de674d6e4550a7f20a40031488e724e40e73cdc89189b472ae61f0` |
| `sol/sol_reply_736_audit_r07_grade2_maps_v3.md` | 6,467 | 146 | yes | supplied externally after sealing |

Both v3 files are LF-only and final-LF terminated. Checker v3 binds and
authenticates the exact path
`search/d972_r07_grade2_forward_adjoint_maps_v3.py` and the producer digest
`7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84` before
artifact validation. The sealed reply's own post-seal digest is supplied
externally because embedding a self-digest changes its preimage.

## Failed-run fact and finite repair

The authenticated failed run was `33811487764/1`, job `100834098415`, head
`b805d4089d76ca98b3bbbc63594ce053ec90e5fa`. It authenticated its inputs and
passed both bounded selftests, emitted all 20 forward/adjoint pairs in about
ten seconds, then failed only at
`structural_identities -> verify_coverage(T_fwd_a0_t0, physical=False)` with
`RuntimeError: coordinate_case_coverage`. No sparse map, actor action,
aggregation, transpose, inverse, or coordinate encoding failure was observed.

The exact v2 -> v3 source diff is 36 insertions and 6 deletions in 5 hunks;
the checker diff is 34 insertions and 9 deletions in 5 hunks. AST comparison
finds only `verify_coverage` and `selftest` changed in each file; 47 other
top-level functions in each implementation are AST-identical. Top-level
changes outside those functions are only the v3 schema/marker in the producer
and the v3 schema, checker marker, producer marker, producer path, and
producer SHA pin in the checker.

The repaired destination decoding is exactly:

```text
nonphysical (tag, component, monomial, psl):
  component = tuple[1], monomial = tuple[2], psl = tuple[3]
physical (character, block, component, monomial, psl):
  component = tuple[2], monomial = tuple[3], psl = tuple[4]
```

Source decoding remains tuple indices `0/1/2/3`. Source tags `0..5`, both
components, all six monomials, all 504 PSL indices, and the physical
character/block checks remain required. All v2 map arithmetic, source pins,
canonical serialization, transpose, inverse, aggregation, and coordinate
logic are unchanged.

## Live coverage regression

Both selftests construct the actual character-zero actor map through their
own production path (`iter_actor_raw -> canonical_entries` in the producer;
`actor_records -> reduce_sparse` in the checker), containing all 36,288
records, and pass it to that program's own `verify_coverage` helper. The exact
asserted receipt is:

```text
source coordinates:       36288
source tags:              0..5
source components:        0..1
source monomials:         0..5
source PSL count:         504
destination coordinates:  36288
destination tags:         0..5 (nonphysical tuple decode)
destination components:  0..1
destination monomials:    0..5
destination PSL count:    504
```

Each selftest also retains the actual inverse-pair, full-width vector,
nonidentity prefix/B, parser, transpose, coefficient-2, and existing safe
output/source-pin/bool fixtures. A live malformed mutation maps every
destination with monomial 5 to monomial 0 while retaining source coverage;
the same production coverage helper rejects it. This contributes the third
producer rejection and thirteenth checker rejection.

## Task731 invariant audit

The checker remains nonimporting and independently owns quotient/context,
prefix, actor/B record generation, sparse reduction, parsing, transpose, and
identity arithmetic. Its source digest gate is reached before artifact
resolution; manifest/source-pin and exact parser gates remain in place. No
shared helper or producer execution was introduced.

The prior strict integer/bool and fixed-shape gates, canonical JSONL/EOF
receipts, exact table rosters, safe external output path and atomic writer,
inverse/transpose checks, and claim boundary remain unchanged. Resource shape
also remains the accepted sparse design: no dense map matrix or quadratic
duplicate-combination structure was added. All terminal flags remain false;
no actual map artifact or downstream grade/A0 result is claimed.

## Bounded commands and results

Only the following bounded commands were run. Bytecode cache was outside the
repository at `%TEMP%\task736-pycache`:

```text
$env:PYTHONPYCACHEPREFIX = Join-Path $env:TEMP 'task736-pycache'
python -m py_compile search/d972_r07_grade2_forward_adjoint_maps_v3.py search/check_d972_r07_grade2_forward_adjoint_maps_v3.py
python -B search/d972_r07_grade2_forward_adjoint_maps_v3.py --selftest
python -B search/check_d972_r07_grade2_forward_adjoint_maps_v3.py --selftest
```

Results:

```text
py_compile: PASS          exit 0, wall 0.318 s
producer selftest: PASS  exit 0, wall 1.171 s, internal 0.9463108999771066 s, fixture_rejection_count 3
checker selftest: PASS   exit 0, wall 1.162 s, internal 0.9494525999762118 s, fixture_rejection_count 13
```

The producer result retained `both_inverse_pairs=true`,
`nontrivial_prefix=true`, and all claim flags false. The checker result
retained its exact producer SHA and all claim flags false. No real `--emit`,
`--check`, 40-table build, workflow, GHA, git, Lean, grade-two, A0, COMMON,
fake, or Ihara operation was run.

```text
ACTUAL_MAP_BUILD=DEFERRED_TO_GHA
GRADE2_DECISION=NOT_RUN
A0=false
COMMON=false
COMPATIBLE_LIFT=false
FAKE=false
IHARA=false
verified=false
```

```json
{"SAFE_TO_DISPATCH_GHA":"yes","verdict":"PASS_GRADE2_MAPS_V3_SAFE_FOR_GHA","verified":false}
```
