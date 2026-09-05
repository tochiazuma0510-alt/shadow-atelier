# CV-9 増分判読 — R07 section cochain oracle v1(producer v1 × checker v2 completion)

判読者: 反証前哨(非当事者)/ 2026-09-06 / 対象 = run 33975617653(producer 完走・checker v1 FAIL)+ run 33977701313(checker v2 completion・PASS)

---

## 0. 結論(先出し)

- **CV-9 三値裁定: 同一対象(SAME OBJECT)。**
  紙 v548 §2–5 / v543 §3–4 の宣言、producer、checker v2 の三者は同一の有限対象
  (F_λ = λH − (λHs)π を section 補正した cochain f と 5 係数 tree potential 試験)を計算している。
  規約(qid 順・edge 順・tree 順・chord 順・monomial 順・handedness・carry 規約・witness 規則)は
  §2 の対応表で全項一致。当哨は**第三実装で score(653,184 値)と f(108,864 値)と tree 段全配列を
  バイト単位で再現**したので、「同一対象」は宣言の突合だけでなく実測で裏付けられている。

- **工房格付け案: cross-checked(限定 8 条)。**
  「rank 1385 の現 λ に対し、section cochain oracle が VIOLATION_CANDIDATE(高々 6 基本閉路の
  合法組合せ・τ=0・scalar=1)を返した」は照合済みと呼べる。**MEMBER でも NONMEMBER でもない。**
  Lean verified ではない。§7 の 8 限定を格付け文面に同梱すること。

- **今回の目玉(前周回になかった所見)**: ①**非クローン錨の被覆率が桁違いに改善**した
  (前周回 26/838,136 ≒ 0.0031% → 今回は score/f/tree 段が **100%** 第三実装で一致)。
  一方 ②**空虚性が広い**: 4 本の B_a 随伴のうち 3 本が恒等的に零、24 個の (tag,character) 係数塊の
  うち 18 個が零、tag 3/4/5 の score は恒等的に零、8 スロットの shared aux 結合は全て零。
  ③ 継承 TCB に**バイト同一クローンが 2 本、両系統で load-bearing** に入っている
  (`read_task712_envelope` 1.0000、`_load_words` 1.0000)。2131 の F-fo-1 と同型の新規指摘。

---

## 1. 実測した受領証(当哨の再計算)

| 項目 | 値 | 出所 |
|---|---|---|
| completion run / head | 33977701313 / `bbce98d8f95a845f36fe89c0f507b9360792666f` | `completion-run-receipt.json` |
| checker status / terminal | PASS / **VIOLATION_CANDIDATE** | `checker-result.json` |
| chords_checked / section_equalities / auxiliary_tests | 54,433 / 8,059 / 2 | 同上 |
| all_stage_arrays_compared / candidate | true / true(cross_checked=false, verified=false) | 同上 |
| rank / generation / state_head | 1385 / 8090 / `8f6605a2…` | 同上 |
| direct_pairing | rows 1385, pivots 0, parent=new=1, `494e89ee…` | 同上 |
| **`sha256(0x00 × 1385)` 外部再計算** | `494e89ee3b969705b4a04b4809d38f051788e3d4b98260af746e0971210a670d` **一致** | 当哨 |
| producer_invocations / old_success_suites / old_parent_canaries | 0 / 0 / 0 | receipt + workflow 本文で構造的に確認 |
| output/ 44 ファイル 5,361,492 B の不変 | **origin run 1 の展開物と全ファイルバイト同一**(当哨が独立照合) | 当哨 |
| preserved-input 53 件 | 全件 hash 一致。うち 2 件は `checker-result.json`→`previous-checker-result.json` 等の改名 | 当哨 |
| TCB | producer/checker 7 対 = 14 ファイル + 修理 checker 1 = 15、全て live repo とバイト一致 | 当哨 |
| raw data pin | `a0_paper_words_v1.json` 115,928/`90ba6033…`、`fuda1_a0_rmax_data.g` 4,709/`625b4d11…` — live 一致 | 当哨 |
| 全 seal / canonical bytes | stage 4 + top 5 + checker-result の **全 JSON で seal 再計算成功・ファイル = canonical bytes** | 当哨 |
| stage manifest | 4 段 × 全 payload の bytes/sha 一致・roster exact・top manifest の stage hash 一致 | 当哨 |

