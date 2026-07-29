# 構造定理試行 v1 — H²(Q;K) と「分裂 3/3 は必然か」の判定

作成: 数学者(Opus 5)・2026-07-29 W4 第一波
入力: 裁定 205 / `search/certs/w62_splitting_20260729.json` / `docs/notes/specimen_zoo_v1.md`(裁定 195 解剖所見)/ `docs/地図.md` 帯 1 / 司令塔追加照準(発案係 I7-1)
計算: `search/_probe_structthm_h2.g`(第 1 段)・`search/_probe_structthm_witness.g`(第 2 段)・`search/_probe_structthm_counterex.g`(付録)
証明書: `search/certs/.structthm_W-D-A{16,18,20}-*.json`・`search/certs/.structthm_wit_W-D-A{16,18,20}-*.json`

---

## 0. 結論(3 行)

1. **判定 = 必然ではない**。$H^2(Q;Z(K))\cong H^2(Q;C_2)$ は三窓で $C_2,\;C_2,\;C_2^3$ と**消滅しない**。直積を成立させている拡大類 $\varepsilon$ は 1/1/3 ビットの真の情報量を持ち、それがたまたま(あるいは未知の機構により)$0$ である。**「$H^2$ の該当成分消滅」という説明は成り立たない**。
2. しかし**結論そのものは 3/3 で成立し、しかも 205 の予想より強い形で確定した**: **GTSh(D4 窓) ≅ $D_8 \times \mathrm{Hol}(\mathbb{Z}/N_{\rm ord})$**(明示同型を GAP が構成・三窓)。$\mathrm{Hol}$ 因子は S1/S3/S4/S5 窓で既に出ていた「素直な答」そのもの(`docs/week4-E2作戦_v1.md` 付録 A)であり、**D4 窓はその素直な答に $D_8$ が丸ごと外積されただけ**という形。
3. **裁定 205 の推論は論理的に穴があった**(結論は正しかったが理由が足りない)。「分裂 + KE-o ⟹ 直積」は**偽**である — 反例 $D_8\rtimes C_2 \cong D_8\circ C_4$ を機械で確認した(§6;数学者・発案係 I7-1・Sol 便 84 が独立同着)。しかも **205 が記録した witness 自身が三窓とも $D_8$ を中心化しない**(§5)ので、穴は仮想ではなく実在した。埋めたのが本ノートの $\varepsilon$ と §5 の取り直しである。

---

## 1. 設定と実測入力(事前登録済の量のみ)

三窓 $W \in \{$W-D-A16-11a, W-D-A18-13a, W-D-A20-15a$\}$、$G = \mathrm{GTSh}(N,N)$、$K=\ker\tilde\chi$、$Q=\mathrm{im}\,\tilde\chi = G/K$。

| 窓 | $N_{\rm ord}$ | $|G|$ | $K$ | $Q$ | $\gcd(N,|Q|)$ |
|---|---|---|---|---|---|
| A16-11a | 11 | 880 | $C_{11}\times D_8$ | $C_{10}$ | 1 |
| A18-13a | 13 | 1248 | $C_{13}\times D_8$ | $C_{12}$ | 1 |
| A20-15a | 15 | 960 | $C_{15}\times D_8$ | $C_4\times C_2$ | 1 |

新規実測(第 2 段):**三窓とも $Q \cong \mathrm{Aut}(C_{N})=(\mathbb{Z}/N)^\times$ で、$C_N$ 上の作用は忠実**($|Q| = \varphi(N)$・作用の核 = 1)。すなわち $\tilde\chi$ は $(\mathbb{Z}/2N)^\times$ へ**全射**。

**用語の確定(重要)**: KE-o(裁定 202)が測ったのは「$Q$ は $K^{\rm ab}$ の 2-部分を固定」である。$\ker\bigl(\mathrm{Aut}(D_8)\to \mathrm{Aut}(D_8^{\rm ab})\bigr)=\mathrm{Inn}(D_8)$ ゆえ、これは群論的には

> **(H3) $G = D_8\cdot C_G(D_8)$**(= $Q$ は $D_8$ に**内部自己同型としてしか**作用しない)

と**同値**であって、「$D_8$ に自明作用」**ではない**。実測でも $|G/C_G(D_8)| = 4 = |\mathrm{Inn}(D_8)|$(三窓)、つまり $G\to\mathrm{Aut}(D_8)$ の像はちょうど $\mathrm{Inn}(D_8)$ で、しかもそれは $D_8$ 自身が既に出している。裁定 205 §「KE-o(Q は D₈ 部分に自明作用)」は表現が強すぎる。

