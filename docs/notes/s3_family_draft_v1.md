# (S3) 族版の起草 — 矢印 (d) 前半「$\mathrm{ord}(a_n)=n\Rightarrow\mathrm{Ih}_{K^{(n)}}$ 全射」

**状態札: `candidate(単系統・Sol 未監査)/ 主定理は既存補題の族適用であり新結果ではない(§3.4 で申告)/ Lean 検証ではない / SURJ は結論しない`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-04・**新設 v1**
- 委嘱: 司令塔「距離図の矢印 (d) 前半 =(S3) 族版を candidate として起草。正典 Thm 4.3 を式番号つきで使い、位数比較案と生成元実現案を比較して主線を選ぶ。補題 LIFT の使用箇所を明示し、閉じない残余を札化。距離規律を維持」
- **依拠(正典 + repo 内のみ・外部文献ゼロ)**
  - 正典 arXiv **2405.11725**: **Thm 4.3 (4.12)**(GT$(K^{(n)})$ の明示式・isolated)/ **Thm 4.6**(群構造と位数)/ **Thm 5.3 (5.4)**(GT$_{\rm arith}$ の下界)/ **(1.5)**($\mathrm{Ih}(g)=(\frac{\chi(g)-1}2,f_g)$)/ **Remark 1.4**(準同型性)。抽出正本 = `docs/week1-定義ノート.md` §2–§3・`docs/notes/2405.11725-抽出ノート_v1.md`・`docs/notes/抽出_Kn定義_D1.md`
  - `docs/notes/surj_d4_t1_v1.md` §2.1 **補題 SURJ-Split**(**窓非依存**・Sol **F86-4.1.1 PASS**(射程修正つき)・裁定 **227**)
  - `docs/notes/w2fam_v1.md` **命題 (W2)-fam**(裁定 **120**)/ `docs/notes/w2arith_v1.md` **命題 W2A / W2B″**(裁定 **122**)
  - `docs/week4-K3飽和_opus_v3.md` §5.2.1–§5.2.2 **定理 $R^{\rm cyc}_{\rm formal}$**(台帳 W3-13・裁定 **24**)
  - `docs/notes/q7_lower_bound_v1.md` §2.2 **命題 LB-gen** + `..._addendum_f91.md` §1(**定理/適用 gate の分離**・Sol **F91-5.1/5.3**・裁定 **266**)
  - `docs/notes/E1_gt_odd_dih_canonical_v1.md` §5(標準機械 (S1)–(S4)・**【E1-GAP-5】【E1-GAP-6】**)・§4(**定理 E1-3**・裁定 111 / **E1-4(a) $\Phi$ 単射**・裁定 130/138)
  - `docs/notes/oddH_full_proof_v1.md`(命題 **ODD-H** (1.3)・補題 C・**命題 ODD-P**)/ `docs/notes/fam_u_assembly_v1.md`(**補題 LIFT** §2.3・距離図 §V.5・**追記 B** = domain 復帰)

> ## 遵守申告
> - **距離規律**: 本稿は矢印 (d) の**前半だけ**を扱う。矢印 (a)(b)(c) の内容(FAM-U の $\mathrm{ord}([u_n]_{2n})=n$、torsor 解釈、B-LIMIT)を**前件として一切使わない**。§1.3 に禁止事項を明文化した。
> - **domain**: 奇数 $n\ge3$(**$n=5$ を含む**)。有効な domain 宣言は裁定 **396/398** の復帰版(effective source = `docs/notes/fam_u_v1_addendum_domain_restore.md`)。委嘱文の「$n\ne5$」は旧宣言の写しであり、司令塔が**新指示ではない**と否認した(2026-08-04)。⚠ **本稿は $K^{(5)}$ の値・窓データ・機械測定値に一切触れていない**($n=5$ は $\varphi$・$\gcd$ の整数計算にのみ現れる)。
> - **機械値の手写し禁止**: §9 の値はすべて `scratchpad/s3fam_check.py` の出力(パス・SHA-256 併記)。

---

## 0. 判定(先に 7 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | 矢印 (d) 前半は本当に未証明か | ★★ **否**。**像形で読むかぎり、既存の補題 SURJ-Split (e)(窓非依存・Sol PASS)を $N=K^{(n)}$ に代入するだけで全奇数 $n$ で従う**(§3.2)。**枠組み層(TB/BFC)は現れない** |
| **②** | では距離図 §V.5.1 の「(d) ★ 未証明((S3) 族版)」は何だったのか | ★★ **ラベルの誤配置**。**(S3) 族版は矢印ではなく矢印 (d) の始点ノード**(「全奇 $n$ で $\mathrm{ord}(a_n)=n$」= **【E1-GAP-5/6】**)である。矢印そのものは閉じている(§3.5・FINDING S3F-1) |
| **③** | 骨組みは位数比較か生成元実現か | ★ **位数比較(案 A)を主線**に採る。**正典の 2 冪証明(Thm 5.3)自体が位数比較型**であり、案 B は前件として案 A の結論を含む(§2.3) |
| **④** | 正典はどこまで来ているか | ★ **Thm 5.3 (5.4) の $\alpha=0$ 分岐 $\lvert\mathrm{GT}_{\rm arith}\rvert\ge2\varphi(n)=\varphi(4n)$**。目標 $\lvert\mathrm{GT}(K^{(n)})\rvert=2n\varphi(n)$ との比は**ちょうど $n=\lvert\mathfrak F_0\rvert$**。**(S3) が供給するのはこの因子 $n$ ただ一つ**(§3.3・検算 100 値 FAILS 0) |
| **⑤** | 補題 LIFT はどこで効くか | ★ **主定理では効かない**(像形は模型・持上げ・一様化元に言及しない)。**効くのは Kummer 形の系のただ 1 箇所** — 右辺 $\mathrm{ord}([u_n]_{2n})=n$ を**窓の述語として well-posed にする**段(§4) |
| **⑥** | LIFT で閉じない残余は | ★ **$[\alpha]\in(\mathbf Z/n)^\times/\{\pm1\}$ の類**。ただし**十分方向では弱化できる** — 新札 **【S3F-A2 = C1′-any】**(どの単元窓かの同定は不要・**ある**単元窓であれば足る)+ 新札 **【S3F-A3 = BRIDGE-one】**((5′)(6′) が**少なくとも一つの**単元窓で成立)。GAP 検査案つき(§4.3) |
| **⑦** | q=7 前件(C1′(7)+C5)は要るか | ★ **主定理には不要**(数学的前件に窓 $H$ が一度も現れない)。**Kummer 形の系の「適用 gate」でのみ要る** — これは Sol **F91-5.3** が $n=7$ で既に確立した定理/gate 分離の族版である(§6) |

---

## 1. 対象の固定と距離規律

### 1.1 記号(既存のものだけを使う・再定義しない)

$n\ge3$ を奇数とし、正典 §3 の記号で

$$K^{(n)}=\ker\psi_n,\qquad G_n=PB_3/K^{(n)},\qquad \nu:=K^{(n)}_{\rm ord}=\operatorname{lcm}(n,2)=2n,\qquad F_n:=\mathbf Q(\zeta_{2\nu})=\mathbf Q(\zeta_{4n}).$$

$$T:=\mathrm{GT}(K^{(n)}),\qquad \widetilde\chi:=\widetilde\chi_{2\nu}:T\to(\mathbf Z/4n)^\times,\ [m,f]\mapsto2m+1,\qquad \mathfrak F_0:=\ker\widetilde\chi,\qquad A:=\mathrm{Ih}_{K^{(n)}}(G_{\mathbf Q}).$$

