# complete oracle CEGAR continuation v1(32 step・rank 1418 候補)増分 CV-9 判読(falsifier 逐語・裁定 2149 で正本化)
著者: falsifier(opus/max・非当事者)。司令塔が scratchpad 報告書(sha256 先頭 16 桁 90662a9098ed8c32・保存ファイル全体)を逐語転記(2026-09-06)。

**工房裁定(2149)**: CV-9 = **同一対象**(3 規約表 diff で統合による弱化なし・交差辺 0・新 pair の最大類似 0.7955/中央値 0.331 で新層は打ち直し・F1 受領証 32/32(row_pairings = sha(0x00×rank_after)・λ·target = 1・λ_j ⊥ 新規行を自前 trit 演算で 32/32 再現)・head 連鎖 32/32・target.scalar 列一致(零 9)・q char0 列一致・chars 1〜3 完全零・κ/score/aux 一致・preserved-input 2,584 file/346,710,509 bytes 全数再 hash で mismatch 0・alias 修理は copy.deepcopy 4 箇所のみで gate 緩和ゼロ(修理は producer 実測値を expected へコピーする方向ではない)・UNKNOWN_CAP は append 数 cap のみ(producer 763 s/5400・checker 755 s/10800))。工房格 = **checker PASS・cross-checked は限定 8 条つき**: (i) 射程 = rank 1386 → 1418 の 32 周回(全 32 step が chord witness 由来・origin/seed 由来 0・failed_chord 10〜62・basis 固定 (2,3,4,6,11)・pivot lead は幅 72 の窓)・NONMEMBER ではない (ii) **F-co-1 = v547 三因子がすべて非自明に実走**(ω 分布 0:17/1:10/2:5・repair-x 18/32・repair-y 15/32・repair-central 15/32)= 2143 F-cy-1 閉鎖。**その代償として F-cy-3 が実効化: ω = 2 の 5 step(2, 6, 21, 22, 28)で sr(2) = −1 ≠ 2(v548 §5 literal)・本 run のどの gate も両読みを区別しない(mod 3 legality は e ≡ 2 で両方満たす・語長上界式は signed 前提)= 5 行は規約選択に依存し得る** → 受理保留は**裁定 2150 で解除**: 工房数学者(GAP 実測 `scratchpad/math_omega2_comm_cube_v1.g`: Δ 内で [r_x,r_y] の位数 3・comm³ = 1・comm⁻¹ = comm²・Γ₀′ 位数 3・Frattini 27; 実装経路では語(SLP)は chain 生成後に物理行へ一切入らず chain は修理因子に非依存(checker L784 ゲート・L782-783 の commutator Fox 零検査・mod 3))と Astra(163 F8.52・(163.52.1)–(163.52.3): c ∈ [N0,N0] ゆえ J_Q0(c) = J_Q2(c) = 0・c³ ∈ Ω・R_(g+3) = R_g c³ は同じ Q2 cycle・v548 (5.1) の同じ Ψ で P1 減算後の物理行が等しい)が独立に**規約非依存**と判定 → **rank 1418 受理**(限定: 物理行はバイト同一だが受領証は SLP 実長で分岐(実 completion の raw-word.json では commutator.length = repair-central.length = 3048・exponent −1・全 actual_slp_length = normalized = 9182; 工房数学者報告の 3046/6092 は自由簡約後の字面長で受領証値ではない — 裁定 2151 で訂正)= 「同じ物理行」であって「同じ artifact」ではない・現行実装は signed に構造固定(語長上界式)・v548 §5 は erratum で sr(ω) へ訂正推奨)(iii) 継承クローンが load-bearing(read_task712_envelope 1.0000・vectorized_projection_chunk 0.99 = 継続 checker v2 L236 が直接呼ぶ新規呼出点・sparse_adjoint バイト同一)・_SeedContext は TCB 外(前回前提の訂正)(iv) base 1386 行分の λ 直交は physical.bin 不在で未再現 (v) F-co-2: `full_four_character_scope: True` は v2 L1493 のリテラルで判別能力ゼロ(実態 = q char1〜3 が 32/32 零・λ_final の台は char 0 内 955 trit)(vi) κ tag1〜5・aux 10 スロット・score tag3〜5・η/τ は 32/32 恒等零 (vii) λ·ρ₂ は DERIVED (viii) raw-word.json の legality.omega = 0 / epsilon_exact_zero = true は修理後 root の値(0 リテラル)で三因子の実走を示さない(誤読注意)。**判読規律(次周回 = resume64 は P/C 同一 sha なので①②③は「source sha 無変更」1 行で省略可・⑤に 3 項追加: ω(w) 分布と repair-central 指数の全 step 列(legality.omega を読まない)・λ の台が char 0 に留まるか・failed_chord 範囲と basis の変化)。GRADE2 NOT_DECIDED・verified=false。

