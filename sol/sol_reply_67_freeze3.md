# 便 67 返信 — \(N_\infty\) stage-2 freeze 最終監査

## F1. 総合判定

**差戻し。freeze ID・実装認可は発行しない。**

三つの提示 blob の SHA-256、v8 の external anchor、v3 pin、非循環な
hash topology、便 66 の二つの複合 failure に対する二軸 routing は通った。
また、依頼された P-S3 の設計判断そのものは **PASS** とする。

しかし exact freeze bundle には、少なくとも次の三つの operative blocker
が残る。

| ID | blocker | 判定 |
|---|---|---|
| **B67-1** | governing spec v8 §5.3 invariant 2 は「public は `primary_reason_code` のみ」とする一方、同じ spec の §5.1 / §5.4.1 は public `secondary_reason_codes[]` を要求する。 | **FAIL** |
| **B67-2** | manifest v3 の D-3 は、その preimage である `build_definition_blob_digest` / `pinned_input_digests[]` を record に持たず、I-0 / D-R2 も D-3 を再計算しない。さらに共有 toolchain / build step を三交差が必ず拾う規則がない。 | **FAIL** |
| **B67-3** | spec v8 §9 の live 実装ゲートが依然として「v6 の Sol 監査 PASS」を起点にしている。v8 exact bundle の freeze PASS を要求する文になっていない。 | **FAIL** |

従って本便の operative state は次である。

```text
predicate_spec_candidate_id       = "mb/ninfty-stage2-predicate/v8"
predicate_spec_candidate_digest   = 9a7df744341e41f30d82f1b36c26638925abee89e367cd5f3d26675302539963
verifier_contract_candidate_id    = "mb/ninfty-verifier-contract/v3"
verifier_contract_candidate_digest
                                    = bd4d5064e04ef292d7f21fa3cf5b8089c20ef34c322461920dc95c9775e4d484
dependency_manifest_candidate_id  = "mb/dependency-manifest/v3"
dependency_manifest_candidate_digest
                                    = 1a8d1f2147178b49d5fe81da625256762a9e9dafd1a963b57d554bcf97c7b7dd

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

便 67 委嘱、対話帳 T-17 まで、便 65・66 返信、spec v7/v8、
contract v2/v3、manifest v2/v3 を読んだ。委嘱 target は commit
`0f4e0d6`、現在 HEAD は配送 commit `241c9f0` である。target から HEAD
まで対象三 path に差分はなく、worktree も同じ bytes だった。

| artifact | bytes | LF 行数 | SHA-256 | 委嘱値 |
|---|---:|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v8.md` | 52,317 | 589 | `9a7df744341e41f30d82f1b36c26638925abee89e367cd5f3d26675302539963` | 一致 |
| `docs/mb_ninfty_verifier_contract_v3.md` | 25,855 | 364 | `bd4d5064e04ef292d7f21fa3cf5b8089c20ef34c322461920dc95c9775e4d484` | 一致 |
| `docs/mb_dependency_manifest_v3.md` | 21,417 | 327 | `1a8d1f2147178b49d5fe81da625256762a9e9dafd1a963b57d554bcf97c7b7dd` | 一致 |
| `docs/week4-K5_S5設計_opus_v1.md` | 69,045 | 518 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` | 便 66 再現値と一致 |

四 blob とも UTF-8、LF、BOM なしで、CR / TAB / C0 は 0。spec の
supersedes v3〜v7、contract v2、manifest v2 の digest も各実体から
再計算して全て一致した。封印値・候補係数・raw shard 名への接触はない。

---

## F3. external anchor・pin・hash topology は PASS

v8 §6 の anchor owner は正しく分離された。

| anchor | owner | bound digest | 判定 |
|---|---|---|---|
| `#cert-schema` ほか spec 内部 anchor | spec v8 | `predicate_spec_digest` | **PASS** |
| `#input-separation` | manifest v3 §5.3 | manifest v3 digest | **PASS** |
| `#derivation` | manifest v3 §2.2 | manifest v3 digest | **PASS** |
| `#result-vector` | contract v3 §3.4 | contract v3 digest | **PASS** |

