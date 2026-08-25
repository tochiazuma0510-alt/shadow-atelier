# Luna reply 163: R07 g760 L3 full-legal target6 gate v1

Date: 2026-08-26
Role: Luna mechanical implementation / independent finite checker
Status: **bounded preflight cross-checked; full mathematical run UNKNOWN and GHA-ready**

## 1. Outcome

The five authorized implementation artifacts were prepared without importing
the rejected v3 B0/B1/109-RHS lane.  The new producer rebuilds the g760 target,
prefix transport and all 28 C-13 legal-overapproximation rows from the frozen
base-independent E4/C-13 formulas vendored minimally inside the authorized
producer.  The producer has no runtime import of a koubou158 L3 file.  The new
checker uses a separate expression path and only the tracked frozen seedspan
arithmetic; it imports neither the new producer nor a koubou158 L3 core.

The bounded producer/checker replay passed.  The heavy rank/nonmembership
ladder and the 649,539-column direct checker were deliberately **not** run
locally.  Therefore no one of the four mathematical full-run terminals has
yet been obtained.

The contamination audit
`sol/audit_r07_760_v3_full_lane_contamination_v97.md` was applied as a hard
boundary.  There is no call to `build_fresh_prefix`, `construct_fixed_B1`, the
old-qstar B1, or the mixed old20-source-anchor chain.  Historical old20 data
are serialized only under `historical_old20_diagnostic_only` and are never a
rank, blocker, target or separator requirement.

## 2. Fresh construction implemented

The producer independently enforces:

- `g760 = w2*(w3^-1*w2)^8*y^36*x^-108`, length 760, signed-list SHA-256
  `518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d`,
  exponent sums `(0,0)` and parent-616 SHA-256
  `3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90`;
- `A=g(X0,Y0)`, `B=g(X0,Z0)`, `C=g(Y0,Z0)` and target `C*B^-1*A`;
- fresh target word SHA-256
  `36ebf29263cb40e1e37983fecb1f82d9b7eefa3d56b89f1574788c5c0ffdbbfd`;
- prefix action exactly `fbar_xz*fbar_yz^-1 = B*C^-1`, with value digest
  `9ceef6f91a34c45258df09a859300bda66f92a4dee15219cd144353aa7e0b887`;
- Delta order 27, nonabelian exponent-3/class-2 type, and all 28 Schreier
  generators, whose roster digest is
  `c7053b4b2c085ff8016ad1da1e0459dc77f0fc777323693b93f1157de0fbde1e`;
- all 28 projected Sigma rows (digest
  `2e21a906124d170c117663fd1e2fcd9318e682b44cc96cfc19a52ece717e73e0`);
- the complete eleven PB4 relators and projected gradients (digest
  `0532b9cc3ba757dbe8e956cff3593b37514358c63ca7ab188c0f5ac167a8d0f5`);
- preregistered ascending `j=2,...,12`, first-nonmember stopping, fresh ranks,
  and a complete separator replay if nonmembership occurs.

At a negative rung, the producer independently streams all
`11*3^10 = 649,539` translated PB4 rows to replay the separator, then rebuilds
that rung from an empty BFS state.  The checker instead directly enumerates
all 59,049 PC elements times eleven relators at every tested rung; it does not
use the producer BFS closure or accept serialized rank/membership booleans.

## 3. Independent checker and destructive gates

The bounded checker reconstructed the full static g760 envelope and matched
the producer receipt.  It passed eleven destructive checks:

1. tail sign mutation;
2. stale base SHA mutation;
3. target product-order mutation;
4. inverse prefix mutation;
5. PB4 coefficient mutation;
6. Jennings-coordinate mutation;
7. omitted legal row;
8. historical-old20 target substitution;
9. target-annihilating forged separator;
10. row-missing forged separator;
11. nonmonotone pivot-insertion mutation.

The last test exposes the former insertion-order hazard explicitly: pivots
inserted in order `2,0,1` make reversed insertion order visit `1,0,2` and miss
one pivot row.  `SparseTracker.separator` now uses
`sorted(self.pivots, reverse=True)`, and the counterexample confirms that the
old order fails while numeric descending back-substitution annihilates every
row and pairs nontrivially with the target.

Bounded commands and final markers were:

```text
python -u -B search/d972_r07_760_l3_target6_v1.py --self-test
R07_760_L3_TARGET6_V1_PRODUCER_SELFTEST_PASS toy_member=1 toy_nonmember=1 separator=1

python -u -B search/d972_r07_760_l3_target6_v1.py --preflight --output ci/out/d972_r07_760_l3_target6_preflight_prospective.json
R07_760_L3_TARGET6_V1_PRODUCER_PASS preflight_state=R07_760_L3_TARGET6_PREFLIGHT_READY sha256=4d305a1af415ffb5acf1d029a69c1b720961fce88dc86575d8fde2d504a787ab bytes=663780

python -u -B crosscheck/check_d972_r07_760_l3_target6_v1.py --self-test
R07_760_L3_TARGET6_V1_CHECKER_SELFTEST_PASS toy_member=1 toy_nonmember=1 separator_mutations=3

python -u -B crosscheck/check_d972_r07_760_l3_target6_v1.py --receipt ci/out/d972_r07_760_l3_target6_preflight_prospective.json --mutations
R07_760_L3_TARGET6_V1_CHECKER_PASS preflight_state=R07_760_L3_TARGET6_PREFLIGHT_READY mutations=11 full_replay=false receipt_sha256=4d305a1af415ffb5acf1d029a69c1b720961fce88dc86575d8fde2d504a787ab
```

The ASCII GAP driver also passed its short serial selftest:

```text
.\gap.ps1 search\d972_r07_760_l3_target6_gha_driver_v1.g -ExtraArgs @('-c','D972_R07_760_L3_TARGET6_V1_SELFTEST:=true;;')
R07_760_L3_TARGET6_V1_GHA_DRIVER_PASS mode=selftest preflight_mutations=11 receipt_sha256=4d305a1af415ffb5acf1d029a69c1b720961fce88dc86575d8fde2d504a787ab bytes=663780
```

One initial sandboxed GAP launch failed before reading the script because the
Windows runtime could not create its signal pipe.  The authorized rerun above
completed in 15.8 seconds.  No production loop ran in either attempt.

The subsequent GHA selftest run `32879297297` was also invocation-only and
does not alter any mathematical grade.  Its workflow environment rendered
the former string preamble as
`D972_R07_760_L3_TARGET6_V1_PYTHON:=python3;;`; transport stripped the quotes,
so GAP stopped with `Variable: python3 must have a value` before `Read` of the
driver.  It emitted no producer/checker receipt and no mathematical terminal.
The repaired driver uses the quote-free boolean below.  Its bounded local
serial selftest passed again in 6.6 seconds with the same preflight receipt and
eleven destructive gates.  Full mode was not run.

GHA selftest run `32879752404` passed the repaired quote gate but stopped at
the next input-packaging gate.  Its clean checkout had committed
`provenance/CLAIMS.md` at 66,635 bytes / SHA-256
`174ddbb50d1579c9373482552759ed2ec822846f1dd83c8d73b13c652ae77f64`,
whereas the driver had pinned the user's dirty local value 68,363 bytes /
`37325e7e7d734f7619785eb1832a051a4e35bb7409e0adaad413443a13038c00`.
It stopped before producer `Read`, emitted no receipt and no mathematical
terminal.  Runs `32879297297` and `32879752404` are therefore both
invocation/input-packaging failures only, not mathematical runs.

## 4. Preflight receipt typing

The preflight artifact has schema `d972-r07-760-l3-target6/v1`, mode
`preflight`, and claim-free state `R07_760_L3_TARGET6_PREFLIGHT_READY`.  It
intentionally has no `terminal_token`: the four preregistered exclusive
terminals are reserved for a full mathematical run, and it would be false to
label a bounded construction receipt MEMBER, NONMEMBER, RESOURCE or INPUT.

All five global claims are false, as are the freshness flags for old20 target,
old20 ranks, old616 target, historical blocker/B0/B1, registered-108 family
and literal five-coface A.18.  In particular the preflight is not an A.18
occurrence, normalized Brunnian class, compatible cofinal lift, Ihara witness,
or all-bases obstruction.

## 5. Clean prospective-HEAD packaging audit

The clean audit base was commit
`eaf7d5ed528143837ddfe68942d0dce4ac4a4611`, extracted with `git archive`
under `%TEMP%`.  Only the four prospective runtime artifacts were overlaid;
the generated prospective certificate was independently replayed and then
mechanically copied to its one authorized repository path after exact
SHA/byte authentication.  The user's dirty `provenance/CLAIMS.md`, dialogue
ledger and every unrelated local/untracked file were neither modified nor
used as runtime content.

Every prospective runtime path was present (`14/14`, missing `0`):

```text
PRESENT  search/d972_r07_760_l3_target6_v1.py                                      53284   7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde
PRESENT  crosscheck/check_d972_r07_760_l3_target6_v1.py                            42005   355b01a67447cd371f6a1e2ebbaed73e1408181717d9ce857aecb8723bfe98ea
PRESENT  search/d972_r07_760_l3_target6_gha_driver_v1.g                            12380   1c0d374dfd61306a7f9f4777a65469e454cc77d5b0f0d5c7272123e293f9e73a
PRESENT  search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json          663780   4d305a1af415ffb5acf1d029a69c1b720961fce88dc86575d8fde2d504a787ab
PRESENT  sol/luna_task_163_r07_760_l3_target6_v1.md                                 9066   9fcdf2f25b724e9dbc225f417b0036e126e7b5e37a0778dab5e0299ee2f74e12
PRESENT  provenance/CLAIMS.md                                                      66635   174ddbb50d1579c9373482552759ed2ec822846f1dd83c8d73b13c652ae77f64
PRESENT  docs/対話帳.md                                                            234377   a5eadcc04468b593e0a1c7896409a59b55c6442ca489df6a91aac60d6e128a06
PRESENT  sol/proof_r07_joint_derived_commutator_rebase_v92.md                       5969   cc56e2187fac08ffa70fe3753e200627e776b5fa591738dee5da908e4d217387
PRESENT  sol/audit_r07_uniform_explicit_lift_checkpoint_v95.md                      5324   12877306446bcfe8b57b01751c929bdee78d15300c4f90a8311764ff2d7eeeae
PRESENT  sol/luna_task_162_r07_760_commutator_affine_rhs_v3.md                      4053   8ca38afc6f30e8e6074f191a17541f508f29ba1da58d3b286ba4fcf33406ae21
PRESENT  sol/luna_reply_162_r07_760_commutator_affine_rhs_v3.md                     8833   70ebb7bf433fafd77dc828efe5f71b9dd6dc982e7682a4c6397695b6a2e6bcf5
PRESENT  search/certs/d972_r07_616_to_760_commutator_affine_rhs_preflight_v3_20260826.json  184890  55752b6c1a748fb0b25a86d6fc1a0381a82b203112568b0b1963c5665cef0408
PRESENT  ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json            231570   3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
PRESENT  search/d972_b345_seedspan_triple4_v1.py                                  535219   fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29
```

On Windows, `git archive` decoded the UTF-8 dialogue filename to a mojibake
display name.  The clean test copied that exact 234,377-byte HEAD blob to the
correct Unicode filename inside `%TEMP%`; no dirty workspace dialogue content
was copied.  Linux/GHA checkouts retain the tracked UTF-8 pathname directly.

These six historical C-13 files are absent from this branch HEAD.  They are
recorded in the producer/checker receipt as `runtime_pin=false` and
`present_in_packaging_HEAD=false`; neither code path opens them:

```text
search/koubou158_L3_radical_v1_2.py                                     14488  05e96bb3e7d0e9b949cb8d9ec0d216f97a698777df82d56449bcc20f89933f17
search/koubou158_L3_core_v1_2.py                                        31192  4366ebd1759fbd11a795b251101776836ef4ec2a28b7b947b93727208e199c63
crosscheck/check_koubou158_L3_radical_v1.py                              28198  451aa614d2c83f43291fa80abf09abe425004288717ed6278b5690b511724529
search/certs/koubou158_L3_radical_v1_1_20260822.json                     17418  4a80c0b4c063eaab31ce32aad69eb9f21c220278dc748e31439aef9af38a2ca2
search/certs/koubou158_L3_radical_v1_2_20260822.json                     20930  56ab4592bf5b64fbe5605afe063681e8c059929cd8abbc07323988aff4a8440f
crosscheck/verdicts/koubou158_L3_radical_crosscheck_v1_20260822.json      7654  c87e12ba96ea95607e99701e1e92786ac93ba08c91ad424dbea1f252304b1b78
```

The vendored producer core was additionally compared, outside the runtime
path, with the local historical v1.2 core on deterministic calibration data:

```text
VENDORED_C13_CALIBRATION_PASS pc_products=16 inverses=4 fox=6 projections=16 j=2..5
```

This is development-audit parity, not a runtime dependency.  The stronger
bounded check is the clean producer receipt agreeing with the structurally
independent seedspan checker on the entire static target/Sigma/PB4 envelope.

The first clean driver attempt exposed only a local Cygwin-old-Python
compatibility issue: `int.bit_count` was unavailable.  The vendored F3 dot
product now uses the historical-compatible `bin(x).count("1")`; after that
repair the complete clean serial driver selftest passed in 6.6 seconds.  All
producer, checker and driver invocations were awaited one at a time.  No
parallel or concurrently active Python subprocess was used.

## 6. Exact GHA dispatch inputs

Use a fresh wrapper with exactly one mode.  Selftest input:

```gap
D972_R07_760_L3_TARGET6_V1_SELFTEST:=true;;
D972_R07_760_L3_TARGET6_V1_USE_PYTHON3:=true;;
Read("search/d972_r07_760_l3_target6_gha_driver_v1.g");;
QUIT_GAP(0);;
```

Full input:

```gap
D972_R07_760_L3_TARGET6_V1_RUN:=true;;
D972_R07_760_L3_TARGET6_V1_USE_PYTHON3:=true;;
Read("search/d972_r07_760_l3_target6_gha_driver_v1.g");;
QUIT_GAP(0);;
```

`USE_PYTHON3=true` selects the internal literal string `"python3"`; no quoted
string crosses the workflow binding boundary.  The omitted boolean defaults
to local `"python"` for bounded Windows selftests, but full mode rejects its
absence or `false`.  The obsolete
`D972_R07_760_L3_TARGET6_V1_PYTHON` string binding is rejected whenever it is
bound, so old and new bindings cannot silently conflict.

Recommended invocation is the existing GAP 4.16 GHA command with `-o 12g`.
The full driver gives the producer 10,200 seconds and producer+checker a
shared 21,000-second budget.  The checker receives the exact remaining time.
A 360-minute job timeout and at least 12 GiB runner memory are appropriate;
each serial Python process enforces a 5,600 MiB RSS cap.  The artifact is
`ci/out/d972_r07_760_l3_target6_v1.json`.

Success requires exactly one each of

```text
R07_760_L3_TARGET6_V1_PRODUCER_PASS
R07_760_L3_TARGET6_V1_CHECKER_PASS
R07_760_L3_TARGET6_V1_GHA_DRIVER_PASS mode=full
```

and exact producer/checker agreement on exactly one of

```text
R07_760_L3_TARGET6_NONMEMBER
R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE
R07_760_L3_TARGET6_UNKNOWN_RESOURCE
R07_760_L3_TARGET6_INPUT_STOP
```

The driver binds receipt SHA/bytes, rejects traceback/error/Reject markers,
and deletes only its five explicit `ci/out/d972_r07_760_l3_target6_v1*`
outputs.  No workflow was changed, and no git operation or GHA dispatch was
performed.

## 7. New file ledger

```text
53284  7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde  search/d972_r07_760_l3_target6_v1.py
42005  355b01a67447cd371f6a1e2ebbaed73e1408181717d9ce857aecb8723bfe98ea  crosscheck/check_d972_r07_760_l3_target6_v1.py
12380  1c0d374dfd61306a7f9f4777a65469e454cc77d5b0f0d5c7272123e293f9e73a  search/d972_r07_760_l3_target6_gha_driver_v1.g
663780 4d305a1af415ffb5acf1d029a69c1b720961fce88dc86575d8fde2d504a787ab  search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json
```

The driver is ASCII-only.  The fixed task pin used by all three code paths is
9066 bytes / SHA-256
`9fcdf2f25b724e9dbc225f417b0036e126e7b5e37a0778dab5e0299ee2f74e12`.
The v97 contamination audit consulted here is 5700 bytes / SHA-256
`ea1f16a72b4f71efde628e9d1d17d43cdb39856f8b01cb676a18c2b059f116e6`.

## 8. Grade and unresolved result

```text
BOUNDED g760 STATIC/PREFLIGHT: CROSS-CHECKED
DESTRUCTIVE MUTATIONS:        11/11 PASS
CLEAN RUNTIME PATHS:           14/14 PRESENT
VENDORED/HISTORICAL CALIBRATION: PASS (DEVELOPMENT AUDIT)
FULL PRODUCER:                 NOT RUN / UNKNOWN
FULL DIRECT CHECKER:           NOT RUN / UNKNOWN
MATHEMATICAL TERMINAL:         UNKNOWN PENDING GHA
LEAN VERIFIED:                 NO
```

Only a future producer/checker-agreed `NONMEMBER` with the full pairing replay
supports implication (2.2) for this one explicit g760 prefix and this one
target6 edge.  `MEMBER_INCONCLUSIVE` remains only survival of this L3 screen.
