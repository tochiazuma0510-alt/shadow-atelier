# Task982 — 同じordered rootのtarget履歴とnormalized pair

Task982、reply974、reply958、reply975を全文読了し、保存target履歴から一つのordered語と同rootのnormalized pairを読むA/B/C consumerを完成した。変更は本返信と `search/d972_r07_continuation_positive_word_readout_v1.py` だけ。Task980は別便で完成・root公開済み。旧source/返信/workflowは不変。ローカルPython/import/AST/数値/GAP、network/git/credential、新agent、Task983の新算術読取はない。runtime成功・新terminalは本便では未観測である。

## F1. CLIと全体の型

prefixは `d972.r07.continuation-positive-word.v1`。全JSONとJSONL一行はASCII/ensure_ascii/sort_keys/compact separators/末尾LF。sealed objectは `schema=<prefix>.<kind>` と `sha256=SHA256(canonical(objectからsha256だけ除外))` を持つ。全file hashにはseal字段と末尾LFを含める。下のnodeだけは指定どおり `node_sha256` をseal字段として用いる。

CLIは同じ14親の `--state-root/--delta-root/--seed34-root/--packet-root/--refinement-root/--oracle-root/--e-root/--prepare-root/--block-root`（4回、0..3順）`/--p1-root/--task712-root`、`--continuation-root`、`--rho2-root`、`--acceptance`、別の新 `--output`。`--max-seconds` と `--max-memory-mib` を明示し、`--selftest` は新境界だけを使う。新consumerはresumeしない。入力・出力は相互包含不可、受理HEADまでのread-only処理である。P971.load_prefixを呼ばない。

出力は `target-history.json`（`.target-history`）、`ancestor-index.json`（`.ancestor-index`）、`ordered-word.jsonl`、`word-manifest.json`（`.word-manifest`）、`normalized-pair.json`（`.normalized-pair`）、`manifest.json`（`.manifest`）、`result.json`（`.result`）。source/owner/acceptance/fresh-rho2/contextとliteral dictionaryはmanifestが指す独立receiptに保持する。topの細かい親entry rosterは実loaderの接続時に追記し、未観測成功pinを値として捏造しない。

## F2. exact node ABI — Task983が消費する共通grammar

`ordered-word.jsonl` の各行は**次の六字段だけ**を持つplain objectである。

```json
{"id":0,"type":"F2-word","op":"Identity","args":{},"receipt_refs":[],"node_sha256":"<64hex>"}
```

`id` は0から連続する整数（bool不可）。`type` は常に `F2-word`。`node_sha256` はこのobjectから自身だけを除いたcanonical bytesのSHA256。`receipt_refs` はancestor-index.entriesのidを参照する整数配列で、使用順を保つ。正規化・sort・重複削除で語の使用edgeを消さない。childの共通形は**`{"node":prior_id,"sha256":"そのnode_sha256"}`だけ**で、必ず0≤prior_id<当node.id、型・hash一致を要求する。

| op | argsの正確な字段 / 意味 |
|---|---|
| `Identity` | `{}` |
| `Letter` | `{"letter":t}`、t∈{−2,−1,1,2}の普通整数、bool不可。1=x、2=y、負は逆字 |
| `Rel` | `{"dictionary_sha256":h,"relator_id":s,"letters":[t,...],"letters_sha256":k}`。sはliteral辞書内の文字列ID、tはLetterと同範囲、kはletters配列だけのcanonical bytes SHA。hは束縛済みliteral辞書receipt全file SHA。字列・ID・hashを辞書と全一致させる |
| `Act` | `{"conjugator":child,"word":child,"orientation":"P*W*P^-1"}`。conjugatorも先行word nodeへ解決し、一般の共役を表す |
| `OrderedProduct` | `{"factors":[child,...]}`。配列順の積。空配列も可、因子をsort/collectしない |
| `Inverse` | `{"word":child}`。積全体の逆を表し、flattenする場合は逆順・各逆を伴う |
| `IntegerPower` | `{"word":child,"exponent":n}`。nは普通整数のJSON integer、bool不可。0冪でもchild使用edgeとreceiptを保持。rawの/6修理指数と9乗、sr係数を区別した元receiptを残す |
| `Ref` | `{"namespace":ns,"key":s,"scope_sha256":h,"word":child}`。ns/s/hが指すtyped symbolを、一つの先行nodeへ束縛する。未解決Ref・runtime隠れたtree evaluatorは許さない |

