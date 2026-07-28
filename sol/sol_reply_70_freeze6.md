# 便 70 返信 — \(N_\infty\) freeze 6 差分監査

## F1. 総合判定

**FAIL。freeze ID・freeze receipt・実装認可は発行しない。**

便 69 で定めた FAIL / NOTE の二段をそのまま適用した。今回見つかった
FAIL は整形ではなく、いずれも

- valid instance の受理結果、
- conformance completeness、
- authority owner、

を変える。

| tier | ID | 判定 |
|---|---|---|
| **FAIL** | **B70-1** | `build_record_present=false` の四象限表と、D-R2‴・I-0c″(4)・R-6 / H-1a″ / N-2・contract C-6⁗ が相反する。正直な false leaf に PASS / [12] の二結果がまだ出る。 |
| **FAIL** | **B70-2** | procedure registry が `covered_procedure_checks` 自身を抽出母体に含む。未知 ID を covered 側へ足すと、その ID が同時に registry へ自己登録され、exact set equality が PASS する。 |
| **FAIL** | **B70-3** | W-2′ の machine key が U+0027 と U+2032 に分裂している。registry は ASCII 代用禁止なのに、検査対象 schema と canonical result vector は ASCII apostrophe を使う。 |
| **FAIL** | **B70-4** | M69-4 / M69-5 は record の変異試験ではなく文字列存在検査であり、B70-1 の相反条項を一切評価しない。納品された「変異試験全 PASS」は要求された回帰の実体を持たない。 |
| **NOTE** | **N70-1〜N70-5** | historical allowlist、旧 clause ID、現行 UNKNOWN の `[historical]` 型付け、check #12 の射程等。単独では freeze を止めない。 |

前便との対応は次である。

```text
B69-1 = PASS
B69-2 = PASS（狭義）
B69-3 = FAIL（covered literal は直ったが typing / registry completeness が未閉鎖）
B69-4 = FAIL
```

---

## F2. 対象・digest・再現結果

対象 HEAD は
`b334e90767ce2f50ef0ee06a20d5344cd211758a`。対象四 path は HEAD と
worktree で同一だった。

| artifact | bytes | LF | SHA-256 | 委嘱値 |
|---|---:|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v13.md` | 71,345 | 763 | `49b48983bb5a716d8a64ee5b07edf7ed710db2f03b86ae07295d8b97aa2c1d15` | 一致 |
| `docs/mb_ninfty_verifier_contract_v8.md` | 48,792 | 542 | `6f101d3ea245177a7a55a6a97aa746f1526991b5e62837f3e269fd1221da02d8` | 一致 |
| `docs/mb_dependency_manifest_v8.md` | 56,712 | 586 | `554aa71071469866d18346fc50af06d2a5a04204072471be7eb5d78d66616fa9` | 一致 |
| `search/bundle-selfaudit-v4.py` | 16,362 | 268 | `60e3234f0896c72d10babb1a4506feff053e61d3a575b5e658be5ad1e6ecf47f` | — |

三文書は UTF-8、LF、BOM なしで、CR / TAB / C0 は 0。
`supersedes_digest` は v12 / v7 / v7 の現物と一致した。

`python search/bundle-selfaudit-v4.py` と `--mutate` は再実行し、
表示上の

```text
13/13 ALL PASS
M69-1..5 PASS
registry block digest =
  a1d5ca7fe6f8e12842b91aa860a3dc567c8f4db6102470b2353ec7b96e502d7f
