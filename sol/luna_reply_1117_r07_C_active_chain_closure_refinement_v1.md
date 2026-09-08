# Task1117 — C側 active 相対鎖と引用境界の改訂

F1. 結論と範囲

初期案は、全登録相対target式と元rolling各リンクをactiveに残す。1114 K02の「旧body/rolling再構成を一括引用」は撤回し、K08もinstruction全body・target全JSON・row-manifest・必要な前後target/実際の行データ・native rootを残す形へ改訂した。旧巨大literal/reductionは、別の意味consumerとΓの依存が閉じたものだけ条件付きcold候補である。1114/1110の保存版を変更していない。

1117指示3732 B/20aa06c44d1883e0b9f2b27debd02c3714c376d9ef28a8b2793f6283bafe5a2a、共通1115指示6105 B/5ae5a24956858e1b9a7fdae22ec430df0c7e78993c6d281c8a884585ae1d746c、2230 ack1208 B/d19f122bdfae8ebc23581230adabd655e462c39c8892967fc7ebae0946f37a31とsnapshot3287 B/7da29b2e4d3144a4b4c441b73ef4e5fb13feff93dc1a3e3774288b5b7c353b4fを全文読了した。P私的source/設計/返信、1115作者途中票、1116は読んでいない。正式1834/8539・限定7・v6/18親/k128/同capsを保持し、未来のa/p/headは変数、1962は仮定しない。

F2. 元body、相対式、hashの三つを分ける

固定C6は419541 B/3996972ccfe8ba9c168b537ac274de96ff69a6fe27fb400e7de6a8e3a19a52ff。全33依存・165 raw区間・42callsiteを再結合し、関連62 readerの全bodyと戻り値を11族へ結んだ。字句行は検索補助として保存し、ASTや全内部file閉包を得たとはしない。58の具体的主張区間にもoffset/bytes/SHAを付けた。

| native経路 | 凍結C6での実読取と保持する鎖 |
|---|---|
| base_pivot_metadata、883–914行 | 全8059 JSONLを順に読む。各元recordからrolling_sha256だけを除くbodyと前hで計算し、零hからL.OLD_HEADまで全リンクを閉じる。非pivot recordも落とさない。 |
| restore_physical_anchor、991–1161行 | 原基点とdelta/seed34/packet3/refinement26/E/old64のinstruction、result.target/pivot、manifest、必要snapshot/step境界を読む。旧instructionの除外はrolling_sha256だけ。元97は32五key＋65六keyの原形と順序を保持する。 |
| 保存v3/v4/v5 row reader、1467・2109・2945行～ | 各instructionのrolling bodyはschema/sha256/rolling_sha256の三つを除いたexact17字段。前h、global/local/candidate、offer/lead、物理/target/literal/係数等のhashを含め、全リンクを閉じる。外側sealはsha256だけを除き、rolling値を含む。 |
| check_saved_batch_target、1203–1211行 | plain3-key targetのscalar、前後packed SHA、target JSON全SHAとinstruction.target_sha256を照合する。これだけで旧全ベクトル差分を計算したことにはならない。 |
| 現BatchReductionState.reduce、502–524行 | 新候補について実target減算の全座標一致を行う。現最新λの全行/二targetと新候補・新finalは引き続きactive。 |

全旧transitionの数値差分・中間target照合は、1115が将来の受領器へ課す義務である。現C6の既実施事実にもsource欠陥にも読み替えない。各one-rowでは実packed前後targetと実normalized行から差=theta×行を照合する。delta/seed34はnative new_reductionsの全項和であり、新しくappendされた一行へcastしない。元rho2→baseの原点命題はΓの条件付き前提に残す。

C6はretained validatorのfactsやtarget全objectを読むが、旧multi-rowの全nested row locatorを自分の直接field列で展開してはいない。用途表ではこの将来必要字段を実直接readと別欄にした。型・locator表が閉じるまではstate/delta/seed34を全role activeに残す。P1/maps等の未列挙TCB内部も同様で、実fixed16 payloadをreceiptへ置換しない。

F3. K01–K15の改訂

