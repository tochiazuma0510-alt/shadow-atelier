# Task988 — 固定 lambda の失敗弦 batch の数学契約

F0. **条件付きで実装可能。固定lambdaによる選定と、順序付きの独立性判定・最終Separatorを分ける必要がある。** 先頭非零32弦をそれぞれ合法語化する数学に、第一失敗弦だけに成立する制約は見つからない。ただし各行が旧spanの外であることから相互独立は従わず、32行の追加や速度改善は保証されない。以下の新batch型を採用し、凍結one-row型へ偽装しないことが必須である。最小案は、実親64段を不変に保つ別の固定snapshot packetと、順序付き消去・一回の最終Separatorを担当する小さいconsumerである。実装・GHA・新CV9の完了判定ではない。

Task988、`provenance/rulings_2153_2154_snapshot_20260906.md`、`docs/notes/cegar_resume64_cv9_reading_v1.md`、対応expressを全文読了した。v542/v543/v546/v547/v548も全文読み直し、既存E・継続器の関連sourceとreply964/976の該当数学を照合した。変更は本返信だけ。987、公刊source/workflow/返信、v220は変更していない。ローカル数値/Python/import/AST/GAP、network/git/credentials、新agentは使用していない。

F1. **観測と外挿を分ける。** 2153は候補9977040548と診断9977050602のReleaseミラー、2154はrun33990567016/1の64段/rank1450/gen8155をcross-checked限定8条で正式受理した裁定である。Separator・UNKNOWN_CAP・grade2 NOT_DECIDED・A0 actual0/1を維持する。限定は、当該64周回、current最終1450のoracle未計算、character0だけが情報的だった実値、未発火auxを含むsource内訳、signed literalと物理同値の区別、DERIVED rho2、保持TCBと第三被覆不足等を含む。新batchはこれらを遡及閉鎖しない。

各段が全54433弦を評価したことと、選定がその先頭失敗弦一本だったことを区別する。35992–36549の失敗総数、先頭indexの後退、target.scalar=0、各実時間は正本の観測であり、本監査は再計算していない。失敗総数に幾何的距離や独立確率の意味を付けない。rank約55000という一定率外挿はF10の有限次元上界を越えるため、完了に必要な段数・時間の予測として採用できない。rootの一回限りの実64親→絶対96の計測対照と、985の同語readoutは本batchの数学・性能判定と別であり、その未観測結果を埋めない。

F2. **固定する数学対象。** 以下はすべてk=F3上、現Q0/Q2・Delta・四character・同P1/Conn/Task712・同source-mapのままである。物理行とP1行の記号を分ける。

```text
P = k^48384,  Lphys = k^32260,  Lsrc = k^96776,
Psi:D -> W2 onto,  D=ker(tau:Z -> k^5) direct-sum k^2,
Z has the full 54433 fundamental cycles z_e,
pi:W2 -> W1 onto,  dim W1=8059,
s(b_i)=tilde_b_i,  pi s=id,  R=id-s pi,
H(b,z)=sum_(a=0..3) B_a(z[a]),  (G-H)R=0,
M2=span(Conn)+G(ker pi),
A=G R Psi=H R Psi:D -> P.
```

旧physical basisを順序付きB0=(p_0,...,p_(r-1))、そのspanをS0、旧target remainderをt0とする。開始条件はConn⊆S0⊆M2、実lambda0(S0)=0、lambda0(t0)=1と、元rho2−t0のaccepted target identityである。r=1450/generation8155は今回の実親であり、一般契約の固定数にはしない。現在lambdaを使い、四q_a=B_a^*lambda0、全4×8059 lift値、全8059の<kappa,b_i>=sum_a<q_a,z_i[a]>を照合する。するとv548(2.3)/(5.3)から

```text
lambda0 A(z,eta) = f(z)+b_aux eta       ((z,eta) in D).  (988.1)
```

raw edge/chordは一般にはDの合法入力ではない。fの全108864辺へのextensionとcarryを同じ親・右Cayley辺/左Fox/tag/qnorm規約へ結び、(988.1)を合法な組合せ上で使う。Connをsource次元や8059等式だけで代用しない。