$M:=\mathrm{ord}(X)=2n$、$e:=\lvert\mathfrak F_0\rvert$、$u_n\in F_n^\times$ は BFC 補題 B-5 (ii) の cusp 主係数、$a_n:=[u_n^{-1}]_M\in F_n^\times/F_n^{\times M}$。

**正典 Thm 4.3 の明示式**(定義ノート §3・画像照合済)は、$n$ 奇($4\nmid n$ ゆえ追加条件は発火しない)のとき

$$\mathrm{GT}(K^{(n)})=\bigl\{(m,\ (r^{2k},r^{-2k},r^{\varkappa(m)}))\ \big|\ m\in\mathcal X_n,\ k\in\mathbf Z\bigr\},\qquad \mathcal X_n=\{m\in[0,\nu):\gcd(2m+1,\nu)=1\},\tag{4.12}$$

$\varkappa(m)=m+1$($m$ 奇)/ $-m$($m$ 偶)、かつ **$K^{(n)}$ は isolated**(⟹ $T$ は (3.53) を積とする有限群、$\mathrm{Ih}_{K^{(n)}}$ は準同型 — 正典 Remark 1.4・補題 E1-3a)。**Thm 4.6**($\alpha=0$ 分岐)より

$$\lvert T\rvert=2n\varphi(n)=n\cdot\varphi(4n).\tag{4.6-odd}$$

### 1.2 出発点 —(H-ord) の**二つの形**と、矢印 (d) がどちらを取るか

距離図 §V.5.1 で矢印 (c) の**終点**に置かれている命題「$\mathrm{ord}(a_n)=n$」は、文脈上**二通りに読める**。両者を分離することが本稿の第一歩である。

| 形 | 言明 | どの側の量か |
|---|---|---|
| **(H-img)$_n$** | $\boxed{\ \mathrm{Ih}_{K^{(n)}}(G_{F_n})=\mathfrak F_0\ }$(同値: $\lvert\mathrm{Ih}_{K^{(n)}}(G_{F_n})\rvert=n$) | ★ **Galois 像側**。模型・cusp・一様化元に言及しない |
| **(H-kum)$_n$** | $\mathrm{ord}(a_n)=n$、$a_n=[u_n^{-1}]_{2n}\in F_n^\times/F_n^{\times2n}$ | **Kummer 類側**。窓・模型・一様化元に相対的 |

- **(H-img) は E1 §5.1 の (S3) の逐語形そのもの**($\mathrm{Ih}_{K^{(n)}}(G_K)=\mathfrak F_0$、$K=\mathbf Q(\zeta_{4n})=F_n$)。
- **両者を結ぶのは橋** — 定理 $R^{\rm cyc}_{\rm formal}$ の (5′)(6′)(= 【GAP-Rcyc】$B_{\rm FC}$)、あるいは B-LIMIT-1(FAITH 条件付き)。**この橋は矢印 (b)(c) の内容であって (d) ではない。**

> ### ★ 本稿の採択(委嘱 §3 の距離規律に従う)
> 委嘱は「出発点は **Galois 像側**の言明」と明示した。したがって
> $$\textbf{矢印 (d) 前半の前件}\ =\ \textbf{(H-img)}_n\qquad(\textbf{(H-kum) ではない})$$
> と読む。**この選択は結論を弱めない**(§5 で (H-kum) 形の系を橋つきで別に立てる)が、**枠組み依存の所在を正確にする**:(H-img) を取ると矢印 (d) には **TB1–TB4・BFC・B-5 が一度も現れない**。

### 1.3 禁止事項(矢印跨ぎ・§V.5.2 の履行)

1. **FAM-U の $\mathrm{ord}([u_n]_{2n})=n$ を (H-img) の根拠として使わない。** 両者は矢印 (b)(c) で隔てられている。本稿は (H-img) を**仮定**としてのみ扱い、その真偽には一切触れない。
2. **本稿は $\mathrm{Ih}_{K^{(n)}}$ の全射性を主張しない。** 主張するのは「(H-img) が成り立てば全射」という**含意**だけである。
3. **odd Conjecture 5.1 を主張しない。** E1-3 の適用には**全**奇 $n$ での (H-img) が要る(§7.2)。
4. **$[u_n]_{2n}$ の値・符号・平方類に触れない**(§5 の系は $u_n$ を**未知量のまま**扱う)。

---

## 2. 骨組みの二案と選定(委嘱 §1)

### 2.1 案 A — 位数比較(**$\lvert T\rvert$ と像の部分群の位数を突き合わせる**)

$$\lvert A\rvert=\lvert A\cap\mathfrak F_0\rvert\cdot\lvert\widetilde\chi(A)\rvert\ \overset{?}{=}\ n\cdot\varphi(4n)=\lvert T\rvert\ \Longrightarrow\ A=T.$$

必要な入力は 3 つ:(i) 完全列(核が**ちょうど** $\mathfrak F_0$)、(ii) $\widetilde\chi(A)$ が全体、(iii) $\lvert T\rvert$ の値。(iii) は正典 Thm 4.6 が与える。

### 2.2 案 B — 生成元ごとの実現(**族**)

Thm 4.6 の座標 $T\cong\mathrm{Aff}(\mathbf Z/n)\times\mathcal Z_2$ の生成元 3 本 — 並進 $(k=1)$・単位元方向(原始根 $2m+1$)・chirality $\mathcal Z_2$ — の各々に $\sigma\in G_{\mathbf Q}$ を割り当て、$\mathrm{Ih}(\sigma)$ が (4.12) のどの $(m,k)$ かを同定する。

> ### ⚠ 案 B が原理的に詰まる点(**本稿の判定**)
> 円分指標の全射性が与えるのは $\chi_{4n}(\sigma)=2m+1$ という**第一成分だけ**である。(4.12) の元は $(m,k)$ の**対**で決まるので、$\sigma$ を指定しても $\mathrm{Ih}(\sigma)$ は **$\mathfrak F_0$ を法としてしか決まらない**。
> - 既知の算術元でも同じ: **複素共役 $c$** は $\chi_{4n}(c)=-1$ ゆえ $m=2n-1$ を与えるが(FINDING $\Phi1$)、$f_c$ すなわち $k$ は**工房のどの文書にも無い**。
> - ⟹ **案 B は「$\mathfrak F_0$ 方向をどう埋めるか」を先に要求する。それはまさに前件 (H-img) である。** 案 B は案 A の代替経路ではなく、**案 A の前件を含んだ上でさらに $f_\sigma$ の計算を要求する**。

### 2.3 比較表と選定

| 観点 | **案 A(位数比較)** | 案 B(生成元実現) |
|---|---|---|
| 必要な正典入力 | Thm 4.3(isolated)+ Thm 4.6(位数)+ (1.5) | 同左 + (4.12) の $(m,k)$ 同定 |
| 必要な工房入力 | (W2)-fam + W2-arith(= 補題 SURJ-Split (a)–(e)) | 同左 **+ 各 $\sigma$ の $f_\sigma$** |
| $n$ 一様か | ★ **一様**(証明に $n$ の場合分けが無い) | 不明(生成元の取り方が $n$ の素因数分解に依存) |
| 前件 (H-img) の要否 | 要る(1 回) | **要る**(§2.2)— 案 A の前件を含む |
| 未供給の入力 | **なし**(前件 (H-img) を除く) | ★ **$f_\sigma$ の算術的構成**(工房にゼロ・文献にもゼロ) |
| 正典の先例 | ★★ **Thm 5.3 が位数比較型**(「$\lvert\mathrm{GT}(K^{(2^\alpha)})\rvert=2^{2\alpha-2}$ が下限 (5.4) と一致」— 抽出ノート §3) | 先例なし |