---

# 増分 CV-9 判読 — complete-oracle CEGAR continuation v1 + checker v2 completion

対象: producer run 33984832010/1(cap 1 / resume 32・rank 1386 → 1418・gen 8123・UNKNOWN_CAP・Separator)
      + checker v2 completion run 33988391926/1(保存 output に対し全 32 step replay・success・754.5 s)
判読者: falsifier(非当事者・事後)。判読日 2026-09-06。
親裁定: 2131(continuation 限定 7)・2138(oracle 限定 8)・2143(E 限定 7)・2144(signed 規約)・2145。

---

## 0. 結論(先出し)

**CV-9 三値裁定 = 同一対象(SAME OBJECT)。限定 8 条。別対象・判定不能の余地は見つからなかった。**

**工房格付け案 = checker PASS / cross-checked(限定 8 条つき)。`verified=false`。**

根拠の要約(すべて生バイトから第三実装で再導出):

- 32 step の rolling head 連鎖を instruction.json の生バイトから独立に再構成 → 32/32 一致、終端
  `0c2451e45fb1859f1ebe9f3fcbada1caefffb9f9c9adb222521cd556c3cdc2dd` = HEAD・result・checker-result と一致。
- target.scalar 列 32 個が Astra 報告と完全一致(零 9・一 6・二 17)。
- 全 32 step の `row_pairings_sha256 == sha256(0x00 × rank_after)`。最終は `sha256(0x00 × 1418)` = `e9c1beda…` 一致。
- λ_j·target_j = 1、λ_j ⊥ (それまでの全新規行) を自前の trit 演算で 32/32 再現。
- coverage receipt の q 零 root・packed byte 列・κ・score・aux をすべて raw payload から再計算 → 32×4 で完全一致。
- preserved-input の **2,584 file を全数再ハッシュ → mismatch 0、合計 346,710,509 bytes 一致**。
- 交差辺なし(P 系は `check_*` を一切 import せず、C 系は `d972_*` producer module を import も動的 load もしない)。

**ただし本判読で新たに 1 件の重大な発見がある(§6.1)。CV-9 の「同一対象か」は揺るがないが、
格付け文面と次周回の設計に必ず反映が要る。**

---

## 1. ① 三規約表 diff の検証(F8.43 の主張 vs 実装・実データ)

### 1.1 materializer 表(2117/2143 → continuation 内の各 E)

| 主張(F8.43) | 判読結果 |
|---|---|
| raw 修理 = `w*(rx^3)^(-A/6)*(ry^3)^(-B/6)*comm^sr(omega)`、ordinary 整数 /6、`sr(2)=-1` | **生バイトで確認**。32 step の SLP node から `repair-x` 指数 = -A/6、`repair-y` 指数 = -B/6、`repair-central` 指数 = sr(ω) を確認(例: step 1 の w.exp=[12,-12] → rx_pow=-2, ry_pow=+2)。ω=2 の step で cen_pow=-1 = sr(2) を確認。実装は `check_…materializer_v1.py:441` の `exponent=signed(slp.values["w"]["omega"])`。**規約の弱化なし** |
| 六 cycle を witness 順で保持し係数 0 も削除しない | 確認。witness.json の `cycles` は 32 step とも 6 要素・係数 0 を含む |
| 一行と target: plain 三字段 target、scalar 0 合法 | 確認。`plain_target`(v2:110)が 3 字段厳格・scalar ∈ {0,1,2}。実データに 0 が 9 個 |
| 外部 E 一行を起点で一度付し、loop の新 step だけを別に数える | 確認。`external_e_attached=1`・`external_e_numerically_replayed=false`・`physical_appends=32` |

**統合による弱化: なし。**

### 1.2 oracle 表(2138 → continuation の各 current λ)

| 主張 | 判読結果 |
|---|---|
| 全四 root を current λ から作る・旧 λ の結果を流用しない | 確認。q.bin は 32 step とも shape [4,36288]・全 32 個が別 sha。coverage row j の `lambda_sha256` は step j の親 λ(row0 = 受理済 rank1386 の `a16f4c82…`) |
| 全 8059 等式・全 54433 chord・二 aux | `section_equalities_each=8059`・`chords_each=54433`・`auxiliary_tests_each=2` |
| UNKNOWN_CAP 時の最終未作成 snapshot から complete を推論しない | **確認(コードで)**。`check_terminal`(v2:1180)の UNKNOWN_CAP 枝は `cap_reached` のみを要求し、oracle 結果を一切参照しない。`current_snapshot_sha256=null`・`current_oracle_terminal=null` |
| 限定: current q の零と作用素恒等零を区別 | 確認。coverage は `zero_for_current_lambda` と `operator_identically_zero_claimed:false` を分離。**この分離は正しく守られている** |

