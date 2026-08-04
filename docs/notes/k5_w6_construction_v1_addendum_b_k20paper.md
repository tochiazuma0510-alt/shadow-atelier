# 追補 B — $K^{(20)}$ の $\Gamma$-加群分解の**紙**裏取り(【K5-GAP-W3】)

**状態札: `candidate / 紙(本追補)+ GAP(cert)の二系統 = cross-checked 候補(CV-9 判読前)/ Lean 検証ではない / 検出力は無主張`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-04・**新設**
- 位置づけ: `docs/notes/k5_w6_construction_v1.md`(SHA-256 `a363b87f39026da63662f862344a33095431c13555619a921ae49f54e7dbe5d9`)への**追補**(**erratum 方式・本体は書き換えない**)。本体 §4.3 が新設した **【K5-GAP-W3】**(「$V=K^{(5)}/K^{(20)}$ の $\Gamma$-加群としての明示分解は当方未計算。**安い(紙 1 枚)と見積もる**」)への回答である。
- 委嘱: 司令塔(副題・軽・1 枚)「implementer の W6 束が GAP 直接構成で出した 3 点を**紙で**裏取りせよ」
- **裏取り対象の機械側正本**: cert `search/certs/w6_coker_tool_20260804.json`(SHA-256 `288d7120dfc139dc9dfb304471430cebd0790cf99388663811d7442e42ee7c88`)/ driver `search/probe/w6_coker_tool/w6_coker_tool_driver.g`(SHA-256 `34c15ac7b85140ae041943f2bd82b923148a3f3c090e290fec6772c151df986e`)
- **依拠**: 正典 arXiv 2405.11725 **(4.7)(4.8)**・**Prop 3.5**・Thm 4.4 / `docs/week1-定義ノート.md` §3(**$\psi_n$ の定義 (3.1)**・数値事実 $\lvert G_n\rvert$)/ 本体 §1.3 補題 GAMMA・§2.3 **定理 W6-OBS (A)(B)(C)**・§3.3 生存表・§4.3 DF-W6-2

> ## ★ 冒頭転記 — 停止規則 **S-W6-3**(本体 §5・逐語)
> > | **S-W6-3** ★ | $\operatorname{coker}\psi_V\ne0$ を確認しただけで「検出力ある窓を作った」と書こうとした | `OVERCLAIM / STOP` | ★ **群 $\ne$ 類**(§4.1)。**障害類の非零性まで到達していない限り candidate と書く** |
>
> **本追補が計算するのは障害群 $\operatorname{coker}\psi_V$ の次元だけである。**
> - **障害類は計算していない**($\widetilde f_0$ と拡大の具体形に依存し、紙では決まらない — 本体 §4.1)。
> - **$d_N$ について何も主張しない。** **窓の存在についても何も主張しない。**
> - **$\operatorname{coker}\ne0$ を「検出力あり」と読まないこと**(本体 §3.3 の表の注意・危険箇所 D-4)。

> ## 封印遵守
> **$K^{(5)}$ の実測に触れていない。** 使った $n=5$ の情報は $G_5$ の**構造**($\lvert G_5\rvert=500$)と reduction の存在だけである。shadow の値・証明書・$\operatorname{Im}R$・$u$ 値・$\hat c_\mu$ には一切触れていない(cert の `seal_declaration` の 5 項すべて `false` と整合)。

---

## 0. 判定(先に 4 行)

