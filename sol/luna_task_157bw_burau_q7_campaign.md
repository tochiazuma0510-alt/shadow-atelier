# Luna task 157bw — versioned q=7 Burau obstruction campaign

Role: Luna implementation/computation support.  The q=5 and synchronized
joint campaigns are already running on GHA.  Build an independent, versioned
q=7 finite-obstruction campaign that can run there in parallel; do not run
local GAP and do not edit any existing producer/checker/workflow.

Authorized files only:

- `search/d972_b4_burau_fiber_v5.py`
- `search/check_d972_b4_burau_fiber_v5.py`
- `.github/workflows/d972-burau-q7-v1.yml`
- `sol/luna_reply_157bw_burau_q7_campaign.md`

Requirements:

1. Audit v4 semantics first.  Preserve the frozen 972 target/word bindings,
   the actual B4 Burau matrices and H10/H11/pentagon word tests, and the
   distinction between a genuine zero fiber (candidate B4-A obstruction),
   exhaustive all-pass (UNKNOWN), and resource/error outcomes.
2. Add prime-field q=7 support without weakening q=3/q=4 calibration gates.
   Cover all nonzero `a in F_7` that are mathematically admissible, or state
   and justify an exact preregistered subset if image size makes all six
   impossible.  Do not infer nonexistence from a cap or timeout.
3. Producer and checker must be independently implemented enough to detect
   shared mistakes; checker must reconstruct matrices/relations and receipt
   counts rather than trust producer summaries.  Add adversarial selftests.
4. GHA must use a matrix of q=7 lanes, read-only permissions,
   `persist-credentials:false`, pinned Python/dependencies, explicit memory
   and timeout bounds, always-uploaded lossless evidence, unique terminal
   markers, and fail-closed aggregation.  A zero may be promoted only after
   the independent checker passes.
5. Run only lightweight local Python/static selftests (no GAP and no large
   local search).  Report source/workflow SHA-256 values, exact commands, and
   finish with `Q7_CAMPAIGN_READY`, or give a precise mathematical or
   computational blocker.  Do not use Git, push, dispatch, or GHA.
