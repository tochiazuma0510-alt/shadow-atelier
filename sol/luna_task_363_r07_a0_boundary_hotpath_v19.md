# Luna task 363 - A0 boundary hot path v19

Create only:

- `search/d972_r07_history_free_positive_fast_resume_v19.py`
- `crosscheck/check_d972_r07_history_free_positive_fast_resume_v19.py`
- `search/d972_r07_history_free_positive_fast_resume_gha_driver_v19.g`
- `sol/luna_reply_363_r07_a0_boundary_hotpath_v19.md`

No execution, GHA, git, SELFTEST, mutation, fixture, retry, or broad
refactor.  Preserve every v18 correctness/checkpoint patch and the frozen
v13 arithmetic.

The completed production run measured 8,000,756 boundary pairs after about
75 minutes total, of which 2,421 seconds were immutable light-base startup.
The internal wall is 10,800 seconds.  Raising the pair cap alone cannot make
the present route finish inside that wall.

Apply only these semantics-preserving hot-path changes at unique sites:

1. In each boundary descriptor, validate `h_inverse*h=1` and
   `h*h_inverse=1` once at descriptor construction.  Remove the second
   per-pair multiplication used only to recheck `t*h=g`; retain
   `t=g*h_inverse` exactly.
2. In each persistent fork worker, memoize decoded group elements by the
   exact `(block,raw_blob)` key across epochs.  This is only a decode cache;
   coefficients, descriptors, duals and accumulator entries remain fresh.
   Do not cache a mathematical terminal or a correlation result.
3. In the positive-search loop, pass the already computed target remainder
   and solution DAG node into dual construction, avoiding the immediately
   repeated identical `reducer.reduce(target)`.  Replay equality before use.
4. Raise only `boundary_pairs` to `500_000_000` so the 10,800-second wall,
   not another artificial semantic count, is the limiting resource.
5. Extend the existing 60-second producer progress line with current
   `boundary_pairs`, `candidate_words`, `retained_columns` and DAG node count.
   No extra scan may be performed to print it.

The independent checker must remain independent and pin the v19 producer.
If its corresponding positive replay has the same per-pair inverse canary,
hoist that canary in the same mathematical manner; otherwise do not change
its arithmetic.  UNKNOWN remains nonpositive.  Resource checkpoint output
must remain replayable and bind the v19 code identity.

The ASCII driver must pin exact final sizes/SHA, use distinct v19 outputs,
make one producer and one checker call, and preserve the v18 fail-closed
terminal/checkpoint behavior.  Report each exact replacement and any omitted
non-unique optimization.  Do not claim a speedup before execution.
