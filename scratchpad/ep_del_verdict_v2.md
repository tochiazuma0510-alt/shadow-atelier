# 予想 EP-DEL の判定 v2 — CP-BRUN を v194/v198 原文で判定

`DIR: proper 側計器 / FRAME: Sol A7 三 endpoint × 工房 BRUN-DEF`
**委嘱**: 司令塔・裁定 1717(c) ①。**v1(sha16 `49c9e1eab9a8718d`)は改変せず並置。本 v2 が v1 を supersede する。**
**読んだ範囲(v2 で追加)**: `sol/proof_r07_combined_block_endpoint_reduction_v194.md`(全 330 行のうち §1–§3 を精読)・`sol/proof_r07_endpoint_only_word_evaluator_v198.md`(§1–§2 精読)・`sol/proof_r07_pointed_ancestry_word_pair_promotion_v191.md`(§1 の $\pi$ 定義部を grep 読み)・`sol/proof_r07_ten_occurrence_seven_block_action_bridge_v189.md`($\rho$ の値域を grep 読み)。**Sol への照会はしていない。**
**判定 = UNKNOWN(on the nose)。ただし障害は「補題」から「有限の機械評価」へ落ちた。**
**著者**: 数学者(Opus 5)/ 2026-08-28。**規約 (R-1)(R-2) 準拠。**

---

## 1. ★ v1 の訂正 — 「1 層ずれる」は**誤り**だった

> ### ⚠ 撤回(v1 §3・§4(i))
> v1 は「$E_P(M)$ と $\mathrm{Fox}(P(F_kc_k))$ は $\mathcal F^{k+1}$ を法としてしか一致しない」「判定は $\mathcal F^{k+1}$ を法として PROVED」と書いた。**原文を読んで誤りと判明したので撤回する。**
> **原因**: v252 の "crossed-prefix terms … are not discarded; (2.4) locates them in the next layer" を「$E_P$ が近似である」と読んだ。**正しくは、その文は Theorem 2.1(残差 $[\Phi(F_kc_k)]_k$ の層)についてのものであり、$E_P$ の定義とは別件である。**
> **v194/v198 の実際の定義では、prefix 輸送は Fox 積則そのもの**であり、$E_P(M)$ は**近似ではなく厳密**である(下 §2)。⟹ **判定は「1 層ずれ」ではなく、別の 1 点に落ちる。**

---

## 2. 原文が与える厳密な形(逐語)

**v194 (1.6)–(1.8)・(2.2)**: 各 occurrence $o$ に固定共通源置換 $\rho_o:\mathcal G\to G_B$ があり、$L_o$ は「literal signed, **prefix-transported** insertion into the Fox chain of the whole block」。
$$(M\star d)_B=\sum_{o\in B}L_o\Bigl(\sum_i a_i\bigl(\rho_o(U_i)-\rho_o(V_i)\bigr)d_o\Bigr),\qquad z_B(M)=e_B-(M\star d)_B,\qquad \eta_B(M)=D_{1,B}z_B(M).$$
**v198 Theorem 2.1(ENDPOINT-ONLY COLLECTION)** が $L_o$ を完全に明示する:
$$\boxed{\ \eta_B(M)=\epsilon_B-\sum_{o\in B}\sigma_o P_o\sum_{i=1}^{t}a_i\bigl(\rho_o(U_i)-\rho_o(V_i)\bigr)\xi_o\ }$$
($\epsilon_B=D_{1,B}e_B$、$\xi_o=D_{1,B}d_o$、$\sigma_o=\pm1$、**$P_o\in G_B$ が prefix**)。証明は $D_{1,B}(vc)=vD_{1,B}(c)$ の $k[G_B]$-線型性のみ。
**v198 (1.4)**: $\rho_o:F(x,y)\to G_B$。**v189 (l.19–20)**: $a=\rho_{xy},b=\rho_{xz},c=\rho_{yz},d=\rho_{ux},e=\rho_{uy}:F\to E_3$(E4 側も同様)。
**v191 (1.1)(1.3)**: $\pi:\mathcal G\twoheadrightarrow\Delta_0$(roof 群)、$M=\sum a_i(U_i-V_i)$ with $\pi(U_i)=\pi(V_i)$。

