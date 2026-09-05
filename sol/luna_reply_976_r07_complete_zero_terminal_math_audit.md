# Task976 — complete-zero の負終端を当該 grade へ結ぶ条件

F0. **条件付き負定理は成立する。positive 同一語11slotを負判定の追加gateにはしない。** Task976、v548/v543/v547、reply957/958/964/970/973を全文読了し、2144の符号付きliteral規約と2131/2138/2143の限定を保持した。後着の正式reply972も全文読了した。公刊973の清書時点の記述を遡及変更しない。

開始時に受領した状態は、run33984832010/1、launch `b8c9e95ddd0183d9e43b7fcc961cb251fdaea13e` のcap1/resume32 success、全prefix checker中まで。その後rootから、独立checker stepが19:09:25Zにfailure（754秒）、source/parent/output不変と診断保存はsuccess、diag9975236748を回収中と連絡された。本便は診断本文を未読で、原因・新rank・producer terminal・complete-zeroを補わない。実checker最終PASSは成立したとしない。受理済み起点はrank1386/gen8091。変更は本返信のみ。ローカル数値/Python/import/AST/GAP、network/git/credential、追加agentはない。

以下、P/Cは新継続器のproducer/checker、Oはそのcheckerが使うoracle checker v2を表す。実bytes/SHAを再確認した。

| 対象 | bytes | SHA256 |
| --- | ---: | --- |
| P `search/d972_r07_complete_oracle_cegar_continuation_v1.py` | 126940 | `67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c` |
| C `search/check_d972_r07_complete_oracle_cegar_continuation_v1.py` | 120245 | `8c000f9b49d04447a09c701daf5907a35b7f2e883f1e36747308a6d4ded29b1f` |
| workflow `d972-r07-complete-oracle-cegar-continuation-v1.yml` | 61275 | `9f751fe1ea21d16b7758f9832d2dd091b73f0796128ceea505c8975031c096c1` |

reply973も31678 bytes / `4177963c096cc2e7f6967c31db008c08bc1c5a855b113e2c0279eb7f951fb8dd`のまま。reply972は13281 bytes / `047ac4378d25ac660233011fd89eccdb821261a66caa0e04d16e665b6651f8e9`。以下の行番号はこの凍結sourceに対するもの。

F1. **必要な負命題と保持前提を分離する。** k=F3、Pphys=k^48384とし、v548(1.1)–(1.4)の同じ有限対象を使う。

```text
Psi:D -> W2 onto,   pi:W2 -> W1 onto,
W1 has the complete independent basis b_i (i=0,...,8058),
s(b_i)=tilde_b_i,   pi s=id,   R=id-s pi,
ell=ell1 pi,   G-H=C_lower pi,
H(b,z)=sum_(a=0..3) B_a(z[a]),
M2=G(ker ell)=span(Conn)+G(ker pi).
```

同じcanonical liftのtopをz_iとする。現lambdaを固定し、全四characterについてq_a=B_a^*lambda、chi_i=sum_a<q_a,z_i[a]>を計算する。全8059等式<kappa,b_i>=chi_iが成立すれば、kappaのW1への制限はlambda Hsである。したがって、すべてのu∈W2について

```text
F_lambda(u)=lambda H(u)-kappa(pi(u))
           =lambda H R(u)=lambda G R(u).                (976.1)
```

最後の等式で使うのは(G-H)R=C_lower pi R=0であり、H(tilde_b_i)=G(tilde_b_i)という一般には偽の等式ではない。source lower全96776座標とphysical lower32260座標を同一視しない。sourceの共有aux8をcharacter別に複製しない。実Task712四Bが純homogeneous restrictionであることはv530(2.1)、P1とそのliftがsectionを与えることはv548(1.1)の保持前提である。

Psi ontoとR(W2)=ker piにより、F_lambda Psi=0ならlambda G(ker pi)=0。ここへ**同じlambdaが完全Connを消す条件**を足して初めて

```text
lambda(M2)=0.                                         (976.2)
```

が従う。Connの仕事は、canonical P1の全physical lower関係のtop像を尽くすこと（v530(3.1)、v535(1.1)、v543(1.4)）。sourceの次元、現在の追加rank、あるsubsetのConn行数で代用できない。一方、C_lowerの全表やv543のphysical multiplier muを新たに数値出力する必要はない。これがv548 Theorem3.1の正確な射程である。

F2. **全有限EOFが(976.1)の全域零を与える理由。** Z=ker(partial:k[Q2]^2→k[Q2])、tau:Z→k^5 onto、D=ker(tau)⊕k^2である。固定marked Q2の全54432頂点/108864正辺、connected treeの54431辺、残りの全54433 fundamental cycle z_eを使う。v546の三rotation carryは実Q0のmod9 markingから整数除算で作り、二exponent行を合わせる。五行という数だけで法的kernelを認定しない。

