# Luna task 455: Task453 batch-64 provenance carrier pin successor v2

Role: Luna implementation owner.  Make a pin-only Task452 carrier successor
for the already dispatched Task453 batch-64 run.  Do not change Task451 search
or any literal-carrier mathematics.

## Exact provenance boundary

The accepted Task452-v1 carrier is pinned at:

```text
search/d972_r07_task451_task193_carrier_v1.py
  8553 / 18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644
crosscheck/check_d972_r07_task451_task193_carrier_v1.py
  8516 / 82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73
search/d972_r07_task451_task193_carrier_gha_driver_v1.g
  2499 / cdf8f4276740a18fc312de3dfca8669a0c8afd424d2551f00596e6d63251cf6a
```

Its upstream Task451 producer/checker and frozen rank-51 checkpoint remain
byte-identical.  Task453 changes only the production driver provenance:

```text
search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g
  2387 / 8f8c803cff86fbb4bb774570cb596e9e5a8262c05321e955e2cf0de545df60dc
Task453 dispatched source head
  7498d381de7180c8ca562fba5cf3bc15323d522c
GHA run/job
  33516227668 / 99883831511
```

That wrapper exact-pins the old v1 driver and constructs an inner whose sole
change is `--batch-cap 16` to `64`.  The new carrier must require the actual
Task453 head above and exact-pin the outer v2 driver.  It must never accept a
caller who reports the old `3316809e...` head for a Task453 artifact.

## Required implementation

Create a versioned carrier-v2 producer, helper-nonshared checker, and driver.
An exact cardinality-checked source successor from accepted carrier-v1 is
preferred.  Advance every carrier schema, terminal, checker schema/terminal,
module label, output path, driver guard, and final marker.  Replace only the
upstream driver pin and required source head/provenance fields.  Preserve
byte-for-byte mathematical behavior:

- exact `C451.check(result)` replay and physical result/checkpoint/log binding;
- extraction only from checker-equal `terminal_replay.literal_word`;
- 760-letter `g760`, right multiplication, exponent zero, ten-coordinate
  joint kernel, target/correction owner, all-seven/eleven-occurrence replay;
- full replay, task193 u32be sparse digest, hexagon and printed pentagon flags;
- selected action ancestry and carrier/checker seals;
- carrier-only claims with A2/lift/fake/Ihara false.

Do not accept both heads in one untagged branch.  V1 remains the exact
batch-16 dialect; v2 is the exact Task453 run dialect.  A RESOURCE/UNKNOWN or
non-PASS input remains nonpositive.

## Tests and scope

Run only bounded compile, source-patch cardinality, fixture, mutation, pin,
ASCII, and expected external-guard tests.  Do not run Task451/Task452
production, GAP production, GHA, git, network, or credentials.  Do not copy
Q0, batches, duals, echelons, or fibres.

Create only:

```text
search/d972_r07_task451_task193_carrier_v2.py
crosscheck/check_d972_r07_task451_task193_carrier_v2.py
search/d972_r07_task451_task193_carrier_gha_driver_v2.g
sol/luna_reply_455_r07_task453_carrier_pin_successor_v2.md
```

Do not edit v1, Task451/Task453, workflows, v220, claims, proofs, or
provenance.  Do not commit/push/dispatch.  Report exact old/new replacement
cardinalities, final pins, fixture terminals, mutation total, and any blocker.
