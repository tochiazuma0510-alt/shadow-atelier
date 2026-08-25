# Luna 162: K2 total fibre roster producer v1 — GHA-ready

## 1. 結論と scope

指定された producer-side の3資産を新規作成した。full 走はローカルでは行っておらず、valid 総数・各 target の valid 数 histogram はまだ **未観測** である。したがって `1944` や「各 target 2点」は実装上も本報告上も acceptance condition にしていない。

- producer: `search/d972_k2_total_fibre_roster_producer_v1.py`
  - bytes: `44829`
  - SHA256: `cc518377347988c5ad531d0d5c0c5410d2c050a91439ccb27db6414ffae9c499`
- GHA wrapper: `search/d972_k2_total_fibre_roster_gha_v1.g`
  - bytes: `7481`
  - SHA256: `9c4cab802845864f4bf11f4d996312ae82b58661f4b48536e6a0b721579f03a4`
  - ASCII-only: PASS
- この報告: `sol/luna_reply_162_k2_total_fibre_roster_producer_v1.md`

これは producer 資産であり、独立 checker ではない。数学的な fake/witness/Ihara claim の promotion はしていない。

## 2. producer lineage と frozen universe

`d972_rung_ordinary_idx3_producer_v2.py` の以下を明示的に再利用した。

- `G36`, `G9`, `PSL(2,8)`, `C3` の積・逆元・冪
- GAP right-action permutation convention
- `theta: x->y, y->x`
- `tau: x->y, y->(xy)^-1`
- deterministic right-Cayley `G36` transversal
- deterministic Schreier residual correction in `PSL(2,8) x C3`
- derived subgroup reconstruction and finite closure primitive

したがって fixed-row36 producer と同じ実装系統であり、producer/checker firewall 上の independent replay ではない。この事実は出力 JSON の `producer.lineage` にも明記される。

roof order は word-key artifact の zero-based row `0..971` を `X0001..X0972` とした。別資産の preflight `T...` order とは同一視しない。word-key の全 target key が frozen tuple roster と逐語・同順序で一致すること、全972 target word が `G9 x PSL(2,8)` で target を replay することを fail-closed にした。

各 target について、同じ reduction law

```text
m mod 36 -> m mod 18
G36       -> G9   (各 rotation exponent mod 9)
PSL(2,8)  -> PSL(2,8) identity map
C3        -> 1
```

の raw fibre を、`2` 個の m-lift、`8` 個の G36-lift、`3` 個の C3-liftの積として deterministic order でちょうど48点列挙する。全体の構造的 raw count は `972*48=46656` である。

## 3. 全 raw 点で評価する predicate

各46,656点について短絡せず、次をすべて materialize する。

1. exact target reduction
2. signed source word の `G36 x PSL(2,8) x C3` replay
3. charming unit `gcd(2m+1,36)=1`
4. charming commutator membership（`G36` derived membership、perfect PSL factor、C3 exponent zero）
5. first hexagon `f theta(f)=1`
6. second hexagon `tau^2(y^m f) tau(y^m f) (y^m f)=1`
7. onto for generators `x^(2m+1)` and `f^-1 y^(2m+1) f`

`stage` は上記順の first-failure label だが、後段の predicate も省略せず計算・保存する。

onto の `G36 x C3` 成分は候補ごとの巨大 Cayley BFS を行わず、exact に次で求める。

- 2 generator の quotient は `V4` を生成する。
- kernel は `a^2`, `b^2`, `(ab)^2` とその4個の `V4` conjugates が生成する `C18^3 x C3` の加法部分群である。
- 各 p-primary presentation の maximal minors の最小 p-valuation（Smith invariant と同値）から kernel order を exact に計算する。
- 小 modulus の6ケースで generic closure BFS と exact equality を selftest した。

`PSL(2,8)` 成分は完全 closure order を計算する。両成分とも同一生成対は exact cache するが、判定を近似・サンプリングにはしていない。

## 4. 出力契約

GHA full 走の唯一の result path は次である。

```text
ci/out/d972_k2_total_fibre_roster_v1_20260825.json
```

主な field は次のとおり。

- `per_target`: 972 target の frozen tuple、48 raw ID、observed valid fibre。valid fibre は ID だけでなく exact `[m,f]` と signed word を含む。
- `raw_roster`: 全46,656点の stable raw ID、exact `[m,f]`、signed word、reduction、全 predicate、first-failure stage。
- `valid_roster`: 全 valid 点の stable `K2V......` ID、exact `[m,f]`、signed word、target/raw provenance。
- `coordinate_to_valid_id`: canonical compact JSON の `[m,f]` から stable valid ID への全 lookup。
- `valid_count_histogram`: full 走で観測された per-target valid count の histogram。
- `claim_cover`: target/raw/evaluated/rejected/valid counts、全 reason histogram、`no_early_stop=true`。
- `roster_digests`: target/raw/valid/lookup の canonical SHA256。

