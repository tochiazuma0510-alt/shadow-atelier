# P-GRT-1 — ℓ=7・重み ≤5・一窓の凍結事前登録 v1

**状態札: `PREREGISTERED / UNMEASURED`**

- 登録時刻: **2026-08-23T00:14:22+09:00** (Asia/Tokyo)
- `DIR`: **graded char-0 reference → mod-7 canary → finite marked window**（一方向の予言。逆推論しない）
- `FRAME`: **B₃-gentle `GT(N)` / HS `K(0,5)/W₅` 上の `PENT_W`**
- 格: **candidate preregistration**。D3(iv) の graded-to-finite bridge と非線形 lifting は未証明である。
- 測定状態: **群・rank・GT・PENT の新規測定はすべて `UNMEASURED`**。

> **凍結規則.** 本文 §6 の payload は測定前の登録内容である。今後得られる有限窓の個数、mod-7 rank、survivor、UNKNOWN、旧 NW(7) の測定個数その他を、この v1 または payload へ輸入してはならない。結果は別の versioned result/cert に記録し、外れた場合も本予言を書き換えない。再定義・別素数・別重み・別窓は、測定前に v2 以降を新設する。

---

## 1. 唯一の宇宙と marked presentation

### 1.1 一窓だけを登録する

自由群と braid の規約を

\[
F_2=\langle x,y\rangle,\qquad
x=\sigma_1^2,\quad y=\sigma_2^2,\quad
\Delta=\sigma_1\sigma_2\sigma_1,\quad c=\Delta^2,
\]

\[
[a,b]:=a^{-1}b^{-1}ab,\qquad
\gamma_{i+1}(G):=[\gamma_i(G),G]
\]

で固定する。verbal power は

\[
G^7:=\langle g^7\mid g\in G\rangle
\]

（**すべての** 7 乗値が生成する characteristic subgroup）を意味する。元ごとの集合 \(\{g^7\}\)、下中心列の 7 番目、Frattini 部分群の略記ではない。

本票の唯一の対象は

\[
V_5(F_2):=\gamma_6(F_2)F_2^7,\qquad
\boxed{N:=V_5(F_2)\times\langle c\rangle\le PB_3=F_2\times\langle c\rangle},
\]

\[
\boxed{P:=F_2/V_5(F_2)=F_2/(\gamma_6(F_2)F_2^7)}.
\]

だけである。\(\ell\ne7\)、class \(\ne5\)、\(\gamma_7F_2^7\)、\(\gamma_6F_2^{49}\)、窓の交叉、既知の class-4 NW(7) 窓は宇宙外である。\(V_5\) が verbal で \(c\in N\) だから、\(N\in\mathrm{NFI}_{PB_3}(B_3)\) かつ VERBAL-ISO の意味で isolated である。

### 1.2 有限座標 presentation と正常形順序

class \(5<7\) なので、marked group \(P\) は自由 2 生成・class 5 の Lie 代数

\[
L_{2,\le5}(\mathbb F_7)
\]

を、次数 5 で打ち切った BCH 積（係数を \(\mathbb F_7\) に還元）で群にした Lazard 模型として固定する。すなわち underlying set は \(\mathbb F_7^{14}\)、marked generators は \(x=\exp X, y=\exp Y\)、積は \(\operatorname{BCH}_{\le5}\) である。これは ANUPQ の内部 pcgs 順序を定義に使わない有限座標 presentation である。

Hall 順序は \(b_1<b_2<\cdots<b_{14}\) とし、次を逐語で固定する。

\[
\begin{array}{lll}
b_1=x, & b_2=y, & b_3=[b_2,b_1],\\
b_4=[b_3,b_1], & b_5=[b_3,b_2],\\
b_6=[b_4,b_1], & b_7=[b_4,b_2], & b_8=[b_5,b_2],\\
b_9=[b_4,b_3], & b_{10}=[b_5,b_3], & b_{11}=[b_6,b_1],\\
b_{12}=[b_6,b_2], & b_{13}=[b_7,b_2], & b_{14}=[b_8,b_2].
\end{array}
\]

重みは順に \(1,1,2,3,3,4,4,4,5,5,5,5,5,5\)。正常形は

\[
\boxed{b_1^{e_1}b_2^{e_2}\cdots b_{14}^{e_{14}}\quad(0\le e_i<7)}
\]