| # | 主張 | 紙の判定 |
|---|---|---|
| **①** | $V:=\ker(G_{20}\twoheadrightarrow G_5)$ は初等アーベル 2 群・$\dim_{\mathbf F_2}V=3$ | ★ **成立**(§2.2)。しかも $V=\langle r^{10}\rangle^3$ と**明示**に決まる |
| **②** | $\theta\vert_V,\tau\vert_V$(cert 記載)が (4.7)(4.8) パターンの $p=2$ 版と同型 | ★ **成立、しかも逐語一致**(§2.3)。基底 $(X^2,\,Y^2,\,(XY)^{-2})$ で (4.7)(4.8) が**そのまま**成り立ち、その $\bmod\,2$ 還元が cert の行列(**行ベクトル規約**)である |
| **③** | $\dim\operatorname{coker}\psi_V=1$ | ★ **成立**(§2.4)。**(A) 式のみで計算**。**(B) は $p=2$ で偽**(値 $0$ を返す)、**(C) は前件不成立**(数値が偶然一致するだけ) |
| **④** | 【K5-GAP-W3】は閉じたか | ★ **閉じた(紙・candidate)**。ただし **DF-W6-2 の残り 2 項(障害類 $=0$・$d=5$)は本追補の射程外**(§5) |

---

## 1. 設定(本体 §1 の記号を変えない)

$D_m=\langle r,s\mid r^m,\ s^2,\ srs^{-1}r\rangle$($位数 2m$)、正典 (3.1) の

$$\psi_m:PB_3\to D_m^3,\qquad x\mapsto(r,s,s),\quad y\mapsto(rs,r,rs),\quad c\mapsto(1,1,1),$$

$K^{(m)}=\ker\psi_m$、$G_m=PB_3/K^{(m)}\cong\operatorname{Im}\psi_m=\langle X,Y\rangle$、$X=(r,s,s)$、$Y=(rs,r,rs)$。

**$W\text{-}3=K^{(20)}=K^{(5)}\cap K^{(4)}$ の確認(1 行)**: $C_{20}\cong C_4\times C_5$ より $D_{20}\hookrightarrow D_4\times D_5$($r\mapsto(r\bmod4,\ r\bmod5)$、$s\mapsto(s,s)$;回転部は CRT で単射、反射は各成分で非自明)。$\psi_{20}$ はこの埋め込みを経由するので $K^{(20)}=K^{(4)}\cap K^{(5)}$。とくに $K^{(20)}\subset K^{(5)}$(正典 Prop 3.5: $5\mid\operatorname{lcm}(20,2)=20$)。$\Longrightarrow\ V=\ker(G_{20}\twoheadrightarrow G_5)=K^{(5)}/K^{(20)}$。

---

## 2. 紙の導出

### 2.1 回転部 $A_m:=G_m\cap C_m^3$ の決定($m$ 偶数)

**反射符号** $\pi:D_m\to\mathbf Z/2$($r\mapsto0$、$s\mapsto1$)を成分ごとに取ると
$$\pi^3(X)=(0,1,1),\qquad \pi^3(Y)=(1,0,1)$$
は独立ゆえ $\pi^3(G_m)\cong C_2^2$、したがって $A_m=\ker(\pi^3\vert_{G_m})$ は $G_m$ の**指数 4** の部分群である。

**生成元の平方**を計算する($rs$ は反射ゆえ $(rs)^2=1$、$sr=r^{-1}s$、$s\cdot rs=(sr)s=r^{-1}$):
$$X^2=(r^2,1,1),\qquad Y^2=(1,r^2,1),\qquad XY=(r^2s,\ r^{-1}s,\ r^{-1}),\qquad (XY)^2=(1,1,r^{-2}).$$
$$\Longrightarrow\qquad A_m\ \supseteq\ \langle r^2\rangle^3 .$$

**逆向き($m$ 偶数)**: $m$ が偶数のとき $\varepsilon:D_m\to\mathbf Z/2$、$r\mapsto1,\ s\mapsto0$ は**準同型**である(関係式の検査: $r^m\mapsto m\equiv0$($m$ 偶)、$s^2\mapsto0$、$srs^{-1}r\mapsto0+1+0+1=0$)。
$$\varepsilon^3(X)=(1,0,0),\qquad \varepsilon^3(Y)=(1,1,1).$$
$\phi:=(\pi^3,\varepsilon^3):G_m\to C_2^3\times C_2^3$ の像は 2 つの独立な対合 $\bigl((0,1,1),(1,0,0)\bigr)$、$\bigl((1,0,1),(1,1,1)\bigr)$ で生成され、位数は **4**。よって $\lvert\ker\phi\rvert=\lvert G_m\rvert/4=\lvert A_m\rvert$ であり、$\ker\phi\subseteq\ker\pi^3\vert_{G_m}=A_m$ と位数が一致するので $\ker\phi=A_m$、すなわち $A_m\subseteq\ker\varepsilon^3$。$C_m^3\cap\ker\varepsilon^3=\langle r^2\rangle^3$ だから

