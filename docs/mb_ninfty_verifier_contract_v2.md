# `mb/ninfty-verifier-contract/v2` — divisor equality certificate の検査契約

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 77)。v1 を supersede。**
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
contract_id     = "mb/ninfty-verifier-contract/v2"
contract_digest = <64 hex: 本稿 exact blob の sha256 — 発行時に司令塔が記入>
encoding        = UTF-8, LF, no BOM, no normalization
governing_spec  = "mb/ninfty-stage2-predicate/v7"
governing_spec_digest = <64 hex: v7 の digest — 発行時に司令塔が記入>
# 注: v7 §6 が本稿の digest を実値で pin するため、本欄は receipt 側で埋める(相互 pin による循環を断つ)
supersedes      = "mb/ninfty-verifier-contract/v1"
supersedes_digest = ae7950f3dec9081029dbda8c60e7fb8bc8e23030d8fa555915ea1eea012d136d   # 監査 FAIL の candidate
```
**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。

### 0.1 優先関係【便 65 F4 → **裁定 78 で解消**】{#precedence}

**原則**: 本稿と governing spec が矛盾した場合、**governing spec が優先**する。本稿は spec §4.1–§4.4 の**手続き的具体化**であって、新しい数学的前件を導入しない。

> **✅ 例外は解消済み(裁定 78)**: v2 起草時、spec v6 §4.2 の未型付け witness 記述が数学的に誤っていたため「この一点に限り本稿 §3.1 が優先する」という例外を置いていた。**`mb/ninfty-stage2-predicate/v7`(erratum E1)が §4.2 を本稿 §3.1・§3.1.2 と同じ 2 kind 型分けへ差し替えたので、例外は不要になった。** **現在 governing spec と本稿は同じ型分けを述べており、原則(governing spec 優先)がそのまま成り立つ。** §8 の erratum 案は **v7 で発行済み**。

---

## 0.2 v1 → v2 差分

| ID | v1 | v2 | 出所 |
|---|---|---|---|
| **B65-1** | W-2 の witness メニューに **Bézout $1=\sum u_ig_i$** を「点同一性の証明」として置いた。**これは非交差(supports が交わらない)の certificate であって同一性ではない** — 反例 $R=\mathbb Q[x]$, $I_0=(x)$, $I_1=(x-1)$ で $1=x-(x-1)$ ゆえ**異なる二点が W-2 を PASS する**(W-1〜W-6 全体の false positive)。**自認** | **W-2 を相互 ideal inclusion に限定**(`kind = ideal-equality`)。**Bézout は `kind = disjointness` の別 witness 型 W-2′ へ再配置**し、**使い所を W-1 の単射性・W-5 の余剰排除に限定**。**`reduction certificate` も tag で二分**(`reduction-to-zero` = membership 用 / `reduction-to-one` = 非交差用) | 便 65 F4 |
| **B65-2** | 「A/B verdict 不一致 → [25] / **native 不一致 → [26] に予約**」は排他でない — **native divisor が違えば equality witness も必ず不成立**なので同一原因が [25] と [26] を同時発生させ、partition まで違えば [24] も重なる | **Sol F5 の最小排他案を採用**: **[25] = A/B がともに witness の欠落・不成立を確認**(**native 一致確認後に限る**)/ **[26] = 同じ certificate・同じ native inputs に対する A/B verifier result の不一致**。**native の実体差は §5.1 の評価順序で先に specific check([13]–[24])へ送り、その段で停止**するので witness 段に到達しない。**「native 不一致を [26] に予約」は撤回。自認** | 便 65 F5 |
| **B65-3** | A/B が**同じ** certificate・両 native を読むことを要求する一方、manifest R-1 が「load する全 artifact」を closure に入れるため、**正しく独立な二 verifier でも必ず $[11]$ で停止**する | **`declared_untrusted_inputs[]` を新設**し、**implementation closure の universe から分離**(§6)。**TCB として差し引くのではない。** 型分離の判定基準は manifest v2 §5.3 | 便 65 F6 |

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

入力は spec v6 §4.1 の `divisor_equality_certificate` 全体と、それが参照する両 native artifact。**これらはすべて `declared_untrusted_inputs[]`(§6)に属する** — **共有されるが信用されない**。

検査対象の witness 群:

```text
W-1   component_bijection
W-2   exact_point_equality_witnesses            # kind = ideal-equality のみ(§3.1)
W-2'  distinctness_witnesses                    # kind = disjointness(§3.1.2)【v2 新設】
W-3   multiplicity_equalities
W-4   chart_overlap_witnesses
W-5   total_coverage_and_no_extra_component_witness
W-6   pushforward_compatibility_witness
```
両 native は各々 **2 対象**(`ramification_divisor_on_C_ref`・`branch_divisor_on_P1_ref`)を持つ。**W-1〜W-6 は 2 対象それぞれについて検査する**(片方だけの PASS を全体の PASS としない)。

---

## 3. 検査手続き {#procedure}

### 3.0 前段: ambient の固定を再検査

```text
P-0.1  ambient_coordinate_ring_schema_id + digest が存在し、digest が実体と一致
P-0.2  ambient_quotient_relations が明示されている
P-0.3  coefficient_field_presentation_id + digest が存在し一致
P-0.4  monomial_order_id + digest が存在し一致
P-0.5  groebner_reduction_contract_id + digest が存在し一致
P-0.6  異 presentation を跨ぐ witness には field_embedding_witness が添付されている
```
**いずれか不成立なら即 `FAIL`(§5 の routing に従う)。**
**理由**: reduced Gröbner basis は ring と term order を固定して初めて一意になる。固定が再検査できない状態で W-2 を「再計算した」と称してはならない。

### 3.1 W-2 の再検査 — **`kind = ideal-equality` に限定**【B65-1】

> **⚠ v1 の数学的誤り(自認)**: v1 §3.1 は $1=\sum u_ig_i$ の展開で W-2 を PASS にしていた。**$1\in I_0+I_1$ は $V(I_0)\cap V(I_1)=\varnothing$、すなわち二つの点が「交わらない」ことの certificate であって、「等しい」ことの certificate ではない。**
> **最小反例(独立に検算した)**: $R=\mathbb Q[x]$, $I_0=(x)$, $I_1=(x-1)$。$1=1\cdot x+(-1)\cdot(x-1)$ ゆえ v1 の Bézout 分岐は PASS を出す。一方 ideal membership の正しい判定は $x \bmod (x-1)=1\ne0$、$(x-1)\bmod (x)=-1\ne0$ で**両方向とも不成立** — 二点は等しくない。**v1 は「異なる点」を「同じ点」として component bijection へ流し、W-1〜W-6 全体の false positive を許していた。**

**W-2 の唯一の許容形式**:

```text
kind = ideal-equality
  I_0 ⊆ I_1  かつ  I_1 ⊆ I_0  を、各生成元の membership certificate で示す