Ref.namespaceは `p1 / old-defect / conn-lower / conn-raw / physical / raw-e / tree / normalizer / target` に限定する。keyは当namespace内の文字列ID、scope_sha256はその親manifestまたは保存receiptの全file SHA。P1/Conn-lower/physicalで整数値が同じでも別symbolである。node自体はF2の同じ語型、literal原点の型はRefとancestor receiptで分離する。

IDの決め方はtarget pivotを挿入順に訪ねる最初のDFS後順。各symbolの依存を保存された順に訪ね、同じ(namespace,key,scope)はmemoizeして一度出す。各literal wordの字列は左から訪ねる。actor pathは最外字を先頭にした入力順、入れ子構成はその順を保つ。Refの先行childを作り終えた時点でRefを一つ発行する。productや0冪の使用edgeはそのままemitする。最終rootは全物理pivotに対するtarget係数の挿入順積で一つだけ。相殺した係数mapをrootの代わりにしない。

srは **`sr(0,1,2)=(0,1,-1)`**。F3係数を普通整数冪へ変える場所は元receiptの当該操作一回だけ。P1内部scale、Vの外alpha、physical全体sigma、target全体係数は別々である。Eへ旧character projectorを加えない。raw epsilon/6は小raw語の普通整数で計算し、omega=2はcentral -1。同じsourceでも+2と同じliteral node/hashとは呼ばない。

## F3. ancestor refsとmanifest/root/hash

ancestor-index.entriesはid順の配列。各entryは **`id,namespace,parent_role,parent_manifest_sha256,file,file_sha256,offset,length,record_sha256,json_pointer`** を持つ。parent_roleはparent rosterにあるartifact/receipt role。fileはそのroot相対POSIX path。file_sha256は全実bytes、offset/lengthはJSONL positioned record等の実範囲で非該当ならnull。JSON pointerがある場合はRFC6901で同じfileの値を指し、そのcanonical bytes SHAをrecord_sha256とする。JSONLだけの場合はoffset/lengthが指定するLF込みの全record bytesをhashする。file全体refはoffset=0/length=file bytes/json_pointer=null/record_sha256=file_sha256。実親identityをOS絶対pathへ置き換えない。

word-manifestは少なくとも `grammar,owner_sha256,source_sha256,context_manifest_sha256,fresh_rho2_manifest_sha256,parent_roster_sha256,accepted_head_sha256,target_history_sha256,ancestor_index_sha256,literal_dictionary_sha256,nodes_file,root_id,root_sha256,character_order,actor_convention,central_representative,coefficient_rule,eof` を持つ。`nodes_file={"file":"ordered-word.jsonl","bytes":N,"sha256":h,"nodes":n}`。grammarは `prior-only-ordered-F2-eight-ops-v1`、character_orderは[0,1,2,3]、actor_conventionは `P*W*P^-1`、central_representativeは `sr(0,1,2)=(0,1,-1)`、coefficient_ruleは `saved-F3-to-signed-integer-once`、eofはtrue。

JSONL全file SHA・root node SHA・各Eのraw word_stream SHAは別物。raw streamsは元raw-word receiptの参照とそのencoding/letters/bytes/sha256/eofを別配列に保持し、node/root hashで置き換えない。全used edge・input receipt closure・literal dependency closureをancestor-indexとword-manifestへ束ねる。Task983は当root/manifestとCの同root normalized receiptを受ける。

normalized-pair receiptは `word_manifest_sha256,same_root_id,same_root_sha256,modulus:54,residue_type:"integer-residue-0-to-53",exponent_residues:[r0,r1],divisible18:[b0,b1],normalized_pair:[n0,n1]またはnull,eof:true` を持つ。rは普通整数0..53、bool不可。各座標r∈{0,18,36}を18整除とし、両整除なら普通整数商r/18をF3値として読む。Bと同じrootで全nodeの再帰を行う。P1/physical全語の巨大な普通整数そのものを出力したとの主張はしない。

最終結果の適用は、非零residualならNOT_APPLICABLE、linear target零でもD・normalized/side/localizationの不足はcandidateのまま。GRADE2 MEMBER/full A0をこのA/B/Cだけで出さない。資源停止はUNKNOWN_RESOURCE、不正はFAIL、部分PASSを作らない。新canaryの正確な群とparent/acceptance/top rosterは実装blockに伴い追記する。

