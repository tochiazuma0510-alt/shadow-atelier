# 鍵補題 SAT-L1 の判定と、その代わりに出てきたもの — **中心化群律**と生き残りの構成 v1

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-30
- 委嘱: 司令塔「鍵補題 SAT-L1 の証明」(PRUNE 飽和の本丸)+ 追加制約データ 2 便(r=4 C 枝・B 枝)
- 入力正本: `docs/notes/pruning_law_v2.md` §6 / `docs/notes/pruning_law_v1_1.md` / `docs/week1-定義ノート.md` §2・§1.5 / `sol/裁定_233_SOL87FIX相互監査.md`
- 実測入力: `search/certs/norm_embedding_20260731.json`(9 窓)/ `search/certs/r4_W_E_A20_5x4t0_C_20260730.json` / `..._B_20260730.json`
- **Sol 便は読んでいない**(委嘱指示どおり sol_reply_87 まで)。

> ### ⚠ 向きの注記(2026-07-31 追記・裁定ノート `hexagon_orientation_ruling_v1.md` 参照)
> **本稿の $f$ は judge(`kerchi-judge.g`)の $f$ の逆元である。** 本稿は $\bar y^{\,f}=f^{-1}\bar yf$(右共役)で書き、judge は paper 語 $f^{-1}\bar yf$ を `AbstractProd` 反転規約で GAP `f*ybar*f^-1`(左共役)と書く。$f_{\rm judge}=f_{\rm mine}^{-1}$ とおくと**写像 $T_{0,f}$ は完全に一致**し、$\Xi$ の値 $\alpha$ も同一 — **同じ shadow の別ラベル**である。
> したがって**本稿の個数・群構造・$\Xi$ 像・結論はすべてそのまま正しい**。judge 規約で書き直すときは定理 SURV を
> $$f_z:=a_1\cdot\bigl(a_1^{\,z}\bigr)\qquad(\text{本稿の }f_z=(a_1^{\,z})a_1\ \text{の逆元})$$
> と置き換えればよい(この向きで judge の実物条件が P-WALL-2 で 2280/2280、W-CENT-B で 162/162 を生成条件込みで通過)。**手書き式で得た $f$ を judge の式に入れない**こと(混用が唯一の実害)。

---

## 0. 結論(先出し)

| # | 主張 | 格 |
|---|---|---|
| **①** | **SAT-L1 は偽**。$c\mapsto(R_1,R_2)$ の $\rho$ は準同型でない($P$ 非可換ゆえ)。障害は $\operatorname{coker}\rho$ ではない | **反証(proof)+ 明示反例(機械)** |
| **②** | 正しい平行移動公式 $\mathcal A(cf_0)=\rho_a(c)\mathcal A(f_0)$、$\rho_a(c)=c\cdot{}^{u}c$($u=f_0a$)。$\rho_a$ は**非可換 1-コサイクル型**で、解集合は $\ker\rho$ の coset ではなく**捻れ共役類**の合併 | **proof**(機械確認つき) |
| **③** | **定理 RED**: $m=0$ の hexagon 系 $\iff\ (fa_1)^2=1\ \wedge\ (fb_1^{-1})^3=1$。すなわち **$v:=a_1b_1^{-1}$ の (2,3)-分解問題** | **定理**(紙 6 行 + 機械で 2 窓**集合一致**) |
| **④** | **補題 SAT-T1**(transporter 非空)を完全証明。本族の全窓で $\mathcal T_\alpha\ne\varnothing$($\forall\alpha\in H$) | **定理**(初等・完結) |
| **⑤** | **定理 SURV(生き残りの構成)**: $z\in C_{S_n}(v)$ ごとに $f_z:=(a_1^{\,z})a_1$ は**必ず** shadow(hexagon + 生成)。$z\mapsto f_z$ は単射。よって $\lvert\ker\widetilde\chi\rvert\ \ge\ \lvert C_{S_n}(v)\rvert$ | **定理**(構成的・**工房初の「生き残り」定理**)+ 11 窓で全 $z$ 通過を機械確認 |
| **⑥** | **予想 CENT(中心化群律)**: $\ \ker\widetilde\chi\ \cong\ C_{S_n}(w)$、$w=b_1^{-1}a_1$($\bar x=w^2$)。**位数・群構造とも 11/11 窓で的中**(r=4 両枝を含む) | **candidate**(⊇ は定理・⊆ は未証明)。11 窓 machine-measured |
| **⑦** | 飽和の正体 = **剛性(rigidity)**: $\subseteq$ は「$v$ の生成的 (2,3)-分解が $C_{S_n}(v)$-共役で一意」と同値。作用は**自由**(証明済)なので $\lvert\ker\rvert=\lvert C_{S_n}(v)\rvert\cdot N$、$N$ = Nielsen 類の個数 | **proof**(還元)+ $N=1$ は 11 窓 measured |
| **⑧** | **PRUNE 律($\ell^{s_2(r)}$)は棄却**。r=4 C 枝の反証は偶然ではなく、$(\mathrm{Stab},S)$ だけの関数である律は**原理的に不可能**(同一 $(\mathrm{Stab},S,B,N)$ で B/C 両枝の答が違う) | **反証(実データ + 機構)** |
| **⑨** | $\varepsilon$ 依存の所在を特定: **$\mathrm{sgn}(a_1)$**(= $g=fa_1$ が住む $A_n$-剰余類)と $v$ の**巡回型**。$P$・$C_P(\bar y)$・$\mathrm{Stab}$ は両枝共通で、依存は残差の**定数項** $v$ にのみ入る | **proof**(司令塔の予想を確認) |
| **⑩** | r=4 の「第二の $C_5$」の正体: $w$ が $(10,10)$ 型(C 枝)/ $(10,5,5)$ 型(B 枝)であること。$A=\mathrm{Syl}_5(C_{S_n}(w))$ の座標が実測と**完全一致** | **proof + 機械一致** |
| **⑪** | **真の境界変数は $p$**(= $w$ に含まれる $2\ell$-巡回の本数)。$t$ でも $r$ でも「$\mathrm{Syl}_2(S_r)$ の非可換性」でもない。奇部 $=\ell^{\,r-p}$、$\varepsilon$ は $p+s$ のパリティを固定する | **candidate**(11/11 窓一致)+ 型の決定は **proof**(§7.5) |
| **⑫** | ~~P-CENT-1($n{=}10$)~~ → **撤回**。**定理 TRI(三角群ゲート)**: $\mathrm{ord}(w)\le5$ の窓は $\langle a_1,b_1\rangle\le\Delta(2,3,5)\cong A_5$ ゆえ**存在しない** — 司令塔の陰性走査(50 対すべて位数 60)の**紙上証明**。$p=0,s=0,\ell=5$ の窓($n{=}15$、$n{=}25$ 壁案を含む)はすべて不可 | **定理**(§10.5.2) |
| **⑬** | **代替の最安判別窓 P-CENT-2**: $\ell=5$、$(r,t)=(2,2)$、$w=(5,5,2)$、$n=12$ ⟹ CENT $\lvert\ker\rvert=100$ vs PRUNE $20$(**5 倍差**)。$a_1$ 候補 $62{,}370$ 個の全数走査で済む | **凍結候補**(§10.5.4) |
| **⑭** | **壁(P4)は $n=27$ で届く**: $w=(5^5,2)$ ⟹ $C_{S_{27}}(w)=(C_5\wr S_5)\times C_2\supseteq S_5$ 非可解。**定理 SURV+ により飽和も剛性も要らず、下限だけで「$\mathrm{GTSh}$ 非可解」が従う**。しかも悉皆($2\times10^{12}$)不要で $7.5\times10^5$ の構成で足りる | **設計 candidate + 下限は定理**(§10.5.5) |
| **⑮** | **$\Xi$ 像の閉じた式**: $\Xi(f_z)=z^{a_1}$ ⟹ $C_{S_n}(w)\subseteq\Xi(\ker\widetilde\chi)\subseteq C_{S_n}(w^2)$。CENT は「**shadow は $\bar x$ ではなく平方根 $w$(分岐データ)を見る**」の一文に要約される | **定理 SURV+**(§10.5.1) |
| **⑯** | **定理 CENT-0**: $w$ が偶長巡回をもたない($p=s=0$)なら $C(w)=C(w^2)$ で**挟み撃ちが閉じ**、$\Xi(\ker\widetilde\chi)=\mathrm{Stab}(\bar x)$ が**定理**。この族で CENT は証明済・PRUNE は証明つきで反証(刈り込みゼロ) | **定理**(§10.6.3) |
| **⑰** | **壁 P4 到達**: **P-WALL-2**($n=24$・$w_0=(19,1^5)$)の witness を構成し全点検。$\Xi(\ker\widetilde\chi)=C_{19}\times S_5$(非可解)⟹ **$\mathrm{GTSh}(N,N)$ は非可解**。飽和・剛性・$\Xi$ 単射のいずれも不要(下限のみ) | **窓 assert + 2280 shadow 全数検算**(§10.6.5) |
| **⑱** | **判別窓 W-CENT-B**($n=18$・$w_0=(9,9)$)の witness も構成・全点検。$\lvert\Xi(\ker)\rvert=162$ vs PRUNE $18$(9 倍差)・奇部 $81=\ell^{r-p}$ vs $s_2$ 律 $9$ | **窓 assert + 162 shadow 全数検算**(§10.6.4) |
| **⑲** | **存在判定は走査前に閉じる**: 不動点なし + 素数長巡回の設計なら推移性・原始性・Jordan が自動 ⟹ **指標係数 $>0$ ⟺ 窓が存在**。witness は 2-opt 山登りで数秒(乱択 $10^{-9}$ を代替) | **proof + 手法**(§10.6.5–6) |

> **一行で**: SAT-L1 は落ちたが、その解剖の途中で **hexagon が (2,3)-分解問題であること**が判り、そこから**核の閉じた記述 $C_{S_n}(w)$** が出た。$\supseteq$(生き残り)は**証明済み**、$\subseteq$ は**剛性**という既知の型の問題に還元された。

---

## 1. 記号・規約(窓の構成をそのまま使う)

命題 0.3 型窓の構成(`search/probe/wac_v1/*.g` の `BuildS1S2E` 系と同一):

- $a_1,b_1\in S_n$、$a_1^2=1$、$b_1^3=1$、$\langle a_1,b_1\rangle\in\{A_n,S_n\}$。
- $a:=a_1\cdot(n{+}1,n{+}3)$、$b:=b_1\cdot(n{+}1,n{+}3,n{+}2)$、$E:=\langle a,b\rangle\le S_{n+3}$。
- $\sigma_1:=b^{-1}a$、$\sigma_2:=ab^2$。**$\bar x=\sigma_1^2$、$\bar y=\sigma_2^2$、$P:=\langle\bar x,\bar y\rangle=A_n$。**
- $c=(\sigma_1\sigma_2)^3=b^3=1$ ゆえ **$c\in N$**(本族では自動)。$\mathrm{Aut}(P)=S_n$($n\ne6$)。

> ### 観察 1.1(marking の同定 — 以後すべてここに乗る)【proof・機械確認】
> $$\sigma_1\sigma_2=b,\qquad \sigma_1\sigma_2\sigma_1=a .$$
> すなわち **$\delta:=\sigma_1\sigma_2$ は marking の 3-元 $b$ そのもの、$\Delta:=\sigma_1\sigma_2\sigma_1$ は対合 $a$ そのもの**。
> **証明.** $\sigma_1\sigma_2=(b^{-1}a)(ab^2)=b^{-1}a^2b^2=b^{-1}b^2=b$。$\sigma_1\sigma_2\sigma_1=b\cdot b^{-1}a=a$。∎
> $\Delta^2=a^2=1$、$\delta^3=b^3=1$。**$E$ は $C_2*C_3=\mathrm{PSL}_2(\mathbf Z)$ の有限商であり、$\Delta,\delta$ がその $(2,3)$-生成対**。

