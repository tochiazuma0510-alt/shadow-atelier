# $u_7$ 発火執行ログ v1(裁定 300 認可・数学部)

**状態札: `measured (cross-checked, 単系統実装) / Sol 監査前 / Lean 検証ではない / 下流ゲート G-1〜G-4 未評価`**
執行: 影工房 数学者(Claude・Opus 5)/ 2026-08-01
認可: **裁定 300**(発火)/ 凍結: **裁定 287** + 凍結修正 v2(`u7_twist_determination_v1.md` §3)
cert: **`search/certs/u7_fire_20260801.json`**(`sha256 = 02d2ee59…f67074b`・全数値は機械生成)
**凍結文書は不変**(本書は執行ログであり、`u7_meas_design_v1.md` / `u7_twist_determination_v1.md` を書き換えていない)。

---

## 0. 結論(先に 7 行)

1. **CAL-3(fail-closed ゲート P-11 / MP-7)PASS**: 同一装置で $n=3$ を走らせ $u_3=-4$(公開値)を再現。さらに $\mathrm{ord}([-4]_6)=3$ も再現 — **正典の定理 K3 と逐語一致**。
2. **経路 A(幾何 descent)実行**: $\bar{\mathbf Q}$ 正規形は $\mathbf Q(i)\subset F$ 上に取れ、補題 TW-1(b) の一意性で $F$-モデルと同定。決定式 $\mathrm{disc}\,F[R_1,R_2]$ を実行 ⟹ **$R_\pm$ は個別に $F$-有理**、すなわち **$[\gamma]=1$**。
3. **経路 B(有限群)実行**: 橋は正典で立つ((W2)+(W2)-fam+$\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X^2\rangle)$+系 B-4c+補題 B-5)。$X^2\in AH$ ゆえブロック指標は自明 ⟹ **$[\gamma]=1$**。位数による独立論証($|\mathfrak F_0|=7$ 奇 ⟹ $\mathrm{Hom}(\mathfrak F_0,C_2)=1$)も同結論。
4. **両経路一致(`agree = true`)⟹ cross-checked**(**verified ではない** — Lean 未使用・実装は単系統)。
5. **測定値**: $\boxed{u_7=-4}$。全付値: $\mathfrak p\mid2$ の 2 素点で $w_\mathfrak p(u_7)=4$、**他は全て 0**。
6. **P-9 の 6 量**: $[u_7]_2$ **自明**、$[u_7]_7$ **非自明**、$u_7=-4\in\mathbf Q^\times$、$\exists\mathfrak p:w_\mathfrak p\not\equiv0\ (7)$、$[\gamma]=[\delta_0]=1$、$\mathrm{ord}(a_7)=\mathbf 7$。
7. **NULL 枠 N-1〜N-10 は 1 つも発動せず**(`any_triggered = false`)。**LB-RES は第 1 段で決着**(第 2 段 $\mathrm{Cl}(F_7)$・第 3 段 単数群は**不要**)。

---

## 1. 橋の言明(委嘱 ①)— 経路 B は**成立する**

委嘱の懸念は「$\mathfrak F_0$ 上で自明 ⟹ $G_F$ 像全体で自明」の橋だった。正確に書き下ろすと、橋は **4 本の正典命題の合成**である。

