Task1193 public — V11 の公開 driver/WF 設計

Noether の bounded 設計を固定した。V11 source・受領器の実装、import/AST/compile/selftest、対象実行はすべて 0。P/C の私有 source・diff・fixture 本文、埋込 archive は読んでいない。Git/GHA/network/credentials/new agent も 0。ここで固定したのは公開入力、型と依存順、原文の接続先であり、F2/F8 の実装修理済みや将来の数学結果は主張しない。

R = C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163、U = R/task1193/public。
最短の参照は U/public-V11-initial-design-material-manifest-v1.json、3186 B / 46f1c365f4113912c1ff82ac64a3613f91e6583cbbb8ed10dd9da7a05b84a406。

| 選択材料（U 内） | bytes | SHA256 |
|---|---:|---|
| public-V11-fixed-inputs-and-scope-v3.json | 12632 | 82fd3d07301f30e34d276b3a0cee4285a08dc32d7e02fb23788a2d3caa7bc370 |
| public-V11-canonical-wire-and-history-DAG-design-v2.json | 29476 | fda7762199bae13145192f391b5ee95972e10f9fea5b52bcb9bf0959d402b6e5 |
| public-V11-workflow-CPU-and-reception-boundaries-v1.json | 25137 | 5ab1f4c299d7d2e9e1fcac7c85547d9a02719ddb687f9b7e79e4e98a7e0a7a1c |
| public-V11-bounded-design-selfread-v1.json | 10143 | 01e1b3f5ee80de4ea18eb729c0f3fdc23cb7e6d68142ebba5664aa489598c211 |
| public-F8-scope-object-erratum-v1.json | 2432 | 99438d0486e5345803f9ed85e21b78bcc2e436c5b0bb9a9295704b9cc7287984 |

裁定2302・Task1193は全文読了した。root の追加指示に従い、1192 の root 実受領と並行して設計だけを先行した。その後、1192 公開 wrapper と外部 execution/phase/preservation は root 実行で全 native 0、errors/after errors 空として採用済みになった。指定1192返信は 12132 B / 0ec05d8178f7b6ef3f7da8514b4675bc5990b7a66b0b28afef6e259b4c71cabd へ追記済みで、元9161 Bの全prefixを保持した。P all9/2childを含むroot最終正式・CV9採用も後着で完了している。Noether はこれらを再実行していない。

親入力は元 run34731988156/1、head785bd2d87f2b97452a7f0deb2085afe4e7e56d95、rank2474/gen9179、state_head168d2cf1004ee6ace61fd082dedb21af41ff1047cf3a88482ed8170ad81786f9 に限定する。timing-only run34735785100 は親・数学結果・λの出所にしない。既22親の順序を完全保持し、batch-parent-v10 を1件だけ後置する。8層の事前登録は previous896=7×128、total1024=8×128、祖先1121=97+8×128、phase6144=6×1024、checkpoint6176=6144+4×8、invocation8。この数値は親の登録範囲であって次の128候補の結果ではない。

D = R/run34731988156-reception-v1。root正式採用 D/root-v10-formal-and-cv9-mathematical-adoption-v1.json は 1050634 B / 7385f32671c0742cc91df1ffbf1ca2097b3c80ee21f82445aa4863b2ebc8c4a4、formal5 は D/root-v10-formal-inventory5-v1.json、229 B / b2ead8b4b63e3ff76caa2ea1e98d6759bb7d38d619b5fa73bc009e108643536a。files12590/file_bytes1673885307/directories3744 と両名簿SHAを実値で束縛した。cross-checked は root の限定8条、verified=false、grade2 NOT_DECIDED/full_A0=false/A0 actual0/1を保持する。

次親 header は Pauli の R/task1193/P/batch-anchor-v10-proposed-from-actual-Q-v1.json、156207 B / bb67a1eebd9d4b2850099940eaddf6afcd2b1835cdad7e67daa4173d1edf3820 を author proposal として登録した。36field/791D3の独立受領を Noether が代行したとは書かない。この設計の切断時点では root header 採用D3は null、固定後に別途束縛する。新選定λ2474は元V10 final λ e910b7b65d64b1450e2c9b8aad495488e34b643fc0c6f4a01af5b1a78abf4e36。旧選定λ2346の保存35780/index435/edge847と区別し、新λ2474 oracleはnullのままにする。

F2 は既 keysets に残5本 P_timing/C_timing/producer_interface/producer_final_adoption/checker_final_adoption を加えた exact6 を扱う。各元公開文書の全JSONを canonical ASCII compact/sorted + LF にし、元pretty raw D3とcanonical D3を分離した。旧C_timingは raw84329に対しcanonical67241/e56ef155…、旧P/C採用はcanonical3575/f1ebbb3e…・2959/3176b75b…であり、bytesが違うことを意味論的不一致や改善とは扱わない。これらは旧実値の識別でありV11値ではない。