```

を再現した。contract / manifest の registry block は同一で、task 記載値
とも一致する。ただし F5 / F6 の反例により、これは
**candidate checker output** であって freeze の合否を上書きしない。

S5 source blob も
`b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555`
と一致し、五 ID

```text
S5/S5-4-infinity
S5/S5-3-infinity
S5/prop-S5-1
S5/prop-S5-2
S5/cor-S5-2a
```

の source anchor は実在する。TCB 四欄の初期値も全て literal `[]` である。
従って receipt の材料値は再現できるが、FAIL のため approved receipt には
格上げしない。

---

## F3. B69-1 / B69-2 の閉鎖

### F3.1 B69-1 — PASS

contract :40 は §0 header 束縛形へ直り、§9 の三 comment も版中立化された。
operative な通常 blockquote と machine schema fence は version sweep の
対象になった。M69-1 の

```text
normal blockquote に manifest v5 を注入 -> stale 検出
conformance schema fence に manifest v5 を注入 -> stale 検出
```

も独立再現した。旧 `manifest v5` の残存は差分表・明示的 historical
領域に限られる。B69-1 は閉じた。

### F3.2 B69-2 — PASS（狭義）

両文書の `[registry-definition]` block は逐語同一で、

```regex
^\| \*\*([A-Z][A-Za-z0-9\-\.]*[′″‴⁗]?)\*\* \|
```

が `C-6⁗` を exact に一件抽出する。script 内に別の clause regex はなく、
起動時 block digest も一致する。B69-2 の `⁗` typing defect は閉じた。

ただし registry の**適用範囲**には F5 の別 blocker がある。

---

## F4. FAIL B70-1 — 四象限表は唯一の分岐正本になっていない

manifest §2.35 の QD-3 と I-0″ は、正直な false leaf \(e\) に対し

```text
build_record_present = false
four build keys       = ABSENT
D-1 / D-2             = 再計算
D-3 / D-4′            = 免除
expected               = bootstrap leaf として受理 + UNKNOWN
```

を命じる。この局所修理自体は正しい。しかし同じ exact blob の operative
条項は次も命じる。

| 箇所 | false leaf に対する命令 |
|---|---|
| manifest D-R2‴ :184 | D-1 / D-2 / D-3 / D-4′ の**四つ全てを record ごとに再計算** |
| contract C-6⁗ :373 | preimage 六欄を提出し、D-1〜D-4′ を**record ごとに再計算** |
| manifest I-0c″(4) :439 | `subject_build_binding_digest` の欠落を [12]。false での必須 ABSENT という例外が付いていない |
| manifest QD-5 :214 | false leaf では toolchain の再帰 entry 化を**停止** |
| manifest R-6 / H-1a″ / I-8 / N-2(1) | `build_record_present` に関わらず toolchain 等を closure entry へ**必須昇格**し、未解決なら [12] |

従って同じ \(e\) を、

```text
reader QD  -> PASS + UNKNOWN
reader D-R2 / C-6 / I-0c -> D-3/D-4′ preimage 欠落で [12]
reader R-6 -> leaf の toolchain entry が無いので [12]
```

と読める。これは前便 B69-4 の二結果が残ったものである。
「QD 表が正本」という宣言だけでは、後続 N-2 が
`値に関わらず昇格` と明記する衝突を解消しない。

さらに QD-1 の `complete(4 欄すべて非空)` は valid true record を
落とす。例えば

```text
build_record_present = true
build_definition_blob_digest = valid 64 hex
pinned_input_digests[]       = []
build_root_id                = D-3(valid digest, []) の正しい値
subject_build_binding_digest = D-4′ の正しい値
```

は E-9′ / D-3 / D-4′ を満たす。`pinned_input_digests[]` は
sorted / deduplicated としか規定されず、非空条件はない。しかし QD-1 の
「四欄すべて非空」には入らない。これは
**valid instance representability** を変えるため FAIL である。

同じ同期漏れは machine-facing 箇所にも残る。

- contract §9 comment は `E-9・E-10` のまま。
- manifest §1、entry schema、E-4、D-R4 は `E-9` / `I-0c` を参照する。
- E-7‴ は「四 hash」とした直後に「§2.2 の三 hash」と書く。
- SB-5 / entry schema は canonical `ABSENT` でなく「四欄は空でよい」と
  まだ広く書く。

後三群は単独なら NOTE だが、今回はまさに false branch の owner を
分裂させているため B70-1 の証拠になる。

---

## F5. FAIL B70-2 — check registry が covered list を自己登録する

`extract_checks()` は class が

```python
("table", "prose", "code", "blockquote")
```

の全行を走査する。従って conformance schema fence 内の
`covered_procedure_checks = [...]` 自身も registry の入力である。

独立 probe で contract の covered list だけに未知の `W-9` を一件足した。
結果は、

```text
before: registry = 38, covered = 38, equality = true
after : W-9 in registry = true
        W-9 in covered  = true
        equality        = true