> ### 補題 FIRE-B(経路 B の橋)
> $K=F_n=\mathbf Q(\zeta_{2M})$、$M=2n$ とする。
> **(B-i)** **(W2)**(正典・定義ノート D1 (4.12)): $1\to\mathfrak F_0\to\mathrm{GT}(N)\xrightarrow{\tilde\chi}(\mathbf Z/2M)^\times\to1$ が完全で $\tilde\chi\circ\mathrm{Ih}_N=\chi_{2M}$。
> ⟹ $\mathfrak F_0=\ker\tilde\chi$ は**部分群**(集合ではない)であり、$\gamma\in G_K$ に対し $\chi_{2M}(\gamma)=1$ ゆえ $\mathrm{Ih}_N(G_K)\subseteq\mathfrak F_0$。
> **(B-ii)** **系 B-4c**(BFC §6.3): $c_\Lambda:\mathrm{Fib}_{\vec{01}}(W_0)\xrightarrow{\sim}\Lambda$ は $G_K$-同変で、$\gamma$ の作用は $\beta_\gamma=\Phi(\mathrm{Ih}_N(\gamma))$。
> **(B-iii)** **補題 B-5 (7.1)(7.2)**: $\mathrm{Fib}$ は $\mu_M$-torsor で類は $[u^{-1}]_M$、$X$ の作用は $\tau(\zeta_M)$。
> **(B-iv)** **系 SPLIT**(凍結設計 §4.1): $u_n=\gamma c^2$、$[u_n]_2=[\gamma]_2$。
>
> このとき、ブロック分割($\bar A\bar H$-軌道)は torsor の $\mu_n$-剰余に対応し($X\notin\bar A\bar H$、$X^2\in\bar A\bar H$、$\langle\zeta_M^2\rangle=\mu_n$)、商 torsor $\mathrm{Fib}/\mu_n$ は $\mu_2$-torsor でその類は $\mu_M\xrightarrow{\xi\mapsto\xi^n}\mu_2$ の押し出し $=[u^{-1}]_2=[u]_2$。ゆえに
> $$\boxed{\ \chi_{\rm blk}\;=\;\bigl(\text{ブロック指標}\bigr)\circ\Phi\circ\mathrm{Ih}_N\;=\;[u_n]_2\;=\;[\gamma]\ }$$
> であり、これは**群準同型の合成**なので $\mathfrak F_0$ を経由する。したがって
> $$\Phi(\mathfrak F_0)\subseteq\mathrm{Stab}(\text{各ブロック})\ \Longrightarrow\ \chi_{\rm blk}=1\ \Longrightarrow\ [u_n]_2=1 .$$

**押し出しの計算(委嘱の「B-5 の正確な言明への依存」)**: Kummer 同型 $K^\times/K^{\times M}\cong H^1(G_K,\mu_M)$、$a\mapsto\kappa_a(\sigma)=\sigma(a^{1/M})/a^{1/M}$ の下で、$p:\mu_M\to\mu_M/\mu_n\cong\mu_2$ は $\xi\mapsto\xi^n$($n$ 奇ゆえ $\mu_2$ 上恒等)。$p_*\kappa_a(\sigma)=\kappa_a(\sigma)^n=\sigma(a^{n/M})/a^{n/M}$ ゆえ $p_*[a]_M=[a]_2$。**この一行が橋の要である。**

**前件の充足(正典)**:

| # | 必要な入力 | 出所 | 状態札 |
|---|---|---|---|
| B-i | (W2) | 定義ノート D1 (4.12) | **正典** |
| B-i′ | $\mathfrak F_0\cong C_n$($n=7$: $C_7$) | **(W2)-fam・裁定 120** | **candidate**(紙上 + $n\le27$ 機械検算) |
| B-ii | 系 B-4c | BFC §6.3 | (W1)(W2)(W3)(W5)+(CAL)+(TB1)–(TB4) 相対 |
| B-iii | 補題 B-5 (7.2) | BFC §7 | (TB1)–(TB4)+(W4) 相対 |
| B-iv | 系 SPLIT | 凍結設計 §4.1 | 紙上・単系統・Sol 監査前 |
| B-v | $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X^2\rangle)$ | **Sol 便 73 Q1.5 (1.13)(1.14)** + `w2fam_v1.md` §3.5(独立再確認) | 正典に採録済 |

> ### ⟹ 判定: **橋は立つ。** 経路 B は「十分条件不成立・判定不能」で閉じる必要はない。
> **しかも結論は 2 通りに出る(どちらも機械確認)**:
> * **(a) 構造論証**: $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X^2\rangle)$ かつ $X^2=2e_1\in A\subseteq AH$。ブロックは $AH$-軌道だから、$AH$ の元による内部自己同型は**各ブロックを保つ**。⟹ $\chi_{\rm blk}=1$。
> * **(b) 位数論証(「罠の 1 行」)**: $\mathfrak F_0\cong C_7$ は**奇位数群**ゆえ $\mathrm{Hom}(\mathfrak F_0,C_2)=1$。⟹ $\chi_{\rm blk}=1$。
> **(a) は (W2)-fam の同型そのものを使わず**((b) は使う)、**(b) は $\Phi$ の像の同定を使わない**((a) は使う)。⟹ **経路 B 内部でも二重化されている。**

