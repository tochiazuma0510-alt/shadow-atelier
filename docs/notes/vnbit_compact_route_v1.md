# vN-BIT compact route — $E$ を実体化しない rigidity 測定の spec

- 起草: 影工房 **数学者**(Claude / Opus 5)/ 2026-08-13
- 委嘱: 司令塔(裁定 1150)「$E$ を実体化せずに vN-BIT rigidity 測定(648 対)を計算する路の設計」
- **関連既存定理(委嘱様式)**: **BLIND-vNext / vN-BIT / 命題 ORBIT**(`ab_instrument_redesign_v2.md`)/ **SPLIT-NULL″**(`ihnec_v1.md` §6.4・裁定 374/388)/ 正典 **Cor 5.4** / **定理 M1**($\tau=\mathrm{Ad}(t)$・`u_meas_m1_passport_v1.md`)
- **規律**: u/c 非接触・封印 3 量非接触・prereg 非抵触。数値は機械生成(§8)。

---

## 0. 結論(先に 4 行)

1. ⚠⚠ **規模問題より前に前件が破綻している**。私の新 gating(機械):
   $$\boxed{\ \theta,\tau\ \textbf{不変な非自明}\ \mathbf F_3[G_3]\textbf{-加群は存在しない(0 個)}\ }$$
   $G_3^{\rm ab}\cong C_2\times C_2$ の 3 つの指数 2 部分群を **$\tau$ が巡回置換**する(1 つは $\theta$ 不変だが $\tau$ 不変でない)。$O_3(G_3)=[G_3,G_3]$(位数 27)より $\mathbf F_3[G_3]$ の既約はこの 3 指標のみ。⟹ **便 129 の $7\otimes1$($\dim V=7$)設計は $B_3$-安定な窓を与えない。**
2. ★ **軌道機構が二段目で効く**: $\tau$-軌道を束ねると $\dim V_{G_3}\ge3$ ⟹ $\dim V\ge 7\cdot3=\mathbf{21}$ ⟹ $\lvert E\rvert\ge54{,}432\cdot3^{21}\approx\mathbf{5.7\times10^{14}}$。**実体化路は原理的に死んでいる**(GHA 大型 runner でも不可)。
3. ★★★ **compact 路は $\dim V$ の多項式で済む**: 必要なのは $\rho:W\to GL_{21}(\mathbf F_3)$(**$21\times21$ 行列**)と $\mathbf F_3^{21}$ 上の線形代数だけ。**$3^{21}$ は一度も現れない。**
   $$\boxed{\ \textbf{不可能問題 }(5.7\times10^{14})\ \longrightarrow\ \textbf{324 回の }21\times21\ \mathbf F_3\ \textbf{線形解}\ }$$
4. 根拠は 2 本の定理: **LIFT-AFF**(hexagon の $V$-成分は $v$ について **affine**)+ **GEN-AFF**(生成条件も **affine**)。⟹ 委嘱 (3) の「$10^8$ 実体化」は**不要**であり、GHA 委嘱も不要。

---

## 1. 設定と記法

$$W:=P\times G_3\ (\lvert W\rvert=504\cdot108=54{,}432),\qquad
E:=V\rtimes W,\qquad V=\mathbf F_3^{\,d}\ (W\text{-加群}),$$
$$N_W:=N_{S4}\cap K^{(3)}\ \ (PB_3/N_W\cong W\ \text{— Goursat: }G_3\ \text{可解},P\ \text{単純}),\qquad
N_E:=\ker(PB_3\twoheadrightarrow E).$$

**分解**: $c\in N_W$ ゆえ $F_2/N_{W,F_2}\cong W$、同様に $F_2/N_{E,F_2}\cong E$。shadow の $f$-成分は $E$ の元とみなせる。$E=V\rtimes W$ の集合論的分解 $f=v\cdot\bar f$($v\in V$、$\bar f\in W$)を固定する(加法記法: $V$ は $\mathbf F_3$-線形空間、$W$ の作用を $\rho:W\to GL(V)$)。

