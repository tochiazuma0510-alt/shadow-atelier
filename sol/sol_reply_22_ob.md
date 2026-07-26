# 影工房 便 22 返信 — class 6 の ob 定義批准

## 定義の一意な言明

**結論は (B)。ただし「別の正準射影」とは部分加群への Reynolds 射影ではなく、次の商への射影である。(A) は誤り、(C) も誤り。便 19 F10 の (10.1)(10.2) は本便で訂正する。**

\[
R:=\mathbb Z/2^e,\qquad e=j-1\ge1,\qquad
\mathcal N:=1+\sigma+\sigma^2,\qquad
P_\sigma:=3^{-1}\mathcal N,\qquad
K:=\ker\mathcal N .
\]
class-6 中心
\[
C=R\langle t_5,t_6,u_1,u_2,u_3,u_4\rangle
\]
について、正準障害群と正準障害元を
\[
\boxed{\quad
\mathcal O_{6,e}:=
C^\theta/(1+\theta)K,\qquad
\operatorname{ob}_{6,e}(\bar f):=
\left[
q_\theta(\bar f)-3^{-1}(1+\theta)q_N(\bar f)
\right]_{\mathcal O_{6,e}}
\quad}
\tag{0.1}
\]
と定義する。

class-6 の確定表から
\[
(1+\theta)K=(1+\theta)C
\tag{0.2}
\]
が従うので
\[
\mathcal O_{6,e}
=\widehat H^0(\langle\theta\rangle,C)
\cong R[2]\,a\oplus(R/2R)\,\bar b,
\qquad
a:=u_4,\quad b:=u_1+u_2+u_3,
\tag{0.3}
\]
かつ
\[
\boxed{\quad
\operatorname{ob}_{6,e}(\bar f)
=[q_\theta(\bar f)].
\quad}
\tag{0.4}
\]
すなわち、正しい商では \(q_N\) 項は零になる。

より具体的に、\(q_\theta\in C^\theta\) を一意に
\[
q_\theta
=x(t_5+t_6)+y(u_1+u_3)+z\,u_2+d\,u_4,
\qquad 2d=0
\tag{0.5}
\]
と書けば、
\[
\boxed{\quad
(q_\theta)_+
:=\rho_{6,e}(q_\theta)
=d\,a+(z\bmod2)\,\bar b
\in R[2]a\oplus(R/2R)\bar b .
\quad}
\tag{0.6}
\]
これが `(q_theta)+` の一意な意味である。

manifest の最小 gate \(j=2\), \(R=\mathbb F_2\) では
\[
\boxed{
\operatorname{ob}_a=(q_\theta)_{u_4},\qquad
\operatorname{ob}_b=(q_\theta)_{u_2}
}
\tag{0.7}
\]
である。この場合だけ \(\bar b=b\) と同一視でき、target は
\(\mathbb F_2a\oplus\mathbb F_2b\) になる。

---

## F1. 中央補正問題を型付きで書く

\(\bar f\) を線型段の解、\(g=s(\bar f)\) を任意の lift とし、加法記法の中心欠損を
\[
q_\theta=\theta(g)g\in C^\theta,\qquad
q_N=E_m\sigma^2(g)\sigma(g)g\in C^\sigma
\]
とする。前者・後者の所属は便 19 F2 の中央欠損補題で無条件に従う。

中心補正 \(z\in C\) によって \(g_z=gz\) と取り替えると
\[
\begin{aligned}
q_\theta(g_z)&=q_\theta(g)+(1+\theta)z,\\
q_N(g_z)&=q_N(g)+\mathcal Nz .
\end{aligned}
\tag{1.1}
\]
従って二つの群方程式を同時に満たす条件は
\[
(1+\theta)z=-q_\theta,\qquad
\mathcal Nz=-q_N.
\tag{1.2}
\]

\(3\in R^\times\) かつ \(\sigma^3=1\) on \(C\) なので
\[
P_\sigma=3^{-1}\mathcal N
\]
は \(C\to C^\sigma\) の Reynolds 射影であり、
\(\mathcal N:C\to C^\sigma\) は全射である。しかし、重要なのは

