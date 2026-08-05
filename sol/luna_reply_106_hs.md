# Luna 返書 106-HS — 最終追補（class-freeze 小 gate 再提出）

## 総合判定

**PASS（exact draft に対する class-freeze gate）。**

初回提出の BLOCKED 判定は、外部実行環境での current-source 再較正と、その後の二回の停止記録を経て解消した。独立差分監査の対象となった exact draft は次で固定されている。

| 項目 | exact 値 |
|---|---|
| class ID | HS-NW7-CLASS-v3-draft-2c5c1559812c5d9b |
| component bundle SHA-256 | 2c5c1559812c5d9b8dccd9f0ca5b74a7d288fc18508c3872dea3f2c3798c02d7 |
| draft file | search/certs/hsp7_class_manifest_v3_draft_20260805.json |
| draft file SHA-256 | 48364db7d82aa8000096058f07c321a2003ada6655d84cd4544548428d37e31b |
| superseding source commit | a9a653e9a82f4dd93ca9eabec085a03af931b26e |
| 実行環境 | GAP 4.16.0 / ANUPQ 3.3.3 |

ここで PASS は「この exact bytes/components を frozen 化してよい」という class-freeze 適格性の判定であり、Luna が frozen artifact を発行した、または探索を開始した、という意味ではない。現ファイルはなお schema hsp7-class-manifest-draft/v1、status READY_FOR_SOL_FREEZE_REVIEW で、authorization の main_run / workflow_dispatch / calibration_shard / claim_grade_promotion は全て false である。

親からの境界訂正に従い、本追補では frozen manifest を作らず、workflow を .github へ設置せず、fresh frozen-path preflight も実行していない。main shard、較正 shard、705,894 対の main sweep、未登録候補、workflow dispatch、claim-grade 昇格への接触は全て 0 である。実 dispatch は後記の workshop 手順を完了した工房だけが行える。

## 1. P/S/V runnable wrapper と実 cert

三 wrapper は would-write stub ではなく、hsp7-lane-cert/v3 の実 JSON を書く production 経路である。current source に対する登録 fixture 再較正 v4 は次をすべて満たした。

- S 13、V 13、P 8、P5 control 5 は全て exit 0。
- 比較 8 項目は全て true: S/V/P の登録 baseline 一致、S=V、V の N/N0 全一致、P5 の CONV/native 5 一致、ordered-PCGS core の S=P と S=V。
- SHARD mode は一度も呼ばれず、receipt schema field は candidate_universe_contact=0。

  この 0 の正確な意味は **main/unregistered sweep contact 0** である。registered fixtures は既知宇宙元に対する許可済み較正なので、literal set-theoretic な「candidate 元への接触 0」とは呼ばない。

- runtime ordered-PCGS fingerprint は S/P/core =
  ff2e40c93bf3b547f34dabb0ab7ee6ea1fa2e46dd67bcca43c59fec5158726d3、
  V（S→V bridge 材料込み）=
  eaf54f528795c7831ab4a1b52d4c5e7578f0e93633c2332bfd9428b4b0503889。

実 lane cert の SHA-256 は次である。

| lane | cert SHA-256 |
|---|---|
| S | 11813961c83d8db77905b54ab0e5eac61b6de935d9f84151371517a2a8c81eea |
| V | 64215fb4f67955bf035702586968f22456a53b32f6f238b4846d00c53762b7fb |
| P | d786797d563e6b955fd5b77bfa41b69b670e067fd7f7507d8179c9e8a0edfdc9 |

aggregate は search/certs/hsp7_registered_wrappers_preflight_pcgs_v4_20260806.json、SHA-256
4dc9464d7e8be153ced72bd19887f5e7f5fad13cd1f714bb54cad410e98db60e で overall_pass=true である。

## 2. CF / CONV-P と registered fixture の主経路統合

