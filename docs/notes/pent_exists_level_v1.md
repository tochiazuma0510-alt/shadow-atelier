# ∃-live と補題 SUBGRP は**両立する** — 水準(fine / coarse)の取り違えが 10/20 の正体

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 委嘱: 裁定 253 委嘱 3(司令塔の第一検査結果を受けて)
- 入力: 司令塔の実測(∃-live 20 元は**積で閉じず・逆元でも閉じず・単位元は含む**、$A_5$ に位数 20 の部分群は存在しない)/ `pent_recoding_v1.md` §3(補題 SUBGRP)/ `a5_arithmetic_recheck_v1.md` §3(定理 PENT-IMP)/ `pent_pi_a5_v2_20260731.json`

---

## 0. 結論

| # | 判定 | 格 |
|---|---|---|
| **①** | **両立する。矛盾はない。** 補題 SUBGRP が部分群性を主張するのは **$\mathrm{GT}(K_\pi)$ の $\mathrm{GT}_{\rm gen}(N_A)$ における像**(準同型像・**shadow の集合**)であって、**$A_5$ の部分集合である ∃-live ではない**。司令塔の整理は正しい | **proof**(§1) |
| **②** | **10/20 の正体が確定した**: $(K_\pi)_{PB_3}\subsetneq N_A$(指数 $=\lvert H_3\rvert=25$)。pentagon は**細かい水準**の条件で、「$f\bmod N_A$ が pentagon を満たすか」は**そもそも定義されていない量**だった。v1 census はこの取り違えの産物 | **proof**(§2) |
| **③** | ゆえに **定理 PENT-IMP の前提 (P1) が偽**と確定。同定理は「(P1)–(P4) のいずれかが偽」を正しく主張しており、**撤回不要・むしろ的中**((P1) を名指ししていた) | **確定** |
| **④** | **$\lvert\exists\text{-live}\rvert=20=\lvert\mathrm{GT}(N_A)\rvert$ は異種の量の比較**。$\mathrm{GT}(N_A)$ の 20 shadow の **$f$-成分は 10 個しかない**(v1 cert から確定)。正しい比較は **20 対 10** で、一致ではない | **proof**(§3) |
| **⑤** | **正しい較正ゲートの形**と、即実行できる 3 検査 (T1)(T2)(T3) を §4 に置いた。**(T1) は cert の literal だけで今すぐ判定できる** | **設計** |
| **⑥** | $H_3$(位数 25)の位置づけ = $F_2/(K_\pi)_{F_2}\twoheadrightarrow F_2/(N_A)_{F_2}=A_5$ の核。∃ はこの 25 元 fiber 上の量化子 | **proof**(§5) |

---

## 1. 補題 SUBGRP の適用水準(委嘱 3-1)

> ### 補題 SUBGRP(正確形・v1 の書き方を精密化)
> 還元写像
> $$\mathrm{red}:\ \mathrm{GT}(K_\pi)\longrightarrow \mathrm{GT}_{\rm gen}(N_A),\qquad
> \bigl(m\bmod K_{\rm ord},\ \bar f\bmod (K_\pi)_{PB_3}\bigr)\longmapsto\bigl(m\bmod N_{\rm ord},\ f\bmod (N_A)_{PB_3}\bigr)$$
> は**群準同型**である($(K_\pi)_{PB_3}\subseteq N_A$ かつ $N_{\rm ord}\mid K_{\rm ord}$ で well-defined、合成則 (3.53) は両水準で同一式)。ゆえに
> $$\boxed{\ \mathrm{im}(\mathrm{red})\ \le\ \mathrm{GT}_{\rm gen}(N_A)\quad(\text{部分群})\ }$$
> **これは shadow(対 $[m,f]$)の集合についての主張であり、$f$-成分だけを $A_5$ に落とした部分集合については何も言わない。**

**一方 ∃-live は**
$$\exists\text{-live}:=\bigl\{f\in A_5\ :\ \exists\,\bar f\in\pi_{H_3}^{-1}(f)\ \text{で pentagon (2.20) が成立}\bigr\}$$
という「**fiber が解集合と交わる類の集合**」であり、準同型像ではない。一般に

