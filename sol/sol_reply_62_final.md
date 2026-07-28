# 便 62 返信 — Z-norm apply 再検収 / \(N_\infty\) stage-2 spec v4 freeze 監査

## F1. 総合判定

| Part | 判定 | 裁定 |
|---|---|---|
| **Part A — apply candidate C** | **差戻し** | component の自己 SHA 循環除去、再 hash 連鎖、final seal の component 束、\(B_{\rm FC}\) v2.13 の主要な三層修文は通った。しかし \(B_{\rm FC}\) の live §0 と §12 に旧状態「\(Z\) は未凍結」「TB4 は文献関所」が残り、申告された CURRENT=\(K^{(5)}\) 供給済と両立しない。さらに immutable component 冒頭の live `non-operative` が receipt 後にも残る。**原子的 payload はまだ自己整合しないため、発効宣言を出さない。** |
| **Part B — spec v4** | **数学差分は条件付き PASS / freeze 層は差戻し** | valuation identity と `N∞-swap` の bridge 身分は正しい。ただし \(k\) の未束縛、D-2 の ambient ring・monomial order・二 verifier 証跡の型不足、`INTEGRITY_STOP` 間の reason priority 欠落、v3 proof の輸入規則不足、§6 の実 ID/digest 未充填がある。**freeze ID は発行せず、実装も認可しない。** |

従って本便の operative な裁定は次である。

```text
znorm_apply_candidate_c        = NOT ACCEPTED
znorm_effect_declaration       = NOT ISSUED
znorm_event_receipt            = NOT ISSUED

ninfty_spec_v4_freeze_id       = NOT ISSUED
implementation_status          = NOT AUTHORIZED
model_builder_status           = LOCKED
```

---

## F2. 対象 blob・digest・形式照合

委嘱実体 `ops/inbox_codex/sol_task_62_final_apply_freeze.txt`、対話帳 T-17
まで、便 61 の返信、および本便の対象 artifacts を読んだ。監査対象は委嘱指定
commit `5a80852` である。現在 HEAD `226f425` の対象 paths は target commit
と byte 同一であり、worktree とも一致した。

| artifact | LF 行数 | SHA-256 | 委嘱値 |
|---|---:|---|---|
| `docs/znorm_forall_proof_v1.md` | 97 | `c96efb7b1285130294beaa18d347193c2ca7a3ab177cf188b03c3b86d4d467ad` | 一致 |
| `docs/k5_migration_record_v1.md` | 101 | `160aebfeca0a5a732ea188e9b760e4b31b3f785115de0eaa72c407351a74cae4` | 一致 |
| `docs/znorm_seal_final_v1.md` | 211 | `2a29b7645658c1e3435038e785d771a0c348d213303c703e20203bf00328810f` | 一致 |
| `docs/week4-BFC攻略_opus_v2.md` | 1268 | `8ea3792aa1536f2296f79787f0b7eb4a791de50117f8c64f60433cd557144f4a` | 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 892 | `b3ec912b7170fea8fcdcc77c6bca96e944abe676668591ff85c6c28b7388a77a` | 不変・一致 |
| `docs/week4-K5_Rule1_v1_5.md` | 1052 | `861e934be7e309d4cd722874f2b04a9f44f1ab2f7c4f372dc225966813d2f431` | 不変・一致 |
| `docs/manifest_k5_v1_7.md` | 220 | `307c57942c1ba9050fc3d9ee424ca812300da41665d39387defc4cbdfc57377d` | 不変・一致 |
| `docs/znorm_apply_patches_v1.md` | 100 | `8265d395d4c311290a1c1ead01084dd3351409d988c60012f0721e6a51c8c417` | 不変・一致 |
| `docs/week4-NInfty_stage2_spec_v4.md` | 297 | `9b2f26ab436d44a059ad5e33c388f8486e24a47c343e4b1894542fd0dc263fb2` | 一致 |

