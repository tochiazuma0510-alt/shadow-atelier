# $N_\infty$ searcher — **stage 2 述語の仕様(spec v6・自己完結版)**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 75)。v5 を supersede。**

## 0.0 lifecycle state【B63-4・便 63 F11】

> **⚠ 無時制の状態欄を frozen artifact に埋め込むと、freeze ID / 実装認可を外から発行した瞬間に artifact 自身が反対の live 状態を主張し続ける。欄を直接更新すれば full digest が変わり、提示済み hash は freeze digest でなくなる。自認**(A62-2 と同型の欠陥)。

```text
embedded_state_at_candidate_creation = {
  freeze_id:      NOT ISSUED,
  implementation: NOT AUTHORIZED,
  model_builder:  LOCKED
}
live_status_authority = Sol freeze reply + commander receipt
live_freeze_and_authorization_authority = approved freeze receipt
```
**本稿の上記 blob は「candidate 作成時点で埋め込まれた状態」であって live status ではない。live status の正本は approved freeze receipt 側にあり、receipt 発行によって本稿を書き換える必要はない(digest 不変)。**

```text
supersedes_draft             = sha256:77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2
audited_predecessor_rejected = sha256:813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4
supersedes_v3 = sha256:83c9f58887a508d2bbe451a456e41e6ff19f5b2eaa6fdfb957516f6a57aede3b
supersedes_v4 = sha256:9b2f26ab436d44a059ad5e33c388f8486e24a47c343e4b1894542fd0dc263fb2
supersedes_v5 = sha256:290c7d5768f95e9a1b9412fea123cfa36527f7e3917a1b656fe4479065d9428b
self_containment = FULL RESTATEMENT (no external proof import)
```
**正典**: `sol/sol_reply_63_final2.md` **F4 / F8–F11**・便 62 F4–F13・便 61・便 60・便 59・便 54・S5 設計(命題 S5-1 / 命題 S5-2 / 系 S5-2a / §3.3.5 S5-3∞)・便 36 F2.1。
**接触規律**: 値に依存しない。$C:=\hat c_\mu$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。

> **【自己完結の方針(v5 から継続)】** 便 62 F12 問 6 の裁定どおり **§1 に数学核を全文再掲し、v3/v4/v5 から proof body を import しない**。**normative body は本稿のみ。**

---

## 0. v5 → v6 差分

