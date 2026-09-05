# Task964 — 同じ complete source の固定 cycle packet

F0. **紙上では可能。実用速度の採否は未決。** Task964、v548/v543/v546/v547、正式 reply957、Task959 の公開 geometry/witness ABI、Task963 と返信、Task958 の positive 接続を読んだ。以下は同じ登録 source の有限基底を固定する設計であり、新 source、旧504 orbit、実装、runtime 発注を追加しない。変更は本返信だけ。ローカル数値、Python/import/AST/GAP、network/git/credentials/dispatch、追加 agent はない。Task961 の completion 親の実 pins と最終 freeze が届いたら、その監査を優先する。root からの全26段 checker PASS 連絡は承知したが、本便の紙上の同値は新 artifact の未読 bytes や CV9 の受理を前提にしない。

F1. **54428＋2 本は D の基底であり、補正後の物理行は M2 の生成系になる。** v543/v548 の型をそのまま使う。

```text
Z = ker(partial:F3[Q2]^2 -> F3[Q2]), dim Z=54433
tau:Z -> F3^5 onto, K=ker tau, D=K direct-sum F3^2
Psi:D -> W2 onto, pi:W2 -> W1 onto
s:W1 -> W2, s(b_i)=tilde_b_i, pi s=id, i=0..8058
R=id-s pi, ell=ell1 pi
M2=G(ker ell)=span(Conn)+G(ker pi).
```

tree/chord は reply957/959 の正 X,Y BFS と edge ID 昇順を固定する。全 chord の fundamental cycles を z_e とし、tau が独立な最初の五本を順序付き J=(e_1,...,e_5)、T の第 j 列を tau(z_ej) とする。J の選択は lambda に依存しない。e outside J ごとに

```text
d_e=T^-1 tau(z_e), k_e=z_e-sum_j d_e[j] z_ej.
```

と置く。これらは tau 零である。線形関係 sum_(e outside J) c_e k_e=0 の z_e 係数を見ると各 c_e=0。逆に z=sum_e c_e z_e が ker tau にあれば、J 上の係数は outside J の係数から T を使って一意に定まり、z=sum_(e outside J) c_e k_e である。従って54428本は K の基底、二つの独立 eta を足した54430本は D の基底である。各 k_e は零係数を含め高々六 cycle の組合せだが、全列がこの疎い cycle 記述を持つことと、展開 edge/word/source/physical 行が疎であることは別である。

線形写像

```text
A=G R Psi = H R Psi : D -> P, P=F3^48384
H(b,z)=sum_a B_a(z[a])
```

を固定する。v548 (1.3) の G-H=C pi と pi R=0 が、**D の全入力**に対して等式を与える。これは非零 witness 一個だけの性質ではない。Psi が onto、R(W2)=ker pi なので A(D)=G(ker pi)。従って

```text
M2 = span(Conn, A(k_e,0) for all e outside J,
                A(0,e_x), A(0,e_y)).                  (964.1)
```

が成立する。前件は同じ complete legal source/Psi、実 P1 の独立8059基底と同じ canonical lifts、全 physical lower relations の Conn である。canonical P1 を現在の physical pivots へ置き換えない。物理 lower 関係を source-rank で代用しない。v546 の12092は A の source grade の上限を与えるのであって、Conn を含む全物理像の次元そのものではない。

**各 A 列の非零・独立は従わない。** 零列や従属列を含み得る。v548 の rank-rise は、その時点の lambda が S_current 全体を殺し、その一列への pairing が非零の場合に限る。旧 lambda が二列に非零でも二列が独立とは限らない（同一行を二回選ぶ場合だけでも反例）。固定 packet に非零 witness の rank 保証を一括して付与しない。

F2. **基本の lambda-free packet と現在 state の消去を分ける。** packet の数学的 key は Q0/Q2 marking、PSL 順、tag/transport、tree/carry/J、P1 source basis/lifts/index、四 B と Conn の accepted parent、および各算術 source pin である。current lambda/target は packet 行の定義に入らない。Task959 の geometry *stage manifest* は snapshot_sha256 を持つので、将来 packet の再利用時にその manifest を別 snapshot のものへ偽装しない。array の固定値と別の packet owner を明示し、current HEAD は消去 consumer の start に置く。