**統合による弱化: なし。**

### 1.3 continuation 表(凍結 P/C v1 → 修理 C v2)

| 主張 | 判読結果 |
|---|---|
| P と全保存 output は不変。C の metadata 親列/pairing だけ deep-copy で所有隔離 | **diff で全数確認**(§5)。実質的変更は `copy.deepcopy` 4 箇所のみ |
| gate を弱めず alias を修理 | **確認。gate の緩和は 1 箇所もない**(§5.3) |
| start は rank1386/gen8091 | 生バイトで確認。`output/start.json` の parents = **33 件**、rank 1386、gen 8091、completed_steps 0 |
| 各 snapshot は append 前、step j は snapshot j−1 | 確認 |
| 新 P 0・旧成功 suite 0・新 C 全 32 一回 | receipt で確認(`new_producer_appends:0`・`old_success_suites_rerun:0`・`actual_checker_runs:1`)。workflow に producer 実行 step が存在しない |

**三表とも、統合器による規約の弱化は検出できなかった。**

---

## 2. ② 交差辺・系統分離

静的に全数確認(`search/` 内の import / `spec_from_file_location` 全走査):

- **P 系(6 module)**: `d972_r07_complete_oracle_cegar_continuation_v1.py` → `d972_r07_selected_cycle_materializer_v1.py`
  → `d972_r07_section_cochain_oracle_v1.py` → `d972_r07_full_origin_refinement_v1.py`
  → `d972_r07_fixed_root_packet_loop_v2.py` → `d972_r07_actual_root_seed_materializer_v3.py` …
- **C 系(10 module)**: `check_…continuation_v2.py` → `check_…selected_cycle_materializer_v1.py`(E)/
  `check_…section_cochain_oracle_v2.py`(O) → `check_…section_cochain_oracle_v1.py` / `check_…full_origin_refinement_v1.py`
  → `check_…fixed_root_packet_loop_v2.py` → `check_…actual_root_seed_materializer_v3.py`
  → `check_…actual_grade2_root_scalar_batch_v2.py` → `check_…targeted_grade2_owner_generated_join_v15.py` /
  `check_…rank1355_root_seed_scalars_v1.py`

- **P 系が `check_*` を import する箇所: 0 件。**
- **C 系が `d972_*` を import / 動的 load する箇所: 0 件。**
- C v2 は producer file を **読んで sha を pin するだけ**(`producer_source` v2:705-711)。import していない。
- P/C とも `canonical/sha/seal` を各自定義(P: v1:85-95、C: `O.canonical` 等)。**打ち直しである。**

**交差辺なし。**

---

## 3. ③ クローン(その周回で load-bearing になった関数対)

### 3.1 新 pair(continuation P v1 × C v2)の実測

token 列 difflib 比(top-level def・25 token 以上)。

- 最大 **0.7955**(`cap_reached`、44 token = 3 行の述語)
- 次点 0.7632(`decode_payload` × `typed_input`)、0.7068(`progress` × `boundary`)
- **0.995 以上のペア: 0 件**。top-1 比の中央値 **0.3313**

→ **本周回で新設された continuation 層は両側とも打ち直しである。2143(新 pair 最大 0.8424)と同水準の良好さ。**

### 3.2 継承クローンの所在(依頼の 3 件)

| 継承クローン | 現 TCB か | 本統合器での load-bearing |
|---|---|---|
| `read_task712_envelope`(1.0000) | **あり**(`*fixed_root_packet_loop_v2.py` 両系) | **あり**。`check_…full_origin_refinement_v1.py:379` ほか 3 箇所から呼ばれ、B 表の復号 = 32 本の物理行すべての生成経路上 |
| `vectorized_projection_chunk`(0.99) | **あり**(`*actual_grade2_root_scalar_batch_v2.py` 両系) | **あり。しかも本周回で継続 checker 自身が直接呼ぶ**: `check_d972_r07_complete_oracle_cegar_continuation_v2.py:236` の `BASE.vectorized_projection_chunk(...)`。加えて oracle v2:372・refinement:408 |
| `_SeedContext`(0.9684) | **なし**(`*grade2_violation_materializer_v*.py` は 19/20 source pin に含まれない) | **なし**。本周回では load-bearing でない |
| (参考)`sparse_adjoint`(本文バイト同一) | あり(`*join_v15.py` 両系) | あり(`check_…full_origin_refinement_v1.py:480`)= q の子 root 生成 |

