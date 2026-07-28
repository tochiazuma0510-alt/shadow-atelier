# W-Exist 独立検証 v1(candidate)

**委嘱**: 二層検証・単独委嘱(司令塔)。対象 = Sol 便 78 発案札 A「命題 W-Exist」(`sol/sol_reply_78_math5.md` §0・§1)。
**状態札**: candidate / paper-proof。**Lean verified ではない**。**cross-checked でもない**(§3.4 の算術検算は Python 単系統・初等整数演算のみ)。
**封印値・u は一切扱っていない。**

---

## 0. 判定

> ## **CONFIRM(補修つき)**

命題 W-Exist は、§2 の仮定表 (H1)–(H5) の下で**真**である。Sol の証明骨格(逆極限 → prosolvable → G_ℚ の非可解商と矛盾)は正しく、核の非可解性の系(§4)は無条件に正しい。

ただし **Sol の証明文には一段の欠落がある**:

> **【欠落 X】埋込 Ih: G_ℚ → ĜT_gen が位相群の埋込である(= 連続である)こと。**

Sol は「その閉部分群も prosolvable」と書いており位相を言外には使っているが、**なぜ像が閉部分群になるのか**(= なぜ Ih が連続か)を述べていない。これは装飾的な形式性ではない — **抽象群としての同じ議論は偽である**(§5 R-2 に反例: F₂ は prosolvable 群 = 自由 pro-2 群に抽象部分群として埋まるが、S₅ を有限商に持つ)。したがって欠落 X は**論法の成否を決める本質的な一段**である。

本ノート §3.3 の**補題 C** でこれを閉じたので、判定は CONFIRM を維持する。補修後の完全な証明を §3 に置く。

**副産物**(§7): 同じ論法の**弱い段**で、より安い算術入力(S₄ の ℚ 上実現)だけから「**非 metabelian な isolated 窓が存在する**」が出る。壁キャンペーンの**近傍目標も存在保証済み**である。

---

## 1. 主張の書き直し(型を明示する)

Sol の文の型を、定義ノート(`docs/week1-定義ノート.md` §2)と正典の記法で書き直す。

> **命題 W-Exist(再掲・型明示)**
> 仮定 (H1)–(H5) の下、**ある $N \in \mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$**(すなわち $N \trianglelefteq B_3$、$[B_3:N]<\infty$、$N \le PB_3$、かつ $N$ は GTSh の isolated 対象)が存在して、**有限群** $GT(N) = GTSh(N,N)$ は非可解である。さらに同じ $N$ について $\ker\widetilde\chi_N$ も非可解である。

型の要点(ここを外すと主張が無意味になる):

- $GT(N)$ が**群**であるのは $N$ が isolated のときだけ(2401 Def 3.13 の直後: 「Of course, in this case, $GT(N)=GTSh(N,N)$. In particular, $GT(N)$ is a group.」)。非 isolated $N$ では $GT(N)$ は**集合**であり「可解」は型が付かない — 2405 Remark 1.4 が明言。**Sol の札 B(isotropy への型修理)と整合**。
- $GT(N)$ は $N$ の isolated 性によらず**常に有限**($\mathbb Z/N_{\rm ord} \times F_2/N_{F_2}$ の部分集合)。有限性は問題ではなく、**群であること**が問題。
- 主張は**存在**のみ。指数の上界は出ない(Sol も明記・§6 で再確認)。

---

## 2. 仮定表(委嘱項目 2 — 最重要)

