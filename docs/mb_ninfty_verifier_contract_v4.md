# `mb/ninfty-verifier-contract/v4` — divisor equality certificate の検査契約

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 81)。v3 を supersede。**
**この文書は `mb/ninfty-stage2-predicate/v9` §4.4 の `verifier_contract_id` が指す実体である。**

> **【版履歴】v4 = v3 の同期版。** 変更は **3 点** — **(S1) manifest pin を v4 へ**(hash 順序 manifest → contract → spec により、manifest が変われば contract も新版が要る)・**(S2) governing spec を v9 へ**(ID 束縛・digest は receipt)・**(S3) §5.3 の cross-reference 誤り(案 A → 案 B)の修正**。**数学的内容・検査手続き・二軸 routing は v3 と逐語同一。**

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
contract_id     = "mb/ninfty-verifier-contract/v4"
contract_digest = <64 hex: 本稿 exact blob の sha256 — receipt が記入>
encoding        = UTF-8, LF, no BOM, no normalization
governing_spec  = "mb/ninfty-stage2-predicate/v9"
governing_spec_digest = <64 hex: v9 の digest — receipt が記入>
dependency_manifest_schema_id     = "mb/dependency-manifest/v4"
dependency_manifest_schema_digest = 378f30c84f79bf5d18055ccb824f21e65b3efd11a1d947178e94233f74412d11
supersedes        = "mb/ninfty-verifier-contract/v3"
supersedes_digest = bd4d5064e04ef292d7f21fa3cf5b8089c20ef34c322461920dc95c9775e4d484   # 監査 FAIL の candidate
supersedes_v2     = 1fd36b3eda0da33b2aba5d3d371a24749850b9b05a3f4c4f17ef1725ffe555bd
```

> **【hash 順序・便 66 F11】** 非循環な順序は **manifest → contract → spec → receipt**。**本稿は manifest v4 の exact digest を pin し、spec の digest は pin しない**(governing spec は **ID で束縛し digest は receipt 側**)。**spec v9 が本稿の exact digest を pin する。**
> **【fail-closed】`mb/ninfty-stage2-predicate/v9` は本稿起草時点で未発行の後継である。receipt が v9 の実在と digest を束縛するまで、本稿を operative として扱ってはならない。**

**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。

### 0.1 優先関係 {#precedence}

**本稿と governing spec が矛盾した場合、governing spec が優先する。** 本稿は spec §4.1–§4.4 の**手続き的具体化**であって、新しい数学的前件を導入しない。
**v2 が置いていた「1 点優先の例外」(§4.2 の型誤り)は spec v7 erratum E1 で解消済み。** §8 は **v8 への erratum 案**を持つが、これは**要請であって本稿の優先を主張するものではない** — **v8 発行前に本稿を operative にしない**(上の fail-closed 条項)。

---

## 0.2 v3 → v4 差分【裁定 81】

| ID | v3 | v4 | 出所 |
|---|---|---|---|
| **S1** | `dependency_manifest_schema_id/digest` が **v3**(`1a8d1f21…`)を pin | **manifest v4**(`378f30c8…`)へ。**hash 順序 manifest → contract → spec により、manifest が新版になれば contract も新版が必要**(v3 のまま spec v9 が manifest v4 を pin すると、contract と spec が別の manifest を指す — 便 66 F7 と同型の型不一致) | 便 67 F11-2 |
| **S2** | governing spec = v8 | **v9 へ**(ID 束縛・digest は receipt) | 裁定 81 |
| **S3** | §5.3 の表が public secondary の spec 側条文を **「§8 の erratum 案 A」** と参照していた。**正しくは案 B**(案 A は二軸 routing、案 B が public secondary)。**自認** | **案 B へ修正** | 便 67 F11-2 |

> **v4 でも不変**: **§1 役割・§2 検査対象・§3 検査手続き(W-2 / W-2′ の型分け・§3.4 result vector)・§4 合否・§5.1 二軸 routing(X-1〜X-6)・§5.4 secondary(P-S1〜P-S6)・§6 入力型分離・§7 独立要件。**

---

## 0.2.1 v2 → v3 差分(v3 から継承・変更なし)

| ID | v2 | v3 | 出所 |
|---|---|---|---|
| **B66-1(F4)** | §5.1 の評価順序が「前段が reason を発したら停止」で**後段を抑圧**した。**同じ原因の二重分類を防ぐ意図が、別原因として同時に起きた verifier disagreement まで消していた。** ① native partition mismatch [24] と **A/B の witness vector 不一致**が同時でも step 2 停止で [26] が public から落ちる(**二実装監査が検出すべき common/individual bug の証跡**が消える) ② A: W-2 FAIL/W-3 PASS・B: W-2 PASS/W-3 FAIL は**両者 overall FAIL だが result vector は不一致**なのに、現 step 3 が [25] を発して step 4 へ行かない(**enum 名 `verifier-result-mismatch` と一致しない**)。**自認** | **§5.1 を二軸へ**(便 66 F13 の発案を採用): **semantic axis**(envelope / native mathematics / witness validity — **軸内は排他**)と **concordance axis**($R_A$ vs $R_B$ — **入力 digest が一致する限り常に評価**)。**[26] は semantic reason と共存する。** 判定は **`if R_A ≠ R_B: add [26] / elif native reasons 空 かつ $R_A=R_B$ が failure を含む: add [25]`**。**primary の単数性は維持**し、**public に `secondary_reason_codes[]` を新設**(§5.4) | 便 66 F4・F13 |
| **B66-2(F7)** | machine field は v7 へ直ったが、**live 文が v6 のまま**: 冒頭「v6 §4.4 の実体」・§2「spec v6 §4.1 の certificate」・§5.2「spec v6 §5.3 が決める」。**P-3.1 の governing-spec equality と衝突する exact bundle の型不一致。**(§8 の v6 記述は historical quotation なので可) | **live 三箇所を後継 spec(v8)へ同期。** §8 の歴史記述は `[historical quotation]` として保持。**自認** | 便 66 F7 |

---

## 1. 役割と非役割 {#role}

| # | 条項 |
|---|---|
| **V-0** | verifier は **`divisor_equality_certificate` を検査する装置**であり、**判定 lane ではない**。candidate に対する `ACCEPT` を**単独で出せない**。出力は §3.4 の **canonical per-witness result vector** と overall `PASS`/`FAIL`、およびその digest。 |
| **V-1** | verifier は **searcher / checker の native 出力を再生産しない**。両 native は入力として受け取り、**certificate の witness が両者を実際に同一視しているか**だけを検査する。 |
| **V-2** | **generator は verifier ではない**(spec §4.3 G-1)。generator が作った witness を、**A と B が独立に再検査**する(G-3)。 |
| **V-3** | verifier は **`SEALED_INTERNAL` の値を public envelope へ写さない**。検査に用いた量は digest でのみ参照する。 |

---

## 2. 検査対象 {#scope}

入力は **governing spec(v8)§4.1** の `divisor_equality_certificate` 全体と、それが参照する両 native artifact。**これらはすべて `declared_untrusted_inputs[]`(§6)に属する** — **共有されるが信用されない**。

```text
W-1   component_bijection
W-2   exact_point_equality_witnesses            # kind = ideal-equality のみ(§3.1)
W-2'  distinctness_witnesses                    # kind = disjointness(§3.1.2)
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
**理由**: reduced Gröbner basis は ring と term order を固定して初めて一意になる。固定が再検査できない状態で W-2 を「再計算した」と称してはならない。

