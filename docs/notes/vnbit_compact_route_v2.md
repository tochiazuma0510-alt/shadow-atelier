# vN-BIT compact route **v2** — C-3(標識付き全射)充填版

- 起草: 影工房 **数学者**(Claude / Opus 5)/ 2026-08-13
- 委嘱: 司令塔(裁定 1153)「(1) 標識付き全射の指定 (2) $W$ の有限表示と GEN-AFF 用関係子列 (3) $A$ の型」
- **関連既存定理(委嘱様式)**: **LIFT-AFF / GEN-AFF**(`vnbit_compact_route_v1.md` §2–3)/ **BU-S35 §26・§43・§61**(`bu_s35_embedding_v1.md`: $\Delta=\sigma_1\sigma_2\sigma_1$, $\delta=\sigma_1\sigma_2$, $c=\Delta^2$, $\theta=\mathrm{Ad}(\Delta)$, $\tau=\mathrm{Ad}(\delta)$)/ **D-1** / **SPLIT-NULL″** / 正典 **Cor 5.4**
- v1 は**不改変**(versioned 規律)。本稿は C-3 入力を充填する。
- **規律**: u/c 非接触・封印 3 量非接触・prereg 非抵触。数値は機械生成(§8)。**novelty 表は grep 出力のコピーのみ**(規律 GREP-3)。

---

## 0. 結論(先に 4 行)

