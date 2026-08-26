# Luna reply 164: g760 L3 target6 checkpoint/resume v2

Date: 2026-08-26
Role: Luna / versioned implementation and bounded mechanical audit

## 1. Result

The task164 resume lane is implemented.  It authenticates the exact
`32901384400` resource-stop artifacts, accepts only the inherited candidate
prefix `[2,3,4,5,6,7,8]` with `start_j=9`, and recomputes all of `j=9` from
D2 relator 1.  No lost relator-1-through-6 state is claimed or reused.

The producer writes an immutable cumulative checkpoint after each fully
completed `j`.  A resource stop preserves completed checkpoint files and does
not infer anything about the interrupted `j`.  A later invocation can resume
only from the exact `next_j` authenticated by the full SHA/byte checkpoint
chain.

No local full computation, parallel Python/GAP, git operation, or GHA dispatch
was performed.  Task163/v1 files, `provenance/CLAIMS.md`, proofs, and existing
certificates were not changed.

## 2. New versioned files

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_760_l3_target6_resume_v2.py` | 35068 | `9f6f8c2d3d3dbbc69373e1413b5d47a8893d6be62b228dc04ecd522a4fa51238` |
| `crosscheck/check_d972_r07_760_l3_target6_resume_v2.py` | 63772 | `7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365` |
| `search/d972_r07_760_l3_target6_resume_gha_driver_v2.g` | 17443 | `6241566df743069b7da6924e7c2facd766ef058b622f5e44f87c90f1d5392935` |
| `search/certs/d972_r07_760_l3_target6_prior_run32901384400_v1_20260826.json` | 3239 | `1c739559eee368ba676c694960be21db94d6bc2292a6136d89b97bedfef3e15b` |
| `search/certs/d972_r07_760_l3_target6_prior_run32901384400_producer_v1_20260826.log` | 164 | `fc3901c29f958e216e17ba175be4857ee26cc140f3f809f0e29833b636ccd436` |
| `search/certs/d972_r07_760_l3_target6_resume_preflight_v2_20260826.json` | 7986 | `272d4c4e91bb0234d49316277b354b722dfcb1366e47e9bf00d745469a1c1a94` |

The GAP driver contains only ASCII bytes, ends in LF, and has no trailing
whitespace.  The two prior-run certificates are byte-for-byte copies of the
external downloads: one LF, no CR, and the preregistered hashes above.

Task pin used by all v2 components:

```text
sol/luna_task_164_r07_760_l3_target6_resume_v2.md
bytes=5292
sha256=761359bda0fc14543ab9266ec61139006403525d828811bb2af5d27d34ccfc9d
```

## 3. Prior stop authentication

Both producer and checker independently enforce:

```text
run_id=32901384400
head_sha=c1e7eb8fcd08676d5a6efad82add2c1c832a22c0
schema=d972-r07-760-l3-target6/v1
mode=full
terminal_token=R07_760_L3_TARGET6_UNKNOWN_RESOURCE
result.requested_seconds=10200.0
result.stage=j=9:D2-relator-7
result.mathematical_membership_claimed=false
result.mathematical_nonmembership_claimed=false
static.base.base_kind=r07_760_commutator
static.base.sha256=518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
```

They also replay the v1 canonical self-digest and require the producer log to
be exactly the single marker binding the 3,239-byte receipt.  The inherited
`j=2,...,8` statement is therefore recorded only as
`producer_control_flow_candidate_only`; it is never called independently
cross-checked.

## 4. Producer/checkpoint contract

The v2 producer pins and imports the frozen v1 producer core only after its
53,284 bytes and SHA-256 have been authenticated.  It then calls the frozen
static construction afresh.  The full static object, v1 pin manifest, v2 pin
manifest, prior-run binding, g760 base, target, legal rows, PB4 relators, and
Jennings bases are all digest-bound into every v2 receipt and checkpoint.

The only fresh order is

```text
9, 10, 11, 12
```

with the same first-`NONMEMBER` rule.  Checkpoint names are fixed:

```text
d972_r07_760_l3_target6_resume_v2_j9.json
d972_r07_760_l3_target6_resume_v2_j10.json
d972_r07_760_l3_target6_resume_v2_j11.json
d972_r07_760_l3_target6_resume_v2_j12.json
```

Each checkpoint contains the cumulative full public `compute_j_bfs` rows,
`completed_j_prefix`, `next_j`, `first_nonmember_j`, current-row digest,
previous checkpoint path/SHA/bytes, static and prior bindings, false global
claims, and a canonical self-digest.  Loading a checkpoint requires an exact
prefix of `[9,10,11,12]`, adjacency of `next_j`, byte-authenticated prior files,
and cumulative-row equality throughout the chain.

Relator-level echelon state is deliberately absent in v2.  Therefore an
interrupted `j` is always restarted at relator 1.  A completed `NONMEMBER` row
contains the producer's direct 649,539-row separator replay; producer-only
grade nevertheless remains `CANDIDATE`.

## 5. Structurally independent checker

The v2 checker imports neither producer.  Its only dynamic arithmetic import
is the pinned older seed-span module.  It independently reconstructs E4,
g760, target6, the Schreier legal rows, PB4 relators, and Jennings projection.
The v1 producer pathname is authenticated as inert data for the prior
control-flow pin, never imported.

For every freshly completed `j` present in a receipt, it enumerates all

```text
59049 x 11 = 649539
```

translated D2 rows, reconstructs ranks and the decision independently, and
checks the entire immutable checkpoint chain.  For a `NONMEMBER`, it separately
replays both its own separator and the producer separator against every legal
and translated D2 row and against the target.

The checker intentionally does not recompute `j=2,...,8`.  Agreement at one
fresh `j>=9` is sufficient for the branch-local nonmembership implication, but
does not upgrade the inherited prefix.

## 6. Bounded serial audits

The clean audit base was HEAD
`4418e767508b075b7cfb2d203092e3f3c5d5b5be`, with only the task164 prospective
files overlaid.  Windows tar mangled the UTF-8 pathname `docs/対話帳.md`; the
clean committed file was reintroduced under its correct pathname only after
its pinned 234,377 bytes/SHA were checked.  This was a pathname compatibility
repair, not a content substitution.  The locally dirty CLAIMS file was not
used.

Producer unit selftest:

```text
R07_760_L3_TARGET6_RESUME_V2_PRODUCER_SELFTEST_PASS prior_artifacts=2 inherited_prefix=7 start_j=9 checkpoint_mutations=6 relator_state=absent
```

Independent checker unit selftest:

```text
R07_760_L3_TARGET6_RESUME_V2_CHECKER_SELFTEST_PASS imports_producer=false prior_artifacts=2 separator_mutations=3 checkpoint_mutations=6
```

Clean producer preflight:

```text
R07_760_L3_TARGET6_RESUME_V2_PRODUCER_PASS preflight_state=R07_760_L3_TARGET6_RESUME_V2_PREFLIGHT_READY grade=CANDIDATE checkpoints=0 sha256=272d4c4e91bb0234d49316277b354b722dfcb1366e47e9bf00d745469a1c1a94 bytes=7986
```

It was byte-equal to the committed prospective preflight certificate.

Independent preflight replay:

```text
R07_760_L3_TARGET6_RESUME_V2_CHECKER_PASS preflight_state=R07_760_L3_TARGET6_RESUME_V2_PREFLIGHT_READY mutations=17 full_replay=false receipt_sha256=272d4c4e91bb0234d49316277b354b722dfcb1366e47e9bf00d745469a1c1a94
```

The 17 destructive tests comprise eight preflight/static/prior/scope
mutations, three sparse-separator tests including the nonmonotone-pivot
counterexample, and six checkpoint mutations:

```text
skip_prefix
wrong_next
row_basis
prior_binding
claim_flip
self_digest
```

Parent clean-clone driver selftest:

```text
R07_760_L3_TARGET6_RESUME_V2_GHA_DRIVER_PASS mode=selftest producer_processes=1 checker_processes=0 checkpoint_mutations=6 grade=CANDIDATE
```

All bounded audits were serial.  No Python or GAP process remained active at
handoff.

## 7. Clean-checkout runtime dependency audit

The driver authenticated every row below in the prospective clean checkout.
`yes` means that the exact bytes existed either in clean HEAD or in the
authorized task164 overlay.

| runtime or packaging path | bytes | SHA-256 | present |
|---|---:|---|---|
| `search/d972_r07_760_l3_target6_resume_v2.py` | 35068 | `9f6f8c2d3d3dbbc69373e1413b5d47a8893d6be62b228dc04ecd522a4fa51238` | yes |
| `crosscheck/check_d972_r07_760_l3_target6_resume_v2.py` | 63772 | `7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365` | yes, packaging only in producer driver |
| `search/certs/d972_r07_760_l3_target6_resume_preflight_v2_20260826.json` | 7986 | `272d4c4e91bb0234d49316277b354b722dfcb1366e47e9bf00d745469a1c1a94` | yes |
| prior receipt certificate | 3239 | `1c739559eee368ba676c694960be21db94d6bc2292a6136d89b97bedfef3e15b` | yes |
| prior producer-log certificate | 164 | `fc3901c29f958e216e17ba175be4857ee26cc140f3f809f0e29833b636ccd436` | yes |
| `sol/luna_task_164_r07_760_l3_target6_resume_v2.md` | 5292 | `761359bda0fc14543ab9266ec61139006403525d828811bb2af5d27d34ccfc9d` | yes |
| `search/d972_r07_760_l3_target6_v1.py` | 53284 | `7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde` | yes |
| `search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json` | 663780 | `4d305a1af415ffb5acf1d029a69c1b720961fce88dc86575d8fde2d504a787ab` | yes |
| `sol/luna_task_163_r07_760_l3_target6_v1.md` | 9066 | `9fcdf2f25b724e9dbc225f417b0036e126e7b5e37a0778dab5e0299ee2f74e12` | yes |
| `provenance/CLAIMS.md` (clean HEAD) | 66635 | `174ddbb50d1579c9373482552759ed2ec822846f1dd83c8d73b13c652ae77f64` | yes |
| `docs/対話帳.md` | 234377 | `a5eadcc04468b593e0a1c7896409a59b55c6442ca489df6a91aac60d6e128a06` | yes |
| `sol/proof_r07_joint_derived_commutator_rebase_v92.md` | 5969 | `cc56e2187fac08ffa70fe3753e200627e776b5fa591738dee5da908e4d217387` | yes |
| `sol/audit_r07_uniform_explicit_lift_checkpoint_v95.md` | 5324 | `12877306446bcfe8b57b01751c929bdee78d15300c4f90a8311764ff2d7eeeae` | yes |
| `sol/luna_task_162_r07_760_commutator_affine_rhs_v3.md` | 4053 | `8ca38afc6f30e8e6074f191a17541f508f29ba1da58d3b286ba4fcf33406ae21` | yes |
| `sol/luna_reply_162_r07_760_commutator_affine_rhs_v3.md` | 8833 | `70ebb7bf433fafd77dc828efe5f71b9dd6dc982e7682a4c6397695b6a2e6bcf5` | yes |
| `search/certs/d972_r07_616_to_760_commutator_affine_rhs_preflight_v3_20260826.json` | 184890 | `55752b6c1a748fb0b25a86d6fc1a0381a82b203112568b0b1963c5665cef0408` | yes |
| `ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json` | 231570 | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` | yes |
| `search/d972_b345_seedspan_triple4_v1.py` | 535219 | `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29` | yes |

