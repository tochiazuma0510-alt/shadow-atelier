# I-23 — SQ-$dq$ 一般化と巡回核カスケード定理

**状態札: candidate(裁定前・未 commit・単系統)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-29
設問: 司令塔委嘱(便 79 検分材料)/ 発案 **I-23**(`ideas/ideas_005_panorama.md` §I-23)の一般補題化
正典・依拠:
- `docs/notes/i17_check_v1.md`(命題 SQ-3q・補題 A/B/C・caveat C1/C1′/C-3q)— **本稿の特例回収先**
- `docs/notes/t63_reconnaissance_v1.md` §2((T) = (2.3)・前件 A4–A7・(6.3-cls)/(6.3-chr) の型)
- `docs/notes/hfun_functoriality_v1.md`(HF-1・HF-2)/ `docs/notes/oddH_full_proof_v1.md`(§4 補題 G/H・§6 命題 ODD-P)
- `docs/notes/rad2_degree_check_v2.md`(RAD-deg)/ 正典 arXiv 2405.11725 (5.1)
- 外部文献なし。使う代数的事実は **Kronecker–Weber と conductor–discriminant のみ**(標準・§2.4 で使用箇所を明示)。

> ## 封印遵守
> **公開値は $u_3=-4$ ただ一つしか使っていない。** 他の $u_d,u_m$ の値・平方類・$\hat c_\mu$・$c$ の平方類には一切触れていない。本稿の主定理(§4 カスケード定理)は **$u$ の値を一切含まない**(歯の細かさは $\mathrm{rad}(d)$ だけで決まる — §4.3 が要点)。$K^{(5)}$($q=5$)は blind 進行中につき第一適用先から明示除外。
> ⚠ §5 の $q=7$ 適用と §4.4 の族帰結は**測定前の予言**であり、SQ-3q と同じく**凍結(pre-registration)手続きの対象**として扱うことを要請する。

---

## 1. 結論(要旨)

四つ出た。うち二つは発案の主張を**強め**、二つは発案の想定を**訂正**する。

| | 内容 | 発案との差 |
|---|---|---|
| **(A)** | 平方類制限核の一般形は「巡回」を要さない: 任意の有限拡大で $\ker=\{[a]\mid K(\sqrt a)\subseteq L\}$、Galois なら $\cong\operatorname{Hom}(\mathrm{Gal},\pm1)$(§2)。円分塔では $\ker=\langle[p]:p\mid d\rangle\cong(\mathbf Z/2)^{\omega(d)}$ | 発案は「$d=p^k$ 巡回」に限定していた。**素数冪の仮定は不要**で、しかも合成 $d$ でも核の**形が完全に分かる** |
| **(B)** | **カスケード定理**: 使える歯の集合 $\mathcal D$ に対し $[u_m]_2\in E_{\gcd(\mathcal D)}$。**$\{1\}$ に潰れる $\iff\gcd(\mathcal D)=1$**(§4) | 発案の「$\{1,[3]\}\cap\{1,[-7]\}=\{1\}$」は $\gcd(3,7)=1$ の特例。一般判定条件は**判別式の独立性ではなく単なる $\gcd$** に帰着する(判別式の独立性は §2.4 で一度だけ使い、以後は座標部分空間の交叉に還元) |
| **(C)** | $p^*$ の符号規約は **本設定では無効**($i\in F_m$ ゆえ $[-1]=1$、$[p^*]=[p]$)。falsifier 用の懸案 1 件が消える(§2.3) | 発案の「破綻しそうな点」の 1 項を除去 |
| **(D)** | **SQ 述語は体の自己同型で不変**なので、C1/C1′ の脅威は「共役でない曖昧性」に限定される(§6.2) | 発案・i17 の caveat 表を**軽くする**(無害化ではない — 限定) |

さらに **梃子率の定量化**(発案が求めたもの): 第 2 の歯の限界価値は最大、**第 3 の歯の限界価値はゼロ**(§4.5)。

---

## 2. 一般補題 — 平方類の制限核

$\operatorname{char}\ne2$ の体のみ扱う。$[\,a\,]_2$ は $K^\times/K^{\times2}$ の類。

### 2.1 核の同定(巡回性は不要)

> **補題 K1.** $L/K$ を有限拡大とすると
> $$\ker\bigl(K^\times/K^{\times2}\xrightarrow{\ \mathrm{res}\ }L^\times/L^{\times2}\bigr)=\bigl\{[a]\ \big|\ K(\sqrt a)\subseteq L\bigr\},$$
> これは $K^\times/K^{\times2}$ の部分群であり、その非自明元は $L/K$ の**二次中間体**と 1 対 1 に対応する。$L/K$ が Galois で $G=\operatorname{Gal}(L/K)$ なら
> $$\ker\ \cong\ \operatorname{Hom}(G,\{\pm1\})\ \cong\ G^{\rm ab}/(G^{\rm ab})^2 .$$

