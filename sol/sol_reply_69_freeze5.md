# 便 69 返信 — 研究指令・\(N_\infty\) freeze 5・Z-norm receipt 一括検収

## F1. 総合判定

### \(N_\infty\) freeze

**FAIL。freeze ID・freeze receipt・実装認可は発行しない。**

指摘は本便から次の二段に分ける。

| tier | ID | 内容 |
|---|---|---|
| **FAIL** | **B69-1** | contract v7 の operative な hash-order 文と machine-facing schema が、header の manifest v7 ではなく manifest v5 を参照する。self-audit は blockquote / code fence を一括除外して見逃す。 |
| **FAIL** | **B69-2** | contract が凍結する clause-registry 正規表現は quadruple prime `⁗` を認識せず、現行 clause `C-6⁗` を抽出できない。script は文書と異なる正規表現を使って PASS を出す。 |
| **FAIL** | **B69-3** | procedure-check extractor が `W-2′` を `W-2` に潰し、`covered_procedure_checks` も `W-2′` を欠く。distinctness 検査を落としても完全 coverage と自己申告できる。 |
| **FAIL** | **B69-4** | manifest v7 の `build_record_present=false` 分岐について、E-9 / I-0′ / `build_artifact_set` と SB-5 / I-0c″ が異なる処理を命じる。false record の受理と交差集合が一意でない。 |
| **NOTE** | **N69-1〜N69-5** | stale な meta label、履歴 allowlist の範囲、Markdown、内部 ID の軽微な非同期、registry の将来耐性。**これらだけを理由に再提出を要求しない。** |

B69-1〜B69-4 は書類の見栄えではない。exact owner、契約適合の母集合、
W-2′ の数学検査、独立性 manifest の受理結果を変えるため freeze-blocking
である。

### Z-norm Part A

**CONFIRMED。** `znorm-event-receipt/v1`、operative seal、W3-20 / W3-21
の区別記帳を検収した。これは \(N_\infty\) freeze の FAIL と独立であり、
Z-norm の既発効状態を取り消さない。

---

## F2. 対象 commit・digest・形式

対象 HEAD は
`d2a2bf1940b4e4cb99e1637eeb21d5bbb7a605f1`。対象三 path は HEAD と
worktree で同一である。

| artifact | bytes | LF | SHA-256 | 委嘱値 |
|---|---:|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v12.md` | 70,031 | 748 | `ac52abc5655578d6a0535a1b1640e93686e98a31dd99ee1bc740bbdb17aa4df4` | 一致 |
| `docs/mb_ninfty_verifier_contract_v7.md` | 47,126 | 529 | `d863bd7a018c2c5c3bfc1d74fde5b9c538d4954dcfa06abf6094188f3056465a` | 一致 |
| `docs/mb_dependency_manifest_v7.md` | 51,934 | 544 | `9bdd91604559cebae270efbb420324a320190f875fd2948e4e69df4b9c966673` | 一致 |
| `docs/week4-K5_S5設計_opus_v1.md` | 69,045 | 518 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` | 一致 |

全て UTF-8、LF、BOM なしで、CR / TAB / C0 は 0。HEAD blob から再計算した
直前版の digest も、

```text
spec v11     = 43e65e067ca75e826aff499193b00eeff0b797dcd470f633a809ab060714ebff
contract v6  = 7cee75fdf4190cbaad37c85a920676773c8df9966e4a1307842ac2bb4280294b
manifest v6  = f4372600b99850bea4c6545761974e7b4c8189e4e4414f491824ad47fee0c070
```

で各 `supersedes_digest` と一致した。

`python search/bundle-selfaudit-v3.py` は再実行し、13/13 `ALL PASS` を
再現した。ただし F4〜F7 は、その checker の抽出規則自体を
exact 文書と突き合わせて得た反例である。従って 13/13 は
**candidate checker output** であって、本束の合否を上書きしない。

---

## F3. 閉じた項目

既知修理のうち、次は PASS とする。

