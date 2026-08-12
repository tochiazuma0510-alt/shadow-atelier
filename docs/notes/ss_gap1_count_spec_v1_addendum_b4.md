# 【追補 B4】SS-GAP-1 の訂正 — $U_{\rm split}$ は上界でない・真の上界は 1,915,460(裁定 1109)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1109(Sol 便 122 §4 の取り込み)
対象 = `ss_gap1_count_spec_v1.md`(+ `ssg1_stage0_model_adjudication_v1.md`・`ssg1_stage0_pred_failure_v1.md`・`ssg1_stage0_pred_repair_v1.md`)
根拠 = `sol/sol_reply_122_r1_line3.md` §4。私の独立検算 = `scratchpad/ssg1_b4_recheck.py`
⚠ $u$/$c$ 非接触・封印非接触。**格: candidate**。

---

## §0 三行

1. ⚠ **私の COUNT-PSL §2 の等式 $\#\text{kernels}=\#\mathrm{Epi}^{\rm mk}/\lvert\mathrm{Aut}(\tilde H)\rvert$ は未証明でした**(marked を固定したまま全自己同型で割れる根拠がない)。⟹ Sol の**安全形**へ差し替え。**最終上界式は生き残ります**(§1)。
2. ⚠⚠ **$U_{\rm split}=954{,}962$ は $N'$ の上界ではありません**。分裂模型は真の $\tilde H$ より**小さい値**を出します(比 **2.0058**)。⟹ 「$N'$ の上界」と呼ぶ行は**撤回**し、**split calibration 値**と改名。
3. ★ **真の上界は Sol の直接計数で得られました**(私の独立検算で 6 整数と既約分数まで一致):
$$\boxed{\ \bigl\lvert GT(N')\bigr\rvert\ \le\ U_{\rm true}=\frac{152212029822}{79465}=1{,}915{,}460.0116\ldots\ \Longrightarrow\ \bigl\lvert GT(N')\bigr\rvert\le\mathbf{1{,}915{,}460}\ }$$
⟹ **③ 線の「規模で詰んだ」判定はやはり撤回**(下界 15,180 の **126 倍**、$10^7$ の**内側**)。**Stage 1 は不要**・**【SSG1-GAP-1】= candidate closed**。

---

## §1 差し替え 1 — COUNT-PSL の導出(安全形)

**旧(`ss_gap1_count_spec_v1.md` §1 (ii) / §2)**:
$$\#\mathcal C(N)\ \le\ \frac{\#\mathrm{Epi}^{\rm mk}(\mathbf Z/2*\mathbf Z/3,\ \tilde H)}{\lvert\mathrm{Aut}(\tilde H)\rvert}\qquad\text{⚠ この等式/不等式は未証明}$$

