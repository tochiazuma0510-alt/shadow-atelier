# Luna reply 168: g760 Jennings legal-coefficient certificate v1

Date: 2026-08-27  
Role: Luna / implementation and bounded serial mechanical audit only

## 1. Outcome

Task 168 の全番号節を順に処理した。task167 final v5 を変更せず、その `build_full` が completed-j checkpoint を認証した後だけ terminal D2 delta chain を再生し、次の 28 座標系を解く versioned adapter を追加した。

```text
A_j = {a in F3^28 : target_j - sum_i a_i legal_row_{j,i} in D2_j}
```

実装は `rank_L`、canonical free-zero particular、canonical reduced kernel basis、nullity、`0<1<2` の exact lex-first を返す。original D2 echelon への直接 replay、frozen Schreier words からの語の実体化、三 context、projected Sigma、D2 零剰余も要求する。複数 MEMBER j では新 particular と全 kernel vectors を直前系へ代入して affine-family inclusion を確認する。

Actual full j=9 D2 closure は委嘱どおりローカル実行していない。従って actual A9 の係数・kernel・語はまだ UNKNOWN であり、今回完成したのは「本計算一回で completed j=9 直後に同じ job から A9 を返せる producer/checker」である。

## 2. New assets

| asset | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_760_l3_target6_legal_coefficients_v1.py` | 57,792 | `7db4e174dec13e2f69f4011b09abcc52320699261b164b5eedb18a53fa64b962` |
| `crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py` | 49,633 | `a54383185601e8251b7cbac87b6c57f89d3a8df8519cb93014b08a3893825e25` |
| `search/d972_r07_760_l3_target6_legal_coefficients_gha_driver_v1.g` | 19,176 | `bad7911b0958983aacd541bb682b0f14a2903de02cecfc01043b593b17ab1e16` |
| `search/certs/d972_r07_760_l3_target6_legal_coefficients_preflight_v1_20260827.json` | 6,833 | `f390f53e6fc840f41009eb31beab519e36b4989b49ac70f9c8f4df7b32776138` |

Schemas:

```text
main = d972-r07-760-l3-target6-legal-coefficients/v1
per-j = d972-r07-760-l3-target6-legal-coefficient-certificate/v1
checker = d972-r07-760-l3-target6-legal-coefficients-check/v1
```

Per-j outputs are `ci/out/d972_r07_760_l3_target6_legal_coefficients_v1_j09.json` through `j12.json`。Concrete word field 名は指定どおり厳密に `C13_overapproximation_correction_candidate` とした。

## 3. Pins and noninterference

Task167 final pins:

| input | bytes | SHA-256 |
|---|---:|---|
| v5 producer | 108,142 | `94184831ede05c78d7206e62dbdd5c564daa493330fe1c5e433be2804267652b` |
| v5 driver | 29,496 | `ff820866983c1d1bc5d0a98bb748d4a7fda4e406b3283e6c6a6ccf817011be20` |
| v5 preflight | 36,718 | `76da0c9f78f3efff305289bb864e25819a722c2362dc2dffb250c98be9244305` |
| task167 | 7,170 | `3b885303f4bf512fc7a9a8e3f124f87a91ca4f3c7728920ee420d781dbe23e8c` |
| reply167 | 11,832 | `6412ceb1f9e415fc863a46eb9de30314157a73c20bb8374e3c3d9a16e1c10475` |

Task168 と proof v105/v106 も pin し、v5 `build_context` が全 inherited v1--v4、q3、prior/base/target/legal bindings を認証する。Preflight records:

```text
inherited_v5_pin_manifest_sha256
= 3db1ed35031b17d1af4150f03d03d7977c8c970232d0238422c7c0c62d381ed6
inherited_v3_fixed_bindings_sha256
= 2c868f9dd69663a0e673a2e857be82eb61235ab10838ee8396bf29e7086f6fde
```

V5 の traversal、relator/pivot insertion order、Jennings projection、exact caches、rank、target、membership、first-terminal rule は不変である。Completed row があるのに係数抽出が失敗すれば process を fail closed し、空の成功 receipt にしない。

作業は pinned inputs の clean overlay `%TEMP%/d972_task168_clean_overlay_v1` で行い、live-tree CLAIMS drift を隔離した。v1--v5、workflow、proof、CLAIMS、Sol reply は変更していない。git/push/GHA dispatch も行っていない。

## 4. Solve, lex proof, and word replay

D2 では provenance を追わず quotient-zero とし、28 legal coordinates だけを追跡する。Reduced quotient columns/target は coefficient-1/2 bitplanes で lossless serialize し、ordered rows、target、ambient equation matrix/rhs、RREF、kernel、terminal D2 commitment、relator-11 record、completed-j record、public-row digest を別々に bind する。

Lex-first は arbitrary RREF particular ではない。RREF から particular `p` と kernel basis `k_r` を得ると全解はちょうど `p + sum t_r k_r`。座標 1..28 で 0,1,2 の順に、その prefix を延長する parameter `t` の存在を exact F3 RREF で判定して最小値を採る。より小さい解があれば最初に違う座標で reject 済みの値を持つので矛盾する。

速度のため、prefix ごとに ambient の多数の equations を再消去せず、高々28次元の kernel-parameter 系だけを消去する。解・順序・lex rule は同一で、producer 90 系と checker 70 系の exhaustive small-F3 照合で固定した。

語は frozen order のまま

```text
c_j = s_1^(a_1) ... s_28^(a_28), a_i in {0,1,2}
```

とし、2 は同じ signed word を正方向に二回連結する。Free cancellation 以外はしない。語自身から三 context、Fox/Sigma、ordered legal sum、`target-Sigma` の D2 zero remainder を再計算する。

Bounded j=2 word replay hashes:

```text
coefficients = 4ee1934d973d1f8df8aee652bc618e9db22f97115f43e72499e0257c43351895
word         = b2ce31956bd0f1e0d03137fabd7a707dc6304f1948046e1945bed031df2f0125
Sigma        = 8cea29a5241307538e333742e0edcafe96ff3579d49126be7be16a89e03c9706
```

さらに actual j=9 Jennings basis/28 columns と、target 一本だけを pivot とする synthetic D2 を使い、11 delta checkpoints、completed-j checkpoint、係数抽出、空語、三 context、Sigma、D2 零剰余を本番 path で通した。Fixture の `rank_L=20`, `nullity=8`, lex-first zero は **synthetic D2 の数値であり actual A9 の数値ではない**。

## 5. Independent checker

Checker は新 producer/helper を import しない。Producer は read-only bytes/hash pin のみである。旧 helper-nonshared v2 checker から frozen 28 words/rows、target、Jennings projection、F3 solve、word/context/Sigma を独立再構成する。

D2 だけは許可どおり pinned v5 lossless delta chain と completed-j JSON chain を認証・再生する。従って格付けは `coefficient extraction conditional on authenticated v5 D2 state` であり、649,539 translated rows の独立再列挙は別 promotion gate である。

Depth inclusion は rank 比較でなく、新 particular を previous affine system へ、新 kernel vectors を previous homogeneous system へ直接代入する。Lex stabilization は data としてのみ記録する。

## 6. Bounded serial audit

Producer:

```powershell
python -u -B search/d972_r07_760_l3_target6_legal_coefficients_v1.py --self-test
```

```text
R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PRODUCER_SELFTEST_PASS random_exhaustive=90 mutations=11 completed_j_next=10 safe_stop_ancestor_counted=false full_j9_local=false
```

Checker:

```powershell
python -u -B crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py --self-test
```

```text
R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_CHECKER_SELFTEST_PASS random_exhaustive=70 mutations=11 synthetic_full_certificates=1 helper_shared=false full_D2_local=false
```

Both implementations rejected 11 mutation classes: coefficient, kernel basis, target, D2 splice, legal-row reorder, word order, word sign, context, Sigma, false global claim, false actual-domain boundary. Tests also cover inconsistent/member systems, nontrivial kernels, all-zero legal rows, and a free-zero particular `(1,0)` whose lex-first is `(0,1)`。

Preflight was generated twice serially from the clean overlay:

```text
R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PRODUCER_PASS state=R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PREFLIGHT_READY grade=CANDIDATE certificates=0 sha256=f390f53e6fc840f41009eb31beab519e36b4989b49ac70f9c8f4df7b32776138 bytes=6833
```

Both bytes were identical. Final pinned path regeneration gave the same bytes/hash.

GAP driver:

```powershell
& .\gap.ps1 search\d972_r07_760_l3_target6_legal_coefficients_gha_driver_v1.g `
  -ExtraArgs @('-c','D972_R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_SELFTEST:=true;;')
```

