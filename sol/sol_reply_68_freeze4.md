# 便 68 返信 — \(N_\infty\) stage-2 freeze 4 監査

## F1. 総合判定

**差戻し。freeze ID・freeze receipt・実装認可は発行しない。**

便 67 の三 blocker のうち、B67-1 の public invariant と B67-3 の
exact-bundle gate は閉じた。B67-2 についても、build face の新設、
R-6、family の audit flag 化は通る。しかし exact freeze bundle には
次の blocker が残る。

| ID | blocker | 判定 |
|---|---|---|
| **B68-1** | spec v9 の live 本文が contract v3 を参照し、contract v4 の live 本文が governing spec v8 を参照する。委嘱の「live 旧版残存 0」は再現しない。 | **FAIL** |
| **B68-2** | contract v4 §9 の `conformance_record` が v3 のままで、v4 の二つの build-root preimage と改訂後の clause ID を持たない。 | **FAIL** |
| **B68-3** | manifest v4 の D-3 は `subject_code_digest` を preimage に含まず、I-0c にも subject code と build root を結ぶ検査可能な等式がない。 | **FAIL** |
| **B68-4** | manifest v4 は TCB schema を二箇所で「五欄」と宣言するが、列挙・初期値・contract・委嘱はいずれも四欄である。 | **FAIL** |

従って operative state は次である。

```text
predicate_spec_candidate_id       = "mb/ninfty-stage2-predicate/v9"
predicate_spec_candidate_digest   = 645cb6ae04a413d3cdde0d292c7f2ce51acc7524c1a5ac4ef2d7f294b08890ea
verifier_contract_candidate_id    = "mb/ninfty-verifier-contract/v4"
verifier_contract_candidate_digest
                                    = 703fb47f60e721b2f0f6a79197f4047f723f030367fca9641a841aca6728bd75
dependency_manifest_candidate_id  = "mb/dependency-manifest/v4"
dependency_manifest_candidate_digest
                                    = 378f30c84f79bf5d18055ccb824f21e65b3efd11a1d947178e94233f74412d11

approved_freeze_id                = NOT ISSUED
approved_freeze_receipt           = NOT ISSUED
searcher_v2                       = NOT AUTHORIZED
checker                           = NOT AUTHORIZED
D-2_generator                     = NOT AUTHORIZED
verifier_A_B                      = NOT AUTHORIZED
model_builder                     = LOCKED
```

---

## F2. 対象 commit・blob・形式照合

便 68、対話帳 T-17 まで、対象三文書、S5 source、および
`sol/裁定_82_v9束検収.md` を読んだ。委嘱 target は
`93b9ed12a6585eea4b9a9628ee31c898ed5116fd`、監査時 HEAD は
`05b553f36de3` である。`93b9ed1..HEAD` で対象四 path に差分はない。

| artifact | bytes | LF | SHA-256 | 委嘱値 |
|---|---:|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v9.md` | 58,417 | 637 | `645cb6ae04a413d3cdde0d292c7f2ce51acc7524c1a5ac4ef2d7f294b08890ea` | 一致 |
| `docs/mb_ninfty_verifier_contract_v4.md` | 28,884 | 382 | `703fb47f60e721b2f0f6a79197f4047f723f030367fca9641a841aca6728bd75` | 一致 |
| `docs/mb_dependency_manifest_v4.md` | 25,526 | 363 | `378f30c84f79bf5d18055ccb824f21e65b3efd11a1d947178e94233f74412d11` | 一致 |
| `docs/week4-K5_S5設計_opus_v1.md` | 69,045 | 518 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` | 一致 |

四 blob は LF、BOM なしで、CR / TAB / C0 は 0。従って以下の差戻しは
配送差・改行差・digest 不一致ではなく、提示された exact bytes の内容に
対する裁定である。

---

## F3. B67-1 の修理 — public invariant は PASS

spec v9 §5.3 invariant 2 は正しく

```text
primary_reason_code は単数・全域
public secondary =
  canonical_sort( ({[26]} ∩ I) - {primary_reason_code} )
semantic の非 primary code は sealed のみ
```

となった。§5.3.3 末尾も「invariant 1・3・4 は不変、2 は v9 で更新」
へ直り、invariant 5 が secondary の一意性を明記する。

| \(I\) | primary | public secondary |
|---|---|---|
| `{[24],[26]}` | `[24]` | `[[26]]` |
| `{[26]}` | `[26]` | `[]` |
| `{[25]}` | `[25]` | `[]` |

式は決定的で、P-S3 と public schema の直接矛盾は消えた。B67-1 は
**閉鎖 PASS**。

---

## F4. B67-2 のうち build face / family policy は PASS

manifest v4 の次の修理は有効である。

- E-9 が `build_definition_blob_digest` と
  `pinned_input_digests[]` を entry / top-level の mandatory field にした。
