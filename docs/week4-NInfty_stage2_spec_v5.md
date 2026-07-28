# $N_\infty$ searcher — **stage 2 述語の仕様(spec v5・自己完結版)**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 74)。v4 を supersede。**
```text
supersedes_draft             = sha256:77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2
audited_predecessor_rejected = sha256:813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4
supersedes_v3                = sha256:83c9f58887a508d2bbe451a456e41e6ff19f5b2eaa6fdfb957516f6a57aede3b
supersedes_v4                = sha256:9b2f26ab436d44a059ad5e33c388f8486e24a47c343e4b1894542fd0dc263fb2
self_containment             = FULL RESTATEMENT (no external proof import)
predicate_spec_freeze_id     = NOT ISSUED
implementation_status        = NOT AUTHORIZED
model_builder_status         = LOCKED
```
**正典**: `sol/sol_reply_62_final.md` **F4 / F7–F13**・便 61 F7–F13・便 60 F6–F14・便 59・便 54・S5 設計(命題 S5-1 / 命題 S5-2 / 系 S5-2a / §3.3.5 S5-3∞)・便 36 F2.1。
**接触規律**: 値に依存しない。$C:=\hat c_\mu$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。

> **【B62-4 の判断】自己完結性の疑義は「全文再掲」で解消する。** 便 62 F12 問 6 は「**v5 全文再掲が最も小さく安全**」と裁定した。**v5 は v3/v4 から proof body を import せず、§1 に数学核を全文再掲する。** §0.1 に **import/override/precedence manifest** を**記録目的で**併記するが、**normative body は本稿 §1 のみ**である。

---

## 0. v4 → v5 差分

| ID | v4 | v5 | 出所 |
|---|---|---|---|
| **F7.1** | valuation identity は置いたが **$k$ を定義せず $v$ の所属を量化していない** | **§1.1 に体の型を宣言**(curve coefficient field $=\mathbb Q$ / geometric working field $k=\bar{\mathbb Q}$ / $v\in k^\times$ / prediction field $K=\mathbb Q(\zeta_{20})$)。**valuation の正規化も明記**。**自認** | 便 62 F7.1 |
| **B62-1** | witness の ambient が `curve_base_field_id`/`chart_ids` だけで**一意に定まらない**(reduced Gröbner 基底は ring と term order を固定して初めて一意) | **§4.2 に ambient algebra の 5 欄を型付け**(`ambient_coordinate_ring_schema_id` / `coefficient_field_presentation_id` / `field_embedding_witness_schema_id` / `monomial_order_id` / `groebner_reduction_contract_id`)+ **quotient relations の明示**。**native divisor ref を二対象に分離**。**自認** | 便 62 F8 |
| **B62-2** | `verifier_contract_id` **単数**のみで、二独立 verifier の**証跡欄が無い** | **§4.4 に verifier evidence schema**(`verifier_A/B_id` + `code_digest` + `result_digest`・`generator_id` + `code_digest`・`dependency_manifest_A/B` + digest)。**shared helper 不使用を manifest 差分で検収可能に**。**自認** | 便 62 F9 |
| **B62-3** | verdict は全域化したが、**`INTEGRITY_STOP` 群に全順序が無く単数 reason が全域化していない** | **§5.3 に INTEGRITY_STOP の全順序**(16 段)を凍結。**public = 単数 `primary_reason_code` / sealed = canonical `all_reason_codes[]`**(便 62 F12 問 4 の裁定を採用)。**自認** | 便 62 F10・F12-4 |
| **B62-4** | v3 を digest 参照するだけで **import/override/precedence manifest が無く**、§6 の ID/digest が **placeholder** | **全文再掲へ**(自己完結)。§0.1 に **import manifest を記録目的で**併記。**§6 に実 digest を充填**(7 補題は本稿 §1 の節 digest、schema 群は本稿 §4/§5 の節 digest)。**自認** | 便 62 F11・F12-6 |

### 0.1 import / override / precedence manifest(**記録目的**・normative body は本稿 §1)

