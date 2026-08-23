# M3(E[4] レーン)— 残問 2 ビットの判定

`DIR: 判定(全 YES = 窓水準全射(算術飽和)/ NO = 非算術元の明示 = B3-証人型候補)/ FRAME: B₃-gentle 窓 × 楕円被覆(E=27a3)`

**状態札**: `mixed — §2(定理 L2-LIFT)= 定理(自前証明・機械入力 2 点に載荷)/ §3(ℚ(E[4]) の決定)= 定理(自前・2 経路一致・機械非依存)/ §4-§6(ビット判定と帰結)= 定理(上記 2 つ+実測に相対)/ 全体の格 = candidate(独立照合器なし・Sol 監査前・verified ではない)/ 封印非接触`

- 起草: 影工房 数学者(Claude / Opus 5)・2026-08-23
- 委嘱: 司令塔(83 窓線 M3 = memo §7.6 の発注 M3・レーン EC-83)
- 正典: `docs/week1-定義ノート.md` / 2401.06870 / 2405.11725
- 前提の正本: `scratchpad/gt_grt_dictionary_memo_v1.md` **§8**(便 156 訂正後の逐語 (S1′)(S3′)(S7′))・`sol/sol_reply_156_c3lift.md` §2(幾何鎖の作法)・`provenance/CLAIMS.md` C-15「便 156 反映」節
- 用語: `docs/notes/用語改定_fake型証人型_20260823.md` に準拠(旧 A 型/B 型は使わない)

---

## §0 裁定サマリ(4 行 + 一枚)

| 項目 | 裁定 | 一言 |
|---|---|---|
| **(i) L₂ ↔ E[4] の定式化** | **定理 L2-LIFT**(自前証明・candidate) | $P^{\rm ab}=P/[P,P]\ \cong\ E[4]$ **as $G_\mathbb{Q}$-加群**。C3-LIFT の mod-4 版で、同じ localization sequence を使い**分裂は使わない**。機械入力は 2 点だけ($\lvert P^{\rm ab}\rvert=16\cong(\mathbb Z/4)^2$・$x^3,y^3,z^3\in[P,P]$)。**$\Phi(P)$ を直接扱う必要はなかった** — 正しい L₂ 対象は $P^{\rm ab}$ である。 |
| **(ii) ビット 1** | ★**YES**(candidate) | $\ker(\Theta\vert_{H_0})$ の生成元 $t$ は **$P^{\rm ab}$ 上ちょうど $-1$(反転)**として作用する(実測・3 レコード一致)。他方 **$[\mathbb Q(E[4]):\mathbb Q]=24$**(自前 2 経路)・$\mathbb Q(E[4])\cap\mathbb Q(\zeta_{24})=\mathbb Q(\zeta_{12})$ より $\rho_{E,4}(G_{\mathbb Q(\zeta_{24})})=\ker(N_{K/\mathbb Q})=\langle\zeta_3\rangle\times\{\pm1\}\ni-1$。⟹ **$t$ は算術的**。 |
| **(iii) ビット 2** | ★**YES**(幾何・楕円曲線を一切使わない 2 行) | $\chi$ 全射 ⟹ $\exists g,\ \chi(g)\equiv13\ (\mathrm{mod}\ 24)$ ⟹ $m_g\equiv6\ (\mathrm{mod}\ 12)$。**$m=6$ 層は無条件に算術元をもつ。** ⟹ $\lvert A\rvert=2\lvert A_0\rvert$。 |
| **(iv) 帰結** | ★★**窓水準全射(算術飽和)** | $A=\ker\chi_{\rm vir}$(位数 12)・$\lvert\mathrm{Im}(\mathrm{Ih}_N)\rvert=48$ ⟹ $\boxed{\mathrm{Im}(\mathrm{Ih}_N)=GT(N)}$(両窓)。**18 候補 → 0**。さらに閉じた形: $\boxed{GT(N)\ \cong\ \mathrm{Gal}\bigl(\mathbb Q(\zeta_{24},E[4])/\mathbb Q\bigr)}$(次数 48)。 |

> ★**本ノートの一行**: 83 窓の全 48 shadow は算術的である(candidate)。したがって **83 線は「反例路」ではなく「算術飽和」側で閉じる** — **B3-証人型候補はこの窓からは出ない**。RES-1 の予測(「$L_2$ でしか進めない」)は正しく、$L_2$ はちょうど $E[4]$ だった。

> **格の限界(先に書く)**: 全て **candidate**。(a) 機械入力は本ノート 1 系統(**独立照合器が要る**)。(b) L2-LIFT の幾何鎖は C3-LIFT の mod-4 版で、**Sol 監査は未了**(§8【GAP-L2-1】)。(c) 「窓水準全射」は **$\widehat{GT}_{\rm gen}$ 水準の全射性でも井原予想でもない** — 有限窓 $N$ 一点での言明である。(d) `verified` ではない。`cross-checked` でもない(1 系統)。

---

## §1 記法・入力・前件

### 1.1 記法(正典どおり)
$B_3=\langle\sigma_1,\sigma_2\rangle$、$x=\sigma_1^2,\ y=\sigma_2^2,\ z=(xy)^{-1},\ \Delta=\sigma_1\sigma_2\sigma_1,\ c=\Delta^2$。$N\in\mathrm{NFI}_{PB_3}(B_3)$、$G=F_2/N_{F_2}$、$P=[G,G]$、$N_{\rm ord}=\mathrm{lcm}(\mathrm{ord}\,\bar x,\mathrm{ord}\,\bar y,\mathrm{ord}\,\bar c)$。
$\mathrm{Ih}(g)=((\chi(g)-1)/2,\ f_g)$(2405 (1.5))、$\mathrm{Ih}_N=PR_N\circ\mathrm{Ih}$(同 (1.11))、$\chi_{\rm vir}([m,f])=2m+1$。
本ノートの窓 = $N\in\{[1152,154161],[1152,154163]\}$(DEEP15 の 3 レコード)。$\lvert G\rvert=192$、$G^{\rm ab}=C_3$、$\lvert P\rvert=64$、$N_{\rm ord}=12$、$\lvert GT(N)\rvert=48$、$\lvert\ker\chi_{\rm vir}\rvert=12$($m$ 分布 $\{0:6,6:6\}$)。

$K:=\mathbb Q(\zeta_3)=\mathbb Q(\sqrt{-3})$、$\mathcal O:=\mathbb Z[\zeta_3]$、$\omega:=\zeta_3$、$\alpha:=\sqrt[3]{2}$(実根)。
$E:\ Y^2=X^3+16$($\cong y^2+y=x^3$、LMFDB **27a3**、$j=0$、CM by $\mathcal O$)、$S=\{O,T,-T\}$、$T=(0,4)$、$U_3=E\setminus S$。

### 1.2 前件(凍結・本ノートは再証明しない)
- **(A1)** 便 156 §8.1–8.2 の幾何鎖(逐語 = memo §8.7 (S1′)): $\widehat R\cong\hat\pi_1(U_3,\bar{\mathbb Q})$(標準 tangential base point とその lift を一つ選んだ同型・選択変更に対し同型)、$\widehat R$ は $G_\mathbb{Q}$-安定($q\circ\varphi_g=(\chi(g)\bmod3)q$)、ℚ 上の deck 群は $\mu_3$、被覆式 $w^3=t(1-t)$ が ℚ 上にあるので ℚ-構造は循環論法なしに明示。
- **(A2)** $G_\mathbb{Q}$-同変 localization sequence(便 156 §8.2): 任意の $n$ に対し
  $$0\ \to\ W_n\ \to\ H_1(U_3;\mathbb Z/n)\ \to\ H_1(E;\mathbb Z/n)=E[n]\ \to\ 0,\qquad W_n\cong\widetilde H_0(S;\mathbb Z/n)(1)\cong(\mathbb Z/n(1))^{2}.$$
  $W_n$ は 3 尖点の inertia class(= $x^3,y^3,z^3$ の像)で張られ、関係は 1 本。**分裂は主張しない。**
  （$n=2$ では $\mathbb F_2(1)=\mathbb F_2$ ゆえ $W_2$ は自明加群。$n=4$ では $W_4\cong\mu_4^{\oplus2}$ で**自明ではない** — 本ノートは $W_4$ の Galois 構造を一切使わない。）
