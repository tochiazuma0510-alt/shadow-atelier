# 増分 CV-9 判読 — R07 fixed-lambda cycle batch **v7 / repair-v2 / envelope-v1 / k = 128**(rank 1962 → 2090・第 19 親 batch-parent-v6 の入場・10-key acceptance・fresh λ_1962 oracle・修理 3 段の逆置換・新計器 3 種の初回)

対象 run: **34523172734 / attempt 1**(success・head `bf0b5c0b6ee00736481575b98f50ac071fc97e28`・workflow `d972-r07-fixed-lambda-cycle-batch-v7-repair-v2.yml`・**5 実行すべて exit 0 / `outer_terminated` 5/5 False**)
候補 artifact **10173275037**(403,815,011 B・zip entry **12,050**・展開合計 **1,444,771,837 B**)
診断 artifact **10173299214**(同 bytes・内容同一を私が中央ディレクトリで独立確認)
判読者: falsifier(非当事者・事後)。判読日 2026-09-11。
前回 CV-9 正本: `docs/notes/fixed_lambda_batch_v6_cv9_reading_v1.md`(裁定 2244・限定 7 条・F-v6-1〜4)。
数学者追補: `docs/notes/math_cost_order_addendum_v1.md`(§1.3 の層あたり JSON バイト予測・0.0853 s/MB・642:1 冗長性)。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 7 条(§10)。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 7 条)・rank 2090 / gen 8795 を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v6 の rank 1962 の直系後継として置き換える(合算ではない)。**

**a(128) = 128**(offered 128 / accepted 128 / dependent 0 / skipped 0・partial false)。rank 2090 = 1962 + 128。消化率 128 / 36,000 = **0.3556 %**。

見出し 7 つ:

1. **【重大・v6 判読の訂正】v6 が出した「層費用は加速する」という読みは、4 点目で棄却された。** 層あたり P 残差の増分は **+42.823 → +45.042 → +49.207 → +42.336** で、4 層目が最小。7 点再フィット `fixed(k,n) = 26.422 + 1.2642k + 45.4855n`(最大残差 2.69)。k=128 の 5 点で n² 係数は **0.228**(v6 判読の実質 1.355 から激減)し、**線形の最大残差 2.332 < 2 次の 2.560** — **2 次項は不要**。壁の数字は実質不変(最良 (k,N) でも最終 run が 10,182 s = cap の **1.886 倍**・v6 は 1.86 倍)。**「線形 n モデルは楽観側に外れる」という v6 の警告は撤回すべき。**
2. **【一次データ・本判読の最大の収穫】新計器が層費用の Θ(k·R) を厳密式で確定した。** 層 i の `ordered_reductions` 要素数は **128·R_i + 8,128**(実測 193,728 / 210,112 / 226,496 / 242,880 = 予測と完全一致)。層 i が parse する一意 JSON バイトは **129.778 / 141.432 / 153.185 / 164.938 MB** — **数学者 §1.3 の「4 層目 ≈ 165 MB」予測を誤差 0.04 % で的中**、s/MB も **0.0892**(§1.3 の 0.0853 と 5 % 差)。**F-v6-2 の要求 2(要素数)と要求 3(C 側 file_bytes)は両方実装され、片肺は解消した。**
3. **【重大な副産物・除去可能な無駄】P は親 `reduction.json` を 1 層あたり 2 回 parse している。** 計器実測: `parse_attempts 256 / unique_documents 128`、`repeated_input_bytes` は層ごとに **64.73 / 70.55 / 76.41 / 82.28 MB**。C 側は `duplicate_successful_parses = 0` で重複ゼロ。数学者の 642:1 payload 冗長性とは別口の、**実測された 2 倍読み**である。
4. **【一次データ・射程に効く】λ_1962 の失敗数が 5 世代で初めて増えた。** 36,274 → 36,104 → 36,002 → 35,921 → **36,000**(net **+79**)。**roster が単調に減るという前提は消滅**し、v6 判読の「35,921/81×128 ≈ 56,770 行」型の外挿は定義不能になった。`failure_set_monotonicity_asserted: false` は正しかった。
5. **【一次データ】end-to-end 較正が 4 段先まで揃った。** λ_1962 の下で v6 / v5 / v4 / v3 が消費した各 128 弦は **すべて 0/128 失敗**(= 全部が充足に留まる)。乱択基準線は 85.3 ± 5.3(2,000 回の実験値と理論値が一致)で、**z ≈ −16.02 / −15.95 / −15.90 / −15.83 σ の 4 連**。
6. **【解決】修理 3 段の差分は逆置換で全数説明された。** P 初版→repair-v1 = **4 行**(identity 2 + 親行数定数 2 = 256/384 → 384/512)、P repair-v1→v2 = **identity 2 行のみ**、C 初版→repair-v1 = **identity 4 行**、C repair-v1→v2 = **identity 4 行 + 旧 path 負例 1 assignment**。バイト差 **+20 / +0 / +40 / +50** が 1 バイトの余りもなく説明される。Astra の主張と完全一致。
7. **【新規・軽微だが要注意】rank 2090 の sealed object が 2 つ存在する。** 失敗 run 34492284273 の `state_head = 400e9e29…` と本走の `31b3d6db…`。数値 payload(物理行 128 本・λ・target・残差表)は **両者バイト同一** で、差は seal(owner/source/start/selection 由来)のみ。**v5 で解消したはずの F-v5-5 型が再発した。**

---

## 1. (1) 規約表 diff(v6 → v7 初版 → repair-v1 → repair-v2)

### 1.1 修理 3 段の逆置換(git 実バイト・全数)

私は repo 作業ツリーの 14 本を再計測し、**14/14 が便の pin(bytes + sha256)と一致**することを確認したうえで diff を取った。repair-v2 の 4 path は HEAD(bf0b5c0b)とバイト同一。

| 段 | 側 | bytes | hunk | 変更行 | 内容 |
|---|---|---:|---:|---:|---|
| v7 初版 → repair-v1 | P | 552,865 → 552,885(**+20**) | 3 | **4** | `C_FILE` / `WORKFLOW`(identity)+ `final_manifest_value` の `anchor_previous_parent_batch_rows: 256→384` と `anchor_total_parent_batch_rows: 384→512`(同一行) |
| v7 初版 → repair-v1 | C | 525,617 → 525,657(**+40**) | 2 | **4** | `PRODUCER_FILE` / `CHECKER_FILE` / `CHECKER_WORKFLOW` / `CURRENT_PRODUCER_REGISTRATION`(すべて identity) |
| repair-v1 → repair-v2 | P | 552,885 → 552,885(**±0**) | 2 | **2** | `C_FILE` / `WORKFLOW` のみ |
| repair-v1 → repair-v2 | C | 525,657 → 525,707(**+50**) | 3 | **5** | identity 4 行 + **旧 path 負例 1 行** |

repair-v2 の C の核心(裁定 2255 の修理):

```
-        bad[side]["file"] = bad[side]["file"].replace("_v7.py", "_v6.py")
+        bad[side]["file"] = "search/" + ("check_" if side == "checker" else "") + "d972_r07_fixed_lambda_cycle_batch_v6.py"
```

置換式(44 B)→ 明示構成(94 B)の差 **+50 B** が C の全バイト差と一致する。**私は artifact 同梱の fixture 実バイトも取得し、`selftest-fixtures/C/registration/old-{producer,checker}-path/code.json`(各 333 B)が `search/d972_r07_fixed_lambda_cycle_batch_v6.py` / `search/check_d972_r07_fixed_lambda_cycle_batch_v6.py` を持つことを確認した**(repair-v1 では repair_v1 名のまま = no-op だった)。両負例は本走内 selftest で実際に拒否されている(§6)。

**⇒ 「変更は C4 外の旧 path fixture 1 assignment と deployment identity/public pin のみ」という Astra の主張は、バイト単位で正しい。C の肯定側判定ロジックは v7 3 版すべてでバイト同一であり、修理が checker を緩めた可能性は構造的に無い。**

### 1.2 v6 → v7 の span 全数分類(私の第三実装・AST 由来)

| 側 | v6 span | v7 span | **バイト同一** | 変更 | 新設 | 削除 |
|---|---:|---:|---:|---:|---:|---:|
| P | 262 | 301 | **241** | 20 | 40 | 0(最終行の位置のみ) |
| C | 256 | 298 | **226** | 28 | 44 | 0(同上) |

- **新設はすべて第 19 親関連(`batch_v6_*` / `fourth_*` / `check_v6_*` / `historical_v6_*` / `promote_*`)+ 計器 7 本**(P: `OrderedReductionObserver` / `ParserBytesObserver` / `ordered_reduction_observe` / `parser_bytes_observe` / `authenticate_parent_with_{ordered_timing,parser_bytes}` / `finish_inputs_with_timing` / `emit_auxiliary_timing`、C: `OrderedReductionTiming` / `SavedParentJsonBytes` / `InputPreservationTiming` / `emit_auxiliary_diagnostic`)。**算術核に新設は無い。**
- 六相(raw/source/primal/p1/B/reduction)の実装・`vectorized_projection_chunk` / `sparse_adjoint` を含む算術区間は **v6 とバイト同一**(241/226 の同一集合に含まれる)。

**等長置換(「同じ大きさの別物」を隠せる)を最優先で全数 diff した**:

| 側/symbol | bytes | 実差分 | 判定 |
|---|---:|---|---|
| P `current_derived_rho2` | 1508 → 1508 | `481 → 609`(祖先数)・`256/384 → 384/512`・require 名 `all481… → all609…` | **正しい前進** |
| P `final_manifest_value` | 1267 → 1267 | 同じ `256/384 → 384/512`(**初版ではここだけ更新漏れ = 2251 の原因**) | 修理済 |
| P `SCHEMA` | 48 → 48 | `.v6 → .v7` | — |
| C `SelectionArithmetic` | 216 → 216 | **`@dataclass` の区間境界移動のみ**(コードは同一) | 実質無変更 |

### 1.3 registry の全数分類(私の第三実装)

`audit-region-registry.json`(1,815,821 B)の `current_transitions` を全数分類:

| 側 | baseline | current | `EXACT_RAW_BYTES_UNCHANGED` | `ADDED_CURRENT` | `REGISTERED_CHANGED_RAW_BYTES` | `REMOVED_BASELINE` |
|---|---:|---:|---:|---:|---:|---:|
| P | P6 177 区間 | P7 **205** | **160** | **28** | **17** | **0** |
| C | C6 165 区間 | C7 **194** | **132** | **30** | **32** | **1** |

