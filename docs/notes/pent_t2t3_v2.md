# (T2)(T3) fine 水準の実測 — $\lvert\mathrm{im}(\mathrm{red})\rvert=4$、per-m $=[1,1,1,1]$、$H_3$ は中心的 $C_5^3$

> **【SUPERSEDED — 裁定 278/280(2026-07-31)】** 本稿の測定値 4/20・im(red)≅C₄ は**粗↔精の語順規約食い違い(f と f⁻¹ の fiber 取り違え)による誤測定**として撤回。正値は **20/20**(`pent_t2t3_v3_20260731.{g,json}`・著者 witness 20/20 受理・回帰 unit test 第 4 元つき)。診断の正本 = `pent_conflict_diagnosis_v2.md`。構造値(7500/1500/125・H₃=C₅³ central・Ψ(c) 位数 5)は生存。本稿は誤りの記録として保存。

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- probe: `search/probe/wac_v1/pent_t2t3_run2.g` / cert: `search/certs/pent_t2t3_20260731.json`(`json.load` 検証済・`DRIVER_DONE` marker あり)
- 前走 `pent_t2t3_v1.md`(設計前提の誤り = fine≠coarse)を修理した本走。**接触遮断**(期待値 20/10/$\{\pm1\}$ を述語に一切使用せず)。

---

## 0. 結果

| 量 | 実測 |
|---|---|
| $\lvert PB_3/(K_\pi)_{PB_3}\rvert$ | **7500** |
| $\lvert F_2/(K_\pi)_{F_2}\rvert$ | **1500** |
| $\Psi(c)=1$ ? | **false**($\mathrm{ord}\,\Psi(c)=5$)|
| $H_3=\ker\bigl(PB_3/(K_\pi)_{PB_3}\twoheadrightarrow A_5\bigr)$ | **125 $=C_5\times C_5\times C_5$・中心的** |
| ($F_2$ 水準の $H_3$)| $1500/60=$ **25 $=C_5\times C_5$** — 司令塔の $\lvert H_3\rvert=25$ と**独立一致** |
| fiber の大きさ | **125** |
| $\lvert\mathrm{GT}(N_A)\rvert$ / 相異なる $f$ | 20 / **10**(接触遮断下で独立再現)|
| **(T2) 持ち上がった shadow** | **4 / 20**、per-m $=[m{=}0{:}1,\ m{=}1{:}1,\ m{=}3{:}1,\ m{=}4{:}1]$ |
| **(T3) $\lvert\mathrm{im}(\mathrm{red})\rvert$** | **4**(相異なる $f$-成分 = 2)|

---

## 1. 実装の要点(設計どおり)

- $(K_\pi)_{PB_3}$ は **(2.4) の 5 余面全数**で判定: $\Psi:PB_3\to E^5$、$\Psi_i=\pi\circ\varphi_i$ を $N_A$ で還元。$PB_3/(K_\pi)_{PB_3}\cong\Psi(PB_3)\le E^5$(**部分直積**)。
- **$\Psi(c)\ne1$ が判明**(位数 5)⟹ **$c\notin(K_\pi)_{PB_3}$** ⟹ **簡約 hexagon (3.10)(3.11) は fine 水準では使えない**(等価性は $c\in N$ を要する)。よって本走は**原形 (2.18)(2.19) の defect** を $PB_3=\langle x,y,c\rangle$ の語として構成した:
 $$A:=\mathrm{conj}_{\sigma_1},\quad B:=\mathrm{conj}_{\sigma_2},\qquad x_{13}=x_{12}^{-1}c\,x_{23}^{-1},$$
 $$A:\ x\mapsto x,\ y\mapsto y^{-1}x_{13}y,\qquad B:\ y\mapsto y,\ x\mapsto x_{13}$$
 $$D_1=A(P)\,A(B(R))^{-1}f\ \ (P=x^mf^{-1}B(y^mf),\ R=(x_{13}y)^m),\qquad
 D_2=f^{-1}B(y^mf)\,BA(x^m)\,[BA(S)BA(f)]^{-1}\ \ (S=(x\,x_{13})^m)$$
 判定は $\Psi(D_1)=\Psi(D_2)=1$。**これが implementer の報告した「$\sigma_1,\sigma_2$ と $c$ の表現がない」ギャップの解消**($B_3$ の商を作らずに、$\sigma$-共役公式で $PB_3$ の語に落とす)。