| ID | v5 | v6 | 出所 |
|---|---|---|---|
| **B63-1** | `shared_helper_intersection = ∅` のみ。**直接依存か推移的閉包か未定義**で、別名・wrapper・runtime/parser/CAS をどこまで helper と数えるかも未定義。文字どおり「全 helper」なら標準 runtime の共有で交差は通常空にならず、暗黙に除けば**共通 canonicalizer を除外した証拠にならない** | **§4.4 を推移的依存閉包へ**。`dependency_manifest_schema_id + digest` / `dependency_closure_A[]/B[] = transitive content digests` / `allowed_shared_tcb[] = frozen content digests + role` / `forbidden_shared_math_helper_intersection = (closure_A ∩ closure_B) − allowed_shared_tcb = ∅`。**「直接依存のみの manifest は不可」を条文化**。**intersection は producer の自己申告を信じず receipt 受領側が canonical content digest 集合から導出**。build root / toolchain / implementation provenance も記録。**自認** | 便 63 F8 |
| **B63-2** | 「16 段」と表記(実列挙は $[9]$–$[26]$ の **18 段**)。**public primary = 全順序の最小**としたため、`precondition/degree-mismatch`[1] と `sealed-field-leak`[9] の同時検出で **REJECT[1] が選ばれ証拠汚染[9] を隠す**(設計理由と逆転)。`accepted` が failure と同居しない不変条件も無い。G-2 が入力 digest 不一致を `divisor-equality-failure` へ送り `digest-mismatch`[12] と**二重割当** | **18 段に数え直し**。**§5.3 を verdict state machine へ**(verdict 決定と reason priority を**分離**・`primary = minimum(I, integrity_priority)`・`accepted` は $I=R=\varnothing$ のときのみ)。**envelope-level leak / digest / dependency check を early REJECT より先に実行**。**G-2 の routing を分割**(digest 不一致 → `digest-mismatch` / witness 欠落・不成立 → `divisor-equality-failure`)。**自認** | 便 63 F9 |
| **B63-3** | §6 の digest が `sha256(§x.y 本文)` という**計算式**で 64 桁 hex ではなく、heading 行・区切り・改行正規化の**境界規約も未定義**(同じ blob から複数の正当な section digest が出る)。ID も statement の説明(`"K^x / (K^x)^2"` 等)で versioned artifact ID でない。外部 dependency の digest を**自分の段落**へ向けていた | **section digest を全廃**し、**全 fragment を full-blob digest へ anchor**(便 63 F10.3 の最小形・裁定 75 の推奨)。`predicate_spec_id = "mb/ninfty-stage2-predicate/v6"` / `predicate_spec_digest = <発行時記入>` / `lemma_id = predicate_spec_id + "#anchor"` / `bound_blob_digest = predicate_spec_digest`。**byte-range 抽出規約の凍結を丸ごと回避**。外部 dependency は**外部 source artifact の versioned ID + digest 欄**として分離。**自認** | 便 63 F10 |
| **B63-4** | `NOT ISSUED / NOT AUTHORIZED / LOCKED` が**無時制**で、§9 も現行命令として再掲 | **§0.0 の `embedded_state_at_candidate_creation` + `live_status_authority` 分離形へ**。**§9 も時制付き**(receipt 前は禁止 / approved receipt 後は **receipt の scope に限って**認可)。**自認** | 便 63 F11 |

> **便 63 F9.2 の局所判断は保持**: `[15] pell-derivative-mismatch` と `[25] divisor-equality-failure` の同時例で **primary = [15]**。**18 段内部の順序方針そのものには Sol も反対していない。**

---

## 1. 数学核(**全文再掲・v5 から不変**)

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

### 1.2 補題 `N∞-N`(norm / divisor pushforward) {#N-inf-N}

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

### 1.3 系 `N∞-1:1`(局所 multiplicity 一致) {#N-inf-1to1}

> $Q\in\mu^{-1}(v)$ なら $\mu^\iota(Q)=C/v$。ゆえに
> $$ \boxed{\ \iota Q\in\mu^{-1}(v)\iff v^2=C\ } \tag{60.3} $$
> ($Q=\iota Q$ すなわち $y(Q)=0$ の場合も同じ: $\mu(Q)^2=\mu(Q)\mu^\iota(Q)=C$。**したがって $v^2\ne C$ の fiber に Weierstrass 点は存在しない**。)
> $v^2\ne C$ なら $\pi|_{\mu^{-1}(v)}$ は単射・unramified で、$(v-\mu^\iota)(Q)=(v^2-C)/v\ne0$ ゆえ他因子は単元。よって
> $$ \boxed{\ \operatorname{ord}_{x(Q)}H_v=\operatorname{ord}_Q(v-\mu)\ } \tag{60.4} $$
> したがって multiplicity partition が一致。さらに $v\ne0$ なら $H_v=-2v(a-w)$、$w=(v^2+C)/(2v)$。

### 1.4 命題 `N∞-fix`(fixed fiber の局所構造) {#N-inf-fix}

$v^2=C$ なら fiber 全体で $py=0$、$a(x_0)=v$。$\{py=0\}$ の三場合は exhaustive:

| 場合 | uniformizer | 導出 | 結果 |
|---|---|---|---|
| (i) $y_0=0,\ p(x_0)\ne0$ | $y$ | $\operatorname{ord}_Q(x-x_0)=2$ ゆえ $\operatorname{ord}_Q(a-v)\ge2$、$\operatorname{ord}_Q(py)=1$ | **$e=1$** |
| (ii) $p(x_0)=0,\ y_0\ne0$ | $x-x_0$ | $(a-v)(a+v)=f_6p^2$、$a(x_0)+v=2v\ne0$ ⟹ $\operatorname{ord}(a-v)=2m$;$\operatorname{ord}(py)=m$ | **$e=m:=\operatorname{ord}_{x_0}p$** |
| (iii) $p(x_0)=y_0=0$ | $y$ | $\operatorname{ord}_Q(p)=2m$、$\operatorname{ord}_Q(py)=2m+1$、$\operatorname{ord}_{x_0}(f_6p^2)=2m+1$ ⟹ $\operatorname{ord}_Q(a-v)=4m+2$ | **$e=2m+1$(奇数)** |

**⇒ (iii) から $e=2$ は出ない。**

### 1.5 補題 `N∞-pair`(十分側・**target 非依存**) {#N-inf-pair}

> $k=\bar{\mathbb Q}$ 上で $s^2=-C$ を選ぶ。$C\ne0$・標数 0 ゆえ $s\ne0$ かつ $s^2\ne C$。よって $\pm s$ の二 fiber は **non-fixed** で
> $$ H_{s}=-2s\,a,\qquad H_{-s}=+2s\,a \tag{N-pair-1} $$
> $$ \boxed{\ \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=\operatorname{rootpart}(a)\ } \tag{N-pair-2} $$

**証明.** (N-1) に $s^2=-C$ を代入して (N-pair-1)。$a(x_0)=0$ なら (Pell) より $p(x_0)^2f_6(x_0)=-C=s^2\ne0$、すなわち **$p(x_0)\ne0$ かつ $f_6(x_0)\ne0$** — 両 fiber は**自動的に非退化 locus**にある。$s^2\ne C$ ゆえ (60.4) が使え multiplicity が一致。∎
**この証明は S5 の target branch condition・`N∞-swap`・branch polynomial の計算を一切使わない。**

### 1.6 補題 `N∞-swap`(必要側) {#N-inf-swap}

> $\deg p=2$・$f_6$ squarefree の下で、**有限 branch fiber が二つとも $[2,2,1]$** かつ **有限 branch pair が $\{s,-s\}$**(系 S5-2a)ならば $\boxed{j(s)=-s,\ s^2=-C}$。

**証明.**
**(0) $j$-stability**: $\mu\circ\iota=C/\mu=j\circ\mu$。$\iota$ は $C_{\rm crv}$ の自己同型ゆえ **ramification locus を保ち**、$j$ は target の Möbius 自己同型ゆえ **branch-value set を保つ**。$j$ は $0,\infty$ を交換するから**有限二値 $\{s,-s\}$ は $j$-stable**。
**(1)** $j$-stable な二値集合は **fixed**($s^2=C$)か **swapped**($s\cdot(-s)=C$ ⟹ $s^2=-C$)。
**(2) fixed の排除**: `N∞-fix` より fixed fiber で $e=2$ が出るのは **(ii) の $m=2$** のみ。$\deg p=2$ ゆえ double root は唯一で、その $x_0$ が与える fixed value $a(x_0)$ も唯一。fixed case は $s$ と $-s$ の**双方**に $e=2$ 点を要求するが、$a(x_0)$ は一方にしかなれない($s\ne0$)。矛盾。∎

### 1.7 補題 `N∞-div` {#N-inf-div}