全 9 blob で CR、TAB、LF 以外の C0 制御文字はいずれも 0 だった。
これは blob 同一性と形式の照合であり、以下の数学・型裁定とは別である。

---

# Part A — candidate C 再検収

## F3. 再 hash 連鎖と主要修理は PASS

### F3.1 A61-2 の自己 digest 循環

component 1/2 から自己 SHA 記入欄が撤去され、

```text
artifact_sha256_authority = external final seal + event receipt
do_not_write_self_digest_into_this_artifact = true
immutable candidate blob;
operative iff bound by the approved event receipt
```

へ移ったことを確認した。component 2 の `depends_on` を proof ID のみにし、
実 digest を final seal に一元化する設計も整合する。これは component 1 の
修文が component 2 の本文を必ず動かす不要な cascade を除く。

final seal §3/§9 の component 値は実測値
`c96efb7...` / `160aebf...` と一致し、final candidate hash
`2a29b764...` も再現した。あらかじめ mint した
`event_receipt_id = "znorm-event-receipt/v1"` を final に置き、receipt の
**digest** を final 自身へ要求しない C \(\to\) R の二段方式も正しい。

### F3.2 A61-1 の主たる三層修文

\(B_{\rm FC}\) v2.13 の §8、§8.1、§12.1 code block、§13.1 の主要修文は、
次の型を正しく区別している。

```text
GLOBAL:
  Z-norm-seal/v1 + retained TB4-3/A3
    -> exact epsilon = 1 relative theorem

PER WINDOW:
  Z_{2M}-link is supplied only if inventory(window) = migrated
  and the receipt binds that migration-record digest

CURRENT:
  K5 = Z20-link supplied
  K3 = Z12-link pending
  A5 = Z10-link pending
```

一般の現行 B-6/B-7 が seal と名指しの per-window link の**双方**を要する
こと、TB4-E alternate / link-free proof ID を別行に保つことも正しい。
数学命題と前件集合そのものに新しい破綻は認めない。

---

## F4. blocker A62-1 — \(B_{\rm FC}\) の live status が悉皆同期されていない

申告では旧出現は履歴・自認引用だけとされたが、次は現行判定を述べる
**live 本文**である。

1. §0「判定（先に10行）」第 5 項は、なお
   **「\(Z\) は未凍結」**とする。
2. 同第 6 項は、なお
   **「未凍結の \(Z\)」**を閉じなかった札に数え、TB4 を
   exact \(\varepsilon=1\) の**文献関所**、\(Z_{2M}\)-link を
   **未凍結**の規約関所とする。
3. §12 の文献要請 13 直前も、現行説明として
   **「\(Z\)(未凍結)も同じ向き感受性の関所」**とする。

これらは v2.13 の履歴表ではなく、文書冒頭の総括と現行依存説明である。
少なくとも K5 について `CURRENT: supplied` と `Z: unfreezed` を同時に
正本化できず、GLOBAL の seal-relative theorem と「TB4 は文献関所のまま」
も無限定には併記できない。

したがって「三層型へ悉皆同期」「残存は履歴引用だけ」という apply 前件は
再現しない。修理では §0 と §12 を、

```text
global seal-relative status
per-window inventory status
pre-event candidate state / post-receipt operative state
historical quotation
```

のいずれかへ明示的に型付けし、live grep の全出現に分類を付ける必要がある。

---

## F5. blocker A62-2 — immutable component 内の live 状態欄

component 1 冒頭は

```text
状態: drafted / unapproved / non-operative
```

component 2 冒頭も同じ live 状態を持つ。一方、両 component の末尾は
`immutable candidate blob; operative iff bound by the approved event receipt`
とする。receipt 発行後も byte 不変なら、冒頭の無時制
`non-operative` は post-receipt の外部状態と衝突する。

この欄が「candidate 作成時の snapshot」を意味するなら、例えば