The immediate driver executes only the v2 producer.  The checker and seed-span
source are authenticated packaging for later independent replay; the driver
does not execute either.

## 8. Exact driver invocations

Bounded GHA selftest input:

```gap
D972_R07_760_L3_TARGET6_RESUME_V2_SELFTEST:=true;;
D972_R07_760_L3_TARGET6_RESUME_V2_USE_PYTHON3:=true;;
Read("search/d972_r07_760_l3_target6_resume_gha_driver_v2.g");;
QUIT_GAP(0);;
```

Initial producer-only full input:

```gap
D972_R07_760_L3_TARGET6_RESUME_V2_RUN:=true;;
D972_R07_760_L3_TARGET6_RESUME_V2_USE_PYTHON3:=true;;
Read("search/d972_r07_760_l3_target6_resume_gha_driver_v2.g");;
QUIT_GAP(0);;
```

The driver command is fixed to:

```text
python3 -u -B search/d972_r07_760_l3_target6_resume_v2.py --full --start-j 9 --seconds 21000 --checkpoint-dir ci/out/d972_r07_760_l3_target6_resume_v2_checkpoints --output ci/out/d972_r07_760_l3_target6_resume_v2.json
```

It runs exactly one Python process and zero checker processes, uses the frozen
5,600 MiB producer RSS cap, and has a 21,600-second outer timeout/margin.  A GHA
job timeout above 360 minutes is therefore required; 370--380 minutes is the
recommended wrapper range with at least 12 GiB available memory.