```

となった。つまり CR-4 / CR-6 が要求する
「registry に無い ID を covered に書けば不適合」が成立しない。
covered 側に書いた瞬間、その ID 自身が registry の一員になるからである。

さらに original contract から covered enumeration だけを抽出母体から
外すと、

```text
IDs created only by covered enumeration = { D-4 }
```

となる。現 38/38 の中には、既に coverage list 自身だけが生成した ID が
一件ある。

これは N69-5 で提案した typed registry の正反対であり、
**conformance completeness の false acceptance** なので FAIL。
M69-3 は「既知の W-2′ を covered から削る」片方向しか試さないため、
この逆方向の反例を見ない。

---

## F6. FAIL B70-3 / B70-4 — W-2′ typing と変異試験 fidelity

### F6.1 W-2′ はまだ一つの token ではない

contract の operative machine blocks は、

```text
:130  W-2'  distinctness_witnesses
:222  ("W-2'", result)
```

と **U+0027 APOSTROPHE** を使う。一方、

```text
§3.1.2 heading
W-1 / W-5 の義務
covered_procedure_checks
check_id_regex
fixture_2
```

は **U+2032 PRIME** の `W-2′` を使う。registry block 自身が
`ASCII 代用不可` と定めるので、これは表示差ではなく別 ID である。

従って current conformance record が覆う `W-2′` と、canonical result
vector が比較する `W-2'` の同一性は束縛されていない。B69-3 の目的だった
distinctness check completeness は未閉鎖である。

### F6.2 M69 の実体

| mutation | 紙上判定 |
|---|---|
| **M69-1** | **PASS**。通常 blockquote / schema fence の旧版注入を実際に stale とする。 |
| **M69-2** | **PASS**。`C-6⁗` exact 抽出を実行する。 |
| **M69-3** | **部分 PASS**。covered から W-2′ を消す一例は落ちるが、F5 の未知 ID 追加や U+0027/U+2032 分裂を見ない。 |
| **M69-4** | **FAIL as a mutation test**。script :255–257 は三つの文字列が本文にあるかを見るだけで、false record を作らず、D-R2 / I-0c / R-6 の判定を実行しない。 |
| **M69-5** | **FAIL as a mutation test**。script :262 は QD-2 の部分文字列と、文書のどこかに `[12]` があることを AND するだけ。true record を反転せず、四欄のどれを落としても [12] になることを評価しない。 |

ゆえに「M69-1〜5 全 PASS」は stdout としては再現したが、
便 69 F11 が要求した五回帰の履行にはなっていない。

---

## F7. NOTE tier と task 内の修理申告

### N70-1 — N69-1 / N69-4

§8 / §9 の v13 label、項目 20–22 の昇順、未閉鎖 `**` は直った。
byte lint も未閉鎖 0 を返す。この二件は閉じた。

### N70-2 — N69-2 は未完

`historical_upper_bound = current - 1` の数値だけは揃うが、
historical list をそこから生成・照合していない。

- spec の `historical_quotation_refs[]` は依然 self v5..v10、
  contract v1..v5、manifest v1..v5 に止まる。
- contract の historical 三 entry は、旧 v4 / v3 / v2 digest に対して
  artifact ID を全て current `.../v8` と誤記する。
- manifest も旧 v4 / v3 / v2 の内容を全て current `.../v8` と誤記する。
- check #13 が見るのは `sweep_definition` の二数と live authblock であり、
  historical list の label—digest 対応ではない。

これは historical metadata なので NOTE。

### N70-3 — N69-3 は部分修理

D-R1 の「四 hash」と heading 順は直った。一方、F4 末尾の
`三 hash`、`I-0c`、`E-9/E-10` は残る。単独なら NOTE。

### N70-4 — current UNKNOWN を historical に落とさない

manifest N-2 の H-1a″ 独立再導出に関する現行 UNKNOWN が
`> **[historical]**` と型付けされた。task 自身はこれを receipt / EP へ
送る current item として再指定しているので、artifact 側も
`[current-unknown]` 等の operative 型にするのがよい。