$$\boxed{\ \textbf{主線 = 案 A(位数比較)。}\ }$$

**選定理由 3 点**:(1) 案 B は案 A の前件を真に含むので、独立な第二経路にならない。(2) 正典が唯一証明した場合($2$ 冪、Thm 5.3)の論法が位数比較型であり、族へ写す先例が案 A 側にしか無い。(3) 案 A は $n$ の素因数分解を一度も使わないため、$n$ 合成数($9,15,21,\dots$)で場合分けが増えない。

> **★ 案 B の唯一の値打ち(捨てない)**: $f_c$($c$ = 複素共役)を一つでも決めれば、(H-img) を**部分的に**埋める入力になる。**これは E1-GAP-6(下界層)への未探索の攻め口である**(§11【S3F-GAP-3】)。

---

## 3. 主定理(案 A)

### 3.1 前件表(**窓 $H$ は一度も現れない**)

| # | 前件 | 内容 | 格 | pin |
|---|---|---|---|---|
| **A1** | **isolated / typing** | $K^{(n)}$ は isolated ⟹ $T$ は有限群、$\mathrm{Ih}_{K^{(n)}}:G_{\mathbf Q}\to T$ は準同型 | ★ **正典の定理** | Thm 4.3・Remark 1.4;E1-1 / 補題 E1-3a(裁定 111) |
| **A2** | **(W2)-fam** | $1\to\mathfrak F_0\to T\xrightarrow{\widetilde\chi}(\mathbf Z/4n)^\times\to1$ 完全、$\mathfrak F_0=\ker\widetilde\chi\cong C_n$、$e=n$ | **candidate**(紙 + $n\le27$ 機械) | `w2fam_v1.md`・裁定 **120** |
| **A3** | **W2-arith(Route A)** | $\widetilde\chi\circ\mathrm{Ih}_{K^{(n)}}=\chi_{4n}$ | **paper-proof candidate**。**Route A は正典 (1.5) の引用のみ ⟹ 枠組み非依存**(Route B は (CAL)+(TB4$^{\rm u}$) 相対の第二経路) | `w2arith_v1.md` 命題 W2A・裁定 **122**;補題 SURJ-Split (b) |
| **A4** | **円分の全射性** | $\chi_{4n}:G_{\mathbf Q}\twoheadrightarrow(\mathbf Z/4n)^\times$ | **古典**($\Phi_{4n}$ の $\mathbf Q$ 上既約性) | 補題 SURJ-Split (c) |
| **A5** | **$\lvert T\rvert$** | $\lvert T\rvert=2n\varphi(n)=n\varphi(4n)$ | ★ **正典の定理** | Thm 4.6($\alpha=0$);(4.12) の繊維勘定と一致(`w2fam_v1.md` §3.3 系) |
| **H** | **(H-img)$_n$** | $\mathrm{Ih}_{K^{(n)}}(G_{F_n})=\mathfrak F_0$ | ★ **前件(本稿は真偽を問わない)** | E1 §5.1 の (S3) |

> **⚠ A2 と A5 の重複について**: 実は **A5 は主線に不要である**(§3.2 注)。表に残すのは、位数比較という骨組みを字義どおり実行する形を示すためと、正典との突合(§3.3)のためである。

### 3.2 定理 SURJ-fam

> ### 定理 SURJ-fam【candidate】
> **$n\ge3$ を奇数**とする。前件 **A1–A5** の下で
> $$\boxed{\ \textbf{(H-img)}_n:\ \mathrm{Ih}_{K^{(n)}}(G_{F_n})=\mathfrak F_0\qquad\Longrightarrow\qquad \mathrm{Ih}_{K^{(n)}}:G_{\mathbf Q}\longrightarrow\mathrm{GT}(K^{(n)})\ \text{は全射}\ }$$
> であり、逆も成り立つ(すなわち **$\iff$**)。

**証明**(位数比較の形で書く)。$A=\mathrm{Ih}_{K^{(n)}}(G_{\mathbf Q})\le T$ と置く(A1 より $A$ は部分群)。

**(i) $A\cap\mathfrak F_0=\mathrm{Ih}(G_{F_n})$.** A3 より、$\gamma\in G_{\mathbf Q}$ について
$$\mathrm{Ih}(\gamma)\in\mathfrak F_0=\ker\widetilde\chi\iff\widetilde\chi(\mathrm{Ih}(\gamma))=1\iff\chi_{4n}(\gamma)=1\iff\gamma\in G_{F_n}$$
($F_n=\mathbf Q(\zeta_{4n})$ は $\chi_{4n}$ の固定体)。ゆえに $A\cap\mathfrak F_0=\mathrm{Ih}(G_{F_n})$。

**(ii) $\widetilde\chi(A)=(\mathbf Z/4n)^\times$.** A3 と A4 より $\widetilde\chi(A)=\widetilde\chi(\mathrm{Ih}(G_{\mathbf Q}))=\chi_{4n}(G_{\mathbf Q})=(\mathbf Z/4n)^\times$。

**(iii) 位数.** $\widetilde\chi|_A:A\to(\mathbf Z/4n)^\times$ は核 $A\cap\mathfrak F_0$ をもつ全射(ii)だから、第一同型定理より
$$\lvert A\rvert=\lvert A\cap\mathfrak F_0\rvert\cdot\varphi(4n)\ \overset{\text{(i),(H-img)}}{=}\ \lvert\mathfrak F_0\rvert\cdot\varphi(4n)\ \overset{\text{A2}}{=}\ n\,\varphi(4n)\ \overset{\text{A5}}{=}\ \lvert T\rvert .$$
$T$ は有限(A1)ゆえ $A=T$。

**(iv) 逆.** $A=T$ なら (i) より $\mathrm{Ih}(G_{F_n})=A\cap\mathfrak F_0=T\cap\mathfrak F_0=\mathfrak F_0$。$\blacksquare$

> ### 注(**A5 を落とした節約形** — 位数を一度も使わない)
> (i)(ii) と (H-img) から $\mathfrak F_0=A\cap\mathfrak F_0\subseteq A$。任意の $g\in T$ に対し (ii) より $\widetilde\chi(a)=\widetilde\chi(g)$ なる $a\in A$ が取れ、$ga^{-1}\in\ker\widetilde\chi=\mathfrak F_0\subseteq A$、よって $g\in A$。∎
> ⟹ **正典 Thm 4.6 の位数式は主線に不要**である。位数比較の形は「何と何を突き合わせているか」を可視化する記述上の利点のためだけに残す。**この節約は案 A の頑健性であって、案 B には対応物が無い。**

### 3.3 ★ 系 IDX — 正典 (5.4) の $\alpha=0$ 分岐を**等式へ精密化**する

**(H-img) を仮定しない**段として、(i)(ii)(iii) の途中式だけを取り出す:

> ### 系 IDX【candidate】
> 前件 A1–A5 の下で、全奇数 $n\ge3$ について
> $$\boxed{\ \lvert\mathrm{GT}_{\rm arith}(K^{(n)})\rvert\ =\ \varphi(4n)\cdot\lvert\mathrm{Ih}_{K^{(n)}}(G_{F_n})\rvert\ =\ 2\varphi(n)\cdot\lvert\mathrm{Ih}_{K^{(n)}}(G_{F_n})\rvert\ }$$
> $$\bigl[\mathrm{GT}(K^{(n)}):\mathrm{GT}_{\rm arith}(K^{(n)})\bigr]=\frac{n}{\lvert\mathrm{Ih}_{K^{(n)}}(G_{F_n})\rvert}\ \Big|\ n\qquad(\textbf{とくに指数は }n\textbf{ の約数で奇数}).$$

**帰結の読み方(★ 本稿で最も有用な会計)**:

| 量 | 値 | 出所 |
|---|---|---|
| 正典が既に持っている下界 | $\lvert\mathrm{GT}_{\rm arith}(K^{(n)})\rvert\ge2\varphi(n)$ | **Thm 5.3 (5.4)**($\alpha=0$ 分岐) |
| 目標 | $\lvert\mathrm{GT}(K^{(n)})\rvert=2n\varphi(n)$ | Thm 4.6 |
| **比(=欠けている因子)** | ★ $\boxed{n=\lvert\mathfrak F_0\rvert}$ | 機械検算 100 値・FAILS 0(§9) |

$$\Longrightarrow\quad\boxed{\ \textbf{(S3) が供給するのは、この 1 個の整数因子 }n\ \textbf{だけである。}\ }$$

さらに **系 IDX は正典 (5.4) の $\alpha=0$ 分岐を系として含む**($\lvert\mathrm{GT}_{\rm arith}\rvert\ge\varphi(4n)=2\varphi(n)$)。

> ### ⚠ 同じ数だが同じ主張ではない(★教材)
> 正典 (5.4) は $\lvert A\rvert\ge2\varphi(n)$ という**位数の下界**、A3+A4 は $\widetilde\chi(A)=(\mathbf Z/4n)^\times$ という**商方向の全射性**である。**後者は前者を含意するが逆は言えない** — 下界だけからは「単位元方向が全部埋まっている」は出ない。⟹ **正典 (5.4) を主線の入力に使ってはならない**(本稿は使っていない;§9 の突合にのみ用いる)。この区別は `q7_lower_bound_v1.md` §4 の「二つの『1 ビット』は別のビット」と同型の罠である。

### 3.4 ★ 新規性の申告(**主定理は新結果ではない** — grep 済)

**grep 語**: `SURJ-Split`・`SURJ-fam`・`SURJ-K7`・`GT_arith`・`ord(a_n)`・`(S3) 族版`・`E1-GAP-5`。

- **定理 SURJ-fam の内容は既出である。** `docs/notes/surj_d4_t1_v1.md` §2.1 **補題 SURJ-Split (e)** が
  $$\mathrm{Ih}_N\ \text{全射}\iff\mathrm{Ih}_N(G_{K_0})=\ker\widetilde\chi\qquad(K_0=\mathbf Q(\zeta_{2\nu}))$$
  を**任意の isolated 窓 $N$** について、**窓データを一切使わずに**証明している(Sol **F86-4.1.1 PASS**・裁定 **227**;「無条件」の射程は「isolated と $\mathrm{Ih}_N$ の typing が供給された後」に限る、という Sol の修正つき)。$N=K^{(n)}$、$\nu=2n$ を代入し、$\ker\widetilde\chi=\mathfrak F_0\cong C_n$(A2)を入れれば定理 SURJ-fam になる。
- **本稿が足したのは 4 点だけである**:(a) $K^{(n)}$ 族への代入と、そこで $\ker\widetilde\chi=\mathfrak F_0$ が (W2)-fam で**全奇数一様に**同定済であることの明示(§3.1 A2);(b) **系 IDX** と正典 (5.4) との突合(§3.3);(c) **案 A/案 B の比較と選定**(§2);(d) **ラベル誤配置の診断**(§3.5)と**残余の札化**(§4.3)。
- **「初」という語は使わない。** 工房外の文献での既知性は未調査。

### 3.5 ★★ 診断 — 距離図 §V.5.1 のラベルは誤配置である

距離図 §V.5.1 の矢印 (d) は

> $\mathrm{ord}(a_n)=n\ \xrightarrow[\text{未証明}]{\textbf{(d)}}\ \mathrm{Ih}_{K^{(n)}}$ 全射 ……「★ **未証明**((S3) 族版)」

と記されている。しかし E1 §8 の定義では

> **【E1-GAP-5】(S3) の族版が無い**。……「全奇 $n$ で $\mathrm{ord}(a_n)=n$」……**これを族として証明する道具は無い**

であり、**(S3) 族版とは「$\mathrm{ord}(a_n)=n$ を全奇 $n$ で証明すること」**、すなわち矢印 (d) の**始点ノードを全 $n$ で満たすこと**である。⟹

$$\boxed{\ \textbf{矢印 (d) の前半は閉じている(§3.2)。開いているのはその}\textbf{始点ノード}\textbf{である。}\ }$$

**この誤配置が実害をもたらす形**: 「矢印 (d) を証明する」という課題設定は、**下界層(【E1-GAP-6】)へ資源を向けない**。`q7_lower_bound_v1.md` の診断(「装置が無いのではなく入力が無い」)と合わせると、**残っている仕事は測定 M2 型の入力供給であって、含意の証明ではない**。⟹ §12 監査点 1 と §11【S3F-GAP-1】。

---

## 4. 補題 LIFT の使用箇所(委嘱 §2)

### 4.1 主定理では使わない — その理由

**補題 LIFT**(`fam_u_assembly_v1.md` §2.3・F95-1.7 / F96-1.4 **PASS**・裁定 344/353)は

$$\widetilde\alpha\mapsto\widetilde\alpha+n\ \text{は}\ y\mapsto g(k)y\ (\rho=g(i)=-i)\ \text{と同一の操作},\qquad u\mapsto u\cdot(-i)^{-2n}=-u$$

という**模型側**の言明である。定理 SURJ-fam の言明にも証明にも、**模型・cusp・持上げ $\widetilde\alpha$・一様化元・$u$ が一度も現れない**(§3.1 の前件表を見よ:窓 $H$ の文字が無い)。したがって

$$\boxed{\ \textbf{補題 LIFT は定理 SURJ-fam の前件ではない。}\ }$$

これは記帳上重要である —「LIFT ⟹ (S3) 持上げ変更の型が閉じる」(§V.2.1 の行)の **(S3) は最短鎖の第 3 段**(FAM-U 側)であって、**E1 の (S3)(= 窓ごとの本体)ではない**。**同名異物**であり、混同すると「LIFT が矢印 (d) の前件だ」という誤読が生じる(★教材・§12 監査点 2)。

### 4.2 効くのは Kummer 形の系のただ 1 箇所

§5 の系 SURJ-fam-K は右辺に $\mathrm{ord}([u_n]_{2n})=n$ を置く。この右辺が**窓の述語**として意味をもつためには、$u_n$ の

1. **整数持上げ $\widetilde\alpha$ の取り替え**($\widetilde\alpha\mapsto\widetilde\alpha+n$)
2. **局所一様化元の取り替え**($\tau\mapsto\rho\tau$)

に対する不変性が要る。**1 は補題 LIFT が、2 は前件 C5 の取り替え則 $u\mapsto u\rho^{-2n}$ が与え**、いずれも $[\,\cdot\,]_{2n}$ で消える(**INV**: $-1=\zeta_{4n}^{2n}\in F_n^{\times2n}$ ゆえ $[4]_{2n}=[-4]_{2n}$;$\rho^{-2n}\in F_n^{\times2n}$)。

