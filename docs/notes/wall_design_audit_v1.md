# 壁キャンペーン共同設計の監査 — Sol 便 78 §1 と宇宙 v1.2

**状態札: candidate(裁定前・未 commit)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-29
監査対象: `sol/sol_reply_78_math5.md` §1(札 B・(a)A1/A2/A3・(d)D1・(e))および
`provenance/registered/universe_wall_v1.md` v1.2 の該当条項。
**W-Exist(発案札 A)は委嘱により対象外**(別途検証中)。§2 数学検分・§3 手続きゲートも対象外。

正典・依拠:
- `docs/week1-定義ノート.md` §1(基礎対象)・§1.5(語規約 W-1〜W-4)・§2(groupoid GTSh・(3.3)(3.4)・charming・Def 3.7・Prop 3.6・(3.53)(3.54)・settled/isolated)・§3(dihedral poset)
- `docs/notes/kerchi_equality_v1.md`(T-A/T-B/補題 P/TIER-1.5)
- 外部文献: **Dyer–Grossman(Out(B₃) ≅ C₂)にのみ言及**。§6 で「correctness には不要」と分離した(正典内で閉じる形に書き換え済み)。

> ### 封印遵守
> $u$(封印記号)および封印 3 量に一切触れていない。本稿は有限群論と $B_3$ の初等的事実のみ。
> 本稿で記号 $u$ が現れる箇所はすべて **$u := 2m+1$(GT-pair の指数)**であり、Sol 便 78 の記法をそのまま踏襲したものである(封印記号とは別物・混同禁止)。

---

## 0. 判定表

| # | 監査対象 | 判定 | 一行要旨 |
|---|---|---|---|
| **1** | 札 B(isotropy 型修理) | **修正付き CONFIRM** | 型違反の指摘は正しい。処方に**全射性条項の欠落 1 件**。$K$ の計算は well-defined、しかも Sol の想定より**安く**できる(§1.4)。**無料の個数等式**を追加(§1.5) |
| **2a** | (W1) 候補数の床 | **CONFIRM** | $f\in[P_N,P_N]$ は charming の**定義そのもの**(2401 Def・pentagon の有限側の影)。**閉形式 $c_m(N)=\varphi(2N_{\rm ord})$** を確定(GAP 検算) |
| **2b** | (W2)(W3) 指数 $<48$ 消去 | **CONFIRM(ただし著しく弱い)** | 正しいが鈍い。Sol 自身の「$\widetilde\chi$ 像可換」論法を A1 に適用すると **(W2′) $\lvert[P_N,P_N]\rvert<60\Rightarrow$ 可解**、**(W3′) 非可解には指数 $\ge360$** が出る。**band W-A(指数 $\le192$・66 窓)は全窓が理論可解確定** |
| **3** | A2 の $H_N$ sieve | **CONFIRM(論理は厳密)+ コスト批判** | 論理鎖(C2F との合わせ技)は穴なし。ただし $H_N$ の構成コストは候補数そのもの ⟹「hexagon 前の安価な sieve」は誇張。**$H_N\subseteq N_{\rm Aut(A)}(\langle\bar x\rangle)$** という無料の上群、および $\ker\Theta$ の構造式を追加(§3.3–3.4) |
| **4** | A3(nilpotent 除外) | **CONFIRM(穴なし)+ 無条件化** | Burnside basis の適用条件に問題なし。**ただし「$\ker\Theta$ 可解ゲート」も「$\Theta$ 忠実」も不要** — 両結論は無条件に強められる(§4.3) |
| **5** | (d) D1 congruence 族 | **CONFIRM(全 5 主張)+ 予備計算で族の結末を予言** | CRT は正当(環の CRT + $SL_2(\mathbf Z)\twoheadrightarrow SL_2(\mathbf Z/n)$)。$p=5,7$ の完全列挙(予備計算): $\lvert GT(N_p)\rvert=2p(p-1)$、**isolated**、$GT(N_p)\cong C_2\times\mathrm{Aff}(\mathbf F_p)$、**metabelian**。**$\Theta_N$ 忠実性の明示反例**でもある |
| **6** | (e) 対称簡約 | **修正付き CONFIRM** | transport の**明示式 $[m,f]\mapsto[m,\iota(f)]$** を確定。$\iota$ 非内部は初等証明可(文献不要)。**修正**: 証明書に書くべきは $\iota(K)$ との一致。**実効性ゼロの警告**: $K^{(n)}$ も $N_p$ も $\iota$-固定 |
| **補完** | §7 | — | **Hol 篩**(Sol の A2/A3 を包含し、$E,\mathrm{Aut}(E),\Theta$,C2F をすべて不要にする)+ **標的選定の必要条件**+ kerchi との統合 |

---

## 1. 札 B — isotropy 型修理

### 1.1 主張は正しい(CONFIRM)

**命題 1.1.** $N$ が isolated でないとき、$GT(N)$ 上に (3.53) は群構造を定めない。群対象は $G_N:=GTSh(N,N)$ である。

**証明.** 定義ノート §2 より $[m,f]\in GTSh(K,N)$ は「source $K$ → target $N$」の射(= $T_{m,f}:B_3\twoheadrightarrow B_3/N$、$\ker T_{m,f}=K$)。(3.53) を写像の合成と照合すると
$$T_{m_1,f_1}\circ T_{m_2,f_2}:\ \sigma_1\mapsto\sigma_1^{u_1u_2},\quad
\sigma_2\mapsto\bigl(f_1E_{m_1,f_1}(f_2)\bigr)^{-1}\sigma_2^{u_1u_2}\bigl(f_1E_{m_1,f_1}(f_2)\bigr)$$
($u_i=2m_i+1$。$(3.49)$ が第一成分、$E$ の準同型性が第二成分を与える)。すなわち **(3.53) は「$[m_2,f_2]$ を先に適用する」通常の合成**であり、定義されるのは
$$\mathrm{source}([m_1,f_1])=\mathrm{target}([m_2,f_2])=N$$
のとき、つまり $[m_1,f_1]$ が settled のときに限る。

さらに well-definedness も壊れる。$E_{m_1,f_1}(f_2)$ が $N_{F_2}$ を法として確定するには $f_2$ が **$K_{1,F_2}$ を法として**与えられていなければならない($E_{m_1,f_1}(K_{1,F_2})\subseteq N_{F_2}$ は $\ker T_{m_1,f_1}=K_1$ から従うが、$E_{m_1,f_1}(N_{F_2})\subseteq N_{F_2}$ は一般に**偽**)。$GT(N)$ は $f_2$ を $N_{F_2}$ を法としてしか保持しないので、$K_1\ne N$ の項では表そのものが定義できない。∎

$G_N=GTSh(N,N)$ が群であることは groupoid の頂点群として自動(単位 $[0,1]$、逆元 (3.54))。**Sol の型判定は正しい。**

### 1.2 【修正 1・blocker 級】処方 1 に全射性条項が欠けている

Sol の手順は「① charming pair と full hexagon を列挙 → ② source kernel を証明書化 → ③ $K=N$ のみ残す」。
しかし GT-shadow の定義(Def 3.7)は **charming GT-pair + 全射性**である(定義ノート §2)。全射性を落とすと:

- $T_{m,f}$ の像が真部分群になり得て $[B_3:K]<[B_3:N]$、
- したがって「$N\subseteq K\Rightarrow K=N$」という指数勘定が使えず、②③ の判定が破れる。

**修正**: 手順 ① を「charming pair + full hexagon + **全射性(Prop 3.6 によりどの版で判定してもよい)**」とすること。宇宙 v1.2 §「群対象の型」の①も同様に修正が要る。

### 1.3 $K$ は類 $[m,f]$ の関数として well-defined(CONFIRM)

**補題 1.3.** $T_{m,f}$ は $(m\bmod N_{\rm ord},\ fN_{F_2})$ にのみ依存する。ゆえに $K=\ker T_{m,f}$ も類の関数。

