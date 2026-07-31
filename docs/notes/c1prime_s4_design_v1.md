# C1′(S4 窓)を閉じる証明書の**数学設計** — P92-4 の 4 点の工程表

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 委嘱: 司令塔(次波 4)「S4 窓の C1′ を閉じる 4 点(①monodromy 9T27 の証明 ②j-table+class vector+diagonal [0,0,0] ③商 dessin → W-lift の一意 binding ④全 digest 束縛)の**数学設計**(何をどう証明・計算するかの工程表 — 実装は次段)。`u7_meas_design_v1.md` の C1′(7) 要件表との整合も」
- 入力: `sol/sol_reply_92_math19.md` **W92-5 / P92-4 / F92-5.2**、`docs/notes/u_meas_m3_design_v1.md` §1.2/§4、`docs/notes/u_meas_m1_passport_v1.md` §2.4、`docs/notes/u7_meas_design_v1.md` §5.3、`docs/notes/surj_s4_v2.md`
- **状態札: design(candidate)・未実行・実装は次段。本書に測定値は一切書かない。**

---

## 0. 設計の中心思想(先に 1 段)

W92-5 の指摘は正確である:
> 「240 個の Frobenius cycle type が許容型内にあり 7-cycle が出たことは強い evidence だが、**有限標本から geometric monodromy が正確に 9T27 であること、まして 6 個の $W$-dessin のうち指定した diagonal lift であることは証明できない**」

**⟹ 設計方針の転換**: **見つけた曲線の monodromy を検証しにいく(標本 → 群)のをやめ、monodromy が強制されるように曲線を構成する(群 → 対象)。**

我々には既にその素材がある — 命題 U-LOC / U-Q / U-Q′(`u_meas_m3_design_v1.md` §1.2–1.3)は $W$ を
$$W\ =\ C\times_{\mathbf P^1_t}\mathbf P^1_\lambda$$
という**fibre 積**として与える。fibre 積の monodromy は**群論の式**で決まる(標本不要)。したがって C1′ の中核は「$W$ の monodromy を測る」ではなく「**$C\to\mathbf P^1_t$ の monodromy を確定し、fibre 積の式で $W$ 側へ持ち上げる**」になる。これが P92-4 の ③ が ① を含意する構造である。

さらに **rationality が dessin を一意に指す**という第 2 の梃子がある(§3・**本書の新提案**)。

---

## 1. C1′ の論理構造(何と何を同一視するのか)

| 側 | 対象 | 由来 |
|---|---|---|
| **定理側**(intrinsic) | 窓 $W$ の GTSh データが定める抽象 dessin $D_W$ = 三つ組 $(X,Y,Z)$ の $S_9$-共役類($XYZ=1$) | `surj_s4_v2.md` §1 の窓データ($P=\mathrm{PSL}(2,8)$、$M=\mathrm{ord}(X)=9$、`phi_image`$=\mathrm{Hol}(\mathbf Z/9)$) |
| **測定側**(extrinsic) | 厳密モデル $(C,t)$ が定める Belyi 被覆 $\beta:W_{\rm meas}\to\mathbf P^1_\lambda$ の dessin $D_{\rm meas}$ | U-LOC の曲線・cusp・局所助変数 |

$$\textbf{C1}'\ :\quad D_W\ \cong\ D_{\rm meas}\quad(\text{dessin としての同型}).$$

これが無ければ「測った $u_0$」と「判定表の intrinsic $u$」は**別の量**であり、$\mathrm{Ih}_{S4}$ 全射の主張は成立しない(F92-5.3 の算術含意は正しくても、その主語が違う)。

**passport では足りない理由**(既知): 順序 passport $\bigl((9),(9),(9)\bigr)$ をもつ monodromy $\mathrm{PSL}(2,8)$ の dessin は **6 個**ある(`u_meas_m1_passport_v1.md` §2.4)。

---

## 2. 工程 G-1 — 幾何 monodromy の**証明**(P92-4 ①)