| # | 仮定 | 正確な内容 | 身分 | 出所 |
|---|---|---|---|---|
| **H1** | Ihara 埋込 | $\mathrm{Ih}(g):=\bigl((\chi(g)-1)/2,\ f_g\bigr)$ は群準同型 $G_{\mathbf Q}\to\widehat{GT}$ を定め、**Belyi の定理により単射**。 | **正典定理** | 2405 §1.3 (1.5)(1.6)+ 直後の箇条書き「Belyi's theorem [2] implies that homomorphism (1.6) is injective」。原典: [2]=Belyi 1979、[15]=Ihara 1994、[25]=Pop の survey Thm 4.7.6 / 4.7.7 / Fact 4.7.8 |
| **H2** | pentagon 落としの向き | $\widehat{GT}\ \le\ \widehat{GT}_{\rm gen}$(**部分群**)。ゆえに同じ式 (1.5) が単射準同型 $G_{\mathbf Q}\hookrightarrow\widehat{GT}_{\rm gen}$ を定める。 | **正典の明言**(当工房未再導出) | 2405 §1 冒頭「The original version $\widehat{GT}$ … is a subgroup of $\widehat{GT}_{\rm gen}$. Hence $\widehat{GT}_{\rm gen}$ also receives an injective homomorphism from $G_{\mathbf Q}$…」 |
| **H3** | isolated Main Line | $\Psi:\widehat{GT}_{\rm gen}\to\varprojlim(\mathrm{ML})$ は**群同型かつ同相**。$\mathrm{ML}$ は isolated poset 上の $N\mapsto GT(N)$、遷移射は reduction 準同型 $R_{N,H}$、各 $GT(N)$ は**有限群**。 | **正典定理** | 2401 **Thm 5.2**(「defines an isomorphism of groups $\Psi$ … Moreover, $\Psi$ is a homeomorphism (of topological spaces)」)+ Remark 5.3 + Def 3.13 + Remark 3.16(3.60 が準同型)+ Prop 3.14(cofinal)+ Prop 3.15(交わりで閉じる ⇒ poset は有向) |
| **H4** | **連続性(欠落 X)** | $\mathrm{Ih}: G_{\mathbf Q}\to\widehat{GT}_{\rm gen}$ は**連続**(ゆえに位相群の埋込・像は閉)。 | **正典に明文なし。本ノート §3.3 補題 C で証明**。依存は「(1.4) が**副有限群の**完全列で Ihara の分裂 $s$ が連続」という接基点理論の標準事実 + 2401 Rem 2.9 + H3 | 2405 §1.3 (1.4)(副有限群の完全列と明記)+ [15 §1.4] / 2401 Remark 2.9($E_{\hat m,\hat f}$ が単射準同型) |
| **H5** | 算術入力 | $G_{\mathbf Q}$ は**非可解な有限連続商**をもつ(例: $\mathrm{Gal}(L/\mathbf Q)\cong S_5$)。 | **古典**(正典外)。§3.4 に**自前の完全な witness と検算**あり — 引用に依存しない | Hilbert 既約性定理(Hilbert 1892)/ 明示witness $x^5-x-1$(Selmer)+ Dedekind の分解定理 |

### 2.1 枠組み札(TB1/TB3/TB4ᵘ/A3)との突合

**結論: W-Exist が触れる枠組み札は (TB1)(TB3) の棚の一点だけであり、(TB2)(TB4)(TB4$^{\rm u}$)(A3) は使わない。**

- 使う唯一の枠組み事実は **H4 の中の「$G_{\mathbf Q}$ の $\widehat F_2$ への作用が連続」**である。これは `docs/week4-BFC攻略_opus_v1.md` §2 の **(TB1)(繊維関手・Grothendieck–Galois 同値)+(TB3)($\pi_1(U_{\bar{\mathbf Q}},\vec{01})\cong\widehat F_2$)** が置いている棚と**同じ棚**(接基点繊維関手の標準事実)。さらに言えば 2405 §1.3 が (1.4) を**副有限群の完全列**として自ら書いているので、W-Exist に関する限り**正典の内側**で足りる。
- **(TB2)**($\zeta$ 系と基点規約)は不要 — W-Exist は $x$ の向きも Kummer 指標も使わない。
- **(TB4)/(TB4$^{\rm u}$)**(慣性の正規化)は不要 — 同上。**文献関所 `FRAMEWORK-UNKNOWN` を W-Exist は踏まない**(`docs/manifest_k5_v1_7.md` の「(TB4) は現在も文献関所」に該当しない)。
- **(A3)**(位相/étale 比較・Deligne 1989 §15)は不要 — 比較定理の向きは W-Exist の主張に一切入らない。

> ★ **報告に値する事実**: **W-Exist の枠組み依存は K5/BFC キャンペーンより真に軽い。** BFC 側は (TB1)–(TB4)+(CAL)+(W1)–(W5) を要したが、W-Exist は「$G_{\mathbf Q}\curvearrowright\widehat F_2$ が連続」+ 正典 2 定理 + 古典 1 個で閉じる。壁キャンペーンの冒頭定理として**依存が薄い**のは設計上の利点である。

### 2.2 (W2) との照合(委嘱項目 4 の前段)

`docs/week4-BFC攻略_opus_v1.md` §3 の **(W2)** は $1\to\mathfrak F_0\to GT(N)\xrightarrow{\tilde\chi}(\mathbb Z/2M)^\times\to1$ を置く($M=\mathrm{ord}(X)$)。Sol の「$\operatorname{Im}\widetilde\chi\subseteq(\mathbb Z/2M)^\times$」はこの工房内表記に従ったもの。**正典の表記は別**:

$$ \chi_{{\rm vir},N}([m,f]) := 2m+1+N_{\rm ord}\mathbb Z\ :\ GT(N)\longrightarrow(\mathbb Z/N_{\rm ord}\mathbb Z)^\times \qquad\text{(2405 (1.9))} $$

