# Task963 — v548 witness から追加一行への最小 consumer intake

F0. **条件付き read-only 設計。** Task963 全文、正式 reply957 E、Task958 positive intake、v547/v548、Task959 の公開 witness/geometry ABIを前提に、自系 retained source の下記 entrypoints と v459/v542 を読んだ。完全 oracle は未走行であり、非零 witness を予測していない。元 full-origin の26段は観測された保存 prefix で、completion run33971897879/1 の独立 checker 完了までは新 parent として未受理である。Task959 の受理 pins は引き続き保留。本便は reply963 だけを作成し、新実装、ローカル数値/Python import/AST/GAP、network/git/credential/dispatch、追加 agent は行っていない。published reply958 は変更していない。

E は「oracle witness → legal raw word → 同じ raw Q2 chain/eta → full source → canonical P1 subtraction → 四 B の和 → 一行の物理追加」の consumer として切り出せる。44 seed/actor closure で cycle の係数をもう一度解く必要はない。以下の新関数名は提案であり、既存 export の存在を意味しない。

## F1. aux / 六 cycle から一つの ordered raw SLP

入力は受理された oracle `manifest.json/start.json/owner.json` と、そこから参照される `geometry/{parent,parent-edge,bfs-order,chord-edges}.u32`、`carry.u8`、`tree/{chord-tau,chord-values,chord-residuals}.u8`、`selected-chords.u32`、`witness.json`。candidate-only 出力を無条件に新 parent にせず、root の受理と双方 checker の一致を exact tuple/bytes で固定する。

`T_0=1`、`T_v=T_parent(v)*g(parent_edge(v)%2)` を同じ geometry の tree SLP とする。chord の語は `W_e=T_tail*g*T_head^-1`。witness の並びは failed chord が先頭、その後に保存された五つの basis chords の選択順である。係数を `{0,1,-1}` の signed representative に直し、

```
w = W_failed * product_(j=1..5, recorded order) W_basis[j]^(-d[j]).
```

を一つの root にする。0 の因子は word では identity としてよいが、元 witness の六項 receipt（0 を含む）と edge ID は保存する。edge ID sort への並べ替えや literal coefficient collection はしない。

raw SLP node は最低限 `Identity,Letter,Ref,OrderedProduct,Inverse,IntegerPower`。trit coefficient の2を inverseにする規則と、次の **整数 power** を区別する。各 node に ordinary integer exponent pair `(A,B)`、mod3 の `omega`、語長の上界、actual Q0/Q2 endpoint を bottom-up に持たせる。

```
A(uv)=A(u)+A(v), B(uv)=B(u)+B(v)
omega(uv)=omega(u)+omega(v)+B(u)*A(v) mod3
omega(u^-1)=-omega(u)+A(u)*B(u) mod3
omega(u^m)=m*omega(u)+m*(m-1)/2*B(u)*A(u) mod3
```

chord branch は全保存 cycle の `tau` と chain の boundary を再計算し、`tau(z)=0`、`scalar=f(z) !=0` を確認する。v546/v547 の保持前提から w は N0、A/B は6の倍数となるが、consumerも ordinary integer divisibility を実測する。`g=signrep(omega(w))` として、v547 の固定順

```
C(z)=w * (r_x^3)^(-A/6) * (r_y^3)^(-B/6) * [r_x,r_y]^g
[u,v]=u^-1*v^-1*u*v
```

を適用する。指数をmod3にしてから割らない。Q0/Q2 endpoints、normalizerのzero Fox、rootのinteger exponent `(0,0)`、rootのomegaを接続し、同じ root が `J_Q2(C(z))=z, eta=0` を持つ receipt を出す。Omega 所属は v547 の明示 endpoint 読出しと保持された有限群前提に結ぶ。single E3 projectionを全Deltaのfaithful representationと呼ばない。

aux branch は `(z,eta)=(0,e_x)` または `(0,e_y)`、literal はそれぞれ **`c_x=r_x^9` / `c_y=r_y^9`** である。ordinary exponentは `(18,0)` / `(0,18)`、normalized pair は選択した eta。ここで exact exponent zero に直すと witness 自体の方向を消す。`J_Q2(c_i)=0` と正しいetaを確認し、そのまま section subtraction へ渡す。

normalizer atom の具体入力は `scratchpad/a0_v2_words.json.raw_q0_relators` の19語、roster SHA `dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a`（compact ASCII JSON、LFなし）。whole-file SHA `fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612` と区別する。v459 の

```
r_x=q1*q6^-2*q7^4*q9, r_y=q8^-1*q4^-1
```

