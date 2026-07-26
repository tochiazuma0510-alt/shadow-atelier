# S5 紙上設計 — $K^{(5)}$ 標的 dessin(次数 10・種数 2)の明示モデル探索の設計書 v1

2026-07-27 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱**。上位文書: `docs/manifest_k5_v1.md` v1.2(事前登録)・`sol/裁定_29_ben31.md`(工程 ③)・`sol/sol_reply_31_manifest.md` F9(Sol の紙上設計の贈り物)。姉妹文書: `docs/week4-K5_Rule1_v1.md`(凍結 1 候補)。

> ## 接触禁止の宣言(本稿の最重要規律)
>
> **本稿は個別モデル候補・係数の数値・数値近似・database 照会に一切接していない。** 探索コマンドを一度も実行していない。本稿で行った機械計算は **1 本だけ**で、その入力は **既に凍結済みの有限 fixture($G_5$ と標的 $H$ の置換データ)のみ**である(§2.4・scratchpad の `k5_blocks.js`)。曲線・$\lambda$・$u$・局所展開には触れていない。
>
> 本稿は manifest v1.2「現在許可されている工程」= **S5 の紙上設計**の成果物であり、個別モデル探索は**修正版凍結 1(Rule 1)の受理後**に始まる。

---

## 0. 結論(先に 8 行)

1. **divisor 恒等式は係数 ansatz より遥かに強い。** Riemann–Roch により、$(C,P_0,P_\infty)$ を固定した時点で $\lambda$ は**定数倍を除いて一意**に決まる($\ell(10P_\infty-10P_0)=1$)。**$\lambda$ の 9 個の係数は自由変数ではない**(§3.1)。
2. **★ Sol の紙上フィルタ $\operatorname{ord}[P_0-P_\infty]\in\{5,10\}$ は、$\{5\}$ へ半分に絞れる**(命題 S5-1・§2.4)。根拠は幾何でも数論でもなく、**凍結済み有限 fixture の置換群のブロック構造**である。
3. **★ その帰結として $\lambda$ は分解する**: $\boxed{\lambda = c\,\mu^2}$、$\mu:C\to\mathbf P^1$ は**次数 5・monodromy $D_5$**・$(\mu) = 5P_0-5P_\infty$、分岐型 $(5,\ 2^21,\ 2^21,\ 5)$(命題 S5-2)。**探索対象は次数 10 の Belyi 写像ではなく次数 5 の $\mu$ になる。**
4. **変数削減の見積り**: 素朴な係数 ansatz は **未知数 ~20 / 方程式 ~22**(次数 10 の連立)。divisor 第一段で **未知数 4**(3 次元 moduli + スカラー)/ 条件 4。ブロック第二段の正規形で **自由母数 2(Weierstrass 枝)/ 3(非 Weierstrass 枝)**。§3.4 の表。
5. **$\lambda\in\mathbb Q(x)$ は禁止**(Sol F9.2)。さらに $\mu$ の段でも同じ理由で $\boxed{\mu = a(x)+b(x)y,\ b\ne0}$ が必須(§4)。
6. **★★ 漏洩警報(manifest への必須修理提案)**: $\lambda = c\mu^2$ の定数 $c$ について $\boxed{\text{(P1)}\iff c\in K^{\times2}\iff \operatorname{sqfree}(c)\in\{1,-1,5,-5\}}$(命題 S5-4)。すなわち **$c$ の平方類は「$u$ と同値な leading class」であり、Model-Builder が 1 行で封印予測 (P1) を判定できてしまう。** 便 31 F4.3 が抽象的に警告した「$u$ という語を使わずに同値量を計算できる」の**具体例が実在した**。Rule 1 の whitelist に追加を要する(§6.2)。
7. **二 dessin は同一曲線とは限らない**(Sol F9.2)。ただし**両者の有限側 fixture は完全に同型な入力を与える**(§2.4 の機械検査は sq/ns で全項目一致)。同時探索は「共同凍結」の意味であって同一 ansatz の強制ではない。
8. **exact 受理物**は §5 の 8 項目。**数値近似・database label は discovery 用であり証拠でない**(Sol F9.4)。

### 0.1 状態札

| 主張 | 札 |
|---|---|
| §2.1–§2.3(RH・divisor 恒等式・位数 1/2 の排除) | **紙上・Sol F9.1 と一致**(私の独立再証明) |
| **命題 S5-1**($\operatorname{ord} = 5$ ちょうど)・**S5-2**($\lambda = c\mu^2$) | **紙上 + 単系統機械検査**(node のみ・§2.4)。**`two-system cross-checked` ではない** — GAP 側の再現と Sol 監査を要請 |
| §3 の変数削減見積り | **紙上・単系統**。素朴側の本数は上界の概算(§3.4 の注) |
| **命題 S5-3**(正規形 $y^2 = a(x)^2+c_5(x-x_0)^5$) | **紙上・単系統・未監査** |
| **命題 S5-4**((P1) $\iff c\in K^{\times2}$) | **紙上・単系統・未監査**。**運用上は最優先で監査されたい**(漏洩経路の閉塞に直結) |
| §3.5(D₅ ⇒ 巡回五次被覆) | **構造の指摘のみ・実行しない**(scope 宣言) |

