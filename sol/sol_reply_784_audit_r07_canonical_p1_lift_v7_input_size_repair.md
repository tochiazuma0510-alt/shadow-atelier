# Sol Task784 — hostile audit of canonical P1 lift v7 input-size repair

## Ruling

**PASS; authorize the v4 GHA dispatch immediately.**  The actual v3 failure
site is closed on the reached path.  Producer-v7 consumes the structural
helper's third return as an integer byte count, never presents it to SHA-256,
does not introduce a large body copy, and preserves both the earlier
canonical-byte/digest authentication and the later physical-file rehash.

This is authorization for one candidate-producing run, not a prediction that
the run will succeed.  I did not run the 8,059-row recurrence, download a
parent, use network/GHA/git/delegation, or make a mathematical claim.
I read every commissioned input; the two producers and two workflows were
also consumed in full by the byte/AST/diff checks below.

## 1. Controlling call chain and exact type

The traceback from run/attempt `33827142944/1`, job `100882118138`, at exact
head `bd1f092b8301e4a07cf0a3c8b228bff63e23276b` is controlling:

```text
phase=build.authenticate_inputs
producer-v6 authenticate_inputs: sha(body_raw)
sha: hashlib.sha256(data)
TypeError: object supporting the buffer API required
```

The pinned path proves why the value was an integer and why v7 is correct:

1. Producer-v7 loads semantic-v5 and structural-v1 with `load_exact`: it
   hashes the bytes, compiles those same retained bytes, and does not reopen a
   path through a normal module loader.
2. For prepare, `sem.authenticated_prepare` calls `read_sealed`.
   `read_canonical` requires the physical bytes to equal `canonical(value)`,
   and `read_sealed` requires `sha(body_raw) == PREPARE_DIGEST`.  V7 then takes
   `len(prepare_raw)`, passes that built-in integer through
   `nonnegative_size`, and immediately deletes the raw-byte reference.
3. The actual CLI requires exactly four block roots.  V7 enumerates all four,
   and `sem.block_envelope` first enforces index `0..3` and prepare ancestry.
   It calls the supplied, already authenticated structural module.
4. Structural-v1 constructs the body filename from its pinned digest, parses
   the exact HEAD and body, requires canonical HEAD bytes and the exact HEAD
   object, requires both `sha(br) == digest` and `br == canonical(body)`, and
   enforces the exact three-file roster.  Its return is exactly
   `(root, body, len(br))`.
5. Semantic-v5 additionally checks the full block semantics and pinned basis
   digest and passes the third component through unchanged.
6. V7 immediately applies `nonnegative_size` before appending each value.
   `plain_int` excludes `bool`, and the same guard excludes negative values.
   The four values are stored only as `block_sizes: list[int]`; a count gate
   requires four.
7. `artifact_entry` applies the guard again, requires a lowercase 64-hex
   digest, checks the exact regular file selected by stem and digest, requires
   its current `st_size` to equal the integer, and records the five-component
   stable identity `(dev, ino, size, mtime_ns, ctime_ns)`.

The prepare call passes `PREPARE_DIGEST`; every block call and sealed-body
registry entry passes `PARENTS[index]`.  Mechanical extraction showed that
the prepare pin and all four parent pins are identical in producer-v7,
semantic-v5, and structural-v1.  Thus this is not an untrusted digest copied
from the size-bearing return.

## 2. Authentication is not weakened

Replacing the impossible `sha(integer)` calls with the fixed digests does not
remove an authentication gate:

- Prepare bytes were already checked for canonical serialization and against
  `PREPARE_DIGEST` by the pinned semantic module.
- Each block's `br` was already checked for canonical serialization and
  against the index-specific parent digest by the pinned structural module.
- The workflow's launch constructor independently reads and hashes each
  physical body against the same five pins and records size and stable
  identity.
- Producer-v7 recomputes its five `raw_artifacts` entries from the current
  files and requires exact equality with the canonical launch manifest before
  any recurrence row.
- `FileRegistry.verify`, unchanged from v6, streams every registered physical
  file through `file_sha`, requires stable identity across that read, and
  compares size and digest with the registered values.  It runs after stream
  receipts but before manifest creation and `os.replace` promotion.

