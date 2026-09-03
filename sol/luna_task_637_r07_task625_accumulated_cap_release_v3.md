# Luna Task637: Task625 cumulative-work-cap release v3

## 1. Scope

Read this mail completely.  Implement one finite workflow-only successor to
the audited Task632 release.  Do not edit either Python executable, v475,
Task632, the v2 workflow, or any unrelated file.  Do not run production, GHA,
or git.  Write only:

- `.github/workflows/d972-r07-a0-grade1-selected-slp-v3.yml`;
- `sol/luna_reply_637_r07_task625_accumulated_cap_release_v3.md`.

## 2. Exact parent and observed terminal

Read in full the final v2 workflow and Task634 reply.  Parent release commit:

```text
c4ae5094800d4acb812eefb21820b9998afc3804
```

GHA run/attempt/job `33732940935/1 / 100576830812` passed checkout, all
hashes, fixtures and downloads.  Producer telemetry completed the route and
source construction and then reached:

```text
elapsed                         about 448.5 s
peak RSS                        2,699,411,456 bytes
RSS at final complete stage     about 1.36 GiB
durable bytes                   231,680,287
interned paths                  29
maximum live entries            8,356
completed cumulative insertions 1,812,080
terminal                        UNKNOWN_RESOURCE:staged_state_cap
```

The next insertion crossed the shared `2,000,000` counter.  Log artifact id
`9884845034`, digest
`sha256:44429fafe79808d097130f172ab7766b7a81c1691be6bc60687f128740bdfdf3`;
`producer.log` is 4,534 bytes, SHA-256
`e5c86f0750fe348d3c30e073ec94053c2753817a8097c8e5280c802ab2b68f37`.
There was no payload and the checker did not run.

## 3. The only production change

Copy the exact audited v2 workflow into the new v3 path and change only the
versioned workflow identity/trigger/artifact labels plus:

```text
TASK625_ACCUMULATED_CAP: "50000000"
```

This counter is cumulative insertion/work telemetry, not retained live
memory.  Do not change the 60-minute job, 45-minute executable timeouts,
8-GiB VM limit, 7-GiB RSS and durable caps, 2,000,000 interned-path cap, path
length cap, exact parents, action pins, serial producer/checker order, or
success-only payload/always-log rules.  The unchanged RSS cap remains the
memory safety boundary.

Use versioned names consistently:

```text
workflow name: d972-r07-a0-grade1-selected-slp-staged-v3
fire marker:   [fire-grade1-selected-slp-staged-v3]
artifact stem: task625-grade1-selected-slp-staged-v3
```

Keep the v2 producer/checker and their exact Task632 hashes.  Do not claim the
new cap proves completion or a mathematical result; exhaustion at 50,000,000
remains `UNKNOWN_RESOURCE`.

## 4. Bounded gates and reply

Run only serial bounded gates: YAML parse, exact comparison showing the
permitted delta from v2, both existing tiny selftests, hash-pin checks,
immutable-action checks, placeholder/control/whitespace scan.  Record exact
bytes/SHA-256 of the new workflow and reply.  End the reply with a static
`READY_FOR_SOL_MAX_REAUDIT`, not launch authorization and not a result.
