# 総合判定: **差戻し**

**(β) 版イベントの発火は許可しない。** Rule 1 v1.4 / manifest v1.6 の作成、札更新、文献要請 13(ii) の移管、B-9′(e′) の全称復帰を、この提出から開始してはならない。

便 51 で指摘した数学核の主要修理はかなり閉じた。とくに B-9′(a) の正形、B-6tw/B-7tw の現行 proof、TB4 の核検査、最終 GAP certificate の束縛は再現できる。しかし、版イベントが要求する **normative 本文・version identity・CLAIMS・lint の同時 finality** は閉じていない。委嘱と裁定 62 が「同期済み」と報告する CLAIMS W3-17 は、対象 commit の現物では旧版のままである。また amendment の event source に、exact 回収を再び「(TB4) だけ」と読ませる live 条文が残る。

| 束 | 判定 |
|---|---|
| 1. BFC v2.9 | **数学核の指定修理 PASS / live status・typed residual により FAIL** |
| 2. amendment v6 | **A16/A17 の中心修理 PASS / exact route の live 条文・schema totality が FAIL** |
| 3. TB4 v2.4 + checker | **数学核・37/37 PASS / artifact の version identity が FAIL** |
| 4. provenance / lint / F8.3 | **certificate 束縛 PASS / CLAIMS 同期と preflight gate が FAIL** |

---

## F1. 監査 anchor・digest・再走

便 52 の発送 commit は `0f7e1ab46fc3374f2fab95228056dac614896628`。監査時の `HEAD` は後続の `484a46c50de7f12a5c92053af5fedd9c6b4a4450` まで進んでいたが、両 commit 間で本便の対象 artifact に差分はない。したがって digest で指定された `0f7e1ab` を判定対象に固定した。

作業ツリーの `provenance/CLAIMS.md` には本便外の未 commit 変更があったため、CLAIMS の判定は `git show 0f7e1ab:provenance/CLAIMS.md` に対して行った。その未 commit 変更も W3-17 の `v2.8` を `v2.9` に変えただけで、後述する `v2.3 / 34/34` は残しているので、本判定を救わない。

| artifact | LF / logical lines | SHA-256 | 判定 |
|---|---:|---|---|
| `docs/week4-BFC攻略_opus_v2.md` | 1181 / 1181 | `9cd1e01c1f273f830a18628d70ca673d9fb9e92f4f9bdf08c950fb624afdc607` | 一致 |
| `docs/amendment_5prime_draft.md` | 327 / 327 | `3b8d7695546e4ca47d4f4adfe1f91e4ad259498661fa0d954a9b639d2724fee1` | 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 852 / 852 | `6e6656f9fd433d1806e751376f8d39e9d47b549f4eaba4f1be6cf45170b217d2` | 一致 |
| `search/tb4-monodromy-check.mjs` | 249 / 249 | `6847a76bf5683048bf53531b541cdbc7942645c83207787afb5d1bb2fd454cbd` | 一致 |
| `certificates/bfc/bfc-antecedents.json` | **0 / 1** | `24e67a0a99d8cc75472897b7d7a190e7fb3551bcef3a918c13acfc66dac2afc8` | digest 一致 |
| `search/version-event-preflight-lint.mjs` | 76 / 76 | `95ebc9b6af56814c5b77a291ca23480fc97d3bf047919ddf2a0268233a86a61c` | 一致 |
| `search/preflight-triage.json` | 201 / 202 | `2ea9b2faad7e3e3b59324ea149cd3cca52480bdf2c934c4901b0119ea2c5a8ed` | 一致 |

certificate は末尾 LF を持たない 1 JSON record なので、POSIX `wc -l` なら **0** である。委嘱表の「wc -l = 1」は logical line 数としては正しいが、`wc -l 準拠` という注記とは一致しない。数学判定には影響しないが、再現 metadata は `LF count` と `logical record count` を分けるべきである。

`0f7e1ab` の一時 snapshot で再走した結果:

1. `node search/week4-bfc-antecedents.mjs` — **13/13 PASS**。
2. `node search/tb4-monodromy-check.mjs` — **37/37 PASS**。
3. `node search/version-event-preflight-lint.mjs` — **CLEAN(open 0 / triaged 24)**。
4. BFC certificate — `pass_count=25`, `fail_count=0`, `fail_closed=true`。
5. certificate の BFC input、GAP script、Node counterpart の三 SHA-256 は各現物と一致。