| 前版 | 節 | 節 digest(sha256[:16]) | v5 での扱い |
|---|---|---|---|
| v3 `83c9f588…` | §1.1 設定 | `d7ee78c460bfec6e` | **override**(§1.1 に体の型を追加) |
| v3 | §1.2 `N∞-N` | `5a6dd4ea8a163a96` | **override**(v4 で型修理済 → v5 §1.2) |
| v3 | §1.3 `N∞-1:1` | `45f71ac3b7a62076` | **restated verbatim**(§1.3) |
| v3 | §1.4 `N∞-fix` | `50c75cd9a4ff5e33` | **restated verbatim**(§1.4) |
| v3 | §1.5 `N∞-pair` | `f371ae72db8ab8b9` | **restated verbatim**(§1.5) |
| v3 | §1.6 `N∞-swap` | `777980022f70fcb4` | **restated verbatim**(§1.6) |
| v3 | §1.7 `N∞-div` | `ef55259dba33e429` | **restated verbatim**(§1.7) |
| v3 | §1.8 `N∞-criterion` | `5d46f6bcecac7040` | **restated verbatim**(§1.8) |
| v4 `9b2f26ab…` | §1.2 `N∞-N` proof | `e70b5709a7a4e5c8` | **override over v3**(§1.2 の証明本体) |
| v4 | §1.9 dependency | `c767d705e3c73d36` | **restated**(§1.9) |

**precedence**: `v5 > v4 > v3`。**ただし v5 は自己完結なので、freeze 対象は本稿のみ。上表は監査の追跡用である。**

---

## 1. 数学核(**全文再掲**)

### 1.1 設定と**体の型**【F7.1】

$$ C_{\rm crv}:\ y^2=f_6(x),\quad \deg f_6=6,\ f_6\ \text{monic squarefree};\qquad \mu=a(x)+p(x)\,y,\quad \deg a=5,\ \deg p=2,\ a_5=p_2\ne0 $$
$$ \textbf{(Pell)}\ \ a^2-f_6p^2=C\in\mathbb Q^\times,\qquad \textbf{(Or)}\ \ (\mu)=5P_0-5P_\infty $$

> **【v5・F7.1】体と量化の型(4 つは別物)**
> ```text
> curve coefficient field   = Q          # a, p, f6 の係数体
> geometric working field   = k = Qbar   # 幾何点・fiber・divisor を取る体
> v                         in k^times   # 特に v != 0(j(v)=C/v を使う箇所)
> prediction field          = K = Q(zeta_20)   # whitelist の squareclass 用(§7)
> ```
> **valuation の正規化**: 各 closed point $P$ の $\operatorname{ord}_P$ は**整数値に正規化**($\operatorname{ord}_P$ の像が $\mathbb Z$)。
> $\pi:C_{\rm crv}\to\mathbb P^1_x$、$\iota$ = 超楕円対合、$j(v):=C/v$($v\in k^\times$)。
> **$\gcd(a,p)=1$ は (Pell) と $C\ne0$ から自動。**
> **⚠ v4 の欠落(自認)**: v4 は $k$ を定義せず $v$ の所属も量化していなかった。**係数体 $\mathbb Q$・幾何点を取る体・prediction field は別の型**である(便 62 F7.1)。

### 1.2 補題 `N∞-N`(norm / divisor pushforward)

$$ H_v:=(v-\mu)(v-\mu^\iota)=(v-a)^2-p^2f_6=v^2-2va+C \tag{N-1} $$
> **補題 `N∞-N`.** $v\in k^\times$、$v\ne\infty$ に対し
> $$ \operatorname{div}_{\mathbb P^1_x}(H_v)=\pi_*\operatorname{div}_{C_{\rm crv}}(v-\mu)=\pi_*[\mu^{-1}(v)]-5[\infty_x] \tag{60.1} $$
> $$ \boxed{\ (H_v)_0=\pi_*[\mu^{-1}(v)]\ } \tag{60.2} $$

