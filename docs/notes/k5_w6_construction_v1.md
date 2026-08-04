# W-6(検出力ある細分)の建設 — 設計ノート v1

**状態札: `design / candidate / 実測ゼロ / Sol 未監査 / 発火未認可`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-04
- 委嘱: 司令塔(K⁽⁵⁾ genuine 戦役 W-6 建設の設計委嘱)
- 入力正本: `docs/notes/k5_genuine_campaign_v1.md`(§2.3 命題 K5-BIT・§3 篩・§4 予言・§6 干渉表・§7.4【K5-GAP】)/ 同 addendum A(`k5_genuine_campaign_v1_addendum_a_k5mod.md`、**§A.13 が current erratum**)/ `docs/notes/roof2_cv9_freeze_v1.md`(命題 ENT-CRIT・追記 H)/ `docs/notes/no_ent3_v1.md` / `docs/week3-狩場計画_v2.md` §2.1(**定理 H8・系 H8′**)/ `docs/notes/hs_prop7_translation_v1.md`(§2 検出力事前見積りの様式・§9 **S-7′/S-8**)/ 正典 **2405.11725 (4.7)(4.8)**・2401.06870。
- **外部文献ゼロ。**【文献要請】は §7.5。

> ## 非接触の申告(**campaign §6 が正本・スコープ照合は司令塔**)
> - **$\mathrm{Im}\,R_{N,K^{(5)}}$ を一度も測っていない。** 本稿は紙 + $\mathbb F_p$ 線型代数の検算のみ。
> - **K⁽⁵⁾ の実測に触れない**(委嘱指定)。使う $n=5$ の情報は $G_5$ の**構造**($\lvert G_5\rvert=500$・$A\cong C_5^3$・$G_5^{\rm ab}\cong C_2^2$)と、正典 (4.7)(4.8) の $\theta,\tau$ **作用式**だけである。shadow の値・証明書は読んでいない。
> - **封印 3 量に非接触**: $\hat c_\mu$ / PSL 窓の構造量 / ε bits。**曲線・dessin・Kummer・$u$ 値も一切使わない。**
> - ⚠ **記号衝突を先に名指し**(§6.1): 本稿の $\varepsilon$(符号指標)は封印語彙の「ε bits」ではない。本稿の $\Gamma$ は $S_3$ **ではない**(§1.3)。

---

## 0. 判定(先に 7 行)

1. ★★ **【K5-GAP-1】は閉じた(候補)。** $\widetilde m=0$ における hexagon の 2 本のノルム方程式は、核 $V$ 上の**有限次元 $\mathbb F_p$-線型写像 $\psi_V$ の余核**という完全に計算可能な障害に落ちる(**定理 W6-OBS**・§2.3)。捻れノルムの余核は「型」ではなく**明示式**になった。
2. ★★ **委嘱が挙げた 2 候補は両方とも死んでいる。**
   - **elementary-5 側 = $\rho$ / $\rho\otimes\varepsilon$(次元 3・$62{,}500$)**: 両型とも $\operatorname{coker}\psi_V=0$ ⟹ $\phi_1$ は**必ず持ち上がる** ⟹ $d_N=5$ ⟹ **検出力ゼロ**(定理 W6-NULL5・§2.5)。**構成しても無駄弾**。
   - **$p=3$ 側 = WARN-13500($S_4$ 標準 3 次元 $\mathbb F_3$-加群)**: 同じく $\operatorname{coker}\psi_V=0$ ⟹ **検出力ゼロ**(§3.2)。**実現性を調べる前に落ちる。**
3. ★★★ **さらに強く: 初等アーベル 5 核 class は「全滅」である**(次元によらない・定理 W6-NULL5)。⟹ **addendum §A.7 が下界 $62{,}500$ を守った当の class は、そのまま検出力ゼロの class でもある。** K5-MOD-v2 の数値結論と本稿は矛盾しない — **下界は生きたまま、その上の窓が全部空だと分かった**のである。
4. ★ **なぜそうなるかの機構**: $\theta$ は位数 2、$\tau$ は位数 3。**係数の標数が 6 と互いに素なら両ノルムが射影の定数倍に退化し、障害は $V$ の $\Gamma$-余不変部分に潰れる**(系 W6-DUAL)。そこでは K5-MOD-v2 (D) が類の消滅を与える(補題 CLASS-TRIV)。⟹ **検出力の在処は標数 2 と標数 3 に限られる。**
5. ★★ **⟹ 優先度は反転する。**【K5-GAP-5】(**2-primary 核**・既に UNKNOWN で起票済)が**第一標的**、次が $p=3$ の**非自由 $\tau$-構造**をもつ核。**【K5-GAP-6】(i)(WARN-13500)は本稿で閉じる(否定側)。**
6. ★ **較正が既に在庫にある**: $W\text{-}3=K^{(20)}=K^{(5)}\cap K^{(4)}$ は 2-primary 核をもち、$\operatorname{coker}\psi_V\ne0$ でありながら正典 Thm 4.4($4\mid q$ 分岐)で $d=5$ が**証明済**。⟹ **「障害群は非零だが類は消える」の既製 control**(§4.3 DF-W6-2)。**新しい実測を要しない。**
7. ⚠ **買わないもの**: 本稿は $d_{\rm gen}(5)$ について何も言わない。**言えるのは「この族では検出力がゼロ」という上界側だけ**である(campaign §7.2 の非対称は不変)。

> ### ★ 委嘱の前提が動いた件(司令塔へ・§7.6-1)
> 委嘱は「①どちらが安いか・両方やるかの優先度提案」を求めたが、**答は「どちらもやらない」**である。**代わりに 2-primary 標的の起票を提案する。** これは委嘱スコープの縮小ではなく**標的の差し替え**なので、**司令塔の裁定を仰ぐ**(速達送付済)。

---

## 1. 設定と記号(**再定義しない・出所つき**)

### 1.1 対象

campaign §1.3 のまま。$K^{(5)}=\ker\psi_5$、$G_5=PB_3/K^{(5)}$($\lvert G_5\rvert=500$)、$A:=[G_5,G_5]\cong C_5^3$、$Q:=G_5/A\cong C_2^2$、$\widehat G_5:=B_3/K^{(5)}$($\lvert\widehat G_5\rvert=3000$)。
$T=\mathrm{GT}(K^{(5)})$($\lvert T\rvert=40$)、$\mathfrak F_0=\ker\widetilde\chi\cong C_5$、生成元 $\phi_1=[0,f_1]$、$f_1=(r^2,r^{-2},1)\in A$。

### 1.2 測る量(**変更しない**)

$N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、isolated。$d_N=\lvert\mathrm{Im}\,R_{N,K^{(5)}}\cap\mathfrak F_0\rvert\in\{1,5\}$。
**命題 K5-BIT**(campaign §2.3・**便 100 で Sol PASS**): $d_N=5\iff\phi_1\in\mathrm{Im}$、かつ $\widetilde m=0$ の項では系は

$$\textbf{(N}_\theta\textbf{)}\ \ \widetilde f\,\theta(\widetilde f)=1,\qquad
\textbf{(N}_\tau\textbf{)}\ \ \tau^2(\widetilde f)\,\tau(\widetilde f)\,\widetilde f=1,\qquad
\textbf{(SURJ)}\ \ \langle\bar x,\widetilde f^{-1}\bar y\widetilde f\rangle=P_N$$

($P_N:=F_2/N_{F_2}$、$\widetilde f\in[P_N,P_N]$、$\widetilde f\bmod K^{(5)}_{F_2}=f_1$)。

> ### ★ 論理の向きを先に固定する(**本稿全体の使い方**)
> $\widetilde m=0$ は $\mathcal X_N$ の元である($2\widetilde m+1=1$ ゆえ charming 条件 $\gcd(1,N_{\rm ord})=1$ は恒真)。ゆえに
> $$\boxed{\ \textbf{(N}_\theta\textbf{)(N}_\tau\textbf{)(SURJ) が }\widetilde m=0\textbf{ で可解}\ \Longrightarrow\ \phi_1\in\mathrm{Im}\ \Longrightarrow\ d_N=5\ (\textbf{検出力ゼロ})\ }$$
> **逆は言えない。** $\widetilde m=0$ で不可解でも、$\widetilde m\in\mathcal X_N$、$\widetilde m\equiv0\ (\mathrm{mod}\ 10)$ の**他の項**が残る(campaign §4.3 の T1 走査候補数の一般式)。
> ⟹ **本稿の主結果はすべて「検出力ゼロ」の側**であり、**「検出力がある」を主張したことは一度もない**。§3.3 の生存表は「**ここでしか有り得ない**」という**必要条件**の表である。

### 1.3 ★★ 対称群の正体 — $\Gamma=\langle\theta,\tau\rangle$ は $S_3$ ではない

$\theta,\tau\in\mathrm{Aut}(F_2)$($\theta:x\mapsto y,y\mapsto x$;$\tau:x\mapsto y\mapsto z\mapsto x$)。$\theta^2=\tau^3=\mathrm{id}$。正典 2405 の明示式:

$$\textbf{(4.7)}\quad\theta(r^{2n_1},r^{2n_2},r^{2n_3})=(r^{2n_2},r^{2n_1},r^{-2n_3}),\qquad
\textbf{(4.8)}\quad\tau(r^{2n_1},r^{2n_2},r^{2n_3})=(r^{2n_3},r^{2n_1},r^{2n_2}).$$

指数座標 $(n_1,n_2,n_3)$ の行列で

$$\theta=\begin{pmatrix}0&1&0\\1&0&0\\0&0&-1\end{pmatrix},\qquad
\tau=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix},\qquad
(\theta\tau)^2=\mathrm{diag}(1,-1,-1)\ne I,\ \ (\theta\tau)^4=I .$$