を実際に構成し、同便の reduced-length/hash を照合する。

| atom | reduced length | compact signed-word JSON SHA256 |
|---|---:|---|
| r_x | 1058 | 82fa1ff07d5269e5228fb411b97321b61869791c49133aaa65161f44d16b6f2c |
| r_y | 466 | 88657577db0338fd5c58f7edeec205c27ce5ff5ddba128b8af403167cb232ac0 |
| c_x | 9522 | 2935d479d5896360e71b66aa95bcb964cdb04d9716f27c06f492034b5ac98abb |
| c_y | 4194 | c1f3ebec1ef6c448b854b216f8473e674a67a3b5d3a3059888af016293a1a6dd |

この19語を使うのは明示 normalizer の literal dictionary としてであり、旧 lane の physical model/payload を現 owner に持ち込むためではない。q_i や r_x/r_y は N0 の語であって、個々を Omega relator と宣言しない。legal-root の v547 certificate と raw atom の型を分ける。

## F2. actual endpoint / raw Fox / full source の最小演算

調べた自系 entrypoints は次の契約を持つ。

| source / function | 引数 → 返値 | この consumer での用途・限界 |
|---|---|---|
| `d972_r07_actual_grade2_root_scalar_batch_v2.py:source_context()` | なし → `(context,words)` | accepted actual v15 の marked PSL順・Q2画像・transport・paper dictionary |
| `d972_r07_targeted_grade2_owner_generated_join_v15.py:_seed_perm_mul(left,right)` / `_seed_perm_inv(value)` | permutation tuples → tuple | `right[left[i]]`。元36点Q0 markingにも使える原始積/逆。ただしQ0 SLP endpoint wrapper自体は新設 |
| 同 `_seed_affine_eval(word,images)` / `_seed_affine_mul(left,right)` / `_seed_affine_inv(value)` | signed letters / `(P,e0,e1,k)` → 同じQ2型 | section-left/kernel-right、kernelはmod3。Q0mod9へ黙って流用しない |
| 同 `_seed_affine_fox(word,images)` | signed-letter iterable → `(dict[(component,SeedAffine),trit],endpoint)` | 非閉 word を許す。正letterは前prefix、負letterは逆元へ進んだ後のprefixで負号 |
| 同 `_seed_qnorm(word,context)` | **closed** Q2 word → `([(PB3_component,SeedAffine,trit)],x_augmentation)` | endpoint-oneを要求。tree prefixなど非閉入力には使えない |
| 同 `_seed_evaluate_seed(context,word)` | signed-letter tuple → `(d0[4,6048],d1[4,18144],d2[4,36288],aux[8])` | 名前はseedだが本文はwordを六tagへ置換する。全tagでclosed、integer exponentsの18整除を要求。flat入力のbounded comparatorにはなるがSLP consumerではない |
| 同 `_seed_e_poly(k)` / `_seed_cv(label,parity)` | kernel/parity → 十monomial係数 / trit sign | producer側のfull filtered source scatter。sourceのd0/d1寄与を捨てない |
| Task959 `geometry_inputs(arith,context)` | actual context → right graph、phi、tree、carry等 | 新geometryの同じ owner/roster。既存oracleの保存arraysは独立checkerの受理後にhashで使える |
| Task959 `raw_edge_source_fixture(arith,context,tail_word,slot,wrong_left=False)` | 一つの非閉edge → full source tuple | changed-interface canary用の小さなforward scatter。cycle/SLP materializerはまだない |
| Task959 `raw_edge_pullback(context,geometry,score,kappa)` | 全scoreとkappa → f[108864] | scalar adjointだけ。これをsource rowを出す関数と呼ばない |

新 `evaluate_raw_slp` の最小状態は各nodeの **actual endpoint と一つの raw chain**、別のordinary `(A,B,omega,length)` で足りる。Q2 chainは `F3[Q2]^2`、edge順はoracleの`2*q+slot`。基本式は

```
J(UV)=J(U)+ev(U)*J(V)
J(U^-1)=-ev(U)^-1*J(U)
```

である。ここで作用は **raw Fox prefixへの左積** `s -> ev(U)*s`。graphの正edgeは右積`q -> qX/qY`である。正規化後のhomogeneous Task712 Tを、非閉prefixの一般Fox作用として使わない。powerはこのproduct/inverse規則による二乗法または省メモリ参照消費で処理できる。

