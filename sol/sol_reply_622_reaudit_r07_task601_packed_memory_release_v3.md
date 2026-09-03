# Sol(max) Task622 final re-audit reply

## Verdict

**PASS**

The exact Task622 quartet satisfies all six final gates.  Task621 implements
exactly the four finite repairs required by Task620; I found no mathematical,
authentication, transcript-completeness, resource-lifetime, or claim-status
weakening.  No further repair is required before the single Task618-authorized
GHA rerun.

This is a static release verdict only.  I did not run the full 8,059-offer
route, production, GHA, or git.  It does not promote an SLP, residual, A0,
COMMON, fake, Ihara, `cross_checked`, or `verified` claim.

## Exact input binding

I read the four requested predecessor records and the Task622 instruction in
full, and audited the complete exact quartet.

| input | bytes | SHA-256 |
|---|---:|---|
| `sol/sol_reply_618_audit_r07_task601_memory_terminal_v1.md` | 12,980 | `e97c2cfc3e7c02ec385245f670335088fe42f128ae3b2ba0c96dd4b46bbdcc88` |
| `sol/luna_task_619_r07_task601_packed_memory_repair_v2.md` | 8,545 | `3ef92d4e519b82d1137b1331ac841cc6343c2e9c824cc7ca99f0374e98f48026` |
| `sol/sol_reply_620_audit_r07_task601_packed_memory_release_v2.md` | 15,314 | `3741a8027cf73e04ea865a20dcb070b7d2f92d1b419aaedbdd15df998969552d` |
| `sol/luna_task_621_r07_task601_static_release_repairs_v3.md` | 2,693 | `15ec8346bf16bef67f7cfa719440379fa582375e3747afc71d0b35afa4b4c951` |
| `sol/sol_task_622_reaudit_r07_task601_packed_memory_release_v3.md` | 2,610 | `e288b6dc95e15c3f2da185b2d718ce32c871da84a1f143f0ddc3f0d2ff1f0500` |
| `search/d972_r07_a0_grade1_selected_slp_v1.py` | 47,935 | `cfd581f8a71176f9252555a94028a8482ede862ee3430098270109e52fa0d3ff` |
| `search/check_d972_r07_a0_grade1_selected_slp_v1.py` | 71,637 | `09ee815345e9ad2cfd80799a5bf7daf4446cda0eb3d8bc79bd7b3d9c61fa86c8` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml` | 5,497 | `7f1b59790d2092fd93035742510ce7232834b4f7ea0a470507a408100d2e39cd` |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | 7,634 | `a8511edcebff406af9a3b4fa0a0b2119d46f150741178379800cb1e88b7f16e2` |

## Final-gate findings

### F1. Producer `append_row`: PASS

At producer lines 203--209, `append_row` obtains a byte-cast `memoryview`,
checks the exact expected byte length, performs the canonical packed-byte
bound with one NumPy `frombuffer(...).max()` scan, and only then extends the
destination `bytearray`.  The scan is zero-copy and vectorized; it is not a
Python per-byte hot path.  The prior length and `byte <= 80` rejection
semantics are preserved.

### F2. Selected lower pre-replay and complete standalone reroute: PASS

Checker lines 522--533 replay lower recurrence only when
`declared_lower[pivot]` is true.  This is the authenticated least dependency
closure: lines 1637--1671 independently recompute the grade/lower closure and
require exact equality with both declared bitsets before physical replay.
Thus every earlier lower row needed by a selected row is present, while the
unneeded preliminary all-1,661 replay has been removed.

This optimization does not replace the independent terminal route.  Checker
lines 1321--1491 reconstruct all four old characters and all four blocks,
require `(logical, lower_offers, grade_offers, len(grade.rows)) ==
(8059, 2014, 6398, 5044)`, compare each online node/edge/row receipt, and call
`OnlineReceipts.finish()`.  The zero-lower branch consumes an
`old_lower_zero` row before attempting grade insertion, so accepted and
dependent grade offers are both covered.

### F3. Candidate-basis view reuse and terminal member test: PASS

Checker line 520 constructs the sole candidate-basis `RowView`; line 555
returns that object in `physical`.  The final independent comparison reuses
it at line 1493 rather than rescanning/reconstructing another `RowView`.
Lines 1494--1528 still require, without weakening:

- byte equality for every independently rebuilt basis row;
- the canonical basis SHA-256 and exact pivot leads;
- zero target remainder and byte equality with the sealed candidate
  remainder;
- exact equality with the body coefficient list (hence 3,317 terms);
- reconstruction of the target from those coefficients; and
- the packed/dense target and remainder hashes.

### F4. Negative selftests cross production boundaries: PASS

The new tests exercise the actual production predicates, not parallel test
logic:

- lines 1861--1874 leave a real `OnlineReceipts` instance unconsumed and
  require `finish()` to raise `authoritative_cursor_exhaustion`;
- lines 1912--1920 mutate the `states_exported` header byte to one and require
  production `validate_leaf_syntax()` to raise `leaf_header`;
- lines 1942--1961 add `states` to otherwise valid derived metadata and
  require production `validate_derived_metadata()` to raise
  `derived_compact_schema`.

The derived validator is itself used by `validate_ancestry` at line 377, so
the third test is on the live payload-validation boundary.

### F5. Task620 PASS invariants remain intact: PASS

Full-file inspection found the following prior findings unchanged:

- Producer transcript rows and edges retain one compact packed physical
  representation (`bytearray` streams); node/edge/row views do not reintroduce
  tuple-expanded edge stores or full-row Python lists.
- Dense lower companions are released after the old phase.  Block bodies and
  owners are created and released character by character; the checker likewise
  completes the sealed selected replay before releasing ancestry structures
  and beginning the standalone reroute.
- Ancestry remains parsed once and authenticated.  `derived.states` and an
  embedded `derived.literal_leaves` table are forbidden.  The exported leaf
  stream is canonical, sorted, carries the ancestry SHA in its header, and is
  compared byte-for-byte with the checker's independently recomputed adjoint
  leaf map.
- The selected source graph, defect expressions, ordered signed reductions,
  scale factors, literal dictionary, exact root coefficients, and closure
  bitsets remain checked.  No producer leaf helper is imported by the
  independent leaf recurrence.
- The later independent router still consumes every authoritative online
  cursor, including every all-zero old-lower offer; no lossy join or
  end-of-run digest-only substitute was introduced.
- Phase/RSS/peak/cursor diagnostics, the reserved emergency buffer, and
  `UNKNOWN_RESOURCE` handling remain present.  Manifest and roots false/null
  claim gates remain exact, including explicit roots filename/receipt binding.

The four Task621 edits are therefore local performance/testability repairs,
not a change to the routed vector space, recurrence signs/scales, ancestry
meaning, terminal decision, or epistemic status.

### F6. Workflow envelope and pins: PASS

Workflow lines 27--29 pin the exact producer, checker, and Luna reply hashes
listed above.  Its job gate contains exactly
`[fire-grade1-selected-slp-v2]`.  The pinned checkout/setup/download/upload
actions, serial producer-then-checker execution, success-only payload upload,
60-minute job timeout, 45-minute process bounds, `ulimit -v 8388608`, and
`TASK601_MAX_RSS=7516192768` remain intact.  The workflow file itself matches
the required `7f1b...e39cd` digest.

## Permitted lightweight checks

All were run serially; none invoked the real route.

| check | result |
|---|---|
| in-memory compile of producer | PASS |
| in-memory compile of checker | PASS |
| producer `--selftest` | PASS |
| checker `--selftest` | PASS |
| YAML parse and jobs-map check | PASS |

The checker selftest reported the required positive witnesses:
`zero_copy_cursor_exhaustion=PASS`,
`forbidden_state_mutation_count=2`,
`derived_states_absent=PASS`, compact-leaf checks PASS, coefficient-2 PASS,
and all eight false/null claim mutations rejected.

## Release boundary

There is no remaining finite static repair.  Root may commit/push this exact
release and launch the one Task618-authorized GHA rerun.  Promotion remains
conditional on that immutable run successfully producing and checking its
actual payload inside the stated time/RSS envelope; this PASS alone changes no
claim status.