さらに $S_n$-成分だけを見ると
$$\sigma_1\ \leftrightarrow\ w:=b_1^{-1}a_1,\qquad \sigma_2\ \leftrightarrow\ v:=a_1b_1^{-1}\quad(b^2=b^{-1}\ \text{ゆえ}),$$
$$\boxed{\ \bar x=w^2,\qquad \bar y=v^2,\qquad v=a_1wa_1\ (\text{ゆえ}\ \bar y=\bar x^{\,a_1}).\ }$$

**$\varepsilon$ 分岐**: $\mathrm{sgn}(a_1)=+1\iff\langle a_1,b_1\rangle=A_n\iff E=A_n\times S_3$($\varepsilon=0$)。$\mathrm{sgn}(a_1)=-1\iff\langle a_1,b_1\rangle=S_n\iff E=S_n\times_{C_2}S_3$($\varepsilon=1$)。($b_1$ は 3-巡回の積ゆえ常に偶。)

**hexagon の正本形($m=0$・工房の judge と同一)**: `prune_ident2.g` の判定式をそのまま採る。
$$\text{(H1)}\quad \sigma_1f^{-1}\sigma_2f=f^{-1}\sigma_1\sigma_2,\qquad
\text{(H2)}\quad f^{-1}\sigma_2f\sigma_1=\sigma_2\sigma_1f\qquad(f\in P).$$
積の向きは GAP の `*` と同一(規約 W-1 の作用式で paper 語 "AB" $\leftrightarrow$ `B*A`)。以下 ${}^{g}u:=gug^{-1}$。

---

## 2. 定理 RED — $m=0$ hexagon は $v$ の (2,3)-分解問題である

> ### 定理 RED【定理・紙上完全証明 + 機械で集合一致】
> $f\in P$ に対し
> $$\text{(H1)}\wedge\text{(H2)}\iff (fa)^2=1\ \wedge\ (fb^{-1})^3=1\iff (fa_1)^2=1\ \wedge\ (fb_1^{-1})^3=1 .$$
> さらに $g:=fa_1$、$h:=fb_1^{-1}$ とおくと、これは
> $$\boxed{\ g^2=1,\qquad h^3=1,\qquad gh=v\ \ (v:=a_1b_1^{-1})\ }$$
> と同値($g^2=1$ より $v=g^{-1}h=gh$)。**すなわち $m=0$ 層は、固定元 $v$ の「対合 × 位数 3」分解の集合**である。基点は $(g,h)=(a_1,\,b_1^{-1})$($f=1$ に対応)。

**証明.**
(i) (H1) を左から $f$ 倍して $f\sigma_1f^{-1}\sigma_2f=\sigma_1\sigma_2$、これは
$$f\cdot({}^{\sigma_1}f)^{-1}\cdot({}^{\sigma_1\sigma_2}f)=1 \tag{2.1}$$
と同値(展開すれば同じ語)。
(ii) (H2) を左から $f$ 倍・右から $f^{-1}\sigma_1^{-1}$ 倍して $\sigma_2\cdot f({}^{\sigma_1}f)^{-1}=f\sigma_2$、すなわち
$$f\cdot({}^{\sigma_1}f)^{-1}={}^{\sigma_2^{-1}}f. \tag{2.2}$$
(iii) (2.1) は $f({}^{\sigma_1}f)^{-1}=({}^{b}f)^{-1}$($b=\sigma_1\sigma_2$)と読める。(2.2) と併せて $({}^bf)^{-1}={}^{\sigma_2^{-1}}f$。両辺に ${}^{\sigma_2}(-)$ を施すと $({}^{\sigma_2b}f)^{-1}=f$。$\sigma_2b=\sigma_2\sigma_1\sigma_2=\sigma_1\sigma_2\sigma_1=a$(braid)だから
$${}^af=f^{-1}\iff (fa)^2=1. \tag{R-a}$$
(iv) (R-a) の下で ${}^{\sigma_1}f={}^{b^{-1}a}f={}^{b^{-1}}(f^{-1})=({}^{b^{-1}}f)^{-1}$。これを (2.1) に代入して
$$f\cdot({}^{b^{-1}}f)\cdot({}^{b}f)=1 .$$
$b^3=1$ より ${}^{b^{-1}}={}^{b^2}$。積が 1 になる条件は巡回置換で不変だから $({}^{b^2}f)({}^bf)\,f=1$ と同値。ここで
$$({}^{b^2}f)({}^bf)f=b^2fb^{-2}\cdot bfb^{-1}\cdot f=b^2\,(fb^{-1})(fb^{-1})\,f=b^2(fb^{-1})^3b$$
($b^{-2}b=b^{-1}$ と $(fb^{-1})^2f=(fb^{-1})^3b$ を使う)。$b^3=1$ ゆえ
$$({}^{b^2}f)({}^bf)f=1\iff (fb^{-1})^3=b^{-3}=1. \tag{R-b}$$
逆向きは同じ変形を逆にたどる((iii)(iv) はいずれも同値変形)。
(v) $f\in S_n$ は tail $(n{+}1,n{+}2,n{+}3)$ と可換ゆえ $(fa)^2=(fa_1)^2\cdot(\text{tail})^2=(fa_1)^2$、同様に $(fb^{-1})^3=(fb_1^{-1})^3$。
(vi) $g=fa_1$、$h=fb_1^{-1}$ なら $gv=fa_1\cdot a_1b_1^{-1}=fb_1^{-1}=h$ かつ $g^2=1$ ゆえ $v=g^{-1}h=gh$。∎

**機械照合**(`sat_l1_probe1.g`): `W-E-A10-5x2t0` と `W-E-A15-5x3t0` で、$C_{S_n}(\bar y)\cdot\mathrm{Stab}$ 上の全候補について
$\{(\mathrm{H1})\wedge(\mathrm{H2})\}$ と $\{(fa)^2{=}1\wedge(fb^{-1})^3{=}1\}$ と $\{(fa_1)^2{=}1\wedge(fb_1^{-1})^3{=}1\}$ が **集合として一致**(10 個 / 50 個・証明書値と一致)。向きを誤った $(fb)^3=1$ 版は 1 個しか返さない — **規約 W-4「(H-b′) は向きに敏感」の再現**。

> ### 系 RED-1(GT 公理の幾何的意味)
> $m=0$ shadow $\iff$ marking の $(2,3)$-対 $(a_1,b_1^{-1})$ を、**積 $v$ を保ったまま**別の $(2,3)$-対 $(g,h)$ へ動かすこと。$f=ga_1$ が「動かし方」。これは dessins/Hurwitz の Nielsen 類の言葉そのものである。

---

## 3. SAT-L1 の判定 — **偽**。ただし平行移動公式は正しい形で残る

### 3.1 まず torsor の向きの訂正

`pruning_law_v2` §6.1 は $f'f^{-1}\in C_P(\bar y)$ と正しく書いているが、§6.3 で $f=f_0c$ と**右から**掛けている。$\bar y^f=f^{-1}\bar yf$ の規約では
$$\bar y^{f}=\bar y^{f_0}\iff ff_0^{-1}\in C(\bar y)\iff f=c\,f_0\ (c\in C_P(\bar y))$$
で **左剰余類**。以下 $f=cf_0$ を採る(この訂正がないと以下の公式は成立しない)。

### 3.2 平行移動公式(正しい形)

$\mathcal A(f):=(fa)^2$、$\mathcal B(f):=(fb^{-1})^3$(定理 RED の残差)とおく。

> ### 補題 SAT-L1′(平行移動公式)【proof】
> 任意の $c\in P$、$f_0\in P$ に対し
> $$\mathcal A(cf_0)=\rho_a(c)\cdot\mathcal A(f_0),\qquad \rho_a(c):=c\cdot{}^{u}c\quad(u:=f_0a),$$
> $$\mathcal B(cf_0)=\rho_b(c)\cdot\mathcal B(f_0),\qquad \rho_b(c):={}^{v_1}c\cdot{}^{v_2}c\cdot{}^{v_3}c$$
> ($v_1,v_2,v_3$ は $f_0,b$ から決まる定数)。**証明.** $(cf_0a)^2=cf_0ac f_0a=c\cdot{}^{f_0a}c\cdot(f_0a)^2$。$\mathcal B$ も同様に 3 項へ分解。∎
> **機械確認**: `sat_l1_probe1.g` で全 $c\in C_P(\bar y)$ について成立(2 窓)。

### 3.3 SAT-L1 の反証

> ### 判定 SAT-L1 = **偽**【proof + 明示反例】
> $\rho_a$ が準同型 $\iff\ \forall c,d:\ d\cdot{}^{u}c={}^{u}c\cdot d\ \iff\ [P,{}^uP]=1\iff P$ 可換。
> 本族では $P=A_n$(完全群)ゆえ **$\rho_a$ は準同型でない**。したがって「$\rho$ と定数の合成 = アフィン写像」「解集合 = $\ker\rho$ の coset」「障害 = $\operatorname{coker}\rho$ の 1 元」という SAT-L1 の骨格は**すべて成立しない**。
> **明示反例**(`W-E-A10-5x2t0`、$f_0=1$、$u=a$): $c=d=(2,5,9,6,10)\in C_P(\bar y)$ に対し
> $$\rho_a(cd)=(1,9,10,3)(2,7,5,6)\ \ne\ (1,3)(2,6)(5,7)(9,10)=\rho_a(c)\rho_a(d).$$
> $C_P(\bar y)$ の $625$ 対のうち **576 対**で準同型が破れる($r{=}3$ 窓では $139876/140625$)。

### 3.4 では正しい枠組みは何か — 非可換 1-コサイクル

$a^2=1$ ゆえ $\mathcal A(f)=f\cdot{}^af$ は **$C_2=\langle a\rangle$ の $P$ 係数 1-コサイクル条件**そのもの、$\mathcal B(f)=1$ は **$C_3=\langle b\rangle$ の 1-コサイクル条件**である:
$$\{f:\mathcal A(f)=1\}=Z^1(\langle a\rangle,P),\qquad \{f:\mathcal B(f)=1\}=Z^1(\langle b\rangle,P).$$
$Z^1$ は部分群ではなく、**捻れ共役 $c\star f:=cf\,{}^ac^{-1}$ で安定な集合**(軌道 = $H^1$ の類)。したがって

> **障害は $\operatorname{coker}\rho$(アーベル的余核)ではなく、$H^1(C_2,P)\times H^1(C_3,P)$ の中の「対角一致」条件である。** $m=0$ 層 $=Z^1(\langle a\rangle,P)\cap Z^1(\langle b\rangle,P)$(自由積 $C_2*C_3=\mathrm{PSL}_2(\mathbf Z)$ の $Z^1$ の**対角切片**)。

これが定理 RED の (2,3)-分解の別表現である。**SAT-L1 が「アフィン」を仮定したのは、非可換係数のコサイクルを可換群の 1-コサイクルと取り違えたため**と特定できる。

---

## 4. 補題 SAT-T1(transporter 非空)— 完全証明

> ### 補題 SAT-T1【定理・初等・完結】
> $\alpha\in S_n$ に対し $\mathcal T_\alpha:=\{f\in P=A_n:\bar y^f=\bar y^\alpha\}$ とおくと
> $$\mathcal T_\alpha\ne\varnothing\iff C_{S_n}(\bar y)\alpha\cap A_n\ne\varnothing\iff \bigl[\alpha\in A_n\ \text{または}\ C_{S_n}(\bar y)\not\le A_n\bigr].$$
> $\bar y$ が型 $(\ell^r,1^t)$($\ell$ 奇)なら $C_{S_n}(\bar y)=(C_\ell\wr S_r)\times S_t$ で、
> $$C_{S_n}(\bar y)\not\le A_n\iff r\ge2\ \text{または}\ t\ge2 .$$
> ($\ell$ 奇ゆえ 2 つの $\ell$-ブロックの互換は $\ell$ 個の互換の積 = **奇**。$S_t$ の互換も奇。$\ell$-巡回自身は偶。)
> **したがって本族(命題 0.3 型窓)では $r\ge2$ または $t\ge2$ なら $\forall\alpha\in S_n$ で $\mathcal T_\alpha\ne\varnothing$。残る $r=1,t\le1$ では $H=C_{S_n}(\bar x)=C_\ell\le A_n$ ゆえ全 $\alpha\in H$ は偶で、やはり $\mathcal T_\alpha\ne\varnothing$。**
> **系: 本族の全窓・全 $\alpha\in H$ で (T1) は成立する。**(pruning_law_v2 §6.2 の「見込み」を証明に格上げ。)

