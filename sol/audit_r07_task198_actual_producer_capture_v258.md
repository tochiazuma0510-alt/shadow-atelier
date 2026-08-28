# R07 task198 actual producer capture audit v258

Author: Sol / 2026-08-28

Status: authenticated actual producer capture, awaiting the independent
production checker.  The receipt is a candidate until that checker accepts
the exact production object.  No A4 run, lift, fake certificate, or Ihara
conclusion is declared.  `verified=false`.

## 1. Run and artifact identity

```text
run id          = 33155653989
head            = bed1d5e6b41477b8799f2a33a24e46f7800f9510
mode            = PRODUCER_CAPTURE
conclusion      = success
artifact id     = 9684074697
artifact digest = adbd58fb887bce0b3be86ce1302447f7a1fd875607384ef39c159ba855b36840
artifact bytes  = 715186
```

The downloaded artifact was read outside the repository.  Its actual receipt
is

```text
member = d972_r07_seven_context_roof_presentation_v1.json
bytes  = 31017244
sha256 = d4bccb2f6443acde5ebe07c3648fc9a505315fd4b2eb00e6cdbad372fa9c5f4b
self_digest_sha256 = cdfd677f4d912232ad7d125bfec092905619e99f3d9ba9d6896614236443fec7
```

The producer log contains exactly the positive terminal

```text
R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM
```

and the driver sentinel is present.

## 2. Exact receipt observations

The receipt has schema `d972-r07-seven-context-roof-presentation/v1`, status
`COMPLETE`, and terminal `ROOF_BRIDGE_ISOMORPHISM`.  Direct readback gives:

```text
presentation row_count / rows length = 6441 / 6441
layer counts = Gamma_Cayley 6318, Q0_lift 19, action 104
chunks = [0,1024), [1024,2048), [2048,3072), [3072,4096),
         [4096,5120), [5120,6144), [6144,6441)
rows sha256 = e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950
presentation normal closure exact = true
Delta0 normal closure exact = true
bridge image order / kernel order = 357128352 / 1
bridge relator replay count = 6441
bridge seven blocks / occurrences / marked replays = 7 / 11 / 4
evaluator coordinate widths = 40,40,40,40,40,154,154,154,154,154
```

The evaluator binds the same relator-row digest and the registered v188
consumer action ABI.  The receipt explicitly leaves `fake`, `cofinal_lift`,
and `Ihara_witness` false.

## 3. Acceptance and performance boundary

This capture has no checker verdict or checker terminal.  Therefore it does
not close A1 production acceptance and must not yet be staged as the A4
authenticated input.  Production run 33155710862 is independently replaying
the producer/checker path at the same immutable head.

The producer reports a one-process elapsed time of 10,564.41 seconds.  The
current direct driver recomputes the producer before running the checker,
rather than consuming the already captured immutable member.  For this
already-running direct job, cancellation would discard completed work; it is
left running.  Future reruns must prefer a checker-only authenticated-capture
mode or an equivalent exact-artifact handoff so the three-hour producer is not
repeated merely to obtain an independent verdict.

The forthcoming A4 code audit must likewise include performance soundness:
no repeated 31 MB parsing, repeated 6,441-row construction, quadratic rank
rebuild where incremental echelon data exists, unbounded materialization, or
serial duplicate replay may be accepted without a stated necessity.

## 4. Accounting

```text
A1 driver / producer SELFTEST / checker SELFTEST: 3/3 complete
A1 actual producer capture:                       POSITIVE CANDIDATE
A1 actual independent production acceptance:      PENDING
v220 A1:                                          3/4
A4 actual:                                        0/3
WITNESS / FAKE / IHARA:                           NONE
```

`R07_TASK198_ACTUAL_PRODUCER_CAPTURE_POSITIVE_CHECKER_PENDING`