**入力 pin の三点一致**: 受理 parent artifact `9971466432` は completion workflow env・oracle workflow env・
producer literal・checker literal の 4 箇所に出現し、`REFINEMENT_ARTIFACT`(7 フィールド)と
`REFINEMENT_FILES`(**10 件**)は producer と checker v2 で **AST 比較して完全一致**。
961 F12 が指摘した 8 件 vs 10 件のズレは解消済み(当哨が再確認)。

---

## 2. 主検問相当 — 紙の宣言 ↔ producer ↔ checker の規約対応表

| 紙の宣言 | producer | checker v2 | 判定 |
|---|---|---|---|
| v548 (2.2) χ(b_i)=Σ_a⟨B_a*λ, z_i[a]⟩ | `current_roots_and_values` L443(`ARITH.sparse_adjoint` + 自前 dense unpack、16 行 chunk) | `current_roots_and_contractions` L351(`FIXED.pullback` + `BASE.vectorized_projection_chunk`、256 行 chunk) | 同一。実測: `chi == Σ_a p1_values mod 3` を生バイトで確認 |
| v548 (4.3) ⟨κ,b_i⟩=χ_i を **full 96,776 座標**で・free=0・共有 aux を 4 複製しない | `interpolate_rows` L426(元 lead 降順・`answer[lead] = (χ − dot)%3`) | `interpolate_rows` L381(同式・row ID 保持) | 同一。実測: lead-embedded 埋込式(old d0 = a·6048+L / old aux = 96768+L−6048 / new = 24192+a·18144+L)を **8,059 行全数で検証、違反 0**。8,059 残差全零、free 座標 0 |
| v548 (5.2) f = Σ_a q_a Ψ2[a] − κΨ1 | `score_array` L589(`_seed_e_poly` × 10 単項式)+ `raw_edge_pullback` L619 | `source_scores` L270(27×27 cyclic-difference 基底の逆行列)+ `raw_edge_cochain` L315 | 同一。**当哨の第三実装が両者の score をバイト再現**。単項式順 `SEED_MONOMIALS == checker MONOMIALS`(10 項・実測一致) |
| Fox は `phi_j(q)*prefix` の LEFT 積、正 edge は RIGHT 積、qnorm は右 X / 右 XB=Y⁻¹ | `next[s,0]` / `prev[s,1]`、`maps.at(prefix)[phi]` | `multiply(vertex,x)` / `multiply(right_x, (Y·X)⁻¹)` = s·Y⁻¹ | 同一(代数的に等価・当哨の第三実装で f 一致により実測確認) |
| v546 5 legality 行 = 3 rotation carry + 2 exponent 行、carry は mod3 前の整数差/3 | `geometry_inputs` L390–399(rotation9=(1,0,0),(8,1,8) を **literal**、`validate_marking` L288 が pinned file と突合) | `Geometry.actual_q0_marking` L241(pinned file から sign·k mod 9 を**導出**) | 同一。carry.u8 バイト一致 |
| v543 (3.2)(3.3) tree potential と r_e, t_e | `integrate_tree` L654 + `chord_values` L677 | `complete_tree_test` L502 内 | 同一。**当哨が potential/chord/τ を全数再現** |
| v543 (3.4) 独立 τ 5 本を選び a を解く | `first_independent` L684 + `solve_five` L705(Gauss-Jordan) | `first_independent_columns` L483 + `inverse_matrix_mod3` L86(逆行列) | 同一(a·T = r_sel の向きが一致)。**当哨が 3⁵ 全探索で fit=(0,2,1,0,2) が一意解であることを確認** |
| v548 (5.4) 零 ⟺ b_aux=0 かつ 全 54,433 chord | `classify_complete` L722 | `complete_tree_test` L529 以降 | 同一。優先順 aux x → aux y → 最初の failed chord も一致 |
| v543 (4.1) 高々 6 基本閉路・係数 0 も残す | 6 項 receipt(1 + 5) | 同 | 同一。**当哨が d=(2,0,2,2,2) の一意性を 3⁵ 全探索で確認**、cycles=(1,1,0,1,1,1)、τ=0、scalar=1 |
| 終端命名 | `COMPLETE_ZERO_CANDIDATE` / `VIOLATION_CANDIDATE` | 同(checker は**自分の tree 結果から**終端を導出し、producer の result.json とバイト比較) | 同一 |

