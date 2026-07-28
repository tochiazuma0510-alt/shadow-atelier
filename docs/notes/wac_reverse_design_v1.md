# WA-c 逆設計 v1(裁定 161 委嘱・絞り込み版)

状態: candidate(起草中)
起草: 影工房 数学者(Claude)/ 2026-07-25
前提: `docs/notes/wall_design_audit_v1.md` §7(Hol 篩・命題 7.1 / 系 7.2・A₁₃ 実現可能性)

---

## 0. 目的と範囲

【WA-c】= 監査 §8.2 の未閉鎖項:「§7.3 の $A_{13}$ を $B_3$-窓へ持ち上げる」。
本稿は **2 候補に絞った逆設計**。悉皆探索はしない。$u$(封印記号)は一切現れない。

---

## 0.5 【新規・本稿の鍵】逆設計問題の完全な言い換え

監査 §7.3 は持ち上げを UNKNOWN としたが、$c\in N$ 窓に限れば問題は**完全に初等化する**。

> ### 補題 0.1($c\in N$ 窓 = モジュラー群の有限商)
> $B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle$ において
> $a:=\sigma_1\sigma_2\sigma_1$、$b:=\sigma_1\sigma_2$ とおくと $B_3=\langle a,b\mid a^2=b^3\rangle$、$a^2=b^3=c$(中心)。
> 逆に $\sigma_1=b^{-1}a$、$\sigma_2=a^{-1}b^2$。
> ゆえに **$c\in N$ なる窓 $E=B_3/N$ は、$\Gamma:=B_3/\langle c\rangle=\mathrm{PSL}_2(\mathbf Z)\cong C_2*C_3=\langle a,b\mid a^2=b^3=1\rangle$ の有限商とちょうど同じもの**である。

**証明.** $a^2=b^3$ は $a$ とも $b$ とも可換で $B_3=\langle a,b\rangle$ ゆえ中心的。$B_3$ の標準表示との同値は $\sigma_1=b^{-1}a,\ \sigma_2=a^{-1}b^2$ の相互置換で直接確認(下の GAP 検算 D-0 で機械確認済み)。∎

> ### 補題 0.2($P$ 上の $S_3$ 作用の明示式)
> $\Gamma$ で $a^2=b^3=1$、$s_1=b^{-1}a=b^2a$、$s_2=ab^2$ とおき、$x=s_1^2,\ y=s_2^2$、$w:=byb^{-1}$ とすると
> $$\boxed{\;xyw=1,\qquad b:\ x\mapsto y\mapsto (xy)^{-1}\mapsto x,\qquad a:\ x\leftrightarrow y.\;}$$
> とくに $F_2=\langle x,y\rangle=\ker(\Gamma\twoheadrightarrow S_3)$ は自由階数 2、$b$ の作用は位数 3、$a$ の作用は位数 2。

**証明(語計算・自由積内、$a^2=b^3=1$).**
$x=b^2ab^2a$、$y=ab^2ab^2$。$bxb^{-1}=b^3ab^2ab^{-1}=ab^2ab^2=y$ ✓。$w=byb^{-1}=bab^2ab$。
$xy=b^2ab^2\cdot b^2ab^2=b^2ab^4ab^2=b^2abab^2$、
$xyw=b^2abab^2\cdot bab^2ab=b^2abab^3ab^2ab=b^2ab\,a^2\,b^2ab=b^2ab\cdot b^2ab=b^2ab^3ab=b^2a^2b=b^3=1$ ✓。
$as_1a^{-1}=a(b^2a)a=ab^2=s_2$ ゆえ $a:x\mapsto y$、同様に $y\mapsto x$。$\ker(\Gamma\to S_3)$ が自由階数 2 なのは Kurosh(核は $a,b,b^2$ の共役を含まない)+ $\chi(C_2*C_3)=-\tfrac16$、指数 6 ゆえ $\chi=-1$。∎