- **(A3)** settled/isolated: $N_{F_2}$ は Ihara 作用で安定、$GT(N)$ は群、$\mathrm{Ih}_N$ は準同型(2401 Prop 3.8/3.14)。ゆえに $\rho_N:G_\mathbb{Q}\to\mathrm{Aut}(G)$ が well-defined で、$P$ とその特性部分群はすべて $G_\mathbb{Q}$-加群。
- **(A4)** (P2) $\chi_{{\rm vir},N}\circ\mathrm{Ih}_N=\hat P_{N_{\rm ord}}\circ\chi$、$\chi:G_\mathbb{Q}\to\hat{\mathbb Z}^\times$ 全射。
- **(A5)** (P3) arithmetical ⟹ genuine ⟹ charming(2405 §1.3.1)。genuine ⟹ **全細分 $K\le N$ で生存**(2401 Cor 5.4・便 156 §8.3 の射程訂正済)。
- **(A6)** 定理 **C3-LIFT**(memo §8.7 (S1′)・Sol 便 156 で条件解消・candidate): $P/\Phi(P)\cong E[2]$、$\mathbb Q(E[2])=\mathbb Q(\zeta_3,\sqrt[3]2)$、$\mathrm{Gal}\cong S_3$。
- **(A7)** 定理 **T-ARITH**(memo §8.7 (S3′)・candidate): $R_N(\mathcal T)\subseteq\mathrm{Im}(\mathrm{Ih}_N)$、$H_0=\ker\mu$ は位数 6、$R_N(\mathcal T)$ はその唯一の Sylow 3。
- **(A8)** 定理 **RES-1**(memo §7.2): $\Theta(A)=\Theta(\ker\chi_{\rm vir})=C_3$ — 層 1 は算術で飽和、改善には $L_2$ が要る。

### 1.3 本ノートの機械入力(すべて §7 の 3 スクリプト・W-1 fail-closed assert つき)
| 記号 | 値(3 レコード完全一致) | 使う場所 |
|---|---|---|
| **(M1)** | $P^{\rm ab}=P/[P,P]$ の不変量 $=[4,4]$、$\lvert P^{\rm ab}\rvert=16$ | L2-LIFT |
| **(M2)** | $x^3,y^3,z^3\in[P,P]$(3 つとも)、$\langle x^3,y^3,z^3\rangle^G=[P,P]$(位数 4) | L2-LIFT |
| **(M3)** | $\theta_t$($t=\ker(\Theta\vert_{H_0})$ の非単位元)は $P^{\rm ab}$ 上 **反転 $v\mapsto v^{-1}$** | ビット 1 |
| **(M4)** | $\Theta_{\rm ab}:\ker\chi_{\rm vir}\to\mathrm{Aut}(P^{\rm ab})$ の像 $=\{\pm A^j\}_{j=0,1,2}$(位数 6)、$H_0$ 上単射 | ビット 1 |
| **(M5)** | $\Psi:GT(N)\to\mathrm{Aut}(P^{\rm ab})$ は像 24・核 2 | (iv) |
| **(M6)** | $\lvert\mathrm{Aut}(P^{\rm ab})\rvert=96$、$\lvert C(\mathrm{Ad}\bar x)\rvert=12$、$\lvert N(\langle\mathrm{Ad}\bar x\rangle)\rvert=24$ | canary |

---

## §2 (i) 定理 L2-LIFT — $L_2$ 層 ↔ $E[4]$ の定式化

### 2.1 「$L_2$ 層」の正しい対象は $\Phi(P)$ ではなく $P^{\rm ab}$ である

memo §7.6 の層の梯子は $L_2=\Phi(P)$(位数 16)と書いていた。**これは対象の取り方としては不便で、正しい相手は $P^{\rm ab}=P/[P,P]$(位数 16)である。** 理由:

- $\Phi(P)=[P,P]P^2$ は $P$ の**部分**群だが、$G_\mathbb{Q}$-加群として $E[4]$ と比べる自然な射は**商**の側にある(被覆の $H_1$ は商として現れる)。
- 実測(M1)(M2)より $P^4\subseteq[P,P]$ かつ $[P,P]=\langle\text{尖点}\rangle^G$(位数 4)であり、
  $$P/[P,P]P^4=P^{\rm ab}\ \cong\ (\mathbb Z/4)^2,\qquad P^{\rm ab}/2P^{\rm ab}=P/\Phi(P)\cong E[2].$$
  すなわち **$P^{\rm ab}$ はちょうど「$P/\Phi(P)$ の 1 段深い持ち上げ」**であり、$\Phi(P)$ の情報($\Phi(P)/[P,P]=2P^{\rm ab}$)を丸ごと含む。
- 実測の $\lvert P\rvert=64,\ \lvert[P,P]\rvert=4,\ \lvert P^{\rm ab}\rvert=16$、$P$ は非可換・指数 8・IdGroup $=[64,19]$。

### 2.2 定理 L2-LIFT

> ### 定理 L2-LIFT
> 窓 $N\in\{[1152,154161],[1152,154163]\}$、$P=[G,G]$ とする。前件 (A1)(A2)(A3) と機械入力 (M1)(M2) の下で
> $$\boxed{\ P^{\rm ab}\ :=\ P/[P,P]\ \cong\ E[4]\qquad\text{as }G_\mathbb{Q}\text{-加群}\ }\qquad (E:Y^2=X^3+16).$$
> さらにこの同型は C3-LIFT と両立する: mod 2 に落とすと $P^{\rm ab}/2P^{\rm ab}=P/\Phi(P)\cong E[4]/2E[4]\cong E[2]$(自然な射 $E[4]\to E[2],\ Q\mapsto 2Q$ 経由)。

**証明.**
**(1) 全射の構成.** (A1) より $\widehat R\cong\hat\pi_1(U_3)$ で、$P=R/N_{F_2}=\ker(G\to G^{\rm ab}=C_3)$。よって $P^{\rm ab}=R/[R,R]N_{F_2}$ は $R^{\rm ab}=H_1(U_3;\hat{\mathbb Z})$ の商である。(M1) より $P^{\rm ab}$ は 4 で消えるから、この全射は
$$\pi:\ H_1(U_3;\mathbb Z/4)\ =\ R/R^4[R,R]\ \twoheadrightarrow\ P^{\rm ab}$$
を経由する。(A3) より $N_{F_2}$ は Ihara 作用で安定、$[R,R]$ は特性的ゆえ、$\pi$ は $G_\mathbb{Q}$-同変。

**(2) 位数勘定.** $R$ は階数 4 の自由群(Riemann–Hurwitz: 種数 1・3 尖点 ⟹ $2g+n-1=4$)ゆえ $\lvert H_1(U_3;\mathbb Z/4)\rvert=4^4=256$。(M1) より $\lvert P^{\rm ab}\rvert=16$。よって $\lvert\ker\pi\rvert=16$。