> ### ★ 補題 GAMMA(**本稿の第 1 の設計成果 — 誤りやすい一点**)
> **(a)** $A$ 上で $(\theta\tau)$ は**位数 4** である。ゆえに $\langle\theta,\tau\rangle$ は $S_3$ **ではない**。
> **(b)** $\langle\theta\vert_A,\tau\vert_A\rangle$ は $\det=+1$ の符号付き置換行列全体($\cong S_4$、位数 **24**)であり、これは $\widehat G_5/A\cong S_4$(addendum §A.7 (E))の $A$ への忠実な作用に一致する。とくに $C_{\widehat G_5}(A)=A$。
> **(c)** $\mathbb F_5[S_4]$-加群として $A\cong\mathrm{std}_3\otimes\mathrm{sgn}$(指標で判定: $\chi(\theta)=-1$、$\chi(\tau)=0$、$\chi(\theta\tau)=+1$)。
> **(d)** 抽象群としては $\Gamma:=\langle\theta,\tau\rangle\subseteq\mathrm{Aut}(F_2)$ は $B_3$ の $\mathrm{Aut}(F_2)$ への像であり、$\theta=\mathrm{Ad}(\Delta),\tau=\mathrm{Ad}(\delta)$、$\langle\Delta,\delta\rangle=B_3$。ゆえに **$\Gamma\supseteq\mathrm{Inn}(F_2)$**($=PB_3$ の像)であり、$\Gamma$ は $C_2*C_3\cong PSL_2(\mathbb Z)$ の商である。

**証明.** (a) 上の行列計算(§8 検算 A で $p=3,5,7,11$ に対し機械確認)。(b) $\det\theta=\det\tau=+1$;生成される群を $\mathbb F_5$ 上で悉皆列挙して位数 24(検算 A)。$\lvert\widehat G_5/A\rvert=3000/125=24$ と一致し、$A$ 可換ゆえ作用は $\widehat G_5/C(A)$ を経由するので $C(A)=A$。(c) 指標値を $S_4$ の既約指標表と照合($\mathrm{std}_3$ では $\chi(\text{転置})=1$)。(d) $\Delta=\sigma_1\sigma_2\sigma_1$、$\delta=\sigma_1\sigma_2$、$\Delta^{-1}\delta^2=\sigma_2$ ⟹ $\langle\Delta,\delta\rangle=B_3$。$\Delta^2=c$ は中心ゆえ $F_2=PB_3/\langle c\rangle$ 上 $\theta^2=1$。∎

> ⚠ **危険箇所 D-1(§6.2)**: 「$\theta,\tau$ は $B_3/PB_3\cong S_3$ の作用」という**言い方は本稿の文脈では誤解を招く**。$S_3$ は $\widehat G_5/G_5$ の話であって、**$A$ 上の作用群は $S_4$**($G_5$ の内部作用ぶんだけ大きい)。campaign §3.5 (3) と addendum (S4) の記述は「3 座標を置換する」までは正しいが、**$\theta$ は第 3 座標を反転する**(4.7)ので置換だけではない。**この 1 個の符号が本稿の全結論を決める。**

---

## 2. 【K5-GAP-1】の機構 — 障害の明示式

### 2.1 還元(設計仮説 D-1 の正確化)

$V:=K^{(5)}_{F_2}/N_{F_2}\ (\trianglelefteq P_N)$、$A_N:=[P_N,P_N]$。次を仮定する(**すべて §2.6 で会計する**):

| 前件 | 内容 |
|---|---|
| **(V-ab)** | $V$ はアーベル |
| **(V-der)** | $V\subseteq A_N$ |
| **(V-cen)** | $V$ は $A_N$ の中心に入る(**または** §2.2 の捻れ版で読み替える) |

$\widetilde f_0\in A_N$ を $f_1$ の任意の持上げとし、$\widetilde f=\widetilde f_0\,b$($b\in V$)と書く。$f_1$ は level 5 で (N$_\theta$)(N$_\tau$) を満たすから

$$\beta_\theta:=\widetilde f_0\,\theta(\widetilde f_0)\in V,\qquad
\beta_\tau:=\tau^2(\widetilde f_0)\tau(\widetilde f_0)\widetilde f_0\in V .$$

(V-cen) の下で (N$_\theta$)(N$_\tau$) は $V$ 上の**アフィン線型方程式系**に退化する:

$$\boxed{\ N_\theta(b):=b+\theta b=-\beta_\theta,\qquad N_\tau(b):=b+\tau b+\tau^2b=-\beta_\tau\ }\qquad(V\ \text{を加法的に書く})$$

**制約**: $\theta\beta_\theta=\beta_\theta$、$\tau\beta_\tau=\beta_\tau$(直接計算)。ゆえに $(\beta_\theta,\beta_\tau)\in V^\theta\oplus V^\tau$。
$\widetilde f_0$ の取り替え $\widetilde f_0\mapsto\widetilde f_0b'$ は $(\beta_\theta,\beta_\tau)\mapsto(\beta_\theta+N_\theta b',\beta_\tau+N_\tau b')$ を与えるので、

$$\psi_V:\ V\longrightarrow V^\theta\oplus V^\tau,\qquad b\mapsto(N_\theta b,\ N_\tau b)$$

に対し **$[(-\beta_\theta,-\beta_\tau)]\in\operatorname{coker}\psi_V$ は $\widetilde f_0$ の選び方によらない**。

$$\boxed{\ \textbf{(N}_\theta\textbf{)(N}_\tau\textbf{) が }\widetilde m=0\textbf{ で可解}\iff[(-\beta_\theta,-\beta_\tau)]=0\ \text{in}\ \operatorname{coker}\psi_V\ }$$

> ★ これが campaign §3.6 **設計仮説 D-1** の正確化である。D-1 が「型の記述」に留めた部分(「$\beta$ が $S_3$-捻れノルム写像の像に入らない」)を、**障害群を明示した上で有限線型代数に落とした**。

### 2.2 補題 TWIST(**非可換下位項の処理** —【K5-GAP-1】の第 2 の穴)

> ### 補題 TWIST(candidate)
> (V-ab)(V-der) の下で (V-cen) を落とす。$P_N$ の $V$ への共役作用を $\rho:P_N\to\mathrm{Aut}(V)$(自明に $V\subseteq\ker\rho$)とし、
> $$\theta_\ast:=\rho\bigl(\theta(\widetilde f_0)\bigr)\circ\theta,\qquad
> \tau_\ast:=\rho\bigl(\tau(\widetilde f_0)\,\tau^2(\widetilde f_0)\bigr)\circ\tau\ \ (\text{以下同様の右移動つき})$$
> と置くと、(N$_\theta$)(N$_\tau$) は $\theta_\ast,\tau_\ast$ に対する同型の式に書き換わる。$\theta_\ast^2=\mathrm{id}_V$ かつ $\tau_\ast^3=\mathrm{id}_V$ が成り立つならば、§2.3 以下の全結論は $(\theta,\tau)$ を $(\theta_\ast,\tau_\ast)$ に置換してそのまま成立する。
> **⟹ 非可換下位項は「$V$ の $\Gamma$-加群構造を $\widetilde f_0$ で捻る」ことに尽き、障害群の形は変わらない。**

**証明の骨格.** $\widetilde f_0b\,\theta(\widetilde f_0b)=\widetilde f_0\theta(\widetilde f_0)\cdot\bigl(\theta(\widetilde f_0)^{-1}b\,\theta(\widetilde f_0)\bigr)\cdot\theta(b)$ を展開するだけ($V$ 可換ゆえ順序は自由)。∎
> ⚠ **【K5-GAP-W1】(新設)**: $\theta_\ast^2=\mathrm{id}$・$\tau_\ast^3=\mathrm{id}$ の**検証は未了**。これは「$f_1$ が level 5 で解である」ことのコサイクル的帰結であるはずだが、**当方は書き下していない**。$\rho$ が $f_1$ の像を通してしか効かないこと(level 5 の関係式)を使う 3〜5 行だと見積もる。**Sol 監査点 W-1(最優先)**。
> **本稿の主結果への影響**: §2.5 の定理 W6-NULL5 は **$V$ が $A_N$ の中心に入る場合**((V-cen))には無条件に成立する。$K^{(25)}$ 型はこれを満たす($V=5A_{25}$ は $A_{25}$ 内で中心)。⟹ **【K5-GAP-W1】は射程の一般化にのみ効き、$62{,}500$ 分岐の否定判定には効かない。**

### 2.3 ★★ 定理 W6-OBS(**障害群の明示式** — 本稿の主定理)

> ### 定理 W6-OBS(candidate)
> $V$ を $\mathbb F_p$ 上の有限次元 $\langle\theta,\tau\rangle$-加群とし、$\psi_V=(N_\theta,N_\tau):V\to V^\theta\oplus V^\tau$ とする。このとき
> **(A)(master formula・常に成立)**
> $$\dim\operatorname{coker}\psi_V=\dim V^\theta+\dim V^\tau-\dim V+\dim\bigl(\ker N_\theta\cap\ker N_\tau\bigr).$$
> **(B)($p\ne2$)** $\ \dim\operatorname{coker}\psi_V=\dim V^\tau-\dim N_\tau(\ker N_\theta)$.
> **(B′)($p\ne3$)** $\ \dim\operatorname{coker}\psi_V=\dim V^\theta-\dim N_\theta(\ker N_\tau)$.
> **(C)($p\nmid6$)** $\ \operatorname{coker}\psi_V\ \cong\ \bigl((V^\ast)^\Gamma\bigr)^\ast$、すなわち**障害群は $V$ の $\Gamma$-余不変部分**($\Gamma=\langle\theta,\tau\rangle$)。とくに
> $$\operatorname{coker}\psi_V\ne0\iff V\ \text{が自明な }\Gamma\text{-商をもつ}.$$