### 2.1 ★ 先に潰すべき記号の食い違い【要即決・コスト 1 GAP 呼び出し】

- 工房の実測: 「monodromy 群 $=\mathrm{PSL}(2,8)$、`TransitiveIdentification` $=27$ ⟹ **9T27**」(`u_meas_m1_passport_v1.md` L125/L150)。$\lvert\mathrm{PSL}(2,8)\rvert=504$。
- Sol の便 92 の表記: 「**9T27 $=\mathrm{P\Gamma L}(2,8)$**」(F92-5 / P92-4)。$\lvert\mathrm{P\Gamma L}(2,8)\rvert=1512$。

**どちらかが誤記であり、放置すると証明書の必須欄がずれる。**
> **【C1P-0】** `TransitiveGroup(9,27)` の `Size` と `StructureDescription` を 1 回引き、$504$ か $1512$ かを cert の `monodromy_T_label` 脚注に固定する。**この 1 行を工程の第 0 番に置く。**

**ただし食い違いは単なる誤記ではない可能性が高い** — それが次項である。

### 2.2 幾何 monodromy と算術 monodromy を**分けて**書く

$\overline{\mathbf Q}(\lambda)$ 上の Galois 群(**幾何** monodromy)$M_{\rm geom}$ と $\mathbf Q(\lambda)$ 上の Galois 群(**算術** monodromy)$M_{\rm arith}$ は一般に異なり、
$$M_{\rm geom}\ \trianglelefteq\ M_{\rm arith},\qquad M_{\rm arith}/M_{\rm geom}\hookrightarrow\mathrm{Gal}(\overline{\mathbf Q}\cap\text{定数体}/\mathbf Q).$$
$\mathrm{PSL}(2,8)$ は $\mathrm{Out}=C_3$(Frobenius)をもち $\mathrm{P\Gamma L}(2,8)=\mathrm{PSL}(2,8)\rtimes C_3$。**したがって $M_{\rm geom}=\mathrm{PSL}(2,8)$ かつ $M_{\rm arith}=\mathrm{P\Gamma L}(2,8)$ は完全に両立し、むしろ自然な形である。**
> **設計指定**: cert には **2 欄**を置く。`monodromy_geometric`(= 定理側が要求するもの)と `monodromy_arithmetic`(= Frobenius 標本が見ているもの)。**W92-5 の「240 個の Frobenius cycle type」が測っているのは後者である** — この分離だけで、Sol の指摘の一部(「標本は幾何 monodromy を決めない」)が**設計上の当たり前**に変わる。

### 2.3 幾何 monodromy を**証明する** 3 経路(推奨順)

| 経路 | 内容 | 何を出力するか | コスト | 失敗モード |
|---|---|---|---|---|
| **(G1-a) 構成的**(★ 推奨) | $W=C\times_{\mathbf P^1_t}\mathbf P^1_\lambda$ の**構成**から monodromy を群論で導く(§4)。$C\to\mathbf P^1_t$ の monodromy $\bar M$ と $\mathbf P^1_\lambda\to\mathbf P^1_t$ の次数から、fibre 積の monodromy は**部分直積の明示式**で出る | $(X,Y,Z)$ の**明示置換表現**(標本ゼロ) | 中(紙+GAP) | $C\to\mathbf P^1_t$ 側の monodromy が未確定なら空回り ⟹ そちらを先に閉じる |
| **(G1-b) resolvent** | 次数 9 の定義多項式 $f(\lambda,T)$ に対し $\mathbf Q(\lambda)$ 上の Galois 群を resolvent 分解で決定。$\overline{\mathbf Q}$ 係数へ上げて幾何側を得る | 群の同定 + 分解の証拠 | 大(次数 9 の resolvent は重い・8GB 制約) | 係数膨張。定数体拡大の扱いを誤ると幾何/算術を混同 |
| **(G1-c) 下界+上界の挟み撃ち** | **下界**: 標本(Frobenius)で $M_{\rm arith}\supseteq\langle$観測された巡回型を含む群$\rangle$。**上界**: passport から $M_{\rm geom}\subseteq$「3 つの 9-巡回で生成され推移的な群」= 有限リスト。両者が 1 点で交われば確定 | 挟み撃ちの 2 枚 | 小〜中 | **上界が本当に有限リストになるか**の証明が要る。$S_9$ の推移部分群で 9-巡回 3 個が積 1 で生成するもの、を悉皆(degree 9 の推移群は 34 個 — **悉皆可能**) |