**(3) 尖点部分は $\ker\pi$ に入る.** (A2)($n=4$)より $W_4\subseteq H_1(U_3;\mathbb Z/4)$ は 3 尖点の inertia class、すなわち $x^3,y^3,z^3$ の像で張られる。(M2) より $x^3,y^3,z^3\in[P,P]$、つまり $P^{\rm ab}$ での像は $0$。ゆえに $W_4\subseteq\ker\pi$。

**(4) $\lvert W_4\rvert=16$.** $\hat{\mathbb Z}$ 係数の完全列 $0\to W_{\hat{\mathbb Z}}\to H_1(U_3;\hat{\mathbb Z})\to T E\to0$ において $TE\cong\hat{\mathbb Z}^2$ は**自由**ゆえ、この列は $\hat{\mathbb Z}$-加群として分裂する(**$G_\mathbb{Q}$-同変分裂は主張しない** — 使うのは係数環上の分裂だけ)。したがって $W_{\hat{\mathbb Z}}\cong\hat{\mathbb Z}^2$ は直和因子で、$W_4=W_{\hat{\mathbb Z}}\otimes\mathbb Z/4\hookrightarrow H_1(U_3;\mathbb Z/4)$ は単射、$\lvert W_4\rvert=16$。

**(5) 結論.** (3)(4) と (2) より $\ker\pi=W_4$。ゆえに (A2) から
$$P^{\rm ab}\ \cong\ H_1(U_3;\mathbb Z/4)/W_4\ \cong\ H_1(E;\mathbb Z/4)\ =\ E[4]\quad(G_\mathbb{Q}\text{-加群として}).$$
**両立性**: $H_1(-;\mathbb Z/4)\otimes\mathbb Z/2=H_1(-;\mathbb F_2)$ かつ $W_4\otimes\mathbb Z/2=W_2$ ゆえ、(5) を mod 2 したものが C3-LIFT の同型に一致する。$\square$

> **証明の設計上の注意(Sol §2.3 の作法の踏襲)**
> - **分裂は $G_\mathbb{Q}$-同変には主張していない**。使ったのは「$TE$ が自由 ⟹ $W_{\hat{\mathbb Z}}$ は $\hat{\mathbb Z}$-直和因子」だけで、これは係数環上の事実。
> - **$W_4$ の Galois 構造($\mu_4^{\oplus2}$・非自明)は一切使っていない**。mod 2 のとき $W_2$ が自明だったのは幸運だが、mod 4 では非自明になる — それでも証明は通る、というのが本定理の要点。
> - 基点は (A1) と同じ「lift を一つ選んで得られる同型」形。lift の変更は deck 変換による同型を変えるだけで $G_\mathbb{Q}$-加群の同型型を変えない。

### 2.3 系(CM 構造の一致 — 3 本の独立 canary)

$2$ は $K=\mathbb Q(\zeta_3)$ で**惰性**($x^2+x+1$ は $\mathbb F_2$ 上既約)。ゆえに $\mathcal O/4$ は剰余体 $\mathbb F_4$ の局所環、$E[4]\cong\mathcal O/4$($\mathcal O$-加群として階数 1 自由)、$(\mathcal O/4)^\times$ は位数 12。したがって次が**予言**され、すべて実測と一致した:

| 予言(CM 側) | 実測(GAP) | 一致 |
|---|---|---|
| $E[4]\cong(\mathbb Z/4)^2$ | $P^{\rm ab}$ の不変量 $=[4,4]$ | ✓ |
| $\zeta_3-1$ のノルムは 3(奇)⟹ $\zeta_3$ は $E[4]$ 上**自由**に作用(非零固定点なし)、位数 3 | $\mathrm{Ad}(\bar x)$ は位数 3・非零固定点 0 | ✓ |
| $\zeta_3$ の特性多項式 $X^2+X+1$ ⟹ $\det=1$、$\mathrm{tr}=-1\equiv3$ | $\mathrm{Ad}(\bar x)$ の行列 $\det=1$、$\mathrm{tr}=3$ | ✓ |
| $\mathrm{Aut}(E[4])=GL_2(\mathbb Z/4)$ 位数 96、非分裂 Cartan $(\mathcal O/4)^\times$ 位数 12、その正規化群 24 | $\lvert\mathrm{Aut}(P^{\rm ab})\rvert=96$、$\lvert C(\mathrm{Ad}\bar x)\rvert=12$、$\lvert N\langle\mathrm{Ad}\bar x\rangle\rvert=24$ | ✓ |
| **Weil 対**: $\det\rho_{E,4}=\chi_{\rm cyc}\bmod4$ ⟹ $\det(T_{m,f}\vert_{P^{\rm ab}})=(2m+1)\bmod4$ | **全 48 shadow で成立**(3 レコード) | ✓✓ |
| 複素共役は $N\setminus C$ の元($\det=-1$・Cartan と非可換) | $[11,1]$: $\det=3=-1$、$\mathrm{Ad}(\bar x)$ と非可換 | ✓ |

> **Weil 対 canary の重み**: これは $E[4]$ 同定の**最強の独立傍証**である。$\det(T_{m,f})$ は純群論的に計算され、$2m+1$ は shadow の第 1 座標(円分側)である。両者が全 48 行で一致することは、$P^{\rm ab}$ 上の Galois 作用が「行列式 = 円分指標」という楕円曲線 $H_1$ に固有の性質をもつことを意味する。**反証機会は実在した**(1 行でも外れれば L2-LIFT は即座に反証)。

---

## §3 $\mathbb Q(E[4])$ の決定(自前・機械非依存・2 経路一致)

$L_0:=\mathbb Q(E[2])=\mathbb Q(\omega,\alpha)$(次数 6、$x^3-2$ の分解体、$\mathrm{Gal}\cong S_3$、**唯一の 2 次部分体は $\mathbb Q(\sqrt{-3})$**)。$X^3+16=0$ の根は $e_k=-2\alpha\omega^k$($k=0,1,2$)。

$$d_1:=e_0-e_1=-2\alpha(1-\omega),\qquad d_2:=e_0-e_2=-2\alpha(1-\omega^2),\qquad d_3:=e_1-e_2=-2\alpha\sqrt{-3}.$$

### 3.1 補題 F1($\mathbb Q(E[4])=L_0(\sqrt{d_1},\sqrt{d_2})$)

**証明.** $2Q=(e_i,0)$ なる $Q$ の座標は $r=\sqrt{e_i-e_j},\ s=\sqrt{e_i-e_k}$ として $x(Q)=e_i+rs$、$y(Q)=\pm rs(r+s)$(直接計算: $x-e_i=rs,\ x-e_j=r(r+s),\ x-e_k=s(r+s)$ ⟹ $\prod=(rs(r+s))^2$)。よって $\mathbb Q(E[4])=L_0(\sqrt{e_i-e_j}:\ i\ne j)$。$\sqrt{e_j-e_i}=\mathrm i\sqrt{e_i-e_j}$ ゆえ $\mathrm i$ も入る。
- $d_1d_3=4\alpha^2(1-\omega)\sqrt{-3}$、$(1-\omega)\sqrt{-3}=\omega(1-\omega)^2=\omega(-3\omega)=-3\omega^2$ ⟹ $d_1d_3=-12\alpha^2\omega^2=(2\alpha\omega\sqrt{-3})^2$ は $L_0$ の平方。よって $\sqrt{d_3}\in L_0(\sqrt{d_1})$。
- $d_1d_2=4\alpha^2(1-\omega)(1-\omega^2)=12\alpha^2$ ⟹ $\sqrt{d_1d_2}=2\alpha\sqrt3$、すなわち $\sqrt3\in L_0(\sqrt{d_1},\sqrt{d_2})$。$\sqrt{-3}\in L_0$ と合わせて $\mathrm i\in L_0(\sqrt{d_1},\sqrt{d_2})$。
ゆえに $\mathbb Q(E[4])=L_0(\sqrt{d_1},\sqrt{d_2})$。$\square$