$$\boxed{\ \textbf{LIFT の使用箇所} = \textbf{系の右辺を well-posed にする段(ただ 1 箇所)。定理本体には入らない。}\ }$$

**LIFT が果たす第二の役割**: 許容持上げの族 $\{\widetilde\alpha\in\mathbf Z:\gcd(\widetilde\alpha,n)=1\}$ を **$\widetilde\alpha\bmod n$** へ潰す。すなわち残るのは**類** $\alpha\in(\mathbf Z/n)^\times$ のみ。

### 4.3 ★ LIFT が閉じない残余 → 新札 2 枚

$$\text{残余}\ =\ [\alpha]\in(\mathbf Z/n)^\times/\{\pm1\}\quad(\varphi(n)/2\ \text{個の窓類})$$

(GT 作用が $[\alpha]$ を $\pm1$ 倍しか動かさないこと = ODD-H §11.2;$j$ 方向は定理 W-REL / J-BLIND で閉鎖済 = 裁定 173;$\beta=0$ は C1 の規約)。既存札は **C1′**(「測定される $u$ が $H^{\rm fun}_n=H_{2,1,0}$ 窓の値であること」・**開**)。本稿はこれを**十分方向に限って弱められる**ことを見出したので、新しい札を 2 枚立てる。

> ### 【S3F-A2 = C1′-any】(**弱化・candidate**)
> **系 SURJ-fam-K の十分方向($\Leftarrow$)には、$u$ が**どの**単元窓 $H_{2,\alpha,0}$($\alpha\in(\mathbf Z/n)^\times$)のものかを同定する必要はない。ある**一つの**単元窓のものであれば足りる。**
> **理由**: 定理 SURJ-fam の結論「$\mathrm{Ih}_{K^{(n)}}$ 全射」は**窓 $H$ に言及しない**。$R^{\rm cyc}_{\rm formal}$ を窓 $(K^{(n)},H_{2,\alpha,0})$ に適用して得られる同値は、$\alpha$ ごとに**左辺が同じ**である。ゆえに一つの $\alpha$ で右辺が成立すれば結論が出る。
> **要る方向**: 逆($\Rightarrow$)、すなわち**非全射を測定値から結論する**場合、および (5′)(6′) が特定の $\alpha$ でしか確認されていない場合には、従来どおり C1′ が要る。
> **GAP 検査案(機械確認可)**: 奇数 $n\in\{3,7,9,11,13,15,21\}$ について、$\alpha\in(\mathbf Z/n)^\times$ の全窓 $H_{2,\alpha,0}$ が (P1)(P2)(P3)(= ODD-H (1.3)+補題 C(2))を満たし、$\lvert\Lambda_\alpha\rvert=2n$ かつ $\langle X\rangle$ が単純推移であり、ordered passport が $((2n),2^{n-1}1^2,(2n))$($=$ ODD-P の $d=\gcd(\alpha,n)=1$ 分岐)であることを悉皆確認する。**1 つでも落ちればその $n$ で C1′-any は偽**。

> ### 【S3F-A3 = BRIDGE-one】(**新前件・UNKNOWN**)
> **各奇数 $n\ge3$ について、$R^{\rm cyc}_{\rm formal}$ の (5′)(= $B_{\rm FC}$)と (6′) が、**少なくとも一つの**単元窓 $H_{2,\alpha,0}$($\alpha\in(\mathbf Z/n)^\times$)で成立すること。**
> - これは「工房標準窓 $H_{2,1,0}$ で成立すること」より**真に弱い**前件であり、系 SURJ-fam-K が実際に要する最小形である。
> - **状態**: (6′) は**有限計算で決着する**(§5.2.3 の補題 R′ により「$\rho_0$ が忠実」の 1 ビットへ縮約 — 縮約は前件 (3) の regular 性を使い、ODD-H (1.3) が $\alpha\ne0$ で (3) を与える)。**(5′) は UNKNOWN**(【GAP-Rcyc】$B_{\rm FC}$・橋 B-1)。
> - **GAP 検査案**: 各 $(n,\alpha)$ で $\Lambda_\alpha=H_{2,\alpha,0}^{G_n}$($\lvert\Lambda_\alpha\rvert=2n$)を作り、$\rho_0=\Phi|_{\mathfrak F_0}$ の $\Lambda_\alpha$ 上への制限が忠実か、$\rho_0(\mathfrak F_0)=\tau(\mu_{2n}[n])$ かを直接検査する。**(6′) 側だけなら機械で閉じる。**

> ### 【S3F-A1】(**依存の明示・candidate**)
> **$\mathfrak F_0$ の二つの定義の一致に $\Phi_n$ の単射性が load-bearing である。**
> `w2fam_v1.md` §3.5 が示すのは $\ker\widetilde\chi\xrightarrow{\sim}\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X^2\rangle)$ という**$\Phi$ の像レベルの一致**である。BFC 側の $\mathfrak F_0$($\Lambda$ 上の作用で定義される部分群)と $\ker\widetilde\chi$ を **$T$ の部分群として**同一視するには **$\Phi_n$ 単射(E1-4(a)・裁定 130/138・紙上相互監査 PASS)**が要る。
> - **本稿の主定理はこの札に依存しない**($\mathfrak F_0:=\ker\widetilde\chi$ と**定義**して通る)。
> - **依存するのは §5 の系**((H-kum) 側の $\mathfrak F_0$ は BFC 側の定義で入ってくるため)。
> - ⟹ 記帳上は「主定理は $\Phi$ 単射に非依存・系は依存」と分けるべきである(§12 監査点 3)。

---

## 5. 系(Kummer 形)と適用 gate — F91-5.3 の族版

Sol は $n=7$ で**数学定理と適用 gate を分離**することを要求し(F91-5.3・裁定 266)、それが `q7_lower_bound_v1_addendum_f91.md` §1.1/§1.2 の形で確立した。**本稿はその族版を同じ二段で書く。**

### 5.1 系 SURJ-fam-K(**数学定理**)

> ### 系 SURJ-fam-K【candidate / framework-conditional】
> **前件(数学のみ)**
> 1. **A1–A5**(§3.1)
> 2. **【S3F-A3 = BRIDGE-one】**@$n$ — ある単元窓 $\alpha$ で (5′)(6′)
> 3. **A7-fam**@$n$(裁定 214)— $[u_n]_{2n}$ が uniformizer/モデル非依存の**窓不変量**であること(**値ではない**)+ **補題 LIFT**(§4.2)
> 4. **【S3F-A1】** — $\mathfrak F_0$ の二定義の一致($\Phi_n$ 単射)
>
> **主張**($u_n\in F_n^\times$ は当該単元窓の cusp $P_0$ における intrinsic な主係数、$F_n=\mathbf Q(\zeta_{4n})$)
> $$\boxed{\ \mathrm{Ih}_{K^{(n)}}\ \text{全射}\iff\mathrm{ord}\bigl([u_n]_{2n}\bigr)=n\iff\underbrace{[u_n]_2=1}_{\textbf{上界層}}\ \wedge\ \underbrace{\forall p\mid n\ \text{素数}:\ u_n\notin F_n^{\times p}}_{\textbf{下界層}\ (\omega(n)\ \text{本})}\ }$$
> **証明.** 第 1 の同値は定理 $R^{\rm cyc}_{\rm formal}$(前件 (0)(1)(2)(3)(5′)(6′);(0)=A1、(1)=A2+A3、(2)=A2($e=n\mid2n$)、(3)= ODD-H (1.3)+補題 C(2)、(5′)(6′)= 前件 2)。$\mathrm{ord}(a_n)=\mathrm{ord}([u_n^{-1}]_{2n})=\mathrm{ord}([u_n]_{2n})$($\ell$ 冪所属は $v\mapsto v^{-1}$ で不変)。第 2 の同値は**命題 LB-gen**(`q7_lower_bound_v1.md` §2.2・補題 ORD・Sol **F91-5.1 PASS**)を $M=2n$、$\mu_{2n}\subset F_n$ で適用。$\blacksquare$
>
> **★ この系は全射性を主張しない。** 右辺の真偽は射程外である。**下界層は現在どの $n\ge5$ でも未供給**(【E1-GAP-6】)。