> ### 命題 0.3(持ち上げの十分条件 — **構成的**)
> $G$ を**完全**(perfect)かつ **(2,3)-生成**な有限群とし、$a_1^2=b_1^3=1$、$\langle a_1,b_1\rangle=G$ とする。
> $$E:=G\times S_3,\qquad a:=(a_1,(1\,3)),\quad b:=(b_1,(1\,3\,2))$$
> とおくと、$E=\langle a,b\rangle$、$a^2=b^3=1$、$E\twoheadrightarrow S_3$(第 2 成分)であり、対応する
> $$s_1=b^{-1}a,\quad s_2=ab^2\ \text{は braid 関係を満たし}\quad
> P:=\langle s_1^2,s_2^2\rangle=\ker(E\twoheadrightarrow S_3)=G\times1\cong G,$$
> $$\bar x=s_1^2=(b_1^{-1}a_1)^2,\qquad \bar y=s_2^2=b_1\bar x b_1^{-1}.$$
> さらに $c=(s_1s_2)^3=1$、すなわちこれは **$c\in N$ 窓**である。

**証明.** $a^2=(a_1^2,1)=1$、$b^3=1$ ✓。$\langle a,b\rangle$ は両成分に全射、$G$ 完全ゆえ Goursat の共通商は自明、よって $\langle a,b\rangle=G\times S_3$ ✓。
$b^{-1}a=(b_1^{-1}a_1,\ (1\,3\,2)^{-1}(1\,3))$ の第 2 成分は互換ゆえ $s_1^2=((b_1^{-1}a_1)^2,1)$ ✓。
$\langle\bar x,\bar y\rangle=\mathrm{im}(F_2)$ は $E$ で正規、$\Gamma/F_2=S_3$ ゆえ $E/\mathrm{im}(F_2)$ は $S_3$ の商;一方 $\mathrm{im}(F_2)\subseteq G\times1$ で $E/(G\times1)=S_3$ ゆえ $E/\mathrm{im}(F_2)\twoheadrightarrow S_3$。$S_3$ の商が $S_3$ に全射 ⟹ 同型 ⟹ $\mathrm{im}(F_2)=G\times1$ ✓。
$b_1\bar xb_1^{-1}=(b_1b_1^2a_1b_1^{-1})^2=(a_1b_1^{-1})^2=\bar y$ ✓。∎

**この命題が WA-c を「群の構成問題」から「(2,3)-生成対の探索問題」に落とす。**
監査 §7.3 の「残る困難(UNKNOWN)」は、$c\in N$ 窓に限れば**消える**。

> ### 系 0.4(必須の双曲性 — 探索空間を強く切る)
> $m:=\mathrm{ord}(b_1^{-1}a_1)$ とおくと $G$ は三角群 $\Delta(2,3,m)$ の商。
> $\Delta(2,3,m)$ は $m\le5$ で有限($A_4,S_4,A_5$)、$m=6$ でユークリッド(可解)。
> ゆえに $\lvert G\rvert>60$ の非可解 $G$ には **$m\ge7$ が必須**。
> かつ $\mathrm{ord}(\bar x)=\mathrm{ord}((b_1^{-1}a_1)^2)=m/\gcd(2,m)$。

**証明.** $a=b^{-1}\cdot(b^{-1}a)^{-1}\cdot$… 直接には $u:=b_1^{-1}a_1$ に対し $u^{-1}=a_1b_1$ ゆえ $m=\mathrm{ord}(a_1b_1)$ で、$\langle a_1,b_1\mid a_1^2,b_1^3,(a_1b_1)^m\rangle=\Delta(2,3,m)$。∎

---

## 1. 候補 P

### 1.1 候補 (a): 監査 §7.3 の $A_{13}$ — 篩条件は成立(再確認 PASS)

`design_wac.g` D-1(GAP 単系統):$P=A_{13}$、$\bar x=(7\,8\,9\,10\,11\,12\,13)$、$\bar y=(1\,\dots\,7)$。

| 量 | 値 | 可解? |
|---|---|---|
| $\langle\bar x,\bar y\rangle$ | $=A_{13}$ ✓ | — |
| $C_P(\bar y)$ | $C_7\times A_6$、位数 2520 | **非可解** ✓ |
| $\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)=C_{S_{13}}(\bar x)$ | $C_7\times S_6$、位数 5040 | **非可解** ✓ |

系 7.2 の必要条件は満たす。**しかし §2 で持ち上げ不能を証明する。**

