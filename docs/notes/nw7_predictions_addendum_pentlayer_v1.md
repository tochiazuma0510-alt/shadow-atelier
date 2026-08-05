# NW(7) 予言票 addendum A — **補題 PENT-LAYER(層移送)**+ LAY-3 の安全な言い換え + PRE-2 erratum

**状態札: `candidate(証明ノート・紙のみ / 機械は付録 A の 25 行整数演算のみ / 本走宇宙の候補評価ゼロ / 封印非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05
- 委嘱: 司令塔(**裁定 559**)— `sol/sol_reply_106_math33.md` **F106-2.2** の指定「$H_W$ が GT 合成で閉じることの補題 **PENT-LAYER** を起草せよ」+ **F106-2.1** 末尾の「LAY-3 の安全な言い換え」
- 対象: `docs/notes/nw7_mainrun_predictions_iffirst_v1.md`(以下 **票 v1**、commit `89349a8`)。
  ★ **票 v1 は IF-FIRST 凍結のまま 1 バイトも改変しない。本 addendum は additive であり、票 v1 の予言値を 1 つも変更しない**(§6)。
- 前提: F106-2 の裁定(LAY-1〜4 = 前件相対 PASS / PENT-HOM = $m=0$ kernel 部分 PASS / PRE-1・B-1a = PASS / PRE-2 = FAIL)

---

## 0. 結論(先に 4 行)

| # | 結論 |
|---|---|
| **0-1** | ★★ **$H_W$ が部分群であることは、層移送に必要ではなかった。** F106-2.2 が要求した「pentagon-live 集合が GT 合成で閉じる」補題は**真に難しい**(§3.3 に理由)。しかし予言票が実際に必要とするのは**それより弱い言明**であり、そちらは**類 4 の窓の中で直接証明できる**(**補題 PENT-LAYER**・§3.1)。 |
| **0-2** | ★ 鍵は「**左から掛ける**」こと。$h'\in A\subseteq\gamma_3(P)$、$f_0\in\gamma_2(P)$ に対し $E_{0,h'}(f_0)=f_0$(**exact**・補題 LEFT-TRIV)なので、fiber は $P$ の中の**素朴な左移動** $A\cdot f_0$ になる。右から掛けると $E_{m_0,f_0}$ の捻れが入って同じ論法は通らない。 |
| **0-3** | ★ 副産物: 共役作用が $\gamma_3(P)$ 上でちょうど $\Phi=E_{m,f}$ に一致することが**証明された**(系 CONJ-Φ)⟹ 票 v1 の**【EXQ-GAP-2】は graded 水準で閉じた**(EXQ-6 の $u^3/u^4$ が骨子でなく定理に)。 |
| **0-4** | PRE-2 の typing failure の機序を独立に再確認した(§5)。**Sol の値は正しい**: 生の $r$ は (3.10) を通るが (3.11) の次数 4 欠陥が $3(v_1{+}v_2{+}v_3)\ne0$。正しい $g_1=r\,s^{-1}$、$s=v_1v_2v_3$ の群語。 |

---

## 1. 補題 **SUB-W**(置換の重さ補題)— **F106-2.1 が求めた LAY-3 の安全な言い換え**

Sol の指示は「重さ 3 の語の一引数を $\gamma_4$ でずらすと差が $\gamma_6$ へ行く、と書けば安全」であった。この形は**一般補題の $d=3,k=4$ の場合**なので、一般形を証明して以後すべての置換段で引く。

> ### 補題 SUB-W
> $G$ を群、$\psi\in\mathrm{End}(G)$ とし、ある生成系 $Z$ の各元 $z$ について $\psi(z)z^{-1}\in\gamma_k(G)$($k\ge2$)とする。このとき
> $$w\in\gamma_d(G)\ \Longrightarrow\ \psi(w)\,w^{-1}\in\gamma_{d+k-1}(G).$$
>
> **証明**($d$ についての帰納)。
> **$d=1$**: 生成元では仮定そのもの($\gamma_{1+k-1}=\gamma_k$)。積については、$\psi(w_1w_2)(w_1w_2)^{-1}=\psi(w_1)\psi(w_2)w_2^{-1}w_1^{-1}=w_1\alpha_1w_2\alpha_2w_2^{-1}w_1^{-1}$ で、$\gamma_k$ が正規ゆえ $\in\gamma_k$。逆元も同様。
> **$d-1\to d$**: $\gamma_d$ は $[v,z]$($v\in\gamma_{d-1}$, $z\in G$)の正規閉包で生成される。$\psi v=v\alpha$($\alpha\in\gamma_{d+k-2}$)、$\psi z=z\beta$($\beta\in\gamma_k$)と書くと
> $$[\psi v,\psi z]=[v\alpha,z\beta]=[v,z\beta]^{\alpha}\,[\alpha,z\beta],$$
> $$[v,z\beta]=[v,\beta]\,[v,z]^{\beta}.$$
> ここで
> $[\alpha,z\beta]\in[\gamma_{d+k-2},\gamma_1]\subseteq\gamma_{d+k-1}$、
> $[v,\beta]\in[\gamma_{d-1},\gamma_k]\subseteq\gamma_{d+k-1}$、
> $[v,z]^{\beta}[v,z]^{-1}\in[\gamma_d,\gamma_k]\subseteq\gamma_{d+k}$、
> 外側の $\alpha$-共役の差も $[\gamma_d,\gamma_{d+k-2}]\subseteq\gamma_{2d+k-2}\subseteq\gamma_{d+k-1}$($d\ge1$)。
> ゆえに $\psi([v,z])[v,z]^{-1}\in\gamma_{d+k-1}$。正規閉包・積・逆元へは $d=1$ と同じ議論で伝わる。∎

### 1.1 ★ LAY-3 の該当段の言い換え(**1 行**)

> 票 v1 §2.2 LAY-3 (ii) の
> 「$f_2\in\gamma_3$ は重さ $\ge3$ の交換子の積で、その 1 引数を $\gamma_4$ でずらすと差は $[\gamma_2,\gamma_4]\subseteq\gamma_6(P)=1$」
> は、**補題 SUB-W の $d=3$, $k=4$**、すなわち
> $$\boxed{\ \textbf{重さ 3 の語の一引数を }\gamma_4\textbf{ でずらすと差は }\gamma_{3+4-1}=\gamma_6(P)=1\textbf{ へ行く}\ }$$
> と書くのが安全である。**結論は変わらない**(F106-2.1 逐語: 「現文の $[\gamma_2,\gamma_4]\subseteq\gamma_6$ はその collection の核心を表しており、結論は変わらない」)。

---

## 2. 補題 **LEFT-TRIV** と fiber の明示全単射

> ### 補題 LEFT-TRIV(**左掛けは捻れゼロ**)
> $P$ を類 $\le4$ の群、$h'\in\gamma_3(P)$、$f_0\in\gamma_2(P)$ とする。$E_{0,h'}$ は $x\mapsto x$、$y\mapsto h'^{-1}yh'$ で定まる自己準同型($m=0$、$u=1$)である。このとき
> $$\boxed{\ E_{0,h'}(f_0)=f_0\qquad(\textbf{$P$ の中の exact な等式}).\ }$$
> **証明.** $h'^{-1}yh'=y[y,h']$、$[y,h']\in[\gamma_1,\gamma_3]\subseteq\gamma_4(P)$。ゆえに $E_{0,h'}$ は生成元を $\gamma_4$ の分だけずらす自己準同型で、**補題 SUB-W**($k=4$)を $f_0\in\gamma_2$($d=2$)に適用して
> $$E_{0,h'}(f_0)f_0^{-1}\in\gamma_{2+4-1}(P)=\gamma_5(P)=1.\qquad\blacksquare$$

> ### 系 COSET-EXP(fiber は $P$ の中の**素朴な左移動**)
> $g_0=[m_0,f_0]\in\mathrm{GT}(\mathbf N)$、$A=\ker\chi_{\rm vir}=\mathrm{hex}(0)$ とする。合成 (3.53) に $[0,h']\circ[m_0,f_0]$ を代入すると $m$-成分は $m_0$、$f$-成分は $h'E_{0,h'}(f_0)=h'f_0$(LEFT-TRIV)。$A=\ker\chi_{\rm vir}$ は正規で fiber は coset なので
> $$\boxed{\ \mathrm{hex}(m_0)=A\cdot f_0\ =\ \{h'f_0\ :\ h'\in A\}\subseteq P,\qquad h'\longmapsto h'f_0\ \textbf{は全単射}.\ }$$

> ★ **これは LAY-1 の強化である。** LAY-1 は「fiber は coset ゆえ個数一様」までだったが、系 COSET-EXP は **$P$ の中の具体的な左移動として fiber を書き下す**。以下の議論はすべてこの明示形に載る。
> ⚠ **右からは駄目**: $[m_0,f_0]\circ[0,h']=[m_0,\ f_0\,E_{m_0,f_0}(h')]$ で、$E_{m_0,f_0}$ は $\mathrm{gr}_3$ に $u_0^3$、$\mathrm{gr}_4$ に $u_0^4$ で効く**非自明な**自己準同型である($u_0\ne1$ で $u_0^3\ne u_0^4$ — 付録 A)。**左右の非対称性がこの addendum の技術的な核心。**

---

## 3. ★★ 補題 **PENT-LAYER**(層移送)

### 3.1 主張と証明

> ### 補題 PENT-LAYER
> 記号は票 v1 §1.3 のとおり($D(\bar f)=\bar\rho^4(j\bar f)\cdots j\bar f$、$\mathrm{PENT}_W\iff D=1$、$H_W=\{g\in\mathrm{GT}(\mathbf N):\mathrm{PENT}_W(g)\}$)。$\mathbf N$ は isolated(ISO-V)、$W=\mathcal V(K(0,5))$ は verbal、$P,Q$ はともに類 $\le4$ とする。このとき **各 $m\in\mathcal X_{\mathbf N}$ について**:
>
> **(1)** $\mathrm{hex}(m)$ が **PENT を通る元を 1 つでも含む**なら
> $$\boxed{\ \bigl\lvert\mathrm{pent}(m)\bigr\rvert\ =\ \bigl\lvert\ker(D|_A)\bigr\rvert\ =\ \bigl\lvert\mathrm{pent}(0)\bigr\rvert\ }$$
> であり、しかも $\mathrm{pent}(m)=\ker(D|_A)\cdot f_0$($f_0$ = 当該 PENT 元の $f$-成分)という**明示形**をもつ。
> **(2)** 含まないなら $\lvert\mathrm{pent}(m)\rvert=0$。
> **(3)** ゆえに $\lvert\mathrm{pent}(m)\rvert\in\{0,\ \lvert\ker(D|_A)\rvert\}$ が**全層で一様**であり、$\lvert A\rvert=49$ の下では $\lvert\ker(D|_A)\rvert\in\{1,7\}$(PENT-HOM・F106-2.2 で PASS)。
>
> **証明.**
> **(2)** は自明。**(1)** を示す。$g_0=[m_0,f_0]\in H_W$、すなわち $D(f_0)=1$ とする。
>
> **段 1(fiber の明示形)**: 系 COSET-EXP より $\mathrm{hex}(m_0)=\{h'f_0:h'\in A\}$、対応は全単射。
>
> **段 2($D$ の分解)**: $h'\in A\subseteq\gamma_3(P)$(票 v1 LAY-3 (i): $m=0$ で $c_2=0$)ゆえ $j h'\in\gamma_3(Q)$、$jf_0\in\gamma_2(Q)$。$Q$ は類 $\le4$ ゆえ
> $$[\gamma_2(Q),\gamma_3(Q)]\subseteq\gamma_5(Q)=1,\qquad [\gamma_3(Q),\gamma_3(Q)]\subseteq\gamma_6(Q)=1 .$$
> $\bar\rho$ は各 $\gamma_k(Q)$ を保つ($W$ が完全不変ゆえ $\bar\rho\in\mathrm{Aut}(Q)$・補題 NW-3)ので、5 個の $\bar\rho^i(jh')$ は互いに可換かつ 5 個の $\bar\rho^k(jf_0)$ のすべてと可換。ゆえに積を並べ替えて
> $$D(h'f_0)=\prod_{i=4}^{0}\bar\rho^i(jh'\cdot jf_0)=\Bigl(\prod_{i=4}^{0}\bar\rho^i(jh')\Bigr)\Bigl(\prod_{i=4}^{0}\bar\rho^i(jf_0)\Bigr)=D(h')\,D(f_0).$$
>
> **段 3(結論)**: $D(f_0)=1$ より $D(h'f_0)=D(h')$。したがって
> $$\mathrm{pent}(m_0)=\{h'f_0:h'\in A,\ D(h')=1\}=\ker(D|_A)\cdot f_0 .$$
> $D|_A$ は準同型(PENT-HOM)なので $\ker(D|_A)$ は $A$ の部分群であり、左移動は全単射。ゆえに $\lvert\mathrm{pent}(m_0)\rvert=\lvert\ker(D|_A)\rvert$。$m_0=0$、$f_0=1$ と取れば右辺は $\lvert\mathrm{pent}(0)\rvert$。∎

### 3.2 ★ なぜ「$H_W$ が部分群」は要らなかったか

F106-2.2 は「$H_W$ が GT 合成で閉じる」補題を要求した。しかし予言票が使う言明は**層あたり個数の一様性**だけであり、その証明に必要な閉性は

$$\boxed{\ \textbf{「}H_W\ \textbf{に }A\cap H_W\ \textbf{を}\textbf{左から}\textbf{掛けても }H_W\textbf{」}\ \textbf{だけ}\ }$$

である。これは段 2 の可換性($[\gamma_2(Q),\gamma_3(Q)]=1$)から**直接**出る。一般の $g_1\circ g_2$($両者とも \gamma_2\setminus\gamma_3$ の $f$-成分)では

$$D\bigl(f_1\,E_{m_1,f_1}(f_2)\bigr)$$

の並べ替えに $[\gamma_2(Q),\gamma_2(Q)]\subseteq\gamma_4(Q)\ne1$ の補正項が出るうえ、$j\circ E_{m_1,f_1}$ と $\bar\rho$ の交換関係が全く分からない — **これが「難しい」の中身である**(§3.3)。

> ### ★ 一行で
> **層内は $\gamma_3$ の世界(可換・$D$ は準同型)、層をまたぐと $\gamma_2$ の世界(非可換・$E$ の捻れ)。** 個数の移送は層内の構造だけで足りるので、層をまたぐ閉性を証明する必要がない。

### 3.3 ★ $H_W$ の部分群性そのものの状態(**未証明・臨界路上でない**)

**本 addendum は $H_W$ が部分群であることを証明しない。** 到達した記述は次である。

| # | 事実 | 状態 |
|---|---|---|
| **(a)** | $H_W\supseteq G^{\rm gen}:=\mathrm{Im}(\widehat{GT}\to\mathrm{GT}(\mathbf N))$ で、$G^{\rm gen}$ は**部分群**(群準同型の像)。包含は HSP-SOUND の対偶(lift が在れば PENT は真) | ★ **成立**(B-0a の標準前件相対) |
| **(b)** | 各層について $H_W\cap\chi_{\rm vir}^{-1}(u)=\ker(D\vert_A)\cdot f_u$(PENT-LAYER) | ★ **証明済**(§3.1) |
| **(c)** | ゆえに $\lvert H_W\rvert=\lvert U'\rvert\cdot\lvert\ker(D\vert_A)\rvert$($U'$ = PENT 元をもつ層の集合)。**B-0a の下で $U'=(\mathbb Z/7)^\times$** ゆえ $\lvert H_W\rvert=6\lvert\ker(D\vert_A)\rvert\in\{6,42\}$ | ★ **従う**(b)+(a) |
| **(d)** | ★ **$H_W$ が部分群 $\iff$ $\ker(D\vert_A)$ が全 $\Phi_u:=E_{m_u,f_u}\vert_{\gamma_3(P)}$ で不変**(系 CONJ-Φ より共役作用が $\Phi_u$ に一致するので) | ★ **UNKNOWN**(【PL-GAP-1】) |

> ### ⚠ (d) が非自明である理由(1 行)
> $\lvert\ker(D\vert_A)\rvert=7$ の場合、それは $A\cong\mathbb F_7^2$ の中の直線で、$\langle h_4\rangle$ **ではない**($D(h_4)=\eta\ne0$)。$\Phi_u$ は $\mathrm{gr}$ 上 $\mathrm{diag}(u^3,u^4)$ で、$u\ne1$ では $u^3\ne u^4$(付録 A で全 6 層について機械確認)ゆえ固有直線はちょうど 2 本 — $\langle h_4\rangle$ と、もう 1 本。**$\ker(D\vert_A)$ がその「もう 1 本」に、全 $u$ について同時に一致するか**が問われている。**予言票の値には効かない**(層移送は (b) で閉じている)ので、**臨界路上ではない**。

> ### ★ 司令塔への申し送り
> F106-2.2 が要求した形(「$H_W$ が部分群」)は、**本 addendum では達成していない**。達成したのは「**層移送に十分な弱い閉性**」である。**もし Sol が部分群性そのものを条件として要求し続けるなら**、それは (d) の $\Phi$-不変性を示すか、あるいは HS Prop 7 の lift 存在形を有限窓へ持ち込む(**罠 D-5 に抵触**・「どの $\tilde F$ か」の量化を cert に明記する義務が発生)必要がある。**本 addendum はそのどちらも行わず、要求より弱い十分条件で予言を閉じる道を選んだ**旨を明示して提出する。

---

## 4. 系 **CONJ-Φ** — 共役作用の同定と【EXQ-GAP-2】の部分閉鎖

> ### 系 CONJ-Φ
> $g=[m,f]\in\mathrm{GT}(\mathbf N)$、$h\in A$ とすると、$\mathrm{GT}(\mathbf N)$ における共役は
> $$\boxed{\ g\,h\,g^{-1}=[0,\ \Phi(h)],\qquad \Phi:=E_{m,f}\big\vert_{\gamma_3(P)}\ }$$
> で与えられる。
> **証明.** $h''\in A$ を $g h g^{-1}=h''$ とすると $h''g=gh$。左辺の $f$-成分は LEFT-TRIV より $h''f$、右辺は (3.53) より $f\,E_{m,f}(h)$。ゆえに $h''f=f\,E_{m,f}(h)$。ここで $E_{m,f}(h)\in\gamma_3(P)$、$f\in\gamma_2(P)$ で $[\gamma_2(P),\gamma_3(P)]\subseteq\gamma_5(P)=1$ ゆえ両者は可換、したがって $h''=E_{m,f}(h)=\Phi(h)$。∎

> ### ★ 【EXQ-GAP-2】の状態更新(票 v1 §8.2)
> 票 v1 は「$C_6$ の作用が $\mathrm{gr}_3$ に $u^3$、$\mathrm{gr}_4$ に $u^4$」を**導出骨子のみ**として【EXQ-GAP-2】に立てていた。系 CONJ-Φ により共役作用が $\Phi=E_{m,f}$ **そのもの**と同定され、$E_{m,f}$ が $\mathrm{gr}_k$ に $u^k$ で効くこと($x\mapsto x^u$、$y\mapsto f^{-1}y^uf$ で共役は $\mathrm{gr}_1$ に効かない)から
> $$\boxed{\ \textbf{【EXQ-GAP-2】は }\mathbf{gr}\ \textbf{水準で CLOSED}\ }$$
> **残る部分**: $\Phi$ の $\mathrm{gr}_3\to\mathrm{gr}_4$ の**非対角成分**(filtered だが graded でない部分)は同定していない。EXQ-6 の「$C_7^2\rtimes C_6$ で作用が $u^3,u^4$」という言明を **graded な言明として読む限り証明済**、**$A$ 上の線型作用としての完全形は未同定**(【PL-GAP-2】)。分裂そのものは Schur–Zassenhaus($\gcd(6,49)=1$)で従来どおり。

---

## 5. PRE-2 の erratum — **誤りの機序**(独立再確認)

### 5.1 何が起きたか(F106-2.4 の逐語要旨 + 当方の独立確認)

PRE-2 の cert は $\xi:=D(g_1)$ を測るはずだったが、実際に測ったのは **生の Hall 交換子語**
$$r:=\mathrm{Comm}(\mathrm{Comm}(x,y),x)\cdot\mathrm{Comm}(\mathrm{Comm}(x,y),y)$$
に対する $D(jr)$ であった。Sol の展開によれば
$$\log r=\mathfrak h_3+(v_1+v_2+v_3)\pmod{\gamma_5}.$$

★ **当方の独立確認**(付録 A・PREC-1 と $\theta_*$ の作用だけを使う):

| 検査 | 値 | 判定 |
|---|---|---|
| 生の $r$ の (3.10) 次数 4 欠陥 $=(1+\theta_*)(1,1,1)$ | $(0,0,0)$ | **通る** |
| 生の $r$ の (3.11) 次数 4 欠陥 $=(2\alpha-\beta+2\gamma)$ at $(1,1,1)$ | $\mathbf 3\ne0\bmod7$ | ★ **落ちる** |
| $g_1=r\,s^{-1}$ の (3.11) 次数 4 欠陥($\Psi=0$ + $(0,0,0)$) | $0$ | **通る** |

⟹ **$r\notin A=\mathrm{hex}(0)$**(NW-P3 により $v_1,v_2,v_3$ は標的 $P$ で生存するので非零性は exact)。Sol の裁定は正しく、**cert の非比例性は登録量 $\xi$ の値ではない**。

### 5.2 ★ 誤りの機序(**認識すべき罪**)

$$\boxed{\ \textbf{Lazard 座標の exact lift }\exp(\mathfrak h_3)\ \textbf{と、生の Hall 語 }r\ \textbf{を同一視したこと。}\ }$$

- PRE-1 が示したのは「**$\mathfrak h_3$ を Lazard 座標の次数 3 成分にもつ元で、次数 4 成分を $0$ に取ったものが hexagon を満たす**」($\Psi=0$)。
- 生の交換子語 $r$ の Lazard 座標は $\mathfrak h_3+(v_1{+}v_2{+}v_3)$ であって $\mathfrak h_3$ **ではない**。次数 4 成分がゼロでない。
- ★ **これは翻訳ノート §8.3.3 の自己捕獲**(「$h_3\theta(h_3)$ は $\gamma_4(P)$ に入るが $1$ とは限らない/$h_3^{\,t}$ は exact な hexagon 解ではない/**次数 4 の補正項が要る**」)**の具体値**である。§8.3.3 は「補正が要る」と警告し、PRE-2 の実装はその補正を入れずに走った。
- ★ **規約台帳 §1.3.10 の Lie/群の別**($\mathfrak h_4$ は Lie 元・$h_4$ は群元・**同一視しない**)は $\mathfrak h_4$ については守られていたが、**$\mathfrak h_3$ については同じ規律が明文化されていなかった**。⟹ **申し送り**: 規約台帳に $\mathfrak h_3$/$h_3$ の行を追加し、**「$h_3$ の生語は $A$ の元ではない($\log$ の次数 4 成分が $v_1{+}v_2{+}v_3$)」を注記**すること。

### 5.3 正しい測定対象(**再測定の仕様**・実装係向け)

> $$s:=\bigl[[[x,y],x],x\bigr]\cdot\bigl[[[x,y],x],y\bigr]\cdot\bigl[[[x,y],y],y\bigr]\ \in\gamma_4(P)\qquad(\log s=v_1+v_2+v_3)$$
> $$\boxed{\ g_1:=r\,s^{-1}\quad(=s^{-1}r;\ \gamma_4(P)\ \textbf{は中心ゆえ順序無害}),\qquad \log g_1=\mathfrak h_3 .\ }$$
> **測るもの**: $\xi:=D(j g_1)$ と $\eta:=D(j h_4)=\nu_4(j\mathfrak h_4)$ の $\mathbb F_7$-従属性。
> - $\xi\in\mathbb F_7\eta$ ⟹ **B-2a**($\lvert\ker(D\vert_A)\rvert=7$・PENT 総数 42・hexagon-only 252)
> - $\xi\notin\mathbb F_7\eta$ ⟹ **B-2b**($\lvert\ker(D\vert_A)\rvert=1$・PENT 総数 6・hexagon-only 288)
>
> ★ **fail-closed 前検査(必須・これが今回欠けていた)**: 測定の前に **$g_1$ が実際に $A$ の元であること**を機械で確かめる — すなわち $P$ の中で
> $$g_1\,\theta(g_1)=1\quad\text{かつ}\quad \tau^2(g_1)\tau(g_1)g_1=1$$
> を **exact な群等式として**検査し、通らなければ `TYPING_FAILURE / STOP`。同じ検査を $h_4$ にも掛ける(**補題 DUM-HEX の実測版**)。
> ⟹ **$\xi$ は「$A$ の元に対する $D$ の値」としてのみ意味をもつ。$A$ 所属の検査を通っていない元の $D$ 値は、診断値であって branch evidence ではない**(F106-2.4 の裁定どおり)。

> ⚠ **本 addendum は再測定を行わない**(紙のみ・司令塔が実装係へ発注済)。$\xi$ の値は依然 **UNKNOWN**、**B-2 は OPEN**。

---

## 6. 予言表への影響 — **なし**(層移送だけが閉じた)

| 量 | 票 v1 の登録 | 本 addendum 後 |
|---|---|---|
| nonempty layers | 6(B-0a 前件相対) | **不変** |
| hexagon / layer | 49(B-1a) | **不変**(F106-2.3 で PASS) |
| hexagon total | 294 | **不変** |
| **PENT / layer** | 7(B-2a) | ★ **OPEN: 1 または 7**。ただし ★ **全層で同じ値であることが証明された**(PENT-LAYER)— これが本 addendum の追加分 |
| PENT total | 42 | **OPEN: 6 または 42**(層移送込みで**この 2 値以外はあり得ない**) |
| hexagon-only | 252 | **OPEN: 288 または 252**(同上) |
| SURJ fail / settled | 0 / 100% | **不変**(F106-2.5 の限定つき: settled は**hexagon-pass 294 件を分母**とする。705,894 の非-shadow 候補に settled の語を付けない) |

> ### ★ 本 addendum が予言に加えた唯一の内容
> $$\boxed{\ \textbf{分岐 B-2 の決着は「層あたり 1 か 7 か」の}\textbf{1 ビット}\textbf{に完全に縮約された。}\ }$$
> 票 v1 は EXQ-7 で「各非空層の PENT 通過数 $=7$」と書いたが、**PENT-HOM が与えていたのは $m=0$ 層だけ**であり、**他の 5 層への移送を暗黙に飛ばしていた**(F106-2.2 の指摘は正当)。本 addendum の PENT-LAYER がその一段を埋める。⟹ **再測定は $m=0$ 層の $\xi$ 1 点だけでよい**(全層を測る必要はない)。
>
> ⚠ **票 v1 §7 の解釈規約は不変**。とくに「登録済み分岐への着地は『外れ』でなく『決着』」(丙類)は B-2b にもそのまま適用される。**本 addendum は分岐の値を動かしていないので、S-7′ に抵触しない。**

---

## 7. 格付け・【GAP】・規律申告

### 7.1 格付け

| 対象 | 格 |
|---|---|
| 補題 **SUB-W** | ★ **paper-proof**(初等・群論の標準補題を自前証明。外部入力ゼロ) |
| 補題 **LEFT-TRIV** / 系 **COSET-EXP** | ★ **paper-proof candidate**(SUB-W + 類 4)**Sol 未監査** |
| ★ 補題 **PENT-LAYER** | ★ **paper-proof candidate**(**Sol 未監査**)。前件: ISO-V($\mathbf N$ isolated)・LAY-3 (i)($c_2=0$)・PENT-HOM(F106-2.2 PASS)・$Q$ 類 $\le4$ |
| 系 **CONJ-Φ** | ★ **paper-proof candidate**(LEFT-TRIV の 3 行系) |
| §3.3 (a)(b)(c) | (a) は B-0a の標準前件相対、(b)(c) は PENT-LAYER 相対 |
| §5 の PRE-2 独立再確認 | ★ **PREC-1 と $\theta_*$ の作用のみを使う整数演算**(付録 A)。**Sol と同じ結論に独立に到達したが、起草者が同一系統ではないため `cross-checked` の候補ではある — ただし CV-9 判読未実施ゆえ本 addendum では `cross-checked` を付さない** |
| `verified` | ✗ 付かない(Lean 未使用) |
| novelty | **主張しない** |

### 7.2 【GAP】

| 札 | 内容 | 状態 |
|---|---|---|
| ★ **【PL-GAP-1】**(新規) | **$H_W$ が部分群かは未証明。** 判定基準 = $\ker(D\vert_A)$ が全 $\Phi_u$ で不変か(§3.3 (d))。$\Phi_u$ は $u\ne1$ で $\mathrm{gr}$ 上に相異なる固有値 $u^3\ne u^4$ をもつ | **UNKNOWN**。★ **臨界路上でない**(層移送は PENT-LAYER で閉じている) |
| ★ **【PL-GAP-2】**(新規) | 系 CONJ-Φ は共役 $=\Phi$ を同定したが、$\Phi\vert_A$ の **$\mathrm{gr}_3\to\mathrm{gr}_4$ 非対角成分**は未同定。EXQ-6 の作用主張は **graded 水準でのみ**証明済 | **OPEN**(紙・本走非接触) |
| **【EXQ-GAP-2】**(票 v1) | $C_6$ 作用の $u^3/u^4$ | ★ **graded 水準で CLOSED**(§4)。完全形は PL-GAP-2 へ引き継ぎ |
| **【EXQ-GAP-3】**(票 v1) | $\xi$ の値が未計算 ⟹ B-2 未決 | ★ **OPEN(継続)**。PRE-2 の再測定待ち。**測定対象の仕様は §5.3 で確定** |
| **【EXQ-GAP-1】**(票 v1) | $\Psi$ の値 | ★ **CLOSED**($\Psi=0$・PRE-1・F106-2.3 で PASS) |

### 7.3 規律申告

- ★ **本走宇宙(705,894 対)の候補を 1 件も評価していない。** GAP も pc 群も起動していない。機械は付録 A の python 25 行(整数演算のみ)。
- **封印 3 量($n=5$ 関連・$\mathrm{Im}\,R$・$d_N$・$u$ 値)非接触。**
- **外部文献検索ゼロ。新しい原典頁を開いていない。【文献要請】は起票しない。**
- ★ **票 v1(commit `89349a8`)を 1 バイトも改変していない**(IF-FIRST 凍結の保全)。本 addendum は additive で、**予言値を 1 つも変更していない**(§6)。
- **HS Prop 7 の lift 存在形を使っていない**(罠 D-5 遵守)。$\widehat{GT}$ の使用は §3.3 (a) の HSP-SOUND 対偶のみで、これは既在の命題である。

---

## 8. Sol への監査点(3 点・便 107 用)

> **Q-1 ★★ 補題 LEFT-TRIV**(§2)。「$E_{0,h'}(f_0)=f_0$ が $P$ の中の **exact な等式**」という主張。補題 SUB-W($d=2$, $k=4$ ⟹ 差は $\gamma_5(P)=1$)の適用が正しいか。**ここが「fiber は素朴な左移動 $A\cdot f_0$」(系 COSET-EXP)と PENT-LAYER の両方を支えている。** とくに SUB-W の帰納段($[v\alpha,z\beta]$ の展開で拾う 4 つの項がすべて $\gamma_{d+k-1}$ に落ちること)に穴がないか。
>
> **Q-2 ★★ 補題 PENT-LAYER の位置づけ**(§3.2/§3.3)。F106-2.2 が要求した「$H_W$ が GT 合成で閉じる」を**証明せず**、より弱い「$A\cap H_W$ を**左から**掛ける閉性」で層移送を閉じた、という設計判断を認めるか。**認めない場合、部分群性の証明に何を許すか**(【PL-GAP-1】の $\Phi$-不変性か、罠 D-5 に抵触する lift 存在形か)の指示を請う。
>
> **Q-3 ★ 系 CONJ-Φ**(§4)。$h''f=f\,E_{m,f}(h)$ から $[\gamma_2(P),\gamma_3(P)]\subseteq\gamma_5(P)=1$ を使って $h''=E_{m,f}(h)$ を出した一段。および、これによって票 v1 の【EXQ-GAP-2】を **graded 水準で閉じた**と数えてよいか(非対角成分は PL-GAP-2 として残す会計)。

---

## 付録 A. 独立検算(**本走非接触**・整数演算のみ)

使う事実は **PREC-1**($(1+\tau_*+\tau_*^2)(\alpha v_1+\beta v_2+\gamma v_3)=(2\alpha-\beta+2\gamma)(v_1{+}v_2{+}v_3)$)と $\theta_*$ の作用($v_1\mapsto-v_3$, $v_2\mapsto-v_2$, $v_3\mapsto-v_1$)のみ。

```python
p = 7
prec = lambda a,b,c: (2*a-b+2*c) % p                       # PREC-1
th   = lambda a,b,c: ((a-c)%p, 0, (c-a)%p)                 # (1+theta_*)
# 生の r : log r = h3 + (v1+v2+v3)  [Sol F106-2.4]
assert th(1,1,1) == (0,0,0)          # (3.10) は通る
assert prec(1,1,1) == 3 != 0         # (3.11) が落ちる  => r は A の元でない
# g1 = r*s^-1 : log g1 = h3
assert prec(0,0,0) == 0              # Psi=0 (PRE-1) と合わせて hexagon OK
# h4 = (1,4,1) の再確認
assert th(1,4,1) == (0,0,0) and prec(1,4,1) == 0
assert [(a,b,c) for a in range(p) for b in range(p) for c in range(p)
        if th(a,b,c)==(0,0,0) and prec(a,b,c)==0] == [(t%p,(4*t)%p,t%p) for t in range(p)]