$$\boxed{\ A_m=\langle r^2\rangle^3\qquad(m\ \text{偶数}),\qquad \lvert G_m\rvert=4\Bigl(\tfrac m2\Bigr)^3 .\ }$$

> ★ **副産物**: これは定義ノート §3 の数値事実「$\lvert G_n\rvert=4(n/2)^3$($n$ 偶)」の**紙による再導出**である。$m=20$ で $\lvert G_{20}\rvert=4\cdot10^3=4000$、$m=5$(奇)では $\langle r^2\rangle=\langle r\rangle$ ゆえ $A_5=C_5^3$、$\lvert G_5\rvert=4\cdot5^3=500$。**cert の `g20_order`=4000 / `g5_order`=500 と一致**(§3)。

### 2.2 ★ $V$ の決定 — 主張 ①

$\rho:D_{20}\twoheadrightarrow D_5$($r\mapsto\bar r$($\bar r^5=1$)、$s\mapsto\bar s$)は $\rho^3\circ\psi_{20}=\psi_5$ を満たすので $G_{20}\twoheadrightarrow G_5$ を誘導する(cert `reduction_hom_well_defined_onto`=true と整合)。$\pi_{D_5}\circ\rho=\pi_{D_{20}}$ ゆえ $V\subseteq A_{20}$、したがって

$$V=\ker\bigl(A_{20}\to A_5\bigr)=\ker\bigl(\langle r^2\rangle^3\to\langle\bar r\rangle^3\bigr).$$

成分ごとに $\langle r^2\rangle=\{r^{2k}:k\in\mathbf Z/10\}\to C_5$、$r^{2k}\mapsto\bar r^{2k}$。核は $2k\equiv0\ (5)\iff k\equiv0\ (5)\iff k\in\{0,5\}$、すなわち $\{1,r^{10}\}=\langle r^{10}\rangle\cong C_2$。ゆえに

$$\boxed{\ V=\langle r^{10}\rangle^3\ \cong\ (\mathbf Z/2)^3,\qquad \lvert V\rvert=8,\qquad V\ \text{は初等アーベル 2 群},\qquad \dim_{\mathbf F_2}V=3 .\ }$$

(位数の突合: $\lvert G_{20}\rvert/\lvert G_5\rvert=4000/500=8$ ✓。)

### 2.3 ★ $\theta,\tau$ の作用 — 主張 ②(**(4.7)(4.8) の逐語一致**)

$K^{(m)}\in\mathrm{NFI}_{PB_3}(B_3)$(正典 Prop 3.1)ゆえ $B_3/PB_3\cong S_3$ が $G_m$ に作用し、cert が採る規約(`ScanRoofHexagon`: $x\leftrightarrow y$ ; $x\mapsto y,\ y\mapsto(xy)^{-1}$)で

$$\theta:\ X\mapsto Y,\ Y\mapsto X,\qquad\qquad \tau:\ X\mapsto Y,\ Y\mapsto(XY)^{-1}.$$

$A_{20}=\langle r^2\rangle^3$ の**基底**を $a_1:=X^2=(r^2,1,1)$、$a_2:=Y^2=(1,r^2,1)$、$a_3:=(XY)^{-2}=(1,1,r^2)$ と取る($\cong(\mathbf Z/10)^3$、座標 $n_i$)。

