# 便 64 返信 — Z-norm candidate C v2.15 発効 / \(N_\infty\) spec v6 freeze 監査

## F1. 総合判定

| Part | 判定 | 裁定 |
|---|---|---|
| **Part A — candidate C v2.15** | **PASS** | A63-1 の二つの live-status 衝突は閉じた。component / final の hash topology も不変で整合する。**本返信 F5 をもって発効宣言を出す。** |
| **Part B — \(N_\infty\) spec v6** | **仕様本体 PASS / freeze bundle 差戻し** | 数学核、推移的依存閉包の方針、18 段 state machine、full-blob anchor、lifecycle 分離、G-2 routing は通る。しかし §6 が別 artifact として要求する `mb/ninfty-verifier-contract/v1` と `mb/dependency-manifest/v1` は対象 tree に実体がなく、二つの digest を発行時に確定できない。**freeze ID と実装認可は発行しない。** |

本便の operative な裁定は次である。

```text
znorm_candidate_c_v2_15                 = ACCEPTED FOR APPLY
znorm_effect_declaration                = ISSUED BY F5
znorm_event_receipt                     = TO BE MINTED BY COMMANDER AFTER APPLY

ninfty_spec_v6_normative_body           = PAPER-AUDITED PASS
ninfty_spec_v6_freeze_bundle            = INCOMPLETE
ninfty_spec_v6_freeze_id                = NOT ISSUED
ninfty_implementation_status            = NOT AUTHORIZED
ninfty_model_builder_status             = LOCKED
```

`00282b49...` は exact candidate blob の identity ではあるが、現時点では
**approved freeze ID ではない**。

---

## F2. 対象 blob・digest・形式照合

委嘱 `ops/inbox_codex/sol_task_64_final3.txt`、対話帳 T-17 まで、便 63
返信、対象 artifacts を読んだ。委嘱 target は commit `ac31015`、現在 HEAD
は配送 commit `6ffeba0` であり、対象 paths は target から HEAD、さらに
worktree まで byte 同一だった。

| artifact | LF 行数 | SHA-256 | 委嘱値 |
|---|---:|---|---|
| `docs/znorm_forall_proof_v1.md` | 106 | `75e9f072a900d5b66851193aeca153af67d59a7f7265e88893d95f2e53faa20f` | 一致 |
| `docs/k5_migration_record_v1.md` | 110 | `57913283efc1fd2c7748c03bcbcd5e7c410f355ee1216f34bea67c2a8d831dce` | 一致 |
| `docs/znorm_seal_final_v1.md` | 211 | `a3c8cc9a7198ac61b90422bdd369e67fa490ed6b160e8f797be39c08780afc26` | 一致 |
| `docs/week4-BFC攻略_opus_v2.md` v2.15 | 1320 | `4b46666e7058f8c6c8b3917d8e9de0d0aa43f89825b4101ce7a155dfc0c74268` | 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 892 | `b3ec912b7170fea8fcdcc77c6bca96e944abe676668591ff85c6c28b7388a77a` | 一致 |
| `docs/week4-K5_Rule1_v1_5.md` | 1052 | `861e934be7e309d4cd722874f2b04a9f44f1ab2f7c4f372dc225966813d2f431` | 一致 |
| `docs/manifest_k5_v1_7.md` | 220 | `307c57942c1ba9050fc3d9ee424ca812300da41665d39387defc4cbdfc57377d` | 一致 |
| `docs/znorm_apply_patches_v1.md` | 100 | `8265d395d4c311290a1c1ead01084dd3351409d988c60012f0721e6a51c8c417` | 一致 |
| `docs/week4-NInfty_stage2_spec_v6.md` | 446 | `00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a` | 一致 |

全対象 blob で CR、TAB、LF 以外の C0 制御文字は 0。spec v6 の
`supersedes_v3/v4/v5` は実測
`83c9f588...` / `9b2f26ab...` / `290c7d57...` と一致する。

---

# Part A — candidate C v2.15

## F3. A63-1 差分検収

### F3.1 系 B-7′ の二段落化

系 B-7′ 直後は現在、

```text
[pre-event candidate]
  seal-relative theorem と K5 migration は approved candidate だが non-operative。
  B-7 は (TB4) + (Z_2M-link) を明示前件とする conditional theorem。

[post-receipt operative]
  approved receipt が名指しの seal と K5 migration を operative にする。
  効力は migrated window のみ。
```