F3. **任意の失敗弦に同じ六cycle構成が使える。** 固定tree/chord rosterと、tauが最初に独立となる五本J=(e_1,...,e_5)を固定する。Tの第j列をtau(z_ej)とし、Tが可逆であることを照合する。fのtree potentialから全弦値h_e=f(z_e)を得て、五本をfitしたaを使う。

```text
T^T a = (h_e1,...,h_e5)^T,
d_e = T^-1 tau(z_e),
k_e = z_e - sum_j d_e[j] z_ej,
rho_e = h_e - tau(z_e)^T a
      = h_e - sum_j d_e[j] h_ej.                       (988.2)
```

ここでrho_eは弦残差で、元物理target rho2とは別記号である。全54433のrho_eと二b_auxを評価・EOF照合してから、既定roster順の先頭min(32,非零件数)本を選ぶ。各選定eについてtau(k_e)=0、eta=(0,0)、lambda0 A(k_e,0)=rho_e∈{1,2}。式は任意のeに成立し、eがfirst_failedであることを使わない。五基準弦の残差は必ず零で、選定非零弦はJに属さない。

実source `d972_r07_section_cochain_oracle_v1.py:722–790` は全残差identity/EOFを確認した後、745–755行で同じTd=t、六項、tau零、scalar一致を作る。`failed[0]`は選択方針であり合法性の前提ではない。継続Pの `current_tree_cached:1229–1247` も固定tau/Jと現f/fitの全配列を保持している。新batchはこの全配列から各候補の新witnessを作り、既存一個のwitness hashを別eへ流用しない。零係数を含む六項の順はfailed eを先頭、その後J順で固定する。

aux分岐は省けない。既存 `classify_complete:735–742` は非零auxを先に一件選ぶ。本候補の「失敗弦roster先頭≤32、弦失敗零なら先頭非零aux一件」という方針は、その優先順位を変える新契約として明記する。b_auxも非零の時に弦を先に選んでも、各弦のeta=0なので(988.1)–(988.2)は成立する。弦失敗零・b_aux非零ならc_xまたはc_y一件へ必ずfallbackする。未実装ならその枝はUNKNOWNであり、完全性・有限前進の主張をその枝まで広げない。旧aux優先を保持する別方針も数学上は可能だが、両方を同じselectorと称さない。弦失敗零だけでCOMPLETE_ZEROとすることは不可。

F4. **個別違反と相互独立の反例。** q_i=A(k_ei,0)と置く。lambda0(q_i)≠0かつlambda0(S0)=0なのでq_i∉S0である。しかしS0=span(e1)、lambda0=e2*、q1=e2、q2=e1+e2なら双方のpairingは1でも、S0+span(q1,q2)のrank増分は1だけ。S0に四つの座標を持たせ、32個の異なるs_i∈S0についてq_i=e5+s_iとすれば、32行が異なりすべて違反しても増分1である。これは紙の反例で、ローカル計算ではない。

k_e自体はK=ker tauの独立な基底の部分集合である。実際、全e∉Jのk_eにはそれぞれ固有の非基準z_e係数1があり、これら54428本はKの基底となる。だが線形写像Aがこの独立性を保つとは限らない。「独立なcycle」や「異なる失敗弦」を「独立なphysical行」と呼んではならない。

さらに、batch内で先に採用した行を引いた残差にはlambda0=0の独立行もある。S0=0、lambda0=e1*、q1=e1+e2、q2=e1+2e2なら双方のraw pairingは1だが、q1を引いた二本目はe2で非零、lambda0(e2)=0である。この行を落としてはならない。凍結EのP `one_physical_row:823–826` とC同関数 `1022–1025` の「old lambdaによる消去後scalarが元非零scalarと同じ」というgateは、消去対象全spanをold lambdaが殺す一行更新専用である。新batchの二本目以降へこのassertionをそのまま適用できない。