⟹ **$L_o$ は「符号つき左乗 $\sigma_oP_o$」= Fox 積則の prefix そのもの。近似ではない。**

---

## 3. $(d_i)_*$ を通す(★ 2 つの成分に完全分解する)

$d_i:G_P\to G_P^{(i)}$(strand deletion)は群準同型ゆえ、群環へは**環準同型**として伸び、左乗を保つ。v198 (2.2) に適用して

$$(d_i)_*\eta_P(M)=\underbrace{(d_i)_*\epsilon_P}_{(\mathrm{C}\text{-}\alpha)}\ -\ \underbrace{\sum_{o\in P}\sigma_o\,d_i(P_o)\sum_i a_i\bigl(d_i\rho_o(U_i)-d_i\rho_o(V_i)\bigr)(d_i)_*\xi_o}_{(\mathrm{C}\text{-}\beta)} .$$

### 3.1 (C-α) は **PROVED**(on the nose)

Fox の基本恒等式 $D_1\bigl(\mathrm{Fox}(w)\bigr)=w-1$ より $\epsilon_P=D_{1,P}e_P=w_e-1$($w_e$ = corrected residual の literal word)。
**仮定「occurrence が charming 台(commutator words)」**から v252 (3.1) の $F_kc_k$ が commutator word となり、**BRUN-DEF**(工房・paper-proof)経由の v252 (3.3) が
$$w_e=P(F_kc_k)\in B_P=\mathrm{Im}(\mathrm{Brun}_4\to G_P)$$
を与える。$\mathrm{Brun}_4=\bigcap_i\ker d_i$ ゆえ $d_i(w_e)=1$。したがって
$$\boxed{\ (d_i)_*\epsilon_P=d_i(w_e)-1=0\qquad(\forall i).\ }$$
∎ **これは委嘱が問うた「BRUN-DEF の endpoint 版」の半分であり、成立している。**

### 3.2 (C-β) が**残りの全て** — そしてそれは補題ではなく**有限評価**

各項は因子 $\bigl(d_i\rho_o(U_j)-d_i\rho_o(V_j)\bigr)$ を持つ。$\pi(U_j)=\pi(V_j)$(v191)なので

$$\boxed{\ (\mathrm{C}\text{-}\beta)=0\ \ \Longleftarrow\ \ \ker\pi\subseteq\ker\bigl(d_i\circ\rho_o\bigr)\quad(\forall o\in P,\ \forall i)\ }$$

すなわち **「$d_i\circ\rho_o$ が roof $\pi$ を経由するか」**。

> ### ★ 原文が与える否定側の証拠(**無料では通らない**)
> **v191 §1(l.79 逐語)**: 語対は "**indistinguishable at the roof but may separate at a finer level**"。
> ⟹ **$\rho_o$ 自身は $\pi$ を経由しない**(経由するなら $\rho_o(U_j)=\rho_o(V_j)$ で $\eta_P$ が $M$ に依存せず、テストが空虚になる)。
> ⟹ (C-β) は「**削除 $d_i$ が、$\rho_o$ の分離部分をちょうど潰す**」ことを要求する。**自明ではない。**

> ### ★ しかし決定的に軽い(これが v2 の最大の収穫)
> (C-β) は**普遍的な補題ではなく、登録済みの有限データに対する評価**である:
> - $\rho_o$ は **5 本の E3 写像 + 5 本の E4 写像**(v189 l.19–20, l.309)で明示。
> - $(U_j,V_j)$ は $M$ ごとに有限個の literal source words(v191 (1.3):「literal source words で取れる」)。
> - $d_i$ は 4 本の strand deletion。
> ⟹ **$d_i\rho_o(U_j)$ と $d_i\rho_o(V_j)$ を削除文脈で評価して比べるだけ。**しかも **v198 の evaluator が既に $\rho_o(U_j)-\rho_o(V_j)$ を計算している**ので、**その出力に $d_i$ を後合成するだけ**で済む。

