# (U2)の証明 — $L_{2^\alpha}/\mathbb Q$ は $2$ の外不分岐。**混合側は奇側へ完全帰着する**

> **【ERRATUM — 裁定 306/P93-1(2026-08-01)】** 本稿 §3 の「2m+1≡1 (mod K_ord) ⟹ m≡0」は**偽**(偽解 m=2^{a-1} が χ_vir 不可視)。修理は `u2_unramified_bridge_v1_addendum_p93.md` が正本 — 本体は歴史的記録として不変。

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 委嘱: 司令塔(次波 3)「配達覚書 `docs/notes/litgate_u2_ihara_v1.md` の (U2-bridge) の証明を試みよ。検証 3 点 = R1-R3・**最大性 Question 6.5.2 は使用禁止**・moduli/定義体の区別に注意」
- 入力: `ops/inbox_hunter/ihara_ICM1990_braids_galois.pdf`(**§5.2 のみ使用・reader による頁画像照合済**)/ `docs/week1-定義ノート.md` §2–§3(正典)/ `docs/notes/n12_goursat_v1.md` §7.1(U2 の役割)
- **AI1988 本体は使わない**(未入手のまま結論に到達した — ILL 不要)。**Question 6.5.2(最大性)は使わない**。**「被覆の定義体」も「moduli 体」も一度も使わない**(§2 の設計判断)。

---

## 0. 結論(先に 5 行)

| # | 主張 | 格 |
|---|---|---|
| **①** | **定理 U2-BR**: 窓 $K$ が「$K_{\rm ord}$ が $2$ 冪」かつ「$F_2/K_{F_2}$ が有限 $2$-群」を満たせば、$\ker\bigl(G_{\mathbb Q}\to\mathrm{Out}\,\widehat F_2^{(2)}\bigr)\subseteq\ker\mathrm{Ih}_K$ | **定理**(証明 §3・5 行) |
| **②** | ⟹ $L_K\subseteq\mathbb Q^{(2)}(\infty)$(Ihara の塔)⟹ **$L_K/\mathbb Q$ は $2$ の外不分岐** | **定理**(§4・前件 = ICM §5.2) |
| **③** | $K=K^{(2^\alpha)}$ は①の前件を満たす($K_{\rm ord}=2^\alpha$、$\lvert G_{2^\alpha}\rvert=2^{3\alpha-1}$ — 正典 §3)⟹ **(U2) 成立** | **定理** |
| **④** | ⟹ `n12_goursat_v1.md` §7.1 の十分条件が発効 ⟹ **定理 MIX の前件 (c) が全 $\alpha\ge2$・全奇 $n_0>1$ で成立** ⟹ **dihedral 予想は完全に奇側へ帰着** | **定理**(MIX の他の枠組前件は継承) |
| **⑤** | 覚書の提案経路(「$L_{2^\alpha}$ が $X(S_0)$ 対象の定義体塔の有限段に入る」)は**採らない**。定義体経由は降下(descent)の穴を負う。**核どうしの比較**で直接閉じるほうが短く、R3(moduli/定義体)の危険を**構造的に回避**する | **設計判断** |

> **一行で**: 「$L$ が塔の中にあるか」を**体の言葉で**問うと定義体・moduli・降下の泥沼に入る。**表現の核の言葉で**問い直すと、$\chi$ の pro-$2$ 成分と $f_\sigma\in[\widehat F_2,\widehat F_2]$ の 2 つだけで 5 行で閉じる。

---

## 1. 使う道具の棚卸し(前件の明示)

