# ideas_020 の数学検分 — 1-A / 1-C / 1-D / 付録 A + W-5 erratum 原稿 **v1**

**状態札: `検分書 / 紙のみ / 新規機械計算ゼロ(整数 6 行の charming 会計検算 1 本のみ)/ Lean 検証ではない / 封印 3 量非接触・Im R 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-04・**新設 v1**
- 委嘱: 司令塔 — 「`ideas_020_w6_target.md` の 1-A【ROOF-KILL】/ 1-C【W-TRANS】/ 1-D【THETA-GONE】/ **付録 A【W-5 スケッチ】(最重要・ENT-1 との整合が必須)** の数学検分 + campaign §3.7 W-5 行 erratum 節の起草」
- 検分対象: `docs/notes/ideas_020_w6_target.md`(発案係・全札 candidate)
- 入力正本: `docs/notes/k5_w6_construction_v1.md`(§1.2 命題 K5-BIT の系・§2.1 (V-ab)(V-der)(V-cen) と $\psi_V$・§2.3 定理 W6-OBS・§3.3 生存表・§4.2 補題 SURJ-W6・§4.4 篩 W6-F)/ `docs/notes/k5_w6_construction_v1_addendum_b_k20paper.md`(**§1 正典 (3.1) の $\psi_m$・§2.1 $A_m=\langle r^2\rangle^3$ と基底 $(X^2,Y^2,(XY)^{-2})$・§2.3 (4.7)(4.8) の逐語成立**)/ `docs/notes/k5_dn_prereg_k20_draft_v1.md` **§2.6**((V-der) 破れ・$W:=V\cap[P_N,P_N]$)/ `docs/notes/k5_genuine_campaign_v1.md` §2.3・§3.7・§4.3 / `docs/notes/roof2_cv9_freeze_v1.md` §7.4(標的 ENT-1)/ `docs/notes/no_ent3_v1.md`・`provenance/CLAIMS.md` NO-ENT(3) / `provenance/LEDGER.md` 裁定 405・416・472・**473** / `scratchpad/w5_order_check.g`+`.log`(裁定 473 の実測)
- **外部文献ゼロ。**

> ## 非接触の申告
> - **$\mathrm{Im}\,R_{N,K^{(5)}}$ を一度も測っていない。** 本稿は紙 + 有限群論のみ。
> - **封印 3 量非接触**($\hat c_\mu$ / PSL 窓の構造量 / ε bits)。**$u$ 値・曲線・dessin・Kummer にも一切触れていない。**
> - 使った $n=5$ の情報は $G_5$ の**構造**($\lvert G_5\rvert=500$・$A\cong C_5^3$・$G_5^{\rm ab}\cong C_2^2$)、正典 (3.1) の $\psi_m$、(4.7)(4.8) の作用式、$\phi_1$ の座標 $f_1=(r^2,r^{-2},1)$(裁定 396/398 で封印解除済)だけである。
> - **新規機械計算は発注していない。** 本稿の唯一の機械実行は charming 会計の整数 6 行(§5.3・`scratchpad/w5_charming_check.py`)であり、群計算ではない。

---

## 0. 判定(先に 6 行)

| # | 対象 | 判定 |
|---|---|---|
| **①** | **1-A【ROOF-KILL】** | ★★ **条件つきで定理候補として立つ**(§1 に **命題 ROOF-KILL** を証明つきで起草)。ただし発案の言い方「**屋根型は成分合成 witness で死ぬ**」は**そのままでは偽** — 前件 (d)($V\subseteq[P_N,P_N]$)が要り、**$K^{(20)}$ はまさにそれが破れる屋根**である(prereg §2.6 の (V-der) 破れと同じ 1 点)。発案自身の「破綻しそうな点」(全滅と局在の混同)は**正しい警戒**だった |
| **②** | **1-C【W-TRANS】** | ★ **機構化は正しい**(§2)。$W=\ker(V\to P_N^{\rm ab})$ の五項完全列表示は成立、$K^{(20)}$ instance も再現。**二択への回答は「消滅機構が在る」側** — ただし射程は **(V-der) が成立する窓に限る**。⟹ **p=2 の生存域は $\dim W\ge2$、または $\dim W=1$ かつ (V-der) 破れ、に縮む**(発案が期待した「掘る空間が半減」は**その通りに起きる**) |
| **③** | **1-D【THETA-GONE】** | ★★ **恒等は正しい・代表の同定も正しい**(§3)。$w=x^2y^{-2}$ で $w\theta(w)=1$ は $F_2$ で恒等、$\psi_5(w)=X^2Y^{-2}=(r^2,r^{-2},1)=f_1$ は addendum B の基底で**紙で確認**した。判定式 $\beta_\tau\in N_\tau(\ker N_\theta\vert_W)$ も**同値**である。⚠ **ただし必須の前件が 1 つ抜けている**: $\bar w\in[P_N,P_N]$。これは **(V-der) と同値に近い**(§3.3)— $K^{(20)}$ では**破れる** |
| **④** | **付録 A【W-5】** | ★★ **全段が成立する**(§4)。$\lvert PB_3/N\rvert=1000$・$V\cong C_2$ 中心・**非分裂**(Arf 型・私はより短い直接証明を与えた)・$V\subseteq[P,P]$・witness $(f_1,+1)$ で **$d_{W\text{-}5}=5$**。⚠ 未確認の前件 1 件(**isolated**)は §4.6 に【GAP】として立てた |
| **⑤** ★★ | **ENT-1 との整合** | ★★ **完全に無矛盾。切り分け成立**(§4.5)。ENT-1 の走査域は **$n=3$・$[K^{(3)}:N']=3$($p=3$ 核)・$[B_3:N']=1944$**。W-5 は **$n=5$・$[K^{(5)}:N]=2$($p=2$ 核)・$[B_3:N]=6000$** — **3 つの軸すべてで走査域の外**。さらに NO-ENT(3) は登録時に「**他の $n$ へ広げない**」と射程を固定済み。**どちらも誤りではない** |
| **⑥** | **novelty の型** | ⚠ **「entangled 実在庫」だけでは新規ではない**(§4.4)。$K^{(9)}/K^{(3)}$・$K^{(25)}/K^{(5)}$ が既在(K5-ENT-INSUF)。**新規なのは「屋根型で非分裂」= entangled *屋根* の初の実在庫**という点である。この 1 語を落とすと novelty grep 違反になる |

> ### ★ 一行で
> $$\boxed{\ \textbf{発案の 3 札(1-A / 1-C / 1-D)は、まとめて 1 本の否定定理に収束する:}\ \textbf{(V-der) を満たす細分で }\dim_{\mathbf F_2}W\le1\ \textbf{なら検出力ゼロ。}\ }$$
> W-5 はその初の実物であり、$K^{(20)}$ は「(V-der) が破れるので定理の射程外」の実物である。⟹ **2-primary 標的(w6 §3.4 順位 1)の最下段 $\lvert PB_3/N\rvert=500\cdot2$ は本稿で死ぬ**(§6 FINDING R-5)。

---

## 1. 1-A【ROOF-KILL】の検分 — **条件つきの定理として立つ**

### 1.1 発案の主張(逐語)

> $N=K^{(5)}\cap N'$($N'$ isolated・$N'\not\subseteq K^{(5)}$)のとき $P_N$ は subdirect($P_N\hookrightarrow G_5\times PB_3/N'$)であり、$\widetilde m=0$ の (N_θ)(N_τ)(SURJ) 系は**成分ごとに分解**する。… ⟹ **障害は $N'$ 側の 1 個の類に局在し、多くの在庫窓で消える**。

### 1.2 ★ 命題 ROOF-KILL(**本稿が起草する条件つき形・candidate**)

> ### 命題 ROOF-KILL(candidate・第 4 の死因型)
> $N'\trianglelefteq B_3$、$c\in N'$、$N:=K^{(5)}\cap N'$、$G':=PB_3/N'$、$P:=P_N=PB_3/N$、$D:=PB_3/(K^{(5)}N')$(Goursat の共通商)、$V:=K^{(5)}/N=\ker(P\to G_5)$ とする。
> **(a)【Goursat】** $P=G_5\times_D G'$(fiber product)。とくに $V\cong V':=\psi_{N'}(K^{(5)})\trianglelefteq G'$。
> **(b)** $f_1$ の $D$ における像が自明 — **とくに $5\nmid\lvert D\rvert$ のとき** — ならば $\pi^{-1}(f_1)=\{(f_1,v):v\in V'\}$。
> **(c)【成分合成 witness】** (b) の下で $\widetilde f:=(f_1,1)$ は $\widetilde m=0$ の 2 本のノルム方程式を**満たす**:
> $$\widetilde f\,\theta(\widetilde f)=1,\qquad \tau^2(\widetilde f)\,\tau(\widetilde f)\,\widetilde f=1 .$$
> **(d)** さらに $V\subseteq[P,P]$(= 前件 **(V-der)**)ならば $\widetilde f\in[P,P]$。
> **(e)** さらに $V$ が $P$ の中心に入るならば $V\subseteq\Phi(P)$ であり、**(SURJ) は自動**である。
> $$\Longrightarrow\ \boxed{\ \textbf{(b)+(d)+(e) かつ }N\textbf{ が isolated }\Longrightarrow\ \phi_1\in\mathrm{Im}\,R_{N,K^{(5)}},\quad d_N=5,\quad\textbf{検出力ゼロ}\ }$$

**証明.**

**(a)** $N=K^{(5)}\cap N'$ ゆえ $P\hookrightarrow G_5\times G'$ は単射で、両射影は全射。Goursat により像は共通商 $D=PB_3/(K^{(5)}N')$ 上の fiber product。$\ker(P\to G_5)=K^{(5)}/N\cong\psi_{N'}(K^{(5)})=V'$。∎

**(b)** $(f_1,v)\in P\iff$ $f_1$ と $v$ の $D$-像が一致。$f_1\mapsto1$ なら条件は $v\in\ker(G'\to D)$。$\lvert D\rvert$ が 5 と互いに素なら、$f_1\in A=[G_5,G_5]\cong C_5^3$ の像は $D$ の 5-元であり自明。fiber は $\ker(P\to G_5)=V'$ の左剰余類 $= V'$ 自身。∎

**(c)** $\theta,\tau$ は $F_2$ の自己同型で $K^{(5)},N'$ をともに保つ($K^{(5)}$ は正典 Prop 3.1、$N'\trianglelefteq B_3$)ので、埋め込み $P\hookrightarrow G_5\times G'$ は $\Gamma$-同変。ゆえに成分ごとに計算してよい。
- **第 2 成分**: $\theta(1)=\tau(1)=1$ ゆえ両ノルムとも $1$。
- **第 1 成分**: 座標 $(n_1,n_2,n_3)$($a=(r^{2n_1},r^{2n_2},r^{2n_3})$)で $f_1=(1,-1,0)$。正典 **(4.7)** $\theta(n_1,n_2,n_3)=(n_2,n_1,-n_3)$ より $\theta(f_1)=(-1,1,0)$、$f_1+\theta(f_1)=(0,0,0)$ ✓。正典 **(4.8)** $\tau(n_1,n_2,n_3)=(n_3,n_1,n_2)$ より $\tau(f_1)=(0,1,-1)$、$\tau^2(f_1)=(-1,0,1)$、和 $=(0,0,0)$ ✓。∎

**(d)** 射影 $[P,P]\to[G_5,G_5]=A$ は全射(全射準同型は交換子群を交換子群に写す)。$f_1\in A$ ゆえ $(f_1,v_1)\in[P,P]$ なる $v_1$ が在り、(b) より $v_1\in V'$。$(1,v_1)\in V\subseteq[P,P]$(仮定)だから $(f_1,1)=(f_1,v_1)\cdot(1,v_1)^{-1}\in[P,P]$。∎

**(e)** $M$ を $V\not\subseteq M$ なる極大部分群とすると極大性から $MV=P$。$V$ が中心ゆえ $M$ は $M$ と $V$ の両方で正規化され $M\trianglelefteq P$。極大かつ正規なので $P/M$ は真の非自明部分群をもたない ⟹ 素数位数巡回 ⟹ 可換 ⟹ $[P,P]\subseteq M$ ⟹ (d) の仮定より $V\subseteq M$、矛盾。ゆえに $V\subseteq\Phi(P)$。あとは **補題 SURJ-W6**(w6 §4.2)の Frattini 論法: level 5 の (SURJ) から $H:=\langle\bar x,\widetilde f^{-1}\bar y\widetilde f\rangle$ は $G_5$ 上全射 ⟹ $HV=P$ ⟹ $V\subseteq\Phi(P)$ より $H=P$。∎

**結論**: 命題 K5-BIT($\widetilde m=0$ の項)の 3 条件が揃うので $\phi_1\in\mathrm{Im}$、$d_N=5$。∎

### 1.3 ★ 発案の言い方のどこが強すぎるか(**前件 (d) は空虚でない**)

$$\boxed{\ \textbf{反例(前件 (d) が破れる屋根の実物): }K^{(20)}=K^{(5)}\cap K^{(4)}\ }$$

- $\lvert D\rvert=\lvert G_5\rvert\lvert G_4\rvert/\lvert G_{20}\rvert=500\cdot32/4000=4$ ⟹ **(b) は成立**($5\nmid4$)。
- しかし $V=\langle r^{10}\rangle^3\cong(\mathbf Z/2)^3$(addendum B §2.2)に対し **$\lvert V\cap[G_{20},G_{20}]\rvert=2$**(prereg §2.6 の実測)⟹ **(d) は破れる**。

**私の独立再導出**(紙・addendum B の基底で):$A_{20}=\langle r^2\rangle^3\cong(\mathbf Z/10)^3$、$Q=G_{20}/A_{20}\cong C_2^2$ の作用は $X\mapsto\mathrm{diag}(1,-1,-1)$、$Y\mapsto\mathrm{diag}(-1,1,-1)$(共役の直接計算)。ゆえに
$$I_QA_{20}=(2\mathbf Z/10)^3\cong C_5^3\ (\text{位数 }125),\qquad [X,Y]=(r^{-2},r^2,r^{-2})\ \text{すなわち}\ (-1,1,-1),$$
$$[G_{20},G_{20}]=I_QA_{20}+\langle(-1,1,-1)\rangle=\{n:\ n_1\equiv n_2\equiv n_3\ (\mathrm{mod}\ 2)\},\qquad \lvert[G_{20},G_{20}]\rvert=250 .$$
$V=\{n=5b:b\in\mathbf F_2^3\}$、$5b_i\equiv b_i\ (\mathrm{mod}\ 2)$ ゆえ
$$W=V\cap[G_{20},G_{20}]=\{b:b_1=b_2=b_3\}=\langle(1,1,1)\rangle\cong\mathbf F_2 .$$
★ **prereg §2.6 の $W=\langle(1,1,1)\rangle$(対角線)・$\lvert W\rvert=2$・$\lvert[G_{20},G_{20}]\rvert=250$ を、独立の紙経路で再現した。**

⟹ **「屋根は成分合成 witness で死ぬ」は $K^{(20)}$ では言えない**(実際 $K^{(20)}$ は $\widetilde m=0$ で witness $(0,6)$ をもつが、それは**成分合成ではない別経路**である・prereg §0-4)。

### 1.4 判定

| 項目 | 判定 |
|---|---|
| **定理候補として立つか** | ★ **立つ(条件つき)** — §1.2 の命題 ROOF-KILL。3 前件 (b)(d)(e) はいずれも**紙で判定でき、実装ゼロ**である |
| **「第 4 の死因型」という位置づけ** | ★ **妥当**。elementary-5 / WARN-13500 は $\operatorname{coker}\psi=0$(**障害群が消える**)で死に、$K^{(20)}$ は $\operatorname{coker}\ne0$ のまま**類が 0** で死ぬ。ROOF-KILL は「**類が 0 である理由が subdirect 構造から紙で読める**」型であり、prereg §0-3 の分類に**第 4 の欄を足す** |
| **「多くの在庫窓で消える」** | ⚠ **量化しないこと**。立証できたのは「3 前件を満たす屋根で消える」までである |
| **「障害は $N'$ 側の 1 個の類に局在」** | ★ **正しい・かつ強められる**。(b) の下で $\widetilde f$ の第 1 成分は $f_1$ に固定され、自由度は第 2 成分 $v\in V'$ のみ。⟹ **障害は $G'$(= $N'$ 窓)側のデータだけで決まる**。これは発案の核心であり、**成立する** |
| **【V-ESS】(札 1-B)への含意** | 札 1-B は「$V$ が essential」を必要条件に立てたが、**本命題が示すのは「(V-der) の破れ」または「$5\mid\lvert D\rvert$」の方が実効的な分岐点**であるということ。$K^{(20)}$ は essential 性ではなく **(V-der) で射程外**になった。⟹ **札 1-B の必要条件は (V-der) 側から書き直すべき**(本稿は札 1-B を検分対象としていないので提案に留める) |

---

## 2. 1-C【W-TRANS】の検分 — **機構化は正しい・二択の答は「消滅機構が在る」**

### 2.1 五項完全列表示の検証 — **成立**

$1\to V\to P\to G\to1$($V$ アーベル、$G:=G_5$)に対する **LHS ホモロジー五項完全列**:
$$H_2(P)\longrightarrow H_2(G)\xrightarrow{\ \mathrm{trans}\ }V_G=H_0(G,V)\longrightarrow P^{\rm ab}\longrightarrow G^{\rm ab}\longrightarrow0 .$$
$V\to P^{\rm ab}$ は共役作用が $P^{\rm ab}$ 上自明ゆえ $V_G$ を経由する。ゆえに
$$W=V\cap[P,P]=\ker\bigl(V\to P^{\rm ab}\bigr)=I_GV+\widetilde{\operatorname{im}(\mathrm{trans})}\qquad(I_GV=(1-G)V\ \text{は増大部分加群}).$$
$$\Longrightarrow\ \boxed{\ \textbf{発案の式 }W=(1-G_5)V+\operatorname{im}(\mathrm{trans})\ \textbf{は成立する}\ }$$
(記法の注: $\operatorname{im}(\mathrm{trans})\subseteq V_G$ を $V$ へ持ち上げる際の不定性がちょうど $I_GV$ なので、右辺は well-defined。)

**「transgression は拡大類 $[P]\in H^2(G,V)$ の関数」** — ★ **正しい**。
- **$G$-作用が自明な場合**: 普遍係数定理 $0\to\operatorname{Ext}^1(H_1(G),V)\to H^2(G,V)\to\operatorname{Hom}(H_2(G),V)\to0$ の右射が**まさに transgression** であり、$\mathrm{trans}=[P]$ の像。⟹ **拡大類から明示的に決まる**。
- **一般の作用**: $\mathrm{trans}$ は LHS ホモロジースペクトル系列の $d^2:E^2_{2,0}=H_2(G)\to E^2_{0,1}=V_G$ であり、拡大の同型類(= 作用 + 類)で決まる。⟹ **「決まる」は正しいが「閉じた式で計算できる」ではない**。
- ⚠ **発案の「紙決定」は自明作用の場合の話としては正確、一般には「決まるが計算は要る」に弱まる**。発案自身の破綻点(「$p\mid6$ で平均化が効かず filtration しか出ない」)は**別の・かつ実在する**懸念である。

### 2.2 $K^{(20)}$ instance の検証 — **一致**

- $V=\langle r^{10}\rangle^3$ への $G_{20}$-作用: $X$ は $\mathrm{diag}(1,-1,-1)$ で作用するが、$V$ 上では $-5\equiv5\ (\mathrm{mod}\ 10)$ ゆえ**恒等**。$Y$ も同様、$A_{20}$ は可換。⟹ **$G_5$-作用は自明**、$I_GV=0$ ✓。
- ゆえに $W=\operatorname{im}(\mathrm{trans})$。§1.3 の独立導出で $W=\langle(1,1,1)\rangle\cong\mathbf Z/2$ ✓。
- ⟹ **発案の $K^{(20)}$ 適用は正しい。**

### 2.3 ★ 発案の設問(二択)への回答

> **設問**(1-C 検証の一手目):「p=2・$W$ 自明 1 次元で障害類が非零になる細分は在り得るか、それとも(屋根に限らず)消滅機構があるか」

$$\boxed{\ \textbf{答: 消滅機構が在る。ただし射程は「(V-der) が成立する窓」に限る。}\ }$$

**根拠**($\Gamma$ が $W$ に自明に作用することは $\dim_{\mathbf F_2}W=1$ から**自動**である — $\operatorname{Aut}(\mathbf F_2)=1$):

| $\dim_{\mathbf F_2}W$ | 障害 | 判定 |
|---|---|---|
| **0** | $\beta_\theta,\beta_\tau\in W=0$ ゆえ**強制的に $0$**。$\widetilde f_0$ 自身が witness | ★ **常に消える(自明)** |
| **1**、かつ **(V-der) 成立**($W=V$) | §3 の **THETA-KILL**: canonical 代表 $\bar w$ が使えて $\beta_\theta=0$、さらに $N_\tau=\mathrm{id}$ が全射ゆえ $\beta_\tau$ は必ず解ける | ★★ **常に消える(証明つき・§3.4)** |
| **1**、かつ **(V-der) 破れ**($W\subsetneq V$) | $\bar w$ が $[P,P]$ に入る保証がない ⟹ $\beta_\theta$ は一般に非零でありうる | ⚠ **UNKNOWN**。$K^{(20)}$ は実際には消えた(witness $(0,6)$)が、それは別経路 |
| **$\ge2$** | $\operatorname{coker}\psi_W$ が非自明な情報をもちうる | ★ **生存域** |

### 2.4 篩への含意(発案の提案「$W$ が $\Gamma$-自明成分のみなら降格」)

★ **採用してよい・かつ強められる。** 発案は「降格」を提案したが、上表の第 2 行は**降格ではなく棄却**である。篩 W6-F(w6 §4.4)への提案:

> **W6-F3′(新設案)**: **$W:=V\cap[P_N,P_N]$ を計算し、$\dim_{\mathbf F_p}W$ で分岐する。**
> - $\dim W=0$ ⟹ **棄却**(障害は強制的に消える)。
> - $p=2$ かつ $\dim W=1$ かつ (V-der) 成立 ⟹ **棄却**(命題 THETA-KILL・§3.4)。
> - それ以外 ⟹ W6-F3(coker 計算)へ進む。
> ★ **F3 が $V$ でなく $W$ で評価すべきである**という発案 1-C の指摘は正しい(prereg §2.6 の CV-9 事案と同根 — cert の $\dim\operatorname{coker}\psi_V=1$ と窓の障害群 $\operatorname{coker}\psi_W$ は**別の加群で偶然同値**)。

---

## 3. 1-D【THETA-GONE】の検分 — **恒等は正しい・ただし前件が 1 つ抜けている**

### 3.1 恒等の検証 — **成立(自明)**

$\theta\in\operatorname{Aut}(F_2)$、$\theta:x\mapsto y,\ y\mapsto x$(w6 §1.3)。$w:=x^2y^{-2}$ に対し
$$w\,\theta(w)=x^2y^{-2}\cdot y^2x^{-2}=x^2x^{-2}=1\qquad\textbf{(}F_2\textbf{ で恒等)}\quad\checkmark$$

### 3.2 ★ 代表の同定 $\psi_5(x^2y^{-2})=f_1$ の検証 — **成立(紙で確認した)**

正典 (3.1)(addendum B §1 逐語): $\psi_m:PB_3\to D_m^3$、$x\mapsto(r,s,s)$、$y\mapsto(rs,r,rs)$、$c\mapsto(1,1,1)$。
addendum B §2.1 の計算($rs$ は反射ゆえ $(rs)^2=1$、$sr=r^{-1}s$):
$$X^2=(r^2,1,1),\qquad Y^2=(1,r^2,1),\qquad (XY)^{-2}=(1,1,r^2).$$
これが基底 $a_1,a_2,a_3$ であり、座標 $(n_1,n_2,n_3)$ は $a=(r^{2n_1},r^{2n_2},r^{2n_3})$。ゆえに
$$\psi_5(w)=X^2Y^{-2}=(r^2,1,1)\cdot(1,r^{-2},1)=(r^2,r^{-2},1)=f_1\qquad\checkmark$$
$$\text{座標で}\quad (n_1,n_2,n_3)=(1,-1,0).$$
★ **発案が「addendum B §2.1 の基底で確認」と書いた点は正しい。私は逐語で追検算した。**

### 3.3 ⚠ ★ 抜けている前件 — $\bar w\in[P_N,P_N]$

命題 K5-BIT は $\widetilde f\in[P_N,P_N]$ を要求する。ところが **$w=x^2y^{-2}\notin[F_2,F_2]$**(アーベル化で $(2,-2)\ne0$)。ゆえに:

$$\boxed{\ \bar w\in[P_N,P_N]\iff 2(\bar x-\bar y)=0\ \text{in}\ P_N^{\rm ab}\ }$$

| 窓 | $P_N^{\rm ab}$ | $2(\bar x-\bar y)$ | $\bar w\in[P_N,P_N]$? |
|---|---|---|---|
| **W-5**($K^{(5)}\cap N_Q$) | $C_2^2$(**実測**: `w5_ab_check.g` の `AbelianInvariants(QW5)=[2,2]`) | $2\bar x=2\bar y=0$ | ★ **YES** |
| **$K^{(20)}$** | $C_2^2\ltimes$…、位数 16(§1.3 より $A_{20}/[G,G]\cong C_2^3/\langle(1,1,1)\rangle\cong C_2^2$、$G_{20}/A_{20}\cong C_2^2$) | $\bar a_1-\bar a_2=(1,1,0)\bmod\langle(1,1,1)\rangle\ne0$ | ★ **NO** |

⟹ **$K^{(20)}$ では canonical 代表が使えない。** 発案 1-D の「どの細分でも $\beta_\theta=0$ 表示が canonical に取れる」は**そのままでは偽**である。

> ### ★ 修理は 1 行で済む(**そして (V-der) と結びつく**)
> $V\subseteq[P_N,P_N]$(= 前件 **(V-der)**)ならば $P_N^{\rm ab}=P_N/[P_N,P_N]\cong G_5/[G_5,G_5]=G_5^{\rm ab}\cong C_2^2$ であり、そこでは $2\bar x=0$。
> $$\Longrightarrow\ \boxed{\ \textbf{(V-der)}\ \Longrightarrow\ \bar w\in[P_N,P_N]\ \Longrightarrow\ \beta_\theta=0\ \textbf{が canonical に取れる}\ }$$
> ⟹ **1-D の正しい前件は (V-der) である。** これは 1-A の前件 (d)・1-C の $W=V$ 条件と**同じ 1 点**であり、3 札が同一の分岐点に収束していることを意味する。

### 3.4 ★ 命題 THETA-KILL(**本稿が起草する・candidate**)

> ### 命題 THETA-KILL(candidate)
> $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$c\in N$、$P:=P_N$、$V:=K^{(5)}_{F_2}/N_{F_2}$ とし、**(V-ab)**・**(V-der)**($V\subseteq[P,P]$)・**$V$ が $P$ の中心に入る**を仮定する($\Rightarrow W=V$)。$w:=x^2y^{-2}$ と置く。
> **(1)** $\bar w\in[P,P]$ かつ $\bar w\bmod V=f_1$。ゆえに $\widetilde f_0:=\bar w$ は許容される持上げである。
> **(2)** $\beta_\theta=\overline{w\,\theta(w)}=1$ **(恒等的)**。
> **(3)** 障害は $\beta_\tau:=\overline{\tau^2(w)\tau(w)w}\in W$ の **1 個の membership 条件** $\beta_\tau\in N_\tau(\ker N_\theta\vert_W)$ に**同値に**帰着する。
> **(4)** ★ とくに **$\dim_{\mathbf F_2}V=1$**($p=2$)ならば $N_\theta=1+\theta=2=0$、$N_\tau=1+\tau+\tau^2=3=\mathrm{id}$ ゆえ $\ker N_\theta=W$、$N_\tau(W)=W$ で条件は**恒真**。さらに (SURJ) は自動(§1.2 (e))。
> $$\Longrightarrow\ \boxed{\ V\ \textbf{中心・}V\subseteq[P,P]\textbf{・}\dim_{\mathbf F_2}V=1\ \Longrightarrow\ d_N=5\ (\textbf{検出力ゼロ})\ }$$

**証明.** (1) §3.2(代表)+ §3.3(修理)。(2) §3.1 の恒等の像。(3) $\widetilde f_0\mapsto\widetilde f_0b'$($b'\in W$)で $(\beta_\theta,\beta_\tau)\mapsto(\beta_\theta+N_\theta b',\beta_\tau+N_\tau b')$。$\beta_\theta=0$ を保つ自由度は**ちょうど $\ker N_\theta$** であり、そのとき $\beta_\tau$ は**ちょうど $N_\tau(\ker N_\theta)$ だけ動く**。ゆえに「$(0,-\beta_\tau)\in\operatorname{im}\psi_W$」と「$\beta_\tau\in N_\tau(\ker N_\theta)$」は同値。(4) 直接代入。∎

> ★ **発案 1-D の「破綻しそうな点」への回答**: 「$\beta_\theta=0$ を保ったまま $\beta_\tau$ を動かす自由度が $N_\tau(\ker N_\theta)$ と正確に一致するか」— ★ **一致する**((3) の証明)。**判定式は片側条件ではなく同値である。**

### 3.5 副次的な指摘(**札 2-B の篩の修正**・検分対象外だが 1-D から直接従う)

札 2-B は「(b) $W_\tau$-像 $=1$ なら**即棄却**」と書くが、**これは棄却条件を過小評価している**。正しくは:
- $\dim W=1$($p=2$)では $N_\tau=\mathrm{id}$ が全射なので、**$W_\tau$-像が $1$ でなくても棄却**される(§3.4 (4))。
- 一般には篩の判定は「$\overline{W_\tau}=1$」ではなく「$\overline{W_\tau}\in N_\tau(\ker N_\theta\vert_W)$」である。
⟹ **札 2-B (b) は「$\overline{W_\tau}\in N_\tau(\ker N_\theta\vert_W)$ なら棄却」に置き換えるべき**(語 2 個の評価で済むという利点は不変)。

---

## 4. 付録 A【W-5 スケッチ】の検分(**最重要**)

### 4.1 検分表(手順 1〜5 の逐項)

| 手順 | 付録 A の主張 | 判定 | 根拠 |
|---|---|---|---|
| **1** | $G_5$ と $Q_8$ は $PB_3$ の**同一の $C_2^2$ 商**($x,y$ の mod-2 類)を共有 | ★ **成立** | $G_5^{\rm ab}\cong C_2^2$・$Q_8^{\rm ab}\cong C_2^2$、いずれも $\bar x,\bar y$ で生成($c\mapsto0$)。実測: `AbelianInvariants(G5)=AbelianInvariants(Q8)=AbelianInvariants(QW5)=[2,2]`(裁定 473) |
| **2** | $\lvert PB_3/N\rvert=500\cdot\lvert\psi_Q(K^{(5)})\rvert=1000$、$\psi_Q(K^{(5)})=\{\pm1\}$ | ★★ **成立・実測一致** | 紙: $K^{(5)}\subseteq(\text{mod-2 核})$ ゆえ $\psi_Q(K^{(5)})\subseteq\ker(Q_8\to C_2^2)=\{\pm1\}$;$x^{10}\in K^{(5)}$($\mathrm{ord}(\bar x)=10$)で $\psi_Q(x^{10})=i^{10}=i^2=-1$ ⟹ 等号。実測(裁定 473): $\lvert PB_3/N\rvert=1000$・$\lvert\mathrm{Image}(\mathrm{proj}_{Q_8},\ker\mathrm{proj}_{G_5})\rvert=2$ |
| **3** | $B_0=1\times\{\pm1\}$ は中心・拡大は **非分裂**(Arf 型類の inflation) | ★★ **成立**(私はより短い直接証明を与えた・§4.2) | 中心性: $\{\pm1\}=Z(Q_8)$。非分裂: §4.2。類の同定: §4.3 |
| **4** | $[P,P]=A\times\{\pm1\}$、$\widetilde f=(f_1,+1)\in[P,P]$、$\theta$-ノルム $=\tau$-ノルム $=1$、SURJ 成立 ⟹ $d_{W\text{-}5}=5$ | ★★ **全段成立**(§4.2 (c)(d)(e)) | $\lvert[P,P]\rvert=1000/4=250$(実測 $P^{\rm ab}=C_2^2$)。$[P,P]$ は $A$ の全逆像 $=A\times\{\pm1\}$。ノルムは §1.2 (c) の計算 |
| **5** | 教訓: 非分裂でも subdirect が witness を成分合成させる = **第 4 の死因型** | ★ **成立**(§1 の命題 ROOF-KILL がその一般形) | — |

### 4.2 ★ 私の再証明(**より短く・より強く**)

$P=G_5\times_{C_2^2}Q_8$($\lvert P\rvert=1000$)、$V=1\times\{\pm1\}$、$\pi:P\to G_5$。

> **(a) $V$ は $P$ の中心に入る。** $\{\pm1\}=Z(Q_8)$、$G_5$ 成分は $V$ と可換。∎
>
> **(b) 拡大 $1\to V\to P\to G_5\to1$ は非分裂。** 分裂 $\iff$ 準同型 $\sigma:G_5\to Q_8$ で $G_5\twoheadrightarrow C_2^2$ を持ち上げるものが在る。$\sigma(A)$ は $A\cong C_5^3$ の準同型像かつ $Q_8$ の部分群 ⟹ 位数は 125 と 8 の公約数 $=1$ ⟹ $\sigma$ は $G_5/A\cong C_2^2$ を経由する ⟹ **$Q_8\twoheadrightarrow C_2^2$ が分裂することになる**が、$Q_8$ の対合は $-1$ ただ 1 個で $C_2^2$ を含まない。矛盾。∎
> ★ **コホモロジーも LHS も使わない 4 行の証明である**(付録 A の「$\lvert A\rvert=125$ 奇 ⟹ LHS 退化で inflation 単射」も正しいが、こちらの方が前件が少ない)。
>
> **(c) $[P,P]=A\times\{\pm1\}$、位数 250。** $P^{\rm ab}\cong C_2^2$(実測)⟹ $\lvert[P,P]\rvert=250$。$[P,P]$ は $[G_5,G_5]=A$ 上に全射し、$A$ の $P$ における全逆像は $\{(a,q):a\in A,\ q\in\ker(Q_8\to C_2^2)\}=A\times\{\pm1\}$(位数 250)。位数が等しいので一致。∎
> **直接確認**: $[X,Y]_P=([X,Y]_{G_5},[i,j])=((-1,1,-1),-1)$。第 1 成分の位数は 5 ゆえ $[X,Y]_P^5=(1,-1)$ ⟹ **$V\subseteq[P,P]$**(付録 A の「奇数冪」= 5 乗)。∎
>
> **(d) witness.** $(f_1,+1)\in[P,P]$ ✓((c))。$\pi(f_1,+1)=f_1$ ✓。ノルムは §1.2 (c) の計算(第 2 成分は $\theta(1)=\tau(1)=1$、第 1 成分は (4.7)(4.8) で $0$)。∎
>
> **(e) SURJ.** (a)+(c) と §1.2 (e) より $V\subseteq\Phi(P)$、Frattini で自動。∎
>
> **(f) 1-D との一致(★)**: $\psi_Q(w)=\psi_Q(x^2y^{-2})=i^2(j^2)^{-1}=(-1)(-1)^{-1}=(-1)(-1)=+1$、$\psi_5(w)=f_1$(§3.2)。
> $$\Longrightarrow\ \boxed{\ \textbf{付録 A の witness }(f_1,+1)\ \textbf{は、1-D の canonical 代表 }\bar w=\overline{x^2y^{-2}}\ \textbf{そのものである}\ }$$
> さらに $\beta_\tau=\overline{W_\tau}$ を計算すると:$\psi_Q(z)=(ij)^{-1}=-k$、$W_\tau=z^2x^{-2}\cdot y^2z^{-2}\cdot x^2y^{-2}\mapsto(-1)^6=+1$、第 1 成分も $0$ ⟹ **$\beta_\tau=0$ も成立**。⟹ **W-5 は命題 THETA-KILL(§3.4)の第 1 の実物である。**

$$\Longrightarrow\ \boxed{\ d_{W\text{-}5}=5,\quad\textbf{検出力ゼロ。付録 A の結論は正しい。}\ }$$

### 4.3 Arf 型類の同定 — **成立**

$P$ は fiber product ゆえ拡大類は $1\to\{\pm1\}\to Q_8\to C_2^2\to1$ の類の $G_5\twoheadrightarrow C_2^2$ に沿う **inflation**。$H^2(C_2^2;\mathbf F_2)$ は $\{a^2,ab,b^2\}$ を基底とする 3 次元で、$GL_2(\mathbf F_2)=S_3$ の不変部分は
$$\alpha a^2+\beta ab+\gamma b^2\ \text{が不変}\iff\alpha=\beta=\gamma\quad(\text{$b\mapsto a+b$ と $a\leftrightarrow b$ の 2 本で確認})$$
すなわち $\{0,\ a^2+ab+b^2\}$ の 1 次元。$a^2+ab+b^2$ は Arf 不変量 1 の二次形式 ⟹ **$Q_8$**(Arf 0 は $D_8$)。⟹ **付録 A の「$S_3$-不変な唯一の非零類」は正しい。** ∎

### 4.4 ⚠ novelty の型の訂正

| 表現 | 判定 |
|---|---|
| 「**本質的 entangled の実在庫**」(単体) | ⚠ **新規ではない**。K5-ENT-INSUF が $K^{(9)}/K^{(3)}$(補群なし・かつ $R$ 全射 12/12)と $K^{(25)}/K^{(5)}$($5A_{25}\subset\Phi$)を既に登録している |
| ★ 「**屋根型で非分裂**(entangled *屋根* の実在庫)」 | ★ **これが新規**。ENT-1(裁定 405)が探していたのは**まさにこの型**であり、$n=3$ 側は空だった。$n=5$・$p=2$ 側で**初めて実物が出た** |
| 「非分裂の紙判定・位数 1000・witness 明示は grep で未出」(札 2-D) | ★ **正しい**(裁定 473 で位数は確定・非分裂判定と witness は本稿が初の証明) |

⟹ **記帳語は「工房初の entangled *屋根*」とし、「工房初の entangled 窓」とは書かないこと。**

### 4.5 ★★ ENT-1 との整合判定(**委嘱の必須項目**)

**ENT-1 の走査域**(`roof2_cv9_freeze_v1.md` §7.4 逐語 + 裁定 405):
$$N'\trianglelefteq B_3,\quad N'\subseteq K^{(3)},\quad [K^{(3)}:N']=3,\quad PB_3/N'\ \text{が}\ G_3\ \text{の非分裂}\ \chi_i\text{-拡大(位数 324)},\quad [B_3:N']=6\cdot324=\mathbf{1944}.$$
**結果**(裁定 405): 指数 1944 の宇宙で該当窓は 1 件のみ・それは**分裂** ⟹ この深さに非分裂 $\chi_i$-拡大窓は無い(**bounded negative**)。さらに **NO-ENT(3)**(裁定 416/422・CLAIMS 登録)により **紙で空**が確定し、**1944 走査は較正へ降格**(非存在証明の役割を持たない)。

**W-5 の位置**:
$$N=K^{(5)}\cap N_Q,\quad N\subseteq K^{(5)},\quad [K^{(5)}:N]=\lvert\psi_Q(K^{(5)})\rvert=\mathbf 2,\quad \lvert PB_3/N\rvert=1000,\quad [B_3:N]=6\cdot1000=\mathbf{6000}.$$

| 軸 | ENT-1 の走査域 | W-5 | 判定 |
|---|---|---|---|
| **窓の基底** | $K^{(3)}$($n=3$) | **$K^{(5)}$**($n=5$) | ★ **外** |
| **核の位数(標数)** | $C_3$($p=3$・指数 3) | **$C_2$**($p=2$・指数 2) | ★ **外** |
| **$B_3$ 指数** | **1944** | **6000** | ★ **外** |
| **NO-ENT(3) の登録射程** | 「指数 9 以上、他の $n$、$B_3$-正規性を外した対象へは広げない」(CLAIMS 逐語) | $n=5$ は**明示的に射程外** | ★ **外** |

$$\Longrightarrow\ \boxed{\ \textbf{完全に無矛盾。ENT-1 / NO-ENT(3) と W-5 は「どちらかが誤り」の関係に立たない。}\ }$$

> ### ★ さらに: 機構レベルでも整合している(**偶然の一致ではない**)
> - **NO-CENTRAL の $n=5$ 版**(campaign §3.5 (1)): $H^2(G_5,\mathbf F_5)=0$ ⟹ **中心 $C_5$ 拡大は全部分裂**。
> - **W-5 は中心 $C_2$ 拡大**であり、$2\mid\lvert G_5\rvert=500$ ゆえ $H^2(G_5,\mathbf F_2)\ne0$(実際 Arf 類の inflation が非零・§4.3)。
> - ⟹ **「中心拡大は死ぬ」は標数 5 の話であり、標数 2 では成り立たない。** これは **w6 §3.4 の順位 1 の予測**(「2-primary 核: $2\mid\lvert G_5\rvert$ ゆえ $H^2(G_5,V)\ne0$ が期待でき、**非分裂拡大の供給も期待できる**」)が**初めて実物で当たった**ことを意味する。
> - ⚠ **しかし供給が在ることと検出力が在ることは別**である: W-5 は供給側の予測を当てた上で、**検出力の側で死んだ**(命題 THETA-KILL)。

### 4.6 ⚠ 未確認の前件(**【GAP】として立てる**)

| # | 項目 | 状態 |
|---|---|---|
| **【W5-GAP-1】** ★ | **$N=K^{(5)}\cap N_Q$ が isolated か**(命題 K5-BIT の必須前件・(HOM)) | ★ **UNKNOWN**。付録 A も本稿も検査していない。**isolated でなければ $d_N$ は主張できない**(campaign §5.2 段 K5-8 の「真の settled 判定」が対応する検査)。⟹ **$d_{W\text{-}5}=5$ は「isolated ならば」の条件つき結論**である |
| **【W5-GAP-2】** | $N_Q$ の生成規約($x\mapsto i,\ y\mapsto j,\ c\mapsto1$)が狩場計画 §・campaign §3.7・裁定 473 の検算スクリプトで**同一**か | ★ **実質確認済**。`w5_order_check.g` は `search/week3-battery-common.g` の `MakeQ8()` を逐語再利用しており、付録 A §0 の規約と同一と申告されている。⚠ **CV-9 判読としては非当事者判読を経ていない**(札 2-D 自身が「別の $N_Q$ を指している可能性を 1 度は疑うべき」と書いた点) |
| **【W5-GAP-3】** | $\theta,\tau$ が $N_Q$ を保つこと($N_Q\trianglelefteq B_3$) | ★ **私が確認した**: $\theta$ は $i\leftrightarrow j$($Q_8$ の自己同型)、$\tau$ は $i\mapsto j\mapsto -k\mapsto i$(検算: $\sigma(i)\sigma(j)=j(-k)=-i=\sigma(k)$、$\sigma^3=\mathrm{id}$)⟹ ともに $\operatorname{Aut}(Q_8)$ の元 ⟹ $N_Q\trianglelefteq B_3$ ✓。**$N=K^{(5)}\cap N_Q$ は $B_3$-正規な細分である** |

---

## 5. 【収載用原稿】`k5_genuine_campaign` v2 §3.7 erratum 節

> ## ⚠ 本節は **原稿**である
> - **`k5_genuine_campaign_v1.md` は 1 バイトも改変していない。** 以下は同ノートの **v2 改版時に §3.7 の直後へ挿入するための逐語原稿**である(適用は司令塔検収後)。
> - 正本は **裁定 473**(`provenance/LEDGER.md` 2026-08-04)。裁定 236 の正誤表形式に倣う。

---

### 【収載原稿ここから】

### 3.7.1 ★ erratum(**裁定 473** — W-5 行の 3 値の訂正)

**§3.7 の候補窓一覧の W-5 行($N=K^{(5)}\cap N_Q$)に誤りがあった。** 裁定 473 の実測(`scratchpad/w5_order_check.g` + `.log`・既存 fiber-product 構成の逐語流用・**証明書非読**・生成器から新規構築)により訂正する。

| 欄 | v1 の記載 | ★ **正** | 根拠 |
|---|---|---|---|
| $\lvert PB_3/N\rvert$ | **4,000** | ★ **1,000** | 実測。$4000$ は**直積上限** $\lvert G_5\rvert\cdot\lvert Q_8\rvert=500\cdot8$ であり、$G_5$ と $Q_8$ が **$PB_3$ の同一の $C_2^2$ 商**($x,y$ の mod-2 類)を共有するため対角に潰れて $500\cdot8/4=1000$ |
| $N_{\rm ord}$ | **40** | ★ **20** | 実測 `Lcm(Order(xhat),Order(yhat))=20`。紙でも $\mathrm{lcm}(\mathrm{ord}_{G_5}(X),\mathrm{ord}_{Q_8}(i))=\mathrm{lcm}(10,4)=20$。**40 は $\mathrm{lcm}(10,8)$ = $Q_8$ の位数を指数と取り違えた値** |
| $\lvert\mathcal X_N\rvert$ | **32** | ★ **16** | $\mathcal X_N=\{\widetilde m\bmod N_{\rm ord}:\gcd(2\widetilde m+1,N_{\rm ord})=1\}$。$N_{\rm ord}=20=2^2\cdot5$ で $2\widetilde m+1$ は奇ゆえ条件は $\widetilde m\not\equiv2\ (\mathrm{mod}\ 5)$、$20-4=16$ 個。**$\mathcal X_{20}$ は $K^{(20)}$(W-3 行)と同一の集合**である |
| 族 | **B?(要判定)** | ★ **C(entangled)** | 拡大 $1\to\{\pm1\}\to PB_3/N\to G_5\to1$ は**非分裂**($\sigma:G_5\to Q_8$ が存在すれば $\lvert\sigma(A)\rvert\mid\gcd(125,8)=1$ ゆえ $C_2^2\to Q_8$ の分裂を要するが $Q_8$ の対合は 1 個)。拡大類は $Q_8$ の Arf 型類($a^2+ab+b^2$・$H^2(C_2^2;\mathbf F_2)$ の $S_3$-不変な唯一の非零類)の inflation |
| 予言 $d_N$ | **5(分裂なら)** | ★ **5(非分裂だが死ぬ — 第 4 の死因型)** | witness $\widetilde f=(f_1,+1)=\overline{x^2y^{-2}}$ が $\widetilde m=0$ の (N$_\theta$)(N$_\tau$)(SURJ) を満たす(`ideas_020_review_v1.md` §4.2)。⚠ **isolated 性は未確認**(【W5-GAP-1】) |
| 全列挙 raw | **4,000** | **4,000**(★ **値は不変・根拠が変わる**) | 正しい根拠は $\lvert\mathcal X_N\rvert\cdot\lvert[P_N,P_N]\rvert=16\cdot250$。$\lvert[P_N,P_N]\rvert=1000/4=250$($P_N^{\rm ab}\cong C_2^2$ の実測)。**v1 の 4,000 は偶然一致した数値であり、v1 の内訳では再現しない** |
| K5-BIT 走査 | **要計算** | ★ **4** | §3.7.2 |

> ### ★ 誤りの機構(**再発防止のため名指しする**)
> **2 つの誤りは同一の型である**: $Q_8$ を「位数 8 の第 2 成分」として**直積のように**扱い、(i) 位数を $500\times8$、(ii) 指数を $\mathrm{lcm}(10,8)$ と取った。**実際には $G_5$ と $Q_8$ は共通商 $C_2^2$ を持つ fiber product であり、位数は 1/4 に落ち、$Q_8$ の指数は 8 でなく 4 である。**
> ⚠ **§3.7 の W-5 行の注記自身が正しく警告していた**:「$Q_8^{\rm ab}=C_2^2$ ゆえ **$C_2$ 共通商がありうる** — 段 0 で分裂判定してから族を決める」。**警告は正しかったが、同じ行の数値がその警告を織り込んでいなかった。** ⟹ **警告と数値を同じ行に書くときは、数値側に警告を反映させること。**

### 3.7.2 ★ $N_{\rm ord}=20$ が W-5 の charming 会計($\mathcal X_N$)に与える影響

$\mathcal X_N$ は $N_{\rm ord}$ だけで決まる集合であり、$N_{\rm ord}$ の訂正は **charming 会計を丸ごと半分にする**。$N_{\rm ord}=20$ では $\mathcal X_{20}=\{0,1,3,4,5,6,8,9,10,11,13,14,15,16,18,19\}$(16 個・$\widetilde m\not\equiv2\bmod5$)であり、**§4.3 の T1 走査候補数の一般式**
$$\#\bigl\{\widetilde m\in\mathcal X_N:\widetilde m\equiv0\ (\mathrm{mod}\ 10)\bigr\}\ \times\ \bigl\lvert(K^{(5)}_{F_2}/N_{F_2})\cap[P_N,P_N]\bigr\rvert$$
の第 1 因子は $\{0,10\}$ の **2**($N_{\rm ord}=40$ なら $\{0,10,20,30\}$ の 4 だった)、第 2 因子は $\lvert W\rvert=\lvert V\cap[P_N,P_N]\rvert=\lvert V\rvert=\mathbf 2$($V\cong C_2$ が $[P_N,P_N]=A\times\{\pm1\}$ に含まれる)。ゆえに **T1 走査候補は $2\times2=\mathbf 4$**(誤値の下では 8 だった)、**全列挙 raw は $16\times250=\mathbf{4{,}000}$**(誤値の下では 8,000 だった)。⟹ **走査規模はどちらの tier でも半減し、W-5 は $K^{(20)}$($\mathcal X_{20}$・T1 = 4)と完全に同じ charming 宇宙・同じ T1 規模の窓になる** — 両者を並走させれば tier 間突合(P-K5-10)の材料が 1 件増える一方、**同じ $N_{\rm ord}$・同じ $\mathcal X_N$ をもつ別窓が 2 つ在庫に並ぶことになるので、cert の窓ラベル取り違えを CV-9 事項として先に塞ぐこと**。なお第 1 因子が $\ge2$ である以上、W-5 は札 1-E【NORD10】の「$\widetilde m$ 項が 1 本」条件を満たさず、$\widetilde m=0$ の不可解から $d_N=1$ を結論することは**できない**窓である(もっとも $\widetilde m=0$ で既に witness が在るので実害はない)。

**検算**: `scratchpad/w5_charming_check.py`(整数 6 行・Python)。$N_{\rm ord}\in\{10,20,30,40,50\}$ で $\lvert\mathcal X_N\rvert=8,16,16,32,40$、$\#\{\widetilde m\equiv0(10)\}=1,2,2,4,5$。**$N_{\rm ord}=30$ の $(16,2)$ は §4.3 の W-4 行($16\cdot375$ / T1 $=2\times3=6$)と、$N_{\rm ord}=50$ の $(40,5)$ は W-2 行($40\cdot15625$ / T1 $=5\times125=625$)と一致する** ⟹ **式と実装の突合が既存 2 行で取れている。**

### 【収載原稿ここまで】

---

## 6. FINDING

| # | 格 | 内容 |
|---|---|---|
| **R-1** | ★★ **新規の否定定理候補(1-A の厳密化)** | **命題 ROOF-KILL**(§1.2): $N=K^{(5)}\cap N'$ で (b) $f_1\mapsto1$ in $D$(とくに $5\nmid\lvert D\rvert$)+ (d) $V\subseteq[P_N,P_N]$ + (e) $V$ 中心 ⟹ **成分合成 witness $(f_1,1)$ が (N$_\theta$)(N$_\tau$)(SURJ) を全部満たす** ⟹ $d_N=5$。**5 段すべて証明つき。** 発案の「屋根は死ぬ」は前件 (d) 抜きでは偽 — **$K^{(20)}$ が実物の反例** |
| **R-2** | ★★ **新規の否定定理候補(1-C+1-D の合流)** | **命題 THETA-KILL**(§3.4): (V-ab)+(V-der)+$V$ 中心 ⟹ canonical 代表 $\bar w=\overline{x^2y^{-2}}$ で **$\beta_\theta=0$ が恒等的に取れる**;さらに $\dim_{\mathbf F_2}V=1$ なら **$d_N=5$**。⟹ **2-primary 標的の最下段($\lvert PB_3/N\rvert=500\cdot2$)は死ぬ** |
| **R-3** | ★★ **3 札が 1 点に収束する** | 1-A の前件 (d)・1-C の $W=V$・1-D の $\bar w\in[P_N,P_N]$ は**すべて前件 (V-der) と同値ないし同値に近い**(§3.3 で (V-der) $\Rightarrow$ $P_N^{\rm ab}=C_2^2$ $\Rightarrow$ $\bar w\in[P_N,P_N]$ を証明)。⟹ **(V-der) が W-6 探索の実効的な分岐点である**。prereg §2.6 が $K^{(20)}$ で見つけた「前件の破れ」は、**むしろ生存の必要条件だった** |
| **R-4** | ★★ **付録 A は全段成立**(条件 1 件つき) | $\lvert PB_3/N\rvert=1000$・$V\cong C_2$ 中心・**非分裂**(4 行の直接証明・§4.2 (b))・Arf 類の同定(§4.3)・$V\subseteq[P,P]$・witness $(f_1,+1)=\bar w$・SURJ 自動 ⟹ **$d_{W\text{-}5}=5$**。⚠ **isolated 性は未確認**(【W5-GAP-1】) |
| **R-5** ★ | ★★ **ENT-1 との整合 = 無矛盾(切り分け成立)** | ENT-1 は **$n=3$・$p=3$ 核・$[B_3:N']=1944$**、W-5 は **$n=5$・$p=2$ 核・$[B_3:N]=6000$**。**3 軸すべてで走査域の外**。加えて NO-ENT(3) は「他の $n$ へ広げない」と登録済で、1944 走査は既に較正へ降格。機構的にも整合(NO-CENTRAL は $p=5$ の話・$H^2(G_5,\mathbf F_2)\ne0$)。⟹ **どちらも誤りではない** |
| **R-6** | ★ **w6 §3.4 順位 1 の供給側予測が的中した** | 「2-primary なら $H^2(G_5,V)\ne0$ で非分裂拡大の供給が期待できる」— **W-5 が初の実物**。⚠ **ただし検出力の側では R-2 で死ぬ** ⟹ **供給の的中を検出力の証拠と読まないこと**(S-W6-3 型の事故防止) |
| **R-7** | ⚠ **novelty の型** | 「entangled 実在庫」単体は**新規でない**($K^{(9)}/K^{(3)}$・$K^{(25)}/K^{(5)}$)。新規なのは「**entangled *屋根* の実在庫**」。記帳語を 1 語落とすと novelty grep 違反(§4.4) |
| **R-8** | ★ **1-C の「紙決定」の格** | transgression が拡大類で**決まる**のは正しい。**自明作用なら UCT で明示的**($H^2(G,V)\to\operatorname{Hom}(H_2(G),V)$)。**一般の作用では「決まるが閉じた式ではない」**に弱まる(§2.1) |
| **R-9** | ★ **札 2-B の篩の修正** | 「$\overline{W_\tau}=1$ なら棄却」は**棄却条件の過小評価**。正しくは「$\overline{W_\tau}\in N_\tau(\ker N_\theta\vert_W)$ なら棄却」(§3.5)。$\dim W=1$・$p=2$ では **$\overline{W_\tau}$ の値によらず棄却**される |
| **R-10** | ★ **erratum の副産物** | $N_{\rm ord}=20$ の訂正で W-5 の charming 宇宙は **$K^{(20)}$ と完全一致**($\mathcal X_{20}$・T1 = 4)。⟹ **同じ $N_{\rm ord}$ の別窓が 2 つ並ぶ** ⟹ cert の窓ラベル取り違えを **CV-9 事項として先に塞ぐ**(§5) |

---

## 7. 未閉鎖・申告

### 7.1 本稿が**主張しないこと**

1. 「W-6 が空である」— **主張しない**。本稿が閉じたのは **(V-der) を満たす $\dim W\le1$ の帯**だけである。
2. 「屋根型がすべて死ぬ」— **主張しない**(§1.3 の $K^{(20)}$ が前件破れの実物)。
3. 「$d_{\rm gen}(5)$ について何か言える」— **言わない**。本稿の結論はすべて「検出力ゼロ」の上界側である(campaign §7.2 の非対称は不変)。
4. `cross-checked` — **付さない**(§4 の再証明は紙単系統。裁定 473 の GAP 実測とは**別系統だが、CV-9 判読を経ていない**)。
5. `verified` — **付さない**(Lean 未使用)。
6. 「W-5 は本命窓である」— **主張しない**。W-5 は **control**(第 4 の死因型の実物教材)である。

### 7.2 私が読んでいない/確認していないもの

| # | 項目 | リスク |
|---|---|---|
| **U-1** ★ | **$N=K^{(5)}\cap N_Q$ の isolated 性** | 【W5-GAP-1】。$d_{W\text{-}5}=5$ はこの前件つきの結論 |
| **U-2** | `search/week3-battery-common.g` の `MakeQ8()` の**実装本体** | 【W5-GAP-2】。$N_Q$ の生成規約の同一性は申告に依拠(CV-9 非当事者判読 未) |
| **U-3** | w6 §2.2 **補題 TWIST**(非可換下位項)と【K5-GAP-W1】($\theta_\ast^2=\mathrm{id}$・$\tau_\ast^3=\mathrm{id}$) | 本稿の命題は**すべて $V$(または $W$)が中心という強い前件の下**で書いた。中心でない核へは射程が伸びない |
| **U-4** | `k5_w6_construction_v1.md` の §5.3 以降(**369 行目以降**) | 発注仕様・検算 A〜F は読んでいない。§0〜§5.2 のみ読了 |
| **U-5** | ideas_020 の札 1-B / 1-E / 2-A〜2-E / 3-A〜3-D / 4-A〜4-D | **検分対象外**(委嘱は 1-A / 1-C / 1-D / 付録 A の 4 点)。§1.4 と §3.5 で 1-B・2-B に触れたのは**提案**であり判定ではない |

### 7.3 司令塔への 3 行

1. ★★ **付録 A は通る。ENT-1 とは無矛盾**(3 軸で走査域の外・§4.5)。⟹ **裁定 472 の「整合検分が必要」は本稿で閉じる。**
2. ★★ **1-A / 1-C / 1-D は 2 本の否定定理候補(ROOF-KILL / THETA-KILL)に収束した**(§1.2・§3.4)。**Sol 監査に出す価値がある** — とくに THETA-KILL は **2-primary 帯の最下段を紙で殺す**ので、w6 §3.4 の優先度表に直接効く。
3. ⚠ **【W5-GAP-1】(isolated)を先に閉じること。** 閉じるまで $d_{W\text{-}5}=5$ は条件つき結論であり、erratum の「予言 $d_N$」欄もその旨を明記した(§5)。