**証明.**
**(A)** $N_\theta(V)\subseteq V^\theta$、$N_\tau(V)\subseteq V^\tau$(直接)。$\dim\operatorname{im}\psi_V=\dim V-\dim\ker\psi_V$、$\ker\psi_V=\ker N_\theta\cap\ker N_\tau$。
**(B)** $p\ne2$ ゆえ $N_\theta=2e_\theta$($e_\theta=(1+\theta)/2$ は $V^\theta$ への射影)で $\ker N_\theta=V^{\theta=-1}$、$\dim\ker N_\theta=\dim V-\dim V^\theta$。(A) に代入し $\dim(\ker N_\theta\cap\ker N_\tau)=\dim\ker N_\theta-\dim N_\tau(\ker N_\theta)$ を使う。
**(B′)** 対称(3 が可逆ゆえ $N_\tau=3e_\tau$)。
**(C)** $p\nmid6$ ゆえ $\ker N_\theta=(1-e_\theta)V$、$\ker N_\tau=(1-e_\tau)V$。双対で
$$(\ker N_\theta)^\perp=\{\lambda\in V^\ast:\lambda\circ(1-e_\theta)=0\}=(V^\ast)^\theta,\qquad(\ker N_\tau)^\perp=(V^\ast)^\tau .$$
(A) より $\operatorname{coker}\psi_V\cong V/(\ker N_\theta+\ker N_\tau)$(次元計算 — $\dim V^\theta+\dim V^\tau-\dim\operatorname{im}\psi=\dim V-\dim(\ker N_\theta+\ker N_\tau)$)。その双対は $(\ker N_\theta)^\perp\cap(\ker N_\tau)^\perp=(V^\ast)^\theta\cap(V^\ast)^\tau=(V^\ast)^\Gamma$。∎

**機械側**(§8 検算 B/C・**FAILS = 0**): 28 個のモジュール(4 標数 × 7 型)で (A)(B)(B′) の 3 式が一致。(C) は $p=5,7$ の全 case で $\dim\operatorname{coker}=\dim(V^\ast)^\Gamma$ を照合。**$p=2$ で (B) が破れること**(6 件)も、前件を明示した上で機械が捕まえた(→ 前件は本質的)。

### 2.4 補題 CLASS-TRIV(**自明 $\Gamma$-商の上では類が消える**)

> ### 補題 CLASS-TRIV(candidate)
> (V-ab)(V-der)(V-cen) と $p\nmid6$ を仮定する。$\bar V:=V_\Gamma$($\Gamma$-余不変)、$\bar N\ (N\subseteq\bar N\subseteq K^{(5)})$ を $K^{(5)}_{F_2}/\bar N_{F_2}=\bar V$ となる部分群とする。このとき
> **(a)** $\bar N\trianglelefteq B_3$(核が $\Gamma$-安定 ⟹ $B_3$-安定;補題 GAMMA (d));
> **(b)** $\Gamma$ が $\bar V$ に自明に作用 ⟹ **$\widehat G_5$ が $\bar V$ に自明に作用**(補題 GAMMA (d) で $\Gamma\supseteq\mathrm{Inn}$);
> **(c)** ⟹ **K5-MOD-v2 (D)** により拡大 $1\to\bar V\to PB_3/\bar N\to G_5\to1$ は分裂し、補群 $C$ は一意・正規・**$B_3$-安定**;
> **(d)** $C\xrightarrow{\sim}G_5$ は $B_3$-同変ゆえ $f_1$ の $C$ 内の像 $\widetilde f_C$ は $\widetilde m=0$ の (N$_\theta$)(N$_\tau$) を**満たす** ⟹ 類は $\operatorname{coker}\psi_{\bar V}$ で消える;
> **(e)** $\operatorname{coker}\psi_V\xrightarrow{\ \sim\ }\operatorname{coker}\psi_{\bar V}$(定理 W6-OBS (C) と $(V^\ast)^\Gamma=(\bar V^\ast)^\Gamma$)⟹ **$\operatorname{coker}\psi_V$ における類も消える**。
> $$\Longrightarrow\ \boxed{\ p\nmid6\ \text{の核では}\ \textbf{(N}_\theta\textbf{)(N}_\tau\textbf{) は常に可解}\ }$$

> ⚠ **【K5-GAP-W2】(新設)**: (d) の「$C\cong G_5$ が $B_3$-同変」から「$\widetilde f_C\in[P_N,P_N]$ かつ $F_2$ 水準の (N$_\theta$)(N$_\tau$) を満たす」への渡り(**$PB_3/\bar N$ 水準と $F_2/\bar N_{F_2}$ 水準の突合**・$c\in N$ の要否)を当方は 1 行で済ませている。**Sol 監査点 W-2**。campaign §5.0 の $\theta/\tau$ 評価水準の注意(**$c\in N$ 依存**)と同じ論点である。

### 2.5 ★★★ 定理 W6-NULL5(**初等アーベル 5 核 class は全滅**)

> ### 定理 W6-NULL5(candidate)
> $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$V=K^{(5)}_{F_2}/N_{F_2}$ が**初等アーベル 5 群**で (V-ab)(V-der)(V-cen) を満たすとする。このとき $\widetilde m=0$ の (N$_\theta$)(N$_\tau$) は可解であり、さらに (SURJ) が自動(§4.2 補題 SURJ-W6)ならば
> $$\phi_1\in\mathrm{Im}\,R_{N,K^{(5)}},\qquad d_N=5,\qquad\textbf{検出力ゼロ}.$$
> **とくに次元によらない** — addendum §A.7 (E) の**最小次元 3 の両型 $\rho,\rho\otimes\varepsilon$ を含む**。

**証明.** $p=5\nmid6$ ゆえ定理 W6-OBS (C) と補題 CLASS-TRIV。∎

**次元 3 の直接確認**(紙 + 機械・§8 検算 D):

| 型 | $\dim V^\theta$ | $\dim V^\tau$ | $\dim\ker N_\theta$ | $\dim\operatorname{coker}\psi$ |
|---|---|---|---|---|
| $A$ 型 $=\mathrm{std}_3\otimes\mathrm{sgn}$(**$K^{(25)}$ が実現**) | 1 | 1 | 2 | **0** |
| $A\otimes\mathrm{sgn}=\mathrm{std}_3$(**もう一方の型**) | 2 | 1 | 1 | **0** |
| 自明 1 次元 | 1 | 1 | 0 | 1(**ただし類は補題 CLASS-TRIV で消える**) |

$A$ 型: $V^{\theta=-1}=\{n_2=-n_1\}$(次元 2)は $(0,0,1)$ を含み $\sum n_i=1\ne0$ ⟹ $V^{\theta=-1}+\ker N_\tau=V$ ⟹ $\operatorname{coker}=0$。
$\mathrm{std}_3$ 型: $V^{\theta=-1}=\langle(1,1,0)\rangle$、$\sum=2\ne0$ ⟹ 同上。

> ### ★★ **K5-ENT-INSUF との整合(独立な裏取り)**
> $N=K^{(25)}$ では $V=K^{(5)}/K^{(25)}=5A_{25}\cong\mathbb F_5^3$ で作用は (4.7)(4.8) そのもの ⟹ $\operatorname{coker}=0$ ⟹ 本定理は **$d_{K^{(25)}}=5$** を予言する。これは **命題 K5-ENT-INSUF (c)(補題 THM44-odd)が独立に与える既知の事実と一致する。**
> ⟹ **定理 W6-NULL5 は、既に測られている 1 点で当たっている。** さらに本定理は **K5-ENT-INSUF の「なぜ」に答える**: 非分裂であっても、**ノルム方程式の障害群がそもそも消えている**からである。

### 2.6 ★ 検出力の在処 — 標数 2 と 3 だけ

定理 W6-OBS (C) の前件は $p\nmid6$。**$\theta$ の位数 2 と $\tau$ の位数 3 が標数を割るときだけ機構が壊れる。**

| 標数 | 壊れ方 | 帰結 |
|---|---|---|
| $p=3$ | $N_\tau=1+\tau+\tau^2=(\tau-1)^2$ に退化。$\operatorname{im}N_\tau\subsetneq V^\tau$ がありうる($H^1(C_3,V)\ne0$) | ★ **$\langle\tau\rangle$-加群として $V$ が非自由なとき障害が立つ**。自由($\mathbb F_3[C_3]$ 正則)なら消える |
| $p=2$ | $N_\theta=1+\theta=(\theta-1)$ に退化。$\ker N_\theta=V^\theta$ | ★★ **ほぼ全型で $\operatorname{coker}\ne0$**(§8 検算 B の $p=2$ 行: 7 型中 6 型が非零) |
| $p\nmid6$ | 退化なし | **全滅**(定理 W6-NULL5 と同型の議論) |

> ★ これは `hs_prop7_translation_v1.md` §2.4 の「悪い標数 $=p=5$」(そこでは $\rho$ の位数が 5)と**同じ型の現象**である。**検出器の生死は「ノルムを取る群の位数と係数標数の一致」で決まる。**

### 2.7 補題 EQUIV の適用範囲(**委嘱指定**)

addendum §A.3 補題 EQUIV は $\mathrm{res}:H^i(\widehat G_5,M)\xrightarrow{\sim}H^i(G_5,M)^{S_3}$($\lvert S_3\rvert=6$ が $\mathbb F_5$ で可逆)。**本稿での使い方と射程を明示する**:

| 項目 | 判定 |
|---|---|
| **使う場面** | **窓の分類**(拡大類の同変性)。addendum §A.13.4 の語法修正どおり **extension equivalence class までで、実現一意性ではない** |
| **使わない場面** | ★ **本稿の障害計算には使っていない。** $\psi_V$ の余核は $H^\ast(\widehat G_5,-)$ ではなく **$\langle\theta\rangle,\langle\tau\rangle$ 個別のノルム**で書かれており、$\lvert S_3\rvert$ の可逆性ではなく **$\lvert\theta\rvert=2,\lvert\tau\rvert=3$ の可逆性**が効く |
| **射程が切れる所** | $\operatorname{char}\mid6$。**$p=2$ では $\lvert S_3\rvert=6$ も可逆でない**ので EQUIV も同時に落ちる ⟹ **2-primary 標的では窓の分類も障害計算も両方 addendum の枠外**(§3.4 の見積りに反映) |
| **$p=3$** | EQUIV は $3\mid6$ ゆえ落ちる(addendum §A.3 帰結の但し書き「$\lvert S_3\rvert$ が係数の標数を割る場合はこの救済が効かない」がそのまま該当) |

