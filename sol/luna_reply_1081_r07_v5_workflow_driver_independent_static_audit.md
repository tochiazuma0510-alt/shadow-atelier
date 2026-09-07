# Task1081 — v5 WF/driver/registry 独立静的監査

F1. Task1081/1079全文、P公開interface-v1/v2、C公開interface-c-v1/v2、1079 public-scope-and-cost-contract-v1を全文読了した。変更は本返信とTEMP/shadow-atelier-audit163/task1081の新監査材料だけ。1079作者のimmutable snapshotを依頼済みで、現時点では未着。mutable草案を最終監査済みとはしない。P1077成果は不変、C私的算術/fixture本文は読まず、source/AST/import/Python/GAP/compile/数学/Git/GHA/network/credentialの実行は0。

F2. 指示書1081の旧driver basename _workflow_driver_v1.pyは実repoに存在せず、正本はTask1079/旧1067票/実小WF envどおり _workflow_driver_v2.pyである。rootもこの表記訂正を明示した。実全pinは536145 B /35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0c。旧小WF22153 B /56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859bの全368行を再読し、baseline-v4に両原文を固定した。新v5 _workflow_driver_v1.pyは別名なので、この旧basename訂正で新pathを変えない。旧1067の独立監査全文も再読し、旧保持本文の読了根拠と新変更範囲の監査を分けた。

F3. 初期必須対応表をcontract-correspondence-v1.md、6478 B /b23f579deb11f584b7b60782ef398428d05d388f962810791052aee6187c2e3fへ保存した。全17親輸送/復元/最終inventory、旧64+v3+v4/353祖先/previous target、全source/body registry/共有TCB、四群fixtureの全実bodyと理由、全5execution、cost全descriptor/字段/単位、観測seq3/9/partial、全保全とcandidate gateの27表面を、旧driverの実関数/行へ対応させている。全て新snapshot監査前の要求表であり、実装済み判定ではない。

F4. root追加表面をcontract-correspondence-addendum-v1.md、1344 B /c3415b94459204d7e54d651761e1557575725e5a03a29b2fbc83037b1839fde6へ保存した。旧第三群の実fixtureはPがcurrent ROLES17役（旧投影[:15]）、Cが明示historical16役である。raw本文保持と展開後のfixture型を混同せず、WFが両者を別に認証するかを読む。第四P28file/C15fileと旧DEPENDENT116fileの到達点限定も別に保持する。costのsigned NEGATIVE_RESIDUALと欠品/不正/数学候補の判定を混ぜないことも通常dataflowから確認する。

F5. 初期入場票initial-inputs-and-scope-v1.jsonは4316 B /c251ec732a2c76ea2176af41c606fa7fcf950c93cea87943b0d708b60f0bc199。全公開資料/旧pin/要求表を結び、新snapshot未着、新本文未監査、新runtime主張なしと記録した。required source findingはまだ判定対象に入っていない。次にimmutable1079 snapshotの全差分・新本文・全EOF区間/registry raw reconstructionを別読し、必須所見は作者とrootへ即時報告する。


## F6 immutable snapshot と全域台帳

Task1079 review-snapshot-v1 の driver 1139184 B / `0aaaa9f8822513a0520e99a4e37901595936d7e08ccda70263643200de42acba`、WF 26294 B / `fbf4ef94d2235f1f23f658ea1563c1f328ff582bf2846e844be178fa81cc1f8b`、registry 498361 B / `4247b8472378ba9a837df60de55473f9d0d59e04f48f43d60b161fba177a43ea` を独自 TEMP snapshotへ固定した。旧driverからの独自raw EOF台帳は91→105区間、67不変・24変更・14追加・削除0。新registry rawと埋込み全bytes一致、歴史76867 B registryと直前236390 B registryも旧driver由来全raw一致を確認した。全追加本文と旧共通callerの読取は進行中であり、この台帳だけから完成判定しない。

## F7 required R1 — 二層 fixed 参照票の排他的保存名衝突

v1 driver L6519 の旧 batch_fixed_reference と L7043 の新 next_batch_fixed_reference は同じ `REPORT/batch-fixed-reference-receipt.json` を save する。通常 intake_mode L7694–7695 は両認証を順に呼び、save L5520 は open('xb') なので新層の二回目に FileExistsError となる。実GHA失敗を観測した報告ではなく静的な到達経路findingである。rootが必須として採用し、旧名保持＋新 `next-batch-fixed-reference-receipt.json` への分離、全参照・保全・最終join・公開契約の結合を作者へ指示した。原snapshot不変、修理差分の独立再読は未了。

