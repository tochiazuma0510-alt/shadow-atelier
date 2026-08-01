# 定理 GTPI — `red : GT(K_π) → GT(N_A) ≅ F₂₀` は群同型(PB₃ 実装模型水準)

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 委嘱: 司令塔 札 **P6-1**(裁定 355 採択の発案 P6-1)
- **IF-FIRST 凍結(計算前)**: `docs/notes/gtpi_cv9_freeze_v1.md` SHA-256 `b5b3969812bc168a7995efba556e46ef217e1fd710bb66b4c6bc53b819cd539c`
- **本走**: `search/probe/wac_v1/gtpi_closure_20260801.g`(`4b28c438f0f0255c39a62dc302a43d89afcaee538a19b77773db4be07c4d46f4`)/ cert `search/certs/gtpi_closure_20260801.json`(`761785795c1346b06b575caa27f0a82dd96c2ed97efcea874d3d3cc2bf683f35`)
- **格**: **紙の証明**(§2)+ **単系統 GAP の独立確認**(§3)。**cross-checked ではない**(CV-9 主検問未実施)。**Lean verified ではない。**
- **LEVEL CAVEAT(削除禁止)**: すべて **$PB_3$ 実装模型水準**。$PB_4$ 水準(2106.06645 Prop 2.11 / 2008.00066)の主張ではない。§6 でこの caveat が**現行構成では内部で解消できない**ことが確定した。

---

## 0. 判定(先に 6 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | $\mathcal G$(精 shadow)は合成で閉じるか | **閉じる。紙で証明した**(定理 CLOSURE)。機械は 400/400 で独立確認 |
| **②** | `red` は群同型か | **同型。紙で証明した**(定理 GTPI)。$\ker=1$ は**計算前に**決まる(補題 UNIV) |
| **③** | 相手は $F_{20}$ か | **然り**。$\mathcal G\cong\mathcal S\cong H=N_{S_5}(\langle\bar x\rangle)$、`IdGroup`$=[20,3]$、$C_5{:}C_4=\mathrm{AGL}(1,5)$。位数分布 $1^1 2^5 4^{10} 5^4$ = 予言と一致 |
| **④** | probe は spot-check に降格したか | **した**(§3)。紙が先に閉じたので、400 対は**確認**であって根拠ではない |
| **⑤** | W92-1 の 3 件は | **(i) 閉鎖・(iii) 閉鎖**(いずれも PB₃ 模型水準)。**(ii) PB₄ isolated 性は UNKNOWN のまま** |
| **⑥** | groupoid 性は本質だったか | **否**。$K_\pi$ 窓では $\mathrm{GTSh}(K_\pi,K_\pi)$ が全体で、型修正 3 択は**不要になった** |

> **一行で**: 決め手は「$c_4$ が探索宇宙を導来部分群 $A\cong A_5$(60 元)に閉じ込め、$\rho\vert_A$ が同型である」という**一行の構造事実**。ここから fiber 濃度 1・red 単射・閉性が芋づるで出る。7500 元の話が 60 元の話に潰れる。

---

## 1. 記号(`pent_settled_cent_v1.md` から継承・再定義しない)

$P:=P_N=\langle\bar x,\bar y\rangle=A_5$、$F=\langle x,y,c\rangle$ 自由、$\Psi:F\to E^5$(**反**準同型)、$Q_P:=\Psi(F)$、$\lvert Q_P\rvert=7500$、$\rho:Q_P\to P$(準同型)、$\theta:F\to P$(順方向)。

> **定理 STR**(既証・`pent_settled_cent_v1.md` §1): $Q_P=A\times V$、$A:=[Q_P,Q_P]\cong A_5$、$V:=Z(Q_P)=\ker\rho\cong C_5^3$、$\rho\vert_A:A\xrightarrow{\sim}P$。
> **定理 ORI**(既証・§2): $\theta(\mathrm{WordOf}(q))=\tau(\rho(q))$、$\tau(g)=\hat c(g)^{-1}$、$\hat c=\mathrm{conj}_\kappa$、$\kappa=(1,4)(2,5)$。

**粗**: $\mathcal S:=\mathrm{GT}(N_A)=\{(m,f)\}$、$\lvert\mathcal S\rvert=20$、$\Phi_{m,f}:\bar x\mapsto\bar x^u,\ \bar y\mapsto f^{-1}\bar y^uf$($u=2m+1$)。
**精**: $\mathcal G:=\{(m,q):m\in\{0,1,3,4\},\ q\in Q_P,\ \mathrm{Chk6}(m,q)\ \text{全 true}\}$。
**作用(T′ 整合規約・裁定 298)**: $T'_{m,q}:\Psi(x)\mapsto\Psi(x)^u,\ \Psi(y)\mapsto q\Psi(y)^uq^{-1},\ \Psi(c)\mapsto\Psi(c)^u$。
**$\Phi'$**: $\Phi'_{m,g}:\bar x\mapsto\bar x^u,\ \bar y\mapsto g\bar y^ug^{-1}$。$\Phi'_{m,g}=\Phi_{m,g^{-1}}$。
**合成 $\circ$ は「右を先に施す」**(凍結 §2.4)。