### 1.2 候補 (b) の選定原理 — 「$\bar x$ は同じ長さの巡回を 5 本以上もて」

$P=A_n$($n\ge7$、$n\ne6$)では $\mathrm{Aut}(P)=S_n$、$\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)=C_{S_n}(\bar x)$、
$C_{S_n}(\bar x)=\prod_\ell(C_\ell\wr S_{m_\ell})$($m_\ell$ = 長さ $\ell$ の巡回の本数、不動点は $\ell=1$)。
$C_\ell\wr S_m$ 可解 $\iff m\le4$。また $C_{A_n}(\bar x)$ は $C_{S_n}(\bar x)$ の指数 $\le2$ 部分群ゆえ可解性は同値。$\bar y$ は $\bar x$ と $E$ 共役(補題 0.2 の $b$)ゆえ $C_P(\bar y)\cong C_P(\bar x)$。したがって:

> ### 補題 1.1($A_n$ 標的の判定条件)
> $P=A_n$ に対し 系 7.2 の必要条件 $\iff$ **$\bar x$ が同じ長さの巡回を 5 本以上もつ**(不動点も 1-巡回として数える)。加えて $\mathrm{ord}(\bar x)\ge3$。

---

## 2. 持ち上げ — Ree 篩と、$A_{13}$ の不能性証明

### 2.1 【本稿の主結果 1】Ree の不等式が逆設計の主関門

