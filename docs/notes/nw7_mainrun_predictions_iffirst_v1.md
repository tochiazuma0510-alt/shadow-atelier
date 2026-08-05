# NW(7) 悉皆本走(705,894 対)— **事前予言票 v1(IF-FIRST 凍結)**

**状態札: `candidate(事前予言票・紙のみ / 機械実行は付録 A の 20 行算術のみ / 本走宇宙の候補評価ゼロ / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05
- 委嘱: 司令塔「`docs/notes/exploration_queue_candidates_v1.md` の **札 P-1【EXQ-CF7】**を IF-FIRST 凍結票として正式起草せよ」
- **別 registry**: 本票は本走事前登録票 `docs/notes/hsp7_mainrun_prereg_v2.md`(+ v1・付録 C)とは**別の登録**である。prereg は「宇宙・述語・停止規則」の凍結、**本票は「結果の形の予言」の凍結**。両者の digest は互いに独立に pin する。
- 入力正本(すべて既在・本票は 1 バイトも改変しない): `docs/notes/hs_prop7_translation_v1.md`(§2・§8・§9)/ 同 `_addendum_nwp8_v1.md` / `docs/notes/auto_settled_check_v1.md`(+ v1.1 addendum)/ `docs/week1-定義ノート.md` §2 / `docs/week3-狩場計画_v2.md` §2.1(系 H8′)/ `sol/sol_reply_105_math32.md`(F105-3.3)

---

## 0. 票の性格と拘束(先に 5 行)

| # | 拘束 |
|---|---|
| **0-1** | ★ **本票は 705,894 対の候補を 1 件も評価していない。** 記載の数値はすべて**紙の導出**か、**発火条件 2 で既に確定し Sol が PASS した窓パラメータ**(§1.2)からの算術である。**これが IF-FIRST の意味である。** |
| **0-2** | 本票は**本走の再 gate 通過より前に単独コミットされねばならない**(裁定 543 恒久規則)。§9 に注記を再掲。 |
| **0-3** | 予言は **EXQ-1〜EXQ-9** の 9 本。各々に**格**(定理の帰結 / 定理級・前件つき / 予想)と**登録済み分岐**を付す。分岐は**発火前に**登録されているので、分岐のもう一方に落ちても事後緩和ではない。 |
| **0-4** | ★ **「定理の帰結」に分類した予言は、的中しても情報量ゼロである**(§8.7.6 の SURJ 事故の教訓・S-W6-3 の趣旨)。それらは**予言ではなく実装バグ検出器**として運用する(§7)。 |
| **0-5** | 本票は**新しい停止規則を発効させない**。§7.4 に **S-EXQ-1/S-EXQ-2 を提案**として書くが、発効は司令塔裁定 + Sol ゲート。 |

---

## 1. 宇宙(凍結済みの再掲・**再測定しない**)

### 1.1 窓対(定義 NW(7)・翻訳ノート §8.7.3)

$$\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\qquad \mathbf N_0=\mathcal V(F_2)\times\langle c^{7}\rangle,\qquad N_{F_2}=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,7},$$
$$W=\gamma_5(K(0,5))K(0,5)^{\,7},\qquad P=F_2/N_{F_2},\qquad Q=K(0,5)/W.$$

### 1.2 発火条件 2 で確定済みの値(**本票の入力・再測定しない**)

| 量 | 値 | 出所 |
|---|---|---|
| $\lvert P\rvert$ | $7^8=5{,}764{,}801$ | NW-P2 実測(cert `search/certs/hsp7_cond2_p7_20260804.json`・翻訳ノート §9.6 で Sol PASS) |
| $\lvert[P,P]\rvert$ | $7^6=117{,}649$ | 同上 |
| $N_{\rm ord}$ | $7$ | 同上(紙: 補題 NW-1b (4)) |
| $\lvert\mathcal X_{\mathbf N}\rvert$ | $6$ | 同上 |
| $\dim_{\mathbb F_7}\gamma_4(P)$ | $3$、かつ $h_4\ne1$ | NW-P3 実測 |
| $\eta:=\nu_4(j\mathfrak h_4)\in\gamma_4(Q)$ | $\ne0$ | ★ **NW-P5 実測**(発火条件 2 の本体) |
| 候補宇宙 | $6\times117{,}649=705{,}894$ | prereg v1 §1.2 |

> ⚠ **これらは「窓のパラメータ」であって「候補の評価結果」ではない。** 本票がこれらを使うことは IF-FIRST に抵触しない(prereg v2 §1.1 が「本走はこの値を再登録するのみで再測定しない」と既に凍結している)。

### 1.3 記号(本票で導入・以後固定)

- $u:=2m+1\in(\mathbb Z/7)^\times$、$\chi_{\rm vir}([m,\bar f])=u$(定義ノート §2「virtual cyclotomic character の有限版」)。
- $\mathrm{hex}(m):=\{\bar f\in[P,P]\ :\ [m,\bar f]\ \text{が hexagon を満たす}\}$。
- $\mathrm{pent}(m):=\{\bar f\in\mathrm{hex}(m)\ :\ \mathrm{PENT}_W([m,\bar f])\}$。
- ★ **PENT 欠陥写像** $\;D:[P,P]\to Q,\quad D(\bar f):=\bar\rho^4(j\bar f)\,\bar\rho^3(j\bar f)\,\bar\rho^2(j\bar f)\,\bar\rho(j\bar f)\,j\bar f$。
  $\mathrm{PENT}_W\iff D(\bar f)=1$。**$D$ は $m$ に依らない**(補題 HSP-WD の注)。
- $\mathfrak h_3=u_1+u_2$、$\mathfrak h_4=v_1+4v_2+v_3$、$h_3,h_4$ は対応する**群元**(定義 DUM-FIN・規約台帳 §1.3.10 の Lie/群の別を維持)。

---

## 2. 予言の土台(**引用と自前導出の分離**)

### 2.1 引用する既在の結果(本票は再証明しない)

| 札 | 内容 | 格(既在) |
|---|---|---|
| **ISO-V** | 補題 **VERBAL-ISO**: $N_{F_2}$ が完全不変 ⟹ $N$ は isolated(全 shadow が settled) | ★ Sol **F105-3.3 で「paper theorem」として受理**。$\mathbf N$ への適用は `auto_settled_check_v1.md` §3.5(逐語: $\mathcal V(F_2)$ は verbal) |
| **GRP** | isolated ⟹ $\mathrm{GT}(N)=\mathrm{GTSh}(N,N)$ は**有限群**。合成 (3.53)、$2m+1$ は乗法的 (3.49)、単位 $(0,1)$ | 正典 Thm 3.10(定義ノート §2・画像照合済) |
| **H8′** | $P$ が $p$ 群・$\bar f\in[P,P]\subseteq\Phi(P)$・$\gcd(u,p)=1$ ⟹ **SURJ 自動** | 既在(`week3-狩場計画_v2.md` §2.1)。翻訳ノート §8.7.6 が本窓族への適用と**識別力ゼロ**を記帳。Sol F101-1.3 が理由づけ訂正を全面採択 |
| **D3-B** | 定理 **D3-BLIND**: (a) $\ker(\nu_3|_{\mathrm{gr}_3})=\mathbb Q\mathfrak h_3$、(b) hexagon の深さ 3 は $a=b$ | paper-proof((b))+ 計算 candidate((a)) |
| **D4-P** | 定理 **D4-POWER** (a): hexagon の深さ 4 斉次解空間 $=\mathbb F\mathfrak h_4$(1 次元)、(b) $\nu_4|_{\mathrm{gr}_4}$ 単射 | 有限線型計算 candidate(2 素数一致)。**PREC-1** で $(1+\tau_*+\tau_*^2)(\alpha,\beta,\gamma)=(2\alpha-\beta+2\gamma)(v_1{+}v_2{+}v_3)$ と精確化済 |
| **DUM** | 定理 **DUM-1/p** + 補題 **DUM-HEX**: $f_t=h_4^{\,t}$ は hexagon を **$P$ の中の等式として exact に**満たし、$\mathrm{PENT}\iff t\eta=0$ | paper-proof candidate(NW-P5 相対) |
| **C2-F** | $c_2=m(m+1)/6$(C2-FIN・翻訳ノート §2.3 (d) が引用) | 既在 |
| **SOUND** | 命題 **HSP-SOUND**: $\mathrm{PENT}_W$ が偽 ⟹ $\widehat{GT}$ への持ち上げは存在しない(**片側健全**・真なら何も言わない) | paper-proof |
| **GEN** | genuine(Def 4.2)= $\widehat{GT}_{gen}$ の元の射影。Thm 5.2: $\widehat{GT}_{gen}\cong\varprojlim$(isolated poset 上の $N\mapsto\mathrm{GT}(N)$)。arithmetical ⟹ genuine ⟹ charming | 正典 |
| **GEN-AB** | charming の生成判定は abelian 成分しか識別しない($G_n$ 族での言明) | candidate。★ **本票では射程外**(下記 ⚠) |

> ⚠ **GEN-AB の扱い**: 命題 GEN-AB は $P=G_n$(dihedral 商)についての言明であり、**NW 窓($P$ は $p$ 群)には直接適用しない**。NW 窓で SURJ が自動になる根拠は **H8′(Frattini)**であって GEN-AB ではない。両者は「**SURJ の識別力がどこに集中するか**」という同じ問いへの、**別の窓族での**回答である。本票は H8′ のみを根拠に使い、GEN-AB は**対比のためだけ**に §6.3 で引く。

> ⚠ **系 D4-PRED は使わない**。翻訳ノート §8.3.1 R-1 で**撤回済**(「offset がその直線に入る証明がない」)。本票の $1/7$ 型の主張は **D4-PRED の再利用ではなく、§3 の群構造から独立に導く**。

### 2.2 ★ 本票が自前で導く構造補題(4 本)

> ### 補題 **LAY-1**(層は coset・層別個数は一様)
> $\mathbf N$ は isolated(ISO-V)ゆえ $\mathrm{GT}(\mathbf N)$ は有限群(GRP)。本走宇宙 $\mathcal X_{\mathbf N}\times[P,P]$ の上では
> $$\text{hexagon}\ \iff\ \text{GT-shadow}$$
> である(charming は宇宙の定義から自動、SURJ は H8′ で自動)。$\chi_{\rm vir}$ は (3.49) より群準同型 $\mathrm{GT}(\mathbf N)\to(\mathbb Z/7)^\times$ で、その fiber がちょうど層 $\mathrm{hex}(m)$ である。ゆえに
> $$U:=\{u:\mathrm{hex}(m)\ne\emptyset\}\ \le\ (\mathbb Z/7)^\times\ \textbf{は部分群},\qquad
> \lvert\mathrm{hex}(m)\rvert=\lvert A\rvert\ (\forall u\in U),\quad A:=\ker\chi_{\rm vir}=\mathrm{hex}(0).$$
> **∎**(準同型の fiber は kernel の coset)

> ### 補題 **LAY-2**($\pm1\in U$ — 明示元 2 個)
> $\bar f=1$ は (3.10) を自明に満たし、(3.11) は $x^m z^m y^m=1$($z=(xy)^{-1}$)に帰着する。
> - $m=0$: 自明に $1$。⟹ $[0,1]$ は単位元(GRP)。
> - $m=-1$($=6\bmod7$、$u=-1$): $x^{-1}z^{-1}y^{-1}=x^{-1}(xy)y^{-1}=1$ — **$F_2$ の中の exact な等式**。
>
> ゆえに $\{\pm1\}\subseteq U$、したがって $\lvert U\rvert\in\{2,6\}$。**∎**

> ### 補題 **LAY-3**($A$ は $\gamma_3(P)$ の**部分群**で、初等アーベル)
> **(i)** $m=0$ では $c_2=0$(C2-F)ゆえ $A\subseteq\gamma_3(P)$。
> **(ii)** $u_1=u_2=1$ の合成 (3.53) は $f_{12}=f_1\cdot f_2(x,f_1^{-1}yf_1)$。$f_1\in\gamma_3(P)$ ゆえ $f_1^{-1}yf_1=y[y,f_1]$、$[y,f_1]\in[\gamma_1,\gamma_3]\subseteq\gamma_4$。$f_2\in\gamma_3$ は重さ $\ge3$ の交換子の積で、その 1 引数を $\gamma_4$ でずらすと差は $[\gamma_2,\gamma_4]\subseteq\gamma_6(P)=1$。ゆえに $f_2(x,f_1^{-1}yf_1)=f_2(x,y)$ で、**$A$ の上では GT 合成 $=$ $P$ の積**。
> **(iii)** よって $A\le\gamma_3(P)$ は部分群。$P$ は指数 7 ゆえ $A$ は**指数 7 の初等アーベル群**。**∎**

> ### 補題 **LAY-4**($\lvert A\rvert\in\{7,49\}$ — 中間値の排除)
> 射影 $\pi_3:A\to\mathrm{gr}_3(P)=\gamma_3/\gamma_4$ は LAY-3 (ii) より**群準同型**。
> - **像**: $\bar f\in A$ の深さ 3 斉次類は深さ 3 の hexagon 方程式($c_2=0$ ゆえ低次からの寄与なし)を満たす ⟹ **D3-B (b)** より $\mathrm{im}(\pi_3)\subseteq\mathbb F_7\mathfrak h_3$。部分群ゆえ $\mathrm{im}(\pi_3)\in\{0,\ \mathbb F_7\mathfrak h_3\}$。
> - **核**: $\ker\pi_3=\{\bar f\in\gamma_4(P):\text{hexagon}\}$。$\gamma_4(P)$ は中心・初等アーベルで $\theta,\tau$ はそこで次数付き作用そのもの(**DUM-HEX** の証明)ゆえ、解集合は深さ 4 の斉次核 $=\mathbb F_7\mathfrak h_4$(**D4-P (a)**)。すなわち $\ker\pi_3=\langle h_4\rangle$、位数 **7**。
>
> ゆえに $\lvert A\rvert=7\cdot\lvert\mathrm{im}(\pi_3)\rvert\in\{7,\ 49\}$。**中間値 $14,21,28,35,42$ は排除される。∎**

> ### ★ 補題 **PENT-HOM**($D$ は $A$ 上で準同型・PENT 通過集合は部分群)
> $Q$ は類 $\le4$ ゆえ $[\gamma_2(Q),\gamma_3(Q)]\subseteq\gamma_5(Q)=1$、とくに $\gamma_3(Q)$ はアーベルかつ $\gamma_2(Q)$ と可換。$j:P\to Q$ は準同型で $j(\gamma_3(P))\subseteq\gamma_3(Q)$、$\bar\rho$ は $\gamma_3(Q)$ を保つ。ゆえに $\gamma_3(P)$ 上で
> $$D(\bar f\bar g)=\prod_i\bar\rho^i(j\bar f\cdot j\bar g)=\Bigl(\prod_i\bar\rho^i(j\bar f)\Bigr)\Bigl(\prod_i\bar\rho^i(j\bar g)\Bigr)=D(\bar f)D(\bar g).$$
> すなわち **$D|_{\gamma_3(P)}$ は準同型**。さらに $A$ 上では深さ 3 成分が $\nu_3(s\mathfrak h_3)=0$(**D3-B (a)**)ゆえ $D(A)\subseteq\gamma_4(Q)$(初等アーベル)。
> $D(h_4)=\eta\ne0$(NW-P5)より $\ker(D|_A)\subsetneq A$、したがって
> $$\lvert\mathrm{pent}(0)\rvert=\lvert\ker(D|_A)\rvert=\frac{\lvert A\rvert}{\lvert\langle\xi,\eta\rangle\rvert},\qquad \xi:=D(g_1)\ (g_1\in A,\ \pi_3(g_1)=\mathfrak h_3).$$
> $\lvert A\rvert=49$ のとき $\lvert\mathrm{pent}(0)\rvert=7\iff\xi\in\mathbb F_7\eta$、そうでなければ $1$。**∎**

---

## 3. ★ 予言 **EXQ-1 〜 EXQ-9**(凍結)

> **表の読み方**: **格 T** = 定理の帰結(前件つき・的中は情報量ゼロ・**バグ検出器**)/ **格 T\*** = 定理級だが前件に candidate を含む / **格 C** = 予想(登録済み分岐あり)。

| ID | 予言 | 値 | 格 | 根拠 |
|---|---|---|---|---|
| **EXQ-1** | 非空層の集合 $U$ は $(\mathbb Z/7)^\times$ の**部分群**で $\{\pm1\}$ を含む | $\lvert U\rvert\in\{2,6\}$ | **T\*** | LAY-1 + LAY-2 |
| **EXQ-1′** | ★ **$U=(\mathbb Z/7)^\times$ 全体 = 6 層すべて非空** | 6 層 | **C**(分岐 B-0) | GEN + Thm 5.2:$\mathbf N$ は isolated ゆえ $\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)$ が在り、$G_{\mathbb Q}\to\widehat{GT}\subseteq\widehat{GT}_{gen}$ と $\chi_{\rm cyc}$ の全射性から $U\supseteq\mathrm{im}(\chi_{\rm cyc}\bmod7)=(\mathbb Z/7)^\times$ |
| **EXQ-2** | ★ **非空層の hexagon 通過数はすべて等しい**($m$ に依らない) | 一様 | **T\*** | LAY-1(fiber = coset) |
| **EXQ-3** | ★★ **各非空層の hexagon 通過数 $=49$** | $\lvert\mathrm{hex}(m)\rvert=49$ | **C**(分岐 B-1) | LAY-4 が $\{7,49\}$ に絞る。$49$ 側の判定基準は §4.1 |
| **EXQ-4** | 本走全体の hexagon 通過総数 $=\lvert\mathrm{GT}(\mathbf N)\rvert$ | **294**($=6\cdot7^2$)。検出比 $294/705{,}894=\mathbf{7^{-4}}=1/2401$ | **C** | EXQ-1′ × EXQ-3 |
| **EXQ-5** | ★ hexagon 解の**深さ 2 座標は層ごとに一意**: $c_2=\dfrac{m(m+1)}{6}=\dfrac{u^2-1}{3}\bmod7$ | $m{=}0{:}0$, $1{:}5$, $2{:}1$, $4{:}1$, $5{:}5$, $6{:}0$ | **T** | C2-F。$(u^2-1)/3$ 形は本票の初等変形(付録 A で機械照合) |
| **EXQ-6** | ★ 群構造: $\ker\chi_{\rm vir}=A\cong C_7\times C_7$(初等アーベル)、$\mathrm{GT}(\mathbf N)\cong C_7^2\rtimes C_6$(Schur–Zassenhaus・$\gcd(6,49)=1$)。$C_6$ の作用は $\mathrm{gr}_3$ 因子に $u\mapsto u^3$、$\mathrm{gr}_4$ 因子に $u\mapsto u^4$ | 位数 294 | **C**(EXQ-3 相対) | LAY-3(初等アーベル)+ LAY-1。作用の指数は $E_{m,f}$ が $\mathrm{gr}_k$ に $u^k$ で効くことから(**導出骨子のみ・§8【EXQ-GAP-2】**) |
| **EXQ-7** | ★★ **各非空層の PENT 通過数 $=7$**(= hexagon 通過の**ちょうど $1/7$**) | $\lvert\mathrm{pent}(m)\rvert=7$ | **C**(分岐 B-2) | PENT-HOM が $\{1,7\}$ に絞る。$7$ 側の判定基準は §4.2 |
| **EXQ-8** | ★★ **hexagon 通過かつ PENT FAIL の件数 $=252$**($=294-42$) | **252** | **C** | EXQ-4 − (EXQ-7×6)。**これが札 F-1【FAKE-PROTOCOL】が想定する「A 型 fake の有限証明書」の予測件数**(§6.3) |
| **EXQ-9** | ★ **SURJ 落ち 0 件 / settled 100%** | 705,894 件で SURJ fail = **0**、hexagon 通過 294 件すべて settled | **T** | SURJ: H8′(全 charming が通る=**識別力ゼロ**)。settled: ISO-V($\mathbf N$ は isolated) |

### 3.1 総括表(予言される分布表の形)

| 層 $m$ | $u=2m+1$ | 予言 $c_2$ | 予言 $\lvert\mathrm{hex}(m)\rvert$ | 予言 $\lvert\mathrm{pent}(m)\rvert$ | 予言 hexagon-only |
|---|---|---|---|---|---|
| 0 | 1 | 0 | 49 | 7 | 42 |
| 1 | 3 | 5 | 49 | 7 | 42 |
| 2 | 5 | 1 | 49 | 7 | 42 |
| 4 | 2 | 1 | 49 | 7 | 42 |
| 5 | 4 | 5 | 49 | 7 | 42 |
| 6 | 6 | 0 | 49 | 7 | 42 |
| **計** | — | — | **294** | **42** | **252** |

**残り $705{,}894-294=705{,}600$ 件は hexagon FAIL**(= GT-shadow ですらない)。

---

## 4. ★ 分岐の登録(**発火前に登録する = 事後緩和ではない**)

### 4.1 分岐 **B-1**($\lvert A\rvert$ = 49 か 7 か)

> **判定基準(紙で閉じられる)**: $\lvert A\rvert=49\iff$ **$\mathfrak h_3$ 方向が exact な hexagon 解へ持ち上がる**。$P$ は類 $4<p=7$ ゆえ **Lazard 対応**が有効で、$\log$ を取って次数 4 の方程式を書くと:
> - (3.10) の深さ 4: $\theta$ は次数付きゆえ $(1+\theta_*)F_4=0$、すなわち $\alpha=\gamma$。
> - (3.11) の深さ 4: $\tau$ は**次数付きでない**ので、$\mathfrak h_3$ が次数 4 へ落とす項 $\Psi$ が入り
>   $$(1+\tau_*+\tau_*^2)F_4+\Psi=0,\qquad \Psi:=\bigl[(\tau_\bullet+\tau_\bullet^2)(\mathfrak h_3)\bigr]_{\deg 4}\in\mathrm{gr}_4(F_2)\otimes\mathbb F_7 .$$
> - **PREC-1** より $(1+\tau_*+\tau_*^2)$ の像は直線 $\mathbb F_7(v_1{+}v_2{+}v_3)$ で、$\{\alpha=\gamma\}$ 上でも $(4\alpha-\beta)$ が $\mathbb F_7$ 全体を走るので像は**その直線ちょうど**。
>
> $$\boxed{\ \lvert A\rvert=49\iff\Psi\in\mathbb F_7\,(v_1+v_2+v_3);\qquad \text{さもなくば }\lvert A\rvert=7.\ }$$

| 分岐 | 内容 | 予言される分布 |
|---|---|---|
| ★ **B-1a(本票の予言)** | $\lvert A\rvert=49$ | §3.1 の表 |
| **B-1b(登録済み代替)** | $\lvert A\rvert=7$ ⟹ $\mathrm{hex}(m)=\langle h_4\rangle$ の coset・**hexagon 総数 42**・**PENT 総数 6**(各層 1 = 恒等方向のみ)・hexagon-only **36** | 全数を 1/7 に縮小した表 |

> ★ **B-1 は本走を待たずに閉じられる**(§5)。閉じれば EXQ-3 は格 **C → T\*** へ上がり、本走は純粋な検証になる。

### 4.2 分岐 **B-2**(PENT 通過が層あたり 7 か 1 か)

> **判定基準**: PENT-HOM より
> $$\boxed{\ \lvert\mathrm{pent}(m)\rvert=7\iff\xi\in\mathbb F_7\,\eta\quad(\xi=D(g_1),\ \eta=\nu_4(j\mathfrak h_4)\ne0).\ }$$
> $\xi$ は **$Q$ 側の 1 点計算**であり、NW-P5($\eta\ne0$ の確認)と**同じ性格・同じ装置**で測れる。**705,894 の候補宇宙には触れない**。

| 分岐 | 内容 | 予言 |
|---|---|---|
| ★ **B-2a(本票の予言)** | $\xi\in\mathbb F_7\eta$ ⟹ 層あたり PENT 通過 **7**、総数 42 | §3.1 の表 |
| **B-2b(登録済み代替)** | $\xi\notin\mathbb F_7\eta$ ⟹ 層あたり **1**、総数 **6**、hexagon-only **288** | 検出比がさらに 1/7 |

> **どちらの分岐でも各層は非空**である: 各層は genuine な shadow を含み(EXQ-1′ の根拠)、genuine は $\widehat{GT}$ 由来なら (III) を満たすので **HSP-SOUND の対偶で PENT を通る**。⟹ **$\lvert\mathrm{pent}(m)\rvert\ge1$ は分岐に依らない**。

### 4.3 分岐 **B-0**($U$ が 6 層か 2 層か)

| 分岐 | 内容 |
|---|---|
| ★ **B-0a(本票の予言)** | $U=(\mathbb Z/7)^\times$、6 層すべて非空 |
| **B-0b(登録済み代替)** | $U=\{\pm1\}$、非空は $m\in\{0,6\}$ の **2 層のみ**。⟹ hexagon 総数は EXQ-3 の値 $\times2$ |

> ⚠ **B-0b は $\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)$ の $\chi$-全射性が崩れることを意味する** — それは正典 Thm 5.2 / arithmetical の枠組みに対する**重い異常**なので、まず実装を疑う(§7.2 甲類扱い)。

---

## 5. ★ 本走を待たずに閉じられる 2 点(**司令塔への提案**)

| # | 量 | 何を計算するか | 本走宇宙への接触 | 効果 |
|---|---|---|---|---|
| **PRE-1** | $\Psi=[(\tau_\bullet+\tau_\bullet^2)\mathfrak h_3]_{\deg4}$ | rank 2 自由 Lie 環の次数 4 までの有理/$\mathbb F_7$ 線型代数。既存 `search/probe/hsp7_v1/hs_prop7_hexagon_vs_pentagon.py` の**非斉次拡張**(次数 3 の元に $\tau$ を filtered に効かせ、次数 4 成分を取る) | ★ **ゼロ**(窓も候補も出てこない) | **B-1 が閉じる** ⟹ EXQ-3/4/6/8 が予想 → 定理級 |
| **PRE-2** | $\xi=D(g_1)$ の $\eta$ との比例判定 | $Q$(pc 群・$7^{40}$)上で $g_1$ の像に $D$ を 1 回適用し、$\eta$ との $\mathbb F_7$-従属性を見る。**候補の列挙をしない 1 点計算**(NW-P5 と同型の作業) | ★ **ゼロ**(705,894 の候補評価ではない) | **B-2 が閉じる** ⟹ EXQ-7/8 が予想 → 定理級 |

> ### ★ なぜこれを勧めるか(DUM-G3 規律)
> 「**検出力を走らせる前に見積る**」が本設計の一貫した規律である。PRE-1/PRE-2 が閉じれば、**本走は「未知を測る」ではなく「予言済みの分布を確認する」**作業になり、
> - 不一致 = **実装バグの検出**(数学の新事実ではない)という**逆向き運用**が全予言に適用でき、
> - 「識別力ゼロの検査を通ったと数える」事故(§8.7.6 の SURJ 事故)の再発余地が消える。
>
> ⚠ **ただし PRE-1/PRE-2 は本票の発効条件ではない。** 閉じないまま本走しても、本票は分岐形で採点可能である(それが §4 を先に書いた理由)。

---

## 6. 予言が「当たった」場合に何が言えるか(**過大評価の防止**)

### 6.1 言えること

| 予言 | 的中したとき言えること |
|---|---|
| EXQ-5(層別 $c_2$)・EXQ-9(SURJ 0 / settled 100%) | ★ **何も新しくは言えない**(定理の帰結)。**装置が壊れていない**ことだけ |
| EXQ-2(層一様性)・EXQ-1(部分群性) | 同上(LAY-1 の帰結)。**ただし ISO-V が本窓で実効していることの実測的裏づけ**にはなる(前件 = $\mathcal V(F_2)$ の verbal 性) |
| EXQ-3/4/6(hexagon 総数と群構造) | ★ **$\mathrm{GT}(\mathbf N)$ の位数と構造の確定**。これは**新しい在庫**(NW 族で初の $\mathrm{GT}(N)$ 完全決定) |
| EXQ-7/8(PENT の 1/7 と 252 件) | ★ **PENT 検査が有限窓で実際に識別力を持つことの実証**(D4-POWER の有限窓版)。**撤回された D4-PRED の、正しい形での回収** |

### 6.2 言えないこと(★ 明示的に禁じる)

1. 「**$\mathrm{GT}(\mathbf N)$ の 294 個のうち 42 個が genuine**」— **言えない**。PENT 通過は片側健全(SOUND)であり、**真の場合は何も結論しない**。42 は「**$\widehat{GT}$ への持ち上げが深さ 5 の窓で否定されなかった**」件数にすぎない。
2. 「**252 個は fake**」— **言えない**(Def 4.2 の意味では)。言えるのは「**$\widehat{GT}$(pentagon つき本来の GT)へは持ち上がらない**」までで、$\widehat{GT}_{gen}$ への持ち上げは否定されない。**U-10($\widehat{GT}=\widehat{GT}_{gen}$)が open** である限り、正しい呼称は札 F-1 の言う **A 型 fake**(= ĜT へ持ち上がらない gentle shadow)である。
3. 「**dihedral 予想に効いた**」— **言えない**。$\mathbf N$ は dihedral 族ではない。
4. `cross-checked` / `verified` — **付かない**。本票は単系統・紙のみ。本走が出す値も、CV-9 判読を経ない限り cross-checked にはならない。

### 6.3 対比(★ H8′ と GEN-AB — **同じ問いへの別窓族の回答**)

| 窓族 | SURJ の識別力 | 根拠 |
|---|---|---|
| **NW(7)**($P$ = 類 4・指数 7 の $p$ 群) | ★ **厳密ゼロ**(全 charming 候補が通る) | **H8′**(Frattini: $[P,P]\subseteq\Phi(P)$) |
| **dihedral $K^{(n)}$**($P=G_n$、$\lvert G_n\rvert=4n^3$) | abelian 成分では常に自明、**識別力は $A=[P,P]$ の内部だけ** | **GEN-AB**(candidate) |

⟹ **どちらの族でも「SURJ を通った」は成果として数えない。** NW では判定の実体は **hexagon と PENT だけ**である(翻訳ノート §8.7.6 の発注仕様一行)。

---

## 7. ★★ 予言が外れた場合の解釈規約(**逆向き運用**)

### 7.1 大原則(3 行)

$$\boxed{\ \textbf{① 同一 run・同一登録の中で予言を書き換えない(S-7′)。}\quad
\textbf{② 外れの意味は「格」で決まる。}\quad
\textbf{③ 登録済み分岐への着地は「外れ」ではなく「分岐の決着」。}\ }$$

### 7.2 格ごとの解釈(★ これが本節の本体)

| 類 | 対象 | 外れたときの**一次解釈** | 手続き |
|---|---|---|---|
| ★ **甲(格 T)** | **EXQ-5**(層別 $c_2$)・**EXQ-9**(SURJ 0 / settled 100%) | ★ **実装バグを第一に疑う。** これらは前件が実測済み(NW-P2/P3)の**定理の帰結**であり、数学的な新発見として読まない | **IMPLEMENTATION_BUG_SUSPECTED / STOP**。①候補座標を封印(研究者へ座標を見せない)②独立第二系統で当該候補のみ再評価 ③較正 18 fixture の再走 ④Sol 即報(札 F-1 の protocol を援用) |
| **乙(格 T\*)** | **EXQ-1**(部分群性)・**EXQ-2**(層一様性) | ★ **二段階**: (i) まず実装(層の割付・key 全単射・m の篩)を疑う。(ii) 実装が潔白なら、**前件のどれが崩れたかを特定**する — 候補は「$\mathcal V(F_2)$ の verbal 性(ISO-V の前件)」「$\mathbf N$ の isolated 性」「合成 (3.53) の実装忠実性」「宇宙が GT-shadow 全体と一致するか(charming/SURJ の読み)」 | **LANE/PREREG 整合検査** → 特定できなければ **PREREGISTRATION_FALSIFIED / INTEGRITY_STOP**。★ **ISO-V が崩れるなら AS-GAP-6(真の non-isolated witness)の実物が出たことになり、それ自体が一級の発見** — 封印して別 gate へ |
| **丙(格 C・登録済み分岐へ着地)** | EXQ-1′→B-0b、EXQ-3→B-1b、EXQ-7→B-2b | ★ **「外れ」と記録しない。「分岐 B-xb で決着」と記録する。** 分岐は発火前に登録済みなので事後緩和ではない | 採点欄に `branch_resolved: B-1b` 等を記録。**同じ run の中で他の予言を書き換えない**(B-1b なら EXQ-4/6/8 の値も B-1b 版へ**自動的に**移る — これは書き換えではなく**登録済みの従属値**) |
| ★ **丁(格 C・登録した分岐のどれでもない)** | 例: $\lvert\mathrm{hex}(m)\rvert\in\{14,21,28,35,42\}$、層ごとに個数が違う、$\lvert\mathrm{pent}(m)\rvert\notin\{1,7\}$ | ★ **PREREGISTRATION_FALSIFIED。即時停止。** LAY-1〜LAY-4 / PENT-HOM のどれかが偽であり、**紙の構造補題に穴がある** | 残りの測定へ進まない。部分結果は破棄せず保存。**旧予言が外れた事実と本票の digest を明記した別 version の事前登録から再開**(S-7′ 正本の手続きをそのまま適用) |

### 7.3 ★ 「検出器としての逆向き運用」の明文化

> **甲類の予言は、的中を成果として報告しない。** 的中は「装置が壊れていない」という**負の情報**であり、S-8′ が「不一致こそが実装バグの証拠」と定めたのと**同じ向き**である。
> ⟹ 本走 cert の集計欄では、**甲類は `detector` 欄**に、**丙類(格 C)は `prediction` 欄**に分けて記録すること。**同じ表に混ぜて「予言 n/n 的中」と数えない。**(§8.7.6 の SURJ 事故 = 識別力ゼロの検査を「通った」と数えた事故の、予言側での再発防止。)

### 7.4 停止規則の**提案**(発効は司令塔裁定 + Sol ゲート)

```jsonc
// 提案のみ。本票は発効させない。
"S-EXQ-1": { "trigger": "層ごとの hexagon 通過数が m に依存して異なる、または {7,49} のどちらでもない",
             "verdict": "PREREGISTRATION_FALSIFIED / INTEGRITY_STOP",
             "note": "LAY-1(coset)と LAY-4(中間値排除)の同時反証。紙の構造補題の穴を意味する。丁類。" },
