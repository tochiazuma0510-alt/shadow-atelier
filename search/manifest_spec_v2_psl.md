本書は manifest v2_psl の spec 射影(sealed 除去済み)。PSL 実装はこのファイルだけを正とする。

---

# Week 3 manifest 追補 v2 — **PSL 七窓(case A/B)の実装宇宙**(spec 射影)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 07 の任務 2**。
本書は `docs/week3-manifest_v1.md`(七段 25200 点バッテリー)の**追補**であり、置換ではない。v1 の §1(全体規則)・§3(fixture)・§4(reduction)の規律は**そのまま継承**し、本書は **PSL 七窓 = 十 Aut 軌道**の宇宙を追加する。

- **数学的正本**: `docs/week3-PSL封印計算_opus_v1.md`(定理 M1/M2/M3・補題 N)+ `docs/命題_caseB_settled障害_v1.md`(定理 B)+ `docs/week3-狩場計画_v4.md`。本書と食い違ったらこれらが上位。
- **監査根拠**: `sol/sol_reply_09_audit_psl.md`(F11–F19・P113–P117・W78–W82)・`sol/裁定_09_psl.md`・`sol/sol_reply_10_caseB.md`(F1–F19・P118–P125・W83–W90)。
- **反映した提案**: **P114**(実装証明書の必須欄)・**P115**(独立データ源)・**P117**(outer-sign 宇宙の別 target ID)・**W78**(raw と生成の分離)・**W79**(ラベル非依存)・**W81**(状態札)・v1 §6 の P-A/P-B/P-C。
 便 10 から追加: **P121**(rigidity schema の 4 欄分離)・**P125**(case B 実装証明書の積類欄)・**W83**(divisibility trap)・**W84**(square-root class を別欄)・**W86**(`fiber_rigid` と `isolated` を同義にしない)・**W90**(状態語)。
- **状態札**: **紙上相互監査**(case A 4 窓は Sol 便 09 と**独立収束**)。**cross-checked でも verified でもない**。genuine は一切主張しない(W28)。

---

## 0. 開示規律(**実装ブラインド性の保護**)

v1 §0 と同じ二層。**implementer へ渡すのは `spec` 射影だけ**。

| disclosure | 内容 | 実装担当へ |
|---|---|---|
| **`spec`** | 対象定義・明示 marking $(S,T)$・宇宙数値(index / ord / charming set / derived / candidate_total / Aut 軌道数)・inner/outer 区分・evaluation mode・schema・cap・停止規則・**fixture(PU-F*)** | **渡す** |
| **`sealed`** | `gt_count`・per-$m$ staged count・`n_m`・`class_coefficient` の期待値・`settled_m` / `settled_count`・`isolated`・`phi_image`・`normalizer_order` | **渡さない** |

> **封印の状態(2026-07-26)**: 七窓の sealed 値は **封印 `PSL_v1` として実施済み**(nonce + canonical JSON の SHA-256)。**ハッシュは `provenance/LEDGER.md`**、byte 列は金庫。本書の sealed 欄には**値を書かない** — 「**封印済み(PSL_v1)**」とだけ記す。開封は結果が出てから byte 列で行う(再 canonicalize しない)。
> **canonicalization**: `gtsh-canon/v1`(v1 §0 と同一)。

---

## 1. 全体規則(v1 §1 からの差分のみ)

### 1.1 cap(P83・従来様式)

```json
{ "cap": {
    "per_stage_wall_seconds": 600,
    "aggregate_wall_seconds": 1800,
    "max_rss_bytes": 2147483648,
    "gap_options": "-o 2g",
    "forbidden_constructions": ["full_cayley_table_squared"],
    "required_data_structures": ["BFS", "Int32Array"],
    "on_stage_timeout": "stage_result = UNKNOWN; halt",
    "on_aggregate_timeout": "all_remaining_stages = UNKNOWN; halt" } }
```
- **W58 厳守**: 各窓 600 秒以内でも**集約 1800 秒を超えた時点で残りを UNKNOWN に倒す**。
- 本追補の 7 窓合計 B₃ 点数は **19944**(v1 バッテリー 25200 の 0.79 倍)で、最大の群でも $|\hat G| \le 1512$。**二乗 Cayley 表は依然禁止**(不要)。
- **settled 判定**は $\mathrm{Aut}(\hat G)$($\le 1512$ 元)の総当たりで足りる。**部分群探索や自己同型群の構成関数に頼らないこと**(GAP の `AutomorphismGroup` は使わず、明示的な共役元/Frobenius の直積で構成する — §4.2)。

### 1.2 停止規則(P84・v1 §1.2 と同一)

fixture が 1 つでも外れたら**即停止**・次窓へ進まない・後段の既知値で補正しない・`stop_reason`/`stage`/`fixture_id`/`observed`/`expected` を残す・cap 超過の事後免除なし。

### 1.3 語彙(G-04 / W54 / **W78**)

