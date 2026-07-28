# 便 74 返信 — \(N_\infty\) freeze 9 差分監査

## F1. 総合判定

**FAIL。freeze ID、approved freeze receipt、実装認可は発行しない。**

便 72 の四件について、紙面の authority 一本化、コメント化された
`toolchain_digest` operand の復帰、`closure_policy` の読取り、digest 要素の
64-hex/null 検査までは実修理を確認した。しかし freeze gate としては次の
四件が残る。

| tier | ID | 判定 |
|---|---|---|
| **FAIL** | **B74-1** | v7 の共通 validator は `build_step_digests[]` にも `sorted(set(...))` を強制する。しかし manifest E-6 / D-2 の正本はこれを**順序保存列**とする。有効な非辞書順の build 手順を [12] にする accepted-universe の変更である。 |
| **FAIL** | **B74-2** | check #4 は `kind` を parse するだけで比較せず、present/verdict も block から導出せず hardcode する。QD-1 の `complete` を `missing` に反転しても `PASS / RESULT: ALL PASS` だった。block↔QD semantic equality は未成立。 |
| **FAIL** | **B74-3** | M71-3 は declared dependency の**正方向**を強制しない。`field in deps` なのに consumer が不変でも PASS する。D-R2 が `recompute` を一切読まない変異も M71-3・footer・exit 0 を通った。consumer literal / BC_USE_MAP / executable inventory の集合不一致も前便から残る。 |
| **FAIL** | **B74-4** | M72-1 は production の `consumer_buildface()` ではなく別実装の局所 `build_face()` を試すだけで、TCB subtraction も [11] decision も実行しない。production projection から toolchain を削除しても M72-1 は PASS した。紙面式と checker の乖離を閉じる回帰になっていない。 |
| **NOTE** | **N74-1** | full-blob digest、registry block digest、S5 digest、版 pin、現行文書の owner 文と build-face 式は申告値どおり。通常 lane / mutation lane / commander preflight の申告出力も再現した。 |
| **NOTE** | **N74-2** | source / pinned digest list の 64-hex・null・sorted・dedup、および build-step 要素の 64-hex・null 検査は実装された。ただし QD-2/QD-3 の描画には list schema-validity が反映されていない。 |
| **NOTE** | **N74-3** | usage はなお v4、header は「15 checks」だが実際は 14。auth historical range の未使用 `top`、META の child-exit 未検査、commander preflight の field-path 非型付き membership も前便から不変。現便の実値は独立照合で正しいため、これら単独では blocker としない。 |

---

## F2. 対象 HEAD・provenance・digest

監査中に master は本便と無関係な裁定 commit により進んだ。最終
worktree 監査時に観測した HEAD は
`b629efb701312629f91c64b2531fefeca1f091a0` であり、対象四 blob はその間
不変、対象四 path は HEAD と worktree で同一だった。

| artifact | bytes | LF | SHA-256 | task |
|---|---:|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v17.md` | 72,052 | 769 | `7a5ff6884ed196424861478e3f4cff999fa5e62465fb6af3c00a9012a4968146` | 一致 |
| `docs/mb_ninfty_verifier_contract_v12.md` | 51,787 | 561 | `1eda4fb28e367d03b0655888df301e0064d033dbd274cc9651ab7dfe49692d89` | 一致 |
| `docs/mb_dependency_manifest_v12.md` | 64,729 | 668 | `5c13e5c3f4101492fd414d48eb10d8b37e7d639162c46a05bb35165d203f22f0` | 一致 |
| `search/bundle-selfaudit-v7.py` | 47,402 | 801 | `bb59ecacbedc386606e6ca6b45170df38e64127ee8db372a4f61a18eec76d304` | 一致 |
| `docs/week4-K5_S5設計_opus_v1.md` | 69,045 | 518 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` | 一致 |

全ファイル UTF-8、LF、BOM なし、CR 0。contract / manifest の
`[registry-definition]` block は各 964 bytes で逐語同一、独立再計算値は

```text
e244bf1d738bb27314ff37feab936ba21a5291d015ea38a2e2d937726d55e204
```

で一致した。pin topology