> ### 補題 2.1(Ree 篩)
> $H\le S_n$ を推移群、$H=\langle a',b'\rangle$、$a'^2=b'^3=1$、$u':=b'^{-1}a'$ とする。
> $c(\cdot)$ を $n$ 点上の巡回数(不動点込み)とすると
> $$\boxed{\;c(a')+c(b')+c(u')\ \le\ n+2.\;}$$
> $k$ = $a'$ の互換の本数、$j$ = $b'$ の 3-巡回の本数とすれば同値に
> $$c(u')\ \le\ k+2j+2-n\ \le\ \lfloor n/2\rfloor+2\lfloor n/3\rfloor+2-n .$$

**証明.** $a'b'u'=a'b'b'^{-1}a'=a'^2=1$。Ree の定理(1971;同値に「3 分岐点上の連結被覆の種数 $\ge0$」= Riemann–Hurwitz $2g-2=-2n+\sum(n-c(\sigma))\ge-2$)より $\sum_\sigma(n-c(\sigma))\ge2(n-1)$、すなわち $3n-\sum c\ge2n-2$。∎
(初等証明: 各 $\sigma$ は $n-c(\sigma)$ 個の互換の積、全体の積が 1 かつ推移性から、現れる互換の「連結グラフ」条件で $\ge n-1$ 本必要、積が 1 ゆえ本数は偶数で $\ge2(n-1)$。)

【文献要請なし】— Ree の不等式は上の初等論法で自足する。**正典外の引用は使っていない。**

### 2.2 【本稿の主結果 2】$A_{13}$ は $B_3$-窓に持ち上がらない

> ### 定理 2.2($A_{13}$ 標的の否決)
> $N\trianglelefteq B_3$ を有限指数の窓で $P_N\cong A_{13}$ とする。このとき
> $$C_{P_N}(\bar y)\ \text{も}\ \mathrm{Stab}_{\mathrm{Aut}(P_N)}(\bar x)\ \text{も可解}$$
> であり、命題 7.1(Hol 篩)より $GTSh(N,N)$ は**可解**。
> すなわち監査 §7.3 の $A_{13}$ 標的は、$c\in N$ か否かによらず**壁キャンペーンには使えない**。

**証明.**
(i) $\bar E:=E/\langle\bar c\rangle$ とおく($E=B_3/N$、$\bar c$ は中心)。$Z(A_{13})=1$ と $P\cap\langle\bar c\rangle\subseteq Z(P)$ より $P\cap\langle\bar c\rangle=1$、ゆえに $\bar A:=A/\langle\bar c\rangle\cong P\cong A_{13}$、$\bar E/\bar A\cong S_3$。補題 0.1 より $\bar E=\langle\bar a,\bar b\rangle$、$\bar a^2=\bar b^3=1$。命題 0.3 の指数論法(そこで使ったのは「$F_2$ の像は正規で商が $S_3$ の商」だけで、直積構造は不要)より $\langle\bar s_1^2,\bar s_2^2\rangle=\bar A$、$\bar x=\bar u'^2$($\bar u'=\bar s_1$)。
(ii) 共役作用 $\bar E\to\mathrm{Aut}(\bar A)=S_{13}$ の像は $\mathrm{Inn}(\bar A)=A_{13}$ を含むので **13 点上推移的**。像を $H$、$a',b',u'$ を像とすると $a'^2=b'^3=1$、$H=\langle a',b'\rangle$。
(iii) 補題 2.1: $c(u')\le\lfloor13/2\rfloor+2\lfloor13/3\rfloor+2-13=6+8+2-13=3$。
(iv) $\bar x=u'^2$。長さ $\ell$ の巡回は $\ell$ 偶なら $\ell/2$ の 2 本、$\ell$ 奇なら $\ell$ の 1 本に分かれる。$t:=c(u')\le3$ の分割 $\ell_1+\dots+\ell_t=13$ から長さ共通の巡回を 5 本以上得るには、偶部 $e$ 本・奇部 $o$ 本が $2e+o\ge5$、$e+o\le t\le3$ を満たす必要がある。可能なのは $(e,o)=(3,0)$($6L=13$)と $(2,1)$($5L=13$)のみで、いずれも 13 が $6$ でも $5$ でも割れないため**不可能**。
(v) よって補題 1.1 の条件が破れ、$C_{S_{13}}(\bar x)$ は可解。$\bar x$(および共役 $\bar y$)の $P$ 内・$\mathrm{Aut}(P)$ 内の中心化群/安定化群はすべて可解。命題 7.1 より $GTSh(N,N)$ 可解。∎

**注(監査 §8.2【WA-c】への回答)**: 監査は持ち上げを「UNKNOWN・未着手」としたが、**答は NO(証明つき)**。監査 §7.3 の $A_{13}$ は「$P$ 水準では実現可能」だが「$B_3$-窓としては実現不可能」。この落差の正体が Ree 篩である。

### 2.3 $A_n$($n\le15$)の全否決

$k$ の偶奇で $\bar E\to S_n$ の像が $A_n$($k$ 偶)か $S_n$($k$ 奇)かが決まり、$\mathrm{sign}(u')=(-1)^k=(-1)^{n-c(u')}$。両偶奇を尽くして補題 2.1 + 補題 1.1 + 双曲性($\mathrm{ord}(u')\ge7$、系 0.4)+ $\mathrm{ord}(\bar x)\ge3$ を課すと(`enum2.g` E2-1、$n=9..16$ 全分割を悉皆):

| $n$ | 生き残る $u'$ の型 | 結果 |
|---|---|---|
| 9, 10, 11, 13, 14 | **なし** | 組合せ論で否決 |
| 12 | $(7,2,2,1)$、$k=6$、$j=4$(強制) | **類構造定数 $=0$** ⟹ 否決 |
| 15 | $(9,2,2,2)$、$(10,2,2,1)$、$k=7,j=5$(強制) | 構造定数 $72,120$ だが**全解を厳密列挙して $S_{15}$ を生成する解はゼロ** ⟹ 否決 |
| 15 | $(3,4,4,4)$ | 構造定数 $=0$ ⟹ 否決 |
| **16** | $(11,2,2,1)$ / $(2,2,2,10)$、$k=8,j=5$ | **実現** ✓(§2.4) |

- $n=12$: `enum.g` E-2 と `ree.g` R-1 が独立に $\mathrm{ClassMultiplicationCoefficient}=0$ を出し、`ree.g` R-2 の 20 万回標的探索も 0 ヒット(二重確認)。
- $n=15$: `a15c.g` は $u'$ を固定し $C_{S_{15}}(u')$-軌道で解集合を**完全列挙**($72=72$、$120=40+80$ で構造定数と一致 ⟹ 悉皆)。生成される群は $(9,2,2,2)$ で位数 3024・軌道 $\{6,9\}$(非推移)の一種類、$(10,2,2,1)$ で位数 360・軌道 $\{3,12\}$ と位数 150(推移だが $S_{15}$ でない)の二種類。**$S_{15}$ は現れない。**

> ### 定理 2.3(最小性)
> 系 7.2 の必要条件を満たす $P_N\cong A_n$ をもつ $B_3$-窓は $n\le15$ には存在せず、$n=16$ に存在する。

### 2.4 【本稿の主結果 3】$n=16$ の明示窓 $W\text{-}D\text{-}A16\text{-}11a$

`a16.g` が 40 万回試行で 20 個の実現を発見(すべて推移的、すべて $A_{16}$)。一つを固定:

```
a1 := ( 1, 2)( 3,14)( 4,10)( 5,12)( 6, 8)( 7,16)( 9,13)(11,15);;   # 2^8
b1 := ( 2,11,14)( 3,15,10)( 4, 9,12)( 5,13, 8)( 6, 7,16);;         # 3^5 1
```
$\langle a_1,b_1\rangle=A_{16}$ ✓、$u=b_1^{-1}a_1$ は型 $(11,2,2,1)$・位数 22、$\bar x=u^2$ は型 $(11,1^5)$・位数 11。
命題 0.3 により $E:=A_{16}\times S_3$(19 点の置換群)。`build_a16.g` の全 assert:

| 項目 | 値 |
|---|---|
| $a^2=b^3=1$ | true |
| braid $s_1s_2s_1=s_2s_1s_2$ | **true** |
| $c=(s_1s_2)^3=1$ | **true**(**$c\in N$ 窓**) |
| $\mathrm{ord}(s_1)=\mathrm{ord}(s_2)$ | 22 $=2\cdot\mathrm{ord}(\bar x)$ ✓ |
| $\langle s_1,s_2\rangle=E$、$[B_3:N]=\lvert E\rvert$ | $62{,}768{,}369{,}664{,}000=6\lvert A_{16}\rvert$ |
| $P=\langle s_1^2,s_2^2\rangle=\ker(E\twoheadrightarrow S_3)$ | true、$\lvert P\rvert=\lvert A_{16}\rvert=10{,}461{,}394{,}944{,}000$ |
| $\bar x,\bar y$ の型 / 台の重なり | ともに $(11,1^5)$ / 6 点 |
| $N_{\rm ord}=\mathrm{lcm}(11,11,1)$ | **11** |
| $C_P(\bar y)$ | $C_{11}\times A_5$、位数 **660**、**非可解** ✓ |
| $\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)$ | $C_{11}\times S_5$、位数 **1320**、**非可解** ✓ |

**系 7.2 の必要条件を満たす、明示された $B_3$-窓が初めて手に入った。**

---

## 3. 第一撃の指名 — $W\text{-}D\text{-}A16\text{-}11a$

### 3.1 諸元

| 項目 | 値 |
|---|---|
| 窓 ID | `W-D-A16-11a` |
| $E=B_3/N$ | $A_{16}\times S_3$、19 点置換群 |
| 指数 $[B_3:N]$ | $62{,}768{,}369{,}664{,}000$ |
| $c$ の像 | $\bar c=1$(**$c\in N$**;judge の `c_in_N` 系 assert と `EnumerateReducedHexagon` 交差検証がすべて有効) |
| $P_N$ | $A_{16}$、$\bar x,\bar y$ は台が 6 点で重なる 11-巡回 |
| $N_{\rm ord}$ / charming $m$ 数 | $11$ / $\varphi(22)=\mathbf{10}$ |
| $\lvert[P,P]\rvert$ | $=\lvert A_{16}\rvert=10{,}461{,}394{,}944{,}000$($A_{16}$ 完全) |

### 3.2 kerchi-judge v1.1 入力(モード (b))

```gap
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11)(12,13)(14,15)(17,18);;
JUDGE_S2_IMG := ( 1,14,10,12, 8,16, 6,13, 4,15, 2)( 3,11)( 5, 9)(18,19);;
JUDGE_ID     := "W-D-A16-11a";;
JUDGE_OUTFILE := "search/certs/kerchi_judge_WDA16_11a.json";;
```
(1..16 が $A_{16}$ 因子、17..19 が $S_3$ 因子。$s_1$ の $A_{16}$ 成分は $u$ そのもの。)

### 3.3 【本稿の主結果 4・blocker】予算 — 素の judge は走らない

`kerchi-judge.g` の `CorrectedShadows` は
```gap
for f in Elements(DerivedSubgroup(W.PN)) do ... for m in charmingSet do ...
```
すなわち **$[P,P]$ を全列挙**する。よって

$$\text{素の候補数}=c_m\cdot\lvert[P,P]\rvert=10\times1.046\times10^{13}=\mathbf{1.046\times10^{14}}$$

**実行不能**(`Elements` の時点でメモリ死・8GB 制約以前の問題)。これは $A_{16}$ 固有ではなく、**$P$ が非可解な窓すべてで judge v1.1 が壊れる**ことを意味する。

### 3.4 【修理仕様】$\Xi$-制限 — $10^{14}\to8.7\times10^{6}$

> ### 命題 3.1($\Xi$-制限;すべての窓に有効・fail-closed)
> $[m,f]\in GTSh(N,N)$ ならば $E_{m,f}\in\mathrm{Aut}(P_N)$ が存在して
> $$E_{m,f}(\bar x)=\bar x^{2m+1},\qquad E_{m,f}(\bar y)=f^{-1}\bar y^{2m+1}f .$$
> ゆえに $f$ は
> $$\mathcal C_m=\bigcup_{\alpha\in\mathcal A_m}\{f\in[P,P]:f^{-1}\bar y^{2m+1}f=\alpha(\bar y)\},\qquad
> \mathcal A_m:=\{\alpha\in\mathrm{Aut}(P):\alpha(\bar x)=\bar x^{2m+1}\}$$
> に属し、$\mathcal A_m$ は空か $\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)$ の剰余類、内側は空か $C_P(\bar y^{2m+1})$ の剰余類。したがって
> $$\boxed{\;\lvert\mathcal C_m\rvert\le\lvert C_P(\bar y^{2m+1})\rvert\cdot\lvert\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)\rvert\;}$$
> 列挙予算は $\lvert[P,P]\rvert$ ではなく $\;c_m\cdot\lvert C_P(\bar y)\rvert\cdot\lvert\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)\rvert$。