を**左から右**へ掛ける second-kind coordinates とする。class \(<7\) の Lazard/Hall 正常形により一意で、\(|P|=7^{14}\)、

\[
[P,P]=\{e_1=e_2=0\},\qquad |[P,P]|=7^{12}
\]

である。実装が別 presentation を使う場合、\(x,y\) を保つ marked isomorphism と、この 14 座標への往復一致を先に証明しなければ同じ窓とは認めない。

### 1.3 \(N_{\rm ord}\) と \(\mathcal X\)

\(c=1\) in \(PB_3/N\)、\(\operatorname{ord}(\bar x)=\operatorname{ord}(\bar y)=7\) なので \(N_{\rm ord}=7\)。したがって

\[
\boxed{\mathcal X=\{m\in\{0,\ldots,6\}:\gcd(2m+1,7)=1\}=\{0,1,2,4,5,6\}}.
\]

順序は常に `[0,1,2,4,5,6]` とする。\(m=3\) は \(2m+1\equiv0\pmod7\) なので**定義的に宇宙外**であり、測定による FAIL/UNKNOWN ではない。

---

## 2. 述語版と積・作用規約

### 2.1 共通規約

- 数式の積 \(uvw\) は印字順の群積 \((uv)w\)。因子列を反転しない。
- \([a,b]=a^{-1}b^{-1}ab\)。\(z=(xy)^{-1}=y^{-1}x^{-1}\)。
- \(\theta(x)=y,\theta(y)=x\)、\(\tau(x)=y,\tau(y)=(xy)^{-1}\)。作用は各因子へ適用した後、下記の印字順で積を取る。
- \(m\) は上の固定代表 \(0,\ldots,6\) を使う。\(\lambda=2m+1\) の単元判定は mod 7。
- GAP の右作用・冪記法を使う実装は、paper word からの convention adapter を別に pin する。本票は raw GAP 文字列を数学的積と同一視しない。

### 2.2 domain/charming gate

登録 row は

\[
\operatorname{LEGAL}(m,f):\Longleftrightarrow
m\in\mathcal X\ \wedge\ f\in[P,P].
\]

これは 2401 Def. 3.1 の charming side conditions（\(2m+1\) が単元、\(f\) が derived subgroup に属する）だけであり、hexagon、SURJ、PENT をまだ含まない。

### 2.3 hexagon predicate v1

意味論上の正本を full \(B_3/N\) の 2 式とする。

\[
\tag{3.3}
\sigma_1^{2m+1} f^{-1}\sigma_2^{2m+1}f
=f^{-1}\sigma_1\sigma_2x^{-m}c^m,
\]

\[
\tag{3.4}
f^{-1}\sigma_2^{2m+1}f\sigma_1^{2m+1}
=\sigma_2\sigma_1y^{-m}c^m f.
\]

`HEX_FULL_v1(m,f)` はこの 2 本がともに成り立つこと。LEGAL row では \(f\in[P,P]\) で、かつ本窓は \(c\in N\)、\(V_5\) verbal なので、Prop. 3.4 により次の reduced 版と同値である。

\[
\tag{3.10} f\theta(f)=1\quad\text{in }P,
\]

\[
\tag{3.11}
\tau^2(y^mf)\,\tau(y^mf)\,(y^mf)=1\quad\text{in }P.
\]

探索に `HEX_REDUCED_v1` を使ってよいが、同値の side gates を cert に出し、独立照合側は full (3.3)(3.4) を使う。片方だけ、または積順を変えたものは別述語である。

### 2.4 SURJ と `GT(N)`

\[
\operatorname{SURJ}(m,f):\Longleftrightarrow
\langle \bar x^{2m+1},\ f^{-1}\bar y^{2m+1}f\rangle=P.
\]

そして本票で数える gentle population を

\[
\boxed{GT(N):=\{(m,f):\operatorname{LEGAL}\wedge
\operatorname{HEX\_FULL\_v1}\wedge\operatorname{SURJ}\}}
\]

と定義する。本窓では \(P\) が 7 群、\([P,P]\le\Phi(P)\)、\(2m+1\not\equiv0\pmod7\) なので SURJ は LEGAL row 上で従うが、述語から削除せず side-gate theorem として記録する。

### 2.5 `PENT_raw_v1` と `PENT_W`

`PENT` の評価フレームを次で固定する。

