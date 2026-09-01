# Task476 adversarial audit — compact actual positive owner v5

## Verdict

**STOP / NOT DISPATCHABLE / DO NOT ADOPT v5 AS A GHA PRODUCTION DRIVER.**

The commissioned inherited-driver tuple repair is correct, and the bounded
v4 producer/checker ABI checks pass.  However, the inherited driver envelope
has a fatal execution omission: v5 writes the complete strict bash payload,
closes it, and prints `...DRIVER_READY`, but never executes that payload.
The registered generic workflow also does not execute a shell file emitted by
the GAP script.  A normal dispatch would therefore run zero producer and zero
checker processes while potentially reporting a successful workflow.

No production result, MEMBER, lift, fake, Ihara assertion, or negative result
is established here.  `verified=false`.

## F1 — fatal dormant-shell dispatch

Lines 24--46 of
`search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v5.g`
write the intended payload to
`ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v5.sh`.  The payload
does contain the required

```text
set -euo pipefail
```

and its final command would write the exact `...V5_DRIVER_COMPLETE` sentinel.
But the GAP driver ends with only

```gap
CloseStream(D475S);;
Print("R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V5_DRIVER_READY\n");
```

There is no `Exec(...)`, no `bash D475Script`, and no post-execution sentinel
check.  The bounded cardinality scan returned

```text
close_stream=1
exec_calls=0
producer_checker_uB_commands=2   # text written into the dormant shell
inline_json_commands=1           # text written into the dormant shell
```

This is not repaired by `.github/workflows/gap-run.yml`.  Its ordinary path
constructs `ci/out/driver.g` as the optional preamble followed by exactly
`Read("$GAP_RUN_SCRIPT")` (lines 237--243), invokes GAP once (line 248), and
then proceeds to its special-case P2 gate and artifact upload (lines 249--285).
There is no step which discovers or runs the generated v5 shell.  Thus the
physical pin tests, producer, MEMBER-only checker, UNKNOWN frontier check,
and COMPLETE sentinel are all unreachable in an ordinary v5 dispatch.

The printed READY marker certifies only that shell text was written.  It is
not a production or checker terminal.  Consequently no exact dispatch
contract can be issued for v5.

## Passed bounded findings

### F2 — Task476's requested tuple repair and diff confinement pass

The named inherited file is physically exactly

```text
search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g
4233
b1851ea2835ef752b64b8f04c6489bd9f9630178fadbe8acf38c7fb0aeb2a5d7
```

and v5 advertises that complete path/byte/SHA tuple exactly.  The v5 source is

```text
4183
354b29144e6d72ce43e7c6511458a6cd757709dce1e7b12ce9b1f004a4351ef6
```

It is ASCII-only and newline-terminated.  An exact in-memory comparison after
normalizing only `D475` to `D474`, Task476 to Task473, owned v5 output/marker
names to v4, and the repaired inherited tuple back to the v4 contaminated
tuple returned `normalized_equal=True`.  Hence no other v4-to-v5 textual or
executable change is hidden in Task476.  In particular, F1 is inherited from
v4 rather than introduced by Luna's tuple repair.

### F3 — v4 producer/checker pins, generated bodies, CLI, and terminals pass

The driver pins the physical files exactly:

```text
producer search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py
         1876 0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9
checker  crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v4.py
         2552 a94e8180b0280fac92fbf749591c5985092188a62aab08cda2299e2c22d23eeb
```

Bounded `python -B` load-without-main reproduced the sealed bodies:

```text
producer 61376 d9a5a136d875d2fb7f5d596966abf094b7c555a0e4eb4ac6576c72071f734b84
checker  47875 c65f4e7a122f835f5c50b03d6c189ff26a319518ac8b525d6f3d0943b8412ed0
```

Both expose `MEMBER = R07_ZERO_BASE_A5_A6_MEMBER` and the frozen Task193-v5
receipt/verdict schemas.  The producer parser accepts the driver-supplied
`--mode PRODUCTION`, Task193 pair, output, `--seconds 14400`, and
`--rss-bytes 5700000000`, and asserts those frozen caps.  Its stdout prefix is
exactly
`R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V4_PRODUCER_TERMINAL`.
The checker accepts the supplied production/Task193/receipt/output arguments;
its omitted seconds/RSS arguments take and assert the same frozen defaults.
Its production envelope requires `status=COMPLETE`, the actual MEMBER
terminal, and then calls only `check_member`.  The dormant shell extracts the
correct v4 producer prefix and branches on the same MEMBER literal.

### F4 — intended shell process/cost policy passes, conditional on execution

The generated payload text contains exactly one intended producer command and
one checker command syntactically confined to the MEMBER branch.  The only
other Python process is the small nonpositive JSON frontier assertion.  It has
no production SELFTEST/FIXTURE, checkpoint/resume route, external target, or
extra mathematical traversal.  Every accepted nonpositive terminal is checked
against `resumable=false` and the complete six-field NONE/false frontier.
Thus no unnecessary heavy process was added; the defect is instead that none
of the intended processes is launched.

The audit used only byte/hash reads, exact in-memory text comparison, static
scans, and `python -B` load-without-main/AST inspection.  It ran no production,
GHA, workflow, full-authority computation, git operation, or bytecode cache.

## Minimal repair only

Create a versioned successor; do not edit v5 or regenerate the v4
producer/checker.  Preserve the repaired v3 tuple, all v4 pins, mathematics,
caps, terminal policy, and frontiers.  After closing the successor shell,
execute it exactly once and fail closed on the exact fresh COMPLETE sentinel,
for example in the successor's own names:

```gap
CloseStream(DxxxS);;
Exec(Concatenation("bash ",DxxxScript));;
if not IsExistingFile(DxxxOK) then Error("compact v6 missing success marker"); fi;
if StringFile(DxxxOK) <> "R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V6_DRIVER_COMPLETE\n" then
  Error("compact v6 bad success marker");
fi;
Print("R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V6_DRIVER_COMPLETE\n");
```

Add a bounded static gate proving the single shell execution occurs after
`CloseStream`, that the exact sentinel is checked afterward, and that the
shell still contains one producer plus a MEMBER-only checker.  Before any
eventual dispatch, the broker must also materialize an actual authenticated
Task193-v5 receipt/verdict pair at the two job-local paths supplied in the
preamble; the current generic workflow does not create that pair for this
script prefix.

`TASK476_R07_COMPACT_ACTUAL_POSITIVE_OWNER_V5_AUDIT_STOP`