- 健全性検査: $A(c)=c$ ✓、$B(c)=c$ ✓、$\tau^3=1$ ✓、$x_{12}x_{13}x_{23}=1$ in $E$ ✓。

---

## 2. 条件別の内訳(どれが効いているか)

fiber 125 元あたりの通過数(全 20 shadow で同じ型):

| 条件 | 通過数 |
|---|---|
| **c4**(commutator $q\in[Q_P,Q_P]$) | **常に 1 / 125** — 持ち上げを**一意に固定する** |
| **c1, c2**((2.18)(2.19) の defect) | **各 $m$ 層でちょうど 1 個の $f$ について 5/125、残り 4 個の $f$ で 0/125** ← **律速** |
| c3(pentagon (2.20)) | 5 または 25(**0 になることはない**) |
| c5(refined 全射) | 125 または 0 |

> **⟹ 律速は pentagon ではなく fine hexagon。** pentagon 単独ならどの $f$ も fiber 内に解をもつ。**「pentagon が刈る」という v1/v2 の描像は fine 水準では成立しない。**

---

## 3. 構造的整合性検査(2 つとも PASS)

1. **補題 SUBGRP**: $\lvert\mathrm{im}(\mathrm{red})\rvert=4$ は $F_{20}$ の部分群位数 $\{1,2,4,5,10,20\}$ に**含まれる** ✓。
2. **Chebotarev 整合(定理 PENT-IMP の要求)**: per-m $=[1,1,1,1]$ ⟹ $\widetilde\chi\vert_{\mathrm{im}(\mathrm{red})}$ は $(\mathbf Z/5)^\times\cong C_4$ への**全単射** ⟹ $u\in\{2,3\}$ が実現される ✓。
 **これは v1 census の $[5,0,0,5]$ が満たせなかった条件である。** fine 水準へ上げたことで**不可能な署名が消えた** — 水準の取り違えが原因だったという `pent_exists_level_v1` の診断を支持する。

---

## 4. 残る緊張(主張はしない)

$\mathrm{im}(\mathrm{red})\cong C_4$ は、$F_{20}=C_5\rtimes C_4$ の **$C_5$(= $\sqrt[5]2$ 方向 = Kummer 方向)が持ち上がらない**ことを意味する。一方 v4 は $\mathrm{Ih}_{N_A}$ が $F_{20}$ 全体へ全射(⟹ 20/20 が持ち上がるべき)と主張する。**両立しない。**

**現時点では v4 を倒さない。** 理由:
- 本走は **GAP 単系統・規約 1 通り**(論文順の語を評価時に反転)。過去 2 回、規約の取り違えが数値を壊した実績がある(hexagon 向き・fine/coarse 水準)。
- $x_{13}$ の向き、$A/B$ の左右、(2.18)(2.19) の defect の並べ方に**まだ自由度が残る**。§2 の「c1=c2 が同時に 5 か 0」という強い同期は、規約が整合している徴候ではあるが証明ではない。
- **次の判別**: (a) Sol による独立実装(便 91)、(b) $N^{(19)}$(論文実データ 216/36)での **refined-fibre hexagon の較正** — $N^{(34)}$ の 4096 は pentagon evaluator の較正にしかならない(Sol 指摘)。(b) が通れば本走の $4$ は信用してよく、v4 との衝突を正面から扱う段階に入る。

---

## 5. 格付け

| 主張 | 格 |
|---|---|
| $\lvert PB_3/(K_\pi)_{PB_3}\rvert=7500$・$\lvert F_2/(K_\pi)_{F_2}\rvert=1500$ | **machine-measured** |
| **$c\notin(K_\pi)_{PB_3}$**(⟹ 簡約 hexagon は fine 水準で無効) | **machine-measured + proof**(等価性は $c\in N$ を要する) |
| $H_3$($PB_3$ 水準)$=C_5^3$・中心的 / ($F_2$ 水準)$=C_5^2$ | **machine-measured**($F_2$ 水準は司令塔値と独立一致) |
| (T2) 4/20・per-m $[1,1,1,1]$ / (T3) $\lvert\mathrm{im}(\mathrm{red})\rvert=4$ | **machine-measured(単系統・規約 1 通り)** |
| 律速は fine hexagon であって pentagon ではない | **machine-measured**(§2) |
| 構造検査 2 件 PASS(部分群位数・Chebotarev) | **proof + 実測** |
| v4 との衝突 | **UNKNOWN**(規約自由度が残る・§4)。**v4 を倒す主張はしない** |
