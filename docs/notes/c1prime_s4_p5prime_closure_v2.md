# C1′(S4) + P5′ — quotient dessin / passport / local Kummer closure v2

日付: 2026-08-13。v1 を上書きせず、`c1p5_closure_review_v1.md` の要求 A–D, G を反映する再提出版とする。局所係数の数値 payload は読まず、`u/c` と封印 K5 は非接触である。

## 1. 比較図式と load-bearing な対象

\[
\begin{CD}
C_{\rm meas} @>{\iota_C}>> C_{\rm can}\\
@V{t_{\rm meas}}VV                 @VV{t_{\rm can}}V\\
\mathbf P^1_t @= \mathbf P^1_t\\
@A{\lambda^3-t\lambda^2+(t-3)\lambda+1=0}AA
@AA{\lambda^3-t\lambda^2+(t-3)\lambda+1=0}A\\
W_{\rm meas} @>{\iota_W}>> W_{\rm int}.
\end{CD}
\]

$\iota_W$ は $\iota_C$ の base change である。v2 では、7-cycle による monodromy の絞り込みより前に、測定側 $C$ の passport を §2 の三段論法で固定する。旧 `reconstruction_XYZ_exact` はその論証の代用品ではない。

## 2. 要求 A — 測定側 passport の固定

### 2.1 Shanks 分岐

\[
q(\lambda,t)=\lambda^3-t\lambda^2+(t-3)\lambda+1
\]

を $\lambda$ の三次式として取る。整数係数で判別式を展開すると

\[
\operatorname{disc}_{\lambda}(q)
=(t^2-3t+9)^2.
\]

従って Shanks 三次の有限分岐点は

\[
t^2-3t+9=0
\quad\Longleftrightarrow\quad
t=3\zeta_6^{\pm1}
\]

の二点 $\tau_1,\tau_2$ である。

### 2.2 uloc の構造欄

`u_meas_uloc_v2_20260731.json` は `measurement` key より前だけを streaming read した。`N_tau1,N_tau2` は両方とも

```text
degree = 9
deg_radical = 3
deg_gcd_with_derivative = 6
equals_kappa_g_cubed = true
```

である。従って各 $\tau_i$ 上の degree-9 fibre は三つの異なる根が各重複度 3 を持ち、分岐分割は

\[
(3,3,3)=3^3
\]

である。数値 local class はここで使っていない。

### 2.3 登録 W passport と Riemann–Hurwitz

登録済み $W$ passport は $((9),(9),(9))$ であり、normalized fibre product の局所指数は

\[
e_W=\frac{a}{\gcd(a,b)}.
\]

これにより $C$ の有限分岐台は $\{\tau_1,\tau_2,p\}$ に含まれ、$p$ 上は $(9)$、二つの $\tau$ 上は前項の $3^3$ である。degree 9 の Riemann–Hurwitz は

\[
2g(C)-2=-18+8+6+6=2,
\]

すなわち $g(C)=2$ を与える。従って測定側 passport は

\[
\boxed{(3^3,3^3,(9))}
\]

である。ここで Shanks の二分岐点と $C$ の位数 3 branch cycle の二点が同じ $\tau_1,\tau_2$ に束縛された。この binding が §3 の 7-cycle 論証の前件である。

### 2.4 旧 exact reconstruction の位置

`reconstruction_XYZ_exact` は producer 内で orbifold generator から $x,y,z$ を定義した後の自由群恒等式である。独立な dessin 情報は持たず、v2 では regression 欄にだけ残す。dessin の同定を担うのは、passport、monodromy、fixed-9-cycle incidence、対角 orbit の組である。

## 3. 要求 B–D, G — monodromy と定義体

### 3.1 既出部分と今回の増分

商 passport の 24 解、生成群位数の分布

\[
81:6,qquad324:9,qquad504:9,
\]

および位数 504 解の一 orbit は `u_meas_m1_passport_v1.md`【FINDING U-8】F-9/F-10（2026-07-31 凍結）に既出である。v1/v2 の増分は三 normalizer の悉皆と t-line の 7-cycle による強制であり、24 解等を新規とは数えない。

### 3.2 良い特殊化

良い特殊化 $t=t_0$ では、9 根への作用を保ったまま

\[
\operatorname{Gal}(f(x,t_0)/\mathbf Q)
\hookrightarrow
\operatorname{Gal}(f(x,t)/\mathbf Q(t))
\]

と読める。mod-$p$ factor degree は specialization group の cycle type を与えるため、generic group に同じ cycle type の元が存在する。cert の witness はすべて **t-line の組 $(p,t_0)$** であり、10 個の 7-cycle witness は存在証拠としてだけ使う。頻度推定には使わない。

### 3.3 幾何 monodromy

passport を §2 で固定した後の有限悉皆は

| $|G|$ | $|N_{S_9}(G)|$ | normalizer 内の $(7,1,1)$ |
|---:|---:|---|
| 81 | 324 | `false` |
| 324 | 1296 | `false` |
| 504 | 1512 | `true` |