```

| 形式 | 再計算内容 | PASS 条件 |
|---|---|---|
| **membership by representation** | 各生成元 $g\in G_0$ について、certificate が与える**表現係数** $\{u_i\}$ から $\sum u_i h_i$($h_i\in G_1$)を `groebner_reduction_contract_id` の規約で計算し、$g$ と**係数まで**一致するかを見る。$G_1\subseteq I_0$ も同様。 | **両方向の全生成元**について一致 |
| **membership by `reduction-to-zero`** | 各生成元 $g\in G_0$ を、固定 monomial order における $I_1$ の reduced Gröbner basis で**正規形へ簡約**する(reduction 列を一段ずつ再実行)。$G_1$ 側も同様。 | **両方向の全生成元**について**正規形が $0$** |

```text
P-1.1  表現係数 / reduction 列がすべての生成元について存在する(欠落があれば FAIL)
P-1.2  再計算が固定 monomial order・固定 reduction 規約の下で行われた
P-1.3  再計算結果が certificate の主張と一致する
P-1.4  異体 presentation を跨ぐ場合、field_embedding_witness の像が一致する
P-1.5  witness の kind tag が明示されている。tag 無しの reduction certificate は FAIL
       (「各生成元が相手 ideal で 0 に reduce する」のか「1 を得る」のかを
        区別しない certificate は、どちらの主張の証明にもならない)
```

> **⛔ W-2 の PASS 根拠にならないもの**:
> - **Bézout $1=\sum u_ig_i$**(= 非交差の証明。§3.1.2 の W-2′ 用)
> - tag の無い `reduction certificate`(P-1.5)
> - 単なる digest 一致 / 最終 partition の一致 / degree の一致
> - generator の内部 canonicalizer が「等しい」と述べたこと

### 3.1.2 W-2′ `distinctness_witnesses` — `kind = disjointness`【v2 新設】{#distinctness}

```text
kind = disjointness
  1 ∈ I_P + I_Q  の Bézout certificate(表現係数 {u_i} を明示)
  再計算: Σ u_i (I_P ∪ I_Q の生成元) を展開評価し、結果が 1 に一致するか