### 3.1 W-2 の再検査 — **`kind = ideal-equality` に限定**

> **⚠ v1 の数学的誤り(自認・記録)**: v1 は $1=\sum u_ig_i$ の展開で W-2 を PASS にしていた。**$1\in I_0+I_1$ は $V(I_0)\cap V(I_1)=\varnothing$ の certificate であって「等しい」ことの certificate ではない。**
> **最小反例(独立に検算)**: $R=\mathbb Q[x]$, $I_0=(x)$, $I_1=(x-1)$。$1=1\cdot x+(-1)\cdot(x-1)$ ゆえ v1 の Bézout 分岐は PASS を出す。正しい membership 判定は $x \bmod (x-1)=1\ne0$、$(x-1)\bmod (x)=-1\ne0$ で**両方向とも不成立**。

```text
kind = ideal-equality
  I_0 ⊆ I_1  かつ  I_1 ⊆ I_0  を、各生成元の membership certificate で示す
```

| 形式 | 再計算内容 | PASS 条件 |
|---|---|---|
| **membership by representation** | 各生成元 $g\in G_0$ について表現係数 $\{u_i\}$ から $\sum u_i h_i$($h_i\in G_1$)を `groebner_reduction_contract_id` の規約で計算し、$g$ と**係数まで**一致するかを見る。逆向きも同様。 | **両方向の全生成元**について一致 |
| **membership by `reduction-to-zero`** | 各生成元を、固定 monomial order における相手 ideal の reduced Gröbner basis で**正規形へ簡約**する(reduction 列を一段ずつ再実行)。 | **両方向の全生成元**について**正規形が $0$** |

