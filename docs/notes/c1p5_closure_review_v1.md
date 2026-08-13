# 便 125 クロスレビュー — C1′(S4)+P5′ 閉鎖パッケージ / Phase 2 cofinal / (3.60) 波及

- 起草: 影工房 **数学者**(Claude / Opus 5)/ 2026-08-13
- 委嘱: 司令塔 [CP](裁定 1142)「①P3+P5′ 閉鎖パッケージのクロスレビュー(本丸)②(3.60) 座標修理の波及点検 ③Phase 2 深度 1/2 への短評」
- 被レビュー: `sol/sol_reply_125_phase2_p3p5.md`・`docs/notes/c1prime_s4_p5prime_closure_v1.md`・`search/certs/c1prime_s4_p5prime_v1{,_check}_20260813.json`・`search/certs/d972_phase2_coord_v1{,_check}_20260813.json`・producer/checker 4 本
- **規律**: u/c 非接触(uloc cert は `"measurement"` 行の**手前で停止**して構造前置きのみ読取)・封印 3 量非接触・prereg 非抵触。**本書の数値はすべて機械生成**(裁定 1103)— スクリプト §11。

---

## 0. 判定(先に 3 行)

| 対象 | 判定 |
|---|---|
| **P3(幾何 monodromy = 504)+ C1′ dessin binding** | ★ **条件付き採用**。論理の骨格は正しく、有限計算は**独立第三系統で完全再現**。⚠ ただし **§2.3 の穴が 1 個ある**(load-bearing)— 条件 A〜D の明示化を要求 |
| **P5′(局所 Kummer 部分群比較)** | ★ **採用**(紙導出は正しい)。⚠ 前件 1 件(intrinsic 側 ℚ-模型)を本文に上げること。**⟨·⟩ への弱化は正しい設計判断** |
| **Phase 2(cofinal chain・深度 1/2 = 972/972)** | ★★ **差戻し**。値は正しいが**構造的に情報ゼロ**(**命題 PH2-VOID**・§7)。この模型では**すべての** $l$ で 972 が出る ⟹ 停止規則の「324」分岐は**到達不能**。cofinal 性・包含 (6)・半決定への格下げ・(3.60) 修理は**すべて正しく採用** |
| **(3.60) 波及** | ★ **波及なし**(該当実装は 1 箇所のみ・§8)。ただし旧 Phase 1 cert の supersede 手続きが要る |

---

## 1. 独立第三系統(私の再現)

Sol の producer / checker のコードは import せず、sympy も使わず、標準ライブラリの tuple 置換だけで組み直した(合成規約は cert の `explicit_XYZ_array_form` から**数値的に**判定 — **左から右**($(a\cdot b)[i]=b[a[i]]$)で $XYZ=1$)。

| # | 主張 | Sol producer | Sol checker | ★ 私(第三系統) | 一致 |
|---|---|---|---|---|---|
| T1 | 商 Nielsen 類の解数(第 3 分岐巡回固定) | 24 | 24 | **24** | ✓ |
| T1 | 生成群位数分布 | {81:6, 324:9, 504:9} | 同 | **{81:6, 324:9, 504:9}** | ✓ |
| T2 | 位数ごとの**相異なる部分群**数 | {81:1,324:1,504:1} | {…:1} | **{81:1, 324:1, 504:1}** | ✓ |
| T3 | $\lvert N_{S_9}\rvert$ | 324 / 1296 / 1512 | 同 | **324 / 1296 / 1512** | ✓ |
| T3 | $\lvert C_{S_9}\rvert$ | 3 / 1 / 1 | 同 | **3 / 1 / 1** | ✓ |
| T3 | 型 $(7,1,1)$ を含む normalizer | 504 のみ | 同 | **504 のみ** | ✓ |
| — | 位数 504 の 9 解が $\langle C\rangle$ の 1 軌道 | 1 軌道(サイズ 9) | — | **1 軌道(サイズ 9)** | ✓ |
| T4 | $[S_9:N(P)]\cdot\#\{{\rm ord}\,9\}$ | $240\cdot168=40320$ | — | **$240\cdot168=40320=8!$**, incidence **1** | ✓ |
| T5 | ★ $P$ の同定(**行列を使わない独立同定**) | (行列から) | — | **$\lvert P\rvert=504=9\cdot8\cdot7$ かつ順序 3 点の像が 504 通り ⟹ 鋭 3-推移 ⟹ $P\cong\mathrm{PGL}(2,8)=\mathrm{PSL}(2,8)$** | ✓ |
| — | 位数 9 の元の $P$-類 | 3 類 × 56 | — | **3 類・サイズ [56,56,56]** | ✓ |
| T6 | 固定 $Z$ の $W$-dessin 解数 | 54 | 54 | **54** | ✓ |
| T6 | $\langle Z\rangle$-軌道 | 6 個(各 9) | 6 個(各 9) | **6 個(各 9)** | ✓ |
| T6 | 対角軌道数 | 1 | 1 | **1** | ✓ |
| T7 | cert の `explicit_XYZ` | — | — | **$XYZ=1$(左右規約)・全て 9-巡回・$\lvert\langle X,Y\rangle\rvert=504$・同一 $P$-類** | ✓ |

> **★ 有限計算部は三系統一致(cross-checked)。** 私の T5 は**行列表現を経由しない独立同定**なので、Sol の $\mathbf F_8$ 行列 $S,T$ の入力誤りに対する保険にもなっている。

