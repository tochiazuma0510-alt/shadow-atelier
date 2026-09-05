# Task958 — target 零から grade2 positive readout への限定 intake

本便は条件付きの read-only intake である。Task954 の source は 97,806 bytes / `d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa` のまま変更していない。root から与えられた run `33967668257/1` の状態は、事前試験・初回 cap1 success、実 resume32 進行中までである。本便では新 rank、target 零、terminal を観測していない。

v518 全文、reply953 F7、Task954 source / 公開 ABI、実 fixed44 親の target JSON を読み、v534、v511、v516 の接続条項と下記の自系実装を参照した。checker 算術、network、git、credential、Python/GAP/import/AST、追加 agent は使用していない。変更は本返信だけである。

## F1. 係数 readout は保存済みの target 差分を順に連結できる

物理 pivot を **挿入順の 0-based ID** で (S_0,S_1,\ldots\) とする。base の `output/result.json.target_reduction.reductions` に記録された `pivot_id=i, scalar=a_i` を使い、記録のない位置の係数を 0 とする。これは pivot の `lead` 順への並べ替えではない。実 base の reductions は `pivot_id=1,lead=3`、次に `pivot_id=2,lead=1` を含む。

実 parent payload の read-only 照合結果は次のとおりである。表の scalar は target 更新の係数であり、選択違反 scalar や pivot の正規化 scale とは区別する。

| 親 / payload | 追加 pivot ID / offer | target scalar | target remainder の変化 |
|---|---:|---:|---|
| base run33891714539 `output/result.json.target_reduction` | 既存 0–1353 | 保存済み reductions（非零 884 件） | rho2 → `e0053fc6…` |
| seed30 run33946247365 `target-update` | 1354 / 8059 | 2 | `e0053fc6…` → `f5040e3f…` |
| seed34 run33956437467 `target-update` | 1355 / 8060 | 1 | `f5040e3f…` → `46a6b828…` |
| fixed44 run33964709359 `steps/000001/result.json.target` | 1356 / 8061（seed35） | 1 | `46a6b828…` → `678b1457…` |
| 同 `steps/000002/result.json.target` | 1357 / 8062（seed36） | 1 | `678b1457…` → `0a466426…` |
| 同 `steps/000003/result.json.target` | 1358 / 8063（seed37） | **0** | `0a466426…` → 同じ値 |

各 step は (r_{k+1}=r_k-\alpha_k S_k) を保存している。したがって Task954 の新 completed prefix が (m) 段で、その第 (j) 段の `result.target.scalar`（=`instruction.target_scalar`）を (\alpha_j) とすれば、readout の式は

\[
\rho_2=r_m+\sum_{i=0}^{1353}a_iS_i
 +2S_{1354}+S_{1355}+S_{1356}+S_{1357}+0S_{1358}
 +\sum_{j=1}^{m}\alpha_jS_{1358+j}.
\]

新段の offer は `8063+j`、rank は `1359+j` という公開 ABI の ID 規則を用いる。この式は新数値の主張ではない。(r_m=0) が実際に受理された場合に限り、右辺の pivot 和が rho2 の係数 readout になる。

具体的入力は base の reductions、seed30/34 の `new_reductions`、fixed44 三段、新 completed prefix の各 `target` / `instruction` / `physical-normalized.bin` と、その manifest・HEAD・owner・source の連鎖である。fixed44 と新段の target は `parent_remainder_sha256,remainder_sha256,scalar` の **plain dict**、instruction は rolling hash であり、旧 target-update の sealed schema を被せない。file byte hash と embedded seal も区別する。

parent の根拠を残す最小 pin は、base result `d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968`、seed30 result `60e47f7c673942611647a69087d29bd0223e40394144b43aae9e0f55da10fb8b`、seed34 result `3a8357365f4e5f3f7d281b811d36d49e4f334cbec3828c82833ae1b1d5af0242`、および Task954 start の accepted packet layout / exact artifact tuple である。base の rho2 は packed SHA `b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e`、fresh target manifest は `55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488` である。

