# Task1120 — P側 native context / rule 具体登録案

## F1. 判定と実施範囲

指定の bounded metadata/design を完了した。base state、delta/seed30、seed34、packet、refinement、external E、old64 の7群を、実 owner と原型を保った8つの物理 rolling 規則、35実文書 owner、305入れ子 object-owner template に接続した。これは未定パラメータを減らす登録案であり、完成 CoreManifest、全 native family 宇宙、Γ、最小 P1/maps/runtime 閉包、変換成功、availability B の採択ではない。20件の OPEN 字段と保持対象を別表へ残した。

基点は受理済み run34161493396/1、head `a5b456a973f8a917f3af386d327061a02a0cf900`、rank1834/generation8539。新128採用・rank1962・未来 core seal を仮定しない。固定 P6 は453749 B / `75401d4ded04e00187e9a45bfe87603309473a7c6625e6747ecf5c3bf4caa0d7` のまま。18親/k128/caps/親別計器/guard に変更0、既包括認可へ毎試行の新user許可や v6 待ち条件を追加0。正式 inventory5 による P6 finalbinding が後着した場合の優先は保持する。

## F2. 入力登録と三分法の正本

最初の登録 `task1120/input-preregistration-v1.json` は10747 B / `c4d8434a9cc20d7f2e88da27181bb300d6ee52c35665729bd8d9cc21402e1741`。Task1118最終目録7205/`9f4dcf455e4e46ac77b94c684a34d2ae84507ce26a6f3a3459caf920ddbc6291`、自系凍結資料、公開1115 v1六材料/v2四材料とroot公開型票を登録した。既登録の35小JSONだけをmetadataとして読んだ。新しい親全走査、巨大8059 stream、全vectorの読取は行っていない。

後着1115 v3は `additional-public-v3-input-registration-v1.json` 2279 B / `6a149d3d3a7f5e17dce46e0062da89d0897c4660f1c8cff7d77e1a5e5e279168` に別登録。正本 manifest5393/`a8c4693f98cc73ef381f8eab3d0023aa2273ca6d83b39a039384736657863d8e`、delta296340/`0aa42cafc7743d3707c81612e043559a403b39f4062b56d929369572f7607448`、root採択票75515/`824dd740ced5ba2feee3c50193d883ce5147024a8f982b3ec831ee5b004363de` を固定した。R0–R6全文と10種の全scopeを読み、全72行について scope 以外の全 JSON 値が v2 と不変であることをmetadata比較した。`public-v3-scope-application-v1.json` は47162 B / `1301e5dcf0a282b3451be4a4453059802fec416ef0a718b95b909c77eec54aa7`。

したがって v2の退行72 scopeは採択しない。v1各readerの詳細＋v3のCONVERSION/CURRENT_REDERIVED/ACCEPTED_CITED/OPEN_PREMISEとA/Bが最終の正本である。design erratum v3でも型namespaceは `shadow-atelier.r07.cold-closure.proposed.v2` のまま。個々のschema字段を読むだけで全演算を実行したとは扱わない。

## F3. 新しく具体化した owner / 型

`NativeContext.native_root` の whole owner は、baseの state/manifest.json、二deltaの output/manifest.json、packet/refinement/E/old64の output/start.json とした実登録案である。それぞれ元schemaを FIELD として固定する。`RollingFamily.record_schema` は選択 `body.object` 自身、`ObservedNativeRef.document_schema` は selector 適用前のwhole documentに別結合する。

base physical instructionには schema/predecessor/sha256 が無い。selected record は ABSENT だが、tagged state manifest の FIELDを消さない。JSONLのINDEX(o)は元lexical codecの順序上の選択案であり、架空JSON array fileへの変更ではない。全8059 lexical raw_slice/member対応の具体一覧は未測定のためOPEN。入れ子 connection15 とその source6も別 owner/別 ancestry とし、nested predecessorをphysical predecessorへ流用しない。

base target11と二delta target15/16は自分自身のFIELD tagを持つ。後続 plain targetは正確な3key `parent_remainder_sha256,remainder_sha256,scalar` のみでABSENT、そのwhole resultはFIELDのまま。explicit null、未形成、未知型はABSENTにしない。source/positioned descriptorとwhole file descriptor、base/private checkpoint14とold64 checkpoint8、seed/packet/refinement/E/old64の各 version を保持した。観測した各branchのexact keyset/ordinary型と、元writerから判る未観測branchを区別し、305 templateを全宇宙とはしない。

## F4. 初期値・規則・同役の保存期待値

原sourceのbase初期値は `"00" * 32`、すなわち普通の64桁小文字hex文字列である。INITIAL_CONSTANTは変数引数0、physical rollingへの符号化はhex decodeした32 zero bytes。64 ASCII zero bytesやnull/空文字ではない。後続6群は実manifestの parent_state_head 又は実startの state_headへのFIELD bindingとし、直前の別contextのterminalへ独立に結ぶ。存在しないINITIAL_DERIVATIONを追加せず、この7つのinitializerには不要と明記した。他familyに必要なら全typed/ordered/repeated FIELD/RAW引数とenvironmentが別OPENである。