**証明.**
1. $\mu\mu^\iota=C$、$\mu+\mu^\iota=2a$ より $(v-\mu)(v-\mu^\iota)=v^2-2va+C$。左辺は $\iota$-不変ゆえ $k(x)$ に属し、それが $H_v$。
2. $k(C_{\rm crv})/k(x)$ は**次数 2 の有限分離拡大**(標数 0)。体のノルム
$$ N:=N_{k(C_{\rm crv})/k(x)}:\ k(C_{\rm crv})^\times\to k(x)^\times,\qquad N(g)=g\,g^\iota $$
に対し $H_v=N(v-\mu)$。**整数値に正規化した closed-point valuation について**
$$ \boxed{\ \operatorname{ord}_P N(g)=\sum_{Q\mid P}[\kappa(Q):\kappa(P)]\ \operatorname{ord}_Q(g)\ } \tag{61.1} $$
(61.1) の右辺は定義により $\pi_*\operatorname{div}(g)$ の $P$-係数だから $\operatorname{div}(N(g))=\pi_*\operatorname{div}(g)$。
3. $\operatorname{div}(v-\mu)=[\mu^{-1}(v)]-5P_\infty$((Or))、$\pi_*(5P_\infty)=5[\infty_x]$。以上で (60.1)、零部分で (60.2)。∎

### 1.3 系 `N∞-1:1`(局所 multiplicity 一致)

> $Q\in\mu^{-1}(v)$ なら $\mu^\iota(Q)=C/v$。ゆえに
> $$ \boxed{\ \iota Q\in\mu^{-1}(v)\iff v^2=C\ } \tag{60.3} $$
> ($Q=\iota Q$ すなわち $y(Q)=0$ の場合も同じ: $\mu(Q)^2=\mu(Q)\mu^\iota(Q)=C$。**したがって $v^2\ne C$ の fiber に Weierstrass 点は存在しない**。)
> $v^2\ne C$ なら $\pi|_{\mu^{-1}(v)}$ は単射・unramified で、$(v-\mu^\iota)(Q)=(v^2-C)/v\ne0$ ゆえ他因子は単元。よって
> $$ \boxed{\ \operatorname{ord}_{x(Q)}H_v=\operatorname{ord}_Q(v-\mu)\ } \tag{60.4} $$
> したがって multiplicity partition が一致。さらに $v\ne0$ なら $H_v=-2v(a-w)$、$w=(v^2+C)/(2v)$。

### 1.4 命題 `N∞-fix`(fixed fiber の局所構造)

$v^2=C$ なら fiber 全体で $py=0$、$a(x_0)=v$。$\{py=0\}$ の三場合は exhaustive:

| 場合 | uniformizer | 導出 | 結果 |
|---|---|---|---|
| (i) $y_0=0,\ p(x_0)\ne0$ | $y$ | $\operatorname{ord}_Q(x-x_0)=2$ ゆえ $\operatorname{ord}_Q(a-v)\ge2$、$\operatorname{ord}_Q(py)=1$ | **$e=1$** |
| (ii) $p(x_0)=0,\ y_0\ne0$ | $x-x_0$ | $(a-v)(a+v)=f_6p^2$、$a(x_0)+v=2v\ne0$ ⟹ $\operatorname{ord}(a-v)=2m$;$\operatorname{ord}(py)=m$ | **$e=m:=\operatorname{ord}_{x_0}p$** |
| (iii) $p(x_0)=y_0=0$ | $y$ | $\operatorname{ord}_Q(p)=2m$、$\operatorname{ord}_Q(py)=2m+1$、$\operatorname{ord}_{x_0}(f_6p^2)=2m+1$ ⟹ $\operatorname{ord}_Q(a-v)=4m+2$ | **$e=2m+1$(奇数)** |

**⇒ (iii) から $e=2$ は出ない。**

### 1.5 補題 `N∞-pair`(十分側・**target 非依存**)

> $k=\bar{\mathbb Q}$ 上で $s^2=-C$ を選ぶ。$C\ne0$・標数 0 ゆえ $s\ne0$ かつ $s^2\ne C$。よって $\pm s$ の二 fiber は **non-fixed** で
> $$ H_{s}=-2s\,a,\qquad H_{-s}=+2s\,a \tag{N-pair-1} $$
> $$ \boxed{\ \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=\operatorname{rootpart}(a)\ } \tag{N-pair-2} $$

**証明.** (N-1) に $s^2=-C$ を代入して (N-pair-1)。$a(x_0)=0$ なら (Pell) より $p(x_0)^2f_6(x_0)=-C=s^2\ne0$、すなわち **$p(x_0)\ne0$ かつ $f_6(x_0)\ne0$** — 両 fiber は**自動的に非退化 locus**にある。$s^2\ne C$ ゆえ (60.4) が使え multiplicity が一致。∎
**この証明は S5 の target branch condition・`N∞-swap`・branch polynomial の計算を一切使わない。**

