# Task1090 — metadata 受領の静的負担地図

**F0. 判定と射程。** 静的な反復読取り・比較経路は特定したが、旧 A2 の実時間をどの工程へ帰属させるか、削減倍率、安全な再利用の実装可否は UNKNOWN。現行 source の修理要求、現 run の停止診断、受領の待ち条件は追加しない。Task1090 全文（3,546 B / SHA256 3c5e37c797f984633396d5a7bab5b6318d090004bbfd9ff7a0ed2fe92d22cc98）に従う限定設計メモであり、受領器の新たな全体監査判定ではない。

Task 本文の root 観測は、A2 が 15:50:32Z / PID 13988 / session 82390 で開始し、18:04Z 時点で未完、CPU 7619.046875 秒、stdout 0 B。本調査では process・stdout・実 artifact を再観測しておらず、停止や数学 FAIL を導かない。後着 root 通知の新 run 34148667863/1 の final failure と短い C wrapper 終了も、別の Task1091 の対象であり、本メモの原因説明へ流用しない。新 GHA、1089 binding、既存受領の進行と本設計案は独立。

**F1. 読取根拠と固定材料。** 以下三 source を全 bytes/SHA 照合して task1090 TEMP へ同一 bytes のコピーを保存した。表の V4/V5 は受領器の対象版を指す。P/C 私的数学 source は読んでいない。

| 呼称 | 元 source（%TEMP%/shadow-atelier-audit163/ 以下） | bytes / SHA256 |
|---|---|---|
| V4 | task1074/audit-r07-batch-v4-metadata-v5.ps1 | 261800 / dcccf94a7eb3458d6cf709478a449d3377f86e5b90edfa0a9f011d82122ac411 |
| V5-1088 | task1088/root-review-receiver-v5-envelope-v2-guardclosed-v1.ps1 | 516693 / 5e51d5ab28459ae565a8ee61dd0ea1f6f7d0e1c579c8786f4c8277edf46a39b7 |
| V5 | task1089/root-review-receiver-v5-run34148667863-launch-bound-guardclosed-v1.ps1 | 516900 / 49601381a834c583071251288e7f9b94e9b1036b6f88e32262d1051a8dbee0e4 |

全 source は ASCII、CR 0、末尾 LF。V4 は LF 2474、後二本は LF 4626。V5-1088→V5 の実変更は L14/28 のコメントと L30/31 の launch/承認だけで、四行の forward/reverse 全 bytes 再構成が各全 SHA と一致する。一般本文の費用構造をこの binding 差で変更したとは扱わない。コピーは task1090/v4-1074-source.raw.ps1、v5-1088-source.raw.ps1、v5-1089-source.raw.ps1。

根拠台帳 [source-ranges-and-static-binding-v1.json](C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/task1090/source-ranges-and-static-binding-v1.json) は **22251 B / SHA256 4a65f1293483e13446c1c9bfa233c25fddcac510b36e3498f7de9985dd19eb21**。R01–R17 / S01–S18 の 35 範囲について、元 source 全 pin・コピー・1-based 行番号・0-based offset・bytes・全 SHA を保存した。範囲は重なりを許す出典表であり、全 EOF を相互排他的に分割した台帳という主張ではない。V4 L53–219 と V5 L76–242 の共通 primitives、V4 L961–1010 と V5 L984–1033 の checkpoint 関数は raw 一致も確認した。

**F2. 同一 file と別 root の区別。** R64 は原 continuation の old64 root、R3 は旧 v3 parent（登録 11437 files / 3475 directories）、R4 は v4 parent（登録 11648 files / 3525 directories）、R5 は将来受領する今回 v5 root、と区別する。これらは source 内の登録・変数接続の説明であり、今回ローカル全 file を再 hash した件数ではない。

V4 の通常 main は R4 を読み、L2073–2079 で R3 を読む。V5 main は R5 を読み、L4203 の ReceiveNextBatchParentV5 が R4 の whole envelope（L2860）を読んだ後、ReceiveHistoricalV4CompleteEnvelope（L2863）で元 V4 の全受領射程を R4 に対して再実施する。この wrapper 内で R3 の受領も行う。外側 V5 L4204–4210 はその R3 結果を明示的に利用しており、ここでもう一回 R3 全 prefix を走る、と数えてはいけない。[R14, S02, S04, S13]

