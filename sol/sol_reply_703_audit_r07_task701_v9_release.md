# Sol(max) Task703 — exact Task701 v9 release audit

## Verdict

`verified=false`

Task701 implements exactly the Task700-approved minimal deletion boundary.
No release blocker was found.

## Frozen inputs

| path | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 31,609 | 383 | `8719929bfd6d134320da8c6fc1a8df527f458c1523f8edb0330b539649097206` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v9.yml` | 10,225 | 162 | `b381c5ebd8d791bdd36925898d25f4292a05fc62e83588f1782b0e32242e7186` |
| `sol/luna_task_701_r07_task640_v9_minimal_deletion.md` | 2,713 | 58 | `ca20b6bf6daa0ba17930353a3ebc9e5000137d789b8c4ef1e0f8633f15ed8e18` |
| `sol/luna_reply_701_r07_task640_v9_minimal_deletion.md` | 2,465 | 59 | `5079de2349909b3d79cef4755e8127d5f826268beb971bf203076ae26e7b8676` |
| accepted Task700 reply | 6,218 | 125 | `3d73fd18af183bb04af7daf5c206f61e99f65bcabfb638237cbb9b0e719e9e0e` |
| `sol/sol_task_703_audit_r07_task701_v9_release.md` | 1,134 | 24 | `dbdc9378481865d550df3b7c035ce9265ef33ec0a40ceb3f32ceedb5a030e6bc` |

The three hashes frozen by Task703 match exactly.

## Producer delta

`load_all_seven` now has the required order:

1. pinned `build_light(registry,meter)` at line 95;
2. `install_endpoint_deletion(runtime)` at line 96;
3. construction of `ProducerAllSeven(runtime)` at line 97;
4. the first `coordinates(())` call in the zero-word canary at lines 98–103;
5. only then return to the later signature/endpoint arithmetic.

The installer at lines 106–123 is the Task700 prefix, with no mathematical
substitution:

- it takes `p176`, `old`, `e3`, `e4`, and the same runtime `meter`;
- it calls `build_fine_deletion(e3,e4,meter)` and requires the public source
  order to equal exactly `59049`;
- it canonicalizes the two Q0 marked rows through
  `old.perm_from_row(row,36)` and the pinned task176 validator;
- it passes the returned fine table once to `make_deleter`, requires the
  result callable, attaches the exact `fine_public` receipt, and installs only
  `delete` plus `deletion_public` in the light runtime.

The returned `delete` closure naturally retains that single fine table.  An
AST call census found zero calls to v12f `build_heavy`; the similarly named
fixture trap is only a definition and is never invoked.

The zero-word canary compares `ProducerAllSeven.coordinates(())` with exactly
five packed E3 identity blobs followed by five packed E4 identity blobs.  It
therefore exercises the installed deletion through the production coordinate
API before the first trie signature and has the precise Task700 type/order.

The shared installer fixture invokes this production helper, observes one
fine-build and one deleter-build call, exercises the installed callable,
rejects source order `59048`, and leaves the fake `build_heavy` trap false.
The bounded producer selftest emitted:

```text
endpoint_installer=PASS
endpoint_fine_source_order=59049
wrong_fine_order_rejected=1
build_heavy_trap_called=false
```

As an exact regression proof, removing only the new load-site block, the
installer, and its specified fixture fields in memory reconstructs the
Task697 source byte-for-byte: 27,899 bytes, 312 LF, SHA-256
`684c629eef8100175b676a4e4762db18f67e5a99672b4107facc7dad412acfc2`.
Thus all later signature, endpoint, direct-column, precision-two action,
aggregation, target, packing, manifest, and claim logic is unchanged.

## Workflow delta

An exact line comparison against v8 has only the seven Task701 replacements:
workflow name, self-trigger path, producer SHA pin, inert guard plus v9 fire
label, authentication label, and the two artifact names.  In particular:

- `PRODUCER_SHA256` is the exact final producer hash above;
- global `TASK640_SECONDS` remains `5400`, and the producer/checker step alone
  overrides it to `9600`;
- both outer commands remain `timeout ... 45m`, and the job timeout remains
  120 minutes;
- every checker/prebuild/parent/source pin, cap, action SHA, download,
  parent-replay command, producer/checker command, comparison, and upload path
  is byte-identical to v8;
- the frozen guard is explicitly inert via `false && (...)`, as commissioned.

External-cache serial `py_compile` passed for producer and checker.  Both
bounded selftests exited zero; the checker retained its 43 mutations.  The
real 59,049-state deletion and all production/GHA work were deliberately not
run.  No code, workflow, git state, mathematical claim, or unrelated audit
surface was changed.

PASS_MINIMAL_DELETE_ONLY
SAFE_TO_DISPATCH_GHA=yes
