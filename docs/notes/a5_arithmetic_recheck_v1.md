# A₅ 窓の算術飽和・再検分 — **三つ巴は 2 対 1。倒れるのは pentagon 側**(v4 は無傷・私の √5 仮説は撤回)

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 委嘱: 裁定 250(v4 L521 の再検分・$G_{\mathbf Q(\sqrt5)}$ 仮説の検証)
- 正本: `docs/week4-A5算術飽和_v4.md` §4.1(定理 A₅)・`docs/notes/u_meas_cal_a5_v1.md`(W3-8 較正)・`search/certs/pent_pi_a5_20260731.json`・`docs/notes/pent_recoding_v1.md`(定理 REC)
- 結論: **v4 は倒れない。W3-8 も倒れない。両者は同じことを言っている。実測 pentagon(10/20)だけが、v4 とも W3-8 とも独立に、単独で不可能である。**

---

## 0. 結論(先出し)

| # | 判定 | 格 |
|---|---|---|
| **①** | **私の $G_{\mathbf Q(\sqrt5)}$ 仮説を撤回する**。$\mathrm{Ih}_{N_A}$ は $G_{\mathbf Q}$ **全体**で定義され、$\widetilde\chi\circ\mathrm{Ih}$ は Chebotarev により全射。算術像が指数 2 の部分群になることは**あり得ない** | **撤回(proof)** |
| **②** | **決定的論証(v4 も W3-8 も使わない)**: 任意の $K\in\mathrm{NFI}_{PB_4}(B_4)$ で $G_{\mathbf Q}\to\mathrm{GT}(K)$ が定義され、$\widetilde\chi$ は $(\mathbf Z/5)^\times$ へ全射。定理 REC より $\mathrm{GT}(K_\pi)$ の対は $N_A$ の gentle shadow。⟹ **$u\in\{2,3\}$ の pentagon-live shadow が存在しなければならない**。実測 0 ⟹ **pentagon 側に欠陥** | **proof**(§3) |
| **③** | **委嘱 3 の型錯誤の訂正**: W3-8 の $u^{-1}=-2$ は **Kummer 助変数**(有理数)であって $\widetilde\chi$ の値ではない。「$u\equiv3\bmod5$」という読みは成立しない。ただし W3-8 の結論($L=\mathbf Q(\zeta_5,\sqrt[5]2)$・$\mathrm{Gal}=F_{20}$)は **v4 と完全一致**し、$C_4$ 商 = mod 5 円分指標の全射性を支持する | **proof**(§2) |
| **④** | **委嘱 1**: $L=\mathbf Q(\zeta_5,\sqrt[5]2)$ は **rigidification 体**(= v4 命題 M の「marked quotient $(P;X,Y)$ の体」)であって dessin の **moduli 体ではない**。moduli 体は $\mathbf Q$((I1) isolated の帰結)。**「20 全て arithmetical」は $\mathbf Q$ 上の主張として v4 は正しく述べている** | **proof**(§1) |
| **⑤** | したがって **v4 の erratum は不要**。ただし (I1) の言い換え(「$\bar N_A$ が $G_{\mathbf Q}$-安定 $\Leftarrow$ isolated」)を補題として明示すべき(§1.3) | **提案** |
| **⑥** | 欠陥の探索先を優先順で名指し(§5)。第一容疑は **hexagon で実際に起きた向き規約の反転型**($f\leftrightarrow f^{-1}$) — cert の `f_orientation` 欄と readA/readB の存在自体がその兆候 | **candidate** |

---

## 1. 委嘱 1 — $L$ の正体と「20 全て arithmetical」の正確な意味

### 1.1 v4 の主張(逐語)

> $$\boxed{\;\operatorname{Ih}_{N_A}:\; G_{\mathbb Q}\;\twoheadrightarrow\;\operatorname{GT}(N_A)\;\cong\;F_{20}\;}$$
> $$\boxed{\;\ker\bigl(\Phi\circ\operatorname{Ih}_{N_A}\bigr)\ \text{の固定体} \;=\; L \;=\; \mathbb Q\bigl(\zeta_5,\sqrt[5]{2}\bigr),\qquad \operatorname{Gal}(L/\mathbb Q)\cong F_{20}. \;}$$
> したがって **GT(N_A) の 20 元すべてが arithmetical**、ゆえに(G_ℚ ↪ ĜT を経由するので)**すべて genuine** である。
> (`week4-A5算術飽和_v4.md` §4.1)