**分離条件・ダミー検査の同梱**: 両側に実在する。producer selftest = 非単調元 lead / 非閉 edge の d0·d1·d2·η
(edge 85692 で degree 0,1,2 の 3 プローブ)/ chord 後端 EOF・6 cycle・aux 優先。checker selftest = 4 群
(うち **`late_witness_edge: 108862` の後端改変と偽 EOF で `simultaneous_array_errors_detected: 2`**)。
「何にでも当たる試験」ではない。ただし §5 の空虚性は別問題。

---

## 3. 独立性(交差辺・類似度・クローン)

### 3.1 交差辺 — なし
- producer は producer 系統のみ import(`d972_r07_full_origin_refinement_v1` `d7e32aad…` を pin → fixed_root_packet_loop_v2 → materializer_v3 → batch_v2 → v15)。
- checker は checker 系統のみ import(`check_d972_r07_full_origin_refinement_v1` `1ee388c9…` を pin)。
- checker は producer source を **hash するだけ**(`producer_source_receipt` L962)で import しない。
- checker の `candidate_root` は `check_actual` の比較根にのみ使われ、算術 4 段(geometry/section/cochain/tree)には一切渡らない。**producer の出力を読んでから計算する経路は存在しない。**

### 3.2 新 pair の類似度(token 化 SequenceMatcher・autojunk 両方)

| producer | checker v2 | AJ=True | AJ=False |
|---|---|---:|---:|
| `geometry_inputs` | `Geometry.__init__` | 0.1404 | 0.3029 |
| `positive_tree` | `Geometry.positive_tree` | 0.6452 | 0.6452 |
| `validate_marking` | `actual_q0_marking` | 0.1664 | 0.2906 |
| `RightMaps.at` | `Geometry.multiply` | 0.3741 | 0.3741 |
| `current_roots_and_values` | `current_roots_and_contractions` | 0.4080 | 0.5382 |
| `interpolate_rows` | `interpolate_rows` | 0.3050 | 0.6536 |
| `current_section` | `current_section` | 0.3081 | 0.4412 |
| `score_array` | `source_scores` | 0.1540 | 0.3939 |
| `raw_edge_pullback` | `raw_edge_cochain` | 0.2594 | 0.3821 |
| `first_independent` | `first_independent_columns` | 0.5729 | 0.6598 |
| `solve_five` | `inverse_matrix_mod3` | 0.1797 | 0.6119 |
| `classify_complete` | `complete_tree_test`(統合) | 0.3818 | 0.5156 |

**新 pair にクローンはない**(最大 0.66)。前周回の 1.0000 / 0.9908 とは質が違う。

### 3.3 継承 primitive で「今周回に load-bearing になったもの」(改訂規律 ③)

