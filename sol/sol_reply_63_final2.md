# 便 63 返信 — Z-norm candidate C 第3次 / \(N_\infty\) spec v5 最終監査

## F1. 総合判定

| Part | 判定 | 裁定 |
|---|---|---|
| **Part A — candidate C 第3次** | **差戻し** | component 1/2 の lifecycle 時制分離、再 hash 連鎖、final seal の digest 束は PASS。\(B_{\rm FC}\) v2.14 も大部分を修理した。しかし live 状態札に、`[pre-event candidate]` と「採用済み」の同居、および「旧表現を撤回」の直後に同じ `Z(未凍結)…関所` を再掲する箇所が残る。**A62-1 の live 全域同期はまだ再現せず、発効宣言を出さない。** |
| **Part B — \(N_\infty\) spec v5** | **数学核 PASS / freeze 層は差戻し** | 全文再掲、4体の型、valuation identity、ambient algebra の必要項目、二 native の分離は通る。しかし reason の「16段」は実際には18段で、verdict 間の優先と `accepted` の排他が未定義。二 verifier の空交差も完全依存閉包なしには十分でない。§6 は literal digest でなく `sha256(§本文)` の式のままで、節 byte 範囲も未規定。さらに frozen candidate 自身が無時制の `NOT ISSUED / NOT AUTHORIZED / LOCKED` を保持する。**freeze ID と実装認可は発行しない。** |

本便の operative な裁定は次である。

```text
znorm_candidate_c_third_apply = NOT ACCEPTED
effect_declaration            = NOT ISSUED
event_receipt                 = NOT ISSUED

ninfty_spec_v5_freeze_id      = NOT ISSUED
implementation_status         = NOT AUTHORIZED
model_builder_status          = LOCKED
```

---

## F2. 対象 blob・digest・形式照合

実体 `ops/inbox_codex/sol_task_63_final2.txt`、対話帳 T-17 まで、便 62
返信、および対象 artifacts を読んだ。委嘱指定 target は commit
`be1c394`、現在 HEAD は配送 commit `70e7902` である。対象 paths は
target \(\to\) HEAD \(\to\) worktree で byte 同一だった。

| artifact | LF 行数 | SHA-256 | 委嘱値 |
|---|---:|---|---|
| `docs/znorm_forall_proof_v1.md` | 106 | `75e9f072a900d5b66851193aeca153af67d59a7f7265e88893d95f2e53faa20f` | 一致 |
| `docs/k5_migration_record_v1.md` | 110 | `57913283efc1fd2c7748c03bcbcd5e7c410f355ee1216f34bea67c2a8d831dce` | 一致 |
| `docs/znorm_seal_final_v1.md` | 211 | `a3c8cc9a7198ac61b90422bdd369e67fa490ed6b160e8f797be39c08780afc26` | 一致 |
| `docs/week4-BFC攻略_opus_v2.md` | 1297 | `3676a3fec3cbba206222016e7da8c9619562df051408d5117b8359c8ab20383a` | 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 892 | `b3ec912b7170fea8fcdcc77c6bca96e944abe676668591ff85c6c28b7388a77a` | 不変・一致 |
| `docs/week4-K5_Rule1_v1_5.md` | 1052 | `861e934be7e309d4cd722874f2b04a9f44f1ab2f7c4f372dc225966813d2f431` | 不変・一致 |
| `docs/manifest_k5_v1_7.md` | 220 | `307c57942c1ba9050fc3d9ee424ca812300da41665d39387defc4cbdfc57377d` | 不変・一致 |
| `docs/znorm_apply_patches_v1.md` | 100 | `8265d395d4c311290a1c1ead01084dd3351409d988c60012f0721e6a51c8c417` | 不変・一致 |
| `docs/week4-NInfty_stage2_spec_v5.md` | 388 | `290c7d5768f95e9a1b9412fea123cfa36527f7e3917a1b656fe4479065d9428b` | 一致 |

全 9 blob で CR、TAB、LF 以外の C0 制御文字はいずれも 0。これは blob
同一性と形式の照合であり、以下の意味・型裁定とは別である。

---

# Part A — candidate C 第3次

## F3. A62-2 と再 hash 連鎖は PASS

component 1/2 冒頭は、無時制の live 状態を撤去して

```text
embedded_state_at_candidate_creation = drafted / unapproved / non-operative
live_operative_status_authority       = approved event receipt
```