### 1.2 $L$ は moduli 体ではなく rigidification 体

$L$ は $\ker(\Phi\circ\mathrm{Ih}_{N_A})$ の固定体、すなわち **$G_{\mathbf Q}$ が marking 込みの対象 $(P;X,Y)$ に忠実に作用する最小体**である。v4 自身が命題 M の注でこれを正しく命名している:

> **K_N の呼び方(v3 で訂正・Sol F11)**: 一般の P では K_N を直ちに「ある dessin の rigidification の体」と呼べない…**安全な一般名は「marked quotient (P; X, Y) の体」**である。A₅ の自然な 5 点作用ではこの二つは一致する。

一方、**dessin(対象 $N_A$ そのもの)の moduli 体**は「$\bar N_A$ を保つ $\gamma$ の全体」の固定体であり、これは仮定 **(I1)**($\bar N_A$ が $s_v(G_{\mathbf Q})$ で安定 = $N_A$ は isolated)により **$\mathbf Q$** である。

> **⟹ 委嘱 1 の答え: moduli 体 $=\mathbf Q$、rigidification 体 $=L=\mathbf Q(\zeta_5,\sqrt[5]2)$、$[L:\mathbf Q]=20=\lvert\mathrm{GT}(N_A)\rvert$。**
> **「20 全て arithmetical」は基礎体 $\mathbf Q$ 上の主張として述べられており、$\mathbf Q(\sqrt5)$ 上の主張ではない。v4 の書き方に誤りはない。**

### 1.3 (I1) の内実(v4 に補うべき補題)

> ### 補題 ISO-Ih(v4 (I1) の正確形)【proof】
> $N$ が **isolated**(= 全 shadow が settled、$\mathrm{GT}(N)=\mathrm{GTSh}(N,N)$)なら、$\mathrm{Ih}_N:G_{\mathbf Q}\to\mathrm{GT}(N)$ は **$G_{\mathbf Q}$ 全体**で定義される群準同型である。
> **証明.** $\gamma\in G_{\mathbf Q}\subset\widehat{GT}_{\rm gen}$ の対 $(\lambda,\hat f)$ は hexagon を profinite に厳密に満たすから、$N$ を法として還元した $(m,f)$ は (3.3)(3.4) を満たす。charming も全射性も profinite 側から降りる。ゆえに $[m,f]\in\mathrm{GT}(N)$ が**常に**定まる。$N$ isolated ゆえ source も $N$、すなわち $\mathrm{GTSh}(N,N)$ に入る。合成が (3.53) と両立することは還元の関手性による。∎
> **系(Chebotarev)**: $\widetilde\chi\circ\mathrm{Ih}_N=(\text{円分指標 mod } N_{\rm ord})$ は**全射**。$N_A$ では $(\mathbf Z/5)^\times\cong C_4$ の**全 4 値**が実現する。

これが v4 §4.1 証明の第 2 段(「合成 $G_{\mathbf Q}\to F_{20}\twoheadrightarrow(\mathbf Z/5)^\times$ は mod 5 円分指標であり、全射」)の中身であり、**硬い**(Chebotarev のみに依存)。

---

## 2. 委嘱 3 の訂正 — W3-8 の $u$ は $\widetilde\chi$ の値ではない

司令塔の判定材料 3 は「$u^{-1}=-2$ は $u\equiv-2\equiv3\bmod5$ = 非平方類」と読んでいるが、これは**型錯誤**である。

`u_meas_cal_a5_v1.md` の $u$ は **Kummer 助変数**(Belyi 写像の正規化から出る**有理数**)であり、その役割は

> 固定体も $L=K\bigl((u^{-1})^{1/5}\bigr)=\mathbf Q(\zeta_5,\sqrt[5]{-2})=\mathbf Q(\zeta_5,\sqrt[5]2)$ ✓(W3-8 と一致)