**③ の結論: 新層は独立、最深部の算術(source 射影・随伴・Task712 envelope 復号)は依然として単一系統。
2131 の独立性限定は継続し、`vectorized_projection_chunk` については継続 checker 本体に新しい呼び出し点が増えた。**

---

## 4. ④ F1 受領証(λ ⊥ 全 rank_after 行を 32 step とも)

- コード上: `PhysicalState.measure()`(v2:601-622)が `attach` の末尾で毎回呼ばれ、
  `require(not any(measured) and old_dot == current_dot == 1, "current_all_rows_both_targets_direct_dot")`。
  すなわち **rank_after 全行 × λ = 0 と λ·(親 target) = λ·(新 target) = 1 を 32 回すべて要求**している。
  `attach` はさらに `same(self.direct_pairing, result["separator"]["direct_pairing"])` で producer の受領証とバイト突合。
- 受領証: 32 step すべてで `row_pairings_sha256 == sha256(0x00 × rank_after)`(自前計算で 32/32 一致)。
  最終 rank 1418 は `e9c1beda3e46db46d69eaf028fac326931c2ce5103c2047ea3f6e49a7e824899`。
- **私の第三実装での再現**: λ_j·target_j = 1 を 32/32、λ_j ⊥ (step ≤ j の全新規正規化行) を 32/32 で再現。

**私が再現できなかった部分(正直に)**: 受理済み 1386 base 行との直交性は `state/physical.bin` が本 artifact に
含まれないため再計算していない。ここは checker の `measure()` + 上記 sha 受領証に依拠する(= 二系統一致)。

---

## 5. alias 修理の受領証(3 件)

### 5.1 修理の実体(C v1 → v2 の全 diff = 189 行)

実質的変更は **4 箇所の `copy.deepcopy` のみ**:

- `measure()` の返り値(v1:622 `return self.direct_pairing` → v2 `return copy.deepcopy(self.direct_pairing)`)
- `derived()` の `accepted_target_derivation_parents`
- `summary()` の `accepted_target_derivation_parents` と `direct_pairing`
- 最終 result 組立の `direct_pairing`(v2:1486)

加えて 114 行の `snapshot_isolation_selftest` と CLI mode 1 本。**それ以外の算術・gate・schema・scope は 1 行も変わっていない。**

### 5.2 因果の独立確認(root の静的診断は正しい)

- `root_start_owner`(v2:690-702)は `start = document("start", {**state.summary(), …})` を作る。
  v1 の `summary()` は `self.parents` を**参照で**返すので、`start` が `state.parents` を alias する。
- `replay_head_prefix`(v2:1104)は冒頭で `actual["start_sha256"] == sha(canonical(start))` を検査(このとき親 33 件で PASS)。
- 32 回の `attach` で `self.parents` が 33 → **65** に伸びる。
- 末尾 `head_record(state, start, …)`(v2:1067)が `sha(canonical(start))` を**再計算**するため最終 HEAD だけ不一致。
  → 観測された FAIL 理由 `HEAD_entire_replayed_prefix_and_cursor` と完全一致。
- **実測の裏取り**: 旧 C の FAIL は `phase: "current_physical_all_rows"`・elapsed **753.28 s**、
  新 C の PASS は **754.54 s**。ほぼ同一 = v1 は最後の 1 比較を除き全作業を完了していた。因果診断は妥当。

### 5.3 修理が「gate を弱めていない」ことの確認

**重要**: v1 は同じ `start` を 2 度ハッシュして異なる値を得ていた。1 度目(v2:1104)は親 33 件で
**producer の HEAD.start_sha256 と一致していた**。したがって producer 側の start は 33 件が正であり、
deepcopy はその 33 件版に固定するだけで、**producer の実測値を expected へコピーしに行く方向の修理ではない**。

実測: `sha(canonical(output/start.json))` = `87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b`
= HEAD.start_sha256 = invocation 2 件の start_sha256。parents 33 件。一方、最終 checker-result の
`lambda_rho2.accepted_target_derivation_parents` は **65 件**(= 33 + 32、現在状態として正しく伸びている)。
**start は凍り、current は進む — 修理の意味論として正しい。**

### 5.4 3 件の regression

