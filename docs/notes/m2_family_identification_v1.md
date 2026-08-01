# (M2) の族同定 — 標準モデルが各奇数窓 $K^{(n)}$ の被覆であることの **$n$ 一様**証明

**状態札: `theorem(紙・$n$ 一様)+ 有限機械 spot-check($n\in\{3,7,9,11,13\}$)/ 単系統(python のみ・cross-checked ではない)/ Lean 検証ではない / SURJ は結論しない / K^{(5)} 非接触`**

> ### ⚠ 冒頭注記(2026-08-01・便 95 検収 = 裁定 344・**追記 E(本稿末尾)による更新**)【CV-10 誘導】
> 上の状態札は **v1 起草時**(GAP cert 発行前・便 95 監査前)のものであり、**書き換えない**。**現在有効な格**は次のとおり:
>
> | 対象 | 現格(2026-08-01 時点) |
> |---|---|
> | §1–§7(M2-NF / NIE / GEO / UNIQ / AUT-n) | 紙は $n$ 一様の **theorem**(便 95 **F95-1.1 / F95-1.2** で PASS) |
> | §9 の有限 spot-check(交差表・三つ組数・軌道) | ★ **cross-checked**($n\in\{3,7,9,11,13\}$)— GAP 独立実装が python と数値完全一致(裁定 329・cert `search/certs/m2_crosstable_gap_20260801.json` / SHA-256 `414c78e4db4ec607182de97befe21f137f5826f88ff7c6bd7138725928e70668`)。**紙の定理の根拠ではなく、その予言の spot-check** である点は不変 |
> | §D(M2-DESC) | 結論 **PASS**。ただし**主証明は差し替わった** — 便 95 **F95-1.4** の「BCL 不要の $\mathbf Q(i)/\mathbf Q$ 直接降下」が主証明(**追記 E.2**)、§D.3 の BCL 経路は**参考(第二経路)**へ降格 |
> | §D.7 の spot-check | **python 単系統のまま**(cross-checked ではない) |
> | 撤回 | 「$\mathrm{Aut}=1$ だから marked 版も同じ」= **撤回**(追記 **E.4**)。mere cover と $F_n$ 上の明示 source-map には影響しない |
> | 必須修文 | $\alpha$ の型 / $m$ の型 / D.3 段 3「一意」/ D.4 の $\Theta^*W_0$ = **追記 E.1** |
> | Lean / SURJ / $K^{(5)}$ | **Lean 検証ではない**・**SURJ は結論しない**・**$K^{(5)}$ 非接触** — いずれも不変 |
>
> ⟹ **有効出所 = 本稿 + 追記 E**。**§8 と §D の本文だけを引用しないこと**(CV-10)。

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

> ### ⚠ 本節は末尾の**追記(§D)により更新された**(2026-08-01・裁定 328)
> 下表の **M2-DESC「candidate(未閉鎖)」は、§D.3 定理 M2-DESC により解消**された(moduli 体 $=\mathbf Q$ ⟹ $\mathbf Q$ 上定義 ⟹ $F_n$ 上定義)。**【文献要請 M2-1】も §D で消費済**(代わりに軽い【文献要請 M2-2】= BCL の引用の型 が立った)。本文は誤りの記録として書き換えない。

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

---
---

# 追記(2026-08-01・裁定 328 追加委嘱)— **§(M2-DESC) 算術的降下の閉鎖**

> **位置づけ**: §8 への **追補**。§1〜§11 の本文は**書き換えない**(§8 の「M2-DESC = candidate(未閉鎖)」という記述は**本追記が更新する**)。**【文献要請 M2-1】は本追記で消費された** — 司令塔が機構抽出済(裁定 328 覚書・骨格文献 = Dèbes–Emsalem 1999 / Dèbes–Douai 1997)。

## D.0 判定(先に 5 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | (M2-DESC) は閉じたか | ★★ **閉じた。しかも予想より強い。** $\mathcal C_\alpha$ の **moduli 体は $\mathbf Q$** であり、$\mathrm{Aut}=1$(AUT-n)ゆえ **$\mathbf Q$ 上定義される**。$F_n$ 上定義されることは**その系** |
| **②** | 機構 | ★ **一行**: $G_{\mathbf Q}$ は 3 つの慣性を**すべて同じ** $\chi(\tau)$ 乗する。我々の完全不変量 $\rho=[\delta/\eta]$ は**比**である。⟹ **$\chi(\tau)$ が約分されて消える**(補題 POW) |
| **③** | marked / mere の差 | ★ **本件では差がない。** $\mathrm{Aut}=1$ なので marking は rigidification として何も追加せず、marked 降下と mere 降下は同値。**mere で降ろして marking を忘れる**必要すら生じない(司令塔の注意点への回答) |
| **④** | 障害($H^2$)の正体 | ★ **障害は定義域ごと存在しない。** Dèbes–Douai の $H^2(K,Z(G))$ 障害は **$G$-cover の理論**;我々は **mere cover** で $\mathrm{Aut}=1$ ゆえ、降下データが**一意**で cocycle 条件が**自動的に**成り立つ(Weil)。$H^1$ も $H^2$ も自明群係数 |
| **★** | (M2) 全体 | ★★ **完全閉鎖**: (M2) = M2-GEO(§6・定理)+ M2-UNIQ(§7 AUT-n・定理)+ **M2-DESC(本追記・定理)**。⟹ **FAM-U の最大の穴 (M2) が消えた** |
| **⑥** | 副産物 | **(M4) $[\gamma]=1$ も落ちる可能性**(§D.5・**candidate**・依存明記)。fam_u 監査点 D の循環懸念は**解消**される |

---

## D.1 使う道具(外部入力の明示)

> ### (T1) Weil 降下 + $\mathrm{Aut}=1$【外部一般論・司令塔覚書経由】
> $f:W\to\mathbf P^1_{\bar{\mathbf Q}}$ を有限被覆、その moduli 体を $M$($\mathbf Q$ 相対)とする。各 $\tau\in G_M$ に対し ${}^\tau f\cong f$($\mathbf P^1$ 上)ゆえ同型 $\theta_\tau:{}^\tau W\to W$ が存在する。
> **$\mathrm{Aut}_{\mathbf P^1}(f)=1$ ならば $\theta_\tau$ は一意**、したがって cocycle 条件
> $$\theta_{\sigma\tau}=\theta_\sigma\circ{}^\sigma\theta_\tau$$
> は**両辺とも ${}^{\sigma\tau}W\to W$ の同型であるという理由だけで自動的に成立**する(選択の余地がない)。⟹ Galois 降下データが得られる。
> **有効性**: $f$ は**有限射**なので $f_*\mathcal O_W$ は $\mathbf P^1_{\bar{\mathbf Q}}$ 上の**連接 $\mathcal O$-代数層**であり、降下データは準連接層の fpqc 降下により**無条件に有効**。⟹ $M$ 上のモデル $W_M\to\mathbf P^1_M$ が存在。
> **⟹ $\mathrm{Aut}=1$ の mere cover では FoM = FoD。** 骨格文献: Dèbes–Emsalem 1999(十分条件)/ Dèbes–Douai 1997(障害論 — **本件では $Z(G)$ 障害の圏に入らない**)。

> ### (T2) Branch Cycle Lemma【外部一般論・**要引用**】
> 分岐点集合 $D=\{0,1,\infty\}$ は $\mathbf Q$-有理で $G_{\mathbf Q}$ が各点を固定する。$\tau\in G_{\mathbf Q}$、$m:=\chi(\tau)\in\hat{\mathbf Z}^\times$ とすると、${}^\tau f$ の記述 $T^\tau=(g_0^\tau,g_1^\tau,g_\infty^\tau)$ は
> $$g_i^\tau\ \sim\ g_i^{\,m}\qquad(\text{モノドロミー群の中で共役})$$
> を満たす。
> **機構**: 分岐点 $P$($\mathbf Q$-有理)における tame 慣性は標準的に $\hat{\mathbf Z}(1)=\varprojlim\mu_N$ と同一視され、$G_{\mathbf Q}$ はそこに**円分指標で**作用する。⟹ 慣性生成元は $\chi(\tau)$ 乗される(共役の不定性を除いて)。
> **註**: 本追記は $\tau(x)=x^{\chi}$ のような**精密な形**(Ihara / Belyi の明示公式・$f_\tau$ 付き)を**使わない**。共役を除いた $\chi$ 乗という**粗い形だけ**で足りる — これが論証を頑健にしている。

