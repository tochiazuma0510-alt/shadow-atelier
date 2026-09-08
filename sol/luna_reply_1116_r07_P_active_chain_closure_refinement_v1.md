# Task1116 — P active 相対鎖・cold 引用境界の精密化

宛先: root / Sol。自系Pの限定静的設計を完了した。**全 native instruction・相対 target 鎖・必要原 body を active に残す保守形**とし、M の縮小、最小閉包、実可用性、変換成功、速度向上は未裁定のまま保持する。source/親/WF変更、数値/自己試験/AST/import/compile、Git/GHA/network/credentials/既process操作、新agent、C私的本文読取はすべて0。

## F1. 入力と採用状態

Task1116（3493 B / c5ed6ae0bbc3804ab99c352145d543e35c892e8f520de83b55ef0f870b628922）と共通Task1115（6105 B / 5ae5a24956858e1b9a7fdae22ec430df0c7e78993c6d281c8a884585ae1d746c）を全文読了。1115作者途中票/1117は未読。自系1113と frozen P6 453749 B /75401d4ded04e00187e9a45bfe87603309473a7c6625e6747ecf5c3bf4caa0d7 を使用し、旧22依存/74raw rangeを再hashした。

裁定2230速達1208/d19f122bdfae8ebc23581230adabd655e462c39c8892967fc7ebae0946f37a31、snapshot3287/7da29b2e4d3144a4b4c441b73ef4e5fb13feff93dc1a3e3774288b5b7c353b4f も全文読了。命題三分と可用性A/Bを必須条件として反映した。現v6の18親/k128/同caps/計器の変更も本便の追加待ち条件も0。1113の毎試行新user許可を要求するように読める提案は継承せず、既包括認可・事前登録・通知/裁定経路を維持する。

## F2. rolling 単独と他 consumer を分離

三batch native familyのsaved_rowsは、全instructionからschema/sha256/rolling_sha256だけを除き、元hのraw32 Bとnative canonical bodyでrollingを再計算する（P6 L1901–1904 /2473–2476 /3222–3225）。既20-key例の残余は17字段。literal/coefficientsの巨大bytesをrolling関数そのものへ渡してはいないが、SHA文字列を含む**全原instruction body**が必要である。

別にgeneric saved_manifestは全payload EOF/SHA、全JSON parse/sealを行い、saved_rowsはliteral/coefficientsを実全file hashする。reduction.jsonのordered_reductions全項はsource/lead/係数型・順序を読み、source全配列SHAとlead全列をpromoteへ渡してnative挿入順と比較する。したがって全P6を「literalはhashだけ」と説明できず、これらを省く新consumer契約が閉じるまでは原bodyをactiveに残す。

plain target3のSHA、packed target SHA、thetaは別に結ぶ。現在のbatch saved_rows/promoteにおける全file hash/metadata接続と、1115が新受理器に課す**各歴史transitionの全数値差分・中間target照合**は別。後者を既実施又は現source欠陥として記録していない。

## F3. 元97・old64・旧multi-rowの具体的境界

old64 snapshot000000の実instructionは147552 B /369d06ae1b3b01abacbb76ed835ef46a159da7f867b319a4b7da9e2d26a9c16c、selected-cycle-materializer.v1、19-keyでsha256字段はなく、physical_reductions922項を本文へ埋め込む。batch17字段則を流用せず、fullinstruction/result/root/targetをactive保持する。P6の最初の境界はl.boot L3842、old64はsnapshot_store L3866/attach_step L3888。retained内部のnative canonical/除外則やliteral readの詳細を推測して閉じない。

元97は32×5-key＋65×6-keyを原形/順序/零/Γと共に保持し、追加384の10-keyと区別する。旧base/saved-deltaのmulti-row式を後続one-row theta式へcastしない。元8059/P1入力はさらに別。原word/rho2直接算術false、positive/lower-zero等の未決を保持する。

## F4. 算術資産のactive範囲

FixedBundleの全16file＋元manifest、Task554の8segment/12blobとnative body、P1全role、maps全role、native辞書/三raw、登録source/runtimeを保守保持する。12blobの各行sliceは1514/18144/4536 Bで全domainを列挙でき、全8059を覆うが、prepare/block全role内の他recipeが不要という証明ではない。

P1 cache/instructionsやmapsの内部読取りdomainは、e.primal_section L4896、e.corrected_source L4903、l.current_section_cached L5458、e.four_B L4913、module.own_dependencies L769等の最初の未列挙境界を明示した。未列挙TCB内fileを除外して最小閉包完成とせず、source inventory全射だけでhidden import不在ともしていない。三batchのfixedは参照manifestであり、実16payloadは旧64fixedにある。

## F5. per-callと旧観測への射影