7群のphysical rollingは原どおり `H(hex_decode(previous_h) || C(instruction without only top rolling_sha256))`。schemaがあれば残し、全source/ordered reductions/literal/descriptorを保持する。baseは各位置IMPLICIT、他6群は実predecessor等のSTORED列挙。digestは全primary instructionでSTORED。terminal/duplicated same-role fieldsを文書・context・役割ごとに列挙し、同じ値だからと統合しない。今回の35小JSONにあるhead系H参照13262件は位置・selector・値を全保存し、別contextのsource/P1/ancestry/whole HEAD SHAも分離した。これは全original宇宙の参照走査ではない。old64の未再登録terminal result/checker等、残るfull occurrence closureはO08/O09へ残す。

rootの限定指摘を最終catalog v3へ適用した。FULL-FILE-HASHは常に元fileの全raw bytes/EOFのSHAであり、sealやLFの存在は要件ではない。存在すればそれも含む。H(C(object))との同一性は元codecとraw完全一致が成立した場合だけである。JSON/selfseal・physical h・packed target・target object・manifest/checkpoint full hashを混同しない。自系再読でもE/old64のnested期待値の正確なpathは `separator.lambda_rho2.target_derivation.new_delta.state_head` と確認し、catalog v1を保ってv2で訂正後、v3へ継承した。

## F5. 現 consumer と将来義務

私的対応表B01–B15は `m.validate_old_state`、二deltaの `p2.load_saved_delta`、packet/refinementの各loader、`L.attach_e_delta`、`PhaseStore`、P6の `accepted_oracle_top_metadata` / `thin_anchor` / `parent_row_sources` 等の実範囲へ結ぶ。public/native登録と自系callable根拠は別材料であり、C private source/返信/fixtureは読んでいない。

現在の元8059全文rolling、全9phaseのtyped/fullbytes、stored scalar/plain-target/row/hash照合、metadata predecessor/checkpoint比較はACTIVEの実用である。RAMから捨てること、歴史的な出自や引用予定をcold化の根拠にしない。target/descriptor等に架空の零リンクfamilyを作らず、N01–N08のwholebody/型/row-target/context/fullhash-chain/相対式/pairing/97mixed/運用証拠の契約へ分けた。step/phase/checkpointのfullfile参照鎖を、完全宇宙で別RollingFamilyに分類するかはO11に残すが、現在必要なfullhash/順序/前駆比較は落とさない。

元8059、mixed97、anchor1450のΓは別clause。旧lambda1450/1578/1706、最新親lambda1834の全行・二target、新candidate/新lambdaも別query。新しい全中間targetの数値差分は1115の将来CURRENT義務であり、現在のPが全て実行したとも、既sourceの不具合ともしていない。元rho2直接read、original word/lower/positive/A0の不足はOPENを維持する。

## F6. OPEN字段・CONVERSION・A/B

20項目のOPEN表には、各実字段・利用consumer・不足理由・保持するrole/fileを付した。残件は特に、全original/family宇宙と全member span、採択済み完全native契約、原runtime/辞書/P1/maps、正確なΓ/引用条項、未登録の全terminal/copied reference、全中間targetの将来計算、checkpoint universe、変換/復元/現在use-stability、Bの追加TCBである。これらをnull/偽SHA/偽pathで正規wireへ埋めない。

CONVERSIONは全原file→全出力→全復元のEOF/実raw対応と全dir/emptyを独立に閉じる別操作。CURRENTは必要ACTIVE全体と実operation。Aは毎run全COLD bytesをEOFまで再hash。Bは既全復元＋個別採択したimmutable generation/TCB＋全COLD現在存在/長さであり、current full cold hashや旧数学再演とは記さない。B採択0、変換artifact作成0、性能実測0。既受理結果やLean用語へ昇格しない。

## F7. 最終材料と自己点検

以下は全て `%TEMP%/shadow-atelier-audit163/task1120/` の新/versioned材料。旧v1/v2・1118等は不変。