| 出力名 | 意味 | 自動出力 |
|---|---|---|
| `class_coefficient` | **生成条件を課さない**類積係数 $N_{\hat G}(w^u) = \#\{(r,g)\in T_3\times T_2 : rg = w^u\}$ | **可** |
| `generation_pass_count` | そのうち $\langle X^u, f^{-1}Y^uf\rangle = G$ を通る数(G-05: boolean 禁止・整数) | **可** |
| `frobenius_zero` | `class_coefficient = 0` の $m$ | **可** |
| `m_missing` | `generation_pass_count = 0` の $m$ | **可** |
| `fake_witness` | 粗い $K$ の shadow が細分へ持ち上がらない | **不可**(F11 の 4 項が揃った別証明書に限る) |

> **W78(厳守)**: `class_coefficient` と `generation_pass_count` は**別欄**であり、**片方をもう片方から推測して書いてはならない**。両者が食い違う実例が control(§3 PU-F12)である。

### 1.4 語規約(**必記** — `docs/定義ノート追記案_語規約_v2.md`)

規約 W-1〜W-4 に従うこと。とくに:
1. **paper 語 "AB" は GAP の `B*A`**($i^{B*A} = (i^B)^A$)。
2. **hexagon の判定式の積も paper 積**(W-4): $(t^{-1}Y^mf)^3$ は GAP では `(f * Y^m * t^-1)^3`。**(H-a) は向きに鈍感だが (H-b′) は敏感**なので、(H-a) が通ったことを根拠に規約を正しいと判断してはならない。
3. **適合テスト A5-CONV を列挙前に通す**(§3 PU-F11)。
4. 規約を変えたくなったら**変えずに司令塔へ差し戻す**。

### 1.5 certificate schema(`gtsh-cert/v2-psl` — v2 からの追加欄)

```text
gtsh-cert/v2-psl                     # v1 §1.4 の全欄を継承し、以下を追加
  ambient_group        "PSL(2,7)" | "PGL(2,7)" | "PSL(2,8)" | "PGammaL(2,8)" | ...   # spec: Ĝ
  case                 "A_split_inner" | "B_outer"                                   # spec (P-C)
  object_count         <int>          # spec: 同じ (G,k) をもつ対象 N の個数 = Aut 軌道数
  aut_orbit_index      <int>          # spec: 走らせた軌道の番号(1-origin)
  element_encoding     "pgl2q_matrix/v1"                                             # spec
  marking              { S, T, w, X, Y, w2, det_S, det_S_is_square, ord_S, ord_T,
                         ord_w, ord_X, s_is_inner }                                  # spec
  generation_checks    { gen_ambient: "<S,T> の位数", gen_derived: "<X,Y> の位数" }  # spec
  ambient_product_class  "<w の積類の非ラベル指紋: (ord, class_size, min_canonical_matrix)>"  # P125
  power_class_map      [ { m, u, u_mod_2k, w_pow_u_is_inner,                         # W79 / P125
                           powered_product_class: "<同じ指紋形式>",
                           same_class_as_base: true|false,      # = outer_product_class_preserved (W84)
                           conjugator: "<matrix>"|null,         # same_class_as_base が真のときの明示共役元
                           x_power_reachable: true|false } ]     # W84: X^u が X と Aut(G)-共役か(別欄!)
  per_m                [ { m, u, ha_pass,                                            # W78 / P121
                           raw_structure_constant,              # = class_coefficient(別名・両方出してよい)
                           generation_pass_count,
                           global_conjugacy_orbits,             # 生成 factorization の同時共役軌道数
                           fixed_product_centralizer_orbits,    # C(v)-torsor の軌道数(fiber_rigid の指標)
                           n_m } ]
  hexagon_free_certificate { candidate_total, h10_fail, h11_fail,
                             generation_fail, shadow_total }                         # 排他的 (F16/W49)
  settled_detail       [ { m, f, settled: true|false,
                           automorphism_witness: "<matrix>"|null } ]                 # P114 / F19
  settled_count        <int>
  normalizer_order     <int>          # |N_{Aut(Ĝ)}(<w>)|(定理 B の照合値)
  isolated             true|false|UNKNOWN
```
- **F19 厳守**: `settled[m]` 形式は**禁止**。key は **exact な $(m,f)$**。
- **排他的 staged count(F16/W49)**: `shadow_total = candidate_total − h10_fail − h11_fail − generation_fail` が成り立たない証明書は不正。
- **W52**: 生成判定の正本は $\langle X^u, f^{-1}Y^uf\rangle = G$。系 T2-B の $\langle g,r\rangle = \hat G$ は参考値 `torsion_generation_agrees` に置く(命題 B・補題 B5 により両者は同値のはずだが、**実装は独立に両方出して一致を観測する**)。
- **W84(厳守・便 10)**: `x_power_reachable`($X^u$ が $X$ と $\mathrm{Aut}(G)$-共役か)と `same_class_as_base`($w^u$ が $w$ の積類に残るか)は**別欄**である。**$k=4$ と $k=6$ では前者が真で後者が偽になる** — `x_power_reachable` だけを証明書にしてはならない(P125)。
- **W86(厳守・便 10)**: `fiber_rigid`(固定積類内の torsor 性)と `isolated`(charming power map をまたぐ条件)を**同義にしない**。case B は「各繊維は rigid だが対象は非 isolated」という**両立**の実例である。

