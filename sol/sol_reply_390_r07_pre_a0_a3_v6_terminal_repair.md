# Task390 bounded static implementation -- pre-A0 A3/v6 terminal repair

## 1. Decision and immutable identities

The bounded driver-only repair is **COMPLETE**.  I created the new v6 driver
and did not edit or duplicate either frozen v5 Python owner, P0, or any
authority.  No candidate, interpreter, compiler, import, GAP process,
workflow, mutation, RSS measurement, git command, or network operation was
run.  All checks reported here were read-only PowerShell text inspection and
SHA-256 hashing.

| owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v6.g` | 19,507 | `f1f716dc8bf27a8d66eba3477a52baf9f8619a04763dff15c3a814498ba12a9a` |
| frozen `search/d972_r07_pre_a0_single_target_a3_v5.py` | 104,446 | `4fbbd5792a1d1cc7bb1c3d534bdc0966291751cc9d3cea99d1ed20ca7d70fecb` |
| frozen `crosscheck/check_d972_r07_pre_a0_single_target_a3_v5.py` | 116,872 | `90838f12061783c77651c656f7bd1a572ca4a687339b5b70747342d18d32028a` |
| frozen `search/d972_r07_pre_a0_single_target_a3_gha_driver_v5.g` | 18,597 | `0465b46a734048b4ef6c16ed079e7daf825f71407f8cfe1b969a648ffb936d27` |
| unchanged P0 | 16,417 | `14ea6de8efac73e71854f6566a9202eb89164ab6b7b5940954e87b3af21ee8ae` |

P0 retains self seal
`f1991fa0c232e1d7ea95a211498b4d1741c2104b22271fb90ec1a7ee3af98be7`.
Its recursive inventory still has exactly 23 distinct owners totalling
33,121,619 bytes.  I streamed and rehashed every one of those physical owners;
all 23 declared byte counts and SHA-256 pins matched.

The new driver is ASCII, LF-only, has 254 physical lines and a final LF.  The
sentinel token at line 184 is byte-for-byte the frozen token
`D363_V5_ACCEPTED`.  A direct ASCII count is 16 octets; therefore the
commission's phrase "15-byte content" is an off-by-one prose count.  No
unspecified 15-byte substitute was invented, and the actual frozen content was
not changed.

## 2. Sole repaired edge

The existing final Python helper remains the one and only sentinel helper at
driver lines 170--249.  The repair is confined to that helper and the terminal
GAP suffix.

- Lines 182--184 preserve dirfd-relative `O_EXCL|O_NOFOLLOW` creation and the
  exact frozen content.  Lines 185--189 preserve the bounded complete-write
  loop and file `fsync`.
- Lines 190--191 capture the creation fd identity and require a regular file
  of the exact content size.  Line 192 makes the writer close a prerequisite;
  line 193 preserves the output-directory `fsync`.
- Lines 194--196 reopen the fixed basename read-only with `O_NOFOLLOW` under
  the already-bound `ci/out` dirfd, require a regular file, use
  `os.path.samestat` to equate its device/inode with the creation fd, and
  require the same exact size.
- Lines 197--198 perform only two fixed-size reads: the exact token length and
  one EOF canary byte.  Any short read, wrong byte, or non-EOF byte raises the
  admission error.  Line 199 makes read-fd close a success prerequisite.
- Lines 200--224 retain publication/admission and all file/read/root/ci close
  failures, then, once `created=True`, attempt the existing dirfd-relative
  unlink and output-directory `fsync`.  Lines 225--239 preserve the special
  output-dir-close failure route: record the primary close failure, attempt
  unlink plus directory `fsync` if rollback has not yet run, retain every
  cleanup error, and reclose.
- Lines 240--247 retain separate `ORIGINAL` and `ROLLBACK` rows.  Diagnostic
  emission is itself guarded; an output exception is retained as
  `diagnostic-output`, and every such failure still terminates with helper
  status 70 after the rollback route.  The shell maps any helper nonzero to its
  existing nonaccepting `fail sentinel-publication` status at line 249.

Thus the helper can return zero only after exclusive creation, exact complete
write, file fsync, writer close, directory fsync, same-object no-follow
readback, exact content plus EOF, read-fd close, root/ci closes and output-dir
close have all succeeded.  Every recorded failure after creation reaches the
same unlink-plus-directory-fsync rollback; primary errors are never overwritten
by cleanup errors.

## 3. Complete forward and reverse delta

The exact minimal physical-line comparison is:

| direction | bytes | lines | LCS | deleted | inserted | net |
|---|---:|---:|---:|---:|---:|---:|
| v5 -> v6 | 18,597 -> 19,507 | 245 -> 254 | 231 | 14 | 23 | +910 bytes, +9 lines |
| v6 -> v5 | 19,507 -> 18,597 | 254 -> 245 | 231 | 23 | 14 | -910 bytes, -9 lines |

Driver lines 1--169 are byte-identical.  The complete edit inventory inside
the single logical suffix hunk (old lines 170--245, new lines 170--254) is:

| frozen v5 line(s) | v6 line(s) | exact line operation |
|---:|---:|---|
| 171 | 171 | replace `import os,sys` by `import os,stat,sys` |
| 173 | 173 | replace fd initializer by the same initializer plus `rfd=-1` |
| after 189 | 190--191 | insert creation-fd `fstat`, regular-file and exact-size admission |
| after 191 | 194--199 | insert no-follow read fd, `fstat`/`samestat`/size gate, exact read plus EOF, required close |
| 193 | 201 | replace phase `publication` by `publication-or-admission` |
| before 194 | 202--205 | insert retained read-fd cleanup-close route |
| 229--231 | 241--246 | replace the three unguarded diagnostic lines by the same nested emission plus guarded `diagnostic-output` retention |
| 238--245 | 253--254 | replace two status checks, GAP `StringFile`, sentinel comparison and success `Print` by one integer-zero assertion |

Those rows account for all 14 deletions and all 23 insertions; every other
physical line is equal modulo the listed shifts.  As a separate in-memory
reverse check, I retained the exact new prefix through line 169 and reversed
only the one logical suffix hunk.  The reconstruction was byte-for-byte equal
to frozen v5: 18,597 bytes and SHA-256
`0465b46a734048b4ef6c16ed079e7daf825f71407f8cfe1b969a648ffb936d27`.
The old/new hunk sizes were respectively 4,879 and 5,789 ASCII bytes.

## 4. Exhaustive post-Process operation inventory

`CloseStream(D363Stream)` is at line 250, before `Process`; hence the generated
script owner is resolved and closed before launch.  The status-bearing exact
`/usr/bin/bash` call occupies lines 251--252.  The complete remainder of the
file is only:

```gap
if not (IsInt(D363Status) and D363Status=0) then
  Error("task384: shell process status is not integer zero"); fi;
