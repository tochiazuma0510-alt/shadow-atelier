# M3 case (b) — 窓 B の商曲線 $C$ の方程式系($\bar P$ 非 Weierstrass)**v1**

**状態札: `design + partial result (candidate) / 紙 + GAP/python 単系統・Sol 監査前・解は未確定`**
起草: 影工房 数学者(Claude・Opus 5)/ 2026-07-31
委嘱: 司令塔「case (b) の方程式系を立てて解く」(裁定 244 後の続行指示)
前提正本: `u_meas_m1_passport_v1.md`(M0–M2 凍結)/ `u_meas_m3_design_v1.md`(命題 U-LOC・U-Q・§6 予言)/ `u_meas_cal_a5_v1.md`(CAL-M3 PASS・case (a) 棄却)

> **封印・汚染管理**: $u$ の値には触れていない(本書は $C$ の**モデル探索**まで。命題 U-LOC で値を読むのは $C$ が確定してから)。$K^{(5)}$ 非接触。DB(arXiv:1805.07751)は検疫どおり**引いていない**。

---

## 0. 結論(5 行)

1. **case (b) は独立に確認された(proof + 機械)**: $\bar\psi$ の固定点はちょうど **2 個**(`u_meas_probe7.g`)⟹ $\bar\psi\ne\iota$ ⟹ **$\bar P$ は Weierstrass 点でない**。case (a) 棄却(命題 CAL-a2)と整合。
2. **副産物の訂正**: $Y:=W/S_3$ の種数は **1(楕円曲線)**。前便の思考中に一度 $g_Y=0$ と口走ったが、それは RH の算術ミス($2g-2=0\Rightarrow g=1$)。**文書には未混入**だが記録する。
3. **モデルが確定した**: $C:\ y^2=x^6+ax^4+bx^2+c$(**偶六次**)、$\bar P=\infty_+$、$\bar\psi(x,y)=(-x,-y)$、$\iota\bar P=\infty_-$ かつ $t(\infty_-)=\tfrac32$。$t-\tfrac32$ は $\bar\psi$-反不変で、その空間は**次元 4**(極位数 3,5,7,9)。
4. **方程式系は 6 未知数 6 条件**(または $Y$ 側で 4 未知数 4 条件)で 0 次元。しかも **$Y$ は $\mathbf Q$-有理な 3-捻れ点をもつ楕円曲線**であることが**証明できた**(§4)— 配達文献 B6/B4 の直撃点。
5. **mod-$p$ 悉皆探索を実装・$p=7$ を走行中**(`u_meas_caseb_search.py`)。**本書時点で解は未確定**。次便で報告する。

---

## 1. case (b) の独立確認(前便の「$g_Y$ 疑義」の決着)

前便で case (a) を棄却したあと、私は「$Y=W/S_3$ が種数 0 なら $C\to Y$ が超楕円写像になり $\bar\psi=\iota$、すなわち case (a) に戻ってしまう」という矛盾を疑った。**この疑義は解消した。原因は私の RH の算術ミスである。**

### 1.1 機械による決着(`u_meas_probe7.g`)

$\bar\psi$ は $\nu(t)=3-t$ を覆う $C$ の自己同型。その持ち上げ $\varrho\in\mathrm{Sym}(\Lambda)$ は
$$\Theta(A)^\varrho=\Theta(B),\qquad \Theta(B)^\varrho=\Theta(A)$$
で特徴づけられる($\Theta(A)=\pi^{-1}$、$\Theta(B)=X^{-1}\pi$、M1 §3.4)。$S_9$ 全体で走査した結果:

| 出力 | 値 |
|---|---|
| 解 $\varrho$ の個数($S_9$ 内・悉皆) | **1**(一意) |
| $\varrho$ の位数・巡回型・固定点数 | **2**、$2^41$、**$\#\mathrm{Fix}=1$** |
| $\varrho\in P$ か | **true**($\varrho\in\mathrm{PSL}(2,8)$) |
| $W$ 水準の $\psi$: $X^s=Y$、$Y^s=X$ | **true / true**($s$ = marking の対合)、$\#\mathrm{Fix}_\Lambda(s)=1$、型 $2^41$ |

$\nu$ の固定点は $t=\tfrac32$ と $t=\infty$。$t=\infty$ 上は 1 点($\bar P$、必ず固定)、$t=\tfrac32$ 上は $\#\mathrm{Fix}(\varrho)=1$。