| # | 前件 | 内容 | 出所 | 格 |
|---|---|---|---|---|
| **U2-A** | 自由 pro-$p$ 群の中心化群 | 階数 2 の自由 pro-$2$ 群 $F$ と基底 $x$ について $C_F(x)=\overline{\langle x\rangle}\cong\mathbb Z_2$ | 古典(Ribes–Zalesskii, *Profinite Groups*, 自由 pro-$p$ 群の中心化群は procyclic)。**正典外・Lean 化せず Mathlib 待ち枠** | **classical**(外部) |
| **U2-B** | $f_\sigma$ の可換子性 | $\widehat{\mathrm{GT}}_{\rm gen}$ の定義が $\hat f\in[\widehat F_2,\widehat F_2]^{\rm cl}$ を含み、$G_{\mathbb Q}\hookrightarrow\widehat{\mathrm{GT}}\subseteq\widehat{\mathrm{GT}}_{\rm gen}$ | **正典**(定義ノート §2「gentle の意味」) | **canonical** |
| **U2-C** | $\mathrm{Ih}_K$ の成分 | $\mathrm{Ih}_K(\sigma)=[m,f]$、$2m+1\equiv\chi(\sigma)$($\bmod K_{\rm ord}$ 資格)、$f\equiv f_\sigma$($\bmod K_{F_2}$) | **正典**(定義ノート §2 Def 3.1/§3;$\chi_{\rm vir}([m,f])=2m+1\bmod N_{\rm ord}$) | **canonical** |
| **U2-D** | Galois 作用の公式 | $\sigma(x)=x^{\chi(\sigma)}$、$\sigma(y)=f_\sigma^{-1}y^{\chi(\sigma)}f_\sigma$(接ベクトル基点 $\overrightarrow{01}$ での **Aut** 表現) | Ihara ICM (2.3.2)(**配達済・頁画像照合済**)。正典の hexagon もこの形 | **delivered** |
| **U2-E** | 塔の定義 | $\mathbb Q^{(2)}(\infty)$ = $\ker\bigl(\varphi_{X_4}^{(2)}:G_{\mathbb Q}\to\mathrm{Out}(\widehat F_2^{(2)})\bigr)$ の固定体 | Ihara ICM §5.2 (5.2.1) 直後(**頁画像照合済**) | **delivered** |
| **U2-F** | 塔の不分岐性 | 「$\mathbb Q^{(l)}(\infty)$ は $\mathbb Q(\mu_{l^\infty})$ 上 pro-$l$ 拡大で **$l$ の外不分岐**」。**$l$ に条件は付いていない**($l=2$ を除外していない) | Ihara ICM §5.2 p.112(**頁画像照合済**) | **delivered** |
| **U2-G** | 窓の数値 | $\lvert G_n\rvert=4n^3$($n$ 奇)$/\ 4(n/2)^3$($n$ 偶)、$K_{\rm ord}=\mathrm{lcm}(n,2)$、$G_n\cong F_2/K^{(n)}_{F_2}$ | **正典**(定義ノート §3・GAP 検算済 $n=3..12$) | **canonical** |

**使わないもの**(明示):
- **Question 6.5.2**(塔の最大性 — 未解決)**を使わない**。使うのは「塔の中は不分岐」という**許された向きだけ**。
- **AI1988 本体**を使わない(higher circular $l$-units・$E^{(l)}$・Corollary [A-I₁] は**一度も現れない**)。
- **「被覆の定義体」「moduli 体」を使わない**(§2)。
- **Coleman 1989 / Vogel 2005 を使わない**(前者は meta-abelian 層で射程外、後者は (U2) 成立**後**の構造論)。

> **★ reader の記号訂正の反映**: 配達覚書の「$\Omega^{(\ell)}(m)$」は ICM1990 には存在しない。塔の記号は **$\mathbb Q^{(l)}(m)$** である($\Omega$ は同論文 p.100 で「一般の定義体」を表す汎用記号)。本稿は $\mathbb Q^{(2)}$ を使う。

---

## 2. 設計判断 — なぜ「定義体の塔」経由を採らないか

配達覚書 §2 の提案は
> (U2-bridge) $L_{2^\alpha}$ は $X(\{0,1,\infty\})$ の対象の**定義体塔**のある有限段に含まれる

だった。この形は 3 つの荷物を負う:

1. **降下(descent)の穴**: ICM p.100 は「被覆・射・基点上の点がすべて $\Omega$ 上定義されているなら $G_{\mathbb Q}$ は $\mathrm{Gal}(\Omega/\mathbb Q)$ 経由で作用する。**逆も $\pi_1$ の完備化の中心が自明なら成立**」と書く。逆向き(核 ⟹ 定義体)には**中心自明性 + 降下**が要り、有限段($\widehat F_2^{(2)}/\widehat F_2^{(2)}(m{+}1)$ は冪零 = 中心非自明)では**この括弧書きが効かない**。
2. **R3(moduli 体 vs 定義体)**: 定義体を語る限りこの区別が常につきまとう(v4 戦訓)。
3. **塔が pro-$l$ 専用**: ICM の塔は $l$ 冪被覆しか扱わない。dihedral は $n$ が奇なら非 $2$-群 — reader 報告どおり **ICM に dihedral の言及はゼロ**。

**本稿の経路はこの 3 つを全部回避する。** 主張を「体の包含」ではなく
$$\ker\bigl(\text{塔を定める表現}\bigr)\ \subseteq\ \ker\mathrm{Ih}_K$$
という**核の包含**に書き換える。核の包含は固定体の逆向き包含と同値であり($L_K\subseteq\mathbb Q^{(2)}(\infty)$)、**被覆も定義体も moduli も一度も登場しない**。残るのは「$\mathrm{Out}$ 表現の核の元が $\mathrm{Ih}_K$ で消えるか」という純粋な群論の問いだけになる — そしてそれが §3 の 5 行である。

**(R2)(基点・内外作用の規約)は障害ではなく本題である**: 塔は $\mathrm{Out}$、$\mathrm{Ih}$ は接ベクトル基点 $\overrightarrow{01}$ での $\mathrm{Aut}$ の情報。$\mathrm{Out}$ の核は $\mathrm{Aut}$ の核より**大きい**ので、素朴には包含が**逆向きに出て失敗する**。§3 の補題 INN がまさにこのギャップを潰す段である。

---

## 3. 定理 U2-BR

$F:=\widehat F_2^{(2)}$(階数 2 の自由 pro-$2$ 群、基底 $x,y$ = $\pi_1$ の $0,1$ のまわりの生成元の pro-$2$ 像)。$\varphi^{(2)}:G_{\mathbb Q}\to\mathrm{Out}(F)$ を ICM §5.2 の外表現、$\chi_2:G_{\mathbb Q}\to\mathbb Z_2^\times$ を円分指標の pro-$2$ 成分とする。

> ### 補題 INN(本稿の核心・5 行)【定理】
> $\sigma\in\ker\varphi^{(2)}$ ならば
> $$\chi_2(\sigma)=1\qquad\text{かつ}\qquad f_\sigma=1\ \ \text{in}\ F .$$
> **証明.** $\sigma\in\ker\varphi^{(2)}$ とは、$\sigma$ が $F$ 上**内部**自己同型として働くこと: ある $g\in F$ で $\sigma\vert_F=\mathrm{conj}_g$($a\mapsto g^{-1}ag$)。$f$ を $f_\sigma$ の $F$ での像とする。U2-D より
> $$x^{\chi_2(\sigma)}=g^{-1}xg,\qquad f^{-1}y^{\chi_2(\sigma)}f=g^{-1}yg. \tag{$\ast$}$$
> 1. **$\chi_2(\sigma)=1$**: $(\ast)$ の第 1 式を可換化 $F^{\rm ab}=\mathbb Z_2\bar x\oplus\mathbb Z_2\bar y$ に落とす。内部自己同型は可換化に自明に働くから $\chi_2(\sigma)\bar x=\bar x$、$\mathbb Z_2\bar x$ は捻れ自由ゆえ $\chi_2(\sigma)=1$。
> 2. **$g\in\overline{\langle x\rangle}$**: 1. を $(\ast)$ 第 1 式に戻すと $x=g^{-1}xg$、すなわち $g\in C_F(x)$。U2-A より $C_F(x)=\overline{\langle x\rangle}$。
> 3. **$gf^{-1}\in\overline{\langle y\rangle}$**: 1. を $(\ast)$ 第 2 式に戻すと $f^{-1}yf=g^{-1}yg$、すなわち $gf^{-1}\in C_F(y)=\overline{\langle y\rangle}$(U2-A)。
> 4. **可換化で潰す**: $h:=gf^{-1}\in\overline{\langle y\rangle}$、$g\in\overline{\langle x\rangle}$、$f=h^{-1}g$。U2-B より $\bar f=0$ in $F^{\rm ab}$、よって $\bar g=\bar h$。ところが $\bar g\in\mathbb Z_2\bar x$、$\bar h\in\mathbb Z_2\bar y$ で、この 2 つの交わりは $0$。ゆえに $\bar g=\bar h=0$。
> 5. $\overline{\langle x\rangle}\cong\mathbb Z_2$ は $F^{\rm ab}$ に単射に入るから $\bar g=0\Rightarrow g=1$;同様に $h=1$。ゆえに $f=h^{-1}g=1$。∎