```text
embedded_state_at_candidate_creation = drafted / unapproved / non-operative
live_operative_status_authority       = approved event receipt
```

と時制と authority を明記すればよい。これは自己 SHA 循環とは別の、
immutable artifact に可変 lifecycle state を埋めた型の残りである。

この修文により component 1/2 の hash が変わるため、両実値を final seal
へ再記入して final を再 hash する必要がある。component 2 の `depends_on`
は ID のままでよく、component 1 digest を component 2 に戻してはならない。

---

## F6. Part A 発効裁定

```text
component mathematical content       = PASS
self-digest removal                   = PASS
component-ID / final-digest topology  = PASS
final-seal component binding          = PASS
BFC main three-layer repair           = PASS
BFC live-status exhaustive sync       = FAIL
immutable lifecycle typing            = FAIL

candidate_c_atomic_apply              = NOT ACCEPTED
effect_declaration                    = NOT ISSUED
status_on_apply / applied_at          = MUST REMAIN BLANK
operative_hash                        = NOT MINTED
event_receipt R                       = NOT ISSUED
CLAIMS operative entry                = NOT AUTHORIZED
```

`2a29b764...` は照合済みの **candidate hash** ではあるが、operative seal
hash ではない。上の二 blocker を閉じた新 blob 束について差分再監査を行う
まで、発効処理を進めてはならない。

---

# Part B — \(N_\infty\) stage-2 spec v4

## F7. 数学差分の裁定

### F7.1 valuation identity — 式は PASS、基礎体の型を要修理

有限分離拡大 \(k(C_{\rm crv})/k(x)\) と整数値に正規化した closed-point
valuation に対して、

\[
\operatorname{ord}_P N(g)
 =\sum_{Q\mid P}[\kappa(Q):\kappa(P)]\operatorname{ord}_Q(g)
\]

は正しい。従って

\[
\operatorname{div}(N(g))=\pi_*\operatorname{div}(g)
\]

および \(g=v-\mu\) に対する (60.1)、(60.2) は従う。便 61 F7.1 が求めた
一行の代数的根拠として十分であり、外部文献の節番号を freeze 前件にする
必要はない。

ただし v4 は \(k\) を定義せず、\(v\) の所属も量化していない。係数体
\(\mathbb Q\)、geometric point を取る体、whitelist の prediction field
\(\mathbb Q(\zeta_{20})\) は別の型である。少なくとも

```text
curve coefficient field = Q
geometric working field  = k = Qbar
v belongs to k (and v != 0 where j(v)=C/v is used)
prediction field         = K = Q(zeta_20)
```

相当を設定に置くこと。この一語修理後、`N∞-N` は紙上 PASS とする。

### F7.2 その他の数学核

v3 から statement を変えていない `N∞-1:1` / `N∞-fix` / `N∞-pair` /
`N∞-div` / `N∞-criterion` に新しい数学 blocker はない。

`N∞-swap` を

```text
S5 target -> (60.6) RHS
```

の bridge と呼び、(60.6) の RHS から \(s^2=-C\) を外さない選択も正しい。
RHS \(\Rightarrow\) LHS の依存閉包では `N∞-swap` が冗長であることも
§1.9 が明記しており、循環はない。

---

## F8. blocker B62-1 — D-2 witness の ambient algebra が未型付け

相互 ideal inclusion の表現係数、Bézout/reduction、component bijection、
multiplicity、chart overlap、total coverage、pushforward compatibility まで
要求した方向は正しい。digest/partition/degree 一致だけを equality
certificate として拒否したことも PASS とする。

しかし `curve_base_field_id` / `curve_model_digest` / `chart_ids` だけでは、
§4.2 が使う次を一意に定めない。

- ambient coordinate ring と quotient relations;
- 係数体の具体 presentation と、異なる presentation 間の embedding;
- monomial order;
- reduced Gröbner basis / normal-form の serialization と reduction contract。

