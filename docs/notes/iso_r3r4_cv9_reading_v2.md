# ISO-GATE route-2 R3/R4 CV-9 再判読書 v2(修理 6 項目の検問・副検問)

- **判読者**: falsifier(反証前哨・opus/max)/ 2026-08-05 / 司令塔委嘱(裁定 541)
- **前書**: `docs/notes/iso_r3r4_cv9_reading_v1.md`(【重大 1】【重大 2】【重大 3】+ M-ISO-2 計画監査)。本書はその修理の検問。
- **拘束**: 読み取りのみ・対象改変なし・封印 3 量/705,894 非接触・W-5 の `iso_gate_state` は UNKNOWN 不変(確認済み)。「verified」は Lean 予約語のため不使用。

---

## 0. provenance(本判読時に自分で再計算した SHA-256)

| 役割 | path | sha256 |
|---|---|---|
| GAP driver v2 | `search/probe/w6_bu_s0/iso_gate_r3r4_driver.g` | `0bd70659660cab5e30449a9bb3a8c93079c39940fdbb9cc0ace81ecd75961e1a` |
| Python 第二系統 v2 | `search/probe/w6_bu_s0/r4_second_system.py` | `a617f48398d29b75de09326146b3f5a5d37112c032933a41585213733d0e5c94` |
| 受け渡しデータ | `search/probe/w6_bu_s0/r4_input_data.json` | `a8700551f7d6e0e31482658e30b20a2eaaa073fa00d0b301777b370d3275fcfb` |
| 第二系統 出力 | `search/probe/w6_bu_s0/r4_second_system_output.json` | `42823c74b33ce86fdee38242ea491df49df61d2f159fdb2d0d1a91e0949e68a1` |
| **cert v2** | `search/certs/w6_bu_s0_iso_gate_r3r4_v2_20260805.json` | `4ca7e06865eda88a639bd08c109642e464825aea4e2011cf655977a768728087` |
| cert v1(不改変の確認) | `search/certs/w6_bu_s0_iso_gate_r3r4_20260805.json` | `32e07558cd7e05ada296cae160ac186d1557ad1992a4da1438a27cf2dbad83b8` |
| IF-FIRST 凍結 | `docs/notes/iso_r3r4_iffirst_freeze_v1.md` | `ddc5b21c22c5a71830ed1354f18a0847f127d0605f582e10269fe289feea14be` |

**v1 cert の hash は v1 判読書 §0 に記録した値と完全一致** ⟹ 不改変を機械確認。`M-ISO-8` の語も v1 cert に不在(0 件)。v2_supersedes による継承は成立。

---

## 1. CV-9 三値裁定(再裁定)

# **同一対象(5 量すべて)**

v1 で唯一「別対象」と裁定した `verdict` が、両側同型の 4 変数関数へ整列されたことを**全数確認**した(§②)。ただし v1【重大 1】の帰結は不変であり、**この裁定は原典読解に基づくものであって数値一致に基づくものではない** — その禁止は両 cert に恒久記載された(§①)。

---

## ① 格付け文の恒久禁止 + conventions_used の機械 diff 可能性 — **PASS / FAIL の混合**

### (a) 恒久禁止の記載: **PASS**

両 cert に禁止条項が入った。GAP: `conventions_used.grading_prohibitions`、Python: トップレベル `grading_prohibitions`。両文とも "numeric agreement" が "convention identity" を示さない旨を明記し、GAP 側は「'same object' verdict must rest on source-reading (CV-9 judge), never on this cert's own numeric match」まで書いている。**v1【重大 1】の要求を満たす。**

### (b) 副検問の機械 diff は **まだ原理的に不可能** — **FAIL**

実際に両 cert の `conventions_used` を突合した結果(判読者の diff スクリプト):

| 要求項目 | GAP | Python | 機械 diff 可能か |
|---|---|---|---|
| `perm_composition` | あり | あり | **不可** — 値が別文字列(`"gap_native_right"` vs `"gap_native_right (custom compose() matches k^(p*q)=(k^p)^q)"`) |
| `abstract_prod_reversal`(用例 5 箇所) | あり(**dict**、`usages` 配列に 5 site) | あり(**str**、散文中に "(z, hex310, ymf, hex311, genB)") | **不可** — **型が違う**(dict vs str) |
| `word_eval`(prepend) | あり(2 層の配列) | **不在** | **不可** — 片側欠落 |
| `h10_fail_bookkeeping_unit` | あり | あり | **不可** — 値が別散文 |
| `comparison_target` | あり(dict) | **不在** | **不可** — 片側欠落 |

