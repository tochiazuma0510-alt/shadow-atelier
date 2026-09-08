# Task1111 返信 — 全証拠を保持する統合案の独立数学監査

F0. 判定は「R1–R4の相対的な意味保存は明示前件付きで採択可、実装契約の精密化が必要、回転／冷保存／性能の採択は別」である。root原案を私が独立に審査した。Opus正本の有効な検問を採るが、その必要十分性・計算量・証拠消失に関する強い主張をそのまま定理としては採らない。1108は固定済みで、v6への変更0。

原案12428/d4a44d47c0ad6e1018aef7b0f782d5f7fb17cc48e909ef7ef2ef528a0ad9b3ac、Opus正本52640/28ab573e716990c6ab7f4d1b8229922586797feca93d287a53bdbc8a4b77bfb6を全文読了。2225・2227・2228・2229のsnapshot／速達、2224速達、指定されたCV-9正本§7・限定7条／裁定末尾、reply163 F8.169を読んだ。1113/1114は指示書だけで範囲を確認し、相手の私的設計票・返信・P/C本文は読んでいない。読取範囲／pin票は %TEMP%/shadow-atelier-audit163/task1111/reading-and-independence-scope-v1.json =4720/903e234909304dc0caae4103346154e7cbde4dc4396a1704ec6350413fcaced0。以下の反例は紙上の例で、プログラム・数学計算を実行していない。

F1. R2の十分条件と、その証明の方向。

命題P（相対的意味保存）。元の受理済み入力について、固定したF3空間E、基底順、physical map、各native文法／語演算／符号規約と、元97祖先および各行の由来に関する採択済み前提をΓとする。次の前件を満たす変換を考える。(a) 全行・全順序・元資料の全bytesを、F2の型付き文脈写像で一致させる。(b) 語の導出依存は有限・整礎なDAGで、写像は型、構成子、順序付き引数と重複出現、整数指数、native環境を保つ。(c) 元の各逐次target式・元rolling各リンク・層間接続を保持し、完成状態と指定終端の役割を一致させる。(d) R2(v)の全保存対象と認証範囲を変えない。するとΓの下で、旧新の順序付き行、literal導出の意味、相対target履歴、最新状態／λ／terminalは同じである。元の未知前件は未知のままであり、Γの真実性を変換が新たに証明するわけではない。

証明。葉は同一の型・bytes・Γ内の解釈に到達する。有限DAGの高さに関する帰納法で、各構成子の順序付き引数と指数が同じなので、その語・作用・physical rowの意味が一致する。同じ順序付き行を同じ消去規則で読む限り、その行参照・lead・spanも一致する。各jについて公刊規約 t_(j+1)=t_j−θ_j q_j が前件であり、変形して足すと t_B=t_S+Σ_j θ_j q_j。これは逐次式の弱い系であり、総和から順序・零記録・途中状態を逆に復元したのではない。λと行／targetのbytesが同じなら既存pairing命題も保持される。新λの実照合を省く結論は出ない。positiveの場合もt_S=0と既存祖先の相対命題までである。∎

原R2(ii)(iii)(v)を「全原入力とのtyped解決・全原辞書／前後pin／命令の保持」と読むなら、instructionを変えて再sealしheadだけ写す例はその前件を破る。(iv)単独の弱い読みに対する反例を、原R2全体の反例とは判定しない。同様に原案は各式から総和を導き、総和だけの確認を明示禁止しているので、Opusの「論証の向きが逆」という評価には同意しない。ただし原案は実行可能な受理器仕様ではない。Γ・有限DAG・全リンク再計算・各索引・全consumerを曖昧なまま実装へ渡すことは不可で、F2–F4を公開契約として明記する。