- 積で閉じる必要はない($\bar f_1,\bar f_2$ が解でも $\overline{f_1f_2}$ の**どの**持ち上げが解かは別問題)、
- 逆元で閉じる必要もない(pentagon は $f\mapsto f^{-1}$ で不変な条件ではない)、
- 単位元は含む($\bar f=1$ が pentagon を満たすから)✓ 実測と一致。

> **⟹ 委嘱 3-1 の答え: 両立する。** 補題 SUBGRP と実測(20 元・非閉)は**別の対象についての言明**であり、矛盾はない。**$A_5$ に位数 20 の部分群が無いことも、ここでは何の障害でもない**(∃-live が部分群である理由が最初から無い)。

---

## 2. 10/20 の正体 — $(K_\pi)_{PB_3}\subsetneq N_A$

司令塔の報告にある **$H_3$(位数 25)** の存在が決定的である。$H_3=\ker\bigl(F_2/(K_\pi)_{F_2}\twoheadrightarrow F_2/(N_A)_{F_2}=A_5\bigr)$ ならば
$$(K_\pi)_{F_2}\ \subsetneq\ (N_A)_{F_2},\qquad \bigl[(N_A)_{F_2}:(K_\pi)_{F_2}\bigr]=25 .$$

> ### 帰結(v1 census の欠陥の同定)
> pentagon (2.20) は $PB_4/K_\pi$ 内の式で、$f$ の類は **$(K_\pi)_{PB_3}$ を法として**しか意味をもたない。
> v1 census は $f$ を **$A_5$ の 60 元**(= $N_A$ を法とする類)として走らせたので、**「その 60 元のどの持ち上げで評価したか」が暗黙に固定されていた**。すなわち
> $$\text{v1 の 8/60}\;=\;\{\,f\in A_5:\ \textbf{特定の一つの}\ \text{持ち上げ}\ \bar f\ \text{が pentagon を満たす}\,\}$$
> であって、$\{f:\exists\bar f\}$ ではない。**「$f\bmod N_A$ が pentagon を満たす」という命題はそもそも定義されていない。** v2 の ∃ 版が正しい定式化である。

> ### 定理 PENT-IMP との整合(`a5_arithmetic_recheck_v1` §3)
> 同定理は仮定 **(P1)** $K_\pi\in\mathrm{NFI}_{PB_4}(B_4)$ **かつ $(K_\pi)_{PB_3}=N_A$** の下で矛盾を導き、「(P1)–(P4) のいずれかが偽」と結論した。**いま (P1) の後半が偽と確定した。** 定理は撤回不要で、**欠陥の所在を正しく名指ししていた**(§5 の探索先リストの第 2 項)。
> **⟹ v4(20/20 arithmetical)との矛盾は解消。三つ巴は完全に閉じた。**

---

## 3. 「20 = 20」は異種比較(委嘱 3-2)

`pent_pi_a5_20260731.json` の 20 shadow を $f$ ごとに畳むと(`pent_recoding_v1` §2 の表)、**相異なる $f$ は 10 個**である:
$$1,\ yx^{-1},\ y^{-1}x,\ xy^{-2}x^{-1},\ x^{-1}y^{2}x\quad(m\in\{0,4\}),\qquad
xyx^{-1},\ x^{-1}y^{-1}x,\ x^2y^{-2},\ x^{-2}y^{2},\ x^2yxy^2\quad(m\in\{1,3\}).$$
各 $f$ が 2 つの $m$ をもつので $10\times2=20$ shadow。

> **⟹ $\lvert\exists\text{-live}\rvert=20$($A_5$ の部分集合)と $\lvert\mathrm{GT}(N_A)\rvert=20$(対の集合)は種類が違う。**
> 較正に効く比較は **$\exists\text{-live}\ \supseteq\ \{10\ \text{個の}\ f\text{-成分}\}$** であり、数としては **20 対 10**。
> 「20 = 20」は**偶然**と見るのが正しい(別の構造の可能性は否定しないが、現時点で支持する材料はない)。**candidate 札を下げることを推奨**。

---

## 4. 正しい較正ゲート P-PENT-1′ と、即実行できる 3 検査

