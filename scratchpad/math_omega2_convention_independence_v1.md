# ω=2 の 5 行 — 規約非依存性の判定(数学者・限定発注 v1)

判定者: 工房数学者(Opus 5)。判定日 2026-09-06。
対象: producer run 33984832010/1 + checker v2 completion 33988391926/1 の rank 1386 → 1418 の 32 行、
      うち ω(w)=2 の 5 行(step 2, 6, 21, 22, 28)。
入力: falsifier CV-9 `scratchpad/fal_cv9_cegar_cont_v1_report_v1.md` §6.1(F-co-1)、裁定 2143 F-cy-3 / 2144。
正典: v542 / v545 / v547 / v548 §5、および実装 2 系統の生コード。

---

## 0. 結論(先出し)

### **三値判定 = 規約非依存(CONVENTION-INDEPENDENT)。5 行は両読みで同一の物理行を与える。rank 1418 の受理は本件を理由に妨げられない。**

三段の根拠、いずれも独立:

1. **[r_x,r_y]³ ∈ Ω** — GAP で直接確認。Δ(位数 357,128,352)の中で Θ([r_x,r_y]) の位数は **ちょうど 3**。
   よって v548 §5 の読み `comm^{2}` と v547 (4.2) の読み `comm^{-1}` が生む二つの語は、
   **どちらも Ω ∩ [F,F] に属する正当な語**であり、その差 comm³ 自身も Ω の元。
2. **差 comm³ の Q2 Fox 導分は消える** — しかも「P1 減算で消える」のではなく **P1 減算に到達する前に消えている**。
   [r_x,r_y] ∈ Φ₃(N₀) ⊆ ker J_{Q0} ⊆ ker J_{Q2}(v547 §4 の証明・v542 (1.4))であり、
   実装も producer/checker 両方が実行時に `chain([r_x,r_y]) ≡ 0` を要求して通している。
   加えて仮に非零でも 3 倍は mod 3 で消える(二重の安全)。
3. **物理行は語ではなく (chain, η) の関数** — 実装の全経路を追跡した結果、
   `chain` は witness から独立に再構成される `wanted_chain` に**ゲートで釘付け**されており、
   η も ε(comm^e)=(0,0) ゆえ不変。したがって source → P1 減算 → lower-zero → G(v) → 正規化行 は**バイト同一**。

**ただし一点だけ限定を付す(§3.1)**: 物理行はバイト同一だが、`raw-word.json` の受領証(語長・word_stream sha)は
両読みで異なるため、**候補 artifact の sha と instruction rolling head は一致しない**。
「同じ物理行」は数学的主張として正しく、「同じ受領証」ではない。また現行実装の語長上界は signed 前提で書かれており、
unsigned 語(長さ 2 倍)は上界式もろとも書き換えない限り通らない(= 実装は signed に構造的に固定されている)。

---

## 1. 問 1: [r_x,r_y]³ は Ω に入るか — **YES(計算で確定)**

### 1.1 紙の側の根拠(二系統)

- **v547 (1.1)**: `|Gamma0'|=3`。a=Θ(r_x), b=Θ(r_y) は共に Γ₀ の元(v547 (1.2) が r_x,r_y ∈ N₀ を与える)なので
  [a,b] ∈ Γ₀'、ゆえに [a,b]³ = 1。Ω = ker Θ だから **[r_x,r_y]³ ∈ Ω**。
- **v542 §3 (3.2)-(3.3)**: Γ₂' は位数 3 かつ中心的、そして原文どおり
  「For any a,b in Gamma2, `[a^3,b] = [a,b]^3 = 1`」。v545 §1 が Γ₀ ≤ Γ₂ を与えるので a,b ∈ Γ₀ にも適用できる。
- **v545 §3 (3.1)-(3.2)**: Φ(Γ₀) = <a³> × <b³> × <[a,b]> = C₃³。[a,b] は位数 3 の直和因子。

### 1.2 GAP による直接確認(新規計算)

スクリプト `scratchpad/math_omega2_comm_cube_v1.g`(`gap.ps1` 経由・-o 2g・runtime 32 ms)。
`scratchpad/a0_v2_prelude.g` の実物 Δ = DeltaJ と Θ = JointImg、`scratchpad/a0_v2_qraw.g` の 19 語 raw Q0 relator を使い、
v459 (2.1) / v547 (1.2) のとおり r_x = q1·q6⁻²·q7⁴·q9、r_y = q8⁻¹·q4⁻¹ を Δ で評価した:

```text
OM2 delta_order 357128352 gamma_order 243
OM2 a_in_Gamma0 true b_in_Gamma0 true
OM2 a_is_one false b_is_one false a_order 9 b_order 9
OM2 Gamma0_derived_order 3 comm_in_Gamma0_derived true
OM2 comm_is_one false comm_order 3
OM2 COMM_CUBE_IS_ONE true   (TRUE <=> [r_x,r_y]^3 in Omega)
OM2 comm_inv_eq_comm_sq true   (the two readings have the SAME Delta-endpoint)
OM2 Frattini_order 27 ab_generate_Gamma0 true
OM2 comm_central_in_Gamma0 true
```

副産物として v547 の未検算だった主張も同時に確認できた:
|Γ₀|=243・|Γ₀'|=3・|Φ(Γ₀)|=27・a,b の位数 9(= Exp(Γ₀)=9 と整合)・**<a,b> = Γ₀**(v547 §2 の
「a,b generate Gamma0」)・[a,b] は Γ₀ で中心的(v545 (3.1))・[a,b] ≠ 1(v547 (3.7) が主張する
E3 射影の Γ₀' 上の忠実性と整合)。

### 1.3 帰結

R_signed = w·(r_x³)^{-A/6}·(r_y³)^{-B/6}·comm^{-1}、R_unsigned = 同·comm^{+2} と置くと

```text
R_unsigned = R_signed · comm^3,     comm^3 in Omega,
eps(R_unsigned) = eps(R_signed) + 3*eps(comm) = eps(R_signed)   (eps(comm)=(0,0))
```

ゆえに **両読みとも Ω ∩ [F,F] の正当な語**。v547 Thm 4.1 の証明自体、中心座標条件を
`omega(w)+2g=0` としか要求していない(v547 §4)ので、ω=2 では g=−1 も g=2 も証明を通る。
**signed 代表の採用は語長最適化であって数学的必然ではない** — これが F-cy-3 の齟齬の本質。

---

## 2. 問 2: 物理行は Ω を法とする類にしか依存しないか — **依存しない(もっと強い形で)**

依頼文は「Ω の元の Fox 導分が P1 減算で消える根拠」を求めているが、実装の実際の機構は**それより一段手前**である。
以下、checker(`search/check_d972_r07_selected_cycle_materializer_v1.py`)の実経路を追跡した結果。producer
(`search/d972_r07_selected_cycle_materializer_v1.py`)も同型。

### 2.1 物理行の依存関係(全経路)

```text
witness (cycles, eta, scalar)
  → slp(語)                                        ← ここだけが規約に依存する
  → chain = slp.chain("raw-root")                    :781
      require(chain == wanted_chain % 3)             :784  "raw_repair_preserves_same_chain"
  → tagged = tag_chain_from_raw(geometry, chain)     :790   ← chain のみの関数
  → source = ordinary_source(geometry, tagged, eta)  :793   ← (chain, eta) のみの関数
  → primal = actual_primal(source, basis)            :1196  ← P1 減算(source の関数)
  → corrected = p1_corrected_source(source, basis, primal, index)  :1198  ← lower-zero 補正源
  → physical_raw = sum_a grouped_forward(tables[a], corrected[2][a]) mod 3   :1201-1202  ← G(v)
  → one_physical_row(physical_raw, ...)              :1211 / 定義 :1020
```

**語(SLP)は `chain` を作った後、物理行の経路には一切入らない。** 全 grep で確認した唯一の例外は
`raw["slp"].values["raw-root"]["exponent"]`(checker :1046 / producer :760)だが、これは (A,B) 指数対のみで、
ε(comm^e)=(0,0) ゆえ両読みで同一。`length` を読むのは telemetry(:1245)と語長ゲート(:800)と受領証だけである。

### 2.2 `chain` が規約非依存であること(三重の根拠)

**(i) ゲートによる釘付け。** `wanted_chain`(checker :762-776 / producer `witness_chain` :371)は
witness の 6 本の chord と固定スパニング木だけから組み立てられ、修理因子を一切参照しない。
:784 の `raw_repair_preserves_same_chain` がこれとの一致を要求する。producer 側も :440
`raw_root_same_witness_chain`。したがって **受理された行の chain は定義により witness の関数**。

**(ii) 実行時検証。** checker :782-783 は "r-x-cube", "r-y-cube", **"commutator"** の三つについて

```python
normalizer_chain, normalizer_endpoint = slp.chain(name)
require(normalizer_endpoint == 0 and not np.any(normalizer_chain), "repair_factor_actual_Q2_Fox_zero")
```

すなわち **chain([r_x,r_y]) = 0 かつ Q2 終点 = 単位**を毎 step 要求している(producer :434-437 も同じ)。
Fox 連鎖の積規則(`RawSLP.chain` の `product_pair`: chain(uv) = chain(u) + u·chain(v))から
chain(comm^e) = e·chain(comm) = 0(任意の整数 e)。raw-root は N₂ の元(:449 で q2=0 を要求)なので
chain(R·comm³) = chain(R) + chain(comm³) = chain(R)。

**(iii) 規約に依らない mod 3 の理由。** 仮に chain(comm) ≠ 0 でも、差は 3·chain(comm) ≡ 0 (mod 3)。
すなわち **(ii) が仮に落ちても結論は変わらない**。

**紙の側の対応する根拠**: [r_x,r_y] ∈ [N₀,N₀] ⊆ Φ₃(N₀)。v542 §1 が Z_Q = N/Φ₃(N) を与えるので J_Q は Φ₃(N) を殺し、
v547 §4 の Thm 4.1 証明が「every appended factor is in Phi(N0)=N0^3[N0,N0]. Its mod-three Fox row vanishes at Q0,
and hence at each quotient Q of Q0」と明記している。Q2 は Q0 の商(v542 §1 の塔 F→Δ→Q0→Q2)。

### 2.3 η が規約非依存であること

`expected = [18*eta_i]` と `require(root["exponent"] == expected)`(checker :447-449)。
ε(comm^e) = e·ε(comm) = (0,0)(交換子の通常指数和は零)なので ε(raw-root) は両読みで同一。
chord witness では producer :443-445 が (a0,b0) = (0,0) すなわち η = [0,0] を強制する。

### 2.4 六本の tag 連鎖(`direct_slp_tag_chains`)も同一

物理行の値は `tagged`(chain の線形関数)から作られるので 2.2/2.3 で決着だが、
`all_six_actual_direct_SLP_Fox_chains`(:792)という**語レベルの整合ゲート**も unsigned 語で通る:

tag 置換 σ_tag は Q2 へ降りる(`search/d972_r07_section_cochain_oracle_v1.py`:360 `phi[tag, 0] = 0`、
:366 `tag_map_bijection`、:367-369 `tag_map_all_positive_edges` が σ_tag の同変性 φ(v·g)=φ(v)·σ(g) を全辺で検証)。
特に **φ_tag(単位) = 単位**。comm ∈ N₂ なので σ(comm) の Q2 終点も単位、よって
chain_σ(comm^e) = e·chain_σ(comm)、差は 3·chain_σ(comm) ≡ 0 (mod 3)。

### 2.5 SLP 統計の直接検算(Python・独立実装)

実データ `scratchpad/a0_v2_words.json`(106,133 bytes・sha256 先頭 `fb191e30d269b539` = 実装の pin と一致)から
r_x, r_y を実装と同じ手順で組み、v547 (3.1)-(3.3) を独立に再実装して字面の語でも規則でも計算した:

```text
len(r_x) = 1058, len(r_y) = 466            (実装の NORMALIZER_ATOMS と一致)
eps(r_x) = (2,0), eps(r_y) = (0,2)          (v547 (1.2) と一致)
comm = [r_x,r_y]: (A,B,omega) = (0,0,2), 長さ 3046
   → v547 (3.6)(3.7) の omega([r_x,r_y]) = 2 を字面の 3046 文字語で確認
comm^{-1}: (A,B,omega) = (0,0,1),  長さ 3046
comm^{+2}: (A,B,omega) = (0,0,1),  長さ 6092
comm^{ 3}: (A,B,omega) = (0,0,0)   (= 単位元の統計)
```

**すなわち raw-root の SLP 値は、両読みで `exponent`・`omega`・`q0`・`q2` がすべて同一で、
異なるのは `length` だけ**(raw-root の SLP 長で 3046 の差。差の語 comm³ 自体は 9138 文字だが、
comm^{-1}·comm³ は自由簡約で comm² に落ちる)。`combine_statistics`(:274)の
ω(uv)=ω(u)+ω(v)+B(u)A(v) で A(comm^e)=0 だから、raw-root の ω も両読みで一致する
(これが falsifier の「2 + 2e ≡ 0 は e=−1 も e=2 も満たす」の代数的中身)。

---

## 3. 問 3: 三値判定

| 判定 | 内容 |
|---|---|
| **規約非依存** ✅ | **採用。** ω=2 の 5 行(step 2, 6, 21, 22, 28)は、v547 signed 読みと v548 §5 unsigned 読みで **同一の物理行**を与える。両読みの語はいずれも Ω ∩ [F,F] の正当な元で、差 comm³ ∈ Ω は Q2 Fox 導分に何も寄与しない。**rank 1418 の受理を本件が妨げることはない。** |
| 規約依存 | 否。行の値は語ではなく (chain, η) の関数で、両者とも witness に釘付けされている。 |
| 判定不能 | 否。必要な finite premise(|Γ₀'|=3・Θ([r_x,r_y]) の位数)は本便で GAP により実測した。 |

### 3.1 それでも規約は 1 つに固定すべき(格付け文面への要請)

判定は「非依存」だが、**規約の一本化は依然必要**である。理由は数学ではなく受領証:

- 両読みは**異なる語**を生み(長さ 3046 対 6092 の因子)、`raw-word.json` の `word_stream.sha256`・
  `word_bound`・`node_values[].length` が変わる。ゆえに `raw_word_sha256` → step の instruction →
  rolling head が変わる。**「同じ物理行」であって「同じ artifact」ではない。**
- 現行実装の語長上界(checker :796-798 / producer :466-468)は `2*|sr(omega)|*(1058+466) = 3048` で、
  実測 `actual_slp_length == normalized` の等号成立。unsigned 語(6092)は上界式も同時に
  `2*omega*(...)` へ書き換えない限り**ゲートで落ちる**。すなわち実装は signed に構造的に固定されている。
  falsifier の「語長 gate は規約の外部検証にならない(自己整合の対)」は正しい。

**推奨**: 裁定 2144(signed 採用)を維持し、**v548 §5 の `[r_x,r_y]^{omega(w)}` を erratum で
`[r_x,r_y]^{sr(omega(w))}` へ訂正**する(v547 (4.2) が正本)。実装変更は不要。
本便の結論は「訂正前に走った 5 行を破棄・再走する必要はない」ことを保証する。

---

## 4. 検算資産

| ファイル | 内容 |
|---|---|
| `C:\Users\81905\Desktop\shadow-atelier\scratchpad\math_omega2_comm_cube_v1.g` | GAP 検算(Δ 内で Order([a,b])=3・[a,b]³=1・a,b∈Γ₀・<a,b>=Γ₀・\|Γ₀'\|=3・\|Φ(Γ₀)\|=27)。`gap.ps1` 経由・runtime 32 ms |
| (一時) omega_check.py | v547 (3.1)-(3.3) の独立再実装。実データ `a0_v2_words.json` から r_x,r_y を再構成し ε・ω・語長を字面と規則の両方で算出 |

再現手順: `.\gap.ps1 scratchpad\math_omega2_comm_cube_v1.g`

---

## 5. 限定(正直な申告)

1. **|Γ₀'|=3 等は前提ではなく本便で実測した**が、その土台である `scratchpad/a0_v2_prelude.g` の Δ 構成
   (Δ の位数 357,128,352・Γ の位数 243)は既登録資産をそのまま使っており、本便で再監査していない。
   ただし `a0_v2_gamma_output.txt` 冒頭 2 行と本便の出力は独立に一致する。
2. **物理行の (chain, η) 依存性は、実装 2 系統の当該呼び出し経路を読んで確定した**。
   下流ヘルパ(`REFINE.source_lift`・`grouped_forward`・`LEGACY.*`)の内部は読んでいないが、
   これらは配列/ストリームのみを引数に取り、語も SLP も受け取らない(grep で全数確認)。
3. **本便は rank 1418 の他の側面(oracle の正当性・separator・P1 台帳)を一切監査していない。**
   判定範囲は「ω=2 の 5 行が規約選択に依存するか」のみ。
4. `cross-checked` / `verified` の格付けは変えない。本件は **paper proof + GAP 実測 + 実装読解**であって
   Lean 検証ではない。`verified=false`。

## 6. Sol / 司令塔への申し送り

- 【要 erratum】v548 §5 の `[r_x,r_y]^{omega(w)}` は v547 (4.2) の `[r_x,r_y]^{sr(omega(w))}` に合わせて訂正。
  数学的にはどちらも正しい(本便が証明)が、**受領証が分岐する**ので正本を一本にすること。
- 【提案】v547 §4 に一行足すと同種の齟齬が二度と起きない:
  「中心座標条件は omega(w)+2g ≡ 0 (mod 3) のみを要求し、g の Z への持ち上げ方は
  [r_x,r_y]³ ∈ Ω(|Γ₀'|=3)ゆえ Ω 語の類を変えない。signed 代表は語長最短の選択である。」
- 【新規事実】v547 §2 の「a,b generate Gamma0」と (2.3) の Φ(Γ₀)=C₃³、および (3.7) の
  [a,b]≠1 は、いずれも本便で Δ の中で実測確認された(それまでは紙の議論のみ)。

---

判読ファイル: `C:\Users\81905\Desktop\shadow-atelier\scratchpad\math_omega2_convention_independence_v1.md`

sha256(this file, excluding this line) = 335fd91243b8de2b