> **★ (G1-c) は思ったより安い**: 次数 9 の推移群は **34 個しかない**。「3 個の 9-巡回 $X,Y,Z$ で $XYZ=1$、$\langle X,Y\rangle$ 推移」を満たす 34 群の悉皆判定は GAP で即座に終わる。**上界側が悉皆で閉じるなら、標本は下界にしか使わないので W92-5 の批判(標本から群は決まらない)を正面から回避できる。**
> **⟹ 設計採択: (G1-a) を主経路、(G1-c) を独立の第二系統。(G1-b) は最後の手段。**

---

## 3. 工程 G-2 — 6 個のうちどれか(P92-4 ②)。**★ 新提案: 有理性が対角を強制する**

### 3.1 既存の道具

`u_meas_m1_passport_v1.md` §2.4【FINDING U-2】: 6 個の dessin は**類ベクトル**($X,Y,Z$ がそれぞれ $\mathrm{PSL}(2,8)$ の 3 つの 9-巡回類のどれに入るか)で**完全に分離**する。窓 B の dessin は **$(0,0,0)$(対角)**。

### 3.2 ★ 本書の新提案 — 「どれか」を「有理か」に置き換える

$\mathrm{Out}(\mathrm{PSL}(2,8))=C_3$ は 3 つの 9-巡回類を巡回置換する。$G_{\mathbf Q}$ の 6 個の dessin への作用は $\mathrm{Aut}(P)$ 経由でこの $C_3$ を通して factor する。従って:

> ### 【設計提案 C1P-DIAG】
> **もし 6 個のうち「対角」なものがちょうど 1 個なら、それは $C_3$-作用の不動点であり、従って** $$\boxed{\ \textbf{定義体}=\textbf{moduli 体}=\mathbf Q\ \text{をもつ dessin は、その 1 個に限られる}\ }$$
> 一方、命題 **U-Q / 系 U-Q′** は我々の $W=C\times_{\mathbf P^1_t}\mathbf P^1_\lambda$ が **$\mathbf Q$ 上定義される**ことを既に与えている。
> **⟹ 「$D_{\rm meas}$ は $\mathbf Q$ 上定義される」+「$\mathbf Q$ 上定義される dessin は対角のみ」⟹ $D_{\rm meas}$ = 対角 = $D_W$。C1′ の ② と ③ が同時に閉じる。**

**この提案の前件(要確認・いずれも安い)**:

| # | 確認事項 | 方法 | 現状 |
|---|---|---|---|
| **D-a** | 6 個のうち対角なものが**ちょうど 1 個**か | GAP 悉皆(既存の 6 個の類ベクトル表を読むだけ) | 【FINDING U-2】の「**唯一の**対角 dessin」がそう読めるが、**類ベクトルの値 $(0,0,0),(1,1,1),(2,2,2)$ が 3 つとも 6 個の中に現れるなら「対角」は 3 個**になる。**まず表を読め**(コスト 0) |
| **D-b** | $C_3$-軌道構造(6 = 1+1+1+3? 3+3? 1+2+3?) | 同上 + $\mathrm{Out}$ 作用の明示 | **未計算** |
| **D-c** | $G_{\mathbf Q}$ の作用が $\mathrm{Out}(P)=C_3$ を通ることの証明 | dessin の Galois 作用は monodromy 群の外部自己同型としてしか働けない、という標準事実。**正典外なら紙で 3 行** | **要記述** |
| **D-d** | 「moduli 体 $=\mathbf Q$ ⟹ 定義体 $=\mathbf Q$」の向き(障害)| 我々は逆向き(定義体 $\mathbf Q$ ⟹ moduli 体 $\mathbf Q$)しか使わないので**障害は不要** ✓ | **問題なし** |