F5. **各候補を実Omega語からsource-zero行にする契約。** 各k_eに対して、treeのSchreier語W_eを先頭、W_ejのsigned係数をJ順に置く。基準五語は一般には合法でなく、個別にOmegaへ修理してから引くのではない。組み合わせたw全体のtau零から、v546(2.3)/(3.2)によりw∈N0かつepsilon(w)∈6Z²を得る。v547(4.2)を固定順に使う。

```text
C_e = w (r_x^3)^(-A(w)/6) (r_y^3)^(-B(w)/6)
        [r_x,r_y]^sr(omega(w)),  sr(0,1,2)=(0,1,-1).   (988.3)
```

C_e∈Omega∩[F,F]、J_Q2(C_e)=k_e、nu(C_e)=0が全選定eに成立する。A/Bと/6はordinary integerで、omegaも同じSLPの積/逆/整数冪再帰から読む。v548末尾の裸のomega表記は2150/2151のsigned literal規約で読む。語の同一性・hashと、別代表でも同じ物理行になるという命題を混同しない。一般OmegaのFox像が零という主張は使わない。auxはc_x/c_yの九乗語とeta=e_x/e_yを保持し、exact-zero修理でetaを消してはいけない。

EのP `selected_raw_word:390–483` とC `raw_materialization:757–825` を再読した。実tree/SLP全EOF、raw rootのQ0/Q2 endpoint、三修理語のFox零、同じ六cycleのchain、boundary/carry零、同scalar、六tagの直接SLP Foxとsourceを確認する経路であり、first eだけに制限した算術はない。新batchでは各候補のgeometry/source/layout/witness参照を正しく独立に結ぶ必要がある。

u_i=Psi(k_ei,0)またはPsi(0,eta)をfull filtered sourceで作り、各候補ごとに新しいraw partsから

```text
pi(u_i)=sum_l alpha_il b_l,
v_i=u_i-sum_l alpha_il tilde_b_l,
pi(v_i)=0 on all96776 source-lower coordinates,
q_i=G(v_i)=H(v_i)=sum_(a=0..3) B_a(v_i.d2[a]),
lambda0(q_i)=rho_ei (or selected b_aux).               (988.4)
```

を照合する。source lower零とell=ell1 piを結んで全32260 physical lower零を得る。混合raw sourceに四Bだけを適用してはならない。Pの `primal_section:646–707` はoldの元embedded lead昇順→new ownerごとの元lead昇順、共有auxと全四d1 companionを同係数で引く。`corrected_source:733–781` はraw copyからcanonical liftを一回だけ引く。候補間でmutable work/alpha/partsを使い回して前候補の補正を混ぜない。全8059 alpha、primal eventsと元row ID、全P1 instruction/cache/indexのhash/EOF、選定Refを保持する。

P1語因子はprimal event順に指数−sr(alpha)で積む。同じordered rootをordinary mod54で評価し、各pairはboolでない整数0..53、18整除は0/18/36、nuはその整数商mod3である。18をF3内で割らない。source補正後は既存contractのnu=(0,0)を全source auxと照合する。rawのexact epsilon零から、P1やphysical因子を加えた最終語のordinary epsilonまで零とは推論しない。

F6. **順序付き消去・literal・targetの符号。** 各q_iのrecipeはS0とlambda0に固定したまま、消去だけをB0と先に採用した新normalized行に対して行う。p_jはその時点の全physical basisを表す。

```text
r_i = q_i - sum_j c_ij p_j,                            (988.5)
r_i=0: dependent offer, no pivot/target/rank update.
r_i!=0: lead_i=first_nonzero(r_i),
        sigma_i=r_i[lead_i]^-1 (=r_i[lead_i] in F3),
        n_i=sigma_i r_i;  append this monic row.
```

実基底はphysical insertion順のまま全行を一巡し、全旧lead零を確認する。数値lead順へ並べ替えたり、未知の先頭leadを見つけて消去を打ち切ったりしない。凍結 `d972_r07_actual_root_seed_materializer_v3.py:1239–1298` のphysical_reduce/normalize_pivot/update_targetはこの契約である。新rowはそれまでの全pivot座標で零・自身のleadで1となる。rank/genの増分は非零残差の採用数aだけ、offer数kとは別。採用順j=0,...,a-1についてglobal row ID=r0+j、offer用logical generation=g0+j、batch blobのlocal offset=j*12096を区別し、final generationはg0+aとする。