---

## 1. 対象の再掲(凍結済み・変更禁止)

`docs/week4-K5橋_D1_opus_v1.md` §4・§8.1 より(二系統 cross-checked):

- $P = G_5\cong\mathbb F_5^3\rtimes C_2^2$(位数 500)、marking $X=\bar x,\ Y=\bar y,\ Z=\bar z$、$XYZ=1$、$\operatorname{ord}(X)=10$。
- 標的 $H\le G_5$: $\lvert H\rvert=50$、$N_{G_5}(H)=H$、$\Lambda = \{H\text{ の }G_5\text{-共役}\}$、$\lvert\Lambda\rvert = 10 = M$。
- $\Lambda$ 上の ordered passport $(\sigma_0,\sigma_1,\sigma_\infty) = (10,\ 2^41^2,\ 10)$、$\sigma_0\sigma_1\sigma_\infty = 1$。
- monodromy 群 $\operatorname{Mon} = G_5/\operatorname{Core}(H)$、位数 **100**、$\operatorname{Core}(H)\cong C_5$。
- $\operatorname{Aut}(W_0/U) = N_{G_5}(H)/H = \mathbf 1$。
- 標的は $G_5$-共役類 **2 つ**($\Lambda_{\rm sq}$: $\alpha\in\{1,4\}$ / $\Lambda_{\rm ns}$: $\alpha\in\{2,3\}$)。**`target_policy = all_two_classes`**。
- $K = \mathbb Q(\zeta_{20})$、$M=10$、$e=5$、$\mathfrak F_0\cong C_5$。

---

## 2. divisor 恒等式を係数 ansatz より先に使う

### 2.1 Riemann–Hurwitz と三つの divisor(Sol F9.1 の再導出)

$$ 2g-2 = 10\cdot(-2) + \underbrace{9}_{\lambda=0} + \underbrace{4}_{\lambda=1} + \underbrace{9}_{\lambda=\infty} = 2,\qquad \boxed{g = 2}. \tag{2.1} $$

$\lambda=0$ と $\lambda=\infty$ の fiber は各々**幾何点 1 個**(分岐指数 10)。1 点集合は $G_{\mathbb Q}$-安定だから、$\mathbb Q$-モデル上で

$$ P_0,\ P_\infty\ \in\ C(\mathbb Q). \tag{2.2} $$

$\lambda=1$ 上の二重点を $Q_1,\dots,Q_4$、単純点を $R_1,R_2$ とすると

$$ (\lambda) = 10P_0-10P_\infty,\qquad (\lambda-1) = 2\textstyle\sum_j Q_j+R_1+R_2-10P_\infty,\qquad (d\lambda) = 9P_0+\textstyle\sum_j Q_j-11P_\infty. \tag{2.3–2.5} $$

次数検算: $0$ / $8+2-10=0$ / $9+4-11 = 2 = 2g-2$ ✓(最後は標準因子)。

### 2.2 これを「先に」使うとは何を意味するか

(2.3) は $\lambda\in L(10P_\infty-10P_0)$ を意味する。**この空間の次元は Riemann–Roch で先に分かる**:

$$ \deg(10P_\infty-10P_0)=0\ \Longrightarrow\ \ell\in\{0,1\},\qquad \ell = 1\iff 10P_0\sim10P_\infty\iff 10\,[P_0-P_\infty]=0. \tag{2.6} $$

すなわち:

> **観測 A(第一段の変数削減).** $(C,P_0,P_\infty)$ を固定し $[P_0-P_\infty]\in J(C)(\mathbb Q)[10]$ が成り立つなら、**$\lambda$ はスカラー倍を除いて一意**である。
> ⇒ **$\lambda$ の係数は独立変数ではない。** 探索すべきは「$\lambda$ の係数」ではなく「**10-torsion 差をもつ二点付き種数 2 曲線**」である。

これが「divisor 恒等式を係数 ansatz より先に使う」の数学的中身である。素朴な ansatz が $\lambda$ に 9 個の係数を割り当てるのに対し、実際の自由度は **0 個 + スカラー 1 個**しかない。

### 2.3 紙上フィルタ $\operatorname{ord}[P_0-P_\infty]\in\{5,10\}$(位数 1 / 2 の排除)

$D := [P_0-P_\infty]\in J(C)(\mathbb Q)$ と置く。(2.6) より $10D = 0$、ゆえに $\operatorname{ord}(D)\mid10$。

