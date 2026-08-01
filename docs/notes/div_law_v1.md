# DIV-LAW v1 — 奇 dihedral 窓における**安定像の除数法則**(genuine 層の有限データ決定と部分証拠の会計)

**状態札: candidate / 研究内部文書**(論文ではない)
起草: 数学者(Opus 5)/ 2026-08-01 ・ 委嘱 = **採択札 E**(発案係第 18 便・**裁定 394**)
記法・正典: `docs/notes/E1_gt_odd_dih_canonical_v1.md`(以下「E1 ノート」・$\Theta_n$ 座標 = 命題 E1-S1)/ `docs/notes/ihnec_v1.md`(以下「ihnec」・ML-ODD・【IHNEC-GAP-1】・追補 D)/ `docs/week1-定義ノート.md`(定義の正本)/ 正典 arXiv **2401.06870**・**2405.11725**。

> ## 封印遵守
> **$K^{(5)}$ 非接触。** 本稿の定理は「奇 $n\ge3$」で一様に述べるが、**$n=5$ における $d_{\rm gen}(5)$・$d_{\rm arith}(5)$・$\mathrm{ord}(a_5)$ の値は一切主張しない**(形式的な instance として量化に含まれるだけであり、値・測定・窓内計算に触れない)。**検算スクリプトからも $n=5$ を明示的に除外した**(§10.2)。封印 3 量($u_9/a_9$ の値・$c$ の平方類・$\hat c_\mu$)にも触れていない。

---

## 0. 本稿が置くもの・置かないもの

> **置くもの**:
> ① **補題 PIN**($\iota:=[-1,1]$ が**全ての**窓 $N$ で GT-shadow・reduction 整合・したがって genuine。braid 恒等式 2 行)
> ② **補題 CHI**($\widetilde\chi$ の全像が算術層から供給される)
> ③ ★ **定理 DIV-LAW**(奇窓 $K^{(n)}$ の中で「$\mathrm{GT}_{\rm arith}$ を含む部分群」は**約数 $d\mid n$ ただ 1 個**で完全に決まる。捻れ類 $[\kappa]$ は**恒等的に消える**)
> ④ 系 DIV-LAT(束同型)・系 DIV-GEN($\mathrm{GT}_{\rm gen}$ への適用・**降下回数 $\le\Omega(n)$**)・系 DIV-ARITH・系 DIV-CHI-NULL(**$\chi$ 方向に fake は存在しない**)・系 DIV-SPLIT(**分裂屋根は常に全射** — (MCOV) は自動)・**一般窓形 DIV-LAW$^{\rm gen}$**
> ⑤ **パリティ罠**の名指し($(\mathbb Z/2n)^\times$ と $(\mathbb Z/4n)^\times$・裁定 209 型)
> ⑥ **換算表**(部分証拠の会計 = 約数束の中の区間演算)
> ⑦ 【IHNEC-GAP-1】の帰結の明文化(**優先度の組み替え**)と前件表(FAM-U-ASM 方式)
>
> **置かないもの**: **新しい算術**。$d_{\rm gen}(n)$ の値は**どの奇 $n$ でも UNKNOWN のまま**である。本稿は「未知量の**型**」を $\mathrm{GT}(K^{(n)})$ の部分群という無限に細かい対象から**約数 1 個**へ落としただけであり、その値を決める装置は与えない(【DIV-GAP-1】)。**有限深度の PASS から genuine を導く経路は本稿にも無い**(工房の掟 2 は不変・§6.4)。

---

## 1. 記法(再定義はしない)

$n$ は以下つねに**奇数 $\ge3$**。$T:=\mathrm{GT}(K^{(n)})$、$M:=K^{(n)}_{\rm ord}=2n$。

**(1.1) $\Theta_n$ 座標**(E1 ノート 命題 E1-S1・正典 Thm 4.3 (4.12) を入力とする):
$$\Theta_n:\ T\ \xrightarrow{\ \sim\ }\ \mathrm{Aff}(\mathbb Z/n)\times C_2,\qquad [m,f]\longmapsto(k,\ u,\ \varepsilon),\qquad u=2m+1\bmod n,\ \ \varepsilon=m\bmod2,$$
$$(k_1,u_1,\varepsilon_1)\cdot(k_2,u_2,\varepsilon_2)=(k_1+u_1k_2,\ u_1u_2,\ \varepsilon_1+\varepsilon_2),\qquad\lvert T\rvert=2n\varphi(n).$$
($k$ は (4.12) の $f$-三つ組 $(r^{2k},r^{-2k},r^{\varkappa(m)})$ の第 1 成分から復元される。$n$ 奇ゆえ $2\in(\mathbb Z/n)^\times$。)

**(1.2) $\widetilde\chi$ と $\mathfrak F_0$**(`kerchi_equality_v2.md` 定理 T-A・E1 ノート (S1)):
$$\widetilde\chi=\widetilde\chi_{2M}:\ T\longrightarrow(\mathbb Z/4n)^\times,\qquad[m,f]\longmapsto2m+1\ (\mathrm{mod}\ 4n),\qquad\ker\widetilde\chi=\mathfrak F_0=\{[0,f]\}\cong C_n.$$
$n$ 奇より CRT で $(\mathbb Z/4n)^\times\cong(\mathbb Z/n)^\times\times(\mathbb Z/4)^\times$、$\Theta_n$ の下で
$$\boxed{\ \widetilde\chi\ \longleftrightarrow\ (k,u,\varepsilon)\mapsto(u,\varepsilon)\ },\qquad Q:=(\mathbb Z/4n)^\times\cong(\mathbb Z/n)^\times\times C_2,\ \ \lvert Q\rvert=2\varphi(n),$$
($\widetilde\chi:T\to Q$ 自体は (THM43) より無条件に**全射**である — 問題になるのは**部分群の像**であり、それが §3。)
$$\mathfrak F_0=\{(k,1,0)\}\cong C_n,\qquad\text{共役作用}\ (k,u,\varepsilon)\cdot(k',1,0)\cdot(k,u,\varepsilon)^{-1}=(uk',1,0)\ \ (\textbf{乗法作用}).$$
すなわち $T=\mathfrak F_0\rtimes Q^{\rm std}$、$Q^{\rm std}:=\{(0,u,\varepsilon)\}$、$C_2=\varepsilon$ 因子は $\mathfrak F_0$ に**自明に**作用する。

**(1.3) 標準部分群**。$d\mid n$、$e:=n/d$ に対し
$$\mathfrak F_0[d]:=\{(k,1,0):k\equiv0\ (\mathrm{mod}\ e)\}\ (\cong C_d\ \text{= }\mathfrak F_0\text{ の唯一の位数 }d\text{ 部分群}),$$
$$\boxed{\ H_d:=\mathfrak F_0[d]\rtimes Q^{\rm std}=\{(k,u,\varepsilon)\in T\ :\ k\equiv0\ (\mathrm{mod}\ n/d)\}\ },\qquad\lvert H_d\rvert=2d\varphi(n),\ [T:H_d]=n/d.$$
$H_1=Q^{\rm std}$、$H_n=T$。($\mathfrak F_0[d]$ は巡回群の部分群ゆえ乗法作用で安定 — **これが「units 不変性は自動」の正体**;§4.1 証明 (b))。

**(1.4) 三層**(ihnec (1.A)):$\mathrm{GT}_{\rm arith}(K^{(n)})\subseteq\mathrm{GT}_{\rm gen}(K^{(n)})\subseteq T$。
$$d_{\rm arith}(n):=\lvert\mathrm{GT}_{\rm arith}(K^{(n)})\cap\mathfrak F_0\rvert,\qquad d_{\rm gen}(n):=\lvert\mathrm{GT}_{\rm gen}(K^{(n)})\cap\mathfrak F_0\rvert,\qquad d_N:=\lvert\mathrm{Im}\,R_{N,K^{(n)}}\cap\mathfrak F_0\rvert.$$

**引用する正典・工房の主張**(再証明しない):

| 札 | 内容 | 出所 |
|---|---|---|
| **(E1-1)** | 全 $n\ge3$ で $K^{(n)}$ は isolated ⟹ $T$ は有限群 | 2405 Lemma 4.2 / Thm 4.3 |
| **(THM43)** | $\mathrm{GT}(K^{(n)})$ の明示形 (4.12) | 2405 Thm 4.3 |
| **(E1-S1)** | $\Theta_n$ が群同型 | E1 ノート §2.1(工房・paper-proof)。$n=9$ で **11,664 対 cross-check**(裁定 379・ihnec 追補 C.3) |
| **(HOM)** | isolated $N\le H$ で $R_{N,H}$ は群準同型 | 2401 Remark 3.16 |
| **(COR54)** | genuine $\iff$ 全細分 $K$ で $\mathrm{Im}\,R_{K,N}$ に属す | 2401 Cor 5.4 |
| **(INT)** | isolated $\cap$ isolated $=$ isolated(有向性) | 2401 Prop 3.15(**証明は原論文に無い** — ihnec 追補 B.2 の自前証明を使う) |
| **(AR)** | $\mathrm{Ih}(g)=\bigl(\tfrac{\chi(g)-1}2,f_g\bigr)$ かつ $\chi:G_{\mathbb Q}\to\widehat{\mathbb Z}^\times$ 全射 | 2405 (1.5)・Kronecker–Weber |
| **(LS-CC)** | 複素共役の像 $=(-1_{\widehat{\mathbb Z}},\,1_{\widehat F_2})$ | Lochak–Schneps [20, Thm 1](2405 §1 が「elementary tools」(ii) として明示引用) |
| **(ARG)** | arithmetical $\Rightarrow$ genuine | 2405 §1.3 / 正典 Def 4.2 |

---

## 2. 補題 PIN — 全ての窓に共通の**錨**

### 2.1 補題 PIN-A(存在と reduction 整合)