### 5.2 SURJ-fam-APPLY(**適用 gate**・数学ではなく手続き)

> ### SURJ-fam-APPLY【gate】(F91-5.3 の gate 表の族版)
> 測定線が値 $\tilde u$(または類)を出したとき、それを系 SURJ-fam-K の $u_n$ に代入してよいのは次を**すべて**満たすときに限る。
>
> | # | gate 項目 | 族版での内容 | 現状 |
> |---|---|---|---|
> | **G-1** | **C1′($n$)** | ★ **十分方向では【S3F-A2 = C1′-any】へ弱化**(「**ある**単元窓の値であること」)。逆方向・非全射結論では従来の C1′ | **開**(弱化形は未監査) |
> | **G-2** | **C5** | 宇宙の事前登録(測る量を後から足さない) | **手続き・司令塔** |
> | **G-3** | **モデル束縛** | 整モデル・cusp section・局所 parameter・正規化が 定理 B-4 / B-5(ii-loc)の規約と一致 | **開** |
> | **G-4** | **provenance** | cert・入力ハッシュ・独立再計算(値は機械生成のみ) | 手続き |
>
> **系 SURJ-fam-K の真偽は gate に依存しない。** gate が支配するのは「代入してよいか」だけである。

---

## 6. q=7 前件(C1′(7)+C5)は (S3) 族版のどこで要るか(委嘱 §4)

$$\boxed{\ \textbf{定理 SURJ-fam(矢印 (d) 前半・本体)には }\textbf{要らない}\textbf{。系 SURJ-fam-K の }\textbf{適用 gate}\textbf{ でのみ要る。}\ }$$

**要らないことの理由(3 点・いずれも検証可能)**

1. **前件表に窓が現れない**: A1(isolated)・A2((W2)-fam)・A3(W2-arith)・A4(円分)・A5(Thm 4.6)はすべて **$K^{(n)}$ のみの関数**である。$H_{2,\alpha,\beta}$ の文字が一度も出ない。補題 SURJ-Split が「**窓データを一切使わない**」(裁定 227)と明記しているのと同じ理由である。
2. **前件 (H-img) が窓に言及しない**: $\mathrm{Ih}_{K^{(n)}}(G_{F_n})=\mathfrak F_0$ は $T$ の部分群の等式であり、窓 $H$ を含まない。
3. **C5 は測定手続きである**: 矢印 (d) は測定を一つも行わない。Sol **F85-1.2**(「C5 の survey は較正であって前件ではない」)とも整合する。

**要る箇所(正確に)**

| 局面 | C1′($n$) | C5 |
|---|---|---|
| 定理 SURJ-fam(§3.2) | ✗ 不要 | ✗ 不要 |
| 系 SURJ-fam-K の**言明**(§5.1) | ✗ 不要(intrinsic な $u_n$ を使う) | ✗ 不要 |
| 系の**適用**(測定値の代入・§5.2) | ★ **要る**(G-1)。ただし**十分方向では C1′-any へ弱化** | ★ **要る**(G-2) |
| **非全射**を測定値から結論する場合 | ★ **要る(弱化不可)** | 要る |

**⟹ $q=7$ 前線との関係**: $q=7$ の残前件 C1′(7)+C5(裁定 214)は、**本稿の矢印 (d) には一切効かない**。それらは矢印 (b)(c) の下流、すなわち「測った値を系の $u_7$ と呼んでよいか」を支配する。**第二の下界歯(C5・CASC の $d=7$)についても同じ** — CASC が運ぶのは上界層($\ell=2$)であり(命題 G7-NOGO′・射程限定版)、矢印 (d) の前件 (H-img) には触れない。

---

## 7. 射程と会計

### 7.1 $K^{(n)}=K^{(2n)}$ による自動的な拡張($\alpha\le1$)

$n$ 奇のとき $K^{(n)}=K^{(2n)}$(定義ノート §3 の数値事実)なので、定理 SURJ-fam は **$\alpha\le1$ の全対象**($n$ 奇、または $n\equiv2\bmod4$)を同時に覆う。正典 Thm 5.3 (5.4) の $\alpha\in\{0,1\}$ 分岐が同じ下界 $2\varphi(n_0)$ を与えることと整合する。

### 7.2 ★ E1-3 への接続と **$n=5$ の会計**

**定理 E1-3**(裁定 111・紙上相互監査 PASS)は「odd Conj 5.1 $\iff$ $\mathrm{Ih}^{\rm odd}$ 全射」であり、**系 E1-3e** が「有限個の窓をいくら獲っても極限には到達しない」と述べる。したがって

$$\text{odd Conj 5.1}\ \Longleftarrow\ \Bigl[\ \textbf{(H-img)}_n\ \text{が}\ \boldsymbol{\text{全}}\ \text{奇数}\ n\ge3\ \text{で成立}\ \Bigr]\ +\ \text{定理 SURJ-fam}\ +\ \text{E1-3}.$$

- ★ **「全」は文字どおり全奇数である。$n=5$ を除いた集合では E1-3 は適用できない。** 現行の有効 domain 宣言は裁定 396/398 により **奇数 $n\ge3$(除外なし)**なので、この点で障害は無い。ただし **$K^{(5)}$ blind campaign の運用**が $n=5$ の値に触れることを制限している場合、**(H-img)$_5$ の供給だけが別扱いになる**可能性がある — これは数学ではなく運用の問題であり、司令塔裁定事項として上申する(§12)。
- 続いて **U2-BR**(裁定 319)が「混合側 Conj 5.1 ⟸ 奇側」を与える。⟹ 鎖の外枠は閉じている。**開いているのは (H-img)$_n$ の供給ただ一つ**である。

### 7.3 $\alpha=2$ 層への波及(**主張しない・射程注記のみ**)

`docs/notes/n12_goursat_v1.md` の **定理 MIX-4**(candidate / framework-conditional / **Sol 未監査**)は「$n_0>1$ 奇、$\mathrm{Ih}_{K^{(n_0)}}$ 全射 ⟹ $\mathrm{Ih}_{K^{(4n_0)}}$ 全射」である。格が candidate である以上、本稿は $\alpha=2$ への波及を**主張しない**(注記のみ)。$\alpha\ge3$ は【n12-GAP-1】として未閉鎖。

---

## 8. 予言(**事前登録** — 値を書く前に述語を固定する)

> **凍結の型**: 以下 4 本は、いずれも**測定・機械実行の前**に述語を確定したものである。IF-FIRST 規律に従い、値は書かない。

