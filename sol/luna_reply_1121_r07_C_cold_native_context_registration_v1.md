# Task1121 — C側 cold native context・rule の具体登録案

## F1. 結論と射程

Task1121（7164 B / 0218cfd4caf5a4a2aa1e3153fdc345236bd1f6fc916745343ce36f1eaaf0800a）を全文読了し、既存 C6 の native 実体を公開1115の owner・union・rule・family coverage 型へ接続する限定設計を完了した。7 origin の physical chain 案、47実 owner＋2文法 owner、位置付き60期待値、13 nonrolling用途、12本の自系 current call 接続、14項目の OPEN 表を新TEMPへ保存した。完全 CoreManifest・実 NativeContext/AcceptedClaim・実行票を作ったという判定ではない。

正式出発例は run34161493396/1、head a5b456a973f8a917f3af386d327061a02a0cf900、受理済み1834/8539。未来1962・新採用数・最終λ・core sealは仮定しない。C6は419541 B / 3996972ccfe8ba9c168b537ac274de96ff69a6fe27fb400e7de6a8e3a19a52ffのまま、THIRD_BATCH_INVENTORY_REGISTRATION / CURRENT_PRODUCER_REGISTRATIONのNoneを保持。旧1110/1117/1119、source/WF、親、root受領processは変更していない。P6/1113/1116/1118/1120 private本文の読取、新agent、Git/GHA/network/credential、Python/GAP/AST/import/compile/source/数学/自己試験実行は0。許可されたPS/.NETの原文・JSON metadata・bytes/SHA照合のみを実施した。v6追加gateは0、正式inventory5と最終source結合の委嘱が届けば最優先で復帰する。

## F2. 入力登録と公開scope v3

入力は初回40 metadata票、11既採択source、旧1119由来の39小JSON（8652007 B）を事前登録した。後着の正式1115 scope-only v3は、root票を含む5入力を別登録した。最終自己票で計95論理入力pinを再照合し全一致。親全artifactの新scan、8059 JSONL全読、packed/vector読取・演算は行っていない。旧66 raw範囲を再hashし、元writerの定数を確認する1–153行（offset0 / 7045 B / da479cda6039fa84b2859d6cb0274bcd0e46a363984fe6008a8cd838daaa4836）を読取前に追加登録した。合計67範囲は重なりを持つ範囲表であり、11 source全EOFの意味分割ではない。

型は公開1115の proposed.v2（有効524字段/85型）、scopeは正式v3とv1各reader詳細を用いる。初稿で拒否されたv2の72退行scopeを採択しない。後着v3の全72変更はscope限定と照合し、選択した110 reader行中61行へ適用、残りの詳細を保持した。選択型字段は92。namespaceをproposed.v3へ変えず、今回の書式修訂と型版を区別した。基点v1票は上書きせず残した。

## F3. 三つのschema ownerと具体値

NativeContextのnative_root候補は、baseのstate/manifest.json、delta/seed34のoutput/manifest.json、packet/refinement/E/old64のoutput/start.json。各origin-qualified Idに実root/file/全bytes/SHAを結び、各native_rootのFIELD tagを登録した。Idは提案名であり、完成OriginalRootや採択済みcontext参照ではない。

NativeContext.schema_declarationはnative_root全体、RollingFamily.record_schemaは選択body.object、ObservedNativeRef.document_schemaは値を選ぶ前のdocument全体に、それぞれ別に付く。全39小JSONと8個のtarget選択を実キー集合へ結び、43 ownerはFIELD、4個のplain3 targetはABSENTとなった。含有resultにFIELDがあっても、そのtargetへ転写しない。baseの11-key target、seed30の15-key、seed34の16-key、後続のplain3を区別した。deltaのparents.rho2.target_derivation_accepted_as_premiseは欠落、seed34の同字段は厳密trueであり、前者をfalseと補わない。

baseのJSONL全体と各15-key通常/16-key skipped recordは別ownerで、原writerがheader/tagを書かない文法から各ABSENTを提案した。実8059 recordの全membership/各Sliceは未作成であり、2件とも文法根拠として明示した。未読・欠品・null・未知variantをABSENTにしない。普通整数とBool、元の符号/指数/零・重複/配列順を保持し、PSのCLR型観測だけで将来decoderの数値字句規約を全充足したとはしない。

## F4. 元initializer・rolling規則と期待値

Jは元のsort_keys/compact/ensure_ascii/ASCII＋末尾LF1個のcanonical JSONである。物理hは H(decode_hex(previous_h) || J(instructionからtop-level rolling_sha256だけ除いた全body))。schema/predecessor・nested seal・literal/reduction body・零係数を追加除外しない。wrapper字段やSelectorPath集合順を元bodyへ挿入しない。inner seal、全文file SHA、physical hを別の役として登録した。

