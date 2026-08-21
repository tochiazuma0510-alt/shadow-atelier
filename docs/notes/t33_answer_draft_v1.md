# T-33 / T-34 / T-35 への回答(起草・対話帳エントリ番号 **T-36** 予定)— cofinal STEP / SINGLE / 非可換 S^t / 最小 typed obstruction / Relative-Frattini-3 jump / κ+Θ

**状態札: 数学者起草・司令塔検分前・Sol 未監査**
起草: Claude 数学者 / 2026-08-18 / 委嘱 = 司令塔(T-33 §4 の 4 問 + T-34 の評価 + T-35 の κ+Θ 評価 + 発案札との合成)
非接触宣言: 封印 3 量・$u$ の値と平方類・$c$ の値・sealed $K^{(5)}$ インスタンスに非接触。以下で $u=2m+1$ は**形式変数**としてのみ現れる。
NAME-COLLIDE: 本書の $X=\mathrm{ML}(M)$, $A$, $I_K$, $\mathrm{ML}(K)$ は **T-33/T-29 の定義**に従う(gentle/$B_3$ 側の $GT(M)$・$\widehat{GT}_{\rm gen}$ とは同構造別系)。$K(5)$ は Stasheff associahedron であり sealed $K^{(5)}$ とは同名別物。
格付け: 本書の新規結果はすべて **paper candidate(紙上証明・Sol 監査前・cross-checked ではない・verified でもない)**。機械計算は一切行っていない。

---

## 0. 裁定一覧表

| 設問 | 内容 | 裁定 | 中身 |
|---|---|---|---|
| **1** | matched tower + q=3 correction + 手術/トーサー + B5/K(5) horn から **任意の elementary abelian first-bad chief section の STEP** が出るか | **obstruction 定式化**(証明も型付き反例も出ない)+ **部分的な正の定理 2 本** | ①T-33 §3 の literal な STEP は **B4-B と同値**(定理 T33-T1)なので「STEP を補題として証明する」道は存在しない。②elementary abelian に制限した $\mathrm{STEP}_{ab}$ は真の部分命題だが、**非可換 chief 不可避性**(補題 T33-L7)により単独では B4-B に到達しない。③新しい十分条件 **SYL3**(定理 T33-T2)は typed lift の構成なしに $I_L=X$ を出す有限判定。④要求された「正確な characteristic/functorial 仮説と可換図」は §2.4 に明示(そこで**未証明の要石は (CH-p) 一本**に縮約される) |
| **2** | 同じ固定 $x$ に対する SINGLE(x) を与える **inverse-system selection theorem** があるか | **証明**(ただし「そのような定理は存在し得ない」ことの証明) | SINGLE(x) は cofinal family 上で **B4-B と同値**(定理 T33-T1)。単調性(T33-L1)+ one-outside(固定入力 2)+ cofinality だけで $\forall K\,I_K=X$ が出る。従って SINGLE(x) は STEP の弱形ではなく**同一命題**であり、「より安い selection theorem」は原理的に無い。副産物: 安定化補題 T33-L3(A 側は有限証明書を持ち、B 側は持たない) |
| **3** | 非可換 chief factor $S^t$。A5/V4 型反模型を排除する braid/GT 固有の条件は何か。literal A.18/B5 から従うか | **obstruction 定式化 + 1 件の圏違い指摘(証明つき)** | ①**A5/V4 反模型は圏違い**である(補題 T33-L8): 2008 Thm A.1 + Def 2.6 により typed lift の障害は「3 本の残差を $\Lambda$ 内で消せるか」だけであり、Wells の *compatible pair の存在* 問題は GT 側には**発生しない**。従って「centerless Wells が存在を与えない」ことは $S^t$ 段の障害ではない。②ただしこれは **A.18/B5 から従わない** — 従うのは **Thm A.1(Fresse coherence)+ Def 2.6 + (3.24)** からである(設問 3 後半への直接回答: **No**)。③残る本当の障害は非線形残差方程式の可解性で、これは open。④$S^t$ 段は迂回不能(補題 T33-L7)。⑤T-35 が提案する代替(κ+Θ)については**本表最終行**を参照 — そちらも A.18/B5 からは構成できず、しかも手前に未着工の一階部分がある |
| **4** | B4-B を止める最小の actual typed obstruction の定式化 + 有限入力の列挙 | **定式化**(2 件: OBS★-3 と OBS★-S) | §5 に、群・作用・coface・correction domain・comparison map をすべて列挙した有限問題として定式化。さらに **SYL3 版**(位数だけで決まる軽い証明書)を併記 |
| **5**(T-34) | Relative-Frattini-3 jump theorem($\Phi_3(H_r)$, $V_r=H_1(H_r;\mathbf F_3)$)の評価 | **中核は証明(支持)。軽量化 (a) 正当。判定 (b) 正当 — 欠けていた証明を補完。注意 (c)(d) 確認 + 1 点訂正。ただし重い留保 1 件** | 支配補題(T34-J1)は正しく、$\Phi_3(H_4)$ は**この層の厳密な最小共通下界**(最適)。(a) の軽量化は正当(T34-J3)。(b) の同値は真で、証明は Magnus/Crowell 完全列 + Tor 消滅から出る(T34-J4)。**訂正 1**: ambient は「誤り」ではなく「健全だが劣化」— $N_{PB_4}(3)$ は支配しないが $N_{PB_4}(3e_M)$ は支配する(T34-J2)。**訂正 2**: specialization は pruning 専用ではなく**厳密な非所属証明書**になる(T34-J6)。**追加提案**: 群環を一切使わない等価な語証明書 CERT-Φ-WORD(T34-J5)。**留保**: T-34 は吸収定理ではなく **∀→∃ の再指標化**であり、数学的難度は減らず一点に集中する。かつ一層分のみ(T34-J10) |
| **合成** | **T-34 × A-4(UNIFORM-WITNESS)= T-34 の条件を一回の有限 run にできるか** | **半分成立・半分不成立**(§6.8) | **(a) 型としては well-defined(成立)**: ambient witness の literal pair を $\Phi_3(H_4)$ 段で読むことは全 gate が意味を持つ(T34-J11)。$J_3$(注意 c1)とは衝突せず、むしろ $J_3$ が正しい評価場。nonsplit(注意 c2)とも衝突しない(語で評価するため)。$m$ 側の friendly gate は**ほぼ無料**($\Phi_{\rm ord}/H_{\rm ord}$ が 3 冪)。onto gate だけ自動でない ⟹ **FC-6**。**(b) 「同一 schema がそのまま通る」は不成立**: pentagon 残差が $\Phi_3(H)$ に入るのは余次元 $d\sim10^7$ の一致で、ambient positive はそれを一切拘束しない。T-30 §2 の係数独立性は **untwisted** complex の話で actual 残差の座を拘束しない。⟹ **1 run は宝くじであって計画ではない**。**(c) 正しい合成**: $V=H/\Phi_3(H)$ が elementary abelian なので**この層の問題は $\mathbf F_3$ 上アフィン**(T34-J12)。従って「疎な証明書を探索」ではなく「**疎 $\mathbf F_3$ 線形系を解く**」— 次元 $\sim10^7$・非零 $\sim10^8$ で block-Wiedemann 級の射程。これにより T-34 の `positive-semidecision` が **decision** に上がる。**(d) A-7 の双対**: 単一 replay 失敗は何も証明しない。**線形系の非可解性 + outside $g$ の全走査**なら設問 4 の形式を満たす |
| **合成 2** | **A-5(BOUNDED-COMPLEXITY-KÖNIG)/ A-4 強形** | **却下(反証つき)** | 機構は修理すれば妥当($W_j$ は**減少列**なので鳩の巣ではなく減少列の交叉で共通元が出る)。だが結論が強すぎる: **定理 T33-L10** — 単一 literal pair が cofinal 族の全段で shadow なら $2m+1=\pm1$、すなわち pentagon と両 hexagon を $B_3/PB_4$ で**厳密に**満たす離散対の存在を主張することになる。これは B4-B より真に強い。⟹ **A-5 と A-4 の全段形は経路として却下**(§6.9) |
| **κ+Θ**(T-35) | 各 arity の $V_r=H_1(H_r;\mathbf F_3)$ 内の stable subquotient $\kappa_r:U1_r/U0_r\cong$ sign-window と stabilizer-reflecting comparison $\Theta$ は literal A.18/B5 data から構成できるか | **構成できない(No)。ただし T-35 が挙げた障害とは別の、より基本的な理由による。加えて T-35 の反模型に 2 件の射程限定を付す** | **①T-35 の 2 つの論拠を独立検算 → 両方正しい**(Frobenius 相互律 $\mathrm{Hom}_X(\mathrm{Ind}_A^X1,\mathrm{sgn})=\mathrm{Hom}_A(1,\mathrm{sgn}|_A)=0$;$A_5$-$C_2^2$ 反模型の $H_1(-;\mathbf F_3)=0$)。**②$\Theta$ の「stabilizer-reflecting」部分は実は無償**: 固定入力 1($A\le\mathrm{Stab}$)と $[X:A]=3$ 素数から $\mathrm{Stab}\in\{A,X\}$、すなわち軌道は 1 か 3(補題 T35-Θ1)。**③真の急所は $\kappa$ でも $\Theta$ でもなく「$X$ が $V_r$ に作用する」という前提**: $X$ の元は $PB_4$ の自己同型ではなく対 $(m,f)$ で $H_r$ を保つ保証がない。$V_r$ に自然に作用するのは $G_r=B_4/H_r$ だけ。作用は「$H_r$ を保つ shadow」からしか出ず、それは構成対象そのもの ⟹ **循環**(補題 T33-L11)。**④$\kappa$ の唯一の自然な braid 側候補**は permutation sign $\varepsilon:B_4\to S_4\to\{\pm1\}$($\mathrm{Hom}(B_4,C_2)=C_2$ で一意)。ただし T-30 §4 (4) が禁じた同一視そのもの。**⑤射程限定 1**: T-35 の反模型の消滅機構は「kernel perfect + quotient が 3′-群」に依存する。$\mathrm{Out}(S)\supseteq C_3$(札 B-2 の $PSL(2,8)$)なら $H_1(-;\mathbf F_3)\ne0$ となり**反模型は実系に転写されない**(補題 T35-R1)。**⑥射程限定 2**: 実系では $V_r$ は $\sim10^7$ 次元(T-34 自身の見積)で、$H_1=0$ という消滅は起こり得ない(補題 T35-R2)。**⑦前提警報**: sign-window は $X\twoheadrightarrow S_3$($A$ 非正規)を前提とする。$A\trianglelefteq X$ なら coset 作用の像は $C_3$ で $\mathbf F_3^\times\cong C_2$ への非自明指標が存在せず、**sign-window は概念として存在しない**。T-29 §6・T-31 §3・T-35 はいずれもこの前提を共有 ⟹ **FC-1 は 3 便すべての load-bearing 前件**(補題 T33-L12) |

---

## 1. 記号・固定入力・本書で新たに証明したものの一覧

### 1.1 記号(T-33/T-29 準拠)

$$\mathcal I_4:=\{K\trianglelefteq B_4:\ [B_4:K]<\infty,\ K\le PB_4,\ K\ \text{isolated}\},\qquad \mathcal I_4(M):=\{K\in\mathcal I_4: K\le M\}.$$
$$X:=\mathrm{ML}(M),\quad A:=\mathrm{im}(G_{\mathbf Q}\to X),\quad I_K:=\mathrm{im}\bigl(R_{K,M}:\mathrm{ML}(K)\to X\bigr),$$
$$|X|=972=2^2\cdot3^5,\qquad |A|=324=2^2\cdot3^4,\qquad [X:A]=3 .$$
$K_{PB_3}:=\bigcap_{j}(d^j)^{-1}(K)$(2008 (2.4)・五 coface)、$K_{PB_2}$ は (2.5)、$K_{\rm ord}=[PB_2:K_{PB_2}]$。

### 1.2 固定入力(T-33 §2 逐語・再監査しない)

(1) $A\le I_K$ と $I_K$ の群性(2008 Prop. 3.7 / 3.11)(2) one-outside lemma (3) 段ごとの seed 差は許容 (4) 真に cofinal な全段で $I_K=X$ なら compactness で profinite lift (5) matched pure-power tower の functorial descent/cofinal infrastructure (6) q=3 stage の typed positive(GHA run 32135808950)と全 literal side gate/settlement。

### 1.3 本書で新たに証明した命題(すべて paper candidate)

