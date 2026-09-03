# Luna Task654 reply

The single inverse-choice blocker is closed. Production now obtains each
signed base factor through `signed_base_factor(base, sign, inverse)`. The same
helper is exercised by selftest with the non-self-inverse S3 3-cycle
`(1,2,0)`, whose independently fixed inverse is `(2,0,1)`. Returning the base
from the negative branch makes `signed_base_inverse_choice` fail. Invalid
signs are rejected by the same helper.

The Task651 noncommutative prefix, ancestry-binding, and packing-roundtrip
fixtures are unchanged. Checker selftest reports `mutation_count=43`. No
production, GHA, or git operation was run. Exact final hashes are supplied
out of band after the workflow/reply chain is sealed.

| path | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 92,071 | 1,563 | `889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `4d76e057838af7d7c1d6ad28203bdfeec545be36aaf94a815b22bfad58a15f39` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,972 | 58 | `a187b207f4cbf97c0b20fe28c8edd33a39f60cbdf34909a5cfba56000dd4287b` |
| `sol/luna_reply_651_r07_task640_three_live_fixture_closure.md` | 1,770 | 36 | `08d16a55a0d913c829f2446c28022aa39a8360c1ebd96c6b90aaa29ebc68e404` |

Serial `py_compile`, both selftests, YAML safe parse, forbidden shared-import/
exec scan, immutable-action scan and inert `false &&` check all passed. This
reply's final digest is supplied out of band.

READY_FOR_TASK655_FINAL_REAUDIT