reduced Gröbner basis は ring と term order を固定して初めて一意になる。
従って certificate または freeze bundle に、少なくとも

```text
ambient_coordinate_ring_schema_id + digest
coefficient_field_presentation_id  + digest
field_embedding_witness_schema_id  + digest
monomial_order_id                  + digest
groebner_reduction_contract_id      + digest
```

相当を束縛すること。§4.2 の prose に「fixed」と書くだけでは、何を固定した
かが certificate から再検査できない。

また §4.1 の `searcher_native_divisor_ref` / `checker_native_divisor_ref` は
単数だが、§5.2 の各 native は
`ramification_divisor_on_C` と `branch_divisor_on_P1` の二対象を持つ。
各 lane について二 ref と native schema ID/digest を明示するか、両者を
含む typed aggregate artifact であることを schema に固定する必要がある。

---

## F9. blocker B62-2 — G-1〜G-5 は原理 PASS、証跡 schema は不足

次の原理裁定は正しい。

- generator は第三判定 lane でなく、単独 ACCEPT を出さない;
- 欠落・witness 不成立・入力 digest 不一致は fail-closed;
- A/B が同じ witness を独立に再検査する;
- shared canonicalizer/helper を禁止する;
- verifier contract を freeze bundle に束縛する。

しかし現 schema は単数の
`verifier_contract_id + digest` しか持たず、実行 artifact に

```text
verifier_A_id + code_digest + result_digest
verifier_B_id + code_digest + result_digest
generator_id  + code_digest
dependency_manifest_A/B + digest
```

を保存する欄がない。`searcher_id` / `checker_id` だけでは、別実装 verifier
の identity や shared helper 不使用の証跡を含むとは限らない。G-3/G-4 は
設計原理として必要だが、現 schema のままでは receipt 上で検収不能であり、
便 61 F9 への十分な**運用上の**回答にはまだなっていない。

---

## F10. blocker B62-3 — verdict は全域化したが単数 reason は全域化していない

`accepted` の新設、raw precondition 六段、T-1 の
`triple-root-of-a` 優先、E-4 exact PASS 後の
\(\gcd(a,p)\ne1\) を `INTEGRITY_STOP` とする修理は正しい。

しかし固定 priority が書かれているのは precondition 群と T-1 の二分岐
だけである。`INTEGRITY_STOP` 群には全順序がなく、例えば

```text
digest-mismatch + divisor-equality-failure
checker-mismatch + finite-partition-cross-mismatch
```

が同時に成立したとき、単数 `reason_code` は一意に決まらない。従って
§5.3 の「複数同時 failure は固定 priority で単数化」という totality
主張は現 enum からは従わない。

採用案は次とする。

```text
public:
  primary_reason_code = 全 verdict を通した凍結済み全順序で一意化

SEALED_INTERNAL:
  all_reason_codes[] = 同じ全順序で canonical sort した全検出理由
```

public envelope の単純さを保ちつつ、複合 integrity failure の診断情報を
失わない。配列を採らない場合でも、少なくとも全
`INTEGRITY_STOP` codes の priority を明記しなければならない。

また E-6 は §2/§3 で raw decision precondition に数える一方、§5 では
E-4 後の不成立を integrity contradiction とする。後者が正しいので、
E-6 を candidate rejection precondition ではなく
`redundant theorem-consistency assertion` 等へ再分類すると型が明瞭になる。

---

## F11. blocker B62-4 — proof import と freeze bundle は具体的束縛になっていない

### F11.1 v3 digest 参照

`supersedes_v3 = sha256:83c9f588...` は参照先 byte 列を固定する。しかし
digest が固定するのは**どの artifact か**であって、

- v3 のどの節を normative proof body として輸入するか;
- v4 のどの節が v3 を上書きするか;
- 同名 statement が衝突した場合の precedence

までは固定しない。現文は「v3 §1 を参照」「変更した `N∞-N` の証明のみ
差替え」と自然言語で述べるが、`supersedes` と `imports` の合成規則が
freeze bundle にない。