**法が $2M$ か $N_{\rm ord}$ かは W-Exist の結論に影響しない**(どちらも可換群だから)。ただし定義ノート §4 の較正項目 4 が「$m$ の法 $N_{\rm ord}$ と $u=2m+1$ の法 $2n$ を混同しない」と明示的に警告している箇所なので、**論文執筆時は正典の (1.9) を正本にすべき**(訂正提案 §8-③)。

---

## 3. 補修した証明

記号: 「$G$ が prosolvable」= $G$ は副有限群で、**すべての開正規部分群 $U$ について $G/U$ が可解**。

### 3.1 補題 A(逆極限)

> **補題 A.** $\{G_i\}_{i\in I}$ を有限**可解**群の逆系(添字は任意の小さい圏でよい)とし $L:=\varprojlim G_i$ とおく。**$L$ は prosolvable である。**
> **遷移写像の全射性は仮定しない。有向性も仮定しない。**

**証明.** $L$ は $\prod_i G_i$ の閉部分群である(各 $G_i$ は有限離散、compatibility 条件は閉条件)。$\prod_i G_i$ の $1$ の近傍基は「有限個の座標で $1$ に等しい元の集合」だから、$L$ の $1$ の**開近傍基**は
$$ K_S:=\ker\Bigl(L\to\prod_{i\in S}G_i\Bigr),\qquad S\subseteq I\ \text{有限} $$
で与えられる。$U\trianglelefteq L$ を開正規とすると、ある有限 $S$ について $K_S\subseteq U$。よって $L/U$ は $L/K_S$ の商であり、$L/K_S$ は有限可解群 $\prod_{i\in S}G_i$ の部分群である。可解性は部分群・商群に遺伝するから $L/U$ は可解。∎

**注(重要)**: 補題 A は「$L$ が可解」を主張**しない**。導来長が非有界なら $L$ は prosolvable だが可解ではない。Sol の証明もこの区別を正しく守っている(矛盾を導く相手は「$G_{\mathbf Q}$ の可解性」ではなく「$G_{\mathbf Q}$ の**有限商**の可解性」)。

### 3.2 補題 B(部分群への遺伝 — 位相込み)

> **補題 B.** $L$ が prosolvable、$H$ が副有限群、$\iota:H\to L$ が**連続な単射準同型**とする。このとき $H$ のすべての有限連続商は可解である(= $H$ は prosolvable)。

**証明.** $H$ はコンパクト、$L$ は Hausdorff だから $\iota$ は像への同相であり、$\iota(H)$ は $L$ の閉部分群。$U\trianglelefteq H$ を開正規とすると $\iota(U)$ は $\iota(H)$ の開部分群だから、ある開正規 $V\trianglelefteq L$ について $\iota(H)\cap V\subseteq\iota(U)$。したがって
$$ H/U\ \cong\ \iota(H)/\iota(U)\ \text{は}\ \iota(H)/(\iota(H)\cap V)\ \hookrightarrow\ L/V $$
の商。$L/V$ は補題 A より可解、可解性は部分群・商に遺伝するから $H/U$ は可解。∎

### 3.3 補題 C(欠落 X の補修 — Ih の連続性)

> **補題 C.** $\mathrm{Ih}:G_{\mathbf Q}\to\widehat{GT}_{\rm gen}$ は連続である($\widehat{GT}_{\rm gen}$ は $\widehat{\mathbb Z}\times\widehat F_2$ からの部分空間位相)。

**証明.**

1. **$\widehat{GT}_{\rm gen}$ はコンパクト位相群**。H3(2401 Thm 5.2 + Rem 5.3)より $\widehat{GT}_{\rm gen}\cong\varprojlim(\mathrm{ML})$(同相)、右辺は有限離散群の積の閉部分空間ゆえコンパクト。
2. **$E:\widehat{GT}_{\rm gen}\to\operatorname{Aut}(\widehat F_2)$ は連続単射準同型**。単射性は 2401 **Remark 2.9**。連続性: 任意の開特性部分群 $U\trianglelefteq\widehat F_2$ に対し、$E_{\hat m,\hat f}$ の $\widehat F_2/U$ 上への誘導は
 $$ x\mapsto x^{2\hat m+1},\qquad y\mapsto \hat f^{-1}y^{2\hat m+1}\hat f $$
 の $U$ を法とした像で決まり、これは $(\hat m,\hat f)$ の連続関数。$\widehat F_2$ は位相的有限生成だから $\operatorname{Aut}(\widehat F_2)$ は合同位相で副有限(Hausdorff)。