選定scalarをh_iとすると、正しいold-lambda関係は

```text
lambda0(r_i)=h_i-sum_(new p_j) c_ij lambda0(p_j),
lambda0(n_i)=sigma_i lambda0(r_i).                     (988.6)
```

である。後二値は零でもよい。lambda0(q_i)≠0と、final Separatorの新span直交は別receiptにする。

source補正語をV_i、既存normalized physical行の語をL_jとすると、新行のliteralは、同じ消去event順で

```text
L_new = ( V_i product_j L_j^(-sr(c_ij)) )^sr(sigma_i). (988.7)
```

全因子は同じOmegaのaccepted ancestryを持つので、full physical readoutは(0,n_i)となる。旧Conn由来因子はphysical lower零でもsource lower零とは限らないため、(988.7)のsource lower零はNOT_ASSERTEDを維持する。依存offerでもV_iと全c_ij・r_i=0を保存するが、その語を自由群のidentityと呼ばない。行を追加せず、後続targetにも直接は使わない。原rowと同値な縮約recipeを残す場合も参照元は落とさない。

targetは新採用行の順に、t_beforeの実lead成分theta_jを使う。

```text
theta_j=t_before[lead_j],
t_after=t_before-theta_j n_j,
t0-t_final=sum_(accepted j) theta_j n_j.               (988.8)
```

theta=0も正常なrank増加であり、行・祖先を捨てない。selected scalarやsigmaをthetaの代用にせず、sigmaをtargetに再乗算しない。元rho2へのaccepted identityは

```text
rho2=t_final+sum_(old j) beta_j p_j
                  +sum_(new j) theta_j n_j.            (988.9)
```

となる。rho2−t_finalを表す累積correction語へ追加する因子の符号は+sr(theta_j)であり、行の消去因子の負号とは違う。残差側を語として表す別契約なら負号になる。どの量をword rootが表すかを明記し、既存printed物理規約を変更しない。2154で非空虚に判別された(988.8)を、新batchでも全採用行の実trit identityとして照合する。

F7. **最終lambdaと完全零を分離する。** batchの線形判定後、t_final≠0なら新全basisからlambda_starを一回作り、全旧rowと全新normalized rowへのdot零、t0とt_finalへのdot1を直接確認する。逆physical insertion順のback substitutionが使えるが、旧Eの「一行だけ増える」wrapperを複数行と偽らない。(988.9)からlambda_star(rho2)=1はDERIVEDとする。新lambda_starはS0も消すため旧target identityに適用できるが、lambda0の各世代dot1を混ぜた議論は不要である。

t_final=0ならtyped LinearMembershipCandidate・lambda=nullと、全target/literal係数を出す。これは同一語11slotの完了でも、当該gradeの正式MEMBERでもない。新batch Refとtarget ancestryを読むpositive consumerは別の明示adapterが必要で、公刊982/983の旧one-row/親rosterへ未対応batchを通してよいとはしない。新語のendpoint・normalized pair・全11 typed slot/printed/full filtered readout・side/localizationの条件を保つ。

lambda0は第一採用行へのpairingが非零なので、採用後spanのSeparatorではない。batch末尾に残ったlambda0の古い零・非零oracleをlambda_starのcurrent oracleと表示してはならない。t_final≠0のbatch終了はBATCH_PIVOTS/UNKNOWN系であり、次の完全判定にはlambda_starを結んだ新しい全oracleが必要である。COMPLETE_ZEROは同じcurrent lambdaについて全54433 residual零かつb_aux二成分零、全8059/source-map/Conn/全row/targetの受理が揃う別終端に限る。この負定理はreply976の条件付き定理を維持し、positive一語11slotを自動gateに足さない。

F8. **最小receiptと独立checkerの必須式。** 次の新領域を別schemaで登録する。旧snapshot startのcopyに新rankを書き足す方式は禁止する。

