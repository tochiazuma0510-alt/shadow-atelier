# Luna reply 781 — canonical P1 input-size type repair v1

## Outcome

Created only the three requested successors:

- `search/d972_r07_canonical_p1_dag_degree2_lift_v7.py`
- `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v4.yml`
- this reply

No GHA, git, network, parent-artifact download, or 8,059-row build replay was
run.

## Repair

The producer now names the third `sem.block_envelope(...)` result
`body_size` and passes it through `nonnegative_size`.  `plain_int` rejects
bytes and bool, and the nonnegative check rejects negative values.  The
`artifact_entry` ABI takes that integer, checks it against the current regular
file's `st_size`, and records the existing `body_bytes` field plus stable
identity.  It does not hash or serialize a block body.

The prepare ABI is coherent: `len(prepare_raw)` is recorded as
`prepare_size`, then the raw string is deleted.  The prepare sealed-body
registry entry uses pinned `PREPARE_DIGEST`; each block sealed-body entry uses
`PARENTS[index]` directly.  `FileRegistry.verify` remains unchanged and
rehashes every physical registered file against its pinned digest.

The old `block_raws: list[bytes]` storage and boundary key are gone.  The
boundary retains only `block_sizes: list[int]` (four small integers); no
downstream code consumes the old key.  The bounded selftest constructs a
two-byte fixture envelope whose third component is `len(payload)`, reaches
`artifact_entry` and `FileRegistry.verify`, and rejects bytes, bool, negative,
wrong-length, and post-registration physical mutations.  It constructs no
production-size body and does not invoke the build loop.

## Versioning and receipts

The producer final result schema is v6, launch schema is v6, and executable
key is `producer_v7`.  Workflow v4 invokes and authenticates v7, uses the exact
fire token `[fire-r07-canonical-p1-degree2-lift-v4]`, and publishes task781/v4
candidate and log labels.  All inherited checker, source, parent-artifact,
receipt, resource, actor, packet, cache, and claim pins are unchanged.

| file | bytes | SHA-256 | LF / CR / NUL | final byte |
|---|---:|---|---:|---:|
| `search/d972_r07_canonical_p1_dag_degree2_lift_v7.py` | 108071 | `b42cc67bf6c56110b6fb52d95bbbb0870a6c111da739eaf0e1401b4474325e3d` | 2304 / 0 / 0 | 10 |
| `.github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v4.yml` | 27574 | `5405fd5a83844ff95e3b79239e1f158ab653b237d2f8bfb6fd20eba73497f1cb` | 497 / 0 / 0 | 10 |

The workflow pins the producer as v7 at exactly 108071 bytes, 2304 LF, and
SHA-256 `b42cc67bf6c56110b6fb52d95bbbb0870a6c111da739eaf0e1401b4474325e3d`.

## Bounded checks

- `python -B -m py_compile search/d972_r07_canonical_p1_dag_degree2_lift_v7.py` — PASS.
- `python -B -u search/d972_r07_canonical_p1_dag_degree2_lift_v7.py --selftest` — PASS:
  `body_size_artifact_registry=true`, `body_size_rejections=5`,
  `selftest=PASS`, `actual_replay=DEFERRED_TO_GHA`, `verified=false`.
- PyYAML parse — PASS; one job, 17 serial steps, 10 pinned actions.
- Exact pin check — PASS; producer path/hash/bytes/LF match and the fire token
  occurs exactly once.
- AST/diff check — PASS; all arithmetic functions tested (`recurse_node`,
  projector/packet, seed/defect, flattening, row/instruction hashing) are
  unchanged.  `build` has four loops and all four loop ASTs are unchanged;
  its differences are only final manifest schema/executable-key literals.
- Static search — PASS; successor contains no `block_raws`, no
  `canonical(body)` substitute, and no `sha(body_size)`; no code consumes
  `boundary["block_raws"]` or `boundary["prepare_raw"]`.

No arithmetic AST or build-loop AST changed:

```text
ARITHMETIC_AST_UNCHANGED=yes
BUILD_LOOP_AST_UNCHANGED=yes
ACTUAL_8059_ROW_LIFT_REPLAY=NOT_RUN
verified=false
READY_FOR_SOL_AUDIT=yes
```