\[
\boxed{P_\sigma\theta\ne\theta P_\sigma\quad\text{on the full class-6 center}}
\tag{1.3}
\]

である。従って \(P_\sigma q_\theta\) をそのまま
\((C^\sigma)^\theta\) の元と読むことはできない。

## F2. class-6 確定表から \(\mathcal N\) を直接読む

確定表 `crosscheck/agree6_*.json` の中心六基底上の作用を用いる。
\[
z=\xi_5t_5+\xi_6t_6+\eta_1u_1+\eta_2u_2+\eta_3u_3+\eta_4u_4
\]
と書くと、直接和を取って
\[
\boxed{
\mathcal Nz=B_m(z)b+A_m(z)a
}
\tag{2.1}
\]
ただし
\[
\begin{aligned}
B_m(z)
&=(m+2)\xi_5+(1-m)\xi_6
  +2\eta_1-\eta_2+2\eta_3,\\
A_m(z)
&=(m-1)\xi_5+(m+2)\xi_6+3\eta_4.
\end{aligned}
\tag{2.2}
\]
従って
\[
C^\sigma=Ra\oplus Rb
\tag{2.3}
\]
は正しい。ただし、これはまだ障害群ではない。

\(\theta\) の作用は厳密に
\[
t_5\leftrightarrow t_6,\qquad
u_1\leftrightarrow u_3,\qquad
\theta(u_2)=u_2,\qquad
\theta(u_4)=-u_4.
\tag{2.4}
\]
ゆえに
\[
C^\theta
=R(t_5+t_6)\oplus R(u_1+u_3)\oplus Ru_2\oplus R[2]u_4.
\tag{2.5}
\]

## F3. \((1+\theta)\ker\mathcal N\) の決定

\(z\in K=\ker\mathcal N\) である条件は (2.2) から
\[
\begin{aligned}
\eta_2&=(m+2)\xi_5+(1-m)\xi_6+2\eta_1+2\eta_3,\\
\eta_4&=-3^{-1}\bigl((m-1)\xi_5+(m+2)\xi_6\bigr).
\end{aligned}
\tag{3.1}
\]
一方
\[
(1+\theta)z
=(\xi_5+\xi_6)(t_5+t_6)
(\eta_1+\eta_3)(u_1+u_3)
2\eta_2u_2.
\tag{3.2}
\]

\(2m+1\) は \(R\) の単元である。従って
\(\xi_5+\xi_6\) と \(\eta_1+\eta_3\) を固定しても、(3.1) の
\(\eta_2\) は任意の \(R\) の値を走る。よって
\[
\begin{aligned}
(1+\theta)K
&=R(t_5+t_6)\oplus R(u_1+u_3)\oplus2Ru_2\\
&=(1+\theta)C.
\end{aligned}
\tag{3.3}
\]
これが (0.2) の証明である。

従って
\[
\begin{aligned}
\mathcal O_{6,e}
&=C^\theta/(1+\theta)K\\
&\cong (R/2R)[u_2]\oplus R[2][u_4]\\
&\cong (R/2R)\bar b\oplus R[2]a.
\end{aligned}
\tag{3.4}
\]
特に
\[
\boxed{|\mathcal O_{6,e}|=4\quad\text{for every }e\ge1.}
\tag{3.5}
\]
便 19 (10.1) の
\(\mathbb Z/2\oplus\mathbb Z/2^e\) は \(e=1\) では偶然一致するが、
\(e\ge2\) では過大である。\(b\)-方向も高々一ビットである。

## F4. ob 式の証明 — 必要性

\(\bar f\) が中心まで持ち上がるとし、(1.2) を満たす \(z\) を取る。
\(\mathcal Nz=-q_N\) より
\[
P_\sigma z=-3^{-1}q_N.
\]
従って
\[
k:=z+3^{-1}q_N\in K.
\]
第一式へ代入すると
\[
0=q_\theta+(1+\theta)z
=q_\theta-3^{-1}(1+\theta)q_N+(1+\theta)k.
\]
ゆえに (0.1) の商で
\[
\operatorname{ob}_{6,e}(\bar f)=0.
\]
これは必要性である。

