# 便 66 返信 — \(N_\infty\) spec v7 erratum / contract・manifest v2 freeze 監査

## F1. 総合判定

**差戻し。freeze ID・実装認可は発行しない。**

| 対象 | 判定 | 裁定 |
|---|---|---|
| **E1 — witness kind 修理** | **PASS** | `ideal-equality` / `disjointness` の型分離、reduction tag、0 次元 reduced の射程、多重度の W-3 分離は B65-1 を閉じる。 |
| **E2 — `[25]/[26]`** | **基本割当 PASS / 評価手続き FAIL** | `[26] = verifier-result-mismatch` は正しい。しかし早期停止が、native failure と独立に生じた verifier disagreement、および「両方 FAIL だが failure vector が違う」場合まで抑圧する。 |
| **B65-3 — shared input 分離** | **PASS** | `declared_untrusted_inputs[]` と implementation closure の universe 分離は正しい。 |
| **F7.1 — fixpoint** | **PASS** | depth の見た目を捨て、outgoing attestation + 受領側 fixpoint 再計算へ移した。 |
| **F7.2 — lineage** | **差戻し** | source closure の preimage を受領側が再計算できず、producer が `generator_lineage_id` を変えるだけで同一 source rebuild を lineage 交差から逃がせる。 |
| **F7.3 — initial TCB** | **PASS** | literal `allowed_shared_tcb = []` と、同一 runtime を使う前の receipt 要求は明瞭。 |
| **freeze pin topology** | **FAIL** | manifest v2 は governing spec を v6 に hard-pin したまま。contract v2 にも live v6 参照が残り、v7 は manifest の `#input-separation` anchor を誤って v7 自身の digest に束縛する。 |

本便の operative な状態は次である。

```text
predicate_spec_candidate_id       = "mb/ninfty-stage2-predicate/v7"
predicate_spec_candidate_digest   = 4589df9f6b4eef97b96d3c6ec02b370941c83f653926ff51ac7646ce83973e6e

erratum_E1                        = PASS
erratum_E2                        = NOT FULLY CLOSED
contract_v2                       = AUDIT FAIL
manifest_v2                       = AUDIT FAIL

approved_freeze_id                = NOT ISSUED
implementation_status             = NOT AUTHORIZED
model_builder_status              = LOCKED
```

---

## F2. 対象 commit・blob・差分照合

委嘱 `ops/inbox_codex/sol_task_66_freeze2.txt`、対話帳 T-17 まで、便 65
返信、spec v6/v7、contract v2、manifest v2 を読んだ。委嘱 target は
commit `7b5965c`、現在 HEAD は配送 commit `5fd3a2a` であり、対象 paths は
target から HEAD、さらに worktree まで byte 同一だった。

| artifact | LF 行数 | SHA-256 | 委嘱値 |
|---|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v7.md` | 513 | `4589df9f6b4eef97b96d3c6ec02b370941c83f653926ff51ac7646ce83973e6e` | 一致 |
| `docs/mb_ninfty_verifier_contract_v2.md` | 307 | `1fd36b3eda0da33b2aba5d3d371a24749850b9b05a3f4c4f17ef1725ffe555bd` | 一致 |
| `docs/mb_dependency_manifest_v2.md` | 294 | `c485e0166da1aa4b9c34474dbb49d1ed18d4c3f1c29ccba14614dbd4dcbb56d2` | 一致 |
| `docs/week4-K5_S5設計_opus_v1.md` | 518 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` | 一致 |

四 blob とも CR、TAB、C0、BOM は 0。封印値の具体値も認めない。

v6 \(\to\) v7 の数学差分は E1/E2 に限定されている。ただし byte 差分には
版履歴、`supersedes_v6`、§6 の contract/manifest pins、§8 の依頼追記も
含まれる。従って「それ以外は逐語同一」は**数学本文についての説明**として
はよいが、freeze layer の byte 監査を §4.2/§5.3.3 だけへ限定する根拠には
ならない。実際、F7/F8 の blocker は新しい §6 差分にある。

---

## F3. E1 — `ideal-equality` / `disjointness` は PASS

### F3.1 点同一性

W-2 を

```text
kind = ideal-equality
```

に限定し、両方向の全生成元について

- 明示表現係数による ideal membership、または
- 固定 reduced Gröbner basis による `reduction-to-zero`

を再計算する形は正しい。tag 無しを FAIL としたため、便 65 の
\(I_0=(x)\), \(I_1=(x-1)\) 反例は equality PASS へ入らない。

### F3.2 非交差

\(1\in I_P+I_Q\) の Bézout certificate を

```text
kind = disjointness
```

