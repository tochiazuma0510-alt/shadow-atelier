# $u$ 測定キャンペーン 第一波 — **M0(被覆データ)/ M1(順序 passport・凍結)/ M2(種数)** v1

**状態札: `measurement (frozen) / 紙上定理 + GAP 単系統・cross-checked ではない・Lean verified ではない`**
起草: 影工房 数学者(Claude・Opus 5)/ 2026-07-31
委嘱: 司令塔「P1 本峰・$u$ 測定キャンペーン第一波(M0–M2 の実行と M3 の設計)」

> ## 本書の自己制約(prediction/measurement 分離)
> **本書は測定側の文書である。$u$ の値・$\mathrm{ord}([u^{-1}]_9)$・全射性の予想は一切書かない。**
> 予言・NULL 枠・凍結提案はすべて別文書 `docs/notes/u_meas_m3_design_v1.md` §6 に隔離した(PREDICTION_TO_MEASUREMENT_CONTAMINATION 対策)。
> 封印遵守: $K^{(5)}$ 非接触。$u$ 系の封印量非接触。本書で実行した機械計算は**群論(置換)のみ**で、曲線・$\lambda$・主係数・平方類・database には一切接触していない。

**入力正本**: `docs/notes/surj_s4_v2.md` §5(測定計画 M0–M7)/ `docs/notes/surj_s4_v1.md` §5(M0–M7 の項目表)/ `docs/notes/lg34_semilocal_design_v2.md` §1・§2(半局所枠 $B^{\rm sl}_{\rm FC}$)/ `docs/notes/surj_d4_t1_v1.md` §4(命題 W-OBS・TAIL-OBS)/ `docs/notes/sat_l1_v1.md` §1 観察 1.1・§2 定理 RED / `docs/week3-PSL封印計算_opus_v1.md` §1 定理 M1・M2・§5.4(段 S4 の封印 marking)/ `docs/week4-A5算術飽和_v4.md` §2・補題 FC-4($A_5$ 先例)/ `search/certs/sdc_twist_W_E_A10_9t1_20260730.json` / `search/certs/a13_ladder_W_E_A10_9t1_20260730.json` / `docs/week1-定義ノート.md`。**外部文献なし**(文献ゲート遵守。要請は設計書 §5)。

---

## 0. 先に片づける — **窓の同定と枠の辞書**(委嘱の前提に 1 点の是正)

委嘱は「正本 = `surj_s4_v2.md` の M0–M7」「対象窓 = `W-E-A10-9t1`」と指示した。この 2 つは**同一の窓ではない**。ここを曖昧にしたまま passport を凍結すると、後で「どの窓の $u$ を測ったのか」が回復不能になるので、最初に確定させる。

| | **窓 A = `W-E-A10-9t1`**(委嘱の対象窓) | **窓 B = 段 S4**(`surj_s4_v2` の定理の窓) |
|---|---|---|
| $P$ | $A_{10}$、$\lvert P\rvert=1{,}814{,}400$ | $\mathrm{PSL}(2,8)$、$\lvert P\rvert=504$ |
| 生成 marking | $a_1=(1,2)(3,5)(4,10)(6,9)$、$b_1=(2,9,5)(3,4,10)(6,8,7)$(ladder cert) | $S=\begin{pmatrix}1&0\\1&1\end{pmatrix}$、$T=\begin{pmatrix}x^2&x{+}1\\1&x^2{+}1\end{pmatrix}$ over $\mathbf F_8$(封印 JSON 段 S4) |
| $k=N_{\rm ord}=\mathrm{ord}(X)$ | 9 | 9 |
| $e=\mathrm{ord}(w)$ | 9 | 9 |
| $\lvert\mathrm{GT}(N)\rvert$ | 54、$\mathrm{GTSh}\cong\mathrm{Hol}(\mathbf Z/9)$ | 54、$\mathrm{GTSh}\cong\mathrm{Hol}(\mathbf Z/9)$ |
| **(W4)**(全分岐 cusp・$[P:H]=M$) | **空**(命題 TAIL-OBS: $A_{10}$ に指数 9 の部分群は無い) | **成立**($H=$ Borel・指数 9) |
| 適用される橋 | **$B^{\rm sl}_{\rm FC}$**(半局所版・`lg34_semilocal_design_v2` §2.3 補題 B-5$^{\rm sl}$) | $B_{\rm FC}$(BFC v2.15 補題 B-5) |
| 測定量 | $N^{\rm wt}=[u_0]_9\in K^\times/K^{\times9}$(lg34 v2 §1.4) | $[u]_9\in K^\times/K^{\times9}$ |

$$\boxed{\ \textbf{両窓とも }K=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)\textbf{・}M=e=9\textbf{ で、測定量の住処は同じ }K^\times/K^{\times9}\textbf{。しかし被覆は別物である。}\ }$$

### 0.1 【FINDING U-0】`surj_s4_v2.md` §7.1 の証明書は**別窓の測定値**である

`surj_s4_v2.md` §7.1 は「SD-c 証明書(新規生成)」として `search/certs/sdc_twist_W_E_A10_9t1_20260730.json` を掲げ、その表に `|P| = 1814400 = |A10|`・`C_{S10}(X) = 9`・`N_{S10}(<X>) = 54` を書いている。しかし同文書 §1 の窓データは $P=\mathrm{PSL}(2,8)$・$\lvert P\rvert=504$ である。**証明書は窓 A の測定であり、定理 SURJ-S4 の窓 B の測定ではない。**

* 数値が一致するのは偶然ではない: 両窓とも $C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$(位数 9)・$N_{\mathrm{Aut}(P)}(\langle X\rangle)\cong\mathrm{Hol}(\mathbf Z/9)$(位数 54)が成り立つ(窓 B は本書 §1.2 で機械確認)。**したがって「値が合っているから同じ窓」とは言えない。**
* **格の帰結**: 便 86 NOTE 3 の「S4 に監査可能な証明書が無い」は、§7.1 では**解消していない**。窓 B の SD-c 証明書は**未生成**である。
* 委嘱が「対象窓 = W-E-A10-9t1」と書いたのは、この §7.1 の窓すり替えを引き継いだものと推定する。**ただし窓 A も正当な測定対象である**(§0.2)ので、委嘱そのものが無効になるわけではない。
* **自認の範囲**: 私は `surj_s4_v2.md` の起草者(同レイヤー)である。この誤りは私の系統の産物として記録する。

