# Sol task 369 — independent pre-A0 A3/v2 static code/performance audit

## 結論

**STATIC REJECT.** 物理 owner 自体は指定 identity と一致し、v303-only projection、単一 producer closure、独立 checker closure route も静的には成立する。しかし、受理前提を壊す load-bearing defect が残る。

1. P0 の `g760_ancestry` 2 owner が両 Python と driver の pin walker から脱落する。
2. task198 evaluator は ABI 辞書を比較するだけで、ordinary route から一度も call されない。
3. 12 mutation は ordinary authority/replay validator を通らず、コピーした fixture の等値 validator を通る。
4. input/authority telemetry は上の脱落と import loader の暗黙 read を数えず、一部 closure counter も意味どおりに charge されない。
5. publication は parent directory fd を開くが、それに temp/create/rename/unlink を bind せず、driver も validation 後の verdict bytes を digest に再結合しない。敵対的 parent/substitution を排除する契約には足りない。

したがって fresh GHA は **FORBIDDEN**。本監査では task369 の禁止に従い、candidate、Python、Node、GAP、GHA、workflow、git、network は実行していない。使用したのは read-only PowerShell の byte inspection/SHA-256 のみである。commit label `180e305e` 自体は git 禁止のため照会せず、以下の物理 owner を直接監査した。

## Frozen physical owners

| owner | bytes | SHA-256 | result |
|---|---:|---|---|
| `ci/in/d972_r07_pre_a0_single_target_a3_v2.prereg.v1.json` | 13,748 | `4a7f966d803dfdf7977dc73ab2db9b7f54d0d932ec2a10e410e034b5b6b151af` | exact |
| `search/d972_r07_pre_a0_single_target_a3_v2.py` | 76,763 | `01578037cfabc73fdb7cb29d7725a41f903b05aab0f689d259fc89f56489daa6` | exact |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v2.py` | 84,273 | `3d77b6e6ca577bd762512b99a1ba2be647d994c4632b66ca2478259fea06f403` | exact |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v2.g` | 15,917 | `05ecedcf238fc55f758302a6210de0e32cf52c5d6304d3ad472007aba99c99b6` | exact |
| `sol/luna_reply_363_r07_pre_a0_a3_v2_complete_repair.md` | 19,513 | `942f470f4fb9234b1cd2e671542d022237df1fa70e972befe2f32193593ca7f4` | exact |

P0 は BOM/CR/LF/ASCII 外 byte/文字列外 whitespace が各 0、先頭 `{`、末尾 `}` の単一 canonical JSON byte stream である。top-level `self_digest_sha256` を除いた 13,660 bytes の canonical body SHA-256 は、宣言値どおり
`f633498efef1e8fb2adf02a474dcca05b87de83fe5655e1e805f8e10f1f916a4`。
両 wrapper の `raw == canonical(p0)` と seal pin（producer 445–480、checker 373–410）はこの exact P0 を受理し、余分な whitespace/BOM/改行を受理しない。P0 に rejected v1 owner hash はなく、新 v2 owner/driver も pin されていないので、向き自体は acyclic である。

P0 が意図する authority owner は次の 17 個、合計 31,598,768 bytes であり、全物理 bytes/SHA は P0 と一致した。