**証明.** GT-shadow は $T_{m,f}:B_3/N\to B_3/N$ が well-defined な全射準同型であることを要求する(judge の settled 節)。$T(\sigma_1)=\sigma_1^{2m+1}$ より $T(x)=x^{2m+1}$、$T(y)=f^{-1}y^{2m+1}f$。有限 $P$ の全射自己準同型は自己同型ゆえ $E_{m,f}\in\mathrm{Aut}(P)$。$\alpha,\alpha'\in\mathcal A_m$ なら $\alpha^{-1}\alpha'\in\mathrm{Stab}(\bar x)$。$f,f'$ が同じ $\alpha$ を与えるなら $f'f^{-1}\in C_P(\bar y^{2m+1})$。∎

**$W\text{-}D\text{-}A16\text{-}11a$ への適用**: $\bar y$ の位数 11 は素数で $\gcd(2m+1,11)=1$(charming)ゆえ $\langle\bar y^{2m+1}\rangle=\langle\bar y\rangle$、$C_P(\bar y^{2m+1})=C_P(\bar y)=660$。$\mathrm{Stab}=1320$。

$$\lvert\ker\widetilde\chi\rvert\le660\times1320=871{,}200,\qquad
\lvert G_N\rvert\le10\times871{,}200=\mathbf{8{,}712{,}000},$$
候補数も **$8.7\times10^6$**。**7 桁の縮小。**

