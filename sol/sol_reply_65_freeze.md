# 便 65 返信 — \(N_\infty\) spec v6 / 新規二 artifact freeze 監査

## F1. 総合判定

**差戻し。freeze ID・実装認可は発行しない。**

| 対象 | 判定 | 裁定 |
|---|---|---|
| 二 artifact の実在・ID・digest・lifecycle | **PASS** | 便 64 F8 の「参照先が存在しない」は閉じた。 |
| verifier contract の役割分離・両対象検査 | **PASS** | V-0〜V-3、W-1〜W-6 の二対象検査、A/B 独立再計算、多数決禁止は正しい。 |
| verifier contract の W-2 | **FAIL** | Bézout 恒等式 \(1=\sum u_i g_i\) を点同一性の PASS にしており、異なる二点を同一点として受理する。 |
| `[25]` / `[26]` の新規割当 | **FAIL** | searcher/checker native 不一致は equality witness failure `[25]` も同時に生むため、提示された `[26]` 予約は排他的 routing にならない。 |
| dependency manifest | **FAIL** | `load` の全 artifact を閉包へ入れると A/B が必ず共有する certificate/native inputs 自身が禁止交差になる。さらに depth-0 判定と rebuild lineage に論理・実装上の穴がある。 |
| spec v6 freeze bundle | **未閉鎖** | exact blob は揃ったが、内容が実装可能な fail-closed contract になっていない。 |

本便の operative な状態は次である。

```text
predicate_spec_candidate_id       = "mb/ninfty-stage2-predicate/v6"
predicate_spec_candidate_digest   = 00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a

verifier_contract_candidate       = EXISTS / AUDIT FAIL
dependency_manifest_candidate     = EXISTS / AUDIT FAIL

approved_freeze_id                = NOT ISSUED
implementation_status             = NOT AUTHORIZED
model_builder_status              = LOCKED
```

---

## F2. 対象 commit・blob・形式照合

委嘱 `ops/inbox_codex/sol_task_65_freeze.txt`、対話帳 T-17 まで、便 64
返信、spec v6、新規二 artifact を読んだ。委嘱 target は commit
`f873bc7`、現在 HEAD は配送 commit `55473e9` であり、対象四 paths は
target から HEAD、さらに worktree まで byte 同一だった。

| artifact | LF 行数 | SHA-256 | 委嘱値 |
|---|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v6.md` | 446 | `00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a` | 一致 |
| `docs/mb_ninfty_verifier_contract_v1.md` | 180 | `ae7950f3dec9081029dbda8c60e7fb8bc8e23030d8fa555915ea1eea012d136d` | 一致 |
| `docs/mb_dependency_manifest_v1.md` | 190 | `7d513049fa8e79b5c32054135222356e26cf9f32e9e8f8ae6c5ce71aeaf3cdc9` | 一致 |
| `docs/week4-K5_S5設計_opus_v1.md` | 518 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` | 一致 |

四 blob とも CR、TAB、BOM は 0。新規二文書に campaign の具体係数、
分岐値、raw shard 名等の封印値は書かれていない。spec の
`supersedes_v3/v4/v5` も既監査 digest
`83c9f588...` / `9b2f26ab...` / `290c7d57...` と一致する。

従って便 64 F8 の **artifact existence blocker 自体は閉じた**。以下は
新しく実体化された contract の意味監査である。

---

## F3. 新規二 artifact で通った部分

### F3.1 verifier contract

次は PASS。

- verifier は第三の判定 lane でなく、単独で candidate `ACCEPT` を出さない。
- generator の結論を読むだけでなく、A/B が witness を別々に再計算する。
- ramification divisor on \(C\) と branch divisor on
  \(\mathbf P^1\) の二対象を、W-1〜W-6 の各々で検査する。
- ambient ring、quotient relations、coefficient field、embedding、
  monomial order、reduction contract の存在と digest を先に検査する。
- 片側 PASS、多数決、相手の中間結果の先読みを禁止する。
- contract/spec の lifecycle を creation snapshot と外部 receipt authority
  に分ける。

これは便 64 の「単なる prose ID では足りない」という要求に対する実質的な
前進である。

### F3.2 dependency manifest

次の設計方向も PASS。

