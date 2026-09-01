# Luna reply 461: A0 rank-68 checkpoint resume v7

Status: **IMPLEMENTED / BOUNDED GATES PASS / PRODUCTION NOT RUN**

## Frozen artifact authentication

The five required Task450 artifact files matched their prescribed byte counts and SHA-256 values. The checker log contained `R07_A0_ACTUAL_TAU_FREE_RANK_LADDER_V6_CHECKER_PASS`; `run.log` contained `R07_A0_RANK51_CHECKPOINT_RESUME_V6_DRIVER_PASS`.

The copied checkpoint is byte-identical to the production output. Its canonical v3 state seal independently recomputes to `d900bbb4f3b69ee66f9c2f4000b169f69a9202091a69fe0bbb8d33c4ae061537`, with rank `68`, accepted count `25`, round `27`, and reason `UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit`. This is 17 rises beyond rank 51 and is not COMMON; lift/fake/Ihara remain unclaimed.

## Exact outputs

| path | bytes | SHA-256 |
|---|---:|---|
| `search/certs/d972_r07_a0_actual_tau_free_rank68_checkpoint_v1.json` | 33015 | `73ad85624d079d01ecc824ab6adc699c51b0dabfddcc36c0f7d2bd4384f7d5a4` |
| `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py` | 3653 | `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1` |
| `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v7.g` | 2844 | `4aefd6adf6157bcabcaef4e9c37e8c1713a8440801206aacb81e492bc0a213d8` |

## Transport/checker boundary

- The driver pins the unchanged v3 producer, v7 checker, and rank-68 checkpoint; requires the external v7 preamble; copies and reauthenticates a fresh `ci/out` resume input; requests 7,200 seconds, 4.8 GB RSS, and at most 64 further rises; and launches exactly one production producer process followed by the checker.
- The checker exact-pins and delegates the complete v6 checker. Independently it authenticates the frozen checkpoint outer pin, v3 schema/binding, canonical seal, fields/reason, and all 25 source records. It requires those records as the exact ordered prefix and enforces rank/count/round monotonicity from `(68,25,27)`.

## Bounded gates

Passed:

1. external artifact byte/SHA and marker authentication;
2. repo-external-cache `py_compile` for the v7 checker;
3. checker `--self-test`, rejecting checkpoint-seal, prefix, rank, count, and round mutations;
4. independent checkpoint canonical-seal/field replay;
5. static driver inspection for one production process, resume input, caps, pins, fresh paths, and absence of production SELFTEST/FIXTURE or universe changes.

No local production, GHA, network, workflow edit, git, commit, push, closure rebuild, eager store, or actor-adapted rebase was performed.

## Parent adoption and production dispatch

The parent repeated `py_compile`, the v7 self-test, exact pin checks, and the
one-process/resume/cap/static scans.  The five synthetic mutations were again
rejected.  A local full artifact replay reached the known Windows
same-handle-identity platform stop inside the inherited Task198 runtime; no
mathematical or v7-checker failure was observed, and the full replay remains
assigned to the Linux production job.

The four outputs were committed and pushed at
`dd67f12b0ee4f022061df27ed396ad3d3a37f264`.  The parent dispatched
`gap-run.yml` with that exact source as run `33524681526`, job `99912387760`:

```text
script=search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v7.g
preamble=D972_R07_A0_RANK68_CHECKPOINT_RESUME_V7_RUN:=true;;
out_dir=ci/out
timeout_min=150
with_pquot_packages=false
```

The job entered setup on 2026-09-02 JST.  Dispatch does not change the A0
numerator; the first possible promotion is an exact v7 checker PASS on a
COMMON terminal.