- GAP 12 キー / Python 4 キー。**Python 側にのみ不在**: `comparison_target`, `effective_source_chain`, `enumeration_domain`, `grading_prohibitions`(位置違い), `group_side`, `ledger_version`, `seal_recoverability`, `word_eval`。
- 共有 4 キーのうち**値が一致するのは `level`(="PB3")の 1 件のみ**。
- 司令塔の指定した 5 項目のうち **diff 可能なものは 0/5**。

**根本原因**: 値が統制語彙(enum)でなく自由散文である。同じことを言っていても文字列が違えば機械 diff は落ちる。**安価な修理**: 値を正規化 enum(`"gap_native_right"` 等)に固定し、散文は `note` 副フィールドへ退避。`word_eval` と `comparison_target` を Python 側へ複製。`grading_prohibitions` を両側同一パス(`conventions_used` 内)に置き、文言をバイト同一にする。

**判定**: 恒久禁止の記載は PASS、**機械 diff 可能化は FAIL(未達)**。本判読は v1 と同じく全て手作業になった。

---

## ② verdict の 4 変数整列 + h10 帳簿統一 — **PASS**

### verdict: 意味論水準で **同一対象**

- GAP `ComputeVerdict(allShadowsGenuine, shadowSumOk, totalShadows, settledCount)`(driver:121-133)
- Python `compute_verdict(all_shadows_genuine, shadow_sum_ok, total_shadows, settled_count)`(py:175-191)

**分岐順・停止コードが完全一致**(`NONSHADOW_IN_DATUM` → `CANDIDATE_ENUM_INCONSISTENT` → `NO_SHADOWS` → `TRUE` → `FALSE`)。判読者が両実装を書き起こして **2×2×5×5 = 100 入力を全数比較 ⟹ 不一致 0**。到達可能出力は 5 種すべて。**同一関数。**

### h10 帳簿単位と恒等式: 両側成立

- GAP: `hex310` を **m ループの内側**で判定・計数 ⟹ (f,m) 対単位。
- Python v2: `hex310` は f ごとに 1 回計算するが、**カウンタの加算は m ループの内側**(py:276-279)⟹ (f,m) 対単位。**単位一致。**

| | candidate_total | h10 | h11 | genfail | shadow | 恒等式 |
|---|---|---|---|---|---|---|
| K^(3) GAP | 108 | 72 | 24 | 0 | 12 | 108−72−24−0=12 ✓ |
| K^(3) Python | 108 | 72 | 24 | 0 | 12 | ✓(`assert shadow_sum_check`) |
| W-5 GAP | 4000 | 3200 | 720 | 0 | 80 | 4000−3200−720−0=80 ✓ |
| W-5 Python | 4000 | 3200 | 720 | 0 | 80 | ✓ |

v1【重大 2】(「Python 側では恒等式が型として成立しない」)は**解消**。副次的に v1【要修正 1】(列挙宇宙 `|D|` が突合外)も、`candidate_total = |D|×|charming|` が両側に出力されたことで**実質的に閉じた**。

**残る軽微**: Python は `candidate_total / h10 / h11 / genfail` を**自己出力するだけで GAP 値に assert していない**(`r4_input_data.json` に `expected_` が無い)。両出力ファイルを人手/機械で並べれば一致は見えるが、自動 fail-closed ではない。

---

## ③ M-ISO-8 と settled 偽側の実発火 — **PASS(核心)/ 但し M-ISO-8 の帰属は誤り**

### (a) settled 偽側の実発火: **PASS** — v1【重大 3】の核心は閉じた

M-ISO-2(v2) は witness を h11_fail バケツから shadow バケツへ**実際に移し**、13 要素リストを **実 `SettledCheckGeneral` に通している**(driver:386-394)。結果 `witness_settled = false`、`settled = 12/13`。Python 側も `build_hom_with_check` の実経路で `witness_settled: false`、`settled_count: 12`。

**キャンペーンを通じて初めて、settled 述語の偽側が両系統で実行された。** 判読者の v1 独立計算(hom は well-defined・像位数 36 ≠ 108)とも一致。

### (b) `settled := true` 固定変異体は殺されているか: **PASS(ただし殺しているのは M-ISO-8 ではない)**

殺されている。ただし機構は M-ISO-2(v2) の**素の assertion** である:

```
mIso2Ok := ... and (witnessSettledEntry.settled = false)
           and (mIso2SettledResult.settled_count = 12) and (mIso2SettledResult.total = 13)
```

変異体下では `witnessSettledEntry.settled` が true、`settled_count` が 13 になり **`mIso2Ok` が落ちる**。Python も `expected_witness_settled` / `expected_settled_count` を同様に assert。⟹ **素通り生存の穴は閉じた。**