## F8 並行1082と継続範囲

Task1082で root が正式全inventoryを登録し、P定数だけの新案と全逆差分を別便で閉じた。1081の旧snapshotと既読scopeは保持し、後着の正式P/C pins・registry・R1修理は新snapshotの限定差分として扱う。全typed metadata受領の未完は全inventory完了と区別する。

現読了は全17親live・両batch入場・旧64参照・acceptance 8key・三registry生成/全source保持・57bodyと旧8loader gate・第四群の保存fixture・常時保全・最終candidate gate。現時点のrequired findingはR1一件で、残るcost生成/停止run票/main/WFの環境列/全registry raw range照合を継続する。旧第三群はP/C各実subtreeの別baselineから全bytesを保持するため、P17/C16へ共通16を強制する型衝突は既読gateにはない。


## F9 完成bodyの静的別読

v1 の全変更・新設function body、module prefix（埋込み三registryは別全raw認証）、WF全414行を読了した。17親の live API/ZIP全bytesと安全EOF、旧v3の36dir/新v4の38dirの認証済復元、旧15→16→17のportable acceptance、両128行と97→225→353の全親列・theta=0項保持、各原生schema・plain target JSON hashとpacked hashの分離を確認した。formal inventoryとP/C final pinの後着結合を未実行のまま待つ旧v1 guardは、後続1082/root裁定の新snapshotで置換される。

新costは保存P/C elapsed_seconds・全P selection三相・実processed数の各六相・final telemetryのpinから作成する。一般的な独立数128を予言せず、実n件へ8+6n入力を列挙し、後尾SKIPPED_AFTER_LINEARへdurationを捏造しない。P residualはP totalからP各測定を引いた符号付き差で、負値を丸めずNEGATIVE_RESIDUALへ保持する。この負値だけではcandidateを拒否しない。欠品/不正型はnullとINCOMPLETE/INVALID_METADATAを区別し、bool/非有限値/overflowを観測秒数に昇格しない。C総時間、P+C総時間、新17親とnative1450/1578/1706 pairingなどの交絡を別欄に残し、232.786064を今回の期待値やgateへしない。

P[30,10,6,7] / C[28,9,6,7] は既存二数学群＋二親metadata群と型を分け、旧数学suite全再走や共有TCBの独立性を追加主張しない。P第四群28file、C第四群15fileは公開ordered case/目的label/実caught error/positive保持へ接続し、最終gateで保存全票を再読する。旧第三群はP17役・C16役の各実subtreeを自分のbaselineへ結ぶため共通16の再解釈はなく、旧DEPENDENTを含む全fixtureと空dirをZIP明示entry/EOF/全bytesで保全する。

正常/COMPLETE_ZERO/LINEARでは公開型と全C終了・HEAD/result・全親入場・全source/current registry・前後保全の結合を要求する。停止/未形成は実P/C終了コード・部分prefix/hidden diagnosticsをREPORTに残し、完了candidateへ昇格しない。新lambdaの再oracleは未計算nullのまま。launchはhost metadataへ、portable owner/startは固定親とcode/runtimeへ結ぶ。

## F10 独立 raw 照合の証跡

`task1081/independent-public-registry-all-raw-checks-v1.json` は401256 B / `20cd69ab69b561f600f4ee8fa4a6d945f6714b7ad73c34d92e0dbdcc6f1a7538`。全10 sourceの実全bytes/SHA、P137→156（121不変/16変更/19追加）とC117→140（100/17/23）の全EOF、旧loader8対、保持body57対、歴史60区間、共有4kernelを別に照合した。範囲チェックは740件。C private本文を表示・算術解釈せず、公開opaque rangeのraw/hashだけを用いた。Pの自作数学を独立監査した票でもなく、WF metadataと公開wireの独立別読である。

現在の独立所見はR1のみ。作者の修理済snapshotへ全参照到達・正式P/C定数・offset/全raw registryを照合した後、最終判定を置く。

以上はv1時点の経過。以下F11–F13でR1と最終bindingを閉鎖する。
## F11 最終v2とR1の閉鎖