| 継承関数対 | AJ=T | 今周回どちらが使うか | 評価 |
|---|---:|---|---|
| `sparse_adjoint` | **1.0000**(本文バイト同一) | **producer のみ**(checker は `FIXED.pullback` = `np.add.at` 版) | 共有故障経路ではない。ただし §5 の空虚性により実質比較は 4 本中 1 本 |
| `vectorized_projection_chunk` | 0.9908 | **checker のみ**(producer は自前 dense unpack) | 同上・片側のみ |
| `_seed_e_poly` | 0.9867 | producer は**本番**、checker は **canary のみ**(本番は cyclic-difference) | 独立性成立。当哨が両表の一致を第三実装で確認 |
| `_seed_affine_mul/fox/inv`, `_seed_perm_mul` | 0.92–0.98 | producer は本番、checker は canary のみ(本番は自前 `psl_product`/`multiply`/`linear_fox_terms`) | 独立性成立 |
| `checker_stream_dots` | 0.795 | **checker のみ** | 片側のみ |
| **`read_task712_envelope`** | **1.0000**(1,552 token・本文バイト同一) | **両側**(B_a テーブルの復号) | **新規指摘 F-sc-1** |
| **`_load_words`** | **1.0000**(159 token) | **両側**(raw word JSON 読取) | **新規指摘 F-sc-1** |
| **`_SeedContext` / `_CheckerSeedContext`** | **0.9684**(616 token) | **両側**(psels/psidx/images/**transport**/pb3_b) | **新規指摘 F-sc-1** |
| `source_context` / `checker_source_context` | 0.9254 | 両側(上記 class の薄いラッパ) | 2131 で既出 |
| `_state_descriptor` / `state_descriptor` | 0.6311 | 両側(descriptor/pin 検証) | クローンではない |

**F-sc-1**: 入力層(生 word・PSL 列挙と順序・generator images・**六 tag の transport 表**・Task712 の
B テーブル復号)は**両系統でバイト同一/0.97 クローンの単一実装**。したがって
「B の読取規約の誤り」「transport 表の誤り」「PSL 順序の誤り」は二系統一致では**検出されない**。
2131 の F-fo-1 と同型で、今周回で新たに load-bearing になった分。名前つき入力前提として格付けに明記が必要。

### 3.4 全 stage 配列の再計算と突合
`check_actual` L997–1062 は geometry/section/cochain/tree の 4 段を**自分で計算し直し**、
`compare_complete_stage` L708 が **exact roster + 全 payload の完全バイト + 1 バイト超読による EOF 厳格化**で比較、
さらに top の owner/start/source/result/manifest を同様に比較し、`require(not errors, …)` の後にのみ PASS を返す。
`all_stage_arrays_compared: true` は自己申告フラグではなく、この gate の後段。

---

## 4. 当哨の第三実装による再計算(非当事者・生バイトから)

producer・checker のどちらのコードも呼ばずに書いた独立実装で、封印配列から以下を再現した。

| 再導出したもの | 規模 | 結果 |
|---|---|---|
| 27×27 cyclic-difference 展開と 27×10 moment 表 | 全数 | `expansion_sha256` `502719a4…` / `moments_sha256` `13a57d81…` が **cert と一致**、かつ **producer の `_seed_e_poly` 表の hash と同一**(= 二経路が同じ 27×10 表を出している) |
| PSL 積 `(p*q)[j]=q[p[j]]`・affine 群積・右 generator 作用 | 504²/54,432 | `right_mul(v,X)==next-pos[:,0]`、`right_mul(v,Y)==next-pos[:,1]` |
| `score.u8` | 6×2×54,432 = **653,184 値** | **バイト一致** |
| `f.u8` | **108,864 値** | **バイト一致** |
| `b_aux` | 2 | `[0,0]` 一致(= −κ_aux[6:8]) |
| tree potential(f・τ) | 54,432 + 54,432×5 | **バイト一致** |
| chord values / τ | 54,433 + 54,433×5 | **バイト一致** |
| 5 本選択 | — | `[2,3,4,6,11]` 一致 |
| fit | 3⁵ 全探索 | `(0,2,1,0,2)` が**一意解**・cert 一致 |
| 全 chord 残差 | 54,433 | **バイト一致**、非零 **36,343** 一致 |
| witness の d | 3⁵ 全探索 | `(2,0,2,2,2)` が**一意解**・cycles `(1,1,0,1,1,1)`・τ=0・**scalar=1** 一致 |
| 8,059 式の内部整合 | 全数 | `chi == Σ_a p1_values mod 3`、`equation_values == chi`、残差全零 |
| lead-embedded 埋込式 | 8,059 行 | 違反 0・embedded lead は 8,059 個すべて相異 |

**非クローン錨の被覆率**: score / f / tree 段は **100%**(653,184 + 108,864 + 全 chord)。
第三実装が届かなかった層 = q_a(Task712 テーブル 4×36,288)と κ(P1 cache 292 MB + Task554 blob からの
96,776 座標の解)と受理 parent 状態。ここは producer×checker の二系統一致のみ。