---

## 2. 還元定理(本ノートの主結果・証明つき)【STR-1】

尾部 8 転回案に直接使えるよう、$D_8$ ではなく一般の 2-部分で述べる。

> **定理 STR-1.** 有限群 $G$、正規部分群 $K\trianglelefteq G$、$Q = G/K$ とし、次を仮定する。
> - **(H1)** $K = A\times S$、$A$ は奇位数アーベル、$S=\mathrm{Syl}_2(K)$、$Z(S) = \langle z\rangle \cong C_2$。
> - **(H2)** $\gcd(|A|,|Q|)=1$。
> - **(H3)** $G = S\cdot C_G(S)$($G$ は $S$ に内部自己同型としてしか作用しない)。
>
> このとき:
> **(1)** $A,S \trianglelefteq G$、$z \in Z(G)$、$G = S \circ_{\langle z\rangle} C_G(S)$(中心積)、$|C_G(S)| = |A|\,|Q|\cdot 2$。
> **(2)** $\bar C := C_G(S)/A$ は**中心拡大** $1\to\langle z\rangle\to\bar C\to Q\to 1$ を与える。その類を $\varepsilon\in H^2(Q;C_2)$(自明作用)とおく。
> **(3)** 次は同値:
>  (a) $G\cong S\times (A\rtimes Q)$;
>  (b) $K$ の補群を $C_G(S)$ の**内部に**取れる;
>  (c) $\varepsilon = 0$;
>  (d) $z\notin \Phi\bigl(\mathrm{Syl}_2(\bar C)\bigr)$。
> **(4)** (a) が成り立てば $\mathrm{Syl}_2(G)\cong S\times \mathrm{Syl}_2(Q)$ かつ $\mathrm{dl}(G) = \max\bigl(\mathrm{dl}(S),\,\mathrm{dl}(A\rtimes Q)\bigr)$。
> **(5)** $H^2(Q;Z(K)) \cong H^2(Q;C_2)$($H^2(Q;A)=0$ は (H2) による)。
> **(6)** $\mathrm{Syl}_2(Q)$ が**巡回**なら、$\varepsilon=0$ $\iff$ $\mathrm{Syl}_2(Q)$ の唯一の位数 2 元 $\iota$ の $C_G(S)$ における逆像が、$A\langle z\rangle$ の外に位数 2 の元を含む。

### 証明

**(1)** $A$ は $K$ の Hall $2'$-部分群、$S$ は $K$ の Sylow 2-部分群で、(H1) より $K$ は冪零だから両者は $K$ の特性部分群、よって $G$ で正規。$Z(S)$ は $S$ の特性部分群ゆえ $G$ で正規で位数 2、したがって $G/C_G(z)\hookrightarrow \mathrm{Aut}(C_2)=1$、つまり $z\in Z(G)$。(H3) より $G = S\,C_G(S)$、$S\cap C_G(S) = Z(S)=\langle z\rangle$ だから $G$ は中心積で $|C_G(S)| = 2|G|/|S| = 2|A||Q|$。

**(2)** $A\le C_G(S)$($K=A\times S$ より)かつ $A\trianglelefteq G$ なので $\bar C$ は定義できる。$C_G(S)\cap K = C_K(S) = A\times\langle z\rangle$、また $C_G(S)K = C_G(S)SA = G$ ゆえ $C_G(S)/(A\times\langle z\rangle)\cong G/K = Q$。よって $\bar C$ は $\langle \bar z\rangle\cong C_2$ による $Q$ の拡大で、$z\in Z(G)$ より中心的。