### 3.2 補題 F2($[\mathbb Q(E[4]):\mathbb Q]=24$)

$3$ の上の素点で $L_0$ の正規化付値 $w$($e(3)=6$、$w(3)=6$)を取る。$(1-\omega)^2=-3\omega$ ⟹ $w(1-\omega)=3$、同様に $w(1-\omega^2)=3$。$w(2)=w(\alpha)=0$。ゆえに
$$w(d_1)=3,\qquad w(d_2)=3\quad(\text{ともに奇}) \ \Longrightarrow\ d_1,d_2\notin(L_0^\times)^2 .$$
$d_1d_2\equiv3\ (\mathrm{mod}\ (L_0^\times)^2)$ で、$\sqrt3\in L_0$ とすると $L_0/\mathbb Q$($S_3$)の 2 次部分体が $\mathbb Q(\sqrt{-3})$ 唯一であることに反する。ゆえに $d_1,d_2$ は $L_0^\times/(L_0^\times)^2$ で独立、
$$[\mathbb Q(E[4]):L_0]=4,\qquad [\mathbb Q(E[4]):\mathbb Q]=24 .\ \square$$

### 3.3 第 2 経路(4-分多項式・独立)

$E:Y^2=X^3+16$($a=0,b=16$)の位数 4 の点の $x$ 座標は $x^6+320x^3-2048=0$ の根。$u=x^3$ と置くと $u=-160\pm96\sqrt3$。実際 $x=2\alpha(\sqrt3-1)$ が $x^3=16(\sqrt3-1)^3=96\sqrt3-160$ を満たす。ゆえに
$$\mathbb Q(x(E[4]))=\mathbb Q(\omega,\alpha,\sqrt3)=\mathbb Q(\zeta_{12},\sqrt[3]2)=:M,\qquad [M:\mathbb Q]=12 .$$
$y^2=x^3+16=16(6\sqrt3-9)=16\cdot3(2\sqrt3-3)$。$M$ の 3 上の付値($e(3)=6$、$w(3)=6$、$w(\sqrt3)=3$、$w(2\sqrt3-3)=\min(3,6)=3$)で
$$w\bigl(3(2\sqrt3-3)\bigr)=6+3=9\quad(\text{奇})\ \Longrightarrow\ y\notin M\ \Longrightarrow\ [\mathbb Q(E[4]):\mathbb Q]=2\cdot12=24 .$$
**両経路は一致し、しかも中間体まで一致する**($L_0(\sqrt{d_1d_2})=L_0(\sqrt3)=M=\mathbb Q(x(E[4]))$ — $-1$ の固定体)。

**分岐指数の pin(付値論法の前件・見落としやすい)**: $L_0=\mathbb Q(\omega,\alpha)$ は $[L_0:\mathbb Q]=6$ で $3$ の分岐指数は $e\ge\mathrm{lcm}(2,3)=6$ ゆえ $e=6,f=g=1$。$M=\mathbb Q(\zeta_{12},\alpha)$ は $[M:\mathbb Q]=12$ で、$\mathbb Q_3(\zeta_4)$ が不分岐 2 次($x^2+1$ は $\mathbb F_3$ 上既約)ゆえ $f\ge2$、$e\ge\mathrm{lcm}(2,3)=6$、$ef\le12$ ⟹ **$e=6,\ f=2$**。したがって両方で $w(3)=6$ の正規化が正しい。($e=12$ なら §3.3 の付値は偶数になり議論が崩れる — ここを pin しないと穴になる。)

