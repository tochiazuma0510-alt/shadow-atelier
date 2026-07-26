# Week 4 — 【GAP-E2】正面 作戦計画 v1

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 08 の任務 2**。
依存: `docs/week3-狩場計画_v4.md`(T2・E1–E7・E2′・E2′-a・F13 基準式・W54)・`docs/文献配達_03_scalar化_被覆_量化子.md`(Burkhart / Kawanaka–Matsuyama)・`sol/sol_reply_11_final.md` F16/F17・`sol/裁定_11_final.md` §採用 4・`docs/week1-定義ノート.md` v2(§1.5 語規約)。
原著の閲覧範囲: `papers/delivered/2308.12286.pdf`(Burkhart)を **pp.1–3(abstract・§1 序・Theorem 1・Theorem 2・§1.2 記法)まで精読**。`1811.09526`(CST)は **読んでいない**(§2.3 の理由により不要になったため)。

---

## 0. 冒頭結論(この便で確定したこと)

| # | 内容 | 札 |
|---|---|---|
| **C1** | **命題 E8**: $A = [P,P]$ が**可換**なら、E2 の交わり問題は完全に**線型代数**へ潰れる — $\mathcal S_m\cap\mathcal B_\theta \ne \varnothing \iff -E_m \in \mathcal N(\ker(1+\theta))$ | **紙上証明**(Opus 単独・Sol 未監査) |
| **C2** | **定理 E9**: $P$ が 2 生成・$\mathrm{class}(P)\le 3$・$3\nmid\lvert A\rvert$ なら、**全ての $m$** で同時解 $\bar f = w^{\lambda T_m}$ が**明示的に存在**($\lambda = 3^{-1}$、$T_m = m(m+1)/2$)。⇒ **class ≤ 3 に E2 型障害は存在しない** | **紙上証明**+**H6/H9 を独立再現**(検算 §4) |
| **C3** | **命題 E10(降下)**: $m$-full 性は許容全射に沿って**粗い側へ降りる**。⇒ 相対自由対象を一つ潰せば、その全ての許容商が一括で安全 | **紙上証明**(3 行) |
| **C4** | **定理 E9′: class ≤ 4 も閉じた**。明示 witness $\bar f = w^{\lambda T_m}(pq)^{-\lambda^2B_m}$($B_m = T_m(T_m+1)/2$)。**係数は $\mathbb Z[1/3]$ に載る** ⇒ 2 群では常に可解 | **紙上構造+厳密有理計算**(多項式次数による決定・§4) |
| **C5** | **★ 狩場の再配置**: 2 生成 2 群では $A$ 非可換 ⟺ $\mathrm{class}\ge 5$ ⟺ $\lvert P\rvert\ge 2^6$。C2+C4 と合わせ、**E2 正面の生きた最小地点は class ≥ 5**。v4 §4.1 の「$\lvert P\rvert\le 512$ の 2 群掃引」は **class ≥ 5 に絞ってよい**(残りは事前登録 PASS control) | **本稿の主張** |
| **C8** | **★★ 予想 E15(掃引の前に撃つべき)**: **2 群には E2 型障害が存在しない**かもしれない。class ≤ 4 の witness が両方とも $\mathbb Z[1/3]$-係数だったことから、**障害の唯一の素数は 3** と読める。正しければ委嘱の想定した 2 群掃引は**原理的に空振り**する | **予想**(§1.6 に falsification 計画つき)。**撤回済み H8″ と結論が似るので取り扱い注意** |
| **C6** | **Burkhart は E2 正面では原理的に無力**。作用群 $J = \langle\rho\rangle \cong C_2$ が**素数冪位数**なので Thm 1/Thm 2 の仮定「各素数 $p$ で $J$ の Sylow $p$ が不動点をもつ」は**結論と同値**になり、定理が空虚 | **紙上確定**(原文 Thm 1 と照合・§2.1) |
| **C7** | **命題 E12(選択則)**: $n_m$ の指標展開に寄与するのは $\mathrm{Irr}(A)$ のうち **$\sigma$-安定 かつ $\theta$-安定**なものだけ。Kawanaka–Matsuyama はこの $\mathcal B_\theta$ 因子の評価に入る | **紙上証明**(選択則のみ)。**係数の正規化は【GAP-E12】** |

★ **一行でいうと**: 委嘱が想定した「2 群掃引で $\mathcal S_m\cap\mathcal B_\theta = \varnothing$ の初例を探す」は正しい方向だが、**掃引すべき領域は思われていたより遥かに狭い** — class ≤ 4 は紙と計算で閉じた。掃引は **class ≥ 5** に集中させ、class ≤ 4 は**実装が正しいことを証明する control** として使う。

---

## 1. 新しい数学 — E2 の線型化

### 1.0 記法(v4 §2/§3 を継承)

$N$ を許容対象($c \in N$)、$P := PB_3/N \cong F_2/\bar N$、$A := [P,P]$、$k := \mathrm{ord}(\bar X) = N_{\mathrm{ord}}$、$u := 2m+1$。
$\theta = \mathrm{Ad}(\bar\Delta)$、$\tau = \mathrm{Ad}(\bar\delta)$(定理 T2(ii))。$A$ 上で
$$ \sigma(a) \;:=\; \bar Y^{-m}\,\tau(a)\,\bar Y^{m} \;=\; (\tau a)^{\bar Y^m},\qquad
\mathcal N \;:=\; 1 + \sigma + \sigma^2,\qquad E_m := \tau^2(\bar Y^m)\tau(\bar Y^m)\bar Y^m = \bar X^m\bar Z^m\bar Y^m \in A. $$
既知(v3 §1.1 F1): $\sigma^3 = \mathrm{Inn}_A(E_m)$、$\sigma(E_m) = E_m$。
$$ \mathcal B_\theta = \{f\in A : \theta(f) = f^{-1}\},\qquad
\mathcal S_m = \{f \in A : \mathcal N\text{-方程式 } E_m\mathcal N_m(f) = 1\ \text{の解}\}. $$

> **注意(語規約 W-1 の落とし穴 — 実装者へ)**: paper の $a^g := g^{-1}ag$ は、規約 W-1(paper 語 "AB" ↔ GAP `B*A`)の下で **GAP では `a^(g^-1)`** になる。**共役も向きが反転する。** $\sigma$ を GAP で書くときはここで必ず一度間違える。§3.4 の適合テストを先に通すこと。

### 1.1 命題 E8 — $A$ 可換なら E2 は線型代数

> **補題 E8.0.** $P$ が **2 生成**で $\mathrm{class}(P)\le 4$ ならば $A = [P,P]$ は**可換**である。逆に $A$ が非可換なら $\mathrm{class}(P)\ge 5$、したがって $\lvert P\rvert \ge 2^6$($P$ が 2 群のとき)。

**証明.** 2 生成なので $\gamma_2 = \langle w\rangle\gamma_3$($w := [X,Y]$)。ゆえに
$[\gamma_2,\gamma_2] = [\langle w\rangle\gamma_3,\ \langle w\rangle\gamma_3]$ は $[\langle w\rangle,\gamma_3]\subseteq[\gamma_2,\gamma_3]\subseteq\gamma_5$ と $[\gamma_3,\gamma_3]\subseteq\gamma_6$ の共役たちで生成されるので $\subseteq\gamma_5$。class $\le 4$ なら $\gamma_5 = 1$。
最後の主張: 2 生成 $p$ 群で $\lvert\gamma_i/\gamma_{i+1}\rvert\ge 2$($i\le c$)かつ $\lvert P/\gamma_2\rvert\ge 4$ ゆえ $\lvert P\rvert\ge 2^{c+1}$。∎

