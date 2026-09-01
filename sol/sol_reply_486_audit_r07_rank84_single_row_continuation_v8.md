# Sol reply 486 — Task484 rank-84 single-row continuation v8 audit

## Verdict

**GO.  Task484 is safe to dispatch as the narrow rank-84 continuation.**

No fatal defect was found in the release binding, resume identity, process
cardinality, resource envelope, syntax, marker gates, or claim boundary.

## Audit findings

### F1 — Permanent release and exact member pins pass

The permanent asset URL resolves to the commissioned archive.  A bounded
in-memory read independently reproduced its exact identity:

```text
bytes   23004
sha256  dde60bad768e20ead6ad08e8bd0a8e53fc97050a43f6c207552ba97d579c438a
members 7
```

All seven members are ordinary files with safe, single-component relative
names.  Their byte counts and SHA-256 values exactly match the seven-row
manifest in the driver and Luna reply.  There are no directory, absolute,
parent-traversal, backslash, or symlink members.  The driver authenticates the
archive before `unzip`, extracts into a newly created dedicated directory, and
then authenticates all seven extracted files.  Its fixed zip, extraction,
resume, result, checkpoint, and log paths are guarded against stale files,
directories, and dangling symlinks before use.  Historical `driver.g` and
`run.log` therefore remain isolated under the archive directory.

The source provenance agrees with the pinned record in v220: run
`33524681526`, job `99912387760`, head
`dd67f12b0ee4f022061df27ed396ad3d3a37f264`, artifact `9812928957`, and API
zip digest
`4b3239f35f6ec2a4859e6a81e2b49456702f0f22f695a7332089b407dbcb817d`.

### F2 — The resume object is exactly the cross-checked rank-84 state

The selected member is exactly
`d972_r07_a0_actual_tau_free_rank_ladder_v7_output.checkpoint`, 52,707 bytes,
SHA-256
`eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24f`.
Independent JSON/canonical-seal replay gave:

```text
schema          d972-r07-a0-actual-tau-free-rank-ladder/v3/checkpoint
rank            84
accepted_count  41 (accepted_sources length 41)
round           44
reason          UNKNOWN_RESOURCE:tau_free_localized_dual:time_limit
state_sha256    3c38d9021e20c04a24e99136e47902e8911658f244a202f9c49f4a4280e2f6a7
seal replay     exact match
```

The companion artifact independently reports the same rank/count/round and
typed reason, with every claim flag (`A0`, `COMMON`, `NONMEMBER`, `fake`, and
`Ihara`) false.  The driver rechecks the copied resume bytes and SHA before
passing that fresh path through the producer's real `--resume` interface.

### F3 — Exactly one pinned producer and one pinned checker are invoked

The live files reproduce their commissioned pins:

```text
producer  12215  0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37
checker    3653  e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1
```

The generated shell body contains exactly two `python3 -u -B` invocations:
one real v3 producer and one v7 independent checker.  The producer receives
exactly `--mode PRODUCTION`, the authenticated resume, `--seconds 7200`,
`--rss-bytes 4800000000`, `--max-rises 64`, and fresh result/checkpoint paths.
There is no fixture, self-test, second producer, shard, or preliminary heavy
replay.

### F4 — Resource margins and shell propagation pass

The producer foreground supervisor is 7,500 seconds, strictly above its
7,200-second internal wall by 300 seconds.  Bash `ulimit -v 5200000` is in
KiB, hence the hard VM ceiling is 5,324,800,000 bytes, strictly above the
4,800,000,000-byte internal RSS gate by 524,800,000 bytes.  This leaves a real
terminal/checkpoint serialization reserve.  The checker has a separate
3,600-second foreground timeout under the same hard VM ceiling, a sensible cap
for the single independent replay.

`set -euo pipefail`, foreground timeout, kill grace, and `tee` pipelines
propagate producer/checker timeout, signal, and nonzero failure.  Result and
checkpoint must both be nonempty before the checker runs.

### F5 — Syntax, markers, and claim boundary pass

The 7,680-byte ASCII driver has SHA-256
`ea4794dbe13e751e661804de238553b5607120c2f04d498fcc2a88fdaaed3edb` and a
final newline.  GAP `ReadAsFunction` parsed the complete file.  The exact shell
body produced by its GAP concatenations passed `bash -n`; both pinned Python
files passed independent AST parsing.

The shell requires exactly one anchored producer terminal line and exactly one
one-line v7 checker PASS.  GAP then requires the exact checker log and emits
only the exact driver marker
`R07_A0_RANK84_CHECKPOINT_RESUME_V8_DRIVER_PASS`.  Neither the driver nor the
reply calls workflow success, checker PASS, or an `UNKNOWN_RESOURCE` result an
A0/COMMON completion.  A further resource terminal remains a checked
continuation result only.

## Audit boundary

Only bounded reads, hashes, archive/state inspection, AST/GAP/Bash parsing,
and static cardinality/resource checks were performed.  No producer, checker
semantic replay, GHA/workflow action, git operation, or production computation
was run.  No implementation change is requested.

**GO**