| authority owner | bytes | SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json` | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt` | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json` | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.json` | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| `ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt` | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| `crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py` | 35,463 | `e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44` |
| `crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py` | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| `crosscheck/check_d972_r07_typed_single_seed_endpoint_consumer_v2.py` | 34,200 | `028e615bd71276c22cea2180b8ff59e53d8e9ee745c84a1912c862f217f2bb95` |
| `search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py` | 33,409 | `f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f` |
| `search/d972_r07_760_l3_target6_v1.py` | 53,284 | `7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde` |
| `search/d972_r07_actual_two_word_endpoint_specializer_v2.py` | 40,556 | `a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb` |
| `search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g` | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |
| `search/d972_r07_seven_context_roof_presentation_v1.py` | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| `search/d972_r07_typed_single_seed_endpoint_consumer_gha_driver_v2.g` | 5,387 | `38352fd53e2aa2534e6b4d61c5a613c38fd65c4a6843fa5cb6dd2a04918cfe7d` |
| `search/d972_r07_typed_single_seed_endpoint_consumer_v2.py` | 47,135 | `755ba97e55266bcdb51796cc1a89a562efa782db48475d0e3479e82e325cde8e` |
| `sol/proof_r07_a18_area_invisibility_single_a3_target_v302.md` | 7,340 | `ba508bbe96f34967ebe456c51285ecbe774861a864c369699bbf1dce2b9fc6c3` |
| `sol/proof_r07_pre_a0_computational_base_equivalence_v303.md` | 6,739 | `9868aa26d630138da9b8b963b0f3968e8c2ee698ba4461d596a2b6f155d25cf2` |

## Line-numbered findings

### F1 — load-bearing: `g760_ancestry` の 86,693 bytes が authority walker から落ちる

P0 line 1 の `authority.g760_ancestry` は、上表の 33,409-byte checker と 53,284-byte producer の **path を object key** にし、値は `{bytes,sha256}` としている。一方、producer 433–442 と checker 361–370 の `iter_pins` は、値 object 自身に `path`、`bytes`、`sha256` の三 field がある場合しか yield しない。`authenticate_authority`（producer 498–518、checker 427–446）はその iterator だけを読むため、この 2 owner を open/hash しない。driver の generated Python collector も driver 162–168 行で同じ三-field predicate を複製しており、verdict の `source_identities` からも同じ 2 owner が落ちる。

したがって実装が物理認証するのは 15 owner、31,512,075 bytes だけである。物理ファイル自体は正しいが、「frozen authorities → P0 → wrappers → driver」という完全 graph は成立しない。これは P0/authority の REJECT 理由である。

### F2 — load-bearing: task198 evaluator ABI は call されない

task198 receipt/manifest/member/attestation/verdict/source link/self-seal の decode は producer 575–739、checker 526–690 にあり、receipt は各 process 一回だけ read/parse される。retained raw は 31,020,292 bytes（receipt 31,017,244 + manifest/attestations/verdict 3,048）、canonical comparison は 65,536-byte emitted chunk 単位で、producer 1616–1618 と checker 1762–1764 は次の result/receipt DOM より前に raw map を解放する。この部分と 11 occurrence ledger、40×5/154×5 coordinate widths の binding は静的に通る。

しかし ordinary route が呼ぶ `evaluator_exercise` は、producer 964–999 と checker 1131–1165 のどちらも `contract` の文字列、entry-point 名、width、ledger digest を比較して返すだけである。production の call site（producer 1636–1637、checker 1581–1582）まで含めて、task198 callable を一度も呼ばない。実 callable は frozen task198 producer の `roof_eval` 719、`roof_multiply` 752、`roof_inverse` 765、`roof_source_section` 777、`roof_action` 800、`roof_section_cocycle` 809、registry 819 行にあるが、新 wrapper が import するのは task226/task227 の二 module だけ（producer 1620–1621、checker 1565–1566）。`decoded_callable_bindings` や `*_convention_exercised` という出力名は実 exercise の証拠にならない。

よって task363 §4 と task369 §3 の「ordinary g760/base/central reconstruction で decoded evaluator を actually exercise」に反する。

### F3 — projection sufficiency と closure route は PASS

producer 1173–1223 / checker 1049–1095 の projection は full task226 package を deep-copy しない。frozen task227 が実際に読む値は次で尽きる。

- top-level: `schema`, `modulus`, `ten_to_eleven`, `occurrences`, `bar_epsilon_1`, `u0`;
- occurrence: `ordinal`, `combined_block`, `key_width`/derived width, checker 側 `q_degree`, `factor_sign`, `p_o`, `q_o(x)`, `q_o(y)`, `xi_o`, `w_o`, `translated`, `u0`, `ancestry`, `fox_prefix_occurrences`, `orientation`;
- `u0` row: `ordinal`, `terms`, `translated_terms`, `source_coefficient_terms` と、その ancestry。

