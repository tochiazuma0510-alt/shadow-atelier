# Task1119 — C 側の元 native operand / rolling 契約

F1. Task1119（3965 B / d4a6bc7eacc6eb80364e9bd9b31a9ab10c20dfa6b6b7ede09908abce454064e6）と共通 Task1115・裁定2230に従い、1117追補を凍結した後に行った限定設計調査です。根拠は自系 C6、既採択 retained C、root が明示許可した旧 state writer の静読と、事前登録した公開小 JSON です。P6/1113/1116/1118私的本文・1115作者途中票は未読。新 source/fixture、数学実装、変換器は作っていません。

F2. 元の七族を別型として記録しました。全登録39文書の top key/type、対象 native nested keyset は native-family-contracts-v1.json、元 root の8オブジェクトは native-root-identity-shapes-v1.json にあります。下表の key 数は保存された当該型であり、全 nested Gamma を列挙した意味ではありません。

|族|instruction|result の target|正規化行の参照|
|---|---|---|---|
|base|schema/self sha 無し。通常15-key、skipped16-key。reductions は [pivot_id,scalar] の配列|11-key の plain target_reduction。reductions は6-key object列|全8059命令から physical_pivot を元順に抽出し、その pivot_id から physical/coefficient の別 offset を解決|
|delta/seed30|23-key、rolling のみ|15-key self-sealed target-update、new_reductions は6-key列|global1354/offset16377984、delta の一行 file 内では local0|
|seed34|23-key、rolling のみ|16-key self-sealed target-update。old_target_history_replayed=false が追加|global1355/offset16390080、seed34 の一行 file 内では local0|
|packet|18-key、rolling のみ|schema/self sha のない plain3-key|同 step の normalized descriptor、global offset と local0 を別にする|
|refinement|20-key、rolling のみ|同じ plain3-key|同 step の normalized descriptor と元 selected/scan/materialization/index|
|external E|19-key、E 固有 schema の rolling|同じ plain3-key|同 manifest の normalized 行、origin と元 physical h|
|old64|E と同じ19-keyを継承|同じ plain3-key|snapshots/(n−1)/e/physical、外側 step は n|

普通整数・trit・nullable は元形のままです。実 token の型と、旧 validator が個別に行う type guard、全file pinにより固定する字段を区別しました。seed30 の parents.rho2 に premise flag は存在せず、seed34 では true が必須です。seed に架空 HEAD を作らず、plain target に schema/sha256 を足しません。base store descriptor は file/rows/bytes/sha256/eof、命令 descriptor はさらに final_head、seed/packet/refinement file は3-key、E/old64 phase は dtype/shape を含む5-keyです。

F3. N03/O1 の operand は次の境界まで明示しました。base target の全6-key は pivot_id/offer/lead/scalar/physical_sha256/coefficient_sha256。二 offset は operand 内に無く、元 physical_pivot 命令から解決します。normalized 12096 B と companion 2015 B の位置を同じ pivot ordinal に結びます。これを元 physical instruction の2要素配列と取り違えません。

seed target.new_reductions の全6-key は pivot_id/offer/lead/scalar/physical_offset/row_sha256。元 rank の global offset を一行 delta file に seek する型ではありません。parent_result_sha256 は親 result 全file、parent_target_sha256 は元 embedded target 全 canonical bytes、old_remainder_sha256 は packed target の識別です。実 seed30/seed34 は各1項ですが、元契約は全 new_reductions の和として保ち、後続 plain3-key の「新一行 scalar」に cast しません。

将来の数値義務は、base では rho2−R_base=Σ scalar_e N_e、seed では R_before−R_after=Σ new_reductions.scalar_e N_e、packet/refinement/E/old64 の explicit one-row では R_before−R_after=target.scalar N_new です。全48384座標のこれらの式を本便で実行していません。元 writer は零係数を sparse event に書かない箇所がありますが、保存列を補充・並替え・重複除去・係数収集しません。後続 scalar0 でも instruction/target/親参照は保持します。実 refinement 第1 step は scalar0 かつ前後 remainder hash 同値でした。

整数 word 指数も別型です。旧 seed の normalized-word-dag は coefficient_two_means=inverse の注記と、seed34 serializer の literal_exponent=(-scalar)%3 をそのまま保持します。E は明示的に −signed(scalar)、外側 signed(sigma) を使います。両者を保存 bytes 上で相互変換せず、旧 Gamma の全解釈や common positive word を得たとは述べません。

F4. N04 の元 h は、h_next=SHA256(bytes.fromhex(h_prev) || J(instruction から rolling_sha256 だけを除いた全 body)) です。J は元の ASCII・sort_keys・compact・末尾LF、配列順も保持します。schema がある族では schema も body に残り、nested source/reductions/literal も省略しません。base は零32 Bから全8059命令を辿り、skipped/dependent を含めて state/HEAD と manifest.instructions.final_head に到達します。以後は seed30 の1、seed34 の1、packet の3、refinement の26、external E の1、old64 の64命令を、この順の元 predecessor で接続します。