3. 1+2 とコンパクト性より **$E$ は像への同相**、ゆえに $E^{-1}:E(\widehat{GT}_{\rm gen})\to\widehat{GT}_{\rm gen}$ は連続。
4. **$\rho:G_{\mathbf Q}\to\operatorname{Aut}(\widehat F_2)$ は連続**。2405 §1.3 の (1.4) は**副有限群の**完全列であり、Ihara [15 §1] の分裂 $s$ を用いて $\rho(g)=\mathrm{conj}_{s(g)}|_{\widehat F_2}$。$(g,w)\mapsto s(g)ws(g)^{-1}$ は副有限群 $\pi_1(\mathbf P^1_{\mathbf Q}\smallsetminus\{0,1,\infty\})$ の中の連続演算の合成だから連続、よって各 $\widehat F_2/U$ への誘導はコンパクト性より開核をもつ。
 【この一点だけが接基点理論の標準事実(= (TB1)(TB3) の棚)。2026-07-28 裁可により自前再導出しない。】
5. (1.5) の定義そのものから $\rho=E\circ\mathrm{Ih}$($\rho(g)(x)=x^{\chi(g)}$、$\rho(g)(y)=f_g^{-1}y^{\chi(g)}f_g$、$\chi(g)=2\hat m+1$)。よって
 $$ \mathrm{Ih}=E^{-1}\circ\rho\quad\text{は連続}. \qquad\blacksquare $$

### 3.4 算術入力(H5)— 自前 witness

> **事実.** $L\subset\bar{\mathbf Q}$ を $f(t)=t^5-t-1$ の分解体とすると $\mathrm{Gal}(L/\mathbf Q)\cong S_5$。ゆえに $G_{\mathbf Q}\twoheadrightarrow S_5$ は**連続**全射(Krull 位相の定義から)で、$S_5$ は非可解($A_5$ が非可換単純)。

**検算(Python 単系統・整数演算のみ。スクリプト: scratchpad `wexist_witness.py` / `wexist_irred.py`)**

| 検査 | 値 | 結論 |
|---|---|---|
| $\operatorname{disc}(t^5+at+b)=256a^5+3125b^4$、$a=b=-1$ | $\mathbf{2869}=19\cdot151$ | **平方数でない** ⇒ $\mathrm{Gal}\not\subseteq A_5$。**奇数**ゆえ $2\nmid\operatorname{disc}$ |
| $\mathbf F_2$ 上 $(t^2+t+1)(t^3+t^2+1)$ | $=t^5+t+1=f \bmod 2$、両因子とも $\mathbf F_2$ に根なし(既約) | Dedekind ⇒ **Frobenius の型は $(2,3)$** ⇒ その $3$ 乗は**互換** |
| $f$ の有理根 | なし | — |
| $f$ の $\mathbf Z$ 上 $\deg2\times\deg3$ 分解 | 係数消去で**存在しない**(範囲探索でなく制約解: $b e=-1,\ c=-a,\ d=a^2-b$ を $x^1$ 式に代入 → $a\in\{0,1\}$、いずれも $x^2$ 式を破る) | ⇒ $\mathbf Z$ 上既約 ⇒ Gauss より $\mathbf Q$ 上既約 |