> **命題 E8($A$ 可換のときの完全判定).** $A$ を加法的に書く($\theta,\sigma$ は $\mathbb Z$-線型)。
> **(i)** $\mathcal B_\theta = \ker(1+\theta)$ は**部分群**である。
> **(ii)** $\mathcal S_m = \{f : \mathcal N(f) = -E_m\}$ は空か、$\ker\mathcal N$ の**剰余類**である。
> **(iii)** ゆえに
> $$ \boxed{\ \mathcal S_m\cap\mathcal B_\theta \ne \varnothing \iff -E_m \in \mathcal N\bigl(\ker(1+\theta)\bigr)\ } $$
> であり、非空なら $\lvert\mathcal S_m\cap\mathcal B_\theta\rvert = \lvert\ker(1+\theta)\cap\ker\mathcal N\rvert$。
> **(iv)** さらに $3\nmid\lvert A\rvert$ なら $\sigma^3 = \mathrm{Inn}_A(E_m) = \mathrm{id}$ かつ Maschke より $A = A^\sigma\oplus\ker\mathcal N$、$\mathcal N\vert_{A^\sigma} = 3\cdot\mathrm{id}$、$E_m\in A^\sigma$。したがって $\lambda := 3^{-1}\bmod\exp A$ と置くと
> $$ \mathcal S_m = -\lambda E_m + \ker\mathcal N, \qquad
> \mathcal S_m\cap\mathcal B_\theta\ne\varnothing \iff \lambda\,(1+\theta)(E_m) \in (1+\theta)\bigl(\ker\mathcal N\bigr). $$
> **障害は $\mathrm{Im}(1+\theta)\big/(1+\theta)(\ker\mathcal N)$ の中の $\lambda(1+\theta)(E_m)$ の類**という**ただ一つの明示的な不変量**である。

**証明.** (i) $A$ 可換ゆえ $\nu: f\mapsto \theta(f)f$ は準同型($\nu(fg) = \theta(f)\theta(g)fg = \theta(f)f\theta(g)g$)であり $\mathcal B_\theta = \ker\nu = \ker(1+\theta)$。
(ii) $A$ 可換なので $\mathcal N_m(f) = \sigma^2(f)\sigma(f)f = \mathcal N(f)$ は準同型。方程式 $\mathcal N(f) = -E_m$ はアフィン。
(iii) (i)(ii) から直ちに。個数は解集合が $\ker(1+\theta)\cap\ker\mathcal N$ の剰余類であることによる。
(iv) $\sigma^3 = \mathrm{Inn}_A(E_m)$ は $A$ 可換ゆえ恒等。$\langle\sigma\rangle\cong C_3$ が $A$ に作用し $3$ が可逆なので $e := \lambda\mathcal N$ は $A^\sigma$ への射影冪等元で $A = A^\sigma\oplus\ker\mathcal N$。$\mathcal N(f) = -E_m$ の $A^\sigma$-成分は $3f_+ = -E_m$、$\ker\mathcal N$-成分は自由。∎

> **系 E8-a(v4 §3 の攻撃 A/B との関係).** $A$ 可換の領域では **指標和(E4/E4′/F13)も Glauberman/Burkhart も不要**である。判定は $\lvert A\rvert$ 次元以下の整数線型代数で**完全に**決まる。指標和が本質的に要るのは **$A$ 非可換 = class ≥ 5** の領域だけである。

### 1.2 定理 E9 — class ≤ 3 は完全に閉じた

> **補題 E9.1(構造定数 — 自由 class 3 で計算・検算 §4).** $P$ 2 生成・class $\le 3$、$w := [X,Y]$、$p := [w,X]$、$q := [w,Y]$ とすると $A = \langle w\rangle\gamma_3$、$\gamma_3 = \langle p,q\rangle \le Z(P)$、$A$ 可換。さらに
> $$ \underbrace{\theta(w) = w^{-1}}_{\textbf{$F_2$ の中で厳密}},\qquad
> \underbrace{\theta(p) = q^{-1},\ \ \theta(q) = p^{-1},\ \ \tau(w) = wp^{-1},\ \ \tau(p) = q,\ \ \tau(q) = p^{-1}q^{-1}}_{A = \gamma_2/\gamma_4 \text{ の中で}(\text{class 4 では } \gamma_2/\gamma_5 \text{ でも成立 — §4})}. $$
> **★ 証明が寄りかかるのは $\theta(w) = w^{-1}$ の厳密性だけ**である($\theta$ が $F_2$ の自己同型 $x\leftrightarrow y$ ゆえ $\theta([x,y]) = [y,x] = [x,y]^{-1}$ — 商へ降ろす前に成り立つ)。残りは $A$ の中の等式で足りる。
> ゆえに $\sigma(w) = w\,q^{m}p^{-1}$、$\sigma\vert_{\gamma_3} = \tau\vert_{\gamma_3}$、**$\mathcal N\vert_{\gamma_3} = 0$**、そして
> $$ \kappa_m := \mathcal N(w) = w^{3}\,p^{-(m+2)}\,q^{\,m-1}. $$

**証明.** $\theta(w) = \theta([x,y]) = [y,x] = w^{-1}$ は $F_2$ の中の恒等式(**厳密**であって mod $\gamma_3$ ではない)。$\tau(w) = [y,z] = [y,x^{-1}] = w^{x^{-1}} = wp^{-1}$、$\tau(p) = [\tau w,\tau x] = [wp^{-1},y] = [w,y] = q$、$\tau(q) = [\tau w,\tau y] = [w,z] = [w,y^{-1}x^{-1}] = p^{-1}q^{-1}$($\gamma_3$ 中心)。$\gamma_3$ 上 $1+\tau+\tau^2$ は $p\mapsto p+q+(-p-q) = 0$、$q$ も同様ゆえ $\mathcal N\vert_{\gamma_3} = 0$。$\gamma_3$ 中心ゆえ $\mathrm{Ad}(\bar Y^{-m})$ は $\gamma_3$ 上恒等・$w\mapsto wq^{m}$、よって $d := \sigma(w)-w = mq-p$、$\sigma(d) = -mp-(1+m)q$、
$\kappa_m = \mathcal N(w) = 3w + 2d + \sigma(d) = 3w-(m+2)p+(m-1)q$。∎(**全項を Magnus 埋め込みで機械照合済み — §4**)

> **補題 E9.2(基本恒等式).** 自由 class-3 対象の $A\cong\mathbb Z^3$ において
> $$ \boxed{\ 3\,E_m \;=\; -\,T_m\,\kappa_m\ },\qquad T_m := \tfrac{m(m+1)}2 . $$

**証明.** $\sigma$ の固定部分 $A^\sigma\otimes\mathbb Q$ を求める: $\sigma(\alpha w+\beta p+\gamma q) = \alpha w + (-\alpha-\gamma)p + (\alpha m+\beta-\gamma)q$ を $=(\alpha,\beta,\gamma)$ と置くと $\beta = -\alpha(m+2)/3$、$\gamma = \alpha(m-1)/3$ — すなわち **$A^\sigma\otimes\mathbb Q$ は 1 次元で $\kappa_m$ が張る**。一方 $\sigma(E_m) = E_m$ ゆえ $E_m\in A^\sigma$、したがって $E_m = c\,\kappa_m$($c\in\mathbb Q$)。$w$-成分を比べる: mod $\gamma_3$ で $E_m \equiv w^{-T_m}$(class 2 の計算 = 定理 H6 の内容)かつ $\kappa_m\equiv w^{3}$ ゆえ $-T_m = 3c$。∎

> **定理 E9(class ≤ 3 に E2 型障害は無い).** $N$ を許容対象($c\in N$)、$P = F_2/\bar N$ を **2 生成・$\mathrm{class}(P)\le 3$**、$A = [P,P]$ が **$3\nmid\lvert A\rvert$** を満たすとする。$\lambda := 3^{-1}\bmod\exp(A)$ と置くと、**全ての $m\in\mathbb Z$** に対し
> $$ \bar f \;:=\; w^{\lambda T_m} \qquad (w = [X,Y],\ T_m = m(m+1)/2) $$
> は (H-a) と (H-b′) を**同時に**満たす。すなわち $\mathcal S_m\cap\mathcal B_\theta\ne\varnothing$。

