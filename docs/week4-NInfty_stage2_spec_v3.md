# $N_\infty$ searcher — **stage 2 述語の仕様(spec v3)**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 71)。v2(`docs/week4-NInfty_stage2_spec_v2.md`)を supersede。**
**身分**: **spec 草案・Sol 監査前**。
```text
supersedes_draft            = sha256:77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2
audited_predecessor_rejected= sha256:813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4
predicate_spec_freeze_id    = NOT ISSUED
implementation_status       = NOT AUTHORIZED
model_builder status        = LOCKED
```
**正典**: `sol/sol_reply_60_seal_spec_v2.md` **F6–F14**(核 4 補題 PASS・精密化 P60-B1〜B9)・便 59 F5–F14・便 54 F6/F9/F12・S5 設計 **命題 S5-1 / 命題 S5-2 / 系 S5-2a / §3.3.5 S5-3∞**・便 36 F2.1・Rule 1 v1.4。
**接触規律**: 値に依存しない。$\hat c_\mu$(以下 $C$)・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。

> **便 60 の判定**: 核 4 補題(`N∞-fix` / `N∞-swap` / `N∞-red` / `N∞-div`)は **PASS**、**F8.3 の独立再構成も承認**。v3 が閉じるのは **P60-B1〜B9 の精密化**である。

---

## 0. v2 → v3 差分(P60-B1〜B9)

| ID | v2 | v3 | 出所 |
|---|---|---|---|
| **B1** | `N∞-N` を $\operatorname{div}(H_v)=\pi_*(\mu^{-1}(v))$ と書いた(**左辺 deg 0・右辺 deg 5 で型不整合**) | **(60.2) $(H_v)_0=\pi_*[\mu^{-1}(v)]$** を定理文に。(60.1) を併記。**norm → divisor pushforward の証明 artifact を明示**。**自認** | 便 60 F6.1 |
| **B2** | `N∞-1:1` が**集合の単射**までで停止 | **(60.3)**($\iota Q\in\mu^{-1}(v)\iff v^2=C$・$v^2\ne C$ なら Weierstrass 点も不在)と **(60.4)**($\operatorname{ord}_{x(Q)}H_v=\operatorname{ord}_Q(v-\mu)$)を追加し、**局所 multiplicity 一致まで証明**。**自認** | 便 60 F6.2 |
| **B3** | `N∞-swap` の $j$-stability が暗黙・iff が無い | **$j$-stability を明示導出**し、**`N∞-criterion` (60.6) を iff 定理として設置**。**`N∞-pair` を `N∞-swap` より先に置き**、pair(十分)/swap(必要)/criterion(iff)の**三段一方向依存**に(F13.1)。**E-7 を target condition・E-1〜E-6 を raw precondition へ型分離** | 便 60 F6.4・F7・F8.1・F13.1 |
| **B4** | T-2 が「$a'/p$ が $p$ と比例しない場合の整合」(**pass predicate として型未定**) | **(60.5)**: $d:=\operatorname{monic}\gcd(a,a')$、**$a'\doteq p\,d$**、**$a'/p\doteq d$** | 便 60 F6.6・F8.3 |
| **B5** | T-1 後の失敗に `REJECT` と `INTEGRITY_STOP` の**双方**を割当(同一到達状態に二 verdict) | **T-1 通過後は全て cross-check lane** ⟹ **到達状態を一意化**(不一致は**すべて `INTEGRITY_STOP`**)。**actual finite partitions を両経路で比較**(F8.4)。**decision / audit lane を分離**(F13.2) | 便 60 F8.2・F8.4・F13.2 |
| **B6** | 「同じ divisor digest」に **canonical object が未定義**(number-field presentation / 順序で raw bytes が変わる) | **divisor canonical object schema を規範化**、**または** 第三の **divisor-equality certificate**(F9.2 の自己訂正を採用)。**二層 freeze ID 束**(F13.3) | 便 60 F9.2・F13.3 |
| **B7** | `fibers[]`・divisor digest が `sealed` の**外**(candidate-dependent = dictionary key) | **`SEALED_INTERNAL` へ移動**。public は **random opaque `candidate_ref` + code identity + verdict/reason + 数学的射影 5 欄**。**`fiber_ref` の typed random-reference schema 統一**・**EP extension field** | 便 60 F10.1 |
| **B8** | provenance の出所が `S5-2` に集約(誤り) | **F11 の行別 source map へ**: branch type / $(5,2^21,2^21,5)$ = **系 S5-2a**、orientation = **命題 S5-1**(+ S5-3∞ との同値)、$\lambda=c\mu^2$ = **命題 S5-2**。**negative lane runner と clean HMAC steward の役割分離**(tainted actor は steward 不可) | 便 60 F11・F10.2 |
| **B9** | whitelist の $[s^2]=[C]$ に **base field $K$ が未宣言** | **$K$・$-1\in K^{\times2}$ の proof ID・S5-4∞ dependency を freeze bundle に型付け** | 便 60 F10.4 |

---

## 1. 数学的基礎

### 1.1 設定

