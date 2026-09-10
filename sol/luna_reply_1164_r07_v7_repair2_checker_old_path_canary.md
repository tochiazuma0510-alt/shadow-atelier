# Task1164 — repair-v2 旧path負例の最小修理と未束縛C納品

指示書を全文読み、実repair-v1 CのC4外の負例1assignmentと、新P/C/WF identity、CURRENT_PRODUCER_REGISTRATION=Noneを新規版へ反映した。C述語、C4、全旧event/method、6群の件数・case名・範囲は保持した。数学sourceの実行/import/AST/compile/selftest、binder実行、P private読取は0。1163公開exportの作業メモを保存しており、本便後に継続する。

実run34518126217/1、head2f8ad063da52da90ed74fd230fb122f96ad79ec7の公開stderr287 B/SHA2562d437aa4a935ffc21501e00546fda2a02c5c611466fa3fc3feebdb6fc86da524を独立に読み、ValueError:cycle_batch:missing_required_rejection:old-producer-pathとFAILを照合した。公開exit-codeは2 B/SHA2564355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865、実値1。P本体/C本体skippedはrootから受領した実run情報であり、本体の結果を補っていない。

repair-v1名に完全部分文字列 _v7.py はないため、旧L6021のreplaceはproducer/checker両sideでno-opとなる。第1負例old-producer-pathは正対照と同じcurrent pathのまま既存check_executable_pathsを通過し、rejectedが記録されたmissing_required_rejectionを発生させる。新L6021はsideから固定の旧v6 basenameを構成する指定の1assignmentへ変更した。producerはsearch/d972_r07_fixed_lambda_cycle_batch_v6.py、checkerはsearch/check_d972_r07_fixed_lambda_cycle_batch_v6.pyとなり、新current *_v7_repair_v2.pyとはそれぞれ異なる。両方とも相対path文字列のまま、bytes/SHA/反対sideを保持し、既存D3型検査を通った後にregistered_new_executable_pathsで拒否される静的構成である。既存rejected harness自体は許容例外種の検査でありexact-label専用検査ではない点も公開票に記した。新testやC述語の緩和はない。

以前の「selftest raw同一だから新identityでも同義」という説明は、この負例の成立前提を落としていた。raw同一だけでは生成されるnegativeがpositiveと異なることを保証しない、と明示訂正する。今回、6群すべてをrawで全読し、current名を作る箇所・そのconsumer・間接hashの流れを別に追った。

材料の基点 R は %TEMP%/shadow-atelier-audit163、全新材料は R/task1164/。準備sourceは実repair-v1 C525657 B/SHA256ccd572ee1f0cd2504521526fbfbf830a95197d99044870cf19c7a6cc0ffb67a7から作成し、既存sourceを変更していない。

| 材料 | bytes | SHA256 |
| --- | ---: | --- |
| unbound-v1/search/check_d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py | 525553 | 71920c6dfe8799a41fb6f1b560ecdcdf081ea88b6080027175c3e1e5713e3245 |
| repair2-five-RHS-forward-reverse-v1.json | 5362 | a4010848bf20d728bfed353f117e19c14df624ca58e954c4ff0e6f55a32ceb53 |
| repair2-unbound-all194-retention-v1.json | 94158 | 23dc0811564e2f9b1d8d329f793ff8e13b172c9bfef9f20cf9ea9aa69e945a02 |
| repair-P-opaque-binding-plan-v1.json | 2432 | 87f5eb0d8b1a09fe88f09bb530f21732355e1abcdd0c1d9cc1280d817ed9c9cc |
| bind-repair-C-P-opaque-v1.py | 9499 | 461db212a45c9a3cee18cbd5c49192a0b58d35ee02a093e2adacebc42594ea47 |
| bind-repair-C-P-opaque-contract-v1.md | 4962 | 0ad67058c0e01dc035f10927c7d8b336dede0d843881c4d4a30499b51a80c25e |
| public-selftest-identity-consumer-contract-v1.json | 36779 | 42904e25d62bb8c10ae3e03b3a8885d8ec86c13d551bc03555d2fe3f04924161 |
| author-final-material-manifest-v1.json | 2557 | 189c56a5e4cb736f30bf3a440c02c45c3d17310ceb09d6400146f0ca191df301 |

最終材料manifestは自身と本返信を除く11材料713753 Bを全D3で列挙する。公開source/identity overlay、2本のmetadata-only author作業スクリプト、source準備票も含む。author作業スクリプトはraw/text/JSON/pinだけを処理しており、C/P sourceをimport/AST/compile/実行していない。

全EOF正逆票にはL52/53/54/325/6021の5 RHSだけを、前後offset・長さ・SHA・base64で記した。全194連続領域をEOFまで再計算し、変更はPREAMBLEとk128_registration_canaryの2領域のみ、192領域が全raw同一。6979LF・0CRを保持した。C4登録24・一意21は全rawに加えて前後16 B境界も同一。元retentionのselftest欄はk128_registration_canaryだけがraw不同であることを正確に表し、全旧方法/計器/述語を変更していない。

公開consumer票はselftest全域L5884–6884、entry/failure L6906–6979、関連通常helperをsource rangeのoffset/bytes/SHA/占有行で結ぶ。current identityの直接参照はL5937/5938（fixture sourceと実C receipt）、L6016（正対照P descriptor）、L6111（bootstrap WF）の4行。修理後selftest域のreplace呼出は0、CURRENT_PRODUCER_REGISTRATION参照は0。main/output_locationのroleハイフン変換はCLI属性名の対応でありcurrent executable suffix変換ではない。current C全bytesに由来するfixture source/owner/start/phase/selection/view等のhashは、実実行で同じfresh recordsから双方に流れる。固定旧artifact identity18件とnative v3/v4/v5/v6名前空間は変更しない。