---

## 2. 紙の証明

### 補題 UNIV(探索宇宙の潰れ)【定理・3 行】

> `Chk6` の条件 $c_4$ は逐語で「$q\in[Q_P,Q_P]$」である。よって定理 STR から:
> 1. $\mathcal G\subseteq\{0,1,3,4\}\times A$、$\lvert A\rvert=60$。**$4\times60=240$ 組の走査は近道ではなく悉皆**である。
> 2. $\rho\vert_A$ は同型ゆえ $q\mapsto\rho(q)$ は $\mathcal G$ 上単射。$\theta\circ\mathrm{WordOf}\vert_A=\tau\circ\rho\vert_A$ も($\tau$ 全単射ゆえ)単射。
> 3. $A\cap V=1$ ゆえ $\ker(\mathrm{red})=1$。
> 4. 各 fiber(125 元)と $A$ の交わりは**ちょうど 1 元**。

**証明.** 1. は $c_4$ の定義そのもの。2.–4. は $Q_P=A\times V$、$\ker\rho=V$、$\rho\vert_A$ 同型(定理 STR)から直ちに従う。∎

> **★ 系 UNIV′(W92-1 (i) の閉鎖 — PB₃ 模型水準)**
> **精 shadow の代表 $q$ は fiber ごとに一意である。** ゆえに「representative 非依存性」という問題自体が消える(選ぶ自由度がない)。
> ⟹ cert `pent_t2t3_v32` の 20 行すべての `c4_pass = 1` は**測定結果ではなく構造の帰結**である(系 KQ と同じ型の格上げ)。

### 補題 SHAPE(合成が $T'$ 形に閉じる)【定理・4 行】

> $T'_1:=T'_{m_1,q_1}$、$T'_2:=T'_{m_2,q_2}$ が $Q_P$ の自己準同型なら
> $$T'_1\circ T'_2=T'_{m'',q''},\qquad q''=T'_1(q_2)\,q_1,\qquad 2m''+1\equiv u_1u_2\ (\mathrm{mod}\ 5).$$
> さらに $m''\equiv 2m_1m_2+m_1+m_2\ (\mathrm{mod}\ 5)$ — **正典 2401.06870 (3.53) の $m$-成分と同一**。

**証明.** $\Psi(x),\Psi(y),\Psi(c)$ はいずれも位数 5(機械: `ord Psi(x)=ord Psi(y)=ord Psi(c)=5`)なので指数は mod 5 でよい。
$T'_1(T'_2(\Psi(x)))=T'_1(\Psi(x)^{u_2})=\Psi(x)^{u_1u_2}=\Psi(x)^{u''}$。$\Psi(c)$ も同様。
$$T'_1(T'_2(\Psi(y)))=T'_1\bigl(q_2\Psi(y)^{u_2}q_2^{-1}\bigr)=T'_1(q_2)\,\bigl(q_1\Psi(y)^{u_1}q_1^{-1}\bigr)^{u_2}\,T'_1(q_2)^{-1}=q''\,\Psi(y)^{u''}\,q''^{-1}.$$
$m$-成分: $2(2m_1m_2+m_1+m_2)+1=(2m_1+1)(2m_2+1)=u_1u_2$。∎

> **系 SHAPE′.** $q_1,q_2\in A\Rightarrow q''\in A$。
> **証明.** $A=[Q_P,Q_P]$、$T'_1$ 準同型ゆえ $T'_1(A)=[T'_1(Q_P),T'_1(Q_P)]\le A$。積も $A$ の中。∎

### 補題 DICT(2 座標の辞書 — ★ 4 件目の規約事故を殺す一行)【定理】

> (a) $T'_{m,q}$ が $Q_P$ の**自己同型**なら $\rho\circ T'_{m,q}=\Phi'_{m,\rho(q)}\circ\rho$。
> (b) $\hat c\circ\Phi_{m,f^\kappa}=\Phi_{m,f}\circ\hat c$。
> (c) ⟹ 著者側ラベル $f_i:=\theta(\mathrm{WordOf}(q_i))$ について
> $$\boxed{\ \theta(\mathrm{WordOf}(q''))=f_1\cdot\Phi_{m_1,f_1}(f_2)\ }$$
> すなわち **精合成は著者座標で正典 (3.53) そのものになる**。