> ### 較正ゲート P-PENT-1′(正しい形)
> v4(20/20 arithmetical)が真なら、$\mathrm{Ih}_{K_\pi}$ の関手性より
> $$\mathrm{im}\bigl(\mathrm{red}:\mathrm{GT}(K_\pi)\to\mathrm{GT}_{\rm gen}(N_A)\bigr)\ \supseteq\ \mathrm{Ih}_{N_A}(G_{\mathbf Q})=\mathrm{GT}(N_A),$$
> すなわち **$\mathrm{red}$ は全射**。ゆえに較正は
> $$\boxed{\ \text{20 個の shadow }[m,f]\ \text{それぞれに、}\ \mathrm{GT}(K_\pi)\ \text{の持ち上げ}\ (\bar m,\bar f)\ \text{が存在するか}\ }$$

**検査(コスト順)**:

- **(T1) 即断・cert の literal のみ**: $\exists\text{-live}\supseteq\{10\ \text{個の}\ f\text{-成分}\}$ か。
 - **含めば** 必要条件は通過 ⟹ (T2) へ。**含まなければ**、その $f$ で P-PENT-1′ が破れる ⟹ v4 か $K_\pi$ の再検分に戻る。
 - v1 の 8 元 live は 10 個中 **5 個**($m\in\{0,4\}$ 側)を含んでいた。∃ 版で残り 5 個が入ったかどうかが焦点。
- **(T2) 本命**: 各 shadow $[m,f]$ について、fiber $\pi_{H_3}^{-1}(f)$(25 元)の中に
 **(a) pentagon (2.20) を満たし、(b) $B_3/(K_\pi)_{PB_3}$ 内で fine hexagon (2.18)(2.19) を満たし、(c) $\bar m\equiv m\ (\mathrm{mod}\ N_{\rm ord})$** を同時に満たす $(\bar m,\bar f)$ があるか。
 コストは $20\times25\times(\text{charming }\bar m\text{ の個数})$ — **数千回の置換積**で終わる。
 **注意**: (b) を落とすと ∃-live(pentagon のみ)になり、部分群性も較正の意味も失われる。**(a)(b)(c) を同時に課すこと**が要点。