**C-β-IND との関係**: (T1)(T2) は「特定の窓に関する主張を含まない一般論」= **(P2)** である。TOWER-$n$/KUM-$n$/TW-1/SPLIT/EXP は**依然として使っていない**(§D.5 の (M4) 観察のみ SPLIT に依存 — そこだけ明示的に分離した)。`uses_Ih_image = false` 維持。

---

## D.2 補題 POW(本追記の一工夫)【proof・$n$ 一様】

> ### 補題 POW
> $m$ を**奇数**とする。$\Gamma_n$ の元について
> $$\eta\bigl(g^{\,m}\bigr)=m\,\eta(g)\quad(g\ \text{が型}\ \langle1,+;\cdot\rangle),\qquad \delta\bigl(g^{\,m}\bigr)=m\,\delta(g)\quad(g\ \text{が型}\ \langle1,-;\cdot\rangle).$$
> とくに $\rho=[\delta/\eta]$ は**同時 $m$ 乗で不変**である。

**証明.** $g=\langle1,+;p_0,p_1\rangle$、$\eta=p_0+p_1$。$g^2=\langle0,+;\eta,\eta\rangle$ ゆえ $g^{2k}=\langle0,+;k\eta,k\eta\rangle$、
$$g^{2k+1}=g\cdot g^{2k}=\langle1,+;\ p_0+k\eta,\ p_1+k\eta\rangle,\qquad \eta(g^{2k+1})=(p_0+p_1)+2k\eta=(2k+1)\eta .$$
$g=\langle1,-;c_0,c_1\rangle$、$\delta=c_0-c_1$。$g^2=\langle0,+;-\delta,\delta\rangle$ ゆえ $g^{2k}=\langle0,+;-k\delta,k\delta\rangle$、
$$g^{2k+1}=g\cdot g^{2k}=\langle1,-;\ c_0+k\delta,\ c_1-k\delta\rangle,\qquad \delta(g^{2k+1})=(c_0-c_1)+2k\delta=(2k+1)\delta . \qquad\square$$

> ### ★ ここが「一工夫」
> $G_{\mathbf Q}$ は $\eta$ と $\delta$ を**同じ因子 $m$ 倍する**。我々の完全不変量は**その比**である。**⟹ 円分作用は約分されて消える。**
> 対照的に、もし完全不変量が $\eta$ や $\delta$ **単体**であれば、moduli 体は $\mathbf Q(\zeta_{2n})$ 級になっていたはずである。**比であること**が降下を可能にしている。

---

## D.3 ★ 定理 M2-DESC【定理・$n$ 一様】

> ### 定理 M2-DESC
> $n\ge3$ 奇、$\alpha\in(\mathbf Z/n)^\times$。mere cover $\mathcal C_\alpha:W_0\to\mathbf P^1_\lambda$(分岐 $\{0,1,\infty\}$)について:
> 1. **moduli 体($\mathbf Q$ 相対)は $\mathbf Q$ である。**
> 2. $\mathrm{Aut}_{\mathbf P^1}(\mathcal C_\alpha)=1$(§7 AUT-n)ゆえ、**$\mathcal C_\alpha$ は $\mathbf Q$ 上定義される。**
> 3. とくに $F_n=\mathbf Q(\zeta_{4n})$ 上定義され、**M2-UNIQ($F$-形式の一意性)により、標準モデルの $F_n$-底変換が唯一の $F_n$-形式である。**
>
> $$\boxed{\ \textbf{(M2)}\ =\ \textbf{M2-GEO}\ +\ \textbf{M2-UNIQ}\ +\ \textbf{M2-DESC}\ \ \text{— 三つとも定理。(M2) は閉じた。}\ }$$

**証明.**

**(段 1)** $\tau\in G_{\mathbf Q}$、$m:=\chi(\tau)$。$m$ は $\hat{\mathbf Z}^\times$ の元、とくに **$m$ は奇数**であり $\gcd(m,n)=1$。(T2) より ${}^\tau\mathcal C_\alpha$ の記述 $T^\tau$ は $g_i^\tau\sim_{\Gamma_n}g_i^{\,m}$ を満たす。

**(段 2)** 補題 ABS より元の記述は $T=(\bar X,\bar Y,\bar Z)$、$\eta(\bar X)=2$、$\delta(\bar Z)=2\alpha$。補題 POW より
$$\eta(\bar X^{\,m})=2m,\qquad \delta(\bar Z^{\,m})=2m\alpha,\qquad \bar Y^{\,m}=\bar Y\ (\bar Y\ \text{は対合・}m\ \text{奇}).$$
定理 NIE(4) の符号表より $\Gamma_n$-共役は $\eta,\delta$ の**符号しか変えない**。ゆえに
$$T^\tau\ \in\ \mathcal T^{\rm cl}(2m,\ 2m\alpha)\ :=\bigsqcup_{\pm,\pm}\mathcal T(\pm2m,\pm2m\alpha).$$

**(段 3)** $2m$ と $2m\alpha$ はともに $(\mathbf Z/n)^\times$ の元($n$ 奇・$\gcd(m,n)=1$・$\alpha$ 単元)。定理 NIE(4) より $\mathcal T^{\rm cl}(2m,2m\alpha)$ は **単一 $\Gamma_n$-軌道**(サイズ $4n^2$・安定化群自明)。**⟹ $T^\tau$ はこの軌道の元として一意に定まる**(記述の不定性がすべて吸収される)。

**(段 4)** $\rho(T^\tau)=[\,2m\alpha/2m\,]=[\alpha]=\rho(T)$。§6 より $\rho$ は $\mathrm{Sym}(2n)$-同時共役の**完全不変量**であるから
$$T^\tau\ \sim\ T\qquad\Longrightarrow\qquad {}^\tau\mathcal C_\alpha\ \cong\ \mathcal C_\alpha .$$

**(段 5)** $\tau\in G_{\mathbf Q}$ は任意だったから、安定化群は $G_{\mathbf Q}$ 全体。⟹ moduli 体 $=\mathbf Q$。(1) ∎

**(段 6)** (T1) を $M=\mathbf Q$ に適用して (2)。(3) は $\mathbf Q\subseteq F_n$ と M2-UNIQ から。∎

> ### ⚠ 論証の頑健性(どこが折れると倒れるか)
> * **段 1 のみが外部入力 (T2) に依存**する。しかも「共役を除いて $\chi$ 乗」という**最も粗い形**しか使わない。
> * 段 2–4 は本稿 §3–§6 の**自前の定理**のみ。
> * 段 6 のみが外部入力 (T1)。$\mathrm{Aut}=1$ は §7 で自前に証明済。
> * ⟹ **反証の急所は (T2) の正確な形**である(§D.8 の【文献要請 M2-2】)。

---

## D.4 独立整合検査 — 複素共役の**明示証人**

段 1–5 は組み合わせ論的である。**幾何的に独立な**確認を 1 本置く。

$c\in G_{\mathbf Q}$ を複素共役($\chi(c)=-1$)とする。模型の式の係数を共役すると
$$ {}^c h=\frac{(k+i)(k+1)^{\alpha}}{(k-i)(k-1)^{\alpha}}=h^{-1}g^{2\alpha}\ \overset{\text{補題 TRF}}{=}\ (-1)^{\alpha+1}\,h^{\theta},\qquad {}^cg=g,\qquad {}^cm_0=m_0,\ {}^c\lambda=\lambda .$$

$\Theta:\mathbf P^1_k\to\mathbf P^1_k,\ k\mapsto1/k$($=\theta$)は **$\mathbf P^1_\lambda$ 上の自己同型**である(補題 V4)。$\epsilon:=(-1)^{\alpha+1}\in\{\pm1\}$ は $n$ 奇ゆえ $\epsilon^n=\epsilon$、したがって $y\mapsto\epsilon y$ は
$$\Theta^*\widetilde W_0:\ y^n=h^\theta=\epsilon\cdot{}^ch\qquad\xrightarrow{\ \sim\ }\qquad {}^c\widetilde W_0:\ y^n={}^ch$$
の同型を与える。さらに $\iota$ の引き戻しは($V_4$ が可換で $\Theta^{-1}\sigma\Theta=\sigma$ ゆえ)**同じ式** $(k,y)\mapsto(-k,1/y)$ になり、$\epsilon^2=1$ ゆえ $y\mapsto\epsilon y$ と可換。ゆえに商まで込めて
$$ {}^cW_0\ \cong\ \Theta^*W_0\ \cong\ W_0\qquad(\mathbf P^1_\lambda\ \text{上の同型;第 2 の同型は }\Theta\text{ が }\mathbf P^1_\lambda\text{ 上の自己同型だから}).$$