$$ C_{\rm crv}:\ y^2=f_6(x),\ \deg f_6=6,\ f_6\ \text{monic squarefree};\qquad \mu=a(x)+p(x)y,\ \deg a=5,\ \deg p=2,\ a_5=p_2\ne0 $$
$$ \textbf{(Pell)}\ \ a^2-f_6p^2=C\in\mathbb Q^\times,\qquad \textbf{(Or)}\ \ (\mu)=5P_0-5P_\infty $$
$\iota$ = 超楕円対合、$\pi:C_{\rm crv}\to\mathbb P^1_x$、$j(v):=C/v$。$\gcd(a,p)=1$ は (Pell) から自動。

### 1.2 補題 `N∞-N`(norm / divisor pushforward)【B1 で型修理】

$$ H_v:=(v-\mu)(v-\mu^\iota)=(v-a)^2-p^2f_6=v^2-2va+C \tag{N-1} $$

> **補題 `N∞-N`.** $v\ne0,\infty$ に対し
> $$ \operatorname{div}_{\mathbb P^1_x}(H_v)=\pi_*\operatorname{div}_{C_{\rm crv}}(v-\mu)=\pi_*[\mu^{-1}(v)]-5[\infty_x] \tag{60.1} $$
> 同値に、**零 divisor だけを取って**
> $$ \boxed{\ (H_v)_0=\pi_*[\mu^{-1}(v)]\ } \tag{60.2} $$

**証明 artifact(norm → divisor pushforward).**
1. **norm 恒等式**: $\mu\mu^\iota=N(\mu)=C$ と $\mu+\mu^\iota=2a$ より $(v-\mu)(v-\mu^\iota)=v^2-2va+C$。左辺は $\iota$-不変な $C_{\rm crv}$ 上の関数なので $\pi$ で $\mathbb P^1_x$ へ降り、それが $H_v$。
2. **pushforward**: 有限射 $\pi$ に対する **norm 写像 $N_{\pi}:\pi_*\mathcal O_{C_{\rm crv}}^\times\to\mathcal O_{\mathbb P^1}^\times$** は $\operatorname{div}\circ N_\pi=\pi_*\circ\operatorname{div}$ を満たす(有限平坦射の norm と divisor の両立)。$H_v=N_\pi(v-\mu)$ だから $\operatorname{div}(H_v)=\pi_*\operatorname{div}(v-\mu)$。
3. **極の勘定**: $\operatorname{div}(v-\mu)=[\mu^{-1}(v)]-[\mu^{-1}(\infty)]=[\mu^{-1}(v)]-5P_\infty$((Or))。$\pi(P_\infty)=\infty_x$ で $\pi_*(5P_\infty)=5[\infty_x]$。以上で (60.1)、零部分を取って (60.2)。∎

> **⚠ v2 の誤り(自認)**: v2 §1.2 は $\operatorname{div}(H_v)=\pi_*(\mu^{-1}(v))$ と書いた。**左辺は次数 0 の principal divisor、右辺は次数 5 の effective divisor**で**型が合わない**(便 60 F6.1)。さらに証明を「2 乗消去」だけで済ませ、**norm/pushforward の一行を書いていなかった**。

### 1.3 系 `N∞-1:1`(局所 multiplicity 一致)【B2 で完成】

> **系 `N∞-1:1`.** $Q\in\mu^{-1}(v)$ なら $\mu^\iota(Q)=C/v$。ゆえに
> $$ \boxed{\ \iota Q\in\mu^{-1}(v)\iff v^2=C\ } \tag{60.3} $$
> **($Q=\iota Q$、すなわち $y(Q)=0$ の場合も同じ**: そのとき $\mu(Q)^2=\mu(Q)\mu^\iota(Q)=C$。**したがって $v^2\ne C$ の fiber には Weierstrass 点が存在しない**。)
> $v^2\ne C$ のとき $\pi|_{\mu^{-1}(v)}$ は単射かつ unramified で、各 $Q$ について
> $$ \boxed{\ \operatorname{ord}_{x(Q)}H_v=\operatorname{ord}_Q(v-\mu)\ } \tag{60.4} $$
> ゆえに **multiplicity partition が一致**する。さらに $v\ne0$ なら $H_v=-2v\,(a-w)$、$w=(v^2+C)/(2v)$。

**証明.** (60.3): $\mu(\iota Q)=\mu^\iota(Q)=C/v$ で、これが $v$ に等しいのは $v^2=C$ のとき。$y(Q)=0$ なら $\iota Q=Q$ で同じ式。
(60.4): $H_v=(v-\mu)(v-\mu^\iota)$ を $Q$ の近傍で見ると、$v^2\ne C$ より
$$ (v-\mu^\iota)(Q)=v-\frac Cv=\frac{v^2-C}{v}\ne0 $$
なので**他方の因子は $Q$ で単元**。$\pi$ は $Q$ で unramified($y(Q)\ne0$)だから $\operatorname{ord}_{x(Q)}=\operatorname{ord}_Q$ で、$\operatorname{ord}_{x(Q)}H_v=\operatorname{ord}_Q(v-\mu)$。∎

> **⚠ v2 の未完(自認)**: v2 は**集合の単射**までしか示さず、**(60.4) を書いていなかった** — それが multiplicity 一致に必要な一行である(便 60 F6.2)。

### 1.4 命題 `N∞-fix`(fixed fiber の局所構造)【便 60 F6.3 で PASS・不変】

$v^2=C$ なら fiber 全体で $py=0$、$a(x_0)=v$。三場合は exhaustive:

| 場合 | uniformizer | 結果 |
|---|---|---|
| (i) $y_0=0,\ p(x_0)\ne0$ | $y$ | $\operatorname{ord}_Q(py)=1$ ⟹ **$e=1$** |
| (ii) $p(x_0)=0,\ y_0\ne0$ | $x-x_0$ | $\operatorname{ord}(a-v)=2m$、$\operatorname{ord}(py)=m$ ⟹ **$e=m$**($m=\operatorname{ord}_{x_0}p$) |
| (iii) $p(x_0)=y_0=0$ | $y$ | $\operatorname{ord}_Q(p)=2m$、$\operatorname{ord}_Q(py)=2m+1$、$\operatorname{ord}_Q(a-v)=4m+2$ ⟹ **$e=2m+1$(奇数)** |

**⇒ (iii) から $e=2$ は出ない。**

### 1.5 補題 `N∞-pair`(十分側・**target を仮定しない**)【F13.1 採用・新設】

> **補題 `N∞-pair`.** 任意の Pell tuple に対し、$\bar{\mathbb Q}$ 上で $s^2=-C$ を選ぶ。$C\ne0$・標数 0 より $s^2\ne C$ なので、$\pm s$ の二 fiber は **non-fixed** であり
> $$ H_{s}=-2s\,a,\qquad H_{-s}=+2s\,a \tag{N-pair-1} $$
> $$ \boxed{\ \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=\operatorname{rootpart}(a)\ } \tag{N-pair-2} $$

**証明.** (N-1) に $s^2=-C$ を代入して (N-pair-1)。$a(x_0)=0$ なら (Pell) より $p(x_0)^2f_6(x_0)=-C=s^2\ne0$、すなわち **$p(x_0)\ne0$ かつ $f_6(x_0)\ne0$** — **両 fiber は自動的に非退化 locus**にある。$s^2=-C\ne C$ だから系 `N∞-1:1` の (60.4) が使え、multiplicity が一致。∎

> **★ この補題は target を一切仮定しない**(F13.1)。**candidate から canonical harmonic pair を構成する十分側**である。

### 1.6 補題 `N∞-swap`(必要側)【F6.4 で PASS・$j$-stability を明示】

> **補題 `N∞-swap`.** $\deg p=2$・$f_6$ squarefree の下で、**有限 branch fiber が二つとも $[2,2,1]$** かつ **有限 branch pair が $\{s,-s\}$**(系 S5-2a)ならば
> $$ \boxed{\ j(s)=-s,\qquad s^2=-C.\ } $$

**証明.**
**(0) $j$-stability の導出【B3 で明示】**: $\mu\circ\iota=C/\mu=j\circ\mu$。$\iota$ は $C_{\rm crv}$ の自己同型なので **ramification locus を保ち**、$j$ は target の Möbius 自己同型なので **branch-value set を保つ**。さらに $j$ は $0,\infty$ を交換するから、**有限二値 $\{s,-s\}$ は $j$-stable**。(v2 はこの一行を暗黙にしていた。**自認**。)
**(1) 二場合**: $\{s,-s\}$ が $j$-stable ⟹ **fixed**($s^2=C$)か **swapped**($s\cdot(-s)=C$ ⟹ $s^2=-C$)。
**(2) fixed の排除**: 命題 `N∞-fix` より fixed fiber で $e=2$ が出るのは **(ii) の $m=2$** のみ。$\deg p=2$ ゆえ double root は唯一で、その $x_0$ が与える fixed value $a(x_0)$ も唯一。ところが fixed case は $s$ と $-s$ の**双方**に $[2,2,1]$、すなわち双方に $e=2$ 点を要求する。$a(x_0)$ は一方にしかなれない($s\ne0$)。矛盾。∎

### 1.7 補題 `N∞-div`($p\mid a'$ と (60.5))【B4】

(Pell) を微分して $2aa'=p(f_6'p+2f_6p')$、$\gcd(a,p)=1$ より **$p\mid a'$**。
$d:=\operatorname{monic}\gcd(a,a')$ とし $\operatorname{rootpart}(a)=[2,2,1]$ とすると $\deg d=2$・$d$ squarefree。$\gcd(p,a)=1$ ゆえ $\gcd(p,d)=1$、かつ $\deg a'=4=\deg p+\deg d$。よって
$$ \boxed{\ a'\doteq p\,d,\qquad \frac{a'}{p}\doteq d\ } \tag{60.5} $$

### 1.8 **定理 `N∞-criterion`**(iff)【B3・便 60 F7.1 (60.6)】

> **定理 `N∞-criterion`.** E-1〜E-6 の下で次は同値:
> $$ \boxed{\ \operatorname{rootpart}(a)=[2,2,1]\iff \begin{array}{c}\operatorname{Br}(\mu)=\{0,s,-s,\infty\}\ \text{for some}\ s^2=-C,\\[2pt] \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=[2,2,1].\end{array}\ } \tag{60.6} $$
> **右辺は stage 2 が必要とする branch signature を述べる。monodromy 群そのものの再証明は主張しない。**