**(3)**
- **(c)⟹(b)**: $\varepsilon=0$ なら $\bar C = \langle\bar z\rangle\times \bar Q$、$\bar Q\cong Q$。$Y := $ $\bar Q$ の $C_G(S)$ における逆像は位数 $|A||Q|$、$A\le Y$。$Y\cap K \le C_G(S)\cap K = A\times\langle z\rangle$ で、その $\bar C$ での像は $\bar Q\cap\langle\bar z\rangle = 1$ ゆえ $Y\cap K = A$。(H2) と Schur–Zassenhaus より $A$ の $Y$ における補群 $H\cong Q$ が存在し、$H\le C_G(S)$、$H\cap K = H\cap A = 1$、$|H||K|=|G|$。
- **(b)⟹(a)**: $H\le C_G(S)$ を $K$ の補群とする。$AH$ は位数 $|A||Q|$ の部分群。$S\cap AH \le K\cap AH = A(H\cap K) = A$ かつ $S\cap A=1$ ゆえ $S\cap AH=1$。$S\cdot AH = SAH = KH = G$。$[S,A]=1$ と $[S,H]=1$ より $[S,AH]=1$。ゆえに $G = S\times AH$ で、$AH$ は $A$ の $Q$ による拡大で分裂(Schur–Zassenhaus)、$AH \cong A\rtimes Q$。
- **(a)⟹(c)**: $G = S\times X$ なら $C_G(S) = Z(S)\times X$ ゆえ $\bar C = \langle\bar z\rangle\times (X/A)$、$\varepsilon=0$。
- **(c)⟺(d)**: $\langle\bar z\rangle$ は $\bar C$ のアーベル正規 2-部分群だから、Gaschütz の定理より補群の存在は $\mathrm{Syl}_2(\bar C)$ 内での補群の存在と同値。2-群 $T$ の中心にある位数 2 の $\langle z\rangle$ が直和因子 $\iff$ $z\notin\Phi(T)$(⟸: $z\notin\Phi(T)$ なら $z\notin M$ なる極大部分群 $M$ が存在し、$z$ 中心ゆえ $T = \langle z\rangle\times M$。⟹: $T=\langle z\rangle\times M$ なら $\Phi(T)=\Phi(M)\le M\not\ni z$)。

**(4)** $G = S\times X$ なら $\mathrm{Syl}_2(G) = S\times \mathrm{Syl}_2(X)$、$X = A\rtimes Q$ で $A$ 奇位数ゆえ $\mathrm{Syl}_2(X)\cong \mathrm{Syl}_2(Q)$。導来長は直積で $\max$。

**(5)** $Z(K) = A\times\langle z\rangle$($A$ アーベル)で $Q$-加群として直和。(H2) より $H^i(Q;A)=0\ (i\ge1)$。$z$ は $Z(G)$ にあるから $\langle z\rangle$ は自明 $Q$-加群。

**(6)** $H^2(Q;C_2)$ は 2-torsion だから制限 $\mathrm{res}: H^2(Q;C_2)\to H^2(Q_2;C_2)$($Q_2=\mathrm{Syl}_2(Q)$)は単射($\mathrm{cor}\circ\mathrm{res} = [Q:Q_2]\cdot\mathrm{id}$ で指数は奇)。$Q_2$ 巡回位数 $2^a$ のとき $H^2(Q_2;C_2)=C_2$ で、非自明類は拡大 $C_{2^{a+1}}\twoheadrightarrow C_{2^a}$ に対応し、これを唯一の位数 2 部分群へ制限すると位数 4 の巡回群 = 非分裂。よって $\mathrm{res}:H^2(Q_2;C_2)\to H^2(\langle\iota\rangle;C_2)$ も単射。合成が単射だから $\varepsilon = 0 \iff \langle\iota\rangle$ 上への制限が分裂 $\iff$ $\iota$ の $\bar C$ における逆像($\cong C_2\times C_2$ or $C_4$)が $C_2\times C_2$。$\square$

**注(なぜ「分裂」では足りないか)**: (3) の (b) は「補群が $C_G(S)$ の**中に**取れる」であって、単なる「補群が存在する」ではない。両者は**同値でない** — §6 の反例。

---

## 3. $H^2$ の計算(必然性の判定)

$Q$-加群 $Z(K) = C_N\times C_2$、$Q$ は $C_2=Z(D_8)$ に自明作用。STR-1(5) より $H^2(Q;Z(K))\cong H^2(Q;C_2)$(自明作用)。

| 窓 | $Q$ | $\dim_{\mathbb F_2}Z^2$ | $\dim B^2$ | $\dim H^2(Q;C_2)$ | $|H^2|$ | HAP `GroupCohomology(Q,2,2)` | 手計算 |
|---|---|---|---|---|---|---|---|
| A16 | $C_{10}$ | 2 | 1 | **1** | 2 | `[ 2 ]` | $M/10M=\mathbb F_2$ ✔ |
| A18 | $C_{12}$ | 3 | 2 | **1** | 2 | `[ 2 ]` | $M/12M=\mathbb F_2$ ✔ |
| A20 | $C_4\times C_2$ | 4 | 1 | **3** | 8 | `[ 2, 2, 2 ]` | Künneth $1+1+1=3$ ✔ |