- \(K(0,5):=PB_4/\langle\Delta_4^2\rangle\)（\(PB_4/Z(PB_4)\)）。marked generator order は
  `[x12,x13,x14,x23,x24,x34]`。
- sphere rows は
  \(x_{15}=(x_{12}x_{13}x_{14})^{-1}\)、
  \(x_{25}=(x_{12}x_{23}x_{24})^{-1}\)、
  \(x_{35}=(x_{13}x_{23}x_{34})^{-1}\)、
  \(x_{45}=(x_{14}x_{24}x_{34})^{-1}\)。
- \(W_5:=\gamma_6(K(0,5))K(0,5)^7\)、\(Q_5:=K(0,5)/W_5\)。ここでも \(K(0,5)^7\) は全 7 乗値が生成する verbal subgroup。
- \(j:F_2\to K(0,5)\) は \(x\mapsto x_{12},y\mapsto x_{23}\)。同じ verbal operator を両側に使うため \(\bar\jmath:P\to Q_5\) が well-defined。
- \(\rho(x_{ij})=x_{i+3,j+3}\)（添字 mod 5、その後 \(x_{ij}=x_{ji}\) で正規化）。上の generator order での像は
  `[x45,x14,x24,x15,x25,x12]`。\(W_5\) が verbal なので \(\bar\rho\in\operatorname{Aut}(Q_5)\) が誘導される。

\(u=\bar\jmath(f)\) として

\[
\operatorname{PENT\_raw\_v1}(f):\Longleftrightarrow
\bar\rho^4(u)\,\bar\rho^3(u)\,\bar\rho^2(u)\,\bar\rho(u)\,u=1
\quad\text{in }Q_5.
\]

これは \(m\) を含まない。しかし予言で数える `PENT_W` は raw norm 通過元全体ではなく、

\[
\boxed{\mathrm{PENT}_W:=\{(m,f)\in GT(N):
\operatorname{PENT\_raw\_v1}(f)\}}
\]

という **`GT(N)` との交差集合**である。`{f∈[P,P]:PENT_raw_v1(f)}` の個数は別量で、本票では `UNKNOWN / NOT_PREDICTED`。`GT(N)`、LEGAL、hexagon、raw PENT、`PENT_W`、本来の profinite pentagon/genuine population を同一視しない。

---

## 3. row universe・key・順序・coverage

### 3.1 f-row

\([P,P]\) の row は

\[
f(e_3,\ldots,e_{14})=b_3^{e_3}b_4^{e_4}\cdots b_{14}^{e_{14}},
\qquad e_i\in\{0,\ldots,6\}
\]

とする。\(e_3\) を最上位、\(e_{14}\) を最下位にした big-endian index

\[
f\_index=\sum_{i=3}^{14}e_i7^{14-i}\in[0,7^{12}-1]
\]

を canonical key とする。\(f\)-row 数 \(7^{12}\) は Witt/Lazard 正常形から登録済みの紙上値であり、実測値ではない。

### 3.2 pair-row

`m_values=[0,1,2,4,5,6]` の位置を `m_index=0..5` とし、

\[
pair\_index=m\_index\cdot7^{12}+f\_index
\in[0,6\cdot7^{12}-1]
\]

とする。canonical row key は

`[m,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14]`。

登録した row 数は `m_count=6`, `f_count=7^12`, `pair_count=6*7^12`。列挙器は全 pair index の exact cover（欠落 0、重複 0、範囲外 0）を証明する。PENT lane を f-only で走らせる場合も、独立 join で各 f-key を 6 個の pair-key へ展開する。timeout、構築不能、未評価 row は `UNKNOWN` であり、FAIL や非存在へ丸めない。full finite enumeration が完了しない限り、\(|GT(N)|\) と \(|\mathrm{PENT}_W|\) の観測値はともに `UNKNOWN` のままである。

---

## 4. 凍結予言と外れた場合の分岐

重み 1 は charming が除く。登録する重み 2–5 の参照次元は

\[
(\dim\mathcal H_2,\dim\mathcal H_3,\dim\mathcal H_4,\dim\mathcal H_5)
=(0,1,1,2),
\]

\[
(\dim\mathfrak{grt}_2,\dim\mathfrak{grt}_3,
\dim\mathfrak{grt}_4,\dim\mathfrak{grt}_5)=(0,1,0,1).
\]

従って変更禁止の予言は