安全な修理は v5 で必要 proof を全文再掲することである。複合 artifact を
採るなら、少なくとも次の import manifest を規範化すること。

```text
normative_dependency_sha256 = 83c9f58887a508d2bbe451a456e41e6ff19f5b2eaa6fdfb957516f6a57aede3b
imported_fragments           = exact section IDs for unchanged proof bodies
excluded_fragment            = v3 N∞-N proof
override                     = v4 N∞-N proof
precedence                    = v4 over imported v3
```

従って、**digest 束縛参照という方式自体は可だが、現在の参照規則だけでは
freeze 自己完結性に不足する**と裁定する。

### F11.2 §6 は field declaration であって実 ID/digest の列挙ではない

B9 の campaign/field 四欄、七補題名、schema 群、`s5_source_map` を
**列として設計した方向**は PASS である。しかし §6 の

```text
lemma_N_inf_N_id + digest
...
reason_code_enum_id + digest
```

は値の placeholder であり、委嘱がいう「7 補題の実 ID+digest 全列挙」には
なっていない。D-2 contract も上の blocker により digest を mint できない。
実値を持たない bundle に一つの freeze ID を発行すると、後から dependency
を差し替えられるので fail-closed でない。

---

## F12. 委嘱 §8 の六問への回答と freeze 裁定

| 問 | 回答 |
|---|---|
| **1. (61.1)** | valuation identity は正しい。\(k\)、\(v\)、valuation normalization を型付けすれば自己完結な一行として採用可。外部文献番号は不要。 |
| **2. D-2 witness** | 表現係数/Bézout/reduction という witness 形は可。しかし `curve_base_field_id` / `chart_ids` だけでは ambient ring と monomial order を固定できず、不足。 |
| **3. G-1〜G-5** | 原理として PASS。二 verifier の実 ID/code digest/result と dependency manifest が schema に無いため、freeze 条項としては不足。 |
| **4. reason 設計** | public は単数 `primary_reason_code`、sealed は canonical `all_reason_codes[]` を採用する。いずれにせよ integrity codes を含む全順序が必要。 |
| **5. `N∞-swap`** | S5 target \(\to\) (60.6) RHS の bridge とする現選択で PASS。 |
| **6. v3 参照** | digest 参照方式は可だが、現 v4 には exact import/override/precedence manifest がなく不足。v5 全文再掲が最も小さく安全。 |

最終状態は次である。

```text
predicate mathematics              = CONDITIONAL PASS
  condition                         = bind k and v explicitly
N∞-swap dependency role            = PASS
D-2 witness direction              = PASS
D-2 frozen ambient algebra         = FAIL
two-verifier frozen evidence        = FAIL
verdict/reason totality             = FAIL
v3 import closure                   = FAIL
concrete dependency ID/digests      = MISSING

predicate_spec_freeze_id            = NOT ISSUED
implementation_status               = NOT AUTHORIZED
model_builder_status                = LOCKED
```

従って F12 様式の freeze ID を形式だけ発行しない。searcher、checker、
D-2 generator、二 verifier のいずれにも実装着手認可を出さない。

---

## F13. 差分再提出の最小条件

### Part A

1. \(B_{\rm FC}\) 新 version で §0・§12 を含む全 live status を
   GLOBAL / PER WINDOW / CURRENT / HISTORY に分類して同期する。
2. component 1/2 の冒頭状態を creation-time snapshot と明記し、live
   authority を receipt へ移す。
3. component 1/2 \(\to\) final seal の順で再 hash し、新 candidate hash
   と全同期 artifact hash を再提示する。

### Part B

1. \(k\)、\(v\)、geometric field と prediction field を分離して型付けする。
2. ambient ring、field presentation/embedding、monomial order、reduction
   contract を D-2 schema に追加する。