```

**使い所(この 2 つに限る)**:

| 用途 | 内容 |
|---|---|
| **W-1 の単射性** | component bijection が**相異なる component を相異なる component へ送る**ことの証明。$P\ne Q$ と主張する各対に W-2′ を要求する。 |
| **W-5 の余剰排除** | 「対応外の余剰 component が無い」を示す際、**ある component が既にマッチした全 component と別物である**ことの証明。 |

> **数学的注記(型の限定)**: 一般には **disjointness $\Rightarrow$ distinctness** であって逆は成り立たない(相異なる二つの部分スキームが交わることはある)。**本設定では両 native の component は $C$ 上および $\mathbb P^1$ 上の閉点であり、support は 0 次元 reduced** なので、**相異なる閉点は交わらず、この設定に限り両者は同値**である。**多重度は W-2′ ではなく W-3 が扱う** — W-2′ に用いる ideal は**点の ideal(radical)** であり、multiplicity を含む非被約構造を持ち込まない。
> **⛔ W-2′ を W-2 の代用にしてはならない。** W-2′ が全対で PASS しても、それは「対応が単射である」ことしか言わない。

### 3.2 W-1・W-3〜W-6

| # | 再計算内容 | PASS 条件 |
|---|---|---|
| **W-1** | 両 native の component 集合の間の全単射を、**W-2 の点同一性から独立に構成し直す**。単射性は **W-2′** で裏づける | 構成した対応が certificate の `component_bijection` と一致し、両側とも全域・単射 |
| **W-3** | 対応する component 対の multiplicity を両 native から読み、**整数として比較** | 全対で一致 |
| **W-4** | chart 重なり上で、両 chart の記述が同じ component を与えるかを再計算 | 全重なりで一致 |
| **W-5** | 両 native の component 総数と、W-1 の像の大きさを比較。余剰候補には **W-2′** を要求 | **被覆に漏れがなく、対応外の余剰 component が両側に存在しない** |
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
         native_cross_check_results[],            # §5.1 step 2
         per_witness_results[W-1, W-2, W-2', W-3..W-6], verdict }
       の canonical serialization
```
**P-3.3 の不一致は「検査対象が入れ替わっている」ことを意味するので、witness の成否に関わらず即停止。**

---

## 4. 合否規準 {#verdict}

```text
verifier_verdict = PASS   iff   P-0.* ∧ P-1.* ∧ (W-1, W-2, W-2', W-3..W-6 すべて PASS) ∧ P-3.*
                 = FAIL(reason)   otherwise
```
- **PASS は「certificate が両 native の同一性を実際に証明している」ことのみを主張する。** candidate の数学的判定(ACCEPT/REJECT)は述べない。
- **A と B の verdict が食い違った場合、両者を FAIL として扱う**(§5.1 step 4 の [26])。**多数決・片側採用を禁止。**

---

## 5. `INTEGRITY_STOP` 条件と routing {#integrity}

### 5.1 評価順序(**排他性はここで担保する**)【B65-2】{#evaluation-order}

> **v1 の欠陥(自認)**: 「native 不一致 → [26] に予約」は排他でなかった。**native divisor が違えば、それを同一視する W-1〜W-6 も必ず不成立**になり、partition まで違えば [24] も重なる。**同一 event に二 code を割り当てないという §5 冒頭の原則を、v1 自身が破っていた。**

```text
step 1  envelope-level: leak / digest / dependency checks
        → 該当あれば [9]..[12] を発して停止(witness 段へ進まない)

step 2  native cross-check: 両 native に対する specific な数学的検査
        (divisor identity, pell-derivative, chart/locus, RH, branch count,
         harmonicity, finite partition の突合)
        → 該当あれば [13]..[24] のうち該当する specific code を発して停止
        ※ この段で停止した場合、witness 検証は実行するが reason code を出さない
          (結果は native_cross_check_results[] / per_witness_results[] に記録のみ)

step 3  witness 検証(**native の一致が step 2 で確認された下でのみ reason 源となる**)
        A と B が独立に W-1, W-2, W-2', W-3..W-6 を再計算
        → A と B が**ともに**欠落・不成立を確認 → [25] divisor-equality-failure

step 4  A/B result 突合
        → 同じ certificate・同じ native inputs に対する
          A/B verifier result の不一致 → [26]
```