\[
\boxed{\frac{|GT(N)|}{|\mathcal X|}=7^{0+1+1+2}=7^4=2401},
\]

\[
\boxed{\frac{|\mathrm{PENT}_W|}{|\mathcal X|}=7^{0+1+0+1}=7^2=49}.
\]

各 \(m\in\mathcal X\) でそれぞれ 2401 / 49、全体では \(|GT(N)|=6\cdot2401=14406\)、\(|\mathrm{PENT}_W|=6\cdot49=294\) を予言する。これらは**測定値ではない**。

外れた場合は順に次だけを登録分岐とする。

1. **`MOD7_RANK_STEP`**: §5 の exact mod-7 rank/dimension が char-0 reference と異なる。有限個数を bridge の反例として採点する前にここで fail closed。
2. **`BRIDGE_OR_NONLINEAR_LIFTING_FAILURE`**: rank canary は一致したが、exact finite coverage 後の個数が予言と異なる。D3(iv) 型の graded-to-finite 同定、拡大類、または層の非線形 lifting/貼り合わせのどこかが破れたという分岐であり、どれか一つへ勝手に特定しない。

coverage 不完了、UNKNOWN > 0、predicate binding 不成立は予言の外れではなく **`MEASUREMENT_INCOMPLETE / UNKNOWN`** である。

---

## 5. char-0 / mod-7 rank canary（測定前固定）

体 \(k\in\{\mathbb Q,\mathbb F_7\}\) と重み \(w=2,3,4,5\) に対し、\(L_w(k)\) を \(X<Y\) の Hall basis を持つ自由 Lie 代数の斉次部分とする。列は §1.2 と同じ Hall 再帰順、展開先の非可換語は alphabet `X<Y` の lexicographic 順にする。

\[
h_w(\psi)=\bigl(
\psi(X,Y)+\psi(Y,X),\ 
\psi(X,Y)+\psi(Y,Z)+\psi(Z,X)
\bigr),\quad Z=-X-Y,
\]

\[
\mathcal H_w(k):=\ker h_w.
\]

PENT 線型 canary は \(\mathfrak t=\operatorname{gr}K(0,5)\) 上で pin する。generator order は `T0<T1<T2<T3<T4`、\(j(X)=T_0=x_{12}\)、\(j(Y)=T_1=x_{23}\)、\(\rho(T_i)=T_{i+3\bmod5}\)、

\[
\nu_w:=1+\rho+\rho^2+\rho^3+\rho^4,
\qquad
\mathcal S_w(k):=\ker\bigl(\nu_w\circ j\mid_{\mathcal H_w(k)}\bigr).
\]

quotient coordinates は 5 文字 Lyndon 語の lexicographic order から Drinfeld–Kohno ideal を rref で落とす。rank は `rank(h_w)`、および \(\mathcal H_w\) の上の `rank(nu_w*j)` として数える。

| w | dim L_w | reference dim H_w | rank h_w | reference dim S_w | rank PENT on H_w | combined rank |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 0 | 1 | 0 | 0 | 1 |
| 3 | 2 | 1 | 1 | 1 | 0 | 1 |
| 4 | 3 | 1 | 2 | 0 | 1 | 3 |
| 5 | 6 | 2 | 4 | 1 | 1 | 5 |

- char-0 reference: 上表。\(\mathcal H_w\) 列は便 156 の裁定どおり **candidate**（二大素数一致は有理 rank の下界にとどまる）。\(\mathfrak{grt}_w\) 列は memo の [NW] Cor. 7 読みの範囲で登録する。
- `char0_exact_observation`: **UNMEASURED**（本票では fraction-free/SNF 計算をしない）。
- `mod7_observation`: **UNMEASURED**（全セル）。
- future gate: char-0 exact certificate が reference と違えば `CHAR0_REFERENCE_MISS / STOP`。mod-7 の `dim L`, `dim H`, `dim S` または二つの rank が上表と違えば `MOD7_RANK_STEP / STOP`。一致した場合だけ finite count を P-GRT-1 と採点する。

rank 一致は finite bridge の証明ではない。canary PASS と個数 PASS を同一の「検証」と呼ばない。

---

## 6. canonical digest payload

次の JSON はコメントなし、key 順・配列順を変更しない。digest は opening fence 後から closing fence 前までの**文字列に terminal LF を 1 個付けた UTF-8（BOM なし）**を対象とする。