> ### 定理 U2-BR【定理】
> $K\in\mathrm{NFI}_{PB_3}(B_3)$ が
> $$\textbf{(H1)}\ K_{\rm ord}\ \text{は}\ 2\ \text{の冪},\qquad \textbf{(H2)}\ F_2/K_{F_2}\ \text{は有限}\ 2\text{-群}$$
> を満たし、$\mathrm{Ih}_K$ が定義されているとする。このとき
> $$\boxed{\ \ker\varphi^{(2)}\ \subseteq\ \ker\mathrm{Ih}_K\ }$$
> **証明.** $\sigma\in\ker\varphi^{(2)}$ とする。補題 INN より $\chi_2(\sigma)=1$、$f_\sigma\mapsto1$ in $F=\widehat F_2^{(2)}$。
> - **$m$ 成分**: (H1) と $\chi_2(\sigma)=1$ から $\chi(\sigma)\equiv1\pmod{K_{\rm ord}}$(法が $2$ 冪なので pro-$2$ 成分しか見ない)。ゆえに $2m+1\equiv1$、すなわち $m\equiv0$。
> - **$f$ 成分**: (H2) より、全射 $\widehat F_2\twoheadrightarrow F_2/K_{F_2}$ は**最大 pro-$2$ 商 $F$ を経由する**($2$-群への準同型は pro-$2$ 商を経由)。$f_\sigma$ の $F$ での像が $1$ だから $f_\sigma\in K_{F_2}$。
> ゆえに $\mathrm{Ih}_K(\sigma)=[0,1]$ = 単位元。∎

---

## 4. (U2) と、その先

> ### 系 U2(不分岐性)【定理・前件 U2-F】
> (H1)(H2) を満たし $\mathrm{Ih}_K$ が全射な窓 $K$ について、$L_K:=(\ker\mathrm{Ih}_K)$ の固定体は
> $$L_K\ \subseteq\ \mathbb Q^{(2)}(\infty)\qquad\text{かつ}\qquad L_K/\mathbb Q\ \text{は}\ 2\ \text{の外不分岐}.$$
> **証明.** 定理 U2-BR + U2-E で $L_K\subseteq\mathbb Q^{(2)}(\infty)$。U2-F で $\mathbb Q^{(2)}(\infty)/\mathbb Q(\mu_{2^\infty})$ は $2$ の外不分岐。$\mathbb Q(\mu_{2^\infty})/\mathbb Q$ は有限素点では $2$ でのみ分岐。$p\ne2$ を取ると、$p$ は $\mathbb Q^{(2)}(\infty)/\mathbb Q(\mu_{2^\infty})$ でも $\mathbb Q(\mu_{2^\infty})/\mathbb Q$ でも不分岐だから合成でも不分岐、その部分体 $L_K/\mathbb Q$ でも不分岐。∎
> **注(無限素点)**: ICM は archimedean 素点に触れていない(reader: UNKNOWN)。本稿の主張も**有限素点についてのみ**である。§5 の用途(円分体の部分体の導手比較)は有限素点だけで足りる。

