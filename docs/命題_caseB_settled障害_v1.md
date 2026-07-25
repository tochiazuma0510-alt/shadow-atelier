# 命題 B — case B(outer 窓)の settled 障害機構と非 isolated 性【紙上証明・新規】

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 07 の任務 3**。
埋める対象: `docs/week3-PSL封印計算_opus_v1.md` §6 の **【GAP-06b】**(「case B の settled ⟺ u ≡ ±1 mod 2k は k=5 でしか機構が説明できない。k=4, 6 では未解明」)。
副産物として **【GAP-06c】**(命題 R の推移性)と **【GAP-06a】**(case A の群同型)にも決着をつける。

> ### ⚠ 開示区分
> 本稿は **sealed 側の数学的根拠**(settled 数・isolated の予測値)を含む。**implementer へ渡してはならない**。読者は司令塔・Sol・研究者に限る。封印 PSL_v1(SHA-256 D696AC9E…B28C141B・金庫)の値そのものは本稿では再掲せず、**構造式**として述べる。

**状態札**

| 内容 | 札 |
|---|---|
| 補題 B1〜B6・定理 B | **紙上証明**(私の単系統起草・未監査)。便 10 で Sol 監査へ |
| §7 の数値 | **私の第三独立実装(node・行列)による計算確認**。GAP 実装との突合は未了 ⇒ **cross-checked ではない**・**verified でもない** |
| 【GAP-B7】 | 補題 B6 の一般化(反射 witness の存在)は 7 窓で計算確認・**一般証明は未了** |
| genuine / arithmetical | **一切主張しない**(W28) |

---

## 0. 結論(先に 5 行)

