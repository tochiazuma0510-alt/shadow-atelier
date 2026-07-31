# SETTLED-CENT の紙上定式化 — **予想は的中しているが、機構は「向きの混線」である**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 委嘱: 司令塔(次波 2)「命題候補『$(m,f)$ の fine lift が settled $\iff\Phi(m,f)\in C_H(\hat c)$』の証明を試みよ。証明が立てば一般窓への予言も。発案係の $\mathrm{Aut}(P)$ 実装と $\mathrm{Hol}(\mathbb Z/5)$ 座標の対応検分も(裁定 293 の検分待ち事項)」
- 入力正本: `search/certs/pent_settled_struct_20260731.json`(SHA-256 `a735339e…95e6b0`)/ `search/probe/wac_v1/pent_settled_struct_20260731.g`(`618156 02…5ccbf55`)/ `ideas/ideas_016_post_bridge.md` I16-1a/1c/1d / `docs/notes/pent_conflict_diagnosis_v2.md` / `sol/sol_reply_92_math19.md` **F92-1.1**(★ 本稿の核心と直結)
- 本稿の検算: `search/probe/wac_v1/pent_settled_cent_proofcheck_20260731.g`(`b4328f5c…9e5e6efd`)+ `..._proofcheck2_20260731.g`(`9ee1d981…d27596f4`)。**v3.1 / struct probe を 1 バイトも書き換えず、窓・`cof`・`Psi`・`coarse_of`・`Hex`・`Chk6` を逐語移植した別ファイル**。
- **LEVEL CAVEAT(継承)**: 本稿の settled はすべて **$PB_3$ 水準**($PB_4$ 水準 C1 Prop 2.11 の必要条件であって、その主張ではない)。

---