**証明.** $[a]\mapsto1$ $\iff$ $a\in L^{\times2}$ $\iff$ $\sqrt a\in L$ $\iff$ $K(\sqrt a)\subseteq L$。部分群性: $K(\sqrt a),K(\sqrt b)\subseteq L$ なら $K(\sqrt{ab})\subseteq K(\sqrt a,\sqrt b)\subseteq L$。$[a]\ne1$ のとき $K(\sqrt a)$ は二次中間体で、$K(\sqrt a)=K(\sqrt b)\iff[a]=[b]$(Kummer 理論 $\mu_2\subset K$ は無条件)。Galois の場合、二次中間体 $\leftrightarrow$ 指数 2 部分群 $\leftrightarrow$ $\operatorname{Hom}(G,\pm1)\setminus\{1\}$。$\blacksquare$

> **系 K2(巡回の場合).** $L/K$ が巡回 $f$ 次なら $\ker=\{1,[\delta]\}$($f$ 偶・$K(\sqrt\delta)$ は唯一の二次中間体)、$\ker=\{1\}$($f$ 奇)。

これは **i17 補題 B($f=2$ の初等計算 $y=s+t\sqrt\delta$、$2st=0$)の一般化**であり、発案の項目 1 と一致する。ただし K1 が示すとおり**巡回性は本質ではない** — 効いているのは「二次中間体の集合」だけである。

### 2.2 円分塔での具体形

以下 $F_m:=\mathbf Q(\zeta_{4m})$($正典・i17 §2 と同じ記法$)。

> **補題 K3.** $m\ge3$ 奇、$d\ge3$ 奇、$\gcd(d,m)=1$ とする。このとき
> $$[F_{dm}:F_m]=\varphi(d),\qquad \operatorname{Gal}(F_{dm}/F_m)\xrightarrow{\ \sim\ }(\mathbf Z/d)^\times$$
> であり、
> $$\boxed{\ E_d\ :=\ \ker\bigl(F_m^\times/F_m^{\times2}\to F_{dm}^\times/F_{dm}^{\times2}\bigr)\ =\ \bigl\langle\,[p]\ :\ p\mid d\ \text{素数}\,\bigr\rangle\ \cong\ (\mathbf Z/2)^{\omega(d)}\ }$$
> ($\omega(d)$ = $d$ の相異なる素因数の個数)。**$E_d$ は $m$ にも $d$ の指数にも依らず、$\mathrm{rad}(d)$ だけで決まる。**

**証明.** (i) 次数: $d,m$ 奇で互いに素だから $\varphi(4dm)=\varphi(4)\varphi(d)\varphi(m)=2\varphi(d)\varphi(m)$、$\varphi(4m)=2\varphi(m)$、比は $\varphi(d)$。(機械確認: $3\le d,m<40$ 奇・$\gcd=1$ の全対で一致 — §7 の script A)
(ii) $\gcd(4m,d)=1$ ゆえ $F_m\cap\mathbf Q(\zeta_d)=\mathbf Q(\zeta_{\gcd(4m,d)})=\mathbf Q$、よって制限 $\operatorname{Gal}(F_{dm}/F_m)\to\operatorname{Gal}(\mathbf Q(\zeta_d)/\mathbf Q)=(\mathbf Z/d)^\times$ は同型。
(iii) K1 より $E_d\cong\operatorname{Hom}((\mathbf Z/d)^\times,\pm1)$。$d=\prod p_i^{a_i}$(奇)で $(\mathbf Z/d)^\times\cong\prod(\mathbf Z/p_i^{a_i})^\times$、各因子は位数 $\varphi(p_i^{a_i})$ の**巡回群で位数は偶**。ゆえに $|\operatorname{Hom}|=2^{\omega(d)}$。(機械確認: $3\le d<200$ 奇の全てで $2^{\omega(d)}$ — §7 script A)
(iv) 生成元: $\mathbf Q(\zeta_{p^{a}})$ の唯一の二次部分体は $\mathbf Q(\sqrt{p^*})$、$p^*=(-1)^{(p-1)/2}p$(Gauss 和 / conductor–discriminant)。(ii) の同型で $F_{dm}/F_m$ の二次中間体は $F_m(\sqrt{D_S})$、$D_S=\prod_{p\in S}p^*$($\emptyset\ne S\subseteq P(d)$)。$i=\zeta_4\in F_m$ より $[-1]=1$、ゆえに $[D_S]=\bigl[\prod_{p\in S}p\bigr]$。$\blacksquare$

### 2.3 ★ 符号規約は無効(発案の懸案 1 件の消去)