**組み立て**: $f$ 既約 ⇒ $G:=\mathrm{Gal}(L/\mathbf Q)\le S_5$ は推移的 ⇒ $5\mid|G|$ ⇒ Cauchy より $5$-巡回 $\sigma\in G$。互換 $\tau=(a\,b)\in G$。$\sigma$ は $5$-巡回だから $\sigma^j(a)=b$ なる $j\not\equiv0$ があり、$\sigma^j$ も $5$-巡回。点をラベルし直して $\tau=(1\,2)$、$\sigma^j=(1\,2\,3\,4\,5)$ としてよい。$\sigma^j$ で $\tau$ を共役すれば全ての $(i\ i{+}1)$ が得られ、これらは $S_5$ を生成する。ゆえに $G=S_5$。∎
(補助確認: 総当たりで $S_5$ の導来列 $S_5\supset A_5=A_5'$ が停止 = **非可解**、$S_4$ の導来長 $=3$ を機械確認済み。)

### 3.5 定理の組み立て

**証明(W-Exist 前半).** 背理法。すべての $N\in\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$ について $GT(N)$ が可解と仮定する。$GT(N)$ は有限群(H3)なので、補題 A より $L:=\varprojlim(\mathrm{ML})$ は prosolvable。H3 の同相 $\Psi$ と H1・H2・**補題 C** により
$$ G_{\mathbf Q}\ \xrightarrow[\ \text{連続単射}\ ]{\ \mathrm{Ih}\ }\ \widehat{GT}_{\rm gen}\ \xrightarrow[\ \cong\ ]{\ \Psi\ }\ L $$
は連続単射準同型。$G_{\mathbf Q}$ は副有限だから補題 B より $G_{\mathbf Q}$ のすべての有限連続商は可解。しかし §3.4 より $G_{\mathbf Q}\twoheadrightarrow S_5$ は非可解な有限連続商。矛盾。ゆえにある isolated $N$ で $GT(N)$ は非可解。∎

---

## 4. 核の非可解性(委嘱項目 4)

> **系.** isolated $N$ について $GT(N)$ が非可解なら $\ker\widetilde\chi_N$ も非可解。

**確認.** $\chi_{{\rm vir},N}:GT(N)\to(\mathbb Z/N_{\rm ord}\mathbb Z)^\times$ は群準同型(2405 (1.9))。準同型であることの根は合成則 (3.53) の $m$-成分:
$$ 2\bigl(2m_1m_2+m_1+m_2\bigr)+1=(2m_1+1)(2m_2+1) $$
— これは $\mathbb Z$ の中の**恒等式**なので、法が $N_{\rm ord}$ でも $2N_{\rm ord}$ でも $2M$ でも準同型性は保たれる。よって
$$ 1\to\ker\widetilde\chi_N\to GT(N)\to\operatorname{Im}\widetilde\chi_N\to1,\qquad \operatorname{Im}\widetilde\chi_N\ \text{は可換群の部分群ゆえ可換}. $$
$\ker\widetilde\chi_N$ が可解なら「可解群による可換群の拡大」で $GT(N)$ は可解。対偶より $\ker$ も非可解。∎

**判定: Sol の §1 発案札 A 後半は PASS(無条件・正典 (1.9) のみに依存)。** 法の表記だけ §2.2 の通り。

**系の帰結の scope 訂正**: Sol は「全 finite gentle 窓で hexagon が $\ker\widetilde\chi$ を可解に強制する一般定理は存在し得ない」と書くが、正しくは **「全 *isolated* 窓で」**。非 isolated 窓の isotropy 群 $GTSh(N,N)$ については本論法は何も言わない(§6)。

---

## 5. 反駁の試み(委嘱項目 5)

### R-1【DEFEATED】遷移写像 $R_{N,H}$ が全射でないと prosolvable 議論は壊れるか

**壊れない。** 補題 A は全射性も有向性も使っていない — $\varprojlim$ が積の**閉部分群**であることだけを使う。非全射性は $\varprojlim$ を**小さく**する方向にしか効かず、本論法は $\varprojlim$ の複雑さの**上界**を使っているので無害。
なお別ルートで安全でもある: isolated poset は Prop 3.15(交わりで閉じる)により有向、Prop 3.14 により cofinal であり、そもそも $\Psi$ が同型であることは H3 が保証している。

### R-2【欠落 X の正体・DEFEATED but LOAD-BEARING】「閉部分群として埋まるだけで十分か」— 抽象部分群では**不十分**

委嘱が名指しした通り、ここが本命題の唯一の危険箇所である。

> **反例(抽象版の議論は偽).** $F_2$ は residually finite-$p$(Magnus)なので、自然な写像 $F_2\hookrightarrow\varprojlim_{\ }\{$有限 $p$-群商$\}=\widehat{F_2}^{(p)}$ は**単射**。右辺は pro-$p$ ゆえ pronilpotent、特に **prosolvable**。ところが $F_2\twoheadrightarrow S_5$($(1\,2)$ と $(1\,2\,3\,4\,5)$ が生成)。
> **⇒「prosolvable 群に抽象部分群として埋まる群の有限商は可解」は偽。**

したがって Sol の「閉部分群も prosolvable」は、**像が閉である(= $\mathrm{Ih}$ が連続でありコンパクト性が効く)ことを暗黙に使っている**。これを明示しないと、上の $F_2$ 反例と論法上区別がつかない。

**閉じ方**: 補題 C(§3.3)。$G_{\mathbf Q}$ はコンパクトなので、**連続性さえ言えれば閉性は自動**(コンパクト → Hausdorff の連続単射は像への同相)。よって補修後は DEFEATED。

**なぜこれが「重い」か**: 連続性を捨てた版で救おうとする自然な試み — 「$\ker(\mathrm{Ih}_N)$ は有限指数正規部分群で交わりは自明だから residually solvable」— は上の $F_2$ 反例と同型の構造をもち、**救えない**。有限指数だが開でない部分群の可能性を排除できないためである($G_{\mathbf Q}$ は位相的有限生成でないので Nikolov–Segal も Serre の定理も使えない)。

### R-3【DEFEATED / 仮定に格上げ】Belyi 単射性を弱めたらどうか

論法が真に必要とするのは「$\mathrm{Ih}(G_{\mathbf Q})$ が非可解な有限連続商をもつ」だけで、単射性はその十分条件にすぎない。しかし単射性を落とすと $\ker(\mathrm{Ih})$ が $S_5$-商を潰す可能性を排除できず、**論法は成立しない**。よって H1 は本質的仮定として表に残す(正典が Belyi で閉じているので実務上の危険はない)。

### R-4【DEFEATED】$\widetilde\chi$ の法の取り違えで系が壊れるか

壊れない(§4)。準同型性は $\mathbb Z$ 上の恒等式に由来し、像は任意の法で可換。

### R-5【UNKNOWN(部分的に閉じた)】非 isolated 窓の isotropy 群への転送

§6 に分離。**結論の非 isolated 窓への拡張は得られない**(UNKNOWN)。ただし逆向きの転送は部分的に証明できた(命題 T)。

### R-6【NOTE】規約リスク — 「同じ $GT(N)$ か」

W-Exist は**紙の $GT(N)$** についての定理である。壁キャンペーンが機械計算する $G_N$ が同じ対象であるためには、定義ノート §1.5 の語規約 W-1〜W-4(特に **(H-b′) の向き敏感性**)を実装が守っていることが前提。**理論の存在保証は実装の規約バグを免除しない。**

### R-7【DEFEATED】「導来長が非有界なだけで実は全部可解」ではないか

補題 A は導来長の一様上界を要求しないので、この抜け道はない。逆に、$G_{\mathbf Q}$ が**可解でない**ことではなく **非可解な有限商をもつ**ことを使っている点が本質。「全窓可解 ⇒ $G_{\mathbf Q}$ 可解」という(誤った)強い形を主張していないのは Sol の証明の正しい所である。

---

## 6. 「isolated に限る」の必要性(委嘱項目 3)

### 6.1 なぜ逆極限が isolated 窓に限られるか(3 つの独立な理由)

1. **群でないと関手にならない**: $GT(N)=GTSh(N,N)$ は $N$ が isolated のときのみ(2401 Def 3.13 直後)。
2. **遷移射が準同型にならない**: $R_{N,H}$ が群準同型なのは $N,H$ **両方**が isolated のとき(2401 Remark 3.16)。
3. **近似写像が準同型にならない**: 2405 **Remark 1.4** — 「if the object $N$ is not isolated … $GT(N)$ does not have a natural group structure, so $\mathrm{Ih}_N$ is not a group homomorphism」。Thm 5.2 の証明も「$N^{(\hat m,\hat f)}=N$ **since $N$ is isolated**」を冒頭に置く。

正当化は Prop 3.14(isolated 部分 poset は cofinal)+ Prop 3.15(交わりで閉じる)であり、**cofinal だからこそ isolated だけで $\widehat{GT}_{\rm gen}$ を全部捉えられる**。

### 6.2 結論は非 isolated 窓に及ばない

- **型として及ばない**: 非 isolated $N$ で「$GT(N)$ が非可解」は無意味(集合)。
- **isotropy 群にも及ばない**: $GTSh(N,N)$ は任意の $N$ で群だが、$\varprojlim(\mathrm{ML})$ から $GTSh(N,N)$ への簡約準同型が一般には存在しない。理由は 2401 (4.2)/Thm 4.4: $\mathrm{PR}_N(\hat m,\hat f)$ は **$N^{(\hat m,\hat f)}:=\ker(\widehat P_N\circ T_{\hat m,\hat f}|_{B_3})$ から $N$ への射**であって、$N$ が isolated でなければ $N^{(\hat m,\hat f)}=N$ とは限らない(Thm 5.2 の証明冒頭がまさにこの一致に isolated 性を使う)。すなわち $\mathrm{PR}_N$ の像は $GTSh(N,N)$ に入るとは限らない。**論法は沈黙する。**

### 6.3 逆向きの転送(部分的に証明できたこと)— 命題 T

キャンペーンは(v1.2 の型修理により)非 isolated 窓でも $G_N=GTSh(N,N)$ を計算しうるので、「そこで非可解を見つけたら W-Exist の窓を得たことになるか」を確かめておく価値がある。

> **命題 T(本ノートの副産物・paper-proof candidate).** $N\in\mathrm{NFI}_{PB_3}(B_3)$、$N^\diamond\le N$ をその連結成分の交わり(Prop 3.14 より isolated)とする。$[m,f]\in GT(N^\diamond)=GTSh(N^\diamond,N^\diamond)$ に付随する $\bar\alpha_{[m,f]}\in\operatorname{Aut}(B_3/N^\diamond)$ を取り
> $$ \mathrm{Stab}_N:=\{[m,f]\in GT(N^\diamond)\ :\ \bar\alpha_{[m,f]}(N/N^\diamond)=N/N^\diamond\} $$
> とおく。$\mathrm{Stab}_N$ は $GT(N^\diamond)$ の**有限指数部分群**であり、reduction $R_{N^\diamond,N}$ はその上で**群準同型 $\mathrm{Stab}_N\to GTSh(N,N)$** を与える。
> ゆえに $R_{N^\diamond,N}(\mathrm{Stab}_N)$ が非可解なら $GT(N^\diamond)$ は非可解(= **W-Exist の witness が得られる**)。

**証明.** $[m,f]\in GTSh(N^\diamond,N^\diamond)$ に対し $T_{m,f}:B_3\to B_3/N^\diamond$ は核 $N^\diamond$ の全射だから $\bar\alpha\in\operatorname{Aut}(B_3/N^\diamond)$ を誘導する。Prop 3.12 の可換図式 (3.59) より $T_{m,f,N}=P_{N^\diamond,N}\circ T_{m,f}$、よって
$$ \ker T_{m,f,N}=T_{m,f}^{-1}(N/N^\diamond)=P_{N^\diamond}^{-1}\bigl(\bar\alpha^{-1}(N/N^\diamond)\bigr), $$
これが $N$ に等しいことと $\bar\alpha(N/N^\diamond)=N/N^\diamond$ は同値。$[m,f]\mapsto\bar\alpha_{[m,f]}$ は合成 (3.53) が $T$ の合成に対応することから**(反)準同型**であり(向きは 2401 (2.25) と工房の $rs=s*r$ 慣習のどちらを取るかで決まるが、以下は向きに鈍感)、部分群の固定化群である $\mathrm{Stab}_N$ はどちらの向きでも部分群。指数は $N/N^\diamond$ の $\bar\alpha$-軌道の長さ以下で有限。$R_{N^\diamond,N}$ は代表元 $(m,f)$ をそのまま使う写像で合成則も代表元で定義されるから、$\mathrm{Stab}_N$ 上で準同型。最後の主張は「可解群の部分群は可解」の対偶。∎

> **【UNKNOWN】** 逆は言えない。$GTSh(N,N)$ が非可解でも、非可解性の witness が $R_{N^\diamond,N}(\mathrm{Stab}_N)$ **の外側**(= genuine でない shadow を含みうる真部分集合の外)にあれば、$GT(N^\diamond)$ の非可解性は従わない。**キャンペーン運用への含意: 非 isolated 窓で NONSOLVABLE 札が立ったら、その witness が $\mathrm{Stab}$ の像に入るかを別途証明書化する必要がある**(入らなければ W-Exist の witness としては使えず、当該窓の isolated 細分 $N^\diamond$ を直接計算する必要がある)。

---

## 7. 副産物 — 「非 metabelian 窓」も存在保証されている(安い階梯)

補題 A の証明は「有限可解群の有限積の部分群・商は可解」だけを使うので、**可解性を導来長 $\le d$ に置き換えてもそのまま通る**(導来長 $\le d$ の群のクラスも部分群・商・有限積で閉じる)。よって:

> **系 W-Exist-$d$.** 各 $d\ge1$ について、$G_{\mathbf Q}$ が導来長 $>d$ の有限連続商をもつならば、ある isolated $N$ で $GT(N)$ の導来長は $>d$(または非可解)。
>
> **系 W-Meta($d=2$).** **非 metabelian な isolated 窓が存在する。** 算術入力は $S_4$ の $\mathbf Q$ 上実現だけでよい。

**$S_4$ の witness(自前検算済み)**: $t^4-t-1$。有理根なし・$\mathbf Z$ 上 $\deg2\times\deg2$ 分解なし ⇒ 既約。$\operatorname{disc}=-27p^4+256q^3=\mathbf{-283}$(平方数でない ⇒ $\not\subseteq A_4$)。分解三次式 $t^3-4qt-p^2=t^3+4t-1$ は有理根なし ⇒ 既約 ⇒ $\mathrm{Gal}\in\{S_4,A_4\}$ ⇒ $S_4$。$S_4$ の導来長 $=3$(機械確認済み)。

> ★ **キャンペーンへの含意**: 現 atlas の「全 14 対象 metabelian」は**低い帯の現象**であるという Sol の判断は、非可解性(S₅ 相当)より**弱い算術入力**でも既に裏づけられる。すなわち「非 metabelian 窓を探す」段階の目標も**存在が保証済み**であり、探索は存在賭けではない。ただし**指数の上界は依然出ない**(§8-② 参照)。

---

## 8. Sol の文言への訂正提案(便 79 に載せる候補)

| # | 箇所 | 提案 |
|---|---|---|
| ① | 発案札 A の証明本文 | 「その逆極限は prosolvable であり、その閉部分群も prosolvable」の前に **「$\mathrm{Ih}$ は連続だから $G_{\mathbf Q}$ の像はコンパクト、ゆえに閉部分群」** を挿入。補題 C を脚注に。**理由: 抽象群版は偽(§5 R-2 の $F_2$ 反例)** |
| ② | 「最初の指数の定量的上界はこの議論から出ない」 | 同意。加えて **「導来長の階梯(§7)により非 metabelian 窓の存在も同時に従う」**を併記すると、band 設計の動機が強くなる |
| ③ | $\operatorname{Im}\widetilde\chi\subseteq(\mathbb Z/2M)^\times$ | 正典表記は $(\mathbb Z/N_{\rm ord}\mathbb Z)^\times$(2405 (1.9))。工房内 (W2) 表記と併記し、**法の混同禁止**(定義ノート §4 項目 4)を注記 |
| ④ | 「全 finite gentle 窓で…一般定理は存在し得ない」 | **「全 *isolated* 窓で」** に限定(§4 末尾・§6) |
| ⑤ | ★教材 1 | 「逆極限は探索の存在保証になる」に **「ただし位相込みで」** を追加。抽象的な residual 性では保証にならない |

---

## 9. 未閉鎖項・UNKNOWN の悉皆

- **【U-1】** H2($\widehat{GT}\le\widehat{GT}_{\rm gen}$)の根拠(pentagon $\Rightarrow \hat f\in[\widehat F_2,\widehat F_2]^{\rm cl}$)は **2401 が引用で済ませている**(定義ノート §5 確認質問 2 が既に指摘)。当工房未再導出。**身分 = 正典の明言**として使用。
- **【U-2】** H4 の依存点「(1.4) の分裂 $s$ が連続な副有限群の分裂」は接基点理論の標準事実(枠組み棚)。2026-07-28 裁可により自前再導出しない。**補題 C はこの一点に依存する。**
- **【U-3】** 命題 T の逆(非 isolated 窓の非可解 isotropy ⇒ isolated 窓の非可解)は **UNKNOWN**(§6.3)。
- **【U-4】** 本ノートの検算は Python 単系統(初等整数演算)。**cross-checked ではない。** 第二 lane(GAP の `GaloisType`/`DerivedSeries`)での再現は未了。
- **【U-5】** 補題 A・B・C、命題 T はいずれも **paper-proof candidate**。Lean 化していない。

### 【文献要請】(低優先・論文執筆段で効く)

> **困難**: Ihara 埋込 $\mathrm{Ih}:G_{\mathbf Q}\to\widehat{GT}$(および $\widehat{GT}_{\rm gen}$)が**位相群の連続準同型/閉埋込である**ことを明記した文献が、当工房の正典(2401 / 2405)には見当たらない。両論文は単射性(Belyi)しか述べていない。本ノート §3.3 は自前で閉じたが、W-Exist を論文の冒頭定理に置くなら**引用可能な一文**が欲しい。
> **欲しい結果の型**: 「$\mathrm{Ih}$ is a continuous injective homomorphism of profinite groups(または: a closed embedding)」を定理・注意の形で述べた出典。候補の当たり: Ihara 1994 §1、Pop の survey(2401 の [25])§4.7、Schneps の ĜT サーベイ、Lochak–Schneps。
> **代替**: 「$G_{\mathbf Q}\to\operatorname{Aut}(\widehat F_2)$(接基点つき)が連続」を明記した出典でも補題 C は閉じる。

---

## 10. 監査範囲

- 読んだもの: `sol/sol_reply_78_math5.md` 全文、`docs/week1-定義ノート.md` 全文、`provenance/registered/universe_wall_v1.md`、`docs/week4-BFC攻略_opus_v1.md` §2–§3(TB/W 札の原文)、`papers/txt/2401.06870`(§2 Rem 2.6–2.10、§3.1–3.2 Prop 3.12/3.14/3.15/Rem 3.16、§5 全体・Thm 5.2 の証明)、`papers/txt/2405.11725`(Abstract、§1 冒頭、§1.3・§1.3.1・Rem 1.4/1.5)、memory の framework-assumptions-policy。
- **やっていないこと**: PDF ページ画像による原文再照合(txt 抽出のみ)、GAP 実行、Lean 形式化、外部文献の探索(文献ゲート遵守 — §9 に要請として提出)。
- 本ノートは **candidate**。commit していない。