### 1.6 S₃ marking(G-02・v1 §1.5 と同一)

$\bar\Delta \mapsto (1\,2)$、$\bar\delta_B \mapsto (1\,2\,3)$、`equals_standard: false`、`simultaneous_conjugate_of_standard: true`、`conjugator: "(1 2 3)"`。

### 1.7 記号衛生

- $\hat G$(周囲群)と $G$(単純群 $=PB_3/N$)を混同しない。case A では $\hat G = G$、case B では $\hat G = \tilde A \supsetneq G$。
- $e := \mathrm{ord}(w)$ と $k := N_{\rm ord} = \mathrm{ord}(X)$ を混同しない。case A で $e=k$、case B で $e=2k$。
- $\mathrm{ord}_Q(\bar\sigma_1) = 2k$ は**両 case で共通**(系 T2-A′)。$e$ とは別物。

---

## 2. 七窓の宇宙(**spec**)

### 2.0 宇宙表(**列挙前に固定 — 後から変えない**)

| 段 | 群 $G$ | $q$ | case | $\hat G$ | $\lvert G\rvert$ | $\lvert\mathrm{Aut}(\hat G)\rvert$ | $e$ | $k=N_{\rm ord}$ | $\lvert\mathcal X\rvert$ | derived | candidate_total | $\lvert PB_3{:}N\rvert$ | **B₃ 点数** | **Aut 軌道数** |
|---|---|---:|:--:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **S1** | PSL(2,7) | 7 | **A** | PSL(2,7) | 168 | 336 | 7 | **7** | 6 | 168 | 1008 | 168 | **1008** | **1** |
| **S2** | PSL(2,7) | 7 | **B** | PGL(2,7) | 168 | 336 | 8 | **4** | 4 | 168 | 672 | 168 | **1008** | **2** |
| **S3** | PSL(2,8) | 8 | **A** | PSL(2,8) | 504 | 1512 | 7 | **7** | 6 | 504 | 3024 | 504 | **3024** | **1** |
| **S4** | PSL(2,8) | 8 | **A** | PSL(2,8) | 504 | 1512 | 9 | **9**(3\|k) | 6 | 504 | 3024 | 504 | **3024** | **1** |
| **S5** | PSL(2,11) | 11 | **A** | PSL(2,11) | 660 | 1320 | 11 | **11** | 10 | 660 | 6600 | 660 | **3960** | **1** |
| **S6** | PSL(2,11) | 11 | **B** | PGL(2,11) | 660 | 1320 | 10 | **5** | 4 | 660 | 2640 | 660 | **3960** | **2** |
| **S7** | PSL(2,11) | 11 | **B** | PGL(2,11) | 660 | 1320 | 12 | **6**(3\|k) | 4 | 660 | 2640 | 660 | **3960** | **2** |

> **P114 の要求「探索前に総数を固定する」**:
> $$ \textbf{七型・十軌道}\qquad 1+2+1+1+1+2+2 \;=\; \boxed{10} $$
> **B₃ 点数合計(各型 1 軌道を走らせる場合)= 19944**。第二軌道まで全部走らせる場合は **+ 1008 + 3960 + 3960 = 28872**。
> **`object_count`(= その $(G,k)$ をもつ対象 $N$ の個数)= Aut 軌道数**。case B が 2 なのは PGL の位数 $e$ の 2 類($8A/8B$, $10A/10B$, $12A/12B$)が $\mathrm{Aut}(\tilde A) = \mathrm{Inn}(\tilde A)$ では融合しないため(v1 §2)。**同じ $(G,k)$ に複数の対象があるのは atlas 初**(P-C)。
> **charming set は $\mathcal X_N \to (\mathbb Z/2k)^\times$, $m\mapsto 2m+1$ が全単射**なので $|\mathcal X| = \varphi(2k)$(命題 B・系 B3-a)。実装はこれを fixture として検査する(PU-F9)。

### 2.1 共通の対象定義(全窓)