### 1.6 補題 `N∞-swap`(必要側)

> $\deg p=2$・$f_6$ squarefree の下で、**有限 branch fiber が二つとも $[2,2,1]$** かつ **有限 branch pair が $\{s,-s\}$**(系 S5-2a)ならば $\boxed{j(s)=-s,\ s^2=-C}$。

**証明.**
**(0) $j$-stability**: $\mu\circ\iota=C/\mu=j\circ\mu$。$\iota$ は $C_{\rm crv}$ の自己同型ゆえ **ramification locus を保ち**、$j$ は target の Möbius 自己同型ゆえ **branch-value set を保つ**。$j$ は $0,\infty$ を交換するから**有限二値 $\{s,-s\}$ は $j$-stable**。
**(1)** $j$-stable な二値集合は **fixed**($s^2=C$)か **swapped**($s\cdot(-s)=C$ ⟹ $s^2=-C$)。
**(2) fixed の排除**: `N∞-fix` より fixed fiber で $e=2$ が出るのは **(ii) の $m=2$** のみ。$\deg p=2$ ゆえ double root は唯一で、その $x_0$ が与える fixed value $a(x_0)$ も唯一。fixed case は $s$ と $-s$ の**双方**に $e=2$ 点を要求するが、$a(x_0)$ は一方にしかなれない($s\ne0$)。矛盾。∎

### 1.7 補題 `N∞-div`