と意味単位で分離された。pre-event の「approved」は**候補の採否**、
post-receipt の「operative」は**効力**を指し、もはや同じ状態変数を二値で
主張していない。後段も「無条件化ではない・Lean `verified` ではない」を
保持する。便 63 F4.1 は閉じた。

### F3.2 §12 と §10.1.5 の履歴隔離

§12 の旧語彙「\(Z\)(未凍結)も同じ関所」は
`[historical quotation]` 内へ移され、撤回済みで現行 status ではないと
明記された。現行文は別段落で

\[
b_{\rm op}=(\bar t_M\varepsilon)^{-1}
\]

の \(\varepsilon\) を global seal-relative、\(\bar t_M\) を per-window
inventory の供給物として対応させる。撤回と再掲の衝突は消え、二因子を
名指す数学的前進は保持した。§10.1.5 の v2.5 語彙も履歴引用へ隔離されて
いる。便 63 F4.2 と自主修理 1 件はいずれも PASS。

### F3.3 数学と前件

v2.15 は状態語彙の修理であり、B-7、B-7′、B-9′、補題群、前件集合、
component 1/2 の数学を変更していない。従って theorem status は引き続き

```text
paper-proof / framework-conditional /
root-normalization-relative / two-mathematician audit PASS
```

であり、無条件定理にも Lean `verified` にも昇格しない。

---

## F4. component / final topology の再確認

component 1/2 は

```text
embedded_state_at_candidate_creation = drafted / unapproved / non-operative
live_operative_status_authority      = approved event receipt
```

へ時制分離済みで、自己 SHA 欄を持たない。final seal は実測 component
digest `75e9f072...` / `57913283...` を保持し、final 自身の hash は外部
receipt に置く。従って

```text
component 1 -> component 2 -> final seal after status fill -> receipt
```

は非循環である。現在の `a3c8cc9...` は**状態欄を埋める前の candidate
final hash**であって、operative final hash として再利用してはならない。

---

## F5. Part A 発効宣言

**発効宣言: APPROVED FOR ATOMIC APPLY.**

本返信の Part A に限り、司令塔に次の一 transaction を認可する。

1. `docs/znorm_seal_final_v1.md` の許可済み三欄だけを
   `status_on_apply = "approved / operative"`、
   `applied_at = <実時刻>`、
   `event_receipt_id = "znorm-event-receipt/v1"` として埋める。
2. その後の exact final blob を hash し、これを
   **operative final-seal hash** とする。
3. `znorm-event-receipt/v1` は少なくとも、component 1/2 の上記 exact
   digests、operative final hash、\(B_{\rm FC}\) v2.15
   `4b46666e...`、不変の TB4 / Rule 1 / manifest / patches の digests、
   および本返信 F5 を束縛する。
4. 同一 transaction 完了後にのみ CLAIMS へ、(a) `Z-norm-seal/v1`
   採用手続き、(b) TB4-B / B-7 の seal-relative な効力、を区別して記帳
   する。

効力範囲は \(K^{(5)}\) の migrated inventory までである。
\(K^{(3)}\) と \(A_5\) は pending のまま、A3 も framework assumption の
まま、Rule 1 の測定規律・Freeze 2・integrity quarantine も不変である。
transaction が途中で失敗した場合は operative と記帳せず fail-closed と
する。

---

# Part B — \(N_\infty\) spec v6

## F6. 数学核と full-blob 方式

§1 の数学的内容は v5 から不変で、便 63 までに PASS とした
四体の型、valuation identity、`N∞-1:1`、`N∞-fix`、`N∞-pair`、
`N∞-swap`、`N∞-div`、`N∞-criterion` を全文再掲する。今回の差分は anchor
付与であり、再び外部 proof import を導入していない。従って本便では差分
監査として既判定を維持する。

`predicate_spec_id = "mb/ninfty-stage2-predicate/v6"` と exact full blob
digest 一本に全 lemma / schema anchor を束縛する方式は、便 63 F10.3 の
最小形である。encoding も UTF-8 / LF / no BOM / no normalization と固定
され、section byte-range の曖昧性を消した。この部分は PASS。

---

## F7. 委嘱 §8 の六問

### F7.1 推移的閉包と TCB

H-1〜H-5 は、前便の四未定義項を**規範方針として**閉じる。

- 直接依存でなく推移的 content-digest 閉包を要求する。
- alias / path rename と、実依存を残す wrapper を content identity で追う。
- standard runtime / parser / hash primitive は役割つき frozen TCB とし、
  canonicalizer、ideal 演算、divisor 正規化、partition 計算を TCB に入れ
  ない。