> ### 系 U2-DIH(= 委嘱の (U2))【定理】
> $K=K^{(2^\alpha)}$($\alpha\ge2$)は (H1)(H2) を満たす:
> - (H1) $K_{\rm ord}=\mathrm{lcm}(2^\alpha,2)=2^\alpha$ ✓(U2-G)。
> - (H2) $F_2/K^{(2^\alpha)}_{F_2}\cong G_{2^\alpha}$、$\lvert G_{2^\alpha}\rvert=4\cdot(2^{\alpha-1})^3=2^{3\alpha-1}$ ✓(U2-G;$n=2^\alpha$ は偶)。
>
> $\mathrm{Ih}_{K^{(2^\alpha)}}$ は全射(正典 **Thm 5.3**)。よって
> $$\boxed{\ L_{2^\alpha}/\mathbb Q\ \text{は}\ 2\ \text{の外不分岐}\ }\qquad(\textbf{(U2)}).$$

> ### 系 MIX-ALL(混合側の完全帰着)【定理・MIX の他の枠組前件は継承】
> `n12_goursat_v1.md` §7.1 の
> > **十分条件 (U2)**: $L_{2^\alpha}/\mathbb Q$ が $2$ の外不分岐 $\Longrightarrow$ 前件 (c) が全 $\alpha\ge2$・全奇 $n_0>1$ で成立
>
> が発効する。従って
> $$\textbf{混合側 Conjecture 5.1}\ \Longleftarrow\ \textbf{奇側 Conjecture 5.1}.$$
> $2$ 冪側は正典 Thm 5.3 で既決だから、**dihedral 予想の未決部分は「奇数 $n_0$ の窓 $K^{(n_0)}$」だけになる**。
> **証明の再掲**($\S7.1$ より): $M:=L_{2^\alpha}\cap L_{n_0}$ は $\mathrm{Gal}(M/\mathbb Q)$ が $2$-群かつ $\mathrm{GT}(K^{(n_0)})\cong\mathrm{Aff}(\mathbb Z/n_0)\times C_2$ の商(導来部分群 $\mathbb Z/n_0$ は奇位数ゆえ落ちる)なのでアーベル、ゆえに $M\subseteq\mathbb Q(\zeta_{4n_0})$。系 U2-DIH で $M$ は $2$ の外不分岐、$\mathbb Q(\zeta_{4n_0})$ の $2$ の外不分岐な部分体は $\mathbb Q(\zeta_4)=\mathbb Q(i)$ に含まれる。$\mathbb Q(i)\subseteq M$ は既出。∎
> **継承する前件**: 定理 MIX の D-1〜D-8(isolated・Thm 5.3・$L_4=\mathbb Q(\zeta_8)$・定理 K3・fibre 積単射性・reduction 整合・Thm 4.6)。**本稿は【n12-GAP-1】だけを閉じる。**

---

## 5. 検証 3 点(要請票 R1/R2/R3)への逐条回答

| # | 要請票の問い | 本稿での扱い |
|---|---|---|
| **R1** | 実際の有限 quotient $G_{2^\alpha}$ を固定せよ | **固定した**。$G_{2^\alpha}\cong F_2/K^{(2^\alpha)}_{F_2}$、位数 $2^{3\alpha-1}$(正典 §3 の位数式・GAP 検算済)。使ったのは**「$2$-群である」という 1 点だけ**で、構造の詳細は不要 |
| **R2** | 基点・内外作用の規約を固定せよ | **これが本題だった**。塔 = $\mathrm{Out}$(ICM §5.2)、$\mathrm{Ih}$ = 接ベクトル基点 $\overrightarrow{01}$ での $\mathrm{Aut}$ データ(ICM (2.3.2))。**ギャップは補題 INN が潰す** — 内部自己同型として働く $\sigma$ に対し、$\chi_2=1$ と $f_\sigma\in[\ ,\ ]$ から共役元 $g$ 自身が $1$ に落ちる。**「$\mathrm{Out}$ の核 ⊆ $\mathrm{Aut}$ の核」がこの設定では成り立つ**、というのが結論 |
| **R3** | 実際の有限 Galois 拡大を固定せよ / 定義体と moduli 体を混同するな | **どちらも登場しない**。$L_K$ は「$\ker\mathrm{Ih}_K$ の固定体」として定義され、$\mathbb Q^{(2)}(\infty)$ も「$\ker\varphi^{(2)}$ の固定体」。被覆の定義体を一度も語らないので、**R3 の危険は構造的に消えている**(§2) |