```json
{ "definition": "N = pi^{-1}( ker( q: F2 ->> G,  x |-> X,  y |-> Y ) )",
  "ambient": "B3", "quotient_P": "G", "quotient_Q": "Q = B3/N,  |Q| = 6|G|",
  "element_encoding": "pgl2q_matrix/v1",
  "encoding_note": "2x2 行列 [[a,b],[c,d]] を GF(q) 上で PGL(2,q)=GL/scalars の元として表す。正準形 = 最初の非零成分を 1 に正規化した行列。GF(8) は F_2[x]/(x^3+x+1)、元 a0+a1*x+a2*x^2 を整数 a0+2*a1+4*a2 で表す(0..7)",
  "marked_images": { "x": "X", "y": "Y", "c": "1" },
  "B3_marking": { "Delta_bar": "(S, (1 2))", "deltaB_bar": "(T, (1 2 3))" },
  "derivation": "w := T^{-1} S,  X := w^2,  Y := S X S^{-1} = T X T^{-1},  Z := T^2 X T^{-2},  w2 := S T^{-1}",
  "c_in_N": true,
  "evaluation_mode": "quotient_ok",
  "triangle_marking": { "applicable": true, "exact_order_binv_a": "2k" }
}
```
- **`c_in_N = true` の根拠**: 定理 M2 の構成で $\bar\Delta$ の両成分が対合ゆえ $c = \Delta^2 \mapsto 1$。したがって **A2 段で問題になった「$c\notin M$ の罠(語レベル評価必須)」は本追補の全窓で発生しない**(商内評価が正当)。ただし §1.4 の W-4(判定式の積の向き)は**依然効く**。
- **`case B` の $Q$ 構造**: `"Q_structure": "Aut2(G) x_{C2} S3"`。$\bar\Delta$ の $\hat G$-成分 $S$ は **outer**(det が非平方)。

### 2.2 各窓の明示 marking(**spec** — 封印 payload と同一の行列を用いる)

行列は $[[a,b],[c,d]]$、正準形($q$ 奇では det の平方剰余性が inner/outer を決める)。
**下表の $w, X, Y, w_2$ は $S,T$ からの導出値である**(実装は自分で導出し、この表と一致することを fixture PU-F2/F3 で検査する)。

| 段 | $S$($\bar\Delta$ の $\hat G$ 成分) | $T$($\bar\delta$ の $\hat G$ 成分) | $\det S$ | $S$ は inner? | $w=T^{-1}S$ | $X=w^2$ | $Y$ | $w_2=ST^{-1}$ |
|---|---|---|---:|:--:|---|---|---|---|
| **S1** | `[[2,1],[1,5]]` | `[[4,0],[2,2]]` | 2(平方) | **inner** | `[[1,4],[0,1]]` | `[[1,1],[0,1]]` | `[[0,1],[5,1]]` | `[[1,2],[3,3]]` |
| **S2** | `[[1,0],[0,6]]` | `[[1,1],[4,5]]` | 6(非平方) | **outer** | `[[1,3],[2,4]]` | `[[0,1],[3,1]]` | `[[0,1],[3,6]]` | `[[1,4],[5,4]]` |
| **S3** | `[[1,0],[1,1]]` | `[[4,2],[4,5]]` | 1 | **inner**($q$ 偶) | `[[1,3],[0,6]]` | `[[1,2],[0,2]]` | `[[1,7],[6,0]]` | `[[1,4],[2,7]]` |
| **S4** | `[[1,0],[1,1]]` | `[[4,3],[1,5]]` | 1 | **inner**($q$ 偶) | `[[1,5],[4,7]]` | `[[1,1],[3,6]]` | `[[0,1],[5,7]]` | `[[1,6],[3,5]]` |
| **S5** | `[[1,1],[1,10]]` | `[[9,1],[8,1]]` | 9(平方) | **inner** | `[[0,1],[6,8]]` | `[[1,5],[8,8]]` | `[[0,1],[8,1]]` | `[[1,2],[5,3]]` |
| **S6** | `[[1,0],[0,10]]` | `[[3,1],[9,7]]` | 10(非平方) | **outer** | `[[1,8],[5,9]]` | `[[1,10],[9,0]]` | `[[1,1],[2,0]]` | `[[1,3],[6,9]]` |
| **S7** | `[[1,0],[0,10]]` | `[[4,1],[1,6]]` | 10(非平方) | **outer** | `[[1,2],[9,3]]` | `[[1,1],[10,2]]` | `[[1,10],[1,2]]` | `[[1,9],[2,3]]` |

