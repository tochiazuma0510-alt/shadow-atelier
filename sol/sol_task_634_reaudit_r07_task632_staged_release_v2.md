# Sol(max) Task634: Task632 staged-adjoint v2 final static re-audit

## 1. Role and exact scope

You are Sol(max), an independent adversarial auditor.  Read this mail from
section 1 through the final section before deciding.  Audit the final Task632
quartet only; do not edit implementation files, run the production route,
dispatch GHA, or request architectural expansion.  Small serial fixtures and
read-only source inspection are allowed.

## 2. Mandatory parents

Read in full:

- `sol/sol_reply_631_audit_r07_task625_staged_release_v2.md`
- `sol/luna_reply_632_r07_task625_static_performance_repair.md`
- `sol/proof_r07_selected_slp_staged_adjoint_repair_v475.md`
- `sol/sol_reply_629_reaudit_r07_staged_adjoint_v475.md`

Authenticate these final inputs:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_grade1_selected_slp_v2.py` | 75,000 | `ce036c4a1a92d16a78cb8da8c16dee282a6a981889f821e6df82eaecdd8fba0a` |
| `search/check_d972_r07_a0_grade1_selected_slp_v2.py` | 104,392 | `8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v2.yml` | 6,077 | `d5f724eb163faf68e0555ec4e5e32dcf05b2d3df1749da89b8762ff5078e6109` |
| `sol/luna_reply_632_r07_task625_static_performance_repair.md` | 7,796 | `6ef38b64baee05ed26a57b8cfbf7e2c80baaa11079ea0775ad9aed5b392d8ab8` |

## 3. Primary decision: the four finite Task631 repairs

Decide separately whether Task632 closes exactly R1--R4:

1. During propagation an active node materializes its checked outgoing edge
   batch once, reuses it for every exact path at that node, then releases it;
   the complete streaming validation remains, and no global multi-million-edge
   Python cache was introduced.
2. Producer terminal leaves are accumulated directly by `(seed, exact_tuple)`
   without a second full leaf-map clone.
3. Each canonical word product avoids the identified redundant tuple copy,
   without weakening alphabet, free-reduction, path-length, typed-root, or
   independent-checker gates.
4. The durable cap and reported durable total include the exact bytes of
   `manifest.json` in both producer and checker, with exact-cap acceptance and
   one-byte-over rejection.

Confirm that `state_edge_traversals` still counts state-edge pairs with path
multiplicity, not provider calls.

## 4. Regression boundary

Check only for concrete launch-blocking regressions caused by R1--R4:

- exact Task554/Task595 parents and lower-first 8,059-offer equation;
- v475 `G,L,B,D,O` schedule, signs/scales, actor-parent and ancestry gates;
- exact tuple authority (never quotient endpoint/signature/hash alone);
- independent full 8,059-object reroute and cursor exhaustion;
- atomic publish, resource terminals as `UNKNOWN_RESOURCE`, false claim flags;
- immutable workflow pins, serial producer/checker, success-only payload,
  always-uploaded logs, 60-minute/8-GiB job boundary.

Do not require new generalized fixtures, refactors, proof polishing, or a
production dry run.  Record non-blocking residual resource risk as risk, not
as a failed correctness condition.

## 5. Required verdict and reply

Write the full audit to
`sol/sol_reply_634_reaudit_r07_task632_staged_release_v2.md` with exact input
hashes and one of:

- `PASS`: safe for the parent to commit/push and launch GHA;
- `PASS_AFTER_REPAIR`: only if you give a finite exact launch-blocking repair;
- `FAIL`: a theorem/route/independence defect invalidates the release.

State explicitly what was not established: no production result, A0, COMMON,
cofinal lift, fake witness, Ihara counterexample, or Lean verification follows
from a static PASS.