> ### 補題 PIN-A
> $\iota_N:=[-1,\,1]$($m=-1$、$f=1$)は **任意の** $N\in\mathrm{NFI}_{PB_3}(B_3)$ に対して $\mathrm{GT}(N)$ の元であり、
> $$R_{N,H}(\iota_N)=\iota_H\qquad(N\le H\ \text{の全ての対で}).$$
> さらに奇 $n\ge3$ に対し $\ \Theta_n(\iota_{K^{(n)}})=(0,\,-1,\,1)\ $、$\ \widetilde\chi(\iota)=-1\in(\mathbb Z/4n)^\times$、$\ \iota^2=1$。

**証明.** $\Delta:=\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2$、$c=\Delta^2$(中心)。$m=-1$ ゆえ $2m+1=-1$、$f=1$。

*(a) hexagon(定義ノート §2 (3.3)(3.4))*。**$B_3$ の中の恒等式として**成り立つ(mod $N$ に落とす前に成立するので、全ての $N$ で自動):
$$\text{(3.3) 右辺}=\sigma_1\sigma_2\,x^{1}\,c^{-1}=\underbrace{(\sigma_1\sigma_2\sigma_1)}_{\Delta}\sigma_1\Delta^{-2}=\Delta^{-1}\sigma_1=(\sigma_1\sigma_2\sigma_1)^{-1}\sigma_1=\sigma_1^{-1}\sigma_2^{-1}=\text{(3.3) 左辺},$$
$$\text{(3.4) 右辺}=\sigma_2\sigma_1\,y^{1}\,c^{-1}=\underbrace{(\sigma_2\sigma_1\sigma_2)}_{\Delta}\sigma_2\Delta^{-2}=\Delta^{-1}\sigma_2=(\sigma_2\sigma_1\sigma_2)^{-1}\sigma_2=\sigma_2^{-1}\sigma_1^{-1}=\text{(3.4) 左辺}.$$
($x=\sigma_1^2$、$y=\sigma_2^2$、$\Delta^{-2}$ が中心であることだけを使う。)

*(b) charming*。$\gcd(2m+1,N_{\rm ord})=\gcd(-1,N_{\rm ord})=1$ ✓。$f=1\in[F_2/N_{F_2},F_2/N_{F_2}]$ ✓。

*(c) $T_{m,f}$ の全射性*。$T_{-1,1}(\sigma_1)=\sigma_1^{-1}N$、$T_{-1,1}(\sigma_2)=1^{-1}\sigma_2^{-1}1\,N=\sigma_2^{-1}N$。像は $\langle\sigma_1^{-1}N,\sigma_2^{-1}N\rangle=B_3/N$ ✓。以上より $\iota_N\in\mathrm{GT}(N)$。

*(d) reduction 整合*。(3.60) より $R_{N,H}([-1,1])=(-1\bmod H_{\rm ord},\ 1\cdot H_{F_2})=\iota_H$ ✓。

*(e) 座標*。$m=-1\equiv2n-1\ (\mathrm{mod}\ 2n)$ は奇だから $\varepsilon=1$、$u=2m+1=-1\bmod n$。$f=1$ ゆえ $f$-三つ組は $(1,1,1)$、すなわち $r^{2k}=1\Rightarrow k=0$(第 3 成分の整合: $m$ 奇より $\varkappa(m)=m+1=2n\equiv0$、$r^{2n}=1$ ✓)。$\iota^2$: $(0,-1,1)^2=(0+(-1)\cdot0,\ 1,\ 0)=(0,1,0)$ ✓。∎

> **★ 実物での確認**: 証明書 `certificates/K9.v1.json` の shadow index 1 が **$m=17$($=-1\bmod18$)・`f_word`=[]・`f_triple`=$((0,0),(0,0),(0,0))$** = $\iota$ そのものであり、$\Theta_9(\iota)=(0,8,1)$、合成表で $\iota^2=$ index 0(単位元)。**証明書に既に入っていた**(§10.2 検査 (G))。
> **★ $c\ne1$ の窓での確認**: 定義ノート §4-7 の **$N_5$ control**($c$ の位数 5)で $f=1$ の charming GT-pair は $m\in\{0,1,3,4\}$ であり、$m=-1\equiv4$ が含まれる(§10.2 検査 (I))。**$c^m$ 項が非自明な窓でも補題 PIN-A が生きる**ことの確認。

### 2.2 系 PIN-gen($\iota$ は genuine)

> ### 系 PIN-gen
> **(COR54)** の下で、$\iota_N$ は**全ての** $N$ で genuine。すなわち $\iota\in\mathrm{GT}_{\rm gen}(N)$、とくに $\iota\in\mathrm{Im}\,R_{K,N}$($\forall K\subseteq N$)。

**証明.** 任意の細分 $K\subseteq N$ に対し補題 PIN-A より $\iota_K\in\mathrm{GT}(K)$ かつ $R_{K,N}(\iota_K)=\iota_N$。ゆえに $\iota_N\in\mathrm{Im}\,R_{K,N}$ が全 $K$ で成り立ち、(COR54) より genuine。∎
**(別経路)** $(\iota_N)_N\in\varprojlim\mathrm{ML}$ は (LIM) により $\widehat{GT}_{\rm gen}$ の元 $(-1,1)$ を与える(こちらは (LIM) を使うので上の証明の方が安い)。

### 2.3 補題 PIN-B(算術版・**正典 pin**)

> ### 補題 PIN-B
> **(AR)(LS-CC)** の下で、複素共役 $\mathfrak c\in G_{\mathbb Q}$ に対し $\mathrm{Ih}(\mathfrak c)=(-1,1)$、ゆえに
> $$\iota_N=\mathrm{Ih}_N(\mathfrak c)\in\mathrm{GT}_{\rm arith}(N)\qquad(\forall N).$$

**証明.** (LS-CC) と $\mathcal{PR}_N(-1,1)=[-1,1]=\iota_N$。∎

> **注**: E1 ノート FINDING $\Phi$1 が「$m=2n-1$ は $u\equiv-1\ (4n)$ すなわち**複素共役に対応する元**」と書いているのは同じ元である。正典 2405 Thm 5.3 の証明(2 冪の場合)は「$(0,-1)$ による共役」を使っており、**正典自身がこの pin を使って像を測っている**(2405 抽出ノート §「elementary tools」(ii))。
> **⚠ 依存の分離**: 本稿の主定理は **PIN-A + PIN-gen だけ**で回る(§4)。**PIN-B は $\mathrm{GT}_{\rm arith}$ を厳密標準形に固定するときにだけ要る**(系 DIV-ARITH)。混ぜないこと。

---

## 3. 補題 CHI — $\widetilde\chi$ 全像はどこから来るか

> ### 補題 CHI
> **(E1-1)(AR)** の下で
> $$\widetilde\chi\bigl(\mathrm{GT}_{\rm arith}(K^{(n)})\bigr)=(\mathbb Z/4n)^\times .$$
> ゆえに $\mathrm{GT}_{\rm arith}(K^{(n)})\subseteq H\subseteq T$ なる**任意の**中間部分集合 $H$ について $\widetilde\chi(H)=(\mathbb Z/4n)^\times$。

**証明.** (AR) より $\widetilde\chi(\mathrm{Ih}_{K^{(n)}}(g))=2\cdot\frac{\chi(g)-1}2+1=\chi(g)\ (\mathrm{mod}\ 4n)$、$\chi$ は全射(Kronecker–Weber)ゆえ $\chi\bmod4n$ は $(\mathbb Z/4n)^\times$ へ全射。$\mathrm{Ih}_{K^{(n)}}$ が well-defined($\mathrm{GT}(K^{(n)})$ への写像)であることに (E1-1) を使う。∎

> **出所と格**: これは工房の **(S2) = W2-arith**(`w2arith_v1.md` 判定 = 「閉鎖(全奇数 $n\ge3$)・二経路」/ 裁定 122)そのものである。**Route A(正典 2405 (1.5) 引用)は枠組み仮定を使わない**。
> ⚠ **格の食い違い(申し送り §9)**: ihnec §6.4 系 SPLIT-NULL′ は同じ (S2) を「**framework-conditional**」と記帳している。`w2arith_v1.md` の Route A は正典引用のみで閉じており、framework 依存は Route B(内在的・(CAL)+(TB2)+(TB4$^{\rm u}$))の側にある。**本稿は Route A を採り「paper-proof(正典引用)」と記帳する**が、両文書の格が違うこと自体は司令塔の裁定事項として上申する(§9)。
> **⚠ 有限側だけでは出ない**: $\widetilde\chi(T)=(\mathbb Z/4n)^\times$ 自体は (THM43) から無条件に出るが、本補題が要るのは**部分群 $H$ の像**についてであり、それは算術層の充満性からしか来ない。**ここが本稿で唯一の算術的入力**である。

---

## 4. ★ 主定理 DIV-LAW

### 4.1 定理

> ### 定理 DIV-LAW(**安定像の除数法則**)
> $n$ 奇 $\ge3$、$T=\mathrm{GT}(K^{(n)})$、$\Theta_n$ 座標(1.1)–(1.3)。$H\le T$ を部分群とし
> **(CHI)** $\widetilde\chi(H)=(\mathbb Z/4n)^\times$(**$\varepsilon$ 成分を含む全像**)
> を仮定する。$d:=\lvert H\cap\mathfrak F_0\rvert$ と置くと $d\mid n$ であり:
>
> **(1) 位数**: $\lvert H\rvert=2d\varphi(n)$、$[T:H]=n/d$。
> **(2) 分類(捻れ類の消滅)**: $H$ は $H_d$ の $\mathfrak F_0$-共役である。すなわち分類不変量
> $$[\kappa]\in H^1\bigl((\mathbb Z/4n)^\times,\ \mathfrak F_0/\mathfrak F_0[d]\bigr)$$
> は**恒等的に $0$** であり、$d$ を固定したとき条件を満たす $H$ はちょうど $n/d$ 個・単一の $\mathfrak F_0$-軌道をなす。
> **(3) 錨づけ(厳密形)**: さらに **(PIN)** $\iota=(0,-1,1)\in H$ を仮定すれば
> $$\boxed{\ H=H_d=\{(k,u,\varepsilon)\in T\ :\ k\equiv0\ (\mathrm{mod}\ n/d)\}\ }$$
> — $H$ は**約数 $d$ ただ 1 個**で完全に決まり、所属判定は **$k$ 座標の合同式 1 本**になる。
> **(4)** $H=T\iff d=n$。