同じ actual Q0 endpoint は、`fuda1_a0_rmax_data.g` の二つの元36点 permutationを読み、36点identityから同じSLP product/inverse/powerを評価すればよい。Task959 `validate_marking` の全36点 equalityを通す。Q0のmod9 carry座標とQ2mod3の型を分け、carryによるtauとordinary exponent/omegaが同じraw SLPに属すことを確認する。新Deltaの列挙・新27表は必要ない。

全nodeへdense108864-chainを保持する設計は避ける。raw tree部分は選択された六cycleのpathを順に消費し、normalizerは小さなatomとpower DAGで評価する。P1語はこの段階では評価/flattenせず、後述のaccepted canonical Refとして保持する。

flat入力を補助に使う場合の上界は保存metadataから導ける。tree depthをparent順で計算し `h=max depth <= N-1` を確認すると、

```
L0=sum_(nonzero witness terms) (depth(tail)+1+depth(head)) <= 6*(2*h+1)
```

は未修復wの安全な長さ上界である。free reduction前のfactor長なので、reductionで大きくならない。v547の修復後も

```
L(C) <= L0 + 3*abs(A/6)*1058 + 3*abs(B/6)*466
              + 2*abs(signrep(omega))*(1058+466)
```

を **整数**で先に保存できる。auxはv459の上表の長さをpinする。上界、実emitted letter数、EOF、binary/JSON encodingごとのhashを確認してからbounded flattenを使う。上界が運用capを超えれば UNKNOWN_RESOURCE またはDAG経路とし、短いと仮定して切らない。非可換P1語全体へのflattenやcoefficient collectionにはこの上界を流用しない。

raw chain/etaからの新 `source_from_chain` は同じ z を全六tagへ送り、各termを `phi_j(q)*prefix` と左積し、右qnorm stencilを適用する。

```
x-Fox term (s,d): -component0 at sX, -component1 at sXB, aux_j += d
y-Fox term (s,d): +component1 at s
XB=Y^-1
```

その後、同じtransport、全d0/d1/d2、共有auxをscatterする。aux6/7は最後の**同じ legal root の整数指数/18 mod3**または照合済みetaであり、raw edgeのmod3値を18で割って作らない。返値は上表のfull tuple。`J(root)=sealed z`、normalized pair=sealed eta、`source_from_chain(z,eta)`とsame-root direct raw-SLP経路の一致を要求する。

producerは自系 affine/Fox＋十monomial展開、checkerは自系marked graph / ordinary27係数・moment抽出等の別経路で、この実raw-source部分を計算する。SLP文法・順序・pins・array ABIのみ共通にし、新action/scatter/solver helperは共有しない。

## F3. primal section は old → new、元leadは昇順

新 `reduce_source_p1(raw_parts,basis_metadata)` は Task959 の dual interpolation を逆呼出しする関数ではない。入力bは `concat(d0[4,6048],d1[4,18144],aux8)`、出力は `alpha.u8[8059]`、ordered reduction events、full96776 lower remainderである。

1. Task554 prepare の `old_blocks[a].record.dag_nodes[p].lead` と lower/grade blob pinsを読む。old元lead l の joint E=24200座標は、l<6048なら `a*6048+l`、auxなら`24192+l-6048`。全old行をこのembedded **元lead昇順**に一巡する。canonical IDは `O[a]+p` のまま。
2. pivot座標の現在tritを係数とし、normalized old lower rowをd0 owner＋共有auxから引く。**同じ係数でoldの全四d1 companionも引く**。元leadをfull96776行のfirst_nonzeroに置換せず、元normalized rowへdag scaleを重ねない。old後に全d0/共有auxが零であることを確認する。
3. 各ownerのnew `basis_blob` を `pivot_leads[p]` 昇順で消去する。canonical IDは `H[a]+p`。newはownerのd1だけに作用する。最後に全96776 zeroと `b_raw=sum_i alpha_i*b_i` を照合する。

`O=(0,505,1008,1511)`、`H=(2014,3523,5035,6547)` は現canonical order。stored row offsetは常に元local ID×packed row bytesであり、sortした順のoffsetに変えない。alphaの添字とliteral factor順を分け、literalは記録したnonzero reduction eventsの順にする。

具体的readerは `d972_r07_actual_grade2_root_scalar_batch_v2.py:_state_descriptor(parent,index,need_blobs=True)`。引数parentは `{root,head,body,files}`、index=-1またはowner0..3、返値は `{root,head,body,body_sha256,index,blob_descriptors}`。Task959の `PackedRows(root,descriptor).row(local)` は pinしたpacked blobから一行を返す。これらを各自のlineageで使い、五つの大きなTask554 bodyは一度に一つ、元leads/小descriptorだけを残す新 `basis_segments` adapter が最小である。44seed relation全体を再生成するための `collect_relations` は必要ない。

