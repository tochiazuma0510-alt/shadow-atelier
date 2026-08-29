# Sol task 374 — independent pre-A0 A3/v3 static code/performance reaudit

## 結論

**STATIC REJECT.** frozen physical owners、canonical P0 と 23-owner authority graph、v303-only projection、producer の単一 closure、十二 mutation の ordinary validator 構造は静的に通る。しかし、現在の checker は load-bearing evaluator build の最初で必ず停止する。また、31 MB receipt の重複処理、mutation ごとの full-object deepcopy、内部 wall deadline の未被覆、pre-rename rollback の directory fsync 欠落がある。従って一件の pre-A0 A3/v3 GHA も許可しない。

本監査では task374 の禁止を守り、candidate、Python、Node、GAP、GHA、workflow、git、network、syntax compilation を一度も実行していない。使用したのは read-only PowerShell による byte inspection、JSON source inspection、SHA-256 と行番号付き source 読みだけである。以下は実行結果ではなく frozen code の静的裁定であり、Lean の意味での「検証」ではない。

## 1. Frozen physical identities

全 5 owner は指定 byte length / SHA-256 と exact match した。

| frozen owner | bytes | SHA-256 | 判定 |
|---|---:|---|---|
| `ci/in/d972_r07_pre_a0_single_target_a3_v3.prereg.v1.json` | 16,417 | `2660c8e1dce475d19f4d8a40f43626df401d3ca299f34b0f1dd067db896d2ce6` | exact |
| `search/d972_r07_pre_a0_single_target_a3_v3.py` | 95,172 | `436e7c06acff9cf2087277a12067371518c2ce033effaf85bff6b04585c0f9cf` | exact |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v3.py` | 106,148 | `eaaa9d602da22921991f25229eed559c50a920a30c3c56495b0954b40af03485` | exact |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v3.g` | 20,110 | `63126f5c0c1c2278656a5a2a77fab4d1562af0566e9bca54a85b090cbcc3783e` | exact |
| `sol/sol_reply_370_r07_pre_a0_a3_v3_complete_finite_repair.md` | 18,965 | `619c1bb857cdb5c5b4633594bccc7b5ef447f7e19ee3adc683607b1404a43645` | exact |

task363/task369/task370 と各 full reply、v302/v303、accepted task198 authority/evaluator owners、pinned task226/task227 producer/checker ownersを全て通読した。task370 実装者の自己監査には依存していない。

## 2. Canonical P0 と complete acyclic authority graph

P0 は先頭 `{`、末尾 `}`、BOM 0、CR 0、LF 0、非 ASCII byte 0 の compact ASCII JSON である。top-level `self_digest_sha256` を除いた canonical body は 16,329 bytes、SHA-256 は宣言値どおり

`0539e586fd6001ff65965e990461f390fc8868bb6fbbd0ec2a9cd4464f91df0e`

であり、物理全体の SHA-256 も上表どおりである。P0 line 1 の `authority` を source から再帰走査し、ordinary `{path,bytes,sha256}` record だけを全列挙した結果は次の 23 unique owners / 33,121,619 bytes であった。inventory 宣言を合計値の根拠には用いていない。