1. ★★★ **C-3 は $(\Delta,\delta)$ 標識に切り替えれば自動的に閉じる**。`bu_s35_embedding_v1.md` §61 の逐語 $\theta=\mathrm{Ad}(\Delta),\ \tau=\mathrm{Ad}(\delta)$ より、$B_3$ からの標識付き全射を使えば **$N_E$ の $\theta,\tau$-不変性は内部自己同型として自動**。⟹ 「$\theta,\tau$ 不変な核が取れるか」という懸案そのものが消える。
2. ★ **81 類の分類は 1 回の線形計算で終わる**(定理 SURJ-LIN):
   $$\boxed{\ \#\{\text{全射を与える類}\}\ =\ 81-\bigl\lvert H^1(\bar W,V)\bigr\rvert\ }$$
   非全射類は $Z^1(\bar W,V)$ の inflation 像 = **$\mathbf F_3^{25}$ の線形部分空間**。⟹ 81 回の**所属判定**のみ。
3. ★ **核同一性は分類しない**。$\le81$ 類 × 324 行 $=\le26{,}244$ 回の線形解は依然自明 ⟹ **全類を測って分布を出す**(族全体の答えが出るので科学的にも上位)。
4. **$A$ は $42\times21$ のまま仕様化**。21×21 への縮約は(i) コスト上不要 (ii) 誤縮約は**制約の取りこぼし = 偽陽性**という危険な向き((3.60) 事故と同型) (iii) 2 本の hexagon は $\theta$-共役で **rank は一致するが行は独立**でありうる。⟹ 整合検査 `rank(A₁)==rank(A₂)` を cert 欄に。

---

## 1. 委嘱 1 — 標識付き全射の指定

### 1.1 ★★★ 定理 MARK($\theta,\tau$-不変性が自動になる)

> ### 定理 MARK
> $\Delta:=\sigma_1\sigma_2\sigma_1$, $\delta:=\sigma_1\sigma_2$, $c:=\Delta^2=\delta^3$(中心)とすると(**BU-S35 §43 逐語**)
> $$B_3=\langle\Delta,\delta\mid\Delta^2=\delta^3\rangle,\qquad B_3/\langle c\rangle\cong C_2*C_3=\mathrm{PSL}(2,\mathbf Z).$$
> $c\in N_E$ なる窓に対し $\tilde E:=B_3/N_E$ は $C_2*C_3$ の商であり、**標識付き全射とは**
> $$\boxed{\ \bigl(U,S\bigr)\in\tilde E^2,\quad U^2=S^3=1,\quad \langle U,S\rangle=\tilde E\ }$$
> **に他ならない**($U=\bar\Delta$, $S=\bar\delta$)。
>
> ★ さらに **BU-S35 §61 逐語**「$\theta:=\mathrm{Ad}(\Delta),\ \tau:=\mathrm{Ad}(\delta)$」より、$\theta,\tau$ は $\tilde E$ 上 $\mathrm{Ad}(U),\mathrm{Ad}(S)$ として実現される。⟹
> $$\boxed{\ N_E=\ker(B_3\to\tilde E)\ \textbf{は }B_3\textbf{-正規ゆえ }\theta,\tau\textbf{-不変が}\textbf{自動}\ }$$

**⟹ 委嘱 1 の本体は「不変核が取れるか」ではなく「$U^2=S^3=1$ を満たす生成対を取れるか」に変わる。** これは §1.3 の線形問題である。

⚠ **前件 C-3′**: $c\in N_E$(中心が核に入る)。これは $\tilde E$ の中で $U^2=S^3$ が $1$ になることと同値であり、**設計として課す**(すべての既存窓が満たす — 定義ノート $\mathrm{NFI}_{PB_3}(B_3)$)。cert に `center_in_kernel: true` を必須欄に。

### 1.2 $Z^1$ の構造 — Sol の生値 11 / 14 / 4 の**独立な構造確認**

$C_2*C_3$ の $V$ 係数 1-cocycle は各因子上の cocycle 条件だけで決まる:
$$Z^1(C_2*C_3,V)=\ker(I+\theta)\ \oplus\ \ker(I+\tau+\tau^2),\qquad \theta:=\rho(U),\ \tau:=\rho(S).$$

★ **私の独立確認(機械・§8)**: $\tau$ は $V=V_7\otimes(\chi_1\oplus\chi_2\oplus\chi_3)$ の **3 ブロック(各 7 次元)を巡回**する。$\mathbf F_3$ 上 $1+x+x^2=(x-1)^2$ ゆえ
$$\mathrm{rank}(I+\tau+\tau^2)=\mathbf 7\ \Longrightarrow\ \dim\ker(I+\tau+\tau^2)=21-7=\mathbf{14}\quad\checkmark\ \text{(Sol と一致・構造から必然)}$$
$\theta$ は 1 ブロック固定 + 2 ブロック交換 ⟹ 交換部の寄与 $7$ + 固定ブロック上の $(-1)$-固有空間 $\dim=4$ で $\mathbf{11}$ ✓(Sol と一致)。

$$\dim Z^1=11+14=25,\qquad \dim B^1=21-\dim V^{\bar W}=21\ (V\ \text{は非自明既約}),\qquad \dim H^1=\mathbf 4,\ \lvert H^1\rvert=3^4=\mathbf{81}\ \checkmark$$

### 1.3 ★★ 定理 SURJ-LIN — 全射類の分類は**線形**

> ### 補題 IRR
> $V=V_1'\oplus V_2'\oplus V_3'$($V_i'=V_7\otimes\chi_i$)は $W$-加群として**相異なる 3 既約の直和**、かつ $\bar W/W$($\cong$ 外側 $S_3$ の像)は 3 成分を**推移置換**する。⟹ **$V$ は $\bar W$-既約**(Clifford)。
>
> ### 定理 SURJ-LIN
> $(a,b)\in Z^1(C_2*C_3,V)$ に対し $S_{(a,b)}:=\langle aU,\ bS\rangle\le\tilde E$ と置く。
> 1. $S_{(a,b)}\cap V$ は $\bar W$-部分加群(§v1 定理 GEN-AFF (2))⟹ 補題 IRR より $\in\{0,V\}$。
> 2. $S_{(a,b)}=\tilde E\iff S_{(a,b)}\cap V\ne0\iff (a,b)\notin \mathrm{infl}\bigl(Z^1(\bar W,V)\bigr)$。
> 3. inflation $H^1(\bar W,V)\hookrightarrow H^1(C_2*C_3,V)$ は**単射**($V$ 上 $\ker(C_2*C_3\to\bar W)$ は自明作用)。⟹
> $$\boxed{\ \#\{\text{全射を与える }H^1\text{-類}\}=81-\bigl\lvert H^1(\bar W,V)\bigr\rvert\ }$$
> とくに $H^1(\bar W,V)=0$ なら **80 類が全射**(零類だけが非全射)。

**⟹ 委嘱 1 の答え**: 分類は **$Z^1(\bar W,V)\subseteq\mathbf F_3^{25}$ を 1 回計算**すれば終わる。以後は 81 回の**線形部分空間への所属判定**(各 $O(25^2)$)。**紙で決まる部分は上の 3 段、機械が要るのは $Z^1(\bar W,V)$ の 1 回計算のみ。**

### 1.4 ★ 核同一性 — 分類せず**全類を測る**

異なる $H^1$-類は異なる窓 $N_E$ を与えうるので、**$\lvert\mathrm{Im}R\rvert$ が類に依存する可能性がある**。核同一性の分類($\mathrm{Aut}(\tilde E)$ 作用での商)は非自明だが、

$$\le81\ \text{類}\times324\ \text{行}=\le26{,}244\ \text{回の}\ 42\times21\ \mathbf F_3\ \text{消去}\ \approx\ 5\times10^8\ \text{基本演算}$$

⟹ **numpy(mod 3)で数秒**。⟹

$$\boxed{\ \textbf{推薦}:\ \textbf{分類しない。全射類を}\textbf{全部測り}\textbf{、}\lvert\mathrm{Im}R\rvert\ \textbf{の分布を報告する。}\ }$$

**anchor 正規化の役割**: 代表選択のためではなく**再現性のため**に使う。$Z^1$ の基底を固定し、辞書式最小の類を `canonical_class` として cert に記録する(異なる走行が同じ類を指すことの保証)。

---

## 2. 委嘱 2 — $W$ の有限表示は**不要**

### 2.1 ★ 部分空間路(第一選択)

GEN-AFF が要求するのは「関係子列」ではなく、**$S\cap V=0$ の判定**である。定理 SURJ-LIN 2. により、それは
$$(a,b)\in\mathrm{infl}\bigl(Z^1(\bar W,V)\bigr)\subseteq Z^1(C_2*C_3,V)=\mathbf F_3^{25}$$
という**線形部分空間への所属**にすぎない。⟹

> ### 仕様 GEN-SUB
> ```
> 1 回だけ:  Zbar := OneCocycles( barW, GModuleByMats(rho_gens, GF(3)) )   # GAP
>            infl := Zbar を Z^1(C_2*C_3,V) = F_3^25 の部分空間として表現
> 以後:      (a,b) が全射を与える  ⟺  (a,b) ∉ infl        # O(25^2) の所属判定
> ```
> $\lvert\bar W\rvert=6\cdot54{,}432=\mathbf{326{,}592}$、$\dim V=21$ ⟹ GAP の `OneCocycles` の射程内。

### 2.2 表示路(fallback・第一選択が失敗したときのみ)

$\bar W$ を $C_2*C_3$ の商として提示する必要が生じた場合:
```
F := FreeGroup("U","S");;  rel := [ U^2, S^3 ];;
hom := GroupHomomorphismByImages( F/rel, barW, [U,S] );;
P := PresentationViaCosetTable( barW, ... );;   # index 326,592 — GAP で可能だが不要
```
⚠ **関係子列を手で固定しない**(私が書けば誤る危険がある型・6 度の型境界事故の教訓)。**機械が出したものを cert に digest 束縛せよ。**

### 2.3 ⚠ $W=P\times G_3$ の直積表示について

委嘱文は「$W=P\times G_3$ の有限表示」を求めたが、**我々が使う標識は $(\Delta,\delta)$ であって $(P\text{-生成元},G_3\text{-生成元})$ ではない**。直積表示(各因子の表示 + 交換子)は $(\Delta,\delta)$ 標識に**直接は接続しない**。⟹ **§2.1 の部分空間路を採れば、そもそも表示が要らない。**(これも「型を確認してから輸入する」規律の適用。)

---

## 3. 委嘱 3 — $A$ の型は **42×21 のまま**

| 論点 | 判定 |
|---|---|
| **コスト** | $42\times21$ の $\mathbf F_3$ 消去 $=O(21^2\cdot42)\approx1.9\times10^4$ 演算。$\times324\times81\approx5\times10^8$ ⟹ **numpy で数秒**。縮約の動機が無い |
| **安全性** | ★ 誤った従属性証明は**制約の取りこぼし** ⟹ **偽陽性**(「324 なのに 972」ではなく「972 なのに 324」— **発火の偽陽性**という最悪の向き)。**(3.60) 事故と同型**。⟹ **縮約しない** |
| **構造** | 2 本の hexagon (3.11)/(3.12) は $\theta=\mathrm{Ad}(\Delta)$ で移り合う ⟹ $A^{(2)}$ は $A^{(1)}$ の**共役**。⟹ $\mathrm{rank}(A^{(1)})=\mathrm{rank}(A^{(2)})$ は**従うが**、両者の行が張る空間が一致するとは**限らない** ⟹ 一般に $21\times21$ には落ちない |

> ### 仕様 A-42
> - $A_t\in\mathrm{Mat}_{42\times21}(\mathbf F_3)$、$b_t\in\mathbf F_3^{42}$ のまま解く。
> - **整合検査(必須 cert 欄)**: `rank_A1 == rank_A2`(θ-共役の帰結)。**破れたら実装バグ ⟹ 即停止**。
> - `rank_A`, `dim_ker_A`, `consistent`(= $b_t\in\mathrm{Im}A_t$)を 324 行すべてに記録。

---

## 4. 完全な測定アルゴリズム(v1 §4 の C-3 充填版)

```
入力:
  rho_P : P の 7 次元 F_3 既約(生成元 2 枚の 7x7 行列)         … C-1 で一意確定
  chi_i : G_3 -> {±1} ⊂ F_3^x  (i=1,2,3, τ-軌道)
  rho   : W̄ -> GL_21(F_3),  block-diagonal ⊕_i (V_7 ⊗ χ_i) + 外側 S_3 のブロック置換
  W̄     : 次数 18+? の置換群(|W̄| = 326,592)、標識 (U,S) with U^2=S^3=1
  GT(N_S4) 54 shadow, GT(K^(3)) 12 shadow                     … 既存 cert

段 0(1 回): Zbar := OneCocycles(W̄, V) を計算し infl ⊆ F_3^25 を得る    … 仕様 GEN-SUB
            surj_classes := { H^1 類 } \ infl                          … |surj| = 81 - |H^1(W̄,V)|
            予言 P-vNC2-1 の検査

段 1(1 回): GT(N_W) を貼り合わせで構成(324 個)                        … P-vNC1 の再現

段 2(類ごと・|surj| ≤ 81 回):
  類代表 (a,b) から標識付き全射 B_3 ↠ Ẽ を固定
  各 t = [m, f̄] ∈ GT(N_W) (324 行):
     a. hexagon 語を f = v·f̄ で展開し (A_t, b_t) ∈ F_3^{42x21} × F_3^42   … 定理 LIFT-AFF
     b. rank/consistency 判定 → 解空間(アフィン)
        非整合 ⟹ t は持ち上がらない
     c. 解空間上で GEN-AFF: S_v ∩ V ≠ 0 となる v が存在するか
        (補題 IRR より二値。解空間はアフィンなので「全部が非全射」なら空、でなければ存在)
     d. lifts[t] を記録
  Im R_{N_E,N_W} を出力

段 3: Θ_2 rigidity: 各 t_2 ∈ GT(N_S4) について
        #{ k mod 3 : ∃ s ∈ GT(K^(3)), (t_2,s) ∈ Im R } を出す
      すべて 1 ⟹ rigid(発火)/ どれかが 3 ⟹ 自由(盲)
段 4: |Im R_{K,M}| = #{(t_1,t_2) ∈ GT(M) : (t_2, Θ_1(t_1)) ∈ Im R}     … P-vN-1 の検査
段 5: 類ごとの |Im R| の分布を報告                                       … P-vNC2-4 の検査
```

---

## 5. gating 追補と cert schema

### 5.1 gating(v1 §7.1 に追加)

| # | gating | 内容 | 失敗時 |
|---|---|---|---|
| **C-3′** | `center_in_kernel` | $c=\Delta^2=\delta^3\in N_E$(⟺ $\tilde E$ で $U^2=S^3=1$) | 定理 MARK の前提が崩れる ⟹ 停止 |
| **C-7** | $\lvert H^1(\bar W,V)\rvert$ | 段 0。全射類の個数を確定 | $=81$ なら全射類ゼロ ⟹ **窓が作れない ⟹ 停止・報告** |
| **C-8** | 補題 IRR の確認 | $V$ が $\bar W$-既約(3 成分が非同型・外側が推移) | 可約なら $S\cap V$ が二値でない ⟹ 段 2c を部分加群格子で書き直す |
| **C-4′** | isolated 性 | ★ **走行の入口条件にしない**(下記) | — |

### 5.2 ★ C-4(isolated)の扱い — **走行を止めない**

- 包含 (6)($A_{\rm arith}\subseteq\mathcal{PR}_M(\widehat{GT}_{\rm gen})\subseteq\mathrm{Im}R$)の証明は $\mathcal{PR}_M=R_{K,M}\circ\mathcal{PR}_K$ **だけ**を使う ⟹ **isolated 性は不要**。
- $\lvert\mathrm{Im}R\rvert$ は**集合の濃度**なので群構造なしに測れる。
- isolated 性が要るのは「$\lvert\mathrm{Im}R\rvert=324\Rightarrow\mathrm{Im}R=A_{\rm arith}$」(指数 3 素数の二択 = DICHOTOMY-972)の段のみ。
$$\boxed{\ \textbf{仕様}:\ \textbf{isolated 未確認でも測定は走らせる。}\ \mathbf{324}\ \textbf{が出た場合にのみ isolated 性の証明が入口条件になる。}\ }$$
⚠ **$N_E$ の isolated 性を compact 路で判定する方法は本稿では書けていない**(settled 判定は $\ker T_{m,f}=N_E$ の一致判定を要し、$N_E$ の正規生成元が $3^{21}\cdot326{,}592$ 指数で取れない)。⟹ **【vNB-GAP-1】として登録**。

### 5.3 cert schema `vnbit_compact/v2`(v1 §7.2 への差分)

```
marking       : { presentation: "B_3 = <Delta,delta | Delta^2=delta^3>",
                  center_in_kernel: true, U_order: 2, S_order: 3,
                  Z1_dim: 25, ker_I_plus_theta: 11, ker_norm_C3: 14,
                  H1_C2C3_dim: 4, H1_classes: 81 }
surjectivity  : { H1_barW_order, surjective_class_count,          # = 81 - |H^1(W̄,V)|
                  canonical_class_index, class_enumeration: [...] }
A_shape       : { rows: 42, cols: 21, rank_A1, rank_A2,
                  rank_A1_equals_rank_A2: true }                  # ★整合検査
per_class     : [ { class_index, lift_table: [...324], theta2_rigid: bool,
                    Im_R_size } × surjective_class_count ]
isolated      : { N_E_isolated: "UNKNOWN", gate_policy: "measure anyway (C-4′)" }
```

---

## 6. 予言(prereg・走行前に凍結)

| # | 予言 | 根拠 |
|---|---|---|
| **P-vNC2-1** | 全射類の個数 $=81-\lvert H^1(\bar W,V)\rvert$ | 定理 SURJ-LIN |
| **P-vNC2-2** | 全 324 行で $\mathrm{rank}(A^{(1)})=\mathrm{rank}(A^{(2)})$ | $\theta$-共役 |
| **P-vNC2-3** | $\lvert\mathrm{Im}R_{K,M}\rvert\in\{972,324\}$(P-vN-1 再掲) | 包含 (6) + $\lvert A_{\rm arith}\rvert=324$ |
| **P-vNC2-4**(★ 弱い見立て) | **全ての全射類が同じ $\lvert\mathrm{Im}R\rvert$ を与える**。外れたら「窓の選択が答えを変える」= 重要な発見 | heuristic のみ。**証明ではない** |
| **P-vNC2-5**(★ 弱い見立て・v1 P-vNC-4 再掲) | $\Theta_2$ は **rigid でない**(= 盲)。外れれば発火 = 大収穫 | heuristic のみ |

---

## 7. novelty grep 領収書(★ 規律 GREP-3: **実行後にコピー**・自分の新規ファイル除外)

```
$ grep -rn "Delta, *delta|(\Delta,\delta)|Delta.*delta.*marking" docs/ sol/ | grep -v vnbit_compact | wc -l
2      → bu_s35_embedding_v1.md §26, §43  ★既出(依拠・逐語引用)
$ grep -rn "C_2 \* C_3|C_2\*C_3|PSL(2,Z)|自由積" docs/ sol/ | grep -v vnbit_compact | wc -l
55     → ★既出(多数)
$ grep -rn "OneCocycles|Z\^1(W|1-cocycle.*window" docs/ sol/ | grep -v vnbit_compact | wc -l
0      → ★新規(仕様 GEN-SUB・定理 SURJ-LIN)
$ grep -rn "標識付き全射|marked surjection" docs/ sol/ | grep -v vnbit_compact | wc -l
1      → sol_reply_130(本委嘱の入力)
$ grep -rn "42x21|42 x 21|従属性" docs/ sol/ | grep -v vnbit_compact | wc -l
5      → 一般文脈のみ(本件の A の型ではない)
$ grep -rn "H\^1(\bar W|全射類|surjective class" docs/ sol/ | grep -v vnbit_compact | wc -l
2      → sol_reply_130 の生値
```

| 主張 | 判定 |
|---|---|
| $(\Delta,\delta)$ 標識・$\theta=\mathrm{Ad}(\Delta)$・$\tau=\mathrm{Ad}(\delta)$ | ★ **既出**(BU-S35 §26/43/61)— **依拠・引用** |
| $B_3/\langle c\rangle=C_2*C_3$ | ★ **既出**(55 件) |
| **定理 MARK($\theta,\tau$ 不変性が自動)** | 上 2 つの**合成**。合成自体の記述は grep 0 ⟹ ★ **本稿の増分**(小) |
| **定理 SURJ-LIN(全射類 $=81-\lvert H^1(\bar W,V)\rvert$)** | grep 0 ⟹ ★ **新規** |
| **仕様 GEN-SUB(表示不要・部分空間所属判定)** | grep 0 ⟹ ★ **新規** |
| $Z^1$ の 11/14/4 | ★ **Sol の生値**(便 130)。本稿は**構造的な独立確認**のみ(§1.2) |
| 仕様 A-42(縮約しない判断) | 判断であって定理ではない ⟹ **設計** |

---

## 8. 検算(機械生成の数値の出所)

inline(本便)。Sol のコード非使用・標準ライブラリのみ。

| 検査 | 出力 |
|---|---|
| $\tau$ = 3 ブロック(各 7 次元)巡回のとき | $\mathrm{rank}(I+\tau+\tau^2)=\mathbf 7$、$\dim\ker=\mathbf{14}$ ⟹ **Sol の 14 と一致** |
| $\theta$ の内訳 | 交換部の寄与 $7$ + 固定ブロックの $(-1)$-固有空間 $4$ $=\mathbf{11}$(Sol と一致) |
| $H^1$ の勘定 | $\dim Z^1=25$, $\dim B^1=21$, $\dim H^1=\mathbf4$, $\lvert H^1\rvert=3^4=\mathbf{81}$ |
| $\lvert\bar W\rvert$ | $6\times54{,}432=\mathbf{326{,}592}$ |
| 段 2 の総コスト | $324\times81=26{,}244$ 回の $42\times21$ 消去 $\approx5\times10^8$ 基本演算 |

**格付け**: §1.2 の構造確認 = **機械・単系統**。定理 MARK / SURJ-LIN / 補題 IRR = **paper-proof(単系統・Sol 未監査)**。§3・§5 = **設計**。**verified ではない。** u/c・封印 3 量・prereg 非接触。

---

## 9. 司令塔への回答(4 行)

1. **委嘱 1**: $(\Delta,\delta)$ 標識に切り替えれば **$\theta,\tau$-不変性は自動**(定理 MARK・BU-S35 §61 に依拠)。81 類の分類は **$\#\{\text{全射}\}=81-\lvert H^1(\bar W,V)\rvert$**(定理 SURJ-LIN)で、機械が要るのは $Z^1(\bar W,V)$ の **1 回**の計算のみ。**核同一性は分類せず、全射類を全部測る**(≤81×324 = 数秒)。
2. **委嘱 2**: **有限表示は要らない**(仕様 GEN-SUB — 部分空間所属判定に置換)。⚠ 委嘱文の「$W=P\times G_3$ の表示」は $(\Delta,\delta)$ 標識に接続しないので**採らない**(型の確認)。関係子列を手で固定することは**禁止**(機械出力を digest 束縛)。
3. **委嘱 3**: **$42\times21$ のまま**。縮約はコスト上不要・誤縮約は**発火の偽陽性**という最悪の向き。整合検査 `rank(A₁)==rank(A₂)` を必須欄に。
4. ⚠ **新規 GAP を 1 本登録**: 【**vNB-GAP-1**】$N_E$ の **isolated 性を compact 路で判定する方法が書けていない**。⟹ **C-4′ として「isolated 未確認でも測定を走らせる。324 が出た場合にのみ入口条件になる」**という運用を提案(掃討教義に整合)。Sol はこれで事前登録 → 324 行へ直行できる。