へ分離した。末尾の

```text
immutable candidate blob;
operative iff bound by the approved event receipt
```

と矛盾せず、便 62 F5 は閉じた。旧 component digest
`c96efb7...` / `160aebf...` / 旧 final digest `2a29b764...` の残存も対象
三文書で 0 だった。

final seal §3/§9 の component 値は実測
`75e9f072...` / `57913283...` と一致し、K5 inventory の
`migrated_record_digest` も component 2 と一致する。final candidate hash
`a3c8cc9...` も再現した。component 2 の依存を proof ID に留め、実 digest
を final seal に一元化する topology、final 自身に receipt digest を要求
しない C \(\to\) R topology も正しい。

\(B_{\rm FC}\) v2.14 の §0 第5・6項、§2、§8、§12、§13 の主たる修文は、

```text
GLOBAL       = seal-relative exact epsilon
PER WINDOW   = migrated window の link
PRE-EVENT    = candidate
POST-RECEIPT = operative
HISTORY      = 現行判定ではない
```

を区別する方向へ直っている。数学命題・前件集合の変更も認めない。

---

## F4. blocker A63-1 — label は付いたが live 文の意味がまだ衝突する

### F4.1 系 B-7′ の状態札

\(B_{\rm FC}\) v2.14 の系 B-7′ 直後の live 状態札は、

```text
[global seal-relative][per-window inventory][pre-event candidate]
根の正規化は Z-norm-seal/v1 で採用済み
```

とする。`pre-event candidate` なら seal はまだ operative でなく、
「採用済み」は post-receipt の文である。三つの label を並べても、どの
節がどの時制に属するかを指定しなければ矛盾は消えない。

正確には例えば、

```text
[pre-event candidate]
  seal-relative theorem and K5 migration are approved candidates,
  but are not operative.

[post-receipt operative]
  the approved receipt makes the named seal and K5 migration operative.
```

と文を分ける必要がある。

### F4.2 §12 の撤回直後の再掲

§12 の live 依存説明はまず、

> 「\(Z\)(未凍結)も同じ関所」という v2.13 までの表現は撤回する

と正しく書く。しかし同じ行の直後に、

> ただし「唯一」ではない — **\(Z\)(未凍結)も同じ向き感受性の関所**

を無分類の現行文として再掲する。これは撤回した旧状態をその場で復活
させている。`【v2.7】` という版注は四分類の
`[historical quotation]` に代わらず、live §12 の現在文である。

現行文は例えば、

```text
[global seal-relative]
  TB4 / epsilon factor is supplied relative to the named seal and framework.

[per-window inventory]
  the tbar factor is supplied only for migrated windows;
  K5 supplied, K3/A5 pending.

[historical quotation]
  v2.7 called both items "gates"; that status vocabulary is withdrawn.
```

とすればよい。

従って「live 未型付け 0」は再現しない。全15箇所を再び開ける必要はなく、
上の二 live 文を意味単位で直す小差分で足りる。

---

## F5. Part A 発効裁定

```text
component lifecycle typing           = PASS
component / final hash chain          = PASS
final-seal inventory binding          = PASS
BFC four-class design                 = PASS
BFC live semantic synchronization     = FAIL

candidate_c_third_atomic_apply        = NOT ACCEPTED
effect_declaration                    = NOT ISSUED
status_on_apply / applied_at          = MUST REMAIN BLANK
operative_hash                        = NOT MINTED
event_receipt R                       = NOT ISSUED
CLAIMS operative entry                = NOT AUTHORIZED
```

`a3c8cc9a...` は candidate final-seal hash であって operative hash ではない。
上の修理が \(B_{\rm FC}\) だけなら component 1/2 と final candidate の bytes
を動かす必要はない。ただし新しい \(B_{\rm FC}\) digest を apply payload
と receipt に束縛し、許可された final 状態欄を埋めた**後**の operative
final hash を receipt が保持しなければならない。

---

# Part B — \(N_\infty\) spec v5

## F6. 数学核と自己完結方針は PASS

### F6.1 4体の型と valuation

§1.1 は、

```text
curve coefficient field = Q
geometric working field  = k = Qbar
v                         in k^times
prediction field         = K = Q(zeta_20)
```

を分離し、closed-point valuation を整数値に正規化した。便 62 F7.1 の
要求を満たす。

有限分離拡大 \(k(C_{\rm crv})/k(x)\) に対する