---

## 5. 空虚性(vacuity)の実測 — 本判読の主要所見

生バイトから測った (tag, character) ごとの**非零係数塊**:

| | char0 | char1 | char2 | char3 |
|---|---|---|---|---|
| tag0 | d0=331 d1=1015 **q=915** | d0=326 d1=1007 q=0 | d0=338 d1=1044 q=0 | d0=329 d1=985 q=0 |
| tag1 | d0=0 d1=0 **q=915** | 0 | 0 | 0 |
| tag2 | d0=0 d1=0 **q=915** | 0 | 0 | 0 |
| tag3 | **全零** | 全零 | 全零 | 全零 |
| tag4 | **全零** | 全零 | 全零 | 全零 |
| tag5 | **全零** | 全零 | 全零 | 全零 |

- **24 個の (tag,character) 塊のうち生きているのは 6 個**。`score` の tag 別非零数 = [40263, 21864, 21864, **0, 0, 0**]。
- **B_1, B_2, B_3 の随伴は恒等的に零**(q の非零は character 0 のみ 915/36,288)。
  v548 §4 が「この run では q1=q2=q3=0 で和が v0 に退化する。これは観測値であって前提ではない」と
  **明示的に警告した空虚性が、rank 1385 でも同じく起きている**。
  ⇒ `sparse_adjoint` vs `pullback` の実質比較は 4 本中 **1 本**。残り 3 本は両者が零を返すだけ。
- **transport の非自明置換は未試験**。tag 1,2 は character 0 のみ寄与し、全 tag が label (0,0) を (0,0) に送るため
  重み ≡ 1。非自明な重み(1/2 の混在)が効くのは **tag 0 の κ character 1–3 だけ**。
  tag 1,2,3,5 の transport 置換内容に誤りがあってもこの run では見えない。
- **8 スロットの shared aux 結合は全て零**: κ_aux[0:8] = 0。
  aux 6,7 は行 0,1 に pin されており χ_0=χ_1=0 ゆえの零(= 有意な試験を通った零)だが、
  **aux 0–5(edge augmentation −κ_aux[tag])はどの式にも pin されない free 座標で、規約により零**。
  ⇒ `raw_edge_cochain` の augmentation 項は恒等的に無効化されており未試験。
  (数学的には無害: κ の自由部分は W1 上で消えるので閉路上の f は不変。しかし**試験としては空虚**。)
- **`COMPLETE_ZERO_CANDIDATE` 分岐は本番で一度も走っていない**(canary のみ)。
- **aux witness 分岐(kind:"auxiliary")も本番未走行**。

補足(結果の頑健性): 残差の値分布は 0/1/2 = **18,090 / 18,083 / 18,260**(非零率 0.66766 ≈ 2/3)。
一様乱数 F3 cochain と統計的に区別できない。したがって
**この違反判定は 36,343 本の独立な証人に支持された過剰決定であり、単一の脆い hit ではない**。
同時に、零が返る事前確率は極めて低く、この oracle の「零側」の識別力はこの λ では実質検証されていない。

---

## 6. v1 → v2 修理の同一性(sentinel)

- 全文 diff は **74 行**のみ: docstring 1 行、新 helper `rooted_indices_u32`(L572)、新 canary
  `serialization_selftest`(L589)、`geometry_payloads` の **2 箇所の呼び出し**、CLI フラグ 1 本、mode 排他 1 行。
- 関数単位類似度: `check_actual` **1.0000**、`typed_array` **1.0000**、`geometry_payloads` 0.9561。
  **A–D の算術・solver・owner/start/result・選択規則は無変更**(当哨が独立に確認)。
- 修理内容: int32 配列 → `astype(np.int64, copy=True)` → 位置 0 に 4294967295 代入 → `<u4`。
  入力配列は非改変、非 root の負値/範囲外/型を拒否。
