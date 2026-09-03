# Sol(max) Task731 — repaired grade-two maps v2 independent release audit

## Verdict

`PASS_GRADE2_MAPS_V2_SAFE_FOR_GHA`

`SAFE_TO_DISPATCH_GHA=yes`

All four Task719 blockers are closed on the actual production paths. The preserved forward/adjoint mathematics, serialization, checker independence, and sparse resource design remain sound. I found no release-critical finite defect.

This verdict authorizes only the inert map-pair GHA build/check. It is not a grade-two decision and implies no A0, COMMON, compatible cofinal lift, fake, Ihara, or Lean verification claim. `verified=false`.

## Audited executable receipts

The parent receipts reproduce exactly:

| executable | bytes | LF | final LF | SHA-256 |
|---|---:|---:|---|---|
| `search/d972_r07_grade2_forward_adjoint_maps_v2.py` | 44,667 | 959 | yes | `fdcb9a8ca9804179f350500c02203cdde550498b5cc5912ff1b0bde1d92e4d84` |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v2.py` | 48,459 | 988 | yes | `e388300c88de674d6e4550a7f20a40031488e724e40e73cdc89189b472ae61f0` |

Relevant paper receipts checked for direction and boundary:

| paper | bytes | LF | final LF | SHA-256 |
|---|---:|---:|---|---|
| v474 | 12,755 | 321 | yes | `a0ae668799de33d79b5e80ca2a6b7b50224770528b1201d8fb999506757c08c9` |
| v483 | 8,383 | 226 | yes | `60b745781b5a10ada68445b852ca8c79958a8ac2ae2fb7a5b922275afbcc7393` |
| v486 | 3,465 | 88 | yes | `fcb34e306e2d568f55985b56fb049cd56d269e93a906b2b5362bdcc6658ddcb7` |

## Task719 blocker re-audit

### F719-1 — CLOSED

Checker constants bind the exact repository path
`search/d972_r07_grade2_forward_adjoint_maps_v2.py` and literal digest
`fdcb9a8c...e4d84`. `check_artifact` calls `validate_producer_source` before resolving or reading the artifact, and the manifest gate separately requires `manifest.producer_sha256` to equal that authenticated digest. The checker neither imports nor executes the producer.

The live checker selftest passes the exact producer, then rejects both a changed-byte copy and the real path paired with a wrong literal. Thus a coordinated producer-metadata/digest mutation cannot move the checker-local source identity.

### F719-2 — CLOSED

Both selftests construct one complete character's four maps through the production record generators:

- producer: `iter_actor_raw` → `canonical_entries`;
- checker: independently implemented `actor_records` → `reduce_sparse`.

They test `x` against `x^-1` and `y` against `y^-1` over all 36,288 source coordinates with the same inverse validators used by actual mode, and additionally apply both compositions to a full-width vector.

Each context selects an actually nonidentity g760 shift, sends a basis coordinate from that tag through the production six-occurrence aggregation generator and sparse application, and constructs all 36,288 B records. The producer writes/parses this B table through `write_table/parse_table`; the checker independently serializes and parses it through `parse_exact`. Only after these branches succeed are `both_inverse_pairs` and `nontrivial_prefix` reported true.

The older generic 12-coordinate coefficient/cancellation/transpose fixtures remain canaries and are no longer the sole evidence for actor/prefix coverage.

### F719-3 — CLOSED

`strict_fixed` distinguishes bool before int and recursively validates exact list/dict shape and every fixed integer leaf. Production `check_artifact` applies it to dimensions, coordinate orders, occurrence triples, source/marking/word receipts, g760 prefix receipt, and the complete structural receipt. Top-level counts retain explicit `is_int` checks.

`parse_exact` requires the exact forward/adjoint T/B receipt key sets before values. It explicitly rejects bool for widths, counts, byte lengths, character, and T actor, while every JSONL coordinate/coefficient and EOF count/length also uses `is_int`.

Live mutations reject actor `1→true`, character `0→false`, an occurrence coordinate, a dimension count, and actor-order coordinate. They enter the same production validators used by actual check mode.

### F719-4 — CLOSED

The production result writer calls `safe_output_path`. It resolves artifact/output paths, requires the target not to exist, rejects an artifact descendant and any repository descendant, walks existing ancestors rejecting symlinks and Windows junctions, creates only the validated external parent, and then uses a same-directory temporary file, flush/fsync, atomic replace, and byte readback.

Live fixtures reject an existing file, an artifact descendant, and a repository descendant, and confirm the existing file's bytes remain unchanged. Inspection confirms a symlink/junction ancestor reaches the same production rejection branch; no separate alternate writer bypasses it.

## Preserved mathematical and executable core

### Coordinates and roster

The exact dimensions are

```text
V_a = 6 tags × 2 components × 6 monomials × 504 = 36,288,
P   = 4 characters × 2 blocks × 2 components × 6 monomials × 504 = 48,384.
```

The orders are fixed as required: four characters, actors `(1,-1,2,-2)`, monomials `(u1²,u1u2,u1u3,u2²,u2u3,u3²)`, then PSL index. `map_specs` emits 16 actor forwards and four B forwards, each followed by its mechanically derived transpose: 20 forward maps and 20 adjoints, exactly 40 JSONL tables.

### Sparse semantics and word direction

Both implementations interpret `(source,destination,c)` as

```text
forward[destination] += c * input[source],
adjoint[source]       += c * dual[destination].
```

Raw duplicates are accumulated by `(source,destination)`, reduced modulo three, zeros removed, and survivors sorted canonically. Source/destination ranges and coefficients `{1,2}` are checked. Adjoint tables are obtained by mechanically swapping the first two coordinates, and actual mode compares every adjoint entry with that transpose.

Actor maps agree with v474's pure associated-grade convention: primitive forward maps act on source rows; dual right extension applies the matching transpose `T_adj(a,t)`. The stored word tuple is not reversed or relabelled. Both inverse pairs are checked for every character and every source coordinate.

### Occurrences and prefixes

All six coupled monomials remain in one source slice. The B generator iterates the exact six triples

```text
(0,0,1),(1,0,2),(2,0,1),(3,1,2),(4,1,2),(5,1,1)
```

before producing physical coordinates, retaining both components. Its six shifts are derived from the pinned g760 tag images in the exact order

```text
identity,
tags(g760)[2], tags(g760)[2],
tags(g760)[5] * tags(g760)[4]^-1,
tags(g760)[5], tags(g760)[5].
```

The producer and checker own separate quotient/context implementations and agree on the registered marked-quotient multiplication convention.

### Canonical artifact and independence

Every table uses canonical LF-terminated JSON triples plus one canonical EOF object. Parsers enforce strict increasing pair order, no duplicate/uncombined entry, exact count/body bytes/body SHA/full bytes/full SHA, EOF, and no trailing byte. Manifest and filesystem rosters are exact.

The checker imports/calls neither producer, Task565, nor shared executable arithmetic. It locally rebuilds the marked quotient, PSL enumeration, transport, prefixes, actor/B tables, transposes, inverse identities, and structural coverage before producing its unique PASS marker. CLI mode groups are exclusive; checker selftest refuses output, while actual check optionally writes only through the safe writer.

V486 concerns the later filtered P1-DAG lift packet clause and does not widen this map artifact's claim. These maps supply only the v474 structural forward/adjoint interface.

## Resource audit

No dense `36,288²` or `48,384×36,288` matrix is constructed. Each map has one sparse record per source coordinate before canonical reduction. Producer context is constructed once, emits one table pair at a time, and retains only the 20 forward sparse tables needed for final inverse/coverage receipts. The checker reconstructs and retains the 40 parsed sparse tables for final cross-table identities.

There is one avoidable but nonblocking linear duplication: checker actual mode reconstructs the same expected forward arithmetic again when parsing the corresponding adjoint and retains forward plus transpose records until final structural checks. This is roughly 40×36,288 sparse records, not a quadratic matrix, and the bounded full-character tests complete in under one second of internal elapsed time. It does not make the GHA build vacuous and is not a release blocker. A later performance-only revision may cache 20 expected forwards or stream final identities, but Task731 does not require it.

No repeated context construction, dense map, or quadratic duplicate-combination loop was found.

## Bounded commands and results

Bytecode cache was redirected outside the repository. Executed only:

```text
$env:PYTHONPYCACHEPREFIX=Join-Path $env:TEMP 'task731-pycache'
python -m py_compile search/d972_r07_grade2_forward_adjoint_maps_v2.py search/check_d972_r07_grade2_forward_adjoint_maps_v2.py
python search/d972_r07_grade2_forward_adjoint_maps_v2.py --selftest
python search/check_d972_r07_grade2_forward_adjoint_maps_v2.py --selftest
```

Results:

```text
py_compile: PASS                         wall 0.316 s
producer selftest: PASS                 wall 1.098 s
  internal elapsed 0.836 s
  fixture_rejection_count 2
checker selftest: PASS                  wall 0.974 s
  internal elapsed 0.834 s
  fixture_rejection_count 12
```

Producer rejections are truncation and trailing-data mutations. Checker rejections comprise those two, two table-descriptor bool aliases, three fixed-manifest bool aliases, two producer-source pin mutations, and three safe-output mutations.

No actual `--emit`, actual `--check`, real artifact, GHA, or git operation was performed.

## Claim boundary

```text
GRADE-TWO FORWARD/ADJOINT MAP PAIR V2: SAFE FOR INERT GHA BUILD/CHECK
ACTUAL MAP ARTIFACT:                   NOT BUILT IN THIS AUDIT
GRADE-TWO MEMBER/NONMEMBER:            NOT RUN
A0 / COMMON / COMPATIBLE COFINAL LIFT: NOT DECLARED
FAKE / IHARA:                          NOT DECLARED
verified:                              false
```

The sealed reply's byte/LF/final-LF/SHA-256 receipt is supplied externally because embedding its own digest would change its preimage.

```json
{"SAFE_TO_DISPATCH_GHA":"yes","verdict":"PASS_GRADE2_MAPS_V2_SAFE_FOR_GHA","verified":false}
```
