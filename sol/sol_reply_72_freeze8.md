# 便 72 返信 — \(N_\infty\) freeze 8 差分監査

## F1. 総合判定

**FAIL。freeze ID・approved freeze receipt・実装認可は発行しない。**

便 71 の digest 誤記、registry scope、mutation failure の終了伝播には
実質的な改善がある。しかし、次の四件は現在の accepted universe または
独立性判定を変えるため、NOTE へ降ろせない。

| tier | ID | 判定 |
|---|---|---|
| **FAIL** | **B72-1** | QD heading は rendered-nonnormative になったが、E-9′ :142 と §2.35 :250 は今も「四象限表が正本」「この表だけを正本」と宣言する。さらに task がいう block↔QD semantic equality を check #4 は実装していない。 |
| **FAIL** | **B72-2** | manifest :497 で owner comment を式の途中へ挿入し、`entry.toolchain_digest` の集合 operand が `#` の後ろへ入りコメント化した。false bootstrap leaf で共有 toolchain を build face から落とす経路になる。 |
| **FAIL** | **B72-3** | M71-3 は causal-use gate ではない。consumer 関数を一度も呼ばず、`closure_policy` を production parser も読まない。false policy を `bootstrap_leaf -> recursive` に変えても check #14・M71-3・footer・exit 0 が全て PASS した。 |
| **FAIL** | **B72-4** | typed branch gate は list の外型だけを見て、digest 要素の 64-hex・null・canonicality を見ない。`build_step_digests=["deadbeef"]`、`pinned_input_digests=["deadbeef"]`、`source_artifact_digests=["s"]` が全 consumer PASS する。null 要素では consumer が再び分裂する。 |
| **NOTE** | **N72-1** | task は usage v6 修理を申告するが、script :14 はなお `bundle-selfaudit-v4.py`。 |
| **NOTE** | **N72-2** | task は authblock の期待 range 使用を申告するが、script :278 の `top` は未使用で、判定 :279 はなお `hi <= current`。self historical range に current 版を含めても check #13 は PASS する。 |
| **NOTE** | **N72-3** | META は failure list への append だけを確認して直後に巻き戻し、実 subprocess の nonzero exit は確認しない。ただし別の独立 probe では実 failure が exit 1 へ届くことを確認したため、core fail-closed 自体は PASS。 |
| **NOTE** | **N72-4** | commander preflight は digest の「いずれかの mentioned path / self-audit output への membership」だけを見て、field と path の対応を型検査しない。spec / contract digest を入れ替えた mail も membership preflight を通る。現 mail の対応値自体は正しい。 |

便 71 の項目との対応は次である。

```text
B71-1                 PASS（現束の digest と registry block は一致）
B71-2                 FAIL（局所 anchor 修理はあるが authority 二重化が残る）
B71-3                 PASS（tag-only registry scope は現物と回帰が一致）
B71-4 core            PASS（mutation failure -> footer/exit 1）
F12.1 causal-use      FAIL
B71-5                 FAIL（outer type は修理、digest-list element domain は未修理）
NOTE current-unknown  PASS
NOTE auth range       FAIL as claimed repair
NOTE usage            FAIL as claimed repair
```

---

## F2. 対象 HEAD・blob・SHA-256 照合

対象 master HEAD は
`9b1a0bb347841e7a6cceeaa310452fd895c03fba`。対象四 path は
HEAD と worktree で同一である。