**$\theta$**: $a_1=X^2\mapsto Y^2=a_2$、$a_2\mapsto a_1$。第 3 座標は $YX=(rsr,\ rs,\ r)=(s,\ rs,\ r)$(∵ $rs\cdot r=r(sr)=r\cdot r^{-1}s=s$)より $(YX)^2=(1,1,r^2)$、ゆえに $a_3=(XY)^{-2}\mapsto(YX)^{-2}=(1,1,r^{-2})=a_3^{-1}$。したがって
$$\theta(n_1,n_2,n_3)=(n_2,\ n_1,\ -n_3)\tag{= (4.7)}$$

**$\tau$**: $a_1=X^2\mapsto Y^2=a_2$;$a_2=Y^2\mapsto\bigl((XY)^{-1}\bigr)^2=(XY)^{-2}=a_3$;$XY\mapsto Y\cdot(XY)^{-1}=Y\cdot Y^{-1}X^{-1}=X^{-1}$ ゆえ $a_3=(XY)^{-2}\mapsto(X^{-1})^{-2}=X^2=a_1$。したがって
$$\tau(n_1,n_2,n_3)=(n_3,\ n_1,\ n_2)\tag{= (4.8)}$$

> ★ **正典 (4.7)(4.8) が $m=20$ でも逐語で成り立つ**(基底 $(X^2,Y^2,(XY)^{-2})$ において)。本体 §1.3 は $A=[G_5,G_5]\cong C_5^3$ での形として (4.7)(4.8) を引いていたが、**同じ式が偶数 $m$ の $A_m=\langle r^2\rangle^3$ でも成り立つ**ことをここで確認した。

**$V$ への制限**: $V=\{n_i\in\{0,5\}\subset\mathbf Z/10\}$。$n_i=5b_i$($b_i\in\mathbf F_2$)と書くと $-5\equiv5\ (10)$ ゆえ $-n_3\equiv n_3$、したがって

$$\boxed{\ \theta\vert_V(b_1,b_2,b_3)=(b_2,b_1,b_3),\qquad \tau\vert_V(b_1,b_2,b_3)=(b_3,b_1,b_2).\ }$$

> ### ⚠ **$p=2$ では (4.7) の符号が消える**(★教材 — 危険箇所 D-1 の裏面)
> 本体 §1.3 の危険箇所 D-1 は「**$\theta$ は第 3 座標を反転する。この 1 個の符号が本稿の全結論を決める**」と警告した。**その符号は $p=2$ では不可視になる。** ゆえに $V$ は $\Gamma$ の像が $S_4$ ではなく **$S_3$**(3 座標の置換)で、加群としては **$\mathbf F_2$ 上の 3 点置換加群** である。⟹ 本体 §3.3 生存表の $p=2$ 行が「**A 型**」と「**$\mathrm{std}_3$**」を別行に並べて**どちらも $\dim\operatorname{coker}=1$** としているのは、$p=2$ で**両者が一致する**からである(整合)。

**cert 行列との突合(規約の明示 — CV-9 事項)**: cert は
`theta_matrix_gf2` $=\begin{psmallmatrix}0&1&0\\1&0&0\\0&0&1\end{psmallmatrix}$、`tau_matrix_gf2` $=\begin{psmallmatrix}0&1&0\\0&0&1\\1&0&0\end{psmallmatrix}$ を記載する。**行ベクトル規約($v\mapsto vM$、GAP の標準)**で読むと
$$vM_\theta=(v_2,v_1,v_3),\qquad vM_\tau=(v_3,v_1,v_2)$$
となり、上の $\theta\vert_V,\tau\vert_V$ と**逐語一致**する。
⚠ **列ベクトル規約で読むと $M_\tau$ は $\tau^{-1}$ を表す**が、$\langle\tau\rangle=\langle\tau^{-1}\rangle$ かつ $N_\tau=1+\tau+\tau^2$ は巡回群 $\langle\tau\rangle$ 上の和なので**両規約で同一の作用素**であり、$\operatorname{coker}\psi_V$ は規約に依存しない。**結論は規約選択に頑健である**(この一点は CV-9 判読の入力として §4 に置く)。