**⟹ 是正案**: (a) `surj_s4_v2.md` §7.1 の表題を「窓 A(W-E-A10-9t1)の SD-c 測定」に改め、窓 B の SD-c は `not_measured` と明記する。(b) 窓 B 用の SD-c 証明書(`sdc_twist_S4_psl28_k9`)を別途生成する。**司令塔裁定案件。**

### 0.2 窓 A は「測れない窓」ではない — 半局所枠なら定義される

`surj_d4_t1_v1.md` §7.2 は窓 A について「$u$ を同定する装置が存在しない ⟹ UNKNOWN」と書いた。**これは `lg34_semilocal_design_v2.md`(2026-07-30)で更新されている**:

* $\Lambda\cong P/H$ は **(W3) だけ**から従い **(W4) は不要**(lg34 v2 §2.1)。窓 A では $H=A_9$(指数 10・$N_{A_{10}}(A_9)=A_9$ を機械確認・§1.1)。
* $X$ は $\Lambda$(10 点)上で巡回型 $(9,1)$、$\lambda^{-1}(0)$ は 2 点 $\{P_0,P_1\}$、指数 $(9,1)$、**両点とも $K$-有理**(補題 SL-1 (b)・両 index 層が singleton)。
* 測定量は $N^{\rm wt}=[u_0]_9$(lg34 v2 §1.4・§2.3 補題 B-5$^{\rm sl}$ (v))。**$t=1$ では三型($N^{\rm wt}$/MARK-U/型 C)が一致**するので定義の選択問題が起きない(命題 LG3)。
* **ただし** 段 II-b(補題 B-6)は `design NOTE`、(W1) は【SD-a】により **UNKNOWN** のまま。**つまり窓 A の測定は「$B^{\rm sl}_{\rm FC}$ が未完のまま幾何量だけ先に測る」形になる。**

$$\boxed{\ \textbf{本書は「窓 A の }[u_0]_9\textbf{ が(半局所枠で)何の被覆の量か」を確定し、その被覆の passport と種数を凍結する。窓 B も同時に測る。}\ }$$

---

## 1. M0 — Belyi 被覆データの再構成

### 1.1 枠組み(両窓共通・辞書の正規化)

正規化は **`week3-PSL封印計算_opus_v1.md` §1 の座標**を採る(定義ノート §1 の $\bar\Delta,\bar\delta$ 規約と同じ):

$$Q=B_3/N,\quad \bar\Delta,\ \bar\delta\in Q,\quad \sigma_1=\bar\delta^{-1}\bar\Delta,\quad \bar X=\sigma_1^2,\quad k=N_{\rm ord}=\mathrm{ord}(\bar X).$$

case A(split-inner・定理 M2)では $Q\cong P\times S_3$、$\bar\Delta=(s,(1\,2))$、$\bar\delta=(t,(1\,2\,3))$、$s^2=t^3=1$、
$$w:=t^{-1}s,\qquad X=w^2,\qquad e=\mathrm{ord}(w).$$

**RED との辞書**(`sat_l1_v1.md` §1 観察 1.1)。$a=\Delta$、$b=\delta$、$a_1=s$、$b_1=t$、$w=b_1^{-1}a_1$、$v=a_1b_1^{-1}$、$\bar x=w^2$、$\bar y=v^2$:

| RED(sat_l1) | 週3-PSL(封印計算) | 本書での採用 |
|---|---|---|
| $\Delta=a$(対合) | $\bar\Delta$ の $P$-成分 $s$ | **$a_1=s$** |
| $\delta=b$(3-元) | $\bar\delta$ の $P$-成分 $t$ | **$b_1=t$** |
| $w=b_1^{-1}a_1$($\sigma_1$ の $P$-成分) | $w=t^{-1}s$ | **一致 — 記号も向きも同一。辞書は恒等写像。** |
| $\bar x=w^2$、$\bar y=v^2$ | $X=w^2$、$Y=\tau(X)$ | **一致**($\tau=\mathrm{Ad}(t)$、機械確認 §1.2) |

$$\boxed{\ \textbf{RED の正規化と }\mathrm{surj\_s4}\textbf{ の正規化は同一である(座標変換不要)。委嘱の「どちらを採るか」への回答: 差が無い。}\ }$$

**monodromy 三つ組の定義**(BFC の $\lambda$-被覆): $\hat F_2=\langle x,y\rangle=\pi_1(\mathbf P^1\smallsetminus\{0,1,\infty\})$、$z=(xy)^{-1}$、その像
$$\boxed{\ g_0:=X,\qquad g_1:=Y,\qquad g_\infty:=Z=(XY)^{-1},\qquad g_0g_1g_\infty=1\ }$$
が $\Lambda=P/H$ 上の置換三つ組。被覆次数 $=\lvert\Lambda\rvert$。($A_5$ 窓での同じ規約が `week4-A5算術飽和_v4.md` 補題 FC-4(a)。)

### 1.2 窓 A(`W-E-A10-9t1`)の被覆データ【機械確認済】

`search/certs/a13_ladder_W_E_A10_9t1_20260730.json` / `sdc_twist_W_E_A10_9t1_20260730.json` の $a_1,b_1$ をそのまま入力:

$$a_1=(1,2)(3,5)(4,10)(6,9),\qquad b_1=(2,9,5)(3,4,10)(6,8,7).$$