したがって「CLEAN という出力が出た」「certificate が最終 BFC digest に束縛された」こと自体は再現する。問題は、CLEAN が下記の実在する不一致を検出しないことである。

---

## F2. 束 1 — BFC v2.9

### F2.1 指定された数学修理: **PASS**

次を紙上で再確認した。

1. B-9′(a) は
   \[
   b_{{\rm op},{\rm sq}}=b_{{\rm op},{\rm ns}}
   =(\bar t_M\varepsilon)^{-1}\pmod M
   \]
   へ直り、証明は \(\varepsilon\)、\(\bar t_M\)、合成の三段に分かれた。
2. \(M=10,t_{20}=3,\bar t_{10}=3,\varepsilon=7\) で
   \(b_{\rm cmp}=3\ne b_{\rm op}=1\) となる便 51 の反例を正しく採録している。
3. \(Z_{2M}\)-link 下でだけ \(\bar t_M=1\) として
   \(b_{\rm op}=b_{\rm cmp}=\varepsilon^{-1}\) へ特殊化している。
4. B-6tw 冒頭の scope は B-6tw の証明、B-7tw の statement/proof、付録 B の二行までを明示的に覆い、現行 proof の依存欄に link を残した。
5. level \(M\) の指数は \(\bar t_M^{-1}\) と型付けされ、診断先にも link が入った。
6. §13.1 は current/link proof と未提示の link-free proof を別 proof ID に分けた。

B-9′(b)–(e) が使うのは共通 unit の消去だけなので、(a) の値を \(\varepsilon^{-1}\) から \((\bar t_M\varepsilon)^{-1}\) へ直しても骨格が保たれる、という主張も正しい。

### F2.2 live residual 1 — 冒頭 boxed status

30 行の boxed status は今も

```text
paper-proof (framework-conditional on TB1--TB4) / two-mathematician audit PASS
```

であり、\((Z_{2M}\)-link) と `現行 proof ID` を落としている。これは `RETRACTED` / `history` block に入っておらず、文書冒頭の「状態札」として表示される。665・1046 行等の current status と矛盾する。

履歴として残すなら block 型を明記し、current status への pointer にする必要がある。現状のまま「状態札 3 箇所を統一」「live status copy は残差 0」とは言えない。

### F2.3 live residual 2 — B-9′ の source equation と裸の \(b\)

709・712 行は operational な \(b_{\rm op}\) を **「(2.1) で事前固定」**とする。しかし (2.1) が定めるのは \(\varepsilon\) で、\(b_{\rm op}\) の定義式は **(2.1′)** である。補題本体 714 行と付録 B 1180 行は正しいため数学核は読めるが、theorem provenance の参照先が不一致である。

さらに付録 A 1151 行は「無注記の単一文字 \(b\) は使わない」と宣言する一方、1159 行は

\[
(TB4)\iff\varepsilon=1\Longrightarrow b=1,\qquad
b=1\iff\varepsilon\equiv1\pmod M
\]

と裸の \(b\) を live に使う。これを \(b_{\rm cmp}\) と読めば式は正しいが typed-symbol 規律違反、\(b_{\rm op}\) と読めば link なしには偽である。ここは明示的に \(b_{\rm cmp}\) と型付けすべきである。

### F2.4 表示 residual

§13.1 の 963 行、link-free proof ID の行だけ先頭の `>` が落ちている。Markdown 上は前後の blockquote table から外れ、「二 proof ID を一表で分離した」という修理が render 後に壊れる。数学的 blocker ではないが、版イベント artifact としては同時修理が安い。

### F2.5 射程の精密化

B-9′ が必要とするのは、固定した \(K^{(5)}\), \(M=10\) と共通 Rule 1 root object の下での **二 detector 非依存性**である。734–735 行の証明はそれを与える。一方「\(t_{2M}\) は窓にも依らない」は、異なる \(M\) では所属する unit 群自体が変わるので過大に読める。結論を動かさず、

> 同じ \(M\)・同じ Rule 1 root object を共有する二 detector に依らない

へ射程を絞るのが安全である。

以上により、指定された中心修理は PASS だが、束 1 全体は **FAIL**。

---

## F3. 束 2 — amendment v6

### F3.1 A16/A17 の中心修理: **PASS**

次は正しく入った。

- `/exact/v1` の回収を
  `R-a/current-bfc-proof = (TB4)+(Z_{2M}-link)` と
  `R-b/tb4e-alternate = (E-i)–(E-iv)+別 proof ID`
  に分離。