各列 u=Psi(k_e,0) または Psi(0,e_i) について、新 primal adapter で

```text
pi(u)=sum_i alpha_i b_i,
v=u-sum_i alpha_i tilde_b_i,
all96776 lower(v)=0,
A_col=sum_(a=0..3) B_a(v.d2[a])
```

を計算できる。primal は **old の元 embedded lead 昇順 → new 各 owner の元 lead 昇順**、row ID は canonical insertion ID のまま、stored normalized row への scale 再乗算なし。old 行の全四 d1 companion と共有 aux を同じ係数で引く。これは reply957 の dual の段順・向きとは異なる。kappa は lambda に依存するので、その数値を固定 packet の section そのものと呼ばない。

current S に対して packet を決めた順序で読み、各行を **その時点の全 current physical pivots** で消去する。非零 residual のみ normalize/append し、target の対応 lead を消す。ブロック処理でも、ブロック内で既に選んだ新 pivot を後続行から除去する独立な elimination が必要である。旧 lambda の scalar 全列を一回計算して、その非零列を全部無条件 append する方式は不可。

全列を走査した span は (964.1) により M2 である。target が途中で零になれば線形所属の係数 receipt を出せる。target が非零で全 packet EOF になれば、全 basis を殺す fresh lambda を作り、**Conn/accepted rows と全54430 packet rows**への residual/pairing を同じ lambda で再掃引し、両保存 target への dot1 と原 rho2 の DERIVED identity を区別して保存する。途中停止は UNKNOWN。全 row を読んだ事実は旧 lambda に対する非零件数では代替できない。正式 MEMBER は F4 の same-word readout を待つ。

F3. **最小 receipt。** 全 decoded source matrix や全 literal 展開を保存する必要はないが、以下の完全性と ancestry は必要である。

| receipt | 最小内容 |
|---|---|
| geometry/source domain | exact parent pins、qid/右 edge/左 Fox/tag qnorm、全 tree/chord roster、実36点 Q0 reconstruction、全五 carry、rank5、J/T、outside J の edge ID 昇順と全 d_e、二 eta、全 boundary/tau 零、件数/EOF |
| canonical section | original/embedded leads と row IDs、12 lower blob pins、P1 v9 cache/index/instructions pins、s(b_i)=tilde_b_i の保持前提。基本方式なら全列 alpha[8059] と ordered nonzero primal events、全96776 lower-zero check。F6 の compiled 方式なら全8059 **物理 vector** interpolation 等式と明示された線形 extension を保存し、primal ancestry は要求された列で作る |
| packet rows | row ID→source basis descriptor→section receipt→packed physical offset/length/hash、四 B の和、exact file roster/full EOF。生の unnormalized A 行の hash を normalized pivot と分離 |
| state reduction | accepted initial HEAD/rows/target/Conn、全 offer の ordered reduction coefficients、零/非零 residual、非零時の lead/scale/new row、前後 target/scalar、rolling predecessor、完了 row cursor。未完部分を complete packet として扱わない |
| terminal | 所属なら全 accepted/new pivot の target coefficients と零 target。非所属なら一つの fresh lambda、全 accepted/Conn/packet pairing residual と EOF、両 actual target dots、別の DERIVED rho2。source-map/P1/Conn の保持前提と numerical comparison/verified=false を明記 |

基本方式の alpha は数値配列として集約可能だが、ordered primal events と canonical Ref を literal から消さない。上の「全 row residual」は packet の全 physical offers を含む。非零 offer だけを receipt に残す方式では完全 EOF の根拠が失われる。

F4. **literal は全列で構成可能だが、線形な word selector ではない。** 各 k_e の raw word は W_e を先頭、次に J の選択順で W_ej の signed powers を置く。**五本の z_ej は一般には非合法**であり、個別に Omega word へ正規化したとの仮定を置かない。組み合わせた w 全体の tau が零であることから v547 の

```text
C(k_e)=w*(r_x^3)^(-epsilon_x(w)/6)
         *(r_y^3)^(-epsilon_y(w)/6)*[r_x,r_y]^sign(omega(w))
```