**証明.**

**(a) $d\mid n$ と (1).** $H\cap\mathfrak F_0$ は巡回群 $\mathfrak F_0\cong C_n$ の部分群だから $\mathfrak F_0[d]$($d\mid n$)。$\widetilde\chi|_H$ の核は $H\cap\mathfrak F_0$ だから第一同型定理で $\lvert H\rvert=d\cdot\lvert\widetilde\chi(H)\rvert=d\cdot2\varphi(n)$。$\lvert T\rvert=2n\varphi(n)$ より指数 $n/d$。

**(b) 商への還元(★ units 不変性が自動である段).** $\mathfrak F_0[d]$ は巡回群 $\mathfrak F_0$ の**特性部分群**、したがって $T$ の正規部分群である。**同じことを $\Theta_n$ で言えば**: $Q$ の $\mathfrak F_0$ への作用は「$u$ 倍」という**乗法作用**であり、$\mathbb Z/n$ の部分群はすべて乗法で安定だから、$H\cap\mathfrak F_0$ の $\widetilde\chi(H)$-不変性は**条件ではなく自動**である(発案係のスケッチの 1 行目はここで正しい)。$A:=\mathfrak F_0/\mathfrak F_0[d]\cong\mathbb Z/e$($e=n/d$)と置くと
$$T/\mathfrak F_0[d]=A\rtimes Q^{\rm std},\qquad H/\mathfrak F_0[d]\ \text{は }A\ \text{の補群}$$
($H/\mathfrak F_0[d]$ は $A$ と自明にしか交わらず($H\cap\mathfrak F_0=\mathfrak F_0[d]$)、(CHI) より $Q$ へ全射)。可換正規部分群 $A$ の補群の $A$-共役類は $H^1(Q,A)$ で分類される(標準)。

**(c) $H^1(Q,A)=0$(初等 3 行).** $z\in Q$ を $u$-成分 $=-1$、$\varepsilon$-成分 $=0$ の元とする($n\ge3$ ゆえ位数 2)。$z$ は $A$ に $-1$ 倍で作用する。$\kappa\in Z^1(Q,A)$ とすると $Q$ は可換だから $zq=qz$、cocycle 条件より
$$\kappa(z)+z\!\cdot\!\kappa(q)=\kappa(zq)=\kappa(qz)=\kappa(q)+q\!\cdot\!\kappa(z)\ \Longrightarrow\ 2\kappa(q)=(1-q)\kappa(z).$$
$\lvert A\rvert=e$ は**奇数**だから $2\in(\mathbb Z/e)^\times$。$b:=2^{-1}\kappa(z)$ と置けば $\kappa(q)=(1-q)b=-\bigl(q\!\cdot\!b-b\bigr)=\partial(-b)(q)$、すなわち $\kappa\in B^1$。ゆえに $H^1(Q,A)=0$。
また $A^Q\subseteq A^{\langle z\rangle}=A[2]=0$ だから $B^1\cong A$ で、補群はちょうど $e=n/d$ 個・単一 $A$-軌道。これを $T$ へ引き戻して (2)。

**(d) $\iota$ による錨づけ.** $g=(k_0,1,0)\in\mathfrak F_0$ による共役は
$$gH_dg^{-1}=\{(k+(1-u)k_0,\ u,\ \varepsilon)\ :\ k\in\mathfrak F_0[d]\}.$$
これが $\iota=(0,-1,1)$ を含む $\iff$ $\exists k\in\mathfrak F_0[d]:k+2k_0=0$ $\iff$ $2k_0\equiv0\ (\mathrm{mod}\ e)$ $\iff$($e$ 奇より)$k_0\equiv0\ (\mathrm{mod}\ e)$ $\iff$ $k_0\in\mathfrak F_0[d]$ $\iff$ $gH_dg^{-1}=H_d$。ゆえに軌道の $n/d$ 個のうち $\iota$ を含むのはちょうど $H_d$ 一つ。これが (3)。

**(e)** $d=n\iff\lvert H\rvert=2n\varphi(n)=\lvert T\rvert\iff H=T$。∎

> ### 系 DIV-COSET(**所属判定の形**)
> (3) の下で、$H_d$ の**左剰余類は写像 $(k,u,\varepsilon)\mapsto k\bmod(n/d)$ の fiber** そのものである:
> $$(k_0,1,0)H_d=\{(k,u,\varepsilon):k\equiv k_0\ (\mathrm{mod}\ n/d)\}.$$
> ⟹ **$T$ の $H_d$ による剰余類分解は「$k$ の合同類」による分解**であり、$T/H_d\cong\mathbb Z/(n/d)$($T$ は affine に作用)。

### 4.2 系 DIV-LAT(**束としての除数法則**)