| receipt | 必須の結合と数値 |
| --- | --- |
| batch-start | exact accepted-parent artifact/HEAD/全64prefix、元physical owner/source/start/fixed、現全basis/target/lambda0、P1/Conn/Task712/Q0/Q2/source pins、ordinary k=32、aux優先方針、partial commit方針、資源枠。新batch owner/sourceは元のものと別字段 |
| selection | selection_snapshot_id、全q/P1/chi/kappa/score/f/b_aux/tree/tau/J/fit/residual配列とdtype/shape/hash/EOF、非零全件数、先頭kのroster indexとedge ID、全eの(988.2)、各新witness hash。k件見つけた時点でEOFを切らない |
| offer[i] | batch IDと候補ordinal、同selection lambda/hash、六cycleまたはaux、同SLP/実endpoint/Fox/eta/omega/整数指数、source全成分、alpha[8059]/primal/P1 Ref、全96776零、四Bの和・raw48384 row・lambda0(q_i)と(988.1)/(988.4)。候補ごとにfresh input |
| reduction[i] | 全prior physical basis ID/hash/順、係数と(988.5)、実zero/dependentまたはlead/sigma/normalized/新global ID、(988.6)、(988.7)のexact ancestry。dependentにも完了receiptを付ける |
| target/final | 各theta/前後target/全(988.8)、(988.9)の元rho2親列、accepted数/rank/gen、final全basis/両targetのdirect pairingまたは零target。selection lambdaとfinal lambdaを別に型付けし、current oracle未計算をnullとして保持 |
| durable state | processed offer cursor・採用cursor・全phase EOF、prior batch/parent/commit hash、complete prefixと未完diagnostic、入力/元64prefix前後不変、実source/launch/runtime/資源/時間/I/Oとchecker全新prefixの比較範囲 |

独立CはPのPASSフラグや選定scalarだけを信用せず、自系の全oracleと全8059等式、各Td=t・tau零・scalar、各語/source/P1/四B、全相互消去と依存判定、target delta、final全row pairingを比較する。すべてのselected offerをraw vectorまで確認し、採用された行だけを再生して依存行の捨て方を未照合にしない。旧64のaccepted実Cと全bytesを親前提として保持できるが、新lambdaでの全旧行dotは省けない。旧suiteの再走を一律に追加する必要はない。

各系統内で固定geometry/T/P1 readerやoperator cacheを共有することは可能だが、新P/C間で消去・raw-source・primal算術をコピーして独立と称さない。共通に渡すものは本数学/型/選択順とpinsのみ。継承envelope/packed projection/sparse adjoint等のload-bearing TCBは明記し、新batchの配列一致やmetadata wrapperで第三独立性へ昇格しない。

F9. **保存移行は新packet＋consumerを最小案とする。**

| 案 | 旧64prefixとstateの扱い | 追加する契約 |
| --- | --- | --- |
| 固定snapshot packet＋batch consumer（推奨） | 実親candidate全体をreadonlyで保持。packetは選定snapshotの全oracleと候補recipe/行を持つ。consumerは別rootで旧basis＋packetを順序付き消去 | 新packet/offer/reduction/commit schema、final multirow Separator、親64へのthin delta。幾何的全54430列を作るreply964のcomplete packetとは異なり、選定≤32だけ |
| 新continuation型 | 旧64をimmutable legacy prefixとして参照し、新epochsにselection snapshotと複数offers/採用rowsを置く。epoch末尾だけcurrent Separatorを公刊 | phase/HEAD/result/invocation/cursor/positive Refの新ABI。batch epoch数・offer数・採用数・累積physical countを分離し、P/C全tailを改版監査 |
| 旧one-row型のままsnapshot/lambdaを使い回す | 旧stateと異なるspanに古いlambdaをcurrentとして挿入する | 不可。P `check_current_witness:1039–1045`、`restore_physical:1197–1226`、`step_manifest:1395–1410`とC one_physical_rowの意味に反する |

推奨案でもpacketだけで新rankを公刊しない。各完了offer phaseと消去receiptをdurableに保存し、物理HEADの外のstaging cursorから再開する。selection snapshotのbasis/親list/lambda/targetはimmutableな別値とし、深いlist/array aliasを通じて後続row追加が過去startのsealを変えないようにする。旧source/owner/HEADを新実装のhashで書き換えず、新consumer source/ownerとunderlying physical parent identityを区別する。