これは **受理済み parent arithmetic を前提とする新しい係数読出し** であり、旧 target 除去を新たに計算したとの表示をしない。base の `p1_expression_hex` は Separator のため null である。既存の MEMBER 用係数ファイルが既にあると扱わず、明示的 reductions から読む。pivot companion の P1 係数は線形照合用であり、順序付き word の代用品ではない。

target scalar 0 の段も、ID、parent/new remainder、pivot、ancestry を保持する。最終外側の係数が 0 でも、その pivot が後続 pivot の reduction で参照されうる。係数 readout に正規化 scale をもう一度掛けない。scale は次節の pivot word 定義の内部で一度だけ使う。

## F2. 現物の ancestry から一つの v518 SLP を作る consumer

v518 §§1–4 の語彙 `Rel / Act / ordered Prod / Inv / prior Ref / identity` で、次の順序を固定すればよい。以下の指数は ([0]=1,[1]=W,[2]=W^{-1}) の意味であり、**2 は literal inverse** である。

1. canonical P1 の原点 (Z_i)、記録順の reductions (E_i)、scale (\sigma_i) から
   (W_i=(Z_i\prod_{(p,q)\in E_i}^{\rm recorded}W_p^{[-q]})^{[\sigma_i]})。seed origin、旧 seed/transition defect、new-block origin は受理済み DAG の型どおりに展開する。new-block では whole old-defect への projector を一度だけ掛ける。
2. Conn の lower pivot は (U_i=(W_i\prod_p^{\rm recorded}U_p^{[-q_{ip}]})^{[\sigma_i]})、dependent raw Conn は (K_i=W_i\prod_p^{\rm recorded}U_p^{[-q_{ip}]})。raw Conn と normalized physical pivot を同一視しない。
3. 新 seed defect は bare relator と全 raw reduction events、actor defect は **(tW_i t^{-1})** と全 ordered ActRed events から作り、whole defect を指定 character で project する。Task954 の actor は complete filtered action を用い、lower-to-top (K_t b) を含む。direct input の (W_i) と、最終係数が相殺した raw-event 参照も ancestry の対象とする。
4. projector は `CHARACTER_LABELS=((0,0),(0,1),(1,0),(1,1))` の順で、`PURE_Q1_WORDS[e]` による conjugate を符号付きで掛ける。辞書列挙や sort への置換はしない。raw path (w=(t_1,\ldots,t_k)) は (t_1) が最外、(t_k) が最内の nested conjugation。行への forward application は逆走査であり、右への path extension は最内の追加になる。Task954 root selection の path は空であるが、この型を崩さない。
5. raw orbit / Conn word (G_j) と ordered physical reductions から
   (S_j^{\rm word}=(G_j\prod_p^{\rm recorded}(S_p^{\rm word})^{[-q_{jp}]})^{[\sigma_j]})。F1 の挿入順係数を使い、最終 root を
   (\Delta C_2=\prod_j^{\rm insertion}(S_j^{\rm word})^{[a_j]}) とする。

inverse は product 全体の inverse である。展開するなら因子順も反転する。mod3 leaf の collection / sort / cancellation は補助的な線形 receipt に限り、上の nonabelian SLP 自体を置き換えない。

調べた公開 API と不足箇所は次のとおりである。