frozen producer `validate_abi` 138–147 と frozen checker `check_abi` 124–139 は `rword_f`/`rword_g` の **存在だけ**を検査し、値を読む計算を持たない。従って `V303_OMITTED_NOT_CONSUMED` marker は presence-only compatibility marker として十分で、full-package value の偽装ではない。seal stripping、body/sealed digest、untouched baseline は mutation より先に通り、`ABI_seal_target` はその後に到達する。

producer は full package を 1644 行で解放し、minimal consumer だけを frozen task227 `closure` に 1646–1654 行で一回渡す。486/729、ancestry、basis/echelon/rank、coefficients、replay/dual は Boolean に潰さず gate に残る。checker は checker-side task226/task227 owner だけを import し、physical gate に full `verify_gate` を 1662–1673 行で一回呼ぶ。従って producer closure と独立 checker closure の構造は PASS である。

### F4 — known frozen duplicate work は開示済み、wrapper duplicate はない

frozen checker `check_d972_r07_typed_single_seed_endpoint_consumer_v2.py` 95–104 の `compare_sparse_spans(left,right)` は一回の call 内で両包含を検査する。それにもかかわらず frozen verifier 198 行は 6 unordered pair を正順/逆順の 12 calls で処理し、block-image list も繰り返し再構築する。従って frozen dependency 内には 6 redundant reverse calls がある。

ただし task363 156–163 は、この frozen-owner 内 duplicate を削除したと称さず、実数を報告する契約である。v2 wrapper は reverse call を追加せず、checker 1684–1692 と verdict/driver は `independent_verify_calls=1`, `frozen_internal_span_comparison_calls=12`, `wrapper_reversed_span_calls=0` を保持する。この frozen cost は将来の versioned task227 optimization 候補だが、今回の wrapper に hidden duplicate はない。task226 build も各 side で base 1 回 + 要求された area canary 3 回、closure/verifier は各 1 回である。

### F5 — load-bearing: mutation は ordinary validator を traverse しない

producer 1362–1365 / checker 1262–1265 は untouched cheap baseline を mutation より先に通す。各 mutation は別 deepcopy を変更し、`NarrowReject` だけを catch し、`MutationAccepted` と wrong-reason failure は catch 外（producer 1411–1425、checker 1285–1298）。P0 の exact first-reason roster も使う。この制御構造自体はよい。

しかし全 12 case が呼ぶのは `cheap_validate`（producer 1318–1356、checker 1218–1256）だけである。特に:

- `task198_raw_manifest_binding` は copied `manifest_contract.producer.member.sha256` を 0 にし、P0 snapshot との不一致で落ちるだけ（producer 1319–1325, 1369–1371、checker 1219–1225, 1269）。ordinary `authenticate_task198` の manifest→member→attestation→verdict binding は再実行しない。
- H1/H2/P mutation は copied `central.blocks` と copied `reference`/P0 rows の等値比較だけ（producer 1339–1344、checker 1239–1244）。ordinary `central_replay` を通らない。
- projected-area mutation も copied target/area summary の等値比較（producer 1345–1348、checker 1245–1248）で、closure が使う replay/target constructor を再実行しない。

従って extant owner を変えて「同じ ordinary validator」を通すという task363 240–250 / task369 73–75 の条件を満たさない。期待理由に合わせた parallel fixture gate であり、mutation matrix 全体を REJECT とする。

false conclusion flags 自体は 8 field を完全に持ち、`actual_a3_numerator=false` を含む。producer/checker と driver は accepted terminal 前に top/result/gate の false を要求するため、現コードが A0、actual A3 numerator、lift、fake、Ihara を宣言する経路はない。

### F6 — load-bearing: cap margin はあるが accounting が exact でない

source-derived byte formulas は次のとおり。