**数値検算(独立・`scratchpad/ec4.py` 相当)**: $e_k$ が $X^3+16$ の根/$d_1d_2=(2\alpha\sqrt3)^2$/$d_1d_3=(2\alpha\omega\sqrt{-3})^2$/$x=e_0+rs=2\alpha(\sqrt3-1)$ が $x^6+320x^3-2048$ の根/$y^2=x^3+16$/**倍化公式で $x(2Q)=e_0$**(= $Q$ が本当に $(e_0,0)$ を半分にする 4-捻れ点であることの確認)/$y$ が $y^8-96768y^4+47775744$ の根 — **7 項目すべて PASS**。

### 3.4 系 F3(像とその位置)

$C:=(\mathcal O/4)^\times\cong\mathbb Z/3\times(\mathbb Z/2)^2$(位数 12、$1+2\mathcal O\cong\mathbb F_4$ が 2 部分)、$N(C)=C\rtimes\langle\text{複素共役}\rangle$(位数 24)。$\rho_{E,4}(G_\mathbb{Q})\subseteq N(C)$ で、F2 より $\lvert\rho_{E,4}(G_\mathbb{Q})\rvert=24$、すなわち
$$\boxed{\ \rho_{E,4}(G_\mathbb{Q})=N(C)\ \ (\text{非分裂 Cartan の正規化群の全体}).\ }$$
$[N,N]$: $c\mapsto c/\bar c$ の像は $\mathbb F_4^\times$ 部分で全体($\mathbb Z/3$)、$1+2\mathcal O$ 部分で $1+2\,\mathrm{Tr}(\mathbb F_4)=\{1,-1\}$。ゆえに $\lvert N^{\rm ab}\rvert=4$ で、$\det$(円分)と $N/C$(= $K$)の 2 指標が独立ゆえ
$$\mathbb Q(E[4])^{\rm ab\text{-}max}=\mathbb Q(\mathrm i,\sqrt{-3})=\mathbb Q(\zeta_{12}),\qquad \mathbb Q(E[4])\cap\mathbb Q(\zeta_{24})=\mathbb Q(\zeta_{12}).$$
(後者: 交わりは $\mathbb Q$ 上可換なので最大可換部分体 $\mathbb Q(\zeta_{12})$ に含まれ、逆の包含は自明。もし $\sqrt2$ 等が $\mathbb Q(E[4])$ に入れば可換部分体が次数 8 になり $\lvert N^{\rm ab}\rvert=4$ に矛盾。)
したがって
$$\boxed{\ \rho_{E,4}\bigl(G_{\mathbb Q(\zeta_{24})}\bigr)=\mathrm{Gal}\bigl(\mathbb Q(E[4])/\mathbb Q(\zeta_{12})\bigr)=\ker\bigl(N_{K/\mathbb Q}:(\mathcal O/4)^\times\to(\mathbb Z/4)^\times\bigr)=\langle\omega\rangle\times\{\pm1\}\ \cong\ \mathbb Z/6 .\ }$$
とくに $-1\in\rho_{E,4}(G_{\mathbb Q(\zeta_{24})})$、また $1+2\omega,\ 1+2\omega^2\notin$(この 2 つはノルム $-1$)。

> **$1+2\mathcal O$ の 3 個の involution のうち算術的なのは $-1$ だけ**、というのが §4 の鍵である。

---

## §4 (ii) ビット 1 の判定 — **YES**

### 4.1 ビット 1 の正確な言い換え

$H:=\ker\chi_{\rm vir}$(位数 12)、$\mu:H\to\{0,6\}\cong C_2$(補題 M)、$H_0=\ker\mu$(位数 6)、$A:=\mathrm{Im}(\mathrm{Ih}_N)\cap H$、$A_0:=A\cap H_0$。(A7) より $A_0\in\{R_N(\mathcal T),H_0\}$ で、判定は $\ker(\Theta\vert_{H_0})=\{1,t\}$ の生成元 $t$ の算術性(memo §7.8(4))。

> **補題 B1(ビット 1 の同値な形).** 次は同値:
> (a) $t\in\mathrm{Im}(\mathrm{Ih}_N)$。
> (b) $\theta_t\in\rho_{P^{\rm ab}}\bigl(G_{\mathbb Q(\zeta_{24})}\bigr)$($\theta_t:=t$ の $P^{\rm ab}$ 上の誘導作用)。

**証明.** (a)⟹(b): $t=\mathrm{Ih}_N(g)$ なら $m_g=0$ ⟹ $\chi(g)\equiv1\ (\mathrm{mod}\ 24)$(A4)⟹ $g\in G_{\mathbb Q(\zeta_{24})}$、かつ $\rho_N(g)\vert_{P^{\rm ab}}=\theta_t$。
(b)⟹(a): $g\in G_{\mathbb Q(\zeta_{24})}$ が $\rho_N(g)\vert_{P^{\rm ab}}=\theta_t$ を満たすとする。$\chi(g)\equiv1\ (24)$ ⟹ $m_g\equiv0\ (12)$ ⟹ $\mathrm{Ih}_N(g)\in H_0$。実測 (M4) より $H_0\to\mathrm{Aut}(P^{\rm ab})$ は**単射**(6 元の像が相異なる)。$\theta_t\ne1$ ゆえ $\mathrm{Ih}_N(g)=t$。$\square$

### 4.2 実測 — $\theta_t$ の同定

$\mathrm{Ad}(\bar x)$ の $P^{\rm ab}$ 上の行列を $A$ とすると(独立生成元基底で $[[1,1],[1,2]]$ または $[[2,3],[3,1]]$、レコード依存 — どちらも $A^2$ の関係で同じ $\langle A\rangle$)、

$$\Theta_{\rm ab}(\ker\chi_{\rm vir})=\{\,I,\ A,\ A^2,\ -I,\ -A,\ -A^2\,\}\quad(\text{位数 6・全て }\det=1),$$
$$\boxed{\ \theta_t=-I\ \ (\text{反転 }v\mapsto v^{-1})\ }\qquad\text{— 3 レコード(両窓)すべてで一致。}$$

$t$ の同定手続き(循環なし): $H_0$ の 6 元のうち **$m=0$・shadow 位数 2・非単位**なのはちょうど 1 元で、それが $t$。その $P^{\rm ab}$ 作用が $[[3,0],[0,3]]=-I$ であることを直接検査した。

> **なぜ $\theta_t$ が well-defined か**: 「反転」は $P^{\rm ab}$ の**内在的**な言明(同型の選び方に依らない)。したがって $E[4]$ との同型の非一意性($N(C)$ の中心化群 $=\{\pm1\}$ ぶんの自由度)はここに影響しない。

### 4.3 定理 BIT1

> ### 定理 BIT1
> 前件 (A1)–(A5)+定理 L2-LIFT+実測 (M3)(M4) の下で
> $$\boxed{\ t\in\mathrm{Im}(\mathrm{Ih}_N),\qquad\text{すなわち}\quad A_0=H_0\ (\text{位数 }6).\ }$$

**証明.** L2-LIFT により $P^{\rm ab}\cong E[4]$($G_\mathbb{Q}$-加群)、ゆえに $\rho_{P^{\rm ab}}=\rho_{E,4}$。系 F3 より $\rho_{E,4}(G_{\mathbb Q(\zeta_{24})})=\langle\omega\rangle\times\{\pm1\}\ni-1$。実測 (M3) より $\theta_t=-1$。よって補題 B1 (b) が成り立ち、(a) すなわち $t\in\mathrm{Im}(\mathrm{Ih}_N)$。(A7) より $A_0\supseteq R_N(\mathcal T)$ かつ $t\in A_0$、$\lvert H_0\rvert=6$ ゆえ $A_0=H_0$。$\square$

> **反証の在り処(この判定が「たまたま」でない理由)**: $\theta_t$ は $1+2\mathcal O\cong\mathbb F_4$ の 3 個の involution $\{-1,\ 1+2\omega,\ 1+2\omega^2\}$ のいずれかでありえた。そのうち算術的(= $\ker N_{K/\mathbb Q}$ に入る)なのは **$-1$ ただ 1 つ**。実測が $1+2\omega$ 型を返していれば **ビット 1 = NO** で、$t$ は**非算術 shadow の明示** = **B3-証人型候補**になっていた。**判定は 1/3 の当たりを引いた形ではなく、両側に実在の分岐があった。**

---

## §5 (iii) ビット 2 の判定 — **YES**(幾何を使わない)

> ### 定理 BIT2
> (A4) のみを使う。$\chi:G_\mathbb{Q}\to\hat{\mathbb Z}^\times$ は全射ゆえ $\chi(g)\equiv13\ (\mathrm{mod}\ 24)$ なる $g\in G_\mathbb{Q}$ が存在する。このとき
> $$m_g=\frac{\chi(g)-1}{2}\bmod12\equiv6,\qquad \chi_{\rm vir}(\mathrm{Ih}_N(g))=2\cdot6+1=13\equiv1\ (\mathrm{mod}\ 12),$$
> すなわち $\mathrm{Ih}_N(g)\in\ker\chi_{\rm vir}$ かつ $m=6$。ゆえに
> $$\boxed{\ \mu(A)=C_2,\qquad \lvert A\rvert=2\lvert A_0\rvert .\ }$$

**注(この 2 行の位置づけ)**: memo §7.8(4) と便 156 §3.3 は「$m=6$ 層は算術元が一つでもあるか」をもう 1 ビットの**未決**として登録していた。**これは $\chi$ の全射性だけで決まる** — $m$ の法($N_{\rm ord}=12$)と $u=2m+1$ の法($2N_{\rm ord}=24$)の区別(既登録の trap)を丁寧に追えば出る。楕円曲線も C3-LIFT も使わない。⟹ **残問は実質 1 ビット(ビット 1)だけだった。**

---

## §6 (iv) 帰結の整理

### 6.1 定理 SAT-83(窓水準全射)

> ### 定理 SAT-83
> 定理 BIT1 + 定理 BIT2 + (A4) より、両窓 $N\in\{[1152,154161],[1152,154163]\}$ について
> $$A=\ker\chi_{\rm vir}\ (\text{位数 }12),\qquad \lvert\mathrm{Im}(\mathrm{Ih}_N)\rvert=\lvert\chi_{\rm vir}(\mathrm{Im})\rvert\cdot\lvert A\rvert=4\cdot12=48,$$
> $$\boxed{\ \mathrm{Im}(\mathrm{Ih}_N)\ =\ GT(N)\ \ \bigl(=GT^{\rm arith}(N)\bigr).\ }$$
> すなわち **$GT(N)$ の 48 個の shadow はすべて算術的**。(A5) より **すべて genuine**、したがって **すべて全細分 $K\le N$ で生存する**。

($\lvert\chi_{\rm vir}(\mathrm{Im})\rvert=\lvert(\mathbb Z/12)^\times\rvert=4$ は (A4)。)

### 6.2 第 2 経路(独立・ビットを経由しない)

$\Psi:GT(N)\to\mathrm{Aut}(P^{\rm ab})$ は (M5) より像 24・核 2。
- $\Psi(\mathrm{Im}\,\mathrm{Ih}_N)=\rho_{E,4}(G_\mathbb{Q})=N(C)$(系 F3)$=\mathrm{Im}\,\Psi$(位数 24 が一致)。
- $\ker\Psi\subseteq\mathrm{Im}(\mathrm{Ih}_N)$: 系 F3 より $\mathbb Q(E[4])\cap\mathbb Q(\zeta_{24})=\mathbb Q(\zeta_{12})$ ゆえ、$\chi\bmod24$ の $G_{\mathbb Q(E[4])}$ への制限の像は $\{1,13\}$。$\chi(g)\equiv13$ なる $g\in G_{\mathbb Q(E[4])}$ を取れば $\mathrm{Ih}_N(g)$ は $m=6$ かつ $P^{\rm ab}$ 上自明 ⟹ $\ker\Psi$ の非単位元(実測: $m=6$ で $\Psi=I$ の shadow はちょうど 1 個)。
ゆえに $\mathrm{Im}(\mathrm{Ih}_N)\cdot\ker\Psi=GT(N)$ かつ $\ker\Psi\subseteq\mathrm{Im}(\mathrm{Ih}_N)$ ⟹ $\mathrm{Im}(\mathrm{Ih}_N)=GT(N)$。$\square$

### 6.3 系 FIELD-83(閉じた算術的実現)

> ### 系 FIELD-83
> $$\boxed{\ \mathrm{Ih}_N\ \text{は同型}\quad \mathrm{Gal}\bigl(\mathbb Q(\zeta_{24},E[4])/\mathbb Q\bigr)\ \xrightarrow{\ \sim\ }\ GT(N)\ }\qquad [\mathbb Q(\zeta_{24},E[4]):\mathbb Q]=\frac{8\cdot24}{4}=48 .$$

**証明.** $\ker(\mathrm{Ih}_N)$ の固定体を $L$ とすると $\mathrm{Gal}(L/\mathbb Q)\cong\mathrm{Im}(\mathrm{Ih}_N)=GT(N)$、$[L:\mathbb Q]=48$。
包含 $\ker(\mathrm{Ih}_N)\subseteq G_{\mathbb Q(\zeta_{24},E[4])}$: $\mathrm{Ih}_N(g)=1$ なら (i) $m_g=0$ ⟹ $\chi(g)\equiv1\ (24)$ ⟹ $g$ は $\zeta_{24}$ を固定、(ii) $T_{0,1}=\mathrm{id}$ ⟹ $P^{\rm ab}$ 上自明 ⟹ $\rho_{E,4}(g)=1$ ⟹ $g$ は $E[4]$ を固定。
次数は $[\mathbb Q(\zeta_{24}):\mathbb Q]\cdot[\mathbb Q(E[4]):\mathbb Q]/[\mathbb Q(\zeta_{12}):\mathbb Q]=8\cdot24/4=48$(系 F3)。両者の次数が一致するので $L=\mathbb Q(\zeta_{24},E[4])$。$\square$

### 6.4 台帳・地図への反映(検収後・全て candidate)

| 項目 | 旧 | **新** |
|---|---|---|
| C-15 (C6) | $\mathrm{Im}(\mathrm{Ih}_N)\supseteq C_2\times C_3$(位数 ≥12) | **$\mathrm{Im}(\mathrm{Ih}_N)=GT(N)$(位数 48・窓水準全射)** |
| 候補数 | 22 → 18 | **18 → 0** |
| 残問 2 ビット | 未決 | **両方 YES**(ビット 2 は幾何不要) |
| DICHOTOMY-83 | genuine 側(𝒯 3 元) | **全 48 元 genuine**(算術経由) |
| $L_2$ レーン | 未着手 | **完了**($L_2=P^{\rm ab}\cong E[4]$・RES-1 の要求を満たした) |
| 83 線の性格 | 反例候補線 | **算術飽和線**(B3-証人型候補は出ない) |

### 6.5 何を主張していないか(規律)

- ❌ 「$\widehat{GT}_{\rm gen}$ への $G_\mathbb{Q}$ の全射性」— **言っていない**。有限窓 $N$ 一点での $\mathrm{Im}(\mathrm{Ih}_N)=GT(N)$ である。
- ❌ 「井原予想の証拠」— 単一窓の全射は予想の**必要条件の 1 例**にすぎない(反例窓が他にありうる)。
- ❌ **PENT_W 昇格とは別勘定**: 本ノートは B₃-gentle 窓の話。$B_4$ 側(pentagon)への押し出しは一切扱っていない。
- ❌ `verified` でも `cross-checked` でもない。**candidate・1 系統**。
- ⚠ 「genuine」は (A5) の含意鎖 arithmetical ⟹ genuine による。**有限深度の生存実測から導いたのではない**(裁定 1447 の非対称は不変)。

### 6.6 retrospective agreement(格上げしない記録)

C-15 (C2′) の「full-48 単段生存が $p=2,3$ で cross-checked・$p=5$ で単系統・登録済み有限探針から fake 証明書 0」は、定理 SAT-83 が予言する姿(**全 48 元 genuine ⟹ 全細分で生存**)と一致する。**これは事後的な数値一致(retrospective agreement)であり、独立裏取りでも SAT-83 の証拠でもない**(C5-e の語法規律)。ただし**反証機会は実在した**: 1 枚でも真正の死亡証明書が出ていれば SAT-83 は反証されていた。

### 6.7 (S7′) 片側反証器の強化(自動的)

memo §8.7 (S7′) の反証器は $[0,f_\nu]$($\nu\ne0$)の 3 元を対象としていた。SAT-83 の下では**対象が全 48 元に広がる**:

> **falsifier canary CAN-SAT-83**: 任意の $K\le N$ と任意の $s\in GT(N)$ について、(S7′) の 5 要件(canonical key・全 fibre・exact multiset coverage・破壊/陽性対照・原因を一意帰属させない)を満たす真正の死亡証明書が 1 枚出れば、**SAT-83 は反証**され、ひいては L2-LIFT / C3-LIFT / C-15 (C1) / reduction 実装の連言のどれかが偽である。**有限深度で死が出ないことは支持証拠へ格上げしない**(不変)。

---

## §7 機械検算(3 スクリプト・再現手順つき)

| スクリプト | 内容 | 主な出力 |
|---|---|---|
| `scratchpad/m3_l2_probe_v1.g` | $P$ の層構造($\Phi(P),[P,P],P^2,P^4,M_4$)・尖点の所属・$\mathrm{Ad}(\bar x)$・$\ker\chi_{\rm vir}$ 12 元の各層での作用位数・inner 判定・shadow 位数 | $\lvert P\rvert=64$, $\lvert\Phi(P)\rvert=16$, $\lvert[P,P]\rvert=4$, $\lvert P^4\rvert=2$, $P^{\rm ab}=[4,4]$, IdGroup$=[64,19]$, 尖点 3 つとも $\in[P,P]$, $\langle$尖点$\rangle^G=[P,P]$ |
| `scratchpad/m3_l2_probe_v2.g` | $\theta_t$ の同定($\{\pm\mathrm{Ad}(\bar x)^j\}$ に対する照合)・$H_0$ の類 | **$t$: IS_INVERSION = true**(3 レコード)・$H_0$ の像 $=\{\pm A^j\}$ |
| `scratchpad/m3_l2_probe_v3.g` | $P^{\rm ab}$ 上の**行列**(独立生成元基底)・**Weil 対 canary**・$\Psi$ の像/核・Cartan/正規化群・複素共役 | **det canary 48/48 PASS**(3 レコード)・$\lvert\mathrm{Im}\Psi\rvert=24$, $\lvert\ker\Psi\rvert=2$, $\lvert C(\mathrm{Ad}\bar x)\rvert=12$, $\lvert N\langle\mathrm{Ad}\bar x\rangle\rvert=24$, $[11,1]$: $\det=3$・非可換 |
| `scratchpad/m3_e4_field_numcheck_v1.py` | §3 の代数恒等式の数値検算(GAP と独立・群論非依存) | 7/7 PASS(倍化公式 $x(2Q)=e_0$ を含む) |

**規約遵守**: 3 本とも **W-1 fail-closed assert** を先頭に置いた — 陽性(補題 U′ $f_1^{-1}\sigma_2f_1=x\sigma_2x^{-1}$、$f_1=$ paper $yx^{-1}=$ GAP `x^-1*y`)+**陰性 canary**(誤形 paper $x^{-1}y$ が同 fixture で不一致)+ fixture 非可換性の確認。3 本・3 レコードすべて PASS(不成立なら `Error` で停止する設計)。積は全て `AbstractProd`(reversal 規約)経由。

**再現**: `.\gap.ps1 scratchpad\m3_l2_probe_vK.g`(K=1,2,3)。入力は既在 `search/iso_census83_deep15_data.g` と `search/week3-battery-common.g` のみ。**窓の shadow 候補値・封印には非接触**(shadow は本スクリプトが正典の (3.3)(3.4)(charming) から自前に再列挙し、$\lvert GT(N)\rvert=48$・$\ker\chi_{\rm vir}=12$・$m$ 分布 $\{0:6,6:6\}$ という**既登録の二系統事実を再現**した — これが本スクリプトの健全性検査を兼ねる)。

**自己申告**: (a) 機械入力は本ノート 1 系統(独立照合器なし)。(b) §3 は完全に手計算(機械非依存)で、2 経路が一致。(c) 配達文献 2 本(Ishii)は**本ノートの結論に使っていない**(§9 参照)。

---

## §8 残る GAP(Sol 監査の入力)

| 札 | 内容 | 重み |
|---|---|---|
| 【**GAP-L2-1**】 | **定理 L2-LIFT の幾何鎖の Sol 監査**。C3-LIFT で監査済みの (A1)(A2) を $n=4$ に上げただけだが、**$W_4\cong\mu_4^{\oplus2}$ が非自明加群になる**点と、証明が「$W_4$ の Galois 構造を使わない」ことの妥当性(§2.2 の注)を確認されたい。とくに「$TE$ が自由 ⟹ $W_{\hat{\mathbb Z}}$ は係数環上の直和因子 ⟹ $W_4\hookrightarrow H_1(U_3;\mathbb Z/4)$」の 1 行。 | **高** |
| 【**GAP-L2-2**】 | **機械入力 (M1)–(M6) の独立照合**(著者分離・producer 非開封)。とくに (M3)「$\theta_t$ = 反転」は**判定の全体を載せている 1 ビット**。照合器は $P^{\rm ab}$ を独立に構成し、$t$ の同定手続き($m=0$・shadow 位数 2・非単位で一意)を再現し、反転性を再計算すべき。 | **高(格の前件)** |
| 【GAP-L2-3】 | 系 F3 の $\mathbb Q(E[4])\cap\mathbb Q(\zeta_{24})=\mathbb Q(\zeta_{12})$ を、$N^{\rm ab}$ 計算に依らずに直接(例: $\sqrt2\notin\mathbb Q(E[4])$ を分岐で)確認する第 2 経路 | 中 |
| 【GAP-L2-4】 | $\mathrm{Ih}_N$ が**準同型**であること(isolated ⟹ 群)を本ノートは (A3) から引用している。$\lvert\mathrm{Im}\rvert=\lvert\chi_{\rm vir}(\mathrm{Im})\rvert\cdot\lvert A\rvert$ はこれに載る | 低(既登録) |
| 【GAP-L2-5】 | $E[4]$ より深く($E[8]$・$T_2E$・$\pi_1$ の非可換部分)は**未着手**。本窓では不要になったが、他窓へ機構を運ぶときに必要(§9) | 低(本窓では不要) |

---

## §9 配達文献の扱い(正直な申告)と 文献要請の更新

**配達された 2 本は本ノートの決着に使わなかった。** 理由を明記する:

- 我々が必要としたのは **$\mathbb Q(E[4])$ という具体的な次数 24 の体の決定**であり、水準が小さいので **初等的な 2-降下(Kummer 類 $d_1,d_2$)と 4-分多項式**で完全に決まった(§3・2 経路一致)。elliptic Soulé 元/Kummer 指標の非消滅判定という一般機構は、**この水準では過剰**である。
- 覚書が指示した「Im$(G_\mathbb{Q}\to\mathrm{Out}\,\pi_1^{(2)}(E\setminus S))$ の下界」は、本窓では **$P$ が位数 64 の有限商**であるため、下界ではなく**等式**(全射)が有限計算+初等代数体論で出た。

**したがって【文献要請 E-1】は本窓については解消**(取り下げ)。**残す要請は水準を上げた形に置き換える**:

> 【**文献要請 E-2**】(新・優先度は低〜中 — 本窓では不要、他窓への横展開用)
> **困難**: 同じ機構($G^{\rm ab}=C_p$ の中間被覆 ⟹ 穴あき曲線 ⟹ その $H_1(\ \cdot\ ;\mathbb Z/\ell^k)$)を **$\ell^k\ge8$** または**種数 ≥2 の被覆**に適用すると、(a) 分体の次数計算が初等 2-降下では届かない、(b) $\pi_1$ の非可換部分($[R,R]$ 以下の層)が現れて $H_1$ だけでは像が決まらない、の 2 点で止まる。
> **欲しい結果の型**: ①CM 楕円曲線 $E/\mathbb Q$ と $\ell$ 惰性のとき $[\mathbb Q(E[\ell^k]):\mathbb Q]$ と $\mathbb Q(E[\ell^k])\cap\mathbb Q(\zeta_M)$ を **$k$ について一様に**与える定理(entanglement の明示)。②穴あき $E\setminus S$($S$ = 捻れ点)の pro-$\ell$ $\pi_1$ の **weight-2 層**($[R,R]/[[R,R],R]$ 相当)への $G_\mathbb{Q}$ 像の下界(elliptic Soulé/Eisenstein 由来)。
> **なぜ必要か**: 83 窓は飽和で閉じたので、次は**別の窓**($\mathrm{solvis}$ が非空な窓)へ同じ機構を運ぶ段。そのとき (a)(b) が最初の壁になる。

**Ishii 2 本の位置づけ**(読解結果は §10 に別記): 本ノートの結論に対しては **cross-check にもならない**(扱う水準・仮定が異なる)。ただし E-2 の①②に直接効く可能性があり、**資料庫に残す**。

---

## §10 配達文献の読解結果(読解係経由・§/定理番号つき)

**結論(先に)**: 2 本とも **我々の設定は仮定を満たさない**(三重に破綻)。§9 の裁定は変わらない — 本ノートの結論は文献に依存していない。ただし**設計図としては有用**で、E-2 の照準が定まった。

### 10.1 Ishii **2312.04196**(once-punctured CM elliptic の pro-p 外 Galois 表現の核)

- **主定理 Thm A = Thm 2.14** (p.11): $p\ge5$ が $K$ で**分裂**し、(1) $K(\mathfrak p)$ の類数が $p$ で割れない (2) $K(\mathfrak p^2)$ の上に $p$ の素点がちょうど 2 つ (3) Conjecture 2.3(楕円 Deligne–Ihara・**未解決**)ならば $\bar{\mathbb Q}^{\mathrm{Ker}\rho_{X,p}}=K(E[p])\cdot\Omega$。像の分解は **Lemma 2.13** (p.10): $\rho_{X,p}(G_{K(\mathfrak p)})=\mathrm{Gal}(K(E[p])/K(\mathfrak p))\times\mathrm{Gal}(\Omega^*/K(\mathfrak p))$。
- **仮定と我々の設定の照合**(読解係の判定):