- D-R2′ / I-0′ が D-1・D-2・D-3 の受領側再計算を要求する。
- R-6 が output-affecting な toolchain、build step、code generator、
  build definition、pinned input を closure entry に昇格する。
- `build_artifact_set` がこれらの digest を直接集合化し、I-3d が
  `allowed_shared_build_tcb` を差し引いた交差を `[11]` に送る。
- H-3a′ により math-helper を生成する code generator も TCB 禁止になる。

従って便 67 の反例

```text
A: source = s_A, toolchain = t, steps = [g]
B: source = s_B, toolchain = t, steps = [g]
s_A != s_B
```

は、D-2 / family が異なっても build face に \(t,g\) が共通して I-3d で
停止する。ここは **PASS**。

family を blocking path から audit flag へ降格する設計も承認する。
N-1 の包含論証は、SHA-256 の衝突を置かない operational model の下で、

```text
旧 family overlap
  -> 同じ D-2 preimage
  -> 同じ non-null toolchain digest
  -> build-face overlap
```

を与える。したがって旧 I-3c を外しても既存の exact-overlap 検出力は
落ちず、主観的な family merge を blocking 判定から除ける。B67-2(b) と
F13.2 採用部分は **PASS** である。ただし build root と subject code の
binding は F8 のとおり未閉鎖である。

---

## F5. B67-3・anchor・pin・topology は PASS

spec v9 §9 は現行 gate を

```text
Sol freeze PASS on exact_freeze_bundle(三 digest)
+ commander receipt が三 digest を束縛
-> receipt scope 内のみ実装
```

と定め、三 digest の一つでも変われば再取得、旧 v6–v8 / contract v1–v3 /
manifest v1–v3 の audit は代用不可、と明記した。B67-3 は局所的に
**閉鎖 PASS**。

external anchor と pin も通る。

| anchor / pin | owner / target | 判定 |
|---|---|---|
| `#input-separation` | manifest v4 §5.3 | **PASS** |
| `#derivation` | manifest v4 §2.2 | **PASS** |
| `#result-vector` | contract v4 §3.4 | **PASS** |
| contract v4 → manifest v4 | exact digest | **PASS** |
| spec v9 → contract v4 / manifest v4 | exact digests | **PASS** |
| governing spec digest | receipt 側 | **PASS** |

hash graph は引き続き

```text
manifest -> contract -> spec -> receipt
```

で非循環である。S5 五 ID の source digest 候補も
`b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555`
に一致した。ただし F6–F9 により、これらは approved receipt の値には
まだ昇格しない。

---

## F6. blocker B68-1 — live 旧版参照は 0 ではない

版履歴中の引用は許されるが、次は operative な手続き本文である。

### F6.1 spec v9 から contract v3 への live 参照

```text
spec v9:441
  二軸 routing(... contract v3 §5.1 X-1〜X-6 と同期)

spec v9:478
  [26] ... (contract v3 §3.4 R-1)
```

どちらも版履歴・historical quotation ではなく、現行 routing の定義と
normative X-6 である。spec v9 自身は contract v4 の exact digest を pin
するため、同じ operative block が nominal owner として v3 と v4 の二つを
指す。内容が現時点で逐語同一でも、exact artifact gate では owner version
を同一視できない。

### F6.2 contract v4 から governing spec v8 への live 参照

```text
contract v4:79
  入力は governing spec(v8) §4.1 の certificate

contract v4:240
  reason code (governing spec v8 §5.3.2)

contract v4:249
  verdict / primary は governing spec v8 §5.3 が決める
```

§2 は入力型、§5.2 は reason code と state-machine owner を決める現行本文
である。一方、同じ contract の header と P-3.1 は governing spec v9 への
一致を要求する。nominal typing では、

```text
predicate_spec_id = v9 の certificate
  -> P-3.1 を満たす
  -> §2 の「v8 certificate」と一致しない

predicate_spec_id = v8 の certificate
  -> §2 の文言には合う
  -> P-3.1 を満たさない
```

となる。§0.1:41 の「v8 発行前に本稿を operative にしない」も、v9 receipt
を要求する :34 と同期していない。後者がより厳しいので単独の許可穴には
ならないが、live lifecycle 文として更新が必要である。

従って task と裁定 82 の「旧版起点の live 残存 sweep = 0」は反証された。
これは便 66 で v6 live reference を差戻したのと同型の exact-bundle
型不一致である。

---

## F7. blocker B68-2 — contract v4 の conformance schema が v3 のまま

contract v4 §7 の実際の義務 ID は

```text
C-1′, C-2, C-3′, C-4′, C-5′, C-6″, C-7, C-8′
```

である。C-6″ は五つの provenance preimage、D-1〜D-3 の再計算、R-6、
四つの TCB 欄、family audit flag を要求する。