### (c) 【要修正 A】M-ISO-8 の `kills` 記述は実態と一致していない

判読者が機械確認した事実:

```
ComputeVerdict(allGenuine=false, sumOk=true, total=13, settled=12)  -> UNKNOWN/NONSHADOW_IN_DATUM
ComputeVerdict(allGenuine=false, sumOk=true, total=13, settled=13)  -> UNKNOWN/NONSHADOW_IN_DATUM
                                                     ^^ 変異適用後
```

**M-ISO-2(v2) の datum 上で、v2 の実 verdict は settled 変異に対し完全に不感である。** M-ISO-8 が比較しているのは

- `mIso8NaiveVerdict` = **genuineness gate を持たない 3 変数関数**(driver:481-486)→ TRUE
- `mIso8RealVerdict` = **gate を持つ 4 変数関数** → UNKNOWN

であり、両者の差は **settled 変異ではなく gate の有無**である。すなわち M-ISO-8 は実質 **M-ISO-3 の重複**(gate 無し/定数 mutant verdict 関数 vs 実関数の比較)であって、cert の

> `"kills":"settled predicate fixed to always-true (the checker's negative-detection power, untested in v1)"`

という帰属は**不正確**。実際にその変異を殺しているのは M-ISO-2(v2) の assertion である(上記 (b))。

**安価な修理(1 行)**: M-ISO-8 を verdict 比較ではなく **detail リストの要素比較**にする —
`SettledCheckGeneral(datum3, mIso2Shadows).detail` と `MutantSettledAlwaysTrue(datum3, mIso2Shadows).detail` を突合し、witness エントリで `false` vs `true` が食い違うことを検出させる。これが「settled チャネルを直接叩く」唯一の形。

### (d) 【留保】「genuine な shadow が settled=false」という組み合わせは依然として未実現

`FALSE` verdict へ至る唯一の経路は M-ISO-4 の合成フラグ反転のみ。**真の非 settled GT-shadow は存在しない**(AS-GAP-6 open)ため、数学者 A.2 の禁止(false-FALSE を作るな)と両立させる限りこれが上限。**FAIL ではなく構造的留保**として記録する。

---

## ④ M-ISO-2 の意味論(NONSHADOW_IN_DATUM)— **PASS**

### A.2(false-FALSE 経路の禁止)を満たすか: **満たす**

witness は `stage = h11_fail`(判読者が v1 で実列挙から再現確認済み)ゆえ Def 3.7 の GT-shadow ではない。v2 はこれを「非 settled な shadow」と読ませず、**最優先 gate で `UNKNOWN(NONSHADOW_IN_DATUM)` に落とす**。isolated=FALSE の主張へ漏らす経路は塞がれている。

### 判読者の安価修理案を満たすか: **満たす(提案どおり)**

v1 §4.2 で提示した「h11_fail バケツ 24→23、shadow バケツ 12→13 で恒等式を整合させる」構成がそのまま実装され、恒等式 `108−72−23−0 = 13` が**手渡しでなく計算で成立**(`identity_holds: true`)。v1 の自己矛盾(M-ISO-2 が自ら追加した sum-check gate を手で迂回)は解消。

### 撤回と AS-GAP-6: **明記されている**

cert `m_iso2_construction_note` に「the v1 claim that M-ISO-2 is 'the campaign's first isolated=FALSE instance' is **WITHDRAWN**」「there is no marked datum here whose GT(N) contains a genuine non-settled GT-shadow」「**AS-GAP-6 ... remains OPEN**」。`mutant_matrix` の M-ISO-2 にも `is_this_isolated_false: "NO -- ..."` フィールドあり。**v1 §4.4 の是正要求は履行された。**

### 【軽微 C】残存する手渡し gate

M-ISO-4 と M-ISO-6b は依然 `shadowSumOk` にリテラル `true` を手渡している:
```gap
mIso4Verdict := ComputeVerdict(mIso4AllGenuine, true, Length(flippedDetail), flippedSettledCount);
mIso6bVerdict := ComputeVerdict(emptyAllGenuine, true, emptySettled.total, emptySettled.settled_count);
```
M-ISO-4 については実測値も true なので**結論に影響はない**が、v1 で批判したのと同じ anti-pattern。`res3.shadow_sum_check` を渡すべき(1 語の修正)。

### 【軽微 G】M-ISO-2 の `all_genuine=false` は構成上「落ちようがない」