```text
P-1.1  表現係数 / reduction 列がすべての生成元について存在する
P-1.2  再計算が固定 monomial order・固定 reduction 規約の下で行われた
P-1.3  再計算結果が certificate の主張と一致する
P-1.4  異体 presentation を跨ぐ場合、field_embedding_witness の像が一致する
P-1.5  witness の kind tag が明示されている。tag 無しの reduction certificate は FAIL
```

> **⛔ W-2 の PASS 根拠にならないもの**: **Bézout $1=\sum u_ig_i$**・tag の無い `reduction certificate`・単なる digest 一致・最終 partition の一致・degree の一致・generator の内部 canonicalizer の宣言。

### 3.1.2 W-2′ `distinctness_witnesses` — `kind = disjointness` {#distinctness}

```text
kind = disjointness
  1 ∈ I_P + I_Q  の Bézout certificate(表現係数 {u_i} を明示)
```

| 用途(この 2 つに限る) | 内容 |
|---|---|
| **W-1 の単射性** | component bijection が**相異なる component を相異なる component へ送る**ことの証明。 |
| **W-5 の余剰排除** | ある component が既にマッチした全 component と別物であることの証明。 |

> **数学的注記(型の限定)**: 一般には **disjointness $\Rightarrow$ distinctness** で逆は偽。**本設定では component は $C_{\rm crv}$ 上・$\mathbb P^1$ 上の閉点で support は 0 次元 reduced** なので、**相異なる閉点は交わらず、この設定に限り同値**。**多重度は W-3 が扱う** — W-2′ の ideal は**点の radical**であり非被約構造を持ち込まない。
> **⛔ W-2′ を W-2 の代用にしてはならない。**

### 3.2 W-1・W-3〜W-6

| # | 再計算内容 | PASS 条件 |
|---|---|---|
| **W-1** | 全単射を **W-2 の点同一性から独立に構成し直す**。単射性は **W-2′** で裏づける | certificate の `component_bijection` と一致し、両側とも全域・単射 |
| **W-3** | 対応する component 対の multiplicity を**整数として比較** | 全対で一致 |
| **W-4** | chart 重なり上で両 chart が同じ component を与えるか再計算 | 全重なりで一致 |
| **W-5** | component 総数と W-1 の像の大きさを比較。余剰候補には **W-2′** を要求 | 被覆に漏れがなく、**両側**に余剰 component が無い |
| **W-6** | `ramification_divisor_on_C` の pushforward と `branch_divisor_on_P1` の整合を multiplicity の和として再計算 | 全 branch point で一致 |

### 3.3 入出力の束縛

```text
P-3.1  certificate の predicate_spec_id / predicate_spec_digest が governing spec と一致
P-3.2  certificate の schema_id / schema_digest が governing spec §4.1 の anchor と一致
P-3.3  両 native の native_artifact_digest が、verifier が実際に読んだ blob の digest と一致
```
**P-3.3 の不一致は「検査対象が入れ替わっている」ことを意味するので即停止。**

### 3.4 canonical per-witness result vector【B66-1】{#result-vector}