- **`REMOVED_BASELINE` 1 件は C の `PREAMBLE` 区間で、対応する `ADDED_CURRENT: module-prefix` と対になる「改名」**(P 側の命名に揃えたもの)。内容の削除ではない。**この 1 行を「checker から検査が消えた」と読む誤読を防ぐため明記する。**
- C の 32 変更のうち **11 件は `@dataclass` デコレータ行を前の区間の末尾から次の区間の先頭へ移した境界移動のみ**(`select_all_residuals` / `telemetry_record` / `batch_tree_payloads` / `compare_candidate_publication` / `candidate_readouts` / `SelectionArithmetic` / `DecisionArithmetic` / `SavedPhysicalRow` / `RootRecords` / `SelectionReplay` / `CandidateReplay` / `FinalReplay`)。私の AST span 比較では同一と出る。
- **registry が申告した全区間の `bytes` と `sha256` を、私が repo の実ファイルの行範囲から再計算 → 検査した 26 区間すべて一致。** registry は正直である。
- **弱化は 1 件も見つからなかった。**

### 1.4 【2251/2255 の失敗型の残存検査】親層依存定数・identity 由来定数の機械列挙

**(a) 親行数**: `parent_batch_rows` を含む行を P 50 箇所 / C 50 箇所すべて列挙。現行 run の値 `128 / 384 / 512` を持つのは P L733-735(親 facts)・L4500・L5287・L5320(`promote_batch_v6_anchor`)・L6263-6264(`current_derived_rho2`)・L6362-6363(`final_manifest_value`)、C L2787-2788・L2822・L3881。**それ以外の 256/384・128/256 はすべて親世代の凍結値であり、私は各出現の所属関数を確認した。現行値を持つべき箇所で旧値が残っているものは無い。**
**C は literal ではなく導出している**:

```
promoted.previous_parent_batch_rows = BATCH_PARENT_ROW_COUNT + NEXT_BATCH_ROW_COUNT + THIRD_BATCH_ROW_COUNT   # 384
promoted.total_parent_batch_rows    = promoted.previous_parent_batch_rows + FOURTH_BATCH_ROW_COUNT            # 512
```

(4 定数はすべて 128。)**P だけが literal を持つ非対称が 2251 の直接原因であり、この非対称は v7 でも解消されていない。**

**(b) 祖先数**: 97 → 225 → 353 → 481 → **609** の累積が P/C の literal と `output/parent-intake.json` の `old/intermediate/second/third/target_derivation_parents` で一致。**現行 run の 737 は literal 化されておらず `count + accepted_new_rows` で算出**されるので、この系統に 2251 型の危険は無い。

**(c) key 数 / role 数**: `OLD_PARENT_ROLES` 15 / `V4_PARENT_ROLES` 16 / `V5_PARENT_ROLES` 17 / `V6_PARENT_ROLES` 18 / `PARENT_ROLES` 19、要求名 `old_batch_exact_fifteen_roles` / `next_batch_exact_sixteen_roles` / `third_batch_exact_seventeen_roles` / `fourth_batch_exact_eighteen_roles` / `nineteen_registered_roots`。native acceptance key 数は v3=6 / v4=7 / v5=8 / v6=9、現行=10(`acceptance_exact_ten_plain_keys`)。**すべて整合し、v6 で残っていたラベル残留(F-v6-3)は解消**(`production_requires_exact_seventeen_roots…` → `…nineteen_roots…`、`eighteen_registered_roots` → `nineteen_registered_roots`)。

**(d) file 名由来(2255 型)**: 両ファイルの `.replace(` 全 14 箇所を列挙。path/名前を触るのは
 (i) `role.replace("-","_")`(P 3・C 4 箇所)= `ROLES`/`PARENT_ROLES` 駆動で親数に自動追随、
 (ii) **P L4856 `pending["file"].replace("/reduction/reduction.json", "/manifest.json")`**(新計器 `OrderedReductionObserver` の型検査窓の終端検出)、
 (iii) `started_utc.replace("Z","+00:00")`(時刻・無関係)、
 (iv) `os.replace`(原子リネーム)。
**修理済みの旧 path 負例以外に、名前変異型の負例は残っていない。** `_v7.py` / `repair_v1` / `repair-v1` / `batch-v7.yml` という旧 identity 文字列は **P/C とも 0 出現**。
**(ii) は 2255 と同族だが自己検知型**: 期待の後続読みが来なければ `status: OBSERVER_ERROR` / `observation_error: OBSERVED_PARSE_WITHOUT_COMPLETED_TYPECHECK` を吐き、run は落ちない。今回は `status: COMPLETED` / `observation_error: null` が 4 層すべてで出ている。

**(e) 単一登録表の存在**: `audit-region-registry.json` の `new_source_audit` に `mathematical_parent_count: 19` / `previous_parent_batch_rows: 384` / `total_parent_batch_rows: 512` / `target_derivation_parents: 609` / `initial_rank: 1962` / `initial_generation: 8667` / `checker_expected_rejections: [28,9,6,7,8,10]` / `producer_expected_rejections: [30,10,6,7,8,8]` が載っており、**私が実データから測った値と 8/8 一致**。裁定 2252 の設計は先取り実装されている。
**ただし【要修正】** — この表は **driver の静的 literal であって、P/C はこれを読まない**(P/C が参照する registry 名は 3〜4 箇所だが、いずれも raw pin の突合であり値の導出ではない)。**すなわち登録表は「宣言」であって「導出源」ではなく、2251 の再発を機構的に防いではいない。** P の 384/512 literal を C 同様に名前つき定数の和へ変えるまでは、同じ事故は起こり得る。

### 1.5 公開 JSON の key 集合の機械列挙(前 3 回の失敗型の再発防止)

v6 親と v7 の同名 18 文書の top-level key 集合を機械列挙:

| 文書 | v6 | v7 | 追加 | 削除/改名 |
|---|---:|---:|---|---|
| `output/HEAD`・`result.json`・`owner.json`・`source.json`・`selection/start.json`・`selection/selection.json`・`final/separator.json`・`final/manifest.json`・`fixed/manifest.json`・`progress/HEAD`・`checker-result.json`・`source-receipt.json`・`cost-receipt.json` | 24/48/8/10/19/27/12/27/9/16/50/18/15 | **同数** | **なし** | **なし** |
| `output/parent-intake.json` | 49 | **57** | `accepted_batch_v6_{anchor,checker,head,parent_intake,result}_sha256` + `third_intermediate_{rank,generation,target_derivation_parents}` | なし |
| `output/start.json` | 44 | **49** | `accepted_batch_v6_*` ×5 | なし |
| `run-receipt.json` | 79 | **82** | `accepted_batch_anchor_v6`・`batch_parent_v6_envelope_intake`・`batch_parent_v6_restoration`・`selection_lambda1962_oracle_is_separate_from_new_final_lambda_oracle` | **`selection_lambda1834_oracle_is_separate_…`(版番号入り key の改名 1 件)** |

**⇒ 16 文書が key 集合完全同一、2 文書は追加のみ。唯一の改名は run-receipt の版番号入り自己申告 key。** これは gate ではないが、**版番号を key 名に埋める設計は 2255 と同じ「identity 由来の名前」であり、literal 名で読む消費者を毎 run 壊す**。【軽微】として記録する。

### 1.6 registry と pin の物理固定・run 中の検証証拠

- registry 4 本を driver literal から抽出 → artifact 同梱コピーと突合: historical 76,867 / v4 236,390 / v5 499,053 / **v6 867,833**(すべて v6 判読の値と同一)/ 現行 1,815,821 B。
- **artifact 同梱の配置 4 本を repo とバイト照合**: `workflow.yml` 34,800 B・`driver.py` 4,457,044 B・`workflow-parent-v6.yml` 30,603 B・`workflow-parent-v6-driver.py` 2,281,118 B — **4/4 が size + CRC32 一致**、うち yml 2 本は sha256 も直接一致。
- `checkout-sources/search/{,check_}d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py` と `audit-history-sources/search/{,check_}…_v6.py` の 4 本を実バイト取得 → **repo と sha256 完全一致**。
- **run 中の pin 検証の証拠**: `driver-bootstrap-stdout.log` に **18 行の `OK`**(v6 は 14 行)。repo 側 9 + `_temp` 側 9。**repair-v2 driver 自身が repo 側の検査対象に入っている。**
  - **【軽微・継続】現行 WF(`…-v7-repair-v2.yml`)自身はこの 18 行に含まれない**(同梱コピー `workflow.yml` は私が repo と照合済み)。
- **候補 artifact と診断 artifact の同一性**: 中央ディレクトリを両方読み、**entry 12,050 / 名前集合一致 / size・CRC32 の相異 0 / 展開合計 1,444,771,837 B 一致**。`candidate_and_diagnostics_upload_the_same_envelope_root: true` を独立に裏づけた。
- **交差辺(独立性)**: C の import は標準ライブラリ + numpy + `check_d972_r07_complete_oracle_cegar_continuation_v2` のみ。producer への参照は `PRODUCER_FILE` と `CURRENT_PRODUCER_REGISTRATION`(bytes/sha pin)だけ。**v1〜v6 と同じ二系統分離。**
- 凍結 envelope: acceptance の `registration` ブロックが **v6 とバイト完全一致**(batch 128 / max_batches 1 / refill false / caps 5,400・10,800 s / 7,168 MiB / 同一 selection_policy / 同一 partial_policy)。**caps・宇宙は 1 バイトも動いていない。**

---

## 2. (2) 第 19 親 batch-parent-v6 の入場

### 2.1 10-key acceptance

`acceptance.json`(10,671,359 B)の top-level key は **ちょうど 10**:
`{schema, parents, anchor, batch_anchor, next_batch_anchor, batch_anchor_v5, batch_anchor_v6, code, runtime, registration}`。C の `check_acceptance_header` が `acceptance_exact_ten_plain_keys` で総当たり要求。

`batch_anchor_v6`(36 key)と v6 の公開値の突合(**私は v6 artifact 10131122423 から 16 本の実バイトを取得して sha256 を再計算**):