最小の通常commitは、選定k件の完了・依存判定・target更新・final SeparatorまたはLinearをすべてsealしてから、manifestを先にdurable publicationし最後に新HEADをatomicに更新する一取引でよい。中断時、最後の公刊HEADはそのままで、完了phaseは再利用可能なcheckpoint、未完payloadは明示diagnosticとなる。これならSeparatorが存在しない中間spanを旧型で公刊しない。

資源停止時に完成prefixだけを早期commitしたい場合も可能だが、事前に許可したflush境界でprefix採用行の全算術・target・新final Separatorを完成させてからに限る。未完一行を数えず、selected_count/processed_count/accepted_countとpartial=true・UNKNOWN_RESOURCEを記録する。処理済offerの依存証明を含むprefixを凍結し、残る候補のselection lambdaは元lambda0のまま、次の消去spanだけを更新する。flush用final lambdaの計算をselection lambdaの更新と呼ばない。Separatorを完成できなければ新physical commitはせず旧HEADを維持する。再開一回あたりのrank増加は保証せず、完成非空batch全体の保証だけをF10で述べる。残りを破棄して新selectionへ移るなら別batch IDとし、元k件全部の完了を称さない。

旧64全file/dir/hashと旧C64の全dictをそのまま保持する。新global pivot IDとpacket内offset、元generationとnew offer ordinal、raw word IDとnormalized row IDは別の型にする。HEAD外tailを自動採用せず、同snapshot/source/prefix hashに対してだけresumeする。継承PhaseStoreの「全payload→manifest→publication→HEAD」という順序（P:327–357/1423–1444）は参考になるが、九phase一rowという旧rosterを複数offerに再解釈しない。

F10. **有限前進はrankで証明できるが、失敗総数の単調減少は証明できない。** 完成した非空batchの全選定行をq_1,...,q_kとすると、順序付き消去後は

```text
S_final = S0 + span(q_1,...,q_k),
a = dim(S_final/S0),
1 <= a <= min(k,48384-r0).                             (988.10)
```

第一候補はlambda0(q_1)≠0なので旧span外、少なくとも一行が採用される。全選定行の消去を終えたとき、依存offerもS_final内というreceiptを持つ。全候補が依存とされたなら、非空違反batchの開始前提・算術・state bindingのいずれかが壊れており、正常なrank0成功ではない。部分resumeの残りがすべて依存ということはあり得る。

同じgeometry/J、Psi、P1 section、Bを固定する限り、q_e=A(k_e,0)自体はlambdaに依存しない。fitやkappaがlambdaごとに変わっても合法入力上は(988.1)が同じlambda(q_e)を与える。従ってbatch完了後のSeparatorは、採用・依存を含む選定全q_eを消す。その後さらにspanを増やしても、この選定集合の方向は再び違反しない。一方、以前のlambdaで偶然零だった未選定弦は新lambdaで非零になり得る。失敗総数、先頭失敗index、target supportは単調量ではなく、「先頭index以下を永久に消化した」とも言えない。

十分な資源で各oracle/batchが完了し、非零auxも上の総分岐で処理するという条件の下では、非終端の各非空batchでrankが厳密に増える。Pの次元は48384だから、現1450からの独立追加総数は最大46934。Separatorが存続する間はrank≤48383で、rank48384なら任意targetはspan内となりLinearへ移る。あるいはそれ以前に現在lambdaの完全零oracleへ進み得る。この有限性は実資源内の終了、32倍の前進、target到達、行列の真のrankを予言しない。v546の12092というsource grade上界をConn込みM2のrankへ置き換えない。

kはordinary正整数32としてfreezeし、候補数不足ならmin(32,実非零件数)、aux枝は登録した一件とする。32はmaterialization/処理の上限であってoracle探索宇宙の上限ではない。未知の中断・k消費・absolute cap・候補全依存をNONMEMBERへ昇格しない。性能比較ではoracle回数、materialized/processed/dependent/accepted数、各段の実時間/peak memory/read/write bytes、同じ前後lambdaでの全失敗件数を別に保存する。同lambdaでoracleを一回にできても、各語・P1/primal/四Bとbatch内消去の費用は残る。成功したbatchで何行採用されるか、共有cacheがどれだけ効くかは新しい実測事項である。