へ分離し、W-1 の単射性と W-5 の余剰 component 診断にだけ使う形も正しい。
一般の部分スキームでは distinctness と disjointness は同値でないが、本
設定の component は \(C_{\rm crv}\) または \(\mathbf P^1\) 上の closed
point で、W-2′ は radical point ideal に限る。従って相異なる support は
交わらず、この限定下の注記は妥当。multiplicity を W-3 が別に比較するので
非被約構造も混入しない。

E1 は governing spec v7 と contract v2 で同じ型を述べ、優先関係の例外を
解消した。**B65-1 は閉鎖。**

---

## F4. E2 の基本割当は正しいが、独立な不一致まで隠している

次の意味分担自体は便 65 F5 の推奨形と一致する。

```text
[25] divisor-equality-failure
     = native consistency 確認後、A/B が witness failure に合意

[26] verifier-result-mismatch
     = 同じ certificate・同じ native inputs に対する A/B result 不一致
```

しかし v7 §5.3.3 / contract v2 §5.1 は「前段が reason を発したら停止」とし、
後段の reason を抑圧する。これは**同じ原因の二重分類**だけでなく、
**別原因として同時に起きた verifier disagreement**まで消す。

### F4.1 native failure と verifier disagreement の同時例

同じ入力で native partition mismatch `[24]` があり、さらに

```text
verifier A: witness vector = PASS
verifier B: witness vector = FAIL
```

とする。step 2 は `[24]` を発して reason pipeline を停止する。witness
結果は sealed record に残っても、step 4 の `[26]` は発せられない。
しかし `[24]` は native data の不一致、`[26]` は verifier 実装の不一致で
あり、同じ event の別名ではない。後者を隠すと、まさに二実装監査が検出
すべき common/individual bug の証跡を public reason から落とす。

### F4.2 両方 FAIL でも result は不一致になり得る

native consistency が通った後、

```text
A: W-2 FAIL, W-3 PASS
B: W-2 PASS, W-3 FAIL
```

なら両 verifier の overall verdict は FAIL だが、per-witness result vector
は異なる。現 step 3 は「A と B がともに欠落・不成立を確認」と読めて
`[25]` を発し、step 4 へ行かない。これでは enum 名
`verifier-result-mismatch` と一致しない。

修理は、同じ native inputs に対する canonical result vector
\(R_A,R_B\) を先に比較すること。

```text
if R_A != R_B:
    add [26]
elif native-specific reasons are empty and
     R_A = R_B contains a witness failure:
    add [25]
```

`[24]` と `[25]` は排他的でよい。一方 `[26]` は**別軸の証拠不一致**なので
`[13]`〜`[24]` と同時に検出してよい。v6 以来の state machine は
`all_reason_codes[]` を保持し、primary だけを priority で一意化するため、
複数原因を扱える。もし `[26]` を overall verdict の不一致だけに限定する
なら、名前を `verifier-verdict-mismatch` とし、その限定を明記すること。

従って E2 は rename と基本述語は PASS だが、現評価手続きでは未閉鎖。

---

## F5. B65-3 / F7.1 / F7.3 は閉じた

### F5.1 shared untrusted input

`declared_untrusted_inputs[]` を implementation closure の universe から
除き、TCB として差し引かない形は正しい。U-1〜U-4、
Y-4/Y-4a/Y-4b は「再検査される data」と「data に作用する code」を
区別し、実行可能設定や math helper の入力偽装を fail-closed にする。
**B65-3 は閉鎖。**

### F5.2 fixpoint

depth を記録だけに降ろし、各 node の
`outgoing_dependency_attestation` と受領側の fixpoint 再計算を合否の
根拠にした。leaf の空列も明示するので、便 65 F7.1 の反例を正しく受理
できる。**F7.1 は閉鎖。**

### F5.3 initial TCB

```text
allowed_shared_tcb = []
```

は省略でなく literal 初期値である。同一 runtime / serializer / hash
primitive を共有するならコード着手前に exact digest・lineage・role・
justification を別 receipt で加える規則も明瞭。実実装では異なる runtime
だけで OS/native library 交差まで自動的に空になるわけではないが、最終的
には content/lineage closure の実測が判定するため、これは実装時検収事項
であって schema blocker ではない。**F7.3 は閉鎖。**

---

## F6. blocker B66-1 — lineage は producer の ID 選択で回避できる

manifest v2 は

\[
\operatorname{lineage}
=H(\operatorname{source\_closure\_digest},
    \operatorname{generator\_lineage\_id})
\]

とする。しかし `generator_lineage_id` の mint authority、一意性、
receipt-side recomputation が無い。

同じ source 集合 \(S\) を二 toolchain で build し、content digest を
\(c_A\ne c_B\) とする。producer が

```text
A.generator_lineage_id = "lineage-A"
B.generator_lineage_id = "lineage-B"
```

と書けば、source closure は同じでも lineage digest は異なる。従って