同名の output/fixed/manifest.json、run-receipt.json、source.json、各 fixture baseline は R3/R4/R5 で別 file。一方 fixed-reference reader が参照する実 16 payload は各呼出しとも R64/output/fixed に結ばれ、同じ物理 file が再読される。R5 の old64 intake と wrapper 内の old64 intake も R64 の同じ root を読む。PSScriptRoot の正式 canonical inventory 二 raw は、V5 L4069、L2859、L3467 から同じ ReadRegisteredNextInventoryV5 に三回入り、各回で全 pin・parse・完全配列比較を行う。basename だけでこれらを分類できない。[R04, R14, S03, S04, S07, S09, S13]

wrapper は local taskRoot・schema・launch・artifact 等を切り替え、directory plan / restoration 関連 script state を退避・復帰する。返す parsed object も通常の mutable object である。global context や一つの root 名を暗黙に共有する cache は、原 source のこれらの境界を表していない。[S02 L2029–2635]

**F3. 最上位工程からの負担地図。** 下表は通常成功経路で各行へ到達する条件付きの source 読解であり、現在の A2 がそこへ到達したこと、実呼出件数、実 elapsed を記録したものではない。

| 工程と出典範囲 | 全 byte hash・parse・比較の反復 |
|---|---|
| 共通入口 R01/R02、S17 | J は LocalPath→ReadAllText→ConvertFrom-Json を毎回行う。Pin と FilePin は毎回 Get-FileHash。Inventory は Nodes による全名前列挙に加え、宣言した全 file を Pin する。LocalPath は NoReparse で祖先 path を歩くため、同じ小 file でも path/属性アクセスが付随する。 |
| typed 比較 R01 | Same は null、配列長、各 scalar の .NET 型と値を比較し、object では毎回 key 抽出・ordinal sort・全 child 比較を行う。1072 の scalar leaf 限定修理は既に含まれる。Same 自体は file I/O をせず、同じ receipt を何度も parse する費用とは別。 |
| 初期 fixture と REPORT R11/R12、main R13 | RestoreFixtures の各 fixture file Pin、inner ZIP 全 entry StreamPin、PlanDirectories の全 REPORT file Pin、復元後の全 fixture Inventory、before-producer / before-checker / after-checker 各 P/C subtree Inventory がある。全正常到達なら各 fixture file はこの工程内で少なくとも六回、最後の whole REPORT を含め少なくとも七回、ローカル file hash の対象になる。ZIP 内 bytes の hash は別に数える。復元前後の namespace 比較には異なる目的があり、反復だから省略可能とはしない。 |
| 大きい親 roster R14 L2022–2049、S13 L4152–4179 | before→after、before→middle の全比較に加え、各 role の before→acceptance、acquired→before、acquired-after→before の全 files/directories 比較がある。したがって当該 block だけでも各親 file 配列を五回たどる条件付き構造。これは異なる保存主張の比較であり、五つの現物 root を全 hash することとは異なる。 |
| source / audit / controls R09/R10/R14、S05/S06/S10/S13 | 明示 24 source Pin に、audit の全 source/range・保存コピー照合が重なる。registry は ReceiveAuditMaterials 系から読まれた後、main で再度 loader を呼ぶ。controls 全件 Pin 後にも live reader が必要 subset を Pin し、acquired-parents の J も親 roster block と重なる。実 source/range は opaque bytes として比較する経路である。 |
| R3 受領 R03/R05/R06 | whole parent Inventory→outer ZIP 全 file entry→fixture Inventory→inner ZIP 全 entryに加え、128 candidate の六 phase と各採用 row、全 ordinary checkpoint、三時点の P/C fixture subtree を読む。outer ZIP の圧縮 file hash、展開 entry hash、展開先 file hash は別の対象。 |
| R4 の追加受領 S02/S04/S07/S08 | V5 は R4 whole Inventory・outer ZIP・fixture/inner ZIP を読み、続く historical wrapper 内でも R4 の初期全 REPORT、fixture、output、全通常本文、末尾全 REPORT を読む。その後の R4 fixture-history 三時点も再度各 subtree を Inventory。R3 結果の明示再利用と、この R4 の実再読を区別する。 |
| manifest reader R04 L372–397 / R15 L2176–2202、S14 | SavedFileManifest / ManifestFiles は各 payload を Pin した直後、同じ payload＋manifest の Inventory を行う。各 payload はこの一呼出し内で二回全 hash。manifest 自体も FilePin と Inventory 内 Pin を受け、caller の HashJoin や phase manifest Pin がさらに重なる。 |
| current checkpoint R07 / S18 | 普通・pending の各 checkpoint file は FilePin の直後に Pin。各 ordinary checkpoint の期待状態を組み立てる loop では、既存 selection/候補 phase manifest を HashJoin→FilePin で反復する。正確な静的式は下段。R3 prefix の checkpoint loop を同じ式で水増ししない。 |
| current phase / cost R16、S15/S11/S16 | coverage の全 4＋6p phase は manifest/telemetry Pin→ManifestFiles→telemetry J→全 measurement Same。V5 cost reader は OBSERVED input を再 Pin/J し、phase manifest も再 Pin/J、L3986 で全 payload を再 Pin、L3989 でも manifest を Pin する。cost receipt は保存 P/C 秒の照合であり、受領器自身の elapsed の計測ではない。 |
| 末尾 whole REPORT R17、S16 | full inventory JSON を再 parse し、明示二除外 file を足して全 REPORT Inventory。末尾では execution-result JSON 五本も再び J する。保存 summary に至るまで恒常的な stage 出力が無いため、stdout 0 B だけでは現在位置を定められない。 |