```text
R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_GHA_DRIVER_PASS mode=selftest producer_processes=1 checker_processes=1 driver_fixture_mutations=6 grade=CANDIDATE helper_shared=false
```

All tests were serial. No full closure or parallel local Python/GAP was run.

## 7. Full-run terminal/resource contract

One job runs: unchanged v5 traversal -> authenticated relator-11 delta -> authenticated completed-j -> same Python invocation coefficient extraction -> serial helper checker.

```text
v5 inner monitor       18000 s
producer outer         18600 s
checker outer            900 s
workflow               21600 s
required margin         1800 s
default max relators      11
processes              1 producer + 1 checker, serial
```

Inherited terminal tokens remain exactly:

```text
R07_760_L3_TARGET6_NONMEMBER
R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE
R07_760_L3_TARGET6_UNKNOWN_RESOURCE
R07_760_L3_TARGET6_INPUT_STOP
```

If j=9 is MEMBER and the 11-relator allowance is reached, v5 returns authenticated `UNKNOWN_RESOURCE` safe stop after the j9 checkpoint; the adapter then appends A9 in the same invocation. This does not alter terminal semantics.

Unchanged generic workflow already uploads `ci/out/`。However it does not automatically download a previous run's artifact, so cross-run resume works only when checkpoints are preseeded; automatic ingress remains operational UNKNOWN.

## 8. Remaining UNKNOWNs

1. Actual full-D2 j=9 run and actual A9 coefficients/kernel/word.
2. Direct helper-nonshared re-enumeration of all 649,539 translated D2 rows.
3. Intersection with the smaller actual common-word correction image.
4. Literal A.18 and two-hexagon joint replay.
5. Cofinal actual-word compatibility.
6. Actual A.18 lift, fake, or Ihara witness.
7. Automatic cross-run GHA artifact ingress.

No full j=9 computation was run locally. No GHA run was dispatched. No git operation was performed.

## 9. Required boundary, verbatim

```text
coefficient certificate = C-13/full-K overapproximation data only
j=9 nonmember=false is producer survival evidence, not an A18 lift
actual common-word domain intersection is still required
MEMBER != actual A18 lift
no fake / cofinal lift / Ihara witness declared
```

Every main/per-j/checker receipt also fixes:

```text
actual_common_word_domain_intersection_computed = false
literal_A18_replayed = false
two_hexagons_replayed_as_joint_system = false
cofinal_compatibility_proved = false
```