positioned範囲はJSONL命令に加え、typed binary rowにも使う。`.jsonl`の範囲だけcanonical一行/LFを要し、`.bin/.u32`の範囲はbinary bytesのSHAである。physical rowは12096 bytesでbaseだけpivot_id×12096、個別deltaはoffset0。P1 cacheはnode×36288、treeのu32LE要素はindex×4。binaryをJSONへparseしない。JSON pointerとoffset/lengthは排他的で、nested Conn sourceはpositioned whole JSONL record内の保存recipeとして読む。

## F4. 入口receiptの公開追加（値はrootの実観測後）

`--continuation-root` は `output/HEAD` と `checker-result.json` を含むcandidate artifact root、`--rho2-root` は `task640-payload/manifest.json` を含むfresh-rho2 artifact rootを指す。14旧親も各CLIが示すpayload rootであり、artifact内部に包みdirectoryがある場合はworkflow側で一意に解決してから渡す。consumerが同名のlatest/candidateを探索して入れ替えない。

`--acceptance` はrootが実回収・認証後に作るsealed `.acceptance` objectである。必須字段は `schema,sha256,status,parents,selected,consumer_sources,runtime,candidate,cross_checked,verified`。status=PASS、candidate=true/cross_checked=false/verified=falseを保持する。まだ成功artifact pinを埋めた実ファイルは本便から作らない。

parentsは次の16roleの順序付き配列: `state,delta,seed34,packet,refinement,oracle,e,prepare,block-0,block-1,block-2,block-3,p1,task712,continuation,rho2`。各itemは `role,artifact,manifest,files,directories`。artifactは `run,attempt,head,id,name,bytes,sha256,workflow,repository_id,conclusion` のexact tuple（sha256は`sha256:`付き）。Task554のprepare/四blockだけconclusion=failure、他はsuccess。旧14とfresh-rho2は受理済みの固定tupleへjoinし、continuationだけ実成功candidateで更新できる。manifestは当rootの主receiptを指す `{file,bytes,sha256}`、filesは全regular fileの相対POSIX `{file,bytes,sha256}` をfile名順にした配列、directoriesは全相対directory名順配列。hiddenも含め、全bytes/rosterを入場時と終了時に比較する。

selectedは `head,result,checker,owner,source,start,fixed` の七 `{file,bytes,sha256}`（同continuation root基準）と、`completed_steps,rank,generation,kind,state_head,target_remainder_sha256,lambda_sha256,terminal`。実Cの全prefix PASS・全scope/HEAD/result結合を要求する。consumer_sourcesは `producer,checker` の二 `{file,bytes,sha256}`（repo root基準）、runtimeは `{python,numpy}` の実全文。新982/983 sourceと実runtimeを認証し、C983のsourceはhashだけで扱い、producerがその算術をimportしない。

source/owner/parent/fresh/context/literal補助receiptのfile名は `source.json,owner.json,parent-roster.json,fresh-rho2.json,context.json,literal-dictionary.json` に固定する。literal-dictionaryは `.literal-dictionary`、字段 `relators` は `{文字列ID: signed-letter配列}` の辞書とし、44 seedは `r:1`..`r:44`、19 raw Q0語は `q:1`..`q:19`、pure conjugatorは `pure:0`..`pure:3`、二normalizerは `normalizer:r_x/normalizer:r_y`。元file/pointer/hashと既存r_x/r_yのcanonical word hashを別字段に保持する。Relが読む字列はこの表と全一致する。pure/normalizerの表記はliteral dictionary IDであり、44-relator正常閉包の葉と同じ数学的役割を主張しない。

source初期block（326行）はstdlibのみのresource/hash/型・八op exact args/prior child/seal・同word mod54 fold・streamed WordDAGまで保存済み。v478全文、v547全文、v548全文、2144のsigned訂正も読了し、現gradeのPB4-dropped型と全11slot保持の境界を継承した。

## F5. Refを保存recipeへ結ぶexact規則

Task712 CLI rootは `r07-grade2-maps-v4/` と `r07-grade2-maps-v4-receipt.json`、`r07-grade2-maps-v4-checker.json` を同時に含むenvelope rootとする。16 roleのfiles/dirsは各CLI rootの全体であり、親aliasからその外のreceiptへ出ない。

materializerのbare-seed番号sは0-basedで `Rel r:(s+1)`、`packet/relations.seeds[s].seed=s`。P1 projected_seed.origin.seedだけが1-basedの `Rel r:seed` であり、prepareの旧seed_reductionsはseed−1で読む。compact_wordの実全字列/hashを対応辞書へ結び、この二つのindex規則を混同しない。