### 2.4 ★ $\dim\operatorname{coker}\psi_V=1$ — 主張 ③(**(A) 式のみ**)

$\psi_V=(N_\theta,N_\tau):V\to V^\theta\oplus V^\tau$、$N_\theta=1+\theta$、$N_\tau=1+\tau+\tau^2$($\mathbf F_2$ 係数)。

| 部分空間 | 記述 | 次元 |
|---|---|---|
| $V^\theta$ | $\{b_1=b_2\}$ | **2** |
| $V^\tau$ | $\{b_1=b_2=b_3\}$ | **1** |
| $\ker N_\theta$ | $N_\theta b=(b_1{+}b_2)(1,1,0)$ ⟹ $\{b_1=b_2\}=V^\theta$ | 2 |
| $\ker N_\tau$ | $N_\tau b=\sigma\cdot(1,1,1)$、$\sigma=b_1{+}b_2{+}b_3$ ⟹ $\{\sigma=0\}$ | 2 |
| $\ker N_\theta\cap\ker N_\tau$ | $\{b_1=b_2,\ b_3=0\}=\langle(1,1,0)\rangle$ | **1** |

**定理 W6-OBS (A)(master formula・常に成立)**:
$$\dim\operatorname{coker}\psi_V=\dim V^\theta+\dim V^\tau-\dim V+\dim(\ker N_\theta\cap\ker N_\tau)=2+1-3+1=\boxed{1}.$$

**独立な直接確認**: $\dim\operatorname{im}\psi_V=\dim V-\dim\ker\psi_V=3-1=2$、$\dim(V^\theta\oplus V^\tau)=3$、$\operatorname{coker}=3-2=1$ ✓。

> ### なぜ (B)(C) を使えないか(**1 行ずつ + 実害の明示**)
> - **(B)($p\ne2$)**: 証明は $N_\theta=2e_\theta$($e_\theta=(1+\theta)/2$)という**$2$ の可逆性**に依存する。$p=2$ では成り立たない。**しかも数値が違う** — (B) の右辺は $\dim V^\tau-\dim N_\tau(\ker N_\theta)=1-1=\mathbf 0$ を返す。⟹ **(B) は $p=2$ で「未証明」ではなく「偽」である**(本体 §2.3 の機械側注記「$p=2$ で (B) が破れること(6 件)」の実物)。
> - **(B′)($p\ne3$)**: $p=2\ne3$ ゆえ**適用可能**。$\dim V^\theta-\dim N_\theta(\ker N_\tau)=2-1=1$ ✓((A) と一致 — 独立な第 3 の確認になる;**機械確認 = §6 の B9b**)。
> - **(C)($p\nmid6$)**: $p=2\mid6$ ゆえ**前件不成立**。射影 $e_\theta,e_\tau=(1+\tau+\tau^2)/3$ が存在しない。⚠ **数値は偶然一致する**($\dim(V^\ast)^\Gamma=\dim V^\Gamma=1$;置換加群は自己双対で不変部分が 1 次元)。**この一致を「(C) が $p=2$ でも使える」証拠と読んではならない。**

---

## 3. cert との突合(**値は機械生成・パス併記・手写しなし**)

正本: `search/certs/w6_coker_tool_20260804.json` の `part3_k20_module`(および `part2_fixtures.DF_W6_2`)。

