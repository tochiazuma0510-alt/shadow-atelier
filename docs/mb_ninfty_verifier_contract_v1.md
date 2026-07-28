# `mb/ninfty-verifier-contract/v1` — divisor equality certificate の検査契約

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 76)。**
**この文書は `mb/ninfty-stage2-predicate/v6` §4.4 の `verifier_contract_id` が指す実体である。**

## 0. lifecycle state {#lifecycle}

```text
embedded_state_at_candidate_creation = {
  contract_freeze_id: NOT ISSUED,
  verifier_implementation: NOT AUTHORIZED
}
live_status_authority = Sol freeze reply + commander receipt
live_freeze_and_authorization_authority = approved freeze receipt
```
**上記 blob は candidate 作成時点で埋め込まれた状態であって live status ではない。live status の正本は approved freeze receipt 側にあり、receipt 発行によって本稿を書き換える必要はない(digest 不変)。**

```text
contract_id     = "mb/ninfty-verifier-contract/v1"
contract_digest = <64 hex: 本稿 exact blob の sha256 — 発行時に司令塔が記入>
encoding        = UTF-8, LF, no BOM, no normalization
governing_spec  = "mb/ninfty-stage2-predicate/v6"
governing_spec_digest = <64 hex — 発行時に記入>
```
**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。
**優先関係**: 本稿と governing spec が矛盾した場合、**governing spec が優先**する。本稿は spec §4.1–§4.4 の**手続き的具体化**であって、新しい数学的前件を導入しない。

---

## 1. 役割と非役割 {#role}

| # | 条項 |
|---|---|
| **V-0** | verifier は **`divisor_equality_certificate` を検査する装置**であり、**判定 lane ではない**。verifier は candidate に対する `ACCEPT` を**単独で出せない**。出力は `PASS` / `FAIL(reason)` の 2 値と、その根拠となる再計算結果の digest のみ。 |
| **V-1** | verifier は **searcher / checker の native 出力を再生産しない**。両 native は入力として受け取り、**certificate の witness が両者を実際に同一視しているか**だけを検査する。 |
| **V-2** | **generator は verifier ではない**(spec §4.3 G-1)。generator が作った witness を、**A と B が独立に再検査**する(G-3)。 |
| **V-3** | verifier は **`SEALED_INTERNAL` の値を public envelope へ写さない**。検査に用いた量は digest でのみ参照する。 |

---

## 2. 検査対象 {#scope}

入力は spec v6 §4.1 の `divisor_equality_certificate` 全体と、それが参照する両 native artifact。検査対象の witness 群は次の 6 種:

```text
W-1  component_bijection
W-2  exact_point_equality_witnesses              # spec §4.2
W-3  multiplicity_equalities
W-4  chart_overlap_witnesses
W-5  total_coverage_and_no_extra_component_witness
W-6  pushforward_compatibility_witness
```
両 native は各々 **2 対象**(`ramification_divisor_on_C_ref`・`branch_divisor_on_P1_ref`)を持つ。**W-1〜W-6 は 2 対象それぞれについて検査する**(片方だけの PASS を全体の PASS としない)。

---

## 3. 検査手続き {#procedure}

### 3.0 前段: ambient の固定を再検査

W-2 の再計算に入る前に、spec §4.1 の ambient 欄が**証明書から再検査できる形で束縛されているか**を確かめる。

```text
P-0.1  ambient_coordinate_ring_schema_id + digest が存在し、digest が実体と一致
P-0.2  ambient_quotient_relations が明示されている
P-0.3  coefficient_field_presentation_id + digest が存在し一致
P-0.4  monomial_order_id + digest が存在し一致
P-0.5  groebner_reduction_contract_id + digest が存在し一致
P-0.6  異 presentation を跨ぐ witness には field_embedding_witness が添付されている
```
**いずれか不成立なら即 `FAIL(digest-mismatch)` または `FAIL(divisor-equality-failure)`(§5 の routing に従う)。**
**理由**: reduced Gröbner basis は ring と term order を固定して初めて一意になる。固定が再検査できない状態で W-2 を「再計算した」と称してはならない。

### 3.1 W-2 の再検査(**verifier の中核**)

certificate が採る形式に応じて次のいずれかを**verifier 自身が再計算**する。**generator の主張する結論を読み取るだけの検査は PASS としない。**

| 形式 | 再計算内容 | PASS 条件 |
|---|---|---|
| **相互 ideal inclusion certificate** | 各生成元 $g\in G_1$ について、certificate が与える**表現係数** $\{u_i\}$ から $\sum u_i h_i$ を `groebner_reduction_contract_id` の規約で計算し、$g$ と**係数まで**一致するかを見る。$G_2\subseteq I_1$ も同様。 | **両方向の全生成元**について一致 |
| **Bézout / reduction certificate** | $1=\sum u_i g_i$ を明示係数から**展開して**評価、または reduction 列を**一段ずつ**再実行する。 | 展開結果が $1$、または reduction 列の各段が規約どおりで終端が $0$ |

```text
P-1.1  表現係数がすべて存在する(欠落生成元があれば FAIL)
P-1.2  再計算が固定 monomial order・固定 reduction 規約の下で行われた
P-1.3  再計算結果が certificate の主張と一致する
P-1.4  異体 presentation を跨ぐ場合、field_embedding_witness の像が一致する
```

> **⛔ 以下は W-2 の PASS 根拠にならない**(spec §4.2 の拒否条項の再掲):
> - 単なる digest 一致
> - 最終 partition の一致
> - degree の一致
> - generator の内部 canonicalizer が「等しい」と述べたこと

### 3.2 W-1・W-3〜W-6