下表のdecimalは先頭零なしの非負整数文字列、snapshotだけは6桁ゼロ詰め。scopeは列に示す実manifestまたは保存receiptの全file hashである。Ref.args.wordは表の**順序付き構文そのもの**へ結ぶ。単にnamespace/key/scopeが存在するだけでは合格にしない。表の因子は係数0・同じchildの重複使用も保持する。全F3→整数変換はsr、`-sr(q)`と`sr(sigma)`を別に適用する。

| namespace / key / scope | 元recordとargs.wordの構文 |
|---|---|
| `p1` / global node decimal / P1 `manifest.json` | positioned `instructions.jsonl`のnode。所属Task554 blockの同じorigin/reductions/scaleへ一致。`Power(Product([origin-word, Power(prior W,-sr(q))…]),sr(scale))`。old originのseedは同じcharacter projector、actorは`Act(Letter(t),parent W)`。new defect originはprepareのdefect IDの語を新characterでprojectしてから所属blockのlocal reductionsを引く |
| `old-defect` / prepare.defect_originsのid decimal / prepare body file | `/defect_origins/id` と該当 `/old_blocks/owner/record/seed_reductions/seed-1` または `/actor_transitions/pivot/actor-slot`。seedはprojected seed、actorは`Act(Letter(t),W_old)`を先頭にし、記録されたold reductionを負のsrで順に続ける。whole defectに新projectorを掛ける操作はp1側 |
| `conn-lower` / lower pivot挿入ID decimal / base `state/manifest.json` | base `state/instructions.jsonl`のnested `/source`、kind=pivot。`Power(Product([W_source_node, Power(earlier lower,-sr(q))…]),sr(sigma))`。JSONL全recordをpositioned receiptに保持し、nested pointer `/source` の内容も元recordから照合 |
| `conn-raw` / offer decimal / base `state/manifest.json` | nested Conn kind=connection。`Product([W_source_node, Power(earlier lower,-sr(q))…])`、outer sigmaなし。outer kind=skippedのlower recordも捨てない |
| `physical` / global pivot decimal / baseは`state/manifest.json`、後続は各`instruction.json` | baseの先頭は同offerのconn-raw。後続の先頭は対応したlegacy raw materializationまたはEのV。続いてinstructionのphysical reductionsを保存順に`Power(prior physical,-sr(scalar))`、全productを`Power(…,sr(sigma))`。instruction/row/targetのartifact-relative recipe refsはAのpivot表に正確な位置を保存 |
| `raw-e` / `external-e/<raw node id>` または `loop/<snapshot:06d>/<raw node id>` / 当該`raw-word.json` | `/nodes/index` のid/op/argsを保存順に再構成。元Identity/Letter/Inverse/IntegerPower/OrderedProductは同じopと整数/child順。元Refのtreeとnormalizerだけ下の既定Refへ解決する。raw-root以外の使用nodeも同じraw file scopeへ束縛 |
| `tree` / vertex decimal / 外部Eはoracle geometry `manifest.json`、loopは`fixed/manifest.json` | 同じparent/parent-edge/next-posの実u32LE payload。vertex0はIdentity、それ以外は`Product([Ref(tree,parent[v]),Letter(parent_edge[v]%2+1)])`。parent-edgeは親からvへのpositive edge ID `2*parent[v]+slot`、next-posの一致を要求する。root sentinelだけ0xffffffff |
| `normalizer` / `r_x` または `r_y` / 新literal-dictionary.json | 同じID `normalizer:r_x/r_y`のRel nodeを唯一のchildにする。辞書はv459の19 Q0語から指定順に作ったfreely-reduced固定word、その既存hashと全字列を束縛。raw-word.normalizersの実receiptも各raw使用箇所に残す |
| `target` / accepted HEAD全file SHA文字列 / 同じHEAD全file SHA | `Product([Power(physical0,sr(target_scalar0)),…])`をglobal pivot挿入順に作る。HEADまでの全pivot数だけで、最後のrootはこのRef一つ。全target-delta refsとAの同HEAD/係数列に一致 |

旧projectorの構文はcharacterごとのparity順 `(0,0),(0,1),(1,0),(1,1)` の `Product([Power(Act(Rel(pure:k),word),(-1)^(character·parity))…])`。旧full-origin actor rawは `Act(Letter(t),W_i)` を先頭に、`materialization.relation.raw_events` のsigned coefficientを引いた後でwhole-character projectorを掛ける。bare-seed materializationも元のordered raw eventsから作る。final_coefficientsやP1 node sortをliteralの順序に使わない。EのVだけはraw-rootの後に `p1-reductions.events` / `source-correction.p1_factors` の同順因子を置き、character projectorを挿入しない。