| 項目 | 判定 | 根拠 |
|---|---|---|
| public invariant 2 / invariant 5 | **PASS** | `[24]+[26] -> primary [24], secondary [[26]]` が一意。 |
| exact three-digest gate | **PASS** | spec §9 の tuple 自体は v12 / v7 / v7 の実 digest。変更時再取得も明記。 |
| anchor / pin graph | **PASS** | external anchors 15 件実在。`manifest -> contract -> spec -> receipt` は非循環。 |
| TCB arity | **PASS** | content / source / build / family の四欄、初期値は全て literal `[]`。 |
| family policy | **PASS** | blocking は binary / source / build、family は差し引かない audit flag。 |
| true build record の D-4′ | **PASS（狭義）** | top-level は `subject_code_digest`、entry は自身の `content_digest` を preimage に入れ、record ごとに再計算する。 |
| SB-7 / BA 層 | **PASS** | identity binding と実生成証跡を分け、一括捏造を防げない限界を正直に宣言。 |
| `verifier_evidence` | **PASS** | certificate から削除され、`independence_evidence` を SEALED_INTERNAL 並列に一本化。 |
| contract §7 の現行 clause 参照 | **PASS** | D-4′ / D-R2‴ / I-0c″ / SB-5〜7 等へ同期。 |
| N-2 の UNKNOWN 表示 | **PASS（表示）** | H-1a″ の独立再導出が実装依存であることを EP へ送り、過大主張を禁止。 |

spec の数学核、witness の `ideal-equality` / `disjointness` 型分離、二軸
routing は直前の PASS 部から不変であり、新しい数学的反例は見つからない。
今回の FAIL は数学核の真偽ではなく、その実装を受け入れる契約層にある。

---

## F4. FAIL B69-1 — live owner はまだ版中立化されていない

contract v7 §0 の header は

```text
dependency_manifest_schema_id     = "mb/dependency-manifest/v7"
dependency_manifest_schema_digest = 9bdd9160...
```

を pin する。一方、直後の operative な hash-order 文 :40 は、

```text
本稿は manifest v5 の exact digest を pin
```

と述べる。この blockquote は版履歴ではなく、**本稿が何を exact pin
するかを定める現行 lifecycle 文**である。

さらに §9 の machine-facing `conformance_record` 内にも、

```text
:438  provenance preimage 6 欄 (manifest v5 §2.1 ...)
:450  build_attestation optional (manifest v5 §2.5)
:456  TCB 四欄 (manifest v5 §5.2 ...)
```

が残る。ここは historical quotation ではなく実装が提出する record の
型である。

self-audit の `classify()` は全 blockquote と通常 code fence の内容を
`OPERATIVE` から外すため、これらを一件も走査しない。つまり
`LIVE-STALE=0` は「旧版が無い」のではなく、**旧版が置かれた構造を
checker が無審査域にした**結果である。

最小修理文は、版番号を再び直接書くより次でよい。

```text
本稿は §0 header の dependency_manifest_schema_id / digest を exact pin し、
governing spec の digest は receipt 側で束縛する。
```

§9 の三 comment も

```text
dependency manifest §2.1 / §2.5 / §5.2
(版は §0 header の dependency_manifest_schema_id により束縛)
```

へ版中立化する。lint は `> **[historical]**` のように明示型付けされた
blockquote だけを除外し、通常 blockquote と machine schema fence は
operative として走査しなければならない。

---

## F5. FAIL B69-2 — document-defined registry と script が別の言語

contract v7 CR-1 が凍結する clause ID 抽出規則は

```regex
^\| \*\*([A-Z][A-Za-z0-9\-\.]*[′″‴]?)\*\* \|
```

である。しかし現行の独立要件には quadruple prime の

```text
C-6⁗
```

がある。文書の正規表現を exact に適用した独立再計算では、

```text
document regex: registry size = 52, C-6⁗ absent
script regex:   registry size = 53, C-6⁗ present
difference = { C-6⁗ }
```

となった。script は無断で character class を `[′″‴⁗]?` に拡張している。

従って二つの読みのどちらでも FAIL である。

1. contract を正とする受領側では `covered_clauses` に registry 外の
   `C-6⁗` があり、CR-4 により現 conformance record 自身が不適合。
2. script を正とするなら、受領側は frozen contract に無い抽出言語を
   実行しており、contract fidelity がない。

最小修理は、contract / manifest の CR-1 を script と同じ

```regex
^\| \*\*([A-Z][A-Za-z0-9\-\.]*[′″‴⁗]?)\*\* \|
```

へ直し、fixture

```text
extract("| **C-6⁗** | ... |") == ["C-6⁗"]
```

を self-audit に固定すること。

---

## F6. FAIL B69-3 — W-2′ が procedure coverage から消える

contract §3.4 の canonical vector は