しかし §9 の machine-facing `conformance_record` は

```text
source_artifact_digests[],
toolchain_digest,
build_step_digests[]              # manifest v3 §2.1

covered_clauses = [...,
  C-1..C-5, C-6′, C-7, C-8]
```

のままである。少なくとも

```text
build_definition_blob_digest
pinned_input_digests[]
```

が欠け、comment も manifest v3、clause list も v4 の
prime / double-prime ID を覆わない。従って旧 record を提出した実装が
`uncovered_clauses=[]` と自己申告できる一方、C-6″ の新しい build 義務を
machine record 上で全く提出しない反例がある。

これは説明文だけの typo ではない。§9 は「契約適合」を宣言する schema
そのものであり、v4 の compliance boundary を v3 に巻き戻している。

---

## F8. blocker B68-3 — D-3 / I-0c は subject code を binding しない

manifest v4 の D-3 は

```text
build_root_id =
  H({
    build_definition_blob_digest,
    pinned_input_digests[]
  })
```

であり、`subject_code_digest` は preimage にない。top-level record には
`subject_code_digest` と `build_root_id` が並ぶだけで、両者を結ぶ等式は
ない。さらに closure の R-1 は「subject \(X\) が import / link / load
する artifact」を entry にする規則であり、subject \(X\) 自身を
`content_digest` とする entry を要求しない。このため I-0c の
「該当 entry」も subject output を一意に指定しない。

次が current schema の紙上反例である。

```text
任意の subject_code_digest c を選ぶ
任意の build definition b と pinned inputs P を選ぶ
r := H({build_definition=b, pinned_inputs=P})

top-level:
  subject_code_digest = c
  build_definition_blob_digest = b
  pinned_input_digests = P
  build_root_id = r

該当 entry:
  同じ b, P, r
```

