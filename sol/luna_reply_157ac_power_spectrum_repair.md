# Task 157ac — power-spectrum v2 repair report

## Result

The v2 bundle repairs F1–F4 from the 157x audit without overwriting v1.
Static dispatch readiness: **YES, pending the mandated GHA full producer/checker
run**.  No local GAP, git, push, or GHA was run here.

## Changed files

* `search/d972_power_spectrum_v2.g` — new versioned GAP producer.
* `search/check_d972_power_spectrum_v2.py` — new independent checker.
* `search/d972_dovetail_core_v2.g` — new definition-only reusable D972 core.
* `.github/workflows/d972-power-spectrum-v2.yml` — new versioned workflow.
* `sol/luna_reply_157ac_power_spectrum_repair.md` — this report.

The v1 producer, checker, and workflow remain untouched.

## 157ai runtime/descent repair

The v2 producer no longer Reads `search/d972_dovetail_worker_v1.g`, whose
top-level dispatcher ends in `QUIT`.  It Reads the new
`search/d972_dovetail_core_v2.g:8-12`; the core contains definitions only and
has no `GetEnv`, task-path Read, dispatcher, or `QUIT`.  Its only transitive
Reads are the four fixed helper files listed in the receipt manifest.  The v2
workflow now triggers and hashes the core plus all four helpers
(`.github/workflows/d972-power-spectrum-v2.yml:7-17,38-49`).  The old worker is
not part of the v2 runtime or manifest, and its dynamic `Read(taskPath)` paths
are therefore unreachable by construction.

The checker now independently enumerates the degree-27 G9 Cayley graph (2,916
vertices) and degree-9 PSL factor Cayley graph (504 vertices) once, then for
each of the 972 rows checks generator-image membership and every directed edge
for consistency (`search/check_d972_power_spectrum_v2.py:147-299,475-480`).
This is O(972*(2916+504)*4) edge checks and does not enumerate 972^3 triples.
Before row-action descent, it also uses the canonical G9 section words to form
all 11,664 directed-edge Schreier relators, verifies their G9 projection is
identity, evaluates their PSL projections, and checks that those kernel values
generate order 504 (`search/check_d972_power_spectrum_v2.py:220-243`).
Surjective projections to both enumerated factors plus this full kernel prove
the compact roof is the direct product G9 x PSL; individual factor membership
therefore implies compact C membership.
The subsequent 972^2 generator-action composition check is retained, so its
associativity conclusion is now conditional only on the independently replayed
factor descent, not on GAP `GroupHomomorphismByImages` or `settled` metadata.

The workflow has `workflow_dispatch` in addition to the push trigger
(`.github/workflows/d972-power-spectrum-v2.yml:3-18`).  Runtime immutability is
bounded explicitly: `ubuntu-24.04`, apt package `gap=4.12.1-2build2`, and GAP
`4.12.1` are enforced (`:22-30,51-55`), while the Ubuntu archive and runner
label remain external mutable infrastructure; no stronger full-image
immutability claim is made.

## Follow-up 1-based/0-based repair

The initial v2 producer had one mixed-index order-loop defect: GAP's
`PositionProperty` returns the 1-based row position, while serialized product
entries are 0-based.  The order walk now initializes
`power := identity-1` before using `products[power+1][i]`
(`search/d972_power_spectrum_v2.g:131-145`).  The inverse lookup remains
correct: `Position(products[i], identity-1)` is a GAP 1-based column/row
position and is serialized as `inv-1`; `squareMap`/`cubeMap` similarly convert
the zero-based square output back to a GAP row with `+1`
(`:149-151`).  A complete occurrence audit found no other mixed-index use.
The independent checker now documents the zero-based receipt convention and
adds a C2 zero-based identity/order regression selftest
(`search/check_d972_power_spectrum_v2.py:351-356,399-418`).

## Closure of prior findings

F1 is closed by the v2 workflow paths at
`.github/workflows/d972-power-spectrum-v2.yml:7-17`, which include the producer,
checker, definition-only core, both previously omitted direct reads
`search/probe/wac_v1/gap_output_prelude.g` and `search/gaplib_common.g`, both
other fixed helpers, and the frozen artifact.  The producer emits the complete
five-file runtime manifest (`search/d972_power_spectrum_v2.g:17-18,188`); the
checker requires exact manifest equality and recomputes every file hash
(`search/check_d972_power_spectrum_v2.py:24-30,301-307`).  The workflow also
hash-checks the same files before GAP starts (`.github/workflows/d972-power-spectrum-v2.yml:38-49`).

