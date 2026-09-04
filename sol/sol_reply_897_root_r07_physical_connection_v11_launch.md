# Root launch receipt -- R07 physical connection v11

## Outcome

The workflow-only semantic-artifact layout repair passed independent Sol(max)
Task896 and was launched exactly once.  The new run passed every pre-production
gate and remained inside the authenticated producer after the immediate v10
failure interval.

## Immutable launch identity

```text
branch=sol/r07-explicit-lift-20260825
workflow_commit=e01ffeae
marker_commit=b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2
marker=[task895-physical-connection-v11]
run/attempt=33876776771/1
job=101035535909
workflow=d972 r07 canonical P1 physical connection v11
url=https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/33876776771
```

The committed workflow receipt is:

```text
.github/workflows/d972-r07-canonical-p1-physical-connection-v11.yml
bytes=27497
LF=362
sha256=c7f3c9a8b728fa5ab0bd6be0b550b381e5b33d8ce1f59523dc04fb82b306fb74
```

## Observed boundary

Steps 1--16 completed successfully: setup, all exact authority queries,
downloads, immutable-source checks, launch construction, compilation and both
bounded executable selftests.  Step 17 `Run authenticated producer` entered
`in_progress` and remained there after a further 25-second poll.  This passes
the old missing `/semantic/prepare-receipt.json` point, which had rejected v10
within seven seconds.

This is a live production run, not a physical-connection result.  The final
candidate requires producer success, independent checker success and exact
artifact publication.

```text
PHYSICAL_CONNECTION=RUNNING
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