| 攻撃 | 独立判定・具体的な破綻 |
|---|---|
| spanだけ同じ | 不可。例えばqを2qへ変えるとF3のspanは同じでも単位lead・行bytes・正規化と語の係数が変わる。行の順列でも元の順序付き認証対象は変わる。 |
| 異層local0の同一視 | 不可。各層のlocal0は別origin／native root／採用区間に属する。physical payloadが偶然同じでもlogical occurrenceと由来は同一にならない。 |
| 元97を10-keyへcast | 不可。32件5-key＋65件6-keyの元文法・値・順序・rawを失う。存在しなかった前後digest等を補うことも不可。 |
| θ=0記録を削除 | 不可。Σθqと両端targetは不変でもDの長さ／順序／由来／命令列が変わる。記録数・record-wise照合が必要。 |
| target signを反転 | 不可。q≠0、θ=1ならt−qとt+qは一般に異なる。F3の減法規約を整数指数の規約へ無断で移さない。 |
| 古いλで新λ検査を代用 | 不可。旧行e1を殺すλ=(0,1)でも新行e2は殺さない。新λに対する全R行と指定targetの実照合は別命題。 |
| sealだけ残して閉包を切断 | 原R2では不可。digest単独は語・演算・元資料を解決するpayloadでも、採択済み命題そのものでもない。引用化は別scope。 |
| hidden history import | 不可。全inventoryとνが正しくても、保持された旧.pyを現resolverが実行することは防げない。実行closure／data-only readerの独立条件が要る。 |
| positive→MEMBER | 不可。商空間内t=0は、未了のsame-word／lower-zero／positive readoutや元targetの前件を満たしたことではない。 |
| 同じ行の段を併合 | 不可。sr(1)+sr(1)=2だがsr(2)=−1。自由群のx²とx^(-1)は一般に異なり、F3で同じ係数でも元語は同じにならない。 |
| 語因子の順序置換 | 不可。一般にxy≠yx。DAGの辺集合だけでなく、引数の順序と重複出現を保つ。 |

F2. 型付き解決・rolling・全証拠の具体境界。

F2.a 三索引と元の層を残す。層iの実採用数をa_i、実処理候補数をp_i、採用local jに対応する元candidate ordinalをc_i(j)とする。o_1=0、o_(i+1)=o_i+a_i、global row=1450+o_i+j、D内位置=97+o_i+j。c_iは実採用候補列から得る順序保存単射であり、jとの恒等写像を仮定しない。A=Σa_i、R=1450+A、generation=8155+A、|D|=97+Aは元状態の実遷移とも照合する。既存3層のa_i=128という観測を、将来も128mという規則にしない。完成した採用0層も来歴／選定／終端を持ち得るため、空segmentを勝手に消さない。

segment表はoriginのrun/attempt/head/artifactとwhole pin、native schema、元root文書、o_i/a_i/p_i、rank/gen入出、target入出、元state head入出、lambdaのselection/finalという役割を明示する。各境界を実start/finalへ結び、o・target・hの連結を全数確認する。role名やファイルbasenameだけからcurrent/previousを推定しない。明示表に代わる全情報同等の表現は可能だが、境界情報自体は必要である。

F2.b 文脈を含む解決。参照の論理identityは少なくとも (origin artifact全pin, native schema/type, native root, 元relative path, field/row occurrence) である。νはこのlogical occurrenceと新sliceの対応を全数検査する。各元pathの解決と新path/sliceの解決が同じ型・全bytes・値へ到達する可換性を、元側と新側の独立readerから確認する。sliceは普通整数offset/length、範囲内・EOF・12096 B/packed3・不正trit拒否まで閉じる。順序付き行への対応は全単射、物理blobの共有は多対一でもよいが、論理namespace／path／明示directoryを併合しない。旧OS上のdirectory不変を、仮想目録で同じflagとして代用する設計は別途公開が必要。

保持native文書のowner/source/start/selection-start等は元のrootに束縛する。foreign-bindingとはその元文脈を許す明示tagであって、任意のroot hashを許す例外ではない。元schema・canonical規約・ordinary整数とsigned整数・packed encoding・generator辞書・physical basis・算術資産／runtimeとTCBを文脈へ結ぶ。同じraw JSONでも外部generator辞書が違えば同じ語とは限らない。原文を現在schemaへ改名したり、同値JSONとして再整形することはR1外である。

F2.c 有限DAGの前件。数学的な導出依存グラフと、輸送manifestの参照グラフを区別する。前者は葉まで有限に到達し、同じtyped constructor・順序付き子・指数を保つ必要がある。例えばw=w·xという自己参照を双方へコピーしても、graph同型だけから有限語の意味は出ない。未解決参照、型循環、循環をvisitedだけで成功扱いするreader、contextを無視したhash-only memoを拒否する。正当な共有DAGの再訪は許すが、循環検出と混同しない。source/transportの参照が循環する場合にもそれを語の帰納法の前件に流用せず、独立に根拠付けられたnative hash契約を要する。core自身のwhole SHAによる自己根拠付けは禁止し、外側C結果／GHA束縛はcore後に置く。