F2 is closed as far as the Ubuntu workflow contract permits: the job is pinned
to `ubuntu-24.04`, the GAP package is pinned to `4.12.1-2build2`, and runtime
version `4.12.1` is enforced (`.github/workflows/d972-power-spectrum-v2.yml:22-30,51-55`).
Checkout and artifact upload use immutable commit SHAs, not mutable tags
(`:33-36,88-95`).  The v2 producer/checker source hashes are also checked before
execution (`:25-26,42-43`).

F3 is closed.  The producer computes zero-based table-indexed `square_map`,
`cube_map`, and the folded exact-order exponent
(`search/d972_power_spectrum_v2.g:149-155,195-199`).  The independent checker
derives the same maps and exponent from its independently replayed table and
rejects any mismatch (`search/check_d972_power_spectrum_v2.py:379-388`).

F4 is closed by an independent direct-product certificate and factor descent followed by a structure-derived,
exhaustive pair check rather than trust in receipt metadata.  The factor check
enumerates each finite factor once, proves the Schreier kernel order 504, and
verifies all directed Cayley edges for all 972 assignments
(`search/check_d972_power_spectrum_v2.py:162-299,475-480`).
For every 972^2 pair, the checker then verifies
`h_(i*j) = h_j o h_i` on both compact roof generators, including the lambda
arithmetic relation (`search/check_d972_power_spectrum_v2.py:389-417,543-546`).
This is the associativity proof for the lambda/f composition law; the receipt's
`associativity_method` and pair count are checked only after this independent
calculation.  The producer records the corresponding expected pair count
(`search/d972_power_spectrum_v2.g:192-193`).

The fail-closed outside lane is preserved verbatim in meaning: v2 emits
`UNKNOWN_MISSING_AUTHENTICATED_LABEL`, null outside rows/histogram, and
`outside_inference_forbidden=true` (`search/d972_power_spectrum_v2.g:201-202`);
the checker rejects any consumable authenticated outside label
(`search/check_d972_power_spectrum_v2.py:207-221,293-298`).

## Static checks run

All checks below were lightweight and used no GAP:

```text
python -B -m py_compile search/check_d972_power_spectrum_v2.py
python -B search/check_d972_power_spectrum_v2.py --self-test
python -B -c "ast.parse(...)"
python -B -c "yaml.safe_load(...)"
```

Results:

```text
D972_POWER_SPECTRUM_V2_CHECKER_SELFTEST_PASS
PY_AST_PASS
YAML_PARSE_PASS
PY_FACTOR_SCHREIER_PASS 2916 504
V2_TRANSITIVE_SOURCE_DISPATCH_PASS 5
V2_WORKFLOW_SOURCE_HASH_BIND_PASS
```

The path-coverage check independently confirmed that the definition-only core
and all four fixed transitive `Read` dependencies are workflow-triggered.  The full 972-row producer,
945,441-product replay, and exhaustive associativity loop remain intentionally
for GHA.

## Final SHA-256 hashes

Bundle files:

* `search/d972_power_spectrum_v2.g` —
  `1855cf69b78cda06f5a829f4a4d500f4f8e89431e88110271e2567d78e6ba651`
* `search/check_d972_power_spectrum_v2.py` —
  `c5a837d5c194ecb42163d8944c59aaa919705bd488129068aa5324830ae00213`
* `search/d972_dovetail_core_v2.g` —
  `1c3348003805df874ab6d42503720259564eec25c1aebfb1c548a759e3d9f7ae`
* `.github/workflows/d972-power-spectrum-v2.yml` —
  `2fee55211194660452d33b1e87b8ef02d1a0e95fb6070c357b7083201717675a`

Bound runtime inputs:

* `search/d972_dovetail_core_v2.g` —
  `1c3348003805df874ab6d42503720259564eec25c1aebfb1c548a759e3d9f7ae`
* `search/probe/wac_v1/gap_output_prelude.g` —
  `2e4da671ad9d018be1bc6f2f387f0e1d597e87c2c0e807eef40aeef3b92deece`
* `search/gaplib_common.g` —
  `f80eeeae71c4e39f8b3d62d997d18635f5ea8fb339a6d0578e834300ea4d4911`
* `search/week3-battery-common.g` —
  `aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998`
* `search/week3-psl-common.g` —
  `e48e50d55562983415b5691d07e3d893182620b1f73b8fe35ea77815ad9695c4`
* `search/certs/d972_b4_word_key_artifact_v1_20260816.json` —
  `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9`