```text
W-1, W-2, W-2′, W-3, W-4, W-5, W-6
```

を別成分として持つ。W-2′ は component bijection の単射性と余剰排除を
支える `kind=disjointness` の検査であり、W-2 の ideal equality では
代用できない。

ところが §9 の `covered_procedure_checks` は

```text
..., W-1, W-2, W-3, W-4, W-5, W-6
```

で、**W-2′ を含まない**。それでも `uncovered_checks=[]` になっている。

原因は self-audit の regexp の alternation 順である。

```regex
... | W-[0-9] | W-2′ | ...
```

`W-2′` を読むと、先に `W-[0-9]` が `W-2` までを受理する。次の `′` は
ASCII alphanumeric でないため negative lookahead も通り、
`W-2′` は registry 上 `W-2` に潰れる。独立 probe でも

```text
input "W-2′" -> extracted ["W-2"]
```

を再現した。

これは check completeness の核心に直接反する。`W-2′` 実装を省いても、
current self-audit と conformance set equality は full coverage を返す。

最小修理は次の三点。

```text
1. alternation を W-2′ | W-[0-9] の順にする
   （または W-[0-9](?!′) とする）。
2. contract の covered_procedure_checks に W-2′ を literal 追加する。
3. negative fixture:
     covered から W-2′ を一つ落とす -> check registry equality FAIL
```

manifest 側で W-2 が registry に現れるのは CR-5 自身の列挙を全本文 scan
しているためであり、manifest の実手続きではない。F13 の registry scope
案で併せて除くのがよい。

---

## F7. FAIL B69-4 — `build_record_present=false` の意味が一意でない

manifest v7 は false entry について SB-5 で

```text
build_definition_blob_digest = empty
pinned_input_digests[]       = empty
build_root_id                 = empty
subject_build_binding_digest = empty
```

を許し、I-0c″ (3) は「四欄が空であることを確認」と命じる。

しかし同じ blob の別条文は次を命じる。

- E-9 は build definition / pinned inputs を全 entry で mandatory とする。
- I-0′ は全 entry について D-1 / D-2 / **D-3** を再計算し、preimage
  欠落なら `[11]` とする。false entry の D-3 免除を書かない。
- `build_artifact_set(X)` は全 entry の
  `build_definition_blob_digest` を無条件に union する。

従って false entry \(e\) に対し、

```text
reader A (I-0′):
  D-3 preimage が空 -> 再計算不能 [11]
  または H(empty,[]) != empty build_root -> [12]

reader B (I-0c″ (3)):
  四欄が空 -> PASS
```

という二結果が出る。また empty を `null` や `""` という共通 sentinel
として集合へ入れれば、A/B の両 closure が同じ empty を共有して
I-3d が偽の `[11]` を出す。field omission と読むなら、集合式の
`entry.build_definition_blob_digest` 自体が未定義になる。

このため N-2 は、虚偽 `false` の補償以前に **正直な `false` record を
どう受けるか**が定まっていない。

最小修理形は次である。

```text
E-9':
  top-level と build_record_present=true の entry では
  build_definition_blob_digest / pinned_input_digests[] が mandatory。
  false entry では canonical empty representation を一意に定義する。

I-0':
  D-1 / D-2 は全 entry で再計算。
  D-3 / D-4′ は top-level と build_record_present=true の entry だけで再計算。
  false entry は I-0c″(3) の canonical-empty check だけへ送る。

build_artifact_set(X):
  toolchain_digest / build_step_digests[] は全 entry から取る。
  build_definition_blob_digest / pinned_input_digests[] は
  build_record_present=true の entry からだけ取る。
  null / empty sentinel は集合要素にしない。
```

併せて `build_record_present=false` が provenance の bootstrap leaf なのか、
その場合も E-6 の non-null `toolchain_digest` を再帰的に entry 化するのかを
一文で定める必要がある。現行 E-6 + R-5 + R-6 を全 entry に再帰適用すると、
toolchain の toolchain を無限に要求する読みがあり、有限 manifest の
base case がない。false を leaf とするなら、その leaf で失う保証を
`UNKNOWN` として receipt / EP に送ればよい。

---

## F8. NOTE tier — 次の自然改版で直せばよい項目

以下は単独では freeze を止めない。B69-1〜4 の修理版で同時に直すことを
勧めるが、未修理でも次回の FAIL にはしない。

### N69-1 — spec の meta label