| 仮定 | 論文 | 我々 | 判定 |
|---|---|---|---|
| CM 体 | $K$ = 類数 1 の虚二次体、$\mathrm{End}_K(E)=\mathcal O_K$ | $K=\mathbb Q(\sqrt{-3})$、$h=1$ | ✅ |
| 除去点 | **$X=E-O$(原点 1 点)**・$\Pi_{1,1}$ は階数 2 自由 pro-$p$ | **3 点 $\{O,T,-T\}$**・階数 4 | ❌ **本質的** |
| 素数 | **$p\ge5$ かつ $K$ で分裂**(+ $p\nmid\lvert\mathcal O_K^\times\rvert=6$) | $\ell=2$・**惰性** | ❌ **三重に破綻** |
| 基礎体 | $K$ 上の $\rho_{X,p}:G_K\to\mathrm{Out}$ | $\mathbb Q$ | ⚠(底変更すれば可・ただし $G_\mathbb{Q}$ の情報が落ちる) |

- **層構造**(§2.1, Prop 2.2 p.6): 重みフィルトレーション $F^mG_K$、$\mathfrak g_m\otimes\mathbb Q_p\cong\bigoplus\mathbb Q_p(\mathbf m)$($\mathbf m=(m_1,m_2)$、二重次数)。$m$ 奇数と $m=2$ で自明。各層の**検出器は楕円 Soulé 指標 $\kappa_{\mathbf m}$**(Thm 2.6 = Nakamura [Nak95] の母関数 $\alpha_{1,1}$)。
- ★**我々の曲線が現れる唯一の地点** — **Remark 2.15.1** (p.11): $K=\mathbb Q(\sqrt{-3})$、$p_K=3$、$E$ = **3 次 Fermat 曲線**($\bar{\mathbb Q}$ 上 27a3 と同型)、1 点抜きで**無条件**に核の固定体を決定($K=K(3)=K(E[3])$)。**$p=3$・1 点抜き**であって我々($\ell=2$・3 点抜き)ではない。