| 番号 | 内容 | 使うもの |
|---|---|---|
| T33-L1 | **単調性** $L\le K\Rightarrow I_L\le I_K$ | 2008 Prop. 3.7 (3.7) |
| T33-L2 | **二値性** $I_K\in\{A,X\}$ | 固定入力 1,2 |
| T33-L3 | **上閉性と安定化** — $\{K:I_K=X\}$ は上に閉じ、$\{I_K\}$ は単一の $K_0$ で最小値 $P$ を達成 | L1, L2, $X$ 有限 |
| **T33-T1** | **崩壊定理**: B4-B ⟺ STEP ⟺ SINGLE(x) ⟺ $\forall K\ I_K=X$ ⟺ DEEP(x) | L1–L3, 固定入力 2,4 |
| T33-L4 | **探索標的の縮小(無条件)**: $I_K=X\iff I_K\cap(X^2\setminus A)\ne\varnothing$。$X^2=\mathrm{Syl}_3(X)$、$|X^2\setminus A|=162$ | 凍結 $X$ 構造(157bu §2) |
| **T33-T2** | **SYL3 判定法**: $3\nmid[\mathrm{ML}(K):\mathrm{im}\,R_{L,K}]\Rightarrow I_L=X$。逆に $I_L=A\Rightarrow 3\mid[\cdots]$ | Sylow + Lagrange + L4 |
| T33-L5 | $X^2\subseteq I_K\iff I_K=X$(**UTL の仮説は目標と同値**、過剰に強くない) | L4 |
| T33-L6 | **相対 core tower**: $\Lambda_j(K):=\bigcap\{U\trianglelefteq_{\rm open}K:[K:U]\le j\}$ による塔は characteristic・matched・cofinal(**Zelmanov 不要**) | 初等 |
| T33-L7 | **非可換 chief の不可避性(強化版)**: 任意の downward-cofinal family は $M/C$ が非可解な $C$ を含む。isolatedization による回避は不可能 | 152_b4_chief_obstruction §4 + cofinality |
| **T33-L8** | **GT の lift 問題は Wells 問題ではない**: 障害は 3 本の残差のみ。compatible pair の存在問題は生じない | 2008 Thm A.1, Def 2.6, (3.24) |
| T33-L9 | **残差の $p$ 群性**: $K/L$ が $p$ 群なら correction domain $\Lambda(L)$ の 3 成分すべてが $p$ 群 | (2.4)(2.5) |
| **T33-L10** | **定数 schema の不可能性**: 単一 literal pair $(m,f)\in\mathbf Z\times F_2$ が cofinal 族の全段で shadow なら $2m+1=\pm1$ | friendly gate (2.36) + 全リンク数窓 |
| **T33-L11** | **$X$ の $V_r$ への作用は循環**: $X$ の元は $PB_4$ の自己同型でないので $H_r$ を保つ保証がなく、$V_r$ への作用は構成対象からしか出ない | Cor 2.7/2.13 |
| T33-L12 | **sign-window は $A$ 非正規を前提**: $A\trianglelefteq X$ なら coset 像 $C_3$ には $\mathbf F_3^\times$ への非自明指標がない | 初等 |
| T35-V1/V2 | T-35 の 2 論拠の独立検算(Frobenius / $A_5$-$C_2^2$ 反模型) | Frobenius 相互律・完全群 |
| T35-Θ1 | $\Theta$ の stabilizer-reflecting 性は固定入力 1 と素指数から**無償** | 固定入力 1 + $[X:A]=3$ |
| T35-R1 | T-35 反模型の射程限定 1: $\mathrm{Out}(S)\supseteq C_3$ なら $H_1(-;\mathbf F_3)\ne0$ | 完全群の $E^{ab}$ 計算 |
| T35-R2 | T-35 反模型の射程限定 2: 実系では $V_r\ne0$($\sim10^7$ 次元) | T-34 の見積 + $PB_4^{ab}\otimes\mathbf F_3=\mathbf F_3^6$ |
| T34-J11 | ambient witness の $\Phi$ 段 replay は**型として well-defined**(全 gate が意味を持つ・$J_3$/nonsplit と非衝突・friendly はほぼ無料) | Def 2.6/2.9/2.19, T33-L9 |
| T34-J12 | **$\Phi$ 層の問題は $\mathbf F_3$ 上アフィン** ⟹ 探索ではなく疎線形系 | $V$ elementary abelian |
| T34-J1 | **支配補題**: $\Phi_3(H)=\bigcap\{L: H/L\ \text{elem. ab. }3\}$(層の厳密な最小共通下界) | 初等 |
| T34-J2 | ambient の正確な位置づけ($N_{PB_4}(3)$ は支配しない / $N_{PB_4}(3e_M)$ は支配する / relative が最適) | 初等 |
| T34-J3 | T-34 の軽量化 (a) の正当性 | 2008 Def 3.2, Def 3.12/(3.24), Prop 3.7 |
| **T34-J4** | **Fox 判定の証明**: $w\in\Phi_3(H_r)\iff\nabla_3(\tilde w)\in\mathrm{im}\,D_2$ | Magnus/Crowell 完全列 + $\mathrm{Tor}$ 消滅 |
| T34-J5 | **CERT-Φ-WORD**: 群環を使わない等価な語証明書 | J4 の系 |
| T34-J6 | specialization は**厳密な非所属証明書**(pruning 専用ではない) | 右完全性 |
| T34-J7 | 注意 (c1) の誤差の向きは保守側($\Phi_3(H_3)\subseteq J_3$) | 初等 |
| T34-J10 | T-34 は吸収定理ではなく再指標化(留保) | T1 |

---

## 2. 設問 1 — elementary abelian first-bad chief section の STEP

### 2.1 まず、T-33 §3 の literal な STEP は補題ではない

**補題 T33-L1(単調性).** $L\le K\le M$ をすべて isolated とすると $I_L\le I_K$。
*証明.* 2008 Prop. 3.7 (3.7) より $R_{L,M}=R_{K,M}\circ R_{L,K}$。よって
$I_L=R_{K,M}\bigl(R_{L,K}(\mathrm{ML}(L))\bigr)\subseteq R_{K,M}(\mathrm{ML}(K))=I_K$。∎

**補題 T33-L2(二値性).** $K\in\mathcal I_4(M)$ に対し $I_K\in\{A,X\}$。
*証明.* 固定入力 1 より $A\le I_K\le X$ で $I_K$ は部分群。$[X:A]=3$ は素数なので $[X:I_K][I_K:A]=3$。∎($A$ の正規性は不要。)

**補題 T33-L3(上閉性と安定化).**
(i) $\{K\in\mathcal I_4(M): I_K=X\}$ は $\mathcal I_4(M)$ の中で**上に閉じる**($L\le K$ かつ $I_L=X$ なら $I_K=X$)。
(ii) $P:=\bigcap_{K\in\mathcal I_4(M)}I_K$ は**単一の** $K_0\in\mathcal I_4(M)$ で達成される($I_{K_0}=P$、かつ $\forall K\le K_0:\ I_K=P$)。
*証明.* (i) は L1。(ii): $X$ は有限群なので部分群は有限個。よって $K_1,\dots,K_n$ を選んで $\bigcap_i I_{K_i}=P$ とできる。$\mathcal I_4$ は下方 directed(2008 Prop 3.6 + Cor 3.5)なので $K_0\le K_1,\dots,K_n$ なる $K_0\in\mathcal I_4(M)$ が取れ、L1 より $I_{K_0}\subseteq\bigcap_i I_{K_i}=P$。逆の包含は $P$ の定義。∎

**定理 T33-T1(崩壊定理).** 固定入力 1–4 のもとで次は同値。
1. **B4-B**($P=X$、すなわち固定 $x\in X\setminus A$ が genuine)。
2. **STEP**(T-33 §3 逐語): 任意の isolated $H\le M$ と任意の「次の」isolated refinement $L\le H$ について $I_H=X\Rightarrow I_L=X$。
3. **SINGLE(x)**(T-33 §3 逐語): ある固定 $x\in X\setminus A$ と downward-cofinal な isolated family $\mathcal C$ が存在し、$\forall C\in\mathcal C:\ F_C(x)\ne\varnothing$。
4. $\forall K\in\mathcal I_4(M):\ I_K=X$。
5. **DEEP(x)**(発案札 A-2 の中間命題): $\forall K\in\mathcal I_4(M)\ \exists K'\le K$ isolated with $F_{K'}(x)\ne\varnothing$。

*証明.*
(4)⟹(1): $P=\bigcap I_K=X$。固定入力 4(compactness、157cq §5–6 で CLOSED)より B4-B。
(1)⟹(4): $P=X$ かつ $P\le I_K$ より $I_K=X$。
(4)⟺(2): (4)⟹(2) は自明。(2)⟹(4): $I_M=X$($R_{M,M}=\mathrm{id}$)。任意の $K\in\mathcal I_4(M)$ に対し $M/K$ は有限群なので $K$ と $M$ の間の isolated 対象は有限個、よって極大鎖 $M=H_0>H_1>\cdots>H_r=K$($\mathcal I_4$ 内)が取れる。STEP を $r$ 回適用。
(3)⟹(4): $C\in\mathcal C$ に対し $F_C(x)\ne\varnothing$ すなわち $x\in I_C$、$x\notin A$ なので L2 より $I_C=X$。任意の $K\in\mathcal I_4(M)$ に対し cofinality で $C\le K$ なる $C\in\mathcal C$ を取り L1 で $I_K\supseteq I_C=X$。
(4)⟹(3): 自明(任意の cofinal family で成立)。
(4)⟺(5): (4)⟹(5) 自明。(5)⟹(4): $K$ に対し $K'\le K$ で $F_{K'}(x)\ne\varnothing$ なら $I_{K'}=X$(L2)、L1 で $I_K=X$。∎

> **設問 1 への一次裁定.** T-33 §3 の literal な STEP は B4-B と論理的に同値である。よって「STEP を先に閉じてから B4-B へ」という工程は存在しない。**STEP の証明 = B4-B の証明**、**STEP の型付き反例 = B4-A の証明書**である。委嘱が求める「証明または型付き反例」は、そのまま研究全体の決着を求めていることになる。どちらも本書では出ない。

### 2.2 では設問 1 の実質は何か — $\mathrm{STEP}_{ab}$ は真の部分命題である

T-33 §4.1 は「**任意の elementary abelian first-bad chief section に対する** STEP」を問うている。これは §3 の STEP を弱めた

$$\mathrm{STEP}_{ab}:\quad L\le H\ \text{isolated},\ H/L\ \text{が}\ B_4\text{-chief かつ elementary abelian}\ \Longrightarrow\ (I_H=X\Rightarrow I_L=X)$$

であり、T1 の同値には入らない(non-abelian 段が量化から外れているため)。従ってこれは**正当な部分目標**である。ただし:

**補題 T33-L7(非可換 chief の不可避性・強化版).** 任意の downward-cofinal family $\mathcal C\subseteq\mathcal I_4(M)$ は、$M/C$ が非可解であるような $C\in\mathcal C$ を含む。従って $M$ から $C$ へ至る任意の $B_4$-chief 系列は非可換 chief factor $S^t$ を少なくとも一つ通る。
*証明.* `sol/luna_reply_152_b4_chief_obstruction_v2.md` §4 は、$F=\langle x_{12},x_{23}\rangle\le PB_3$ の有限指数自由部分群から $A_5$ 商を作り、2008 Prop 3.9(A) で $PB_4$ へ延長し、$B_4$-normal core $J$ を取って $M/(M\cap J)$ が非可解部分群を含むことを示した(同 §4 (F))。$U:=M\cap J$ は開かつ $B_4$-normal で $M/U$ は非可解。2008 Cor 3.5 により isolated $U'\le U$ を取れば $M/U'\twoheadrightarrow M/U$ なので $M/U'$ も非可解。cofinality より $C\le U'$ なる $C\in\mathcal C$ があり、$M/C\twoheadrightarrow M/U'$ なので $M/C$ は非可解。有限群の chief 系列が非可解群を分解するなら、少なくとも一つの因子は非可換 characteristically simple すなわち $S^t$。∎
*(§4 は「isolatedization が選んだ section を壊し得る」という留保を付けていた。上の議論はその留保を消す: cofinal family は**どのみち** $U'$ の下へ潜らねばならないから、isolatedization による回避は原理的にできない。)*

> ⟹ **$\mathrm{STEP}_{ab}$ を完全に閉じても B4-B には到達しない。** 設問 3 は選択肢ではなく必須経路である。

### 2.3 $\mathrm{STEP}_{ab}$ に対して本書が出せる正の結果

#### (i) 探索標的の縮小(無条件)

**補題 T33-L4.** 凍結構造 $X\cong((C_9\times C_9)\rtimes C_6)\times C_2$(157bu §2)のもとで $X^2:=\langle x^2:x\in X\rangle$ は位数 $243=|X|_3$、$X$ の**唯一の(正規)Sylow 3-部分群**である。さらに $|A\cap X^2|=81$、$|X^2\setminus A|=162$ で、任意の isolated $K\le M$ に対し
$$I_K=X\iff I_K\cap(X^2\setminus A)\ne\varnothing .$$
*証明.* $|X^2|=243$ は 157bu §2 の凍結計算。$|X|_3=3^5=243$ なので $X^2\in\mathrm{Syl}_3(X)$、かつ $X^2$ は characteristic だから正規、よって唯一。$X^2\not\le A$(Lagrange: $243\nmid324$)なので $AX^2$ は $A$ を真に含む部分群、すなわち $AX^2=X$、よって $|A\cap X^2|=|A||X^2|/|X|=81$。最後の同値: ($\Leftarrow$) 外側元を含むので L2 より $I_K=X$。($\Rightarrow$) $I_K=X\supseteq X^2\setminus A\ne\varnothing$。∎

> **運用上の含意**: outside witness の探索は **648 個の外側 roof すべてではなく、Sylow 3-部分群内の 162 個**に限ってよい。しかもそれらはすべて 3 冪位数である。$A$ の $X$ 内正規性(未確定・157ae:51 参照)は不要。

#### (ii) SYL3 判定法 — typed lift を作らずに $I_L=X$ を出す

**定理 T33-T2(SYL3).** $L\le K\le M$ をすべて isolated とし、$I_K=X$ とする。$J:=\mathrm{im}\bigl(R_{L,K}:\mathrm{ML}(L)\to\mathrm{ML}(K)\bigr)$ と置く。
1. $3\nmid[\mathrm{ML}(K):J]$ ならば $I_L=X$。
2. 逆に $I_L=A$ ならば $3\mid[\mathrm{ML}(K):J]$。
同値な形: $\ v_3(|\mathrm{ML}(L)|)-v_3(|\ker R_{L,K}|)=v_3(|\mathrm{ML}(K)|)\ \Rightarrow\ I_L=X$。

*証明.* $\rho:=R_{K,M}$ は $I_K=X$ より全射で、$\rho(J)=I_L$(L1 の証明と同じ合成則)。
(1) $3\nmid[\mathrm{ML}(K):J]$ なら $|J|_3=|\mathrm{ML}(K)|_3$、よって $J$ は $\mathrm{ML}(K)$ の Sylow 3-部分群 $S$ を含む。全射準同型は Sylow を Sylow に写すので $\rho(S)\in\mathrm{Syl}_3(X)$、$|\rho(S)|=3^5=243$。$\rho(S)\subseteq\rho(J)=I_L$。もし $I_L=A$ なら Lagrange で $243\mid324$ となり矛盾。L2 より $I_L=X$。
(2) 全射 $\rho$ と $H\le G$ に対し $[\rho(G):\rho(H)]\mid[G:H]$(剰余類の全射 $G/H\twoheadrightarrow \rho(G)/\rho(H)$)。$I_L=A$ なら $[X:\rho(J)]=3$ なので $3\mid[\mathrm{ML}(K):J]$。∎

> **意義**: 「固定 $x$ の上に typed lift を作る」ではなく「**位数の 3-part が落ちない**」を確かめれば $I_L=X$ が出る。しかも abelian/non-abelian、$p$ の値、chief factor か否かを一切問わない。これは既在 UTL の「$X^2\subseteq I_K$ を typed に作れ」(157bu, 157br §2)より弱い十分条件である。

**補題 T33-L5.** $X^2\subseteq I_K\iff I_K=X$。
*証明.* L4 の最後の同値の特別な場合。∎
*(⟹ UTL の仮説「$X^2\subseteq I_K$」は目標より真に強い仮説ではなく、目標と**同値**である。UTL を「強すぎる迂回」として捨てる理由はない。)*

#### (iii) 残差の $p$ 群性 — 何が $p$-primary で、何がそうでないか

**補題 T33-L9.** $L\le K$ を $B_4$-normal 開部分群、$V:=K/L$ を $p$ 群とする。このとき
$$K_{PB_3}/L_{PB_3}\hookrightarrow V^{5},\qquad K_{PB_2}/L_{PB_2}\hookrightarrow (K_{PB_3}/L_{PB_3})^{4},$$
特に $K_{PB_3}/L_{PB_3}$ と $L_{\rm ord}/K_{\rm ord}=[K_{PB_2}:L_{PB_2}]$ はいずれも $p$ 冪。
*証明.* $u\mapsto(d^j(u)L)_{j=0..4}$ は $K_{PB_3}\to V^5$ を定め(定義 (2.4) より $d^j(K_{PB_3})\subseteq K$)、核はちょうど $K_{PB_3}\cap\bigcap_j(d^j)^{-1}(L)=L_{PB_3}$。$PB_2$ 側は (2.5) で同様。∎

**系(correction domain の型).** $K$ 上の shadow $[(m,f)]$ を $L$ へ持ち上げる候補集合は
$$\Lambda(L)\;=\;\bigl(m+K_{\rm ord}\mathbf Z/L_{\rm ord}\mathbf Z\bigr)\;\times\;\bigl(fK_{PB_3}/L_{PB_3}\bigr)$$
で、$K/L$ が $p$ 群なら $|\Lambda(L)|$ は $p$ 冪。また shadow 条件の残差は
$$\beta=(\beta_{\rm hex1},\beta_{\rm hex2},\beta_{\rm pent})\in\bigl(K_{PB_3}/L_{PB_3}\bigr)^2\times(K/L)$$
の 3 成分のみ(補題 T33-L8 参照)で、これも $p$ 群の中に住む。

### 2.4 要求された「正確な characteristic/functorial 仮説と可換図」

設問 1 後半が求めているのは「任意の section が universal q=3 correction の quotient/image として受け取るための仮説」である。正確に書くと次の **(CN1)–(CN4)** になる。

$H$ を現在の段、$W:=H/\Phi_3(H)=H_1(H;\mathbf F_3)$(**universal 層**)、$V:=H/L$ を任意の elementary abelian $\mathbf F_3$ chief section、$\pi:W\twoheadrightarrow V$ を標準射影($\Phi_3(H)\le L$ による — T34-J1)とする。$G:=B_4/H$ とし、$W,V$ は $\mathbf F_3[G]$-加群。

- **(CN1) 支配**: 任意の $L$($H/L$ elem. ab. 3)について $\Phi_3(H)\le L$。**⟹ 証明済み(T34-J1)。**
- **(CN2) 係数関手性**: 残差と correction が係数加群について自然:
$$\beta_V=\pi_*(\beta_W),\qquad D_V\circ\pi_*=\pi_*\circ D_W .$$
- **(CN3) admissible の押し出し**: $c\in C_{\rm adm}(W)\Rightarrow\pi_*(c)\in C_{\rm adm}(V)$(hexagon/marking/charming/onto/settlement の各条件が射影で保たれる)。
- **(CN4) matched coface**: 五 coface $d^j:PB_3\to PB_4$ と六 coface $PB_4\to PB_5$ が $\Phi_3$ を保つ、すなわち $d^j(H_3)\subseteq H_4\Rightarrow d^j(\Phi_3(H_3))\subseteq\Phi_3(H_4)$。**⟹ 証明済み**(準同型は $3$ 乗を $3$ 乗へ、交換子を交換子へ送る)。

**可換図(要求された形)**:

$$
\begin{array}{ccc}
C_{\rm adm}(W) & \xrightarrow{\ D_W\ } & R_{A18}(W)\\
\ \ \downarrow{\scriptstyle \pi_*} & & \ \ \downarrow{\scriptstyle \pi_*}\\
C_{\rm adm}(V) & \xrightarrow{\ D_V\ } & R_{A18}(V)
\end{array}
\qquad\text{かつ}\qquad \pi_*(\beta_W)=\beta_V .
$$

**命題 T33-P1(条件付き).** (CN1)–(CN4) のもとで、$W$ 段で $D_W(c_0)=-\beta_W$ の解 $c_0\in C_{\rm adm}(W)$ が一つあれば、任意の elementary abelian $\mathbf F_3$ chief section $V$ で $D_V(\pi_*c_0)=-\beta_V$。
*証明.* $D_V(\pi_*c_0)=\pi_*D_W(c_0)=-\pi_*\beta_W=-\beta_V$。∎

> **正直な評価**: この命題は**線形化された言い換えに過ぎない**。(CN1) は単調性($\Phi_3(H)\le L$)の別表現であり、命題 T33-P1 の内容は T33-L1 の内容と同じである。すなわち「universal 層で解けば下位はすべて解ける」は自明な下降であり、**難しさは universal 層で解くこと自体に完全に移る**。これが T-34 の評価(§6)と同じ結論である。

### 2.5 未証明の要石 —(CH-p)

$\mathrm{STEP}_{ab}$ を「characteristic 3 だけ」に厳密に縮約する道は一本ある。

**(CH-p) 障害写像の crossed-homomorphism 性.** $L\le K$ isolated、$V=K/L$ が $p$ 群とする。$J=\mathrm{im}(R_{L,K})$ に対し、写像
$$\mathrm{ob}:\ \mathrm{ML}(K)\longrightarrow \mathcal O,\qquad J=\mathrm{ob}^{-1}(0)$$
が、ある有限 $p$ 群 $\mathcal O$ への **crossed homomorphism**($\mathrm{ob}(g_1g_2)=\mathrm{ob}(g_1)+g_1\cdot\mathrm{ob}(g_2)$)として実現できるか。

**命題 T33-P2(条件付き).** (CH-p) が成り立てば $[\mathrm{ML}(K):J]=|\mathrm{im\,ob}|$ は $p$ 冪。従って $p\ne3$ のとき T33-T2 (1) より $I_L=X$。
すなわち **(CH-p) ⟹ $\mathrm{STEP}_{ab}$ は characteristic 3 の section だけに縮約される**(= 設問 1 が求めた characteristic 仮説の正体)。

**現状**: 補題 T33-L9 により**障害が住む場所はすべて $p$ 群である**ことは証明済み。欠けているのは「$\mathrm{ob}$ が加法的(crossed)である」ことだけで、これは合成則 (2.52) $m=2m_1m_2+m_1+m_2$, $fN=f_2N\cdot T^{PB_3}_{m_2,f_2}(f_1)$ が残差にどう作用するかを書き下せば決まる**有限の紙作業**である。私はこれを完了していないので **【GAP: CH-p】** として明示する。

> **【文献要請】** 困難: 「groupoid/operad の有限商の間の同型の持ち上げ障害が、係数群への crossed homomorphism として実現されるか(coprime action で消えるか)」。欲しい結果の型: 群の Wells 完全列(Wells 1971)の **groupoid 版 / operad 自己同型版**、または「$\mathrm{Aut}$ ではなく生成元-関係式で定義された持ち上げ問題」に対する障害の加法性定理。これが降りれば (CH-p) が閉じ、設問 1 が characteristic 3 のみに縮約される。

### 2.6 設問 1 の裁定(まとめ)

- literal STEP: **B4-B と同値**(T33-T1)⟹ 補題として証明することは不可能。
- $\mathrm{STEP}_{ab}$: 委嘱の道具立て(matched tower + q=3 correction + 手術/トーサー + B5/K(5) horn)からは**導けない**。理由は 3 つ:
  1. universal 層への functorial 下降(§2.4)は自明な単調性の言い換えで、新しい情報を持たない。
  2. $p\ne3$ の section を落とすには (CH-p) が要る(未証明・§2.5)。
  3. $\mathrm{STEP}_{ab}$ が全部閉じても L7 により B4-B に届かない。
- ただし本書は**新しい十分条件 SYL3(T33-T2)**と**探索標的の 648→162 縮小(T33-L4)**を提供する。これらは typed lift の構成を要求しない。
- 型付き反例は出せない(出せればそれは B4-A の証明書であり、研究の決着)。

---

## 3. 設問 2 — SINGLE(x) の inverse-system selection theorem

**裁定: 証明。ただし「そのような定理は存在し得ない」ことの証明である。**

定理 T33-T1 (3)⟺(4)⟺(1) が示すとおり、SINGLE(x) は STEP の弱形ではない。証明の核は 3 行である:

> cofinal family $\mathcal C$ の各 $C$ で $F_C(x)\ne\varnothing$ ⟹ $x\in I_C\setminus A$ ⟹(one-outside)$I_C=X$ ⟹ 任意の isolated $K$ に対し $C\le K$ なる $C$ を取れば(単調性)$I_K\supseteq I_C=X$。

つまり「**一つの $x$ だけ**」「**cofinal family の上だけ**」という二重の弱化は、one-outside lemma(固定入力 2)と単調性(T33-L1)によって**同時に消える**。従って:

- 「各段非空でなく、cofinal family 上の実 fibre と遷移写像を明記した selection theorem」を作っても、その結論はそのまま $\forall K\ I_K=X$、すなわち B4-B である。**逆向きの節約は生じない。**
- 遷移写像は明記できる(157cq §5 の $b_{K',K}$、そこで CLOSED)。問題は写像ではなく**各段の非空性**であり、それが唯一の内容である。

### 3.1 発案札 A-2(DEEP)の採否

**採用する。** ただし正確な位置づけは「STEP と SINGLE の中間命題」ではなく「**三者すべてと同値な第 5 の言い換え**」である(T33-T1 (5))。証明義務は減らないが、**設計上は有用**: DEEP(x) は「任意の窓 $K$ に対して、$K$ の下のどこか一段で勝てばよい(その一段を自分で選んでよい)」という形なので、探索は「与えられた窓を攻める」ではなく「攻めやすい深い窓を自分で作る」設計になる。T33-L6 の相対 core tower はまさにその「作る」側の道具である。
発案札 A-2 の自己申告(「禁止短路① に当たらないか」)への回答: **当たらない**。禁止されているのは coarser→finer の伝播(surjectivity の自動伝播)であり、L1 は finer→coarser の**写像が実在する向き**の包含である。

### 3.2 副産物 — A 側と B 側の非対称性(安定化補題 T33-L3 の含意)

- $\{I_K\}$ は単一の $K_0$ で最小値に達する(L3 (ii))。よって **B4-A が真なら、それを目撃する単一の isolated $K$ が存在する**(有限証明書が存在する)。
- 一方 B4-B には有限証明書が存在しない(Cor 3.13 の全称量化、既在: 157bz UNIFORM_325, sol_reply_151 §5)。
- ⟹ **現行の計算キャンペーンは原理的に B4-B を確認できない。反証(空 fibre 発見)のみ可能である。** B4-B へ至る唯一の道は一様定理であり、T33-T1 によりそれは B4-B そのものである。これは戦略上の一級の情報だが、悲観の材料ではない: **どちらに転んでも重い**(A なら「初の fake charming GT-shadow」— 2008 Question 4.6 の未解決問題の解決、B なら井原予想の反例)。

### 3.3 c² 反例(gentle 側 sol_reply_151 §4.3 / 157cc:91–114)との関係

gentle 側の非 cofinality 反例は「固定した窓 $W,K_2$ との交叉で作った族 $X_s$ が $c^2$ を必ず含み、$c^2\notin L=M\cap N_5^{\rm cyc}$ の下に潜れない」という形だった。**相対 core tower(T33-L6)はこの型の失敗を構造的に起こさない**: 塔の各段は「固定の窓との交叉」ではなく「前段の characteristic 部分群」として定義されるので、指数によって定義される任意の窓の下へ必ず潜る。

**補題 T33-L6(相対 core tower).** $K\le M$ 開・$B_4$-normal に対し
$$\Lambda_j(K):=\bigcap\{U\trianglelefteq_{\rm open}K:\ [K:U]\le j\}$$
と置き、$K_0:=M$, $K_{j+1}:=\Lambda_j(K_j)$ とする。このとき
1. 各 $K_j$ は開かつ $B_4$-normal($\Lambda_j$ は characteristic)。
2. **matched**: $d(K^{(r)})\subseteq K^{(r+1)}$ を満たす coface $d$ に対し $d(\Lambda_j(K^{(r)}))\subseteq\Lambda_j(K^{(r+1)})$。
3. **cofinal**: 任意の開 $B_4$-normal $U\le M$ に対しある $j$ で $K_j\le U$。
*証明.* 1. $K$ が位相的有限生成($\widehat{PB_4}$ の開部分群)なので指数 $\le j$ の開部分群は有限個、よって $\Lambda_j(K)$ は開。$\mathrm{Aut}(K)$ で不変なので characteristic、$K$ が $B_4$-normal なら $\Lambda_j(K)$ も。
2. $U\trianglelefteq K^{(r+1)}$、$[K^{(r+1)}:U]\le j$ とすると $d^{-1}(U)\cap K^{(r)}$ は $K^{(r)}$ の正規開部分群で指数 $\le j$。よって $\Lambda_j(K^{(r)})\subseteq d^{-1}(U)$。全ての $U$ で交わって主張を得る。
3. $M/U$ を位数 $n$ とし、$B_4$-normal な鎖 $M=U_0>U_1>\cdots>U_\ell=U$($\ell\le\log_2 n$)を取る。$J:=\max(n,\ell)$ と置く。$K_{J+i}\le U_i$ を $i$ について帰納する。$i=0$ は塔が降下列だから成立。$K_{J+i}\le U_i$ なら $U_{i+1}\cap K_{J+i}$ は $K_{J+i}$ の正規開部分群で指数 $\le[U_i:U_{i+1}]\le n\le J+i$、よって $K_{J+i+1}=\Lambda_{J+i}(K_{J+i})\le U_{i+1}$。∎

**注(既在との衝突回避).**
- `sol/luna_reply_152_relative_cofinal_v1.md` の `RELATIVE_COFINALITY_FALSE_IN_GENERAL` は「$C\cap W\le N$ かつ $CW=G$ なる ambient $W$ が取れるか」(= 直積因子問題)についての反証であり、**本補題とは別命題**。本補題は $M$ の内部を降りるだけで、$C$ に transverse な部分群を要求しない。
- `sol/luna_reply_152_b4_7adic_verbal.md` の「7V-COFINAL を『7-primary だから自動』としてはいけない」も本補題と両立する。実際、**単一素数の verbal 族は cofinal でない**: $N_K(p)$ を反復して得る塔の商は反復 $p$ 群拡大なので可解であり、$\widehat{PB_4}$ が pro-solvable でない($PB_4\twoheadrightarrow PB_3\twoheadrightarrow F_2\twoheadrightarrow A_5$)ことに反する。T33-L6 は指数で刻むので、この壁を持たない。
- また T33-L6 は Zelmanov(制限 Burnside)を使わない。$N_K(q)$ 型の pure power tower を composite $q$ で使うと $K/N_K(q)$ の有限性に RBP が要る点は、独立の留保として記録する。

---

## 4. 設問 3 — 非可換 chief factor $S^t$

**裁定: obstruction 定式化。ただし枠組みについて 1 件の訂正(証明つき)を提出する。**

### 4.1 訂正 — A5/V4 反模型は圏違いである

**補題 T33-L8.** $L\le K$ を $NFI_{PB_4}(B_4)$ の元、$[(m,f)]\in GT^\heartsuit(K)$ とする。$[(m,f)]$ が $L$ へ survive するとは、$(m',f')\in\Lambda(L)$(§2.3 (iii) の候補集合)であって
- (2.18)(2.19) が $B_3/L_{PB_3}$ で成立、
- (2.20) が $PB_4/L$ で成立、
- $T^{PB_3},T^{PB_2}$ が全射(2008 Prop 2.10 によりこれで $T^{PB_4}$ 全射も従う)、
- charming(代表 $f'_1\in[F_2,F_2]$ かつ $T^{F_2}$ 全射)

を満たすものが存在することと**同値**である。特に **$\mathrm{Aut}(PB_4/K)$ の元を $\mathrm{Aut}(PB_4/L)$ へ持ち上げる Wells 型の「compatible pair の存在」問題は生じない。**
*証明.* 2008 Theorem A.1(= Fresse Thm 6.2.4)により $\mathrm{PaB}$ は $\alpha,\beta$ で生成され、全関係式は pentagon (A.13) と二 hexagon (A.14)(A.15) の帰結。よって $T_{m',f'}(\alpha)=[\alpha\cdot\mathfrak m(f')]$, $T_{m',f'}(\beta)=[\beta\cdot\mathfrak m(x_{12}^{m'})]$ が $\mathrm{PaB}^{\le4}\to\mathrm{PaB}^{\le4}/\!\sim_L$ の射を定める条件はちょうど Def 2.6 の 3 本(2.18)(2.19)(2.20)であり、全射性条件が Def 2.9、charming が Def 2.19。survive 写像 (3.24) は「同じ代表対を読む」写像なので、$L$ 上の対の存在が survive と同値。∎

**含意.** T-31 §3 の反模型
$$N=A_5,\quad Q=C_2^2,\quad 0\ne\alpha:Q\to\mathrm{Out}(A_5)=C_2,\quad E_\alpha=\{(u,q):\mathrm{sgn}(u)=\alpha(q)\},\quad \mathrm{Aut}(Q)=S_3$$
は「$\mathrm{Aut}(Q)$ の外側元が abstract kernel $[\alpha]$ の $\mathrm{Out}$-共役類を動かすので compatible lift がない」という構図である。補題 T33-L8 により、GT 側の lift 問題にはこの段階が存在しない — candidate は最初から**対 $(m',f')$** であって、抽象自己同型ではない。よって:

> **A5/V4 反模型は、GT typed 系における $S^t$ 段の障害の反模型では「ない」。** それは $\mathrm{Aut}$-持ち上げ問題の反模型である。両者を同一視すると、存在しない障害を守ることになる。

**設問 3 後半への直接回答**: この条件は **literal A.18/B5 data からは従わない**。従うのは **2008 Theorem A.1(Fresse coherence)+ Definition 2.6 + Definition 3.12/(3.24)** からである。A.18 は coface の生成元値表であって、生成元-関係式による $\mathrm{PaB}$ の記述ではない。

### 4.2 では $S^t$ 段の本当の障害は何か

補題 T33-L8 により、$V=K/L\cong S^t$ の段で解くべきは次の**非線形有限方程式**である。$\Lambda(L)$ を候補集合、$\beta_g:\Lambda(L)\to (K_{PB_3}/L_{PB_3})^2\times(K/L)$ を残差写像とすると
$$\exists\,g\in\mathrm{ML}(K)\ \text{with}\ \rho(g)\in X^2\setminus A,\quad \exists\,\lambda\in\Lambda(L):\quad \beta_g(\lambda)=(1,1,1)\ \wedge\ \Sigma(\lambda) ,$$
($\Sigma$ = 全射性 + charming の side gate)。$V$ が非可換なので $\beta_g$ は加群写像ではなく、$\beta_g^{-1}(1,1,1)$ はトーサーでもない。**線形代数が使えないこと**が $S^t$ 段の実体であり、centerless Wells の一意性/存在の話ではない。

### 4.3 それでも $S^t$ 段に効く 3 本の道具(いずれも本書で確立)

1. **SYL3(T33-T2)は $S^t$ 段でもそのまま使える。** 位数の 3-part しか見ないので、$V$ が可換か否かを問わない。$S^t$ 段の $I_L=X$ を、非線形方程式を解かずに位数比較で出せる可能性がある。
2. **探索標的は 162 個(T33-L4)。** $S^t$ 段でも同じ。
3. **不可避性(T33-L7)。** 迂回設計に予算を割かない根拠。

### 4.4 T-35 の検算 — 2 つの論拠はいずれも正しい

**T35-V1(Frobenius 論拠).** $X=S_3$, $A=C_2=\langle s\rangle$, $\Omega=X/A$, $P=\mathbf F_3[\Omega]=\mathrm{Ind}_A^X\mathbf 1$。
$\mathrm{Hom}_X(P,\mathrm{sgn})\cong\mathrm{Hom}_A(\mathbf 1,\mathrm{Res}_A\mathrm{sgn})=0$(Frobenius 相互律。$\mathrm{Res}_{C_2}\mathrm{sgn}$ は非自明指標、$\mathrm{char}\,\mathbf F_3\ne2$ ゆえ半単純)。同様に $\mathrm{Hom}_X(\mathrm{sgn},P)\cong\mathrm{Hom}_A(\mathrm{Res}_A\mathrm{sgn},\mathbf 1)=0$。
なお $P$ の内部構造 $0<C<I<P$ と $I/C\cong\mathrm{sgn}$ は正しい(検算: $s(e_1-e_2)=-(e_1-e_2)$、$r(e_1-e_2)-(e_1-e_2)=2e_2-e_1-e_3\equiv3e_2=0\bmod C$)。**すなわち sgn は $P$ の subquotient ではあるが、部分加群でも商でもない。** ⟹ **T-35 の第 1 論拠は正しい。**

**T35-V2(型付き反模型).** $S=A_5$, $Q=C_2^2$, $E_\alpha=\{(u,q)\in S_5\times Q:\mathrm{sgn}(u)=\alpha(q)\}$。$E_\alpha\to Q$ は全射で核 $A_5$。三つの $Q$ 上 fibre product $E$ は核 $A_5^3$、商 $Q=C_2^2$。$A_5$ は完全なので $E^{ab}$ は $Q^{ab}=C_2^2$ の商、従って 2-群。よって $H_1(E;\mathbf F_3)=E^{ab}\otimes\mathbf F_3=0$。⟹ **T-35 の第 2 論拠も正しい。orbit/sign 障害が非零でも actual elementary-$\mathbf F_3$ 窓が空になり得る。**

> **裁定: T-35 の STOP は正しい。** 「orbit → 抽象 sign 加群」は GO だが「orbit/torsor/flatness → actual $H_1$ 窓」は一般には成立しない。私はこれを支持する。

### 4.5 T-35 の射程限定 2 件 — 反模型は実系に転写されない

**補題 T35-R1($\mathrm{Out}(S)$ に 3 が入ると消滅機構が働かない).** T-35 の反模型で $H_1(E;\mathbf F_3)=0$ となった理由は、核が完全群で商 $Q$ が 3′-群だったことに尽きる。$\mathrm{Out}(S)\supseteq C_3$ の場合、例えば $S=PSL(2,8)$($\mathrm{Out}=C_3$)、$Q=C_3^2$、$\alpha:Q\to C_3$ を三本取れば、$E_\alpha=\{(u,q)\in P\Gamma L(2,8)\times Q:\ \bar u=\alpha(q)\}$ の fibre product $E$ は核 $PSL(2,8)^3$・商 $C_3^2$ で
$$H_1(E;\mathbf F_3)=C_3^2\otimes\mathbf F_3\ne0 .$$
⟹ **detector は沈黙しない。T-35 の反模型は $\mathrm{Out}(S)$ が 3′-群である場合に限った現象である。**
発案札 B-2 の見立て(実系の最初の非可換 chief は $PSL(2,8)$・$\mathrm{Out}=C_3$)が正しければ、**反模型は実系に転写されない**。⟹ **FC-4(最初の非可換 chief の同定)の優先度を最上位に上げるべき根拠。**

**補題 T35-R2(実系では $V_r\ne0$).** $PB_4^{ab}\otimes\mathbf F_3=\mathbf F_3^6\ne0$ であり、$H_r$ は $\widehat{PB_4}$ の開部分群なので $V_r=H_1(H_r;\mathbf F_3)$ は Nielsen–Schreier により次元 $\le5[\widehat{PB_4}:H_r]+1$ の非零空間。T-34 自身が「数千万次元」と見積もっている。⟹ **反模型の「$H_1=0$ だから窓がない」という状況は実系では起こらない。**

> **従って T-35 の正確な射程は**「**形式的な** bridge(orbit/torsor/Wells/flatness だけから actual 窓へ)は存在しない」であって、「実系で detector が沈黙する」ではない。これは T-30 §4 と `152_b4_chief_obstruction_v2` §5 が繰り返してきた「actual data を使え」と同じメッセージであり、私はこの読みを提案する。

### 4.6 κ + Θ は literal A.18/B5 data から構成できるか — **No**。ただし急所は別の場所にある

**(1) $\Theta$ の "stabilizer-reflecting" 部分は無償である.**
**補題 T35-Θ1.** $X$ が或る typed datum の集合に作用しているとする。固定入力 1 より arithmetic 元はその datum を安定化するので $A\le\mathrm{Stab}_X(\text{datum})$。$[X:A]=3$ は素数なので $\mathrm{Stab}\in\{A,X\}$、すなわち軌道長は 1 か 3。$\mathrm{Stab}=A$ は軌道長 3 と同値。∎
⟹ T-35 が $\Theta$ に求めた性質のうち「stabilizer を $A$ と同定する」部分は**追加の数学を要しない**。$\Theta$ の実質的内容は「**非可換 A.18 incompatibility を窓の非零 residual へ送る**」の方だけである。

**(2) しかしその前に、$X$ が $V_r$ に作用するという前提が未確立である(真の急所).**
**補題 T33-L11(循環).** $g\in X=\mathrm{ML}(M)$ は対 $[(m,f)]$ であって $PB_4$ の自己同型ではない。2008 Cor 2.7 の $T^{PB_4}_{m,f}$ は $PB_4\to PB_4/N$ という**商への**準同型であり、$PB_4$ の自己準同型ではない(そもそも生成元の像が braid 関係式を $PB_4$ の中で満たすとは限らない — それを法 $N$ で要求するのが hexagon 条件である)。従って $g$ は $H_r$ を保つとは限らず、$V_r=H_1(H_r;\mathbf F_3)$ に自然には作用しない。$V_r$ に自然に作用するのは $G_r=B_4/H_r$(共役)だけであり、$X\to G_r$ の標準射はない。
$g$ が $V_r$ に作用するのは、$g$ が或る $L\le\Phi_3(H_r)$ 上の shadow $z$ に持ち上がり、かつ $T_z\in\mathrm{Aut}(PB_4/L)$ が $H_r/L$ を保つときに限る。**その持ち上げの存在こそが構成しようとしている当のものである** ⟹ 循環。∎

> ⟹ **κ と Θ は「$X$ の $V_r$ への作用」の上に建てる二階部分であり、一階部分が未着工である。** T-35 の裁定行 `PB4-specific kappa + Theta comparison: OPEN / exact next target` は正しいが、**next target の中身は κ/Θ の構成ではなく、その手前の作用の構成**である、というのが私の裁定。

**(3) $\kappa$ の唯一の自然な braid 側候補と、それが無償でない理由.**
1 次元 $\mathbf F_3[G_r]$-加群の指標は $G_r\to\mathbf F_3^\times\cong C_2$ の準同型である。$B_4^{ab}=\mathbf Z$(生成元 $\sigma_i$)なので $\mathrm{Hom}(B_4,C_2)=C_2$、その唯一の非自明元は**置換符号** $\varepsilon:B_4\to S_4\to\{\pm1\}$ である。$H_r\le PB_4=\ker(B_4\to S_4)$ なので $\varepsilon$ は $G_r$ に降りる。⟹ **$\kappa$ の唯一の自然な候補は $\varepsilon$-isotypic 部分である。**
しかし T-30 §4 (4) が明示的に禁じたのは、まさにこの $\varepsilon$(strand relabelling 由来)と $X/A$ の coset sign の同一視である。⟹ **$\kappa$ は「$\varepsilon$-窓を取る」だけなら構成できるが、それが T-29 §6 の相対 sign と同じものであることは示されていない。その同定を担うのが $\Theta$ であり、従って $\kappa$ と $\Theta$ は独立な 2 要求ではなく、$\Theta$ が $\kappa$ の意味を決める。**

**(4) literal A.18/B5 から従うか: No.**
- A.18 は五 coface の生成元値表、B5/K(5) は associahedron の胞体データで、いずれも $B_4,PB_4,PB_5$ の**組合せ論**のみ。$G_{\mathbf Q}$ も $A$ も含まない。
- $\Theta$ が要求する 2 性質のうち、stabilizer 部分は固定入力 1 から無償(T35-Θ1)、残る「非可換 incompatibility → 非零 residual」は $H_r$ の actual な $\mathbf F_3$-homology の中の位置を決める主張であり、**A.18/B5 は残差がどの窓に落ちるかを一切拘束しない**(これは T-30 §4 が「actual chief layer では transport が同一とは限らない/prefix conjugation が Fox 微分を捻る」と述べた点と同じ)。
- ⟹ **κ+Θ は literal A.18/B5 data からは従わない。**

**(5) 前提警報 — sign-window の存在自体が FC-1 に依存する.**
**補題 T33-L12.** $X$ の $\Omega=X/A$ への coset 作用の像を $T\le S_3$ とする。$T=C_3$($A\trianglelefteq X$)なら、$\mathbf F_3^\times\cong C_2$ への $C_3$ からの非自明準同型は存在しないので、**sign 指標は存在しない**。sign-window が意味を持つのは $T=S_3$($A$ 非正規)の場合だけである。∎
T-29 §6($G=S_3$, $H=\langle s\rangle$)・T-31 §3(permutation module から $0\ne[b]\in H^1(X,A;\mathbf F_{3,\rm sign})$)・T-35(同上)は**いずれもこの前提を共有**している。⟹ **FC-1(「$A$ は $X$ で正規か」)は 3 便すべての load-bearing 前件であり、未確定のまま 3-primary sign 路線を進めるべきでない。** 既在の指摘は `157ad:104`, `157ae:51`(非正規なら coset 作用の像は $S_3$)。

### 4.7 発案札 B-1(ARITH-STAB)・B-5(BURAU-FROB)の採否(T-35 反映後)

- **B-1(軌道 1 か 3 の二分)**: **骨格は採用・機構は却下**。
  - **採用する部分**: 「中間がない(軌道 1 か 3)」は**正しく、しかも無条件**である。ただしそれは Wells 由来ではなく、$S^t$ 段でも成り立つ **T33-L2(one-outside の帰結 $I_L\in\{A,X\}$)** そのものであり、typed datum への $X$ の作用を仮定するなら **T35-Θ1** である。
  - **却下する部分**: 「軌道 3 ⟹ 空 fibre = A-witness」という**検出**の枝。理由は二重: (i) 補題 T33-L8 — GT 側に $\mathrm{Aut}$ 持ち上げ段階がないので $[\omega]$ 保存は問うべき量でない;(ii) **T-35 — 仮に Wells 像を認めても、軌道 3 が actual elementary-$\mathbf F_3$ 窓に映る保証がない(反模型では窓が空)**。⟹ **一般形では STOP(T-35 が正)。**
  - **復活しうる条件**: 補題 T35-R1 により、実系の $\mathrm{Out}(S)$ が $C_3$ を含む(B-2 の $PSL(2,8)$ 見立て)なら反模型の消滅機構は働かない。さらに T33-L11 の循環を解く必要がある。⟹ **B-1 は「FC-4 で $\mathrm{Out}\supseteq C_3$ が確認され、かつ $X$ の $V_r$ 作用が構成できた場合にのみ復活」**という条件つき札に格下げして保持。
  - なお B-1 が期待した「決定手続き」は、**T33-T2(SYL3)が無条件かつ片側で既に提供している**(位数の 3-part が落ちなければ段は閉じる)。$S^t$ 段の実務的決定力はこちらに移すのが妥当。
- **B-5(Burau specialization)**: **$\kappa$ の実現候補としてのみ採用検討・$\Theta$ の候補としては却下**。
  - $\Theta$ 候補として読むのは誤り: $\Theta$ の stabilizer 部分は無償(T35-Θ1)、残る部分は actual residual の位置に関する主張で、線形表現の specialization はそれを与えない。
  - 一方 **$\kappa$ 側には効き得る**: reduced Burau の $\mathbf F_8$ 特殊化は $G_r$ の線形実現を与えるので、$V_r$ の中の $\varepsilon$-isotypic 部分(= (3) の唯一の自然な候補)を**具体的に切り出す道具**になり得る。ただし札自身の破綻点 (i)(同名別物リスク・CV-9 型判読が要る)は残る。
  - ⚠ 封印: $u$ の residue **値**・平方類に踏み込む設計は行わない。本書では $u$ を形式変数としてのみ扱った。

### 4.8 設問 3 の裁定

- braid/GT 固有の条件は**存在する**(補題 T33-L8)が、それは A5/V4 を排除する条件というより「**A5/V4 が排除すべき対象でない**」ことを示す構造的事実である。
- それは **literal A.18/B5 からは従わない**(Thm A.1 + Def 2.6 + (3.24) から従う)。設問 3 後半への直接回答は **No**。
- T-35 が提案した代替(κ + Θ)も **literal A.18/B5 からは構成できない**(§4.6 (4))。しかも κ/Θ の手前に「**$X$ が $V_r$ に作用する**」という未着工の一階部分がある(T33-L11)。⟹ **設問 3 の exact next target は κ/Θ ではなく、その作用の構成である**、というのが本書の対案。
- T-35 の STOP 自体は**正しい**(§4.4 で独立検算)。ただし射程は「形式的 bridge の不在」であって「実系での detector 沈黙」ではない(T35-R1/R2)。$\mathrm{Out}(S)\supseteq C_3$ なら反模型は転写されない ⟹ **FC-4 最優先**。
- 3-primary sign 路線(T-29 §6・T-31 §3・T-35 に共通)は $A$ が $X$ で**非正規**であることを暗黙の前件にしている(T33-L12)⟹ **FC-1 は 3 便の共通 load-bearing 前件**。
- $S^t$ 段の実際の障害(非線形残差方程式の可解性)は **OPEN**。§5 の OBS★-S に定式化する。実務的な片側決定力は **T33-T2(SYL3)** が無条件に提供する。
- 「$S^t$ が first-bad になる最小状況の型」: T33-L7 の構成が最小候補を与える —— $M\twoheadrightarrow$(自由部分の $A_5$ 商)$\to$ $B_4$-core $U$ を取り、$M/U$ の $B_4$-chief 系列で最初に現れる非可換因子 $S^t$。実系では発案札 B-2 が「最初の非可換 chief は $PSL(2,8)$・$\mathrm{Out}=C_3$」と見立てており、$[X:A]=3$ と共鳴する。**T35-R1 により、この見立ての真偽が T-35 反模型の転写可否を決める。** literal 確認は FC-4。

---

## 5. 設問 4 — B4-B を止める最小の actual typed obstruction

以下は「これが立てば B4-B は偽(= B4-A)」という形の**最小の有限判定**である。2 件を挙げる(elementary abelian 版と非可換版)。どちらも **T33-L8 の形**(3 本の残差 + side gate)で書けており、Wells 型の量は一切現れない。

### 5.1 OBS★-3(elementary abelian $\mathbf F_3$ 層・即実装可能)

**入力(すべて有限)**

| 項目 | 中身 |
|---|---|
| 群(coarse) | $Q_4:=PB_4/H$、$Q_3:=B_3/H_{PB_3}$($H$ = authenticated q=3 stage $K_*$ or 現段) |
| 群(fine) | $E_4:=PB_4/\Phi_3(H)$、$E_3:=B_3/J_3$、$J_3=\bigcap_{j=0}^4(d^j)^{-1}\Phi_3(H)$(T-34 の注意どおり $\Phi_3(H_3)$ で代用しない) |
| 係数 | $V:=H/\Phi_3(H)=H_1(H;\mathbf F_3)$、$\mathbf F_3[B_4/H]$-加群 |
| 作用 | $B_4/H$ の $V$ への共役作用。$H$ は $V$ に自明に作用($V$ は可換なので) |
| coface | 五 $d^j:PB_3\to PB_4$(A.18 の生成元値)、六 $PB_4\to PB_5$(B5 syzygy 用)。matched 性は T33-L6 (2) / CN4 |
| correction domain | $\Lambda:=\bigl(H_{\rm ord}\mathbf Z/\Phi_{\rm ord}\mathbf Z\bigr)\times\bigl(H_{PB_3}/J_3\bigr)$(m 補正 × f 補正) |
| comparison map | $\rho=R_{H,M}:\mathrm{ML}(H)\to X$(outside 判定用)、および 162 個の標的集合 $X^2\setminus A$(T33-L4) |
| side gate | $2m'+1\in(\mathbf Z/\Phi_{\rm ord})^\times$、$T^{F_2}$ 全射、$f'$ の $[F_2,F_2]$ 代表可能性、settlement |

**判定**
$$\mathrm{OBS\star\text{-}3}(H)\ :\iff\ \forall g=[(m,f)]\in\mathrm{ML}(H)\ \text{with}\ \rho(g)\in X^2\setminus A,\ \forall\lambda\in\Lambda\ \text{with}\ \Sigma(\lambda):\ \beta_g(\lambda)\ne(1,1,1).$$
成立すれば、$\Phi_3(H)$ の下の**ある** isolated $L$(実際は $\Phi_3(H)$ 自身を含む全ての elem. ab. 3 段)で $I_L=A$、従って **B4-A**。
不成立(= 一つでも解がある)なら T-34 の jump が発火して当該層は全滅する(T34-J1)。

**⟹ この一つの有限判定は、どちらに転んでも決着する。** 規模の見積りと軽量化は §6 を参照。

### 5.2 OBS★-S(最初の非可換 chief 段)

**入力**: 上の表の $\Phi_3(H)$ を、T33-L7 が構成する $U'$($M/U'$ 非可解)へ差し替え、$V=H/L\cong S^t$(最初の非可換 $B_4$-chief factor)とする。correction domain は同じ形 $\Lambda=(m\text{-lifts})\times(H_{PB_3}/L_{PB_3})$、$L_{PB_3}=\bigcap_j(d^j)^{-1}(L)$。

**判定**: 同形。ただし $\beta_g$ は非線形なので、解集合はトーサーでなく、線形代数による枝刈りが効かない。
**軽量版(推奨)**: 先に **SYL3(T33-T2)** を走らせる —
$$v_3\bigl(|\mathrm{ML}(L)|\bigr)-v_3\bigl(|\ker R_{L,H}|\bigr)\ \ge\ v_3\bigl(|\mathrm{ML}(H)|\bigr)\ \Longrightarrow\ I_L=X\ (\text{当該段は閉じる}).$$
これは非線形方程式を解かずに済み、$|\mathrm{ML}(L)|$ の **3-part だけ**を要求する(3 冪位数の shadow のみ列挙すれば足りる)。

### 5.3 有限検査要求(FC)

| 番号 | 検査 | なぜ要るか |
|---|---|---|
| FC-1 | $A$ は $X$ で正規か($X/A\cong C_3$ か、それとも $X\twoheadrightarrow S_3$ か) | 157ae:51 で未決。T33-L4 は不要だが、SEARCH-3 の強形と B-1 型の軌道議論に効く |
| FC-2 | $|\mathrm{ML}(K_*)|$ と $v_3$ の値 | SYL3(T33-T2)の入力 |
| FC-3 | $[PB_4:M]$ と $e_M:=\exp(PB_4/M)$ | T34-J2(ambient がどこまで支配するか)の判定 |
| FC-4 | $M$ の下の最初の非可換 $B_4$-chief factor の同定($PSL(2,8)$ か否か・$\mathrm{Out}$ の型) | OBS★-S の literal 入力。発案札 B-2 の見立ての検証 |
| FC-5 | $\dim_{\mathbf F_3}H_1(K_*;\mathbf F_3)$ の実測(または Nielsen–Schreier 上界 $5[\widehat{PB_4}:K_*]+1$) | T-34 の実行可能性(§6.6) |
| FC-6 | $V=H/\Phi_3(H)\subseteq\Phi_{\rm Frat}(PB_4/\Phi_3(H))$ か(= onto gate が自動で持ち上がるか) | 合成 T-34 × A-4 の (a) 5(§6.8)。in-house SURJ-W6(T-28(4))の前件 |
| FC-7 | $V_r=H_1(H_r;\mathbf F_3)$ の $\varepsilon$-isotypic 部分($\varepsilon:B_4\to S_4\to\{\pm1\}$)は非零か | $\kappa$ の唯一の自然な候補(§4.6 (3))の存在検査。零なら $\kappa$ は braid 側から作れない |

**優先度**: FC-1 と FC-4 を最優先とする。FC-1 は 3-primary sign 路線(T-29 §6・T-31 §3・T-35)の共通前件(T33-L12)、FC-4 は T-35 反模型が実系に転写されるか否かを決める(T35-R1)。

---

## 6. 設問 5 — T-34「Relative-Frattini-3 jump theorem」の評価(+ 発案札との合成の検分)

### 6.1 中核(支配補題)は正しい — 証明

**補題 T34-J1.** $H\trianglelefteq B_4$ 開、$\Phi_3(H):=\overline{H^3[H,H]}$ と置く。
1. $\Phi_3(H)$ は $H$ で characteristic、従って $B_4$-normal。開である。
2. $H/L$ が elementary abelian 3-群であるような閉部分群 $L\le H$ の全体を $\mathcal L$ とすると
$$\Phi_3(H)=\bigcap_{L\in\mathcal L}L .$$
すなわち $\Phi_3(H)$ は**この層の厳密な最小共通下界(= 最適な jump 対象)**である。
*証明.* 1. $H^3[H,H]$ は $H$ の全自己同型で不変、閉包も同様。$H$ は $\widehat{PB_4}$ の開部分群なので位相的有限生成、よって $H/\Phi_3(H)=H_1(H;\mathbf F_3)$ は有限次元 $\mathbf F_3$ 空間、従って $\Phi_3(H)$ は開。$H$ が $B_4$-normal なら $b\in B_4$ による共役は $H$ の自己同型を誘導し $\Phi_3(H)$ を保つ。
2. ($\subseteq$) $L\in\mathcal L$ なら $H/L$ は指数 3・可換なので $H^3[H,H]\le L$、$L$ 閉より $\Phi_3(H)\le L$。($\supseteq$) $\Phi_3(H)\in\mathcal L$ 自身が族の元。∎

> **これは T-34 の主張の核であり、正しい。** 「$\Phi_3(H_4)$ 上の一つの pair が $H_4$ 直下の全 elementary-$\mathbf F_3$ chief へ同時に還元される」は、補題 T34-J1 (2) と単調性(T33-L1)からただちに従う。

**定理 T34-J1'(T-34 の jump、私の再定式化).** $H\in\mathcal I_4(M)$ とし、$z_\Phi\in GT^\heartsuit(\Phi_3(H))$ が存在して $R_{\Phi_3(H),M}(z_\Phi)=x\in X\setminus A$ とする。このとき **$\Phi_3(H)\le L$ を満たす任意の isolated $L\le M$** について $I_L=X$。特に $H/L$ が elementary abelian 3-群であるような全ての isolated $L$ について $I_L=X$。
*証明.* survive 写像は代表対を読むだけなので $R_{\Phi_3(H),M}=R_{L,M}\circ R_{\Phi_3(H),L}$(§6.2)。よって $x\in\mathrm{im}\,R_{L,M}=I_L$。$L$ が isolated なので $I_L$ は部分群で $A\le I_L$(固定入力 1)、$x\notin A$ と $[X:A]=3$ から $I_L=X$。∎

### 6.2 軽量化 (a) の正当性 — 支持する

T-34 の 4 つの軽量化(Φ の isolatedness 不要 / settlement 不要 / full relative Burnside 商不要 / 必要なのは 1 つの literal charming/onto pair)は**すべて正当**である。根拠を明示する。

- $GT(N)$ と $GT^\heartsuit(N)$ は**任意の** $N\in NFI_{PB_4}(B_4)$ に対して定義される(2008 Def 2.9, Def 2.19)。isolated 性(Def 3.2)は $GT^\heartsuit(N)$ が**群**になるための条件であって、元の存在や survive 写像の定義には要らない。
- survive 写像 (3.24)(2008 Def 3.12)は $K\le N$ に対し「同じ代表対 $(m,f)$ を $N$ の shadow として読む」写像。関係式 (2.18)(2.19)(2.20) は $K$ で成立すれば $N$ でも成立(商を粗くするだけ)、全射性・charming も射影の合成で保たれる。**isolated 性はどこにも使われない。**
- 従って合成則 $R_{\Phi,M}=R_{L,M}\circ R_{\Phi,L}$ は代表対のレベルで自明に成り立ち、**source 側($\Phi$)の isolation は不要**。
- one-outside の群論(固定入力 2)は reduction 先の isolated $L$ でのみ使う。ここは T-34 の記述どおり。

**唯一の追加注意**: $GT^\heartsuit$ の元は charming なので $f$ の代表を $[F_2,F_2]$ に取れる(Def 2.19)。従って (3.24) が要求する「$\mathbf Z\times F_2$ の代表対」は charming の枠内では常に存在する。**非 charming shadow(2008 p.23 の未解決点: $\mathbf Z\times F_2$ で代表できない onto 射の存否)には触れない設計になっている点も正しい。**

### 6.3 判定 (b)(Fox/Shapiro sparse boundary certificate)— 正しい。欠けていた証明を補完する

T-34 は $w\in\Phi_3(H_r)\iff\nabla_q(w)\in\mathrm{im}\,D_2$ を「この同値自体が証明対象」として掲げた。**証明する。**

**設定.** $PB_r=\langle S\mid R\rangle$ を有限表示、$F$ を $S$ 上の自由群、$\rho:F\twoheadrightarrow PB_r$($\ker\rho=\langle\langle R\rangle\rangle^F=:\mathcal R$)、$\varepsilon:PB_r\twoheadrightarrow E_r$($\ker\varepsilon=H_r$)、$N:=\rho^{-1}(H_r)=\ker(\varepsilon\rho)$。$G:=F/N\cong E_r$。$\nabla(\tilde w):=(\partial\tilde w/\partial s)_{s\in S}\in\mathbf Z[G]^S$ を Fox 微分ベクトル、$\nabla_3$ をその mod 3 還元、$D_2:\mathbf F_3[G]^R\to\mathbf F_3[G]^S$ を Fox 行列 $(\partial r/\partial s)$、$D_1:\mathbf F_3[G]^S\to\mathbf F_3[G]$, $e_s\mapsto \bar s-1$ とする。

**補題 T34-J4.** $w\in H_r$、$\tilde w\in N$ をその任意の持ち上げとする。このとき
$$w\in\Phi_3(H_r)\ \Longleftrightarrow\ \nabla_3(\tilde w)\in\mathrm{im}\,D_2 .$$
しかも左辺は $\tilde w$ の取り方に依らない。
*証明.*
(i) **Magnus/Crowell 完全列**: 表示 $G=F/N$ から $\mathbf Z$ の $\mathbf Z[G]$-自由分解
$$0\to N^{\rm ab}\xrightarrow{\ \nabla\ }\mathbf Z[G]^S\xrightarrow{\ d_1\ }\mathbf Z[G]\xrightarrow{\rm aug}\mathbf Z\to0$$
が得られ、$\nabla$ は単射(Magnus 埋め込み)でその像は $\ker d_1$。
(ii) **$H_r$ の 1 次ホモロジー**: $H_r=N/\mathcal R$($\mathcal R\le N$ は各 relator が $H_r$ で 1 に落ちるから)。よって
$$H_r^{\rm ab}=N/\mathcal R[N,N]=N^{\rm ab}/\bigl(\mathcal R[N,N]/[N,N]\bigr)=\ker d_1/\mathrm{im}\,D_2^{\mathbf Z},$$
ここで $D_2^{\mathbf Z}:\mathbf Z[G]^R\to\ker d_1$ は $e_r\mapsto\nabla(r)$($\mathcal R[N,N]/[N,N]$ が relator 類の生成する $\mathbf Z[G]$-部分加群であることは、$\nabla$ の $G$-同変性と $\mathcal R=\langle\langle R\rangle\rangle^F$ から)。
(iii) **mod 3 への降下**: $\mathbf Z[G]^S/\ker d_1\cong\mathrm{im}\,d_1=I_G\subseteq\mathbf Z[G]$ は自由 $\mathbf Z$-加群なので $\mathrm{Tor}_1^{\mathbf Z}(\mathbf Z[G]^S/\ker d_1,\mathbf F_3)=0$。従って $\ker d_1\otimes\mathbf F_3\hookrightarrow\mathbf F_3[G]^S$ で像は $\ker D_1$、すなわち $N^{\rm ab}\otimes\mathbf F_3\cong\ker D_1$。
(iv) 右完全性より
$$H_1(H_r;\mathbf F_3)=H_r^{\rm ab}\otimes\mathbf F_3=\ker D_1/\mathrm{im}\,D_2 .$$
$w\in\Phi_3(H_r)$ は $w$ の $H_1(H_r;\mathbf F_3)$ での像が 0 と同値で、その像は $\nabla_3(\tilde w)\bmod\mathrm{im}\,D_2$。
(v) **持ち上げ非依存**: 二つの持ち上げは $\mathcal R$ の元だけ違い、$\nabla_3(\mathcal R)\subseteq\mathrm{im}\,D_2$。∎

**前件(明示)**
- **(P-FOX-1)** $PB_r$ は有限表示(2008 (A.3) が $PB_4$ の表示)。
- **(P-FOX-2)** 離散/副有限の突合: $\Phi_3(H_r)$ は副有限完備化内の閉包として定義されるが、$H_r^3[H_r,H_r]$ は $H_r$ の有限指数部分群なので副有限位相で閉じており、$\overline{H_r^3[H_r,H_r]}\cap PB_r=H_r^3[H_r,H_r]$(離散側)。$H_r$ が有限群への全射の核として与えられているとき、離散 $H_r$ は副有限 $H_r$ で稠密。**この突合は書けば済むが、書かずに済ませてはならない。**
- **(P-FOX-3)** $E_r=PB_r/H_r$ が有限で、$\mathbf F_3[E_r]$ 上の計算が意味を持つこと。

> **裁定: T-34 の (b) は正しい。** ただし上記 (i)–(v) と (P-FOX-1..3) を明記しない限り「証明対象」のまま残る。本補題をもって埋める。

### 6.4 追加提案 — 群環を一切使わない等価証明書 CERT-Φ-WORD

**補題 T34-J5.** $w\in H_r$ について、次は同値:
1. $w\in\Phi_3(H_r)$;
2. **$PB_r$ の中での等式** $\ w=\prod_{i=1}^{a}h_i^{\,3}\cdot\prod_{j=1}^{b}[u_j,v_j]$ が成立するような $h_i,u_j,v_j\in H_r$(語として与える)が存在する;
3. $\nabla_3(\tilde w)\in\mathrm{im}\,D_2$。
*証明.* (1)⟺(2) は $\Phi_3(H_r)\cap PB_r=H_r^3[H_r,H_r]$(P-FOX-2)の定義そのもの。(1)⟺(3) は T34-J4。∎

**実装上の含意(producer/checker 分離に直結)**
- **producer** は $(h_i,u_j,v_j)$ の語列を出す。
- **checker** は (α) 各語が $H_r$ に属する($E_r$ で評価して 1 になる — 有限群の 1 回の評価)、(β) $PB_r$ での語等式 $w=\prod h_i^3\prod[u_j,v_j]$ を検査する、の 2 つだけを行う。$PB_r$ は反復半直積 $PB_n\cong F_{n-1}\rtimes PB_{n-1}$ による明示正規形(Artin combing)を持ち語問題は可解、既在の KBMAG consumer(`search/d972_b4_norm_tietze_kbmag_consumer_v4.g`)も使える。
- ⟹ **checker のコストが $\mathbf F_3[E_r]$(次元 $\sim10^6$–$10^7$)の線形代数から語等式検査へ落ちる。** $V_r$ の基底も群環も一切構成しない。
- Fox 版(T-34 の (b))は **探索の指針**(線形代数として枝刈りできる)として残し、**受領票は語証明書で取る**、という役割分担を提案する。

### 6.5 注意 (c)(d) の確認と 2 件の訂正

**(c1) $J_3=\bigcap_j(d^j)^{-1}\Phi_3(H_4)$ を $\Phi_3(H_3)$ で代用しない — 正しい。誤差の向きも確定する。**
**補題 T34-J7.** $d^j(H_3)\subseteq H_4$(matched)なら $\Phi_3(H_3)\subseteq J_3$。従って $\Phi_3(H_3)$ で代用した判定は**過度に厳しい**(false negative は起こるが false positive は起こらない)。
*証明.* $u\in H_3^3[H_3,H_3]$ に対し $d^j(u)\in H_4^3[H_4,H_4]$。閉包を取って $d^j(\Phi_3(H_3))\subseteq\Phi_3(H_4)$。∎
> 実務上: もし過去の実装が $\Phi_3(H_3)$ を使っていたなら、**得られた positive は依然として有効**(保守側の誤差)。ただし探索空間が不当に狭まっているので、positive が出ていない段では $J_3$ に直して再走する価値がある。

**(c2) $PB_r/\Phi_3(H_r)$ が一般に nonsplit — 正しい。かつ (b) がこれを自動処理する。**
Fox/Magnus 判定(T34-J4)も語証明書(T34-J5)も $PB_r$ の語で完結しており、$V_r$ を加群の直和因子として扱わない。extension cocycle は relator の Fox 像($\mathrm{im}\,D_2$)として最初から入っている。**⟹ (c2) の危険は (b) を採用する限り自動的に回避される。**(逆に、$V_r$ を加群として単独に扱う実装 — 例えば「$E_r$ 上の加群 $V_r$ の中で線形方程式を解く」— は (c2) に直撃する。)

**(d) 「ambient q3 positive → relative pair は自動では出ない」— 正しい。**
ambient positive は $K_*=M\cap N_4(3)$ 上の対である。$\Phi_3(K_*)\lneq K_*$ なので、関係式 (2.18)(2.19)(2.20) を $\Phi_3(K_*)$ の法で成立させることは新たな要求であり、$\Lambda(\Phi_3(K_*))$ の中で残差を消す surgery を解かねばならない。**自動では出ない。** Sol の自己限定を支持する。

**訂正 1 — ambient は「誤り」ではなく「健全だが劣化」。**
**補題 T34-J2.** $e_M:=\exp(PB_4/M)$ とし、$H\le M$、$H/L$ が exponent 3 とする。
1. $N_{PB_4}(3)\le L\iff\exp(PB_4/L)\mid3$。よって $e_M\nmid3$ なら **ambient $N_{PB_4}(3)$ は支配しない**(T-34/速達の主張は正しい)。
2. 一方 $\exp(PB_4/L)\mid 3\,e_H$($e_H:=\exp(PB_4/H)$)なので **$N_{PB_4}(3e_H)$ は支配する**。
3. さらに $N_{PB_4}(3e_H)\subseteq\Phi_3(H)$。すなわち relative 対象は ambient 対象より**粗い(= 商が小さい・計算が軽い)**。
*証明.* 1. 定義。2. 群 $G$ が exponent $a$ の正規部分群による exponent $b$ の拡大なら $\exp G\mid ab$。3. $g\in PB_4$ に対し $g^{e_H}\in H$ なので $g^{3e_H}=(g^{e_H})^3\in H^3\subseteq\Phi_3(H)$。∎
> ⟹ 正しい言い方は「**ambient は間違いではないが、relative $\Phi_3(H)$ が層の最適(最大)対象**」である(T34-J1 (2))。これは Sol の結論を弱めない — むしろ $\Phi_3$ の最適性という強い形で支える。

**訂正 2 — specialization は pruning 専用ではなく、厳密な非所属証明書になる。**
**補題 T34-J6.** $\psi:\mathbf F_3[E_r]\to\mathrm{End}_{\mathbf F_3}(W)$ を任意の有限次元 $\mathbf F_3[E_r]$-加群 $W$ が定める表現とし、$D_2^\psi:W^R\to W^S$ を $D_2$ の $\psi$-像とする。$\nabla_3(\tilde w)\in\mathrm{im}\,D_2$ ならば、右完全性(関手 $-\otimes_{\mathbf F_3[E_r]}W$ の適用)により $\nabla_3(\tilde w)^\psi\in\mathrm{im}\,D_2^\psi$。**対偶により、ある $W$ で $\nabla_3(\tilde w)^\psi\notin\mathrm{im}\,D_2^\psi$ が示せれば $w\notin\Phi_3(H_r)$ が厳密に証明される。**
> T-34 は「specialization は pruning／障害検出専用とし、positive の根拠には使わない」と書いた。前半は**控えめすぎる**: specialization の失敗は pruning ではなく**厳密な負の証明書**である。後半(positive の根拠にしない)は正しい。char 3 で非半単純であることは「positive を出せない」理由であって「negative が緩む」理由ではない。
> ⟹ **negative 側の受領票設計に使える。** これは OBS★-3(§5.1)の A 側決着に直結する。

### 6.6 最大の留保 — T-34 は吸収定理ではなく再指標化である

**T34-J10.** T-34 の内容は本質的に補題 T34-J1 (2)、すなわち
$$\forall L\in\mathcal L:\ (\text{$L$ で解ける})\quad\Longleftarrow\quad \exists\ \text{解 at}\ \inf\mathcal L=\Phi_3(H)$$
という **$\forall$ を族の下限での $\exists$ に付け替える**操作である。難度は減らない。むしろ:
- $\Phi_3(H)\le L$ なので、**$\Phi_3(H)$ での問題は層の中で最も難しい単一問題**である。
- $|V_r|=3^{d}$、$d=\dim H_1(H_r;\mathbf F_3)$、Nielsen–Schreier より $d\le 5\,[\widehat{PB_4}:H_r]+1$。T-34 自身が「数千万次元」と見積もっており、これは $[\widehat{PB_4}:H_r]\sim10^6$ 程度に対応する。**$\Lambda(\Phi_3(H))$ の全走査は不可能**であり、positive は「たまたま短い証明書が見つかる」ことに依存する(完全性保証はない)。
- 一層分しか進まない。次の層(別の素数・非可換 $S^t$)は新しい pair を要求する。T-34 の裁定行 `nonabelian S^t and global iteration: STILL OPEN` はこの点で正確。

> **それでも T-34 には実質的価値がある。** 「不定個・未知の $L$ に対する $\forall$」を「canonical で計算可能な単一対象 $\Phi_3(H)$ に対する $\exists$」に変えたことで、**問題が初めて well-posed な有限標的になった**。加えて (b)(語証明書に置き換えれば J5)により checker が現実的コストに落ちる。裁定行 `PROVED CONDITIONALLY ON ONE LITERAL PAIR AT Phi` は**正確**であり、私はこれを支持する。

### 6.8 合成 T-34 × A-4(UNIFORM-WITNESS)の検分 — 半分成立・半分不成立

司令塔の読み: 「T-34 の唯一の条件は $\Phi_3(H_4)$ 上の pair 一個。A-4 は導出でなく**直接 replay の測定**を提案。合成が正当なら T-34 の条件は一回の有限 run に変わる」。検分結果を (a)(b)(c)(d) に分ける。

**(a) 型としての well-definedness — 成立。**
**補題 T34-J11.** run 32135808950 の witness を与える literal pair $(m,f)\in\mathbf Z\times F_2$ を $\Phi:=\Phi_3(H_4)$ 段で読むことは型として well-defined であり、各 gate は $\Phi$ 上で literal な意味を持つ。
1. 関係式: (2.18)(2.19) を $B_3/\Phi_{PB_3}$、(2.20) を $PB_4/\Phi$ で評価。ここで $\Phi_{PB_3}=J_3=\bigcap_j(d^j)^{-1}\Phi$ — **T-34 の注意 (c1) はここに正しく効いており、衝突ではなく指定である**。
2. nonsplit(注意 (c2))とも衝突しない: 評価は $PB_4/\Phi$ の**語**で行い、$V_r$ を加群として単独に扱わない(T34-J5/§6.5)。
3. **friendly gate はほぼ無料**: 補題 T33-L9($p=3$)より $\Phi_{\rm ord}/H_{\rm ord}=[H_{PB_2}:\Phi_{PB_2}]$ は 3 冪。よって $3\mid H_{\rm ord}$ なら $\gcd(2m+1,\Phi_{\rm ord})=1$ は自動。$3\nmid H_{\rm ord}$ でも $m\mapsto m+H_{\rm ord}t$ の mod 3 調整で足りる。
4. charming 前半($f'\in[F_2,F_2]$ 代表): 補正 $c$ を $[F_2,F_2]\cap H_{PB_3}$ に取れば保存 — これは補正空間の**線形部分空間条件**。
5. **onto gate($T^{F_2},T^{PB_3}$ 全射)は自動でない**。$V=H/\Phi_3(H)\subseteq\Phi_{\rm Frat}(PB_4/\Phi_3(H))$ なら自動(in-house SURJ-W6・T-28(4))。この包含は要検査 ⟹ **FC-6**。∎

**(b) 「同一 schema がそのまま通る」という予想 — 構造的支持なし。**
pentagon 残差 $w_{\rm pent}$ は $H$ の元で、要求は $w_{\rm pent}\in\Phi_3(H)$。$[H:\Phi_3(H)]=3^{d}$、$d=\dim_{\mathbf F_3}H_1(H;\mathbf F_3)$(T-34 自身の見積で $\sim10^7$)。**ambient positive は $w_{\rm pent}$ を「$H$ の元である」以上には拘束しない**(それが shadow at $H$ の定義)。従って「そのまま通る」は余次元 $d$ の一致であり、それを支える機構が必要である。
A-4 が挙げる根拠(T-30 §2 の split correction が任意係数で有効)は **untwisted linking-number complex** についての言明で、actual 残差が $H_1(H;\mathbf F_3)$ のどこに座るかを拘束しない — T-30 §4 自身が「この同定は未証明」と 5 点の理由つきで明記している。
実データ側の傍証も逆向き: 当該 run の terminal は `B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION`(`correction_index=1`)であり、**無補正の対は既に通っていない**。schema が段をまたいで不変であるという経験的支持はない。
⟹ **「1 run で T-34 の条件が満たされる」という読みは成立しない。1 run は安価な宝くじであって計画ではない。**(なお安価なので**引くこと自体は推奨**する: コストは §6.4 の語証明書 3 本ぶん。)

**(c) 正しい合成 — replay ではなく「$\Phi$ 層の疎 $\mathbf F_3$ 線形系を解く」。**
**補題 T34-J12.** $V=H/\Phi_3(H)$ は elementary abelian、correction domain の $f$-成分 $H_{PB_3}/J_3$ も elementary abelian(T33-L9, $p=3$)。従って基点 $\lambda_0$ を固定すると残差写像 $\beta_g$ は $\mathbf F_3$ 上の**アフィン写像**であり、可解性は $\mathbf F_3$ 線形系
$$\beta_g(\lambda_0)+D\cdot\gamma=0,\qquad \gamma\in H_{PB_3}/J_3\ (\oplus\ m\text{-成分})$$
の可解性である。∎
帰結:
- **探索ではなく決定**になる。T-34 の裁定行 `sparse Fox positive certificate: IMPLEMENTABLE`(= positive-semidecision)が **decision** に上がる。
- Fox 行列 $D_2$ は群環係数で疎(各成分が短い語)なので $\mathbf F_3$ 行列としても疎(非零 $\sim|R|\cdot|E_r|\cdot$語長)。次元 $\sim10^7$・非零 $\sim10^8$ の疎 $\mathbf F_3$ 線形系は block-Wiedemann 級の道具の射程内。
- **留保**: side gate のうち friendly と charming 前半は線形/自動((a) 3,4)だが、**onto と settlement は非線形**。従って「線形解空間を求める → 非線形 gate で filter」の二段構成になる。線形系が非可解なら filter 前に決着する(A 側)。
⟹ **A-4 の正しい実装は「同一 schema の replay」ではなく「$\Phi$ 層の線形系の求解」であり、T-34 の Fox complex はそのための正しい枠組みである。** 合成は**この形でなら成立する**。

**(d) A-7(同一 run の双対読み)は自動では設問 4 の形式を満たさない。**
- 単一 pair の replay 失敗は**何も証明しない**(T-29 手戻り防止ルール 5 そのもの)。
- **線形系の非可解性**なら証明する。ただし設問 4 の形式(OBS★-3・§5.1)を満たすには **outside roof を持つ全ての $g\in\mathrm{ML}(H)$ について**非可解を示す宇宙完全性が要る。T33-L4 により標的 roof は 162 個に落ちるが、各 roof の上の $g$ は $|\mathrm{ML}(H)|/972$ 個ある。
- 非可解性の証明は **T34-J6(specialization による厳密な非所属/非可解証明書)**で安価に取れる場合がある。
⟹ **A-7 は「線形非可解 + 宇宙完全性」の 2 条件つきで設問 4 の形式を満たす。単独では満たさない。**

### 6.9 A-5(BOUNDED-COMPLEXITY-KÖNIG)および A-4 強形の検分 — 機構は妥当、仮説は目標より真に強い

**(i) 機構の修理.** 「有限集合 $S$ の非空部分集合の族 $\{W_j\}$ に共通元がある」は**偽**(鳩の巣からは「ある schema が無限個の $j$ に現れる」しか出ない)。正しくは $W_j$ が**減少列**であることが要る。そしてそれは成り立つ: 細かい段の shadow は同じ literal pair のまま粗い段の shadow なので(survive 写像 (3.24))$W_{j+1}\subseteq W_j$。減少する非空有限集合列の交わりは非空。⟹ **この修理の下で A-5 の機構は妥当。**

**(ii) しかし結論が強すぎる.**
**定理 T33-L10.** 単一の literal pair $(m,f)\in\mathbf Z\times F_2$ が cofinal な族の全段で GT-shadow なら、それは**全ての**窓 $N\in NFI_{PB_4}(B_4)$ で GT-shadow であり、従って $2m+1=\pm1$、すなわち $m\in\{0,-1\}$。
*証明.* まず任意の窓 $N\in NFI_{PB_4}(B_4)$ について $M\cap N$ も窓で $\le M$ なので、$M$ 以下での cofinality から $K_j\le M\cap N\le N$ なる $j$ がある。$s$ が $K_j$ の shadow なら survive 写像 (3.24) により $N$ の shadow でもある。従って $s$ は**全ての**窓の shadow。
次に friendly gate (2.36) は $\gcd(2m+1,N_{\rm ord})=1$ を要求する。任意の素数 $p$ について、全リンク数 $\lambda:PB_4\to\mathbf Z$($PB_4^{ab}=\mathbf Z^6$ の基底 $x_{ij}$ を $B_4$ が置換するので $\lambda$ は $B_4$-不変)の mod $p$ 還元の核 $N_p$ は $NFI_{PB_4}(B_4)$ の元。$x_{12}^k\in(N_p)_{PB_2}$ なら特に $\varphi_{123}(\phi_{12}(x_{12}^k))=x_{12}^k\in N_p$、すなわち $k\equiv0\ (p)$。よって $p\mid(N_p)_{\rm ord}$。従って $2m+1$ は全ての素数と互いに素、すなわち $\widehat{\mathbf Z}^\times\cap\mathbf Z=\{\pm1\}$ の元。∎
⟹ 定数 schema 仮説は「**pentagon と両 hexagon を $B_3$/$PB_4$ の中で厳密に満たす離散対 $(m,f)\in\{0,-1\}\times F_2$ が存在し、しかもその屋根像が $A$ の外**」という主張と同値である。これは B4-B より真に強い独立の重大主張であり、「複雑性上界という**測れる量**に交換した」つもりが実は目標を強めている。
⟹ **A-5 は経路として却下。同じ論法で A-4 の強形(全段で同一 schema)も却下。** A-4 の弱形(次の一段だけ replay)は §6.8 のとおり安価な宝くじとして残る。

**(iii) 副産物.** T33-L10 は「$f$ の代表語は段が深くなるにつれて伸びざるを得ない」ことの理由でもある(段ごとに $f$ は $K_{PB_3}$ を法としてしか定まらず、定数語で全段を通せば上の剛性に抵触する)。従って A-5 が要求する「段独立な正規形をもつ固定有限 schema 集合」は存在しない。

### 6.10 A-2(UP-SET/DEEP)× T-34 — 部分的に有効だが cofinal にならない

- T33-T1 (5) より DEEP(x) $\iff$ B4-B なので、A-2 の枠に載せても証明義務は減らない(§3.1)。**設計上の利点はある**: 「与えられた窓を攻める」から「攻めやすい深い窓を自分で作る」への転換。
- T-34 を「一段を丸ごと良くする道具」として反復すると $H\mapsto\Phi_3(H)\mapsto\Phi_3(\Phi_3(H))\mapsto\cdots$ の塔になるが、その交わりは $H$ の**最大 pro-3 商の核**であり cofinal でない($H$ は pro-3 でない)。全素数で交互に刻んでも各段が elementary abelian ⟹ 商は可解 ⟹ **pro-solvable 方向にしか降りられない**。
- これは発案札 A-3 の two-tower gap の観察と一致し、**T33-L7(非可換 chief 不可避性)の別証明**にもなっている。
- ⟹ **T-34 は SINGLE(x) への最短路の一部を構成するが、それだけでは cofinal にならない。** cofinal に降りるには T33-L6(指数で刻む相対 core tower)のような非可解段を含む刻みが必要で、そこで必ず $S^t$ に出会う。

### 6.11 設問 5 の裁定(まとめ)

| T-34 の項目 | 私の裁定 |
|---|---|
| 支配補題($\Phi_3(H_4)\le L_4$)と jump | **証明(支持)**。しかも $\Phi_3(H)$ は層の**最小共通下界 = 最適対象**(T34-J1 (2)) |
| 軽量化 (a)(isolation/settlement 不要) | **正当**(T34-J3)。根拠は Def 2.9/2.19 が任意の $N$ で定義されること + (3.24) が代表対を読むだけであること |
| 判定 (b)(Fox sparse certificate) | **正しい。証明を補完した(T34-J4)**。前件 P-FOX-1..3 を明記。**より軽い等価証明書 CERT-Φ-WORD を提案(T34-J5)** |
| 注意 (c1)($J_3$ vs $\Phi_3(H_3)$) | **正しい**。誤差の向きは保守側(T34-J7)— 既存 positive は無効化されない |
| 注意 (c2)(nonsplit) | **正しい**。かつ (b) を採る限り自動回避(T34-J8 = §6.5) |
| (d)(ambient → relative 自動は NO) | **正しい**(支持) |
| ambient が「誤り」 | **訂正**: 健全だが劣化。$N_{PB_4}(3)$ は支配しないが $N_{PB_4}(3e_H)$ は支配し、$\subseteq\Phi_3(H)$(T34-J2) |
| specialization は pruning 専用 | **訂正**: 厳密な非所属証明書になる(T34-J6)。negative 受領票に使える |
| `full H1 enumeration: FORBIDDEN / INFEASIBLE` | **支持**。Nielsen–Schreier で $d\le5[\widehat{PB_4}:H]+1$(FC-5) |
| 全体の位置づけ | **留保**: 吸収定理ではなく $\forall\to\exists$ の再指標化。難度不変・一層分のみ(T34-J10) |
| 合成 T-34 × A-4 | **型は well-defined(成立・T34-J11)/「同一 schema がそのまま通る」は不成立(§6.8 (b))/ 正しい合成は「疎 $\mathbf F_3$ 線形系の求解」で、これなら成立し semidecision が decision に上がる(T34-J12)/ A-7 の双対は「線形非可解 + 宇宙完全性」つきでのみ設問 4 の形式を満たす** |
| 合成 A-5 / A-4 強形 | **却下**(T33-L10 による反証・§6.9) |
| 合成 A-2 × T-34 | **部分的に有効だが cofinal にならない**(pro-solvable の壁・§6.10) |

---

## 7. 使用した既在定理の一覧(引用)

**正典(2008.00066 / 2401.06870)**
- 2008 **Theorem A.1**(= Fresse Thm 6.2.4): $\mathrm{PaB}$ は $\alpha,\beta$ で生成され、全関係式は pentagon (A.13) + 二 hexagon (A.14)(A.15) の帰結 — 補題 T33-L8 の要。
- 2008 **Def 2.6**(GT-pair: (2.18)(2.19)(2.20))・**Def 2.9**(全射性)・**Prop 2.10**(PB3+PB2 全射 ⟹ PB4 全射)・**Def 2.19**(charming)。
- 2008 **(2.4)(2.5)**(誘導部分群 $N_{PB_3},N_{PB_2}$)・**Prop 2.2**・**Prop 2.3**($N_{\rm ord}$)。
- 2008 **Def 3.2**(settled/isolated)・**Prop 3.3**($N^\sharp$)・**Cor 3.5**(isolated は cofinal)・**Prop 3.6**(交叉)。
- 2008 **Prop 3.7**($\mathrm{ML}_{K,N}$ は群準同型・合成 (3.7))・**Prop 3.11**((3.18) 算術自然性)・**Def 3.12/(3.24)**(survive)・**Thm 3.8**($\widehat{GT}\cong\lim\mathrm{ML}$)・**Cor 3.13**(genuine ⟺ 全 $K$ へ survive)。
- 2008 **Prop 3.9(A)**($PB_3$ 窓の上への $PB_4$ 窓の明示構成)・**(A.3)**($PB_4$ 表示)・**(A.18)**(coface 生成元値)。
- 2008 **Table 1 / §4.1**(Mighty Dandy $N^{(34)}$: $|GT^\heartsuit|=486$, Sylow-3 = $\mathbf Z_3\ltimes(\mathbf Z_9\times\mathbf Z_9)$ 正規)。

**in-house(引用して使用)**
- `sol/luna_reply_157bu_utl_group_theory.md` §2: 凍結 $X\cong((C_9^2)\rtimes C_6)\times C_2$, $|X^2|=243$, $[X,X]=V$, $\Phi(X)=3V$ — T33-L4/L5 の入力。同 §3: 抽象反模型($I_K=A_0$)— T33-T1 が「抽象公理からは決まらない」ことの独立確認。
- `sol/luna_reply_157br_b4b_power_cofinal_theorem.md` §2: $243\nmid324$ の Lagrange 論法(**T33-T2 はこれの精密化**)。同 §3: UTL の定式化。同 §4: deletion-core 警告 $M^{[4]}<M$。
- `sol/luna_reply_157cq_b4_cofinal_compactness.md` §§1–6: 窓 poset・$\mathrm{SINGLE}(x)$/$\mathrm{STEP}$ の定式化・有限 fibre と compactness(固定入力 4 の典拠)。§4 条件 1–4(chief 還元の必要条件)。
- `sol/luna_reply_157cc_b4b_compatibility_theorem.md`: 325 補題、c² 非 cofinality 反例($L=M\cap N_5^{\rm cyc}$)。
- `sol/luna_reply_157bz_b4b_compactness_bridge.md`: UNIFORM_325(有限受領票の限界)、「一段の outside lift は profinite lift ではない」。
- `sol/luna_reply_152_b4_chief_obstruction_v2.md` §3–§4: 全素数の elementary abelian chief 段の構成、**非可解下位 section と $S^t$ の存在**(T33-L7 の土台)。§2: joint correction の反模型($\Psi_V(v)=(2v,3v,5v)$)。
- `sol/luna_reply_152_relative_cofinal_v1.md`: `RELATIVE_COFINALITY_FALSE_IN_GENERAL`(T33-L6 との非衝突を §3.3 で明示)。
- `sol/luna_reply_152_b4_7adic_verbal.md`: 「単一素数 verbal 族の cofinality を自動と見なすな」(T33-L6 が守る)。
- `sol/luna_reply_157ay_isolated_nested_pair.md`: $N\mapsto N^\sharp$ は単調でない(T33-L6 が isolated 化を塔の定義に組み込まない理由)。
- `sol/sol_reply_150_bside.md` (MODULE-SEPARATED-GLUE-150)・`sol/sol_reply_148_dovetail.md` (COPRIME-GLUE-148)・`sol/sol_reply_151_finish.md` §4.3(c² 反例・A 半決定性): gentle 側先行。**本書では直接は使わなかった**(理由は §8)。
- `docs/notes/t33_ideas_v1.md` 札 A-1〜A-7・B-1・B-2・B-5: §3.1・§4.7・§6.8–6.10 で採否を記載。

**古典(標準)**
- Fox 微分と Magnus/Crowell 完全列 $0\to N^{\rm ab}\to\mathbf Z[G]^S\to\mathbf Z[G]\to\mathbf Z\to0$(T34-J4)。
- Nielsen–Schreier(副有限版)$d(H)\le[\Pi:H](d(\Pi)-1)+1$(§6.6)。
- Sylow の定理・Lagrange(T33-T2)。
- (**使わなかった**) Zelmanov の制限 Burnside — T33-L6 が回避。

---

## 8. 司令塔の着眼への回答

**(1) MODULE-SEPARATED-GLUE-150 の移植について.**
着眼は「位数が互いに素でなくても $Q_0$-加群 support の分離で fiber product が閉じる」構造が、設問 1 の elementary abelian chief 吸収と同型に見える、というものだった。**私の判定: 現時点では移植しない。** 理由:
- 150 の補題は**二つの非比較な窓を貼る**装置である(fiber product $GT(J)\cong GT(K_2)\times_{GT(M)}GT(W)$)。T-33 の STEP/SINGLE は**鎖に沿って降りる**問題で、非比較な窓を貼る場面がそもそも出ない(発案札 A-1 と同じ観察)。
- 仮に $B_4$ 版 $\mathrm{ML}(L_1\cap L_2)\cong\mathrm{ML}(L_1)\times_{\mathrm{ML}(K)}\mathrm{ML}(L_2)$ が立っても、$I_{L_1\cap L_2}=\rho(J_1\cap J_2)$ であり、$3\nmid[\mathrm{ML}(K):J_i]$ ($i=1,2$) からは $3\nmid[\mathrm{ML}(K):J_1\cap J_2]$ が**従わない**(反例: $G=A_4$, $J_1=\langle(123)\rangle$, $J_2=\langle(124)\rangle$、両指数 4 だが交叉は自明で指数 12)。従って SYL3 と組み合わせるには「$\mathrm{ML}(K)$ の Sylow 3-部分群が正規」という追加前件が要る(Mighty Dandy では実際に正規 — 2008 §4.1)。**この前件つきなら移植は有効**であり、FC として登録する価値がある。
- 「relative 化が support を分離する動き」という見立て自体は正しい方向だと考えるが、$\Phi_3(H)$ への移行は support の分離ではなく**層の下限を取る操作**(T34-J1 (2))であり、機構が違う。

**(2) c² 反例を $x$ を固定したまま回避する設計.** §3.3(相対 core tower T33-L6)で回答した。族の側に自由度を移す、という着眼はそのとおりで、**「固定窓との交叉」ではなく「前段の characteristic 部分群」で族を定義する**のが正しい移し方である。

**(3) $S^t$ を無理に閉じず設問 4 形式で返す.** 概ねそのとおりにした(§4.8, §5.2)。ただし二点、**閉じないまま放置してはいけない構造的事実**を見つけたので提出した:
- 補題 T33-L8(A5/V4 反模型は圏違い)— 「$S^t$ が難しい理由」を Wells から非線形残差方程式へ移す訂正。Sol の `generic nonabelian absorption: STOP` の**根拠**を差し替える(STOP という結論自体は維持)。
- 補題 T33-L11($X$ の $V_r$ への作用が未着工)— T-35 の `PB4-specific kappa + Theta comparison: OPEN / exact next target` の **next target の中身**を差し替える対案。

**(4) 発案札との合成(司令塔の読み)への回答.** §6.8(T-34 × A-4)・§6.9(A-5 / A-4 強形)・§6.10(A-2 × T-34)・§4.7(B-1 / B-5)に個別に書いた。要点だけ再掲すると:
- **T-34 × A-4**: 型は通る。「同一 schema 一発」は通らない。**正しい形(疎 $\mathbf F_3$ 線形系の求解)なら通り、しかも semidecision が decision に上がる**。
- **A-5 / A-4 強形**: T33-L10 で却下。
- **A-2 × T-34**: 有効だが pro-solvable の壁で cofinal にならない。
- **B-1**: 骨格(中間なし)は無条件で正しいが Wells 由来ではない。検出の枝は T-35 により一般形で STOP、$\mathrm{Out}\supseteq C_3$ かつ作用構成の 2 条件つきでのみ復活。
- **B-5**: $\Theta$ の候補ではなく $\kappa$ の候補として読むべき(FC-7 と接続)。

---

## 9. novelty grep 領収書

概念語彙で repo 全体を grep した結果(実施日 2026-08-18)。

| 概念 | grep 結果 | 本書での扱い |
|---|---|---|
| `absorption` | `152_b4_absorption_literature_v1`, `157ao`, T-31 §3(`generic nonabelian absorption: STOP`)ほか多数 | 既在。T33-L8 で**根拠の差し替え**を提案(結論は維持) |
| `jump` | T-34 / 速達のみ(2026-08-18 新規) | 既在。§6 で評価 |
| `selection` | 該当なし(`SINGLE`/`STEP` の命名も 8 主要ファイルに不在 — 部隊調査で確認) | T-33 が新規命名。本書は T33-T1 で同値性を証明 |
| `Wells` | `157w_fixed_obstruction_class`, `152_typed_lifting_literature_v1`, `152_b4_absorption_literature_v1`, T-31/T-33, `t33_ideas_v1` 札 B-1/B-4 | 既在。T33-L8 で**適用範囲の訂正** |
| `Sylow` / `3-part` / 素冪位数元への探索限定 | **repo 全体で該当なし**(部隊調査 (e) で確認) | **T33-L4 / T33-T2 は in-house 新規**(ただし $243\nmid324$ の Lagrange 論法は 157br §2 / 157bu / 157bf / 157bh が既在 — その精密化として提出) |
| $I_K$ の単調減少・最小値の単一 $K_0$ 達成 | 8 主要ファイルに**該当なし**(合成則 $\mathrm{ML}_{K,M}\circ\mathrm{ML}_{K',K}=\mathrm{ML}_{K',M}$ は既在)。同日の発案札 A-2(UP-SET)が上閉性を candidate で提出 | T33-L1/L3 は**発案札 A-2 と重複**(A-2 を出典として明記)。安定化(単一 $K_0$)は grep 範囲で新規 |
| SINGLE ⟺ STEP ⟺ B4-B の同値 | **該当なし**(片方向 SINGLE ⟹ B4-B のみ既在: `157bz:179-186`, `152_7adic:118-147`, `157cc:73-83`) | **T33-T1 は in-house 新規**(三者同値) |
| 相対 Frattini $\Phi_p(K)=K^p[K,K]` | 対象は既在(`152_relative:126-142` の $N_p=[C_M,C_M]C_M^p$、用途は fail-fast 作用検査)。「層の普遍対象」としての使用は**該当なし** | T-34(同日)が普遍対象として提出。T34-J1 で**最小共通下界であること**を証明 |
| verbal/冪部分群の characteristic 性と cofinality | 既在(`152_7adic:40-48`, `152_relative:31-51`, `157ao:117-119`, `157bz:36-40`) | T33-L6(指数で刻む相対 core tower)は**新しい配置**。単一素数族の非 cofinality は既在警告と整合 |
| isolatedization が witness を壊す | 既在・多数(`157ay:56,58-77,88-91`, `157az:154,165-167`) | T33-L6 は塔に isolated 化を組み込まない設計で回避。T34-J3 は isolated 性自体を要求から外す |
| 非可換 chief の不可避性 | **既在**(`152_b4_chief_obstruction_v2` §4) | T33-L7 は**強化**(cofinality により isolatedization 回避も不可能)。初出主張はしない |
| Fox/Magnus による $\Phi_3$ 判定 | T-34(同日)が提出、証明は「証明対象」と明記 | T34-J4 で**証明を補完**。CERT-Φ-WORD(T34-J5)は grep 範囲で新規 |
| `sign` / sign-window / permutation module の linearization | 既在(T-29 §6, T-31 §3, T-35, `157z_index3_transfer`)。**「sign-window の存在自体が $A$ 非正規を前提とする」という指摘は grep 範囲で該当なし** | T33-L12 は新規。既在の $A$ 正規/非正規の二分は `157ad:104`, `157ae:51` にあり、それが sign 路線の前件だという接続が新規 |
| `Out(S)` に 3 が入るかで反模型が転写されるかが変わる | 該当なし(T-35 は反模型の射程を限定していない) | T35-R1 は新規 |
| $X$ の $H_1(H_r;\mathbf F_3)$ への作用の存在問題 | 該当なし | **T33-L11 は新規**。既在の近接物は T-30 §4 (4)(二つの sign を同一視するな)と `157ay` の $N\mapsto N^\sharp$ 非単調性 |
| 定数 witness schema / 複雑性上界 | 発案札 A-4/A-5(同日・candidate)。`152_cocycle_absorb_universal_v1` が「全 layer への普遍化は前件から出ない」と裁定済 | **T33-L10(定数 schema なら $2m+1=\pm1$)は新規の反証**。152 の裁定と同方向だが機構が違う(cohomology 前件ではなく friendly gate の剛性) |
| $\Phi$ 層が $\mathbf F_3$-アフィンであること / 疎線形系としての求解 | 該当なし(T-34 は「sparse boundary certificate の探索」として提示) | T34-J12 は新規。T-34 の semidecision を decision に上げる |

---

## 10. 申告

- 本書の全結果は **paper candidate**。機械計算・GAP・GHA・commit・push は一切行っていない。**cross-checked ではなく、verified でもない。**
- 固定入力 1–6(T-33 §2)は再監査していない。
- 封印 3 量・$u$ の値と平方類・$c$ の値・sealed $K^{(5)}$ には非接触。$u=2m+1$ は形式変数としてのみ使用。
- 未閉の穴を明示する:
  - **【GAP: CH-p】** 障害写像 $\mathrm{ob}$ の crossed-homomorphism 性(§2.5)。これが閉じれば設問 1 は characteristic 3 のみに縮約。**【文献要請】**を §2.5 に添付。
  - **【GAP: P-FOX-2】** T34-J4 の離散/副有限突合(§6.3)。書けば済むが未記述。
  - **【GAP: ISO-Λ】** T33-L6 の塔の各段は isolated とは限らない。T-34 の軽量化(§6.2)により reduction 先だけ isolated であればよいので致命的ではないが、$I_{K_j}$ を部分群として使う場面では isolated 核を挟む必要がある。
  - **【GAP: X-ACT】** $X$ の $V_r=H_1(H_r;\mathbf F_3)$ への作用(T33-L11 の循環)。κ/Θ 路線の一階部分。設計上の出口候補(塔を $\widehat{PB_4}$ の characteristic 部分群、あるいは $M$ の $G_{\mathbf Q}$-core で刻む — 開部分群の軌道は有限なので core は開)は本書では**提案のみ・未証明**。
  - **【GAP: NONLIN】** §6.8 (c) の二段構成のうち、onto/settlement という非線形 gate が線形解空間とどう交わるか。
  - **【UNKNOWN】** $\mathrm{STEP}_{ab}$ の真偽。**【UNKNOWN】** $S^t$ 段の非線形残差方程式の可解性。**【UNKNOWN】** B4-A / B4-B の別。**【UNKNOWN】** FC-1(A の正規性)— これが未確定である限り 3-primary sign 路線は前件未充足。
- **B4-B は宣言していない。** 本書は T-33 §4 の 4 問・T-34 の評価・T-35 の κ+Θ 評価・発案札との合成の裁定のみである。
- 発案札(`docs/notes/t33_ideas_v1.md`)は全札 candidate として扱い、採否と根拠を §3.1・§4.7・§6.8–6.10 に明記した。札 B-6 の「2008.00066 未入手」は誤りであること(papers/ に収蔵済・裁定 596)を確認した上で読んだ。

---

## Erratum(2026-08-19・本文凍結・追記のみ)

**§2.5 命題 T33-P2 は誤っている。** 「(CH-p) が成り立てば $[\mathrm{ML}(K):J]=|\operatorname{im\,ob}|$ は $p$ 冪」という結論が偽 — crossed homomorphism の像は一般に部分群でないので、$|\operatorname{im\,ob}|$ が $|\mathcal O|$ を割る保証がない。反例: $C_3\curvearrowright C_7$ で index 3、係数 7。
⟹ **(CH-p) だけでは設問 1 の「characteristic 3 のみへの縮約」は出ない。** 必要なのは **(CH-p′)**(障害写像が $3'$-群への真の準同型、または zero-fibre index が直接 $3'$-数)。詳細・検算・修理不能性の議論は `docs/notes/chp_proof_v1.md` の **Erratum E-2**。出典 = Sol T-42 監査。
**影響しないもの**: §2.3 の **T33-T2(SYL3)**(Sylow と Lagrange のみ使用)、**T33-L4**、**T33-T1**、**T33-L8**、§6 の T-34 評価 — いずれも crossed hom を使わないので無傷。
また §2.5 に添えた【文献要請】は、`chp_proof_v1.md` §6 で「関係加群による正規閉包の線形化定理」へ絞り込み済み。