| 項目 | `batch_anchor_v6` | v6 実 artifact の再計算 | 一致 |
|---|---|---|---|
| `rank` / `generation` | **1962 / 8667** | v6 final | ✔ |
| `lambda` / `lambda_sha256` | 12,096 B / `b3eb3b39…` | `output/final/lambda.bin` を再計算 | ✔ |
| `target` / `target_remainder_sha256` | 12,096 B / `706a8d1d…` | `output/final/target-remainder.bin` を再計算 | ✔(§4.3 で t₀ として使用) |
| `state_head` | `11ade7a4…` | v6 の final state_head | ✔ |
| `target_derivation_parents` | **609** | v6 の ancestry | ✔ |
| `accepted / previous / total_parent_batch_rows` | 128 / **384** / **512** | 4 層 × 128 の累積 | ✔ |
| `old_oracle` | `{35921, 234, 120}` | v6 の選定 oracle(λ_1834) | ✔ |
| `head` / `result` / `checker` / `owner` / `source` / `parent_intake` / `progress_head` / `selection` / `selection_start` / `separator` / `final_manifest` / `fixed` / `source_receipt` / `run_receipt` / `start` / `parent_layout` | 16 記述子 | **16/16 を実 artifact から取得して sha256 再計算 → 全一致** | ✔ |

**記述子の全数照合**: `batch_anchor_v6` に埋まった `{bytes,file,sha256}` 記述子は **791 個**。**791/791 が親 inventory の同名 entry と bytes・sha256 完全一致・欠落 0・不一致 0。**

### 2.2 親 inventory の実バイト束縛(私の第三実装)

- acceptance の `batch-parent-v6` は **files 11,915 / directories 3,582 / 合計 1,395,498,726 B**。
- **私が v6 artifact の中央ディレクトリを直接読み → entry 11,915・名前集合完全一致・サイズ不一致 0・合計バイト一致。**
- **directories 3,582 = 名前から導出できる 3,538 + 空 dir 44**(`ZIP-{casefold,duplicate,traversal}-extracted`・`metadata-fixture/empty`・`selftest-fixtures/C/parent1834/registered-empty-directory-missing/empty`・`selftest-fixtures/P/batch-parent-v5/positive/inventory-root/empty`・`selftest-fixtures/P/registration/host-{0,1}/parents{,/…}` 38 件)。**導出集合 ⊂ 宣言集合で余分 0。私は 44 件すべてを列挙した。**
- **登録定数の再計算**: `sha(canonical(files))` = `a0ef0148…`、`sha(canonical(directories))` = `f4f6101f…` — **P の `BATCH_V6_INVENTORY_REGISTRATION` / C の `FOURTH_BATCH_INVENTORY_REGISTRATION` と完全一致**。
- **【事前登録の的中】v6 判読 §7.6 と付録 B が事前計算した「v7 の登録定数 = files 11,915 / file_bytes 1,395,498,726 / 名前由来 dir 3,538」は、3/3 とも的中した。**

### 2.3 旧 18 親の参照が v6 と同一か

- **v6 の acceptance.json(8,338,053 B)を実 artifact から取得し、v7 の acceptance と全数比較**:
  - `anchor` / `batch_anchor` / `next_batch_anchor` / `batch_anchor_v5` の **4 ブロックは canonical バイト完全同一**。
  - 先頭 18 親の entry は **`path` の run-local 接頭辞(`fixed-lambda-batch-v6-inputs` → `-v7-inputs`)を除いてすべて canonical 同一**。files 配列・directories 配列・artifact メタ(id / run / head / bytes)まで一致。
  - `runtime` / `registration` / `code.{producer,checker}_dependencies` / `code.data` も同一。`code.producer` / `code.checker` のみ v7 の pin へ更新(552,885 B / 525,707 B・repo とバイト一致)。
- 親 4 世代の inventory(continuation 7,916 / 1,265 / 1,046,747,777、batch-parent 11,437 / 3,475 / 1,267,599,138、v4 11,648 / 3,525 / 1,308,094,050、v5 11,750 / 3,547 / 1,347,269,002)は **v6 判読 付録 B と 1 バイトも違わない**。artifact id も同一。

### 2.4 native 6/7/8/9-key 受付の先頭 15/16/17/18 親への射影・累積則

- role 階層: `OLD_PARENT_ROLES`(15)⊂ `V4_PARENT_ROLES`(16)⊂ `V5_PARENT_ROLES`(17)⊂ `V6_PARENT_ROLES`(18)⊂ `PARENT_ROLES`(19)。P 側は `ROLES`(19)・`HISTORICAL_V5_ROLES = ROLES[:17]`・`HISTORICAL_V6_ROLES = ROLES[:18]`。
- 要求は総当たり: `native_v6_acceptance_exact_nine_plain_keys` + `fourth_batch_exact_eighteen_roles`、以下 8-key/17・7-key/16・6-key/15。**私は v6 親の acceptance が実際にちょうど 9 key であることを実バイトで確認した。**
- **累積則**: 親行数 128 / 384 / 512(4 層 × 128)、祖先 97 → 225 → 353 → 481 → 609、`candidate_manifests_checked = row_manifests_checked = 512`、`candidate_phase_manifests_checked = 3,072`(= 512 × 6)、`checkpoints_checked = 3,088`(= 772 × 4)、`invocations_checked = 4`、`native_pairing_rows_rechecked = [1450, 1578, 1706, 1834, 1962]`。**すべて整合。本 run 後の祖先は 609 + 128 = 737 で、737 は literal 化されていない。**

---

## 3. (3) fresh λ_1962 oracle — 生バイトからの完全再現

### 3.1 選定 oracle の再導出

`selection/start.json` の `selection_lambda_sha256` = **`b3eb3b39…` = v6 の final λ**(私が v6 artifact の `output/final/lambda.bin` から再計算して一致)。`state_head` = `11ade7a4…`、`target_remainder_sha256` = `706a8d1d…`、`previous_target_remainder_sha256` = `99c3f3ef…`(= v5 final target)。

| 量 | 公刊 | 私の独立再導出 |
|---|---|---|
| `chords_checked` | 54,433 | 54,433 |
| 残差配列 `chord-residuals.u8` | 54,433 B | `(values − tau·fit) mod 3` で全数再計算 → **バイト完全一致・不一致 0** |
| `failed_count` | **36,000** | **36,000** |
| `failed-indices.u32` | 144,000 B | 私の昇順配列と **バイト一致** |
| `first_failed_index` / `first_failed_edge` | **110 / 212** | **110 / 212**(`fe[0] = 212`) |
| `fit` | **[2,2,2,1,0]** | 3⁵ = 243 通り全数探索で **一意解**(§3.4) |
| 残差値分布 | — | 0: 18,433 / 1: 17,925 / 2: 18,075 |
| `values` 分布 | — | 0: 18,290 / 1: 18,049 / 2: 18,094 |
| `aux_values` | [0, 0] | aux 枝は本番未発火 |
| 選定 128 本の型 | — | すべて `kind=chord`・`coordinate=null`・`scalar ∈ {1,2}`(1:56 / 2:72・**0 は無し**) |
| 選定 128 本 = roster 先頭 128 | — | **`roster_index` が `sorted(failed_indices)[:128]` と完全一致** |

### 3.2 五 λ の失敗集合の比較(初の 5 点データ・**単調性が破れた**)

| | λ_1450(v3) | λ_1578(v4) | λ_1706(v5) | λ_1834(v6) | **λ_1962(v7)** |
|---|---:|---:|---:|---:|---:|
| 失敗数 | 36,274 | 36,104 | 36,002 | 35,921 | **36,000** |
| `first_failed_index` | 70 | 74 | 71 | 120 | **110** |
| `first_failed_edge` | 125 | 131 | 127 | 234 | **212** |

| 遷移 | 正味 | 共通 | 旧のみ(解消) | 新のみ(新規失敗) | Jaccard |
|---|---:|---:|---:|---:|---:|
| λ_1450 → λ_1578 | −170 | 24,041 | 12,233 | 12,063 | 0.4974 |
| λ_1578 → λ_1706 | −102 | 23,936 | 12,168 | 12,066 | 0.4969 |
| λ_1706 → λ_1834 | −81 | 23,978 | 12,024 | 11,943 | 0.5001 |
| **λ_1834 → λ_1962** | **+79** | **23,938** | **11,983** | **12,062** | 0.4989 |

- 五 λ すべてで失敗した弦 **7,140**、どれか 1 つでも失敗 **54,119**、**一度も失敗しなかった弦は 314 本のみ**。
- **churn の大きさはほぼ不変**(片道 ≈ 12.0k)。**正味が初めて正に転じた。**
- **【重大・射程】「失敗数 → 0」を終端条件と見た外挿は、もはや定義できない。** v4/v5/v6 判読が積み上げてきた「roster サイズで残工程を見積もってはならない」という警告は、**外挿の符号が反転したことで決着した**。**Task 988 F4 の反例は依然排除されていない。**

### 3.3 消費した弦の運命(end-to-end 較正・**4 段先まで**)

| 検査 | 結果 | 乱択基準線(理論 / 2,000 回実験) | z |
|---|---|---|---:|
| v6 が消費した 128 弦が λ_1962 で失敗するか(1 段) | **0 / 128** | 85.30 ± 5.32 / 85.27 ± 5.28 | **−16.02 σ** |
| v5 の 128 弦(2 段) | **0 / 128** | 85.05 ± 5.33 / 84.91 ± 5.36 | **−15.95 σ** |
| v4 の 128 弦(3 段) | **0 / 128** | 84.86 ± 5.34 / 84.99 ± 5.23 | **−15.90 σ** |
| v3 の 128 弦(4 段) | **0 / 128** | 84.63 ± 5.35 / 84.61 ± 5.34 | **−15.83 σ** |
| v7 の選定 128 弦 ∩ v6 / v5 / v4 / v3 の選定 128 弦 | **0 / 0 / 0 / 0**(再消費なし) | — | — |
| v7 の選定 128 弦のうち λ_1834 でも失敗 | 54 / 128(λ_1706 で 69・λ_1578 で 85・λ_1450 で 82) | — | — |

読み方(私の判断): v6 判読の 3 段が **4 段に伸び、基準線の実験値と理論値が一致した**。producer が誤った行を足していればこの検査は落ちる。**fresh λ が可能にする最も強い end-to-end 較正であり、失敗数が増えた世代でも成立している点が重要**(すなわち「λ が全体的に良くなったから」では説明できない)。**ただし「定理として強制される」ことを受領証から示したわけではない**(§11)。