3 系統(GAP `TwoCocycles/TwoCoboundaries`・HAP `GroupCohomology`・手計算)一致。

> ### 判定:**必然ではない(NOT FORCED)**
> $H^2(Q;Z(K)) \neq 0$。$(K,Q,\text{結合類})$ という抽象データだけからは直積も分裂も出ない。$\varepsilon=0$ は 1+1+3 = **5 ビットの実質情報**であり、一様乱択なら $1/2\cdot1/2\cdot1/8 = 1/32$ の事象。

### 3.1 計算した $H^2$ の**型**の明記(Sol F84-2.2 の必須要求への回答)

**答: (ii) 中心障害 $H^2(Q;Z(D_8)) = H^2(Q;C_2)$ である。(i) ではない。**

- $K$ は非可換だから $H^2(Q;K)$ という群は**存在しない**。正確には:結合類 $\psi:Q\to\mathrm{Out}(K)$ の障害は $H^3(Q;Z(K))$ にあり、消えるとき拡大の同値類の集合は $H^2(Q;Z(K))$ の単純推移的作用を受ける(Eilenberg–MacLane)。司令塔スペックの「$H^2(Q;K)$」はこの意味で $H^2(Q;Z(K))$ と読み替えた。
- そして本ノートで実際に使う $\varepsilon$ は **$K$-拡大の類ではない**。**W84-1(Sol)への回答**: 仰るとおり $1\to K\to G\to Q\to1$ は既に分裂しており、その「類が 0」を言っても何も進まない — 同じ $\psi$ を持つ**分裂拡大が複数ある**(持ち上げ $\varphi:Q\to\mathrm{Aut}(K)$ の取り方だけ違う半直積が互いに非同型になりうる)からである。§6 の $\Gamma = D_8\rtimes C_2 \cong D_8\circ C_4$ はまさにその実例(分裂だが直積でない)。
- $\varepsilon$ が住む拡大は**別の短完全列**:
 $$1\;\longrightarrow\;Z(D_8)=\langle z\rangle\;\longrightarrow\;C_G(D_8)/C_N\;\longrightarrow\;Q\;\longrightarrow\;1 \qquad(\text{中心拡大})$$
 これは Sol が名指しした「lift の積ずれ $d(q_1)d(q_2)d(q_1q_2)^{-1}\in Z(D_8)\cong C_2$」の類そのものである(KE-o により各 $q\in Q$ は $D_8$ 上 $\mathrm{conj}_{d(q)}$ で作用し、$d$ は $D_8/Z(D_8)$ への準同型としてしか定まらない;その持ち上げの積ずれが 2-コサイクル)。**見るべき係数は $Z(D_8)$** — Sol の指定と一致する。
- 上表の GAP/HAP の値はすべてこの $H^2(Q;C_2)$(自明作用)であり、$K$-拡大の類ではない。

---

## 4. 実測結果(直積は成立・しかも Hol として同定)【STR-2:実測命題】

| 窓 | $|C_G(D_8)|$ | $G=D_8\!\cdot\!C_G(D_8)$ | $\bar C$ | $\varepsilon=0$ | $z\in\Phi$? | $\mathrm{Syl}_2(G)$ | **直積** | $X$ |
|---|---|---|---|---|---|---|---|---|
| A16 | 220 | true | $C_{10}\times C_2$ | **true** | false | $C_2\times D_8$ | **true** | $C_{11}\!:\!C_{10}$ |
| A18 | 312 | true | $C_{12}\times C_2$ | **true** | false | $C_4\times D_8$ | **true** | $C_{13}\!:\!C_{12}$ |
| A20 | 240 | true | $C_4\times C_2\times C_2$ | **true** | false | $C_2\times C_4\times D_8$ | **true** | $(C_5\!:\!C_4)\times S_3$ |

さらに第 2 段で **明示同型を構成**:

> **$G \;\cong\; D_8 \times \mathrm{Hol}(\mathbb{Z}/N_{\rm ord})$**、三窓とも `IsomorphismGroups` が `fail` を返さない(A16: $8\times110$、A18: $8\times156$、A20: $8\times120$)。