**★ 規約に関する副産物(前タスクの Ad 規約裁定と接続)**: producer は `diagonal_flags_by_orbit=[F,T,F,F,F,F]`(index 1)、checker は `[F,F,T,F,F,F]`(index 2)を出し、checker 自身が `X/Z exchanged under the documented left/right composition transport` と申告している。**軌道の番号だけがずれ、個数(6)と対角の個数(1)は一致** — これは左右規約の差の**予期される**現れ方であり、矛盾ではない。ただし **cert の同一欄に別番号が入っている**のは CV-9 上よろしくない。⟹ **要求 E**(§9)。

---

## 2. 急所 (a) — 幾何 monodromy $=504$ の確定論理

### 2.1 骨格(**正しい**)

Sol の論法は次の 4 段で、**私はこれを支持する**。

1. **上界(悉皆)**: 商 passport $(3^3,3^3,(9))$・第 3 分岐巡回 $C$ 固定の解は 24 個で、生成部分群は**集合として 3 個しかない**(位数 81 / 324 / 504)。$C$ を固定してよいのは $S_9$ が 9-巡回に推移的だから。
2. **算術は幾何を正規化**: $G_{\rm geom}\trianglelefteq G_{\rm arith}\le N_{S_9}(G_{\rm geom})$。
3. **下界(標本は存在にのみ使う)**: exact model の good-reduction factorization が型 $(7,1,1)$ の Frobenius witness を**存在させる** ⟹ $7\mid\lvert G_{\rm arith}\rvert$ ⟹ $7\mid\lvert N_{S_9}(G_{\rm geom})\rvert$。
4. $\lvert N\rvert=324,1296$ は $7$ で割れない ⟹ $\lvert G_{\rm geom}\rvert=504$。

> ★ **これは W92-5 への正しい回答である。** 旧設計 (G1-c) は **$W$ 水準**の passport $((9),(9),(9))$ で上界を取ろうとして失敗した(`c1prime_s4_design_v1.md` §10.1: 次数 9 推移群 34 個中 **18 個**が許容し、$A_9,S_9$ を含む)。Sol は上界を**商水準**に移した — そこでは許容群が **3 個**に落ちる。**標本は「1 個の元の存在」という、標本が正当に言える主張にだけ使われている。** 旧穴(標本分布から群を推測)は再演していない。

### 2.2 ★ 先行記述の申告(novelty-grep 領収)

Sol の §2.2 の商悉皆は **工房の既存凍結事項の再導出**である。

> `docs/notes/u_meas_m1_passport_v1.md`【FINDING U-8】(2026-07-31・凍結 F-9/F-10)逐語:
> 「**枚挙の内訳**(窓 B): 型 $3^3$ の元 × 型 $3^3$ の元で積 $=c_q$(9-巡回)となる対は **24 個**、monodromy 別に **81:6, 324:9, 504:9**。**504 の 9 個が $\langle c_q\rangle$ の 1 軌道**。」

⟹ 24 / {81:6,324:9,504:9} / 1 軌道は**既出**。Sol の新規部分は **normalizer 表 + 7-cycle 判定による強制**であり、そこは repo に先行がない(grep 済・§10)。**この訂正を Sol 側 §2.2 に入れること**(要求 D)。

### 2.3 ⚠★★ **穴** — 商 passport はどちら側の量か

Sol の cert は `passport: [[3,3,3],[3,3,3],[9]]` を**リテラルで持っている**。本文にも由来の記述がない。しかし:

$$\boxed{\ \textbf{強制の全体が「測定模型 }C_{\rm meas}\to\mathbf P^1_t\textbf{ の passport が }(3^3,3^3,(9))\textbf{ である」に懸かっている}\ }$$

そこで **代替 passport を悉皆した**(私・機械)。Riemann–Hurwitz と $W$ の登録 passport から、$C$ の可能な分岐型は
$$\bigl(3^{j_1}1^{9-3j_1},\ 3^{j_2}1^{9-3j_2},\ (9)\bigr),\qquad j_1+j_2\in\{4,5,6\}$$
に限られる(§2.4 で導出)。各々を悉皆した結果:

| $C$ の passport | 解数 | 生成群位数の分布 | $N_{S_9}$ が 7-巡回を含むか |
|---|---:|---|---|
| $(3^3,\,3^3,\,(9))$ | 24 | {81:6, **324:9**, **504:9**} | 504 のみ ✓ |
| $(3^3,\,3^21^3,\,(9))$ | **48** | {81:3, **1512:18**, **181440:27**} | ★ **1512($=\mathrm{P\Gamma L}(2,8)$)も 181440($=A_9$)も含む** |
| $(3^21^3,\,3^21^3,\,(9))$ | **36** | {**1512:36**} | ★ **含む** |
| $(3^3,\,3\cdot1^6,\,(9))$ | 3 | {81:3} | 含まない |
| $(3^21^3,\,3\cdot1^6,\,(9))$ | 0 | — | — |

> ### ⚠ **7-cycle 判定は passport を仮定しなければ 504 を強制しない。**
> $(3^3,3^21^3,(9))$ なら $G_{\rm geom}\in\{\mathrm{P\Gamma L}(2,8),A_9\}$ が生き残り、**どちらも normalizer に $(7,1,1)$ を持つ**。⟹ **商 passport の測定側での pin は load-bearing。**

### 2.4 ★ 穴は塞がる — ただし**別の cert 欄**で(私の補完)

**(i) 可能な passport の絞り込み(紙・私)**