- **$\operatorname{ord}(D)\ne1$**: $D=0$ なら $P_0\sim P_\infty$ ゆえ $\ell(P_\infty)\ge2$、すなわち次数 1 の写像 $C\to\mathbf P^1$ が存在して $C\cong\mathbf P^1$。$g=2$ に矛盾。
- **$\operatorname{ord}(D)\ne2$**: $2D=0$ なら $2P_0\sim2P_\infty$、ゆえに $\ell(2P_\infty)=2$ で $\lvert2P_\infty\rvert$ は種数 2 の**唯一の** $g^1_2$(超楕円写像)である。その写像を $h$ とすると $(h) = 2P_0-2P_\infty$ と取れ、$(\lambda) = 5\,(h)$ ゆえ $\lambda/h^5$ は零点も極も持たない ⇒ $\lambda = c\,h^5$。$h$ の deck 変換は超楕円対合 $\iota$ であり、$\iota$ は $\lambda$ を固定する。ゆえに $\operatorname{Aut}(C/\mathbf P^1)\supseteq C_2$ で、$\operatorname{Aut}=1$ に矛盾。

$$ \Longrightarrow\qquad \boxed{\operatorname{ord}[P_0-P_\infty]\in\{5,\ 10\}} \tag{2.7} $$

(Sol F9.1 (9.4) と一致。私の独立再証明。)

### 2.4 ★★ 命題 S5-1 / S5-2 — フィルタを $\{5\}$ に絞り、$\lambda$ を分解する

(2.7) は幾何の議論だけから来ている。**凍結済み有限 fixture の置換群を見ると、さらに強い結論が出る。**

> **補題 S5-B(ブロック構造).** 標的の次数 10 の置換作用($\Lambda$ 上・$\Lambda_{\rm sq}$ と $\Lambda_{\rm ns}$ の**両方**)は、**ちょうど一つ**の非自明なブロック系をもつ:
> $$ \textbf{2 ブロック}\times\textbf{サイズ 5}. $$
> さらに $\sigma_0$ と $\sigma_\infty$ は二つのブロックを**入れ替え**、$\sigma_1$ は各ブロックを**保つ**。

**紙上証明。** $\operatorname{Core}(H)$ を決める。$R=\mathbb F_5^3$ の $C_2^2$-安定部分空間は、三つの指標が相異なるので座標部分空間だけ。$H\cap R = U = \langle e_2,\ \alpha e_1+e_3\rangle$($\alpha\ne0$)に含まれる座標線は $\langle e_2\rangle$ のみ。また $\operatorname{Core}(H)\not\subseteq R$ なら $(v,q_2)\in\operatorname{Core}$ を $e^t$ で共役して $(1-q_2)t$ が $\langle e_1,e_3\rangle$ 全体を走るので $\operatorname{Core}\supseteq\langle e_1,e_3\rangle\not\subseteq U$、矛盾。ゆえに $\operatorname{Core}(H)=\langle e_2\rangle = \langle Y^2\rangle\cong C_5$、$\operatorname{Mon} = M := G_5/\langle e_2\rangle$(位数 100)。

$M = V\rtimes C_2^2$、$V = \langle\bar e_1,\bar e_3\rangle$。$(1-q_1)V=\langle\bar e_3\rangle$, $(1-q_3)V=\langle\bar e_1\rangle$ より $[M,M]=V$、$M^{\rm ab}\cong C_2^2$。点安定化群 $\bar H$(位数 10)を含む中間群 $\bar H\le \mathcal K\le M$ を数える:

- $\lvert\mathcal K\rvert=20$: $\lvert\mathcal K\cap V\rvert=5$ かつ $\mathcal K V/V=C_2^2$ が必要。$\mathcal K\cap V$ は $\mathcal K$ で正規ゆえ $q_1$-安定でなければならないが、$\mathcal K\cap V\supseteq\bar U=\langle\alpha\bar e_1+\bar e_3\rangle$ で $q_1(\alpha\bar e_1+\bar e_3) = \alpha\bar e_1-\bar e_3$、これが $\bar U$ に入るのは $2\alpha=0$ すなわち $\alpha=0$ のときだけ。$\alpha\ne0$(good の条件)に矛盾。**⇒ 存在しない。**
- $\lvert\mathcal K\rvert=50$: $\mathcal K = V\rtimes\langle q\rangle$ で $q_2$ を含む必要 ⇒ $\mathcal K = V\rtimes\langle q_2\rangle$ **ちょうど 1 個**。

ブロック系 ↔ 中間群だから、非自明なブロック系はサイズ 5 のもの 1 つだけ。$X\mapsto q_1\notin\langle q_2\rangle$、$Z\mapsto q_3\notin\langle q_2\rangle$、$Y\mapsto q_2$ ゆえ入替/保存も従う。∎

**機械検査(単系統・node)**: `scratchpad/k5_blocks.js`(全 $2^{10}$ 部分集合をブロック判定で悉皆)。$\alpha=1$($\Lambda_{\rm sq}$)と $\alpha=2$($\Lambda_{\rm ns}$)の両方で