| origin | 元physical member順 | initial / predecessor |
| --- | --- | --- |
| base | offer0..8058、全kindを元順 | Text64個の0（ZERO_HEAD = "00" *32）を32個の零byteへdecode。各recordのpredecessorはIMPLICIT |
| delta/seed30 | instruction1件 | base終端へ結ぶ実FIELD / STORED |
| seed34 | instruction1件 | delta終端へ結ぶ実FIELD / STORED |
| packet | step1..3 | seed34終端へ結ぶ実FIELD / 各instruction STORED |
| refinement | step1..26 | packet終端へ結ぶ実FIELD / 各instruction STORED |
| external E | instruction1件 | refinement終端へ結ぶ実FIELD / STORED |
| old64 | step1..64、snapshot=step−1 | E終端へ結ぶ実FIELD / 各instruction STORED |

baseの零初期値は空byteでも零byteのhashでもない。resumeは認証された既prefixを継続する。各後続FIELDは前context終端とのincoming equationも要求するので、任意seedを自己申告してよい意味ではない。selected7群ではINITIAL_DERIVATIONを架空に作らない。他native族が実に導出initializerを持つなら、FIELD/RAWの全引数型・順序・重複・環境を登録するまでOPENとする。

39文書のprimary physical字段60個を16位置へ分け、層間6組を保存Textの同値で接続した。各項目に実全文pin、document schema、KEY selector、native位置を保存し、packet/refinement/old64のstep1とterminal3/26/64を混ぜない。hやsealの再計算は0。未登録の残member/期待値をDERIVED_ONLYへ変えずOPENとする。今回選択したphysical link/terminalは全STOREDであり、実に未保存と立つ別native出力だけが将来DERIVED_ONLYの再導出義務を持つ。

全10468 named-field出現の索引も保存した。内訳はraw-event h5362、P1 predecessor2785、earlier-pivot word reference1791、legacy named-parent h344、embedded-layout h116、full-file metadata pointer8、primary physical60、別native/query参照2。これは10468 chainの意味照合や再計算ではない。base p1_identity/instruction/final_headとpacket scan.state_headも別役に保つ。7 originを全native宇宙と宣言しない。

## F5. 現在の用途と別族

private-C-current-native-parameter-use-joins-v1.jsonに、公開字段→実native object→自系通常callerの12接続と20再読raw範囲を別保存した。公開数学登録案には相手private実装を入れていない。C6のbase_pivot_metadataは8059全body/h/EOFとpivot位置を読むが、全offerの数学再演ではない。restore_physical_anchorのappend_savedは元instructionのh、target/normalized/full-file身份、ordered named親、六key DERIVED/new_deltaへ接続する。これらの現在のbodyはACTIVEである。選択60字段のうち直接比較する箇所と、全文pin/seal入力として保つがその字段自体の比較をこの経路で主張しない箇所を分けた。全caller閉包をこの12行だけで得たとはしない。

step/phase manifestのpredecessorは元null又は前manifestの全file SHAで、physical hの連結則とは別。old64 checkpointは八key sealed prefix要約/content addressであり、instruction式のrollingを持たない。C6の通常check_invocations→invocation_before_heads→read_checkpointとphase全文pinの読取をcurrent nonrolling用途として保持する。未登録checkpoint本文を仮造せず、規則から導く歴史HEADを保存済み歴史HEADの実読と呼ばない。

13のnonrolling用途と4つの非rolling文書類を具体化した。元target884個の六key operand、元97親（32五key＋65六key）、後続384十keyは別の列である。local file offset0とglobal physical_offsetも区別する。literal/reduction bodyは元hのcurrent入力であり、signs/coefficientsのcurrent返値用途も既1117混合return追補で保護した。旧62 helper全部のper-helper next-consumer閉包とは呼ばず、未列挙55本はOPEN/ACTIVEを継承する。

## F6. 三分法・A/Bと14 OPEN

CONVERSIONは全原file/出力/復元のEOFとraw対応、CURRENT_REDERIVEDは実に必要なACTIVE入力と演算、ACCEPTED_CITEDは正確な採択条項/来歴/閉包とavailability票を読む。引用だから旧native body/数学を暗黙に再演するわけではなく、並行してcurrent用途があればACTIVEを保つ。OPENはPASSへ補完せず、必要資料欠品はUNKNOWN_INPUT_MISSING、型/契約違反はREJECTEDとする。

Aは毎run全COLD普通fileをEOFまで読んでhashする。Bは既全復元＋個別採択のimmutable-generation TCB＋全COLD objectの現在存在/正確長であり、現在の全COLD再hashや旧native/数学再演ではない。BのTCB採択は今回行わない。ACTIVE input/controlのbefore/after義務は両方で維持する。

公開OPEN表14行は、全native catalog、採択public contract、source/runtime、辞書/P1/maps/foreign bindings、全member/Slice/期待値、未観測variant/字句型、seed constructor、metadata chain分類、実checkpoint入力、Gamma三範囲、別λ query条項、未来の旧数値transition、B前件、混合helper閉包を、各通常readerと保持role/fileへ結ぶ。欠けた正規字段にnull/[]/架空SHA/pathを入れない。Gamma.original8059/legacy97/anchor1450、旧1450/1578/1706の質問、現在1834の全行・二target・新λは別clauseである。全旧multi-row/one-row target数値照合は将来1115の義務で、現C6の既実施事実やsource欠陥という主張ではない。