$$\boxed{\ \textbf{複素共役は被覆を固定する — 明示的な証人 }\Theta=\theta\ \textbf{つきで。}\ }$$

> ### ★ なぜこれが**非自明な**検査なのか
> 模型の式には $i$ が露わに現れるので、素朴には「$\mathbf Q(i)$ が要る」と見える。実際に起きているのは、**$i\mapsto-i$ が塔の底の自己同型 $\theta$ による捻れで打ち消される**ことである。そしてこれは (T2) の予言($m=-1$ ⟹ $\eta\mapsto-\eta$、$\delta\mapsto-\delta$、$\rho$ 不変)と**完全に整合**している。
> **構造的な傍証**: $\mathrm{div}(h)=[i]-[-i]+\alpha[-1]-\alpha[1]$ は $c$ で $-\mathrm{div}(h)+2\alpha\,\mathrm{div}(g)$ に移る。すなわち **Kummer 部分群 $\bar A=\langle[h],[g]\rangle$ 自体が $G_{\mathbf Q}$-安定**である($[i],[-i]$ の入れ替えと $[\pm1]$ の固定から、任意の $\tau$ について同様)。塔全体が $G_{\mathbf Q}$ で保たれており、残る問題は「その中のどの部分群 $\bar H^{\rm mod}$ か」だけ — それを $\rho$ が決める。

---

## D.5 系 — (M2) の閉鎖と (M4) への波及

### D.5.1 系 M2-CLOSE【定理】

$$\textbf{(M2)}\ \textbf{は閉じた。}$$
前件表 `fam_u_v1.md` §3.2 の **(M2)(格: ★★ candidate — 族定理の最大の穴)** と **(M3)(未実行・設計のみ)** は、いずれも **theorem($n$ 一様)** に格上げされる。**(D)(D-3/D-4)群は同定の鎖から完全に外れる**(§7 DROP-n が無条件になる)。

### D.5.2 観察 M4-OBS【★ candidate・依存を明示】

**主張**: $[\gamma]=1$ が全奇 $n$・全単元 $\alpha$ で成り立つ((M4) が落ちる)。

**論拠(3 行)**:
1. **SPLIT(D-3d)**: $[u_n]_2=[\gamma]$ in $F_n^\times/F_n^{\times2}$。
2. **§2.2 の値計算**(fam_u): $u_{n,\alpha}=4(-1)^\alpha\in\{4,-4\}$ — これは**モデルからの直接の局所計算**であって $\gamma$ も conic $B$ も使わない。
3. $F_n=\mathbf Q(\zeta_{4n})\ni i$ ゆえ $4=2^2$、$-4=(2i)^2$ — **どちらも $F_n$ の平方**。⟹ $[u_n]_2=1$ ⟹ $[\gamma]=1$。∎

> ### ★ 循環していない(fam_u 監査点 D への回答)
> fam_u は「$R_\pm$ が $\mathbf Q$-有理に見えるのは**正規形が $F_n$ 上に降りている ((M2)) を前提にしている**;循環していないか」と問うていた。**本追記で (M2) が (M4) と独立に閉じた**ので、循環は断ち切れた: (M2) の証明(§3–§6・D.1–D.4)は $\gamma$・$\delta_0$・conic $B$・$R_\pm$ の**どれにも触れていない**。
> **格の留保**: 本観察は **SPLIT(D-3d・格 `proof + 表記規律`)** と **§2.2 の値計算**に依存する。C-β-IND は「同定に D-3 を使うな」であって「同定が済んだ後の帰結に使うな」ではないが、**依存を明示した上で candidate に留める**。Sol 監査点(§D.9)。

---

## D.6 何が言えて、何が言えないか(射程宣言)

**言えること**:
1. mere cover $\mathcal C_\alpha$ は **$\mathbf Q$ 上定義される**(全奇 $n$・全単元 $\alpha$・$\varphi(n)/2$ 個すべて)。
2. したがって $F_n$ 上定義され、標準モデルがその唯一の $F_n$-形式。**(M2) 閉鎖。**
3. marked 版も同じ(**$\mathrm{Aut}=1$ ゆえ marking は降下に何も足さない**)。

**言えないこと(重要)**:
1. ★ **「被覆が $\mathbf Q$ 上」は「測定が $\mathbf Q$ で済む」を意味しない。** $u_n$ の測定は cusp $P_0$・**局所一様化元 $\tau=y$**・$\mu_{2n}$ を要し、Kummer 類 $[u_n]_{2n}\in F_n^\times/F_n^{\times2n}$ は **$F_n$ でこそ意味を持つ**。FAM-U が $F_n$ を要求するのは**Kummer 理論の側の事情**であって被覆の定義体の事情ではない。**両者は矛盾しない。**
2. **塔の中間対象**($V$、conic $B$、$m$-座標)の $\mathbf Q$-有理性は主張しない。$\mathbf Q$-モデルの存在は中間層の $\mathbf Q$-有理性を含意しない($G_{\mathbf Q}$-安定な中間部分群が要る)。
3. **$\mathrm{Ih}$ の像・全射性・dihedral 予想**については何も言わない(GEO/ARITH の区別は不変)。
4. **U7-14($[\alpha]$ の規約)**は動かない。本追記も「どの $[\alpha]$ を $K^{(n)}$ が要求するか」には答えない。
5. **$d=\gcd(\alpha,n)>1$・$n$ 偶**は射程外(定理 NIE(5)・補題 SPL)。

---

## D.7 機械 spot-check

**probe**: `search/probe/wac_v1/m2_desc_check.py`(新規)。**正規形($\eta,\delta,\rho$)を一切使わず**、$\Gamma_n$ の共役類を総当りで作り、BFS 正準形で比較する**独立経路**。

| # | 検査 | 期待 | 結果 |
|---|---|---|---|
| P1 | 全 $m\in(\mathbf Z/2n)^\times$ について $\mathcal{Ni}(C_0^m,C_1^m,C_\infty^m)$ が **$4n^2$ 本・単一 $\Gamma_n$-軌道** | 定理 NIE(4)+補題 POW | ✓ |
| P2 | その **全元** が元の被覆と $\mathrm{Sym}(2n)$-同時共役(正準形が一致) | 定理 M2-DESC 段 4 | ✓ |

> **註(P2 は生成条件検査を内包する)**: BFS 正準形は**推移的**三つ組にしか定義されない(非推移なら `None`)。「Nielsen 類の全元の正準形が元の三つ組のそれと一致する」は、**推移性(= $\Gamma_n$ を生成すること)と単一 $\mathrm{Sym}$-類であることを同時に**保証する。ゆえに別建ての生成条件 BFS は不要(かつ本検査の方が強い)。

**実測**:

| $n$ | $\alpha$ 代表 | $\chi(\tau)\bmod 2n$ の値域 | $\lvert C_0^m\rvert,\lvert C_1^m\rvert,\lvert C_\infty^m\rvert$ | 三つ組 / 軌道 | $\tau$-固定 |
|---|---|---|---|---|---|
| 3 | $\{1\}$ | $\{1,5\}$(2 個) | $6,9,6$ | $36$ / **1**(36) | **True** |
| 7 | $\{1,2,3\}$ | $\{1,3,5,9,11,13\}$(6 個) | $14,49,14$ | $196$ / **1**(196) | **True** |
| 9 | $\{1,2,4\}$ | $\{1,5,7,11,13,17\}$(6 個) | $18,81,18$ | $324$ / **1**(324) | **True** |
| 11 | $\{1,\dots,5\}$ | $\varphi(22)=10$ 個 | $22,121,22$ | $484$ / **1**(484) | **True** |
| 13 | $\{1,\dots,6\}$ | $\varphi(26)=12$ 個 | $26,169,26$ | $676$ / **1**(676) | **True** |

⟹ **全 $(n,\alpha,m)$ の組($n=3,7,9,11,13$ / $\alpha$ 全代表 / $m$ 全単元 — 計 $2+18+18+50+72=160$ 通り)で $G_{\mathbf Q}$ は被覆を固定する。** $n=5$ は `ALLOWED_N` の assert が防ぐ。

