# Luna reply 162: R07 760-letter commutator affine RHS v3

Date: 2026-08-26

## 1. Disposition

Implemented the requested fresh-760 producer, helper-independent checker,
single-process GHA driver, and bounded preflight certificate.  No heavy full
run, complete-D2 column generation, git operation, or GHA dispatch was made
locally.

The bounded preflight is **cross-checked**: the producer and independent
checker agree on the exact 760-letter base, all settled joint values, the
current E4 relation/onto certificate, the corrected target DAG, and seven
destructive mutations.  The 109-row/B0/B1 lane is **candidate / GHA-ready**;
it is not called cross-checked until an isolated full GHA run completes.
Nothing here is Lean-verified.

## 2. New files and immutable digests

| file | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_616_to_760_commutator_affine_rhs_v3.py` | 39385 | `db945914f2ed84329ca296e03732c6c4a16035f5181cecb683d12bdfca1f6377` |
| `search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py` | 33409 | `f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f` |
| `search/d972_r07_616_to_760_commutator_affine_rhs_gha_driver_v3.g` | 9625 | `2d0ff74f856f51857f5257c4e039253d21ef96baff7941d90d271fc8b90436e2` |
| `search/certs/d972_r07_616_to_760_commutator_affine_rhs_preflight_v3_20260826.json` | 184890 | `55752b6c1a748fb0b25a86d6fc1a0381a82b203112568b0b1963c5665cef0408` |

The GAP source is ASCII-only.  The final mathematical pin bundle is parent
commit `72d1ba034869899978fbaf1cdf85670121c703dc`:

| frozen input | bytes | SHA256 |
|---|---:|---|
| `sol/luna_task_162_r07_760_commutator_affine_rhs_v3.md` | 4053 | `8ca38afc6f30e8e6074f191a17541f508f29ba1da58d3b286ba4fcf33406ae21` |
| `sol/proof_r07_goursat_nakayama_onto_v88.md` | 4254 | `e0d8ff49963ef0cb98312e5ee288ed0744a42fd7d2dd6e0b8450439e28fe329b` |
| `sol/audit_r07_616_e4_relation_onto_v89.md` | 4388 | `0b965baa8bade54c3e3784df64fdfe6f440824518f2c21174e26122f452d4244` |
| `sol/proof_r07_joint_derived_commutator_rebase_v92.md` | 5969 | `cc56e2187fac08ffa70fe3753e200627e776b5fa591738dee5da908e4d217387` |
| `sol/proof_r07_left_right_a18_basechange_v93.md` | 4578 | `5adc49196b7ac0c9d7472f5de0c77af9919b945304f6732e8ea182899308660e` |
| `sol/proof_r07_frattini_invisible_onto_stability_v94.md` | 6506 | `fee0868727bc027d002d19200a73ac0292d76bb04d95e88553cbfa0e29942840` |

The driver additionally pins the q3 artifact (231570 bytes,
`3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`),
the frozen 157em producer (410757 bytes,
`8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc`),
and its independent checker (228980 bytes,
`08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e`).

## 3. Bounded preflight result

Serial output was:

```text
PRODUCER_AST_PASS
CHECKER_AST_PASS
R07_760_COMMUTATOR_AFFINE_RHS_V3_PRODUCER_SELFTEST_PASS base=760 terminals=6 negative=0
R07_760_COMMUTATOR_AFFINE_RHS_V3_CHECKER_SELFTEST_PASS stdlib_adapter=1 mutations=7 negative=0
R07_760_COMMUTATOR_AFFINE_RHS_V3_PRODUCER_PASS terminal=R07_760_COMMUTATOR_BASE_READY sha256=55752b6c1a748fb0b25a86d6fc1a0381a82b203112568b0b1963c5665cef0408 bytes=184890
R07_760_COMMUTATOR_AFFINE_RHS_V3_CHECKER_PASS terminal=R07_760_COMMUTATOR_BASE_READY mutations=7 full_replay=false receipt_sha256=55752b6c1a748fb0b25a86d6fc1a0381a82b203112568b0b1963c5665cef0408
```

The exact reconstructed base is

```text
base_kind       = r07_760_commutator
g               = f * y^36 * x^-108
length(g)       = 760
SHA256(g)       = 518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
exp(g)          = [0,0]
parent_616_sha  = 3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90
r               = x^108 * y^-36
```

Here signed-word SHA256 means SHA256 of canonical compact JSON, consistently
in producer and checker.  Direct replay gives `r=1` in G36, PSL(2,8), p2
source plus five cofaces, p3 source plus five cofaces, the complete E3 source,
and all five complete E4 cofaces.  Consequently the settled values of the
616- and 760-letter words agree coordinate-by-coordinate in the frozen joint
map.  The checker separately reconstructs these values and the free exponent
sums; it does not import the v3 producer.

The current E4 certificate directly replays all 11 PB4 relators, recovers all
six Q4 generators, and obtains the identity rank-6 matrix on
`Pi4[3]/Phi`.  Together with `|Q4^ab|=32`, this is the finite certificate used
by v88/v89.  The v94 cofinal-3-Frattini theorem is recorded separately as a
paper consequence: it preserves onto-ness for compatible lifts in that
cofinal finite marked 3-group category.  It does **not** construct a compatible
cofinal family and does not imply a whole mixed tower lift.

The same-base v93 side canary reconstructs the formal identity
`D_R = D_L A_q` and rejects the prescribed final-prefix mutation.  Actual
successor-chief action matrices and the five literal lambda matrices remain
`UNBUILT`.

## 4. Fresh full lane and independent replay

The producer's `--full` lane uses `g760` as `FIXED_WORD` before making any
base-dependent object.  It freshly constructs:

1. the six source words and exact inverse/source preflight;
2. B0, its dependent events, complete-block registry and recovery map;
3. the fixed 11-relator B1 block, anchor and old-qstar boundary;
4. the base row plus all 108 registered direction words;
5. every raw Fox gradient, gradient binding, formula row and reduced
   remainder;
6. the assembled/ranked target-6 affine system, raw parents, and final
   recovery map;
7. lossless old-20 comparison digests, never an imported RHS or transport.

For `R07_760_AFFINE_RHS_READY`, the checker does not trust
`all_109_rows_fresh=true`.  With no import from the v3 producer it uses the
separately pinned 157em checker chain to replay the q3 input, base/inverse,
registered seeds, source preflight, all 76 numbered base occurrences, eleven
typed base columns, B0, qstar correlation, fixed B1 and anchor, semantic
recovery, all 109 raw words/gradients/remainders, target system, direct parent
manifest, and comparison digests.  Equality of the complete reconstructed
public objects is required.  A full-only raw-gradient mutation is the eighth
destructive test.

`R07_760_AFFINE_UNKNOWN_RESOURCE` and `R07_760_AFFINE_INPUT_STOP` are checked
as typed, claim-free envelopes: no B0/B1/109 freshness, no imported RHS, no
assembled target system, no mathematical negative, and all global witness
claims false.  Unexpected `AttributeError`, `TypeError`, `KeyError`, and other
programming defects are re-raised rather than converted to an input terminal.

This lane deliberately stops at RHS readiness:

```text
registered_target6_solve_executed=false
target_affine_system_assembled_and_ranked=true
complete_D2_column_generation_executed=false
next_target_ordinal=null
```

Thus the registered full-D2 target-6 correction/separator was **not** run.
The built differential is explicitly the left-Fox presentation complex.  No
literal normalized arity/coface A.18 occurrence was built; that field is
`UNBUILT`.  The already settled ordered A.18 relation replay must not be
confused with this missing next-chief object.

Every terminal retains:

```text
full_JH_over_JPhi_complete=false
cofinal_lift=false
ihara_witness=false
actual_A18_occurrence=false
registered_108_family_is_full_universe=false
```

## 5. Exact GHA dispatch inputs

Use exactly one of the following GAP bindings with the pinned driver.

Selftest:

```gap
D972_R07_760_COMMUTATOR_AFFINE_RHS_V3_SELFTEST:=true;;
Read("search/d972_r07_616_to_760_commutator_affine_rhs_gha_driver_v3.g");;
```

Full RHS lane:

```gap
D972_R07_760_COMMUTATOR_AFFINE_RHS_V3_RUN:=true;;
Read("search/d972_r07_616_to_760_commutator_affine_rhs_gha_driver_v3.g");;
```

The full driver copies the pinned q3 artifact to its authenticated runtime
path, then launches exactly one producer and one independent checker under a
shared 18000-second budget.  It accepts exactly one of `RHS_READY`,
`UNKNOWN_RESOURCE`, or `INPUT_STOP`; producer/checker terminal, receipt SHA,
receipt byte count, sentinel and forbidden diagnostic tokens are bound
fail-closed.

The final local driver-selftest attempt overlapped the parent's simultaneous
selftest: the shared log contained one producer marker but two copies of each
checker marker, so the driver's exact-count guard correctly stopped.  No
process remained, the generated log/sentinel were removed, and the parent
ordered no further local execution.  This collision is not reported as a
final-driver PASS; an isolated parent replay is the remaining selftest step.

For context only, the preceding v1 slow-4096 lane completed on GHA run
`32870813120` with SUCCESS and its type-mismatch stop was independently
checked.  That result is not transported into the fresh 760 RHS.
