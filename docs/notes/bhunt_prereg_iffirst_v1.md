# B-HUNT — NW(7) 窓における**算術像の同定**と B 型候補の狩り出し(**IF-FIRST 事前登録票 v1**)

**状態札: `candidate(事前登録票・紙のみ / 機械は付録 A の 40 行整数演算のみ / 候補 key の値を 1 個も列挙していない / 新規窓計算ゼロ / 封印 3 量非接触 / novelty 主張なし / Sol 未監査)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 委嘱: 司令塔(**裁定 572 の帰結**)— 探索新札 **B-HUNT** の前件整理と事前登録票の起草
- 対象窓: $\mathbf N=\mathcal V(F_2)\times\langle c\rangle$(**NW(7)**・翻訳ノート §8.7.3)
- 入力正本(すべて既在・本票は 1 バイトも改変しない):
  `docs/week1-定義ノート.md` §2 / `papers/txt/2405.11725-…txt` §1.3・§1.3.1(式 (1.4)–(1.13))/
  `docs/notes/hs_prop7_translation_v1.md` §1.3(定義 HSP-W/HSP-T・補題 HSP-WD・命題 HSP-SOUND)/
  `docs/notes/nw7_mainrun_predictions_iffirst_v1.md`(**票 v1**・commit `89349a8`)/
  `docs/notes/nw7_predictions_addendum_pentlayer_v1.md`(**addendum A**)/
  `docs/notes/auto_settled_check_v1.md` §3.5(ISO-V の適用)/
  `docs/notes/fake_void_v1.md` §1.1–§1.3(三層と fake の三分)/
  `search/certs/nw7_mainrun_scoring_20260806.json`(**本走 cert**・裁定 572)/
  `docs/notes/conventions_ledger_v1.md` §1.3.9(fake の語)・§1.3.10($\mathfrak h_3/\mathfrak h_4$)

---

## 0. 票の性格と拘束(先に 6 行)

| # | 拘束 |
|---|---|
| **0-1** | 本票は **紙のみ**。GAP も pc 群も起動していない。機械は付録 A の python(整数演算・窓非接触)だけである。 |
| **0-2** | 本票は **42 個の candidate key の値を 1 個も書かない**(cert 参照で足りる)。key を扱うのは §3 の**設計文**としてのみ。 |
| **0-3** | ★ **用語の是正(規約台帳 §1.3.9・裁定 374)**: 委嘱文の「**B 型 fake**」は正式用語では **fake と呼ばない**。正式には **B 型 = genuine だが非算術(= 非算術証人)**。有限窓が証明できるのは**非算術性まで**で genuine 性は有限深度から出ない(掟 2)⟹ 本票の狩る対象は正確には **「hexagon と PENT$_W$ を通るが非算術な元」= B 型候補(非算術証人候補)** である。以後この語を使う。 |
| **0-4** | 予言・分岐はすべて**発火前**に登録する。分岐への着地は「外れ」ではなく「決着」(票 v1 §7.1 の三原則をそのまま継承)。 |
| **0-5** | 本票は**新しい停止規則を発効させない**。§6.4 に提案として書くが発効は司令塔裁定 + Sol ゲート。 |
| **0-6** | 本票の結論はすべて **framework-relative**(前件 = 正典の Ihara 埋め込み・ISO-V・LAY/PENT 補題群)。`cross-checked` も `verified` も付かない。 |

---

## 1. 舞台(**凍結済みの再掲・再測定しない**)

### 1.1 窓と群

$$\mathbf N=\mathcal V(F_2)\times\langle c\rangle,\quad N_{F_2}=\mathcal V(F_2)=\gamma_5(F_2)F_2^{\,7},\quad P=F_2/N_{F_2},\quad N_{\rm ord}=7,\quad \lvert\mathcal X_{\mathbf N}\rvert=6 .$$

$\mathbf N$ は **isolated**(補題 **ISO-V** = VERBAL-ISO・`auto_settled_check_v1.md` §3.5・Sol F105-3.3 で paper theorem 受理)。ゆえに $\mathrm{GT}(\mathbf N)=\mathrm{GTSh}(\mathbf N,\mathbf N)$ は**有限群**(正典 Thm 3.10)。

### 1.2 本走で確定した値(**本票の入力・再測定しない**・出所 = 本走 cert)

| 量 | 値 | 出所(cert 欄) |
|---|---|---|
| hexagon 通過総数 $=\lvert\mathrm{GT}(\mathbf N)\rvert$ | **294** | `measured.hexagon_total_lane_S/V`(S/V 二系統・mismatch 0) |
| 層数(非空)/ 層あたり | **6 / 49** | `measured.nonempty_layers_*`・`hexagon_per_layer_*` |
| $A:=\ker\chi_{\rm vir}=\mathrm{hex}(0)$ | $\lvert A\rvert=49$ | `measured.hex0_size`(分岐 **B-1a** 決着) |
| $\lvert\ker(D\vert_A)\rvert=\lvert\mathrm{pent}(0)\rvert$ | **7** | `measured.pent_within_hex0_m0`(分岐 **B-2a** 決着) |
| $\eta:=\nu_4(j\mathfrak h_4)\neq0$ | 非零 | NW-P5(発火条件 2・`hsp7_cond2_p7_20260804.json`) |

> ⚠ **未測定の限定(cert の正直記帳をそのまま継承)**: 層 $m\ne0$ の PENT 通過数は本走で**独立測定されていない**(lane P の宇宙は $[P,P]$ 全体 = $m=0$ 相当の 117,649 のみ)。総数 42 / hexagon-only 252 は **PENT-LAYER による外挿込み**である。★ **本票 §3.1 (J0) は、この外挿を新規走行なしに測定へ格上げする手順を与える。**
>
> ★ **委嘱文の前提の訂正(申し送り)**: 委嘱は「42 個の candidate key は P lane cert に在中」としたが、**在中しているのは層 0 の 7 key だけ**である(残り 35 key は lane P の宇宙に存在しない)。ただし **$\mathrm{PENT}_W$ が $m$ に依らない**(補題 HSP-WD の注)ため、lane P の PASS 集合は $[P,P]$ 全体の $D^{-1}(1)$(49 元)であり、**lane S/V の層別 hexagon PASS 集合との join で 42 key 全部が復元できる**(§3.1 (J0))。⟹ **欠品ではなく join 待ち**である。

### 1.3 記号(票 v1 §1.3 を継承・本票で追加する分のみ)

- $u:=2m+1=\chi_{\rm vir}([m,\bar f])\in(\mathbb Z/7)^\times$。**この $u$ は封印語彙の「$u$ 値」とは別物**(§4.3 で逐点確認)。
- $D:[P,P]\to Q$、$D(\bar f)=\bar\rho^4(j\bar f)\cdots j\bar f$。$\mathrm{PENT}_W\iff D(\bar f)=1$。**$D$ は $m$ に依らない**(補題 HSP-WD の注: 「$m$ は使わない。$\mathrm{PENT}_W$ は $\bar f$ のみの関数」)。
- $H_W:=\{g\in\mathrm{GT}(\mathbf N):\mathrm{PENT}_W(g)\}$(addendum A §3 の記号)。
- $L:=\ker(D\vert_A)$、$\lvert L\rvert=7$(§1.2)。
- $L_4:=\langle h_4\rangle=A\cap\gamma_4(P)$($h_4$ は**群元**。Lie 元 $\mathfrak h_4$ との同一視は $\gamma_4(P)/\gamma_5(P)=\mathrm{gr}_4(P)$ 経由・規約台帳 §1.3.10 遵守)。
- $L_3:=A$ の中の $u^3$-同型成分(§2.5 で存在と一意性を示す)。**$L_3$ は群の部分群であって Lie 元 $\mathfrak h_3$ ではない**(同上)。
- $\mathfrak G_{\rm ar}:=\mathrm{GT}^{\rm arith}(\mathbf N)=\mathrm{Im}(\mathrm{Ih}_{\mathbf N})$、$\mathfrak G_{\rm pent}:=\mathrm{Im}(\widehat{GT}\to\mathrm{GT}(\mathbf N))$、$\mathfrak G_{\rm gen}:=\mathrm{Im}(\widehat{GT}_{\rm gen}\to\mathrm{GT}(\mathbf N))$(`fake_void_v1.md` §1.1 の鎖)。

---

## 2. ★ 算術供給の正確な形(委嘱 §1)

### 2.1 供給の分解(**4 段・どの段が正典で・どの段が測定か**)

$$G_{\mathbb Q}\ \overset{(a)}{\hookrightarrow}\ \widehat{GT}\ \overset{(b)}{\subseteq}\ \widehat{GT}_{\rm gen}\ \overset{(c)}{\longrightarrow}\ \mathrm{GT}(\mathbf N)\ \overset{(d)}{\longrightarrow}\ (\mathbb Z/7)^\times$$

| 段 | 内容 | 出所と格 |
|---|---|---|
| **(a)** | $\mathrm{Ih}(g)=\bigl((\chi(g)-1)/2,\ f_g\bigr)$ が群準同型 $G_{\mathbb Q}\to\widehat{GT}$ を定め、Belyi により単射 | **正典 2405 (1.5)(1.6)**(原典 Ihara ICM 1990 §2.3 (2.3.1)(2.3.2) — 読解ノート `reading_ihara_icm1990_tb3_v1.md` §3.5 で頁照合済) |
| **(b)** | $\widehat{GT}\subseteq\widehat{GT}_{\rm gen}$ | 正典 2405 §1.3(同 (1.5) が $\widehat{GT}_{\rm gen}$ への単射も定める) |
| **(c)** | $\mathbf N$ が isolated ゆえ $\mathrm{PR}_{\mathbf N}:\widehat{GT}_{\rm gen}\to\mathrm{GT}(\mathbf N)$ は**群準同型**、$\mathrm{Ih}_{\mathbf N}:=\mathrm{PR}_{\mathbf N}\circ\mathrm{Ih}$、$\mathfrak G_{\rm ar}=\mathrm{Ih}_{\mathbf N}(G_{\mathbb Q})$ は**部分群** | **正典 2405 (1.11)(1.12)** + **ISO-V**(本窓の isolated 性) |
| **(d)** | $\chi_{\rm vir,\mathbf N}([m,f])=2m+1$、図式 (1.13) が可換: $\chi_{\rm vir,\mathbf N}\circ\mathrm{Ih}_{\mathbf N}=\widehat P_{7}\circ\chi$ | **正典 2405 (1.9)(1.10)(1.13)** |

> ★ **この 4 段が「算術供給」の全体である。** 本窓に固有の入力は (c) の ISO-V だけで、他は正典の一般論。

### 2.2 補題 **SUP-1**(下界の供給 — mod 7 円分指標の全射性)

> **補題 SUP-1.** $\chi_{\rm vir,\mathbf N}(\mathfrak G_{\rm ar})=(\mathbb Z/7)^\times$。とくに $6\mid\lvert\mathfrak G_{\rm ar}\rvert$ であり、$\mathfrak G_{\rm ar}$ は **6 層すべてと交わる**。
>
> **証明.** (1.13) の可換性より $\chi_{\rm vir,\mathbf N}\circ\mathrm{Ih}_{\mathbf N}=\widehat P_7\circ\chi$。円分指標 $\chi:G_{\mathbb Q}\to\widehat{\mathbb Z}^\times$ は全射(正典 2405 Remark 1.3 が明示的に引く標準事実)、$\widehat P_7:\widehat{\mathbb Z}^\times\to(\mathbb Z/7)^\times$ も全射。合成は全射。∎

> ★ **明示的な算術元が 1 つある**: 複素共役 $\iota$ は $\chi(\iota)=-1,\ f_\iota=1$(Ihara ICM 印字 106 逐語: "When $\sigma$ is the complex conjugation, $\chi(\sigma)=-1$, $f_\sigma=1$")。ゆえに
> $$\boxed{\ \mathbf c:=\mathrm{Ih}_{\mathbf N}(\iota)=[6,\,1]\in\mathfrak G_{\rm ar},\qquad \mathbf c^2=[0,1]=\text{単位元}.\ }$$
> これは票 v1 **LAY-2** が $F_2$ の中の exact な等式として確認した元と**同一**である(独立の裏取り 2 経路)。

### 2.3 補題 **SUP-2**(上界の供給 — pentagon 窓)

> **補題 SUP-2.** $\mathfrak G_{\rm ar}\subseteq\mathfrak G_{\rm pent}\subseteq H_W$。
>
> **証明.** 第 1 の包含は $\mathrm{Ih}$ が $\widehat{GT}$ を経由すること(§2.1 (a)(b))。第 2 の包含は **命題 HSP-SOUND の対偶**: $\widehat{GT}$ の元へ持ち上がるなら (III) が $\widehat{K(0,5)}$ で成立し、$W$ への射影で $\mathrm{PENT}_W$ が真。∎

> ⚠ **片側性の再確認**: HSP-SOUND は「$\mathrm{PENT}_W$ が偽 ⟹ 持ち上げなし」であり、**真の側は何も言わない**。ゆえに $H_W$ は $\mathfrak G_{\rm pent}$ の**上界**にすぎない($H_W\supseteq\mathfrak G_{\rm pent}$ であって等号ではない)。

### 2.4 補題 **SUP-3**($\lvert H_W\rvert=42$ — 外挿の紙の裏づけ)

> **補題 SUP-3.** $\lvert H_W\rvert=6\cdot\lvert L\rvert=42$。
>
> **証明.** SUP-1 より各層 $m$ は算術元を含み、SUP-2 よりその算術元は $\mathrm{PENT}_W$ を通る ⟹ **全 6 層で $\mathrm{pent}(m)\ne\emptyset$**。補題 **PENT-LAYER**(addendum A §3.1)より $\lvert\mathrm{pent}(m)\rvert=\lvert\ker(D\vert_A)\rvert=\lvert L\rvert=7$(§1.2 の測定値)。総和して 42。∎

> ★ **意味**: 本走 cert が「42 は外挿(m≠0 は非独立測定)」と正直に記帳した部分は、**紙では framework-relative に閉じている**(前件 = 正典の算術供給 + PENT-LAYER)。⚠ ただしこれは**測定ではない** — cert の格付けは不変とし、§3.1 (J0) の join でのみ測定へ格上げする。

### 2.5 補題 **SUP-4**($A$ の $C_6$-加群構造と算術像の位置)

> **補題 SUP-4.** $A\cong\mathbb F_7^{\,2}$ 上の共役作用は $A$ 自身を自明に作用させるので $\mathrm{GT}(\mathbf N)/A\cong C_6$ の作用に落ちる(系 **CONJ-Φ**: 共役 $=\Phi=E_{m,f}\vert_{\gamma_3(P)}$)。$\gcd(6,7)=1$ ゆえこの表現は半単純で、合成因子の指標は $\mathrm{gr}_3$ 上 $u\mapsto u^3$、$\mathrm{gr}_4$ 上 $u\mapsto u^4$(EXQ-GAP-2 は addendum A §4 で **graded 水準 CLOSED**)。$u\ne1$ で $u^3\ne u^4$(付録 A・全 5 層で機械確認)ゆえ二指標は相異なり、
> $$A=L_3\oplus L_4\quad(\text{標準分解}),\qquad L_4=A\cap\gamma_4(P)=\langle h_4\rangle,$$
> $C_6$-部分加群はちょうど 4 個: $\{0,\ L_3,\ L_4,\ A\}$(付録 A で機械確認)。
>
> さらに $\mathfrak G_{\rm ar}\cap A$ は $\mathfrak G_{\rm ar}$ で正規、$\mathfrak G_{\rm ar}$ は $C_6$ 全体を覆う(SUP-1)ので **$C_6$-部分加群**である。SUP-2 より $\mathfrak G_{\rm ar}\cap A\subseteq L$。$D(h_4)=\eta\ne0$ ゆえ $L_4\not\subseteq L$、また $\lvert L\rvert=7<49$ ゆえ $A\not\subseteq L$。したがって
> $$\boxed{\ \mathfrak G_{\rm ar}\cap A\in\{1,\ L\},\qquad \text{かつ }\mathfrak G_{\rm ar}\cap A=L\ \Longrightarrow\ L=L_3 .\ }$$
> **∎**

> ★ **副産物(明示的な非算術元)**: $h_4\notin H_W$ ゆえ $h_4\notin\mathfrak G_{\rm ar}$。**$\langle h_4\rangle\setminus\{1\}$ の 6 元は「名前のついた非算術 GT-shadow」**である(DUM 由来・既在の A 型証明書 252 個の一部であって新規主張ではない)。

### 2.6 ★★ 定理 **BH-1**(算術像のブラケット)と 系 **BH-2**

> ### 定理 BH-1
> $\mathcal C$ を「$H_W$ に含まれ $\mathbf c=[6,1]$ を含む位数 6 の部分群」とする(補題 BH-3 で**存在と一意性**を示す)。このとき
> $$\boxed{\ \mathcal C\ \subseteq\ \mathfrak G_{\rm ar}\ \subseteq\ H_W,\qquad \lvert\mathcal C\rvert=6,\quad\lvert H_W\rvert=42,\qquad \mathfrak G_{\rm ar}\in\{\mathcal C,\ H_W\}. \ }$$
> すなわち $\lvert\mathfrak G_{\rm ar}\rvert\in\{6,42\}$ であり、**中間値は存在しない**。
>
> **証明.** SUP-1 より $\mathfrak G_{\rm ar}\to C_6$ は全射、SUP-4 より $\mathfrak G_{\rm ar}\cap A\in\{1,L\}$。
> - $\mathfrak G_{\rm ar}\cap A=L$ の場合: $\lvert\mathfrak G_{\rm ar}\rvert=42=\lvert H_W\rvert$ と SUP-2 より $\mathfrak G_{\rm ar}=H_W$。
> - $\mathfrak G_{\rm ar}\cap A=1$ の場合: $\mathfrak G_{\rm ar}\cong C_6$、$\mathbf c\in\mathfrak G_{\rm ar}\subseteq H_W$(SUP-2 + §2.2)ゆえ $\mathfrak G_{\rm ar}$ は BH-3 の一意な $\mathcal C$ に一致。
> 前者の場合も $H_W$ は位数 42 の群(SUP-4 で $L=L_3$、$H_W=L_3\rtimes C_6$)で、Schur–Zassenhaus と $\mathbf c\in H_W$ より $\mathcal C\subseteq H_W=\mathfrak G_{\rm ar}$。∎

> ### 系 BH-2(**B 型候補集合**)
> $$\mathcal B:=H_W\setminus\mathfrak G_{\rm ar}\ \in\ \bigl\{\ \emptyset\ (\text{0 個}),\qquad H_W\setminus\mathcal C\ (\textbf{36 個})\ \bigr\}.$$
> **B 型候補の個数は 0 か 36 の二値しかない。** 42 個の key を 1 個ずつ判定する問題ではない。

> ### 系 BH-2′(**$\mathrm{Ih}_{\mathbf N}$ の非全射性**)
> $\lvert\mathfrak G_{\rm ar}\rvert\le42<294=\lvert\mathrm{GT}(\mathbf N)\rvert$ ⟹ **本窓で $\mathrm{Ih}_{\mathbf N}$ は全射でない**(指数 $\ge7$)。
> ⚠ これは正典 Conj 5.1(dihedral 予想)への反例では**ない** — $\mathbf N$ は dihedral 族でない。既在の帰結(A 型証明書 252 個 = HSP-SOUND により非算術)の言い換えであり、**novelty 主張はしない**。

### 2.7 補題 **BH-3**($\mathcal C$ の存在・一意性・計算法)

> **補題 BH-3.** $H_W$ に含まれ $\mathbf c$ を含む位数 6 の部分群は**ちょうど 1 つ**存在する。
>
> **証明.** $u_0$ を $(\mathbb Z/7)^\times$ の生成元(例 $u_0=3$)とし、層 $\chi_{\rm vir}^{-1}(u_0)$ を $A$-torsor と見る。3 乗写像 $g\mapsto g^3$ は $\Phi$ 上のアフィン写像で、その線型部は $1+\Phi+\Phi^2$。$\Phi$ の固有値は $u_0^3,u_0^4$ で $1+u_0^3+u_0^6=1$、$1+u_0^4+u_0^8\equiv0$($u_0=3,5$ の両方で機械確認・付録 A)ゆえ
> $$\ker(1+\Phi+\Phi^2)=L_4\quad(\text{位数 }7).$$
> したがって $\{g:\ g^3=\mathbf c\}$ は空か $L_4$ の coset(7 元)。空でないことは $\mathfrak G_{\rm ar}$ の存在から従う($\lvert\mathfrak G_{\rm ar}\rvert=6$ なら $\mathfrak G_{\rm ar}\cong C_6$ の 3 乗元が層 $u_0^3=6$ の唯一の元 $=\mathbf c$;$\lvert\mathfrak G_{\rm ar}\rvert=42$ なら $H_W=L_3\rtimes C_6$ の中で Schur–Zassenhaus)。
> 一方 $H_W\cap\chi_{\rm vir}^{-1}(u_0)$ は $L$ の coset(7 元・PENT-LAYER)。$L\ne L_4$ ゆえ、2 次元アフィン平面の中で**方向の異なる 2 本のアフィン直線は 1 点で交わる**(付録 A で全 coset について機械確認)。交点が求める生成元で、$\mathcal C=\langle g\rangle$。∎

> ★ **計算法(§3 の (J2))**: $\mathcal C$ は「$\mathbf c$ を 3 乗根に持ち、かつ $\mathrm{PENT}_W$ を通る層 $u_0$ の元」**ただ 1 つ**から生成される。**cert 内のデータだけで同定できる。**

### 2.8 ★★ 定理 **BH-4**(判定の 1 ビット還元)と 系 **BH-5**(片側の紙判定)

> ### 定理 BH-4
> $\ker(\chi\bmod 7)=G_{\mathbb Q(\mu_7)}$ であり、$\mathrm{Ih}_{\mathbf N}(g)\in A\iff g\in G_{\mathbb Q(\mu_7)}$。ゆえに
> $$\mathfrak G_{\rm ar}\cap A=\mathrm{Ih}_{\mathbf N}\bigl(G_{\mathbb Q(\mu_7)}\bigr),$$
> したがって
> $$\boxed{\ \mathfrak G_{\rm ar}=H_W\ (42)\iff \mathrm{Ih}_{\mathbf N}(G_{\mathbb Q(\mu_7)})\ne1\iff \exists\,\sigma\in G_{\mathbb Q(\mu_7)}:\ f_\sigma\not\equiv1 \pmod{\mathcal V(F_2)} .\ }$$
> さらに SUP-4($L\cap L_4=1$)より、この非自明性は **$\mathrm{gr}_3$ 成分の非消滅と同値**である($\mathrm{gr}_4$ 成分だけが非零であることはあり得ない)。
>
> **証明.** $\chi_{\rm vir,\mathbf N}(\mathrm{Ih}_{\mathbf N}(g))=\chi(g)\bmod 7$((1.13))。ゆえに像が $A=\ker\chi_{\rm vir,\mathbf N}$ に入るのは $\chi(g)\equiv1\ (7)$ のとき、すなわち $g\in G_{\mathbb Q(\mu_7)}$ のとき。$\sigma\in G_{\mathbb Q(\mu_7)}$ に対し $m_\sigma\equiv0$ で $\mathrm{Ih}_{\mathbf N}(\sigma)=[0,\ f_\sigma\bmod\mathcal V(F_2)]$。あとは BH-1 と SUP-4。∎

> ### 系 BH-5(**片側は紙+小計算で閉じる**)
> $$\boxed{\ L=\ker(D\vert_A)\ \text{が }\Phi\text{-不変でない}\ \Longrightarrow\ \mathfrak G_{\rm ar}=\mathcal C\ (\text{位数 }6)\ \Longrightarrow\ \textbf{B 型候補が 36 個確定}.\ }$$
> **証明.** SUP-4 より $\mathfrak G_{\rm ar}\cap A$ は $C_6$-部分加群かつ $\subseteq L$。$L$ が $\Phi$-不変でなければ $L$ 自身は部分加群でなく、位数 7 の部分加群は $L_3,L_4$ のみでいずれも $\ne L$ ⟹ $\mathfrak G_{\rm ar}\cap A=1$。∎
> ⚠ **逆は成り立たない**: $L$ が $\Phi$-不変($=L_3$)でも $\mathfrak G_{\rm ar}$ は 6 か 42 か決まらない(定理 BH-4 の 1 ビットが残る)。**この検査は片側だけの検出器である。**

### 2.9 EXQ-6(予言 $\mathrm{GT}(\mathbf N)\cong C_7^2\rtimes C_6$)との整合

| 予言 EXQ-6 | 本票の帰結 | 整合 |
|---|---|---|
| $\lvert\mathrm{GT}(\mathbf N)\rvert=294$、$A\cong C_7\times C_7$ | $\mathfrak G_{\rm ar}\in\{\mathcal C,H_W\}$、$\lvert\mathcal C\rvert=6=\lvert C_6\rvert$、$\lvert H_W\rvert=42=\lvert L_3\rtimes C_6\rvert$ | ★ **両値とも $C_7^2\rtimes C_6$ の部分群の位数**であり、位数水準で整合 |
| $C_6$ の作用 = $\mathrm{gr}_3$ に $u^3$、$\mathrm{gr}_4$ に $u^4$ | この**指標の相異**がちょうど「部分加群は 4 個」を与え、BH-1 の二値性を生んでいる | ★ **EXQ-6 の構造部分が B-HUNT の臨界路上にある**(位数水準だけでは足りない) |
| — | $\mathfrak G_{\rm ar}$ の指数 $\ge7$ | $\mathrm{Ih}_{\mathbf N}$ 非全射(系 BH-2′) |

> ⚠ **cert の限定を継承**: EXQ-6 は本走で**位数水準しか確認されていない**(cert 逐語: 「群構造(3.53)そのものを再構成していないので群表(乗積表・作用の指数)は独立に確認していない」)。**本票の BH-1/BH-3 は $\Phi$ の作用(構造)を使う**ので、§3.1 (J1′) で作用の実測を設計に含める。

---

## 3. ★ 判定可能性の設計(委嘱 §2)

### 3.0 設計の心臓(**先に 3 行**)

$$\boxed{\ \textbf{①「42 個の key を個別に判定する」問題ではない — 系 BH-2 により答は 0 個か 36 個の 1 ビット。}}$$
$$\boxed{\ \textbf{② 突合すべきは個々の key ではなく「部分群の形」。identity の錨は複素共役 }\mathbf c=[6,1]\ \textbf{ただ 1 つ。}}$$
$$\boxed{\ \textbf{③ 有限窓計算は「非算術」を証明できるが「算術」を証明できない。正側の 1 ビットは窓の外にある。}}$$

### 3.1 工程(J0 → J3)

| 段 | 内容 | 入力 | 新規窓計算 | 出力 |
|---|---|---|---|---|
| **(J0)** | **42 key の実体化**: $\mathrm{pent}(m)=\mathrm{hex}(m)\cap\{f:D(f)=1\}$。lane S/V の PASS 集合(層つき)と lane P の PASS 集合($[P,P]$ 全体の $D^{-1}(1)$・49 元)を **$e$-ベクトルで join** するだけ。両 lane の `pcgs_basis_fingerprint` は同一なので key は直接比較可能 | 既収集の joined artifact のみ | ★ **ゼロ**(post-hoc join) | 42 key の実体+**層別 PENT 数の測定**(外挿の解消) |
| **(J1)** | $L=\ker(D\vert_A)$ の同定(層 0 の 7 key) | (J0) の出力 | ゼロ | $L$(7 元) |
| **(J1′)** | **$\Phi$ の実測**: 生成層 $u_0$ の hexagon 元 $g_0$ を 1 つ取り、$h\in L$ に対し $\Phi(h)=E_{m_0,f_0}(h)$ を $P$ の中で計算 | $P$ 上の群演算(既存 pcgs) | 小(**$7\times$ 1 元の自己準同型評価**・宇宙の再走なし) | $\Phi\vert_A$ の行列 |
| **(J2)** | **$\mathcal C$ の同定**: 層 $u_0$ の $H_W$ 元 7 個のうち $g^3=\mathbf c$ を満たすものを探す(BH-3 より**ちょうど 1 つ**) | (J0)(J1′) | 小 | $\mathcal C$ の 6 key = **算術像の下界(明示)** |
| **(J3)** | **残る 1 ビット**: $\mathrm{Ih}_{\mathbf N}(G_{\mathbb Q(\mu_7)})\ne1$ か(定理 BH-4) | ★ **窓の外**(算術的入力) | — | $\mathfrak G_{\rm ar}=\mathcal C$ か $H_W$ か |

- **(J1) + (J1′) ⟹ 系 BH-5 の検査**: $\Phi(L)=L$ か。**否なら (J3) を待たずに B 型候補 36 個が確定**する。
- **(J2) は分岐に依らず実行できる**(BH-3 の一意性は両分岐で成立)。⟹ **算術像の明示的な下界 6 key は、(J3) を待たずに手に入る。**

### 3.2 何と何を突合すれば identity が取れるか(**委嘱の核心**)

| 突合の対象 | 可能か | 理由 |
|---|---|---|
| **Thm 4.3 型の明示式との突合** | ★ **不可** | 2405 Thm 4.3 は $\mathrm{GT}(K^{(n)})$ の明示式であり、**HS 窓 $\mathbf N$ には対応物が無い**(委嘱の注意どおり)。$K^{(n)}$ で使える「$\mathrm{GT}$ の全元を式で書き、算術層を Thm 5.3 の下界で挟む」型の議論は移植できない |
| **複素共役との突合** | ★ **可(唯一の明示錨)** | Ihara ICM 印字 106: $\chi(\iota)=-1$, $f_\iota=1$ ⟹ $\mathbf c=[6,1]$。**これが本窓で名指しできる唯一の算術元** |
| **部分群の形との突合(BH-1/BH-3)** | ★ **可** | 算術像は「$C_6$ を覆い・$A$ 成分が $C_6$-部分加群で・$L$ に含まれ・$\mathbf c$ を含む」部分群。この条件を満たす部分群は**ちょうど 2 つ**($\mathcal C$ と $H_W$)⟹ 判定は 1 ビット |
| **個別 key の「算術性」の直接判定** | ★ **不可(原理的)** | 算術性は $G_{\mathbb Q}$ の像への所属であり、**有限窓の述語ではない**。窓が与えるのは必要条件(hexagon・$\mathrm{PENT}_W$)だけ |
| **細分窓への survive による非算術性の証明** | 可(**片側**) | $K\le\mathbf N$ で $s\notin\mathrm{Im}(R_{K,\mathbf N})$ なら非 genuine ⟹ 非算術(Cor 5.4)。**逆は無限深度**(`fake_void_v1.md` §1.2 の非対称性)。⚠ 適用は **NW 系の細分に限る**(§4.2 の規則) |

> ### ★ 一行で
> **本窓の「identity」は、個々の shadow に貼るラベルとしては取れない。取れるのは「算術像という部分群の同定」であり、それは $\mathbf c$ を錨とした群構造の突合で 1 ビットまで縮む。**

### 3.3 (J3) の中身 — 何が要るか

定理 BH-4 により、残る 1 ビットは
$$\textbf{「}G_{\mathbb Q(\mu_7)}\textbf{ の像が }P=F_2/\gamma_5(F_2)F_2^{\,7}\textbf{ の中で自明か」}$$
すなわち **mod 7 での重さ 3 の Galois 元の非消滅**である。これは正典(2401/2405/HS/Ihara ICM §2–3)が**扱っていない**種類の言明である — Ihara ICM は $f_\sigma$ の定義と (I)(II)(III) までで、**次数ごとの非消滅は射程外**(読解ノート §4.1 の範囲)。⟹ **【文献要請 BH-L1】**(§7.3)。

> ⚠ **出所ラベル(正典外の背景知識・根拠に数えない)**: 起草者は「$7$ は正則素数なので重さ 3 の mod 7 非消滅が期待される」という背景を持つが、**本票はこれを根拠に数えない**。予言(§6.1)にはこの期待を**登録済み分岐として**書くが、格は「予想」であって定理ではない。

---

## 4. ★★ 封印回避の逐点検査(委嘱 §3 — 最重要)

### 4.1 検査の基準

封印 3 量の記載は repo 内で複数の言い回しがある。**保守的に和集合**を取って検査する:
(i) $n=5$ 関連($u_9/a_9$ の値・$c$ の平方類・$\hat c_\mu$)、(ii) $\mathrm{Im}\,R$(= $\mathrm{Im}\,R_{N,K^{(5)}}$)、(iii) $d_N$、(iv) genuine 層の $u$ 値、(v) PSL 窓の構造量・$\varepsilon$ bits。

### 4.2 逐点表(**設計の全入力**)

| # | 本票/設計が使う量 | 出所 | 封印との関係 | 判定 |
|---|---|---|---|---|
| 1 | 正典式 (1.4)–(1.13)・Thm 3.10/5.2・Def 4.2・Cor 5.4 | 公刊論文 | 無関係 | ✅ 非接触 |
| 2 | Ihara ICM (2.3.1)(2.3.2)・複素共役 $f_\iota=1$ | 公刊論文(頁照合済) | 無関係 | ✅ 非接触 |
| 3 | ISO-V($\mathcal V(F_2)$ verbal ⟹ isolated) | 工房の紙補題 | 無関係 | ✅ 非接触 |
| 4 | 窓パラメータ $\lvert P\rvert,\lvert[P,P]\rvert,N_{\rm ord}=7,\lvert\mathcal X\rvert=6,\eta\ne0$ | NW(7) 発火条件 2 cert | **K⁽⁵⁾ とは別戦役**の窓 | ✅ 非接触 |
| 5 | 本走測定 294 / 49 / 7 | NW(7) 本走 cert(`sealed_quantities_contacted: false` を cert 自身が宣言) | 同上 | ✅ 非接触 |
| 6 | (J0) の join(lane S/V/P の PASS key) | 同 joined artifact | 同上 | ✅ 非接触 |
| 7 | (J1′) の $\Phi$ 実測($P$ 内の自己準同型評価) | 既存 pcgs | 同上 | ✅ 非接触 |
| 8 | (J2) の $\mathcal C$ 同定(3 乗根探索) | 上記の出力のみ | 同上 | ✅ 非接触 |
| 9 | (J3) の重さ 3 非消滅 | **外部文献**(未取得) | 封印ではなく**文献ゲート**の対象 | ✅ 封印非接触・⚠ 文献要請 |
| 10 | (§3.2 最終行)細分 survive による非算術性 | $R_{K,\mathbf N}$($K\le\mathbf N$) | ★ **$\mathrm{Im}\,R$ と同型の量**。ただし対象は **NW 系の細分**であって $K^{(5)}$ ではない | ⚠ **条件つき可**(§4.4 規則 R-2) |

### 4.3 ★ 名前衝突の検査(**偽陰性・偽陽性の両方を防ぐ**)

| 記号 | 本票での意味 | 封印語彙での意味 | 判定 |
|---|---|---|---|
| **$u$** | $u=2m+1=\chi_{\rm vir}$、$(\mathbb Z/7)^\times$ の値。**公開の窓座標**(票 v1 §1.3・cert の層 index) | $K^{(5)}$ 戦役の $u_9$ 等・genuine 層の $u$ 値 | ★ **完全な別物**。grep で「$u$」が一致しても封印接触ではない。**逆に「$u$ を避ければ安全」でもない**(下記 $d$・$\mathrm{Im}\,R$ を見よ) |
| **$d$** | 本票は $d_N$ 型の量を**一切使わない**(深さは (§3.2) の細分 survive でのみ概念的に現れる) | $d_{\rm gen}(5)$・$d_{\rm arith}(5)$ 等 | ✅ 非接触 |
| **$\mathrm{Im}\,R$** | 本票の臨界路(J0–J2)は $R_{K,\mathbf N}$ を**使わない** | $\mathrm{Im}\,R_{N,K^{(5)}}$ | ✅ 臨界路は非接触(§4.4 R-2 の枠内でのみ将来の選択肢) |
| **$\mathcal C$/$L$/$L_3$/$L_4$** | 本票で新規に導入(NW(7) 内部) | — | ✅ 衝突なし(grep 済) |

### 4.4 ★ 結論と運用規則

> $$\boxed{\ \textbf{B-HUNT の臨界路(J0 → J1 → J1′ → J2 → 系 BH-5)は封印 3 量に一切依存しない。}\ }$$
> $$\boxed{\ \textbf{⟹ HUNT は封印解除待ちにならない。}\ }$$

残る (J3) は**封印ではなく文献ゲート**に依存する。すなわち止めているのは秘匿ではなく未取得の外部機構である。

**運用規則(本札に付随・司令塔裁定を請う)**:
- **R-1**: B-HUNT の全成果物で、$K^{(5)}$ 由来の量($u_9/a_9$・$c$ の平方類・$\hat c_\mu$・$\mathrm{Im}\,R_{N,K^{(5)}}$・$d_N$・genuine 層の $u$ 値)を**入力にも特徴量にも置かない**。
- **R-2**: §3.2 最終行(細分 survive による非算術性証明)を将来使う場合、**細分先は NW 系の窓に限る**。$K^{(5)}$ を含む交差窓($M=\mathbf N\cap K^{(5)}$ 型)は**禁止**。$K^{(7)}$ 等の他戦役との交差窓(札 F-1 の設計案)は、**着手前に司令塔へ当該戦役の封印状態の確認を求める**(本票では判断しない)。
- **R-3**: 本票で使う「$u$」は必ず「$u=2m+1=\chi_{\rm vir}$」と初出で書く(§4.3 の衝突対策)。

---

## 5. 前件表(**BH-1 が何に乗っているか**)

| 札 | 前件 | 現在の格 |
|---|---|---|
| **ISO-V** | $\mathbf N$ は isolated | Sol F105-3.3 で paper theorem 受理 |
| **GRP** | isolated ⟹ $\mathrm{GT}(\mathbf N)$ は群・合成 (3.53)・(3.49) | 正典 Thm 3.10 |
| **IH** | (1.5)(1.6)(1.11)(1.12)(1.13)+$\chi$ 全射 | 正典 2405 §1.3(+ Belyi・Ihara) |
| **SOUND** | HSP-SOUND(片側健全) | paper-proof(Sol F100-1.3 PASS) |
| **LAY-1〜4** | 層 = coset・$\lvert A\rvert\in\{7,49\}$ | Sol F106-2 **前件相対 PASS**・実測で $\lvert A\rvert=49$(B-1a) |
| **PENT-HOM** | $D\vert_A$ が準同型 | Sol F106-2.2 **$m=0$ kernel 部分 PASS** |
| **PENT-LAYER** | 層移送 | addendum A §3.1 **paper-proof candidate**(Sol 未監査) |
| **CONJ-Φ** | 共役 $=\Phi=E_{m,f}$、graded で $\mathrm{diag}(u^3,u^4)$ | addendum A §4 **paper-proof candidate**(非対角成分は **PL-GAP-2** で OPEN — ★ BH-1 は**半単純性しか使わない**ので非対角成分の未同定は無害) |
| **測定** | $\lvert A\rvert=49$・$\lvert L\rvert=7$・$\eta\ne0$ | 本走/条件 2 cert(CV-9 判読は未経由) |

> ★ **PL-GAP-2 が臨界路に無いことの確認(重要)**: BH-1/BH-3 が使うのは「$C_6$ 表現が半単純で二指標が相異なる」ことだけであり、$\Phi\vert_A$ の**非対角成分の値は不要**である。⟹ addendum A の残 GAP は本札を止めない。
> ★ 一方 **PL-GAP-1**($H_W$ が部分群か)は、**系 BH-5 の検査そのもの**である(addendum A §3.3 (d) と本票 §2.8 は同じ検査を別方向から見ている)⟹ (J1)(J1′) は **PL-GAP-1 も同時に閉じる**。

---

## 6. ★ 分岐の事前登録(委嘱 §4)

### 6.1 登録分岐(**発火前に登録**)

| 分岐 | 判定条件 | $\lvert\mathfrak G_{\rm ar}\rvert$ | B 型候補 | 解釈 |
|---|---|---|---|---|
| ★ **BH-α(本票の予言)** | (J1′) で $\Phi(L)=L$(⟹ $L=L_3$)**かつ** (J3) の重さ 3 mod 7 非消滅 | **42**($=H_W$) | **0 個** | ★ **窓レベルで B 型候補が空**。「hexagon と PENT を通る元はすべて算術」= P5(FAKE-VOID)に**有利**な観測。副産物: $H_W$ が部分群(**PL-GAP-1 CLOSED**) |
| **BH-β(登録済み代替)** | $\Phi(L)=L$ だが (J3) が消滅側 | **6**($=\mathcal C$) | **36 個** | $\mathcal C$ 以外の 36 元は**非算術**(有限証明書つき)。genuine 性は **UNKNOWN**(有限深度から出ない)⟹ **B 型候補**であって B 型証人ではない |
| **BH-γ(登録済み代替)** | (J1′) で $\Phi(L)\ne L$ | **6**(系 BH-5 で**強制**) | **36 個** | 窓計算だけで非算術 36 個が確定。★ **ただし同時に「重さ 3 mod 7 が消滅する」という古典算術の言明を導いてしまう** ⟹ §6.2 の警報 |
| **BH-δ(登録外 = 事前登録の反証)** | $\lvert\mathfrak G_{\rm ar}\rvert\notin\{6,42\}$ が示唆される・(J2) の $\mathcal C$ が **0 個または 2 個以上**・層別 PENT 数が 7 でない層がある | — | — | **PREREGISTRATION_FALSIFIED / STOP**(§6.3 丁類) |

> ★ **BH-α が本票の予言である理由**(格 = 予想): 系 BH-2 の二値のうち、**登録済みの外部期待**(§3.3 の出所ラベルつき背景)が 42 側を指すため。⚠ **根拠は文献要請 BH-L1 の回答待ちであり、本票はこれを定理として書かない。**

### 6.2 ★ BH-γ 着地時の特別扱い(**外部整合性の警報**)

> BH-γ は窓内では自己完結するが、**定理 BH-4 と組み合わさると「$G_{\mathbb Q(\mu_7)}$ の像が class 4・指数 7 の商で自明」という古典的算術の言明**を導く。これは**窓の外に波及する強い主張**である。⟹
> $$\boxed{\ \textbf{BH-γ 着地時は「発見」として即報しない。まず翻訳の忠実性を疑う。}\ }$$
> 一次点検リスト: ①$D$ の実装が定義 HSP-T と逐語一致か(CV-9 判読)②lane P の PASS 集合が本当に $D^{-1}(1)$ か($m$ 非依存性の実測確認)③$\Phi$ の実測が系 CONJ-Φ の $E_{m,f}$ と同じ対象か ④$L$ の 7 元が本当に $\mathrm{hex}(0)\cap D^{-1}(1)$ か。**4 点すべてが潔白で初めて BH-γ を数学的結論として扱う。**

### 6.3 外れ値の四分類(票 v1 §7.2 の様式を継承)

| 類 | 対象 | 一次解釈 | 手続き |
|---|---|---|---|
| ★ **甲(格 T = 定理の帰結)** | (J0) で **PENT 通過が 0 の層がある**/層別 PENT 数が 7 以外/$\lvert H_W\rvert\ne42$ | ★ **実装バグを第一に疑う**。SUP-1+SUP-3 は正典 (1.13) と PENT-LAYER の帰結であり、数学的新発見として読まない | `IMPLEMENTATION_BUG_SUSPECTED / STOP`。①当該候補の座標を封印 ②join を独立第二実装で再計算 ③lane P の $m$ 非依存性を fixture で確認 ④Sol 即報 |
| **乙(格 T\*)** | (J2) の $\mathcal C$ が一意でない/$\mathbf c=[6,1]$ が $H_W$ に無い/$L=L_4$ | 二段階: (i) 実装(key 変換・層割付・3 乗の合成則)を疑う (ii) 潔白なら**前件の特定** — 候補は PENT-HOM・CONJ-Φ・LAY-3・$\eta\ne0$ | `LANE/PREREG 整合検査` → 特定不能なら `PREREGISTRATION_FALSIFIED` |
| **丙(登録済み分岐へ着地)** | BH-β / BH-γ | ★ **「外れ」と記録しない。「分岐 BH-β/γ で決着」と記録する** | cert に `branch_resolved: BH-β` 等。**同一 run 内で他の予言を書き換えない**(S-7′) |
| ★ **丁(登録外)** | BH-δ の各条件 | ★ **紙の構造補題に穴**(BH-1/BH-3/SUP-4 のいずれかが偽) | 即時停止。部分結果は保存。**v1 が外れた事実と digest を明記した v2 の事前登録から再開** |

### 6.4 停止規則の**提案**(発効は司令塔裁定 + Sol ゲート)

```jsonc
// 提案のみ。本票は発効させない。
"S-BH-1": { "trigger": "(J0) の層別 PENT 通過数が 7 でない層が 1 つでもある",
            "verdict": "IMPLEMENTATION_BUG_SUSPECTED / STOP",
            "note": "SUP-1+SUP-3+PENT-LAYER の帰結。甲類 = 検出器。的中(全層 7)は成果として数えない。" },
