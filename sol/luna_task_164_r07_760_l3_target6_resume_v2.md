# Luna task 164: g760 L3 target6 checkpoint/resume v2

Date: 2026-08-26  
Role: Luna / implementation and bounded mechanical audit only

## 1. Fixed purpose

Run `32901384400` reached `j=9:D2-relator-7` after exhausting the v1
10,200-second producer budget.  It returned `UNKNOWN_RESOURCE`, not a
mathematical terminal.  The v1 first-terminal control flow implies only a
producer-side candidate prefix with no `NONMEMBER` at `j=2,...,8`.

Build a versioned resume lane which starts by recomputing **all of j=9 from
relator 1**, writes an immutable checkpoint after every completed j, and never
pretends that the lost in-memory relator-1-through-6 state was serialized.

## 2. Prior artifact pins

Copy the two downloaded run artifacts into new immutable versioned certificate
paths under `search/certs/`, byte-for-byte, and bind them in every v2 output:

```text
run_id = 32901384400
head_sha = c1e7eb8fcd08676d5a6efad82add2c1c832a22c0

prior receipt:
  bytes = 3239
  sha256 = 1c739559eee368ba676c694960be21db94d6bc2292a6136d89b97bedfef3e15b

prior producer log:
  bytes = 164
  sha256 = fc3901c29f958e216e17ba175be4857ee26cc140f3f809f0e29833b636ccd436
```

The source copies are currently in the shared external temporary directory
`%TEMP%/d972_run32901384400_20260826a/`.  Authenticate before copying.  Use
`apply_patch` for repository writes; do not silently normalize line endings.

The v2 parser must validate the v1 canonical self-digest convention and the
exact stop fields:

```text
schema=d972-r07-760-l3-target6/v1
mode=full
terminal_token=R07_760_L3_TARGET6_UNKNOWN_RESOURCE
result.requested_seconds=10200.0
result.stage=j=9:D2-relator-7
result.mathematical_membership_claimed=false
result.mathematical_nonmembership_claimed=false
base_kind=r07_760_commutator
base sha256=518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
```

## 3. Allowed new files

Use new versioned paths only:

1. v2 resume producer;
2. v2 structurally independent resume checker;
3. v2 ASCII-only producer GHA driver;
4. the two prior-artifact certificate copies;
5. a v2 preflight/checkpoint schema certificate if needed;
6. `sol/luna_reply_164_r07_760_l3_target6_resume_v2.md`.

Do not modify v1 producer/checker/drivers, CLAIMS, existing certificates,
proof notes, or the Sol reply.

## 4. Producer contract

- Accept only a fixed inherited candidate prefix `[2,3,4,5,6,7,8]` and
  `start_j=9`; reject arbitrary skip values.
- Rebuild and authenticate the full static g760/PC/Jennings input exactly as
  v1.  No old20/old616 answer or historical blocker may be imported.
- Fresh order is `j=9,10,11,12`, with the same first-nonmember rule.
- Write an immutable checkpoint immediately after each completed j.  It must
  include the full public `compute_j_bfs` row, `completed_j_prefix`, `next_j`,
  prior checkpoint SHA/bytes, static/pin digests, false global claims, and a
  canonical self-digest.
- On a resource stop, preserve every completed checkpoint and emit a
  claim-free stop receipt.  Never infer the unfinished j.
- A later invocation may resume only from the exact next j authenticated by
  the checkpoint chain.  It must replay all checkpoint structural canaries
  before starting.
- Use a configurable bounded cap up to the existing 21,600-second maximum;
  the recommended first GHA cap is 21,000 seconds.  Keep RSS cap 5,600 MiB.
- A producer-only outcome is always `CANDIDATE`, even for NONMEMBER.

Relator-level echelon serialization is optional.  If omitted, an interrupted j
is recomputed from relator 1.  If implemented, use the lossless pivot encoding
and replay gates specified in Luna reply 163 §8.2.

## 5. Independent checker contract

The checker imports neither producer.  It may reuse the independent v1 design
only by a versioned copy.  It authenticates the prior artifacts and every
checkpoint, independently reconstructs each **freshly completed** j row, and
directly enumerates all `59,049 x 11 = 649,539` translated D2 columns for the
tested j.  A NONMEMBER separator must annihilate all legal and translated D2
rows and pair nontrivially with the target.

It need not recompute j=2,...,8 to certify a fresh j>=9 NONMEMBER: agreement at
one j already kills this g760 prefix.  It must not call the inherited prefix
cross-checked.  MEMBER remains inconclusive and is not a lift.

## 6. Driver and venue

The immediate driver is producer-only and ASCII-only.  It runs exactly one
Python process, no checker, with a 21,000-second inner cap and an outer margin.
It validates exclusive terminals, checkpoints, immutable hashes, false global
claims, process count, and `grade=CANDIDATE`.  Provide exact selftest and GHA
invocations.

Do not run local full, parallel Python/GAP, git, or GHA.  Bounded serial
selftests/preflight are allowed.  Parent Sol alone commits, pushes, dispatches,
and records run ids.

## 7. Required report

Report exact paths, bytes, SHA-256, clean-checkout dependency audit, selftest
markers, process counts, checkpoint mutation tests, and the precise boundary:

```text
inherited j2..8 = producer control-flow candidate only
fresh resumed output = candidate until independent checker agrees
MEMBER != actual A18 lift
NONMEMBER kills one g760 prefix only
no fake / no cofinal lift / no Ihara witness declared by the implementation
```