同一source-mapのraw-chainへの線形extensionが

```text
(F_lambda Psi)(z,eta)=f(z)+b_aux eta   for (z,eta) in D
```

を満たすことを要求する。raw chord自身は一般には非合法であり、その個別値をlambda G Psiと読み替えない。reply957 F4の右Cayley辺、左Fox prefix、六tag、右X/XB qnorm、degree0/1の項、二etaを含む同じextensionであればよい。

tree potential pをfから積分し、r_e=f(e)+p(tail)-p(head)、t_e=tau(z_e)を全chordで作る。五つの独立t_eでa∈(k^5)*をfitして、全54433のr_e-a t_e=0とb_aux=(0,0)を照合する。z_eはZの基底だからf|Z=a tau、従ってfはker tauを消す。これがF_lambda Psi=0であり、(976.2)へ届く（v543 Theorem3.1、v548(5.4)）。f自体が零である必要はなく、coboundaryとcarryの線形結合でも正しい完全零証明である。

reply964(964.1)の54428 legal cycle＋二etaの全packetを物理化して消す方法と同値だが、そのpacketやGammaの新実装は必要ない。根拠は全54433の有限基底等式であり、少数sample、残差度数の形、ROOT_ORIGINS_ZERO、cap到達、未完cursorではない。この有限Dを超えるquotient、別H、別lower-state、無限cofinal族へ射程を広げない。

F3. **DERIVED rho2は、最後のlambdaを固定する帰納で正当化できる。** 受理済み起点までの全normalized physical行をP_i、起点剰余をr_0とする。accepted target親列は、同じ元rho2と行に対する

```text
rho2-r_0=sum_i beta_i P_i
```

という線形identityを保持する。base/seed30/seed34/packet三段/refinement26段/external-eを含む同じ親列であり、原rho2のpacked SHAは `b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e`。新j段のnormalized行をN_j、plain target.scalarをt_jとして、実target更新が

```text
r_(j-1)-r_j=t_j N_j
```

を満たすなら、任意の完成m段について

```text
rho2=r_m+sum_i beta_i P_i+sum_(j=1..m) t_j N_j.         (976.3)
```

最後のlambda_*を一つ固定する。lambda_*が全P_i/N_jを消し、lambda_*(r_m)=1なら、(976.3)へ適用してlambda_*(rho2)=1となる。各世代で異なるlambdaのdot1を無条件に連鎖するのではない。最後の全row sweepがその誤りを防ぐ。t_j=0も合法で、scaleをもう一度掛けず、target.scalarとselected.scalarを取り違えない。

C:605 `PhysicalState.measure` は全rank行の直接dot、前/current targetの直接dot1を測る。C:624 `attach` はnormalized row/rolling/offer/rank/target親hashを結び、C:659 `derived` は元rho2 hashと名付き親列・上記三種のidentity規約を保存する。新段のtarget算術はC:996→凍結E checker:1020 `one_physical_row`→`check_d972_r07_actual_root_seed_materializer_v3.py:571 next_target`で、old.copy()からscalar×normalizedを引く実処理に接続される。C:1096以降は全新段を初めから再計算し、最後にC:1142のmeasureで同じlambdaを全行に戻す。

**hash列だけで(976.3)を証明したとはしない。** 新段は実再計算、起点以前はaccepted arithmetic identityを前提とする。原rho2は新runでは直接読まれないため、`mode=derived/value=1/original_rho2_directly_read=false`が正しい表示である。DERIVEDは数学的に無効という意味ではなく、この明示前提付きの帰納を意味する。元targetと親identityが未受理なら、現在剰余のdot1だけで元targetの負判定へ進めない。

F4. **凍結checkerの実gateは負命題へ接続される。** source上の確認であり、本runの実PASSを宣言しない。