## F5. ob 式の証明 — 十分性

逆に
\[
\operatorname{ob}_{6,e}(\bar f)=0
\]
とする。定義により、ある \(k\in K\) が存在して
\[
q_\theta-3^{-1}(1+\theta)q_N=-(1+\theta)k.
\tag{5.1}
\]
そこで
\[
z:=-3^{-1}q_N+k
\tag{5.2}
\]
と置く。\(q_N\in C^\sigma\) だから
\[
\mathcal Nz
=-3^{-1}\mathcal N q_N+\mathcal Nk
=-q_N.
\]
また (5.1) から
\[
q_\theta+(1+\theta)z=0.
\]
従って \(gz\) は二つの群方程式を同時に満たす。よって固定した
\(\bar f\in\mathcal L_m\) について
\[
\boxed{
\bar f\text{ が full class-6 解へ持ち上がる}
\iff
\operatorname{ob}_{6,e}(\bar f)=0.
}
\tag{5.3}
\]

全体の可解性は
\[
\boxed{
\mathcal S_m\cap\mathcal B_\theta\ne\varnothing
\iff
\exists\bar f\in\mathcal L_m:
\operatorname{ob}_{6,e}(\bar f)=0.
}
\tag{5.4}
\]
である。任意に選んだ一個の線型 witness で ob が非零でも、
他の \(\bar f\) で零になる可能性を排除していない。negative certificate
には \(\mathcal L_m\) 全体の悉皆または同値な零点不存在証明が必要である。

## F6. lift・section からの独立性

初期 lift を \(g\mapsto gc\), \(c\in C\) と替えると
\[
(q_\theta,q_N)
\mapsto
\bigl(q_\theta+(1+\theta)c,\ q_N+\mathcal Nc\bigr).
\]
(0.1) の代表元の変化は
\[
\begin{aligned}
&(1+\theta)c
-3^{-1}(1+\theta)\mathcal Nc\\
&\qquad=(1+\theta)(c-P_\sigma c).
\end{aligned}
\tag{6.1}
\]
しかも
\[
\mathcal N(c-P_\sigma c)=0,
\]
すなわち \(c-P_\sigma c\in K\)。従って (6.1) は
\((1+\theta)K\) に入り、ob の類は変わらない。

これが、未定義だった `+` を単なる座標読取りで済ませてはならない
理由である。

## F7. class 6 では \(q_N\) 項が商で消える

(3.3) により
\[
3^{-1}(1+\theta)q_N\in(1+\theta)C=(1+\theta)K.
\]
従って (0.1) は
\[
\operatorname{ob}_{6,e}=[q_\theta]
\]
へ簡約する。これは \(q_N\) 方程式を無視したという意味ではない。

- \(\mathcal N:C\to C^\sigma\) は全射なので norm 欠損自体は必ず補正できる。
- その補正が \(\theta\) 方程式へ与える変化は、class-6 表では
  \((1+\theta)K\) に吸収できる。
- 残る obstruction は \(\theta\)-Tate class の二ビットだけである。

従って F10 の「\(q_N\) が \(b\)-方向の \(2^e\) 障害を残す」という読みは
撤回する。

## F8. (A) の明示反例と分岐検出 fixture

確定表から
\[
\begin{aligned}
\mathcal Nt_5&=(m+2)b+(m-1)a,\\
\mathcal N(t_5+t_6)&=3b+(2m+1)a.
\end{aligned}
\tag{8.1}
\]

### 必須 fixture: lift-gauge invariance

欠損対 \((q_\theta,q_N)=(0,0)\) から始め、同じ \(\bar f\) の lift を
\(g\mapsto gt_5\) と替える。新しい欠損対は
\[
q_\theta'=t_5+t_6,\qquad
q_N'=\mathcal Nt_5.
\tag{8.2}
\]
これは同じ持ち上げ問題の別表示だから、ob は両方で零でなければならない。

正しい定義では
\[
q_\theta'-3^{-1}(1+\theta)q_N'
=(1+\theta)(t_5-P_\sigma t_5)\in(1+\theta)K,
\]
よって確かに ob \(=0\)。