- Shanks 三次 $\lambda^3-t\lambda^2+(t-3)\lambda+1=0$ の判別式は **$(t^2-3t+9)^2$**(機械)⟹ $\pi:\mathbf P^1_\lambda\to\mathbf P^1_t$ は巡回 3 次で、**$\tau_{1,2}=\tfrac{3\pm3\sqrt{-3}}2=3\zeta_6^{\pm1}$ のちょうど 2 点で全分岐**(RH: $-2=3(-2)+2\cdot2$ ✓)。
- 正規化 fibre 積の局所式 $e_W=a/\gcd(a,b)$($a=e_C$, $b=e_\pi$)より:
  - $b=3$(すなわち $\tau_i$ 上)で $W$ が不分岐 $\iff a\in\{1,3\}$。$a=9$ は $e_W=3\neq1,9$ を与えるので **$W$ の分岐点は $\tau_i$ の上には無い**。
  - $W$ の 3 分岐点は各 $e_W=9$(登録 passport $((9),(9),(9))$)⟹ $b=1$ かつ $a=9$ ⟹ **$C$ が全分岐する点 $p$ が 1 個**、その 3 個の $\pi$-原像が $W$ の 3 分岐点。
  - 他の点で $C$ が分岐すれば $W$ も分岐する ⟹ **$C$ の分岐台 $\subseteq\{\tau_1,\tau_2,p\}$**、$\tau_i$ での指数は $\{1,3\}$。
- RH($C$): $2g_C-2=-18+8+2(j_1+j_2)$。$g_C\ge0$ ⟹ $j_1+j_2\ge4$。**これが §2.3 の表の根拠。**

**(ii) 測定側の pin(既存 cert に**ある**)**

`search/certs/u_meas_uloc_v2_20260731.json` の構造前置き(`"measurement"` 手前・u/c 非接触):

```
"N_tau1": {"degree": 9, "deg_gcd_with_derivative": 6, "deg_radical": 3, "equals_kappa_g_cubed": true}
"N_tau2": {  同上  }
```

`docs/notes/u_meas_m3_caseb_v1.md` §(L97–99, L143)がこの記号を定義している:
$$\mathcal N_\tau(x):=\mathrm{Norm}_{\mathbf Q(C)/\mathbf Q(x)}(t-\tau),\quad \deg=9,\qquad
J:=t^2-3t+9=(t-\tau_1)(t-\tau_2),\quad \tau\in\{3\zeta_6,3\zeta_6^{-1}\}$$
$$\mathcal N_{\tau_1}=\kappa\,g^3\ (g\ \text{モニック 3 次})\iff t-\tau_1\ \text{が}\ \textbf{3 個の 3 重零点}\ \text{をもつ}$$