| quantity | formula | bytes |
|---|---|---:|
| intended P0 authority owners | 15 traversed + 53,284 + 33,409 | 31,598,768 |
| intended `authority_bytes`, P0 自身を含む | 13,748 + 31,598,768 | 31,612,516 |
| producer が現在 charge する input | 13,748 + 31,512,075 + 2×(40,556+47,135) | 31,701,205 |
| producer の現在の物理 source reads（loader read を追加） | 31,701,205 + 40,556+47,135 | 31,788,896 |
| producer、missing ancestry も認証した正しい物理式 | 31,788,896 + 86,693 | 31,875,589 |
| checker が現在 charge する input（receipt 前） | 13,748 + 31,512,075 + 2×(35,463+34,200) | 31,665,149 |
| checker の現在の物理 source reads（loader read を追加） | 31,665,149 + 35,463+34,200 | 31,734,812 |
| checker、missing ancestry も認証した receipt 前の物理式 | 31,734,812 + 86,693 | 31,821,505 |
| checker + 最大 producer receipt | 31,821,505 + 19,000,000 | 50,821,505 |

従って corrected totals でも `authority_bytes=40,000,000` と `input_bytes=60,000,000` には入る。しかし `load_engine` は authenticated pre-read、`exec_module` が行う暗黙 source read、authenticated post-read の三 read であるのに、meter は前後の二 read しか reserve/charge しない（producer 1432–1452、checker 1304–1322）。task363 194–196 の「every material read before use」を満たさず、reply363 の 31,701,205 / 31,665,149 は物理式ではない。

さらに CAPS にある `closure_actions` と `occurrence_support`（producer 46–56、checker 47–57）は ordinary success route で一度も bump されない。producer closure は actor/orbit/rank/block/dual 等を charge するが、この二 counter は real closure/support work があっても 0 のままで、semantically honest counter ではない。checker が opaque verifier を `independent_verify_calls=1` とし、完了後に exact 486/729/ranks を count する設計は正しい。

output は producer `19,000,000 + 65,536 = 19,065,536`、checker `1,000,000 + 65,536 = 1,065,536` を `serialized_bytes=20,000,000` 内で事前 reserve する。fixed-point serializer（producer 1466–1495、checker 1373–1402）は logical output を一度だけ charge し、sealed `serialized_bytes` を最終長に一致させる。反面、反復時には旧 encoded bytes、次の JSON text、次の encoded bytes が一時共存し得るため、encoded-payload 部分だけでも概ね `3N`（producer cap なら約 57 MB、checker 約 3 MB）の allocation envelopeを見込む必要がある。DOM/辞書/list/allocator overhead を含む actual RSS peak は static source から数値確定できず、実行時 boundary sample だけが証拠になる。

Linux `RLIMIT_AS=4,294,967,296` は producer 1612 / checker 1759 で heavy import/build/closure/verifier より先に hard ceiling として入る。RSS は hard interrupt ではなく boundary sample と明記される。`signal.setitimer` は 1,800-second remaining process budget で expensive region を interrupt する。ただし既存 timer が非零なら `WallDeadline.__exit__` は経過時間を差し引かず元の remaining を再設定する（producer 306–316、checker 235–245）ので、一般の timer restoration は正しくない。fresh isolated Python process では旧 timer が 0 という native assumption に依存する。

accepted five-case 493 sec から単純一件比は 98.6 sec、登録 nominal は各 side 300 sec。internal 1,800 sec に対し external は各 2,100 sec、serial external は 4,200 sec、six-hour 21,600 sec への setup margin は 17,400 sec である。wall envelope 自体は feasible である。

### F7 — load-bearing: publication は directory fd に bind されず、driver verdict rehash も閉じない

正常な単一 writer Linux filesystem では、両 wrapper は同一 directory の exclusive temp (`O_EXCL|O_NOFOLLOW`) に全 bytes を書き、temp fsync、`renameat2(..., RENAME_NOREPLACE)`、directory fsync、best-effort rollback を行い、stale final/temp を拒否する（producer 1498–1583、checker 1405–1491）。UNKNOWN は accepted ではなく、小さい別 reserve から作られ、publication が成功した後だけ terminal を印字する。driver は receipt SHA を checker に注入し、checker 後と最終段で receipt を rehash し、exact-one full-line terminal、accepted terminal equality、flags/seals/ranks/cross-bindings を通った後だけ sentinel を書く（driver 83–195）。UNKNOWN/mismatch に accepted sentinel はない。