**機械確認**: $n=3,7$($\alpha=1,2,3$)で `X2_in_AH = true`、$\Phi(\mathfrak F_0)$ の像 7 元(n=3 は 3 元)の**どれもブロックを入れ替えない**(`any_element_swaps_blocks = false`)。

---

## 2. 経路 A の $n=7$ 明示模型(委嘱 ②)

### 2.1 構成(KUM-n からの新規導出)

定理 KUM-n(4) の $\bar{\mathbf Q}$ 正規化($\delta_0=1$ ⟹ $\mu=1$、$\kappa=i\mu=i$;$\gamma=1$ ⟹ $\mu_\pm=\pm1$)を書き下すと

$$h(k)=(k-i)^{r_0}(k+i)^{-r_0}(k-1)^{r_\infty}(k+1)^{-r_\infty},\qquad (r_0,r_\infty)=(1,-\alpha),$$
$$\widetilde W_0:\ y^{\,n}=h(k),\qquad \iota(k,y)=(-k,\,1/y),\qquad W_0=\widetilde W_0/\langle\iota\rangle,$$
$$m_0=\frac{1+k^2}{1-k^2}\ \ (\iota\text{-不変}),\qquad \lambda=m_0^{\,2}\ \ (\text{すなわち }\gamma=1\text{ の座標}).$$

* $h(-k)=h(k)^{-1}$ を機械確認(19 ケース) ⟹ $\iota$ は $\widetilde W_0$ の対合で $C_n$ を反転 ⟹ $\langle\rho,\iota\rangle\cong D_n$。
* **すべての係数が $\mathbf Q(i)\subseteq F_n=\mathbf Q(\zeta_{4n})$ にある**($\zeta_n$ は $D_n$-Galois 構造にのみ必要で、$W_0$ の定義には不要)。
* 分岐: $\mathrm{div}(h)$ より $\pi$ の分岐は $k\in\{\pm i,\pm1\}$ の 4 点、$m_0(\pm i)=0$、$m_0(\pm1)=\infty$、$\lambda^{-1}(1)\leftrightarrow k\in\{0,\infty\}$ ⟹ **分岐は $\lambda\in\{0,1,\infty\}$ のみ**。
* passport: $\lambda=0$ 上 — $\widetilde W_0$ に 2 点($e=14$)を $\iota$ が入れ替え ⟹ $W_0$ に **1 点・$e=14$**;$\lambda=\infty$ 同様;$\lambda=1$ 上 — 各繊維で $\iota$ が 7 点のうち 1 点を固定し 3 対を作る ⟹ **$2^3\,1$ が 2 つ = $2^61^2$**。⟹ **$\bigl((14),2^61^2,(14)\bigr)$ ✓**。
* 補題 TW-1(b)(形式一意性)より、$W_0\times_{\mathbf Q(i)}F$ は**窓の $F$-モデルそのもの**。

### 2.2 決定式 $\mathrm{disc}\,F[R_1,R_2]$ の実行

$\lambda^{-1}(1)$ の非分岐点 $R_\pm$ = 各繊維の $\iota$-固定点(そこだけ $\widetilde W_0\to W_0$ が分岐するので $e_{W_0/V_0}=2/2=1$)。

$$h(0)=(-1)^{\alpha+1},\qquad h(\infty)=1\qquad\Longrightarrow\qquad R_+=(k,y)=(0,(-1)^{\alpha+1}),\quad R_-=(\infty,1).$$

$\alpha=1$ では $R_+=(0,1)$、$R_-=(\infty,1)$ — **いずれも $\mathbf Q$-有理**(したがって個別に $F$-有理)。

$$\boxed{\ \mathrm{disc}\,F[R_1,R_2]=1\ \Longrightarrow\ [\gamma]=1\ \Longrightarrow\ [u_7]_2=1\ }$$

**機械確認**: 19 ケース全てで `both_R_rational = true`。

### 2.3 cusp 局所展開(P-9(iii)(iv) のための値の取得)