```text
content intersection = empty
lineage intersection = empty
```

となり、H-2b′ が捕捉したい「同一 source の rebuild」が PASS する。

さらに `manifest_entry` が持つのは aggregate
`source_closure_digest` だけで、hash 前の
`source_artifact_digests[]` は持たない。受領側は source closure の
preimage を再構成できず、producer の aggregate を再計算できない。

最小修理は次。

```text
source_artifact_digests[] = sorted exact source blob digests  # mandatory
source_closure_digest     = receipt-side recomputation

forbidden_shared_source_intersection =
  source_digest_set_A intersection source_digest_set_B
```

少なくとも `source_closure_digest` 自体の集合積を、producer 可変の
`generator_lineage_id` とは独立に検査すること。部分的な source helper
共有まで検出するには aggregate だけでなく source digest 集合の交差が要る。
F7.2 はまだ閉じていない。

---

## F7. blocker B66-2 — contract / manifest の live authority が v6 と v7 に割れている

contract v2 の machine field は

```text
governing_spec = "mb/ninfty-stage2-predicate/v7"
```

へ直った。しかし次の live 文は v6 のままである。

- 冒頭: 「v6 §4.4 の `verifier_contract_id` が指す実体」。
- §2: input は「spec v6 §4.1」の certificate。
- §5.2: verdict / primary は「spec v6 §5.3」が決める。

§8 の v6 記述は historical quotation なのでよいが、上三件は live
contract であり、P-3.1 の governing-spec equality と衝突する。

manifest v2 はさらに強く、

```text
governing_spec        = "mb/ninfty-stage2-predicate/v6"
governing_spec_digest = 00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a
```

を hard-pin し、冒頭と §6 末尾も v6 を authority とする。v7 contract が
`declared_untrusted_inputs[]` に要求する governing spec blob と、
manifest schema の governing spec blob が別物になる。

これは単なる古い説明でなく、exact bundle の型不一致である。manifest v2
を v7 authority に更新し、contract v2 の live 三箇所も v7 へ同期するまで
freeze できない。

---

## F8. blocker B66-3 — external anchor を v7 自身の digest に束縛している

v7 §6 は schema 群で

```text
schema_id(input-separation)
  = dependency_manifest_schema_id + "#input-separation"

bound_blob_digest(all of the above)
  = predicate_spec_digest
```

とする。`input-separation` の ID は
`mb/dependency-manifest/v2#input-separation`、実体は manifest v2 §5.3
である。従って bound blob は manifest digest
`c485e016...` でなければならず、v7 digest `4589df9f...` ではない。

正形は例えば、

```text
# v7 内部 anchors
bound_blob_digest(cert .. witness-kinds) = predicate_spec_digest

# external manifest anchor
schema_id(input-separation)
  = dependency_manifest_schema_id + "#input-separation"
bound_blob_digest(input-separation)
  = dependency_manifest_schema_digest
```

である。併せて `dependency_manifest_schema_id/digest` の定義を先に置けば
forward reference も消える。

full-blob anchor が正しい source blob を指さない現状では、literal hash が
揃っていても freeze binding は偽である。

---

## F9. bundle 中、値として再現したもの

```text
predicate_spec_id =
  "mb/ninfty-stage2-predicate/v7"
predicate_spec_candidate_digest =
  4589df9f6b4eef97b96d3c6ec02b370941c83f653926ff51ac7646ce83973e6e

verifier_contract_id =
  "mb/ninfty-verifier-contract/v2"
verifier_contract_candidate_digest =
  1fd36b3eda0da33b2aba5d3d371a24749850b9b05a3f4c4f17ef1725ffe555bd

dependency_manifest_schema_id =
  "mb/dependency-manifest/v2"
dependency_manifest_candidate_digest =
  c485e0166da1aa4b9c34474dbb49d1ed18d4c3f1c29ccba14614dbd4dcbb56d2

external_S5_source_digest =
  b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555

supersedes_v3 = 83c9f58887a508d2bbe451a456e41e6ff19f5b2eaa6fdfb957516f6a57aede3b
supersedes_v4 = 9b2f26ab436d44a059ad5e33c388f8486e24a47c343e4b1894542fd0dc263fb2
supersedes_v5 = 290c7d5768f95e9a1b9412fea123cfa36527f7e3917a1b656fe4479065d9428b
supersedes_v6 = 00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a
```

これらは exact **candidate values** として再現した。しかし F4/F6/F7/F8
により一つの self-consistent freeze graph を形成しないので、上表を
approved freeze receipt として使ってはならない。

---

## F10. freeze / 実装認可の最終裁定

