# Sol(max) Task655: terminal bounded release audit of Task640 v3

## Verdict

`PASS`

`SAFE_TO_DISPATCH_GHA=yes`

All charged checks passed.  This authorizes only a fresh-rho2 Task640 GHA
run.  No production run, GHA dispatch, implementation edit, or git operation
was performed.

`verified=false`

## Frozen inputs

No `INPUT_MISMATCH` occurred.  Direct byte/LF/SHA-256 recomputation gave:

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,474 | 304 | `060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 92,071 | 1,563 | `889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `4d76e057838af7d7c1d6ad28203bdfeec545be36aaf94a815b22bfad58a15f39` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,972 | 58 | `a187b207f4cbf97c0b20fe28c8edd33a39f60cbdf34909a5cfba56000dd4287b` |
| `sol/luna_reply_654_r07_task640_inverse_choice_fixture_closure.md` | 1,620 | 26 | `106a1c3f2dad3d9e41df997d206de690e79099517ad6ae5dcd75fb5fdafebe19` |

## Charged live gates

- Checker lines 384--386 define `signed_base_factor`; selftest lines 443--445
  call it with the non-self-inverse S3 cycle `bytes((1,2,0))` and the
  independently literal inverse `bytes((2,0,1))`.  Production line 1360 calls
  that same helper with `self.old.inv_word`.  Replacing only its negative
  branch by `base` made selftest fail exactly with
  `signed_base_inverse_choice`; invalid sign remains rejected.
- The Task652 gates remain live.  Removing only the ancestry digest comparison
  made selftest fail with `fixture_ancestry_binding_mutation`.  Replacing
  `reversed(indices)` by `indices`, and separately reversing the multiplication
  side in the shared prefix helper, each failed with
  `checker base prefix identity`.  Disabling only the unpack/roundtrip
  comparison failed with `fixture_mutation_accepted`.

Thus the negative inverse choice, ancestry binding, suffix traversal,
noncommutative multiplication order, and packing roundtrip are each charged
by a failing one-site mutation of the live helper used by production.

## Bounded regression

- **F646-A/B:** producer line 276 emits the fixed typed parent; checker lines
  476--477 require the same complete dictionary without coercion.  The seven
  canonical receipt names are fixed at checker line 19, checked before reads
  at lines 479--486, and compared against all independently rebuilt bytes by
  `exact_receipt_gate` at line 547.
- **R1/R3/R4:** workflow lines 113--118 retain the exact Task595 v2 candidate.
  Producer lines 221--240 and checker lines 491--521 derive reached seeds from
  raw prior-plus-leaf terms before cancellation, exercise the typed all-seven
  endpoint/direct route, and only then group.  Checker lines 502--534 rebuild
  signatures and buckets and independently replay the bucket terms through
  the dense/packing gate.
- **R5:** the checker has no producer import and the bounded forbidden scan
  found no `exec`, `.load`, `ModuleType`, `importlib`, or producer-module
  reference.  Its local all-seven `direct_column` terminates in the shared
  direct/occurrence equality gate at line 1499.
- **R7:** parent payloads are stream-hashed in 1 MiB chunks (producer line 168,
  checker line 314); no ancestry DOM was introduced.  Time/RSS, record,
  path-length, path-count, trie-count, state-count, and durable-output caps
  remain attached to live counters.  Exact false/null claim gates remain at
  checker lines 363--364 and 537--547.
- Workflow producer/checker/reply pins equal the frozen hashes.  Its seven
  `uses:` entries are the exact expected actions, each pinned to a full
  40-hex commit; line 40 retains the inert `false &&` guard.

## Serial checks

- External-cache `python -B -m py_compile` on producer and checker: `PASS`.
- Producer `--selftest`: exit 0, `leaf_live_mutations=4`.
- Checker `--selftest`: exit 0, `mutation_count=43`.
- PyYAML `safe_load`: `PASS` (`jobs=1`).
- Frozen-input, forbidden-import/exec, exact-action, workflow-hash, and inert
  guard scans: `PASS`.
- The five tiny in-memory source mutations listed above all failed at their
  intended live gates.

## Claim boundary

This PASS proves no rho2 value, grade-two MEMBER/NONMEMBER result, A0,
compatible cofinal lift, FAKE, IHARA, cross-check, or Lean verification.
