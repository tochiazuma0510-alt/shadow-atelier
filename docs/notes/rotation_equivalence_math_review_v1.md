# 工房数学者による独立審査 — Astra 原案「親層の回転(統合親)による認証対象の同値性」(task 1111)

審査対象: `sol/luna_task_1111_r07_parent_rotation_equivalence_independent_review.md`(12,428 B)の原案 R1–R4
発注: 裁定 2226(工房数学者への独立審査発注)。裁定 2225 の納品条件 (i)(ii)(iii) に対応。
審査者: 工房数学者(Opus・非当事者)。**実装 0・GHA 0・新数学実行 0**。数値は正典(v3/v4/v5 CV-9 判読・裁定 snapshot)と repo 作業ツリーの P5 source から取得。
審査日: 2026-09-08。

---

## 0. 判定(先出し)

**(A) 数学としての判定 = 条件付き受理可。ただし原案 (i)–(v) は「認証対象の同値性」に対して不足 6 点・過剰 1 点がある。**
補うべき条件を §1.5 に (N-a)〜(N-h) として列挙した。特に **(iv) は致命的に弱い**:「最新 state/terminal が元完成状態と一致する」だけでは rolling 鎖が**主張であって計算ではなくなる**(§1.4-4・§5.1)。

**(B) 設計としての判定 = 受理不可(現状のまま採択してはならない)。理由は 3 つ。**

1. **原案は「回転」ではなく「統合」である。** F-v5-1 と裁定 2225 が問うたのは「最古の batch 親を落とす(= 証拠量を一定に保つ)」設計だが、原案 R1–R4 は全層の証拠を 1 つの親に**畳み込んで全部保持する**設計である。役割数 n は 1 に固定されるが、**認証すべき証拠量は従来どおり線形に増える**。費用モデルの n が「役割数」なのか「証拠量」なのかが未解決である以上、**利益はゼロかもしれない**。
2. **公表済み集計は、いかなる単一機構モデルとも整合しない。**(§4.2)基点 15 role は ZIP 1,669,392,893 B・9,150 file を認証して非 k 固定費 26.1 s に収まる一方、batch 親 1 層は ZIP 377,383,320 B・11,648 file で 44.4 s を要する。**byte あたりでは 7.5 倍、file あたりでは 1.3 倍**。純 byte モデルも純 file モデルも両方を再現できない。したがって 44.4 s/層の律速は「batch 層にだけ存在する仕事」= **層の 128 行再認証**(`authenticate_batch_parent` / `authenticate_next_batch_parent`)である蓋然性が高く、これは**統合親でも消えない**。
3. **塔の真の壁は親層ではなく k·R である。**(§4.4)producer は候補ごとに `physical_factors`(P5 `:3371-3381`)と `ordered_reductions`(P5 `:3403`)を**各々ちょうど rank 個**の要素で構築する。すなわち **per-run 仕事は Θ(k·R)**(コードから確定・回帰ではない)。実測係数を R = 48,384 へ外挿すると消去相だけで **≈ 940–980 s/run**、literal payload だけで **≈ 1.6 GB/run**。**回転設計は、律速でない壁を対象にしている。**

**(C) 先にやるべき最小の一手(GHA 費用ゼロ・数学リスクゼロ)**: producer/checker に **role 別・親層別の経過秒**を 1 行ずつ吐かせる(`progress("admitted-parent", ...)` は既に role ごとに発火しているので秒を足すだけ)。これで n 項の機構(byte / file / k·R_layer)が**一発で確定**する。5 点回帰から設計を決めるより桁違いに安く、確実である。§4.6 に 3 モデルの予測値を置いた(n=3 では 4 % 以内に密集して**分離しない**)。

**(D) 裁定 2225 (3)「1,695 s 一定は未証明」への数学的見立て = 未証明どころか偽。** per-run 仕事の R 依存は少なくとも 1 次(新候補の Θ(k·R))、campaign 全体では層再認証の Σ_i Θ(k·R_i) = Θ(N·k·R̄) が乗る。§4.4・§4.5。

---

## 1. 審査項目 1 — 「認証対象」の定式化と必要十分条件

### 1.1 記法(正典の定義に従う)

- E = F₃^{48384}(physical quotient・1 行 = `packed3` 12,096 B = 48,384 trit・v5 §4)。
- 状態 rank R での行列は**順序付き列** (r_0,…,r_{R−1})、階段形(相異なる lead・self-lead = 1・先行 lead で零)。RREF ではない(v5 §4.1: 後続 lead での非零 5,456 箇所)。
- t ∈ E = target remainder(12,096 B)。θ_j = `target.scalar` ∈ {0,1,2} ⊂ F₃。
- 公刊符号規約(coverage-receipt): `target_update_sign: remainder_before − theta * normalized_row`。
- sr = `signrep`: sr(0)=0, sr(1)=+1, sr(2)=−1。語層の指数に使う(`correction appends normalized_word^sr(target.scalar)`・P5 `:3954`)。
- D = 祖先列(`accepted_target_derivation_parents`)。基点 97 = 32(5-key)+ 65(6-key)。batch 行は **10-key** レコードを追記(P5 `:2056-2057`):
  `(role, candidate_ordinal, local_row_offset, row_manifest_sha256, instruction_sha256, target_sha256, parent_remainder_sha256, remainder_sha256, scalar, state_head)`。
  累積則 97 → 225 → 353 → 481(毎回 +128・prefix 完全一致・P5 `:2043-2046`)。
- rolling 鎖: `rolling_sha256 = sha(bytes.fromhex(predecessor) ‖ canonical(body))`(body から schema/sha256/rolling_sha256 を除く)。
- λ: `row_pairings_sha256 = sha(0x00 × R)`・λ·t₀ = λ·t_final = 1。
- ρ₂: `mode=derived, value=1, original_rho2_directly_read=False`・`original_rho2_packed_sha256` を pin 保持。

### 1.2 認証対象 Σ の定義

**定義 1.** run が認証する対象を次の 7 組とする:

  Σ = ( A ; (r_0,…,r_{R−1}) ; t ; D ; h ; λ ; ι )

- A = anchor(基点 state_head + 元 64/continuation の identity)
- (r_i) = **順序付きの行 bytes 列**(span ではない)
- t = 現 target remainder の bytes
- D = 順序付き祖先列(|D| = 97 + (R − 1450))
- h = 終端 state_head(= 次 run の anchor)
- λ = 現証明書(positive 分岐では null)
- ι = 出所解決写像(各要素 → origin artifact + native schema + path)

**定義 2(検証命題集合).** run が生 bytes から再導出する命題の集合を V とする。主要な成分:

| 札 | 命題 | 順序感受性 |
|---|---|---|
| I₁ | 階段形(lead 相異・self-lead=1・先行 lead で零) | **あり**(部分的) |
| I₂ | t_base = t + Σ_j θ_j r_j (mod 3) | **なし**(可換和) |
| I₂' | 逐次 digest 鎖 `D[j].remainder = D[j+1].parent_remainder` | **あり** |
| I₃ | D = D_base ‖ D_1 ‖ … ‖ D_m(record-wise・θ=0 込み) | **あり** |
| I₄ | rolling 鎖の畳み込みが h に到達 | **あり(完全)** |
| I₅ | λ ⊥ 全 R 行(sha(0^R))・λ·t = 1 | なし |
| I₆ | 各行の導出閉包(raw → source → P1 → B → reduction → literal → witness) | — |
| I₇ | 入力保全(全 file/空 dir・不変性) | — |