### 10.2 Ishii **2312.04175**(Kummer 指標)

- **Def 1.1** (p.3): $\kappa_{\mathbf m}:G^{\rm ab}_{K(E[p^\infty])}\to\mathbb Z_p$ は**楕円単数**(基本テータ函数 $\theta_p$ の $p^n$-捻れ点での値)の Kummer 類。**捻れ点の分体そのものの Kummer 類ではない。**
- **Thm 1.5 / Thm 4.5** (p.4–5, p.18): $\kappa_{\mathbf m}$ 非自明 ⟸ **$H^2_{\text{ét}}(\mathrm{Spec}\,\mathcal O_K[1/p],\mathbb Z_p(\mathbf m))$ の有限性**(= Jannsen 予想の特別な場合・一般には未解決)。全射性は **射類体 $K(\mathfrak p)$ の類数の $p$ 可除性**(円分の Vandiver の位置)。無条件ケース 3 本: Cor 4.8・**Cor 4.10($\kappa_{(m,m)}$ は全 $m\ge2$ で非自明 — Soulé 経由)**・Prop 4.14。$L$ 値は Yager の $p$ 進 Hecke $L$ 判定基準として **Example 4.2** に登場。
- **水準**: $E[p^n]$ 全 $n$ で定義されるが、**$p\ge5$ かつ $E$ が $p$ 上 potentially good *ordinary* reduction が全篇の大前提**(Notations p.5)。**$p=2$ の記述は論文中に 1 箇所も無い**(読解係の全文 grep)。$\mathbb Q(\sqrt{-3})$ の明示例も無い(例は $\mathbb Q(\sqrt{-1})$・$\mathbb Q(\sqrt{-163})$)。