### 3.4 fit の一意性と索引規約(F-v5-4 の再確認)

- `basis-tau.u8`(5×5)は **`chord-tau[[0,1,2,3,5]]` と完全一致**、`chord-tau[[2,3,4,6,11]]` とは不一致(私が実バイトで確認)。
- 3⁵ = 243 通りを全数探索し、`basis_tau · x ≡ values[[0,1,2,3,5]] (mod 3)` の解が **唯一 `[2,2,2,1,0]` = 公刊 fit**。誤った索引読み([2,3,4,6,11] を行番号と読む)では `[1,1,0,0,0]` という別解が出る — **誤読が沈黙して別の答を返す構造は健在**。
- **【軽微・継続】受領証はこの二重索引規約を依然明示していない。** v5/v6 判読の指摘(`basis_chord_ordinals` の併記か `basis_edges` への改名)は未反映。

### 3.5 情報性の内訳

- 新 λ(`dd565268…`)の support = **1,383**・character 0 のみ(trit 1 が 726・trit 2 が 657)・非零 index 範囲 2..2262。`result.final_lambda_characters` の `[1383, 0, 0, 0]` / `trit_counts [10713, 726, 657]` と一致。
- 帯構造: **新 lead 帯(2129..2261)より下が 1,299**、**帯内が 83**(= 128 lead のうち非零のもの)、**最終 lead より上の自由座標が 1**(index 2262)。合計 1,383 ✔。**帯内で lead でない座標の非零は 0。**

---

## 4. (4) 階段形・独立・λ・target・鎖(全数確認)

物理行は `packed3` の 12,096 B。1 バイト = 4 trit の little-endian 3 進として全 128 行を展開し、`instruction.physical_sha256` と **128/128 一致**、pack3 往復も 128/128 一致を確認したうえで以下を計算した。

### 4.1 階段形と一次独立

| 検査 | 結果 |
|---|---|
| 行数 / 相異なる lead | 128 / **128**(lead 範囲 **2129..2261**・**昇順ではない** = 挿入順) |
| 自 lead の値 = 1 | **128 / 128** |
| 宣言 lead == 最初の非零座標 | **128 / 128** |
| 先行 lead(j < i)での非零 | **違反 0 件** |
| 後続 lead(j > i)での非零 | **5,365 箇所**(v6 は 5,418・v5 は 5,456)→ **RREF ではなく挿入順前進消去** |

→ **階段形かつ pivot が 128 個相異なるので、128 本の一次独立は定理として従う**(producer の INDEPENDENT フラグに依存しない)。`dependent_candidates = 0` / `skipped_after_linear = []` と整合。

### 4.2 λ

| 検査 | 結果 |
|---|---|
| λ_new ⊥ 新 128 行 | **128 / 128 が 0** |
| λ_new · t_final | **1** |
| λ_new · t₀(= v6 final target を v6 artifact から取得) | **1** |
| `row_pairings_sha256` | **`sha(0x00 × 2090)` を手計算 → `a67c1112…` = separator の値と一致**(親側 `sha(0x00 × 1962)` も再計算し `96677f17…` = `parent-intake.direct_pairing` の値と一致) |
| **λ の 128 個の新 lead 成分の後退代入** | 128 成分を消去(消去係数の非零は 88)してから逆順に復元 → **48,384 座標すべて一致・不一致 0**。復元した λ を packed3 に戻すと公刊 `lambda.bin` と **sha256 完全一致**(`dd565268…`) |
| `direct_pairing` | `lambda_new_remainder = 1` / `lambda_parent_remainder = 1` / `lambda_pivots = 0` / `rows = 2090` |

### 4.3 target 恒等式と符号規約

- 公刊規約(coverage-receipt): `target_update_sign = remainder_before - theta * normalized_row`・`normalizer_convention = sr(0)=0,sr(1)=1,sr(2)=-1; ordered repair x,y,central; mod54 then exact /18`・`correction_word_factor_sign = +sr(theta)` — **3 本とも v6 と文字列同一**。
- **私の検算**: t₀ = **v6 artifact から取得した `output/final/target-remainder.bin`(`706a8d1d…`)** を出発点に `t_{i+1} = (t_i − sr(θ_i)·row_i) mod 3` を 128 段実行 → **最終値が公刊 `target-remainder.bin` とバイト完全一致**(sha `2df80b53…`)。**親 artifact の実バイトから本 run の最終 target までが数値で閉じた。**
- **非空虚性**: θ の分布は **{0: 46, 1: 37, 2: 45}** で `sr` の 3 分岐すべてが通っている。`sigma` は **{1: 78, 2: 50}** で外側指数の 2 分岐も非空虚。

### 4.4 鎖

| 検査 | 結果 |
|---|---|
| `rolling_sha256 = sha(bytes.fromhex(predecessor) ‖ canonical(body))`(body = instruction − {schema, sha256, rolling_sha256}) | **128/128 再計算一致** |
| `predecessor` == 直前の head(anchor = **v6 の `11ade7a4…`** から起算) | **128/128・断絶 0** |
| 128 段後の head | **`31b3d6db…`** = `HEAD.state_head` = `result.state_head` = `checker_result.state_head` |
| instruction の自 seal(sha256 のみ除外) | **128/128** |
| row-manifest の自 seal | **128/128** |
| `manifest.state_head == instruction.rolling_sha256` | **128/128** |
| `physical_sha256` == 行 bin の実 sha | **128/128** |
| `physical_offset == 12096 × (1962 + i)` | **128/128** |
| `target_scalar` == `target.json` の `scalar` | **128/128** |
| `global_row_id` / `rank` / `generation` | 1962..2089 / 1963..2090 / 8668..8795(rank_before/after が連続・coverage-receipt の 128 candidate でも確認) |
| ρ₂ の状態 | `mode=derived` / `value=1` / `original_rho2_directly_read=False` → **未昇格・限定条項 継続** |
| `first_candidate` 予言 | 5 条件すべて True・`expected/observed = INDEPENDENT`・`matches_prediction True`(5 回目)。`first_independent_prediction_is_conditional: true`・`independence_rate_predicted: false`・`failure_set_monotonicity_asserted: false` |
| 128 候補の `outcome` | **INDEPENDENT 128/128** |

---

## 5. (5) 前 run(初回失敗)P 出力との同一性 — v5 判読 §5 と同じ規律

初回失敗 run **34492284273** の diagnostics **10161505854**(403,520,626 B・12,048 entry・展開 1,443,734,701 B)を実バイトで取得し、本走と全数比較した。

**バイト同一(数値 payload)**

| 対象 | 判定 |
|---|---|
| `output/final/lambda.bin`(12,096 B) | **同一** |
| `output/final/target-remainder.bin`(12,096 B) | **同一** |
| `output/selection/tree/chord-residuals.u8`(54,433 B) | **同一** |
| `output/selection/tree/failed-indices.u32`(144,000 B) | **同一** |
| `output/selection/tree/tree.json`(430 B) | **同一**(failed 36,000 / index 110 / edge 212 / fit [2,2,2,1,0]) |
| **`output/rows/*/physical-normalized.bin` 128 本** | **128/128 同一** |

**差分(seal のみ)**

- instruction 20 field のうち **差があるのは `sha256` / `rolling_sha256` / `predecessor` / `selection_sha256` / `literal_sha256` / `witness_sha256` の 6 つだけ**。`lead` / `physical_sha256` / `physical_offset` / `target_scalar` / `sigma` / `offer` / `coefficients_sha256` / `target_sha256` / `candidate_ordinal` / `local_row_offset` / `global_row_id` / `rank` / `generation` は **128 行すべて同一**。
- candidate 000000 の 5 文書を全 key 比較: `witness.json` は 20 key 中 **16 key 同一**(差は owner/source/start/selection_start の 4 identity + 自 seal)、`reduction.json` は 27 key 中 **23 key 同一**、`physical-literal.json` は 12 key 中 **8 key 同一**。**差はすべて上流 identity の伝播**。
- `output/HEAD` は **`anchor_previous_parent_batch_rows` 256 → 384** と **`anchor_total_parent_batch_rows` 384 → 512** が違う — **2251 のバグそのものが失敗 run の公開出力に残っており、修理が効いていることが実データで確認できる**。同じ run の `selection/start.json` は既に 384/512 だった(= producer 内部の不整合であったことの直接証拠)。
- acceptance.json は 10,671,339 → 10,671,359 B(**+20 B** = source path 改名分)。

**判読(私)**: **「同一数学・別 seal」である。** 本走は前 run の出力を流用しておらず(全 seal が新 identity で再構成されている)、かつ算術は決定的に再現している。**したがって本走の P 出力は前 run の複製ではないが、独立な新事実でもない — 同一計算の再実行である。** CV-9 の観点ではこれで十分だが、費用の観点では「初回 run の P 15:01–15:31Z(30 分)+ 本走の P 20:00–20:31Z(30 分)= 同じ計算を 2 回」というコストが実際に発生している。

**【新規・要注意 F-v7-3】rank 2090 の sealed object は 2 つある。** 失敗 run の `state_head = 400e9e29a1dc099754f5fff3c780c1208e030b70ea730fc1b7bdd7907ec94a7d`(未受理・checker REJECTED)と本走の `31b3d6db…`(受理)。両者は Release ミラーと診断 artifact の双方に永続化されている。v5 判読の F-v5-5(v6 で「解消」と記録)と同型の再発である。**「rank 2090」を state_head なしで参照する記述は今後すべて曖昧になる。** 裁定 2251 が「未受理の 2090/8795 を昇格しない」と明記しているので手続きは守られているが、**索引・地図・台帳の側で `rank 2090 = state_head 31b3d6db…` を明示すること**を進言する。

repair-v1 の run 34518126217 は step 13(C selftest)で停止しており本 P は skipped、diagnostics 10168815742 は 25,041,369 B / 2,049 file。**rank 2090 の sealed object は生成していない**(3 つ目は存在しない)。

---

## 6. (6) selftest 群