```text
R_X = canonical_serialize( [
        ("W-1",  result), ("W-2",  result), ("W-2'", result),
        ("W-3",  result), ("W-4",  result), ("W-5",  result), ("W-6", result)
      ] )                       # X ∈ {A, B}・各 result ∈ {PASS, FAIL, ABSENT}
      × 2 対象(ramification_divisor_on_C / branch_divisor_on_P1)

result_digest_X = sha256( canonical_serialize( {
        contract_id, contract_digest, certificate_digest,
        searcher_native_artifact_digest, checker_native_artifact_digest,
        native_cross_check_results[],        # §5.1 semantic step 2
        R_X, overall_verdict_X
      } ) )
```

| # | 条項 |
|---|---|
| **R-1** | **$R_A$ と $R_B$ は同一の canonical 形式で作られ、要素ごとに比較可能でなければならない。** overall verdict だけの比較を「result 比較」と称してはならない(**両者 FAIL でも vector は違い得る** — 便 66 F4.2)。 |
| **R-2** | **$R_X$ は `ABSENT`(witness が存在しない)と `FAIL`(存在するが不成立)を区別する。** |
| **R-3** | **$R_A\ne R_B$ の比較は、入力 digest(certificate・両 native)が A/B で一致する場合にのみ意味を持つ。** 不一致なら先に [12]。 |

---

## 4. 合否規準 {#verdict}

```text
verifier_verdict_X = PASS  iff  P-0.* ∧ P-1.* ∧ (R_X の全成分が PASS) ∧ P-3.*
                   = FAIL  otherwise
```
- **PASS は「certificate が両 native の同一性を実際に証明している」ことのみを主張する。** candidate の数学的判定は述べない。
- **A と B の verdict または vector が食い違った場合、両者を FAIL として扱う**(§5.1 concordance axis の [26])。**多数決・片側採用を禁止。**

---

## 5. `INTEGRITY_STOP` 条件と routing {#integrity}

### 5.1 二軸 routing【B66-1・便 66 F13】{#two-axis}

> **v2 の欠陥(自認)**: 「前段が reason を発したら停止」は**同じ原因の二重分類**を防ぐには正しかったが、**別原因として同時に起きた verifier disagreement まで消していた**。**[24] は native data の不一致、[26] は verifier 実装の不一致であり、同じ event の別名ではない。**

```text
# --- semantic axis(軸内は排他・上から評価し reason を発した段で停止)---
S1  envelope-level: leak / digest / dependency checks      -> [9]..[12]
S2  native cross-check: 両 native への specific な数学的検査 -> [13]..[24]
S3  witness validity                                        -> [25]

# --- concordance axis(独立・入力 digest が一致する限り常に評価)---
C1  R_A vs R_B                                              -> [26]

# --- 合成 ---
if R_A != R_B:
    concordance_reasons = { [26] }
elif S2 の native reason が空 かつ (R_A = R_B) が failure を含む:
    semantic_reasons ∪= { [25] }

I       = semantic_reasons ∪ concordance_reasons
verdict = INTEGRITY_STOP (I ≠ ∅ のとき)
primary = minimum(I, integrity_priority)          # 単数性は維持
```

| # | 条項 |
|---|---|
| **X-1** | **semantic axis は軸内で排他。** [9]–[12] / [13]–[24] / [25] は同時に立たない。 |
| **X-2** | **[25] は「native の一致が S2 で確認された下で、$R_A=R_B$ が witness failure を含む」に限定される。** |
| **X-3** | **[26] は concordance axis に属し、semantic reason と共存する。** [13]–[24] と同時に検出してよい。**「native 不一致を [26] に予約する」案は不採用**(便 65 F5)。 |
| **X-4** | **[25] と [26] は相互排他**($R_A=R_B$ が [25] の前提、$R_A\ne R_B$ が [26] の前提)。 |
| **X-5** | **S2 で停止した場合も witness 検証と concordance 比較は実行する。** semantic の後段 reason は発しないが、**concordance の [26] は発する** — これが v2 との違い。 |
| **X-6** | **`[26]` の述語は「overall verdict の不一致」ではなく「canonical result vector $R_A\ne R_B$」である**(R-1)。もし overall verdict の不一致に限定するなら enum 名を `verifier-verdict-mismatch` とすべきだが、**本稿は vector 比較を採る**(便 66 F4.2)。 |

