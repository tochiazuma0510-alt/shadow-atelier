# Task1132: Q1450 の公開作業報告 wire 案

F0. 一つの具体案を公開設計として閉じた。正本は TEMP/shadow-atelier-audit163/task1132/public-work-report-wire-v3.md（26171 B / d7e534a5cf1a644a00850f4010dd7edfc0d3ef829315098af424b8e569d4b194、116行）。新namespaceは shadow-atelier.r07.q1450-work-report.proposed.v3。これは型・義務・紙上例であり、新しい実run receipt、実装、引用適用又は数学測定ではない。1108/1127 v2・正式handback優先を維持し、v6追加gateは0。

F1. 過去の採択Q1–Q3、今回Pの自己観測、今回Cの自己観測を別の来歴にした。数学対象1450行と、成功した現在row検査、戻ったrow-dot、二つのtarget-dot、三種類の実引用消費を7個のevent kindに分ける。各ownerの実execution/source/runtime/query/ordinary occurrenceを固定し、過去1450から未保存の過去作業件数を合成しない。現在の実Gamma・同一operand/lifetime・TCB・effect・availability A/Bは過去条項の採択と別の前件である。

F2. CountEstimateは UNKNOWN / LOWER_BOUND / EXACT。recorded_completedは保存eventの件数、actual_completedは明示範囲への知識である。健全な単射の根拠で下限、閉じた範囲の全被覆まで示してexactとする。dotのreturnから記録までの中断窓や保存失敗を0にせず、事前incrementはattemptであってcompletionに数えない。全被覆根拠はcounter値とは別に必要だが、第三者観測を必須とする意味ではなく、同ownerの採択された計器/runtimeの根拠でもよい。EXACTは第三独立性やLean verifiedの格付けではない。

F3. root所見をv3で反映した。旧checkpoint TraceSnapshotを参照するmetricは、そのcheckpointまでの範囲に限る。後の停止までの下限を述べるには、同じ保存eventsでも後の実境界を明記した新TraceSnapshotが必要であり、end.classificationだけで期間を暗黙延長しない。境界や観測の健全性が不明なら、旧prefixだけを保持又はUNKNOWNとする。

F4. CのPeerAuthenticationはP wireの全bytes/schema/subject/数学値/内部整合性を認証する。PのelapsedやcounterをCが独立観測したことにはならず、P_SELF_OBSERVATION_NOT_INDEPENDENTLY_MEASUREDを保持する。C自身の作業は別WorkReportである。paper-scenarios-and-publication-order-v1.md（12702 B / 762b1f2661d525975386669edb95f867e3421be3a6cbd1a56d3745c68110115d、44行）は直接/直接、直接/引用、引用/直接、引用/引用の4組合せと11停止・欠品等の例を定義した。表の件数は全被覆等を仮定した紙上内訳で、実測値ではない。

F5. 将来current P intakeだけを新4-key wrapperにする具体案を選んだ。現49字段のうち46はNativeV6(field)依存型として原native reconstructionの型・値・nested検査をそのままimportし、3字段をschema版上げ・外部whole-file pin・Q1450作業報告への分離で扱う。他3 queryのP宣言[1578,1706,1834]は保持する。旧49/歴史41字段や元start/timing/sealは改変しない。NativeV6は名前だけから型を推測したAnyではない。根拠はroot公開current49宣言とopaque source束縛、及び公開P1129/C1130のquery/return/effect・packet consumer契約であり、未提供nested型を今回再構成したとはしない。

F6. public-field-correspondence-v2.json（71611 B / a96c07874d9f89daedd15f645b53d47a803f72bd06272fba997749d2f453b10b）は全49 intake、P12/C10 timing、Return5全5字段及び歴史41名を対応させた。Pの選択timerは continuation/state-restore-and-pairing/保存ordinal22、Cは continuation/direct-pairing/ordinal0である。P実start/finish/elapsed、Cのelapsed-onlyとfloat_seconds、元files/file_bytes/rows/recordsを保持し、数量はdomain/ancestryでdot件数ではない。P26/C31順序・inclusive scope・他の計器は元契約のまま。現在intake writer、rechecked伝播/guard、後成start→selection→root-record、C再構成とresult、選択timing readerの将来版分岐義務を全対応表に記した。

F7. file pinは後成→先行だけにする。将来pre-call execution/runtime/invocation declarationとOccurrenceを先に形成し、実trace/applicability/clock/coverage→WorkReport→CurrentIntake→後成start/selection/root-recordの順とする。報告から当該intake/startや後成invocation hashへ戻さない。C自身の観測とP票認証の実順序を勝手に仮定せず、後成C result/Bundleが両枝をpinできる。既sourceにこのpre-call recorderがあるとはせず、必要な将来実装義務を明示した。

F8. v1は保存。v1→v2は14置換（40桁Git head型、4数量保持、P22/C0、owner/型/参照等の精密化）、v2→v3はversion2箇所と範囲段落だけで、双方の全raw順逆一致をPS/.NETで照合した。中間wire-decisions-v1 D3の independent evidence は「counter値とは別の全被覆根拠」の意味に限定して最終本文で明確化した。全本文・全差分・全対応表・紙上例を自己読了した。集約表示の切断部は個別の限定行読取で回収した。

F9. final-input-preservation-and-text-audit-v1.json（12457 B / 106ae208e0a48ed1840b1c4036d113c690037c2e2b7e515138defff875bfaae1）は事前登録12入力と1127 v2の3凍結物の全bytes/SHA不変を照合し、公開大JSONの今回の限定読取範囲も区別した。最終全材料目録は同dir final-material-manifest-v1.json。旧材料を上書きせず、新TEMP材料とこの指定返信のみ作成した。private P/C本文、実親/process、Git/GHA/network/credentialは操作0、source/数学/Python/AST/自己試験実行0。

F10. 未実装のpre-call記録、計器の健全性/全被覆、同一subject/寿命、適用Gamma/TCB/effect、正確な既native reader再利用、P/C局所adapterと全current publication consumerの実装/採択は残る。完全AcceptedClaim、完全Gamma、新しい実適用・費用・rank・作業receiptは作成していない。設計完了をこれらの成立へ昇格させず、正式handback到着時は1108/1127を最優先する。

TASK1132_VERDICT: PUBLIC_PAPER_WIRE_COMPLETE; IMPLEMENTATION_AND_CURRENT_APPLICABILITY_OPEN; NO_RUNTIME_INSTANCE; V6_ADDITIONAL_GATE_0