| 側 | 群 | 拒否件数 | 本走内の実測 |
|---|---|---:|---|
| P | `k128-version-registration-and-types` | 30 | PASS |
| P | `k128-full-roster-cutoff-and-restoration` | 10 | PASS |
| P | `batch-parent1578-admission-and-projection` | 6 | PASS |
| P | `batch-parent1706-two-layer-admission` | 7 | PASS |
| P | `batch-parent1834-three-layer-admission` | 8 | PASS |
| P | **`batch-parent1962-four-layer-admission`** | **8** | PASS(**新設**) |
| C | `k128-version-registration-and-types` | 28 | PASS(**`old-producer-path` / `old-checker-path` を含む**) |
| C | `k128-full-roster-cutoff-and-restoration` | 9 | PASS |
| C | `batch-parent1578-admission-and-projection` | 6 | PASS |
| C | `batch-parent1706-two-layer-admission` | 7 | PASS |
| C | `batch-parent1834-three-layer-admission` | 8 | PASS |
| C | **`batch-parent1962-four-layer-admission`** | **10** | PASS(**新設**) |

- **source 側 literal**: P に `… == [30, 10, 6, 7, 8, 8]`(`selftest_exact_six_group_counts`)、C に `… == [28, 9, 6, 7, 8]`(前 5 群・**v6 と同一 literal**)+ `len(sixth["rejected_cases"]) == 10`。**実行結果の件数と完全一致**、`run-receipt.new_selftest_rejections_registered` とも一致。
- 新設第 6 群(P): `omit-v5-from-old18-projection` / `v6-local0-as-v5-local0` / `inherited481-as-complete609` / `omit-v6-theta0-ancestry` / `previous-target-from-v6-start-previous` / `packed-hash-as-v6-plain-target` / `v6-fixed-reference-as-colocated-payload` / **`inventory-bool-file-count`**。
- 新設第 6 群(C): `omit-v5-from-native18-projection` / `alias-v6-local0-to-v5` / `alias-v6-local0-to-v4` / **`alias-v6-local0-to-v3`** / `drop-zero-from-complete609` / `previous-from-v6-start-previous` / `lambda-source-is-completed-selection` / `registered-empty-directory-missing` / `uncomputed-oracle-is-zero` / **`current-field-in-native49-intake`**。
- **【評価】第 6 群は §2 で私が検算した束縛の一つ一つに対応する否定形になっている。** 特に `inherited481-as-complete609` / `drop-zero-from-complete609`(祖先を親値で代用・θ=0 記録の脱落)、`registered-empty-directory-missing`(空 dir 44 件の脱落)、`uncomputed-oracle-is-zero`(未計算 λ oracle を 0 と読む)は、私が §2・§3・§4 で人手で潰した誤りと同じ形。**非空虚。**
- metadata canary: **16 件・PASS**(`metadata-gate.json` の `metadata_regression_cases: 16`)。
- fixture gate: P/C とも `new_mathematical_selftest_groups: 2` + `new_parent_metadata_selftest_groups: 4` = 6 群。`parent1706` / `parent1834` / **`parent1962`** の fixture gate 受領証が実在。
- **in-run 実行の証拠(v6 の F-v6-4 が今期は非該当)**: 今期は **公開 selftest 版のコミットが存在しない**(v7 系の commit は 0373142c / 2f8ad063 / bf0b5c0b の 3 本のみ)。`execution/producer-selftest-start.json` / `checker-selftest-start.json` の argv は
  `python -B …/search/{,check_}d972_r07_fixed_lambda_cycle_batch_v7_repair_v2.py --selftest --selftest-root …`
  で、**本走 binary そのものに対して 12 群 76 拒否が実行され PASS している。** v6 で指摘した「公開 selftest は None/False guard を保持したまま走る」という証拠力の穴は、今期は構造的に発生していない(配置版は `IMPLEMENTATION_COMPLETE = True` / 全 registration が実 dict)。

---

## 7. (7) 費用 — F-v6-1 の訂正と新計器 3 種の読み(**診断であり gate ではない — 裁定 2225**)

### 7.1 実測(私が telemetry を全数集計)

| | v1(k=32) | v2(k=64) | v3(k=128) | v4 | v5 | v6 | **v7** |
|---|---:|---:|---:|---:|---:|---:|---:|
| 開始 rank | 1450 | 1450 | 1450 | 1578 | 1706 | 1834 | **1962** |
| 親 role 数 / batch 親層数 n | — / 0 | 15 / 0 | 15 / 0 | 16 / 1 | 17 / 2 | 18 / 3 | **19 / 4** |
| producer 実秒(自己申告) | 432.437 | 825.483 | 1,622.717 | 1,668.098 | 1,702.391 | 1,755.574 | **1,802.733** |
| checker 実秒(自己申告) | 551.331 | 1,023.682 | 1,956.121 | 2,013.378 | 2,041.426 | 2,073.026 | **2,109.440** |
| **P + C** | 983.768 | 1,849.165 | 3,578.838 | 3,681.476 | 3,743.817 | 3,828.600 | **3,912.173** |
| **1 行あたり P+C** | 30.743 | 28.893 | 27.960 | 28.762 | 29.248 | 29.911 | **30.564** |
| 候補六相 合計 | 351.018 | 707.981 | 1,419.982 | 1,422.421 | 1,411.645 | 1,415.426 | **1,420.162** |
| selection(3 相) | 11.880 | 11.963 | 11.836 | 11.871 | 11.832 | 11.948 | **11.953** |
| final separator | 0.869 | 0.893 | 0.936 | 1.020 | 1.086 | 1.165 | **1.247** |
| **計測外の固定費(P 残差)** | 68.670 | 104.647 | 189.963 | 232.786 | 277.828 | 327.035 | **369.370** |
| 出力 ZIP | 94.7 MB | 187.1 MB | 369.2 MB | 377.4 MB | 385.0 MB | 393.8 MB | **403.8 MB** |
| producer cap 使用率(5,400 s) | 8.0 % | 15.3 % | 30.1 % | 30.9 % | 31.5 % | 32.5 % | **33.4 %** |
| checker cap 使用率(10,800 s) | 5.1 % | 9.5 % | 18.1 % | 18.6 % | 18.9 % | 19.2 % | **19.5 %** |

**私の独立集計**: `coverage-receipt.json` の `phase_measurements` **772 本**(= 128×6 + selection 3 + final 1)を全数合算 → **1,433.362383 s**。P 残差 = 1,802.732642 − 1,433.362383 = **369.370259** — cost-receipt の `producer_residual` と **小数点以下まで一致**。

相分解(私の集計): raw 13.142(0.93 %)/ source 32.350(2.28 %)/ primal 307.015(21.62 %)/ **p1 1,019.405(71.78 %)**/ B 9.400(0.66 %)/ reduction 38.850(2.74 %)。**律速は 7 run とも P1 補正相**(primal + p1 = 93.40 %)。

### 7.2 【重大・v6 判読の訂正】層費用は加速していない

v6 判読は層あたり増分 **+42.823 → +45.042 → +49.207**(2 階差 +2.216 / +4.165)を根拠に「線形 n モデルは楽観側に外れる」と書いた。**4 点目は +42.336 で、4 つの中で最小である。**

| 対象 | 7 点フィット | 最大残差 |
|---|---|---:|
| P 残差 | **`26.422 + 1.2642·k + 45.4855·n`** | 2.69 |
| producer 全体 | **`34.642 + 12.3887·k + 44.8864·n`** | 7.78 |
| checker 全体 | `80.505 + 14.7269·k + 36.5851·n` | 11.24 |

k=128 の 5 点だけで 2 次を当てると:

| 対象 | 2 次(最大残差) | 線形(最大残差) | 判定 |
|---|---|---|---|
| P 残差 | `189.24 + 44.395n + `**`0.228`**`n²`(2.560) | `188.78 + 45.306n`(**2.332**) | **線形が良い。n² 不要** |
| producer 全体 | `1624.0 + 38.34n + 1.603n²`(4.705) | `1620.8 + 44.75n`(7.911) | 弱い凸性(未確定) |
| checker 全体 | `1960.0 + 47.52n − `**`2.724`**`n²`(8.605) | `1965.4 + 36.63n`(11.328) | **凹**(符号が逆) |

**⇒ v6 判読の「層あたり増分が単調に増える」は 4 点目で棄却された。3 点の 2 階差を根拠に曲率を主張したのは早計であり、本判読でこれを撤回する。**
**参考(事前登録の照合)**: 司令塔が渡した線形モデル `26.12 + 1.271k + 44.40n` の (128,4) 予測は **366.41 s**、観測 369.370 で **+2.96**。v6 の再フィット `26.63 + 1.2596k + 45.885n` は 371.40 で **−2.03**。**両方 ±3 s に入る。** 数学者の 2 次モデル `T_P(n) = 1,580.7 + 46.68n + 0.5685n²` は producer 全体の (n=4) を **1,776.5 s** と予測し、観測 1,802.733 に対し **−26.2 s**(モデルは n=0..3 でも ±40 s 級に外れており、本 run で改善はしていない)。

### 7.3 【新計器・本判読の最大の収穫】Θ(k·R) が厳密式で確定した

新設計器 3 種(P: `ordered-reductions-timing.v1` ×4 / `parser-bytes-timing.v1` ×4 / `input-preservation-timing.v1` ×1、C: `ordered-reduction-timing.v1` ×4 / `saved-parent-json-parse-bytes.v1` / `input-preservation-timing.v1`)。宣言は honest:
`arrival_timestamp_used_as_internal_timing: false` / `nested_inclusive_times_summed: false` / `inclusive_intervals_added_together: false` / `causal_mechanism_identified: false` / `mathematical_success_inferred: false` / `add_to_inclusive_elapsed: false`。
**P/C とも stderr 全行会計 `unparsed_or_rejected_lines: 0` / `duplicate_count: 0` / `empty_lines: 0` / `all_lines_accounted: true` / `whole_raw_stderr_pin_reread: true`**(P 10,653 行 / 706,928 B・C 17,660 行 / 1,229,633 B)。

**設計の健全性(私がコードで確認)**: C の `OrderedReductionTiming.compare` は `same_json(actual, expected, label)` を**そのまま**呼び、`read` は元と同じ `kind="reduction"` を渡す。`SavedParentJsonBytes.parse` は両分岐とも元の `json_value(raw, role + "/" + name, canonical_required)` を呼ぶ。P 側の observer は例外を再送出し、観測失敗は `observation_error` に記録するだけ。**計器が判定を置き換えている箇所は無い。**

**(a) 要求 2(`ordered_reductions` 要素数)= 実装され、厳密式で閉じた**

| 層(R_i) | 1450 | 1578 | 1706 | 1834 |
|---|---:|---:|---:|---:|
| 実測要素数 | 193,728 | 210,112 | 226,496 | 242,880 |
| **128·R_i + 8,128** | 193,728 | 210,112 | 226,496 | 242,880 |