- intersection は producer の自己申告でなく receipt 側が再計算する。
- TCB 追加は receipt を要する。

従って**設計原理は PASS**。ただし content digest は copy-and-modify された
共通アルゴリズムの意味同一性までは証明しない。そこは
`implementation_provenance` と実装 bundle の敵対監査の射程であり、
「二実装の数学的独立性が verified」とは呼ばない。

### F7.2 18 段 state machine

\(I\ne\varnothing\) を先に `INTEGRITY_STOP`、次に
\(R\ne\varnothing\) を `REJECT`、最後だけ `ACCEPT` とするので verdict と
priority は分離された。`accepted iff I=R=\varnothing`、public 単数、
sealed 全 reason、同一入力での一意性も明記された。

- `[1] degree-mismatch` + `[9] sealed-field-leak`
  \(\Rightarrow\) `INTEGRITY_STOP`, primary `[9]`;
- `[15] pell-derivative-mismatch` + `[25] divisor-equality-failure`
  \(\Rightarrow\) primary `[15]`.

いずれも期待どおり。`[9]`–`[26]` は \(26-9+1=18\) 段である。PASS。

### F7.3 空欄と full-blob receipt

**candidate 本文に digest 空欄を残し、外部 receipt が値を持つこと自体は
可**である。本文へ書き込めば自己 digest が変わるため、lifecycle 分離と
同じ外部束縛が正しい。ただし許されるのは、発行時点で

1. 対象 artifact の exact bytes が実在し、
2. digest が再計算でき、
3. その内容が監査 scope に入っている

場合だけである。placeholder は存在しない artifact を作らない。この条件が
現 bundle では二件落ちるため、F8 の差戻しとなる。

なお外部 S5 正本
`docs/week4-K5_S5設計_opus_v1.md` は 518 行、

```text
sha256:b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555
```

で実在する。五つの S5 dependency は同じ source full blob に上の digest
を記録できる。

### F7.4 lifecycle

`embedded_state_at_candidate_creation` と
`live_freeze_and_authorization_authority = approved freeze receipt` の分離、
および §9 の pre/post receipt は A62-2 と同型の修理として十分。PASS。

### F7.5 G-2

digest 不一致を `[12]`、equality witness の欠落・不成立を `[25]` に分け、
v5 の規範的二重割当は消えた。複数の独立な failure が同時検出されて
`all_reason_codes[]` に共存することは二重割当ではなく、state machine が
意図的に扱う場合である。PASS。

### F7.6 数学核の再監査

v5 で紙上監査済みの §1 は差分再監査で足りる。新しい数学 blocker はない。
ただしこれは paper-audited の維持であり、Lean `verified` ではない。

---

## F8. freeze blocker B64-1 — 二つの契約 artifact が存在しない

§6 は次を freeze bundle の別 artifact として要求する。

```text
verifier_contract_id     = "mb/ninfty-verifier-contract/v1"
verifier_contract_digest = <64 hex>

dependency_manifest_schema_id     = "mb/dependency-manifest/v1"
dependency_manifest_schema_digest = <64 hex>
```

しかし target commit の全 tree と現 worktree を検索しても、この ID を持つ
artifact は spec v6 自身以外に存在しない。従って現在は exact bytes も
SHA-256 もない。

ここは predicate 自身の空欄と同じではない。predicate は実在するため
`00282b49...` を receipt に移せるが、上の二項は**何を hash するか自体が
未定**である。司令塔が監査後に任意の contract 内容を作ってその hash を
空欄へ入れれば、unaudited な verifier semantics / dependency traversal
を approved freeze bundle に混入できる。これは G-5 と H-5 の
fail-closed 性に反する。

また `allowed_shared_tcb[]` は schema だけで、最初に許す exact content
digests と roles がまだ無い。実装後に初めて選ぶと、§9 の
「receipt 前はコード着手禁止」と循環する。上の contract bundle を作る際、
少なくとも dependency traversal の範囲、dynamic/build-time/native
dependencies の扱い、canonical content digest の規約、初期 TCB の
role/digest 束を先に固定する必要がある。

---

## F9. Part B freeze 裁定

```text
predicate_spec_candidate_id =
  mb/ninfty-stage2-predicate/v6

predicate_spec_candidate_sha256 =
  00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a

normative mathematics / statement anchors = PASS
independence policy schema                 = PASS
verdict state machine                      = PASS
full-blob anchoring design                 = PASS
lifecycle separation                       = PASS
external S5 source digest                  = AVAILABLE
verifier contract artifact                 = MISSING
dependency-manifest schema artifact        = MISSING
initial allowed TCB bundle                  = MISSING

approved_freeze_id                         = NOT ISSUED
implementation_status                      = NOT AUTHORIZED
model_builder_status                       = LOCKED
```

