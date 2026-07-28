# $N_\infty$ searcher — **stage 2 述語の仕様(spec v4)**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 73)。v3 を supersede。**
```text
supersedes_draft             = sha256:77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2
audited_predecessor_rejected = sha256:813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4
supersedes_v3                = sha256:83c9f58887a508d2bbe451a456e41e6ff19f5b2eaa6fdfb957516f6a57aede3b
predicate_spec_freeze_id     = NOT ISSUED
implementation_status        = NOT AUTHORIZED
model_builder status         = LOCKED
```
**正典**: `sol/sol_reply_61_apply_specv3.md` **F7–F13**(数学核 **全 PASS**・blocker B61-1/2/3・B9 束・F7.1 一語修理)・便 60 F6–F14・便 59・便 54。
**接触規律**: 値に依存しない。$C:=\hat c_\mu$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。

> **便 61 F7 の判定**: **6 補題 + `N∞-criterion` の数学核は全 PASS**(紙上監査であって Lean `verified` ではない)。**v4 が閉じるのは B61-1/2/3・B9 束・F7.1 の一語**である。

---

## 0. v3 → v4 差分

| ID | v3 | v4 | 出所 |
|---|---|---|---|
| **F7.1** | `N∞-N` step 2 で `N_pi : pi_* O_C^times -> O_P1^times` と書いた(**sheaf-unit と rational function の型が混在** — $v-\mu$ は零・極をもつ) | **体のノルム $N_{k(C_{\rm crv})/k(x)}:k(C_{\rm crv})^\times\to k(x)^\times$** に書き換え、**valuation identity** $\operatorname{ord}_PN(g)=\sum_{Q\mid P}[\kappa(Q):\kappa(P)]\operatorname{ord}_Q(g)$ を一行置いて**自己完結**させる。**外部文献の §/定理番号を freeze 前件にしない**。**自認** | 便 61 F7.1 |
| **B61-1** | D-2 の本体が「差の divisor が 0 であることの exact な証明書」の**一文だけ**(目標命題の言い直し)。`divisor_equality_cert_schema_id` に **digest なし** | **§4 に full schema を設置**(field list・witness の exact 再検査可能形・verifier contract)。**generator は第三判定 lane に数えず ACCEPT を単独で出せない**・**欠落/検証失敗/digest 不一致 = `INTEGRITY_STOP / divisor-equality-failure`**・**shared canonicalizer/helper の再導入禁止**・**二独立 verifier**。**「D-2 は名前だけで D-1 より独立ではない」も明記**(v3 の比較は強すぎた。**自認**) | 便 61 F9 |
| **B61-2** | `SEALED_INTERNAL` が `finite_aggregate_partitions` / divisor を**各 1 個**しか持たず、**二 lane を表せない** | **`searcher_native{...}` と `checker_native{...}` を別々に保存**+`divisor_equality_certificate`+`partition_equality_result`。**片側を他側の parser/canonicalizer で変換してから保存することを禁止**。**自認** | 便 61 F10 |
| **B61-3** | 閉じた enum に **ACCEPT 用 code が無く正の certificate を型付けできない**・T-1/precondition の複数同時 failure に**優先順位が無い**・**E-4 exact PASS 後の $\gcd(a,p)\ne1$ を REJECT にしていた** | **`accepted` を新設**・**T-1 と precondition の total order を凍結**・**E-6 は E-4+$C\ne0$ から自動ゆえ `INTEGRITY_STOP / pell-implies-coprime-mismatch`**。**自認** | 便 61 F11 |
| **B9 束** | §7 に記述しただけで **freeze bundle に 4 欄が無い** | **freeze bundle に `prediction_base_field_id` / `minus_one_square_proof_id` / `squareclass_quotient_schema_id` / `s5_4_infinity_dependency_id` を追加** | 便 61 F12 |
| **F12 問 6** | `predicate_theorem_id + dependency 4 lemmas` の**省略形** | **7 補題を実 ID・digest で全列挙**(`N∞-N` / `N∞-1:1` / `N∞-fix` / `N∞-pair` / `N∞-swap` / `N∞-div` / `N∞-criterion`) | 便 61 F12 |
| **F7.4** | (60.6) の RHS に `for some s^2=-C` を含むため、**右→左だけなら `N∞-swap` は論理的に冗長** | **dependency 表記を精密化**(§1.9): `N∞-pair`+RH → RHS / **S5 target + `N∞-swap` → RHS** という **bridge の役**として明記 | 便 61 F7.4 |