`snapshot-isolation-selftest.json`(727 bytes / `ac5c37d8…`)の 3 件すべて PASS、
`legacy_alias_control_detected: true`。workflow の jq gate(`…checker-completion-v1.yml:824-830`)が
この 3 件と `legacy_alias_control_detected == true` を**ハード条件**にしている。
逆対照(control)は v2:1683-1693 で旧 alias パターンを故意に再構成し、seal が腐ることを要求する。

**【軽微 F-al-1】** この control は「v1 の実コードを走らせて落ちるのを見た」のではなく
「v1 のパターンを手で再構成して落ちるのを見た」。等価だが厳密には再構成であり、v1 実物の実行ではない。

**【軽微 F-al-2】** 全 gate PASS は「他に alias が無い」ことの証明ではない。
alias は「変異後に再ハッシュされて初めて」露見するので、再ハッシュされない alias は PASS のまま潜り得る。
ただし私の静的走査では `self.parents` / `self.direct_pairing` が外へ出る箇所は
`measure`/`derived`/`summary` の 3 つで全部であり、3 つとも deepcopy 済み(v2:622/664/675)。
`self.pivots`・`self.rows` は document に入らず、`self.target/functional` は numpy で常に sha 化される。
**修理は必要十分と読める。**

---

## 6. 新規発見(重大/要修正/軽微)

### 6.1 【重大 F-co-1】F-cy-1 は閉じた。しかし同時に F-cy-3(紙の齟齬)が**初めて実効化**した

生バイト(`output/snapshots/*/e/raw/raw-word.json` の SLP node)から 32 step 分を抽出した:

| 量 | 実測(32 step) |
|---|---|
| ω(w) の分布 | 0 が 17、**1 が 10、2 が 5** |
| `repair-x` 指数 ≠ 0 | **18 / 32**(値 ±1, ±2) |
| `repair-y` 指数 ≠ 0 | **15 / 32** |
| `repair-central` 指数 ≠ 0 | **15 / 32** |
| 三因子すべて 0 の step | 8(step 0,3,4,8,13,18,24,27) |
| 修理による語長変化 | 例 step 1: unrepaired 162 → normalized **9306** |

**(A) 2143 の限定 (ii) F-cy-1「v547 三因子修理のうち効いたのは 1 因子のみ・中心項は本番で一度も試されていない」は、
本 run で閉じた。中心項 `[r_x,r_y]^{sr(ω)}` は 15 step で実際に非自明に効いている。**

**(B) しかしその代償として、2143 の限定 (iii) F-cy-3 が初めて判定可能領域に入り、かつ本 run のどの gate も判定していない。**

- 紙の齟齬: v548 §5 は `[r_x,r_y]^{ω(w)}`、v547 (4.2) は `[r_x,r_y]^{sr(ω(w))}`(sr = [0,1,-1])。裁定 2144 は signed を採用。
- ω=1 の 10 step では sr(1)=1=ω なので依然区別不能。
- **ω=2 の 5 step(step 2, 6, 21, 22, 28)では sr(2) = −1 ≠ 2。両読みは異なる語を生む。**
- 実装は sr を使っている(`check_…materializer_v1.py:441`、実データの cen_pow=−1 で確認)。
- **かつ、legality gate は両者を区別しない**: 交換子 node の ω 値は 2、`comm^e` の ω は 2e mod 3。
  root の ω ≡ 0 を要求すると 2 + 2e ≡ 0 → e ≡ 2 (mod 3)。**e = −1 も e = 2 も等しく満たす。**
- 語長 gate も区別しない: `check_…materializer_v1.py:796` の上界式が `2*abs(signed(ω))*(1058+466)` と
  **signed 規約を前提に書かれている**。実測でも全 32 step で `actual_slp_length == normalized`(等式)。
  つまり長さ検査は規約の外部検証にならない(自己整合の対)。
- 注: `raw-word.json` の `legality.omega`(= 0)と `epsilon_exact_zero`(= true)は
  **修理後 root の値**であって修理前 w の値ではない(`check_…materializer_v1.py:811` は `omega` を 0 リテラルで書き、
  `epsilon_exact_zero` は `not any(slp.values["raw-root"]["exponent"])`)。
  **これを「三因子が効いていない証拠」と読むと誤読になる。** 本判読は SLP node の `w` 値から直接読み直した。

**帰結**: rank 1386 → 1418 の 32 行のうち **5 行は規約選択に依存する**。
`[r_x,r_y]^{-1}` と `[r_x,r_y]^{2}` が同じ物理行を与えるか(= 対象商で交換子が位数 3 か)は本 run で**未検査**。

