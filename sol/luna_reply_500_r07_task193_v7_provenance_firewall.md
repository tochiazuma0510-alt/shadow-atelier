# Task500 — Task193-v7 exact rank99 provenance firewall

Implemented exactly the four requested outputs.  The frozen carrier trio and
Task193-v6 owners were not edited.  V7 transforms the exact generated v6
bodies with cardinality-checked patches only: v7 wrapper/result/checkpoint/
checker-verdict names, the independent producer `firewall` predicate, the
independent checker `boundary` predicate, output provenance binding, and
bounded fixture coverage.

## Frozen pins

Carrier trio (unchanged):

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_rank99_v5_task193_carrier_v1.py` | 17290 | `34983cfaec66f426bdfc63eae5230c27a34f02c847f6154ba81771e6c995b0cd` |
| `crosscheck/check_d972_r07_rank99_v5_task193_carrier_v1.py` | 17400 | `fde1cf20ed2111bddabb47abd8fd6c165db3f6e4f4c00a4acf493ceb9c0f169b` |
| `search/d972_r07_rank99_v5_task193_carrier_gha_driver_v1.g` | 3019 | `9bb7dc6778517089f3ae77f94a99d065330635552443f8e701f1e9df8dd46b99` |

V6 transformation owners (unchanged):

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_second_frattini_affine_prefix_compiler_v6.py` | 5512 | `0f1bf66f53d8cd4decdcd28b1ef6c1b185329f1b8b00f9e681bff112d8534fc1` |
| v6 generated producer body | 12282 | `2d26dd83c930165f740ec53b621b03d1b57b1232a7b2cd1905730033f4e20341` |
| `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v6.py` | 5428 | `ce735eb1fafb743a53b17ef056b56f4cbd3bf1ff39969dabb5b708c4c43519fb` |
| v6 generated checker body | 7831 | `b1e7b9047b839fcf5306cf32bb7876f4d55ef8e5f1eb0c48829a348811911ea3` |

V7 outputs:

| file/body | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_second_frattini_affine_prefix_compiler_v7.py` | 9574 | `05cd9bd5c965941d89d09a7ea2a1438e99d7f9fed8effdb0241f1bc2a1a99bc2` |
| v7 generated producer body | 18194 | `b5461b39c842bf9d310a4b70fd4be82a43d5249f2380beca27b6fe21459dce87` |
| `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v7.py` | 9539 | `4660de49dab3fbb4c749b7c0b841d812b22b77fc1d7ca625ca55755adff1ee48` |
| v7 generated checker body | 13831 | `4469ea689ca6dec1864fa842525cb680fa49463789a4dd6357406ff706776cb5` |
| `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v7.g` | 2887 | `1fba473e278ec98bd33f1daaf5d515b1b92a6c5ec2e27e853ceac47f5bac6041` |

## Firewall and bounded gates

Both generated bodies independently require source head
`dd6d90b64e2bfba73d7f131f4da876235746f314`, run `33553895281`, canonical
positive-decimal dynamic artifact text, the exact complete v5 `upstream`
dictionary, exact six-key `inputs` with physical identity shape, and exact
checker-verdict `inputs == carrier inputs`.  The producer carries the bound
head/run/artifact into `source_provenance.carrier_provenance`; the checker
requires that output binding before its frozen Task193 compatibility checks.

The actual generated `firewall` and `boundary` were exercised by the fixtures.
Each retained an honest-shaped dynamic artifact (`7331`) with
`actual_common=false`.  Both independently rejected 20 mutations covering
missing/extra upstream, wrong run/head, artifact `0`, `00`, `01`, signed,
whitespace, non-ASCII digit, integer, receipt/upstream/verdict artifact/run/
head/physical-identity drift, stale v6 dialect, and binding drift.

Bounded commands/results:

```text
python -B search/d972_r07_second_frattini_affine_prefix_compiler_v7.py --fixture --output %TEMP%\task500-v7-producer-fixture.json
R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V7_PRODUCER_TERMINAL FIXTURE
fixture status=PASS actual_common=false dynamic_artifact=7331 mutations=20

python -B crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v7.py --self-test
R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V7_CHECKER_SELFTEST_PASS mutations=20 inner_key_transform=true final_reseal=true verdict_abi=true actual_common=false

AST wrapper parse: PASS
source-patch cardinality and generated pins: PASS
GAP ReadAsFunction(v7 driver): PASS (unbound-global warnings only)
generated-shell syntax: not applicable; v7 driver executes its two bounded commands directly
```

No Task193 heavy computation, A0, production, GHA, or git operation ran.

TASK500_R07_TASK193_V7_PROVENANCE_FIREWALL_PASS