### 5.2 routing 表

| 事象 | reason code(**governing spec v8** §5.3.2 の段) | 軸 |
|---|---|---|
| 入力 / native / certificate の **digest 不一致** | **`digest-mismatch` [12]** | semantic S1 |
| implementation closure の三交差が非空(§7) | **`shared-helper-detected` [11]** | semantic S1 |
| verifier が sealed 値を public 面に露出 | **`sealed-field-leak` [9]** | semantic S1 |
| **native cross-check の specific な失敗** | **[13]–[24] の該当 code** | semantic S2 |
| **$R_A=R_B$ が witness の欠落・不成立を含む**(native 一致確認後) | **`divisor-equality-failure` [25]** | semantic S3 |
| **$R_A\ne R_B$**(同一入力に対する canonical result vector の不一致) | **`verifier-result-mismatch` [26]** | **concordance C1** |

**上記はすべて `INTEGRITY_STOP` であり、REJECT ではない。** verdict の決定と primary の選択は **governing spec v8 §5.3** の state machine が行う — **本稿は reason code を供給するだけで、自ら verdict を宣言しない。**

### 5.3 state machine との整合 {#state-machine-fit}

| 層 | 内容 | spec 側の根拠 |
|---|---|---|
| **primary** | `minimum(I, integrity_priority)` — **単数・全域**。v6 以来の不変条件をそのまま保つ | spec §5.3 invariant 2・4 |
| **sealed** | `all_reason_codes[]` = canonical 整列した $I\cup R$ — **全 code を保持** | spec §5.3 invariant 3 |
| **public secondary** | **§5.4 で新設** | **spec 側条文が要る → §8 の erratum 案 B**【v4 で修正・v3 は「案 A」と誤記(**自認**)】 |

**二軸化そのものは spec §5.3 の state machine を変えない** — `I` の作り方が「排他的な単一 code」から「semantic ∪ concordance」へ広がるだけで、`primary = minimum(I, ...)` と `accepted iff I=R=∅` はそのまま成立する。

### 5.4 `secondary_reason_codes[]`(public)【裁定 79】{#secondary}

```text
public envelope = {
  candidate_ref, predicate_spec_id, predicate_spec_digest,
  searcher_id+digest, checker_id+digest,
  verdict,
  primary_reason_code,              # 単数・従来どおり
  secondary_reason_codes[],         # canonical 整列【v3 新設】
  <数学的射影 5 欄>
}
```

| # | 条項 |
|---|---|
| **P-S1** | **`primary_reason_code` の単数性は維持する。** `secondary_reason_codes[]` は primary を**含まない**。 |
| **P-S2** | **`secondary_reason_codes[]` は canonical 昇順に整列**する(producer の順序に依存しない)。 |
| **P-S3** | **【漏洩最小化】public の secondary は concordance axis の code に限る**(現行 enum では **[26] のみ**)。**semantic axis の非 primary code は sealed の `all_reason_codes[]` にのみ置く。** |
| **P-S4** | **P-S3 の理由**: public envelope の情報量が増えるほど、**小さい探索宇宙では reason の組合せが指紋になり得る**(便 59 F11.3 の deterministic digest と同型のリスク)。**F4.1 が要求するのは「verifier disagreement が public から消えないこと」**であり、それは **1 ビット**([26] の有無)で満たせる。**semantic の全 code を public へ出す必要はない。** |
| **P-S5** | ゆえに **[24] と [26] の同時成立**では `primary = [24]`(priority 最小)・`secondary = [[26]]` となり、**両方が public に可視**である(F4.1 の要求を満たす)。 |
| **P-S6** | `secondary_reason_codes[]` が空のときは**空配列を明示**する(欄の欠落と区別する)。 |

---

## 6. 入力の型分離 {#input-separation}

```text
declared_untrusted_inputs[] = {
  divisor_equality_certificate, searcher_native_artifact, checker_native_artifact,
  governing_spec_blob, contract_blob
}
```