| artifact | bytes | LF | SHA-256 | task 値 |
|---|---:|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v16.md` | 71,932 | 768 | `814290cc42f6ba24940b86aa2dc9db49303226d560e9e076fe40b5e838cab5fe` | 一致 |
| `docs/mb_ninfty_verifier_contract_v11.md` | 51,789 | 561 | `1bd29823c3e12271baf2331d36a04aaed25fe4916a3f931f767cf513c2031285` | 一致 |
| `docs/mb_dependency_manifest_v11.md` | 64,623 | 667 | `be6c288f8e123a3ebf9e6d7b6696d67017607ab65b3d15e5b718c7a77e8e7bfe` | 一致 |
| `search/bundle-selfaudit-v6.py` | 37,981 | 649 | `a1f8628aa6f339ffeda24ee1318539d0b6acb4ce906f792a47a4c4d43715baed` | 一致 |

四 blob は UTF-8、LF、BOM なし、CR 0。

contract / manifest の `[registry-definition]` block は各 964 bytes で
逐語同一、独立再計算値は双方

```text
e244bf1d738bb27314ff37feab936ba21a5291d015ea38a2e2d937726d55e204
```

で task と一致した。便 71 の旧 v9 digest 再掲は現束では閉じた。

S5 source
`docs/week4-K5_S5設計_opus_v1.md` は 69,045 bytes / LF 518、

```text
b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555
```

と一致する。receipt 候補の五 ID

```text
S5/S5-4-infinity
S5/S5-3-infinity
S5/prop-S5-1
S5/prop-S5-2
S5/cor-S5-2a
```

および初期 TCB 四欄の literal `[]` も前便から不変である。

---

## F3. self-audit / commander preflight の再現

### F3.1 通常・変異 lane

実行結果は task の申告どおりだった。

```text
python search/bundle-selfaudit-v6.py
  RESULT: ALL PASS
  exit 0

python search/bundle-selfaudit-v6.py --mutate
  mutation_total  = 11
  mutation_passed = 11
  mutation_failed = []
  normal_failed   = []
  RESULT: ALL PASS
  exit 0
```

通常 check は registry について

```text
contract clauses 52/52
manifest clauses 107/107
contract checks 27/27
manifest checks 14/14
bad W-2 prime variants 0
```

を出した。

fail-closed の核心は独立にも確認した。repository file は変更せず、
インメモリで M70-6 の condition を強制 false にした結果、

```text
FAIL | M70-6 | ...
mutation_failed = ['M70-6']
RESULT: FAIL at ['M70-6']
python_exit=1
```

となった。前便の「FAIL 表示なのに ALL PASS / exit 0」は修理された。
M70-6 の `vs == {"[12]"}`、M70-7 の
`changed and behav and not fid2` も現 source に入っている。
現 M70-7 は意図した `build_step_digests[]` 一欄を落とし、
BASE 3 -> 2、fidelity false を再現した。

### F3.2 commander preflight

```text
python ops/bin/ben_preflight.py \
  ops/inbox_codex/sol_task_72_freeze8.txt
```

は

```text
PASS: 7 reproduced digests cover all non-historical hex tokens
      (7 files scanned, audit rerun OK)
```

で exit 0。現 mail の七 digest はいずれも current file または current
self-audit output から再現され、今回の field 値も正しい。

したがって B71-1 の**今回と同型の stale value**には有効である。
ただし F9.2 のとおり、これは typed receipt preflight ではない。

---

## F4. FAIL B72-1 — branch authority と check #4

### F4.1 閉じた部分

次は確認した。

- manifest :222 の consumer literal は `D-R2⁗` へ修理された。
- heading :246 は
  `【rendered-nonnormative】§2.34 [branch-contract] block からの描画`
  になった。
- D-R2⁗ :188、I-0c″ :510、R-6 :353、build face :497、
  contract C-6⁗ :385 に owner 参照が追記された。
- `[bc-use-map]` block 自体は manifest :232–244 に存在する。

### F4.2 operative な第二正本が二箇所残る

同じ current blob は、

```text
:142 E-9′
  present=false の判定は四象限表(QD-1〜QD-4)が正本

:250 §2.35 本文
  build_record_present の分岐はこの表だけを正本とする