| # | 条項 |
|---|---|
| **X-1** | **step は上から順に評価し、reason を発した段で停止する。** ゆえに [9]–[12] / [13]–[24] / [25] / [26] は**相互排他**。 |
| **X-2** | **[25] は「native 一致が確認された下での witness 検証失敗」に限定される。** step 2 を通過していない witness 失敗は [25] を発しない。 |
| **X-3** | **[26] は「同一入力に対する A/B result の不一致」に限定される。** searcher/checker の native の実体差は step 2 の specific code へ送る。**「native 不一致を [26] に予約」する v1 の案は不採用**(便 65 F5)。 |
| **X-4** | step 2 で停止した場合も **witness 検証は実行し結果を記録する**(原因分析の材料)。**ただし reason code は発しない** — これが二重割当の回避点。 |

### 5.2 routing 表

| 事象 | reason code(spec §5.3.2 の段) |
|---|---|
| 入力 / native / certificate の **digest 不一致**(P-0.1・P-0.3〜P-0.5 の digest 欄、P-3.1〜P-3.3) | **`digest-mismatch` [12]** |
| implementation closure の禁止交差が非空(§6) | **`shared-helper-detected` [11]** |
| verifier が sealed 値を public 面に露出させた | **`sealed-field-leak` [9]** |
| **native cross-check の specific な失敗**(step 2) | **[13]–[24] の該当 code** |
| **witness の欠落・不成立**(P-0.2・P-0.6・P-1.*・W-1〜W-6 のいずれか)を A/B がともに確認 | **`divisor-equality-failure` [25]** |
| **同一入力に対する A/B verifier result の不一致** | **`verifier-result-mismatch` [26]**(v7 §5.3.3 と同期) |

**上記はすべて `INTEGRITY_STOP` であり、REJECT ではない。** verdict の決定と primary の選択は spec v6 §5.3 の state machine が行う — **本稿は reason code を供給するだけで、自ら verdict を宣言しない。**

---

## 6. 入力の型分離【B65-3】{#input-separation}

> **v1 の欠陥(自認)**: v1 §2 は A/B が**同じ** certificate・両 native を読むことを要求する一方、manifest R-1 は「load する全 artifact」を closure に入れた。**文字どおりなら三入力の digest は $D_A\cap D_B$ に必ず現れ、正しく独立な二 verifier でも必ず [11] で停止する。** 「contract と manifest を同時に満たす実装が存在しない」状態だった。

```text
declared_untrusted_inputs[] = {
  divisor_equality_certificate,
  searcher_native_artifact,
  checker_native_artifact,
  governing_spec_blob,
  contract_blob
}
```

| # | 条項 |
|---|---|
| **Y-1** | **`declared_untrusted_inputs[]` は implementation closure の universe から分離される**(manifest v2 §5.3)。**TCB として差し引くのではなく、そもそも交差検査 I 系の対象外。** |
| **Y-2** | **入力の共有は独立性を毀損しない。毀損するのは実装の共有である。** untrusted input は**両 verifier が独立に内容を再検査する**対象であり、共有されることが前提。 |
| **Y-3** | untrusted input については **A と B で digest 一致を要求する**(P-3.1〜P-3.3)。**一致しなければ検査対象が別物**であり [12]。 |
| **Y-4** | **入力クラスへの math-helper 混入を禁止**。判定基準は manifest v2 §5.3 に置き、本稿はそれを参照する。**要旨**: 入力とは「**内容が再検査されるデータ**」であり、実装とは「**データに作用するコード**」である。`monomial_order_id` のような**規約を選ぶパラメータ値の共有は許される**(A と B は同じ規約を**各々の実装で**実現する)。**禁止されるのは、その規約を実現するコードの共有。** |

---

## 7. 二 verifier の独立要件 {#independence}

**`mb/dependency-manifest/v2` の H 系・I 系を参照する。** 本稿はそれを verifier 側の義務として再掲する。

