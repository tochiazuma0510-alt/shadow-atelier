# $N_\infty$ searcher v2 — **stage 2 fiber-partition 述語の仕様(spec v2)**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 70)。v1(`docs/week4-NInfty_stage2_spec_v1.md`・digest `77ed7131…`)は便 59 Part B で差戻し。本稿は P59-B1〜B7 を反映した再提出版。**
**身分**: **spec 草案・Sol 監査前・実装着手禁止(継続)**。freeze ID は v2 PASS 後に F12 様式で発行(`supersedes_draft = 77ed7131…`)。
**正典**: `sol/sol_reply_59_znorm_ninfty.md` **F5–F14**(差戻し理由と設計指定)・`sol/sol_reply_54_event_candidates.md` F6/F9/F12(v1 の骨格)・`docs/week4-K5_S5設計_opus_v1.md` **命題 S5-1 / S5-2 / S5-2a / §3.3.5 S5-3∞**・**便 36 F2.1**・`docs/week4-K5_Rule1_v1_4.md`(operative)。
**接触規律**: **本稿は値に依存しない。** $\hat c_\mu$・$C$・$h$・$a_5$・leading coefficient・平方類・符号・分岐値・具体係数を**一切書いていない**。§4 の negative fixture は **neutral ID のみ**で参照する(raw shard 名・digest は sealed mapping へ退避 — P59-B6)。本稿で行った機械計算は**檢分用の boolean 出力のみ**(§1.7)。

---

## 0. v1 → v2 差分(P59-B1〜B7)

| ID | v1 | v2 | 出所 |
|---|---|---|---|
| **B3(最重要)** | 補題 N∞-L で **$\iota$-固定性を主張**し $s^2=\hat c_\mu$ と結論 | **撤回**。$x$-root と $C$ 上 ramification point を混同し、**swapped orbit の寄与を半分落としていた**(RH 12 は swapped でちょうど整合)。**一般結論は $s^2=\pm\hat c_\mu$**。さらに **F8.3 を独立に検分して成立を確認**し、**補題 N∞-swap** として独立命題化($s^2=-\hat c_\mu$)。**自認** | 便 59 F8.1–F8.3・F13.1 |
| **B4** | §2.3 で $w^2=\hat c_\mu,\ v=w$(**fixed**)を強制 → §2.4 で非退化 gcd 判定(**内部矛盾**) | **撤回**。**swapped 下の簡約 $H_{\pm s}=\mp2s\,a$** に置換し、判定を **$a$ 一本の (9.3)** + **$p\mid a'$** + 局所検査 + 調和 boolean + RH 12 に | 便 59 F9 |
| **B1** | 入口契約に monic・$a_5=p_2\ne0$・divisor orientation・調和条件が無い | **入口契約 E-1〜E-7 に復元**。出所を S5-1/S5-2/**S5-2a**/S5-3∞+便 36 F2.1 に精密化 | 便 59 F5 |
| **B2** | 補題 N∞-F が「1:1」を**全称**で主張 | **2 つに分割**: **N∞-N(norm/pushforward)**(常に成立)+ **系 N∞-1:1**($v^2\ne\hat c_\mu$ でのみ)。**fixed fiber は局所 divisor 直接計算へ** | 便 59 F6・F14-1 |
| **B5** | searcher を「divisor 経路」と呼びつつ §2.3 で $\mathrm{Res}_x$ 使用・両者が N∞-L を共有 | **真の別経路**: searcher = **$C$ 上二 chart の local expansion から ramification divisor を構成し $\mu$ で pushforward** / checker = **baseline multiplicity と saturation を一般補題で証明した elimination**。**ramification divisor を第一 object 化** | 便 59 F10.1・F13.3 |
| **B6** | raw shard 名(**符号を符号化**)・deterministic digest を人間可視・schema 不整合 5 点・fixture 用途矛盾・EP の次数 | **neutral ID `ninfty-neg-01..08`**・**random opaque ID + clean steward の HMAC**(deterministic digest は pre-Freeze-2 に出さない)・**branch-value-free certificate**・schema 5 点修理・**用途分離**(救済入力禁止 / neutral lane 再現は可)・**EP は same schema / non-campaign coefficients** | 便 59 F10.2–F10.4・F11.2・F11.3・F13.2 |
| **B7** | — | **修理版 EP と 8 fixture の機構一致を実装前に事前登録**(§9) | 便 59 F12 |

> **v2 の状態札**: `spec draft v2 / single-mathematician / 未監査`。**§1 の N∞-N・N∞-1:1・N∞-swap は要監査**(N∞-swap は Sol F8.3 の独立検分として本稿で確認したが、**二人目の検算は未了**)。

---

## 1. 数学的基礎

### 1.1 設定(すべて S5 / Rule 1 の凍結文)

$$ C:\ y^2=f_6(x),\ \deg f_6=6,\ f_6\ \text{monic squarefree};\qquad \mu=a(x)+p(x)y,\ \deg a=5,\ \deg p=2 $$
$$ \textbf{(Pell)}\quad N(\mu)=\mu\mu^\iota=a^2-f_6p^2=\hat c_\mu\in\mathbb Q^\times,\qquad \textbf{(Norm-or)}\quad (\mu)=5P_0-5P_\infty $$
$$ \textbf{(S5-2)}\quad \text{分岐型}\ (5,\,2^21,\,2^21,\,5),\qquad \textbf{(S5-2a)}\quad \text{有限分岐値は調和対}\ \{s,-s\} $$