**完全一致。すなわち層 i の要素数は Θ(k·R_i) であることが回帰なしで確定した**(8,128 = Σ_{i<128} i)。P 側の型検査は **1.23 µs/要素**、C 側の read+compare 窓は **2.61×10⁻⁵ s/要素**(最大残差 0.11 s)。

**(b) 要求 3(hash/parse バイト)= 両側実装され、数学者 §1.3 の予測を的中**

| 層(R_i) | 1450 | 1578 | 1706 | 1834 |
|---|---:|---:|---:|---:|
| P が parse した一意バイト | 129,778,211 | 141,432,282 | 153,185,119 | **164,937,972** |
| C が parse したバイト | 129,778,211 | 141,432,282 | 153,185,119 | **164,937,972** |
| 数学者 §1.3 の予測 | 129.78 MB | 141.43 MB | 153.19 MB | **≈ 165 MB** |
| 1 行あたり | 89,502 B | 89,628 B | 89,792 B | 89,934 B |

**4 層目 164.938 MB は予測 ≈165 MB を誤差 0.04 % で的中。** P と C が同じバイト数を parse していることも独立に一致した。
P `native-metadata` の層時間に対する回帰: **`18.164 + 0.08922 · MB`(最大残差 0.325 s)** — 数学者の **0.0853 s/MB** と 5 % 差。R で書けば `17.895 + 0.0081693·R`。

**(c) ただし「per-byte parse が層費用の主因」ではない**

| 層 | P `native-metadata` | うち read+parse 実測 | 割合 |
|---|---:|---:|---:|
| 1450 | 29.935 | **2.924** | 9.8 % |
| 1578 | 30.458 | **3.050** | 10.0 % |
| 1706 | 31.907 | **3.339** | 10.5 % |
| 1834 | 32.937 | **3.804** | 11.6 % |

parse 部分の傾きは **0.0250 s/MB** で、層全体の傾き 0.0892 s/MB の **28 %** にすぎない。**残り 72 % の R 比例項(hash・expected 構築・deepcopy・canonical)は依然として計器の外側にある。** 数学者 §1.3 の「層費用 = 親候補の Θ(R) JSON 2 本の parse/sha 往復」は **バイト量については的中、時間配分については parse が少数派** と読むべきである。

**(d) 【新規・除去可能な無駄 F-v7-2】P は親 `reduction.json` を 2 回 parse している**

`parser-bytes-timing.v1` の `by_document_kind.reduction.json`: `parse_attempts 256 / unique_documents 128 / repeated_parse_attempts 128`、`repeated_input_bytes` = **64,730,069 / 70,546,389 / 76,411,861 / 82,277,333 B**(層ごと)。`physical-literal.json` は重複 0。C 側は `duplicate_successful_parses: 0` / `duplicate_reads: 0` で重複ゼロ。
**⇒ P の親 JSON parse バイトの 33 %(層あたり 64.7〜82.3 MB)は同一文書の 2 回目である。** 数学者の 642:1 payload 冗長性(構造の問題)とは独立の、実装上の 2 倍読み。**次 run で `reduction.json` の parse を 1 回にできれば、P の層費用のうち parse 相当分(3.0〜3.8 s/層)の約 1/3 が消える見込み**(層全体では 1 s/層 前後・小さい)。

**(e) 新規の run-level 計器**

- C `AcceptedInputs.unchanged` = **21.249 s**(全 19 role の input preservation)。
- P `finish_inputs` = **14.196 s**(`coverage: ALL_TARGET_PARENTS_COMPLETED`・19 role すべて完了)。

### 7.4 【F-v6-2】計器の被覆率(改善したが未閉)

| 層 | P 実測層計 | 被覆(45.486 s/層) | 未帰属 | C 実測層計 | 被覆(36.585 s/層) | 未帰属 |
|---|---:|---:|---:|---:|---:|---:|
| batch-parent | 33.577 | 73.8 % | 11.91 | 17.083 | 46.7 % | 19.50 |
| v4 | 34.231 | 75.3 % | 11.25 | 19.149 | 52.3 % | 17.44 |
| v5 | 35.812 | 78.7 % | 9.67 | 18.724 | 51.2 % | 17.86 |
| **v6** | **36.951** | **81.2 %** | **8.53** | **20.244** | **55.3 %** | **16.34** |

v6 判読時点は P 78.9 % / C 46.8 %。**C は 46.8 → 55.3 % に改善**(`file_bytes` 実値化と ordered-reduction 窓の追加による)。**P も 78.9 → 81.2 %。** 残る未帰属は P ≈ 8.5 / C ≈ 16.3 s/層。
計器が可視化した C 側の総量は **89.478 s(親認証)+ 21.249 s(unchanged)= 110.7 s = C 全体 2,109.44 s の 5.25 %**(v6 は 3.2 %)。**F-k64-7(C の相別 timestamp 不在)は継続。**

**次の 1 手(私からの進言・低コスト)**: (i) P の層内で `native-metadata` を「hash」「expected 構築」「比較」に 3 分割する区間を足せば、残る 8.5 s/層 の大半が閉じる見込み。(ii) C の `state-restore`(11.5〜13.0 s/層 = C 層費用の 65 %)を同様に分割。(iii) `reduction.json` の 2 回 parse を 1 回にする。

### 7.5 壁の更新(**診断であり gate ではない**)

**(a) 積み上げのまま**: `producer(k,n) = 34.642 + 12.3887k + 44.8864n ≤ 5,400` → k=128 で **n ≤ 84.2**。n=4 から **あと 80 run**、行にして 10,240、**rank ≈ 12,330 で頭打ち**(目標 48,384 の **25.5 %**)。v6 時点(12,586 / 26 %)とほぼ同じ。
**(b) k を上げても逃げられない**: 残 46,294 行を N 回に割ると最終 run の producer は最小でも `34.6 + 2√(12.3887 × 44.8864 × 46,294)` = **10,182 s = cap の 1.886 倍**(k\* = 409.5)。v6 の 1.86 倍から実質不変。**係数が 2 倍ずれても結論は変わらない。**
**(c) 回転の見積り**: 新候補の消去相は 38.850 s / 128 候補 / 平均 rank 2,025.5 = **1.498×10⁻⁴ s/(候補×行)**(v5 由来の 1.51×10⁻⁴ / v6 の 1.507×10⁻⁴ を 3 run 連続で再現)。層再認証の R 比例項は 0.00817 s/(層×行)。**v6 判読の外挿(上端で k_max ≈ 250・140〜360 run 級)は本 run の測定でも変わらない。ただし §7.2 の訂正により、n の非線形悪化を前提にした部分は取り下げる。**
**(d) 【新規】層時間の run 間再現性が悪い**: **同じ層(R = 1450/1578/1706)の P `native-metadata` は v6 で 31.386 / 32.273 / 33.382、v7 で 29.935 / 30.458 / 31.907 — 一貫して 1.45〜1.82 s 速い。** v6 の当てはめ残差は ≤ 0.074 s だったが、v7 では ≤ 0.325 s。**「層あたり定数 ≈ 20 s」は run 間で ±2 s ぶれる**(v7 の切片は 17.9〜18.2)。**層費用の定数項を 3 桁で語ってはいけない。**

**この節の外挿はすべて「cost-extrapolation-needs-math-review」に該当する。私は測定値と一次外挿までを提出し、裁定に載せる前の数学者確認を求める。**

### 7.6 その他

- checker 増分 +57.257 / +28.048 / +31.601 / **+36.414**。cap 使用率 19.5 %。
- RSS: P telemetry の最大 `process_ru_maxrss_kib` = **696,400 KiB ≈ 680 MiB**(上限 7,168 MiB・10.5 倍の余裕)。
- 出力 ZIP 393.8 → **403.8 MB**(+10.0 MB)。展開合計 **1,444,771,837 B**。
- **次 run(v8)の登録定数の事前計算(私からの照合材料)**: v7 candidate の zip entry は **12,050 file**(dir entry 0)・**file_bytes 1,444,771,837**・名前から導出される dir が **3,565**(空 dir を足したものが `directories` になる)。**v8 の `BATCH_V7_INVENTORY_REGISTRATION` がこれと違えば、その時点で何かがおかしい。**

---

## 8. (8) 事前登録・恒真性・非空虚性

| 検査 | 結果 |
|---|---|
| `accepted` が [0,128] で固定されていないか | **固定されていない**。`accepted_new_rows` は `len(state.rows)` 由来、`terminal` は 3 分岐、`selection_readout` は `integer(…, 0, BATCH_SIZE)`。該当コードは v6 とバイト同一 |
| `rank == 1962 + accepted` | **2090 = 1962 + 128**。P/C/HEAD/final/progress すべて一致。私は 128 段の鎖から独立に導出 |
| 128 という数の literal 化 | `("accepted_new_rows", 128)` 等の literal は **親(v3/v4/v5/v6)についての登録事実**であり、本 run の結果には課されていない |
| silent cap | **無し**。5 実行の `outer_terminated` すべて False・exit code 5/5 が 0・RSS 上限まで 10 倍の余裕・`partial=False`・`durable_tail=None` |
| `SELFTEST_REJECTIONS` の literal | P `== [30,10,6,7,8,8]` / C `== [28,9,6,7,8]` + `== 10` を source に確認、実行結果・run-receipt と 3 系一致 |
| 選定の判別性 | roster index **110..779**・**gap≠1 が 69/127・最大 gap 70**。「先頭 128 連番」ではない |
| 予言の非空虚性 | `first_candidate` の 5 条件がすべて実測 True で `INDEPENDENT` を予言し的中(5 回目)。`first_independent_prediction_is_conditional: true` の自己申告どおり **条件つき・1 件のみ** |
| 「見つからなかった」を非存在と読んでいないか | `new_lambda_oracle: null`・`failure_set_monotonicity_asserted: false`・`independence_rate_predicted: false`・`new_final_q_computed: false`。**NONMEMBER 主張は一切していない** |
| 個数一致だけで済ませていないか | 済ませていない。§2〜§4 は**バイト同一性**と**代数恒等式**で確認している |
| UNKNOWN の置き場 | `NOT_DECIDED`(grade2)・`NOT_MEASURED`(kernel coverage)・`NOT_ASSERTED`(source_lower_zero)・`NOT_APPLICABLE`(positive_readout / same_word_adapter)・`PENDING`(workshop_CV9)・`UNMEASURED`(新計器の未到達行)が実際に使われている |
| 分岐の非空虚性(coverage-receipt 128 候補) | θ {0:46, 1:37, 2:45}・σ {1:78, 2:50}・`selection_scalar` {1:56, 2:72}・`section_scalar` {0:47,1:39,2:42}・`omega_unrepaired` {0:47,1:42,2:39}・`source_homogeneous_scalar` {0:41,1:40,2:47}・`repair_exponents` **33 通り**・`epsilon_unrepaired` **12 通り**・`raw_slp_letters` 26..12,332・`alpha_support` 5,194..5,472。**修復・符号の分岐は広く発火している** |