The upload step should preserve these exact paths:

```text
ci/out/d972_r07_760_l3_target6_resume_v2.json
ci/out/d972_r07_760_l3_target6_resume_v2_producer.log
ci/out/d972_r07_760_l3_target6_resume_v2_timing.txt
ci/out/d972_r07_760_l3_target6_resume_v2.ok
ci/out/d972_r07_760_l3_target6_resume_v2_checkpoints/*.json
```

The driver prints SHA/bytes for the receipt, producer log, timing ledger, and
every completed checkpoint.  It validates exclusive terminals, false claims,
the inherited-prefix label, start index, checkpoint prefix/manifest bindings,
and `producer_processes=1`, `checker_processes=0`, `grade=CANDIDATE`.

For a later resume, the producer additionally accepts only an exact latest
checkpoint in the same directory, for example:

```text
--resume-checkpoint ci/out/d972_r07_760_l3_target6_resume_v2_checkpoints/d972_r07_760_l3_target6_resume_v2_j9.json
```

and derives `next_j=10` from the authenticated chain.  Arbitrary skip values
and terminal checkpoints are rejected.

## 9. Claim boundary

```text
inherited j2..8 = producer control-flow candidate only
fresh resumed output = candidate until independent checker agrees
MEMBER != actual A18 lift
NONMEMBER kills one g760 prefix only
no fake / no cofinal lift / no Ihara witness declared by the implementation
```

No mathematical full terminal was produced in this task.  The preflight and
schema are independently checked mechanical assets; there is no Lean
verification claim.