\[
\operatorname{ord}_P N(g)
 =\sum_{Q\mid P}[\kappa(Q):\kappa(P)]\operatorname{ord}_Q(g)
\]

から
\(\operatorname{div}(N(g))=\pi_*\operatorname{div}(g)\) を得る一段も正しい。
従って `N∞-N` の (60.1)(60.2) は紙上 PASS。

### F6.2 補題群

`N∞-1:1` / `N∞-fix` / `N∞-pair` / `N∞-swap` / `N∞-div` /
`N∞-criterion` の再掲に新しい数学 blocker はない。とくに、

- \(s^2=-C\) なら \(H_{\pm s}=\mp2sa\);
- fixed 二 fiber の排除には \(\deg p=2\) の唯一の double root を使う;
- RH contribution \(4+4+2+2=12\) の使い切り;
- `N∞-swap` を S5 target \(\to\) (60.6) RHS の bridge とする

は整合する。

`N∞-criterion` の RHS \(\Rightarrow\) LHS 本文は、RHS が既に
\(s^2=-C\) を含むのに `N∞-swap` を一度呼ぶ。§1.9 がいうとおり論理的に
冗長だが、偽の依存や循環ではない。次版で削れば dependency 表が読みやすく
なるという推奨事項に留め、blocker にはしない。

### F6.3 全文再掲

normative proof body を v5 §1 に全文再掲し、v3/v4 を記録目的に限定する
方針は PASS。`v5 > v4 > v3` は theorem の成立に必要な import merge では
なく、監査系譜だけになった。この選択により便 62 F11.1 の proof-import
blocker は閉じた。

---

## F7. ambient algebra 5欄 — 必要な型は揃ったが freeze 実体は未束縛

§4.1/§4.2 は次を certificate に持たせた。

```text
ambient coordinate ring + quotient relations
coefficient-field presentation
field-embedding witness schema
monomial order
Groebner reduction / normal-form contract
```

ring・係数体 presentation・変数順・term order・reduction contract が
**具体的に解決されるなら**、reduced Gröbner basis と normal form は一意に
なる。相互 ideal inclusion の表現係数または Bézout/reduction 列を witness
とする判断も正しい。searcher/checker 各々で
`ramification_divisor_on_C_ref` と `branch_divisor_on_P1_ref` を分けた修理も
PASS。

ただし freeze schema としては次を明瞭にする必要がある。

1. 単数 `ambient_quotient_relations` でなく、各 `chart_id` に
   ring / relations / variable order / monomial order を対応させること。
   \(C\) 上、\(\mathbb P^1\) 上、infinity chart は同一 ring ではない。
2. \(k=\bar{\mathbb Q}\) は幾何的 working field であり計算用の有限
   presentation ではない。各 algebraic point を担う有限 number field
   または共通 splitting field の presentation と \(k\) への embedding を
   concrete witness に持たせること。
3. §6 は §4.1/§4.2 の**schema 文**を参照するだけで、
   `groebner_reduction_contract_id` / `verifier_contract_id` の具体値を
   freeze bundle に束縛していない。

従って問2への答えは、**field category と witness shape は PASS、現 freeze
bundle における concrete contract binding は不足**である。

---

## F8. blocker B63-1 — `shared_helper_intersection = ∅` だけでは独立性を検収できない

G-1〜G-5 の原理と、A/B の verifier ID・code digest・result digest を別々に
保存する方向は正しい。しかし

```text
dependency_manifest_A
dependency_manifest_B
shared_helper_intersection = empty
```

だけでは次が未定義である。

- manifest が直接依存だけか、**推移的依存閉包**か;
- 同じ helper を別名・別 path・薄い wrapper で包んだ場合の同一性;
- runtime、parser、serialization、CAS/library のどこまでを helper と数えるか;
- schema parser や hash primitive など、共有を許す trusted base。

「全 helper」の文字どおりなら標準 runtime 等の共有で交差は通常空にならず、
それらを暗黙に除けば共通 canonicalizer を除外した証拠にならない。

必要なのは例えば、

```text
dependency_manifest_schema_id + digest
dependency_closure_A[] = transitive content digests
dependency_closure_B[] = transitive content digests
allowed_shared_tcb[]   = frozen content digests + role
forbidden_shared_math_helper_intersection
    = (closure_A ∩ closure_B) - allowed_shared_tcb
    = empty
```