## F7. 最終材料と自己照合

材料はすべて %TEMP%/shadow-atelier-audit163/task1121/。全目録はfinal-material-manifest-v1.json **12031 B / 5faf75820a81a8280fdb8b9f18e95764adb8b93ce16f2a118908e9dc48f52127**。自己と本返信を除く19 file / **26376200 B**、subdirectory0を収録し、各whole SHA/bytes/EOLを記帳した。公開本文はpublic-native-registration-proposal-v1.md **9666 B / fb9b845444517cddaecf8de47011e5b014351c9675bae61addfdb815f76c1bc2**。private caller票は明示別材料である。

| 主要材料 | bytes | SHA256 |
| --- | ---: | --- |
| public-wire-parameter-basis-v2.json | 259664 | 699b48c757488b4e429618ab0264e5772014310eebbd31903ae6fe8e60f3ef5e |
| public-native-owner-context-candidates-v1.json | 613091 | a591ebc5fc8fb2ba9e3b11d8400f1918f2986ccfaf8852287554335ab12dcb86 |
| public-native-rule-catalog-proposed-v2.json | 21759 | 918e866faed2e1cfe7478e06e9b32e2c1ed03108040b8de1f032bd76d9ef1916 |
| public-native-family-coverage-proposed-v2.json | 38931 | 21e0333bde1bd2b39f9ebbc4caa115c8cc0b1b7db5906bd43e54524c17d2bf0e |
| native-stored-expectation-bindings-proposed-v1.json | 307320 | 41d2156df304a348ef9ce1099af068105a7ccc4165950bc033dfd69866374c2c |
| private-C-current-native-parameter-use-joins-v1.json | 43221 | 9d8d57abaf09ebf195fbc2cb6c608e7d76a3d7a3891d0ef4fa472f9714bf460a |
| public-open-parameters-and-operation-scope-v1.json | 16268 | 8b14f6a2b6a8775eba29bd61fd12b113670550e453c7758912a270fca2d1ec70 |
| author-static-parameter-join-audit-v1.json | 115299 | 48f41a0410468256f1adb46015f1599306158852dc9a9768038b30db368c5581 |

最終自己票は95入力pin、11 source/67 raw範囲、47 ownerの実keyset/tag、60実selector/値、10468索引の重複なし全分割、current12接続の範囲参照を照合した。これはnested全意味・全ordinary字句・全数学を閉じた判定ではない。source範囲20本は今回current用途へ再読、他範囲は登録済み1119根拠と明示追加読取を区別する。全67を新規全文意味監査したとはしない。rule v1→v2は定数locator44→45だけを全raw逆対応で確認、family v2はGamma SET順と60字段票への具体参照を修訂した。旧版は全保持している。

## F8. 凍結判定

指定設計の具体登録可能部分と未閉鎖部分を分離して完了。新資料には新Core/Γ/AcceptedClaim/完全catalog/最小TCBの採択、availability Bの発効、数値再導出、cross-checked/verified/A0の昇格を含めない。入力/source不変、実行/親変更0、v6追加待ち条件0のまま、本返信と最終目録の版を凍結する。

## F9. root別読による優先scope訂正

rootのP1–P6別読に従い、元writerの一般文法と固定base8059の受理範囲を分離する。元writerにはphysical_dependent枝があるが、今回の固定8059 intakeは既審査のphysical_pivot/skipped範囲である。既登録J001（515 B / 2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433）のphysical_rank=1354、skipped=6705、dependent=0、source_offers=8059を保持する。dependentの実出現やcurrent intake拡張を主張しない。F4の「全kind」と公開P2/rule/coverage/grammarの該当文は、固定入力の全occurrenceを保つ意味と、writer一般枝の文法説明をこの二範囲へ分けて読む。新8059 stream scanや数値演算は行わない。

優先訂正票はpublic-dependent-variant-scope-erratum-v1.md **3238 B / 0e2b24210651c4a0d0491b2d7c8987e421d1d1bc6dac591283f619131c177332**。旧19資料と目録v1は全raw不変、追補前返信もreply1121-before-dependent-scope-erratum-v1.md（12912 B / fea28eeb6699119404c453c2f8760c3098c488c8c4e725489222b5fc35979962）へ原bytesのまま保存した。現在の最終目録はfinal-material-manifest-v2.json **14097 B / 6b33e01f3bd931aa237e184f59400abb040b0f443afb8e63867e592c12b6bcba**、自己/現在返信を除く22材料 / **26404381 B**、subdirectory0。このF9をF1–F8の該当scope表記より優先し、他のbound値・OPEN・source不変・実行0・v6追加gate0は不変のまま再凍結する。

TASK1121_VERDICT: LIMITED_STATIC_NATIVE_REGISTRATION_DESIGN_COMPLETE_WITH_EXPLICIT_OPEN_PREMISES; NO_CORE_OR_RUNTIME_CLAIM; V6_ADDITIONAL_GATE_0