を固定順で使う。整数 exponent と omega は同じ SLP の bottom-up 値、division は整数である。aux 列は c_x/c_y をそのまま使い、先に exact exponent 零へ直して eta を消さない。その後 canonical P1 words の負係数因子を **primal event 順**で付ける。v547 の word R と v548 の線形 R=id-s pi は別物で、word の掛算を線形係数の sort に置換しない。

全列の大きな word DAG を先に展開せず、tree parent/J/d_e/normalizer rule と P1 Ref から必要な列の同じ ordered DAG を再生成する方式は可能である。Task963 の source SLP/endpoint/Q2-chain/eta 照合を実施した列についてのみ、actual literal replay 済みと記す。基本 packet の全行 source-zero と、物理消去後 normalized pivot word の source-zero を混同しない。後者が引く Conn word は physical lower-zero でも source P1 lower-zero とは限らない。

target 零なら、全 target scalar を accepted ancestry とともに挿入順で読出す。scalar0 の pivot も後続行の参照になり得るので祖先から落とさない。Task958 の one-root SLP、同じ word の normalized pair、11 typed slots の直接 Fox/grade/printed aggregation が別 consumer として必要である。六 source tags を11 slotsと呼ばない。raw cycle ごとの word を先に作ったことだけで、最終同一語の gate を満たしたとはしない。finite grade の線形所属、正式 MEMBER、full A0 を分ける。

F5. **具体的な幅・保存量・基本方式の支配項。** 下表は既存 ABI の整数式であり、新計算の実測ではない。M=54430、r=8059、L=96776、U=4*36288=145152、P=48384。packed は4 trits/byte、alpha は行末 padding を入れる。source metadata/JSON/index/hash、Python object overhead、一時 dtype 変換は表の数値に含めない。

| 対象 | trits / decoded uint8 bytes | packed bytes |
|---|---:|---:|
| source lower 一行 | 96776 | 24194 |
| 全四 source top 一行 | 145152 | 36288 |
| full source 一行 | 241928 | 60482 |
| physical 一行 | 48384 | 12096 |
| alpha 一行 | 8059 | ceil(8059/4)=2015 |
| full source 全 packet | M*241928 | M*60482 |
| corrected four top 全 packet | M*145152 | M*36288=1975155840 |
| physical 全 packet | M*48384 | M*12096=658385280 |
| alpha 全 packet | M*8059 | M*2015=109676450 |
| canonical P1 top cache | r*145152 | r*36288=292444992 |
| h_i=H(tilde_b_i) 全 P1 | r*48384 | r*12096=97481664 |

Task554 lower は full96776を各行に埋め込んで保存せず、old2014本の6056＋72576、new6045本の18144を使い、合計

```text
Lblob=2014*(6056+72576)/4 + 6045*18144/4 = 67011332 bytes.
```

`full_origin_refinement_v1.py:753 subtract_lifts` は選択 top を positioned read する一方、毎回12 lower blobsを全 hash/EOF まで読む。これを M 回呼べば lower だけで M*Lblob、top は sum_c nnz(alpha_c)*36288 bytes の入力になる。`PackedRows.__init__` も全 blob pin を hash するため、各列で reader を作り直したのに「一度の認証」と数えない。pin した handles/indexを保持し、block内で読んだ同じ行を複数 RHS に使う新 adapter が必要である。

primal 算術では、各列について全8059 pivot coordinateを決めた順で調べる。非零係数の old lower/全 d1 と new d1 を引く必要があり、source の疎い入力だけから疎い alpha は導けない。保守的な decoded lower traffic 上限は一列あたり

```text
2014*(6056+72576)+6045*18144 = 4*Lblob
```

に相当する row updatesと、その dtype/accumulator/read overheadである。top の直接補正は nnz(alpha_c)*U、四 B の素朴な `apply_sparse` は一列あたり E_B=sum_a nnz(B_a) 個の triplet 走査を行う。同関数は source が疎でも全 entries を回る。source-coordinateごとの B adjacency を新たに作れば使う座標の entries だけにできるが、その index の構築/保持と actual support の計測を必要とする。