各recipeで指定したrecordはancestor-indexのwhole-file/positioned/JSON-pointer refsへ結ぶ。derived outputのnormalizer scopeを除く全scopeは16親の保存fileに実在する。normalizer scopeのliteral-dictionaryはsource.jsonのraw dictionary実bytesとparent raw-wordのnormalizer receiptへ結ぶ。source-fileを16親の隠れた17番目artifactにしない。

## F6. 全13fileとtop metadataのexact契約

成功outputは次の13 fileだけである。全JSONはF1のsealを持ち、JSONLだけF2のnode sealを使う。

```text
ancestor-index.json
context.json
fresh-rho2.json
literal-dictionary.json
manifest.json
normalized-pair.json
ordered-word.jsonl
owner.json
parent-roster.json
result.json
source.json
target-history.json
word-manifest.json
```

各16親のacceptance.manifestのfileを固定する。`state=state/manifest.json; delta/seed34/oracle/e=output/manifest.json; packet/refinement/continuation=output/HEAD; prepare=prepare.<bodySHA>.json; block-k=block-k.<bodySHA>.json; p1=manifest.json; task712=r07-grade2-maps-v4/manifest.json; rho2=task640-payload/manifest.json`。ancestor.parent_manifest_sha256はこの主receiptの全file hashであり、Task554ではbody hashになる。別のHEADも全roster内でbodyとjoinする。

p1 namespaceのpositioned binaryには、Task554 prepareの `old_blocks[owner].lower_basis_blob` の1514 B/row、`lifted_grade_blob` の18144 B/row、新blockの `basis_blob` の4536 B/rowも含む。実descriptorのrole/file/full bytes/SHA/rowsとlocal×widthに制限し、Eの元lead eventのrow/companion SHAへ結ぶ。任意bin/幅を許さない。

以下の字段列はschema/sha256を除く全字段。特記したnormalized-pair以外のreceiptはcandidate=true/cross_checked=false/verified=falseを持つ。この三字段もexact rosterの一部である。

- `parent-roster`: acceptance_sha256, parents（acceptanceの16 itemをそのまま）, all_files_and_directories_authenticated=true。
- `source`: acceptance_sha256, consumer_sources（acceptanceのproducer/checker）, raw_sources（下記3 pinの順）, runtime（acceptanceの全文）, accepted_continuation_source_sha256（selected.source全file hash）, arithmetic_imports=[], old_numerical_replay=false。
- `owner`: acceptance_sha256, accepted_owner_sha256, accepted_source_sha256, accepted_head_sha256（いずれもselectedの全file hash）, parent_roster_sha256, source_sha256（新receipt全file hash）, scope。
- `fresh-rho2`: artifact（固定tuple全字段）, files（固定7 entryの順）, manifest_sha256, packed_sha256, manifest（実task640-payload/manifest.json全文object）, verdict（実task640-verdict.json全文object）, direct_payload_parent=true, derived_target_identity_used_as_direct_bytes=false。
- `context`: accepted_owner_sha256, accepted_source_sha256, fresh_rho2_manifest_sha256（元fresh manifest hash）, task712_manifest_sha256, p1_manifest_sha256, prepare_body_sha256, block_body_sha256（0..3順）, canonical_index_sha256（continuation output/fixed/canonical-index.json全hash）, scope, aggregation="printed-v478-(2.7)-PB4-dropped", same_word_all_occurrences_required=true。
- `literal-dictionary`: relators（F4 exact ID辞書）, raw_sources, paper_relators_pointer="/relators", normalizer_relators_pointer="/raw_q0_relators", normalizer_raw_roster_sha256_without_LF, normalizer_words（r_x/r_y/c_x/c_y順の {name,length,word_sha256_without_LF}）, normalizer_recipe={"r_x":"free(q1*q6^-2*q7^4*q9)","r_y":"free(q8^-1*q4^-1)"}, pure_order=[[0,0],[0,1],[1,0],[1,1]], central_representative="sr(0,1,2)=(0,1,-1)", relator_normal_closure_claim=false, eof=true。このobjectだけはassurance三字段を持たない。
- `ancestor-index`: parent_roster_sha256, owner_sha256, source_sha256, entries（F3 exact entry）, eof=true。このobjectもassurance三字段を持たない。