$Q_+=(k=i,\;y=0)$ は $\widetilde W_0$ の $\lambda=0$ 上の点で、$v_{Q_+}(y)=1$($v_{Q_+}(h)=7\cdot1$)。$\iota$ が $Q_+\leftrightarrow Q_-$ を入れ替えるので $\widetilde W_0\to W_0$ は $Q_+$ で**不分岐**、ゆえに $\widehat{\mathcal O}_{W_0,P_0}\xrightarrow{\sim}\widehat{\mathcal O}_{\widetilde W_0,Q_+}$($F$-代数として)。$y$ に対応する $\tau$ が $F$-有理 uniformizer(補題 B-5(ii-loc) より $[u]_M$ は取り替えに不変)。

$t:=k-i$ と置くと厳密に
$$m_0=\frac{t(2i+t)}{2-2it-t^2}=i\,t\,(1+O(t)),\qquad \lambda=m_0^2=-t^2(1+O(t)),$$
$$h=h_1\,t\,(1+O(t)),\quad h_1=\frac{(1+i)^\alpha}{2i\,(i-1)^\alpha}=\frac{(-i)^\alpha}{2i},\qquad y^{\,n}=h\ \Longrightarrow\ t=h_1^{-1}y^{\,n}(1+O(y)),$$
$$\boxed{\ \lambda=-h_1^{-2}\,y^{\,2n}\bigl(1+O(y)\bigr)\quad\Longrightarrow\quad u_n=-h_1^{-2}=4\,(-1)^{\alpha}\ }$$

$\alpha=1$($=H_7^{\rm fun}$)⟹ $h_1=-\tfrac12$ ⟹ $\boxed{u_7=-4}$。

> **$\alpha$ 依存の消滅(整合性チェック)**: 機械は $\alpha=1,2,3$ で $u_7=-4,+4,-4$ を返した。しかし $-1=\zeta_{28}^{14}\in F^{\times14}$ ゆえ $[-4]_{14}=[4]_{14}$ — **$F^\times/F^{\times14}$ では同一**。$[\alpha]$ の取り違え(U7-14 の未解決点)は**測定値に影響しない**。$\alpha$ と $-\alpha$(同一窓・補題 TW-6 の 2 ブロック)も同様に $\mp4$ で同一類。**$K=\mathbf Q(\zeta_{2M})$ を取る理由がここで効いている。**

---

## 3. 交差確認と較正(委嘱 ③④)

| 項目 | 経路 A | 経路 B | 一致 |
|---|---|---|---|
| $[\gamma]=[u_7]_2$ | **自明**($\mathrm{disc}\,F[R_1,R_2]=1$) | **自明**(ブロック指標 = 1;構造論証 + 位数論証) | **✓ `agree = true`** |
| 使う道具 | 代数幾何(Kummer 正規形・Weil descent) | 有限群論 + 橋 $B_{\rm FC}$ | — |
| **共有前提** | 定理 TOWER-n・系 SPLIT・(W3)(W4) | 同左 | ⚠ **完全独立ではない** |

$$\boxed{\ \textbf{status = cross-checked}\ (\textbf{verified ではない})\ }$$

### 較正 CAL-3(fail-closed ゲート)— **2 項目とも PASS**

| 検査 | 装置の出力 | 既知(公開・封印外) | 判定 |
|---|---|---|---|
| $u_3$ | **$-4$** | $-4$(W3-8 系) | **PASS** |
| $\mathrm{ord}([u_3]_6)$ | **3** | **3**(定理 K3・`E1_gt_odd_dih_canonical_v1.md` L338) | **PASS** |

> 装置は $n=3$ 端点で**値と類の位数の両方**を再現した。$n=3$ は $[\alpha]$ が 1 類しかないので **C1′ 非依存の純粋な装置較正**である(凍結設計 §8.2 の設計どおり)。

---

## 4. 測定結果(cert の機械値そのまま・解釈なし)

$$u_7=-4,\qquad F_7=\mathbf Q(\zeta_{28}),\ [F_7:\mathbf Q]=12,\ M=14 .$$

| P-9 | 量 | 機械値 |
|---|---|---|
| (i) | $[u_7]_2\in F^\times/F^{\times2}$ | **自明**($-4=(2i)^2$、$i\in F$) |
| (ii) | $[u_7]_7\in F^\times/F^{\times7}$ | **非自明** |
| (iii) | $u_7$ | $\mathbf{-4}\in\mathbf Q^\times$ |
| (iv) | **全付値** | $p=2$: $e=2,\ f=3,\ g=2$、**$w_\mathfrak p(u_7)=4$**(2 素点とも)。**他の全ての素点で $0$**。$\exists\mathfrak p:\ w_\mathfrak p\not\equiv0\ (\mathrm{mod}\ 7)$ ✓ |
| (v) | $[\gamma],[\delta_0]$ | 正規形座標で $\gamma=\delta_0=1$、$[\gamma]_2$ 自明 |
| (vi) | $\mathrm{ord}(a_7)$ | $\mathbf 7$ |