"S-BH-2": { "trigger": "(J2) が位数 6 の部分群を 0 個または 2 個以上返す",
            "verdict": "PREREGISTRATION_FALSIFIED / INTEGRITY_STOP",
            "note": "補題 BH-3 の一意性の反証。丁類。" },
"S-BH-3": { "trigger": "分岐 BH-γ への着地",
            "verdict": "EXTERNAL_CONSISTENCY_ALARM / HOLD",
            "note": "§6.2 の 4 点点検を通過するまで数学的結論として扱わない。即報もしない。" }
```

### 6.5 的中しても言えないこと(**過大評価の防止**)

1. 「**42 個が genuine**」— 言えない。$\mathrm{PENT}_W$ は片側健全(SOUND)。
2. 「**36 個が fake**」— 言えない(§0-3)。言えるのは**非算術**まで。**genuine 性は有限深度から出ない**ので FAKE-KILL の証人にはならない。
3. 「**井原予想に反例**」— 言えない。系 FAKE-KILL の前件は **genuine かつ非算術**であり、本窓は前者を供給しない。
4. 「**dihedral 予想に効いた**」— 言えない。$\mathbf N$ は dihedral 族でない。
5. `cross-checked` / `verified` — 付かない。

---

## 7. 格付け・【GAP】・【文献要請】・規律申告

### 7.1 格付け

| 対象 | 格 |
|---|---|
| 補題 **SUP-1 / SUP-2** | ★ **paper-proof**(正典 (1.13)+HSP-SOUND の引用のみ・自前の新段なし) |
| 補題 **SUP-3 / SUP-4**、定理 **BH-1**、系 **BH-2 / BH-2′**、補題 **BH-3**、定理 **BH-4**、系 **BH-5** | ★ **paper-proof candidate**(本票・**Sol 未監査**・単系統)。前件は §5 の表(measurement-relative + framework-relative) |
| 分岐 **BH-α** | **予想**(格 C)。根拠は文献要請 BH-L1 待ち |
| 42 の外挿解消(J0) | **設計**(未実行) |
| `cross-checked` / `verified` | ✗ どちらも付かない |
| novelty | **主張しない**(grep 済: `B-HUNT`・`BH-`・「算術像のブラケット」は repo に既出なし。⚠ ただし「**非可解窓の算術像を読む道具**」は裁定 386 の既在文言[`hs_prop7_translation_v1.md` §4]であり、語としては新規でない。系 BH-2′ の内容は HSP-SOUND+252 件の言い換えで既在) |

### 7.2 【GAP】

| 札 | 内容 | 状態 |
|---|---|---|
| ★ **【BH-GAP-1】** | (J3) の 1 ビット(重さ 3 mod 7 非消滅)が未供給 ⟹ BH-α/β が未決 | **OPEN**(文献要請 BH-L1) |
| ★ **【BH-GAP-2】** | $L$ の $\Phi$-不変性が未測定 ⟹ 系 BH-5 が未発火 | **OPEN**((J1′) で閉じる・**新規窓走行なし**) |
| **【BH-GAP-3】** | $\mathfrak G_{\rm pent}$ と $H_W$ の差(片側性)は本票で一切埋めていない。$H_W\setminus\mathfrak G_{\rm ar}$ の内訳(arith-fake / pentagon-fake / hexagon-fake)は**分離できない** | **UNKNOWN**(原理的・`fake_void_v1.md` §1.3) |
| **【BH-GAP-4】** | 本票は $\mathrm{GT}(\mathbf N)$ の**乗積表を独立に再構成していない**(cert の EXQ-6 は位数水準のみ)。BH-3 の 3 乗計算は (J1′) の実測に依存 | **設計で解消**((J1′)) |
| **【PL-GAP-1】**(addendum A) | $H_W$ が部分群か | ★ **(J1) + (J1′) で閉じる**(§5 末尾) |

### 7.3 ★ 【文献要請 **BH-L1**】

- **具体的な技術的困難**: 本窓の算術像の同定は、群論・有限窓計算をすべて使い切った後に **1 ビット**だけ残る(定理 BH-4)。そのビットは
  $$\mathrm{Ih}_{\mathbf N}\bigl(G_{\mathbb Q(\mu_7)}\bigr)\ne1\ \Bigl(\iff \exists\sigma\in G_{\mathbb Q(\mu_7)}:\ f_\sigma\not\equiv1\bmod \gamma_5(F_2)F_2^{\,7}\Bigr)$$
  であり、SUP-4 により **$\mathrm{gr}_3\otimes\mathbb F_7$ 成分の非消滅**と同値。**正典(2401/2405/HS/Ihara ICM §2–3)にはこの型の非消滅を与える言明が無い**(Ihara ICM は $f_\sigma$ の定義と (I)(II)(III) までで、次数別の非消滅は射程外)。
- **欲しい結果の型**: 「素数 $\ell$ と重さ $w$(奇)に対し、$G_{\mathbb Q(\mu_\ell)}\to\mathrm{gr}_w(\widehat{F_2})\otimes\mathbb F_\ell$ の像が非零であるための**判定条件**」。とくに $(\ell,w)=(7,3)$ を決める形。等価な形でよい(例: 対応する Galois 指標の mod $\ell$ 非消滅の判定基準、$\ell$ の正則性/非正則対との関係)。
- **翻訳の要件(司令塔の一工夫義務)**: 得られた機構を **B₃-gentle の窓 $\mathbf N$**($P=F_2/\gamma_5F_2^{\,7}$・class 4・exponent 7)へ翻訳し、$\mathrm{GT}(\mathbf N)$ の $A$ 成分($L_3\oplus L_4$)と対応づける段が要る。とくに「$\mathrm{gr}_3$ 成分の非消滅」が **$L$ が $\Phi$-不変であること**とどう整合するかまで降ろせると (J1′) の結果と突合できる。
- **不要なもの**: pentagon 側・dihedral 側の文献。本要請は **hexagon 側の深さ 3・mod 7** に限局する。

### 7.4 規律申告

- ★ **新規の窓計算ゼロ。** GAP も pc 群も起動していない。機械は付録 A の python(整数演算・42 個の key に非接触)だけ。
- ★ **42 個の candidate key の値を 1 個も列挙していない。** cert の**構造**(lane・フィールド名・件数)のみ参照した。
- **封印 3 量($n=5$ 関連・$\mathrm{Im}\,R$・$d_N$・genuine 層の $u$ 値)非接触** — §4 で逐点検査済。名前衝突(「$u$」)も明示的に潰した。
- **外部文献検索ゼロ**(文献ゲート遵守)。**新しい原典頁を開いていない**(引用はすべて既在の読解ノート経由)。**【文献要請 BH-L1】を起票**した。
- **既存文書は 1 バイトも改変していない**(本票は新規ファイル)。票 v1(`89349a8`)・addendum A の IF-FIRST 凍結を保全。
- 数値は**すべて機械生成**(付録 A の出力を転記・手写しゼロ)。

---

## 8. Sol への監査点(4 点)

> **Q-1 ★★ 定理 BH-1 の二値性**(§2.6)。「$\mathfrak G_{\rm ar}\cap A$ は $C_6$-部分加群」(SUP-4)の一段 — $\mathfrak G_{\rm ar}$ が $C_6$ 全体を覆う(SUP-1)ことから共役作用が全 $C_6$ を渡る、という論法に穴はないか。**ここが「判定は 1 ビット」の全体を支えている。**
>
> **Q-2 ★★ 補題 BH-3 の一意性**(§2.7)。3 乗写像の線型部 $1+\Phi+\Phi^2$ の核が $L_4$ であること(固有値 $u_0^3,u_0^4$ からの計算・付録 A)と、「方向の異なる 2 本のアフィン直線は 1 点で交わる」の適用。**および $\{g:g^3=\mathbf c\}\ne\emptyset$ の論証**(両分岐での存在)を認めるか。
>
> **Q-3 ★ 補題 SUP-3**(§2.4)。「算術供給が各層に PENT 元を 1 つ供給する」ことで PENT-LAYER の前件を満たし、**外挿 42 が紙で閉じる**という主張。⚠ ただし cert の測定格付けは変えない(測定へ格上げするのは (J0) の join のみ)という会計を認めるか。
>
> **Q-4 ★ 系 BH-5 と PL-GAP-1 の同一性**(§5 末尾)。「$L$ の $\Phi$-不変性検査」は addendum A §3.3 (d)($H_W$ の部分群性)と**同じ検査**であり、(J1′) が両方を同時に閉じる、という読みを認めるか。

---

## 9. ★★ 単独コミットの注記(裁定 543 恒久規則)

$$\boxed{\ \textbf{本票は照合走(J0–J2)の実行前に、}\textbf{単独コミット}\textbf{されるべし。}\ }$$

- **理由**: 他のファイルと同一コミットに入れると、コミット時刻が「走行前」であることの証拠が同梱物の由来と混ざる。IF-FIRST の事前性は**コミットの単独性と時刻**で担保する。
- **確認手順(発注時)**: B-HUNT 走行 cert の `iffirst_registry` 欄に本票のパス・SHA-256・**単独コミット hash** を記録し、`git log --name-only <hash>` が本票 1 ファイルのみを示すことを機械確認する。
- **本票の改版**: 発火後に本票を書き換えない。改版が要るなら **v2 を新規に起こし、v1 が外れた事実と v1 の digest を冒頭に明記**する(S-7′ 正本の手続き)。

---

## 付録 A. 独立検算(**窓非接触**・整数演算のみ)

$A=\mathbb F_7^2$、$\Phi=\mathrm{diag}(u_0^3,u_0^4)$($u_0=3$)という**抽象モデル**の上で、§2 の群論的主張を悉皆で確認する。
半単純性(§2.5)より実際の $\Phi$ はこのモデルと $L_4$ を保つ基底変換で共役であり、以下の計数はすべて基底に依らない。

```python
p = 7; u = 3                                   # u_0 = (Z/7)^x の生成元
a3, a4 = pow(u,3,p), pow(u,4,p)                # gr3, gr4 上の固有値
Phi = lambda v: ((a3*v[0])%p, (a4*v[1])%p)
S3  = lambda v: tuple((v[i]+Phi(v)[i]+Phi(Phi(v))[i])%p for i in range(2))
# (1) C6-部分加群の総数  (2) ker(1+Phi+Phi^2)  (3) アフィン直線の交わり
# (4) 位数 294 の群 F_7^2 x| C_6 の中で c=((0,0),t^3) を含む C_6 の個数、
#     および H_W = L3 x| C6 の中でのその個数
```

**出力(機械生成 — `scratchpad/bhunt_check.py`)**:

```
u = 3  u^3 = 6  u^4 = 4  distinct: True
u^3 != u^4 for all layers with u != 1 : True
C6-submodules of A: 4 = {0, L3, L4, A}: True
  Phi-stable lines: ['L3', 'L4']
#{v : (1+Phi+Phi^2)v = 0} = 7  equals L4: True
every coset of every line L != L4 meets L4 in exactly 1 point: True
#C_6 subgroups of G containing c : 7
#C_6 subgroups inside H_W = L3><C6 containing c : 1
```

- 3 行目: **SUP-4**($C_6$-部分加群はちょうど 4 個)。
- 5 行目: **BH-3** の $\ker(1+\Phi+\Phi^2)=L_4$。
- 6 行目: **BH-3** の一意性(方向の異なるアフィン直線は 1 点で交わる)。
- 7–8 行目: ★ **群全体では $\mathbf c$ を通る $C_6$ が 7 個あるが、$\mathrm{PENT}_W$ で切ると 1 個に落ちる** — pentagon 窓が identity を一意化しているという、本票の設計の核心の数値的な姿。
