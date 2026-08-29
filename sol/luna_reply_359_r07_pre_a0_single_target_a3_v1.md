# Luna reply 359 — R07 pre-A0 single-target actual A3 compiler v1

Implemented the five authorized outputs only.  No Python, Node, GAP, GHA,
workflow, git, or network command was run.

## Machine-owner seals

| owner | bytes | SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_pre_a0_single_target_a3_v1.prereg.v1.json` | 6691 | `f8092796af77da3ea137908b1cca48db6563c412d937147bc341be29cc49489f` |
| `search/d972_r07_pre_a0_single_target_a3_v1.py` | 45897 | `de69138d64a0324b45cd8327cb1425df88dcf54525c32d6127f0dbac251e94d6` |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v1.py` | 46751 | `ba087b0e37fa15a7ff8dbb1a1d65509e0a3721b4d1b4a0f07789c40c3411ad7d` |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v1.g` | 7032 | `69ac613a075b3677b16b038ae9be8dd0954acfbfd9038b6929f94f5ada322f8a` |

P0 self seal: `406b333ee2acfd67e09a5cd43ba75abb03d7c4d4a80df14efc5ae70ed038fa18`.
P0 pins schema `d972-r07-pre-a0-single-target-a3/v1/prereg/v1`, exact terminal
vocabulary, caps, central rows, false-conclusion flags, mutation roster,
v302 (`ba508...`) and v303 (`9868aa...`).  It also records the frozen task227
SELFTEST run `33153010409`, head `d1e34bb450bdee48633f64b251db5b14580ce798`,
artifact `9678665435`, archive `cf67587fe34dd33d8bef1d79e57b942cccb54c03ca4de189b04c0daf97199549`,
receipt `4636766/dd642ad26b336c9ee5c399798b83867465cb9023c4ec08a02af3fa2eeb723df8`,
and verdict `615/3ea0e5e59662c3014364adcf11d3ec40d8e52d70a36c20d6529c7e00236238ea`.

## Authority and import graph

Both Python owners authenticate the P0 raw canonical bytes and self seal,
then hash every recursively pinned authority owner before any import.  The
authority includes the accepted task198 receipt, v3 acceptance manifest,
both attestations, checker verdict, all three task198 source owners, both
g760 ancestry owners, v302/v303 proof owners, task226 producer/checker,
task227 producer/checker/driver, and the frozen task227 SELFTEST metadata.
The producer imports only the pinned task226 producer and task227 producer
under `_d359_producer_*` names.  The checker imports only the pinned task226
and task227 crosscheck engines under `_d359_checker_*` names.  No `sys.path`
lookup, subprocess, shared helper, task192 input, or receipt-supplied source
identity is used.  The driver independently pins P0, both new programs, and
every P0 authority file before serial execution.

## Mathematical and typing trace

Producer locations are `construct_g760` line 563, `base_checks` 575,
`central_replay` 626, `make_projection` 673, `area_canary` 761,
`run_mutations` 832, and the single `t227.closure(..., structural=None)`
call at line 957.  The checker repeats these owners independently at lines
525, 561, 599, 669, and 718, and invokes only `t227.verify_gate` at line 900.

Each side contains literal W2/W3, free reduction, inverse, exponent sums,
and the exact `g616`/`g760` length and digest pins.  The side-local task226
constructor receives `(g760, [], authenticated_task198_ledger)`.  The full
package is typed `PRE_A0_COMPUTATIONAL_BASE_ONLY` with
`correction_word_constructed=false`, `task192_consumed=false`,
`f_role=BASE_REFERENCE_EQUAL_TO_G760`, `f=g760`, `a=[]`, `B_a=0`, and equal
base/f occurrence words.  Retained `f`, `rword_f`, `B_a`, and PB-chain fields
are marked `BASE_REFERENCE_ONLY` with `transfer_evidence=false`.

The explicit `projected_a3_interface` contains authenticated ledger and
digest, quotient/action ABI, all eleven `p_o/xi_o/w_o/u0_o` rows, combined
`w/u0`, and all three `1-R_B(g760)` target blocks.  Only the resealed
projected ABI is passed to the closure.  Each side independently computes
the signed central rows/products/sums and Fox endpoint identity, then builds
the three `zword^t` representatives (`t=0,1,2`) through its own task226
engine, labelled `PROJECTED_AREA_REPRESENTATIVE_ONLY`.

## Closure, checker, mutations, and resources

The producer encodes one frozen task227 gate retaining occurrence ancestry,
the 486 ideal rows, 729 translates, block echelon/remainder, and the complete
MEMBER coefficient replay or NONMEMBER dual pairings.  Top terminals map only
to `R07_PRE_A0_A3_PROJECTED_MEMBER` or
`R07_PRE_A0_A3_PROJECTED_NONMEMBER_DUAL`; both UNKNOWN terminals are typed and
non-accepting.  The checker reconstructs the ABI, central replay, area
canary, and all gate rosters before its single independent verifier call.

Both sides execute the twelve cheap P0 glue mutations exactly once each:
task198 raw/manifest binding, ledger sign, prefix, g760 letter/digest,
computational-base mode, forbidden task192 binding, H1/H2/P central rows,
projected-area target, ABI seal/target, and forbidden conclusion flag.  Each
record has changed before/after owner SHA and first rejection gate; only the
narrow registered rejection is caught, and `MutationAccepted` is not caught.
The accepted task227 24-mutation/three-edge SELFTEST is recorded as frozen
ancestry and is not rerun by this wrapper.

P0 caps are conservative: input 500,000,000 bytes; authority 400,000,000
bytes; two dynamic imports; three area builds; one base ABI; one closure;
486 occurrence/block rank increases; 729 checker-roster entries; 2,000,000
actor/orbit/closure actions; 1,000,000 dual work; 100 glue mutations;
2,000,000,000 serialized bytes; 6,442,450,944-byte RSS; and 21,600 seconds.
Each process has one meter and returns only typed UNKNOWN on a measured cap.
Measured wall, RSS, output size, and one-case runtime remain UNEXECUTED.

The GAP driver is serial and fail-closed (lines 61-96): it refuses stale
`ci/out` paths, redirects producer/checker logs, uses bounded `timeout 21600s
python -u -B` for each process (the P0 21600-second cap is per process; the
producer+checker serial worst-case is 43200 seconds plus small launch/validation
overhead), requires exactly one terminal per log, checks fresh receipt and
verdict bytes, and source line 87 emits
`grep -Fq -- '"receipt_sha256":"'${rsha}'"'`, so the physical receipt SHA
expands between the fixed JSON quotes before the verdict binding is checked;
ends with `R07_PRE_A0_SINGLE_TARGET_A3_DRIVER_SENTINEL_PRODUCTION`.

`TASK359_R07_PRE_A0_SINGLE_TARGET_ACTUAL_A3_COMPILER_V1`

V302 ACTUAL CENTRAL REPLAY:          IMPLEMENTED
PRE-A0 COMPUTATIONAL BASE ABI:       IMPLEMENTED
ONE ACTUAL 486/729 CLOSURE ROUTE:    IMPLEMENTED
INDEPENDENT MEMBER/DUAL CHECKER:     IMPLEMENTED
CHEAP GLUE MUTATIONS:                IMPLEMENTED
SERIAL GHA DRIVER / P0:              IMPLEMENTED
EXECUTION / GHA:                     UNEXECUTED
ACTUAL A3 NUMERATOR:                 remains 0/3 pending accepted run
A0 COMMON / POINTED / EXACT PB:      OPEN
COFINAL LIFT / FAKE / IHARA:         NONE