---

## 9. 新規/継続の指摘一覧

| 札 | タグ | 内容 | 状態 |
|---|---|---|---|
| **F-v7-1** | **【重大・計画/訂正】** | **v6 判読 F-v6-1 の「層費用は加速する(2 階差 +2.2/+4.2)」は 4 点目(+42.336)で棄却。** 7 点で線形 n が最良(n² 係数 0.228・線形の残差の方が小さい)。壁の数字は実質不変(最良 (k,N) で cap の **1.886 倍**・n ≤ 84 で rank ≈ 12,330 = 目標の 25.5 %)。**司令塔判断(積み上げか回転か)は依然必要だが、「非線形に悪化するから急げ」という根拠は消えた。** | **新設(F-v6-1 を訂正して引き継ぎ)** |
| **F-v7-2** | 【要修正・実装】 | **P は親 `reduction.json` を 1 層あたり 2 回 parse している**(256 attempts / 128 unique・重複 64.7〜82.3 MB/層)。C は重複 0。計器が直接測った、除去可能な無駄 | 新設 |
| **F-v7-3** | 【要修正・記帳】 | **rank 2090 の sealed object が 2 つ存在する**(失敗 run 34492284273 の `400e9e29…` と本走の `31b3d6db…`)。数値 payload はバイト同一・seal のみ相異。v5 の F-v5-5 と同型の再発。**索引・地図・台帳で `rank 2090 = state_head 31b3d6db…` を明示すること** | 新設 |
| **F-v7-4** | 【要修正・再発防止】 | 裁定 2252 の「単一公開登録表」は `audit-region-registry.json` の `new_source_audit` として**実装済みで、値も 8/8 実データと一致**。**しかし P/C はこの表を読まない(driver の静的宣言)。P の `384/512` は依然 literal、C は名前つき定数の和で導出。この非対称が 2251 の直接原因であり、機構的には解消していない。** P 側を C 同様の導出に変えることを進言 | 新設 |
| **F-v7-5** | 【軽微】 | C L322-323 のコメント「Root's actual completed formal handback and final independent P7 pin are pending. The observed 11915 files / … are **not a binding**.」が、**直後の L324 が設定している束縛(および `check_fourth_registered_inventory` の「This independent registration binds that full inventory」)と矛盾する陳腐化コメント**。ラベルを根拠に読む監査を誤らせる(F-v6-3 と同族) | 新設 |
| **F-v7-6** | 【軽微】 | 新計器に identity 由来の依存が 2 箇所: (i) P `require` が **エラーメッセージ literal `batch_saved_full_ordered_reduction_ancestry`** を鍵に型検査開始を検出、(ii) P `OrderedReductionObserver.before_read` が **path literal `/reduction/reduction.json` → `/manifest.json`** の置換で窓を閉じる。**いずれも 2255 と同族だが自己検知型**(空振りすると `status: OBSERVER_ERROR` を吐き run は落ちない)。今回は 4/4 が `COMPLETED` / `observation_error: null` | 新設 |
| **F-v7-7** | 【軽微】 | `run-receipt` の自己申告 key が **版番号入り**(`selection_lambda1834_…` → `selection_lambda1962_…`)。公開 JSON 全体で唯一の改名。literal 名で読む消費者を毎 run 壊す設計 | 新設 |
| **F-v6-2** | 【要修正 → 大幅前進】 | 要求 2(`ordered_reductions` 要素数)と要求 3(C 側 `file_bytes`)が**両方実装され、Θ(k·R) が厳密式 `128R+8128` で確定**。被覆率は P 78.9 → **81.2 %**、C 46.8 → **55.3 %**。**未閉**(P ≈8.5 / C ≈16.3 s/層)。次は `native-metadata` と `state-restore` の内部 3 分割 | 継続(縮小) |
| **F-v6-3** | 【軽微 → 解消】 | 古いラベル残留(`…seventeen_roots…` / `eighteen_registered_roots`)は `…nineteen…` へ更新済み | **解消** |
| **F-v6-4** | 【軽微 → 非該当】 | 今期は公開 selftest 版のコミットが無く、selftest は本走 binary に対する in-run 実行のみ。区別の必要が生じなかった | **非該当** |
| **F-v5-2** | 【軽微】 | `fixture_audit('before-checker')` の被覆窓 | 継続(harness TCB・限定条項 5) |
| **F-v5-3** | 【軽微 → 悪化】 | artifact が持ち込む envelope 履歴は **v4 系列のみ**(`workflow-envelope-v1/v2.yml`)。**今期は自分自身のサイクルで 2 本の失敗 envelope(初版 v7 WF 34,693 B・repair-v1 WF 34,797 B)が生じたのに、どちらも同梱されていない。** 失敗の系譜は Release ミラーと git にしか残らない | 継続(**悪化**) |
| **F-v5-4** | 【軽微】 | `basis-tau.u8` の行索引が**弦序数** [0,1,2,3,5]、`basis_chords` が**辺 id** [2,3,4,6,11] という二重索引が受領証に未明示。誤読すると別解 `[1,1,0,0,0]` が沈黙して出る | 継続(未反映) |
| F-k64-1 | 【解消済】 | DEPENDENT 枝 | v7 でも第 2 群に継続(P `dependent-nonnull-lead` / C `dependent-outcome-resealed`) |
| F-k64-7 | 【軽微】 | C の相別 timestamp 不在。新計器で 3.2 → **5.25 %** まで可視化 | 継続(部分緩和) |

---

## 10. 限定条項(7 条)

1. **射程 = rank 1962 → 2090 の 1 batch のみ**。rank 2090 の λ\* に対する oracle は**未計算**(`new_lambda_oracle = null`)。**NONMEMBER 主張ではない。**
2. **a(128) = 128 は roster 前置 128 本の観測**(batch パラメータ k の性質ではない)。消化率 128 / 36,000 = **0.3556 %**。**Task 988 F4 の反例は排除されていない。** §3.2 のとおり **失敗数が初めて増加した(net +79)ため、roster 枯渇までの見積り自体が定義できなくなった**。
3. **算術 TCB は共有カーネル 2 本を含む**(`vectorized_projection_chunk` / `sparse_adjoint`・P/C 各 1 で計 4 区間)。`current_run_call_coverage = NOT_MEASURED`・`kernel_third_independence_claimed = false`。**第三独立性はこの 2 本に及ばない。** P1 相が候補時間の 71.8 % なので前者は確実に load-bearing。
4. **旧 1,962 行の実バイトは私自身は未取得**。λ_new ⊥ 旧行 と ρ₂ の旧行部分は checker の再現に依存する。**ρ₂ は依然 DERIVED**。**また「選定 λ_1962 が旧 1,962 行を殺す」ことは v6 の性質の継承であり、本 run で私が再測したわけではない。**
5. **harness TCB は単著**(WF 34,800 B + driver 4,457,044 B)。私は harness 出力を根拠に使わず §2〜§6 を生バイトから第三実装で再導出した。ただし **§7.1 の相別秒と §7.3 の計器値は producer/checker の自己計測**である(集計は私が全数やり直した)。
6. **checker の相別 timestamp は依然無い**。新計器で可視化できたのは親認証 89.478 s + `unchanged` 21.249 s = **110.7 s = C 全体の 5.25 %** にすぎない。**F-k64-7 継続。**
7. **私は 404 MB の ZIP を全量ダウンロードしていない**(HTTP Range で必要 entry を個別/一括取得)。ZIP 全体の sha は GitHub API の digest を採り、自分でバイト再計算していない。candidate/diagnostics の同一性判定と親 inventory の全数照合は zip 中央ディレクトリの **size + CRC32** による(主要 file は sha256 で直接検算済み: v6 親 16 本・本 run の 128 行 bin + λ + target + 残差表・source/registry/WF/driver)。**CRC32 一致は sha256 一致の証明ではない。**

### 10.1 前回 7 条との対応

| v6 の条 | 本 run での扱い |
|---|---|
| 1. 射程 1 batch | **継続**(条 1) |
| 2. a(k) の意味・F4 未排除 | **継続 + 質的悪化**(条 2・失敗数が増加に転じ、外挿が定義不能に) |
| 3. 共有 kernel 2 本 NOT_MEASURED | **継続**(条 3) |
| 4. 旧行の実バイト未取得・ρ₂ DERIVED | **継続 + 明記追加**(条 4・選定 λ の旧 span 消滅も未再測) |
| 5. harness TCB 単著 | **継続**(条 5) |
| 6. checker 段別 timestamp 無し | **継続 + 部分緩和**(条 6・3.2 → 5.25 %) |
| 7. ZIP 全量 DL せず | **継続**(条 7) |

**新設は無し。7 条 → 7 条。** F-v7-1〜7 は限定条項ではなく所見として別立て(§9)。

---

## 11. 判読者の限界(正直な申告)

- 旧 1,962 行の実バイトを取得していないので、λ_new ⊥ 旧行 と ρ₂ 恒等式の旧行部分は checker の再現に依存している。
- 「消費した弦が次以降の λ で充足に留まる」ことが**定理として強制されるか**は、受領証だけからは示せていない。4 段先まで |z| ≈ 15.8〜16.0 σ が揃ったので**偶然ではない**ことしか言えていない。
- 語(Ω / P1 / literal)の**再構成**は私の射程外。今回も `target_literal_factor` の三つ組の再検算は行わず、代わりに **target 恒等式を親 artifact の実バイトから 128 段すべて数値で再現**した(こちらの方が強い)。
- `sparse_adjoint` / `vectorized_projection_chunk` が本 run の実行経路で呼ばれた行は特定していない。
- §7.5 の外挿は **7 点フィット + 単一 run の R 傾き**からのものであり、法則ではない。交絡(第 19 親・新計器 3 種のオーバーヘッド・acceptance の 8.34 → 10.67 MB 成長)を私は完全には分離できていない。**ただし §7.5(b) の不可能性は係数が 2 倍ずれても結論が変わらない。**
- **§7.2 の訂正は「v6 の主張を棄却する」ものであって「線形が正しい」ことの証明ではない。** 5 点で 2 次を当てる自由度の問題は残る。**数学者の次数確定を経ずに裁定に載せてはならない。**
- Astra の root 側受領証(root-task1150 / 1160 / 1166 など、`C:\…\Temp\shadow-atelier-audit163\…` の Windows path)は**私の手元に無く未再測(静的主張)**である。私が検証したのは結果物であり、その差分は §1.1 のとおりであった。
- Release `archive-gha-checkpoints` へのミラーは**私は確認していない**(裁定 2251/2255 補記の記録に依拠)。
- **この観点では仕様の齟齬(別対象)を見つけられなかった** — 保証ではない。