---

## 3. 窓の構成戦略(**委嘱 §1 への回答**)

### 3.1 elementary-5 側($\rho$ 型・次元 3・$62{,}500$)— **判定: 構成しても無駄**

**委嘱の問い**: 「$K^{(5)}/N$ としての実現可能性判定(【K5-GAP-2】の攻め方・拡大類から marked subgroup $N\subset B_3$ を実際に構成できるか・障害は何か)」。

**回答**: ★ **実現可能性を調べる前に検出力で落ちる。**

- 定理 W6-NULL5 により、$\rho$ 型・$\rho\otimes\varepsilon$ 型のどちらが実現しようとも $d_N=5$。
- ⟹ 【K5-GAP-2】(実現性)と【K5-GAP-4】($\rho\otimes\varepsilon$ の実現)は、**W-6 の目的にとっては起票不要**になった。
- ⚠ **ただし数学的には未解決のまま**である。「実現しない」と言ったのではなく「**実現しても使えない**」と言った(**篩 F-4 の役割 = 走らせる前に検出力ゼロと分かる**・campaign §3.6)。

> ### ★ 会計(K5-MOD-v2 との関係 — **矛盾していない**)
> addendum §A.7 (C) は **下界** $\lvert PB_3/N\rvert\ge62{,}500$ を初等アーベル 5 核 class で証明した。本稿はその class を**上から**空にした。両者は独立の主張であり、**合わせると「初等アーベル 5 核 class には W-6 が 1 つも無い」**という完結した否定になる。
> ⟹ **§A.13.1 の禁止表現規律(「$62{,}500$ は一般 W-6 下界ではない」)は不変**。本稿はそれを**強める**方向に働く(その class 自体が空だから、下界の一般化は無意味になった)。

### 3.2 $p=3$ 側(WARN-13500)— **判定: 同じく死**

**委嘱の問い**: 「13,500 candidate の実現性判定(新 GAP =【K5-GAP-6】(i) の第一歩)」。

WARN-13500(addendum §A.13.2)= $\bar G=\widehat G_5/A\cong S_4$ の**標準 3 次元 $\mathbb F_3$-加群**の inflation。$A$ は自明に作用、$V=G_5/A\cong C_2^2$ は非自明。核位数 27、群位数 13,500。

**回答**: ★ $\theta,\tau$ の $S_4$ における像(補題 GAMMA (b): $\theta\mapsto$ 転置、$\tau\mapsto$ 3-巡回、$\theta\tau\mapsto$ **4-巡回**)を入れて計算すると

$$\dim V^\theta=2,\quad\dim V^\tau=1,\quad\ker N_\theta=\langle e_1-e_2\rangle,\quad N_\tau(\ker N_\theta)\ne0
\ \Longrightarrow\ \dim\operatorname{coker}\psi_V=1-1=\mathbf 0 .$$

($\mathrm{std}_3\otimes\mathrm{sgn}$ 版も **0**。§8 検算 E で両方 PASS。)

$$\Longrightarrow\ \boxed{\ \textbf{WARN-13500 は実現するとしても検出力ゼロ。}\ \textbf{【K5-GAP-6】(i) は本稿で閉じる(否定側)。}\ }$$

> ⚠ **落とし穴を 1 つ潰しておく**: $\theta\mapsto(12),\tau\mapsto(123)$ と**取ってしまうと** $\theta\tau$ が転置になり($S_4$ の中で位数 2)、**$\operatorname{coker}$ が 1 次元に見える**。正しい対 $(\theta\tau)$ **位数 4** を使うと 0 になる。**この 1 点の取り違えが「$p=3$ に検出力がある」という誤結論を生む** — 当方は初稿でこれを踏み、補題 GAMMA (a) の機械確認で捕まえた。**危険箇所 D-2(§6.2)に登録。**

### 3.3 ★ 生存表(**検出力が有り得る型の必要条件**)

§8 検算 B の全表(28 モジュール)から、$\operatorname{coker}\psi_V\ne0$ となるのは:

| 標数 | 型 | $\dim\operatorname{coker}$ | 備考 |
|---|---|---|---|
| 任意 | **自明加群**(1 次元・$\theta,\tau$ とも自明) | 1 | ★ **類は消える**(補題 CLASS-TRIV / K5-MOD-v2 (D))⟹ 使えない |
| $p=3$ | **sgn**($\theta\mapsto-1$、$\tau\mapsto1$)1 次元 | 1 | $\dim V^\Gamma=0$ ⟹ **CLASS-TRIV が効かない** ⟹ ★ **生存** |
| $p=3$ | $S_3$ の **2 次元既約** | 1 | ★ **生存**($\tau$ が $\mathbb F_3$ で非自由) |
| $p=3$ | $\tau$ が **2×2 unipotent**(非自由 Jordan) の 2 次元 | 1 | ★ **生存**(§8 検算 F で実物確認) |
| $p=3$ | $\mathbb F_3[C_3]$ **正則** + 座標転置(3 次元) | 1 | ★ **生存** |
| $p=2$ | $A$ 型 / $A\otimes\mathrm{sgn}$ / 自明 / sgn / $\mathrm{std}_3$ / $\mathrm{std}_3\otimes\mathrm{sgn}$ | 各 1 | ★★ **7 型中 6 型が生存**($S_3$ の 2 次元だけ 0) |
| $p=5,7$ | **全型** | 0 | 死(定理 W6-NULL5) |

> ⚠ **この表は必要条件の表である。** $\operatorname{coker}\ne0$ は「**障害群が非零**」であって「**類が非零**」ではない。類の非零性は $\widetilde f_0$ と拡大の具体形に依存し、**紙では決まらない**(§4.1)。**表の行を「検出力あり」と読まないこと。**

### 3.4 ★★ 優先度提案(**委嘱の「どちらが安いか・両方やるか」への回答**)

**答: どちらもやらない。標的を差し替える。**

| 順位 | 標的 | 根拠 | 規模の見積り | 状態 |
|---|---|---|---|---|
| **1** | ★★ **2-primary 核**(【K5-GAP-5】) | §3.3 で最も広く生存。かつ **$2\mid\lvert G_5\rvert=500$** ゆえ $H^2(G_5,V)\ne0$ が期待でき、**非分裂拡大の供給も期待できる** | 未確定。$\lvert V\rvert=2^k$ ⟹ $\lvert PB_3/N\rvert=500\cdot2^k$ — ★ **$62{,}500$ より遥かに小さい窓が有り得る**($k=2$ なら 2000) | **UNKNOWN(有望)** |
| **2** | $p=3$・**非自由 $\tau$ 構造**の核(sgn 型 / 2 次元既約 / unipotent 型) | §3.3 で生存 | $\lvert PB_3/N\rvert=500\cdot3^k$($k=1,2$ ⟹ 1500, 4500)— ★ **これも安い** | **UNKNOWN** |
| — | ~~elementary-5($62{,}500$)~~ | ★ **定理 W6-NULL5 で死** | — | **CLOSED(否定)** |
| — | ~~WARN-13500($p=3$・$\mathrm{std}_3$)~~ | ★ **§3.2 で死** | — | **CLOSED(否定)** |

> ### ★ **窓の規模が 1 桁下がったという副産物**
> 委嘱の 2 候補はどちらも $\ge13{,}500$ だった。生存する標的は $500\cdot2^k$ / $500\cdot3^k$ の形で、**$k=2$ なら 2,000〜4,500** — campaign §4.3 の RAM/cap 見積り($\le62{,}500$ で無害)の**内側に余裕で入る**。⟹ **計算資源はもはや律速ではない。律速は「そういう $N\trianglelefteq B_3$ が実在するか」だけ**(【K5-GAP-2】の 2/3-primary 版)。

> ### ⚠ 2-primary 標的に固有の困難(**先に名指す**)
> 1. **補題 EQUIV が効かない**($2\mid6$)⟹ 同変障害を plain $H^2(G_5,V)^{S_3}$ で書けない(§2.7)。**addendum の枠外**。
> 2. **補群の一意性が壊れる**($\mathrm{Hom}(G_5,V)=V[2]^2\ne0$・addendum §A.9【K5-GAP-5】)⟹ K5-MOD-v2 (D) の「一意 ⟹ 正規 ⟹ $B_3$-安定」の一行が使えない。
> 3. **$K^{(20)}$ という既知の反例的較正が在る**(§4.3)⟹ 「2-primary なら検出力あり」と読まないこと。
> ⟹ **これらは【文献要請 ROOF2-L1】(同変拡大の障害理論)の射程そのもの**である(§7.5)。

---

## 4. 検出力の事前見積り(**C2-Q / HS の轍を踏まない**・委嘱 §3)

### 4.1 ★ 何が事前に見積もれて、何が見積もれないか(**正直に**)

| 量 | 紙で決まるか |
|---|---|
| **障害群** $\operatorname{coker}\psi_V$ | ★ **決まる**(定理 W6-OBS・$\mathbb F_p$ 線型代数・実装ゼロ) |
| **障害類** $[(-\beta_\theta,-\beta_\tau)]$ | ✗ **決まらない**。$\widetilde f_0$ の具体形 = $N$ の具体的な表示が要る ⟹ **有限計算(GAP)** |
| $d_N$ | ✗(上記に従属) |

> ⚠ ★ **これが C2-Q / HS との構造的な差である。** HS 側は定理 D4-POWER で「検出器が厳密に 1 次元」まで**紙で**決まった。**本件はそこまで行かない** — 紙で決まるのは**障害群までで、類は計算**である。⟹ **「$\operatorname{coker}\ne0$ の窓を見つけた」を成果と呼ばないこと**(§5 の停止規則 S-W6-3)。