review-snapshot-v2の全限定差分を読了した。旧 `batch-fixed-reference-receipt.json` は保持し、新v4層は `next-batch-fixed-reference-receipt.json` へ分離された。新check_fixed_reference_receiptsは二つの実票のexact17key・各層の参照manifest・旧64の固定manifestと16payload・実geometryを読み直す。writer再呼出しはない。排他的保存衝突の解消だけでなく、acceptance-receiptの二role pin、全REPORT controls、alwaysのfixed-reference-receipts-after、保全flag、final gate、runの両票とafter票への全参照到達を確認した。未形成はnull、完成入場の推測はfalseであり、generic readerや親payloadは緩めていない。公開R1追補2804 B / `63ed42b5b75a126467a28e2232673d2eab80c73d88c8eeed529ef2b5ab07a64f` と実serializerも一致する。R1は静的に閉鎖、追加必須findingは0。

独立R1票は `task1081/R1-static-closure-v1.json` 5124 B / `2f93bf106246df269fa46cd353c6f76b4fbbc5fb1b5486c984f00a134c564006`。最終binding票は `task1081/independent-final-binding-v2.json` 4100 B / `a0ab37e2662f2323caaa7dc27aabc99c7c603fc532af4ee2353b1fc5306405dc`。最終P/C全296区間、旧8loader対と57body対の計426 raw rangeを再照合し、全source EOF・歴史source・旧partition/classification保持を確認した。埋込み三registryは各独立原文と全bytes一致し、compact/readableの全JSON値も同一。旧428237 B生成票は57bodyを既に含む整形違いであり、最終生成票はcompact/readable両pinへ更新されている。

正式7022 B / `64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753` のroot票から、11648file / 1308094050 B / 3525dirとfile/dir両canonical SHAをexact五keyへ結ぶ。registryの新parent_inventory_registrationはregistration/root_receipt/full_typed_parent_metadata_complete/scopeのexact四key。guardTrueはこの正式inventoryと最終P/Cへ結ばれ、full_typed_parent_metadata_complete=falseは保持される。全typed受領完了を代わりに主張しない。WFのv1→v2はP/C/driverのbytes・SHAの六literalだけで、他の全414行は不変。

## F12 最終固定pin

全pinを実ファイルの全bytes/SHAで再照合した。P/Cは本文の相互算術共有をせず、公開pin/rangeとして認証している。

| 対象 | bytes | SHA256 |
|---|---:|---|
| P5 `search/d972_r07_fixed_lambda_cycle_batch_v5.py` | 366644 | `664f593a4c9b6eb5d088960215674175a123d7f5a5f2bb3e134d3cb0e16c1c66` |
| C5 `search/check_d972_r07_fixed_lambda_cycle_batch_v5.py` | 336193 | `47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73` |
| driver `search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v1.py` | 1145254 | `f7181bc573c3aff041d6fff3520266ca401de6416b410d145c94aceaf3a18913` |
| WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml` | 26294 | `f5abb0c604a53142accf6c02fb092cee1e448cba27ff428f67be4788894cc0d3` |
| registry `task1079/review-snapshot-v2/inheritance-registry.json` | 499053 | `e30a6bde668f0778932f0c4fbd62752c698bd70b97e9b097dccde4e9348c2858` |

snapshot manifestは4879 B / `0940f80bccf4245d0d86c0f41df1c339311fbc852a4fe14e1c9acff50abab1c0`、最終registry生成票は4256 B / `1f86dd4289a2bd6f098e7cc9112fe07e3511415107b40e1de045a51cc6b67d91`。各deliveryを独自snapshotへ固定した。

## F13 最終判定と射程

Task1081の独立静的別読はSTATIC_CONTRACT_PASS。R1一件を修理後の全保存・最終参照まで閉じ、最終版に残る必須findingは0、指定範囲の未読変更bodyは0。17親、旧64＋v3/128＋v4/128、353祖先、P17/C16旧第三群の別fixture型、四群、cost、資源停止、全保全、公開keysetを実制御本文へ照合した。自作P数学の独立照合やC私的算術の審査を意味せず、共有TCBの追加独立性も主張しない。

source/数学/AST/import/Python/GAP/compile、Git/GHA/network/credential実行は0。新v5の実run・新rank・新候補・自己試験PASSは本票では未観測。配置、具体marker通知、commit/pushと実発射はrootの担当である。全typed親受領の継続は2210の分離を保つ。本返信とTEMP監査材料だけを変更し、旧source/WF/snapshot/既返信は不変。

AUDIT_1081_VERDICT: STATIC_CONTRACT_PASS; R1_CLOSED; FINAL_PINS_AND_ALL_REFERENCES_CLOSED; REQUIRED_FINDINGS_0; NO_SOURCE_EXECUTION; NEW_RUNTIME_NOT_OBSERVED.