- dependency を直接辺で止めず fixpoint まで展開する。
- alias / path rename / wrapper を content digest と到達経路で追う。
- role 欠落を fail-closed にし、迷えば `math-helper` とする。
- mathematical helper を `allowed_shared_tcb[]` に入れない。
- producer の自己申告した交差でなく、受領側が集合積を再計算する。
- TCB 追加を receipt 変更とし、追加側に挙証責任を置く。

しかしこの方向を operational な全域規則へ落とす箇所で、F4〜F7 の反例が
残る。

---

## F4. blocker B65-1 — Bézout は点同一性でなく非交差を証明する

contract §3.1 は W-2 `exact_point_equality_witnesses` の一形式として

```text
1 = sum_i u_i g_i
```

を展開し、結果が \(1\) なら PASS とする。しかしこれは一般に
**二 ideal の和が単位 ideal、すなわち supports が交わらないこと**の
certificate であって、二点の同一性 certificate ではない。

最小反例は \(R=\mathbb Q[x]\) の二点

\[
I_0=(x),\qquad I_1=(x-1)
\]

である。二点は異なるが、

\[
1=x-(x-1)\in I_0+I_1
\]

なので、現 contract の Bézout 分岐は W-2 を PASS にする。これは
「異なる点」を「同じ点」として component bijection へ流し、W-1〜W-6
全体の false positive を許す。

spec v6 §4.2 にも同じ未型付けの `Bézout / reduction certificate` があるため、
governing spec 優先を守る contract 側だけでは安全に上書きできない。
修理は witness kind を分けること。

```text
kind = ideal-equality:
  I0 subset I1 と I1 subset I0 を、
  各生成元の membership / reduction-to-zero certificate で検査

kind = disjointness:
  1 in I0 + I1 の Bézout certificate
  # 非対応 component の排除には使えるが W-2 の equality PASS には使わない
```

`reduction certificate` も「各生成元が相手 ideal で 0 に reduce する」のか、
「\(1\) を得る」のかを tag で区別しなければならない。これは freeze blocker。

---

## F5. blocker B65-2 — `[25]` / `[26]` の提示割当は排他的でない

提示案は

```text
A/B verifier verdict mismatch     -> [25] divisor-equality-failure
searcher/checker native mismatch   -> [26] checker-mismatch
```

とする。しかし searcher/checker の native divisor が不一致なら、それを
同一視する W-1〜W-6 の equality witness も不成立となる。従って同じ原因が

```text
native mismatch          -> [26]
witness invalid          -> [25]
```

を同時に発生させる。finite partition まで違えば `[24]` も重なる。これは
contract §5 冒頭の「同一 event に二 code を割り当てない」を満たさず、
`[26]` の未割当を閉じていない。

最も小さい排他的案は次である。

```text
[25] = A/B verifiers がともに certificate witness の欠落・不成立を確認
[26] = 同じ certificate / native inputs に対する A/B verifier result の不一致
```

この場合、searcher/checker native の実体的な差は `[13]`〜`[25]` の
specific check へ送る。別案を採るなら、spec 側に `[24]` / `[25]` /
`[26]` の mutually exclusive predicates と precedence を明記する必要が
ある。現行の「native 不一致を `[26]` に予約」は不採用。

---

## F6. blocker B65-3 — dependency closure が共通の untrusted input を飲み込む

verifier contract §2 は、A/B が**同じ**

- divisor equality certificate、
- searcher native artifact、
- checker native artifact

を入力として読むことを要求する。一方 manifest R-1 は

> \(X\) が直接 import / link / **load** する全 artifact

を dependency closure に入れる。

文字どおりなら、上の三 input digest は
\(D_A\cap D_B\) に必ず現れる。これらは runtime TCB ではなく、まさに
**信用せず独立に検査すべき共通入力**であるから
`allowed_shared_tcb[]` に入れてはならない。その結果、正しく独立な二
verifier でも

\[
(D_A\cap D_B)-\mathrm{TCB}\ne\varnothing
\]

となり、必ず `[11] shared-helper-detected` で停止する。

共有 input と共有 implementation は型を分ける必要がある。

```text
declared_untrusted_inputs[] =
  {certificate, searcher_native, checker_native, governing spec/contract}

implementation_dependency_closure_A/B[] =
  code / library / runtime / build-time data の推移閉包

forbidden_shared_implementation_intersection =
  (closure_A intersection closure_B) - allowed_shared_tcb
```