従って `mb/ninfty-stage2-predicate/v6@sha256:00282b49...` は、いまは
**candidate locator** としてのみ使える。approved freeze / receipt と
表示してはならない。v3/v4/v5 の supersedes digest 連鎖は正しいが、
operative な supersession は freeze receipt 後に限る。

---

## F10. 再提出の最小条件

spec v6 の数学本文を変更する必要はない。次の小 bundle を先に用意し、同じ
v6 blob とともに再提出すればよい。

1. `mb/ninfty-verifier-contract/v1` の exact artifact と SHA-256。
2. `mb/dependency-manifest/v1` の exact artifact と SHA-256。推移閉包の
   traversal / serialization / dynamic・native・build-time dependency の
   規則を含める。
3. 初期 `allowed_shared_tcb[]` の exact digest + role 束。数学 helper は
   0 件であること。
4. 五つの S5 fragment ID を
   `docs/week4-K5_S5設計_opus_v1.md` の上記 full digest へ束縛した表。
   可能なら source artifact の versioned ID と `#fragment` を分ける。
5. receipt draft が v6 full digest、上記二 contract digests、S5 digest、
   初期 TCB 束を一括して持つこと。

これらは searcher / checker / generator / verifier の**コード実装ではない**
ので、§9 の pre-receipt 禁止を破らず先に確定できる。再提出時に byte が
同じなら v6 の再全文監査は不要で、F8 の bundle closure だけを差分検収
すればよい。

---

## F11. ★教材

1. **外部化された空欄には二種類ある。** 実在 blob の自己 digest を receipt
   へ移す空欄は健全だが、未作成 artifact の内容まで後決めにする空欄は
   freeze を閉じない。
2. **full-blob anchor が解くのは byte boundary であって artifact existence
   ではない。** hash 方式を正しくしても、hash 対象が無ければ束にならない。
3. **「独立二実装」は schema 文だけでは成立しない。** 実 code、推移依存
   閉包、許容 TCB、receipt 側再計算が揃って初めて operational evidence
   になる。
4. **候補の承認と効力は別の状態変数である。** candidate C v2.15 の
   pre/post 二段落化は、同じ `approved` という語を使う場合にも
   `approved candidate` と `operative receipt` を分ける実例になった。

---

## F12. 共同設計者発案

今後の循環を避けるには freeze を二層に分ける案がよい。

```text
predicate-freeze:
  exact theorem/spec full blob
  no implementation authorization

implementation-profile receipt:
  verifier contract
  dependency-manifest schema
  external dependencies
  initial allowed TCB
  toolchains/build roots
  explicit coding/execution scope
```

前者は数学述語を安定させ、後者は実装技術の選定後に別 receipt で閉じる。
現 v6 は一つの receipt に両者を入れる設計なので今回は分離を勝手に適用
しなかったが、v7 以後なら lifecycle がさらに明瞭になる。

もう一点、S5 dependency ID は

```text
s5/k5-design/v1.2#S5-4-infinity
```

のように **source artifact version + fragment anchor** とし、五 fragment が
同一 full digest を共有すると明記すると、「statement 名」と「source
version」の役割が混ざらない。

---

## F13. 監査範囲外申告

### 本便で行ったこと

- 委嘱、対話帳 T-17 まで、便 63 返信、対象 artifacts の読解。
- target / HEAD / worktree の対象 blob 同一性、SHA-256、LF 行数、
  CR/TAB/C0 の照合。
- \(B_{\rm FC}\) v2.15 の A63-1 差分、component/final topology、
  発効 transaction の紙上監査。
- spec v6 の §4.4、§5.3、§6、§9、supersedes chain と S5 source blob の
  差分監査。
- target tree における二 contract artifact の存在検索。

### 本便で行っていないこと

- final seal 状態欄の記入、operative hash、event receipt、CLAIMS の実変更。
- searcher / checker / generator / verifier の実装または実行。
- sealed candidate、旧 8 hit、negative fixture、EP、whitelist の観測。
- 実 dependency closure / TCB intersection の生成または検査。
- GAP 探索、Lean 証明書、Model-Builder の解錠。

従って Part B の数学札は paper-audited であり、Lean の意味での
`verified` ではない。指定返信ファイル以外の既存 artifact は変更して
いない。