| 項目 | cert の欄 | cert の値 | 紙(本追補) | 一致 |
|---|---|---|---|---|
| $\lvert G_{20}\rvert$ | `g20_order` | 4000 | §2.1 $4(20/2)^3$ | ✓ |
| $\lvert G_5\rvert$ | `g5_order` | 500 | §2.1 $4\cdot5^3$ | ✓ |
| reduction | `reduction_hom_well_defined_onto` | true | §2.2($\rho^3\circ\psi_{20}=\psi_5$) | ✓ |
| $\lvert V\rvert$ | `v_order` | 8 | §2.2 $\lvert\langle r^{10}\rangle^3\rvert$ | ✓ |
| $V$ の型 | `v_abelian` / `v_elementary_abelian_2group` | true / true | §2.2 $(\mathbf Z/2)^3$ | ✓ |
| $\dim V$ | `module_data.dim` | 3 | §2.2 | ✓ |
| $\theta$ 行列 | `module_data.theta_matrix_gf2` | $[[0,1,0],[1,0,0],[0,0,1]]$ | §2.3(行ベクトル規約) | ✓ |
| $\tau$ 行列 | `module_data.tau_matrix_gf2` | $[[0,1,0],[0,0,1],[1,0,0]]$ | §2.3(行ベクトル規約) | ✓ |
| 位数 | `theta_sq_eq_id` / `tau_cube_eq_id`(および `theta_order_on_g20`=2 / `tau_order_on_g20`=3) | true / true | §2.3(置換 $(12)$ と 3-巡回) | ✓ |
| **$\dim\operatorname{coker}\psi_V$** | `module_data.coker_dim` | **1** | §2.4 式 (A) | ✓ |
| 式の一致 | `module_data.formulas_agree` | true | (A)=(B′)=直接計算 $=1$、**(B) は不適用**(§2.4) | ✓(**ただし下の注意**) |

> ### ⚠ `formulas_agree` の読み方(**紙側からの注意**)
> 本追補の計算では **(B) は $p=2$ で値 $0$ を返す**(= (A) と一致しない)。cert の `formulas_agree`=true が **(A)(B)(B′) の 3 式すべての一致**を意味するなら、それは $p=2$ では成り立たない。cert の当該フラグが **(A) と (B′) と直接計算の一致**を指しているのであれば整合する。
> ⟹ **これは実装の欠陥の指摘ではなく、フラグの意味論の確認要請である**(§4 の CV-9 判読へ回す)。本体 §2.3 が「**$p=2$ で (B) が破れること(6 件)も、前件を明示した上で機械が捕まえた**」と書いていることから、実装は $p=2$ で (B) を適用対象から外している可能性が高い。

---

## 4. 格の行(**二系統になる旨の明示**)

| 層 | 内容 | 格 |
|---|---|---|
| **紙(本追補)** | §2 の導出。$V=\langle r^{10}\rangle^3$・(4.7)(4.8) の逐語成立・(A) 式による $\dim\operatorname{coker}=1$ | **paper-proof candidate**(単系統・Sol 未監査) |
| **機械(cert)** | GAP 直接構成(`Pcgs` 同型で $\mathrm{GF}(2)^3$ へ落とす)。**cert 自身が `scope.cross_checked_status` で「part 3 は GAP 単系統」と申告している** | **GAP 単系統** |
| **両者の関係** | ★ **本追補が第 2 の系統(紙)を供給する。** ⟹ **cross-checked 候補** | ★ **`cross-checked` は名乗らない — CV-9 判読(falsifier・非当事者)を経る前だから** |

**CV-9 判読への入力(何が同一だと主張しているかの明示)**

1. **対象の同一性**: cert の $V$(`Ker(G20->G5)` を GAP で構成)と紙の $V=\langle r^{10}\rangle^3$ が**同じ部分群**であること。紙側は $V$ を**明示的に**決めているので、判読は「GAP の `Ker` が同じ群を返すか」に帰着する。
2. **座標の同一性**: cert は `Pcgs` 由来の基底を使い、紙は $(X^2,Y^2,(XY)^{-2})$ の $\bmod\,5$ 還元を使う。**基底が違えば行列は共役でしか一致しない** — にもかかわらず**逐語一致した**のは偶然かもしれない。⟹ 判読すべきは「行列そのものの一致」ではなく「**加群としての同型**」であり、$\dim\operatorname{coker}$ はどちらでも不変である。
3. **規約の同一性**: 行ベクトル規約($v\mapsto vM$)を採ると逐語一致する(§2.3)。**列規約でも結論は不変**($N_\tau$ が同一作用素)。⟹ **この項目は「判定不能」ではなく「どちらでも同一結論」**と申告する。
4. **`formulas_agree` の意味論**(§3 の注意)。