---

## 1. 数学核

> **v3 §1 の補題群は便 61 F7 で全 PASS。** 以下は **statement を再掲**し、**変更があった `N∞-N` の証明のみ差し替える**。証明の全文は v3(`sha256:83c9f588…`)§1 を参照(**digest 束縛つき参照**)。

### 1.1 設定
$$ C_{\rm crv}:y^2=f_6(x)\ (\deg f_6=6,\ \text{monic squarefree}),\quad \mu=a+py\ (\deg a=5,\deg p=2,\ a_5=p_2\ne0) $$
$$ \textbf{(Pell)}\ a^2-f_6p^2=C\in\mathbb Q^\times,\qquad \textbf{(Or)}\ (\mu)=5P_0-5P_\infty,\qquad j(v):=C/v $$

### 1.2 補題 `N∞-N`【**F7.1 で型修理**】
$$ H_v:=(v-\mu)(v-\mu^\iota)=v^2-2va+C,\qquad \operatorname{div}_{\mathbb P^1_x}(H_v)=\pi_*\operatorname{div}_{C_{\rm crv}}(v-\mu)=\pi_*[\mu^{-1}(v)]-5[\infty_x] \tag{60.1} $$
$$ \boxed{\ (H_v)_0=\pi_*[\mu^{-1}(v)]\ } \tag{60.2} $$

**証明 artifact(自己完結形).**
1. **norm 恒等式**: $\mu\mu^\iota=C$、$\mu+\mu^\iota=2a$ より $(v-\mu)(v-\mu^\iota)=v^2-2va+C$。左辺は $\iota$-不変なので $k(x)$ に属し、それが $H_v$。
2. **【F7.1・型修理】体のノルム**: $k(C_{\rm crv})/k(x)$ は次数 2 の分離拡大で、
$$ N:=N_{k(C_{\rm crv})/k(x)}:\ k(C_{\rm crv})^\times\longrightarrow k(x)^\times,\qquad N(g)=g\cdot g^\iota $$
であり $H_v=N(v-\mu)$。**各 closed point $P\in\mathbb P^1_x$ で**
$$ \boxed{\ \operatorname{ord}_P N(g)=\sum_{Q\mid P}[\kappa(Q):\kappa(P)]\operatorname{ord}_Q(g)\ } \tag{61.1} $$
が成り立つ(Dedekind 環の拡大に対する norm と valuation の関係)。(61.1) の右辺は定義により $\pi_*\operatorname{div}(g)$ の $P$ での係数だから、$\operatorname{div}(N(g))=\pi_*\operatorname{div}(g)$。
3. **極の勘定**: $\operatorname{div}(v-\mu)=[\mu^{-1}(v)]-5P_\infty$((Or))、$\pi_*(5P_\infty)=5[\infty_x]$。以上で (60.1)、零部分を取って (60.2)。∎

> **⚠ v3 の型混在(自認)**: v3 は `N_pi : pi_* O_C^times -> O_P1^times` と sheaf-unit の射で書いたが、**$v-\mu$ は零と極をもつので unit sheaf には属さない**(便 61 F7.1)。**v4 は体のノルムと (61.1) で書き直した。**
> **★ (61.1) を証明 artifact に置いたので、外部文献の §/定理番号を freeze の前件にする必要はない**(便 61 F7.1 の指示どおり)。

### 1.3〜1.7 その他の補題【v3 から不変・便 61 F7.2–F7.5 で PASS】

