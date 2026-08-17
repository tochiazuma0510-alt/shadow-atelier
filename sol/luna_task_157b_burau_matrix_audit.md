# Luna task 157b — independent adversarial audit of matrix-56 campaign

Audit, but do not modify, these candidate files after task 157 completes:

- `search/d972_b4_burau_matrix_v1.g`
- `.github/workflows/d972-burau-matrix-v1.yml`

Write only `sol/luna_reply_157b_burau_matrix_audit.md`.  Do not run local GAP,
commit, push, or dispatch.  Static Python/YAML/text checks are allowed.

Give a strict PASS/BLOCKER verdict.  A PASS means the files are safe for the
parent to commit and launch as an exact finite-obstruction campaign, not that
they settle A/B.

Audit at least:

1. The 56-dimensional block representation is genuinely the full faithful
   36-dimensional roof permutation module plus five distinct literal A.18
   4-dimensional blocks.  Check field encoding at GF(3), GF(4), and GF(5),
   multiplication orientation, block positions, and no scalar/projective loss.
2. The producer computes `H'`, the surjective restricted roof map, and its
   entire kernel with exact GAP finite-group APIs.  Reject guessed kernel
   order, bounded words, capped BFS, random samples, representative-only
   fibers, or any success after a resource/API stop.
3. Every one of the frozen 972 roofs is bound to its exact target key and
   common-word provenance; every fiber is the full coset by the enumerated
   kernel; the five blocks and paper-convention defect match the audited v2
   semantics.  Check negative controls and receipt completeness.
4. The q=3/q=4 expectations are calibration gates only and exactly reproduce
   the frozen values.  q=5 must not assume H/H'/K/fiber counts.  A q=5 zero
   fiber is only a candidate; all-pass is UNKNOWN.
5. Workflow dependency order really prevents q=5 before both calibrations,
   q=5 a=2/a=4 are independent matrix jobs, inputs are closed, pinned download
   hashes are unchanged, checkout does not persist credentials, shell status
   and GAP diagnostic gates cannot be bypassed, and all artifacts/markers are
   attempt-unique and fail-closed.
6. Recompute file hashes, parse the YAML, run non-GAP static/selfhash checks,
   inspect the exact git diff, and list every remaining runtime uncertainty.

If blocked, cite exact file/line locations and propose the smallest correction.