**⟹ 覚書 §2 の 3 つの「要検証点」①②③のうち、① は R1 として済み、② は補題 INN で解決、③ は経路の選択で回避された。**

---

## 6. 独立の傍証(第二系統・**未監査**)

前件 U2-F(塔の不分岐性)は、実は文献引用なしでも標準的に得られる:

> $X=\mathbb P^1_{\mathbb Z}\setminus\{0,1,\infty\}$ は $\mathrm{Spec}\,\mathbb Z$ 上滑らかで幾何的連結な fiber をもつ($0,1,\infty$ は**すべての** $p$ で相異なるまま)。$p\ne l$ なら Grothendieck の特殊化定理により、$\pi_1^{\rm geom}$ の**素な部分 $l$-成分**は特殊化で不変。従って $G_{\mathbb Q_p}$ の $\pi_1^{(l)}$ への外作用は**不分岐**。

これは「$\mathbb Q^{(l)}(\infty)/\mathbb Q(\mu_{l^\infty})$ が $l$ の外不分岐」と同じ主張であり、$l=2$ を除外しない。**格: SGA1 水準の標準論法だが本工房の正典外・Sol 未監査**。ICM §5.2 の引用を主経路とし、これは**独立の健全性チェック**として記録するにとどめる。

---

## 7. 適用範囲と、残るギャップ

### 7.1 定理 U2-BR がカバーする窓 / しない窓

- **カバーする**: $K_{\rm ord}$ と $F_2/K_{F_2}$ がともに $2$-primary な窓。dihedral 族では **$n=2^\alpha$ のみ**。
- **カバーしない**: **奇数 $n_0$ の窓**。$K_{\rm ord}=\mathrm{lcm}(n_0,2)=2n_0$ は $2$ 冪でなく、$\lvert G_{n_0}\rvert=4n_0^3$ は $2$-群でない。**⟹ 一般の素数 $\ell$ 版(下記)を作っても奇側には効かない。**
- **一般化(自明な拡張)**: 素数 $\ell$ について $K_{\rm ord}$ が $\ell$ 冪かつ $F_2/K_{F_2}$ が $\ell$-群なら、同じ 5 行で $L_K/\mathbb Q$ は $\ell$ の外不分岐。**ただし dihedral 族にはそういう奇窓が存在しない**($4\mid\lvert G_n\rvert$ が常に成り立つ)。これは偶然ではなく、$D_n$ が常に位数 2 の元を持つことの反映である。

### 7.2 名指しの残ギャップ

- **【GAP-U2-a】** 前件 U2-A(自由 pro-$2$ 群の中心化群 = procyclic)は**外部の古典定理**であり、工房の正典にも Mathlib にもない。framework-assumptions 方針(2026-07-28 裁可)に従い**自前再導出せず Mathlib 待ち**とするか、Ribes–Zalesskii の該当定理番号を scout に確認させるかは司令塔判断。**この 1 本が本稿の唯一の外部数学依存である。**
- **【GAP-U2-b】** U2-D(Galois 作用の公式 $\sigma(y)=f_\sigma^{-1}y^{\chi}f_\sigma$)の**向きの規約**。ICM (2.3.2) は $f_\sigma=p^{-1}\sigma(p)$、基点 $\overrightarrow{01}$。ICM 脚注 1(p.114)は [Ih₂]/[A-I₂] では基点が $\overrightarrow{\infty1}$ で生成元も違うと警告している。**本稿の証明は向きに頑健**である(補題 INN の 4 段はどちらの向きでも $\bar g\in\mathbb Z_2\bar x$、$\bar h\in\mathbb Z_2\bar y$ を与える)が、$\chi$ の付き方だけは確認しておきたい。**Sol 監査点 B。**
- **【GAP-U2-c】** $\mathrm{Ih}_K$ の $f$ 成分が「$f_\sigma$ の $K_{F_2}$ 剰余」であることは正典の定義と整合しているが、**$\widehat F_2$ から $F_2/K_{F_2}$ への還元が閉包の意味で正しいか**(profinite vs discrete)。$K_{F_2}$ は有限指数なので閉包は自動だが、明示しておく。
- **無限素点**は射程外(§4 の注)。

