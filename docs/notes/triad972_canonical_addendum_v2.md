# TRIAD-972 canonical addendum v2 — roof 等式と $F_2$ 分解

日付: 2026-08-13。v1 の体・次数・Kummer 記号を保ち、レビュー要求 I の load-bearing な一行を展開する。

## 1. 体と Kummer 次数

\[
K=\mathbf Q(\zeta_9),\quad
E=L_{9,\mathrm{Aff}}=K(\sqrt[9]{a_{\rm mod9}}),\quad
F=L_{S4}=K(\sqrt[9]{b_{\rm mod9}}),
\]

\[
L_{9,\mathrm{full}}=E(i),\qquad
d_9=[E:K],\qquad d_{S4}=[F:K].
\]

RES-INJ-9 の範囲では

\[
r=|\langle[a_{\rm mod9}]\rangle\cap\langle[b_{\rm mod9}]\rangle|
\]

を $\mathbf Q^\times/(\mathbf Q^\times)^9$ と $K^\times/(K^\times)^9$ のどちらで計算しても同じ整数として読む。法 18 の $a_{9,\rm mod18}$ とは別記号である。

Kummer 理論から

\[
[EF:K]=\frac{d_9d_{S4}}r.
\tag{1}
\]

また $[K:\mathbf Q]=6$, $[K(i):K]=2$ なので

\[
\boxed{
|A_{\rm arith}|=[L_{9,\mathrm{full}}F:\mathbf Q]
=\frac{12d_9d_{S4}}r.
}
\tag{2}
\]

係数 12 は $6\cdot2$ である。`12[L_{9,Aff}L_{S4}:K]` と書くと型が明瞭で、`L_{9,full}` を括弧内に置く場合の係数は 6 である。

## 2. 純商の完全直積

$P=\mathrm{PSL}(2,8)$ とし、$K^{(l)}\subset PB_3$, $N_{S4}\subset PB_3$ は中心 $\langle c\rangle$ を含むとする。$G_l=PB_3/K^{(l)}$ は可解、$P=PB_3/N_{S4}$ は非可換単純である。従って二因子に共通する非自明商はなく、Goursat の補題から

\[
K^{(l)}N_{S4}=PB_3,
\]

\[
\boxed{
PB_3/(K^{(l)}\cap N_{S4})
\cong G_l\times P.
}
\tag{3}
\]

これは位数の一致だけでなく、二つの自然射から得る同型である。

## 3. 要求 I — $F_2$ 側の対応分解

正典の分解 $PB_3\cong F_2\times\langle c\rangle$ を使い

\[
K_l^F=K^{(l)}\cap F_2,qquad N^F=N_{S4}\cap F_2
\]

と置く。両 kernel は $c$ を含むので、式 (3) の中心因子を除いた対応物は

\[
\boxed{
F_2/(K_l^F\cap N^F)
\cong (F_2/K_l^F)\times(F_2/N^F).
}
\tag{4}
\]

である。式 (4) は $K_l^FN^F=F_2$、すなわち式 (3) と同じ「共通非自明商なし」の Chinese-remainder/Goursat 条件から従う。

## 4. roof が fibre product に等しい理由

$M_l=K^{(l)}\cap N_{S4}$ とする。$M_l$ の shadow を両因子へ reduce すると、同じ charming coordinate

\[
u=2m+1\in U=(\mathbf Z/18)^\times
\]

を持つ一対が得られる。逆に、同じ $u$ を持つ二つの factor shadow は式 (3) 上で componentwise な自己写像を定め、式 (4) によってその二つの $f$ 成分は一つの $F_2$ 商元に同時に持ち上がる。従って reduction は単射かつ全射で

\[
\boxed{
GT(M_l)
=GT(K^{(l)})\times_U GT(N_{S4}).
}
\tag{5}
\]

特に $l=9$ では

\[
|GT(M)|=\frac{108\cdot54}{6}=972.
\tag{6}
\]

式 (5) が既存の roof count を単なる模型同一視から等式へ上げる紙前件である。

## 5. 算術像と差集合

自然性から

\[
\ker\rho_M=\ker\rho_9\cap\ker\rho_{S4},
\qquad
A_{\rm arith}\cong\operatorname{Gal}(L_{9,\mathrm{full}}F/\mathbf Q).
\]

式 (2), (6) より

\[
\boxed{
|X_{\rm shadow}\setminus A_{\rm arith}|
=972-\frac{12d_9d_{S4}}r.
}
\tag{7}
\]

ただし式 (7) の A/B 解釈は別前件に依存する。本 addendum は roof 等式・体次数・記号の型を固定するもので、有限深度から B 型を認定しない。

## 6. 付随規約

- $s'=c_1s(1+O(s))$ なら法 18 で $u_9'=u_9c_1^{-18}$。法 9 の巡回部分群も不変である。
- $\zeta_{12}$ を用いる ambient は $F_9=\mathbf Q(\zeta_{36})$ と明記する。
- $\mathbf Q^\times/(\mathbf Q^\times)^{18}\cong\mathbf Z/2\oplus\bigoplus_p\mathbf Z/18$ では符号成分を残す。法 9 では $-1=(-1)^9$ なので消える。
- NAME-COLLIDE: E1-S3 / FAM-V2-S3 / P8-v3.2-S-3 を namespace 付きで区別する。