top側は同じalphaとaccepted P1 cacheを使い、

```
z_prime[a] = raw_parts.d2[a] - sum_i alpha[i]*canonical_z_i[a], a=0..3
```

を作る。全145152-trit row/cache pinとindexのrow/ancestry hashへ結ぶ。Task954 `canonical_input(m,p1,index,segments,node)` は一つのcanonical full tupleを返す。`subtract_lifts(m,p1,index,segments,coefficients,reference_nodes,parts)` は渡したpartsを**in-place**に全top/lower/auxで引き、nodeごとのcomponent hash receiptsを返す。これは再利用できるrow/blob原始処理である。Eではraw_partsの別copyから同じalphaを引き、primal消去のlower zeroと一致させれば、二重減算を避けられる。selected全Refのcache/EOF/12 blob pinsを残す。

raw legal word rootをC、canonical P1 wordをW_iとすると、補正語は

```
V_word = C * product_(recorded primal reduction events) W_i^[(-alpha_i) mod3]
```

である。W_iはaccepted P1 DAGのorigin/ordered reductions/scaleへ繋ぐRefであり、係数2はliteral inverse。数値alphaは集約してよいが、P1語の順序を集約/sortへ書き換えない。V_wordのinteger exponentは改めて保存する。full source lower zeroからnu=0 mod3が出ても、exact integer exponent zeroを自動的に主張しない。

## F4. 四 B の和と新しい一行への接続

source lowerが零になったraw correctionに対してのみ、Task712の四つのhomogeneous Bを使い、

```
G = sum_(a=0..3) B_a(z_prime[a])
old_lambda(G) = sum_a dot(q_a,z_prime[a])
              = sum_a dot(q_a,raw_top[a]) - kappa(raw_lower)
              = oracle witness.scalar != 0
```

を実測する。`d972_r07_actual_root_seed_materializer_v3.py:apply_sparse(entries,source_width,destination_width,row)` が各Bのprimal sparse map、同版 `pack/unpack/dot` が行の実型である。Task954のsingle-character `append_step` wrapperは呼ばない。

次の既存原始処理はcurrent rowsを引数で受ける。

| 関数（すべて actual_root_seed_materializer_v3.py） | 引数 → 返値 / 必須照合 |
|---|---|
| `physical_reduce(raw,pivots,rows,verbose=True)` | packed G、current metadata/rows → `(packed remainder,ordered reduction dicts)`。physical **挿入順**の全sweep。sourceのlead sortとは別 |
| `normalize_pivot(remainder,old_leads)` | packed非零remainder → `(packed normalized,lead,scale)`。scale1/2、旧lead全部零、新lead1 |
| `update_target(old,normalized,lead,old_leads)` | accepted current target → `(new_target,target_scalar)`。scalar0も合法 |
| `check_final_separator(functional,rows,parent_target_raw,remainder_raw,verbose=True)` | current/newlambda → 全row零、両target dot1とhash receipt |

`old_lambda`が全current rowsを殺すことを先に接続し、物理消去後もold_lambda(remainder)=oracle scalar非零を確認する。これで新normalized rowのrank上昇はちょうど一行である。target scalarはoracle scalarやnormalization scaleとは別で、0ならtargetは変わらない。

target非零ならfresh separatorを新targetの最初の非零free coordinateから作り、**physical挿入順の逆順**で全旧行＋新行を処理し、全行・parent/new targetを直接sweepする。`full_origin_refinement_v1.py:next_separator(m,state,normalized,lead,target,step)` はこの動的state算術の既存例である。一方 `actual_root_seed_materializer_v3.py:separator_after_append(...)` は本文のnew `offer`に固定 `CURRENT_GENERATION` を使う。両方の古いwrapperには親数/namespace/DERIVED receiptの固有契約があるので、新Eでは動的current generationと新cycle parent typeを持つ小wrapperを作る。数値原始処理を再利用しても旧metadataをそのまま出さない。

区別すべき点が一つある。**全96776 source lower zero はraw V_wordのreceipt**である。物理正規化で引く旧Conn pivot wordはphysical lower zeroであって、source P1 lower zeroとは限らない。したがってnormalized physical pivot word

```
S_new_word=(V_word * product_(physical reductions) S_old_word^[(-q) mod3])^[scale]
```

については、同じordered ancestryからphysical lower zero/top=normalizedを主張する型にし、raw V_wordのsource-zero receiptをコピーしない。