| 量 | 値(GAP・`u_meas_probe1.g`) |
|---|---|
| $a_1^2=b_1^3=1$ | ✓ |
| $\mathrm{sgn}(a_1)=\mathrm{sgn}(b_1)=+1$ | ✓ ⟹ $\langle a_1,b_1\rangle=A_{10}$($\varepsilon=0$・case A)、`= AlternatingGroup(10)` **true** |
| $w=b_1^{-1}a_1$ | $(1,2,3,4,5,6,7,8,9)$、$\mathrm{ord}=9$、型 $(9,1)$ |
| $v=a_1b_1^{-1}$ | $(1,5,10,3,9,7,8,6,2)$、$\mathrm{ord}=9$、型 $(9,1)$ |
| $g_0=X=w^2$ | $(1,3,5,7,9,2,4,6,8)$、$\mathrm{ord}=9$ |
| $g_1=Y=v^2$ | $(1,10,9,8,2,5,3,7,6)$、$\mathrm{ord}=9$ |
| $g_\infty=Z=(XY)^{-1}$ | $(1,4,2,6,5,9,10,8,7)$、$\mathrm{ord}=9$ |
| $g_0g_1g_\infty=1$ | ✓ |
| $Y=b_1Xb_1^{-1}$、$Z=b_1Yb_1^{-1}$ | ✓ ✓(**定理 M1 の $\tau=\mathrm{Ad}(t)$ を機械確認**) |
| $Y=a_1Xa_1$ | ✓(RED の $\bar y=\bar x^{a_1}$ と整合) |
| $X,Y,Z$ は $A_{10}$-共役 | ✓ ✓ |
| $\Lambda=P/H$、$H=A_9$ | $\lvert H\rvert=181440$、指数 **10**、$N_{A_{10}}(H)=H$ ✓(**(W3) 成立**) |
| 被覆次数 | **10** |
| monodromy 群 | $\langle X,Y\rangle=A_{10}$、10 点上推移、`TransitiveIdentification = 44` ⟹ **10T44** |

**(W4) が空であることの 1 行証明(命題 TAIL-OBS の再確認)**: $A_{10}$ の指数 $m\le9$ の真部分群があれば剰余類作用で $A_{10}\hookrightarrow S_m$($A_{10}$ 単純ゆえ核は 1)、しかし $\lvert A_{10}\rvert=1{,}814{,}400>362{,}880=\lvert S_9\rvert$(機械確認 A.4)。∎ ⟹ **$[P:H]=M=9$ は不可能。$\Lambda$ の最小は 10。**

### 1.3 窓 B(段 S4 = $\mathrm{PSL}(2,8)$・$k=9$)の被覆データ【機械確認済】

封印 JSON(`week3-PSL封印計算_opus_v1.md` §5.4)の marking を $\mathbf F_8=\mathbf F_2[x]/(x^3+x+1)$(整数符号 $x=2,\ x{+}1=3,\ x^2=4,\ x^2{+}1=5$)で復元:

$$S=\begin{pmatrix}1&0\\1&1\end{pmatrix},\qquad T=\begin{pmatrix}x^2&x+1\\1&x^2+1\end{pmatrix},\qquad \det S=\det T=1 .$$

| 量 | 値(GAP) |
|---|---|
| $\det S=\det T=1$、$\mathrm{tr}(S)=0$、$\mathrm{tr}(T)=1$ | ✓(封印 JSON の `trace_triple:[0,1,2]` の第 1・2 成分と一致) |
| $\mathrm{ord}(s)=2$、$\mathrm{ord}(t)=3$、$\langle s,t\rangle$ | 位数 **504**・単純 ✓ |
| $w=T^{-1}S$ | $\mathrm{ord}=9$(封印 JSON `ord_w:9` と一致)、$\mathbf P^1(\mathbf F_8)$ 上の型 **$(9)$** |
| $g_0=X=w^2$、$g_1=Y=v^2$($v=ST^{-1}$)、$g_\infty=Z$ | いずれも $\mathrm{ord}=9$、$g_0g_1g_\infty=1$ ✓ |
| $Y=tXt^{-1}$、$Z=tYt^{-1}$ | ✓ ✓ |
| $X,Y,Z$ は $P$-共役 | ✓ ✓ |
| $\Lambda=P/H$、$H=$ 点安定化群 | $\lvert H\rvert=56$、`IdGroup [56,11]`、指数 **9**、$N_P(H)=H$ ✓ |
| $\langle X\rangle$ が $\Lambda$ 上 regular | ✓ ⟹ **(W4) 成立** |
| 被覆次数 | **9** |
| monodromy 群 | $\mathrm{PSL}(2,8)$、`TransitiveIdentification = 27` ⟹ **9T27** |
| $C_{S_9}(X)=9$、$N_{S_9}(\langle X\rangle)=54$ | ✓(= §0.1 で述べた「値の一致」の実体) |
| $t$ は $\Lambda$ 上固定点なし | ✓(`surj_s4_v2` §3.2 の「位数 3 の元も固定点自由」を機械確認) |

---

## 2. M1 — **順序 passport**(凍結対象)

### 2.1 ★ 補題 PASS — passport は**先験的に決まる**【proof(2 行)+ 機械確認】

> ### 補題 PASS(case A / c∈N 窓の順序 passport)
> $c\in N$ の許容対象で、$\tau=\mathrm{Ad}(\bar\delta)\vert_P\in\mathrm{Aut}(P)$ が $P$-集合 $\Lambda$ の置換として実現される(すなわち $\Lambda$ が $\mathrm{Aut}(P)$-安定な $P$-集合)とする。このとき
> $$\boxed{\ \text{順序 passport}\ =\ (\lambda,\lambda,\lambda),\qquad \lambda:=(\Lambda\ \text{上の}\ X\ \text{の巡回型}).\ }$$
> **証明.** 定理 M1(`week3-PSL封印計算` §1)より $Y=\tau(X)$、$Z=\tau(Y)$、かつ $X,Y,Z$ は $P$ 内で共役(case A では $\tau$ が内部)。共役な置換は同じ巡回型をもつ。case B でも $\tau$ は $\mathrm{Aut}(P)$ の元で、$\Lambda$ 上の置換として実現されれば同じ結論。∎

> **⚠ 正本の更新**: `surj_s4_v1.md` §5 の M1 欄は「$0$ 上は $(9)$ が先験的に確定・$1,\infty$ 上は**要計算**」と書いていた。**補題 PASS により $1,\infty$ 上も先験的に確定する** — 計算は不要である。委嘱の「(9) が先験確定と正本にあるが再導出して確認」への回答: **再導出したところ、$0$ 上だけでなく 3 つの繊維すべてが先験確定であった。**(機械計算は独立確認として実行した。)

