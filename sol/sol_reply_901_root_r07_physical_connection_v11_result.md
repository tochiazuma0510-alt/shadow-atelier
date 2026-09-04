# Root result receipt -- R07 physical connection v11

## Result

GHA run/attempt `33876776771/1`, job `101035535909`, completed successfully.
The authenticated producer, independent full replay checker, and final
candidate publication all returned success.  Under the workshop hierarchy
this physical-connection artifact is **cross-checked**, not Lean-verified.

```text
branch=sol/r07-explicit-lift-20260825
workflow_commit=e01ffeae
marker_commit=b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2
run/attempt=33876776771/1
job=101035535909
run_status=completed
run_conclusion=success
job_started=2026-09-04T13:12:30Z
job_completed=2026-09-04T13:58:58Z
url=https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/33876776771
```

The producer step ran from approximately `13:13:09Z` until the checker began
at `13:36:29Z`; the independent checker completed at `13:58:52Z`.  The final
checker receipt is:

```text
offers=8059
rank=6705
dependent=1354
reductions=7665974
rolling=3cb1bcf691038d71082b8d4774c5dd8898a239e71ef64da22ec486ba923cb8bd
source_pair_calls=8059
checker_pair_calls=8059
source_node0/checker_node0=1/1
source_node3523/checker_node3523=1/1
verified=false
```

The immutable final artifact is:

```text
id=9939860701
name=d972-r07-canonical-p1-physical-connection-v11-candidate-33876776771-1
archive_bytes=245546516
digest=sha256:0c3753d7384a7850aadab41c9ec2755114475862a0b03fd806e875005a72995a
expires_at=2026-12-03T13:12:28Z
expired=false
```

This closes the actual J1 connection input.  It does not decide whether the
fixed rho2 is in the physical span.  That decision begins by constructing the
file-backed rank-`<=6705` physical state and reducing rho2 against it.

```text
PHYSICAL_CONNECTION=cross-checked
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