$\mathrm{Hol}(\mathbb{Z}/N)=C_N\rtimes\mathrm{Aut}(C_N)$。$\mathrm{Hol}(\mathbb{Z}/15) = S_3\times(C_5\!:\!C_4)$ が A20 の $X$ と一致する点まで込みで確認。

**文脈(grep 済)**: `docs/week4-E2作戦_v1.md` 付録 A で、settled な case A 窓 S1/S3/S4/S5 の GTSh は正規化群 $\mathrm{Hol}(C_7),\mathrm{Hol}(C_7),\mathrm{Hol}(C_9),\mathrm{Hol}(C_{11})$ と一致していた。**したがって D4 窓の内容は「素直な答 $\mathrm{Hol}(C_N)$ に $D_8$ が外積で乗る」**であり、$D_8$ は $\mathrm{Hol}$ と一切干渉しない。$|GTSh| = 8\cdot N\cdot\varphi(N)$。

**格付け**: GAP 単系統の実測(**cross-checked ではない**)。独立照合器(証明書だけを入力に $D_8$ 因子と $\mathrm{Hol}$ 因子の元ごとの可換性を再計算)は未実装 —【要実装】。

---

## 5. 司令塔追加照準(I7-1)への直接回答

- **①「$Q$ の作用が $D_8$ 因子上($K^{\rm ab}$ でなく $K$ 自身の上)で内部自己同型を経由していないか」**
 → **経由している**。$|G/C_G(D_8)| = 4 = |\mathrm{Inn}(D_8)|$(三窓)。$G\to\mathrm{Aut}(D_8)$ の像はちょうど $\mathrm{Inn}(D_8)$ で、これは $D_8$ 自身の寄与で尽きている($D_8C_G(D_8)/C_G(D_8)\cong D_8/Z(D_8)$ が既に位数 4)。**先験的には中心積の場面であり、直積であることは別途の 1(〜3)ビット**。指摘は完全に正しい。
- **②「補群 $H$ を $C_G(\mathrm{Syl}_2$ 因子$)$ 内に取り直せるか」= Sol P84-1(最短の決定打)**
 → **三窓とも YES**。$\mathrm{ComplementClassesRepresentatives}(C_G(D_8),\,C_G(D_8)\cap K)$ が非空:

| 窓 | $K$ の補群クラス(全体) | うち $D_8$ を中心化 | $C_G(D_8)$ 内で取り直した補群 |
|---|---|---|---|
| A16 | 4 | **2** | $C_{10}$、witness $m=3,\ u=7,\ \mathrm{ord}_G=10$ |
| A18 | 5 | **2** | $C_{12}$、witness $m=2,u=5,\mathrm{ord}=4$ / $m=1,u=3,\mathrm{ord}=3$ |
| A20 | 18 | **4** | $C_4\times C_2$、witness $m=3,u=7,\mathrm{ord}=4$ / $m=8,u=17,\mathrm{ord}=4$ |

 shadow 座標つき witness は `search/certs/.structthm_wit_*.json` の `complement_witness_in_CG_D8`。全体の補群クラスのうち $D_8$ を中心化するのは 2/4・2/5・4/18 と**少数派**。

 **さらに:裁定 205 が実際に記録した witness 自身を検査した**(`search/_probe_structthm_w205*.g`、証明書 `w62_splitting_20260729.json` から逐語):

| 窓 | 205 の witness | $\mathrm{ord}_G$ | $[\,\cdot\,,D_8]=1$? |
|---|---|---|---|
| A16 | $m=3$ | 10 | **false** |
| A18 | $m=2$ / $m=1$ | 4 / 3 | **false** / true |
| A20 | $m=3$ / $m=5$ | 4 / 2 | true / **false** |

 **三窓すべてで、205 の補群は $C_G(D_8)$ に入っていない**。すなわち **205 の witness からは直積は出せなかった** — 取り直しは形式ではなく本質だった。
- **③「直積か中心積か」** → **直積**(三窓)。ただし理由は「作用が自明だから」ではなく「中心拡大類 $\varepsilon$ が消えるから」。

---

## 6. 裁定 205 の推論の訂正(機械確認した反例)

> 205: 「分裂 + KE-o(Q は D₈ 部分に自明作用)を合わせると **GTSh ≅ D₈ × (C_N ⋊ Q)** の疑い」