block b 列を保持して lower blobs/P1を一巡ずつ配る基本方式なら、decoded accumulator は概ね b*(L+U+r+P) bytes と少数の一行/一 chunk buffers、reader/metadata/physical basisである。入力の再走査は最大 ceil(M/b)*(Lblob+292444992) に one-time instruction/index 認証を足す形で見積もれる。実 sorted lead は stored row ID順と異なるので、単純な file順一巡は primal solveではない。lead順の seek/index cacheを使うか、別に pin した lead順 scratchを一回作る。block streamという名前でこの reorder/読み直しを隠さない。

物理 echelon の常駐 packed rows は R_final*12096 bytes＋records。全列消去は sum_c R_c 個の pivot-coordinate probe と、実非零 elimination 数 E_red に対する E_red*12096 packed-byte AXPY が基本項である。`first_nonzero/normalize_pivot` と最終 pairing は48384への unpackを伴う。全 packet の一回の final pairing sweepは最低 M*12096の入力、算術は M*48384 tritsである。毎追加後に全旧行 sweepを行うなら、その分も sum_steps R_step*48384で加える。将来 R_final、E_red、target-zero時点は推定しない。

F6. **h cache と compiled section の二段階。** canonical P1 の純 homogeneous physical cache

```text
h_i=H(tilde_b_i)=sum_a B_a(z_i[a])
A_c=H(u_c)-sum_i alpha_c[i]*h_i
```

は正しい。同じ lower contribution を両側で引く v548 に基づくので、h_i を **G(tilde_b_i)** と呼ばない。r*36288の P1 streamと四 B により一度構築・独立照合し、r*12096の固定 cacheにできる。基本方式の以後の top subtraction は nnz(alpha_c)*12096の packed inputで済むが、**alpha の primal solveは残る**。raw full sourceのlower照合と、必要な same-word/canonical top再生も消えない。

さらに次の任意の source-lower extension を vector-valued interpolation で一度構成することは紙上で可能である。

```text
Gamma:Lsrc -> P, Gamma(b_i)=h_i, ambient free coordinates=0.
Phi_raw = H Psi_raw - Gamma Psi1_raw.
Phi_raw|D = H(id-s pi)Psi = A.                         (964.2)
```

ここで Psi_raw は reply957 F4 の実 raw-edge/eta 線形 extension。Gamma は **physical lower rank6705の multiplierではない**。kappa と同じ source lower座標に対する、出力48384-vectorの補間である。new d1 の元lead降順でまず解き、old RHSから全 d1 companion の Gamma値を引き、その後old embedded元lead降順で解く。free0なので非零になり得る列は8059個の pivot座標だけであり、Gamma の supported-column cacheは r*12096 packed bytesで足りる。full L×P matrix の常駐は不要。

必須の認証は **全8059本の Gamma(b_i)=h_i という48384-vector等式**であり、現在lambdaでのscalar一致だけでは足りない。新旧同じcanonical row IDs、元normalized rows、全四h、free0/lead orderを保存する。これが通れば、raw prefixや非合法基準chordにも Phi_raw を線形に適用できる。ただしその値を G R Psi と呼べるのはlegal入力上だけである。s piを非合法 z_ej/tree prefixへ直接適用するのは型違反。(964.2)はその違反をせずに数値的な tree共有を可能にする明示 extension である。

compile費用は消えない。h_i構築の r*E_B の素朴な sparse処理に加え、元 source basis行が他の pivot座標に持つ非零係数の総数を E_tri として、Gamma solveに E_tri*12096 packed AXPY相当、全8059 vector等式に同等の再照合と読込が必要になる。二段型からの保守的な pair数上限は

```text
sum_a new_rank[a]*(new_rank[a]-1)/2
 + 2014*6045 + 2014*(2014-1)/2
```

であり、実 E_tri や疎性は未測定。h/Gammaを二つとも全常駐させる必要はなく、物理座標tileで再構築する選択肢もある。その場合は lower/P1 inputをtile数分読む費用が加わる。

raw edgeには短い tagged Fox と右qnormから来る有限 stencil がある。六tagの語を数えると、X edgeは13個、Y edgeは11個以下のPB3 regular scatter contributions（相殺前）で、それぞれ全四character×十monomialに散布する。これで source の全108864×241928 matrixを作らず、BとGammaの必要列から physical edge vectorを足せる。ただし一つの Gamma列自体はdense physical vectorになり得る。