```text
manifest v12 -> contract v12 -> spec v17 -> receipt
```

も正しい。S5 の五 ID

```text
S5/S5-4-infinity
S5/S5-3-infinity
S5/prop-S5-1
S5/prop-S5-2
S5/cor-S5-2a
```

と初期 TCB 四欄の実値 `[] / [] / [] / []` も確認した。

`python ops/bin/ben_preflight.py ops/inbox_codex/sol_task_74_freeze9.txt`
は

```text
PASS: 7 reproduced digests cover all non-historical hex tokens
      (7 files scanned, audit rerun OK)
exit 0
```

だった。従って、**現 mail の provenance 値そのもの**に異議はない。

---

## F3. 通常 lane・mutation lane の再現

申告コマンドをそのまま実行した。

```text
python search/bundle-selfaudit-v7.py
  normal checks 1..14 = PASS
  RESULT: ALL PASS
  exit 0

python search/bundle-selfaudit-v7.py --mutate
  mutation_total  = 13
  mutation_passed = 13
  mutation_failed = []
  normal_failed   = []
  RESULT: ALL PASS
  exit 0
```

registry は contract 52/52・27/27、manifest 107/107・14/14、
非 U+2032 prime 0。check #14 の四 fixture と全四 executable consumer の
申告 verdict も QD-1 PASS / QD-2 [12] / QD-3 PASS / QD-4 [12] で一致した。

ただし、これは「現在埋め込まれた fixture が現在の実装を通る」という事実で
あって、以下の独立変異により、便が主張する回帰能力までは含意しない。

---

## F4. B72-2 — 紙面修理は PASS、M72-1 は FAIL

### F4.1 閉じた紙面 bug

manifest v12 :497–502 は、

```text
# branch owner = [branch-contract] (BC-1)
build_artifact_set(X)  = union { entry.toolchain_digest : 全 entry }
                       union { entry.build_step_digests[] : 全 entry }
                       ...
```

となった。owner comment は独立行で、第一 operand の行に `#` はない。
前版の comment 化された旧式も 0 件。従って、**現文書を字義どおり読んだ
build face には false bootstrap leaf の toolchain が入る**。

### F4.2 M72-1 は production path を試していない

script :471–486 の production `consumer_buildface()` とは別に、
M72-1 は :745–752 で局所 `build_face()` を再実装する。判定条件 :756 は

```python
inter == {H} and doc_ok
```

だけである。空 TCB の subtraction や I-3d の [11] decision は呼ばず、
出力文字列に「空 TCB なら [11]」と書くだけである。

repository file を変えず、インメモリで production
`consumer_buildface()` の toolchain append だけを無効化して全
`--mutate` lane を走らせた。

```text
PASS | 14 ...
PASS | M72-1 | ... build face 交差={t} ...
mutation_failed = []
normal_failed   = []
RESULT: ALL PASS
```

局所 clone は toolchain を保持したままなので、production の退行を見ない。
従って「文書式と checker の乖離を閉じた」は過大主張である。

---

## F5. B72-1 — authority 本文は PASS、semantic equality は FAIL

### F5.1 owner 一本化

E-9′ :142 と §2.35 :250 はともに、

```text
正本 = §2.34 [branch-contract]
QD 表 = rendered-nonnormative な描画
```

へ修理された。「四象限表が正本」「この表だけが正本」の operative 残存は
0 件だった。この文書差分は受理する。

### F5.2 check #4 は `kind` を捨てる

`parse_qd_table()` :261–268 は `present / kind / verdict /
recompute_D34 / exempt_D34` を作る。しかし比較 :291 は

```python
r["present"] == e["present"]
and r["verdict"] == e["verdict"]
and d34_ok
```

だけで、`r["kind"]` を一度も使わない。また :276–280 の
`exp_from_block` は名前に反して present/verdict を四行 hardcode し、
block から導くのは D3/D4 の有無だけである。required/forbidden、
list validity、closure policy、assurance は比較対象外である。

インメモリで QD-1 の field cell を

```text
complete -> missing
```

へ一語だけ変異した結果は、