**出所**(収蔵後に再実行して本節の表を再生成した版の SHA-256):

| ファイル | SHA-256 |
|---|---|
| `search/probe/wac_v1/m2_desc_check.py` | `7b0d364ded63beb6df6b76b2758fb3f1ff99114b6fb5412111ac261e3906d235` |
| `search/probe/wac_v1/m2_desc_check_run.log`($n=3,7,9$) | `e5fcc3038d853ea93df68d3d5483957b355588e8adb8783343af5d2d84e8ff38` |
| `search/probe/wac_v1/m2_desc_check_run2.log`($n=11,13$) | `2c2c3e527f734497246f7e8c61047ccb753a50030a053c3c35e5eeabc2995d81` |

> **格の申告**: 単系統(python)。紙の証明(D.2–D.3)が $n$ 一様で、機械はその**予言の spot-check**。**cross-checked ではない。Lean 検証ではない。**

---

## D.8 FINDING(本追記の分)

| # | 格 | 内容 |
|---|---|---|
| **MD-POW** | ★★ **定理(新規・機構の核)** | 補題 POW: 奇 $m$ に対し $\eta(g^m)=m\eta$、$\delta(g^m)=m\delta$。⟹ **$\rho$ は円分作用で不変**。「$G_{\mathbf Q}$ は全慣性を同じ $\chi$ 乗するが、我々の不変量は**比**だから約分される」 |
| **MD-FOM** | ★★ **定理(新規)** | **$\mathcal C_\alpha$ の moduli 体 $=\mathbf Q$**。BCL(粗い形)+ 定理 NIE(単一軌道)+ $\rho$(完全不変量)の三点で閉じる |
| **MD-DESC** | ★★ **定理(新規)** | $\mathrm{Aut}=1$(§7)+ Weil 降下(有限射ゆえ有効性自明)⟹ **$\mathcal C_\alpha$ は $\mathbf Q$ 上定義される**。⟹ **(M2) 完全閉鎖** |
| **MD-CONJ** | ★ **独立証人** | 複素共役の固定を**幾何的に**確認: ${}^cW_0\cong\Theta^*W_0\cong W_0$、証人は $\Theta=\theta$。**式に現れる $i$ は $\theta$-捻れで打ち消される** |
| **MD-ABAR** | **構造的傍証** | Kummer 部分群 $\bar A=\langle[h],[g]\rangle$ は $\mathrm{Div}(\mathbf P^1_{\bar{\mathbf Q}})/n$ の中で **$G_{\mathbf Q}$-安定**。塔全体が保たれ、残る自由度は $\bar H^{\rm mod}$ の選択のみ |
| **MD-NOOBS** | **障害論の位置づけ** | Dèbes–Douai の $H^2(K,Z(G))$ 障害は **$G$-cover の圏**の話。本件は **mere cover + $\mathrm{Aut}=1$** ゆえ、**障害の住む群が自明**で、$H^1$($F$-形式の分類)も $H^2$(降下の障害)も消える。**「障害が消える」のではなく「障害の圏に入らない」** |
| **MD-M4** | ★ **candidate(依存明記)** | $[\gamma]=[u_n]_2=[\pm4]_2=1$($F_n\ni i$ ゆえ $-4=(2i)^2$)⟹ **(M4) も落ちる**。依存: SPLIT(D-3d)+ §2.2 の値計算。**循環は断ち切れている** |
| **MD-STRONG** | ⚠ **予想外の強さの申告** | 得られた結論(**$\mathbf Q$ 上定義**)は工房の従来の想定($F_n$ が要る)より**強い**。**強すぎる結論は疑うべき**なので、反証の急所((T2) の正確な形)を §D.3 末に明示し、$n=3$($\varphi(3)/2=1$ ⟹ 自明に $\mathbf Q$)との整合も確認した |

> ### 【文献要請 M2-2】(新規・軽い・引用の型のみ)
> **困難**: 段 1 が **Branch Cycle Lemma** に依存する。使うのは「$\mathbf Q$-有理な分岐点をもつ mere cover について、$\tau\in G_{\mathbf Q}$ は各慣性生成元を(モノドロミー群の中の共役を除いて)$\chi(\tau)$ 乗する」という**粗い形だけ**。
> **欲しい結果の型**: (i) この形の BCL の**標準的な引用先**(Fried 1977 / Völklein *Groups as Galois Groups* の補題番号 / Dèbes–Fried)と、(ii) **仮定の正確な形** — とくに **mere cover(G-cover でない)**でよいか、**接ベクトル基点**が要るか、分岐点が $\mathbf Q$-有理でない場合に現れる**分岐点の置換**の項が本件($0,1,\infty$ 固定)で本当に落ちるか。
> **なぜ軽いか**: 機構は既に理解している(tame 慣性 $=\hat{\mathbf Z}(1)$ への円分作用)。欲しいのは**引用可能な正確な言明**だけ。**これが確定すれば MD-FOM/MD-DESC は完全な定理格になる。**
> **既出との関係**: 【文献要請 M2-1】は本追記で**消費・解消**。U7-3((GR))は別件で未消費。

---

## D.9 Sol への申し送り(本追記の分)

- **監査点 F(最重要)**: 定理 M2-DESC の段 1。**(T2) の粗い形**(慣性は共役を除いて $\chi$ 乗)だけで段 2–4 が回ることを確認いただきたい。とくに「$T^\tau$ の各成分が個別に $g_i^m$ と共役」から「$T^\tau$ が $\mathcal T^{\rm cl}(2m,2m\alpha)$ に属す」へ移るところで、**三成分の共役元を独立に取ってよいか**(取れなくても $\eta,\delta$ は各成分から読むので問題ないと考えたが、明示的に確認願いたい)。
- **監査点 G**: 結論の強さ。**$\varphi(n)/2$ 個の dessin がすべて $\mathbf Q$ 上定義される**という主張は、外部知識と衝突しないか。とくに $n=7$ の 3 個の degree-14 dessin($196$ 位モノドロミー・passport $(14),2^61^2,(14)$)が $\mathbf Q$ 上と言えるか — **反例をご存知なら即座に指摘されたい**(私の論証のどこかが折れている証拠になる)。
- **監査点 H**: (T1) の有効性。**有限射の降下を $f_*\mathcal O_W$ の準連接層降下で片付けた**が、これで $\mathbf P^1_{\mathbf Q}$ 上の**被覆として**の $\mathbf Q$-モデルが得られる、という読みでよいか(代数構造の降下 ⟹ $\mathrm{Spec}$ を取って被覆を復元)。
- **監査点 I**: §D.5.2 の (M4) 観察。SPLIT に依存させたことが格の過大表示になっていないか。$[u_n]_2$ が**モデル・一様化元に相対的**な量である(TW-14)ことと、$[\gamma]$ が**被覆の不変量**であることの間に段差がないか。
- **監査点 J**: 「被覆は $\mathbf Q$ 上・測定は $F_n$ で」の分離(§D.6 言えないこと 1)。FAM-U の言明に修正が要るか(私は**不要**と読んだ — FAM-U は $[u_{n,\alpha}]_{2n}\in F_n^\times/F_n^{\times2n}$ を主張しており、被覆の定義体には言及していない)。

---
---

# 追記 E(2026-08-01・便 95 修文波)— **M2-DESC の主証明差し替え**と必須修文 5 点・marked 主張の撤回

> **位置づけ**: §D への**追補**であり、**§1〜§11 と §D の本文は書き換えない**(CV-10 erratum 方式)。抵触する箇所は**本追記が優先**する。冒頭状態札の更新は**本稿冒頭の注記ブロック**として実施済(W95-1.1(5) の履行・下 §E.1.5)。
> **委嘱**: 司令塔(便 95 M2 修文波・**裁定 344**)
> **入力正本**: `sol/sol_reply_95_math22.md`(SHA-256 `de88488fbf21c42e9c3adf52c4689a84a8854ff24012b125b3a0229fcaeba7e9`)§1 = **F95-1.1〜F95-1.7 / W95-1.1 / W95-1.2 / P95-1.1**
> **検算**: 本追記 §E.2 の逐段検算表(手計算・すべて 1 行の代数;$n$ 奇と $\epsilon^2=1$ のみを使う)

---