この含意は**一般には偽**。最小反例($|{\cdot}| = 16$、`search/_probe_structthm_counterex.g` で機械確認)。
**三者独立に同じ反例に到達**した:数学者(本ノート)・発案係(ideas_007 I7-1、中心積として予告)・Sol(便 84 F84-2.2、$tdt^{-1}=rdr^{-1}$ と紙上で構成)。Sol の反例と下の $\Gamma$ は同一の群である。

$$\Gamma := D_8\rtimes_\varphi C_2,\qquad \varphi(t) = \mathrm{conj}_r\ (r\in D_8,\ \mathrm{ord}(r)=4)$$

- $D_8\trianglelefteq\Gamma$、作用は**内部**($\Gamma = D_8\cdot C_\Gamma(D_8)$、すなわち KE-o 相当が成立)
- $\Gamma$ は $D_8$ 上**分裂**(定義から補群 $C_2$ が存在)
- しかし正規な補群は **0 個**、$\Gamma\not\cong D_8\times C_2$、$C_\Gamma(D_8)\cong C_4$、$\Gamma \cong D_8\circ C_4$(GAP の名前は `(C4 x C2) : C2`)、$\varepsilon\neq0$

**結論**: 205 の結論(直積)は正しかったが、そこに至る推論は不完全だった。正しい十分条件は STR-1(3)(b)/(c)、すなわち「補群を $C_G(D_8)$ 内に取れる」= 「$\varepsilon = 0$」であり、それは §5 で新たに検証した。

---

## 7. 部分機構と残るギャップ

### 7.1 $u=-1$ 層(複素共役の層)の観察
$u\equiv-1$ の層に「位数 2 かつ $D_8$ を中心化する shadow」が**三窓とも存在**: 個数は 22 = 2·11、26 = 2·13、30 = 2·15(= $|Z(D_8)|\cdot N$)。
STR-1(6) と合わせると:

> **系 STR-1.6.** $\mathrm{Syl}_2(Q)$ が巡回のとき、**「$u=-1$ の層に位数 2 で $D_8$ を中心化する shadow が 1 つある」だけで直積が従う**。

A16($Q_2=C_2$)・A18($Q_2=C_4$)はこれで尽きる。A20 は $Q_2 = C_4\times C_2$ が非巡回なので **2 ビットが残る**。
**運用上の価値**: 新窓では補群クラスの全列挙(A20 で 18 クラス)をせずとも、$u=-1$ 層を 1 回走査して involution を探すだけで判定できる($Q_2$ 巡回の場合)。

### 7.2 なぜ $f=1$ の標準切断ではだめか
$f=1$ の shadow 全体は積で閉じる(合成則 $(m_1,1)\cdot(m_2,1) = (m_1\!\circ\!m_2,\,1)$)ので常に部分群 $T\le G$ をなし、$T\cap K = 1$。しかし実測では
$T = C_2$($u\in\{1,-1\}$、A16)、$T = 1$(A18・A20 — **$(u=-1,f=1)$ は shadow ですらない**)。
つまり「複素共役 $(−1,1)$ は常に GT-shadow」という素朴な期待は**この設定では偽**。A16 だけが $(-1,1)$ を持つ。したがって §7.1 の involution は $f\neq1$ のものを使わざるを得ず、その存在は現状**実測**である。

### 7.3 残るギャップ(明示)
> **【GAP-1】** $\varepsilon = 0$ の**機構が不明**。5 ビットが 3 窓で全て 0 になる理由は、$(K,Q,\psi)$ からは出ない。GT-shadow の算術($R_\tau$ 条件・$f\tilde\theta(f)=1$)から来る何かのはずだが、本ノートでは特定できていない。
> **【GAP-2】** $Q\cong\mathrm{Aut}(C_N)$(全射 $\tilde\chi$)と $K$ の 2-部分がちょうど $D_8$ になることも実測であり、証明されていない。
> **【GAP-3】** STR-1 の (H2) $\gcd(|A|,|Q|)=1$ は $N=11,13,15$ では成立するが、**$N=9$ では $\gcd(9,6)=3$ で破れる**。A₁₄ 枝 A 予言(432 = 8·9·6 = $|D_8\times\mathrm{Hol}(\mathbb{Z}/9)|$)の形はまさに $N=9$ なので、その族に STR-1 を適用するには (H2) を外した版が要る(Schur–Zassenhaus が使えず (c)⟹(b) が通らない)。**再利用時の注意**。

