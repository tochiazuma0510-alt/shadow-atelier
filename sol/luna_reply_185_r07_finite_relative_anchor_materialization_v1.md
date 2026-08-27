# Luna reply 185 — finite relative-anchor materialization

Date: 2026-08-27
Role: bounded mechanical implementation and static audit only.

## Numbered dispositions

1. **Objective/claim boundary:** Implemented the v149/v150 boundary. The
   receipt separates the word-bearing task176 structural state from the
   arithmetic no-S coset and never compares g760 with identity or a roof row.
2. **Authorized deliverables:** Created only the four implementation/fixture
   files and this reply. The checked-in JSON is the immutable local-execution
   guard fixture.
3. **Frozen inputs:** Producer and independent checker authenticate v149/v150/
   v153 (11,107 bytes, SHA-256
   `d5b4e8ed6af14094f309e0fc2dda73cc8e4ff2de1690a518a1c753f0a8829762`),
   v154 (6,976 bytes, SHA-256
   `bdb9ae86dcd490788854c9c1b95a3c6709ee3a0feebfeb91528ae876003333e8`),
   task157ee, q3/joint receipts, E3/E4 arithmetic, task176 source/
   checker/driver/task/record, and the frozen g760 source by exact bytes and
   SHA-256 before parsing input receipts.
4. **Producer:** Added canonical g760 reconstruction and explicit Gamma/
   Frattini/factor gates. v154 is authenticated, but the available task176
   API does not expose the full stable-derived R provenance, corrected
   word-bearing relators, marked `kappa` data, and the g760 C coordinate needed
   to build C. Production therefore emits only typed `UNKNOWN_INPUT` with
   STATIC_STOP; Q0 is never relabelled as G/R.
5. **Quotient/selector:** The v150 right-correction convention and v152
   sparse mod-3 Schreier primitive remain implemented for the bounded toy.
   No production C tree, g760 C coordinate, or arithmetic quotient coordinate
   is fabricated; v154 remains pinned as the governing repair contract.
6. **Arithmetic inventory:** q3/joint and direct g760 records are rejected as
   roof-only, missing F-component, missing quotient map, or unnamed-basepoint
   candidates. Production comparison is exactly
   `UNKNOWN_INPUT:ARITHMETIC_NO_S_COSET_NOT_AUTHENTICATED`.
7. **Checker:** Helper-nonshared checker independently rebuilds g760, the
   nonabelian toy residual/selector replay, and the bounded Schreier primitive;
   it checks Q0 table counts explicitly, rejects any Q0/G/R swap, and
   fail-closes rather than accepting an incomplete R/kappa/C receipt.
8. **SELFTEST:** Bounded toy replay covers every toy group element and all 19
   destructive-control names; no 708,588-state production quotient is used by
   SELFTEST. The checked-in fixture remains `UNKNOWN_RESOURCE`.
9. **Driver/terminals:** ASCII-only serial GAP driver has exactly SELFTEST and
   PRODUCTION bindings, pipefail, 6 GiB virtual-memory cap, bounded timeout,
   stale-output rejection, exact marker checks, and no checkpoint fabrication.
   Production expects producer/checker agreement on
   `UNKNOWN_INPUT`; arithmetic comparison remains the exact typed UNKNOWN
   input. `GHA dispatched=false`.

## Static verdict

**STATIC STOP / GHA NOT DISPATCHED.** v154 proves the direct-factor route,
but the authenticated task176 API currently exposes only Q0=1,469,664 and
does not expose enough word-bearing stable-derived/R/kappa data to materialize
the 708,588-state C tree safely. It also lacks authenticated corrected kernel
relators and a g760 C coordinate. Production emits typed `UNKNOWN_INPUT`; the
Q0/G/R destructive swap is rejected, and no formation-purified witness is
declared.

## Exact bytes / SHA-256

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_finite_relative_anchor_v1.py` | 21,137 | `72e97af20f7cfd7a8da6c9b21a91846df7d906784408d8812d17a94e26715a2c` |
| `crosscheck/check_d972_r07_finite_relative_anchor_v1.py` | 16,317 | `fddd630e8cd12d721fa65efd646614335eaa59aab10d3e7ff28a74b4aaa77a97` |
| `search/d972_r07_finite_relative_anchor_gha_driver_v1.g` | 4,839 | `e698f210f4332e0c8e269ffdb39349e6a0f2a0f7991506cbb095c8ff64468512` |
| `search/certs/d972_r07_finite_relative_anchor_preflight_v1_20260827.json` | 309 | `ef57eca45acb43aa72a5e6e75424812e9b8956833f99ac3d6a83d297a8952829` |
| `sol/luna_reply_185_r07_finite_relative_anchor_materialization_v1.md` | self-referential | not listed |

## Generic gap-run.yml preamble

Parent-owned dispatch template (not dispatched here):

```text
gh workflow run gap-run.yml --ref <bundle-commit> -f script=search/d972_r07_finite_relative_anchor_gha_driver_v1.g -f preamble='D972_R07_FINITE_RELATIVE_ANCHOR_V1_MODE:="SELFTEST";;' -f out_dir=ci/out -f timeout_min=10 -f with_pquot_packages=false
```

No Python, Node, GAP, git, or GHA was run locally.

task176 residual materialization only
arithmetic comparison scope explicitly typed
direct task179 route remains independent
no fake / cofinal lift / Ihara witness declared