Lane V は CF の N/N0 両式と baseline を named fixture ごとに照合し、定義域生成、像生成、well-defined、bijective、S→V の六 pcgs 生成子の逐点 bridge を fail-closed gate に含む。Lane P は checked epi、Q の構造 anchor、rho の bijective/order-5/nonidentity、CONV の生成像一致と全単射、native element と verdict の二重比較を含む。

最初の ordered-PCGS 修理で誤って置いた pairNontrivial 条件は撤回した。この rank-2/class-4 P では D=[P,P] が可換なので、六 named D-generator の 15 pair commutator coordinate row が全て 0 なのは正しい。現在の anchor は、それだけで自己循環しないよう、ambient Pcgs(P) 内の x/y と ordered six D generators、PQ source artifact path/SHA、theta/tau の action rows、非恒等性・可逆性、および S→V pointwise bridge を束にしている。

v4 aggregate が pin する source_commit_sha は a9a653e9a82f4dd93ca9eabec085a03af931b26e。本追補時に同 receipt の source_commit_files 22 件について live blob と commit blob を再比較し、22/22 exact byte match を確認した。

## 3. semantic join と binding mutant

join_checker.py は GAP helper、candidate_key_lib.g、wrapper を import せず、manifest の radix/width/m-list から次を独立再導出する。

1. flat pair index と (m,e1,...,e6) の双方向変換。
2. Lane P の一つの f-index から六つの pair-index/candidate-key への展開。

人工 join fixture は 15/15 expectation match、canonical reorder hash も一致した。receipt は search/certs/hsp7_join_fixtures_v2_20260805.json、SHA-256
09a9ee1a27faff46581da743dc24ccccd638295600aa322b61cebf3690865f9d。

class/workflow/cert/receipt/cap の pure binding matrix は 71/71 expectation match（positive 11、tamper-negative 60）、candidate_universe_contact=0。receipt は search/certs/hsp7_binding_negative_matrix_v2_20260805.json、SHA-256
84626520e6c9319b46b75dad73af7d940e14fca4ec9edcb2ee51d9e220554914。

## 4. exact shard、workflow、STOP/UNKNOWN

versioned prereg v3 と Appendix C v3 は exact universe と次の唯一の partition を登録する。

| lane | axis | total | shard size | shards | final range |
|---|---:|---:|---:|---:|---|
| S | pair | 705,894 | 3,678 | 192 | [702498,705893] |
| V | pair | 705,894 | 54,000 | 14 | [702000,705893] |
| P | f | 117,649 | 3,678 | 32 | [114018,117648] |

全 lane は max-parallel=20、256 job/run 以下。runtime PCGS BASIS_ONLY は候補非接触の 15 分 hard timeout、本 shard は 60 分、outer job は回収余白込み 90 分である。digest/range/count/fingerprint/integrity/driver_done の不一致、GAP nonzero、cert/receipt 欠品、partial shard は全て STOP。fatal error を UNKNOWN に格下げせず、自動 retry も行わない。

workflow template は search/probe/hsp7_mainrun/hsp7_mainrun_workflow_v3.yml。freeze sentinel を正規化した SHA-256 は
41b29577479b51a4b9b3b06ffb4d62465afb2e256fab96c42714518dec6615cd。
これは .github/workflows/hsp7-mainrun-class-v3.yml へ未設置で、dispatch 0 である。

## 5. 候補非接触 capacity

各 lane 20,000 の deliberately invalid synthetic row を production record shape で serialize/gzip し、predicate/group 呼出し 0 で測定した。これは主走性能の測定ではなく線形外挿である。

| lane | raw extrapolation | gzip extrapolation |
|---|---:|---:|
| S | 124,239,922 B | 7,979,711 B |
| V | 193,417,749 B | 8,171,164 B |
| P | 27,179,406 B | 1,317,675 B |
| total | 344,837,077 B | 17,468,550 B |

cap は per-shard raw 20 MiB、各 lane compressed 680 MiB = 713,031,680 B、三 lane 合計 2,139,095,040 B、whole class compressed 2 GiB = 2,147,483,648 B。retention は 30 日。超過時は upload 前 STOP とし、truncate/sample/negative deletion はしない。