| 既存の自系 source / API | 既に読むことのできる材料 | 今回必要な consumer |
|---|---|---|
| `d972_r07_grade2_physical_state_separator_v2.py` `_validate_connection_parent`、`_load_state`、`_target_reduce`、`materialize_terminal` | base physical instructions は nested Conn record、source、ordered reductions、scale、row/companion offsets を保存。target reductions も明示 | 現在の delta prefix を含む F1 reader。旧 `materialize_terminal` の base-only MEMBER export をそのまま呼ぶ対象ではない |
| `d972_r07_canonical_p1_physical_connection_v6.py` `PhysicalSource`、`transduce` | P1 offer と lower / top / coefficient を同じ reduction で処理した Conn transcript | raw / lower pivot / physical pivot の三型を持つ SLP compiler |
| `d972_r07_grade2_p1_componentwise_semantic_replay_v5.py` `replay_prepare`、`replay_block`、`join` | Task554 lower components の origin/reduction semantics | canonical precision2 P1 DAG は別の v9 accepted parent へ join。既存 lower semantic replay は 145152-trit top や eleven-slot word replay ではない。旧 closure を再生成する必要もない |
| Task954 `canonical_index`、`actor_relation`、`canonical_input`、`subtract_lifts`、`materialize_actor/seed`、`append_step` | direct input、cancelled raw references、ordered relation、components、row、physical reductions / sigma / target scalar | compact index の offsets/hashes から accepted P1 instructions を positioned read し、原点の full typed DAG を作る。`literal` の ancestry recipe を一つの root SLP に接続 |
| `d972_r07_a0_grade1_selected_slp_v2.py` `NodeView/EdgeView`、`staged_adjoint`、`execute` の `source-ancestry.json` / `structure` | prior-ref DAG、origin / ordered signed reductions / scale の receipt 形式、bounded traversal の実例 | fixed grade1 owner/body/root を期待する CLI から、新 owner の compiler へ versioned adapter。`staged_adjoint` の coalesced leaf map を word として流用しない |
| `d972_r07_grade2_violation_materializer_v2.py` `P1Reader`、`LowerReader`、後半の `materialize_violation`、`insert_physical` | raw-dual path、reverse forward walk、noncommuting `(1,2)` control、raw/physical pair equality、pivot 分離 | path と receipt の既存型は参考になるが、同版 actor の top-only (T_tb^{(2)}\) 部分を Task954 に戻さない。今回の complete filtered actor / global ActRed consumer を用いる |

Task954 の `actor_literal` は現在も `normalized_exponent_pair:"NOT_REPLAYED"`、`eleven_slot_replay:false`、`grade2_positive_terminal_complete:false` である。調べた入口は current target/pivot prefix 全体を受け取る完成済み v518 positive compiler ではない。リポジトリ全体に関数が存在しないとの推測ではなく、上記 owner / input 契約との未接続を指摘している。

## F3. normalized pair と同じ word の eleven-slot 直接再生

normalized pair はこの SLP の整数 exponent sums を bottom-up に求める。Rel は literal relator の二整数、Prod は整数和、Inv は負号、Act は内側の値である。最後に両方の 18 整除を確認し、

\[
\nu(\Delta C_2)=(\epsilon_x(\Delta C_2)/18,\epsilon_y(\Delta C_2)/18)\bmod3=(0,0)
\]

を直接出す。これなら巨大な flat word への展開は不要である。`d972_r07_a0_first_rung_grade2_prebuild_v1.py:evaluate_seed_precision2` は既に同じ整除と `auxiliary[6:]` を計算するが、入力は flat `tuple[int,...]` の seed である。`d972_r07_a0_psl504_member_payload_lift_v3.py` の `exps` / normalized pair の例は旧 PSL504 floor の固定 payload を読む。そこにある `canonical(raw)` の leaf collection と old scratchpad source を現 owner に持ち込まない。また V12F の `producer_exponent_pair` は通常 exponent の mod3 であり、この **18 で割った normalized pair** の代わりにはならない。

実 eleven-slot の既存入口は `d972_r07_a0_fresh_precision2_endpoint_signature_v9.py:load_all_seven(words)` → `build_endpoint_minimal` → pinned `d972_r07_history_free_positive_fast_resume_v12f.py:ProducerAllSeven` である。v9 は accepted fresh-rho2 系の endpoint runtime を構成し、generic history-free campaign 自体を呼ばない。V12F pin は `22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb`、prebuild pin は `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8`。これらの pins だけで新 owner への接続が完了するとはしない。