である。$G_{\rm geom}\triangleleft G_{\rm arith}\le N_{S_9}(G_{\rm geom})$ と t-line の 7-cycle の存在から

\[
|G_{\rm geom}|=504,
\qquad G_{\rm geom}\cong\mathrm{PSL}(2,8)
\]

に絞られる。

### 3.4 要求 G の incidence

9 点作用の $P=\mathrm{PSL}(2,8)$ を全列挙すると、抽象的位数 9 の元は 168 個であり、その 168 個はすべて 9-cycle である。従って

\[
[S_9:N_{S_9}(P)]\cdot168
=240\cdot168
=40320
=8!
\]

である。$S_9$ は 9-cycles に推移的なので、固定 9-cycle を含む $S_9$-共役な $P$ は一つである。この incidence の前提「168 個すべてがこの作用で 9-cycle」を cert と checker が別実装で再計算した。

### 3.5 intrinsic $\mathbf Q$-model

$C_{\rm can}$ と intrinsic parameter $s_{\rm int}$ の $\mathbf Q$-model は `litgate_positive_genus_belyi_v1.md` §(I), **LEDGER 633** に pin する。「passport 内で剛」という語は裸の passport ではなく、**passport と monodromy $\mathrm{PSL}(2,8)$ の組**に対して読む。

位数 504 の商 dessin は一 orbit、$C_{S_9}(P)$ は自明である。両 cover と branch labels が $\mathbf Q$ 上にあるため一意な幾何同型は Galois 固定で、$\iota_C$ は $\mathbf Q$ 上定義される。

### 3.6 算術 monodromy（推奨欄 F）

structural Frobenius 欄には $3^2 1^3$ と $6\cdot2\cdot1$ の元が存在し、いずれも $P$ の cycle type ではない。従って $G_{\rm arith}\supsetneq P$。一方 $N_{S_9}(P)$ の位数は 1512 で商の位数は 3 だから

\[
G_{\rm arith}=\mathrm{P\Gamma L}(2,8),qquad |G_{\rm arith}|=1512.
\]

`outside_PGammaL_2_8` に標本が無かったことは上界として使っていない。

## 4. P5′

labelled base を保つ $\iota_W$ は、$\lambda=0$ 上の分岐指数 9 の一点 $P_0$ を保つ。§3.5 の $\mathbf Q$-model から $s_{\rm int}$ を取り、測定側の $s_{\rm meas}$ と比較すると

\[
s_{\rm meas}=\gamma s_{\rm int}(1+O(s_{\rm int})),\qquad \gamma\ne0.
\]

\[
\lambda=u_{S4}s_{\rm int}^9(1+O(s_{\rm int})),\qquad
\lambda=u_0s_{\rm meas}^9(1+O(s_{\rm meas}))
\]

より $u_0=u_{S4}\gamma^{-9}$。loop の向きを unit exponent $\varepsilon\in(\mathbf Z/9)^\times$ で変える規約も含め、必要な不変量は

\[
\boxed{
\left\langle[u_0^{-1}]_9\right\rangle
=\left\langle[u_{S4}^{-1}]_9\right\rangle .
}
\tag{P5'}
\]

である。代表元の厳密等号は主張しない。まず $K^\times/(K^\times)^9$, $K=\mathbf Q(\zeta_9)$ で比較し、rational class へ戻す箇所だけ RES-INJ-9 を使う。

## 5. theorem-candidate package の境界

以上により exact model と登録 marking の間の C1′(S4) dessin binding、および P5′ の巡回部分群比較を theorem-candidate package として再提出する。有限部分は producer/checker の一致、紙部分は上記の明示前件に依存し、Lean certificate は無い。

別前件 P1/P2、$(Z_{18}\text{-link})$、算術像の最終解釈は本書の射程外である。また SINGLE-BIT の具体化について

\[
K^{(l)}\cap N_{S4}\text{ 族では PH2-VOID により原理的に 324 へ落ちない。}
\]

従ってこの族による A/B の判定可能性は **UNKNOWN** であり、有限深度から B 型を認定しない。非分裂候補の別実験は `d972_phase2b_nonsplit_report_v1.md` に分離する。

## 6. 規約と再現

作用規約は左 $\operatorname{Ad}(g)(h)=ghg^{-1}$ を数学側の正本とする。旧 orbit index は実装依存なので意味を持たせず、`fixed_Z_orbit_count=6`, `diagonal_orbit_count=1`, `intrinsic_orbit_is_diagonal=true` を canonical record とする。

```powershell
python search/c1prime_s4_p5prime_v2.py --hard-timeout-seconds 900
python search/check_c1prime_s4_p5prime_v2.py
```

- `search/certs/c1prime_s4_p5prime_v2_20260813.json`
- `search/certs/c1prime_s4_p5prime_v2_check_20260813.json`
- `search/certs/c1prime_s4_p5prime_v2_checkpoint.json`

NAME-COLLIDE 回避: 本書の `C1′(S4)`, `P5′`, `PH2B-NS64-v1.1` は E1-S3 / FAM-V2-S3 / P8-v3.2-S-3 と別 namespace である。