**$\mathrm{ord}([u_7]_{14})=7$ の根拠(機械)**: $w_\mathfrak p(u_7)\cdot7=28\equiv0\ (\mathrm{mod}\ 14)$ かつ $-1=\zeta_{28}^{14}\in F^{\times14}$ ⟹ $u_7^{\,7}\in F^{\times14}$;他方 $4\not\equiv0\ (\mathrm{mod}\ 14)$ ⟹ 類は非自明。$7$ 素数ゆえ位数 $=7$。

### 判定則 P-10

$[u_7]_2$ 自明 $\wedge$ $u_7\notin F_7^{\times7}$ ⟹ **$\mathrm{ord}(a_7)=7$**。
**⚠ SURJ-K7-APPLY の gate G-1〜G-4 は本執行では評価していない**(cert `gates_G1_G4_not_evaluated_here = true`)。**「$\mathrm{Ih}_{K^{(7)}}$ 全射」はここでは主張しない** — それは gate 通過を条件とする下流の裁定事項である。

### LB-RES 三段

| 段 | 必要か |
|---|---|
| 第 1 段(付値) | **これで決着**($w_\mathfrak p=4\not\equiv0\bmod7$・補題 G7-LB″) |
| 第 2 段($\mathrm{Cl}(F_7)[7]$) | **不要** |
| 第 3 段(単数群) | **不要** |

さらに $u_7=-4\in\mathbf Q^\times\setminus\mathbf Q^{\times7}$ ⟹ **補題 G7-LB(有理性版)でも即決**。⟹ **【文献要請 G7-3】($\mathbf Q(\zeta_{28})$ の類数・単数)は本線では不要になった**(補題 TW-5 の $F(S,2)$ 用途も、値が出た以上は不要)。**優先度を下げてよい。**

### NULL 枠

**N-1〜N-10 は 1 つも発動していない**(`any_triggered = false`)。とくに **N-5(予想 S4-c の反証)は起きず** — $u_7$ は有理数で、先例 3 件($K^{(3)}$・$A_5$・S4)と同じパターンに乗った。

---

## 5. ★ 族への外挿(**candidate・本執行の射程外**)

§2.3 の式 $u_n=4(-1)^\alpha$ は $n$ に依存しない。$\gcd(\alpha,n)=1$・$n$ 奇の窓で、$F_n=\mathbf Q(\zeta_{4n})$ において $e(\mathfrak p\mid2)=\varphi(4)=2$ ゆえ $w_\mathfrak p(u_n)=4$、したがって

$$4k\equiv0\ (\mathrm{mod}\ 2n)\iff k\equiv0\ (\mathrm{mod}\ n)\quad(n\ \text{奇})\qquad\Longrightarrow\qquad \mathrm{ord}\bigl([u_n]_{2n}\bigr)=n .$$

機械は $n=3,7,9,11,13$ の全単元 $\alpha$ で $u_n=\pm4$ を返した($n=9,\alpha=3$ は $d=\gcd=3$ で**窓の型が違う**ため射程外・除外)。$n=3$ は既知の定理 K3 と一致。

> ### ⚠ 格の申告
> これは **candidate** であり定理ではない。理由: (i) 定理 TOWER-n / KUM-n は**紙上・単系統・Sol 監査前**、(ii) 補題 TW-1 は本セッションの新規、(iii) 各 $n$ で (W1)–(W5)+(CAL) と (TB1)–(TB4) を確認していない、(iv) 下流 gate 未評価。
> **ただし「$n=3$ で既知値・既知位数を再現した」という事実は、族の式の強い状況証拠である。** 本執行の委嘱は $n=7$ なので、族の主張は**次の委嘱の標的**として置く(P1 dihedral 本峰に直撃する可能性がある — 司令塔の裁定事項)。

---

## 6. 検算・出所