receipt は search/certs/hsp7_capacity_noncontact_v2_20260805.json、SHA-256
7eca4369d728ca8ea616e2d042906ea351a560c370278c4657efd3228165642f。

## 6. class manifest draft と静的検収

exact draft は predicate/wrapper/conversion/schema/checker/source-map、ordered-PCGS runtime material、semantic key、exact universe/range、sharding、STOP/UNKNOWN、join、exposure/negative-result、capacity/retention、workflow normalized template を一つの component bundle に束縛する。

static audit は 35/35 true、candidate_evaluations=0。receipt は search/certs/hsp7_bundle_static_audit_v2_20260805.json、SHA-256
91ddfd77091eb38e22d6ced64686003ae6683fe4d079dfef0bbf409b6cd66a80。

draft path/SHA に対する S/V/P の preflight-only はすべて PASS、各 candidate_evaluations=0 である。

| lane | draft preflight SHA-256 |
|---|---|
| S | 3e6cfa38572fe51491c05257f780c0673a7b227f1ff0524ce243f624c83b4c3c |
| V | b53200ddb47b8d9bd2466c7a74af47e4f10c0ca2404f5111c3b0fcfb7ec15747 |
| P | fcecfa6b264114a5e5acf370e265ea27577d6171bb85d4957b7d69c3c6376e44 |

ただし、これらは visible draft path/SHA に対する receipt であり、workshop が frozen file を作った後の最終 receipt には引用できない。frozen path/new SHA に対する fresh candidate-0 preflight が別途必要である。

## 7. 停止記録と supersession

停止記録を消さず、次の順で会計する。

1. 初回 managed Windows では GAP/Cygwin の signal-pipe error で実登録評価 0。この初回 BLOCKED は本節の監査履歴として要約保存する。
2. ordered-PCGS v2 は誤った pairNontrivial guard で STOP。実装 bug であり数学的非一致ではない。
3. v3 は BASIS_ONLY fingerprint を三 lane で得た後、条件分岐内の top-level 専用 QUIT; が parse STOP。REGISTERED cert は 0。immutable FAIL aggregate は search/certs/hsp7_registered_wrappers_preflight_pcgs_v3_20260805.json、SHA-256
   8b4773b8516e87821713e17248821669fd4e2aeda229148f52fd3dce60a6849d。
4. v4 はその三箇所だけを GAP 4.16 callable QuitGap(0); へ直した versioned retry。current source 22/22 byte binding の下で §1 の PASS を得た。

従って v3 FAIL を v4 で上書きせず、v4 を superseding receipt とする。main/production cert 0 は blocker ではない。class 認可前に main cert を要求すると循環するためである。

## 8. workshop handoff — dispatch 前の機械 5 条件

独立監査が指定した条件をそのまま固定する。

1. exact draft bytes/components から新しい versioned frozen manifest を作る。class ID と component bundle を維持し、status=FROZEN_AUTHORIZED、main_run=true、workflow_dispatch=true、calibration_shard=false、claim_grade_promotion=false とする。
2. frozen file の新しい SHA-256 を計算する。draft SHA-256 を流用してはならない。
3. exact workflow を .github/workflows/hsp7-mainrun-class-v3.yml へ置き、承認済みの二 sentinel だけを frozen path/new SHA に変更する。normalized digest
   41b29577479b51a4b9b3b06ffb4d62465afb2e256fab96c42714518dec6615cd
   を維持し、class_lock_checks を PASS させる。
4. 全参照 components/manifests/certs と frozen workflow を一緒に commit し、dispatch は workshop だけが行う。他の byte/source/schema/range/cap/output を変更した場合は再 gate とする。
5. dispatch 前に frozen path/SHA に対する fresh candidate-0 --preflight-only receipt を取る。現 visible draft receipt は最終 receipt に引用しない。run receipt には GAP 4.16.0、ANUPQ 3.3.3、resolved action revisions を記録する。