physical座標を w 個ずつtileにし、edge values[108864,w]、tree potentials[54432,w]、chord values[54433,w]を作り、全outside Jで五基準列を引けば固定 A packetが得られる。既存 `integrate_tree` は trailing shapeを保つので、このvector/tile積分そのものの数式を既に実装している。`chord_values` も同じ末尾shapeを保つ。一方 scalar `score_array/raw_edge_pullback` のshape guardはbatch/vectorを許さないので、vector原始adapterを「既にある」とはしない。

この方式の主要 decoded temporaryは O((108864+54432+54433+r)*w) bytes＋少数bufferとmapping metadata、disk出力は M*12096である。tileごとに基準五本を引き、canonical row-major packed fileへ配置する transpose/seekと最終full hashを勘定に入れる。全 physical幅で一度にtreeを持てば、potentialsだけでも54432*48384 decoded bytesとなる。省メモリはtile/re-readとの交換であり、単に「treeなので小さい」としない。

Gamma方式は全M個のprimal solveを各列の必要条件から外す代わりに、8059本のvector solve/validationへ移す。**選ばれたpositive列の alpha・ordered P1 ancestry・全96776lower zeroは依然必要**である。packetの列を数値mapとして照合しただけでは literal materialization済みにならない。全列のexplicit alphaを保存する契約を採るなら、Gamma方式でも全M個のprimal solveは別途残る。この二つのreceipt水準を混ぜない。

F7. **実在 API と最小の新接続。** 下表の path はすべて `search/` 配下。読み直した範囲に基づく。producer/checkerは数式・ABI・pinsだけを共有し、新 raw-source/primal/compiled arithmeticは別計算にする。

| 既存 source / 関数 | 入出力・使える範囲 | 新しい接続 |
|---|---|---|
| `d972_r07_section_cochain_oracle_v1.py:317 geometry_inputs(arith,context)` | graph/phi/tag/tree/carryのdictとarrays | lambda-independentなpacket geometry owner、全outside Jの d_e生成 |
| 同 `:632 integrate_tree(next,parent,parent_edge,order,values)` / `:655 chord_values(next,chords,values,potential)` | trailing dimensionsを保つuint8 potentials/chord values | F6のphysical tileを入力するadapterとrow-major出力 |
| 同 `:662 first_independent(tau)` / `:683 solve_five(matrix,rhs)` | tauの独立五行indices / Td=tの5-trit解 | 一回のJと全54428 d_e、全tau零のreceipt |
| 同 `:387 PackedRows(root,descriptor).row(local)` | fullpinしたblobから元local-ID行をdecodedで返す | reader lifetimeを共有するprimal old→new消去、またはphysical RHSのGamma補間。既存`:404 interpolate_rows`はscalar用 |
| `d972_r07_targeted_grade2_owner_generated_join_v15.py:534 _seed_affine_fox(word,images)`、`:763 _seed_evaluate_seed(context,word)` | 非閉signed-word Fox / closed・18整除wordのfull source | Task963のraw SLP、同じ chain/eta、全tag source adapter。closed-only qnormをprefixへ呼ばない |
| `d972_r07_full_origin_refinement_v1.py:348 canonical_index(m,p1)`、`:725 top_row(m,stream,index,node)` | instruction metadata一巡 / 位置付きpacked P1 top一行とrow hash | 一回のindex、h/Gamma cacheとcanonical Ref join |
| 同 `:733 canonical_input(...)`、`:753 subtract_lifts(...,coefficients,reference_nodes,parts)` | full P1一行 / partsをin-place補正しcomponent receiptsを返す | 選択E用。全M回呼ぶと12blobsの全走査もM回になるため、packet向けblock readerは別途必要 |
| `d972_r07_fixed_root_packet_loop_v2.py:666 subtract_p1`、`:719 subtract_lower` | 44seed RHSに一つの読込rowを配る既存例 | NSEEDS/44-seed relationと固定assertionsを持つので54430のdrop-in consumerではない。新block ABIが必要 |
| `d972_r07_actual_root_seed_materializer_v3.py:349 apply_sparse(entries,source_width,destination_width,source)` | iterable tripletsを全走査してdense一行 | 四Bのsum、optional adjacency/tiled cache。単一characterのappend wrapperは使わない |
| 同 `:286 pack/:305 unpack/:320 packed_subtract` | packed型検査、decoded変換、packed AXPY | block/Gammaでも変換trafficを計上。Python entriesを固定9byte triplet相当と見積もらない |
| 同 `:1239 physical_reduce/:1270 normalize_pivot/:1284 update_target/:1301 check_final_separator` | current physical挿入順のsweep、normalize、target delta、全行/両target直接dot | 固定packet origin ID、全offer ledger、all-row EOF、accepted-parentとのthin delta wrapper |
| full-origin `:923 next_separator(m,state,normalized,lead,target,step)` | dynamic physical逆挿入順からfresh lambda | packet stateのgeneration/DERIVED/manifestを扱う小wrapper。旧固定metadataを流用しない |