`ProducerAllSeven.coordinates(word)` は 10 個の coordinate `bytes`、v9 の `signature` は `TEN=(0,1,2,3,0,4,5,6,7,8,9)` により **11 個の typed `(E3/E4, bytes)`** を返す。同じ coordinate 0 を H1 と H2 の別 occurrence として保持する。

| slot | label | block / sign | coordinate / 型 |
|---:|---|---|---|
| 1 | H1_fxy | 1 / + | 0 / E3 |
| 2 | H1_fxz | 1 / − | 1 / E3 |
| 3 | H1_fyz | 1 / + | 2 / E3 |
| 4 | H2_fux | 2 / − | 3 / E3 |
| 5 | H2_fxy | 2 / − | 0 / E3 |
| 6 | H2_fuy | 2 / + | 4 / E3 |
| 7 | P_b1 | 3 / + | 5 / E4 |
| 8 | P_b2 | 3 / + | 6 / E4 |
| 9 | P_b3 | 3 / + | 7 / E4 |
| 10 | P_b5_inverse | 3 / − | 8 / E4 |
| 11 | P_b4_inverse | 3 / − | 9 / E4 |

v9 `build_atom_cache` / `extend_signature` / `fold_signature` は typed element の product、`occurrence_prefix_contract` は g760 に依存する occurrence prefix と sign、`atom_order_anchor` は非可換 word 順を固定する。V12F `producer_unpack_element` / `producer_element_blob` と quotient `.mul/.inverse` が実データ型への入口である。ただし typed endpoint の一致・identity だけでは Fox row / grade の一致を示さない。

Fox 側の実入口は V12F `ProducerAllSeven.occurrence_column(delta_word,relator_word)` と `direct_column(delta_word,relator_word)` である。後者は literal conjugate、`g760 + conjugate`、二つの hexagon と pentagon の直接 Fox 差分を作り、11 occurrence からの和と比較し、`dict[bytes,int]` の block / component / typed-element row と receipt を返す。これは **一つの relator conjugate の flat word** が契約であり、current ordered SLP 全体を直接受け取る入口ではない。

必要な versioned consumer は同じ SLP の各 node について typed endpoint と Fox pair を同時に評価し、

\[
D(UV)=D(U)+\operatorname{ev}(U)D(V),\qquad
D(U^{-1})=-\operatorname{ev}(U)^{-1}D(U)
\]

を使って全 11 slots を直接進めるものになる。ordered product / inverse / nested Act を保存し、固定 g760 prefixes、printed hexagon / pentagon / PB / A18 の aggregation と現 owner の physical projection へ接続する。出力は各 slot の型・endpoint・Fox/grade receipt、aggregation receipt、同じ root hash に束ねた全 physical lower 0 と top=rho2、normalized pair である。11 個の独立 cycle を別々に解く方法ではない。

現 prebuild の `evaluate_seed_precision2` は source `(d0,d1,d2,aux8)`、`aggregate_precision2` は `context.aggregate_table` の **6 source tags から 2 hexagon blocks**、`flatten_physical_lower` は 32260 trits、physical top は 48384 trits を扱う。Task554 full source lower は別型の 96776 trits、canonical P1 top は 145152 trits である。これら六 tags を eleven slots と呼ばない。v9 `evaluate` の reached-seed direct-column canary や endpoint buckets も、新しい \(\Delta C_2\) 全体の独立 eleven-slot grade replay には置き換えられない。同実装自身の `direct_occurrence_replay:false` という限界も維持する。