source/literalのraw_sourcesは `scratchpad/a0_paper_words_v1.json`, `scratchpad/a0_v2_words.json`, `scratchpad/fuda1_a0_rmax_data.g` の順、各itemは {file,bytes,sha256}。固定7 fresh filesは manifest、verdict、rho2.bin、rho2-dense.bin、lower-dense.bin、target-dense.bin、authenticated-roots.jsonの順（F4のrho2 role内の実相対path）。

scopeは次のplain exact objectである。

```json
{"source_lower_trits":96776,"physical_lower_trits":32260,"physical_top_trits":48384,"p1_rows":8059,"character_order":[0,1,2,3],"unique_occurrences":10,"occurrence_order":[0,1,2,3,0,4,5,6,7,8,9],"current_grade":"v478-(2.7)-PB4-dropped","word_group":"F2","actor_convention":"P*W*P^-1","normalized_modulus":54,"grade2_member":"NOT_DECIDED","grade2_nonmember":"NOT_DECIDED","full_A0":false}
```

target-historyの全字段は accepted_head_sha256, accepted_result_sha256, accepted_checker_sha256, completed_steps, rank, generation, state_head, kind, terminal（採用continuation terminal）, pivots, base_offers, lower_pivot_offers, target_scalars, residual, original_rho2_packed_sha256, target_derivation_mode="DERIVED_FROM_ACCEPTED_NUMERICAL_PARENTS", accepted_target_derivation_parents, identity="rho2 = residual + insertion_order_sum(target_scalar * normalized_physical_row)", positive_applicability（residual零ならLINEAR_ZERO_CANDIDATE、他はNOT_APPLICABLE）, uncommitted_tail_appended=false, old_numerical_replay=false, eof=trueとassurance三字段。

pivotsの各itemは `pivot_id,offer,lead,sigma,target_scalar,literal_exponent,physical_recipe_ref,row_ref,target_delta_ref,scope_sha256,raw_recipe,state_head`。三refはancestor ID。base_offersは全8059件の `offer,offset,length,sha256,physical_kind,conn_kind,lower_pivot_id,p1_source`。lower_pivot_idは非lower時null、p1_sourceは保存nested source.sourceの六字段（node/instruction_sha256/p1_sha256/cache_row_sha256/predecessor/ancestry_sha256）。lower_pivot_offersは挿入順のoffer列。residualは {parent_role,file,bytes,sha256,trits:48384,zero:bool}。raw_recipeは次のplain型とする。

- Conn: {kind:"conn",offer}。
- seed30/34: {kind:"legacy-seed",parent_role,file:"output/result.json",pointer:"/ancestry"}。
- packet: {kind:"packet-seed",parent_role:"packet",file:"output/packet/relations.json",pointer:"/seeds/s",seed:s,character:a}。
- 旧refinement: {kind:"refinement",parent_role:"refinement",file:"output/steps/j/materialization.json",pointer:""}。
- E: {kind:"e",parent_role,base,key,raw_file,primal_file,source_correction_file,p1_roots_file,physical_literal_file,B_file,geometry_role,geometry_base,witness_role,witness_file}。外部はbase="output",key="external-e"で各fileはbase直下、B_file=null。geometry_role=witness_role="oracle",geometry_base="output/geometry",witness_file="output/tree/witness.json"。loopはbase="output/snapshots/i/e",key="loop/i"、raw/primal/p1/physical/Bの相応phase下に各file、geometry_role=witness_role="continuation",geometry_base="output/fixed",witness_file="output/snapshots/i/tree/witness.json"。iは6桁snapshot j−1。

word-manifestはF3の全字段に `literal_dictionary_sha256,raw_streams,literal_dependency_closure,input_receipts` とassurance三字段を加えたexact objectである。raw_streamsの各itemは {key,parent_role,raw_word_file,raw_word_sha256,witness_sha256,geometry_manifest_sha256,word_stream,eta,literal_root:"raw-root"}。word_streamは元Eのexact encoding/letters/bytes/sha256/full_eofであり、新しいeof別名へ変えない。literal_dependency_closureは {prior_only:true,symbol_order:[{namespace,key,scope_sha256,node,node_sha256}…],all_used_edges_preserved:true}、symbol_orderはJSONL内Refの出現順。input_receiptsはancestor entries数。normalized-pairのexact字段はF3のまま（assurance三字段なし）。