| # | 条項 |
|---|---|
| **Y-1** | **`declared_untrusted_inputs[]` は implementation closure の universe から分離される**(manifest v4 §5.3)。**TCB として差し引くのではなく交差検査の対象外。** |
| **Y-2** | **入力の共有は独立性を毀損しない。毀損するのは実装の共有である。** |
| **Y-3** | untrusted input については **A と B で digest 一致を要求する**(P-3.1〜P-3.3)。不一致は [12]。**これは R-3 の前提でもある。** |
| **Y-4** | **入力クラスへの math-helper 混入を禁止**。判定基準は manifest v4 §5.3.2(U-1〜U-4・**Y-4d: build-time artifact は入力クラスに置けない**)。**規約を選ぶパラメータ値の共有は許され、禁止されるのはその規約を実現するコードの共有。** |

---

## 7. 二 verifier の独立要件 {#independence}

**`mb/dependency-manifest/v4` を参照する。**

| # | 義務 |
|---|---|
| **C-1′** | A と B は **別実装**であり、`implementation_dependency_closure` を**推移的閉包**として提出する(H-1′)。検収は **attestation と受領側 fixpoint 再計算**による(depth の見た目で判定しない)。**R-6 の昇格対象が `content_digest` に解決されない場合も [12]**(H-1a″)。 |
| **C-2** | 同一性は **content digest** で判定される(H-2)。別名・別 path・薄い wrapper では独立性を主張できない。 |
| **C-3′** | 共有してよいのは四つの TCB 欄に列挙された値のみ。**`role = math-helper` を TCB に入れてはならない**(H-3)。 |
| **C-4′** | **禁止交差は receipt 受領側が四面から再計算する**(H-4・I-3a binary / I-3b source / **I-3d build**)。**family(I-3c′)は audit flag。** |
| **C-5′** | TCB の拡張は**追加側に挙証責任**があり receipt を要する(H-5)。**四欄は独立**(H-5d′)。 |
| **C-6″** | **【v4 で manifest v4 へ同期】** A と B は **lineage preimage と build_root preimage の 5 欄**(`source_artifact_digests[]`・`toolchain_digest`・`build_step_digests[]`・`build_definition_blob_digest`・`pinned_input_digests[]`)を提出する(manifest v4 §2.1 E-5・E-6・E-9)。**受領側は D-1・D-2・D-3 の三つすべてを再計算する**(D-R2′・I-0′・I-0c)。**output-affecting な toolchain / build step / code generator は closure entry へ必須昇格**(R-6)。**`implementation_family_id` は audit flag であって blocking 判定には使わない**(M-3′)。**producer 可変の識別子を独立性の根拠にしてはならない**(H-2d)。 |
| **C-7** | **A と B は互いの中間結果を読まない。** 相手の `result_digest` を自分の再計算の**前に**参照することを禁止する。**§5.1 C1 の比較は、両者が独立に確定した $R_A$・$R_B$ に対して受領側が行う。** |
| **C-8′** | **初期 TCB は四欄とも空**(manifest v4 §5.4)。ゆえに **A と B は異なる runtime で実装し、かつ異なる toolchain / build step で build する**(**共有 toolchain は build face で [11]**)。共有するなら receipt で該当欄に追加する。 |

---

## 8. governing spec への erratum 案【記録】{#erratum}

> **【状態・v4 更新】以下 A/B/C は `mb/ninfty-stage2-predicate/v8` として発行済み**(裁定 80)。**便 67 F3・F4・F5 で anchor / pin / topology / routing / P-S3 は PASS。**
> **v9 に残る 2 件**(便 67 F6・F8・裁定 81 で発行決定): **(D) §5.3 invariant 2 を P-S3 と同期**(v8 は public schema と §5.4.1 だけを足し、**既存 invariant 2「public は primary のみ」を直し忘れて同一 blob 内で直接矛盾**していた — **契約側の案 B 自身が「invariant に条文を足す」と要求していたのに漏れた。自認**)・**(E) §9 の live gate を「v6 の Sol 監査 PASS」から「本 exact bundle(spec+contract+manifest の三 digest)の freeze PASS receipt」へ**(v6 は erratum 前であり、その audit PASS は現 bundle の freeze PASS の代用にならない)。