この五条件は workshop handoff であり、本 Luna turn では実行していない。特に frozen manifest の機械生成、workflow install、dispatch は親 broker/工房の権限境界に残した。

## 9. 主な digest

| artifact | SHA-256 |
|---|---|
| prereg v3 | 84b186ec2d83be2ec3d2afd07734e254422bba93e3ca35df1266e08220c81ac0 |
| Appendix C v3 | 541e233490fef5651000ccbe179c0596ed0f6db0c3f7edb04931d1bab48329dd |
| class manifest draft | 48364db7d82aa8000096058f07c321a2003ada6655d84cd4544548428d37e31b |
| v4 registered aggregate | 4dc9464d7e8be153ced72bd19887f5e7f5fad13cd1f714bb54cad410e98db60e |
| v3 immutable FAIL aggregate | 8b4773b8516e87821713e17248821669fd4e2aeda229148f52fd3dce60a6849d |
| binding matrix v2 | 84626520e6c9319b46b75dad73af7d940e14fca4ec9edcb2ee51d9e220554914 |
| join fixture receipt v2 | 09a9ee1a27faff46581da743dc24ccccd638295600aa322b61cebf3690865f9d |
| capacity receipt v2 | 7eca4369d728ca8ea616e2d042906ea351a560c370278c4657efd3228165642f |
| static audit v2 | 91ddfd77091eb38e22d6ced64686003ae6683fe4d079dfef0bbf409b6cd66a80 |
| normalized workflow template | 41b29577479b51a4b9b3b06ffb4d62465afb2e256fab96c42714518dec6615cd |

全 component/source/shard digest は class manifest 自身に機械列挙されている。

## 10. 実行・変更境界

本走/未登録 sweep 非接触の実行は registered fixture、synthetic join/binding/capacity、static audit、draft preflight-only に限定した。v4 外部較正は GAP 4.16.0 / ANUPQ 3.3.3、exit 0。探索本走、main matrix、較正 shard、未登録候補、封印値、workflow dispatch は 0。

今回の最終追補で新たに変更したのは sol/luna_reply_106_hs.md だけである。frozen manifest、freeze receipt、frozen-path preflight receiptは作っていない。commit/push/credential 読取も行っていない。source provenance は親 broker の commit a9a653e9a82f4dd93ca9eabec085a03af931b26e による。

---

## 11. artifact commit の exact path 会計

親 broker の consolidation commit は、class manifest の components 45 path を全て exact bytes で含めた上で、次の component 外生成物も含める必要がある。

### 11.1 current class の必須生成物

~~~text
docs/notes/hsp7_mainrun_prereg_v3.md
docs/notes/hsp7_mainrun_prereg_v2_appendixC_v3.md
search/certs/hsp7_lane_cert_schema_v3.json
search/certs/hsp7_binding_negative_matrix_v2_20260805.json
search/certs/hsp7_capacity_noncontact_v2_20260805.json
search/certs/hsp7_join_fixtures_v2_20260805.json
search/certs/hsp7_laneP_registered_preflight_20260805.json
search/certs/hsp7_laneS_registered_preflight_pcgs_v4_20260806.json
search/certs/hsp7_laneV_registered_preflight_pcgs_v4_20260806.json
search/certs/hsp7_laneP_registered_preflight_pcgs_v4_20260806.json
search/certs/hsp7_registered_wrappers_preflight_pcgs_v4_20260806.json
search/certs/hsp7_shard_manifest_laneS_v3_20260805.json
search/certs/hsp7_shard_manifest_laneV_v3_20260805.json
search/certs/hsp7_shard_manifest_laneP_v3_20260805.json
search/certs/hsp7_class_manifest_v3_draft_20260805.json
search/certs/hsp7_bundle_static_audit_v2_20260805.json
search/certs/hsp7_class_preflight_laneS_v4_20260806.json
search/certs/hsp7_class_preflight_laneV_v4_20260806.json
search/certs/hsp7_class_preflight_laneP_v4_20260806.json
search/probe/hsp7_mainrun/hsp7_mainrun_workflow_v3.yml
sol/luna_reply_106_hs.md
~~~