<!-- P-GRT-1-PAYLOAD-BEGIN -->
```json
{
  "conventions": {
    "commutator": "[a,b]=a^-1*b^-1*a*b",
    "full_hexagon_equations": ["3.3", "3.4"],
    "multiplication": "printed-factor-order-left-to-right",
    "reduced_hexagon_equations": ["3.10", "3.11"],
    "tau": {"x": "y", "y": "(x*y)^-1"},
    "theta": {"x": "y", "y": "x"},
    "verbal_power": "G^7=<g^7:g in G>"
  },
  "direction": "graded-char0-reference -> mod7-rank-canary -> finite-marked-window",
  "frame": "B3-gentle-GT(N)+HS-K(0,5)/W5-PENT_W",
  "freeze": {
    "later_measurement_import": "PROHIBITED",
    "registered_at": "2026-08-23T00:14:22+09:00",
    "status": "PREREGISTERED / UNMEASURED"
  },
  "pent_frame": {
    "K05": "PB4/<Delta4^2>",
    "W5": "gamma_6(K05)*K05^7",
    "generator_order": ["x12", "x13", "x14", "x23", "x24", "x34"],
    "j": {"x": "x12", "y": "x23"},
    "predicate": "rho^4(j(f))*rho^3(j(f))*rho^2(j(f))*rho(j(f))*j(f)=1 in Q5",
    "predicate_id": "PENT_raw_v1",
    "population": "PENT_W={(m,f) in GT(N):PENT_raw_v1(f)}",
    "population_excludes": "raw f-only PENT pass set",
    "rho_images": ["x45", "x14", "x24", "x15", "x25", "x12"],
    "sphere_rows": {
      "x15": "(x12*x13*x14)^-1",
      "x25": "(x12*x23*x24)^-1",
      "x35": "(x13*x23*x34)^-1",
      "x45": "(x14*x24*x34)^-1"
    }
  },
  "predicates": {
    "GT_N": "LEGAL and HEX_FULL_v1 and SURJ",
    "HEX_FULL_v1": "full B3/N equations 3.3 and 3.4 both true",
    "HEX_REDUCED_v1": "f*theta(f)=1 and tau^2(y^m*f)*tau(y^m*f)*(y^m*f)=1 in P",
    "LEGAL": "m in X and f in [P,P]",
    "SURJ": "<x^(2m+1),f^-1*y^(2m+1)*f>=P"
  },
  "prediction": {
    "GT_N_per_m": 2401,
    "GT_N_ratio": "7^4",
    "GT_N_total": 14406,
    "PENT_W_per_m": 49,
    "PENT_W_ratio": "7^2",
    "PENT_W_total": 294,
    "miss_branches": ["MOD7_RANK_STEP", "BRIDGE_OR_NONLINEAR_LIFTING_FAILURE"],
    "raw_pent_f_count": "UNKNOWN / NOT_PREDICTED"
  },
  "presentation": {
    "hall_generator_order": [
      "b1=x", "b2=y", "b3=[b2,b1]", "b4=[b3,b1]", "b5=[b3,b2]",
      "b6=[b4,b1]", "b7=[b4,b2]", "b8=[b5,b2]", "b9=[b4,b3]",
      "b10=[b5,b3]", "b11=[b6,b1]", "b12=[b6,b2]", "b13=[b7,b2]", "b14=[b8,b2]"
    ],
    "id": "lazard-bch-hall-xlt-y-v1",
    "model": "BCH_<=5(L_free_2_<=5(F7))",
    "normal_form": "b1^e1*b2^e2*...*b14^e14, 0<=ei<7, left-to-right",
    "order_P": "7^14",
    "order_derived_P": "7^12"
  },
  "rank_canary": {
    "char0_exact_observation": "UNMEASURED",
    "column_order": "Hall X<Y; same recursive order as presentation by weight",
    "failure_policy": "any char0 reference miss or mod7 rank/dimension miss is STOP",
    "mod7_observation": "UNMEASURED",
    "rows": [
      {"combined_rank": 1, "dim_H": 0, "dim_L": 1, "dim_S": 0, "rank_hex": 1, "rank_pent_on_H": 0, "weight": 2},
      {"combined_rank": 1, "dim_H": 1, "dim_L": 2, "dim_S": 1, "rank_hex": 1, "rank_pent_on_H": 0, "weight": 3},
      {"combined_rank": 3, "dim_H": 1, "dim_L": 3, "dim_S": 0, "rank_hex": 2, "rank_pent_on_H": 1, "weight": 4},
      {"combined_rank": 5, "dim_H": 2, "dim_L": 6, "dim_S": 1, "rank_hex": 4, "rank_pent_on_H": 1, "weight": 5}
    ],
    "word_row_order": "associative words lexicographic with X<Y",
    "H_definition": "ker(psi(X,Y)+psi(Y,X), psi(X,Y)+psi(Y,-X-Y)+psi(-X-Y,X))",
    "S_definition": "ker((1+rho+rho^2+rho^3+rho^4)*j restricted to H)"
  },
  "row_universe": {
    "coverage": "exact cover; missing=duplicate=out_of_range=0; UNKNOWN is not FAIL",
    "f_count": "7^12",
    "f_index": "sum_{i=3}^{14} e_i*7^(14-i), e3 most significant",
    "f_normal_form": "b3^e3*...*b14^e14",
    "key": ["m", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "e11", "e12", "e13", "e14"],
    "m_order": [0, 1, 2, 4, 5, 6],
    "pair_count": "6*7^12",
    "pair_index": "m_index*7^12+f_index"
  },
  "schema": "p-grt1-prereg-l7-w5/v1",
  "scope": {
    "ell": 7,
    "measurement": "none",
    "one_window_only": true,
    "weight_max": 5
  },
  "window": {
    "N": "gamma_6(F2)*F2^7 x <c>",
    "N_F2": "gamma_6(F2)*F2^7",
    "N_ord": 7,
    "P": "F2/(gamma_6(F2)*F2^7)",
    "X": [0, 1, 2, 4, 5, 6]
  }
}
```
<!-- P-GRT-1-PAYLOAD-END -->