$4\mid4m$ ゆえ $i\in F_m$、したがって **$F_m$ の中では $[-1]_2=1$、すなわち $[p^*]_2=[p]_2$**。発案の「破綻しそうな点」に挙がっていた *$p^*$ の符号規約* は、$F_m$ 上の平方類の言葉では**一切効かない**。符号が要るのは $\mathbf Q$ 上で「$\mathbf Q(\zeta_{p^a})$ の二次部分体は $\mathbf Q(\sqrt{p^*})$」と言うときだけであり、$F_m$ に上げた瞬間に消える。以後 **$E_d=\langle[p]:p\mid d\rangle$ と素数だけで書く**。

### 2.4 独立性(判別式の独立性を使う唯一の箇所)

> **補題 K4.** $m\ge3$ 奇とする。$2m$ を割らない相異なる奇素数 $p_1,\dots,p_r$ に対し、$[p_1],\dots,[p_r]$ は $F_m^\times/F_m^{\times2}$ の中で $\mathbf F_2$ 独立である。

**証明.** $\prod_{i\in S}[p_i]=1$($S\ne\emptyset$)とすると $F_m(\sqrt{D_S})=F_m$、$D_S=\prod_{i\in S}p_i^*$。各 $p_i^*\equiv1\ (4)$ ゆえ $D_S\equiv1\ (4)$ かつ平方因子なし、よって $D_S$ は**基本判別式**で $\mathbf Q(\sqrt{D_S})$ の conductor は $|D_S|$。Kronecker–Weber と conductor–discriminant より
$$\mathbf Q(\sqrt{D_S})\subseteq\mathbf Q(\zeta_{4m})\iff |D_S|\mid 4m .$$
$|D_S|=\prod_{i\in S}p_i$ は $4m$ と互いに素で $>1$ だから不可能。$\blacksquare$

> **系 K5(座標化).** $V:=\langle[p]:p\ \text{奇素数},\ p\nmid2m\rangle\le F_m^\times/F_m^{\times2}$ は $\{[p]\}$ を基底とする $\mathbf F_2$ ベクトル空間であり、$\gcd(d,m)=1$ かつ $d$ 奇なら $E_d\le V$ は**座標部分空間** $\langle[p]:p\in P(d)\rangle$ である。

---

## 3. 二本差しの一般形 — 命題 SQ-$dm$

### 3.1 対称形(これが本体)

$(T)$ は t63 §2.2 (2.3)、すなわち $d\mid n$・$d\ge3$・ともに奇のとき
$$u_n=\operatorname{res}_{F_n/F_d}(u_d)\cdot w^{2d},\qquad w\in F_n^\times. \tag{T}$$
$u_n$ は $H_n^{\rm fun}$ 窓の cusp 主係数(A7 でモデル非依存)、$\operatorname{res}$ は体の包含による引き戻し(norm ではない — t63 §2.4)。

> **補題 T2(二本差しの対称形).** $d,m\ge3$ 奇、$\gcd(d,m)=1$、$n:=dm$ とする。$(T)$ が両脚 $(n,d),(n,m)$ で成立するなら
> $$\boxed{\ \operatorname{res}_{F_n/F_m}\bigl([u_m]_2\bigr)\ =\ \operatorname{res}_{F_n/F_d}\bigl([u_d]_2\bigr)\quad\text{in } F_n^\times/F_n^{\times2}.\ }$$

**証明.** $w^{2d}=(w^d)^2$、$w'^{2m}=(w'^m)^2$ はいずれも $F_n^\times$ の平方。ゆえに (T)@$(n,d)$ から $[u_n]_2=[\operatorname{res}(u_d)]_2$、(T)@$(n,m)$ から $[u_n]_2=[\operatorname{res}(u_m)]_2$。$\blacksquare$

> **型の注意(i17 I17-2 の再確認)**: (T) は $F_n^\times$ の**元の等式**なので $[\ \cdot\ ]_2$ を直接適用してよい。(6.3-cls)/(6.3-chr) の型混同は $a_n$ 同士を $\bmod\ 2d$ で比べる話であり、本論法には無関係。また $[u]_2=[u^{-1}]_2$ ゆえ $u\leftrightarrow v=u^{-1}$ の取り違えも無害。

### 3.2 命題 SQ-$dm$

> ### 命題 SQ-$dm$
> $d,m\ge3$ 奇、$\gcd(d,m)=1$。$(T)$ が $(dm,d)$ と $(dm,m)$ の両脚で前件(A4–A7・TB1)を満たし、さらに
> $$\textbf{(U3)}\qquad [u_d]_2=1\ \text{ in } F_d^\times/F_d^{\times2}$$
> が成り立つとする。このとき
> $$\boxed{\ [u_m]_2\ \in\ E_d=\bigl\langle[p]:p\mid d\bigr\rangle\ \cong(\mathbf Z/2)^{\omega(d)}\quad\text{in } F_m^\times/F_m^{\times2}.\ }$$