**証明.** (a) $V=Z(Q_P)=\ker\rho$ は特性部分群、$T'$ は自己同型ゆえ $T'(V)=V$。よって $\rho\circ T'$ は $\rho$ を経由し、誘導写像は生成元で $\bar x\mapsto\bar x^u$、$\bar y\mapsto\rho(q)\bar y^u\rho(q)^{-1}$、すなわち $\Phi'_{m,\rho(q)}$。
(b) $\hat c=\mathrm{conj}_\kappa$、$\kappa^2=1$、$\hat c(\bar x)=\bar x^{-1}$、$\hat c(\bar y)=\bar y^{-1}$。生成元で両辺を評価:
$\hat c\Phi_{m,f^\kappa}(\bar x)=\hat c(\bar x^u)=\bar x^{-u}$、$\Phi_{m,f}\hat c(\bar x)=\Phi_{m,f}(\bar x^{-1})=\bar x^{-u}$。
$\hat c\Phi_{m,f^\kappa}(\bar y)=\hat c\bigl((f^\kappa)^{-1}\bar y^uf^\kappa\bigr)=\hat c(f^\kappa)^{-1}\bar y^{-u}\hat c(f^\kappa)=f^{-1}\bar y^{-u}f$(∵ $\hat c(f^\kappa)=f^{\kappa\kappa}=f$)、
$\Phi_{m,f}\hat c(\bar y)=\Phi_{m,f}(\bar y^{-1})=(f^{-1}\bar y^uf)^{-1}=f^{-1}\bar y^{-u}f$。生成元で一致。∎
(c) $g_i:=\rho(q_i)$、$f_i=\tau(g_i)$、$g_i^{-1}=\hat c(f_i)=f_i^{\kappa}$。$\tau$ は反自己同型なので
$$f''=\tau(\rho(q''))\overset{\text{(a)}}{=}\tau\bigl(\Phi'_{m_1,g_1}(g_2)\,g_1\bigr)=\tau(g_1)\cdot\tau\bigl(\Phi'_{m_1,g_1}(g_2)\bigr)=f_1\cdot\tau\bigl(\Phi_{m_1,f_1^\kappa}(g_2)\bigr),$$
$$\tau\bigl(\Phi_{m_1,f_1^\kappa}(g_2)\bigr)=\hat c\bigl(\Phi_{m_1,f_1^\kappa}(g_2)^{-1}\bigr)=\hat c\,\Phi_{m_1,f_1^\kappa}(g_2^{-1})\overset{\text{(b)}}{=}\Phi_{m_1,f_1}\bigl(\hat c(g_2^{-1})\bigr)=\Phi_{m_1,f_1}(\tau(g_2))=\Phi_{m_1,f_1}(f_2).\ \blacksquare$$

> **注**: 対話帳 **T-21 補題 OPP**(第二インスタンス・9600 対機械確認)の $g_{12}=\Phi'_{m_1,g_1}(g_2)g_1$ は本補題 (a) の粗水準版である。**独立に立てられた 2 本が同じ辞書を指している。**

### 補題 COARSE(粗側は群)【正典 + 3 行】

> $\mathcal S=\mathrm{GT}(N_A)$ は (3.53) の積で閉じ、$(m,f)\mapsto\Phi_{m,f}$ は群同型 $\mathcal S\xrightarrow{\sim}H:=N_{S_5}(\langle\bar x\rangle)\cong F_{20}$ を与える。

**証明.** 20 個すべてで $\Phi_{m,f}$ は well-defined(機械)、$P=A_5$ 単純かつ $\Phi_{m,f}(\bar x)=\bar x^u\ne1$ ゆえ $\Phi_{m,f}\in\mathrm{Aut}(P)$、すなわち $\ker T_{m,f}=N_A$ で**全 shadow が settled**。ゆえに $N_A$ は **isolated**、正典 2401.06870 **Prop 3.14** により $\mathrm{GT}(N_A)=\mathrm{GTSh}(N_A,N_A)$ は**有限群**。
$\Phi$ の乗法性は生成元計算: $\Phi_1\Phi_2(\bar y)=\Phi_1(f_2^{-1}\bar y^{u_2}f_2)=(f_1\Phi_1(f_2))^{-1}\bar y^{u_1u_2}(f_1\Phi_1(f_2))$。$\Phi$ は単射(20 個が相異なる)で $\lvert H\rvert=20$ ゆえ全射。$H=N_{S_5}(\langle\bar x\rangle)\cong\mathrm{AGL}(1,5)=F_{20}$ は `pent_settled_cent_v1.md` §7 で既証。∎