**証明.** (H-a): $\theta(\bar f) = \theta(w)^{\lambda T_m} = (w^{-1})^{\lambda T_m} = \bar f^{-1}$(補題 E9.1 の $\theta(w) = w^{-1}$ が**厳密**であることが効く)。
(H-b′): $A$ 可換ゆえ $\mathcal N(\bar f) = \lambda T_m\,\kappa_m$。補題 E9.2 を $P$ へ押し出して $T_m\kappa_m = -3E_m$、ゆえに
$\mathcal N(\bar f) = -3\lambda E_m = -E_m = E_m^{-1}$。∎

> **系 E9-a.** $P$ が **2 群**なら $3\nmid\lvert A\rvert$ は自動。ゆえに **class ≤ 3 の許容 2 群対象は全て $m$-full(torsion 部)**である。

**既知結果との整合(独立再現)**
- **class 2 = 定理 H6**: $\gamma_3 = 1$ なので $\kappa_m = w^3$、条件は $3a\equiv T_m$ — v3 §1.4 の H6 の式そのもの ✔
- **$P_3$(位数 128)= 定理 H9**: $\lambda = 1$($3\cdot1\equiv1\bmod 2$)、$\bar f = w^{T_m}$ は $m = 0,1,2,3$ で $1, w, w, 1$ — **H9 の 8 元表の各行の第一解と完全一致** ✔。さらに §4 の独立計算が H9 の**もう一方の解**($pq$ / $wpq$)と $E_m = (1,wp,wq,1)$ も再現 ✔

### 1.3 命題 E10 — 降下(m-full は粗い側へ落ちる)

> **命題 E10.** $N \le N'$ をともに許容対象、$\pi: P = F_2/\bar N \twoheadrightarrow P' = F_2/\bar N'$ を自然な全射とする($\theta,\tau$ と可換)。$m$ が $N$ で shadow を与えるなら、$m\bmod N'_{\mathrm{ord}}$ は $N'$ で shadow を与える。すなわち
> $$ m \in \mathfrak M(N) \;\Longrightarrow\; (m\bmod N'_{\mathrm{ord}}) \in \mathfrak M(N'). $$
> **対偶**: $N'$ で $m'$ が欠損すれば、$N$ では $m'$ に合同な**全ての** $m$ が欠損する。