さらに $\mathrm{Aut}(A_{16})=S_{16}$ で $(11,1^5)$ 型は $A_{16}$-類が分裂しないので $U=\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)=C_{11}\times S_5$(監査 §7.1 の $U$ を**この窓では厳密に同定できる** — 監査 §8.2【WA-d】の部分解)。

**この窓が「篩を生き延びる」理由と「計算できる」理由が同一の量**($C_P(\bar y)$・$\mathrm{Stab}$ が**非可解だが小さい**:660 と 1320)であることに注意。命題 7.1 の上界 $\mathrm{dl}\le1+\mathrm{dl}(C)+\mathrm{dl}(\mathrm{Stab})$ は非可解ゆえ空虚 = 篩は殺さない。一方 $\mathfrak F_0$ は $C_{11}\times A_5$ の部分群による $C_{11}\times S_5$ の部分群の拡大に埋まるので、**$\ker\widetilde\chi$ が非可解になりうる**(TIER-1 到達可能性が原理的にある初の窓)。D1 は §7.5 で「TIER-1 にすら届かない」と予言されていた帯なので、これは質的に違う。

### 3.5 CI(gap-run)で流す形

**段階 1(即実行可・数分)** — 窓の再構成と全 assert(判定はまだしない):
```
script:   search/probe/wac_v1/build_a16.g
out_dir:  search/certs
```
**段階 2(judge 修理後)** — 命題 3.1 の $\Xi$-制限を `CorrectedShadows` に入れた `kerchi-judge v1.2` に、§3.2 の preamble を与える。
$m$ ごと(10 シャード)、さらに $\alpha\in U$ ごと(1320 シャード)に分割すれば 1 シャード 660 候補で 600 秒 cap に余裕。シャード出力の JoinC は G1★ 工程の既存線形化をそのまま流用できる。

