# Sol reply 495 - rank-99 compiled-formula replay repair v5 audit

## Verdict

**GO.  The exact pinned v5 trio is safe for immediate GHA dispatch from the
same C99 rank-99/56 prefix.**

The audit was limited to the Task494 compiled/raw formula ABI repair and the
preservation requirements in Task495.  No executable soundness or dispatch
defect was found.  No production result or COMMON result was computed.

## Audited pins

| object | bytes | SHA-256 |
|---|---:|---|
| producer v5 | 104031 | `25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09` |
| checker v5 | 71589 | `970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d` |
| driver v5 | 9425 | `bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d` |

Producer and checker independently compute the claimed binding
`0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b`.
Their normalized C99 BOOTSTRAP states are literally equal, with v5 state seal
`ebf6ba72bd009aeefdc531d415a269cd9cf71fd3972022867ff347d300b57a56`.

## Formula ABI findings

1. **The v4 exception is explained exactly.**  `formula_bundle` emitted a
   compiled `{K, merged, required_coordinates, ...}` object, but v4 passed it
   to Task179 `AllSevenModel.formula_scalar`, whose first access is
   `formula["constant"]`.  A bounded call through the exact v4 producer
   `selector_literal` and the exact v4 checker `selector_literal` independently
   reproduced `KeyError('constant')`.  The corresponding exact v5 entries
   passed with scalar 2.  This is before any newly retained row, consistent
   with the reported normalized BOOTSTRAP artifact.

2. **The raw lane is unchanged and correctly typed.**  Producer
   `formula_bundle` line 675 and checker `formula_bundle` line 558 are the only
   production `model.formula_scalar` calls.  In each case the argument is the
   original result of `model.occurrence_data`, containing `constant` and
   `merged`, and the second argument is the identity blob tuple.  Injected raw
   evaluators asserted `constant in formula` and `K not in formula`; both raw
   identity gates passed.  No compiled object reaches either raw evaluator.

3. **Compiled evaluation is independently implemented and well typed.**
   Producer line 633 and checker line 518 define separate helpers; neither
   imports the other.  Both require an integer `K`, a tuple of byte blobs, a
   dictionary `merged`, `(int, bytes)` keys, in-range coordinates, and integer
   coefficients.  They compare target bytes exactly, normalize `K` and every
   coefficient modulo 3, and return

   `(K + sum(hit coefficients)) mod 3`.

   Constant-only, hit, non-hit, cancellation, bounds, missing-`K`
   `constant` substitution, and malformed-`merged` gates passed independently
   in producer and checker.  An independent enumeration of 11,664 signed-K /
   signed-coefficient cases agreed pointwise between both v5 helpers and the
   pinned rank-ladder-v2 `formula_scalar(model,f,blobs)` ABI.

4. **All compiled call sites are unambiguous.**  Independent AST inspection
   found production compiled calls only at producer `selector_literal` line
   703, producer `retain_correction_candidate` line 880, and checker
   `selector_literal` line 584.  Thus frozen-prefix and appended-batch replay
   use the compiled helper through `selector_literal`, while the live retained
   correction lane uses the same compiled formula directly.  The real `run`
   still calls the one retained-candidate helper.  Every adjoint call remains
   the exact three-argument `v4.tau_free_adjoint(P,m,args)` ABI.

## Surgical-diff and dispatch-envelope audit

The complete v4-to-v5 textual diffs contain only:

- task/version/schema/marker/default-output changes;
- the two independent compiled helpers and the three production call-site
  substitutions above;
- bounded compiled/raw regression fixtures and their reported fields;
- exact v5 driver paths, pins, and markers.

There is no change to candidate ordering, finite selector universe,
action-first policy, retained-row ordering, batch size/order, state or segment
logic, checkpoint/rollback behavior, resource caps, or COMMON/RESOURCE
ownership.  In particular, the previously audited Task492 D1--D6 behavior is
byte-identical apart from version-driven schema/marker/path changes:

- producer marker versus checker marker remains separated;
- the immediate parsed predecessor content and actual state seal remain bound
  in a flat ancestor-read-free chain;
- BOOTSTRAP and own-schema zero-progress identity preservation, base first
  close, and own `CLOSED` first close remain exercised;
- one production retained-candidate helper remains shared with the fixture;
- RESOURCE skips the checker and cannot print global COMPLETE;
- post-batch `dual=None` profiles and aggregate-rises 17/zero-current/
  failed-close predicates remain covered.

The exact driver pins the audited producer/checker bytes, has one producer
invocation and one checker invocation located after the RESOURCE early exit,
and preserves
`14040 < 14220 < 14400` and
`4200000000 < 4500000000 < 5120000000` with `ulimit -v 5000000` KiB.
The generated shell contains zero v4 discovery paths or markers, so v4 files,
logs, receipts, and OK markers cannot satisfy the v5 gates.  COMMON completion
still requires the exact v5 checker PASS marker.

## Bounded audit record

- Exact sizes/SHA-256 and shared binding: PASS.
- Full v4-to-v5 diff and independent AST/call-target audit: PASS.
- Producer `python -B ...v5.py --mode FIXTURE --output %TEMP%/...`: PASS.
- Checker `--self-test` and `--pin-check`: PASS.
- Exact v4 producer/checker selector regression: `KeyError('constant')`;
  exact v5 entries: PASS.
- Independent compiled-v2 extensional comparison, 11,664 cases: PASS.
- Exact generated v5 shell, Git Bash `bash -n`: PASS; one producer,
  conditional one checker, RESOURCE-before-checker exit, marker/path/limit
  checks: PASS.
- GAP 4.16.0 via `gap.ps1`, exact-driver `ReadAsFunction`: exit 0 with only
  normal unbound-global warnings.
- Windows symlink fixture remained privilege-limited exactly as in v4; the
  production path guard was not weakened.
- No production selective runtime, GHA/workflow, authority computation, git
  operation, or persistent repository-extra file was used.

Mathematical status: **UNCHANGED**.  The Task487 C99 rank-99 premise remains
CROSS-CHECKED, not Lean-verified; this ruling repairs dispatch execution only
and asserts no new row, COMMON word, fake result, or Ihara conclusion.

GO_FOR_GHA_DISPATCH