## 0. 判定(先に 6 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | SETTLED-CENT(settled $\iff\Phi(m,f)\in C_H(\hat c)$)は正しいか | **実装された測定に対しては正しい。しかも 4 つの互いに異なる判定式が同じ 4 行を切り出す**(§5)。**証明した**(定理 SC) |
| **②** | 機構は何か | **$\hat c$ は「$\bar x,\bar y$ を同時に反転する唯一の自己同型」であり、probe の粗ラベル $f$ と真の準同型像 $\rho(q)$ は $\rho(q)=\hat c(f)^{-1}$ で結ばれる**(定理 ORI・3 行・全 7500 元で機械確認)。settled 判定は本質的に「$f$ が向き反転で不変か」を測っていた |
| **③** | ではその測定は数学的に意図した量か | **否。★ 実装された $T$ は向きの規約を混ぜている**(ラベルは著者側=順方向、共役は我々側=$q^{-1}\cdot q$)。**どちらか一方に統一すると 20/20 が settled になる**(§6・機械確認: flipped $T'$ は 20 行すべてで well-defined かつ単射) |
| **④** | I16-1c KER-QUANT | **定理になった**(定理 KQ)。$Q_P=A\times V$、$A=[Q_P,Q_P]\cong A_5$、$V=Z(Q_P)\cong C_5^3$ から、$T$ の核は **$\{1,\ A\}$ の二値しかあり得ない**。「$A_5$ 丸ごと・$C_5^3$ 無傷」は構造の帰結であって観測ではない |
| **⑤** | I16-1d STAR-LAG(4+8+8) | 実測構造は**定理 TRI の三分**として完全に説明される(§4)。ただし ③ により、この三分自体が規約混線の産物である |
| **⑥** | 発案係の $\mathrm{Hol}(\mathbb Z/5)$ 手計算 | **正しい**($C_{F_{20}}(\hat c)\cong C_4$)。$\mathrm{Aut}(P)$ 実装との対応も確定 — $H=N_{S_5}(\langle\bar x\rangle)$、$\hat c$ は $H$ の中で唯一の「点 3 を固定する対合」、$C_H(\hat c)=\mathrm{Stab}_H(3)$。**発案係の「零切断」は $\hat c$ の不動点の安定化群のことで、番号づけの差だけ**(§7) |

> **一行で**: 「settled 4 行 = 自己逆元 $f$ ちょうど」という指紋を、**Sol 自身が便 92 の F92-1.1 で『共有仕様バグの強い指紋』と名指ししている**。同じ指紋が settled 測定でもう一度出ている。予想は当たったが、当たった先はバグの像である公算が高い。

---

## 1. 記号と、確定している構造

$P:=P_N=\langle\bar x,\bar y\rangle=A_5$($\bar x=s_1^2,\ \bar y=s_2^2$、いずれも位数 5)、$N_{\rm ord}=5$、charming $m\in\{0,1,3,4\}$、$u:=2m+1\in\{1,3,7,9\}$($\gcd(u,5)=1$)。

$F:=\langle x,y,c\rangle$ 自由。**二つの評価**:
- $\theta:F\to P$、$x\mapsto\bar x,\ y\mapsto\bar y,\ c\mapsto1$ — probe の `coarse_of`(**順方向・準同型**)。
- $\Psi:F\to E^5$、$\Psi(w):=\Theta(\mathrm{Rev}(w))$、$\Theta$ は $x\mapsto(\text{cof}_i[1])_i$ 等の準同型 — probe の `Psi`(**語を反転してから代入**;宣言 `f_orientation = psi_reversed_for_defect_eval__forward_coarse_of_WordOf_for_coarse_fiber_label`)。$\Psi$ は**反準同型**である($\Psi(w_1w_2)=\Psi(w_2)\Psi(w_1)$)。

$Q_P:=\Psi(F)=\Theta(F)\le E^5$、$\lvert Q_P\rvert=7500$。$\rho:Q_P\to P$ は $\Psi(x)\mapsto\bar x,\Psi(y)\mapsto\bar y,\Psi(c)\mapsto1$ の**準同型**(probe の `redMap`$=\mathrm{pr}_1\vert_{Q_P}$)。$\mathrm{WordOf}(q)$ は $\Psi(w)=q$ なる語 $w$、probe のラベルは $f:=\theta(\mathrm{WordOf}(q))$。

> ### 定理 STR($Q_P$ の構造)【定理 + 機械】
> $$Q_P=A\times V,\qquad A:=[Q_P,Q_P]\cong A_5,\qquad V:=Z(Q_P)=\ker\rho\cong C_5^3,$$
> かつ $\rho\vert_A:A\xrightarrow{\ \sim\ }P$、$C_{Q_P}(A)=V$、$Q_P/A\cong C_5^3$。
> **証明.** $\lvert A\rvert=60$、$\lvert\ker\rho\rvert=125$(v2 で既測・本稿で再現)。$Q_P/\ker\rho\cong A_5$ は完全だから $Q_P=A\cdot\ker\rho$、位数から $A\cap\ker\rho=1$。両者は正規で交わりが自明ゆえ元ごとに可換、$Q_P=A\times\ker\rho$。$Z(Q_P)=Z(A)\times\ker\rho=\ker\rho$($Z(A_5)=1$)。$C_{Q_P}(A)=Z(A)\times V=V$。∎
> **機械**(proofcheck §C1): $\lvert[Q_P,Q_P]\rvert=60$ = `A5`、$\lvert Z(Q_P)\rvert=125$ = `C5 x C5 x C5`、$Z(Q_P)=\ker\rho$ **true**、$A\cap V=1$ **true**、$\rho\vert_A$ 全単射 **true**、$C_{Q_P}(A)=V$ **true**。

**粗 shadow**: $S_m:=\{f\in P:\mathrm{Hex}(m,f)\wedge\langle\bar x,\bar y^f\rangle=P\}$、$\bigsqcup_m\{m\}\times S_m=\mathrm{GT}(N_A)$、$\lvert S_m\rvert=5$、計 20。
**$\Phi$**: $\Phi_{m,g}\in\mathrm{End}(P)$ を $\bar x\mapsto\bar x^u,\ \bar y\mapsto(\bar y^u)^g$ で定める(存在すれば)。
$$\Sigma_m:=\{g\in P:\Phi_{m,g}\ \text{が well-defined}\}.$$
$\Phi_{m,g}$ は右剰余類 $C_P(\bar y)g$ にのみ依る($C_P(\bar y)=\langle\bar y\rangle$、位数 5)ので $\Sigma_m$ は $C_P(\bar y)$-右剰余類の合併。**機械**: $\lvert\Sigma_m\rvert=25$(5 剰余類)が全 $m$ で成立、$S_m\subseteq\Sigma_m$、$\Phi$ は 20 個の shadow 上**単射**($\lvert H\rvert=20$、相異なる $\Phi$ が 20 個)。

---

## 2. 定理 ORI — 向きの恒等式(本稿の要)

> ### 補題 CC($\hat c$ の正体)【proof + 機械】
> $\hat c:=\Phi_{4,()}$ は $\bar x\mapsto\bar x^9=\bar x^{-1}$、$\bar y\mapsto\bar y^{-1}$、すなわち **$\bar x,\bar y$ を同時に反転する自己同型**である。$\mathrm{Aut}(P)=S_5$ の中でそのような元は**ちょうど 1 個**、$\kappa=(1,4)(2,5)\in A_5$(内部自己同型)。
> **機械**(proofcheck §C2): $\#\{k\in S_5:\bar x^k=\bar x^{-1},\bar y^k=\bar y^{-1}\}=1$、$\kappa=(1,4)(2,5)$、$\hat c=\mathrm{conj}_\kappa$ **true**、$\lvert C_{S_5}(\kappa)\rvert=8$、$\lvert C_H(\hat c)\rvert=4\cong C_4$。
> **一意性の証明.** そのような $k$ 全体は $C_{S_5}(\langle\bar x,\bar y\rangle)=C_{S_5}(A_5)=1$ の剰余類。∎
> **注**: $\hat c$ は 2405 Remark 1.10 の複素共役 shadow $[-1,1]$ の $N_A$ での像(`week4-A5算術飽和_opus_v1.md` (A2) の $\hat c=[4,1]$)。**複素共役が「両生成元の同時反転」として現れることは偶然ではない** — 複素共役は平面の向きを反転し、組紐を逆にする。

$\tau:P\to P$, $\tau(g):=\hat c(g)^{-1}=(g^{-1})^\kappa$ とおく。$\tau$ は**位数 2 の反自己同型**。

> ### 定理 ORI(向きの恒等式)【定理・3 行】
> 全ての $q\in Q_P$ について
> $$\boxed{\ \rho(q)\ =\ \tau\bigl(\theta(\mathrm{WordOf}(q))\bigr)\ =\ \hat c(f)^{-1},\qquad f:=\theta(\mathrm{WordOf}(q))\ }$$
> **証明.** 自由群からの**反準同型は生成元の像で決まる**($\phi\mapsto(\phi(\cdot))^{-1}$ が反準同型と準同型の全単射を与えるから)。
> (i) $\rho\circ\Psi$ は反準同型($\rho$ 準同型 $\circ$ $\Psi$ 反準同型)で $x\mapsto\bar x,y\mapsto\bar y,c\mapsto1$。
> (ii) $w\mapsto\hat c(\theta(w))^{-1}$ は反準同型(準同型 $\hat c\circ\theta$ の後に反自己同型 inv)で、$x\mapsto\hat c(\bar x)^{-1}=(\bar x^{-1})^{-1}=\bar x$、$y\mapsto\bar y$、$c\mapsto1$。
> 生成元で一致 ⟹ 恒等的に一致。$q=\Psi(w)$ を代入。∎
> **機械**(proofcheck §C3): **$Q_P$ の全 7500 元で照合、不一致 0**。

> ### 系 ORI′(ラベルの well-defined 性 — Sol W92-1 (i) の粗水準の解決)
> $\theta(\mathrm{WordOf}(q))=\tau(\rho(q))$ は $q$ のみに依り、代表語の取り方に依らない。すなわち **`coarse_of ∘ WordOf` は $Q_P\to P$ の well-defined な反準同型**であり、その fiber はすべて位数 $125$。
> (これは $q$-水準の well-defined 性の**粗成分について**の主張である。$\mathrm{GT}(K_\pi)$ 全体の型付け(W92-1)を閉じるものではない。)

**★ この 1 本が、便 92 の F92-1.1 で Sol が「$f$ 対 $f^{-1}$ の辞書」と呼んだものの正体である。** 辞書の差は単なる逆元ではなく、**$\hat c$ で捻れた逆元 $\tau$** であった(実際 $m=0$ 層で $f=(2,3,4)\mapsto\rho(q)=(1,3,5)\ne(2,4,3)=f^{-1}$)。診断 v2 §1.2 が「集合としては逆元集合」と観測したのは、$\hat c$ が $S_m$ を保つ($S_m^\kappa=S_m$・機械 true)ためである。

---

## 3. 定理 TRI — settled の完全な三分

probe の実装する写像は、$(m,q)$ に対し
$$T=T_{m,q}:\ \Psi(x)\mapsto\Psi(x)^u,\quad \Psi(y)\mapsto q^{-1}\Psi(y)^uq,\quad \Psi(c)\mapsto\Psi(c)^u$$
であり、`well_defined_on_QP` $=$「これが $Q_P$ の自己準同型に延びる」、`settled` $=$「延びて核が自明」。$g:=\rho(q)$ と置く。

> ### 定理 TRI(三分)【定理・完全】
> 次の 3 つはちょうど 1 つずつ起こる。
> 1. **$g\in\Sigma_m$** $\iff$ $T$ は well-defined かつ**単射**($\ker T=1$)。すなわち **settled**。
> 2. **$g\notin\Sigma_m$ かつ $[\bar x^u,(\bar y^u)^g]=1$** $\iff$ $T$ は well-defined で **$\ker T=A\cong A_5$**、$\mathrm{im}\,T\cong Q_P/A\cong C_5^3$。すなわち **well-defined だが not settled**。
> 3. **$g\notin\Sigma_m$ かつ $[\bar x^u,(\bar y^u)^g]\ne1$** $\iff$ $T$ は **well-defined でない**。
>
> **証明.** 定理 STR で $Q_P=A\times V$、$V$ 中心、$V=\langle\xi,\eta,\gamma\rangle$($\xi,\eta,\gamma$ は $\Psi(x),\Psi(y),\Psi(c)$ の $V$-成分;$Q_P$ が 3 元生成で $V$ が階数 3 だからこれは基底)。$\rho\vert_A$ で $A\cong P$ と同一視する。
> **(1 ⟸ の構成)** $g\in\Sigma_m$ なら $\Phi_{m,g}\in\mathrm{End}(P)$ が存在し、$\Phi_{m,g}(\bar x)=\bar x^u\ne1$ かつ $P$ 単純ゆえ $\Phi_{m,g}\in\mathrm{Aut}(P)$。$\widetilde T:=\Phi_{m,g}\times(u\cdot\mathrm{id}_V)$ は $A\times V$ の自己同型。生成元で照合すると
> $\widetilde T(\Psi(x))=(\bar x^u,u\xi)=\Psi(x)^u$、$\widetilde T(\Psi(y))=((\bar y^u)^g,u\eta)=q^{-1}\Psi(y)^uq$($q$ の $A$-成分は $g$)、$\widetilde T(\Psi(c))=(1,u\gamma)=\Psi(c)^u$。ゆえに $T=\widetilde T$、$\ker T=1$($\gcd(u,5)=1$)。
> **(2 ⟸ の構成)** $[\bar x^u,(\bar y^u)^g]=1$ なら、3 つの像 $\Psi(x)^u,\ q^{-1}\Psi(y)^uq,\ \Psi(c)^u$ は**互いに可換**で位数 5 を割る($V$ は中心・$A$ 成分が可換)。$Q_P/A\cong C_5^3$ は上の 3 生成元の像を基底とする $\mathbb F_5$ 空間だから、$Q_P\twoheadrightarrow Q_P/A\to Q_P$ が well-defined に定まり、$T$ はそれに一致($A\subseteq\ker T$)。核は $A\times(\ker\ \text{on}\ V)$ で、$V$ 上は $v\mapsto uv$ 成分が単射ゆえ $\ker T\cap V=1$。$\ker T\triangleleft Q_P=A\times V$ かつ $\ker T\cap V=1$ ⟹ $\ker T$ は $\pi_A(\ker T)\triangleleft A$ から $V$ への準同型のグラフ;$A\cong A_5$ 完全・$V$ 可換ゆえ準同型は自明、$\pi_A(\ker T)\in\{1,A\}$。$A\subseteq\ker T$ より $\ker T=A$。
> **(排他性と ⟹ 方向)** $T$ が well-defined なら $T(A)=[T(Q_P),T(Q_P)]\le A$ で、$A$ 単純ゆえ $T\vert_A$ は自明か単射。
> - $T\vert_A$ 単射なら $T(A)=A$、$T(V)\le C_{Q_P}(A)=V$、よって $T=T\vert_A\times T\vert_V$。生成元から $T\vert_V=u\cdot$、$T\vert_A$ は $\rho\vert_A$ 越しに $\bar x\mapsto\bar x^u,\bar y\mapsto(\bar y^u)^g$、すなわち $\Phi_{m,g}$ が存在 ⟹ $g\in\Sigma_m$(場合 1)。
> - $T\vert_A$ 自明なら $\mathrm{im}\,T$ は $Q_P/A$ の商で可換、ゆえに $[\bar x^u,(\bar y^u)^g]=1$(場合 2)。
> 場合 1 と 2 は両立しない($\Phi_{m,g}$ が存在すれば像 $P$ は非可換)。ゆえに $T$ が well-defined なら 1 か 2、well-defined でなければ 3。∎
>
> **機械**(proofcheck2 §C6・20 行全数):
> `settled <=> Phi_{m,g} well-def` **true** / `(T ok, not settled) <=> commutes` **true** / `T not well-def <=> neither` **true** / `kernel sizes seen = [1, 60]` ✓

> ### 系 KQ(= I16-1c KER-QUANT の定理化)
> **$T$ が well-defined なら $\ker T\in\{1,\ A\}$、$A\cong A_5$、$Q_P/A\cong C_5^3$、$C_{Q_P}(A)=V\cong C_5^3$。中間の核サイズは原理的に存在しない。**
> ⟹ cert の `K_size=60 / K=A5 / quot=C5^3 / C_QP(K)=C5^3` の**一律性は測定結果ではなく構造の帰結**。発案係の「量子化」は正しく、しかも「$V=1$ が常に」は $A_5$ の完全性・$V$ の中心性から**証明できる**(8 標本の帰納ではない)。**別窓で中間値が出れば即死、という破綻条件も消える**(ただし $P$ が単純でない窓では定理ごと書き直しが要る)。

---

## 4. 定理 SC — SETTLED-CENT の証明(実装された測定に対して)

定理 ORI により $g=\rho(q)=\tau(f)$。$\Sigma_m$ は $\kappa$-共役で安定($\Phi_{m,g^\kappa}=\hat c\Phi_{m,g}\hat c^{-1}$;機械 true)なので
$$g=\tau(f)=(f^\kappa)^{-1}\in\Sigma_m\iff (f^{-1})^\kappa\in\Sigma_m\iff f^{-1}\in\Sigma_m.$$

> ### 定理 SC(settled の閉じた判定式)【定理】
> $$\boxed{\ \text{settled}(m,f)\iff f^{-1}\in\Sigma_m\ }$$
> とくに **$\tau(f)=f$(すなわち $f^\kappa=f^{-1}$)ならば settled**($\tau(f)=f\in S_m\subseteq\Sigma_m$)。
> **証明.** 定理 TRI 場合 1 + 上の同値。∎

> ### 系 SC′(この窓での 4 判定式の一致)【機械・20/20】
> $K_\pi$ 窓では次の 5 条件が 20 行すべてで同値:
> $$\text{settled}\iff f^{-1}\in\Sigma_m\iff f^{-1}\in S_m\iff f=f^{-1}\iff \Phi(m,f)\in C_H(\hat c).$$
> 該当 4 行は $(m,f)\in\{(0,()),(1,\kappa),(3,\kappa),(4,())\}$、$\kappa=(1,4)(2,5)$。**settled な $f$ は $\{1,\kappa\}$ ちょうど**、すなわち $\hat c$ 自身と恒等のみ。
> **$C_H(\hat c)$ 形の閉じた形**: $\Phi_{m,f}\in C_H(\hat c)\iff\Phi_{m,f^\kappa}=\Phi_{m,f}\iff f^\kappa f^{-1}\in C_P(\bar y)$。機械: 4 行では $f^\kappa f^{-1}=1$(すなわち $f^\kappa=f$)、他の 16 行では $C_P(\bar y)$ の外。

> ### ⚠ 系 SC′ の**注意**(一般窓への外挿の危険)
> 上の 5 条件は**論理的に同値ではない**。とくに
> $$\underbrace{f^\kappa=f^{-1}}_{\tau\text{-実}}\quad\text{と}\quad \underbrace{f^\kappa f^{-1}\in C_P(\bar y)}_{\Phi\in C_H(\hat c)}$$
> は別の条件で、この窓で一致したのは settled 側の $f$ が $\{1,\kappa\}$(両方の条件を自明に満たす)しか無かったからである。**機構をもつのは $\tau$-実性のほう**(定理 SC)であり、$C_H(\hat c)$ 形は**窓固有の一致**である。一般窓の予言は $\tau$ 側で立てるべきである(§8)。

---

## 5. 発案係の 3 札の判定

| 札 | 判定 | 根拠 |
|---|---|---|
| **I16-1a SETTLED-CENT** | **的中(実装された測定に対して)・証明済(定理 SC + 系 SC′)。ただし機構は $C(\hat c)$ ではなく $\tau$-実性** | §4 |
| **I16-1b FLIP-REAL** | **本質的に正しい。** 「$K$ が対合的自己同型 $\iota$(flip 型)で不変なら settled は $\iota$ 誘導対合の中心化群に含まれる」— 実際に効いていたのは $B_4$ の鏡映ではなく**語の向き反転**で、その $P$ 上の影が $\hat c$ である。発案係の自己指摘(「バグの残像を構造と誤認するリスクが最も高い形」)は**的中していた** | §2・§6 |
| **I16-1c KER-QUANT** | **定理化(系 KQ)。** 「$A_5$ 丸ごと・$C_5^3$ 無傷」は構造の帰結 | §3 |
| **I16-1d STAR-LAG** | 4+8+8 は定理 TRI の三分。$20=4\times5$ 予言が外れたのは正しく、**層化の正体は「$\tau(f)$ が $\Sigma_m$ に入るか / 可換化で潰れるか / 何も定義されないか」** | §3 |

---

## 6. ★ 最重要 — 測定の向きが混線している(【GAP-PSC-1】)

**事実(機械・proofcheck2 §C6)**:

| 実装 | well-defined | settled |
|---|---|---|
| probe の $T$: $\Psi(y)\mapsto q^{-1}\Psi(y)^uq$ | **12 / 20** | **4 / 20** |
| flipped $T'$: $\Psi(y)\mapsto q\,\Psi(y)^u q^{-1}$ | **20 / 20** | **20 / 20** |

**なぜ混線か.** probe は 2 つの規約を 1 つの計算に混ぜている:
- **ラベル**は **著者側(順方向)**: $f=\theta(\mathrm{WordOf}(q))$。診断 v2 が Package GT と照合して確立した、正しい著者側ラベル。
- **共役**は **我々側($Q_P$ の元 $q$)に、著者側の式 $f^{-1}(\cdot)f$ をそのまま適用**。

ところが $\Psi$ は反準同型であり、$q=\Psi(w)$ は「著者の語 $w$ が表す元」を我々の群で表現したもの。著者の式 $f^{-1}\sigma_2^uf$ を $\Psi$ で運ぶと $q\,\Psi(y)^u\,q^{-1}$ になる(反同型は共役の向きを裏返す)。**したがって probe の $T$ は「著者のラベル」+「我々の共役」という混成である。**

**どちらの規約に統一しても答えは 20/20 になる**:
- **(U-rev) 著者側ラベルを保つ** ⟹ $T'$(flipped)を使う ⟹ 機械で **20/20 settled**。
- **(U-fwd) 我々側に統一する** ⟹ ラベルも $\rho(q)$ に取り替え、hexagon も反転側で解く ⟹ 条件は $\Phi^{op}_{m,\rho(q)}$ の well-defined 性 $\iff\rho(q)^{-1}=f^\kappa\in\Sigma_m$、これは $\Sigma_m$ の $\kappa$-安定性から**常に成立** ⟹ **20/20 settled**。

**しかも settled かどうかは規約に依らない**(「$K_\pi^s=K_\pi$」は $PB_3$ の部分群の等式であり、我々がどの順で語を読むかとは無関係)。ゆえに:

> ### 【GAP-PSC-1】(名指しの穴・最優先)
> **cert `pent_settled_struct_20260731.json` の `settled_true_count = 4`、`settled_false_count = 8`、`not_well_defined_on_QP_count = 8` は、向き規約の混成による artifact である公算が高い。整合的な規約では 20/20 が settled になる。**
> ⟹ **裁定 293 の I16-1a「20/20 完全一致」・I16-1c の 8 行・I16-1d の 4+8+8 は、いったん保留(NOTE 格)に落とすことを進言する。**(数値内容そのものは正しく再現される — 誤りは「どの写像を測ったか」にある。)

**Sol の F92-1.1 との一致(独立の状況証拠)**: Sol は便 92 で
> 「生存 4 行が、10 個の粗 $f$ のうち**自己逆な 2 個**と 2 個の $m$ の直積に正確に一致することは、**この共有仕様バグの強い指紋**である。」

と書いた。settled 4 行はまさにその 4 行($f\in\{(),(1,4)(2,5)\}$、$m\in\{0,1\}\times\{$層$\}$)である。**同じ指紋が、同じ probe の別の測定でもう一度出ている。**

**なぜ回帰テストで捕まらなかったか**: v3.1 が導入した非自己逆元 unit test(element 4)は**ラベルの往復**($\text{coarse\_of}(\mathrm{WordOf}(\Psi(w)))=\theta(w)$)だけを assert しており、**作用($T$)の向きは検査していない**。P92-1 が求めた三角形
$$w\longrightarrow\Psi(w)\longrightarrow\mathrm{coarse}(\Psi(w))=\mathrm{forwardCoarse}(w)$$
は**ラベル層**の三角形であって、**作用層**の三角形ではない。

> ### 修理の指定(実装係へ・1 行の assert で十分)
> 非自己逆元 $f$(例 $(2,3,4)$)について、**$T$ の $y$-像の粗成分が $\Phi_{m,f}(\bar y)$ に等しいこと**を hard assert せよ:
> $$\rho\bigl(T(\Psi(y))\bigr)\ \overset{!}{=}\ \Phi_{m,f}(\bar y)=(\bar y^u)^f .$$
> 現行実装ではこれが $(\bar y^u)^{\tau(f)}$ になり、非自己逆元で即座に落ちる。**「規約はどちらか一方に統一する」という診断 v2 §5 の指示の、作用層への適用漏れがここである。**

---

## 7. 発案係の $\mathrm{Hol}(\mathbb Z/5)$ 座標と実装の $\mathrm{Aut}(P)$ の対応(裁定 293 の検分待ち事項)

**結論: 発案係の手計算は正しい。実装との対応も確定した。**

- $\Phi_{m,f}(\bar x)=\bar x^u$ ゆえ $H:=\langle\Phi_{m,f}\rangle$ の全元が $\langle\bar x\rangle$($\cong C_5$)を正規化する。$\lvert N_{S_5}(\langle\bar x\rangle)\rvert=20=\lvert H\rvert$ ゆえ
 $$\boxed{\ H=N_{S_5}(\langle\bar x\rangle)\ \cong\ \mathrm{Hol}(\mathbb Z/5)=\mathrm{AGL}(1,5)=F_{20}\ }$$
 (機械: $\lvert H\rvert=20$、`C5 : C4`)。同一視は「$\bar x$ が平行移動 $+1$ になるように 5 文字を $\mathbb Z/5$ と見る」。
- この座標で $H\to(\mathbb Z/5)^\times$(線形部)は $\sigma\mapsto u$、すなわち **$\widetilde\chi$(χ_vir)そのもの**。発案係の「$\chi_{\rm vir}=2m+1$」は線形部の座標である ✓。
- $\hat c$ は線形部 $-1$ の元、すなわち $x\mapsto-x+b$ 型 = **点 $b/2$ を唯一の不動点にもつ対合**。実装では $\hat c=\mathrm{conj}_{(1,4)(2,5)}$ で**不動点は 3**。
- $C_H(\hat c)=\mathrm{Stab}_H(3)\cong C_4$。**証明**: $\mathrm{Hol}(\mathbb Z/5)$ の対合は 5 個(不動点ごとに 1 個)。$g\in\mathrm{Stab}_H(3)$ なら $g\hat cg^{-1}$ は $g(3)=3$ を固定する対合ゆえ $\hat c$ に等しい ⟹ $\mathrm{Stab}_H(3)\le C_H(\hat c)$;位数はともに $20/5=4$ ⟹ 等号。∎(機械: $\lvert C_H(\hat c)\rvert=4$、`C4`)
- **発案係の「零切断 $\{(0,k)\}$」は「$\hat c$ の不動点の安定化群」のことで、原点の取り方(不動点を $0$ と置くか $3$ と置くか)の差だけ。数学的内容は一致。** 発案係の懸案「③ $F_{20}$ の半直積規約(作用の向き)を取り違えていれば C(ĉ) の計算ごと誤り」は**杞憂だった**($C_4$・位数 4・$\hat c$ を含む・$\chi_{\rm vir}$ に同型に写る、の 4 点すべて機械で一致)。

**ただし §4 の注意により、この $C_H(\hat c)$ が settled を支配しているという読みは採らない。**

---

## 8. 一般窓への予言(壁族の既存 cert で追試できる形)

**前提**: 以下は【GAP-PSC-1】が示す通り**現行実装の artifact に対する**予言である。修理後の実装に対する予言は「常に settled」(P-SC-0)である。両方を凍結しておけば、修理再走がどちらを支持するかで決着する。

> ### 予言 P-SC-0(修理後・本命)
> 向きを統一した再走では、**$K_\pi$ の 20 lift すべてが settled**($T$ が $Q_P$ の自己同型)になる。`not_well_defined` は 0 行。
> **根拠**: 定理 TRI 場合 1 + $\Sigma_m$ の $\kappa$-安定性(§6)。

> ### 予言 P-SC-1(現行実装を他窓へ回した場合)
> 命題 0.3 型の任意の窓 $K$(粗窓 $N$、$P=\langle\bar x,\bar y\rangle$ 単純)について、現行実装の settled 行は
> $$\{(m,f)\in\mathrm{GT}(N):\ \tau_N(f)\in\Sigma_m\},\qquad \tau_N(g):=\hat c_N(g)^{-1}$$
> でちょうど与えられる。$\hat c_N$ は「$\bar x,\bar y$ を同時反転する $\mathrm{Aut}(P)$ の元」(存在すれば一意;存在しなければ定理 ORI が形を変える — **その窓は判別実験として最良**)。
> **とくに $f=f^{-1}=f^{\hat c}$ なる行は必ず settled**、$\tau_N(f)\notin\Sigma_m$ なる行は必ず非 settled。

> ### 予言 P-SC-2(核の二値性・規約に依らない)
> $P$ が非可換単純で $\ker(Q\to P)$ が中心的な基本可換 $\ell$-群($\ell\nmid\lvert P\rvert$ の素数)である任意の窓で、$T$ が well-defined なら $\ker T\in\{1,\ [Q,Q]\}$。**中間の核は存在しない。**
> **これは規約に依存しない定理**(系 KQ の一般形)であり、**壁族の既存 cert で直ちに追試できる**: 核サイズの実測値が $\{1,\lvert P\rvert\}$ の外に出たら、その窓では $\ker(Q\to P)$ が中心的でないか $P$ が単純でない(構造診断として使える)。
> **追試コスト**: 既存 cert の核サイズ列を読むだけ(新測定ゼロ)。

> ### 予言 P-SC-3($\hat c$ の存在条件)
> $\hat c_N$(両生成元の同時反転)が $\mathrm{Aut}(P)$ に存在する $\iff$ $\bar x\mapsto\bar x^{-1},\bar y\mapsto\bar y^{-1}$ が $P$ の自己同型に延びる。**$P=A_5$、$\bar x,\bar y$ が位数 5 の場合は存在した**。$P=A_n$($n$ 大)の壁族窓では**一般には存在しない**と予想する。その窓では定理 ORI の右辺が「$\theta^-$($x\mapsto\bar x^{-1}$)を経由する」形に退化し、**ラベルと $\rho$-像の関係が $\hat c$ で書けなくなる** — 混線の診断がより難しくなる代わりに、**混線があれば settled 率が窓ごとに乱雑に見える**はずである(構造的な $C(\hat c)$ 形にならない)。
> **⟹ 壁族で settled 率を測って「乱雑」なら混線仮説の支持、「$C(\hat c)$ 形」なら SETTLED-CENT の族則性の支持。判別実験になる。**

---

## 9. 上位の主張への含意

1. **Sol W92-1(型付け残件)への含意**: 系 ORI′ により、粗ラベル写像 $q\mapsto\theta(\mathrm{WordOf}(q))$ は **well-defined な反準同型**である(代表非依存)。W92-1 の (i) は、**粗成分については閉じた**(ただし $\mathrm{GT}(K_\pi)$ の群構造・(ii) source kernel の $PB_4$ isolated 性・(iii) 合成の compatibility は手つかず)。
2. **もし P-SC-0 が正しければ**(20/20 settled)、$PB_3$ 水準の source-kernel 障害は**消える**。これは (ii) にとって良い報せだが、$PB_4$ 水準ではない(LEVEL CAVEAT)。
3. **I16-4c GAL-STAB(settled 率 = 窓の算術性の測度)は、現時点で支持データを失う**。settled 率 $4/20$ が artifact なら「$K_\pi$ の $G_{\mathbb Q}$-軌道が 5 窓分に割れている」という読みの根拠も消える。**GAL-STAB を試すには修理後の再走が先。**
4. **v4(20 全 arithmetical)との整合はむしろ良くなる**: 20 全部が算術的で 20 全部が settled、という一様な絵になる。

---

## 10. 検算一覧(GAP 4.16.0 / `gap.ps1` / -o 2g・単系統)

| ファイル | SHA-256 | 内容 | 結果 |
|---|---|---|---|
| `search/probe/wac_v1/pent_settled_cent_proofcheck_20260731.g` | `b4328f5c…9e5e6efd` | C1(構造)・C2($\kappa$ の一意性)・C3(向き恒等式・**全 7500 元**) | 全 PASS・不一致 0。C3 の後、乱数自由語ループで 2g heap 超過(検査自体は完了済) |
| `search/probe/wac_v1/pent_settled_cent_proofcheck2_20260731.g` | `9ee1d981…d27596f4` | 上の続き(乱数ループ削除)。$\Sigma_m$・20 行表・$T$ と $T'$ の両実装・5 判定式の一致 | 定理 TRI の 3 同値すべて **true**、$T'$ が **20/20 settled** |

**格**: **単系統(GAP のみ)。cross-checked ではない。Lean verified でもない。** ただし定理 STR・ORI・TRI・KQ・SC は**紙の証明があり、機械は照合**である(機械が主張の根拠ではない)。§6 の「20/20」は機械のみ(紙側の根拠は §6 の (U-rev)/(U-fwd) 二経路の議論)。

---

## 11. Sol への申し送り(監査の優先順)

- **監査点 A(最優先)**: **§6 の混線判定**。「$\Psi$ が反準同型だから著者の $f^{-1}(\cdot)f$ は $q(\cdot)q^{-1}$ に運ばれる」という 1 行が本稿最大の主張である。ここが誤りなら【GAP-PSC-1】は消え、SETTLED-CENT は素直な構造定理として生き残る。**便 92 F92-1.1 の指紋論法と独立に照合してほしい。**
- **監査点 B**: **定理 ORI** の 3 行(自由群からの反準同型が生成元で決まる/$\hat c$ が両生成元を反転する)。全 7500 元での機械照合はあるが、証明の型を疑ってほしい。
- **監査点 C**: **定理 TRI 場合 2** の構成($Q_P/A\cong C_5^3$ を $\mathbb F_5$ 空間として自由に扱う段)。$\Psi(x),\Psi(y),\Psi(c)$ の $V$-成分が $V$ の**基底**であること(階数 3・3 元生成)を使っている。
- **監査点 D**: 系 KQ の一般化(予言 P-SC-2)— 中心的 $\ell$-群による拡大という前件が壁族で本当に成り立つか。
- **申し送り**: 裁定 293 の 3 札判定は、本稿 §6 が正しければ**格下げが要る**。逆に §6 が誤りなら定理 SC/SC′ がそのまま族則候補になる。**どちらに転んでも定理 STR・TRI・KQ は生存する**(規約に依存しない構造定理)。

---

## 12. 格付け表

| 主張 | 格 |
|---|---|
| 定理 STR($Q_P=A\times V$) | **定理**(proof)+ 機械 |
| 補題 CC($\hat c=\mathrm{conj}_\kappa$・$\kappa=(1,4)(2,5)$ 一意) | **定理**(proof)+ 機械 |
| **定理 ORI**($\rho(q)=\hat c(f)^{-1}$) | **定理**(3 行)+ **全 7500 元機械照合** |
| 系 ORI′(粗ラベルの代表非依存性) | **定理**(系) |
| **定理 TRI**(三分) | **定理**(proof)+ 20 行機械一致 |
| **系 KQ**(KER-QUANT) | **candidate → 定理** |
| **定理 SC**(settled $\iff f^{-1}\in\Sigma_m$) | **定理** |
| 系 SC′(この窓で 5 判定式が一致・SETTLED-CENT 的中) | **機械 20/20** + 定理 SC |
| **§6 の混線判定と「整合規約では 20/20」** | **paper-proof candidate**(二経路の議論)+ **機械($T'$ で 20/20)**。**Sol 監査待ち(監査点 A)** |
| 【GAP-PSC-1】= cert の 4/8/8 は artifact | **candidate(強)** — 裁定 293 の格下げを進言 |
| 発案係の $\mathrm{Hol}(\mathbb Z/5)$ 手計算 | **検分 PASS**(§7) |
| 予言 P-SC-0/1/2/3 | **凍結予言**(未測定) |
| $PB_4$ 水準の settled | **UNKNOWN**(LEVEL CAVEAT・本稿は $PB_3$ のみ) |