全file SHA、JSON self-seal、物理 h、snapshot/checkpoint/phase の fullfile SHA を別欄にしました。instruction は self sha を持たず、base target/HEAD/manifest も plain です。元 target 親参照97件は base+seed30+seed34+packet3+refinement26 の32件5-keyと、external E+old64 の65件6-keyです。8059命令、base target の884 operand、97親辞書は別の列です。97件を一律10-keyへ変えず、新 core/受付 hash を元 h に代入しません。これは source 契約の静読であり、本便で元 h を再計算した意味ではありません。

F5. 実 caller/return を17行の表へ分離しました。C6 check_actual L4582 の AcceptedInputs が .trees を用意し、L4585 の restore_physical_anchor 内 L1034 が C.FIXED.validate_parent_generations を呼びます。返値は base/seed30/seed34/targets の4-keyで、最後は元 target 3個の順序付き列、元 object を変更しません。C6 は facts.base.target_reduction を初期親へ、同 facts を parent_layout_receipt へ結びます。base_pivot_metadata は1354個の5-key pivot 列を返し、SavedPhysicalRow と ThinAnchor の通常 row consumer に接続します。

old64 には間接 metadata 読取りもあります。C6 L1153 → C.check_invocations → invocation_before_heads → read_checkpoint で、実 checkpoint full SHA・同 snapshot・順序付き phase manifest 全file SHAを読む経路です。一方 C.replay_head_prefix/replay_snapshot の全数値再演は C6 restore から呼ばれません。retained native loader が元実行時に返す ndarray/row/target を、族の説明だけで「履歴 metadata」として省略しません。O1 と O2 は別 source identity のままで、四つの限定 native 関数範囲だけが全raw同一でした。

F6. root 配送5件924041 B、追加34件7727966 B、計39件8652007 Bを内容読取前に登録しました。対象は指定 JSON と source-receipt のみです。58件の native 型・前後識別・manifestへの全file pin結合が一致し、native-small-JSON-join-audit-v1.json は PASS_SCOPED_METADATA_ONLY（failed0）です。元行 payload、8059 JSONL、全word/factor、全親treeを新たに走査していません。h/self-seal の再生成や packed vector の decodeも0です。58件は数学自己試験数ではありません。

11 source 全pin、66個の重複可の限定 raw範囲、表中64参照出現を再照合しました。これは全sourceのEOF分割台帳でも全helper閉包でもありません。v1範囲表は保持し、v2は current check_actual と invocation_before_heads の2範囲だけを追加しています。14依存文書も全pin不変です。source の数値関数を読むことと、その関数を今実行したことを分けています。

F7. 未決と保持範囲は8行で区分し、全該当 role を active に残しました。元8059命令と884 operandの実全row/companion照合、全歴史 target 差分、元 Gamma/P1/literal全解釈、未観測 ConnectionMember 等の一般 branch、全helper/最小TCB/変換器は未完です。これは Task1115 の将来義務で、現 C6 の source 欠陥という判定ではありません。CURRENT_REDERIVED は本便の source/metadata 所見だけ、旧数学は ACCEPTED_CITED、残りは OPEN_PREMISE。可用性A/B、H2/H3の別と正式1834/8539の限定は維持し、未来 a_i/p_i/head や1962を仮定しません。

F8. 全材料は TEMP/shadow-atelier-audit163/task1119/ に保存しました。目録 final-material-manifest-v1.json は7065 B / c4eca00d33dde1c80439dfaff30b2d31fe2ce916b7f42f646f07797484c6441a、自己・本返信を除く16 file /2930535 B /subdir0です。全16件はCR0/BOM無し/最終LF。主要票は次のとおりで、全pinは目録にあります。

|材料|bytes|SHA256|
|---|---:|---|
|source-native-range-map-v2.json|47220|a46df573c54f0261b8d0677e3fef610a03f77914d75053c2cedfcc420b5349b2|
|native-target-operand-and-rolling-contract-v1.json|20012|d2672c75c6fc803233b69db6f7a7945f296d773a40ca3c6a8d819283ddf7a859|
|native-reader-return-consumer-joins-v1.json|19492|08794502c7d526ad4e06a1f8524fdd1b456acad4bd30c37eb0359d52a304f9c1|
|native-small-JSON-join-audit-v1.json|14879|2e3babc47904fdc7c2553169d7b937c531ec662b31076f41435d4c0f1a1ca864|
|author-static-reference-audit-v1.json|39081|3232e2a0317eb6bbac3a4d1734f037a25a6302b3a4229fa2983230fd96451978|

C6 は419541 B /3996972ccfe8ba9c168b537ac274de96ff69a6fe27fb400e7de6a8e3a19a52ff、両登録定数は None のまま。1110/1114/1117・既親・既 process・WFを変更していません。source/Python/GAP/AST/import/compile/数学/自己試験/Git/GHA/network/credential/新agent操作は0。v6追加gateと毎試行の新user許可は0。正式inventory5の後にrootが委嘱する C6 最終bindingを優先する方針です。

TASK1119_VERDICT: SCOPED_NATIVE_CONTRACT_DESIGN_COMPLETE; OPEN_PREMISES_AND_FULL_ACTIVE_ROLES_RETAINED; SOURCE_AND_MATH_EXECUTION_0; NO_NEW_V6_GATE