しかし parent fd は fsync 用に開くだけである。temp `os.open` は pathname、`renameat2` は両 dirfd に `AT_FDCWD=-100` を渡し、rollback `unlink` も pathname（producer 1522, 1534–1543, 1564–1573、checker 1429, 1441–1450, 1471–1480）。最終 parent component の symlink check/O_NOFOLLOW は ancestor replacement や check-to-use parent swap を bind しない。従ってこれは「fresh GHA checkout の `ci/out` は trusted、non-symlink、同一 filesystem、他 writer なし」という assumption の下だけ failure-atomic であり、task369 が求める敵対的 bound-parent property ではない。

また driver は Python validator が読んだ `vraw` を canonical/seal/cross-binding 検査した後、別に `vsha=$(sha256sum "$V")` を計算するが、64-character length しか検査しない（driver 150–194）。validated `vraw` の digest と post-validation physical verdict digest を比較しないため、同じ parent/substitution threat model では verdict の TOCTOU が閉じない。sentinel も通常の `>` publication（195 行）で exclusive/no-follow ではない。GNU `timeout`, `grep -E`, `sed`, `stat -c`, `sha256sum`, `awk`, Bash `compgen`, Linux `signal/resource`, glibc/kernel `renameat2` が必須という platform assumption は driver の GHA-only route と整合するが、parent binding 不足を補わない。

## 一回の bounded repair に必要な項目

1. `g760_ancestry` を通常の `{path,bytes,sha256}` owner に正規化するか、key-as-path を両 wrapper と driver が明示的に列挙し、17 owner 全てを物理 hash する。P0/self seal/final identities と資源式を versioned に更新する。
2. accepted task198 evaluator の runtime/registry/six callables を producer ordinary route で実 call し、checker は独立再構成で同じ semantics を実 call する。単なる entry-point 辞書比較を exercise と呼ばない。
3. mutation harness を、authority は manifest/member/attestation/verdict validator、central/target は closure に供給する actual replay constructor、ABI は実 seal validatorへ戻す。untouched baseline と exact first reason の規律は維持する。
4. import を authenticated bytes から実行するか loader read も事前 reserve/charge し、全 input/authority formula と closure counter semantics を実処理に一致させる。旧 signal timer が許されるなら elapsed-adjusted に復元し、許さないなら zero を fail-closed で要求する。
5. trusted-parent assumption を受理条件に明記するか、dirfd-relative `openat`/`renameat2`/`unlinkat` へ bind する。driver は validated verdict digest を post-validation physical rehash に比較し、sentinel も no-overwrite publicationにする。

これらの新 owner を再 freeze し、別の独立 static PASS が出るまで、pre-A0 A3/v2 GHA を一件も dispatch してはならない。

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
P0 / ACYCLIC AUTHORITY GRAPH:          REJECT
TASK198 AUTHORITY / EVALUATOR ABI:     REJECT
V303-ONLY PROJECTION SUFFICIENCY:      PASS
ONE PRODUCER CLOSURE ROUTE:            PASS
INDEPENDENT CHECKER ROUTE:             PASS
BASELINE + TWELVE MUTATIONS:           REJECT
STATIC CAPS / PERFORMANCE:             REJECT
AVOIDABLE DUPLICATED PROCESSING:       PASS
ATOMIC PUBLICATION / SERIAL DRIVER:    REJECT
PRE-A0 A3/V2 GHA:                      FORBIDDEN
ACTUAL A3 NUMERATOR:                   remains 0/3
A0 / COFINAL LIFT / FAKE / IHARA:      NONE

TASK369_R07_PRE_A0_A3_V2_CODE_PERFORMANCE_AUDIT_V1