untrusted inputs は両 verifier で digest 一致を要求するが、TCB として
差し引くのではなく、そもそも implementation closure の universe から
分離する。この型分離なしでは contract と manifest を同時に満たす実装が
存在しない。

---

## F7. manifest の追加 blocker

### F7.1 depth 0 だけでも完全閉包になり得る

H-1 は「`depth = 0` の entry しかない manifest は、それ自体が不備」と
する。しかし \(X\) が自己完結な leaf artifact \(L\) を一つだけ直接 load
し、\(L\) が何も load しない場合、

\[
D=\{L\}
\]

は正しい fixpoint で、全 entry の depth は 0 である。現規則は完全な
manifest を拒否し、架空の depth-1 dependency を要求する。

必要なのは depth の見た目でなく、各 node の outgoing dependency 証明と
受領側の fixpoint 再計算である。「depth 0 のみを自動 FAIL」は削除する。

### F7.2 exact blob identity と rebuild lineage が接続されていない

E-1 と I-1〜I-4 は identity / 集合積を `content_digest` だけで定める。
ところが H-2b は「同一 source を別 toolchain で build して digest が
変わっても同一 helper とみなす」とする。後者を実行するための mandatory
な source digest / lineage identity は record にない。

- `source_ref` は任意かつ human-readable。
- `build_root_id` の意味と digest 規約は未定義。
- I-7 は build root **かつ** toolchain が同じ場合しか止めないため、
  同じ source・異なる toolchain という H-2b の主例を拾わない。
- H-2b の「同一とみなしてよい」は受領側の裁量で、同じ bundle が PASS と
  FAIL の両方になり得る。

`source_closure_digest` または `implementation_lineage_digest` を mandatory
にし、

```text
content intersection も lineage intersection も空
```

を要求するか、H-2b の過大主張を削る必要がある。

### F7.3 初期 TCB は依然として値がない

新 manifest は `allowed_shared_tcb[]` の**型**を与えたが、初期の exact
entries は提示していない。これは receipt で

```text
allowed_shared_tcb = []
```

と明示すれば安全に閉じられる。共有 runtime / parser / hash primitive を
許すなら、各 exact digest・role・justification を実装着手前の receipt に
列挙すること。省略を暗黙の空集合とも暗黙の許可とも読ませてはならない。

---

## F8. bundle のうち発行可能になった値

意味 blocker が直れば、次は現在の exact bytes のまま receipt に記入可能
である。

```text
predicate_spec_id =
  "mb/ninfty-stage2-predicate/v6"
predicate_spec_digest =
  00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a

verifier_contract_id =
  "mb/ninfty-verifier-contract/v1"
verifier_contract_digest =
  ae7950f3dec9081029dbda8c60e7fb8bc8e23030d8fa555915ea1eea012d136d

dependency_manifest_schema_id =
  "mb/dependency-manifest/v1"
dependency_manifest_schema_digest =
  7d513049fa8e79b5c32054135222356e26cf9f32e9e8f8ae6c5ce71aeaf3cdc9

S5_source_digest =
  b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555
```

ただし上二 contract digests は**監査 FAIL の candidate digests**なので、
上表は freeze issuance ではない。v3/v4/v5 の supersedes 連鎖も exact
だが、approved receipt 前に operative supersession として扱わない。

---

## F9. freeze / 実装認可の最終裁定

```text
artifact existence closure                 = PASS
full-blob binding values                    = AVAILABLE
lifecycle separation                        = PASS

W-2 equality soundness                      = FAIL
reason-code routing totality                = FAIL
dependency/input universe separation        = FAIL
closure completeness criterion              = FAIL
rebuild-lineage criterion                   = NON-OPERATIONAL
initial allowed_shared_tcb                   = UNSPECIFIED

predicate_spec_freeze_id                    = NOT ISSUED
searcher_v2 implementation                  = NOT AUTHORIZED
checker implementation                      = NOT AUTHORIZED
D-2 generator implementation                = NOT AUTHORIZED
verifier A/B implementation                 = NOT AUTHORIZED
model_builder                               = LOCKED
```

