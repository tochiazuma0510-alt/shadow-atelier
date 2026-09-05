# 増分 CV-9 判読 — R07 selected cycle materializer v1(run 33981657987・PIVOT_CANDIDATE・rank 1385→1386)

判読者: 反証前哨(非当事者・事後)/ 2026-09-06 / 前回 = 裁定 2138(section cochain oracle)・2131(full origin)・2117(seed34 materializer 19 規約表)

---

## 0. 結論(先出し)

- **CV-9 三値裁定: 同一対象(SAME OBJECT)。**
  紙 v542 §2 / v547 §3–5 / v548 §5 の宣言、producer、checker の三者は同一の有限対象
  (受理 witness の 6 基本閉路 → v547 三因子修理で Ω 語 → 六 tag source → 完全 P1 減算 →
  lower-zero → 四 B 前進和 → 現物理状態へ 1 行追加 → 新 target・新 λ)を計算している。
  当哨は **producer/checker いずれのコードも呼ばずに書いた第三実装**で
  Ω 語(3,338 文字の全ストリーム sha256・45 SLP ノード値・Fox chain 108,864 座標)、
  6 基本閉路の合成、τ・境界・witness scalar、lower-zero(96,776 座標)、四 B 和、
  正規化行、**新 target から親 target を逆算した sha256 の一致**、λ の三本の内積、
  5,335 P1 事象の全規約を**生バイトから再現**した。「同一対象」は宣言の突合だけでなく実測で裏づく。

- **工房格付け案: cross-checked(限定 7 条・§7)。**
  「rank 1385 の受理状態に、chord 12 の witness 由来の合法物理行を 1 本追加して rank 1386 とし、
  target 剰余が scalar 1 で動き、なお Separator である」という**有限事実**は照合済みと呼べる。
  **MEMBER でも NONMEMBER でもない**(cert 自身が `grade2_member = grade2_nonmember = NOT_DECIDED`,
  `positive_readout = NOT_APPLICABLE`, `full_A0 = false`)。Lean verified ではない。

- **今周回の目玉**
  ① **前回(2138)の主要な穴が 2 つ閉じた**: (a) checker の full selftest 未走行(F-sc-3)→ 両系 3 群/3 件が本走で実行、
     workflow は producer `.groups` / checker `.tests` の**別 gate** で判定(`:530-533`)。
     (b) 空虚性 — raw source の **(character,tag) 24 塊すべてが非零**、四 B すべてが非自明(support 8130/16305/16024/23784)、
     α に 1 と 2 の両方(2679/2656)、old/new とも 4 owner 全部、d0 枝と shared-aux 枝の両方が発火。
  ② **`_seed_*` 系クローンが checker 本番から消えた**: checker は psl 積・affine 積・逆・冪・Fox を**自前実装**し、
     `_seed_perm_mul` / `_seed_affine_mul` / `_seed_affine_fox` / `_seed_e_poly` / `_seed_cv` を**一度も呼ばない**(grep 0 件)。
  ③ 一方 **新しい空虚性が出た**: v547 三因子修理のうち**実際に効いたのは 1 因子だけ**。
     `repair-y` と `repair-central`(中心項 = [r_x,r_y]^g)は**指数 0 = 空語**。中心項は本番で一度も試されていない(F-cy-1)。
  ④ **継承クローン `read_task712_envelope`(1.0000・1,512 token)が両系 load-bearing のまま**で、
     今周回はそれが**物理行そのものを作る B 表の復号**に効く。前周回より射程が重い(F-cy-4a)。

---

## 1. 当哨が生バイトから再計算した受領証