| 数学条件 | 実gateと比較対象 |
| --- | --- |
| current qと全8059 section等式 | C:216–302 `roots_and_values/section`。四B pullback、全4×8059 P1 cacheのfull hash/EOF、new→old元leadの双対、全8059 final dot/residual零。前lambdaの数値を再利用しない |
| 同じ六tag・四characterのsource functional | C:928–930→O:270 `source_scores`、O:315 `raw_edge_cochain`。ordinary27差分基底、全score[6,2,54432]、f[108864]、b_aux[2]を再計算。二etaは-kappa_aux[6:8]で、18をF3内で割らない |
| 正しい固定graph/carryと全zero | O:243の実36点Q0再構成、C:339 `fixed_tree`の全chordと五独立列。C:358 `current_tree`はfresh f potential、全values/fit/residualsと二auxを計算し、両方零の場合だけwitness.kind=none/COMPLETE_ZERO_CANDIDATE |
| 全配列とwitnessなしの根拠 | C:763 `compare_directory`はexact rosterとexpected bytes+一byte超読EOF。O:659/680/690のq/P1/chi/kappa/score/f/aux/chord/fit/residual/witness全payloadをC:802 `compare_phase`から比較。自己申告のfull_eofだけではない |
| current snapshotとcomplete oracle | C:785/824/893/903。現stateからsnapshotを再構成し、owner/source/fixed/step/rank/gen/state_head/lambda/targetを一致させ、三phase実EOFからoracle-result/manifestを作って全bytes一致 |
| HEADの現checkpoint | C:1023/1096。checkpointのsnapshot/physical-parent/順序付きphase hashes、三phase以後のoracle/witness hash、HEADのcurrent snapshot/checkpointを結ぶ。全新step再計算後のstateから現snapshotを作り、C:1135でcheckpointの全算術prefixと比較 |
| 負候補の型 | C:1156–1200 `check_terminal`は現oracleがCOMPLETE_ZERO_CANDIDATE、現checkpoint.last_complete_phase=treeを要求。lambdaなしのlinear targetやUNKNOWNをこの枝へ入れない。complete_zero_oracle_result_sha256とHEAD/result全字段を再構成 |
| 全prefixの受理 | C:1446–1505 `check_actual`、workflow:727以降。prefix_steps_replayed=completed_steps、current_checkpoint_fully_compared、全array/JSON、実result/HEAD/hash/terminalを照合。resource exit3/未完cursorはPASSではない |

P:1621 `current_result`も同じ現state_head/lambdaを要求し、P:1650 `run_loop`は完成oracle零を認めて停止する。単体のP.resultや`witness.kind=none`だけでは上表を満たさない。負証明の最小現物は、exact launch/source/parent pins、HEAD、現snapshot/checkpoint、三phaseとoracle topの全payload、現在lambda・全row/targetの照合receipt、accepted rho2/Conn/P1/source-mapの親である。HEAD外のdurable tailは候補の完成域へ足さない。

F5. **正式当該grade NONMEMBERの最小残件。** 仮定する「complete-zero＋全prefix checker PASS＋CV9」のうち、CV9は紙の正しさまで自動的に保証しない（2138 §9）。本便のF1–F3が紙の含意を担当し、工房は次の二点を同じ実candidateで受理する必要がある。

1. **現在証明書の実受理。** F4の実全EOF/PASS、同じlambdaの全row零/target1、artifact/launch/sourceと保存不変性を、現在の全prefix/current checkpointについて照合する。古いrankのscore/f/treeの第三再計算や成功selftestを、今回の現在配列の照合へ転記しない。
2. **保持前提の継続受理。** actual marked source/Psiの完全性、全8059独立P1と同じcanonical lifts、Task712四B=H、完全Connと初期state span、固定元rho2の意味と(976.3)のaccepted親identityを、当該ownerの根拠として明記する。旧v535本文の当時の未実行表示を現在状態へ流用せず、実受理親のreceiptを参照する。

この二点が受理済みという条件の下では、(976.2)とlambda_*(rho2)=1からrho2∉M2が直ちに従い、**新しいpositive consumerの数値gateは残らない**。単なる`status=PASS`や「CV9済み」というラベルから、保持前提の未受理部分を消したことにはしない。

独立性の最小範囲も分ける。現在pairのsourceは全四q・P1値・kappa・score/f/treeを再計算する経路を持ち、Pのdense収縮とCの保持packed収縮は別算術である。一方、2138 F-sc-1/2143 F-cy-4aのB envelope復号・words/context/transportの共通TCB、P1 cache/Task554の意味、完全Conn/旧target identityは新wrapperで独立にならない。旧F-fo-1 scan cloneは歴史として残る。第三実装が以前q/kappa・B表自体・旧行・lift全体を再計算しなかったことは、今回すべて済んだという主張を禁ずる。

**それらを新たに無条件化する必要がある場合だけ**、未受理のload-bearing境界に絞った独立照合を要する。負証明では最終lambda一つに対するq=B^*lambda、全8059の実lift値/section等式、正しいsource pullbackと全tree恒等式、lambda(Conn)=0、lambda(rho2)=1までを対象にできる。Bの復号/意味が問題なら同じdecoderを再度呼ぶだけでは閉じず、固定raw tableの独立解釈または同じ物理写像との直接scalar比較を要する。Connの**完全性**やPsi onto/P1 sectionの意味が未受理なら、単なるdotやhashの追加だけで代替できない。元target identityだけをaccepted premiseから外すなら、既に正しく同定した原rho2 bytesへの直接dot1でその帰納依存を短絡できるが、これは現runが実施したことではなく、常時必須でもない。