**CV-9 判定への影響: なし。** P も C も同じ v547/2144(signed)を宣言し、同じ signed を実装している。
両者は**同一対象を計算している**。しかし **格付け文面には必須の限定**であり、
「rank 1418 を受理」の前に、ω=2 の 5 行について規約非依存性(または裁定 2144 の数学的正当性)の別便が要る。
これは Sol/数学者の領分なので、私からは事実の提示までとする(CV-9 スコープ制限に従う)。

### 6.2 【要修正 F-co-2】`full_four_character_scope: True` は測定されていない定数で、workflow gate も空虚

- `check_…continuation_v2.py:1493` は `"full_four_character_scope": True` を**リテラルで**書く。
- workflow の jq gate(`…completion-v1.yml:859`)は `.full_four_character_scope == true` を検査する
  = **PASS 側では常に真。判別能力ゼロの gate。**(FAIL 側は字段自体が無いので shape 判別の役には立つ)
- 一方、生バイトの実態は:
  - q.bin は 32 step とも **character 1,2,3 が完全に零**(私の再計算で 32/32 確認)。
  - **λ_final の台は character 0 ブロック内のみ**(非零 955 trit、[12096, 48384) には 0 個)。
  - 32 本の pivot lead はすべて **[1458, 1529]**(character 0 ブロック内、幅 72 / PHYSICAL 48384)。
- coverage receipt は `all_four_characters_informative_claimed: false` と正直に書いており矛盾はないが、
  **checker-result の字段名が誤読を招く**。「四 character 分のバイトを比較した」意味であって
  「四 character が情報を持つ」意味ではない。字段名を `four_character_bytes_compared` 等へ改名するか、
  gate から外すことを推奨。同様に `section_equalities_each` 等も PASS 側では定数。

### 6.3 【軽微 F-co-3】空虚性の残り(2143 (v) の継続・32 step でも不変)

生バイトから全 32 step で確認:

- κ: **tag 0 のみ台。tag 1〜5 は d0/d1 とも恒等零。shared aux 8 スロット全零。b_aux [0,0] 全零。**
- score: tag 0 は両 component 非零、tag 1/2 は component 0 のみ、**tag 3/4/5 は両 component 零** — 32 行すべて同一パターン。
- witness: `eta = [0,0]`・`tau = [0,0,0,0,0]` が 32/32。`normalized_pair = [0,0]` が 32/32。
- **6 source tag のうち 3 本と補助チャネル全体は 32 周回で一度も励起されていない。**

### 6.4 【軽微 F-co-4】探索の射程が極めて狭い

- witness は 32/32 が `kind: "chord"`。**origin/seed 由来の step は 0 件**(依頼の「pivot 由来」への回答)。
- `failed_chord` は **10〜62**(CHORDS = 54,433 のうち 0.1 %)。
- `basis_chords` は 32/32 で **同一の (2,3,4,6,11)**。
- pivot lead は 72 幅の窓に集中(§6.2)。
- q の character 0 非零 packed byte は最大 1095 / 9072 = **12.07 %**。

### 6.5 【軽微 F-co-5】語長上界は等式(2143 F-cy-2 の継続)

32 step すべてで `word_bound.actual_slp_length == word_bound.normalized`。上界ではなく計算式であり、
上界検査としては恒真。

### 6.6 UNKNOWN_CAP の性質(依頼の ⑤ 項目)

- producer `result.json`: `terminal = UNKNOWN_CAP`、`max_appends_this_invocation = 32`(絶対 cap)、
  `max_seconds_this_invocation = 5400.0`、**`elapsed_seconds = 763.237643`(= 14.1 %)**。
- invocation は 2 件: ①cap 1 / 1800 s / resume=false、②cap 32 / 5400 s / resume=true(completed_steps_before=1)。
- checker: `--max-seconds 10800`、外 190 分、job 230 分、`ulimit -v 7 GiB`。**実測 754.54 s(= 7.0 %)**。

**UNKNOWN_CAP は完全に「append 数の cap」で止まったものであり、時間・資源には一切余裕がある。**
資源終端(UNKNOWN_RESOURCE)ではない。checker の ResourceStop は exit 3 で workflow の `test "$code" = 0` に落ちる
= 資源停止を PASS に転換する経路はない(v2:1799-1803、`…completion-v1.yml:851`)。

---

## 7. ⑤ 入力 pin・終端受領証の第三実装再計算(実施内容一覧)

自前実装(project module を一切 import せず、canonical/sha/pack/unpack/dot を独立に書いた)で以下を再導出:

| 検査 | 結果 |
|---|---|
| artifact ZIP 実体 | 102,582,146 bytes / `9f51b03805ca9de08669111e7aeb3acfc8169ff31cee4d27f1383c52bf5c96b1` = API digest 一致・2,699 entry |
| output/HEAD・start.json・result.json の canonical/seal | 一致 |
| head 連鎖 32/32(`sha(bytes.fromhex(prev)+canonical(instruction−rolling))`) | **32/32 一致**、終端 `0c2451e4…` |
| rank/generation の単調性 | 1386+j+1 / 8091+j+1 を 32/32 |
| target.scalar 列 | `[1,2,2,2,2,0,1,2,0,0,1,2,0,2,2,0,0,0,1,0,2,2,2,1,0,2,2,2,1,2,2,2]` = Astra 一致(零 9) |
| row_pairings = sha(0x00×rank) | 32/32 + 最終 1418 |
| λ·target = 1 / λ ⊥ 新規行 | 32/32(自前 trit 演算) |
| lead の相異・character 0 内 | 32 個すべて相異・すべて < 12096 |
| q char0 非零 packed byte 列 32 個 | `[1062,1062,1053,…,1095,1095]` = Astra 一致・coverage 一致 |
| q char 1,2,3 の零 | 32/32 で完全零(生 q.bin から) |
| κ tag0 d0+d1 / tag1-5 零 / shared aux 零 / b_aux 零 | 32/32 一致 |
| score 6 tag × 2 component | 32/32 で coverage 一致(パターン 1 種) |
| coverage の payload sha/bytes(32×4) | 全一致 |
| **preserved-input の 2,584 output file 全数再ハッシュ** | **mismatch 0 / 346,710,509 bytes 一致 / 420 dir** |
| preservation-result の全 file 再ハッシュ | mismatch 0 |
| all-parent-files before/after | **バイト同一**(14 親) |
| repo の 20 source sha vs repair-source-receipt | 全一致(checker v2 = `e985b4ca3922fc4f…` = checker-result.checker_sha256) |
| oracle v2 full selftest receipt | 869 bytes / `094f69ed…` = Astra 申告一致・4 件 PASS(F-sc-3 の閉鎖材料) |
| 旧 C の FAIL 本文保存 | exit 1・`HEAD_entire_replayed_prefix_and_cursor`・別来歴で保存(遡及格上げなし) |

TCB: **20 source(P 系 9 + C 系 10 + 修理版 v2)+ データ pin 3**(a0_paper_words_v1.json / a0_v2_words.json / fuda1_a0_rmax_data.g)。

なお coverage-receipt を作るのは workflow 内のインライン script(`…completion-v1.yml:873-960`)であり、
算術は再計算せず(`source_recomputed:false`・`producer_reexecuted:false`)バイトを数えるだけ。
その数え直しを私が独立に行い一致したので、coverage の数値は三重に導出されている。

---

## 8. CV-9 裁定案・工房格付け案(一行)

> **CV-9 = 同一対象(限定 8 条)。工房格 = checker PASS(交差辺なし・新 pair にクローンなし(最大 0.7955 = 3 行述語・中央値 0.331)・
> 32 step の head 連鎖/target.scalar/row_pairings/q・κ・score 内訳を非当事者が生バイトから第三実装で全数再導出し一致・
> 保存 output 2,584 file/346,710,509 bytes を全数再ハッシュして不変を確認・alias 修理は deepcopy 4 箇所のみで gate の弱化ゼロ・
> 逆対照(旧 alias)を hard gate 化・cap は append 数のみで時間は producer 14 %/checker 7 %)・cross-checked は限定 8 条つき** —
> (i) 射程 = rank 1386 → 1418 の 32 周回のみ・**rank 1418 の λ に対する oracle 計算は存在しない**
> (`current_snapshot/checkpoint = null`)・依然 Separator・MEMBER/NONMEMBER いずれでもない
> (ii) **F-cy-1 は閉じた**(三因子すべて実走: x 18/32・y 15/32・central 15/32)
> (iii) **【新】F-cy-3 が実効化**: ω(w)=2 が 5 step で発生し sr(2)=−1 ≠ 2 = v548 §5 の literal 読み。
> 本 run のどの gate も両読みを区別せず(mod 3 legality は e≡2 で両立・語長上界式は signed 前提)、
> **32 行のうち 5 行は規約選択に依存する**
> (iv) informative は character 0 のみ(q char1-3 は 32/32 で完全零・λ_final の台は char 0 内 955 trit のみ)
> (v) κ は tag 0 のみ台・tag1-5 と aux 10 スロットは 32/32 で恒等零・score tag3-5 も 32/32 で零
> (vi) 探索射程は witness 32/32 が chord・failed_chord 10〜62(0.1 %)・basis 固定 (2,3,4,6,11)・lead は幅 72 の窓
> (vii) **独立性は最深部で単一系統**: `read_task712_envelope`(1.0000)・`vectorized_projection_chunk`(0.99・
> 今回は継続 checker 本体 v2:236 から直接呼ばれる)・`sparse_adjoint`(バイト同一)が両系 TCB で load-bearing。
> `_SeedContext` は本周回では非 load-bearing
> (viii) λ ⊥ 受理済 1386 base 行は checker の measure() と sha 受領証に依拠(判読者は再現していない)・
> λ·ρ₂ は 2117 の DERIVED 前提を継承・base 行/B 行列/P1 cache 由来は二系統一致のみ。
> GRADE2 NOT_DECIDED・full_A0 false・verified=false。**受理 rank 1386 を維持し 1418 は候補**という Astra の境界維持は妥当。