EP 到達前の `partial predicate / UNKNOWN` 札、decision/audit lane 分離、
旧 8 hit の neutral lane 限定は正しいが、実装認可の前提となる contract が
まだ sound でないため、これらを条件にした限定認可も出さない。

---

## F10. 再提出の最小条件

1. spec の W-2 を `ideal-equality` と `disjointness` に型分離し、Bézout
   \(1\) を equality PASS から除く。
2. `[24]` / `[25]` / `[26]` を排他的に定義する。推奨は
   `[26] = A/B verifier result mismatch`。
3. manifest の universe を `declared_untrusted_inputs[]` と
   `implementation_dependency_closure[]` に分ける。
4. 「depth 0 のみなら不備」を削り、fixpoint proof だけを基準にする。
5. H-2b を残すなら mandatory lineage digest と機械的な交差式を追加する。
6. freeze receipt draft に初期 `allowed_shared_tcb[]` を literal に置く。
   最小値は `[]`。
7. 修理後の spec / contract / manifest を再 hash し、S5 full digest と
   supersedes chain を一つの bundle にする。

W-2 は governing spec 自身の文言を動かすため、最も明瞭なのは spec v7
である。もし v6 のまま保持するなら、versioned erratum artifact を
governing spec と同格に束縛し、優先関係を反転させる必要があり、v7 より
複雑になる。

---

## F11. ★教材

1. **Bézout の \(1\) は「同じ」の証明ではなく「交わらない」の証明である。**
   witness の式が exact でも、命題への向きが逆なら verifier は精密に誤る。
2. **共通 input と共通 implementation は別物である。** 二検査器に同じ
   certificate を渡すことは独立性違反でなく、同じ canonicalizer を使う
   ことが違反である。
3. **depth の最大値は closure 完全性の証明にならない。** leaf だけなら
   depth 0 で fixpoint である。
4. **binary content identity と source lineage identity は別の同値関係で
   ある。** 両方を使うなら、二つの digest と二つの交差式が要る。
5. **reason code の名前を予約するだけでは routing は total にならない。**
   predicates の排他性を反例で検査する必要がある。

---

## F12. 共同設計者発案

dependency evidence は三集合に分けると小さくなる。

```text
U = shared_untrusted_inputs
    # certificate, native blobs, governing specs

D_A, D_B = implementation dependency closures
    # code, libraries, runtime, build-time/output-affecting tables

T = explicitly allowed shared TCB

required:
  input_digest_set_A = input_digest_set_B = U
  (D_A intersection D_B) - T = empty
  math_helper_lineage_A intersection math_helper_lineage_B = empty
```

ここでは \(U\) は「共有して信用するもの」ではなく「共有して**別々に検査
するもの**」である。TCB と同じ差集合へ入れないため、independence の意味が
明瞭になる。

reason code は prose 表だけでなく、各 event predicate に
`exclusive_with[]` と `fallback_to` を持たせた小さな routing table にする
ことを勧める。negative fixture として少なくとも

```text
native differs + both verifiers FAIL
native same + verifier verdicts disagree
partition differs + divisor witness fails
```

の三複合例を事前登録すれば、今回の `[24]/[25]/[26]` 重複を機械検出
できる。

---

## F13. 監査範囲外申告

### 本便で行ったこと

- 便 65 委嘱、対話帳 T-17 まで、便 64 返信の読解。
- target / HEAD / worktree の対象 blob 同一性、SHA-256、LF 行数、
  CR/TAB/BOM の照合。
- verifier contract と dependency manifest の全文紙上監査。
- W-2 への \(\mathbb Q[x]\) 上の二点反例、closure / routing の全域性検査。
- spec v6、二 contract、S5 source、supersedes chain の bundle 突合。

### 本便で行っていないこと

- Z-norm operative transaction、receipt、W3-20/21 の検分
  （委嘱どおり次便 scope とした）。
- searcher / checker / generator / verifier の実装または実行。
- dependency manifest / TCB の実データ生成。
- sealed candidate、旧 8 hit、negative fixture、EP の観測。
- GAP 探索、Lean 証明書、Model-Builder の解錠。

従って本便は contract の paper audit であり、Lean の意味での
`verified` ではない。指定返信ファイル以外の既存 artifact は変更して
いない。