$T$ はすべて $\det T = 1$(平方)で **inner・位数 3**。$S$ はすべて位数 2。
**第二 Aut 軌道の構成法**(S2/S6/S7・実装手順として一意に決まる書き方):
1. $\hat G$ 内で「$\mathrm{ord}(S')=2$($q$ 奇の case B では $\det S'$ が非平方)、$\mathrm{ord}(T')=3$、$\mathrm{ord}(T'^{-1}S')=e$、$\langle S',T'\rangle=\hat G$」を満たす対 $(S',T')$ を**全列挙**する。
2. $\mathrm{Aut}(\hat G)$ の作用で軌道に分ける($Z(\hat G)=1$ かつ生成対ゆえ作用は**自由**なので、軌道数 $=$ 対の総数 $/\lvert\mathrm{Aut}(\hat G)\rvert$)。
3. §2.2 の $(S,T)$ を含む軌道を第一軌道とし、**もう一方の軌道から代表を 1 つ取る**(表 §2.0 の Aut 軌道数と一致することを検査 — これが `object_count` の実地検査)。
**実装は第二軌道を独立に走らせ、全数値が第一軌道と一致するか(クラスラベルの入れ替えを除いて)を観測する。**
> ⚠ 手順 1 の全列挙は $\lvert\hat G\rvert^2 \le 1320^2 \approx 1.7\times10^6$ 対の走査だが、$S'$ を対合クラスの代表 1 個に固定してよい($\mathrm{Aut}$ は対合クラス上推移的)ので **$\lvert\hat G\rvert$ 回の走査で足りる**。cap 内。

### 2.3 charming set(**spec**)

| 段 | $k$ | $\mathcal X_N = \{m\in\mathbb Z/k : \gcd(2m+1,k)=1\}$ | $\lvert\mathcal X\rvert = \varphi(2k)$ |
|---|---:|---|---:|
| S1 | 7 | $\{0,1,2,4,5,6\}$ | 6 |
| S2 | 4 | $\{0,1,2,3\}$(条件は空虚) | 4 |
| S3 | 7 | $\{0,1,2,4,5,6\}$ | 6 |
| S4 | 9 | $\{0,2,3,5,6,8\}$ | 6 |
| S5 | 11 | $\{0,1,2,3,4,6,7,8,9,10\}$ | 10 |
| S6 | 5 | $\{0,1,3,4\}$ | 4 |
| S7 | 6 | $\{0,2,3,5\}$ | 4 |

---

## 3. fixture 一覧(**spec** — 1 つでも外れたら列挙へ進まない)

| # | 内容 | 期待値 |
|---|---|---|
| **PU-F1** | 群の位数: $\lvert G\rvert$、$\lvert\hat G\rvert$、$\lvert\mathrm{Aut}(\hat G)\rvert$、$\lvert PB_3{:}N\rvert$、B₃ 点数 $=6\lvert G\rvert$ | §2.0 の表 |
| **PU-F2** | $\mathrm{ord}(S)=2$、$\mathrm{ord}(T)=3$、$\mathrm{ord}(w)=e$、$\mathrm{ord}(X)=k$ | §2.0/2.2 の表 |
| **PU-F3** | $XYZ=1$、$Y=TXT^{-1}=SXS^{-1}$、$Z=T^2XT^{-2}$、$w_2^2=Y$ | PASS |
| **PU-F4** | $\langle S,T\rangle = \hat G$(位数一致)かつ $\langle X,Y\rangle = G$(位数一致) | PASS |
| **PU-F5** | inner/outer 区分: $q$ 奇の窓で $\det S$ の平方剰余性が §2.2 と一致($q=8$ では PSL $=$ PGL ゆえ空虚) | §2.2 の表 |
| **PU-F6** | **exact order(G-01)**: $\mathrm{ord}_Q(\bar\delta_B^{-1}\bar\Delta) = 2k$ | S1/S3: 14、S2: 8、S4: 18、S5: 22、S6: 10、S7: 12 |
| **PU-F7** | **$c\in N$**: $\bar\Delta^2 = 1$ in $Q$($S^2=1$ かつ $(1\,2)^2=1$) | PASS |
| **PU-F8** | **S₃ marking(G-02)**: $\bar\Delta\mapsto(1\,2)$、$\bar\delta_B\mapsto(1\,2\,3)$、標準射との同時共役元が $(1\,2\,3)$ | PASS |
| **PU-F9** | charming set の元と $\lvert\mathcal X\rvert = \varphi(2k)$、および $m\mapsto 2m+1 \bmod 2k$ が $\mathcal X\to(\mathbb Z/2k)^\times$ の**全単射**であること | §2.3 の表 |
| **PU-F10** | `candidate_total` $= \lvert\mathcal X\rvert\cdot\lvert[P,P]\rvert = \lvert\mathcal X\rvert\cdot\lvert G\rvert$($G$ 完全ゆえ derived $=\lvert G\rvert$) | §2.0 の表 |
| **PU-F11** | **語規約適合テスト A5-CONV**(語規約 v2 §5): $\mathrm{ev}(yx^{-1}) = (1\,2\,4)$、A1 の 20 語で hexagon **20/20** | PASS |
| **PU-F12** | **W78 control(除外窓・答えを含まない)**: $\mathrm{PSL}(2,11)$ の **inner 位数 5** の元 $v$ について `class_coefficient` $=10$ かつ `generation_pass_count` $=0$($\Delta(2,3,5)=A_5$ ゆえ全分解が位数 60 の部分群に落ちる) | `10 → 0` |
| **PU-F13** | 群構成の自己検査: $\lvert\mathrm{PGL}(2,q)\rvert = q^3-q$、$\lvert\mathrm{PSL}(2,q)\rvert = (q^3-q)/\gcd(2,q-1)$、$\lvert\mathrm{P\Gamma L}(2,8)\rvert = 1512$ | PASS |
| **PU-F14** | $\lvert C_{\mathrm{Aut}(\hat G)}(w)\rvert$ を各窓で**独立計算し証明書へ出力**する | 出力欄の存在(値の事前指定なし)— **裁定済み 2026-07-26: 選択肢 (b) 採用**(U-F9/S-F9 と同型の処置) |

> **W83(divisibility trap・便 10)**: 「$2 \mid \lvert\mathrm{Out}(G)\rvert$ だから case B がある」と書いてはならない。**case B marking の存在は PU-F2(outer involution・$\mathrm{ord}(T)=3$)・PU-F4($(2,3,e)$-生成)・PU-F6(exact order)の 3 欄が独立に通ることで初めて証明される。** 3 欄を 1 つにまとめない。

---

## 4. checker 要件(**P115 / P117 / 二系統化**)

### 4.1 P115 — **二系統目のデータ源を独立にする**

> 便 09 の Sol 計算は **GAP の CTblLib 1.3.11 の生データ**(ATLAS 由来)を読んで紙で有限和を取ったものである。**GAP 実装が同じ CTblLib を再読するだけでは、データ源まで独立した二系統にならない**(Sol 自己申告)。
>
> ⇒ **checker 要件(厳守)**: 第二系統は次のいずれかを**データ源として**用いること。
> - **(a) 明示 $2\times2$ 行列からの直接列挙**(推奨): $\mathrm{GF}(q)$ を自前で構成し、$\mathrm{PGL}(2,q)$ を行列 mod scalars として作り、$T_2, T_3$ を直接列挙して $\#\{(r,g): rg=w^u\}$ を数える。**指標表を一切参照しない。**
> - **(b) ATLAS 印刷表**(紙のページ画像)から手入力した指標表 + 直交性の自己検証。
>
> **禁止**: 「GAP の `CharacterTable("L2(7)")` を読んで Frobenius 和を計算する」だけの実装を第二系統と呼ぶこと。それは Sol の計算の**再実行**であって独立ではない。
> **追加の巨大探索器は不要**(Sol P115)。(a) は $\lvert\hat G\rvert\le1512$ の総当たりで足りる。

### 4.2 P117 — **outer-sign 宇宙は別 target ID・PGL 表**

- case B(S2/S6/S7)は **`target_id` を case A と別に事前登録**する(`case: "B_outer"`・`ambient_group: "PGL(2,q)"`)。
- **case B の類積は $\hat G = \mathrm{PGL}(2,q)$ の指定 coset で取る**。$\mathrm{PSL}$ の ordinary 表を流用してはならない(Sol F6/F12/W82)。
- 実装上は §4.1(a) の直接列挙で自動的に満たされる(周囲群を $\mathrm{PGL}$ に取るだけ)。
- $\mathrm{Aut}(\mathrm{PSL}(2,8)) = \mathrm{P\Gamma L}(2,8)$ は $(h,i): m\mapsto \mathrm{Frob}^i(hmh^{-1})$($\mathrm{Frob}: x\mapsto x^2$)として明示構成する。**`AutomorphismGroup` に頼らない。**

### 4.3 W79 — ラベル非依存

- $7A/7B/7C$、$9A/9B/9C$、$11A/11B$、$8A/8B$、$10A/10B$、$12A/12B$ は **CTblLib の正規化ラベル**であり、実装は**ラベルを使わない**。
- 証明書に残すのは **power map と coset**:
 各 $m$ について `u`、`u_mod_2k`、`w_pow_u_is_inner`(= $w^u \in G$ か)、`conj_to_w_in_aut`(= $\exists\alpha\in\mathrm{Aut}(\hat G),\ \alpha(w)=w^u$)と、真なら**明示 conjugator**。
- 併せて `x_pow_u_conj_to_x`(= $X^u$ が $X$ と $\mathrm{Aut}(G)$-共役か)も出す。**この 2 欄が食い違う窓があること自体が命題 B の核心**である(v1 §8 の対照表)。

### 4.4 分離の原則(v1 §1 の継承)

**探索器**(GAP: 候補列挙 + 簡約 hexagon)と**照合器**(node/python: 証明書だけを入力に $B_3/N$ 上の (3.3)(3.4) を再計算)を **helper 非共有**で分離する。settled 判定は照合器側でも独立に行う。

---

## 5. 実装順の推薦(**P-A / P-B**)

> **一括封印しない**。開封は段階的に行い、各段で情報を最大化する。

| 順 | 段 | B₃ 点数 | 目的 | 判定の意味 |
|---:|---|---:|---|---|
| **1** | **S1**(PSL(2,7) case A) | **1008** | **最軽量・命題 S の成否がここで決まる** | 通れば命題 S の射程 = split-inner が 1 点で確認。外れれば以降を止めて原因究明 |
| 2 | **S2**(PSL(2,7) case B) | 1008 | **非 isolated の初検証**(定理 B の較正) | settled が繊維単位の二択($0$ か $e$)になっているかを見る。$\mathrm{Aut}(\hat G)=336$ 元の総当たりで足りる |
| 3 | S3(PSL(2,8) A, k=7) | 3024 | $\mathrm{P\Gamma L}$ 実装の較正 | 体自己同型込みの $\mathrm{Aut}$ が正しく効くか |
| 4 | S4(PSL(2,8) A, k=9) | 3024 | **$3\mid k$・$k$ 合成数**の初点 | W80(charming なら $\gcd(u,2k)=1$ で位数が落ちない)の実地確認 |
| 5 | S5(PSL(2,11) A) | 3960 | 最大 $\lvert\mathcal X\rvert$ | Hol$(\mathbb Z/11)$ |
| 6 | S6(PSL(2,11) B, k=5) | 3960 | case B 二点目 | $X$ 側にも障害がある唯一の case B 窓(v1 §8) |
| 7 | S7(PSL(2,11) B, k=6) | 3960 | **$3\mid k$ かつ outer** | 「$3\mid k$ は命題 S の成否に無関係」の確認 |
| (任意) | S2′/S6′/S7′(第二 Aut 軌道) | +8928 | `object_count = 2` の実地検査 | 全数値が A/B 入れ替えを除いて一致するか |

**S1 単独で止めてよい設計にすること**(段ごとに certificate を確定して封印を開ける)。

---

## 6. errata(**P111 / P112** — 既存本文の修正)

> 対象: `docs/week3-20の正体_opus_v1.md` の**補題 3**(P111)と **§4.3 定理 48 / 命題 C′**(P112)。原本は versioned 規律により書き換えず、**本節を正誤表とする**(次版 v2 起草時に本文へ統合)。

### 6.1 【P111】補題 3(scalar 化)の証明の書き換えと射程の縮小

**誤っていた記述**(補題 3 の証明・後半):
> 「$C = \bar\Delta A = P\times\{\sigma\}$ ゆえ $z_{2,C} = z_2(P)\otimes\sigma$ となって $z_2(P)$ は中心元。ゆえに $\rho_\chi(z_{2,C})$ が**スカラー**になり…」

**訂正(便 09 F6)**: $Q = P\times S_3$、$C = P\times\{\sigma\}$ のとき確かに $z_{2,C} = z_2(P)\otimes\sigma$ だが、既約表現 $\chi\otimes\psi \in \mathrm{Irr}(Q)$ 上では
$$ \rho_{\chi\otimes\psi}(z_{2,C}) \;=\; \frac{S_2^P(\chi)}{\chi(1)}\,I_\chi\ \otimes\ \rho_\psi(\sigma) $$
であり、**$S_3$ の 2 次元既約表現では $\rho_\psi(\sigma)$ はスカラーではない**。⇒ **「$z_{2,C}$ が既約表現上スカラー」は偽**。

**正しい閉じ方(二通り・どちらでも同じ結論)**:
1. **直接全単射**(推奨・補題 3 の前半そのもの): $g := sf$、$r := w^ug$ と置くと (H-a) $\wedge$ (H-b′) $\iff r^3 = g^2 = 1 \wedge rg = w^u$。ゆえに $n_m = \#\{(r,g)\in T_3(P)\times T_2(P) : rg = w^u\}$ が**表現論を経由せず**得られ、これに古典 Frobenius の scalar 類積公式を適用すればよい。
2. **trace の因子分解**: $\mathrm{Tr}$ を $P$ 因子と $S_3$ 因子に分け、$S_3$ 因子が「指定された $\rho^{-1}$ 一個」を数えて $1$ になることを先に和で消す。

**射程の訂正(CLAIMS の閉鎖範囲)**: 【GAP-E2a】の閉鎖は「**$P$ 完全**」ではなく
> **exact な位数 $2,3$ の inner implementer($\theta = \mathrm{Ad}(s)$、$\tau=\mathrm{Ad}(t)$、$s^2=t^3=1$)をもつ split-inner 窓**

に限る。$Z(P)=1$ は補題 1 の直積分解 $Q\cong P\times S_3$ には必要だが、**$P$ 内類積への直接全単射には不要**である。実際、中心があっても $\sigma := \bar\Delta s^{-1}$、$\rho := \bar\delta t^{-1}$ は $P$ を中心化し $\sigma^2=\rho^3=1$ なので二つの torsion 条件は $P$ 成分だけに落ち
$$ n_m = \#\{(r,g)\in T_3(P)\times T_2(P) : rg = \bar X^m t^{-1}s\} $$
が成り立つ。**ただし中心消滅なしには $\bar X = (t^{-1}s)^2$ とは限らないので、右辺を $N_P((t^{-1}s)^u)$ まで簡約してはならない。**

**残る UNKNOWN**: (i) $A\subsetneq P$ の一般対象(可解・冪零)、(ii) $\theta,\tau$ が**外部**自己同型である完全群、(iii) 中心のため implementer の位数を $2,3$ に正規化できない完全群。⇒ **【文献要請 4】はこの 3 つに絞る。**

**追記(case B との整合)**: 委嘱 06 の補題 N が示すとおり、**case B(outer)窓では剰余類制限がパリティで自動的に課される**($r\in T_3(\tilde A)$ は必ず $\mathrm{Inn}\,G$ に入り、$w^u$ は outer ゆえ $g$ は自動的に outer 剰余類)。ゆえに $\tilde A$ 全体の $z_2(\tilde A)$ がそのまま使え、**$\mathrm{PGL}(2,q)$-table の指定 coset 類積**で閉じる。これは Sol F6/F16–F18 の処方と**同一のことを別の言い方で述べている**。

**W76(語彙規律)**: 「$P = [P,P]$」だけから $Q \cong P\times S_3$ や termwise scalar 性を推論しない。**中心消滅と exact inner implementer の役割を混同しない。**

### 6.2 【P112】最大共通商補題を $M_Q$ / $M_3$ に追記(【GAP-48a】の対象別閉鎖)

> **補題 E(subdirect-rigidity).** $R = G\times_D P$(fiber product、$D$ は共通商)とし、$H\le R$ は両射影で全射とする。Goursat により $H$ は $G$ と $P$ の**ある**共通商 $E$ によるファイバー積で、$D$ は $E$ の商である。ゆえに
> $$ \textbf{$G$ と $P$ に $D$ より真に大きい共通商が存在しなければ } H = R. $$

**適用(段 1b: $M_Q = K^{(3)}\cap N_Q$)**: $R = G_3\times_{C_2^2}Q_8$。$Q_8$ は 2 群なので共通商 $E$ は 2 群。$G_3'$($\lvert G_3'\rvert = 27$)の像は位数が 3 冪かつ 2 冪だから自明 ⇒ $E$ は $G_3/G_3'\cong C_2^2$ の商 ⇒ $\lvert E\rvert\le4$。一方 $D = C_2^2$ は $E$ の商なので $\lvert E\rvert\ge4$。ゆえに $E = C_2^2 = D$、したがって $H = R$。