**修理は数学者の職掌外(実装)なので、命題 3.1 を仕様として司令塔経由で implementer へ。** 仕様の要点:
1. `for f in Elements(DerivedSubgroup(W.PN))` を、$m$ ごとに $\mathcal C_m$ を構成するループへ置換。
2. $\mathcal A_m$ の構成: $\mathrm{Aut}(P)$ 全体は作らない。$\alpha_0$ を一つ見つけ($\bar x\mapsto\bar x^{2m+1}$ を実現する $\mathrm{Aut}(P)$ の元;$P=A_n$ なら $S_n$ 内の共役元探索で足りる)、$\mathcal A_m=\alpha_0\cdot\mathrm{Stab}(\bar x)$。
3. 各 $\alpha$ に対し $f_0$ を $\bar y^{2m+1}\mapsto\alpha(\bar y)$ の共役元として求め、$f\in f_0\cdot C_P(\bar y^{2m+1})$ を走らせる。**$f\in[P,P]$ の判定は最後に置く**($A_{16}$ では $[P,P]=P$ なので自明)。
4. **fail-closed**: $\lvert\mathcal C_m\rvert$ の実測値と上界 $660\times1320$ を証明書に併記し、超過したら Error。旧 `Elements([P,P])` 経路との一致は $\lvert P\rvert$ が小さい窓(D1 $p=5,7$・N5cong)で回帰テストする — **これが修理の較正ゲート**。

---

## 4. 自己点検(N_A の教訓を明記)

**(1) 十分性の誤読を禁じる。** 系 7.2 は**必要条件**である。$W\text{-}D\text{-}A16\text{-}11a$ が $C_P(\bar y)$・$\mathrm{Stab}$ ともに非可解であることは「Hol 篩がこの窓を可解と断定できない」ことしか意味せず、$GTSh(N,N)$ が非可解であることも、$\ker\widetilde\chi$ が非可換であることさえも**まったく含意しない**。これは N_A の教訓そのもの — 必要側の指標が生きていることを陽性判定と読み替えた失敗型で、本稿の第一撃は「非可解の証明」ではなく「篩で殺されない最初の窓の判定実行」にすぎない。judge の出力が ABELIAN だった場合、それは失敗ではなく**予算 $8.7\times10^6$ で得た正当な UNKNOWN 解消**である。

**(2) 状態札。** §0.5・§2.1・§2.2・§3.4 は**紙上証明(paper-proof candidate)**であって Lean verified ではない。§1.1・§2.3・§2.4 の数値はすべて **GAP 4.16.0 単系統**であり cross-checked ではない($n=12$ のみ構造定数と標的探索の二経路で一致 — ただし同一処理系なので二系統ではない)。$n=15$ の悉皆性は「構造定数(指標理論)= 列挙個数」の一致に依存しており、そこが二重確認の実体。