Consequently a same-size body mutation is not hidden by the size ABI: the
fixed-digest registry rehash rejects it.  A mutation between the structural
read and launch comparison cannot change the parsed dictionary used by the
recurrence; an identity mismatch rejects at launch comparison, and any wrong
bytes still present reject at the final rehash.  Restoring the pinned bytes
before that rehash cannot retroactively alter the already authenticated
parsed dictionary.  The registry does not purport to lock files for the
whole run; v7 neither weakens nor broadens that inherited concurrency model.

A forged launch `raw_artifacts` entry is compared with the producer's locally
computed list, not accepted as its own authority.  The bounded mutation of a
block digest in that list failed with `launch_raw_artifacts`.

## 3. No-copy and production cost

The complete v6/v7 text diff contains no new block-body read,
serialization, byte retention, or copy.  Static search in v7 found no
`block_raws`, no `canonical(body)` in the producer, and no `sha(body_size)`.
The only `prepare_raw` uses are `len(prepare_raw)` followed immediately by
`del prepare_raw`.  In place of raw block buffers, the returned boundary has
only four integer sizes; build does not consume that key.

There are two necessary inherited passes which are not copies added by this
repair: structural-v1's original read/canonical comparison while authenticating
each block, and the final registry's 1-MiB streaming physical rehash.  The
workflow launch constructor's body read is also unchanged from workflow-v3.

The production delta attributable to v7 is therefore:

- logically retained serialized-body payload decreases by exactly
  `len(prepare_raw)` bytes during the four block authentications and
  thereafter; v6 kept that prepare buffer in its returned boundary (an
  immediate RSS decrease is not claimed because that is allocator-dependent);
- the misnamed v6 `block_raws` list already held four integers on the actual
  interface, so renaming it to `block_sizes` changes no large allocation;
- v7 adds ten constant-time nonnegative-integer guards (prepare plus four
  blocks, then five artifact entries), five 64-character digest-format checks,
  and no per-row work;
- v7 removes the extra in-memory SHA-256 pass over the prepare body and
  replaces four invalid `sha(int)` attempts with constant-time size checks;
  the required final streaming hashes are unchanged.

No exact production body byte count was guessed because no parent was
downloaded.  The exact memory improvement is the formula above; the added
large-body allocation is zero.

## 4. AST and recurrence neutrality

Full top-level AST comparison reported exactly these changed definitions:

```text
artifact_entry
authenticate_inputs
build
fixture_receipt_validation
selftest
validate_launch_manifest
```

The only added definitions are `nonnegative_size` and the bounded
`fixture_body_size_artifact`; none was removed.  `validate_launch_manifest`,
`fixture_receipt_validation`, and the non-loop portion of `build` change only
the required launch/result schema and `producer_v7` key, apart from the
selftest wiring and the input-size repair itself.

Every audited arithmetic/storage definition is AST-identical between v6 and
v7: `validate_node`, `validate_expression`, `validate_actor_order`,
`validate_defect_origins`, `validate_authenticated_dag`, `add_full`,
`scale_full`, `flatten_p1`, `full_from`, `expected_p1`, `recurse_node`,
`projected_seed`, `compile_packet_v486`, `compile_old_defect`,
`raw_component_digest`, `full_row_digest`, `reduction_digests`,
`make_instruction`, `checkpoint`, and `instruction_receipt`.  All unchanged
top-level classes, including `PackedCache`, `InstructionSink`, `LazyP1`, and
`FileRegistry`, are AST-identical as well.

`build` contains exactly four `for` nodes: old outer/inner and new
outer/inner.  Their normalized AST SHA-256 values match pairwise across v6
and v7:

```text
962cb00a29d395b0de9b94e871b81b75d5bd9660891b4ada98959d7b528f6026
b87191ef3751c4d6d739c2c742defa99de9582c4b7f8e12cce1665660758cd77
d84bdf9f42e21dc934f789d57bd80c34e7c301872717aea4bee3e12db80e98d9
8afdf54f3d36f0be45ac57a8f4c6bafe5b3ff075d7cf3b555f4749584cdce235
```