である。intersection は producer の自己申告値を信じず、receipt 受領側が
canonical content digest 集合から導出する。別 build root / toolchain /
implementation provenance も receipt に残すと、同一実装の path 改名を
独立二実装と数える事故を防げる。

従って空集合検査は**必要な一部**だが、現状では G-4 の十分な運用証跡では
ない。

---

## F9. blocker B63-2 — reason の全順序と verdict state machine

### F9.1 「16段」ではなく18段

§0 と委嘱は INTEGRITY_STOP を16段とするが、実列挙は
\([9]\) から \([26]\) までで、個数は

\[
26-9+1=18
\]

である。追加された `shared-helper-detected` と
`pell-implies-coprime-mismatch` を含む現在の enum は**18段**と呼ぶのが
正しい。列挙自体は全順序なので、単なる表題 typo だけなら軽微である。

### F9.2 verdict 間の dominance が逆転している

§5.3 は public primary を「下の全順序で最小」とし、

```text
[0] accepted
[1]..[8] REJECT
[9]..[26] INTEGRITY_STOP
```

と並べる。一方、設計理由は `[9]–[12]` の証拠不信を「最優先」とする。
例えば `precondition/degree-mismatch` と `sealed-field-leak` が同時に
検出された場合、数値最小規則は REJECT [1] を選び、証拠汚染 [9] を隠す。
これは設計理由と逆である。

また `accepted` が failure 集合と同時に `all_reason_codes[]` に入ることを
禁ずる不変条件がない。入れば [0] が常に primary となる。

total state machine は次のように verdict と reason priority を分けるのが
安全である。

```text
I = detected integrity reasons
R = detected mathematical reject reasons

if I != empty:
    verdict = INTEGRITY_STOP
    primary = minimum(I, integrity_priority)
elif R != empty:
    verdict = REJECT
    primary = minimum(R, reject_priority)
else:
    verdict = ACCEPT
    primary = accepted
    all_reason_codes = [accepted]

invariant:
    accepted appears iff I = R = empty
```

envelope-level leak / digest / dependency checksは early REJECT より先に行う。
この定義なら `[15] pell-derivative-mismatch` と
`[25] divisor-equality-failure` の同時例で primary=[15] という局所判断は
期待どおりである。**18段内部の順序方針そのものには反対しない。**

### F9.3 G-2 と enum の routing が衝突する

§4.3 G-2 は「入力 digest 不一致」を
`divisor-equality-failure` へ送るが、§5.3 は専用の
`digest-mismatch` [12] を持つ。同一 event に二つの code が割り当たる。

```text
input/native/certificate digest mismatch -> digest-mismatch
missing or invalid equality witness       -> divisor-equality-failure
```

へ分ける必要がある。

以上は reason の cosmetic な並べ替えでなく、同一入力に対する
`verdict + primary_reason_code` の一意性に関わるため freeze blocker とする。

---

## F10. blocker B63-3 — §6 はまだ concrete freeze bundle ではない

### F10.1 literal digest が無い

§6 の7定理と7 schema は、

```text
digest = sha256(§1.2 本文)
digest = sha256(§4.1 本文)
...
```

という**計算式**であり、64桁 hex の実値ではない。`§x.y 本文` についても、

- heading 行を含むか;
- 次 heading 直前の空行・`---` を含むか;
- UTF-8/LF をそのまま使うか、正規化するか

が規定されていない。同じ blob から複数の正当な section digest が出るため、
後から値を選べる。

実例として、v3 §1.1 を「heading 行を含み、次の同階層 heading 直前までの
exact UTF-8/LF bytes」とする自然な規約で再計算すると先頭16桁は
`27252221b02abfcd` であり、§0.1 の記録値
`d7ee78c460bfec6e` と一致しない。別規約を採った可能性はあるが、その規約が
文書にも再現 script にも無いこと自体が問題である。

### F10.2 ID も concrete dependency binding になっていない

次は versioned artifact ID でなく、statement の説明である。

```text
squareclass_quotient_schema_id = "K^x / (K^x)^2"
minus_one_square_proof_id      = "i = zeta_20^5 in K"
```

また `s5_4_infinity_dependency_id` の digest を S5-4∞ の source artifact
でなく v5 §7 本文へ向けると、外部 dependency の identity を束縛せず、
「依存すると書いた自分の段落」を束縛するだけになる。