- $\deg\mathcal N=9$、$\deg\mathrm{rad}=3$、$\deg\gcd(\mathcal N,\mathcal N')=6=9-3$ ⟹ **相異なる 3 根が各重複度 3** ⟹ **$\tau_i$ 上の巡回型 $=3^3$** ✓
- $\tau_{1,2}=3\zeta_6^{\pm1}$ は **Shanks の分岐点そのもの** ✓(判別式の根と一致)
- ⟹ $j_1=j_2=3$、$g_C=2$、passport $(3^3,3^3,(9))$ が **測定模型について**確定。

> ### ★ 結論
> $$\boxed{\ \textbf{穴は実在するが、閉じる材料は既に cert 内にある — 論証の連結が抜けているだけ}\ }$$
> Sol は `tau_product_identities` として **この 2 欄を実際に読んでいる**。しかし「これが商 passport を pin する」という一文が無いため、`passport` 欄がリテラルの仮定に見える。**⟹ 要求 A**(§9)。

### 2.5 Frobenius witness の身分(**確認済・問題なし**)

cert の欄名は `seven_cycle_witnesses_p_t0`、中身は `[[17,1],[17,2],[17,5],[17,6],…,[19,7],[19,8]]` = **$(p,t_0)$ の対**。⟹ 標本は **$t$-線の特殊化**であり、まさに $G_{\rm arith}(C/\mathbf Q(t))$ の元を与える。$\lambda$-線から $t$-線へ移す必要がない(fibre が同一という議論を経なくてよい)。**設計として正しい。**

- 使う古典事実は 1 つだけ: **良い特殊化では $\mathrm{Gal}(f(\cdot,t_0)/\mathbf Q)\hookrightarrow\mathrm{Gal}(f/\mathbf Q(t))$ が 9 根への作用ごと埋め込む** ⟹ $\bmod p$ の分解型 = generic 群の元の巡回型。**⟹ 要求 B**(この一文の明記)。
- 併せて cert の `patterns` は $\{2^41,\ 3^21^3,\ 3^3,\ 6\cdot2\cdot1,\ 7\cdot1^2,\ 9\}$。**$3^21^3$ と $6\cdot2\cdot1$ は $\mathrm{PSL}(2,8)$ に無い型**(位数 6 の元が無い)⟹ $G_{\rm arith}\supsetneq\mathrm{PSL}(2,8)$ が**存在論的に**言える。$G_{\rm geom}=504$ と合わせて $G_{\rm arith}=N_{S_9}(P)=\mathrm{P\Gamma L}(2,8)$(位数 1512)が整合的に確定する。**これは無料の増し**であり、`monodromy_arithmetic` 欄(設計 §2.2 の 2 欄分離)に書ける。⟹ **推奨 F**。
- ⚠ ただし `outside_PGammaL_2_8: []` は**標本の陰性**であって上界の証明ではない。**この用途には使っていない**ことを cert に明記(既に `NOT_USED_FOR_C1PRIME` 相当の設計はある)。

---

## 3. 急所 (b) — $\iota_C$ の $\mathbf Q$ 降下

### 3.1 論理(**正しい**)

$$C_{S_9}(P)=1\ \Longrightarrow\ \mathrm{Aut}(C_{\rm can}/\mathbf P^1_t)=1\ \Longrightarrow\ \text{分岐ラベルを保つ幾何同型は一意}$$

(被覆の deck 群 $\cong$ monodromy 群の $S_9$ 内中心化群。私も $C_{S_9}(P)=1$ を独立確認。)
$\sigma\in G_{\mathbf Q}$ に対し $\sigma(\iota_C)$ も同種の同型 ⟹ **一意性より $\sigma(\iota_C)=\iota_C$** ⟹ $\iota_C$ は $\mathbf Q$ 上定義。**この向きの論法は正しい。**

⚠ 存在(そもそも $\bar{\mathbf Q}$ 上同型か)は §2.1 の強制 + §2.2 の「位数 504 の 9 解は $\langle C\rangle$ の 1 軌道」= **商 dessin の一意性**から出る。ここも正しい。

### 3.2 ⚠ 欠けている 1 歩 — $C_{\rm can}$ の**定義体**

Sol は「両 cover が $\mathbf Q$ 上にあるため」と書く。$C_{\rm meas}$ は命題 U-Q により $\mathbf Q$ 上。**$C_{\rm can}$ の $\mathbf Q$-定義体は自明ではない**(moduli 体 $=\mathbf Q$ から定義体 $=\mathbf Q$ は一般に障害がある)。

- ★ **ただし工房は既にこれを持っている**: 文献ゲート配達覚書 `docs/notes/litgate_positive_genus_belyi_v1.md` §(I)(LEDGER 633)逐語 —
  > 「商曲線 $C=W/\varphi$ 上の Belyi 写像: 種数 2 の超楕円曲線上の次数 9 の写像で、passport $(3^3,3^3,(9))$・monodromy PSL(2,8)(9T27)・**その passport 内で剛(一意)**・**Q 上定義**。」
- ⟹ **新規の文献要請は不要**(出所つきで使える)。⟹ **要求 C**: 本文の「両 cover が $\mathbf Q$ 上にある」に **この出所を pin** する。
- ⚠ 併せて **覚書の「passport 内で剛(一意)」は monodromy 込みで読むべき**(素の passport には §2.3 の通り位数 81/324 の dessin も居る)。工房側の凍結 F-10「商 Nielsen 類数 1(剛)」も窓 A の 28 が $A_{10}$ 限定であることから同様の読み。**この但し書きを覚書参照時に併記**。
- (背景として、$\mathrm{Aut}=1$ ⟹ moduli 体 $=$ 定義体 という剛性降下の一般定理があるが、**覚書があるので援用不要**。援用する場合のみ【文献要請】を立てる。)

---

## 4. 急所 (c) — $240\cdot168=8!$ と対角 dessin の同定

**正しい。私も完全再現(§1 T4/T6)。** 論法を明示しておく:

1. $P$ の位数 9 の元は $168$ 個で、**すべて 9-巡回**($P$ の 9 点作用で位数 9 の元は不動点をもたない)。
2. incidence 二重勘定: $\#\{(P',g):P'\sim_{S_9}P,\ g\in P',\ g\ \text{9-巡回}\}=[S_9{:}N(P)]\cdot168=240\cdot168=40320$。
3. 一方 $S_9$ の 9-巡回は $8!=40320$ 個で、$S_9$-共役は 9-巡回に推移的 ⟹ 各 9-巡回を含む $P$-共役体の個数は**定数** $k$ ⟹ $40320\,k=40320$ ⟹ $k=1$。
4. ⟹ **固定した $Z$ を含む $P$-共役体はただ 1 つ**。その中で $XY=Z^{-1}$($X,Y$ 位数 9)は 54 解、$\langle Z\rangle$-軌道 6 個、うち対角ちょうど 1 個。

> ⚠ **前提の明記が要る(要求 G)**: 手順 1「位数 9 の元がすべて 9-巡回」は $P$ の**特定の 9 点作用**に依存する事実であり、抽象群の性質ではない。cert には `order9_element_count=168` と `ord_XYZ=[9,9,9]` はあるが、「168 個すべてが 9-巡回」の欄が無い。**1 欄追加**を要求(私の第三系統では確認済み)。

---

## 5. 急所 (d) — P5′ の紙導出

### 5.1 導出は**正しい**

$P_0$($\lambda=0$ 上の唯一の分岐指数 9 の点)は labelled base を保つ $\iota_W$ で保存。$\mathbf Q$-有理局所助変数 $s_{\rm int},s_{\rm meas}$ に対し完備局所環の同型から $s_{\rm meas}=\gamma s_{\rm int}(1+O)$、$\gamma\ne0$。定義 $\lambda=u_{S4}s_{\rm int}^9(1+O)=u_0s_{\rm meas}^9(1+O)$ より
$$u_0=u_{S4}\gamma^{-9}\ \Longrightarrow\ [u_0^{-1}]_9=[u_{S4}^{-1}]_9\quad\text{in }K^\times/(K^\times)^9 .$$
向きの取り替え $\varepsilon\in(\mathbf Z/9)^\times$ を許すと $[u_0^{-1}]_9=[u_{S4}^{-1}]_9^{\varepsilon}$、生成部分群は不変 ⟹ (P5′)。**代表元の等号を主張しない**のも正しい。

### 5.2 ★ **⟨·⟩ への弱化は正しい設計判断**(積極評価)

装置が要求するのは `s4_recon_device_v1.md` の橋
$$d_{S4}=\mathrm{ord}\bigl([u_{S4}^{-1}]_9\bigr)$$
であり、**位数は巡回部分群だけで決まる**。⟹ (P5′) は P5(`u_0=u_{S4}` の等号・`s4_recon_device_v1.md` §1.4 の【S4R-GAP-1】= 「最大の未確認」)を**必要十分な強さちょうど**まで弱めている。$\varepsilon$ 乗の吸収も同じ理由で無害。**設計として正しい。**

### 5.3 ⚠ 前件 1 件

$s_{\rm int}$ の存在 = **intrinsic 側の $\mathbf Q$-模型の存在**。これは §3.2 と同一の前件で、覚書 §(I) の「$\mathbf Q$ 上定義」で足りる。**本文の前件表に上げること**(要求 C に含む)。

---

## 6. ⚠ kernel word 復元は**恒等式**(独立情報を持たない)

cert の `reconstruction_XYZ_exact=[true,true,true]` は証拠に見えるが、producer の定義
$$q_a:=A,\qquad q_b:=x^{-1}A^{-1},\qquad r_x:=(q_bq_a)^{-1},\ r_y:=(q_aq_b)^{-1},\ r_z:=(r_xr_y)^{-1}$$
から $r_x=x$、$r_y=AxA^{-1}$ は **自由群で恒等的に従う**(私の T8 で語簡約により機械確認)。$y$ は producer 内で $AxA^{-1}$ と**定義**されているので、3 つの `true` は**トートロジー**である。

> ### ⟹ 実質の binding は別のところにある
> 本当に効いているのは「**Shanks 三次の分岐点 $\{3\zeta_6^{\pm1}\}$ が $C$ の 2 つの位数 3 分岐点と一致する**」(§2.4)であり、これは
> - 判別式 $(t^2-3t+9)^2$
> - `u_meas_m3_caseb_v1.md` の $J=t^2-3t+9=(t-\tau_1)(t-\tau_2)$、$\tau=3\zeta_6^{\pm1}$
> - `N_tau1/N_tau2 = κg³`
>
> の 3 点で閉じる。**cert はこの 3 点を `fibre_product_binding` に持つべきで、`reconstruction_XYZ_exact` は証拠欄から降格すべき。⟹ 要求 A(再掲・統合)。**

**(公平のため)** 群としての底変換の同定自体は妥当である: $\varphi:\Delta(3,3,9)\to\mathbf Z/3$、$A\mapsto\omega,\ B\mapsto\omega^{-1},\ C\mapsto1$ の核は $\Delta(9,9,9)$(orbifold Euler 標数比 $(-2/3)/(-2/9)=3$)で、その 3 つの位数 9 生成元は $A^{-1}CA,\ C,\ ACA^{-1}$ ⟹ Sol の kernel word と一致する。**問題は「この $\varphi$ が Shanks 底変換である」の記録が無いこと**だけ。

---

## 7. ★★ Phase 2 — **命題 PH2-VOID**(差戻しの理由)

### 7.1 実装が実際にしていること

producer `roof_measure` / checker `roof_raw` は、屋根を
$$\mathrm{ROOF}(l)\;=\;\mathrm{GT}(K^{(l)})\times_U\mathrm{GT}(N_{S4}),\qquad U=(\mathbf Z/18)^\times,\quad \mathrm{GT}(N_{S4})\ \text{模型}=\{(u,\text{transl})\}\ (6\times9=54)$$
と**模型化**し、reduction を
$$R\bigl((e,s)\bigr)=\bigl(e\bmod K^{(9)},\ s\bigr)\qquad(\textbf{S4 座標は恒等})$$
で定義して像を数えている。

### 7.2 命題 PH2-VOID

> ### 命題 PH2-VOID
> 上の屋根模型のもとで、任意の $l$ に対し
> $$\bigl\lvert\mathrm{Im}\,R_{K^{(l)}\cap N_{S4},\,M}\bigr\rvert\;=\;\bigl\lvert\mathrm{Im}\bigl(\mathrm{GT}(K^{(l)})\to\mathrm{GT}(K^{(9)})\bigr)\bigr\rvert\times 9 .$$
> とくに **Thm 4.3 より dihedral reduction は全射**(私の Phase 2 設計 §1 で証明済・本書 §7.3 で再実測)だから
> $$\boxed{\ \textbf{すべての }l\ \textbf{で}\ \lvert\mathrm{Im}\,R\rvert=108\times9=972\ }$$
>
> **証明.** $u$ 値ごとの S4-fibre のサイズが $u$ に依らず一定($=9$)であることから
> $\lvert\mathrm{Im}\,R\rvert=\sum_{e'\in\mathrm{Im}(\text{dih})}\#\{s: u(s)=u(e')\}=\lvert\mathrm{Im}(\text{dih})\rvert\cdot9$。∎