---

## 4. 判定(三値)

> ### 予想 EP-DEL の判定 = **UNKNOWN(on the nose)**
> **足りないもの(1 行)**: **$d_i\circ\rho_o$ が roof 射影 $\pi$ を経由するか($\ker\pi\subseteq\ker(d_i\rho_o)$)— v191 §1 は $\rho_o$ 自身は経由しないと明言しているので、削除が分離部分をちょうど潰すかどうかが全て。**
>
> **十分条件は原文に「ある」とは言えない**(v189/v191/v194/v198 のいずれも $d_i\circ\rho_o$ と $\pi$ の関係を述べていない)。
> **反例も構成していない**($\rho_o$ の具体形と $\ker\pi$ を突き合わせていないため)。

**内訳(進んだ分)**:

| 成分 | 状態 | 根拠 |
|---|---|---|
| **(C-α)** $(d_i)_*\epsilon_P=0$ | **PROVED(on the nose)** | Fox 恒等式 + BRUN-DEF + v252 (3.1)(3.3) |
| **(C-β)** 補正和 $=0$ | **UNKNOWN** | $\ker\pi\subseteq\ker(d_i\rho_o)$ が未確認 |
| v1 の「1 層ずれ」 | **撤回** | v194/v198 の prefix 輸送は Fox 積則そのもの |

---

## 5. ★ 実務的帰結 — **EP-DEL は「証明」しなくても「測定」できる**

v198 (2.2) は完全に明示的で、$(d_i)_*$ は環準同型である。ゆえに

$$(d_i)_*\eta_P(M)=\;-\sum_{o\in P}\sigma_o\,d_i(P_o)\sum_i a_i\bigl(d_i\rho_o(U_i)-d_i\rho_o(V_i)\bigr)\,(d_i)_*\xi_o$$

((C-α) により第 1 項は消えている)は、**既存 evaluator の出力に $d_i$ を後合成するだけで計算できる**。⟹

> **提案(実装 1 本)**: v198 evaluator に `deleted_endpoint(i)` を追加し、実際の $M$ について $(d_i)_*\eta_P(M)$ を 4 本とも出す。
> - **全 4 本が 0** ⟹ **その $M$ については EP-DEL が成立**(一般命題は未証明のまま実務効果を取れる)⟹ $E_P=0$ の判定を Brunnian 座標内に還元できる。
> - **1 本でも非零** ⟹ **EP-DEL は一般には偽**(反例が実データで出る)⟹ 予想を REFUTED にできる。
> ⟹ **どちらに転んでも一級の結果**であり、**新しい理論を作らずに三値が確定する**。

**A7 が 2 本になるか**: (C-α) だけでは**ならない**。(C-β) が成り立って初めて $E_P=0$ が Brunnian 座標へ還元される。⟹ **配達判断の材料としては「まだ 3 本。ただし 1 行の測定で決着する」**が正確。

---

## 6. UNKNOWN・債務

1. **(C-β)** — §4 の 1 行。**測定で決着可(§5)。**
2. $\rho_o$ の値域 $E_3,E_4$ の**群としての構造**を私は確認していない(可換なら (C-β) は自明に成立するが、$\mathbb F_3[E_4]$ の次元(C-11 の $5\lvert E_4\rvert+1\approx1.7\times10^{29}$)から**巨大な群**であり、可換とは限らない)⟹ **可換性の確認は 1 行**で、成立すれば (C-β) は即座に閉じる。**未確認。**
3. **$\ker\pi$ の明示**(v191 $\Delta_0$ の定義)を私は読んでいない($\pi$ の存在と $\pi(U_i)=\pi(V_i)$ だけを使った)。
4. **BRUN-DEF の格** = `paper-proof`(工房・falsifier 照合済)・Lean 未形式化。本判定はその上に乗る。
5. **v194 §4–§7・v198 §3 以降は未読**(endpoint の有限計算・証明書契約)。(C-β) の判定に必要なら読むべき箇所。