§4.4 の record は `verifier_contract_id + digest` を要求するが、§6 の
schema 群には concrete `verifier_contract_id/digest` が無い。

### F10.3 fail-closed な簡約

section digest を必要とせず、

```text
predicate_spec_id     = "mb/ninfty-stage2-predicate/v6"
predicate_spec_digest = sha256(full exact blob)

lemma_id = predicate_spec_id + "#N-inf-N"
bound_blob_digest = predicate_spec_digest
```

のように**全 fragment を full-blob digest へ anchor**するのが最小である。
個別 section digest を残すなら、byte-range extraction algorithm の
versioned ID、exact boundary、encoding、line-ending rule と literal hex を
全列挙すること。

従って full blob `290c7d57...` は正しく再現したが、§6 の内部束はまだ
実値 freeze bundle ではない。

---

## F11. blocker B63-4 — frozen candidate 内の lifecycle state

v5 冒頭は無時制で

```text
predicate_spec_freeze_id = NOT ISSUED
implementation_status    = NOT AUTHORIZED
model_builder_status     = LOCKED
```

とし、§9 も `implementation_status = NOT AUTHORIZED` を現行命令として
再掲する。この exact blob digest `290c7d57...` に freeze ID と実装認可を
外から発行すると、frozen artifact 自身が反対の live 状態を主張し続ける。
欄を直接更新すれば full digest が変わり、現在提示された hash は freeze
digest でなくなる。

Part A の A62-2 と同じ修理を適用すること。

```text
embedded_state_at_candidate_creation = {
  freeze_id: NOT ISSUED,
  implementation: NOT AUTHORIZED,
  model_builder: LOCKED
}
live_freeze_and_authorization_authority = approved freeze receipt
```

§9 も「receipt 前は禁止、approved receipt 後は receipt の scope に限って
認可」と時制を付ける。この修文後の exact blob を hash して初めて freeze
対象にできる。

---

## F12. 委嘱 §8 の六問への回答と Part B 裁定

| 問 | 回答 |
|---|---|
| **1. 体の型** | **PASS。** \(\mathbb Q\)、\(k=\bar{\mathbb Q}\)、\(v\in k^\times\)、\(K=\mathbb Q(\zeta_{20})\)、整数正規化 valuation は便 62 F7.1 を閉じる。 |
| **2. ambient 5欄** | **型カテゴリは PASS / concrete freeze は不足。** ring・relations・field presentation・embedding・term order・reduction contract が解決されれば一意。ただし per-chart map と実 contract binding が要る。 |
| **3. 18段 priority** | **INTEGRITY 内部の順序と `[15]` vs `[25]` の選択は可。** ただし段数誤記、verdict dominance、`accepted` 排他、G-2 routing が未定義なので schema 全体は FAIL。 |
| **4. helper 空交差** | **必要だが十分でない。** complete transitive content-digest closure、versioned manifest schema、allowed shared TCB、受領側による導出が必要。 |
| **5. section ID/digest** | **FAIL。** ID の説明化、literal hex 欠落、section byte 規約欠落、source dependency の自己段落 digest 化が fail-closed でない。full-blob anchor を推奨。 |
| **6. 全文再掲と記録 manifest** | **方針 PASS。** normative body を v5 に一本化した判断は正しい。ただし記録用 section digest も再現規約を付けるか削除すること。 |

最終状態は次である。

```text
predicate mathematics                 = PASS (paper audit)
self-contained theorem body           = PASS
ambient witness categories            = PASS
reason/verdict total function          = FAIL
two-verifier operational evidence      = FAIL
concrete freeze dependency bundle      = FAIL
freeze lifecycle typing                = FAIL

predicate_spec_freeze_id               = NOT ISSUED
implementation_status                  = NOT AUTHORIZED
model_builder_status                   = LOCKED
```

従って `290c7d57...` に freeze ID を形式だけ発行せず、searcher / checker /
D-2 generator / verifier A / verifier B の実装着手も認可しない。

---

## F13. 次回差分の最小条件

### Part A

1. \(B_{\rm FC}\) の系 B-7′ 状態札を pre-event と post-receipt の二文に分ける。
2. §12 で撤回直後に再掲した `Z(未凍結)…関所` を current per-window 語彙へ
   置換するか、明示的 historical quotation に入れる。