| probe | SHA-256 | 役割 |
|---|---|---|
| `search/probe/wac_v1/tw_blocks.py` | `4c84fef8500f13156e59da4de15df2ee1014e9400a77f6d313614d298f23e2c7` | 窓・ブロック系・$N_G(H)=H$ |
| `search/probe/wac_v1/tw_orient.py` | `a160b58d0b4b6ac2c0f910b23983acc75e7566d9706334b7d67f72e26af4ea23` | 向き剛性(TW-6) |
| `search/probe/wac_v1/u7_fire_pathA.py` | `09f3d12d1ce5b83c06d0ebf3e66138974005909fe58c4ac54348795b16a89dc3` | **経路 A**(Q(i) 上の厳密演算) |
| `search/probe/wac_v1/u7_fire_pathB.py` | `f45b8db361b03706d9e8b6d74fb1e8b733a48cbc525fe581604deb9db4ae7b08` | **経路 B** + $F$-算術 |
| `search/probe/wac_v1/u7_fire_cert.py` | `25b4ee3de43af2815de4bb2dec840594798a984c2ca8e62438f53e36c3091194` | cert 生成 |
| `search/certs/u7_fire_20260801.json` | `02d2ee592a596b91629610a79d69f0947094797543394e55ccd2190eef67074b` | **証明書** |

**演算**: `fractions.Fraction` 上の $\mathbf Q(i)$ 厳密演算 + 整数群演算。**浮動小数点は一切使用していない。** $n=5$ 非接触(【凍結 U7-NO5】)。

---

## 7. 依存と限界(隠さず全部)

| # | 依存 | 格 |
|---|---|---|
| D-1 | (TB1)(TB2)(TB3)(TB4) | **枠組み仮定**(Mathlib 待ち・裁可済み方針) |
| D-2 | (W1)(W2)(W3)(W4)(W5) + (CAL) | 定理 B-4 / 系 B-4c / 補題 B-5 の前件 |
| D-3 | **定理 TOWER-n・定理 KUM-n・系 SPLIT** | **紙上・単系統・Sol 監査前**(← 最も弱い環) |
| D-4 | **補題 TW-1**(形式一意性) | 本セッション新規・機械確認つき・Sol 監査前 |
| D-5 | (W2)-fam(裁定 120) | **candidate** — **経路 B の (b) 位数論証のみが依存**。(a) 構造論証は非依存 |
| D-6 | $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X^2\rangle)$ | Sol 便 73 + w2fam §3.5(独立再確認済) — **経路 B の (a) のみが依存** |
| D-7 | SURJ-K7-APPLY gate G-1〜G-4 | **未評価**(本執行の射程外) |

> ### 主張しないこと(明示)
> * 「$\mathrm{Ih}_{K^{(7)}}$ は全射」— **主張しない**(D-7)。
> * 「verified」— **主張しない**(Lean 未使用・実装単系統)。正しい札は **cross-checked**。
> * 「族 $\mathrm{ord}(a_n)=n$ は定理」— **主張しない**(§5 は candidate)。
> * 「$u_7$ は単数」— **主張しない**(全付値を報告した・C1′-h の S4 教訓遵守)。実際 $w_\mathfrak p(u_7)=4\ne0$ で**単数ではない**。

## 8. 次の一手

* **【F-a】第二系統の突合**: 実装係の GAP 再構成(ブロック安定化・$h(k)$ 記号)と本 cert の照合(**司令塔**)。一致で初めて実装レベルの cross-check が立つ。
* **【F-b】Sol 監査**: 最優先は **D-3**(TOWER-n / KUM-n / SPLIT)と **D-4**(TW-1)。次に §1 の橋(押し出し $p_*[a]_M=[a]_2$ の一行)。
* **【F-c】gate G-1〜G-4** の評価(C1′(7) 要件表 §5.3 の 9 項)。⟹ そこを通れば下流の裁定へ。
* **【F-d】族(§5)の格上げ**: $n$ 一般で (W1)–(W5) を確認し、TOWER-n/KUM-n を Sol 監査に通す。**P1 本峰への直撃路。**
* **【F-e】$[\delta_0]$ の明示**: 正規形では $\delta_0=1$ だが、cert には「正規形座標で」としか書いていない。凍結修正 v2 の P-7 差し替え後に $[\delta_0]$ を独立に記帳すること。