| 項目 | 結果 | 出所 |
|---|---|---|
| 封 19 件の再計算 | **19/19 成功・全件 canonical bytes と一致・失敗 0** | 当哨 `t1.py` |
| manifest roster | 27 ファイル + `manifest.json` + `HEAD`・**exact roster**・bytes/sha 全一致 | 当哨 |
| 受理 oracle entry 10 件 | 実 completion artifact(`…section-oracle-completion-run33977701313-candidate-a1`)と **0 mismatch** | 当哨 |
| TCB 16 ファイル + データ pin 3 件 | live repo と **0 mismatch**(source-receipt.json) | 当哨 |
| normalizer 語 r_x/r_y/c_x/c_y | 固定辞書 `a0_v2_words.json`(106,133 B `fb191e30…`)から再構成 → **4/4 sha 一致**(1058/466/9522/4194) | 当哨 `t3.py` |
| 6 基本閉路の合成 | tree word + Fox → **`raw-chain.bin` とバイト一致**(support 138) | 当哨 `t2.py` |
| τ / 境界 / witness scalar | τ = [0,0,0,0,0]・∂ ≡ 0 mod 3・scalar = **1**(= dot(chain,f) + dot(η,b_aux)) | 当哨 |
| **Ω 語 raw-root 全ストリーム** | 3,338 文字・sha256 `d7a124e2a145ecaa…` **cert 一致**・Fox chain = raw-chain.bin・endpoint 0・q0 = 恒等・(ε_x,ε_y,ω) = (0,0,0) | 当哨 |
| SLP 45 ノード値 | exponent / ω / length / **36 点 Q0 置換** / Q2 endpoint を全ノードで再現・**不一致 0** | 当哨 |
| 修理因子の Fox 零 | fox(r_x^3)=0, fox(r_y^3)=0, fox([r_x,r_y])=0、fox(r_x)≠0(support 301・augmentation 2), fox(r_y)≠0(224) | 当哨 `t12.py` |
| 語長 | tree height 20・`l0` = 164 ≤ 6(2·20+1) = 246・root 長 3,338 | 当哨 |
| source アンカー | homogeneous **1** / section **0** / (1−0)%3 = **1** = witness scalar・lower sha・top sha とも cert 一致 | 当哨 `t4.py` |
| **lower-zero** | `source-lower-remainder.bin` = **96,776 trit すべて 0** | 当哨 |
| corrected_scalar | Σ_a dot(q[a], corrected_top[a]) = **1** | 当哨 |
| 四 B 和 | Σ_a by_character[a] ≡ physical_raw(全 48,384 座標) | 当哨 |
| 正規化 | lead **1457**・σ = 1・normalized = σ·remainder・prefix 零・sha 一致・support 30,725 | 当哨 |
| **target 差分恒等式** | `new_target + 1·normalized` の sha256 = **`111d12e064b96a6b…`** = **親(rank 1385)の pinned target 剰余** | 当哨 |
| λ | free 座標 **1458** 値 1・λ·新行 = **0**・λ·新 target = **1**・λ·親 target = **1**・sha `a16f4c82…` 一致 | 当哨 |
| F1 受領証 | `row_pairings_sha256` = **sha256(0x00 × 1386)** を外部再計算で確認 | 当哨 |
| P1 5,335 事象 | node id = OLD/NEW_OFFSETS[owner]+local・local 範囲・embedded lead 式・符号付指数・**順序規約**すべて **違反 0** | 当哨 `t13.py` |

**入力 pin の一致**: 受理 oracle は artifact `9972829869`(run 33977701313・2,299,772 B・`1a5c8800…`)。
producer/checker 双方が同じ 10 entry を literal 定数で持ち、配列 44 本は
`result.json → stage_manifests → stage manifest → 各ファイル bytes/sha` で**推移的に pin 済み**(未 pin 入力なし)。
親 9 run を計算前に `gh api` で live 照合(2117 規約 1 の 6 本 → 9 本へ拡大)。
`producer-parent-layout.json` と `checker-parent-layout.json` は **35,866 B バイト同一**。

---

## 2. 主検問相当 — 紙 ↔ producer ↔ checker の規約対応(今周回の新規段)