## E.0 判定(先に 6 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | W95-1.1 の 5 点は受諾か | ★ **全面受諾**。(a) $\alpha$ の型、(b) $m$ の型、(c) D.3 段 3 の「一意」、(d) $\Theta^*W_0$ の型、(e) 状態札 — **いずれも私の記述側の欠陥**であり、結論は倒れない(§E.1) |
| **②** | M2-DESC の主証明は何になるか | ★★ **差し替え**。便 95 **F95-1.4** の $\mathbf Q(i)/\mathbf Q$ 直接降下を**主証明**に昇格(§E.2)。**§D.3 の BCL 経路は参考(第二経路)**へ降格 |
| **③** | 差し替えで何が良くなるか | ★ **反証の急所が移動した**。旧: 外部一般論 (T2)(BCL)の正確な形。新: **二次拡大の明示同型 2 本**($A,B$)— これは**自前で全段検算できる**(§E.2 の検算表)。⟹ MD-STRONG(強すぎる結論の申告)の危険面が縮む |
| **④** | marked 主張 | ★ **撤回**(§E.4)。「$\mathrm{Aut}=1$ だから marked 版も同じ」は一般に偽。**mere cover と $F_n$ 上の明示 source-map には無影響**ゆえ (M2) の閉鎖は不変 |
| **⑤** | 【文献要請 M2-2】 | ★ **消費**(F95-1.3 が引用先と仮定の正確形を供給)。ただし**引用形の受領**であって原著の原文照合ではない(§E.3 末の申告) |
| **★** | (M2) 全体 | ★★ **閉鎖は維持**。(M2) = M2-GEO + M2-UNIQ + M2-DESC、三つとも定理。本追記は**証明の入れ替えと型の修理**であって、結論の変更ではない |

---

## E.1 必須修文 5 点(W95-1.1 の履行)

### E.1.1 (a) $\alpha$ の型 — 模型指数 $\widetilde\alpha\in\mathbf Z$ と窓 label $\alpha=\widetilde\alpha\bmod n$ の分離

**欠陥**: §D.3 の定理 M2-DESC の言明は「$\alpha\in(\mathbf Z/n)^\times$」と量化しながら、証明(§D.4)で $\epsilon=(-1)^{\alpha+1}$ という**整数指数の冪**を計算している。$(\mathbf Z/n)^\times$ の元に $(-1)^{(\cdot)}$ は well-defined でない($n$ 奇ゆえ $\alpha$ と $\alpha+n$ は parity が異なる)。これは追補 `fam_u_v1_addendum_f94.md` §1(**FU-TYPE**・便 94 W94-3.1)で既に指摘・修理された型不正と**同型の欠陥**であり、本稿では未修理のまま残っていた。

**修文(以後この読みが正)**:

> **定理 M2-DESC(型修正版)**: $n\ge3$ 奇、**$\widetilde\alpha\in\mathbf Z$ で $\gcd(\widetilde\alpha,n)=1$**、$\alpha:=[\widetilde\alpha]\in(\mathbf Z/n)^\times$ とする。mere cover $\mathcal C_{\widetilde\alpha}:W_0\to\mathbf P^1_\lambda$ について (1)(2)(3) が成り立つ。

**なぜ結論が動かないか**(自前・2 行):
1. $\epsilon:=(-1)^{\widetilde\alpha+1}\in\{\pm1\}$ は $\widetilde\alpha$ の parity に依存するが、§E.2 の同型 $A$ は $\epsilon$ の**どちらの値でも**成り立つ($\epsilon^2=1$ しか使わない)。
2. 持上げの取り替え $\widetilde\alpha\mapsto\widetilde\alpha+n$ は**被覆の同型**を与える(**補題 LIFT**・追補 f94 §1.3・便 95 **F95-1.7** で PASS)。ゆえに $\mathcal C_{\widetilde\alpha}$ の同型類・moduli 体・定義体は $\alpha$ 水準の量である。

⟹ **§D 全体で「$\alpha$」と書かれた箇所のうち、$(-1)^{(\cdot)}$ の指数に立つものは $\widetilde\alpha$ と読む**(§D.4 の $\epsilon$、§D.5.2 の $u_{n,\widetilde\alpha}=4(-1)^{\widetilde\alpha}$)。**窓の label・不変量 $\rho=[\alpha]$ として現れるものは $\alpha$ のまま**(§D.3 段 4 の $\rho(T)=[\alpha]$)。

### E.1.2 (b) $m$ の型 — $\bar m:=\chi(\tau)\bmod 2n\in(\mathbf Z/2n)^\times$

**欠陥**: §D.1 (T2) と §D.3 段 1 で $m:=\chi(\tau)\in\widehat{\mathbf Z}^\times$ と置き、それを $g^{\,m}$ の**整数指数**として使っている。$\widehat{\mathbf Z}^\times$ の元は整数ではないので型不正。

**修文**:

$$\boxed{\ \bar m:=\chi(\tau)\bmod 2n\ \in(\mathbf Z/2n)^\times\ }\qquad\text{その\textbf{任意の}整数代表 }m\in\mathbf Z\text{ を補題 POW に入れる。}$$

**代表非依存の根拠(自前・3 行)**:
1. 還元 $\widehat{\mathbf Z}^\times\twoheadrightarrow(\mathbf Z/2n)^\times$ は全射なので、任意の $\tau$ に対し $\bar m$ は定まる。
2. 補題 LOC より $g_0,g_\infty$ は**位数 $2n$**、$g_1$ は**対合**。ゆえに $g_i^{\,m}$ は $m\bmod 2n$($g_1$ については $m\bmod2$)にのみ依存する。
3. $\gcd(m,2n)=1\Rightarrow m$ は**自動的に奇数**。ゆえに補題 POW の仮定「$m$ 奇」は、$\bar m$ のどの整数代表を取っても満たされる。

⟹ **補題 POW(§D.2)の言明そのものは修正不要**(「$m$ を奇数とする」のまま正しい)。修理が要るのは **(T2) と段 1 の型宣言**だけである。

### E.1.3 (c) §D.3 段 3 の「$T^\tau$ が一意に定まる」は削除

**欠陥**: 段 3 は「$\mathcal T^{\rm cl}(2m,2m\alpha)$ は単一 $\Gamma_n$-軌道 ⟹ **$T^\tau$ はこの軌道の元として一意に定まる**」と書いている。**軌道は $4n^2$ 個の元をもつ**(定理 NIE(4))ので、文字どおりには偽である。

**修文**: 段 3 の結論を

> $2m,\ 2m\alpha\in(\mathbf Z/n)^\times$ ゆえ $\mathcal T^{\rm cl}(2m,2m\alpha)$ は空でない**単一の $\Gamma_n$-軌道**であり、$T^\tau$ は**この軌道に属する**。

に置き換える。**段 4 が使うのはこれだけ**である($\rho$ は軌道上定数なので、軌道への所属から $\rho(T^\tau)=[2m\alpha/2m]=[\alpha]$ が読める)。⟹ **論証への影響なし**。

### E.1.4 (d) §D.4 の $\Theta^*W_0$ の型

**欠陥**: $W_0$ は $\mathbf P^1_\lambda$ 上の対象であり、$\Theta=\theta:k\mapsto1/k$ は $\mathbf P^1_k$ の自己同型である。「$\Theta^*W_0$」はどちらの底に沿った pullback かが**書かれていない**。

**修文**: **$\mathbf P^1_k$ 上で先に**

$$\bigl(\theta^*\widetilde W_0,\ \theta^*\iota\bigr),\qquad \theta^*\widetilde W_0:\ y^n=h^\theta(k),\qquad \theta^*\iota:(k,y)\mapsto(-k,1/y)$$

を定義し、**その商 $\theta^*\widetilde W_0/\langle\theta^*\iota\rangle$ を取って $\mathbf P^1_\lambda$ 上へ降ろす**(§E.2 の $A,B$ がこの型で書かれている)。

> **註(先取りの禁止)**: $\theta$ は $\mathbf P^1_\lambda$ 上恒等(補題 V4)なので「$\mathbf P^1_\lambda$ 上の対象としては $\theta^*W_0=W_0$」と書きたくなるが、**それは示すべき結論の一部**である。記法で先取りしてはならない — 型を書き下せばこの誘惑は消える(これが W95-1.1(4) の実質)。

### E.1.5 (e) 冒頭状態札の更新【実施済】

**W95-1.1(5) の指摘**: 冒頭状態札は「単系統(python のみ・cross-checked ではない)」と書く一方、後発の GAP cert(裁定 329)が加わっている。