> **【文献要請】**
> **困難**: 有限 GT-shadow 群 $G=\mathrm{GTSh}(N,N)$ について、$S=\mathrm{Syl}_2(\ker\tilde\chi)$ の中心 $Z(S)\cong C_2$ による中心拡大 $1\to Z(S)\to C_G(S)\to G/S\to 1$ が**なぜ分裂するのか**(三窓で実測 0、$H^2$ は非零)。
> **欲しい結果の型**: (i) $\widehat{GT}$ / $\mathrm{GT}(K^{(n)})$ における**複素共役元の位数 2 性が有限 shadow 商へ降りる**ための十分条件(2401.06870 / 2405.11725 の枠内で言えることは何か)。(ii) 「$\mathbb{Z}/2$ による中心拡大が、群が**ある自然な対合を持つ**ことから分裂する」型の一般機構(実形・spinor norm・Galois descent いずれの語彙でも可)。(iii) $\mathrm{Hol}(\mathbb{Z}/N)$ の $C_2$ による中心拡大の分類と、そのうち「算術的に実現されるもの」の特徴づけ。

---

## 8. 尾部 8 転回案への含意(裁定 206 の「列挙せず定理で」)

STR-1 は $D_8$ を一般の $S=\mathrm{Syl}_2(K)$ で述べてあるので、そのまま使える。

- **良い知らせ**: $\mathrm{dl}(\mathrm{Syl}_2(S_{2^n})) = n$(反復輪積 $C_2\wr\cdots\wr C_2$)。$\mathrm{Hol}(\mathbb{Z}/\ell)=C_\ell\rtimes(\mathbb{Z}/\ell)^\times$ は $\mathrm{dl}=2$。よって直積が成り立てば STR-1(4) より
 $$\mathrm{dl}(\mathrm{GTSh}) = \max\bigl(\mathrm{dl}(\mathrm{Syl}_2(S_t)),\,2\bigr) = 3 \iff t\ge 8 .$$
 これは裁定 206 の「dl 跳躍点 $t=8$($S_t$ 側)」を**そのまま説明する**。$t\le7$ では $\mathrm{Syl}_2(S_t)\in\{D_8,\,D_8\times C_2\}$ で $\mathrm{dl}=2$、$t=8$ で初めて 3。**尾部 8 で dl-3 が出るのは列挙の偶然ではなく、直積構造の帰結**という筋が立つ。
- **悪い知らせ(転回案の穴)**: その筋は **$\varepsilon = 0$ を前提にしている**。$\varepsilon$ は $H^2(Q;C_2)\neq0$ に住む本物の自由度で、$t$ が大きいほど (H3)($Q$ が $\mathrm{Syl}_2(S_t)$ に内部作用のみ)も強い仮定になる($\mathrm{Out}(\mathrm{Syl}_2(S_8))$ は $\mathrm{Out}(D_8)=C_2$ より大きい)。**「列挙せず定理で得る」には、$\varepsilon=0$ と (H3) を窓ごとに測る(または証明する)工程が必ず要る**。ただしその工程は §7.1 のとおり非常に安い($Q_2$ 巡回なら $u=-1$ 層の involution 探索 1 回)。

---

## 9. 登録する予言(反証可能・追加費用ほぼゼロ)

次に打つ D4 型窓(裁定 207 手続き (ii) の A₁₃ 打撃など)について、**打つ前に**以下を凍結する。

- **P-STR-1**: $K = C_\ell\times \mathrm{Syl}_2(K)$、$Q\cong(\mathbb{Z}/\ell)^\times$ が $C_\ell$ に忠実(すなわち $\tilde\chi$ 全射)。
- **P-STR-2**: (H3) 成立($|G/C_G(\mathrm{Syl}_2(K))| = |\mathrm{Inn}(\mathrm{Syl}_2(K))|$)。
- **P-STR-3**: $\varepsilon = 0$、すなわち $\mathrm{GTSh}\cong \mathrm{Syl}_2(K)\times\mathrm{Hol}(\mathbb{Z}/\ell)$、$|\mathrm{GTSh}| = |\mathrm{Syl}_2(K)|\cdot\ell\cdot\varphi(\ell)$。
- **P-STR-4**: $u=-1$ の層に位数 2 かつ $\mathrm{Syl}_2(K)$ を中心化する shadow がちょうど $2\ell$ 個。
- **反証されたら**: $\varepsilon\ne0$ の実例 = **中心積型 GT-shadow の第一標本**であり、それはそれで標本庫入り(病理: CENTRAL-PRODUCT)。どちらに転んでも領土が増える。