---

## 8. Sol への申し送り(監査点)

- **監査点 A(最優先)**: **補題 INN の段 4**。$\bar f=0$(U2-B)を使って $\bar g\in\mathbb Z_2\bar x$ と $\bar h\in\mathbb Z_2\bar y$ を突き合わせる 1 行が本稿の全体を支えている。ここが崩れると (U2) は candidate に戻る。とくに **$f_\sigma\in[\widehat F_2,\widehat F_2]$ が pro-$2$ 商でも可換子部分群に入る**(準同型は可換子を可換子へ送る)という自明な段を含め、疑ってほしい。
- **監査点 B**: 【GAP-U2-b】の向きの規約(ICM 脚注 1)。
- **監査点 C**: **系 U2 の合成体論法**($p\ne2$ が二段とも不分岐 ⟹ 合成で不分岐 ⟹ 部分体で不分岐)。初等だが、$\mathbb Q^{(2)}(\infty)$ が**無限次**であることに注意した上で確認してほしい(不分岐性は有限部分体ごとに読む)。
- **監査点 D**: 定理 U2-BR の (H2) の使い方 —「有限 $2$-群への準同型は最大 pro-$2$ 商を経由する」。
- **★ 特筆**: 本稿は **Question 6.5.2(最大性)を使っていない**(禁止条項の遵守)。使ったのは「塔の中は不分岐」という許された向きのみ。**また AI1988 本体を必要としない**ので、**ILL 取得の要否判定は「不要」**である(覚書 §3-2 への回答)。

---

## 9. 格付け表

| 主張 | 格 |
|---|---|
| 補題 INN | **定理**(5 行)。外部依存 = U2-A のみ |
| **定理 U2-BR**($\ker\varphi^{(2)}\subseteq\ker\mathrm{Ih}_K$) | **定理**(正典 + U2-A) |
| 系 U2(不分岐性) | **定理**(+ 前件 U2-F = ICM §5.2・配達済・頁画像照合済) |
| **系 U2-DIH = (U2)** | **定理**(+ 正典 Thm 5.3 と位数式) |
| **系 MIX-ALL**(混合側 ⟸ 奇側) | **定理**(MIX の枠組前件 D-1〜D-8 を継承) |
| §6 の第二系統(Grothendieck 特殊化) | **未監査・傍証のみ** |
| 一般の $\ell$ 版 | **定理**(ただし dihedral 奇窓には適用不能・§7.1) |
| 無限素点での分岐 | **UNKNOWN**(射程外) |
| 【GAP-U2-a】U2-A の出典確定 | **要 scout**(定理番号の確認だけ) |
| 覚書の「定義体塔」経路 | **不採用**(§2・理由 3 点明記) |

---

## 10. 一行の申し送り(司令塔へ)

**この配達は当たりだった。** ただし当たったのは覚書が指した (U2-bridge) の形ではなく、**ICM §5.2 の 1 文(塔の定義と不分岐性)だけ**である。AI1988 も Coleman も Vogel も使っていない。**文献ゲートの費用対効果としては、頁画像照合つきの 1 文で【n12-GAP-1】が閉じ、dihedral 予想の未決部分が「奇数窓」だけに縮んだ** — 地図の delta としては本日最大級である(ただし Sol 監査前)。