- §8 heading は `監査依頼(v11 — 修理の2点)` のままで、v12 の L/M を
  列挙しない。
- §9 の label は `現行の実装ゲート(v9)` のままだが、直下の exact tuple
  は正しく v12 / v7 / v7。
- §8 の項目番号が 21, 22, 20 の順。

formula と pin は一意なので NOTE。heading を v12、gate label を
`現行の実装ゲート(v12)` とすればよい。

### N69-2 — historical allowlist の範囲

`historical_quotation_refs[]` は、

- spec: self v5..v10（v11 を欠く）、
- contract: predicate v6..v9（v10/v11 を欠く）、
- manifest: self v2..v4（v5/v6 を欠く）

で、実際の版履歴全体を表さない。live refs は正しいため NOTE。
`historical_upper_bound` から範囲を生成し、手書きしない方がよい。

### N69-3 — 軽微な本文同期

- manifest E-7‴ の「§2.2 の**三** hash」は D-1〜D-4′ の**四** hash。
- D-R1 は D-1〜D-3 だけを frozen と書く一方、D-4′ も同じ frozen block。
- D-R4 の `I-0c` は現行 `I-0c″` に直す。
- contract の差分 heading `0.14` / `0.15` は版順と逆。

列挙された式と現行手順から意図は決まるため NOTE。

### N69-4 — Markdown

spec X-5、contract X-5、manifest FA-4 に未閉鎖の `**` があり、
contract §5.3 の public-secondary table も行終端が崩れている。
render の問題で acceptance predicate は変わらない。

### N69-5 — registry の構造範囲

current script は全文 regex のため、差分表の `V3 / T3 / Z3` や
CR-5 自身に書かれた check label まで registry に入る。現行の重大欠落は
F5 / F6 で別途 FAIL にしたが、将来耐性としては「全文」ではなく
明示した `[normative-clause-table]` / `[normative-check-block]` だけから
生成すべきである。

---

## F9. Z-norm receipt 検収

**確認結果: CONFIRMED。**

receipt commit は
`2463a5debd950ca8b4c8770f22532dc2541d70f3`、その親
`61281dc223dd5088d490cd6879c1f8810d328ec0` が operative payload commit
である。親 commit の差分は `docs/znorm_seal_final_v1.md` の許可済み三欄
だけで、

```text
status_on_apply  = "approved / operative"
applied_at       = "2026-07-28T02:20:16Z"
event_receipt_id = "znorm-event-receipt/v1"
```

に限定される。

receipt の八 digest は全て現物と一致した。

| artifact | SHA-256 |
|---|---|
| operative final seal | `3623e0ca5ec7be85edc563ef6c4a3ad5a9dbbef41ea5e37d3814f7add57b8a3f` |
| forall proof | `75e9f072a900d5b66851193aeca153af67d59a7f7265e88893d95f2e53faa20f` |
| K5 migration | `57913283efc1fd2c7748c03bcbcd5e7c410f355ee1216f34bea67c2a8d831dce` |
| apply patches | `8265d395d4c311290a1c1ead01084dd3351409d988c60012f0721e6a51c8c417` |
| BFC v2.15 | `4b46666e7058f8c6c8b3917d8e9de0d0aa43f89825b4101ce7a155dfc0c74268` |
| TB4 v2.5 | `b3ec912b7170fea8fcdcc77c6bca96e944abe676668591ff85c6c28b7388a77a` |
| Rule 1 v1.5 | `861e934be7e309d4cd722874f2b04a9f44f1ab2f7c4f372dc225966813d2f431` |
| manifest K5 v1.7 | `307c57942c1ba9050fc3d9ee424ca812300da41665d39387defc4cbdfc57377d` |

親 commit 以降、これら八 path に変更はない。minted 六 ID も final seal
§9 と一致する。

`provenance/CLAIMS.md` は、

- W3-20 = **採用手続き成立**（数学 claim ではない）、
- W3-21 = **Z-norm-seal-relative paper theorem**
  （無条件でも Lean `verified` でもない）

を別行にしている。K5 migrated まで、K3 / A5 pending、A3 未閉、
Freeze 2 未成立、\(N_\infty\) 未再開という non-implication も receipt と
一致する。便 64 F5 の atomic-apply 条件を満たしている。

---

## F10. freeze / 実装認可の裁定

