# C1′(S4) + P5′ — quotient dessin / pullback / local Kummer comparison v1

日付: 2026-08-13。対象は \(N_{S4}\) の degree-9 cover。局所係数の数値 payload は読まず、既存 cert は structural field と digest だけを用いた。

## 1. 一つの比較図式

測定模型と intrinsic 窓を別々に橋渡しせず、次の一図式で比較する。

\[
\begin{CD}
C_{\rm meas} @>{\iota_C}>> C_{\rm can}\\
@V{t_{\rm meas}}VV                 @VV{t_{\rm can}}V\\
\mathbf P^1_t @= \mathbf P^1_t\\
@A{\lambda^3-t\lambda^2+(t-3)\lambda+1=0}AA
@AA{\lambda^3-t\lambda^2+(t-3)\lambda+1=0}A\\
W_{\rm meas}=C_{\rm meas}\times_{\mathbf P^1_t}\mathbf P^1_\lambda
@>{\iota_W}>
W_{\rm int}=C_{\rm can}\times_{\mathbf P^1_t}\mathbf P^1_\lambda .
\end{CD}
\]

下段の \(\iota_W\) は上段 \(\iota_C\) の base change である。右下が intrinsic triple \((X,Y,Z)\) を復元することを有限群で示し、その同じ \(\iota_W\) の完備局所環上の作用で P5′ を得る。

## 2. 測定で閉じた部分

### 2.1 intrinsic triple

\(\mathbf F_8=\mathbf F_2[x]/(x^3+x+1)\) と既登録の二行列 \(S,T\) から 9 点作用を再構成した。得られた \(P=\langle X,Y\rangle\) について

\[
|P|=504,\quad \operatorname{ord}(X)=\operatorname{ord}(Y)=\operatorname{ord}(Z)=9,\quad XYZ=1.
\]

位数 9 の元は 168 個、\(Z\) の \(P\)-共役類は 56 元であり、\(X,Y,Z\) は同じ類に属した。従って intrinsic dessin は対角類である。

### 2.2 商模型の幾何 monodromy

商 passport \((3^3,3^3,(9))\) で第 3 branch cycle を固定し、全解を悉皆した。

| 生成群位数 | 解数 |
|---:|---:|
| 81 | 6 |
| 324 | 9 |
| 504 | 9 |

各生成群 \(G\) の \(S_9\)-normalizer も全 \(9!\) 置換を走査して得た。

| \(|G|\) | \(|N_{S_9}(G)|\) | normalizer に型 \((7,1,1)\) |
|---:|---:|---|
| 81 | 324 | false |
| 324 | 1296 | false |
| 504 | 1512 | true |

既存の exact model gate は good reduction の factorization から型 \((7,1,1)\) の Frobenius witness を持つ。これは標本頻度から群を推測する使用ではなく、算術 monodromy に位数 7 の元が一つ存在するという有限証拠としてのみ使う。幾何 monodromy \(G_{\rm geom}\) は算術 monodromy の正規部分群で、算術側は \(N_{S_9}(G_{\rm geom})\) に入る。上の悉皆表により位数 81 と 324 は除かれ、

\[
|G_{\rm geom}|=504
\]

に強制される。これで有限 Frobenius 標本だけから幾何群を同定する旧い穴を使わない。

位数 504 の 9 解は \(C_{S_9}(C)=\langle C\rangle\) の一 orbit である。従ってこの passport と幾何群を持つ商 dessin は一つである。また \(C_{S_9}(P)\) の位数は 1 なので、\(C_{\rm meas}\) と canonical quotient の幾何学的同型は一意である。両 cover と branch labels は \(\mathbf Q\) 上にあり、一意な同型は Galois 固定、従って \(\iota_C\) は \(\mathbf Q\) 上定義される。

### 2.3 quotient から 6 dessins を分離する

orbifold generators を \(A_{\rm orb},B_{\rm orb}\) とすると、Shanks 三次の kernel の標準生成元は

\[
x=(B_{\rm orb}A_{\rm orb})^{-1},\qquad
y=(A_{\rm orb}B_{\rm orb})^{-1},\qquad z=(xy)^{-1}.
\]

canonical quotient triple にこの語を代入すると、置換として

\[
(x,y,z)=(X,Y,Z)
\]

が三成分とも厳密に一致した。

固定した 9-cycle \(Z\) を含む \(S_9\)-共役な \(P\) は一つしかない。実際

\[
[S_9:N_{S_9}(P)]\cdot\#\{g\in P:\operatorname{ord}(g)=9\}
=240\cdot168=40320,
\]