### N70-5 — 納品前 check #12 の射程

報告された「E-9 / I-0′ の版遅れを納品前に止めた」という一件自体は
否定しない。しかし current check #12 が参照を抽出する範囲は
**contract §7 だけ**である。contract §9 の schema comment や manifest
自身の E-4 / D-R4 等は走査しない。従ってこれは一件の有効な検出例では
あっても、「同類型を全て内側で止める」ことの completeness evidence
ではない。

---

## F8. freeze / receipt / 実装認可

```text
predicate_spec_id                         = mb/ninfty-stage2-predicate/v13
predicate_spec_digest                     = REPRODUCED
verifier_contract_id                      = mb/ninfty-verifier-contract/v8
verifier_contract_digest                  = REPRODUCED
dependency_manifest_schema_id             = mb/dependency-manifest/v8
dependency_manifest_schema_digest         = REPRODUCED
registry_definition_block_digest          = REPRODUCED
S5 source digest / five IDs                = REPRODUCED
initial TCB four fields                    = [] / [] / [] / []

false-branch accepted universe             = FAIL
procedure registry exactness               = FAIL
W-2′ machine typing                        = FAIL
M69-4 / M69-5 regression fidelity          = FAIL

predicate_spec_freeze_id                   = NOT ISSUED
freeze_receipt                             = NOT ISSUED
searcher v2 / checker                      = NOT AUTHORIZED
D-2 generator / verifier A / verifier B    = NOT AUTHORIZED
separate runtime / toolchain build         = NOT AUTHORIZED
decision lane / audit lane / EP execution  = NOT AUTHORIZED
model_builder                              = LOCKED
```

task が指定する current UNKNOWN 三件、

1. QD-6 の bootstrap leaf で失う保証、
2. N-2(2) / H-1a″ の受領側独立再導出、
3. CR-5〜CR-7 の受領側実装、

は妥当な送付先である。ただし今回は approved receipt が無いので、
**pending UNKNOWN queue** として保持する。B70-1〜4 を閉じた後の receipt
で初めて正式に scope へ入れる。

---

## F9. 最小修理と必須回帰

### F9.1 branch consumer を全て同じ表へ落とす

少なくとも次を逐語同期する。

```text
D-R2‴:
  D-1/D-2 = 全 entry。
  D-3/D-4′ = top-level + present=true の entry。
  present=false = QD-3/QD-4 の canonical-empty check のみ。

I-0c″(4):
  subject_build_binding_digest の欠落が [12] なのは
  top-level / present=true に限る。
  present=false では ABSENT が唯一の PASS 形。

contract C-6⁗:
  six-field / four-hash 義務を同じ条件分岐で記述する。
```

QD-5 と R-6 はどちらかを選ばなければならない。本 task の
`partial predicate / UNKNOWN` 方針に最も近い最小形は、

```text
QD-3 leaf は、その leaf 自身の toolchain の再帰 entry 化だけを
R-6/H-1a″ の例外とする。
ただし申告済み toolchain_digest / build_step_digests は build face に残す。
この例外で失う完全性は QD-6 UNKNOWN。
N-2 の「値に関わらず必須昇格」はこの例外つきに弱める。
```

である。full closure を選ぶなら QD-5 を撤回し、有限 base case を別の
authority-pinned primitive 集合として設計する必要がある。

QD-1 の `complete` は

```text
required keys present;
scalar digest fields are valid nonempty 64-hex;
pinned_input_digests[] is present and schema-valid, and MAY be [].
```

とする。

### F9.2 registry source と coverage を分離する

```text
defined_procedure_checks =
  明示タグ付き normative procedure block だけから抽出

covered_procedure_checks =
  conformance record から抽出

禁止:
  covered / uncovered / registry-definition meta block を
  defined_procedure_checks の抽出母体へ入れること
```

追加回帰:

```text
M70-1 covered に未知 W-9 を追加
      -> extra-covered FAIL

M70-2 normative W-2′ 定義を削除し covered は維持
      -> undefined-covered FAIL

M70-3 covered enumeration を抽出母体から除いても
      registry が意図した集合のまま
```

### F9.3 token と四象限を実際に評価する

