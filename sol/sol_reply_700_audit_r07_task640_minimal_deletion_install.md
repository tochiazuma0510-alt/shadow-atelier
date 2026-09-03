# Sol(max) Task700 — minimal endpoint deletion installation audit

## Verdict

`verified=false`

`SAFE_TO_IMPLEMENT_MINIMAL_DELETE=yes`

The proposed deletion prefix is the correct minimal repair for Task697's
missing `runtime["delete"]`.  It constructs the same deletion function and
public deletion receipt as the corresponding prefix of the pinned v12f full
builder, while omitting Q0 section enumeration, memberships, adjusted-L data,
and fibres that Task640 never reads.

## Exact audited inputs

| path | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,899 | 312 | `684c629eef8100175b676a4e4762db18f67e5a99672b4107facc7dad412acfc2` |
| `search/d972_r07_history_free_positive_fast_resume_v12f.py` | 343,155 | 6,472 | `22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb` |
| `search/d972_r07_all_seven_extension_section_census_v1.py` | 66,109 | 1,396 | `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` |
| accepted Task697 reply | 5,443 | 110 | `91fb47cf680d69b907f28f860be00f2d355bdb52dd9b0f9e6c5a17ca2e7f521d` |
| `sol/sol_task_700_audit_r07_task640_minimal_deletion_install.md` | 1,758 | 38 | `c3fc089bc7a30e5a1721fe5e98bd602cbfbeeaf88e640abb72b9ca6732abff8c` |

The first three source hashes equal the Task640 embedded v12f/task176 pins.

## 1. Equivalence to the full-builder deletion

The proposed calls reproduce v12f lines 2917–2922 exactly:

1. `build_fine_deletion(e3,e4,meter)` enumerates the complete 59,049-element
   Pi4 PC group in fixed marked-generator order.  It requires path-consistent
   images, the exact source order, and all six marked fine images before
   returning the `bytes[10] -> bytes[4]` table.
2. The two Q0 marked permutations are obtained by the same
   `old.perm_from_row(row,36)` and
   `canonical_packed_permutation(...,36,...)` calls on the same light-runtime
   `q3` object.
3. `make_deleter` combines the exact noncontiguous 144-to-36 coarse deletion
   with that fine table.  It requires the coarse marked diagnostic and checks
   the resulting matched deletion on all six E4 marked generators.
4. The same `fine_public` object is inserted into `deletion_public`, and the
   same closure and receipt are bound as `runtime["delete"]` and
   `runtime["deletion_public"]`.

Changing the validation label from `"v7 Q0 mark"` to `"task640 Q0 mark"`
changes only an exception message on invalid input; on the authenticated rows
the returned bytes and all receipt fields are identical.  The full builder's
earlier Gamma construction and later Q0 work are not arguments to either
deletion constructor.  They can populate exact memoization caches but cannot
change group products, enumeration order, the fine table, or the deletion
map.  `runtime["task176_receipt"]`, also installed by the full builder, is not
read by these constructors.

Thus the proposed prefix is byte- and mathematics-equivalent to the deletion
used by the full builder.

## 2. Task640 dependency closure

Every post-install v12f use in Task640 closes over the light runtime plus this
one map:

- `ProducerAllSeven.coordinates(word)` reads `p176`, `old`, `e3`, `e4`,
  `contexts`, and `delete`.  `eval_word_coordinates` applies `delete` to the
  five E3 coordinates and passes through the five E4 coordinates.
- `extend_signature` uses only `e3`/`e4`, `p176`,
  `producer_unpack_element`, `producer_element_blob`, and group `mul`.
- the endpoint gate uses only `coordinates`, the two light identities, and
  `p176.packed_joint_blob`.
- `ProducerAllSeven.direct_column` and its occurrence replay use only the
  light `old`, `e3`, `e4`, `p176`, `joint_group`, contexts, and bridge data.
- all later precision-two action, aggregation, packing, and direct-target
  calls are in the independently pinned prebuild/grade1 modules and do not
  access the v12f runtime.

The Task640 producer has no read of `qstates`, `qids`, `parents`, `letters`,
`stores`, `memberships`, `A_maps`, `emitted`, `fibres`, `heavy_public`, or any
other post-deletion heavy key.  Consequently full `build_heavy` is not an API
dependency of this consumer.

## 3. Fine-table lifetime and memory

Retention is necessary with the current implementation.  The returned
`delete(value)` is a closure over `fine`, and every arbitrary E4 PC component
is mapped by `fine[pc_key]`.  Dropping or clearing the table after installation
would make later path signatures fail; `deletion_public` contains only its
receipt, not a replacement lookup structure.

The raw key/value payload is only
`59049 * (10 + 4) = 826,686` bytes.  On ordinary 64-bit CPython, bytes-object,
dict-table, and pointer overhead put the retained mapping at roughly
7–10 MB, not 0.83 MB.  During construction the state/image lists, discovery
dictionary, output dictionary, and bounded PC product caches coexist; a
conservative object-order estimate is tens of MB and below 100 MB.  This is
not an exact RSS benchmark, but it is decisively below v12f's 5.7 GB internal
RSS/address-space ceiling, Task640's 7 GiB RSS gate, and the workflow's 8 GiB
virtual-memory ceiling.  The prefix also avoids the far larger 1,469,664-state
owners retained by full `build_heavy`.

## 4. Smallest live canary

The two constructors already provide the substantive live checks: complete
order/path consistency, six fine marked images, the coarse marked diagnostic,
and six matched marked images.  No second 59,049-state fixture is warranted.

At the consumer boundary, one tiny assertion is sufficient to close the
Task697 wiring regression: after installing the map and constructing the
model, require

```python
model.coordinates(()) == (
    (module.producer_element_blob(runtime, runtime['e3'].identity),) * 5
    + (module.producer_element_blob(runtime, runtime['e4'].identity),) * 5
)
```

This executes the real `coordinates -> eval_word_coordinates -> delete`
path, checks the five E3 and five E4 blob shapes and identities, and requires
no heavy Q0 owner.  Task640's subsequent `signature((), model)` remains the
live production use.

No heavy computation, implementation, GHA, git operation, broader audit, or
new mathematical claim was performed.

SAFE_TO_IMPLEMENT_MINIMAL_DELETE=yes
