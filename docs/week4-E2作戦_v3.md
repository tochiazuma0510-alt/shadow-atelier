# Week 4 — 【GAP-E2】正面 作戦計画 v3

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 10**。
**v1 / v2 は上書きしない**(`docs/week4-E2作戦_v1.md`・`docs/week4-E2作戦_v2.md`)。本稿は **Sol 便 13(`sol/sol_reply_13_graded.md`)の全指摘と裁定 13 を反映した正本**である。v2 の主張のうち **撤回されたもの・修正されたものを §0 の表に一覧**し、以下で一つずつ直す。

**分割**: 本稿は §1–§7(数学の訂正と再定式化)。E22 の完成は `docs/命題_E22三段判定_v1.md`、掃引宇宙 v3 は `docs/week4-掃引宇宙_v3.md`、E19 の二系統化指示書は `docs/week4-E19二系統化指示書_v1.md` に分割した。

依存: 便 13・裁定 13・v2・`docs/week3-狩場計画_v4.md`(命題 E1・系 E2′-a)・`docs/week1-定義ノート.md` v2。
新規検算スクリプト(共有ツリー・監査対象): **`docs/scout/metab_rank.mjs`**(§6 の E19-b′ の入力データ)。

---

## 0. v2 → v3 の差分表(何が撤回され、何が生き残ったか)

| v2 の主張 | 便 13 の裁定 | v3 での処置 | 本稿 |
|---|---|---|---|
| Lemma A(§1.2)の $\sigma^2(p+q)$ の中間式 | 誤植(最終値は正しい) | **訂正して再掲**。Lemma A・Lemma B・(†) は **paper mutual-audit PASS / candidate** へ昇格 | §1 |
| 命題 E16(定理文「$\theta(A^\sigma)=A^\sigma$ ならば」) | **FAIL**(必要方向が出ない・Sol の反例) | **定理文を差し替え**(仮定 $= e\theta=\theta e$)。**十分方向は無仮定で成立**。系 E16-a(class $\le2$)は保持 | §2 |
| 補題 E16.1 の「$\theta(A^\sigma)$ 安定 $=\iota\vert_A=1$」 | 誤り | **等号を包含へ訂正**($\iff\iota\vert_{A^\sigma}=\mathrm{id}$) | §2.2 |
| 補題 E18.2 の証明語句(「単純加群は $R$ のみ」「$\mathbb Z_2[C_2]$-自由」) | 結論 PASS・語句 FAIL | **Morita + normal integral basis + induced** で書き直し | §3 |
| 定理 E18 の障害群 $O_j=(1+\bar\theta)M_j^+$ | **FAIL**(像であって cokernel でない) | **撤回**。$\boxed{C_j=(M_j^{\bar\sigma})^{\bar\theta}}$ へ再定式化。★「$\sigma$-非自明部は induced ゆえ障害を出さない」は**成果として保持** | §4 |
| 「$O_j=0\iff$ 自明表現なし」を有限層の判定に使う | **FAIL**(位数 2 元上で $-1=+1$) | **撤回**し、さらに強い形へ: 有限 2 群では $C_j=0\iff M_j^{\bar\sigma}=0$(§4.3・本稿の追加) | §4.3 |
| weight 5 初出(表 1) | 有理表現論として PASS | **射程を限定して保持**(有理係数の主張・E9/E9′ の再証明ではない) | §5 |
| 定理 E19($c\le7$, $m\le63$) | 単系統 candidate のまま | 札を `Z2-solvable candidate (single system, statically audited)` に固定。二系統化は別紙 | §6.1 |
| 系 E19-b(mod 8 周期性 $\Rightarrow$ 全 $m$) | **FAIL** | **撤回**。代わりに **命題 E19-b′(小行列式の次数による有限判定)を新設し、$c\le6$ については全 $m\in\mathbb Z$ で実際に閉じた** | §6.2 |
| 「素数 2 は完全に落ちた」 | 射程超過 | **撤回**($c\le5$ に限る・§6.3 が正しい射程) | §6.3 |
| 定理 E21(E12-a は空虚) | **PASS** | 維持(変更なし) | — |
| 補題 E22(norm 積公式) | 積公式 PASS・持ち上げ枠組み未完 | 積公式維持。**三段判定として完成**(別紙 `命題_E22三段判定_v1.md`) | §7 |
| 「生存層は class-5 非 metabelian だけ」 | 射程超過 | **撤回**。class-5 非 metabelian は**第一優先層**。metabelian class $\ge8$・$c=7$ の全 $m$ は **UNKNOWN として盤面に残す** | §7 |
| 掃引宇宙 v2(`U-E2-nm5-2026-07-26`) | **NO-GO** | **凍結**。新 ID `U-E2-nm5-r2-2026-07-26` で再登録(別紙) | 別紙 |

★ **一行でいうと**: (†) は紙で閉じた(これは確定)。しかし **graded 解析の「障害は消えている」という読みは誤りだった** — 有限 2 群では潜在障害群はほぼ常に非零で、消えるのは**障害元**であって群ではない。一方 E19 側は、便 13 が撤回を求めた $m$ 量化子が、**小行列式の次数による有限判定で $c\le6$ については実際に閉じた**($c=6$ は便 12/13 時点では $m\le63$ 止まりだった層)。

---

## 1. Errata 1 の反映 — Lemma A の中間式(便 13 F1)

v2 §1.2 の

$$ \sigma^2(p+q) \;=\; -q + r_1 + (1+m)r_2 + (2+m)r_3 \qquad\text{(v2・誤り)} $$

は、第一項 $-\sigma(p) = -q+r_2-mr_3$ の中心座標を落としている。正しい計算を再掲する(独立に再展開して Sol と一致):

$$ \sigma(p+q) = (q-r_2+mr_3) + \bigl(-p-q+2r_1+(2-m)r_2+(1-m)r_3\bigr) = -p+2r_1+(1-m)r_2+r_3. $$
$$
\begin{aligned}
\sigma^2(p+q)
&= -\sigma(p) + 2\sigma(r_1) + (1-m)\sigma(r_2) + \sigma(r_3)\\
&= (-q+r_2-mr_3) + 2r_3 + (1-m)(-r_2-r_3) + (r_1+2r_2+r_3)\\
&= \boxed{\,-q + r_1 + (m+2)r_2 + 2r_3\,}.
\end{aligned}
$$

