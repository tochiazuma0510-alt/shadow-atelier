# W-6 の否定定理 2 本 — **ROOF-KILL** と **THETA-KILL**(起草 v1)

**状態札: `candidate / paper-proof / 紙 + 整数検算(python 単系統)/ Sol 未監査 / Lean 検証ではない / 実測ゼロ / 封印 3 量非接触・Im R 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設 v1**
- 委嘱: 司令塔 —「**定理 ROOF-KILL**(屋根型細分は成分合成 witness で検出力ゼロ)と**定理 THETA-KILL**(θ-ノルム消滅による 2-primary 最下段 $\lvert PB_3/N\rvert=500\cdot2$ の紙上死)を、証明つき candidate として起草。前件 (V-der) の扱いを両定理で明示。系として『W-6 生存に必要な条件の絞り込み』を 1 節」
- **入力正本**:
  - `docs/notes/ideas_020_review_v1.md`(本稿の**直接の前身**。§1.2 命題 ROOF-KILL / §3.4 命題 THETA-KILL / §3.3 の前件 (V-der))
  - `docs/notes/k5_w6_construction_v1.md`(SHA-256 `a363b87f39026da63662f862344a33095431c13555619a921ae49f54e7dbe5d9`)§1.2 命題 K5-BIT・§1.3 補題 GAMMA・§2.1 前件 (V-ab)(V-der)(V-cen)・§2.3 定理 W6-OBS・§4.2 補題 SURJ-W6・§5.2 停止規則 S-W6-x
  - `docs/notes/k5_w6_construction_v1_addendum_b_k20paper.md`(SHA-256 `21cd745c2e49d7287f91ad110ed89ffd41224bab8249ff53dd7eb0d394556b97`)§2.1 $A_m=\langle r^2\rangle^3$・§2.2 $V=\langle r^{10}\rangle^3$・§2.3 (4.7)(4.8) の逐語成立と $p=2$ での符号消失
  - `docs/notes/k5_dn_prereg_k20_draft_v1.md` **§2.6**(**(V-der) 破れ**の実測・$W:=V\cap[P_N,P_N]$・$\lvert[G_{20},G_{20}]\rvert=250$・**P-K20-4 = 障害類 0**)・§1.3 補題 K20-LIFT(witness $(\widetilde m,\widetilde k)=(0,6)$)
  - `docs/notes/ideas_020_w6_target.md` 札 1-A / 1-C / 1-D(発案・candidate)
  - 正典 arXiv **2405.11725 (4.7)(4.8)**・Prop 3.1 / 3.5・Thm 4.3
- **外部文献ゼロ。**【文献要請】は本稿では**発しない**(§7.4)。

> ## 非接触の申告
> - **$\mathrm{Im}\,R_{N,K^{(5)}}$ を一度も測っていない。** 本稿は紙 + 自由群の語簡約 + $(\mathbf Z/10)^3$ の整数演算のみ。
> - **封印 3 量非接触**($\hat c_\mu$ / PSL 窓の構造量 / ε bits)。**$u$ 値・曲線・dessin・Kummer に一切触れていない。**
> - **証明書を 1 本も読んでいない。** 使った $n=5$ の情報は $G_5$ の構造($\lvert G_5\rvert=500$・$A\cong C_5^3$・$G_5^{\rm ab}\cong C_2^2$)、正典 (4.7)(4.8)、$f_1=(r^2,r^{-2},1)$ の座標(裁定 396/398 で封印解除済)だけである。
> - **新規の群計算は発注していない。** 本稿の唯一の機械実行は §8 の整数/語検算(`scratchpad/w6_kill_check.py`)であり、GAP を一度も呼んでいない。

---

## 0. 判定(先に 8 行)

| # | 内容 | 判定 |
|---|---|---|
| **①** | **定理 ROOF-KILL** | ★★ **成立(candidate・全段証明つき)**。前身の命題(review §1.2)から前件 (d) を**削除**し、**鋭い不変量 $\delta_{\rm roof}\in V/W$** に置き換えた。(V-der) は $\delta_{\rm roof}=0$ の**十分条件にすぎない** |
| **②** | **定理 THETA-KILL** | ★★★ **成立(candidate)・かつ前身より大幅に強い**。前身(review §3.4)は (V-der)+中心+$\dim V=1$ を要したが、本稿は **$\bar w'\in[P_N,P_N]$ のみ**((V-cen) は SURJ 用)。核の標数・次元・中心性への仮定は**ノルム方程式には不要** |
| **③** ★★★ | **機構の同定** | $w=x^2y^{-2}$ の θ-ノルムが恒等的に消えるのは、$w=u^{-1}\theta(u)$($u=x^{-2}$)= **θ-余輪体**だからである(補題 COBDY)。同じ $u$ の **τ-余輪体** $w':=\tau(u)u^{-1}=y^{-2}x^2$ は $\psi_5(w')=f_1$ を保ったまま **2 本のノルムを両方とも $F_2$ で恒等的に消す** |
| **④** ★★ | **委嘱の標的(2-primary 最下段)** | ★★ **無条件で死ぬ**(系 THETA-1000)。$\lvert PB_3/N\rvert=500\cdot2$ なら $\lvert V\rvert\le2$ で、(V-der) が成立しても破れても**どちらの分岐でも** $d_N=5$。**前件ゼロの否定定理**である |
| **⑤** ★★ | **$K^{(20)}$ は ROOF-KILL の反例ではない**(★ **review §1.3 の訂正**) | review は「$K^{(20)}$ は (V-der) 破れゆえ射程外」と書いたが、鋭い形では**射程内**である。**$\delta_{\rm roof}(K^{(20)})=0$ を紙で確認し、$\widetilde m=0$ の witness を座標で明示した: $(f_1,1)=(6,4,0)\in(\mathbf Z/10)^3$**(§8 B8–B12)。これは prereg §1.3 の witness $(0,6)$ と独立に整合する |
| **⑥** ★★ | **(V-der) の役割が反転した** | (V-der) は**死因の十分条件**であり、**その破れは生存の必要条件**である。しかも必要条件は完全に明示的: $$\boxed{\ \textbf{生存}\Longrightarrow x^2y^{-2}\notin N_{F_2}\cdot[F_2,F_2]\iff (2,-2)\notin\alpha(N_{F_2})\subseteq\mathbf Z^2\ }$$(§5.2)。**アーベル化 1 本で判定できる最安の篩**である |
| **⑦** ★ | **第 5・第 6 の死因型** | **$W=V\cap[P_N,P_N]=0$ 型**(持上げが一意でノルムが強制的に消える・§3.5)と **$W^\tau=0$ 型**($\beta_\tau$ が強制的に消える・§5.1 KT-5)を新設。既存 3 型 + 屋根合成型 + 本 2 型で **6 型**になった |
| **⑧** | ⚠ **買わないもの** | 本稿は $d_{\rm gen}(5)$ について何も言わない。すべて「検出力ゼロ」の**上界側**である(campaign §7.2 の非対称は不変)。W-6 の**存在**についても何も言わない |

> ### ★ 一行で
> $$\boxed{\ \textbf{2 本のノルム方程式は }\widetilde m=0\textbf{ で「}\overline{y^{-2}x^2}\in[P_N,P_N]\textbf{ か」の 1 個のアーベル化条件に収縮する。}\ }$$
> $$\boxed{\ \textbf{したがって W-6 は }\ (2,-2)\notin\alpha(N_{F_2})\ \textbf{ かつ }\ V\cap[P_N,P_N]\ne0\ \textbf{ かつ 屋根でない、の帯にしか存在し得ない。}\ }$$

---

## 1. 設定(**再定義しない・出所つき**)

campaign §1.3 / w6 §1.1 の記号をそのまま用いる。

$PB_3\cong F_2\times\langle c\rangle$、$F_2=\langle x,y\rangle$、$z:=(xy)^{-1}$。正典 (3.1) の $\psi_m:PB_3\to D_m^3$、$K^{(m)}=\ker\psi_m$、$G_5=PB_3/K^{(5)}$($\lvert G_5\rvert=500$)、$A=[G_5,G_5]\cong C_5^3$、$G_5^{\rm ab}\cong C_2^2$、$X=\psi_5(x)$、$Y=\psi_5(y)$。$A$ の基底 $(X^2,Y^2,(XY)^{-2})$ と座標 $(n_1,n_2,n_3)$(addendum B §2.1)。$f_1=(r^2,r^{-2},1)=X^2Y^{-2}$、座標 $(1,-1,0)$。$\phi_1=[0,f_1]$ が $\mathfrak F_0\cong C_5$ を生成。

$\Gamma=\langle\theta,\tau\rangle\subseteq\mathrm{Aut}(F_2)$、$\theta:x\mapsto y,\ y\mapsto x$;$\tau:x\mapsto y\mapsto z\mapsto x$。$\theta^2=\tau^3=\mathrm{id}$ **on $F_2$**(§8 A0/A1 で機械確認)。正典 (4.7)(4.8):

$$\theta(n_1,n_2,n_3)=(n_2,n_1,-n_3),\qquad \tau(n_1,n_2,n_3)=(n_3,n_1,n_2).$$

### 1.1 窓と測る量

$N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、**$c\in N$**、$N$ **isolated**。$P:=P_N=F_2/N_{F_2}$($c\in N$ ゆえ $P\cong PB_3/N$)、$\pi:P\twoheadrightarrow G_5$、

$$V:=\ker\pi=K^{(5)}_{F_2}/N_{F_2}\ \trianglelefteq\ P,\qquad \boxed{\ W:=V\cap[P,P]\ }$$

**命題 K5-BIT**(campaign §2.3・便 100 で Sol PASS)の $\widetilde m=0$ の項:

$$\textbf{(N}_\theta\textbf{)}\ \widetilde f\,\theta(\widetilde f)=1,\quad
\textbf{(N}_\tau\textbf{)}\ \tau^2(\widetilde f)\,\tau(\widetilde f)\,\widetilde f=1,\quad
\textbf{(SURJ)}\ \langle\bar x,\widetilde f^{-1}\bar y\widetilde f\rangle=P,\qquad \widetilde f\in[P,P],\ \pi(\widetilde f)=f_1 .$$

$$\boxed{\ \textbf{3 本が }\widetilde m=0\textbf{ で可解}\ \Longrightarrow\ \phi_1\in\mathrm{Im}\,R_{N,K^{(5)}}\ \Longrightarrow\ d_N=5\ (\textbf{検出力ゼロ})\ }$$

**逆は言えない**(w6 §1.2・危険箇所 D-3)。本稿の結論はすべてこの向きだけを使う。

### 1.2 前件の名前(w6 §2.1 と同じ・**混同を防ぐため再掲**)

| 名 | 内容 | 本稿での位置 |
|---|---|---|
| **(V-ab)** | $V$ がアーベル | THETA-KILL では**不要**、ROOF-KILL では**不要**(§3/§4 で使わない) |
| **(V-der)** | $V\subseteq[P,P]$、すなわち $W=V$ | ★ **どちらの定理でも「十分条件」であって前件ではない**(§3.4・§4.5) |
| **(V-cen)** | $V\subseteq Z(P)$ | ★ **(SURJ) のためだけに使う**(補題 SURJ-CENT)。ノルム方程式には不要 |

> ⚠ **委嘱文の「前件 (V-der)(障害加群 $=V\cap[P_N,P_N]$)」は 2 つの別物を 1 語で呼んでいる。** 本稿は厳密に分ける: **(V-der) は仮定 $V\subseteq[P,P]$**、**$W=V\cap[P,P]$ は障害の載る加群**、そして **(V-der) $\iff W=V$**。

---

## 2. 共通の基盤 — 障害は $V$ ではなく $W$ に載る

### 2.1 補題 W-TORSOR(**prereg §2.6 の同定を一般形に昇格**)

> ### 補題 W-TORSOR(candidate)
> 上の設定で $\mathcal L:=\pi^{-1}(f_1)\cap[P,P]$ と置く。
> **(a)** $\mathcal L\ne\emptyset$ であり、$\mathcal L$ は右からの $W$-作用について**単純推移的**($W$-torsor)。とくに $\lvert\mathcal L\rvert=\lvert W\rvert$。
> **(b)** 任意の $\widetilde f_0\in\mathcal L$ に対し
> $$\beta_\theta:=\widetilde f_0\,\theta(\widetilde f_0)\in W,\qquad \beta_\tau:=\tau^2(\widetilde f_0)\tau(\widetilde f_0)\widetilde f_0\in W .$$
> **(c)** さらに $W\subseteq Z(P)$ ならば $\theta(\beta_\theta)=\beta_\theta$、$\tau(\beta_\tau)=\beta_\tau$、すなわち $\beta_\theta\in W^\theta$、$\beta_\tau\in W^\tau$。
> **(d)** $W\subseteq Z(P)$ かつ $W$ がアーベルならば、$\widetilde f_0\mapsto\widetilde f_0 b$($b\in W$)は $(\beta_\theta,\beta_\tau)\mapsto(\beta_\theta+N_\theta b,\ \beta_\tau+N_\tau b)$ を与え、
> $$\boxed{\ \textbf{(N}_\theta\textbf{)(N}_\tau\textbf{) が }\widetilde m=0\textbf{ で可解}\iff [(-\beta_\theta,-\beta_\tau)]=0\ \text{in}\ \operatorname{coker}\psi_W\ },\qquad \psi_W=(N_\theta,N_\tau):W\to W^\theta\oplus W^\tau .$$

**証明.**
**(a)** 全射準同型 $\pi$ は交換子群を交換子群の**上へ**写すので $\pi([P,P])=[G_5,G_5]=A\ni f_1$、ゆえに $\mathcal L\ne\emptyset$。$\widetilde f_0,\widetilde f_1\in\mathcal L$ なら $\widetilde f_0^{-1}\widetilde f_1\in\ker\pi\cap[P,P]=V\cap[P,P]=W$。逆に $b\in W$ なら $\widetilde f_0b\in[P,P]$ かつ $\pi(\widetilde f_0b)=f_1$。∎
**(b)** $\pi(\beta_\theta)=f_1\theta(f_1)$。$f_1$ の座標 $(1,-1,0)$ に (4.7) を当てて $\theta(f_1)=(-1,1,0)$、和 $=(0,0,0)$ ⟹ $\pi(\beta_\theta)=1$ ⟹ $\beta_\theta\in V$。他方 $\theta$ は $P$ の自己同型ゆえ $[P,P]$ を保ち、$\widetilde f_0,\theta(\widetilde f_0)\in[P,P]$ ⟹ $\beta_\theta\in[P,P]$。よって $\beta_\theta\in V\cap[P,P]=W$。$\tau$ 側も同様((4.8) で $f_1+\tau f_1+\tau^2f_1=(1,-1,0)+(0,1,-1)+(-1,0,1)=(0,0,0)$)。∎
**(c)** $\theta(\beta_\theta)=\theta(\widetilde f_0)\theta^2(\widetilde f_0)=\theta(\widetilde f_0)\widetilde f_0=\widetilde f_0^{-1}\beta_\theta\widetilde f_0=\beta_\theta$(最後に $\beta_\theta\in W\subseteq Z(P)$)。$u_i:=\tau^i(\widetilde f_0)$ と置けば $\beta_\tau=u_2u_1u_0$、$\tau^3=\mathrm{id}$ より $\tau(\beta_\tau)=u_0u_2u_1=u_0\beta_\tau u_0^{-1}=\beta_\tau$。∎
**(d)** $b\in W\subseteq Z(P)$ ゆえ $(\widetilde f_0b)\theta(\widetilde f_0b)=\widetilde f_0\theta(\widetilde f_0)\cdot b\,\theta(b)$、$\tau$ 側も同様。あとは w6 §2.1 と同じ剰余類の議論。∎

> ### ★ これが w6 §2.1 のどこを直したか
> w6 §2.1 は補正の自由度を **$V$ 全体**に取り、障害を $\operatorname{coker}\psi_V$ と書いた。**K5-BIT が要求するのは $\widetilde f\in[P,P]$** なので、自由度は **$W$ に限られる**。prereg §2.6 が $K^{(20)}$ の実測で捕まえたこの食い違いを、本補題は**一般形の証明**にした。⟹ **篩 W6-F3 は $V$ ではなく $W$ で評価する**(review §2.4 の提案を定理側から確定)。
> ⚠ **campaign §4.3 の T1 一般式は最初から $\cap[P_N,P_N]$ を含んでいた**(prereg §2.6 の傍証)。**食い違っていたのは w6 §2.1 の側だけ**である。

### 2.2 補題 SURJ-CENT(**補題 SURJ-W6 の全面強化**)

> ### 補題 SURJ-CENT(candidate)
> **(V-cen)**($V\subseteq Z(P)$)を仮定する。このとき $\pi(\widetilde f)=f_1$ なる**任意**の $\widetilde f\in P$ に対して (SURJ) が成り立つ:
> $$\langle\bar x,\ \widetilde f^{-1}\bar y\widetilde f\rangle=P .$$
> $$\Longrightarrow\ \boxed{\ \textbf{(V-cen) を満たす窓では (SURJ) の識別力はゼロである}\ }$$

**証明.** $H:=\langle\bar x,\widetilde f^{-1}\bar y\widetilde f\rangle$ と置く。$\phi_1$ が level 5 で (SURJ) を満たす(= $\phi_1\in\mathrm{GT}(K^{(5)})$)ので $\pi(H)=G_5$、すなわち $HV=P$。$V$ が中心ゆえ $V$ は $H$ を正規化し、$H$ は自身を正規化するので $H$ は $\langle H,V\rangle=HV=P$ で正規化される ⟹ $H\trianglelefteq P$。よって $P/H=HV/H\cong V/(V\cap H)$ はアーベル ⟹ $[P,P]\subseteq H$。したがって $H$ を法として $\widetilde f^{-1}\bar y\widetilde f\equiv\bar y$、ゆえに $\bar y\in H$。$\bar x\in H$ と合わせ $H\supseteq\langle\bar x,\bar y\rangle=P$。∎

> ### ★ 補題 SURJ-W6(w6 §4.2)との差
> | | 補題 SURJ-W6 | ★ 補題 SURJ-CENT(本稿) |
> |---|---|---|
> | 前件 | $V\subseteq\Phi(P)$(さらにその十分条件として「$V$ 既約 + 非分裂」) | **$V$ 中心のみ** |
> | 経路 | Frattini 論法 | $[P,P]\subseteq H$ + $P=\langle\bar x,\bar y\rangle$ |
> | 射程 | 既約・非分裂の窓 | ★ **中心核の窓すべて**(可約でも分裂でも可) |
>
> ⟹ **$V\subseteq\Phi(P)$ の検査は不要になった。** w6 §4.4 の篩 **W6-F4** および §5.3 発注仕様の「段 0 で `V ⊆ Φ(P_N)` を assert」は、**(V-cen) の assert に置き換えられる**(より安く、より広い)。
> ⚠ **(V-cen) が破れる窓では本補題は使えない** — その場合のみ (SURJ) の検査が意味を持つ。

---

## 3. 定理 THETA-KILL

### 3.1 ★★★ 補題 COBDY(**機構の同定** — なぜ θ-ノルムが消えるのか)

発案 1-D は「$w=x^2y^{-2}$ で $w\theta(w)=1$ が $F_2$ で恒等」という**観察**を出した。その**理由**は次である。

> ### 補題 COBDY(candidate)
> 任意の群 $G$ と、位数 2 の自己同型 $\theta$、位数 3 の自己同型 $\tau$ に対し、$N_\theta(a):=a\,\theta(a)$、$N_\tau(a):=\tau^2(a)\tau(a)a$ と置く。任意の $u\in G$ について
> $$\boxed{\ N_\theta\bigl(u^{-1}\theta(u)\bigr)=1,\qquad N_\tau\bigl(\tau(u)\,u^{-1}\bigr)=1\ }$$
> がそれぞれ**恒等的に**成り立つ(非可換でよい)。

**証明.** $N_\theta(u^{-1}\theta(u))=u^{-1}\theta(u)\cdot\theta(u^{-1}\theta(u))=u^{-1}\theta(u)\cdot\theta(u)^{-1}\theta^2(u)=u^{-1}u=1$。
$a:=\tau(u)u^{-1}$ と置くと $\tau^2(a)=\tau^3(u)\tau^2(u)^{-1}=u\,\tau^2(u)^{-1}$、$\tau(a)=\tau^2(u)\tau(u)^{-1}$、よって
$N_\tau(a)=u\tau^2(u)^{-1}\cdot\tau^2(u)\tau(u)^{-1}\cdot\tau(u)u^{-1}=u\,u^{-1}=1$。∎

> ★ **これで 1-D の「なぜ」が閉じた**: $w=x^2y^{-2}=u^{-1}\theta(u)$ with $u=x^{-2}$(§8 A9)。**$w$ は θ-余輪体だから θ-ノルムが消える。**

### 3.2 ★★★ 系 COBDY-$w'$(**同じ $u$ から τ 側も同時に消せる**)

$u:=x^{-2}$ に補題 COBDY の**第 2 式**を当てると

$$\boxed{\ w':=\tau(u)\,u^{-1}=\tau(x^{-2})\,x^{2}=y^{-2}x^{2}\ }$$

であり、$N_\tau(w')=1$ が $F_2$ で恒等。さらに $w'=(y^{2})^{-1}\theta(y^{2})$ でもある(§8 A11)から、**同じ第 1 式**により $N_\theta(w')=1$ も $F_2$ で恒等。すなわち

$$\boxed{\ w'=y^{-2}x^{2}\ \textbf{は }F_2\textbf{ において }\ w'\,\theta(w')=1\ \textbf{かつ}\ \tau^2(w')\tau(w')w'=1\ \textbf{を同時に満たす}\ }$$

**直接検算**(§8 A5/A6 で機械確認・ここでは紙):
$\theta(w')=x^{-2}y^{2}$ ⟹ $w'\theta(w')=y^{-2}x^2x^{-2}y^2=1$。
$\tau(w')=z^{-2}y^{2}$、$\tau^2(w')=x^{-2}z^{2}$ ⟹ $\tau^2(w')\tau(w')w'=x^{-2}z^2\cdot z^{-2}y^2\cdot y^{-2}x^2=x^{-2}x^2=1$。

**かつ $\psi_5(w')=f_1$**: $A$ はアーベルゆえ $\psi_5(w')=Y^{-2}X^2=X^2Y^{-2}=f_1$(addendum B §2.1 の基底で $a_1-a_2=(1,-1,0)$)。

> ⚠ $w$ と $w'$ は $F_2$ で共役($w'=y^{-2}wy^{2}$・§8 A12)であるが、**ノルムは共役不変ではない**: $N_\tau(w)\ne1$(§8 A4)、$N_\tau(w')=1$。**共役の取り方 1 つで τ-障害が消える**、というのが本系の内容である。

### 3.3 ★★★ 定理 THETA-KILL

> ### 定理 THETA-KILL(candidate)
> $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$c\in N$、$N$ isolated。$P=P_N$、$V=\ker(P\to G_5)$、$W=V\cap[P,P]$、$w'=y^{-2}x^2$ とする。
>
> **(I)【余輪体 witness】** $\overline{w'}\in[P,P]$ ならば、$\widetilde f:=\overline{w'}$ は $\widetilde m=0$ の **(N$_\theta$)(N$_\tau$) を両方満たす**。$V$ や $W$ の標数・次元・可換性・中心性への仮定は**一切不要**。
> **(II)【判定式】**
> $$\overline{w'}\in[P,P]\iff \overline{w}\in[P,P]\iff 2(\bar x-\bar y)=0\ \text{in}\ P^{\rm ab}\iff x^2y^{-2}\in N_{F_2}\cdot[F_2,F_2]\iff (2,-2)\in\alpha(N_{F_2})$$
> ($\alpha:F_2\to F_2^{\rm ab}=\mathbf Z^2$ はアーベル化)。
> **(III)【$W=0$ 分岐】** $W=0$ ならば $\mathcal L$ は 1 点 $\{\widetilde f_0\}$ で、$\beta_\theta=\beta_\tau=1$(補題 W-TORSOR (b))⟹ $\widetilde f_0$ が **(N$_\theta$)(N$_\tau$) を両方満たす**。
> **(IV)【結論】** (I) または (III) が成り立ち、かつ **(V-cen)** が成り立てば、補題 SURJ-CENT により (SURJ) も自動で、
> $$\boxed{\ \phi_1\in\mathrm{Im}\,R_{N,K^{(5)}},\qquad d_N=5,\qquad \textbf{検出力ゼロ}\ }$$

**証明.**
**(I)** $\pi(\overline{w'})=\psi_5(w')=f_1$(§3.2)。$\overline{w'}\in[P,P]$ は仮定。2 本のノルムは $F_2$ の恒等式(§3.2)の像だから $P$ で成立。∎
**(II)** $w=x^2y^{-2}$ と $w'=y^{-2}x^2$ は共役ゆえ $P^{\rm ab}$ で同じ像をもち、$[P,P]$ への所属は同値。$P^{\rm ab}=F_2/(N_{F_2}[F_2,F_2])=\mathbf Z^2/\alpha(N_{F_2})$ であり、$\alpha(w)=(2,-2)=2(\bar x-\bar y)$。∎
**(III)** 補題 W-TORSOR (a)(b)。(b) は $W$ の可換性も中心性も使っていない。∎
**(IV)** 命題 K5-BIT($\widetilde m=0$ の項)+ 補題 SURJ-CENT。∎

> ### ★ 前身(review §3.4 命題 THETA-KILL)との差分(**明示**)
> | 項目 | review §3.4 | ★ 本稿 定理 THETA-KILL |
> |---|---|---|
> | 代表語 | $w=x^2y^{-2}$($\beta_\theta=0$ **のみ**) | ★ $w'=y^{-2}x^2$(**$\beta_\theta=\beta_\tau=0$ の両方**) |
> | 前件 | (V-ab) + **(V-der)** + $V$ 中心 + $\dim_{\mathbf F_2}V=1$ | ★ **$\overline{w'}\in[P,P]$ のみ**((V-cen) は SURJ 用) |
> | τ 側の扱い | 「$\dim V=1$ なら $N_\tau=\mathrm{id}$ が全射ゆえ解ける」= **次元に依存する議論** | ★ **恒等式**。次元にも標数にも依存しない |
> | (V-der) | **前件** | ★ **十分条件**((II) の最右辺が (V-der) から従う・§3.4) |
> | $W=0$ の場合 | 扱っていない | ★ **(III) で別分岐として閉じる** |

### 3.4 (V-der) はどこで効くか(**委嘱の必須項目**)

> ### 補題 DER-SUF
> **(V-der)**($V\subseteq[P,P]$、すなわち $W=V$)ならば $P^{\rm ab}\cong G_5^{\rm ab}\cong C_2^2$、とくに $2\xi=0$($\forall\xi\in P^{\rm ab}$)、ゆえに $\overline{w'}\in[P,P]$。

**証明.** $\ker(P^{\rm ab}\to G_5^{\rm ab})=V[P,P]/[P,P]\cong V/W$。(V-der) で $V/W=0$ ⟹ $P^{\rm ab}\cong G_5^{\rm ab}\cong C_2^2$。∎

$$\Longrightarrow\ \boxed{\ \textbf{(V-der)}\ \Longrightarrow\ \textbf{定理 THETA-KILL (I)}\ \Longrightarrow\ d_N=5\ }$$

**対偶(★ 本稿の実務上の主産物)**:

$$\boxed{\ \textbf{生存}\ \Longrightarrow\ \textbf{(V-der) は破れる}\ \Longrightarrow\ V/W\ne0\ }$$

さらに (II) は「破れ方」まで指定する: **$V/W\ne0$ だけでは足りず、$2(\bar x-\bar y)$ が $V/W\subseteq P^{\rm ab}$ の中で非零でなければならない**。$V/W\cong 2\mathbf Z^2/\alpha(N_{F_2})$ であり、$2(\bar x-\bar y)=(2,-2)$ の像がそこで非零、という**格子 1 個の条件**である。

### 3.5 ★★ 系 THETA-1000(**委嘱の標的 — 2-primary 最下段の紙上死**)

> ### 系 THETA-1000(candidate)
> $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$N$ isolated、$\lvert PB_3/N\rvert=500\cdot2=1000$ とする。このとき
> $$\boxed{\ d_N=5\ (\textbf{検出力ゼロ})\ }$$
> **前件は上の 3 つだけ**である(核の型・分裂性・作用については何も仮定しない)。

**証明.** $\lvert PB_3/N\rvert=\lvert G_5\rvert\cdot[K^{(5)}:N]$ ゆえ $[K^{(5)}:N]=2$。

*場合 1: $c\in N$.* $P=PB_3/N$、$\lvert V\rvert=2$。$V\trianglelefteq P$ かつ $\lvert V\rvert=2$ ⟹ $V\subseteq Z(P)$(位数 2 の正規部分群は中心。$\mathrm{Aut}(C_2)=1$)⟹ **(V-cen) は自動**。$W=V\cap[P,P]$ は $V\cong C_2$ の部分群だから $W=V$ か $W=0$ の 2 択:
- $W=V$(= (V-der))⟹ 補題 DER-SUF ⟹ 定理 THETA-KILL (I)。
- $W=0$ ⟹ 定理 THETA-KILL (III)。

どちらでも (IV) が発火し $d_N=5$。

*場合 2: $c\notin N$.* $N_{F_2}=NK^{(5)}\cap\ldots$ ではなく、$c\in K^{(5)}$ かつ $[K^{(5)}:N]=2$ ゆえ $K^{(5)}=N\langle c\rangle$、したがって $K^{(5)}_{F_2}=N_{F_2}$、すなわち $V=1$。ゆえに $P\cong G_5$、$\widetilde f=f_1$ 自身が 3 本を満たす(level 5 の事実)。∎

> ⚠ **場合 2 には campaign §5.0 / w6 危険箇所 D-6 の注意($\theta,\tau$ を商の上で評価する近道は $c\in N$ に依存)がかかる**。本稿は $P\cong G_5$ という**同型**を使うので水準の食い違いは起きないが、K5-BIT を $c\notin N$ の窓へ適用する規約自体は **【W6K-GAP-1】**(§7.3)として開いたままにする。**場合 1 だけでも委嘱の標的は閉じる**(場合 2 は $\lvert V\rvert=1$ なので「2-primary 核をもつ窓」ではない)。

> ### ★ この系が何を消したか
> w6 §3.4 は 2-primary 標的の規模を「$\lvert PB_3/N\rvert=500\cdot2^k$、$k=2$ なら 2000」と見積り、**$k=1$(= 1000)を最下段として残していた**。本系はその段を**掘る前に空にした**。⟹ **2-primary 帯の実効的な下限は $\lvert PB_3/N\rvert\ge2000$($\lvert V\rvert\ge4$)である**(§5.3 でさらに絞る)。
> ⚠ ★ **これは「W-5($\lvert PB_3/N\rvert=1000$)は死ぬ」の一般化でもある**。review §4 は W-5 について $Q_8$ の Arf 類・非分裂性・$[P,P]=A\times\{\pm1\}$ を経由して死を出したが、**系 THETA-1000 はそれらを一切使わずに、位数だけから同じ結論を出す**。⟹ review §4 の W-5 解析は**独立な第 2 経路**による裏取りとして残る(§6.2)。

---

## 4. 定理 ROOF-KILL

### 4.1 設定

$N'\trianglelefteq B_3$、**$c\in N'$**、$N:=K^{(5)}\cap N'$(⟹ $c\in N$、$N\trianglelefteq B_3$、$N\subseteq K^{(5)}$)。

$$G':=PB_3/N',\qquad D:=PB_3/(K^{(5)}N'),\qquad P:=PB_3/N,\qquad V':=\ker(G'\to D)=\psi_{N'}(K^{(5)}).$$

### 4.2 ★★ 定理 ROOF-KILL

> ### 定理 ROOF-KILL(candidate・**第 4 の死因型**)
> **(a)【Goursat】** $P\cong G_5\times_D G'$(共通商 $D$ 上の fiber product)であり、$V=\ker(P\to G_5)\cong V'$。
> **(b)【繊維】** $f_1$ の $D$ における像が自明ならば $\pi^{-1}(f_1)=\{(f_1,v):v\in V'\}$、とくに $(f_1,1)\in P$。
> **十分条件: $5\nmid\lvert D\rvert$**($f_1\in A\cong C_5^3$ の位数は 5 の冪)。
> **(c)【成分合成 witness】** (b) の下で $\widetilde f:=(f_1,1)$ は $\widetilde m=0$ の **(N$_\theta$)(N$_\tau$) を両方満たす**。
> **(d)【所属の鋭い不変量】** $\widetilde f_0\in\mathcal L$ を任意に取り
> $$\delta_{\rm roof}(N):=\bigl[\ \widetilde f_0^{\,-1}\,(f_1,1)\ \bigr]\in V/W$$
> と置く($\widetilde f_0$ の取り方によらない — 取り替えは $W$ ぶんの差)。このとき
> $$(f_1,1)\in[P,P]\iff \delta_{\rm roof}(N)=0 .$$
> **(e)【計算式】** $u:=\psi_{N'}(x^2y^{-2})\in V'$ と置くと、(b) の下で
> $$\delta_{\rm roof}(N)=\bigl[\overline{w}\bigr]-\bigl[u\bigr]\in V/W\qquad(\text{両者とも }V[P,P]/[P,P]\cong V/W\text{ の元}).$$
> とくに **$x^2y^{-2}\in N'$(すなわち $u=1$)ならば $\delta_{\rm roof}=0\iff\overline{w}\in[P,P]$** であり、**ROOF-KILL と THETA-KILL は同一の witness に一致する**。
> **(f)【結論】** (b) + ($\delta_{\rm roof}=0$) + **(V-cen)** + $N$ isolated ならば
> $$\boxed{\ \phi_1\in\mathrm{Im}\,R_{N,K^{(5)}},\qquad d_N=5,\qquad \textbf{検出力ゼロ}\ }$$

**証明.**
**(a)** $N=K^{(5)}\cap N'$ ゆえ $P\to G_5\times G'$ は単射、両射影は全射。Goursat の補題により像は共通商 $D=PB_3/(K^{(5)}N')$ 上の fiber product。$\ker(P\to G_5)=K^{(5)}/N=K^{(5)}/(K^{(5)}\cap N')\cong K^{(5)}N'/N'=V'$。∎
**(b)** $(g,g')\in P\iff g,g'$ の $D$-像が一致。$f_1\mapsto1$ なら条件は $g'\in\ker(G'\to D)=V'$。$5\nmid\lvert D\rvert$ なら位数 5 の $f_1$ の像は自明。∎
**(c)** $K^{(5)},N'$ はともに $B_3$-正規ゆえ $\theta,\tau$ は両方を保ち、埋め込み $P\hookrightarrow G_5\times G'$ と両射影は $\Gamma$-同変。よって成分ごとに計算してよい。第 2 成分: $\theta(1)=\tau(1)=1$ ゆえ両ノルムとも 1。第 1 成分: 補題 W-TORSOR (b) の証明で計算したとおり $f_1\theta(f_1)=1$、$\tau^2(f_1)\tau(f_1)f_1=1$。∎
**(d)** $\mathcal L$ は $W$-torsor(補題 W-TORSOR (a))であり $\pi^{-1}(f_1)=\widetilde f_0V$。$(f_1,1)\in\pi^{-1}(f_1)$ ゆえ $(f_1,1)=\widetilde f_0v$ なる $v\in V$ が一意に存在し、$(f_1,1)\in[P,P]\iff v\in W$。$\widetilde f_0$ を $W$ ぶん動かしても $[v]\in V/W$ は不変。∎
**(e)** $\overline{w}\in P$ の 2 成分は $(\psi_5(w),\psi_{N'}(w))=(f_1,u)$。(b) より $u\in V'$、ゆえに $(1,u)\in V$ であり $(f_1,1)=\overline{w}\cdot(1,u)^{-1}$。両辺の $P^{\rm ab}$ での像を取れば主張。∎
**(f)** 命題 K5-BIT + 補題 SURJ-CENT。∎

### 4.3 ★★ 実物 — $K^{(20)}=K^{(5)}\cap K^{(4)}$ は ROOF-KILL の**射程内**である

> ### ★ review §1.3 の訂正
> `ideas_020_review_v1.md` §1.3 は「$K^{(20)}$ は前件 (d)($V\subseteq[P,P]$)が破れるので **ROOF-KILL の射程外**、ゆえに『屋根は死ぬ』は $K^{(20)}$ では言えない」と書いた。**鋭い形 (d) では射程内である。** 以下、紙で確認する。

$N'=K^{(4)}$、$G'=G_4$($\lvert G_4\rvert=4\cdot2^3=32$・addendum B §2.1 の公式 $\lvert G_m\rvert=4(m/2)^3$)、$\lvert D\rvert=500\cdot32/4000=4$ ⟹ **(b) 成立**($5\nmid4$)。

**座標**(addendum B §2.1–2.3): $A_{20}=\langle r^2\rangle^3\cong(\mathbf Z/10)^3$、$A_4\cong(\mathbf Z/2)^3$、還元は **mod 2**;$A_5\cong(\mathbf Z/5)^3$、還元は **mod 5**。$V=\langle r^{10}\rangle^3=\{5b:b\in\mathbf F_2^3\}$。

$$[G_{20},G_{20}]=I_QA_{20}+\langle[X,Y]\rangle=\{n\in(\mathbf Z/10)^3:\ n_1\equiv n_2\equiv n_3\ (\mathrm{mod}\ 2)\},\qquad \lvert[G_{20},G_{20}]\rvert=250$$

(review §1.3 の独立導出・prereg §2.6 の実測と一致。$[X,Y]=(-1,1,-1)$ を本稿でも直接再計算した — §8 B3)。ゆえに

$$W=V\cap[G_{20},G_{20}]=\langle(5,5,5)\rangle\cong\mathbf F_2,\qquad \lvert W\rvert=2,\qquad V/W\cong\mathbf F_2^2 .$$

**★ witness の明示**: $(f_1,1)$ は「mod 5 で $(1,-1,0)$、mod 2 で $(0,0,0)$」の元。CRT で

$$\boxed{\ (f_1,1)=(6,4,0)\in(\mathbf Z/10)^3\ }$$

- $\bmod\ 5$: $(1,4,0)=(1,-1,0)=f_1$ ✓(§8 B8)
- $\bmod\ 2$: $(0,0,0)$ ✓(§8 B9)
- **パリティが全部偶** ⟹ $(6,4,0)\in[G_{20},G_{20}]$ ⟹ $\boxed{\delta_{\rm roof}(K^{(20)})=0}$ ✓(§8 B10)
- $\theta$-ノルム: $(6,4,0)+(4,6,0)=(10,10,0)=(0,0,0)$ ✓(§8 B11)
- $\tau$-ノルム: $(6,4,0)+(0,6,4)+(4,0,6)=(10,10,10)=(0,0,0)$ ✓(§8 B12)
- $V\subseteq Z(G_{20})$: $r^{10}$ は $D_{20}$ の中心元($sr^{10}s^{-1}=r^{-10}=r^{10}$)⟹ **(V-cen) ✓**

$$\Longrightarrow\ \boxed{\ \textbf{定理 ROOF-KILL が }K^{(20)}\textbf{ に適用でき、}d_{K^{(20)}}=5\textbf{ の完全な紙証明を与える}\ }$$

> ### ★★ prereg §1.3 との独立整合
> prereg 補題 K20-LIFT は正典 **Thm 4.3 (4.12)** から「$\phi_1$ の原像はちょうど 2 個、$(\widetilde m,\widetilde k)=(0,6)$ と $(10,1)$」を出し、$\widetilde m=0$ の witness の**存在**を示した(⟹ P-K20-4 = 障害類 0)。
> **本稿は正典 Thm 4.3 を一度も使わずに、その witness を座標で書き下した。** ⟹ **二経路の独立整合**(正典の閉じた式 vs 本稿の fiber product 構成)。
> ⚠ ただし **`cross-checked` は名乗らない**(両方とも紙・同一起草者・CV-9 非当事者判読を経ていない)。
> ★ さらに §8 B13–B17 は「$[P,P]$ 内の $f_1$ の持上げはちょうど 2 個($=\lvert W\rvert$・補題 W-TORSOR (a) の実物)」「**両方とも $\beta_\theta=0$**($N_\theta\vert_W=0$ ゆえ)」「**$\beta_\tau=0$ は 2 個中 1 個だけ**($N_\tau\vert_W=\mathrm{id}$ ゆえ)」を確認した — **補題 W-TORSOR (d) の $\operatorname{coker}\psi_W$ 構造がそのまま実物で見えている**。

### 4.4 (V-der) はどこで効くか(ROOF-KILL 版・**委嘱の必須項目**)

| 主張 | 判定 |
|---|---|
| **(V-der) $\Rightarrow\delta_{\rm roof}=0$** | ★ **成立**。$W=V$ なら $V/W=0$ ゆえ (d) の不変量は消える |
| **$\delta_{\rm roof}=0\Rightarrow$ (V-der)** | ✗ **偽**。$K^{(20)}$ が反例((V-der) は破れるが $\delta_{\rm roof}=0$・§4.3) |
| **review §1.2 の前件 (d)** | ⚠ **強すぎた**。(d) を $\delta_{\rm roof}=0$ に置換すると射程が $K^{(20)}$ まで伸びる |
| **「屋根型は全部死ぬ」** | ⚠ **依然として言えない**。$\delta_{\rm roof}\ne0$ の屋根は原理的にあり得る(§5.1 KT-6 の注) |

> ### ★ 発案 1-A の「障害は $N'$ 側の 1 個の類に局在」の厳密形(**成立**)
> (b) の下で任意の持上げは $\widetilde f=(f_1,v)$($v\in V'$)であり、
> $$\beta_\theta=(1,\ v\,\theta(v)),\qquad \beta_\tau=(1,\ \tau^2(v)\tau(v)v)$$
> — **第 1 成分は恒等的に消え、障害は $G'$($=N'$ 窓)側のデータだけで決まる**。⟹ 発案 1-A の核心は**成立する**。ただし補正 $v$ が動ける範囲は $V'$ 全体ではなく **$W$ に対応する部分**であり、そこが $\delta_{\rm roof}$ の内容である。

---

## 5. 系 — W-6 生存に必要な条件の絞り込み(**掘削前に紙で殺せる型のリスト**)

### 5.1 ★★ 死因型の一覧(**KT 表**)

$N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$c\in N$、$N$ isolated、**(V-cen)** を仮定する(破れる窓は **S-W6-5 / SCOPE_OUT**)。次のいずれか 1 つでも成り立てば $d_N=5$(**検出力ゼロ・掘る前に棄却**)。

| # | 死因型 | 判定基準 | コスト | 出所 |
|---|---|---|---|---|
| **KT-1** | **標数** | $\gcd(\lvert V\rvert,6)=1$ | 位数 1 個 | 定理 W6-NULL5 / W6-OBS (C)(w6 §2.5)**既出** |
| **KT-2** | **障害群消滅** | $\operatorname{coker}\psi_W=0$($\psi_W=(N_\theta,N_\tau):W\to W^\theta\oplus W^\tau$) | $\mathbf F_p$ 線型代数 | 定理 W6-OBS (A) を **$W$ に適用**(★ 加群の訂正・補題 W-TORSOR) |
| **KT-3** | **分裂** | 拡大 $1\to V\to P\to G_5\to1$ が $B_3$-同変に分裂 | 紙 | 命題 K5-SPL0(campaign §3.3)**既出** |
| **KT-4** ★新 | ★ **$W=0$** | $V\cap[P,P]=1$ | 位数 2 個 | **定理 THETA-KILL (III)**(本稿) |
| **KT-5** ★新 | ★ **τ-自由** | $W^\tau=0$ かつ $\beta_\theta\in N_\theta(W)$ | $\mathbf F_p$ 線型代数 | 補題 W-TORSOR (c): $\beta_\tau\in W^\tau=0$ が強制。$p=2$・$W\cong\mathbf F_2^2$ で $\tau$ が位数 3 の型はこれで **$\operatorname{coker}\psi_W=0$ に潰れる**(w6 §3.3 生存表の「$p=2$ の $S_3$ 2 次元だけ 0」の理由) |
| **KT-6** ★ | ★ **屋根合成** | $N=K^{(5)}\cap N'$ かつ $f_1\mapsto1$ in $D$($\Leftarrow5\nmid\lvert D\rvert$)かつ $\delta_{\rm roof}=0$ | 紙 or 語 2 個 | **定理 ROOF-KILL**(本稿) |
| **KT-7** ★★ | ★★ **余輪体 witness** | $(2,-2)\in\alpha(N_{F_2})$、すなわち $x^2y^{-2}\in N_{F_2}[F_2,F_2]$。**十分条件: (V-der)** | ★ **アーベル化 1 本**(最安) | **定理 THETA-KILL (I)(II)**(本稿) |
| **KT-8** ★★ | ★★ **位数** | $\lvert PB_3/N\rvert=1000$ | 位数 1 個 | **系 THETA-1000**(本稿・KT-4/KT-7 の合流) |

> ⚠ **KT-6 の注**: 「屋根型は全部死ぬ」は**依然として証明されていない**。$\delta_{\rm roof}\ne0$ の屋根が実在しないことは示していない(発案 1-A の「破綻しそうな点」= 全滅と局在の混同、は**正しい警戒のまま**)。

### 5.2 ★★★ 生存の必要条件(**対偶・掘る帯の定義**)

上の KT 表の対偶を取ると、**$\widetilde m=0$ の項で障害が立ちうる窓は次をすべて満たす**:

| # | 必要条件 | 由来 |
|---|---|---|
| **NC-1** | $\gcd(\lvert V\rvert,6)\ne1$($V$ は 2- または 3-primary) | KT-1 |
| **NC-2** ★ | $\boxed{(2,-2)\notin\alpha(N_{F_2})}$ すなわち $x^2y^{-2}\notin N_{F_2}[F_2,F_2]$ ⟹ **(V-der) は破れる**、しかも $2(\bar x-\bar y)$ が $V/W\cong2\mathbf Z^2/\alpha(N_{F_2})$ の中で非零 ⟹ **$P^{\rm ab}$ で $\bar x-\bar y$ の位数が 4 以上** | KT-7 |
| **NC-3** ★ | $\boxed{W=V\cap[P,P]\ne0}$ | KT-4 |
| **NC-4** | $\operatorname{coker}\psi_W\ne0$($W$ 上で評価・**$V$ 上ではない**) | KT-2 |
| **NC-5** | 拡大が $B_3$-同変に非分裂 | KT-3 |
| **NC-6** | 屋根で書けるなら $\delta_{\rm roof}\ne0$ | KT-6 |
| **NC-7** | ⚠ **$d_N=1$ を主張するには** さらに $\mathcal X_N$ の $\widetilde m\equiv0\ (\mathrm{mod}\ 10)$ の**全項**が不可解であることが要る(w6 §1.2 の論理の向き)。$N_{\rm ord}=10$ ならその項は 1 本(発案 1-E【NORD10】) | campaign §4.3 |

**NC-2 と NC-3 の合わせ技**:

$$\lvert V\rvert\ \ge\ \lvert W\rvert\cdot\lvert V/W\rvert\ \ge\ 2\cdot2\ =\ 4\qquad\Longrightarrow\qquad \boxed{\ \lvert PB_3/N\rvert\ \ge\ 500\cdot4\ =\ \mathbf{2000}\ }$$

### 5.3 ★ 掘る帯(**2-primary の最小の生存候補**)

| $\lvert V\rvert$ | $\lvert PB_3/N\rvert$ | 判定 |
|---|---|---|
| 2 | **1,000** | ★★ **死**(系 THETA-1000・前件ゼロ) |
| 4 | **2,000** | ★ **生存しうる**。ただし $\lvert W\rvert=\lvert V/W\rvert=2$ が強制され、NC-2 は「$\alpha(N_{F_2})$ が $2\mathbf Z^2$ の指数 2 部分格子で $(2,-2)$ を含まない」に確定 — **格子 3 個のうち 1 個だけが該当**($\alpha(N_{F_2})=\langle(4,0),(0,2)\rangle$ 型 / $\langle(2,0),(0,4)\rangle$ 型は可、$\langle(2,2),(4,0)\rangle$ 型は **$(2,-2)$ を含むので不可**) |
| 8 | **4,000** | 生存しうる($K^{(20)}$ と同位数 — ただし $K^{(20)}$ 自身は KT-6 で死ぬ) |
| 16 | **8,000** | 生存しうる(発案 3-B【AFAITH-8000】の帯) |

> ★ **$p=3$ 側**: $\lvert V\rvert=3^k$。$\dim_{\mathbf F_3}W=1$ では $N_\tau=3=0$、$N_\theta=1\pm1\in\{2,0\}$ ゆえ $\operatorname{coker}\psi_W\cong W$ は**常に非零**で、実効障害は $\beta_\tau$ である(⟺ $p=2$ で実効障害が $\beta_\theta$ であることの鏡像)。**KT-7 の $p=3$ 版**(τ-余輪体 $w'$ が $[P,P]$ に入れば死)は**同じ語 $w'$ で発火する** — 補題 COBDY は標数に依存しないからである。⟹ **NC-2 は $p=3$ 帯にもそのままかかる。**
> ⟹ $p=3$ の最小生存候補は $\lvert V\rvert=9$、$\lvert PB_3/N\rvert=4500$($\lvert V\rvert=3$ は NC-2 + NC-3 で $\lvert V\rvert\ge9$ が要るため死。**系 THETA-1500**: $\lvert PB_3/N\rvert=1500$ も同じ論法で死ぬ)。

> ### ★★ 系 THETA-1500(**$p=3$ 版の最下段**・上と同型の証明)
> $\lvert PB_3/N\rvert=500\cdot3=1500$、$N$ isolated ⟹ $\lvert V\rvert\le3$、$V$ 正規で位数 3 ⟹ $V\subseteq Z(P)$ は**自動ではない**($\mathrm{Aut}(C_3)=C_2$)。⚠ ゆえに **(V-cen) を assert する必要がある**。(V-cen) の下では $W\in\{0,V\}$ の 2 択で、$W=0$ なら KT-4、$W=V$ なら (V-der) ⟹ KT-7。⟹ $d_N=5$。
> ⚠ **(V-cen) が破れる場合(= $P$ が $V\cong C_3$ に位数 2 で作用)は本系の射程外**【W6K-GAP-2】。

---

## 6. 前身文書との差分(**訂正の明示**)

### 6.1 `ideas_020_review_v1.md` への訂正 2 件

| # | review の記述 | ★ 訂正 |
|---|---|---|
| **C-1** ★★ | §1.3「$K^{(20)}$ は前件 (d) が破れる ⟹ **ROOF-KILL の射程外** ⟹ 『屋根は死ぬ』は $K^{(20)}$ では言えない。実際 $K^{(20)}$ の witness $(0,6)$ は**成分合成ではない別経路**」 | **鋭い前件 $\delta_{\rm roof}=0$ の下では射程内**。$(f_1,1)=(6,4,0)$ が実際に $[G_{20},G_{20}]$ に入り、2 本のノルムを満たす(§4.3・§8 B8–B12)。⟹ **$K^{(20)}$ の witness は成分合成そのものである可能性が高い**(prereg の $(0,6)$ との同定は未了・【W6K-GAP-3】) |
| **C-2** ★ | §3.4 命題 THETA-KILL (3)「障害は $\beta_\tau\in N_\tau(\ker N_\theta\vert_W)$ の 1 個の membership に同値」/ §3.5「札 2-B は『$\overline{W_\tau}\in N_\tau(\ker N_\theta\vert_W)$ なら棄却』に置き換えるべき」 | ★ **同値性の主張は正しい**が、**$\dim_{\mathbf F_2}W=1$ ではこの条件は恒真**($N_\theta\vert_W=0$ ゆえ $\ker N_\theta=W$、$N_\tau\vert_W=\mathrm{id}$ ゆえ $N_\tau(W)=W$)。⟹ **実効的な判定量は $\beta_\tau$ ではなく $\beta_\theta$ である**。さらに定理 THETA-KILL (I) により、**$\overline{w'}\in[P,P]$ の窓では $\beta_\theta$ も $\beta_\tau$ も同時に消せる** ⟹ **札 2-B の篩は「$W_\tau$ の語評価」ではなく「$(2,-2)\in\alpha(N_{F_2})$?」に置き換わる**(桁違いに安い) |

### 6.2 保存されるもの(**訂正されない**)

- review §4 の **W-5 解析**(位数 1000・非分裂・Arf 類の同定・$[P,P]=A\times\{\pm1\}$・witness $(f_1,+1)=\bar w$)は**すべて生きている**。系 THETA-1000 はそれと**独立な第 2 経路**であり、両者は同じ結論に到達する。⟹ **W-5 は「第 4 の死因型の control」としての教材価値を保つ**。
- review §4.5 の **ENT-1 / NO-ENT(3) との整合判定**(3 軸で走査域の外)は本稿と無関係に不変。
- review §4.4 の **novelty の型**(「entangled *屋根* の実在庫」)も不変。
- **【W5-GAP-1】(isolated 性)は閉じていない** — 系 THETA-1000 も isolated を前件に置いている。

---

## 7. 格付け・GAP・新規性

### 7.1 格付け

| 主張 | 格 |
|---|---|
| **補題 COBDY**($N_\theta(u^{-1}\theta(u))=1$・$N_\tau(\tau(u)u^{-1})=1$) | ★★ **paper-proof candidate**(2 行の恒等式・群論一般・**Sol 未監査**) |
| **系 COBDY-$w'$**($w'=y^{-2}x^2$ が 2 本を同時に満たす) | ★★★ **paper-proof candidate**(紙 + 語簡約の機械確認・**Sol 未監査**) |
| **補題 W-TORSOR (a)(b)(c)(d)** | ★★ **paper-proof candidate**(初等・**Sol 未監査**) |
| **補題 SURJ-CENT** | ★★ **paper-proof candidate**($P=\langle\bar x,\bar y\rangle$ と $[P,P]\subseteq H$ の 4 行) |
| **定理 THETA-KILL (I)(II)(III)(IV)** | ★★★ **paper-proof candidate**(命題 K5-BIT に相対) |
| **系 THETA-1000** | ★★★ **paper-proof candidate**(前件は「位数 1000 + isolated + $N\trianglelefteq B_3$」のみ) |
| **系 THETA-1500** | ★ **paper-proof candidate**((V-cen) 相対・【W6K-GAP-2】) |
| **定理 ROOF-KILL (a)–(f)** | ★★ **paper-proof candidate**(Goursat + 初等) |
| **§4.3 の $K^{(20)}$ 適用**($\delta_{\rm roof}=0$・witness $(6,4,0)$) | ★★ **paper-proof candidate + 整数検算**。**prereg の Thm 4.3 経路と独立**だが **`cross-checked` は名乗らない**(CV-9 判読未) |
| **§5 の KT 表・NC 表・$\ge2000$ 下限** | ★ **上の定理群の系**(candidate) |
| **障害類の値・$d_N$・$d_{\rm gen}(5)$** | ★ **UNKNOWN**(本稿は上界側しか触れない) |
| §8 の検算 | ★ **single lane(python)。cross-checked ではない。Lean 検証でもない** |
| Lean 検証 | ✗ **していない** |

### 7.2 本稿が**主張しないこと**

1. 「W-6 が空である」— **主張しない**。§5.2 の帯は非空でありうる($K^{(20)}$ は NC-2/NC-3/NC-4 を通り、NC-6 で落ちた)。
2. 「屋根型がすべて死ぬ」— **主張しない**(§4.4 の注)。
3. 「$d_{\rm gen}(5)$ について何か言える」— **言わない**。
4. 「$\operatorname{coker}\psi_W\ne0$ の窓を見つけた = 検出力ある窓を作った」— **書かない**(**S-W6-3**: 群 $\ne$ 類)。
5. `cross-checked` / `verified` — **どちらも付さない**。

### 7.3 【GAP】(**新設・W6K 接頭辞 — 番号衝突を grep 済**)

| 札 | 内容 | 状態 |
|---|---|---|
| **【W6K-GAP-1】** | 系 THETA-1000 の**場合 2($c\notin N$)**。$V=1$ ゆえ結論は自明だが、**K5-BIT を $c\notin N$ の窓へ適用する規約**そのもの(campaign §5.0・w6 危険箇所 D-6)は未確定 | **UNKNOWN**(安い・司令塔の規約事項) |
| **【W6K-GAP-2】** | 系 THETA-1500 の **(V-cen)**。$\lvert V\rvert=3$ では中心性は自動でない($\mathrm{Aut}(C_3)=C_2$)。$P$ が $V\cong C_3$ に位数 2 で作用する窓が実在するか | **UNKNOWN** |
| **【W6K-GAP-3】** ★ | §4.3 の witness $(6,4,0)$ と prereg 補題 K20-LIFT の $(\widetilde m,\widetilde k)=(0,6)$ の**同定**(Thm 4.3 の $\widetilde k$ 座標と $A_{20}$ 座標の対応) | **UNKNOWN**(紙 1 枚・reader 案件) |
| **【W6K-GAP-4】** | 補題 W-TORSOR (d) で $W$ が**非可換**な窓(= $W\not\subseteq Z(P)$)の扱い。w6 補題 TWIST・【K5-GAP-W1】と同根 | **UNKNOWN**(既存 GAP を継承) |
| **【W6K-GAP-5】** ★ | ★ **定理 THETA-KILL (I) の逆**: $\overline{w'}\notin[P,P]$ のとき、**$\widetilde m=0$ で本当に障害が立つ窓**は実在するか。本稿は「立ちうる」までしか言っていない | **UNKNOWN(本命)** — 【K5-GAP-W4】の精密化 |

### 7.4 新規性の申告(**grep 済**)

**grep 語**(`docs/` `sol/` `provenance/` 全文): `ROOF-KILL`・`THETA-KILL`・`COBDY`・`SURJ-CENT`・`delta_roof`・`theta-defect`・`θ-欠損`・`coboundary`・`余輪体`・`境界元`・`y^{-2}x^2`・`y^-2x^2`・`2(\bar x-\bar y)`・`alpha(N`・`アーベル化水準`。

| 項目 | 既出か | 差分 |
|---|---|---|
| `ROOF-KILL` / `THETA-KILL` の**名前** | ★ **既出**(`ideas_020_w6_target.md` 札 1-A/1-D・`ideas_020_review_v1.md` §1.2/§3.4・`docs/地図.md`・LEDGER) | ★ 本稿は**同名の強化版**。§6.1 に訂正 2 件を明示 |
| $w=x^2y^{-2}$ の θ-ノルム恒等消滅 | ★ **既出**(発案 札 1-D・review §3.1 が逐語検算) | ★ 本稿は**理由**を与えた(補題 COBDY: θ-余輪体だから) |
| **$w'=y^{-2}x^2$**(2 本を同時に消す語) | **発見できず**(grep ゼロ) | ★★★ **本稿** |
| **補題 COBDY**(余輪体はノルムを恒等的に消す) | `coboundary` の既出 3 件(`div_law_v1.md`・`loc_lemmas_v1.md`・`no_ent3_v1.md`・Sol 便 08/15/16)は **$H^1$ の余輪体**で**別文脈** | ★ 本稿は $N_\theta,N_\tau$ の恒等式として使う。**群コホモロジーでは標準的な事実**(「ノルムは余輪体を殺す」)であり **「初」とは書かない** — **本設定への翻訳が寄与**である |
| 障害加群が $W=V\cap[P,P]$ であること | ★ **既出**(prereg §2.6 が $K^{(20)}$ の**実測**で同定) | ★ 本稿は**一般形の証明**(補題 W-TORSOR)に昇格 |
| **補題 SURJ-CENT**(中心核 ⟹ SURJ 自動) | ★ **前身あり**(補題 SURJ-W6 = $V\subseteq\Phi(P)$ 版・w6 §4.2) | ★ **前件を「$V$ 中心」だけに落とし、$\Phi$ 検査を不要にした** |
| **$\delta_{\rm roof}\in V/W$** | **発見できず** | ★★ **本稿** |
| **witness $(f_1,1)=(6,4,0)$ for $K^{(20)}$** | **発見できず**(prereg は Thm 4.3 経由で存在のみ) | ★★ **本稿**(座標で明示) |
| **系 THETA-1000**($\lvert PB_3/N\rvert=1000$ 無条件死) | **発見できず** | ★★★ **本稿** |
| **NC-2**($(2,-2)\notin\alpha(N_{F_2})$)= 生存の必要条件 | **発見できず** | ★★★ **本稿** |

**「初」という語は使わない。** ノルム写像が余輪体を消すことも、Goursat による subdirect 分解も、群論では標準である。**本設定($B_3$-正規細分・hexagon の $\widetilde m=0$ 項)への翻訳と、それによる位数 1000/1500 帯の否定判定が本稿の寄与**である。

### 7.5 Sol への監査依頼(優先順)

1. ★★★ **系 COBDY-$w'$**(§3.2)— $w'=y^{-2}x^2$ が $F_2$ で 2 本のノルムを同時に消すこと、および $\psi_5(w')=f_1$。**ここが本稿の全体重を支えている**(私は語簡約で機械確認したが、**規約($\tau$ の定義 $x\mapsto y\mapsto z\mapsto x$、$z=(xy)^{-1}$)が campaign §1.3 と同一か**が急所)。
2. ★★★ **系 THETA-1000**(§3.5)— 「位数 1000 + isolated + $B_3$-正規」だけから $d_N=5$。**前件がここまで少ないことに落ちはないか**。とくに $\lvert V\rvert=2$ ⟹ (V-cen) 自動、$W\in\{0,V\}$ の 2 択、の 2 段。
3. ★★ **補題 SURJ-CENT**(§2.2)— $H\trianglelefteq P$ ⟹ $[P,P]\subseteq H$ ⟹ $\bar y\in H$ の 4 行。**$P=\langle\bar x,\bar y\rangle$ を使ってよいか**($P=F_2/N_{F_2}$ なので使えるはず、というのが当方の見立て)。
4. ★★ **補題 W-TORSOR (b)**($\beta_\theta,\beta_\tau\in W$)— **可換性も中心性も使わずに** $[P,P]$ 保存だけから出る、という当方の主張。
5. ★★ **定理 ROOF-KILL (e)** と §4.3 の $K^{(20)}$ 適用 — **review §1.3 の「射程外」判定を覆した**箇所。$(6,4,0)$ が本当に $[G_{20},G_{20}]$ の元か(= $[G_{20},G_{20}]=\{$同一パリティ$\}$ の同定)。
6. ★ **§5.2 NC-2** の格子表現($V/W\cong2\mathbf Z^2/\alpha(N_{F_2})$)と、そこから出る $\lvert PB_3/N\rvert\ge2000$。
7. **§6.1 C-2** — 「$\dim W=1$ では $\beta_\tau$ 条件は恒真であり実効判定量は $\beta_\theta$」という訂正。発案 札 2-B の篩をこれで置き換える提案。

---

## 8. 検算(**証明とは独立・single lane python・群計算ゼロ**)

- **script**: `scratchpad/w6_kill_check.py`
- **SHA-256**: `39c7787bde25471feb15659934c76828638672915ba1748e6a8c6dce2de8d00e`
- **Python 3.13 / FAILS = 0(ALL PASS)**
- **内容**: (A) $F_2$ の自由簡約による語恒等式 / (B) $(\mathbf Z/10)^3$ の整数演算 / (C) θ-defect 公式。**GAP を呼んでいない・証明書を読んでいない・$\mathrm{Im}\,R$ に触れていない。**

| # | 検査 | 使う場所 |
|---|---|---|
| **A0–A2** | $\theta^2=\tau^3=\mathrm{id}$ on $F_2$、$\tau(z)=x$ | §1 の規約 |
| **A3/A4** | $N_\theta(w)=1$(既出)/ **$N_\tau(w)\ne1$**(既出の非自明語) | 発案 1-D・札 2-B |
| **A5/A6** ★★★ | ★ **$N_\theta(w')=1$ かつ $N_\tau(w')=1$**($w'=y^{-2}x^2$) | ★ **系 COBDY-$w'$**・定理 THETA-KILL (I) |
| **A7/A8** | ランダム 200 個の $u$ で $N_\theta(u^{-1}\theta(u))=1$・$N_\tau(\tau(u)u^{-1})=1$ | ★ **補題 COBDY** |
| **A9–A12** | $w=u^{-1}\theta(u)$($u=x^{-2}$)/ $w'=\tau(u)u^{-1}$($u=x^{-2}$)/ $w'=u^{-1}\theta(u)$($u=y^2$)/ $w'=y^{-2}wy^2$ | §3.1・§3.2 |
| **B1–B3** | $\lvert[G_{20},G_{20}]\rvert=250$、$\lvert G_{20}^{\rm ab}\rvert=16$、$\langle2\mathbf Z^3,(-1,1,-1)\rangle=\{$同一パリティ$\}$ | §4.3(review §1.3・prereg §2.6 の独立再現) |
| **B4–B7** | $\lvert V\rvert=8$、$W=\langle(5,5,5)\rangle$、**$\overline w\notin[G_{20},G_{20}]$** | §4.3・KT-7 が $K^{(20)}$ で発火しないこと |
| **B8–B12** ★★ | ★ **$(f_1,1)=(6,4,0)$**: mod 5 で $f_1$・mod 2 で $0$・**$[G,G]$ に所属**・**2 本のノルム $=0$** | ★★ **定理 ROOF-KILL の $K^{(20)}$ 適用**(§4.3) |
| **B13–B17** ★ | $[G,G]$ 内の $f_1$ の持上げはちょうど **2 個**($=\lvert W\rvert$);**両方とも $\beta_\theta=0$**;**$\beta_\tau=0$ は 1 個だけ** | ★ **補題 W-TORSOR (a)(d)** の実物($N_\theta\vert_W=0$・$N_\tau\vert_W=\mathrm{id}$) |
| **C1–C4** | $v_0$ の候補が 2 個・**θ-defect は取り方によらない**・**$=0$**・$\in W$ | §3・prereg **P-K20-4(障害類 0)と一致** |
| **C5/C6** | $[\overline w]=[u]$ in $V/W$ ⟹ $\delta_{\rm roof}=0$(**§4.3 とは別経路**)・$N_\theta(u)=0$ | ★ **定理 ROOF-KILL (e)** |
| **C7/C8** | $\dim W=1$: $N_\theta\vert_W=0$・$N_\tau\vert_W=\mathrm{id}$ | §6.1 C-2 の訂正 |

> ⚠ **B16 は初稿で FAIL した。** 当方の期待値「第 2 の持上げも $\beta_\tau=0$」が**誤り**で、正しくは $N_\tau\vert_W=\mathrm{id}$ ゆえ $\beta_\tau$ は $W$ ぶん動く。**期待値を訂正して PASS**(検査自体は残し、正しい値 $(5,5,5)$ を assert)。⟹ **これは実装バグではなく当方の紙の誤りを機械が捕まえた事例**であり、S-8 の趣旨に従い**記録を残す**(値を後から弱めたのではなく、理論が予言する値に直した)。

---

## 付録. 記号早見(本稿固有)

| 記号 | 意味 |
|---|---|
| $w$ | $x^2y^{-2}\in F_2$(**既出**・発案 1-D)。$\psi_5(w)=f_1$、$N_\theta(w)=1$ |
| ★ $w'$ | $y^{-2}x^2\in F_2$(**本稿**)。$\psi_5(w')=f_1$、**$N_\theta(w')=N_\tau(w')=1$** |
| $W$ | $V\cap[P_N,P_N]$ — ★ **障害の載る加群**($V$ ではない) |
| $\mathcal L$ | $\pi^{-1}(f_1)\cap[P_N,P_N]$ — $W$-torsor |
| $\beta_\theta,\beta_\tau$ | $\widetilde f_0\theta(\widetilde f_0)$、$\tau^2(\widetilde f_0)\tau(\widetilde f_0)\widetilde f_0\in W$ |
| $\psi_W$ | $(N_\theta,N_\tau):W\to W^\theta\oplus W^\tau$ |
| ★ $\delta_{\rm roof}$ | $[\widetilde f_0^{-1}(f_1,1)]\in V/W$ — 屋根合成 witness の所属不変量 |
| $\alpha$ | $F_2\to F_2^{\rm ab}=\mathbf Z^2$(アーベル化)。$\alpha(w)=\alpha(w')=(2,-2)$ |
| (V-der) | $V\subseteq[P_N,P_N]$、すなわち $W=V$ — ★ **前件ではなく十分条件** |
| (V-cen) | $V\subseteq Z(P_N)$ — ★ **(SURJ) のためだけに使う** |