> **⚠ D-a が「3 個」なら本提案は崩れる**。その場合は類ベクトルを**実際に測る**しかなく、そのためには $(X,Y,Z)$ の明示置換表現(工程 G-1(a))が必須になる。**⟹ D-a の確認を工程の第 1 番に置く。**

### 3.3 j-table の役

`sdc_twist_W_E_A10_9t1_20260730.json` の `j_values = [0,8,6,5,1,7,3,2,4]` は $\mathfrak F_0\xrightarrow{\sim}\mathbf Z/9$ のラベルづけ(`u_meas_m3_design_v1.md`【M3-b】)。これは **dessin の同定ではなく、同定された後の座標の固定**である。cert 上は `F0_labelling` としてハッシュ束縛するだけでよく、**C1′ の証明の重さはここには無い**(この点は既存設計どおり・変更なし)。

---

## 4. 工程 G-3 — 商 dessin → $W$-lift の一意 binding(P92-4 ③)

命題 U-LOC の構図: $W\xrightarrow{\ \deg2\ }C\xrightarrow{\ t\ }\mathbf P^1_t$、$W=C\times_{\mathbf P^1_t}\mathbf P^1_\lambda$、$\lambda\mapsto t$ は次数 ? の被覆($\lambda$ と $t$ の関係は U-LOC の $t=c\,s^{-9}(1+\cdots)$ で固定)。