### 4.2 ★ SURJ の識別力(**委嘱の H8′ 適用可否**)

**系 H8′**(`docs/week3-狩場計画_v2.md` §2.1): $P$ が $p$ 群、$\bar f\in[P,P]\subseteq\Phi(P)$、$\gcd(2m+1,p)=1$ ⟹ 全射性は自動(Frattini)。

★ **W-6 窓族には H8′ はそのままでは適用できない**: $P_N$ は $G_5$(位数 $500=2^2\cdot5^3$)へ全射するので **$p$ 群ではない**。⟹ **委嘱の「H8′ の適用可否」への答は「不適用」**。

**代わりに相対版を立てる**:

> ### 補題 SURJ-W6(candidate・**H8′ の相対版**)
> $V=K^{(5)}_{F_2}/N_{F_2}$、$H:=\langle\bar x^{2\widetilde m+1},\widetilde f^{-1}\bar y^{2\widetilde m+1}\widetilde f\rangle\subseteq P_N$ とする。$\phi_1$(level 5)が (SURJ) を満たすので $HV=P_N$。ゆえに
> $$\boxed{\ V\subseteq\Phi(P_N)\ \Longrightarrow\ H=P_N\ (\textbf{SURJ 自動})\ }$$
> さらに **$V$ が既約 $P_N$-加群かつ拡大 $1\to V\to P_N\to P_5\to1$ が非分裂ならば $V\subseteq\Phi(P_N)$**。
> **証明.** 前半は Frattini 論法($HV=P_N$、$V\subseteq\Phi(P_N)$ ⟹ $H=P_N$)。後半: $V\not\subseteq\Phi(P_N)$ なら $V\not\subseteq M$ なる極大部分群 $M$ が在り、$M\cap V$ は $V$ の真部分加群 ⟹ 既約性より $0$ ⟹ $M$ が $V$ の補群 ⟹ 分裂、矛盾。∎

> ### ★ 委嘱の問いへの回答: **「SURJ はこの窓族でも識別力ゼロか」**
> **条件つきで YES。** 非分裂・既約核の窓(= W-6 の狙う型)では SURJ は**自動 = 識別力ゼロ**である。
> ⚠ **ただし「自動」を仮定として書かず、段 0 で `V ⊆ Φ(P_N)` を assert すること**(§5.3 の発注仕様)。分裂する窓(検出力ゼロが別途分かっている窓)では自動性が保証されない。
> ⟹ **`hs_prop7_translation_v1.md` §8.7.6 と同じ事故型**(識別力ゼロの検査を「通った」と数える)を、**発注仕様の 1 行で先に塞ぐ**。

### 4.3 ★★ dummy(識別力 fixture)

campaign §5.3 の DF-1/DF-2/DF-3 は**抽出器**の識別力を保証する。W-6 では**障害ソルバ**の識別力を別に保証する必要がある。

| fixture | 入力 | 期待出力 | 何を保証するか |
|---|---|---|---|
| **DF-W6-1**(★ 合成 dummy) | $V=\mathbb F_3^2$、$\tau=\begin{psmallmatrix}1&1\\0&1\end{psmallmatrix}$、$\theta=\mathrm{diag}(1,-1)$、$(\beta_\theta,\beta_\tau)$ を $\operatorname{coker}$ の非零類に取る | ソルバが **「解なし」** を返す | ★★ **ソルバが「持ち上がらない」を報告できること**。これが無ければ全 PASS 群は情報量ゼロ(§8 検算 F で $\operatorname{coker}=1$ を確認済 — **実在する**) |
| **DF-W6-2**(★★ 既製の実物 control) | $W\text{-}3=K^{(20)}=K^{(5)}\cap K^{(4)}$(2-primary 核) | $\operatorname{coker}\psi_V\ne0$ **かつ** 障害類 $=0$ **かつ** $d=5$ | ★★ **「障害群は非零だが類は消える」の実物**。$d=5$ は**正典 Thm 4.4($4\mid q$)の証明掲載分岐**で独立に既知 ⟹ **紙の外部 anchor つき** |
| **DF-W6-3** | $V=\mathbb F_5^3$((4.7)(4.8)) | $\operatorname{coker}=0$ ⟹ 「必ず解あり」 | 定理 W6-NULL5 の実装側再現。$K^{(25)}$ で $d=5$(既知)と突合 |
| **DF-W6-4**(向き規約) | $\theta\tau$ の位数を assert | **4**(24 でなく) | ★ 危険箇所 D-2 の検出器(§3.2 の落とし穴を実装で踏まない) |

> ### ★ DF-W6-2 の値打ち(**新しい実測を要しない**)
> `certificates` に $K^{(20)}$ の GT が無くとも、**$V=K^{(5)}/K^{(20)}$ の $\Gamma$-加群構造は紙で書ける**(2405 の $K^{(4)}$ 側)。⟹ **$\operatorname{coker}\ne0$ を紙で確認し、$d=5$ が既知であることから「類 $=0$」を retrodiction として得る。** campaign §3.4 の「既存証明書に反例が在った」と同じ型の資産活用である。
> ⚠ **【K5-GAP-W3】(新設)**: $V=K^{(5)}/K^{(20)}$ の $\Gamma$-加群としての明示分解は**当方未計算**。DF-W6-2 を fixture として使う前に必要。**安い(紙 1 枚)と見積もる。**

### 4.4 篩 W6-F(**発注前に通す 5 段** — campaign §3.6 F-1〜F-4 の後継)

| 段 | 検査 | 実装 | 落ちる例 |
|---|---|---|---|
| **W6-F0** | $B_0$ が奇位数巡回 / $\dim\le2$ の初等 5 核 | 紙 | addendum §A.8 F-0′(不変) |
| **W6-F1** | ENT-CRIT (b) が破れる(= $G_5$ の作用が非自明・K5-MOD-v2 (F)) | 紙 | 中心核・自明作用核 |
| **W6-F2** ★ | ★ **$\gcd(\lvert V\rvert,6)\ne1$**(= 標数 2 または 3) | 紙 | ★★ **初等アーベル 5 核すべて**(定理 W6-NULL5)・$p\ge7$ 核すべて |
| **W6-F3** ★ | ★ **$\operatorname{coker}\psi_V\ne0$**(定理 W6-OBS の式・$\mathbb F_p$ 線型代数) | 紙 or 数行 | ★ **WARN-13500**・$\mathbb F_3[C_3]$ 自由な核 |
| **W6-F4** | $V\subseteq\Phi(P_N)$(SURJ 自動性・補題 SURJ-W6) | 段 0 assert | 分裂窓 |
| **W6-F5** | ★ **障害類が実際に非零**(有限計算 — ここだけ実装が要る) | GAP | ここまで来て初めて実弾 |

> **W6-F0〜F4 は紙 or 数行で判定できる(実装ゼロ)。W6-F2 で落ちる窓は起票しない。**
> ★ **これが本稿の実務上の主産物**: campaign §3.6 の篩は F-4 で「紙で見積もる」としか書けなかったが、**W6-F2/F3 は判定基準が確定した**。

---

## 5. 予言凍結の型(**P-W6-x** — 委嘱 §4)

> **本節は実装前の凍結対象。値をコードに書かない。標的が確定した時点で別 version として事前登録する。**

### 5.1 予言(**IF-FIRST** — 障害類を一度も計算する前に固定)

| # | 予言 | 根拠 | ★ 反証条件(対称形) |
|---|---|---|---|
| **P-W6-1** ★★ | **初等アーベル 5 核の窓では $d_N=5$**(検出力ゼロ) | 定理 W6-NULL5 | ★ そのような窓で $d_N=1$ が出れば、**定理 W6-OBS / CLASS-TRIV / 補題 TWIST / K5-MOD-v2 (D) のいずれかが偽** |
| **P-W6-2** ★ | **$K^{(25)}$ で $\operatorname{coker}\psi_V=0$**(既知の $d=5$ と整合) | §2.5 + 命題 K5-ENT-INSUF | 不整合なら (4.7)(4.8) の読み or 実装が偽(**最安の健全性検査**) |
| **P-W6-3** ★ | **WARN-13500 型($\mathbb F_3$・$\mathrm{std}_3$)で $\operatorname{coker}\psi_V=0$** | §3.2 | 非零なら $\theta,\tau$ の $S_4$ 内の像の同定(補題 GAMMA (b))が偽 |
| **P-W6-4** ★ | **$\theta\tau$ は $A$ 上で位数 4**($S_3$ ではない) | 補題 GAMMA (a) | 位数 2 なら (4.7) の符号の読みが偽 ⟹ **§3.2 の結論が反転する** |
| **P-W6-5** | **$W\text{-}3=K^{(20)}$: $\operatorname{coker}\psi_V\ne0$ かつ 障害類 $=0$ かつ $d=5$** | §4.3 DF-W6-2 + 正典 Thm 4.4 | ★ $d\ne5$ なら正典の証明掲載分岐が偽 |
| **P-W6-6** | **DF-W6-1 でソルバが「解なし」を返す** | §8 検算 F($\operatorname{coker}=1$ の実物) | ★ 返さなければ**ソルバは $d=1$ を報告する能力を持たない** ⟹ 以後の全 PASS は情報量ゼロ |
| **P-W6-7** | **SURJ は $V\subseteq\Phi(P_N)$ の窓で全 charming 候補が通る(識別力ゼロ)** | 補題 SURJ-W6 | 通らない候補が出れば補題 SURJ-W6 か level-5 の (SURJ) が偽 |
| **P-W6-8** ★ | ★ **標的が確定したら、その窓の $d_N$ を測る前に $\operatorname{coker}\psi_V$ の次元と障害類の予測値を凍結する** | — | (契約条項・値は標的確定時に埋める) |

> ⚠ **P-W6-1〜3 は「何も出ない」ことを予言している**(否定型)。**当たっても fake 非存在の証拠にはならない。** 値打ちは反証可能性の側にある(campaign §4.2 の注記と同型)。

### 5.2 停止規則(**S-7′ / S-8 準拠** — `hs_prop7_translation_v1.md` §9)

| # | trigger | verdict | note |
|---|---|---|---|
| **S-W6-1** | 段 0 のアンカー(P-W6-2/3/4)のいずれかが不一致 | `PREREGISTRATION_FALSIFIED / INTEGRITY_STOP` | ★ **S-7′ 逐語**: 即時停止・部分結果は保存・**同一 run / 同一登録内で予言を書き換えない**・構成 bug と数学予言の偽を別検分・続きは**別 version の事前登録から** |
| **S-W6-2** | DF-W6-1 でソルバが「解なし」を返さない | `CALIBRATION_FAILED / INTEGRITY_STOP` | ★ **S-8 型**: 識別力ゼロの検査を「通った」と数えない。**後から期待値を弱めない** |
| **S-W6-3** ★ | $\operatorname{coker}\psi_V\ne0$ を確認しただけで「検出力ある窓を作った」と書こうとした | `OVERCLAIM / STOP` | ★ **群 $\ne$ 類**(§4.1)。**障害類の非零性まで到達していない限り candidate と書く** |
| **S-W6-4** | 障害類が非零 ⟹ **$d_N=1$ の可能性** | **campaign S-3 を発動** | T2(全列挙)を必ず追走。**T2 完了まで「fake 発見」と書かない**。★ **司令塔へ即報**(campaign §4.4 の衝突 + §6.2 X-1 の inference-contact event) |
| **S-W6-5** | §2.2 の (V-cen) / 補題 TWIST の前件が破れる窓に当たった | `SCOPE_OUT / STOP` | 【K5-GAP-W1】が未閉鎖 ⟹ **自己判断で続行しない** |
| **S-W6-6** | campaign §2.2 の禁止量に触れざるを得なくなった | campaign **S-4** 逐語 | **即停止・司令塔へ上申** |

> ★ **cert に貼る停止規則ブロックは `hs_prop7_translation_v1.md` §9.4 の形式に合わせる**(`stop_rules` + `prediction_source.codegen_uses_expected_values: false`)。**停止規則を cert に書かない起票は差し戻し**(P101-1 (5) の規律を継承)。

### 5.3 実装発注の分割案(**委嘱 §4**)

| # | 何を | 誰に | 入出力 | 依存 |
|---|---|---|---|---|
| **I-1** | ★ **$\operatorname{coker}\psi_V$ 計算器**($\mathbb F_p$ 上・$\theta,\tau$ 行列 + $V$ を入力に 3 式で交叉検算) | **implementer**(境界明確・数十行) | in: $(p,\theta,\tau)$ / out: $\dim\operatorname{coker}$ + 3 式一致フラグ | なし(**今すぐ発注可**) |
| **I-2** | **DF-W6-1/3/4 の fixture 実行** | implementer | 期待値は §5.1 のリテラル | I-1 |
| **I-3** | ★ **$K^{(5)}/K^{(20)}$ の $\Gamma$-加群分解**(DF-W6-2 の材料) | **数学者**(紙)→ implementer(裏取り) | 【K5-GAP-W3】 | なし |
| **I-4** | ★★ **2/3-primary な $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$ の在庫探索**(`lins` 低指数正規部分群・指数 $6\cdot500\cdot2^k$ 等) | implementer(**司令塔が規模を裁定**) | out: 候補 $N$ の一覧 + 各々の $V$ の $\Gamma$-加群型 | I-1(篩 W6-F3 を通すため) |
| **I-5** | $\widetilde f_0$ の構成と $(\beta_\theta,\beta_\tau)$ の計算(**障害類**) | implementer | 標的窓確定後 | I-4 + §5.1 の凍結 |
| **I-6** | **CI**: I-1 の 3 式一致・DF-W6-4(位数 4)・P-W6-2/3 を回帰項目に | **ep-keeper**(CI 資産) | — | I-1/I-2 |

> ★ **I-1〜I-3 は標的が未確定でも走らせられる**(較正のみ・$\mathrm{Im}\,R$ 非接触・**Phase 2 の解錠を要しない**)。**I-4 が本命の入口**であり、そこで初めて司令塔の規模裁定が要る。

---

## 6. 危険箇所(**委嘱 §5** — campaign §6 の X 表と突合)

### 6.1 名前衝突(**grep 事故の元**)

| # | 衝突 | 正しい扱い |
|---|---|---|
| **N-1** ★ | **$\varepsilon$**。本稿の $\varepsilon$ は $S_4$ の符号指標(addendum §A.7 (E) 由来)。campaign の $\varepsilon=m\bmod2$($\Theta_5$ 第 3 成分)とも、封印語彙の **「ε bits」**(`epsbits_*`)とも**別物** | 本稿では符号指標を **`sgn`** と書く(以後 $\varepsilon$ を使わない)。cert 欄名に `eps` を使わない。**`epsbits` を grep して本稿の cert が引っかからないこと**を受入条件に |
| **N-2** ★★ | ★ **【K5-GAP-4】【K5-GAP-5】の番号衝突(実在の欠陥)**。campaign §7.4 は GAP-4 = 「$B_0$ が 2 群」・GAP-5 = 「$d_{\rm gen}(5)$ の値」。addendum §A.9 は GAP-4 = 「$\rho\otimes\mathrm{sgn}$ の実現」・GAP-5 = 「$2\mid\lvert B_0\rvert$ の核」を**新設**と書く ⟹ **campaign GAP-4 が addendum GAP-5 に移り、campaign GAP-5(= $d_{\rm gen}(5)$ の値)は表から消えた** | ★ **司令塔へ上申**(§7.6-3)。本稿は **addendum §A.9 の番号を採用**し、消えた「$d_{\rm gen}(5)$ の値」は **【DIV-GAP-1】の $n=5$ 行**(campaign §7.1 の呼び方)で参照する。**本稿の新設は【K5-GAP-W1〜W3】**(W 接頭辞で衝突回避・**grep 済**) |
| **N-3** ★★ | **$\Gamma$ / $S_3$**。本稿の $\Gamma=\langle\theta,\tau\rangle$ は $A$ 上 $S_4$(位数 24)。**roof2 §7.4 【文献要請 ROOF2-L1】と addendum の「$\Gamma=S_3$」は別の群である** | ★ 文献要請を引くときは「**外側 $S_3=B_3/PB_3$**」と「**作用群 $\Gamma=\langle\theta,\tau\rangle$**」を書き分ける(§7.5) |
| **N-4** | **$\rho$**。addendum の $\rho$($\widehat G_5$-加群の型)と、`hs_prop7_translation_v1.md` の $\rho$(位数 5 の巡回作用)は別物 | 本稿では前者のみ使い、必要なら $\mathrm{std}_3\otimes\mathrm{sgn}$ と書く |
| **N-5** | **W-6**。campaign §3.7 の行名。`week4-NInfty` 系の W 番号とは無関係 | cert id を `K5gen.W6.*` に統一 |
| **N-6** | **$V$**。addendum (S3) は $V:=G_5/A\cong C_2^2$。**本稿の $V$ は核 $K^{(5)}_{F_2}/N_{F_2}$** | ★ 本稿は addendum の $V$ を **$Q$**(campaign の記法)と書く。§1.1 で明示済 |
| **N-7** | **定理 H8 の $A$**。狩場計画 §2.1 の $A=[P,P]$(窓全体の導来群)。**本稿の $A=[G_5,G_5]$**(level 5) | 本稿は前者を $A_N$ と書く(§2.1) |

### 6.2 数学的な危険箇所(**踏むと結論が反転する**)

| # | 危険 | 検出器 |
|---|---|---|
| **D-1** ★★ | 「$\theta,\tau$ は 3 座標を置換する $S_3$ 作用」と読む | ★ **(4.7) の第 3 座標の反転を落とすと $\Gamma$ が $S_3$ になり、$\rho\otimes\mathrm{sgn}$ 型の $\operatorname{coker}$ が 1 に見える** ⟹ **P-W6-4**(位数 4 の assert)が検出器 |
| **D-2** ★★ | $S_4$ の中で $\theta\mapsto(12),\tau\mapsto(123)$ と取る(**$\theta\tau$ が転置になる**) | ★ **WARN-13500 の判定が 0 → 1 に反転する** ⟹ **DF-W6-4** が検出器。**当方は初稿でこれを踏んだ** |
| **D-3** ★ | $\widetilde m=0$ での不可解性から $d_N=1$ を結論する | ★ **§1.2 の論理の向き**。$\widetilde m\equiv0\ (10)$ の他項が残る ⟹ **S-W6-4 で T2 追走** |
| **D-4** ★ | $\operatorname{coker}\ne0$ を「検出力あり」と読む | ★ **S-W6-3**。群 $\ne$ 類 |
| **D-5** | (V-cen) を暗黙に使う | ★ **【K5-GAP-W1】**・**S-W6-5** |
| **D-6** | $\theta/\tau$ を商 $F_2/N_{F_2}$ 上で評価する近道($c\in N$ 依存) | campaign §5.0 の注意を継承。**段 0 で $c\in N$ を assert**(通らなければ語レベル経路) |
| **D-7** ★ | 2-primary 標的で addendum の補題(EQUIV・EXT0・SIMPLE)を流用する | ★ **§2.7**: $2\mid6$ ゆえ**全部落ちる**。addendum は elementary-5 専用(§A.13.1 の見出し規律)|

### 6.3 封印との交差(**campaign §6.2 の X 表と突合**)