# Phi_u の graded 固有値
for m in [0,1,2,4,5,6]:
    u = (2*m+1) % p
    print(m, u, pow(u,3,p), pow(u,4,p), pow(u,3,p) != pow(u,4,p))
```

**出力(機械生成)**:

```
raw r : log r = h3 + (v1+v2+v3)  [Sol F106-2.4]
  hexagon(3.10) deg4 defect (1+theta*)(1,1,1) = (0, 0, 0)  -> zero: True
  hexagon(3.11) deg4 defect (2a-b+2c) at (1,1,1) = 3  -> nonzero mod 7: True
g1 = r*s^-1, log g1 = h3 exactly (gamma4 central)
  (3.11) deg4 = Psi(=0 by PRE-1) + (2a-b+2c) at (0,0,0) = 0 -> hexagon OK

h4 = (1,4,1):  (1+theta*) = (0, 0, 0)  (2a-b+2c) = 0  -> both zero: True
sanity: solution space of {a=c} & {2a-b+2c=0} is spanned by (1,4,1): True

Phi_u graded eigenvalues on A: gr3 -> u^3, gr4 -> u^4
  m=0 u=1 u^3=1 u^4=1  distinct=False
  m=1 u=3 u^3=6 u^4=4  distinct=True
  m=2 u=5 u^3=6 u^4=2  distinct=True
  m=4 u=2 u^3=1 u^4=2  distinct=True
  m=5 u=4 u^3=1 u^4=4  distinct=True
  m=6 u=6 u^3=6 u^4=1  distinct=True
```

- 1〜2 行目: **Sol の PRE-2 診断を独立に再現**(生の $r$ は (3.10) を通り (3.11) で落ちる)。
- 4 行目: $D4$-POWER (a) の解空間 $=\mathbb F_7(1,4,1)$ を悉皆で再確認(343 通り全走査)。
- 最終ブロック: $u\ne1$ の全 5 層で $u^3\ne u^4$ ⟹ §3.3 (d) の「$\Phi_u$ の固有直線はちょうど 2 本」。
