# Task386 - independent A4/v9 trace/driver code-performance reaudit v1

## 0. Decisive result

The frozen tranche is **STATIC REJECT**.  The producer/checker repair itself
passes: both reverse exactly to their frozen bases, row 4 has the required two
role-specific containment entries, and the other six first-rejection traces
remain exact.  The two candidate commands are also fixed, serial, separated,
and independent.

The v9 driver nevertheless cannot be authorized.  The complete static audit
found five load-bearing defect groups:

1. the driver never binds or revalidates the six task198 source-pin owners;
2. both candidates report a missing row-4 path as
   `symlink_or_reparse=true`, and the driver requires that untruthful value;
3. result normalization is broader than the registered role fields and the
   resource snapshot admits arbitrary payload-owner maps;
4. the stated 87,048,578-byte maximum omits a third full result-sized byte
   buffer and a simultaneous normalized DOM copy; and
5. rollback is unbounded after the global timer is cancelled, while close
   errors after terminal success are swallowed and one fallible timer call
   remains after the success object is emitted.

These are independent of the repaired row-4 predicate.  Execution must not be
commissioned piecemeal against this owner set.

This audit was source-static.  I used only read-only PowerShell text/byte
inspection, in-memory comparison, and SHA-256 hashing.  I did not run Python,
Node, GAP, either candidate, the driver, mutations, GHA/workflows, git,
network, syntax/import compilation, subprocess tests, or RSS measurement.

For references below, `P`, `C`, and `D` mean the frozen v7 producer, v6
checker, and v9 driver respectively.

## 1. Frozen physical identities and lineage

All five commissioned subject identities match exactly and are regular,
non-reparse physical files in the inspected workspace:

| owner | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v7.py` | 102,958 | 969 | `4f7f57150892e354f3398c33e0f72c0d968c7101de05b7ce7e5690b47fcd064c` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v6.py` | 100,648 | 761 | `7cf5468be847c3a49014986e39af9bb71120af6371aec05e23bb9789bb22c6c1` |
| `search/d972_r07_a4_actual_owner_trace_gha_driver_v9.g` | 72,604 | 1,202 | `130a6e838f648d58a81854eb74dc8476aa4f1d70dc4d6bfc0a5a81a3e3e68155` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json` | 8,489 | 1 | `474d8e19ca49cad06b560cf0ac1d5eeeac1927fe2666224cb9501e77b5cc8481` |
| `sol/sol_reply_383_r07_a4_v9_trace_repair_and_pinned_driver.md` | 14,439 | 267 | `aa6d92ca6292b9b425ea69bbc21c81b2b089ad4ccdfe46e6074ac8fce0c2ccf0` |

The v6/v5 comparison bases also match their frozen pins:

| base owner | bytes | SHA-256 |
|---|---:|---|
| producer v6 | 102,151 | `6bbae63e284e055bba2097696f0202645bc38ec9856815af9c1857ecd2131a58` |
| checker v5 | 99,782 | `33b7905fb1f00b23b8e30c8b90b57a793cabf62ed272fb258790d3c88ba34165` |

I read the complete task/reply lineage requested by task386.  The phrase
`task365/reply367` has no literal task365 file in `sol/`; the extant paired
owner is `sol_task_367_r07_a4_v6d_complete_finite_repair.txt`, and reply367
itself identifies Task367.  I used that physical task367/reply367 pair and did
not treat the commission's numbering typo as a source-owner substitution.

## 2. Fixture and task198 authority bodies

Independent byte-level removal of exactly one root seal member gives:

| authority | payload bytes | body bytes | recomputed body SHA-256 |
|---|---:|---:|---|
| fixture v5 (one final LF excluded) | 8,488 | 8,400 | `c674491a2f50b200a70349780f0e7a80c21cc0fc3cecd44432dc6e70c51f63fb` |
| task198 manifest | 2,722 | 2,625 | `0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684` |
| task198 receipt | 31,017,244 | 31,017,156 | `c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f` |

Each root marker occurs exactly once and all three payloads are ASCII.  The
eight directly pinned task198 physical owners all match:

| owner class | bytes | SHA-256 |
|---|---:|---|
| receipt | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| acceptance manifest | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| task198 producer source | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| task198 checker source | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| task198 GAP driver | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |

The manifest names the three task198 program sources and the three small
attestation/verdict owners.  The receipt refers to the task198 producer module
but contains no v5 fixture, v7/v6 candidate, v9 result, task383, or reply383
back-edge.  The three task198 program owners likewise contain no A4/v9
back-edge.  Thus the frozen content graph itself is acyclic.  The rejection
below is that the v9 driver does not completely bind that graph at runtime.

## 3. Exact bounded reverse delta

The producer reverse operation restored P:2 and P:29, replaced P:862--870 by
the single frozen v6 trace-condition line, and made no other change.  The
in-memory result is exactly 102,151 bytes with SHA-256
`6bbae63e284e055bba2097696f0202645bc38ec9856815af9c1857ecd2131a58`
and is case-sensitive byte-for-byte equal to frozen v6.

The checker reverse operation restored C:2 and C:27, removed the explicit
frozen-fixture schema constant at C:28, restored the former fixture expression
at current C:508, and replaced C:665--673 by the single frozen v5 trace line.
The result is exactly 99,782 bytes with SHA-256
`33b7905fb1f00b23b8e30c8b90b57a793cabf62ed272fb258790d3c88ba34165`
and is byte-for-byte equal to frozen v5.

Consequently the only forward deltas are truthful source/result labels, the
checker fixture-schema decoupling needed to leave the fixture at v5, and one
role-aware trace predicate per program.  There is no hidden mutation,
authority, exception, publisher, or conclusion delta.

## 4. Row-4 and other-six rejection traces

The repaired trace logic passes independently on both sides.

- Producer admission is P:454--467 and both ordinary calls are P:668.  Row 4
  creates only the missing outside receipt path at P:745--749 and reaches the
  ordinary route at P:857.  P:862--866 requires exactly
  `[(transport,manifest.path),(transport,receipt.path)]` and makes the final
  entered event the registered receipt-path rejection.
- Checker admission is C:319--327, its two ordinary calls are C:499, its row-4
  constructor is C:558--562, and its independent route is C:660.  C:665--669
  applies the same ordered requirement to the checker-owned journal.
- P:867--870 and C:670--673 retain exact-once rejection-validator occurrence
  and final validator/stage for the other six.  The source event calls fix the
  final owners; D:628--693 reconstructs every complete event list, D:848--852
  requires its exact validator list and SHA-256 digest, and D:853--859 checks
  the row-4 and other-six terminal shapes.  Fixture owner, reason, allowed
  reseals, terminal count, disposal, and before/after revalidation are checked
  at D:843--866.

The exact terminal owners for rows 1--3 and 5--7 are respectively
`receipt.Delta0.presentation.rows`, `manifest.accepted`,
`manifest.receipt.{bytes,sha256}`,
`receipt.Delta0.presentation.normal_generation_proof`,
`receipt.bridge.occurrence_ledger`, and `receipt.evaluator`; the driver binds
them through the expected event digests.  Producer and checker construct and
digest their own event lists and neither consumes the other's runtime output.

The Task379 non-trace source is byte-for-byte retained.  Its aggregate status
is nevertheless rejected by this stricter audit because the inherited
physical projection misstates the row-4 missing owner, as detailed next.

## 5. Authority/path defects

### F1. Six task198 source owners are unbound after candidate exit

P:95--101 and C:66--68 name the six source-pin owners, and each candidate
authenticates them internally.  D:620--627, however, uses their sizes and
digests only as expected transcript literals.  The driver's `BoundOwner` set
at D:973--998 contains only producer v7, checker v6, fixture, driver, receipt,
and manifest.  It never opens the two attestations, verdict, or three task198
program owners, never includes their device/inode identities in the physical
duplicate test, and never revalidates them at D:1008--1009, D:1011--1012,
D:1023--1024, D:1026--1027, D:1040--1041, or D:1124--1125.

Therefore a source pin can change after the checker has produced its claimed
transcript and before sentinel publication without any retained driver fd
detecting it.  A physical alias among those six and the bound graph is also
outside D:998.  The sentinel's task198 section at D:1062--1065 records only
receipt and manifest, so it cannot close this gap.  This violates the required
complete physical graph and before/after revalidation.

The two output directories are separately bound at D:965--966, but their
physical identities are never compared with each other.  A bind-mount alias
between `ci/out` and `search/certs` is consequently not rejected either.

### F2. Missing is asserted to be a symlink/reparse owner

For row 4, `_path_identity`/`path_identity` correctly constructs
`type="missing"` at P:353--358 and C:231--235.  The subsequent projections at
P:843--845 and C:652--654 set

```text
symlink_or_reparse = identity.type != "regular"
```

so the missing path is emitted as `symlink_or_reparse=true`, while the same
record says `logical_link_target="none"`.  D:775--782 explicitly requires the
false `true` value for the after phase.  The result projection omits the
underlying `exists` and `type` fields, so it supplies no truthful positive
`missing` discriminator.  Unreadability is correct, but unreadable/missing is
not a symlink or reparse point.  This fails task386's truthful missing-path
requirement and makes the physical-owner evidence nonaccepting.

## 6. Independent subprocess and framing boundary

This group passes.  D:75--78 fixes the exact argv and quoted command text.
There is exactly one producer call at D:1010 and, after producer DOM release
at D:1019--1022, exactly one checker call at D:1025.  The checker argv contains
only its own program and the frozen fixture; no producer result or projection
is passed to it.

D:550--608 keeps stdout and stderr on separate bounded pipes, enforces
35,000,000 and 1,000,000-byte caps while streaming, and requires exact integer
status zero.  D:518--548 accepts either exactly one final LF or the source
programs' zero-LF framing and appends the sole LF; it rejects BOM, CR, partial,
extra-line, and over-bound output.  Later JSON parsing and exact canonical
comparison prevent a framed non-document from being admitted.

## 7. Canonical admission and overbroad normalization

The basic byte and seal route is sound: D:916--934 re-reads the physical raw
owner, requires compact ASCII canonical JSON plus one LF, removes only the
root `self_digest_sha256`, and recomputes the body seal.  D:822--869 checks the
v7/v6 schemas, scope, baseline, seven rows, event commitments, identities,
reseals, disposal, revalidations, and public resource formulas.

The overall group is still rejected for F2 and an additional admission gap.
D:763--765 permits any `payload_owners` mapping with string keys, nonnegative
integer values, and the right sum; it does not require the exact nine retained
authority owners and their individual sizes.  Then D:871--890 recursively
normalizes every string value **and every dictionary key** beginning with the
role prefix.  Thus role-prefixed differences inside the underconstrained
payload-owner map, or another underconstrained nested string, can be erased
even though only registered validator/reason names and the admitted schema
version are allowed to differ.  Equality at D:1030 is bytewise and symmetric,
but it is equality of this over-normalized projection, not a semantically
restricted complete projection.

## 8. Static caps and performance defects

The candidate-side arithmetic itself recomputes correctly.  With
`S=315,289`, `F=8,489`, `R=31,017,244`, and `M=2,722`:

```text
authority payload A                         = 31,343,744
opened bytes                                = 186,443,583
temporary bytes                             = 155,099,839
parsed input bytes                          = 279,185,470
fourteen retained-fd revalidation bytes     = 438,812,416
modeled payload-token peak                  = 63,409,572
```

The outputs expressly say that the token ledger omits Python DOM/container,
allocator, bytearray slack, and RSS.  Parent RLIMIT_AS is installed/read back
at D:944--960 before authority material, the candidates are serial, each child
gets CPU 3600/3610 at D:497--500 and installs its own 700,000,000-byte soft
RLIMIT_AS, and external wall 3900 exceeds the hard CPU limit by 290 seconds.
The numerical formula `2*(3900+2*30)+260=8180 < 9000` is arithmetically true.

The driver-level maximum is not true:

- D:1089--1092 claims
  `max(2*R+CHUNK+F+M,2*RESULT_FILE_MAX+2*PROJECTION_MAX+CHUNK)` =
  87,048,578 explicit bytes.
- During result admission D:917 retains `raw` of up to 35,000,001 bytes;
  D:919 creates the 35,000,000-byte LF-stripped `payload`; and D:925 creates a
  second 35,000,000-byte canonical encoding before any of them is deleted at
  D:929.  That is 105,000,001 simultaneous byte-buffer bytes before the parsed
  DOM or decoded ASCII string.  During checker admission, the retained
  producer projection can add 8,000,000, giving 113,000,001 bytes.  Both
  exceed the declared 87,048,578.
- `PROJECTION_MAX` is checked only after `canonical(projected)` has already
  allocated the complete projection at D:910--911.
- D:878--890 recursively constructs a second full dict/list container tree
  while the parsed result DOM remains live.  The sentinel statement "one
  parsed DOM only" therefore omits a simultaneous full normalized DOM copy.
- Each result is fully serialized for canonical comparison at D:925, again
  for its body seal at D:932, and again for normalized projection at D:910.
  The 31-MB task198 receipt likewise receives a full canonical encoding and a
  second body encoding in D:312--332 after its physical hash.  These are
  material duplicate full-document passes rather than a bounded fused route.
- Both GAP D:38--47 and Python D:242--246 materialize/scan complete output
  directory name sets.  `os.listdir` has no entry/count bound, and the GAP
  scan occurs before the harness RLIMIT and global timer.  The second bound-fd
  scan is necessary; the first full duplicate scan is not a performance-safe
  substitute for it.

Finally, the advertised cleanup margin is not enforced.  On any harness
exception D:1146--1147 cancels the global timer **before** process stopping
and `TX.rollback`; rollback D:440--486 contains no deadline checks or separate
timer.  Consequently unlink/fsync/close cleanup can exceed both the reserved
260 seconds and the 9000-second global wall.  Repeated stop attempts after a
second 30-second wait failure are likewise not covered by the stated formula.

These are static buffer/control-flow facts, not observed RSS claims.

## 9. Durable publication audit

Most of the publication primitive is correctly constructed.  D:361--382
pre-registers same-directory exclusive temps; D:383--430 performs complete
writes, file fsync, no-replace hard link, transient two-link audit, temp
unlink, directory fsync, single-link audit, retained-fd hash, and stable
directory check.  D:431--439 revalidates visible owners.  D:440--486 rolls
back only matching retained device/inode owners, attempts directory fsync
after each final/temp removal, and reports rollback errors.  Raw results,
logs, admitted copies, and sentinel all use this route.  GAP uses `Process`
and checks its status at D:1197--1202.

The durable group nevertheless fails for three exact control-flow reasons:

1. As above, the timer is cancelled before rollback, so cleanup is not bounded
   by the declared global/deadline contract.
2. After `TX.close_success` and terminal emission at D:1142--1144, D:1145
   still calls fallible `signal.setitimer`.  A failure can occur after a
   complete accepting terminal object has already been written.
3. On the success path, retained authority fds, their parent fds, both bound
   directory fds, and `ROOT_FD` are closed only in D:1168--1182.  Every close
   error there is swallowed after `success=True`; it neither rolls back nor
   changes the Python/GAP status.  This directly contradicts the requirement
   that a close error remain nonaccepting.

Together with the unbound source pins, these defects prevent a durable
fail-closed authorization even though the link/fsync/rollback primitive itself
is otherwise well designed.

## 10. Scope

Nothing here covers rows 8--48 or changes the A4 numerator.  No runtime fact,
full selftest, basis, lift, fake, or Ihara witness was produced.  A successor
must repair all defect groups above in new versioned owners and receive a new
independent static audit before any rows-1--7 GHA execution.

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
V6/V5 BOUNDED REVERSE DELTA:           PASS
ROW4 TWO-ADMISSION TRACE:              PASS
OTHER SIX REJECTION TRACES:            PASS
TASK379 NON-TRACE CLAUSES:              REJECT
AUTHORITY / PATH GRAPH:                REJECT
INDEPENDENT PRODUCER/CHECKER:           PASS
CANONICAL RESULT / SELF-SEAL:           REJECT
STATIC CAPS / PERFORMANCE:             REJECT
DURABLE FAIL-CLOSED DRIVER:             REJECT
ROWS1-7 A4/V9 GHA:                      FORBIDDEN
FULL 48x2 A4:                           remains INCOMPLETE
ACTUAL A4 NUMERATOR:                    remains 1/3
LIFT / FAKE / IHARA:                    NONE

TASK386_R07_A4_V9_CODE_PERFORMANCE_REAUDIT_V1