### ★ 定理 CLOSURE(精側の閉性)【定理】

> $(m_1,q_1),(m_2,q_2)\in\mathcal G$ ならば $(m'',q'')\in\mathcal G$。

**証明.** $T'_{m_i,q_i}$ は $Q_P$ の自己同型(裁定 298: 20/20 well-defined かつ核自明、有限群ゆえ全単射;本走で再現)。
1. 系 SHAPE′ より $q''\in A$。
2. 補題 DICT(c) より $\theta(\mathrm{WordOf}(q''))=f_1\Phi_{m_1,f_1}(f_2)$、補題 COARSE よりこれは $(m'',\cdot)\in\mathcal S$ を与える。この元を $(m'',f^\sharp)$ と書く。
3. `red` の全射性(本走 exhaustive scan で $\mathrm{red}(\mathcal G)=\mathcal S$;Sol 便 92 **F92-1.2** の cross-checked 全射性とも一致)より、$\exists(m'',q^*)\in\mathcal G$ で $\theta(\mathrm{WordOf}(q^*))=f^\sharp$。
4. $q^*\in A$($c_4$)、$q''\in A$(1.)、$\theta\circ\mathrm{WordOf}\vert_A$ は単射(補題 UNIV 2.)、両者の像は等しい ⟹ $q^*=q''$。
∴ $(m'',q'')=(m'',q^*)\in\mathcal G$。∎

> **注(なぜ hexagon/pentagon を直接扱わずに済んだか)**: $c_1,c_2,c_3$ の閉性を**個別に検証していない**。代わりに「合成結果は $A$ の中にあり、$A$ の元は粗ラベルで一意に決まる」ことで、**すでに $\mathcal G$ に属すると分かっている元と同一視**した。$c_4$ の一行が閉性の証明を肩代わりしている。

### ★★ 定理 GTPI【定理】

> $(\mathcal G,\ast)$ は位数 20 の群であり、
> $$\mathrm{red}:(\mathcal G,\ast)\longrightarrow(\mathcal S,\circ),\qquad (m,q)\longmapsto\bigl(m,\ \theta(\mathrm{WordOf}(q))\bigr)$$
> は**群同型**である。したがって
> $$\mathrm{GT}(K_\pi)\ \cong\ \mathrm{GT}(N_A)\ \cong\ N_{S_5}(\langle\bar x\rangle)\ \cong\ \mathrm{AGL}(1,5)=F_{20}=C_5\rtimes C_4 .$$
> 単位は $(m,q)=(0,1_{Q_P})$。位数分布は $1^1\,2^5\,4^{10}\,5^4$。

**証明.** 定理 CLOSURE より $\ast$ は $\mathcal G$ 上の二項演算。補題 SHAPE より $\ast$ は $T'$ の合成に対応するから結合的で、$T'_{0,1}=\mathrm{id}_{Q_P}$ より $(0,1)$ が単位。補題 DICT(c) より `red` は乗法的、補題 UNIV 3. より単射、上の 3. より全射。ゆえに `red` は**モノイド全単射**。$\mathcal S$ は群(補題 COARSE)なので群構造が $\mathcal G$ に引き戻され、`red` は群同型。$\mathcal S\cong H\cong F_{20}$ は補題 COARSE。∎

> ### 系 GTPI′(W92-1 (iii) の閉鎖 — PB₃ 模型水準)
> `red` は群準同型であり、$\mathrm{GT}(K_\pi)$ は群である。W92-1 が「群全射へ昇格する直前には最優先 blocker」とした (i) representative 非依存性 と (iii) multiplication compatibility は、**PB₃ 実装模型水準で閉じた**。残るのは **(ii) source kernel の $PB_4$ isolated 性**(§6)。

> ### 系 GTPI″(型修正 3 択は不要)
> 委嘱は「不一致 ⟹ groupoid 性が本質と確定・型修正 3 択を記録」を予備していたが、**不一致は起きなかった**。$K_\pi$ は(PB₃ 模型水準で)isolated であり、$\mathrm{GTSh}(K_\pi,-)$ の非自明な射(source ≠ target)は**この窓には存在しない**。groupoid 性は本質ではなかった。

---

## 3. 機械の独立確認(紙が先に閉じたので **spot-check 格**)

`gtpi_closure_20260801.g` / cert 同名。**全 400 対**(spot ではなく全数だが、格としては確認)。