F11. **最小の新API分割と拒否条件。** rootが独立P/C作者へ渡せる共通契約は次の五つで足りる。各実装のアルゴリズムは別にする。

1. `freeze_selection(parent,k,policy)`：現lambdaの全oracleを完成し、全54433/2のEOFから固定順の候補manifestを返す。旧current oracle=nullなら新しく計算する。
2. `materialize_offer(selection,ordinal)`：同候補のraw Omega語、full source、primal/P1、四B raw行とlambda0 scalarを返す。S0/selectionを変更しない。
3. `reduce_offers(base_basis,ordered_offers,base_target)`：全旧basis＋採用済行で(988.5)–(988.8)、依存も含む全offer ledgerとfinal targetを返す。current Separatorは途中で要求しない。
4. `finalize_batch(base,ledger)`：新全basisのSeparator/両target dotsまたはLinear、DERIVED親列、exact new-row/literal refsを完成する。
5. `commit_or_resume(parent,selection,complete_prefix)`：F9の新型・cursor・atomic publication・全保存不変と、独立checkerによる全新prefix比較を結ぶ。

必須拒否は、旧lambda/snapshotの混合、T/fitの向きやJ順の混合、全EOF欠落/aux欠落、非零集合の先頭k不一致、同候補IDの重複、source補正の二重適用、四characterの省略、源96776と物理32260の混同、依存rowの無条件append、zero-lambda residualだけを理由に独立rowを捨てること、sigma/thetaの混同、別語/別Refでの同一語主張、未完phase/HEAD外tailの昇格である。新GHAでの最小境界例としてF4の依存二行とlambda0残差零の独立二行、非零thetaの符号反転、末尾弦だけ非零/auxだけ非零、raw partsの候補間alias・過去snapshot親listのalias、完了manifest前後の中断を実production helperに接続すべきである。本便でその実装・実行をしたとはしない。

F12. **読取源と最終判定。** 以下は静的に再測定したfile全bytes/SHAで、行番号はこの版へのもの。裁定snapshotは1414 B / 24601b91bbc45149f15409df13016f5ee54f5efb86a0ac60ae92fa17d8e84b03、CV9正本は29727 B / 2e64caa0d9f5fe03baaa556fe2e45107a04b60d6e298ade768f5b27b080b65a6、expressは3980 B / 15886fa2f6984946a57231787d327bf5000fcadf70eb8af1d545623f4e796e26であった。

| source | bytes | SHA256 |
| --- | ---: | --- |
| search/d972_r07_section_cochain_oracle_v1.py | 73290 | 4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb |
| search/d972_r07_selected_cycle_materializer_v1.py | 88929 | 4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3 |
| search/check_d972_r07_selected_cycle_materializer_v1.py | 103757 | a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4 |
| search/d972_r07_complete_oracle_cegar_continuation_v1.py | 126940 | 67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c |
| search/check_d972_r07_complete_oracle_cegar_continuation_v2.py | 129557 | e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3 |
| search/d972_r07_actual_root_seed_materializer_v3.py | 86643 | 36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332 |

判定: FIXED_LAMBDA_BATCH_MATH_CONTRACT_PASS; DISTINCT_VIOLATIONS_DO_NOT_IMPLY_MUTUAL_INDEPENDENCE; ORDERED_RANK_FILTER_AND_SEPARATE_FINAL_SEPARATOR_REQUIRED; FULL_54433_PLUS_TWO_AUX_UNCHANGED; VERSIONED_PACKET_OR_CONTINUATION_AND_DURABLE_PREFIX_REQUIRED; IMPLEMENTATION_GHA_CV9_PERFORMANCE_PENDING; GRADE2_NOT_DECIDED; FULL_A0_NOT_DECIDED; verified=false.

AUDIT_988_VERDICT:
