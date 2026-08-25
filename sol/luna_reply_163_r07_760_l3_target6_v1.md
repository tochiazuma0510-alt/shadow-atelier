# Luna reply 163: R07 g760 L3 full-legal target6 gate v1

Date: 2026-08-26
Role: Luna mechanical implementation / independent finite checker
Status: **bounded preflight cross-checked; full mathematical run UNKNOWN and GHA-ready**

## 1. Outcome

The five authorized implementation artifacts were prepared without importing
the rejected v3 B0/B1/109-RHS lane.  The new producer rebuilds the g760 target,
prefix transport and all 28 C-13 legal-overapproximation rows from the frozen
base-independent E4/C-13 core.  The new checker uses a separate expression
path and only the older frozen seedspan arithmetic; it imports neither the new
producer nor either koubou158 L3 producer/core.

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

python -u -B search/d972_r07_760_l3_target6_v1.py --preflight --output search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json
R07_760_L3_TARGET6_V1_PRODUCER_PASS preflight_state=R07_760_L3_TARGET6_PREFLIGHT_READY sha256=0711173b953e164c20ae2ce249d8bce1220b892899d9e14308601d731678d6ba bytes=663404

python -u -B crosscheck/check_d972_r07_760_l3_target6_v1.py --self-test
R07_760_L3_TARGET6_V1_CHECKER_SELFTEST_PASS toy_member=1 toy_nonmember=1 separator_mutations=3

python -u -B crosscheck/check_d972_r07_760_l3_target6_v1.py --receipt search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json --mutations
R07_760_L3_TARGET6_V1_CHECKER_PASS preflight_state=R07_760_L3_TARGET6_PREFLIGHT_READY mutations=11 full_replay=false receipt_sha256=0711173b953e164c20ae2ce249d8bce1220b892899d9e14308601d731678d6ba
```

The ASCII GAP driver also passed its short serial selftest:

```text
.\gap.ps1 search\d972_r07_760_l3_target6_gha_driver_v1.g -ExtraArgs @('-c','D972_R07_760_L3_TARGET6_V1_SELFTEST:=true;;')
R07_760_L3_TARGET6_V1_GHA_DRIVER_PASS mode=selftest preflight_mutations=11 receipt_sha256=0711173b953e164c20ae2ce249d8bce1220b892899d9e14308601d731678d6ba bytes=663404
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

## 5. Exact GHA dispatch inputs

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

## 6. New file ledger

```text
35202  a73b78d1a9ed6faae3230bef07c24194733dee77334e8e5006c38b8d00b46ac0  search/d972_r07_760_l3_target6_v1.py
40489  e8cc6b5acaeaee88147a5ebcb3490a2a51aeaa45f73adf839df732df6ac986b1  crosscheck/check_d972_r07_760_l3_target6_v1.py
13171  c69249c63d31599b3bb3b7d91a2b6f950e83bbde2561ba405f9f4d8f7f1b9477  search/d972_r07_760_l3_target6_gha_driver_v1.g
663404 0711173b953e164c20ae2ce249d8bce1220b892899d9e14308601d731678d6ba  search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json
```

The driver is ASCII-only.  The fixed task pin used by all three code paths is
9066 bytes / SHA-256
`9fcdf2f25b724e9dbc225f417b0036e126e7b5e37a0778dab5e0299ee2f74e12`.
The v97 contamination audit consulted here is 5700 bytes / SHA-256
`ea1f16a72b4f71efde628e9d1d17d43cdb39856f8b01cb676a18c2b059f116e6`.

## 7. Grade and unresolved result

```text
BOUNDED g760 STATIC/PREFLIGHT: CROSS-CHECKED
DESTRUCTIVE MUTATIONS:        11/11 PASS
FULL PRODUCER:                 NOT RUN / UNKNOWN
FULL DIRECT CHECKER:           NOT RUN / UNKNOWN
MATHEMATICAL TERMINAL:         UNKNOWN PENDING GHA
LEAN VERIFIED:                 NO
```

Only a future producer/checker-agreed `NONMEMBER` with the full pairing replay
supports implication (2.2) for this one explicit g760 prefix and this one
target6 edge.  `MEMBER_INCONCLUSIVE` remains only survival of this L3 screen.