| 予言(凍結済) | 実測 |
|---|---|
| P-GTPI-1 合成が $T'$ 形・$q''=T'_1(q_2)q_1$ | **400/400** |
| $m''$ の NF が正典 (3.53) と一致 | **400/400** |
| P-GTPI-2 閉性 $(m'',q'')\in\mathcal G$ | **400/400**(失敗 0) |
| P-GTPI-3 $\lvert\mathcal G\rvert=20$・fiber 濃度 | **$\lvert\mathcal G\rvert=20$(悉皆 240 走査)・fibre_counts_seen $=[1]$・$\lvert A\cap\ker\rho\rvert=1$・$\rho\vert_A$ 全単射 true** |
| P-GTPI-4 red 準同型(著者座標) | **400/400** |
| P-GTPI-4 red 準同型(我々座標・T-21 OPP 形) | **400/400** |
| P-GTPI-5 単位 $(0,1_{Q_P})$・逆元 | 単位 index 1・`all_have_inverses` true |
| P-GTPI-6 $F_{20}$ | `IdGroup(G)=[20,3]`・`C5 : C4`・`IdGroup(H)=[20,3]`・結合律 true・ラテン方陣 true・右正則表現が準同型 true・**位数分布 $[[1,1],[2,5],[4,10],[5,4]]$ = 予言と一致** |
| P-GTPI-7 粗側 literal 閉性 | **400/400**・$\lvert\Sigma_m\rvert=[25,25,25,25]$・$\lvert S_m\rvert=[5,5,5,5]$・Hex が剰余類ごとに 1 個 true |
| 明示同型 $(m,q)\mapsto\Phi'_{m,\rho(q)}$ | defined / distinct / $\in H$ / 準同型(右先) **すべて true** |

**事前登録の照合**: `pre_registered_rows_match = true`(cert `pent_t2t3_v32_20260801.json` の 20 行と GAP 内再生成が集合として一致)。

### 3.1 dummy の識別力(CV-9-5 / §1.3.2)

| dummy | 層 | 結果 | 識別力 |
|---|---|---|---|
| **DUM-G1** $q\mapsto qz$($z\in V\setminus1$) | 出力層 | **粗ラベル不変 true・$\rho$ 不変 true**、しかし `Chk6=[F,F,F,F,T,F]`・$\mathcal G$ 外・合成が $\mathcal G$ を出る **true** | **あり**(粗側だけ見ていると区別できない元を、精側は落とす) |
| **DUM-G2** 積の**逆順** $q_1\cdot T'_1(q_2)$ | 出力層 | $\mathcal G$ に落ちるのは **192/400**(**208 失敗**) | **あり**(順序に関して識別する) |
| **DUM-G3** 混成規約 $T$($q^{-1}(\cdot)q$) | 出力層 | $T$ は **12/20** でしか定義されず、定義される 240 対のうち $\mathcal G$ 到達は **160/240**(**80 失敗**)。核サイズ $\{-1,1,60\}$ = 裁定 293 の 4/8/8 構造を再現 | **あり**(規約選択に関して識別する) |
| **DUM-G4** 非 charming $m=2$($u\equiv0$) | 入力層 | $T'$ は「定義される」が**核 7500**(自明写像)。$\mathrm{Hex}(2,f)$ の解は $f$ が 1 個のみ | **あり**(入力宇宙の外に出る) |

**competitor universe**(凍結 §1.3): 合成結果の競合先は $\{0,1,3,4\}\times Q_P$ の **30000 組**。1 組あたり偶然一致は $1/1500$。400/400 は偶然では説明できない。

---

## 4. 【GAP】— 埋められなかった穴(隠さず名指し)

> ### 【GAP-GTPI-1】模型忠実性(最重要・W92-1 (iii) の真の残り)
> 本稿は $\mathcal G$ = 「`Chk6` を満たす $(m,q)$」についての定理である。**`Chk6` が正典 2401.06870 の GT-shadow 条件と同値であることは証明していない。** ゆえに「$\mathrm{GT}(K_\pi)\cong F_{20}$」は**厳密には模型についての主張**である。
> **状況証拠(証明ではない)**: (α) $\mathcal G$ は正典 (3.53) の積で literal に閉じた(400/400)。(β) $m$-成分 NF が (3.53) と 400/400 一致。(γ) 著者座標での red が (3.53) の準同型になった。**仕様が違っていればこの 3 つが同時に成り立つ理由がない。**
> **要請**: Sol の独立判読(監査点 A)。

> ### 【GAP-GTPI-2】$PB_4$ 水準(LEVEL CAVEAT)
> §6 で「現行構成には $PB_4$ 水準の窓が存在しない」ことが**確定**した。内部では解消できない。**【文献要請 U-PB4】**(§6.3)。