**証明.** (U3) より $\operatorname{res}_{F_n/F_d}([u_d]_2)=1$。補題 T2 より $\operatorname{res}_{F_n/F_m}([u_m]_2)=1$、すなわち $[u_m]_2\in\ker(\mathrm{res}_{F_n/F_m})=E_d$(補題 K3)。$\blacksquare$

> **系(SQ-3q の回収).** $d=3$、$m=q$ 奇素数 $\ne3$: $\omega(3)=1$ ゆえ $E_3=\{1,[3]\}=\{1,[-3]\}$、$[3]\ne1$(補題 K4)。**i17 の命題 SQ-3q と逐語一致**。しかも本証明は $q$ の素数性を使っていない — **$\gcd(q,3)=1$ なる任意の奇数 $m\ge3$ で成立**する(i17 は素数 $q$ に限定していた。射程の拡張)。

### 3.3 二つの精密化(発案・i17 になし)

**(P1) 弱い歯の条件.** SQ-$dm$ の証明が実際に要求するのは (U3) ではなく
$$\textbf{(U3}^-\textbf{)}\qquad \operatorname{res}_{F_{dm}/F_d}([u_d]_2)=1$$
だけである。補題 K3 を $d\leftrightarrow m$ で読むと
$$\ker\bigl(F_d^\times/F_d^{\times2}\to F_{dm}^\times/F_{dm}^{\times2}\bigr)=\bigl\langle[p]:p\mid m\bigr\rangle$$
なので、**(U3$^-$) $\iff$ $[u_d]_2\in\langle[p]:p\mid m\rangle$**。すなわち $[u_d]_2\ne1$ でも、その類が**標的 $m$ の素因数だけで書けている**なら $d$ は使える(ただし歯は $m$ ごとに個別 — 「$m$-特化の歯」)。

**(P2) $\varepsilon\ne1$ の剰余類形.** (U3$^-$) すら成り立たない場合でも、補題 T2 は
$$[u_m]_2\in\mathrm{res}_{F_n/F_m}^{-1}\bigl(\varepsilon\bigr),\qquad \varepsilon:=\operatorname{res}_{F_n/F_d}([u_d]_2)$$
を与える。右辺は空か、さもなくば $E_d$ の**剰余類**(同じ $2^{\omega(d)}$ 個)である。したがって**歯の「目の細かさ」は (U3) の成否に依らず常に $2^{\omega(d)}$**、失われるのは「どの剰余類か」の同定だけ。i17 註「二本目の $d$ を足す道は現状開いていない」は **(U3) を要求した場合の話**であり、(P1)(P2) の下では条件が緩む。

---

## 4. カスケード定理

### 4.1 主定理

標的を奇数 $m\ge3$ に固定する。$m$ に対する **使える歯の集合** を
$$\mathcal D(m):=\{\,d\ge3\ \text{奇}\ \mid\ \gcd(d,m)=1,\ \text{(U1)–(U4) 成立}\,\}$$
と置く(条件は §4.2)。

> ### 定理 CASC(カスケード定理)
> $\mathcal D\subseteq\mathcal D(m)$ を有限部分集合、$g:=\gcd(\mathcal D)$($\mathcal D=\emptyset$ なら $g$ は未定義)とする。このとき
> $$\boxed{\ [u_m]_2\ \in\ \bigcap_{d\in\mathcal D}E_d\ =\ E_g\ =\ \bigl\langle[p]:p\mid g\bigr\rangle\ \cong(\mathbf Z/2)^{\omega(g)} .\ }$$
> とくに
> $$\boxed{\ \bigcap_{d\in\mathcal D}E_d=\{1\}\ \iff\ \gcd(\mathcal D)=1\ \iff\ \mathcal D\ \text{の歯に共通素因数がない}\ }$$
> であり、そのとき $[u_m]_2=1$。

**証明.** 各 $d\in\mathcal D$ に命題 SQ-$dm$ を適用して $[u_m]_2\in E_d$、よって交叉に属する。交叉の計算: 系 K5 により $E_d=\langle[p]:p\in P(d)\rangle$ は基底 $\{[p]\}$ に関する**座標部分空間**である。座標部分空間の交叉は添字集合の交叉上の座標部分空間だから
$$\bigcap_{d\in\mathcal D}E_d=\bigl\langle[p]:p\in\textstyle\bigcap_{d}P(d)\bigr\rangle,\qquad \bigcap_{d}P(d)=P(\gcd\mathcal D).$$
$\gcd(\mathcal D)=1$ なら $P=\emptyset$ で $E_1=\{1\}$。$\blacksquare$