| K | 今回の設計判断 |
|---|---|
| K01 | active全bytes/保全とcold可用性を分割。同一fileにactive用途が一つでもあれば全原fileを残す。 |
| K02 | 元8059/元97/旧物理鎖のrollingと相対targetをactive保持。一括引用を撤回。原word/rho2/Γの前提は別。 |
| K03 | λ1450・全1450行・E/continuation-start targetと最終targetの別問い。具体採用条項R1450が揃う時だけ数値pairingを引用。 |
| K04 | R1578の別pairingは引用候補。ただしv3鎖とv4 intakeのnative境界/rawは残す。 |
| K05 | R1706も同様。v4鎖/v5 intake境界を旧dotと一括削除しない。 |
| K06 | 最新1834行・λ1834・正しいv5 start target1706/最終target1834を実照合。 |
| K07 | native root/受付/層境界の全必要bytesを保持。中の過去assuranceを読んでも今回再計算に昇格しない。 |
| K08 | instruction/target/row/record-wise Dはactive。旧dense bodyは別用途まで閉じた場合だけ条件付きcold。 |
| K09 | old64の元snapshot/step境界や必要終端checkpointを残し、その他過去運用の再読を分離。現progressは全保持。 |
| K10 | 過去loader raw同一性は具体証拠を引用可能。今動くcode/raw/runtimeの認証はactive。 |
| K11 | 元old64固定16実payload、geometry/P1/maps/未列挙数値roleを全保持。 |
| K12 | 最新λのselection全相、全chord/auxを保持。 |
| K13 | 今回候補の全相・全rank係数/零/順序・-sr/外sigma/+srを保持。 |
| K14 | 新finalの全行/二target又はtyped Linearを保持。全相対鎖と原Γを分離し、原rho2直接読取へ昇格しない。 |
| K15 | 今回prefix/一相先tail/diagnostic/invocation/final/全before-afterは保持。過去引用で現在の停止枝を通過させない。 |

R1450/R1578/R1706には、それぞれのλ・全行原点/順序・二targetの全pin、実P/C成功、実source/runtime/入力閉包、run/attempt/head/artifact、採用裁定の具体条項と限定が要る。最新λの全R行照合から異なる旧λの問いを推論しない。未採用ならOPEN又は従来の実計算を残す。現在のmeasured属性へ過去値を注入して既guardを通す案ではない。

旧3pairingを省いた時にnative_pairing_rows_recheckedを四件のまま出さず、実currentとcitedを分ける。過去384行/2304候補相/2316 checkpoint/3 invocationを、新たなchecked数へ写さない。active manifestを読むことと、その全payload/算術を再導出することも別に記帳する。

F4. 巨大bodyは何に必要か

rolling自身はinstructionの全unsigned bodyに入ったliteral_sha256/coefficients_sha256等を値として使う。参照先の巨大bodyを再帰的に展開してhashを計算する処理ではない。one-row相対target式も、前後target・theta・normalized行から計算できる。row-manifestのreduction_manifest_sha256は別のcommitmentである。

一方、凍結C6の保存row readerはcoefficients.u8の全rank trit、reduction.ordered_reductionsの全列、physical-literalの全physical_factors/外指数/原点を再構成し比較する。この仕事をCURRENT_REDERIVEDに残すなら、全bodyが必要である。旧helperへD/hashだけを渡して省略できるとはしない。source-correction.json/p1-roots.jsonも、その箇所では全file SHA参照だが、別のΓ/数値用途があればactiveに戻る。

初期H2では、独立全変換と具体採用命題が閉じた古い意味比較だけをACCEPTED_CITEDへ移す。Γ/typed operand DAGが要求する旧bodyが未確定なら、そのbodyを残す。H3の新codecは採用しない。元97＋後続384の零/重複/順序、original recordのbytes、辞書context、整数指数を失わず、hash参照だけで元語やsource lower-zeroを新導出しない。

将来の層iではaccepted local jとcandidate c_i(j)を分け、global=1450+Σprior a_i+j、D位置=97+Σprior a_i+j。今の3層が128独立でj=cだった事実を一般化しない。採用0層もsegment/processed文脈を残し、架空row/instruction/Dを形成しない。