**証明.** $\pi$ は $\theta,\tau,\mathrm{Ad}(\bar Y^m)$ と可換、$\pi(E_m^{P}) = E_m^{P'}$、$\pi([P,P]) = [P',P']$。ゆえに (H-a)(H-b′) の解は解へ写る。生成条件 $\langle \bar X^u, \bar f^{-1}\bar Y^u\bar f\rangle = P$ も全射で保たれる。charming 条件は $N'_{\mathrm{ord}}\mid N_{\mathrm{ord}}$ より保たれる。∎

★ **使い方(掃引を桁で縮める)**: 相対自由対象(その変種の**最大**対象)で $m$-full を一度示せば、**その全ての許容商が一括で安全**。逆に、掃引で新しい対象を撃つ意味があるのは「どの既知 $m$-full 対象の商にもなっていない」対象だけである。

### 1.4 class 4 の位置 — 第一の「生きた」層は class 5

$A$ の $\mathbb Q[C_3]$-加群構造を見ると障害の余地が判る。$\gamma_i/\gamma_{i+1}$ 上で $\tau$ の指標を自由 Lie 環の公式 $\chi_{L_n}(g) = \frac1n\sum_{d\mid n}\mu(d)\chi_V(g^d)^{n/d}$($V$ = 2 次元 $C_3$-表現、$\chi_V(\tau) = -1$)で計算すると

| 層 | 階数 | 自明表現の重複度 |
|---|---:|---:|
| $\gamma_2/\gamma_3$ | 1 | **1** |
| $\gamma_3/\gamma_4$ | 2 | 0 |
| $\gamma_4/\gamma_5$ | 3 | **1** |

- **class 3**: $\dim_{\mathbb Q}A^\sigma = 1$ ⇒ $E_m\in A^\sigma$ は $\kappa_m = \mathcal N(w)$ に**比例せざるを得ない** ⇒ 補題 E9.2 ⇒ 定理 E9。**障害の余地がゼロ**なのはこの 1 次元性が理由である。
- **class 4**: $\dim_{\mathbb Q}A^\sigma = 2$ ⇒ $E_m$ が $\kappa_m$ の方向から**外れ得る** ⇒ **初めて障害の余地が生じる**。にもかかわらず、下の定理 E9′ が明示 witness で閉じる。
- **class ≥ 5**: $A$ が**非可換になり得る**(補題 E8.0)。E8 の線型判定が使えず、指標和(E4′/F13)と E12 の選択則が要る。**ここが本丸**。

> **定理 E9′(class ≤ 4 も閉じた).** $N$ 許容($c\in N$)、$P$ 2 生成・$\mathrm{class}(P)\le 4$、$3\nmid\lvert A\rvert$。$\lambda := 3^{-1}\bmod\exp A$、$T_m := \tfrac{m(m+1)}2$、$B_m := \tfrac{T_m(T_m+1)}2$ と置くと
> $$ \boxed{\ \bar f \;:=\; w^{\lambda T_m}\,(pq)^{-\lambda^2 B_m}\ }\qquad (w=[X,Y],\ p=[w,X],\ q=[w,Y]) $$
> は (H-a) と (H-b′) を**同時に**満たす。ゆえに $\mathcal S_m\cap\mathcal B_\theta\ne\varnothing$ が全 $m$ で成立する。

**証明.** (H-a): $\theta(w) = w^{-1}$($F_2$ で厳密)と、$A = \gamma_2/\gamma_5$ の中での $\theta(p) = q^{-1}$、$\theta(q) = p^{-1}$(§4 で class 4 の基底全体について確認)より $\theta(pq) = q^{-1}p^{-1} = (pq)^{-1}$($A$ 可換)、ゆえに $\bar f\in\ker(1+\theta)$。
(H-b′): 自由 class-4 対象 $A_{\mathrm{free}} = \gamma_2/\gamma_5\cong\mathbb Z^6$ において
$$ \mathcal N\bigl(w^{3T_m}(pq)^{-B_m}\bigr) \;=\; E_m^{-9} $$
が $m$ の**多項式恒等式**として成立する(両辺の成分は $m$ の次数 $\le 8$ の多項式。$m = 0,\dots,20$ の **21 点**で厳密整数照合 ✔ — §4)。**指数ベクトルを $\lambda^2$ 倍する**と、$\mathcal N$ が $\mathbb Z$-線型なので
$$ \mathcal N\bigl(w^{3\lambda^2T_m}(pq)^{-\lambda^2B_m}\bigr) = E_m^{-9\lambda^2} = E_m^{-1} \qquad(9\lambda^2\equiv1,\ 3\lambda^2\equiv\lambda \bmod \exp A) $$
となり、これが主張の $\bar f = w^{\lambda T_m}(pq)^{-\lambda^2B_m}$ である。$P$ への押し出しは命題 E10 と同じ議論($A^P$ は $A_{\mathrm{free}}$ の $\theta,\sigma$-同変な商)。∎

> **系 E9′-a.** $P$ が 2 群なら $3$ は可逆ゆえ、**class ≤ 4 の許容 2 群対象は全て $m$-full(torsion 部)**である。$P_3$(class 3・128)は $B_m$ 項が $\ker\mathcal N$ に落ちるので定理 E9 の形に退化する(整合 ✔)。

### 1.5 狩場の再配置(C5)

> 2 生成 2 群では
> $$ \lvert P\rvert \le 2^8 \ \wedge\ \mathrm{class}(P)\ge 5 \;\Longrightarrow\; \mathrm{class}(P)\in\{5,6,7\},\quad \lvert P\rvert\ge 2^6 = 64. $$
> さらに $P$ は**位数 3 の自己同型 $\tau$ を許容**しなければならない(⇒ $3\mid\lvert\mathrm{Aut}(P)\rvert$)。これは 2 群には強い制約で、たとえば位数 $\ge 16$ の極大類 2 群(二面体・半二面体・一般四元数)は $\mathrm{Aut}$ が 2 群なので**全て除外**される。⇒ **生きた宇宙は小さい。**
> なお **class ≥ 5 でも $A$ が可換なまま**のこと($P$ が metabelian)はあり、その場合は命題 E8 の線型判定が**そのまま使える**。ゆえに生きた層はさらに二分される: **metabelian class ≥ 5(安い・route L)** と **非 metabelian(高い・route T 単系統)**。

### 1.6 予想 E15 — **2 群には E2 型障害が無いのではないか**(掃引の前に撃つべき)

> **予想 E15.** $N$ を許容対象($c\in N$)、$P = F_2/\bar N$ を **2 群**とする。このとき全ての $m$ で $\mathcal S_m\cap\mathcal B_\theta\ne\varnothing$、すなわち **E2 型の $m$-欠損は 2 群には存在しない**。

**根拠(帰納であって証明ではない)**: class ≤ 4 で成立(E9/E9′)。しかも二つの witness はどちらも**係数が $\mathbb Z[1/3]$ に載る** — 自由対象の上で解が存在し、分母は $3$ の冪だけである。**障害の唯一の素数は $\tau$ の位数 $3$ に由来する**と読める。これは H8(3 ∤ |A| ⇒ (H-b′) 可解)が (H-b′) 単独で示したことの、**同時可解版**にあたる。

> **⚠ 取り扱い注意(W42 の再確認).** 予想 E15 の**結論**は、便 06 で**撤回された H8″「2 群は完全に安全」と同じ形**である。しかし**根拠は全く異なる**: H8″ は (H-b′) 単独の可解性から誤って結論した(交わりを一切見ていなかった)。E15 は class ≤ 4 の**同時解の明示 witness** から帰納している。**それでも E15 は予想であり、撤回済みの主張を復活させる根拠にはならない。** 掃引の safe フィルタに使ってはならない(W42 は生きている)。

**falsification 計画(安い順・これが本稿の一番の推奨)**

| 手 | 内容 | コスト | 結果の使い道 |
|---|---|---|---|
| **F-1** | §4 の Magnus 計算を **$D = 5$** へ拡張し、**自由 metabelian class-5 対象**($A = \gamma_2/(\gamma_6[\gamma_2,\gamma_2])$、階数 10)で解の **2-integrality** を判定 | node 数十行・数分 | 落ちれば **反例の座標が直接得られる**(掃引不要)。通れば E15 の証拠がもう一段 |
| **F-2** | 同じく **$D = 5$ の完全版**($A = \gamma_2/\gamma_6$、非可換・階数 12)で route T 相当を直接計算 | やや重い | $A$ 非可換の初例を紙の上で見る |
| **F-3** | F-1/F-2 が通ったら **掃引の宇宙を 2 群から外す**: $3\mid\lvert A\rvert$ の対象(v4 §4.2 の Q7 型)や非冪零 $P$ へ移す | 宇宙の再登録 | 予算の再配分 |
| **F-4** | F-1 が落ちたら §3 の掃引を**その座標の近傍に絞って**発射 | 小 | `m_missing` の初例 |

★ **司令塔への進言**: **§3 の掃引(GAP 実装・数時間規模)に予算を投じる前に、F-1 を撃つべきである。** F-1 は私が数十分で書ける node 計算であり、予想 E15 が正しければ掃引全体が空振りすることを**事前に**教えてくれる。これは v4 §4.1 の事前登録を撤回するのではなく、**発射順を変える**提案である。

### 1.7 命題 E12 — 指標展開の選択則($A$ 非可換用)

$\mathbb C[A]$ の中で $s_m := \sum_{f\in\mathcal S_m}f$、$b_\theta := \sum_{f\in\mathcal B_\theta}f$ と置くと $n_m^{\mathrm{tor}} = \lvert\mathcal S_m\cap\mathcal B_\theta\rvert = \langle s_m, b_\theta\rangle$。

> **命題 E12(選択則).** $\rho\in\mathrm{Irr}(A)$ に対し
> **(a)** $\rho(s_m) \ne 0 \Rightarrow \rho\cong\rho\circ\sigma$。 **(b)** $\rho(b_\theta)\ne 0 \Rightarrow \rho\cong\rho\circ\theta$。
> ゆえに Plancherel 展開
> $$ n_m^{\mathrm{tor}} = \frac1{\lvert A\rvert}\sum_{\rho\in\mathrm{Irr}(A)} d_\rho\,\mathrm{Tr}\bigl(\rho(s_m)\rho(b_\theta)^{*}\bigr) $$
> に寄与するのは **$\langle\sigma,\theta\rangle$-不変な既約指標だけ**である($\langle\tau,\theta\rangle\cong S_3$ の $\mathrm{Irr}(A)$ への作用で不変な軌道)。

**証明.** (a) $\mathcal S_m$ は $\sigma$-捻れ共役類(H8 の Schur–Zassenhaus 補群共役性)なので $\tilde s := \sum_{a\in A}\sigma(a)^{-1}f_0a$ は $s_m$ のスカラー倍。$\rho(\tilde s) = \sum_a\rho^\sigma(a)^{-1}\rho(f_0)\rho(a)$ は $\lvert A\rvert$ 倍の「$\rho\to\rho^\sigma$ の絡作用素への射影」であり、Schur の補題より $\rho\not\cong\rho^\sigma$ なら $0$。
(b) $\mathcal B_\theta$ は $\theta$-捻れ作用 $a*f = \theta(a)^{-1}fa$ で閉じる(v3 §3.1)ので $\theta$-捻れ類の合併であり、同じ議論。∎

**$A$ 可換での整合検査($P_3$)**: $\mathrm{Ann}(\mathrm{Im}(1-\sigma)) \cap \mathrm{Ann}(\mathrm{Im}(1-\theta))$ で選択則が効き、$\hat s(\chi) = \chi(f_0)\lvert\mathrm{Im}(1-\sigma)\rvert$、$\hat b(\chi) = \lvert\ker(1+\theta)\rvert$ の同時台は自明指標のみ、$n_m = \frac18\cdot4\cdot4 = 2$ ✔(H9 と一致)。

- **状態**: 選択則(a)(b)は**証明済**。**絡作用素の正規化(= 具体的係数)は未確定** ⇒ **【GAP-E12】(新設)**。ここに Kawanaka–Matsuyama の捻れ FS 指標が入る(§2.2)。

---

## 2. 攻撃武器の再評価(配達 03)

### 2.1 Burkhart(2308.12286)— **無力と確定**

原文 Theorem 1(p.2)を写す:

> Given a finite group $J$ acting via automorphisms on a finite **abelian** group $N$, suppose the induced semidirect product $N\rtimes J$ acts on some non-empty set $\Omega$ where the action of $N$ is transitive. **If for each prime $p$, a Sylow $p$-subgroup of $J$ fixes an element of $\Omega$**, then there exists some $J$-invariant element $\omega\in\Omega$.

E2 正面への当てはめ(v3 §3.2 の枠組み)は $N := A$、$\Omega := \mathcal S_m$、$J := \langle\rho\rangle$($\rho(f) = \theta(f)^{-1}$)であり、$\lvert J\rvert = 2$。

> **観察 B1(致命的).** $J$ が**素数冪位数**のとき、$J$ の Sylow $2$-部分群は $J$ 自身、他の素数の Sylow は自明である。ゆえに Theorem 1 の仮定は
> $$ \text{「$J$ が } \Omega \text{ の点を固定する」} $$
> に**帰着し、結論と同一**になる。**したがって Burkhart Theorem 1 は $J\cong C_2$ に対して空虚である。** Theorem 2($N$ 冪零・$N\rtimes J$ 超可解)も仮定の形が同じなので同様に空虚。

**帰結(v4 §3.8 の更新)**: v4 は「攻撃 B は E2′ の同変性が回復した後にしか使えない/入口が見つかっていない」と書いた。**本稿はより強く、入口が回復しても Burkhart 型は何も与えないことを確定する。** 作用群 $J$ を 2 つ以上の素数で割れる群へ**拡大**できない限り(拡大しても Sylow 2 の条件が結論と同値のまま残るので)この方向は死んでいる。

> **記帳(W-新)**: **「非 coprime 不動点定理」は、作用群が素数冪位数のときは自動的に空虚**である。E2 の $\Theta = \langle\rho\rangle\cong C_2$ はまさにこれ。**配達 03 §2 の第一弾は E2 正面から撤去する。**

### 2.2 Kawanaka–Matsuyama — **$\mathcal B_\theta$ 因子としてなら生きる**

K–M(Hokkaido Math. J. 19 (1990) 495–508)の
$$ \#\{g\in G : \theta(g) = g^{-1}\} \;=\; \sum_{\chi\in\mathrm{Irr}(G)}\varepsilon_\theta(\chi)\,\chi(1) $$
は、**$\lvert\mathcal B_\theta\rvert$ の閉じた式そのもの**である($G := A$)。ただしこれは**交わりではなく片方の集合の大きさ**しか与えない。正しい使い所は二つ。

> **補題 E11(鳩の巣フィルタ — 十分条件).**
> $$ \lvert\mathcal S_m\rvert + \lvert\mathcal B_\theta\rvert > \lvert A\rvert \;\Longrightarrow\; \mathcal S_m\cap\mathcal B_\theta \ne \varnothing. $$
> ここで $\lvert\mathcal B_\theta\rvert = \sum_\chi\varepsilon_\theta(\chi)\chi(1)$(K–M)、$\lvert\mathcal S_m\rvert = [A : C_\sigma(f_0)]$、$C_\sigma(f_0) = \{a : \sigma(a)^{-1}f_0a = f_0\}$。

**証明.** 二つの部分集合の和が全体を超えれば交わる。∎
**正直な評価**: **弱い**。$P_3$ では $\lvert\mathcal S_m\rvert + \lvert\mathcal B_\theta\rvert = 4+4 = 8 = \lvert A\rvert$ で**ちょうど届かない**(実際は交わる)。だが**指標表だけで計算できて安い**ので、掃引の前置フィルタとしては使ってよい(`pigeonhole_pass` 欄)。

> **命題 E12 との合流(委嘱が求めた「$\Sigma\varepsilon_\theta(\chi)\chi(1)$ を $\mathcal S_m$ への制限に変形する路線」の到達点).**
> K–M の指標和は、群環の言葉では $\rho(b_\theta)$ の**トレース評価**である。命題 E12 (b) により $\rho(b_\theta)\ne0$ は $\rho\cong\rho^\theta$ に限られ、その上で $\varepsilon_\theta(\rho)$ が絡作用素の符号を与える。一方 $\rho(s_m)$ は $\rho\cong\rho^\sigma$ に限られ、$\sigma$-捻れ類和として決まる。ゆえに
> $$ n_m^{\mathrm{tor}} \;=\; \frac1{\lvert A\rvert}\sum_{\substack{\rho:\ \rho\cong\rho^\sigma\\ \rho\cong\rho^\theta}} d_\rho\ \mathrm{Tr}\bigl(\rho(s_m)\,\rho(b_\theta)^{*}\bigr) $$
> が「**成層された K–M**」の正しい形である。**選択則は証明済み**、**係数(絡作用素の正規化)は未確定 =【GAP-E12】**。
> ★ **W59 の再確認**: これは行列値の式であって、**scalar character-table 公式ではない**。「K–M で E2 が指標表計算に落ちた」とは**書かない**。

### 2.3 CST(1811.09526)を読まなかった理由

配達 03 §1 第二段(Hecke 環・作用素値球関数)は、**$z_{2,C}$ が中心的でないときの scalar 化**のための道具だった。しかし §1.1 の命題 E8 により、**$A$ 可換の領域では指標和そのものが不要**になり、**$A$ 非可換の領域では先に【GAP-E12】(絡作用素の正規化)を閉じないと球関数の枠に載せられない**。したがって現時点で CST を読む情報利得はない。**未読を申告する**(必要になれば再要請)。

### 2.4 【GAP】表の更新

| # | 内容 | v4 での状態 | **本稿での状態** |
|---|---|---|---|
| **【GAP-E2】** | 一般の同時可解性 | 未解決(本丸) | **class ≤ 3 は閉鎖(定理 E9)/ class 4 は計算上閉鎖(§4)/ 本丸は class ≥ 5 = $A$ 非可換**へ縮小 |
| **【GAP-E2a】** | F13 の scalar 化 | UNKNOWN【文献要請 4】 | **$A$ 可換では moot**(E8 が直接解く)。**$A$ 非可換で継続** |
| **【GAP-E2b】** | $\iota_{X^u}$ の吸収 | 塞がっている | **恒久的に閉じる**(観察 B1 — 吸収できても Burkhart が空虚) |
| **【GAP-E2c】** | 一般の $\sigma_A$ の存在必要性 | UNKNOWN | **優先度を最低へ**(同じ理由。数学的には依然 UNKNOWN) |
| **【GAP-E12】** | 命題 E12 の絡作用素の正規化 | — | **新設・UNKNOWN**(【文献要請 7】) |
| **【GAP-E13】** | class 4・$\exp(A)\ge 32$、および class ≥ 5 の一般判定 | — | **新設・UNKNOWN**(掃引の対象) |

---

## 3. 数値実験の設計(宇宙の事前登録)

### 3.1 宇宙 U-E2(**事前登録表** — 発射前に凍結し、後から変えない)

**parametrization は系 T2-A′ に従う**(v4 §2.2): 対象 $N$ ⟷ marked quotient $(Q,\varphi,\varepsilon)$、$Q = B_3/N$、$P = \ker\varepsilon$、`exact_order_binv_a` $= 2k$。

| 項目 | 事前登録値 |
|---|---|
| $k$($=N_{\mathrm{ord}} = \mathrm{ord}\bar X$) | **$k \in \{4, 8\}$**(主)/ $k = 16$(余力があれば・**後から追加しない。追加するなら別便で別宇宙として登録**) |
| $P$ の型 | **2 群**、$2^5 \le \lvert P\rvert \le 2^8$(= 32〜256)。$\lvert Q\rvert = 6\lvert P\rvert \le 1536$ |
| **生きた層(主目標)** | **$\mathrm{class}(P) \ge 5$**(⇒ $\lvert P\rvert\ge 64$)。この層でのみ $A$ が非可換になり得る。**さらに予想 E15 が正しければこの層も空**なので、§1.6 の F-1 を先に撃つこと |
| **control 層(必ず PASS するはず)** | $\mathrm{class}(P)\le 4$ の全対象。**定理 E9 / E9′ + 命題 E10 により全て $m$-full であることが紙で確定している** |
| charming 集合 | $k$ が 2 冪ゆえ $2m+1$ は常に $k$ と互いに素 ⇒ **$\mathcal X_N = \mathbb Z/k$ 全体**(全 $m$ を撃つ) |
| 除外(事前に宣言) | class $\le 2$(H6)は撃たなくてよいが、**「安全」と記帳するのは H6 を引用してから**(W45)。$3\mid\lvert A\rvert$ は 2 群では起きない |
| **cap** | 対象あたり **60 秒**、宇宙全体 **3600 秒**、LINS の index cap **1536**。**cap 超過は UNKNOWN に倒す**(`status = "cap_exceeded"`)。cap を後から緩めるときは**別便・別宇宙 ID** |

> **★ 事前登録の心臓(裏切れない予測)**: 上の control 層について、**掃引が一件でも `m_missing` を出したら、それは発見ではなく実装バグである**(定理 E9 は紙で閉じている)。この予測を発射前に封印する。

### 3.2 対象列挙 — **二系統**(探索器の二重化)

| 経路 | 道具 | 手順 | 射程 |
|---|---|---|---|
| **E-1(正本)** | **`lins`**(Low Index Normal Subgroups) | $\Delta(2,3,2k) = \langle a,b\mid a^2,b^3,(b^{-1}a)^{2k}\rangle$ の指数 $\le 6\cdot 2^8 = 1536$ の正規部分群を列挙 → $Q := \Delta/M$ → $\varepsilon: Q\twoheadrightarrow S_3$ の存在と marking を検査 → $P := \ker\varepsilon$ が 2 群か → `exact_order_binv_a` $= 2k$ を**独立欄で**検査(W51) | $\lvert P\rvert\le 256$ を**完全**に被覆(理論上) |
| **E-2(照合)** | **`SmallGroups`**(+`autpgrp`) | $\lvert P\rvert \in\{32,64,128\}$(必要なら 256)の 2 生成 2 群を全列挙 → $3\mid\lvert\mathrm{Aut}(P)\rvert$ で粗フィルタ → $\tau\in\mathrm{Aut}(P)$ 位数 3・$\theta\in\mathrm{Aut}(P)$ 位数 2 で $(x,y,z)$ を巡回/交換する marking を探索 → $\mathrm{ord}(\bar X) = k$ を検査 | $\lvert P\rvert\le 128$ は**完全**、256 は cap つき |

> **交差検査(必須)**: E-1 と E-2 が $\lvert P\rvert\le 128$ で**同じ対象集合**(marked 同型類として)を出すこと。食い違ったら**掃引を止めて司令塔へ差し戻す**。片方だけで先へ進まない。
> **なぜ二系統か**: v4 §2.2 注意 1(W51)の「presentation の関係式は位数が**割る**ことしか課さない」型の取りこぼしは、単系統では原理的に検出できない。

### 3.3 判定器 — **二系統**(E8 線型 vs `twistedconjugacy`)

各対象・各 $m\in\mathcal X_N$ について、**独立の 2 通り**で $\lvert\mathcal S_m\cap\mathcal B_\theta\rvert$ を出す。

**route L(線型・$A$ 可換のときのみ)** — 命題 E8:
1. $A$ をアーベル群として `IndependentGeneratorsOfAbelianGroup` で座標化。
2. $\theta,\sigma$ を整数行列に。$\mathcal N := 1+\sigma+\sigma^2$、$1+\theta$。
3. $-E_m \in \mathcal N(\ker(1+\theta))$ を**整数線型代数**(Smith 標準形 / Howell 形)で判定。個数は $\lvert\ker(1+\theta)\cap\ker\mathcal N\rvert$。

**route T(捻れ共役・常に可能)** — `twistedconjugacy` パッケージ:
1. `sigma_hom := GroupHomomorphismByImages(A, A, gens, images)`(位数 3 の自己同型として `IsBijective` を確認)。
2. $f_0$: (H-b′) の解を一つ。**cap 内なら $A$ 全走査、越えるなら** `RepresentativeTwistedConjugation`。
3. `S := TwistedConjugacyClass(sigma_hom, IdentityMapping(A), f0)` — パッケージの規約は $\mathrm{tc}(g,h) = \mathrm{hom}_1(h)^{-1}\,g\,\mathrm{hom}_2(h)$(`lib/twistedconjugation.gi` で確認済み)なので $\mathrm{hom}_1 = \sigma$、$\mathrm{hom}_2 = \mathrm{id}$ で $\sigma(a)^{-1}f a$ ✔。
4. `B := Filtered(A, f -> theta(f) = f^-1)`。
5. `intersection_size := Size(Filtered(AsList(S), f -> f in B))`。

> **`routes_agree` を必須欄にする。** 不一致は**即停止**(数学ではなく実装の警報)。
> **$A$ 非可換($\mathrm{class}\ge5$)では route L が使えない** ⇒ その対象だけは route T 単系統になる。**そこは `single_route = true` を立てて記帳し、cross-checked と書かない。**(★ ここが本丸なのに単系統になる — 第二の照合器の設計は次便の課題として **P-新** に起票する。)

### 3.4 適合テスト(**発射前に必ず通す** — 語規約 W-1〜W-4 の実地確認)

| # | fixture | 期待値(**事前登録**) | 出典 |
|---|---|---|---|
| **CT-1** | A5-CONV(定義ノート §1.5.4) | $\mathrm{ev}(yx^{-1}) = (1\,2\,4)$ | 定義ノート §1.5.4 |
| **CT-2** | $P_3$(位数 128・class 3・$A\cong C_2^3$)、$k = 4$ | 各 $m\in\{0,1,2,3\}$ で $\lvert\mathcal S_m\rvert = 4$、$\lvert\mathcal B_\theta\rvert = 4$、**$\lvert\mathcal S_m\cap\mathcal B_\theta\rvert = 2$**、解は $m=0,3$ で $\{1,pq\}$・$m=1,2$ で $\{w,wpq\}$、$E_m = (1,wp,wq,1)$ | **定理 H9**(v3 §1.7)+ 本稿 §4 の独立再現 |
| **CT-3** | $Q_8$($A = C_2$)、$P_2$($A = C_2$) | $m$-full | H6/H9 |
| **CT-4** | 共役の向き | $P_3$ で $\sigma$ を GAP 実装し、$\sigma^3 = \mathrm{id}$ と $\sigma(E_m) = E_m$ を確認 | §1.0 の注意(paper $a^g$ ↔ GAP `a^(g^-1)`) |

**CT-2 を通らない実装で本番を撃たない。** これは全パイプライン(列挙 → marking → $\sigma,\theta$ → 二 route → 個数)を一度に検査する最良の fixture である。

### 3.5 出力 schema `e2-sweep-cert/v1`

```json
{
  "schema": "e2-sweep-cert/v1",
  "universe_id": "U-E2-2026-07-26",
  "object": {
    "id": "k4-P128-...", "k": 4,
    "P_order": 128, "Q_order": 768,
    "enumeration_route": "lins | smallgroups | both",
    "smallgroup_id": [128, 934],
    "nilpotency_class": 3, "derived_length": 2,
    "A_order": 8, "A_exponent": 2, "A_abelian": true, "A_invariants": [2,2,2],
    "triangle_marking": { "exact_order_binv_a": 8 },
    "s3_marking": { "convention": "delta_first", "delta_image": "(12)",
                    "deltaB_image": "(123)",
                    "simultaneous_conjugate_of_standard": true, "conjugator": "(123)" },
    "derived_product_check": { "checked": true, "abelianization_order": 16 },
    "aut_order_divisible_by_3": true
  },
  "charming_set": [0,1,2,3],
  "per_m": [{
    "m": 0, "u": 1,
    "E_m": "<element_encoding>",
    "S_m_size": 4, "B_theta_size": 4,
    "intersection_size": 2,
    "generation_pass_count": 2,
    "frobenius_N_v_m": 12, "frobenius_zero": false,
    "pigeonhole_pass": false,
    "route_linear":           { "available": true, "solvable": true, "count": 2, "witness": "..." },
    "route_twistedconjugacy": { "available": true, "solvable": true, "count": 2, "witness": "..." },
    "routes_agree": true, "single_route": false
  }],
  "m_missing": [],
  "torsion_generation_agrees": true,
  "status": "complete | cap_exceeded | halted",
  "caps": { "per_object_sec": 60, "universe_sec": 3600, "lins_index": 1536 },
  "provenance": { "gap_version": "...", "twistedconjugacy_version": "...",
                  "lins_version": "...", "input_hash": "...", "seed": null }
}
```

**schema の禁止事項(W54 — G-04 の継続)**
- **`fake_witness` 欄をこの schema に置いてはならない。** `intersection_size = 0` が証明するのは `m_missing`(= その $(N,m)$ で同時 hexagon 解が無い)までである。
- `frobenius_zero` / `m_missing` / `fake_witness` は**三つ別の語**であり、自動出力してよいのは前二者だけ。

### 3.6 W54 遵守 — `m_missing` を **fake witness へ昇格**させる手順(相対化)

委嘱は「$\mathcal S_m\cap\mathcal B_\theta = \varnothing$ の初例 = E2 型 fake の初発見」と書いたが、**W54 によりそれは直ちには fake ではない**。昇格には v4 §3.6 の必須 4 項が要る。本稿は**その具体的な取り方**を与える。

> **昇格レシピ(E2 型・class ≥ 5 用).**
> $N$ で $m'$ が欠損したとする。**粗い対象 $K$ として $P_K := P/\gamma_4(P)$(class 3 への切り捨て)を取る。**
> 1. **粗い $K$ の具体的 shadow**: **定理 E9 により $P_K$ は $m$-full** なので、任意の charming $m_0$ に対し shadow $[m_0, f_K]$ が**明示的に**($f_K = w^{\lambda T_{m_0}}$ で)存在する。個数証明は E8 (iii) の $\lvert\ker(1+\theta)\cap\ker\mathcal N\rvert$ で閉じる。 ✔ **(第 1 項が無料で揃う)**
> 2. **$m_0$ の全 lift の欠落**: $m_0\bmod K_{\mathrm{ord}}$ を持つ $\mathcal X_N$ の**全ての** $m'$ について `intersection_size = 0` を示す。⇒ `m_missing` の**全数**が要る(1 個では足りない)。
> 3. **補題 H3 の仮定リスト**((O1)–(O3)・生成性・必要な isolated 性)を対象ごとに明示。
> 4. **W34 の完全 reduction 像**を計算。
>
> ★ **この 4 項が揃うまで、証明書の名前は `m_missing` のままにする。** 昇格は**別 certificate**(`fake-cert/v1`)で、司令塔の裁定を経てから。

### 3.7 発射順(コスト昇順)

0. **【最優先・§1.6 の F-1】** 自由 metabelian class-5 対象で 2-integrality を判定する node 計算。**これが通ったら §3 の掃引は空振りする可能性が高い**(予想 E15)。GAP 実装に予算を投じる前に撃つ。
1. **CT-1〜CT-4**(適合テスト)。落ちたら止める。
2. **control 層**($\mathrm{class}\le 4$)を全部撃つ。**全て $m$-full になることを確認**(= 実装の正しさの証明。定理 E9/E9′ が紙で閉じているので、ここでの `m_missing` は**発見ではなく実装バグ**)。
3. **生きた層**($\mathrm{class}\ge 5$)。$m$ ごとに安い順: `pigeonhole_pass`(E11)→ `frobenius_zero`(E4)→ route L(metabelian なら)→ route T。
4. `m_missing` が出たら **§3.6 のレシピへ**(掃引を止めて司令塔へ報告 — 昇格は自動化しない)。

---

## 4. 検算(**私の node スクリプト・単系統・整数演算のみ**)

Magnus 埋め込み $x\mapsto 1+\xi$、$y\mapsto 1+\eta$ による自由冪零群($\mathbb Z\langle\xi,\eta\rangle/(\deg > D)$)の厳密計算。GAP も既存照合器も import しない独立実装。

| 検査 | 結果 |
|---|---|
| $A = \gamma_2/\gamma_{D+1}$ が可換($D = 3, 4$) | **PASS** ✔ |
| $\theta(w) = w^{-1}$ が **$F_2$ の中で厳密** | **PASS** ✔($\theta(p) = q^{-1}$、$\theta(q) = p^{-1}$ も) |
| $\tau(w) = wp^{-1}$、$\tau(p) = q$、$\tau(q) = p^{-1}q^{-1}$、$\tau^3 = \mathrm{id}$ | **PASS** ✔ |
| $\sigma(w) = wq^mp^{-1}$、$\mathcal N\vert_{\gamma_3} = 0$($m = 0..6$) | **PASS** ✔ |
| $\kappa_m = w^3p^{-(m+2)}q^{m-1}$($m = 0..6$) | **PASS** ✔ |
| $E_m$ の閉形 $= w^{-\binom{m+1}2}p^{\binom{m+2}3}q^{-\binom{m+1}3}$($m = -3..8$) | **PASS** ✔ |
| **補題 E9.2**: $3E_m = -T_m\kappa_m$($m = 0..8$) | **PASS** ✔ |
| **$P_3$ の再現**: $E_m = (1, wp, wq, 1)$、各 $m$ に**解 2 個**、$m=0,3\Rightarrow\{1,pq\}$・$m=1,2\Rightarrow\{w,wpq\}$ | **PASS** ✔ — **定理 H9 の 8 元表と完全一致**(独立経路) |
| class 3・相対自由 $A = (\mathbb Z/2^j)^3$、$j = 1..6$、$m$ を $0..2^{j+1}-1$ で全走査 | **全 $m$ で可解** ✔(定理 E9 と一致) |
| class 4・相対自由 $A = (\mathbb Z/2^j)^6$、$j = 1..4$($\exp A\le 16$)、$m$ 全走査 | **全 $m$ で可解** ✔ |
| **class 4・$\mathbb Q$ 上で解いて分母を検分**($m = 0..20$) | 解は $(T_m/3,\ -B_m/9,\ -B_m/9,\ 0,0,0)$ で **分母は 3 の冪のみ = 2-integral** ✔ ⇒ **全ての $j$ で mod $2^j$ 可解** |
| **定理 E9′ の閉形 witness を直接代入**($m = 0..20$・21 点) | $(1+\theta)\bar f = 0$ と $\mathcal N(\bar f) = E_m^{-1}$ が **21/21 で厳密成立** ✔(両辺 $m$ の次数 $\le 8$ ⇒ 恒等式) |
| $\theta$ が class 4 の基底上でも「反転して逆元」 | $\theta: w\mapsto w^{-1},\ p\mapsto q^{-1},\ q\mapsto p^{-1},\ r_1\mapsto r_3^{-1},\ r_2\mapsto r_2^{-1},\ r_3\mapsto r_1^{-1}$ ✔ |

スクリプト: `scratchpad/class3.mjs`(構造定数と $P_3$ 再現)・`scratchpad/class4.mjs`(class 3/4 の brute force)・`scratchpad/solve2adic.mjs`($\mathbb Z/2^j$ 上の厳密線型解法)・`scratchpad/rational4.mjs`($\mathbb Q$ 上の解と分母検分)・`scratchpad/witness4.mjs`(定理 E9′ の閉形直接検査)。**恒久化が要るなら司令塔経由で `search/` か `crosscheck/` へ移送**(本稿は数学的正本、スクリプトは検算用)。

> **状態札の分離(W60/W92 準拠)**
> - 定理 E9・命題 E8/E10/E12・観察 B1: **紙上証明**(Opus 単独)。**Sol 未監査**なので `paper mutual-audit PASS` ではない。
> - 定理 E9′(class 4): **紙上構造(E8 (iv)+E10)+ 有限点での厳密有理計算 + 多項式次数による決定**。**単系統**(node)。**cross-checked ではない**。
> - **予想 E15**: 予想。**定理でも観測でもない。**
> - $P_3$ の再現が H9 と一致: **紙上二経路一致**(H9 は Opus 起草+Sol 便 06 監査、本稿は Magnus 独立経路)。**GAP/照合器の二系統ではない。**
> - **verified(Lean)は一つもない。**

---

## 5. 未閉鎖項・要請・次の一手

### 5.1 【GAP】

- **【GAP-E13】(本丸・新設)**: class ≥ 5 での $\mathcal S_m\cap\mathcal B_\theta\ne\varnothing$ の判定。まず **metabelian class 5**(E8 が使える・F-1)、次に **$A$ 非可換**(E8 が使えない唯一の領域)。
- **【GAP-E12】(新設)**: 命題 E12 の絡作用素の正規化(= 具体的係数)。
- **【GAP-E15】(新設・最重要)**: **予想 E15**(2 群には E2 型障害が無い)の真偽。falsification 計画は §1.6。
- **【GAP-E2a/E2c】**: $A$ 非可換の領域でのみ継続。優先度は E13 の下。
- **【GAP-E2b】**: **恒久閉鎖**(観察 B1 — 吸収に成功しても Burkhart が空虚)。
- **【GAP-E14】(class 4・$\exp(A)\ge32$)は定理 E9′ により閉鎖**(起票せず — §4 の 2-integrality が全ての $j$ を一度に片付けた)。

### 5.2 【文献要請】

> **【文献要請 6】(【GAP-E13】/【GAP-E15】)** — **ただし §1.6 の F-1 を先に撃ってから出すのが順序**として正しい(F-1 が落ちれば文献は不要、通れば要請の形が変わる)。
> **困難**: 有限**冪零**群 $A$(2 群)と、$\langle\sigma,\theta\rangle\cong S_3$ に近い二つの自己同型($\sigma$ が位数 3 の捻れ、$\theta$ が位数 2)について、
> $$ \mathcal S = \{\sigma(a)^{-1}f_0a : a\in A\}\ (\sigma\text{-捻れ共役類})\quad\text{と}\quad \mathcal B = \{f : \theta(f) = f^{-1}\} $$
> **の交わりの非空性**を判定する道具が欲しい。$A$ が可換なら線型代数で完全に決まる(本稿 E8)ので、**$A$ 非可換の場合のみ**が問題。
> **欲しい結果の型**: (i) 二つの捻れが**同時に**かかった数え上げの指標和公式(絡作用素の正規化つき — Reidemeister 数の理論の「二重捻れ」版)。(ii) $S_3$ が $A$ に作用するときの「$S_3$-捻れ Reidemeister 類」の理論。(iii) **交わりが空になる最小例**(そのものずばりの反例があれば掃引が要らなくなる)。
> **探す先の当たり**: 捻れ共役性(Reidemeister theory)の群論側 — Roman'kov、Bogopolski–Kudryavtseva–Lustig、Dekimpe–Tertooy(`twistedconjugacy` パッケージの背景文献)。冪零群の Reidemeister spectrum の文献。
> **★ 探さなくてよい方向(本稿で潰した)**: **Burkhart 型の非 coprime 不動点定理**。作用群 $\langle\rho\rangle$ が素数冪位数なので**原理的に空虚**(観察 B1)。この系統への追加投資は不要。

> **【文献要請 7】(【GAP-E12】)**
> **困難**: 捻れ類和 $\rho(s_m)$、$\rho(b_\theta)$ の**絡作用素の正規化**。Kawanaka–Matsuyama の $\varepsilon_\theta(\chi)$ は $\theta$ 側の符号を与えるが、$\sigma$ 側(位数 3 の捻れ)の対応物と、両者の積のトレースの正規化が要る。
> **欲しい結果の型**: 位数 $n$ の自己同型に対する「$n$-捻れ Frobenius–Schur 指標」と、その捻れ類和への作用。Vinroot・Kawanaka–Matsuyama の一般化(位数 3 版)があるか。

### 5.3 共同設計者(Sol)への発案要請

1. **P-新 A**: class ≥ 5 の領域は route T(`twistedconjugacy`)の**単系統**になる(§3.3)。**第二の独立判定器**をどう作るか — 群環の直接畳み込み?置換表現での軌道計算?**本丸が単系統というのは工房の規律に反するので、設計を求めたい。**
2. **P-新 B**: 命題 E12 の選択則から、**$\mathrm{Irr}(A)^{\langle\sigma,\theta\rangle} = \{1\}$(自明指標のみ不変)なら $n_m$ が一意に決まる**はずである。この「$S_3$-不変既約指標が自明のみ」という条件を満たす 2 群は E2 障害を**持てない**か? もし言えれば class ≥ 5 の宇宙をさらに縮められる。
3. **P-新 C**: 観察 B1(素数冪位数の作用群では非 coprime 不動点定理が空虚)は、**Glauberman 系の道具全体**への一般的教訓ではないか。裁定 07 以来の「攻撃 B」の位置づけを、Sol の側からも独立に検分してほしい。
4. **P-新 D(最重要・監査要請)**: **予想 E15**(2 群には E2 型障害が無い)を独立に検分してほしい。特に (i) 定理 E9 / E9′ の証明(補題 E9.2 の「$A^\sigma\otimes\mathbb Q$ が 1 次元」と、class 4 の 2-integrality)、(ii) **撤回済み H8″ との論理的差**が私の主張どおりか、(iii) 「障害の唯一の素数は 3」という読みに一般的な理由($\tau$ の位数 3・自由 Lie 環の $C_3$-加群構造)を与えられるか。**もし E15 の一般証明が付けば、E2 正面は 2 群では閉じ、狩場は $3\mid\lvert A\rvert$ 側(Q7 型)へ全面移動する** — 週の戦略が変わる。

---

## 付録 A — 任務 3: S1–S7 証明書の `isolated` 確定の数学的根拠文

**implementer への転記用**(証明書の新欄 `isolated_justification` に 1 行ずつ。**過去版は上書きせず次版で追加** — 便 11 P129)。
根拠の共通の型: **isolated $\iff$ GT($N$) = GTSh($N,N$) $\iff$ 全 shadow が settled**(定義ノート §2)。したがって完全な `settled_detail` から確定できる。

| 証明書 | `isolated` | `isolated_justification`(1 行) |
|---|---|---|
| **S1** | `true` | 全 42 shadow が settled(6 charming 層 × 各 7、`settled_detail` に witness 全数あり)ゆえ GT(N) = GTSh(N,N);case A の正規化群 Hol(C₇)(位数 42)と一致(便 11 F5)。 |
| **S2** | `false` | 全 32 shadow のうち settled は 16 のみ(m = 0,3 の層が 8/8、m = 1,2 の層が 0/8)ゆえ非 settled shadow が存在;定理 B3′ の射程(Ĝ = PGL(2,7) complete・⟨w⟩ 自己中心化極大トーラス・Weyl C₂)で 𝔓 = {±1}、settled 率 2/φ(8) = 1/2(便 11 F6)。 |
| **S3** | `true` | 全 42 shadow が settled(6 層 × 各 7)ゆえ GT(N) = GTSh(N,N);case A の正規化群 Hol(C₇)(位数 42)と一致。 |
| **S4** | `true` | 全 54 shadow が settled(6 層 × 各 9)ゆえ GT(N) = GTSh(N,N);case A の正規化群 Hol(C₉)(位数 54)と一致。 |
| **S5** | `true` | 全 110 shadow が settled(10 層 × 各 11)ゆえ GT(N) = GTSh(N,N);case A の正規化群 Hol(C₁₁)(位数 110)と一致。 |
| **S6** | `false` | 全 40 shadow のうち settled は 20 のみ(m = 0,4 の層が 10/10、m = 1,3 の層が 0/10);定理 B3′ の射程(Ĝ = PGL(2,11))で 𝔓 = {±1}、settled 率 2/φ(10) = 1/2。 |
| **S7** | `false` | 全 48 shadow のうち settled は 24 のみ(m = 0,5 の層が 12/12、m = 2,3 の層が 0/12);定理 B3′ の射程(Ĝ = PGL(2,11))で 𝔓 = {±1}、settled 率 2/φ(12) = 1/2。 |

> **implementer への注意**
> 1. **「半分」は偶然である**(便 11 F6/W96)。S2/S6/S7 で settled 率が 1/2 になるのは $\varphi(8) = \varphi(10) = \varphi(12) = 4$ だからで、**一般形は $2/\varphi(e)$**。justification 文にこれを書かない(上表のとおり $2/\varphi(e)$ の形で書く)。
> 2. **case B の非 isolated は定理 B3′ の射程つき**で書く。「case B は常に非 isolated」と裸で書かない(Errata 2・W96)。
> 3. checker(`crosscheck/check-psl.mjs`)にも `isolated` の再計算(= `settled_detail` の全数一致)を追加すること。現状この欄は未検査(便 11 F15)。

## 付録 B — 語規約の併合(任務 1)完了報告

`docs/定義ノート追記案_語規約_v2.md` を `docs/week1-定義ノート.md` の **新設 §1.5**(§1 と §2 の間)へ併合した。版歴に 2026-07-26 併合を記載。内容: D1–D7 差分表・裁定 11 の注記(**D7 規範部 PASS / `12/20` は candidate**)・規約 W-1〜W-4・補題 W1・盲点 (a)–(d)・適合テスト A5-CONV・未閉鎖項【GAP-W1/W2/W3】。**既存本文の削除はなし**。§2 の 2026-07-25 注記に §1.5 への相互参照を追加。
**implementer への差し戻し 1 件**: 証明書 1b / A1 / 3 の `convention_robust_note` が値 `false` に対して「一致」と書かれており不整合。正しくは「不一致」(便 11 F11 / Errata 3)。**過去版は上書きせず次版で訂正**。