| 紙の宣言 | producer | checker | 判定 |
|---|---|---|---|
| v542 (2.1) `w(z)=∏_e s_e^{z_e}`、s_e = tree(tail)·letter·tree(head)⁻¹、係数 2 は −1、**edge 順固定** | `selected_raw_word:400-410`(`cycle-i` = OrderedProduct(tail, x/y, head⁻¹)、`cycle-power-i` = ^signrep(c)、`w` = 6 因子の順序積) | `selected_raw_slp:415-425` 同一ノード構成 | **同一**(ノード ID・演算・因子順が一致。当哨が 45 ノード全値を再現) |
| v547 (4.2) `R(w)=w (r_x^3)^{−ε_x/6} (r_y^3)^{−ε_y/6} [r_x,r_y]^g`、g ∈ {0,1,−1} は ω(w) の符号付代表、**因子順は書かれた通り固定** | `:424-427` `repair-x/-y/-central` → `raw-root` = OrderedProduct(w, repair-x, repair-y, repair-central) | `:426-430` 同一 | **同一** |
| v547 (3.1) ω(w) = Σ_{x^σ} σ·B(前置) | `exponent_omega:164`(`omega=(omega+value*b)%3` の後に `a+=value` = **前置** ε_y) | `letter_statistics:262`(同順) | **同一**(当哨が全ノードで実測一致) |
| v547 (3.2) ω(uv)=ω(u)+ω(v)+B(u)A(v) | `scalar_product:177`(`(omega+psi+b*c)%3`) | `combine_statistics:275` | **同一** |
| v547 (3.3) ω(u^m)=mω(u)+C(m,2)B(u)A(u)、負 m も整数多項式 | `scalar_power:183`(`exponent*(exponent-1)//2*b*a`) | `power_statistics:284` | **同一**(m<0 でも積が偶数なので `//` の床処理差は生じない) |
| v547 (3.7) ω([r_x,r_y]) = 0·0−2·2 = 2 | `commutator` = OrderedProduct(r-x⁻¹, r-y⁻¹, r-x, r-y) | 同 + **`require(commutator ω == 2)`**(checker 側のみ) | **同一**。括弧の向き([u,v]=u⁻¹v⁻¹uv)は値 2 で**一意に pin される**(逆向きなら 1)。cert も ω=2 |
| v547 (4.3)/(5.1) `J_Q2(R(w)) = z`、追加因子は Φ(N0) ゆえ Fox 行零 | `require(np.array_equal(chain, witness_chain(...)))` + `r-x-cube/r-y-cube/commutator` の Fox 零検査 | `require(np.array_equal(chain,(wanted_chain%3)))` + 同 3 因子の Fox 零 + **原子 r_x の augmentation 非零 canary** | **同一**(当哨が 6 因子すべての Fox chain を独立に再計算) |
| v547 (4.4) ε(R(w)) = (0,0) | `require(a0%18==b0%18==0 and (a0,b0)==(0,0))`(chord 枝) | `require(root["exponent"] == [18η_0,18η_1])`(η=[0,0]) | **同一** |
| v548 §5「Section 3 のように選択 P1 lift を減算 → lower-zero」 | `primal_section:646`(old = embedded lead 昇順 / new = owner major・元 lead 昇順)+ `corrected_source:733` | `primal_rows:642`(同順)+ `p1_corrected_source:727`(P1 cache 292 MB から**独立に再構成**) | **同一**(当哨が 5,335 事象の順序・node 式・embedded lead 式を全数照合) |
| v548 §5「実 materializer は完全 lower-zero 行と物理値を確認する」 | `require(lower.size==LOWER and not np.any(lower))` | `require(...not np.any(lower))` + `require(np.array_equal(full_lower(corrected), primal["lower"]) and not np.any(...))` = **二経路** | **同一・checker 側が強い** |
| 四 B 前進和 → 物理行 | `four_B:784`(`m.apply_sparse` の entry ごと mod3 加算) | `grouped_forward:1111`(出力座標で argsort → int64 group sum → mod3) | **同一**(別算術。当哨が Σ_a を生バイトで確認) |
| 1 行追加・新 target・新 λ | `one_physical_row:821` / `fresh_separator:799`(逆代入 + `m.check_final_separator`) | `one_physical_row:1020`(`LEGACY` 原始 + **1386 行 + 両 target の内積を自前で測る**) | **同一** |
| 終端命名 | `PIVOT_CANDIDATE` / `LINEAR_MEMBERSHIP_CANDIDATE` | 同(checker は自分の計算から導出し、producer の `result.json` をバイト比較) | **同一** |

**分離条件・ダミー検査**: 両側に実在し、今周回は前回の空虚性を**名指しで塞いでいる**。
- producer canary 3 群: ω の積/整数冪(負・零を含む)を直接評価と突合、`ω([x,y])=2`、
  **逆順挿入は非零を残す**(`canary_reverse_insertion_wrong_source_order`)、負係数 chord は chain の符号反転、
  `LINEAR_MEMBERSHIP_CANDIDATE` は λ = None で **MEMBER ではない**(`canary_linear_zero_is_not_MEMBER`)、mod54 の符号付積。
- checker canary 3 件: 非可換 endpoint、負冪 SLP の合成 chain = 平坦 chain、
  **原子 r_x の Fox augmentation = 2 が非零**(root が発見した誤 gate の逆検査・967 F10)、
  三修復因子の Fox 零、**6 tag × 4 character × 混合次数 × η を全部非零で走らせる**
  (`canary_all_six_tags_four_characters_mixed_degrees_eta` = 2138 F-sc-2 への直接の手当)、
  8 aux スロット全走、元 lead ≠ 挿入 ID の分離、residue54 の型拒否 4 種(bool/54/−1/float)、
  target scalar 0 と linear 候補の両枝、封の改竄と**末尾 1 バイト追加**の拒否。
「何にでも当たる試験」ではない。

---

## 3. 独立性

### 3.1 交差辺 — なし
- producer は producer 系統のみ(`d972_r07_section_cochain_oracle_v1.py` `4e7546eb…` を pin → full_origin_refinement → packet_loop_v2 → materializer_v3 → batch_v2 → v15)。
- checker は checker 系統のみ(`check_d972_r07_section_cochain_oracle_v1.py` `2db16640…` を pin)。
- checker は producer source を **hash するだけ**(`producer_source:1008` が `PRODUCER_SHA` を照合)。import しない。
- **checker が producer 出力ディレクトリ(`candidate_root`)に触れるのは
  `check_telemetry:1245` と `finalize_candidate:1247` の 2 箇所だけ**(grep 全 4 件・残り 2 件は COMPLETE_ZERO 分岐と CLI)。
  算術 6 段(raw/source/primal/p1/B/physical)には producer 出力が一切入らない。
- 比較 gate は **exact roster**(`{p.name for p in root.iterdir()} == set(expected)`)+
  **全ペイロードの完全バイト + 1 バイト超読**(`stream.read(len(raw)+1) != raw`)。
  checker 自作の `manifest.json` と `HEAD` も比較対象に入る。