**同値性は Σ の一致(対象同値)であり、V の一致(証拠同値)ではない。原案は両者を区別していない。** これは形式上の難癖ではない: **Φ_new(P₀,B) = Φ_old(P₀,S₁..S_m) を満たしつつ V_new ⊊ V_old となる設計が実在する**(§5)。裁定 2225 (i) の文言「認証対象/ρ₂・literal ancestry を保持する同値性」は前者しか要求していないので、**後者を独立の納品条件として追加すべきである**。

### 1.3 必要十分条件(定理)

**定理 1.** 𝒫_old = (P₀; S₁,…,S_m)、𝒫_new = (P₀; B) とし、Φ を次 run の P/C が読む全量への読み出し写像とする。Φ(𝒫_old) = Φ(𝒫_new) ≠ ⊥ であるための**必要十分条件**は、位置の全単射 ν(層内座標 (i,j) → 統合親の大域座標)が存在して次が成り立つことである:

- **(N1) 行 identity**: q^new_{ν(i,j)} = q^{S_i}_j が bytes 一致し、ν は辞書式順序を保つ(ν(i,j) < ν(i',j') ⟺ (i,j) <_lex (i',j'))。長さ 12,096・packed3・self-lead = 1 を含む。
- **(N2) 祖先 identity**: D_new = D_base ‖ D_{S_1} ‖ … ‖ D_{S_m} が canonical JSON として record-wise 一致(θ=0 レコード・5/6-key 基点 prefix を含む)、|D_new| = 97 + 128m。
- **(N3) target endpoints と鎖**: 両端の target payload が bytes 一致し、全 128m の逐次 digest 鎖 I₂' が閉じる。
- **(N4) 鎖の再計算可能性**: 保持された instruction body が bytes 一致し、rolling 畳み込みが元と同じ state_head 列を**再生成する**(最終値の一致では足りない)。B の terminal = S_m の terminal。
- **(N5) 終端状態**: λ payload が bytes 一致、rank/generation/|D|/current/previous target が一致。
- **(N6) typed 解決の同値**: 保持文書中の全参照が B ∪ P₀ 内で元と同じ raw bytes へ解決し、その解決は**検証済みの ν** を経由する(ν 自体が第三者に検査可能であること)。
- **(N7) 保全**: B の file/dir inventory が(ν の path 作用を除いて)⋃_i inventory(S_i) の**荷重閉包**へ全射・path 衝突なし・空 dir 明示。

*必要性*: (N1) 行 bytes は直接 hash される。(N2) `canonical(actual) == canonical(prefix + appended)`(P5 `:2067`)が直接比較する。(N3)(N5) 次 run の driver が state_head/target/λ/rank/gen を **literal で pin する**(v5 §8「親 pin」)ので bytes 一致が要る。(N4) rolling 値は body から計算される量であり、値だけ写しても再計算で一致しなければ落ちる。(N6) は R2(ii) の主張そのもの。(N7) は `all_parent_files_and_directories_unchanged` と inventory 5-key の要求。
*十分性*: (N1)–(N7) の下で Φ の読む全量が bytes 同一になるので Φ は一致する。∎

### 1.4 原案 (i)–(v) の判定

| 原案 | 定理 1 との対応 | 判定 |
|---|---|---|
| (i) 行 identity | N1 ⊆ (i)、N7 の一部 | **十分**(ただし ν の検証可能性は未言及) |
| (ii) 元の導出の意味 | N6 ⊆ (ii) | **不足**: ν が「検証済み全単射」であることを条件にしていない |
| (iii) target 履歴 | N2 の一部・N3 の一部 | **不足 3 点**(下記 1〜3) |
| (iv) 状態と terminal | N5・N4 の一部 | **不足(最重要)**: 下記 4 |
| (v) 全閉包と保全 | N7 ⊆ (v) | **過剰**: 下記 5 |

**1. 層境界オブジェクト(segment table)が無い。** 10-key レコードは `role="batch-row"`・`local_row_offset ∈ 0..127` を**全層で反復**する(P5 `:2060-2062` は `candidate_ordinal == local_row_offset == ordinal` を層内序数として要求)。層の区別は現在 **role 名**(`batch-parent` / `batch-parent-v4`)と `parent-row` 記述子(P5 `:2950-2952`)だけが担っている。統合すると role が 1 つになり、**481 件の平坦なリストには層の境目が残らない**。canary `inherited225-as-complete353` / `v4-local0-as-v3-local0` はこの境目を突く試験なので、**境目が消えれば試験も空虚化する**。
→ 必須追加: 各吸収層 i について `(offset_i, count_i = 128, rank_in_i, gen_in_i, t_in_i, t_out_i, h_in_i, h_out_i, origin_artifact_i, origin_schema_i, origin_run_i)` の**明示 segment table**、および `off_{i+1} = off_i + 128`・`t_out_i = t_in_{i+1}`・`h_out_i = h_in_{i+1}`。

**2. 中間 remainder の数値再導出が条件になっていない。** (iii) は「前後 target を順序付きに保つ」としか言わない。digest は値ではない。現行 CV-9 は**両端**しか数値再導出していない(v5 §4.3: t_final に θ_j·row_j を足し戻して t₀ の sha に一致)。中間 127 点は hash 鎖の連結だけで支えられている。
→ 必須追加: (t_final, (θ_j, q_j)_j) からの後退累積で**全中間 remainder を再構成**し、128m 個の `parent_remainder_sha256` / `remainder_sha256` を**全数照合**する。費用は 128m × 12,096 B(m=3 で 4.6 MB、m=370 でも 573 MB)= 秒未満〜数秒。**統合親はここで従来より強くなれる。安いので必須にせよ。**

**3. 「θ を保つ」ことの根拠が I₂ に依存している。** §2.3 の核補題により、I₂ は θ=0 レコードの**削除に対して不変**である。θ=0 は v5 実データで **54/128**(42 %)を占める。(iii) は「theta0 を消さない」と正しく書いているが、**なぜそれが I₂ から従わないか**を書いていないので、実装者は「総和が合うから良い」と読み違え得る。

**4. 【最重要・不足】(iv) は rolling 鎖の再計算を要求していない。** 「最新 state/terminal/λ の役割を元完成状態と一致させる」だけである。この条件は、**中間の instruction body を再 seal し、最終 head だけを literal として写した bundle** によって満たされてしまう。そのとき h は「計算結果」ではなく「引き写した主張」になり、I₄ が失われる。
しかも instruction body は **root 束縛 5 field**(`owner_sha256` / `source_sha256` / `start_sha256` / `selection_start_sha256` と自 `sha256`)を含む(v5 §5.2 が実測で特定)。ゆえに:
→ 必須追加 (N4): **吸収層の instruction / candidate-manifest / row-manifest を逐語保持**し、それらが束縛する **元 run の root 文書(owner/source/start/selection-start)も同梱**する。統合親は「自分の root に束縛されない文書」を正当に含むので、**foreign-binding 型を公開型として明示**しなければ現行の exact-key 検査が誤って落とす(または、落とさないために検査を緩める = 弱化)。R3 の「自己 hash 循環を作らない」はこの問題を扱っていない。
→ 併せて: **次 run の anchor はどの state_head か**を確定せよ。F-v5-5 が既に「同一数学に 2 つの sealed object」を記録している。変換は**第 3 の seal** を作る。統合親の wrapper seal ではなく、**吸収した最終層の元 state_head** を anchor 定数にしなければ、鎖は変換点で切れる。