**履行**: 歴史本文(状態札の行)は**書き換えず**、その直後に**冒頭注記ブロック**(CV-10 の「旧正本の冒頭に後継への誘導を置く」)を新設した。内容 = ①有限 instances の現格(§9 は **cross-checked**・§D.7 は **単系統**)②主証明の差し替え ③撤回 ④本追記への誘導。cert digest は機械計算値を記載(machine-piped 規律)。

---

## E.2 ★ 定理 M2-DESC の**主証明**(便 95 F95-1.4・BCL 不要の $\mathbf Q(i)/\mathbf Q$ 直接降下)

> ### 位置づけ(格の宣言)
> 以下は **Sol(外部数学者)が便 95 F95-1.4 で供給した補正証明**であり、**本追記をもって定理 M2-DESC の主証明とする**。§D.3(BCL 経路)は**撤回しない** — 入力の交わらない**参考の第二経路**として保持する(§E.5 の対応表)。

**設定**($\widetilde\alpha\in\mathbf Z$・型は §E.1.1):

$$\widetilde W_{\widetilde\alpha}:\ y^n=h_{\widetilde\alpha}(k),\qquad \iota(k,y)=(-k,y^{-1}),\qquad W_0=\widetilde W_{\widetilde\alpha}/\langle\iota\rangle$$

は **$\mathbf Q(i)$ 上の明示形**である。したがって $G_{\mathbf Q}$ の作用のうち調べるべきは $\mathrm{Gal}(\mathbf Q(i)/\mathbf Q)=\{1,c\}$ **だけ**である。

$\theta(k)=1/k$、$\epsilon:=(-1)^{\widetilde\alpha+1}$ と置く。本稿 §D.4 の恒等式

$${}^ch=\epsilon\,h^\theta,\qquad\text{従って}\qquad h^\theta=\epsilon\,{}^ch$$

の下で、次の**二つの同型を型どおりに**書く:

$$A:\bigl(\theta^*\widetilde W_0,\ \theta^*\iota\bigr)\longrightarrow\bigl({}^c\widetilde W_0,\ {}^c\iota\bigr),\qquad (k,y)\longmapsto(k,\ \epsilon y),$$
$$B:\bigl(\theta^*\widetilde W_0,\ \theta^*\iota\bigr)\longrightarrow\bigl(\widetilde W_0,\ \iota\bigr),\qquad (k,y)\longmapsto(1/k,\ y).$$

**$A$ が方程式を保つ**のは $(\epsilon y)^n=\epsilon y^n=\epsilon^2\,{}^ch={}^ch$($n$ 奇ゆえ $\epsilon^n=\epsilon$、$\epsilon^2=1$)による。**$B$ は pullback の定義そのもの**であり、$\lambda(1/k)=\lambda(k)$ ゆえ $\mathbf P^1_\lambda$ 上の同型である。さらに $\theta(-k)=-\theta(k)$ と $\epsilon^{-1}=\epsilon$ により、**どちらも各 involution と可換**する。商を取って

$$\boxed{\ {}^cW_0\ \cong\ W_0\qquad(\mathbf P^1_\lambda\ \text{上})\ }$$

を得る。$G_{\mathbf Q(i)}$ は係数を固定するから ${}^\tau W_0=W_0$($\tau\in G_{\mathbf Q(i)}$)、残る複素共役も上の同型で固定する。$G_{\mathbf Q}=G_{\mathbf Q(i)}\sqcup c\,G_{\mathbf Q(i)}$ ゆえ **mere cover の安定化群は $G_{\mathbf Q}$ 全体**、すなわち **FoM $=\mathbf Q$**。最後に $\mathrm{Aut}=1$(§7 AUT-n)なので共役同型は一意で cocycle 条件を自動的に満たす。**有限射**(同値に有限 $\mathcal O$-代数)の **fpqc 降下は有効**だから $\mathbf Q$-model が存在する。∎

### E.2.1 逐段検算(工房数学者による独立確認・手計算)

**規律の申告**: 外部から降りた証明を**そのまま格上げしない** — 各段を自分で潰した。以下はすべて 1 行の代数で、$n$ 奇と $\epsilon^2=1$ 以外の入力を使わない。

