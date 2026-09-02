# Luna reply 567 — packed GF(3) compiled backend v1

Implemented exactly the four authorized files. This is a candidate linear
algebra primitive only; no production merge, certificate, roster closure,
dual claim, ancestry claim, or grade-two action was performed.

## Output receipts

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_packed_gf3_echelon_backend_v1.c` | 10593 | `5584c0de34e348935c64f641436bc8b43239b9da7ecdc21abf09f12ee3a511fd` |
| `search/d972_packed_gf3_echelon_backend_v1.py` | 10645 | `53165193a3087e24e2d5eba3ea474d3aa58a7ab5df48fe08f3b9b8c658b14b51` |
| `search/check_d972_packed_gf3_echelon_backend_v1.py` | 14120 | `161912fd2fe7ee4f071079a92f16609d072a2c4de31d33faf93d7258be54ad8c` |
| `sol/luna_reply_567_r07_packed_gf3_compiled_backend_v1.md` | measured after close | measured after close |

The ABI is version `1`, schema `packed-gf3-echelon-v1`, with a checked binary
header, row-major four-trit bytes, uint64 opaque row IDs, and one target row.
The C worker streams offered rows, retains only accepted basis rows plus the
ledger, checks all declared dimensions/products/file trailing bytes, rejects
bytes above 80, and checks the earlier-byte/leading-one pivot invariant before
each suffix update. JSON contains insertion-order accepted rows, leads,
reduction pairs, acceptance/normalization fields, and the target
reductions/complete coefficient list/remainder. Offered remainders are not
retained, avoiding a second full input matrix. The Python wrapper
fails closed when no compiled executable is configured; its reference path is
explicitly test-only.

## Commands and results

```text
$env:PYTHONPYCACHEPREFIX = Join-Path $env:TEMP 'd972-packed-gf3-pycache'
python -B -m py_compile search/d972_packed_gf3_echelon_backend_v1.py search/check_d972_packed_gf3_echelon_backend_v1.py
```

Exit 0; measured wall time 0.2283297 s. The independent checker was then
run serially:

```text
python -B -u search/check_d972_packed_gf3_echelon_backend_v1.py
```

Exit 0; measured wall time 0.3054483 s. Fixture output:

```json
{"compiled": false, "compiled_status": "COMPILED_FIXTURE_NOT_RUN_NO_COMPILER", "compiler": "none", "elapsed_seconds": 0.066838, "fixture": "PASS", "frozen_cases": 6, "member_target": "PASS", "mutations_rejected": 7, "nonmember_remainder": "PASS", "random_rows": 32, "reference_benchmark_seconds": 0.003371, "resume_boundary": "PASS", "suffix_full": "PASS"}
```

The six frozen cases are zero, missing pivot, multiple nonzero trits in one
pivot byte, nonmonotone leads `[5,3]`, coefficient-two normalization, and the
dependent trace `[[1,1],[0,2],[2,2]]`. The independent checker also covers
deterministic randomized rows, suffix/full equality, member target replay,
nonmember nonzero remainder, opaque IDs, resume boundary, and seven rejection
mutations (bad input byte, truncation, schema, pivot lead, coefficient/ledger
offset, and receipt field corruption).

`Get-Command clang,gcc,cc,cl -ErrorAction SilentlyContinue` found no local C
compiler. Therefore no compiled execution or speedup number is claimed;
compiled execution remains for the separately audited GHA calibration. No
temporary build product was placed in the repository, and no certificate was
created.

CURRENT GRADE-ONE RUNS: unchanged
GRADE-TWO PRODUCTION: not launched
MATHEMATICAL TERMINAL: none
verified=false

PACKED_GF3_BACKEND_V1_CANDIDATE_AUDIT_REQUIRED