### 7.3 機械確認(11 個の $l$・私)

| $l$ | 9 | 27 | 36 | 45 | 54 | 63 | 72 | 81 | 108 | 135 | 162 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $\lvert\mathrm{GT}(K^{(l)})\rvert$ | 108 | 972 | 216 | 2160 | 972 | 4536 | 864 | 8748 | 1944 | 19440 | 8748 |
| $\lvert\mathrm{Im}(\text{dih}\to K^{(9)})\rvert$ | **108** | **108** | **108** | **108** | **108** | **108** | **108** | **108** | **108** | **108** | **108** |
| 屋根サイズ | 972 | 8748 | 1944 | 19440 | 8748 | 40824 | 7776 | 78732 | 17496 | 174960 | 78732 |
| ★ $\lvert\mathrm{Im}\,R\rvert$ | **972** | **972** | **972** | **972** | **972** | **972** | **972** | **972** | **972** | **972** | **972** |

**dihedral reduction は 11/11 で全射・恒等式 $\lvert\mathrm{Im}R\rvert=\lvert\mathrm{Im}_{\rm dih}\rvert\cdot9$ は 11/11 で成立。**

### 7.4 ⟹ 帰結(3 点)

1. ★ **深度 1/2 と横断 $l=36$ の「972, 972, 972」は測定ではない** — Thm 4.3(dihedral reduction の全射性)の**再導出**である。**情報量ゼロ。**
2. ★ **登録済み停止規則の「324 ⟹ A 型側の有限証明書を保存して停止」分岐は、この模型では到達不能**。⟹ **半決定手続きとしても空回りする**(Sol §1.2 の格下げは正しかったが、まだ足りない)。
3. ★ **原因は模型ではなく数学**: 私は `d972_h1_adjudication_v1.md` で $\lvert B_3/M\rvert=1{,}469{,}664=2916\times504$ を示した。$B_3/N_{S4}\cong\mathrm{PSL}(2,8)$ は**単純**で、$\lvert G_l\rvert=4l^3$(奇 $l$)/ $4(l/2)^3$(偶 $l$)は **$504$ で割り切れない**(私の機械確認: $l=9,27,36,45,54,63,72,81,108,126,135,162$ の**全部で false**)⟹ $G_l$ は $\mathrm{PSL}(2,8)$ を商に持てない ⟹ $K^{(l)}N_{S4}=B_3$ ⟹
$$\boxed{\ B_3/(K^{(l)}\cap N_{S4})\ \cong\ G_l\times\mathrm{PSL}(2,8)\qquad(\textbf{完全直積・すべての }l)\ }$$
   ⟹ shadow の 2 因子は**完全に分離**しており、**dihedral 側をいくら深めても S4 座標に触れられない**。