**5. 【過剰】(v) の「元 inventory への全射」は荷重に無関係な文書まで巻き込む。** 1 層の output/ 6,587 file のうち **772 checkpoint + 772 telemetry = 1,544(23 %)** は実測秒と進捗であり、Σ の成分でも V の根拠でもない(v5 §5.2 が「相異の原因は C5 pin 伝播と実測秒の 2 つだけ」と特定済み)。これらを毎 run 再認証させるのは純粋な費用である。
→ 推奨: 保持文書を **3 層**に明示的に区分せよ。
  - **Tier A(荷重閉包)**: 毎 run 完全 typed 解決。行 bytes・instruction・target.json・row-manifest・literal・reduction・witness・separator・root 文書。
  - **Tier B(証拠だが非解析)**: bundle 内に保持し **bytes 認証(hash)のみ**、parse しない。telemetry・checkpoint・diagnostics。
  - **Tier C(冷 pin)**: bundle 外・digest だけ保持(Release ミラーで恒久保全済)。
  **Tier B/C の線引きこそが本件の実質的な設計判断であり、R4 が「別スコープ」として棚上げしたものである。** §5.3 参照。

### 1.5 追加すべき条件(まとめ)

- **(N-a)** ν = 検証済み全単射・順序保存・`resolve_new ∘ ν = resolve_native`(bytes・row_manifest_sha256・10-key レコードの 3 水準で)。かつ**保持された native 文書は ν を使わずに自己整合に読める**こと(ν を信用せず検査できるため)。
- **(N-b)** segment table(§1.4-1)。
- **(N-c)** 全中間 remainder の数値再導出と 128m digest 全数照合(§1.4-2)。
- **(N-d)** rolling 鎖の**リンク単位再計算** + foreign-binding 型の公開 + 次 anchor の確定(§1.4-4)。
- **(N-e)** 証拠同値 V_new ⊇ V_old の明示(定義 2)。満たせないなら**どの命題が落ちるかを列挙**して裁定に上げる。
- **(N-f)** fixture/canary の置換義務: 層形の 7 拒否(P/C 各)が空虚化するので、統合形の拒否を**同数以上・相異ラベル・実データ上非空虚**で事前登録(§6.2 D 群)。
- **(N-g)** DERIVED の非昇格: `original_rho2_directly_read = false` と `original_rho2_packed_sha256` を変換で不変に保つ。**構造帰納法で DERIVED を実算へ昇格させない**(原案は正しく書いている・維持)。
- **(N-h)** Tier A/B/C の明示と各 Tier の volume 公開(§1.4-5)。

---

## 2. 審査項目 2 — 合成則 t_B = t_S + Σ θ_j q_j の証明と核

### 2.1 補題 1(望遠鏡則)

**補題 1.** ステップ列 t_{j+1} = t_j − θ_j q_j (j = 0,…,A−1・E = F₃^N 上)に対し
  **t_0 = t_A + Σ_{j=0}^{A−1} θ_j q_j.**

*証明*(A に関する構造帰納法). A = 0: 両辺 t_0、空和 = 0。✓
帰納段: t_0 = t_A + Σ_{j<A} θ_j q_j を仮定。定義より t_{A+1} = t_A − θ_A q_A、E は F₃ 加群だから t_A = t_{A+1} + θ_A q_A。代入して
t_0 = t_{A+1} + θ_A q_A + Σ_{j<A} θ_j q_j = t_{A+1} + Σ_{j<A+1} θ_j q_j. ∎

符号規約は F₃ の減法であり、θ の代表元 {0,1,2} の取り方に依らない。**F₃ 水準では符号の曖昧さは無い。**

### 2.2 補題 2(層の合成 = 連結)

**補題 2.** 層 i が t^{(i)}_in から t^{(i)}_out への 128 ステップ列で、**合成可能性** t^{(i)}_out = t^{(i+1)}_in (i = 1..m−1) が成り立つとき、連結列は正当なステップ列であり
  **t^{(1)}_in = t^{(m)}_out + Σ_{i=1}^{m} Σ_{j=0}^{127} θ^{(i)}_j q^{(i)}_j.**

*証明*. 合成可能性は「層 i+1 の最初のステップの before = 層 i の最後のステップの after」に等しく、これが成り立てば連結列は補題 1 の前件を満たす。補題 1 を連結列に適用。∎

**合成可能性が、統合親における唯一の非自明な前件である。** 現行設計ではこれは digest 一致(`next_batch_previous_is_parent_start_current_target`・P5 `:2070-2073`)で担保されている。平坦化後は **I₂'(逐次 digest 鎖)を層境界を跨いで全数要求する**ことで担保する(= (N-c))。境界の起点は基点 anchor の target(v3 判読 §4.3 が逆順再構成で一致を確認した親 target)。なお**基点 97 レコードは 5-key/6-key で `parent_remainder` / `remainder` を持たない別スキーマ**なので、digest 鎖は最初の batch レコードから始まり、その `parent_remainder_sha256` が基点 anchor target と一致することを別途要求する必要がある。

### 2.3 核補題(I₂ が決めないもの)— **原案の論証の向きは逆である**

S(D) := Σ_j θ_j q_j と置く。

**補題 3.**
(a) S は θ=0 レコードの**削除・挿入**に対して不変。
(b) S はレコードの**任意の置換**に対して不変(可換和)。
(c) S は (θ, q) ↦ (2θ, 2q) に対して不変。
(d) しかし **行が一次独立なら、S と行列 (q_j) から θ ベクトルは一意に定まる**。
(e) (c) は I₁ が殺す: 2q の self-lead は 2 であり、階段正規化(self-lead = 1)に違反する。

*検算*(F₃・N=64・A=24・階段形生成・seed 20260908): (a) True(θ=0 が 6 件削除されても S 不変)、(b) True、(c) True かつ 2q の self-lead は全て 2、(d) rank(rows) = 24/24 で一意、(e) 上記より。加えて sr が加法を保たない対 (1,1),(2,2) を全数確認。rolling 畳み込みは置換で head が変わることも確認(§2.4)。