> ### 【設計指定 C1P-FIB】fibre 積の monodromy 式を cert の必須欄にする
> $\bar M$ を $C\to\mathbf P^1_t$ の monodromy(基点上のファイバー $\bar\Lambda$ への作用)、$\mu$ を $\mathbf P^1_\lambda\to\mathbf P^1_t$ の monodromy(ファイバー $\Lambda'$ への作用)とすると、fibre 積の monodromy は $\bar\Lambda\times\Lambda'$ 上の作用の**推移成分**であり、群としては $\bar M\times\mu$ の部分直積。
> **cert 欄**: `fibre_product_binding = { base_map_t, base_monodromy_gens, lambda_over_t_degree, lambda_monodromy_gens, product_action_orbit_sizes, chosen_orbit_id }`。
> **一意性の主張はここで書く**: 「$\bar\Lambda\times\Lambda'$ の推移軌道が**ちょうど 1 個**」なら lift は一意(binding 完了)。複数なら `chosen_orbit_id` を**別の不変量で**固定する必要があり、そこが穴になる。**⟹ 軌道数の計算が binding の可否を決める。これも群論だけで済む(標本ゼロ)。**

**S4 での具体**: $\deg(W\to C)=2$、$\deg(C\to\mathbf P^1_t)=?$、$\deg\beta=9$。$9=2\times?$ にならないので、正確な次数は U-LOC の記述から拾って固定すること(**本書では数値を書かない** — 設計のみ)。

---

## 5. 工程 G-4 — digest 束縛(P92-4 ④)+ F92-5.2 の格上げ条件

F92-5.2 が `cross-checked` 格上げを差し戻した理由は 4 つ:(i) 生成プログラム欠(ii) 再現 command 欠(iii) source/input digest 欠(iv) helper 共有の非開示。**裁定 290 の `u_meas_m7b_v2_20260731.json` でこの 4 点は充足済**と報告されている。**C1′ 証明書は同じ 4 点を最初から満たす形で設計する。**

> ### cert schema 案 `c1prime-s4/v1`(必須欄)
> ```
> window_binding      : { P:"PSL(2,8)", |P|:504, M:9, N_ord:9, phi_image:"Hol(Z/9)",
>                         source_cert_sha256: <surj_s4_v2 の窓データ元> }
> monodromy_geometric : { group, order, T_label, proof_route:"G1-a"|"G1-c",
>                         explicit_XYZ:[perm,perm,perm], XYZ_product_is_identity: true,
>                         transitive: true, upper_bound_argument: <34群悉皆の receipt> }
> monodromy_arithmetic: { group, order, evidence:"frobenius_sample", sample_size,
>                         NOT_USED_FOR_C1PRIME: true }        # W92-5 への明示回答
> dessin_identification: { class_vector, diagonal:bool, out_orbit_structure:[...],
>                          rationality_argument:"C1P-DIAG"|"direct_class_vector",
>                          uniqueness_proved: bool }
> fibre_product_binding: { ... §4 ... , transitive_orbit_count, chosen_orbit_id }
> j_table_ref         : { cert:"sdc_twist_W_E_A10_9t1_20260730.json", sha256, j_values }
> model_binding       : { curve_eq, cusp, local_parameter, tame_normalization,
>                         uloc_cert_sha256, m7b_v2_cert_sha256 }
> provenance          : { generated_by, generated_by_sha256, reproduce_command,
>                         raw_log_sha256, helper_disjointness_statement }
> ```
> **④ の要点は「全部を 1 枚の cert に入れる」ことである** — P92-4 が「一体で束縛」と書いたのはそこ。現状は窓データ(surj_s4_v2)・j 表(sdc_twist)・モデル(u_meas_uloc)・値(u_meas_m7b_v2)が**4 枚に散っており、その間の同一性が主張されていない**。C1′ 証明書は**その 4 枚を束ねる 5 枚目**である。

---

## 6. `u7_meas_design_v1.md` C1′(7) 要件表との整合

| C1′(7) の項 | S4 での対応 | 一致/差分 |
|---|---|---|
| **a 窓束縛** | `window_binding`(§5) | **同型**。$P=G_7$ ↔ $P=\mathrm{PSL}(2,8)$ |
| **b passport 束縛** | 順序 passport $((9),(9),(9))$・$0$ 上が第 1 成分 | **同型** |
| **c ★ $[\alpha]$ 束縛**(回転指数比・n=7 の中核) | **`class_vector` が役を担う**(`u_meas_m3_design_v1.md`【M3-b】が既に明言) | **役は同じ・実装が違う**。n=7 は「3 類のどれか」を回転指数比で、S4 は「6 個のどれか」を類ベクトル(+ 本書 §3 の有理性)で |
| **d monodromy 束縛** | §2 の `monodromy_geometric`。n=7 は位数 196・可解・2 ブロック系 | **同型だが S4 のほうが難しい**($\mathrm{PSL}(2,8)$ は単純で塔が無い ⟹ **可解性という梃子が使えない**)。**⟹ S4 では §4 の fibre 積構造が n=7 の「塔束縛」の代役** |
| **e 塔束縛** | `fibre_product_binding`(§4) | **同型**($V\cong\mathbf P^1_m$ ↔ $\mathbf P^1_t$) |
| **f cusp 束縛** | `model_binding` の cusp/局所助変数 | **同型** |
| **g 正規化束縛** | 主係数の $M$ 乗倍のずれ = $[u_0^{-1}]_9$ の類での不変性 | **同型**(S4 側は F92-5.1 で既に $u_0^{-1}=-c_{\rm lead}$ の規約が固定済) |
| **h ★ 単数性を主張しない(全付値報告)** | `u_meas_m7b_v2` が既に全付値 $-3^65^9/2^8$ を報告済 | **S4 は既に充足**(むしろ n=7 の要件 h は S4 の教訓から来ている) |
| **i F91-5.4 モデル束縛** | `model_binding` の 4 点 | **同型** |

> **★ 逆輸入すべき差分が 1 つ**: **§2.2 の「幾何 monodromy / 算術 monodromy の 2 欄分離」は C1′(7) の要件 d にも無い。** n=7 の $\mathcal M_7$(位数 196・可解)でも Frobenius 標本を使うなら同じ混同が起きうる。**u7 設計書の次版で要件 d を 2 欄化することを進言する。**

---

## 7. 工程表(順序と依存)

| 順 | 工程 | 出力 | コスト | 依存 |
|---|---|---|---|---|
| **0** | 【C1P-0】`TransitiveGroup(9,27)` の位数確認(504 か 1512 か) | 記号の確定 | **1 分** | なし |
| **1** | 【D-a/D-b】6 個の dessin の類ベクトル表と $\mathrm{Out}=C_3$ 軌道構造 | 対角が 1 個か 3 個か | **10 分**(既存表を読む + GAP) | なし |
| **2** | 【G1-c 上界】次数 9 の推移群 34 個の悉皆:「9-巡回 3 個・積 1・推移」を満たす群のリスト | 幾何 monodromy の**上界の証明** | **30 分**(GAP) | なし |
| **3** | 【D-c】「dessin への $G_{\mathbf Q}$ 作用は $\mathrm{Out}(M_{\rm geom})$ を通る」の紙 3 行 | §3 の論法の正当化 | 紙 | 2 |
| **4** | 【C1P-DIAG】1+3 が揃えば C1′ の ②③ が同時に閉じる。揃わなければ G1-a へ | C1′ の可否判定 | 紙 | 1,3 |
| **5** | 【G1-a】fibre 積の monodromy 式 + 軌道数 → $(X,Y,Z)$ の明示置換表現 | ① の構成的証明・③ の一意性 | 中(紙+GAP) | U-LOC の次数データ |
| **6** | 【④】cert schema `c1prime-s4/v1` の実装と 4 枚の digest 束縛 | C1′ 証明書 | 実装(次段) | 0–5 |
| **7** | 第二系統: 5 と 2 の結果が一致することの照合(helper 非共有) | cross-check | 中 | 2,5 |

**入口条件**: 工程 0–4 は**測定値に一切触れない**(封印・接触遮断に抵触しない)。工程 5 以降は U-LOC の次数データを使うので、既公開分(裁定 269)の範囲で行う。

---

## 8. 予言(先出し・工程 1・2 の答え合わせ用)

- **P-C1-1**: 工程 2 の悉皆で、「3 個の 9-巡回・積 1・推移」を満たす次数 9 推移群は **$\mathrm{PSL}(2,8)$ を含む少数個**に限られる($C_9$、$C_3^2\rtimes\cdots$、$A_9$、$S_9$ 等が候補)。**$A_9$/$S_9$ が排除できるかが鍵** — 排除できなければ (G1-c) の上界は閉じない。
- **P-C1-2**: 工程 1 で対角 dessin は **1 個**(【FINDING U-2】の「唯一の」を額面通りに取る)。**外れ(3 個)なら §3 の新提案は撤回し、類ベクトルの直接測定に戻る。**
- **P-C1-3**: 【C1P-0】は **$\lvert\mathrm{TransitiveGroup}(9,27)\rvert=1512=\mathrm{P\Gamma L}(2,8)$** と出る(Sol の表記が正しく、工房の `u_meas_m1_passport_v1.md` の「9T27 $=\mathrm{PSL}(2,8)$」が誤記)。**根拠**: $\mathrm{PSL}(2,8)$ の 9 点作用は 2-推移だが $\mathrm{P\Gamma L}(2,8)$ が正規化子で、GAP の推移群ライブラリは通常 $\mathrm{PSL}$ を小さい番号に置く。**外れても損はない**(どちらでも工程 0 で確定する)。

---

## 10. ★ 工程 0/1/2 を実行した(`search/probe/wac_v1/c1prime_s4_designcheck_20260801.g`)— **提案 2 本が死に、C1′ の難しさが確定した**

予言を先に書いてから走らせた。**3 本中 2 本外れ**。正直に記録する。

### 10.1 予言の答え合わせ

| 予言 | 実測 | 判定 |
|---|---|---|
| **P-C1-3**: $\lvert 9\mathrm T27\rvert=1512=\mathrm{P\Gamma L}(2,8)$ | **$\lvert 9\mathrm T27\rvert=504=\mathrm{PSL}(2,8)$**。$\mathrm{P\Gamma L}(2,8)=\mathrm{PSL}(2,8){:}C_3$ は **9T32**(位数 1512) | **外れ**。**工房の `u_meas_m1_passport_v1.md`(9T27 = PSL(2,8))が正しく、便 92 の「9T27 = PΓL(2,8)」が誤記**。【C1P-0】は工房側の勝ち |
| **P-C1-1**: 「9-巡回 3 個・積 1・推移」を満たす次数 9 推移群は少数で、$A_9/S_9$ を排除できるかが鍵 | **34 群中 18 群が該当し、その中に 9T33 $=A_9$ と 9T34 $=S_9$ が入っている** | **外れ**(悪い方に)。**⟹ 経路 (G1-c) の上界は原理的に閉じない** |
| **P-C1-2**: 6 個のうち対角はちょうど 1 個 | **的中**。18 個の $P$-dessin のうち対角は 3 個((1,1,1),(2,2,2),(3,3,3))で、それらは $\mathrm{Out}=C_3$ の**ひとつの軌道**をなす ⟹ **6 個の dessin(= $N_{S_9}(P)$-共役類)のうち対角はちょうど 1 個** | **的中** |

### 10.2 得られた完全なデータ

- $P=\mathrm{PSL}(2,8)$(9T27・位数 504・単純)、$N_{S_9}(P)=\mathrm{PSL}(2,8){:}C_3$(位数 1512、$[N:P]=3$)。
- 位数 9 の元 168 個・$P$-類 **3 個**(各 56)。
- 順序三つ組 $(X,Y,Z)$(全て位数 9・$XYZ=1$・$\langle X,Y\rangle=P$)は **9072 個**。
- **$P$-共役で 18 個の dessin**(各軌道 504 = 正則 ⟹ 自己同型自明)、**$N_{S_9}(P)$-共役で 6 個** ✓ 既存の「6 個」と一致。
- **18 個の類ベクトルはすべて相異なる**(27 通り中 18 通りが実現)。$\mathrm{Out}=C_3$ は 18 個に**自由に**作用し、6 軌道。

### 10.3 ⚠ 【C1P-DIAG】は**成立しない**(§3 の提案を撤回)

**Fried の branch cycle lemma** により、$\sigma\in G_{\mathbf Q}$ は dessin の分岐巡回を $(X,Y,Z)\mapsto(X^{\chi(\sigma)},Y^{\chi(\sigma)},Z^{\chi(\sigma)})$(共役を除く)へ送る(分岐点 $0,1,\infty$ は $\mathbf Q$-有理なので順序は不変)。$\langle g\rangle\cong C_9$ 上で $N_P(\langle g\rangle)$ は二面体位数 18 ゆえ共役は反転しか起こさず、3 類は $\{g^{\pm1}\},\{g^{\pm2}\},\{g^{\pm4}\}$。$\chi$ 倍は $(\mathbf Z/9)^\times/\{\pm1\}\cong C_3$ を通って**3 類を巡回置換**する — これは $\mathrm{Out}(P)=C_3$ と**同じ $C_3$** である。

> **⟹ 類ベクトルの $C_3$-軌道は Galois 不変量であり、それが 6 個の dessin を完全に分離する。従って $G_{\mathbf Q}$ は 6 個を動かさない — すなわち**
> $$\boxed{\ \textbf{6 個の dessin はすべて moduli 体 }\mathbf Q\ \textbf{をもつ}\ }$$
> **⟹ 「$\mathbf Q$ 上定義されるから対角である」は言えない。§3 の【C1P-DIAG】は撤回する。**

**これは同時に、C1′ が本質的に難しいことの説明でもある**: 6 個の競合はすべて $\mathbf Q$-有理なので、**どんな算術的不変量も 6 個を分けない**。分けられるのは組合せ(類ベクトルそのもの)だけである。W92-5 の懸念は、単に「標本が足りない」のではなく、**算術側からの補強が原理的に効かない**という形で正しい。

### 10.4 改訂された工程表

| 順 | 工程 | 状態 |
|---|---|---|
| 0 | 【C1P-0】記号 | **完了**。9T27 $=\mathrm{PSL}(2,8)$、9T32 $=\mathrm{P\Gamma L}(2,8)$。**便 92 の表記を訂正する必要がある** |
| 1 | 【D-a/D-b】6 個の構造 | **完了**(§10.2)。対角は 6 個中 1 個 ✓ |
| 2 | 【G1-c】上界の悉皆 | **完了・失敗**。$A_9,S_9$ を含む 18 群が passport を許す ⟹ **経路 (G1-c) は使えない** |
| 3 | 【D-c】Galois 作用 | **完了・提案を否定**(§10.3)。branch cycle lemma で $G_{\mathbf Q}$ は 6 個を動かさない |
| 4 | 【C1P-DIAG】 | **撤回** |
| **5** | **【G1-a】fibre 積からの構成的 monodromy** | **⟹ 唯一の生き残り経路。ここに資源を集中せよ** |
| 6 | ④ cert schema | 5 の後 |

> **⟹ P92-4 への回答(改訂)**: ①(monodromy の証明)と ③(商 dessin → $W$-lift の一意 binding)は**別々に閉じられない。両方とも「$W$ を fibre 積として構成し、$(X,Y,Z)$ を群論の式で書き下す」という 1 本の工程に統合される。** ②(class vector)はその工程の**出力**(構成した三つ組の類ベクトルを読むだけ)になり、独立の証明対象ではなくなる。④ はその後の事務。
> **⟹ 本書 §2.3 の推奨順(G1-a 主・G1-c 副)は、副が消えて「G1-a のみ」に変わる。第二系統は G1-b(resolvent)しか残らない。**

**⚠ 追加の注意**: $A_9/S_9$ が passport を許すということは、**「passport + 標本 Frobenius」だけでは幾何 monodromy が $A_9$ や $S_9$ でないことすら言えない**。F92-5 が挙げた「240 個の Frobenius cycle type が許容型内」という証拠は、**18 群のどれとも整合する**。これも cert に明記すべき負の事実である。

**検算**: `search/probe/wac_v1/c1prime_s4_designcheck_20260801.g`(GAP 単系統・測定値非接触・封印非接触)。

---

## 9. 格付け・残る穴

| 項目 | 格 |
|---|---|
| §1 の C1′ の論理構造 | **設計**(既存の理解の整理) |
| §2.2 幾何/算術 monodromy の分離 | **設計提案(新規)**。W92-5 への構造的回答 |
| §2.3 (G1-c) 上界の悉皆(34 群) | **実行済・失敗**($A_9,S_9$ を含む 18 群が passport を許す・§10.2)。**経路として廃棄** |
| §3【C1P-DIAG】有理性 ⟹ 対角 | **実行済・撤回**(§10.3)。6 個すべて moduli 体 $\mathbf Q$ ⟹ 算術は 6 個を分けない |
| §10 の 3 件の実測(9T27 の位数・18 群・6 個の構造と Galois 不変性) | **機械(GAP 単系統)+ branch cycle lemma(古典)** |
| 便 92 の「9T27 $=\mathrm{P\Gamma L}(2,8)$」 | **誤記と判定**(9T27 $=\mathrm{PSL}(2,8)$・9T32 $=\mathrm{P\Gamma L}(2,8)$)。次便で訂正 |
| §4 fibre 積 binding | **設計**(U-LOC の帰結の cert 化) |
| §5 cert schema | **設計** |
| §6 u7 との整合 + 逆輸入提案 | **設計** |
| C1′ そのもの | **依然 UNKNOWN**。本書は**閉じ方の設計**であって証明ではない |
| $\mathrm{Ih}_{S4}$ 全射 | **candidate のまま**(F92-5.3 / W92-5) |
