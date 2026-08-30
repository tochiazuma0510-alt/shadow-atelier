# Luna task 427 — v9 bootstrap namespace fix

## Actual GHA finding and scope

Task426/v8 passed its bounded fixtures and three-point memory audit, but fresh
GHA run `33317727481` (commit
`b7225a9d59495e19ab8a2d146a473e9254a91f62`, job `99274129809`) stopped before
preflight with the fail-closed artifact

```json
{"status":"UNKNOWN","a0":{"status":"UNKNOWN","reason":"'load'"}}
```

No search, checkpoint, boundary closure, candidate, fake or witness result was
produced.  The direct cause is one bootstrap namespace family at v8 `run`: the
task413 wrapper `load_json(base, rel)` was passed `t413`, which has no `load`,
and the following compact call also incorrectly asks `t413` for `compact`.
Both operations belong to the pinned BASE namespace.

Make a versioned v9 patch containing only this namespace correction.  Preserve
all task426/v8 memory fixes, quotient/search logic, resource policy and claim
boundaries unchanged.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_v9.py`;
2. `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v9.py`;
3. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v9.g`;
4. `sol/luna_reply_427_r07_a0_pb34_direct_quotient_owner_v9_bootstrap_namespace_fix.md`.

Do not edit v3/v8, workflows, proofs, v220, artifacts or checkpoints.  Do not
commit, push, dispatch or run the actual search locally.

## Exact correction

In `run`, after loading pinned task413, load `BASE` before the receipt and q3:

```python
t413 = v3.load(v3.T413, "task427_task413")
base = t413["bound_module"](t413["BASE"], "task427_base")
receipt = t413["load_json"](base, t413["JOINT"])
q3 = t413["load_json"](base, t413["Q3"])
pres = base["compact"](receipt, q3)
```

Then continue with that same `base`; do not load a second BASE copy.  The roof
and acceptance calls already correctly pass `base` and remain so.  Update v9
schema/header/markers/unique filenames and producer/checker pins.  Stale v8
runtime imports are forbidden; the only runtime dependency remains pinned v3.

## Bounded gates

Run:

1. syntax compilation of producer/checker;
2. producer `FIXTURE` and checker `--self-test`;
3. one **single-process, no-checkpoint, zero-second production bootstrap smoke**
   with `--seconds 0` and `--output` in `%TEMP%` outside the repository.

The third gate is allowed only to prove that the actual pinned bootstrap reaches
both `phase=preflight owner_v9=BOUND` and
`phase=runtime_bootstrap owner_v9=READY`, then stops at the first resource guard.
It must not enter seed work, create a checkpoint, fan out Python, or run more
than the bootstrap.  Its artifact must say `UNKNOWN_RESOURCE:time_limit`, not a
namespace/key/pin error.  Remove no repository files.

The v9 driver must remain fresh-run compatible, use distinct input/output
checkpoint paths, 4.8 GB owner cap, live logs, generic GAP-run contract and
exact pins.  Report commands, elapsed time, the two bootstrap markers, artifact
reason, bytes/SHA and exact changed lines.  End with
`V9_LOCAL_GO_FOR_PARENT_DISPATCH` or a precise `NO-GO`.
