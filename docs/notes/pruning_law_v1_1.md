# 刈り込み処方 — v1 追補(裁定 227 / 便 86 P86-7 反映)**v1.1**

- 起草: 影工房 数学者(Claude)/ 2026-07-30
- 位置づけ: **`docs/notes/pruning_law_v1.md` の追補**。v1 は不変(上書きしない)。本稿が erratum + 格付けの正本。
- 入力: `sol/sol_reply_86_math13.md` §4.2(F86-4.2.2〜4.2.5・P86-7)/ 裁定 220/227
- 状態: **candidate**。本稿は主張の**格下げ・分離・次段設計**であって新しい律を立てない(§3 の補題 NORM-E を除く)。

---

## 1. 【正式撤回】無修飾 $\ell^{r-1}$ 律

> ### 撤回記帳 R-PRUNE-1
> **「核の奇部の位数 $=\ell^{\,r-1}$」という無修飾の律を撤回する。**
> **反例**: $r=1$。既測値は $\ell$(A16 の $C_{11}$・A18 の $C_{13}$・A20 の $C_{15}$)であって $\ell^{0}=1$ ではない。
> 出所: 私の v1 §3.5 の指摘と、Sol F86-4.2.2-3 の独立認定が一致。裁定 220 §帰結 2 の「$5^{r-1}$ 律(candidate)」はここで**失効**する。

**付随して撤回する読み**:
- 「$r\ge2$ 限定版なら生きる」も**採らない**。$r=2,3$ の**二点補間**にすぎず(Sol F86-4.2.2-3)、独立な支持がない。
- v1 §3.5 の表で $\ell^{r-1}$ 行を「対抗仮説」として残したのは、**$r=4$ 判別の対抗値を明示するため**であり、生きた候補としてではない。v1.1 ではその役割に限定する。

**v1 の結果への影響**: なし。v1 の同定(§2)・PRUNE の主張(§3.1)・導出(§4)はいずれも $\ell^{r-1}$ に依存していない。撤回対象は裁定 220 が提案した中間 candidate である。

---

## 2. 【格付け】$\ell^{s_2(r)}$ 律と Stab 律は candidate のまま