> **以下は要請時の原文(記録)。**

### 案 A — §5.3.3 を二軸 routing へ(便 66 F4)

> **v7 §5.3.3 の step 1〜4「前段が reason を発したら停止」を、本稿 §5.1 の二軸へ差し替える。**
> - **semantic axis**(S1 envelope / S2 native mathematics / S3 witness validity)— **軸内は排他**。
> - **concordance axis**(C1: canonical result vector $R_A$ vs $R_B$)— **入力 digest が一致する限り常に評価**し、**semantic reason と共存**する。
> - 合成規則: `if R_A ≠ R_B: add [26] / elif S2 の native reason が空 かつ R_A=R_B が failure を含む: add [25]`。
> - **[24] と [25] は semantic 軸内で排他。[26] は別軸なので [13]–[24] と同時に立つ。**
> - **[26] の述語は「canonical per-witness result vector の不一致」**であり、overall verdict の不一致に限定しない(限定するなら `verifier-verdict-mismatch` へ改名すべき)。

### 案 B — public envelope に `secondary_reason_codes[]` を新設(裁定 79)

> **§5.1 public envelope に `secondary_reason_codes[]`(canonical 昇順・primary を含まない)を追加**し、**§5.3 の invariant に次を足す**。
> - `primary_reason_code` は従来どおり**単数・全域**。
> - **public の secondary は concordance axis の code に限る**(現行 enum では [26] のみ)。**semantic の非 primary code は sealed の `all_reason_codes[]` にのみ置く** — public の情報量増加を 1 ビットに抑えるため(本稿 P-S3・P-S4)。
> - 空のときは**空配列を明示**する。

### 案 C — external anchor の digest 型付け(便 66 F8)

> **v7 §6 は `schema_id(input-separation) = dependency_manifest_schema_id + "#input-separation"` としながら、`bound_blob_digest(all of the above) = predicate_spec_digest` で束ねている。** `input-separation` の実体は **manifest の §5.3** なので、**bound blob は manifest digest でなければならず、spec 自身の digest ではない。**
> ```text
> # spec 内部 anchors
> bound_blob_digest(cert .. witness-kinds) = predicate_spec_digest
> # external manifest anchor
> schema_id(input-separation)       = dependency_manifest_schema_id + "#input-separation"
> bound_blob_digest(input-separation) = dependency_manifest_schema_digest
> ```
> **併せて `dependency_manifest_schema_id/digest` の定義を先に置き forward reference を消す。**

### 併せて v8 §6 で pin すべき値

```text
verifier_contract_id     = "mb/ninfty-verifier-contract/v4"
verifier_contract_digest = <本稿の sha256>
dependency_manifest_schema_id     = "mb/dependency-manifest/v4"
dependency_manifest_schema_digest = 378f30c84f79bf5d18055ccb824f21e65b3efd11a1d947178e94233f74412d11
```
**hash 順序は manifest → contract → spec → receipt**(便 66 F11)。**spec 自己 digest と contract の governing-spec digest は receipt 側**に置く。

---

## 9. 適合宣言 {#conformance}

```text
conformance_record = {
  contract_id, contract_digest,
  verifier_id, code_digest, build_root_id,
  source_artifact_digests[], toolchain_digest, build_step_digests[],   # manifest v3 §2.1
  implementation_family_id,                                            # receipt authority mint
  implementation_dependency_closure[]
  declared_untrusted_inputs[]
  covered_clauses = [V-0..V-3, P-0.*, P-1.*, W-1, W-2, W-2', W-3..W-6, P-3.*,
                     R-1..R-3, X-1..X-6, P-S1..P-S6, Y-1..Y-4, C-1..C-5, C-6', C-7, C-8]
  uncovered_clauses = []
}
```
**`uncovered_clauses` が非空の実装を「契約適合」と呼ばない。** 部分適合は `partial verifier / UNKNOWN` として扱う。