第三の全matrix再構築、旧全26scan再走、全54430物理packet、全過去pivotのliteral再生を一律に発注する必要はない。現在の負証明に必要な前提がすでに受理されていれば、以前の第三被覆不足を理由に同じ仕事を重複させない。工房の格付けは保持TCBを明記した有限のcross-checkedであり、Lean verifiedとはしない。

F6. **非零omega実例とpositive 11slotの位置。** v547(4.3)/(5.1)と2144は、すべての合法cycleのsourceをOmega語から得るという紙の完全性を支える。literal規約はsr(0,1,2)=(0,1,-1)、因子順と普通整数epsilon/6を固定する。omega=2での代表2と-1は同sourceでも同一語ではない。この普遍命題を使うために、現在探索から非零omegaの実例を一本見つけることは論理的前提ではない。complete-zeroはEを作らず終了する正規の枝である。

Task958の一root SLP、normalized pair、同じwordの11 typed slots/printed aggregationは、rho2を実現する**正の証人**を受理する条件である。負証明はその証人の非存在を線形necessary imageのseparatorで示すので、存在しない証人の構成・11slot再生を要求しない。ただし、六tagのsource-mapや固定targetの意味を11slot物理問題へ結ぶ既存の構造的前提まで不要になるわけではない。「最終一語のreplay不要」と「source/target mapの正しさ不要」を区別する。

また、最終負証明そのものはlambda(M2)=0とlambda(rho2)=1で閉じ、過去の各pivotがM2内にあるというrank-rise/positive ancestryの証明を改めて使わない。過去の選択法や旧scanの独立性を新しく証明し直す必要はない。既登録の全prefix checker契約はそのまま実行し、保持来歴とrank主張の限定もそのまま残す。

F7. **昇格を禁止する具体的反例条件。**

- **lambdaの混合。** k^2でM=span(e1)、rho=e1とする。lambda_zero=e2*はMを消し、別のlambda_target=e1*はrhoに1を返す。しかしrho∈Mである。古いzero oracleと新しいtarget-dot1を、同じlambdaとして結べない。
- **Conn欠落。** W2=W1=k、pi=id、ell=0、G=H=idとするとR=0でF_lambda=0だが、M2=Conn=k。lambda=id、rho=1なら負判定は偽。完全zero scalar oracleだけでConn条件を省けない。
- **scope/EOF欠落。** 合法sourceの寄与が省いたcharacter/tagにだけある場合、残scopeの零は全域零を意味しない。五fit行や冒頭だけが零でも、最後の一chord residualが非零なら合法六cycleの反例がある。`witness=none`の自己申告、missing arrayをzero扱い、UNKNOWNをEOF扱いにしない。
- **checkpointの混合。** HEADと異なるsnapshotのtree、またはsection/cochainしか完成していないcheckpointへ付けたcomplete-zeroは不受理。HEAD外tailのhash一致も現checkpointの全算術比較を置換しない。
- **DERIVEDの断線。** 元rho2 hash/ownerが違う、親remainder→子remainderの実identityが未受理、scalarをselected値/scaleで代用、参照行が最終全row sweepにない、などの場合、現在剰余へのdot1は元rho2へのdot1にならない。

F8. **結果が実際に揃った場合の正式文案。** 次は条件文であり、本runの結果ではない。

> 同定した実candidateの現lambdaについて、全四character・全8059 section等式・全54433 chord恒等式・二aux零と、完全Connを含む全保存行への零pairingを独立照合した。固定source/P1/Conn/Task712/targetの受理前提と全target差分により、lambda(M2)=0かつlambda(rho2)=1。したがって、この固定R07 H/grade2問題ではrho2∉M2、当該gradeはNONMEMBER（有限、保持TCBを明記したcross-checked）。元rho2のpairingはDERIVEDであり、直接読取と称さない。他のH/grade/lower-state・全A0の普遍的非存在・無限cofinal・Lean verifiedは宣言しない。

実記帳では上文へactual run/attempt/head、candidate・HEAD・current snapshot/checkpoint・lambda・complete-zero oracleのhashと工房裁定番号を入れる。本便には未観測の値を埋めない。現時点の判定は「この条件付き負命題と凍結gateの接続は成立、実結果は待つ」である。

AUDIT_976_VERDICT: CONDITIONAL_COMPLETE_ZERO_TO_GRADE_NONMEMBER_MATH_PASS; CURRENT_FULL_PREFIX_AND_PARENT_PREMISES_REQUIRED; NO_AUTOMATIC_NONZERO_OMEGA_OR_POSITIVE_ELEVEN_SLOT_GATE; ACTUAL_CHECKER_FAILED_DIAGNOSTIC_PENDING; PRODUCER_TERMINAL_UNOBSERVED; verified=false.