```
|H| = 50 / |N_G(H)| = 50 / |Lambda| = 10
cycle types = 10 / 2.2.2.2.1.1 / 10 ,  sX o sY o sZ = id : true
|Core(H)| = 5  -> |Mon| = 100 ,  Core(H) = <e_2>
nontrivial blocks containing point 0: {0,2,4,6,8}      (ちょうど 1 系・サイズ 5)
sX swaps blocks? true | sY swaps? false | sZ swaps? true
deg-5 types: sX^2|B = 5   sY|B = 2.2.1   sZ^2|B = 5
|<sX^2,sY,sZ^2>| on 5 points = 10        (= D_5)
```

**D1 §4・§8.1 の二系統値をすべて再現したうえで**、新規項目(ブロック・$D_5$)を追加した。**新規項目は単系統である。**

> **命題 S5-2(分解).** 標的の被覆 $W_0\to\mathbf P^1_\lambda$ は
> $$ C\ \xrightarrow{\ \mu\ (\deg 5)\ }\ Y\ \xrightarrow{\ \deg 2\ }\ \mathbf P^1_\lambda $$
> と一意に分解し、$Y\cong\mathbf P^1_{\mathbb Q}$、第二の写像は $\mathbb Q$-座標で $\lambda = c\,\mu^2$($c\in\mathbb Q^\times$)である。

**証明。** 補題 S5-B の唯一のブロック系が中間被覆 $Y$ を与える($\deg(Y/\mathbf P^1)=$ ブロック数 $=2$)。$Y\to\mathbf P^1_\lambda$ が分岐するのは $\sigma_i$ がブロックを入れ替える点、すなわち $\lambda=0,\infty$ のちょうど 2 点。Riemann–Hurwitz より $2g_Y-2 = 2(-2)+1+1 = -2$、$g_Y=0$。ブロック系は**一意**ゆえ $G_{\mathbb Q}$-安定で、$Y$ は $\mathbb Q$ 上へ降下する。$\lambda=0$ 上の $Y$ の点は 1 点で $\mathbb Q$-有理、ゆえに $Y\cong\mathbf P^1_{\mathbb Q}$。$\lambda=0,\infty$ で全分岐する $\mathbb Q$-有理な次数 2 写像は、適当な $\mathbb Q$-座標 $\mu$ で $\lambda = c\mu^2$($c\in\mathbb Q^\times$)。∎

> **命題 S5-1(フィルタの半減).** 標的では
> $$ \boxed{\ \operatorname{ord}[P_0-P_\infty] = 5\quad\text{ちょうど}\ } $$

**証明。** $\lambda = c\mu^2$ で $\lambda$ は $P_0$ で 10 位の零、$P_\infty$ で 10 位の極。$t\mapsto ct^2$ は $t=0,\infty$ で 2 位に分岐するから $\operatorname{ord}_{P_0}(\mu)=5$, $\operatorname{ord}_{P_\infty}(\mu)=-5$、しかも $\mu$ の零・極は他にない。ゆえに $(\mu) = 5P_0-5P_\infty$ で $5D=0$。§2.3 より $D\ne0$、$5$ は素数ゆえ $\operatorname{ord}(D)=5$。∎

> **系 S5-2a($\mu$ の分岐データ).** $\mu:C\to\mathbf P^1$ は次数 5・monodromy 群 $D_5$(5 点上の自然作用)で、分岐は
> $$ \{0,\ s,\ -s,\ \infty\}\quad(s^2 = 1/c),\qquad \text{局所型}\ (5,\ 2^21,\ 2^21,\ 5). $$
> 検算: $\sum(e-1) = 4+2+2+4 = 12 = 2g-2+2\deg\mu = 2+10$ ✓。$D_5$ の 5 点作用では回転が 5-巡回、鏡映が $2^21$ — 型が自動的に整合する。

**この 3 つが、Sol F9.1 の贈り物を最大限まで使い切った形である。**

---

## 3. 変数削減の見積り

### 3.1 第一段 — $\lambda$ の係数を消す(観測 A)

§2.2 の通り。$(C,P_0,P_\infty)$ + torsion 条件を先に据えれば $\lambda$ は自動。次元:

$$ \dim\mathcal M_{2,2} = 3+2 = 5,\qquad 5\ \text{torsion 条件は余次元 }2\ (\dim J = 2)\ \Longrightarrow\ \dim = 3. $$

これに $\lambda$ のスカラー 1 を足して **4 母数**。切る条件は「$\lambda$ の 4 個の残余分岐点がすべて同一値」= 3 条件 +「その値を 1 にする」= 1 条件、計 **4 条件**。$4-4=0$ ✓ — **rigid(Hurwitz 空間 0 次元)であることと整合**する。

### 3.2 第二段 — $\lambda$ でなく $\mu$ を探す(命題 S5-2)