F2.d 鎖。元各rolling familyのschema、predecessor、除外字段、canonical body、元root bindingを固定し、各リンクのbodyを実資料から再計算する。各中間hを元の登録列と結び、最後だけコピーして通さない。統合wrapperのsealを元physical hに置換せず、変換そのものによる架空の1リンクも足さない。途中targetは後退 t_j=t_(j+1)+θ_jq_j で全数再構成して各parent/remainder digestへ接続することを、新受理器の十分な検問として採る。これは両端だけの旧読みより強い検査になり得るが、原R2の相対意味保存が論理的にそれなしでは偽ということではない。

θ=0の隣接2段ではすべてのtargetが同じなので、I2'のtarget digest列だけはその2記録の入替えを検出しない。rollingも有限長hashの一般的単射性を証明するものではなく、順序固定の数学的前件は元のrecord-wise順序・origin/index対応・全body identityである。全リンク比較はそれを実認証する検問として使う。元pin認証の信頼モデルを超えて「hashは完全に順序を固定する」とは言わない。

F2.e 全closure。R2(v)で登録した元ordinary file/dir、witness／literal／reduction／target／manifest／root文書、source/runtime/fixture/checkpoint/telemetry/診断/receiptと来歴の全対象を列挙する。数学語の閉包だけでなく、保全命題を支える運用証拠も含む。同じfileが複数用途なら併記する。typedに読んでいたものをhash-onlyへ替えること、payloadをcold pinに替えることは同じ受理器の保持ではない。全payloadを新bundle内へ再配置して必要な元資料を自己完結に読むR3と、1113/1114の過去命題引用化を混ぜない。

F3. OpusのN1–N7／ρ検問への独立判定。

Σ（順序付き行／target／D／h／λ／origin等の対象）と、今回実際に再導出するVを区別する指摘は採る。ただしΦが何を観測するreaderか未固定のまま、N1–N7をΦ旧=Φ新の必要十分条件とはしない。例えば途中bodyを検査しないreaderは同じΣを返せてもN4を満たさないし、Σを変えない非荷重telemetryの欠落は全保存を変える。逆に実読取り全量をΦに含めるなら、新wrapper/path/receipt自体は旧入力と同じbytesではない。比較対象への明示射影πを定義して π_new Φ_new = π_old Φ_old と書き、その射影から除くものを別のV／保全契約へ記帳する必要がある。

| N | 採る内容と必要な精密化 |
|---|---|
| N1 | 順序付き行identityと検査可能なνを採る。blob共有とlogical occurrenceの全単射を分ける。 |
| N2 | 元97／零係数／record-wise順序保持を採る。97+128mを97+Σa_iへ一般化。 |
| N3 | 両端・逐次target・層境界を採る。digest連結だけを数値更新や完全な順序証明とはしない。 |
| N4 | 全native rollingリンクの実再計算、foreign root、最新元hを採る。Σ一致そのものの必要条件と、今回の再計算義務を分ける。 |
| N5 | 完成状態／current/previous／λ役割を採る。nonzero・positive・未完成の枝を区別する。 |
| N6 | typed解決・独立に照合できるνを採る。native環境と有限operand DAGを追加し、裸raw一致だけで語の意味を決めない。 |
| N7 | 原R2では全登録保全の写像。荷重閉包だけへの縮小やTier B/C化は別scope。surjectionだけでhidden importは排除されない。 |

Vは単なる真な命題名集合にせず、(命題, 入力scope, native文脈, 証拠依存, CURRENT_REDERIVED／ACCEPTED_CITED／OPEN_PREMISE) という札を持たせる。V_new⊇V_oldを今回の再導出として要求するなら、νで運んだ旧検査の入力・前件・範囲まで含めて保持する。引用された同じ命題をCURRENT_REDERIVEDへ改名して包含を作らない。より強い十分検査が旧検査を論理的に含意する場合はその含意を示せばよく、同じアルゴリズムや同じ回数の実行が数学的必要条件なのではない。