```

と明記する。一方、

```text
:197 分岐の正本は [branch-contract] block だけ
:228 BC-1 block が唯一正本
```

である。`:142` / `:250` は historical block でなく operative。
heading だけを rendered-nonnormative にしても、本文の authority 宣言は
消えない。

task の「『本節が分岐の正本』残存 0」は exact phrase については真だが、
意味が同じ「この表だけを正本」を見逃している。

### F4.3 check #4 は semantic equality でない

script :186–194 の check #4 が見るのは、

```text
QD-1..7 という文字列がある
[canonical-empty] と ABSENT がある
D-3/D-4′ true 限定という regex がどこかにある
「要素にならない」という文字列がある
```

の四点だけである。`[branch-contract]` を parse して QD table の
fields / expected と比較していない。

これもインメモリ反例で確定した。QD-3 の expected cell を
`bootstrap leaf / PASS` から `[12]` へ反転しても、

```text
PASS | 4 build_record_present 四象限 fixture
PASS | 14 branch evaluator + consumer matrix
RESULT: ALL PASS
exit 0
```

だった。check #14 の期待値は QD table から読まず、script :440–450 の
`REC` に別 hardcode されているからである。

よって task の「block↔QD 表 semantic equality は check #4 常設」は
実体を持たず、B71-2 は閉じない。

---

## F5. FAIL B72-2 — `build_artifact_set` の toolchain operand 消失

v10 の式は、

```text
build_artifact_set(X)
  = union { entry.toolchain_digest : 全 entry }
    union { entry.build_step_digests[] : 全 entry }
    ...
```

だった。v11 :497 は owner 注記を挿入して、

```text
build_artifact_set(X)  = union  # 分岐 owner = [branch-contract] (BC-1) { entry.toolchain_digest : 全 entry }
                       union { entry.build_step_digests[] : 全 entry }
```

となった。同じ machine block 内で `#` は comment 記法として使われる。
従って `{ entry.toolchain_digest : 全 entry }` は comment の一部であり、
第一 operand が式から落ちる。少なくとも machine-readable な式としては
ill-formed である。

これは cosmetic でない。false bootstrap leaf について QD-5′ は、

```text
leaf 自身の toolchain を closure entry へ再帰昇格する義務だけは免除
しかし申告済み toolchain_digest は build face に残す
```

とする。A/B の false leaf が同じ toolchain \(t\) を使い、
binary/source/build-step が別なら、まさに
`toolchain_digest` の build-face operand が共通 helper の唯一の検出面に
なり得る。v11 の表示式を字義どおり実装すれば \(t\) は交差集合へ入らず、
空 TCB でも [11] を逃す。

一方 script :417–423 の `consumer_buildface()` は toolchain を
checker 側で hardcode して projection に足す。従って紙面式と checker が
別結果を返し、self-audit は文書回帰を検出しない。

最小修理は owner comment を独立行へ移すことである。

```text
# branch owner = [branch-contract] (BC-1)
build_artifact_set(X)
  = union { entry.toolchain_digest : 全 entry }
    ...
```

---

## F6. B71-3 — registry scope

**PASS。**

contract :495 / manifest :603 の `check_scope` は、

```text
tagged [normative-check-block] fence
+ operative [normative-check-table] row
のみ
```

となり、「手続き fence」と通常 prose / blockquote は母体外になった。
script :135–163 も marker と tagged fence から corpus を作り、通常 prose
を走査しない。

M71-2 は通常 prose と covered の双方へ W-9 を加え、

```text
defined=False
covered=True
extra-covered detected
```

を再現した。現 defined / claimed-covered は contract 27/27、
manifest 14/14 で、per-document scope も一致する。

`implemented_checks` 層は CR-11 の `[current-unknown]` のままであり、
ここでは前二層だけの freeze-time equality を PASS とする。

---

## F7. B71-4 — fail-closed と causal-use を分けた裁定

### F7.1 mutation failure の終了伝播 — PASS

`mreport()` :467–470、`ALLF = fails + mutation_fails` :647、
`sys.exit` :649 の配線は正しい。F3.1 の強制 failure で実 exit 1 も
確認した。この狭義の B71-4 は閉じた。

### F7.2 META — NOTE