1. **settled の判定は $X$(位数 $k$)ではなく $\bar\sigma_1$ の $\hat G$-成分 $w$(位数 $e$)の上で読まねばならない**(補題 B2)。case A は $\langle w\rangle = \langle X\rangle$ なので両者が一致するが、**case B は $\langle X\rangle \subsetneq \langle w\rangle$(指数 2)であり、その 1 段の差が障害の座**である。
2. 障害の正体は **冪部分群** $\mathfrak P := \mathrm{Im}\bigl(N_{\mathrm{Aut}(\hat G)}(\langle w\rangle) \to (\mathbb Z/e)^\times\bigr)$ である(定理 B3)。**settled $\Rightarrow u \bmod e \in \mathfrak P$。**
3. case B では $\hat G = \tilde A = \mathrm{PGL}(2,p)$ が **complete**($\mathrm{Aut} = \mathrm{Inn}$)であり、$\langle w\rangle$ は**自己中心化的な極大トーラス**で **Weyl 群 $C_2$ が反転のみ**を実現する。ゆえに $\mathfrak P = \{\pm1\}$ — **これが k = 4, 5, 6 を一つの理由で説明する**。
4. 各繊維は **settled 全部か全く無しか**の二択である(定理 B6: $\#\text{settled}(m) \in \{0, e\}$)。ゆえに
 $$ |\mathrm{GTSh}(N,N)| \;=\; |\mathfrak P|\cdot e \;=\; \bigl|N_{\mathrm{Aut}(\hat G)}(\langle w\rangle)\bigr|,\qquad |\mathrm{GT}(N)| \;=\; \varphi(2k)\cdot e. $$
5. ゆえに **case B の対象は常に非 isolated**(定理 B): $\mathfrak P=\{\pm1\}$ かつ許容条件 $e = 2k \ge 7$ から $k \ge 4$、$\varphi(2k) \ge 4 > 2 = |\mathfrak P|$。**「予測」ではなく定理**になった。さらに $\mathrm{GTSh}(N,N) \cong D_{4k}$(位数 $4k$ の二面体群)。

> ★ **v1 の自認**: 委嘱 06 v1 §4.4 で私は k=5 の障害を「$N_{\mathrm{Aut}(G)}(\langle X\rangle)\to(\mathbb Z/5)^\times$ が非全射」と説明した。**結論は正しいが座が誤っていた** — k=4, 6 では $(\mathbb Z/k)^\times$ への写像は**全射**である(§6 の表)。正しい座は $\langle w\rangle$ である。

---

## 1. 設定と記法

`docs/week3-PSL封印計算_opus_v1.md` の定理 M1–M3・補題 N を前提とする。$G$ は有限非可換単純群、$N$ は $c \in N$ なる許容対象、$P := PB_3/N \cong G$、$Q := B_3/N$($|Q| = 6|G|$)。定理 M2 により許容 marking は 2 型:

| | **case A(split-inner)** | **case B(outer)** |
|---|---|---|
| $Q$ | $G \times S_3$ | $\tilde A \times_{C_2} S_3$($\tilde A := \mathrm{Aut}_2(G)$、$[\tilde A:\mathrm{Inn}\,G] = 2$) |
| 周囲群 $\hat G$ | $G$ | $\tilde A$ |
| $\bar\Delta$ | $(s,\zeta_\Delta)$、$s \in G$、$s^2=1$ | $(s,\zeta_\Delta)$、$s \in \tilde A\setminus\mathrm{Inn}\,G$、$s^2=1$ |
| $\bar\delta$ | $(t,\zeta_\delta)$、$t \in G$、$t^3=1$ | 同左($t$ は内部) |
| $w := t^{-1}s$ | $\in G$、$e := \mathrm{ord}(w) = k$(奇) | $\in \tilde A\setminus\mathrm{Inn}\,G$、$e = 2k$ |

共通の記号: $\bar\sigma_1 = \bar\delta^{-1}\bar\Delta = (w,\zeta_1)$、$\bar\sigma_2 = \bar\Delta\bar\sigma_1\bar\Delta^{-1} = (w_2,\zeta_2)$ で $w_2 = st^{-1}$、$X := w^2$、$Y := w_2^2 = sXs^{-1} = tXt^{-1}$、$k = N_{\rm ord} = \mathrm{ord}(X)$、$u := 2m+1$、$\theta = \mathrm{Ad}(s)$、$\tau = \mathrm{Ad}(t)$。
$\zeta_1,\zeta_2$ は $S_3$ の**相異なる互換**、$\zeta_\delta$ は 3-サイクル。

**繊維**: $\mathfrak F_m := \{f \in A = [P,P] = G : (\text{H-a}) \wedge (\text{H-b}') \wedge \langle X^u, f^{-1}Y^uf\rangle = G\}$、$n_m := |\mathfrak F_m|$。
補題 N より $n_m = N_{\hat G}(w^u) = \#\{(r,g) \in T_3(\hat G)\times T_2(\hat G) : rg = w^u\}$。ここで $g := sf$、$r := w^u g$ と置く(以下つねにこの $g, r$ を使う)。

**settled の定義**(定義ノート §2): $\ker(T_{m,f}) = N$。$T_{m,f}: B_3 \to B_3/N$、$\sigma_1 \mapsto \bar\sigma_1^{\,u}$、$\sigma_2 \mapsto \bar f^{-1}\bar\sigma_2^{\,u}\bar f$。

---

## 2. 補題 B1 — $\mathrm{Aut}(Q)$ の決定

> **補題 B1.** case A / case B のいずれにおいても
> $$ \mathrm{Aut}(Q) \;\cong\; \mathrm{Aut}(\hat G)\times\mathrm{Aut}(S_3), $$
> であり、この同型は $Q \le \hat G\times S_3$ 上への**成分別作用**として実現される。

**証明.** $P \cong G$ は $Q$ の**唯一の非可解極小正規部分群**である($Q/P \cong S_3$ は可解、$G$ は非可換単純)。ゆえに $P$ は $Q$ の特性部分群。また $C := C_Q(P)$ も特性部分群であり、
- case A: $C = 1\times S_3$、$Q = P\times C$、$G$ と $S_3$ に共通の直積因子がないので $\mathrm{Aut}(Q) = \mathrm{Aut}(G)\times\mathrm{Aut}(S_3)$。
- case B: $C_{\tilde A}(\mathrm{Inn}\,G) = Z(\tilde A) = 1$ より $C = 1\times A_3 \cong C_3$。$Q/C \cong \tilde A$、$Q/P \cong S_3$、$C\cap P = 1$ ゆえ標準写像 $Q \hookrightarrow (Q/C)\times(Q/P) = \tilde A\times S_3$ は単射で、像は fiber product $\tilde A\times_{C_2}S_3$。任意の $\beta \in \mathrm{Aut}(Q)$ は $P, C$ を保つので両商上に自己同型 $\beta_{\tilde A}, \beta_{S_3}$ を誘導し、埋め込みと可換だから $\beta = (\beta_{\tilde A},\beta_{S_3})|_Q$。逆に任意の対 $(\alpha,\gamma) \in \mathrm{Aut}(\tilde A)\times\mathrm{Aut}(S_3)$ は fiber product 条件 $\pi(a) = \mathrm{sgn}(\sigma)$ を保つ($\alpha$ は $\mathrm{Inn}\,G$ を保つので $\pi\circ\alpha = \pi$、$\mathrm{Aut}(S_3) = \mathrm{Inn}(S_3)$ なので $\mathrm{sgn}\circ\gamma = \mathrm{sgn}$)ので $Q$ を保つ。∎

> ★ 副産物: case B では $|\mathrm{Aut}(Q)| = 12|G| = 2|Q|$ ゆえ $\mathrm{Out}(Q) \cong C_2$。case A では $|\mathrm{Aut}(Q)| = |\mathrm{Aut}(G)|\cdot 6$。

---

## 3. 補題 B2 — settled の判定式(**正しい座**)

> **補題 B2.** $[m,f] \in \mathrm{GT}(N)$ について
> $$ \boxed{\ [m,f]\ \text{settled} \iff \exists\,\alpha \in \mathrm{Aut}(\hat G):\quad \alpha(w) = w^{u}\ \ \wedge\ \ \alpha(w_2) = f^{-1}w_2^{\,u}f\ } $$
> しかもこの $\alpha$ は存在すれば**一意**である。

**証明.** $T_{m,f}$ は全射(shadow の定義)で $|\ker T_{m,f}| = |N|$。ゆえに
$$ \text{settled} \iff \ker T_{m,f} = N \iff T_{m,f}\ \text{が}\ Q\ \text{の自己同型}\ \beta\ \text{を誘導する}. $$
補題 B1 で $\beta = (\alpha,\gamma)$ と書く。$u$ は奇数なので $\zeta_i^u = \zeta_i$、また $\bar f = (f,1)$ は $S_3$ 成分に効かないから、$\beta(\bar\sigma_1) = \bar\sigma_1^u$ と $\beta(\bar\sigma_2) = \bar f^{-1}\bar\sigma_2^u\bar f$ の $S_3$ 成分は
$$ \gamma(\zeta_1) = \zeta_1,\qquad \gamma(\zeta_2) = \zeta_2. $$
$\mathrm{Aut}(S_3) = \mathrm{Inn}(S_3)$ と $\zeta_1\ne\zeta_2$(相異なる互換)から $\gamma \in C_{S_3}(\zeta_1)\cap C_{S_3}(\zeta_2) = \langle\zeta_1\rangle\cap\langle\zeta_2\rangle = 1$。残る $\hat G$ 成分が主張の 2 式である。
**一意性**: $\alpha,\alpha'$ が両式を満たせば $\alpha^{-1}\alpha'$ は $w$ と $w_2$ を固定する。$\langle\bar\sigma_1,\bar\sigma_2\rangle = Q$ ゆえ $\langle w,w_2\rangle = \hat G$、したがって $\alpha^{-1}\alpha' = \mathrm{id}$。∎

> **系 B2-a(case A では $X$ で読んでよい).** case A では $e = k$ は奇数で $w = X^{(k+1)/2} \in \langle X\rangle$、$X = w^2$ ゆえ $\langle w\rangle = \langle X\rangle$ かつ
> $$ \alpha(w) = w^u \iff \alpha(X) = X^u,\qquad \alpha(w_2)=f^{-1}w_2^uf \iff \alpha(Y)=f^{-1}Y^uf. $$
> (⇐ は $2j\equiv1 \bmod k$ なる $j$ で $\alpha(w) = \alpha(X)^j = X^{uj} = w^{2uj} = w^u$。)**これが委嘱 06 v1 で用いた判定式**であり、case A では正しい。
>
> **系 B2-b(case B では $X$ で読んではいけない).** case B では $\langle X\rangle = \langle w^2\rangle$ は $\langle w\rangle$ の**指数 2 の部分群**であり、$\alpha(X)=X^u$ から $\alpha(w)=w^u$ は**出ない**。実際 §6 の表のとおり、$k=4,6$ では $(\mathbb Z/k)^\times$ 側に障害がないのに settled は落ちる。

---

## 4. 定理 B3 — 障害(冪部分群 $\mathfrak P$)

> **定義.** $\displaystyle \mathfrak P \;:=\; \bigl\{\,j \in (\mathbb Z/e)^\times \ :\ \exists\alpha\in\mathrm{Aut}(\hat G),\ \alpha(w)=w^{\,j}\,\bigr\} \;=\; \mathrm{Im}\Bigl(N_{\mathrm{Aut}(\hat G)}(\langle w\rangle)\longrightarrow(\mathbb Z/e)^\times\Bigr).$
> これは $(\mathbb Z/e)^\times$ の**部分群**であり、$\bigl|N_{\mathrm{Aut}(\hat G)}(\langle w\rangle)\bigr| = |\mathfrak P|\cdot\bigl|C_{\mathrm{Aut}(\hat G)}(w)\bigr|$。

$\alpha$ が $\langle w\rangle$ を正規化するのは $\gcd(j,e)=1$ ゆえ $\langle w^j\rangle=\langle w\rangle$ だからであり、核は $C_{\mathrm{Aut}(\hat G)}(w)$ である。

> **定理 B3(障害).** $[m,f]$ settled $\Longrightarrow$ $u \bmod e \in \mathfrak P$。

**証明.** 補題 B2 の第一式そのもの。∎

> **定理 B3′(case B での $\mathfrak P$ の決定).** $G = \mathrm{PSL}(2,p)$($p$ 素数 $\ge 5$)、$\tilde A = \mathrm{PGL}(2,p)$、$w \in \tilde A\setminus G$ が位数 $e = p\mp1$($=$ 極大トーラスの位数)ならば
> $$ \boxed{\ \mathfrak P = \{\pm 1\}\ }. $$

**証明.** 三段。
1. **$\mathrm{Aut}(\tilde A) = \mathrm{Inn}(\tilde A)$**: $p$ 素数 $\ge5$ で $\mathrm{PGL}(2,p)$ は complete(中心自明かつ外部自己同型なし)。ゆえに $\alpha$ は $\tilde A$ 内の共役に限られる。
2. **$\langle w\rangle$ は自己中心化的な極大トーラス**: $w$ は正則半単純($\bar{\mathbb F}_p$ 上の固有値比が位数 $e>2$)なので $C_{\tilde A}(w) = T := \langle w\rangle$、$|T| = e$。
3. **Weyl 群は反転のみ**: $\alpha = \mathrm{Ad}(h)$ が $w\mapsto w^j$($\gcd(j,e)=1$)を与えるなら $hTh^{-1} = hC(w)h^{-1} = C(w^j) = T$ ゆえ $h \in N_{\tilde A}(T)$。$\mathrm{PGL}(2,p)$ では $N_{\tilde A}(T)/T \cong C_2$ が**反転**で作用する($N_{\tilde A}(T) \cong D_{2e}$ — **本稿では $D_n$ は位数 $n$ の二面体群**)。ゆえに $j \equiv \pm1$。逆に $j = \pm1$ は実現される。∎

> **系 B3-a(charming 層と $u \bmod 2k$ の全単射).** $m \in \mathcal X_N \subseteq \mathbb Z/k$、$u = 2m+1$ とすると $u$ は奇数で、charming 条件 $\gcd(u,k)=1$ は $\gcd(u,2k)=1$ と同値。ゆえに
> $$ \mathcal X_N \longrightarrow (\mathbb Z/2k)^\times,\qquad m\longmapsto u \bmod 2k $$
> は**全単射**であり $|\mathcal X_N| = \varphi(2k)$。
> したがって **case B($e = 2k$)では、定理 B3 + B3′ から settled になり得るのは**
> $$ u \equiv \pm1 \pmod{2k}\quad\Longleftrightarrow\quad m \in \{0,\ k-1\} $$
> **のちょうど 2 層だけ**である。**これが k = 4 と k = 6 の未解明部分の答えである**(k = 5 も同じ理由に統合される)。

---

## 5. 補題 B4–B6 — 繊維は「全部 settled」か「全く無し」か

> **補題 B4(settled は繊維の不変量).** $h \in C_{\hat G}(w^u) = \langle w\rangle$、$f' := \theta(h)\,f\,h^{-1}$ とする。$[m,f]$ が witness $\alpha=\mathrm{Ad}(a)$ で settled なら $[m,f']$ は witness $\mathrm{Ad}(ha)$ で settled。逆も同様。

**証明.** $s^{-1}w_2s = s^{-1}(sws^{-1})s = w$ に注意すると($w_2 = sws^{-1}$)、
$$ \theta(h)^{-1}w_2^{\,u}\theta(h) \;=\; s\,h^{-1}\bigl(s^{-1}w_2^{\,u}s\bigr)h\,s^{-1} \;=\; s\,h^{-1}w^{u}h\,s^{-1} \;=\; s\,w^{u}s^{-1} \;=\; w_2^{\,u} $$
($h \in C(w^u)$)。ゆえに
$$ f'^{-1}w_2^{\,u}f' \;=\; h\bigl(f^{-1}w_2^{\,u}f\bigr)h^{-1} \;=\; h\bigl(a\,w_2\,a^{-1}\bigr)h^{-1} \;=\; (ha)\,w_2\,(ha)^{-1}, $$
また $(ha)w(ha)^{-1} = h\,w^u\,h^{-1} = w^u$。∎

> **補題 B5(繊維上の $\langle w\rangle$-作用は自由).** $f \in \mathfrak F_m$、$g = sf$、$r = w^ug$ とすると $\langle r,g\rangle = \hat G$。ゆえに $f$ の固定化群は
> $$ \{h\in\langle w\rangle : \theta(h)fh^{-1}=f\} \;=\; \langle w\rangle\cap C_{\hat G}(g) \;\subseteq\; C_{\hat G}(\langle g,r\rangle) \;=\; Z(\hat G) \;=\; 1. $$

**証明.** まず固定化群の形: $\theta(h)fh^{-1}=f \iff shs^{-1} = fhf^{-1} \iff f^{-1}s \in C_{\hat G}(h)$。$g = sf$、$s^2=1$ より $g^{-1} = f^{-1}s$、ゆえに条件は $h \in C_{\hat G}(g)$。$h \in \langle w\rangle = C(w^u)$ と合わせて $h \in C(g)\cap C(w^u) = C(\langle g, w^u\rangle) = C(\langle g,r\rangle)$($r = w^ug$)。
次に $\langle r,g\rangle = \hat G$: 対 $(s',t') := (g,\ r^{-1})$ は $t'^{-1}s' = rg = w^u$ を満たす marking であり、$X' := (w^u)^2 = X^u$、$Y' := s'X's'^{-1} = gX^ug^{-1}$。定理 M3(iii) を $(s',t')$ に適用すると $\langle s',t'\rangle = \hat G \iff \langle X',Y'\rangle = G$。ここで $g^{-1} = f^{-1}s$ より
$$ \langle X^u,\ gX^ug^{-1}\rangle \;=\; g\,\bigl\langle g^{-1}X^ug,\ X^u\bigr\rangle\,g^{-1} \;=\; g\,\bigl\langle X^u,\ f^{-1}Y^uf\bigr\rangle\,g^{-1} $$
($g^{-1}X^ug = (f^{-1}s)X^u(sf)^{-1\,-1}\!$ を展開すると $f^{-1}(sX^us^{-1})f = f^{-1}Y^uf$)。したがって $\langle r,g\rangle = \hat G$ は **shadow の生成条件 $\langle X^u,f^{-1}Y^uf\rangle = G$ と同値**であり、$f \in \mathfrak F_m$ なら成立する。$\hat G$ は $G$ 単純非可換 or $\tilde A$ で $Z(\hat G)=1$。∎

> **系 B5-a(【GAP-06c】の閉鎖 — 命題 R の推移性).** 補題 B5 より $\langle w\rangle$($\cong C_e$)の $\mathfrak F_m$ 上の作用は自由で、各軌道の大きさは $e$。補題 N の類積計算が $n_m = e$ を与えるとき、$\mathfrak F_m$ は**単一軌道 = $C_{\hat G}(\hat v_m)$-torsor** である。**これは計数からの逆算ではなく、自由性(紙)+ 個数(類積公式)からの正当な帰結**である。

> **定理 B6(二択).** $\#\{f\in\mathfrak F_m : [m,f]\ \text{settled}\} \in \{0,\ e\}$。とくに $n_m = e$ のとき、繊維は**全部 settled か、全く settled でないか**のどちらかである。

**証明.** 補題 B4 より settled 集合は $\langle w\rangle$-安定、補題 B5 より作用は自由 ⇒ $e \mid \#\text{settled}$。一方 $\#\text{settled} \le n_m = e$。∎

> **補題 B7($u\equiv\pm1$ は実際に実現される).**
> **(i) $m=0$($u=1$)**: $[0,1]$ は常に shadow($g=s$: $g^2=1$ ✔、$r = w\cdot s = t^{-1}ss = t^{-1}$: $r^3=1$ ✔、生成条件 $\langle X,Y\rangle=G$ ✔)であり、$\alpha=\mathrm{id}$ で **settled**。
> **(ii) $m=k-1$($u \equiv -1 \bmod 2k$)**: $[k-1,1]$ は常に shadow である。実際 $g = s$、$r = w^{-1}s = (s^{-1}t)s = sts$ で $r^3 = st^3s^{-1} = 1$ ✔、生成条件は $\langle X^{-1},Y^{-1}\rangle = \langle X,Y\rangle = G$ ✔。
> さらに
> $$ [k-1,1]\ \text{settled} \iff \exists\,a'\in\mathrm{Aut}(\hat G):\ a'(s)=s\ \wedge\ a'(t)=t^{-1} $$
> すなわち **marking $(s,t)$ と $(s,t^{-1})$ が $\mathrm{Aut}(\hat G)$-共役**であること。

**(ii) の導出.** $\bar\sigma_1 = \bar\delta^{-1}\bar\Delta$、$\bar\sigma_2 = \bar\Delta\bar\delta^{-1}$ より、$\beta(\bar\sigma_1)=\bar\sigma_1^{-1}=\bar\Delta\bar\delta$、$\beta(\bar\sigma_2)=\bar\sigma_2^{-1}=\bar\delta\bar\Delta$。$\beta(\bar\Delta)=\bar\Delta$、$\beta(\bar\delta)=\bar\Delta\bar\delta^{-1}\bar\Delta^{-1}$ と置くとこの 2 式は満たされる($\bar\Delta^2=1$ を使う)。$S_3$ 成分は $\gamma=1$ で整合($\zeta_\Delta\zeta_\delta^{-1}\zeta_\Delta = \zeta_\delta$)。$\hat G$ 成分は $a(s)=s$、$a(t)=\theta(t^{-1})=st^{-1}s$。$a' := \mathrm{Ad}(s)\circ a$ と置くと $a'(s)=s$、$a'(t)=t^{-1}$。∎

> ★ **解釈(★ 教材)**: $c\in N$ より $Q$ は $\mathrm{PSL}(2,\mathbb Z) = C_2 * C_3 = \langle\bar\Delta\rangle * \langle\bar\delta\rangle$ の商である。$\nu:\ \Delta\mapsto\Delta,\ \delta\mapsto\delta^{-1}$ は $\mathrm{PSL}(2,\mathbb Z)$ の**外部自己同型**($\mathrm{Out}(\mathrm{PSL}(2,\mathbb Z))=C_2$、$\mathrm{PGL}(2,\mathbb Z)$ の共役で実現)である。補題 B7(ii) は
> $$ [k-1,1]\ \text{settled} \iff \bar N := \ker\bigl(\mathrm{PSL}(2,\mathbb Z)\twoheadrightarrow Q\bigr)\ \text{が}\ \mathrm{PGL}(2,\mathbb Z)\ \text{でも正規} $$
> と言い換えられる。すなわち **$u=-1$ の settled 性は「対象が鏡映対称(実)か」という古典的な問い**である。$u=-1$ は $\widehat{GT}$ の複素共役に対応する層でもある。

**7 窓での確認 ✔(§7)**: $a'$ は**各窓でちょうど 1 個**存在する(一意性は補題 B2 の一意性と同じ理由)。構造的理由: $(s,t^{-1})$ に対応する $w' = (t^{-1})^{-1}s = ts = w_2^{-1}$ は $w$ と $\mathrm{Aut}(\hat G)$-共役($w_2 = sws^{-1}$、$w_2^{-1}\sim w_2$ は Weyl 反転)であり、これらの窓では marking の $\mathrm{Aut}$-軌道が $w$ の $\mathrm{Aut}$-類で決まる。**【GAP-B7】この最後の一歩(軌道 ↔ 類の全単射)は窓ごとの計算確認であって一般証明ではない。**

---

## 6. 定理 B — 主結果

> **定理 B.** 上記の設定(定理 M2 の case A / case B、$c\in N$、$n_m = e$ が全 charming $m$ で成立)の下で:
> $$ \boxed{\ |\mathrm{GT}(N)| = \varphi(2k)\cdot e,\qquad |\mathrm{GTSh}(N,N)| = |\mathfrak P|\cdot e = \bigl|N_{\mathrm{Aut}(\hat G)}(\langle w\rangle)\bigr|\ } $$
> かつ $\Psi: [m,f]\mapsto\alpha$(補題 B2)は $\mathrm{GTSh}(N,N)$ から $N_{\mathrm{Aut}(\hat G)}(\langle w\rangle)$ への**全単射**であり、$\mathrm{GTSh}$ の合成が $\mathrm{Aut}$ の合成に対応するので**群の(反)同型**である。したがって
> $$ \mathrm{GTSh}(N,N)\ \cong\ N_{\mathrm{Aut}(\hat G)}(\langle w\rangle),\qquad \text{isolated}\iff |\mathfrak P| = \varphi(2k). $$
>
> **(A)** case A($e=k$ 奇): $u\bmod 2k \leftrightarrow u\bmod k$ は同型 $(\mathbb Z/2k)^\times\cong(\mathbb Z/k)^\times$ ゆえ
> $$ \text{isolated}\iff \mathfrak P = (\mathbb Z/k)^\times \iff \bigl|N_{\mathrm{Aut}(G)}(\langle X\rangle)\bigr| = k\varphi(k), $$
> このとき $\mathrm{GT}(N) = \mathrm{GTSh}(N,N) \cong N_{\mathrm{Aut}(G)}(\langle X\rangle) \cong \mathrm{Hol}(\mathbb Z/k) = \mathbb Z/k\rtimes(\mathbb Z/k)^\times$。
> **(B)** case B($e=2k$、$\hat G=\mathrm{PGL}(2,p)$): 定理 B3′ より $\mathfrak P=\{\pm1\}$ ゆえ
> $$ |\mathrm{GTSh}(N,N)| = 2e = 4k,\qquad \mathrm{GTSh}(N,N)\cong N_{\tilde A}(\langle w\rangle)\cong D_{4k}\ (\text{位数 }4k\text{ の二面体群}), $$
> $$ \text{isolated}\iff \varphi(2k)=2 \iff 2k\in\{4,6\} \iff k\in\{2,3\}. $$
> **許容条件**(三角群の基本補題: $\Delta(2,3,e)$ の非可解全射商は $e\ge7$)から $e = 2k \ge 8$、すなわち $k\ge4$。ゆえに
> $$ \boxed{\ \textbf{case B の対象は常に非 isolated}\ } $$
> であり、settled 率はつねに $2/\varphi(2k)$。

**証明.** 定理 B6 より各繊維の settled 数は $0$ か $e$。定理 B3 より settled な層は $\{m : u\bmod e\in\mathfrak P\}$ に含まれる。逆に $u\bmod e\in\mathfrak P$ なら…
- $\mathfrak P$ は群で、$\Psi$ の像は $N_{\mathrm{Aut}(\hat G)}(\langle w\rangle)$ に含まれる。$\mathrm{GTSh}(N,N)$ は群(2401 Thm 3.10)で $\Psi$ は(反)準同型ゆえ、実現される $u$ の集合 $\bar U := \{u\bmod e\}$ は $\mathfrak P$ の**部分群**。
- case B: 補題 B7 より $1,-1\in\bar U$、定理 B3′ より $\bar U\subseteq\mathfrak P=\{\pm1\}$ ⇒ $\bar U=\mathfrak P$。
- case A: 補題 B7 より $\pm1\in\bar U$。$\mathfrak P=(\mathbb Z/k)^\times$ の窓では $\bar U=\mathfrak P$ を **§7 の計算で確認**(全 charming $m$ が settled)【GAP-B8: $\bar U=\mathfrak P$ の一般証明は未了 — 現状は「$\bar U\le\mathfrak P$ は紙、等号は窓ごとの計算」】。
以上より $|\mathrm{GTSh}(N,N)| = |\bar U|\cdot e = |\mathfrak P|\cdot e = |N_{\mathrm{Aut}(\hat G)}(\langle w\rangle)|$。$\Psi$ の単射性は §7 で全窓確認(位数一致と像の包含から全単射)。∎

---

## 7. 検算(第三の独立実装・node・行列演算のみ)

**スクリプトの所在**(セッション scratchpad・**恒久化は司令塔の判断**):
`C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier\3eff786b-decc-4c68-8490-58f1ecb38f9a\scratchpad\`
- `caseB_v2.mjs` — 繊維列挙・settled 判定・staged count(q=7,11)
- `caseB_v2b.mjs` — 自由性・推移性・反射 witness・$\mathrm{P\Gamma L}(2,8)$ 込みの全 7 窓
- `inj_v2.mjs` — 全 7 窓の $\mathfrak P$・$\lvert C_{\mathrm{Aut}}(w)\rvert$・$\lvert N_{\mathrm{Aut}}(\langle w\rangle)\rvert$・$\Psi$ の単射性
- `verify_v1_markings.mjs` — **封印 payload(v1 §5)の明示行列 $(S,T)$ の再検証**
- `control_v2.mjs` — W78 control 対($L_2(11)$ inner ord5 / outer ord10)
$\mathrm{PGL}(2,q)$ を **$\mathbb F_q$ 上の $2\times2$ 行列 mod scalars**(第一非零成分を 1 に正規化)として構成、$\mathbb F_8 = \mathbb F_2[x]/(x^3+x+1)$、$\mathrm{Aut}(\mathrm{PSL}(2,8)) = \mathrm{P\Gamma L}(2,8)$ は $(h,i): m\mapsto \mathrm{Frob}^i(hmh^{-1})$ で実装。**GAP も照合器も import していない。**

**封印 payload(v1 §5)の明示 marking $(S,T)$ をそのまま入力にして全項目を再現した** — 7 窓すべてで $\mathrm{ord}(S)=2$、$\mathrm{ord}(T)=3$、$\mathrm{ord}(w)=e$、$\mathrm{ord}(X)=k$、$XYZ=1$、$Y=tXt^{-1}=sXs^{-1}$、$\langle s,t\rangle=\hat G$、$\langle X,Y\rangle=G$ ✔。

| 窓 | case | $e$ | $k$ | $|C_{\mathrm{Aut}}(w)|$ | $|N_{\mathrm{Aut}}(\langle w\rangle)|$ | $\mathfrak P \subseteq (\mathbb Z/e)^\times$ | $\varphi(2k)$ | settled 層 | 自由 | 推移 | $\Psi$ 単射 |
|---|---|---:|---:|---:|---:|---|---:|---|:--:|:--:|:--:|
| S1 $L_2(7)$ | A | 7 | 7 | 7 | 42 | **全体**(6 元) | 6 | 全 6 層 | ✔ | ✔ | ✔ |
| S2 $L_2(7)$ | **B** | 8 | 4 | 8 | 16 | **$\{1,7\}$** | 4 | $m\in\{0,3\}$ | ✔ | ✔ | ✔ |
| S3 $L_2(8)$ | A | 7 | 7 | 7 | 42 | **全体**(6 元) | 6 | 全 6 層 | ✔ | ✔ | ✔ |
| S4 $L_2(8)$ | A | 9 | 9 | 9 | 54 | **全体**(6 元) | 6 | 全 6 層 | ✔ | ✔ | ✔ |
| S5 $L_2(11)$ | A | 11 | 11 | 11 | 110 | **全体**(10 元) | 10 | 全 10 層 | ✔ | ✔ | ✔ |
| S6 $L_2(11)$ | **B** | 10 | 5 | 10 | 20 | **$\{1,9\}$** | 4 | $m\in\{0,4\}$ | ✔ | ✔ | ✔ |
| S7 $L_2(11)$ | **B** | 12 | 6 | 12 | 24 | **$\{1,11\}$** | 4 | $m\in\{0,5\}$ | ✔ | ✔ | ✔ |

全窓で $|N_{\mathrm{Aut}}(\langle w\rangle)| = |\mathfrak P|\cdot e = \#\text{settled}$ ✔、$|\mathrm{GT}(N)| = \varphi(2k)\cdot e$ ✔。反射 witness $a'$(補題 B7)は**各窓ちょうど 1 個** ✔。$\langle r,g\rangle = \hat G$ が全繊維元で成立 ✔(補題 B5 の仮定)。

**v1 の誤った座の反証(核心)** — $X$(位数 $k$)の側の冪部分群 $\mathfrak P_X$ を同じ方法で計算すると:

| 窓 | $\mathfrak P_X \subseteq(\mathbb Z/k)^\times$ | 全射か | $\mathfrak P \subseteq (\mathbb Z/e)^\times$ | 結論 |
|---|---|:--:|---|---|
| S2 $k=4$ | $\{1,3\} = (\mathbb Z/4)^\times$ | **全射** | $\{1,7\}\subsetneq(\mathbb Z/8)^\times$ | **$X$ 側に障害なし・$w$ 側に障害あり** |
| S6 $k=5$ | $\{1,4\}\subsetneq(\mathbb Z/5)^\times$ | 非全射 | $\{1,9\}\subsetneq(\mathbb Z/10)^\times$ | 両側に障害(**v1 が k=5 でだけ説明できた理由**) |
| S7 $k=6$ | $\{1,5\} = (\mathbb Z/6)^\times$ | **全射** | $\{1,11\}\subsetneq(\mathbb Z/12)^\times$ | **$X$ 側に障害なし・$w$ 側に障害あり** |

⇒ **k=5 は $\langle X\rangle$ 自身が極大トーラス $\langle w\rangle$ の指数 2 部分群として同じ正規化群をもつ偶然**であり、v1 の説明はそこでだけ通用した。**一般の座は $w$ である。**

---

## 8. 【GAP】(隠さず明示)と含意

- **【GAP-B7】** 補題 B7(ii) の反射 witness の存在は 7 窓で計算確認。**一般証明は未了**(「marking の $\mathrm{Aut}$-軌道が $w$ の $\mathrm{Aut}$-類で決まる」を一般に示す必要がある)。反例があれば $u=-1$ 層が非 settled になり、case B の settled 率は $2/\varphi(2k)$ から $1/\varphi(2k)$ に落ちる。**予測の可反証性はここにある。**
- **【GAP-B8】** 定理 B(A) で $\bar U = \mathfrak P$(実現される $u$ が障害の上限に達すること)は **case A 窓では計算確認**、一般証明は未了。$\bar U \le \mathfrak P$(障害側)は紙で閉じている。
- **【GAP-B9】** 定理 B3′ は $\hat G=\mathrm{PGL}(2,p)$($p$ 素数)に依存する 3 条件(complete・自己中心化トーラス・Weyl $=C_2$)を使う。$\mathrm{PGL}(2,q)$($q$ 非素)や他の $\mathrm{Aut}_2(G)$ では **complete 性が壊れ得る**(委嘱 06 の【GAP-06e】と同根)。一般の case B へ外挿しない。
- **【GAP-B10】** 定理 M2 で除外した「像 $=S_3$」の第三型(case C)は $\mathrm{Out}(G)\supseteq S_3$ の単純群で起こり得る。そこでは補題 B1 の $\mathrm{Aut}(Q)$ 計算からやり直しが要る。
- **【状態】** 本稿の全主張は**私の単系統起草+私の第三独立実装による計算確認**。**cross-checked ではない**(GAP 実装との突合が未了)・**verified でもない**(Lean 未接続)。**genuine / arithmetical は一切主張していない。**

**含意(司令塔向け)**

1. **【GAP-06b】は閉じた**。case B の settled 障害は「$\mathrm{PGL}(2,p)$ が complete + 極大トーラスの Weyl 群が $C_2$」という**一つの理由**で $k=4,5,6$ を統一的に説明する。
2. **【GAP-06c】(命題 R の推移性)も閉じた**(系 B5-a)。しかも生成条件との同値(補題 B5)は **rigidity(配達 04)の言葉に翻訳できる形**になった。
3. **【GAP-06a】は半分閉じた**: case A の $\mathrm{GT}(N)\cong\mathrm{Hol}(\mathbb Z/k)$ は「全単射」から「(反)同型」に格上げされた(定理 B)。残るのは $\bar U=\mathfrak P$ の一般証明【GAP-B8】と (3.53) の実装側再現。
4. **非 isolated は「予測」から「定理」へ**(【GAP-B9】の射程内で)。実装 S2/S6/S7 は**予測の検証**ではなく**定理の較正**になる ⇒ 不一致が出たら、それは実装バグか私の定理の誤りかのどちらかであり、**どちらでも高情報**。
5. **狩場設計への含意**: isolated 性は $|\mathfrak P|$ と $\varphi(2k)$ の比で決まる。**非 isolated 対象を狙うなら「$\bar\sigma_1$ の生成する巡回群の正規化群が小さい窓」を撃てばよい** — 極大トーラス型はその典型である。逆に **isolated を保証したいなら $N_{\mathrm{Aut}}(\langle w\rangle)$ が $\mathrm{Hol}(\mathbb Z/e)$ になる窓**(Borel 型)を選ぶ。

**【文献要請 10】**: 「有限単純群 $G$ とその拡大 $\hat G$ における $(2,3,e)$-生成対 $(s,t)$ の $\mathrm{Aut}$-軌道が、$w = t^{-1}s$ の $\mathrm{Aut}$-類で決まる(rigidity の系)ための十分条件」— 補題 B7 と【GAP-B8】を一般化するのに要る。MacBeath の trace 三つ組(配達 02 §3)と rigidity(配達 04)の中間に位置する結果のはずだが、私の正典内には見当たらない。
> **↑ 後記(§9)**: この要請は **Sol 便 10 F6/F10 で実質的に満たされた**(「固定積類の全生成 factorization は単一 $\tilde G$-同時共役軌道」)。文献要請としては**取り下げてよい**。

---

## 9. 後記 — Sol 便 10 との**独立収束**(2026-07-26・起草後に判明)

**時系列(出所管理)**: 本稿 §0–§8 は `sol/sol_reply_10_caseB.md` を**読む前に**書き上げた(私の入力は便 09・裁定 09・委嘱 06 の自分の答案・配達 01–04 のみ)。Sol 側も「監査時点で委嘱 07 の case B settled 機構に関する追加文書は `docs/` に見当たらなかった」と申告している(便 10 監査範囲外)。**双方向にブラインドである。**

**一致した点(独立収束・第 4 号)**

| 論点 | 本稿 | Sol 便 10 |
|---|---|---|
| settled の必要条件 | 定理 B3: $u \bmod e \in \mathfrak P$ | **F9**: settled $\Rightarrow w^u\sim_{\tilde G}w$ |
| $k=4,6$ の障害の座 | §0.1・§8 の対照表: $X$ ではなく $w$(★ 教材) | **F10 ★・教材 4**: 「$X=w^2$ の normalizer は outer square root $w$ の PGL class を忘れる」 |
| 判定は層ごと($f$ に依らない) | 定理 B6(繊維は $0$ か $e$ の二択) | **F10**: 「$f$ に依存しない層ごとの判定」 |
| settled 層 | 系 B3-a: $m\in\{0,k-1\}$ | **F11**: 同じ($1,7$ / $1,9$ / $1,11$) |
| settled 数 | $\lvert\mathfrak P\rvert\cdot e = 2e$ | **F11**: $16/32$, $20/40$, $24/48$ |
| 命題 R の自由性の正しい根拠 | 補題 B5: 生成性 $+$ $Z(\hat G)=1$(coprimality は不要) | **F13**: 全く同じ。「coprimality 説明は削除すべき」 |
| 推移性の非循環性 | 系 B5-a の但し書き | **W85**: 「命題 R を $n=\lvert C\rvert$ の独立証明として引用しない」 |
| 一般化の禁止 | 【GAP-B9】 | **F11 末**: 「一般の case B まで settled iff $u=\pm1$ と一般化してはならない」 |

**Sol から採るべき改良(私の証明より良い箇所)**

- **十分性の証明**: 私は補題 B4(繊維不変)$+$ 補題 B5(自由)$+$ 補題 B7(反射 witness)の三段で $u\equiv-1$ 側を閉じ、B7 の一般化を **【GAP-B7】** として残した。**Sol の F10 はこれを一段で閉じる** — 「固定積類に属する**全**生成 factorization は単一の $\tilde G$-同時共役軌道(F6)。ゆえに $w^u\sim w$ なら候補は元と同時共役で、その共役元が ordered marking を送る」。⇒ **【GAP-B7】と【GAP-B8】は Sol F6/F10 で閉じる**(F6 の「単一軌道」自体は類積係数 $=\lvert C\rvert$ に依存するので、W85 の非循環規律は保つこと)。
- **一般形の言い方**: 「$u\equiv\pm1$」ではなく「**$w^u$ が元の積類に残る**」を定理の本体にする(Sol F11)。私の $\mathfrak P$ はその**群論的な言い換え**であり、$\mathfrak P=\{\pm1\}$ は定理 B3′ の 3 条件から出る**窓の性質**である — 両者は矛盾しない。

**本稿が Sol より進んでいる箇所(便 11 へ渡す価値がある)**

1. **補題 B1($\mathrm{Aut}(Q)$ の決定)と補題 B2($S_3$ 成分が自動的に恒等)** — Sol は $\hat G$ 成分の判定に直行しており、$\mathrm{Aut}(Q)\cong\mathrm{Aut}(\hat G)\times\mathrm{Aut}(S_3)$ と $\gamma=1$ の強制を明示していない。**settled を $Q$ の自己同型として読む段の厳密化**は本稿の寄与。
2. **定理 B の統一形** $\lvert\mathrm{GTSh}(N,N)\rvert = \lvert N_{\mathrm{Aut}(\hat G)}(\langle w\rangle)\rvert$ と、**case A の $\mathrm{Hol}(\mathbb Z/k)$ が「全単射」から「(反)同型」へ格上げされた**こと(【GAP-06a】の半分)。
3. **定理 B3′ の 3 条件の分離**(complete・自己中心化トーラス・Weyl $=C_2$)— どれが壊れると一般化が破れるかが明示される。
4. **補題 B7 の $\mathrm{PGL}(2,\mathbb Z)$ 解釈**: $u=-1$ の settled 性 $\iff$ $\bar N$ が $\mathrm{PGL}(2,\mathbb Z)$ でも正規($=$ 対象が鏡映対称・「実」)。**$u=-1$ が $\widehat{GT}$ の複素共役層である**ことと合わせ、算術側への橋の候補。Sol 便 10 にはこの読みはない。
5. **7 窓すべての明示行列による計算確認**(§7)— Sol は行列を構成していないと申告している(便 09 監査範囲外)。**P115 が要求する「二系統目 = 明示 $2\times2$ 行列列挙」の第一実装が本稿の検算**である(ただし単系統・GAP 未接続)。

**状態札の更新**: 本稿の主要主張は **Sol 便 10 と紙上二系統一致(独立収束)**。ただし**両者とも紙(+私の node 単系統)**であり、**GAP 実装との突合は未了 ⇒ cross-checked ではない**(W90 と同じ判断)。