$$\boxed{\ \#\mathrm{Fix}_C(\bar\psi)=1+1=\mathbf 2\ }$$

種数 2 の対合の固定点数は $0,2,6$ のいずれかで、**6 のときに限り超楕円対合**。よって $\bar\psi\ne\iota$、**$\bar P$ は Weierstrass 点ではない ⟹ case (b)** ✓。
RH: $2\cdot2-2=2(2g_Y-2)+2\Rightarrow g_Y=1$。**$Y=C/\bar\psi=W/S_3$ は楕円曲線。**

### 1.2 整合の三重チェック

| 経路 | 計算 | 結果 |
|---|---|---|
| $C\to Y$(次数 2・$f=2$) | $2=4g_Y-4+2$ | $g_Y=1$ ✓ |
| $W\to Y$(次数 6・$S_3$) | $f_\varphi=0$(M1 §3.4)・$f_\psi=2$(= $\bar P$ 上 1 + $\lambda=\tfrac12$ 上 $\#\mathrm{Fix}(s)=1$)⟹ 分岐寄与 $3\cdot2\cdot1=6$;$\ 6=6(2g_Y-2)+6$ | $g_Y=1$ ✓ |
| $Y\to\mathbf P^1_J$(次数 9・$(2,3,\infty)$ 軌道体) | 型 $2^41,\ 3^3,\ (9)$;$\ 2g-2=-18+4+6+8=0$ | $g_Y=1$ ✓ |

> **⚠ 自認(3 度目の同型ミス)**: 第 3 行を前便の思考中に $2g-2=0\Rightarrow g=0$ と誤読した。**RH の右辺が 0 なら種数は 1 である。** 【M3-c】(軌道体生成系の同定)に続く**算術の初歩ミス**であり、Sol の監査点に加える。**幸い文書には混入していない**(前便の成果物 3 本に $g_Y$ の記載は無い)。

---

## 2. case (b) のモデル(確定)

### 2.1 曲線の形

$\bar\psi$ は非超楕円対合で、$\iota$ は中心的だから $\iota$ は $\mathrm{Fix}(\bar\psi)=\{\bar P,R\}$ を保つ。$\bar P$ は非 Weierstrass($\iota\bar P\ne\bar P$)ゆえ $\iota$ は 2 点を**入れ替える**: $R=\iota\bar P$。$t(\bar P)=\infty$、$t(R)=\tfrac32$($\nu$ の他方の固定値)。

$\langle\iota,\bar\psi\rangle\cong V_4$ で $\mathrm{Fix}(\bar\psi)=\{\bar P,\iota\bar P\}$ が超楕円写像の 1 本のファイバー ⟹ 標準形

$$\boxed{\ C:\ y^2=f_6(x)=x^6+ax^4+bx^2+c\ \ (\textbf{偶六次}),\qquad \bar P=\infty_+,\ \ \iota\bar P=\infty_-\ }$$
$$\iota(x,y)=(x,-y),\qquad \bar\psi(x,y)=(-x,-y),\qquad \iota\bar\psi(x,y)=(-x,y).$$

($f_6$ をモニックにしてよい: $\bar P$ が $\mathbf Q$-有理 ⟹ 無限遠 2 点が $\mathbf Q$-有理 ⟹ 最高次係数は平方 ⟹ $y$ のスケールで吸収。$x\mapsto\alpha x$ は偶性を保つ唯一の残存自由度。)

**検算**: $\bar\psi$ の固定点は $\{x=-x,\,y=-y\}$ の解 = $\infty_\pm$ のみ(有限点では $x=0,y=0$ が要るが $f_6(0)=c\ne0$ が genus 2 の条件から従う)。$\bar\psi$ は $\infty_\pm$ を**各々固定**($y/x^3$ が不変)⟹ ちょうど 2 点 ✓ §1 と一致。

### 2.2 $t-\tfrac32$ の住処(次元 4)

$t-\tfrac32$ は $\bar\psi$-反不変で極因子 $9\bar P$。$\bar\psi$ は $\bar P$ の局所助変数 $s=1/x$ に $s\mapsto-s$ で作用するから、極位数 $n$ の固有関数は **反不変 $\iff n$ 奇**。$\bar P$ 非 Weierstrass ⟹ ギャップ列 $\{1,2\}$ ⟹ $L(9\bar P)$ の極位数は $0,3,4,5,6,7,8,9$。奇数は $3,5,7,9$:

$$\boxed{\ \dim\bigl(L(9\bar P)^{-}\bigr)=4,\quad \text{基底の極位数 }3,5,7,9\ }$$

$q(x):=x^3+\tfrac a2x$、$e:=\tfrac b2-\tfrac{a^2}8$、$\theta:=y+q$ とおくと(いずれも反不変・$\infty_-$ で極なし):

| 基底 | 式 | $\mathrm{ord}_{\infty_+}$ | $\mathrm{ord}_{\infty_-}$ |
|---|---|---|---|
| $\theta$ | $y+q$ | $-3$ | $1$ |
| $\zeta_5$ | $x^2\theta+e\,x$ | $-5$ | $\ge1$ |
| $\zeta_7$ | $x\,\theta^2$ | $-7$ | $1$ |
| $\zeta_9$ | $\theta^3$ | $-9$ | $3$ |

($\infty_-$ での展開 $y=-x^3-\tfrac a2x-e\,x^{-1}+O(x^{-3})$ から $\theta=-e\,x^{-1}+O(x^{-3})$、よって $x^2\theta=-ex+O(x^{-1})$ で $+ex$ が極を消す。反不変性から $\mathrm{ord}_{\infty_-}$ は奇 ⟹ $\ge1$。)

$$\boxed{\ t=\tfrac32+c_3\theta+c_5\zeta_5+c_7\zeta_7+c_9\zeta_9,\qquad c_9\ne0\ }$$

$\theta^2=(q^2+f_6)+2q\,y$、$\theta^3=(3f_6q+q^3)+(f_6+3q^2)\,y$ より $t=A(x)+B(x)y$ で
$$\deg A=9,\qquad \deg B=6\qquad(\text{最高次係数 }A:4c_9,\ B:4c_9).$$

### 2.3 分岐条件(1 本で足りる)

$$\mathcal N_\tau(x):=\mathrm{Norm}_{\mathbf Q(C)/\mathbf Q(x)}(t-\tau)=(A-\tau)^2-B^2f_6 .$$
最高次($x^{18}$)は $16c_9^2-16c_9^2=0$ で消え、$\deg\mathcal N_\tau=9$(極因子 $9(\infty_++\infty_-)$)。$t-\tau_1$ が 3 個の 3 重零点をもつ条件は
$$\boxed{\ \mathcal N_{\tau_1}(x)=\kappa\,g(x)^3\quad(g\ \text{モニック 3 次})\ }$$
**$\tau_2$ 側は自動**: $t^{\bar\psi}=3-t$ が $\tau_1\leftrightarrow\tau_2$ を入れ替えるので、$\bar\psi$ が $t-\tau_1$ の零点を $t-\tau_2$ の零点へ移す。**case (a) と違い $\deg A=9$ なので「$A$ が定数」という強制は働かない**(補題 CAL-a1 の論法は $\deg A\le4$ に依存していた)。

### 2.4 自由度の勘定(0 次元)

| | 未知数 | 条件 |
|---|---|---|
| 曲線 $(a,b,c)$ | 3 | |
| $t$ の係数 $(c_3,c_5,c_7,c_9)$ | 4 | |
| 正規化 $x\mapsto\alpha x$ | $-1$ | |
| **計** | **6** | |
| $\mathcal N_{\tau_1}$ が立方(9 個の零点が 3 個の 3 重零点へ) | | **6** |

$$\boxed{\ 6=6\ \Longrightarrow\ \textbf{0 次元。剛性(Nielsen 類 1)と整合。}\ }$$

**規約の凍結(要請 1(b) に文献が無かったので自前で決める・裁定 244 の方針どおり)**:
> **【凍結 NORM-b】** (i) $\lambda$ 側の座標は $\mathbf P^1_\lambda$ の標準座標($0,1,\infty$ が分岐点)、$t=\lambda+\frac1{1-\lambda}+\frac{\lambda-1}\lambda$ を**動かさない**(分岐点は $3\zeta_6^{\pm1},\infty$ に固定)。(ii) $C$ 側は $f_6$ **モニック偶六次**、$\bar P=\infty_+$、残る自由度は $x\mapsto\alpha x$ のみ。(iii) $\alpha$ は解が得られてから「$a$ を最も簡明にする」規則で最後に固定する(値の判定 $[u_0]_9$ は $\alpha$ に依らない — 補題 SL-2)。

---

## 3. mod-$p$ 悉皆探索(実装・走行中)

`search/probe/wac_v1/u_meas_caseb_search.py`(純 python・$\mathbf F_p$ 多項式演算を自前実装・浮動小数点不使用)。

* $p\equiv1\pmod3$ を選ぶ($\tau^2-3\tau+9$ が $\mathbf F_p$ で分解する条件)。$p=7$: $\tau\in\{1,2\}$。
* $(a,b,c)$ を走査($f_6$ が squarefree = 種数 2 のもののみ)、$(c_3,c_5,c_7,c_9)$ を走査($c_9\ne0$)。
* 各候補で $A,B$ を作り $\mathcal N_{\tau_1}$ を計算、$\deg=9$ かつ $\mathcal N=\kappa g^3$($g$ 三次)を判定(判定は $\mathcal N/\gcd(\mathcal N,\mathcal N')$ が三次で、その立方倍が $\mathcal N$ に一致するか)。
* $p=7$ の探索空間は $\approx7^6\cdot\frac67\approx7\times10^5$。$p=13$ は $\approx5.8\times10^7$ で純 python では重い ⟹ **$p=7$ の結果を見てから絞り込み版を書く**。

> **⚠ 本書時点で走行中。ヒットの有無・個数は未確定。** 得られた候補は**必ず**次の順で篩う:
> 1. $f_6$ squarefree(種数 2)・$\bar P$ 非 Weierstrass;
> 2. **monodromy が $\mathrm{PSL}(2,8)$(9T27)であること**・**分解可能でないこと**(前便の偽解事件の再演防止・cert schema v2 の必須ゲート);
> 3. $\mathbf Q$ への持ち上げ(有理再構成 → $p$ 進 Newton);
> 4. §4 の 3-捻れ篩;
> 5. 最後に命題 U-LOC で $[u_0]_9$ を読む。

---

## 4. ★ $Y$ 側の構造 — **$\mathbf Q$-有理な 3-捻れ点をもつ楕円曲線**【proof】

$Y=C/\bar\psi$ は楕円曲線(§1)。$u:=x^2$、$w:=xy$ とすると
$$Y:\ w^2=u\,(u^3+au^2+bu+c)=u^4+au^3+bu^2+cu,$$
$\bar P_1:=$($\infty_+$ の像)$=\infty^Y_+$。$C\to Y$ は $\infty_\pm$ の 2 点でのみ分岐 ✓。

$J:=t^2-3t+9=(t-\tau_1)(t-\tau_2)$ は $t\mapsto3-t$ で不変 ⟹ $\bar\psi$-不変 ⟹ **$Y$ 上の関数**、次数 9、$\mathrm{div}_\infty(J)=9\bar P_1$。零点は $C$ 上の $3\sum A_i+3\sum B_j$ で、$\bar\psi$ が $A$ 達と $B$ 達を入れ替えるから
$$\mathrm{div}(J)=3D_A-9\bar P_1,\qquad D_A\ \text{は次数 3 の有効因子}.$$

> ### 命題 CB-3T【proof】
> $\mathfrak t:=\bigl[D_A-3\bar P_1\bigr]\in\mathrm{Pic}^0(Y)=Y$ は **位数ちょうど 3** の点であり、しかも **$\mathbf Q$-有理**である。
> ⟹ **$Y$ は $\mathbf Q$ 上の楕円曲線で $Y(\mathbf Q)_{\rm tors}\supseteq\mathbf Z/3$。**

**証明.** $3\mathfrak t=[\mathrm{div}(J)]=0$ ⟹ 位数 $\mid3$。
**位数 $\ne1$**: もし $\mathfrak t=0$ なら $D_A\sim3\bar P_1$ で $J=\text{const}\cdot h^3$、$h\in L(3\bar P_1)$(次数 3 の写像 $Y\to\mathbf P^1$)。すると $\Xi:=J-\tfrac{27}4$ の重複零点は $h^3=\tfrac{27}4$ かつ $(h^3)'=0$ の点、すなわち $h'=0$ の点のうち $h$ が 1 つの値 $\eta:=(\tfrac{27}4/\text{const})^{1/3}$ を取るもの。$\Xi$ は $C\to Y$ の分岐を決め、分岐は 2 点($\bar P_1$ と $\bar R_1$)しかないから $\mathrm{div}_0(\Xi)$ は **1 個の単純零点 + 4 個の 2 重零点**でなければならない。しかし $h$ は値 $\eta$ を(重複込みで)3 回しか取らないので 2 重零点は 3 個以下 — 4 個に足りない。矛盾。
**$\mathbf Q$-有理性**: $J\in\mathbf Q(Y)$、$\bar P_1$ は $\mathbf Q$-有理($t$ の唯一の極の像)ゆえ $D_A=\tfrac13\mathrm{div}_0(J)$ は $G_{\mathbf Q}$-安定な因子、したがって $\mathfrak t\in Y(\mathbf Q)$。$\blacksquare$

> **⟹ 探索空間の縮約**: $\mathbf Q$-有理 3-捻れをもつ楕円曲線は 1 助変数族
> $$Y_\beta:\ v^2+\alpha uv+\beta v=u^3\quad(3\text{-捻れ点は }(0,0))$$
> で尽くされる(古典)。$Y$ の 1 モジュライがこの族で明示される ⟹ **§2.4 の 6 未知数を $Y$ 側の 4 未知数(モジュライ 1 + $D_A$ 2 + $J$ のスケール 1)へ落とせる**。条件は「$\Xi=J-\tfrac{27}4$ の零点型が $(1,2^4)$」の 4 本。
> **これが配達文献 B6(Suluyer–Sadek・超楕円 Jacobian の有理捻れ)と B4(Naranjo ら・種数 2 の巡回被覆)の直撃点である**(§6)。
> **⚠【型 C 警戒】遵守**: 本命題は $Y$($=C/\bar\psi$、**楕円曲線**)の 3-捻れであって、$\mathrm{Jac}(C)[3]$ の $\mathbf Z_3\times\mathbf Z_3$ 構造ではない。B1/B5 の $\sqrt3$-level とは**別の量**である。覚書の警戒どおり束ねない。

**M7-B4 の篩との関係**: 設計書 §3 の B4 は「$W\to C$ が étale $C_3$ ⟹ $\mathrm{Jac}(C)^\vee[3]$ の $\mathbf Q$-有理点」だった。本命題はそれとは**別の**、より安価で直接的な篩を与える(**$Y$ という 1 次元の対象の上の 3-捻れ**)。候補モデルは $Y$ を作って 3-捻れを確認するだけで篩える。

---

## 5. 証明書 schema v2 のゲート(採用済みの要請を反映)

`u-meas-cert/v2` の `dessin_binding` に**必須**:
```jsonc
"monodromy_computed": "9T27 (PSL(2,8))",   // 計算値。passport からの推定は不可
"primitive": true,                          // 9 点上原始的
"decomposable": false,                      // t が低次写像の合成でないこと
"quotient_model": { "curve": "y^2 = x^6 + a x^4 + b x^2 + c", "even_sextic": true,
                    "Pbar": "infty_+", "Pbar_is_weierstrass": false,
                    "t_basis": ["theta","zeta5","zeta7","zeta9"], "coeffs": [ /*c3,c5,c7,c9*/ ] },
"psibar_fixed_points": 2,                   // = case (b) の指紋(case (a) なら 6)
"Y_three_torsion_rational": true            // 命題 CB-3T
```
`decomposable` の判定手順(前便の偽解の再演防止): $t$ が $\mathbf Q(t)\subsetneq F\subsetneq\mathbf Q(C)$ なる中間体をもつか。**前便の case (a) 解は $\mathbf Q(t)\subset\mathbf Q(t,G(x))\subset\mathbf Q(C)$($G^3=256(t^2-3t+9)$)で引っかかる。**

---

## 6.【文献】読んだ範囲の申告

**本便で読んだのは司令塔の覚書 `docs/notes/litgate_positive_genus_belyi_v1.md` 全文(§0–§4)のみ。原著 10 本は未読。**
理由: §1–§4 は $\bar\psi$ の固定点計算と初等的な因子計算で閉じ、外部の手続きを要さなかった。**次便(方程式を実際に解く段)で以下の順に精読する予定**:

| 優先 | 文献 | 読む目的(具体的な問い) |
|---|---|---|
| 1 | **A1 Sijsling–Voight 1311.2529** | 正種数での「関数体の基底 + 未知係数」の立て方が §2.2 の $L(9\bar P)^-$ と一致するか / $p$ の選び方 / 有理再構成の失敗判定 |
| 2 | **A6 Manes–Melamed–Tobin 1908.10459** | $\mathrm{div}_\infty(t)=9\bar P$(single cycle)特有の簡約が §2.3 の $\mathcal N=\kappa g^3$ を軽くするか |
| 3 | **B6 Suluyer–Sadek 2410.14454** | 命題 CB-3T の族($Y_\beta$)を使った探索空間の縮約 |
| 4 | **B4 Naranjo ら 2306.02147** | 種数 2 の巡回被覆の分類が $W\to C$(étale $C_3$)に翻訳できるか |
| 5 | A2 KMSV 1311.2081 | M7 の数値第二系統 |

**DB(A3・arXiv:1805.07751)は検疫を尊重し引いていない。** 自前構成が済んでから司令塔の解禁を待つ。

---

## 7. FINDING と未閉鎖

| # | 格 | 内容 |
|---|---|---|
| **CB-1** | **proof + 機械** | $\#\mathrm{Fix}_C(\bar\psi)=2$($\varrho$ は $S_9$ 内で一意・型 $2^41$)⟹ **case (b) 確定**・$g_Y=1$ |
| **CB-2** | 自認 | $g_Y$ の RH 算術ミス($2g-2=0\Rightarrow g=1$)。文書未混入だが記録。**Sol 監査点に追加** |
| **CB-3** | **proof** | case (b) のモデル: **偶六次** $y^2=x^6+ax^4+bx^2+c$・$\bar P=\infty_+$・$L(9\bar P)^-$ は次元 4(極位数 3,5,7,9)・明示基底 |
| **CB-4** | **proof** | 方程式系は **6 未知数 6 条件**。$\tau_2$ 側の条件は $\bar\psi$ 対称性から自動(条件が半分で済む) |
| **CB-5** | **proof** | **命題 CB-3T**: $Y=W/S_3$ は $\mathbf Q$-有理な位数 3 の点をもつ楕円曲線。⟹ 探索空間の 1 助変数族への縮約 + 安価な篩 |
| **CB-6** | 規約 | **【凍結 NORM-b】**(自由度の固定)— 文献に該当が無かったため自前凍結(裁定 244 の方針) |
| **CB-7** | 進行中 | mod-7 悉皆探索を実行中。**解は未確定** |

### 出所(provenance)

| ファイル | SHA-256 | 内容 |
|---|---|---|
| `search/probe/wac_v1/u_meas_probe7.g` | `c95e9d71fff5fbd158c8458d4b0eb77468e180cc19b63f8cbcf6b6b57a6c813c` | $\varrho$ の悉皆決定・$\#\mathrm{Fix}(\bar\psi)=2$(GAP 4.16.0) |
| `search/probe/wac_v1/u_meas_caseb_search.py` | `580a326843ce98dd0a54ce1ecf946487d6abdc7d26b47faa006749d40f383083` | case (b) の mod-$p$ 悉皆探索(純 python・$\mathbf F_p$ 多項式演算自前・**走行中**) |

**単系統。cross-checked ではない。Lean verified ではない。**
**⚠ 探索の実行状況**: $p=7$ の走査は 1 プロセスで進行中($\approx7\times10^5$ 候補・純 python)。**本書は結果を含まない。** $p=13$ は同実装では重すぎるので、【CB-b】($Y_\beta$ 族への書き換え)で軽量化してから回す。

### 未閉鎖・次の一手
* 【CB-a】**mod-7 の結果回収** → ヒットの monodromy 判定(9T27・原始性・非分解)→ $p=13$ で確認 → 有理再構成。
* 【CB-b】$Y$ 側($Y_\beta$ 族・4 未知数)への系の書き換え。**探索が重ければこちらが本命**。
* 【CB-c】A1・A6 の精読(§6 の表)。
* 【CB-d】本書は**紙 + 単系統・Sol 監査前**。**Lean 検証ではない。** $u$ の値には触れていない。