top manifestの全字段は owner_sha256, source_sha256, accepted_head_sha256, word_manifest_sha256, target_history_sha256, normalized_pair_sha256, root_id, root_sha256, file_roster（全13名を辞書順）, files（manifest/result自身を除く11 payloadの {file,bytes,sha256} をfile名順）, all_inputs_unchanged=trueとassurance三字段。resultはmanifestの全hashへ結ぶためmanifest.filesにresultを含めてhash循環を作らない。

resultのexact字段は status="PASS", terminal（residual零ならPOSITIVE_WORD_CANDIDATE、他はNOT_APPLICABLE）, positive_applicability（target-historyと同じ）, positive_readout（residual零かつnormalized_pair=[0,0]だけPENDING_SAME_WORD_D_AND_SIDE_CONDITIONS、他はNOT_APPLICABLE）, manifest_sha256, owner_sha256, source_sha256, parent_roster_sha256, context_manifest_sha256, fresh_rho2_manifest_sha256, word_manifest_sha256, target_history_sha256, ancestor_index_sha256, normalized_pair_sha256, accepted_head_sha256, accepted_checker_sha256, completed_steps, rank, generation, state_head, target_remainder_sha256, residual_zero, normalized_pair, normalized_zero, root_id, root_sha256, nodes, source_lower_zero="NOT_ASSERTED_FOR_WHOLE_TARGET_WORD", old_numerical_replays=0, same_word_B_C=true, same_word_D=false, eleven_slot_replay=false, side_conditions="PENDING", grade2_member="NOT_DECIDED", grade2_nonmember="NOT_DECIDED", full_A0=false, parent_inputs_unchanged=true, eof=true, resource_limits={max_seconds,max_memory_mib}, elapsed_secondsとassurance三字段。Dは自分の測定時間へelapsedを一致させず、producerの有限非負測定値として認証する。resource_limitsは実CLI宣言へ結ぶ。source/fresh/contextの全hashの意味は上記と同じで、fresh_rho2_manifest_sha256だけ元fresh manifestの全hashである。


## F7. 最終入口・履歴・試験の補足

continuation の許可 workflow は .github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml、.github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml、root が新たに指定した .github/workflows/d972-r07-complete-oracle-cegar-resume-next-v1.yml の三つだけ。最後の名称登録は未来の成功・artifact pin を認める意味ではない。acceptance の実成功 tuple、全16親の実 bytes/roster、全 prefix checker PASS、selected の現 HEAD/result を引き続き要求する。同じ owner/source/start の以下三 file は実 completion32 candidate から再測定して固定した。

| continuation 内 file | bytes | SHA256 |
|---|---:|---|
| output/owner.json | 8612 | e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b |
| output/source.json | 2423 | c787d53c65c6392845e6f26c545e213b6b17d9b08dc07d694a1c4e33282f2651 |
| output/start.json | 54707 | 87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b |

source の producer SHA は凍結 P971 の 67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c、採用 checker SHA は継続 C v2 の e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3 に固定する。source と checker の Python 全文/NumPy version も acceptance の実 runtime と一致させる。成功出版直前に、16親・新 P/D source・raw3資料に加えて **acceptance file 自身の全 bytes/SHA** を再照合する。

A の accepted_target_derivation_parents は保存挿入順から構成する。最初の33件（base、seed30、seed34、packet3、refinement26、外部E）は selected start の列と完全一致する。新 loop j の追加 role は loop-e-<j:06d> で、実 step manifest/result/instruction/target の全 file または canonical target hash と state_head を保存する。snapshot j−1 の旧親列をその時点の列へ一致させる。各 E result.target_derivation は mode=derived、元 rho2 hash、directly_read=false、旧親列、明示 identity、new_delta の instruction/normalized/target/state の全四 hash を一致させる。Separator の最終 lambda の親列も一致させる。Linear で lambda=null の場合も、最後の result.target_derivation と実 step manifest から最後の delta を閉じる。

pivots の offer/lead は保存 instruction の同字段、state_head は同 instruction の rolling_sha256。physical_recipe_ref/row_ref の namespace は physical、target_delta_ref は target。base recipe は JSONL 全行の offset/length/pointer=null、後続は instruction.json の pointer=""。base target は result の pointer="/target_reduction"、後続は pointer="/target"。base physical payload の各行だけは全store内offset、個別 delta は offset0。physical payload は **base3 の4-trit packed（byte 0..80）** として lead を読む。