Static extraction of every `boundary[...]` access in `build` gave the same
key set for v6 and v7 and excluded `prepare_raw`, `block_raws`, and
`block_sizes`.  Removing the two old returned keys and retaining only the
small size list therefore cannot change the recurrence.

## 5. Bounded hostile controls

All generated material was under temporary directories outside the
repository.

| control | result |
|---|---|
| external-pycache `py_compile` | PASS |
| producer-v7 `--selftest` | PASS; `fixture_accept=7`, `rejections=55`, `body_size_rejections=5`, `actual_replay=DEFERRED_TO_GHA`, `verified=false` |
| real structural helper, indices 0–3, tiny canonical envelopes | each returned built-in `int`, with returned size exactly equal to byte length |
| bytes size | REJECT `artifact_body_size` |
| bool size | REJECT `artifact_body_size` |
| negative size | REJECT `artifact_body_size` |
| wrong integer length | REJECT `artifact_body_identity` |
| same-length physical mutation after registration | REJECT `registry_digest_changed` |
| wrong fixed digest through artifact/registry path | REJECT `registry_digest_changed`; on production it is also excluded earlier by the structural pin |
| forged launch raw-artifact digest | REJECT `launch_raw_artifacts` |

The tiny controls constructed no production-sized body and invoked no build
loop.

## 6. Workflow-v4

Exact byte receipts are:

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| producer-v6 | 105,983 | 2,257 | `e83f6fca9643905b935b73b8dcaea51effbe08f6a9549523478227d3ec85bc62` |
| producer-v7 | 108,071 | 2,304 | `b42cc67bf6c56110b6fb52d95bbbb0870a6c111da739eaf0e1401b4474325e3d` |
| workflow-v3 | 27,574 | 497 | `ac5d47c2e8b709af96b2ebc3e9fef60d4844f3014efef26806b69c06b14c40c1` |
| workflow-v4 | 27,574 | 497 | `5405fd5a83844ff95e3b79239e1f158ab653b237d2f8bfb6fd20eba73497f1cb` |

All four files have zero CR/NUL bytes and end in LF.  Workflow-v4 parses,
and all four inline Python programs parse.  Mechanical audit found:

- one job, 17 sequential steps, no strategy/matrix/retry, and one producer;
- ten action uses, each pinned to a full 40-hex commit;
- all eight local path/SHA-256/byte/LF/EOF pins match the present exact files;
- unchanged checker run/artifact gates, producer receipt gates, source
  run/attempt/head gates, and all five parent ID/name/archive-size/archive-
  digest/expiry/run/head gates;
- launch schema `...launch.v6`, executable key `producer_v7`, candidate schema
  `...lift.v6`, and the exact candidate terminal agree in constructor,
  producer, and validator;
- internal time cap 2,220 seconds, producer wrapper 38 minutes, job cap 45
  minutes, RSS cap 7 GiB, and virtual-memory ceiling 8 GiB are intact;
- candidate upload is `if: success()` and log upload is `if: always()`;
- `[fire-r07-canonical-p1-degree2-lift-v4]` occurs exactly once and the v3
  token is absent.

After reversing only the displayed producer path/hash/size/LF, workflow/fire
version, launch/result schemas, executable key, and artifact-label changes,
workflow-v4 is byte-for-byte workflow-v3.  No parent gate or resource policy
was changed.

No canonical P1 lift, compatible lift, A0/common/cofinal result, fake/Ihara
witness, or Lean verification is claimed.

```text
VERDICT=PASS_CANONICAL_P1_LIFT_V7_INPUT_SIZE_REPAIR
ROOT_CAUSE_CLOSED=yes
NO_LARGE_BODY_COPY=yes
SAFE_TO_DISPATCH_GHA=yes
ARITHMETIC_AST_UNCHANGED=yes
BUILD_LOOP_AST_UNCHANGED=yes
CANONICAL_P1_LIFT=NOT_CLAIMED
FAKE_IHARA=NOT_CLAIMED
verified=false
```
