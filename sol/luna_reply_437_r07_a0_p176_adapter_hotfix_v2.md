# Luna reply — Task437 p176 attribute-adapter hotfix v2

Implemented only the four authorized v2 outputs.  The v2 producer and
checker byte-pin their respective audited v1 files and add only the required
dict-plus-attribute adapter around `p176`; the v1 algorithms and selector
are otherwise reused unchanged.  Public schema, markers, artifact paths,
checkpoint paths, and driver preamble are v2-specific.

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_actual_b72_first_active_v2.py` | 2352 | `9355647447c004483d63b827bc95929ad8432a443f166ccdadcf5f054b7bbc17` |
| `crosscheck/check_d972_r07_a0_actual_b72_first_active_v2.py` | 1767 | `d72c65136d6f8f821031a1fda6b5c11a4d1bca84ae5c91c8146883d68ff82312` |
| `search/d972_r07_a0_actual_b72_first_active_gha_driver_v2.g` | 2303 | `98d9bba8ff19998746bcfe7ca5befe3ca06bbe987a0cab1bfb9268cb5c142be4` |

Gates are limited to external-cache `py_compile`, producer FIXTURE with a
temporary output outside the repository, checker `--self-test`, bounded
driver pin/command reconstruction, and `git diff --check`.  No local
production/bootstrap, checkpoint load, download, workflow edit, commit,
push, or dispatch was performed.

Results: syntax compile PASS; producer v2 fixture PASS with schema v2;
checker v2 self-test PASS with ten mutation rejections; exact driver pins
match the two wrapper files; `git diff --check` PASS.  No production prefix
or selector was run locally.

## Parent broker result

- committed/pushed source
  `61aafa6b5cc1947debbe347d6f2584c9696cd970`;
- dispatched run `33405554013`, job `99532138064`;
- v2 passed the prior p176 failure and compiled all 44 formulae: 1,060,263
  merged targets total, maximum 95,736, with 42 nonempty seeds;
- it then stopped before Q0 with fail-closed `UNKNOWN`, exact reason
  `KeyError('load_json')`.  Artifact `9763308344` contains the 197-byte JSON
  at SHA-256
  `c2ef040007a9ee82e599074f879e77343c2a984cf6e441f98cdfb01a58ea48f6`.

The second mismatch is also bootstrap-local: v1 selective runtime reads
`base["load_json"]`, whereas task435 authenticates the loader as
`t413["load_json"]`.  There is no Q0, ACTIVE, EMPTY, cap, or memory result.
Versioned Task438 v3 repairs that key and adds a toy fixture for both adapter
requirements.