三 external anchor は各 owner blob に実在する。v8 は
`dependency_manifest_schema_id/digest` と `verifier_contract_id/digest` を
external anchor より先に定義しており、v7 の forward reference と
owner-digest 取り違えは閉じた。

pin graph は

```text
manifest v3
    -> governing spec ID v8（digest は receipt）

contract v3
    -> manifest v3 exact digest
    -> governing spec ID v8（digest は receipt）

spec v8
    -> contract v3 exact digest
    -> manifest v3 exact digest

receipt
    -> spec v8 exact digest
    -> contract/manifest の governing_spec_digest
```

であり、`manifest -> contract -> spec -> receipt` の順に hash を確定できる。
循環はない。外部 S5 の五 ID は、receipt でいずれも

```text
b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555
```

へ束縛する候補値として再現した。ただし F6〜F8 により、これはまだ
approved receipt の値ではない。

---

## F4. 便 66 の reason-routing blocker は局所的には閉じた

contract v3 §3.4 と spec v8 §5.3.3 は、`PASS / FAIL / ABSENT` を区別する
canonical per-witness result vector \(R_A,R_B\) を比較する。semantic 軸と
concordance 軸の合成を紙上で展開すると次になる。

| 事象 | \(I\) | primary | P-S3 による public secondary |
|---|---|---|---|
| `[24]` かつ \(R_A\ne R_B\) | `{[24],[26]}` | `[24]` | `[[26]]` |
| S2 failure なし、両者 overall FAIL だが vector が異なる | `{[26]}` | `[26]` | `[]` |
| native 一致、同じ witness failure に合意 | `{[25]}` | `[25]` | `[]` |
| `[24]` かつ \(R_A=R_B\) が witness failure | `{[24]}` | `[24]` | `[]` |

従って、

- X-5 は S2 停止時にも `[26]` を保持する。
- X-6 は「両者 overall FAIL」の下に隠れた vector 不一致を `[26]` に送る。
- `[25]` と `[26]` は \(R_A=R_B\) / \(R_A\ne R_B\) により排他。
- `[24]` と `[25]` は semantic 軸内で排他。
- `[24]` と `[26]` は意図どおり共存する。

便 66 F4.1 / F4.2 に対する routing 修理は **PASS** である。

---

## F5. P-S3 の裁定 — 設計は PASS

**public secondary を concordance 軸、現 enum では `[26]` 一個に限る案を
承認する。**

理由は次の三点。

1. `[26]` が唯一の reason のときは、それ自体が primary なので public に出る。
2. より高優先の semantic reason と共存するときだけ、secondary に `[26]`
   を一個出せば verifier disagreement を隠さない。
3. semantic の非 primary 全組合せは sealed `all_reason_codes[]` に残すため、
   public 面に小宇宙の reason fingerprint を増やさない。

ここで便 66 F13 の「public は primary 一個」は、**primary field の値が
一個である**という意味に訂正する。「public reason は primary 以外を一切
持たない」と読めば便 66 F4.1 と両立しない。過去返信は記録として変更せず、
本便を erratum とする。

正しい射影は明示的には

```text
public_primary(I,R) =
    state_machine が定める単一 code

public_secondary(I, primary) =
    canonical_sort( ({[26]} ∩ I) - {primary} )

sealed_all(I,R) =
    canonical_sort(I ∪ R)
```

である。この policy 自体ではなく、次節のとおり governing spec がまだ
この policy と矛盾していることが blocker である。

---

## F6. blocker B67-1 — v8 invariant 2 が public secondary を禁止する

spec v8 §5.1 は public envelope に

```text
primary_reason_code
secondary_reason_codes[]
```

を置き、§5.4.1 P-S3〜P-S6 は `[26]` の secondary 出力を normative に
要求する。一方、同じ spec の §5.3 invariant 2 は逐語的に

```text
invariant 2: public は primary_reason_code のみを出す(単数・全域)
```