- v1 の停止は `np.where(int32配列, 4294967295, …)` の型強制で、**stage 比較 loop に入る前**。
  したがって「v1 では一致していた/していなかった」は存在せず、比較は今回が初回。
- **producer 出力は run 1 と完全にバイト同一**(当哨が 44 ファイル全数照合)。
  実際 `parent.u32` / `parent-edge.u32` の先頭 4 バイトは元から `ff ff ff ff` で、
  **producer 側は最初から正しかった**。修理は checker の再直列化のみに影響し、
  比較対象そのものは変わっていない ⇒ v1/v2 の挙動差は「落ちるか落ちないか」だけ。

---

## 7. 格付け案と限定 8 条

**cross-checked(限定つき)。verified=false、cross_checked は工房裁定でのみ true。**

1. 対象は **rank 1385 の現 λ 一点**の snapshot。他の λ・他の rank へ移せない(q_a は次の pivot で陳腐化)。
2. 判定は **VIOLATION_CANDIDATE**(F_λ ≠ 0 on D)。**MEMBER でも NONMEMBER でもない**
   (cert 自身が `grade2_member=NOT_DECIDED`, `grade2_nonmember=NOT_DECIDED`)。
3. 親は 2131 の**七限定つき** rank 1385(親 producer terminal は UNKNOWN_RESOURCE、rank 1385 での
   origin scan は不在)。本 oracle はそれを閉じない。
4. **§5 の空虚性**: B_1..B_3 随伴は恒等零、(tag,character) 24 中 18 が零、tag 3/4/5 の score は恒等零、
   aux 8 スロット結合は全て零、零終端分岐と aux witness 分岐は本番未走行。
5. **F-sc-1(新規)**: `read_task712_envelope`(1.0000)・`_load_words`(1.0000)・`_SeedContext`(0.968)は
   両系統で load-bearing な単一実装。B 復号規約・transport 表・PSL 順序は二系統一致の射程外。
6. **F-fo-1(継承)**: `sparse_adjoint` 1.0000 / `vectorized_projection_chunk` 0.9908 は今周回では片側のみ使用
   だが、旧 scan の独立性欠如は遡及的に閉じていない。v15 seed 核クローンも不変。
7. κ・q・受理 parent 状態は第三実装の射程外(二系統一致のみ)。source/Conn/P1 の completeness、
   λ·ρ₂ の DERIVED、固定 packet 3 段は保持前提。
8. **checker v2 の full selftest は未走行**(completion run は 15 件の serialization canary のみ・
   `old_selftests_executed: 0`)。保存 `checker-selftest.json` は **v1 の受領証**。
   差分の逆適用による v1 全文一致(Task969 F3)と当哨の 74 行 diff で代替しているが、
   「v2 で canary を通した」とは書けない。

**物理 pivot になるまでに要るもの(163 F3 / v548 §5 / v543 §4)**:
witness の 6 閉路を v542/v547 の `R_word` で実際の Ω 語として実体化 → その完全 P1 truncation を
canonical lift で減算して lower-zero の v を得る → G(v) を物理行として追加(rank 1385→1386)。
現状は `MATERIALIZATION_PENDING`・`physical_appends: 0` であり、E consumer は未実装。

---

## 8. 指摘一覧

- **【要修正】F-sc-1(独立性)**: `read_task712_envelope` 1.0000・`_load_words` 1.0000・`_SeedContext` 0.9684 が
  両系統で load-bearing。格付け文面に F-fo-1 と並べて明記すること。
  (根拠: `search/d972_r07_targeted_grade2_owner_generated_join_v15.py` ↔
  `search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py` の token 比較。
  producer 経路 `d972_r07_full_origin_refinement_v1.py:815`、checker 経路
  `check_d972_r07_full_origin_refinement_v1.py:379–382`)
- **【要修正】F-sc-2(空虚性)**: §5 の 6/24 生存・tag 3/4/5 恒等零・aux 8 スロット全零・零分岐未走行を
  格付けと LEDGER に数値で残すこと。特に「4 character 収縮を実測した」という表現は
  **1 character のみ非零**の実態と齟齬する。
