# Luna reply 292 - R07 actual three exact PB endpoints v2

Only the five authorized v2 paths were created. No Python, GAP, GHA, network,
or git command was executed.

## Static identities

```text
producer  40044  c44d2c8e7fdd7dcbf691600ba823445d1ac45695ef173043c723874a409f7208
checker   46873  8d7598f376715af16ccec7bae5550f2c5329922b1b36326643a2a4e9e7cf72d8
driver     5542  da35b73d2144b4e2d2850079e4aed6b19231cc589d42181b00333fd616b85dc5
fixture    1696  5583205a500a878460de58e577daec0a2feff612b35742caf31ae0e4e902a9f7
reply      self-referential bytes/SHA intentionally omitted (CV-10)
```

The reply's external identity is reported to the caller after the final bytes
are written; embedding it here would change those same bytes.

## v1 to v2 repair

The endpoint mathematics was not rebuilt. Static slices from `reduce_word`
through the fixture boundary in the producer, and from `cancel` through the
fixture boundary in the checker, agree with v1 after only normalizing the
checkpoint-owner version label.

The mechanical wiring changes are:

1. Schema, producer/checker/fixture paths, output paths, log labels, checkpoint
   owner, and final sentinel are all v2/task292 identities.
2. Every rejected task285 source pin, task285 receipt/verdict path, CLI option,
   reader, object-shape authenticator, and driver pin was removed.
3. PRODUCTION now deterministically emits
   `UNKNOWN_INPUT:task285 accepted MEMBER/M ABI unavailable; a future accepted ABI requires a new explicit binding version`
   without reading any task285 or `ci/in` file.
4. The checker independently accepts only the exact sealed v2 blocker envelope
   with that same terminal and `checkpoint_contract.owner=task292-producer`.
   Its verdict keeps `production_member_authenticated=false` and records the
   production binding as absent. This is envelope acceptance only, not MEMBER,
   endpoint ZERO, or A7 acceptance.
5. The synthetic upstream-seal mutation now uses a local
   `future_a5_a6` canary; it does not name or consume a task285 SELFTEST.

The v1 exact PB endpoint/Artin/full-C1 engine, independent pointwise replay,
five synthetic cases, two typed guards, and all 21 destructive mutation owners
remain present. Static fixture parsing gave exactly 5 cases, 2 guards, and 21
mutations. Producer and checker contain no mutual/helper import.

## SELFTEST dependency closure

The raw pin table contains only the v2 producer/checker/fixture and these
commission-designated tracked load-bearing sources:

```text
search/d972_r07_normalized_exact_common_word_cached_v3.py
crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py
search/d972_r07_second_frattini_affine_prefix_compiler_v1.py
crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v1.py
search/d972_r07_actual_two_word_endpoint_specializer_v2.py
crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py
search/d972_r07_seven_context_roof_presentation_v1.py
crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py
```

All eleven raw pins (three v2 artifacts plus eight tracked sources; the v2
driver itself uses CV-10 path/schema/version identity) were compared statically
against current bytes and full SHA-256 values with zero mismatches. The driver
has zero non-ASCII characters. It retains stale-output rejection, exactly one
producer/checker terminal, terminal equality, typed-terminal grammar, SELFTEST
synthetic ZERO expectation, and one v2 sentinel.

Neither SELFTEST producer nor SELFTEST checker reads or pins task285 source,
receipt, or verdict bytes. SELFTEST therefore has no task285 or `ci/in`
dependency. PRODUCTION also has no such file dependency and reaches its typed
UNKNOWN_INPUT path rather than being preempted by a GAP missing-file error.

## Status boundary

```text
V2 WIRING REPAIR:                       IMPLEMENTED STATICALLY
ENDPOINT/ARTIN/FULL-C1 CORE:            PRESERVED FROM V1
5 CASES / 2 GUARDS / 21 MUTATIONS:      PRESERVED
SELFTEST / CHECKER / DRIVER EXECUTION:  UNEXECUTED
ACCEPTED TASK285 MEMBER/M ABI:          ABSENT
PRODUCTION RESULT:                      TYPED UNKNOWN_INPUT (FAIL CLOSED)
```

The synthetic SELFTEST ZERO and production UNKNOWN_INPUT are not declared to
be an actual A7 ZERO. A8, A9, mixed-prime, perfect-core, fake, and Ihara flags
remain false; no such conclusion is declared.

`TASK292_R07_ACTUAL_THREE_EXACT_PB_ENDPOINTS_V2_UNEXECUTED`

## Sol dispatch record

After static acceptance, the parent Sol broker committed and pushed the exact
v2 package in commit
96b03359e31012322ac96f623ef47deffdb7332d and dispatched generic
gap-run.yml in SELFTEST mode:

```text
run_id   33161477632
head_sha 96b03359e31012322ac96f623ef47deffdb7332d
status   DISPATCH_WIRING_FAILURE
reason   CLI dispatch stripped the GAP string quotes before the driver ran

run_id   33161574578
head_sha 96b03359e31012322ac96f623ef47deffdb7332d
status   SELFTEST_CROSS_CHECKED_PASS
```

The successful run returned the same exact terminal from producer and the
helper-nonshared checker:

```text
terminal       R07_THREE_EXACT_PB_ENDPOINTS_ZERO
receipt        1197967 bytes
receipt_sha256 6315d0616ffce490aa871614af44f16d89b1d1b062da42fc17a92617a2afd2d4
verdict        6840 bytes
verdict_sha256 ac17f4e43a87e7e7d9d135ae3c6564681dee16fcda9be5d0a9da45b9a7c5137a
artifact_id    9681866887
artifact_zip   sha256:b00acd4ea8ea2ecbd9752db2d07fcef94f3319a665583eb289831ac025aca284
```

The checker independently accepted all five expected terminals, both typed
guards, the full Artin/full-C1 replay, and all 21 changed-owner mutations.
It records producer_imported=false and production_member_authenticated=false.
This cross-checks the implementation SELFTEST only.  The input is synthetic,
so A7 actual H1/H2/P remains 0/3.
