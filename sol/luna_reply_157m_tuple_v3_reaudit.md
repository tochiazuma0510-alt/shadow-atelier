# 157m tuple-v3 post-repair re-audit

## Verdict: PASS

No remaining blocker or high finding was found. The three 157j findings are
closed in the current workflow, and the prior fail-closed/exactness gates are
preserved.

### 157j closure

1. The calibration matrix registers q3 as `q=3,a=-1` at workflow lines 21--24,
   and the full invocation passes both values explicitly at lines 57--63:
   `--q "$BURAU_Q" --a "$BURAU_A"`. There is no q3 fallback to the producer
   CLI default `a=2`.

2. Both jobs create the same hash-locked requirements file and use
   `pip download --only-binary=:all: --no-deps --require-hashes` followed by
   offline `pip install --no-index --no-deps --require-hashes` (calibration
   lines 42--49; q5 lines 133--140):

   - SymPy 1.14.0 wheel:
     `e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5`
   - mpmath 1.3.0 wheel:
     `a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c`

   Python 3.13.5 and SymPy 1.14.0 are runtime-gated at lines 49 and 140.

3. The q5 handoff now imports the checked-out producer and calls its complete
   `load_words()`, `producer_source_sha()`, and `calibration_ok()` contract for
   exactly `(3,-1)` and `(4,2)` (workflow lines 145--160). The producer's
   contract checks schema/status/q/a, all frozen hashes and semantic data,
   generator/A.18 order, presentation evidence, complete serialized kernel
   data, and every ordered 972-row key/digest/fiber record
   (`search/d972_b4_burau_fiber_v3.py:638--717`). The q5 full run repeats the
   same producer-side binding before computation (`:724--744`).

### Other gates

- Trigger and inputs are closed to the exact branch and the three registered
  paths (workflow lines 3--10); there is no arbitrary workflow input.
  Checkout is credential-free and permissions are read-only (lines 12--13 and
  26--29, 109--114).
- q3/q4 are independent `fail-fast:false` calibration lanes (lines 19--24),
  and q5 is admitted only after the calibration matrix succeeds (lines 99--107).
  Artifact names include the run attempt and uploads use `always()` (lines
  91--97 and 189--197); q5 downloads the exact q3/q4 names (lines 115--124).
- Self-test precedes each calibration full run and uses status, diagnostic, and
  exact-marker gates (lines 39--63). The q5 full run uses the same shell/status
  gates (lines 161--188). Exact traversal remains uncapped: section BFS,
  Schreier relators, kernel enumeration, normal-closure completion, and coset
  traversal are at producer lines 413--456, 488--537, with no arbitrary
  search/sample bound. The projected-order equality is a fail-closed exact
  condition (`:498--516`).
- q5 accepts only the two mathematical statuses and rejects
  `UNKNOWN_RESOURCE` (`workflow:168--188`). The producer maps calibration
  mismatch and resource exceptions to `UNKNOWN_RESOURCE` with nonzero exit
  (`:798--808`, `:938--948`); no resource stop can become PASS or B.
- The producer self-test includes the negative calibration fixtures and passes
  the exact self-test marker (`search/d972_b4_burau_fiber_v3.py:850--917`).

### Checks run

```text
python -B -c "import yaml; from pathlib import Path; x=yaml.safe_load(Path('.github/workflows/d972-burau-tuple-v3.yml').read_text()); print('YAML_PARSE_PASS', type(x).__name__, list(x.get('jobs',{})))"
YAML_PARSE_PASS dict ['calibrate', 'q5']

python -B -m py_compile search/d972_b4_burau_fiber_v3.py
python -B search/d972_b4_burau_fiber_v3.py --help
python -B search/d972_b4_burau_fiber_v3.py --self-test
D972_B4_BURAU_V3_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_FIBER_V3_SELFTEST_PASS
```

Both audited files have no trailing-whitespace lines. `git diff --check` was
not run because the task explicitly prohibits git operations; no local full
campaign/GAP, GHA dispatch, or implementation/workflow edit was performed.

### SHA-256

| File | SHA-256 |
|---|---|
| `.github/workflows/d972-burau-tuple-v3.yml` | `52817CE9DC3C51C9F7F0E9F3CEB880594F632AEF2F16A26D0E6D80BF0EA04B31` |
| `search/d972_b4_burau_fiber_v3.py` | `0508555B22747EB9E4A8C614ABA6AB7B4217E85E8C285F640C50F70906CB24AD` |
| `sol/luna_task_157h_tuple_v3_workflow.md` | `2DBD196D9B0A2252953F693D96F3D63539D38869A341F1F01E24554F19D0310C` |
| `sol/luna_reply_157h_tuple_v3_workflow.md` | `C9E8351222AB2C7C343E5EA8795A61A6902D5BD23C30CD614325C22D0331BA63` |
| `sol/luna_task_157j_tuple_v3_workflow_audit.md` | `D8AEE2DBC7DB178522E700FD9A516E9EC23E7A9E4FC3E1EBE4DD268B2B76ABBF` |
| `sol/luna_reply_157j_tuple_v3_workflow_audit.md` | `15FB8AEF372C2765E8249FAD4674E26D3FD1025432869EA794F557B378B7E72E` |
| `sol/luna_task_157k_tuple_v3_workflow_repair.md` | `9B02F7CCFBC031D5FC796DB7EE52BAEFED35848381D9FC8422D4E116008B970B` |
| `sol/luna_reply_157k_tuple_v3_workflow_repair.md` | `B900164FC8FFFD8B461AFC00C50C6F69C2160BDAB6D50111EF677A42C37A47FA` |
