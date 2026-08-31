# Luna task 435 - actual A0 quotient-dual profile and tau gate

Task434 v1 is a rejected skeleton for production because it unconditionally
returns `UNKNOWN_RESOURCE:compact_runtime_adapter` and its triangular fixture
keys are not the actual v12 raw ABI.  Do not patch or dispatch that file.
Create a minimal versioned actual-data profiler which answers the one question
needed before the full weighted oracle: what is the first real physical dual,
and does it contain any of the three global `tau` coordinates?

## 1. Allowed outputs

Create only:

1. `search/d972_r07_a0_actual_dual_weight_profile_v1.py`
2. `crosscheck/check_d972_r07_a0_actual_dual_weight_profile_v1.py`
3. `search/d972_r07_a0_actual_dual_weight_profile_gha_driver_v1.g`
4. `sol/luna_reply_435_r07_a0_actual_dual_weight_profile_v1.md`

Do not modify task434, v12, task179, a workflow, v220, or any running A0
file.  No local production run, commit, push, dispatch, download, or release.

## 2. The runtime adapter already exists in the pinned v12 source

Import the exact pinned v12 module.  Reuse the bootstrap at v12 `run`, around
the current source lines 432--433, without copying the owner:

```python
t413 = v12.v3.load(v12.v3.T413, "task435_task413")
base = t413["bound_module"](t413["BASE"], "task435_base")
receipt = t413["load_json"](base, t413["JOINT"])
q3 = t413["load_json"](base, t413["Q3"])
pres = base["compact"](receipt, q3)
core = base["load_task198_core"]()
roof = t413["load_json"](base, base["ROOF"])
acceptance = t413["load_json"](base, base["ACCEPTANCE"])
v12.need(base["acceptance_ok"](acceptance), "acceptance_v2_contract")
authority = types.SimpleNamespace(receipt=roof)
layout = base["load_bound_module"](base["TASK379"], "task435_layout")["validate_layout"]
ledger = layout(core, authority)
runtime = core.Runtime(authority, core.Meter(dict(core.CAPS)))
owner, g760, model = base["direct_physical_owner"](runtime)
p176 = base["load_bound_module"](base["TASK176"], "task435_p176")
q = v12.Quotient(owner, p176, runtime.e3, runtime.e4)
target = q.transform(t413["target_row"](
    base, owner, runtime.old, runtime.e3, runtime.e4, g760, model))
```

The task434 claim that this adapter is unavailable is therefore false.  Pin
and check `len(pres["relators"]) == 44`, the accepted layout, and the exact
target digest.

## 3. Build only the cheap actual prefix

Use one fresh v12 `PackedEchelon`; do not create an occurrence echelon.

1. For each of the 44 literal compact relators, compute

   ```python
   occurrence = v12.seed_v12(model, runtime.old, owner, p176, q, word)
   physical = v12.aggregate(occurrence)
   ```

   and insert the physical identity-conjugator column with literal source
   metadata.  This is sound because each is an actual correction column; no
   descendants or occurrence closure are claimed.
2. Repeatedly obtain the exact physical dual/remainder and run only the
   existing `q.action_support_hits` over
   `runtime.old.pure_relations(4)[5:11]`.  Directly replay every accepted
   action row with `v12.action_row`.  Continue until the six-action oracle is
   empty or a registered resource cap is reached.
3. Emit the final real quotient dual and remainder.  This is a profile, not a
   membership result.  If the target already reduces to zero, emit
   `POSITIVE_PREFIX_CANDIDATE` and the full existing v12 strict replay input;
   do not promote it inside this task.

No task176 `Q0`/Delta roster, weighted fibre, adjoint expansion, PB3/PB4
enumeration, or occurrence checkpoint is loaded.

## 4. Required actual profile

Parse every dual key through the real v12 key ABI.  Record:

- identity compact attempted/retained count;
- physical rank, payload nnz, target remainder nnz, and dual support;
- support count by exact block and label;
- the coefficients of PB3 block-1 `tau`, PB3 block-2 `tau`, and PB4 block-3
  `tau` (missing means zero);
- both normalized exponent coefficients;
- v404 rounds, candidates, retained rows, and proof that the final
  accumulator was empty;
- target, remainder, dual, every retained source, and framed digests needed
  for independent replay; and
- RSS/elapsed time at least every 60 seconds.

Use the real `q.parse` format.  Do not search for byte substring `tau` and do
not use task434's fake `Q<block><label>:` format.

The only ordinary terminal is `PROFILE_READY`.  Resource caps are
`UNKNOWN_RESOURCE` with a durable checkpoint.  Neither terminal is A0
NONMEMBER.  The checker must reject any result calling itself COMMON,
NONMEMBER, fake, or Ihara.

## 5. Independent checker

Without importing the profiler:

1. repeat the pinned v12 bootstrap and target construction;
2. rebuild all 44 identity compact columns and the selected six-action rows;
3. reconstruct the physical echelon and exact final remainder/dual;
4. prove `dual(basis)=0`, `dual(remainder)!=0`, and re-run the complete v404
   support accumulator to confirm it is empty; and
5. parse and compare every reported label/tau/exponent count.

The checker is allowed to import the same pinned v12 mathematical owner, but
must not import the profiler or trust its row/formula summaries.

## 6. Bounded local gates

Run only compile, import/bootstrap-free fixtures, real-key parser fixtures
using v12 constructors, a toy six-action exhaustion, semantic mutations for
one omitted tau and one omitted action row, checker self-test, reconstructed
GAP command, and `git diff --check`.  Do not load the actual runtime locally.

The GHA driver uses a 1,800-second window and 4.8 GB RSS cap, prints progress,
requires the external preamble
`D972_R07_A0_ACTUAL_DUAL_WEIGHT_PROFILE_V1_RUN:=true;;`, and invokes the
independent checker.  Report exact pins and a realistic expectation: this
profile should be much smaller than the rank-1655 physical probe because it
has only 44 identity columns plus dual-active v404 rows.