**証明.** (i) $f\mapsto fh$、$h\in N_{F_2}\subseteq N$: $(fh)^{-1}\sigma_2^{u}(fh)N=h^{-1}(f^{-1}\sigma_2^uf)hN$。$N\trianglelefteq B_3$ ゆえ任意の $w$ に対し $w^{-1}h^{-1}w\in N$、したがって $h^{-1}whN=wN$。
(ii) $m\mapsto m+N_{\rm ord}$: $\sigma_1^{2(m+N_{\rm ord})+1}=\sigma_1^{2m+1}x^{N_{\rm ord}}$ で $x^{N_{\rm ord}}\in N$($\mathrm{ord}(xN)\mid N_{\rm ord}$)。$\sigma_2$ 側も同様。∎

### 1.4 【安価化】source kernel を $B_3$ の部分群として計算する必要はない

**補題 1.4(settled の実装可能判定).** $[m,f]$ を **GT-shadow**(全射性込み)とする。$E:=B_3/N$、$\pi:B_3\to E$ とすると
$$\text{settled}\iff N\subseteq\ker T_{m,f}\iff
\exists\,\alpha\in\mathrm{End}(E):\ \alpha(\pi\sigma_1)=\pi(\sigma_1^{u}),\ \alpha(\pi\sigma_2)=\pi(f^{-1}\sigma_2^{u}f).$$
右辺が成り立てば全射性から $\alpha\in\mathrm{Aut}(E)$、$[B_3:\ker T]=[B_3:N]$ で $K=N$。

**実装**: GAP では `GroupHomomorphismByImages(E,E,[s1,s2],[s1^u, f^-1*s2^u*f]) <> fail` の一行。
$B_3$ の Schreier 生成系や剰余類表を作る必要がない。**§5 の予備計算はこの形で実行し、$p=5,7$ で全 shadow の source kernel を確定した。**

証明書の欄としては `source_kernel_id` の代わりに(あるいは併記で)
`settled_witness = {generator_images, extends_to_endomorphism: true/false}` を置けば、独立レーンが同じ判定を再現できる。

### 1.5 【補完・無料の fail-closed assert】source-kernel は torsor 構造をもつ