### 2.2 凍結する値

> ### 【凍結 M1-A】窓 A = `W-E-A10-9t1`(半局所枠 $\Lambda=A_{10}/A_9$)
> $$\boxed{\ \text{被覆次数}\ d=10,\qquad \text{順序 passport}\ \bigl((9,1),\ (9,1),\ (9,1)\bigr),\qquad \text{monodromy}=A_{10}=\mathbf{10T44}\ }$$
> **$0$ 上**: 2 点、分岐指数 $(9,1)$ — $\lambda^{-1}(0)=\{P_0,P_1\}$、$e_{P_0}=9$、$e_{P_1}=1$。
> **$1$ 上**: 2 点、分岐指数 $(9,1)$。 **$\infty$ 上**: 2 点、分岐指数 $(9,1)$。

> ### 【凍結 M1-B】窓 B = 段 S4($\mathrm{PSL}(2,8)$・$k=9$・$\Lambda=P/\text{Borel}$)
> $$\boxed{\ \text{被覆次数}\ d=9,\qquad \text{順序 passport}\ \bigl((9),\ (9),\ (9)\bigr),\qquad \text{monodromy}=\mathrm{PSL}(2,8)=\mathbf{9T27}\ }$$
> **$0,1,\infty$ 上とも 1 点・全分岐(指数 9)。**

**$A_5$ 先例との比較**(`week4-A5算術飽和_v4.md` 補題 FC-4(a) の逐語「$X,Y,Z$ は位数 5 = 5-サイクル。RH で $g=2$」・LMFDB `5T4-5_5_5-a`): $d=5$、passport $((5),(5),(5))$、$g=2$。**窓 B は $A_5$ 窓の $\ell:5\to9$ 一般化そのものである。**

### 2.3 ★ passport は dessin を決めない — Nielsen 類の個数【機械測定】

$A_5$ 窓では「この型の dessin は同型を除きただ一つ」(補題 FC-4(b))であり、そこから $\mathbf Q$-モデルの一意性が出ていた。**同じことが起きるかを測った**(`u_meas_probe2.g`: 第 3 成分 $Z^{-1}=XY=c$ を固定し、全解を $C_{S_d}(c)$-軌道に分ける。全解の枚挙は悉皆)。

| 窓 | 全解 $(X,Y)$ | monodromy 別内訳 | **目的の monodromy をもつ dessin の個数($S_d$-類)** |
|---|---|---|---|
| **A**($d=10$) | 87,444 | $\lvert\langle X,Y\rangle\rvert=9{:}3,\ 27{:}6,\ 324{:}36,\ 504{:}54,\ 1512{:}432,\ 181440{:}7533,\ \mathbf{1814400{:}79380}$ | $79380/9=\mathbf{8{,}820}$ |
| **B**($d=9$) | 8,064 | $9{:}3,\ 27{:}6,\ 324{:}36,\ \mathbf{504{:}54},\ 1512{:}432,\ 181440{:}7533$ | $54/9=\mathbf{6}$ |

($C_{S_d}(c)=\langle c\rangle$ は位数 9 で、**全軌道の大きさが 9**(自由作用)であることも出力に含まれる。窓 A の値 87,444 のうち $S_9$ に落ちる部分が窓 B の 8,064 と一致するのは、窓 B の $\Lambda$ が窓 A の $\Lambda$ の 1 点を固定する部分集合だからで、機械の内的整合の確認になる。)

> ### 【FINDING U-1】**順序 passport は dessin を決めない。**
> $$\boxed{\ \textbf{窓 B: passport }((9),(9),(9))\textbf{・monodromy }\mathrm{PSL}(2,8)\textbf{ をもつ dessin は }\mathbf{6}\textbf{ 個。窓 A: }\mathbf{8820}\textbf{ 個。}\ }$$
> $A_5$ 窓(1 個)からの**質的な変化**である。補題 FC-4(b)(passport 一意 ⟹ 定義体 $\mathbf Q$)の論法は**そのままでは移植できない**。これは C1′(測定窓の同定)が $q=7$ 族だけの問題ではなく、**本キャンペーンの窓でも生きている**ことを意味する。

### 2.4 窓 B の 6 個を分ける不変量【機械測定・C1′ の材料】

$\mathrm{PSL}(2,8)$ の位数 9 の元は **3 つの共役類**(いずれも大きさ 56。以下 `9A=cl4`, `9B=cl5`, `9C=cl6` と番号は GAP の `ConjugacyClasses` 順)。冪写像 $g\mapsto g^u$ は $u\in(\mathbf Z/9)^\times$ に対しこの 3 類を巡回的に置換し、**$u=\pm1$ で自明**(⟹ 作用は $(\mathbf Z/9)^\times/\{\pm1\}\cong C_3$ を経由)。$\iota(9\mathrm{B})=0,\ \iota(9\mathrm{C})=1,\ \iota(9\mathrm{A})=2$($g\mapsto g^2$ が $\iota\mapsto\iota+1$)と番号づけると:

| dessin | 類ベクトル $(\iota(X),\iota(Y),\iota(Z))$ | 語 fingerprint $\bigl[XY,\ XY^{-1},\ X^2Y,\ XY^2,\ X^2Y^2,\ X^{-1}Y,\ X^3Y\bigr]$ の巡回型 |
|---|---|---|
| **#1 = 窓 B の dessin** | **$(0,0,0)$(対角)** | $(9),(9),(9),(9),(7,1,1),(9),(7,1,1)$ |
| #2 | $(1,1,0)$ | $(9),(9),(7,1^2),(7,1^2),(7,1^2),(9),(7,1^2)$ |
| #3 | $(2,0,0)$ | $(9),(7,1^2),(7,1^2),(9),(7,1^2),(7,1^2),(3,3,3)$ |
| #4 | $(0,2,0)$ | $(9),(7,1^2),(9),(7,1^2),(7,1^2),(7,1^2),(9)$ |
| #5 | $(1,2,0)$ | $(9),(7,1^2),(7,1^2),(7,1^2),(7,1^2),(7,1^2),(2^4,1)$ |
| #6 | $(2,1,0)$ | $(9),(7,1^2),(7,1^2),(7,1^2),(7,1^2),(7,1^2),(7,1^2)$ |