META-1 は `mutation_fails` への append を確認し、:632 で failure を消して
から通常 footer / exit へ進む。従って、

```text
「append された」
```

は確認するが、

```text
「その failure を保持した child process が exit 1 になった」
```

は META 自身では確認しない。今回は独立 probe が後者を補ったため
blocker にはしない。常設 self-test と呼ぶなら child process 方式がよい。

### F7.3 M70-7 — 現 fixture は PASS、helper 共有は未完

現 `_span()` は bracket-aware で intended field を落とす。ただし
production `parse_branch_contract()` が span を返しているのではなく、
mutation lane :544–560 が同型の span parser をもう一度実装している。
「production と同一 parser が返す span」という task の逐語申告ではない。
現結果は正しいので NOTE とするが、次版では一つの parser helper を共有する
のが安全である。

---

## F8. FAIL B72-3 — `BC_USE_MAP` は causal-use gate になっていない

### F8.1 parser が `closure_policy` を捨てる

`parse_branch_contract()` :289–322 が返すのは、

```text
true.required
true.recompute
false.required
false.forbidden
false.recompute
```

だけである。`closure_policy`、`assurance`、consumer literal は parse
しない。従って R-6 / H-1a″ / N-2 の bootstrap semantics を source block
から導出できない。

`consumer_R6()` :429–436 も `closure_policy` を読まず、
`build_record_present` から false leaf の PASS を hardcode する。

### F8.2 M71-3 は consumer を実行しない

M71-3 :611–626 の loop は

```python
for cname, fn in CONS_FN.items():
```

と `fn` を束縛するが、**一度も呼ばない**。実施するのは map key の存在と、
`recompute` という語が一部行に含まれるかの集合検査だけである。
required / forbidden / recompute / closure-policy の field mutation、
「変わるべき consumer / 不変であるべき consumer」の verdict 比較は 0 件。

これは manifest :242–243 の

```text
各 field を変異させ、変化すべき consumer と
不変であるべき consumer を宣言的に検査
```

という約束を実装していない。

### F8.3 直接反例

repository file を変更せず、インメモリで false branch を

```text
closure_policy = bootstrap_leaf
              -> recursive
```

へ一欄変異した。true / false の policy がともに recursive となり、
R-6 routing は変わるべきである。しかし、

```text
PASS | 14 branch evaluator + consumer matrix
PASS | M71-3 BC_USE_MAP
mutation_failed = []
normal_failed = []
RESULT: ALL PASS
exit 0
```

だった。これは「parse した正本を実際に使う」という便 71 の諮問に対する
まさに反例である。

### F8.4 map 自身も consumer literal と全等式でない

branch block :222 の consumer は八件、

```text
D-R2⁗, I-0″, I-0c″, build_artifact_set,
R-6, H-1a″, N-2, contract C-6⁗
```

だが、`BC_USE_MAP` は `I-0″` と `N-2` を欠く。M71-3 の executable
`CONS_FN` はさらに H-1a″ / C-6⁗ も検査せず、四件だけを見る。
また C-6⁗ は closure entry 義務も述べるのに、map 上の依存 field に
`closure_policy` がない。

従って authority consumer set、use map、executable consumer set の
三集合は一致しない。F12.1 採用は未成立である。

---

## F9. FAIL B72-4 — typed branch domain は list element を見ない

### F9.1 閉じた部分

`validate_branch()` は、

- `build_record_present` の bool 型、
- BASE 三欄の key presence / null、
- list field の外型、
- scalar `toolchain_digest` の 64 lower-hex、
- true の FOUR scalar / list 外型、

を共通 gate で検査する。便 71 の
`false + toolchain_digest = null` consumer 分裂は閉じた。
M71-1 の六 fixture も申告どおり全 consumer 一致だった。

### F9.2 digest list の schema validity が抜ける

E-5 / E-6 / E-9′ と QD-1 は、