| ID | statement | 便 61 |
|---|---|---|
| **`N∞-1:1`** | $\iota Q\in\mu^{-1}(v)\iff v^2=C$ (60.3);$v^2\ne C$ なら Weierstrass 点不在・$\pi$ は unramified・$(v-\mu^\iota)(Q)=(v^2-C)/v\ne0$ ゆえ $\operatorname{ord}_{x(Q)}H_v=\operatorname{ord}_Q(v-\mu)$ (60.4) | F7.2 **PASS** |
| **`N∞-fix`** | $v^2=C$ なら fiber は $\{py=0\}$ 上。(i) $e=1$ / (ii) $e=m$ / (iii) $e=2m+1$(奇) | 便 60 F6.3 **PASS** |
| **`N∞-pair`** | $s^2=-C$ なら $H_{\pm s}=\mp2sa$、両 fiber は non-fixed で $\operatorname{part}=\operatorname{rootpart}(a)$。**target 非依存** | F7.3 **PASS** |
| **`N∞-swap`** | $\mu\circ\iota=j\circ\mu$ ⟹ branch set は $j$-stable。有限二 fiber が両方 $[2,2,1]$ かつ pair が $\{s,-s\}$ なら **$j(s)=-s$、$s^2=-C$** | F7.4 **PASS** |
| **`N∞-div`** | $p\mid a'$;T-1 通過時 $d=\operatorname{monic}\gcd(a,a')$ は deg 2 squarefree・$\gcd(p,d)=1$ ゆえ次数比較で $a'\doteq pd$、$a'/p\doteq d$ (60.5) | F7.5 **PASS** |

### 1.8 定理 `N∞-criterion`【便 61 F7.6 で PASS】
E-1〜E-6 の下で
$$ \boxed{\ \operatorname{rootpart}(a)=[2,2,1]\iff \begin{array}{c}\operatorname{Br}(\mu)=\{0,s,-s,\infty\}\ \text{for some}\ s^2=-C,\\ \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=[2,2,1]\end{array}\ } \tag{60.6} $$
**十分方向**は $\bar{\mathbb Q}$ へ base change し、$\deg R_\mu=2g-2+2\deg\mu=12$ を $4+4+2+2$ で使い切る。**different coefficient $e_Q-1$ は非負**なので、$\bar{\mathbb Q}$ にのみ定義される点を含め他の ramification point は存在できない。

### 1.9 dependency の精密化【**F7.4**】

> **(60.6) の RHS は既に `for some $s^2=-C$` を含むため、右→左だけを示すなら `N∞-swap` は論理的に冗長**である(便 61 F7.4)。正確な依存は:
> ```text
> N∞-pair + RH                        -> rootpart(a)=[2,2,1] から (60.6) RHS
> S5 target(E-7 + two [2,2,1] fibers)
>   + N∞-swap                         -> (60.6) RHS
> ```
> **v4 の選択**: **`N∞-swap` を「S5 target を (60.6) の RHS へ入れる bridge」と呼ぶ**(RHS から $s^2=-C$ を外す案は採らない — RHS が stage 2 の必要 signature を直接述べる形を保つため)。**freeze dependency 表(§6)もこの呼び方で統一する。**

---

## 2. 入口契約 / target condition【v3 から不変】

**raw precondition** E-1(monic squarefree, $\deg f_6=6$)/ E-2($\deg a=5,\deg p=2$)/ E-3($a_5=p_2\ne0$)/ E-4((Pell))/ E-5(divisor orientation)/ E-6($\gcd(a,p)=1$)。
**target condition** E-7(有限 branch 値が調和対 $\{s,-s\}$・**系 S5-2a**)。
**出所**: E-1〜E-4 = **S5-3∞**(+便 36 F2.1)/ E-5 = **命題 S5-1**(+S5-3∞ との同値)/ E-7・分岐型 = **系 S5-2a** / $\lambda=c\mu^2$ = **命題 S5-2**。

> **【B61-3】E-6 の身分**: **E-6 は E-4 の (Pell) と $C\ne0$ から自動**(共通根があれば $C=0$)。したがって **E-4 を exact に PASS した後の $\gcd(a,p)\ne1$ は candidate の REJECT ではなく、定理または実装の矛盾**である(§5)。

---

## 3. 述語(decision lane / audit lane)【v3 から不変・§5 で verdict を total 化】