```text
candidate digests / predecessor digests       = REPRODUCED
self-audit-v3 output                          = 13/13 ALL PASS (candidate only)
math kernel / two-axis / public invariant     = PASS (inherited)
true-record D-4′ binding                      = PASS
TCB four fields []                            = PASS
anchor / pin graph                            = PASS

live exact owner consistency                  = FAIL
document/checker clause-registry fidelity     = FAIL
W-2′ procedure completeness                   = FAIL
false build-record semantics                  = FAIL

predicate_spec_freeze_id                      = NOT ISSUED
freeze_receipt                                = NOT ISSUED
searcher_v2 / checker                         = NOT AUTHORIZED
D-2 generator / verifier A / verifier B       = NOT AUTHORIZED
model_builder                                 = LOCKED

Z-norm event receipt                          = CONFIRMED / UNAFFECTED
```

従って spec self digest、両 governing digest、S5 五 ID、TCB 四欄 `[]`、
実装 scope は candidate 値としては再現したが、approved receipt には
記入しない。

---

## F11. 一往復で閉じるための必須回帰

B69-1〜4 を直した次束では、通常の 13 check に加えて次の五つを
**事前に変異試験**すること。これらが揃えば、N69 NOTE の有無を理由に
さらに返さない。

```text
M69-1  operative blockquote / schema fence に旧 manifest ID を注入
       -> live-version lint FAIL

M69-2  literal row "| **C-6⁗** | ... |"
       -> document-defined registry が exact "C-6⁗" を 1 件抽出

M69-3  covered_procedure_checks から W-2′ だけを削除
       -> procedure registry equality FAIL

M69-4  build_record_present=false の正直な leaf fixture
       -> D-1/D-2 は検査、D-3/D-4′ は免除、empty sentinel は I-3d に入らない

M69-5  同じ fixture を true に反転し D-3/D-4′ 一欄を欠落
       -> digest-mismatch / schema FAIL
```

さらに checker source の regex と文書 CR-1 / CR-5 の regex を別々に
手書きしない。一本の literal definition から文書表示と checker の双方を
生成し、起動時に自己 digest を表示するのが最小である。

---

## F12. ★教材

1. **Markdown の構造は authority 型ではない。** blockquote に入った
   lifecycle 文も、code fence 内の schema も operative になり得る。
2. **checker が文書より賢く補正してはいけない。** `⁗` を script だけが
  理解した場合、PASS は fidelity の証拠でなく仕様逸脱の証拠になる。
3. **長い token を短い token より先に lex する。** `W-2′` の前に
   `W-2` を受理すると、prime を守るための registry が prime を消す。
4. **optional branch を足したら全 consumer を条件分岐させる。**
   schema だけ false を許し、recompute と set projection が無条件のままなら、
   一つの record に PASS と FAIL の両方が出る。
5. **ALL PASS は checker の定理ではない。** 少なくとも一回は
   checker 自身の lexer・除外域・negative mutation を反監査する。

---

## F13. 共同設計者発案

### F13.1 prose 抽出から typed registry へ

clause / check ID を Markdown から推測するのでなく、例えば一つの
versioned data block を正本にする。

```text
registry = {
  clauses: [...literal IDs...],
  checks:  [...literal IDs...],
  historical_ids: [...]
}
```

本文の table ID、conformance record、cross-document reference は全て
この registry から lint する。文書を生成する必要まではなく、少なくとも
「現在の registry と本文抽出が一致する」方向を一つにすればよい。

### F13.2 optional record は四象限 fixture を正本にする

`build_record_present` について

| present | fields | expected |
|---|---|---|
| true | complete | D-3 / D-4′ を再計算 |
| true | missing | [12] |
| false | canonical empty | leaf / UNKNOWN として受理 |
| false | nonempty | [12] |

を仕様表として置き、E-9、I-0′、I-0c″、build-face projection はこの表を
参照する。分岐を prose 四箇所で別々に説明しない。

### F13.3 FAIL の定義を今後の常設 gate にする

今後は次のいずれかを変える指摘だけを freeze-blocking FAIL とする。

```text
theorem truth / accepted universe / integrity-stop routing /
authority owner / conformance completeness / valid instance representability
```

それ以外は NOTE とし、次の自然改版へ送る。厳密さを落とすのではなく、
研究を止める権限を意味論的影響のある指摘だけに限定する。

---

## F14. 監査範囲外申告

### 本便で行ったこと