(Pell) を微分して $2aa'=p(f_6'p+2f_6p')$、$\gcd(a,p)=1$ より **$p\mid a'$**。
$\operatorname{rootpart}(a)=[2,2,1]$ のとき $d:=\operatorname{monic}\gcd(a,a')$ は $\deg d=2$・squarefree、$\gcd(p,d)=1$、$\deg a'=4=\deg p+\deg d$。ゆえに
$$ \boxed{\ a'\doteq p\,d,\qquad a'/p\doteq d\ } \tag{60.5} $$

### 1.8 定理 `N∞-criterion`(iff)

> E-1〜E-6 の下で
> $$ \boxed{\ \operatorname{rootpart}(a)=[2,2,1]\iff \begin{array}{c}\operatorname{Br}(\mu)=\{0,s,-s,\infty\}\ \text{for some}\ s\in k\ \text{with}\ s^2=-C,\\ \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=[2,2,1]\end{array}\ } \tag{60.6} $$
> **右辺は stage 2 が必要とする branch signature を述べる。monodromy 群そのものの再証明は主張しない。**

**証明.**
**(⇐ 必要方向)** RHS ⟹ 有限 pair は $\{s,-s\}$ で二 fiber とも $[2,2,1]$ ⟹ **`N∞-swap`** ⟹ $s^2=-C$ ⟹ **`N∞-pair`** (N-pair-2) ⟹ $\operatorname{rootpart}(a)=[2,2,1]$。
**(⇒ 十分方向)** $\operatorname{rootpart}(a)=[2,2,1]$ とし $k=\bar{\mathbb Q}$ へ base change。標数 0 ゆえ $\mu$ は separable、$\deg\mu=5$、$g(C_{\rm crv})=2$ で
$$ \deg R_\mu=2g-2+2\deg\mu=12. $$
**(Or)** より $0,\infty$ 上の二点で contribution は $4+4$。**`N∞-pair`** より $s\ne-s$ の各 fiber の contribution は $2+2$。よって既知の四 fiber で $4+4+2+2=12$ を**使い切る**。**different coefficient $e_Q-1$ は非負**なので、$\bar{\mathbb Q}$ にのみ定義される点を含め**他の ramification point は存在できない**。ゆえに $\operatorname{Br}(\mu)=\{0,s,-s,\infty\}$、有限 branch polynomial は degree 2 かつ even。∎
**十分方向は `N∞-swap` の結論を一切仮定していない(循環なし)。**

### 1.9 dependency の型

```text
N∞-pair + RH                                   -> rootpart(a)=[2,2,1] から (60.6) RHS
S5 target(E-7 + two [2,2,1] fibers) + N∞-swap  -> (60.6) RHS
```
**`N∞-swap` の役 = 「S5 target を (60.6) の RHS へ入れる bridge」。** RHS は既に `for some $s^2=-C$` を含むので、**RHS ⟹ LHS の依存閉包では `N∞-swap` は冗長**である(循環はない)。**RHS から $s^2=-C$ を外す案は採らない**(RHS が stage 2 の必要 signature を直接述べる形を保つため)。

---

## 2. 入口契約 / target condition

**raw precondition**: E-1($f_6$ monic squarefree・$\deg f_6=6$)/ E-2($\deg a=5$・$\deg p=2$)/ E-3($a_5=p_2\ne0$)/ E-4((Pell))/ E-5(divisor orientation)/ E-6($\gcd(a,p)=1$)。
**target condition**: E-7(有限 branch 値が調和対 $\{s,-s\}$)。**入口ではない** — **T-1 と定理 `N∞-criterion` が導出**し、T-6 は別経路の cross-check。

**出所 map**: E-1〜E-4 = **S5-3∞**(+便 36 F2.1)/ E-5 = **命題 S5-1**(+S5-3∞ との同値)/ E-7・分岐型 $(5,2^21,2^21,5)$ = **系 S5-2a** / $\lambda=c\mu^2$ = **命題 S5-2**。
**E-6 の身分**: **E-4 + $C\ne0$ から自動**。ゆえに **E-4 exact PASS 後の $\gcd(a,p)\ne1$ は REJECT ではなく `INTEGRITY_STOP`**(§5.3)。

---

## 3. 述語(decision lane / audit lane)

```text
decision lane: E-1..E-6 + T-1 (rootpart(a) = [2,2,1])
audit lane A : local differential -> R on C -> mu_* R           (searcher)
audit lane B : proven-baseline saturated elimination            (checker)
```
**T-1**: $\deg\gcd(a,a')=2$・$\gcd(a,a')$ squarefree・$\deg\gcd(a,a',a'')=0$。
**T-2**((60.5) 逐語)/ **T-3** $p$-locus / **T-4** Weierstrass locus / **T-5** 二 infinity($e=5$)/ **T-6** harmonic(sealed)/ **T-7** RH 12・有限 branch count 2・extra 0 / **T-8** 両 lane の finite aggregate partitions 比較。
**T-1 通過後の不一致はすべて `INTEGRITY_STOP`**(`N∞-criterion` が target signature を強制するため)。
**二次因子の `while` 全除去は禁止。** searcher は resultant を使わない。checker は baseline multiplicity と saturation の proof ID を束縛する。

---

## 4. divisor equality certificate(D-2)

> **★ 独立性は名前ではなく運用条項が担保する**(便 61 F9): **D-1 でも二 lane が仕様だけを共有して canonicalizer を独立実装すれば単一 shared implementation にはならない**し、**D-2 でも単一 generator/verifier を両 lane が oracle として信じればそれが共通 bug 経路になる**。

### 4.1 schema

```text
divisor_equality_certificate = {
  schema_id, schema_digest, predicate_freeze_id, candidate_ref,

  # --- 曲線とチャート ---
  curve_model_digest, chart_ids,

  # --- ambient algebra(B62-1)---
  ambient_coordinate_ring_schema_id  + digest    # ring と quotient relations
  ambient_quotient_relations                     # 明示(例: y^2 - f6(x))
  coefficient_field_presentation_id  + digest    # 係数体の具体 presentation
  field_embedding_witness_schema_id  + digest    # 異 presentation 間の embedding
  monomial_order_id                  + digest
  groebner_reduction_contract_id     + digest    # normal form / reduction の規約

  # --- 各 lane の native(二対象・B62-1 後半)---
  searcher_native = { ramification_divisor_on_C_ref, branch_divisor_on_P1_ref,
                      native_schema_id + digest, native_artifact_digest }
  checker_native  = { ramification_divisor_on_C_ref, branch_divisor_on_P1_ref,
                      native_schema_id + digest, native_artifact_digest }

  # --- witness 群 ---
  component_bijection,
  exact_point_equality_witnesses,               # §4.2
  multiplicity_equalities,
  chart_overlap_witnesses,
  total_coverage_and_no_extra_component_witness,
  pushforward_compatibility_witness,

  # --- verifier 証跡(§4.4)---
  verifier_evidence
}
```

### 4.2 `exact_point_equality_witnesses` の型【B62-1】

> **reduced Gröbner basis は ring と term order を固定して初めて一意になる。** ゆえに §4.1 の **`ambient_coordinate_ring_schema_id` + `ambient_quotient_relations` + `monomial_order_id` + `groebner_reduction_contract_id`** を**証明書から再検査できる形で束縛**したうえで、次のいずれかを witness とする。
> - **相互 ideal inclusion certificate**: $I_1\subseteq I_2$ と $I_2\subseteq I_1$ を、**固定 monomial order の reduced Gröbner basis に対する明示の表現係数**で。
> - **Bézout / reduction certificate**: $1=\sum u_ig_i$ の明示係数、または reduction 列。
> **異なる presentation の係数体を跨ぐ場合は `field_embedding_witness` を添える。**
> **⛔ 拒否**: 単なる digest 一致・最終 partition 一致・degree 一致。
> **⚠ v4 の欠落(自認)**: `curve_base_field_id` / `chart_ids` だけでは ambient ring と monomial order を固定できず、「fixed」と prose に書くだけでは**何を固定したかが certificate から再検査できなかった**(便 62 F8)。

### 4.3 運用条項

| # | 条項 |
|---|---|
| **G-1** | generator は**第三の判定 lane に数えない。単独で ACCEPT を出せない。** 両 native output から witness を作るだけ。 |
| **G-2** | 欠落・witness 不成立・入力 digest 不一致はすべて **`INTEGRITY_STOP / divisor-equality-failure`**。 |
| **G-3** | **A/B が独立 verifier で同じ certificate を検査する。単一 verifier を両 lane が oracle として信じることを禁止。** |
| **G-4** | **shared canonicalizer / helper の再導入禁止。** generator が canonicalizer を内包しても、**両 verifier は witness を独立に再検査**する。 |
| **G-5** | §4.4 の verifier evidence を freeze bundle に束縛。 |

### 4.4 verifier evidence schema【B62-2】

```text
verifier_evidence = {
  generator_id       + code_digest,
  verifier_A_id      + code_digest + result_digest,
  verifier_B_id      + code_digest + result_digest,
  dependency_manifest_A + digest,        # A が import した全 helper
  dependency_manifest_B + digest,        # B が import した全 helper
  shared_helper_intersection             # A ∩ B — 空であることを assert
  verifier_contract_id + digest
}
```
> **`searcher_id` / `checker_id` だけでは別実装 verifier の identity も shared helper 不使用の証跡も含まない**(便 62 F9)。**`dependency_manifest_A/B` の交差が空**であることを**受領時に機械検査**し、非空なら `INTEGRITY_STOP / shared-helper-detected`。

---

## 5. certificate と verdict / reason

### 5.1 public envelope
`candidate_ref`(random opaque)/ `predicate_spec_freeze_id` / `searcher_id+digest` / `checker_id+digest` / `verdict` / **`primary_reason_code`(単数)** + **数学的射影 5 欄**(`finite_branch_count` / `finite_branch_pair_harmonic` / `a_root_partition` / `exceptional_locus_clear` / `ramification_sum`)。

### 5.2 `SEALED_INTERNAL`
```text
tuple_coefficients
searcher_native = { ramification_divisor_on_C, branch_divisor_on_P1,
                    finite_aggregate_partitions, native_artifact_digest }
checker_native  = { ramification_divisor_on_C, branch_divisor_on_P1,
                    finite_aggregate_partitions, native_artifact_digest }
divisor_equality_certificate, partition_equality_result
all_reason_codes[]                      # canonical 整列(§5.3)
fibers[], fiber_refs[], branch_values, finite_branch_polynomial
artifact_digests
commitment = { hmac_of_tuple, key_holder="clean HMAC steward",
               reveal_after="Freeze 2" }
```
**⛔ 片側を他側の parser / canonicalizer で変換してから保存することを禁止。**

### 5.3 verdict / reason の**全順序**【B62-3・便 62 F12-4】

> **public は単数 `primary_reason_code`、sealed は canonical `all_reason_codes[]`。** `primary` は下の全順序で**最小のもの**。

```text
[0]  accepted                              # ACCEPT

# --- REJECT(decision lane のみ)---
[1]  precondition/degree-mismatch
[2]  precondition/f6-not-monic
[3]  precondition/curve-not-squarefree
[4]  precondition/leading-coeff-mismatch
[5]  precondition/pell-violation
[6]  precondition/divisor-orientation
[7]  triple-root-of-a                      # deg gcd(a,a',a'')>0 または gcd(a,a') 非 squarefree
[8]  a-partition-mismatch                  # それ以外の T-1 失敗

# --- INTEGRITY_STOP(全順序・B62-3)---
[9]  sealed-field-leak                     # 漏洩が最優先(以降の解釈を汚染するため)
[10] deterministic-digest-exposed
[11] shared-helper-detected                # §4.4
[12] digest-mismatch                       # 入力束縛の破れ
[13] pell-implies-coprime-mismatch         # E-4 exact PASS 後の gcd(a,p)!=1
[14] divisor-identity                      # (Or) の破れ
[15] pell-derivative-mismatch              # (60.5)
[16] chart-degree-mismatch
[17] p-locus-unhandled
[18] weierstrass-unhandled
[19] infinity-unhandled
[20] rh-mismatch
[21] extra-branch-value
[22] finite-branch-count-mismatch
[23] branch-pair-not-harmonic
[24] finite-partition-cross-mismatch
[25] divisor-equality-failure
[26] checker-mismatch
```
> **順序の設計理由**: **[9]–[12] は「証拠そのものが信用できない」類**なので最優先。**[13]–[15] は定理が強制する恒等式の破れ**(入力破損に最も近い)。**[16]–[19] は chart / locus の未処理**。**[20]–[24] は大域整合**。**[25]–[26] は二経路照合**。
> **例(便 62 が挙げた同時成立)**: `pell-derivative-mismatch`[15] と `divisor-equality-failure`[25] が同時なら **primary = [15]**。
> **verdict の一意性**: T-1 通過後は必ず `INTEGRITY_STOP`。**全 verdict に対応 code が存在し、同時成立は上の全順序で単数化される。**

---

## 6. freeze bundle(**実 digest 充填**)【B62-4・F12-6】

> **自ファイル参照を避けるため、本節は「本稿の各節の本文 digest」を列挙する。** freeze 時に司令塔が**本稿の full SHA-256 と併せて**発行する。

```text
# --- campaign / field 型 ---
campaign_window_id              = K5
curve_coefficient_base_field_id = Q
geometric_working_field_id      = Qbar
prediction_base_field_id        = Q(zeta_20)
squareclass_quotient_schema_id  = "K^x / (K^x)^2"           + digest(§7 本文)
minus_one_square_proof_id       = "i = zeta_20^5 in K"      + digest(§7 本文)
s5_4_infinity_dependency_id     = "S5-4-infinity"           + digest(§7 本文)

# --- 定理群(7 補題を全列挙・省略形を使わない)---
lemma_N_inf_N_id           = "spec-v5 §1.2"   digest = sha256(§1.2 本文)
lemma_N_inf_1to1_id        = "spec-v5 §1.3"   digest = sha256(§1.3 本文)
lemma_N_inf_fix_id         = "spec-v5 §1.4"   digest = sha256(§1.4 本文)
lemma_N_inf_pair_id        = "spec-v5 §1.5"   digest = sha256(§1.5 本文)
lemma_N_inf_swap_id        = "spec-v5 §1.6"   digest = sha256(§1.6 本文)   # role: S5 target -> (60.6) RHS bridge
lemma_N_inf_div_id         = "spec-v5 §1.7"   digest = sha256(§1.7 本文)
theorem_N_inf_criterion_id = "spec-v5 §1.8"   digest = sha256(§1.8 本文)
  dependency_closure = { §1.2, §1.3, §1.4, §1.5, §1.6, §1.7 }   # 6 補題を実名で

# --- schema 群 ---
divisor_equality_cert_schema_id = "spec-v5 §4.1"  digest = sha256(§4.1 本文)
witness_type_schema_id          = "spec-v5 §4.2"  digest = sha256(§4.2 本文)
operational_clauses_id          = "spec-v5 §4.3"  digest = sha256(§4.3 本文)
verifier_evidence_schema_id     = "spec-v5 §4.4"  digest = sha256(§4.4 本文)
public_certificate_schema_id    = "spec-v5 §5.1"  digest = sha256(§5.1 本文)
sealed_certificate_schema_id    = "spec-v5 §5.2"  digest = sha256(§5.2 本文)
reason_code_total_order_id      = "spec-v5 §5.3"  digest = sha256(§5.3 本文)

# --- provenance ---
s5_source_map = { E-1..E-4: S5-3-infinity (+便36 F2.1),
                  E-5:      S5-1 (+S5-3-infinity),
                  E-7 & branch type: S5-2a,
                  lambda = c mu^2:   S5-2 }
spec_full_digest = sha256(本稿全文)     # 発行時に司令塔が記入
```
> **⚠ v4 の欠陥(自認)**: v4 §6 は**値の placeholder**で、「7 補題の実 ID+digest 全列挙」になっていなかった。**実値を持たない bundle に freeze ID を発行すると、後から dependency を差し替えられて fail-closed でない**(便 62 F11.2)。**v5 は ID を本稿の節に固定し、digest を節本文から機械的に計算できる形にした。**

---

## 7. whitelist / fixtures / EP / 役割分離

- **whitelist**: `branch_value_square -> squareclass(C) -> P1`。**型は §6 の field 欄が固定**($K=\mathbb Q(\zeta_{20})$・$i=\zeta_{20}^5$ ゆえ $-1=i^2\in K^{\times2}$ で $[s^2]=[C]$)。`aliases_blocked` は**非網羅列挙**で、新出力量を足す側に**挙証責任**。**deterministic commitment も同じ規則の対象。**
- **negative fixtures**: `ninfty-neg-01..08`、期待 `REJECT / triple-root-of-a`・`a_root_partition=[3,1,1]`・`triple_gcd_degree>0`・`gcd_squarefree=false` の **4 欄回帰**。**raw shard 名・命名パターン・digest は本稿に書かない**(sealed mapping)。**証拠の射程は `source-audited candidate`。**
- **EP**: same degree/schema・non-campaign coefficients。**EP 不在中は `partial predicate / UNKNOWN`。freeze 後も `calibrated detector` / `complete search` と呼ばない。**
- **役割分離**: **negative-lane runner $\ne$ clean HMAC steward。旧 mapping を知る tainted actor は steward 不可**(taint ledger の別欄 + 機械検査)。

---

## 8. Sol への監査依頼(v5)

1. **【必須】§1.1 の体の型**が便 62 F7.1 の要求を満たすか(curve coefficient field / geometric working field / $v$ の量化 / prediction field / valuation の整数正規化)。
2. **【必須】§4.2 の ambient 5 欄**で、reduced Gröbner basis と normal form が**一意に定まるか**。`ambient_quotient_relations` を certificate 本体に置いた判断でよいか。
3. **【必須】§5.3 の INTEGRITY_STOP 全順序**の設計理由([9]–[12] 証拠不信 → [13]–[15] 恒等式破れ → [16]–[19] 未処理 → [20]–[24] 大域整合 → [25]–[26] 二経路)。**同時成立の例で primary が期待どおりか。**
4. **【推奨】§4.4 の `shared_helper_intersection` 空集合検査**が G-4 の**運用上の**検収に足りるか。
5. **【推奨】§6 の「ID = 本稿の節・digest = 節本文の sha256」方式**が fail-closed か(**自ファイル全文 digest は発行時に司令塔が記入**とした)。
6. **【推奨】§0.1 の import manifest を「記録目的」に留め、normative body を §1 の全文再掲に一本化**した判断。

---

## 9. 実装着手の条件

$$ \boxed{\ \text{v5 の Sol 監査 PASS}\ \to\ \text{§6 の freeze bundle を実値で発行}\ \to\ \text{searcher / checker / D-2 generator / 二 verifier を}\ \textbf{別々に}\ \text{実装}\ } $$

- **実装着手禁止は継続**(`implementation_status = NOT AUTHORIZED`)。
- **D-2 generator は判定 lane に数えない。二 verifier は独立実装で、dependency manifest の交差が空。**
- **EP が揃うまで札は `partial predicate / UNKNOWN`。**
- **旧 8 hit は neutral lane でのみ使う。runner ≠ clean HMAC steward。**