### 3.2 新 pair の類似度(token 化 SequenceMatcher・autojunk 両方)— **クローンなし**

| producer | checker | AJ=T | AJ=F |
|---|---|---:|---:|
| `RawSLP.letters` | `RawSLP.letters` | **0.8424** | 0.8424 |
| `lower_row` | `full_lower` | 0.8081 | 0.8081 |
| `signrep` | `signed` | 0.7952 | 0.7952 |
| `require` | `require` | 0.7917 | 0.7917 |
| `seal` | `document` | 0.6789 | 0.6789 |
| `group_power` | `SelectedGeometry.power` | 0.6533 | 0.6533 |
| `inverse_word` | `inverse_word` | 0.6129 | 0.6129 |
| `free_reduce` | `reduced_word` | 0.5677 | 0.5677 |
| `scalar_power` | `power_statistics` | 0.5385 | 0.5385 |
| `scalar_product` | `combine_statistics` | 0.4585 | 0.4585 |
| `selected_raw_word` | `selected_raw_slp` | 0.2543 | 0.4807 |
| `word_fox` | `flat_fox_chain` | 0.2180 | 0.2180 |
| `source_from_chain` | `ordinary_source` | 0.0275 | 0.2693 |
| `primal_section` | `primal_rows` | 0.1483 | 0.2563 |
| `corrected_source` | `p1_corrected_source` | 0.1421 | 0.2030 |
| `four_B` | `grouped_forward` | 0.0905 | 0.2346 |
| `one_physical_row` | `one_physical_row` | 0.0351 | 0.1496 |
| `fresh_separator` | `one_physical_row` | 0.0278 | 0.1667 |
| `run_actual` | `check_actual` | 0.0410 | 0.2004 |
| `selftest` | `selftest` | 0.0874 | 0.2123 |

最大 0.8424 は 12 行の生成器で、しかも冪の反転処理が別式
(producer `exponent = -e if inverse` → `letters(child, exponent<0)` / checker `letters(child, inverse != (e<0))`)。
0.8081 の `lower_row`/`full_lower` は 1 行の連結(d0,d1,aux — **d2 を含めない**という規約の一致)。
**新 pair に 1.0 クローンはない。**

### 3.3 継承 primitive のうち「今周回に load-bearing になったもの」