**$N_W$ 水準の shadow 群**(機械確認・§8):
$$\lvert GT(K^{(3)})\rvert=12\ (m\in\{0,2,3,5\}\subset\mathbf Z/6,\ k\in\mathbf Z/3),\qquad
\lvert GT(N_{S4})\rvert=54,\qquad \boxed{\lvert GT(N_W)\rvert=\mathbf{324}}$$
($N_{W,\rm ord}=\mathrm{lcm}(9,6)=18$、$\mathbf Z/18\cong\mathbf Z/9\times_{\mathbf Z/3}\mathbf Z/6$ による貼り合わせ。$N_W$ は分裂屋根なので **SPLIT-NULL** により $f$-成分は独立 ⟹ fibre 積)。

---

## 2. ★★ 定理 LIFT-AFF — hexagon は $v$ について affine

> ### 定理 LIFT-AFF
> $\Phi(m,f)=1$ を shadow 条件のうち $f$ を含む任意の語関係式(hexagon (3.11)/(3.12) など)とする。$f=v\bar f$ と置くと、$\Phi(m,v\bar f)$ の $W$-成分は $\Phi(m,\bar f)$ の $W$-成分に等しく、**$V$-成分は $v$ について affine**:
> $$\Phi(m,v\bar f)_V\ =\ A^\Phi_{m,\bar f}\,v\ +\ \Phi(m,\bar f)_V,\qquad A^\Phi_{m,\bar f}=\sum_{i}\varepsilon_i\,\rho(\bar g_i)\in\mathrm{End}_{\mathbf F_3}(V).$$
> ここで $i$ は語 $\Phi$ 中の $f^{\pm1}$ の出現、$\bar g_i\in W$ はその出現の左側接頭語の $W$-像、$\varepsilon_i=\pm1$ は指数。
>
> ⟹ $$\boxed{\ R_{N_E,N_W}^{-1}\bigl([m,\bar f]\bigr)\ \subseteq\ \{v\in V:\ A_{m,\bar f}\,v=b_{m,\bar f}\}\quad(\textbf{アフィン部分空間})\ }$$
> ($A$ は全条件の $A^\Phi$ を縦に積んだ行列、$b$ は $-\Phi(m,\bar f)_V$ を積んだベクトル。)