> ### 【GAP-GTPI-3】CV-9 主検問
> 本稿の起草者は仕様・実装・一次 grading の**当事者**である。凍結 §5 の通り、**非当事者(falsifier / opus・max)の判読が済むまで cross-checked と書かない**。本走はあくまで**単系統 + 紙**。

> ### 【GAP-GTPI-4】逆元の明示形
> $\mathcal G$ が群であることは示したが、**逆元 $(m,q)^{-1}$ の閉じた式**(正典 (3.54) の精水準版)は導いていない。機械では `all_have_inverses = true` のみ。次の一歩の候補。

---

## 5. 上位の主張への含意

1. **W92-1 の 3 件中 2 件が閉じた**(PB₃ 模型水準): (i) representative 非依存性 → 系 UNIV′(fiber 濃度 1 ゆえ自由度が存在しない)。(iii) multiplication compatibility → 定理 GTPI。**残りは (ii) のみ**。
2. **裁定 298 の「$K_\pi$ isolated(candidate)」が定理になった**(PB₃ 模型水準): 20/20 settled ⟹ isolated ⟹ Prop 3.14 で群。本稿はさらに**同型の相手まで特定**した。
3. **`red` の核が自明**であることは、`GT(K_π) → GT(N_A)` の「情報損失ゼロ」を意味する。すなわち **$C_5^3$ 分の精密化は GT-shadow を 1 個も増やさない**。これは「精密化しても shadow が増えない窓」の実例であり、dihedral 予想の全射性を問う際の**分母が増えない**ことを示す(この窓については、粗窓での算術性が分かれば精窓でも分かる)。
4. **§3 の絵が一様になった**: 20 全部が settled・20 全部が lift をもち・lift は一意・群として $F_{20}$。`pent_settled_cent_v1.md` §9.4 が予告した「v4(20 全 arithmetical)との整合はむしろ良くなる」が、群構造の水準で実現した。
5. **【GAP-PSC-1】の完全な後始末**: 裁定 293 の 4/8/8 は artifact であり、整合規約では 20/20。本走はさらに、**整合規約でのみ群になる**ことを示した(DUM-G3: 混成規約は 12/20 でしか定義されず群にならない)。**規約の正否が「群になるかどうか」で判定できる**ようになった — これは便 92 F92-1.1 の指紋論法より強い判別法である。

---

## 6. P6-2 — $PB_4$ 水準検査のサイズ見積もり(先行 30 分枠)

**probe**: `search/probe/wac_v1/gtpi_pb4_size_20260801.g`(窓ブロックは逐語移植・単系統)

### 6.1 実測

| 量 | 値 |
|---|---|
| $\lvert E\rvert$($=\langle a_E,b_E\rangle$) | **360** = $S_3\times A_5$ |
| $\lvert Q_P\rvert=\lvert PB_3/K_\pi\rvert$ | 7500、$\lvert[Q_P,Q_P]\rvert=60$ |
| $X_{12},X_{13},X_{14},X_{23},X_{24},X_{34}$ の位数 | すべて **5** |
| $Q_4:=\langle X_{ij}\rangle\le E$ | **$\lvert Q_4\rvert=60$、$A_5$** |
| $[Q_4,Q_4]$ | **60、$A_5$**(完全) |
| $\langle X_{12},X_{13},X_{23}\rangle$ | 60、$A_5$、**$=P_N$**(等号 true) |

### 6.2 ★ 判定: **現行構成には $PB_4$ 水準の窓が存在しない**

構成に現れる 6 個の $PB_4$ 生成元 $X_{ij}$ の像は、**すべて粗窓 $P=A_5$ の中に収まっている**($Q_4=P_N$)。精密化 $C_5^3$ は $E^5$ への **5 複製の packing**(pentagon の 5 頂点)から来るのであって、$PB_4$ の窓の精密化から来るのではない。

⟹ **coset enumeration 以前の問題**である。「$K_\pi$ 対応部分群の指数」を測る対象そのものが構成の中にない。

**引き戻し窓との対比**(記録のため): $PB_4\twoheadrightarrow PB_3$(第 4 ストランドを忘れる)は全射だから、$K_\pi$ の引き戻しの指数は**ちょうど 7500**(列挙不要)。しかしこの窓は Fadell–Neuwirth 核 $F_3$ を丸ごと含むので $PB_4$ 商が $Q_P$ に潰れ、$PB_4$ 固有の条件がすべて空虚になる ⟹ **使えない**。

### 6.3 【文献要請 U-PB4】