> **註(発案の「判別式類の独立性」の位置).** 独立性は**定理の中では一度も使わない** — 補題 K4 で座標系を作るときに一度だけ使い、以後は線形代数(座標部分空間の交叉)に落ちる。発案が想定した「$\sqrt{3p^*}\in F_{q'}$ になる例外条件」の場合分けは**存在しない**: $\gcd(d,m)=1$ を課した時点で $|D_S|\nmid4m$ が自動なので、例外は起きえない。

### 4.2 「使える歯」の正確な条件

| # | 条件 | 内容 | 値に触れるか |
|---|---|---|---|
| **U1** | 形式 | $d\ge3$ 奇・$\gcd(d,m)=1$($\Rightarrow n=dm$ 奇・両脚とも $\ge3$ で (T) の $d\ge3$ 条件を満たす) | 触れない |
| **U2** | (T) 前件 | $(dm,d)$ と $(dm,m)$ の両脚で A4–A7+TB1。**A4/A5/A6 は全奇数で閉鎖済**(補題 K3・HF-2・ODD-H)。**残るのは A7(BFC B-5 の合成窓 instance)だけ**(→ caveat **C-$dm$**) | 触れない |
| **U3** | 平方類の既知性 | $[u_d]_2=1$(または弱形 (U3$^-$): $[u_d]_2\in\langle[p]:p\mid m\rangle$)が**公開値または証明**から言える | **触れる** |
| **U4** | 窓同定 | 使う $u_d$ が $H_d^{\rm fun}$ 窓の値である(caveat C1$(d)$)。ただし §6.2 で射程を限定 | 触れる |

**公開在庫(2026-07-29 時点)**: $d=3$ のみ。$u_3=-4$、$[-4]_2=[-1]_2[4]_2=[-1]_2=1$($i\in F_3=\mathbf Q(\zeta_{12})$ ゆえ)。他の $d$ については **本稿は台帳を照会しない**(封印遵守)。

### 4.3 ★ 目の細かさは $\mathrm{rad}(d)$ だけで決まる(値非接触の定量化)

補題 K3 の $E_d=\langle[p]:p\mid d\rangle$ は $d$ の**根基のみ**の関数である。したがって:

* $E_{p^k}=E_p$ — **素数冪の歯は素数の歯と同じ目**。発案の「$d=9$ は $p^*=-3$ で在庫を増やさない」は、$\mathrm{rad}(9)=3$ ゆえ $E_9=E_3$ という**値に一切依らない**言明として確立する($u_9$ に触れずに済む)。
* 合成の歯は**目が粗い**: $\omega(d)\ge2$ なら $E_d\supsetneq E_p$($p\mid d$)。単独の歯としては常に劣る。
* しかし**交叉には効く**: 定理 CASC は $\gcd$ しか見ないので、$3\nmid d$ なる**任意の**歯($素数でなくてよい$)が $E_3$ と交わって $\{1\}$ を出す。

### 4.4 帰結の翻訳(Kummer 深度)

i17 補題 C を一般の奇数 $m$ に拡張する(証明は逐語同じ: $\mu_m\subset F_m$、$m$ 奇ゆえ $\zeta=(\zeta^{(m+1)/2})^2$)。

> **補題 C$'$.** $v_m:=u_m^{-1}$、$a_m:=[v_m]_{2m}$ とすると $\operatorname{ord}(a_m)\mid m\iff[u_m]_2=1$。($\operatorname{ord}(a_m)\mid2m$ は自動なので、$[u_m]_2\ne1\iff2\mid\operatorname{ord}(a_m)$。)

したがって定理 CASC の $\gcd(\mathcal D)=1$ の場合:
$$\boxed{\ \operatorname{ord}(a_m)\ \big|\ m\quad(\text{C4 型上界})\ }$$
が前件下で従う。逆枝($[u_m]_2\ne1$)は i17 I17-3 のとおり **(5.1) の前件下で $\operatorname{Ih}_{K^{(m)}}$ 非全射 = Conj 5.1 が窓 $m$ で偽**を意味する — 事前確率は低いが、そのぶん凍結予言としての反証力が高い。

### 4.5 ★ 梃子率(発案が求めた定量化)

標的の族を $\mathcal M$(たとえば $\gcd(m,21)=1$ の奇数 $m\ge3$)とする。歯を 1 本ずつ増やすときの残余曖昧性は

| 歯の在庫 $\mathcal D$ | $\gcd$ | 残余 $E_{\gcd}$ の位数 | 1 標的あたりのビット |
|---|---|---|---|
| $\{3\}$ | 3 | 2 | 1 bit |
| $\{3,7\}$ | 1 | **1** | **0 bit** |
| $\{3,7,11\}$ | 1 | 1 | 0 bit(**増分ゼロ**) |

すなわち **第 2 の歯の限界価値は最大(全標的を一斉に閉じる)・第 3 以降の限界価値はこの述語に関してはゼロ**。これが「$q=7$ 測定一点が族を閉じる」の正確な内容であり、**$u9$ 計画の次期対象選定において $q=7$ を優先する根拠**である。ただし §6 の破綻リスク(とくに A7 の複製)を織り込むと、実効コストは「標的の本数 × 前件監査」で増える(→ §6-R1)。

---

## 5. $q=7$ への第一適用 — 前件リスト

**設定**: 歯 $d=3$、標的 $m=q=7$、合成窓 $n=21$。結論候補: $[u_7]_2\in\{1,[3]\}$ in $F_7^\times/F_7^{\times2}$、$F_7=\mathbf Q(\zeta_{28})$。二択が退化しないこと: $\mathbf Q(\sqrt{-3})$ の conductor $=3\nmid28$ ゆえ $[3]=[-3]\ne1$ ✓(補題 K4)。

| # | 前件 | $(21,3)$ 脚 | $(21,7)$ 脚 | 状態 |
|---|---|---|---|---|
| A4 | 体の塔 | $F_3\subset F_{21}$、$[F_{21}:F_3]=\varphi(7)=6$ | $F_7\subset F_{21}$、$[F_{21}:F_7]=\varphi(3)=2$、$F_{21}=F_7(\sqrt{-3})$ | ✅ 補題 K3(初等) |
| A5 | cover $\bar\pi_{n,d}$(HF-2) | $(21,3)$ | $(21,7)$ | ✅ HF-2 は「$n$ 奇・$d\mid n$・$d\ge3$」で証明済。**機械検分 11 対に $(21,3),(21,7)$ が既在**(i17 §2) |
| A6 | cusp 全分岐・$M_{21}=\operatorname{ord}(X_{21})=42$ | 同左 | 同左 | ✅ ODD-H §4 補題 G/H が全奇数で供給。ordered passport $(2N,2^{N-1}1^2,2N)$、$N=21$(ODD-P) |
| **A7** | 局所 Kummer・$[u]_M$ のモデル非依存(BFC B-5 (ii-loc)(ii-win))の**合成窓 21 での instance** | ❓ | ❓ | ⚠️ **UNKNOWN(caveat C-21)** — i17 の C-3q と同型。$(\mathrm{CAL})$ を要するか未判定・**律速** |
| TB1 | 圏同値 | — | — | 枠組仮定(2026-07-28 裁可: 自前再導出・Lean 化せず) |
| **C1** | $u_3=-4$ が $H_3^{\rm fun}=H_{2,1,0}$ 窓の値 | — | — | ⚠️ **UNKNOWN・最優先**(t63 §5)。ただし §6.2 で射程限定 |
| **C1$'$** | 測定される $u_7$ が $H_7^{\rm fun}$ 窓の値 | — | — | ⚠️ **要事前登録**。$q=7$ の good は $2\cdot7\cdot6=84$ 個・$6$ 類。**ODD-P より単元 $\alpha$ の類は同一 ordered passport** なので passport では識別不能 → **証明書 schema で $(j,[\alpha])=(2,[1])$ を必須欄に**(i17 I17-c) |
| **C5** | 宇宙の事前登録 | — | — | ⚠️ **手続き**: $n=21$ は登録宇宙 $\{3,5,7,9,11\}$ の外。HF-2 機械検分に $21$ が既在なので追記は軽い |

**第二段(カスケード発火条件)**: 上記が全て閉じ、かつ測定が左枝 $[u_7]_2=1$ を出したとき、$d=7$ が歯に加わる(U3 成立)。そのとき定理 CASC より、$\gcd(m,21)=1$ なる**すべての奇数 $m\ge3$** に対し(各 $m$ で A7@$(3m)$・A7@$(7m)$・C1$'(m)$ を追加で要求した上で)
$$[u_m]_2=1,\qquad \operatorname{ord}(a_m)\mid m .$$
**$m=5$ は blind により除外**(手続き)。**$m$ が 3 または 7 で割れる場合は歯が片方しか使えない**ので、残余は 1 bit のまま(§6-R3)。

---

## 6. 自己監査 — 反例・破綻リスク

falsifier に渡す前に自分で潰す/明示する。**R = リスク、○=潰した、△=残る、●=致命**。

### 6.1 数学的な穴

| # | リスク | 判定 |
|---|---|---|
| R-a | 「$\varphi(d)=2$ でないと核が大きい」→ 発案の $d=p^k$ 限定は必要か | ○ **不要**。K1/K3 で任意の $d$ の核が完全に決まる。大きくてよい — 交叉が効く |
| R-b | $p^*$ の符号規約のずれ | ○ **消滅**(§2.3・$i\in F_m$) |
| R-c | $\sqrt{3p^*}\in F_m$ となる例外(発案が心配した点) | ○ **起きない**。$\gcd(d,m)=1$ から conductor 条件が自動で破れる(補題 K4) |
| R-d | 合成 $d$ で核が $(\mathbf Z/2)^{\ge2}$ に太る | ○ **正しいが無害**。太っても座標部分空間なので交叉は $\gcd$ で計算できる(定理 CASC)。単独では劣るだけ |
| R-e | $d$ が偶数・$d=1$ の場合 | ○ **射程外を明記**。(T) は $d\ge3$ 奇を要求(t63 A4–A7)。$d$ 偶は $F_{dm}/F_m$ の 2-部分が変わり $E_d$ の計算式が壊れる(補題 K3 は $\gcd(d,4m)=1$ を使う) |
| R-f | 標的 $m$ が素数でない場合の補題 C$'$ | ○ **成立**($m$ 奇のみ使用)。ただし (5.1) 側(Conj 5.1 との接続)は $K^{(m)}$ の枠組が $m$ 奇で立っていることに依存 |
| R-g | $[u_m]_2$ が $F_m$ の**どの**平方類かを (P2) が同定しない | △ **残る**。$\varepsilon\ne1$ の剰余類形は「目の細かさ」しか保証しない。左枝/右枝の二分法は (U3) 成立時のみ |

### 6.2 ★ C1/C1$'$ の射程限定(部分的な良い知らせ)

> **補題 INV.** $\sigma$ を $F_n$ の体自己同型とすると、任意の $u\in F_n^\times$ と $\lambda\in\mathbf Q^\times$ に対し
> $$[u]_2=[\lambda]_2\ \Longleftrightarrow\ [\sigma(u)]_2=[\lambda]_2 .$$
> **証明.** $u=\lambda y^2\iff\sigma(u)=\lambda\sigma(y)^2$($\sigma(\lambda)=\lambda$)。$\blacksquare$

したがって: **窓の曖昧性が $\operatorname{Gal}(F_n/\mathbf Q)$-共役であるかぎり、SQ 述語($[u]_2=1$ か $[u]_2=[3]$ か)は窓の取り方に依存しない。** これは I-24 の「述語の共役不変性」を SQ 述語について**無条件に**証明したものであり(I-24 の予想 2 の一部)、次を意味する:

* **C1/C1$'$ が SQ-$dm$ に対して脅威になるのは、窓の曖昧性が共役でない場合に限る**(例: $j=2$ 窓と $j=3$ 窓の $u$ が互いに共役でない別値になる場合)。
* 逆に、I-24(a)「$H_{2,\alpha,0}$ たちは Galois 単一軌道か」が肯定なら、**$\alpha$ 類に由来する曖昧性は SQ 述語を一切動かさない**。
* $d=3$ については $u_3=-4\in\mathbf Q$ で全共役が一致するので、**共役曖昧性なら C1 は SQ に関して完全に無害**。

⚠️ これは **無害化ではなく限定**である。「$j$ 分岐が共役かどうか」は本稿では判定できない(I-24(b) の $j=3$ 窓での $u_3$ 再測定が直接の検定)。

### 6.3 工程・手続きのリスク

| # | リスク | 判定 |
|---|---|---|
| **R1** | **A7 の複製(律速)**: 歯 $d$ × 標的 $m$ の**対ごと**に合成窓 $dm$ の BFC instance が要る。族閉鎖しないうちはカスケードは「条件付きの絵」 | ● **最大の危険**。発案の自認どおり。i17-a((CAL) の合成窓版)が族的に閉じるかが全て。**$\{3,7\}$ 二歯 × 標的族なら $2|\mathcal M|$ 個の instance** |
| R2 | C1$(d)$ と C1$'(m)$ の連鎖が全段に相続 | △ §6.2 で**共役曖昧性なら無害**まで限定できたが、非共役曖昧性は残る |
| R3 | $3\mid m$ または $7\mid m$ の標的は片歯のみ($\gcd(d,m)=1$ 違反) | △ **構造的**。$m=9,27,49,\dots$ 型は 1 bit 残る。**標的 $m$ 自身は自分の歯にできない** |
| R4 | 右枝が一度でも出れば篩ごと吹き飛ぶ | ○ **それは最大の収穫**(Conj 5.1 反例)。「破綻」ではない |
| R5 | 凍結手続き: SQ-$dm$ は SQ-3q 凍結の**拡張条項**。版管理を誤ると「測定後に予言を書いた」と見える | △ **手続き**。Sol ゲート提出+タイムスタンプで対処(§8) |
| R6 | 宇宙の事前登録(C5)が標的ごとに要る | △ 軽いが**忘れると無効**。$dm$ の登録を歯×標的の表で一括登録すべき |

### 6.4 「これが偽なら分かる」形の反証点

本稿が偽である最短の道は次の 3 つ。**falsifier はここを突くべき**:

1. **補題 K3 (ii) の $F_m\cap\mathbf Q(\zeta_d)=\mathbf Q$**: $\gcd(d,4m)=1$ を落とすと崩れる。$d,m$ が共通素因数を持つ設定で使っていないか(定理 CASC の $\mathcal D(m)$ 定義で $\gcd(d,m)=1$ を課したか)。
2. **(T) の $w$ の指数**: $w^{2d}$ が本当に $2d$ 乗か($2n$ 乗なら結論は変わらないが、$w^{d}$ で止まっていると平方でなくなり **§3.1 が崩壊**)。t63 §2.2 の導出($e(\rho)=n/d$ と $\lambda_d=u_ds_d^{2d}(1+\cdots)$)を再検すべき点。
3. **A7 の合成窓 instance が (CAL) を要求する**場合: $n=9$ ですら (CAL) は入力未整備で UNKNOWN(`c2c4_closure_v1.md`)。要求するなら**カスケードは当面すべて条件付き**。

---

## 7. 機械確認した箇所

本稿の証明は機械計算に依存しない。以下は**事後の裏取り**のみ。

| # | 確認内容 | 方法 |
|---|---|---|
| script A | $\varphi(4dm)/\varphi(4m)=\varphi(d)$ を $3\le d,m<40$ 奇・$\gcd(d,m)=1$ の全対で確認 / $|\operatorname{Hom}((\mathbf Z/d)^\times,\pm1)|=2^{\omega(d)}$ を $3\le d<200$ 奇の全てで確認 | 数学者の使い捨て整数演算スクリプト(scratchpad・十数行)。**再現には数式 $\varphi(4dm)=2\varphi(d)\varphi(m)$ を直接検算すれば足りる**(証明書として登録する価値なしと判断) |
| 既在 | HF-2 の機械検分 11 対に $(15,3),(15,5),(21,3),(21,7)$ が含まれる | i17 §2 表の引用(`docs/notes/hfun_functoriality_v1.md`) |

---

## 8. 未閉鎖項・次の一手

* 【I23-a】**A7 の合成窓 instance の族化**(= i17-a の一般化)。これが本稿の**唯一の実質的な律速**。$(dm)$ 対ごとでなく「奇 $n$ 一般で A7」が言えるかが問い。
* 【I23-b】**凍結手続き**: 本稿 §4.4/§5 を SQ-3q 凍結の**拡張条項 v2** として、$q=7,11$ を対象に測定前登録(Sol ゲート便)。$q=5$ 除外は i17 と同文。
* 【I23-c】**C5 の一括登録**: 歯 $\{3,7\}$ × 標的族 $\{m\ \text{奇}\ge3:\gcd(m,21)=1,\ m\ne5\}$ の合成窓 $\{3m,7m\}$ を宇宙登録に追記(HF-2 検分済の $15,21$ は既在)。
* 【I23-d】**I-24 との合流**: §6.2 補題 INV により、C1/C1$'$ の SQ 述語への脅威は「非共役曖昧性」に限定された。I-24(b)($j=3$ 窓での $u_3$ 再測定)が**本稿の caveat を直接軽くする最安の実験**である。
* 【I23-e】本稿は紙上(paper-proof candidate)。**Lean 検証ではない**。二系統一致でもない(単系統)。

> ### 【文献要請】
> **困難**: (T) と平方類の組み合わせは「$u_m$ の平方類」を **1 bit まで**しか決めない。$u_m$ の平方類そのものを**被覆データから直接計算する**機構があれば、測定(および C1/C1$'$)を経由せずに左枝/右枝が決まり、本稿のカスケード全体が無条件化する。
> **欲しい結果の型**: 「有限被覆 $\lambda:W\to\mathbf P^1$ の全分岐点における**主係数(leading coefficient)の平方類・より一般に Kummer 類**を、モノドロミー表現・分岐データ・定義体から読む公式」。キーワードの当て: cyclic/dihedral covers の局所主係数、Belyi 写像の cusp expansion の定義体、$\mathbf Q$-有理 uniformizer の下での leading coefficient の Galois 変換則。$\mathrm{GT}$ とは無関係の分野(数論的幾何・被覆理論・Grothendieck dessins の moduli field)にありそう。
> **使い道**: $[u_q]_2$ を測定なしで決める → 二択の解消 → 凍結予言の代わりに定理。