| 継承関数対 | AJ=T | 今周回どちらが使うか | 評価 |
|---|---:|---|---|
| **`read_task712_envelope`** | **1.0000**(1,512 token・本文バイト同一) | **両側**(producer: `fixed_root_packet_loop_v2.py:545` 経由 / checker: `check_…full_origin_refinement_v1.py:379`) | **F-cy-4a・今周回で最重要**。B 表の復号規約は二系統一致で検出されない |
| **`_load_words`** | **1.0000**(159 token) | **両側**(生 word JSON 読取) | F-sc-1 継承・不変 |
| **`_SeedContext` / `_CheckerSeedContext`** | **0.9684** | **両側**(psels/psidx/images/**transport**) | F-sc-1 継承。今周回は transport が両側の `ordinary_source`/`source_from_chain` で本番使用 |
| `source_context` / `checker_source_context` | 0.9254 | 両側(上記の薄い包み) | 同上 |
| `empty_lift` / `zero_source` | **0.8500** | 両側(4 部構成の零 source を確保) | **新規・軽微**: source の形状規約(24192/72576/145152/8)が単一実装の写し |
| `component_receipts` / `source_components` | 0.7273 | 両側 | 受領証の書式のみ |
| `physical_reduce` / `reduce_dense` | 0.3947(F 0.6501) | 両側 | 2117 規約 12 と同じ・クローンではない |
| `normalize_pivot` / `normalize` | 0.5645 | 両側 | 2117 規約 13 |
| `update_target` / `next_target` | 0.4946 | 両側 | 2117 規約 14 |
| `check_final_separator` / `next_separator` | 0.2124 | 両側 | 2117 規約 15/15′ |
| `_seed_perm_mul` / `_seed_affine_mul` / `_seed_affine_fox` / `_seed_e_poly` / `_seed_cv` | (前回 0.92–0.99) | **producer のみ**(checker 側に定義すら存在せず・grep 0 件) | **今周回の改善**。checker は psl 積表・affine 積/逆/冪・Fox を自前実装 |

**F-cy-4a**: `read_task712_envelope` はバイト同一の単一実装で、今周回は**追加された物理行そのもの**
(G(v) = Σ_a B_a·v_a)を作る B 表を復号する。当哨の第三実装は Σ_a by_character = physical_raw までしか届かず
(Task712 blob がローカルにない)、`by_character[a] = B_a·v_a` は**二系統一致のみ**。
task712 artifact 自体は `owner.json` の `task712_manifest_sha256` で hash pin されているので、
穴は「生バイトの真正性」ではなく「**復号規約の単一実装性**」である。

---

## 4. 空虚性(vacuity)の実測

### 4.1 改善した点(前回 2138 との差)

| | 2138(section oracle) | 今回 |
|---|---|---|
| (character,tag) 非零塊 | 24 中 **6** | 24 中 **24**(character 0–3 × tag 0–5 すべて 623–737 個) |
| 四 B の随伴/前進 | q_1=q_2=q_3 = **恒等零** | 前進 by_character の support = **8130 / 16305 / 16024 / 23784**(四本とも非自明) |
| α 係数 | — | 1 が 2,679・2 が 2,656(両符号が発火) |
| owner 被覆 | — | old 329/330/327/347、new 1020/989/1015/978(**8 枝すべて**) |
| shared-aux 枝 | 未走行 | **発火**(owner 0・元 lead 6054・embedded 96774・係数 1) |
| checker full selftest | **未走行**(F-sc-3) | **走行**(3 件 PASS・workflow が `.tests` で別 gate) |
| mod54 指数 | — | 9 種の pair((0,0)5040 / 他 8 種 34–39 件)。18 整除 gate が非自明に発火 |

### 4.2 新規に見つかった空虚性

- **F-cy-1(要修正・本判読の主要所見)**: **v547 三因子修理のうち 2 因子が空語**。
  cert `raw-word.json` の `node_values`: `w` = (ε_x,ε_y,ω) = **(6, 0, 0)**、
  したがって `repair-x` 指数 = −1(長さ 3,174)、**`repair-y` 指数 = 0(長さ 0)**、
  **`repair-central` 指数 = 0(長さ 0)**。
  すなわち **[r_x,r_y]^g の中心項は本番で一度も適用されていない**。
  加えて `scalar_power`/`power_statistics` の二次項 `C(m,2)·B(u)A(u)` は
  **45 ノードすべてで 0**(r_x は (2,0)、r_y は (0,2) ゆえ B·A = 0、cycle 冪は m=1)。
  → 「v547 の三因子修理を実行した」は、データ上は「**1 因子 r_x^{−3} を適用した**」である。
  緩和: 両 canary は ω 機構と三因子すべてを走らせており、`commutator ω == 2` も checker canary が pin している。
  **本番未試験であることを格付け文面に数値で残すこと。**

- **F-cy-2(軽微・空虚な require)**: 語長上界の検査は chord 枝で**恒真**。
  producer `:787-790` / checker `:794-797` の `bound` は
  `l0 + 3|a/6|·|r_x| + 3|b/6|·|r_y| + 2|g|·(|r_x|+|r_y|)` だが、
  構成語の実長は `l0 + |a/6|·len(r_x^3) + |b/6|·len(r_y^3) + |g|·len([r_x,r_y])`
  = 同じ式(len([r_x,r_y]) = 2(|r_x|+|r_y|) = 3,048)。
  実測: `normalized = 3338 = actual_slp_length`(**等号**)。
  → `require(root_length <= bound)` は恒等式であり試験ではない。
  同じ require の前半 `l0 <= 6(2h+1)`(164 ≤ 246)は実質的。

- **F-cy-3(要修正・紙の齟齬)**: **v548 §5 と v547 (4.2) の中心指数の記載が literal に食い違う**。
  v548 §5: `R_word(w)=w (r_x^3)^(-eps_x/6) (r_y^3)^(-eps_y/6) [r_x,r_y]^omega(w)`
  v547 (4.2): `[r_x,r_y]^g`、g = ω(w) の **{0,1,−1} 符号付代表**。
  実装は両側とも v547(`signrep(ω)` / `signed(ω)`)。
  **本 run は ω(w) = 0 なので両読みが区別できない**。ω ≠ 0 の run に進む前に v548 の引用を直すか、
  「v548 は v547 (4.2) を指す略記」と明記すること。

- **F-cy-4b(所見・継承)**: 親から継いだ空虚性は**そのまま**。
  `q_a = B_a^*λ` の support = **[2745, 0, 0, 0]** — **character 0 のみ非零**。
  → 追加された行は四 character すべてを使うが、「この行が λ を動かす」と証す**スカラー 1 は character 0 だけで決まる**。
  `κ` は **tag 0 にしか台を持たない**(d0 = 331/326/338/329、d1 = 1015/1007/1044/985、**tag 1–5 は恒等零**、aux 8 スロット全零)。
  section scalar 0 は character 1,2,3 の tag 0 が各 2 を出して 2+2+2 ≡ 0 という相殺。
  → **section 補正の tag 1–5 は今回も未試験**。

---

## 5. 射程の読み(生バイトからの再導出)

| 主張 | cert | 当哨の再導出 |
|---|---|---|
| rank 1385 → **1386** | `rank_before 1385 / rank_after 1386 / physical_appends 1` | 親 target = 新 target + 1·normalized の sha が **親の pinned target `111d12e0…` と一致** ⇒ 行は実在し、親状態に本当に足された |
| generation 8090 → 8091 | `generation_after 8091` | instruction `rolling_sha256 = sha(親head ‖ canonical(instruction))` = `5e760f6a…` = 新 state_head(cert 一致) |
| 追加行の由来 | `origin.kind = "v548-cycle"` / `witness_sha256 1c282b82…` | witness: kind chord・**failed_chord 12**・basis_chords [2,3,4,6,11]・basis_coefficients (2,0,2,2,2) → cycles (12:1)(2:1)(3:0)(4:1)(6:1)(11:1)。当哨が `(-b)%3` 規約と 6 閉路合成を全数確認 |
| Ω 語 | `word_stream.letters 3338 / sha d7a124e2…` | 全ストリーム再生成・sha 一致・Fox chain 一致・endpoint 0・q0 恒等・ε=(0,0)・ω=0 |
| **target 剰余が動いた** | `target.scalar = 1`・`111d12e0…` → `e902cf3b…` | 差分恒等式で確認。新 target は lead 1457 で 0、非零 **31,081** 座標が残る ⇒ **まだ 0 ではない** |
| **依然 Separator** | `terminal PIVOT_CANDIDATE` / `kind Separator` / `lambda_pivots 0` / `rows 1386` | 新 λ `a16f4c82…`(親 `1e720af4…` と別物)。λ·新行 = 0、λ·新 target = 1、λ·親 target = 1、free 座標 1458 値 1、`row_pairings_sha256` = sha256(0x00×1386) |
| **MEMBER でも NONMEMBER でもない** | `grade2_member = grade2_nonmember = NOT_DECIDED`・`positive_readout = NOT_APPLICABLE`・`full_A0 false`・`cross_checked false`・`verified false` | 同意。PIVOT_CANDIDATE は「合法な行が 1 本増え、なお分離されている」以上を言わない |

**λ ⊥ 1385 本の旧物理行**は当哨の射程外(`state/physical.bin` がローカルにない)。
確認できたのは受領証の形(sha256(0x00×1386))と、λ ⊥ 新行・λ·両 target = 1 のみ。旧 1385 本は**二系統一致**。

---

## 6. 2117(19 規約表)との機械 diff

| # | 規約 | 今回 | 判定 |
|---|---|---|---|
| 1 | 親を計算前に live 照合 | 6 本 → **9 本**(p1/task554/task712/separator/delta/seed34/packet/refinement/oracle)+ artifact 13 件 | **強化** |
| 2 | 違反の同一性 | 受理 oracle artifact `9972829869` + `witness_sha256 1c282b82…` から導出(literal witness は持たない) | 一致(継承) |
| 3 | 「最初の違反」の継承 | 親 oracle の 54,433 chord 全走査結果を継承。今回は選択済み witness の実体化のみ | 継承 |
| 4–7 | 事象列・rolling 封・畳込み・owner/kind | `OLD_OFFSETS (0,505,1008,1511)` / `NEW_OFFSETS (2014,3523,5035,6547)` 不変。**当哨が 5,335 事象全部で node 式を再照合・違反 0** | 一致 |
| 8 | `+(3−c)·row ≡ −c·row` | P `m.add_scaled(...,3-c)` / C `LEGACY.subtract(...,c)` | 一致(式同値・別の書き方) |
| 9 | 下位 96,776 の完全消滅 | P 1 経路 / **C 2 経路**(primal と P1 cache 再構成の一致 + 零) | **強化** |
| 10 | v541 filtered projector | 本周回は**不使用**(源は六 tag Fox source) | **移行** |
| 11 | `q·d = 1` / `λ_old·G = 1` | `corrected_scalar == dot(λ, physical_raw) == witness.scalar == 1`。加えて新規に `(homogeneous − section)%3 == scalar` | 一致+**追加アンカー** |
| 12–14 | 挿入 1 掃引 / 正規化 / 新 target 1 段 | 継承 primitive・`new_target_steps_executed = 1` | 一致 |
| 15/15′ | λ の逆代入 + **全行スイープ** | **1386 行**(旧 1385 + 新 1 本)+ 親/新 両 target | 一致・行数が 1 増 |
| 16 | 「依然 Separator」判定 | P `m.first_nonzero(target)` / C `np.any(target)` | 一致 |
| 17 | λ の受理条件 | `λ·normalized = 0`・`λ·new_target = 1` は実測。**`λ·ρ₂ = 1` は依然 `mode: "derived"`・`original_rho2_directly_read: false`** | **弱化のまま(2117 F-v3-2 未閉鎖)** |
| 18 | 封の正規形 | 19 件すべて再封成功・ファイル = canonical bytes | 一致 |
| 19 | 格の自己抑制 | 全 cert が `cross_checked=false`/`verified=false`、workflow `:496,530-533,549,568` が要求 | 一致 |

---

## 7. 格付け案と限定 7 条

**cross-checked(限定つき)。`verified=false`。`cross_checked` は工房裁定でのみ true。**

1. 射程 = 「rank 1385 の受理状態に chord 12 witness 由来の合法物理行を 1 本追加し、
   rank 1386・generation 8091・target scalar 1・**依然 Separator**」という**有限事実**一点。
   **MEMBER でも NONMEMBER でもない**。他の λ・他の rank へ移せない。
2. **F-cy-1(空虚性)**: v547 三因子のうち**実際に効いたのは 1 因子**。
   `w` = (6,0,0) ゆえ `repair-y` と **中心項 `repair-central` は空語**。
   ω の二次項は 45 ノード全部で 0。中心項は canary でのみ試験されている。
3. **F-cy-2(恒真 require)**: 語長上界 `root_length <= bound` は chord 枝で恒等式(実測 3338 = 3338)。
4. **F-cy-3(紙の齟齬)**: v548 §5 の `[r_x,r_y]^omega(w)` と v547 (4.2) の `[r_x,r_y]^g` は literal に別物。
   実装は v547。本 run は ω=0 で区別不能。
5. **F-cy-4(独立性)**: `read_task712_envelope`(**1.0000**・両側 load-bearing)が
   **今回追加された物理行を作る B 表の復号**に効く。`_load_words`(1.0000)・`_SeedContext`(0.9684・transport)も両側。
   `empty_lift`/`zero_source`(0.8500)は source 形状規約の単一実装。
   これらの規約誤りは二系統一致では検出されない。(改善: `_seed_*` 群は checker 本番から消えた。)
6. **F-cy-4b(継承空虚性)**: `q_a` は **character 0 のみ非零**(support 2745,0,0,0)、
   `κ` は **tag 0 のみに台**(tag 1–5 恒等零・aux 8 スロット全零)。
   スカラーの検定力は character 0 × tag 0 に集中している。
7. 当哨の第三実装が届かなかった層 = **B_a 行列そのもの**(Task712 blob)、
   **旧 1385 本の物理行**(state/physical.bin)、**P1 cache 292 MB / Task554 blob 由来の 5,335 lift**、
   κ と q(親 2138 の限定 vii を継承)。これらは二系統一致のみ。
   2117 規約 17 の弱化(λ·ρ₂ = 1 は 32 件の `accepted_target_derivation_parents` を経た前提)は不変。
   親 rank 1385 の内部は 2131 の七限定 + 2138 の八限定を継承。

---

## 8. 指摘一覧

- **【要修正】F-cy-1**: 「v547 三因子修理で Ω 語を実体化した」を格付け文面に書くなら、
  **実際に非自明だったのは `(r_x^3)^{-1}` の 1 因子で、`(r_y^3)^0` と `[r_x,r_y]^0` は空語**であることを数値で併記する。
  中心項は本 run では一度も試されていない(canary のみ)。
  根拠: `cand/output/raw-word.json` の `node_values` — `w`: exponent [6,0] omega 0 / `repair-y`: exponent 0 length 0 /
  `repair-central`: exponent 0 length 0 / `commutator`: omega 2 length 3048。当哨が 45 ノード全値を独立再現。
- **【要修正】F-cy-3**: `sol/proof_r07_section_corrected_homogeneous_dual_v548.md` §5 の
  `[r_x,r_y]^omega(w)` を v547 (4.2) の `[r_x,r_y]^g`(g = 符号付代表)に合わせるか、略記である旨を明記。
  ω ≠ 0 の witness に進む前に決着させること(今 run では区別不能)。
- **【要修正】F-cy-4a**: `read_task712_envelope` は本文バイト同一(1,512 token)で**両系 load-bearing**、
  かつ今周回は物理行を作る B 表の復号に効く。F-sc-1 / F-fo-1 と並べて格付けに明記。
  根拠: producer 経路 `search/d972_r07_fixed_root_packet_loop_v2.py:545`、
  checker 経路 `search/check_d972_r07_full_origin_refinement_v1.py:379`、
  定義 `search/d972_r07_targeted_grade2_owner_generated_join_v15.py:271` ↔ `search/check_…_v15.py:271`。
- **【軽微】F-cy-2**: 語長上界の require は恒真。実質的な検査は `l0 <= 6(2h+1)`(164 ≤ 246)のみ。
- **【軽微】F-cy-5(非対称な被覆)**: primal 段で **producer は 8,059 行すべて**の
  `row[lead]==1 かつ prefix 零` を検査するが、**checker は係数 0 の 2,724 行を `continue` で飛ばす**
  (`check_…_selected_cycle_materializer_v1.py:654-655`)ので、正規化検査は選択された 5,335 行のみ。
  逆に checker だけが持つ検査が 2 本ある(old 行の `owner==0 or not np.any(row[6048:])`、`commutator ω == 2`)。
  最終 gate は両側とも 96,776 零(checker は二経路)なので健全性の穴ではないが、被覆は片側ずつ違うと書くこと。
- **【軽微】F-cy-6**: producer `:768` の `require(normalized_pair == [0,0] and ...)` の第 1 連言は
  直前の `primal_full_96776_zero`(aux 6,7 を含む)から導かれるため冗長。checker は η を制約しない。
  健全性の問題ではないが、「η = [0,0] を実測した」ではなく「lower-zero から従う」と読むべき。
- **【所見(指摘ではない)】**: 前回 2138 の F-sc-2(24 中 6 塊生存)と F-sc-3(checker selftest 未走行)は
  **今周回で実質的に閉じた**。checker canary `canary_all_six_tags_four_characters_mixed_degrees_eta` は
  F-sc-2 への直接の手当であり、本番でも 24/24 塊が生きた。格付けの positive 側に書いてよい。
- **【所見】**: root(司令塔)が checker の `raw_materialization` で発見した誤 gate
  (原子 r_x/r_y の Fox chain に零を要求 = augmentation を無視した誤り・967 F10)は修正済みで、
  逆向きの canary(`canary_atom_Fox_augmentation_is_nonzero`)が入っている。
  当哨も独立に fox(r_x) support 301 / augmentation 2、fox(r_x^3) = 0 を確認した。

---

## 9. 反証できなかった範囲(正直な申告)

- B_a 行列そのもの(Task712 blob がローカルにない)。Σ_a by_character = physical_raw までは生バイトで確認したが、
  `by_character[a] = B_a·corrected_top[a]` は**二系統一致のみ**で、しかもその復号は 1.0000 クローン(F-cy-4a)。
- 旧 1385 本の物理行との直交(`state/physical.bin` 非所持)。受領証の形と新行・両 target のみ確認。
- P1 cache(292 MB)・Task554 blob 由来の 5,335 lift の中身。順序・node 式・embedded lead 式・
  符号付指数・最終 lower-zero は全数照合したが、lift の数値そのものは二系統一致のみ。
- 紙 v542/v547/v548/v543 の**数学的正しさ**(Φ(N0) の性質、Θ の忠実性、Ψ の same-owner 性、
  F_λΨ = Σ q_a Ψ2 − κΨ1 の導出)は CV-9 の射程外(2026-08-01 スコープ制限)。当哨は判断していない。
- 親 rank 1385 の内部は 2131/2138 の裁定を継承しただけで再監査していない。
- GHA 実行環境の外部証拠は run-receipt(job 100 分・producer/checker とも cap 40 分・内部 1800 秒)と
  telemetry(6 段合計 ≈ 46.2 秒・checker `elapsed_seconds` 82.4)を読んだのみ。資源停止は発生していない。

---

## 付録: 参照ファイル(絶対パス)

- `C:\Users\81905\Desktop\shadow-atelier\search\d972_r07_selected_cycle_materializer_v1.py`(88,929 B・`4f600aae…`)
- `C:\Users\81905\Desktop\shadow-atelier\search\check_d972_r07_selected_cycle_materializer_v1.py`(103,757 B・`a6d52e0d…`)
- `C:\Users\81905\Desktop\shadow-atelier\.github\workflows\d972-r07-selected-cycle-materializer-v1.yml`(44,334 B・`def1e181…`・689 行)
- `C:\Users\81905\Desktop\shadow-atelier\sol\proof_r07_table_free_endpoint_selector_v547.md`(§3–5)
- `C:\Users\81905\Desktop\shadow-atelier\sol\proof_r07_chord_cycle_holonomy_repair_v542.md`(§2・§5)
- `C:\Users\81905\Desktop\shadow-atelier\sol\proof_r07_section_corrected_homogeneous_dual_v548.md`(§5)
- `C:\Users\81905\Desktop\shadow-atelier\sol\luna_reply_965_r07_selected_cycle_materializer.md` / `…966…` / `…967…`
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\section_cochain_v1_cv9_reading_v1.md`(裁定 2138)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\full_origin_v1_cv9_reading_v1.md`(2131)
- `C:\Users\81905\Desktop\shadow-atelier\docs\notes\seed34_mat_v3_cv9_reading_v1.md`(2117・19 規約表)
- 展開済み artifact(candidate 9973974150 / diagnostics 9973974466):
  `C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad\cv9cyc\cand` / `…\diag`
- 受理 oracle: `C:\Users\81905\AppData\Local\Temp\shadow-atelier-section-oracle-completion-run33977701313-candidate-a1`
  / 配列: `C:\Users\81905\AppData\Local\Temp\shadow-atelier-section-oracle-run33975617653-diagnostics-a1\output`
- 当哨の作業物(第三実装):
  `C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad\cv9cyc\`
  (`sim.py` `sim2.py` = 類似度、`t1.py`–`t13.py` = 封/pin/Ω 語/lower-zero/物理行/λ/空虚性の再計算)

本文の sha256 先頭 16 桁: cb6517cfe6b00322