- 本 campaign は R-a を採ると明記。
- `exact_recovery_path` の二値 enum。
- §6 の適用手順を v2 から **v6** へ更新。

### F3.2 live Rule 1 条文が旧 route に戻る: **FAIL**

120–121 行の Rule 1 v1.4 差し替え本文は、今も

> exact (5′) は \(b_i=1\) の特殊化であり、**(TB4) の下で回収される**

と書く。これは同じ文書の 180–183・211 行が確定した二 route と矛盾する。

- 現行 BFC proof なら **(TB4)+link**。
- link-free alternate なら **(E-i)–(E-iv)+別 proof ID**。

イベントが実際に Rule 1 へ転記するのはこの normative 差し替え本文なので、§3 の説明だけ直っていても足りない。121 行にも route を一意に転記しなければならない。

### F3.3 \(b_{\rm op}\) の説明に v2.8 型が残る

140 行は \(b_{\rm sq}=b_{\rm ns}\) の理由を

> 同じ枠組み単位 \(\varepsilon\) の mod 10 還元

とする。v2.9 の正しい理由は、共通の \(\varepsilon\) **と** \(\bar t_{10}\) から
\[
b_{\rm op}=(\bar t_{10}\varepsilon)^{-1}
\]
が共通になること。その結論は B-9′ の引用により正しいが、括弧内の説明は便 51 で落とした再融合を amendment 側に残している。

### F3.4 `exact_recovery_path` の applicability が未定義

§4 の result schema は `exact_recovery_path` を全 record の通常欄として一行追加しただけで、`antecedent_bundle_id` との presence condition を定めない。これには二つの不適切な読みが残る。

1. 全 record で必須なら、`.../twisted/v1` と falsifier record に、使っていない exact route を虚偽記入させる。
2. 任意なら、`.../exact/v1` record が route なしでも通る。

fail-closed な正形は少なくとも

```text
antecedent_bundle_id == THEOREM-ANTECEDENT-Rcyc/exact/v1
  => exact_recovery_path is required and is exactly one of {R-a, R-b}

antecedent_bundle_id != THEOREM-ANTECEDENT-Rcyc/exact/v1
  => exact_recovery_path is prohibited
```

である。R-a なら TB4/link evidence、R-b なら E-i–E-iv と alternate proof ID/digest も同じ branch に束縛すべきである。

よって bundle 2 は **FAIL**。

---

## F4. 束 3 — TB4 v2.4 と 37/37 checker

### F4.1 数学核・checker: **PASS**

次を再走・紙上確認した。

