# Luna reply 494 — rank-99 compiled-formula replay repair v5

## Scope and semantic diff

Implemented only the four requested v5 outputs.  The v4 finite universe,
search order, batching, checkpoint/BOOTSTRAP and zero-progress semantics,
resource limits, retained-candidate helper, D1--D6 behavior, and raw Task179
identity lane are preserved.

The surgical v4-to-v5 changes are:

- `search/..._v5.py:633`: new independent `compiled_formula_scalar` ABI
  validator/evaluator.  It requires integer `K`, mapping-shaped `merged`,
  `(int, bytes)` keys, integer coefficients reduced modulo 3, blob-coordinate
  bounds, and exact target-byte comparison.
- `search/..._v5.py:703`: frozen-prefix `selector_literal` now calls the
  compiled helper; `:675` remains the raw
  `model.formula_scalar(formula, ids)` identity check.
- `search/..._v5.py:880`: live retained-correction evaluation now calls the
  compiled helper instead of `v4.b.formula_scalar`.
- `crosscheck/..._v5.py:518`: independent checker helper; `:584` uses it,
  while `:558` remains the raw identity evaluator.
- Producer fixture `:1287` and checker self-test `:876` cover constant-only,
  one-hit, non-hit, cancellation, bounds, malformed `constant` substitution,
  malformed `merged`, raw-lane preservation, and the frozen selector replay
  call with a raw-evaluator sentinel that would fail under the v4 bug.
- Both scripts use v5 schema/markers/default output paths.  The driver uses
  v5 paths/markers and cannot accept v4 output.

## Final pins

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py` | 104031 | `25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09` |
| `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py` | 71589 | `970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d` |
| `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v5.g` | 9425 | `bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d` |

Shared v5 binding: `0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b`.

## Commands and bounded results

All commands were run from `C:\Users\81905\Desktop\shadow-atelier`:

```text
python -c "from pathlib import Path; [compile(Path(p).read_text(encoding='utf-8'),p,'exec') for p in ['search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py','crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py']]"
python search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py --mode FIXTURE
python crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py --self-test
python crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py --pin-check
```

The AST compile, producer FIXTURE, checker SELFTEST, checker PIN_CHECK, and
exact driver producer/checker pin check all passed.  A bounded GAP harness
executed the v5 driver only through temporary `%TEMP%` paths with the
production shell execution replaced by `QUIT`; the generated shell passed
`bash -n` (`GAP_BOUNDED_PARSE_PASS`, `GENERATED_SHELL_SYNTAX_PASS`).

No production selective runtime, GHA, workflow, git, or production result was
run or produced.  The temporary producer fixture receipt was removed; no
cache or fixture file is part of the repository output.

TASK494_R07_RANK99_COMPILED_FORMULA_REPLAY_REPAIR_V5_PASS