> ### 【FINDING U-2】**類ベクトルが 6 個を完全に分離する。**
> $$\boxed{\ \textbf{窓 B の dessin は「}X,Y,Z\textbf{ が同一の }P\textbf{-共役類に入る唯一の対角 dessin」である。}\ }$$
> * 6 個の類ベクトルは相異なり、語 fingerprint も相異なる(上表)。**⟹ passport を「順序 passport + 類ベクトル」に精密化すれば、窓 B の dessin は一意に指定できる。**
> * 対角性 $\iota(X)=\iota(Y)=\iota(Z)$ は $\mathrm{Out}(P)=C_3$(Frobenius = 3 類の巡回置換)の作用で不変なので、**$\mathrm{Aut}(P)$-不変なラベル**である。$\iota$ の原点の取り方(どれを $9\mathrm B$ と呼ぶか)に依存しない。
> * 表の第 3 成分がすべて $0$ なのは枚挙で $Z^{-1}=c$ を固定したためで、情報を持つのは $(\iota(X)-\iota(Z),\ \iota(Y)-\iota(Z))$ の対である。窓 B は $(0,0)$。
> * **窓 A では使えない**: $A_{10}$ の 9-巡回は 2 類にしか割れないので、類ベクトルは高々 8 通り。8820 個を分けられない。

**⚠ 訂正の申告**: `u_meas_probe3.g` の末尾ブロック(`N_{S9}(P)`-軌道の計算)には**バグがある**(`RepresentativeAction` の呼び出しが走査変数 $g$ を使っていないため、各類が自分自身に写るだけの自明な出力になる)。その出力(「6 個はすべて $N_{S_9}(P)$ の固定点」)は**根拠として採用しない**。上の $\mathrm{Out}$-不変性は §2.4 の紙上の議論(Frobenius が 3 類を巡回置換し、$Z$ を $c$ に戻す再共役が同じ巡回置換の逆を与える)による。**probe3 の同ブロックは使用禁止として記録する。**

---

## 3. M2 — 種数(Riemann–Hurwitz)

### 3.1 系 GENUS(case A の閉じた種数公式)【proof】

補題 PASS より 3 繊維の巡回型が共通なので、$d=\lvert\Lambda\rvert$、$c:=$($\Lambda$ 上の $\langle X\rangle$-軌道の個数 $=$ $\lambda$ の成分数)として
$$2g-2=-2d+3\,(d-c)=d-3c\qquad\Longrightarrow\qquad \boxed{\ g=1+\frac{d-3c}{2}\ }$$

**検算**: $A_5$ 窓 $d=5,c=1\Rightarrow g=2$ ✓(補題 FC-4(a) と一致)。窓 B $d=9,c=1\Rightarrow g=4$。窓 A $d=10,c=2\Rightarrow g=3$。**いずれも GAP の RH 実装(`u_meas_probe1.g` の `GenusRH`)と一致。**

### 3.2 凍結する値

> ### 【凍結 M2】
> $$\boxed{\ \textbf{窓 A}=\texttt{W-E-A10-9t1}:\ \ g=\mathbf3\qquad\qquad \textbf{窓 B}=\text{段 S4}:\ \ g=\mathbf4\ }$$
> **どちらも $g=0$ ではない。** `surj_s4_v2.md` §5 の「$g=0$ なら 1 変数有理関数の係数連立」という楽観枝は**発火しない**。

### 3.3 ★【FINDING U-3】9-梯子は $t\le4$ で**打ち止め**(Riemann 存在定理)

$P=A_n$、$\bar x$ の型 $(\ell,1^t)$($n=\ell+t$、$\ell$ 奇)、$\Lambda=P/A_{n-1}$(自然 $n$ 点作用)とすると $d=n=\ell+t$、$c=1+t$。系 GENUS より
$$g=1+\frac{(\ell+t)-3(1+t)}{2}=1+\frac{\ell-2t-3}{2}.$$
$g\ge0$ は Riemann 存在定理の必要条件(推移的三つ組は連結被覆を与え、その種数は非負)なので

> ### 定理 LAD(梯子の上限)【proof・初等】
> $$\boxed{\ t\ \le\ \frac{\ell-1}{2}\ }\qquad\text{特に }\ell=9\ \Rightarrow\ \boxed{\ t\le4\ }$$
> **証明.** $X,Y,Z$ は $\mathrm{Aut}(A_n)=S_n$($n\ne6$)の元による共役で移り合う(定理 M1)から自然 $n$ 点集合上で同じ巡回型 $(\ell,1^t)$ をもつ(補題 PASS)。$\langle X,Y\rangle=P=A_n$ は推移的。よって $(X,Y,Z)$ は次数 $n$ の連結被覆を定め、$2g-2=n-3(1+t)\ge-2$、すなわち $\ell+t\ge3t+1$。∎

**梯子の実データとの突合**(`sat_l1_v1.md` §6.1 の 4 窓):

| 窓 | $n$ | $t$ | $c=1+t$ | **$g$(本書)** | 存在 |
|---|---|---|---|---|---|
| W-E-A10-9t1 | 10 | 1 | 2 | **3** | ✓ |
| W-E-A11-9t2 | 11 | 2 | 3 | **2** | ✓ |
| W-E-A12-9t3 | 12 | 3 | 4 | **1** | ✓ |
| W-E-A13-9t4 | 13 | 4 | 5 | **0** | ✓ |
| (W-?-A14-9t5) | 14 | 5 | 6 | $-1$ | **✗ 存在しない** |

$$\boxed{\ \textbf{梯子が }t{=}4\textbf{ で止まっているのは探索予算の都合ではなく、定理である。}\ }$$

**独立の裏取り**: 工房の Ree 条件(`sat_l1_v1.md` §10.5.3 設計則 3: $k+2j\ge n+r+t-p-s-2$)でも $\ell=9,t=5$($n=14$、$w=(9,2,2,1)$、$p=0,s=2$)は要 $k+2j\ge16$ に対し $k\le7,j\le4$ で最大 15 ⟹ **不可**。**2 系統が一致**(ただし両者は別の被覆の種数条件なので、独立というより整合)。