| # | campaign の X 行 | 本稿での状態 |
|---|---|---|
| **X-1** | $K^{(5)}$ 算術飽和 manifest の封印予言 (P1) との**推論水準の干渉** | ★ **本稿は干渉を減らす方向**である。主結果はすべて $d_N=5$ 側(検出力ゼロ)であり、**inference-contact event(裁定 412)は発火しない**。発火は S-W6-4 の先(障害類が非零 ⟹ 実測 ⟹ $d_N=1$)でのみ起きる |
| **X-4** | PSL 窓を屋根にすると封印欄に触れる | ★ **本稿も PSL 屋根を除外**(§3.4 の標的は $K^{(4)}$-系 / $C_3$-系のみ)。触れる必要が出たら **S-W6-6** |
| **X-6/X-7** | $\hat c_\mu$ / N∞ / 比較橋 $B_{\rm FC}$ | ★ **データ水準・推論水準とも非交差**。本稿は有限群 + $\mathbb F_p$ 線型代数のみ |
| **X-8** | cert 名前空間 | ★ **本稿の cert は `certificates/k5gen/` の下**(campaign と同じ)。`k5blocks/ k5e/ k5fixture/ k5pipeline/` に書き込まない |
| **X-9** | FAKE-VOID 台帳 FV-28 | 本稿は起票のみ。台帳更新は司令塔 |

---

## 7. 格付け・GAP・新規性・申し送り

### 7.1 格付け

| 主張 | 格 |
|---|---|
| **補題 GAMMA** ($(\theta\tau)$ が位数 4・$\Gamma\vert_A\cong S_4$・$A\cong\mathrm{std}_3\otimes\mathrm{sgn}$) | ★ **paper-proof candidate**(正典 (4.7)(4.8) からの直接計算 + 機械確認・**Sol 未監査**) |
| **定理 W6-OBS (A)(B)(B′)(C)** | ★★ **paper-proof candidate**(線型代数のみ・**Sol 未監査**)。使う外部入力は標準線型代数だけ |
| **補題 TWIST** | ⚠ **candidate(骨格のみ)**。**【K5-GAP-W1】が未閉鎖** |
| **補題 CLASS-TRIV** | ★ **paper-proof candidate**。**K5-MOD-v2 (D)((AR) 相対)と【K5-GAP-W2】に相対** |
| **定理 W6-NULL5** | ★★ **paper-proof candidate**((V-cen) の下では TWIST 不要 ⟹ **$K^{(25)}$ 型を含む射程では無条件**)。**(AR) 相対**(命題 K5-SPL0 経由の部分) |
| **§3.2 の WARN-13500 判定** | ★ **paper-proof candidate**(補題 GAMMA (b) に相対) |
| **補題 SURJ-W6** | **paper-proof candidate**(Frattini 論法・初等) |
| **§3.3 の生存表** | **必要条件の表**(機械計算・single lane python) |
| **予言 P-W6-1〜8** | **prediction(未測定)** |
| **障害類の値・$d_N$・$d_{\rm gen}(5)$** | ★ **UNKNOWN** |
| §8 の検算 | ★ **single lane(python)。cross-checked ではない。Lean 検証でもない** |
| Lean 検証 | ✗ **していない** |

### 7.2 ★ この設計が買うもの・買わないもの

| | 内容 |
|---|---|
| **買うもの (1)** | ★★ 【K5-GAP-1】の**明示式**。捻れノルムの余核が $\mathbb F_p$ 線型代数に落ちた ⟹ 篩 W6-F3 が**実装ゼロで判定可能**になった |
| **買うもの (2)** | ★★ **候補族の大量刈り込み**: 初等アーベル 5 核 class **全滅**・WARN-13500 **死**・$p\ge7$ 核**全滅**。⟹ **委嘱の 2 候補への実装予算がゼロで済んだ** |
| **買うもの (3)** | ★ **標的の差し替えと規模の縮小**: 2/3-primary へ。$500\cdot2^k$ / $500\cdot3^k$ ⟹ **RAM 制約が律速でなくなった** |
| **買うもの (4)** | ★ **既製 control の同定**($K^{(20)}$・DF-W6-2)— 新しい実測を要しない |
| ★ **買わないもの (1)** | **検出力のある窓そのもの**。本稿は「どこに**有り得ない**か」を確定しただけで、**W-6 は依然として未構成**である |
| ★ **買わないもの (2)** | **障害類**。紙で決まるのは群まで(§4.1)|
| **買わないもの (3)** | $d_{\rm gen}(5)$・$B_{\rm FC}$ の情報 |

### 7.3 【K5-GAP】の更新(**番号は §6.1 N-2 の裁定待ち・本稿の新設は W 接頭辞**)

| # | 内容 | 状態 |
|---|---|---|
| **【K5-GAP-1】** | K5-BIT の系(ノルム写像の余核・非可換下位項) | ★ **CLOSED(候補)**: 余核 = 定理 W6-OBS、下位項 = 補題 TWIST。**残余は【K5-GAP-W1】のみ** |
| **【K5-GAP-2】** | $H^2(G_5,A)^{S_3}$ の類の実現性 | ★ **W-6 の目的には不要になった**(§3.1)。数学的には未解決 |
| **【K5-GAP-4】**(addendum) | $\rho\otimes\mathrm{sgn}$ の実現 | ★ **同上**(実現しても検出力ゼロ) |
| **【K5-GAP-5】**(addendum・2-primary) | $2\mid\lvert B_0\rvert$ の核 | ★★ **第一標的へ昇格**(§3.4) |
| **【K5-GAP-6】(i)**(WARN-13500) | $p=3$・$\mathrm{std}_3$ の実現性 | ★ **CLOSED(否定側・§3.2)** — 実現性を問う前に検出力ゼロ |
| **【K5-GAP-6】(ii)(iii)** | 一般 $\mathbb F_q$・非初等核・一般 W-6 の最小位数 | ★ **射程が縮んだ**: 定理 W6-NULL5 で **$q\nmid6$ は全滅** ⟹ **残るのは $q\in\{2,3\}$ と非初等核だけ** |
| ★ **【K5-GAP-W1】(新設)** | 補題 TWIST の $\theta_\ast^2=\mathrm{id}$・$\tau_\ast^3=\mathrm{id}$ | **UNKNOWN**(安いと見積もる・**Sol 監査点 W-1**) |
| ★ **【K5-GAP-W2】(新設)** | 補題 CLASS-TRIV (d) の $PB_3/\bar N$ 水準 ↔ $F_2/\bar N_{F_2}$ 水準の突合($c\in N$ の要否) | **UNKNOWN**(安い) |
| ★ **【K5-GAP-W3】(新設)** | $V=K^{(5)}/K^{(20)}$ の $\Gamma$-加群としての明示分解(DF-W6-2 の材料) | **UNKNOWN**(紙 1 枚) |
| ★ **【K5-GAP-W4】(新設)** ★★ | ★ **2/3-primary な $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$V$ が §3.3 の生存型、の実在**。**これが新しい律速である** | **UNKNOWN(本命)** |

### 7.4 新規性の申告(**grep 済**)

**grep 語**: `coker`・`余核`・`ノルム`・`N_theta`・`N_tau`・`捻れノルム`・`(4.7)`・`std_3`・`S_4`・`Frattini`・`Phi(P)`・`H8′`・`位数 4`・`signed permutation`・`符号付き置換`(`docs/` `sol/` `provenance/` `search/` 全文)。

| 項目 | 既出か | 差分 |
|---|---|---|
| 「(3.11) は $C_3$-拡大の分裂問題」 | ★★ **既出**(**定理 H8**・`week3-狩場計画_v2.md` §2.1・$\sigma^3=\mathrm{Inn}(E_m)$) | ★ **本稿は $K^{(5)}$ への相対版**(level 5 の解の持上げ)に作り替えた。H8 は絶対版(可解性)、本稿は相対版(**障害群**) |
| 「$\gcd(\lvert A\rvert,3)=1$ ⟹ Schur–Zassenhaus で (3.11) 可解」 | ★ **既出**(定理 H8) | ★ 本稿の定理 W6-OBS (C) は**その相対版で、しかも $\theta$ 側と結合した形**。「6 と互いに素なら全滅」は H8 の $\theta$ 込み拡張 |
| 系 H8′(SURJ 自動・$p$ 群) | ★ **既出** | ★ **補題 SURJ-W6 = 非 $p$ 群への相対版**(Frattini を「核が $\Phi$ に入る」に置き換える) |
| 設計仮説 D-1(捻れノルムの余核) | ★ **既出**(campaign §3.6・**型の記述のみ・UNKNOWN**) | ★★ **本稿が式にした**(定理 W6-OBS) |
| $(\theta\tau)$ が $A$ 上で**位数 4**・$\Gamma\vert_A\cong S_4$ | **発見できず** | ★ 本稿(補題 GAMMA)。addendum §A.7 (E) の $\bar G\cong S_4$ とは**別の経路で同じ $S_4$ に到達**しており、両者が一致することも本稿の内容 |
| $A\cong\mathrm{std}_3\otimes\mathrm{sgn}$ の同定 | **発見できず** | ★ 本稿(addendum は $\rho$ と $\rho\otimes\mathrm{sgn}$ の 2 型があると書いたが、**どちらが $A$ か**は同定していない) |
| 「初等アーベル 5 核は検出力ゼロ」 | **発見できず** | ★★ 本稿(定理 W6-NULL5) |
| 「WARN-13500 は検出力ゼロ」 | **発見できず**(Sol F101-2.1 は「実現性は未証明」までで検出力には触れていない) | ★★ 本稿(§3.2) |
| 「検出器の生死は作用群の位数と標数の一致で決まる」 | ★ **既出の型**(`hs_prop7_translation_v1.md` §2.4「悪い標数 $=p=5$」) | 本稿は**同じ型を $\theta,\tau$ に適用**。**型の再利用であって新機構ではない** |

**「初」という語は使わない。** 相対ノルムの余核で持上げ障害を書く型は群拡大論では標準でありうる。**本設定への翻訳と、それによる 2 候補の否定判定が本稿の寄与**である。

### 7.5 【文献要請】

> ### 【文献要請 K5-W6-L1】(★ **ROOF2-L1 / K5-L1 の射程内か要判定**)
> **困難**: $\Gamma=\langle\theta,\tau\rangle$($\theta^2=\tau^3=1$・$\Gamma$ は $C_2*C_3\cong PSL_2(\mathbb Z)$ の商)が作用する有限群 $G$ と、その $\Gamma$-同変な拡大 $1\to V\to\widetilde G\to G\to1$($V$ は $\mathbb F_p$-加群、**$p\in\{2,3\}$ = $\Gamma$ の生成元の位数を割る標数**)が与えられたとき、$G$ の**特定の元** $g$ が「$\theta$-ノルム 1 かつ $\tau$-ノルム 1」を満たす元へ $\widetilde G$ で持ち上がるかを、$V$ の $\Gamma$-加群構造から判定したい。
> **欲しい結果の型**: ① **モジュラー表現論側**: $\mathbb F_p[\Gamma]$-加群($\Gamma$ が $(2,3)$-生成の有限群)に対する $\operatorname{coker}(N_\theta,N_\tau)$ の消滅判定 — **Tate コホモロジー $\hat H^0(\langle\theta\rangle,-)$ と $\hat H^0(\langle\tau\rangle,-)$ の「結合」を扱う機構**。② **既出との関係**: 【文献要請 ROOF2-L1】は「外側 $S_3=B_3/PB_3$ の同変拡大の障害理論」であり、**本要請の $\Gamma$ は別の群**(§6.1 N-3)。**重複ではない可能性が高いが、判断は司令塔。**
> **既に持っているもの**: 本稿の定理 W6-OBS(**判定は済んでいる** — 有限次元なら線型代数で決まる)。⟹ ★ **本要請は「必須」ではなく「構造的理解が欲しい」水準**である。**総当たりで済むなら文献は不要。**
> **【文献要請 K5-L1】(campaign §7.4)の②「特定元の持上げ可能性を $H^1$/捻れノルムの余核で書く定理」は、本稿の定理 W6-OBS が(この設定では)自前で答えた** ⟹ **②は取り下げを提案**(判断は司令塔)。

### 7.6 申し送り(司令塔へ)

1. ★★ **委嘱の 2 候補が両方死んだ**(§0-2)。**標的の差し替え(2/3-primary へ)の裁定を仰ぐ。** 速達送付済。
2. ★★ **I-1〜I-3(§5.3)は標的未確定でも即発注できる**(較正のみ・$\mathrm{Im}\,R$ 非接触・Phase 2 の解錠不要)。**I-4(`lins` 在庫探索)が本命の入口**で、そこで規模の裁定が要る。
3. ★★ **【K5-GAP-4】【K5-GAP-5】の番号衝突**(§6.1 N-2)— campaign §7.4 と addendum §A.9 で番号が食い違い、**campaign GAP-5「$d_{\rm gen}(5)$ の値」が表から消えている**。**台帳の整合は司令塔の記帳事項**。
4. ★ **campaign §3.7 の W-6 行の書き換え**を提案: 「$\ge62{,}500$」→ 「★ **初等アーベル 5 核 class は空(定理 W6-NULL5)。生存標的は 2/3-primary で $500\cdot2^k$ / $500\cdot3^k$**」。**§A.13.1 の禁止表現規律は不変**(むしろ強まる)。
5. ★ **campaign §3.6 の篩 F-1〜F-4 / addendum §A.8 の F-0′〜F-4′ を §4.4 の W6-F0〜F5 で置き換える**ことを提案(**F-4「紙で見積もる」が W6-F2/F3 で判定基準つきになった**)。
6. ★ **roof2 §7.4【文献要請 ROOF2-L1】の射程**に本稿の K5-W6-L1 を含めるか、別立てにするかの判断(§7.5)。**K5-L1 ②は取り下げ提案。**
7. **DF-W6-2($K^{(20)}$)を較正資産として台帳に登録**することを提案 — **新しい実測を要しない外部 anchor** である。

### 7.7 Sol への監査依頼(優先順)

1. ★★ **補題 GAMMA (a)(b)(c)** — とくに **(4.7) の第 3 座標の反転**から $(\theta\tau)$ が位数 4 になること、および $\Gamma\vert_A\cong S_4$ が addendum §A.7 (E) の $\bar G\cong S_4$ と**同一の $S_4$** であること。**ここが本稿の全体重を支えている**(危険箇所 D-1/D-2)。
2. ★★ **定理 W6-OBS (C)** — 双対を取って $\operatorname{coker}\cong((V^\ast)^\Gamma)^\ast$ に潰す 3 行。前件 $p\nmid6$ の使い方に穴はないか。
3. ★★ **定理 W6-NULL5** — 「初等アーベル 5 核は全滅」。とくに **K5-ENT-INSUF($K^{(25)}$ で $d=5$)との整合が偶然でないこと**の読み。
4. ★ **【K5-GAP-W1】(補題 TWIST の $\theta_\ast^2=\mathrm{id}$)** — 当方が骨格しか書けなかった箇所。**level 5 での $f_1$ の解であることから出るはず**という当方の見立ては妥当か。
5. ★ **補題 CLASS-TRIV** — (d) の $B_3$-同変な補群からの持上げが $\widetilde m=0$ の解を与える、という一行(【K5-GAP-W2】)。
6. **補題 SURJ-W6** — 「既約 + 非分裂 ⟹ $V\subseteq\Phi(P_N)$ ⟹ SURJ 自動 ⟹ **識別力ゼロ**」。系 H8′ の相対版として妥当か。
7. **§1.2 の論理の向き** — 「$\widetilde m=0$ で可解 ⟹ $d_N=5$」の一方向しか使っていないという当方の依存申告に穴はないか。

---

## 8. 検算(**証明とは独立・single lane python**)

**script**: `scratchpad/k5_w6_norm_obstruction_check.py`
**SHA-256**: `d8b41a77fc35ff65b7818000112c9ba4d1f2a73bed154e48621d807a112426f4`
**Python 3.13.14 / FAILS = 0**

| # | 検査 | 実測 | 使う場所 |
|---|---|---|---|
| **A** | (4.7)(4.8) で $\theta^2=\tau^3=I$、$(\theta\tau)^2\ne I$、$(\theta\tau)^4=I$、$\lvert\langle\theta,\tau\rangle\rvert=24$($p=3,5,7,11$) | 一致 | ★ **補題 GAMMA (a)(b)**・**P-W6-4** |
| **B** | 28 モジュール(4 標数 × 7 型)で余核の **3 式**(master / $p\ne2$ 版 / $p\ne3$ 版)が一致 | 一致 | ★ **定理 W6-OBS (A)(B)(B′)**。**$p=2$ で (B) が破れること**も前件明示の上で確認(6 件を gate) |
| **C** | $p=5,7$ の全 case で $\dim\operatorname{coker}=\dim(V^\ast)^\Gamma$ | 一致 | ★ **定理 W6-OBS (C)** |
| **D** | $A$ 型(= $\mathrm{std}_3\otimes\mathrm{sgn}$)・$A\otimes\mathrm{sgn}$・$\mathrm{std}_3$ over $\mathbb F_5$ で $\operatorname{coker}=0$;自明加群で $=1$ | 一致 | ★★ **定理 W6-NULL5**・**P-W6-1/2** |
| **E** | $\mathrm{std}_3$ / $\mathrm{std}_3\otimes\mathrm{sgn}$ / $A$ 模型 over $\mathbb F_3$ で $\operatorname{coker}=0$ | 一致 | ★★ **§3.2 の WARN-13500 判定**・**P-W6-3** |
| **F** | $p=3$ で $\tau$ が 2×2 unipotent の 2 次元加群: $\operatorname{coker}=1$($\ne0$ の型が**実在**);$\mathbb F_3[C_3]$ 正則 + 座標転置: $\operatorname{coker}=1$ | 一致 | ★ **§3.3 生存表**・**DF-W6-1 の実在性** |
| **G** | $p=2$ で $\theta$ が unipotent: $\operatorname{coker}=1$ | 一致 | ★ **§3.4 の第一標的の根拠** |

> **格**: **single lane(python)**。**cross-checked ではない・Lean 検証ではない。** 証明書は 1 本も読んでいない・$\mathrm{Im}\,R_{N,K^{(5)}}$ は一度も測っていない・shadow の値に触れていない。
> ⚠ **検査 B の $p=2$ 行の 6 件**は「短縮式の前件が本質的」であることの**肯定的な証拠**として扱う(バグではない)。

---

## 付録 A. 記号早見(本稿固有)

| 記号 | 意味 |
|---|---|
| $\Gamma$ | $\langle\theta,\tau\rangle\subseteq\mathrm{Aut}(F_2)$。$A$ 上では $\cong S_4$(位数 24)。**$S_3$ ではない** |
| $V$ | **核** $K^{(5)}_{F_2}/N_{F_2}$(addendum の $V=G_5/A$ とは別 — §6.1 N-6) |
| $Q$ | $G_5/A\cong C_2^2$(campaign の記法) |
| $P_N,\ A_N$ | $F_2/N_{F_2}$、$[P_N,P_N]$ |
| $N_\theta,\ N_\tau$ | $b\mapsto b+\theta b$、$b\mapsto b+\tau b+\tau^2b$ |
| $\psi_V$ | $(N_\theta,N_\tau):V\to V^\theta\oplus V^\tau$ — ★ **障害はその余核** |
| $\beta_\theta,\beta_\tau$ | $\widetilde f_0\theta(\widetilde f_0)$、$\tau^2(\widetilde f_0)\tau(\widetilde f_0)\widetilde f_0$ — 障害コサイクル |
| $\mathrm{std}_3$ | $S_4$ の標準 3 次元既約。$\mathrm{sgn}$ = 符号指標(**「ε bits」とは無関係**) |
