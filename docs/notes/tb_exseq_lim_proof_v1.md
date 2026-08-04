# 補題 EXSEQ-LIM の完全証明 — **債務 2 件は討たれたのではなく、消えた**

**状態札: `candidate(証明ノート・紙のみ / Lean 検証ではない / cross-checked でもない / 単系統 / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設 v1**
- 委嘱: 司令塔(Sol 非依存の紙仕事)「v2.1 で骨子+債務 2 件として引き受けた **補題 EXSEQ-LIM を完全証明化**せよ」
- 前提文書(**いずれも 1 バイトも改変していない**): `docs/notes/tb_citation_bundle_v1.md` / `v2.md` / `v2_1.md`(とくに v2.1 §4.3 が本ノートの対象)
- **原典**: `papers/sga1-grothendieck-raynaud-arxiv0206203.pdf`(**頁対応: 新頁 = PDF − 16**)

---

## 0. 判定(先に 3 行)

| # | 結論 |
|---|---|
| **1** | ★★ **v2.1 §4.3 の証明経路を差し替えた。** 新経路は **正規化(normalization)も非エタール軌跡も一度も使わない** ⟹ 引き受けた債務 2 件(**正規化の底変換可換性**・**非エタール軌跡の閉性**)は**討ち取られたのではなく、証明から消滅した**。 |
| **2** | ★ **EXSEQ-LIM は完全に証明された**(§3–§7)。使う外部入力は **SGA 1 Exp. I の 3 項目(Prop. 3.1・Déf. 4.1・Déf. 4.9)= すべて `present`/定義**のみ。他はすべて初等代数(PID 上の有限自由性・多項式恒等式の降下・$\Omega$ の底変換)で、**本ノートが自前で証明を書いた**。 |
| **3** | ⚠ **これで `canonical-source-relative` に到達したとは主張しない。** 到達したのは「**工房債務 L-1〜L-7 の全 7 本が証明本文つきになった**」までである(§9)。**relative への残存障害は Ihara ③-1($\pi_1^{\rm geom}\cong\hat F_2$ の `omitted`)ただ 1 点に絞られた**(§10)— **これが「道が開く」の中身であり、道が通ったという主張ではない。** |

> ### ★ 鍵となった観察(一行)
> $$\boxed{\ U=\mathbf P^1-\{0,1,\infty\}\ \textbf{は\textbf{アフィン}であり、}\ \mathcal O(U_L)=L[\beta,\beta^{-1},(\beta-1)^{-1}]\ \textbf{は PID である。}\ }$$
> ⟹ 有限エタール被覆は**有限自由代数**として書け、降下は**構造定数と多項式恒等式の話**に落ちる。v2.1 §4.3 が関数体と正規化を経由したのは**遠回りだった**(自認)。

---

## 1. 何が変わったか — 旧経路 / 新経路

| | **旧経路(v2.1 §4.3・骨子)** | ★ **新経路(本ノート・完全証明)** |
|---|---|---|
| 対象の記述 | 連結被覆 ↔ 関数体 $M/\bar{\mathbf Q}(\beta)$ の有限次分離拡大 | **有限自由 $A_{\bar{\mathbf Q}}$-代数 $B$**(基底 + 構造定数) |
| 降下の仕掛け | $M$ の定義多項式の係数が有限個 ⟹ ある $K_i$ に入る | 構造定数・単位元座標が有限個 ⟹ ある $K_i$ に入る(**同じ着想**) |
| 被覆の再構成 | **$U_{K_i}$ の $M_i$ における正規化** | **不要**(自由加群に構造定数を載せるだけ) |
| エタール性の確認 | **非エタール軌跡が閉**であることを使い、$\bar{\mathbf Q}$ 上で空 ⟹ $K_i$ 上で空 | **$\Omega^1$ の底変換 + 忠実平坦**($\Omega_{B_i/A_{K_i}}\otimes A_{\bar{\mathbf Q}}=\Omega_{B/A_{\bar{\mathbf Q}}}=0$ ⟹ $\Omega_{B_i/A_{K_i}}=0$) |
| 平坦性の確認 | 正規化の有限平坦性 | **構成が自由加群**(自動) |
| **債務** | ★ **2 件**(正規化の底変換可換性・非エタール軌跡の閉性) | ★ **0 件** |
| $i$ の取り直し | 存在段と一意性段で 2 回 | **エタール性では取り直し不要**(§5 の ★) |

> ★ **自認**: v2.1 §4.3 の骨子は、$U$ がアフィンかつ $\mathcal O(U)$ が PID であることを使わず、曲線の関数体論へ迂回した。**数学的に誤りではないが、不要な標準事実 2 件を背負い込んだ**。本ノートはその 2 件を**証明の外へ出す**。

---

## 2. 設定・記法・使う基本事実

### 2.1 設定

- $K\subseteq\bar{\mathbf Q}$ を有限次体、$\{K_i\}_{i\in I}$ を $\bar{\mathbf Q}/K$ の有限ガロア部分拡大の全体(包含で有向・$\bar{\mathbf Q}=\bigcup_iK_i$)。
- $L$ を $K\subseteq L\subseteq\bar{\mathbf Q}$ の体とし
  $$A_L:=L[\beta,\beta^{-1},(\beta-1)^{-1}],\qquad U_L:=\mathrm{Spec}\,A_L=\mathbf P^1_L-\{0,1,\infty\}.$$
- $\mathcal C_L:=$($U_L$ 上の有限エタール被覆の圏)。$\rho_{ij}:\mathcal C_{K_i}\to\mathcal C_{K_j}$($j\ge i$)、$\rho_i:\mathcal C_{K_i}\to\mathcal C_{\bar{\mathbf Q}}$ を底変換関手とする。
- $\Omega=\bar{\mathbf Q}\{\{\beta\}\}$、$F_L:=\mathrm{Fib}^{(L)}_{\vec{01}}(W)=\mathrm{Hom}_{L((\beta))\text{-alg}}\bigl(\mathcal O(W\times_{U_L}\mathrm{Spec}\,L((\beta))),\Omega\bigr)$。
  > ⚠ **射程の注記**: BFC v2 §2 の (TB1) は $k\subseteq\bar{\mathbf Q}$ **有限次**で書かれているが、(TB3) は $\pi_1(U_{\bar{\mathbf Q}},\vec{01})$ を使う。$\mathrm{Fib}$ の定義式は $L=\bar{\mathbf Q}$ でも**逐語のまま意味をもつ**(有限エタール $W\to U_{\bar{\mathbf Q}}$・$\bar{\mathbf Q}((\beta))$-代数準同型)。本ノートはこの延長を採る。**BFC 本文は改変しない。**

### 2.2 使う外部入力(**SGA 1 のみ・3 項目**)

| # | 内容 | pin | 照合 | `proof_body_status` |
|---|---|---|---|---|
| **BF-1** | **net(非分岐)$\iff\Omega^1_{X/Y}$ が $x$ で零** | **SGA 1 Exp. I, Prop. 3.1 (ii)**(**PDF 18 / 新頁 2**)逐語: 「Conditions équivalentes: (i) $\mathcal O_x/\mathfrak m_y\mathcal O_x$ est une extension finie séparable de $k(y)$. **(ii) $\Omega^1_{X/Y}$ est nul en $x$.** (iii) …」 | ★ **150 dpi 画像✓** | **present**(証明が本文) |
| **BF-2** | **étale = plat + net** | **SGA 1 Exp. I, Déf. 4.1 a)**(**PDF 20 / 新頁 4**)逐語: 「On dit que $f$ est *étale* en $x$ si $f$ est **plat** en $x$ et **net** en $x$.」 | ★ **150 dpi 画像✓** | **定義** |
| **BF-3** | **revêtement étale = fini + étale** | **SGA 1 Exp. I, Déf. 4.9**(**PDF 21 / 新頁 5**)逐語: 「On appelle revêtement étale (resp. net) de $Y$ un $Y$-schéma $X$ qui est **fini** sur $Y$ et **étale** (resp. net) sur $Y$.」 | テキスト(pdftotext) | **定義** |

> ★ **BF-1/BF-2/BF-3 はいずれも `present` または定義であり、`reader_exercise` も `external_reference` も含まない。** これが v2.1 §4.3 との最大の差である。

### 2.3 本ノートが**自分で証明する**初等事実

| # | 内容 | §  |
|---|---|---|
| **EL-1** | $A_L$ は PID / $A_{K_i}\to A_{K_j}\to A_{\bar{\mathbf Q}}$ は単射かつ**自由**(ゆえに忠実平坦) | §2.4 |
| **EL-2** | $\Omega^1$ の底変換 $\Omega_{B/A}\otimes_BB'\cong\Omega_{B'/A'}$($B'=B\otimes_AA'$) | §2.5 |
| **EL-3** | 有限自由代数のデータ = 構造定数 + 単位元座標、代数の公理 = 多項式恒等式 | §4 |

> ⚠ **1 つだけ標準事実を使う(申告)**: SGA 1 Exp. I §1 が対角イデアルで定義する $\Omega^1_{X/Y}=\mathcal I/\mathcal I^2$ を、アフィンの場合の **Kähler 微分加群 $\Omega_{B/A}$** と同一視する(普遍導分 $b\mapsto\overline{b\otimes1-1\otimes b}$)。これは**標準的な同一視であり本ノートは証明を書かない**。
> ★ **裏づけ(参考 pin)**: SGA 1 Exp. I §1(**PDF 17 / 新頁 1**)逐語「$\Omega^1_{X/Y}$ … **Il est de type fini si $X\to Y$ est de type fini. Il se comporte bien par rapport à extension de la base $Y'\to Y$.**」— **SGA 1 側は証明を書かず脚注で EGA IV 16.3 へ委ねる**(`omitted`)。⟹ **本ノートは SGA 1 の宣言に依存せず、EL-2 を自前で証明する**(§2.5)。SGA 1 の一文は**傍証としてのみ**引く。

### 2.4 補題 **EL-1**

> **補題 EL-1.** (a) $A_L$ は PID。(b) $L\subseteq L'$ に対し $A_L\to A_{L'}$ は単射で、$A_{L'}$ は $A_L$-加群として**自由**(階数 $=\dim_LL'$)。とくに忠実平坦。
> **証明.** (a) $A_L=S^{-1}L[\beta]$($S$ は $\beta$ と $\beta-1$ が生成する乗法系)。$L[\beta]$ は PID で、PID の局所化は PID。
> (b) $L'$ の $L$-基底 $(\lambda_s)_{s\in S}$ を取ると $A_{L'}=A_L\otimes_LL'=\bigoplus_s A_L\lambda_s$。自由かつ非零ゆえ忠実平坦、とくに単射。∎

### 2.5 補題 **EL-2**($\Omega$ の底変換・**自前証明**)

> **補題 EL-2.** $A\to B$ 環準同型、$A\to A'$ 環準同型、$B':=B\otimes_AA'$ とすると、自然な $B'$-加群同型
> $$\Omega_{B/A}\otimes_BB'\ \xrightarrow{\ \sim\ }\ \Omega_{B'/A'}$$
> がある。
> **証明.** 任意の $B'$-加群 $M'$ について、制限写像
> $$\mathrm{Der}_{A'}(B',M')\longrightarrow\mathrm{Der}_A(B,M'),\qquad D\mapsto D|_B$$
> が全単射であることを示せばよい。
> **単射**: $A'$-導分 $D$ は $D(1\otimes a')=0$ と Leibniz から $D(b\otimes a')=a'\,D(b\otimes1)$ を満たすので、$B$ 上の値で決まる。
> **全射**: $d\in\mathrm{Der}_A(B,M')$ に対し $D(b\otimes a'):=a'\,d(b)$ と置く。$(b,a')\mapsto a'd(b)$ は $A$-双線型($D(ba\otimes a')=a'd(ba)=a'a\,d(b)=D(b\otimes aa')$)なので $B\otimes_AA'$ 上 well-defined。加法性は明らか。Leibniz は
> $$D\bigl((b\otimes a')(c\otimes c')\bigr)=a'c'\,d(bc)=a'c'\bigl(b\,d(c)+c\,d(b)\bigr)=(b\otimes a')D(c\otimes c')+(c\otimes c')D(b\otimes a').$$
> $A'$-線型性は定義から。$D|_B=d$。
> 以上より $\mathrm{Hom}_{B'}(\Omega_{B/A}\otimes_BB',M')=\mathrm{Hom}_B(\Omega_{B/A},M')=\mathrm{Der}_A(B,M')=\mathrm{Der}_{A'}(B',M')=\mathrm{Hom}_{B'}(\Omega_{B'/A'},M')$ が $M'$ について自然に成り立つ。Yoneda により主張を得る。∎

---

## 3. 補題 **LIM-A**(有限エタール代数は有限自由)

> **補題 LIM-A.** $L$ を $K\subseteq L\subseteq\bar{\mathbf Q}$ の体、$W\to U_L$ を有限エタール被覆とし $B:=\mathcal O(W)$ と置く。このとき $B$ は $A_L$-加群として**有限階数の自由加群**である。
> **証明.** BF-3 より $W\to U_L$ は有限、ゆえに $B$ は有限生成 $A_L$-加群。BF-2 より平坦。$A_L$ は整域(EL-1)なので平坦加群は捩れなし($a\ne0$ に対し $A_L\xrightarrow{a}A_L$ が単射ゆえ $B\xrightarrow{a}B$ も単射)。有限生成捩れなし加群は PID 上自由(EL-1 (a) + 構造定理)。∎

> ★ **この一段が新経路の心臓である。** 「有限エタール被覆」という幾何的対象が、**基底と構造定数という有限個のデータ**に還元される。

---

## 4. 補題 **LIM-B**(代数構造の降下)

> **補題 LIM-B.** $B$ を有限エタール $A_{\bar{\mathbf Q}}$-代数とする。**ある $i\in I$ と、$A_{K_i}$-代数 $B_i$($A_{K_i}$-加群として有限自由)が存在して** $B_i\otimes_{A_{K_i}}A_{\bar{\mathbf Q}}\cong B$($A_{\bar{\mathbf Q}}$-代数として)。
> **証明.** LIM-A より $B=\bigoplus_{l=1}^nA_{\bar{\mathbf Q}}e_l$(自由・階数 $n$)。積と単位元を
> $$e_je_k=\sum_lc^l_{jk}e_l,\qquad 1_B=\sum_lu^le_l\qquad(c^l_{jk},u^l\in A_{\bar{\mathbf Q}})$$
> と書く。これらは**有限個**($n^3+n$ 個)の $A_{\bar{\mathbf Q}}=\varinjlim_iA_{K_i}$ の元なので、ある $i$ で全て $A_{K_i}$ に属する。
> $$B_i:=\bigoplus_{l=1}^nA_{K_i}e_l,\qquad e_je_k:=\sum_lc^l_{jk}e_l,\qquad 1:=\sum_lu^le_l$$
> と定める。**可換律・結合律・単位律は、$c^l_{jk}$ と $u^l$ についての多項式恒等式**
> $$c^l_{jk}=c^l_{kj},\qquad \sum_mc^m_{jk}c^l_{mp}=\sum_mc^m_{kp}c^l_{jm},\qquad \sum_mu^mc^l_{mj}=\delta^l_j$$
> であり、$B$ が可換環であることからこれらは $A_{\bar{\mathbf Q}}$ で成立する。$A_{K_i}\hookrightarrow A_{\bar{\mathbf Q}}$ は**単射**(EL-1 (b))なので、同じ等式が $A_{K_i}$ で成立する。ゆえに $B_i$ は可換 $A_{K_i}$-代数。
> 最後に $B_i\otimes_{A_{K_i}}A_{\bar{\mathbf Q}}$ は $\bigoplus_lA_{\bar{\mathbf Q}}(e_l\otimes1)$ で、構造定数が同じだから $e_l\otimes1\mapsto e_l$ が $A_{\bar{\mathbf Q}}$-代数同型を与える。∎

---

## 5. ★ 補題 **LIM-C**(エタール性の降下 — **$i$ を取り直さずに**)

> **補題 LIM-C.** LIM-B の $B_i$ は **$A_{K_i}$ 上有限エタール**である($i$ の取り直しを要しない)。
> **証明.**
> **(有限)** $B_i$ は $A_{K_i}$-加群として階数 $n$ の自由加群、とくに有限生成。
> **(平坦)** 自由加群は平坦。
> **(net)** BF-1 により $\Omega^1_{B_i/A_{K_i}}=0$ を示せばよい。EL-2 を $A=A_{K_i}$, $A'=A_{\bar{\mathbf Q}}$, $B=B_i$ に適用すると($B'=B_i\otimes_{A_{K_i}}A_{\bar{\mathbf Q}}\cong B$ ゆえ)
> $$\Omega_{B_i/A_{K_i}}\otimes_{A_{K_i}}A_{\bar{\mathbf Q}}\ \cong\ \Omega_{B_i/A_{K_i}}\otimes_{B_i}B'\ \cong\ \Omega_{B/A_{\bar{\mathbf Q}}}.$$
> $B$ は $A_{\bar{\mathbf Q}}$ 上エタール(仮定)ゆえ BF-1/BF-2 より $\Omega_{B/A_{\bar{\mathbf Q}}}=0$。他方 EL-1 (b) より $A_{\bar{\mathbf Q}}$ は $A_{K_i}$-加群として自由・非零、すなわち $M\otimes_{A_{K_i}}A_{\bar{\mathbf Q}}\cong M^{(S)}$($S\ne\emptyset$)。ゆえに
> $$\Omega_{B_i/A_{K_i}}^{(S)}=0\ \Longrightarrow\ \Omega_{B_i/A_{K_i}}=0.$$
> BF-1 より $B_i$ は $A_{K_i}$ 上 net、BF-2 とあわせてエタール、BF-3 とあわせて有限エタール被覆。∎

> ### ★ ここが債務 2 件の消えた場所
> **旧経路**は「非エタール軌跡は閉であり、$\bar{\mathbf Q}$ 上で空だから $K_i$ 上でも空」という**位相的**議論を使い、そのために「非エタール軌跡の閉性」を背負った。
> **新経路**は $\Omega^1$ という**加群**を直接扱い、忠実平坦(実は**自由**)による零判定で済ませる。⟹ **軌跡の位相を一度も見ない。**
> 同様に、$B_i$ を**自由加群として構成した**ので平坦性が自動で、**正規化を作る必要がない** ⟹ 「正規化の底変換可換性」も現れない。

---

## 6. 補題 **LIM-D**(充満忠実性)

> **補題 LIM-D.** $i\in I$ と $V,V'\in\mathcal C_{K_i}$ に対し、自然な写像
> $$\varinjlim_{j\ge i}\ \mathrm{Hom}_{\mathcal C_{K_j}}\bigl(\rho_{ij}V,\rho_{ij}V'\bigr)\ \longrightarrow\ \mathrm{Hom}_{\mathcal C_{\bar{\mathbf Q}}}\bigl(\rho_iV,\rho_iV'\bigr)$$
> は全単射である。
> **証明.** $C:=\mathcal O(V)=\bigoplus_{l}A_{K_i}e_l$、$C':=\mathcal O(V')=\bigoplus_mA_{K_i}e'_m$(LIM-A により自由)と置く。$\mathcal C$ の射は $\mathcal O$ の $A$-代数準同型の逆向きなので、$A_{K_j}$-代数準同型 $\phi_j:C'\otimes A_{K_j}\to C\otimes A_{K_j}$ と $A_{\bar{\mathbf Q}}$-代数準同型 $\phi:C'\otimes A_{\bar{\mathbf Q}}\to C\otimes A_{\bar{\mathbf Q}}$ を比べればよい。
> **(単射)** $\phi_j$ は行列 $(a_{ml})$($\phi_j(e'_m)=\sum_la_{ml}e_l$、$a_{ml}\in A_{K_j}$)で決まる。$A_{K_j}\hookrightarrow A_{\bar{\mathbf Q}}$ は単射(EL-1 (b))ゆえ、底変換後に一致する 2 つの行列は一致する。
> **(全射)** $\phi(e'_m)=\sum_la_{ml}e_l$ の $a_{ml}\in A_{\bar{\mathbf Q}}$ は**有限個**ゆえ、ある $j\ge i$ で全て $A_{K_j}$ に属する。同じ行列で $\phi_j$ を定義する。**$A$-代数準同型であること**(加法性・単位元の保存・積の保存)は、$a_{ml}$ と両側の構造定数についての**多項式恒等式**であり、$A_{\bar{\mathbf Q}}$ で成立するから $A_{K_j}$ でも成立する(単射性)。∎

---

## 7. 定理 **EXSEQ-LIM**

### 7.1 圏同値

> **定理 EXSEQ-LIM (1).** 底変換関手たちが誘導する関手
> $$\varinjlim_{i\in I}\ \mathcal C_{K_i}\ \longrightarrow\ \mathcal C_{\bar{\mathbf Q}}$$
> は**圏同値**である。
> **証明.** 本質的全射性 = LIM-A + LIM-B + LIM-C。充満忠実性 = LIM-D。∎

### 7.2 繊維関手との両立

> **補題 EXSEQ-LIM (2).** 自然同型 $F_{\bar{\mathbf Q}}\circ\rho_i\cong F_{K_i}$ および $F_{K_j}\circ\rho_{ij}\cong F_{K_i}$ が、$I$ について両立して存在する。
> **証明.** $W\in\mathcal C_{K_i}$ とすると
> $$\rho_i(W)\times_{U_{\bar{\mathbf Q}}}\mathrm{Spec}\,\bar{\mathbf Q}((\beta))\ =\ W\times_{U_{K_i}}\mathrm{Spec}\,\bar{\mathbf Q}((\beta))\ =\ \bigl(W\times_{U_{K_i}}\mathrm{Spec}\,K_i((\beta))\bigr)\times_{\mathrm{Spec}\,K_i((\beta))}\mathrm{Spec}\,\bar{\mathbf Q}((\beta)),$$
> すなわち $\mathcal O(\rho_iW\times\cdots)=A_W\otimes_{K_i((\beta))}\bar{\mathbf Q}((\beta))$($A_W:=\mathcal O(W\times_{U_{K_i}}\mathrm{Spec}\,K_i((\beta)))$)。$\Omega$ は $\bar{\mathbf Q}((\beta))$-代数だから、テンソルの随伴により
> $$F_{\bar{\mathbf Q}}(\rho_iW)=\mathrm{Hom}_{\bar{\mathbf Q}((\beta))\text{-alg}}\bigl(A_W\otimes_{K_i((\beta))}\bar{\mathbf Q}((\beta)),\ \Omega\bigr)\ \cong\ \mathrm{Hom}_{K_i((\beta))\text{-alg}}(A_W,\Omega)=F_{K_i}(W).$$
> $W$ について自然で、$I$ について両立する。∎

### 7.3 $\pi_1$ への翻訳(**v2.1 §4.3 の主張形**)

> **定理 EXSEQ-LIM (3).** $\rho_i$ が誘導する準同型たちは同型
> $$\pi_1(U_{\bar{\mathbf Q}},\vec{01})=\mathrm{Aut}(F_{\bar{\mathbf Q}})\ \xrightarrow{\ \sim\ }\ \varprojlim_{i\in I}\mathrm{Aut}(F_{K_i})$$
> を与える。
> **証明.** EXSEQ-LIM (2) により、各 $\rho_i$ は $\sigma\mapsto(\sigma_{\rho_i(-)})$ で $\mathrm{Aut}(F_{\bar{\mathbf Q}})\to\mathrm{Aut}(F_{K_i})$ を誘導し、$j\ge i$ で両立する。
> **単射性**: $\sigma$ が全ての $i$ で $\mathrm{id}$ に写るとする。$V\in\mathcal C_{\bar{\mathbf Q}}$ を任意に取ると、EXSEQ-LIM (1) の本質的全射性より $V\cong\rho_i(V_i)$ なる $i,V_i$ がある。$\sigma$ は自然変換だからこの同型と可換で、$\sigma_{\rho_i(V_i)}=\mathrm{id}$ ゆえ $\sigma_V=\mathrm{id}$。
> **全射性**: 両立系 $(\sigma^{(i)})_i$ を取る。$V\in\mathcal C_{\bar{\mathbf Q}}$ に $V\cong\rho_i(V_i)$ を選び $\sigma_V:=$($\sigma^{(i)}_{V_i}$ をこの同型で移したもの)と定める。**well-defined**: 別の表示 $V\cong\rho_{i'}(V_{i'})$ に対し $j\ge i,i'$ を取れば LIM-D(充満忠実)により $\rho_{ij}V_i\cong\rho_{i'j}V_{i'}$ が $\mathcal C_{K_j}$ で成り立ち、$\sigma^{(j)}$ の自然性と系の両立性から両者は一致する。**自然性**: $V\to V'$ を $\mathcal C_{\bar{\mathbf Q}}$ の射とすると LIM-D の全射性により十分大きい $j$ でこの射は $\mathcal C_{K_j}$ から来るので、$\sigma^{(j)}$ の自然性が移る。∎

### 7.4 v2.1 の完全列への接続(**主張形の確認**)

v2.1 §4.2 の **EXSEQ-STAB** により、各 $i$ で $\mathcal C_K/U_{K_i}\simeq\mathcal C_{K_i}$(下記 ★)と $\mathrm{Aut}(F'_i)\cong\mathrm{Stab}_\pi(a_i)$($\pi:=\pi_1(U_K,\vec{01})$、$a_i\in F_K(U_{K_i})=\mathrm{Hom}_{K\text{-alg}}(K_i,\bar{\mathbf Q})$ は包含)。**定理 EXSEQ-LIM (3)** と合わせて
$$\pi_1(U_{\bar{\mathbf Q}},\vec{01})\ \xrightarrow{\ \sim\ }\ \varprojlim_i\mathrm{Stab}_\pi(a_i)\ =\ \bigcap_i\mathrm{Stab}_\pi(a_i)\ =\ \ker\bigl(p:\pi\to G_K\bigr),$$
すなわち **v2.1 §3.4 ②-4 が要求した「IX の証明手順の再走」の極限段が閉じる**。

> ★ **$\mathcal C_K/U_{K_i}\simeq\mathcal C_{K_i}$ の確認**(v2.1 §4.2 で暗黙にしていた一段・本ノートで明示): $K_i/K$ は有限次分離(char 0)なので $U_{K_i}\to U_K$ は有限エタール、とくに $\mathcal C_K$ の対象で、$A_{K_i}$ が整域ゆえ連結。$X\to U_K$ 有限エタールに $U_{K_i}$ 上の構造が与えられたとき、$X\to U_{K_i}$ は **SGA 1 Exp. I Cor. 4.8**(「$X'$ が $Y$ 上非分岐で $X$ が $Y$ 上エタールなら $g:X\to X'$ はエタール」・新頁 3–4)によりエタールで、$X\to U_K$ 有限・$U_{K_i}\to U_K$ 分離ゆえ有限。逆向きは合成(有限エタールの合成は有限エタール)。$F'_i$ と $F_{K_i}$ の一致は、$F_K(X')\to F_K(U_{K_i})$ の $a_i$ 上の繊維が「$K_i$ 上で包含に一致する $K((\beta))$-代数準同型」= $K_i((\beta))$-代数準同型の集合であることによる。

---

## 8. 引き受けた債務 2 件の処理

| 債務(v2.1 §4.3 末) | ★ **処理** | 補足 |
|---|---|---|
| **(a) 正規化は底体の分離拡大と可換**(char 0) | ★★ **消滅**。新経路は正規化を一度も作らない(§5 の ★) | 旧経路を採るなら pin 候補は SGA 1 Exp. I §10(revêtements étales d'un schéma normal・Cor. 10.3 / Prop. 10.4 (iii)「propriété de translation」)。**本ノートは使わないので採らない** |
| **(b) 有限平坦射の非エタール軌跡は閉** | ★★ **消滅**。新経路は軌跡の位相を見ない(§5 の ★) | ★ **在庫内に pin は実在する**: **SGA 1 Exp. I Cor. 3.3**(**PDF 18 / 新頁 2**・**画像✓**)逐語「**L'ensemble des points où $f$ est net est ouvert.**」+ 平坦軌跡の開性。⟹ **もし将来 (b) が必要になっても文献要請は不要**。本ノートでは**使わない** |

$$\boxed{\ \textbf{【文献要請】は起票しない。} \ \textbf{債務 2 件はいずれも「証明の外へ出た」ものであり、外部文献を要さない。}\ }$$

---

## 9. 工房債務 **L 系の消し込み表**

| # | 補題 | 内容 | 状態(本ノート後) | 出所 |
|---|---|---|---|---|
| **L-1** | **TB1-FF′** | $\mathrm{Fib}_{\vec{01}}$ が基本関手($j^*$ の完全性)| ✅ **証明本文あり**・単系統 | v2 §4 |
| **L-2** | **TB4-INJ** | $\iota:I_0\to\pi_1$ 単射 | ✅ **証明本文あり**・**便 102 F102-7.1 で成立確認** | v1 §4.3 |
| **L-3** | **TB4-GEN′** | $\mathrm{im}(\iota)=\overline{\langle x\rangle}$(**閉部分群としてのみ**)| ✅ **証明本文あり**・**便 102 F102-7.1 で成立確認** | v2 §5.2 |
| **L-4** | **EXSEQ (a)(b)** | $F\circ\Phi\cong F_{\bar{\mathbf Q}}$・$p:\pi\to G_K$ | ✅ **証明本文あり**(v2.1 §2.2 で付値・Hensel を削除して訂正) | v2.1 §2.2 |
| **L-5** | **SPLIT** | 接基点 splitting $s_{\vec{01}}$ | ✅ **証明本文あり**・単系統 | v2 §3.4 |
| **L-6** | **EXSEQ-STAB** | $\mathrm{Aut}(F'_i)\cong\mathrm{Stab}_\pi(a_i)$(SGA 1 V 6.13 の reader_exercise 引受)| ✅ **証明本文あり**・単系統。★ **本ノート §7.4 の ★ で $\mathcal C_K/U_{K_i}\simeq\mathcal C_{K_i}$ の一段を補完** | v2.1 §4.2 + 本ノート §7.4 |
| **L-7** | **EXSEQ-LIM** | 極限段(SGA 1 IX 6.1 の reader_exercise 引受)| ★★ **本ノートで完全証明**(債務 2 件は消滅)| **本ノート §3–§7** |

$$\boxed{\ \textbf{工房債務 L-1〜L-7 の全 7 本が「証明本文つき」になった。残るのは\textbf{全 7 本が単系統・Sol 監査未}であること。}\ }$$

---

## 10. 格への含意(**提案・主張ではない**)

### 10.1 `canonical-source-relative` の条件と現況

v1 §7.3 の定義: `canonical-source-relative` = 全 pin が `proof_body_status = present`、または `external_reference` の連鎖が `present` に着地している。

| ブロック | `present` でない pin | ★ **現況** |
|---|---|---|
| **①** | Deligne 10.16 = `external_reference`(「SGA 3 V 7」)| ★ **迂回可能**: ブロック ① は既に **SGA 1 V Th. 4.1 / §7 / Prop. 6.1(すべて `present` または定義)** に直 pin されている(v2 §2)。Deligne 10.16 は**名前 pin として外せる** |
| **②** | SGA 1 V 6.13 = `reader_exercise` / SGA 1 IX 6.1 の極限段 = `reader_exercise` | ★ **工房補題 L-6 / L-7 が `present` で代替**(本ノートで L-7 が完成) |
| **③** | ★ **Ihara ③-1**($\pi_1^{\rm geom}\cong\hat F_2$)= `omitted / silent_omission` | ★★ **未解決**。③-3($z$ の $\infty$-慣性)は (5′) 鎖で非 load-bearing なので障害にならない |
| **④** | Deligne 15.23 PREUVE の Abhyankar = `external_reference` | ⚠ **未検討**(本ノートの射程外) |

$$\boxed{\ \textbf{★ }\texttt{relative}\textbf{ への残存障害は }\mathbf{2}\textbf{ 点に絞られた: ③-1(Ihara の }\hat F_2\textbf{ 自由性)と ④ の Abhyankar。}\ }$$

### 10.2 ⚠ 本ノートが**主張しないこと**

1. 「**`canonical-source-relative` に到達した**」— ★ **主張しない**。到達したのは L-7 の完全証明までである。**現行の格 `theorem-framework-relative [TB: canonical-source-pinned/v2]`(便 103 F103-4)は動かない。**
2. 「**工房補題が文献 pin の代替になる**」— ★ **主張しない**。これは**格の体系の解釈**であり、**司令塔・Sol の裁定事項**である(§11 の監査点 P-2)。本ノートは「工房補題が `present` になった」という**事実**だけを報告する。
3. 「**SGA 1 を通読した**」— **主張しない**。本ノートで新たに開いたのは **Exp. I §1–§4(PDF 17–21)**のみ(既往は Exp. V §4–§7・Exp. IX §6)。
4. 「**EGA IV を参照した**」— ★ **していない**。**新経路は EGA IV を一度も必要としない**(v2.1 §4.3 の申告が解消)。
5. `cross-checked` / `verified` — **付さない**(機械計算ゼロ・Lean 未使用)。**novelty** — 主張しない。
6. $\varepsilon$ / exact (TB4) / $(Z_{2M}$-link$)$ / $K^{(5)}$ の値・窓データ・封印欄 — **一切触れていない**。

---

## 11. Sol への監査点(3 点)

> **P-1 ★★ LIM-C(§5)の 3 行**。「$\Omega_{B_i/A_{K_i}}\otimes_{A_{K_i}}A_{\bar{\mathbf Q}}\cong\Omega_{B/A_{\bar{\mathbf Q}}}=0$ かつ $A_{\bar{\mathbf Q}}$ が $A_{K_i}$ 上自由非零 ⟹ $\Omega_{B_i/A_{K_i}}=0$」。**ここが債務 2 件を消した箇所**であり、新経路の全重量が掛かっている。とくに **EL-2(§2.5)の自前証明**(導分の制限が全単射)に穴はないか。
>
> **P-2 ★ 格の解釈**(§10.2-2)。**工房補題(`present`・単系統・Sol 監査未)が、文献 pin の `reader_exercise` を代替して `canonical-source-relative` の条件を満たすと数えてよいか。** 私は**数えてよいとは主張しない**が、数え方の裁定が要る。数えてよいなら relative への障害は ③-1 と ④ の 2 点、数えないなら L-6/L-7 の**独立照合**(Sol 側の再走 or Lean)が追加で要る。
>
> **P-3 ★ §7.4 の ★ で補完した一段**($\mathcal C_K/U_{K_i}\simeq\mathcal C_{K_i}$)。v2.1 §4.2 の EXSEQ-STAB は $S=U_{K_i}$ を「$\mathcal C_K$ の連結対象」として使うが、**$\mathcal C_K/U_{K_i}$ と $\mathcal C_{K_i}$ の同一視**と **$F'_i\cong F_{K_i}$** を明示していなかった。本ノートで **SGA 1 Exp. I Cor. 4.8** を使って補完した。**この補完で EXSEQ-STAB は閉じるか。**

---

## 付録 A. 本ノートで新規に開いた原典頁

| pin | PDF 頁 | 新頁 | 照合 |
|---|---|---|---|
| SGA 1 Exp. I §1($\Omega^1$ の定義・底変換の宣言)| 17 | 1 | テキスト(**傍証としてのみ使用**) |
| **SGA 1 Exp. I Prop. 3.1 (ii)**(net $\iff\Omega^1=0$)| **18** | **2** | ★ **150 dpi 画像✓** |
| SGA 1 Exp. I Cor. 3.3(net 軌跡は開)| 18 | 2 | ★ **150 dpi 画像✓**(**使用しない・債務 (b) の参考 pin**) |
| SGA 1 Exp. I Cor. 4.8($X$ étale・$X'$ net ⟹ $g$ étale)| 19–20 | 3–4 | テキスト |
| **SGA 1 Exp. I Déf. 4.1**(étale = plat + net)| **20** | **4** | ★ **150 dpi 画像✓** |
| SGA 1 Exp. I Déf. 4.9(revêtement étale = fini + étale)| 21 | 5 | テキスト |
| (参考)SGA 1 Exp. I Prop. 4.10(判別式による étale 判定)| 21 | 5 | テキスト(**代替経路・使用しない**) |
