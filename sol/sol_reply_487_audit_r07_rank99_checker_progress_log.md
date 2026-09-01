# Sol reply 487 - rank99 checker progress-log audit

## Verdict

**GO_FOR_CROSS_CHECKED_PREFIX.**

The immutable closed prefix through physical rank 99 may be promoted to
**cross-checked**.  Run `33534267186` contains a successful full semantic
checker replay.  The workflow's red status is solely a post-checker envelope
false-failure: the GAP driver required the whole checker log to equal one PASS
line, while the pinned checker legitimately emitted 44 progress lines before
its unique final PASS.

This promotes only the durable prefix
`rank 51 -> 67 -> 83 -> 99` (eight frozen records plus three closed 16-row
batches).  It does not promote `A0`, `COMMON`, or `NONMEMBER`; the producer
terminal remains `UNKNOWN_RESOURCE:tau_free_candidate:time_limit`.  It is
cross-checked, not Lean-verified.

## Authenticated execution and inputs

GitHub's read-only API binds run `33534267186`, job `99944586953`, and artifact
`9814122823` to head
`e8546334158ef760bf441512d01298aff64076b9`.  The run/job conclusions are
`failure`, but the step ledger has exactly `Run GAP script` failed and the
following `actions/upload-artifact@v4` step succeeded.  Artifact `gap-run-out`
is 76,965 bytes with server digest
`sha256:81b2abef397cd3effa5d67d62fa9b5725ea77ead376532a7976aad8f0fb91083`.
An independent bounded `gh run download` of that exact run/name reproduced the
files audited below.

The specified head's GitHub contents API gives the exact live pins used by the
job:

| object | bytes | SHA-256 |
|---|---:|---|
| v4 GAP driver | 8,217 | `cacd34a634a647ca0c7ea4a2a08cb548c49d72a2830d535d270b670012e2aaa7` |
| recovered-v2 checker | 14,442 | `1d1080cd3e130d987316feefd820215f495cd632aa5eca764fd2f8997f0c424` |

The driver authenticates the checker before invocation.  Its release pin also
reproduced independently: asset
`artifact_9808605601_gap-run-out.rank99.zip` is 27,959 bytes and SHA-256
`d707cf2553fae24863362d581ba4c09709c629a977ff772d95877dd18fdd5f48`;
the release API digest, a fresh direct download, and the copy retained in
artifact `9814122823` all agree byte-for-byte.  The source production binding
also agrees with the API: run `33512607989`, artifact `9808605601`, head
`3316809e483223ec571ca7d6976dc1317c892441`, original artifact digest
`sha256:fb6b6b776b8b288952196f400a0d32d57fd2a5ddb9780a7718e55cffee8bafe1`.

All six extracted release members reproduce the v4 manifest:

| member | bytes | SHA-256 |
|---|---:|---|
| result JSON | 173,930 | `5079ddfbffbfc00cac6b2672cbef80f7eb2cce069a2dba87aa04e7cbc420c29a` |
| historical checker log | 5,595 | `83378497196b198ef257c4918eedf103baa3532ec71675f2a15d4a5a65db3e91` |
| durable checkpoint | 173,082 | `bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358` |
| producer log | 3,898 | `ef366c147651cf011c16e676878a267dd5d85494d949ff02228f43c6004307af` |
| historical `driver.g` | 125 | `28802be0e11aad96494eaa266baed0c5b7aa9d85add29bf04a7d7d6db67f67c8` |
| historical `run.log` | 9,493 | `075f3db302e3f7ee98d826cbe8b67fcbcf9355472b18322ccb29fb78a510af2a` |

The copied checker-visible JSON and checkpoint have the same hashes.  The
checkpoint is closed (`open_batch=false`), has rank 99, accepted count 56,
batch count 3, round 12, and inner state seal
`f2de40c3b16053464b8cf7d397f8fd05ca4439a46ca7e45df93e60bbc11a312d`.
Its three batches are respectively `51 -> 67`, `67 -> 83`, and `83 -> 99`,
each closed with exactly 16 rows.

## Full checker-log audit

The retained checker log is 3,387 bytes, SHA-256
`0acc9a7567ea2d243d722d592b1a2fcac8b89355963f4c64861747c81e2b6776`,
with exactly 45 LF-terminated lines and no CR bytes.

- Lines 1--11 are `selective_Q0` progress at states 131,072 through
  1,441,792.
- Lines 12--44 are the same eleven progress points for each of
  `selective_membership_S0`, `S1`, and `S2`.
- Line 45 is exactly
  `R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_RECOVERED_V2_CHECKER_PASS`.

The final marker occurs exactly once.  Case-insensitive scans found no
`Traceback`, `error`, `exception`, `failed`, `failure`, `STOP`, `UNKNOWN`, or
`reject` in the complete log.

The progress is expected, not stray diagnostic output.  The exact pinned
dependency `search/d972_r07_a0_actual_b72_first_active_v1.py` is 24,643 bytes,
SHA-256
`5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc`.
Its selective runtime prints at every nonzero multiple of 131,072 in Q0 and
each of S0--S2, and asserts a Q0 state count of 1,469,664.  Hence it emits
exactly 11 lines in each of four phases, matching all 44 observed prefix
lines.  The recovered checker calls this runtime once and caches it.

## Why PASS proves the full semantic replay

In the exact recovered-v2 checker, the only production PASS print is in
`main`, after `check(cert)` returns.  There is no early or exception-path PASS.
Before returning, `check`:

1. authenticates schema/status/claims, the frozen eight-record prefix, flat
   accepted-source equality, outer and inner checkpoint seals, and exact
   result-to-checkpoint equality;
2. reconstructs the pinned physical base and calls `replay`;
3. replays all eight frozen correction records to rank 51, checking formula
   branch, selector, exact exponent, direct row digest, dual pairing, pivot,
   rank rise, and post-state at every record;
4. replays every row of all three closed batches, checking cursor order,
   independently reconstructed correction/action rows, anchor scalar, pivot
   and rank rise, and each batch's post-remainder/post-dual state;
5. requires final physical rank 99 and then independently checks both retained
   RESOURCE profiles and the closed-boundary flag.

Thus the observed final PASS can only occur after the complete semantic replay
of the immutable rank99 prefix.  The progress lines occur during that replay;
they do not bypass or weaken any gate.

## Envelope failure is not a semantic failure

The v4 driver redirects the checker's complete stdout/stderr to the retained
log under `set -euo pipefail`; after the checker command it authenticates all
six historical members.  Only then it reads the log and requires

```text
D475Raw == PASS + "\n"
```

The expected one-line value is 60 bytes, whereas the valid progress-bearing
log is 3,387 bytes.  The comparison must therefore fail despite the unique
terminal PASS.  The authenticated job log ends the GAP step with exactly
`Error, task475 checker exact PASS` followed by exit code 1; no earlier failure
is reported.  The receipt/final-driver marker was consequently not written,
but the checker had already completed successfully and its log and all inputs
were uploaded.

A rerun solely to force a one-line log is not a prerequisite for this narrow
cross-checked promotion.  A future driver may repair the envelope by accepting
the expected progress transcript plus one exact final marker, but that green
wrapper is operational bookkeeping, not missing semantic evidence.

**GO_FOR_CROSS_CHECKED_PREFIX**