> ### 格付け G-PRUNE-1
> 次の 2 つは **candidate(予想)**であり、定理でも cross-checked でもない。
> - **PRUNE**(v1 §3.1): $\ \Xi(\ker\widetilde\chi)=C_{O_{2'}(\mathrm{Stab})}(S)\times S$、$S=\mathrm{Syl}_2(\mathrm{Stab})$。
> - **系 PRUNE-1**(v1 §3.5): 奇部の位数 $=\ell^{\,s_2(r)}$($s_2$ = 2 進桁和)。
> - **Stab 律**(2-部 $=\mathrm{Syl}_2(\mathrm{Stab})$): Sol F86-4.2.2-4 のとおり **candidate**。$t=0$ で 2-部 $=C_2$ が出たので「尾部だけではない」ことは確定したが、一般則は未証明。

**未証明の中身(v1 §4.3 の再掲・強調)**:
$$\underbrace{\Xi(\ker)\subseteq C_{O_{2'}}(S)\times S}_{\text{v1 §4.2 で既測 2 事実から従う}}\qquad\text{vs}\qquad
\underbrace{\Xi(\ker)\supseteq C_{O_{2'}}(S)\times S}_{\textbf{飽和 — 未証明}}$$

> ### 明示: 飽和(saturation)は証明されていない
> $\supseteq$ は「$C_{O_{2'}(\mathrm{Stab})}(S)$ の**すべての**元が実際に shadow として実現する」という**存在主張**である。現状これを支える材料は
> (i) 16 標本の一致(うち実測は 12)、(ii) 【GAP-PR-1】で名指しした未構成の補題、
> の 2 つしかない。**$r\ge4$ では一度も検証されていない**。
> Sol F86-4.2.2-3 の「一般的な飽和方向は未証明であり本便では定理認定しない」を全面的に受け入れる。

**したがって v1 §3.1 の枠囲みは「予想 PRUNE」の札のまま**であり、v1 §3.4 の「STR-2 の一般化」も**予想の帰結**であって定理ではない。v1 §0 の表で「② 律の形」に付けた枠囲みは、格として candidate であることを本稿で明記する。

---

## 3. 【分離】NORM: order-divisibility と structural-embedding

Sol F86-4.2.3 / ★4(「Lagrange は embedding certificate ではない」)を受け、NORM の status を二分する。

| 主張 | status |
|---|---|
| `NORM-order-divisibility`: $\lvert\mathrm{GTSh}\rvert\ \bigm|\ \lvert N_{S_n}(\langle\bar x\rangle)\rvert$ | **PASS**(両窓・driver 欄 16) |
| `NORM-structural-embedding`: $\mathrm{GTSh}\hookrightarrow N_{S_n}(\langle\bar x\rangle)$(marking と作用を保つ) | 便 86 時点 **UNKNOWN** → **§3.3 の測定で 9 窓 PASS(machine-measured)** |

**「NORM 包絡生存」を Lagrange だけで主張しない**(★4)。i10_1_prediction_v1.md §6 の `P-I10-10` の判定文(「NORM は包絡として生存」)は、**order-divisibility に限った PASS** と読み替え、structural-embedding は §3.3 の証明書を根拠として別に記帳する。

### 3.1 PRUNE の主張文への反映(v1 §3.1 の書き換え)

v1 §3.1 は $\Xi(\ker\widetilde\chi)=\mathrm{Pr}(\mathrm{Stab})$ と書いた。これは **$\Xi$ が単射でなければ「$\ker\widetilde\chi\cong\mathrm{Pr}(\mathrm{Stab})$」を意味しない**。正確には二段に分ける:

> ### 主張 PRUNE(v1.1 の正確形)
> **(P-a) 像の主張**: $\Xi\bigl(\ker\widetilde\chi\bigr)=C_{O_{2'}(\mathrm{Stab})}(S)\times S$(部分群として)。
> **(P-b) 同型の主張**: $\ker\widetilde\chi\cong C_{O_{2'}(\mathrm{Stab})}(S)\times S$。
> **(P-b) は (P-a) $+$ $\ker\Xi\cap\ker\widetilde\chi=1$ を要する。** 後者は I10-1 の 2 窓で実測($\alpha$ が 50 個 / 10 個で相異なる・v1 §2.1)だが、一般には未証明(監査 §7.1 の観測)。

### 3.2 【本稿の寄与】補題 NORM-E — 埋め込みは核上の単射性に帰着する

> ### 補題 NORM-E(埋め込みの判定を $\ker\widetilde\chi$ 上へ落とす)
> charming 窓で $\gcd(2m+1,N_{\rm ord})=1$ ゆえ $E_{m,f}(\bar x)=\bar x^{2m+1}$ は $\langle\bar x\rangle$ を保つ。よって
> $$\Xi:\ \mathrm{GTSh}(N,N)\longrightarrow N_{\mathrm{Aut}(P)}(\langle\bar x\rangle),\qquad [m,f]\mapsto E_{m,f}$$
> は well-defined(命題 3.1 の議論)。$\mathrm{pr}:N_{\mathrm{Aut}(P)}(\langle\bar x\rangle)\to\mathrm{Aut}(\langle\bar x\rangle)\cong(\mathbf Z/N_{\rm ord})^\times$ を自然な射影とすると
> $$\mathrm{pr}\circ\Xi=\widetilde\chi$$
> ($\mathrm{pr}(E_{m,f})$ は $\bar x\mapsto\bar x^{2m+1}$ の指数 $=2m+1\bmod N_{\rm ord}=\chi_{\rm vir}$)。ゆえに
> $$\boxed{\ \ker\Xi\ \subseteq\ \ker\widetilde\chi\qquad\Longrightarrow\qquad
> \bigl(\Xi|_{\ker\widetilde\chi}\ \text{単射}\bigr)\ \Longrightarrow\ \bigl(\Xi\ \text{が}\ \mathrm{GTSh}\ \text{上単射}\bigr).\ }$$

**証明.** $\mathrm{pr}\circ\Xi=\widetilde\chi$ より $\ker\Xi\subseteq\ker(\mathrm{pr}\circ\Xi)=\ker\widetilde\chi$。$\Xi$ の $\ker\widetilde\chi$ への制限が単射なら $\ker\Xi=\ker\Xi\cap\ker\widetilde\chi=1$。∎

**効用**: `NORM-structural-embedding` の検査コストが **$\lvert\mathrm{GTSh}\rvert$ から $\lvert\ker\widetilde\chi\rvert$ 層($m=0$ の 1 層のみ)へ落ちる**。charming 層が $c_m$ 本あるので $1/c_m$($N_{\rm ord}=5$ で 1/4、$=9$ で 1/6、$=11$ で 1/10)。
**射程**: 補題は $\Xi$ が準同型であることに依存する(合成則 (3.53) の $E$ の乗法性)。**この乗法性は正典の帰結だが、実装規約(左右どちらの積か)は測定で確かめるべき** — §4 の測定でそこも見る。

### 3.3 測定(P86-7-1 の実装)— **9/9 PASS**

- スクリプト: `search/probe/wac_v1/norm_embedding.g`
- 証明書: `search/certs/norm_embedding_20260731.json`(schema `norm-embedding/v1`)
- 写像: $\Xi:[m,f]\mapsto\alpha$、$\alpha$ は $\bar x^\alpha=\bar x^{2m+1}$ かつ $\bar y^\alpha=(\bar y^{2m+1})^f$ を満たす $S_n$ の**一意の**元。

| 窓 | $\lvert\mathrm{GTSh}\rvert$ | $\lvert\ker\widetilde\chi\rvert$ | $\alpha$ 一意 | hom(左) | hom(右) | $\ker\Xi=1$ | $\lvert\mathrm{im}\rvert$ | $\mathrm{im}\le N_{S_n}(\langle\bar x\rangle)$ | $\lvert\mathrm{im}\rvert=\lvert\mathrm{GTSh}\rvert$ |
|---|---|---|---|---|---|---|---|---|---|
| W-E-A10-9t1 | 54 | 9 | ✓ | ✗ | ✓ | ✓ | 54 | ✓ | ✓ |
| W-E-A11-9t2 | 108 | 18 | ✓ | ✗ | ✓ | ✓ | 108 | ✓ | ✓ |
| W-E-A12-9t3 | 108 | 18 | ✓ | ✗ | ✓ | ✓ | 108 | ✓ | ✓ |
| W-E-A13-9t4 | 432 | 72 | ✓ | ✗ | ✓ | ✓ | 432 | ✓ | ✓ |
| W-E-A10-5x2t0 | 40 | 10 | ✓ | ✗ | ✓ | ✓ | 40 | ✓ | ✓ |
| W-E-A15-5x3t0 | 200 | 50 | ✓ | ✗ | ✓ | ✓ | 200 | ✓ | ✓ |
| W-D-A16-11a | 880 | 88 | ✓ | ✗ | ✓ | ✓ | 880 | ✓ | ✓ |
| W-D-A18-13a | 1248 | 104 | ✓ | ✗ | ✓ | ✓ | 1248 | ✓ | ✓ |
| W-D-A20-15a | 960 | 120 | ✓ | ✗ | ✓ | ✓ | 960 | ✓ | ✓ |

**較正**: $\lvert\mathrm{GTSh}\rvert$・$\lvert\ker\widetilde\chi\rvert$ は既存証明書(A16 $880/88$・A18 $1248/104$・A20 $960/120$・I10-1 の $40/10$ と $200/50$)と**全窓で一致**。本走査は judge とは別実装・別走査軸なので、この一致は shadow 集合濃度の再計算にあたる。

> ### 【測定で確定】$\Xi$ は**反準同型**である
> 全 9 窓で `hom_left = false`・`hom_right = true`、すなわち
> $$\Xi\bigl([m_1,f_1]\circ[m_2,f_2]\bigr)=\Xi([m_2,f_2])\cdot\Xi([m_1,f_1]).$$
> 原因は共役の合成規約: $E_\alpha=\mathrm{conj}_{g_\alpha}$、$E_\beta=\mathrm{conj}_{g_\beta}$ なら $E_\alpha\circ E_\beta=\mathrm{conj}_{g_\beta g_\alpha}$。
> **これは埋め込みの障害ではない**。$\Xi':=\iota\circ\Xi$($\iota:g\mapsto g^{-1}$)は準同型で $\ker\Xi'=\ker\Xi=1$、像は同じ部分群。よって
> $$\boxed{\ \mathrm{GTSh}(N,N)\ \hookrightarrow\ N_{\mathrm{Aut}(P)}(\langle\bar x\rangle)\quad\text{(9 窓すべて・machine-measured)}\ }$$

> ### status の更新
> | 主張 | 更新後 |
> |---|---|
> | `NORM-order-divisibility` | PASS(既に) |
> | `NORM-structural-embedding` | **UNKNOWN → PASS(machine-measured・9 窓)**。Lean verified ではない。一般の窓については未証明 |
>
> 補題 NORM-E(§3.2)により、この 9 窓では $\ker\Xi=1$ が核層だけの検査で足りるはずだが、**本測定は全 shadow を走査**しており(`shadow_total` 欄)、補題を使わずに直接確認している。補題は今後の窓でコストを $1/c_m$ に落とすために使う。

**規約の注記(★4 への対応)**: 証明書に載るのは $\lvert\mathrm{im}\rvert$ と包含判定であって、$\lvert\mathrm{GTSh}\rvert\mid\lvert N\rvert$ という Lagrange 条件ではない。`image_is_subgroup_of_normalizer` は GAP の `IsSubgroup` の生出力、`kernel_trivial` は相異なる $\alpha$ の個数と shadow 総数の一致である。

---

## 4. 次段(発射は司令塔)

### 4.1 $r=4$ 判別(悉皆走行中)

v1 §5.1 のとおり **$r=4$ が唯一の実行可能な決定打**。
- PRUNE: 奇部 $=\ell^{s_2(4)}=\ell^1=5$、$\lvert\ker\rvert=40$。
- 撤回済 $\ell^{r-1}$: $\ell^3=125$、$\lvert\ker\rvert=1000$。**25 倍差**。
- 機構: $\mathrm{Syl}_2(S_4)=D_8$ が 4 ブロックに**推移的** ⟹ $B^S=$ 全対角 $=\langle\bar x\rangle$ ちょうど。
- $n=20$、両パリティ枝とも Ree 通過(v1 §5.1)、$\Xi=4.5\times10^8$。
- **現況**: 実現探索(悉皆)走行中。窓が取れ次第、上の 2 値+ $\mathrm{Syl}_2(\Xi(\ker))\cong D_8$ か否かを凍結予言にする。

### 4.2 P86-7-2 — A15 で「どの前件が壊れたか」を確定する測定欄(設計のみ)

Sol F86-4.2.4: 「$\gcd(25,4)=1$ で (H2) は成立。しかし (H3)・$\varepsilon$・$C_G(S)$ 内補群・$(a_{\rm int})$ は測っていない。ゆえに **STR-1 の反例とも、どの前件が壊れたかとも言えない**」。

**私の作業仮説(測定で割る)**: **STR-1 の前件は 1 つも壊れておらず、外れたのは入力 $A$ の同定だけ**ではないか。
P-I10-6 は $\mathrm{GTSh}\cong C_2\times\mathrm{Hol}(C_5)$(位数 40)を予言したが、これは $A=\langle\bar x\rangle=C_5$(ISO-x̄)を入力にした場合の STR-1 の結論である。実測 $A=C_5^2$ を入れ直すと STR-1 の結論は
$$\mathrm{GTSh}\ \cong\ S\times(A\rtimes Q)=C_2\times(C_5^2\rtimes C_4),\qquad \lvert\cdot\rvert=2\cdot100=200$$
で**実測 200・`IdGroup [200,47]` と整合する**。すなわち「STR-1 が壊れた」のではなく「$A$ を取り違えた」可能性が高い。

**測定欄(`W-E-A15-5x3t0`・生値のみ・期待値をコードに書かない)**:

```text
0.  canonical_id                                     # 既存 spec と同一の fail-closed
1.  S_struct, S_order            = Syl_2(ker chi~) の構造と位数
2.  ZS_order                     = |Z(S)|                      # (H1) 後半
3.  K_is_direct_product          = ker = A x S の内部直積か      # (H1) 前半
4.  A_struct, A_order            = O_{2'}(ker chi~)
5.  G_over_CG_S                  = |G / C_G(S)|
6.  Inn_S_order                  = |S / Z(S)|
7.  H3_holds                     = (5 == 6)                     # (H3)
8.  S_central_in_G               = S <= Z(G) か                 # S=C_2 なら (H3) と同値
9.  gcd_A_Q                      = gcd(|A|, |Q|)                # (H2)
10. compl_classes_all            = # ComplementClassesRepresentatives(G, ker chi~)
11. compl_classes_in_CG_S        = # ComplementClassesRepresentatives(C_G(S), C_G(S) ∩ ker)
12. epsilon_zero                 = (11 > 0)                     # STR-1(3)(b)/(c)
13. z_in_Frattini                = z ∈ Phi(Syl_2(C_G(S)/A)) か   # STR-1(3)(d)
14. split_but_not_direct         = (10 > 0) and (11 == 0)       # 205-witness 型の罠
15. iso_to_S_times_AsemiQ        = IsomorphismGroups(G, S x (A : Q)) ≠ fail
                                   （A, Q は欄 4・欄 9 の実測値から構成）
16. Q_action_on_A_matrices       = Q 生成元の A = C_5^2 上の作用行列(F_5 2x2)
```

**判定の型(司令塔用・driver には渡さない)**: 欄 3・7・12 がすべて true なら STR-1 の前件は無傷 ⟹ **P-I10-6 の外れは「$A$ の取り違え」に一元化**され、STR-1 は反証されない。いずれかが false なら、そこが「H2 以外に壊れた前件」の名指しになる。
欄 16 は PRUNE の副産物として価値がある: $Q=C_4$ が $A=C_5^2=B^\tau$ 上で**スカラー**作用するか(v1 §5 の $\mathrm{dl}$ 議論の入力)。

### 4.3 その他の残務

- 【PR-a】$\Xi$ の一般の単射性($\ker\Xi=1$)は依然 UNKNOWN。補題 NORM-E により**核層だけの問題**に落ちた。
- 【PR-b】v1 §4.2 の補題 PR-1 は最後の一歩で $\mathrm{Stab}$ の可解性を使う。**非可解 $\mathrm{Stab}$ 窓(壁標的の本命)では未検討**。
- 【PR-c】v1 §6 の自己点検で挙げた「16 標本のうち 4 は予言値」は変更なし — 実測適合は **12 標本**。

---

## 5. 語法の是正

v1 本文で格を強めて読める箇所を、本稿で次のとおり確定する。

| v1 の箇所 | v1.1 での格 |
|---|---|
| §0 表「② 律の形」の枠囲み | **candidate**(定理ではない) |
| §3.1 予想 PRUNE | candidate(変更なし・ただし §3.1 の (P-a)/(P-b) 分離を適用) |
| §3.2「**16/16 標本**に適合」 | **GAP 単系統で 12 標本 measured + 4 標本は予言値**。「適合」は calibration であって検証ではない |
| §3.4「STR-2 の一般化」 | **予想の帰結**。STR-2 自体が measured(W4)であり、その一般化も measured 水準を超えない |
| §5.1「$r=4$ が唯一の実行可能な決定打」 | 予算判断(変更なし) |
| §2「同定」 | **GAP 単系統 measured**。$\lvert\ker\rvert=10,50$ が証明書と一致した点は **calibration** |