$$ \ell(10P_\infty) = 9\quad\text{に対し}\quad \ell(5P_\infty) = 4. $$

素朴 ansatz が $\lambda$ に割り当てる 9 係数は、$\mu$ の **4 係数**に落ちる。しかも $\lambda = c\mu^2$ ゆえ $\lambda$ の 9 係数は $\mu$ の 4 係数の**二次式**として自動生成される。

### 3.3 命題 S5-3 — 正規形(二枝)

$\mu\notin\mathbb Q(x)$(§4)なので $\mu = a(x)+b(x)y$、$b\ne0$。$\nu:=\mu\circ\iota = a-by$ と置くと

$$ \mu+\nu = 2a(x)\in\mathbb Q(x),\qquad N:=\mu\nu = a^2-b^2f\in\mathbb Q(x),\qquad \operatorname{div}_0(N) = 5P_0+5\iota P_0 . $$

$N$ は $\mathbf P^1_x$ 上の関数で、その零因子は $x^*(x_0)$ の 5 倍。ゆえに

$$ \boxed{\ N = a(x)^2-b(x)^2f(x) = c_5\,(x-x_0)^5\ }\qquad(x_0 := x(P_0)). \tag{3.1} $$

> **枝 (W): $P_\infty$ が Weierstrass 点**($y^2=f_5(x)$、$P_\infty=\infty$)。$\operatorname{ord}_{P_\infty}(x)=-2,\ \operatorname{ord}(y)=-5$ ゆえ $L(5P_\infty)=\langle1,x,x^2,y\rangle$、$\deg a\le2$, $b = b_0$ 定数。(3.1) の $x^5$ の係数を見て $c_5 = -b_0^2\lambda_f$($\lambda_f$ = $f$ の主係数)。$y$ を再スケールして $b_0=1$、$f$ をモニックに取れば
> $$ \boxed{\ C:\ y^2 = a(x)^2 + c_5\,(x-x_0)^5,\qquad \mu = a(x)+y,\qquad \deg a\le2\ } \tag{3.2} $$
> **母数は $(a_0,a_1,a_2,c_5,x_0)$ の 5 個。** $x$-平行移動で $x_0=0$、$x$-スケールと $\mu$-スケール(重み付き $\mathbb G_m$: $(a,c_5)\mapsto(ta,t^2c_5)$)で 2 個落ちて **正味 2 母数**。
>
> **枝 (N): $P_\infty$ が Weierstrass 点でない**($y^2=f_6(x)$、$P_\infty=\infty_+$)。$\mu+\nu$ は $\infty_\pm$ の両方で 5 位の極 ⇒ $\deg a = 5$;$\mu-\nu = 2by$ も同様で $b = p_2(x)$($\deg p_2 = 2$)。(3.1) は
> $$ a(x)^2 - c_5(x-x_0)^5 = f_6(x)\,p_2(x)^2 \tag{3.3} $$
> となり、**次数 10 の多項式 $a^2-c_5(x-x_0)^5$ が二重根を 2 個もつ**という条件になる。母数 $(a:6,\ c_5,\ x_0) = 8$、正規化 3 個、条件 2 個 ⇒ **正味 3 母数**。

**枝の次元が違う** — (W) は (N) の中の余次元 1 の軌跡である($\dim\mathcal M_{2,2}$ で $P_\infty$ を Weierstrass 点に限ると $5\to4$、torsion 2 を引いて $2$)。

> **【GAP-S5a】どちらの枝かは紙上で決まっていない。** 次元の一般性からは **(N) が期待される**が、これは**発見的**であって証明ではない(解は 0 次元なので余次元 1 の軌跡上にあってもよい)。**Rule 1 は両枝を先に書く**(`docs/week4-K5_Rule1_v1.md` §3・§5)。$P_0$ の Weierstrass 性についても同様(枝 (W) では $a(x_0)=0\iff P_0$ が Weierstrass)。

### 3.4 見積り表

| 段 | 未知数 | 方程式 | 備考 |
|---|---|---|---|
| **素朴**(枝 (W) で $\lambda$ を直接) | $f_5$: 6、$A$: 6、$B$: 3、$x_0,\hat c$: 2、$\lambda=1$ 側の $h,k$: 6 ⇒ **~20**(正規化 3 を引いて ~17) | $A^2-B^2f = \hat c(x-x_0)^{10}$: 11 本、$(A-1)^2-B^2f = \hat c\,h^2k$: 11 本 ⇒ **~22** | 係数次数 10 の連立。**Gröbner 非現実的**(この規模は 8GB 機で通らない) |
| **第一段**(divisor) | 3(moduli)+ 1(スカラー)= **4** | 4 | $\lambda$ の 9 係数が消える。torsion 条件は Mumford 演算で判定(消去法でない) |
| **第二段**(ブロック・命題 S5-3) | 枝 (W): **2**、枝 (N): **3** | 分岐型 $(5,2^21,2^21,5)$ + 調和条件 | $\mu$ の係数 4(枝 (W) では $a$ の 3 + $b_0$)。**方程式の次数も 10 → 5 に落ちる** |
| **第三段**(§3.5・**着手しない**) | 巡回五次被覆の分岐指数 $(n_1,\dots,n_4)\in(\mathbb Z/5)^4$ の**有限個** | — | 連続母数がほぼ消える |