**証明.** $\bar y^f=\bar y^\alpha\iff f\alpha^{-1}\in C_{S_n}(\bar y)\iff f\in C_{S_n}(\bar y)\alpha$。剰余類 $C\alpha$ が $A_n$ と交わるのは、$\alpha$ が偶であるか、$C$ が奇置換を含むかのいずれか。∎

**注**: v2 §6.2 の「$A_n$-類が分裂しない」という言い方は正しい直観だが、正確には**剰余類 $C_{S_n}(\bar y)\alpha$ が $A_n$ と交わるか**の問題である(同値だが、後者は 1 行で片づく)。

---

## 5. 定理 SURV — 工房初の「生き残り」定理(構成的)

> ### 定理 SURV【定理・構成的】
> $v:=a_1b_1^{-1}$、$z\in C_{S_n}(v)$ とし
> $$\boxed{\ f_z:=(a_1^{\,z})\cdot a_1=z^{-1}a_1za_1\ }$$
> と定める。このとき
> **(i)** $f_z\in A_n=P$;
> **(ii)** $f_z$ は $m=0$ hexagon (H1)(H2) を満たす;
> **(iii)** marking が丸ごと $z$-共役へ移る: $f_za=a^{\,z}$ かつ $bf_z^{-1}=b^{\,z}$(すなわち $(g,h)=(a_1,b_1^{-1})^z$);
> **(iv)** $z\mapsto f_z$ は**単射**;
> したがって
> $$\bigl\lvert\{f\in P:\ m=0\ \text{hexagon}\}\bigr\rvert\ \ge\ \bigl\lvert C_{S_n}(v)\bigr\rvert=\bigl\lvert C_{S_n}(w)\bigr\rvert .$$

**証明.**
(i) $g:=f_za_1=a_1^{\,z}$ は $a_1$ の共役ゆえ $\mathrm{sgn}(g)=\mathrm{sgn}(a_1)$、よって $\mathrm{sgn}(f_z)=\mathrm{sgn}(g)\mathrm{sgn}(a_1)=1$。
(ii) $g^2=(a_1^z)^2=1$。$gv=a_1^{\,z}v=a_1^{\,z}v^{\,z}=(a_1v)^{\,z}=(b_1^{-1})^{\,z}$ ゆえ $(gv)^3=((b_1^{-1})^3)^z=1$。定理 RED により hexagon。
(iii) $z\in C(v)$ より $a_1^zb_1^{-z}=v$、ゆえに $b_1^{\,z}=b_1a_1a_1^{\,z}=b_1f_z^{-1}$。tail を付ければ $E$ の中で $f_za=a^z$、$bf_z^{-1}=b^z$。
(iv) $f_z=f_{z'}\Rightarrow a_1^z=a_1^{z'}\Rightarrow z'z^{-1}\in C(a_1)\cap C(v)=C(\langle a_1,v\rangle)=C(\langle a_1,b_1\rangle)=C_{S_n}(A_n\ \text{or}\ S_n)=1$($n\ge5$)。∎

> ### 系 SURV-2(生成条件も自動 — ただし条件つき)
> (iii) より $\langle g,h\rangle=\langle a_1,b_1\rangle^z=\langle a_1,b_1\rangle$。**全 11 窓で $\langle\bar x,\bar y^{f_z}\rangle=P$ を全 $z$ について機械確認済み**(`sat_l1_probe3/4.g`)。
> **【GAP-S1】** 「$\langle g,h\rangle=\langle a_1,b_1\rangle\Rightarrow\langle\bar x,\bar y^{f}\rangle=P$」の紙上証明は未完。$\bar y^{f_z}=\bar x^{\,za_1}$(§1 の $\bar y=\bar x^{a_1}$ から計算)なので、必要なのは「$\bar x$ とその共役 $\bar x^{za_1}$ が $A_n$ を生成する」— **$z=1$ での既知の成立から一般 $z$ へ渡す議論が要る**(未証明・機械では 11 窓全通過)。

**これが「何が生き残るか」を出す工房初の定理である**(`pruning_law_v1` §4.4 が「一本もない」と書いた型)。$R_\tau$(死ぬ側)の双対がここで初めて書けた。

---

## 6. 予想 CENT(中心化群律)と、飽和 = 剛性

> ### 予想 CENT【candidate・11/11 窓 machine-measured】
> $$\boxed{\ \ker\widetilde\chi\ \cong\ C_{S_n}(w),\qquad w=b_1^{-1}a_1\ \ (\bar x=w^2)\ }$$
> 同型は $z\mapsto f_{z^{a_1}}$(すなわち $C_{S_n}(v)\xrightarrow{\ \sim\ }\ker\widetilde\chi$、$C_{S_n}(w)=C_{S_n}(v)^{a_1}$)。
> **$\supseteq$(位数の下限)は定理 SURV で証明済み。$\subseteq$ が未証明**(=§6.2 の剛性)。

### 6.1 実測(11 窓・全一致)

| 窓 | $n$ | $\mathrm{sgn}(a_1)$ | $v$ の型 | $\lvert C_{S_n}(v)\rvert$ | 実測 $\lvert\ker\widetilde\chi\rvert$ | 構造 $C_{S_n}(v)$ | 実測 $K$ 構造 |
|---|---|---|---|---|---|---|---|
| W-E-A10-9t1 | 10 | $+$ | $(9,1)$ | **9** | 9 | $C_9$ | — |
| W-E-A11-9t2 | 11 | $-$ | $(9,2)$ | **18** | 18 | $C_{18}$ | — |
| W-E-A12-9t3 | 12 | $-$ | $(9,2,1)$ | **18** | 18 | $C_{18}$ | — |
| W-E-A13-9t4 | 13 | $+$ | $(9,2,2)$ | **72** | 72 | $C_9\times D_8$ | — |
| W-E-A10-5x2t0 | 10 | $-$ | $(10)$ | **10** | 10 | $C_{10}$ | — |
| W-E-A15-5x3t0 | 15 | $-$ | $(10,5)$ | **50** | 50 | $C_{10}\times C_5$ | — |
| W-D-A16-11a | 16 | $+$ | $(11,2,2,1)$ | **88** | 88 | $C_{11}\times D_8$ | — |
| W-D-A18-13a | 18 | $+$ | $(13,2,2,1)$ | **104** | 104 | $C_{13}\times D_8$ | — |
| W-D-A20-15a | 20 | $+$ | $(15,2,2,1)$ | **120** | 120 | $C_{15}\times D_8$ | — |
| **W-E-A20-5x4t0-C**($\varepsilon{=}0$) | 20 | $+$ | $(10,10)$ | **200** | **200** | `C5 x ((C10 x C2) : C2)`・`IdGroup [200,31]` | **同一文字列**・cert `[200,31]` |
| **W-E-A20-5x4t0-B**($\varepsilon{=}1$) | 20 | $-$ | $(10,5,5)$ | **500** | **500** | `C5 x C10 x D10` | **同一文字列** |

**位数 11/11 一致。構造も r=4 両枝で `StructureDescription` の文字列・`IdGroup` まで一致**(cert `7_K_struct`・`7b_K_idgroup` と突合)。

さらに **$A=\mathrm{Syl}_5$ の座標も一致**(`sat_l1_probe2.g` で $B_x$ 座標を独立再計算):

| 枝 | 予測($C_{S_n}(w)$ の $\ell$-部) | 実測座標(独立再計算) |
|---|---|---|
| C($w=(10,10)$) | 各 $C_{10}$ の 5-部 = その 2 つの 5-ブロックに**等しく**作用 ⟹ $\{(a,a,b,b)\}$、$5^2$ | $\{(a,a,b,b)\}$ **25 本** ✓ |
| B($w=(10,5,5)$) | $C_{10}$ の 5-部が $\{(a,a,\ast,\ast)\}$、$C_5\wr S_2$ の base が自由 ⟹ $\{(a,a,c,d)\}$、$5^3$ | $\{(a,a,c,d)\}$ **125 本** ✓ |

2-部も一致: C 枝の $\Xi(\ker)$ の**偶な対合が 11 個**(独立再計算)= $C_{10}\wr S_2$ の 13 個の対合のうち偶なもの 11 個(base の $(5,5)$ 型 1 個 + 外側 10 個)。ブロック置換の内訳 $[2,1,4,3]\times1$、$[3,4,1,2]\times5$、$[4,3,2,1]\times5$ も輪積の構造と一致。

### 6.2 飽和の正体 = 剛性(rigidity)

> ### 定理 SAT-RIG(飽和の還元)【proof】
> $\mathcal F(v):=\{(g,h): g^2=1,\ h^3=1,\ gh=v,\ \langle g,h\rangle=\langle a_1,b_1\rangle,\ \mathrm{sgn}(g)=\mathrm{sgn}(a_1)\}$ とおく。
> **(a)** 定理 RED により $\ker\widetilde\chi\ \leftrightarrow\ \mathcal F(v)$(全単射 $f\leftrightarrow(fa_1,fb_1^{-1})$)。
> **(b)** $C_{S_n}(v)$ は $\mathcal F(v)$ に同時共役で作用し、**この作用は自由**(安定化群 $=C_{S_n}(\langle g,h\rangle)=C_{S_n}(A_n\text{ or }S_n)=1$)。
> **(c)** ゆえに $$\lvert\ker\widetilde\chi\rvert=\lvert C_{S_n}(v)\rvert\cdot N,\qquad N:=\#\bigl(\mathcal F(v)/C_{S_n}(v)\bigr)\in\mathbf Z_{\ge1}.$$
> **(d)** **飽和 $\iff N=1\iff$「$v$ の生成的 $(2,3)$-分解は $C_{S_n}(v)$-共役を除いて一意」= 逆 Galois 論でいう剛性条件そのもの。**

**したがって $\lvert\ker\widetilde\chi\rvert$ は必ず $\lvert C_{S_n}(w)\rvert$ の倍数**(これは定理)。11 窓すべてで $N=1$(measured)。

**Frobenius 公式による見通し**(未実施・次の probe 候補): $N$ は
$$\#\{(g,h)\in\mathcal C_1\times\mathcal C_2: gh=v\}=\frac{\lvert\mathcal C_1\rvert\lvert\mathcal C_2\rvert}{\lvert G\rvert}\sum_\chi\frac{\chi(\mathcal C_1)\chi(\mathcal C_2)\overline{\chi(v)}}{\chi(1)}$$
を対合類 $\mathcal C_1$・3-元類 $\mathcal C_2$ について足し、非生成対を引けば出る。$G=S_n$ の指標和は $n=20$ でも `ctbllib` で可能な規模。**これが $N=1$ の紙上証明への最短路と考える。**

---

## 7. 司令塔の 6 条件への回答

**(1) coker $\rho$ の $t$ 依存の有無** → **問い自体が失効**。$\rho$ は準同型でないので $\operatorname{coker}$ は定義されない(§3.3)。正しい量は $N$(Nielsen 類の個数)で、これは $(t$ ではなく$)$ $v$ の巡回型と $\mathrm{sgn}(a_1)$ の関数。$t$ は $v$ の型に $(\dots,2,2,1)$ 等として現れるだけ。

**(2) 「$t$ 非依存に飽和ちょうど」が出てしまわないか** → 出ない。定理 SURV/SAT-RIG の $\lvert C_{S_n}(v)\rvert$ は $v$ の巡回型に完全に依存し、$t$ が変われば型が変わる(表 §6.1: $t=1,2,3,4$ で $9,18,18,72$)。**変質した前提は「残差が $(\mathrm{Stab},S)$ だけで書ける」という暗黙の仮定**であり、$m=0$ 制限でも $C_P(\bar y)$ の記述でもない。