一方、(A) を採用し \(j=2\), \(R=\mathbb F_2\) で
\(P_\sigma q_\theta'\) を読むと
\[
P_\sigma(t_5+t_6)=a+b.
\]
しかも \((1+\theta)q_N'=0\) on
\(\mathbb F_2a\oplus\mathbb F_2b\) なので、(A) は
\[
\operatorname{ob}^{(A)}=a+b\ne0
\]
を返す。すなわち **(A) は lift の取り替えで判定を反転させる**。

\(e\ge2\) ではさらに
\[
P_\sigma(t_5+t_6)
=b+\frac{2m+1}{3}a
\]
の \(a\)-係数が \(2\)-torsion でないため、
\((C^\sigma)^\theta\) にすら入らない。

### 二本の nonzero-control

\(j=2\), \(q_N=0\) で次も fixture に入れる。

- \(q_\theta=u_4\): \((\operatorname{ob}_a,\operatorname{ob}_b)=(1,0)\)。
- \(q_\theta=u_2\): \((\operatorname{ob}_a,\operatorname{ob}_b)=(0,1)\)。

\((1+\theta)C\) は \(u_4\) 成分を持たず、mod \(2\) では \(u_2\)
成分も持たないため、どちらも真に補正不能である。

この三 fixture は

1. boundary を nonzero と誤る実装、
2. \(a\)-bit を落とす実装、
3. \(b\)-bit を落とす実装

を別々に検出する。

## F9. (C) も成立しない

\(q_\theta'=t_5+t_6\) は \(\theta\)-固定だが、一般に
\(\sigma\)-固定ではない。しかも F8 のとおり、これは抽象的な
test vector ではなく、実際の欠損を central lift \(t_5\) で
取り替えたときに生じる。

従って
\[
q_\theta\in C^\theta
\quad\not\Rightarrow\quad
q_\theta\in C^\sigma
\]
であり、(C) は棄却される。

## F10. mass check の批准

「解の重複度総和 \(=\prod_i n_i\)」は **条件付きで正しい**。
\(n_i\) が、線型解空間 \(\mathcal L_m\) の独立な invariant-factor
parameter の実際の位数（自由変数の modulus も含む）として
定義され、
\[
\prod_i n_i=|\ker L_m|
\]
となっている場合に限る。ここで \(L_m\) は二つの線型段方程式を
まとめた準同型であり、可解なら
\[
\mathcal L_m\text{ は }\ker L_m\text{ の affine torsor}
\]
なので
\[
\sum_{\text{列挙 branch}}\operatorname{multiplicity}
=|\mathcal L_m|
=|\ker L_m|.
\tag{10.1}
\]

一つの modulus \(n\) 上の Smith diagonal が
\(d_1,\dots,d_r\) で、domain rank が \(D\) なら、可解時の正確な値は
\[
\boxed{
|\mathcal L_m|
=n^{D-r}\prod_{i=1}^r\gcd(d_i,n).
}
\tag{10.2}
\]
従って `Π n_i` に free-variable factor や各
\(\gcd(d_i,n)\) が入っていなければ不可。

さらに full class-6 解の mass は線型段だけの mass ではない。
\[
\Lambda:C\to C^\theta\oplus C^\sigma,\qquad
\Lambda(z)=((1+\theta)z,\mathcal Nz)
\]
とすると、(2.2)(2.4) から
\[
\ker\Lambda
\cong R\oplus R[2],\qquad
|\ker\Lambda|=2|R|=2^{e+1}.
\tag{10.3}
\]
実際、\(\ker\Lambda\) は
\[
\xi_6=-\xi_5,\quad
\eta_3=-\eta_1,\quad
\eta_2=(2m+1)\xi_5,\quad
\eta_4=\xi_5,\quad
2\xi_5=0
\]
で、\(\eta_1\in R\) と \(\xi_5\in R[2]\) が自由である。

従って一系 \(m\) の full-solution mass は
\[
\boxed{
M_m
=2^{e+1}\,
\#\{\bar f\in\mathcal L_m:
\operatorname{ob}_{6,e}(\bar f)=0\}.
}
\tag{10.4}
\]
\(j=2\) では各 ob-zero linear solution に中心 lift がちょうど
\(4\) 個ある。

mass fixture の PASS 条件は次の三項を全て要求する。

1. 線型 branch の multiplicity 総和が (10.2) と一致。
2. 各 branch について ob の二ビットを評価し、ob-zero mass と
   ob-nonzero mass の和が線型 mass と一致。
3. ob-zero branch の full lift 数が一律 (10.3) 倍であり、
   全体が (10.4) と一致。

単に certificate が 64 個ある、あるいは一系一 witness の ob を読むだけでは
mass check にならない。

## F11. manifest への具体的修正要求

1. 判定量を
   \[
   \operatorname{ob}_{6,e}
   =[q_\theta-3^{-1}(1+\theta)q_N]
   \in C^\theta/(1+\theta)\ker\mathcal N
   \]
   に置換する。
2. class 6 では target を
   \[
   R[2]a\oplus(R/2R)\bar b
   \]
   とする。\(Rb\) ではない。
3. \(j=2\) 実装は (0.7)、すなわち生の
   `q_theta[u4]`, `q_theta[u2]` の二ビットを読む。
4. F8 の gauge-invariance fixture と二本の nonzero-control を
   発射条件へ追加する。
5. negative certificate は一個の linear witness でなく、
   全 linear mass に ob-zero がないことを証明する。
6. mass check を F10(10.1)–(10.4) の意味で定義する。

最小 gate \(j=2\) 自体は維持できる。ただし全零でも高い \(j\) は閉じない。
特に \(R[2]a\) の非零元 \(2^{e-1}a\) は下位 modulus への reduction で
零になり得るので、manifest 既定どおり次の \(j\) は別便で撃つ必要がある。

## F12. 状態札

| 主張 | 判定 |
|---|---|
| falsifier §1 の重大指摘 | **全面受理** |
| 選択 (A) \(P_\sigma q_\theta\) | **棄却**。非 \(\theta\)-同変・lift 非不変 |
| 選択 (B) 商射影 \(\rho_{6,e}\) | **採用・紙上証明** |
| 選択 (C) \(q_\theta\in C^\sigma\) | **棄却** |
| 固定 \(\bar f\) の lift 可解性 iff ob \(=0\) | **両向き紙上証明** |
| class-6 obstacle group | \((\mathbb Z/2)^2\)（全 \(e\ge1\)） |
| 便 19 (10.1)(10.2) | **本便で erratum**。過去返信は記録として未編集 |
| class-6 作用表 | 開示どおり二独立導出一致を採用 |
| 本 ob 導出 | **Sol 紙上単系統**。並列答案との突合前 |
| Lean verified | なし |

## ★ 教材

> **平均化射影は、もう一つの対称性と可換するとは限らない。**  
> \(3^{-1}(1+\sigma+\sigma^2)\) が \(C^\sigma\) への正しい射影でも、
> \(\theta\) がその射影を保つとは限らない。今回の weight-5 から
> weight-6 への上三角拡大がまさにその反例であり、射影値を
> \((C^\sigma)^\theta\) と読むと lift-gauge invariance が壊れた。
>
> simultaneous lifting の正本は「代表元の成分」ではなく
> \[
> [q_\theta-3^{-1}(1+\theta)q_N]
> \in C^\theta/(1+\theta)\ker\mathcal N
> \]
> である。座標縮約は、この商を計算した**後**にだけ行う。

---

## 監査範囲外申告

- 禁止された `docs/委嘱16*` および `ops/express/` の当該スレッドは読んでいない。並列 Opus 答案は不可視のままである。
- GAP・node・Python・Lean は実行していない。`agree6_sol2.json` と `agree6_claude.json` は確定表として静的に読み、作用表の再導出・1147 検査の再実行はしていない。
- \(m=0,\dots,63\) の本掃引、fixture 実装、certificate 生成はしていない。
- 有限許容 \(PB_3/N\) への実現性・charming 性、従って E15 の反例認定は本便の範囲外である。
- 過去返信ファイルおよび manifest は編集していない。本便で変更したのは `sol/sol_reply_22_ob.md` のみである。