Payload SHA-256: **`dc7ee417cb2dbfef3a813f62890766afbafb76dce886d0a6b1b693a5d0e57630`**

再現手順（PowerShell、群・rank・GT・PENT は構築しない）:

```powershell
$p = 'docs/notes/p_grt1_prereg_l7_w5_v1.md'
$raw = [IO.File]::ReadAllText($p, [Text.UTF8Encoding]::new($false))
$rx = '(?s)<!-- P-GRT-1-PAYLOAD-BEGIN -->\r?\n```json\r?\n(.*?)\r?\n```\r?\n<!-- P-GRT-1-PAYLOAD-END -->'
$m = [regex]::Match($raw, $rx)
if (-not $m.Success) { throw 'payload block not found' }
$literal = $m.Groups[1].Value -replace "`r`n", "`n"
$bytes = [Text.UTF8Encoding]::new($false).GetBytes($literal + "`n")
$sha = [Security.Cryptography.SHA256]::Create()
([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
```

---

## 7. 非測定チェックと open assumptions

本登録で許した操作は、既在正本の読取り、静的 payload の作成、UTF-8 bytes/SHA-256 の計算だけである。GAP/ANUPQ、群構築、要素列挙、hexagon、SURJ、PENT、char-0 rank、mod-7 rank は実行していない。とくに旧 class-4 NW(7) の測定個数は payload に入力していない（新予言の total `294` は \(6\times49\) の静的導出で、過去窓からの転記ではない）。

open assumptions / 格境界:

1. \(\mathcal H_w\) の char-0 reference は便 156 の裁定どおり candidate。二大素数一致だけを有理 rank の証明に昇格しない。
2. graded \(\mathcal H_w/\mathcal S_w\) と有限 `GT(N)/PENT_W` の各層自由度を同一視する D3(iv) 型 bridge は candidate。拡大類と非線形 lifting/貼り合わせは別勘定。
3. \(Q_5=K(0,5)/(\gamma_6K(0,5)K(0,5)^7)\) の位数、pc presentation、raw PENT 通過数は本票では `UNKNOWN`。予言の分母に使わない。
4. future measurement は marked presentation、full/reduced hexagon の独立系統、P→Q₅ の \(\bar\jmath\)、\(\rho^5=1\)、全 row exact coverage、UNKNOWN 件数を cert に pin する必要がある。
5. 本票は有限個数の予言であり、profinite genuine 性、算術像、全細分 survival、\(\widehat{GT}=\widehat{GT}_{gen}\) を判定しない。