総和は $p,q$ が相殺して
$$ \mathcal N(p+q) = (2+1)r_1 + \bigl((1-m)+(m+2)\bigr)r_2 + (1+2)r_3 = 3\rho . $$

v2 の最終行はすでに正しい係数 $(m+2,\,2)$ を用いていたので、**Lemma A の結論は無傷**である。

> **状態札の更新(便 13 F1–F3・裁定 13 §1)**: Lemma A・Lemma B・**中心恒等式 (†)** $\mathcal N(f_0)=-9E_m$ ・定理 E9′ は
> $$ \texttt{paper mutual-audit PASS / candidate} $$
> へ昇格する(Sol が構造定数・$w$ 座標・Magnus の $\xi^2\eta^2$ 係数を独立に追い、script に依存せず閉じることを確認)。**verified(Lean)ではない。** 便 12 W98 の単系統保留は解除。

---

## 2. 命題 E16 — 正しい定理文(便 13 F4)

### 2.1 Sol の反例の独立検証(FAIL の追認)

Sol の抽象反例を自分で検算した。$A=C_4\oplus C_4^2$、$\sigma(a,x)=(a,Sx)$、$S=\begin{pmatrix}0&-1\\1&-1\end{pmatrix}$。

- $S^2=-S-1$ ゆえ $S^3=1$、$1+S+S^2=0$。$\det(S-1)=3\in(\mathbb Z/4)^\times$ ゆえ $\ker(S-1)=0$、したがって $A^\sigma=C_4\oplus0$。
- $\varphi(x_1,x_2)=x_1$、$\theta(a,x)=(a+\varphi(x),-x)$。$\varphi$ は線型なので $\theta^2=\mathrm{id}$、かつ $\theta(a,0)=(a,0)$ ゆえ $\theta(A^\sigma)=A^\sigma$。
- $\mathcal N(a,x)=(3a,0)$、$3\in(\mathbb Z/4)^\times$ ゆえ $\ker\mathcal N=0\oplus C_4^2$。$\theta(0,x)=(\varphi(x),-x)\notin\ker\mathcal N$($\varphi(x)\ne0$ のとき)⇒ **$\ker\mathcal N$ は $\theta$-安定でない**。
- $x=(2,0)$、$b=(1,x)$: $\theta(b)=(1+2,(2,0))=(3,(2,0))=-b$ ✓、$\mathcal N(b)=(3,0)$。$E:=-\mathcal N(b)=(1,0)\in A^\sigma$。
- ゆえに $(\ast)$ は**成立**するが $\theta(E)=(1,0)=E\ne-E=(3,0)$。∎

**Sol の指摘は正しい。v2 の命題 E16 の定理文は FAIL。** v2 の証明が実際に使っているのは「$\theta(A_+)=A_+$ **かつ** $\theta(A_-)=A_-$」であり、これは $\theta(A^\sigma)=A^\sigma$ からは出ない。

### 2.2 補題 E16.1 の訂正

> **補題 E16.1(訂正版).** 命題 E1 $\ \theta\sigma\theta=\iota_{X^u}\sigma^{-1}$($\iota:=\iota_{X^u}\vert_A$)より、$a\in A^\sigma$ に対し $\sigma(\theta a)=\theta(\iota a)$。したがって
> $$ \theta(A^\sigma)\subseteq A^\sigma \iff \iota\vert_{A^\sigma}=\mathrm{id} \iff A^\sigma\subseteq C_A(X^u). $$
> **$\iota\vert_A=\mathrm{id}$ は十分条件にすぎない**(v2 D3 の「$=$」は誤り)。

**証明.** $\theta\sigma\theta=\iota\sigma^{-1}$ の両辺に右から $\theta$ を掛けて $\sigma\theta=\theta\iota\sigma^{-1}$。$a\in A^\sigma$ なら $\sigma^{-1}a=a$ なので $\sigma(\theta a)=\theta(\iota a)$。よって $\theta a\in A^\sigma\iff\theta(\iota a)=\theta(a)\iff\iota a=a$。∎

### 2.3 命題 E16(v3・正しい定理文)

> **命題 E16 (v3).** $A$ 有限可換 2 群、$\sigma^3=\mathrm{id}$、$\theta^2=\mathrm{id}$、$E_m\in A^\sigma$、$\lambda:=3^{-1}\bmod\exp A$、$e:=\lambda\mathcal N$。
> **(i) 十分方向(無仮定)**: $\theta(E_m)=E_m^{-1}$ ならば $(\ast)$ が成立する。
> **(ii) 必要方向(要仮定)**: $\ \mathcal N\theta=\theta\mathcal N$(同値: $e\theta=\theta e$、同値: $\theta(A_+)=A_+$ かつ $\theta(A_-)=A_-$)を仮定すると、$(\ast)\Rightarrow\theta(E_m)=E_m^{-1}$。
> したがってこの仮定の下でのみ $(\ast)\iff\theta(E_m)=E_m^{-1}$。

**証明.**
**(i)** $b:=-\lambda E_m$ と置く。$E_m\in A^\sigma$ ゆえ $\mathcal N(b)=-\lambda\cdot3E_m=-E_m$。また $(1+\theta)b=-\lambda(E_m+\theta E_m)=-\lambda(E_m-E_m)=0$。ゆえに $b\in\ker(1+\theta)$ かつ $\mathcal N(b)=-E_m$、すなわち $-E_m\in\mathcal N(\ker(1+\theta))$。補題 E15.0 より $(\ast)$。$\theta$ に関する仮定は一切使っていない。∎
**(ii)** $\theta\mathcal N=\mathcal N\theta$ なら $\theta(A_+)=A_+$、$\theta(A_-)=A_-$、したがって
$$ \ker(1+\theta)=\bigl(\ker(1+\theta)\cap A_+\bigr)\oplus\bigl(\ker(1+\theta)\cap A_-\bigr),\qquad
\mathcal N\bigl(\ker(1+\theta)\bigr)=3\bigl(\ker(1+\theta)\cap A_+\bigr)=\ker(1+\theta)\cap A_+ $$
($3$ が $A$ 上可逆)。$E_m\in A_+$ ゆえ $-E_m\in\mathcal N(\ker(1+\theta))\iff(1+\theta)E_m=0$。∎