F5. 可用性と反例

初回は、別作者の変換P/独立Cが全原物・全変換出力・全復元file/hidden/空dirを比較する。logical occurrenceはnative schema/role/run/artifact/path/位置/辞書で区別する。同content blob共有はlogical原点の同一化ではない。元相対/rolling鎖、語の条件付きΓ、変換同値性、現active保全、cold可用性は別命題にする。

Aは毎回必要cold rawを全EOF/bytes/SHAまで読む強い参照基準。Bは既完全復元票とimmutable世代/全object存在・長さ等を信頼する未採択TCB。Bのmetadataだけでは、同じ長さの異内容を検出できない。世代/resolverが正しく同じ内容を返す仮定を明示し、今回全raw再hashとは記帳しない。世代違い、欠品、評価不能、不正、資源中断をそれぞれ型付きで扱い、未知/取得不能を零や成功にしない。どちらのpolicyも将来の永続可用性を無条件に保証しない。

16件の未実行反例表を保存した。隣接零2段の交換はtarget digest列だけでは拒否できず、元record/order/originと各rollingリンクを要する。同じ行のscalar1二段をscalar2一段へまとめるとsrの整数指数を壊す。candidate≠local、採用0層、foreign root、有限DAGの循環、同content異辞書、最後hだけのコピー、異なる旧λ、cold欠品/同長破損/世代差、空dir欠損、OPEN/旧flagの偽昇格、multi-row誤cast等を通常の将来readerの目的境界へ結んだ。実fixtureや新canaryは作っていない。hashの一般的単射性や、inventory全射によるhidden import排除は主張しない。

F6. 残る公開仕様と費用の射程

公開ABIへ戻す未決は、旧multi-rowの厳密operand型/locator、active Γ/DAGと引用leafの境界、旧三pairingの具体採用条項、全旧target数値式の別adapter、a_i/p_i/部分枝の写像、Bのstorage/resolver採択、current/cited/openと実読取/保全の正確なreport型、独立変換/数学別読の8点である。必要箇所が未決ならactive保持又はOPENとし、実装済みとはしない。

H1共有、H2引用化、H3codecは別変更。旧再読が減る候補であっても、新しい相対式照合義務との合計時間は未測定である。rank長要素の走査をwalltime下限やcap内完走保証へ広げない。包括GHA認可を毎試行の新たなユーザー許可へ狭めず、現v6/全typed受領の追加待ち条件を作らない。

F7. 保存と凍結

新TEMP/task1117の原索引1429553 B/520b3c2d82fa93e6c584da0022328acde7e0bc704a7e84f22d8f8480be9d2d5a、native契約v2 25698 B/730f0651f9377fc340fab9c81516d5c9ba3a83bb2a2659e2c0bed82fb91db1c9、改訂K票16229 B/d8037925c1edcc9300356a4eb3db5cfd1a11471aa7a96adaee8bc198a513463e、body用途票12727 B/820485371273e30ff06be5a6bf48ac839deb62585c5f3d741a367f27385ca114を保存した。v1の将来multi-row必要字段を実直接readと紛れないようv2で分離し、v1も保持した。

reader/戻り値票157027 B/70ccf0cdf2d6f3623d90be4d60004079b6af0e24de7e39c4548bafde14e6b7cd、区分/可用性/反例票24601 B/c472d8abb5090f052c356c794d7a84c6503da8f4c4fe05a5c7df46f1d938ba08、入力17pin票6438 B/a28c8b524a82a6d0e4cc57b2f62026de66cca4594f4ee97da75520e089cea531、自己参照照合40182 B/de852b29be0e8b6a31c08960cc683d9bd5171a540c0fa1c163c4a85ea9510728を含め、final-material-manifest-v1.jsonへ全目録を結ぶ。

source/原票変更0、source/import/AST/compile/数値/自己試験/GHA/Git/network/credential/既process操作0、実親payload大規模再hash0。PowerShell/.NETによる自系source raw/小metadata照合と新設計票作成だけであり、独立数学監査1111を代行しない。

F8. Root限定追補 — current返値と共用helperの用途を分ける

