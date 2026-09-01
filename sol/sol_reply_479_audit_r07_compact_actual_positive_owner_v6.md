# Task479 adversarial audit — compact actual positive owner v6

## Verdict

**GO — accept v6 as the exact Task476-F1 dormant-shell repair.**

This GO is for adopting the versioned driver, not for dispatching it now.
The authenticated Task193-v5 receipt/verdict pair is still an undischarged
runtime premise.  The broker must materialize that pair at the two supplied
job-local paths before production dispatch.  No production result, MEMBER,
lift, fake, Ihara assertion, or negative result is established here;
`verified=false`.

## F1 — dormant-shell false success is repaired

The decisive suffix is exactly lines 47--53 of
`search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v6.g`:

```gap
CloseStream(D479S);;
Exec(Concatenation("bash ",D479Script));;
if not IsExistingFile(D479OK) then Error("task479 missing success marker"); fi;
if StringFile(D479OK) <> "R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V6_DRIVER_COMPLETE\n" then
  Error("task479 bad success marker");
fi;
Print("R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V6_DRIVER_COMPLETE\n");
```

The static cardinalities are

```text
CloseStream calls = 1
Exec calls        = 1
owned-shell Exec  = 1
DRIVER_READY      = 0
```

and their source order is strict: `CloseStream` precedes the sole `Exec`,
which precedes the existence check, exact-content check, and final GAP
terminal.  Thus the shell text is no longer dormant.  Even if `Exec` itself
does not propagate a child exit status, the post-execution marker tests close
that gap.

Freshness and fail-closed behavior also pass.  Lines 21--23 reject a preexisting
v6 `.ok` file together with every other owned output.  The generated strict
shell writes the marker only as its final command (line 46).  Therefore a
producer, MEMBER checker, nonpositive assertion, or preceding shell command
failure prevents marker creation under `set -euo pipefail`; absence, unreadable
content, extra content, or a wrong marker then prevents the GAP COMPLETE
terminal.  The three marker literals in the source have exactly the intended
roles: generated-shell write, post-`Exec` comparison, and final print.

## F2 — v5 body, cardinality, and MEMBER-only policy are preserved

After only the version/owner renamings
`D479->D475`, `task479/Task479->task476/Task476`, and `v6/V6->v5/V5`, the v6
source is byte-for-byte equal to v5 from byte zero through
`CloseStream(D475S);;`.  The remaining v6 suffix is exactly the six-line repair
quoted in F1.  Hence no mathematical body, producer/checker CLI, cap, accepted
terminal, frontier, or shell command was silently changed.

The generated payload has the required exact process inventory:

```text
producer commands            = 1   (line 34)
checker commands             = 1   (line 39)
small nonpositive assertions = 1   (line 43)
```

The checker command lies only inside the branch whose condition is the exact
literal `R07_ZERO_BASE_A5_A6_MEMBER` (lines 38--41).  All other accepted
producer terminals go to the small six-field NONE/false JSON assertion.  A
bounded forbidden-token scan found no SELFTEST, FIXTURE, retry, worker pool,
checkpoint/resume route, workflow route, or additional traversal.  The only
new runtime work relative to the defective v5 envelope is the required single
execution of the already-generated payload plus constant-size marker reads.

## F3 — physical pins and generated ABIs agree

Read-only byte/SHA256 checks reproduced the registered tuples exactly:

```text
v5 driver
  4183 354b29144e6d72ce43e7c6511458a6cd757709dce1e7b12ce9b1f004a4351ef6
inherited v3 driver
  4233 b1851ea2835ef752b64b8f04c6489bd9f9630178fadbe8acf38c7fb0aeb2a5d7
v4 producer wrapper
  1876 0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9
v4 checker wrapper
  2552 a94e8180b0280fac92fbf749591c5985092188a62aab08cda2299e2c22d23eeb
```

The independent `python -B` load-without-main gate reconstructed the frozen
bodies as

```text
producer 61376 d9a5a136d875d2fb7f5d596966abf094b7c555a0e4eb4ac6576c72071f734b84
checker  47875 c65f4e7a122f835f5c50b03d6c189ff26a319518ac8b525d6f3d0943b8412ed0
MEMBER   R07_ZERO_BASE_A5_A6_MEMBER (both)
```

The v6 file itself is ASCII-only, newline-terminated, and is exactly

```text
4446 c32d007f96d7c4e889ef56fac3c8f00aec49b9832c39b409d32a5aca918132d8
```

These values agree with the Task479 report.

## F4 — Task193 is a real, still-undischarged input premise

Lines 6--7 require explicit `D479Task193Receipt` and
`D479Task193Verdict`; v6 supplies neither defaults nor fixtures.  The frozen
producer and checker both pin the physical Task193-v5 producer, checker, and
driver, whose current tuples also match:

```text
producer 12207 fab51e296170ac34ebe48b49d79d3460017a51cd797d524e7b0d89481f23960f
checker   7795 941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e
driver    2269 d2cab901ae608d88bcff6dacdee6072c780b9157e1955cbaa740d227a8f2fe7a
```

Their loaders read both JSON files and require self-seals, the v5 schema,
PASS/positive terminals, exact verdict-to-receipt byte/SHA binding, and the
independent-replay/pointed-row claims.  Thus an authenticated pair is necessary
for the MEMBER path and checker verdict.

The present generic `.github/workflows/gap-run.yml` merely injects the optional
preamble and reads the selected GAP script (lines 214--248); it has no Task193
staging/download step.  A repository scan found Task193-v5 schema-bearing code
but no supplied runtime receipt/verdict data pair, and none of the six v6
runtime outputs currently exists.  Consequently the Task479 report is correct
to keep production dispatch blocked pending broker materialization.

One boundary is worth making explicit: the preserved producer converts a
missing/invalid pair to an accepted `UNKNOWN_INPUT:*` nonpositive envelope.
That can complete the driver after the strict NONE/false assertion, but it
cannot yield MEMBER or run the checker.  Hence v6 COMPLETE certifies completion
of the driver envelope, not existence of Task193 inputs or a positive result;
the broker-side pre-dispatch premise must not be inferred from the sentinel.

The audit used only byte/hash reads, exact in-memory comparison, static scans,
and `python -B` load-without-main with bytecode writing disabled.  It did not
execute v6, production, GHA, GAP, git, a fixture, or any heavy traversal, and
created no runtime output or bytecode cache.

`TASK479_R07_COMPACT_ACTUAL_POSITIVE_OWNER_V6_AUDIT_GO`