---

## 12. CV-9 裁定案・工房格付け案(一行)

**CV-9 = 同一対象(SAME OBJECT)・限定 7 条 → 工房格付け案: checker PASS / cross-checked(限定 7 条)・rank 2090 / gen 8795(state_head `31b3d6db…`)を受理・`verified=false`・GRADE2 NOT_DECIDED・A0 actual 0/1 不変。v6 の 1962 の直系後継として置き換える(合算ではない)。**

**司令塔への一行**: 修理 3 段(初版 → repair-v1 → repair-v2)の差分は **P +20/±0 B・C +40/+50 B が 1 バイトの余りもなく逆置換で説明され**、実体は「親行数 2 定数(256/384 → **384/512**)+ 旧 path 負例 1 行 + deployment identity」だけで、**C の肯定側判定は v7 3 版すべてでバイト同一**。第 19 親 batch-parent-v6 は **11,915 file / 3,582 dir(空 44 を含む)/ 1,395,498,726 B が実バイトで結ばれ**(v6 判読が事前計算した 3 値をすべて的中)、**10-key acceptance の 791 記述子と主要 16 文書が v6 の実 artifact と sha256 一致**、旧 18 親のブロックは **run-local path を除き v6 の acceptance と canonical バイト同一**。fresh λ_1962 の oracle は **残差表 54,433 バイトが完全再現**(failed **36,000**・first 110/212・fit は 243 通り中の一意解)、128 行の階段形・λ の後退代入(48,384 座標)・**v6 の final target から 128 段の target 恒等式**・rolling 鎖・`sha(0x00×2090)` はすべて 128/128 で通り、公開 JSON の key 集合は 18 文書中 16 が完全同一・残る 2 は追加のみ・改名は run-receipt の版番号入り自己申告 key 1 件のみ。**初回失敗 run の P 出力とは「物理行 128 本・λ・target・残差表がバイト同一、差は seal のみ」= 同一数学・別 seal**(ただし **rank 2090 の sealed object が 2 つ存在する**ことは記帳で明示すべき)。**費用では 2 つの重要な訂正/発見**: (1) **v6 の「層費用は加速する」は 4 点目 +42.336 で棄却**(7 点で線形が最良・n² 係数 0.228)、壁は実質不変(cap の 1.886 倍・rank ≈ 12,330 で頭打ち); (2) **新計器が Θ(k·R) を厳密式 `128·R + 8,128` で確定し、数学者 §1.3 の「4 層目 ≈ 165 MB」を実測 164.938 MB(誤差 0.04 %)で的中**、0.0853 s/MB も実測 0.0892 s/MB で追認 — **ただし parse は層費用の 10〜12 % にすぎず、R 比例項の 72 % は依然未帰属**。**F-v6-2 の要求 2/3 は両方実装され被覆率は P 81.2 % / C 55.3 % に前進、F-v6-3 は解消、F-v6-4 は今期非該当。** 新規に **P が親 `reduction.json` を 2 回 parse している(層あたり 64.7〜82.3 MB の重複)** ことと、**2252 の登録表が「宣言」であって「導出源」ではない(P の 384/512 は依然 literal)** ことを挙げる。費用の外挿は裁定 2225 と「cost-extrapolation-needs-math-review」に従い **gate ではなく診断**として提出する。

---

## 付録 A. Astra 側の主張と私の測定の対応

| Astra の主張 | 私の測定 | 一致 |
|---|---|---|
| run 34523172734/1・head bf0b5c0b・全 step success | `runtime-observation.json` / `run-receipt.launch` と一致。exit code 5 本すべて 0・`outer_terminated` 5/5 False | **一致** |
| P/C 双方 PASS | `result.status = PASS` / `checker-result.status = PASS`・`cross_checked: true`・`verified: false` | **一致** |
| 128 追加・rank 2090 / gen 8795 | 128 段の鎖から独立に導出。HEAD/result/checker/final/progress の 5 文書で一致 | **一致** |
| 両 selftest native 0 | P/C とも exit 0・6 群 [30,10,6,7,8,8] / [28,9,6,7,8,10] がすべて PASS。**`old-producer-path` / `old-checker-path` が実際に発火**(fixture 実バイトで確認) | **一致 + 補強** |
| 両 ZIP 各 12,050 files / 1,444,771,837 B | **中央ディレクトリを両方読み entry/名前/size/CRC32 が完全一致** | **一致 + 補強** |
| 変更 = C4 外の旧 path fixture 1 assignment と deployment identity/public pin のみ | **P 2 行 / C 5 行・バイト差 +0/+50 が完全説明**(git 実バイト) | **一致** |
| repair-v1 は親行数定数 2 数のみ(+ identity) | **P 4 行(identity 2 + 定数行 1)・C 4 行(identity のみ)・+20/+40 B が完全説明** | **一致** |
| 4 配置 file の bytes/sha | repo 作業ツリーで 4/4 再計算一致・artifact 同梱コピーとも一致 | **一致** |
| k 128 / max_batches 1 / no-refill・caps 不変 | acceptance の `registration` が **v6 とバイト完全同一** | **一致 + 補強** |
| 19 親・受理済 1962/8667 を親に | acceptance parents 19・`batch_anchor_v6` の 791 記述子が v6 実 artifact と全一致 | **一致** |
| 正式受理は runtime/typed 受領後 | `run-receipt.workshop_CV9 = PENDING`。本判読で rank 2090/gen 8795 への更新を提案 | **手続き一致** |
| root 側受領証(root-task1150/1160/1166) | **TEMP path のため未再測**。ただし登録値そのものは私が実バイトから再計算し一致 | 未再測(値は一致) |

## 付録 B. 主要 pin(私の実測・**bytes のみ**)

- run 34523172734 / attempt 1・head `bf0b5c0b6ee00736481575b98f50ac071fc97e28`・workflow id 355228501
- candidate artifact 10173275037 = 403,815,011 B(zip entry 12,050・展開合計 1,444,771,837 B)/ diagnostics 10173299214 = 403,815,011 B(内容同一)
- 初回失敗 run 34492284273 の diagnostics 10161505854 = 403,520,626 B(12,048 entry・展開 1,443,734,701 B)
- repair-v1 失敗 run 34518126217 の diagnostics 10168815742 = 25,041,369 B(2,049 file)
- 配置(repair-v2): P 552,885 B / C 525,707 B / driver 4,457,044 B / WF 34,800 B
- 配置(repair-v1): P 552,885 B / C 525,657 B / driver 4,457,032 B / WF 34,797 B
- 配置(v7 初版): P 552,865 B / C 525,617 B / driver 4,456,946 B / WF 34,693 B
- v6(親): P 453,972 B / C 428,108 B / driver 2,281,118 B / WF 30,603 B
- registry: 現行 1,815,821 B / v6 保持 867,833 B / v5 保持 499,053 B / v4 保持 236,390 B / historical 76,867 B
- acceptance.json 10,671,359 B(v6 親は 8,338,053 B)/ parent-layout.json 10,670,185 B / result.json 208,916 B / checker-result.json 15,960 B / start.json 349,693 B / parent-intake.json 8,621 B
- cost-receipt.json 377,290 B / coverage-receipt.json 876,903 B / run-receipt.json 682,222 B / shared-tcb.json 16,199 B / source-receipt.json 8,449 B / batch-observation-receipt.json 2,749 B
- parent-timing-receipt.json 6,353,165 B + `parent-timing/**` 47 file
- producer-stderr.log 706,928 B(10,653 行)/ checker-stderr.log 1,229,633 B(17,660 行)
- 保持した envelope: `workflow-parent-v6.yml` 30,603 B / `workflow-parent-v6-driver.py` 2,281,118 B / `workflow-parent-v5.yml` 26,294 B / `workflow-parent-v5-driver.py` 1,145,223 B / `workflow-parent-v4.yml` 22,153 B / `workflow-parent-v4-driver.py` 536,145 B / `workflow-envelope-v1.yml` 599,085 B / `workflow-envelope-v2.yml` 20,296 B(**8 本とも repo とバイト一致**)
- 親: batch-parent-v6 = artifact 10131122423 / 393,848,401 B / 11,915 file / 3,582 dir(名前由来 3,538 + 空 44)/ 合計 1,395,498,726 B
- 親: batch-parent-v5 = 10034053256 / 384,961,441 B / 11,750 / 3,547 / 1,347,269,002 B
- 親: batch-parent-v4 = 10020349387 / 377,383,320 B / 11,648 / 3,525 / 1,308,094,050 B
- 親: batch-parent = 9987222571 / 369,233,546 B / 11,437 / 3,475 / 1,267,599,138 B
- 親: continuation = 9977040548 / 304,642,285 B / 7,916 / 1,265 / 1,046,747,777 B
- λ.bin 12,096 B・target-remainder 12,096 B・物理行 12,096 B ×128(packed3・48,384 trit)
- 残差表 54,433 B / chord-tau 272,165 B / chord-values 54,433 B / failed-indices 144,000 B / failed-edges 144,000 B / potential-tau 272,160 B / potential-f 54,432 B / witness-roster 122,313 B
- 選定 `selection.json` 31,023 B / `selection/start.json` 1,115 B / `final/separator.json` 423,492 B / `final/manifest.json` 1,925 B / `fixed/manifest.json` 2,903 B
- checkout-sources 24 file / audit-history-sources 12 file
- **v8 の登録定数の事前計算値**: files 12,050 / file_bytes 1,444,771,837 / 名前由来 dir 3,565(+ 空 dir)