のように **5 乗根を取って体を作る**ことである。$\widetilde\chi([m,f])=2m+1\bmod N_{\rm ord}$ とは**別の量**で、$\bmod 5$ に還元して比べる意味はない($-2$ は $\mathbf Q^\times$ の元であって $(\mathbf Z/5)^\times$ の元ではない)。

> **⟹ W3-8 は「$u=3$ の shadow が像に入る」とは言っていない。**
> **しかし結論は v4 を支持する**: $L=\mathbf Q(\zeta_5,\sqrt[5]2)$、$\mathrm{Gal}(L/\mathbf Q)=F_{20}=C_5\rtimes C_4$ であり、その $C_4$ 商が mod 5 円分指標(= $\widetilde\chi$)。$\zeta_5\in L$ ゆえこの商は**全射** ⟹ $u$ は 4 値すべてを取る。
> **⟹ 三つ巴ではない。v4 と W3-8 は同一の事実($\mathrm{Gal}=F_{20}$・円分部分が全射)を二経路で述べている。対立しているのは pentagon 実測ただ 1 本である。**

---

## 3. 決定的論証 — pentagon 実測は**単独で**不可能(v4 も W3-8 も使わない)

> ### 定理 PENT-IMP【proof】
> 次の 4 つを仮定する:
> **(P1)** $K_\pi\in\mathrm{NFI}_{PB_4}(B_4)$ かつ $(K_\pi)_{PB_3}=N_A$(cert の主張)。
> **(P2)** $x_{12}$ の $PB_4/K_\pi$ での位数は 5(= $PB_4/K_\pi\cong A_5$ で $x_{12}$ が 5-巡回。cert の census が非自明であることから従う)。
> **(P3)** $G_{\mathbf Q}\subset\widehat{GT}$(古典)。
> **(P4)** 定理 REC(`pent_recoding_v1` §1): C1 の hexagon (2.18)(2.19) は 2401 の (3.3)(3.4) と**同一の方程式**。
> このとき **$u\equiv2$ および $u\equiv3\ (\mathrm{mod}\ 5)$ をもつ pentagon-live な gentle shadow が $\mathrm{GT}(N_A)$ の中に存在する。**
>
> **証明.**
> 1. $\gamma\in G_{\mathbf Q}$ の profinite 対 $(\lambda,\hat f)$ は $\widehat{PB_4}$ で pentagon を**厳密に**満たす((P3))。厳密式の還元だから、**任意の** $K\in\mathrm{NFI}_{PB_4}(B_4)$ で (2.20) が成立。hexagon も同様。ゆえに $\mathrm{Ih}_{K}(\gamma):=[(m_\gamma,\hat f\bmod K_{PB_3})]\in\mathrm{GT}(K)$ が定義される((P1))。
> 2. $\widetilde\chi(\mathrm{Ih}_K(\gamma))=\chi_{\rm cyc}(\gamma)\bmod K_{\rm ord}$。(P2) より $5\mid K_{\rm ord}$ なので、$\bmod 5$ に落とせば **Chebotarev により全射**。よって $\chi_{\rm cyc}(\gamma)\equiv2$ となる $\gamma$(例: $\gamma=\mathrm{Frob}_7$、$7\equiv2$)が存在し、その像は $u\equiv2$ をもつ。
> 3. その像の $f$ は $\hat f\bmod(K_\pi)_{PB_3}=\hat f\bmod N_A$((P1))で、対 $(m,f)$ は **(2.18)(2.19) を $B_3/N_A$ 内で満たす**。(P4) よりこれは 2401 の (3.3)(3.4) と同じ条件だから、$[m,f]$ は $N_A$ の charming GT-pair・全射 ⟹ **$\mathrm{GT}(N_A)$ の 20 元のいずれか**。
> 4. 同時に、その $f$ は 1. により **pentagon-live**。$u\equiv3$ も同様($\gamma=\mathrm{Frob}_3$)。∎