---

## 5. 【K5-GAP-W3】の判定と、**閉じていないもの**

$$\boxed{\ \textbf{【K5-GAP-W3】(}V=K^{(5)}/K^{(20)}\textbf{ の }\Gamma\textbf{-加群としての明示分解)は閉じた(紙・candidate)。}\ }$$

明示分解: $V\cong\mathbf F_2^3$、$\Gamma$ の像は 3 座標を置換する $S_3$(**符号は $p=2$ で消える**)、すなわち **$\mathbf F_2[S_3/S_2]$(3 点置換加群)**。$\dim\operatorname{coker}\psi_V=1$。

**閉じていないもの(DF-W6-2 を fixture として使うために残る 2 項)**

| # | 残項 | 状態 | 誰の仕事か |
|---|---|---|---|
| **(i)** | **障害類 $=0$** | ★ **本追補の射程外**(**S-W6-3**: 群 $\ne$ 類)。本体 §4.3 は「$d=5$ が既知であることから類 $=0$ を **retrodiction** として得る」としており、**独立に計算されたものではない** | 実装(有限計算)/ 数学者(retrodiction の論理の明示) |
| **(ii)** | **$d_{K^{(20)}}=5$** | 正典 **Thm 4.4**($4\mid q$ 分岐)の証明掲載分岐で既知、と本体 §4.3 が引く。**本追補は正典の当該分岐を再検分していない** | reader(正典の該当頁の画像照合) |

⚠ したがって **予言 P-W6-5**(「$K^{(20)}$: $\operatorname{coker}\ne0$ かつ障害類 $=0$ かつ $d=5$」)のうち、**本追補が紙で裏取りしたのは第 1 項のみ**である。

---

## 6. 検算(本追補で走らせたもの)

- **script**: `scratchpad/s3fam_check.py`(SHA-256 `99d8824dd2e7ec616fa80e5c74456106e3e490ccfa55bec39acd3396bb962ea7`)の **Part B / Part C**
- **格**: ★ **python 単系統**(GAP cert とは別実装だが、**紙の証明の再確認**であって cert の第 2 系統としては §4 の紙が本体)

| # | 検査 | 結果 |
|---|---|---|
| **B0** | $\theta^2=I$、$\tau^3=I$(cert 行列) | PASS |
| **B1** | 行ベクトル規約で $\theta=(4.7)\bmod2$、$\tau=(4.8)\bmod2$(全 8 元で照合) | PASS |
| **B2–B4** | $\dim V^\theta=2$、$\dim V^\tau=1$、$\dim(\ker N_\theta\cap\ker N_\tau)=1$ | PASS |
| **B5–B7** | (A) 式 $=1$、直接計算 $=1$、cert の `coker_dim`=1 と一致 | PASS |
| **B8** | ★ **(B) 式は $p=2$ で $0$ を返す**(= 不適用の実証) | PASS(期待どおり) |
| **B9** | (C) 式は数値 $1$ に**偶然**一致(前件は不成立) | PASS(期待どおり) |
| **B9b** | **(B′) 式($p\ne3$ ゆえ $p=2$ で有効)$=1$**(= (A) と一致・第 3 の独立確認) | PASS |
| **B10** | $N_\tau(\tau)=N_\tau(\tau^{-1})$(規約頑健性) | PASS |
| **C1–C4** | $\lvert G_{20}\rvert=4000$、$\lvert G_5\rvert=500$、$\lvert V\rvert=8$、$\ker(\mathbf Z/10\to C_5)$ の位数 $=2$ | PASS |