(Pell) を微分して $2aa'=p(f_6'p+2f_6p')$、$\gcd(a,p)=1$ より **$p\mid a'$**。
$\operatorname{rootpart}(a)=[2,2,1]$ のとき $d:=\operatorname{monic}\gcd(a,a')$ は $\deg d=2$・squarefree、$\gcd(p,d)=1$、$\deg a'=4=\deg p+\deg d$。ゆえに
$$ \boxed{\ a'\doteq p\,d,\qquad a'/p\doteq d\ } \tag{60.5} $$

### 1.8 定理 `N∞-criterion`(iff) {#N-inf-criterion}

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

### 4.1 schema {#cert-schema}

```text
divisor_equality_certificate = {
  schema_id, schema_digest, predicate_spec_id, predicate_spec_digest, candidate_ref,

  # --- 曲線とチャート ---
  curve_model_digest, chart_ids,

  # --- ambient algebra(B62-1)---
  ambient_coordinate_ring_schema_id  + digest    # ring と quotient relations
  ambient_quotient_relations                     # 明示(例: y^2 - f6(x))
  coefficient_field_presentation_id  + digest
  field_embedding_witness_schema_id  + digest
  monomial_order_id                  + digest
  groebner_reduction_contract_id     + digest    # normal form / reduction の規約

  # --- 各 lane の native(二対象)---
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

  # --- verifier / independence 証跡(§4.4)---
  verifier_evidence
}
```

### 4.2 `exact_point_equality_witnesses` の型【B62-1】 {#witness-type}

> **reduced Gröbner basis は ring と term order を固定して初めて一意になる。** ゆえに §4.1 の **`ambient_coordinate_ring_schema_id` + `ambient_quotient_relations` + `monomial_order_id` + `groebner_reduction_contract_id`** を**証明書から再検査できる形で束縛**したうえで、次のいずれかを witness とする。
> - **相互 ideal inclusion certificate**: $I_1\subseteq I_2$ と $I_2\subseteq I_1$ を、**固定 monomial order の reduced Gröbner basis に対する明示の表現係数**で。
> - **Bézout / reduction certificate**: $1=\sum u_ig_i$ の明示係数、または reduction 列。
> **異なる presentation の係数体を跨ぐ場合は `field_embedding_witness` を添える。**
> **⛔ 拒否**: 単なる digest 一致・最終 partition 一致・degree 一致。

### 4.3 運用条項 {#operational-clauses}

| # | 条項 |
|---|---|
| **G-1** | generator は**第三の判定 lane に数えない。単独で ACCEPT を出せない。** 両 native output から witness を作るだけ。 |
| **G-2** | **【v6・便 63 F9.3 で routing 分割】** 同一 event に二 code が割り当たらないよう次で分ける。**入力 / native / certificate の digest 不一致 → `digest-mismatch`[12]** / **equality witness の欠落・不成立 → `divisor-equality-failure`[25]**。いずれも `INTEGRITY_STOP`。**自認**(v5 の G-2 は digest 不一致を後者へ送っていた)。 |
| **G-3** | **A/B が独立 verifier で同じ certificate を検査する。単一 verifier を両 lane が oracle として信じることを禁止。** |
| **G-4** | **shared canonicalizer / math helper の再導入禁止** — 判定は §4.4 の**推移的依存閉包**で行う。generator が canonicalizer を内包しても、**両 verifier は witness を独立に再検査**する。 |
| **G-5** | §4.4 の independence evidence を freeze bundle に束縛。 |

### 4.4 independence evidence schema【B63-1・便 63 F8】 {#independence-evidence}

```text
independence_evidence = {
  generator_id  + code_digest + build_root_id + toolchain_id,
  verifier_A_id + code_digest + result_digest + build_root_id + toolchain_id
                + implementation_provenance,
  verifier_B_id + code_digest + result_digest + build_root_id + toolchain_id
                + implementation_provenance,

  dependency_manifest_schema_id + digest,     # manifest の型そのものを束縛
  dependency_closure_A[] = transitive content digests,   # 推移的閉包(直接依存のみは不可)
  dependency_closure_B[] = transitive content digests,

  allowed_shared_tcb[] = frozen content digests + role,  # 共有を許す trusted base
  forbidden_shared_math_helper_intersection
      = (dependency_closure_A ∩ dependency_closure_B) - allowed_shared_tcb
      = empty,

  verifier_contract_id + digest
}
```

| # | 条文 |
|---|---|
| **H-1** | **manifest は直接依存では不可。`dependency_closure_*` は推移的閉包の content digest 集合である。** |
| **H-2** | **同一性は content digest で判定する** — 別名・別 path・薄い wrapper は**同一 content digest を含む閉包**として現れるため区別されない。**path 改名を独立二実装と数える事故を防ぐため `build_root_id` / `toolchain_id` / `implementation_provenance` を receipt に残す。** |
| **H-3** | **`allowed_shared_tcb[]` は共有を許す trusted base を列挙する**(標準 runtime・schema parser・hash primitive 等)。**各項に `role` を付し、frozen content digest で固定する。** **数学的内容を持つ helper(canonicalizer・ideal 演算・divisor 正規化・partition 計算)を TCB に入れることを禁止。** |
| **H-4** | **交差の値は producer の自己申告を信じない。receipt 受領側が canonical content digest 集合から導出して再計算する。** 非空なら `INTEGRITY_STOP / shared-helper-detected`[11]。 |
| **H-5** | **`allowed_shared_tcb[]` への追加は挙証責任を追加側に置く**(freeze bundle の変更として receipt が要る)。 |

> **⚠ v5 の欠陥(自認)**: `shared_helper_intersection = ∅` だけでは、**閉包の深さ・同一性判定・helper の範囲・許される TCB** が未定義。文字どおり「全 helper」なら標準 runtime の共有で交差は通常空にならず、暗黙にそれらを除けば**共通 canonicalizer を除外した証拠にならない**(便 63 F8)。**空集合検査は必要な一部でしかなかった。**

---

## 5. certificate と verdict / reason

### 5.1 public envelope {#public-envelope}
`candidate_ref`(random opaque)/ `predicate_spec_id` + `predicate_spec_digest` / `searcher_id+digest` / `checker_id+digest` / `verdict` / **`primary_reason_code`(単数)** + **数学的射影 5 欄**(`finite_branch_count` / `finite_branch_pair_harmonic` / `a_root_partition` / `exceptional_locus_clear` / `ramification_sum`)。

### 5.2 `SEALED_INTERNAL` {#sealed-envelope}
```text
tuple_coefficients
searcher_native = { ramification_divisor_on_C, branch_divisor_on_P1,
                    finite_aggregate_partitions, native_artifact_digest }
checker_native  = { ramification_divisor_on_C, branch_divisor_on_P1,
                    finite_aggregate_partitions, native_artifact_digest }
divisor_equality_certificate, independence_evidence, partition_equality_result
all_reason_codes[]                      # canonical 整列(§5.3)
fibers[], fiber_refs[], branch_values, finite_branch_polynomial
artifact_digests
commitment = { hmac_of_tuple, key_holder="clean HMAC steward",
               reveal_after="Freeze 2" }
```
**⛔ 片側を他側の parser / canonicalizer で変換してから保存することを禁止。**

### 5.3 verdict state machine【B63-2・便 63 F9】 {#verdict-state-machine}

> **verdict の決定と reason の priority を分離する。** v5 は「全順序の最小」を public primary としたため、**`precondition/degree-mismatch`[1] と `sealed-field-leak`[9] の同時検出で REJECT[1] が選ばれ証拠汚染を隠す**(設計理由と逆転)。**自認。**

```text
# --- 検出順序: envelope-level check を early REJECT より先に実行 ---
step 1: envelope-level leak / digest / dependency checks   -> I に加算
step 2: mathematical precondition + T-1                    -> R に加算
step 3: cross-lane checks                                  -> I に加算

I = detected integrity reasons          # 18 段(§5.3.2)
R = detected mathematical reject reasons #  8 段(§5.3.1)

if I != empty:
    verdict          = INTEGRITY_STOP
    primary          = minimum(I, integrity_priority)
    all_reason_codes = canonical_sort(I ∪ R)
elif R != empty:
    verdict          = REJECT
    primary          = minimum(R, reject_priority)
    all_reason_codes = canonical_sort(R)
else:
    verdict          = ACCEPT
    primary          = accepted
    all_reason_codes = [accepted]

invariant 1: accepted appears iff I = R = empty      # accepted は他 code と排他
invariant 2: public は primary_reason_code のみを出す(単数・全域)
invariant 3: sealed は canonical 整列した all_reason_codes[] を保つ
invariant 4: 同一入力に対し (verdict, primary_reason_code) は一意
```

#### 5.3.1 `reject_priority`(**8 段**・decision lane のみ)
```text
[1] precondition/degree-mismatch
[2] precondition/f6-not-monic
[3] precondition/curve-not-squarefree
[4] precondition/leading-coeff-mismatch
[5] precondition/pell-violation
[6] precondition/divisor-orientation
[7] triple-root-of-a          # deg gcd(a,a',a'')>0 または gcd(a,a') 非 squarefree
[8] a-partition-mismatch      # それ以外の T-1 失敗
```

#### 5.3.2 `integrity_priority`(**18 段** — $26-9+1=18$)
```text
[ 9] sealed-field-leak                 # 証拠そのものが信用できない類(最優先)
[10] deterministic-digest-exposed
[11] shared-helper-detected            # §4.4 H-4
[12] digest-mismatch                   # 入力/native/certificate の digest 不一致(G-2)
[13] pell-implies-coprime-mismatch     # 定理が強制する恒等式の破れ
[14] divisor-identity                  # (Or) の破れ
[15] pell-derivative-mismatch          # (60.5)
[16] chart-degree-mismatch             # chart / locus の未処理
[17] p-locus-unhandled
[18] weierstrass-unhandled
[19] infinity-unhandled
[20] rh-mismatch                       # 大域整合
[21] extra-branch-value
[22] finite-branch-count-mismatch
[23] branch-pair-not-harmonic
[24] finite-partition-cross-mismatch
[25] divisor-equality-failure          # 二経路照合(witness 欠落・不成立: G-2)
[26] checker-mismatch
```
> **段数**: `[9]`–`[26]` で $26-9+1=18$。**v5 の「16 段」は表題 typo。自認。**
> **設計理由**: 証拠不信 [9]–[12] → 定理強制恒等式の破れ [13]–[15] → chart/locus 未処理 [16]–[19] → 大域整合 [20]–[24] → 二経路照合 [25]–[26]。
> **検証例**: `degree-mismatch`[1] + `sealed-field-leak`[9] 同時 ⟹ $I\ne\varnothing$ ゆえ **verdict = INTEGRITY_STOP, primary = [9]**(v5 の規則は誤って [1] を選んでいた)。`pell-derivative-mismatch`[15] + `divisor-equality-failure`[25] 同時 ⟹ **primary = [15]**(便 63 F9.2 の期待どおり)。

---

## 6. freeze bundle(**full-blob anchor 方式**)【B63-3・便 63 F10.3・裁定 75】 {#freeze-bundle}

> **section digest を全廃する。** 便 63 F10.1 のとおり `sha256(§x.y 本文)` は計算式であって literal hex でなく、**heading 行を含むか・次 heading 直前の空行や `---` を含むか・改行正規化をするか**が未定義なら**同じ blob から複数の正当な値**が出る(Sol が v3 §1.1 を自然な規約で再計算して `27252221b02abfcd` を得、記録値 `d7ee78c460bfec6e` と一致しなかったのがその実例)。**byte-range 抽出規約を凍結するより、全 fragment を full-blob digest へ anchor する方が小さく fail-closed。**

```text
predicate_spec_id     = "mb/ninfty-stage2-predicate/v6"
predicate_spec_digest = <64 hex: 本稿 exact blob の sha256 — 発行時に司令塔が記入>
encoding              = UTF-8, LF, no BOM, no normalization

# --- 定理群: ID は anchor 名のみ・digest は full blob 一本 ---
lemma_id( N-inf-N )           = predicate_spec_id + "#N-inf-N"
lemma_id( N-inf-1to1 )        = predicate_spec_id + "#N-inf-1to1"
lemma_id( N-inf-fix )         = predicate_spec_id + "#N-inf-fix"
lemma_id( N-inf-pair )        = predicate_spec_id + "#N-inf-pair"
lemma_id( N-inf-swap )        = predicate_spec_id + "#N-inf-swap"     # role: S5 target -> (60.6) RHS bridge
lemma_id( N-inf-div )         = predicate_spec_id + "#N-inf-div"
theorem_id( N-inf-criterion ) = predicate_spec_id + "#N-inf-criterion"
  dependency_closure = { #N-inf-N, #N-inf-1to1, #N-inf-fix,
                         #N-inf-pair, #N-inf-swap, #N-inf-div }
bound_blob_digest(all of the above) = predicate_spec_digest

# --- schema 群: 同じく anchor + full blob ---
schema_id( cert )              = predicate_spec_id + "#cert-schema"
schema_id( witness-type )      = predicate_spec_id + "#witness-type"
schema_id( operational )       = predicate_spec_id + "#operational-clauses"
schema_id( independence )      = predicate_spec_id + "#independence-evidence"
schema_id( public-envelope )   = predicate_spec_id + "#public-envelope"
schema_id( sealed-envelope )   = predicate_spec_id + "#sealed-envelope"
schema_id( verdict-machine )   = predicate_spec_id + "#verdict-state-machine"
bound_blob_digest(all of the above) = predicate_spec_digest

# --- 実装契約(§4.4 が要求する欄の実体)---
verifier_contract_id     = "mb/ninfty-verifier-contract/v1"
verifier_contract_digest = <64 hex: 契約 artifact の sha256 — 発行時に記入>
dependency_manifest_schema_id     = "mb/dependency-manifest/v1"
dependency_manifest_schema_digest = <64 hex — 発行時に記入>

# --- 外部 dependency: 自分の段落ではなく source artifact を束縛(F10.2)---
external_dependency[] = [
  { id = "S5/S5-4-infinity", digest = <64 hex of S5 source artifact> },
  { id = "S5/S5-3-infinity", digest = <64 hex of S5 source artifact> },
  { id = "S5/prop-S5-1",     digest = <64 hex of S5 source artifact> },
  { id = "S5/prop-S5-2",     digest = <64 hex of S5 source artifact> },
  { id = "S5/cor-S5-2a",     digest = <64 hex of S5 source artifact> }
]

# --- campaign / field 型(statement ではなく型宣言として保持)---
campaign_window_id              = K5
curve_coefficient_base_field_id = Q
geometric_working_field_id      = Qbar
prediction_base_field_id        = Q(zeta_20)
```
> **⚠ v5 の欠陥(自認)**: (i) digest が**計算式**で literal hex でなく、**境界規約が文書にも再現 script にも無かった**(後から値を選べる) — 便 63 F10.1。(ii) `squareclass_quotient_schema_id = "K^x / (K^x)^2"` 等は **versioned artifact ID ではなく statement の説明**で、`s5_4_infinity_dependency_id` の digest を **v5 §7 本文へ向けていた**(外部 dependency の identity を束縛せず、「依存すると書いた自分の段落」を束縛するだけ) — 便 63 F10.2。(iii) §4.4 が要求する `verifier_contract_id/digest` が §6 に無かった。**v6 は (i) を full-blob anchor で、(ii) を `external_dependency[]` で、(iii) を実装契約欄で閉じる。**
> **空欄の身分**: `<...— 発行時に記入>` は **freeze receipt 側で埋める欄**であり、本稿の blob には入らない(§0.0 の lifecycle 分離と同じ理由)。

---

## 7. whitelist / fixtures / EP / 役割分離

- **whitelist**: `branch_value_square -> squareclass(C) -> P1`。**型は §6 の field 欄が固定**($K=\mathbb Q(\zeta_{20})$・$i=\zeta_{20}^5$ ゆえ $-1=i^2\in K^{\times2}$ で $[s^2]=[C]$)。`aliases_blocked` は**非網羅列挙**で、新出力量を足す側に**挙証責任**。**deterministic commitment も同じ規則の対象。**
- **negative fixtures**: `ninfty-neg-01..08`、期待 `REJECT / triple-root-of-a`・`a_root_partition=[3,1,1]`・`triple_gcd_degree>0`・`gcd_squarefree=false` の **4 欄回帰**。**raw shard 名・命名パターン・digest は本稿に書かない**(sealed mapping)。**証拠の射程は `source-audited candidate`。**
- **EP**: same degree/schema・non-campaign coefficients。**EP 不在中は `partial predicate / UNKNOWN`。freeze 後も `calibrated detector` / `complete search` と呼ばない。**
- **役割分離**: **negative-lane runner $\ne$ clean HMAC steward。旧 mapping を知る tainted actor は steward 不可**(taint ledger の別欄 + 機械検査)。

---

## 8. Sol への監査依頼(v6)

1. **【必須】§4.4 の推移的閉包形**が便 63 F8 の 4 未定義項(閉包の深さ / 別名・wrapper の同一性 / helper の範囲 / 許される TCB)を閉じているか。とくに **H-3(数学的内容を持つ helper を TCB に入れない)** の線引きで足りるか。
2. **【必須】§5.3 の verdict state machine**が便 63 F9 の要求(verdict と priority の分離・`primary = minimum(I, integrity_priority)`・`accepted` 排他・envelope check を early REJECT より先)を満たすか。**二つの検証例の primary が期待どおりか。**
3. **【必須】§6 の full-blob anchor 方式**が便 63 F10.3 の最小形か。**`external_dependency[]` の digest 欄を「発行時に記入」で空にしたまま候補を提示する**運用でよいか(埋めれば blob digest が変わるため)。
4. **【必須】§0.0 の lifecycle 分離**が A62-2 と同型の修理として十分か。**§9 の時制付けで足りるか。**
5. **【推奨】§4.3 G-2 の routing 分割**(digest 不一致 → [12] / witness 欠落・不成立 → [25])が同一 event の二重割当を解消しているか。他に二重割当が残っていないか。
6. **【推奨】§1 の数学核**は v5 から不変(便 62 F7.1 の型修理を含む)。**再監査不要と扱ってよいか。**

---

## 9. 実装着手の条件(**時制付き**)【B63-4】

> **receipt 前**: 実装着手は**禁止**。searcher / checker / D-2 generator / 二 verifier のいずれについても、コードを書き始めてはならない。**model builder は LOCKED。**
> **approved receipt 後**: **その receipt が明示した scope に限って**認可される。scope 外(model builder の解錠・新しい lane の追加・`allowed_shared_tcb[]` の拡張)は**別の receipt を要する**。

$$ \boxed{\ \text{v6 の Sol 監査 PASS}\ \to\ \text{§6 の空欄を receipt 側で充填}\ \to\ \text{receipt の scope 内で searcher / checker / generator / 二 verifier を}\ \textbf{別々に}\ \text{実装}\ } $$

- **D-2 generator は判定 lane に数えない。二 verifier は独立実装で、§4.4 の禁止交差が空。**
- **EP が揃うまで札は `partial predicate / UNKNOWN`。**
- **旧 8 hit は neutral lane でのみ使う。runner ≠ clean HMAC steward。**