3. A/B native の二 divisor ref と schema、generator、二 verifier、
   code/result/dependency digests を sealed receipt に追加する。
4. 全 `INTEGRITY_STOP` を含む reason 全順序を凍結し、E-6 を
   consistency assertion へ再分類する。
5. v3 import manifest を exact 化するか、v5 に proof body を全文再掲する。
6. 七補題、B9 四欄、全 schema/contract の実 ID+digest を充填する。

数学核の再証明は不要である。次便は上記差分と、新たに mint した bundle
の exact digest を主対象にすればよい。

---

## F14. 共同設計者としての発案

### F14.1 theorem freeze と execution freeze を別 ID にする

数学核はほぼ閉じ、残件は実行証明書の型である。従って

```text
ninfty-stage2-theorem/K5/v1
ninfty-stage2-execution-schema/K5/v1
```

を別々に束縛すると、D-2 schema の修文で定理 artifact の digest を
動かさずに済む。ただし Model-Builder の unlock 条件は両 ID の receipt
成立とする。

### F14.2 D-2 を proof-carrying join として一つの record にする

```text
native_A + native_B
  -> equality witness
  -> verifier_A attestation
  -> verifier_B attestation
  -> join receipt
```

を一 record にし、各 arrow の input/output digest を前後で連結する。
generator は witness を作るだけで verdict 欄を持たせない。これにより
「第三 oracle」化を schema で禁止できる。

### F14.3 live-status lint は語の件数でなく身分を出力する

\(B_{\rm FC}\) の再発防止には `未凍結` 等の件数だけでなく、

```text
CURRENT | CONDITIONAL-ON-RECEIPT | HISTORY | SELF-ADMISSION
```

の分類と所在を lint artifact に出すのがよい。未分類の status 語が一つでも
あれば apply を fail-closed にする。

---

## F15. ★教材

1. **正しい hash 連鎖は、payload の意味的一貫性を保証しない。**  
   byte が全一致しても、live status が旧状態なら原子的 apply はできない。

2. **immutable artifact の状態欄には時制が要る。**  
   `non-operative` を byte 不変の本文へ置くなら creation-time snapshot と
   明記し、現在状態は外部 receipt に持たせる。

3. **digest は artifact identity を固定するが import 意味論は固定しない。**  
   fragment、override、precedence を manifest にする必要がある。

4. **Gröbner witness の型は多項式だけではない。**  
   係数体 presentation、ambient ring、term order、normal-form contract
   まで固定して初めて exact に再検査できる。

5. **二独立 verifier は prose でなく receipt の二証跡で示す。**  
   code/dependency/result digest が無ければ shared helper の再導入を
   事後に検収できない。

6. **verdict の全域性と reason の一意性は別問題である。**  
   terminal state が一つでも、同時 failure の priority がなければ単数
   reason は total function にならない。

---

## F16. 監査範囲外申告

### 本便で行ったこと

- 便 62 委嘱、対話帳 T-17 まで、便 61 返信、対象 artifacts の読解;
- target commit / HEAD / worktree の対象 blob 同一性、SHA-256、LF 行数、
  CR/TAB/C0 の照合;
- candidate C の外部 digest 連鎖、\(B_{\rm FC}\) live status、component
  lifecycle の紙上監査;
- spec v4 の norm typing、D-2 schema、lane independence、reason totality、
  dependency closure、freeze bundle の紙上監査。

### 本便で行っていないこと

- `status_on_apply` / `applied_at` の記入、operative hash、receipt R、
  CLAIMS 記帳;
- Model-Builder、searcher/checker、D-2 generator、verifier の実行または実装;
- sealed candidate 値、whitelist hit、旧 8 hit、negative/EP fixture の観測;
- GAP、大量探索、Lean 証明書の作成。

従って数学層の札は **paper-audited** であり、Lean の意味での
`verified` ではない。過去返信ファイルおよび指定外 artifact は変更していない。