| # | 義務 |
|---|---|
| **C-1** | A と B は **別実装**であり、`implementation_dependency_closure_A[]` / `_B[]` を **推移的閉包**として提出する(H-1)。**closure は各 node の outgoing dependency 証明と受領側の fixpoint 再計算で検収される**(depth の見た目では判定しない)。 |
| **C-2** | 同一性は **content digest** で判定される。別名・別 path・薄い wrapper では独立性を主張できない(H-2)。 |
| **C-3** | 共有してよいのは `allowed_shared_tcb[]` に列挙された frozen content digest のみ。**`role = math-helper` を TCB に入れてはならない**(H-3)。**§3 の再計算は A・B が各々の実装で行う。** |
| **C-4** | 禁止交差の値は **receipt 受領側が canonical content digest 集合から再導出**する(H-4)。 |
| **C-5** | `allowed_shared_tcb[]` の拡張は**追加側に挙証責任**があり、receipt を要する(H-5)。 |
| **C-6** | A と B は `build_root_id` / `toolchain_id` / `implementation_lineage_digest` を提出する(H-2b′)。 |
| **C-7** | **A と B は互いの中間結果を読まない。** 入力は `declared_untrusted_inputs[]` のみ。相手の `result_digest` を自分の再計算の前に参照することを禁止する。 |
| **C-8** | **初期 TCB は `allowed_shared_tcb = []`(空)**。ゆえに **A と B は異なる runtime で実装する**(manifest v2 §5.4)。同一 runtime を用いるなら、その runtime の exact digest・role・justification を **receipt で TCB に追加**しなければならない。 |

---

## 8. governing spec への erratum 要請【便 65 F4】— **v7 で発行済み**{#erratum}

> **【状態】裁定 78 により `mb/ninfty-stage2-predicate/v7` として発行済み。** 以下は要請時の原文(記録)であり、**v7 §4.2 が逐語適用済み**である。

**spec v6 §4.2 の witness メニューは本稿と同じ数学的誤りを含む。** governing spec 優先の原則により、**spec 側を直さなければ誤りが正本に残る。** 次の差し替えを要請する。

> **spec v6 §4.2 の該当 2 行(現行)**
> - 相互 ideal inclusion certificate: $I_1\subseteq I_2$ と $I_2\subseteq I_1$ を、固定 monomial order の reduced Gröbner basis に対する明示の表現係数で。
> - **Bézout / reduction certificate**: $1=\sum u_ig_i$ の明示係数、または reduction 列。
>
> **erratum 案(差し替え後)**
> - **`kind = ideal-equality`(W-2 の唯一の形式)**: $I_1\subseteq I_2$ と $I_2\subseteq I_1$ を、固定 monomial order の reduced Gröbner basis に対する**明示の表現係数**、または**各生成元の `reduction-to-zero` 列**で。
> - **`kind = disjointness`(W-2′ — 別 witness 型)**: $1\in I_1+I_2$ の Bézout certificate。**component bijection の単射性と余剰排除にのみ使い、W-2 の equality PASS には使わない。**
> - **すべての reduction certificate は `reduction-to-zero` / `reduction-to-one` の tag を持たねばならない。** tag 無しは FAIL。

**併せて要請**: spec v6 §5.3.2 の **[26] の名称 `checker-mismatch` は、本稿 §5.1 step 4 の意味(同一入力に対する A/B verifier result の不一致)と齟齬**する。**`verifier-result-mismatch` への改名**、または spec 側で [26] の述語を明記することを求める。

> **【状態】v7 で実施済み** — `[26] verifier-result-mismatch` へ改名され、**v7 §5.3.3 に [24]/[25]/[26] の相互排他な述語と評価順序**(本稿 §5.1 X-1〜X-4 と同期)が明記された。**本稿 §5.2 の routing 表の「§8 で改名を要請」注記は解消。**

---

## 9. 適合宣言 {#conformance}

```text
conformance_record = {
  contract_id, contract_digest,
  verifier_id, code_digest, build_root_id, toolchain_id,
  implementation_lineage_digest,
  implementation_dependency_closure[]     # mb/dependency-manifest/v2 の様式
  declared_untrusted_inputs[]             # §6
  covered_clauses = [V-0..V-3, P-0.*, P-1.*, W-1, W-2, W-2', W-3..W-6, P-3.*,
                     X-1..X-4, Y-1..Y-4, C-1..C-8]
  uncovered_clauses = []                  # 空でなければ適合しない
}
```
**`uncovered_clauses` が非空の実装を「契約適合」と呼ばない。** 部分適合は `partial verifier / UNKNOWN` として扱う。