とする。さらに §5.3.3 末尾は「invariant 1–4 はそのまま成立する」と書く。
これは同じ blob 内の直接矛盾である。

contract v3 §0.1 は、contract と governing spec が矛盾すれば spec が優先
すると定める。従って `[24]+[26]` の例では、

```text
§5.4.1 P-S5    -> secondary = [[26]]
§5.3 invariant 2 -> secondary を public に出してはならない
```

の二つが同時に operative になり、同じ入力に対する public envelope が
一意に決まらない。contract v3 §8 案 B 自身も「§5.3 の invariant に
secondary 条文を足す」と要求していたが、v8 は public schema と §5.4.1
だけを追加し、既存 invariant を修正し忘れている。

これは prose typo ではない。public output schema と漏洩境界の双方を決める
条文の衝突なので、exact blob を freeze できない。

最小修理は新 spec で invariant 2 を例えば

```text
invariant 2:
  primary_reason_code は単数・全域。
  public reason は primary と
  canonical_sort( ({[26]} ∩ I) - {primary} ) のみ。
```

へ置換し、「invariant 1,3,4 は不変、invariant 2 は v8 erratum で更新」と
版履歴・§5.3.3 に明記すること。既存 v8 blob の上書きではなく新 version が要る。

---

## F7. blocker B67-2 — provenance hash は再計算可能になったが、build 経路が閉じていない

### F7.1 D-1 / D-2 は PASS、D-3 は未 operational

manifest v3 は `source_artifact_digests[]`、`toolchain_digest`、
`build_step_digests[]` を mandatory にし、D-1 / D-2 の canonical preimage
を固定した。I-3b が source digest 集合を直接交差するため、便 66 F6 の

```text
同じ source + 別 toolchain + producer が別 ID を付ける
```

という反例は閉じた。これは **PASS**。

しかし D-3 は

```text
build_root_id = H({
  build_definition_blob_digest,
  pinned_input_digests[]
})
```

と定義する一方、

- `manifest_entry` は二つの preimage 欄を持たない。
- top-level `dependency_manifest` も二つの preimage 欄を持たない。
- D-R2 は受領側再計算を D-1 / D-2 にしか要求しない。
- I-0 も D-1 / D-2 しか再計算しない。

従って受領側は D-3 を再計算できず、`build_root_id` は依然として
producer の申告値である。「D-1〜D-3 を凍結し受領側が再計算」という
納品要旨を D-3 について満たしていない。

### F7.2 三交差は共有 build helper を見逃せる

さらに次の manifest は現条文をすり抜ける。

```text
A:
  content_digest            = a
  source_artifact_digests   = [s_A]
  toolchain_digest          = t
  build_step_digests        = [g]

B:
  content_digest            = b
  source_artifact_digests   = [s_B]
  toolchain_digest          = t
  build_step_digests        = [g]

a != b, s_A != s_B
```

\(t\) と \(g\) は両実装へ同じ数学処理を生成する共有 build helper とする。
空 TCB の下では `[11]` で止まるべき common bug path である。

ところが現規則では、

```text
binary content intersection = empty
source artifact intersection = empty

D2_A != D2_B                       # source が異なるため
family_A != family_B               # M-2 は D2 -> family を単射にするため
implementation family intersection = empty
```

となり I-3a / I-3b / I-3c を全て通る。`toolchain_digest` と
`build_step_digests[]` は D-2 の preimage に入るだけで、それ自身の集合積が
ない。R-1〜R-5 にも、出力へ影響する build-time artifact を必ず closure
entry とし、上の \(t,g\) を `binary_content_set` に入れる条文がない。

また M-2 の「D-2 に対する決定的・単射な family ID」は lineage digest の
別名であり、異なる lineage を「同じ generator family」としてまとめられない。
従って I-3c の説明する family detector にはなっていない。

最小修理は次のいずれかではなく、少なくとも (a)(b) が要る。

1. **(a)** `build_definition_blob_digest` / `pinned_input_digests[]` を mandatory
   field にし、D-3 と subject code への binding を receipt 側で再計算する。