凍結v1の族単位説明では、literal_signs / complete_reduction_coefficients がN08だけへ結ばれ、通常callerの返値消費が不足していた。source不具合ではなく設計索引の精密化である。旧9材料と目録v1は全bytes不変で保持し、追補前の返信も TEMP/task1117/reply-frozen-v1.md（11888 B/f63bd778848285141cf326d7293fe341910deb9420fa3e2440f577061aafd0ba）へ保存した。

新native契約v3（49068 B/e32d66bbdff5a36bd23594509c610b3b32afdc33dac674e3faf64a218d413141）では両helperをN08の歴史reader族からN10/K13へ移した。旧三層readerは該当metadataをinlineで再構成しており、この二つへの直接callはない。新reader票v2（258752 B/3aa0f13cdb06dc9d4a22e6437b805047103c7645b737f9981c7084012cdcc6e0）に、返値全shapeと実通常callerを個別記録した。

| helper | 個別返値と実通常経路 |
|---|---|
| complete_reduction_coefficients、4743–4756行 | state.rank長のuint8 ndarray。零を含む全挿入位置と各非零eventの実row同一性を保持し、3747–3788行のordered_reductions、literal_signs、instruction/reduction hash、coefficients.u8へ渡す。通常callは3747、別の旧fixture内直接callは5113で、今回未実行。 |
| literal_signs、4759–4770行 | 四字段dict。physical_factor_exponentsの全順序付きlistとnormalized_outer_exponentは3754/3755行でliteralへ使う。positive_correction_exponentとnumerical_target_coefficientは返すが、凍結C6内にその返値keyの直接readを認めない。3810–3811行の+sr(theta)と519–524行の数値target差は別経路の実計算であり、この二keyのconsumerとは記録しない。 |
| reduction_payloads / row_source | 前者はpayload dictと四key objects dictを返す。DEPENDENTでも六payloadは形成しtarget/instructionはnull、独立時だけ三payloadを追加。後者は親row8-key又は今回の既採用row6-keyを返す。3950–3954行の通常replayから全phase bytes照合/publicationへ進むため、全係数・全literal・両source variantをcurrent K13に保持する。未形成の第六相を要求する意味ではない。 |

同様の用途混在も限定列挙した。batch_target_parentのexact10-key返値は旧1652/2295/3139行のparents構築と、現3861行のstate.advanceで別に消費する。parent_layer_receiptは13字段＋deepcopy coverage（実認証callerでは五字段）を返し、旧3318–3319行の二層intakeと現2548–2550行の三層intakeへ分ける。過去coverageを今回候補算術の件数へ移さない。ThinAnchorは各methodの返値を分け、旧1450/1578/1706 measure_selectionの引用候補から、現1834 pairingと現BatchReductionStateのrow読取を切り離してactiveに残す。いずれも共用helper全体を削除する根拠にしない。

個別追補は7 helper、実definition/caller/返値参照は60 raw範囲で、全offset/bytes/SHAと実source行を bounded-current-helper-return-audit-v1.json（110749 B/a8eb3d41aa6cdce295b55fe78d8194c73960b35ecad59e02ab52c61663c2ad2a）へ結んだ。native v2→v3の19構造差、reader v1→v2の110構造差も保存した。両新版の保存JSONと意図した型付きobjectの差0、7定義の全pin一致を確認している。

62本すべてのper-helper next-consumer閉包を得たとはしない。残る55本は族の割当のみでOPEN/ACTIVE_KEEP、integer/scalar/JSON/seal/packed等の共通primitiveも代表経路の説明に留め、未列挙のalias・retained TCB・file依存をactive保持する。既K01–K15票は不変、今回の個別化がN10/K13の現用途を優先する。final-material-manifest-v2.jsonを新しい全目録とし、source/数学/自己試験/親/Git/GHA操作0、P private未読、v6追加gate0を継続する。

TASK1117_VERDICT: CONSERVATIVE_ACTIVE_CHAIN_REFINEMENT_COMPLETE; CITATION_AND_CONVERSION_PREMISES_OPEN; NO_IMPLEMENTATION_OR_RUNTIME