S/V の旧 registered lane cert、旧 aggregate、CF calibration receipt、PQ artifacts、gap.ps1、mainrun source は components 45 path に含まれるので、その機械列挙を正とする。特に current normative schema は v3 であり、SHA-256 は
af6a54a3ab7ffe2d9e94bde57658e3bb0dd37a27abe9a1e87e732e2da9fe7477。

### 11.2 immutable STOP history と schema v2

次は current component bundle の判定入力ではないが、versioned audit history として同じ reachable history に残す。

~~~text
search/certs/hsp7_registered_wrappers_preflight_pcgs_v2_20260805.json
search/certs/hsp7_registered_wrappers_preflight_pcgs_v3_20260805.json
search/certs/hsp7_lane_cert_schema_v2.json
~~~

- v2 FAIL SHA-256:
  2de579fc05ae5ad3301843bb0f6fcfc573e0e4b2b0df543ebfa80b4ed8891b0b。
- v3 FAIL SHA-256:
  8b4773b8516e87821713e17248821669fd4e2aeda229148f52fd3dce60a6849d。
- schema v2 SHA-256:
  b4d124a68e4decf99320ebe3b3b565c7c181cf106e86f4295f083d2dbb5a0930。

schema v2 は freeze の normative schema ではなく class component bundle に加えない。しかし歴史的 hsp7-lane-cert/v2 の S/V/P cert が source_bindings.schema_sha256 としてこの値を pin するため、archival dependency として commit する。

### 11.3 join fixture の再現資材

join receipt を再現できるよう、次の exact 15 fixture も source と一緒に含める。

~~~text
search/probe/hsp7_mainrun/join_fixtures/common_permutation.json
search/probe/hsp7_mainrun/join_fixtures/driver_not_done.json
search/probe/hsp7_mainrun/join_fixtures/duplicate_key.json
search/probe/hsp7_mainrun/join_fixtures/good.json
search/probe/hsp7_mainrun/join_fixtures/good_p.json
search/probe/hsp7_mainrun/join_fixtures/missing_candidate_key.json
search/probe/hsp7_mainrun/join_fixtures/missing_shard.json
search/probe/hsp7_mainrun/join_fixtures/overlap.json
search/probe/hsp7_mainrun/join_fixtures/p_expansion_mismatch.json
search/probe/hsp7_mainrun/join_fixtures/p_key_permutation.json
search/probe/hsp7_mainrun/join_fixtures/pcgs_endian_mismatch.json
search/probe/hsp7_mainrun/join_fixtures/receipt_missing_field.json
search/probe/hsp7_mainrun/join_fixtures/reorder.json
search/probe/hsp7_mainrun/join_fixtures/same_flat_index_different_key.json
search/probe/hsp7_mainrun/join_fixtures/wrong_m_semantics.json
~~~

### 11.4 除外する superseded/一時物

次は current class から参照されず、v2/v4 で supersede された unversioned 中間出力なので consolidation commit へ入れない。

~~~text
search/certs/hsp7_binding_negative_matrix_20260805.json
search/certs/hsp7_bundle_static_audit_20260805.json
search/certs/hsp7_capacity_noncontact_20260805.json
search/certs/hsp7_class_preflight_laneS_20260805.json
search/certs/hsp7_class_preflight_laneV_20260805.json
search/certs/hsp7_class_preflight_laneP_20260805.json
search/probe/hsp7_mainrun/__pycache__/**
~~~

visible draft preflight v4 三件は commit 対象だが、§8 条件 5 の final frozen-path receipt の代用品ではない。v2/v3 FAIL は削除・上書きせず、v4 PASS とは別の immutable history として扱う。
