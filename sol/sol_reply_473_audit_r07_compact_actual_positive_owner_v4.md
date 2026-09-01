# Task473 adversarial audit — compact actual positive owner v4

## Verdict

**STOP / NOT DISPATCHABLE / DO NOT ADOPT v4.**

The requested three ABI repairs are correct, and the inherited mathematical
path passes the permitted bounded audit.  Nevertheless the v4 driver has one
new deterministic preflight blocker: it pins the named v3 predecessor with
the byte/hash tuple of an unrelated Task471 driver.  The generated shell
therefore exits before starting the producer.

No production result, MEMBER, lift, fake, Ihara assertion, or negative result
is established here.  `verified=false`.

## F1 — fatal inherited-driver pin contamination

The v4 driver names

```text
search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g
```

but lines 9--10 advertise

```text
6920
05c438d045431948f4a487e0e264ed15e628cc7f22bc0cccf89fd9661b84431d
```

The named file is actually

```text
4233
b1851ea2835ef752b64b8f04c6489bd9f9630178fadbe8acf38c7fb0aeb2a5d7
```

The advertised tuple is exactly the physical tuple of the unrelated
`search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v3.g`
from Task471.  This is not a harmless provenance typo.  The generated shell
uses `set -euo pipefail`, and its first command after that header is the
line-28 byte-count test against `6920`.  That test is deterministically false;
the SHA test and both Python processes are unreachable.

Reproduction:

```powershell
$p='search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g'
(Get-Item -LiteralPath $p).Length
(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()

$q='search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v3.g'
(Get-Item -LiteralPath $q).Length
(Get-FileHash -LiteralPath $q -Algorithm SHA256).Hash.ToLowerInvariant()
```

Thus Luna's reported driver pin gate did not cover the complete inherited
driver tuple.

## Passed findings

### F2 — the actual Task456/Task411 path is retained

Load-without-main expanded the pinned bodies to

```text
producer 61376 d9a5a136d875d2fb7f5d596966abf094b7c555a0e4eb4ac6576c72071f734b84
checker  47875 c65f4e7a122f835f5c50b03d6c189ff26a319518ac8b525d6f3d0943b8412ed0
```

The generated producer v3-to-v4 diff consists only of the compact schema and
producer-line version changes.  The checker diff consists only of the compact
schema/checker-line changes, the scoped two schema repairs, and the complete
producer-pin tuple repair.  Consequently the Task462/Task464 actual arithmetic
is unchanged.

In particular, bounded inspection and replay found all of the load-bearing
v420 path:

- the full Task198 `AuthorityAdapter` is constructed first; `Runtime` and
  `BoundaryLedger` receive that original authority; only `DirectEngine`
  receives `CompactAuthorityProxy`;
- producer-side Task411 reconstruction and checker-side independent Task411
  reconstruction each return 44 immutable rows, in identical order, with
  digest
  `7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8`;
- the proxy delegates owner/receipt/meter data, while attribute replacement,
  row replacement, mapping mutation, and word-tuple mutation are rejected;
- the actual eleven-occurrence package, pointed Task193 target, four actions
  `(1,-1,2,-2)`, translated PB oracle, proof DAG, positive raw-joint replay,
  and literal `M = sum a_gj ((w r_j)-w)` construction remain present;
- no synthetic `sparse_column`, external target argument, assumed-empty PB
  ledger, checkpoint/resume route, SELFTEST, or FIXTURE execution path was
  introduced.

The checker loads the pinned independent Task198-v14 checker arithmetic and
the independent Task411 checker reconstruction.  It does not import or call
producer presentation/action/target/replay helpers; the producer source is
read only for an exact pin.  An in-memory self-sealed receipt mutation was
rejected, as was direct entry of a NONMEMBER result into `check_member`.

### F3 — all three commissioned ABI repairs pass

1. Producer and checker both define
   `MEMBER = R07_ZERO_BASE_A5_A6_MEMBER`; the driver accepts that exact value
   and invokes the checker only on that value.
2. The checker pin equals the complete physical producer tuple:

   ```text
   search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py
   1876
   0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9
   ```

3. Full-line transforms give the compact checker
   `...positive-owner/v4/checker-verdict/v4`, while producer and checker both
   require the frozen Task193 ABI
   `d972-r07-second-frattini-affine-prefix-compiler/v5/checker-verdict/v5`.
   Their Task193 schema, terminal, and all three source pins are identical and
   match the physical files.

### F4 — terminal, argument, and cost contracts pass apart from F1

Producer and checker parsers accept exactly the driver-supplied production
arguments and frozen `14400` second / `5700000000` byte caps.  Output paths
are under `ci/out`; terminal extraction uses the v4 producer marker; there is
one producer invocation and one MEMBER-only checker invocation.  Every
accepted nonpositive terminal is quarantined as UNKNOWN and the driver checks
the complete `resumable=false` plus six-field NONE/false frontier.

Loading the guarded wrapper ancestry compiles definitions but does not invoke
any ancestor main or self-test.  The producer performs one Task411 roster
construction and the intended full-authority setup, then only the 44-row
DirectEngine traversal.  The checker is run only after MEMBER and performs
one independent reconstruction/replay.  No additional material production
cost was found.

The bounded audit used `python -B` throughout, performed no production or
full-authority run, and created no bytecode cache.  It compiled/loaded both
bodies, checked every physical/generated pin, compared the independent 44-row
rosters and digest, exercised the read-only proxies and tamper rejection, and
parsed both CLI contracts.  All intended gates passed except the inherited
driver tuple above.

## Minimal repair only

Do not change producer, checker, mathematics, caps, terminal policy, or
frontiers.  In a versioned successor, repair only the complete inherited
driver tuple to

```text
path   search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g
bytes  4233
sha256 b1851ea2835ef752b64b8f04c6489bd9f9630178fadbe8acf38c7fb0aeb2a5d7
```

Then regenerate the successor's own physical pin and add an executed bounded
gate comparing all three tuple fields with the named file.  Rerun the existing
load/ABI/44-row/proxy/driver static gates.  Until that succeeds, no dispatch
contract is issued.

`TASK473_R07_COMPACT_ACTUAL_POSITIVE_OWNER_V4_AUDIT_STOP`