$\iota$ は超楕円対合、$j(v):=\hat c_\mu/v$ は $\mu^\iota=\hat c_\mu/\mu$ が誘導する $\mathbb P^1$ 上の対合。

> **$\gcd(a,p)=1$** は (Pell) から自動(共通根があれば $\hat c_\mu=0$)。

### 1.2 補題 N∞-N(norm / pushforward)【本稿発・要監査】

> **補題 N∞-N.** 任意の $v\in\mathbb P^1\smallsetminus\{0,\infty\}$ に対し
> $$ H_v(x):=(v-a)^2-p^2f_6=v^2-2v\,a(x)+\hat c_\mu \tag{N-1} $$
> は $\mu^{-1}(v)$ の **$x$-line への pushforward(= norm)** を定める。すなわち
> $$ \operatorname{div}(H_v)\ =\ \pi_*\bigl(\mu^{-1}(v)\bigr),\qquad \pi:C\to\mathbb P^1_x. $$

**証明.** $\mu=v$ は $py=v-a$。2 乗して $y^2=f_6$ を使うと $p^2f_6=(v-a)^2$、すなわち $H_v(x)=0$。第 2 の等号は展開して (Pell) を代入するのみ。$\deg_xH_v=5=\deg\mu$($v\ne0$ で $\mathrm{lc}=-2v\,a_5\ne0$)。$\pi$ は 2:1 なので、**同じ $x$ 座標上の共役点 $Q,\iota Q$ が同時に fiber に入る場合、両者は $H_v$ の同一の根の重複度へ合算される**。∎

> **⚠【v2・B2】v1 の誤り(自認)**: v1 の補題 N∞-F は「根と fiber が**重複度込みで 1:1**」と**全称で**主張した。**これは偽**である — 上記のとおり $H_v$ は fiber ではなく **fiber の押し出し**であり、$Q$ と $\iota Q$ が両方 fiber に入る場合(= fixed case)は 2 点が 1 根に潰れる(便 59 F14-1)。

### 1.3 系 N∞-1:1(1:1 が成り立つ十分条件)【本稿発・要監査】

> **系 N∞-1:1.** $v^2\ne\hat c_\mu$ ならば $\pi|_{\mu^{-1}(v)}$ は**単射**であり、$\mu^{-1}(v)$ の multiplicity partition は $H_v$ の根の multiplicity partition に一致する。さらに $v\ne0$ なら
> $$ H_v=-2v\bigl(a(x)-w\bigr),\qquad w:=\frac{v^2+\hat c_\mu}{2v}. \tag{N-2} $$

**証明.** $Q=(x_0,y_0)$ と $\iota Q=(x_0,-y_0)$ が**ともに** $\mu^{-1}(v)$ に入るとする。$\mu(Q)+\mu(\iota Q)=2a(x_0)=2v$ かつ $\mu(Q)\mu(\iota Q)=N(\mu)(x_0)=\hat c_\mu$、よって $v^2=\hat c_\mu$。対偶が主張。$Q$ が $\iota$-固定($y_0=0$)なら $\mu(Q)=a(x_0)$ で同じく $\mu(Q)^2=a(x_0)^2=\hat c_\mu+f_6p^2$… の代わりに直接 $\mu(Q)\mu^\iota(Q)=\mu(Q)^2=\hat c_\mu$。いずれも $v^2=\hat c_\mu$。∎

> **⇒ 判定の分岐**: $v^2\ne\hat c_\mu$(**non-fixed**)では (N-2) の $a-w$ の重複度で決まる。$v^2=\hat c_\mu$(**fixed**)では **(N-2) を使ってはならない** — §1.4 の局所計算による。

### 1.4 命題 N∞-fix(fixed fiber の局所構造)【本稿発・要監査】

> **命題 N∞-fix.** $v^2=\hat c_\mu$ とする。fiber $\mu^{-1}(v)$ の全点は $\{py=0\}$ にあり、$a(x_0)=v$。各点の分岐指数は
> $$ \text{(i) } y_0=0,\ p(x_0)\ne0:\ e=1;\qquad \text{(ii) } p(x_0)=0,\ y_0\ne0:\ e=m:=\operatorname{ord}_{x_0}(p);\qquad \text{(iii) } p(x_0)=y_0=0:\ e=2m+1\ (\textbf{奇数}). $$