```

Accordingly, after `Process` there is exactly one in-memory integer-zero
predicate and its rejection branch.  Static searches of that suffix found no
`StringFile`, `Print`/`PrintTo`, `CloseStream`, timer, filesystem cleanup,
rehash, revalidation, second `Process`, or `Exec`.  There is no successful-path
operation after the predicate: EOF follows line 254.  A noninteger, signalled,
or nonzero status cannot reach acceptance, while stale sentinel names remain
rejected before creation at unchanged lines 57--61.

## 5. Task388 PASS preservation and bounded cost

The frozen v5 producer/checker identities, P0 and all 23 authorities are exact,
so their live evaluator, v303 projection, one closure, one independent
verifier, 486/729 rosters, baseline plus twelve ordinary mutations,
authenticated receipt-digest transport, resource meters and deadlines are not
semantically changed.  Driver lines 1--169 are exact v5 bytes; this preserves
the exact-bash pin and capability gate, producer/checker status grammar,
receipt/verdict transport, single consolidated receipt parse/canonical/seal
pass, 23-owner authentication, final physical rehashes and all existing caps.

The sentinel edit adds no helper, subprocess, source pass, receipt parse,
canonicalization, hash, collection, scan, candidate call, or mutation.  Static
counts remain four generated `python3 -` commands and one GAP `Process`.  The
only new successful-path work is two `fstat` calls, one fixed-name no-follow
open, two reads bounded by 16+1 bytes, and the required read-fd close.  On the
failure path it adds only the corresponding bounded close/diagnostic retention.
There is no data-dependent loop or material allocation beyond the frozen token.

The task388-only defect is consequently removed without reopening any task388
PASS group.  This is a static implementation/self-audit result, not the fresh
independent audit required by the commission, and it does not authorize GHA.

A3/V6 VERSIONED DRIVER:                  COMPLETE
V5 PRODUCER/CHECKER:                     RETAINED
TASK388 PASS GROUPS:                     RETAINED
SENTINEL READBACK INSIDE HELPER:         REPAIRED
POST-PROCESS FALLIBLE SUCCESS EDGE:      REMOVED
DURABLE POST-CREATE ROLLBACK:            REPAIRED
AVOIDABLE DUPLICATE WORK:                NONE
CANDIDATE EXECUTION:                     UNEXECUTED
FRESH INDEPENDENT STATIC AUDIT:          REQUIRED
PRE-A0 A3/V6 GHA:                        FORBIDDEN
ACTUAL A3 NUMERATOR:                     remains 0/3
A0 / COFINAL LIFT / FAKE / IHARA:        NONE

TASK390_R07_PRE_A0_A3_V6_TERMINAL_REPAIR