| selftest群 | 元negative数 | identity確認 |
| --- | ---: | --- |
| registration | 28 | 2旧path負例を実v6文字列へ。root/phase/checkpointのfresh bindingとbootstrap WFを追跡 |
| roster | 9 | 同じfresh fixture recordsが全witness/view/phaseと従属継続へ伝播。固定current suffixなし |
| batch-parent1578 | 6 | current P/C/WF変換なし。歴史的schema/role/target-hash判定を保持 |
| batch-parent1706 | 7 | current P/C/WF変換なし。歴史的row0・353全順・zero等の元範囲を保持 |
| parent1834 | 8 | current名変換なし。18歴史的公開artifact identityを元値のまま照合する構造 |
| parent1962 | 10 | case名のv6は歴史的親。native18/609/zero/null/native49等の元意味を保持 |

公開票は68個すべてのnegative名を元順で列挙し、各群の保存dir・result名・実行時status文字列・writer/consumer pinを含む。synthetic observed inventory配列試験を物理親全EOF受領とはせず、native49 header/sealを下流全値/算術照合とも称していない。これは静的接続確認であって、新実行selftest PASSを主張しない。

新identityはP search/d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py、C search/check_d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py、WF .github/workflows/d972-r07-fixed-lambda-cycle-batch-v7-repair-v2.yml。name d972-r07-fixed-lambda-cycle-batch-v7-repair-v2-envelope-v1、marker [r07-fixed-lambda-cycle-batch-v7-repair-v2-envelope-v1-run]。論理v7、19親、1962/8667、k128/no-refill、caps、C4 raw、著者分離、数学宇宙、既存formal5を保持する。

binderは1159の全source/契約/CreateNew/全EOF正逆処理を再利用し、task namespace/pathと新plan pinだけを置換した。置換を戻すと旧9499 B/SHA256fce81693099800d9b99f568de01b1108c6f21cd5e20477cb9cb1736157406768に完全一致する。rootは公開P descriptor JSONの実whole D3をCLIで渡す。P file文字列は新正規名との比較にだけ使い、一度もfile APIへ渡さない。実P sourceの別読/採用はroot所掌であり、descriptor自体をその証拠とはしない。唯一の束縛はoffset28091/4 None。束縛後も全193 nonprefixが未束縛版と同一であり、今回修理した負例も保存される。契約のunchangedはその束縛前Uを基準とする。最初の5出力は事前type/pin/range全照合後にfresh dirへCreateNewし、flush/fsync/readback、全入力の再読後、最後にcomplete-binding-handbackを出す。著者は実行していない。root finalP opaque D3を待つ有限状態であり、追加著者承認gateは設けない。

既存P機械結果をrepair-v2の新run結果へ読み替えない。本agentはGit/GHA/network/credential/process操作や新agentを使用していない。rootの別読後のbinder/receiver、およびGHAだけのC数学実行を妨げる追加gateはない。

AUDIT_1164_VERDICT: STATIC_MINIMAL_REPAIR2_AND_FULL_IDENTITY_CONSUMERS_PREPARED_P_OPAQUE_UNBOUND_NO_EXECUTION

root実束縛後の追記（前段の未束縛準備を履歴として保存）:

rootが全binder、5 RHS、194領域、C4と前後16 B境界を別読し、実P opaque D3を用いてbinderをnative0で実行した旨を受領した。本agentはbinderを実行していない。実complete-binding-handback-v1.jsonは2459 B/SHA25635d9211802ca527d904600b6fff518d9e0f5de57d631e8b3d61a053edfb78dde、status BOUND_METADATA_ONLY_COMPLETE。final CはR/task1164/root-bound-v1/search/check_d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py、525707 B/SHA256d0e789ae15978023f29dcfcf21d4d2c4ac7100f9d8241351bee5b2d889132607。

root-P7-repair2-final-opaque-descriptor-v1.jsonは159 B/SHA256e63be7e218cf8e5b5c9142c934e79f7e7c6d29e64b53bcfe05a8d5bd87f9bb29。公開内容はfile search/d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py、bytes552885、sha2566fe3ee03967b21d030a3bf141001df58305306c3b934b1c3fb71bd08a1a419bb。この公開D3とC側handback/overlayだけを読み、新P sourceは開いていない。

R/task1164/final-public-consumer-location-overlay-v1.json 4193 B/SHA2569be54e0f5cd294f1beb7e7072f72250742eb1c6ba3f7749b162924ef0c9f0556を新規追加した。rootの実1RHS delta（offset28091、4 Bから158 B、差+154）を元の公開consumer票と結び、全11 consumer spanのfinal offsetを記した。全selftest/consumer本体はそのRHS後にありoffsetだけ+154、bytes/SHA/行範囲は不変。preambleやopaque RHS行のraw不変を主張する規則ではない。rootのmetadata束縛完了は新C selftestや本体のnative PASSとは別であり、未実行の成功を主張しない。

AUDIT_1164_VERDICT: ROOT_OPAQUE_BOUND_METADATA_HANDOFF_RECORDED_STATIC_REPAIR_AND_CONSUMERS_COMPLETE_AUTHOR_MATH_AND_BINDER_EXECUTION_ZERO