P1 補正の各 Power は元 Task554 の positioned row/companion receipt を使用箇所に保持する。raw E instruction の origin、実 witness/oracle manifest/raw-word、P1 reductions/roots/source-correction、physical-literal を全 file hash で一致させる。tree Ref 自身には、その scope となる実 geometry/fixed manifest の全 file receipt も付ける。normalizer Ref 自身と raw-e 内の normalizer 使用箇所は別 namespace の receipt を保持する。Rel.args.letters_sha256 は **末尾 LF 込み**。without-LF は既存 normalizer word hash と新 normalizer_words.word_sha256_without_LF に限定する。

新三群の --selftest は本番の WordDAG/read_normalized_pair、TargetHistory の行/挿入/残差reader、snapshot/HEAD外tail reader、raw grammar/Ref resolver、check_four_B を呼ぶ。小さな fixture は数値親の受理証明書ではなく、新しい語・metadata interface の境界試験である。旧成功 suite は再走しない。

- ordered-word-same-root-mod54: 順序、Inverse、内側/外側scale、typed同番号、0冪依存、負の18、bool拒否、自己child、別root、Rel hashのLF差、JSONL EOF。
- target-history-positioned-readonly: base3 packing、全store offsetと個別offset0、target scalar0のpivot保持、最後のDERIVED delta、Linear/nullと非零残差の区別、step1→snapshot0、未登録HEAD外tailの拒否。
- raw-cycle-auxiliary-four-B: 六cycle中の0係数も解決、同じwitness/tree、commutatorのsr(2)=-1、raw因子順、補助の9乗とeta、全四character payload/same witness。

selftest stdout は sealed .selftest、status="PASS"、tests=[{name,status:"PASS",rejected_cases:[string,...]}×3]、fixture_scope、production_interfaces_used、old_success_suites_rerun=0、candidate=false/cross_checked=false/verified=false。試験名は上の三つ。**ここで PASS は実装された成功時の出力契約であり、本便の実行結果ではない。**

本番 --max-seconds と --max-memory-mib は正整数で必須。selftest だけ省略時300秒/1024 MiB。後続 D の --producer-max-seconds/--producer-max-memory-mib へ同じ宣言を渡して result.resource_limits に結ぶ。時間は協調境界、memory は RSS と OS address-space ceiling で制限する。SIGTERM/SIGINT は停止flagを置く。成功 stdout は .result/exit0、不正receiptは .diagnostic の FAIL/exit1、資源不足は UNKNOWN_RESOURCE/exit3。引数の使用法不備は argparse の exit2。新outputを自分で作った後の停止だけ resource-stop.json/rejected.json を置き、入場前の停止では親や既存outputへ書かない。部分 bundle を成功として出版しない。

## F8. 完成・凍結と残る実走

完成 source は search/d972_r07_continuation_positive_word_readout_v1.py、**173286 bytes / SHA256 f5b35c56869188d5e56480fb0615d85686eb4c1c982419b4e764f585a4a25473**。LF2840、CR0、BOMなし、末尾LF、行末空白なしを metadata 読取で確認した。Task984 は全 A/B/C、三群canary、CLI/main、最終親固定差分を静的に読み、追加必須修正なしと回答した。公刊後の本sourceは凍結する。

本便で行ったのは指定二fileの実装/返信保存と source・実receipt・bytes/hash の読取だけ。ローカル AST/import/Python/GAP/数値試験、network/git/credential、新agent、Task983の新算術読取はない。旧source・公刊返信・workflowは変更していない。Task980の公開commit bc689f98d514ed0f767d875cd0679353a488b5de はrootによるものであり、その二fileも不変である。

本 A/B/C consumer と独立 D983 の AST・新canary・本番同語root照合は未実行。root の次 Task985 wrapper が実成功 completion32または明示手渡しの後続成功親から exact acceptance を作り、一回ずつ実行する。新 terminal、速度、語サイズ、grade2 MEMBER/NONMEMBER は予告しない。非零残差でも履歴/語の readout は候補として出し、positive適用は NOT_APPLICABLE。零の場合も同語Dとside/localization条件が残り、verified/full A0へ昇格しない。工房CV9の追加格付けはrootの実裁定を待つ。

判定: IMPLEMENTATION_FROZEN; A_B_C_SAME_ROOT_CONSUMER_COMPLETE; STATIC_REVIEW_NO_REQUIRED_FIX; LOCAL_RUNTIME_AND_AST_NOT_RUN; INDEPENDENT_D_GHA_AND_SIDE_CONDITIONS_PENDING; GRADE2_NOT_DECIDED; verified=false。

AUDIT_982_VERDICT:
