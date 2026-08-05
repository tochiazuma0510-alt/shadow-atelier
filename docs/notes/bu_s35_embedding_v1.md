# BU 掘削 S3.5 — $\sigma_1,\sigma_2$ の $\widehat G_5$ 内埋め込み公式 v1

**状態札: `design / paper-proof candidate / Sol 未監査 / GAP 実行ゼロ / 実測ゼロ / 封印 3 量非接触・Im R 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 委嘱: 司令塔(裁定 585 補)—「S3.5(marked lift L1〜L3)が要求する $\sigma_1,\sigma_2$ の $\widehat G_5$ 内の具体的埋め込み公式。危険点 D-1/N-4 があるため当て推量禁止」
- **入力正本**(すべて既在・外部文献ゼロ):
  - `docs/notes/w6_bottomup_design_v2.md` §3.1 定義 MARKED・§3.2 取得段 S3.5(L-1〜L-4)・§7.2 assert 表 A-0/A-1/A-2
  - `docs/notes/w6_bottomup_design_v3.md` §1.1 定義 MARK-ISO・§1.2 補題 MARK-BIJ
  - `docs/notes/w6_bottomup_design_v4.md` §1.1 FREEZE-1〜5・§1.2 発火請求範囲
  - `docs/notes/k5_w6_construction_v1.md` §1.1 記号・**§1.3 補題 GAMMA (a)(b)(c)(d) と正典 (4.7)(4.8)**・§6.1 **N-4**・§6.2 **D-1/D-2**
  - `docs/notes/conventions_ledger_v1.md` **CV-13**(向き自己検査とその射程限定 = 外部 anchor 併置義務)
  - `search/week3-battery-common.g` `MakeGn`(既在の $G_5$ 構成 = 外部 anchor)/ `search/probe/w6_bu_s0/w6_bu_s0_driver.g`(A-0〜A-13 の実装)
  - 正典 **arXiv 2405.11725 (4.7)(4.8)**(k5_w6_construction §1.3 経由の引用。**原文 PDF は本稿では開いていない** — 逐語は既在ノートからの孫引きである旨を申告)

> ## 非接触の申告
> **GAP を 1 度も起動していない。** 検算は python 単系統(整数 / $\mathbf F_5$ 演算のみ・§9)であり **cross-checked ではない**。$\mathrm{Im}\,R_{N,K^{(5)}}$ 非接触・$d_N$ 非評価・**封印 3 量非接触**($\hat c_\mu$ / PSL 窓構造量 / ε bits)・証明書非読・$u$ 値非接触。本稿は **S1〜S3.5 の発火ではない**(紙の対象設計のみ)。

---

## 0. 判定(先に 8 行)

| # | 内容 |
|---|---|
| **①** ★★★ | **委嘱の①は「明示式」側で解けた。** 鍵は **$c\in K^{(5)}$**(§2 定理 EMB-C)。これは仮定ではなく **補題 GAMMA (b) から導出できる**($Z(\widehat G_5)=1$)。⟹ $q:B_3\twoheadrightarrow\widehat G_5$ は $B_3/\langle c\rangle\cong PSL_2(\mathbf Z)\cong C_2\ast C_3$ を経由する |
| **②** ★★★ | ⟹ **marked lift の正しい変数は $(\rho(\sigma_1),\rho(\sigma_2))$ ではなく $(\rho(\Delta),\rho(\delta))$**(定理 EMB-BRAID・§3)。$U:=\rho(\Delta),\ W:=\rho(\delta)$ と置くと $$\boxed{\ \rho(\sigma_1)=W^{-1}U,\qquad \rho(\sigma_2)=U^{-1}W^2\ }$$ で、**L-1(braid)と L-2($\rho(c)=1$)は $U^2=W^3=1$ と同値**になる。⟹ **L-1 は検査項目から消え、L-2 は 2 本のアフィン線型方程式になる** |
| **③** ★★ | **$\widehat G_5\cong\mathbf F_5^3\rtimes S_4$**(Schur–Zassenhaus・§4)。明示式は §4.3: $$\widehat\sigma_1=\bigl((1,0,-1);\,T^2\Theta\bigr),\qquad \widehat\sigma_2=\bigl((0,1,1);\,\Theta T^2\bigr)$$ ($\Theta,T$ = 正典 (4.7)(4.8) の行列)。**braid・$c\mapsto1$・全射性($\lvert\langle\widehat\sigma_1,\widehat\sigma_2\rangle\rvert=3000$)を紙で検証済**(§4.4) |
| **④** ★★ | **一意性の正確な言明**(§5): $q$ の marked lift は $A$-共役を除いて **$H^1(C_2\ast C_3,A)\cong\mathbf F_5$ の 5 類**、うち **4 類が全射**で、**4 類はすべて同じ核 $K^{(5)}$ をもつ**(スカラー自己同型で移り合う)。⟹ **窓としては一意・座標としては 4 択**。さらに **$\rho(\sigma_1^2)=x,\ \rho(\sigma_2^2)=y$ を既在の `MakeGn(5)` の $x,y$ に固定すると lift は完全に一意**(命題 EMB-UNIQ) |
| **⑤** ★★★ | **15 点置換モデル(`MakeGn(5)` と同じ土俵)で $\widehat\sigma_1,\widehat\sigma_2$ を明示**(§6)。$N_{S_{15}}(G_5)$ 内で **braid + $c\mapsto1$ + $\sigma_i^2=x,y$ を満たす対はちょうど 1 組**(悉皆確認)。実装係はこれをそのまま貼れる |
| **⑥** ★★ | ★ **D-1/N-4 の罠を実証した**(§7.3): $\tau\leftrightarrow\tau^{-1}$ の取り違え(GAP の行ベクトル作用で実際に起こりうる)は **L-1・L-2・L-3 も A-0 もすべて素通りし**、**$x$ と $y$ の役割だけを入れ替える**。⟹ **既存の 4 検査は全部この罠に盲目**。検出器は「$\mathrm{Ad}(\rho(\sigma_1)^2)\vert_A=\mathrm{diag}(1,-1,-1)$」ただ 1 本(§8 F-2) |
| **⑦** ★★ | ★ **座標基底の食い違いを発見**(§7.4): `MakeGn` のブロック座標と正典 (4.7)(4.8) の座標は **$\mathrm{diag}(1,1,-1)$ だけずれている**。$\Theta$ はこの共役で不変なので**$\theta$ 側では見えず、$\tau$ 側だけに現れる**。既存 cert(A-2d は abelian invariants の比較のみ)とは**矛盾しない**が、S3.5 では効く |
| **⑧** ★ | 委嘱の②(「$G_5$ 水準への還元」)は**不要になった**が、②の実質 = 「安い機構への還元」は **§3 の線型化**が上位互換で果たす。$\lvert V\rvert^2$ 総当りは **2 本の $\mathbf F_p$-アフィン系**に落ち、解の個数は $\lvert\ker N_\theta\rvert\cdot\lvert\ker N_\tau\rvert$(§3.3・機械照合済) |

> ⚠ **本稿は凍結も発火も請求しない。** FREEZE-1〜5(v4 §1.1)への**変更提案は §10-1 の 1 点のみ**(S3.5 の検査項目 L-1/L-2 を同値な線型形へ差し替える件)で、採否は司令塔裁定 → Sol ゲート。

---

## 1. 設定と記号(**再定義しない・出所つき**)

定義ノート §1 / k5_w6_construction §1.1 のまま:

$$B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle,\qquad
\Delta:=\sigma_1\sigma_2\sigma_1,\quad \delta:=\sigma_1\sigma_2,\quad c:=\Delta^2 .$$

$$x:=\sigma_1^2,\quad y:=\sigma_2^2,\quad PB_3=F_2\times\langle c\rangle,\quad F_2=\langle x,y\rangle,$$

$$K^{(5)}=\ker\psi_5,\quad G_5=PB_3/K^{(5)}\ (\lvert G_5\rvert=500),\quad A:=[G_5,G_5]\cong C_5^3,\quad
\widehat G_5:=B_3/K^{(5)}\ (\lvert\widehat G_5\rvert=3000),$$

$$q:B_3\twoheadrightarrow\widehat G_5,\qquad \widehat G_5/A\cong S_4,\qquad G_5/A\cong V_4=O_2(S_4).$$

正典 2405.11725 の作用式(k5_w6_construction §1.3 で引用・**本稿の基底の定義**):

$$\textbf{(4.7)}\quad \theta(r^{2n_1},r^{2n_2},r^{2n_3})=(r^{2n_2},r^{2n_1},r^{-2n_3}),\qquad
\textbf{(4.8)}\quad \tau(r^{2n_1},r^{2n_2},r^{2n_3})=(r^{2n_3},r^{2n_1},r^{2n_2}),$$

$$\Theta:=\begin{pmatrix}0&1&0\\1&0&0\\0&0&-1\end{pmatrix},\qquad
T:=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}\qquad(\text{列ベクトルに左から作用}).$$

> ### ★★★ 用語の固定(**N-4 / D-1 の直撃点**)
> $$\boxed{\ \theta:=\mathrm{Ad}(\Delta),\qquad \tau:=\mathrm{Ad}(\delta)\qquad(\mathrm{Ad}(g)(h)=ghg^{-1})\ }$$
> **$\theta,\tau$ は $\sigma_1,\sigma_2$ の像ではない。** $S_4=\widehat G_5/A$ における像として
> $$\Delta\mapsto\theta=(1\,2)\ (\text{位数 }2),\qquad \delta\mapsto\tau=(1\,3\,4)\ (\text{位数 }3),$$
> $$\boxed{\ \sigma_1=\delta^{-1}\Delta\mapsto \tau^{-1}\theta=\tau^2\theta=(1\,2\,4\,3),\qquad \sigma_2=\Delta^{-1}\delta^2\mapsto\theta^{-1}\tau^{2}=\theta\tau^2=(1\,4\,3\,2)\qquad(\textbf{どちらも位数 }4\textbf{ の 4-巡回})\ }$$
> ⟹ **「$\rho(\sigma_1)$ は $(1\,2)$ の上に乗る」「$\rho(\sigma_2)$ は $(1\,3\,4)$ の上に乗る」は誤り。** v2 §7.2 A-0 の $\theta=(1\,2),\tau=(1\,3\,4)$ は $\Delta,\delta$ のラベルである。$\sigma_i$ の像は $V_4$ の外の 4-巡回であり、$\sigma_i^2$ の像がはじめて $V_4$ に落ちる。

$\Delta,\delta$ から $\sigma_i$ を戻す式(k5_w6_construction §1.3 (d) の $\Delta^{-1}\delta^2=\sigma_2$ を含む):

$$\sigma_1=\delta^{-1}\Delta,\qquad \sigma_2=\Delta^{-1}\delta^2,\qquad \delta^3=\Delta^2=c. \tag{1.1}$$

**(1.1) の検算(紙)**: $\delta^{-1}\Delta=\sigma_2^{-1}\sigma_1^{-1}\cdot\sigma_1\sigma_2\sigma_1=\sigma_1$ ✓。
$\Delta^{-1}\delta^2=\sigma_1^{-1}\sigma_2^{-1}\sigma_1^{-1}\cdot\sigma_1\sigma_2\sigma_1\sigma_2=\sigma_1^{-1}\sigma_2^{-1}\cdot\sigma_2\sigma_1\sigma_2=\sigma_2$ ✓。
$\delta^3=\sigma_1\sigma_2\sigma_1\sigma_2\sigma_1\sigma_2\overset{(3,4,5)}{=}\sigma_1\sigma_2(\sigma_2\sigma_1\sigma_2)\sigma_2=\sigma_1\sigma_2^2\sigma_1\sigma_2^2$、
$\Delta^2=\sigma_1\sigma_2\sigma_1^2\sigma_2\sigma_1$。両者の一致は $\sigma_2\sigma_1\sigma_2^2=\sigma_1^2\sigma_2\sigma_1$、すなわち $(\sigma_2\sigma_1\sigma_2)\sigma_2=\sigma_1(\sigma_1\sigma_2\sigma_1)$、すなわち $\sigma_1\sigma_2\sigma_1\sigma_2=\sigma_1\sigma_2\sigma_1\sigma_2$ ✓。∎

---

## 2. ★★★ 定理 EMB-C — $c\in K^{(5)}$(**すべての鍵・仮定ではなく導出**)

> ### 定理 EMB-C(candidate・本稿)
> $$Z(\widehat G_5)=1,\qquad\text{したがって}\qquad q(c)=1,\quad\text{すなわち}\quad c\in K^{(5)}.$$

**証明.** 補題 GAMMA (b)(k5_w6_construction §1.3・機械確認済)より $C_{\widehat G_5}(A)=A$。ゆえに
$Z(\widehat G_5)\subseteq C_{\widehat G_5}(A)=A$、したがって $Z(\widehat G_5)\subseteq A^{\widehat G_5}=A^{S_4}$。
補題 GAMMA (c) より $A\cong\mathrm{std}_3\otimes\mathrm{sgn}$ は $S_4$-加群として非自明既約であり $A^{S_4}=0$。⟹ $Z(\widehat G_5)=1$。
$c\in Z(B_3)$ ゆえ $q(c)\in Z(\widehat G_5)=1$。∎

> ### ★ 帰結(**設計上の意味**)
> $B_3=\langle\Delta,\delta\mid\Delta^2=\delta^3\rangle$(標準表示)ゆえ
> $$B_3/\langle c\rangle=\langle\Delta,\delta\mid\Delta^2=\delta^3=1\rangle\cong C_2\ast C_3\cong PSL_2(\mathbf Z).$$
> 定理 EMB-C より $q$ はこれを経由する。**marked datum の条件 $\rho(c)=1$(v2 §3.1)も同じ経由を強制する。**
> ⟹ **S3.5 の全体が $C_2\ast C_3$ の表現論に落ちる**(§3)。これが本稿の設計上の主張である。

> ⚠ **整合確認**: v2 §3.1 定義 MARKED は $\rho(c)=1$ を要求し、$\pi_{\widehat P}\circ\rho=q$ を要求する。両立には $q(c)=1$ が**必要**である。定理 EMB-C はこの必要条件が実際に成り立つことを示す。⟹ **定義 MARKED は空でない**(v2 は暗黙にこれを使っていた)。**この 1 行は v2/v3/v4 のどこにも書かれていない** — 【BU-GAP-10】として §10 に起票する。

---

## 3. ★★★ 定理 EMB-BRAID — marked lift の正しい変数(**L-1 が消える**)

### 3.1 主張

拡大 $1\to V\to\widehat P\xrightarrow{\pi}\widehat G_5\to1$ を固定する($V$ は有限 $\mathbf F_p[\widehat G_5]$-加群・v2 §3.1)。

> ### 定理 EMB-BRAID(candidate・本稿)
> 写像
> $$\Bigl\{\rho:B_3\to\widehat P\ \Bigm|\ \pi\circ\rho=q,\ \rho(c)=1\Bigr\}
> \ \xrightarrow{\ \sim\ }\
> \Bigl\{(U,W)\in\widehat P^2\ \Bigm|\ U^2=W^3=1,\ \pi(U)=q(\Delta),\ \pi(W)=q(\delta)\Bigr\}$$
> $$\rho\longmapsto\bigl(\rho(\Delta),\rho(\delta)\bigr),\qquad
> (U,W)\longmapsto\Bigl[\sigma_1\mapsto W^{-1}U,\ \ \sigma_2\mapsto U^{-1}W^2\Bigr]$$
> は**全単射**である。とくに
> $$\boxed{\ \textbf{L-1}\ (\text{braid})\ \text{は自動};\qquad \textbf{L-2}\ (\rho(c)=1)\ \iff\ U^2=1\ \wedge\ W^3=1.\ }$$

**証明.**
**(→)** $U:=\rho(\Delta)$、$W:=\rho(\delta)$。$U^2=\rho(\Delta^2)=\rho(c)=1$ ✓。$W^3=\rho(\delta^3)=\rho(c)=1$ ✓((1.1))。$\pi(U)=q(\Delta)$ ✓。
**(←)** $U^2=W^3=1$ とし $s_1:=W^{-1}U$、$s_2:=U^{-1}W^2$ と置く。
$$s_1s_2s_1=W^{-1}U\cdot U^{-1}W^2\cdot W^{-1}U=W^{-1}\cdot W^2W^{-1}\cdot U=U,$$
$$s_2s_1s_2=U^{-1}W^2\cdot W^{-1}U\cdot U^{-1}W^2=U^{-1}\cdot W^2W^{-1}\cdot W^2=U^{-1}W^3=U^{-1}=U.$$
⟹ $s_1s_2s_1=s_2s_1s_2$(**braid 関係が成立**)。ゆえに $\sigma_i\mapsto s_i$ は準同型 $\rho$ を定め、$\rho(\Delta)=s_1s_2s_1=U$、$\rho(\delta)=s_1s_2=W^{-1}U\cdot U^{-1}W^2=W$、$\rho(c)=\rho(\Delta)^2=U^2=1$ ✓。$\pi\circ\rho=q$ は生成元 $\sigma_1,\sigma_2$ 上で $\pi(s_1)=q(\delta)^{-1}q(\Delta)=q(\sigma_1)$ ✓ 同様に $\sigma_2$ ✓。
**互いに逆**: 上の 2 つの計算がそのまま両側の逆写像であることを示している。∎

> ### ★ なぜこれが重要か(**D-1 対策としても**)
> 1. **L-1 を実装しなくてよくなる。** v2 §3.2 の L-1 は 3 文字の語を 2 通りに評価して突合する検査で、**GAP の左右合成規約を踏み外すと静かに壊れる**。定理 EMB-BRAID の形なら検査語は $U^2$ と $W^3$ の 2 本だけで、**どちらも合成順に依存しない**($U^2$ は自明、$W^3$ は巡回)。
> 2. **braid 語は回文**($\sigma_1\sigma_2\sigma_1$ を逆から読んでも同じ)なので L-1 自体は合成規約に鈍感だが、**$\delta=\sigma_1\sigma_2$ は回文でない** — 危険は $\Delta$ ではなく $\delta$ 側に集中する(§7 で実証)。

### 3.2 ★★ 系 EMB-LIN(**S3.5 の線型化** — $\lvert V\rvert^2$ 総当りの廃止)

$U_0\in\pi^{-1}(q(\Delta))$、$W_0\in\pi^{-1}(q(\delta))$ を任意の集合論的持上げとし
$$\varepsilon_\Delta:=U_0^2\in V,\qquad \varepsilon_\delta:=W_0^3\in V$$
と置く($\pi(U_0^2)=q(\Delta)^2=q(c)=1$ ゆえ $U_0^2\in V$ ✓・定理 EMB-C)。$V$ を加法的に書き、$\theta,\tau$ で $q(\Delta),q(\delta)$ の $V$ への作用を表す。

> ### 系 EMB-LIN(candidate・本稿)
> $U=U_0a$、$W=W_0b$($a,b\in V$)と書くと
> $$U^2=1\iff N_\theta(a):=a+\theta a=-\varepsilon_\Delta,\qquad
> W^3=1\iff N_\tau(b):=b+\tau b+\tau^2b=-\varepsilon_\delta .$$
> ⟹ **marked lift の集合は 2 本の独立なアフィン線型系の解の直積**であり、
> $$\#\{\text{marked lift}\}=
> \begin{cases}
> \lvert\ker N_\theta\rvert\cdot\lvert\ker N_\tau\rvert & (\varepsilon_\Delta\in\operatorname{im}N_\theta\ \wedge\ \varepsilon_\delta\in\operatorname{im}N_\tau)\\[2pt]
> 0 & (\text{それ以外})
> \end{cases}$$
> **持上げの存在条件**は $[\varepsilon_\Delta]=0$ in $H^2(C_2,V)=V^\theta/N_\theta V$ かつ $[\varepsilon_\delta]=0$ in $H^2(C_3,V)=V^\tau/N_\tau V$、すなわち **$q^\ast[\varepsilon]$ の $\langle q(\Delta)\rangle$ と $\langle q(\delta)\rangle$ への制限が消えること**。

**証明.** $U^2=U_0aU_0a=U_0^2\cdot(U_0^{-1}aU_0)\cdot a=\varepsilon_\Delta+\theta^{-1}a+a$。$\theta^2=\mathrm{id}_V$($q(\Delta)^2=1$)ゆえ $\theta^{-1}=\theta$ ⟹ $U^2=\varepsilon_\Delta+N_\theta(a)$。
$W^3=W_0bW_0bW_0b=W_0^3\cdot(W_0^{-2}bW_0^{2})(W_0^{-1}bW_0)b=\varepsilon_\delta+\tau^{-2}b+\tau^{-1}b+b=\varepsilon_\delta+N_\tau(b)$($\tau^3=\mathrm{id}$ ゆえ $\{1,\tau^{-1},\tau^{-2}\}=\{1,\tau,\tau^2\}$)。
存在条件は $-\varepsilon_\Delta\in\operatorname{im}N_\theta$ ⟺ $[\varepsilon_\Delta]=0$ in $V^\theta/N_\theta V$($\varepsilon_\Delta\in V^\theta$ は $\theta\varepsilon_\Delta=U_0U_0^2U_0^{-1}=\varepsilon_\Delta$ から)。$C_3$ 側も同様(Tate コホモロジー $\widehat H^0$)。∎

> ### ★★ ここに現れる $N_\theta,N_\tau$ は **W6-OBS の $\psi_V=(N_\theta,N_\tau)$ と同じ 2 本のノルム**である
> ただし**掛かる対象が違う**: W6-OBS(k5_w6_construction §2.3)は $\widetilde f_0$ の障害類 $[(-\beta_\theta,-\beta_\tau)]\in\operatorname{coker}\psi_V$ を扱い、EMB-LIN は $\rho$ の存在障害 $(\varepsilon_\Delta,\varepsilon_\delta)$ を扱う。**同じ線型代数部品($\ker N_\theta,\ker N_\tau,\operatorname{im}N_\theta,\operatorname{im}N_\tau$)を S3.5 と S6/S7 で共有できる**ので、実装は 1 つの $\mathbf F_p$-モジュールで足りる。⚠ **両者を同一視してはならない**(別の量である)— 【BU-GAP-11】(§10)。

### 3.3 機械照合(2 レーン)

$V=\mathbf F_2^3$($S_4\to S_4/V_4\cong S_3$ から inflate した 3 点置換加群 = $K^{(20)}$ の加群・addendum B §2.3)、$\widehat P=V\rtimes\widehat G_5$、$U_0,W_0$ を**わざと非標準に**取った 3 例で:

| $u_0$ | $w_0$ | $\varepsilon_\Delta$ | $\varepsilon_\delta$ | lane A(線型) | lane B(悉皆 $\lvert V\rvert^2$) | |
|---|---|---|---|---|---|---|
| $(0,0,0)$ | $(0,0,0)$ | $0$ | $0$ | **16** | **16** | MATCH |
| $(1,0,0)$ | $(0,1,1)$ | $0$ | $0$ | **16** | **16** | MATCH |
| $(1,1,0)$ | $(1,0,0)$ | $(0,1,1)$ | $(1,1,1)$ | **16** | **16** | MATCH |

$\lvert\ker N_\theta\rvert=4$、$\lvert\ker N_\tau\rvert=4$ ⟹ 積 16 ✓。
スクリプト: `scratchpad/bu_s35_linearize.py`(SHA-256 `c6590582da6bbff34387f9b51a1d52e17c334d5bb7ccf79cbdf1ab6837bf190b`)。
⚠ **python 単系統・cross-checked ではない。**

---

## 4. ★★★ $\widehat G_5$ の明示モデルと $\sigma_1,\sigma_2$ の式

### 4.1 補題 EMB-SPLIT

> ### 補題 EMB-SPLIT(candidate・本稿)
> $$\widehat G_5\ \cong\ A\rtimes S_4\ =\ \mathbf F_5^3\rtimes S_4,$$
> ここで $S_4$ は $A$ に $\langle\Theta,T\rangle$($=\det=+1$ の符号付き置換行列全体 $\cong S_4$)として作用する。補群はすべて共役。

**証明.** $A=[G_5,G_5]$ は $G_5\trianglelefteq\widehat G_5$ の特性部分群ゆえ $A\trianglelefteq\widehat G_5$。$\lvert A\rvert=125$、$\lvert\widehat G_5/A\rvert=24$、$\gcd(125,24)=1$ ⟹ Schur–Zassenhaus により分裂し補群は共役。作用は補題 GAMMA (b)(忠実・像は $\langle\Theta,T\rangle$、位数 24)。∎

記法: 元を $(a;s)$($a\in\mathbf F_5^3$ 列ベクトル、$s\in S_4$)と書き
$$(a;s)(b;t)=\bigl(a+M(s)b;\ st\bigr),\qquad M(\theta)=\Theta,\quad M(\tau)=T. \tag{4.1}$$

### 4.2 $\Delta,\delta$ の明示元(**規約 EMB-NORM**)

> ### 規約 EMB-NORM(本稿が固定する選択・§5 で非一意性を会計する)
> $$\boxed{\ \widehat\Delta:=\bigl((0,0,0);\ \theta\bigr),\qquad
> \widehat\delta:=\bigl((1,-1,0);\ \tau\bigr)\ }$$
> ($(1,-1,0)$ は $f_1=(r^2,r^{-2},1)$ の指数座標。**この一致は語呂であって導出ではない** — §5 の 4 択のうち $t=1$ を取っただけである)。

**検査**: $\widehat\Delta^2=\bigl((I+\Theta)\cdot0;1\bigr)=(0;1)$ ✓。
$\widehat\delta^3=\bigl((I+T+T^2)(1,-1,0);1\bigr)$、$(1,-1,0)+(0,1,-1)+(-1,0,1)=(0,0,0)$ ✓。

### 4.3 ★★★ 主公式

(1.1) と (4.1) から($\widehat\delta^{-1}=\bigl((1,0,-1);\tau^2\bigr)$、$\widehat\delta^2=\bigl((1,0,-1);\tau^2\bigr)$):

$$\boxed{\ \widehat\sigma_1=\widehat\delta^{-1}\widehat\Delta=\bigl((1,0,-1);\ \tau^2\theta\bigr),
\qquad
\widehat\sigma_2=\widehat\Delta^{-1}\widehat\delta^{\,2}=\bigl((0,1,1);\ \theta\tau^2\bigr)\ }\tag{4.2}$$

行列部分(**列ベクトル規約**):

$$M(\sigma_1)=T^2\Theta=\begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}:\ (n_1,n_2,n_3)\mapsto(n_1,-n_3,n_2),$$
$$M(\sigma_2)=\Theta T^2=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}:\ (n_1,n_2,n_3)\mapsto(n_3,n_2,-n_1).$$

### 4.4 紙による検証(**委嘱の「紙で検証せよ」への履行**)

**(a) braid 関係.**
$\widehat\sigma_1\widehat\sigma_2=\bigl((1,0,-1)+M(\sigma_1)(0,1,1);\ \tau^2\theta\cdot\theta\tau^2\bigr)$。
$M(\sigma_1)(0,1,1)=(0,-1,1)$、$(1,0,-1)+(0,-1,1)=(1,-1,0)$;$\tau^2\theta\theta\tau^2=\tau^4=\tau$。
⟹ $\widehat\sigma_1\widehat\sigma_2=\bigl((1,-1,0);\tau\bigr)=\widehat\delta$ ✓。
$\widehat\sigma_1\widehat\sigma_2\widehat\sigma_1=\widehat\delta\,\widehat\sigma_1=\bigl((1,-1,0)+T(1,0,-1);\ \tau\cdot\tau^2\theta\bigr)$、$T(1,0,-1)=(-1,1,0)$ ⟹ 和は $(0,0,0)$、$\tau^3\theta=\theta$。
⟹ $\widehat\sigma_1\widehat\sigma_2\widehat\sigma_1=(0;\theta)=\widehat\Delta$ ✓。
$M(\sigma_2\sigma_1)=\Theta T^2T^2\Theta=\Theta T\Theta:(n_1,n_2,n_3)\mapsto(n_2,-n_3,-n_1)$。
$\widehat\sigma_2\widehat\sigma_1=\bigl((0,1,1)+M(\sigma_2)(1,0,-1);\ \cdot\bigr)$、$M(\sigma_2)(1,0,-1)=(-1,0,-1)$ ⟹ $(-1,1,0)$。
$\widehat\sigma_2\widehat\sigma_1\widehat\sigma_2=\bigl((-1,1,0)+M(\sigma_2\sigma_1)(0,1,1);\ \Theta T\Theta\cdot\Theta T^2\bigr)$、$M(\sigma_2\sigma_1)(0,1,1)=(1,-1,0)$ ⟹ 和 $(0,0,0)$;$\Theta T\Theta\Theta T^2=\Theta T^3=\Theta$。
⟹ $\widehat\sigma_2\widehat\sigma_1\widehat\sigma_2=(0;\theta)=\widehat\Delta$ ✓。
$$\Longrightarrow\quad \widehat\sigma_1\widehat\sigma_2\widehat\sigma_1=\widehat\sigma_2\widehat\sigma_1\widehat\sigma_2=\widehat\Delta.\quad\blacksquare$$

**(b) $c\mapsto1$.** $\widehat c=(\widehat\sigma_1\widehat\sigma_2\widehat\sigma_1)^2=\widehat\Delta^2=(0;1)$ ✓(§4.2)。

**(c) 全射性 $\lvert\langle\widehat\sigma_1,\widehat\sigma_2\rangle\rvert=3000$.**
$H:=\langle\widehat\sigma_1,\widehat\sigma_2\rangle=\langle\widehat\Delta,\widehat\delta\rangle$((1.1) と (a) から双方向)。
$\pi_A(H)=\langle\theta,\tau\rangle=\langle(1\,2),(1\,3\,4)\rangle=S_4$(推移的 + 転置 + 3-巡回)。
$H\cap A$ は $H$ で正規化され、$\pi_A(H)=S_4$ ゆえ $A$ の $S_4$-部分加群。$5\nmid24$ ゆえ $\mathbf F_5[S_4]$ は半単純で、$A\cong\mathrm{std}_3\otimes\mathrm{sgn}$ は**絶対既約**($S_4$ の全既約は $\mathbf Q$ 上実現可能・Schur 指数 1)。⟹ $H\cap A\in\{0,A\}$。
$H\cap A\ne0$ を示す: $\widehat\Delta\widehat\delta=\bigl(\Theta(1,-1,0);\theta\tau\bigr)=\bigl((-1,1,0);\theta\tau\bigr)$、$M(\theta\tau)=\Theta T:(n)\mapsto(n_1,n_3,-n_2)$、$(\theta\tau)^2=\mathrm{diag}(1,-1,-1)$。
$(\widehat\Delta\widehat\delta)^2=\bigl((-1,1,0)+(-1,0,-1);(\theta\tau)^2\bigr)=\bigl((-2,1,-1);(\theta\tau)^2\bigr)$、
$(\widehat\Delta\widehat\delta)^4=\bigl((-2,1,-1)+\mathrm{diag}(1,-1,-1)(-2,1,-1);1\bigr)=\bigl((-4,0,0);1\bigr)=\bigl((1,0,0);1\bigr)\ne1$。
⟹ $H\cap A=A$ ⟹ $\lvert H\rvert=125\cdot24=3000$ ✓。∎

**(d) 位数(fixture 用).** $\widehat\sigma_1^{\,4}=\bigl(\sum_{k=0}^3M(\sigma_1)^k(1,0,-1);1\bigr)$、
$(1,0,-1)+(1,1,0)+(1,0,1)+(1,-1,0)=(4,0,0)\ne0$ ⟹ $\mathrm{ord}(\widehat\sigma_1)=20$。同様に $\mathrm{ord}(\widehat\sigma_2)=20$。
$\widehat x:=\widehat\sigma_1^{\,2}=\bigl((2,1,-1);\mathrm{diag}(1,-1,-1)\bigr)$、$\widehat y:=\widehat\sigma_2^{\,2}=\bigl((1,2,1);\mathrm{diag}(-1,1,-1)\bigr)$、ともに位数 **10**。

### 4.5 $S_4$ ラベルの再現(**A-0 の規約と逐点一致すること**)

$S_4$ は「立方体の 4 本の対角線」への作用として実現される($\det=+1$ 符号付き置換行列 = 立方体の回転群)。**対角線ラベル**を

$$\ell(1)=[1{:}1{:}{-}1],\quad \ell(2)=[1{:}1{:}1],\quad \ell(3)=[{-}1{:}1{:}1],\quad \ell(4)=[1{:}{-}1{:}1]\qquad(\pm\text{ を同一視})$$

と取ると:

| 元 | $A$ 上の作用 | $S_4$ ラベル | 位数 |
|---|---|---|---|
| $\widehat\Delta$ | $\Theta$ | **$(1\,2)$** = $\theta$ | 2 |
| $\widehat\delta$ | $T$ | **$(1\,3\,4)$** = $\tau$ | 3 |
| $\widehat\Delta\widehat\delta$ | $\Theta T$ | $(1\,3\,4\,2)$ | **4** ← A-0 |
| $\widehat\sigma_1$ | $T^2\Theta$ | **$(1\,2\,4\,3)$** | 4 |
| $\widehat\sigma_2$ | $\Theta T^2$ | **$(1\,4\,3\,2)$** | 4 |

⟹ **v2 §7.2 A-0 の $\theta=(1\,2)$、$\tau=(1\,3\,4)$、$\mathrm{ord}(\theta\tau)=4$ を、正典 (4.7)(4.8) の行列から明示ラベル $\ell$ つきで再現した。** 既存 assert と矛盾しない。

> ### ★ 補足: $(\theta,\tau)$ は $\mathrm{ord}(\theta\tau)$ で一意に決まる
> $S_4$ 内の(転置, 3-巡回)対は同時共役で**ちょうど 2 軌道**(対の個数 $6\times8=48$、安定化群 $C(\theta)\cap C(\tau)=1$ ⟹ 軌道長 24 ⟹ 2 軌道)。両軌道は $\mathrm{ord}(\theta\tau)\in\{2,4\}$ で完全に分離する。⟹ **A-0(位数 4)は「対の共役類」を一意に固定する** — 危険箇所 D-2 の検出器としては**必要十分**である。
> ⚠ **しかし A-0 は $\tau$ と $\tau^{-1}$ を区別しない**($\mathrm{ord}(\theta\tau^{-1})$ も 4)。⟹ **D-1 の残りは A-0 では捕まらない**(§7.3)。

---

## 5. ★★ 一意性 / 非一意性の会計(**委嘱の拘束「一意性を主張するなら根拠・非一意なら選択の規約」**)

### 5.1 命題 EMB-H1

> ### 命題 EMB-H1(candidate・本稿)
> $q$ の marked lift $\rho:B_3\to\widehat G_5$($\pi_A\circ\rho=\bar q$、$\rho(c)=1$)の集合を $A$-共役で割ると
> $$\mathrm{Lift}/A\text{-conj}\ \cong\ H^1(C_2\ast C_3,\,A)\ \cong\ A/(A^\theta+A^\tau)\ \cong\ \mathbf F_5\quad(\textbf{5 類}).$$
> このうち **$t=0$ の 1 類は像が $S_4$(位数 24)で全射でない**;**残り 4 類はすべて全射**($\lvert\mathrm{im}\rvert=3000$)。
> **4 類はスカラー自己同型 $\varphi_\lambda:(a;s)\mapsto(\lambda a;s)$($\lambda\in\mathbf F_5^\times$)で移り合い、したがって $\ker\rho$ はすべて等しい。**

**証明.** 定理 EMB-BRAID より lift は対 $(U,W)=\bigl((\alpha;\theta),(\beta;\tau)\bigr)$ with $(I+\Theta)\alpha=0$、$(I+T+T^2)\beta=0$ と同一視される($Z^1$)。$A$-共役 $(\gamma;1)$ は $(\alpha,\beta)\mapsto(\alpha+(I-\Theta)\gamma,\ \beta+(I-T)\gamma)$($B^1$)。
$C_2\ast C_3$ の Mayer–Vietoris($H=1$):
$$0\to A^{\Gamma}\to A^{\theta}\oplus A^{\tau}\to A\to H^1(C_2\ast C_3,A)\to H^1(C_2,A)\oplus H^1(C_3,A)\to0 .$$
$\gcd(\lvert C_2\rvert\lvert C_3\rvert,5)=1$ ⟹ 右端 2 項は 0。$A^\Gamma=0$。$\dim A^\theta=\dim A^\tau=1$ ⟹ $\dim H^1=3-2=1$ ⟹ $\lvert H^1\rvert=5$ ✓。
**代表系**: $\operatorname{im}(I-\Theta)=\ker(I+\Theta)$($\Theta$ の固有値は $+1$ が 1 重・$-1$ が 2 重)ゆえ $\alpha=0$ に正規化できる。残る自由度は $\gamma\in A^\theta=\langle(1,1,0)\rangle$ で、$\beta\mapsto\beta+(I-T)(g,g,0)=\beta+(g,0,-g)$。⟹ $\beta\in\{\sum\beta_i=0\}/\langle(1,0,-1)\rangle$、代表 $\beta=t\cdot(1,-1,0)$、$t\in\mathbf F_5$。
**全射性**: §4.4 (c) と同じ論法。$\mathrm{im}\rho\cap A$ は $A$ の $S_4$-部分加群 = $0$ か $A$。$0$ ⟺ $\mathrm{im}\rho$ が補群 ⟺ 類が自明 ⟺ $t=0$。
**$\varphi_\lambda$**: $\varphi_\lambda\bigl((0;\theta)\bigr)=(0;\theta)$、$\varphi_\lambda\bigl((t(1,-1,0);\tau)\bigr)=(\lambda t(1,-1,0);\tau)$ ⟹ $\rho_{t'}=\varphi_{t'/t}\circ\rho_t$($t,t'\ne0$)⟹ $\ker\rho_{t'}=\ker\rho_t$。∎

**機械確認**(`scratchpad/bu_s35_embed_check.py`, SHA-256 `a1f8b0f167b87d57e472b0076ee073cb6e0bac899ec18609156c077a9935175d`):
$\lvert Z^1\rvert=625$、$\lvert B^1\rvert=125$、$\lvert H^1\rvert=5$;$Z^1$ の 625 対のうち **500 対が位数 3000 を生成・125 対が位数 24**(= ちょうど $B^1$ = 自明類)✓。

### 5.2 ★ 命題 EMB-UNIQ(**$x,y$ を固定すれば完全に一意**)

> ### 命題 EMB-UNIQ(candidate・本稿)
> $\rho,\rho'$ を $\bar q$ の全射 marked lift とし、$\rho(\sigma_1^2)=\rho'(\sigma_1^2)$ かつ $\rho(\sigma_2^2)=\rho'(\sigma_2^2)$ とする。このとき $\rho=\rho'$。

**証明.** 命題 EMB-H1 より $\rho'=\varphi_\lambda\circ\mathrm{conj}_a\circ\rho$($\lambda\in\mathbf F_5^\times$、$a\in A$)と書ける。$\psi:=\varphi_\lambda\circ\mathrm{conj}_a$ と置く。
$\psi$ は $\rho(x)$ と $\rho(y)$ を固定するので $\langle\rho(x),\rho(y)\rangle=\rho(PB_3)=G_5$ を**各点固定**する。とくに $A\subseteq G_5$ を各点固定。$\psi\vert_A=\lambda\cdot\mathrm{id}$ ⟹ $\lambda=1$。
残る $\mathrm{conj}_a$ が $\rho(x),\rho(y)$ を固定 ⟹ $a\in C_A(\rho(x))\cap C_A(\rho(y))$。§4.4 (d) より $\rho(x)$ の $A$ 上の作用は $\mathrm{diag}(1,-1,-1)$、$\rho(y)$ は $\mathrm{diag}(-1,1,-1)$ ⟹ $C_A(\rho(x))=\langle e_1\rangle$、$C_A(\rho(y))=\langle e_2\rangle$、交叉 $=0$ ⟹ $a=0$ ⟹ $\psi=\mathrm{id}$。∎

> ### ★ 設計上の帰結(**規約 EMB-NORM の正当化**)
> $$\boxed{\ \textbf{窓 }N=\ker\rho\textbf{ は 4 択に依存しない(EMB-H1)。座標(}\widehat\sigma_i\textbf{ の }A\textbf{-成分)だけが }t\in\{1,2,3,4\}\textbf{ で動く。}\ }$$
> 本稿は $t=1$ を **規約 EMB-NORM** として固定する。**この選択は数学的内容を持たない**(スカラー自己同型で移る)が、**$\rho(\sigma_1^2)$ を既在の `MakeGn(5)` の $x$ に合わせるという第 2 の規約を課すと $t$ も一意に決まる**(命題 EMB-UNIQ)。⟹ §6 の 15 点モデルが**正典的な代表**である。

---

## 6. ★★★ 15 点置換モデル(**`MakeGn(5)` 互換 — 実装係が直に貼れる形**)

### 6.1 土俵

`search/week3-battery-common.g` の `MakeGn(5)` と**同一の点集合・同一の $x,y$**:
点 $1..15$、ブロック $i$ = 点 $5(i-1)+1..5i$、$r=(1,2,3,4,5)$、$s=(2,5)(3,4)$、
$$x=\mathrm{tr}(r,1)\,\mathrm{tr}(s,2)\,\mathrm{tr}(s,3),\qquad y=\mathrm{tr}(sr,1)\,\mathrm{tr}(r,2)\,\mathrm{tr}(sr,3),\qquad G_5=\langle x,y\rangle\ (\lvert G_5\rvert=500).$$

### 6.2 ★★★ 結果

$$\boxed{\begin{aligned}
\widehat\sigma_1&=(1,4,2,5,3)(6,11)(7,12,10,15)(8,13,9,14)\\
\widehat\sigma_2&=(1,12,2,11)(3,15,5,13)(4,14)(6,9,7,10,8)
\end{aligned}}$$

導かれる元:

| 元 | 置換 | 位数 |
|---|---|---|
| $\widehat\Delta=\widehat\sigma_1\widehat\sigma_2\widehat\sigma_1$ | $(1,8)(2,9)(3,10)(4,6)(5,7)(11,14)(12,13)$ | **2** |
| $\widehat\delta=\widehat\sigma_1\widehat\sigma_2$ | $(1,14,6)(2,13,7)(3,12,8)(4,11,9)(5,15,10)$ | **3** |
| $\widehat\sigma_1,\widehat\sigma_2$ | 上 | **20** |
| $\widehat x=\widehat\sigma_1^{\,2},\ \widehat y=\widehat\sigma_2^{\,2}$ | $=x,\ =y$(`MakeGn` の値と**バイト一致**) | **10** |

$$\lvert\langle\widehat\sigma_1,\widehat\sigma_2\rangle\rvert=\mathbf{3000},\qquad
\lvert\langle x,y\rangle\rvert=500,\qquad \widehat\Delta^2=\mathrm{id}\ (=\widehat c).$$

⚠ **合成規約**: 上の値は **GAP の左から右**($p\ast q$ = 「$p$ してから $q$」)で検証した。braid 語 $\sigma_1\sigma_2\sigma_1$ は回文なので規約に鈍感だが、**$\delta=\sigma_1\sigma_2$ は鈍感でない**。

### 6.3 ★★ 悉皆一意性

> ### 命題 EMB-PERM(本稿・機械悉皆)
> $\rho(PB_3)=G_5\trianglelefteq\rho(B_3)$ ゆえ $\widehat\sigma_i\in N_{S_{15}}(G_5)$ が必要。$G_5$ の軌道はちょうど 3 ブロックで各ブロック上の誘導群は $D_5$、$N_{S_5}(D_5)=F_{20}=AGL(1,5)$ ⟹ $N_{S_{15}}(G_5)\subseteq F_{20}\wr S_3$($\lvert\cdot\rvert=48{,}000$)。
> この 48,000 元の中で
> $$g_1^2=x,\quad g_2^2=y,\quad g_1g_2g_1=g_2g_1g_2,\quad (g_1g_2g_1)^2=1$$
> を満たす対は **ちょうど 1 組**(= §6.2)であり、それは位数 3000 を生成する。

**機械確認**: `scratchpad/bu_s35_perm_uniqueness.py`(SHA-256 `eb2f3ce34e8ef30494ace894758e5ef6341635086a1c69ae6485cd6f2be50838`)。$g^2=x$ の解 8 個・$g^2=y$ の解 8 個・64 対中 **1 対**のみ通過。
これは命題 EMB-UNIQ の**独立な追認**(紙の論法とは別経路)である。⚠ ただし**同一の python 単系統**なので **cross-checked ではない**(CV-9 判読対象外)。

### 6.4 ★ 惜しい誤答(**negative fixture**)

$g^2=x$ の解のうち $D_5\wr S_3$ 内にあるもう 1 つは
$$(1,4,2,5,3)(6,11)(7,15,10,12)(8,14,9,13)\qquad(\textbf{FAIL} — \text{braid を通らない})$$
$g^2=y$ の側は
$$(1,11,2,12)(3,13,5,15)(4,14)(6,9,7,10,8)\qquad(\textbf{FAIL})$$
⟹ **「$\sigma_1^2=x$ を満たす」だけでは足りない**(2 択のうち 1 つは braid で落ちる)。実装が平方根を 1 つ拾って済ませると 1/2 の確率で誤る。

---

## 7. ★★★ 既存規約との逐点整合(**D-1 / N-4 / D-2 / CV-13**)

### 7.1 N-4($\rho$ の記号衝突)との整合

k5_w6_construction §6.1 **N-4** は「addendum の $\rho$($\widehat G_5$-加群の型)と `hs_prop7_translation_v1.md` の $\rho$(位数 5 の巡回作用)は別物」と警告する。
**本稿の $\rho$ は第 3 の意味**(v2 §3.1 の marked lift $\rho:B_3\to\widehat P$)である。
⟹ **本稿では加群の型を $\rho$ と呼ばない**。$A\cong\mathrm{std}_3\otimes\mathrm{sgn}$ と書く(k5_w6_construction §6.1 の指示に逐語従う)。**位数 5 の巡回作用の $\rho$ は本稿に出てこない。**

### 7.2 D-1($\Gamma$ は $S_3$ ではない)との整合

k5_w6_construction §1.3 の D-1 は「$\theta,\tau$ を $B_3/PB_3\cong S_3$ の作用と読むな・$A$ 上の作用群は $S_4$・$\theta$ は第 3 座標を反転する」。
本稿は **$\Theta$ の $(3,3)$ 成分 $-1$ を最初から持ち込み**、§4.4 (c) の全射性証明で $\det=+1$ 符号付き置換行列 $\cong S_4$(位数 24)を使う。$\theta\tau$ の位数 4 は §4.5 の表で再現。
⟹ **D-1 と整合**。さらに §4.5 の補足で「A-0 は対の共役類を一意に決める」ことを証明したので、**D-2 の検出器としての A-0 の十分性が紙で裏づけられた**(従来は「位数 4 を assert する」という手続きだけだった)。

### 7.3 ★★★ **D-1 の残り穴を実証** — $\tau\leftrightarrow\tau^{-1}$ は既存 4 検査を全部素通りする

$\tau$ を $(n_1,n_2,n_3)\mapsto(n_2,n_3,n_1)$($=\tau^{-1}$)と取り違えて同じ手順を回すと:

| 検査 | 正しい規約 | **取り違え** | 検出? |
|---|---|---|---|
| **L-1** braid | PASS | **PASS** | ✗ |
| **L-2** $\rho(c)=1$ | PASS | **PASS** | ✗ |
| **L-3** $\lvert\langle\widehat\sigma_1,\widehat\sigma_2\rangle\rvert$ | 3000 | **3000** | ✗ |
| **A-0** $\mathrm{ord}(\theta\tau)$ | 4 | **4** | ✗ |
| ★ $\mathrm{Ad}(\widehat\sigma_1^{\,2})\vert_A$ | $\mathrm{diag}(1,-1,-1)$ | **$\mathrm{diag}(-1,1,-1)$** | ✔ |
| ★ $\mathrm{Ad}(\widehat\sigma_2^{\,2})\vert_A$ | $\mathrm{diag}(-1,1,-1)$ | **$\mathrm{diag}(1,-1,-1)$** | ✔ |

**⟹ 取り違えは $x$ と $y$ の役割をちょうど入れ替える。** `MakeGn` の $x=(r,s,s)$ は $\mathrm{diag}(1,-1,-1)$、$y=(sr,r,sr)$ は $\mathrm{diag}(-1,1,-1)$ を要求するので、**外部 anchor(既在の $x,y$)との突合が唯一の検出器**である。
機械実証: `scratchpad/bu_s35_d1_trap.py`(SHA-256 `c8d016c75b0d68ad139919b2d472d0221cfd3dd47eff2ae77716cc9fd2dfd828`)。

> ### ★ これは CV-13 の射程限定の実例である
> 規約台帳 CV-13 は「生成器と受理器が同じ誤った向き関数を共有すれば一様な鏡像は素通りする ⟹ **外部 anchor または独立 source-map route を必ず併置せよ**」と定める。
> **L-1/L-2/L-3 は完全に内部整合的であり、$\tau$ の向きを一様に鏡像しても全部通る。** 本節はその 5 例目である。⟹ **S3.5 の実装には `MakeGn(5)` の $x,y$ という外部 anchor の併置が CV-13 上**必須**である**(§8 F-2)。

> ### ⚠ GAP 実装での具体的な発火経路(**実装係へ**)
> `search/probe/w6_bu_s0/w6_bu_s0_driver.g` の Route 1 は
> `homS4toGL := GroupHomomorphismByImages(S4grp, GL(3,5), [theta,tau], [thetaA,tauA])` と
> `SemidirectProduct(S4grp, homS4toGL, GF(5)^3)` で $\widehat G_5$ を作る。
> GAP の行列群の自然作用は**行ベクトルへの右作用** $v\mapsto v\cdot M$ である。`tauA` の行作用は $(n_1,n_2,n_3)\mapsto(n_2,n_3,n_1)=\tau^{-1}$ であり、**正典 (4.8) の $\tau$ ではない**。
> ⟹ **その模型の中で $\widehat\delta$ に相当するのはラベル $(1\,4\,3)$($=\tau^2$)の側かもしれない。**
> ★ **当方は GAP を走らせていないので、これは「起こりうる」であって「起きている」ではない。** 実装係は**列挙の前に F-2 を必ず走らせ、失敗したら $\widehat\delta$ を逆元に取り替える**こと(判定は実行時に機械が行い、人が読み替えない)。
> ⚠ **既存 S0 cert(A-0〜A-13)への影響はない**: A-0 は抽象 $S_4$ 内の位数、A-1/A-2 は位数と abelian invariants、A-3/A-4 は加群・軌道の不変量で、いずれも $\tau\leftrightarrow\tau^{-1}$ の再ラベルで不変。**本稿は既存 cert を偽としない。**

### 7.4 ★★ 座標基底の食い違い(**新発見・§6 と §4 をつなぐとき必須**)

15 点モデルで実測した共役作用($A=\langle\mathrm{tr}(r,1),\mathrm{tr}(r,2),\mathrm{tr}(r,3)\rangle$ のブロック基底):

$$\mathrm{Ad}(\widehat\Delta)\vert_A=\begin{pmatrix}0&1&0\\1&0&0\\0&0&-1\end{pmatrix}=\Theta\ \ (\textbf{一致}),\qquad
\mathrm{Ad}(\widehat\delta)\vert_A=\begin{pmatrix}0&0&-1\\1&0&0\\0&-1&0\end{pmatrix}\ne T .$$

$d:=\mathrm{diag}(1,1,-1)$ と置くと $d\,\mathrm{Ad}(\widehat\delta)\vert_A\,d=T$ かつ $d\,\Theta\,d=\Theta$。

$$\boxed{\ \textbf{`MakeGn` のブロック座標と正典 (4.7)(4.8) の座標は }d=\mathrm{diag}(1,1,-1)\textbf{ だけずれている。}\ }$$

- $\Theta$ は $d$-共役で**不変**なので、**$\theta$ 側を見ているかぎりズレは見えない**。$\tau$ 側にだけ現れる。
- $f_1=(r^2,r^{-2},1)\leftrightarrow(1,-1,0)$ は第 3 座標が 0 なので**どちらの基底でも同じ**(偶然)。
- $\det d=-1$ ゆえ $d\notin S_4$($\det=+1$ 符号付き置換群)。しかし共役は $\det$ を保つので $S_4$ の**内部**自己同型を誘導し、対角線ラベルは $(1\,2)(3\,4)$ で読み替わる。§4.5 のラベル $\ell$ を
  $$\ell'(1)=[1{:}1{:}1],\ \ \ell'(2)=[1{:}1{:}{-}1],\ \ \ell'(3)=[{-}1{:}1{:}{-}1],\ \ \ell'(4)=[1{:}{-}1{:}{-}1]$$
  に取り替えると、15 点モデルでも $\widehat\Delta\mapsto(1\,2)$、$\widehat\delta\mapsto(1\,3\,4)$、$\widehat\sigma_1\mapsto(1\,2\,4\,3)$、$\widehat\sigma_2\mapsto(1\,4\,3\,2)$ が**そのまま**再現する(機械確認: `scratchpad/bu_s35_basis_labels.py`, SHA-256 `fcfb6058b025476b79a9fca9adbf8c7fb747718cd98e76747449ce8f622a7921`)。

⚠ **どちらの基底も「正しい」。** 禁止事項は**混用**である。S3.5 では $V$ 上の $\theta,\tau$ しか使わない($A$ の基底は現れない)ので実害は出にくいが、**$f_1$ や $\beta_\theta,\beta_\tau$ を $A$-座標で書く段(S6/S7)では効く**。⟹ 【BU-GAP-12】(§10)。

---

## 8. ★★★ fixture(**実装係がそのまま検査に使える形**)

すべて **fail-closed**。1 つでも落ちたら `PREREGISTRATION_FALSIFIED / INTEGRITY_STOP`(S-BU-1 逐語)。

### F-1 — 生成元と関係式(**L-1/L-2/L-3 の置換**)

| # | assert | 期待値 |
|---|---|---|
| F-1.1 | $\widehat\Delta:=\widehat\sigma_1\widehat\sigma_2\widehat\sigma_1$ の位数 | **2** |
| F-1.2 | $\widehat\delta:=\widehat\sigma_1\widehat\sigma_2$ の位数 | **3** |
| F-1.3 | $\widehat\sigma_1\widehat\sigma_2\widehat\sigma_1=\widehat\sigma_2\widehat\sigma_1\widehat\sigma_2$ | **true** |
| F-1.4 | $\widehat\Delta^2=1$($=\widehat c$) | **true** |
| F-1.5 | $\lvert\langle\widehat\sigma_1,\widehat\sigma_2\rangle\rvert$ | **3000** |
| F-1.6 | $\mathrm{ord}(\widehat\sigma_1)$, $\mathrm{ord}(\widehat\sigma_2)$ | **20, 20** |
| F-1.7 | $\mathrm{ord}(\widehat\sigma_1^{\,2})$, $\mathrm{ord}(\widehat\sigma_2^{\,2})$ | **10, 10** |
| F-1.8 | $\lvert\langle\widehat\sigma_1^{\,2},\widehat\sigma_2^{\,2}\rangle\rvert$($=\lvert G_5\rvert$) | **500** |

⚠ **F-1 だけでは D-1 を検出できない**(§7.3)。**F-2 を必ず併走させること。**

### F-2 — ★ 外部 anchor(**D-1 検出器・CV-13 の必須併置**)

| # | assert | 期待値 |
|---|---|---|
| **F-2.1** ★ | $\widehat\sigma_1^{\,2}=x$(`MakeGn(5).x` と**同一元**) | **true** |
| **F-2.2** ★ | $\widehat\sigma_2^{\,2}=y$(`MakeGn(5).y` と**同一元**) | **true** |
| **F-2.3** ★ | $\mathrm{Ad}(\widehat\sigma_1^{\,2})\vert_A$ の対角 | **$(1,-1,-1)$** |
| **F-2.4** ★ | $\mathrm{Ad}(\widehat\sigma_2^{\,2})\vert_A$ の対角 | **$(-1,1,-1)$** |
| **F-2.5** ★ | $\mathrm{Ad}(\widehat\Delta)\vert_A=\Theta$(§7.4 の基底注意つき) | **true** |
| **F-2.6** ★ | $\mathrm{Ad}(\widehat\delta)\vert_A$ が $T$(canon 基底)/ $d T d$(MakeGn 基底) | **true**(どちらの基底かを cert に明記) |

> ★ **F-2.6 が落ちたら $\widehat\delta$ を $\widehat\delta^{-1}$ に取り替えて再実行**(§7.3 の GAP 行ベクトル経路)。**取り替えたことを cert に記録する**(黙って直さない)。
> ★ **F-2.1/F-2.2 が両方落ち、かつ入れ替えると通る場合は D-1 の罠を踏んでいる**(§7.3 の表)。

### F-3 — S3.5 の 2 レーン照合(**系 EMB-LIN の受理試験**)

固定した $(V,[\varepsilon])$ に対し:

| # | assert | 期待値 |
|---|---|---|
| **F-3.1** | lane A(線型): $\#\{a:N_\theta a=-\varepsilon_\Delta\}\times\#\{b:N_\tau b=-\varepsilon_\delta\}$ | $n_A$ |
| **F-3.2** | lane B(悉皆): $\lvert V\rvert^2$ 対の $(\rho(\sigma_1),\rho(\sigma_2))$ を L-1∧L-2 で篩った個数 | $n_B$ |
| **F-3.3** ★ | $n_A=n_B$ | **true**(不一致なら `TWO_LANE_MISMATCH / STOP`) |
| **F-3.4** | 既知較正: $V=\mathbf F_2^3$($S_3$ 置換加群 = $K^{(20)}$ の加群)・分裂類 | $n_A=n_B=\mathbf{16}$($=4\times4$) |
| **F-3.5** | negative: $\varepsilon_\Delta\notin\operatorname{im}N_\theta$ を人工的に作る | $n_A=n_B=\mathbf 0$(**「解なし」を報告できること**) |

⚠ **F-3.5(陰性 fixture)を欠くと F-3 の全 PASS は情報量ゼロ**(k5_w6_construction §4.3 DF-W6-1 と同じ理由)。

### F-4(参考) — 既存 A-0 との接続

| # | assert | 期待値 |
|---|---|---|
| F-4.1 | $S_4$ 内で $\mathrm{ord}(\theta\tau)$ | **4**(既存 A-0 と同値) |
| F-4.2 | $\widehat\sigma_1,\widehat\sigma_2$ の $S_4$-像の位数 | **4, 4**(**2 でも 3 でもない**) |
| F-4.3 | $\widehat\sigma_1^{\,2},\widehat\sigma_2^{\,2}$ の $S_4$-像が $V_4=O_2(S_4)$ に入る | **true**(ラベル $\ell$ の下で $(1\,4)(2\,3)$ と $(1\,3)(2\,4)$・**互いに異なること**も assert) |
| F-4.4 | ラベル $\ell$(§4.5)の下で $\widehat\sigma_1\mapsto(1\,2\,4\,3)$、$\widehat\sigma_2\mapsto(1\,4\,3\,2)$ | **true** |

---

## 9. 検算の申告(**格付けを誤らせないため**)

| # | スクリプト | SHA-256 | 内容 | 格 |
|---|---|---|---|---|
| 1 | `scratchpad/bu_s35_embed_check.py` | `a1f8b0f167b87d57e472b0076ee073cb6e0bac899ec18609156c077a9935175d` | §4(明示式・braid・全射性・位数)・§4.5(ラベル)・§5.1($H^1$・500/125 分割)・§6 | python 単系統 |
| 2 | `scratchpad/bu_s35_d1_trap.py` | `c8d016c75b0d68ad139919b2d472d0221cfd3dd47eff2ae77716cc9fd2dfd828` | §7.3(D-1 の罠が L-1/L-2/L-3/A-0 を素通りすること) | python 単系統 |
| 3 | `scratchpad/bu_s35_linearize.py` | `c6590582da6bbff34387f9b51a1d52e17c334d5bb7ccf79cbdf1ab6837bf190b` | §3.3(EMB-LIN の 2 レーン照合・3 例) | python 単系統 |
| 4 | `scratchpad/bu_s35_perm_uniqueness.py` | `eb2f3ce34e8ef30494ace894758e5ef6341635086a1c69ae6485cd6f2be50838` | §6.3($F_{20}\wr S_3$ = 48,000 元の悉皆・1 対のみ) | python 単系統 |
| 5 | `scratchpad/bu_s35_basis_labels.py` | `fcfb6058b025476b79a9fca9adbf8c7fb747718cd98e76747449ce8f622a7921` | §7.4(基底ズレ $d$ とラベル $\ell'$) | python 単系統 |

$$\boxed{\ \textbf{全部 python 単系統。}\ \texttt{cross-checked}\ \textbf{ではない。}\ \texttt{verified}\ \textbf{でもない(Lean 不使用)。}\ }$$

GAP による第 2 系統(= 既存 `MakeGn(5)` との実物突合 = F-2)は**未実施**。**F-2 が通るまで、本稿の §6 の置換値を「$\widehat G_5$ の正典的表現」と呼んではならない。** 現在の格は **paper-proof candidate + single-lane machine check**。

---

## 10. 【GAP】と申し送り

### 10.1 【GAP】

| 札 | 内容 | 状態 |
|---|---|---|
| **【BU-GAP-10】** ★新 | **$q(c)=1$ が v2/v3/v4 のどこにも書かれていない。** 定義 MARKED は $\rho(c)=1$ と $\pi\circ\rho=q$ を同時に課すので、$q(c)=1$ は**定義が空でないための必要条件**。本稿 §2 定理 EMB-C が補題 GAMMA (b) から導いた | ★ **本稿で閉じた(candidate)**。FREEZE-1 の本文に 1 行入れる価値あり(§10.2-1) |
| **【BU-GAP-11】** ★新 | EMB-LIN の $(\varepsilon_\Delta,\varepsilon_\delta)$ と W6-OBS の $(\beta_\theta,\beta_\tau)$ は**別の量**だが、同じ $N_\theta,N_\tau$ を使う。実装で共有する場合に**取り違えの余地がある** | **UNKNOWN**(規約事項・cert の欄名を分けることで回避可能) |
| **【BU-GAP-12】** ★新 | **$A$ の座標基底が 2 系統ある**(§7.4)。S3.5 には効かないが **S6/S7 で $f_1$・$\beta$ を $A$-座標で書く段で効く** | **UNKNOWN**(規約事項・宣言すれば閉じる) |
| **【BU-GAP-13】** ★新 | 正典 2405.11725 (4.7)(4.8) を**原文 PDF で照合していない**(既在ノート経由の孫引き)。第 3 座標の符号は本稿の全体重を支える | **UNKNOWN** — ★ **司令塔に原文 1 ページの照合を要請**(§10.2-4) |
| **【BU-GAP-8】**(既在) | isolated 性は marked lift の段で判定できない | 不変(本稿は触れない) |

### 10.2 申し送り

1. ★★★ **FREEZE-1 への追記提案(1 行)**: 定義 MARKED の直後に「$q(c)=1$(定理 EMB-C)ゆえ $\rho$ は $B_3/\langle c\rangle\cong C_2\ast C_3$ を経由する」を入れる。**凍結内容の変更ではなく、既に暗黙に使われていた事実の明記**である。採否は司令塔 → Sol。
2. ★★★ **S3.5 の検査項目の差し替え提案**: L-1(braid)を**削除**し、L-2 を「$U^2=1\wedge W^3=1$」に置換(定理 EMB-BRAID で同値)。これは **FREEZE-3 の段の順序を変えない**(S3.5 の中身だけ)。**実装コストは下がり、D-1 の露出面も 1 つ減る**。⚠ ただし**同値性の主張は本稿の paper-proof candidate であり Sol 未監査**なので、**当面は L-1 も併走させて両者一致を assert する**(移行期の二系統)ことを推奨。
3. ★★ **F-2 の実施を S3.5 発火の前件にすること**を提案。CV-13 の外部 anchor 併置義務の直接の帰結であり、§7.3 の罠は **F-2 なしでは絶対に捕まらない**。
4. ★ **【文献要請 BU-S35-1】**: 正典 **arXiv 2405.11725 の (4.7)(4.8) を含む 1 ページ**の原文画像照合を要請する。**困難の記述**: 第 3 座標の符号 1 個(D-1)と $\tau$ の向き 1 個(§7.3)が本稿の全結論を決めるが、当方は既在ノート経由の孫引きしか持たない。**欲しい結果の型**: (4.7)(4.8) の**逐語**と、その直前の $A$ の座標の定義($(r^{2n_1},r^{2n_2},r^{2n_3})$ の 3 成分が**どの部分群・どの順序**を指すか)。**これは新規文献の要請ではなく、既に持っている正典の 1 ページの照合である。**
5. ★ **委嘱②(「$G_5$ 水準への還元」)は不要と判断した**。理由: S3.5 は $\widehat G_5$ 上の lift を数える段であり、$G_5$($=\ker$ の $PB_3$ 側)に落とすと $\Delta,\delta$ が消えて marked 条件が表現できない。代わりに **§3 の $C_2\ast C_3$ 還元が「安い機構」の役を果たす**(総当り → 2 本の線型系)。**この判断は当方の裁量であり、司令塔が②を意図していたなら差し戻されたい。**
6. ⚠ **本稿は 1 行も走らせていない**(GAP 起動ゼロ)。§6 の置換値は python で構成・検証したものであって、**GAP 内で `MakeGn(5)` と突合してはいない**(= F-2 未実施)。

---

## 付録 A. 実装係への受け渡し(**最短経路**)

1. **$\widehat G_5$ を作る**。二択:
   - **(A) 15 点置換**(推奨・`MakeGn` と同じ土俵): §6.2 の 2 元をそのまま `s1 := (1,4,2,5,3)(6,11)(7,12,10,15)(8,13,9,14);;`、`s2 := (1,12,2,11)(3,15,5,13)(4,14)(6,9,7,10,8);;` と置き、`Ghat5 := Group(s1,s2);;`。**F-2.1/F-2.2 が即座に走る**(`MakeGn(5).x`, `.y` と比較するだけ)。
   - **(B) 半直積**(既存 S0 driver 流用): §4 の $\widehat\Delta,\widehat\delta$ を作り $\widehat\sigma_1=\widehat\delta^{-1}\widehat\Delta$、$\widehat\sigma_2=\widehat\Delta^{-1}\widehat\delta^2$。**必ず F-2.6 を先に走らせ、落ちたら $\widehat\delta\to\widehat\delta^{-1}$**(§7.3)。
2. **S3.5 を回す**。$\widehat P$ 上で $U_0\in\pi^{-1}(\widehat\Delta)$、$W_0\in\pi^{-1}(\widehat\delta)$ を 1 つずつ取り、$\varepsilon_\Delta=U_0^2$、$\varepsilon_\delta=W_0^3$ を計算。$N_\theta a=-\varepsilon_\Delta$、$N_\tau b=-\varepsilon_\delta$ を $\mathbf F_p$ 上で解く(系 EMB-LIN)。各解対 $(a,b)$ に対し
   $$\rho(\sigma_1)=(W_0b)^{-1}(U_0a),\qquad \rho(\sigma_2)=(U_0a)^{-1}(W_0b)^2 .$$
3. **L-3(全射性)だけが残る非線型条件**: $\langle\rho(\sigma_1),\rho(\sigma_2)\rangle=\widehat P$ を確認。
4. **cert に必ず書く欄**: ①使った基底(canon / MakeGn・§7.4)②$\widehat\delta$ を逆元に取り替えたか③F-2 の全結果④lane A/lane B の個数(F-3)。

## 付録 B. 一目でわかる対応表(**D-1 早見**)

| $B_3$ の元 | $\widehat G_5$ での位数 | $S_4=\widehat G_5/A$ での像 | 位数 | $V_4$ に入るか |
|---|---|---|---|---|
| $\Delta=\sigma_1\sigma_2\sigma_1$ | **2** | $\theta=(1\,2)$ | 2 | ✗ |
| $\delta=\sigma_1\sigma_2$ | **3** | $\tau=(1\,3\,4)$ | 3 | ✗ |
| $c=\Delta^2=\delta^3$ | **1** | $\mathrm{id}$ | 1 | ✓ |
| $\sigma_1$ | **20** | $(1\,2\,4\,3)$ | **4** | ✗ |
| $\sigma_2$ | **20** | $(1\,4\,3\,2)$ | **4** | ✗ |
| $x=\sigma_1^2$ | **10** | $(1\,4)(2\,3)$ | 2 | **✓** |
| $y=\sigma_2^2$ | **10** | $(1\,3)(2\,4)$ | 2 | **✓** |

> ★ **この表の第 4 列だけ覚えればよい**: $\theta,\tau$ は $2,3$;$\sigma_1,\sigma_2$ は $\mathbf 4$;$x,y$ は $2$。
> **$\sigma_i$ の $S_4$-像の位数が 2 か 3 になったら、それは $\Delta$ か $\delta$ と取り違えている。**