## F5. 26段prefixに追加一行だけを結ぶ提案 ABI

次consumerは `d972.r07.selected-cycle-materializer.v1` のversioned **standalone delta** とするのが小さい。CLIはexact accepted refinement root、exact accepted oracle root、既存canonical P1/Task554/Task712 roots、fresh output、resource bound。旧26段のscan/insert算術を再走しない。Task959の`accepted_snapshot(refinement,p2,m,base,descriptors,args)`は薄い親loadの例だが、現時点では受理pins未設定であり、この関数を完成済み受理証明と呼ばない。

| 新出力 | 内容 |
|---|---|
| `start.json/owner.json/source.json` | accepted completion artifact/HEAD/result/source、oracle manifest/start/witness、P1/Task554/Task712/dictionary、runtime pins。current rank/generation/head/target/lambdaを明示 |
| `raw-word.json` | F1のtyped SLP、root、tree/normalizer parents、length bound/count、ordinary A/B、omega、Q0/Q2 endpoint、v547またはv459合法性receipt |
| `raw-chain.bin` / `raw-source-*.bin` | sealed witnessと同じQ2 chain/eta、full d0/d1/d2/aux、same-word source再生とoracle scalar一致 |
| `p1-coefficients.u8` / `p1-reductions.json` / `p1-roots.json` | 全8059 alpha、元ID/lead/offset/hash、ordered events、canonical祖先。full lower remainder零、z_prime[4,36288]を別保存 |
| `physical-raw.bin/physical-remainder.bin/physical-normalized.bin` | 四Bを合計したG、そのordered消去、normalized一行 |
| `instruction.json` | predecessor=current head、offer=current generation、rank/generation各+1、physical offset=current rank×12096、origin.kind=`v548-cycle`または`v548-aux`、oracle/witness/word/P1/source refs、ordered physical reductions、lead/sigma、row hash、target scalar/hash、rolling hash |
| `target-remainder.bin` / `result.json.target` | plain `{parent_remainder_sha256,remainder_sha256,scalar}`。old target historyをコピーしない |
| `lambda.bin` / `result.json.separator` | target非零のときだけ。fresh reverse solve / 全rows / 両targetのdirect receiptと別のDERIVED rho2 certificate |
| `manifest.json/HEAD` | exact file roster / hashes、accepted parent→この一行のchain。payload/manifestをdurable化した後にHEADを公開 |

parentの観測済み26段をcompletion後に受理できた場合、追加のgeneration/row offsetはそのexact HEADから求める。旧base・seed30/34・packet3段・refinement26段の名前付きtarget identitiesを継ぎ、今回の

```
parent_remainder - new_remainder = target.scalar * new_normalized_row
```

だけを新実算術として足す。原rho2を直接読んだとはせず `mode:derived,original_rho2_directly_read:false` を維持し、現在/新targetへのactual dotと分ける。

後続のthin loaderはaccepted parentのrows/targetをhashで読み、この新一行のmanifest/rolling predecessor/normalized type/target/lambdaを足せばよい。新E checkerは**新raw-word/source、primal P1消去、四B、物理一行、target/freshlambda**を独立再計算する。旧scan/insertの全数値再走を追加gateにしない。途中deadlineでは未完prefixをpositive/negative結果にしない。

## F6. 最小実装単位と下流の境界

新設が必要な単位は、(a) witness→ordered legal raw SLP、(b) actual endpoint/raw-Fox SLPとcomplete source adapter、(c) old→new元lead昇順のprimal P1消去、(d) 四Bとcycle型の一行delta wrapper、の四つである。既存のmetadata/blob/packed row primitivesと新たなsource/literal consumerを区別した。Eのproducer/checkerは公開契約だけを共有し、特に(b)と(c)の算術を別計算にする。

Eが完成しても、結果は新physical pivot candidateとtarget deltaである。targetが零になった場合には、Task958の保存全target係数から一つのordered correction wordを作り、同じwordのnormalized exponent pairと全11 typed slotsを直接再生する下流consumerが別途必要である。raw sourceの6 tagsを11 slotsと呼ばない。新pivotをもってMEMBER、full H/P/A0、cofinal lift、cross-checked、verifiedを宣言しない。未実測のend-to-end秒数やrank収束回数も見積もらない。

AUDIT_963_VERDICT: CONDITIONAL_SELECTED_CYCLE_CONSUMER_SPECIFIED; RAW_SLP_SOURCE_AND_PRIMAL_P1_FOUR_B_ONE_ROW_WRAPPERS_PENDING; NO_ORACLE_OUTCOME_PREDICTED; verified=false