**証明.** $\mu(Q)=v$ かつ $\mu^\iota(Q)=\hat c_\mu/v=v$ を引き算して $2p(x_0)y_0=0$、足して $a(x_0)=v$。
**(i)**: $f_6(x_0)=0$ で $y$ が uniformizer、$\operatorname{ord}_Q(x-x_0)=2$。$\operatorname{ord}_Q(a-v)=2\operatorname{ord}_{x_0}(a-v)\ge2$、$\operatorname{ord}_Q(py)=1$。ゆえに $\operatorname{ord}_Q(\mu-v)=1$。
**(ii)**: $f_6(x_0)\ne0$ で $x$ が uniformizer。(Pell) より $(a-v)(a+v)=a^2-\hat c_\mu=f_6p^2$、$a(x_0)+v=2v\ne0$ ゆえ $\operatorname{ord}_{x_0}(a-v)=2m$。$\operatorname{ord}_{x_0}(py)=m<2m$ より $e=m$。**$Q$ と $\iota Q$ の双方**が fiber に属し、それぞれ $e=m$。
**(iii)**: $y$ が uniformizer、$\operatorname{ord}_Q(p)=2m$、$\operatorname{ord}_Q(py)=2m+1$。$\operatorname{ord}_{x_0}(f_6p^2)=1+2m$ ゆえ $\operatorname{ord}_{x_0}(a-v)=2m+1$、$\operatorname{ord}_Q(a-v)=4m+2>2m+1$。よって $e=2m+1$。∎

### 1.5 **補題 N∞-swap**(便 59 F8.3 の独立検分 → 独立命題化)【**本稿で検分・成立**】

> **補題 N∞-swap.** $N_\infty$ Pell 正規形($\deg p=2$・$f_6$ squarefree)で、**有限 branch fiber が二つとも $[2,2,1]$** かつ **branch pair が $\{s,-s\}$**(S5-2a)ならば、対合 $j$ は二値を**交換**し
> $$ \boxed{\ j(s)=-s,\qquad s^2=-\hat c_\mu.\ } $$

**証明(本稿による独立再構成).**
$\{s,-s\}$ が $j$-安定なので **fixed case**($j(s)=s$, $j(-s)=-s$ ⟹ $s^2=\hat c_\mu$)か **swapped case**($j(s)=-s$ ⟹ $s\cdot(-s)=\hat c_\mu$ ⟹ $s^2=-\hat c_\mu$)のいずれか。
**fixed case を排除する。** 命題 N∞-fix より、fixed fiber の点が $e=2$ をもつのは **(ii) で $m=2$** のときに限る((i) は $e=1$、(iii) は $e$ 奇数)。$m=2$ かつ $\deg p=2$ ならば $p=p_2(x-x_0)^2$ で、**$p$ の double root は唯一**。よって $e=2$ の点をもつ fixed fiber は $v=a(x_0)$ の**ただ 1 つ**である。ところが fixed case では $s$ と $-s$ の**双方**が $[2,2,1]$ を要求し、双方が $e=2$ 点をもたねばならない。$a(x_0)$ は $s$ と $-s$ の**一方にしかなれない**($s\ne0$)。矛盾。∎

> **★ 検分の結論**: **Sol の F8.3 は正しい**(本稿で独立に再構成し、(i)(ii)(iii) の場合分けが exhaustive であること・$\deg p=2$ が double root を一つしか許さないことを確認した)。**鵜呑みにしていない** — 各分岐指数を uniformizer の取り方まで含めて再導出した(§1.4 の証明)。
> **★ v1 の誤りの正体(自認)**: v1 §1.5 は「二値が互いに移り合うと $a'$ の 4 根を 2 根しか消費できない」と数えたが、**swapped case では同じ 2 つの $x$-root が二つの共役 fiber で 4 つの ramification point を担う**ので $\sum(e-1)=2+2=4$ となり、RH の 12 に**ちょうど整合する**。**$x$-root と $C$ 上の ramification point を混同していた**(便 59 F8.1・F14-3)。
> **★ leakage の正しい根拠**: 一般には $s^2=\pm\hat c_\mu$、本正規形では $s^2=-\hat c_\mu$。**いずれにせよ $-1=i^2\in K^{\times2}$ より $[s^2]=[\hat c_\mu]\in K^\times/K^{\times2}$** ⟹ 平方類が (P1) を決める(S5-4∞)。**符号を $+$ に固定してはならない**(便 59 F8.2)。**便 54 F12.4 は元から $\pm$ と述べており、v1 の「同内容」という provenance は誤りだった。自認。**

### 1.6 系 N∞-red(swapped 下の簡約)【便 59 F9.2 の採用・本稿で再検算】

補題 N∞-swap より $s^2=-\hat c_\mu$ なので (N-1) から
$$ \boxed{\ H_{s}=-2s\,a(x),\qquad H_{-s}=+2s\,a(x)\ } \tag{9.1} $$
さらに $a(x_0)=0$ なら (Pell) より $p(x_0)^2f_6(x_0)=-\hat c_\mu=s^2\ne0$、すなわち **$p(x_0)\ne0$ かつ $f_6(x_0)\ne0$**。ゆえに両有限 fiber は**自動的に非退化 locus** にあり、系 N∞-1:1 が適用でき
$$ \boxed{\ \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=\operatorname{rootpart}(a).\ } \tag{9.2} $$

> **⇒ 判定は $\mathbb Q$ 係数の多項式 $a$ 一本**で閉じる(**algebraic な $w$ の列挙が不要**)。

### 1.7 補題 N∞-div($p\mid a'$)【便 59 (9.4)・本稿で再検算】