| # | 予言(述語) | 根拠 | ★ 反証条件(対称形) |
|---|---|---|---|
| **P-S3F-1** ★★ | **同一の奇数 $n$ について、【S3F-A3】が成立する 2 つの単元窓 $\alpha,\alpha'\in(\mathbf Z/n)^\times$ があれば $\mathrm{ord}([u_{n,\alpha}]_{2n})=\mathrm{ord}([u_{n,\alpha'}]_{2n})$**(値でなく**位数**が一致する) | 系 SURJ-fam-K を両窓に適用すると**左辺が同一**(窓非依存) | ★ 位数が食い違えば、**(5′) か (6′) がどちらかの窓で偽**、または $R^{\rm cyc}_{\rm formal}$ の前件確認札が誤り |
| **P-S3F-2** ★ | **任意の奇数 $n\ge3$ で $\bigl[\mathrm{GT}(K^{(n)}):\mathrm{GT}_{\rm arith}(K^{(n)})\bigr]$ は $n$ の約数(とくに奇数)** | 系 IDX(§3.3) | ★ 偶数の指数、または $n$ を割らない指数が測定されれば **A2 か A3 が偽** |
| **P-S3F-3** | **【S3F-A2 = C1′-any】の GAP 検査(§4.3)が $n\in\{3,7,9,11,13,15,21\}$ で全 PASS** | ODD-H (1.3)+補題 C(2)+ODD-P($d=1$ 分岐) | ★ 落ちる $(n,\alpha)$ があれば C1′-any はその $n$ で偽 ⟹ G-1 の弱化は撤回 |
| **P-S3F-4** | **【S3F-A3】の (6′) 側(「$\rho_0$ が忠実」)は $n\in\{3,7,9\}$ の全単元窓で成立** | 補題 R′ の縮約 + ODD-H (1.3) が (3) を供給 | ★ 忠実でない単元窓があれば、補題 R′ の縮約が当該窓で使えず、(6′) の直接確認へ切替 |

⚠ **P-S3F-1 と矢印 (a) の値との関係(整合性の観察であって含意ではない)**: FAM-U 側(矢印 (a))が扱う模型量は $\widetilde\alpha$ に依存しない形をとると記録されている(補題 LIFT + INV)。これは P-S3F-1 と**矛盾しない**が、**(a) から (d) への含意ではない** — (a) の量と系 SURJ-fam-K の $u_n$ を同一視するには橋(B-1)が要る。本稿はその同一視を行わない。

---

## 9. 検算(本稿で走らせたもの)

- **script**: `scratchpad/s3fam_check.py`(SHA-256 `99d8824dd2e7ec616fa80e5c74456106e3e490ccfa55bec39acd3396bb962ea7`)
- **格**: ★ **python 単系統**(cross-checked ではない)。**紙の証明の予言の spot-check** であり、証明の根拠ではない。**Lean 検証ではない**。
- **宇宙(事前登録)**: 奇数 $n\in[3,201]$、$\lvert$宇宙$\rvert=100$(**除外なし** — 裁定 396/398 の domain 復帰に従う)

| # | 検査 | 内容 | 結果 |
|---|---|---|---|
| **A1** | 水準 | $\varphi(4n)=2\varphi(n)$ | PASS |
| **A2** | 位数 | $\lvert T\rvert=2n\varphi(n)=n\cdot\varphi(4n)$(Thm 4.6 $\alpha=0$) | PASS |
| **A3** | 正典下界 | Thm 5.3 (5.4) $\alpha=0$ 分岐 $2\varphi(n)=\varphi(4n)$ | PASS |
| **A4** | ★ **欠けている因子** | $\lvert T\rvert\ /\ (\text{正典下界})=n$(整除つき) | PASS |
| **A5/A6** | (4.12) の座標 | $\lvert\mathcal X_n\rvert=\varphi(4n)$、かつ $m\mapsto2m+1$ が $\mathcal X_n\to(\mathbf Z/4n)^\times$ の**全単射**(補題 L) | PASS |

**出力**: `FAILS = 0`(`RESULT: ALL PASS`)。標本行(機械出力): $(n,\lvert T\rvert,\varphi(4n),\text{下界},\text{比})=(3,12,4,4,3),(7,84,12,12,7),(9,108,12,12,9),(11,220,20,20,11),(13,312,24,24,13)$。

同じ script の **Part B / Part C** は本稿とは無関係な別委嘱(`docs/notes/k5_w6_construction_v1_addendum_b_k20paper.md` の $\mathbf F_2$ 線型代数)の検算であり、**本稿の主張には一切使っていない**(同一ファイルに同居しているのは実行の便宜)。

⚠ **A5/A6 は補題 L(`w2arith_v1.md` §1)の再検算**であり、独立の証明ではない。**$n=5$ 行は $\varphi$・$\gcd$ の整数計算のみ**で、$K^{(5)}$ の窓データ・shadow・測定値には一切触れていない。

---

## 10. FINDING

| # | 格 | 内容 |
|---|---|---|
| **S3F-1** | ★★ **診断(本稿の主成果)** | **距離図 §V.5.1 の矢印 (d) 前半は閉じている。** 像形 (H-img) を出発点に取れば、**補題 SURJ-Split (e)(窓非依存・Sol PASS・裁定 227)+ (W2)-fam + W2-arith** で全奇数 $n$ 一様に従い、**枠組み層(TB1–TB4・BFC)は一度も現れない**。「★ 未証明((S3) 族版)」というラベルは**矢印ではなく始点ノード**(= 【E1-GAP-5/6】)に付くべきものである |
| **S3F-2** | ★★ **会計** | **系 IDX**: $\lvert\mathrm{GT}_{\rm arith}(K^{(n)})\rvert=2\varphi(n)\cdot\lvert\mathrm{Ih}(G_{F_n})\rvert$。正典 Thm 5.3 (5.4) の $\alpha=0$ 分岐($\ge2\varphi(n)$)を**等式へ精密化**し、**目標との比がちょうど $n=\lvert\mathfrak F_0\rvert$** であることを確定した(100 値 FAILS 0)。**⟹ (S3) が供給するのは 1 個の整数因子だけ** |
| **S3F-3** | ★ **骨組みの選定** | **案 A(位数比較)を主線**。案 B(生成元実現)は $\mathrm{Ih}(\sigma)$ が $\mathfrak F_0$ を法としてしか決まらないため**案 A の前件を含む**(複素共役ですら $f_c$ が未知)。正典 Thm 5.3 も位数比較型。さらに案 A は **Thm 4.6 の位数式さえ落とせる節約形**をもつ(§3.2 注) |
| **S3F-4** | ★ **LIFT の位置** | 補題 LIFT は**定理 SURJ-fam の前件ではない**。効くのは**系の右辺を well-posed にする 1 箇所**のみ。⚠ **§V.2.1 の「LIFT ⟹ (S3)」の (S3)(最短鎖第 3 段)と E1 の (S3)(窓ごとの本体)は同名異物** |
| **S3F-5** | ★ **残余の札化** | LIFT が閉じない残余 $=[\alpha]$ 類。**【S3F-A2 = C1′-any】**(十分方向では窓ラベル同定不要 — **C1′ の弱化**)・**【S3F-A3 = BRIDGE-one】**((5′)(6′) は**ある一つの**単元窓で足りる;**(6′) 側は有限計算で決着**)・**【S3F-A1】**($\mathfrak F_0$ の二定義の一致に $\Phi$ 単射が load-bearing;**主定理は非依存・系は依存**) |
| **S3F-6** | ★ **q=7 前件の位置** | **C1′(7)・C5 は矢印 (d) の数学的前件ではない**。Sol **F91-5.3** が $n=7$ で確立した「定理 / 適用 gate」分離の**族版**として §5.1/§5.2 に固定した |
| **S3F-7** | ⚠ **語の区別(★教材)** | 正典 (5.4) の「$\lvert A\rvert\ge2\varphi(n)$」と工房 A3+A4 の「$\widetilde\chi(A)=(\mathbf Z/4n)^\times$」は**同じ数だが同じ主張ではない**(後者 ⟹ 前者・逆は不成立)。⟹ **(5.4) を主線の入力にしてはならない** |