候補ABIは /new_source_audit/public_wire_values の exact6全値、同階層 public_wire_value_bindings のcanonical D3、public_wire_original_provenance の元D3。原典の全値を落とす暗黙projectionを使わない。rootがregistryより前に独立したcanonical文書を固定し、実metadata入力として配備、REPORT/public-declarationsへ保存する。registryから同じ値を生成して再読するだけでは独立照合と呼ばない。通常経路は元raw D3、canonical file bytes、登録全値、先に確定したsource/adoption、保存copy、終了raw pinを順に結ぶ。whole JSON相違は役割別の拒否labelへ到達させる。新たなデータJSONは有限metadata入力名簿へ明記し、元の数学raw3やPython executableへ混入しない。

DAGの順は「受理済み歴史原典 → 数値表/snapshot/sidecar → P → P opaqueを持つC → root source-only採用 → 全6公開文書 → registry → driver → WF → root全体closure → actual保存票 → root実受領」。source-only採用に後段のregistry/driver/WF/全体closureや自己完全SHAを含めない。循環する旧全材料票を黙ってprojectionして代用せず、必要なら新しい完全なsource-only票をrootが発行する。現registryは現driver/WFの最終全SHAを含まず、driver/WFも自己完全SHAを内蔵しない。rootの4source最終pinは全ファイル固定後の外部票に置く。

F8 の候補正本は /new_source_audit/schema_keyset_snapshots。payload exact2={schema,native_domains}、全8世代は順序付き、各exact4={generation,role,namespace,documents}、15familyの各exact3={present,schema,keys}。存在は元保存文書に基づくordinary True/False、未知を不存在にしない。不存在ならschema/keysはnull。現行キーの唯一のownerは既 current_count_inputs/current_exact_keys、元exact8 ABIを保持する。数値prefixは歴史fieldの存在を証明しない。

rootの別sidecarが各世代・familyを受理済みrun/role/model/member全D3/schemaへ結ぶ。CはP数表を数値authorityにせず、独立のキー数、実原schemaと全keyset、存在・不存在、元seals/値/参照/祖先の通常述語を照合する。信頼済みcallerの世代/familyが期待viewを選び、入力文書のschemaだけでviewを選ばせない。snapshotを作ることとreaderを移行することは別義務である。

現在のP案はnative V9/V10のauthoritative期待値を移行し、旧V3〜V8 raw readerを保持する。C案はC4外の全8 metadata viewを対象とする。全8世代の実snapshotに加え、P/C/公開driverそれぞれの全ordinary caller・置換raw・残るliteral・移行statusを列挙する。未移行のauthoritative literalをF8解消済みに数えない。C4原文は保持し、rootがこの実対応表を別読するまで全移行済みとは主張しない。

追加負例はP14/C13の著者案と、公開F2の5件だけを明示した。公開5件は元300秒のmetadata窓内で、まず正例を通常comparatorに通し、最終実文書のscalar1個だけを同ordinary型で変異、copyのcanonical D3のみ整合させ、独立に固定した登録値を残して役割別全値拒否を要求する。正確なpointerは最終実文書から固定し、今は生成も実行もしていない。旧P111/C117の9群、2 child、元parent300/outer360、追加child予算0、非production親/production子、optional16+required2 envを保持する。

F11 は runtime-observation に cpu_model:string|null を1欄追加する案である。実公開observed_runtime()はpython/numpy exact2、そのruntime()完全一致gateは変更しない。観測票だけ現V11 exact5={schema,actual,expected,launch,cpu_model}とし、旧V10 exact4は旧形のまま受領する。ubuntu-24.04の /proc/cpuinfo を上限1MiBで一度読み、最初の完全なmodel name行の値を記録する案。欠測、decode/IO失敗、空値等はnullとし、元のsource/runtime/数学処理の例外やnative/statusを変更しない。CPU modelはcovariateにすぎず、同版1回再走と合わせても原因識別・交絡解消済みとは書かない。費用モデル更新・外挿はrootの数学裁定へ留保する。

WFでは元のoriginal/saved workflow.ymlとdriver.pyのbefore/after bytes/SHA、両regular/no-link名簿、完全SHA名簿を保持し、新親と新metadata原本/copyだけを明示追加する。現WFの自己hashは実fileから観測し、自己literalにしない。識別5点はP WORKFLOW、C CHECKER_WORKFLOW、repo WF path、WF_FILE env、actual launch.workflow。新V11標準4配置名とname d972-r07-fixed-lambda-cycle-batch-v11-envelope-v1、marker [r07-fixed-lambda-cycle-batch-v11-envelope-v1-run] を候補として固定したが、全4source/registryの実最終pinは未形成でnull。

公開outerは旧59実callerを保持し、batch-parent-v10のlive/restoration/intake/native-intakeを各1件登録する63案。P74/C154は別著者の計器順序案であり、これらからouter件数や欠測区間を補完しない。C保存計器の追加registered_public_metadataはscope辞書の第5keyで、measurement_scope文字列とは別である。この1文の初版混同をv2と全raw正逆errataへ訂正した。旧C outer exact11/STARTED・COMPLETE・FAILED/partial/nullを保持し、実measurement_scope文字列は著者の最終wireへ直接結ぶ。