checkpoint の限定式は、完成 prefix が p candidate、sequence が 3＋6p、p が 0..128 の場合に限る。ordinary checkpoint は 4＋6p 個。selection 三 manifest の HashJoin 回数は 1＋2＋3＋18p＝6＋18p、候補側五 manifest は各 candidate の途中 1＋2＋3＋4＋5＝15 回、合計 15p。p＝128 なら ordinary 772 個に対し、selection 2310 回、候補 phase 1920 回、合計 4230 回となる。参照される distinct 相対 file 名は 3＋5p＝643 個。この数には checkpoint file 自身、fixed manifest、他工程、pending diagnostic を含めず、byte 数や実時間の上限にも変換しない。零件・早期拒否・未完をこの完成式で埋めない。

この式の実範囲 R07 は offset 101166 / 6211 B / SHA256 b777d4752ef993c0c409f81e6d276727690740bac0467e1904c2059d3c5092cf。R15 は offset 226670 / 2896 B / SHA256 d4cc6ecd2b20611dddcd31d3b1faf0793c8a2b419f55feb0e44b8e5fab0def75。その他の各出典 pin は F1 の範囲台帳を正本とする。

**F4. 負担削減候補は二つまで。** 全 file hash / typed roster の重複を構造上の候補として先に挙げ、狭い checkpoint loop は変更範囲を限定しやすい対象とする。どちらが実時間を支配するかは未測定。次の二案はいずれも採用済み修理ではなく、前件未証明のため実装可否 UNKNOWN。

1. **checkpoint 関数内だけの manifest hash 再利用。** selection 三 file と当該候補五 file に限定し、全 checkpoint の普通型・predecessor・順序・期待 hash・全字段 Same を各回維持したまま、既読 file の FilePin を再利用する余地を別読する。R07 の 4230 回を distinct 643 名と比較できるのはこの範囲だけで、受領全体の倍率ではない。key は basename でなく、受理 root/role・schema 文脈・実正規 path・参照する file identity/pin・観測区間を含む必要がある。現在の fs がその区間で不変という保証が無ければ、以前の hash を現在の観測と置き換えられない。size/mtime の一致、既存 PASS 票、末尾 hash だけでは途中変更して戻る場合を除けない。OS が保証する固定入力 snapshot 等の前件と、alias/reparse の拒否を閉じてから検討する。
2. **繰返し J する登録 metadata の parse 再利用。** 同じ physical file の registry、inventory、fixture baseline、acquired receipt 等の限定集合について、全 bytes pin に結んだ parse 結果を一つの固定観測区間で再利用する案。全別 receipt との Same は省略せず、比較した事実だけの memo にもしない。wrapper の root/role/schema と入力世代を明示し、同名別 root や PSScriptRoot の別材料を混ぜない。caller が得る graph の共有 mutation を防ぐ手段が必要であり、浅い copy は不可。型を失う JSON 再生成、配列の展開、Hashtable 化、null/一要素配列の変形を伴う clone も不可。read-only graph で全 caller が成立するか、型を保存する隔離 copy の費用が再 parse より小さいかは今回未確認。

両案とも空 directory 復元前/後、親 preflight/全 hash、before/after と異なる観測区間、別 wrapper への切替えを cache 境界とする。source/親が実際に変わるケースの拒否を、元の観測点を含めて維持できる保証が必要。正式全 inventory・全祖先・全 checkpoint・全 ZIP/fixture・全 source pin/range・最終 whole REPORT を省略する案にはしない。走査の一括統合や旧 PASS receipt による代用を第三案として追加しない。