> **補題 E16.2(仮定の書き下し).** $\psi:=\iota\sigma^{-1}$ と置くと $\theta\mathcal N\theta=1+\psi+\psi^2$。したがって
> $$ \mathcal N\theta=\theta\mathcal N \iff \iota\sigma^{-1}+(\iota\sigma^{-1})^2=\sigma+\sigma^2 \quad\text{on }A. $$
> 特に $\iota\vert_A=\mathrm{id}$(厳密 $S_3$)なら成立する。

**証明.** $\theta\sigma\theta=\psi$、$\theta\sigma^2\theta=(\theta\sigma\theta)^2=\psi^2$。$\theta^2=1$ より $\theta\mathcal N\theta=1+\psi+\psi^2$、これが $\mathcal N$ に等しいことと $\mathcal N\theta=\theta\mathcal N$ は同値。∎

> **系 E16-a(生存・変更なし).** $\mathrm{class}(P)\le2$ なら系 E2′-a より $\iota\vert_A=\mathrm{id}$、補題 E16.2 より命題 E16 の仮定が成立。さらに $A=\langle w\rangle$、$E_m=w^{-T_m}$、$\theta(w)=w^{-1}$ ゆえ $\theta(E_m)=E_m^{-1}$。したがって $(\ast)$。∎
> (なお (i) が無仮定なので、**class $\le2$ の結論は命題 E16 の仮定を経由せずとも出る**。)

> **【GAP-E16】(v3 で鋭化).** class $\ge3$ の許容対象で $\mathcal N\theta=\theta\mathcal N$(補題 E16.2 の等式)が成立し得るか。v2 は「$\theta(A^\sigma)$ が安定か」を問うていたが、**それでは足りない**ことが §2.1 で判明した。正しい問いは上の等式である。**UNKNOWN。**

---

## 3. 補題 E18.2 の証明語句の修復(便 13 F5)

> **補題 E18.2(v3).** $M$ を有限 2-primary $\mathbb Z_2$-加群、$\bar\sigma$ が $M$ 上 $1+\bar\sigma+\bar\sigma^2=0$ を満たし、$\bar\theta\bar\sigma\bar\theta=\bar\sigma^{-1}$、$\bar\theta^2=1$ とする。このとき $\widehat H^*(\langle\bar\theta\rangle,M)=0$、すなわち
> $$ \ker(1+\bar\theta)=(1-\bar\theta)M,\qquad \ker(1-\bar\theta)=M^{\bar\theta}=(1+\bar\theta)M. $$

