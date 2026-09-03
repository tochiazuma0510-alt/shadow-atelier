# Luna Task651 reply

Exactly three live-fixture blockers were repaired in the existing checker.

1. The checker selftest passes an otherwise valid `R07LEAF1` stream with the
   wrong ancestry digest to production `parse_literal_leaves`; it is rejected.
2. Production occurrence-prefix construction now calls
   `occurrence_prefix_gate`. Its bounded permutation fixture uses the same
   helper and checks reverse traversal, positive/negative sign choice and
   order-sensitive prefix multiplication.
3. The dense fixture supplies matching top/packed blob arguments but a packed
   decoding unequal to top, so preceding byte gates pass and the production
   packing-roundtrip branch alone rejects it.

## Frozen files

| path | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 92,071 | 1,563 | `889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `4d76e057838af7d7c1d6ad28203bdfeec545be36aaf94a815b22bfad58a15f39` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,972 | 58 | `a187b207f4cbf97c0b20fe28c8edd33a39f60cbdf34909a5cfba56000dd4287b` |

## Bounded commands and outcomes

- `python -m py_compile` on producer and checker: PASS.
- producer `--selftest`: PASS (`leaf_live_mutations=4`).
- checker `--selftest`: PASS (`mutation_count=43`).
- PyYAML `safe_load`: PASS.
- forbidden shared import/exec scan: PASS.
- immutable-action full-SHA scan: PASS.
- inert `false &&` guard check: PASS.

No production, GHA, or git operation was run. This reply's post-write hash is
supplied out of band because embedding it would be self-referential.

READY_FOR_TASK652_FINAL_REAUDIT
