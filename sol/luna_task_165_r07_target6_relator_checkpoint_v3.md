# Luna task 165: g760 target6 lossless relator checkpoint v3

Date: 2026-08-26
Role: Luna / implementation and bounded mechanical audit only

## 1. Purpose

GHA run `32966890811` is currently recomputing j=9 from D2 relator 1 with
the v2 j-level checkpoint lane at head
`474435d52161eb042f04e15ed93fdb6b906d05d4`.  V2 preserves only a fully
completed j.  If the six-hour job ends inside j=9, all completed relator
closures are lost again.

Build a new versioned producer adapter which writes a lossless checkpoint
after every fully completed D2 relator and can resume at the exact next
relator.  This is resource recovery only.  Do not infer membership or
nonmembership from an unfinished j.

## 2. Inputs and fixed scope

Read and pin in full:

- `search/d972_r07_760_l3_target6_v1.py`;
- `search/d972_r07_760_l3_target6_resume_v2.py`;
- `crosscheck/check_d972_r07_760_l3_target6_resume_v2.py`;
- `search/d972_r07_760_l3_target6_resume_gha_driver_v2.g`;
- the v1 prior-run receipt/log copies and v2 preflight certificate;
- `sol/luna_task_164_r07_760_l3_target6_resume_v2.md`;
- `sol/luna_reply_164_r07_760_l3_target6_resume_v2.md`;
- this task.

Keep the inherited prefix `[2,3,4,5,6,7,8]`, fresh j order
`[9,10,11,12]`, first-NONMEMBER rule, g760 SHA, static PC/Jennings input,
21,000-second producer cap and 5,600 MiB RSS cap unchanged.

## 3. Allowed new files

Use versioned v3 paths only:

1. a relator-checkpoint producer/adapter;
2. an ASCII-only producer GHA driver;
3. a bounded preflight/schema certificate;
4. `sol/luna_reply_165_r07_target6_relator_checkpoint_v3.md`.

An independent mathematical checker need not be duplicated: a completed
NONMEMBER must still be replayed by the v2 direct-enumeration checker, which
imports neither producer.  V3 may add a small standalone checkpoint-format
validator if that materially improves independence.  Do not modify v1/v2,
CLAIMS, proofs, workflows, or the Sol reply.

## 4. Relator checkpoint payload

Immediately after a complete relator closure returns, atomically write an
immutable checkpoint containing at least:

```text
schema/version and canonical self-digest
j
dimension and Jennings basis SHA
target and legal-row binding SHA values
completed_relator_prefix = [1,...,k]
next_relator = k+1, or null after relator 11
D2 echelon rank
lossless D2 echelon pivot list
v1/v2/v3 pin manifests and static binding
prior j-checkpoint / prior relator-checkpoint SHA and bytes
all global mathematical claims false
```

Encode each F3 pivot as

```text
[pivot_index, coefficient_one_plane_lowercase_hex,
              coefficient_two_plane_lowercase_hex]
```

sorted by increasing pivot.  Validate on load:

1. unique in-range pivots and vectors masked to the exact dimension;
2. disjoint one/two bit planes;
3. the recorded pivot is the leading nonzero coordinate and has
   coefficient one;
4. replaying the stored rows through a fresh `F3BitEchelon` reproduces every
   pivot and the exact rank;
5. the reconstructed pivot dictionary and canonical digest equal the saved
   state;
6. relator prefix, j, static basis, target, legal rows, base and all pins are
   unchanged.

If the actual insertion invariant needs a stronger ordering/reduction
canary, implement and explain it.  Never serialize Python pickle or an
implementation-dependent object graph.

## 5. Resume and terminals

- With no checkpoint, start j=9 relator 1.
- From a relator checkpoint, resume the same j at its exact next relator.
- From a completed v2/v3 j checkpoint, resume the exact next j at relator 1.
- Reject arbitrary j/relator skips, terminal checkpoints, missing ancestors,
  mutation, stale files and cross-directory path substitution.
- After relator 11, finish the legal+target membership reduction exactly as
  v1/v2, write the ordinary completed-j checkpoint, and continue in order.
- A resource stop preserves every completed checkpoint and makes no claim
  about the interrupted closure.
- MEMBER remains inconclusive.  Producer NONMEMBER remains candidate until
  the direct-enumeration checker agrees.

## 6. Bounded tests and venue

Use toy echelons to test round-trip and reject at least:

- one flipped bit plane;
- overlapping planes;
- wrong leading pivot;
- out-of-mask bits;
- missing or reordered relator prefix;
- wrong j/basis/target/legal binding;
- broken ancestor SHA/bytes;
- forged self-digest;
- noncanonical hex or pivot ordering.

Run only serial syntax, selftest and preflight locally.  Do not run the full
649,539-row calculation, git, push or GHA.  Parent Sol alone handles those.
The GHA driver must run exactly one producer process and zero checker
processes and must upload/hash every relator and j checkpoint.

## 7. Report boundary

Report paths, bytes, SHA-256, exact clean-checkout tests, mutation counts,
checkpoint size estimates, and resume invocations.  State explicitly:

```text
relator checkpoint = resource recovery, not a mathematical result
inherited j2..8 = producer control-flow candidate only
fresh NONMEMBER = candidate until helper-nonshared direct checker agrees
MEMBER != actual A18 lift
no fake / cofinal lift / Ihara witness declared
```