- **困難**: $K_\pi\le PB_3$(指数 7500・$PB_3/K_\pi\cong A_5\times C_5^3$)に対応する $PB_4$ の窓 $\tilde K\trianglelefteq B_4$ を、手持ちの正典(2401.06870 / 2405.11725 / 2106.06645 抽出ノート / 定義ノート)から**構成できない**。2106.06645 Prop 2.11(C1)の settled 条件は $PB_4$ 水準で述べられているが、**窓の定義**(($PB_4$ の charming subgroup の定義 / $PB_3$ 窓からの標準的持ち上げの有無 / $PB_4/\tilde K$ の作り方)は arXiv **2008.00066** にあり未入手。§6.2 により、この不足は「後で埋める注意書き」ではなく**測定の対象が定義できない**という実体的閉塞である。
- **欲しい結果の型**:
  - **(α)** $PB_4$ の charming/窓部分群の定義、および $PB_3$ の窓からの標準的持ち上げが存在するか(存在しないなら「独立に選ぶ」ことの意味)。
  - **(β)** $\lvert PB_4/\tilde K\rvert$ の見積り、とくに **Fadell–Neuwirth 核 $F_3$ の像の位数 $d$**。$\lvert PB_4/\tilde K\rvert=7500\,d$ の形になるはず。
  - **(γ)** 2106.06645 **Prop 2.11** の settled の正確な定式化(kernel を取る対象・水準)。
- **見積もり(条件付き)**: 本走の教訓は「探索宇宙は $c_4$ により**導来部分群**に潰れる」ことである。同じ形が $PB_4$ 水準でも成り立つなら、**scan コストは $\lvert[PB_4/\tilde K,\ \cdot\ ]\rvert\times4$** であり、$d\le10^3$ 程度なら 8GB で十分に回る。**爆発するのは $[Q,Q]$ 自身が大きい($\gtrsim10^6$)場合のみ。** すなわち「$PB_4$ 検査は原理的に重くない — 重いのは窓の定義が無いこと」。
- **格**: **UNKNOWN**(coset enumeration は実施していない — 対象が定義できないため実施できない)。**外部検索は一切していない**(文献ゲート遵守)。

---

## 7. 格付け表

| 主張 | 格 |
|---|---|
| 補題 UNIV(探索宇宙 $=A$・fiber 濃度 1・$\ker\mathrm{red}=1$) | **定理**(3 行・定理 STR から) |
| 系 UNIV′(W92-1 (i) 閉鎖・PB₃ 模型水準) | **定理**(系) |
| 補題 SHAPE / 系 SHAPE′ | **定理**(生成元計算) |
| **補題 DICT**($\hat c\Phi_{m,f^\kappa}=\Phi_{m,f}\hat c$ と (3.53) 一致) | **定理** + 400/400 機械・T-21 補題 OPP と独立一致 |
| 補題 COARSE($\mathcal S$ は群・$\cong F_{20}$) | **定理**(正典 Prop 3.14 + 3 行) |
| **定理 CLOSURE** | **定理** + 400/400 機械 |
| **定理 GTPI**(`red` 群同型・$\cong F_{20}$) | **定理**(紙)+ 機械独立確認。**単系統・Sol 監査前・CV-9 主検問前** |
| 系 GTPI′(W92-1 (iii) 閉鎖) | **定理**(系・PB₃ 模型水準) |
| 系 GTPI″(型修正 3 択は不要) | **定理**(系) |
| 【GAP-GTPI-1】模型忠実性 | **未証明**(状況証拠 3 本) |
| $PB_4$ 水準 | **UNKNOWN**。§6.2 で「現行構成に窓が無い」ことは**確定**(これは結果) |
| 逆元の閉じた式 | **未着手** |

---

## 8. Sol への申し送り(監査の優先順)

- **監査点 A(最優先)**: **補題 UNIV** の一行 — 「`Chk6` の $c_4$ は $q\in[Q_P,Q_P]$ であり、定理 STR で $[Q_P,Q_P]=A\cong A_5$、$\rho\vert_A$ 同型」。**本稿はここに全体重を乗せている。** $c_4$ が正典の GT-shadow 条件($f\in$ 導来部分群、Drinfeld の $f\in[\hat F_2,\hat F_2]$ の類似)の正しい実装か、独立に判読してほしい。ここが誤りなら補題 UNIV・定理 CLOSURE・定理 GTPI が同時に倒れる。
- **監査点 B**: **補題 DICT (b)** $\hat c\Phi_{m,f^\kappa}=\Phi_{m,f}\hat c$。4 行の生成元計算だが、$\hat c(f^\kappa)=f$($\kappa^2=1$)の一段が効いている。$f/f^{-1}$ 族の 4 件目が潜むならここ。
- **監査点 C**: **補題 COARSE** の正典引用 — 「全 shadow settled ⟹ isolated ⟹ Prop 3.14 で群」。$N_A$ が Prop 3.14 の前提(charming・$N_{\rm ord}$ 一致等)を満たすかを正典側から確認してほしい。
- **監査点 D**: **定理 CLOSURE の 4 段目**。「$q^*,q''\in A$ で像が等しいから等しい」— ここで $c_1,c_2,c_3$ の閉性を**迂回**している。迂回が正当か(すなわち $\mathcal G$ の元が粗ラベルで一意に決まることが、閉性の証明として十分か)。
- **監査点 E**: **§6.2** の判定「$Q_4=\langle X_{ij}\rangle=P_N$ ゆえ現行構成に $PB_4$ 窓は無い」。これが正しければ LEVEL CAVEAT は**内部では永久に解消できない**ことになり、【文献要請 U-PB4】の優先度が上がる。
- **申し送り**: 本稿が通れば、`GT(K_π)` は「群・位数 20・$F_{20}$・`red` は同型」まで確定し、**便 92 F92-1.3 が禁じた「群準同型を作ってはならない」の禁が(PB₃ 模型水準で)解ける**。禁の解除は Sol の判定事項なので、こちらからは主張しない。

---

# 追記 A(便 99 検収・裁定 412)— **総合格の確定 P99-2.2**

> **追記型**: §0–§8 の本文を**一切改変しない**。以下は**格の確定**である。
> 起草: 数学者(Opus 5)・2026-08-02。入力 = **Sol 便 99 返信 F99-2.3 / P99-2.2**(`sol/sol_reply_99_math26.md` §2)。

## A.1 検収の結果(F99-2.3)

**条件付き PASS。**

- ★ **通った**: $(A')$ $c_3$-pentagon を含む **source-map / 定義式の紙上忠実性**は閉じた。
- ⚠ **通らなかった読み**: 「**紙証明が probe を単なる spot-check に降格した**」とは**書けない**。CLOSURE(20 lifts の存在・全射)および PB4-settled/NFI は**有限計算に論理依存**するからである。
⟹ §3 の見出し「機械の独立確認(紙が先に閉じたので **spot-check 格**)」は、**§3 の probe の格**としては妥当だが、**定理 CLOSURE 全体が紙で閉じたという含意では読まない**こと。

## A.2 ★ 確定文 P99-2.2(**Sol 逐語** — CLAIMS 用)

> 固定した $K_\pi/N_0$ に対し、source-map の定義式と $c_3$-pentagon の向きは **paper-audited** である。**CLOSURE**(20 lifts の存在・全射)および **PB4-settled/NFI** の有限結論は **finite exhaustive artifact に本質的に依存**する。総合格は **paper-proof + finite-exhaustive candidate**。**settled 段は別の独立照合が付かない限り single lane** であり、**Lean verified ではない**。

## A.3 CLAIMS の二行分離(**記帳済**)

Sol の指示「**数値群構造の主張と canonical-fidelity の主張は CLAIMS で別行にする**のが最も安全」に従い、`provenance/CLAIMS.md` の **C-GTPI** が既に二行構成で記帳されている(司令塔の記帳・2026-08-02 時点で存在を確認)。

| 行 | 内容 | 格 |
|---|---|---|
| **行 1(数値群構造)** | `red: GT(K_π) ≅ GT(N_A) ≅ AGL(1,5) = F₂₀`・GTPI$^{PB_4}$ で $N_0$ isolated・$\mathrm{GT}^\heartsuit(N_0)\cong F_{20}$ | **paper-proof + finite-exhaustive candidate**。CLOSURE と PB4-settled/NFI は有限計算に論理依存・**settled 段は single lane** |
| **行 2(canonical fidelity)** | source-map の定義式と $c_3$-pentagon の向きの正典忠実性 | **paper-audited**(紙) |

**この 2 行を合体させて引用しない。** とくに「$F_{20}$ が正典忠実に照合された」という合成文は**両行のどちらでもない**。

## A.4 この追記が変えないもの

- §2 の紙の証明(補題 UNIV / SHAPE / DICT / COARSE・定理 CLOSURE・定理 GTPI)の**言明と証明**。
- §4 の【GAP】・§6.2 の判定(現行構成に $PB_4$ 水準の窓は無い)・【文献要請 U-PB4】。
- §7 の格付け表(本追記はそれを**上書きせず**、総合格を上に載せる)。
- §8 の Sol 監査点 A–E(**A–D は F99-2.3 の PASS に含まれる**が、**監査点 E**($PB_4$ 窓の不在)は F99-2.3 の判定文に明示がないので**未決として残す**)。