次の実受領では1192の有限部品を必要差分だけversionedにし、新しい全受領器を書き直さない。元run/native/branch/argv、全ZIP EOF/CRC/member名簿、完全modelと空dirの物理custody、現source全原文、実P/C statuses/保存joins/full128鎖、execution/runtime/audit/caps/preservation/phase/cost、新formal5はrootの実入力と採用へ結ぶ。新runの完全inventoryやformal5をV10から継承せず、partial/UNKNOWN/null/負残差をPASSや0へ変えない。対象宇宙・k128/max1/no-refill・元caps/C4/著者分離は固定入力票の全値を保持する。

自己照合は6個の既公開関数bodyとWF14原行を実offset/bytes/SHAで再結合し、6元文書の全文canonical D2、12-node非循環順序、23親prefix、null範囲、全登録inputの前後pinを確認した。旧版はすべて保持した。残るのは設計に対するrootの実装範囲判断、header/snapshot/sidecar/現sourceと全6wireの後着実pin、実caller/literal移行の全raw対応であり、ここで実装完了や将来の成功を先取りしない。

判定: BOUNDED_PUBLIC_DESIGN_READY; SOURCE_AND_RECEIVER_NOT_GENERATED; AUTHOR_TARGET_EXECUTION_0; VERIFIED_FALSE。
AUDIT_1193_PUBLIC_VERDICT:

2026-09-13: root が認可した実 metadata export と公開 consumer 名簿を完成した。数学 source/receiver は実行していない。旧返信原文 10,998 B を完全な prefix として保持する。

作業先は C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/task1193/public/snapshot-v1/。

- historical-keysets-v1.json: 71,827 B / a7f7ad8f1550c74947386f0e934d18f7b70ed0292080e5fb402c8d84da877aa0。
- historical-keysets-provenance-v1.json: 345,456 B / 00290a630966127ce5059387627d496a7c7dc2941672f8e22657ec237bce19bf。
- historical-keysets-export-receipt-v1.json: 1,243 B / 1a4ff7683012f66e5b8de31d7116495321de4fddee46fc844042a4500b783e7d。
- public-driver-all-historical-literal-consumers-v1.json: 660,804 B / d199d076fc2bd7180ea2b331c311f75cbbcc54055126dbc59269710b612c9350。
- public-history-and-eight-metadata-input-ABI-v1.json: 37,280 B / 1058507185509b69fcda0f76bb6554387776bc63c43b94623b8bbf3eac13f4c3。
- actual-history-and-public-consumer-material-manifest-v1.json: 3,681 B / f56ce731b35e69d7c02c466a151f215e70883dbbda52e468ca6b0da11ea47436。

全8世代 v3～v10、共通15 family、全120 slotのうち119は実 ordinary JSON の schema/全keysを直接抽出した。v3 の parent-intake だけは原物理rootと完全原model、受理済みV10全親file名簿の3辺で不在を確定した。未知を false にせず、fixtureやP/C私有source、公開driver内の期待literalからkeysetsを生成していない。元run34731988156の正式受理 7385f326…、model ba146b61…、formal5 b2ead8b4…、新親header root採用 802c9bef…と、各旧世代の全model/原acquisitionを直接結合した。全135入力の前後raw D3が同一。抽出は 2e5221/session48262 → 68a444/native0 の有限data-author実行のみ。

公開driver consumer名簿は既採用V10 rawの既7 ordinary入口、到達する45関数、関係する350文と全310個のnamespace/field-map/keyset名参照を実offset/bytes/SHA/物理行へ結合した。新native-v10入口の実装はTask1194へ明示して留保する。候補・phase・row・invocation/checkpoint、partial anchor/HEAD、historical fixture、current owner、数学値比較はsnapshotの15 family移行と別欄に保持した。snapshot完成だけで旧readerのsource移行完了とはしない。名簿生成は25bced/session99368 → b70c45/native0、対象実行0。

共通CLIは --registered-public-metadata-root。配備root search/public-metadata-v11 の history2 leafとpublic-declarations下の6 canonical leafを用いる。元authorファイルのversion付き保存名と配備名は、bytes/SHAを同じくする別のD3.fileとして扱う。source-only root leafと未来の6宣言/registry/driver/WFとの非循環DAGは継続し、未来結果は置かない。P/Cへ実snapshotと公開ABIを先行供給し、rootの独立採用とTask1194の全raw source接続を後続とする。

AUDIT_1193_PUBLIC_VERDICT: ACTUAL_120_METADATA_AND_PUBLIC_CONSUMER_PREREGISTRATION_COMPLETE; author metadata export native0; private P/C body read 0; target/receiver execution 0; actual V11 source integration continues in Task1194; no new mathematical outcome claimed.