> **⚠ 運用への即時の含意**: `ideas/ideas_013_solver_platform.md` に予定ジョブ `ladder-9t5-20260801` の記載がある。**この窓は存在しないので発車しても陰性しか出ない。** 速達で司令塔へ通知した(`ops/express/`)。

### 3.4 ★ 位数 3 の自己同型(M3 の梃子)【proof + 機械確認】

> ### 命題 PHI3
> $\mu(z):=1/(1-z)$($0\to1\to\infty\to0$ を巡回する $\mathbf Q$-有理 Möbius 変換)とする。case A の窓の $\lambda$-被覆 $W\to\mathbf P^1$ に対し、**位数 3 の自己同型 $\varphi\in\mathrm{Aut}(W)$ で $\lambda\circ\varphi=\mu\circ\lambda$ を満たすものが一意に存在する。**
> さらに $\varphi$ の固定点の個数は
> $$f=\#\mathrm{Fix}_\Lambda(\pi^{-1})+\#\mathrm{Fix}_\Lambda(X\pi^{-1}),\qquad \pi:=\text{(}\pi^{-1}X\pi=Y,\ \pi^{-1}Y\pi=Z\text{ なる一意の元)}=t^{-1},$$
> であり、$W/\langle\varphi\rangle$ の種数 $g'$ は $2g-2=3(2g'-2)+2f$ で決まる。

**証明.** $\omega\in\mathrm{Aut}(\hat F_2)$、$\omega:x\mapsto y\mapsto z\mapsto x$ は $\omega^3=\mathrm{id}$($\omega(z)=(yz)^{-1}=x$)。$\pi:=t^{-1}$ は定理 M1 の $\tau$ の逆で、$\theta\circ\omega=\mathrm{Ad}(\pi)^{-1}\circ\theta$、すなわち $\pi^{-1}X\pi=Y$、$\pi^{-1}Y\pi=Z$。$C_{\mathrm{Sym}(\Lambda)}(\theta(\hat F_2))=C_{\mathrm{Sym}(\Lambda)}(P)=1$(機械確認: 窓 A・B とも 1)ゆえ $\pi$ は一意で $\pi^3=1$。$\mu$ を持ち上げた $\varphi$ は $\pi$ に対応し、$\mathrm{Aut}(W/\mathbf P^1)=N_P(H)/H=1$((W3))ゆえ一意・位数 3。
固定点は $\mu$ の 2 固定点($z^2-z+1=0$、$\{0,1,\infty\}$ に無い)の上にある。商軌道体 $\mathcal O:=U/\langle\mu\rangle$($U=\mathbf P^1\smallsetminus\{0,1,\infty\}$)は $\mathbf A^1_t$ に位数 3 の錐点 2 個で、$\pi_1^{\rm orb}(\mathcal O)=\hat F_2\rtimes_\omega C_3\cong C_3*C_3=\langle A,B\mid A^3,B^3\rangle$、穴のループは $C=(AB)^{-1}$。
**$U$ は端を 3 個、$\mathcal O$ は 1 個もち被覆次数 3 ゆえ各端は次数 1 で写る ⟹ $C\in\hat F_2$**、すなわち $A$ と $B$ は $C_3$ の**互いに逆の**生成元へ写る。したがって
$$A=(1,\omega),\qquad B=(x^{-1},\omega^2),\qquad AB=(y^{-1},1),\qquad C=(AB)^{-1}=y .$$
($B^3=1$ は $x^{-1}\omega^2(x^{-1})\omega(x^{-1})=(yzx)^{-1}=1$ による。$A,B$ が非共役なのはアーベル化で $1-\omega$ の余核が $\mathbf Z/3$、$x\notin\mathrm{im}(1-\omega)$ による。)
$\Theta((u,\omega^i)):=\theta(u)\pi^{-i}$ は準同型で $\Theta(A)=\pi^{-1}$、$\Theta(B)=X^{-1}\pi$、$\Theta(C)=Y$。固定点数はその $\Lambda$ 上の固定点数。∎

> **⚠ 自認(v1 起草中の誤りと是正)**: 最初 $B=(x,\omega)$ と取った($A$ と**同じ** $C_3$-生成元へ写る)。これは幾何的な標準生成系ではなく、`u_meas_probe5.g` v1 が $\Theta(C)$ を位数 7(窓 B)と出したことで露見した — $t$ が $\bar P$ で 9 位の極をもつ($\mathrm{ord}_{P_0}\lambda=9$、$t$ は $\lambda=0$ で単純極)という初等的事実と矛盾する。上の「端の数え上げ」が正しい導出である。**$f$(固定点数)は変わらない**: $X^{-1}\pi$ は $(X\pi^{-1})^{-1}$ と $\pi$-共役なので固定点数が等しい。probe5 は v2 で是正し再走した。

**測定値**(`u_meas_probe1.g`):

| 窓 | $\pi$ | $\#\mathrm{Fix}(\Theta(A))$ | $\#\mathrm{Fix}(\Theta(B))$ | $f$ | $g$ | **$g'=\mathrm{genus}(W/\varphi)$** |
|---|---|---|---|---|---|---|
| A | $b_1^{-1}$ | 1 | 1 | 2 | 3 | $4=6g'-6+4\Rightarrow$ **$g'=1$(楕円曲線)** |
| B | $t^{-1}$ | 0 | 0 | 0 | 4 | $6=6g'-6\Rightarrow$ **$g'=2$** |

(整合検査: $\Lambda$ の点数 $\bmod\,3$ から $f\equiv d\cdot 2\ (\mathrm{mod}\ 3)$ が要請され、A: $f\equiv2$ ✓、B: $f\equiv0$ ✓。)