> ### ⟹ Phase 2 の再設計指針(私の Phase 2 設計 §2 の heuristic を**定理に格上げ**)
> - 設計 §2 の「欠けている $1/3$ は Kummer 絡み $\langle[a]\rangle\cap\langle[b]\rangle$ そのもの ⟹ 片方の因子だけ深める軸は構造的に弱い」は **heuristic ではなく §7.4-3 の帰結**だった。
> - 設計 §4 の「軸 (i) 3-塔 / 軸 (ii) S4 側細分」は**両方とも死ぬ**(軸 (ii) は既に §4 で $N_{S4}^\diamond=N_{S4}$ により死んでいた)。
> - ★ **生き残るのは「$B_3/K$ が $($可解$)\times\mathrm{PSL}(2,8)$ に分解しない窓 $K\subseteq M$」だけ。** $K^{(l)}\cap N_{S4}$ 族はすべて分解する ⟹ **族ごと除外**。
> - ⟹ 次の標的は **$B_3/N_{S4}=\mathrm{PSL}(2,8)$ の非分裂拡大を実現する窓**(例: $\mathrm{PSL}(2,8)$ の Schur 乗数/表現論的持ち上げ、あるいは $\mathrm{P\Gamma L}(2,8)$ 窓)。**これは新しい探索設計であり、本書の射程外**(司令塔へ上申)。
> - **私の凍結予言 P-PH2-1**($K^{(81)}\cap N_{S4}$ も 972)は **$l=81$ 行で機械的に確認**したが、命題 PH2-VOID により**予言としての情報価値は消滅**した(当たって当然)。**正直に記録する。**

### 7.5 CV-9(仕様同一性)の指摘

producer と checker は **helper 非共有だが意味論は同一**(両方 `roof_raw`/`roof_measure` として同じ fibre 積模型を実装)。⟹ `all_checks_true=true` は**算術の一致**を保証するが、**「屋根が本当にその fibre 積か」については何も言っていない**。格付けは `cross-checked(模型内)` が上限。**⟹ 要求 H。**

なお **屋根模型そのもの**は §7.4-3 の直積分解から正当化できる(私が上で与えた)。ただし $F_2$ 側の対応する分解を 1 行書く必要がある(**要求 I**)。この点は本パッケージ由来の欠陥ではなく、既存の式 (2) $\lvert\mathrm{GT}(M)\rvert=108\cdot54/6=972$ に元から付いている前件である。

---

## 8. (3.60) 座標修理の波及点検

### 8.1 瑕疵の特定と**方向**

唯一の該当箇所:
```
search/d972_phase1_v1.g:130:  modBase := coarseOrd / 2;   ## u = 2m+1 (mod coarseOrd) <=> m (mod coarseOrd/2)
```
コメント内部は整合しているが、**正典 (3.60) が要求するのは $m\bmod H_{\rm ord}$**(同値な $u$-表現は $u\bmod 2H_{\rm ord}$)。⟹ 使った法が**半分**。

★ **方向の裁定(重要)**: $\mathrm{modBase}$ が粗い ⟹ 候補集合 `mFineCands` は正しい集合の**上位集合**。`LiftCheck` は**存在判定**なので、誤差は **偽陽性のみ**を生む。機械確認($\text{coarseOrd}=18,\ \text{fineOrd}=54,\ m=0$):正しい候補 `[0,18,36]`(3 個)に対し旧 helper は `[0,9,18,27,36,45]`(6 個)⟹ **上位集合・余分 3 個**。
$$\Longrightarrow\ \boxed{\ \textbf{旧 Phase 1 は }\lvert\mathrm{Im}\,R\rvert\ \textbf{を}\textbf{過大評価}\ \textbf{する側の瑕疵} = \textbf{「324 なのに 972 と出る」危険}\ }$$
**まさに危険な向きだった。** Sol の再列挙(正しい法)で 972 が再現されたことにより解消 — この照合は**必須だった**。⟹ **Sol の自己申告と処置は適切。**

### 8.2 他 cert への波及(**なし**)