右辺は \(S_9\) の 9-cycles の総数 \(8!=40320\) であり、共役推移性から incidence はちょうど 1 である。その唯一の \(P\) 内で \(XY=Z^{-1}\) を全数走査すると 54 解、\(\langle Z\rangle\)-orbit は各 9 元の 6 個となった。6 orbit のうち \(X,Y,Z\) が同じ \(P\)-共役類に入るものはちょうど 1 個で、上の再構成 orbit がそれであった。

以上により、測定模型の quotient dessin、固定 Shanks base change、intrinsic な唯一の対角 \(W\)-dessin が同じ図式に束縛される。これが C1′(S4) の dessin binding である。

## 3. P5′ の紙部分

\(P_0\) は degree-9 passport の \(\lambda=0\) 上の唯一の点で、分岐指数 9 である。labelled base を保つ \(\iota_W\) は \(P_0\) を保つ。intrinsic 側と測定側の \(\mathbf Q\)-有理 local parameter をそれぞれ \(s_{\rm int},s_{\rm meas}\) とすると、完備局所環の同型から一意な \(\gamma\neq0\) があり

\[
s_{\rm meas}=\gamma s_{\rm int}(1+O(s_{\rm int})).
\]

定義を

\[
\lambda=u_{S4}s_{\rm int}^{9}(1+O(s_{\rm int})),\qquad
\lambda=u_0s_{\rm meas}^{9}(1+O(s_{\rm meas}))
\]

と書けば

\[
u_0=u_{S4}\gamma^{-9},\qquad
[u_0^{-1}]_9=[u_{S4}^{-1}]_9
\]

となる。標準 loop の向きを unit exponent \(\varepsilon\in(\mathbf Z/9)^\times\) で取り替える規約まで許す場合も

\[
[u_0^{-1}]_9=[u_{S4}^{-1}]_9^{\,\varepsilon}
\]

であり、必要な最小命題は変わらない。

\[
\boxed{
\left\langle [u_0^{-1}]_9\right\rangle
=\left\langle [u_{S4}^{-1}]_9\right\rangle .
}
\tag{P5'}
\]

まず \(K^\times/(K^\times)^9\), \(K=\mathbf Q(\zeta_9)\) で得られ、両類を rational class として読む箇所では RES-INJ-9 により \(\mathbf Q^\times/(\mathbf Q^\times)^9\) へ戻せる。代表元の厳密等号は主張せず、uniformizer と向きに不変な巡回部分群だけを固定する。

## 4. 測定部分と紙部分の境界

| 部分 | 根拠 |
|---|---|
| \(P\), intrinsic \(XYZ\), order-9 class | producer + helper 非共有 checker の全数計算 |
| quotient 24 解、\(81/324/504\) 分布 | 同上 |
| 三 normalizer と 7-cycle 可否 | 全 \(S_9\) 走査を二実装で再計算 |
| 位数 504 の quotient が 1 orbit | 同上 |
| fixed-\(Z\) の 54 解 / 6 dessins / 対角 1 | 同上 |
| kernel words から \(XYZ\) の厳密復元 | 同上 |
| model の exact structural gate と 7-cycle witness | 既存 cert の structural fields。局所数値 payload は未読 |
| \(G_{\rm arith}\le N_{S_9}(G_{\rm geom})\) と幾何群の強制 | 紙 |
| trivial centralizer から \(\mathbf Q\)-同型 | 紙 + centralizer の有限計算 |
| base change の関手性、局所 parameter 比較、(P5′) | 紙 |

C1′/P5′ はこの exact model と既登録 marking の比較リンクを閉じる。別の前件 P1/P2、\((Z_{18}\text{-link})\)、算術像の解釈は本票の射程外であり、それらの状態を変更しない。

## 5. 再現と証明書

    python search/c1prime_s4_p5prime_v1.py --hard-timeout-seconds 900
    python search/check_c1prime_s4_p5prime_v1.py

producer は stage ごとに search/certs/c1prime_s4_p5prime_v1_checkpoint.json を原子的に更新し、watchdog timeout 時も同じ path に停止 stage を残す。

- search/certs/c1prime_s4_p5prime_v1_20260813.json
- search/certs/c1prime_s4_p5prime_v1_check_20260813.json
- search/certs/c1prime_s4_p5prime_v1_checkpoint.json

両 cert は \(u/c\) の数値欄を出力せず、numeric_local_class_read=false, u_touched=false, c_touched=false を記録する。