> ### 系 DIV-LAT
> $\mathcal H:=\{H\ :\ \mathrm{GT}_{\rm arith}(K^{(n)})\subseteq H\le T\}$ と置く。**(AR)(LS-CC)** の下で $\mathcal H$ の全ての元は (CHI)(PIN) を満たす(補題 CHI・補題 PIN-B)。したがって
> $$\boxed{\ \mathcal H\ \xrightarrow{\ \sim\ }\ \{d:\ d_{\rm arith}\mid d\mid n\},\qquad H\longmapsto d(H)=\lvert H\cap\mathfrak F_0\rvert\ }$$
> は**束同型**である:
> $$H_d\cap H_{d'}=H_{\gcd(d,d')},\qquad\langle H_d,H_{d'}\rangle=H_{\mathrm{lcm}(d,d')},\qquad H_d\subseteq H_{d'}\iff d\mid d'.$$
> とくに $[\mathrm{GT}_{\rm arith},T]$ は $\prod_{p\mid n}\bigl[v_p(d_{\rm arith}),v_p(n)\bigr]$ という**鎖の直積(分配束)**であり、
> $$\textbf{真に減少する鎖の長さ}\ \le\ \Omega(n)-\Omega(d_{\rm arith})\ \le\ \Omega(n)\qquad(\Omega=\text{重複込みの素因子数}).$$

**証明.** 定理 DIV-LAW (3) より $\mathcal H\ni H\mapsto H_{d(H)}$。$H_d\cap H_{d'}=\{k\equiv0\ (e),\ k\equiv0\ (e')\}=\{k\equiv0\ (\mathrm{lcm}(e,e'))\}=H_{\gcd(d,d')}$($e=n/d$)。生成側は双対。$H_d\supseteq\mathrm{GT}_{\rm arith}=H_{d_{\rm arith}}\iff d_{\rm arith}\mid d$。鎖の長さは約数鎖の長さ。∎

### 4.3 系 DIV-GEN($\mathrm{GT}_{\rm gen}$ への適用 — **本稿の標的**)

> ### 系 DIV-GEN
> **(E1-1)(THM43)(E1-S1)(HOM)(COR54)(INT)(AR)(LS-CC)(ARG)** の下で、奇 $n\ge3$ に対し:
> **(1)** 各 isolated $N\subseteq K^{(n)}$ で $\mathrm{Im}\,R_{N,K^{(n)}}=H_{d_N}$($d_N\mid n$)。
> **(2)** $\displaystyle\mathrm{GT}_{\rm gen}(K^{(n)})=\bigcap_N\mathrm{Im}\,R_{N,K^{(n)}}=H_{d_{\rm gen}},\qquad d_{\rm gen}=\gcd_N d_N .$
> **(3) genuine 判定は $k$ の合同式 1 本**:
> $$\boxed{\ [m,f]\ \text{が genuine}\iff k([m,f])\equiv0\ \bigl(\mathrm{mod}\ n/d_{\rm gen}\bigr)\ }$$
> — **$u$ にも $\varepsilon$ にも依存しない**。fake の集合は $H_{d_{\rm gen}}$ の非自明左剰余類の合併($n/d_{\rm gen}-1$ 個)であり、その元数は $(n-d_{\rm gen})\cdot2\varphi(n)$。
> **(4) 全 shadow が genuine(ML-ODD (iii) の $n$ 成分)$\iff d_{\rm gen}=n$。**
> **(5) 降下回数の上界**: 減少族 $\{\mathrm{Im}\,R_{N,K^{(n)}}\}_N$ の**真の降下は高々 $\Omega(n)$ 回**。とくに $n=q$ 素数なら**高々 1 回** ⟹ $\mathrm{GT}_{\rm gen}(K^{(q)})\in\{H_1,\ T\}$ の**2 択(1 ビット)**。

**証明.** (1) $N$、$K^{(n)}$ ともに isolated ゆえ (HOM) で $R$ は準同型、像は部分群。(ARG)+(COR54) より $\mathrm{GT}_{\rm arith}\subseteq\mathrm{GT}_{\rm gen}\subseteq\mathrm{Im}\,R_{N,K^{(n)}}$、よって補題 CHI で (CHI)、補題 PIN-B(または系 PIN-gen)で (PIN) が成立し、定理 DIV-LAW (3)。
(2) ML-ODD (ii)$\iff$(iii) の段(ihnec §4.3;(COR54)+(INT) で isolated への制限が正当)より $\mathrm{GT}_{\rm gen}=\bigcap_N\mathrm{Im}\,R$。系 DIV-LAT の交叉公式(有限個ずつ取れば十分 — $T$ は有限)。
(3) 系 DIV-COSET。(4) 定理 (4)。(5) 系 DIV-LAT。∎

> **★ T-25 との関係(工房内の先行)**: 対話帳 **T-25** の系 GEN9-$\Lambda$ は $n=9$ で「$\mathrm{GT}_{\rm gen}(K^{(9)})$ の指数は $\{1,3,9\}$ のいずれか」を出していた。系 DIV-GEN は **(i) 全奇 $n$ へ一般化し、(ii) 指数だけでなく部分群そのものを $H_d$ と特定する**。$n=9$ での帰結は T-25 と整合($[T:H_d]\in\{1,3,9\}$)。**新規性の申告は §10.3。**

### 4.4 系 DIV-ARITH(算術層・**既知の機械の再導出**)

> ### 系 DIV-ARITH
> **(AR)(LS-CC)(E1-1)** の下で $\mathrm{GT}_{\rm arith}(K^{(n)})=H_{d_{\rm arith}}$、$d_{\rm arith}=\lvert\mathrm{Ih}_{K^{(n)}}(G_{\mathbb Q(\zeta_{4n})})\rvert$。ゆえに
> $$\textbf{odd Conj 5.1 が窓 }n\text{ で成立}\iff d_{\rm arith}(n)=n .$$
> さらに **定理 $R^{\rm cyc}_{\rm formal}$ の前件 (0)(1)(2)(3)(5′)(6′)** の下で(**framework-conditional**)
> $$d_{\rm arith}(n)=\mathrm{ord}\bigl(a_n\bigr),\qquad a_n=[u_n^{-1}]_{2n}\in F_n^\times/F_n^{\times2n},\ F_n=\mathbb Q(\zeta_{4n}).$$

**証明.** 前半は定理 DIV-LAW を $H=\mathrm{GT}_{\rm arith}$ に適用(補題 CHI・補題 PIN-B)。$\widetilde\chi\circ\mathrm{Ih}=\chi_{4n}$ より $\mathrm{Ih}_{K^{(n)}}(g)\in\mathfrak F_0\iff g\in G_{\mathbb Q(\zeta_{4n})}$。後半は `week4-K3飽和_opus_v3.md` §5.2.2 の**証明の段 2**「$\lvert\mathrm{Ih}_N(G_K)\rvert=\mathrm{ord}([u^{-1}]_M)$」— (R6-full) は「$=e$ か否か」の形で述べられているが、証明は**位数の等式そのもの**を出している。本稿はこの等式を**名前をつけて取り出す**だけである。∎

> ⚠ **これは $R^{\rm cyc}_{\rm formal}$ の再証明ではない**。(S1)(S2)(S4) の勘定(E1 ノート §5.1)は既にこの形をしており、系 DIV-ARITH は**その勘定を「値 $=n$ か否か」から「値そのもの」へ読み替えた**にすぎない。本稿の新しさは §4.3(**同じ勘定を genuine 層と細分の像へ移す**)にある。

### 4.5 系 DIV-CHI-NULL / 系 DIV-SPLIT(**$\chi$ 方向に fake は無い**)

> ### 系 DIV-CHI-NULL
> 奇窓 $K^{(n)}$ では、**$\widetilde\chi$-fiber($=m$-fiber)全体が欠落する型の fake は存在しない**。
> より一般に、$\mathrm{GT}_{\rm arith}(K^{(n)})$ を含み **$\widetilde\chi$-fiber の合併になっている**部分集合 $S\subseteq T$ は $S=T$ に限る。

**証明.** $S$ が $\widetilde\chi$-fiber の合併なら $S=\widetilde\chi^{-1}(\widetilde\chi(S))$。補題 CHI より $\widetilde\chi(S)\supseteq\widetilde\chi(\mathrm{GT}_{\rm arith})=(\mathbb Z/4n)^\times$。ゆえに $S=T$。∎

> ### 系 DIV-SPLIT(**ihnec 追補 D の (MCOV) は奇 dihedral 標的では自動**)
> ihnec 定理 SPLIT-NULL の設定($n$ 奇 $\ge3$、$N'$、$M=K^{(n)}\cap N'$、$G_n$ と $PB_3/N'$ に共通の非自明商なし)で、**(AR) の下では前件 (MCOV) は自動的に成立し**、
> $$R_{M,K^{(n)}}\ \text{は全射}.$$
> **⚠ ここでは $M$ の isolated 性も (HOM) も使わない**(像が部分群であることを使わない — 使うのは「$\widetilde\chi$-fiber の合併である」ことと「$\mathrm{GT}_{\rm arith}$ を含む」ことだけ)。
> ⟹ ihnec 追補 D.1.5 の「**(MCOV) 破れを探す走査**(【IHNEC-GAP-2】の新しい安価な標的)」は、**標的が奇 dihedral 窓である限り空である**(走らせても何も出ない)。

**証明.** 定理 SPLIT-NULL より $\mathrm{Im}\,R_{M,K^{(n)}}$ は $\widetilde\chi$-fiber の合併。(ARG)(COR54) より $\mathrm{GT}_{\rm arith}\subseteq\mathrm{Im}$。系 DIV-CHI-NULL より $\mathrm{Im}=T$。$\mathrm{Im}=T$ と主公式から (MCOV) が従う。∎

> **★ 記帳の正確な形**: これは ihnec 追補 D.1.2 の「**(MCOV) の供給経路 ①(framework-conditional: (S2)=W2-arith)**」を**一般に閉じた**ものであって、新しい機構ではない。**新しいのは「①が常に発火する ⟹ ②(直接測定)も破れ探索も不要」という帰結**である。
> **⚠ 射程**: 標的が**奇 dihedral 窓**であることが本質(補題 CHI が要る)。壁窓や $\mathfrak F_0$ が非巡回の窓を**標的**にする場合には適用しない。
> **⚠ 便 98 の判定は無傷**: 便 98 F98-3.7 が旧 系 SPLIT-NULL″ の無条件形を FAIL としたのは**論理として正しい**(前件 (MCOV) の脱落)。本系はその前件を**別経路で供給**したのであって、判定を覆すものではない。

### 4.6 一般窓形 DIV-LAW$^{\rm gen}$(奇 dihedral 以外へ)

> ### 定理 DIV-LAW$^{\rm gen}$
> $N$ を isolated 窓、$\mathfrak F_0(N)=\ker\widetilde\chi_{2N_{\rm ord}}$ が**巡回**で位数 $e_N$ とする。$\mathrm{GT}_{\rm arith}(N)\subseteq H\le\mathrm{GT}(N)$ なる部分群について、$Q_N:=\widetilde\chi(\mathrm{GT}_{\rm arith}(N))$ と置くと
> $$\lvert H\cap\mathfrak F_0\rvert=:d(H)\ \mid e_N,\qquad\lvert H\rvert=d(H)\cdot\lvert Q_N\rvert,\qquad H=\mathrm{GT}(N)\iff d(H)=e_N\ \text{かつ}\ Q_N=\widetilde\chi(\mathrm{GT}(N)),$$
> $$d\Bigl(\bigcap_iH_i\Bigr)=\gcd_i d(H_i),\qquad\textbf{真の降下回数}\le\Omega(e_N).$$
> **分裂・$H^1$ 消滅・$\iota$ 錨づけ($H=H_d$ の厳密形)は使っていない** — したがって $\mathrm{GT}(N)=\mathfrak F_0\rtimes Q$ の分裂も、$-1$ が $\widetilde\chi$ 像にあることも不要である。

**証明.** 巡回群の部分群は位数で決まるので $H\cap\mathfrak F_0$ は $d$ で決まり、$\bigcap_i(H_i\cap\mathfrak F_0)$ は位数 $\gcd$ の部分群。$\widetilde\chi(H)\supseteq\widetilde\chi(\mathrm{GT}_{\rm arith})=Q_N$ かつ $\bigcap H_i\supseteq\mathrm{GT}_{\rm arith}$ ゆえ交叉でも像は $\supseteq Q_N$。位数は第一同型定理。∎

> **効き所**: $N_{\rm S4}$($\mathrm{PSL}(2,8)$ 窓)は $\mathfrak F_0\cong C_9$ で**巡回**(ihnec §6.1 の窓データ)。⟹ **壁窓側にも会計が立つ**。ただし $Q_{N}$ の充満性(補題 CHI の類似)は窓ごとに証明書が要る(【DIV-GAP-3】)。

---

## 5. ★ パリティ罠($\varepsilon$ = $C_2$ 因子)— **裁定 209 型への警戒**

発案係の札 E は捻れ類を $[\kappa]\in H^1\bigl((\mathbb Z/2n)^\times,\ C_n/C_d\bigr)$ と書いた。**群としては $(\mathbb Z/2n)^\times\cong(\mathbb Z/n)^\times$ であり $H^1$ の値は変わらない**(下記 (b))が、**$\widetilde\chi$ の水準を $(\mathbb Z/2n)^\times$ と読むと定理の骨格が壊れる**。名指しする。

| # | 罠 | 正しい扱い |
|---|---|---|
| **P-1** | **$\widetilde\chi$ の水準**。$\widetilde\chi$ が well-defined になる**最細の水準は $2M=4n$** であり $(\mathbb Z/2n)^\times$ ではない。$\varphi(2n)=\varphi(n)$ に対し $\varphi(4n)=2\varphi(n)$ — **ちょうど因子 2 のずれ** | 常に $(\mathbb Z/4n)^\times\cong(\mathbb Z/n)^\times\times C_2$ で書く。工房の正本は `kerchi_equality_v2.md` T-A(1)・`w2arith_v1.md` 補題 L(「$\bmod\ 2n$ での一致は (W2) より真に弱い・核は位数 2 = chirality $\mathcal Z_2$」) |
| **P-2** | **「$d=n\Rightarrow H=T$」が偽になる**。$\varepsilon$ 成分を落として $\lvert H\rvert=d\varphi(n)$ と数えると、$d=n$ から $H=T$ を結論してしまう | **反例(明示)**: $H^{\rm bad}:=\mathrm{Aff}(\mathbb Z/n)\times\{0\}=\{(k,u,0)\}$ は部分群で $H^{\rm bad}\cap\mathfrak F_0=\mathfrak F_0$(**$d=n$**)だが $[T:H^{\rm bad}]=2$。**$d=n$ でも全体ではない。** ⟹ 「全 genuine $\iff d=n$」は **(CHI) を $(\mathbb Z/4n)^\times$ で要求して初めて正しい** |
| **P-3** | **pin がこの罠を殺す**($\iota$ の $\varepsilon$ は 1) | $\iota=(0,-1,1)\notin H^{\rm bad}$。⟹ **(PIN) を課せば $\varepsilon$ 成分の充満性は自動**。$\widetilde\chi(\iota)=-1$ の $(\mathbb Z/4)^\times$ 成分が非自明であることが効く。**(CHI) が要るのは $u$ 成分だけ**と言い換えてよい |
| **P-4** | **$m$ の水準**(ihnec T-4 の再掲) | $m\in\mathbb Z/2n$ であって $\mathbb Z/n$ ではない。$\varepsilon=m\bmod2$ が well-defined なのは $K^{(n)}_{\rm ord}=2n$ が偶であるため(**奇 $n$ でのみ**) |

**(b) $H^1$ の値は変わらないことの確認**(過剰訂正の防止): $Q=(\mathbb Z/n)^\times\times C_2$ で $C_2$ は $A$ に自明作用・$\lvert C_2\rvert=2$ は $\lvert A\rvert=e$(奇)と互いに素だから、inflation-restriction で $H^1(Q,A)\cong H^1(Q/C_2,A^{C_2})=H^1\bigl((\mathbb Z/n)^\times,A\bigr)$。**どちらで書いても $0$**(§4.1 (c) はそもそも $z$ の存在しか使っていないので両方を同時にカバーしている)。⟹ **札 E の $H^1$ 表記は結果として正しい。壊れるのは位数勘定の側だけ**である。

> **★ 教訓(裁定 209 型)**: 「同型な群だから同じ」と「同じ水準だから同じ」を混同しない。$(\mathbb Z/2n)^\times\cong(\mathbb Z/n)^\times$ は**抽象群としての同型**であり、$\widetilde\chi$ の**像として**は $(\mathbb Z/4n)^\times$ が正しい。**パリティ枝($\varepsilon\in\{0,1\}$)を落とすと因子 2 が消える** — これは裁定 209 の恒久チェック項目と同型の事故である。§10.2 検査 (D) が $n=3,7,9,15,21$ で $H^{\rm bad}$ を実際に構成して確認した。

---

## 6. ★ 換算表 — **部分証拠の会計**

### 6.1 会計の場は「約数束」であって「実数の不等式」ではない

定理 DIV-LAW により未知量は
$$d_{\rm arith}(n)\ \mid\ d_{\rm gen}(n)\ \mid\ n$$
という**約数の連鎖**に整理された(系 DIV-LAT)。したがって部分証拠は**すべて整除の言明**として書かれねばならない。

> ⚠ **「$\mathrm{ord}\ge n/p$」という不等式形の言明は使わない**(札 E の例示はこの形だった)。$d\mid n$ の下で「$d\ge n/p$」が意味を持つのは $d$ が $n/p$ の**倍数**であるときだけであり、正しい入力の型は
> $$\ell\mid d\qquad(\ell\ \text{は既知の約数})$$
> である。$\ell=n/p$($p\mid n$ 素数)のとき、$\ell\mid d\mid n$ から $d\in\{n/p,\ n\}$ が従い、**そのときに限り**「$d\ge n/p$」と読んでよい。

### 6.2 換算表(**入力 → $d$ への効き → fake の居場所**)

| # | 入力(証拠) | 型 | $d_{\rm arith}$ への効き | $d_{\rm gen}$ への効き | **fake の居場所** |
|---|---|---|---|---|---|
| **L1** | $\ell\mid\mathrm{ord}(a_n)$(算術的下界) | 整除・**framework-conditional**(系 DIV-ARITH) | $\ell\mid d_{\rm arith}$ | $\ell\mid d_{\rm gen}$ ⟹ $H_\ell\subseteq\mathrm{GT}_{\rm gen}$ | fake $\subseteq T\setminus H_\ell=\{k\not\equiv0\ (\mathrm{mod}\ n/\ell)\}$。**剰余類の個数 $\le n/\ell-1$**・shadow 数 $\le(n-\ell)2\varphi(n)$ |
| **L2** | $\ell=n/p$($p\mid n$ 素数)で L1 | 同上 | $d_{\rm arith}\in\{n/p,n\}$ | $d_{\rm gen}\in\{n/p,n\}$ | **fake は空、またはちょうど $p-1$ 個の剰余類**($=(1-1/p)\lvert T\rvert$ 個の shadow)。判定は $k\bmod p$ |
| **L3** | $\mathrm{ord}(a_n)=n$(ASM 鎖の枠組み昇格が供給する形) | 整除・同上 | $d_{\rm arith}=n$ | $d_{\rm gen}=n$ | ★ **fake は無い**(かつ odd Conj 5.1 が窓 $n$ で成立 — genuine 性は**系として落ちてくる**) |
| **U1** | ある isolated 細分 $N$ で $\mathrm{Im}\,R_{N,K^{(n)}}\ne T$ の実測 | 有限計算・**cross-checked 可** | — | $d_{\rm gen}\mid d_N<n$ | genuine $\subseteq\{k\equiv0\ (\mathrm{mod}\ n/d_N)\}$。**fake witness が具体的に出る**($k\not\equiv0$ の全元) |
| **U2** | $\lvert\mathrm{Im}\,R_{N,K^{(n)}}\rvert$ の測定値 | 有限計算 | — | $d_N=\lvert\mathrm{Im}\rvert/(2\varphi(n))$ | 測定値は **$\{2d\varphi(n):d\mid n\}$ のいずれか**でなければならない(**反証可能**・§7.4 P-DIV-1) |
| **X1** | L1 と U1 が $\ell\nmid d_N$ で衝突 | — | — | — | ★ **前件のどれかが偽**。DIV-LAW・(AR)・$R^{\rm cyc}_{\rm formal}$ の前件・測定のいずれかの反証(`proof/record consistency failure`) |
| **X2** | L1 と U1 が $\ell=d_N$ で一致 | — | — | $d_{\rm gen}=\ell$ **確定** | fake の集合が**完全に決定される** |

**会計の要約(1 行)**: $\ \boxed{\ \mathrm{lcm}(\text{全ての下界}\ \ell)\ \mid\ d_{\rm gen}\ \mid\ \gcd(\text{全ての上界}\ d_N)\ }$ — 区間が 1 点に潰れたとき $d_{\rm gen}$ が決まる。

### 6.3 具体例(**値は主張しない・型だけ**)

| 窓 | 約数 | 会計の形 |
|---|---|---|
| **$n=q$ 素数** | $\{1,q\}$ | $d_{\rm gen}\in\{1,q\}$ — **genuine 判定は 1 ビット**。$\mathrm{GT}_{\rm gen}(K^{(q)})$ は $T$ か $H_1=Q^{\rm std}$(位数 $2\varphi(q)$)のいずれか。降下は高々 1 回 |
| **$n=7$、右枝** | $\{1,7\}$ | 右枝 $\Rightarrow\mathrm{ord}(a_7)\ne7$、$7$ 素数ゆえ $\mathrm{ord}(a_7)=1\Rightarrow d_{\rm arith}(7)=1$、$\mathrm{GT}_{\rm arith}(K^{(7)})=H_1$(位数 $2\varphi(7)=12$)。$\lvert T\rvert=84$ ゆえ**非算術 shadow は $84-12=72$ 個**。そのうち genuine なものが在る $\iff d_{\rm gen}(7)=7$(**このとき 72 個すべてが非算術証人**)。ihnec 系 FK-Q7 の「窓 1 つの genuine 性」= **この 1 ビット** |
| **$n=9$** | $\{1,3,9\}$ | 下界 $3\mid\mathrm{ord}(a_9)$ の経路がある(塔関係 (6.3-cls)・**T63-P1 = 予測**・E1 ノート §5.5)。**これが入れば** $d_{\rm gen}(9)\in\{3,9\}$ ⟹ **$K^{(9)}$ の fake は(在るなら)全て $k\not\equiv0\ (\mathrm{mod}\ 3)$**($108$ 個中 $72$ 個の側)。降下は高々 2 回 |
| **$n=21$** | $\{1,3,7,21\}$ | 上界側 CASC(左枝)は $\mathrm{ord}(a_m)\mid m$ しか出さない ⟹ **$d$ の上界にはならない**(§6.4 注意) |
| **$n=p^2$** | $\{1,p,p^2\}$ | 降下は高々 2 回。中間段 $H_p$ が唯一の真の中間 |

### 6.4 会計の禁止事項(**混同すると崩れる 4 点**)

1. **★ 有限深度の PASS から $d_{\rm gen}=n$ を導かない**(工房の掟 2)。表の U1/U2 は**上界**しか与えない。「有限個の $N$ で全射だった」は $d_{\rm gen}$ について**何も**言わない。**下界は算術層(L1–L3)からしか来ない** — DIV-LAW はこの非対称性を消していない、**逆に見えるようにした**。
2. **CASC / 補題 C′ の「上界 $\mathrm{ord}(a_m)\mid m$」は本表の上界ではない**。それは $d_{\rm arith}\mid n$ の再確認であって、$d_{\rm gen}$ の上界(表 U1)とは別物である。**上界という語が二つの意味で使われている**(E1 ノート §5.1 の「上界/下界」は $\mathrm{ord}(a_n)$ の内側の話)。
3. **fake(正典 Def 4.2 = 非 genuine)と非算術を混ぜない**(裁定 374・ihnec 追補 A.1)。本表で $d_{\rm gen}$ が支配するのは **fake**、$d_{\rm arith}$ が支配するのは**非算術**。両者の差 $H_{d_{\rm gen}}\setminus H_{d_{\rm arith}}$ が **非算術証人(旧「B 型」)** である:
 $$\boxed{\ \textbf{窓 }n\textbf{ に非算術証人が存在}\iff d_{\rm arith}(n)<d_{\rm gen}(n)\ },\qquad\text{その個数}=(d_{\rm gen}-d_{\rm arith})\cdot2\varphi(n).$$
4. **$\Omega(n)$ は「降下の回数」であって「停留する $N$ の深さ」ではない**(§7.2)。

---

## 7. 【IHNEC-GAP-1】の帰結の明文化 — **優先度の組み替え**

### 7.1 GAP の原文と、本稿が変えたこと

ihnec 【IHNEC-GAP-1】原文(要旨): 「ML-ODD (ii) は各 $(N,n)$ については有限計算だが $N$ の量化は無限。停留は保証されるが**どの $N$ で停留するかの上界を与える装置が無い**。要る型: 明示的 $N_0$、あるいは有限個の $N$ で停留を保証する構造的理由。」

| | GAP-1 が求めていたもの | 本稿が置いたもの |
|---|---|---|
| 未知量の型 | $T$ の**部分群**($\lvert T\rvert=2n\varphi(n)$ の部分群束の中の 1 点) | ★ **約数 $d_{\rm gen}\mid n$** ただ 1 個($\tau(n)$ 通り)。しかも $H_{d}$ と**明示的に書ける** |
| 停留の保証 | Mittag-Leffler の有効版が要る(【文献要請 IHNEC-L1】) | ★ **降下は高々 $\Omega(n)$ 回**(系 DIV-GEN(5))— 有効版の**「回数」の側は自前で閉じた** |
| 停留の場所 | 明示的 $N_0$ | ✗ **与えていない**(【DIV-GAP-1】) |
| 下界の供給 | (GAP-1 の視野外) | ★ $d_{\rm arith}\mid d_{\rm gen}$ により**算術層がそのまま下界供給器**になる(§6.2 L1–L3) |

> ### ★ 結論(札 E の主張の正形)
> $$\boxed{\ \textbf{【IHNEC-GAP-1】は「停留上界の新定理」を要求していない。要求されているのは }d_{\rm gen}\textbf{ の下界であり、それは }d_{\rm arith}\textbf{ の下界と同一の仕事である。}\ }$$
> したがって **ASM 鎖($\mathrm{ord}([u_n]_{2n})=n$)の枠組み昇格 + 橋 $B_{\rm FC}$ の閉鎖**という **P1 の最優先タスクが、そのまま IHNEC-GAP-1 の実効解**である。**「停留深度の上界」を別立ての課題として抱える必要はない。**

### 7.2 ★ ただし GAP-1 は**解消していない**(正直な形)

- **$\Omega(n)$ 上界は「回数」の上界であって「深さ」の上界ではない**。$\Omega(n)$ 回の降下が**どの $N$ で起きるか**は依然 UNKNOWN であり、有限個の $N$ を走らせて「$d_{\rm gen}=n$」を**証明する**ことはできない。(COR54) の壁は不変。
- ゆえに **DIV-LAW は決定手続きを与えていない**(ihnec §4.4 の記述と同じ限界)。変わったのは**未知量の大きさ**(部分群束 → 約数 $\tau(n)$ 通り)と**証拠の会計法**である。
- **【DIV-GAP-1】** $d_{\rm gen}(n)$ の値は全ての奇 $n$ で **UNKNOWN**。

### 7.3 帰結の再配置(**司令塔への提案** — 裁定事項)

| # | 提案 | 根拠 |
|---|---|---|
| **R-1** | 【文献要請 IHNEC-L1】の**「その先(停留の深さの上界)」の項を臨界路から外す** | §7.1。回数側は自前で閉じ、場所側は下界供給で迂回できる |
| **R-2** | **(MCOV) 破れ走査(ihnec 追補 D.1.5 項 3)を、標的が奇 dihedral 窓である限り取り下げる** | 系 DIV-SPLIT(証明つき・空であることが確定) |
| **R-3** | **札 D(entangled 屋根)の実測目標を「$d_N<n$ を出す細分の構成」と言い換える** | 系 DIV-GEN(1):どんな屋根でも像は $H_{d_N}$。**測るべきは 1 個の約数**であって群の構造ではない ⟹ 測定コストが下がる(位数だけで足りる・§7.4 P-DIV-3) |
| **R-4** | **素数窓($q=7$ 等)の genuine 判定を「1 ビット測定」として登録** | 系 DIV-GEN(5)。ihnec 系 FK-Q7 の「窓 1 つの genuine 性」がこの 1 ビットと同一であることが確定した |

### 7.4 事前登録予言(**実測前に凍結** — 反証可能性の確保)

| # | 予言 | 根拠 | 反証の意味 |
|---|---|---|---|
| **P-DIV-1** | **任意の** isolated 細分 $N\subseteq K^{(n)}$ について $\lvert\mathrm{Im}\,R_{N,K^{(n)}}\rvert\in\{2d\varphi(n):d\mid n\}$。$n=9$ なら $\{12,36,108\}$、$n=7$ なら $\{12,84\}$ | 系 DIV-GEN(1) | 他の値が出れば DIV-LAW か (AR) か (HOM) か測定が偽 |
| **P-DIV-2** | その像は**必ず** $\{k\equiv0\ (\mathrm{mod}\ n/d)\}$ の形($u,\varepsilon$ に非依存) | 定理 DIV-LAW (3) | $u$ や $\varepsilon$ に依存する像が出れば偽 |
| **P-DIV-3** | 像は**常に $\iota=[-1,1]$ を含む** | 補題 PIN-A/系 PIN-gen | 含まない像が出れば補題 PIN-A の braid 恒等式か実装が偽(**安価な健全性検査**) |
| **P-DIV-4** | **分裂屋根**($PB_3/M\cong G_n\times PB_3/N'$)では**必ず全射** | 系 DIV-SPLIT | 非全射が出れば (AR) 経路か SPLIT-NULL が偽 |
| **P-DIV-5** | $n=9$ で下界 $3\mid\mathrm{ord}(a_9)$ が確定すれば、$K^{(9)}$ の fake は(在るなら)**全て $k\not\equiv0\ (\mathrm{mod}\ 3)$** | §6.3 | fake witness が $k\equiv0\ (3)$ で出れば下界か DIV-LAW が偽 |

> **⚠ P-DIV-1〜4 は「何も出ない」ことを予言している**(較正型)。**当たっても fake の非存在の証拠にはならない**(工房の掟 2)。値打ちは**反証可能性**の側にある。

---

## 8. 前件表(**FAM-U-ASM 方式**)

### 8.1 最短鎖(**この 7 段以外は前件ではない**)

| 段 | 内容 | 使う前件 |
|---|---|---|
| **(D0)** | $\Theta_n$ 座標: $T\cong\mathfrak F_0\rtimes Q^{\rm std}$、$\mathfrak F_0\cong C_n$、$Q$ の作用は乗法 | **(E1-1)(THM43)(E1-S1)** |
| **(D1)** | $\widetilde\chi$ の水準は $4n$、$\ker\widetilde\chi=\mathfrak F_0$ | **(W2)-fam / T-A(1)(3)**(`kerchi_equality_v2.md`) |
| **(D2)** | **補題 PIN-A**: $\iota=[-1,1]\in\mathrm{GT}(N)$($\forall N$)・$R$-整合 | **本稿の初等証明**(braid 恒等式・(3.3)(3.4)) |
| **(D3)** | **系 PIN-gen**: $\iota$ は genuine・全ての $\mathrm{Im}\,R$ に属す | (D2)+**(COR54)** |
| **(D4)** | **補題 CHI**: $\widetilde\chi(\mathrm{GT}_{\rm arith})=(\mathbb Z/4n)^\times$ | **(AR)**+(E1-1)(= (S2)/W2-arith Route A) |
| **(D5)** | **定理 DIV-LAW**: (CHI)+(PIN) ⟹ $H=H_d$ | (D0)(D2)(D4)+**$H^1=0$ の 3 行**(本稿) |
| **(D6)** | $\mathrm{Im}\,R_{N,K^{(n)}}$ は部分群で $\mathrm{GT}_{\rm arith}$ を含む ⟹ $=H_{d_N}$ | **(HOM)(ARG)(COR54)** |
| **(D7)** | $\mathrm{GT}_{\rm gen}=\bigcap=H_{\gcd d_N}$・降下 $\le\Omega(n)$ | (D5)(D6)+**(INT)**(isolated への制限) |

**終点 = 系 DIV-GEN(3)(4)(5)。鎖は 8 段。$d_{\rm arith}=\mathrm{ord}(a_n)$(換算表の入力側)は鎖の外**(§8.2 の (RCYC) 行)。

### 8.2 前件表(**落とすと何が壊れるか**)

| 札 | 言明 | 格 | 出所 | **落とすと壊れるもの** |
|---|---|---|---|---|
| **(E1-1)** | $K^{(n)}$ は isolated | **正典の定理** | 2405 Lemma 4.2/Thm 4.3 | $T$ が群でなくなり (D0) 以降**全部**が消える |
| **(THM43)** | (4.12) の明示形 | **正典の定理** | 2405 Thm 4.3 | $\Theta_n$ の構成が消える |
| **(E1-S1)** | $\Theta_n$ が**群**同型 | **工房 paper-proof**;$n=9$ で 11,664 対 cross-check | E1 ノート §2.1・裁定 379 | $\mathfrak F_0\cong C_n$ と乗法作用が消え、**巡回性(= 除数で決まること)が消える** ⟹ 定理の骨格が崩壊 |
| **(HOM)** | isolated 間の $R$ は準同型 | **正典の定理** | 2401 Remark 3.16 | $\mathrm{Im}\,R$ が部分群でなくなり (D6) が消える(**部分集合の減少族としての停留は残るが、除数法則は消える**) |
| **(COR54)** | genuine $\iff$ 全細分に survive | **正典の定理**(証明鎖は Prop 3.15 経由 — 対話帳 T-24) | 2401 Cor 5.4 | (D3)(D7) が消える。$\mathrm{GT}_{\rm gen}$ と $\bigcap\mathrm{Im}\,R$ の同一視が失われる |
| **(INT)** | isolated $\cap$ isolated $=$ isolated | **正典 Prop 3.15**(★ **原論文に証明が無い** — ihnec 追補 B.2 の自前証明で代替) | 2401 Prop 3.15 | (D7) の「isolated に制限してよい」が消える。**(COF) が落ちても ML-ODD は生きる**(対話帳 T-24)が **(INT) は落ちてはいけない** |
| **(AR)** | $\mathrm{Ih}(g)=(\frac{\chi(g)-1}2,f_g)$・$\chi$ 全射 | **正典 + Kronecker–Weber** | 2405 (1.5) | **補題 CHI が消える** ⟹ (CHI) が仮定に戻り、$H$ の位数勘定と「$d=n\iff H=T$」が消える。**本稿唯一の算術的入力** |
| **(LS-CC)** | 複素共役 $\mapsto(-1,1)$ | **正典引用**(Lochak–Schneps [20, Thm 1]) | 2405 §1「elementary tools」(ii) | **$\mathrm{GT}_{\rm arith}$ の厳密標準形だけ**が消える(系 DIV-ARITH)。**$\mathrm{GT}_{\rm gen}$ 側は無傷**(系 PIN-gen が代替) |
| **(ARG)** | arithmetical $\Rightarrow$ genuine | **正典** | 2405 §1.3 | (D6) の「$\mathrm{GT}_{\rm arith}\subseteq\mathrm{Im}\,R$」が消え、補題 CHI が $\mathrm{Im}\,R$ へ渡らない |
| **(RCYC)** | $d_{\rm arith}=\mathrm{ord}(a_n)$ | ★ **framework-conditional**(前件 (0)(1)(2)(3)(5′)(6′);**(5′) = 比較橋 $B_{\rm FC}$ = 【GAP-Rcyc】は UNKNOWN**) | `week4-K3飽和_opus_v3.md` §5.2.2 段 2 | **換算表の入力側だけ**が消える(§6.2 L 行)。**DIV-LAW 本体・系 DIV-GEN は無傷** |
| **(ASM)** | $\mathrm{ord}([u_n]_{2n})=n$ | ★ **candidate**(枠組み仮定 TB1–TB4・BFC・GR 相対;**domain = 奇 $n\ge3,\ n\ne5$**) | `fam_u_assembly_v1.md` §1・§V.2 | L3 行が消える(L1/L2 の部分下界は残りうる) |

### 8.3 **除外欄**(= 前件では**ない**もの・混ぜないこと)

| 除外するもの | 理由 |
|---|---|
| **(LIM)**(2401 Thm 5.2) | 使わない。系 PIN-gen は (COR54) だけで出る(§2.2) |
| **(THM44)**($\mathrm{Dih}$ 内 reduction 全射) | 使わない。本稿は $K^{(n)}$ **単独**の内部構造しか見ない |
| **定理 E1-2 / E1-3 / E1-4** | 使わない。中間峰の極限も同値定理も本稿の鎖に現れない |
| **(U-10)**($\widehat{GT}=\widehat{GT}_{\rm gen}$) | 使わない。**FAKE-KILL′ へ渡すときに初めて要る**(ihnec (A7)) |
| **定理 SPLIT-NULL / (MCOV)** | **本体の前件ではない**。系 DIV-SPLIT(§4.5)で**逆に供給する側**に回る |
| **(CPT)**(有向極限の非空性) | 使わない($T$ は有限・交叉は有限個で足りる) |
| **CASC / 補題 C′ / $q=7$ の 1 ビット** | 換算表の**入力例**としてしか現れない。本体には不要 |
| **$K^{(5)}$ 関連の一切** | 封印(冒頭) |

### 8.4 矢印表(**距離の図** — 一本矢印にしない)

| 矢印 | 内容 | 格 |
|---|---|---|
| **(a)** | $\mathrm{GT}_{\rm arith}\subseteq H\le T$ なる $H$ は $H_d$ 型 | ★ **本稿の定理**(前件 = (E1-1)(THM43)(E1-S1)(AR)(LS-CC) or PIN-gen)。**算術的入力は (AR) のみ** |
| **(b)** | $d_{\rm gen}=\gcd_N d_N$・降下 $\le\Omega(n)$ | ★ **本稿の系**(+(HOM)(COR54)(INT)) |
| **(c)** | $d_{\rm arith}=\mathrm{ord}(a_n)$ | ★ **framework-conditional**($B_{\rm FC}$ = UNKNOWN) |
| **(d)** | $\mathrm{ord}(a_n)=n$(全奇 $n\ne5$) | ★ **candidate**(ASM 鎖・枠組み相対) |
| **(e)** | $d_{\rm gen}(n)$ の値 | ★ **UNKNOWN**(全ての奇 $n$) |

$$\mathrm{GT}(K^{(n)})\ \xrightarrow[\textbf{(a) 定理}]{\ \Theta_n,\ \widetilde\chi\ }\ \{H_d\}_{d\mid n}\ \xleftarrow[\textbf{(b) 系}]{\ \bigcap\mathrm{Im}\,R\ }\ d_{\rm gen}\ \xleftarrow[\textbf{(c) 枠組み}]{\ d_{\rm arith}\mid d_{\rm gen}\ }\ \mathrm{ord}(a_n)\ \xleftarrow[\textbf{(d) candidate}]{\ \text{ASM 鎖}\ }\ n$$

**禁止(FAM-U-ASM §V.5.2 の規律を継承)**: **矢印を跨いだ主張をしない**。とくに **(a)(b) の theorem 格を (c)(d) の証拠に使わない**、また **(d) の candidate 格で (e) を埋めない**。

### 8.5 罠(§5 のパリティ罠に加えて)

| # | 罠 | 正しい扱い |
|---|---|---|
| **T-a** | **$\mathrm{Im}\,R$ が部分群であることに $N$ の isolated 性が要る** | 非 isolated $N$ には (HOM) が効かない。ML-ODD の (INT) 経由で isolated に制限してから使う |
| **T-b** | **$\Omega(n)$ を「深さ」と読む** | §7.2。**回数**の上界であって**場所**の上界ではない |
| **T-c** | **$d$ を実数の不等式で扱う** | §6.1。入力の型は整除 $\ell\mid d$ |
| **T-d** | **(S4-ISO) 型の前件**(壁窓の isolated 性) | 一般窓形 DIV-LAW$^{\rm gen}$(§4.6)を壁窓に使うときは isolated 性が**機械測定のみ**であることを明記(ihnec T-5) |
| **T-e** | **fake / 非算術の二義** | 裁定 374。§6.4 項 3 の分離を守る |

---

## 9. 【DIV-GAP】一覧・申し送り

| 札 | 内容 | 状態 |
|---|---|---|
| **【DIV-GAP-1】** | $d_{\rm gen}(n)$ の**値**。本稿は型を決めただけで、どの奇 $n$ についても値を決めない | **UNKNOWN**(全奇 $n$) |
| **【DIV-GAP-2】** | $d_{\rm arith}=\mathrm{ord}(a_n)$ の橋(= 比較橋 $B_{\rm FC}$ = 【GAP-Rcyc】) | **UNKNOWN**(既知の GAP の再掲・本稿は新設しない) |
| **【DIV-GAP-3】** | $\mathfrak F_0$ が**非巡回**の窓への拡張。$\mathfrak F_0$ の $Q$-部分加群の束が約数束を置き換えるが、**$H^1$ の消滅は保証されない**(§4.1 (c) は $\lvert A\rvert$ 奇 + $-1\in$ 作用に依存)。また補題 CHI の類似($Q_N$ の充満性)は窓ごとの証明書が要る | **未着手**(型は書ける) |
| **【DIV-GAP-4】** | **$d_{\rm gen}=n$ を有限計算で証明する手続きは無い**。(COR54) の壁は DIV-LAW でも破れない | **原理的**(掟 2) |

### 申し送り(司令塔へ)

1. **格の食い違い(要裁定)**: (S2) = W2-arith を ihnec §6.4 は「framework-conditional」、`w2arith_v1.md` は「閉鎖・二経路(Route A は正典引用)」と記帳している。**本稿は Route A を採って paper-proof と記帳した**。どちらの記帳が正本か裁定を請う(本稿の補題 CHI・系 DIV-SPLIT・換算表の格がこれに連動する)。
2. **R-1〜R-4(§7.3)の採否**。とくに **R-2(MCOV 破れ走査の取り下げ)は工数削減**であり、**R-3(札 D の測定目標の言い換え)は測定コストを下げる**。
3. **ihnec への追補としての位置づけ**: 本稿は ihnec 追補 D.1.5 の項 1・項 3 と、【IHNEC-GAP-1】の記述に**直接干渉する**。ihnec 本文は不改変(erratum 方式)とし、本稿を参照先とするか、ihnec に追補 E を立てるかは司令塔の判断。
4. **Sol 監査点の推奨**: ①§4.1 (c) の $H^1=0$(3 行の初等証明)②補題 PIN-A の braid 恒等式(2 行)③系 DIV-SPLIT が便 98 F98-3.7 の判定と衝突していないこと ④§5 のパリティ罠の扱い ⑤系 DIV-ARITH が $R^{\rm cyc}_{\rm formal}$ 証明段 2 の**正しい抽出**であること。
5. **対話帳 T-25 の系 GEN9-$\Lambda$ との関係**(§4.3 の注)を Sol へ同時に提示すること(T-25 は便 99 の監査点として既出)。

---

## 10. 格付け・検算・出所・新規性の申告

### 10.1 格付け表

| 主張 | 格 |
|---|---|
| **補題 PIN-A**($\iota\in\mathrm{GT}(N)$ 全窓・$R$ 整合) | **proof(初等・$N$ 一様)**。braid 恒等式 2 行。証明書 `K9.v1.json` と $N_5$ control で実物確認 |
| **系 PIN-gen**($\iota$ genuine) | **proof**((COR54) 相対) |
| **補題 PIN-B**(算術 pin) | **正典引用**((LS-CC)) |
| **補題 CHI** | **proof**((AR)+(E1-1) 相対)= 工房 (S2) の再掲。**格の食い違いあり(§9-1)** |
| **定理 DIV-LAW**(§4.1) | ★ **paper-proof candidate**(単系統・Sol 未監査)。$n\in\{3,7,9,15,21\}$ で**完全列挙による機械確認**(§10.2 (C)) |
| **系 DIV-LAT / DIV-GEN / DIV-COSET** | **paper-proof candidate**(同上) |
| **系 DIV-ARITH** | **paper-proof candidate**。後半($=\mathrm{ord}(a_n)$)は **framework-conditional** |
| **系 DIV-CHI-NULL / DIV-SPLIT** | **paper-proof candidate**。(AR) 相対 |
| **定理 DIV-LAW$^{\rm gen}$**(§4.6) | **paper-proof candidate**(窓ごとに $Q_N$ 充満性の証明書が要る) |
| **換算表(§6)/ 予言(§7.4)** | **設計・会計規約**(定理ではない) |
| Lean 検証 | ✗ **していない**。§7.4 の予言も cross-checked でもない |

### 10.2 検算(**証明とは独立・整数演算のみ・単系統**)

**script**: `search/probe/wac_v1/divlaw_check.py`(SHA-256 `b7553814eb3aa348eb9d9f9dbc38bf09cdcb440fae0aa5ead1e63ca90ba12e07`)。**failures 0 / ALL PASS**。

| # | 検査 | 範囲 | 結果 |
|---|---|---|---|
| **(A)** | $\Theta_n$ 群公理・$\widetilde\chi$ 準同型・$\ker=\mathfrak F_0\cong C_n$・共役作用 $=u$ 倍・$\iota^2=1$・$\widetilde\chi(\iota)=(-1,1)$ | $n=3,7,9,11,15,21,25,27,33,45$ | PASS |
| **(B)** | $H_d$ が部分群・$\lvert H_d\rvert=2d\varphi(n)$・$H_d\cap H_{d'}=H_{\gcd}$・**左剰余類 $=k\bmod(n/d)$ の fiber** | $n=3,7,9,15,21,25,27,45$ 全約数対 | PASS |
| **(C)** | ★ **分類定理**: $\widetilde\chi$ 全像の部分群を**完全列挙**し、①個数 $=\sigma(n)$ ②各々 $H_d$ の $\mathfrak F_0$-共役 ③$\iota$ を含むものはちょうど $\{H_d\}_{d\mid n}$ | $n=3,7,9,15,21$(実測 $4,8,13,24,32=\sigma(n)$) | PASS |
| **(C′)** | (C) の列挙が漏れていないことを**全部分群の総当たり**で独立確認 | $n=3$(16 部分群)・$n=9$(98 部分群) | PASS |
| **(D)** | **パリティ罠**: $H^{\rm bad}=\mathrm{Aff}(\mathbb Z/n)\times\{0\}$ が $d=n$ かつ $[T:H^{\rm bad}]=2$・$\iota\notin H^{\rm bad}$・$\varphi(2n)=\varphi(n)$ vs $\varphi(4n)=2\varphi(n)$ | $n=3,7,9,15,21$ | PASS |
| **(E)** | $H^1(Q,\mathbb Z/e)=0$ を **$Z^1$ 全列挙 $=B^1$** で直接確認・$\lvert B^1\rvert=e$ | $n=3,7,9,15$ の全 $d\mid n$ | PASS |
| **(F)** | 最長真減少約数鎖 $=\Omega(n)$ | $n$ 9 個($1155$ まで) | PASS |
| **(G)** | **証明書 `K9.v1.json`**: $\Theta_9$ 単射(108 点)・$\iota=[17,1]$ が index 1 に実在・$\Theta_9(\iota)=(0,8,1)$・合成表で $\iota^2=$ 単位元・$H_1,H_3,H_9$ が**合成表の上で**部分群かつ $\widetilde\chi$ 全像 | $n=9$ | PASS |
| **(H)** | 補題 PIN-A の braid 恒等式を **Burau 表現**(乱択 $t$・8 回)で cross-check($c\ne1$ を確認した上で) | — | PASS |
| **(I)** | **$N_5$ control**($c$ の位数 5)で $f=1$ の charming GT-pair が $\{0,1,3,4\}$、$m=-1\equiv4$ を含む | — | PASS |

> **格の正確な形**: 単系統(python)であり **cross-checked ではない**。(G) のみ GAP 由来の証明書を入力にしている(証明書の生成は GAP 単系統)。**Lean 検証ではない。**
> **封印**: 全検査で $n=5$ を除外。

### 10.3 出所と新規性の申告(**grep 済**)

**出所**:
- §1 記法・$\Theta_n$: E1 ノート §2.1(命題 E1-S1)・ihnec §1・`kerchi_equality_v2.md` §2(T-A)・`w2arith_v1.md` 補題 L。
- §2 補題 PIN: **本稿**(braid 恒等式)。(LS-CC) は 2405 §1 の引用(`docs/notes/2405.11725-抽出ノート_v1.md` §「elementary tools」(ii))。
- §3 補題 CHI: `w2arith_v1.md`(裁定 122)・`kerchi_equality_v2.md` T-A(4′)・E1 ノート (S2)。
- §4: **本稿**。位数勘定 (1) は E1 ノート §5.1 の **(S4)** と同型(算術層版)。
- §6 換算表: **本稿**。入力側の出所は E1 ノート §5.1・§5.5(上界/下界)・`fam_u_assembly_v1.md`(ASM 鎖)・`week4-K3飽和_opus_v3.md` §5.2.2(段 2)。
- §7: ihnec §4.4【IHNEC-GAP-1】・追補 D.1.5・裁定 394 の札 E 要旨。

**新規性の申告(grep 済 — `DIV-LAW` / `除数法則` / `H_d` / `約数束` / `安定像の分類` を `docs/` `provenance/` `sol/` 全文検索)**:

| 項目 | 既出か | 正確な差分 |
|---|---|---|
| $\lvert A\rvert=\lvert A\cap\mathfrak F_0\rvert\cdot\lvert\widetilde\chi(A)\rvert$ の勘定 | ★ **既出**(E1 ノート §5.1 (S4)・`kerchi` T-A(5)) | **算術層 $A=\mathrm{GT}_{\rm arith}$ についてのみ既出**。本稿は同じ勘定を **$\mathrm{GT}_{\rm gen}$ と $\mathrm{Im}\,R_{N,K^{(n)}}$ へ移した**(そのために補題 CHI と (ARG) が要る) |
| 「$\mathrm{Im}\,R$ は部分群の減少有向族で必ず停留」 | ★ **既出**(ihnec 系 ML-A) | 本稿は**停留値の形**($H_d$)と**降下回数**($\le\Omega(n)$)を決めた |
| $\mathrm{GT}_{\rm gen}(K^{(9)})$ の指数 $\in\{1,3,9\}$ | ★ **既出**(対話帳 **T-25** 系 GEN9-$\Lambda$・$n=9$ のみ・$\Lambda=\ker(\to\mathrm{GT}(K^{(3)}))$ 経由) | 本稿は **全奇 $n$** へ一般化し、**部分群そのものを特定**($H_d$・$k$ の合同式)。経路も別($\Lambda$ を使わない) |
| $\iota=[-1,1]$ が全窓の shadow | **部分的に既出**(2405 が複素共役として使用・E1 ノート FINDING $\Phi$1 が $m=2n-1$ を名指し・証明書 `K9.v1.json` に実在) | 「**全ての $N$ で GT-shadow・$R$ 整合・ゆえに genuine**」という**窓横断の補題としての定式化**は工房内に発見できなかった(grep 済) |
| 捻れ類 $[\kappa]\in H^1$ の分類と**その消滅** | **発見できず**(札 E が枠を提示・計算は無し) | 本稿が $H^1=0$ を証明し、**分類が約数 1 個に潰れる**ことを示した |
| 「genuine 判定 $=k$ の合同式 1 本」 | **発見できず** | 本稿 |
| 「分裂屋根は常に全射((MCOV) 自動)」 | **半分既出**(ihnec 追補 D.1.2 の供給経路①が (S2) から (MCOV) を出す形で書かれている) | 本稿は**①が常に発火する**ことを一般に示し、**(MCOV) 破れ走査が空**という帰結を出した |
| 【IHNEC-GAP-1】の「下界供給への組み替え」 | **札 E が提示**(裁定 394) | 本稿は**その正形**(§7.1 の boxed)と**限界**(§7.2)を確定した |

**外部文献**: 使用なし。群論的入力は「巡回群の部分群は位数で決まる」「可換正規部分群の補群は $H^1$ で分類」「位数互いに素なら $H^1=0$」のみ(すべて標準)。**【文献要請】は本稿からは出さない**(§7.3 R-1 はむしろ既存の要請の取り下げ提案)。

---

## 付録 A. 記号早見

| 記号 | 意味 |
|---|---|
| $T=\mathrm{GT}(K^{(n)})$ | 奇窓の shadow 群($\lvert T\rvert=2n\varphi(n)$) |
| $\Theta_n=(k,u,\varepsilon)$ | 自然座標(命題 E1-S1)。$u=2m+1\bmod n$、$\varepsilon=m\bmod2$ |
| $\widetilde\chi$ | $[m,f]\mapsto2m+1\bmod4n$。$\Theta$ では $(k,u,\varepsilon)\mapsto(u,\varepsilon)$ |
| $\mathfrak F_0$ | $\ker\widetilde\chi=\{(k,1,0)\}\cong C_n$ |
| $Q^{\rm std}$ | $\{(0,u,\varepsilon)\}=H_1$(位数 $2\varphi(n)$) |
| $H_d$ | $\{(k,u,\varepsilon):k\equiv0\ (\mathrm{mod}\ n/d)\}$、$d\mid n$ |
| $\iota$ | $[-1,1]$、$\Theta_n(\iota)=(0,-1,1)$(複素共役の像) |
| $d_{\rm arith},d_{\rm gen},d_N$ | 各層の $\mathfrak F_0$ との交叉の位数 |
| $\Omega(n)$ | $n$ の素因子数(重複込み) |
