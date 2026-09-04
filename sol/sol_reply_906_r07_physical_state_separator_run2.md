# Sol reply -- R07 physical-state separator run 2 result

## Disposition

The repaired fresh live run completed successfully through producer,
independent checker, both uploads, and final publication.  Its terminal is a
canonical initial `Separator`, not a `ConnectionMember`.  This separates the
fixed rho2 target from the current 1,354-row physical state only.  It is the
next J3 scalar/CEGAR input and is not a full grade-two NONMEMBER, A0, COMMON,
cofinal lift, fake certificate, or Ihara witness.

## GHA and final artifact authority

```text
commit=7b7b9de20faaa3b8f26e331bb738b374f6f5708c
workflow=.github/workflows/d972-r07-grade2-physical-state-separator-v2.yml
run/attempt=33891714539/1
job=101084707867
run=completed/success
job=completed/success
job_started=2026-09-04T15:49:50Z
job_completed=2026-09-04T15:53:09Z
producer=success (15:50:26Z--15:51:50Z)
independent_checker=success (15:51:50Z--15:53:00Z)
unchecked_upload=success
final_upload=success
```

Final artifact:

```text
id=9944214057
name=d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1
archive_bytes=107195261
digest=sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017
expired=false
expires_at=2026-12-03T15:49:47Z
```

The diagnostic unchecked artifact is id `9944212161`, 107,668,798 bytes,
digest
`sha256:393b49f607cb0cb176e71f874472c6564c34598c187fcddd85abbfee175b8694`.
It is not used as the final authority.

Root downloaded the named final artifact outside the repository at
`C:/Users/81905/AppData/Local/Temp/shadow-atelier-task904-run33891714539-final`.
Its exact file receipts are:

| file | bytes | SHA-256 |
|---|---:|---|
| `state/HEAD` | 299 | `f789ac352864ae662beced75f9004887fe677f81eee922eb9d9200dcaf6860ef` |
| `state/manifest.json` | 7,780 | `d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b` |
| `state/physical.bin` | 16,377,984 | `1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e` |
| `state/physical-p1-coeff.bin` | 2,728,310 | `a2d462ea6c8685a59e28f3f5d1c89656e2e942a65110a21184e33c6cb334826c` |
| `state/instructions.jsonl` | 86,919,157 | `a7cbe317ba92b0d4076623dfd5ea672d2ef4b154f5be2862e0dc232ba91309c2` |
| `output/lambda.bin` | 12,096 | `7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed` |
| `output/reverse-substitution.jsonl` | 232,321 | `b1119a6aa506e8ccca339dfbc140f5a59a5bc732db2f266f2a81dff762e115f7` |
| `output/terminal.json` | 457,656 | `098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf` |
| `output/result.json` | 457,791 | `d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968` |
| `checker-result.json` | 515 | `2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433` |

## Terminal semantics

The state is complete at `cursor=offers=authenticated_offers=generation=8059`,
with `physical_offers=rank=1354`, `skipped=6705`, `dependent=0`, state head
`69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88`,
and physical reduction bound 915,981.  The fixed rho2 was reduced by 884
insertion-order pivots.  The nonzero remainder has SHA-256
`e0053fc6e745e4459e0324d26320bf9f5e434a2942fa4a519ebaf9e28df50011`.

Reverse substitution over all 1,354 pivots produced:

```text
kind=Separator
free_coordinate=1417
free_value=2
lambda_bytes=12096
lambda_sha256=7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed
lambda_physical_pivots=0
lambda_rho2=1
target_reduction_sha256=521cfa1702f1a561e44e15ad148511dd17a49941d654a84cbdd953509e7837e6
```

The independent checker returned `status=PASS`, `kind=Separator`,
`source_offers=8059`, `physical_rank=1354`, `dependent=0`, `skipped=6705`,
`target_reductions=884`, `separator_free_coordinate=1417`,
`nonmonotone_insertion=true`, and `reverse_substitution=true`.

As a third, small root-side check independent of the producer/checker helper
implementations, all packed base-3 coordinates were decoded directly.  The
12,096-byte lambda has 914 nonzero coordinates; its dot product with each of
all 1,354 stored physical rows is zero, while its dot product with the exact
rho2 packed vector is one:

```text
INDEPENDENT_DOT_CHECK=PASS rows=1354 bad=0 lambda_rho2=1 lambda_support=914
```

This note is candidate result bookkeeping pending Sol(max) Task907's hostile
same-object audit.  The embedded producer/checker JSON deliberately retains
`cross_checked=false` and all upper claims false; no promotion is made here
before that audit.

```text
INITIAL_SEPARATOR=FOUND
INITIAL_SEPARATOR_CROSS_CHECKED=pending_Task907
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