(Pell) を微分して $2aa'=p(f_6'p+2f_6p')$。$\gcd(a,p)=1$ より $p\mid a'$。$\deg a'=4$、$\deg p=2$ ゆえ $a'=p\cdot r$、$\deg r=2$。

> **系**: $a$ の root partition が $[2,2,1]$、$a=a_5(x-\alpha)^2(x-\beta)^2(x-\gamma)$ なら $a'=a_5(x-\alpha)(x-\beta)g$、$\deg g=2$。$\gcd(a,p)=1$ ゆえ $p$ は $\alpha,\beta$ を根にもてず、**$p\doteq g$**。すなわち **$a'$ の残り 2 根はちょうど $p$-locus**(便 59 F9.2 と一致・本稿で独立確認)。

> **本稿で行った機械計算(boolean 出力のみ)**: 隔離済み 8 tuple について **(Pell) 定数性・$f_6$ squarefree・$\gcd(a,p)=1$・$p\mid a'$・$\operatorname{ord}_0(a)$・$\deg\gcd(a,a')$・squarefree 性・$\deg\gcd(a,a',a'')$・partition 判定**を exact 有理演算で確認した。**係数・値は一切出力していない。** 結果は §9。

---

## 2. 入口契約(P59-B1)

**すべて満たさなければ `REJECT / precondition/*`。**

| # | 条件 | 出所 |
|---|---|---|
| **E-1** | $\deg f_6=6$・**$f_6$ monic**・**squarefree** | S5-3∞ / 便 36 F2.1 |
| **E-2** | $\deg a=5$・$\deg p=2$ | S5-3∞ |
| **E-3** | **$a_5=p_2\ne0$**(leading coefficient の一致・gauge) | S5-3∞ |
| **E-4** | **(Pell)** $a^2-f_6p^2$ が非零定数 | S5-3∞ |
| **E-5** | **divisor orientation** $(\mu)=5P_0-5P_\infty$($P_0$/$P_\infty$ の役割を取り違えない) | S5-2 / Rule 1 §1.2 |
| **E-6** | $\gcd(a,p)=1$(E-4 から自動だが独立に assert) | 本稿 §1.1 |
| **E-7** | **調和条件**: 有限 branch 値集合が $\{s,-s\}$(= $B_{\rm fin}(V)=V^2-\sigma$ の形) | **S5-2a** |

> **★ E-7 は passport から出ない**(便 59 F14-2): 分岐型 $(5,2^21,2^21,5)$ だけでは $\{0,s,-s,\infty\}$ の調和条件は復元されない。**独立の入口条件として明記する。**

---

## 3. stage 2 述語(P59-B4 — swapped 経路)

**入力** $(a,p,f_6)$ → **出力** verdict $\in\{\texttt{ACCEPT},\texttt{REJECT},\texttt{INTEGRITY\_STOP}\}$ + reason code + §5 の certificate。

### 3.1 判定手順

| 段 | 内容 | 失敗時 |
|---|---|---|
| **T-0** | 入口契約 E-1〜E-6 | `REJECT / precondition/*` |
| **T-1** | **$a$ の root partition が $[2,2,1]$**: $$\deg\gcd(a,a')=2,\quad \gcd(a,a')\ \text{squarefree},\quad \deg\gcd(a,a',a'')=0 \tag{9.3}$$ | `REJECT / a-partition-mismatch`(**$a$ が三重根をもつ場合は `REJECT / triple-root-of-a`**) |
| **T-2** | **$p\mid a'$**(補題 N∞-div)かつ $a'/p$ が $\doteq p$ でない場合の整合(§1.7 系) | `INTEGRITY_STOP / pell-derivative-mismatch` |
| **T-3** | **$p$-locus の局所検査**: $p$ の各根 $x_0$ 上の $C$ 上 2 点で $e$ を局所展開で決定 | `INTEGRITY_STOP / p-locus-unhandled` |
| **T-4** | **Weierstrass locus の局所検査**: $f_6$ の各根上の点で $y$ を uniformizer として $e$ を決定 | `INTEGRITY_STOP / weierstrass-unhandled` |
| **T-5** | **二 infinity の局所検査**: $x=\infty$ chart で $P_0,P_\infty$ の $e=5$ を assert | `INTEGRITY_STOP / infinity-unhandled` |
| **T-6** | **調和 boolean**: 有限 branch polynomial が $B_{\rm fin}(V)=V^2-\sigma$(degree 2 かつ even)。**sealed に検査**し、人間可視には `finite_branch_pair_harmonic` のみ | `REJECT / branch-pair-not-harmonic` |
| **T-7** | **RH 合算** $\sum_Q(e_Q-1)=12$・有限 branch count $=2$・余分な branch $=0$ | `REJECT / extra-branch-value` / `INTEGRITY_STOP / rh-mismatch` |

$$ \boxed{\ \texttt{ACCEPT}\iff \text{T-0}\wedge\text{T-1}\wedge\text{T-2}\wedge\text{T-3}\wedge\text{T-4}\wedge\text{T-5}\wedge\text{T-6}\wedge\text{T-7}\ } $$

> **★ 撤回した設計(自認)**: v1 §2.3 は $w^2=\hat c_\mu,\ v=w$(= **fixed case**)を強制しながら、直後の §2.4 で **non-exceptional な $a-w$ の gcd 判定**を適用していた。命題 N∞-fix より fixed fiber は全点が exceptional locus($py=0$)にあるので、**この 2 段は同時に成り立たない**(便 59 F9.1)。**v2 は swapped 経路に一本化した。**
> **★ fixed 枝の扱い**: 補題 N∞-swap により、**target(二 fiber とも $[2,2,1]$ + 調和対)では fixed case は起こりえない**。したがって v2 は fixed 枝を**判定の分岐として持たない**。ただし **T-1 が通ったのに T-6 が「調和でない」と出た**場合は前提が崩れているので `INTEGRITY_STOP / swap-lemma-precondition`(補題の適用外を黙って通さない)。

### 3.2 二次因子の while 全除去は引き続き禁止

**`stripKnownQuadraticFactor` 型の `while` 除去を禁止する。** v2 の第一経路(searcher)は **resultant を使わない**(§4)。checker が elimination を使う場合は **baseline multiplicity と saturation を一般補題として証明し、proof ID を certificate に束縛**する。

---

## 4. searcher / checker の真の別経路(P59-B5)

| | **Searcher(第一経路)** | **Checker(独立照合器)** |
|---|---|---|
| 対象 | **$C$ 上の ramification divisor** | **同じ divisor**(digest 一致を要求) |
| 方法 | 二 chart($x$-affine / $x$-infinity)で **$d\mu$ の局所展開**から $R=\sum_Q(e_Q-1)Q$ を直接構成し、**$\mu$ で pushforward** して branch divisor を得る | **saturated elimination**: baseline multiplicity と saturation を**一般補題で証明した上で** discriminant/resultant を使う |
| 禁止 | resultant / 判別式を**使わない** | searcher の local / divisor helper を**共有しない** |
| 共有禁止 | **補題 N∞-swap の帰結を「仮定」として共有しない** — checker は $[2,2,1]$ を fiber から独立に再計算する | 同左 |

> **ramification divisor を第一 object にする**(便 59 F13.3):
> ```text
> ramification_divisor_on_C        # digest
> branch_divisor_on_P1             # digest
> fiber_decomposition_by_branch_ref
> ```
> **searcher は local differential、checker は saturated elimination で同じ divisor digest に到達する。** 「resultant の指数」と「fiber partition」の**再融合を schema が防ぐ**。

> **⚠ v1 の設計欠陥(自認)**: v1 は searcher を「resultant を使わない divisor 経路」と呼びながら §2.3 で $\mathrm{Res}_x(a-W,a')$ を使い、さらに**両経路が偽の N∞-L と critical-value reduction を共有**していた。**共通の predicate bug を独立に見逃す構成**だった(便 59 F10.1)。

---

## 5. certificate schema(P59-B6 — branch-value-free)

```text
schema              = "mb/ninfty-fiber-partition/v2"
candidate_ref                      # random opaque ID(高 entropy・値の関数でない)
predicate_spec_freeze_id           # 本 spec の freeze ID(§10)
searcher_id, searcher_digest
checker_id,  checker_digest
verdict                            # ACCEPT | REJECT | INTEGRITY_STOP
reason_code                        # §6 の閉じた enum

# --- 人間可視(pre-Freeze-2)はこの 5 欄のみ(便 59 F13.2)---
finite_branch_count                # 2 を期待
finite_branch_pair_harmonic        # bool
a_root_partition                   # [2,2,1] を期待
exceptional_locus_clear            # bool(p-locus / Weierstrass / infinity すべて処理済)
ramification_sum                   # 12 を期待

# --- 二層の fiber 構造(F10.4-2)---
fibers = [
  { fiber_id,
    chart_components = [ { chart_id, local_partition, degree } , ... ],
    aggregate_partition,
    branch_ref                     # random opaque(SEALED mapping 経由)
  }, ...
]

# --- ramification divisor(第一 object・F13.3)---
ramification_divisor_on_C_digest
branch_divisor_on_P1_digest

# --- sealed 区画(pre-Freeze-2 は人間可視にしない)---
sealed = {
  tuple_coefficients, branch_values, finite_branch_polynomial,
  artifact_digests                 # integrity binding 用の unkeyed digest
  commitment = { hmac_of_tuple, key_holder = "clean steward", reveal_after = "Freeze 2" }
}
```

### 5.1 **hash は concealment ではない**(便 59 F11.3 — Sol 自己訂正の反映)

> **【禁止】** `candidate_id = sha256(canonical tuple)` や `branch_value_digests = sha256(branch value)` を **pre-Freeze-2 の人間可視に出すこと**。
> **理由**: bound $\le5$ の**有限な探索宇宙**では **dictionary attack が可能**であり、deterministic digest は**値の別名**になる。さらに branch value は canonical algebraic-number serialization・共役の順序・基礎体表現が未定義で、**再現可能な digest にすらなっていない**。
> **【正しい分離】**
> - **sealed 区画**: unkeyed artifact digest を保持し **integrity binding** に使う。
> - **人間可視**: **高 entropy の random opaque `candidate_ref` / `fiber_ref` のみ**。
> - **事前 commitment が要るとき**: **clean steward が secret nonce / HMAC key を Freeze 2 後まで保持**し、reveal 時に binding を検証する。
> - **branch value の deterministic digest は pre-Freeze-2 に出さない。**
> **⇒ dependency audit は量そのものだけでなく、その deterministic commitment にも適用する。**
> **★ v1 の誤り(自認)**: v1 §3・§4 は `candidate_id`・`tuple digest`・`branch_value_digests` を**人間可視の同一性 ID として設計**していた。**上の理由で不可。**

---

## 6. reason code(閉じた enum・prefix を統一 — F10.4-1)

```text
# REJECT
precondition/degree-mismatch      precondition/f6-not-monic
precondition/curve-not-squarefree precondition/pell-violation
precondition/leading-coeff-mismatch precondition/divisor-orientation
precondition/common-root
a-partition-mismatch   triple-root-of-a
branch-pair-not-harmonic   extra-branch-value   finite-branch-count-mismatch

# INTEGRITY_STOP
pell-derivative-mismatch   p-locus-unhandled   weierstrass-unhandled
infinity-unhandled   chart-degree-mismatch   divisor-identity   rh-mismatch
swap-lemma-precondition   digest-mismatch   checker-mismatch
sealed-field-leak   deterministic-digest-exposed
```
**未知の reason code は fail-closed。**

---

## 7. dependency-typed whitelist — $N_\infty$ 節

```text
rule: branch_value_square -> squareclass(c_hat_mu) -> P1
  semantic_quantity      = branch_value_square
  determines_prediction  = [P1]
  release_stage          = post-freeze2
  branch_scope           = N_infty
  aliases_blocked        = [branch_value, s^2, mu_norm_constant, c_hat_mu,
                            squareclass(c_hat_mu), sqfree(c_hat_mu), sign(c_hat_mu),
                            h, discriminant_leading_class,
                            sha256(branch_value), sha256(canonical_tuple),
                            any deterministic commitment of the above]
```

> **根拠**: 補題 N∞-swap(§1.5)より $s^2=-\hat c_\mu$、一般には $s^2=\pm\hat c_\mu$。**いずれにせよ $[s^2]=[\hat c_\mu]$**(∵ $-1\in K^{\times2}$)。S5-4∞ より $\hat c_\mu$ 単独で (P1) が決まる。
> **`aliases_blocked` は列挙であって網羅ではない** — **新しい出力量を足す側に「それが $\hat c_\mu$ の平方類を決めない」ことの挙証責任**がある。**deterministic commitment も同じ規則の対象**(§5.1)。

---

## 8. negative regression fixtures(P59-B6 — neutral ID)

| neutral ID | 期待 verdict / reason | 期待 `a_root_partition` | 期待 alarm |
|---|---|---|---|
| `ninfty-neg-01` … `ninfty-neg-08` | **`REJECT / triple-root-of-a`** | `[3,1,1]` | `gcd_squarefree=false`・`triple_gcd_degree>0` |

- **raw shard 名・hit index・deterministic digest は本稿に書かない。** 対応は **quarantine / taint ledger の sealed mapping** に置く(便 59 F11.2: **旧 shard の命名規約は $a_5$ と $p$ の符号を名前に符号化しており**、「fixture 名に値・符号を含めない」規則と両立しない — **その命名パターン自体を本稿に転記しない**)。**v1 の §4 表(raw shard 名 + index + digest を人間可視の表として掲載)は撤回。自認。**
- **用途の分離**(便 59 F10.2):
 - **禁止**: 旧 hit を **genuine candidate の救済入力・順位付け入力**にすること。
 - **許可**: **quarantine された negative-test lane** で、**neutral fixture ID の下に** searcher/checker 双方が**同じ rejection mechanism を再現**すること。
- **回帰の合格条件(4 欄)**: `verdict` + `a_root_partition` + `triple_gcd_degree>0` + `gcd_squarefree=false`(F10.2 の推奨を採用)。
- **proof ID に含める事実**: 便 54 F6 が確認した **$p(0)\ne0$ かつ $f_6(0)\ne0$**(**両方** — v1 は $p(0)\ne0$ しか再掲せず、N∞-N の Weierstrass 例外を閉じていなかった。**自認**)。

---

## 9. 機構一致の事前登録(P59-B7)

**実装前に、本 spec と分離して次を事前登録する。**

### 9.1 8 negative fixtures の機構(**本稿で exact 検算・boolean のみ**)

| 検査項目 | 8 件すべての結果 |
|---|---|
| (Pell) が非零定数 | **true** |
| $f_6$ squarefree | **true** |
| $\gcd(a,p)=1$ | **true** |
| **$p\mid a'$**(補題 N∞-div) | **true** |
| $\operatorname{ord}_0(a)$ | **3(= $a$ が $x=0$ で三重根)** |
| $\deg\gcd(a,a')$ | **2** |
| $\gcd(a,a')$ squarefree | **false** |
| $\deg\gcd(a,a',a'')$ | **1**($>0$) |
| **(9.3) の $[2,2,1]$ 判定** | **false(全件 REJECT)** |

> **★ 機構一致の確認**: **旧経路(便 54 F6)の棄却理由「$x=0$ に $e=3$ の真分岐」と、新経路(9.3)の棄却理由「$a$ が $x=0$ で三重根」は同一の現象**である。実際 (9.2) より有限二 fiber の分割は $\operatorname{rootpart}(a)$ に一致し、$\operatorname{ord}_0(a)=3$ は partition $[3,1,1]$ を意味する。**旧 $a'=\epsilon5x^2p$ の観測とも整合**($\operatorname{ord}_0(a')=2$)。
> **⇒ v2 は旧 8 件を同じ機構で棄却する。** ただし **reason code は `triple-root-of-a` へ改称**(v1 の `triple-fiber-at-x0` は fiber 語彙で、新経路の対象($a$ の根)と型が合わない)。

### 9.2 EP(end-to-end positive control)の条件(便 59 F10.3)

> **EP は「same schema / non-campaign coefficients」でなければならない。**
> ```text
> deg f6 = 6,  deg a = 5,  deg p = 2
> f6 monic squarefree,  a5 = p2 != 0
> same N_infty predicate schema
> ```
> **次数そのものを変えた例は P-1 で REJECT されるので calibration にならない**(v1 の「別の $(f_6,\deg)$ 設定」は**誤り。自認**)。
> **EP は本番 tuple であってはならない。** certificate に `positive_control_scope = "same-schema, non-campaign-coefficients"` を明記。
> **EP が 1 件も無い間、探索器の札は `partial predicate / UNKNOWN`。**

---

## 10. schema / 相互参照の修理(F10.4 の 5 点)

| # | v1 の不整合 | v2 |
|---|---|---|
| 1 | reason code が §2.0(`degree-mismatch`)と §7(`precondition/degree-mismatch`)で不一致 | **`precondition/*` に統一**(§6) |
| 2 | `fibers[]` が branch fiber と chart component を同一行に潰す | **二層化**: `fiber_id → chart_components[] → aggregate_partition`(§5) |
| 3 | `predicate_spec_id` の参照先を「§8」としたが §8 は whitelist で freeze ID の定義が無い | **`predicate_spec_freeze_id`** を導入し、**定義を §10 本節**に置く。freeze ID は **v2 PASS 後に F12 様式で発行**(`supersedes_draft = 77ed7131…`) |
| 4 | §2.1 の checker 参照「§5」は実際には §6 | **§4(searcher/checker)へ統一** |
| 5 | §10 の条件番号が本文 §2.3/§2.4 とずれ | **T-0〜T-7 の単一体系**に統一(§3.1) |

---

## 11. 前件表の型列挙(★教材 T7 様式)

| # | 前件 | 型 | 状態 | 用途 |
|---|---|---|---|---|
| S-1 | $C:y^2=f_6$・$\deg f_6=6$・monic squarefree | 凍結文(S5-3∞ / 便 36 F2.1) | 閉 | E-1 |
| S-2 | $\mu=a+py$・$\deg a=5$・$\deg p=2$・$a_5=p_2\ne0$ | 凍結文(S5-3∞) | 閉 | E-2・E-3 |
| S-3 | (Pell) | 凍結文(S5-3∞) | 閉 | E-4・§1.2・§1.7 |
| S-4 | $(\mu)=5P_0-5P_\infty$(orientation 込み) | 凍結文(S5-2 / Rule 1 §1.2) | 閉 | E-5・T-5 |
| S-5 | 分岐型 $(5,2^21,2^21,5)$ | 凍結文(S5-2) | 閉 | T-7 |
| **S-6** | **有限 branch 値が調和対 $\{s,-s\}$** | **凍結文(S5-2a)** | 閉 | **E-7・T-6・補題 N∞-swap の前件** |
| S-7 | $\hat c=1$ ゆえ $\hat c_\mu$ 単独で (P1) が決まる | 凍結文(S5-4∞) | 閉 | §7 |
| **N-1** | **補題 N∞-N**(norm/pushforward) | **導出(本稿発)** | **未監査** | §1.2 |
| **N-2** | **系 N∞-1:1** | **導出(本稿発)** | **未監査** | §1.3 |
| **N-3** | **命題 N∞-fix**(fixed fiber の局所構造) | **導出(本稿発)** | **未監査** | §1.4・補題 N∞-swap |
| **N-4** | **補題 N∞-swap** | **Sol F8.3 の独立検分**(本稿で再構成) | **本稿で成立を確認・二人目未了** | §1.5・§3・§7 |
| **N-5** | **系 N∞-red**((9.1)(9.2)) | 便 59 F9.2 + 本稿で再検算 | **未監査** | §1.6・T-1 |
| **N-6** | **補題 N∞-div**($p\mid a'$) | 便 59 (9.4) + 本稿で再検算 | **未監査** | §1.7・T-2 |
| R-1 | while 全除去禁止 | 規約(便 54 F6.2) | 閉 | §3.2 |
| R-2 | branch-value-free certificate・random opaque ID・HMAC commitment | 規約(便 59 F11.3・F13.2) | 閉 | §5・§5.1 |
| R-3 | mismatch は `INTEGRITY_STOP` | 規約(便 54 F9.2) | 閉 | §3.1・§6 |
| R-4 | EP 不在中は `partial predicate / UNKNOWN` | 規約(便 54 F9.1-6・便 59 F10.3) | 閉 | §9.2 |
| R-5 | fixture の用途分離 | 規約(便 59 F10.2) | 閉 | §8 |

---

## 12. 出所対応表(P56-1 5 欄)

| spec 条項 | 出所文書 | §・式番号 | 引用の型 | 状態 |
|---|---|---|---|---|
| §1.2 N∞-N | 便 59 | F6・F14-1 | **要約**(pushforward の定式化は本稿) | 未監査 |
| §1.3 N∞-1:1 | 便 59 | F6 | **本稿発の導出** | 未監査 |
| §1.4 N∞-fix | 便 59 | F8.3 の (i)(ii)(iii) | **独立再構成**(uniformizer の取り方まで再導出) | 未監査 |
| §1.5 N∞-swap | 便 59 | **F8.3・F13.1** | **独立検分 → 命題化**(本稿で成立を確認) | **本稿で確認・二人目未了** |
| §1.6 N∞-red | 便 59 | F9.2 (9.1)(9.2) | **逐語 + 本稿で再検算** | 未監査 |
| §1.7 N∞-div | 便 59 | F9.2 (9.4) | **逐語 + 本稿で再検算**(系は本稿発) | 未監査 |
| §2 入口契約 | S5 設計 | S5-1 / S5-2 / **S5-2a** / §3.3.5 S5-3∞ + 便 36 F2.1 | **逐語** | 凍結済(S5 側) |
| §3.1 T-1..T-7 | 便 59 | F9.3 | **逐語**(順序と reason code は本稿) | 未監査 |
| §4 二経路 | 便 59 | F10.1・F13.3 | **逐語** | 凍結候補 |
| §5 certificate | 便 59 | F13.2・F10.4-2 | **逐語**(5 欄)+ 二層化 | 凍結候補 |
| §5.1 hash 論 | 便 59 | **F11.3** | **逐語**(Sol 自己訂正) | 凍結候補 |
| §6 reason code | 便 59 | F10.4-1 | **要約** | 凍結候補 |
| §7 whitelist | 便 54 / 便 59 | F12.1 / F8.2・F11.3 | **逐語 + $\pm$ への訂正 + commitment の追加** | 凍結候補 |
| §8 fixtures | 便 59 | F10.2・F11.2 | **逐語** | 凍結候補 |
| §9.1 機構一致 | — | — | **本稿の exact 検算(boolean)** | 未監査 |
| §9.2 EP | 便 59 | F10.3 | **逐語** | 凍結候補 |
| §10 schema 修理 | 便 59 | F10.4 | **逐語**(5 点) | 凍結候補 |

---

## 13. Sol への監査依頼(v2)

1. **【必須】補題 N∞-swap の検分**(§1.5)。私は F8.3 を**独立に再構成**し、(i)(ii)(iii) が $\{py=0\}$ を**尽くす**こと・$\deg p=2$ が double root を**一つしか**許さないことを確認した。**場合分けの網羅性**と、**$m=2$ 以外で $e=2$ が出ない**ことに漏れがないか。
2. **【必須】命題 N∞-fix (iii) の $e=2m+1$**。$y$ を uniformizer とした $\operatorname{ord}$ の計算($\operatorname{ord}_Q(a-v)=4m+2$ vs $\operatorname{ord}_Q(py)=2m+1$)。
3. **【必須】系 N∞-1:1 の証明**。$Q,\iota Q$ が同時に fiber にある ⟺ $v^2=\hat c_\mu$ の同値性(私は $\mu(Q)\mu(\iota Q)=N(\mu)(x_0)=\hat c_\mu$ を使った)。**$y_0=0$ の場合も同じ式で閉じているか。**
4. **【推奨】T-2 の型**。補題 N∞-div の系「$p\doteq a'/\bigl(a_5(x-\alpha)(x-\beta)\bigr)$」を **T-2 の失敗条件としてどう書くべきか**(私は `pell-derivative-mismatch` を `INTEGRITY_STOP` にしたが、`REJECT` が正しい場合があるか)。
5. **【推奨】§3.1 の `swap-lemma-precondition`**。T-1 が通って T-6 が落ちたときに `INTEGRITY_STOP` とした判断(補題の適用外を黙って通さない)。
6. **【推奨】§9.1 の機構一致**を回帰の事前登録として十分か(4 欄一致 + `ord_0(a)=3` の記録)。

---

## 14. 実装着手の条件

$$ \boxed{\ \text{v2 の Sol 監査 PASS}\ \to\ \text{freeze ID 発行(F12 様式・}\texttt{supersedes\_draft = 77ed7131…}\text{)}\ \to\ \text{searcher と checker を}\ \textbf{別々に}\ \text{実装}\ } $$

- **実装着手禁止は継続**(裁定 70)。
- **searcher = §4 左列(local differential → ramification divisor → pushforward)/ checker = §4 右列(証明済み baseline の elimination)。実装者を分ける。**
- **EP(§9.2)が揃うまで札は `partial predicate / UNKNOWN`。**
- **旧 8 hit は §8 の neutral lane でのみ使う。**
