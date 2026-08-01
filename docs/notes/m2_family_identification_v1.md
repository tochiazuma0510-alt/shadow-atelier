# (M2) の族同定 — 標準モデルが各奇数窓 $K^{(n)}$ の被覆であることの **$n$ 一様**証明

**状態札: `theorem(紙・$n$ 一様)+ 有限機械 spot-check($n\in\{3,7,9,11,13\}$)/ 単系統(python のみ・cross-checked ではない)/ Lean 検証ではない / SURJ は結論しない / K^{(5)} 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01・**新設 v1**
- 委嘱: 司令塔(FAM-U 専任)「**(M2)** 標準モデル(塔 $y^n=h(k)$・$\lambda=\gamma m^2$)が各奇数 $n$ の窓 $K^{(n)}$ の算術被覆であることを **$n$ 一様に**証明せよ」(攻め筋 = C-β 段 3′ の一般化・裁定 308〜314)
- 入力正本: `docs/notes/u7_fire_log_v1_addendum_grade.md` §4.2.3〜4.2.5(C-β 段 3′)、`docs/notes/fam_u_v1.md` §2.1・§3.2((M1)–(M4))、`docs/notes/oddH_full_proof_v1.md` 補題 A/G/H/I・命題 ODD-P、`docs/notes/u7_twist_determination_v1.md`・同 `_addendum_d3.md`、`docs/notes/conventions_ledger_v1.md`(CV-1〜9)
- 機械: `search/probe/wac_v1/m2_family_check.py`(新規)・`search/probe/wac_v1/m2_symbolic_ext.py`(新規)。ログ = 同ディレクトリ `m2_family_check_run.log` / `m2_family_check_run2.log`

---

## 0. 判定(先に 6 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | 段 3′-a(模型側モノドロミー群の代数的構成)は $n$ 一様か | ★ **一様。** 変換則 $h^\sigma,h^\theta,g^\sigma,g^\theta$ は **$n$ を含まない有理関数の恒等式**。$n$ が効くのは **2 箇所だけ**(§2.5 末の悉皆列挙) |
| **②** | $\chi_P$ の一般式 | ★ **$n$ にも依らない閉形**: $\chi_{k=i}=(1,0)$、$\chi_{k=1}=(-\alpha,-1)$、$\chi_{k=0}=\chi_{k=\infty}=(0,0)$(**$\alpha$ は $\chi_{k=1}$ にしか現れない**) |
| **③** | ★ 核心 = Nielsen 枚挙の軌道一意性を一般の奇 $n$ で | ★★ **証明した(定理 NIE)。** $\lvert\mathcal T\rvert=n^2$ で、**平行移動部分群 $A$(位数 $n^2$)が単純推移的**に作用する。生成条件は**自動**。完全共役類版は $4n^2$ 本・単一 $\Gamma_n$ 軌道・**自明安定化群** |
| **④** | S6-a/b の恒等対角を一般 $n$ で | ★★ **証明した(定理 M2-GEO)。** S6-a = スケール共役 $\mu_2$、S6-b = $\langle X,Y\rangle=G_n$ + ODD-H 補題 I。**補題 D3-PAR の parity 論法の一般化は不要だった**(別の・より強い論法が通った) |
| **⑤** | (M2) は閉じたか | ★ **幾何側は閉じた**(M2-GEO)。残るのは**算術的降下 (M2-DESC) の一点のみ**。TW-1(a)($\mathrm{Aut}=1$)も本稿で $n$ 一様に再導出されるので、残余は「$K^{(n)}$ 側の被覆が $F_n$ 上定義されるか」= **§8【文献要請 M2-1】** |
| **★** | 副産物 | 補題 **CORE**($\lvert\mathcal M\rvert=4n^2$)・補題 **EXP**($[r_\infty/r_0]=[\alpha]$)・**TW-1(a)**・**ODD-P**($j=2,d=1$ 行)が**すべて $n$ 一様に独立再導出**される(§7) |

> ### ★ 一行で
> **段 3′ は $n=7$ の偶然ではない。** 模型側の被覆と抽象窓の被覆は $\mathrm{Sym}(\{0,1\}\times\mathbf Z/n)$ の**文字どおり同じ**部分群 $\Gamma_n$($4n^2$ 次)の中で起きており、その中で Nielsen 類は**ただ一つの単元不変量**
> $$\boxed{\ \rho\ :=\ \bigl[\delta/\eta\bigr]\ \in\ (\mathbf Z/n)^\times/\{\pm1\}\ }$$
> で**完全に**分類される。模型($\alpha$)は $\rho=[\alpha]$、抽象窓 $H_{2,\alpha',0}$ は $\rho=[\alpha']$ を与える。**恒等対角はこの一行の系である。**

---

## 1. 規約宣言(CV 台帳 v1 準拠)

```jsonc
"conventions_used": {
  "ledger_version": "conventions_ledger_v1",
  "perm_composition": "paper_left",              // (p*q)(x) = p(q(x))          [CV-1]
  "conjugation":      "paper_inn_g_X_g_inv",     //                              [CV-2]
  "coset_side":       "left",                    // 左剰余類 gH・左作用 m.(gH)=(mg)H
  "word_eval":        "n/a",                     // 本稿は語表示を使わない       [CV-3]
  "coarse_of":        "n/a",  "word_of": "n/a",  //                              [CV-4]
  "roundtrip_assert": "n/a",
  "chi_level":        "n/a",                     //                              [CV-5]
  "opposite":         "n/a",                     //                              [CV-6]
  "comparison_target":
     "for each unit alpha, the model triple is compared with the window H_{2,alpha',0}
      for EVERY alpha' in (Z/n)^x / {+-1}  (full cross table; not a fixed alpha'=1)",  // [CV-7]
  "separation_condition_included": true,         // S6-b を定理に含める          [§1.2]
  "chi_P_criterion":  "exact AND conjugacy_class (both proved; 'line' は禁止・使用せず)", // [CV-8]
  "branch_labels":    "lambda=0 <-> m_0=0 <-> k=+-i ;  lambda=inf <-> m_0=inf <-> k=+-1 ;
                       lambda=1 <-> k in {0,inf}   (model 側は lambda=m_0^2 から強制)",
  "marking":          "(g_0,g_1,g_inf) = (X,Y,Z),  X=a_1q_1, Y=a_1a_2a_3q_2, Z=(XY)^{-1}  [P-2/C2]",
  "level":            "n/a"
}
```

**C-β-IND の遵守**(§4.2.3.1): 本稿が使うのは **(P1) 模型の式そのもの**(と有限の代数操作)、**(P2) 一般論**(Kummer 理論・Galois 理論・tame 慣性の巡回性・有限群論)、**(P3) 抽象側の定義**($G_n$・$H_{2,\alpha,0}$・marking)のみ。**使っていない**もの: TOWER-$n$・KUM-$n$・TW-1・SPLIT・**補題 EXP**・ODD-P(照合の相手としてのみ言及)・$\mathrm{Ih}$ の像。⟹ `uses_Ih_image = false`。
**操作的判定基準**(「$h$ を別の有理関数に取り替えても同じ議論が走るか」): §2〜§4 は $h,g$ の**因子**しか使わないので走る ✓。§5 は抽象側の定義のみ ✓。

**$K^{(5)}$ 凍結**: 本稿の定理は「奇数 $n\ge3$」を言明に含む(**$n=5$ を含む**)が、$n=5$ の窓データ・数値・機械計算には**一切接触していない**。probe は `ALLOWED_N=(3,7,9,11,13)` を assert し、`5` の混入で停止する。

---

## 2. 段 1 — 模型側モノドロミー群の $n$ 一様構成

### 2.1 設定(式そのもの)

$n\ge3$ 奇、$\alpha\in\mathbf Z$、$\gcd(\alpha,n)=1$。$\mathbf C(k)$ 上で

$$h(k):=\frac{(k-i)\,(k+1)^{\alpha}}{(k+i)\,(k-1)^{\alpha}},\qquad g(k):=\frac{k+1}{k-1},$$
$$\widetilde W_0:\ y^{\,n}=h(k),\qquad \iota(k,y)=(-k,1/y),\qquad W_0=\widetilde W_0/\langle\iota\rangle,$$
$$m_0=\frac{1+k^2}{1-k^2},\qquad \lambda=m_0^{\,2}.$$

$$\mathrm{div}(h)=[i]-[-i]+\alpha[-1]-\alpha[1],\qquad \mathrm{div}(g)=[-1]-[1].$$

> **註(代表元の非依存性)**: $h_{\alpha+n}/h_\alpha=g^{\,n}$ ゆえ $[h]$ は $\alpha\bmod n$ にしか依らない。以下の構成はすべて $[\alpha]\in\mathbf Z/n$ の関数である。

### 2.2 補題 V4(底の $V_4$-Galois 性)【proof・$n$ 非依存】

$m_0(k')=-m_0(k)\iff k^2k'^2=1$ ゆえ $\mathbf C(k)/\mathbf C(\lambda)$ は Galois で
$$V_4=\{\mathrm{id},\ \sigma:k\mapsto-k,\ \theta:k\mapsto1/k,\ \sigma\theta:k\mapsto-1/k\}\cong C_2\times C_2 .$$
分岐は $\lambda\in\{0,1,\infty\}$ の上のみ、各繊維は型 $2^2$:

| $\lambda$ | $k$-点 | 慣性($V_4$) |
|---|---|---|
| $0$ | $k=i$ / $k=-i$ | $\sigma\theta$ |
| $\infty$ | $k=1$ / $k=-1$ | $\theta$ |
| $1$ | $k=0$ / $k=\infty$ | $\sigma$ |

*(自己検査: $2g-2=4(-2)+3\cdot2=-2\Rightarrow g(\mathbf P^1_k)=0$ ✓)*

### 2.3 補題 TRF(変換則)【proof・$n$ 非依存】

$\alpha$ を任意の整数として、**厳密な有理関数等式**として
$$h^\sigma=h^{-1},\quad g^\sigma=g^{-1},\quad g^\theta=-g,\quad h^\theta=(-1)^{\alpha+1}h^{-1}g^{2\alpha}.$$

*証明.* $h(-k)$: 分子分母の各因子で $-k-i=-(k+i)$、$(-k+1)^\alpha=(-1)^\alpha(k-1)^\alpha$ 等を代入すると符号がすべて相殺し $h^{-1}$。$h(1/k)$: $1-ik=-i(k+i)$、$1+ik=i(k-i)$、$(1-k)^\alpha=(-1)^\alpha(k-1)^\alpha$ より
$$h(1/k)=\frac{-i(k+i)(k+1)^\alpha}{i(k-i)(-1)^\alpha(k-1)^\alpha}=(-1)^{\alpha+1}\frac{(k+i)(k+1)^\alpha}{(k-i)(k-1)^\alpha}=(-1)^{\alpha+1}h^{-1}g^{2\alpha}. \qquad\square$$

**機械(独立・sympy)**: `m2_symbolic_ext.py` が $\alpha=1..8$ で 4 恒等式すべて `True`(既存 `cbeta_symbolic_check.py` の $\alpha=1..5$ を拡張)。**$n$ はこれらの式のどこにも現れない。**

### 2.4 補題 KUM(Kummer 層)【proof】

$\bar A:=\langle[h],[g]\rangle\le\mathbf C(k)^\times/(\mathbf C(k)^\times)^n$ は $\cong(\mathbf Z/n)^2$。

*証明.* $\mathbf C$ 代数閉ゆえ定数はすべて $n$ 乗、また $f\in(\mathbf C(k)^\times)^n\iff n\mid\mathrm{div}(f)$。$a\,\mathrm{div}(h)+b\,\mathrm{div}(g)\equiv0\ (n)$ は $[i]$ の係数から $a\equiv0$、次いで $[1]$ の係数 $-a\alpha-b$ から $b\equiv0$。∎(**$\alpha$ の可逆性も $n$ の奇性も不要**)

補題 TRF より $\bar A$ は $V_4$-安定、したがって $L:=\mathbf C(k)(h^{1/n},g^{1/n})$ は $\mathbf C(\lambda)$ 上 Galois で
$$\mathcal M^{\rm mod}:=\mathrm{Gal}(L/\mathbf C(\lambda)),\qquad \lvert\mathcal M^{\rm mod}\rvert=n^2\cdot4=4n^2 .$$

### 2.5 補題 SPL(分裂)【proof・**$n$ 奇をここで 1 回使う**】

$y:=h^{1/n}$、$u:=g^{1/n}$、$c:=(-1)^{\alpha+1}\in\{\pm1\}$ と置くと
$$\tilde\sigma:(k,y,u)\mapsto(-k,\ y^{-1},\ u^{-1}),\qquad \tilde\theta:(k,y,u)\mapsto\bigl(1/k,\ c\,y^{-1}u^{2\alpha},\ -u\bigr)$$
はともに対合で可換。ゆえに $\mathcal M^{\rm mod}=\bar A^\vee\rtimes V_4$(分裂)。指標座標 $(c_h,c_g)$($y\mapsto\zeta_n^{c_h}y$, $u\mapsto\zeta_n^{c_g}u$)で
$$\sigma\cdot(c_h,c_g)=(-c_h,-c_g),\qquad \theta\cdot(c_h,c_g)=(-c_h+2\alpha c_g,\ c_g).$$

*証明の要点.* 整合性 $\tilde\theta(y)^n=h^\theta$ には $c^{\,n}=(-1)^{\alpha+1}$、すなわち **$n$ 奇**が要る。$\tilde\theta(u)^n=(-u)^n=-g=g^\theta$ も **$n$ 奇**。$\tilde\theta^2=\mathrm{id}$ は $(-1)^{2\alpha}=1$ から。$\tilde\sigma\tilde\theta=\tilde\theta\tilde\sigma$ は $c=c^{-1}$($c^2=1$)から。∎

> ### ★ $n$ が効く箇所の**悉皆列挙**(委嘱 1 への回答)
> 模型側の構成全体で $n$ が本質的に入るのは **次の 2 箇所だけ**である:
> 1. **補題 SPL**: $c^n=c$ と $(-u)^n=-u^n$ — **$n$ 奇**。
> 2. **$y^n=h$ の分岐指数** — これは「$e=n$」という数値としてしか現れず、群構造の式には入らない。
>
> 他はすべて $n$ 非依存。とくに補題 TRF・補題 KUM・補題 V4 は $n$ を含まない。**これが Sol F93-3.1 の「$n$ は ramification index にしか現れない」という指摘の、群レベルでの正確な形である。**

### 2.6 補題 STAB($\bar H^{\rm mod}$)【proof】

$\mathbf C(k,y)=L^{\{(0,c_g)\}}$、$\iota=\tilde\sigma\vert_{\mathbf C(k,y)}$ ゆえ
$$\bar H^{\rm mod}=\mathrm{Gal}\bigl(L/\mathbf C(W_0)\bigr)=\{(0,c_g)\}\ \sqcup\ \{(0,c_g)\tilde\sigma\},\qquad \lvert\bar H^{\rm mod}\rvert=2n,\quad [\mathcal M^{\rm mod}:\bar H^{\rm mod}]=2n .$$

---

## 3. 段 2 — **座標補題**と正規形(両側が同じ群であることの正体)

ここが本稿の技術的な要である。以下 $\Lambda:=\{0,1\}\times\mathbf Z/n$、点を $(\epsilon,x)$ と書く。

> ### 記法 AFF
> $s\in\{0,1\}$、$e\in\{\pm1\}$、$c_0,c_1\in\mathbf Z/n$ に対し
> $$\bigl\langle s,e;c_0,c_1\bigr\rangle:\quad (0,x)\mapsto(s,\ ex+c_0),\qquad (1,x)\mapsto(1-s,\ ex+c_1)$$
> ($c_\epsilon$ = **ブロック $\epsilon$ から出る**点に加える定数)。これらは $\mathrm{Sym}(\Lambda)$ の部分群
> $$\Gamma_n:=\bigl\{\langle s,e;c_0,c_1\rangle\bigr\}\ \cong\ (\mathbf Z/n)^2\rtimes\bigl(\langle-\mathrm{id}\rangle\times\langle\mathrm{swap}\rangle\bigr),\qquad \lvert\Gamma_n\rvert=4n^2$$
> をなす。$A:=\{\langle0,+;c_0,c_1\rangle\}$(平行移動・位数 $n^2$)は正規。

### 3.1 補題 NF-mod(模型側の座標)【proof + 機械】

$\mathcal M^{\rm mod}$ の元 $(b,v)$($b=(b_h,b_g)$)に対し
$$\beta:=b_h,\qquad \beta':=b_h-2\alpha b_g$$
と置く($n$ 奇・$\alpha$ 単元ゆえ $(b_h,b_g)\mapsto(\beta,\beta')$ は全単射)。剰余類 $\mathcal M^{\rm mod}/\bar H^{\rm mod}$ は
$$\ell(b,v)=\begin{cases}(0,\ b_h) & v\in\{1,\sigma\}\\[2pt] (1,\ b_h-2\alpha b_g)& v\in\{\theta,\sigma\theta\}\end{cases}$$
で $\Lambda$ と全単射に対応し(**$\ell$ は左剰余類上定数**)、左作用は

| $v$ | $\langle s,e;c_0,c_1\rangle$ |
|---|---|
| $1$ | $\langle 0,+;\ \beta,\ \beta'\rangle$ |
| $\sigma$ | $\langle 0,-;\ \beta,\ \beta'\rangle$ |
| $\sigma\theta$ | $\langle 1,+;\ \beta',\ \beta\rangle$ |
| $\theta$ | $\langle 1,-;\ \beta',\ \beta\rangle$ |

*証明.* $v\in\{1,\sigma\}$ の剰余類は $\bar H^{\rm mod}$ が $c_g$ 方向を掃くので $b_h$ だけで決まり、$v\in\{\theta,\sigma\theta\}$ では $\theta\cdot(0,c')=(2\alpha c',c')$ より不変量が $b_h-2\alpha b_g$。あとは $(b,v)\cdot(x,0)$ 型の代表元に直接掛けて読む(§機械 A で全 $n,\alpha$ について検査)。∎

**帰結**: $\mathcal M^{\rm mod}\to\mathrm{Sym}(\Lambda)$ は**単射**($(\beta,\beta')$ が自由に動く)で、像は $\Gamma_n$ **ちょうど**。⟹ **補題 CORE($\lvert\mathcal M\rvert=4n^2$)の独立再導出。** また $L$ は $\mathbf C(W_0)/\mathbf C(\lambda)$ の Galois 閉包である。

### 3.2 補題 NF-abs(抽象側の座標)【proof + 機械】

$G_n=A_3\rtimes Q$、$A_3=(\mathbf Z/n)^3$、$q_ja_iq_j^{-1}=a_i^{\varepsilon_{ji}}$、$\varepsilon_{ji}=+1\iff i=j$(ODD-H (1.1))。窓 $H=H_{2,\alpha,0}=U\sqcup Uq_2$、$U=U_{2,\alpha}=\{(\alpha t,s,t)\}$(ODD-H (1.2))。$m=(v,q)$ に対し
$$B:=v_1-\alpha v_3,\qquad B':=v_1+\alpha v_3,$$
$$\ell(v,q)=\begin{cases}(0,\ v_1-\alpha v_3)& q\in\{1,q_2\}\\[2pt](1,\ v_1+\alpha v_3)& q\in\{q_1,q_3\}\end{cases}$$
は左剰余類上定数で $G_n/H\xrightarrow{\ \sim\ }\Lambda$、左作用は

| $q$ | $\langle s,e;c_0,c_1\rangle$ |
|---|---|
| $1$ | $\langle 0,+;\ B,\ B'\rangle$ |
| $q_2$ | $\langle 0,-;\ B,\ B'\rangle$ |
| $q_1$ | $\langle 1,+;\ B',\ B\rangle$ |
| $q_3$ | $\langle 1,-;\ B',\ B\rangle$ |

($v_2$ は作用に現れない = 核 $\langle e_2\rangle$、位数 $n$ ✓ $4n^3/4n^2=n$。)

### 3.3 系 SAME【proof + 機械】

$$\boxed{\ \mathcal M^{\rm mod}\bigl(=\mathrm{im}\bigr)\ =\ \mathcal M_n\bigl(=\mathrm{im}\ G_n\bigr)\ =\ \Gamma_n\ \le\ \mathrm{Sym}(\Lambda)\ }$$
— **模型側と抽象側は、同型なだけでなく $\mathrm{Sym}(2n)$ の中で文字どおり同じ部分群**であり、しかも $\Gamma_n$ は **$\alpha$ に依らない**。$\alpha$ 依存性は「どの三つ組か」にのみ現れる。
**辞書**(導出結果であって仮定ではない): $q_1\leftrightarrow\sigma\theta$、$q_2\leftrightarrow\sigma$、$q_3\leftrightarrow\theta$。

---

## 4. 段 3 — 局所類($\chi_P$)と **Nielsen 一意性(核心)**

### 4.1 補題 LOC($\chi_P$ の一般式)【proof】

tame 慣性は巡回で、$\zeta_n$ を固定すると点 $P\in\mathbf P^1_k$ 上の $\mathrm{Gal}(L/\mathbf C(k))$-慣性の**標準生成元**は $\chi_P=(v_P(h),v_P(g))\in\bar A^\vee$。因子から:

| $\lambda$ | $k$-点 | $V_4$ 慣性 | $\chi_P$ | $\Gamma_n$-型 | 不変量 |
|---|---|---|---|---|---|
| $0$ | $k=i$ | $\sigma\theta$ | $(1,0)$ | $\langle1,+;\cdot\rangle$ | $\eta=1$ |
| $0$ | $k=-i$ | $\sigma\theta$ | $(-1,0)$ | $\langle1,+;\cdot\rangle$ | $\eta=-1$ |
| $\infty$ | $k=1$ | $\theta$ | $(-\alpha,-1)$ | $\langle1,-;\cdot\rangle$ | $\delta=\alpha$ |
| $\infty$ | $k=-1$ | $\theta$ | $(\alpha,1)$ | $\langle1,-;\cdot\rangle$ | $\delta=-\alpha$ |
| $1$ | $k=0,\infty$ | $\sigma$ | $(0,0)$ | $\langle0,-;\cdot\rangle$ | — |

ここで、型 $\langle1,+;c_0,c_1\rangle$ の元 $w$ には $w^2=\langle0,+;\eta,\eta\rangle$、$\eta(w):=c_0+c_1$;型 $\langle1,-;c_0,c_1\rangle$ には $w^2=\langle0,+;-\delta,\delta\rangle$、$\delta(w):=c_0-c_1$ と定める。補題 NF-mod により $\chi_{k=i}=(1,0)\Rightarrow\eta=1$、$\chi_{k=1}=(-\alpha,-1)\Rightarrow\delta=\alpha$。

**⟹ $\alpha$ は $\chi_{k=1}$(すなわち $\delta$)にしか現れない。** これが「$[\alpha]$ の決定点」であり、**補題 EXP を使わずに**因子から読まれる。

**共役類**($\Gamma_n$ による):
$$C_0=\{\langle1,+;\cdot\rangle:\eta=\pm1\}\ (\lvert C_0\rvert=2n),\quad C_\infty=\{\langle1,-;\cdot\rangle:\delta=\pm\alpha\}\ (\lvert C_\infty\rvert=2n),$$
$$C_1=\{\langle0,-;\cdot\rangle\}\ \text{全体}\ (\lvert C_1\rvert=n^2,\ \text{単一類}).$$
*(符号 $\pm$ の由来: $\varsigma=\langle0,-;0,0\rangle$ 型による共役が $\eta,\delta$ の符号を反転する。これは $\lambda=0$ の上の 2 点 $k=\pm i$ のどちらを取るかの自由度そのものであり、**「厳密一致」(CV-8 の `exact`)はこの類の切片、「完全共役類」は類全体**。両者は同じ答を返す — 定理 NIE が両方で成り立つ。)*

**巡回型**: $\eta,\delta$ 単元 ⟹ $g_0,g_\infty$ は $2n$-巡回、$g_1$ は $x\mapsto c-x$ が各ブロックで固定点ちょうど 1 個($n$ 奇)ゆえ型 $2^{\,n-1}1^2$。
$$\boxed{\ \text{passport}=\bigl((2n),\ 2^{\,n-1}1^2,\ (2n)\bigr)\ }\quad\text{— (M1) の passport 主張の }n\text{ 一様版・ODD-P }(j{=}2,d{=}1)\text{ と一致 ✓}$$

### 4.2 定理 NIE(Nielsen 類の一般 $n$ 一意性)【定理・本稿の核心】

> ### 定理 NIE
> $n\ge3$ 奇、$\eta,\delta\in(\mathbf Z/n)^\times$ とする。
> $$\mathcal T(\eta,\delta):=\Bigl\{(g_0,g_1,g_\infty)\ :\ g_0=\langle1,+;\cdot\rangle,\ \eta(g_0)=\eta;\quad g_1=\langle0,-;\cdot\rangle;\quad g_\infty=\langle1,-;\cdot\rangle,\ \delta(g_\infty)=\delta;\quad g_0g_1g_\infty=1\Bigr\}$$
> と置く。このとき:
> 1. **$\lvert\mathcal T(\eta,\delta)\rvert=n^2$**(閉形パラメータ表示つき)。
> 2. **生成は自動**: 任意の $(g_0,g_1,g_\infty)\in\mathcal T$ に対し $\langle g_0,g_1\rangle=\Gamma_n$。
> 3. $Z(\Gamma_n)=1$。ゆえに $\Gamma_n$ は同時共役で $\mathcal T$ に**自由**に作用し、**$A$($位数 n^2$)は $\mathcal T(\eta,\delta)$ に単純推移的**。⟹ **$\mathcal T(\eta,\delta)$ は単一 $A$-軌道**。
> 4. 完全共役類版 $\mathcal T^{\rm cl}:=\bigsqcup_{\pm,\pm}\mathcal T(\pm\eta,\pm\delta)$ は $4n^2$ 本で、**単一 $\Gamma_n$-軌道**(サイズ $4n^2=\lvert\Gamma_n\rvert$・**安定化群自明**)。
> 5. 逆に $\eta$ または $\delta$ が非単元なら (2) は破れる(生成しない)。

**証明.**

**(1)** $g_0=\langle1,+;p_0,p_1\rangle$($p_0+p_1=\eta$)、$g_1=\langle0,-;q_0,q_1\rangle$ と置く。直接合成して
$$g_0g_1=\langle1,-;\ q_0+p_0,\ q_1+p_1\rangle,\qquad g_\infty=(g_0g_1)^{-1}=\langle1,-;\ q_1+p_1,\ q_0+p_0\rangle$$
(型 $\langle1,-;c_0,c_1\rangle$ の逆元は $\langle1,-;c_1,c_0\rangle$)。よって
$$\delta(g_\infty)=(q_1+p_1)-(q_0+p_0)=(q_1-q_0)+(\eta-2p_0).$$
条件 $\delta(g_\infty)=\delta$ は $q_1-q_0=\delta-\eta+2p_0$ と同値。**自由パラメータは $p_0,q_0\in\mathbf Z/n$ の 2 個**で $p_1,q_1$ は決定される。⟹ $\lvert\mathcal T\rvert=n^2$。∎

**(2)** $g_0^2=\langle0,+;\eta,\eta\rangle$、$g_\infty^2=\langle0,+;-\delta,\delta\rangle$ はともに $\langle g_0,g_1\rangle$ に属す($g_\infty=(g_0g_1)^{-1}$)。$A\cong(\mathbf Z/n)^2$ の中でこの 2 元が張る部分群の判別式は
$$\det\begin{pmatrix}\eta&\eta\\-\delta&\delta\end{pmatrix}=2\eta\delta ,$$
$n$ 奇かつ $\eta,\delta$ 単元ゆえ**単元** ⟹ $A\le\langle g_0,g_1\rangle$。さらに $g_0\mapsto(s,e)=(1,+)$、$g_1\mapsto(0,-)$ は $\Gamma_n/A\cong V_4$ を生成する。⟹ $\langle g_0,g_1\rangle=\Gamma_n$。∎

**(3)** まず $Z(\Gamma_n)=1$: $V_4=\langle-\mathrm{id}\rangle\times\langle\mathrm{swap}\rangle$ は $A=(\mathbf Z/n)^2$ に**忠実**に作用する($n\ge3$)から、中心元は $A$ に属し、$\varsigma=\langle0,-;0,0\rangle$ との可換性から $z=-z$、$n$ 奇ゆえ $z=0$。∎
三つ組の同時共役に関する安定化群は $C_{\Gamma_n}(\langle g_0,g_1\rangle)=C_{\Gamma_n}(\Gamma_n)=Z(\Gamma_n)=1$(← (2))。次に $A$ が $\mathcal T(\eta,\delta)$ を**保つ**: $t=\langle0,+;t_0,t_1\rangle$ による共役は
$$\langle1,+;p_0,p_1\rangle\mapsto\langle1,+;p_0-t_0+t_1,\ p_1-t_1+t_0\rangle\quad(\eta\ \text{不変}),$$
$$\langle1,-;c_0,c_1\rangle\mapsto\langle1,-;c_0+t_0+t_1,\ c_1+t_0+t_1\rangle\quad(\delta\ \text{不変}),$$
$\langle0,-;\cdot\rangle$ 型は型が保たれる。ゆえに $A$ は $\mathcal T(\eta,\delta)$($n^2$ 元)に自由に作用し、$\lvert A\rvert=n^2$ ゆえ**単純推移的**。∎

**(4)** $\varsigma$ 型・$\varkappa$ 型による共役の符号作用は
$$\begin{array}{c|cc}\text{共役元の型}&\eta&\delta\\\hline \langle0,+;\cdot\rangle&+&+\\ \langle0,-;\cdot\rangle&-&-\\ \langle1,+;\cdot\rangle&+&-\\ \langle1,-;\cdot\rangle&-&+\end{array}$$
(4 通りの符号組すべてが実現する)。ゆえに $\Gamma_n$-軌道は $\bigsqcup_{\pm,\pm}\mathcal T(\pm\eta,\pm\delta)$ で、要素数 $4n^2$、安定化群自明ゆえ**単一軌道**。∎

**(5)** $\eta$ か $\delta$ が非単元なら $\det=2\eta\delta$ が非単元となり $A\not\le\langle g_0,g_1\rangle$。∎

> ### ★ 委嘱 3 への回答(手法の訂正)
> 委嘱は「補題 D3-PAR の parity 論法の一般化が候補」としていたが、**parity 論法は不要**だった。D3-PAR($Y$ の固定点が各ブロックに 1 個)は本稿では**巡回型の計算に自動的に含まれる**(補題 LOC の $2^{n-1}1^2$)。一意性の真の機構は
> $$\boxed{\ \lvert\mathcal T\rvert=n^2=\lvert A\rvert\ \textbf{かつ}\ Z(\Gamma_n)=1\ \Longrightarrow\ \textbf{単純推移}\ }$$
> という**数え上げ + 自明中心**である。これは $n=7$ の「$49$ 本」も $n=3$ の「$9$ 本」も同じ一行で説明する。

> ### ★ §4.2.3.4 の記述の**精密化**(erratum ではない)
> 既存追補は「三つ組 **49** 本・軌道 **1** 個(サイズ **196**)」と書いているが、**どの群の軌道か**が省かれている。正確には:
> * **厳密一致**基準: $n^2$($=49$)本 — これは $\Gamma_n$-安定ではなく、**$A$ の単純推移軌道**(サイズ $n^2$)。$\Gamma_n$-軌道に埋めると $4n^2$($=196$)に広がる。
> * **完全共役類**基準: $4n^2$($=196$)本 — **$\Gamma_n$ の単一自由軌道**(サイズ $196$)。
>
> ⟹ 「49 本・軌道 1・サイズ 196」は**両基準の数値が 1 行に混ざっている**。数学的結論(一意性)は両方で正しい。cert には**軌道を取る群**を明記されたい(`orbit_group: "Gamma_n" | "A(translations)"`)。

---

## 5. 段 4 — 抽象側三つ組の閉形

### 5.1 補題 ABS【proof + 機械】

marking $X=a_1q_1$、$Y=a_1a_2a_3q_2$、$Z=(XY)^{-1}$(P-2)に補題 NF-abs を適用すると、**すべての奇 $n$ と単元 $\alpha$ で**
$$\bar X=\langle1,+;\ 1,\ 1\rangle,\qquad \bar Y=\langle0,-;\ 1-\alpha,\ 1+\alpha\rangle,\qquad \bar Z=\langle1,-;\ 2+\alpha,\ 2-\alpha\rangle,$$
$$\boxed{\ \eta(\bar X)=2,\qquad \delta(\bar Z)=2\alpha\ }\qquad\Longrightarrow\qquad (\bar X,\bar Y,\bar Z)\in\mathcal T(2,\,2\alpha).$$

*証明.* $X=((1,0,0),q_1)$ ⟹ $B=B'=1$ ⟹ $\bar X=\langle1,+;1,1\rangle$。$Y=((1,1,1),q_2)$ ⟹ $B=1-\alpha$、$B'=1+\alpha$。$\bar X\bar Y=\langle1,-;2-\alpha,2+\alpha\rangle$、その逆が $\bar Z$。∎
*(整合: $\bar X^2=\langle0,+;2,2\rangle$ は $X^2=2e_1$(ODD-H 補題 A(3))そのもの ✓。巡回型は $((2n),2^{n-1}1^2,(2n))$ で ODD-P と一致 ✓。)*

### 5.2 補題 SCALE【proof】

$u\in(\mathbf Z/n)^\times$ に対し $\mu_u:(\epsilon,x)\mapsto(\epsilon,ux)$ は $\Gamma_n$ を正規化し
$$\mu_u\langle s,e;c_0,c_1\rangle\mu_u^{-1}=\langle s,e;uc_0,uc_1\rangle\ \Longrightarrow\ \eta\mapsto u\eta,\ \delta\mapsto u\delta,\ \mathcal T(\eta,\delta)\xrightarrow{\ \sim\ }\mathcal T(u\eta,u\delta).$$

---

## 6. ★ 定理 M2-GEO(恒等対角の一般証明)

> ### 定理 M2-GEO【定理・$n$ 一様】
> $n\ge3$ 奇、$\alpha,\alpha'\in(\mathbf Z/n)^\times$ とする。模型 $\mathcal C^{\rm mod}(\alpha)$ の慣性標識三つ組 $(g_0,g_1,g_\infty)$($\lambda=0,1,\infty$)と、抽象窓 $H_{2,\alpha',0}$ の標識三つ組 $(\bar X,\bar Y,\bar Z)$ について:
> $$\boxed{\ (g_0,g_1,g_\infty)\ \sim_{\mathrm{Sym}(2n)}\ (\bar X,\bar Y,\bar Z)\quad\Longleftrightarrow\quad \alpha'\equiv\pm\alpha\ \ (\mathrm{mod}\ n)\ }$$
> すなわち $\varphi(n)/2\times\varphi(n)/2$ の交差表は**恒等行列**である(**S6-a 一致 + S6-b 分離**の両方)。これは $\chi_P$ 基準を `exact` に取っても `conjugacy_class` に取っても同じ。

**証明.**

**(S6-a・一致)** 補題 LOC より模型の三つ組は $\mathcal T(1,\alpha)$ に属し(`exact` 基準;$k=i$ と $k=1$ を取る切片)、定理 NIE(3) より $\mathcal T(1,\alpha)$ は空でない単一 $A$-軌道。補題 SCALE で $u=2$($n$ 奇ゆえ単元)を取ると $\mu_2\mathcal T(1,\alpha)\mu_2^{-1}=\mathcal T(2,2\alpha)$。補題 ABS より $(\bar X,\bar Y,\bar Z)\in\mathcal T(2,2\alpha)$ で、これも単一 $A$-軌道。ゆえに**適当な $a\in A$ に対し $\mu_2$ と $a$ の合成が模型三つ組を抽象三つ組へ移す**。∎

**(S6-b・分離)** $\alpha'_1\ne\pm\alpha'_2$ なら $(\bar X,\bar Y,\bar Z)_{\alpha'_1}\not\sim(\bar X,\bar Y,\bar Z)_{\alpha'_2}$ を示せば、S6-a と合わせて主張が出る。$c\in\mathrm{Sym}(2n)$ が両者を同時共役にするとする。**$\langle X,Y\rangle=G_n$**(ODD-H の $G_n$ の定義そのもの・機械 assert 済)ゆえ、任意の $g\in G_n$ を語 $w(X,Y)$ と書けば
$$c\,\pi_{\alpha'_1}(g)\,c^{-1}=c\,w(\pi_1X,\pi_1Y)\,c^{-1}=w(\pi_2X,\pi_2Y)=\pi_{\alpha'_2}(g).$$
すなわち $c$ は **$G_n$-集合の同型** $G_n/H_{2,\alpha'_1,0}\cong G_n/H_{2,\alpha'_2,0}$ を与える。ゆえに点安定化群が $G_n$-共役: $H_{2,\alpha'_1,0}\sim_{G_n}H_{2,\alpha'_2,0}$。ODD-H **補題 I(3)**(共役軌道 $=\{H_{2,\pm\alpha,\beta}\}_\beta$・大きさ $2n$)と **補題 G**(パラメータ付けの単射性)より $\alpha'_2=\pm\alpha'_1$。矛盾。∎

**(基準の非依存)** `conjugacy_class` 基準では模型の三つ組は $\mathcal T^{\rm cl}=\bigsqcup_{\pm,\pm}\mathcal T(\pm1,\pm\alpha)$ に属す。$\mathcal T(-1,-\alpha)=\varsigma$-共役、$\mathcal T(1,-\alpha)=\varkappa$-共役 … で**すべて $\Gamma_n$-共役**(定理 NIE(4))ゆえ、同時共役類は変わらない。∎

> ### ★ 何が言えて、何が言えないか(S6 の意味論・§4.2.5.3 を族へ拡張)
> * **言えること**: 同定機構は $(\mathbf Z/n)^\times/\{\pm1\}$ の $\varphi(n)/2$ 個の窓類を**完全に識別する**(不変量 $\rho=[\delta/\eta]$)。模型に入れた $\alpha$ は模型の**式だけから**取り戻される。$n=7$ の $3\times3$ 恒等対角は $\varphi(7)/2=3$ の場合にすぎない。
> * **言えないこと**: **どの $[\alpha]$ を $K^{(n)}$ が要求するか**(= 凍結 **U7-14**)。これは【I24-a】($\alpha$ 軌道予想)/ Sol Q6.1(reduction-functoriality)に依存し、**本定理の射程外**。$n$ 一様化しても U7-14 は動かない。
> * **実害**: なし。$u_{n,\alpha}=4(-1)^\alpha$ と $-1=\zeta_{4n}^{2n}\in F_n^{\times2n}$ より $[4]_{2n}=[-4]_{2n}$ ⟹ **$\varphi(n)/2$ 個の窓すべてが同じ $[u_n]_{2n}$ と同じ $\mathrm{ord}=n$ を与える**(FAM-U (2)(3)(4) は $[\alpha]$ 非依存)。

---

## 7. 系(依存の降格・$n$ 一様版)

| # | 内容 | 格 |
|---|---|---|
| **CORE-n** | $\lvert\mathcal M_n\rvert=4n^2$、degree $2n$、$\lvert\bar H\rvert=2n$ | 補題 NF-mod / NF-abs の系。**補題 CORE の独立再導出**(全奇 $n$) |
| **EXP-n** | $[r_\infty/r_0]=[-\alpha]=[\alpha]$ | 補題 LOC の $\chi_{k=1}=(-\alpha,-1)$ から**因子として読まれる**。⟹ **補題 EXP は同定の鎖から外れる**(全奇 $n$) |
| **AUT-n** | $\mathrm{Aut}_{\bar{\mathbf Q}}(W_0/\mathbf P^1_\lambda)=C_{\mathrm{Sym}(\Lambda)}(\Gamma_n)=1$ | **TW-1(a) の独立再導出**(下記証明・全奇 $n$・機械 assert 済) |
| **PASS-n** | passport $=\bigl((2n),2^{n-1}1^2,(2n)\bigr)$ | (M1) の passport 部分の $n$ 一様化。ODD-P($j=2$, $d=1$)と一致 |
| **BLOCK-n** | $\Lambda$ は $\Gamma_n$-不変な 2 ブロック($A$-軌道)に分かれる | S7(経路 B との整合)の $n$ 一様版。**$\mathrm{Ih}$ は使っていない** |
| **DROP-n** | ⟹ **D-3(TOWER-$n$/KUM-$n$/SPLIT)と D-4(TW-1)は同定の鎖から外れ「発見の道具」に降格**(全奇 $n$) | 条件付き(§8 の M2-DESC を除く) |

**AUT-n の証明.** 被覆の自己同型群は $C_{\mathrm{Sym}(\Lambda)}(\Gamma_n)$($\Gamma_n$ 推移的)。$c$ がこれに属するとき、$c$ は $A$ の軌道(= 2 ブロック)を置換する。
(i) ブロックを保つ場合: $c\vert_{B_\epsilon}$ は $B_\epsilon\cong\mathbf Z/n$ 上の正則平行移動群と可換ゆえ平行移動 $x\mapsto x+t_\epsilon$。$\varsigma=\langle0,-;0,0\rangle$ との可換性から $t_\epsilon=-t_\epsilon$、$n$ 奇ゆえ $t_\epsilon=0$。
(ii) ブロックを入れ替える場合: $c(0,x)=(1,x+t)$、$c(1,x)=(0,x+t')$ とすると、平行移動 $\langle0,+;c_0,c_1\rangle$ との可換性が全 $(c_0,c_1)$ で $c_0=c_1$ を要求し矛盾。
⟹ $c=\mathrm{id}$。∎

> **註**: AUT-n は「$F$-形式は(存在すれば)一意」を与える(TW-1 の内容)。**存在は与えない** — §8。

---

## 8. ★ 残る穴 — (M2) のうち閉じていない部分

本稿が閉じたのは **(M2) の幾何側**である。前件表 `fam_u_v1.md` §3.2 の (M2) を 2 つに分解して記帳する:

| # | 命題 | 格(本稿後) |
|---|---|---|
| **M2-GEO** | 標準モデルの被覆は、窓 $H_{2,\alpha,0}$ の抽象被覆と**標識つき $\bar{\mathbf Q}$-被覆として同型**であり、$\alpha'\ne\pm\alpha$ の窓とは非同型 | ★★ **theorem($n$ 一様)** — 本稿 §6 |
| **M2-UNIQ** | $\mathrm{Aut}_{\bar F}(W_0/\mathbf P^1)=1$ ⟹ $F_n$-形式は**存在すれば一意** | ★★ **theorem($n$ 一様)** — 本稿 §7 AUT-n(TW-1 に依存しない) |
| **M2-DESC** | ★ $K^{(n)}$ 窓に対応する**算術的**被覆が $F_n=\mathbf Q(\zeta_{4n})$ 上定義されること | ★ **candidate(未閉鎖・本稿の射程外)** |
| **M2-CONV** | どの $[\alpha]$ を $K^{(n)}$ が要求するか(U7-14) | ★ **規約(未決)**。**(2)(3)(4) には影響しない** |

**論理**: モデルは $\mathbf Q(i)\subseteq F_n$ 上の式で与えられているから $F_n$-形式は**存在する**。M2-UNIQ より $F_n$-形式は高々 1 つ。したがって
$$\textbf{M2-DESC}\ \Longrightarrow\ \textbf{(M2)}\quad(\text{M2-GEO + M2-UNIQ の下で}).$$
すなわち **(M2) は「算術側の被覆が $F_n$ 上定義される」という一点に還元された**。

> ### 【文献要請 M2-1】(新規・本稿から)
> **困難**: 標識つき被覆の**幾何的**同定は $n$ 一様に閉じた(定理 M2-GEO)。$\mathrm{Aut}_{\bar{\mathbf Q}}=1$ も $n$ 一様に証明した(AUT-n)。残るのは「$K^{(n)}$ 窓に対応する $\mathbf P^1\setminus\{0,1,\infty\}$ の被覆が、**モジュライ体上定義される**(そしてそのモジュライ体が $F_n=\mathbf Q(\zeta_{4n})$ に含まれる)」という降下の一点である。
> **欲しい結果の型**:
> 1. **mere cover(G-cover ではない)**の版で、「$\mathrm{Aut}_{\bar k}(\text{cover})=1$ ⟹ **field of moduli = field of definition**」を与える定理の**正確な仮定**(底が $\mathbf P^1$・分岐点が $k$-有理・$k$ 数体、で足りるか;基点/tangential base point の要否)。
> 2. モジュライ体を **marked triple への $G_{\mathbf Q}$-作用(GT 作用)から読む**標準的手続き。とくに「$\varphi(n)/2$ 個の窓類の集合への $G_{\mathbf Q}$-作用の核が $\mathbf Q(\zeta_{4n})$ を含む/含まれる」を判定する形。
> **なぜ効くか**: これが降りれば FAM-U の最大前件 (M2) が**族で完全に閉じ**、$u_{n,\alpha}$ の族公式が「別の被覆の $u$」でないことが確定する。
> **既出との関係**: **U7-3((GR) tame + 非衝突 ⟹ 良還元)とは別件**。U7-1(a)(b) は撤回済。

**その他の未閉鎖(本稿の射程外・既記載の再掲)**:
- **(M4)** 各 $n$ で $[\gamma]=1$ — 本稿は $[\gamma]$ に触れない($\bar{\mathbf Q}$ 上の議論のみ)。**M2-DESC が閉じても (M4) は独立に残る。**
- **$d=\gcd(\alpha,n)>1$ の窓**: 定理 NIE(5) により**生成が破れる**(⟹ $\Gamma_n$ が真部分群に落ちる)。ODD-P の $(2n/d)^d$ 型と整合。本稿の射程外であることが**内在的に説明された**。
- **$n$ 偶**: 補題 SPL(§2.5)と $Z(\Gamma_n)=1$ と $g_1$ の固定点数がすべて $n$ 奇に依存する。射程外。

---

## 9. 機械 spot-check(委嘱の $n\in\{3,7,9,11,13\}$)

**probe**: `search/probe/wac_v1/m2_family_check.py`(新規・仕様ヘッダつき)。**収蔵 → 収蔵版をそのまま再実行 → 本節の表を再生成**(CB4-ERR の是正手順を本稿にも適用)。ログ: `m2_family_check_run.log`($n=3,7,9$)、`m2_family_check_run2.log`($n=11,13$)。

検査項目(すべて fail-closed の `assert`):

| # | 検査 | 期待 | 結果 |
|---|---|---|---|
| A | 座標補題(模型)— $\ell$ が左剰余類上定数・全単射 | PASS(全単元 $\alpha$) | ✓ |
| A′ | 座標補題(抽象)— 同上 | PASS | ✓ |
| B | 正規形 AFF — 群の**全元**が $\langle s,e;c_0,c_1\rangle$ 型 | PASS・位数 $4n^2$・次数 $2n$ | ✓ |
| C | 系 SAME — 模型群 = 抽象群 = $\Gamma_n$($\alpha$ に依らず) | `True` | ✓ |
| C′ | $\lvert Z(\Gamma_n)\rvert=1$、$\lvert C_{\mathrm{Sym}}(\Gamma_n)\rvert=1$(AUT-n)、$\langle X,Y\rangle=G_n$ | $1,1$, assert | ✓ |
| D | $\lvert C_0^{\rm ex}\rvert=\lvert C_\infty^{\rm ex}\rvert=n$、$\lvert C_0^{\rm cl}\rvert=\lvert C_\infty^{\rm cl}\rvert=2n$、$\lvert C_1\rvert=n^2$ | 閉形 | ✓ |
| E | 三つ組数 $n^2$ / $4n^2$、軌道 $[n^2]$(平行移動)/ $[4n^2]$($\Gamma_n$)、生成失敗 $0$ | 定理 NIE | ✓ |
| F | $(\eta,\delta)=(1,\alpha)$(模型)/ $(2,2\alpha)$・$\rho=\alpha$(抽象) | 補題 ABS | ✓ |
| G | **交差表 = 恒等行列**(全 $\varphi(n)/2$ 窓) | 定理 M2-GEO | ✓ |

**実測**($\alpha$ は $(\mathbf Z/n)^\times/\{\pm1\}$ の代表):

| $n$ | 窓数 $\varphi(n)/2$ | $\lvert\Gamma_n\rvert$ | 次数 | $\lvert\mathcal T^{\rm ex}\rvert$ / 軌道 | $\lvert\mathcal T^{\rm cl}\rvert$ / 軌道 | passport | 交差表 |
|---|---|---|---|---|---|---|---|
| 3 | 1 | 36 | 6 | 9 / **1**(サイズ 9) | 36 / **1**(サイズ 36) | $(6),2^21^2,(6)$ | 恒等 ✓ |
| 7 | 3 | 196 | 14 | 49 / **1**(49) | 196 / **1**(196) | $(14),2^61^2,(14)$ | 恒等 ✓ |
| 9 | 3 | 324 | 18 | 81 / **1**(81) | 324 / **1**(324) | $(18),2^81^2,(18)$ | 恒等 ✓ |
| 11 | 5 | 484 | 22 | 121 / **1**(121) | 484 / **1**(484) | $(22),2^{10}1^2,(22)$ | 恒等 ✓ |
| 13 | 6 | 676 | 26 | 169 / **1**(169) | 676 / **1**(676) | $(26),2^{12}1^2,(26)$ | 恒等 ✓ |

- **$n=7$ は既存 C-β の実測(49 本 / 196 本 / $3\times3$ 恒等対角)を逐語再現**する ⟹ 本稿は既存結果の一般化であって置換ではない。
- **$n=9$(合成数・単元 $\alpha\in\{1,2,4\}$)も恒等対角** ⟹ 定理は $n$ 素数に依存しない。
- **$n=5$ は走らせていない**(`ALLOWED_N` の assert が防ぐ)。定理の言明は $n=5$ を含むが、値・データへの接触はゼロ。

**独立記号計算**: `m2_symbolic_ext.py`(sympy)が補題 TRF の 4 恒等式を $\alpha=1..8$ で `True`。

**出所**(収蔵後に再実行して本節の表を再生成した版の SHA-256):

| ファイル | SHA-256 |
|---|---|
| `search/probe/wac_v1/m2_family_check.py` | `7c52b50239ec91454d67731a0165110be9b2e9afbea726b8acb8b9e148039b96` |
| `search/probe/wac_v1/m2_symbolic_ext.py` | `227daceff4c1772168c8fb6a645b0e8e271aaa5820fb5a59abd0663ebd446e58` |
| `search/probe/wac_v1/m2_family_check_run.log`($n=3,7,9$) | `81b547da759bc8615b8b8c4bb2ca2fbfb0dbd8fcdcd2cec2d2acd69da73af2fe` |
| `search/probe/wac_v1/m2_family_check_run2.log`($n=11,13$) | `10358454be1d5f77af23a163248ea3ec014561bed282dfcd5cb737b1bc00a69b` |

> ### ⚠ 格の申告
> (i) **単系統**(python のみ)。GAP 等での第二実装は未実施 ⟹ **`cross-checked` を名乗らない**。
> (ii) 紙の証明(§2〜§6)は **$n$ 一様**であり、機械は**その予言の spot-check**である(機械が定理の根拠ではない)。
> (iii) **Lean 検証ではない**。
> (iv) ⟹ 実装係への引き渡し: 上表を**予言**として先に置く。**不一致は本稿の反証。** 独立実装は `cbeta_crosstable.g` を $n$ 一般化するのが最短(有限群計算のみ・曲線に触れない)。

---

## 10. FINDING(本稿の分)

| # | 格 | 内容 |
|---|---|---|
| **M2-NF** | ★★ **定理(新規)** | **座標補題 + 正規形**: 模型側と抽象側のモノドロミー群は $\mathrm{Sym}(\{0,1\}\times\mathbf Z/n)$ の**同一**部分群 $\Gamma_n\cong(\mathbf Z/n)^2\rtimes(C_2\times C_2)$($4n^2$ 次)であり、$\alpha$ に依らない。$\alpha$ 依存は三つ組にのみ現れる |
| **M2-NIE** | ★★ **定理(新規・核心)** | **Nielsen 一意性の $n$ 一様証明**: $\lvert\mathcal T(\eta,\delta)\rvert=n^2=\lvert A\rvert$ かつ $Z(\Gamma_n)=1$ ⟹ **平行移動群が単純推移**。完全共役類版は $4n^2$ 本・単一自由 $\Gamma_n$-軌道。**生成条件は自動**で、その成立条件は $\det=2\eta\delta$ が単元 ⟺ $\gcd(\alpha,n)=1$ |
| **M2-INV** | ★★ **定理(新規)** | **完全不変量** $\rho=[\delta/\eta]\in(\mathbf Z/n)^\times/\{\pm1\}$。模型($\alpha$)$\Rightarrow\rho=[\alpha]$、抽象窓($\alpha'$)$\Rightarrow\rho=[\alpha']$。恒等対角はこの系 |
| **M2-SEP** | ★ **定理(新規・証明の簡略化)** | **S6-b は群論だけで出る**: $\langle X,Y\rangle=G_n$ ⟹ 同時共役 = $G_n$-集合同型 ⟹ 窓の $G_n$-共役 ⟹ ODD-H 補題 I。**正規化群 $N_{\mathrm{Sym}(2n)}(\Gamma_n)$ の計算を経由しなくてよい**(経由すると $u_1=\pm u_0$ の分岐で厄介になる) |
| **M2-AUT** | ★ **定理(新規)** | $C_{\mathrm{Sym}(\Lambda)}(\Gamma_n)=1$ — **TW-1(a) の $n$ 一様な独立再導出**。$n$ 奇が 2 回効く |
| **M2-PAR** | **手法の訂正** | 委嘱が候補とした **D3-PAR の parity 論法の一般化は不要**。parity は巡回型 $2^{n-1}1^2$ の計算に吸収され、一意性の機構は**数え上げ + 自明中心**だった |
| **M2-NDEP** | **$n$ 依存の悉皆列挙** | 模型側で $n$ が本質的に効くのは **2 箇所のみ**(補題 SPL の $c^n=c$・$(-u)^n=-u^n$)。他は $n$ 非依存。⟹ Sol F93-3.1 の「$n$ は分岐指数にしか現れない」の**群レベルでの正確化** |
| **M2-RED** | ★★ **前件の還元** | **(M2) = M2-GEO(証明済)+ M2-UNIQ(証明済)+ M2-DESC(未閉鎖)。** ⟹ FAM-U の最大の穴は「**算術側の被覆が $F_n$ 上定義されるか**」の一点に縮んだ。【文献要請 M2-1】 |
| **M2-ORB** | **記述の精密化** | §4.2.3.4 の「49 本・軌道 1(サイズ 196)」は**両基準の数値の混在**。cert に `orbit_group` 欄を要求 |
| **M2-D** | **射程の内在的説明** | $d=\gcd(\alpha,n)>1$ で定理が落ちる理由は $\det=2\eta\delta$ の非可逆性(= 生成の破れ)。ODD-P の $d$ 分岐と同じ源 |

---

## 11. Sol への申し送り(次便)

- **監査点 A(核心)**: 定理 NIE(3) の「$\lvert\mathcal T\rvert=n^2=\lvert A\rvert$ + 自由 ⟹ 単純推移」。自由性は $C_{\Gamma_n}(\langle g_0,g_1\rangle)=Z(\Gamma_n)=1$ に依存し、これは**生成 (2) を先に使う**。順序に循環がないか(生成 (2) は $\eta,\delta$ が単元であることのみを使い、軌道の議論を使わない)を確認いただきたい。
- **監査点 B**: 定理 M2-GEO の S6-b。「同時共役 ⟹ $G_n$-集合同型」は $\langle X,Y\rangle=G_n$ に**全面的に**依存する。ODD-H では $G_n:=\langle(r,s,s),(rs,r,rs)\rangle$ が定義だったので自動と読んだが、正典の側でこの読みが正しいか。
- **監査点 C**: `exact` と `conjugacy_class` の同値(§6 末)。$\varsigma,\varkappa$ 共役が $(\eta,\delta)$ の 4 通りの符号組を実現する(定理 NIE(4) の表)から、切片の取り方は結論に影響しない — この論法で **CV-8 の「同答」主張が族で定理化される**と読んでよいか。
- **監査点 D**: §8 の還元。「モデルは $\mathbf Q(i)$ 上定義されている + $\mathrm{Aut}=1$ ⟹ $F_n$-形式は高々 1 つ」から **(M2) が M2-DESC 一点に還元される**という論理。$H^1(G_{F_n},\mathrm{Aut})=1$ の使い方に穴がないか(とくに「$\mathbf P^1$ の分岐点を固定した被覆の形式」という圏の取り方)。
- **監査点 E**: 委嘱の想定(D3-PAR の一般化)を**使わずに**通したこと。parity 論法が本当に不要か、それとも私が別の場所で暗黙に使っているか(巡回型 $2^{n-1}1^2$ の導出 = $x\mapsto c-x$ の固定点が $n$ 奇でちょうど 1 個 — これは parity そのものである、という読みもありうる)。**「D3-PAR は消えたのではなく、補題 LOC の中に吸収された」**という整理が正しいと思うが、格付けの言葉として適切か。

---

## 付録: 記号対応表(既存文書との橋)

| 本稿 | 既存(追補 §4.2.3) | 備考 |
|---|---|---|
| $\Gamma_n$ | $\mathcal M^{\rm mod}$ / $\mathcal M_n$ | **同一**(系 SAME) |
| $A=\{\langle0,+;\cdot\rangle\}$ | $\bar A^\vee$ の像 | 位数 $n^2$・平行移動 |
| $\langle s,e;c_0,c_1\rangle$ | — | 本稿の新記法(記法 AFF) |
| $\eta(g_0)$ | $\chi_0=(1,0)$ の像 | `exact` で $\eta=1$ |
| $\delta(g_\infty)$ | $\chi_\infty=(-\alpha,-1)$ の像 | `exact` で $\delta=\alpha$ |
| $\rho=[\delta/\eta]$ | — | **新規・完全不変量** |
| $\mathcal T(\eta,\delta)$ | Nielsen 類($\chi_P$ 厳密一致) | $n=7$ で 49 本 |
| $\mathcal T^{\rm cl}$ | Nielsen 類(完全共役類) | $n=7$ で 196 本 |