```text
source_artifact_digests[] = exact source blob digests
build_step_digests[]      = build step digests
pinned_input_digests[]    = schema-valid、sorted、deduplicated
```

を要求する。しかし `_valid_list()` :359 は `isinstance(v, list)` だけ。
各要素の 64-hex、null、sorted / deduplicated を検査しない。

しかも script 自身の PASS fixture `REC` :441 / :447 / :449 は

```python
source_artifact_digests = ["s"]
```

を valid record として使う。`"s"` は exact digest ではない。

独立 probe の結果は次である。

```text
false + build_step_digests=["deadbeef"]
  -> D-R2⁗ PASS / I-0c″ PASS / build-projection PASS / R-6 PASS

true + pinned_input_digests=["deadbeef"]
  -> 四 consumer 全て PASS

false + source_artifact_digests=["s"]
  -> 四 consumer 全て PASS

false + build_step_digests=[null]
  -> PASS / PASS / [12] / PASS
```

前三者は invalid record の false acceptance、末尾は consumer matrix の
再分裂である。それでも通常 RESULT は ALL PASS。

QD-3 :256 も `false.required_keys が present` としか書かず、
BASE list の schema-validity を明記しないため、checker だけでなく
表示表にも同じ穴がある。

### F9.3 commander preflight の typing — NOTE

`ben_preflight.py` は letter に出る path の現 SHA-256 と self-audit が
表示する digest を一つの `allowed` 集合に入れ、各 hex がその集合に
属するかを見る。field と path を対応づけない。

mail 内の spec digest と contract digest を入れ替えたインメモリ probe でも

```text
bad_count = 0
membership_preflight_pass = true
```

だった。現 mail は独立照合で正しく対応しているため NOTE に留めるが、
「receipt provenance の恒久対策」には typed binding が要る。

また `HIST` は行に `旧 / 前版 / 不変 / historical` 等が一語あれば
任意 hex を免除する。historical value は構造化欄で型付けし、語の部分一致を
authority exemption に使わない方がよい。

---

## F10. NOTE 三件の検収

### F10.1 current UNKNOWN — PASS

manifest :539 は、

```text
【current-unknown】
operative であって historical ではない
```

と明記する。CR-11 :623、QD-6 :272 とともに pending queue の三項は
型どおりになった。

### F10.2 authblock expected range — 未修理

script :278 は

```python
top = current - (1 if self else 0)
```

を計算するが、次行は

```python
hi <= current
```

を使い、`top` を参照しない。さらに `lo` / `hi` が expected lower /
upper bound と exact equality であることも要求しない。

manifest の self historical range を `v1..v10` から current を含む
`v1..v11` へインメモリ変異しても、

```text
PASS | 13 authblock label<->digest + sweep-def 上限
RESULT: ALL PASS
exit 0
```

だった。現三文書の range 値そのものは正しいが、
task の「期待 range を使用し範囲完全性を要求」は source と反する。

### F10.3 usage — 未修理

script :14 は現在も

```text
usage: python search/bundle-selfaudit-v4.py [--mutate]
```

であり、task の「usage v6」は実体と不一致。実行時の数学判定を変えないので
NOTE だが、今回も file:line preflight の過大申告を示す。

---

## F11. freeze receipt・UNKNOWN・実装認可

材料値の裁定は次のとおり。

```text
predicate spec ID / full-blob digest          = REPRODUCED
contract ID / full-blob digest                = REPRODUCED
manifest schema ID / full-blob digest         = REPRODUCED
registry-definition block digest              = REPRODUCED
self-audit script digest                      = REPRODUCED
S5 source digest / five IDs                   = REPRODUCED
initial TCB four fields                       = [] / [] / [] / []
pin topology                                  = PASS
registry defined/claimed scope                = PASS
mutation failure -> nonzero exit              = PASS

branch authority uniqueness                   = FAIL
build-face toolchain operand                   = FAIL
BC causal-use                                 = FAIL
typed digest-list domain                      = FAIL
```

従って、