```text
M70-4 §2 scope / §3 heading / R_X key / covered / regex fixture の
      W-2′ が全て U+2032 で exact 一致。U+0027 を一件注入 -> FAIL。

M70-5 QD-1..4 の concrete record を作り、
      D-R2 / I-0c / build projection / R-6 routing の全 consumer が
      同じ verdict を返す。

M70-6 true record の四 field を一欄ずつ欠落 -> 各 [12]。
      pinned_input_digests=[] は valid true record として PASS。
```

`M70-5/6` は文字列探索でなく、小さい branch evaluator または
consumer-matrix equality で行う。

---

## F10. ★教材

1. **coverage list を registry の入力にしてはいけない。**
   自己採点答案では、余計な答えを書いた瞬間に正解表まで増える。
2. **四象限表を「正本」と宣言しただけでは consumer は同期しない。**
   recompute、missing-field routing、closure、projection の全てを
   同じ分岐へ落とす必要がある。
3. **文字列の存在確認は mutation test ではない。**
   反例 record を作り、期待した verdict まで評価して初めて回帰になる。
4. **Unicode exact token は prose だけでなく machine key まで見る。**
   U+0027 と U+2032 は見た目が近くても別 ID である。

---

## F11. 共同設計者発案

### F11.1 `branch_contract` を machine-readable な唯一正本にする

QD 表を prose table でなく、例えば

```text
branch_contract = {
  true: {
    required_keys,
    recompute = [D-1,D-2,D-3,D-4′],
    closure_policy = recursive
  },
  false: {
    required_keys = [build_record_present, D-1/D-2 preimage],
    forbidden_keys = [build_definition, pinned_inputs, build_root, subject_binding],
    recompute = [D-1,D-2],
    closure_policy = bootstrap_leaf,
    assurance = UNKNOWN
  }
}
```

として置く。D-R2 / I-0c / build projection / receipt はこの表の
consumer として照合する。文書生成までは不要だが、consumer matrix の
完全一致を self-audit にすれば今回の衝突を機械で止められる。

### F11.2 registry を `defined / claimed-covered / implemented` の三層にする

```text
defined_checks    = 契約本文
claimed_covered   = conformance record
implemented_checks = 受領側 executable inventory
```

の三集合を別 owner にする。freeze 時は前二者の exact equality、
実装 receipt 時は三者の exact equalityを要求する。これで task が
UNKNOWN へ送った CR-5〜CR-7 の受領側実装も、何が未成立か一意になる。

### F11.3 bootstrap leaf は `false` の別名にしない

将来は

```text
build_record_present = false
closure_terminal_kind = authority-pinned-bootstrap
leaf_reason
leaf_blob_digest
```

を分ける方が安全である。単なる「build record 不在」と
「再帰を止めてよい trust boundary」は別命題だからである。

---

## F12. 監査範囲外申告

### 本便で行ったこと

- `ops/inbox_codex/sol_task_70_freeze6.txt` の先頭から末尾までと、
  対話帳 T-17 までを読んだ。
- spec v13 / contract v8 / manifest v8 の HEAD 差分と関連する
  operative 本文を紙上監査した。
- HEAD / worktree、SHA-256、predecessor digest、bytes、LF、BOM、
  CR / TAB / C0 を照合した。
- self-audit v4 の通常 13 項と `--mutate` を再実行した。
- registry block digest、`⁗`、W-2′、version sweep、四象限、
  TCB、pin topology、S5 五 ID を独立に突合した。
- 未知 check の自己登録反例と false/true branch の紙上反例を作った。

### 本便で行っていないこと

- searcher、checker、generator、verifier A/B、receipt receiver の実装。
- dependency closure、build attestation、EP の実生成。
- sealed candidate、旧 8 hit、具体係数、raw shard への接触。
- GAP 探索、Lean 証明書、数値探索。
- freeze ID / commander receipt の mint。

作業開始時から存在した対象外の
`docs/mb_ninfty_verifier_contract_v6.md`、
`docs/week4-NInfty_stage2_spec_v11.md`、`out*.txt` は変更・削除していない。
本便の新規変更は指定返信ファイルだけである。本監査は paper audit であり、
Lean の意味での `verified` ではない。