**(3) r=4 C 枝の「第二の $C_5$」の理論的説明** → $w$ が $(10,10)$ 型だから。$C_{S_{20}}(w)=C_{10}\wr S_2$ の 5-部は $C_5\times C_5$ で、各 $C_5$ は 1 本の 10-巡回の 2 乗、すなわち**その 10-巡回が割れてできた 2 つの $\bar x$-ブロックに同じ量だけ回す**。座標 $(a,a,b,b)$ の「$a,a$」がそれ。**対角 $\langle\bar x\rangle$ は $a=b$ の線**。第二の $C_5$ は「2 本の 10-巡回を独立に回せる」ことの反映であり、$\mathrm{Syl}_2(\mathrm{Stab})$ の固定点とは無関係。生き残りの機構は定理 SURV そのもの($z$ = その回転)。

**(4) $\varepsilon$ 依存がどこから入るか** → 司令塔の推測どおり**定数項**から。厳密には 2 か所、いずれも $\sigma$ の $E$-持ち上げ経由:
- **(a) $v=a_1b_1^{-1}$ の巡回型**: C 枝 $(10,10)$ / B 枝 $(10,5,5)$。$\bar x=w^2$ が同じ $(5,5,5,5)$ でも、**その平方根 $w$ の型は $\varepsilon$ で変わる**(パリティ制約 $\mathrm{sgn}(w)=\mathrm{sgn}(a_1)$ による)。$\mathrm{Stab},S,B_x,N$ が両枝同一でも $C_{S_n}(w)$ は違う — これが割れの機構。
- **(b) 対合因子 $g=fa_1$ が住む剰余類**: $\varepsilon=0$ なら $g$ は偶、$\varepsilon=1$ なら奇。分解の探索空間そのものが違う。
$P$・$C_P(\bar y)$・$\mathrm{Stab}$ が共通でも答が違うことは、これで**完全に説明される**。

**(5) 数値整合(C 枝 $5^2$/対角 $5$、B 枝 $5^3$/対角 $5$)** → §6.1 の表で両方同時に出る:$\mathrm{Syl}_5(C_{S_n}(w))$ は C 枝で $C_5^2$、B 枝で $C_5^3$、対角 $\langle\bar x\rangle$ はどちらでも $w$ の全体回転 1 本。**座標集合まで実測一致**(§6.1 下段)。

**(6) $S'$ が枝で違う($D_8$ vs $C_2\times C_2$)** → $\mathrm{Syl}_2(C_{S_n}(w))$ が $C_{10}\wr S_2$ なら $D_8$、$C_{10}\times(C_5\wr S_2)$ なら $C_2\times C_2$。**「実際に作用する 2-群」は $\mathrm{Syl}_2(\mathrm{Stab})$ ではなく $\mathrm{Syl}_2(C_{S_n}(w))$**。LOC-1 の「$S$-方向退化」は、$S$ を $\mathrm{Syl}_2(\mathrm{Stab})$ と取る限り成立しない(B 枝が反例) — **$S$ の定義を $\mathrm{Syl}_2(C_{S_n}(w))$ に取り替えるべき**というのが本稿からの提案。

---

## 7.5 境界変数の同定 — $t$ でも $r$ でも「$\mathrm{Syl}_2(S_r)$ の非可換性」でもない

司令塔の第 3 信(訂正)は「境界は $t$ ではなく $r=4$($\mathrm{Syl}_2(S_r)$ が初めて非可換)ではないか」という candidate を出した。本稿の枠組みは**この 3 候補をすべて排除し、真の境界変数を名指しできる**。

### 7.5.1 閉じた位数公式

本族の窓の $w=b_1^{-1}a_1$ は、$\bar x=w^2$ が型 $(\ell^r,1^t)$ であることから、必ず
$$w\ =\ (2\ell)^{\,p}\ (\ell)^{\,r-2p}\ (2)^{\,s}\ (1)^{\,t-2s}\qquad(0\le 2p\le r,\ 0\le 2s\le t)$$
の型をもつ($2\ell$-巡回は平方で 2 本の $\ell$-巡回に割れ、$\ell$ 奇ゆえ $\ell$-巡回は平方でそのまま; 2-巡回は平方で 2 個の不動点に割れる)。**$(p,s)$ は工房が既に存在設計(Ree 条件)で追っている量そのもの**(`pruning_law_v1` §5.1 の $\mathsf w=(2\ell)^p(\ell)^{r-2p}$)。予想 CENT はこのとき

> ### 予想 CENT-ORD(閉じた位数公式)【candidate・11/11 窓一致】
> $$\boxed{\ \lvert\ker\widetilde\chi\rvert=\underbrace{(2\ell)^p\,p!}_{C_{2\ell}\wr S_p}\cdot\underbrace{\ell^{\,r-2p}(r-2p)!}_{C_\ell\wr S_{r-2p}}\cdot\underbrace{2^s s!}_{C_2\wr S_s}\cdot\underbrace{(t-2s)!}_{S_{t-2s}}\ }$$
> 特に **$\ell$-部は $\ \ell^{\,r-p}\times(\ell\text{-part of }p!\,(r-2p)!)$**、すなわち標準域($p,r-2p<\ell$)では
> $$\boxed{\ \lvert\ker\widetilde\chi\rvert_{\ell}\ =\ \ell^{\,r-p}\ }$$
> さらに $\mathrm{sgn}(w)=\mathrm{sgn}(a_1)$($b_1$ は常に偶)から
> $$\boxed{\ \varepsilon=0\iff p+s\ \text{偶},\qquad \varepsilon=1\iff p+s\ \text{奇}.\ }$$

**11 窓での照合(すべて一致)**:

| 窓 | $\ell$ | $(r,t)$ | $w$ の型 | $(p,s)$ | $p{+}s$ | $\mathrm{sgn}(a_1)$ 実測 | 公式値 | 実測 $\lvert\ker\rvert$ |
|---|---|---|---|---|---|---|---|---|
| A10-9t1 | 9 | (1,1) | $(9,1)$ | (0,0) | 偶 | $+$ ✓ | $9$ | 9 |
| A11-9t2 | 9 | (1,2) | $(9,2)$ | (0,1) | 奇 | $-$ ✓ | $9\cdot2$ | 18 |
| A12-9t3 | 9 | (1,3) | $(9,2,1)$ | (0,1) | 奇 | $-$ ✓ | $9\cdot2\cdot1$ | 18 |
| A13-9t4 | 9 | (1,4) | $(9,2,2)$ | (0,2) | 偶 | $+$ ✓ | $9\cdot(4\cdot2)$ | 72 |
| A10-5x2t0 | 5 | (2,0) | $(10)$ | (1,0) | 奇 | $-$ ✓ | $10\cdot1$ | 10 |
| A15-5x3t0 | 5 | (3,0) | $(10,5)$ | (1,0) | 奇 | $-$ ✓ | $10\cdot5$ | 50 |
| A16-11a | 11 | (1,5) | $(11,2,2,1)$ | (0,2) | 偶 | $+$ ✓ | $11\cdot8\cdot1$ | 88 |
| A18-13a | 13 | (1,5) | $(13,2,2,1)$ | (0,2) | 偶 | $+$ ✓ | $13\cdot8$ | 104 |
| A20-15a | 15 | (1,5) | $(15,2,2,1)$ | (0,2) | 偶 | $+$ ✓ | $15\cdot8$ | 120 |
| **r4-C** | 5 | (4,0) | $(10,10)$ | **(2,0)** | 偶 | $+$ ✓ | $10^2\cdot2$ | **200** |
| **r4-B** | 5 | (4,0) | $(10,5,5)$ | **(1,0)** | 奇 | $-$ ✓ | $10\cdot(5^2\cdot2)$ | **500** |

### 7.5.2 3 つの境界候補の棄却

- **$t$ 説**: 棄却(司令塔自身の訂正どおり)。$t$ は $(s,t{-}2s)$ を通じて**位数には効くが飽和の破れとは無関係**。
- **$r=4$ 説 / $\mathrm{Syl}_2(S_r)$ 非可換性説**: **棄却できる**。破れたのは $\ell$-部が $\ell^{s_2(r)}$ でなくなったことだが、真の値は $\ell^{r-p}$ であり、**$r$ にも $\mathrm{Syl}_2(S_r)$ にも依存しない**。$r\le3$ で $s_2$ と一致していたのは
 $$r=1:\ p=0\Rightarrow \ell^{1}=\ell^{s_2(1)};\qquad r=2:\ p=1\Rightarrow\ell^{1}=\ell^{s_2(2)};\qquad r=3:\ p=1\Rightarrow\ell^{2}=\ell^{s_2(3)}$$
 という**測定された窓の $p$ がたまたま $r-p=s_2(r)$ を満たしていた**だけ。$r=4$ では $\varepsilon=0$ 枝が $p=2\Rightarrow\ell^2$、$\varepsilon=1$ 枝が $p=1\Rightarrow\ell^3$ で、どちらも $s_2(4)=1$ と外れる。
- **C 枝($S'=D_8$)と B 枝($S'=V_4$)で壊れ方が違う理由**も $p$ で説明される: $S'=\mathrm{Syl}_2(C_{2\ell}\wr S_p\times C_\ell\wr S_{r-2p})$ で、$p=2$ なら $C_2\wr S_2=D_8$、$p=1,r-2p=2$ なら $C_2\times C_2$。**「作用する 2-群」は $\mathrm{Syl}_2(\mathrm{Stab})$ ではなく $\mathrm{Syl}_2(C_{S_n}(w))$**(§7 (6))。

### 7.5.3 **安い決定的判別窓の提案**($n=10$ で $s_2$ 説に止めを刺す)

> ### 予言 P-CENT-1(凍結候補)
> **$(r,t)=(2,0)$、$\ell=5$、$n=10$、$\varepsilon=0$(= $\mathrm{sgn}(a_1)=+1$)の窓**、すなわち $w=(5,5)$($p=0$)型の窓を実現せよ。
> - **予想 CENT の予言**: $\lvert\ker\widetilde\chi\rvert=\lvert C_{S_{10}}((5,5))\rvert=\lvert C_5\wr S_2\rvert=\mathbf{50}$、奇部 $\mathbf{25}=\ell^{r-p}=\ell^2$、2-部 $C_2$、$\lvert\mathrm{GTSh}\rvert=4\cdot50=200$。
> - **$s_2$ 律の予言**: 奇部 $\ell^{s_2(2)}=5$、$\lvert\ker\rvert=10$。
> - **5 倍差。$n=10$ なので探索コストは r=4 窓の $10^{-7}$ 程度**(既存の A10 窓と同じ規模)。
> **存在の一次点検**: $a_1$ は偶ゆえ互換数 $k$ 偶、$b_1$ は 3-巡回 $j$ 本。Ree: $c(a_1)+c(b_1)+c(w)\le n+2$ すなわち $(10-k)+(10-2j)+2\le12\iff k+2j\ge10$。$k\le5$・$j\le3$ かつ $k$ 偶 ⟹ **$(k,j)=(4,3)$ が唯一**(等号 = 種数 0)。$\mathrm{sgn}(w)=+1=(-1)^{p+s}$、$s=0$ ⟹ $p$ 偶 ⟹ $p=0$ ✓ 整合。
> **⟹ 実現探索は $S_{10}$ 内の小さな走査で済む。これが次の最安の決定打**(r=4 の再走行は不要)。

同様に $(r,t)=(3,0)$・$\varepsilon=0$($w=(5,5,5)$、$p=0$)なら予言 $\lvert\ker\rvert=\lvert C_5\wr S_3\rvert=750$、奇部 $5^3\cdot3=375$ — $s_2$ 律の $25$ と **30 倍差**($n=15$)。

## 7.6 A の座標パターンの判別 — 「$S'$ の可換部分群の固定空間」か「$w$ のブロック対」か

司令塔の第 4 信は C 枝の $A$ 座標を $\{(a,a,b,b)\}$ と確定し、読みとして **$A=B^{\langle(12),(34)\rangle}$**($D_8$ の可換な鏡映部分群の固定空間)を candidate 提示した。座標の**値**は本稿の独立再計算(`sat_l1_probe2.g`)と完全一致する。しかし**読み(機構)は 2 つある**:

| 仮説 | 内容 | $\langle(12),(34)\rangle$ という「対の取り方」の説明 |
|---|---|---|
| **X**(司令塔) | $A=B^{H_0}$、$H_0=$ $S'$ の可換部分群 | **なし**(なぜ $(12),(34)$ で $(13),(24)$ でないかは未説明) |
| **Y**(本稿) | $A=\mathrm{Syl}_\ell\bigl(C_{S_n}(w)\bigr)$ = 「$w$ の各巡回を回す」ことの全体 | **あり**: 等値を強制される 2 ブロックは、**$w$ の 1 本の $2\ell$-巡回が平方で割れてできた 2 つの半分**。窓に内在する量で、選択の余地がない |

> ### 判別実験(`sat_l1_probe5.g`)— **仮説 Y 支持・X は不完全**
> $w$ の巡回が触れる $\bar x$-ブロックを直接出力した:
>
> | 窓 | $w$ の巡回 → ブロック | 予測 $A$ 座標 | 実測 $A$ 座標 |
> |---|---|---|---|
> | C 枝 | $10\to\{1,2\}$、$10\to\{3,4\}$ | $(a,a,b,b)$ | **$(a,a,b,b)$ ✓** |
> | B 枝 | $10\to\{1,2\}$、$5\to\{3\}$、$5\to\{4\}$ | $(a,a,c,d)$ | **$(a,a,c,d)$ ✓** |
> | r=3 窓 | $10\to\{1,2\}$、$5\to\{3\}$ | $(a,a,b)$ | **$(a,a,b)$ ✓**(`pruning_law_v1` §2.2 の実測と一致) |
>
> **仮説 X は C 枝では正しい答を出すが、B 枝では $B^{\langle(12),(34)\rangle}=\{(a,a,c,c)\}$($5^2$)を与えて外れる**(実測 $5^3$)。仮説 Y は 3 窓すべてで的中。

> ### **prediction-first の記録**(司令塔の要請に対して)
> 司令塔の B 枝 probe 着弾**前**に、本稿は既に B 枝の $A$ を**独立に測定済み**である:
> - `sat_l1_probe2.g`(本セッション内で実行完了・出力は task ログ `b41417apg`)が $A_B=\{(a,a,c,d)\}$、**125 本**、$A\cong C_5^3$、$\Xi$ は各 $\alpha$ に $f$ ちょうど 1 個、を出力済み。
> - 司令塔の予言「$B$ 枝は $\mathrm{fixed}(\langle(12)\rangle)=\{(a,a,b,c)\}$」と**値としては一致**する(座標の並べ方の差のみ)。
> - **ただし機構は異なる**: 本稿は $\langle(12)\rangle$ を「$S'$ の部分群」としてではなく「$w$ の $2\ell$-巡回が束ねたブロック対」として導く。**$2\ell$-巡回が 2 本ある窓(C 枝)で両説は割れ、実測は Y を支持した。**

> ### 司令塔の「[S,S] 方向が効かない」検算課題への回答
> $\rho$ の線型化という道具立ては §3.3 で否定された(準同型でない)ので、「$c$ の $[S,S]$-方向が $R$ に効かない」という形の計算は**そもそも立たない**。代わりに定理 SURV が同じ現象を**構成で**説明する: 生き残る奇 shadow は $z\in\mathrm{Syl}_\ell(C_{S_n}(w))$ から来る $f_z$ であり、$z$ が回すのは **$w$ の巡回**であって $\bar x$ のブロックではない。$2\ell$-巡回は 2 ブロックを 1 本に束ねているので、その回転は 2 ブロックに**同じ量**を与える — これが「$(a,a,\cdot,\cdot)$」の正体である。$[S',S']$ は登場しない。

---

## 8. PRUNE 系の格の更新(何が死に、何が生き残るか)