### 10.3 我々の設定との構造的不整合(独立に確認できる 1 行)

**$2$ は $K=\mathbb Q(\sqrt{-3})$ で惰性 ⟺ $E$ は $2$ で超特異(supersingular)** — 04175 が要求する *ordinary* reduction の**否定**。ゆえに岩澤主予想経由の証明機構(§4.1)が土台から効かない。
> **整合の記録**: この超特異性は、本ノートが §3 で独立に得た「$\rho_{E,4}(G_\mathbb{Q})=$ **非分裂** Cartan の正規化群」とちょうど同じ事実の 2 つの言い方である(分裂 Cartan ⟺ ordinary、非分裂 ⟺ supersingular)。**文献側の適用不能理由と我々の計算結果が同じ構造事実に由来している** — 一致の記録であり、証拠には数えない。

### 10.4 裁定(§9 の更新)

- **C1(E[8] 以降に直接使えるか)= 使えない**。理由 3 点: (a) $\ell=2$ が全面的に射程外(両論文 $p\ge5$・$p=2$ の記述皆無)・かつ超特異で機構が効かない、(b) **1 点抜き専用**($\Pi_{1,1}$ 階数 2 と Nakamura の 2 変数母関数に全面依存)、(c) 主定理が未解決予想(Conj 2.3)に条件付き。
- **C2(近い具体例)= 無い**。楕円曲線から 3 点抜く例は両論文に皆無(3 点抜きは $\mathbb P^1\setminus\{0,1,\infty\}$ のみ)。最も近いのは 04196 Remark 2.15.1($\mathbb Q(\sqrt{-3})$・$p=3$・1 点抜き)。
- **【文献要請 E-1】は取り下げ**(§9 のとおり)。**【文献要請 E-2】の照準を更新**: ①に加えて ②を「**3 点抜き**(捻れ点を抜いた)CM 楕円曲線の pro-$\ell$ $\pi_1$ に対する Nakamura 型母関数の**一般化**が存在するか」+「$\ell$ が**惰性(超特異)**のときの楕円 Soulé/Kummer 理論」に絞る。**追跡候補(未入手・読解係の指摘)**: 04196 p.3 が引く **[Hos15, Example 3.4 (2)]**(高種数曲線で $\mathbb P^1\setminus\{0,1,\infty\}$ と同核)と **[Tak12, Thm 3.6]**(Oda's prediction)。
- **読解の射程申告**: 04196 pp.13–25・pp.29–30 と 04175 pp.7–14・pp.27–35 は**未読**(読解係申告)。上記の引用は §1–2 と該当 Cor/Remark に限る。読解係が導いた $I=\{(m_1,m_2):m_1\equiv m_2\ (\mathrm{mod}\ 6)\}$ と「第 1 層 = 次数 4 = $\kappa_{(2,2)}$」等は**論文に明示なし = 読解係の計算**(candidate)。

---

## §11 handover(次の一歩の候補・優先順)

1. **【GAP-L2-2】独立照合器の発注**(格の前件・最優先)。仕様 = $P^{\rm ab}$ の独立構成 + $t$ の一意同定 + 反転性 + Weil det canary 48 行 + W-1 assert/`ad_convention` pin(A4-1/A4-2 準拠)。
2. **Sol 便**(【GAP-L2-1】の幾何鎖監査 + SAT-83/FIELD-83 の格判定 + §5 の「便 156 が未決としたビット 2 が 2 行で決まる」件の確認)。
3. **CAN-SAT-83 の登録**(park 中の survival lane を全 48 元の片側反証器へ拡張)。
4. **横展開**: $\mathrm{solvis}$ が非空な**別の窓**を探す(判定計器 = $G^{\rm ab}$ の巡回商 → 中間被覆の種数 → 曲線の同定)。83 が飽和で閉じた以上、B3-証人型を探すなら**別の窓か別の機構**が要る。
5. **地図・C-15 の同期**(§6.4 の表)。**「83 線完結」と書くのは検収後**(§6.5 の非含意を必ず併記)。