- 便 69 の section 0〜5 全文、対話帳 T-17 まで、研究目的書の読解。
- spec v12 / contract v7 / manifest v7 の全文紙上監査。
- target / HEAD / worktree、SHA-256、predecessor digest、bytes、LF、
  CR / TAB / C0 / BOM の照合。
- self-audit v3 の再実行と、lexer / structure classifier / registry の
  独立反監査。
- clause ID、procedure check、D-4′、false branch、四面交差、
  TCB、anchor、pin、lifecycle の敵対的検分。
- Z-norm receipt commit / parent、atomic three-field apply、八 digest、
  minted IDs、W3-20 / W3-21、non-implication の照合。

### 本便で行っていないこと

- searcher、checker、generator、verifier A/B、Model-Builder の実装。
- 実 dependency closure、build attestation、EP、receipt の生成。
- sealed candidate、旧 8 hit、具体係数、raw shard への接触。
- GAP 探索、Lean 証明書、数値探索。
- N∞ freeze ID / commander receipt の発行。

作業開始時から存在した対象外の
`docs/mb_ninfty_verifier_contract_v6.md`、
`docs/week4-NInfty_stage2_spec_v11.md`、`out*.txt` は変更・削除していない。
本便の新規変更は指定返信ファイルだけである。本監査は paper audit であり、
Lean の意味での `verified` ではない。

---

# R. 反省文

研究リーダーの進言は、「監査を甘くせよ」ではなく、**監査の厳しさを
研究成果へ結びつく場所に使え**という指示だと理解した。仕様の一文字が
false acceptance を許すなら止めるべきだが、意味が一意なまま残った見出しの
版番号まで同じ強さで止めれば、監査が数学を守る手段から版更新を生む目的へ
反転する。私の役割は文書の無欠性そのものを最大化することではなく、
誤った定理・汚染された独立性・再現不能な証拠が研究者の判断へ入るのを
防ぎ、同時に数学の前進速度を守ることだ。

便 65〜68 が四往復になった原因は、著者側の修理が次の層に新しい同期面を
作ったことだけではない。私にも寄与がある。第一に、私は各便で見えた
blocker を深く掘った一方、最初から bundle 全体に対して
「不正な物が通るか」「正直な物が表現できるか」「一 field を替えても
判定が変わらないか」「optional 分岐に base case があるか」という
end-to-end の反例表を先に作らなかった。D-3 の再計算、build face、
subject binding を順番に発見したのは、同じ record flow を初回に最後まで
通さなかった私の検査順にも原因がある。

第二に、「binding」「coverage」「live reference」という言葉に要求する
機械的な合格条件を早い便で逐語化し切らなかった。後から最小修理文を出すと
一往復で閉じたが、それ以前は著者が概念を満たしたつもりでも、私が次の便で
別の読みを攻撃する余地が残った。第三に、operative owner の型不一致と、
意味を変えない meta label の古さを同じ freeze-blocking の箱へ入れがち
だった。前者を止めた判断は維持するが、後者まで毎回 exact artifact の
再発行理由にしたことは、同期面と往復を増やした私側の過剰である。

次便から運用を次のように変える。

まず監査の最初に、数学・受理集合・独立性について end-to-end countermodel
を作る。次に machine contract と checker の fidelity を、checker 自身とは
別の小さい probe と negative mutation で見る。文言・履歴・render の sweep
は最後に回し、意味論への影響がなければ NOTE にする。時間の重心は概ね
数学と反例 70%、実装契約 20%、文書同期 10% とする。既に PASS した不変部分は
差分が無い限り再審理せず、浮いた資源を証明の依存、量化、反例、UNKNOWN の
境界へ使う。

また、最初の blocker を見つけてもそこで発見フェーズを終えず、同じ便で
全分岐・全 consumer・正負 fixture まで走査してから返信する。各 FAIL には
「判定をどう変えるか」「最小修理文」「修理を一撃で検収する negative
fixture」を必ず添える。FAIL は theorem truth、accepted universe、
integrity routing、authority owner、conformance completeness、valid
instance representability のいずれかを変えるものに限定する。それ以外は
NOTE とし、NOTE だけを理由に往復を要求しない。

この変更によって監査の水準を下げるつもりはない。むしろ、整形上の雑音を
機械へ移し、私の判断を「この穴から誤った数学が通るか」という問いへ
集中させる。以後の便では、この約束どおり FAIL/NOTE の境界、発見の
一括性、反例と最小修理の有無で自分の仕事を点検する。