**実測**: cert の read A では $u\in\{2,3\}$ の 10 shadow が**すべて dead**。read B でも「$u$ の全 4 値が live」にはならず、しかも live 集合が部分群でない(`pent_recoding_v1` §3 で棄却済)。

> ### 帰結
> **(P1)–(P4) のいずれかが偽である。** (P3) は古典、(P4) は私が原文照合で証明済、(P2) は cert の非自明性から従う。
> **⟹ 疑いは (P1) に集中する — すなわち $K_\pi$ の $\mathrm{NFI}_{PB_4}(B_4)$ 性、または pentagon 判定式の実装(= 「実際に計算しているのは (2.20) の還元ではない」)。**
> **この論証は v4 も W3-8 も使わない。したがって「v4 を倒す」方向の再検分は不要である。**

---

## 4. 私の $G_{\mathbf Q(\sqrt5)}$ 仮説の撤回

> ### 撤回記帳 R-PENT-1
> `pent_recoding_v1.md` §4 の帰結 **(b)**「$N_A$ は $G_{\mathbf Q}$-安定でなく $G_{\mathbf Q(\sqrt5)}$-安定で、算術像はちょうど指数 2 の部分群」を**撤回する**。
> **理由**: 補題 ISO-Ih(§1.3)により、$N_A$ が isolated である限り $\mathrm{Ih}$ は $G_{\mathbf Q}$ 全体で定義され、$\widetilde\chi\circ\mathrm{Ih}$ は Chebotarev で全射。算術像が $\widetilde\chi^{-1}(\{\pm1\})$ に含まれることは**あり得ない**。$N_A$ の isolated 性は二系統確定済(v4 (I1))。
> 同 §4 の帰結 **(a)**(v4 L521 は保持できない)も**撤回**する。§3 の定理 PENT-IMP が、v4 に触れずに pentagon 側の欠陥を示すため。
> **残す**: §4 の論理の鎖 1–4(arithmetical ⟹ pentagon-live)と、live $=\widetilde\chi^{-1}(\{\pm1\})$ が指数 2 の部分群であるという観測、および read B の棄却。これらは正しい。

**なぜ私は誤ったか(記録)**: live 集合が $\widetilde\chi^{-1}(\text{平方})$ と完全一致するという**美しい符合**に引かれ、「$\mathrm{Ih}$ の定義域が狭い」という逃げ道を作ってしまった。逃げ道は Chebotarev で塞がっている。**符合が美しいときほど、それが「装置の側の構造」でないかを先に疑うべきだった** — 実際 §5 のとおり、$u$ で完全に決まる live/dead は装置由来の署名として自然である。

---

## 5. 欠陥の探索先(優先順・司令塔と implementer 向け)

1. **【第一容疑】向き規約の反転($f\leftrightarrow f^{-1}$ 型)**。hexagon で実際に起きた事故と同型(`hexagon_orientation_ruling_v1.md`)。cert の `f_orientation: abstractprod_reversed_matching_paB_compAll` という欄名と readA/readB の併存が、まさに未決の規約が残っている兆候。
 **診断法**: pentagon 判定を $f$ と $f^{-1}$ の両方で走らせ、live 集合が入れ替わるかを見る。もし $\{f^{-1}:f\ \text{live}\}$ が $u\in\{2,3\}$ 側を拾うなら**それが答**。
2. **$K_\pi$ の定義**: $\pi^{-1}(N_A)$ か $\pi^{-1}(N_A)\cap PB_4$ か。**前者は $PB_4$ に含まれない**(核 $V_4$ の分が乗る・`pent_recoding_v1` §4.1 で証明済)ので圏の外。cert のどちらかを確認。
3. **coface 像の関係式の全数検査**: (A.2)(A.3) の $PB_4$ 表示関係式を、6 生成元の像 $g_{12},\dots,g_{34}$ が**すべて**満たすか(cert の `B4_relations_on_images` が何本を検査したか)。1 本でも落ちれば $\varphi$ は準同型でなく、(2.20) の還元を計算していないことになる。
4. **$\pi$-lift の退化**: $\pi(\sigma_3)=\sigma_1$ ゆえ $x_{34}\mapsto x_{12}$。**live/dead が $u$ だけで決まる**という実測の署名は、pentagon が「$\bar x\mapsto\bar x^{\pm1}$ 型の条件」に退化していることを示唆する。$\varphi_{234}$ が $\pi$ 下で $\theta$($x\leftrightarrow y$)に落ちることは紙で確認できる(§5.1)。
5. **calibration の射程**: 装置は $N^{(34)}$(**直接の $B_4$ 窓**)で 4096/254016 を再現したが、**$\pi$-lift 経路そのものは未較正**。$N^{(34)}$ の $PB_3$-部を $\pi$-lift して census を取り直し、直接計算と一致するかを見るのが最短の較正。