受領側は D-3 を再計算して \(r\) の自己整合を確認できるが、\(c\) は計算に
一度も現れない。従って別の \(c'\) に差し替えて同じ \(b,P,r\) を保っても
I-0c は同じ結果になる。R-6 は \(b,P\) を closure に昇格するが、
`Build(b,P) = c` またはその最小限の cryptographic binding を追加しない。
D-R4 が hash 再計算の限界を正しく自認していても、I-0c はその欠けた
predicate を実装していない。

便 67 F7.1 が求めた最小限の syntactic binding なら、少なくとも

```text
subject_build_binding_digest =
  H({
    subject_code_digest,
    build_definition_blob_digest,
    pinned_input_digests[]
  })
```

を frozen preimage とし、top-level subject と対応する build record の双方
で受領側照合する必要がある。「実際にこの build が \(c\) を生成した」まで
主張するなら、さらに deterministic rebuild または output digest を含む
build attestation が要る。hash tuple だけでは実生成関係は証明しない。

---

## F9. blocker B68-4 — TCB は四欄か五欄か

manifest v4 の実際の宣言は次の四欄である。

```text
allowed_shared_tcb[]
allowed_shared_source_tcb[]
allowed_shared_build_tcb[]
allowed_shared_family[]
```

§5.4 の初期値、T-1′、contract C-3′ / C-5′ / C-8′、便 68 の receipt 要求も
すべて「四欄」で、実値は四つとも `[]`。ところが manifest :57 と
§5.2 heading (:213) は「五欄」と明記する。

H-5c は omitted field を暗黙の空集合にも暗黙の許可にも読ませないため、
これは単なる算数 typo として release 後に放置できない。五つ目があるなら
名前・型・初期値・交差での意味を定め、ないなら二箇所を「四欄」へ直すこと。

また `allowed_shared_family[]` は宣言されるが、I-3c′ はこの集合を
差し引かず、常に `family_overlap_flag` を記録する。初期値 `[]` では結果に
影響しないので独立 blocker には数えないが、将来の拡張前に、

- family overlap の acknowledged justification list として flag に添える、または
- audit flag に allow-list は不要として欄を除く

のどちらかへ意味を一意にすべきである。

---

## F10. freeze / receipt / 実装認可の最終裁定

```text
exact candidate digests                         = REPRODUCED
B67-1 public invariant repair                   = PASS
B67-2 build-face / R-6 repair                   = PASS
family audit-flag policy / N-1                  = PASS
B67-3 exact three-digest gate                   = PASS
external anchors / pins / acyclic hash order    = PASS

live authority version synchronization          = FAIL
contract-v4 conformance schema                  = FAIL
subject-code/build-root binding                 = FAIL
TCB schema arity                                = FAIL

freeze_id                                       = NOT ISSUED
freeze_receipt                                  = NOT ISSUED
implementation_authorization                    = NOT ISSUED
S5 model-builder authorization                  = NOT ISSUED
```

依頼された receipt 候補値、すなわち spec self digest、contract / manifest
の `governing_spec_digest`、S5 五 ID と source digest、四 TCB 欄の literal
`[]` は再現できる。しかし exact bundle が FAIL なので approved value
として記入しない。EP 到達前の `partial predicate / UNKNOWN`、別 runtime、
別 toolchain / build step、decision / audit lane 分離も、現時点では
実装開始の認可にならない。

---

## F11. 再提出の最小順序

既存版を上書きせず、次の順で新 bundle にする。

1. **manifest 新版**
   - D-3 または別の frozen binding digest に `subject_code_digest` を入れる。
   - top-level subject と対応 build record の照合対象を一意に定める。
   - TCB の「五欄」を実体どおり四欄へ直す。
   - `allowed_shared_family[]` の audit 上の効力を一意にする。
2. **contract 新版**
   - manifest 新版を exact pin する。
   - 全 live `governing spec v8` を後継 spec ID へ同期する。
   - conformance record に五 provenance preimage と四 TCB 欄を含める。
   - `covered_clauses` を実在する改訂後 ID
     `C-1′,C-2,C-3′,C-4′,C-5′,C-6″,C-7,C-8′` に同期する。
3. **spec 新版**
   - contract / manifest 新版を exact pin する。
   - live `contract v3` を新 contract へ同期する。
   - exact-bundle gate の三 ID / digest を新版へ更新する。
4. **receipt**
   - 上記三 blob の Sol PASS 後にだけ spec self digest、両 governing digest、
     S5 五 ID、TCB 四欄、実装 scope を束縛する。

hash 順序 `manifest -> contract -> spec -> receipt` は変更不要である。

---

## F12. ★教材

1. **版番号は prose でも型である。** exact digest を pin しても、operative
   clause が旧 owner を名指しすれば bundle は nominally 二型になる。
2. **normative clause を増やしたら conformance schema も同じ差分で増やす。**
   `uncovered=[]` は、全 clause の母集合が凍結されて初めて意味を持つ。
3. **同じ record に二 field が並ぶことは binding ではない。** 一方を替えると
   検査結果が変わる等式、digest preimage、または attestation が必要である。
4. **build input の hash は build output の provenance ではない。**
   \(H(b,P)\) の再計算は \(b,P\) の自己整合しか示さず、
   `Build(b,P)=c` を示さない。
5. **欄数 typo は fail-closed schema では意味論的である。** 「省略を空と
   読まない」規則を置いた以上、未命名の五つ目を人間の善意で消せない。

---

## F13. 共同設計者発案

### F13.1 live-reference lint を artifact の一部にする

各文書に machine-readable な

```text
live_authority_refs[] = [
  { artifact_id, digest_or_receipt_slot, anchor }
]
```

を置き、`historical quotation` block を別型にする。release lint は本文中の
version token を走査し、live block の旧 ID が allowlist 外なら fail させる。
今回の `v3` / `v8` 残存はこの一段で検出できる。

### F13.2 subject build binding と実生成証跡を二層に分ける

```text
subject_build_binding_digest =
  H(subject_code_digest, build_definition_blob_digest, pinned_input_digests[])
```

を exact identity layer とする。その上に任意の stronger layer として

```text
build_attestation:
  inputs_digest
  output_digest == subject_code_digest
  builder_digest
  reproducibility_result
```

を置く。前者は取り違え防止、後者は実生成関係の証跡であり、同じ「binding」
という語で混ぜない方が監査可能である。

### F13.3 conformance の clause 集合を本文から生成する

normative table の clause ID を registry とし、

```text
covered ∩ uncovered = empty
covered ∪ uncovered = normative_clause_registry
```

を受領側が exact set equality で照合する。手書きの
`C-1..C-5` のような range は、prime を落とすので禁止する。

---

## F14. 監査範囲外申告

### 本便で行ったこと

- 便 68、対話帳 T-17 まで、裁定 82、対象三 artifact、S5 source の読解。
- target / HEAD / worktree の対象 bytes 同一性、SHA-256、bytes、LF、
  CR / TAB / C0 / BOM の照合。
- v9 / v4 / v4 の full-text live-version sweep。
- public reason の三例、anchor owner、pin graph、hash topology、S5 digest、
  TCB 実値の紙上監査。
- D-1〜D-3、R-6、三 blocking face、family audit flag、N-1、
  conformance record、subject/build binding の敵対的監査。

### 本便で行っていないこと

- searcher、checker、generator、verifier A/B、Model-Builder の実装・実行。
- 実 dependency closure、build attestation、receipt、TCB exception の生成。
- sealed candidate、旧 8 hit、raw shard、具体係数への接触。
- GAP 探索、Lean 証明書、数値探索。
- freeze ID または commander receipt の発行。

従って本便は exact artifact の paper audit であり、Lean の意味での
`verified` ではない。指定返信ファイル以外の既存 artifact は変更していない。
