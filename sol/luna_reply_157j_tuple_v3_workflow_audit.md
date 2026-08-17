# 157j tuple-v3 workflow adversarial audit

## Verdict

**`FAIL`**.

The workflow is otherwise closed-input, credential-free, staged, and
fail-closed in several important places, but the q3 calibration lane has a
blocking invocation error.

## BLOCKER

1. **q3 calibration passes no `--a` value (workflow line 52).**

   The calibration matrix sets `BURAU_A=-1` at lines 23 and 36, but the full
   producer command at line 52 is only
   `python ... --q "$BURAU_Q" --output ...`.  The producer's CLI default is
   `a=2` (producer line 932), so the q3 run executes `(q,a)=(3,2)`, which is
   outside the registered specializations `(3,-1),(4,2),(5,2),(5,4)` and
   exits nonzero.  The exact q3 marker/receipt gate at lines 55--82 therefore
   cannot pass, `calibrate` cannot succeed, and the dependent q5 job at line
   95 is never admitted.  The command must explicitly pass
   `--a "$BURAU_A"`.

## HIGH FINDINGS

2. **Dependency integrity is version-pinned but not hash-pinned (workflow
   lines 42--43 and 127--128).**

   Python `3.13.5` and SymPy `1.14.0` are version-gated, but
   `pip install 'sympy==1.14.0'` has no wheel/hash gate or locked transitive
   dependency set.  Thus the requested version/hash gate is incomplete; the
   exact package bytes are not authenticated by this workflow.

3. **The workflow's q5 calibration precheck is weaker than the producer's
   source-side authentication (lines 133--146).**

   It checks schema, marker, q/a, row count, and only that
   `producer_source_sha256` is a string.  It does not compare that hash to the
   checked-out producer or inspect `presentation_evidence`, complete kernel
   elements, deletion evidence, frozen semantic digests, or every calibration
   row's fiber/count fields.  The v3 producer's `calibration_ok` at lines
   638--715 does perform the stronger source/hash/evidence/kernel/972-row
   authentication before q5 computation, so this is defense-in-depth rather
   than a second mathematical bypass; nevertheless the workflow gate itself
   is not the advertised strong handoff gate.

## PASS findings

- **Closed trigger and paths:** push is restricted to
  `sol/d972-dmtcp-provision-v420` (workflow lines 3--10), and paths are exactly
  the workflow, v3 producer, and frozen word artifact.  No arbitrary inputs or
  dispatch path exists.
- **Permissions and credentials:** `contents: read` is set at line 13;
  checkout disables persisted credentials at lines 26--28 and 103--105.
- **Lane structure:** q3/q4 are an independent `fail-fast:false` matrix
  (lines 19--24); q5 waits for successful calibration and runs a separate
  `fail-fast:false` a=2/a=4 matrix (lines 94--101).
- **Selftest-first and shell status:** each lane uses `set -euo pipefail`,
  captures the Python status through `PIPESTATUS`, rejects diagnostics, and
  requires exactly one selftest marker (lines 39--50 and 124--128).
- **Calibration receipt gates:** when the invocation is repaired, lines
  60--83 gate exact schema/marker/status/q/a/orders, 972 ordered rows, unique
  keys, complete fibers, counts, and common-word membership.  The producer's
  `calibration_ok` additionally checks frozen hashes, source hash, presentation
  evidence, all serialized kernel elements, and every frozen row (producer
  lines 638--715), including negative fixtures in lines 887--913.
- **Exact traversal:** the producer's `exact_section` (lines 413--426),
  `kernel_from_section` (429--440), `enumerate_kernel` (443--456),
  `complete_hprime` (488--520), and `quotient_cosets` (523--537) have no
  arbitrary search cap or sampling bound.  The only projected-size check is
  the expected exact `P'` order; failure to reach it is fail-closed.  Resource
  exhaustion is converted to `UNKNOWN_RESOURCE` with exit code 2 (producer
  lines 938--944), and the workflow rejects it (lines 159--160 and 174).
- **Terminal/artifact handling:** full markers are exact-count checked for
  calibration (line 57) and q5 (line 175); q5 allows only candidate finite-zero
  fiber or all-pass `UNKNOWN` (lines 158--165), never a mathematical B claim.
  Calibration and q5 logs, receipts, inputs, and diagnostics are uploaded
  with `always()` and attempt-unique names (lines 85--91 and 176--183).
- **Memory/time:** both jobs have six-hour timeouts (lines 18 and 97) and an
  explicit 12 GB virtual-memory ceiling (lines 40 and 125).  These ceilings
  can stop an exact traversal, but the producer/workflow preserve the stop as
  non-success rather than converting it into PASS/A/B.

## Static and lightweight checks

Run without GAP, a full campaign, GHA, or git operations:

```text
python -B -c "import yaml; from pathlib import Path; x=yaml.safe_load(Path('.github/workflows/d972-burau-tuple-v3.yml').read_text()); print('YAML_PARSE_PASS', type(x).__name__, list(x.get('jobs',{})))"
YAML_PARSE_PASS dict ['calibrate', 'q5']

python -m py_compile search/d972_b4_burau_fiber_v3.py
python search/d972_b4_burau_fiber_v3.py --help
python search/d972_b4_burau_fiber_v3.py --self-test
D972_B4_BURAU_V3_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_FIBER_V3_SELFTEST_PASS
```

`git diff --check` was not run because this audit explicitly forbids git
operations.  No local GAP/full receipt run, GHA dispatch, or workflow edit was
performed.

## Audited file SHA-256

| File | SHA-256 |
|---|---|
| `.github/workflows/d972-burau-tuple-v3.yml` | `16C7DB1B1D2C651C8790455C16EE1C0D412AFDF6C471FE08424D60E2AD173AAF` |
| `search/d972_b4_burau_fiber_v3.py` | `0508555B22747EB9E4A8C614ABA6AB7B4217E85E8C285F640C50F70906CB24AD` |
| `sol/luna_task_157h_tuple_v3_workflow.md` | `2DBD196D9B0A2252953F693D96F3D63539D38869A341F1F01E24554F19D0310C` |
| `sol/luna_reply_157h_tuple_v3_workflow.md` | `C9E8351222AB2C7C343E5EA8795A61A6902D5BD23C30CD614325C22D0331BA63` |

Earliest repair: add `--a "$BURAU_A"` to workflow line 52, then rerun the
static gates and calibration campaign under the repaired file hashes.