`VerifyShadowsGenuine` は列挙器と**同一の式**で hex310/hex311/SURJ を再計算する。witness は列挙器が `h11_fail` に分類した元なので、再検査が false を返すことは**論理的に保証**されている(driver 自身のコメントも「分類と一致するので自動的に一致」と認めている)。したがって M-ISO-2(v2) の看板結果 `UNKNOWN(NONSHADOW_IN_DATUM)` は**発見ではなく定義**。情報量のある部分は `witness_settled = false` と恒等式 `108−72−23−0 = 13` の方である。gate 自体の設置は正当(手組み shadow リストへの保険)なので FAIL ではないが、cert がこれを「独立の検出」と読ませないこと。

---

## ⑤ IF-FIRST の事前性と §7 突合 — **期待値表 PASS / 事前性は留保**

### (a) §7 期待値表 vs 再走結果: **PASS(16/16 完全一致)**

判読者が機械照合した全項目(K^(3) の g_size/n_ord/shadow_total/settled/verdict、W-5 の同 5 項、M-ISO-2(v2) の h11_fail=23・shadow_total=13・identity=true・settled=12/13・witness_settled=false・verdict=UNKNOWN(NONSHADOW_IN_DATUM))が**一致**。§1 の入力 universe 表の `|G|` 期待(N5-control=30・Q3-a=18)も実測と一致。恒等式 `108−72−23−0 = 13` も算術確認。`all_mutants_fired_as_expected: true` / `all_crosschecks_pass: true`。

### (b) 事前性の git 確認: **できない** — 司令塔の前提が成立しない

```
76fbc65 2026-08-05 20:47:41  裁定541: ...
  docs/notes/iso_r3r4_iffirst_freeze_v1.md          (新規 87 行)
  search/probe/w6_bu_s0/iso_gate_r3r4_driver.g      (445 行改変)
  search/probe/w6_bu_s0/r4_second_system.py         (305 行改変)
  search/certs/w6_bu_s0_iso_gate_r3r4_v2_20260805.json (新規)
```

**凍結文書・driver v2・python v2・cert v2 が単一コミットに同梱**されており、凍結文書だけを含む先行コミットは存在しない(`git log --all` で 1 件のみ)。⟹ **git 履歴からは事前性を確認できない。**

### (c) 代替証拠(mtime)は事前性と整合するが証明ではない

```
20:32:31  iso_r3r4_iffirst_freeze_v1.md   ← 凍結文書の最終書き込み
20:42:47  iso_gate_r3r4_driver.g
20:45:16  r4_second_system.py
20:46:19  r4_input_data.json / cert v2     ← GAP 走行の出力
20:46:27  r4_second_system_output.json     ← Python 走行の出力
```

凍結文書の最終書き込みは走行出力の **14 分前**。⟹ §7 期待値表を走行結果から後付けした可能性は、この痕跡の範囲では**反証されない**。ただし mtime は最終更新しか記録せず、20:32 以前に draft driver を走らせて出力を上書きした可能性は**排除できない**。

**判定: 留保**(反証もされていないが証明もされていない)。
**勧告(コスト ~0)**: 今後の IF-FIRST は**凍結文書だけを単独コミットしてから走らせる**。これだけで事前性が git で機械確認可能になる — 事前登録の意味はそこにしかない。

### (d) 【軽微 D】凍結文書の内部不整合

§2 の項目 5 が「GAP `ComputeVerdict(shadowSumOk, total, settled)` と同型の **3 変数関数**を Python 側にも実装し」と書いているが、同文書 §6 が `NONSHADOW_IN_DATUM` を新設し、実装は**両側 4 変数**である。**事前登録文書が自らの §6 および実装と食い違っている**。事前登録の正本としては訂正されたい(結論には影響しない)。

---

## ⑥ 経路層変異の復元(M-ISO-3/4/5/6b)— **PASS(3 件完全・1 件は上限)**

| # | v1 | v2 | §5.3 事前登録の趣旨に合致するか |
|---|---|---|---|
| M-ISO-3 | 文字列リテラル比較 | **実関数** `MutantConstantTrueVerdict` を実 4 引数で呼ぶ | **PASS**(依然 ComputeVerdict 層だが、mutant が実行される) |
| M-ISO-4 | `ComputeVerdict(true,12,11)` | `res3.settled.detail` の実レコードを `ShallowCopy`→1 件反転→`Number()` で**再計数** | **PASS(留保)** — §5.3 は「shadow を差し替え」だが実装は `SettledCheckGeneral` の**出力**を書き換えている。入力側の差し替えは A.2 が禁ずる false-FALSE 構成になるため**現状の上限**。スカラー算術からは脱した |
| M-ISO-5 | `ComputeVerdict(false,11,11)` | 実リストスライス `shadows{[2..12]}` + **実 `SettledCheckGeneral` 呼び出し** → sumOk=false → UNKNOWN | **完全 PASS**(§5.3「列挙から shadow を 1 個落とす」に合致) |
| M-ISO-6b | `ComputeVerdict(true,0,0)` | **実 `SettledCheckGeneral([])` 呼び出し**(ループ本体が実際に 0 回回る) | **PASS**(§4 軽微 C の手渡し true は残存) |