> **注(誠実な但し書き)**: 「素朴」欄の本数は**上界の概算**である。$\iota$-対称性による冗長性を除けば実効本数は減る。主張は「桁が違う」ことであって、正確な Gröbner 複雑度ではない。**第一段・第二段の未知数は正確**(Riemann–Roch と正規形から)。

### 3.5 第三段(構造の指摘のみ・本稿では着手しない)

系 S5-2a より $\operatorname{Mon}(\mu)\cong D_5$。ゆえに $C\to\mathbf P^1_\mu$ は**二面体的五次被覆**であり、その Galois 閉包 $\tilde C$($\deg 10$、$g=4$)は

$$ \tilde C\ \longrightarrow\ \tilde C/C_5\ \longrightarrow\ \mathbf P^1_\mu $$

を経由し、$\tilde C/C_5$ は $\{s,-s\}$ の 2 点でのみ分岐する次数 2 被覆ゆえ $\cong\mathbf P^1$。したがって **$\tilde C$ は $\mathbf P^1$ の巡回 5 次(superelliptic)被覆 $v^5 = \prod_{i}(w-w_i)^{n_i}$ であり、$C = \tilde C/\langle\text{鏡映}\rangle$**。

> **scope 宣言**: この還元は「探索を有限の指数選択に帰着させる」という意味で第二段よりさらに強い。しかし**これ以上進めると個別モデルの構成そのものになる**ため、**本稿では指数 $(n_i)$ の決定も $w$-座標の正規化も行わない**。Rule 1 受理後の Model-Builder の作業とする。**司令塔・Sol へ**: この第三段を S5 の作業指示に含めるか(含めると探索は劇的に軽くなるが、Rule 1 の正規形規則を第三段の座標で書き直す必要がある)を裁定されたい(§7 論点 1)。

---

## 4. ansatz の必須形 — $B\ne0$(Sol F9.2)と、その $\mu$ 版

> **補題 S5-H.** $\lambda\notin\mathbb Q(x)$。さらに $\mu\notin\mathbb Q(x)$。

**証明。** $\lambda\in\mathbb Q(x)$ なら $\lambda$ は超楕円写像 $x$ を経由するので $\lambda\circ\iota=\lambda$、すなわち $\iota\in\operatorname{Aut}(C/\mathbf P^1_\lambda)$。$\operatorname{Aut}=1$ に矛盾。$\mu\in\mathbb Q(x)$ なら $\lambda = c\mu^2\in\mathbb Q(x)$ で同じ矛盾。∎

$$ \Longrightarrow\qquad \boxed{\ \lambda = A(x)+B(x)y,\ B\ne0\ }\qquad\text{かつ}\qquad \boxed{\ \mu = a(x)+b(x)y,\ b\ne0\ } \tag{4.1} $$

$\lambda = c\mu^2 = c\bigl(a^2+b^2f\bigr) + 2cab\,y$ なので $A = c(a^2+b^2f)$, $B = 2cab$。**$B\ne0$ は $b\ne0$ かつ $a\ne0$ を要求する**($a=0$ なら $\mu = by$ で $\mu^2\in\mathbb Q(x)$、上と同じ矛盾)。

> **★ 教材候補 1**: 「$\operatorname{Aut}=1$ ゆえ $\lambda\notin\mathbb Q(x)$」は、**分解 $\lambda=c\mu^2$ を見つけたあとも消えない**。分解は $\mathbf P^1_\lambda$ 側の話で、超楕円対合は $C$ 側の話だから、二つは独立である。$\mu$ が「$x$ の関数でない」ことを毎回確認せよ。

---

## 5. exact 受理物の一覧(Sol F9.4)

**凍結 2 に入れてよいのは、次の 8 項目が exact に閉じたものだけである。**