"S-EXQ-2": { "trigger": "SURJ fail が1件でも出る、または hexagon 通過候補に非 settled が1件でも出る",
             "verdict": "IMPLEMENTATION_BUG_SUSPECTED / STOP",
             "note": "H8′ と ISO-V の帰結。甲類 = 検出器。的中側(0件)は成果として数えない。" }
```

> ⚠ **既存の S-3 / S-6 / S-7′ / S-8′ / S-9 は不変**。本票はそれらに触れない。

### 7.5 採点の記録先

- 各予言 ID(EXQ-1〜EXQ-9)ごとに `hit` / `miss` / `branch_resolved` / `not_evaluated` を本走 cert へ記録。
- ★ **統計 v2 予言 (iii)(HS 深さ 4 層)の「未採点」**(F105 §7 末尾)は、**EXQ-7/EXQ-8 の採点をもって初めて採点可能**になる。本票の digest をその採点欄から参照すること。

---

## 8. 格付け・【GAP】・規律申告

### 8.1 格付け

| 対象 | 格 |
|---|---|
| 補題 **LAY-1 / LAY-2 / LAY-3 / LAY-4 / PENT-HOM** | ★ **paper-proof candidate**(本票・**Sol 未監査**・単系統)。前件に既在の candidate(D3-B (a)・D4-P (a)・DUM-HEX・ISO-V)を含む |
| **EXQ-1 / EXQ-2 / EXQ-5 / EXQ-9** | **定理の帰結**(格 T / T\*)。**予言ではなく検出器** |
| **EXQ-1′ / EXQ-3 / EXQ-4 / EXQ-6 / EXQ-7 / EXQ-8** | **予想**(格 C・分岐登録済み) |
| §4 の 2 判定基準($\Psi$・$\xi$) | ★ **paper-proof candidate**(本票)。**基準の値そのものは未計算** |
| `cross-checked` / `verified` | ✗ **どちらも付かない**(本票の機械実行は付録 A の 20 行算術のみ) |
| novelty | **主張しない**(grep 済: `EXQ-`・`LAY-`・`PENT-HOM`・「層別 hexagon 通過数」は既在文書に無いが、**新規性の主張はしない**) |

### 8.2 【GAP】

| 札 | 内容 | 状態 |
|---|---|---|
| ★ **【EXQ-GAP-1】** | **$\Psi$ の値が未計算** ⟹ B-1 未決 ⟹ EXQ-3/4/6/8 は予想のまま | **OPEN**(PRE-1 で閉じられる・本走非接触) |
| ★ **【EXQ-GAP-2】** | **EXQ-6 の $C_6$ 作用の指数($u^3$/$u^4$)は導出骨子のみ**。$E_{m,f}$ が $\mathrm{gr}_k$ に $u^k$ で効くことから来るが、**共役 $[m,f_0]\circ[0,g]\circ[m,f_0]^{-1}$ の $f$-成分を正確に追う一段を書いていない** | **OPEN**(紙 1 枚・本走非接触) |
| ★ **【EXQ-GAP-3】** | **$\xi$ の値が未計算** ⟹ B-2 未決 | **OPEN**(PRE-2 で閉じられる・本走非接触) |
| **【EXQ-GAP-4】** | EXQ-1′ は **$\widehat{GT}_{gen}\to\mathrm{GT}(\mathbf N)$ の存在**(Thm 5.2 + ISO-V)と **$G_{\mathbb Q}\to\widehat{GT}$、$\chi_{\rm cyc}$ 全射**に依存する。後者は**正典の外側の標準事実**(Belyi/Drinfeld/Ihara の枠組み)であり、本票は pin を取っていない | **申告**(分岐 B-0b が保険) |
| **【EXQ-GAP-5】** | LAY-1 の「宇宙上で hexagon $\iff$ GT-shadow」は、**GT-pair の定義に (3.10)(3.11)+charming 以外の条件が無い**という読みに依存する(定義ノート §2・Prop 3.5/3.6) | **要 Sol 確認**(§10 監査点 Q-2) |

> ⚠ **正典外の類推(根拠に数えない・出所ラベル)**: $\mathfrak h_3$ 方向が持ち上がる(B-1a)ことの傍証として、prounipotent 側の $\sigma_3$(次数 3 の GT 元)の存在を連想したが、**これは正典外の背景知識であり、本票は根拠に数えない**。判定は §4.1 の $\Psi$ 基準のみによる。もし $\Psi$ の計算が難航して外部機構が要るなら、そのとき初めて【文献要請】を起票する。**本票では起票しない。**

### 8.3 規律申告

- ★ **本走宇宙(705,894 対)の候補を 1 件も評価していない。** GAP も pc 群も窓も起動していない。機械は付録 A の python 20 行(整数演算のみ)だけである。
- **封印 3 量($n=5$ 関連・$\mathrm{Im}\,R$・$d_N$・$u$ 値)非接触。** $K^{(5)}$ の値・窓データに一切触れていない。
- **外部文献検索ゼロ**(文献ゲート遵守)。**新しい原典頁を開いていない。**
- **既存文書は 1 バイトも改変していない**(本票は新規ファイル)。
- 数値は**すべて機械生成**(付録 A のスクリプト出力を転記・手写しゼロ)。

---

## 9. ★★ 単独コミットの注記(裁定 543 恒久規則)

$$\boxed{\ \textbf{本票は本走の再 gate 通過より}\textbf{前}\textbf{に、}\textbf{単独コミット}\textbf{されるべし。}\ }$$

- **理由**: 他のファイルと同一コミットに入れると、コミット時刻が「本走前」であることの証拠が、同梱物の由来と混ざる。IF-FIRST の事前性は**コミットの単独性と時刻**で担保する。
- **確認手順(発注時)**: 本走発注 cert の `iffirst_registry` 欄に、本票のパス・SHA-256・**単独コミットの hash** を記録し、`git log --name-only <hash>` が本票 1 ファイルのみを示すことを機械確認する。
- **本票の改版**: 発火後に本票を書き換えない。改版が要るなら **v2 を新規に起こし、v1 が外れた事実と v1 の digest を冒頭に明記**する(S-7′ 正本の手続き)。

---

## 10. Sol への監査点(3 点)

> **Q-1 ★★ 補題 LAY-3 (ii)**(§2.2)。「$u_1=u_2=1$ の GT 合成は $\gamma_3(P)$ 上で $P$ の積に一致する」という主張。$f_2\in\gamma_3$ の 1 引数を $\gamma_4$ でずらした差が $[\gamma_2,\gamma_4]\subseteq\gamma_6(P)=1$ に落ちる、という重さ勘定に穴はないか。**ここが「$A$ が初等アーベル $C_7\times C_7$」(EXQ-6)と「$\lvert A\rvert\in\{7,49\}$」(LAY-4)の両方を支えている。**
>
> **Q-2 ★ 補題 LAY-1 の前段**(§2.2)。本走宇宙 $\mathcal X_{\mathbf N}\times[P,P]$ の上で **hexagon $\iff$ GT-shadow** と読んでよいか(charming は宇宙の定義から、SURJ は H8′ から自動)。すなわち **GT-pair の定義に (3.10)(3.11) + charming 以外の条件が無い**という読み(定義ノート §2・Prop 3.5/3.6)の確認。**これが崩れると層 = fiber の等式が壊れ、EXQ-1〜4 が全部倒れる。**
>
> **Q-3 ★ 補題 PENT-HOM**(§2.2)。$[\gamma_2(Q),\gamma_3(Q)]\subseteq\gamma_5(Q)=1$ から「$D$ は $\gamma_3(P)$ 上で準同型」を出した一段と、$D(A)\subseteq\gamma_4(Q)$(深さ 3 成分が $\nu_3(\mathfrak h_3)=0$ で消える)。**および §4.2 の判定基準 $\xi\in\mathbb F_7\eta$ が PENT の $1/7$ の正しい必要十分形になっているか**(撤回された D4-PRED の穴 = 「offset が直線に入る証明がない」を、今度は**群構造で**埋めたという主張の可否)。

---

## 付録 A. 数値の生成(**本走非接触**・整数演算のみ)

以下を実行して得た出力を §3 の表へ転記した。**窓も候補も現れない純粋な算術**である。

```python
p = 7
inv = lambda a: pow(a, p-2, p)
X = [m for m in range(p) if (2*m+1) % p != 0]            # X_N
for m in X:
    u  = (2*m+1) % p
    c2 = (m*(m+1) % p) * inv(6) % p                       # C2-FIN
    assert c2 == ((u*u-1) % p) * inv(3) % p               # (u^2-1)/3 形
U   = 6 * p**6            # 705894
HEX = 6 * 49              # 294   (分岐 B-1a)
PEN = 6 * 7               # 42    (分岐 B-2a)
```

**出力(機械生成)**:

```
X_N = [0, 1, 2, 4, 5, 6]   |X_N| = 6
u=2m+1 : [1, 3, 5, 2, 4, 6]   set==(Z/7)^x : True
m, u, c2=m(m+1)/6, c2=(u^2-1)/3, agree
(0, 1, 0, 0, True)
(1, 3, 5, 5, True)
(2, 5, 1, 1, True)
(4, 2, 1, 1, True)
(5, 4, 5, 5, True)
(6, 6, 0, 0, True)
universe 6*7^6 = 705894   ==705894: True
|[P,P]|=7^6 = 117649  |P|=7^8 = 5764801
hex total(pred) 6*49 = 294   ratio 1/x, x = 2401 = 7^4: True
pent total(pred) 6*7 = 42   hex-only = 252
alt branch A: |hex(m)|=7 -> total 42  pent 6*1= 6
```

> ★ **$c_2$ の 2 通りの閉形式($m(m+1)/6$ と $(u^2-1)/3$)が全 6 層で一致**したことは、C2-FIN の独立再導出(§2.1 C2-F を BCH で手計算し直したもの)との整合点である。⚠ **ただし起草者が同一なので `cross-checked` ではない**(単系統)。