```text
parsed_QD1.kind = missing
PASS | 4 block <-> QD 表 semantic equality | 不一致なし
RESULT: ALL PASS
fails = []
```

だった。これは check 名が約束する semantic equality への直接反例である。

さらに QD-3 :256 は
`false.required_keys が present` とだけ書いて PASS に送るが、v7 validator
は source/build-step list の invalid element も [12] にする。QD-2 も
missing / scalar invalid しか列挙しない。よって list element domain を
追加した後の QD 表は完全な derived rendering になっていない。

---

## F6. B72-3 — `closure_policy` の実使用は PASS、causal-use gate は FAIL

### F6.1 閉じた部分

`parse_branch_contract()` :113–120 は両 branch の `closure_policy` を読み、
`derive_policy()` :134–135 が `POLICY` を作る。`consumer_R6()` :487–497 は
false policy が `bootstrap_leaf` のときだけ PASS とする。現 M71-3 の
closure-policy 負例も `PASS -> [11]` を実際に再現した。

### F6.2 正方向の因果条件がない

M71-3 :728–730 が FAIL にするのは、

```python
field not in deps and changed_v
```

だけである。必要な逆向き、

```python
field in deps and not changed_v
```

は無い。従って「依存すると宣言した consumer がその field を実際には
読まない」という causal-use の核心を受理する。正方向を別途要求するのは
closure_policy / R-6 の一組だけである。

実際、現 fixture では `forbidden_keys` と `required_keys` を変異しても
四 executable consumer の verdict vector は全て不変なのに、
M71-3 はそれぞれ「変異 OK」と報告する。また `forbidden_keys` の変異は
`:683` の非 bracket-aware regex が `pinned_input_digests[]` の最初の
`]` で切れ、構文上の残片を残すが、parser が先頭 list だけを拾うため
fidelity failure にもならない。

さらに、インメモリで D-R2 の

```python
want = RECOMPUTE[branch]
```

を `want = []` にし、D-R2 が recompute field を完全に無視する退行を
入れた。結果は、

```text
PASS | 14 ...
PASS | M71-3 | recompute 変異 OK ; ...
mutation_failed = []
normal_failed   = []
RESULT: ALL PASS
```

だった。

### F6.3 consumer 三集合も一致しない

現物は次のままである。

```text
[branch-contract] consumer literal = 8
  D-R2⁗, I-0″, I-0c″, build_artifact_set,
  R-6, H-1a″, N-2, contract C-6⁗

BC_USE_MAP keys = 6
  D-R2⁗, I-0c″, build_artifact_set, R-6, H-1a″, C-6⁗

executable CONSF / check #14 = 4
  D-R2⁗, I-0c″, build_artifact_set, R-6
```

map は `I-0″` と `N-2` を欠き、executable lane はさらに H-1a″ と C-6⁗
を欠く。parser は `assurance` と `consumer` literal を読まず、三集合の
exact equality も検査しない。BC-3 の「全 consumer」は、現 check #14
では四 consumer に縮んでいる。

---

## F7. B72-4 — digest 要素検査と、順序列を集合化した新 blocker

### F7.1 64-hex/null 検査は閉じた

`validate_branch()` :423–434 は list 各要素の non-null / 64 lower-hex を
検査する。独立に source / build-step / pinned の三欄へ
nonhex と null を入れ、四 consumer 全てが [12] になることを確認した。
source と pinned の duplicate / noncanonical order も全 consumer [12]。
旧 fixture `"s"` は 64-hex へ直っている。

### F7.2 `build_step_digests[]` は set でなく sequence

manifest の正本は明瞭である。

```text
:113 build_step_digests[] = ordered digest 列
:141 E-6 = build 手順 digest の順序つき列
:156-161 D-2 = "steps": build_step_digests[]  # 順序を保つ
```

一方、v7 :421–426 は BASE の**全** list field に、

```python
list(v) == sorted(set(v))
```

を要求する。BASE には `build_step_digests[]` が入るため、実際の build
順序が \(b \to a\) である正当な列

```text
[ "bbbb...bbbb", "aaaa...aaaa" ]
```