### 5.1 紙で確認できる退化(参考)

$\pi$($\sigma_3\mapsto\sigma_1$)の下で余面像は
$$\varphi_{123}\rightsquigarrow \mathrm{id},\qquad \varphi_{234}\rightsquigarrow\ (x\mapsto y,\ y\mapsto x)\ =\ \theta,$$
$$\varphi_{12,3,4}\rightsquigarrow(x\mapsto x_{13}x_{23},\ y\mapsto x),\quad \varphi_{1,23,4}\rightsquigarrow(x\mapsto x_{12}x_{13},\ y\mapsto x_{24}x_{34}),\quad \varphi_{1,2,34}\rightsquigarrow(x\mapsto x,\ y\mapsto x_{23}x_{24}).$$
すなわち $\pi$-lift の pentagon は **$f$、$\theta(f)$ とその捻れ**だけの関係式に落ちる。$\theta$ は hexagon (H-a) の主役でもあるので、**この窓では pentagon が hexagon 側の情報を再言しているだけになる危険**がある。$u$ だけで live/dead が決まる実測は、その危険が現実化した署名と読める(**candidate**)。

---

## 6. v4 への提案(erratum ではなく補強)

- **erratum は不要**(§1・§3)。「20 全て arithmetical」は $\mathbf Q$ 上の主張として正しく述べられている。
- **補うべき 1 点**: (I1) の言い換えを **補題 ISO-Ih**(§1.3)として明示すること。v4 は「(I1) = $N_A$ は isolated」と等置しているが、**「isolated ⟹ $\mathrm{Ih}$ が $G_{\mathbf Q}$ 全体で定義される」の一行**が本文にない。§3 の論証はこの一行に依存するので、正本化しておくと以後の裁定が速い。
- **W3-8 の引用の仕方**: 「$u^{-1}=-2$」を $\bmod5$ の類として使わないこと(§2)。使ってよいのは「固定体が $\mathbf Q(\zeta_5,\sqrt[5]2)$、$\mathrm{Gal}=F_{20}$、円分部分が全射」という形。

---

## 7. 格付け

| 主張 | 格 |
|---|---|
| 補題 ISO-Ih(isolated ⟹ $\mathrm{Ih}$ は $G_{\mathbf Q}$ 全体で定義・$\widetilde\chi$ 全射) | **proof** |
| $L$ = rigidification 体、moduli 体 = $\mathbf Q$(委嘱 1) | **proof**(v4 命題 M の注と整合) |
| W3-8 の $u$ は Kummer 助変数($\widetilde\chi$ の値ではない)(委嘱 3) | **proof**(原文) |
| **定理 PENT-IMP**(pentagon 実測は (P1)–(P4) と両立しない) | **proof** |
| $G_{\mathbf Q(\sqrt5)}$ 仮説・「v4 は保持できない」の**撤回** | **撤回記帳 R-PENT-1** |
| 欠陥の所在((P1) = $K_\pi$ か実装) | **candidate**(§5 に診断法) |
| $\pi$-lift 退化の署名($\varphi_{234}\rightsquigarrow\theta$) | **紙で確認・candidate** |

**本稿は新しい機械計算を行っていない**(cert の生値・v4・W3-8・C1/2401 原文の照合のみ)。**pentagon 側を「合わせる」操作は一切していない** — §3 は実測を使わずに実測の不可能性を示している。