**適用(段 3: $M_3 = K^{(3)}\cap N_3$)**: $P_3$(位数 128)も 2 群なので**同じ論法がそのまま通る** ⇒ $E = C_2^2$ ⇒ $H = R$。

⇒ **【GAP-48a】(定理 48 の全射性)は $M_Q$・$M_3$ の両対象で紙上閉鎖**。証明書の `generation_fail = 0` は「実測でそうなった」ではなく **紙上の予測**になった(fixture としての格が上がる)。

**命題 C′ への仮定の追加(W77)**: 「fiber product への二射影が全射なら部分群も全体」は**一般には偽**である。命題 C′ の一般版には
```
(O5) no_larger_common_quotient:
     G と P には D より真に大きい共通商が存在しない
```
を仮定として明記する。**列挙前にチェックできる条件**であることが利点(補題 D の coprimality と同じ性格)。

---

## 7. 本書に残る UNKNOWN と【GAP】

| # | 内容 | 状態 |
|---|---|---|
| 【GAP-PM1】 | 七窓の per-$m$ staged 分配の**紙上導出** | $\lvert\mathcal X\rvert\cdot\lvert G\rvert$ からの引き算と (H-a) の解数までは紙で出るが、**実装 1 と実装 2 の突合が第二系統** |
| 【GAP-PM2】 | `object_count = 2`(case B)は $\mathrm{Aut}(\tilde A) = \mathrm{Inn}(\tilde A)$ に依拠 | $q$ 非素では成り立たない。**七窓の外へ外挿しない** |
| 【GAP-PM3】 | (3.53) の合成則と $\Psi$ の両立(case A の群同型) | 命題 B 定理 B で「(反)同型」まで進んだが、**実装側の合成表による二系統化は未了** |
| 【GAP-PM4】 | 定理 M2 の第三型(case C・$\mathrm{Out}(G)\supseteq S_3$) | 本追補の 3 群では起きない。掃引を広げるときは M2 と補題 B1 の拡張が要る |
| 【GAP-PM5】 | 本書の全数値 | **実装 1 の node + 実装 2 の紙上指標計算**の一致。**GAP との突合は未了 ⇒ cross-checked ではない。Lean 未接続 ⇒ verified でもない**(W81) |
| 【GAP-PM6】 | 語規約 W-4 の遡及監査 | 既存の全証明書が (H-b′) を paper 積で書いているかを再監査していない |

**W48 遵守**: Guillot の計算済み表($\mathrm{PSL}(2,q)$ の $GT_1$)は**参照していない**(比較写像が未確立・対象が別物)。本書の数値は完全に自前。

---

## 8. 実装担当への一行

**本書の `spec` 射影だけを読み、期待値を推測しないこと。** fixture(§3)は列挙前の較正ゲートであり、**1 つでも外れたら即停止して報告する**(§1.2)。`gt_count` / `n_m` / `settled` は司令塔が封印している — **合わせに行く対象ではない**。cap(§1.1)は延長交渉の対象ではない。
**語規約(§1.4)を自分で決めてはならない。** `class_coefficient` と `generation_pass_count` は**別に数える**(§1.3・W78)。指標表を読む実装を「第二系統」と呼んではならない(§4.1・P115)。