| ρ | 独立判断 |
|---|---|
| ρ-1 | 元prefix97と全record保持を採る。長さは97+A。 |
| ρ-2 | exact10-key、ordinary trit／hash／native役割を採る。candidate ordinal=accepted localを将来の一般条件にしない。 |
| ρ-3 | segmentの実a_i、元target/h境界、rank/genを全数接続。固定128は受理済み各旧層の実観測だけ。 |
| ρ-4 | 全digest鎖を採るが、零更新の順序や数値内容をこれだけで認証しない。 |
| ρ-5 | 全中間targetの再導出を新検問として採る。費用は固定次元ならO(A)のベクトル更新だが、全資料parse/hash費用までO(R)とはしない。 |
| ρ-6 | 基点／終端の実packed3 bytesと型を固定。元97に架空の中間digestを足さない。 |
| ρ-7 | D→元row-manifest→physical rowの全対応を採る。D自体に無いphysical hashを推測しない。 |
| ρ-8 | instruction全body・元root・全native linkを採る。row bytes＋祖先台帳だけではrollingを再計算できない。 |
| ρ-9 | θの0/1/2件数は実値を公開。各値の非零件数を未来の数学的必要条件や目標quotaにしない。 |
| ρ-10 | targetの+sr(θ)、消去の−sr係数、outerの+sr(σ)をnative型別に保持。全因子順・重複・元整数指数も必要。 |
| ρ-11 | 元run/attempt/head/artifact/source/判定の束縛を採る。pinはpayloadや当該命題の採択履歴を代替しない。 |
| ρ-12 | DERIVEDとoriginal_rho2_directly_read=false、元packed pin・限定を保持。 |
| ρ-13 | logical νの全単射／順序／resolve可換を元側から独立照合。 |
| ρ-14 | nonzero終端では最新λを全R行と指定二targetで実照合。positiveのλ=nullにλ·t=1を強制しない。新λと異なる旧λの命題は別。 |

Opus命題2の数値部分は、元基点と各rowの由来をΓに置き、必要な行／target／instruction／manifestをすべて持つ場合の相対target鎖の再導出として採る。元の語／ρ2そのものを新たに直接計算したという主張は出ない。他方、完全なliteral／witness／演算環境を持てば、それを独立評価すること自体が数学的に不可能とも言えない。費用や今回未実施であることと、再導出不能を区別する。Opus§5.3の「行bytesと祖先台帳だけでrolling等すべて」を字義どおりには採らない。命題2自身が要求するinstruction等が欠けている。

またR3の自己完結性から、元資料／m個の証言が必然的に消えるとはしない。全native bytes・元seal／root束縛と出所を内部へコピーして再認証する構成は可能であり、原R1–R4はそれを要求している。一回の変換票だけを信頼して以後は元照合を行わないなら、新TCB／引用化を明示する。別runの再確認を、同じコード・共有kernel・同じ前提を越えたm系統の独立性とも数えない。

F4. 実装委嘱前に固定すべき公開契約。

必要なのは、core／origin／segment／row-slice／logical file/dir／typed resolver環境／各native rolling family／target-chain／状態・終端／変換照合票／実行closure／V差分／資源停止のexact schemaと参照表である。各consumerを root→file→schema→field/type→戻り値→次consumer へ全数接続し、同じraw helperも変わるglobal・文脈を照合する。元bytesと新sliceを独立に読むCはPの変換表を正しいものとして先に信用しない。P/Cは公開schema・符号・固定元pin・対象範囲だけを共有し、private parser／resolver／算術helper／fixtureを共有しない。共通kernelが必要ならTCBと実際の独立性限界を登録する。

fixtureは最初に全契約を通る正例を保存する。少なくとも複数層local0、元97 mixed shape、零θ、candidate途中のDEPENDENTによる索引ずれ、採用0層、nonzero／positive／未完成、同content別context、正当な共有DAGを含める。現実の元pinとの初回全比較と、小さな合成fixtureの数学目的を分ける。以下は未実行の事前登録義務であり、件数を揃えただけで被覆済みとはしない。

| 単一変異／対照 | 到達させる通常拒否条件 |
|---|---|
| 順序置換・θ0削除 | record/order/長さとchain。target総和だけは通る対照を含める。零2段ではtarget digest列も通り得る。 |
| local0衝突・candidate/accepted混同・a_i欠落 | native occurrence／segment全単射・正しい三索引。 |
| 元97のcast・scalar float/bool・指数2と−1の同一視 | exact native型とsigned語規約。 |
| instruction再seal／中間h破壊／wrapperをanchor化 | 元body／foreign root／各rollingリンク／元terminal h。 |
| 同じrowの段併合・因子順序交換 | 逐語constructor・指数・順序・重複。F3総和一致を成功条件にしない。 |
| offset重複／末尾1 byte欠損／不正trit | slice全範囲・packed3・EOF・元全bytes。 |
| foreign root差替え・同blobを異なる辞書で解釈 | context-qualified resolverと公刊演算環境。 |
| 循環／未解決参照／空dir欠損／path二重割当 | 有限整礎性・全closure・ordinary file/dir写像。 |
| cold pinだけ／旧sourceのimport／DERIVEDやpositiveの昇格 | V scope／実行closure／終端と前提札。 |
| 旧λの結果を最新λへ改名 | 実λ bytes／全行prefix／target／native入力の束縛。 |