**新(Sol §4.1 の安全形)**:
> 各 $K\in\mathcal C(N)$ には shadow が与える marked epi が少なくとも 1 本ある。それを $\mathrm{Inn}(\tilde H)$ で**後合成**すると、$T$/$R$ は共役類なので marked 性が保たれ、同じ核をもつ $\lvert\tilde H\rvert/\lvert Z(\tilde H)\rvert$ 本の相異なる marked epi が得られる。ゆえに
> $$\boxed{\ \#\mathcal C(N)\cdot\frac{\lvert\tilde H\rvert}{\lvert Z(\tilde H)\rvert}\ \le\ \#\mathrm{Epi}^{\rm mk}\ \le\ i_2^T\,i_3^R\ }$$

$$\Longrightarrow\quad \bigl\lvert GT(N)\bigr\rvert=\lvert GT^{\rm settled}(N)\rvert\cdot\#\mathcal C(N)\ \le\ \frac{\lvert GT^{\rm settled}(N)\rvert\cdot i_2^T\,i_3^R\cdot\lvert Z(\tilde H)\rvert}{\lvert\tilde H\rvert}$$

★ **最終の上界式は字面が変わりません**($\lvert\mathrm{Aut}\rvert\ge\lvert\mathrm{Inn}\rvert$ を経由していた部分が、Inn 後合成の直接議論に置き換わっただけ)。⟹ **数値は不変・導出だけが健全化**。
⚠ **定理 COUNT-PSL (iii)**($\#\mathrm{Hom}^{\rm mk}=i_2^T i_3^R$)と **(i)**($c\in N\Rightarrow$ 全 $K$ が $c$ を含む)は Sol も正しいと認めています ⟹ **無傷**。

---

## §2 差し替え 2 — 分裂模型は上界でない

### 2.1 真の $\tilde H$(段 2 正本・Sol §4.2)

$$\boxed{\ \tilde H=\{(A,s)\in SL^{\pm}(2,\mathbf Z/p^2)\times S_3\ :\ \det A=\mathrm{sgn}(s)\},\qquad p=691\ }$$

これは $S_3$ 上の **fiber product** であって、私が Stage 0 で使った**分裂模型 $S_3\times\mathrm{PSL}(2,\mathbf Z/p^2)$ とは別の群**です。

### 2.2 直接計数(★ 私の独立検算・`scratchpad/ssg1_b4_recheck.py`)

$R=\mathbf Z/p^2$、$p\equiv7\ (\mathrm{mod}\ 12)$(⟹ $2,3\in R^\times$、$p\equiv1\bmod3$、$p\equiv3\bmod4$):

| 量 | 導出 | 値 | Sol と一致 |
|---|---|---:|---|
| $J_2:=\#\{A: A^2=I,\ \det A=-1\}$ | 順序つき直和分解 $R^2=L_+\oplus L_-$ ⟹ $\lvert GL_2(R)\rvert/\lvert R^\times\rvert^2=p^3(p+1)$ | 228,318,044,732 | ★ ✔ |
| $J_3:=\#\{A: A^3=I,\ \det A=1\}$ | $I$ +($\omega,\omega^2$ 固有直線の順序つき分解)$=1+p^3(p+1)$ | 228,318,044,733 | ★ ✔ |
| $i_2^T=3J_2$ | 互換 3 個 | 684,954,134,196 | ★ ✔ |
| $i_3^R=2J_3$ | 3-巡回 2 個 | 456,636,089,466 | ★ ✔ |
| $\lvert\tilde H\rvert=6p^4(p^2-1)$ | fiber product | 653,158,563,286,621,680 | ★ ✔ |
| $\lvert Z(\tilde H)\rvert$ | $(\pm I,1)$ のみ | 2 | ★ ✔ |

$$\boxed{\ U_{\rm true}=\frac{2\,i_2^T\,i_3^R\,\lvert Z(\tilde H)\rvert}{\lvert\tilde H\rvert}=\frac{152212029822}{79465}=1{,}915{,}460.011602592\ldots\ }$$
$$\bigl\lvert GT(N')\bigr\rvert\ \text{は整数}\ \Longrightarrow\ \boxed{\ \bigl\lvert GT(N')\bigr\rvert\le1{,}915{,}460\ }$$

### 2.3 ⚠ 分裂模型との比

$$\frac{U_{\rm true}}{U_{\rm split}}=\frac{57079511183}{28457270749}=2.005797101431654\ldots>1$$

$$\boxed{\ \Longrightarrow\ U_{\rm split}=954{,}962.000012572\ \textbf{は真の上界ではない — 「split calibration 値」と呼ぶこと}\ }$$

**なぜ小さく出たか**(私の診断): 分裂模型では $S_3$ 成分と行列成分が独立なので、互換コセットの対合は「$A^2=1$ **かつ $\det A=1$**」($\mathrm{PSL}$ 内の対合)から来ます。真の $\tilde H$ では marking が **$\det A=\mathrm{sgn}(s)=-1$** を強制し、**$\det=-1$ 側の対合**($SL$ の外)を数えることになります。**この 2 つの個数が約 2 倍違う**のが比 2.006 の正体です。⟹ ★ **実装係 E が最初に指摘した「odd 側の対合は $SL$ に存在しない」という点(裁定 1092)が、実は真の群では本質だった**わけです — 私は分裂模型でそれを回避してしまいました。

---

## §3 各文書への 1 行補記

| 文書 | 補記 |
|---|---|
| `ss_gap1_count_spec_v1.md` §1(ii)・§2 | **⚠ 訂正**: $\#\text{kernels}=\#\mathrm{Epi}^{\rm mk}/\lvert\mathrm{Aut}\rvert$ は未証明 ⟹ 本追補 §1 の Inn 後合成の安全形へ差し替え(**最終上界式は不変**)。 |
| `ss_gap1_count_spec_v1.md` §3(Stage 1)・§5.2・§7 | **⚠ 撤回**: Stage 1(拡大型の同定)は**不要**。真の $\tilde H$ は fiber product として明示済み ⟹ 残すなら証明書化のみ。**【SSG1-GAP-1】= candidate closed**。 |
| `ssg1_stage0_model_adjudication_v1.md` §5.1・§6 | **⚠ 撤回**: $U(691)\approx10^6$ を「$N'$ の上界」と読む行 ⟹ **split calibration 値**。真の上界は $U_{\rm true}=1{,}915{,}460$。 |
| `ssg1_stage0_pred_failure_v1.md` §0・§6 | 同上。$\boxed{U(691)=954{,}962.0000126}$ は**分裂模型内の厳密値**であり、$\lvert GT(N')\rvert$ の上界ではない。 |
| `ssg1_stage0_pred_repair_v1.md` §5 | 同上。$p=691$ の 4 値は**分裂模型の値**として有効(閉形式の検証には使える)。 |
| すべて | ★ **結論は不変**: CP-D(下界 15,180)は $U_{\rm true}$ でも成立(**126 倍**)、1 ビット($<10^7$)も**内側**。⟹ **③ 線の「規模で詰んだ」判定の撤回は維持**。 |

---

## §4 残る作業(Sol §4.3 の縮約版)

Stage 1 は不要になり、**証明書化 3 点**だけが残ります:

```
[SSG1-CERT] 真の上界の証明書化(実装係へ)
[C-1] H~ = {(A,s) ∈ SL^±(2,Z/p^2) × S_3 : det A = sgn s} の定義・位数・S_3 marking・
      |Z(H~)| = 2 を exact に再確認
[C-2] J_2 = p^3(p+1) , J_3 = 1 + p^3(p+1) の直和分解計数を
      (a) symbolic rail  (b) 小さい p ≡ 7 (mod 12) での literal enumeration rail
      の二系統で照合  ★ 候補 p = 7, 19, 31, 43（すべて p ≡ 7 mod 12）
[C-3] p = 691 の 6 整数と既約分数 152212029822/79465 を cert 化し、
      既知下界 15,180 との向き（U_true / 15180 = 126.18…）を確認
出力: cert (schema ssg1_true_bound/v1)。整数と既約分数のみ。u_touched=false
```

**★ 凍結予言(整数・機械生成 `scratchpad/ssg1_b4_recheck.py`)**: [C-2] の小 $p$ での literal 値

| $p$ | $J_2=p^3(p+1)$ | $J_3=1+p^3(p+1)$ |
|---|---:|---:|
| 7 | 2,744 | 2,745 |
| 19 | 137,180 | 137,181 |
| 31 | 953,312 | 953,313 |
| 43 | 3,498,308 | 3,498,309 |

⚠ **$p\equiv7\ (\mathrm{mod}\ 12)$ に限ること**($p\equiv1\bmod3$ が $J_3$ の $\omega$ 分解に、$2,3\in R^\times$ が両方に効く)。他の類では式が変わります。

## §5 記帳

- ⚠ **自己捕獲 m1109-2**: COUNT-PSL の $\#\mathrm{Epi}/\lvert\mathrm{Aut}\rvert$ 等式を証明せずに使いました。⟹ Sol の Inn 後合成で修理(数値は不変)。
- ⚠⚠ **自己捕獲 m1109-3**: Stage 0 の分裂模型を「$p$ 依存性の代理」として設計しましたが、**真の $\tilde H$ が既に明示されていた**(段 2 正本)ことを見落としました。⟹ 代理は不要で、**直接数えるべきでした**。しかも代理は**上界にならない**方向に外れていました。
 ★ **教訓**: 「模型で代理する」前に、**真の対象が既に手元にないかを在庫検査する**(`stock-check-before-acquisition` の数学版)。
- ★ **生き残ったもの**: 定理 COUNT-PSL の (i)(iii)(= $c\in N$ 還元と $i_2^Ti_3^R$ 公式)・補題 TR と閉形式(分裂模型内で厳密・PRED-S0-4 の検定対象として有効)・最終上界式の形。
- **【SSG1-GAP-1】** = 「分裂模型は上界か」には **NO**、「真の上界を得る」には **candidate closed**。
- **申告**: 紙 + 機械(`scratchpad/ssg1_b4_recheck.py`・有理数厳密)。本追補の全数値は機械生成(裁定 1103 規約)。$u$/$c$ 非接触・**verified ではない**(candidate 格)。
