# Luna Task701 — Task640 v9 minimal deletion install

## Exact blocker

Task697 proved that after v8 constructs only the v12f light runtime, the first
`ProducerAllSeven.coordinates()` unconditionally reads `runtime["delete"]`
and raises `KeyError('delete')`.  GHA v8 was cancelled before wasting the full
parent replay.  The full v12f `build_heavy` is not permitted here: after its
deletion prefix it constructs the unrelated 1,469,664-state Q0 owner,
memberships and fibres.

## Required producer delta

In `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`, factor and
call a minimal endpoint-deletion installer immediately after `build_light` and
before returning/using `ProducerAllSeven`.  Translate exactly the deletion
prefix of hash-pinned `v12f.build_heavy`:

```python
p176, old = runtime['p176'], runtime['old']
e3, e4 = runtime['e3'], runtime['e4']
fine, fine_public = p176.build_fine_deletion(e3,e4,meter)
q0_marked = [p176.canonical_packed_permutation(
    old.perm_from_row(row,36),36,'task640 Q0 mark')
    for row in runtime['q3']['coarse_models']['Q0']['marked_permutations']]
delete, deletion_public = p176.make_deleter(old,e3,e4,fine,q0_marked)
deletion_public['fine'] = fine_public
runtime.update({'delete':delete,'deletion_public':deletion_public})
```

Require the public fine receipt's source order to be 59,049 and require the
installed key/callable.  Do not construct or copy any later heavy key.  The
deleter closure must retain its fine table naturally; do not duplicate it.
Add one bounded live fake-runtime fixture proving the production installer is
called, installs a callable, rejects a wrong fine order, and never calls a
fake `build_heavy` trap.  Do not change the payload schema, endpoint math,
checker, source pins, caps or unrelated tests.

## v9 wrapper

Create `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v9.yml` from
v8.  Change only v8-to-v9 wrapper labels/artifact names, update the producer
SHA pin to the new exact file, and add an inert `false &&` to the job guard.
Preserve the step-local `TASK640_SECONDS=9600`, global 5400, both 45m timeouts,
120m job timeout and every other pin/command/action.

Run serial `py_compile` and both bounded producer/checker selftests; do not run
the 59,049-state real build locally.  Report exact bytes/LF/SHA, normalized
source/workflow diff and fixture result in
`sol/luna_reply_701_r07_task640_v9_minimal_deletion.md`.

Candidate only; no commit, push, dispatch, GHA, or other file changes.

## Mutation boundary

- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v9.yml`
- `sol/luna_reply_701_r07_task640_v9_minimal_deletion.md`