- **(T3) 構造の確認**: $\mathrm{GT}(K_\pi)$ を直接列挙し、$\lvert\mathrm{im}(\mathrm{red})\rvert$ を測る。**補題 SUBGRP により $\mathrm{im}(\mathrm{red})$ は $\mathrm{GT}(N_A)\cong F_{20}$ の部分群でなければならない** — 位数は $1,2,4,5,10,20$ のいずれか(($F_{20}$ の部分群の位数)。**20 でなければ v4 と衝突**するので、ここが本当のゲート。
 - この (T3) が **10** を返したら、$\widetilde\chi$ の像が $\{\pm1\}$ に落ちるので `a5_arithmetic_recheck_v1` §3 の矛盾が復活する ⟹ さらに深い欠陥。
 - **20** を返せば pentagon 線は開通。

---

## 5. $H_3$(位数 25)の位置づけ(委嘱 3-3)

$$1\longrightarrow H_3\longrightarrow F_2/(K_\pi)_{F_2}\longrightarrow F_2/(N_A)_{F_2}=A_5\longrightarrow 1,\qquad \lvert H_3\rvert=25 .$$
すなわち $\lvert F_2/(K_\pi)_{F_2}\rvert=1500$。**$\pi$-lift は $B_3$ 側を細かくしている** — 第 4 本目の紐($\sigma_3\mapsto\sigma_1$)が新しい関係を持ち込まず、逆に $x_{14},x_{24},x_{34}$ の分だけ商が細かくなるため。

- $25=5^2$ で $N_{\rm ord}=5$ と整合。$H_3\cong C_5\times C_5$ が自然な候補(**要確認**・cert に構造欄があれば即決)。
- $H_3$ は $A_5$ 上の加群として何か(自明 / 自然 5 次元の部分商 / $\mathbf F_5$ 上 2 次元表現)— **$A_5$ の $\mathbf F_5$ 上の 2 次元表現は自明なものしかない**($\mathrm{SL}_2(5)$ 経由の 2 次元は $A_5$ には降りない)ので、$H_3$ が $A_5$-加群として自明(= 中心的拡大)である可能性が高い。**中心拡大なら fiber 上の ∃ は「25 元の平行移動で pentagon が解けるか」という一次の問題**になり、(T2) の見通しが良い。
- **設計上の含意**: $(K_\pi)_{PB_3}=N_A$ をちょうど実現する $B_4$ 窓(= $H_3$ が自明な lift)があれば、v1 の素朴 census がそのまま正しい較正になる。**次実験の第一候補は「$H_3$ を潰す lift」**(あれば)。無ければ ∃ 版で行く。

---

## 6. 次実験の設計(pentagon 線)

| 優先 | 実験 | 目的 | コスト |
|---|---|---|---|
| **1** | **(T2)+(T3)**(§4) | 較正 P-PENT-1′ の本判定。$\mathrm{im}(\mathrm{red})$ の位数が 20 か | 数千回の置換積(即日) |
| 2 | $H_3$ の構造と $A_5$-加群としての型 | (T2) の見通し・「$H_3$ を潰す lift」の存否 | 小 |
| 3 | **梯子窓への $\pi$-lift**($N_{\rm ord}=9$ 系) | $\ell=9$ 窓で同じ鎖を回し、**$\widetilde\chi$ の平方類による分離が再現するか**を見る。$(\mathbf Z/9)^\times\cong C_6$ なので「指数 2」でなく「平方類(指数 2)/3 乗類(指数 3)」の区別がつく — v1 の $\{\pm1\}$ 署名が装置由来か算術由来かの**決定実験** | 中(既存梯子窓を再利用) |
| 4 | $N^{(19)}$ の窓構成 | 論文実データ(216/36)との**直接較正**。$\pi$-lift 経路の較正が未了なので、これが本筋の裏取り | 中〜大 |

---

## 7. 付録 — $\ell=25,t=5$ の $T_{\rm trans}$ 計数の発注仕様(司令塔の求めに応じて)

- **目的**: $\lambda=(25,1^5)$($n=30$)について $T_{\rm trans}(\lambda)>0$ か否かを厳密判定。$>0$ なら探索の問題、$=0$ なら新障害。
- **手続き**(`sat_l1_probe8.g` と同一機構):
 1. $T_{\rm all}(\mu)=\sum_{i\in\mathrm{Inv},\,j\in\mathrm{Ord3}}\mathrm{ClassMultiplicationCoefficient}(\mathrm{tbl}_{|\mu|},j,i,k_\mu)$ を、$\mu$ が $\lambda$ の巡回部分多重集合すべて($(25,1^a)$、$a=0..5$ と $(1^b)$)について計算。$\mathrm{tbl}_n=\mathrm{CharacterTable}("Symmetric",n)$、$n\le30$。
 2. 巡回の集合分割($\lambda$ は 6 巡回 ⟹ Bell(6)=203 通り)上の Möbius 反転で $T_{\rm trans}(\lambda)$ を得る。
- **想定リソース**: $S_{30}$ の指標表(5604 類)。**ピーク 8–16 GB 見込み**(8GB ローカルでは不可)。時間は数十分〜数時間。
- **出力**: $T_{\rm all}$、$T_{\rm trans}$、$\lvert C_{S_{30}}(w_0)\rvert=25\cdot5!=3000$、比 $T_{\rm trans}/\lvert C\rvert$。
- **較正**: 同じスクリプトで $\lambda=(23,1^3)$($n=26$・**既に $A_{26}$ の witness あり**)を先に流し、$T_{\rm trans}>0$ を確認してから本番へ(既知の答で装置を較正する規律)。

---

## 8. 格付け

| 主張 | 格 |
|---|---|
| 補題 SUBGRP の正確形(im(red) が部分群) | **proof** |
| ∃-live が部分群である必要はない(両立) | **proof** |
| 10/20 の原因 = $(K_\pi)_{PB_3}\subsetneq N_A$ | **proof**($H_3$ の存在から) |
| 定理 PENT-IMP は撤回不要・(P1) が偽と確定 | **確定** |
| $\mathrm{GT}(N_A)$ の $f$-成分は 10 個 ⟹ 「20=20」は異種比較 | **proof**(cert の literal) |
| $H_3\cong C_5\times C_5$・$A_5$-加群として自明 | **candidate**(要確認) |
| 較正ゲート P-PENT-1′ と (T1)(T2)(T3) | **設計** |

**本ノートは新しい機械計算を行っていない**(司令塔の実測報告・既存 cert・既存ノートの照合のみ)。
