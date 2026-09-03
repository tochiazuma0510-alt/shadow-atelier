# Sol(max) Task700 — minimal endpoint deletion install versus full build_heavy

Task697 correctly found that Task640's first `ProducerAllSeven.coordinates`
call requires `runtime["delete"]`, absent from `build_light`.  Do **not** assume
that calling the full `build_heavy` is the shortest repair: it continues into
the 1,469,664-state Q0 section owner, memberships and fibres, none of which is
used by Task640.

Audit the exact prefix of `v12f.build_heavy` that constructs deletion:

```python
p176, old = runtime["p176"], runtime["old"]
e3, e4 = runtime["e3"], runtime["e4"]
fine, fine_public = p176.build_fine_deletion(e3,e4,meter)
q0_marked = [p176.canonical_packed_permutation(
    old.perm_from_row(row,36),36,"task640 Q0 mark")
    for row in runtime["q3"]["coarse_models"]["Q0"]["marked_permutations"]]
delete, deletion_public = p176.make_deleter(old,e3,e4,fine,q0_marked)
deletion_public["fine"] = fine_public
runtime.update({"delete":delete,"deletion_public":deletion_public})
```

Questions:

1. Is this byte/mathematics-equivalent to the deletion installed by the full
   builder before its unrelated Q0 work?
2. Does every subsequent Task640 producer API require only this deletion plus
   the light runtime, or any later heavy key?
3. Is retaining the 59,049-entry `fine` table through the closure necessary
   and inside the existing memory cap?  Give an honest order/rough byte bound;
   no benchmark is required.
4. State the smallest live fixture/canary needed (if any) and an exact
   `SAFE_TO_IMPLEMENT_MINIMAL_DELETE=yes/no` verdict.

Do not edit code, run heavy computation, request generic hardening, or touch
git/GHA.  Reply only to
`sol/sol_reply_700_audit_r07_task640_minimal_deletion_install.md` with hashes
and `verified=false`.