v1 の「7 件中 5 件が 10 行の純関数だけを叩いていた」状態は解消。現在スカラー層のみで完結する mutant は**なし**。

---

## 2. 発見一覧(v2)

| 札 | 内容 | 参照 |
|---|---|---|
| **【要修正 A】** | M-ISO-8 の `kills` 帰属が誤り。実 verdict は settled 変異に不感(機械確認済み)。実際に殺しているのは M-ISO-2(v2) の assertion。M-ISO-8 は M-ISO-3 の重複 | ③(c) |
| **【要修正 B】** | `conventions_used` の機械 diff が依然不可能(要求 5 項目のうち diff 可能 0/5・Python に 2 項目不在・型不一致 1・自由散文 2) | ①(b) |
| 【軽微 C】 | M-ISO-4 / M-ISO-6b が `shadowSumOk` にリテラル `true` を手渡し(v1 で批判した anti-pattern の残滓) | ④ |
| 【軽微 D】 | 凍結文書 §2 の「3 変数関数」が §6・実装(4 変数)と不整合 | ⑤(d) |
| 【軽微 E】 | Python が staged counters(candidate_total/h10/h11/genfail)を GAP 値に assert していない(自己出力のみ) | ② |
| 【軽微 F】 | `grading_prohibitions` の配置が両側で異なる(GAP=`conventions_used` 内 / Python=トップレベル)・文言がバイト非同一 | ①(a) |
| 【軽微 G】 | M-ISO-2 の `all_genuine=false` は列挙器の分類と同一式ゆえ構成上保証された結果(「独立の検出」と読ませない) | ④ |
| 【留保 H】 | 「genuine shadow が settled=false」の組み合わせは依然未実現(AS-GAP-6 open・A.2 と両立する上限) | ③(d) |
| 【留保 I】 | IF-FIRST の事前性は git で確認不能(単一コミット)。mtime は整合するが証明ではない | ⑤(b)(c) |
| 【残置】 | Python 出力は assert 成功時のみ生成 ⟹ 出力単体に識別力なし・入力ハッシュなし(v1【要修正 2】未修理。**cert が正直に明記**しており、6 項目の範囲外として意図的に残置) | cert `r4_second_system.note` |

**v1 の 3 件の重大所見はいずれも実質的に閉じた**:【重大 1】= 恒久禁止として両 cert に記載(ただし機械 diff は未達)/【重大 2】= verdict 同型化・帳簿統一を全数確認/【重大 3】= settled 偽側が両系統で初実行・変異体も殺されている(帰属の記述は要訂正)。

---

## 3. 総合所見

# **支持する** — cross-checked 格付けは、宣言された 5 量・3 データ(K^(3)・W-5・M-ISO-2(v2) 再構成 datum)の範囲で支持できる。ただし格付け文に(i) 数値一致が規約同一性を示さない旨の恒久禁止と、「同一対象」の根拠が**原典読解**にある旨、(ii) 本件は tool-calibration 層であって isolated=FALSE の数学的主張を一切含まない旨(AS-GAP-6 open)を明記し、**【要修正 A】(M-ISO-8 の帰属訂正)と【要修正 B】(conventions_used の機械 diff 可能化)を格付けと同時か直後に是正すること**を条件とする。

補足: 【要修正 A】【要修正 B】はいずれも**証拠の帰属と検問可能性の問題**であって、「両系統が別の対象を計算している」という所見ではない。両者を理由に格付けを止める必要は認めないが、放置すれば次回の副検問がまた全手作業になり、cert の `kills` 欄が実態と乖離したまま将来の読者に引用される。

**判読の限界(正直な申告)**: 本判読は判読者の第三実装(v1 で作成した独立 Python 実装)による K^(3)/W-5 の全段再現と、v2 の verdict 関数・conventions_used・凍結表の機械照合に基づく。GAP の再走は行っていない(cert と出力 JSON の値を照合したのみ)。W-5 側の witness 経路・N5-control/Q3-a の内部は再現していない。数学的正しさ(反転規約が正典 (3.10)/(3.11) の意味か、A.2 の妥当性)は判読していない — Sol / 数学者の領分。