3. 新 \(B_{\rm FC}\) hash と、修文箇所だけの live-status lint を提示する。
   component/final candidate は byte 不変なら再 hash 不要。

### Part B

1. INTEGRITY 18段へ表題を直し、F9.2 の verdict state machine と
   `accepted iff no failure` を規範化する。
2. G-2 の digest failure / equality-witness failure routing を分離する。
3. helper manifest を推移依存閉包・content digest・allowed TCB で型付ける。
4. per-chart ambient algebra と concrete verifier/reduction contract を束縛する。
5. full-blob anchored fragment ID、または canonical section extraction +
   literal digest を採用し、B9/source dependency の versioned ID を実値化する。
6. freeze/authorization 状態を creation-time snapshot と receipt authority に
   分離する。

数学核の再証明は不要。次版は schema/lifecycle/digest 差分だけを主対象に
すればよい。

---

## F14. 共同設計者としての発案

### F14.1 verdict を ordered list でなく total function として凍結する

reason の表は人間向け表示に留め、規範を

```text
decide(integrity_set, reject_set)
  -> (verdict, primary_reason, canonical_all_reasons)
```

という純関数にする。positive control、REJECT+INTEGRITY 同時例、
二 INTEGRITY 同時例を fixture にすれば、表の追記で dominance が壊れる
事故を機械的に拾える。

### F14.2 fragment ID は Merkle 化より full-blob anchor を先に使う

現規模では各節を別 hash にする利益より、section boundary 規約の事故面が
大きい。full blob 一個と fragment anchor の組で theorem/schema ID を
作れば、どの一字の修文も全体 digest を動かすため最も fail-closed である。
将来 artifact が巨大化して初めて、versioned extraction/Merkle schema を
導入すればよい。

### F14.3 independence receipt に「許される共有」を正面から書く

独立性を「共通物ゼロ」と定義すると、実際には共有している runtime や
serialization contract が台帳外へ押し出される。むしろ

```text
allowed shared TCB     = small, named, digest-bound
shared math helpers    = empty
algorithm provenance   = distinct
```

を三欄に分ける。隠れた共有をゼロと偽装するより、小さな共通基盤を明示して
監査する方が強い。

---

## F15. ★教材

1. **status label を置くだけでは時制衝突は消えない。**  
   `[pre-event] adopted` のように本文が逆なら、label より本文が勝つ。

2. **撤回文の直後に同じ旧文を再掲すると、撤回は成立しない。**  
   historical quotation は引用範囲を明示する必要がある。

3. **全順序の要素数も schema の一部である。**  
   `[9]`–`[26]` は16でなく18。件数誤記は enum 差分の見落としを示す。

4. **`accepted` は最小 failure code ではなく空集合の sentinel である。**  
   failure と同居させず、`accepted iff no failure` を不変条件にする。

5. **manifest の空交差は manifest の完全性以上には強くない。**  
   推移依存閉包、content identity、allowed TCB が無ければ path 改名で
   独立性を偽装できる。

6. **`sha256(§本文)` は digest ではなく未実行の手順である。**  
   byte range と canonicalization、literal hex が無ければ freeze 束に
   ならない。

7. **immutable freeze blob に live authorization state を埋めない。**  
   creation snapshot と receipt authority を分ける規律は、seal component
   だけでなく spec にも同じく適用される。

---

## F16. 監査範囲外申告

### 本便で行ったこと

- 便 63 委嘱、対話帳 T-17 まで、便 62 返信、対象 artifacts の読解;
- target commit / HEAD / worktree の対象 blob 同一性、SHA-256、LF 行数、
  CR/TAB/C0 の照合;
- component/final の digest 束と \(B_{\rm FC}\) v2.14 live status の差分監査;
- spec v5 の全文、数学核、ambient witness、verifier evidence、reason
  state machine、freeze bundle、lifecycle の紙上監査;
- heading-bounded exact UTF-8/LF という明示規約による section hash の
  小規模な再計算。

### 本便で行っていないこと

- Part A の状態欄記入、operative hash、receipt、CLAIMS 記帳;
- freeze ID / event ID の mint、Model-Builder の unlock;
- searcher/checker/generator/verifier の実装または実行;
- sealed candidate、旧8 hit、whitelist、negative/EP fixture の観測;
- GAP 探索または Lean 証明書の作成。

従って数学層の札は **paper-audited** であり、Lean の意味での
`verified` ではない。過去返信および指定外 artifact は変更していない。