| 実装 | m 比較 | 判定 |
|---|---|---|
| `search/d972_phase1_v1.g:130` | `coarseOrd/2` | ★ **瑕疵**(該当・retract 済) |
| `search/d972_phase2_v1.g:88` | `mm mod coarseOrd = m mod coarseOrd` | ✓ 正 |
| `search/at2_p2_quantization_v1.g:237` | `mPushed := sh.m mod W.Nord` | ✓ **正**(前段 L212 で `WM.Nord mod W.Nord = 0` の可除性前件も検査済) |
| `search/kerchi-judge.g:554`, `a16/a18/a20-kernel-structure.g` | `(2*k+1) mod (2*W.Nord)` | ✓ **正**($u$ 側は $2N_{\rm ord}$ 法 — (3.60) と同値) |
| charming 判定 `Gcd(2*mm+1, Nord)` 各所 | — | ✓ 無害($2m+1$ は奇数ゆえ $\gcd(\cdot,N_{\rm ord})=1\iff\gcd(\cdot,2N_{\rm ord})=1$) |

> ### ⟹ **P2 量子化(`at2_p2_quantization` / trace [24,24])は無傷。値の変更なし。**
> `coarseOrd`/`modBase` の grep はリポジトリ全体で上表の 2 ファイルのみにヒット。**波及半径 = 1 ファイル・1 行。**

### 8.3 事務(司令塔へ)

- `search/certs/d972_phase1_v1_20260813.json`(SHA `b41c9968…`)は **superseded** の札を貼ること(削除ではない)。Phase 2 cert は `input_sha256` でこれを束縛しているので、**「束縛はするが根拠には使わない」**の明記が要る。
- 裁定 1133 で研究者に報告した Phase 1 の生値 972 は**値としては生存**(修理後再現)。ただし §7 により**その 972 の情報価値は別途ゼロ**である旨を併記。

---

## 9. 差戻し/採用の条件(Sol への要求)

| # | 対象 | 要求 | 重み |
|---|---|---|---|
| **A** | closure §2.2 / cert `quotient_dessin.passport` | ★★ **商 passport の測定側 pin を論証として書く**: 判別式 $(t^2-3t+9)^2$ ⟹ Shanks 分岐 $=\{3\zeta_6^{\pm1}\}$、`N_tau1/N_tau2 = κg³`(既読)⟹ $\tau_i$ 上が $3^3$、$W$ 登録 passport $((9),(9),(9))$+RH ⟹ 分岐台 $\subseteq\{\tau_1,\tau_2,p\}$。**この 3 点を `fibre_product_binding` の必須欄に** | ★★ **必須**(§2.3 の代替 passport census が示す通り load-bearing) |
| **B** | closure §2.2 | 「良い特殊化で $\mathrm{Gal}(f_{t_0}/\mathbf Q)\hookrightarrow\mathrm{Gal}(f/\mathbf Q(t))$(9 根への作用ごと)」の一文 + witness が **$t$-線**の $(p,t_0)$ であることの明記 | ★ 必須 |
| **C** | closure §2.2/§3 | $C_{\rm can}$(および $s_{\rm int}$)の $\mathbf Q$-定義体を `litgate_positive_genus_belyi_v1.md` §(I)(LEDGER 633)に pin。**「passport 内で剛」は monodromy 込みの読み**である但し書きを併記 | ★ 必須 |
| **D** | closure §2.2 | **先行記述の申告**: 24 / {81:6,324:9,504:9} / 1 軌道は `u_meas_m1_passport_v1.md`【FINDING U-8】F-9/F-10(2026-07-31 凍結)が既出。Sol の新規は normalizer + 7-cycle 強制 | ★ 規律 |
| **E** | 2 cert | `diagonal_flags_by_orbit` の**軌道番号規約**を 1 つに固定(producer index 1 / checker index 2)。左右合成規約を cert の `convention` 欄に明記(**正典 = 左 $\mathrm{Ad}(g):h\mapsto ghg^{-1}$・GAP 既定 = 右**) | ★ CV-9 |
| **F** | cert(推奨) | `monodromy_arithmetic` 欄を作り、$3^21^3$ / $6\cdot2\cdot1$ の存在から $G_{\rm arith}\supsetneq\mathrm{PSL}(2,8)$、$=\mathrm{P\Gamma L}(2,8)$ を記録(無料の増し)。`outside_PGammaL_2_8: []` は**上界に使っていない**と明記 | 推奨 |
| **G** | cert | 「$P$ の位数 9 の元 **168 個がすべて 9-巡回**」を 1 欄追加(§4 手順 1 の前提) | ★ 必須 |
| **H** | Phase 2 cert | ★★ **命題 PH2-VOID の記載と停止規則の撤回**。producer/checker が**意味論同一**であること(CV-9)の申告。格付け上限 `cross-checked(模型内)` | ★★ 差戻し条件 |
| **I** | addendum §3.1 式 (2) | 屋根の fibre 積が**等式**である根拠(§7.4-3 の直積分解)+ $F_2$ 側の対応分解の 1 行 | ★ 必須 |

---

## 10. 便 124 発効条件 4 点の充足判定

| # | 条件(便 124 §8) | 判定 |
|---|---|---|
| 1 | 式 (4) の記号へ修正し B1 の正本を正しい文書へ pin | ✓ 充足(`triad972_canonical_addendum_v1.md` §3.1)— ⚠ 要求 I の 1 行を追加 |
| 2 | P2 を閉じ **P3 を閉じ** P5 を (P5′) として証明書化(P1 は逐項 pin) | ★ **要求 A〜C, G を入れれば充足**。現状は **条件付き** |
| 3 | SINGLE-BIT に包含 (6) を追記し「決定」を「半決定」に直す | ✓ 充足(Sol §1.2 + 私の Phase 2 設計 §3.3/3.4) |
| 4 | Phase 2 を cofinal enumeration/chain にする | △ **形式は充足・実質は空**(§7)。⟹ **要求 H を入れれば「充足かつ空である旨が明記された」状態**になる |