**副産物(M3 で使う)**: $\mathbf P^1_\lambda\to\mathbf P^1_\lambda/\langle\mu\rangle$ の商座標を $t:=\lambda+\frac{1}{1-\lambda}+\frac{\lambda-1}{\lambda}$ と取ると、$\lambda$ は $\mathbf Q(t)$ 上
$$\boxed{\ \lambda^3-t\lambda^2+(t-3)\lambda+1=0\ }$$
を満たす(3 根が $\lambda,\mu(\lambda),\mu^2(\lambda)$。$e_3=-1$、$e_1-e_2=3$ を直接計算)。これは **Shanks の "simplest cubic"**($x^3-Tx^2-(T+3)x-1$、$T=-t$、$x=-\lambda$)であり、判別式 $(t^2-3t+9)^2$ は平方、分岐は $t^2-3t+9=0$ の 2 点 $t=3\zeta_6^{\pm1}$(= $\mu$ の 2 固定点、$\mathbf Q(\sqrt{-3})=\mathbf Q(\zeta_3)$ 上共役)。**この $\mathbf Q$-有理な巡回三次構造が M3 の作業座標になる。**

### 3.5 ★★ 商被覆 $C:=W/\langle\varphi\rangle\to\mathbf P^1_t$ — **M3 の実作業対象**【機械測定】

命題 PHI3 の $\Theta$ は、次数 $\lvert\Lambda\rvert$ の**商 dessin** を与える(基底は $\mathbf P^1_t$、分岐 3 点 $=\{3\zeta_6,3\zeta_6^{-1},\infty\}$、順序三つ組 $(\Theta(A),\Theta(B),\Theta(C))=(\pi^{-1},\,X^{-1}\pi,\,Y)$)。$W=C\times_{\mathbf P^1_t}\mathbf P^1_\lambda$(Shanks 三次による底変換)で $W$ が復元されるので、**$C$ を決めれば $W$ と $\lambda$ が決まる。**