```text
decision lane: E-1..E-6 + rootpart(a)=[2,2,1]   (T-1)
audit lane A : local differential -> R on C -> mu_* R          (searcher)
audit lane B : proven-baseline saturated elimination           (checker)
```
**T-1**: $\deg\gcd(a,a')=2$・$\gcd(a,a')$ squarefree・$\deg\gcd(a,a',a'')=0$。
**T-2**〜**T-8**: (60.5) の逐語検査 / $p$-locus / Weierstrass / 二 infinity / harmonic boolean / RH 12 / **両 lane の finite aggregate partitions 比較**。
**T-1 通過後の不一致はすべて `INTEGRITY_STOP`**(定理 `N∞-criterion` が target signature を強制するため)。

---

## 4. divisor equality certificate(D-2)【B61-1】

> **★ 先に v3 の言い過ぎを撤回する(自認)**: v3 §4.2 は「D-1 は canonicalizer が第三実装となり**必ず**共通 bug 経路になる」と書いたが、**強すぎる**(便 61 F9)。**D-1 でも二 lane が仕様だけを共有して canonicalizer を独立実装すれば単一 shared implementation にはならない**し、逆に **D-2 でも一つの generator/verifier を両 lane が oracle として信じればそれが共通 bug 経路になる**。**D-2 は名前だけで D-1 より独立なのではない** — 独立性は**下の運用条項が担保する**。

### 4.1 schema

```text
divisor_equality_certificate = {
  schema_id, schema_digest,
  predicate_freeze_id,
  candidate_ref,                       # opaque(値の関数でない)

  curve_base_field_id,                 # 係数体と数体表現の規約
  curve_model_digest,
  chart_ids,                           # 固定 projective coordinates 込み

  searcher_native_divisor_ref, searcher_native_artifact_digest,
  checker_native_divisor_ref,  checker_native_artifact_digest,

  component_bijection,                 # 両 native の成分の対応
  exact_point_equality_witnesses,      # 下記 4.2
  multiplicity_equalities,             # 対応成分ごとの重複度一致
  chart_overlap_witnesses,             # affine / infinity chart の重複除去
  total_coverage_and_no_extra_component_witness,
  pushforward_compatibility_witness,   # mu_* が両 native で一致

  verifier_contract_id, verifier_contract_digest
}
```

### 4.2 `exact_point_equality_witnesses` の型(**exact に再検査可能な形**)

> presentation が違う algebraic point を対応させる witness は、**固定 ambient coordinate ring 上で exact に再検査できる形**でなければならない。許される形:
> - **相互 ideal inclusion certificate**: $I_1\subseteq I_2$ と $I_2\subseteq I_1$ を、**固定 monomial order の reduced Gröbner basis に対する明示の表現係数**で与える。
> - **Bézout / reduction certificate**: $1=\sum u_ig_i$ 型の明示係数、または reduction 列。
> **⛔ 拒否**: **単なる digest 一致・最終 partition 一致・degree 一致は divisor equality certificate ではない。**

### 4.3 運用条項(独立性を担保する部分)

| # | 条項 |
|---|---|
| **G-1** | **certificate generator は第三の判定 lane に数えない。ACCEPT を単独で出せない。** 両 native output を受け取って **witness を作るだけ**。 |
| **G-2** | **欠落・検証失敗・入力 digest 不一致はすべて `INTEGRITY_STOP / divisor-equality-failure`。** |
| **G-3** | **searcher 側と checker 側が独立 verifier で同じ certificate を検査する**(または同等の二実装検査)。**単一 verifier を両 lane が oracle として信じることを禁止**(便 61 F9)。 |
| **G-4** | **shared canonicalizer / helper の再導入を禁止。** generator が canonicalizer を内包する場合も、**両 verifier はそれを信じず witness を独立に再検査**する。 |
| **G-5** | `verifier_contract_id + digest` を freeze bundle に束縛(§6)。 |

---

## 5. certificate schema(public / sealed)と verdict の total order

### 5.1 public envelope【v3 から不変】
`candidate_ref`(random opaque)/ `predicate_spec_freeze_id` / `searcher_id+digest` / `checker_id+digest` / `verdict` / `reason_code` + **数学的射影 5 欄**(`finite_branch_count` / `finite_branch_pair_harmonic` / `a_root_partition` / `exceptional_locus_clear` / `ramification_sum`)。

### 5.2 `SEALED_INTERNAL`【**B61-2 — 二 lane を別々に保存**】

```text
SEALED_INTERNAL = {
  tuple_coefficients

  searcher_native = {                        # lane A の native output
    ramification_divisor_on_C,
    branch_divisor_on_P1,
    finite_aggregate_partitions,             # [[2,2,1],[2,2,1]]
    native_artifact_digest
  }
  checker_native = {                         # lane B の native output
    ramification_divisor_on_C,
    branch_divisor_on_P1,
    finite_aggregate_partitions,
    native_artifact_digest
  }

  divisor_equality_certificate               # §4
  partition_equality_result                  # T-8 の比較結果

  fibers[], fiber_refs[], branch_values, finite_branch_polynomial
  artifact_digests
  commitment = { hmac_of_tuple, key_holder="clean HMAC steward",
                 reveal_after="Freeze 2" }
}
```

> **⛔【B61-2】片側を他側の parser / canonicalizer で変換してから保存することを禁止する。** 各 native は**その lane が生成したままの表現**で保存し、`native_artifact_digest` と D-2 witness で相互束縛する。
> **⚠ v3 の欠陥(自認)**: v3 は `finite_aggregate_partitions` / divisor を**各 1 個**しか持たず、`[[2,2,1],[2,2,1]]` は**二 fiber**を表すだけで**二 lane を表さなかった**。**独立再構成の証拠が receipt に残らなかった**(便 61 F10)。

### 5.3 **verdict / reason の total order**【B61-3】

```text
ACCEPT:
    reason_code = accepted                       # ← v4 で新設(F11)

REJECT(decision lane のみ):
  precondition(複数 failure は下の固定 priority で単数化):
    1. precondition/degree-mismatch
    2. precondition/f6-not-monic
    3. precondition/curve-not-squarefree
    4. precondition/leading-coeff-mismatch
    5. precondition/pell-violation
    6. precondition/divisor-orientation
  T-1 fail:
    if deg gcd(a,a',a'') > 0  or  gcd(a,a') is not squarefree:
        REJECT / triple-root-of-a
    else:
        REJECT / a-partition-mismatch

INTEGRITY_STOP:
  E-4 exact pass but gcd(a,p) != 1:
        INTEGRITY_STOP / pell-implies-coprime-mismatch      # ← v4(F11)
  T-1 通過後の不一致(すべて):
        pell-derivative-mismatch, p-locus-unhandled, weierstrass-unhandled,
        infinity-unhandled, chart-degree-mismatch, divisor-identity, rh-mismatch,
        branch-pair-not-harmonic, extra-branch-value,
        finite-branch-count-mismatch, finite-partition-cross-mismatch,
        divisor-equality-failure, digest-mismatch, checker-mismatch,
        sealed-field-leak, deterministic-digest-exposed
```

> **★ total 性の保証**: **(a)** 全 verdict に対応する code が存在する(`accepted` を新設)/ **(b)** 複数同時 failure は**固定 priority で単数化**される/ **(c)** 各到達状態に **verdict は一意**(T-1 後は必ず `INTEGRITY_STOP`)。
> **⚠ v3 の欠陥(自認)**: v3 の enum には **ACCEPT 用 code が無く、正の certificate を一件も型付けできなかった**。また `triple-root-of-a` と `a-partition-mismatch` は**同時に成り立ちうる**のに優先順位が無かった。さらに **E-4 PASS 後の $\gcd(a,p)\ne1$ を REJECT にしていた**が、E-6 は E-4 から自動なので**矛盾 = `INTEGRITY_STOP`** が正しい(便 61 F11)。
> **代替案(採らない)**: 単数 `reason_code` の代わりに **canonical に整列した `reason_codes[]`** を持つ設計もありうる(便 61 F11)。**v4 は単数欄 + 固定 priority を選ぶ**(public envelope の型を単純に保つため)。**選択は freeze 時に司令塔が確認。**

---

## 6. freeze bundle【B9 束 + F12 問 6 の全列挙】

```text
freeze_bundle = {
  # --- campaign / field 型(B9)---
  campaign_window_id              = K5
  curve_coefficient_base_field_id = Q
  prediction_base_field_id        = Q(zeta_20)
  squareclass_quotient_schema_id  + digest        # K^x / (K^x)^2
  minus_one_square_proof_id       + digest        # i = zeta_20^5 in K, -1 = i^2
  s5_4_infinity_dependency_id     + digest        # c_hat = 1 => C alone fixes P1

  # --- 定理群(省略形を使わず全列挙・F12 問 6)---
  lemma_N_inf_N_id           + digest
  lemma_N_inf_1to1_id        + digest
  lemma_N_inf_fix_id         + digest
  lemma_N_inf_pair_id        + digest
  lemma_N_inf_swap_id        + digest             # role: S5 target -> (60.6) RHS bridge
  lemma_N_inf_div_id         + digest
  theorem_N_inf_criterion_id + digest             # dependency closure = 上の 6 補題

  # --- schema 群 ---
  divisor_equality_cert_schema_id + digest
  verifier_contract_id            + digest
  public_certificate_schema_id    + digest
  sealed_certificate_schema_id    + digest
  reason_code_enum_id             + digest

  # --- provenance ---
  s5_source_map = { E-1..E-4: S5-3-infinity(+便36 F2.1),
                    E-5: S5-1(+S5-3-infinity),
                    E-7 & branch type: S5-2a,
                    lambda = c mu^2: S5-2 }
}
```
**`predicate_theorem_id + dependency 4 lemmas` という省略は freeze 文として使わない。**

---

## 7. whitelist / fixtures / EP / 役割分離【v3 から不変】

- **whitelist**: `branch_value_square -> squareclass(C) -> P1`。**型は §6 の 4 欄が固定**(`prediction_base_field_id` = $K=\mathbb Q(\zeta_{20})$ 等)。`aliases_blocked` は**非網羅列挙**で、新出力量を足す側に挙証責任。
- **negative fixtures**: `ninfty-neg-01..08`、期待 `REJECT / triple-root-of-a`・`a_root_partition=[3,1,1]`・`triple_gcd_degree>0`・`gcd_squarefree=false` の **4 欄回帰**。raw shard 名・命名パターン・digest は本稿に書かない(sealed mapping)。**証拠の射程は `source-audited candidate`**(便 60 F10.2)。
- **EP**: same degree/schema・non-campaign coefficients。**EP 不在中は `partial predicate / UNKNOWN`。freeze 後も `calibrated detector` / `complete search` と呼ばない。**
- **役割分離**: **negative-lane runner $\ne$ clean HMAC steward**。**旧 mapping を知る tainted actor は steward 不可**(taint ledger に別欄 + 機械検査)。

---

## 8. Sol への監査依頼(v4)

1. **【必須】(61.1) の valuation identity**(§1.2 step 2)。$k(C_{\rm crv})/k(x)$ が次数 2 分離拡大・$\pi$ が有限という設定で、**この一行を証明 artifact として自己完結と見てよいか**(便 61 F7.1 の指示どおり外部 §番号を前件にしていない)。
2. **【必須】§4.2 の witness 型**が「exact に再検査できる形」の要件を満たすか(相互 ideal inclusion の**表現係数**・Bézout/reduction)。**固定 monomial order と ambient coordinate ring の宣言が §4.1 の `curve_base_field_id` / `chart_ids` で足りるか。**
3. **【必須】§4.3 の G-1〜G-5** が、便 61 F9 の「D-2 は名前だけで D-1 より独立ではない」への十分な回答になっているか。**とくに G-3(二独立 verifier)と G-4(shared canonicalizer 禁止)。**
4. **【推奨】§5.3 の priority 順**(precondition 6 段・T-1 の 2 分岐)。**単数 `reason_code` + 固定 priority と、canonical 整列 `reason_codes[]` のどちらを freeze すべきか。**
5. **【推奨】§1.9 の dependency 表記**。`N∞-swap` を「S5 target → (60.6) RHS の bridge」と呼ぶ選択(RHS から $s^2=-C$ を外さない)でよいか。
6. **【推奨】§1 の「v3 を digest 束縛で参照」形式**。**freeze artifact として自己完結性が不足しないか**(不足なら v5 で全文再掲する)。

---

## 9. 実装着手の条件

$$ \boxed{\ \text{v4 の Sol 監査 PASS}\ \to\ \text{§6 の freeze bundle を全列挙で発行}\ \to\ \text{searcher / checker / D-2 generator / 二 verifier を}\ \textbf{別々に}\ \text{実装}\ } $$

- **実装着手禁止は継続**(`implementation_status = NOT AUTHORIZED`)。
- **D-2 generator は判定 lane に数えない。二 verifier は独立実装。**
- **EP が揃うまで札は `partial predicate / UNKNOWN`。**
- **旧 8 hit は neutral lane でのみ使う。runner ≠ clean HMAC steward。**