| # | 検算項目 | 計算 | 判定 |
|---|---|---|---|
| 1 | ${}^ch=h^{-1}g^{2\widetilde\alpha}$ | 係数の共役 $i\mapsto-i$ で $\frac{(k-i)(k+1)^{\widetilde\alpha}}{(k+i)(k-1)^{\widetilde\alpha}}\mapsto\frac{(k+i)(k+1)^{\widetilde\alpha}}{(k-i)(k-1)^{\widetilde\alpha}}$ | ✓ |
| 2 | ${}^ch=\epsilon h^\theta$ | 補題 TRF の $h^\theta=(-1)^{\widetilde\alpha+1}h^{-1}g^{2\widetilde\alpha}=\epsilon\cdot{}^ch$、$\epsilon^2=1$ で両辺に $\epsilon$ | ✓ |
| 3 | $A$ が方程式を保つ | $y^n=h^\theta=\epsilon\,{}^ch\Rightarrow(\epsilon y)^n=\epsilon^n y^n=\epsilon\cdot\epsilon\,{}^ch={}^ch$($n$ 奇) | ✓ |
| 4 | $\lambda(1/k)=\lambda(k)$ | $m_0(1/k)=\frac{1+k^{-2}}{1-k^{-2}}=\frac{k^2+1}{k^2-1}=-m_0(k)$、$\lambda=m_0^2$ | ✓ |
| 5 | $\theta^*\iota$ の形が $(k,y)\mapsto(-k,1/y)$ | $\theta\sigma=\sigma\theta$($\theta(-k)=-1/k=\sigma\theta(k)$)。整合には $h^\theta(-k)=h^\theta(k)^{-1}$ が要り、$(h^\theta)^\sigma=(h^\sigma)^\theta=(h^{-1})^\theta=(h^\theta)^{-1}$ | ✓ |
| 6 | $A$ が involution と可換 | $A(\theta^*\iota(k,y))=A(-k,1/y)=(-k,\epsilon/y)$;${}^c\iota(A(k,y))={}^c\iota(k,\epsilon y)=(-k,1/(\epsilon y))=(-k,\epsilon/y)$($\epsilon^{-1}=\epsilon$) | ✓ |
| 7 | $B$ が involution と可換 | $B(\theta^*\iota(k,y))=B(-k,1/y)=(-1/k,1/y)$;$\iota(B(k,y))=\iota(1/k,y)=(-1/k,1/y)$ | ✓ |
| 8 | 合成の型 | $A\circ B^{-1}:W_0\to{}^cW_0$。$B$ は $\theta$ を覆い($\mathbf P^1_k$ 上ではない)、$\theta$ は $\mathbf P^1_\lambda$ 上恒等(補題 V4)。$A$ は $\mathbf P^1_k$ 上。⟹ 合成は **$\mathbf P^1_\lambda$ 上の同型** | ✓ |
| 9 | 安定化群 $=G_{\mathbf Q}$ | 模型の係数は $\mathbf Q(i)$ にある(§2.1)。$\tau=c\tau'$($\tau'\in G_{\mathbf Q(i)}$)なら ${}^\tau W_0={}^c({}^{\tau'}W_0)={}^cW_0\cong W_0$ | ✓ |
| 10 | $\epsilon$ の依存性 | 証明中 $\epsilon$ については $\epsilon^n=\epsilon$($n$ 奇)と $\epsilon^2=1$ しか使わない ⟹ **$\widetilde\alpha$ の parity に依らず成立**(§E.1.1 の型修正と整合) | ✓ |

**⟹ 全 10 項目 PASS。私は Sol の補正証明に穴を見つけられなかった。**

### E.2.2 何が構造的に良くなったか

| 観点 | 旧(§D.3・BCL 経路) | 新(本節・直接降下) |
|---|---|---|
| **外部入力** | (T1) Weil 降下 + (T2) **BCL**(引用の型が未確定 = 【文献要請 M2-2】) | (T1) Weil 降下 + **fpqc 降下**のみ。**BCL 不要** |
| **反証の急所** | (T2) の正確な形(外部・自前検算不能) | **明示同型 $A,B$**(§E.2.1 で全段自前検算済) |
| **使う自前定理** | §3–§6 の $\Gamma_n$ 組合せ論(NIE・POW・$\rho$) | **使わない**(補題 TRF と補題 V4 のみ) |
| **Galois 元** | 全 $\tau\in G_{\mathbf Q}$(慣性の $\chi$ 乗) | **非自明な 1 個($c$)だけ** |
| **$n$ 一様性** | 一様 | 一様(**$n$ 奇のみ**) |

> ### ★ 二経路であることの意味(用語の規律)
> §D.3(BCL 経路)と §E.2(直接降下)は**入力が交わらない**($\Gamma_n$ の組合せ論を使う/使わない、BCL を使う/使わない)。両者が同じ結論 FoM $=\mathbf Q$ に達したことは、**紙の独立二経路の一致**である。
> **⚠ ただし `cross-checked` とは呼ばない** — 工房規律で `cross-checked` は**二実装の機械一致**に、`verified` は **Lean** に予約されている。ここは**紙の二経路**である。

### E.2.3 MD-STRONG(強すぎる結論の申告)の現状

結論「$\varphi(n)/2$ 個の mere cover がすべて $\mathbf Q$ 上定義される」は依然として工房の従来想定より強い。**申告は維持**する。ただし危険面は次のとおり縮んだ:

- 旧: 外部一般論 (T2) の形が違えば倒れうる ⟹ **自前で潰せない**。
- 新: 倒れるとすれば $A$ か $B$ の初等的な誤り ⟹ **§E.2.1 の 10 項目に集約**し、全て潰した。
- 残る外部依存は **(T1) Weil 降下 + 有限射の fpqc 降下**のみ(F95-1.4 末尾で Sol が明示的に肯定 ⟹ **§D.9 監査点 H は解消**)。

---

## E.3 BCL の逐条裁定(F95-1.3)と【文献要請 M2-2】の消費

主証明が BCL 非依存になったので、以下は**参考経路 §D.3 の正当化**として記録する(§D.9 監査点 F への直接回答を含む)。

| # | §D.8【文献要請 M2-2】の問い | 便 95 F95-1.3 の回答 |
|---|---|---|
| 1 | **mere cover(G-cover でない)でよいか** | ★ **YES**。非 Galois の degree $d$ mere cover を幾何 monodromy $G\le S_d$ の **absolute Nielsen class** として扱い、**$S_d$ 内の同時共役**として使う |
| 2 | **接ベクトル基点が要るか** | ★ **粗形には不要**。局所慣性の「元」を正準に選ぶ精密式には要るが、今回使う**共役類の粗形**には不要。基点・path の変更は各慣性元への共役として吸収される |
| 3 | **分岐点の置換項** | ★ **恒等**。一般には $z_i\mapsto\tau z_i$ が同じ Galois 軌道の分岐点を置換するが、本件の $0,1,\infty$ は**個別に $\mathbf Q$-有理**ゆえ置換は恒等 |
| 4 | **三成分の共役元を独立に取ってよいか**(= 監査点 F) | ★ **YES**。BCL が与えるのは**各成分の局所共役類**であり、path correction は成分ごとに異なり得る。一方 $T^\tau$ は**実在する共役 cover の branch tuple** なので product-one と生成条件を**既に**満たす ⟹ 「各成分が指定共役類に属する」ことだけで $\mathcal T^{\rm cl}$ へ入れられる |

> ### ⚠ 自認(監査点 F の私の読みは結論だけ当たっていた)
> §D.9 で私は「取れなくても $\eta,\delta$ は各成分から読むので問題ない」と書いた。結論は正しかったが、**理由が弱い** — 各成分から不変量を読めることは、三つ組が $\mathcal T^{\rm cl}$(product-one と生成条件を含む集合)に入ることを保証しない。**正しい理由は「$T^\tau$ が実在の被覆の branch tuple だから product-one と生成条件は既に成立している」**である(F95-1.3(4))。**充足しているのは仮定であって、私が示したのは必要条件の一部にすぎなかった。**

**引用形**(便 95 F95-1.3 供給・BCL の粗形に対する標準引用先):

- M. D. Fried, *Fields of Definition of Function Fields and Hurwitz Families — Groups as Galois Groups*, Comm. Algebra **5** (1977), 17–82、**Thm. 5.1**(Branch Cycle Argument・非 Galois / absolute 版を含む)。
- H. Völklein, *Groups as Galois Groups*, **Lemma 2.8**, p. 34。
- 再掲: Fried, *Finite Fields Appl.* **11** (2005), **Appendix A.1 / B.1**。

**左右規約**: 版によって指数が $\chi(\tau)^{-1}$ と書かれるが、本件の不変量は**比** $\rho=[\delta/\eta]$ なのでどちらでも同じ結論(F95-1.3)。⟹ CV-6(反準同型・左右規約)の観点でも安全側。

> ### ⚠ 文献ゲートの申告(重要)
> 【文献要請 M2-2】は**消費**したが、これは **Sol が便で降ろした引用形の受領**であって、**工房は原著を読んでいない**。すなわち「引用先が確定した」であり「原文照合済み」ではない。**原文照合が要る場面**(たとえば Lean 公理化の P95-4.1(1): axiom ごとに原典の exact theorem/頁と PDF 画像照合を束縛する)では、別途 pdftocairo による頁画像照合を要する。
> **なお主証明は §E.2 に移ったので、BCL は Lean 公理化の対象から外れる**(P95-4.1(6) の Sol 推奨と一致 — 二次拡大の明示同型と有限降下を形式化する方が axiom boundary が小さい)。

---

## E.4 ★ 撤回 — 広い marked 主張(W95-1.1 末)

> ### 撤回文
> **「$\mathrm{Aut}=1$ だから marked 版も mere 版と同じ」は撤回する。**
> $\mathrm{Aut}=1$ が消すのは **descent isomorphism の選択肢**であって、**marking 自体の Galois 不変性**ではない。自動的に降りるのは、ここでは **$\mathbf Q$-有理な $0,1,\infty$ の branch label** までである。fiber の基点、sheet labeling、特定の branch-cycle element の選択などの**追加 marking は、Galois 不変性を別に示す必要がある**。$\mathrm{Aut}=1$ は、存在する marking-preserving 同型を**一意にする**だけで、**任意の marking の存在を保証しない**。

### E.4.1 撤回の所在(本文を grep して確認した実在箇所)

| 所在 | 記述 | 処置 |
|---|---|---|
| **§D.0 ③行** | 「marked / mere の差 — 本件では差がない。$\mathrm{Aut}=1$ なので marking は rigidification として何も追加せず、marked 降下と mere 降下は同値」 | ★ **撤回** |
| **§D.6 言えること (3)** | 「marked 版も同じ($\mathrm{Aut}=1$ ゆえ marking は降下に何も足さない)」 | ★ **撤回** |
| **§D.7** | Sol は「D.7(3)」も撤回対象に挙げたが、**§D.7 は機械 spot-check であり marked 主張を含まない**(本文 grep で確認: `marked`/`marking`/`標識` の出現は §1 規約宣言・§5.1・§6・§8・§D.0・§D.6 のみ) | **該当なし**。代わりに §D.8 **MD-DESC 行**は「**mere cover** についての主張」と読むこと(本追記が注記) |

### E.4.2 無影響の確認(何が生き残るか)

| 対象 | 影響 | 理由 |
|---|---|---|
| **定理 M2-GEO(§6)** | **無影響** | 「標識つき $\bar{\mathbf Q}$-被覆として同型」は **$\bar{\mathbf Q}$ 上の幾何的主張**(Nielsen 類の同時共役)であって、降下の主張ではない |
| **定理 M2-UNIQ(§7)** | **無影響** | $\mathrm{Aut}_{\bar F}=1$ の計算そのもの |
| **定理 M2-DESC(§D.3 / §E.2)** | **無影響** | **mere cover** についての主張。§E.2 の証明は marking を一切使わない |
| **FAM-U が要求するもの** | **無影響** | 要求は **mere cover** と **$F_n$ 上の明示 source-map** であり、追加 marking の降下ではない(F95-1.1・W95-1.1 末) |
| **§10 FINDING の M2-NF / NIE / INV / SEP / AUT** | **無影響** | いずれも $\bar{\mathbf Q}$ 上の群論・組合せ論 |

### E.4.3 新設 UNKNOWN

> **【UNKNOWN M2-MARK】** marking(fiber 基点・sheet labeling・branch-cycle element の選択)込みの降下がどの体上で成り立つかは **未決**。本稿は**主張しない**。必要になった時点で別命題として立て、Galois 不変性を明示的に示すこと。**現在の FAM-U の鎖はこれを要求していない。**

> ### ★教材(便 95 P95-1.1 末の再掲・工房の共有知として)
> **$\mathrm{Aut}=1$ は「余計な marking は何でも降りる」という定理ではない。** $\mathrm{Aut}=1$ が消すのは **descent isomorphism の選択肢**であり、**marking 自体の Galois 不変性**ではない。

---

## E.5 効力対応表(本文のどの行が、どう読み替わるか)

| 本文の所在 | 旧記述 | 本追記後の読み |
|---|---|---|
| **冒頭 状態札** | 「単系統(python のみ・cross-checked ではない)」 | **冒頭注記ブロック**が正:§9 は **cross-checked**(GAP×python)・§D.7 は**単系統** |
| **§D.1 (T2)** | $m:=\chi(\tau)\in\widehat{\mathbf Z}^\times$ | $\bar m:=\chi(\tau)\bmod2n\in(\mathbf Z/2n)^\times$ の**任意の整数代表**(§E.1.2) |
| **§D.1 (T2) の位置づけ** | **主証明の外部入力** | ★ **参考経路の外部入力**へ降格(主証明は §E.2・BCL 不要) |
| **§D.3 言明の量化** | $\alpha\in(\mathbf Z/n)^\times$ | $\widetilde\alpha\in\mathbf Z$、$\gcd(\widetilde\alpha,n)=1$、$\alpha:=[\widetilde\alpha]$(§E.1.1) |
| **§D.3 段 3** | 「$T^\tau$ が一意に定まる」 | 「$T^\tau$ は**単一軌道に属する**」(軌道は $4n^2$ 元)(§E.1.3) |
| **§D.3 段 1–5 全体** | **主証明** | ★ **参考(第二経路)**。撤回はしない — 入力が交わらない独立経路として保持(§E.2.2) |
| **§D.3 末「反証の急所は (T2)」** | (T2) の正確な形 | ★ **明示同型 $A,B$**(§E.2.1 で全段検算済)。(T2) は参考経路の急所として残る |
| **§D.4** | $\Theta^*W_0$ | $(\theta^*\widetilde W_0,\theta^*\iota)$ を先に書き商へ降ろす(§E.1.4)。**§D.4 の内容自体は §E.2 の $A,B$ に吸収された** |
| **§D.0 ③ / §D.6(3)** | marked 版も同じ | ★ **撤回**(§E.4) |
| **§D.8 MD-DESC 行** | — | **mere cover** についての主張と読む(§E.4.1) |
| **§D.8【文献要請 M2-2】** | 未消費 | ★ **消費**(§E.3)。ただし**引用形の受領**であり原文照合ではない |
| **§8【文献要請 M2-1】** | §D で消費済 | 不変(消費済) |

---

## E.6 残る UNKNOWN と Sol への申し送り(便 96)

### E.6.1 §D.9 監査点の帰趨

| 監査点 | 便 95 の回答 | 現状 |
|---|---|---|
| **F**(三成分の独立共役) | **F95-1.3(4)** で YES(理由は私の読みより強い) | ★ **解消**(§E.3) |
| **G**(結論の強さ・外部知識と衝突しないか) | **明示回答なし・反例の指摘もなし** | ⚠ **UNKNOWN 継続**。「反例が報告されていない」は「反例がない」ではない。ただし §E.2 により反証の急所が自前検算可能な所へ移った |
| **H**(有限射の fpqc 降下) | **F95-1.4 末尾**で肯定 | ★ **解消** |
| **I**((M4) 観察の格) | **F95-1.6** で PASS(依存の向き $\mathrm{M2}\Rightarrow\mathrm{M4}$ を固定・逆向き禁止) | ★ **解消**(M4 は M2 の系) |
| **J**(被覆 $\mathbf Q$・測定 $F_n$ の分離) | **F95-1.5** で PASS(FAM-U の射程宣言を承認) | ★ **解消** |

### E.6.2 申し送り(便 96)

- **監査点 K(新規・最重要)**: **§E.2.1 の逐段検算表 10 項目**。私は Sol の補正証明を自前で潰したつもりだが、見落としがないか。とくに **8 番(合成の型)** — $B$ が $\mathbf P^1_k$ 上ではなく $\theta$ を覆う射であること、$\theta$ が $\mathbf P^1_\lambda$ 上恒等であること、この二つで「$A\circ B^{-1}$ が $\mathbf P^1_\lambda$ 上の同型」と結論した箇所。
- **監査点 L(新規)**: **【UNKNOWN M2-MARK】**(§E.4.3)を独立の未決命題として台帳に立てる価値があるか。現在の鎖は要求していないので、**立てずに「要求されていない」と記録するだけ**でよいと私は読んだが、将来 GT 作用(marked triple への $G_{\mathbf Q}$-作用)を使う段が来ると必要になる可能性がある。
- **監査点 M(継続)**: **監査点 G**(反例の有無)。$n=7$ の 3 個の degree-14 dessin(passport $((14),2^61^2,(14))$・モノドロミー位数 196)が $\mathbf Q$ 上、という主張に心当たりがあれば指摘されたい。**主証明が BCL から独立になった今、反例が出れば $A$ か $B$ の初等的誤りを意味する**ので、判定が鋭くなった。

---

## E.7 FINDING(本追記の分)

| # | 格 | 内容 |
|---|---|---|
| **ME-DIRECT** | ★★ **主証明の差し替え(便 95 F95-1.4 供給)** | M2-DESC の主証明を **$\mathbf Q(i)/\mathbf Q$ 直接降下**へ。外部入力は **(T1) Weil 降下 + 有限射の fpqc 降下**のみ、**BCL 不要**。$\Gamma_n$ の組合せ論も使わない ⟹ §D.3 とは**入力の交わらない第二経路**が成立(紙の二経路一致・`cross-checked` とは呼ばない) |
| **ME-CHECK** | ★ **独立検算(自前)** | §E.2.1 の **10 項目**を手計算で全 PASS。使った入力は「$n$ 奇」と「$\epsilon^2=1$」だけ。**反証の急所が外部文献から自前検算可能な初等代数へ移った** |
| **ME-TYPE** | ⚠ **自認(型の修正 2 件)** | (a) $\alpha\in(\mathbf Z/n)^\times$ ⟹ $\widetilde\alpha\in\mathbf Z$ + $\alpha=[\widetilde\alpha]$(追補 f94 の **FU-TYPE と同型の欠陥**を本稿で再発していた)。(b) $m\in\widehat{\mathbf Z}^\times$ ⟹ $\bar m\in(\mathbf Z/2n)^\times$ の整数代表。**補題 POW の言明自体は修正不要**($\bar m$ の代表は自動的に奇数) |
| **ME-ORB** | ⚠ **自認(誤記の削除)** | §D.3 段 3 の「$T^\tau$ が一意」は文字どおり偽(軌道は $4n^2$ 元)。必要なのは**単一軌道への所属**のみ ⟹ 論証に影響なし |
| **ME-PULL** | ⚠ **自認(記法の型)** | $\Theta^*W_0$ は型が曖昧。$(\theta^*\widetilde W_0,\theta^*\iota)$ を先に書き商へ降ろす。**「$\mathbf P^1_\lambda$ 上なら $\theta^*W_0=W_0$」は結論の先取り** |
| **ME-MARK** | ★ **撤回** | 「$\mathrm{Aut}=1$ だから marked 版も同じ」を撤回。所在 = §D.0③・§D.6(3)(§D.7 には該当なし)。**mere cover と $F_n$ 上の明示 source-map には無影響**ゆえ (M2) 閉鎖は不変。**【UNKNOWN M2-MARK】**を新設 |
| **ME-BCL** | **文献要請の消費** | 【文献要請 M2-2】= 消費(F95-1.3 が引用先 4 件と仮定の正確形を供給)。⚠ **引用形の受領であり原文照合ではない**。主証明が BCL 非依存になったため **Lean 公理化の対象からも外れる**(P95-4.1(6) と一致) |
| **ME-GRADE** | ★ **格の更新** | §9 の有限 spot-check は **cross-checked**(GAP×python・裁定 329)。§D.7 は**単系統のまま**。冒頭注記ブロックが CV-10 の誘導を担う |