| # | 受理物 | 形式 |
|---|---|---|
| A1 | **曲線方程式** $C/\mathbb Q$ | $\mathbb Q$-係数の明示式(§3.3 の正規形・Rule 1 §3 の全順序で一意化) |
| A2 | **Belyi 写像** $\lambda$ | $\mathbb Q(C)$ の元としての明示式。$\lambda = c\mu^2$ の分解形も併記(**ただし §6.2 の警報を参照**) |
| A3 | **divisor 恒等式** (2.3)(2.4)(2.5) | 各点の座標つき。**成立の exact 証明**(数値評価でない) |
| A4 | **種数・分岐型** | $g=2$、passport $(10,2^41^2,10)$ の exact 検証 |
| A5 | **monodromy 群と exact conjugator** | $(\sigma_0,\sigma_1,\sigma_\infty)\in S_{10}^3$ と、標的三つ組への**明示置換**(**一意** — 補題 S5-U・下記) |
| A6 | $\operatorname{Aut}(C/\mathbf P^1)=1$ | exact 証明(数値的な「見つからなかった」は不可) |
| A7 | $P_0,\ P_\infty$ と **uniformizer $t$** | $\mathbb Q$-有理点の明示座標 + Rule 1 §5 のアルゴリズムが返した $t$ の式 |
| A8 | **$\operatorname{ord}[P_0-P_\infty]=5$ の exact 検証** | 命題 S5-1 の独立確認(Jacobian 上の exact 演算)。**不一致なら integrity stop** |

> **補題 S5-U(exact conjugator の一意性).** $\operatorname{Aut}(W_0/U)=1$ ゆえ $C_{S_{10}}(\operatorname{Mon})\cong N_{\operatorname{Mon}}(\text{点安定化群})/(\text{点安定化群}) = N_{G_5}(H)/H = 1$。したがって幾何 fiber と $\Lambda$ の間の、monodromy を intertwine する全単射は**ちょうど一つ**。**A5 に tie-break は不要**である。

**受理しないもの(discovery 用であり証拠でない)**: 数値近似(浮動小数点の根・数値 monodromy)、database label(LMFDB 等)、「探索して見つからなかった」型の否定、他窓($K^{(3)}$・$A_5$)からの類推。

---

## 6. 探索戦略と、その最中に守るべきこと

### 6.1 推奨する探索順序(Rule 1 受理後)

1. **枝の決定**: $P_\infty$(および $P_0$)の Weierstrass 性を intrinsic に判定($\ell(2P_\infty)=2$ か)。両枝を**同時に**走らせる(片枝で見つからないことは非存在の証明でない)。
2. **正規形 (3.2)/(3.3) の 2–3 母数**を、$\mu$ の分岐条件(型 $(5,2^21,2^21,5)$ + 分岐点が $\{0,\pm s,\infty\}$ = **調和条件**)で切る。
3. **exact に閉じる**(A1–A8)。**この段階まで $u$ に触れない。**
4. 両 dessin(sq/ns)を **atomic joint freeze**(凍結 2)。**片翼だけで Extractor を起動しない。**
5. 発射錠のあとに Extractor(B)が $u$ 二経路(Rule 1 §6)。

### 6.2 ★★ 漏洩警報 — $c$ の平方類は $u$ と同値である(命題 S5-4)

> **命題 S5-4.** $\lambda=c\mu^2$、$\mu = v\,t^5+O(t^6)$($t$ は $P_0$ の $K$-有理 uniformizer)とすると $u = c\,v^2$。ゆえに
> $$ \boxed{\ \text{(P1)}\ \operatorname{ord}\bigl([u^{-1}]_{10}\bigr)\in\{1,5\}\ \iff\ c\in K^{\times2}\ \iff\ \operatorname{sqfree}(c)\in\{1,\,-1,\,5,\,-5\}\ } $$
> ($c\in\mathbb Q^\times$・$K=\mathbb Q(\zeta_{20})$ の二次部分体は $\mathbb Q(i),\mathbb Q(\sqrt5),\mathbb Q(\sqrt{-5})$ の 3 つ)。

**証明。** $\lambda = c\mu^2 = c v^2t^{10}(1+O(t))$ ゆえ $u = cv^2$。(P1) $\iff u^5\in K^{\times10}$。$u^5 = c^5v^{10}$ で $v^{10}\in K^{\times10}$ ゆえ $\iff c^5\in K^{\times10}$。$c^5=d^{10}\iff(c/d^2)^5=1\iff c/d^2\in\mu_5(K)$、そして $\mu_5\subseteq K^{\times2}$($\zeta=(\zeta^3)^2$)ゆえ $\iff c\in K^{\times2}$。逆は $c=e^2\Rightarrow u=(ev)^2\Rightarrow u^5=(ev)^{10}$。最後の同値は $\mathbb Q^\times\cap K^{\times2}$ が $K$ の二次部分体で決まることから。∎

