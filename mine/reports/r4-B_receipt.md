# 判定 receipt -- r4-B

- 生成: 2026-07-30T15:08:39.529026+00:00 (UTC)
- 生成器: `mine/collector/receipt.py`(P88-R4-2 恒久処方 -- sol_reply_88_math15.md SS2)
- window_id: `W-E-A20-5x4t0-B`

## 出所(fail-closed 検査済み)

- prediction-doc: `docs\notes\r4_prediction_v1.md` (SHA-256 `a991f65a8c84a553b4d730a39cb3591c42e3fd6f3bfa05c2292fd56b2d66b78f`, 期待値と一致)
- prediction-map: `mine\collector\r4_prediction_map_v1.json` (source_sha256 が prediction-doc と一致)
- cert: `search\certs\r4_W_E_A20_5x4t0_B_20260730.json` (SHA-256 `620c97f5310203781b38e67b85949e6832d05d34489d989aa279f35e4e358236`)
- manifest: `search\certs\r4_manifest_B_20260730.json` -- windows[].outfile='r4_W_E_A20_5x4t0_B_20260730.json' の cert_sha256 束縛と実 SHA-256 が一致(検査 PASS)
- manifest の S0 entry gate 束縛: entry_gate_file='search/certs/r4_gate_20260730.json', entry_gate_all_pass=True (束縛あり)

## 予言欄(凍結文書からの引用のみ -- 実測値は書かない)

出典: `docs/notes/r4_prediction_v1.md` (SHA-256 `a991f65a8c84a553b4d730a39cb3591c42e3fd6f3bfa05c2292fd56b2d66b78f`)