2. **(b)** output-affecting な toolchain / build step / code generator を
   closure entry に必ず昇格し、各 digest が entry の `content_digest` に
   解決されることを fixpoint 検収する。これで I-3a が共有 build helper を拾う。
3. **(c)** `implementation_family_id` を使うなら、D-2 の単射的別名ではなく、
   receipt authority が根拠付きで mint する**複数 lineage を含み得る
   equivalence class**にする。機械的な exact identity だけを扱うなら
   “family” の過大主張を削る。

hash の再計算は「申告 preimage と申告 aggregate の整合」を示すだけで、
preimage の完全性や build への実接続を自動では証明しない。

---

## F8. blocker B67-3 — spec §9 の live gate が v6 のまま

spec v8 §9 は current implementation condition であるにもかかわらず、
boxed chain を

```text
v6 の Sol 監査 PASS
  -> §6 の空欄を receipt 側で充填
  -> 実装
```

としている。これは版履歴中の historical quotation ではない。

§0.0 の `live_status_authority = Sol freeze reply + commander receipt` により
receipt 自体を省略することはできないので、単独で即時実装を許す穴ではない。
しかし v6 は E1・E2・A・B・C の erratum 前であり、v6 の audit PASS は
v8 exact bundle の freeze PASS の代用にならない。便 66 F7 で contract /
manifest の live v6 reference を blocker としたのと同じ基準で、ここも
新 spec の

```text
exact freeze bundle の Sol PASS
  + その digest 群を束縛した commander receipt
  -> receipt scope 内の実装
```

へ同期する必要がある。

---

## F9. 旧 blocker の閉鎖表

| 便 66 の項目 | 便 67 判定 | 理由 |
|---|---|---|
| E1 witness kind | **PASS（不変）** | v7 の `ideal-equality` / `disjointness` 分離を保持。 |
| E2 independent mismatch | **PASS** | X-5 / X-6 と canonical vector が二例を捌く。 |
| source-ID 付け替え | **PASS（狭義）** | source preimage と I-3b により、同じ source の ID 付け替えは不可。 |
| contract live authority | **PASS** | operative な参照は v8。旧 v6 は差分表の historical quotation のみ。 |
| manifest live authority | **PASS** | operative な参照は v8、digest は receipt。 |
| external anchor owner | **PASS** | owner artifact と bound digest が一致。 |
| initial TCB | **PASS** | content / source / family の三欄が literal `[]`。 |
| exact freeze bundle 全体 | **FAIL** | B67-1〜B67-3。 |

---

## F10. freeze / 実装認可の最終裁定

```text
exact candidate digests                       = REPRODUCED
v8 external anchor typing                     = PASS
v3 pin topology / no hash cycle               = PASS
two-axis routing                              = PASS
P-S3 policy                                   = PASS
public-envelope normative consistency         = FAIL
build-root receipt-side recomputability       = FAIL
shared build-helper detection                 = FAIL
live implementation-gate version              = FAIL

predicate_spec_freeze_id                      = NOT ISSUED
freeze_receipt                                = NOT ISSUED
searcher_v2 implementation                    = NOT AUTHORIZED
checker implementation                        = NOT AUTHORIZED
D-2 generator implementation                  = NOT AUTHORIZED
verifier A/B implementation                   = NOT AUTHORIZED
model_builder                                 = LOCKED
```

従って依頼された receipt 四欄

1. spec self digest、
2. contract / manifest の `governing_spec_digest`、
3. 五つの S5 ID と source digest、
4. content / source / family TCB の三つの空列、

は candidate values としては準備できるが、approved receipt として記入・
発行しない。EP 到達前の `partial predicate / UNKNOWN`、decision/audit lane
分離、別 runtime、旧 8 hit の neutral lane 限定も、まだ実装認可へ昇格しない。

---

## F11. 再提出の最小順序

記録を上書きせず、新 version で次を行う。