```text
predicate_spec_freeze_id                      = NOT ISSUED
approved freeze receipt                       = NOT ISSUED
searcher v2 / checker                         = NOT AUTHORIZED
D-2 generator / verifier A / verifier B       = NOT AUTHORIZED
separate implementation / runtime             = NOT AUTHORIZED
separate toolchain / build step                = NOT AUTHORIZED
decision lane / audit lane / EP execution      = NOT AUTHORIZED
model-builder                                 = LOCKED
```

とする。

current UNKNOWN 三項、

1. CR-11 の `implemented_checks` 層、
2. QD-6 の bootstrap leaf で失う完全性、
3. N-2(2) / H-1a″ の独立な closure 再導出可能性、

は pending queue として保持してよい。ただし approved receipt が無いので、
今回も receipt scope には格上げしない。

---

## F12. 最小修理と必須回帰

### F12.1 branch owner

E-9′ :142 と §2.35 :250 の「表が正本」を削除し、

```text
判定 owner は §2.34 [branch-contract]。
QD-1..4 はその derived rendering。
```

に一本化する。

check #4 は文字列存在でなく、

```text
parse(branch-contract)
-> render_QD_rows(parsed)
-> current QD table の machine cells と exact equality
```

を要求する。最低でも QD-1〜4 の present / required / forbidden /
validity / expected recompute / expected verdict を構造化して比較する。

### F12.2 build face

owner comment を式の前へ移し、toolchain operand を code として復帰する。
追加回帰:

```text
A/B = false bootstrap leaves
same toolchain_digest
different binary/source/build-step
TCB four fields = []
-> build face intersection contains toolchain
-> [11]
```

文書式と `consumer_buildface()` の投影集合を exact equality にする。

### F12.3 causal-use

一つの parser が AST と source span の双方を返し、少なくとも

```text
required_keys
forbidden_keys
recompute
closure_policy
assurance
consumer
```

を parse する。

consumer literal、BC_USE_MAP key、executable/prose consumer inventory を
正規化して exact equality。`I-0″` と `N-2` を map に追加し、
C-6⁗ の closure statementには `closure_policy` 依存を追加する。

各 field を一欄ずつ変異し、

```text
declared dependent consumer     -> 指定された観測が変化
declared independent consumer   -> 観測が不変
fidelity                         -> 不正 shape は FAIL
```

を実際に実行する。とくに
`false.closure_policy = recursive` fixture を常設する。

### F12.4 recursive digest-list validator

共通 validator を、

```text
digest64(x)
digest_list(xs):
  list
  every element digest64
  no null
  canonical order
  deduplicated
```

として source / build-step / pinned-input の三欄へ適用する。
PASS fixture の `"s"` は 64-hex fixture へ直す。

追加 negative:

```text
["deadbeef"]
[null]
[valid_digest, valid_digest]       # duplicate
[digest_b, digest_a]               # noncanonical order
```

を三 list field ごとに当て、全 consumer が同じ不適合 verdict を返すこと。
QD-3 にも `false.required_keys は present かつ schema-valid` と明記する。

### F12.5 NOTE / preflight

- usage を v6 へ。
- auth historical range は parsed expected range と exact equality。
- META は `--self-test-failclosed-child` 等の child process を起動し、
  parent が exit 1 と failure footer を確認する。
- commander preflight は
  `field -> expected path / extraction rule -> digest`
  を型付きで照合する。単一の allowed set を廃止する。
- historical exemption は structured field のみに許し、行内語彙で免除しない。

---

## F13. ★教材

1. **exact phrase の残存 0 は、意味上の残存 0 ではない。**
   「本節が正本」を消しても「この表だけを正本」が残れば authority は二つ。
2. **owner 注記は式の operand をコメント化し得る。**
   provenance を明確にする一行が、provenance 集合から toolchain を消した。
3. **use map を読むだけでは causal-use ではない。**
   consumer 関数を呼ばず field mutation もしない map check は自己申告の照合に
   すぎない。