> **★ これが意味すること(必須修理の提案)。**
> 便 31 F4.3 / 裁定 29-5 の whitelist は「許可: 明示モデル・**Belyi map**・…/ 禁止: $\lambda/t^{10}$ の非零定数項とその同値物」と書く。ところが **Belyi map の出力そのものに含まれる定数 $c$ の平方因子を 1 行で計算するだけで、封印予測 (P1) の真偽が決まってしまう。** これは W5(「二つの抽出器の一致」と「Kummer 類の等号証明」は別ゲート)ともまた別の、**whitelist 内部の抜け穴**である。
>
> **提案(manifest v1.3 / Rule 1 への追加)**:
> - **(L1)** Model-Builder(A)の禁止項目に「$\lambda$ の分解 $\lambda = c\mu^2$ における $c$ の**平方類・平方因子・符号**を計算すること、およびそれを候補選択に使うこと」を明記する。
> - **(L2)** A が $\lambda$ を出力すること自体は不可避なので、**A の出力形式を「$\lambda$ の完全な式」に固定**し、$c$ を分離した形($c$ と $\mu$ の対)で報告することを**禁止**する(分離した瞬間に (P1) が読める)。
> - **(L3)** 逆に、これは **(P1) を「実行可能な exact 判定」に格上げする**朗報でもある。凍結 2 のあと、Extractor(B)は $u$ の 10 次展開を待たずに $\operatorname{sqfree}(c)$ の 1 行で (P1) を**閉じられる**。**(P1) の証明書型として (L3) を Rule 1 §7 に登録する**(cusp 展開経路の独立な裏取りになる)。
> - **(L4)** 同型の抜け穴が他にないかの点検: $u=cv^2$ の $v$ 側は? $v$ は局所展開の量なので whitelist ですでに禁止側にある。$c$ だけが「大域的な模型データ」の顔をして通っていた。
>
> **★ 教材候補 2**: **「局所量の禁止」は、大域量が局所量の一部を決めるときに漏れる。** $u$ は局所係数だが、$\lambda$ の分解定数 $c$ という**大域データ**が $u$ の**平方類**を決めていた。禁止リストは「量の出自(局所/大域)」でなく「**封印予測のどのビットを決めるか**」で書かねばならない。

---

## 7. 論点(便 32 / 司令塔裁定へ)

1. **第三段(§3.5・$D_5$ ⇒ 巡回五次被覆)を S5 の作業指示に含めるか。** 含めれば探索は劇的に軽くなる(連続母数がほぼ消える)が、Rule 1 の正規形規則を $\tilde C$ の座標で書き直す必要があり、**凍結 1 の再起草**になる。私は「含めるべきだが、Rule 1 v1 は $(C,\lambda)$ の座標で凍結し、第三段は**発見の補助**としてのみ使う(受理物 A1–A8 は必ず $(C,\lambda)$ で書く)」が安全だと見ている。
2. **命題 S5-1/S5-2 の監査。** 単系統(node)である。**GAP での再現**(`ConjugacyClassesSubgroups` からの中間群列挙で「$\bar H$ を含む中間群は $\lvert\mathcal K\rvert=50$ の 1 個だけ」を独立に確認)を implementer へ発注すべきか。私はすべきだと考える — **これは探索空間を半分にする load-bearing な主張**である。
3. **命題 S5-4 と (L1)–(L3) の採否。** とくに **(L2)**(出力形式の固定)は Model-Builder の作業を不自然に縛る可能性がある。代案として「A は $\lambda = c\mu^2$ の分解を出力してよいが、$c$ の**平方因子分解を行わない**ことを申告し、access log で担保する」も考えられる。Sol の意見を求めたい。
4. **$P_0$/$P_\infty$ の Weierstrass 性(【GAP-S5a】)を紙上で決められるか。** 私は決められなかった(次元の一般性からは (N) が期待される、という発見的議論しかない)。$5$-torsion 点 $[P_0-P_\infty]$ と超楕円対合の相互作用に、私が見落としている制約はないか。
5. **【文献要請】**(文献ゲート・要請駆動): 「**種数 2・$\mathbb Q$ 上・$J(\mathbb Q)$ に位数 5 の点をもち、その点が二つの $\mathbb Q$-有理点の差 $[P_0-P_\infty]$ で表される曲線族**」の明示パラメトリゼーションが文献にあれば、§3.3 の正規形 (3.2)/(3.3) の独立な裏取りになる(私の導出は単系統)。欲しい結果の型: **$X_1(5)$ 類似のモジュラー的パラメトリゼーション、または「$P_0-P_\infty$ が $n$-torsion」条件の Mumford 表現による明示方程式**。降ろされた場合でも **§3.3 は自前導出を正本とし、文献は照合にのみ使う**(降下の轍を踏まない)。

---

## 8. 検算と出所

- 機械検査 1 本: `scratchpad/k5_blocks.js`(node・自己完結・$G_5$ を $(v,q)$ 座標で自前実装)。入力は凍結済み有限 fixture のみ。**D1 §4/§8.1 の二系統既知値(|H|=50・|N|=50・|Λ|=10・passport・$\sigma_0\sigma_1\sigma_\infty=1$・$\lvert\operatorname{Core}\rvert=5$・$\lvert\operatorname{Mon}\rvert=100$)をすべて再現**したうえで、新規項目(ブロック系の一意性・$D_5$)を得た。
- **新規項目は単系統**。`two-system cross-checked` を名乗らない。`verified`(Lean)でもない。
- 曲線・$\lambda$・$u$・数値近似・database には一切接触していない。
