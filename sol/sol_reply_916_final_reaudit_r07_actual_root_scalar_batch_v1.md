# Task916 final narrow re-audit -- actual root scalar batch v1

## Ruling

PASS.  Task915 fixes the sole Task914 blocker without changing the producer,
workflow, mathematical evaluator, parents, or claim boundary.

## Launch SHA handoff

Checker `validate_launch` first reads the launch through `read_json`, which
hashes/reads it and requires that the decoded value re-encode to the exact
canonical bytes.  Its returned base object now contains
`"launch_sha256": sha(raw)` (lines 416--438).  `check_output` consumes that
same base field verbatim as the expected result's `launch_sha256` (line 806),
then exact-compares the reconstructed result.  There is no second launch
serialization or attacker-supplied hash in this handoff.

The public checker selftest now writes a canonical temporary launch file and
passes that file through the real `validate_launch`.  Only the three large
parent validators are temporarily replaced; launch parsing, canonical-byte
authentication, exact shape/claims/source checks, Task712 parent pins, and
the returned handoff are real.  It asserts both returned raw-byte identity
and `checked["launch_sha256"] == sha(authenticated_raw)` before setting
`launch_sha256_handoff=true`.  The executed public selftest reported that
flag true.

## Retained Task913 gates

Source review reconfirms that checker independently reconstructs all four
character records and then the complete terminal, result, and manifest.
Exact sealed equality fixes every terminal claim and kind/character roster,
all launch/separator/P1/ordered-Task712/result/terminal joins, and the exact
file roster; additional fields and coherently resealed false values remain
rejected.

All Task913 executed controls remain on the public selftest path: separator,
Task712 transpose, P1 digest/truncation, and Task554 order mutations;
relation/child/prefix/terminal/result reseals; four zero roots and
`AllFourRootEOF`; seed-first and actor-first violations; the full 32,280
origin EOF scan; and the genuine two-nonempty-block/four-slot accumulator
against its separately written direct reference.

The producer receipt is byte-identical to Task914.  The accepted mod-3 fold,
vectorized 256-row projection, seed/actor ordering, single P1 cache pass, and
prepare-plus-one-current-block residency are unchanged.  The workflow is
also byte-identical: exact parent pins, sole marker, 90-minute job cap,
40-minute producer/checker caps, sequential acceptance, and conservative
publication gates remain intact.  Claims still state root-batch candidate
only, incomplete dual orbits, undecided Grade2 status, no A0/COMMON/cofinal/
fake/Ihara declaration, and `verified=false`.

## Bounded execution

No actual parent, download, GHA, or git command was run.  Compilation used a
unique `%TEMP%` `PYTHONPYCACHEPREFIX`.

```text
python -m py_compile search/d972_r07_actual_grade2_root_scalar_batch_v1.py search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py
exit=0  elapsed=0.320 s

python -u search/d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest
exit=0  status=PASS  elapsed=2.562 s

python -u search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest
exit=0  status=PASS  launch_sha256_handoff=true  elapsed=1.971 s
```

## Current receipts

Bytes and LF counts were taken from the raw bytes; SHA-256 was recomputed
with `Get-FileHash -Algorithm SHA256`.  All four files have zero CR bytes and
no BOM.

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_actual_grade2_root_scalar_batch_v1.py` | 78662 | 1361 | `aa76f1ff16314f6e3b6253d3d0276a21934ae493c0bd0318065ec73c50b98d72` |
| `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py` | 81753 | 1321 | `dea105cd8c196565d95c6828c4afdfdd7f1d6395b5d85dfb7d3447fdfe4f0fa2` |
| `.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v1.yml` | 23735 | 433 | `cfa9814863e2c61db3158b5940854b72e9c0cd0bbd4b0ab53ea4a29fa7a238c3` |
| `sol/luna_reply_908_r07_actual_root_scalar_batch_v1.md` | 4530 | 48 | `6cd917350cd76d0926d1a2e7d65ac3460dfc1c8f6ec5d3a8387b37be8aa3478a` |

VERDICT=PASS
SAFE_TO_PUSH_TRIGGER_GHA=yes