16単位のcaller表に現P6の実問合せ、CURRENT_REDERIVED/ACCEPTED_CITED候補/OPEN_PREMISE、active資料、採用条項、旧flagの扱いを対応させた。旧λ1450/1578/1706のpairingはそれぞれ異なるquery。最新λ1834の全1834行＋target1706/1834の実pairing、新oracle/候補/最終λはCURRENT_REDERIVEDとして残す。古い別λ問いは具体C(Q)とavailabilityが揃うまで引用未採択。

旧2304phase/2316checkpoint等を省いた時、今回checked件数やnative_pairing_rows_recheckedを元値でtrueにしない。原P6のold_snapshot_numeric_replays=0等から、H2で元から実施していない旧solveを削減したとも言わない。

π_state/π_operand/π_fileは元root/役/順序/三索引/全旧path/空dirへの写像として定義した。実currentactive保全、実cold全rawread、未materializedな仮想復元可能性は別。全旧資料を内部保持して再認証する方式までm証言の消失を必然としない。

## F6. 可用性と費用

Aは登録全cold rawを実EOF/SHAで再読む参照基準。Bは初回独立全復元票＋immutable世代/object存在/長さ/権限/保持・復元契約等を信用する**未採択storage TCB**。pinや保存先存在だけから可用性を推定せず、欠品UNKNOWN_INPUT_MISSING、評価不能OPEN、不正REJECTEDを区別する。全byte再hashと全旧directoryへの実展開も別。

H2の費用をread/call multisetで記述し、cold typed bytes・旧phase/literal parse・個別旧λcallの削除候補と、残るactive bytes/native chain/new相対式/current算術を分離した。Aではcoldraw全I/Oが残る。Bでは代わりに新TCB費用/仮定が増える。旧異λのΣR_iを「同一queryの重複をRにまとめた」と説明しない。H3のdensefactor codecは別将来案、現dense列/零/順序は変更0。秒/上界/wholewalltimeのΘ/速度予言/未来1962は0。

## F7. 明示した残義務

| ID | active保持又は未採択の理由 |
|---|---|
| O01–O02 | 元14親bootとold64attachのnative family別body/除外則・推移read domain |
| O03 | oldordered reduction/literal本文を小さなtyped根拠へ置き換える新consumer/変換契約 |
| O04–O07 | FixedBundle、P1/Task554、maps、import/contextの全内部operand file閉包 |
| O08 | Γ/元word・rho2/旧multi-row・positive等の残前提 |
| O09 | 各歴史Qの具体採用判断/source/runtime/inputscope/限定を封入した引用票 |
| O10–O11 | A/B可用性の具体採用、独立全変換/元全logicalname・bytes・空dir復元 |
| O12 | exclusiveなread/call計器と実費用・性能比較；H3は別案 |

これらは次にactiveを削るときの義務で、現source修理findingではない。本便のsource required findingは0。22/74等の件数一致で全consumer意味閉包を捏造していない。

## F8. 凍結材料

共通場所は %TEMP%/shadow-atelier-audit163/task1116/。各材料はCreateNewで保存し、既source/旧票/親原物は不変。source wholepin、74＋30関数参照と13直読区間、8登録入力、7小nativeJSONと2fixed metadataを最終再照合した。大規模原root scan/数学実行0。

| 材料 | bytes / SHA256 |
|---|---|
| p6-source-boundary-evidence-v1.json | 101964 /38c7fab81c1489c561275ee8566b2ba27b2e7e9aed851019d4d6f9e264004f3a |
| native-small-json-shapes-v1.json | 181008 /c0e5ceb16f5bda32f18c5db13e6ef2c7407579d63e047007043090f31b073f8f |
| native-consumer-refinement-v1.md | 17773 /1c7a3c269ce1cd22b2a0642e0fea785d909aadd8ad4d9065ba0da6688d214c19 |
| active-asset-descriptors-v1.json | 44986 /3cad3c8b0ff6b3b6ebc0e7ef8ca38d7193ae462b94e60f9202029c51f30e50b6 |
| active-assets-and-open-boundaries-v1.md | 12959 /37f8e8335901e67dee87925af36cbb8544271db65a5d92996ec832ef22684bc4 |
| per-call-propositions-and-projection-v1.md | 13427 /b2f605a939686a80dd6df9ad8779a53f08e105d75f14be3c57600722d18aa555 |
| availability-and-H2-cost-boundary-v1.md | 11695 /9c0ee76b21a46441ada8b30f9eea01a1c6bc3613fa966e040d725982a9e2ee93 |
| author-static-closure-and-open-obligations-v1.json | 33466 /42bc6e471f481ffd3560973b3940d58ae46613e0cd35e4c294693afd3b0bb8da |

最終目録は同場所 final-design-delivery-v1.json（本返信と全8材料の全pin、自己を含めない）。全source/1113/1109不変、設計だけの限定完了でfreezeする。

TASK1116_VERDICT: DESIGN_REFINEMENT_COMPLETE_ACTIVE_RETENTION_WITH_EXPLICIT_OPEN_BOUNDARIES_NO_EXECUTION