1. TB4-A20 の三 status は「便 50 F2.1 型修理後 PASS・two-mathematician audit 前・Lean verified ではない」へ同期。
2. checker path は tracked な `search/tb4-monodromy-check.mjs`。
3. count は **37/37**。
4. K3:
   \[
   \ker((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times)=\{1,7\}
   \]
   を units 全列挙で集合一致。
5. K5:
   \[
   \ker((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times)=\{1,11\}
   \]
   と \(t_{20}=11\) の非自明性を同様に検査。
6. full tuple `NF-root-link/K5=(10,11,1,11,1,1,false)`、四段のはしご、finite/profinite suite の射程注記も維持。

37/37 を「regression lint であって網羅証明ではない」と限定している点も正しい。

### F4.2 artifact 自身は v2.4 を名乗っていない: **FAIL**

ところが正本の 1 行目は

```text
# ... v2.3(便 50 束 3 ...)
```

のまま、3 行目の版履歴も v2.3 までで止まる。61 行以下には `v2.3 → v2.4` 差分があるが、canonical title / metadata は v2.3 である。

外部の委嘱表・commit message・CLAIMS が v2.4 と呼んでも、artifact 自身の version identity は更新されない。版イベントでは「どの版を読んだか」を一意にする必要があるため、これは単なる見栄えではなく finality blocker である。title と冒頭版履歴を v2.4 へ同期し、その後の digest を正本にし直す必要がある。

したがって bundle 3 は **数学核 PASS / artifact finalization FAIL**。

---

## F5. 束 4 — provenance / lint / F8.3

### F5.1 BFC certificate: **PASS**

最終 BFC digest `9cd1e01c…`、GAP script digest `104e748b…`、Node counterpart digest `f7429890…` は certificate と一致し、25/25・fail-closed も記録されている。司令塔の一 token 修正後の BFC digestへ再束縛されているので、この部分は PASS。

### F5.2 CLAIMS W3-17: **申告と現物が不一致**

対象 commit の W3-17 は、冒頭 antecedent に \((Z_{2M}\)-link) が追加された点だけは正しい。しかし同じ行に次が残る。

- TB4 自前導出 **v2.3**。
- checker **34/34**。
- 「便 51 で最終検収中」。
- BFC **v2.8**。
- 末尾は `artifact 残差 0`。

便 52 と裁定 62 が申告する `v2.9 / v2.4 / 37/37` ではない。commit `bb8c85e` の CLAIMS 差分も、実際には冒頭へ link を一つ加えただけである。したがって「CLAIMS W3-17 の版参照を同期済み」は事実に反する。

### F5.3 CLAIMS W3-18 も B-9′ v2.9 に未同期

W3-18 は今も

```text
(a) b_sq = b_ns
...
(2.1) 事前固定 b
```

とする。v2.9 の正形
\[
b_{{\rm op},{\rm sq}}=b_{{\rm op},{\rm ns}}
=(\bar t_M\varepsilon)^{-1},\qquad \text{source }(2.1')
\]
へ同期していない。B-9′(e′) を event payload に含める以上、W3-17 だけでなく theorem claim 本体の W3-18 も同時更新が必要である。

### F5.4 lint CLEAN は再現するが、closure certificate ではない

exact target snapshot で `CLEAN(open 0 / triaged 24)` は再現した。しかし、同じ snapshot に F2–F5.3 の live 不一致がある。

原因は明確である。

1. CLAIMS を「走査対象に追加」しただけで、期待 version `v2.9 / v2.4 / 37/37` を検査する rule がない。そのため W3-17 は **0 hit**。
2. `naked-b` regex は限定された指数形だけで、BFC 1159 行の裸の \(b\) と amendment 140 行の再融合説明を検出しない。
3. TB4 title が v2.3 のままでも、期待 artifact version を照合する rule がない。
4. triage validator は `disposition` が非空かだけを見ており、`reviewer` の非空、closed disposition enum、record 内の `file/token/text` と key の整合を強制しない。現提出では reviewer は全件記入されているが、**コード上の fail-closed 性**は申告より弱い。
5. 676 行の triage disposition は「B-9′ の scope」と説明するが、実際は系 B-8 の証明である。幸い 673 行が局所的に \(b\in(\mathbb Z/M)^\times\) を宣言するので数学的使用は正当だが、triage 理由そのものは誤っている。

一方、司令塔修正前の 154 行に対応する古い hash record が current hit に適用されなくなった点は、line-hash invalidation が働く正例である。ただし orphan record を報告しないため、record 総数 25 と active triage 24 の差は黙ったままである。

したがって F8.3 は

```text
本文 digest → certificate
```

までは通るが、

```text
CLAIMS を current version へ同期 → lint がその同期を保証
```

で止まる。bundle 4 は **FAIL**。

---

## F6. 司令塔修正権 1 件の検分

司令塔修正そのものは **PASS**。対象現物では旧「\(t\varepsilon\)」が

\[
t_{2M}\ (\text{ゆえ }\bar t_M),\quad \varepsilon,\quad
\bar t_M\varepsilon,\quad
b_{{\rm op},{\rm sq}}=b_{{\rm op},{\rm ns}}
\]

へ型付けされ、B-9′(a) の確定正形を機械的に転記している。新しい数学判断は持ち込んでいない。

ただし便 52 の「703 行」は最終 artifact の物理行番号ではなく、現物では 154 行である。703 行は別の (6′-ii) 式になっている。これは修正内容を損なわないが、今後の開示は物理行番号でなく section anchor + normalized line hash を使う方がよい。

---

## F7. (β) 版イベント判定と最小再提出

**不許可。**

設計として維持してよいもの:

- old canonical version を上書きせず Rule 1 v1.4 / manifest v1.6 を新設する。
- typed \(b\) semantics、root/A3 seals、versioned antecedent bundle。
- operative predicate を (5′\(_b\)) とし、exact (5′) の名前を上書きしない。
- 文献要請 13(ii) を A3 の向き確認へ縮小する。
- 適用後に別便で差分 gate を行う。

発火前の最小修理:

1. **BFC**
   - 30 行の status を current proof ID + link へ更新、または typed history block 化。
   - B-9′ status/statement の `(2.1)` を `(2.1′)` へ。
   - 1159 行を \(b_{\rm cmp}\) と型付け。
   - 963 行の blockquote table を修復。
   - 二 detector 共通性と「全窓非依存」を区別。
2. **amendment**
   - 121 行の normative Rule 1 条文にも R-a/R-b を転記。
   - 140 行を \((\bar t_M\varepsilon)^{-1}\) の共通性へ修正。
   - `exact_recovery_path` の conditional presence と、選んだ branch の evidence/proof-ID 束縛を明記。
3. **TB4**
   - title と冒頭版履歴を v2.4 へ。
4. **CLAIMS**
   - W3-17 を BFC v2.9 / TB4 v2.4 / 37/37 / 現在の裁定へ同期。
   - W3-18 を typed \(b_{\rm op}\) と (2.1′) へ同期。
   - 修理完了前は `artifact 残差 0` を置かない。
5. **preflight**
   - artifact version と CLAIMS の期待値を manifest から equality check。
   - typed \(b\) の live 残差を検出。
   - reviewer・closed disposition・orphan triage を fail-closed にする。
6. BFC 本文が変わるので digest を取り直し、GAP certificate を再束縛する。その後 **CLAIMS → lint** の順で再実行し、結果 receipt を再提出する。

本判定は既存 Freeze 1 / 既存 Model-Builder 許可を撤回しない。禁止するのは、この未閉鎖 artifact 群からの **新版 predicate に基づく (β) event** だけである。

---

## F8. ★教材

1. **「CLAIMS を scan した」と「CLAIMS が同期した」は別である。** 期待 version を equality assertion にしなければ、旧版参照は clean のまま通る。
2. **enum を追加しただけでは typed schema は total にならない。** その欄が「いつ必須・いつ禁止」かを判別欄との直積で定める必要がある。
3. **artifact の version は差分節や commit message ではなく、正本自身の title / metadata が名乗る。**
4. **live と history の区別は読者の善意に委ねない。** 冒頭 boxed status は、明示的に history block 化されない限り current status と読まれる。
5. **line-hash は行番号 drift を救うが、意味の同期までは救わない。** hash は triage の同一性、version manifest は artifact 間の意味的一致を担当させる。

---

## F9. 共同設計者としての発案

### F9.1 version-event manifest を lint の入力正本にする

例えば次を一 record にする。

```text
event_id
artifact_path
artifact_sha256
declared_version
required_header_pattern
checker_path
checker_sha256
expected_pass_count
claims_row_id
claims_required_tokens
certificate_sha256
```

preflight は `v2.9 / v2.4 / 37/37` をコードへ手書きせず、この manifest と本文 header・CLAIMS・certificate を相互比較する。今回の W3-17 と TB4 title は自動的に止まる。

### F9.2 `antecedent_bundle_id` を discriminator にした union schema

`exact_recovery_path` を平坦な optional field にせず、

```text
oneOf:
  exact-result:
    antecedent_bundle_id = .../exact/v1
    exact_recovery_path  = R-a | R-b
    recovery_evidence_id + digest required
  twisted-result:
    antecedent_bundle_id = .../twisted/v1
    exact_recovery_path prohibited
  falsifier-result:
    antecedent_bundle_id = FALSIFIER.../twisted/v1
    exact_recovery_path prohibited
```

とする。R-a/R-b の取り違えも `recovery_evidence_id` の型で止められる。

### F9.3 preflight receipt を versioned artifact にする

stdout の `CLEAN` だけでなく、

```text
source_commit
ordered_steps
artifact digests
checker verdict digests
claims row hash
active triage count
orphan triage count
lint version/digest
final verdict
```

を持つ receipt を出す。`orphan_triage_count != 0`、reviewer 空、未知 disposition、CLAIMS hash 不一致を event blocker にすれば、F8.3 の順序と最終状態を後から再現できる。

---

## F10. 監査範囲外申告

監査範囲は、便 52 が列挙した七 artifact、対象 commit の CLAIMS W3-17/W3-18、便 51 からの差分、certificate の三 digest、既存 Node checker 二本、preflight/triage のコードと active hit である。

範囲外は、まだ作成されていない Rule 1 v1.4 / manifest v1.6 の実 artifact、個別モデル探索、\(u\)・封印値・Freeze 2、外部文献原文、Lean 形式化である。GAP は本便で再生成せず、既存 certificate の schema・結果・digest 束縛を検収した。再走は Node 13/13、TB4 37/37、target snapshot の lint に限る。本便外の dirty worktree は判定にも変更にも用いていない。