| 主張 | 更新後の格 |
|---|---|
| 予想 PRUNE $\Xi(\ker)=C_{O_{2'}(\mathrm{Stab})}(S)\times S$ | **棄却**。r=4 C 枝(奇部 25 > 5)・B 枝(2-部 $V_4\ne D_8$)の二重反証 |
| 系 PRUNE-1 $\lvert$奇部$\rvert=\ell^{s_2(r)}$ | **棄却**(C 枝で $5^2\ne5^{s_2(4)}=5$) |
| 対抗 $\ell^{r-1}$ | 既に撤回済(r=1・r=4 とも不一致) |
| **定理 PRUNE-FIX**($C_{O_{2'}(H)}(T)\cong C_\ell^{s_2(r)}$) | **無傷**(抽象群 $H$ の固定点計算として真)。ただし**核とは無関係だったことが確定** |
| Stab 律(2-部 = $\mathrm{Syl}_2(\mathrm{Stab})$) | **棄却**(B 枝: 2-部 $=C_2\times C_2$、$\mathrm{Syl}_2(\mathrm{Stab})=D_8$) |
| 補題 PR-1($\subseteq$ 方向) | 前提 (D)(直積性)が B/C 枝で偽ゆえ**空回り**。$\subseteq$ は §6.2 の剛性へ置換 |
| **$(\mathrm{Stab},S)$ だけの関数である律** | **原理的に不可能**(同一 $(\mathrm{Stab},S,B_x,N)$ で 200 と 500) |

**なぜ PRUNE が 16 標本で当たっていたか**も説明がつく: 梯子・D 族では $v$ の型が $(\ell,2,2,\dots)$ で $C_{S_n}(v)=C_\ell\times D_8$ 等となり、たまたま $C_{O_{2'}}(S)\times S$ と同型になる。**$r\ge2$ で $\ell$-ブロックが複数本の 10-巡回に束ねられる窓で初めて分岐する**。

---

## 9. 残ギャップ・次の一手・【文献要請】

### 9.1 未証明(名指し)

- **【GAP-C1】剛性 $N=1$**(= 予想 CENT の $\subseteq$)。§6.2 の Frobenius 指標和が最短路。**これが本丸の後継**。
- **【GAP-S1】**(§5 系)「$\langle\bar x,\bar x^{za_1}\rangle=A_n$ が全 $z\in C(v)$ で成立」の紙上証明。11 窓 machine のみ。
- **【GAP-M】$m\ne0$ 層**: 本稿は $m=0$ のみ。規約 W-4 の一般形から、$m$ 層は $(fa_1)^2=1\wedge(f\bar y^{\,m}b_1^{-1})^3=1$、すなわち**固定元 $u_m:=a_1\bar y^{\,m}b_1^{-1}$ の (2,3)-分解**になるはず(**candidate・未検証**)。もし正しければ
 $$\lvert\mathrm{GTSh}(N,N)\rvert=\sum_{m\ \mathrm{charming}}\lvert C_{S_n}(u_m)\rvert\cdot N_m$$
 という**完全な位数公式**が出る。次の probe の第一候補(コスト小)。
- **$\Xi$ 単射 (I)**: 本稿は触れていない(9 窓 measured のまま)。ただし定理 RED により $\ker\widetilde\chi$ が $\mathcal F(v)$ と同一視できたので、$\Xi$ 単射は「$(g,h)$ が $\bar y^f$ で決まる」という別問題に翻訳できる。

### 9.2 【文献要請】

> **困難**: 有限交代群/対称群 $G$($n\le20$)と固定元 $v\in G$(型 $(10,10)$、$(10,5,5)$、$(\ell,2,2,1)$ 等)に対し、
> $$\mathcal F(v)=\{(g,h): g^2=1,\ h^3=1,\ gh=v,\ \langle g,h\rangle=G\}$$
> が $C_G(v)$-共役の下で**単一軌道**である(= 剛性 $N=1$)ための判定条件が欲しい。
> **欲しい結果の型**: (a) 種数 0 系(genus-0 systems)や $(2,3,k)$-Hurwitz 系の分類で、$C(v)$-軌道数が 1 になる条件を与える定理; (b) Frobenius 指標和から軌道数を読む標準手続き(非生成対の差し引きを含む); (c) 「$v$ の巡回型が $\ell$-ブロックを 2 本ずつ束ねる」型での既知の剛性例。
> **注**: これは逆 Galois 論の剛性判定・Hurwitz 空間の連結成分の言葉と思われるが、**正典外なので自分では漁っていない**(文献ゲート遵守)。降りてくれば §6.2 に直結する。

### 9.3 Sol への申し送り(相互裏取り用)

- 定理 RED は **6 行で検証可能**(§2 の証明)。ここが崩れると本稿は全部崩れる — **最優先の監査点**。
- 定理 SURV は **4 行**。$z\in C(v)$ の条件を $C(w)$ と取り違えると falsе になる(向きに注意)。
- 予想 CENT の $\subseteq$ は未証明。**「11 窓で当たったから真」とは書いていない**。

---

## 10. 検算(GAP 4.16.0・`gap.ps1`・単系統)

| スクリプト | SHA-256 | 内容 | 結果 |
|---|---|---|---|
| `search/probe/wac_v1/sat_l1_probe1.g` | `2daae0c9…92dc24` | 定理 RED の集合一致(2 窓悉皆)・$(fb)^3$ 版との分離・$\rho_a$ 非準同型の明示反例・平行移動公式 | RED 一致 10/10・50/50、反例出力、公式全 $c$ 成立 |
| `search/probe/wac_v1/sat_l1_probe2.g` | `480a8ed6…42cef1` | r=4 両枝の $A=\Xi(\ker)\cap B_x$ 座標と 2-元の独立再計算(還元形を使い $1.1\times10^7$ 反復へ圧縮) | C: 25 本 $\{(a,a,b,b)\}$ / B: 125 本 $\{(a,a,c,d)\}$・偶対合 11 個 / 5 個 |
| `search/probe/wac_v1/sat_l1_probe3.g` | `1d0d2162…04d2a7` | 定理 SURV の全項目(4 窓)+ $z\mapsto\alpha_z$ の準同型性 + 小窓での $\mathrm{Sol}$ 完全一致 | 全 true・$\lvert C(v)\rvert=10,50,200,500$、`IdGroup [200,31]`/`[500,53]` |
| `search/probe/wac_v1/sat_l1_probe4.g` | `01512816…f2e9f4` | 9 窓一斉(norm_embedding と同一窓)の $\lvert C_{S_n}(v)\rvert$ vs 実測 $\lvert\ker\rvert$ | **9/9 一致**・全 $z$ で hexagon+生成 |
| `search/probe/wac_v1/sat_l1_probe5.g` | `d7d987b5…5363c7` | $w$ の巡回 → $\bar x$-ブロック対応(仮説 X vs Y の判別) | 3 窓で Y 的中(§7.6) |
| `search/probe/wac_v1/sat_l1_probe6.g` | `75a523e6…0ff2a4` | (A) $\Xi(f_z)=a_1za_1$ の全 $z$ 照合(4 窓)/ (B) $\lvert\Delta(2,3,m)\rvert$、$m=3,4,5$ | (A) 4 窓全 true / (B) $12,24,\mathbf{60}$($m\ge6$ は列挙非停止 = 無限性は古典事実として引用) |
| `search/probe/wac_v1/sat_l1_probe7.g` | `87d6087d…a4aabc` | n=12 の 3840 障害の同定(悉皆再現)+ 指標計数の初回較正 | $2^5{:}S_5$・推移・**非原始**(ブロック 2×6)。100 対を再現 |
| `search/probe/wac_v1/sat_l1_probe8.g` | `cea3cff3…e4ca19` | $T_{\rm all}$(Frobenius)+ $T_{\rm trans}$(巡回集合分割 Möbius)の機構と 11 窓較正 | §10.6.2 の表(司令塔の悉皆値 50・100 を厳密再現) |
| `search/probe/wac_v1/sat_l1_probe9.g` | `6a0720e8…f6b49e` | 判別候補 A/B/C の $T_{\rm trans}$ + **壁窓 n=24 の単一指標係数** | A 588 / B 5292 / C 18522、**壁 = 2280 = $\lvert C\rvert$(軌道 1)** |
| `search/probe/wac_v1/sat_l1_probe10.g` | `5f3f9f1e…aed1bd` | P-WALL-2 の witness を 2-opt 山登りで構成 | **HIT**(restart 11・step 568)・$\langle a_1,b_1\rangle=A_{24}$ |
| `search/probe/wac_v1/sat_l1_probe11.g` | `7bbd9250…93e2a4` | P-WALL-2 の窓 assert + 2280 shadow 全数検算 | 全 assert ✓・落ち 0・$\Xi(\ker)=C_{19}\times S_5$ 非可解 |
| `search/probe/wac_v1/sat_l1_probe12.g` | `295fc125…8e5bba` | 判別窓 A(n=14)・B(n=18)の witness 探索 | B は $A_{18}$ 到達 ✓ / A は真部分群を引いた(再走行で可) |
| `search/probe/wac_v1/sat_l1_probe13.g` | `2e622c2d…45841d` | W-CENT-B(n=18)の窓 assert + 162 shadow 全数検算 | 全 assert ✓・落ち 0・$\Xi(\ker)=\mathrm{Stab}=162$ |

(SHA-256 全長は `provenance/LEDGER.md` 記帳時に司令塔が再計算のこと。上は先頭 8 + 末尾 6 桁。)

**単系統(GAP のみ)。cross-checked ではない。Lean verified でもない。登録宇宙の掃引結果ではなく、台帳請求権は発生していない。**

---

## 10.5 追補 — 裁定 238 追記 2 への回答(SURV+・三角群ゲート・次の窓設計)

### 10.5.1 定理 SURV+ — $\Xi$ 像の閉じた式(機械観察を定理へ格上げ)

> ### 定理 SURV+【定理・2 行】
> §5 の $f_z=(a_1^{\,z})a_1$($z\in C_{S_n}(v)$)に対し
> $$\boxed{\ \Xi([0,f_z])\ =\ a_1za_1\ =\ z^{\,a_1}.\ }$$
> したがって $\Xi$ の像は**部分群として** $C_{S_n}(v)^{a_1}=C_{S_n}(w)$ を含み、
> $$\boxed{\ C_{S_n}(w)\ \subseteq\ \Xi(\ker\widetilde\chi)\ \subseteq\ C_{S_n}(\bar x)=C_{S_n}(w^2).\ }$$
> **証明.** $\alpha:=a_1za_1$ とおく。$\bar y=v^2$ と $z\in C(v)$ から $\bar y^{\,z}=\bar y$、ゆえに $\bar x^{\,\alpha}=(\bar x^{a_1})^{za_1}=(\bar y^{\,z})^{a_1}=\bar y^{\,a_1}=\bar x$($\bar y=\bar x^{a_1}$、$a_1^2=1$)。また §5(iii) の計算から $\bar y^{\,f_z}=\bar x^{\,za_1}=(\bar x^{a_1})^{a_1za_1}=\bar y^{\,\alpha}$。$\Xi$ の定義($\bar x$ を固定し $\bar y\mapsto\bar y^f$ を実現する一意の元)より $\Xi=\alpha$。∎
> **機械確認**(`sat_l1_probe6.g`): 4 窓すべてで全 $z$ について一致(§6.1 の「$z\mapsto\alpha_z$ は準同型」の機械観察は、この式で説明され尽くす)。

**帰結(重要)**: **$\supseteq$ 方向は「$C_{S_n}(w)$ が丸ごと $\Xi(\ker)$ の部分群として入る」という形の定理になった。**$C_{S_n}(w)\le C_{S_n}(w^2)$ は自明なので、予想 CENT は「**shadow は $\bar x$ ではなく、その平方根 $w$(= 分岐データ)を見ている**」という一文に要約される。

### 10.5.2 定理 TRI(三角群ゲート)— P-CENT-1 が存在しないことの**証明**

司令塔の陰性結果(50 対すべて位数 60)は偶然ではなく、**必然**である。

> ### 定理 TRI【定理・古典的】
> $w=b_1^{-1}a_1$ の位数を $m$ とすると、$a_1^2=b_1^3=1$ ゆえ $\langle a_1,b_1\rangle$ は von Dyck 群
> $$\Delta(2,3,m)=\langle A,B\mid A^2,\ B^3,\ (B^{-1}A)^m\rangle$$
> の商である。$\Delta(2,3,m)$ は $\tfrac12+\tfrac13+\tfrac1m>1$ すなわち $m\le5$ のとき**有限**で
> $$\Delta(2,3,3)\cong A_4\ (12),\quad \Delta(2,3,4)\cong S_4\ (24),\quad \Delta(2,3,5)\cong A_5\ (60)$$
> ($m=6$ はユークリッド型で可解、$m\ge7$ は双曲型で無限)。**機械確認**: `sat_l1_probe6.g` で $12,24,60$ を coset enumeration で確認($m\ge6$ は列挙が停止せず — 無限性は古典的事実として引用、機械証明はしていない)。
> **系 TRI-1**: $\mathrm{ord}(w)=5$ の窓では $\langle a_1,b_1\rangle$ は $A_5$ の商ゆえ位数 $\le60$。**$n\ge6$ で $A_n$ に到達不能。**

**$\mathrm{ord}(w)$ の計算**: §7.5.1 より $w=(2\ell)^p(\ell)^{r-2p}(2)^s(1)^{t-2s}$ なので
$$\mathrm{ord}(w)=\begin{cases}2\ell & (p\ge1\ \text{または}\ s\ge1)\\ \ell & (p=s=0).\end{cases}$$

> ### 判定(小委嘱への直接回答)
> | 提案窓 | $\ell$ | $(p,s)$ | $\mathrm{ord}(w)$ | 判定 |
> |---|---|---|---|---|
> | **P-CENT-1** $(r,t)=(2,0)$、$n=10$、$w=(5,5)$ | 5 | $(0,0)$ | **5** | **存在しない(定理 TRI)**。司令塔の全数走査(50 対すべて位数 60)と完全一致 — **陰性の紙上説明が付いた** |
> | 本稿 §7.5.3 の第二候補 $(r,t)=(3,0)$、$n=15$、$w=(5,5,5)$ | 5 | $(0,0)$ | **5** | **存在しない**。同じ理由。**本稿の提案を撤回する** |
> | 司令塔 candidate(裁定 238 追記) $r=5$、$n=25$、$w=(5^5)$ | 5 | $(0,0)$ | **5** | **存在しない**。同じ理由。**壁の設計図はこの形では不可** |
>
> **⟹ 「Ree 予算だけでなく生成到達性まで」という司令塔の懸念は正しく、その正体は種数ではなく $\mathrm{ord}(w)$ である。** 種数 0 自体は無害(既存の `W-E-A10-5x2t0` は種数 0 で $S_{10}$ に到達している)。

**「50 対」の生値も説明が付く**: $\lvert C_{S_{10}}((5,5))\rvert=5\cdot5\cdot2=\mathbf{50}$。定理 SAT-RIG(§6.2)の自由作用は $\langle g,h\rangle=A_5$(10 点上推移・$C_{S_{10}}(A_5)=1$)でも成立するので、分解の個数は $\lvert C(w)\rvert\cdot N=50N$。実測 50 ⟹ **$N=1$(剛性)がこの退化窓でも成立**。司令塔の「例外なく $A_5$」は「$C(w)$-軌道が 1 本」の言い換えである。

### 10.5.3 設計則(必要条件のチェックリスト)と **$s=1$ トリック**

窓設計は以下を順に通すこと(①②が hard gate):

1. **【三角群ゲート・必要】** $\mathrm{ord}(w)\ge7$。$\ell=5$ で $t=0$ なら $p\ge1$ が**必須**。$\ell\ge7$ なら $p=0$ も可。
2. **【パリティ】** $\mathrm{sgn}(a_1)=(-1)^{p+s}$($=\varepsilon$ 分岐を決める)。
3. **【Ree/種数】** $k+2j\ \ge\ n+r+t-p-s-2$、$k\le\lfloor n/2\rfloor$、$j\le\lfloor n/3\rfloor$、$k\equiv p+s\ (2)$。種数 $=\tfrac12\bigl(k+2j-(n+r+t-p-s-2)\bigr)$。
4. **【生成到達性】** ★**$s=1$ トリック**: $s=1$ なら $w^{\ell}$ は**ちょうど 1 個の互換**。原始群が互換を含めば $S_n$ 全体(古典)。**⟹ 推移性+原始性を確認するだけで $\langle a_1,b_1\rangle=S_n$ が従う。** $s=0$ や $s\ge2$ ではこの近道がない。

> **$s=1$ を積極的に使うのが本稿の設計上の推奨**である。$s\ge1$ は同時に $\mathrm{ord}(w)=2\ell$ を保証するので、**ゲート①と④を一手で通す**。

### 10.5.4 **新・最安判別窓 P-CENT-2**($n=12$)— P-CENT-1 の正しい代替

> ### 予言 P-CENT-2(凍結候補)
> **$\ell=5$、$(r,t)=(2,2)$、$(p,s)=(0,1)$、$n=12$、$w=(5,5,2)$**($\bar x=(5,5,1,1)$、$\varepsilon=1$ = $a_1$ 奇)。
> - **CENT の予言**: $\lvert\ker\widetilde\chi\rvert=\lvert C_{S_{12}}((5,5,2))\rvert=\lvert C_5\wr S_2\rvert\cdot2=\mathbf{100}$、奇部 $\mathbf{25}=\ell^{\,r-p}=5^2$、2-部 $C_2\times C_2$、$N_{\rm ord}=5$、$c_m=4$、$\lvert\mathrm{GTSh}\rvert=\mathbf{400}$。
> - **PRUNE/$s_2$ 律の予言**: 奇部 $\ell^{s_2(2)}=5$、2-部 $=\lvert\mathrm{Syl}_2(\mathrm{Stab})\rvert=4$ ⟹ $\lvert\ker\rvert=\mathbf{20}$。
> - **5 倍差**。$n=12$。
> **設計点検**: $\mathrm{ord}(w)=10\ge7$ ✓(ゲート①)。$\mathrm{sgn}(a_1)=(-1)^{0+1}=-1$ ✓。Ree: 要 $k+2j\ge12+2+2-0-1-2=13$、$k$ 奇 $\le5$・$j\le4$ ⟹ **$(k,j)=(5,4)$ の一択**(種数 0)。$c(a_1)+c(b_1)+c(w)=7+4+3=14=n+2$ ✓。
> **生成**: $w^5=$ ちょうど 1 個の互換 ⟹ **原始性を確認すれば $S_{12}$ 確定**(ゲート④)。$a_1$ 型 $2^51^2$ は $S_{12}$ に $12!/(2^5\cdot5!\cdot2!)=62{,}370$ 個 — **全数走査が一瞬**。
> **これが P-CENT-1 の正しい代替であり、$s_2$ 律に止めを刺す最安手。**

補助候補(より大きな差): $\ell=5$、$(r,t)=(3,2)$、$(p,s)=(0,1)$、$n=17$、$w=(5,5,5,2)$ ⟹ CENT $\lvert\ker\rvert=\lvert C_5\wr S_3\rvert\cdot2=1500$ vs PRUNE $25\cdot4=100$(**15 倍差**)。

### 10.5.5 壁(P4)設計 **P-WALL-1** — 非可解核は $n=27$ で届く、しかも**悉皆不要**

司令塔 candidate($r=5$・$n=25$・$w=(5^5)$)は定理 TRI で不可。**$s=1$ の尾を足すだけで復活する**:

> ### 設計 P-WALL-1(非可解核の設計図)
> **$\ell=5$、$(r,t)=(5,2)$、$(p,s)=(0,1)$、$n=27$、$w=(5^5,2)$**($\bar x=(5^5,1^2)$、$\varepsilon=1$)。
> - $C_{S_{27}}(w)=(C_5\wr S_5)\times C_2$、位数 $5^5\cdot120\cdot2=\mathbf{750{,}000}$。**$S_5$ を含むので非可解。**
> - **定理 SURV+ により、この群は $\Xi(\ker\widetilde\chi)$ の部分群として実際に埋め込まれる — 飽和(CENT の $\subseteq$)も剛性も不要。** すなわち
> $$\boxed{\ \text{窓が実現すれば}\ \mathrm{GTSh}(N,N)\ \text{は非可解}\ }$$
> が**下限として定理から従う**(上限は要らない)。**これが壁 P4 への最短路である。**
> **設計点検**: $\mathrm{ord}(w)=10$ ✓。$\mathrm{sgn}(a_1)=-1$(奇)✓。Ree: 要 $k+2j\ge27+5+2-0-1-2=31$、$k$ 奇 $\le13$・$j\le9$ ⟹ **$(k,j)=(13,9)$ の一択**(種数 0)。$c=14+9+6=29=n+2$ ✓。
> **生成**: $w^5=$ 1 個の互換 ⟹ 原始性 ⟹ $S_{27}$ ✓。
> **計算量が決定的に変わる点**: 従来の悉皆($\lvert C_{S_n}(\bar y)\rvert\cdot\lvert\mathrm{Stab}\rvert\cdot c_m\approx 2\times10^{12}$)は**不可能**だが、**定理 SURV の構成なら $\lvert C_{S_n}(w)\rvert=7.5\times10^5$ 個を作って hexagon を検算するだけ**(数分)。**⊇ の証拠は線形コストで取れる。**
> **【注意・格】** これは「$\mathrm{GTSh}$ が非可解」の**下限側**である。$\ker$ が**ちょうど** $C_{S_n}(w)$ かは CENT(未証明)。壁の主張に必要なのは下限のみ。

### 10.5.6 なぜ $\ell=5,t=0$ では $r\le3$ が $s_2$ 律と一致したか — **強制**であって偶然ではない

ゲート①($p\ge1$ 必須)と $2p\le r$ を併せると、$\ell=5$・$t=0$ では
$$r=1:\ \text{(不可)}\quad r=2:\ p=1\quad r=3:\ p=1\quad r=4:\ p\in\{1,2\}\quad r=5:\ p\in\{1,2\}$$
であり、$r\le3$ では **$p$ が一意に決まって $r-p=s_2(r)$ になってしまう**($2-1=1=s_2(2)$、$3-1=2=s_2(3)$)。$r=4$ で初めて $p$ に自由度 2 が生じ、**どちらの値でも $s_2(4)=1$ と食い違う**。

> **⟹ 司令塔の「境界は $r=4$」という直観は結論として正しかった。ただし機構は $\mathrm{Syl}_2(S_r)$ の非可換性ではなく、「三角群ゲートが $p\ge1$ を強制し、$2p\le r$ が $r\le3$ で $p$ を一意にする」ことである。**(§7.5.2 の「$r$ 説の棄却」は、この意味で**部分的に撤回**する: $r=4$ が最初の判別点であること自体は正しい。棄却されるのは「$\mathrm{Syl}_2(S_r)$ の非可換性が原因」という機構の方。)
> なお $t\ge2$ を許せば($s=1$)$\ell=5$・$r=2$ でも $p=0$ が可能になり、**$r=2$ で判別できる**(= P-CENT-2)。**境界は $r$ ではなく、$(p,s)$ の自由度がいつ生じるかで決まる。**

---

## 10.6 追補 2 — 裁定 240 追記 2 への回答(3840 の同定・計数機構・設計 v3・**壁到達**)

### 10.6.1 3840 障害の同定 — 推移だが**非原始**

`sat_l1_probe7.g` で悉皆を再現(a₁ 類 62,370 → 適合 100 対)し、生成群を同定した:

> **$G=\bigl((C_2)^5:A_5\bigr):C_2=2^5{:}S_5$、位数 3840、$\{1..12\}$ 上 **推移的**、しかし**非原始**(大きさ 2 のブロック 6 個)。**
> ブロック系の代表 $\{1,10\}$、$G\le S_2\wr S_6$ で頂 $S_5$ は 6 ブロックに推移的($\cong\mathrm{PGL}_2(5)$ の 6 点作用)。

**私の §10.5.3 ゲート④($s=1$ トリック)の誤りを明示する**: 「$w^\ell$ が 1 個の互換 ⟹ **原始性を確認すれば** $S_n$」という条件文自体は正しいが、**原始性は自動ではない**。実際この窓では互換 $w^5=(11,12)$ が**ブロックの内側**に落ちており(ブロック $\{11,12\}$)、Jordan 型の議論が発動しない。**$s=1$ トリックは「原始性が別途保証されるとき」にのみ使える** — 単独の設計原理としては撤回する。

### 10.6.2 計数機構(委嘱 1・2)— Frobenius + 巡回集合分割上の Möbius

実装(`sat_l1_probe8.g`):

- $T_{\rm all}(\lambda):=\#\{(a_1,b_1): a_1^2=1,\ b_1^3=1,\ b_1^{-1}a_1=w_0\}$($w_0$ の型 $\lambda$)を、対称群指標表の **class multiplication coefficient** を対合類 × 位数 3 類の全対で足して厳密計算。
- $T_{\rm trans}$(= $\langle a_1,b_1\rangle$ が推移的なもの)は、**$w_0$ の巡回の集合分割上の Möbius 反転**で得る:
 $$T_{\rm all}(\lambda)=\sum_{\pi\ \vdash\ \text{cycles}(\lambda)}\ \prod_{B\in\pi}T_{\rm trans}(\lambda_B).$$
 **Hall の部分群格子 Möbius の代わりにこれで足りる**(軌道は $w_0$ の巡回の合併に限られるため)。巡回数 $\le6$ なら分割数 $\le203$ で**桁違いに軽い**。

**較正(11 窓・すべて既知の答と整合)**:

| 窓 | $w$ | $\lvert C(w)\rvert$ | $T_{\rm all}$ | $T_{\rm trans}$ | $T_{\rm trans}/\lvert C\rvert$ | 実測 $\lvert\ker\rvert$ |
|---|---|---|---|---|---|---|
| n=10 $p{=}0$ | $(5,5)$ | 50 | 75 | **50** | **1** | **0**(悉皆陰性) |
| n=10 $p{=}1$ | $(10)$ | 10 | 65 | 65 | 13/2 | 10 |
| n=12 P-CENT-2 | $(5,5,2)$ | 100 | 275 | **100** | **1** | **0**(悉皆陰性) |
| n=15 | $(10,5)$ | 50 | 1035 | 710 | 71/5 | 50 |
| n=10 梯子 | $(9,1)$ | 9 | 90 | 54 | 6 | 9 |
| n=11 梯子 | $(9,2)$ | 18 | 90 | 54 | 3 | 18 |
| n=12 梯子 | $(9,2,1)$ | 18 | 270 | 54 | 3 | 18 |
| n=13 梯子 | $(9,2,2)$ | 72 | 216 | **72** | **1** | **72**(実在!) |
| n=16 D 族 | $(11,2,2,1)$ | 88 | 2354 | **88** | **1** | **88**(実在!) |
| n=20 C 枝 | $(10,10)$ | 200 | 25825 | 21600 | 108 | 200 |
| n=20 B 枝 | $(10,5,5)$ | 500 | 23475 | 11500 | 23 | 500 |

**計数機構は司令塔の悉皆走査を再現する**: n=10 の「50 対」・n=12 の「100 対」は、対応する単一 class pair の係数として**厳密に一致**(`probe7`)。**乱択・悉皆は今後不要**。

> ### 較正から出た 2 つの教訓(重要)
> **(教訓 1) $T_{\rm trans}/\lvert C\rvert=1$ は死を意味しない。** n=13 梯子と n=16 D 族は比が 1 で**実在**する(唯一の推移軌道がそのまま $A_n$ 生成)。逆に n=10($p{=}0$)と n=12 は比 1 で**その唯一の軌道が真部分群**($A_5$ / $2^5{:}S_5$)。**⟹ 残る関門は「推移だが $A_n$ でない」だけ。**
> **(教訓 2) 全 11 窓で $\lvert\ker\rvert=\lvert C(w)\rvert$**(生成分解はちょうど 1 自由軌道)。剛性 $N_{\rm gen}=1$ が計数機構でも追認された。

### 10.6.3 **定理 CENT-0** — $p=s=0$ の窓では CENT は**定理**(挟み撃ちの閉包)

> ### 定理 CENT-0【定理・2 行】
> $w$ が偶長の巡回をもたない($p=s=0$、すなわち $w=(\ell^{\,r},1^{\,t})$)とき、$\ell$ 奇より $\langle w\rangle=\langle w^2\rangle$、ゆえに
> $$C_{S_n}(w)=C_{S_n}(w^2)=C_{S_n}(\bar x)=\mathrm{Stab}(\bar x).$$
> 定理 SURV+(§10.5.1)の挟み撃ち $C_{S_n}(w)\subseteq\Xi(\ker\widetilde\chi)\subseteq C_{S_n}(\bar x)$ は**両端が一致して閉じる**:
> $$\boxed{\ \Xi(\ker\widetilde\chi)=C_{S_n}(w)=\mathrm{Stab}(\bar x)\qquad(p=s=0\ \text{の窓}).\ }$$
> **⟹ この族では予想 CENT は定理であり、飽和も剛性も不要。同時に PRUNE は(刈り込みが一切起きないので)証明つきで反証される。**
> **証明.** $w=(w^2)^{(\ell+1)/2}$ ゆえ $C(w^2)\subseteq C(w)$、逆は自明。∎

既存窓では `W-E-A10-9t1`($w=(9,1)$)がこの族で、実測 $\lvert\ker\rvert=9=\lvert\mathrm{Stab}\rvert$ ✓。

### 10.6.4 **W-CENT-B(n=18)— 判別窓の witness(実物)**

$\ell=9$、$(r,t)=(2,0)$、$p=s=0$、$w_0=(9,9)$。TRI: $\mathrm{ord}(w)=9\ge7$ ✓。$T_{\rm trans}=5292=32.67\lvert C\rvert$(軌道が豊富)。
**局所探索**(`sat_l1_probe12.g`・下記 10.6.6)で witness を取得、`sat_l1_probe13.g` で全点検:

```
a1 = ( 1, 2)( 3, 4)( 5, 9)( 6,18)( 7,15)( 8,10)(11,14)(16,17)     [2^8 1^2, 偶 => eps=0]
b1 = ( 2, 9, 4)( 5, 8,18)( 6,17,15)( 7,14,10)(11,13,12)           [3^5 1^3]
```

| 検査 | 結果 |
|---|---|
| $a_1^2=b_1^3=1$、$b_1^{-1}a_1=w_0=(9,9)$、$\langle a_1,b_1\rangle=A_{18}$ | ✓ |
| braid・$c=1$・$P=\langle\bar x,\bar y\rangle=A_{18}$・$\lvert E\rvert=6\lvert A_{18}\rvert$ | ✓ |
| Ree $10{+}8{+}2=20=n{+}2$(種数 0)・$N_{\rm ord}=9$・$c_m=6$ | ✓ |
| $C(w)=C(w^2)=\mathrm{Stab}=C_9\times D_{18}$(位数 **162**) | ✓(定理 CENT-0 適用可) |
| SURV 構成 162 個が**全て** hexagon (3.3)(3.4) + 全射を通過(落ち 0) | ✓ |
| $\Xi(\ker\widetilde\chi)=\mathrm{Stab}$、位数 **162** | ✓ |

> **$\lvert\Xi(\ker\widetilde\chi)\rvert=162$。PRUNE の予測は $18$ — 9 倍差で、しかも測定でなく証明として決着。**
> ($\mathrm{Stab}=C_9\times D_{18}$、$O_{2'}=C_9\times C_9$、$S=\mathrm{Syl}_2=C_2$、$C_{O_{2'}}(S)=$ 対角 $C_9$ ⟹ PRUNE は $9\cdot2=18$。実際は刈り込みゼロ。)
> **CENT-ORD の $\ell^{\,r-p}=9^{2-0}=81$**(奇部)も一致 ✓($\mathrm{Syl}_3(C_9\times D_{18})=C_9\times C_9=81$)。$s_2$ 律は $9^{s_2(2)}=9$ — **これも 9 倍差で決着**。

### 10.6.5 **P-WALL-2(n=24)— 壁 P4 到達**

$\ell=19$(素数)、$(r,t)=(1,5)$、$p=s=0$、$w_0=(19,1^5)$、$\bar x=w_0^2$ も同型。

**設計が事前に閉じる 3 段(すべて紙)**:
1. **推移性が自動**: Ree より $(k,j)=(12,8)$ 一択で $a_1,b_1$ とも**不動点なし** ⟹ 各軌道長は 2 でも 3 でも割れる ⟹ $\equiv0\ (\mathrm{mod}\ 6)$。軌道は $w_0$ の巡回の合併ゆえ長さ $19+a$($0\le a\le5$)、$19+a\equiv0\ (6)\Rightarrow a=5$ ⟹ **全 24 点が 1 軌道**。
2. **原始性が自動**: ブロック長 $b\mid24$、$b\ge2$ なら ブロック数 $\le12<19$ ゆえ 19-巡回はブロックを固定 ⟹ ブロックは 19-軌道を丸ごと含む ⟹ $b\ge19$、矛盾。
3. **Jordan**: 原始 + 素数長 $19\le n-3=21$ の巡回 ⟹ $\langle a_1,b_1\rangle\supseteq A_{24}$。

**⟹ 存在判定 = 指標係数 1 個の正値性。** `sat_l1_probe9.g`:
$$\#\{(a_1,b_1):\ a_1\in 2^{12},\ b_1\in3^{8},\ b_1^{-1}a_1=w_0\}=\mathbf{2280}=\lvert C_{S_{24}}(w_0)\rvert\ \Longrightarrow\ \text{軌道数}=1.$$

**witness(局所探索が restart 11・step 568 で取得)**:
```
a1 = ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23)
b1 = ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23)
```
`sat_l1_probe11.g` の全点検: $\langle a_1,b_1\rangle=A_{24}$ ✓、braid・$c=1$・$P=A_{24}$・$\lvert E\rvert=6\lvert A_{24}\rvert$ ✓、Ree $12{+}8{+}6=26=n{+}2$(種数 0)✓、$N_{\rm ord}=19$・$c_m=18$ ✓、$\mathrm{sgn}(a_1)=+1$($\varepsilon=0$)✓。

> ### 結論 WALL【SURV+ と定理 CENT-0 から従う・機械全点検つき】
> $$C_{S_{24}}(w_0)=C_{19}\times S_5\ (\text{位数 }2280,\ \textbf{非可解}),\qquad \Xi(\ker\widetilde\chi)=\mathrm{Stab}(\bar x)=C_{19}\times S_5 .$$
> SURV で構成した **2280 個の $f_z$ がすべて** hexagon (3.3)(3.4)($m=0$)と全射性を通過(落ち 0・`probe11`)。全射 ⟹ 有限群の全射自己準同型は自己同型 ⟹ **settled も自動**。
> $$\boxed{\ \ker\widetilde\chi\ \text{は非可解群}\ C_{19}\times S_5\ \text{を商にもつ}\ \Longrightarrow\ \mathrm{GTSh}(N,N)\ \text{は非可解}.\ }$$
> **飽和も剛性も $\Xi$ 単射も不要**(下限側のみ使用)。**悉皆走査($\sim10^{12}$)も乱択($10^{-10}$)も不要。**

**司令塔 candidate(裁定 238 追記)の $r=5$・$w=(5^5)$ は定理 TRI で不可だったが、壁の本質($C(w)\supseteq S_5$)は「$w$ が 5 個の等長巡回をもつ」ことであり、その 5 個を**不動点**に取れば $\ell$ を 1 本にできる** — これが P-WALL-2 の発想。$n$ も 27 → **24** に下がり、しかも存在が紙で閉じた。

### 10.6.6 構成法(乱択の廃止)— 2-opt 山登り

$w_0$ を固定し、$a_1$ を「$2k$ 点上の完全マッチング」として、
$$\mathrm{defect}(a_1):=\bigl\lvert\mathrm{supp}\bigl((a_1w_0^{-1})^3\bigr)\bigr\rvert$$
を目的関数に 2 辺張り替え(2-opt)の山登り+ランダム再出発。**乱択が $10^{-10}$ の窓でも数秒**:

| 窓 | 空間の大きさ | 乱択 hit 率 | 局所探索 |
|---|---|---|---|
| n=24 P-WALL-2 | $\lvert2^{12}\text{ 類}\rvert=3.2\times10^{11}$ | $7\times10^{-9}$ | **restart 11 / step 568** |
| n=18 W-CENT-B | — | — | **restart 3 / step 273** |
| n=14 候補 A | — | — | hit するが $\langle a_1,b_1\rangle$ が真部分群(6 軌道のうち非生成のものを引いた)— 再走行で可 |

**⟹ 「計数してから構成する」の実装形: ①指標係数で存在判定 → ②2-opt で witness → ③窓 assert → ④SURV で shadow を全部作る。**

### 10.6.7 配達覚書への訂正(3 点・軽微)

`docs/notes/litgate_rigidity_hurwitz_v1.md` は総じて正確。訂正・補足は次の 3 点:

1. **§3.1「指標和 1 本で事前判定できる」は条件つきで正しい**。分解数 $>0$ は存在の**必要条件**だが十分ではない(n=10・n=12 がまさに「分解数 $>0$ だが生成しない」)。**ただし不動点なし+素数長巡回の設計では推移性・原始性・Jordan が自動になり、そこでは「分解数 $>0$ ⟺ 窓が存在」が**厳密に成立**する(P-WALL-2 が実例)。設計をこの形に寄せるのが要点。
2. **§2 の Hall 1936(部分群格子の Möbius)は本件では過剰**。推移性の差し引きだけなら**$w_0$ の巡回の集合分割上の Möbius**で閉じる(§10.6.2)。部分群格子が要るのは「推移だが $A_n$ でない」分の除去だが、設計側で Jordan を効かせればその項は消える。
3. **§1.1 Liu–Osserman の適用不可判定は正しい**。P-WALL-2 は $w_0=(19,1^5)$ が単一巡回型だが $a_1=2^{12}$・$b_1=3^8$ は pure-cycle でない ⟹ やはり直接適用外。**手法だけ輸入**という覚書の判断を支持する。

なお §4 の警戒(braid 軌道 / $C(w_0)$-軌道 / Nielsen 類を束ねない)は妥当。本稿の $N$ は一貫して **$C_{S_n}(w_0)$-共役軌道数**である。

---

## 11. 格付け表(本稿の全主張・再掲)

| 主張 | 格 |
|---|---|
| 観察 1.1($\Delta=a$、$\delta=b$) | **proof**(2 行)+ 機械 |
| **定理 RED**(§2) | **定理**(紙上完全証明 + 2 窓で集合一致) |
| 平行移動公式 SAT-L1′(§3.2) | **proof** + 機械 |
| **SAT-L1 = 偽**(§3.3) | **反証(proof)** + 明示反例 |
| 非可換 $H^1$ 枠組み(§3.4) | **proof**(定義の言い換え) |
| **補題 SAT-T1**(§4) | **定理**(初等・完結) |
| **定理 SURV**(§5) | **定理**(構成的) |
| 系 SURV-2(生成条件) | **11 窓 measured**・紙は【GAP-S1】 |
| **定理 SAT-RIG**(飽和 ⟺ 剛性・自由作用・$\lvert\ker\rvert=\lvert C\rvert\cdot N$)(§6.2) | **定理**(還元は完全) |
| **予想 CENT**($\ker\widetilde\chi\cong C_{S_n}(w)$)(§6) | **candidate**($\supseteq$ 定理・$\subseteq$ = 剛性未証明)。**11/11 窓 machine-measured**(位数)・**2 窓で構造文字列一致** |
| $w$ の型が $(2\ell)^p(\ell)^{r-2p}(2)^s(1)^{t-2s}$ に限る(§7.5.1) | **proof**(1 行: $L$ 奇なら $L\in\{\ell,1\}$、$L$ 偶なら $L/2\in\{\ell,1\}$) |
| **予想 CENT-ORD**(閉じた位数公式・奇部 $\ell^{r-p}$)(§7.5.1) | **candidate**・**11/11 窓一致**(位数と $\mathrm{sgn}(a_1)$ の両方) |
| 境界変数 = $p$、$r$/$\mathrm{Syl}_2(S_r)$ 非可換性説の棄却(§7.5.2) | **CENT-ORD 依存の帰結**(CENT-ORD が candidate ゆえ同格)。ただし $s_2$ 律の反証自体は実データで確定 |
| ~~**予言 P-CENT-1**~~(§7.5.3) | **撤回**(§10.5.2 定理 TRI により**窓が存在しない**。司令塔の全数走査陰性と一致) |
| **定理 SURV+**($\Xi(f_z)=z^{a_1}$、$C_{S_n}(w)\subseteq\Xi(\ker)\subseteq C_{S_n}(\bar x)$)(§10.5.1) | **定理**(2 行)+ 4 窓機械確認 |
| **定理 TRI**(三角群ゲート・$\mathrm{ord}(w)\ge7$ が必要)(§10.5.2) | **定理**(古典的事実 $\Delta(2,3,5)\cong A_5$ に依拠・$m\le5$ の位数は機械確認) |
| $s=1$ トリック($w^\ell=$ 互換 ⟹ 原始性で $S_n$ 確定)(§10.5.3) | **proof**(Jordan 型の古典事実) |
| **予言 P-CENT-2**($n{=}12$・$w=(5,5,2)$ で $\lvert\ker\rvert=100$ vs PRUNE $20$)(§10.5.4) | **凍結候補**(設計点検済・存在探索は $62{,}370$ 個の全数走査) |
| **設計 P-WALL-1**($n{=}27$・$w=(5^5,2)$ ⟹ 非可解核)(§10.5.5) | **設計 candidate**。ただし**非可解性の主張自体は SURV+ から下限として従う**(飽和・剛性は不要) |
| 「境界は $r=4$」の機構の訂正(§10.5.6) | $r=4$ が最初の判別点なのは**正しい**(定理 TRI + $2p\le r$ による強制)。「$\mathrm{Syl}_2(S_r)$ 非可換性が原因」は**棄却** |
| 3840 障害 $=2^5{:}S_5$、推移だが**非原始**(§10.6.1) | **同定完了**(悉皆再現 + ブロック系) |
| $s=1$ トリック(§10.5.3 ゲート④)| **単独の設計原理としては撤回**(原始性は自動でない・n=12 が反例)。条件文自体は真 |
| 計数機構(Frobenius + 巡回集合分割 Möbius)(§10.6.2) | **実装・11 窓較正済**。司令塔の悉皆値(50・100)を厳密再現 |
| **定理 CENT-0**($p=s=0$ ⟹ $\Xi(\ker)=C_{S_n}(w)=\mathrm{Stab}$)(§10.6.3) | **定理**(2 行・挟み撃ちの閉包)。**この族で CENT は証明済・PRUNE は証明つきで反証** |
| **W-CENT-B**(n=18・witness 実物・$\lvert\Xi(\ker)\rvert=162$ vs PRUNE 18)(§10.6.4) | **窓 assert + 162 shadow 全数検算(GAP 単系統)**。CENT-0 により結論は定理 |
| **P-WALL-2**(n=24・witness 実物・$\Xi(\ker)=C_{19}\times S_5$ 非可解)(§10.6.5) | **窓 assert + 2280 shadow 全数検算**。⟹ **$\mathrm{GTSh}(N,N)$ 非可解**(下限のみ・飽和/剛性/単射性 不要) |
| 存在判定 = 指標係数の正値性(不動点なし+素数長巡回の設計)(§10.6.5) | **proof**(推移性・原始性・Jordan の 3 段) |
| 2-opt 山登りによる witness 構成(§10.6.6) | **手法**(n=24 で数秒・乱択 $10^{-9}$ を代替) |
| PRUNE / 系 PRUNE-1 / Stab 律 | **棄却**(§8) |
| 定理 PRUNE-FIX | **無傷だが核とは無関係**(§8) |
| $m\ne0$ 層の一般公式(§9.1) | **candidate・未検証** |
| $\Xi$ 単射 | **UNKNOWN**(本稿は触れていない) |