---

## 10. 定理 candidate(Sol ゲートへ回す形)

> **【定理 candidate STR-1】**(§2・証明つき・純群論)
> (H1)(H2)(H3) の下で (a)⟺(b)⟺(c)⟺(d)、および (4)(5)(6)。
> **証明の負担**: すべて標準的(特性部分群・中心積・Gaschütz・Schur–Zassenhaus・制限写像の単射性)。**Lean 化候補**としても素直(有限群の等式のみ・数論層なし)。
> **監査してほしい点**: (3)(c)⟹(b) での Schur–Zassenhaus の使い方((H2) が本当に必要か・$A$ 非アーベルへ緩められるか)、(6) の $\mathrm{res}$ 単射性の議論。

> **【実測命題 STR-2】**(§4・GAP 単系統)
> W-D-A{16,18,20} の三窓で $\mathrm{GTSh}(N,N)\cong D_8\times\mathrm{Hol}(\mathbb{Z}/N_{\rm ord})$、$N_{\rm ord}=11,13,15$。
> **格付け**: measured(cross-checked ではない)。独立照合器が付けば cross-checked に昇格可。

> **【判定 STR-3】**(§3)
> 分裂/直積は **$H^2$ の消滅では説明されない**。$H^2(Q;Z(K))\cong C_2,C_2,C_2^3$。$\varepsilon=0$ は 5 ビットの実測事実。

---

## 11. 新規性の申告(grep 済)

`grep -rniE "holomorph|Hol\(C|Hol\(Z" docs/ sol/ ideas/ provenance/` および `grep -rn "中心積" docs/ sol/ ideas/` を実行済。

- **既出**: 直積疑い・分裂 3/3・転回案(裁定 205/206)。$\mathrm{Hol}(C_N)$ という群自体(week4-E2 の case A 窓・PSL 封印計算)。中心積に落ちる可能性・KE-o の測定水準($K^{\rm ab}$)と $D_8$ 本体の Inn ギャップ・「補群を $C_G$ 内に取り直す 1 ビット」(**発案係 ideas_007 I7-1、本セッション同時刻**)。
- **本ノートで新規**: (i) 還元定理 STR-1(TFAE + 証明・一般の $S=\mathrm{Syl}_2(K)$ 版)、(ii) $H^2(Q;Z(K))$ の実計算と「**必然ではない**」の確定、(iii) D4 窓の $\mathrm{GTSh}$ を **$D_8\times\mathrm{Hol}(\mathbb{Z}/N)$ として同定**(week4-E2 の case A 答との接続)、(iv) 205 の推論への**明示反例による訂正**、(v) $Q_2$ 巡回時の「$u=-1$ 層の involution 1 個」判定法(系 STR-1.6)、(vi) 尾部 8 の dl 跳躍 $t=8$ が直積構造の**帰結**として説明できること、および転回案に残る $\varepsilon$ の穴の明示、(vii) (H2) が $N=9$ で破れるという再利用時警告。
- 「初」という語は使わない(工房外の文献は未調査 — §7.3 の【文献要請】参照)。

---

## 12. 出所

- スクリプト: `search/_probe_structthm_h2.g`(第 1 段)・`search/_probe_structthm_witness.g`(第 2 段)・`search/_probe_structthm_counterex.g`(§6 反例)・`search/_probe_structthm_w205.g` + `_w205_a{16,18,20}.g`(205 witness 検査)
- 証明書: `search/certs/.structthm_W-D-A{16,18,20}-{11a,13a,15a}.json`(第 1 段)、`search/certs/.structthm_wit_W-D-A{16,18,20}-*.json`(第 2 段)
- 入力の shadow 集合は既存の `search/certs/.w62_shadows_*.g`(段 A = `search/w62-scan.g` の出力)を再利用 — 走査は再実行していない(規律: 1 窓 1 プロセス・`-o 2g`・走査と群論を同居させない)。
- GAP 4.16.0 + HAP。実行時間: 第 1 段 31.6 / 57.8 / 37.3 秒、第 2 段は各 1 分未満。