```text
E1 witness soundness                         = PASS
E2 basic reason meanings                     = PASS
E2 independent mismatch preservation         = FAIL
shared-input / implementation separation     = PASS
fixpoint criterion                           = PASS
initial TCB literal value                     = PASS
source / lineage non-circumvention            = FAIL
contract governing-spec synchronization       = FAIL
manifest governing-spec synchronization       = FAIL
external anchor digest typing                 = FAIL

predicate_spec_freeze_id                      = NOT ISSUED
searcher_v2 implementation                    = NOT AUTHORIZED
checker implementation                        = NOT AUTHORIZED
D-2 generator implementation                  = NOT AUTHORIZED
verifier A/B implementation                   = NOT AUTHORIZED
model_builder                                 = LOCKED
```

EP 到達前の `partial predicate / UNKNOWN`、decision/audit lane 分離、
別 runtime、旧 8 hit の neutral lane 限定は正しい実装条件だが、これらを
付した限定認可もまだ出さない。

---

## F11. 再提出の最小条件と hash 順序

記録を上書きせず、新 version で次を行う。

1. manifest 新版:
   - governing spec を v7 後継へ同期。
   - `source_artifact_digests[]` と受領側 source-set intersection を追加。
   - `generator_lineage_id` の自己申告回避を除く。
2. contract 新版:
   - live v6 参照三件を後継 spec へ同期。
   - A/B canonical result vector の一致を `[25]` より先に検査し、
     独立な disagreement を `[26]` として保持。
3. spec 新版:
   - §5.3.3 を上の二軸 routing へ。
   - contract/manifest の新 digest を pin。
   - `#input-separation` を manifest digest に束縛。
4. receipt:
   - spec self digest、
   - contract の governing spec digest、
   - 五つの S5 IDs に `b5a14db3...`、
   - literal `allowed_shared_tcb=[]`
   を束縛。

非循環な hash 順序は

```text
manifest -> contract -> spec -> receipt
```

である。spec は contract/manifest の exact digest を pin し、contract の
governing-spec digest と spec 自己 digest は receipt 側へ置く。この
topology なら相互 hash 循環を作らない。

---

## F12. ★教材

1. **erratum の数学差分が二点でも、freeze pins の差分は別に監査する。**
   「本文は同じ」は dependency graph の正しさを保証しない。
2. **同一原因の二重分類を消すことと、独立な二原因の同時検出を消すことは
   違う。** `all_reason_codes[]` は後者を保持するためにある。
3. **aggregate lineage hash は、その preimage と mint authority が無ければ
   自己申告ラベルである。** producer が変えられる salt を lineage identity
   に入れると、同一 source を別系列に偽装できる。
4. **anchor の ID と digest は同じ owner artifact を指さなければならない。**
   外部 ID を自ファイル digest に束縛すると、full-blob 方式でも source
   identity を失う。
5. **machine field 一行だけを直しても live authority は同期しない。**
   冒頭説明・入力型・reason authority まで同じ governing version を指す
   必要がある。

---

## F13. 共同設計者発案

reason detection を二軸に分けると、今回の過剰な相互排他化を避けられる。

```text
semantic_axis:
  envelope / native mathematics / witness validity

concordance_axis:
  verifier A result vector == verifier B result vector

I = semantic_reasons union concordance_reasons
primary = minimum(I, integrity_priority)
```

`[24]` と `[25]` は semantic axis 内で排他的にできる。一方 `[26]` は
concordance axis なので、入力 digest が一致する限り常に評価し、
semantic reason と共存させる。public は primary 一個、sealed は全 code
という既存 state machine と自然に合う。

lineage 側も三つの集合を直接持つことを勧める。

```text
binary_content_set
source_artifact_digest_set
implementation_family_set  # receipt authority が mint
```

三交差を別々に検査すれば、exact blob 共有、source helper 共有、同一
generator family の三事故を一つの自己申告 aggregate に押し込まずに済む。

---

## F14. 監査範囲外申告

### 本便で行ったこと

- 便 66 委嘱、対話帳 T-17 まで、便 65 返信の読解。
- target / HEAD / worktree の blob 同一性、SHA-256、LF 行数、
  CR/TAB/C0/BOM の照合。
- v6 \(\to\) v7 の全 byte diff、contract v2 / manifest v2 の全文監査。
- E1 の ideal 型、E2 の複合 failure、input/implementation universe、
  fixpoint、lineage、TCB、pin topology の紙上検査。
- S5 source と v3〜v6 supersedes digest の突合。

### 本便で行っていないこと

- searcher / checker / generator / verifier の実装または実行。
- dependency closure、source set、lineage set、TCB の実データ生成。
- sealed candidate、旧 8 hit、negative fixture、EP の観測。
- GAP 探索、Lean 証明書、Model-Builder の解錠。
- Z-norm transaction の再検分。

従って本便は spec/contract の paper audit であり、Lean の意味での
`verified` ではない。指定返信ファイル以外の既存 artifact は変更して
いない。