**命題 1.5.** $GTSh(K,N)\ne\emptyset$ なら $GTSh(K,N)$ は $G_N$ の**左 torsor**である($g\cdot[b]:=g\circ[b]$)。ゆえに
$$\boxed{\ \lvert GT(N)\rvert=\lvert G_N\rvert\cdot\#\{K:\ GTSh(K,N)\ne\emptyset\}\ }$$
特に $\lvert G_N\rvert$ は $\lvert GT(N)\rvert$ を割り、source kernel の相異なる個数は $\lvert GT(N)\rvert/\lvert G_N\rvert$ に等しい。

**証明.** $[a],[b]\in GTSh(K,N)$ に対し $[b]^{-1}\in GTSh(N,K)$、$[a]\circ[b]^{-1}\in GTSh(N,N)=G_N$(合成可能性は source/target が一致)。作用は自由かつ推移的。∎

**用途**: source-kernel 証明書群の整合性を**追加コストゼロ**で検査できる(列挙した source の異なり数 × $\lvert G_N\rvert$ が $\lvert GT(N)\rvert$ に一致しなければ、その窓の列挙は壊れている)。isolated 窓では自明($\#=1$)だが、非 isolated 窓ではこれが唯一の安価な整合性検査になる。

### 1.6 【修正 2】$\iota$-transport 後の source-kernel(§6 参照)

Sol (e) の実装規約「transport 後の source-kernel **一致**」は、正しくは **$\iota(K)$ との一致**である(§6.4)。

---

## 2. (a) A1 — 理論の床

### 2.1 (W1) は charming の定義だけから出る(CONFIRM)

**「$f\in[P_N,P_N]$ の根拠は正典のどの条項か」への回答**: **charming の定義そのもの**である。
定義ノート §2:「**charming**: $2m+1$ が $(\mathbf Z/N_{\rm ord})^\times$ の元を代表 **かつ** $fN_{F_2}\in[F_2/N_{F_2},F_2/N_{F_2}]$」(2401 Def 3.x)。
同 §2「gentle の意味」:「gentle 版 $\widehat{GT}_{\rm gen}$ は pentagon をその帰結 $\hat f\in[\widehat F_2,\widehat F_2]^{\rm cl}$ に置換(**= 有限側では charming 条件**)」。
すなわち **(W1) は導出された不等式ではなく、GT-shadow の定義域を数えただけ**である。hexagon も全射性も使っていない。Sol の「charming 条件だけから」は正確。

$$\lvert G_N\rvert\le\lvert GT(N)\rvert\le\#\{m\}\cdot\#\{f\}=c_m(N)\cdot\lvert[P_N,P_N]\rvert.\tag{W1}$$

### 2.2 【補完】$c_m(N)$ の閉形式

**補題 2.2.** $M:=N_{\rm ord}$ とすると $\;c_m(N)=\#\{m\in\mathbf Z/M:\gcd(2m+1,M)=1\}=\varphi(2M)$。

**証明.** $M$ 奇: $m\mapsto 2m+1$ は $\mathbf Z/M$ の全単射、$c_m=\varphi(M)=\varphi(2M)$。
$M$ 偶: $2m+1\equiv2m'+1\ (M)\iff m\equiv m'\ (M/2)$ ゆえ $2$ 対 $1$ で奇剰余($M/2$ 個)を覆う。$M$ 偶のとき単元はすべて奇なので単元の個数は $\varphi(M)$、よって $c_m=2\varphi(M)=\varphi(2M)$。∎
**GAP 検算**: $M\in[1,200]$ で不一致ゼロ(`floors.g`)。

**帰結(kerchi との接続)**: $Q:=(\mathbf Z/2M)^\times$ は kerchi ノート T-A の $\mathrm{Im}\widetilde\chi_{2M}$ の受け皿であり、$\lvert Q\rvert=\varphi(2M)=c_m(N)$。したがって (W1) は
$$\lvert G_N\rvert=\lvert\mathrm{Im}\widetilde\chi\rvert\cdot\lvert\mathfrak F_0\rvert
\le \underbrace{\varphi(2M)}_{\text{像の床}}\cdot\underbrace{\lvert[P_N,P_N]\rvert}_{\text{核の床}}$$
という**像・核の分解そのもの**である。**しかも像側は (AR) の下で等号**(T-A(4))。したがって (W1) の情報はすべて核側 $\lvert\mathfrak F_0\rvert\le\lvert[P_N,P_N]\rvert$ に集約される。

### 2.3 (W2) は正しいが、より強い版に置き換えるべき

**命題 2.3 (W2′).** $\;\lvert[P_N,P_N]\rvert<60\ \Longrightarrow\ G_N$ は可解。

**証明.** $\widetilde\chi_{2M}:G_N\to(\mathbf Z/2M)^\times$ は準同型で像は可換(T-A(1)(2)、純群論・(AR) 不要)。核 $\mathfrak F_0=\{[0,f]\in G_N\}$(T-A(3))は写像 $[0,f]\mapsto f$ で $[P_N,P_N]$ へ**単射**(charming)。よって $\lvert\mathfrak F_0\rvert<60$、位数 $<60$ の群は可解、$G_N/\mathfrak F_0$ 可換 ⟹ $G_N$ 可解。∎

$c_m\ge1$ ゆえ Sol の (W2)「$c_m\lvert[P',P']\rvert<60$」は (W2′) に**真に含まれる**($c_m$ 倍だけ弱い)。
**(W2′) は $c_m$ を掛けないぶん、$N_{\rm ord}$ が大きい窓で効きが変わる。**

### 2.4 (W3) は正しいが鈍い — (W3′) に置き換え

Sol の (W3): $N_{\rm ord}\le\lvert A_N\rvert$、$\lvert[P_N,P_N]\rvert\le\lvert A_N\rvert$ より $\lvert A_N\rvert^2\ge60$、$[B_3:N]=6\lvert A_N\rvert\ge48$。**各ステップは正しい**($P_N=F_2/(N\cap F_2)\hookrightarrow PB_3/N=A_N$、$N_{\rm ord}\mid\exp(A_N)$)。

しかし (W2′) を通すと格段に鋭くなる。

> ### 命題 2.4 (W3′ — 理論の床の改訂)
> 1. $G_N$ が**非可解**なら $\lvert[P_N,P_N]\rvert\ge60$、ゆえに $\lvert P_N\rvert\ge60$、ゆえに
> $$\boxed{\ [B_3:N]\ \ge\ 360\ }$$
> 2. $G_N$ が**非 metabelian** なら $\lvert[P_N,P_N]\rvert\ge6$、ゆえに $\lvert P_N\rvert\ge14$、ゆえに
> $$\boxed{\ [B_3:N]\ \ge\ 84\ }$$

**証明.** (1) 非可解 ⟹ $\mathfrak F_0$ 非可解(§2.3)⟹ $\lvert\mathfrak F_0\rvert\ge60$ ⟹ $\lvert[P_N,P_N]\rvert\ge60$。$P_N$ は **2 生成有限群**($=F_2/N_{F_2}$)で $\lvert P'\rvert\ge60$ を満たす最小位数は $60$($A_5$)。$\lvert P_N\rvert\le\lvert A_N\rvert=[B_3:N]/6$。
(2) 非 metabelian ⟹ $G_N''\ne1$ ⟹ $G_N'$ 非可換。$G_N'\subseteq\mathfrak F_0$ ⟹ $\mathfrak F_0$ 非可換 ⟹ $\lvert\mathfrak F_0\rvert\ge6$ ⟹ $\lvert[P_N,P_N]\rvert\ge6$。2 生成有限群で $\lvert P'\rvert\ge6$ の最小位数は $14$(位数 14 の二面体群、$P'\cong C_7$)。∎
**GAP 検算**(`floors.g`): 2 生成有限群の最小位数 — $\lvert G'\rvert\ge6$ で **14(GAP 名 `D14`= 位数 14)**、$G'$ 非可換で **24(`SL(2,3)`、$G'=Q_8$)**、$\lvert G'\rvert\ge60$ および $G'$ 非可解で **60(`A5`)**。

### 2.5 【重要な帰結】band W-A は掃引前に全窓決着する

宇宙 v1.2 の band W-A は指数 $\le192$、$PB_3$ 内 **66 本**(`search/certs/wall_probe_20260728.json` stage 192)。

- $[B_3:N]\le192\Rightarrow\lvert A_N\rvert\le32\Rightarrow\lvert[P_N,P_N]\rvert\le32<60$
  ⟹ **66 窓すべてが可解確定**(計算不要・(W2′) の即決)。
- 指数 $<84$ の窓は **20 本**(66 − 46)。これらは **metabelian も理論確定**(命題 2.4(2))。
- 残る **46 本**(指数 $84\!-\!192$)だけが「非 metabelian か?」の計算対象。

**したがって v1.2 の記述「理論消去: 指数 < 48 は (W3) により可解確定」は
「非可解性については band W-A 全体が理論消去済み。非 metabelian の計算対象は指数 $\ge84$ の 46 窓のみ」
に改めるべきである。** band W-A の位置づけは「探索帯」から **「較正帯 + metabelian 悉皆帯」** へ変わる。

**Sol の漏れの型**: Sol は発案札 A(W-Exist)の証明で「$\widetilde\chi$ の像は可換 ⟹ 核が可解なら全体が可解」を**自分で使っている**。同じ一行を A1 に適用すれば (W3′) が出る。**同一便の中で使った補題を別節に適用し忘れた**型の漏れである。

---

## 3. A2 — C2F と Aut overgroup による sieve

### 3.1 論理鎖は厳密(CONFIRM)

**命題 3.1.** $\psi:G_N\xrightarrow{\Theta_N}\mathrm{Aut}_\pi(E)\xrightarrow{\mathrm{res}}\mathrm{Aut}(A)$ とすると
$$1\to\ker\Theta_N\to\ker\psi\to Z^1(Q,Z(A))\ (\text{可換}),\qquad
G_N/\ker\psi\cong\psi(G_N)\subseteq H_N.$$
ゆえに $\ker\Theta_N$ 可解 $\wedge$ $H_N$ 可解 $\Longrightarrow G_N$ 可解。

**検証した各点**:
1. $\psi$ の像が power-form であること: $T(x)=T(\sigma_1^2)=\sigma_1^{2u}=x^u$、$T(y)=(f^{-1}\sigma_2^uf)^2=f^{-1}y^uf$、$T(c)=c^u$ ✓(定義ノート §2 Prop 3.2)。
2. $\Theta_N$ が $\mathrm{Aut}_\pi(E)$ に落ちること: $u$ は奇なので $T(\sigma_i)PB_3=\sigma_iPB_3$、すなわち **$T$ は $Q=S_3$ 上恒等**(Sol の「$Q$ を保つ」より強い)。この強い形が C2F の適用条件($A$ 上・$Q$ 上ともに恒等)をちょうど満たす ✓。$N\le PB_3$ より $A=\ker(E\to Q)$ ✓。
3. $K_{\rm aut}\cong Z^1(Q,Z(A))$ が**可換**であること: $z_{\alpha\beta}=z_\beta\cdot z_\alpha$(反準同型)だが $Z^1$ は値が $Z(A)$ で pointwise 積ゆえ可換、群同型 ✓。
4. $\psi(G_N)$ は $\mathrm{Aut}(A)$ の**部分群**で、生成部分群 $H_N$ に含まれる ✓。

**「合わせ技の厳密性」への回答: 穴なし。** ただし Sol の本文は 2. と 3. を明示していないので、v1.2 に条項として書くべきである(特に「$Q$ 上恒等」を落とすと C2F が使えない)。

### 3.2 【コスト批判】$H_N$ は「hexagon 前の安価な sieve」ではない

$H_N$ の生成系を得るには、$u$(admissible)$\times f\in[P_N,P_N]$ のすべてについて
「$x\mapsto x^u,\ y\mapsto f^{-1}y^uf,\ c\mapsto c^u$ が $A$ の自己同型に延びるか」を判定する。
これは **(W1) の候補数 $c_m\cdot\lvert[P_N,P_N]\rvert$ と同じ規模**の作業である。
実測(§5): $p=5$ で 400 個、$p=7$ で 1176 個の写像構成。

節約されるのは hexagon **評価**($c\notin N$ 窓では語レベル評価)だけであり、
Stage 0 の欄として「安価」と書くのは不正確。**v1.2 §Stage 0 の文言を「候補数と同オーダー」と正直に書くこと。**

### 3.3 【補完・無料の上群】$H_N\subseteq N_{\mathrm{Aut}(A)}(\langle\bar x\rangle)\cap N_{\mathrm{Aut}(A)}(\langle\bar c\rangle)$

**命題 3.3.** charming($\gcd(u,N_{\rm ord})=1$)と $\mathrm{ord}(\bar x)\mid N_{\rm ord}$ から $\langle\bar x^u\rangle=\langle\bar x\rangle$。ゆえに
すべての power-form 自己同型は $\langle\bar x\rangle$ と $\langle\bar c\rangle$ を正規化する。
とくに **$N_{\mathrm{Aut}(A)}(\langle\bar x\rangle)$ が可解なら $H_N$ は可解**(列挙不要・正規化群 1 回)。

**効果**: これだけで D1 族(§5)が落ちる — $A=SL_2(\mathbf F_p)$、$\bar x$ は unipotent、その正規化群は Borel(可解)。
**実測一致**: $\lvert H_N\rvert=p(p-1)=\lvert\text{Borel}\rvert$($p=5$: 20、$p=7$: 42)。

### 3.4 【補完】$\ker\Theta_N$ の構造(Sol は「計算せよ」としか書いていない)

**命題 3.4.**
1. $\Theta_N([m,f])=\mathrm{id}$ なら $u\equiv1\ (\bmod\ N_{\rm ord})$。ゆえに $\ker\Theta_N\subseteq\ker\chi_{\rm vir}$ で、$[\ker\chi_{\rm vir}:\mathfrak F_0]\le2$。
2. $\ker\Theta_N\cap\mathfrak F_0\hookrightarrow C_E(\sigma_2N)\cap[P_N,P_N]$ は**群の単射準同型**($[0,f]\mapsto f$)。
3. ゆえに **$C_E(\sigma_2N)$ が可解なら $\ker\Theta_N$ は可解**(中心化群 1 回)。

**証明.** (1) $T(x)=x^u=x$、$T(c)=c^u=c$、$\mathrm{ord}(yN)=\mathrm{ord}(xN)$($x,y$ は $\Delta$ で共役)ゆえ $u\equiv1$ mod $\mathrm{lcm}=N_{\rm ord}$。$\ker\bigl((\mathbf Z/2M)^\times\to(\mathbf Z/M)^\times\bigr)$ の位数 $\le2$。
(2) $\Theta([0,f])=\mathrm{id}$ ⟹ $E_{0,f}$ は $P_N$ 上恒等 ⟹ (3.53) が $[0,f_1][0,f_2]=[0,f_1f_2]$ に退化。像の条件は $f^{-1}\sigma_2f=\sigma_2$ in $E$。∎

**実測**($p=5$): $\lvert\ker\Theta_N\rvert=2$、$m$-値は $\{0,p\}$ — (1) の「$\mathfrak F_0$ の外に高々指数 2」と一致 ✓。$\lvert C_E(\sigma_2N)\rvert=20$ 可解 ✓。

---

## 4. A3 — nilpotent 除外

### 4.1 「$p$ 群 ⟹ $A/\Phi(A)$ 上 scalar ⟹ $H_N$ 可解」— 穴なし(CONFIRM)

**検証**:
- $A=PB_3/N=\langle\bar x,\bar y,\bar c\rangle$ ✓($PB_3=\langle x,y,c\rangle$)。
- $\Phi(A)\supseteq[A,A]$ ゆえ $A/\Phi(A)$ は可換、共役は消え、生成元 3 個がすべて $v\mapsto v^u$。可換群で $v\mapsto v^u$ は自己準同型なので **$\bar\alpha$ は全体で scalar $u$** ✓。
- **Burnside basis theorem の適用条件**: 「$A$ 有限 $p$ 群 ⟹ $\ker(\mathrm{Aut}(A)\to\mathrm{Aut}(A/\Phi(A)))$ は $p$ 群」— $A$ が有限 $p$ 群であること以外の仮定は不要。本件は満たされる ✓。**穴なし。**
- ゆえに $H_N$ は($p$ 群)-by-(scalar 部分群 $\subseteq\mathbf F_p^\times$ 巡回)で可解 ✓。$p=2$ でも scalar 像が自明になるだけで結論不変 ✓。
- 有限 nilpotent $A=\prod A_p$: $A_p$ は characteristic、$\mathrm{Aut}(A)\hookrightarrow\prod\mathrm{Aut}(A_p)$、power-form は各 $A_p$ 上でも power-form($A_p=\langle\bar x_p,\bar y_p,\bar c_p\rangle$)✓。

### 4.2 「class-2 + $\Theta$ 忠実 ⟹ metabelian」— 正しい(CONFIRM)

$\widetilde\chi=1$ の元では $u\equiv1\ (N_{\rm ord})$ ⟹ $x^u=x,y^u=y,c^u=c$ ✓。$f\in[P_N,P_N]\subseteq Z(P_N)$(class $\le2$)で $y\in P_N$ ゆえ $f^{-1}yf=y$ ✓。よって $\psi(\ker\widetilde\chi)=1$、$\Theta$ 忠実なら $\ker\widetilde\chi\hookrightarrow Z^1(S_3,Z(A))$ 可換 ⟹ $G_N$ metabelian ✓。

**細部の注記**: Sol は「$A$ が class 2」と書くが、使っているのは **$P_N$ が class $\le2$** である。両者は実は同値 — $A=P_N\langle\bar c\rangle$ で $\bar c\in Z(A)$ なので $\gamma_k(A)=\gamma_k(P_N)$($k\ge2$)。誤りではないが、条項としては $P_N$ で書くほうが掃引に直結する($P_N$ は掃引が持つ量)。

### 4.3 【強化・無条件化】両結論から仮定を落とせる

§7 の Hol 篩(命題 7.1)を使うと、A3 の**両方の仮定が不要**になる。

> **命題 4.3(A3 の無条件版).**
> 1. **$P_N$ が nilpotent なら $G_N$ は可解**($\ker\Theta$ 可解ゲート**不要**)。
> 2. **$P_N$ が class $\le2$ なら $\mathfrak F_0$ は $[P_N,P_N]$ の部分群と同型で、$G_N$ は metabelian**($\Theta$ 忠実性**不要**)。

**証明.** 命題 7.1 により $\mathfrak F_0$ は $K.U'$($K\hookrightarrow[P_N,P_N]\cap C_{P_N}(\bar y)$、$U'\subseteq U$)。
(1) $P_N$ nilpotent ⟹ $K$ は nilpotent ⟹ 可解。$U$ の元 $\alpha$ は $\bar x\mapsto\bar x$、$\bar y\mapsto f^{-1}\bar yf$ で、$P_N/\Phi(P_N)$ 上では**両生成元に恒等**($[P,P]\subseteq\Phi$)。したがって $U\subseteq\ker(\mathrm{Aut}(P_N)\to\mathrm{Aut}(P_N/\Phi))$ = nilpotent(Burnside)⟹ 可解。ゆえに $\mathfrak F_0$ 可解、$G_N/\mathfrak F_0$ 可換 ⟹ $G_N$ 可解。
(2) class $\le2$ ⟹ $[P,P]\subseteq Z(P_N)$ ⟹ 全 $f$ で $E_{0,f}=\mathrm{id}_{P_N}$ ⟹ $U'=1$ ⟹ $\mathfrak F_0\cong K\le[P_N,P_N]$ 可換(class 2 ゆえ $[P,P]$ 可換)⟹ $G_N'\subseteq\mathfrak F_0$ 可換 ⟹ metabelian。∎

**さらに一般化**: (2) の仮定は $[P_N,P_N]\subseteq C_{P_N}(\bar y)$ まで弱められる(そのとき $\mathfrak F_0\cong$ $[P_N,P_N]$ の部分群)。

**評価**: A3 の数学は正しいが、**Sol は $E$ と $\mathrm{Aut}(E)$ を経由したために不要な仮定($\ker\Theta$・$\Theta$ 忠実)を背負った**。$P_N$ 内で完結させれば仮定は消える。extraspecial 族の較正族降格という**結論は無条件に正しい**(むしろ強化される)。

---

## 5. (d) D1 — congruence product 族

### 5.1 各主張の判定(すべて CONFIRM)

| 主張 | 判定 | 根拠 |
|---|---|---|
| $B_3\to SL_2(\mathbf Z)$、$\sigma_1\mapsto\begin{psmallmatrix}1&1\\0&1\end{psmallmatrix}$、$\sigma_2\mapsto\begin{psmallmatrix}1&0\\-1&1\end{psmallmatrix}$ | CONFIRM | braid 関係を満たす(GAP 検算)。$\Delta\mapsto\begin{psmallmatrix}0&1\\-1&0\end{psmallmatrix}$、$c=\Delta^2\mapsto-I$ |
| **CRT の正当性** | **CONFIRM** | 「像の独立性」を別途示す必要は**ない**。$\mathbf Z/2p\cong\mathbf Z/2\times\mathbf Z/p$ は**環同型**ゆえ $SL_2(\mathbf Z/2p)\cong SL_2(\mathbf F_2)\times SL_2(\mathbf F_p)$ は群同型。あとは $SL_2(\mathbf Z)\twoheadrightarrow SL_2(\mathbf Z/n)$(標準)と $B_3\twoheadrightarrow SL_2(\mathbf Z)$ を合成するだけ |
| $E_p\cong S_3\times SL_2(\mathbf F_p)$ | CONFIRM | 上記 + $SL_2(\mathbf F_2)\cong S_3$。**GAP 実測 $\lvert E\rvert=720,2016$** |
| $N_p\le PB_3$ | CONFIRM | mod 2 の像は $S_3$ の 3 点作用で $\sigma_1\mapsto(e_2e_3)$、$\sigma_2\mapsto(e_1e_3)$ — 番号付け替えで**標準 $\beta$ そのもの**。ゆえに $\ker\subseteq\ker\beta=PB_3$ |
| $A_p\cong SL_2(\mathbf F_p)$ | CONFIRM | $PB_3$ は全射の下で $\{1\}\times SL_2(\mathbf F_p)$ の原像ゆえ第二因子へ全射。**実測 $\lvert A\rvert=120,336$** |
| $c\mapsto -I$、$c\notin N_p$ | CONFIRM | $c\mapsto(\mathrm{id}_{S_3},-I)$、$p$ 奇ゆえ $-I\ne I$。**実測 $\mathrm{ord}(cN)=2$** |
| 指数 $6p(p^2-1)$ = 720/2016/7920/13104 | CONFIRM | $6\cdot\lvert SL_2(\mathbf F_p)\rvert$。四値とも算術的に正しい |

### 5.2 追加で確定した窓不変量(紙上 + GAP)

$$N_{\rm ord}=\mathrm{lcm}(p,p,2)=2p,\qquad c_m=\varphi(4p)=2(p-1),\qquad
P_N=A_p\cong SL_2(\mathbf F_p),\qquad Z(A)=\{\pm I\}\cong C_2.$$
$E_p$ は**直積**なので $Q=S_3$ の $A$ への作用は自明、ゆえに
$$Z^1(S_3,Z(A))=\mathrm{Hom}(S_3,C_2)\cong C_2\quad\Longrightarrow\quad \text{C2F 核は位数 }\le2 .$$
$\lvert[P_N,P_N]\rvert=p(p^2-1)\ge120\ge60$ ⟹ (W2′) では落ちない ⟹ **理論床は通過**($[B_3:N_p]\ge360$ も $p\ge5$ で成立)。Sol の族選定は**床の観点では正当**。

### 5.3 【予備計算・単系統・非登録】$p=5,7$ の完全列挙

> **⚠ 状態札**: 以下は **GAP 単系統の予備計算**(`search/probe/wall_audit_v1/congp.g`)。
> 登録宇宙の掃引ではない・node 独立レーン未実施・**cross-checked ではない**・verified でもない。
> 委嘱文の「$p=5$ で先に手を動かして予想を立てるのは可」の範囲で実行した。

| 量 | $p=5$ | $p=7$ |
|---|---|---|
| $[B_3:N_p]=\lvert E\rvert$ | 720 | 2016 |
| $\mathrm{ord}(\sigma_1N)$ | **10** $=N_{\rm ord}$ | **14** $=N_{\rm ord}$ |
| 候補 charming pair 数 | $8\times120=960$ | $12\times336=4032$ |
| $\lvert GT(N_p)\rvert$(charming+hexagon+全射) | **40** | **84** |
| settled / 全体 ⟹ **isolated** | **40/40 ✓** | **84/84 ✓** |
| $G_N=GTSh(N,N)$ | $C_2\times(C_5\rtimes C_4)$ | $C_2\times(C_7\rtimes C_6)$ |
| 導来列 | $[40,5,1]$ | $[84,7,1]$ |
| 可解性 / metabelian | 可解・**metabelian** | 可解・**metabelian** |
| $\lvert\mathrm{Im}\widetilde\chi_{2M}\rvert$ / $\varphi(2N_{\rm ord})$ | 8 / 8 ✓**全射** | 12 / 12 ✓**全射** |
| $\lvert\ker\widetilde\chi\rvert$ / T-A(5) 個数等式 | 5 / ✓ | 7 / ✓ |
| $\ker\widetilde\chi=[G,G]$ | ✓ | ✓ |
| $\lvert\ker\Theta_N\rvert$ | **2**($m\in\{0,5\}$) | **2**($m\in\{0,7\}$) |
| $\lvert C_E(\sigma_2N)\rvert$ | 20(可解) | 28(可解) |
| $\lvert H_N\rvert$(Sol A2) | 20(可解) | 42(可解) |
| $\lvert\mathrm{Aut}(A)\rvert$ | 120(**非可解**) | 336(**非可解**) |
| $\lvert U\rvert$(§7 の安価版) | 5(可解) | 7(可解) |

### 5.4 予想と、その理論的説明

> ### 予想 W-C-Pred(**candidate・未証明**)
> すべての奇素数 $p\ge5$ について
> $$GT(N_p)=GTSh(N_p,N_p)\cong C_2\times\mathrm{Aff}(\mathbf F_p)=C_2\times(C_p\rtimes C_{p-1}),\qquad
> \lvert GT(N_p)\rvert=2p(p-1),$$
> $N_p$ は **isolated**、$G_{N_p}$ は **metabelian**、$\ker\widetilde\chi\cong C_p=[G,G]$。

**なぜそうなるかの理論的説明(紙上・確定)**: §3.3 により $\psi(G_N)\subseteq H_N\subseteq N_{\mathrm{Aut}(SL_2(\mathbf F_p))}(\langle\bar x\rangle)$。$\bar x$ は unipotent で $\mathrm{Aut}(SL_2(\mathbf F_p))=PGL_2(\mathbf F_p)$、根部分群の正規化群は **Borel**(位数 $p(p-1)$、可解)。実測 $\lvert H_N\rvert=p(p-1)$ は Borel と一致する。したがって「$A_p$ が非可解・Aut-rich」という選定理由は **GT 側には届かない**。

**kerchi との整合**: $Q=(\mathbf Z/4p)^\times\cong C_2\times C_{p-1}$、$\Lambda^2Q\cong C_2$。$Q$ は $\mathfrak F_0\cong C_p$ に $C_{p-1}$ 経由で忠実に作用するので余不変量 $(\mathfrak F_0)_Q=0$、**T-B(B1) により等号成立** — 実測と一致。

**注**: $GT(K^{(n)})\cong\mathrm{Aff}(\mathbf Z/n_0)\times\mathcal Z_2$(2405 Thm 4.6、$n$ 奇)と**同じ型**である。congruence 族は dihedral 塔と別の窓でありながら **同じ形の答え**を返す。

### 5.5 D1 についての運用判定

**Sol 自身の A2/A3 を発射前に走らせれば、D1 は最優先から落ちる。** これは Sol 自身の D2 の警告
「$PSL_2$ の split/unipotent centralizer・normalizer は可解になりやすいので、単純群名だけで点数を上げず、**実際の $H_N$** で選別する」
が **D1 にそのまま当てはまる**ことを意味する。**発案札(d)D1 と(d)D2 の警告は内部で衝突しており、D2 の側が正しい。**

宇宙 v1.2 の band W-C(720/2016/7920/13104 の 4 窓)は、
**「予言つき較正帯」**(予想 W-C-Pred を掃引が再現するかの検証)として再定義するのが最も価値が高い。
撤回する必要はない — むしろ **予言先行**の good practice の実例になる。

### 5.6 D1 が提供する 3 つの副産物(較正資産)

1. **$\Theta_N$ 忠実性の明示反例**: $\lvert\ker\Theta_N\rvert=2$。Sol の「$\ker\Theta_N=1$ を一般定理にしてはいけない」は**実測で正当化された**。$\Theta$ 忠実を暗黙に使う実装のための negative fixture として登録推奨。
2. **F78-2.2 の仮定 $c\in N$ の必要性の witness**: $\mathrm{ord}(\sigma_1N_p)=2p=N_{\rm ord}\ne2N_{\rm ord}$。定理の反証ではない($c\notin N_p$ ゆえ仮定外)が、**仮定を落として使うと壊れる**ことを示す adversarial fixture。
3. **語規約カナリア**: 判定式の積を逆順にすると **$p=5$ で $40\to24$**(実測。$p=7$ の逆順対照は未実施)。**この族は §1.5.3 の盲点ではない** — 規約バグを検出する。$c\notin N$ 窓の較正族として A1 バッテリーより素直。

---

## 6. (e) 対称簡約

### 6.1 $\sigma_1\leftrightarrow\sigma_2$ が $\Delta$-inner(CONFIRM)

$\Delta=\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2$ より $\Delta\sigma_1=\sigma_2\Delta$、$\Delta\sigma_2=\sigma_1\Delta$。ゆえに $\Delta\sigma_1\Delta^{-1}=\sigma_2$、$\Delta\sigma_2\Delta^{-1}=\sigma_1$ ✓。

### 6.2 $\mathrm{Out}(B_3)\cong C_2$ — 【文献依存を分離せよ】

Sol の主張は Dyer–Grossman(1981, Amer. J. Math. 103)の定理であり、**正典(2401/2405/定義ノート)の外**である。
**ただし対称簡約の correctness には不要**。必要なのは次の 2 点だけで、どちらも初等:

1. **$\iota:\sigma_i\mapsto\sigma_i^{-1}$ は $B_3$ の自己同型で $\iota^2=\mathrm{id}$**:
   $\iota(\sigma_1\sigma_2\sigma_1)=(\sigma_1\sigma_2\sigma_1)^{-1}$、$\iota(\sigma_2\sigma_1\sigma_2)=(\sigma_2\sigma_1\sigma_2)^{-1}$ で braid 関係が保たれる ✓。
2. **$\iota$ は内部でない**: $H_1(B_3)=\mathbf Z$($\sigma_i\mapsto1$)上で $\iota$ は $-1$ 倍、内部自己同型は $H_1$ 上恒等 ✓。
3. **$\iota(PB_3)=PB_3$**: $S_3=B_3/PB_3$ 上で $\sigma_i$ の像は対合ゆえ $\iota$ は $S_3$ 上恒等 ✓。

Dyer–Grossman が支えるのは「**これ以外に外部対称がない**」という**完全性(最適性)の主張**だけである。
**v1.2 は「$\mathrm{Out}(B_3)\cong C_2$ による」ではなく「$\iota\in\mathrm{Aut}(B_3)\setminus\mathrm{Inn}$、$\iota^2=1$ による」と書けば正典内で閉じる。**
完全性を主張したいときのみ文献ゲートを通せばよい(**本稿は文献要請を出さない** — 分離で十分)。

### 6.3 【補完】transport の明示式 — Sol は式を与えていない

> ### 命題 6.3
> $N':=\iota(N)$、$\bar\iota:B_3/N\to B_3/N'$ を誘導同型とする。$T':=\bar\iota\circ T_{m,f}\circ\iota^{-1}$ とおくと
> $$T'=T_{m,\ \iota(f)},\qquad\text{すなわち}\qquad
> \boxed{\ [m,f]\ \longmapsto\ [m,\ \iota(f)]\ }$$
> であり、これは $GTSh(K,N)\xrightarrow{\ \sim\ }GTSh(\iota(K),\iota(N))$ を与える。**$m$ が不変なので $\widetilde\chi$ も $N_{\rm ord}$ も保たれる**。合成と両立する(共役だから)ので $G_N\cong G_{N'}$ の群同型。

**証明.** $\iota(\sigma_1^{-u})=\sigma_1^{u}$ より $T'(\sigma_1)=\bar\iota T(\sigma_1^{-1})=\bar\iota(\sigma_1^{-u}N)=\sigma_1^{u}N'$。
$T'(\sigma_2)=\bar\iota\bigl(T(\sigma_2^{-1})\bigr)=\bar\iota\bigl(f^{-1}\sigma_2^{-u}fN\bigr)=\iota(f)^{-1}\sigma_2^{u}\iota(f)N'$。
$\ker T'=\iota(\ker T)$。charming の保存: $\iota(F_2)=F_2$、$\iota([F_2,F_2])=[F_2,F_2]$、$\iota(N_{F_2})=N'_{F_2}$、$u$ 不変。
hexagon は「$T$ が well-defined 準同型」と同値(Prop 3.2)ゆえ共役で保たれる。$\mathrm{ord}(\iota(x)N')=\mathrm{ord}(x^{-1}N')=\mathrm{ord}(xN)$ 等で $N'_{\rm ord}=N_{\rm ord}$。∎

**Sol の 3 主張はすべて CONFIRM**(isotropy 同型・$\widetilde\chi$ 保存・orbit の大きさ $1$ or $2$)。

### 6.4 【修正 3】証明書の欄

Sol の実装規約「transport 後の **source-kernel 一致**」は、正しくは
**「transport 後の source kernel が $\iota(K)$ に一致すること」**。
$K$ そのものとの一致を検査すると、$\iota$-非固定窓で偽陽性/偽陰性になる。

### 6.5 【警告】transport の $\iota$ は語規約バグの $\iota$ と同一写像

$\iota|_{F_2}$ は $x\mapsto x^{-1},y\mapsto y^{-1}$、すなわち **定義ノート §1.5.2 補題 W1 の $\iota$(語の指数一斉反転)と同じ写像**である。補題 W1 は
$$\mathrm{ev}^{\rm bad}(w)=\mathrm{ev}(\iota(w))^{-1}$$
なので、transport 証明書と規約バグは**同じ形の差分**として現れる。
**規約: transport 欄(`transport_automorphism`)と規約検査欄(`convention_robust`)を同一欄に統合してはならない。** transport を適用した証明書の $f$-word を「規約が逆かもしれない」と誤判定する事故、およびその逆の見逃しが、いずれも起こりうる。

### 6.6 【実効性の実測】主要 2 族はどちらも $\iota$-固定 — 簡約の節約はゼロ

**命題 6.6.**
1. **$\iota(K^{(n)})=K^{(n)}$**(全 $n$)。
2. **$\iota(N_p)=N_p$**(全奇素数 $p$)。

**証明.** (1) $\psi_n\circ\iota$ は $x\mapsto(r^{-1},s,s)$、$y\mapsto(rs,r^{-1},rs)$($(rs)^{-1}=rs$、$sr^{-1}=rs$ を使う)。
$\beta=(\beta_1,\beta_2,\beta_3)\in\mathrm{Aut}(D_n^3)$ を $\beta_1:(r\mapsto r^{-1},s\mapsto r^2s)$、$\beta_2:(r\mapsto r^{-1},s\mapsto s)$、$\beta_3=\mathrm{id}$ と取ると $\psi_n\circ\iota=\beta\circ\psi_n$。ゆえに核が一致。
(2) $\mathrm{diag}(-1,1)\in GL_2$ による共役は $A\mapsto A^{-1}$、$B\mapsto B^{-1}$ を与える($A=\begin{psmallmatrix}1&1\\0&1\end{psmallmatrix}$、$B=\begin{psmallmatrix}1&0\\-1&1\end{psmallmatrix}$)。$S_3$ 因子では $\iota$ は恒等。∎

**帰結**: $\iota$-orbit 簡約が計算量を減らすのは **band W-A / W-B のみ**。band W-C(D1)では節約ゼロ。
v1.2 の「対称簡約」節にこの但し書きを入れないと、band W-C の見積りが楽観になる。

---

## 7. 補完 — 見落とされた設計要素(発案)

### 7.1 【主提案】Hol 篩 — $E$・$\mathrm{Aut}(E)$・$\Theta$・C2F をすべて不要にする

> ### 命題 7.1(Hol 篩)
> $N$ を窓、$G_N=GTSh(N,N)$(**settled が前提** — 札 B)、$P_N=F_2/N_{F_2}=\langle\bar x,\bar y\rangle$ とする。
> $\mathfrak F_0=\ker\widetilde\chi_{2N_{\rm ord}}=\{[0,f]\in G_N\}$ について、
> $$\Xi:\ \mathfrak F_0\longrightarrow\mathrm{Aut}(P_N),\qquad [0,f]\longmapsto E_{0,f}\ \ (\bar x\mapsto\bar x,\ \bar y\mapsto f^{-1}\bar yf)$$
> は**群準同型**であり、
> $$1\to K\to\mathfrak F_0\to U'\to1,\qquad
> K\hookrightarrow[P_N,P_N]\cap C_{P_N}(\bar y),\qquad
> U'\subseteq U:=\{\alpha\in\mathrm{Aut}(P_N):\alpha(\bar x)=\bar x,\ \alpha(\bar y)\in\bar y^{P_N}\}\subseteq\mathrm{Stab}_{\mathrm{Aut}(P_N)}(\bar x).$$
> ゆえに
> $$\boxed{\ \mathrm{dl}(G_N)\ \le\ 1+\mathrm{dl}\bigl(C_{P_N}(\bar y)\bigr)+\mathrm{dl}\bigl(\mathrm{Stab}_{\mathrm{Aut}(P_N)}(\bar x)\bigr)\ }$$
> とくに **$C_{P_N}(\bar y)$ 可解 $\wedge$ $\mathrm{Stab}_{\mathrm{Aut}(P_N)}(\bar x)$ 可解 $\Longrightarrow G_N$ 可解**。

**証明.** settled なので $T_{0,f}$ は $E$ の自己同型で $F_2$ を保ち、$E_{0,f}$ は $P_N$ の自己同型を誘導($E_{0,f}(N_{F_2})\subseteq N\cap F_2=N_{F_2}$、有限ゆえ全単射)。(3.53) は $T$ の合成だから $\Xi$ は準同型。$\ker\Xi=\{[0,f]:f\in C_{P_N}(\bar y)\}$ で、そこでは (3.53) が $[0,f_1][0,f_2]=[0,f_1f_2]$ に退化するので $\ker\Xi\hookrightarrow[P_N,P_N]\cap C_{P_N}(\bar y)$ は群の単射。$G_N/\mathfrak F_0$ は可換(T-A)。∎

**GAP 数値検証**($p=5$、`holsieve.g`): $\Xi$ が準同型であること・全 $E_{0,f}$ が $\mathrm{Aut}(P_N)$ の元であること・$\ker\Xi=1$・$\mathrm{Im}\,\Xi$ の位数 5 $=\lvert\mathrm{Stab}\rvert$・$\lvert C_{P_N}(\bar y)\rvert=10$ をすべて確認。dl 上界 3、実測 dl$(G_N)=2$ ✓。

**Sol の A2/A3 に対する優位**:

| | Sol A2/A3 | Hol 篩 |
|---|---|---|
| 必要な対象 | $E$、$\mathrm{Aut}_\pi(E)$、$\Theta_N$、$Z^1(Q,Z(A))$、$H_N$ | **$P_N$ のみ** |
| 列挙 | $c_m\times\lvert[P,P]\rvert$ 個の写像構成 | **なし**(中心化群 1 回 + 安定化群 1 回) |
| 追加仮定 | $\ker\Theta_N$ 可解 / $\Theta$ 忠実 | **なし** |
| nilpotent の結論 | 可解($\ker\Theta$ ゲート下) | 可解(**無条件**) |
| class 2 の結論 | metabelian($\Theta$ 忠実下) | metabelian(**無条件**) |

**Stage 0 への提案**: v1.2 の Stage 0 採点欄を次の 2 欄で置き換える(既存 7 欄は参考欄に降格可):
`centralizer_y_order/solvable`、`stab_aut_x_order/solvable`。**両方可解なら SOLVABLE 確定(理論)**。

### 7.2 【標的選定の正本】必要条件 — 「Aut-rich」を捨てて「centralizer/stabilizer 非可解」を採れ

命題 7.1 の対偶:

> ### 系 7.2(非可解の必要条件)
> $G_N$ が非可解なら
> $$C_{P_N}(\bar y)\ \text{が非可解}\quad\text{または}\quad \mathrm{Stab}_{\mathrm{Aut}(P_N)}(\bar x)\ \text{が非可解}.$$
> さらに $\mathrm{ord}(\bar x)\le2$ は不可($\mathrm{ord}(\bar x)=1$ なら $P_N=1$;$\mathrm{ord}(\bar x)=2$ なら $\bar y$ も位数 2 で $P_N=\langle\bar x,\bar y\rangle$ は二面体、$[P_N,P_N]$ 巡回、$A$ は metabelian)。ゆえに **$\mathrm{ord}(x\bmod N)\ge3$ が必須**。

これは D1 が「Aut-rich」を満たしながら落ちる理由を説明し、**quotient-first(D2)の選別条件を機械的にする**:

> **設計スペック(band W-D 候補)**: braid 関係を満たす生成対 $(s_1,s_2)$ をもつ有限群 $E$ で、
> $P:=\langle s_1^2,s_2^2\rangle$ が $C_P(s_2^2)$ 非可解 **または** $\mathrm{Stab}_{\mathrm{Aut}(P)}(s_1^2)$ 非可解 となるもの。
> $\lvert P\rvert\ge60$ かつ $\mathrm{ord}(s_1^2)\ge3$ は自動的な下限。

### 7.3 【実現可能性の確認】標的は空ではない

**GAP 検算**(`design.g`): $P=A_{13}=\langle\bar x,\bar y\rangle$、$\bar x=(7\,8\,9\,10\,11\,12\,13)$、$\bar y=(1\,2\,3\,4\,5\,6\,7)$(支持集合が 1 点で重なる 2 つの 7-巡回)。
- $\langle\bar x,\bar y\rangle=A_{13}$ ✓
- $C_P(\bar y)\cong C_7\times A_6$、位数 **2520・非可解** ✓
- $\mathrm{Stab}_{\mathrm{Aut}(A_{13})}(\bar x)=C_{S_{13}}(\bar x)\cong C_7\times S_6$、位数 **5040・非可解** ✓

**したがって系 7.2 の必要条件は充足可能**であり、壁キャンペーンの標的空間は空でない。
一般に $A_n$ で $\bar x,\bar y$ が支持サイズ $s$、$2s\ge n$(生成)かつ $n-s\ge5$($C\supseteq A_{n-s}$ 非可解)を満たせばよく、$n\ge10$ で可能。

**残る困難(UNKNOWN)**: この $P$ を $F_2/N_{F_2}$ として実現する $B_3$-窓($E=\langle s_1,s_2\rangle$、braid 関係、$E\twoheadrightarrow S_3$、$s_i^2\mapsto\bar x,\bar y$)の構成。$\mathrm{ord}(\bar x)=7$ なら $\mathrm{ord}(s_1)=14$ が要る。**これは D2 の逆設計そのもの**であり、本監査では未着手。

### 7.4 kerchi_equality_v1 との統合

1. **$c_m=\varphi(2N_{\rm ord})=\lvert Q\rvert$**(§2.2)により、(W1) は T-A の「像 × 核」分解と**同一の式**である。二つの設計が独立に同じ量に到達したことの確認になる。
2. **T-A(5) の fail-closed assert**(`|ker_chi| * phi(2N_ord) == |GT|`)は Stage 0 に**無料**で入る。D1 予備計算では $p=5,7$ とも成立 ✓ — 新しい窓型での初めての追試。
3. **補題 P**($\lvert\mathfrak F_0\rvert$ 素数)が D1 で実際に働いた: $\lvert\mathfrak F_0\rvert=p$ 素数 + $G_N$ 非可換 ⟹ 等号成立。合成表なしで先に予言できた。
4. **TIER-1.5 の発火可能性が Stage 0 で予言できる**: TIER-1.5 は $\mathrm{dl}(\mathfrak F_0)\ge3$ を要求するが、命題 7.1 より
 $$\mathrm{dl}(\mathfrak F_0)\le\mathrm{dl}\bigl(C_{P_N}(\bar y)\bigr)+\mathrm{dl}\bigl(\mathrm{Stab}_{\mathrm{Aut}(P_N)}(\bar x)\bigr).$$
 **右辺 $\le2$ の窓では TIER-1.5 は原理的に発火しない。** 掃引の陽性判定路がどの窓で生きているかを事前に表にできる。
5. **反例 $L$ の機構(T-E 重み 2)と Hol 篩の関係**: $L$ では $P_L$ が class 2 成分($H_3$)を含み、命題 4.3(2)の「$E_{0,f}=\mathrm{id}$」層がちょうど重み 2 の層に対応する。$\ker\Xi$ が「重み 1 で潰れずに残る層」の群論的正体であり、**kerchi の【文献要請】(重み分解)は $\ker\Xi$ と $\mathrm{Im}\,\Xi$ の分解を計算する問題に翻訳できる**。これは有限群論の計算で閉じるので、文献なしでも窓ごとには決着する。
6. **T-B(B2) の適用範囲**: $Q$ 巡回 $\iff N_{\rm ord}\in\{1,2,p^k,2p^k\}$($p$ 奇)。D1 は $N_{\rm ord}=2p$ なので $Q\cong C_2\times C_{p-1}$ で非巡回、$\Lambda^2Q\cong C_2$。$(\mathfrak F_0)_Q=0$ なので (B1) で等号 — 実測一致(§5.4)。

### 7.5 D1 における $\ker\widetilde\chi$ の見込み(委嘱の設問)

**予想**: $\ker\widetilde\chi(N_p)\cong C_p$、$[G,G]=\ker\widetilde\chi$(等号成立)、$G_N^{\rm ab}\cong(\mathbf Z/4p)^\times$。
**根拠**: $p=5,7$ の実測 + T-B(B1)($Q$ が $C_p$ に忠実作用ゆえ余不変量 0)+ §3.3 の Borel 構造。
**含意**: D1 は TIER-1(核非可換)にすら到達しない。**W-C は「壁を破る帯」ではなく「予言を検証する帯」。**

---

## 8. 未閉鎖項・状態札・検算証明書

### 8.1 状態札(混同禁止)

| 内容 | 札 |
|---|---|
| §1.1・1.3・1.5、§2.2・2.3・2.4、§3.1・3.3・3.4、§4.3、§6.3・6.6、§7.1・7.2 | **紙上証明(paper-proof candidate)**。Lean verified ではない |
| §2.4 の最小位数 14/24/60、§2.2 の $c_m=\varphi(2M)$($M\le200$) | **GAP 単系統検算**。cross-checked ではない |
| §5.3 の $p=5,7$ 全数表 | **予備計算・単系統・非登録**。node 独立レーン未実施。**登録宇宙の掃引結果ではない** |
| 予想 W-C-Pred(§5.4)、§7.5 の見込み | **予想(candidate)**。$p=5,7$ の 2 点しか根拠がない |
| §7.3 の $A_{13}$ | **GAP 単系統検算**($P$ 水準の実現可能性のみ。$B_3$-窓への持ち上げは **UNKNOWN**) |
| $\mathrm{Out}(B_3)\cong C_2$ | **正典外(Dyer–Grossman)**。§6.2 で correctness から分離済み |

### 8.2 未閉鎖項

- 【WA-a】**予想 W-C-Pred の族的証明**。$H_N\subseteq$ Borel(§3.3)は $\psi$ 像側を閉じるだけで、$\lvert GT(N_p)\rvert=2p(p-1)$ と isolated 性の族的証明にはならない。$p=11,13$ の予備計算は未実施(候補数 $20\times1320$、$24\times2184$ — 実行可能な規模)。
- 【WA-b】**§5.3 の二系統化**。node 独立レーンで $p=5$ の 40 shadow・合成表・導来列を再計算すれば cross-checked に昇格する。**入力は $E$ の乗積表と $\bar x,\bar y,\bar c$、$f$ の像**(v1.2 のレーン独立性規約どおり)。
- 【WA-c】**§7.3 の $B_3$-窓への持ち上げ**(D2 逆設計)。$\mathrm{ord}(s_1)=2\,\mathrm{ord}(\bar x)$、braid 関係、$E\twoheadrightarrow S_3$ を同時に満たす $E$ の構成。**壁キャンペーンの次の実質的一手はここ**だと考える。
- 【WA-d】**命題 7.1 の $U'$ の同定**。現状 $U'\subseteq U$ の包含しか使っていない。$U'$ を正確に決めれば $\mathfrak F_0$ の位数が理論的に出る可能性がある(D1 では $U'=U\cong C_p$ が実測)。
- 【WA-e】(W3′) の更なる鋭化。$P_N$ には $N\trianglelefteq B_3$ 由来の制約($c\in N$ 窓では $N_{F_2}$ の $\theta,\tau$-不変性)があり、$\lvert P_N\rvert\ge60$ の床はさらに上がる可能性がある。**本稿では使っていない**($c\notin N$ 窓では成り立たないため)。

### 8.3 検算証明書(すべて GAP 4.16.0、`gap.ps1`、単系統)

| スクリプト | SHA-256 | 内容 |
|---|---|---|
| `search/probe/wall_audit_v1/floors.g` | `58b0f6a374dc07a55535a1d443ed96867850ce40919839b327dd212ab48d3d02` | $c_m=\varphi(2M)$($M\le200$)、2 生成有限群の最小位数(§2.2・2.4) |
| `search/probe/wall_audit_v1/congp.g` | `965009060400c3ff8195baa40fc8dc8e1ab86653584d49f2be3f73d959f1578f` | D1 族 $p=5,7$ の完全列挙・isolated 判定・$G_N$ 構成・$\ker\Theta$・$H_N$・$U$(§5.3) |
| `search/probe/wall_audit_v1/holsieve.g` | `9beedc0d6d8ef686a6c559071eb5b62352484ec6f2aee89077bf207e9b0e4521` | 命題 7.1($\Xi$ が準同型・像/核)の数値検証(§7.1) |
| `search/probe/wall_audit_v1/design.g` | `f01e7cb3c42e2a90848b0973c12533e09e7903d97da4b3834982f9f497cdadc8` | 系 7.2 の必要条件の実現可能性($A_{13}$)(§7.3) |

**規約の扱い(§1.5 の語規約)**: `congp.g` は $\sigma_i\mapsto s_i$ を**自由群からの準同型**として構成し(braid 関係子が消えることを実行時に確認)、語も判定式も **paper 順で左から** GAP の行列積に写す。行列積は左右作用の問題を生じないので規約 W-1 の置換群向けの読み替え(`paper AB ↔ GAP B*A`)は不要。**逆順の対照実験も実行**し、$p=5$ で $40\to24$ と値が変わることを確認した(この窓は規約盲点ではない)。

### 8.4 自己監査(falsifier 前)

| # | リスク | 判定 |
|---|---|---|
| R-1 | §5.3 の hexagon 実装ミス | ○ 一度 (3.4) の $\sigma_1^{2m+1}$ を $\sigma_1$ と誤記し、$\widetilde\chi$ が全射でない($\lvert\mathrm{Im}\rvert=2$)という**矛盾**が出て検出できた。T-A(4) が**バグ検出器として働いた**実例。修正後は全指標が整合 |
| R-2 | 命題 7.1 が settled を前提 | ○ **明示**。非 settled shadow には $\Xi$ が定義できない — 札 B の型修理が前提であることを本文で明記 |
| R-3 | (W3′) が $[P_N,P_N]$ への**集合**単射しか使っていない | ○ 意図的。$\mathfrak F_0$ の群法は (3.53) で $P_N$ の積ではないので、位数の比較のみに使った |
| R-4 | 「band W-A 全窓可解」が probe の 66 本という**計数**に依存 | ○ 依存しない。指数上界 192 だけから従う(probe は本数の情報のみ) |
| R-5 | 予想 W-C-Pred を結果と混同 | ○ **予想と明記**。$p=11,13$ 未検証 |
| R-6 | §7.3 が $B_3$-窓の存在を主張していると読まれる危険 | ○ **$P$ 水準のみ**と明記。持ち上げは 【WA-c】 |
| R-7 | $\iota$-固定の証明(命題 6.6)が $D_n$ の関係式に依存 | ○ $sr^{-1}=rs$、$(rs)^{-1}=rs$ を明示的に使用。$n$ に依らない |
| R-8 | §2.5 の「46 本」が probe JSON の読み取りに依存 | △ `wall_probe_20260728.json` stage 192 の `in_PB3=true` レコードの `index` を機械集計した(66 本中 index $\ge84$ が 46 本)。**JSON の正しさ自体は継承した仮定** |

---

## 9. 総括 — v1.2 への差し戻し事項

1. **【blocker】** 群対象の型の手順①に**全射性**を追加(§1.2)。
2. **【要更新】** band W-A の位置づけ: 「指数 $<48$ 消去」→ **「非可解性は band 全体が理論消去済み。非 metabelian の計算対象は指数 $\ge84$ の 46 窓のみ」**(§2.5)。
3. **【要更新】** Stage 0 の (W2) を **(W2′) $\lvert[P_N,P_N]\rvert<60$** に置換(§2.3)。
4. **【要更新】** Stage 0 に **Hol 篩 2 欄**を追加し、$H_N$ 欄は参考へ降格(§7.1)。nilpotent/class-2 の条項から $\ker\Theta$ ゲートと $\Theta$ 忠実の前件を削除(§4.3)。
5. **【要更新】** band W-C の位置づけを「最優先探索帯」→ **「予言つき較正帯」**(予想 W-C-Pred)へ(§5.5)。あわせて D1 が提供する 3 つの negative/adversarial fixture を較正欄に登録(§5.6)。
6. **【要更新】** 対称簡約: 根拠を $\mathrm{Out}(B_3)$ から $\iota\in\mathrm{Aut}\setminus\mathrm{Inn}$ へ(正典内で閉じる・§6.2)。transport 式 $[m,f]\mapsto[m,\iota(f)]$ と **$\iota(K)$** を証明書欄に明記(§6.3・6.4)。**主要 2 族が $\iota$-固定である**旨の但し書き(§6.6)。$\iota$ 欄と規約欄の分離(§6.5)。
7. **【新設提案】** band W-D(標的族)の事前登録スペックを系 7.2 の必要条件で書く(§7.2)。