| authority owner | bytes | SHA-256 |
|---|---:|---|
| `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json` | 231,570 | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json` | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt` | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json` | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.json` | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt` | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| `crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py` | 35,463 | `e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44` |
| `crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py` | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| `crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py` | 34,200 | `028e615bd71276c22cea2180b8ff59e53d8e9ee745c84a1912c862f217f2bb95` |
| `search/check_d972_b345_joint_kernel_qstar_closure_v1.py` | 47,661 | `9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f` |
| `search/check_d972_b345_seedspan_triple4_v1.py` | 574,347 | `ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981` |
| `search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py` | 33,409 | `f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f` |
| `search/d972_b345_joint_kernel_qstar_closure_v1.py` | 67,945 | `06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc` |
| `search/d972_b345_seedspan_triple4_v1.py` | 535,219 | `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29` |
| `search/d972_r07_760_l3_target6_v1.py` | 53,284 | `7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde` |
| `search/d972_r07_actual_two_word_endpoint_specializer_v2.py` | 40,556 | `a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb` |
| `search/d972_r07_all_seven_extension_section_census_v1.py` | 66,109 | `878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b` |
| `search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g` | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |
| `search/d972_r07_seven_context_roof_presentation_v1.py` | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| `search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g` | 5,387 | `38352fd53e2aa2534e6b4d61c5a613c38fd65c4a6843fa5cb6dd2a04918cfe7d` |
| `search/d972_r07_typed_single_seed_endpoint_consumer_v2.py` | 47,135 | `755ba97e55266bcdb51796cc1a89a562efa782db48475d0e3479e82e325cde8e` |
| `sol/proof_r07_a18_area_invisibility_single_a3_target_v302.md` | 7,340 | `ba508bbe96f34967ebe456c51285ecbe774861a864c369699bbf1dce2b9fc6c3` |
| `sol/proof_r07_pre_a0_computational_base_equivalence_v303.md` | 6,739 | `9868aa26d630138da9b8b963b0f3968e8c2ee698ba4461d596a2b6f155d25cf2` |

23 files とその現物 ancestor directories は ordinary regular file/directory で、reparse/symlink alias はない。producer 478--516 / checker 432--470 は duplicate、inventory missing/extra、P0/candidate/driver cycle を拒否し、両 `load_p0` は exact P0 pin と canonical seal を拘束する（producer 519--575、checker 473--530）。producer/checker の source pins は P0 authority inventory に再結合される（producer 578--599、checker 533--554）。driver 2--4, 15--22 は P0 と最終 producer/checker identity を pin する。従って

`immutable authorities -> canonical P0 -> producer/checker -> driver`

は一方向であり、v2 hash、partial digest、missing/key-skipped owner、duplicate path、post-freeze cycle はない。

## 3. task198 authority と live evaluator

### Authority binding

producer 656--821 と checker 634--787 は同じ P0 authority から accepted receipt、manifest、member、producer/checker attestations、checker verdict、source identities、run/head/artifact/zip を ordinary route で照合する。accepted receipt は 31,017,244 bytes、SHA-256 `82f795...b19f5`、body self seal `c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f`。manifest self seal は `0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684`、evaluator contract digest は `4fc38881ffee293f0820d3639230dd44a2af9b9ed126dfb21dc5831290ff08b8` である。11-row ledger digestは `040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7`。この authority decoding 自体は PASS。

### Exact callable/call trace

producer は live registry を 1201--1206 で取得し、direct call sites は 1219--1227 の 9 calls:

`eval(g760), eval([1]), eval([2]), multiply(x,y), inverse(x), inverse(g760), source_section(2,2), action([1],y), section_cocycle([1],[2],[1,2])`。

従って direct roster は `eval=3, multiply=1, inverse=2, source_section=1, action=1, section_cocycle=1`。accepted producer source 719--823 の nested calls を展開すると transitive roster は `eval=6, multiply=4, inverse=3, source_section=1, action=1, section_cocycle=1` である。

checker は producer summary を callable evidence にせず、checker authority functions を 1395--1402 で直接束ね、1416--1424 で同じ 9 direct calls を行う設計である。accepted checker source 968--1075 を展開した checker-side transitive roster は `eval=8, multiply=4, inverse=3, source_section=1, action=1, section_cocycle=1`。producer-compatible trace と checker actual trace は 1457--1497 で分離されている。

coordinate widths は exact `[40,40,40,40,40,154,154,154,154,154]`。occurrence binding は次のとおりで、各 value は sign `+1` なら `eval(g760)[ten_index]`、`-1` なら `inverse(eval(g760))[ten_index]` に拘束される（producer 1241--1254、checker 1438--1451）。

| ordinal / occurrence | ten index | width bytes | sign | orientation |
|---|---:|---:|---:|---|
| 1 `H1_fxy` | 0 | 40 | +1 | direct |
| 2 `H1_fxz` | 1 | 40 | -1 | inverse |
| 3 `H1_fyz` | 2 | 40 | +1 | direct |
| 4 `H2_fux` | 3 | 40 | -1 | inverse |
| 5 `H2_fxy` | 0 | 40 | -1 | inverse |
| 6 `H2_fuy` | 4 | 40 | +1 | direct |
| 7 `P_b1` | 5 | 154 | +1 | direct |
| 8 `P_b2` | 6 | 154 | +1 | direct |
| 9 `P_b3` | 7 | 154 | +1 | direct |
| 10 `P_b5_inverse` | 8 | 154 | -1 | inverse |
| 11 `P_b4_inverse` | 9 | 154 | -1 | inverse |

`x/y/xy/x_inverse/source/action/cocycle` の full ten-coordinate arrays は accepted receipt canaries と value equality で拘束され（producer 1228--1240、checker 1425--1437）、`g760` とその inverse を含む全 values は receipt/verdict に省略せず保持する設計である。candidate 未実行なので、それらを観測値とは主張しない。

### F1 — load-bearing checker API mismatch

checker `Meter` が定義する wall method は **`check` のみ**である（200--219、特に 214）。ところが `EvaluatorBudget.check` は存在しない `self.meter.check_wall(...)` を呼ぶ（1294--1300）。この adapter は 1315 で生成され、checker build は 1341 で frozen task176 `build_fine_deletion` に渡す。frozen task176 435--437 は最初の `sid=0` で直ちに `budget.check("fine_deletion")` を呼ぶため、これは遅い corner case ではなく ordinary checker の必達 `AttributeError` である。

main の typed UNKNOWN catch 2250--2252 に `AttributeError` は含まれず、verdict/terminal は publication されない。driver 139--145 は exact-one checker terminal を得られず非受理になる。従って checker evaluator、projection、mutations、`verify_gate` は現 owner では到達不能であり、TASK198 LIVE EVALUATOR と INDEPENDENT CHECKER ROUTE は REJECT。

## 4. v303-only projection と closure/verifier

frozen task227 producer `validate_abi` 138--147 と checker `check_abi` 124--139 の全 field read を列挙すると次で尽きる。

- top level: `schema`, `modulus`, `ten_to_eleven`, `occurrences`, `bar_epsilon_1`, `u0`;
- occurrence: `ordinal`, `combined_block`, `q_degree`, `key_width`, `factor_sign`, `p_o`, `q_o(x)`, `q_o(y)`, `xi_o`, `w_o`, `translated`, `u0`, `ancestry`, plus presence of `rword_g`, `rword_f`, `fox_prefix_occurrences`, `orientation`; orientation の値は direct/inverse として読む;
- combined `u0` row: `ordinal`, `terms`, `translated_terms`, `source_coefficient_terms` と original provenance の ancestry。

producer 1408--1514 / checker 1165--1254 はこの exact consumer body を projected v303 interface だけから作る。`rword_f/rword_g` は frozen code が `field in row` しか検査せず値を計算に使わないので、`V303_OMITTED_NOT_CONSUMED` は正当な presence-only marker である。full-package-only `B_a`、PB chain、literals、actual `rword_f`、task192 ancestry は consumer ABI へ入らない。v303 proof の pre-A0 computational-base equivalence boundaryを越えない。

producer の load-bearing closure call は 2024 の一回だけ。返却物は 2030--2033 で exact 486/729 を要求し、frozen `encode_gate` は ancestry、basis/echelon、rank、coefficients、replay 又は dual を保持する。checker の独立 `verify_gate` call site は 2094--2095 の一回だけで、full reconstruction は frozen checker 185--214 にある。wrapper reverse comparison は 0。

frozen verifier の `compare_sparse_spans` は一 call 内で両包含を検査する（95--110）のに、frozen line 198 は 6 unordered pairs を正逆 12 calls で比較する。従って内部に 6 redundant reverse calls があり、block-image lists も ideal を 4 回、translates を 2 回 materialize する（NONMEMBER dual passes はさらに追加）。これは開示済み frozen dependency cost であり、v3 wrapper が追加した second closure/verifier ではない。`independent_verify_calls=1`, `frozen_internal_span_comparison_calls=12`, `wrapper_reversed_span_calls=0` の区別は正しい。

## 5. Untouched baseline と十二 mutation routes

producer 1631--1757 / checker 1573--1688 の local mutation logic を、実 route と exact first reason まで追跡した。

| mutation | ordinary route | exact first reason |
|---|---|---|
| `task198_raw_manifest_binding` | `authenticate_task198` | `task198 raw/manifest binding` |
| `task198_ledger_sign` | `validate_ledger_owner` | `task198 ledger sign` |
| `task198_prefix` | `validate_ledger_owner` | `task198 ledger prefix` |
| `g760_letter_digest` | `validate_g760_owner` | `g760 digest` |
| `computational_base_mode` | `validate_base_owner` | `computational-base mode` |
| `forbidden_task192_binding` | `validate_base_owner` | `task192 binding` |
| `H1_central_row` | `central_replay` | `H1_central_row` |
| `H2_central_row` | `central_replay` | `H2_central_row` |
| `P_central_row` | `central_replay` | `P_central_row` |
| `projected_area_target` | `target_from_fox` | `projected area target` |
| `ABI_seal_target` | reseal + `validate_projection` | `ABI seal/target` |
| `forbidden_conclusion_flag` | `validate_false_flags` | `forbidden conclusion flag` |

ordinary baseline は production で先に構成済みの rows/g760/base/central/area/projection owners を用い、mutation harness 内でも producer 1638--1646 / checker 1580--1588 で mutation 前に通す。各 mutation は changed-owner digest inequality を要求し、narrow expected exceptions だけを reason に変換する。`MutationAccepted` は main で hard nonaccepting status 4、wrong first reason は fail closed。従って mutation semantics の局所構造は PASS とする。ただし checker 全体では F1 によりこの場所へ到達しない。また次節の重複処理と deadline defect は別の load-bearing performance REJECT である。

P0、receipt top/result/gate、checker verdict、driver acceptance の全層で 8 false flags を false に拘束する。特に `actual_a3_numerator=false` は欠落不可であり、この静的 code は actual numerator、A0、cofinal lift、fake、Ihara を主張しない。

## 6. Resource arithmetic と avoidable work

### Source-derived formulas

| quantity | independent formula | bytes / seconds | 判定 |
|---|---|---:|---|
| immutable authority | 23-owner sum | 33,121,619 | exact |
| authority + P0 | `33,121,619 + 16,417` | 33,138,036 | `< 40,000,000` |
| producer source imports | `535,219+67,945+66,109+137,169+40,556+47,135` | 894,133 | exact |
| producer input | `16,417+33,121,619+2*894,133` | 34,926,302 | `< 60,000,000` |
| checker source imports | `535,219+574,347+47,661+66,109+157,253+35,463+34,200` | 1,450,252 | exact |
| checker before receipt | `16,417+33,121,619+2*1,450,252` | 36,038,540 | exact |
| checker + max receipt | `36,038,540+19,000,000` | 55,038,540 | `< 60,000,000` |
| producer normal serializer | `3*19,000,000+65,536` | 57,065,536 | exact component bound |
| producer normal + emergency charge | `57,065,536+4*65,536` | 57,327,680 | cap exact |
| checker verdict serializer | `3*1,000,000+65,536` | 3,065,536 | exact component bound |
| checker private Q0 retained | `5*1,469,664` | 7,348,320 | exact |
| checker private Q0 construction | `2*7,348,320` | 14,696,640 | exact component peak |
| hard address-space ceiling | `RLIMIT_AS` requested cap | 4,294,967,296 | hard upper ceiling |
| wall | internal / each external / serial external | 1,800 / 2,100 / 4,200 s | `1800<2100`, `2*2100=4200<21600` |

全 authority/source physical reads は `read_bytes` で read 前 reserve される（producer 399--430、checker 353--384）。dynamic imports は authenticated pre-read bytes を `compile(raw)` / `exec` し（producer 1760--1788、checker 1691--1718）、loader の hidden source read は 0、post-read も別 charge する。従って `2*source` input 式は物理 read と一致する。accepted 31 MB receipt は各 process で disk から一回だけ読み、raw map は candidate result DOM より前に解放する。

fixed-point の old bytes / JSON text / new bytes の `3N` と streaming chunk charge、65,536-byte emergency reserve、checker Q0 bytearray-to-bytes 二重生存式は source と一致する。これは process 全体の Python allocator/RSS 証明ではないが、Linux `RLIMIT_AS` が全体の hard ceilingで、RSS sample は boundary telemetry にすぎないと明記される。task226 は各 side base 1 build + preregistered area 3 builds、producer closure 1、checker verifier 1 で、hidden second build/closure はない。

### F2 — 31,017,244-byte receipt の重複 DOM/canonical work

baseline `authenticate_task198` は producer 663 / checker 641 で accepted receipt を `json.loads` し、producer 667--675 / checker 645--653 で full canonical comparison と body seal traversal を行い、raw SHA も producer 682, 809 / checker 660, 776 で重ねて計算する。

raw-manifest mutation は小さい manifest だけを変更するのに、producer 850 / checker 817 で同じ full `authenticate_task198` を再呼出しする。expected mismatch は producer 803 / checker 772 の route 最後まで現れないため、その前に 31,017,244-byte receipt をもう一度 parse して巨大 DOM を作り、sealed/raw canonical traversals と raw SHA を繰り返す。物理 disk read の重複ではないが、各 side 一回ずつの巨大 DOM 再構築と複数の 31 MB pass は明確に avoidable である。

### F3 — mutation ごとの full-owner deepcopy

`mutation_fixture` は producer 1585--1594 / checker 1528--1536 で `target_constructor_owner` を含む全 reference を deepcopy する。この引数は caller で full task226 ABI そのもの（producer 2014--2017、checker 2012--2015）。さらに roster の残り 11 件すべてで、対象 owner 一個だけを変える前に reference 全体を deepcopy する（producer 1648--1649、checker 1590--1591）。従って full ABI、interface、consumer、areas、base、central を、最初の fixture copy を含め **各 side 12 回** full-copyする。full ABI が必要なのは projected-area mutation 一件だけであり、owner-local copy に分けられる。この per-item full-object copying は GHA を不必要に遅くし、AVOIDABLE DUPLICATED PROCESSING を REJECT にする。

### F4 — internal signal deadline が material mutation work を覆わない

raw authority mutation には outer `WallDeadline` がある（producer 1968--1970、checker 2203--2205）。しかし残り 11 routes を呼ぶ `run_mutations` は producer 2014--2017 / checker 2012--2015 で `WallDeadline` 外である。各 full `deepcopy(reference)` は meter check より前（producer 1649 対 1712、checker 1591 対 1644）に行われ、actual validator call（producer 1715、checker 1647）も signal timer 内にない。projection/seal materialization（producer 2008--2009、checker 2006--2007）も同じ untimed interval にある。

次の meter call が elapsed excess を拒否するため 1,800 秒超の accepting telemetry は作れないが、個々の copy/mutation call を 1,800-second signal で interrupt する保証はなく、2,100-second external timeout まで走り得る。task374 §6 の「elapsed-adjusted signal deadline が every expensive mutation/build を cover」を満たさない。timer restoration 自体（producer 352--361、checker 307--316）は旧 timer から実経過を差し引いており正しい。

以上により算術式そのものは exact でも、STATIC CAPS / PERFORMANCE と AVOIDABLE DUPLICATED PROCESSING は REJECT。

## 7. Bound publication と serial driver

### 正常 publication route

両 writer は output を `ci/out` direct child に限定し、repo-root -> `ci` -> `out` を `O_DIRECTORY|O_NOFOLLOW` の dirfd chain で開く（producer 1835--1862、checker 1793--1820）。temp は同じ bound `out` fd に `O_CREAT|O_EXCL|O_NOFOLLOW` で作り、complete write、file fsync 後、source/destination とも同じ fd の `renameat2(..., RENAME_NOREPLACE)` を用い、成功時は directory fsync する（producer 1865--1904、checker 1823--1862）。Linux/RLIMIT/signal/`renameat2` assumptions は producer 365--385 / checker 320--339 で fail closed。stale final/temp と UNKNOWN は accepting terminalにならない。

driver は producer/checker exact-one terminal（86--92, 139--145）、terminal equality（146）、receipt SHA injection（96--99, 136--137）、checker 後と最終の receipt rehash（147--148, 203--204）、validated exact verdict bytes の digest と post-validation verdict rehash（152--206）、23 authority identities と P0/result/projection/evaluator/mutation/rank cross-bindings（154--200）を sentinel 前に要求する。sentinel は root/ci/out dirfd chain上の exclusive no-follow create、file/directory fsync、failure unlink+fsync である（207--234）。driver subroute 自体は PASS。

### F5 — pre-rename temp rollback に directory fsync がない

writer の post-rename failure branch は final を `unlink(..., dir_fd=directory)` した後 directory fsync する（producer 1911--1915、checker 1869--1874）。しかし `renamed == False` branch は temp を unlink するだけで directory fsync を行わない（producer 1917--1922、checker 1875--1880）。write、file-fsync、close、又は rename failure はこの branch に入り、temp directory-entry removal の durability が契約上閉じない。task374 §7 が明示する「rollback under every typed/untyped failure + directory fsync」を満たさないため、成功経路と driver が正しくても BOUND PUBLICATION / SERIAL DRIVER の総合判定は REJECT。

## 8. 一回の versioned repair に必要な全 load-bearing 修理

1. checker `EvaluatorBudget.check` の呼出先を実在する `Meter.check` に一致させ、fresh owner で checker evaluator build から `verify_gate` までの reachability を再監査する。
2. raw-manifest mutation を ordinary authority validator に残しつつ、既に認証済みの 31 MB receipt resultを stage/cacheするか、manifest binding failure を巨大 receipt 再parseより前に同じ ordinary routeで判定し、baseline 内の重複 raw SHA も再利用する。
3. mutation fixture を owner-local copy に分け、full task226 ABI/reference 全体を各 case で deepcopy しない。
4. projection/sealing と全 mutation copy/validator routes を elapsed-adjusted `WallDeadline` 内に置く。
5. pre-rename temp unlink 後にも同じ bound directory fd を fsyncし、rollback error は accepting pathへ戻さない。

この 5 群を新 versioned owners と P0/hash/resource disclosure に反映し、fresh independent static auditをやり直すまで GHA は禁止する。

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
P0 / ACYCLIC AUTHORITY GRAPH:          PASS
TASK198 AUTHORITY / LIVE EVALUATOR:    REJECT
V303-ONLY PROJECTION SUFFICIENCY:      PASS
ONE PRODUCER CLOSURE ROUTE:            PASS
INDEPENDENT CHECKER ROUTE:             REJECT
BASELINE + TWELVE MUTATIONS:           PASS
STATIC CAPS / PERFORMANCE:             REJECT
AVOIDABLE DUPLICATED PROCESSING:       REJECT
BOUND PUBLICATION / SERIAL DRIVER:     REJECT
PRE-A0 A3/V3 GHA:                      FORBIDDEN
ACTUAL A3 NUMERATOR:                   remains 0/3
A0 / COFINAL LIFT / FAKE / IHARA:      NONE

TASK374_R07_PRE_A0_A3_V3_CODE_PERFORMANCE_REAUDIT_V1