**出力**: `FAILS = 0`(`RESULT: ALL PASS`)。

---

## 7. FINDING(本追補の分)

| # | 格 | 内容 |
|---|---|---|
| **W6B-1** | ★★ **紙の裏取り(主成果)** | $V=\ker(G_{20}\to G_5)=\langle r^{10}\rangle^3\cong(\mathbf Z/2)^3$ を**明示的に**決定し、$\dim_{\mathbf F_2}V=3$・初等アーベル 2 群・$\dim\operatorname{coker}\psi_V=1$ を **(A) 式のみ**で紙で導いた。cert の 10 欄すべてと一致(§3) |
| **W6B-2** | ★ **(4.7)(4.8) の射程の拡張** | 正典 (4.7)(4.8) は、基底 $(X^2,Y^2,(XY)^{-2})$ において**偶数 $m$ の $A_m=\langle r^2\rangle^3$ でも逐語で成り立つ**。本体 §1.3 は $A=[G_5,G_5]$ での形として引いていた |
| **W6B-3** | ★ **副産物** | $A_m=\langle r^2\rangle^3$($m$ 偶)を紙で証明し、定義ノート §3 の数値事実 $\lvert G_m\rvert=4(m/2)^3$ を**再導出**した(§2.1) |
| **W6B-4** | ⚠ **★教材(危険箇所 D-1 の裏面)** | **$p=5$ で全結論を決める (4.7) の符号は、$p=2$ では不可視になる。** ゆえに $\Gamma\vert_V$ の像は $S_4$ ではなく $S_3$、$V$ は 3 点置換加群。⟹ 生存表の $p=2$ 行で「A 型」と「$\mathrm{std}_3$」が同じ値なのは**両者が一致するから** |
| **W6B-5** | ⚠ **(B) は $p=2$ で偽** | 「前件が満たされないので使わない」ではなく「**使うと $0$ という誤った値が出る**」。本件はその実物である(§2.4) |
| **W6B-6** | ★ **CV-9 への入力** | 二系統は**基底が異なる**(cert は `Pcgs`・紙は $(X^2,Y^2,(XY)^{-2})$)。判定すべきは行列の逐語一致ではなく**加群としての同型**。規約(行/列)は結論に影響しない。`formulas_agree` の意味論は確認要 |

---

## 8. 【GAP】と申し送り

| 札 | 内容 |
|---|---|
| **W6B-GAP-1** | **障害類は計算していない**(S-W6-3)。DF-W6-2 の 3 項のうち紙で裏取りしたのは $\operatorname{coker}\ne0$ の 1 項のみ(§5) |
| **W6B-GAP-2** | **正典 Thm 4.4($4\mid q$ 分岐)の $d=5$ を再検分していない**。本体 §4.3 の「外部 anchor」はこの引用に依存する |
| **W6B-GAP-3** | 本追補は**単系統(紙)・Sol 未監査**。$A_m=\langle r^2\rangle^3$ の証明(§2.1)と (4.7)(4.8) の $m=20$ での成立(§2.3)は本追補が初出 |

**Sol / falsifier への論点(3 点)**
1. §2.1 の $A_m=\langle r^2\rangle^3$($m$ 偶)の証明 — $\phi=(\pi^3,\varepsilon^3)$ の像が位数 4 であることから $\ker\pi^3=\ker\phi$ を出す段に落ちはないか。
2. §2.3 の $\theta,\tau$ の規約(`ScanRoofHexagon`: $x\leftrightarrow y$;$x\mapsto y,\ y\mapsto(xy)^{-1}$)が本体 §1.3 の (4.7)(4.8) を導いた規約と**同一**か(内部自己同型の差で $a_3$ の符号がずれる余地はないか)。
3. §3 の `formulas_agree` の意味論(**(A)(B)(B′) の 3 式か、(A)(B′) と直接計算か**)。