必要 artifact は、current owner/source/start/complete HEAD、F1 全親の target/pivot receipts、accepted P1 v9 の instructions/cache と Task554 origin/body/packed lower blobs、Conn / base state instructions、Task712 B/T tables、同じ paper literal dictionary / 44 relators / PURE_Q1_WORDS、fresh rho2 の full parent、endpoint runtime の pinned source closure・Q3 marked quotient・context registry・fine deletion・g760 と occurrence prefix である。特に fresh-rho2 の artifact は run `33839962829/1`、id `9925190479`、head `17a8439c766d92719d7ae7d35846ea444da598fa`、name `task640-fresh-rho2-v17-33839962829-1`、zip 6,049,643 bytes / `01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4` として exact parent を示せる。旧 Task601 固定 root を読む v9 `evaluate` CLI や旧 PSL504 payload CLI をそのまま現 owner 用に呼ばず、accepted model/data が現 owner と同じである join を明示する。DERIVED lambda receipt は positive direct rho2 replay の代替ではない。

## F4. 最小実装単位と判定の分離

独立に実装・照合できる最小単位は次の四つである。いずれも新数値が与えられるまで terminal を決めない。

| 単位 | 入力 | 出力 / 境界 |
|---|---|---|
| A. ordered target reader | exact parent result/manifest、current complete prefix / HEAD、normalized pivot receipts | 挿入順 `(pivot_id,scalar,owner,step/ref)`、0 の段を含む全差分列、rho2−sum=remainder の受理親付き readout receipt |
| B. selected v518 SLP compiler | A、P1/Conn/defect/physical の ordered typed ancestry、literal dictionary | one root ID/hash、reachable typed DAG、source / offset / hash join、係数2 inverse・projector順・非可換 nested path の canary。mod3 collected leaves は補助出力だけ |
| C. normalized-pair consumer | B の同じ root / literal DAG | 整数 exponent pair、18 整除、normalized mod3 pair、side/localization の指定 gate receipt |
| D. same-word direct eleven-slot consumer | B と同じ root、exact endpoint / occurrence / PB / A18 owner、fresh rho2 | 11 typed replay と direct physical aggregation、全 lower 0 / top=rho2 の比較。producer とは独立の consumer が同じ契約を照合する |

v518 Theorem5.1 / v511 / v516 に照らした主張の境界は次のとおりである。

- **linear target 零**: F1 の current completed rows と target の線形等式。Task954 の target-zero terminal だけで literal MEMBER gate 完了とはしない。
- **条件付き one-word 存在**: accepted 44-relator normal-closure premise と全 ordered source ancestry から、B の \(\Delta C_2\in U\) を構成する紙上の接続。逆 physical map や arbitrary cycle の lift を新たに仮定しない。
- **当該 grade の正式 MEMBER**: v518 の canonical P1 / source replay、fresh rho2 の lower/aux zero、ordered target transcript、**独立した同じ word の 11 slots 直接再生・printed aggregation**、normalized pair と登録済み side/localization gates がすべてそろった場合に限る。Task954 の ancestry recipe のままでは C/D が未完了である。
- **full H/P/A0**: この有限 grade の結果だけからは出ない。v511 の ambient word / reached normal kernel / preferred formation を分け、さらに必要な selected lane と full target の条件を別に維持する。逆に、一つの有限 grade certificate に無限 cofinal saturation / compactness を追加の前提として課さない。

v516 の augmentation-ideal / nested commutator construction は、その coefficient identity がある場合の別の具体 materialization route である。今回の selected word には v511 の直接 normalized-pair check が使えるため、未提示の IM 所属証明を追加 gate にしない。本便は実走時間を見積もらず、新 MEMBER、full A0、新 numerical result、cross-checked、verified を宣言しない。

AUDIT_958_VERDICT: CONDITIONAL_POSITIVE_READOUT_SPECIFIED; CURRENT_OWNER_SLP_AND_SAME_WORD_NORMALIZED_ELEVEN_SLOT_CONSUMERS_PENDING; NO_NEW_RUNTIME_RESULT