| 予言ID | 予言(引用) |
|---|---|
| P-R4-0 | canonical ID SHA-256 が窓表と一致し、窓 assert が全項 PASS |
| P-R4-1 | |ker chi~| = 40 (B枝・C枝とも) |
| P-R4-2 | |ker chi~| の奇部 = 5 |
| P-R4-3 | |ker chi~| の2-部 = 8 かつ Syl_2(ker) ≅ D8 |
| P-R4-4 | Xi(ker)の奇部 = <xbar>(全対角)であり、B_x 座標が (a,a,a,a) 型 |
| P-R4-5 | ker chi~ ≅ C5 x D8, IdGroup=[40,10] |
| P-R4-6 | GTSh(N,N) の IdGroup=[160,207] かつ |GTSh|=160 かつ dl=2 |
| P-R4-7 | |Q| = phi(5) = 4, Q ≅ C4 が <xbar> に忠実 |
| P-R4-8 | B枝とC枝で |ker|・奇部・2-部・|GTSh|・IdGroup が全一致 |
| P-R4-9 | Xi: GTSh -> N_{S20}(<xbar>) が ker Xi=1、像が N(60000) の部分群 |
| P-R4-10 | u=-1 層に位数2かつSを中心化するshadowがちょうど2ell=10個 |
| P-R4-11 | (奇部,2-部) が SS3.0 表のいずれかの行に一致する(ker = C_B(S')xS' の形が保たれる) |

## 実測欄(cert JSON からのみ機械抽出)

| 欄 | 値 |
|---|---|
| `generated_by` | `"search/strike-r4.g"` |
| `window_id` | `"W-E-A20-5x4t0-B"` |
| `n` | `20` |
| `ell` | `5` |
| `r` | `4` |
| `t` | `0` |
| `a1` | `"( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16)"` |
| `b1` | `"( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16)"` |
| `s1` | `"( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15)(16,17,18,19,20)(21,22)"` |
| `s2` | `"( 1,18,16, 6, 3)( 2,14, 5, 4,13,20, 9, 8,19,15)( 7,12,17,11,10)(22,23)"` |
| `canonical_string` | `"W-E-A20-5x4t0-B|n=20|ell=5|r=4|t=0|a1=( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16)|b1=( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16)|S1=( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15)(16,17,18,19,20)(21,22)|S2=( 1,18,16, 6, 3)( 2,14, 5, 4,13,20, 9, 8,19,15)( 7,12,17,11,10)(22,23)"` |
| `canonical_id_sha256` | `"093b8b32d239de2a363b170b692e3f72ab3e9433d403e1587d54fef2eb54b586"` |
| `canonical_id_sha256_gate` | `"093b8b32d239de2a363b170b692e3f72ab3e9433d403e1587d54fef2eb54b586"` |
| `stage1_all_pass` | `true` |
| `N_ord` | `5` |
| `0_canonical_id` | `"W-E-A20-5x4t0-B"` |
| `1_eps_branch` | `"eps1_fibre"` |
| `1b_stage1_asserts_ok` | `true` |
| `2_group_order` | `2000` |
| `3_ker_size` | `500` |
| `4_ker_odd_part_order` | `125` |
| `5_ker_2_part_order` | `4` |
| `6_ker_odd_part_primes` | `[5]` |
| `7_K_struct` | `"C5 x C10 x D10"` |
| `7b_K_idgroup` | `[500, 53]` |
| `7b_K_idgroup_note` | `null` |
| `8_K_is_direct_product` | `false` |
| `9_A_order` | `125` |
| `9_A_idgroup` | `{"idgroup": [125, 5]}` |
| `10_S_struct` | `"C2 x C2"` |
| `10_S_order` | `4` |
| `11_chi_image_order` | `4` |
| `11_Q_struct_invariant_factors` | `[4]` |
| `12_Q_action_faithful_on_A` | `false` |
| `13_gtsh_idgroup` | `{"idgroup": [2000, 931]}` |
| `14_derived_length_G` | `2` |
| `15_derived_series_G` | `[2000, 125, 1]` |
| `16_Stab_order` | `15000` |
| `16b_Syl2_Stab_struct` | `"D8"` |
| `16b_Syl2_Stab_order` | `8` |
| `17_xbar_normalizer_order` | `60000` |
| `18_xi_alpha_well_defined` | `true` |
| `19_xi_hom_left` | `false` |
| `19_xi_hom_right` | `true` |
| `19_xi_hom_check_exhaustive` | `true` |
| `20_xi_kernel_trivial` | `true` |
| `20_distinct_alphas` | `2000` |
| `21_xi_image_order` | `2000` |
| `21b_xi_image_in_normalizer` | `true` |
| `22_Bx_order` | `625` |
| `22_Bx_gen_cycles` | `"[ [ 1, 3, 5, 7, 9 ], [ 2, 4, 6, 8, 10 ], [ 11, 13, 15, 12, 14 ], [ 16, 18, 20, 17, 19 ] ]"` |
| `22b_A_coords_status` | `"computed"` |
| `22b_A_coords_count` | `125` |
| `23_S_block_status` | `"computed"` |
| `24_ZS_order` | `4` |
| `25_G_over_CG_S` | `5` |
| `26_Inn_S_order` | `1` |
| `27_H3_holds` | `false` |
| `28_compl_classes_all` | `4` |
| `29_compl_classes_in_CG_S` | `4` |
| `30_epsilon_zero` | `true` |
| `31_z_in_Frattini` | `null` |
| `32_central_product_witness` | `null` |
| `33_split_but_not_direct` | `false` |
| `34_u_minus1_involutions` | `100` |
| `34_m0_layer` | `4` |
| `35_xi_count_measured_per_m` | `[112500000, 112500000, 112500000, 112500000]` |
| `35b_xi_count_bound_per_m` | `112500000` |
| `36_xi_count_measured_total` | `450000000` |
| `36b_xi_count_bound_total` | `450000000` |
| `shadow_total` | `2000` |

(全欄は cert 原本を参照。上表は `stage1_asserts` / `37_shard_manifest` / `note` を省略した抜粋。)

## 恒等式 assert(要件2 -- cert に該当欄がある場合のみ評価)

| ID | 恒等式 | 左辺 | 右辺 | 判定 |
|---|---|---|---|---|
| ID-1 | |G| = |K| |Q| | 2_group_order=2000 | 3_ker_size * 11_chi_image_order = 500*4=2000 | PASS |
| ID-2 | |K| = |K|_odd |K|_2 | 3_ker_size=500 | 4_ker_odd_part_order * 5_ker_2_part_order = 125*4=500 | PASS |
| ID-3 | |Xi(G)| = |G| | 21_xi_image_order=2000 | 2_group_order=2000 | PASS |
| ID-4 | layer sum = total | sum(35_xi_count_measured_per_m)=450000000 | 36_xi_count_measured_total=450000000 | PASS |

## 派生判定欄(予言欄 x 実測欄の比較結果のみ -- 値そのものは上の2欄を参照)

| 予言ID | 判定 | 内訳 |
|---|---|---|
| P-R4-0 | PASS | measured={'canonical_id_sha256': '093b8b32d239de2a363b170b692e3f72ab3e9433d403e1587d54fef2eb54b586', 'canonical_id_sha256_gate': '093b8b32d239de2a363b170b692e3f72ab3e9433d403e1587d54fef2eb54b586', 'stage1_all_pass': True} predicted='canonical_id_sha256 の期待値は窓ごとに R4_CANONICAL_SHA (strike-r4.g) / prediction doc SS1.1 に凍結済み -- ここでは cert 自身の canonical_id_sha256_gate 欄(driver がその場で束縛した期待値)と canonical_id_sha256 の一致、および stage1_all_pass=true を見る。' |
| P-R4-1 | **FAIL** | measured=500 predicted=40 (3_ker_size) |
| P-R4-2 | **FAIL** | measured=125 predicted=5 (4_ker_odd_part_order) |
| P-R4-3 | **FAIL** | 5_ker_2_part_order: measured=4 predicted=8 [MISMATCH]; 10_S_struct: measured='C2 x C2' predicted='D8' [MISMATCH] |
| P-R4-4 | NULL | measured=None predicted=None (cert に座標リスト本体が無い(22b_A_coords_status='computed' はカウントのみで literal 配列は別ファイル r4_acoords_{B,C}_20260730.json 側)。receipt.py は cert 単体からは判定しない -- NULL として記帳。) |
| P-R4-5 | **FAIL** | measured=[500, 53] predicted=[40, 10] (7b_K_idgroup) |
| P-R4-6 | **FAIL** | 13_gtsh_idgroup: measured={'idgroup': [2000, 931]} predicted={'idgroup': [160, 207]} [MISMATCH]; 2_group_order: measured=2000 predicted=160 [MISMATCH]; 14_derived_length_G: measured=2 predicted=2 [OK] |
| P-R4-7 | PASS | 11_chi_image_order: measured=4 predicted=4 [OK]; 11_Q_struct_invariant_factors: measured=[4] predicted=[4] [OK] |
| P-R4-8 | NULL | measured=None predicted=None (単一 cert からは判定不能(両枝の cert が要る)。receipt.py は単一 branch receipt では NULL として記帳する。) |
| P-R4-9 | PASS | 20_xi_kernel_trivial: measured=True predicted=True [OK]; 21b_xi_image_in_normalizer: measured=True predicted=True [OK]; 21_xi_image_order: measured=2000 predicted='= 2_group_order (2000)' [OK] |
| P-R4-10 | **FAIL** | measured=100 predicted=10 (34_u_minus1_involutions) |
| P-R4-11 | **FAIL** | measured=[125, 4] predicted=[[5, 8], [5, 4], [25, 4], [25, 2], [125, 2], [625, 1]] (4_ker_odd_part_order,5_ker_2_part_order) |

## 集計まとめ

- 派生判定: PASS 3 / FAIL 7 / NULL 2 (全 12 予言)
- 恒等式 assert: FAIL 0 / NULL(欄なし) 0 / 全 4

(本 receipt は cert JSON の値と凍結 prediction-map の引用値の機械照合であり、候補判定であって裁定ではない。裁定は人(司令塔/研究者)が行う。)