**(3) 残る穴。** (i) 定理 2.3 は **$P\cong A_n$ に限った最小性**であり、非交代群 $P$(例えば $\mathrm{Stab}_{\mathrm{Aut}(P)}$ が非可解になる非単純 $P$)がより小さく存在する可能性は**未探索・UNKNOWN**。悉皆探索はしていない。(ii) 命題 0.3 は十分条件であり、$c\notin N$ の窓を尽くしていない(ただし定理 2.2 の否決は $c\notin N$ も込みで成立する)。(iii) $U'=\mathrm{Im}\,\Xi$ の同定(【WA-d】)は本窓で $U$ の上界までしか進めていない。

**(4) 判断の帰属。** 定理 2.2 は監査 §7.3 の標的を**否決**する。監査は自分の起草物なので、これは自己反証である — 「$P$ 水準の実現可能性」を「窓の実現可能性」と読み替えたのが誤りの所在で、両者を隔てるのが Ree 篩であった。この分離は監査 §8.2【WA-c】に「残る困難」として自ら書いていたが、困難の**向き**(存在するが難しい / そもそも存在しない)を取り違えていた。

---

## 5. 検算証明書(GAP 4.16.0・`gap.ps1` 経由・すべて単系統)

| スクリプト | SHA-256 | 内容 |
|---|---|---|
| `search/probe/wac_v1/design_wac.g` | `9f5d70e1d45e5de6df33204d4e4de9ce9c0e79bec83a8c3b11bd8e0f46c5c0d0` | D-1 $A_{13}$ 再確認・D-2 $A_{12}$・D-3 素朴探索(NOT FOUND) |
| `search/probe/wac_v1/diag.g` | `ebf1bb6470ac88fd9bf4976f9b4dc26f70561090ee3adee2e154914d76ba328b` | NOT FOUND の原因診断(型一致 111 件) |
| `search/probe/wac_v1/diag2.g` | `93be02f0e668fb925affaf4b6c170d5962824d839140e4d50559cd41f4d70c9f` | 111/111 が非推移 → Ree 篩の発見 |
| `search/probe/wac_v1/ree.g` | `1c839f358abf104a29ee771d8df34018256e9ce2dddd2cbfa0f12abd662901c6` | $A_{12}$ 構造定数 $=0$・20 万回標的探索 0 ヒット・Ree 上界表 $n=9..24$ |
| `search/probe/wac_v1/enum.g` | `1871f69b1dbce96eb8dd57e359d297c9c61d1da6910c461560c25584a6d2bbf1` | 組合せ生き残り悉皆($u$ 偶のみ)+ $S_n$ 構造定数 |
| `search/probe/wac_v1/enum2.g` | `58964b42ccffb0229215166e0cf51ae3d649b90869b466952a416a6c221dac7b` | 両偶奇での悉皆($n=9..16$)+ 構造定数 — 定理 2.3 の主表 |
| `search/probe/wac_v1/a16.g` | `38a790b921f24c97291cd7d3cb7e48c258c3f01e199ed987b60b5ee5f90b0606` | $n=16$ の実現探索(40 万回・20 ヒット・全て $A_{16}$) |
| `search/probe/wac_v1/a15.g` | `f1b3f28a3db160a04471e1bdc43377b3f1988e76c490825d112b177a6fa978e1` | $n=15$ 標的探索(30 万回・$S_{15}$ ゼロ) |
| `search/probe/wac_v1/a15b.g` | `efd8316801facbf347daa713a3f229e2e1f545c21ac1b9190f0f731f5a17c12e` | $n=15$ 実現群の同定(位数 3024 / 360 / 150) |
| `search/probe/wac_v1/a15c.g` | `4b124b7aa27f11fee6e002bb068f0c08db5973419629baef2535590b26f29527` | $n=15$ の否決(全解 72/120 を $C_{S_{15}}(u)$-軌道で**完全列挙**) |
| `search/probe/wac_v1/build_a16.g` | `bc0921da53801b16a38f3dcd05b141a60d60e0bf827802e271af0d268cd44a8d` | 窓 `W-D-A16-11a` の構成と全 assert・予算・judge 入力 |

**登録宇宙の掃引結果ではない。台帳請求権はまだ発生していない。**