現 counter の taskPinChecks / taskHashedBytes は Pin の成功だけを数え、FilePin/HashJoin、ReadAuditSource の直接 bytes hash、ZIP StreamPin、J の読取りを含まない。従ってこの値から重複率・全読取 bytes・物理 I/O を推定しない。将来再利用を実装するなら、論理照合件数と実全 file hash 件数・実読取 bytes・再利用件数を別にし、旧 counter を実 I/O と読み替えない。candidate/cross_checked/verified の意味や数学 assurance は変更しない。

**F5. 将来の少数観測境界。** 実装・今回 process への取付けは行わない。次の六区分について entry/exit の時刻と単調 elapsed、可能なら process CPU の差、完了した phase/checkpoint/fixture 件数を残せば、stdout 0 B より位置が分かる。historical wrapper は root role と深さをラベルに含め、親区分の内包 elapsed を足し合わせて総時間としない。

| 区分 | entry/exit と件数の対象 |
|---|---|
| 1 | read-only 親 preflight と current fixture/archive/復元。予定/既復元/作成 directory、全 file/ZIP entry の処理件数を区別。 |
| 2 | source/audit/control と全親 before/middle/after roster。role 数と比較した roster 行数。 |
| 3 | R3/R4 parent envelope・ZIP・全歴史 prefix。root 別に ordinary checkpoint、row、phase、fixture entry の件数。 |
| 4 | current candidate/row/DERIVED と全 checkpoint。到達した selected/processed/ordinary checkpoint 件数。 |
| 5 | current coverage と保存 cost receipt。phase 数と実在/未形成/不正 input の件数。 |
| 6 | 最終 whole REPORT と最終 receipt。file/directory 件数、正常完了または停止位置。 |

初めは境界単位の少数記録と既存 Pin counter 差を、その限定名のまま使う。必要になった場合だけ FilePin/J/ZIP 等の独立集計 counter を別途設計し、全 Pin ごとのログや Same の全 scalar ログは作らない。P/C 数学 source に計測を足さず、既存 cost-receipt の P/C 秒と root metadata receiver の秒を混同しない。今回の CPU 値や無出力状態から timeout 値を新たに決めない。

**F6. 実装へ進む場合の最小独立比較と閉鎖。** 新たな実装委嘱後に、まず変更する共通入口だけを固定した小 metadata 対象で比較する範囲を事前登録する。今回その fixture/実装/性能試験は作らず実行もしない。

- 同一 root の同じ file と、相対名だけ同じ別 root、alias/reparse を分ける正負対照。初回読取後の content 変更、同 size/mtime の変更、変更して戻す場合、空 directory の未復元/復元後について、入力固定の前件を満たすか、元の拒否を保存することを別読する。
- J 案は ordinary int/float/bool、null、空/一要素/入れ子配列、key 順、共有 object の後続 mutation を含む型保存対照。受理/拒否の比較対象を別 receipt ごとに残し、再利用 graph の mutation で他の比較結果が変わらないことを対象にする。
- checkpoint 案は既存通常 helper に正しい prefix を一度通した後、後方 checkpoint の一字段だけを変えた場合の拒否位置/理由と、全 checkpoint・参照 manifest 集合が変わらないことを対象にする。目的外の上流例外で対照を成立させない。

独立別読では全 raw 差分、入力・出力の型付き値と元の拒否意味、全 inventory/EOF/pin の対象集合、計測専用字段以外の受領内容を比較する。小対照の成立だけで full receiver の同等性や高速化を宣言せず、入力固定前件・全保持範囲を閉じられなければ UNKNOWN のまま不採用とする。現在の A2 停止/再起動、未完 artifact での試行、現 GHA/1089 の追加 gate はこの比較計画に含めない。

保存・確認は三本の metadata source の raw copy/hash、四行 binding の双方向 raw 再構成、35 出典範囲の hash、指定返信のみ。新 source 実装 0、受領器/helper 実行 0、性能試験 0、process 操作 0、数学/AST/import/compile/Git/network/GHA/credential 操作 0、新 agent 0。旧 source・旧票・実 artifact は変更していない。実原因・安全な再利用可否・実速度改善は未観測のまま本メモを凍結する。

AUDIT_1090_VERDICT: STATIC_COST_MAP_AND_BOUNDED_DESIGN_ONLY; ACTUAL_CAUSE_AND_SPEEDUP_UNKNOWN; TWO_REUSE_PROPOSALS_REQUIRE_IMMUTABILITY_AND_TYPE_PROOF; NO_IMPLEMENTATION_OR_RECEIVER_EXECUTION; NO_NEW_RUN_OR_RECEPTION_GATE.