- **【要修正】F-sc-3(検査の未走行)**: checker v2 の full selftest 未実行(限定 8 条 8 番)。
  次に v2 を使う run では `--selftest` を 1 回通すべき。
- **【軽微】F-sc-4(空虚な require)**: `check_d972_r07_section_cochain_oracle_v2.py:188`
  `require(not np.any(numerator % 3), "integer_carry_division")` は
  直前で `numerator = integer_sum - integer_sum % 3` としているため**恒真**。
  producer 側にある実質的な検査(`d972_r07_section_cochain_oracle_v1.py:394`
  `require(np.array_equal(reduced, rotation[head]), "carry_actual_successor_rotation")` =
  carry と successor 写像の整合)に対応する checker 側の独立検査は存在しない。
  carry 配列自体はバイト比較されるので穴ではないが、片側にしかない検査である。
- **【軽微】F-sc-5**: witness は 36,343 本の failing chord の**最小 edge ID の 1 本**。
  基底 chord も edge 2,3,4,6,11(単位元近傍)。残差分布は一様(18090/18083/18260)。
  結果は過剰決定で頑健だが、「6 閉路で捕まえた」という表現は「最初の 1 本を選んだ」意味であることを明記。
- **【所見(指摘ではない)】**: 非クローン錨の被覆率が 2131 の 26/838,136(≒0.0031%)から
  score/f/tree の **100%** に改善。これは今周回で最も強い独立性の材料であり、
  格付け文面の positive 側に書いてよい。

## 9. 反証できなかった範囲(正直な申告)

- κ(96,776 座標)と q_a(4×36,288)を当哨が第三実装で再計算することは、
  P1 cache 292 MB と Task554 blob がローカルにないため**行っていない**。二系統一致のみ。
- 紙 v548/v543/v546/v547 の**数学的正しさ**(F_λ = λGR の導出、Conn 前提、Ψ の same-owner 性、
  v546 の 5 legality 行の妥当性)は CV-9 の射程外(2026-08-01 スコープ制限)。当哨は判断していない。
- 受理 parent(rank 1385)の内部は 2131 の裁定を継承しただけで、再監査していない。
- GHA 実行環境の外部証拠(job step の実測秒)は取得していない。本 run は資源停止していないため
  ⑤-9 は非該当。

---

## 付録: 参照ファイル(絶対パス)

- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_section_cochain_oracle_v1.py`(73,290 B・`4e7546eb…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_section_cochain_oracle_v1.py`(80,740 B・`2db16640…`・FAIL 版)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_section_cochain_oracle_v2.py`(84,402 B・`a44ce4ba…`)
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-section-cochain-oracle-v1.yml`(503 行)
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-section-cochain-checker-completion-v1.yml`(704 行・`b439c242…`)
- `C:\Users\81905\Desktop\shadow-atelier\sol\proof_r07_section_corrected_homogeneous_dual_v548.md`(§1–5)
- `C:\Users\81905\Desktop\shadow-atelier\sol\proof_r07_grade2_tree_potential_dual_oracle_v543.md`(§3–4)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_959_r07_section_cochain_oracle.md`(公開 ABI)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_961_r07_section_cochain_oracle_audit.md`(F1–F12)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_968_r07_section_oracle_checker_completion.md`
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_969_r07_section_oracle_completion_audit.md`
- `C:\Users\81905\Desktop\shadow-atelier\ops\express\20260906_astra_fable_section_sentinel_exact_cause.md`
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\full_origin_v1_cv9_reading_v1.md`(裁定 2131・改訂規律)
- 展開済み artifact: `C:\Users\81905\AppData\Local\Temp\shadow-atelier-section-oracle-completion-run33977701313-candidate-a1`
- 展開済み origin: `C:\Users\81905\AppData\Local\Temp\shadow-atelier-section-oracle-run33975617653-diagnostics-a1`
- 当哨の作業物: `C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad\cv9sec\`
  (`sim.py` `sim2.py` = 類似度、`t1`–`t13.py` = 第三実装の再計算・不変照合・空虚性測定)

---

本文(この区切りより上)の sha256 先頭 16 桁: fea1523af518615a