artifact には wall-clock time を入れていないため、同一入力・同一 source では canonical bytes が再現可能である。実行時間は log のみに出す。

## 5. fixed-row36 lineage control

full 走の終了前に zero-based row36 の48点を authenticated prereg/receipt に対して replay する。

- exact source coordinates
- exact signed words と word SHA
- first-failure stages と histogram
- fixed receipt が実際に計算した nonzero onto component/PSL orders

いずれかが異なれば result は書かれない。この control は producer lineage の整合性試験であり、independent cross-check ではない。

## 6. input pins

Python producer は次の13本を byte count/SHA256 で fail-closed に pin する。

| path | bytes | SHA256 |
|---|---:|---|
| `search/d972_rung_ordinary_idx3_producer_v2.py` | 54993 | `b8dd453f7647dacc87356b13cb5428674a21bfabe6aa5af3850ac89129eb7211` |
| `search/certs/nf972_sourcemap_a_tuples_v2_20260804.json` | 43751 | `cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801` |
| `search/certs/d972_b4_word_key_artifact_v1_20260816.json` | 176474 | `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9` |
| `search/certs/d972_rung_ordinary_idx3_prereg_v2_20260824.json` | 46928 | `1273f6050afaaba01f8dc137042ae191cecd91dea44a1618f665c2e3048e4656` |
| `ci/ordinary_idx3_artifacts_32682548731/d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json` | 62680 | `48512270d265753944ff9b86d19fa5e84095ffffd8ae78beba969088c31053e9` |
| `search/certs/b3_gentle_source_census_preflight_v1_20260823.json` | 887124 | `c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2` |
| `crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json` | 4931 | `e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e` |
| `certificates/K36.v1.json` | 727834 | `feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719` |
| `crosscheck/verdicts/K36.v1.verdict.json` | 71093 | `4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b` |
| `certificates/K9.v1.json` | 173224 | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` |
| `crosscheck/verdicts/K9.v1.verdict.json` | 20991 | `9c299baba6cd3c49296621ecfe5efbc260d7971fa874f44465fa5e968cc065f9` |
| `certificates/S4.v2.json` | 287984 | `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d` |
| `crosscheck/verdicts/S4.psl.verdict.json` | 470 | `8d9d98965e270c2130b56fd6240c3b7460fe906ef5523f5e90396280dd043b28` |

GHA wrapper はさらに producer 自身と `.github/workflows/gap-run.yml` (`11346`, `7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763`) を pin する。

## 7. selftest / destructive controls

ローカルで実行したのは軽量 selftest と syntax/static audit のみである。

```text
python -B search/d972_k2_total_fibre_roster_producer_v1.py --selftest
D972_K2_TOTAL_FIBRE_ROSTER_SELFTEST_PASS mutations=8 small_component_cases=6 inputs=13
```

mutants/controls:

- noncommuting signed word reversal
- raw row deletion
- duplicate raw ID
- lookup deletion
- forged per-target valid histogram
- broken per-target raw binding
- first-hexagon bit mutation
- exact-reduction bit mutation

Python AST parse: PASS。GAP `ReadAsFunction` parse-only: syntax errorなし（top-level wrapper を function body として読むことによる expected unbound-global warnings のみ）。wrapper ASCII audit: PASS。full 972x48 run は未実行。

## 8. GHA launch contract

既存 `gap-run.yml` に渡す値:

```text
script: search/d972_k2_total_fibre_roster_gha_v1.g
preamble: <empty>
out_dir: ci/out
timeout_min: 120
with_pquot_packages: false
```

wrapper は selftest/full subprocess の exit sentinel、forbidden diagnostics、Python terminal の exact-one occurrence、result の存在、schema/status/coverage semantics、result 内 terminal の exact-one occurrenceを順に検査する。成功時の最終 marker は次である。

```text
D972_K2_TOTAL_FIBRE_ROSTER_GHA_V1_FINAL result=ci/out/d972_k2_total_fibre_roster_v1_20260825.json python_terminal_count=1 result_terminal_count=1
```

想定時間は GHA でおおむね `5–20 min`、余裕をみた timeout は `120 min`。git/GHA 操作は行っていない。

`K2_TOTAL_FIBRE_ROSTER_PRODUCER_V1_GHA_READY`