| 最終材料 | bytes | SHA256 |
|---|---:|---|
| public-native-rule-catalog-v3.md | 21335 | 5fc1ff86f011ad38a09f5283ad865f4b1e5e52587c02778fcd7a4230e81ee527 |
| public-family-and-rule-parameters-v2.json | 45275 | f79ce72fc86e6adccea90c764f7d1ced1540df8bf9173bf35dfced6516244de2 |
| public-native-owner-registration-v1.json | 994443 | 93f107a8a65ffb8576ff9f9b95dbca8905ec9839c14b6884401d23afc41c79fd |
| public-selected-owner-shapes-v1.json | 505021 | a09861a213c99319b8c82cbc51f4e66639e63e617b3e6295235573978686448a |
| public-stored-head-occurrences-v2.json | 6410116 | 35459661a36fac9419c400b4b8ef2d4491d993fdd252c14c5993619d0a7f093d |
| public-native-source-range-pins-v1.json | 78189 | 0777dcc05b730938ceba4c55e7b7229c4493811c74c14ff2bdf0dcb810e9c99f |
| public-native-shape-and-null-contracts-v1.md | 10517 | de7dbbfca7322e631c8999b4e57a80b44abd7e31b60b74bb73d2154def8ec16a |
| public-open-fields-and-three-way-scope-v1.md | 10904 | 979b4b184d33e71c8642ff4b62dfd0b8802bd3c34373af04fa710b7385306c0c |
| private-source-and-small-input-evidence-v1.json | 138575 | 73a97f2a3a427621d6acf42a88e16a32abad829c94d52990f150e4e967a7d3da |
| private-current-consumer-and-rule-binding-v1.md | 10623 | cb446ed68107ccf96db31e60429a26d2d73e08445433547366538797c943959e |
| author-static-closure-v1.json | 21236 | 7194b2e0deb69e3feeea84a6e26bd415ca618b23c728398c734677e9a273a67d |

自己点検は132 raw範囲（今回raw範囲を再読した9 source）と全35小文書のbefore/after pin、7 family/8 rule、35/305 owner、13262全参照位置/値/selector、7つの二重配列excluded_fields、追加72scopeを閉じた。入力pinの再照合40件は重複登録を含む照合回数であり、新しい40親や40個の独立宇宙ではない。全source/math/selftest/AST/import/compile実行0、Git/GHA/network/credential0、親/旧資料への書込0。

PS metadata helperは新規資料生成のため実行した。最初のv1は H aliasがGet-Historyに解決され、出力前に停止したため、新v2で専用名へ変更して完了。family helperは未実行v1を保持しv2でexcluded_fieldsの二重配列を明示。後着入力登録後の読取コマンドに局所B/b名衝突が一度あり、登録済み正確pathの別コマンドで全文読了した。いずれもsource/数学実行や親変更ではない。全既版は残した。

全材料は別ファイル `final-native-registration-delivery-v1.json` へ self-excluded で全pinを固定する。public候補とprivate読取根拠、旧中間版/metadata helper、最終返信を区別して記載する。未閉鎖の全宇宙・Γ・TCBを成功扱いせず、登録可能な具体字段/規則と残る未来義務の境界でこの便を閉じる。

## F8. Ledger選択述語の事後明文化

rootの限定指摘に応じ、`public-ledger-selection-and-classification-erratum-v1.md` 7283 B / `a2e74f482967f293eb44e9569248db65757b14cc1b28e95c6a95e32e5c9eaaa8` を追加した。35文書の事前登録と、列選択を形成後に明文化したことを分ける。実述語は値がSystem.String、case-sensitive `^[0-9a-f]{64}$`、keyがcase-insensitive `(^head$|head_|_head$|rolling|predecessor|ancestry_sha256)`。実16key集合は観測結果であり、元述語を16literal allowlistへ後付け変更しない。

原登録documents順、各PSCustomObjectのProperties列挙と深さ優先、arrayのINDEX0..n-1、KEY/INDEX selectorとescape済pointer、first-match分類の全優先順とv2の4つの役割補正を正確に開示した。元実施本文の根拠はmetadata helper v2のL22–38/L46–65、後処理helper v2のL31である。全13262のlexical抽出完備性と、全native期待値宇宙/同役分類の意味上の閉包は別。O08/O09はOPEN、元ledger v1/v2は変更0。

この追補を結んだ最終自己票は `author-static-closure-v2.json`。旧自己票v1/返信草稿もTEMPへ原bytesのまま残し、最終目録で区別する。source/数学実行0、実親再scan0を維持して凍結する。

## F9. 末尾 LF と実 ledger 値の限定訂正

root の追加指摘により、`public-ledger-selection-regex-erratum-v2.md` 1812 B / `9b313389a327a83680b27aaca037918cb71c59e18931e51bea8b1134615a14d2` を保存した。.NET regex の `$` は末尾 LF の直前にも一致するため、F8 が参照する v1 の L2 にあった「長い文字列は常に抽出されない」という一般化だけを撤回する。元の実述語は変更せず、native H 文法や consumer gate も変更しない。

既に保存された ledger v2 の値だけを直接読んだ観測は、13262 件全て System.String / Length 64、LF を含む値 0、CR を含む値 0、厳密な全体 lowercase-hex 64 文字から外れる値 0。これは今回の実値の性質であり、元 regex が全可能入力に同じ性質を強制する主張や全 file pin だけからの推論ではない。原入力文書の再 scan は 0。選択・分類・全旧 ledger・自己票 v1/v2 を保持し、この短い訂正を最終目録で優先適用する。

TASK1120_VERDICT: BOUNDED_NATIVE_CONTEXT_AND_RULE_PARAMETERS_REGISTERED_FULL_UNIVERSE_GAMMA_TCB_OPEN_NO_SOURCE_OR_MATH_EXECUTION