| # | 再計算内容 | PASS 条件 |
|---|---|---|
| **W-1** | 両 native の component 集合の間の全単射を、**W-2 の点同一性から独立に構成し直す** | 構成した対応が certificate の `component_bijection` と一致し、両側とも全域・単射 |
| **W-3** | 対応する component 対の multiplicity を両 native から読み、**整数として比較** | 全対で一致 |
| **W-4** | chart 重なり上で、両 chart の記述が同じ component を与えるかを再計算 | 全重なりで一致 |
| **W-5** | 両 native の component 総数と、W-1 の像の大きさを比較 | **被覆に漏れがなく、対応外の余剰 component が両側に存在しない** |
| **W-6** | `ramification_divisor_on_C` の pushforward が `branch_divisor_on_P1` と整合するかを、multiplicity の和として再計算 | 全 branch point で一致 |

**W-5 の注意**: 「余剰が無い」は**両側**について確かめる。片側の被覆だけでは、他方に余分な component がある場合を見逃す。

### 3.3 入出力の束縛

```text
P-3.1  certificate の predicate_spec_id / predicate_spec_digest が governing spec と一致
P-3.2  certificate の schema_id / schema_digest が spec §4.1 の anchor と一致
P-3.3  両 native の native_artifact_digest が、verifier が実際に読んだ blob の digest と一致
P-3.4  verifier の出力 record は result_digest を持ち、その中身は
       { contract_id, contract_digest, certificate_digest,
         searcher_native_artifact_digest, checker_native_artifact_digest,
         per_witness_results[W-1..W-6], verdict } の canonical serialization
```
**P-3.3 の不一致は「検査対象が入れ替わっている」ことを意味するので、witness の成否に関わらず即停止。**

---

## 4. 合否規準 {#verdict}

```text
verifier_verdict = PASS   iff   P-0.* ∧ P-1.* ∧ (W-1..W-6 すべて PASS) ∧ P-3.*
                 = FAIL(reason)   otherwise
```
- **PASS は「certificate が両 native の同一性を実際に証明している」ことのみを主張する。** candidate の数学的判定(ACCEPT/REJECT)は述べない。
- **A と B の verdict が食い違った場合、両者を FAIL として扱う**(`checker-mismatch` ではなく、後述の routing に従う)。**多数決・片側採用を禁止。**

---

## 5. `INTEGRITY_STOP` 条件と routing {#integrity}

**spec v6 §4.3 G-2 の分割を厳守する**(同一 event に二 code を割り当てない)。

| 事象 | reason code(spec §5.3.2 の段) |
|---|---|
| 入力 / native / certificate の **digest 不一致**(P-0.1・P-0.3〜P-0.5 の digest 欄、P-3.1〜P-3.3) | **`digest-mismatch` [12]** |
| **witness の欠落・不成立**(P-0.2・P-0.6・P-1.*・W-1〜W-6 のいずれか) | **`divisor-equality-failure` [25]** |
| §6 の独立要件の破れ(closure の禁止交差が非空) | **`shared-helper-detected` [11]** |
| A/B の verdict 不一致 | **`divisor-equality-failure` [25]**(**証拠が両立しないため。`checker-mismatch` [26] は searcher/checker の native 同士の不一致に予約**) |
| verifier が sealed 値を public 面に露出させた | **`sealed-field-leak` [9]** |

**上記はすべて `INTEGRITY_STOP` であり、REJECT ではない。** verdict の決定と primary の選択は spec v6 §5.3 の state machine が行う — **本稿は reason code を供給するだけで、自ら verdict を宣言しない。**

---

## 6. 二 verifier の独立要件 {#independence}

**`mb/dependency-manifest/v1` の H-1〜H-5 を参照する。** 本稿はそれを verifier 側の義務として再掲する。

| # | 義務 |
|---|---|
| **C-1** | A と B は **別実装**であり、`dependency_closure_A[]` / `dependency_closure_B[]` を **推移的閉包**として提出する(**直接依存のみの manifest は不可** — H-1)。 |
| **C-2** | 同一性は **content digest** で判定される。別名・別 path・薄い wrapper では独立性を主張できない(H-2)。 |
| **C-3** | 共有してよいのは `allowed_shared_tcb[]` に列挙された frozen content digest のみ。**数学的内容を持つ helper(canonicalizer・ideal 演算・divisor 正規化・partition 計算)を TCB に入れてはならない**(H-3)。**§3 の再計算は A・B が各々の実装で行う。** |
| **C-4** | 禁止交差の値は **receipt 受領側が canonical content digest 集合から再導出**する。verifier の自己申告を信じない(H-4)。 |
| **C-5** | `allowed_shared_tcb[]` の拡張は**追加側に挙証責任**があり、freeze bundle の変更として receipt を要する(H-5)。 |
| **C-6** | A と B は `build_root_id` / `toolchain_id` / `implementation_provenance` を提出する。**path 改名を独立二実装と数える事故を防ぐため。** |
| **C-7** | **A と B は互いの中間結果を読まない。** 入力は certificate と両 native のみ。相手の `result_digest` を自分の再計算の前に参照することを禁止する。 |

---

## 7. 適合宣言 {#conformance}

実装が本契約に適合すると称するには、次を receipt に添える。

```text
conformance_record = {
  contract_id, contract_digest,
  verifier_id, code_digest, build_root_id, toolchain_id,
  implementation_provenance,
  dependency_closure[]            # mb/dependency-manifest/v1 の様式
  covered_clauses = [V-0..V-3, P-0.*, P-1.*, W-1..W-6, P-3.*, C-1..C-7]
  uncovered_clauses = []          # 空でなければ適合しない
}
```
**`uncovered_clauses` が非空の実装を「契約適合」と呼ばない。** 部分適合は `partial verifier / UNKNOWN` として扱う。