陰性をhash・seal不一致で早期拒否しただけなら、その後の意味条件へ到達した実証とは記さない。目的の型／演算／リンクまで到達させる合成入力は事前登録したfixture namespace内で整合的に構成し、通常helperを呼ぶ。必要な外側sealを更新しても、原origin照合を無効化するtest-only例外は導入しない。保存するのは正例・変異・全raw・expected label・実caught reason・実到達範囲であり、原物pinの拒否対照と意味拒否対照は別に採点する。

F5. 省ける仕事、裁定範囲、未決事項。

15基点＋統合親1は通常の役割数／入口を16にする提案であって、証拠量・rank・祖先長・旧命題数を一定にするものではない。R3は全資料を保持する統合であり、最古証拠の切落としではない。旧prefixを同じ文脈で何度も解決する部分は一回へまとめ得るが、元層ごとの固有資料・異なる照合命題は残る。内容アドレス共有は同blobの物理読取りを減らせても、異文脈の意味解釈を同一化してはならない。

特にnative pairingは、同じ (λ bytes, 順序付きrow prefix, 指定target, E/native型) の同一問合せだけが重複である。最新λが全R行を殺しても、異なる歴史λ_iが各旧prefixを殺す命題はそこから導けない。V_new⊇V_oldを今回の実再導出として要求するなら、各異なる旧問合せを保持するか、それを含意する別の実計算を示す必要がある。引用へ替えるならACCEPTED_CITEDに移す。従ってOpusのΣ_i R_i→R、D_i/E_i/F_i消滅は、単なる役割統合の一般的帰結としては採択しない。native文脈や復元／保全の仕事も、その対応する義務を残した上でどこを省くかを示す。

費用はR／L／M／実p,kに依存する。固定次元でのtarget後退更新はO(A)、最新λの全行pairingはO(R)相当のデータを扱う一方、全instruction／reductionのparse・canonical hashはその全量Mにも依存する。全証拠を毎run認証する条件なら増えるMの仕事は残る。公刊source読解に基づくrank長factor/reduction列は、該当する要素生成／走査についてΘ(Σ_candidate R_j)、全runについて少なくともΩ(Σ R_j)という2228の射程で採る。私はP/C私的sourceを読み直してこのコード事実を再実測したとはしない。全walltimeのΘ(kR)、有限rankでのcap超過、1695秒の将来一定性、他方式不可能性／唯一の手段は未証明。固定有限宇宙の秒数を漸近記号から決定しない。

公開計器はP/C別、phase/native context別に unique logical occurrence／unique blob／unique query と total visits、bytes hashed／typed bytes／files／directories、row/target/pairing数、ordered reduction/factor要素数、cache hit/miss、pack/index/復元費用、実elapsedとmissing/UNKNOWNを分ける。inclusive区間は加算しない。2229のwhole-file重複集計は登録宇宙内の保存量に対する根拠であり、chunk重複・parse仕事・同一prefix再訪・walltimeの機構を否定または同定しない。今後もk／R／親数／版が同時に変わる一標本から原因や成功run数を確定しない。

最終裁定。R1–R4はF1のΓとF2の明示前件の下で相対的意味保存の基礎案として採択可。未来の実装／具体親変更／性能最適化は未採択で、F2–F4の契約と独立照合が必要。1113/1114の冷保存は2227–2229で認可された別設計であり、本票はその実案を監査・承認していない。CURRENT_REDERIVED／ACCEPTED_CITED／OPEN_PREMISEの三分と変更TCBを隠さないことだけを共通条件とする。

基準として採用済みなのはrun34161493396/1、head a5b456a973f8a917f3af386d327061a02a0cf900、rank1834/gen8539、cross-checked限定7条である。初回変換を旧17親段階から行うか、今後受理されるv6の18親段階から行うか、吸収する最新packetの位置／全origin集合／実a／各pinは別に固定する。v6の全128採用や1962を仮定せず、rankは旧新を合算しない。k425・約110run・A0成立の約束をせず、k/caps変更も本票では認可しない。v6 18親/k128/同capsと1108 immutable v2は不変。新source/GHA/数学/AST/import/compile/selftest実行0、Git/network/credential0、新agent0、実root/process操作0、verified=false。A0 actual0/1・階段1/6・grade2両NOT_DECIDEDの格付けを変えない。

AUDIT_1111_VERDICT: CONDITIONAL_EQUIVALENCE_ACCEPTABLE_EXPLICIT_CONTRACT_REFINEMENTS_REQUIRED_IMPLEMENTATION_AND_COST_UNPROVEN