**証明(語句を修復した版).** $M$ の指数を $2^e$ とし $R_e:=(\mathbb Z/2^e)[\omega]=(\mathbb Z/2^e)[X]/(X^2+X+1)$ と置く。$1+\bar\sigma+\bar\sigma^2=0$ より $M$ は $R_e$-加群であり、$\bar\theta\bar\sigma\bar\theta=\bar\sigma^{-1}$ は $\bar\theta$ が $R_e/(\mathbb Z/2^e)$ の Galois 群(Frobenius $\omega\mapsto\omega^2$)に沿って**半線型**であることを意味する。$\mathbb Z_2\subseteq\mathbb Z_2[\omega]$ は**不分岐**なので、この Galois 拡大の crossed product は
$$ R_e\#\langle\bar\theta\rangle \;\cong\; \mathrm{End}_{\mathbb Z/2^e}(R_e)\;\cong\;M_2(\mathbb Z/2^e) $$
であり(Galois 降下 / Wedderburn の crossed product 定理の可換環版)、この環は $R_e$ と **Morita 同値**である。したがって任意の $R_e\#\langle\bar\theta\rangle$-加群は
$$ M\;\cong\;R_e\otimes_{\mathbb Z/2^e}N,\qquad N:=\mathrm{Hom}_{R_e\#\bar\theta}(R_e,M) $$
の形をもつ。一方、不分岐拡大には**正規整基底**があるので、$C_2=\langle\bar\theta\rangle$-加群として $R_e\cong(\mathbb Z/2^e)[C_2]$、したがって $M\cong(\mathbb Z/2^e)[C_2]\otimes_{\mathbb Z/2^e}N$ は $C_2$ から **induced** な加群である。induced 加群の Tate コホモロジーは消える(Shapiro)。∎

> **v2 からの訂正(便 13 F5 / Errata 4)**: v2 の「行列環 $M_2(\mathbb Z_2)$ の単純加群は $R$ のみ」「任意の加群は $\mathbb Z_2[C_2]$-**自由**」は誤り($M_2(\mathbb Z_2)$ は半単純でなく、有限 torsion 加群は $\mathbb Z_2[C_2]$-自由でない)。**必要なのは free ではなく induced** である。結論は変わらない。

---

## 4. 定理 E18 の再定式化 — 障害群は $C_j=(M_j^{\bar\sigma})^{\bar\theta}$(便 13 F6・裁定 13 §2)

### 4.1 設定と補題 E18.1(変更なし)

$P$ 2 生成有限 2 群、$A=[P,P]$ 可換、$\gamma_j:=\gamma_j(P)$、$M_j:=\gamma_j/\gamma_{j+1}$。

> **補題 E18.1(PASS・再掲).** 任意の $g\in P$ について $(\iota_g-1)\gamma_j=[\gamma_j,g]\subseteq\gamma_{j+1}$。ゆえに $\iota_{X^u}$ と $\mathrm{Ad}(\bar Y^m)$ は $M_j$ 上恒等に作用し、$M_j$ 上では $\bar\theta\bar\sigma\bar\theta=\bar\sigma^{-1}$、$\bar\theta^2=\bar\sigma^3=1$ — **$\langle\bar\sigma,\bar\theta\rangle$ は真に $S_3$ を通す**。

$3$ は $M_j$ 上可逆なので $M_j=M_j^+\oplus M_j^-$、$M_j^+:=M_j^{\bar\sigma}$、$M_j^-:=\ker\bar{\mathcal N}$、この分解は $\bar\theta$-安定($\bar\theta\bar{\mathcal N}\bar\theta=\bar{\mathcal N}$)。

### 4.2 定理 E18(v3・正しい局所 cokernel)

> **定理 E18 (v3).** 重み $j$ の段で、現在の $(1+\theta)$-欠損 $\varepsilon$ と $\mathcal N$-欠損 $\delta$ を補正 $g\in M_j$ で消す問題を考える。目標群は
> $$ T_j:=M_j^{\bar\theta}\oplus M_j^{+}\qquad(\varepsilon\in M_j^{\bar\theta}\text{ は自動、}\delta\in M_j^{+}\text{ も自動}) $$
> であり、$\Psi_j:M_j\to T_j$、$g\mapsto\bigl((1+\bar\theta)g,\ \bar{\mathcal N}g\bigr)$ に対し
> $$ \boxed{\ \operatorname{coker}\Psi_j\;\cong\;C_j:=(M_j^{\bar\sigma})^{\bar\theta}\ } $$
> であり、$(\varepsilon,\delta)$ の**障害元**は
> $$ \boxed{\ \mathrm{ob}_j(\varepsilon,\delta)\;=\;\varepsilon_+-\lambda(1+\bar\theta)\delta\;\in\;C_j\ }\qquad(\lambda=3^{-1}) $$
> である。**$M_j^-$ 成分は補題 E18.2 により常に解消される** — これが graded 解析の正味の成果である。

**証明(独立に再構成し Sol と一致).** $g=g_++g_-$ と分けると $\bar{\mathcal N}g=3g_+$ なので、第二成分の一致は $g_+=\lambda\delta$ を**強制**する。すると
$$ (1+\bar\theta)g=\underbrace{\lambda(1+\bar\theta)\delta}_{\in M_j^+}+\underbrace{(1+\bar\theta)g_-}_{\in M_j^-}. $$
$\varepsilon\in M_j^{\bar\theta}$ を $\varepsilon_++\varepsilon_-$ と分けると $\varepsilon_\pm\in(M_j^\pm)^{\bar\theta}$。よって
- $M_j^-$ 成分: $\varepsilon_-\in(1+\bar\theta)M_j^-$ が必要十分。補題 E18.2 より $(M_j^-)^{\bar\theta}=(1+\bar\theta)M_j^-$ なので**常に成立**。
- $M_j^+$ 成分: $\varepsilon_+=\lambda(1+\bar\theta)\delta$ が必要十分。

したがって $\Phi:T_j\to(M_j^+)^{\bar\theta}$、$(\varepsilon,\delta)\mapsto\varepsilon_+-\lambda(1+\bar\theta)\delta$ は well-defined($(1+\bar\theta)\delta$ は $\bar\theta$-固定)、$\ker\Phi=\operatorname{im}\Psi_j$、かつ $\Phi(h,0)=h$ ゆえ全射。∎

> **v2 の $O_j$ が誤りである最小反例(Sol F6・独立に検算).** $M=C_2$、$\bar\sigma=1$、$\bar\theta=1$($=-1$)。$M^+=M$、$M^-=0$。v2 の $O=(1+\bar\theta)M=2M=0$ だが、$(\varepsilon,\delta)=(1,0)$ は $g_+=\lambda\cdot0=0$ を強制し $(1+\bar\theta)g=0\ne1$。ゆえに $\operatorname{im}\Psi$ に入らない。真の cokernel は $C=(M^+)^{\bar\theta}=M=C_2\ne0$。**$O_j$ は「強制される欠損の像」であって障害群ではない。**

### 4.3 ★ 有限 2 群では潜在障害群はほぼ常に非零(本稿の追加・便 13 F6/W107 の帰結の鋭化)

> **系 E18.3(v3・新設).** $M_j$ が有限 2 群のとき
> $$ \boxed{\ C_j=0 \iff M_j^{\bar\sigma}=0\ } $$

**証明.** ($\Leftarrow$) 自明。($\Rightarrow$) $M_j^{\bar\sigma}\ne0$ とする。$\langle\bar\theta\rangle\cong C_2$ が有限 2 群 $M_j^{\bar\sigma}\ne0$ に作用しているので、軌道分解より
$$ \lvert M_j^{\bar\sigma}\rvert\equiv\lvert(M_j^{\bar\sigma})^{\bar\theta}\rvert \pmod 2 $$
(自明でない軌道は長さ 2)。左辺は偶数、右辺は $0\in(M_j^{\bar\sigma})^{\bar\theta}$ ゆえ $\ge1$、したがって $\ge2$。∎

> **★ この系が意味すること(v2 の楽観の完全な撤回).**
> 1. **「$\bar\theta=-1$ on $M_j^+$」は障害消滅を与えない。** $\bar\theta=-1$ なら $(M_j^+)^{\bar\theta}=M_j^+[2]$ であり、これは $M_j^+\ne0$ なら必ず非零。「符号作用 $-1$」と「固定点なし」は有限 2 群では**同義でない**(位数 2 元上で $-1=+1$)。
> 2. **表 1 の $\dim M_j^{\bar\sigma}$ が非零な全ての $j$ で $C_j\ne0$。** metabelian 表 1(b) では $j=2,4,5,6,7,\dots$ の全てで $M_j^+\ne0$、したがって $C_j\ne0$。**ところが $j=2,3,4$ は定理 E9′ により実際には可解である**(紙で閉じている)。すなわち **$C_j\ne0$ は「障害が起き得る」ですらなく、単に「この方法では何も言えない」を意味する**。
> 3. ゆえに **graded 解析から得られる正味の情報は「$M_j^-$ 成分は常に消える」の一点のみ**であり、判定には**障害元 $\mathrm{ob}_j(\varepsilon,\delta)$ を実際に計算する**しかない。v2 §3.2 の「$O_j=0\iff$ 自明表現なし」を安全基準に使う路線は**閉じている**。

> **【GAP-E18】(v3 で書き直し).** 逐次近似の各段で $\mathrm{ob}_j=0$ が全ての $j$ で成り立てば大域解が存在するか(持ち上げの二次障害の制御)。v2 と同じく **UNKNOWN**。ただし v3 では、class-5 の具体的対象について**この二次障害を明示的に定式化した**(`docs/命題_E22三段判定_v1.md`)。

---

## 5. weight 5 初出 — 射程を限定した登録(便 13 F7・P144・W107)

自由 Lie 環の Witt 指標 $\chi_{L_n}(g)=\frac1n\sum_{d\mid n}\mu(d)\chi_V(g^d)^{n/d}$ を独立に再計算した($V$ = $S_3$ の 2 次元標準表現、$\chi_V=(2,-1,0)$):

| $j$ | $\chi_{L_j}$ | 自明の重複度 | $\mathrm{sgn}$ の重複度 | $\dim(M_j^+\otimes\mathbb Q)$ |
|---|---|---|---|---|
| 2 | $(1,1,-1)=\mathrm{sgn}$ | 0 | 1 | 1 |
| 3 | $(2,-1,0)=V$ | 0 | 0 | 0 |
| 4 | $(3,0,-1)$ | 0 | 1 | 1 |
| **5** | $(6,0,0)$ | **1** | 1 | 2 |

自由 metabelian 側 $M_j\otimes\mathbb Q\cong\mathrm{Sym}^{j-2}(V)\otimes\mathrm{sgn}$ も独立に確認($j=2$: $\mathrm{sgn}$、$j=3$: $V$、$j=4$: $(3,0,-1)$、$j=5$: $(4,1,0)$ ⇒ 自明の重複度 $0,0,0,\mathbf1$、$j=6$: $(5,-1,-1)$ ⇒ 0)。**両塔とも自明表現の初出は weight 5** である。

> **採用する主張(P144)**: torsion-free universal lattice を $\mathbb Q$ 化したとき、$(M_j^{\bar\sigma})^{\bar\theta}\otimes\mathbb Q$ の初出は **weight 5**。これは **class 5 を第一撃にする強い構造的理由**である。

> **採用しない主張(W107・v2 D5 の撤回部分)**: 「$j\le4$ で graded 自明表現がないことから、有限 2 群上の同時方程式が解ける」。理由は §4.3 の系 E18.3(有限 2-torsion では符号成分にも固定点 $M[2]$ がある)と、【GAP-E18】が未閉鎖であることの二つ。**表 1 は E9/E9′ の構造的説明であって、独立な再証明ではない。**

---

## 6. 定理 E19 — 撤回と修理(便 13 F8/F10/W108)

### 6.1 定理 E19 本体の札

> **定理 E19(札のみ更新).** 自由 metabelian rank-2 対象 $A_c=\mathbb Z[S,T]/(S,T)^{c-1}$($3\le c\le7$)、$0\le m\le63$ について、`docs/scout/metab.mjs` は「基本因子が全て奇数」かつ「$\mathbb Q$-可解」を出力する。
> 札 = $\ \texttt{Z2-solvable candidate (single system, statically audited)}$。**cross-checked ではない**。理由(便 13 F8):内蔵 `snf` は canonical Smith 形ではなく整数対角化であり、列変換 $V$ の保存も unimodularity の事後検査も `elementary_divisors` の全出力もない。⇒ 二系統化は `docs/week4-E19二系統化指示書_v1.md`。

### 6.2 系 E19-b の撤回と ★ 命題 E19-b′(修理・本稿の主要な新結果)

**撤回**: v2 系 E19-b の推論「$M(m)\bmod2$ が $m\bmod8$ にしか依らない $\Rightarrow$ 基本因子が全ての $m$ で奇数」は誤り。理由(便 13 F10・独立に追認): 「全ての非零基本因子が奇数」は
$$ \operatorname{rank}_{\mathbb Q}M(m)=\operatorname{rank}_{\mathbb F_2}M(m) $$
と**同値**であり、右辺は mod 2 行列で決まるが**左辺は決まらない**。Sol の $D(t)=\mathrm{diag}(1,2t)$ はこの点を正確に突いている。

しかし、**$M(m)$ の成分が $m$ の多項式である**という事実を使えば、有限個の標本点から全 $m$ を制御できる。

> **命題 E19-b′(有限判定・本稿で新設).** $c$ を固定し、$n:=\binom c2$、$d:=2(c-2)$ と置く。
> **(a) 次数上界**: $M(m)$ の成分は $m$ の整数係数多項式で次数 $\le d$、$b(m)=-E_m$ の成分は次数 $\le c$。
> **(b) 周期性**: $M(m)\bmod2$ は $m\bmod8$ にのみ依存($c\le7$ ゆえ Lucas より)。したがって $r_{\bar m}:=\operatorname{rank}_{\mathbb F_2}M(m)$ は剰余類 $\bar m\in\mathbb Z/8$ の関数。
> **(c) 有限判定**: ある剰余類 $\bar m$ について、$K+1$ 個の標本 $m=\bar m,\bar m+8,\dots,\bar m+8K$ すべてで
> $$ \operatorname{rank}_{\mathbb Q}M(m)=\operatorname{rank}_{\mathbb Q}[\,M(m)\mid b(m)\,]=r_{\bar m} $$
> が成り立ち、かつ $K\ \ge\ (r_{\bar m}+1)\,d+c$ ならば、**その剰余類の全ての $m\in\mathbb Z$** について
> $$ \operatorname{rank}_{\mathbb Q}M(m)=\operatorname{rank}_{\mathbb F_2}M(m)=\operatorname{rank}_{\mathbb Q}[M(m)\mid b(m)]=r_{\bar m}, $$
> すなわち **(i) 全ての非零基本因子が奇数、(ii) $\mathbb Q$-可解、したがって (iii) $\mathbb Z_2$-可解**(= 全ての $j$ で mod $2^j$ 可解)。

**証明.**
**(a)** $\sigma_m=(1+T)^m\cdot\tau$ の行列成分は $\binom mi$($0\le i\le c-2$)の $\mathbb Z$-結合ゆえ次数 $\le c-2$。$\sigma_m^2$ は次数 $\le2(c-2)=d$、$\mathcal N=1+\sigma_m+\sigma_m^2$ も次数 $\le d$、$(1+\theta)$ は定数。$E_m$ の座標は $c$ 以下の次数の binomial の $\mathbb Z$-結合(class-4 の閉形 $\bigl(-\binom{m+1}2,\binom{m+2}3,-\binom{m+1}3,-\binom{m+3}4,\binom{m+2}4,-\binom{m+1}4\bigr)$ はその $c=4$ の場合)。
**(b)** Lucas より $\binom mi\bmod2$ は $i<2^L$ のとき $m\bmod2^L$ のみに依存。$c\le7$ ゆえ $i\le c-2\le5<8$、$L=3$。$M(m)\bmod2$ の成分は $\binom mi\bmod2$ の多項式なので $m\bmod8$ にのみ依存。
**(c)** $m=\bar m+8k$ と置くと、$M(m)$ と $[M(m)\mid b(m)]$ の成分は $k$ の多項式で次数はそれぞれ $\le d$、$\le\max(d,c)$。$r:=r_{\bar m}$ と置く。$[M\mid b]$ の任意の $(r+1)\times(r+1)$ 小行列式は $k$ の多項式で、次数は
$$ \le \max\bigl((r+1)d,\ rd+c\bigr)\le (r+1)d+c $$
標本点 $k=0,\dots,K$ で $\operatorname{rank}_{\mathbb Q}[M\mid b]=r$ ゆえ全ての $(r+1)$-小行列式が消える。零点の個数 $K+1>(r+1)d+c$ が次数を超えるので、**各小行列式は恒等的に零**。したがって $\operatorname{rank}_{\mathbb Q(k)}[M\mid b]\le r$、特殊化で rank は増えないので全ての $k\in\mathbb Z$ で $\operatorname{rank}_{\mathbb Q}[M(m)\mid b(m)]\le r$。
一方 $\operatorname{rank}_{\mathbb Q}M(m)\ge\operatorname{rank}_{\mathbb F_2}M(m)=r$((b) より剰余類上一定)。挟み込みで
$$ r\le\operatorname{rank}_{\mathbb Q}M(m)\le\operatorname{rank}_{\mathbb Q}[M(m)\mid b(m)]\le r $$
ゆえ三者すべて $=r$。**(i)**: 非零基本因子の個数 $=\operatorname{rank}_{\mathbb Q}$、うち奇数のものの個数 $=\operatorname{rank}_{\mathbb F_2}$、両者一致ゆえ全て奇数。**(ii)**: $\operatorname{rank}[M\mid b]=\operatorname{rank}M$ は $\mathbb Q$-可解と同値。**(iii)**: Smith 判定 $\bigl(v_2(c_i)\ge v_2(d_i)\ (i\le r)$ かつ $c_i=0\ (i>r)\bigr)$ において、(i) より $v_2(d_i)=0$ で第一条件は恒真、第二条件は (ii) と同値。∎

> **★ 検算結果(`docs/scout/metab_rank.mjs`・本稿の新規スクリプト).** 上の判定基準を実際に走らせた。各剰余類で $\operatorname{rank}_{\mathbb Q}M$、$\operatorname{rank}_{\mathbb F_2}M$、$\operatorname{rank}_{\mathbb Q}[M\mid b]$ を全標本で計算し、必要標本数 $(r+1)d+c+1$ を満たすまで走らせた結果:
>
> | $c$ | $n=\binom c2$ | $d=2(c-2)$ | 観測 rank $r$(全剰余類共通) | 必要標本数/類 | 走らせた範囲 | 判定 |
> |---|---|---|---|---|---|---|
> | 3 | 3 | 2 | **2** | 10 | $m=0..80$(10–11/類) | **CLOSED** |
> | 4 | 6 | 4 | **4** | 25 | $m=0..260$(32–33/類) | **CLOSED** |
> | 5 | 10 | 6 | **8** | 60 | $m=0..480$(60–61/類) | **CLOSED** |
> | 6 | 15 | 8 | **11** | 103 | $m=0..900$(112–113/類) | **CLOSED** |
> | 7 | 21 | 10 | **16** | 178 | $m=0..63$ のみ(8/類) | **UNKNOWN** — $m\le1423$ まで走らせれば閉じる |
>
> ⇒ **$c=3,4,5,6$ については、$m\le63$ ではなく全ての $m\in\mathbb Z$ について $\mathbb Z_2$-可解かつ $\mathbb Q$-可解が確定した**(命題 E19-b′ + 上の計算)。**$c=6$ は v2 の定理 E19 が $m\le63$ でしか主張できなかった層であり、$m$ 量化子が初めて閉じた。**
> ⇒ **$c=7$ も rank は $m=0..63$ の全剰余類で一定($16$)であり、必要な標本数($178$/類 ⇒ $m\le1423$)まで走らせるだけで閉じる見込み — 有限・実行可能**(指示書 §4.2 に正確なコマンドと上限を記載)。
> **札 = `candidate`(単系統)**。本スクリプトは `metab.mjs` と**同一モデルのコードを共有**しており(意図的・rank という別量を測る補助計算)、**第二系統ではない**。二系統化の対象に含めること(指示書 §4)。

> **系 E19-c(v3・射程を明示).** 命題 E10(v2 §2)より、**2 生成 metabelian 2 群で class $\le5$ の許容対象は、全ての charming $m$ で torsion-full**(指数 $2^j$ は任意)。class $6,7$ は $m\le63$ の範囲で candidate、全 $m$ は UNKNOWN。

### 6.3 便 12 ★ への最終回答(射程の確定・W109/F11)

**採用する**:
> `metab.mjs` の結果が第二系統と一致すれば、自由 metabelian $c\le7$、$m\le63$ では高い 2 冪で初出する divisibility obstruction はない。さらに **$c\le6$ については命題 E19-b′ により全 $m\in\mathbb Z$ へ拡張される**。

**採用しない(v2 D7 / §3.5(i) の撤回)**:
- 「全 metabelian 塔に 2-primary obstruction は存在しない」— **反駁**(metabelian class $\ge8$ は UNKNOWN)。
- 「class $\le7$ の全 $m$ で存在しない」— **UNKNOWN**($c=7$ は E19-b′ の標本が未取得。$c\le6$ は取得済み)。
- 「素数 2 は完全に落ちた」— **撤回**。落ちたのは $c\le6$ の metabelian 塔だけである。

---

## 7. 狩場の正しい記述(便 13 F11・裁定 13 §3)

### 7.1 盤面(v2 §3.5 の表を全面差し替え)

| 層 | 状態 | 根拠 | 札 |
|---|---|---|---|
| class $\le2$ | **閉鎖** | 命題 E16(i)(無仮定)+ 系 E16-a | 紙上・相互監査 PASS |
| class $\le4$(⇒ $A$ 可換) | **閉鎖** | 定理 E9′・(†)(§1) | paper mutual-audit PASS / candidate |
| metabelian $c\le6$、**全 $m\in\mathbb Z$**、全指数 $2^j$ | **閉鎖(単系統)** | 定理 E19 + **命題 E19-b′**(§6.2) | candidate(単系統・二系統化待ち) |
| metabelian $c=7$、$m\le63$、全 $j$ | candidate | 定理 E19 | candidate(単系統) |
| metabelian $c=7$、**全 $m$** | **UNKNOWN(ただし有限・実行可能)** | E19-b′ の標本未取得($m\le1423$ で閉じる見込み) | UNKNOWN |
| **metabelian class $\ge8$** | **UNKNOWN** | 8GB 制約で未計算 | UNKNOWN(盤面に残す) |
| **$A$ 非可換(導来長 $\ge3$・class $\ge5$)** | **UNKNOWN・第一優先** | weight-5 初出(§5)+ 三つの武器が同時失効 | UNKNOWN |

> **★ v2 の「唯一の生きた層」は撤回する。** 正しくは:
> $$ \text{class-5 非 metabelian}\;=\;\textbf{現在もっとも情報価値の高い第一優先層} $$
> であって唯一ではない。**metabelian class $\ge8$、$c=7$ の全 $m$、および E19 の第二系統は生きたまま盤面に残す**(便 13 F11)。

### 7.2 なぜ第一優先か(三つの独立な理由)

1. **表現論**: 有理 lattice の $S_3$-自明成分の初出が weight 5(§5・P144)。
2. **武器の同時失効**: (a) 命題 E8 の線型化が使えない($\mathcal N$ が準同型でない)、(b) 定理 E18 の graded 解析は $A$ 可換を仮定、(c) 定理 E19 のモデル($F'/F''$ 上の加群)は $[A,A]$ を潰している。
3. **最小性**: $F_2/\gamma_6$ が **$A$ 非可換な最小の相対自由対象**($A=\gamma_2/\gamma_6$、Hirsch length 12、$[A,A]$ は階数 2 で中心)。

### 7.3 定理 E21(変更なし・PASS)

> **定理 E21.** $P$ 非可換 2 生成 2 群、$A=[P,P]$ とすると、$B:=\gamma_3[A,A]A^2$ による商 $A/B\cong C_2$ は常に $\langle\sigma,\theta\rangle$-自明加群。ゆえに非自明な同時安定 1 次元指標が常に存在し、**系 E12-a の仮定は本設定では決して満たされない**。

便 13 F12 が PASS を出した。「E12-a を安価な safe criterion として使う道は本設定では閉じている」を CLAIMS へ登録する際は**適用可能性 = 空**を併記(P146)。

---

## 8. 【GAP】表・状態札・文献要請(v3)

### 8.1 【GAP】表(v2 §5.1 からの差分)

| # | 内容 | v3 での状態 |
|---|---|---|
| **【GAP-E2】** | 一般の同時可解性 | 本丸 = $A$ 非可換。**正しい定式化 = 三段判定(線型部+二次形式部+cocycle 部)** — `docs/命題_E22三段判定_v1.md` で完成 |
| **【GAP-E13】** | class $\ge5$ の判定 | metabelian は $c\le6$ 全 $m$ 閉鎖(単系統)/ $c=7$ 部分 / $c\ge8$ UNKNOWN。非 metabelian は【GAP-E2】と合流 |
| **【GAP-E15】** | 予想 E15 の真偽 | **反証されず**。射程: class $\le4$ 紙上、metabelian $c\le6$ 全 $m$(単系統)。残るのは $c=7$ の $m$ 量化子・class $\ge8$・$A$ 非可換 |
| **【GAP-E16】** | 命題 E16 の仮定 | **問いを鋭化**: $\iota\sigma^{-1}+(\iota\sigma^{-1})^2=\sigma+\sigma^2$ が class $\ge3$ で成立し得るか。**UNKNOWN** |
| **【GAP-E18】** | 定理 E18 の逆 | **UNKNOWN**。§4.3 により「$C_j$ の消滅」からは何も出ない($C_j\ne0$ がほぼ常に成立)ので、逆は障害元 $\mathrm{ob}_j$ の逐次制御としてのみ意味をもつ |
| **【GAP-E19】** | $\mathbb Q$-可解性の全 $m$ | **$c\le6$ は命題 E19-b′ で閉鎖(単系統)**。$c=7$ は標本取得待ち(有限・実行可能・$m\le1423$)。$c\ge8$ は 8GB 制約 |
| **【GAP-E20】** | $A$ 非可換な許容 2 群の最小位数 | **UNKNOWN**($\ge2^7$ と見込む) |
| **【GAP-E22】(新設)** | 三段判定の第三段(中心補正の値域)が class-5 普遍対象で空でないか | **UNKNOWN** — 掃引 ① r2 の主目標 |

### 8.2 状態札(W60/W92 準拠)

| 主張 | 札 |
|---|---|
| Lemma A / Lemma B / (†) / 定理 E9′ | **paper mutual-audit PASS / candidate**(便 13 F1–F3) |
| 補題 E10.1 / 命題 E10 全称版 | 紙上証明(Opus 単独・Sol 未監査) |
| 命題 E16 (v3) / 補題 E16.1 (v3) / 補題 E16.2 / 系 E16-a | **紙上証明**(v3 新規・Sol 未監査。Sol の反例は独立検算済み) |
| 補題 E18.1 / 補題 E18.2 (v3) | PASS(便 13 F5・語句修復済み) |
| **定理 E18 (v3)**($C_j$ 版) | 便 13 F6 と本稿で**独立に同じ結論**(相互監査 PASS 相当・candidate) |
| **系 E18.3**($C_j=0\iff M_j^{\bar\sigma}=0$) | **紙上証明**(v3 新規・Sol 未監査) |
| 表 1(a)(b)・weight 5 初出 | 紙上証明(指標公式・独立再計算で一致)。**射程は有理係数のみ** |
| 定理 E19($c\le7,m\le63$) | `Z2-solvable candidate (single system, statically audited)` |
| **命題 E19-b′**(有限判定) | **紙上証明**(v3 新規・Sol 未監査) |
| **E19-b′ の適用結果($c=3,4,5,6$ 全 $m$)** | **candidate(単系統)** — `metab_rank.mjs`($c=6$ は $m=0..900$・112–113 標本/類) |
| 系 E19-b(v2) | **撤回(refuted as stated)** |
| 定理 E21 / 命題 E20 | PASS(便 13 F12) |
| 補題 E22(積公式) | PASS(便 13 F13・独立に再導出) |
| 予想 E15 | **予想**。safe フィルタに使わない(W42) |
| verified(Lean) | **本稿には一つもない** |

### 8.3 【文献要請 6″】(6′ を差し替え)

> **困難**: 有限 class-2 群 $A$($C:=[A,A]\subseteq Z(A)$、$C$ の階数 2)と、位数 3 の(mod inner)自己同型 $\sigma$、対合 $\theta$ に対し、二つの**中心値二次写像**
> $$ q_\theta(\bar f)=\theta(s\bar f)\,s\bar f,\qquad q_N(\bar f)=E_m\,\sigma^2(s\bar f)\sigma(s\bar f)\,s\bar f \qquad(s:\bar A\to A\text{ は section}) $$
> の**同時値域**が、線型部の解空間 $\mathcal L=\bar f_0+K$ 上で、部分群 $\operatorname{im}\Lambda\subseteq C\times C$($\Lambda(z)=((1+\theta)z,\mathcal N z)$)と交わるかを判定したい。**特に本設定では $\mathcal N\vert_C=0$ が構造的に成り立つ**(`命題_E22三段判定_v1.md` 系 3.4)ので、$q_N$ は中心補正で一切修正できない。
> **欲しい結果の型**: (i) 有限アーベル群($\mathbb Z/2^j$ 係数、体でない)に値をとる**対の二次形式**の同時表現可能性の判定法。(ii) 二次形式が一つでなく**組**であるときの Witt 型 / Arf 型不変量、あるいは「同時値域が部分群と交わらない」ための障害。(iii) 中心拡大 $1\to C\to A\to\bar A\to1$ の cocycle と $\langle\sigma,\theta\rangle$-作用が絡む場合の $H^2$ 的言語。
> **探す先の当たり**: 冪零群の twisted conjugacy と Reidemeister 数(Dekimpe ら)、$\mathbb Z/2^j$ 上の二次形式の分類(Wall・Kawauchi–Kojima の linking form)、有限群の cohomological quadratic map(Baues の quadratic functor)。
> **★ 探さなくてよい方向(潰した)**: (a) Burkhart 型の非 coprime 不動点定理、(b) $S_3$ の 2-modular 表現論を $A$ そのものへ適用する路線(§2)、(c) 系 E12-a 型の条件(定理 E21)、**(d) graded 障害群 $C_j$ の消滅を判定条件にする路線(系 E18.3 により空虚)**。

---

## 付録 — v2 からの訂正一覧(v2 は上書きしない)

| v2 の箇所 | 訂正 |
|---|---|
| §1.2 の $\sigma^2(p+q)$ | $-q+r_1+(m+2)r_2+2r_3$(§1)。Lemma A の結論は無傷 |
| §0 D3・§3.1 命題 E16 | 定理文を差し替え(§2.3)。仮定は $\mathcal N\theta=\theta\mathcal N$ |
| §3.1 補題 E16.1 の「$=$」 | 「$\theta(A^\sigma)\subseteq A^\sigma\iff\iota\vert_{A^\sigma}=\mathrm{id}$」へ(§2.2) |
| §3.2 補題 E18.2 の「単純加群 / 自由」 | 「Morita 同値 + normal integral basis ⇒ **induced** ⇒ Tate 消滅」へ(§3) |
| §0 D4・§3.2 定理 E18 の $O_j$ | **撤回**。$C_j=(M_j^{\bar\sigma})^{\bar\theta}$ へ(§4.2)。「$O_j=0\iff$ 自明表現なし」も撤回(§4.3) |
| §0 D5 の「E9/E9′ の再証明」 | **撤回**。構造的説明に留める(§5) |
| §0 D6 末尾・§3.3 系 E19-b | **撤回**。命題 E19-b′ へ(§6.2) |
| §3.3 系 E19-a 末尾「素数 2 は完全に落ちた」 | **撤回**。$c\le5$ に限る(§6.3) |
| §0 D7・§3.5(ii) の「唯一残った生きた層」 | **撤回**。第一優先層へ(§7.1) |
| §4 掃引宇宙 v2 | **凍結**。`docs/week4-掃引宇宙_v3.md` の新 ID へ |
| §5.2【文献要請 6′】 | 【文献要請 6″】へ差し替え(§8.3) |