---

## 9. 次周回(Task 980/981 = 同じ保存 output から resume 64)の判読範囲

**⑤ のみでは不足。以下の最小構成を推奨。**

前提の確認(私が resume64 workflow を読んで確定した事実):

- producer sha は同一(`67d2302c3c4d571a…`)、checker は同じ v2(`e985b4ca3922fc4f…`)。
  → **①②③ は「両側 source sha 無変更」の 1 行確認で省略してよい**(2131 改訂規律の「同一 pair 継続 run」に該当)。
- `--resume --max-appends 64 --max-seconds 5400`、RESUME_CAP_MINUTES 100、job 330 分。
- checker は毎回 start から全 prefix を replay するので **64 step 全部**を再生する。
  現行実測から外挿すると checker ≈ 1,500〜1,700 s / 上限 10,800 s。**cap 余裕は十分**(約 6〜7 倍)。
- resume64 workflow は完成 completion の 10 entry を exact sha で pin 済み(`COMPLETION_ENTRY_PINS`)であり、
  私が §7 で照合した 10 件と一致する。

**必須 ⑤ 項目(前回同様)**: head 連鎖 64/64・target.scalar 列(零の個数)・row_pairings = sha(0x00×rank)・
q 零 root と char0 内訳・κ/score/aux 内訳・preserved-input 全数照合・UNKNOWN_* 時の実測秒 vs cap。

**追加すべき 3 項目(本判読で発生した理由つき)**:

1. **ω(w) 分布と `repair-central` 指数の全 step 列**(§6.1)。ω=2 が再び出るなら、
   **その step 数を格付け文面に明記し、規約非依存性の裁定が出るまで「規約選択に依存する行」として札を付ける**。
   `legality.omega` を読むのは誤り。SLP node の `w` 値を読むこと。
2. **λ の台が character 0 に留まるか**(rank が伸びても char 1-3 に台が出ないか)。
   出れば射程限定 (iv) が変わる大きな進展であり、出なければ限定を継続。
3. **`failed_chord` の範囲と basis の変化**。62 を大きく超える chord や別 basis が出れば射程 (vi) が更新される。

**①②③ を復活させる条件**: producer か checker の source sha が変わったとき、
または継続器が新しい module を TCB に取り込んだとき。

---

## 10. 判読者の限界(正直な申告)

- 受理済み 1386 base 行との λ 直交性は、`state/physical.bin` が本 artifact に含まれないため**再計算していない**。
- 各 phase の算術本体(section/cochain/tree/raw/source/primal/p1/B)は checker が producer バイトと突合した
  結果を受け入れており、**私が第三実装で再計算したのは §7 の表に挙げた量のみ**。
- §6.1 の「5 行が規約選択に依存する」は、`[r_x,r_y]^{-1}` と `[r_x,r_y]^{2}` が**語として異なる**ことに基づく事実で、
  それらが対象商で同じ物理行を与えるか否かは**私は判定していない**(数学的判断は CV-9 のスコープ外)。
- 「この観点では穴を見つけられなかった」= 保証ではない。特に §5.4 F-al-2 のとおり、
  再ハッシュされない alias の不在は証明されていない(静的走査で十分と読めるが証明ではない)。

---

判読ファイル: `C:\Users\81905\Desktop\shadow-atelier\scratchpad\fal_cv9_cegar_cont_v1_report_v1.md`

sha256(this file, excluding this line) = b5b687489e4efa25
