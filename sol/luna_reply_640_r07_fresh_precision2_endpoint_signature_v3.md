# Luna Task648: final finite Task640 v3 release repair

## Result

Only F646-A/B/C were repaired in the existing quartet. Accepted R1/R3/R4/R5/R7,
the inert workflow, stream-only ancestry, bucket-only dense replay, live caps,
and the false/null claim boundary remain unchanged. No production, GHA or git
operation was run.

## F646 repair map

- **A -- canonical parent scalars.** The checker now requires the four run and
  attempt fields as the exact JSON strings emitted by the producer. Production
  and selftest share `exact_parent_gate`; integer/string and artifact-envelope
  mutations are rejected without coercion.
- **B -- exact seven receipts.** `RECEIPT_NAMES` fixes every key-to-filename
  mapping. The checker first rejects aliases/renames, independently rebuilds
  all seven expected byte strings, then requires each complete receipt object
  to equal fixed filename, exact length and SHA-256. Filename, length and digest
  mutations pass through the same `exact_receipt_gate` used by production.
- **C -- live-predicate fixtures.** Production and bounded selftest now share
  gates for manifest header/claims, exact parent, root contract, raw-source
  seeds, occurrence type/coordinate/sign order, typed E3/E4 identities,
  right signature extension and recurrence, full-signature buckets,
  block-product and direct/occurrence equality, dense target/lower/top/packing,
  exact receipts, and the existing R07LEAF1 parser. Tiny mutations cover the
  requested scalar/envelope, schema/marker, claim, missing/swapped root,
  invalid seed, slot/type/sign, inverse/PP/right order, premature merge,
  nonidentity/direct mismatch, receipt, dense byte and malformed leaf cases.

During this repair the new live packing fixture exposed a name collision
between dense `unpack` and endpoint element unpacking. The endpoint helper was
renamed `unpack_element`; production dense packing now reaches its intended
independent implementation.

## Bounded checks

- both Python `py_compile`: PASS.
- producer `--selftest`: PASS.
- checker `--selftest`: PASS (`mutation_count=43`).
- local q3 E3/E4 construction and eleven-context endpoint smoke: PASS.
- YAML safe parse: PASS.
- forbidden checker scan (`exec`, `.load`, `ModuleType`, shared semantic
  imports): PASS.
- immutable action full-SHA scan and inert `false &&` guard: PASS.
- whitespace/final-LF and workflow pin checks: PASS.

## Exact Python files before final workflow pin

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,474 | 304 | `060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 92,071 | 1,563 | `889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32` |

The final workflow and reply hashes are supplied in the out-of-band completion
handoff to avoid a workflow/reply mutual self-reference.

READY_FOR_TASK649_FINAL_REAUDIT
