# Task914 narrow re-audit -- actual root scalar batch v1

## Verdict

`FAIL/unsafe`.  Task913 repaired the two Task912 comparison and control-test
classes in substance, but left one fatal one-field wiring omission on the
ordinary checker path.

## 1. Complete output comparison and remaining blocker

`check_output` independently reconstructs the four complete character
records, then the complete terminal, result, and output manifest.  The
terminal reconstruction fixes its kind, character/actor order, character
roster, counts, orbit bound, and every conservative claim field.  The result
reconstruction fixes `launch_sha256`, the separator and P1 manifest hashes,
the ordered four Task712 manifest hashes, relation-stream hash, character and
terminal joins, file receipts, and claims.  The manifest reconstruction fixes
the exact file roster, exact sorted receipts, result receipt, terminal kind,
and conservative candidate/verified values.  `validate_character_record` and
`validate_output_objects` then require exact object equality as well as valid
embedded seals, so extra fields are also rejected.

The bounded checker selftest executes coherent reseals of relation, child,
scalar-prefix, terminal-claim, manifest-terminal, launch, separator, P1, and
all four Task712-join fields.  Each changed object is canonically resealed and
is rejected by the same exact-equality helpers used by `check_output`.
Consequently the Task912 unchecked-field weakness is repaired at the
comparison layer.

However, checker `validate_launch` returns `launch`, `launch_raw`, separator,
P1, Task554, and Task712 data, but does **not** return `launch_sha256`
(checker lines 437--438).  `check_output` unconditionally reads
`base["launch_sha256"]` while constructing the expected result (line 806).
Thus every ordinary `--check-launch` execution reaches a deterministic
`KeyError: 'launch_sha256'` after its replay instead of accepting even a valid
producer output.  The public selftest does not call this full `check_output`
path, so its PASS does not cover the omission.

Smallest repair: add exactly `"launch_sha256": sha(raw)` to the base object
returned by checker `validate_launch` (equivalently derive that same value
from its authenticated `launch_raw` in `check_output`).  No producer,
workflow, formula, or parent change is needed.

## 2. Executed selftest controls

Both public selftests returned PASS, and each advertised flag is downstream
of an executed assertion/control:

- a real temporary separator parent is accepted, then an internal sealed
  receipt mutation is rejected;
- real temporary Task712 table parsing accepts the transpose and rejects a
  mutated, resealed non-transpose table;
- a one-row P1 parent and production projection path execute, after which a
  manifest-digest mutation and cache truncation are rejected;
- the Task554 expression validator used by every body rejects reversed term
  order;
- four actual zero-root constructors feed the shared classifier and prove
  `AllFourRootEOF`;
- live-size arrays exercise the full `44 + 4*8059 = 32280` origin EOF scan,
  plus first-seed and first-actor violation order;
- a genuine tiny prepare plus two nonempty new blocks exercises all four
  actor slots and local/global offsets; its production accumulator arrays are
  exactly compared with a separately written direct fold;
- checker exact-record/output helpers execute the coherent relation, child,
  prefix, terminal-claim, manifest-terminal, and parent-join reseal
  rejections.

These controls repair Task912's literal-telemetry issue, but do not cure the
ordinary-path missing key above.

## 3. Retained bounded gates

Full reread found no regression in the accepted mod-3 scalar fold, seed-first
then actor-first scan, vectorized packed P1 projection, or one-pass/one-block
memory form.  Producer and checker each retain one 256-row cache buffer, one
cache pass, one prepare body, and one Task554 block at a time; no global
relation tree or all-row dense matrix is materialized.  Frozen arithmetic,
root/child, P1, separator, Task554, and Task712 pins remain in place.

The unchanged workflow retains the sole marker, 90-minute job cap,
40-minute producer/checker caps, exact parent metadata checks (including the
accepted Task554 `completed/failure` conclusion), checker-after-producer
ordering, final publication only after both succeed, and always-uploaded
diagnostics.  Claims remain conservative and `verified=false`.

## 4. Bounded commands and receipts

No actual parent, download, GHA, or git command was run.  A unique directory
under `%TEMP%` was used as `PYTHONPYCACHEPREFIX`.

```text
python -m py_compile search/d972_r07_actual_grade2_root_scalar_batch_v1.py search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py
exit=0  elapsed=0.725 s

python -u search/d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest
exit=0  status=PASS  elapsed=3.922 s

python -u search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest
exit=0  status=PASS  elapsed=1.960 s
```

Receipts were recomputed with `[IO.File]::ReadAllBytes`, LF byte counting, and
`Get-FileHash -Algorithm SHA256`:

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_actual_grade2_root_scalar_batch_v1.py` | 78662 | 1361 | `aa76f1ff16314f6e3b6253d3d0276a21934ae493c0bd0318065ec73c50b98d72` |
| `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py` | 79522 | 1286 | `c331e009a184096454cd67bff017db320059187fe4c833a2ce8ec530ce800b0c` |
| `.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v1.yml` | 23735 | 433 | `cfa9814863e2c61db3158b5940854b72e9c0cd0bbd4b0ab53ea4a29fa7a238c3` |
| `sol/luna_reply_908_r07_actual_root_scalar_batch_v1.md` | 4440 | 48 | `0c1a7808a27086fba388f9e3106330a5c250390d1042f9eb7ead3acf32939741` |

VERDICT=FAIL
SAFE_TO_PUSH_TRIGGER_GHA=no
