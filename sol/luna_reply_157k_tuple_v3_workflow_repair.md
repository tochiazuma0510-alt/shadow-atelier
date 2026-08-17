# 157k tuple-v3 workflow repair

## Result

`PASS` for the requested static repair.  Only the authorized workflow and
this reply were changed; the producer was not modified.

### Blocker repaired

The calibration full command now passes the matrix row's exact parameter:

```text
workflow:58  python ... --q "$BURAU_Q" --a "$BURAU_A" --output ...
```

Thus q3 executes `(q,a)=(3,-1)` rather than silently falling back to the
producer CLI default `a=2`.

### Hash-gated dependencies

Both calibration and q5 jobs now create the same closed requirements file,
download only binary distributions with `--require-hashes`, and install
offline with `--no-index --no-deps --require-hashes`:

- `sympy==1.14.0` wheel SHA256
  `e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5`
- `mpmath==1.3.0` wheel SHA256
  `a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c`

The existing Python 3.13.5 and SymPy 1.14.0 runtime gates remain in place.

### Strong calibration handoff

The q5 precheck now imports the checked-out v3 producer without dispatching
it and calls its complete `load_words()`, `producer_source_sha()`, and
`calibration_ok()` contract for both `(3,-1)` and `(4,2)` receipts.  This
replaces the former type-only source-hash check and therefore inherits the
producer's fail-closed checks for schema/marker/status, source and frozen
hashes, semantic premises, generator/A.18 ordering, normal-closure and
Schreier evidence, complete kernel elements, and every ordered 972-row key,
word digest, fiber size, and defect count.  The producer selftest still runs
first in each calibration lane, including its negative fixtures.

Closed triggers, attempt-unique always-uploaded artifacts, exact terminal
markers, uncapped exact traversal, and `UNKNOWN_RESOURCE` non-success
behavior were preserved.

## Checks run

No local GAP, full campaign, GHA dispatch, or git operation was run.

```text
python -B -c "import yaml; from pathlib import Path; x=yaml.safe_load(Path('.github/workflows/d972-burau-tuple-v3.yml').read_text()); print('YAML_PARSE_PASS', list(x['jobs']))"
YAML_PARSE_PASS ['calibrate', 'q5']

python -m py_compile search/d972_b4_burau_fiber_v3.py
python search/d972_b4_burau_fiber_v3.py --help
python search/d972_b4_burau_fiber_v3.py --self-test
D972_B4_BURAU_V3_NEGATIVE_FIXTURES_PASS
D972_B4_BURAU_FIBER_V3_SELFTEST_PASS
```

`git diff --check` was not run because git operations are prohibited for this
task.

## File SHA256

- `.github/workflows/d972-burau-tuple-v3.yml`: `52817CE9DC3C51C9F7E0E9F3CEB880594F632AEF2F16A26D0E6D80BF0EA04B31`
- `search/d972_b4_burau_fiber_v3.py` (audited, unchanged): `0508555B22747EB9E4A8C614ABA6AB7B4217E85E8C285F640C50F70906CB24AD`
- `sol/luna_reply_157k_tuple_v3_workflow_repair.md`: `F17B96B3BD7D4E712736F73108E0CE9EA9F2F4319A7977D88A2C0967D13E66B7`