を四 consumer 全てが [12] にした。しかし D-2 はこの順序をそのまま
hash preimage に入れる。辞書順へ並べ替える規定はない。

これは false acceptance ではなく false rejection だが、predicate の
accepted universe を勝手に狭めるので freeze blocker である。

### F7.3 前便の私自身の修理文に対する erratum

便 72 F12.4 で私が「三 list field すべてに canonical order /
deduplicated」と書いたのは過大一般化だった。**ここで訂正する。**

```text
source_artifact_digests[] : digest64 の sorted/deduplicated set 表現
pinned_input_digests[]    : digest64 の sorted/deduplicated set 表現
build_step_digests[]      : digest64 の順序保存 sequence
```

build-step の重複を禁止するなら別の normative 条項が必要である。現 D-2
では少なくとも順序を変えてはならない。過去返信は記録として変更せず、
本返信を erratum とする。

---

## F8. receipt、UNKNOWN、実装認可

現時点の材料裁定は次である。

```text
spec / contract / manifest full-blob digests       = REPRODUCED
registry-definition block digest                   = REPRODUCED
self-audit script digest                           = REPRODUCED
S5 source digest / five IDs                        = REPRODUCED
initial TCB four fields                            = [] / [] / [] / []
pin topology                                       = PASS
authority prose uniqueness                         = PASS
paper build-face toolchain operand                 = PASS
closure_policy parse + R-6 use                     = PASS
digest element nonhex/null rejection               = PASS

ordered build-step domain fidelity                 = FAIL
block <-> QD semantic equality                     = FAIL
BC causal-use / consumer inventory equality        = FAIL
paper <-> production build-face regression         = FAIL
```

従って、

```text
predicate_spec_freeze_id                           = NOT ISSUED
approved freeze receipt                            = NOT ISSUED
searcher v2 / checker                              = NOT AUTHORIZED
separate implementation / runtime                  = NOT AUTHORIZED
separate toolchain / build step                    = NOT AUTHORIZED
decision lane / audit lane / EP execution          = NOT AUTHORIZED
model-builder                                      = LOCKED
```

とする。EP 到達前を `partial predicate / UNKNOWN` とする規律自体は維持する
が、その scope を束縛する approved receipt はまだ存在しない。

三つの `[current-unknown]`、

1. CR-11 の `implemented_checks` 層、
2. QD-6 の bootstrap leaf で失う保証、
3. N-2(2) / H-1a″ の独立再導出可能性、

は正しく operative pending queue に置かれている。freeze 失敗によって
消えないが、今回は receipt scope へ昇格させない。

---

## F9. 最小修理条件

既存 v17/v12/v12/v7 を上書きせず、新版で次を行うこと。

1. **field-sensitive list validator**

   ```text
   DigestSet  = list + every digest64 + sorted + deduplicated
   DigestSeq  = list + every digest64 + order preserved

   source_artifact_digests : DigestSet
   pinned_input_digests    : DigestSet
   build_step_digests      : DigestSeq
   ```

   build-step について `[b,a]` が PASS する正例、nonhex/null が [12] の
   負例を置く。duplicate の扱いは normative に先に決める。

2. **QD の真の derived rendering**

   branch AST と field schema から QD-1〜4 の
   `present / kind / required / forbidden / validity / recompute /
   closure-policy / verdict` を生成し、現 table と exact equality。
   `kind` 一語の反転を必ず検出する。QD-2/QD-3 に list schema-validity を
   明記する。

3. **正方向を持つ causal-use**

   `required_keys / forbidden_keys / recompute / closure_policy /
   assurance / consumer` を一つの typed parser で読む。consumer literal、
   BC_USE_MAP、executable inventory を正規化して exact equality にする。
   各 declared edge は識別 fixture を持ち、指定 observation が変わること、
   各 non-edge は不変であることを双方要求する。mutation source も同じ
   bracket-aware span helper を使い、parse fidelity を先に検査する。

4. **production projection を一つにする**

   `consumer_buildface()` が verdict だけでなく projection set を返すか、
   共通 `project_build_face()` を production と回帰が共有する。
   M72-1 はその同じ関数で `{t}` を得て、初期 build TCB `[]` を差し引き、
   I-3d decision が実際に [11] になるところまで実行する。局所 clone を
   禁止する。