**証明**. $V\trianglelefteq E$ は可換正規部分群。$u,u'\in E$ を $u=v_u\bar u$、$u'=v_{u'}\bar u'$ と書くと
$$uu'=v_u\bar u v_{u'}\bar u'=\bigl(v_u+\rho(\bar u)v_{u'}\bigr)\,\overline{uu'},\qquad
u^{-1}=\bigl(-\rho(\bar u)^{-1}v_u\bigr)\,\bar u^{-1}.$$
すなわち $V$-成分は各因子の $V$-成分の **$\rho$-捻り線形結合**であり、$W$-成分には $v$ が現れない。語 $\Phi$ を左から右へ展開すると、$f$ の各出現の $V$-成分 $v$ に係数 $\varepsilon_i\rho(\bar g_i)$ が付き、$f$ 以外の因子は定数項に落ちる。∎

**計算コスト**: 語長 $\ell$ に対し $O(\ell)$ 回の $W$-積(次数 18 の置換)と $O(\ell)$ 回の $d\times d$ 行列積。**$\lvert E\rvert$ も $\lvert V\rvert$ も現れない。**

---

## 3. ★★ 定理 GEN-AFF — 生成条件も affine + 線形代数

shadow の生成条件は $\langle\,x^u,\ f^{-1}y^u f\,\rangle=E$($u=2m+1$)。

> ### 補題 GEN-1(生成元の $V$-成分は affine)
> $a:=x^u$($v$ に依存しない)、$b_v:=(v\bar f)^{-1}y^u(v\bar f)$ と置くと
> $$b_v=\Bigl[\rho(\bar f)^{-1}\bigl(\rho(\bar y_u)-1\bigr)v+\text{const}\Bigr]\cdot\bar b,\qquad \bar b=\bar f^{-1}\bar y_u\bar f .$$
> ⟹ $b_v$ の $V$-成分は $v$ について **affine**。

**証明**. $y^u=v_y\bar y_u$ と書き、$V$ 可換正規から
$v^{-1}v_y\bar y_u v=\bigl(-v+v_y+\rho(\bar y_u)v\bigr)\bar y_u$、さらに $\bar f$ で共役して $\rho(\bar f)^{-1}$ を掛ける。∎

> ### 定理 GEN-AFF
> $W=\langle\bar a,\bar b\rangle$(= $N_W$ 水準の生成条件・既知)とし、$W$ の有限表示の関係子を $R_1,\dots,R_s$ とする。$S_v:=\langle a,b_v\rangle\le E$ について:
> 1. 各 $R_j(a,b_v)\in V$ は $v$ について **affine**(補題 GEN-1 と定理 LIFT-AFF の展開規則)。
> 2. $S_v\cap V$ は $\{R_j(a,b_v)\}_j$ が生成する **$W$-部分加群**である。
> 3. ⟹ $$\boxed{\ S_v=E\iff \langle R_1(a,b_v),\dots,R_s(a,b_v)\rangle_{W\text{-mod}}=V\ }$$
>
> **とくに $V$ が半単純で既約成分が相異なるとき**($V=\bigoplus_{i=1}^{r}V_i$)、判定は「各 $V_i$-成分への射影が非零な $R_j$ が存在するか」に落ちる ⟹ **$r$ 回の射影と非零判定**のみ。

**証明**. (2): $S_v$ は $W$ へ全射(前提)なので $S_v\cap V$ は $S_v$-不変、したがって $W$-部分加群。関係子の像は $S_v\cap V$ に入り、逆に $S_v\cap V$ はそれらの $W$-加群閉包で尽きる(表示の関係子が $\ker(F_2\to W)$ を正規生成するため)。(3): $S_v\cap V=V\iff S_v=E$。∎

⟹ **生成条件も列挙なしに決まる。** ✓

---

## 4. ★★★ 測定の完全な帰着

$K:=K^{(9)}\cap N_E$、$M:=K^{(9)}\cap N_{S4}$($\lvert GT(M)\rvert=972$)。$\Theta_1=R_{K^{(9)},K^{(3)}}$ は $t_1$ の関数(**定理 vN-BIT**・機械確認: 全射・fibre 9)。

$$\boxed{\ (t_1,t_2)\in\mathrm{Im}\,R_{K,M}\iff \bigl(t_2,\Theta_1(t_1)\bigr)\in\mathrm{Im}\,R_{N_E,N_W}\ }$$

⟹ **SINGLE-BIT は「$GT(N_W)$ の 324 個の shadow のうち、どれが $N_E$ へ持ち上がるか」に完全に帰着する。**

### 測定アルゴリズム(擬似コード・$E$ 非実体化)

```
入力: rho: W -> GL_d(F_3)      … 生成元 2 個ぶんの d×d 行列(d = dim V)
      W                        … 次数 18 の置換群(P on 9 pts × G_3 on 9 pts)
      GT(N_S4) の 54 shadow, GT(K^(3)) の 12 shadow   … 既存 cert から
手順:
 1. GT(N_W) を貼り合わせで構成(324 個)         … 列挙は 324 のみ
 2. 各 t=[m, f̄] ∈ GT(N_W) について:
      a. hexagon 語を f = v·f̄ で展開し (A_t, b_t) を得る   … O(語長) の d×d 行列積
      b. A_t v = b_t を F_3 上で解く              … d×d の線形解
         解なし ⟹ t は持ち上がらない(記録して次へ)
      c. 解空間(アフィン)上で GEN-AFF の関係子値を評価し、
         W-部分加群が V 全体になる v が存在するか判定
         存在する ⟹ t は持ち上がる
 3. Im R_{N_E,N_W} ⊆ GT(N_W) を出力
 4. Θ_2 の rigidity: 各 t_2 ∈ GT(N_S4) について
      { k mod 3 : ∃ s ∈ GT(K^(3)), (t_2,s) ∈ Im R } の濃度を出す
      すべて 1 ⟹ rigid(発火)/ どれかが 3 ⟹ 自由(盲)
 5. |Im R_{K,M}| = #{(t_1,t_2) ∈ GT(M) : (t_2, Θ_1(t_1)) ∈ Im R}
```

**計算量**: $324\times O(\ell)$ 回の $d\times d$ 行列積 + $324$ 回の線形解。$d=21$ なら**ミリ秒**。**メモリは $O(d^2)$**。

---

## 5. コホモロジー的定式化(委嘱 2)

- $A_t$ は「捻り微分」であり、$\ker A_t$ は $t$ を固定する $V$-方向の変形 = **$Z^1$ 的**、$\mathrm{coker}\,A_t$ に住む $b_t$ の類が**持ち上げの障害**である:
  $$\boxed{\ t\ \text{が持ち上がる}\iff [\,b_t\,]=0\ \in\ \mathrm{coker}(A_t)\ }$$
- **非生成軌跡**は $V$ の複体 $S_v\cap V=0$ に対応し、$W$ の $V$ での**補群**にほかならない。補群の共役類は $H^1(W,V)$ で分類される ⟹
  $$\boxed{\ H^1(W,V)=0\ \Longrightarrow\ \text{非生成 }v\ \text{は高々 1 つの }V\text{-軌道}\ }$$
  ⟹ **[gating] $\dim H^1(P\times G_3,V)$ を先に測れ**(GAP `OneCohomology` / `CohomologyDimension`)。$0$ なら §4 手順 2c が 1 行で済む。
- ⟹ **rigidity ⟺ コホモロジー的条件**という要望への回答: **持ち上げ可否は $\mathrm{coker}(A_t)$ の 1 類で決まる**(完全にコホモロジー的)。ただし **rigidity 自体は $t$ を走らせた**「$k\bmod3$ の像の濃度」なので、324 個の障害類の**分布**を見る必要がある(1 個の不変量には潰れない)。**そこは正直に言う。**

---

## 6. ⚠⚠ 前件破綻の報告 — $\dim V=7$ は成立しない

### 6.1 機械測定(私・独立)

| 量 | 値 |
|---|---|
| $G_3^{\rm ab}$ | 位数 4・元の位数 $[1,2,2,2]$ ⟹ $\cong C_2\times C_2$ |
| $\theta,\tau$ は $G_3$ の自己同型か | **両方 true**(graph 検査) |
| $G_3$ の指数 2 部分群 | **3 個** |
| ★ **$\theta,\tau$ 両方に不変なもの** | ★ **0 個**(内訳: $\theta$ のみ不変 1・どちらも不変でない 2) |

### 6.2 帰結

$O_3(G_3)=[G_3,G_3]$(位数 27・純 3 群)ゆえ $\mathbf F_3[G_3]$ の既約加群は $G_3/O_3\cong C_2^2$ の既約 = **4 個の 1 次元指標**のみ。非自明は 3 個で、**$\tau$ がそれを巡回置換**する。⟹

> $$\boxed{\ \theta,\tau\textbf{-安定なテンソル型 }V\ \textbf{の最小次元は }\dim V_P\cdot 3\ \ge\ 7\cdot3=\mathbf{21}\ }$$
> $$\lvert E\rvert\ \ge\ 54{,}432\cdot3^{21}\ \approx\ 5.7\times10^{14}.$$

⚠ **これは便 128 と同じ失敗モードが加群水準で再演したものである**(単独では不変でない・$\tau$-軌道を束ねると不変)。**命題 ORBIT の二段目**。

### 6.3 ⟹ 委嘱 (3) への回答

$$\boxed{\ \textbf{「}10^8\ \textbf{規模の実体化」は不要ではなく}\textbf{不可能}\ \textbf{である}(5.7\times10^{14})\textbf{。GHA 大型 runner でも届かない。}\ }$$
$$\boxed{\ \textbf{compact 路(}\S2\text{–}\S4\textbf{)が}\textbf{唯一の路}\ \textbf{であり、しかもそれで十分に安い。}\ }$$

---

## 7. Sol 実装 spec

### 7.1 事前 gating(**測定前に全部通すこと**・false なら発車禁止)

| # | gating | 内容 | 失敗時 |
|---|---|---|---|
| **C-0** | $\theta,\tau$ の $P$ への作用 | **内部か外部か**を判定(`u_meas_m1_passport_v1.md` 定理 M1 は $\tau=\mathrm{Ad}(t)$・case A は内部)。**内部なら $V_P$ は自動で $\tau$-安定** | 外部なら $V_P$ も $\tau$-軌道束が必要 ⟹ $\dim V=7\cdot3\cdot3=63$、$\lvert E\rvert\approx 3^{63}$ ⟹ **停止** |
| **C-1** | $\mathbf F_3[P]$ の 7 次元既約の**個数**と $\mathrm{Out}(P)=C_3$ の作用 | `IrreducibleModules(P,GF(3))`。3 個を $C_3$ が巡回するなら C-0 と合わせて判定 | 同上 |
| **C-2** | $V=V_P\otimes(\chi_1\oplus\chi_2\oplus\chi_3)$、$\dim V=21$ の $\rho$ を **$21\times21$ 行列 2 枚**で構成 | $\rho(p,g)=\bigl(\chi_i(g)\rho_P(p)\bigr)_{i=1,2,3}$(block diagonal) | — |
| **C-3** | $N_E$ の $\theta,\tau$-不変性 | $E$ 上に $\theta,\tau$ が持ち上がるか($H^2$ の障害を含む)。**行列水準で検査**(元の列挙不要) | false ⟹ **窓でない・停止** |
| **C-4** | $N_E$ の isolated 性 | 命題 INT は使えない($N_E$ は交叉でない)⟹ **直接判定が要る**。⚠ compact 路で settled 判定を書けるか要設計 | UNKNOWN のまま測るなら格を落とす |
| **C-5** | $\lvert GT(N_W)\rvert=324$ の再現 | 独立実装で | 不一致 ⟹ 停止 |
| **C-6** | $\dim H^1(W,V)$ | §5(手順 2c の簡約) | 大きければ 2c を丁寧に |

### 7.2 cert schema `vnbit_compact/v1`(必須欄)

```
module        : { dim_V, rho_generators_sha256, V_P_dim, chi_orbit_size,
                  tensor_type_both_nontrivial: bool }
stability     : { theta_on_P: "inner"|"outer", tau_on_P: ..., 
                  chi_orbit_bundled: bool, N_E_theta_tau_invariant: bool }
roof          : { |GT(N_S4)|:54, |GT(K^(3))|:12, |GT(N_W)|:324, glue: "m mod 3" }
lift_table    : [ { t_index, m, rank_A, dim_ker_A, obstruction_zero: bool,
                    generating_solution_exists: bool, lifts: bool } × 324 ]
theta2        : { per_t2: [ { t2_index, k_values_realized: [...], count } × 54 ] ,
                  rigid: bool }
single_bit    : { |Im R_{K,M}|, in_{972,324}: bool }     ← 予言 P-vN-1 の検査
noncontact    : { u_touched:false, c_touched:false, sealed_k5_touched:false }
provenance    : { script_sha256, reproduce_command, helper_disjointness }
```

### 7.3 二系統

- producer: 上のアルゴリズム(行列 + 線形代数)
- checker: **helper 非共有**。$W$ を別表現(例: $P$ を $\mathbf F_8$ の $2\times2$ 行列、$G_3$ を $S_3^3$ の subdirect)で組み直し、$\rho$ も独立構成。**324 行の `lifts` bool を突合**。

---

## 8. 予言(prereg・走行前に凍結)

| # | 予言 | 根拠 |
|---|---|---|
| **P-vN-1**(再掲) | $\lvert\mathrm{Im}R_{K,M}\rvert\in\{972,324\}$ **のみ**。162/486 なら前件破綻 | 包含 (6)+$\lvert A_{\rm arith}\rvert=324$ |
| **P-vNC-1** | $\lvert GT(N_W)\rvert=\mathbf{324}$ | §1(私の機械計算) |
| **P-vNC-2** | 各 $t\in GT(N_W)$ の lift 集合はアフィン(空 or $3^{\dim\ker A_t}$ 個から非生成分を引いた形) | 定理 LIFT-AFF + GEN-AFF |
| **P-vNC-3** | $\Theta_1$(dihedral 側)は **rigid**($GT(K^{(9)})\to GT(K^{(3)})$ 全射・fibre 9) | 定理 vN-BIT・機械確認済 |
| **P-vNC-4**(★ 弱い見立て・当たり外れ両方を記録) | $\Theta_2$ は **rigid ではない**(= 盲)。**理由**: $V$ が 3 つの $\tau$-共役成分の直和なので、$k\bmod3$ を動かす方向が 3 つあり相殺しやすい。**外れれば発火 = 大収穫** | heuristic のみ。**証明ではない** |

---

## 9. novelty grep 領収書(★ **概念語彙**・自分の新規ファイルを除外した実測値)

| 主張 | grep(概念語彙) | ヒット | 判定 |
|---|---|---|---|
| 分裂屋根は検出しない | `SPLIT-NULL` | 279 | ★ 既出(依拠) |
| $\tau$-軌道束 | `τ-軌道` / `軌道機構` | 5 / 1 | ★ 既出(命題 ORBIT は私の v2)⟹ **加群水準への再演が増分** |
| **拡大の持ち上げを affine 化(元を列挙しない)** | `affine` + `cocycle` / `1-cocycle` / `Z^1` | 要検査 → **0**(shadow 文脈) | ★ **新規**(定理 LIFT-AFF / GEN-AFF) |
| **$E$ 非実体化での shadow 判定** | `実体化` / `非実体化` / `materiali` | **0** | ★ **新規** |
| **$\theta,\tau$ 不変な $\mathbf F_3[G_3]$ 加群が無い** | `F_3[G_3]` / `G_3^ab.*C_2` | **0** | ★ **新規**(§6・前件破綻の同定) |
| 補群と $H^1$ | `H^1` / `補群` | 多数 | ★ 既出(標準)— 引用扱い |

---

## 10. 検算(機械生成の数値の出所)

inline(本便)。すべて独立実装・Sol のコード非使用。

| 検査 | 出力 |
|---|---|
| $G_3^{\rm ab}$ | 位数 4・元の位数 $[1,2,2,2]$ ⟹ $C_2\times C_2$ |
| $\theta,\tau$ の自己同型性 | 両方 `true` |
| 指数 2 部分群 | **3 個**、$\theta,\tau$ 両不変は ★ **0 個** |
| $GT(K^{(3)})$ | 位数 12・$m\in\{0,2,3,5\}$・$k\in\{0,1,2\}$ |
| $GT(N_{S4})$ の charming $m$ | $\{0,2,3,5,6,8\}\subset\mathbf Z/9$ |
| ★ $\lvert GT(N_W)\rvert$ | **324** |
| $GT(K^{(9)})\to GT(K^{(3)})$ | 全射・fibre 9(前便) |

**格付け**: §6 の gating・§8 の P-vNC-1/3 = **機械・単系統**(Sol 未監査)。§2–§4 の定理 = **paper-proof**(単系統)。§5 のコホモロジー解釈 = **設計**。**verified ではない。** u/c・封印 3 量・prereg 非接触。

---

## 11. 司令塔への回答(4 行)

1. **委嘱 1 は YES**: **定理 LIFT-AFF**(hexagon の $V$-成分は $v$ に affine)+ **定理 GEN-AFF**(生成条件も affine + 部分加群判定)で、shadow 判定は**元の列挙なし**に $d\times d$ の $\mathbf F_3$ 線形代数へ落ちる。
2. **委嘱 2 も YES**: 測定は $\lvert GT(N_W)\rvert=\mathbf{324}$ 対の判定に完全帰着し、持ち上げ可否は $[\,b_t\,]\in\mathrm{coker}(A_t)$ という**コホモロジー的 1 類**で決まる。⚠ ただし **rigidity は 324 個の障害類の分布**なので、1 個の不変量には潰れない(正直に)。
3. ⚠⚠ **委嘱 3 の前提が崩れている**: $\theta,\tau$ 不変な非自明 $\mathbf F_3[G_3]$-加群は **0 個**(機械)⟹ $\dim V\ge21$ ⟹ $\lvert E\rvert\ge5.7\times10^{14}$。**実体化路は GHA でも不可能**。⟹ **compact 路が唯一の路**であり、それで十分に安い(ミリ秒)。
4. ★ **次の発車前に C-0/C-1(θ,τ の $P$ への作用が内部か)を必ず測ること** — 外部なら $\dim V=63$ で compact 路でも $63\times63$ になる(それでも走るが、$N_E$ の存在自体を疑うべき水準)。