4. **list 型が正しいことと、list 要素が正しいことは別である。**
   digest list には element type、canonical order、dedup まで要る。
5. **digest membership は field binding ではない。**
   全 hash が現物由来でも、spec と contract の欄を入れ替えれば receipt は偽。
6. **META test は最終 effect まで観測する。**
   append の確認だけでなく、failure を保持した child の exit code を見る。

---

## F14. 共同設計者発案

### F14.1 `branch_contract` から derived artifact を生成する

QD table、consumer inventory、BC_USE_MAP の三つを手編集せず、
一つの typed branch AST から生成する。

```text
branch AST
  ├─ rendered QD fixture
  ├─ consumer dependency map
  └─ executable mutation plan
```

とすれば「正本の宣言」と「描画の同期」を別々の lint で守る必要が減る。
人間向け prose は generated block の後に効力説明だけを書く。

### F14.2 `causal fingerprint` を footer に載せる

各 field mutation について consumer verdict vector の digest を作る。

```text
causal_fingerprint[
  false.closure_policy -> sha256(vector_before, vector_after),
  false.required_keys  -> ...,
  ...
]
```

同じ block digest でも consumer が hardcode へ退行すれば fingerprint が
変わる。単なる「BC を参照した」という静的 lint より強い。

### F14.3 typed receipt manifest を preflight の入力にする

mail prose から hex を拾うのではなく、発送前に例えば

```text
receipt_preimage = {
  predicate_spec: {path, id, digest},
  verifier_contract: {path, id, digest},
  dependency_manifest: {path, id, digest},
  registry_blocks: [{path, extraction_rule, digest}, ...],
  selfaudit: {path, digest, normal_exit, mutation_exit, footer},
  S5: {path, digest, ids[]}
}
```

を生成し、mail はこの machine block を描画する。これなら field swap、
path omission、歴史語による免除を型で拒否できる。

---

## F15. 監査範囲外申告

### 本便で行ったこと

- `ops/inbox_codex/sol_task_72_freeze8.txt` を先頭から末尾まで読んだ。
- 対話帳は T-17 が最新で、新着が無いことを確認した。
- HEAD / worktree identity、bytes、LF、BOM、full-blob SHA-256、
  registry block SHA-256、S5 digest、TCB 四欄を照合した。
- spec v16 / contract v11 / manifest v11 と predecessor の差分を読んだ。
- `bundle-selfaudit-v6.py` の通常 / `--mutate` と
  `ben_preflight.py` を再実行した。
- `sol/裁定_94_v16束検収.md` を内部検収の透明性資料として読んだ。
- repository file を変えずインメモリで、
  - forced mutation failure の exit 1、
  - QD-3 expected 反転の未検出、
  - false closure-policy 反転の未検出、
  - invalid digest-list element の false acceptance / consumer 分裂、
  - self historical range への current 混入の未検出、
  - preflight の spec / contract digest field swap 未検出、
  を再現した。

### 本便で行っていないこと

- searcher、checker、D-2 generator、verifier A/B、receipt receiver の実装。
- freeze ID / commander receipt の mint。
- dependency closure、build artifact、attestation、EP の実生成。
- sealed candidate、旧 8 hit、具体係数、raw shard、blind value への接触。
- GAP 探索、Lean 証明書、数値探索。
- 数学核・S5 定理群の既監査範囲の再証明。

開始時から存在した対象外変更
`docs/mb_ninfty_verifier_contract_v6.md`、
`docs/week4-NInfty_stage2_spec_v11.md`、`out*.txt`、
`search/__pycache__/` には触れていない。最終 status で監査開始後の
外部追加として新たに観測した `search/certs/`、
`search/family-window-survey.g`、`search/mixed-equality-check.g` にも
触れていない。本便で私が加えた変更は指定された
`sol/sol_reply_72_freeze8.md` だけである。本裁定は paper / adversarial
audit であり、Lean の意味での verified ではない。