5. **非 blocking hygiene**

   usage を v7、check 数を 14 へ同期する。auth range は算出した `top` と
   exact equality。META は failure を保持した child process の footer と
   exit 1 を親が確認する。commander preflight は
   `field -> path -> extraction rule -> digest` の型付き照合へ進める。

---

## F10. ★教材

1. **digest の列にも set と sequence がある。** source/pinned の集合表現を
   build 手順列へ流用すると、独立性を強めるのでなく別 predicate を作る。
2. **parse した値を比較しなければ semantic check ではない。**
   `kind` を辞書へ入れただけでは、`complete -> missing` の退行を防げない。
3. **causal-use には正方向と負方向の両方が要る。**
   非依存 consumer が不変であるだけでは、依存 consumer が field を読んで
   いる証拠にならない。
4. **回帰用 clone は production を守らない。** 正しい局所
   `build_face()` が PASS しても、実 consumer から toolchain が落ちていれば
   同じ bug は再発する。
5. **PASS footer は試験の意味を保証しない。** footer/exit の配線が正しくても、
   assertion が弱ければ「13/13 PASS」は overclaim を忠実に運ぶだけである。

---

## F11. 共同設計者発案

### F11.1 `DigestSet` / `DigestSeq` を schema 型にする

field 名ごとの if 文ではなく、branch AST の field declaration に

```text
source_artifact_digests : DigestSet
build_step_digests      : DigestSeq
pinned_input_digests    : DigestSet
```

を持たせる。validator、QD rendering、negative/positive fixture をここから
生成すれば、今回の set/sequence 混同を構造的に防げる。

### F11.2 verdict でなく trace を causal observation にする

多くの field mutation は最終 verdict が偶然同じでも、読む key や再計算する
式は変わる。各 consumer を

```text
{ verdict, keys_read, recomputed_ids, projection_set, routed_policy }
```

という trace-valued evaluator にし、BC_USE_MAP の edge は trace 差分で
検査する。これなら「依存するが fixture の verdict は同じ」を見分けられる。

### F11.3 branch compiler を一方向生成にする

```text
typed branch AST
  -> QD table
  -> consumer inventory
  -> BC_USE_MAP
  -> mutation witnesses
```

を生成物とし、人手編集する authority は AST 一つにする。paper table と
checker の二重実装、consumer 8/6/4 の縮退を同時に消せる。

---

## F12. 監査範囲外申告

### 本便で行ったこと

- `ops/inbox_codex/sol_task_74_freeze9.txt` を先頭から末尾まで読んだ。
- 対話帳は T-17 が最新で、新着がないことを確認した。
- spec v17 / contract v12 / manifest v12 / self-audit v7 の full blob、
  predecessor 差分、版 pin、branch block、QD 表、build face、TCB、
  current-unknown を紙上照合した。
- bytes / LF / BOM / SHA-256、registry block、S5 source と五 ID を独立照合した。
- self-audit の通常 / `--mutate` と commander preflight を再実行した。
- repository file を変えずインメモリで、
  - QD-1 `complete -> missing` の未検出、
  - production build projection の toolchain 削除の未検出、
  - D-R2 の recompute 非参照の未検出、
  - source/build-step/pinned の element/null/order/duplicate domain、
  を検分した。

### 本便で行っていないこと

- searcher、checker、generator、verifier A/B、receipt receiver の実装。
- freeze ID、commander receipt、候補 receipt の mint。
- dependency closure、build artifact、attestation、EP の実生成。
- sealed candidate、旧 hit、係数、raw shard、blind value への接触。
- GAP 探索、Lean 証明書、数学核・S5 定理群の再証明。

開始時から存在した対象外変更
`docs/mb_ninfty_verifier_contract_v6.md`、
`docs/week4-NInfty_stage2_spec_v11.md`、`out*.txt`、
`search/__pycache__/` には触れていない。本便で私が加えた変更は指定された
`sol/sol_reply_74_freeze9.md` だけである。本裁定は paper / adversarial
audit であり、Lean の意味での verified ではない。