**証明(本稿で完成).**
**(⇐ 必要方向)** 右辺 ⟹ 有限 branch pair は $\{s,-s\}$ で二 fiber とも $[2,2,1]$ ⟹ **`N∞-swap`** ⟹ $s^2=-C$ ⟹ **`N∞-pair`** の (N-pair-2) ⟹ $\operatorname{rootpart}(a)=[2,2,1]$。
**(⇒ 十分方向)** $\operatorname{rootpart}(a)=[2,2,1]$ とし、$\bar{\mathbb Q}$ 上で $s^2=-C$ を取る($C\ne0$・標数 0 より $s\ne0$、$s^2\ne C$)。**`N∞-pair`** より両 fiber は non-fixed で partition は $[2,2,1]$、各 fiber の ramification contribution は $(2-1)+(2-1)=2$。**(Or)** より $0,\infty$ の二 fiber は各々 $e=5$ で contribution $4+4$。よって
$$ 4+4+2+2=12=2g(C_{\rm crv})-2+2\deg\mu $$
を**使い切る**。Riemann–Hurwitz より**余分な ramification point / branch value は存在しない**。ゆえに $\operatorname{Br}(\mu)=\{0,s,-s,\infty\}$ で、有限 branch polynomial は degree 2 かつ even。∎

> **★ 循環がないこと**(便 60 F7.3): **十分方向は `N∞-swap` の結論を一切仮定していない** — 使うのは `N∞-pair`(target 非依存)と RH だけである。
> **★ 依存の一方向性**(F13.1): $$ \texttt{N∞-pair}\ (\text{十分})\ \longrightarrow\ \texttt{N∞-criterion}\ (\text{iff})\ \longleftarrow\ \texttt{N∞-swap}\ (\text{必要}) $$ **`N∞-swap` は `N∞-pair` を使わず、`N∞-pair` は `N∞-swap` を使わない。**

---

## 2. 入口契約と target condition(B3 の型分離)

### 2.1 raw candidate precondition(E-1〜E-6)— **入口**

| # | 条件 | 出所【B8 で修正】 |
|---|---|---|
| E-1 | $\deg f_6=6$・monic・squarefree | **§3.3.5 S5-3∞** + 便 36 F2.1 |
| E-2 | $\deg a=5$・$\deg p=2$ | **§3.3.5 S5-3∞** |
| E-3 | $a_5=p_2\ne0$ | **§3.3.5 S5-3∞** |
| E-4 | (Pell) $a^2-f_6p^2=C\in\mathbb Q^\times$ | **§3.3.5 S5-3∞** |
| E-5 | **divisor orientation** $(\mu)=5P_0-5P_\infty$ | **命題 S5-1**(正規形との同値として S5-3∞) |
| E-6 | $\gcd(a,p)=1$ | E-4 から自動・独立 assert |

### 2.2 target condition(E-7)— **入口ではない**

| # | 条件 | 出所 | 身分 |
|---|---|---|---|
| E-7 | 有限 branch 値が**調和対** $\{s,-s\}$ | **系 S5-2a** | **target condition**。**T-1 と定理 `N∞-criterion` がこれを導出する。**T-6 は**別経路による cross-check** |

> **⚠ v2 の型衝突(自認)**: v2 は E-1〜E-7 を「一つでも無ければ precondition REJECT」としながら、T-0 では E-1〜E-6 しか検査せず E-7 を T-6 で計算していた。**同じ命題を input と output の両方に置いていた**(便 60 F8.1)。
> **★ upstream certificate として E-7 を入力する設計を選ぶ場合**は、**その proof ID を入力 schema に追加**し、**T-6 不一致は必ず `INTEGRITY_STOP`**。**`REJECT` と `INTEGRITY_STOP` の双方を割り当ててはならない。**
> **参考(混同しない)**: **$\lambda=c\mu^2$ は命題 S5-2**、**分岐型 $(5,2^21,2^21,5)$ と branch type は系 S5-2a**(便 60 F11)。

---

## 3. stage 2 述語(B5 — decision lane / audit lane の分離)

### 3.1 decision lane(数学的本線)

```text
E-1..E-6 fail           -> REJECT / precondition/*
E-1..E-6 pass, T-1 fail -> REJECT / a-partition-mismatch  |  REJECT / triple-root-of-a
E-1..E-6 pass, T-1 pass -> target branch signature is mathematically forced  (定理 N∞-criterion)
```