| | 窓 A(`W-E-A10-9t1`) | 窓 B(段 S4) |
|---|---|---|
| 次数 | 10 | 9 |
| 順序 passport $(\Theta(A),\Theta(B),\Theta(C))$ | $\bigl((3,3,3,1),\ (3,3,3,1),\ (9,1)\bigr)$ | $\bigl((3,3,3),\ (3,3,3),\ (9)\bigr)$ |
| $\Theta(C)=Y$ | ✓(機械) | ✓(機械) |
| monodromy | $A_{10}$ | $\mathrm{PSL}(2,8)$ |
| **種数 $g_C$**(RH) | **1(楕円曲線)** | **2** |
| $W\to C$ | 分岐 2 点(指数 3) | **不分岐(étale)** |
| $g_W$ との整合 | $2\cdot3-2=3(2\cdot1-2)+2\cdot2$ ✓ | $2\cdot4-2=3(2\cdot2-2)$ ✓ |
| この passport の dessin 数($S_d$-類・悉皆) | **28**(ours = #21) | **1(剛)** |

> ### 【FINDING U-8】**商 dessin は $W$ の dessin より桁違いに剛い。**
> $$\boxed{\ \textbf{窓 B の商 dessin }C\to\mathbf P^1_t\textbf{ は passport }\bigl(3^3,3^3,(9)\bigr)\textbf{ の中で\textbf{ただ一つ}(剛性)。}\ }$$
> $W$ 水準の 6 個 → 商水準の 1 個。**$A_5$ 窓の補題 FC-4(b)(passport 一意 ⟹ 定義体が決まる)の論法が、$W$ ではなく $C$ の水準で復活する。**
> 窓 A も $W$ 水準 8820 → 商水準 **28** に落ちる(ただし 1 ではない)。
> **枚挙の内訳**(窓 B): 型 $3^3$ の元 $\times$ 型 $3^3$ の元で積 $=c_q$(9-巡回)となる対は 24 個、monodromy 別に $81{:}6,\ 324{:}9,\ 504{:}9$。$504$ の 9 個が $\langle c_q\rangle$ の 1 軌道。
> **枚挙の内訳**(窓 A): 対は 276 個、$81{:}6,\ 324{:}9,\ 504{:}9,\ 1814400{:}252$。$A_{10}$ の 252 個が 28 軌道。

---

## 4. 凍結宣言と非凍結事項

> ### 凍結する(M3 以降で変更禁止)
> | # | 内容 |
> |---|---|
> | **F-1** | 窓 A の $\Lambda$ の同定: $H=A_9$、$\lvert\Lambda\rvert=10$、(W3) ✓・(W4) ✗ |
> | **F-2** | 窓 B の $\Lambda$ の同定: $H=$ Borel、$\lvert\Lambda\rvert=9$、(W3)(W4) ✓ |
> | **F-3** | 三つ組の規約 $(g_0,g_1,g_\infty)=(X,Y,(XY)^{-1})$、$X=w^2$、$w=b_1^{-1}a_1=t^{-1}s$(RED と週3-PSL の辞書は恒等) |
> | **F-4** | **順序 passport**: 窓 A $=((9,1),(9,1),(9,1))$ / 窓 B $=((9),(9),(9))$ |
> | **F-5** | **monodromy**: 窓 A $=$ 10T44 $=A_{10}$ / 窓 B $=$ 9T27 $=\mathrm{PSL}(2,8)$ |
> | **F-6** | **種数**: 窓 A $g=3$ / 窓 B $g=4$ |
> | **F-7** | **Nielsen 類数**: 窓 A **8820** / 窓 B **6**。窓 B の 6 個の類ベクトル表(§2.4)と、窓 B の dessin $=$ **対角** $(\iota(X),\iota(Y),\iota(Z))$ が等しいもの |
> | **F-8** | $\varphi$(位数 3)の存在と $g_C$: 窓 A $g_C=1$(楕円)/ 窓 B $g_C=2$。$W\to C$ は窓 A で 2 点分岐・窓 B で étale |
> | **F-9** | **商 dessin** $C\to\mathbf P^1_t$ の順序 passport: 窓 A $=\bigl((3^3,1),(3^3,1),(9,1)\bigr)$ / 窓 B $=\bigl(3^3,3^3,(9)\bigr)$。$\Theta(C)=Y$。分岐点は $\{3\zeta_6,3\zeta_6^{-1},\infty\}$、底変換は $\lambda^3-t\lambda^2+(t-3)\lambda+1=0$ |
> | **F-10** | **商 Nielsen 類数**: 窓 A **28**(ours $=$ #21)/ 窓 B **1(剛)** |

> ### 凍結しない(=まだ測っていない・本書の射程外)
> * $u_0$・$[u_0]_9$・$\mathrm{ord}([u_0^{-1}]_9)$ の**いかなる情報も本書には無い**。
> * $W_0$ の $K$-モデル・平面方程式・$\lambda$ の係数(M3)。
> * dessin の**定義体・モジュライ体**(窓 B の 6 個の $G_{\mathbf Q}$-軌道分解)。**UNKNOWN。**
> * (W1)【SD-a】。窓 A は **UNKNOWN**、窓 B は「機械測定 settled 54/54(定理ではない)」(`surj_s4_v2` §3.5)。
> * $B^{\rm sl}_{\rm FC}$ の段 II-b(`design NOTE`)。$(Z_{18}$-link$)$ の窓行(手続き)。

---

## 5. 出所(provenance)

| probe | SHA-256 | 内容 |
|---|---|---|
| `search/probe/wac_v1/u_meas_probe1.g` | `961e6582da645242245cf7cc7f296128752516a7c71007b5133a8affe5c3ba94` | M0/M1/M2 本体(両窓)・$\varphi$ の固定点 |
| `search/probe/wac_v1/u_meas_probe2.g` | `68a210085be569d2a7d8399623f59acc27fbb07a028411a617888f34a5489c02` | Nielsen 類の悉皆枚挙(窓 A 87,444 / 窓 B 8,064) |
| `search/probe/wac_v1/u_meas_probe3.g` | `1cdb3722f9a72121b2fe011e536101e6205a5f8986f516d3f6d541675b1e5beb` | 窓 B の 6 dessin の語 fingerprint(**末尾の $N_{S_9}(P)$-軌道ブロックはバグ・不採用**) |
| `search/probe/wac_v1/u_meas_probe4.g` | `d1baa2ab98fde93d67756ab1308b01b7cab661b1bf6b3359dec45f67f297f8d1` | 窓 B の 6 dessin の類ベクトル・冪写像の 3 類上の作用 |
| `search/probe/wac_v1/u_meas_probe5.g` **(v2)** | `a4aef28a56aea19a78ad095a16ebaeb9f5414a2141e0637910895189dc78069c` | 商被覆 $C\to\mathbf P^1_t$ の passport・種数・窓 B の商 Nielsen 類数(**v1 は $\Theta(B)$ を誤り。§3.4 の自認欄参照。v2 が正**) |
| `search/probe/wac_v1/u_meas_probe6.g` | `ab69dbbeb756445b14497f1efc205dfe7d381b887ce92465326aa47ce7dd4097` | 窓 A の商 Nielsen 類数(276 対の悉皆・28 類) |

**環境**: GAP 4.16.0(`gap.ps1`・`-o 2g`)。**単系統。cross-checked ではない。Lean verified ではない。** 入力証明書: `a13_ladder_W_E_A10_9t1_20260730.json`(canonical id `6092f5f0…3f4b`)・`sdc_twist_W_E_A10_9t1_20260730.json`・封印 JSON 段 S4(`week3-PSL封印計算_opus_v1.md` §5.4)。

**第二系統の未実施を明記**: 本書の値はすべて GAP 1 実装のみ。**passport・種数・Nielsen 類数の独立再計算(python/node)は未実施**であり、凍結は「この実装での値を以後変えない」という手続き的凍結であって cross-checked の格ではない。→ 設計書【M-b】。

---

## 6. FINDING 一覧(本書)

| # | 格 | 内容 |
|---|---|---|
| **U-0** | 是正要請 | `surj_s4_v2.md` §7.1 の SD-c 証明書は**窓 A の測定**で、定理 SURJ-S4 の窓 B のものではない。便 86 NOTE 3 は未解消。自認 |
| **U-1** | 測定 | **passport は dessin を決めない**。窓 B に 6 個、窓 A に 8820 個。$A_5$ 窓(1 個)からの質的変化 |
| **U-2** | 測定 + 紙 | 窓 B の 6 個は**類ベクトルで完全分離**。窓 B の dessin $=$ 唯一の**対角**類ベクトル。$\mathrm{Aut}(P)$-不変ラベル ⟹ **C1′ の必須欄になる** |
| **U-3** | **定理** | **定理 LAD**: $\ell$-梯子は $t\le(\ell-1)/2$。$\ell=9$ で $t\le4$ ⟹ **既知 4 窓で完結・$t=5$ 窓は存在しない**(予定ジョブ `ladder-9t5` は空撃ち) |
| **U-4** | **定理** | **補題 PASS**: case A/$c\in N$ 窓の順序 passport は $(\lambda,\lambda,\lambda)$ で先験確定。`surj_s4_v1` §5 の「$1,\infty$ 上は要計算」を不要化 |
| **U-5** | **定理** | **系 GENUS**: $g=1+(d-3c)/2$。$A_5$ 窓($g=2$)・窓 A($g=3$)・窓 B($g=4$)・梯子 $t=1..4$ で $g=3,2,1,0$ |
| **U-6** | **定理** + 機械 | **命題 PHI3**: 位数 3 の自己同型 $\varphi$($\lambda\circ\varphi=1/(1-\lambda)$)が一意存在。$W/\varphi$ は 窓 A で**楕円曲線**、窓 B で $g_C=2$。商座標は Shanks の simplest cubic |
| **U-7** | 自認 | `u_meas_probe3.g` 末尾ブロックにバグ(走査変数未使用)。当該出力は不採用。`u_meas_probe5.g` v1 は $\Theta(B)$ の同定を誤り(§3.4)。**v2 で是正・再走。固定点数 $f$ と F-8 は不変** |
| **U-8** | 測定 + 紙 | **商 dessin $C\to\mathbf P^1_t$ が M3 の実作業対象**。窓 B の商 dessin は passport $\bigl(3^3,3^3,(9)\bigr)$ の中で**唯一(剛)**、種数 2。窓 A は 28 個・種数 1。$W$ は Shanks 三次による底変換で復元される |