checker側も frozen full-origin `source_lift(args,streams,cache,reference)` は一行ずつ全lower/topを返し、既存finite27/own forward primitivesを持つ。今回の新 raw-chain scatterまたはGammaを相手側から共有しない。Task960のordinary27 actual source-score経路はscalarであり、独立whole packet mapperは未実装である。

F8. **三候補の比較と採否に足りない最小情報。** 全候補は同じ登録 source/Conn/P1/四Bを保持する。新しい有限幾何表現・cacheを導入することと、登録 sourceを増やすことを分ける。

| 候補 | 今回のsourceの扱い | 主な追加費用/メモリ・I/O | positive接続と終了条件 |
|---|---|---|---|
| complete scalar oracle一回→E一個 | D全体を一つのlambdaで完全テスト。非零なら一つだけ | Task959のfresh4 roots、P1 cache292444992を一巡、source dual interpolation/全8059dots、scalar edge108864/chord54433。E一個のraw word/source/primalとselected lifts | zeroならConn前提付き完全separator。非零はE後の一pivotであり反復回数は未知。same-word positiveはTask958 |
| 現 full-origin loop | 44 root seeds＋8059×4 root actorsを全四characterでscan。同じ宇宙の現在のroot roster | 各scanでfresh roots/children、P1 cache一巡。producer lower I/Oはそのscanのactive character数 a に対し a*Lblob、5 bodiesもa回。checkerは自身のbatch方式。selected materializationと全current物理sweepが各追加に必要 | root-origin EOFをDの完全separatorへ昇格しない。追加後のlambdaで再scan。full-originの観測26段/target変化回数から残反復を予測しない |
| 固定complete packet | Dの54430基底をlambda-free Aへ送る。新sourceなし | 基本方式はblockごとのprimal/全lower/top、optional h cache。compiled方式はGammaのvector solveと全8059vector等式、tiled edge/tree、packet658385280 bytes＋physical reduction。F5–F6の再走査/pack/unpack費用 | 完全EOFなら線形所属か全rowseparatorを決められる。positive列のliteral/primal再生と最終same-word readoutは残る。行数はrank/pivot数ではない |

固定packetは同じlambdaの再scanを避けられるが、いま必要な一個のviolating row以外も多数実体化する。complete scalar oracleはA行全体の代わりに一つのdualで済む。どちらが速いかは上の式だけでは判定しない。

採否に必要な最小追加観測は、(i)すでに予定されたA–Dの各stage実時間/peak memory/bytesと全配列照合、(ii)非零時のE一個におけるactual tree depths/word長上界、alpha support、source/primal/top/B/物理消去の時間・読込bytes、(iii)静的source-basis pivot部分の実 E_tri と四Bの実 entries/support、選んだblock/tile幅でのcache作成・full equality・row-major書出しの測定である。これらを全packet/収束の前提無しで比較すればよい。本便はその試験を発注せず、旧suiteや別sourceの追加も要求しない。compiled Gammaは採るなら新しい限定実装・独立照合が要る任意案であり、進行中Task959/960のrelease gateではない。

AUDIT_964_VERDICT: PAPER_EQUIVALENT_FIXED_COMPLETE_PACKET_FEASIBLE; PRIMAL_OR_VECTOR_SECTION_COST_EXPLICIT; PERFORMANCE_AND_SAME_WORD_POSITIVE_CONSUMERS_PENDING; NO_NEW_SOURCE_OR_RUNTIME_CLAIM; verified=false