1. manifest 新版:
   - D-3 preimage を record に加え、I-0 / D-R2 で再計算。
   - output-affecting build artifact を closure へ必須接続。
   - family ID を本当に family equivalence にするか、過大な family claim を削る。
2. contract 新版:
   - manifest 新版を exact pin。
   - §5.3 の「erratum 案 A」という public-secondary cross-reference を
     正しい案 B へ直す。
3. spec 新版:
   - invariant 2 を P-S3 と同期。
   - 「invariant 1–4 不変」を正確に修正。
   - §9 の live `v6 PASS` を exact bundle PASS へ更新。
   - contract / manifest 新版を exact pin。
4. 最後に receipt:
   - spec self digest、
   - 両下位 artifact の governing-spec digest、
   - S5 五 ID、
   - 初期 TCB 全欄
   を literal に束縛。

hash 順序は引き続き

```text
manifest -> contract -> spec -> receipt
```

でよい。

---

## F12. ★教材

1. **新しい public field を足したら、古い output invariant も同じ差分で更新する。**
   schema と invariant の片方だけを直すと、一つの exact blob が二つの出力を許す。
2. **hash 再計算は provenance の真実性ではなく、提示された preimage との
   自己整合しか証明しない。** preimage の完全性と build output への接続は
   別の義務である。
3. **単射な `lineage_digest -> family_id` は family 分類ではなく rename である。**
   family が複数 lineage を束ねる概念なら、同値類の mint 規則が要る。
4. **build-time の common bug path も implementation dependency である。**
   runtime closure だけを取ると、共有 code generator / compiler plugin /
   output-affecting table が抜ける。
5. **古い version 名が許されるのは明示した履歴欄だけ。** current gate の
   boxed formula に残った version は live authority の型誤りになる。

---

## F13. 共同設計者発案

### F13.1 public reason は「列」より射影関数を正本にする

将来 enum が増えても P-S3 の意味を保つため、schema prose より先に

```text
PUBLIC_SECONDARY_ALLOWLIST = { verifier-result-mismatch }

secondary_reason_codes =
  canonical_sort(
    (I ∩ PUBLIC_SECONDARY_ALLOWLIST) - {primary_reason_code}
  )
```

を frozen rule とし、fixture を三つ置くことを勧める。

```text
[24]+[26] -> primary [24], secondary [[26]]
[26] only -> primary [26], secondary []
[15]+[24] -> primary [15], secondary []
```

### F13.2 provenance は runtime / source / build / family の四面に分ける

```text
runtime_binary_set
source_artifact_set
build_artifact_set       # toolchain + build steps + generators
authority_family_set     # 必要なら、根拠付き equivalence class
```

を別々に交差させると、D-2 aggregate の解釈に依存しない。初期 TCB も同じ
四面で空にする。family の主観判定を避けたいなら最初の三面だけを normative
にし、family は audit flag に留める方が fail-closed である。

---

## F14. 監査範囲外申告

### 本便で行ったこと

- 便 67 委嘱、対話帳 T-17 まで、便 65・66 の読解。
- target / HEAD / worktree の同一性、SHA-256、bytes、LF 行数、
  CR / TAB / C0 / BOM の照合。
- spec v7→v8、contract v2→v3、manifest v2→v3 の全 byte diff と、
  v8 / v3 / v3 の全文監査。
- external anchor の owner、anchor 実在、pin graph、supersedes digest、
  S5 source digest、TCB 実値の検査。
- F4.1 / F4.2 と追加二例の reason-routing 紙上展開。
- lineage preimage、受領側再計算、build dependency、family mint の
  adversarial paper audit。

### 本便で行っていないこと

- searcher / checker / generator / verifier の実装または実行。
- 実 dependency manifest、build attestation、source closure、TCB の生成。
- sealed candidate、旧 8 hit、negative fixture、EP の観測。
- GAP 探索、Lean 証明書、Model-Builder の解錠。
- approved receipt の発行。

従って本便は exact artifact と仕様の paper audit であり、Lean の意味での
`verified` ではない。指定返信ファイル以外の既存 artifact は変更していない。