> ### ⟹ 私の裁定
> $$\boxed{\ \textbf{要求 A・B・C・G・H・I の 6 件を反映した版に限り、TRIAD-972 具体適用の theorem-candidate package の再提出に}\ \textbf{同意}\ }$$
> **ただし条件 4 について**: package 本文に「SINGLE-BIT の具体判定は $K^{(l)}\cap N_{S4}$ 族では**原理的に不可能**(命題 PH2-VOID)。判定可能性は未解決 = **UNKNOWN**」と**明記**すること。これ無しに「半決定手続きがある」と書くのは**実質的に誤り**である。
>
> ⚠ **$r_{\rm TRIAD}$ と 648 の conditional が「実質剥がれる」という司令塔の見通しについて**: **剥がれるのは P3/P5′ 経由の $d_{S4}$ 橋の前件**だけであり、**648 の A 型/B 型判定(= SINGLE-BIT)の conditional は剥がれない**。むしろ §7 で**判定手段が 1 つ失われた**。この区別を裁定文に落とすこと。

---

## 11. novelty-grep 領収書(私の恒久対策・3 度の失敗の再演防止)

| 主張 | grep コマンド | ヒット | 判定 |
|---|---|---|---|
| 商悉皆 24 / {81:6,324:9,504:9} / 1 軌道 | `grep -rn "(3^3,3^3\|商 passport\|quotient passport"` docs/ sol/ | **6 件**(`u_meas_m1_passport_v1.md` F-9/F-10, `r1_branch_retraction_v1.md`, `p8_corr_v1.md`, `s4_recon_device_v1.md`, `u_meas_m3_design_v1.md`) | ★ **既出** — §2.2 で先行を明記(**新規主張しない**) |
| 商 dessin の $\mathbf Q$-定義体・剛性 | `grep -n "剛\|Q 上定義\|定義体" litgate_positive_genus_belyi_v1.md` | **1 件**(§(I)) | ★ **既出**(文献ゲート配達)— §3.2 で pin |
| **代替 passport $(3^3,3^21^3,(9))$ / $(3^21^3,3^21^3,(9))$ の census** | `grep -rn "3\^2 1\^3\|(3,3,1,1,1)\|3²1³\|181440"` docs/ sol/ | **0 件**(181440 のヒットは全て $A_{10}$/窓 A 文脈で無関係) | ★ **新規**(§2.3) |
| **命題 PH2-VOID**(屋根模型で $\lvert\mathrm{Im}R\rvert$ が恒等的に 972) | `grep -rn "PH2-VOID\|恒等的に 972\|情報ゼロ\|発火不能"` docs/ sol/ | **0 件**(「情報ゼロ」のヒットは B₄ hexagon・$d$ ゲート等で別対象) | ★ **新規**(§7.2) |
| **$B_3/(K^{(l)}\cap N_{S4})\cong G_l\times\mathrm{PSL}(2,8)$ の全 $l$ 版** | `grep -rn "2916 x 504\|直積分解"` docs/ | **$l=9$ のみ**(私の `d972_h1_adjudication_v1.md`) | ★ **一般 $l$ は新規**(§7.4-3) |
| $C$ の passport の RH による絞り込み | (上の 1 行目に含む) | 先行は**結論のみ**(F-9)、**導出は無し** | 導出は新規・結論は既出 |

---

## 12. 検算スクリプト(すべての数値の出所)

| スクリプト | 出す数値 |
|---|---|
| `scratchpad/c1p5_review_check.py` | §1 の表 T1–T8 全部(24 / {81:6,324:9,504:9} / 部分群 1 個ずつ / normalizer 324,1296,1512 / centralizer 3,1,1 / 7-cycle 判定 / $240\cdot168=8!$ / 鋭 3-推移 / 位数 9 の 3 類 × 56 / 54 解・6 軌道・対角 1 / cert の explicit XYZ / kernel word 恒等式) |
| `scratchpad/ph2_void_check.py` | §7.3 の 11 列表・命題 PH2-VOID の恒等式・§8.1 の候補集合の上位集合性 |
| (inline) | Shanks 判別式 $(t^2-3t+9)^2$・代替 passport census(§2.3 の 5 行)・$504\nmid\lvert G_l\rvert$ の 12 個 |

> **格付け**: §1 の有限計算 = **cross-checked(三系統)**。§2.4 / §4 / §5.1 / §7.2 / §7.4-3 の紙部分 = **paper-proof(単系統・Sol 未監査)**。**verified ではない**(Lean 化なし)。u/c・封印 3 量・prereg 量は**非接触**。

---

## 13. ★ 司令塔への上申(2 件)

1. **Phase 2 の再設計が要る。** $K^{(l)}\cap N_{S4}$ 族は§7.4-3 により**族ごと除外**。次の標的候補は「$B_3/K$ が $(\text{可解})\times\mathrm{PSL}(2,8)$ に分解しない窓」— 具体的には $\mathrm{P\Gamma L}(2,8)$ 窓($G_{\rm arith}$ 側・§2.5 で存在が示唆された)や $\mathrm{PSL}(2,8)$ の非分裂拡大。**設計は次委嘱で書ける。**
2. **裁定 1133 の「Phase 1 発火済み」の読みを補正されたい。** 発火(手続き完了)は正しいが、**得られた 972 は情報ゼロ**(§7)。研究者への報告に「値は正しい・情報は無い」の 1 行を。