**帰結(重要).**
- **θ ベクトル自体は偽造できない**(補題 3(d)): 行 bytes と両端 target があれば θ は一意に決まる。これは統合親にとって強い追い風である(§3.1 命題 2 の B9)。
- **しかし I₂ は次を一切決めない**: ① D の**順序**、② θ=0 の行が D に**記録されているか**、③ 中間 remainder、④ state_head 列、⑤ instruction / manifest digest。
- したがって R2(iii) の論証「各式を履歴順に連鎖すると t_B = t_S + Σ θ_j q_j であり、元基点 identity と合成した認証対象が保持される」は **向きが逆**である。強い言明は**鎖**(I₂' と I₄)であり、**総和は弱い系**にすぎない。原案の一文「この式の総和だけを確認して個々の祖先 identity を捨ててはならない」は正しい注意だが、**二つの核(順序置換・θ=0 削除)を同定していない**ため、実装仕様としては不十分である。

### 2.4 順序を固定するのは何か

- **I₄(rolling 鎖)は順序を完全に固定する**(hash 畳み込みは非可換・検算で置換により head が変化)。
- **I₁ は部分的に固定する**: 行 i < j に対し r_j[lead(r_i)] = 0 が要求される一方、r_i[lead(r_j)] ≠ 0 が v5 で 5,456 箇所 / 最大 8,128 対 = **67 %** 観測されている。この 67 % の対は転置すると I₁ を破る。残る 33 % は I₁ だけでは可換。
- **I₂' も固定する**(digest 鎖)。
⇒ **順序保存の根拠は I₄ と I₂' に置くべきで、I₂ に置いてはならない。**

### 2.5 語層は合成しない — 段の併合の禁止

`sr` は F₃ → ℤ の**切断であって準同型ではない**: sr(1)+sr(1) = 2 ≠ sr(2) = −1、sr(2)+sr(2) = −2 ≠ sr(1) = 1(検算で全数確認)。三層の符号(v4 §8.2)は
`target_literal_factor.exponent = +sr(θ)` / `physical_factors[].exponent = −sr(coefficient)` / `outer_exponent = +sr(σ)`
であり、`correction appends normalized_word^sr(target.scalar)`(P5 `:3954`)が語(自由群/群環)への追記である。

**系.** 同一行に触れる 2 段を「scalar を θ₁+θ₂ にまとめた 1 段」へ**併合すると、target 恒等式は保たれるが語層の指数が壊れる**。また語は非可換なので、**語因子の順序も保存しなければならない**。
本設定では各行はちょうど 1 段にしか現れないので併合は生じないが、**統合器が「最適化」として併合しないことを側条件として明記せよ**。順序保存の理由も、I₂(可換)ではなく**語層(非可換)**に置くのが正しい。

---

## 3. 審査項目 3 — ρ₂ ancestry の担保

### 3.1 何が再導出でき、何ができないか(切り分け)

補題 3(d) と (N-c) から次が従う。

**命題 2.** 統合親が (α) 全 R 行の payload bytes を順序付きで、(β) 基点 target payload と現 target payload を、(γ) 順序付き 10-key 祖先列を、(δ) 各レコードが指す instruction / target.json / row-manifest を逐語で保持するならば、**第三者は生 bytes だけから ρ₂ ancestry の全数値内容を再導出できる**:
1. D の θ 列 → S = Σ θ_j q_j を計算 → t_base = t_final + S を照合(両端 payload と bytes 比較)。
2. t_final から後退累積で全中間 remainder を再構成 → 128m 個の `parent_remainder_sha256` / `remainder_sha256` を全数照合。
3. instruction body を canonical 化して rolling 畳み込み → 全 state_head を再生成 → D の `state_head` 列および終端 h に一致。
4. `row_manifest_sha256` → row-manifest → `physical_sha256` → 行 payload の sha、を全数照合。
5. `target_sha256` → target.json → その {parent_remainder_sha256, remainder_sha256, scalar} が D のレコードの 3 field と一致。

**⇒ ρ₂ ancestry(= target 導出鎖)の担保に、層を親として持ち回る必要は無い。O(R) の再計算で足りる。** これは統合案にとって**最も強い肯定材料**である。

**逆に、統合親では再導出できないもの**:
- **各行の語水準の導出閉包**(raw-word → raw-source → P1 reduction → B(四 character)→ reduction → physical-literal → witness)。これは当該行を作った run の実算そのものであり、bytes を持ち回っても「再導出」ではなく「再読解」にすぎない。
- **出所の証言**(どの run/commit/artifact がこれらの bytes を生んだか)。これは pin と Release ミラーで担保する。

**この切り分けが本件の核心である**: 現行設計は毎 run、過去層の語水準閉包を**再解析**している。それは (i) 当該 run で既に 2 系統で cross-check 済み、(ii) bytes が pin されている、(iii) **現 run の数学は過去行の bytes と祖先台帳しか使わない**(語は現 run の候補にしか要らない)、の 3 点から、**厳密な意味で冗長**である。

### 3.2 落とした層の 128 行を何で担保するか(処方)

| 札 | 要求 | 第三者が生 bytes からできること |
|---|---|---|
| ρ-1 | D 逐語保持・\|D\| = 97 + 128m・基点 97 の prefix 完全一致 | canonical 比較 |
| ρ-2 | 10-key の型検査(role="batch-row"・ordinal == local_row_offset == 層内序数・scalar ∈ {0,1,2}・6 digest が 64-hex) | 全数検査 |
| ρ-3 | **segment table**(§1.4-1)と `t_out_i = t_in_{i+1}`・`h_out_i = h_in_{i+1}`・`off_{i+1} = off_i + 128` | 全数検査 |
| ρ-4 | 逐次 digest 鎖 I₂' を層境界跨ぎで全数 | 全数検査 |
| ρ-5 | **中間 remainder の数値再導出**(後退累積) | 128m 回の 12,096 B 演算 |
| ρ-6 | 両端 payload の bytes 一致(t_base = 基点 anchor target・t_final = 統合親 final) | bytes 比較 |
| ρ-7 | 行束縛: レコード → row-manifest → `physical_sha256` → 行 payload(**10-key レコード自体は行 digest を持たない**ので row-manifest の逐語保持が必須) | 全数 |
| ρ-8 | rolling 鎖のリンク単位再計算(instruction body 逐語 + foreign root 文書同梱) | 全数 |
| ρ-9 | θ 分布の非空虚性(segment ごとに {0,1,2} の件数を公開・v5 は 54/36/38) | 全数 |
| ρ-10 | `target_literal_factor.exponent == +sr(scalar)` を保持 literal 全数で | 全数 |
| ρ-11 | 出所 pin(segment ごとに origin artifact id/bytes/digest/run/head/schema) | 突合(payload の代替にはしない) |
| ρ-12 | `original_rho2_packed_sha256` 不変・`directly_read = false` 継続(**DERIVED を昇格させない**) | 突合 |
| ρ-13 | ν の全単射性・順序保存・resolve 可換(§1.5 N-a) | 全数 |
| ρ-14 | λ: `row_pairings_sha256 == sha(0^R)` を**全 R 行**で再計算・λ·t = 1(両端)・新 lead の後退代入 | 全数 |

**「rolling 鎖の再起点をどう封印するか」への答え**: 再起点を作ってはならない。統合親の terminal state_head は**吸収した最終層の元 state_head そのもの**でなければならず、統合器の wrapper seal は鎖の**外側**に置く(R3 の「core の後に GHA 外側束縛を形成する」方針と整合)。鎖は基点 anchor から連続していなければならず、**変換は鎖に 1 リンクも足さない。**

---

## 4. 審査項目 4 — 省ける仕事と省けない仕事

### 4.1 n 項が生じ得る操作の分解

per-run で親層 i につき走る仕事(P5 の実装から):

| 記号 | 操作 | 依存 | 該当コード |
|---|---|---|---|
| A_i | `inventory(root_i)`: rglob + 全 file の sha256 + 全 path の `safe_name` + 辞書構築 | **file 数 F_i と bytes V_i** | `:521-533` |
| B_i | acceptance の宣言 inventory を `validate_input_inventory` で型検査 → `observed == expected` | **F_i** | `:1331-1339`, `:2775-2777` |
| C_i | 層 i の 128 行再認証: instruction/raw/manifest/target/reduction を読み `check_seal`、`ordered_reductions` を**全 R_i 要素**走査、`ordered_sources_sha256` を再計算 | **k·R_i** | `:1754-1786`, `:2326-2358` |
| D_i | native schema の射影(6/7/8-key)と adapter | 層あたり定数 | `:2740`, `:3013` |
| E_i | 空 dir 復元受領証・fixed-reference 受領証 | 層あたり定数 | v5 §2.2, §2.3 |
| F_i | native direct pairing(`native_pairing_rows_rechecked = [1450,1578,1706]`) | **R_i** | v5 §4.4 |

**C_i が決定的である**: `reduction["ordered_reductions"]` の長さは `1450 + ordinal`(P5 `:1754`)/ `1578 + ordinal`(`:2326`)と**明示要求**されており、層 i の再認証は **128 × R_i 個の消去記録**を読んで走査する。

### 4.2 公表集計は単一機構モデルと整合しない(本審査の一次所見)

repo の `REGISTERED_ARTIFACTS`(P5 `:917-1101`)から基点 15 role の ZIP 総量を集計した:

| 集合 | ZIP bytes | file 数 | 非 k 固定費 |
|---|---:|---:|---:|
| 基点 15 role(state…continuation) | **1,669,392,893** | 9,150 | 26.1 s に収まる(v2/v3 が n=0) |
| batch 親 1 層(batch-parent-v4) | **377,383,320**(展開 1,308,094,050) | 11,648 | **44.4 s** |

- **byte あたり**: 基点 ≤ 26.1 / 1,669 MB = **0.0156 s/MB** vs 層 44.4 / 377 MB = **0.118 s/MB** → **7.5 倍の乖離**。
- **file あたり**: 基点 ≤ 26.1 / 9,150 = **2.85 ms/file** vs 層 44.4 / 11,648 = **3.81 ms/file** → **1.34 倍**。

**⇒ 純 byte モデルは 7.5 倍外し、純 file モデルでも 1.34 倍残る。** 残差を説明できるのは「**batch 層にだけ存在する仕事**」= C_i(+D_i, E_i, F_i)である。C_i は Θ(k·R_i) であり、**統合親でも(全証拠の typed 再解決を保つ限り)そのまま残る**。

なお v5 判読の 2 増分から得た「0.11598 / 0.11935 s/MB」の近一致は、**2 層の大きさが 2.2 % しか違わない**ため per-byte と per-layer と per-(k·R) を分離できていない(3 モデルはこの範囲でほぼ共線)。裁定 2225 (1) の「回帰適合を原因同定にしない」はこの点で正しい。

### 4.3 統合で本当に消えるもの / 残るもの

| 項 | 統合後 | 根拠 |
|---|---|---|
| D_i(native adapter・射影) | **消える**(m → 1) | 原案 R4 の狙いどおり。ただし層あたり定数なので寄与は小さいと見込まれる |
| E_i(空 dir 復元・fixed reference 受領証) | **消える**(m → 1) | 同上 |
| F_i(native pairing を層ごと) | **1 回へ**(Σ_i R_i → R) | 実額は小(R=48,384 で 0.6 s 対 30 s 級) |
| B_i(inventory 型検査) | **F の総和が減った分だけ**縮む | 重複がある場合のみ |
| A_i(全 file hash) | **重複分だけ**縮む。重複が無ければ**縮まない** | UNKNOWN 2 の測定が必要 |
| **C_i(層の 128 行再認証)** | **縮まない**(R2(ii)(v) が typed 再解決を要求する限り) | Θ(Σ_i k·R_i) は証拠量に固有 |
| 新 λ の全 R 行 direct pairing | **残る**・Θ(R) | 原案が正しく明記 |
| 新 k 候補の raw/source/P1/B/reduction | **残る**・Θ(k) + Θ(k·R) | §4.4 |

**⇒「n が定数になる」は役割数の話であって、仕事量の話ではない。** 原案 R4 の「一本の全走査」は D_i/E_i/B_i/F_i を畳めるが、**C_i と A_i は証拠量に比例して残る**。R4 の但し書き「親 role 数が一定でも一定時間にはならない」「保持する原証拠の全量が単調増加すれば一回走査の I/O も増える」は正しいが、**その但し書きが利益の主要部分を食い潰す可能性を定量していない**。

### 4.4 【最重要】per-run 仕事の R 依存 — 裁定 2225 (3) への回答

**コードから確定する事実**(回帰ではない):
- `physical_factors` は候補ごとに **ちょうど `state["rank"]` 要素**(P5 `:3371-3373, :3378-3380`)。各要素は row source 記述子(sha256 2 本を含む ≈ 250–280 B)を埋め込む。
- `ordered_reductions` も候補ごとに **ちょうど rank 要素**(P5 `:3371, :3403`)。
- 検証側も層ごとに `len(ordered_reductions) == R_i + ordinal` を要求して全走査(`:1754-1756`)。
- v4 判読の実測がこれを裏づける:「候補あたり平均 1,640 factor = 1578 + ordinal に一致」「32 候補の 52,480 entry」。

**⇒ per-run の producer 仕事は Θ(k·R)**、出力 payload も Θ(k·R) bytes。

実測係数(v5 §7.1: 消去相 34.301520 s / 128 候補 / 平均 rank ≈ 1,770)= **1.51 × 10⁻⁴ s /(候補 × 行)**。
外挿(**線形外挿であり法則ではない**・裁定 2225 (2) の射程制限を継承):

| R | k=128 の消去相 | k=128 の literal payload(概算 260 B/要素) |
|---:|---:|---:|
| 1,834 | 35.9 s | 61 MB |
| 12,000 | 235 s | 400 MB |
| 24,000 | 470 s | 799 MB |
| **48,384** | **946 s** | **1.61 GB** |

これは**親層をゼロにしても残る**。producer cap 5,400 s に対し、消去相だけで 946 s、p1 相(候補あたり 7.90 s・R 非依存と仮定)が 1,012 s、合計で既に 1,958 s。k を 425 へ上げると消去相だけで **3,142 s**、p1 相が 3,359 s で **合計 6,501 s > cap**。
**⇒ F-v5-1 の「回転すれば k_max ≈ 425 で約 110 run」は、k·R 項を無視した見積りであり成立しない。**(裁定 2225 (2) は既に「110 run で A0 完了へ拡張しない」と射程を切っており、本所見はそれを数学側から補強する。)

さらに campaign 全体では、run N が層 1..N−1 を再認証するので **Σ_i k·R_i = Θ(N·k·R̄)**、campaign 総計 **Θ(N²·k·R̄)**。R = 48,384 到達に N ≈ 370(k=128)とすると、最終 run の再認証だけで ≈ 128 × Σ R_i ≈ 128 × 370 × 24,000 ≈ **1.14 × 10⁹ 消去記録**。**いかなる包装でも読み切れない。**

**⇒ 結論: 過去層の消去記録を毎 run 再解析する設計は、統合しようが回転しようが塔を登れない。R4 が「別スコープ」として外した「過去証拠を再解析しない」方式こそが、唯一の登坂手段である。**

### 4.5 「1,695 s 一定」への見立て

**未証明ではなく偽**。per-run 仕事の R 依存の次数:
- 新候補: **Θ(k·R)**(literal + ordered_reductions + 実消去)
- 全 R 行への新 λ direct pairing・階段検査: **Θ(R)**
- 層再認証: **Θ(Σ_i k·R_i)**(統合しても証拠量が同じなら同じ)
- 祖先長 L = 97 + 128m: **Θ(L)**(中間 remainder 再導出を入れても軽い)
- origin metadata 量 M: **Θ(M)**

最小でも 1 次、campaign では実質 2 次。**定数時間は成立しない。**

### 4.6 費用を識別する公開計測項目(R4 の要求を具体化)

原案の「unique / total の visit・bytes・row・context」に加えて、**機構同定に直結する最小 3 項目**を要求する:

1. **role 別・親層別の経過秒**(`progress("admitted-parent", role, files)` に `seconds` を足すだけ)。→ A_i と C_i の分離。
2. **C_i 相の計器**: 層 i の再認証で読んだ `ordered_reductions` 要素の総数と経過秒。→ Θ(k·R_i) の直接確認。
3. **A_i 相の計器**: 層 i で hash した bytes 総量・file 数・経過秒。→ per-byte / per-file の分離。

**予測(3 モデルの分岐点・次 run n=3 で測れる)**:

| モデル | 層項の予測(v6・n=3) |
|---|---:|
| per-layer 一定(F-v5-1) | 3 × 44.4 = **133.2 s** |
| per-byte(0.118 s/MB・v5 親 385 MB) | **136.5 s** |
| **per-(k·R_i)**(2.29 × 10⁻⁴ s/要素) | 128 × (1450+1578+1706) × 2.29e-4 = **138.9 s** |

**n=3 では 3 モデルが 4 % 以内に密集して分離しない。** 上記の計器 1〜3 なら**その run で確定する**。**設計判断は計器の後に行うべきである。**

---

## 5. 審査項目 5 — 弱化の検出

### 5.1 従来 CV-9 検問への影響

| 検問 | 統合後 | 評価 |
|---|---|---|
| 階段形 I₁(全 R 行) | 生 bytes から再計算・不変 | **不変** |
| λ の後退代入・`row_pairings = sha(0^R)` | 全 R 行で再計算・不変 | **不変** |
| target 恒等式(両端) | 不変。中間も (N-c) を入れれば**強化** | **強化可能** |
| rolling 鎖 | **危険**。(iv) のままだと主張に退化(§1.4-4) | **要 (N-d)** |
| ρ₂ 累積則 97→225→353→481 | 平坦化で層境界が消える。**要 segment table** | **要 (N-b)** |
| source 28/28・checkout-sources 32/32 | 現 run の自系コード。不変 | **不変** |
| 親 inventory 5-key・空 dir 復元 | 1 親分になる。canary は再設計要 | **要 (N-f)** |
| 層形 canary 7 件/側 | `omit-v3-from-old16-projection`・`v4-local0-as-v3-local0`・`inherited225-as-complete353`・`fixed-reference-as-colocated-payload` の 4 件は**指示対象を失う** | **空虚化・要置換** |
| m 重の独立証言 | **失われる**(§5.2) | **本質的弱化** |

### 5.2 m 重の独立証言の消失(統合案の本質的な代償)

現行では、層 i の数学は**層 i を作った run 自身の sealed 文書**(別 commit・別 GHA run・別 P/C 著者分離)によって証言されており、毎 run その native 文書を native schema で読み直している。これは **m 個の独立した証言の再確認**である。

R3 は「**新統合親が過去の統合親を再帰 load しないと全意味を解決できない状態は R3 の失敗**」と明記する。つまり**原資料が入力でなくなることを設計として要求している**。ゆえに変換後は、全ての将来 run が **1 つの変換器 P_conv の産物だけ**を読む。P_conv のバグ(または変換時の改竄)は以後**不可視**になる。

これは「別スコープの変更」ではなく、**R1–R4 自身の帰結**である。正直な定式化は:

> 変換は独立 2 著者(P_conv / C_conv)が**元の層 artifact に対して 1 回だけ**照合し、その等値証明書を bytes + sha で裁定に pin する。以後は「1 回 cross-check 済み・以後は pin により引用」という格付けになる。

**これは R4 が排した「冷 pin」と同じ認識論的な一手を、連続的にではなく一時点で行うもの**である。防御可能だが、**格付けの変更として明記されねばならない**: 「毎 run が生から全再導出」→「毎 run が変換済み bundle から全再導出、変換自体は 1 回 cross-check」。

### 5.3 「全過去証拠を pin だけの冷保存へ替える」が別変更である理由(数学の側から)

再導出不能になるのは次である:

1. **語水準の導出閉包**(raw-word / raw-source / P1 reduction / B / physical-literal / witness)。行 payload だけからは Ω 語も P1 減算も復元できない(語 → 行は情報損失を伴う写像であり、逆像は payload に無い)。冷 pin にすると、**「この行は実在の Ω 語から来た」という命題が bundle 内で再検査不能**になる。
2. **消去の逐語記録** `ordered_reductions`(各行に対する係数と語因子指数)。これが無いと、行が**既存 span から実際に前進消去で得られた**ことが再検査できず、I₁(階段形)だけの証拠に落ちる。
3. **witness の全 field**(v5 §5.2 が `basis_chords`・`cycles`・`edge`・`eta`・`failed_chord`・`tau` 等の同一性を確認した対象)。

**逆に、冷 pin にしても失われないもの**: Σ の全成分(§3.1 命題 2)。すなわち **ρ₂ ancestry・target 鎖・rolling 鎖・階段形・λ 証明書は行 bytes と祖先台帳だけで完全に再導出できる。**

**⇒ 冷 pin の代償は正確に「過去行の語水準の由来を、毎 run 再検査する能力」である。** これは (i) 当該 run で 2 系統 cross-check 済み、(ii) bytes が pin され Release ミラーで恒久保全済(裁定 2222 補記)、という条件下では、**再検査の限界効用が極めて低い**。§4.4 の Θ(N²·k·R̄) と突き合わせれば、**この一点を譲らない限り塔は登れない**というのが本審査の結論である。

---

## 6. 審査項目 6 — 判定と v7 CV-9 checklist 案

### 6.1 個別裁定(task 1111 F1 の要求項目)

| 論点 | 裁定 | 根拠 |
|---|---|---|
| 「span だけ同一」 | **不可** | Σ は順序付き行列・D・h を含む(定義 1)。span は I₁/I₄/I₂' を決めない |
| 「元 local0 衝突」 | **不可**、かつ**統合案で悪化** | 10-key は role="batch-row"・local 0..127 を全層で反復(P5 `:2060-2062`)。役割名という唯一の識別子を統合が奪う。**segment table + ν 必須** |
| 「元 97 を 10-key 化」 | **不可** | 基点 97 は 5-key/6-key の別スキーマ。cast は D の canonical 比較(`:2067`)を破る。かつ digest 鎖の起点が消える |
| 「theta0 を削る」 | **不可**。**I₂ からは検出できない**ので独立条件が必須 | 補題 3(a)。v5 実データ 54/128 |
| 「target sign 反転」 | **不可**。ただし F₃ 水準では符号は一意(§2.1)。**危険は語層の sr** | sr は準同型でない(§2.5)。`+sr(θ)` / `−sr(coefficient)` / `+sr(σ)` の三層を混同する誤りが本命 |
| 「最新 λ を再利用して新 λ 照合を省く」 | **不可** | λ_new ⊥ 全 R 行 は新 λ 固有の命題。原案も正しく明記 |
| 「sealed prefix だけで参照閉包を切る」 | **原案どおり不可**。ただし §5.3 の切り分けを条件に**別途裁定すべき対象**である | 冷 pin の代償は語水準の再検査能力に限定される |
| 「hidden history import」 | **不可** | (N7) の path 衝突禁止・全射条件で塞ぐ。ν の全単射性でも塞ぐ |
| 「positive を MEMBER へ変える」 | **不可** | 原案どおり。same-word adapter / positive readout 未了 |
| **段の併合(新規指摘)** | **不可** | §2.5 系。target 恒等式は保つが語層が壊れる |
| **rolling 鎖の再 seal(新規指摘)** | **不可** | §1.4-4。(iv) はこれを許してしまう |
| **wrapper seal を次 anchor にする(新規指摘)** | **不可** | §3.2。鎖は変換点で 1 リンクも増やさない |

### 6.2 v7 CV-9 checklist 案(統合親を格付けするときの検問)

**A 群 — 対象同値(定理 1)**
- A1. ν の全単射性・順序保存を全 R 行で確認(片側のみ 0・重複 0)。
- A2. 全 R 行 payload の bytes 一致(元層 artifact と統合親の双方から取得して照合)。
- A3. D の canonical 一致(\|D\| = 97+128m・基点 97 prefix・record-wise)。θ=0 件数を segment 別に公開。
- A4. segment table の整合(off / t_in / t_out / h_in / h_out / rank / gen / origin pin)。
- A5. 両端 target payload の bytes 一致。
- A6. λ payload の bytes 一致・rank / generation / \|D\| 一致。
- A7. 統合親の terminal state_head == 吸収最終層の元 state_head(**wrapper seal ではない**)。次 run の anchor 定数がこれと一致。

**B 群 — 数値再導出(生 bytes から第三者が)**
- B1. I₂: t_base = t_final + Σ θ_j q_j を packed3 で再構成し sha 一致。
- B2. **I₂'(新設・必須)**: 全 128m 中間 remainder を後退累積で再構成し、`parent_remainder_sha256` / `remainder_sha256` を**全数**照合。
- B3. I₄: instruction body の canonical から rolling 畳み込みを全リンク再計算 → 全 state_head と終端 h に一致。
- B4. I₁: 全 R 行の lead 相異・self-lead=1・宣言 lead == 最初の非零・先行 lead で零 = 違反 0。後続 lead の非零件数を公開(非空虚性)。
- B5. I₅: `row_pairings_sha256 == sha(0^R)` を全 R 行で再計算、λ·t = 1(両端)、新 lead 成分の後退代入。
- B6. 行束縛: レコード → row-manifest → `physical_sha256` → 行 payload を全数。
- B7. target.json 束縛: `target_sha256` → 3 field が D のレコードと一致(全数)。
- B8. `target_literal_factor` = {row_id, local_row_offset, coefficient=θ, exponent=+sr(θ), normalized_literal_sha256} を保持 literal 全数で。
- B9. **θ の一意性検査(新設)**: 全 R 行が一次独立であることと S から θ 列が一意に定まることを確認(補題 3(d))。これは D の scalar 列を**独立に裏取り**する。

**C 群 — 弱化の検出**
- C1. V_new ⊇ V_old の差分表(落ちた命題の明示列挙)。落ちたものがあれば裁定対象。
- C2. Tier A/B/C の分類表と各 Tier の file 数・bytes(§1.4-5)。
- C3. DERIVED 非昇格: `original_rho2_directly_read == false`・`original_rho2_packed_sha256` 不変。
- C4. foreign-binding 型の公開定義と、それを許す検査が**他の束縛を緩めていない**ことの明示。
- C5. 変換の 1 回 cross-check 証明書(P_conv / C_conv・著者分離・元層 artifact に対する照合)の pin。
- C6. 元層 artifact の恒久保全(Release ミラー)の pin 再掲。

**D 群 — fixture / canary(層形 7 件の置換・P/C 各 ≥ 7・相異ラベル・実データ上非空虚)**
- D1. `merge-drops-theta-zero-record`(θ=0 を 1 件落とす)
- D2. `merge-permutes-two-ancestry-records`(順序置換・I₂ は通るが I₂'/I₄ で落ちること)
- D3. `merge-collides-two-layer-local0`(異層 local0 を同一視)
- D4. `merge-casts-legacy-97-to-ten-key`
- D5. `merge-reseals-instruction-bodies`(rolling 鎖が主張に退化)
- D6. `merge-uses-wrapper-seal-as-anchor`
- D7. `merge-omits-segment-boundary`(t_out_i ≠ t_in_{i+1} を通す)
- D8. `merge-fuses-two-steps-same-row`(scalar 加算で target は通るが語指数が壊れる・§2.5)
- D9. `merge-substitutes-equivalent-json`(同値だが別 bytes の JSON への置換)
- D10. `merge-double-assigns-logical-path`(path 衝突)
- D11. `merge-omits-registered-empty-dir`
- D12. `merge-promotes-derived-rho2`

各件について `intended_label_reached: true` と**相異なるエラーラベル**を要求(v5 §6 と同型)。

**E 群 — 費用の識別(§4.6)**
- E1. role 別・親層別の経過秒。
- E2. 層再認証で走査した `ordered_reductions` 要素総数と秒。
- E3. hash した bytes / file 数と秒。
- E4. unique / total の visit・bytes・row・context(原案の要求)。
- E5. **k·R 項の公開**: 当該 run の Σ_{候補} rank(= physical_factors 総要素数)と literal payload 総 bytes。

### 6.3 事前登録すべき恒等式・fixture・陰性例

**恒等式(変換前に凍結)**
1. t_base = t_final + Σ_j θ_j q_j (mod 3)、両端は payload bytes で固定。
2. ∀j: t_j = t_{j+1} + θ_j q_j、かつ sha(pack(t_j)) = D[j].parent_remainder_sha256。
3. ∀j: D[j].remainder_sha256 = D[j+1].parent_remainder_sha256(境界跨ぎ)。
4. 最初の batch レコードの parent_remainder_sha256 = 基点 anchor target の sha。
5. h_j = sha(bytes.fromhex(h_{j−1}) ‖ canonical(body_j))、h_{−1} = 基点 anchor。
6. \|D\| = 97 + 128m、D[0:97] = 凍結された基点列。
7. ∀j: exponent = +sr(scalar)、coefficient = scalar。
8. `row_pairings_sha256` = sha(0x00 × R)。

**fixture(positive / negative / adversarial の三分)**
- positive: 実 v3/v4/v5 の 3 層を変換した既知の bundle 断片(小規模再現: 各層 4 行の縮小 fixture)で全恒等式が通ること。
- negative: D1–D12 の各改竄。
- adversarial: (a) I₂ は通るが I₂'/I₄ が落ちる置換、(b) θ=0 削除、(c) 段の併合、(d) 同値別 bytes JSON、(e) wrapper seal anchor。
  **(a)(b)(c) は「target 恒等式だけ見ていると通ってしまう」型であり、本審査が最も重視する陰性例である。**

**陰性例(必ず落ちること)**
- 統合親のみで、元層 artifact を一切参照せずに B1–B9 を通せること自体は**正しい**(R3 の自己完結要求)。しかし **A1/A2 を元層 artifact と照合せずに PASS を出す変換検収**は陰性例として拒否せよ(変換の 1 回照合は元層に対して行われねばならない)。

---

## 7. 未解決・UNKNOWN として残すもの

- **UNKNOWN 1**: 44.4 s/層の機構(per-byte / per-file / per-(k·R_i))。§4.2 の乖離により**単一機構では説明できない**ことは示したが、内訳は未測定。**計器 E1–E3 が入るまで統合の利益は UNKNOWN のままである。**
- **UNKNOWN 2**: 各層 artifact 間の内容重複率。展開値の差は v4 tree − v3 tree = 40,494,912 B / +211 file であるのに対し、1 run の output/ は 6,587 file である。この不整合(層 artifact が自 output 全部を積んでいるなら +6,587 file のはず)を私は解決できていない。**重複率は 2 つの親 artifact の中央ディレクトリ(name + size + CRC32)の比較で GHA 費用ゼロで測れる**(v5 §5.1 と同じ手法)。統合の A_i 削減量はこの一数値で決まる。
- **UNKNOWN 3**: checker 側の相別内訳(限定条項 6・段別 timestamp 無し)。C の n 依存(+57.257 / +28.048 と非線形)は説明できていない。
- **UNKNOWN 4**: p1 相(候補時間の 71.7 %)が R 非依存であることを私はコードから確認していない(候補自身の語処理と読んだが、未検算)。もし R 依存なら §4.4 の壁はさらに手前に来る。

**【文献要請】なし。** 本件は正典と repo 内実装で閉じている。

---

## 8. 審査者の限界(正直な申告)

- 実 artifact(385 MB 級)は取得していない。数値は v3/v4/v5 CV-9 判読(工房正本)・裁定 snapshot・repo 作業ツリーの `search/d972_r07_fixed_lambda_cycle_batch_v5.py` から取った。
- §4 の外挿は**線形外挿であり法則ではない**(裁定 2225 (2) の射程制限を継承)。ただし Θ(k·R) は回帰ではなく**コードのデータ構造から確定**する(`physical_factors` / `ordered_reductions` の長さが `rank` に等しいという明示要求)。
- §4.2 の「基点 15 role ≤ 26.1 s」は、v2/v3 が n=0 でモデル `26.1 + 1.271k` に残差 ≤ 2.8 s で乗ることからの推論である。v1 の親 role 数が記録されていない(v5 §7.1 の「—」)ため、**15 role の限界費用そのものを測ったわけではない**。
- 補題 1–3 と sr の非準同型性・rolling の順序感受性は N=64 の縮小モデルで検算した(seed 20260908)。実 N=48,384 では走らせていない(構造は N に依らない)。
- Astra 側の主張(R1–R4)は原文のまま「Astra 側の主張」として扱い、実 bundle の成立とは区別した。**本審査時点で実統合 bundle・変換器・公開 ABI は存在しない。**
- `verified = false`。本審査は Lean 形式化ではない。二系統一致でもない(単独審査)。

---

## 付録. 参照した pin(bytes のみ)

- 審査対象 `sol/luna_task_1111_r07_parent_rotation_equivalence_independent_review.md` 12,428 B
- 正本 `docs/notes/fixed_lambda_batch_v5_cv9_reading_v1.md` 64,510 B / `..._v4_...` 56,007 B / `..._v3_...` 51,374 B
- `sol/luna_reply_1106_r07_next_batch1834_public_contract_plan.md` 9,270 B
- 裁定 snapshot: 2223 = 2,947 B / 2224 = 368 B / 2225 = 2,809 B / 2226 = 2,034 B
- express `ops/express/20260908_astra_2225_rotation_equivalence_plan_ready_for_independent_review.md` 1,747 B
- producer `search/d972_r07_fixed_lambda_cycle_batch_v5.py` 366,659 B(参照行: `:42` ROLES / `:404-410` inventory 登録 / `:521-533` inventory / `:1754-1786` v3 層再認証 / `:2043-2067` 祖先累積 / `:2056-2057` 10-key / `:2070-2073` previous target / `:2326-2358` v4 層再認証 / `:2750-2790` acceptance / `:2947-2952` parent-row 記述子 / `:3371-3382` physical_factors / `:3403` ordered_reductions / `:3520-3524` row_source・target_parent / `:3954` 語規約)
- 基点 15 role の登録 artifact ZIP 総量 1,669,392,893 B(内訳: state 107,195,261 / delta 915,410 / seed34 984,053 / packet 1,855,391 / refinement 51,943,596 / oracle 2,299,772 / e 2,816,692 / prepare 204,360,988 / block-0..3 = 81,729,645 + 82,259,824 + 82,200,189 + 82,266,526 / p1 641,518,300 / task712 22,404,961 / continuation 304,642,285)
- batch-parent 369,233,546 B(展開 1,267,599,138 B / 11,437 file)・batch-parent-v4 377,383,320 B(展開 1,308,094,050 B / 11,648 file)
- 検算スクリプト(scratchpad・審査者作成)1 本


---

**裁定 2227(司令塔・2026-09-08)採択**: 本審査(原本 `scratchpad/math_rotation_equivalence_review_v1.md` 51,555 B・sha256 0d39b9c5b388b657f2e42b982ad1761600b941b65dd2da9f322f0261029dbd20・工房 sha256sum で pin)を工房の正本として採用。判定 = 数学としては条件付き受理可・設計としては受理不可(1111 原案は「回転」でなく「統合」で証拠量は線形に増える)。核心 = producer の per-run 仕事は Θ(k·R)(P5 :3371-3381/:3403 の physical_factors/ordered_reductions が rank 個)で、統合しても回転しても過去層の消去記録を毎 run 再解析する設計では塔を登れない → **裁定 2224 の「回転すれば k_max ≈ 425 で約 110 run」は撤回**。登坂手段 = 過去証拠を pin だけの冷保存に替える方式(1111 が別スコープとした R4)を本線設計へ。次 run の残差 1 数値では 3 モデル(層/byte/k·R)が 4 % 以内に密集し分離しない → admitted-parent の progress に経過秒を足す計器(GHA 費用 0)を先に入れる。