---

## 11. 【GAP】(隠さず明示・埋めていない)

| 札 | 内容 | 重み |
|---|---|---|
| **【S3F-GAP-1】** | ★★ **(H-img)$_n$ の供給が全奇 $n$ で無い。** これが本当の未閉鎖である(= 【E1-GAP-5】)。下界層は【E1-GAP-6】(下界が出ているのは $n=3$・$n=9$ の 2 例のみ) | **重**(中間峰の本丸) |
| **【S3F-GAP-2】** | **【S3F-A3 = BRIDGE-one】の (5′) は UNKNOWN**(= 【GAP-Rcyc】$B_{\rm FC}$ / 橋 B-1・機械化不能)。⟹ **系 SURJ-fam-K は framework-conditional のまま**。**定理 SURJ-fam(本体)はこれに依存しない** | 中 |
| **【S3F-GAP-3】** | ★ **案 B の残骸 = $f_c$(複素共役の $f$ 成分)が未知。** これを一つ決めれば (H-img) の一部が埋まる可能性があるが、工房にも(調査した限りの)正典にも記述が無い。**未探索の攻め口**として登録 | 中(**新規の攻め口**) |
| **【S3F-GAP-4】** | **A2((W2)-fam)は `candidate`**(裁定 120)。主定理はこれに全面依存する。$\ker\widetilde\chi$ が**ちょうど** $C_n$ であること(より大きくないこと)が破れれば §3.2 (iii) の位数勘定が崩れる | 中 |
| **【S3F-GAP-5】** | 本稿は**単系統・Sol 未監査**。系 IDX・案 A/B 比較・S3F-A1/A2/A3・診断 S3F-1 はいずれも本稿が初出(工房内では) | — |

**「verified」は本稿で一度も使っていない**(Lean 未接続)。「紙上相互監査 PASS」と書いたのは**引用元**の格であって、本稿の新規命題の格ではない。

---

## 12. Sol への申し送り(監査点 5・優先順)

1. ★★ **診断 S3F-1 の可否(最重要)**: 「矢印 (d) 前半は、出発点を**像形** (H-img) に取れば補題 SURJ-Split (e) の族適用で閉じており、未証明なのは矢印ではなく**始点ノード**である」— この読みは正しいか。特に、**距離図 §V.5.1 の矢印 (d) の始点「$\mathrm{ord}(a_n)=n$」を像形で読む**ことが、あなたが (c-n)/B-LIMIT-1 を設計したときの意図と一致するか。**もし始点が Kummer 形でしか読めないなら、橋が矢印 (d) の内部に入り、「(d) は枠組み非依存」という本稿の主張は撤回すべきである。**
2. ★ **同名異物 2 件の確認**:(i) `fam_u_assembly` §V.2.1 の「LIFT ⟹ **(S3)**(持上げ変更の型)」と E1 §5.1 の **(S3)**(窓ごとの本体 $\mathrm{Ih}(G_K)=\mathfrak F_0$)は別物、(ii) 正典 (5.4) の位数下界と工房の商方向全射性は別主張 — この 2 つの分離で足りるか、他に同名衝突が残っていないか。
3. ★ **【S3F-A1】の判定**: $\mathfrak F_0$ を $\ker\widetilde\chi$ と**定義**する立場(主定理)と、BFC の $\Lambda$ 上の作用で定義する立場(系)を分け、後者の同一視に $\Phi_n$ 単射(E1-4(a))が load-bearing だとした読みは正しいか。`w2fam_v1.md` §3.5 はこの依存を明示していない。
4. ★ **【S3F-A2 = C1′-any】の弱化の可否**: 「十分方向では**どの**単元窓かの同定は不要」— 結論が窓非依存であることからこう言ってよいか。**逆方向(非全射結論)では弱化不可**という切り分けで足りるか。
5. **【S3F-A3 = BRIDGE-one】の形**: (5′)(6′) を「**ある一つの**単元窓で」と量化するのが系の要する最小形か。また補題 R′ による (6′) → 「$\rho_0$ 忠実」の縮約が、**全**単元 $\alpha$(非単元ではなく)で使えるという読み(前件 (3) を ODD-H (1.3) が $\alpha\ne0$ で供給)に異論はないか。

---

## 13. 出所・文献要請・司令塔への上申

### 13.1 各節の出所

| 節 | 主たる出所 |
|---|---|
| §1 | 定義ノート §2–§3(Thm 4.3 (4.12)・Thm 4.6・$K_{\rm ord}$)/ E1 §5.1((S3) の逐語形)/ `fam_u_assembly_v1.md` §V.5 |
| §2 | 正典 Thm 4.6・Thm 5.3(抽出ノート §3)/ FINDING $\Phi1$(`phifam_v1.md`・裁定 130) |
| §3 | **補題 SURJ-Split**(`surj_d4_t1_v1.md` §2.1・裁定 227)/ (W2)-fam(裁定 120)/ W2-arith(裁定 122)/ 正典 (1.5)・Thm 4.6・Thm 5.3 (5.4) |
| §4 | 補題 LIFT(`fam_u_assembly_v1.md` §2.3・裁定 344/353)/ ODD-H (1.3)・補題 C・ODD-P / W-REL・J-BLIND(裁定 173) |
| §5 | $R^{\rm cyc}_{\rm formal}$(W3-13・裁定 24)/ 命題 LB-gen(`q7_lower_bound_v1.md` §2.2)/ **F91-5.3 の定理/gate 分離**(裁定 266) |
| §6 | F91-5.3 gate 表 / F85-1.2(C5)/ 裁定 214(C1′(7)+C5)/ 命題 G7-NOGO′(f91 追補 §2.2) |
| §7 | E1-3(裁定 111)・系 E1-3e / U2-BR(裁定 319)/ 定理 MIX-4(`n12_goursat_v1.md`)/ 裁定 396/398(domain 復帰) |

### 13.2 【文献要請】

**本稿からの新規はゼロ。** 既出の **【文献要請 G7-2】**(「$p$-深さの下界を値を測らずに出す道具 = 副有限像の非退化定理」)が、本稿の【S3F-GAP-1】に**そのまま**対応する — 本稿はその要請の優先度が上がったことだけを報告する(新しい要請は立てない)。

### 13.3 司令塔への上申(3 点)

1. ★★ **距離図 §V.5.1 の矢印 (d) のラベル訂正**を提案する — 「未証明((S3) 族版)」は**始点ノードの札**であり、矢印そのものは §3.2 で閉じている。**地図 P1/P2 行と `fam_u_assembly` の erratum(追記 C 等)で処理されたい**(本稿は他ノートを書き換えていない)。
2. ★ **資源配分**: 本稿の会計(系 IDX)により、残る仕事は「**1 個の整数因子 $n$ を供給すること**」= 下界層の入力(測定 M2 型)に収束する。**含意の証明に資源を割く必要はない。**
3. **【S3F-GAP-3】($f_c$ = 複素共役の $f$ 成分)を新しい攻め口として起票**することを提案する。案 B は主線としては落としたが、この 1 点だけは (H-img) の**部分的供給**になりうる未探索路である。