**T-1**: $\operatorname{rootpart}(a)=[2,2,1]$、すなわち
$$ \deg\gcd(a,a')=2,\qquad \gcd(a,a')\ \text{squarefree},\qquad \deg\gcd(a,a',a'')=0 \tag{9.3} $$

> **⇒ decision lane は E-1..E-6 + $\operatorname{rootpart}(a)$ だけ**(F13.2)。

### 3.2 audit lane(**T-1 通過後はすべて cross-check**)

| lane | 内容 |
|---|---|
| **audit A** | 二 chart の local differential → $C_{\rm crv}$ 上の ramification divisor $R$ → $\mu_*R$ |
| **audit B** | baseline multiplicity と saturation を**一般補題で証明した** saturated elimination |

**T-2 【B4・(60.5) 逐語】**
```text
d := monic_gcd(a, a')
assert  p divides a'
assert  a' = unit * p * d
assert  a'/p = unit * d
```
**T-3** $p$-locus の局所検査 / **T-4** Weierstrass locus / **T-5** 二 infinity($e=5$)/ **T-6** 有限 branch polynomial が degree 2 かつ even(sealed 検査・public は boolean)/ **T-7** $\sum(e_Q-1)=12$・有限 branch count $=2$・extra branch $=0$ / **T-8 【B5・F8.4】** searcher と checker が独立に作った**有限二 fiber の `aggregate_partition` を sealed 内で比較**:
$$ \texttt{finite aggregate partitions} = [[2,2,1],[2,2,1]] $$

### 3.3 **到達状態の一意化**(B5 の核)

> $$ \boxed{\ \text{T-1 通過後の不一致は}\ \textbf{すべて}\ \texttt{INTEGRITY\_STOP}\ } $$
> **理由**: T-1 が通れば定理 `N∞-criterion` により **target branch signature は数学的に強制される**。したがって T-2〜T-8 のいずれかが破れたなら、それは**紙上定理の誤りか実装の不一致**であって、**candidate の数学的 REJECT ではない**(便 60 F8.2・★教材 4)。
> **⚠ v2 の欠陥(自認)**: v2 は `REJECT / branch-pair-not-harmonic` と `INTEGRITY_STOP / swap-lemma-precondition` を**同じ到達状態**に割り当てており、**freeze できなかった**。**v3 は `branch-pair-not-harmonic` と `swap-lemma-precondition` を REJECT 側から削除**し、すべて `INTEGRITY_STOP` の下位 reason にした。
> **★ これにより elimination bug が candidate の数学的 REJECT に偽装されない**(F13.2)。

### 3.4 二次因子の while 全除去は引き続き禁止

searcher は **resultant を使わない**。checker が elimination を使う場合は **baseline multiplicity と saturation を一般補題として証明**し、**proof ID を certificate に束縛**する。

---

## 4. searcher / checker と divisor object(B6)

### 4.1 経路分離【便 60 F9.1 で PASS】

| | Searcher(audit A) | Checker(audit B) |
|---|---|---|
| 方法 | 二 chart の **local differential** から $R$ を構成し $\mu$ で pushforward | **証明済み baseline** の saturated elimination |
| 禁止 | resultant / 判別式を使わない | searcher の local / divisor helper を共有しない |
| **共有禁止(重要)** | **`N∞-swap` の結論も $a$-partition も両者の共通仮定にしない** | 同左 |

### 4.2 divisor equality をどう定義するか【B6・F9.2 の自己訂正を採用】

> **⚠ 「同じ divisor digest に到達する」だけでは数学的 divisor equality と同値でない**(便 60 F9.2): 基礎体と algebraic point / prime ideal の表現・affine/infinity chart の重複除去・Galois 共役成分の束ね方・multiplicity の表現・成分順序・canonical serialization と hash domain separator が**未定義**なら、**同じ divisor でも raw bytes が異なる**。

**v3 は次の 2 案を提示し、freeze 時にどちらかを選ぶ**(実装前に司令塔が裁定):

**案 (D-1) canonical object schema を規範化**
```text
divisor_object_schema_id
base_field_schema_id                  # 数体の表現(定義多項式 + 根の選択規約)
chart_ids + fixed projective coordinates
galois_stable_prime_ideals            # monic reduced Groebner basis
monomial_order_id                     # 固定
component_multiplicities
component_canonical_ordering          # 全順序を明示
canonical_byte_serialization_id
hash_algorithm + domain_separator
```
**二実装がそれぞれ canonicalize** し、その後で digest を比較する。

**案 (D-2) 第三の divisor-equality certificate**
raw digest 一致を**やめ**、**両者の divisor が等しいことを独立に証明する certificate**(例: 差の divisor が 0 であることの exact な証明書)を第三 artifact として出す。

> **本稿の推奨は (D-2)**。理由: (D-1) は canonicalization そのものが第三の実装になり、**その bug が両経路に共通して効く**(v2 が犯した「共通仮定の共有」と同型のリスク)。(D-2) は**等式の証明**を出すので presentation に依存しない。**ただし決定は司令塔。**

### 4.3 二層 freeze ID 束【F13.3】

```text
freeze_bundle = {
  predicate_theorem_id + digest        # 定理 N∞-criterion(+ 依存 4 補題)
  divisor_object_schema_id + digest    # (D-1) を採る場合
  divisor_equality_cert_schema_id      # (D-2) を採る場合
  public_certificate_schema_id + digest
  sealed_certificate_schema_id + digest
  reason_code_enum_id + digest
}
```
**divisor の raw bytes ではなく、この二層 ID を凍結する。**

---

## 5. certificate schema(B7)

### 5.1 public envelope(**pre-Freeze-2 に人間可視でよいもの**)

```text
candidate_ref              # random opaque(高 entropy・値の関数でない)
predicate_spec_freeze_id   # §4.3 の bundle ID
searcher_id + searcher_digest      # code/artifact identity(candidate 非依存)
checker_id  + checker_digest
verdict                    # ACCEPT | REJECT | INTEGRITY_STOP
reason_code                # §6 の閉じた enum

# --- 事前承認済みの数学的射影 5 欄(F10.1 の列挙どおり)---
finite_branch_count            # 2 を期待
finite_branch_pair_harmonic    # bool
a_root_partition               # [2,2,1] を期待
exceptional_locus_clear        # bool
ramification_sum               # 12 を期待
```

> **★ 「五欄のみ」の正しい意味**(便 60 F10.1 の erratum を反映): **公開する数学的射影が 5 欄**であって、**candidate/spec identity・verdict・reason まで消す意味ではない**。上の public envelope 全体が公開可能。

### 5.2 `SEALED_INTERNAL`(**pre-Freeze-2 は人間可視にしない**)

```text
SEALED_INTERNAL = {
  tuple_coefficients
  fibers[]                            # ← v2 は sealed の外だった(B7 で移動)
  fiber_refs[]                        # typed random-reference schema(下記)
  branch_values, finite_branch_polynomial
  finite_aggregate_partitions         # [[2,2,1],[2,2,1]](T-8)
  ramification_divisor_on_C           # object(digest ではなく object)
  branch_divisor_on_P1
  ramification_divisor_digest         # ← candidate 依存ゆえ sealed(B7)
  branch_divisor_digest               # ← 同上
  artifact_digests                    # integrity binding 用の unkeyed digest
  commitment = { hmac_of_tuple, key_holder="clean HMAC steward",
                 reveal_after="Freeze 2" }
}
```

### 5.3 typed random-reference schema【F10.1 の三語統一】

> v2 は `fiber_ref` / `fiber_id` / `branch_ref` の**三語**を混用していた。**自認。**
```text
opaque_ref = { kind: "candidate" | "fiber" | "branch",
               value: <high-entropy random>,   # 値の関数でない
               scope: "public" | "sealed" }
```
**public に出てよいのは `kind="candidate"` の 1 個のみ**。fiber / branch の ref は `SEALED_INTERNAL`。

### 5.4 二層 fiber 構造【F10.4-2 は v2 で対応済・維持】
```text
fibers = [ { fiber_ref, chart_components=[{chart_id, local_partition, degree},...],
             aggregate_partition } , ... ]      # すべて SEALED_INTERNAL
```

### 5.5 EP certificate extension【F10.1】
```text
EP_extension = {
  positive_control_scope = "same-schema, non-campaign-coefficients"
  ep_tuple_ref           # opaque_ref(kind="candidate")
  ep_verdict             # ACCEPT を期待
}
```

### 5.6 hash は concealment ではない【便 59 F11.3・維持】

deterministic digest を pre-Freeze-2 の人間可視に出さない。**sealed 区画の unkeyed digest は integrity binding にのみ使う。** 事前 commitment は **clean HMAC steward** が key を Freeze 2 後まで保持する。

---

## 6. reason code(閉じた enum・到達状態一意)

```text
# REJECT(decision lane のみ)
precondition/degree-mismatch     precondition/f6-not-monic
precondition/curve-not-squarefree precondition/pell-violation
precondition/leading-coeff-mismatch precondition/divisor-orientation
precondition/common-root
a-partition-mismatch             triple-root-of-a

# INTEGRITY_STOP(audit lane の不一致はすべてこちら)
pell-derivative-mismatch   p-locus-unhandled   weierstrass-unhandled
infinity-unhandled   chart-degree-mismatch   divisor-identity   rh-mismatch
branch-pair-not-harmonic          # ← v3 で REJECT から移動(B5)
extra-branch-value                # ← 同上
finite-branch-count-mismatch      # ← 同上
finite-partition-cross-mismatch   # ← T-8(F8.4)
divisor-equality-failure          # ← §4.2
digest-mismatch   checker-mismatch
sealed-field-leak   deterministic-digest-exposed
```
**未知の reason code は fail-closed。**

---

## 7. dependency-typed whitelist — $N_\infty$ 節(B9)

```text
rule: branch_value_square -> squareclass(C) -> P1
  semantic_quantity        = branch_value_square
  determines_prediction    = [P1]
  release_stage            = post-freeze2
  branch_scope             = N_infty
  # --- B9: squareclass の型を固定する ---
  prediction_base_field_id = K = Q(zeta_20)          # K5 window
  squareclass_quotient_id  = K^x / (K^x)^2
  minus_one_square_proof_id= "i = zeta_20^5 in K"    # -1 = i^2 in K^{x2}
  s5_4_infinity_dependency_id = "S5-4-infinity"      # c_hat = 1 => c_hat_mu alone fixes P1
  aliases_blocked = [branch_value, s^2, mu_norm_constant, C,
                     squareclass(C), sqfree(C), sign(C), h,
                     discriminant_leading_class,
                     sha256(branch_value), sha256(canonical_tuple),
                     any deterministic commitment of the above]
```

> **⚠ v2 の欠落(自認)**: v2 §7 は $[s^2]=[C]\in K^\times/K^{\times2}$(∵ $-1=i^2\in K^{\times2}$)を leakage edge の根拠にしながら、**$K$ をどこにも宣言していなかった**。**係数体 $\mathbb Q$ で読めば $-1$ は平方でなく、$s^2=-C$ から $[s^2]=[C]$ は一般には従わない**(便 60 F10.4)。**これは leakage 結論を弱める指摘ではなく、squareclass の型を固定する要求である。**
> **本正規形では $s^2=-C$(`N∞-swap`)、一般には $s^2=\pm C$。$K$ 上で $-1$ が平方なので、いずれにせよ $[s^2]=[C]$。**
> **`aliases_blocked` は列挙であって網羅ではない** — 新しい出力量を足す側に「それが $C$ の平方類を決めない」ことの**挙証責任**がある。

---

## 8. negative regression fixtures と役割分離(B8 の後半)

| neutral ID | 期待 verdict / reason | 期待 `a_root_partition` | 期待 alarm |
|---|---|---|---|
| `ninfty-neg-01` … `ninfty-neg-08` | **`REJECT / triple-root-of-a`** | `[3,1,1]` | `triple_gcd_degree>0`・`gcd_squarefree=false` |

- **raw shard 名・命名パターン・hit index・deterministic digest を本稿に書かない。** 対応は **quarantine / taint ledger の sealed mapping**。
- **用途分離**: 旧 hit を **genuine candidate の救済入力・順位付け入力にしない**。**quarantine された negative-test lane** で neutral ID の下に **searcher/checker 双方が同じ rejection mechanism を再現**するのは可。
- **回帰の合格条件(4 欄)**: `verdict` + `a_root_partition` + `triple_gcd_degree>0` + `gcd_squarefree=false`。
- **proof ID に含める事実**: **$p(0)\ne0$ かつ $f_6(0)\ne0$**(両方)。

### 8.1 **役割分離条項**【B8・便 60 F10.2】

> $$ \boxed{\ \text{negative-test lane runner}\ \ne\ \text{clean HMAC steward}\ } $$
> **旧 mapping(neutral ID ↔ raw shard/tuple)を知る tainted actor は clean HMAC steward になれない。** steward は commitment key を保持し Freeze 2 後に reveal する役であり、**候補値を推測できる立場にあってはならない**。
> **taint ledger に `role=negative_lane_runner` / `role=clean_hmac_steward` を別欄で記録**し、**同一 actor が両方を持たないことを機械的に検査**する。

### 8.2 証拠の射程【便 60 F10.2 の限定を明記】

> 便 60 は **raw 8 tuple と本稿の exact arithmetic を見ていない**。したがって紙上で受理されたのは **申告された boolean 間の機構整合**までであり、**8 件の数値計算は `cross-checked` に格上げされていない**。**本稿もそれ以上を主張しない。**

---

## 9. 機構一致の事前登録(維持)

### 9.1 8 fixtures(本稿 v2 で exact 検算・boolean のみ)

(Pell) 非零定数 / $f_6$ squarefree / $\gcd(a,p)=1$ / **$p\mid a'$** がすべて true、$\operatorname{ord}_0(a)=3$、$\deg\gcd(a,a')=2$、squarefree **false**、$\deg\gcd(a,a',a'')=1$ ⟹ **(9.3) 判定 false(全件 REJECT)**。

> **機構一致**: 旧経路の「$x=0$ に $e=3$」と新経路の「$a$ が $x=0$ で三重根」は**同一の局所機構**((N-pair-2) より有限二 fiber の分割 $=\operatorname{rootpart}(a)$)。**状態は `source-audited candidate`**(§8.2)。

### 9.2 EP【便 60 F10.3 で PASS】

```text
deg f6 = 6, deg a = 5, deg p = 2
f6 monic squarefree,  a5 = p2 != 0
same N_infty predicate schema
non-campaign coefficients
```
**EP 不在中の札は `partial predicate / UNKNOWN`。freeze 後も EP が出るまで `calibrated detector` / `complete search` と呼んではならない。**

---

## 10. 前件表の型列挙(★教材 T7 様式)

| # | 前件 | 型 | 状態 | 出所【B8 修正済】 |
|---|---|---|---|---|
| S-1 | $f_6$ monic squarefree・$\deg f_6=6$ | 凍結文 | 閉 | **S5-3∞** + 便 36 F2.1 |
| S-2 | $\deg a=5$・$\deg p=2$・$a_5=p_2\ne0$ | 凍結文 | 閉 | **S5-3∞** |
| S-3 | (Pell) | 凍結文 | 閉 | **S5-3∞** |
| S-4 | divisor orientation $(\mu)=5P_0-5P_\infty$ | 凍結文 | 閉 | **命題 S5-1**(+ S5-3∞ との同値) |
| S-5 | 分岐型 $(5,2^21,2^21,5)$ | 凍結文 | 閉 | **系 S5-2a** |
| S-6 | 有限 branch 値の調和対 $\{s,-s\}$ | 凍結文(**target condition**) | 閉 | **系 S5-2a** |
| S-7 | $\lambda=c\mu^2$(**本 spec は直接使わない**) | 凍結文 | 閉 | **命題 S5-2** |
| S-8 | $\hat c=1$ ⟹ $C$ 単独で (P1) | 凍結文 | 閉 | S5-4∞ |
| N-1 | `N∞-N`((60.1)(60.2)) | 導出 | **v3 で型修理・要監査** | 本稿 §1.2 |
| N-2 | `N∞-1:1`((60.3)(60.4)) | 導出 | **v3 で完成・要監査** | 本稿 §1.3 |
| N-3 | `N∞-fix` | 導出 | **便 60 F6.3 PASS** | 本稿 §1.4 |
| N-4 | **`N∞-pair`** | 導出(**新設**) | **要監査** | 本稿 §1.5 |
| N-5 | `N∞-swap` | 導出 | **便 60 F6.4 PASS**($j$-stability を v3 で明示) | 本稿 §1.6 |
| N-6 | `N∞-div`(+(60.5)) | 導出 | **便 60 F6.6 PASS** | 本稿 §1.7 |
| N-7 | **`N∞-criterion`**(iff) | 導出(**新設**) | **要監査** | 本稿 §1.8 |
| R-1 | while 全除去禁止 | 規約 | 閉 | 便 54 F6.2 |
| R-2 | branch-value-free public envelope・random opaque ID・HMAC | 規約 | 閉 | 便 59 F11.3・便 60 F10.1 |
| R-3 | **T-1 後の不一致はすべて `INTEGRITY_STOP`** | 規約 | 閉 | 便 60 F8.2 |
| R-4 | EP 不在中は `partial predicate / UNKNOWN` | 規約 | 閉 | 便 60 F10.3 |
| R-5 | fixture 用途分離・**役割分離**(runner ≠ steward) | 規約 | 閉 | 便 60 F10.2 |

---

## 11. 出所対応表(P56-1 5 欄)

| spec 条項 | 出所 | §・式番号 | 引用の型 | 状態 |
|---|---|---|---|---|
| §1.2 `N∞-N` | 便 60 | F6.1 (60.1)(60.2) | **逐語**(証明 artifact は本稿) | 要監査 |
| §1.3 `N∞-1:1` | 便 60 | F6.2 (60.3)(60.4) | **逐語**(証明は本稿で完成) | 要監査 |
| §1.4 `N∞-fix` | 便 60 | F6.3 | **PASS 済**(v2 から不変) | 承認済 |
| §1.5 `N∞-pair` | 便 60 | **F13.1** | **提案の採用 + 本稿で証明** | 要監査 |
| §1.6 `N∞-swap` | 便 60 | F6.4 | **PASS 済** + $j$-stability を本稿で明示 | 承認済(明示部は要監査) |
| §1.7 `N∞-div` | 便 60 | F6.6 (60.5) | **逐語** | 承認済 |
| §1.8 `N∞-criterion` | 便 60 | **F7.1 (60.6)・F7.2・F7.3** | **骨格の供与を受け本稿で証明を完成** | 要監査 |
| §2 入口/target 分離 | 便 60 | F8.1 | **逐語** | 凍結候補 |
| §2 出所 map | 便 60 | **F11** | **逐語**(S5-1/S5-2/S5-2a/S5-3∞) | 凍結候補 |
| §3 lane 分離・到達状態一意化 | 便 60 | F8.2・F13.2 | **逐語** | 凍結候補 |
| §3.2 T-2 | 便 60 | F8.3 (60.5) | **逐語** | 凍結候補 |
| §3.2 T-8 | 便 60 | F8.4 | **逐語** | 凍結候補 |
| §4.2 divisor equality | 便 60 | **F9.2**(自己訂正) | **逐語**(2 案の提示と推奨は本稿) | **司令塔裁定待ち** |
| §4.3 二層 freeze ID | 便 60 | F13.3 | **逐語** | 凍結候補 |
| §5 public/sealed 分離 | 便 60 | **F10.1**(erratum) | **逐語** | 凍結候補 |
| §7 whitelist 型 | 便 60 | **F10.4** | **逐語** | 凍結候補 |
| §8.1 役割分離 | 便 60 | F10.2 | **逐語** | 凍結候補 |
| §9 EP | 便 60 | F10.3 | **逐語** | 凍結候補 |

---

## 12. Sol への監査依頼(v3)

1. **【必須】定理 `N∞-criterion` の十分方向**(§1.8)。RH の「使い切り」の論法 — $4+4+2+2=12$ から**余分な ramification が存在しない**を出す段が、**$\bar{\mathbb Q}$ 上の議論として過不足ないか**(有限 branch value が $\bar{\mathbb Q}$ に住む点も含めて)。
2. **【必須】`N∞-pair` が target を仮定していないこと**(§1.5)。**依存の一方向性**(pair と swap が互いを使わない)を確認いただきたい。
3. **【必須】`N∞-N` の証明 artifact**(§1.2 の 3 段)。とくに **step 2 の「有限平坦射の norm と divisor の両立 $\operatorname{div}\circ N_\pi=\pi_*\circ\operatorname{div}$」**を、この設定($\pi$ は 2:1・$C_{\rm crv}$ は超楕円)で使ってよいか。**標準事実として引くなら §/定理番号が要るか。**
4. **【推奨】§4.2 の 2 案**。私は **(D-2) 第三の divisor-equality certificate を推奨**した(理由: (D-1) の canonicalization 自体が第三の実装になり、**その bug が両経路に共通して効く**)。**この見立てが正しいか。**
5. **【推奨】§3.3 の到達状態一意化**で、`branch-pair-not-harmonic` 等を **REJECT から INTEGRITY_STOP へ移した**こと。**decision lane に残す REJECT が `precondition/*` と `a-partition-mismatch` / `triple-root-of-a` だけでよいか。**
6. **【推奨】§7 の `prediction_base_field_id = K = Q(zeta_20)`**。**K5 window に固定してよいか**、それとも **spec を window 非依存にして $K$ を入力 field にすべきか。**

---

## 13. 実装着手の条件

$$ \boxed{\ \text{v3 の Sol 監査 PASS}\ \to\ \text{§4.3 の二層 freeze ID 束を発行}\ \to\ \text{searcher と checker を}\ \textbf{別々に}\ \text{実装}\ } $$

- **実装着手禁止は継続**(`implementation_status = NOT AUTHORIZED`)。
- **§4.2 の (D-1)/(D-2) は freeze 時に司令塔が裁定する。**
- **EP が揃うまで札は `partial predicate / UNKNOWN`。**
- **旧 8 hit は §8 の neutral lane でのみ使う。runner ≠ clean HMAC steward。**
