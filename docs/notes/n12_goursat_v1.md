# 定理 MIX-4 / 系 MIX-12 — 混合位数窓 $K^{(4n_0)}$ の $\mathrm{Ih}$ 全射性(E1-GAP-3 の閉鎖)

**状態札: paper-proof candidate / framework-conditional / Sol 未監査**
起草: 数学者(Opus 5)/ 2026-07-31 ・ 委嘱 = 司令塔「E1-GAP-3 = n=12 の Goursat 一段を書く」(E1 正典文書 `E1_gt_odd_dih_canonical_v1.md` §5.6 の上申 → 裁定 257)
記法: 正典 arXiv 2401.06870 / 2405.11725 準拠。定義の工房内正本 `docs/week1-定義ノート.md`。
**封印量・$K^{(5)}$ 非接触**(本稿が $n_0=5$ に触れるのは正典 Thm 4.6 の公開位数 $\lvert\mathrm{GT}(K^{(5)})\rvert=40$ のみ。$K^{(5)}$ の算術的状態については何も仮定も主張もしない)。

---

## 0. 判定(結論を先頭に)

> ### **閉じた。** しかも $n=12$ 単独ではなく $\alpha=2$ 層の**族定理**として閉じた。
> $$\boxed{\ \textbf{定理 MIX-4.}\quad n_0>1\ \text{奇}.\quad \mathrm{Ih}_{K^{(n_0)}}\ \text{全射}\ \Longrightarrow\ \mathrm{Ih}_{K^{(4n_0)}}\ \text{全射}.\ }$$
> $$\boxed{\ \textbf{系 MIX-12.}\quad \mathrm{Ih}_{K^{(12)}}:G_{\mathbb Q}\twoheadrightarrow\mathrm{GT}(K^{(12)})=\mathrm{GTSh}(K^{(12)},K^{(12)})\ \ (\text{位数 }24).\ }$$
> すなわち **Conjecture 5.1 は $n=12$(混合位数の最小 open 対象)で成立する**。

**委嘱が想定した形との差 3 点**(いずれも上方修正だが、格は下がっていないことを §9 で確認する):

1. **Goursat は要るが、その Galois 版(合成体の次数公式)で足りる** — 抽象群の Goursat を持ち出す必要はない(§5.1)。
2. **$\mathcal E_{12}=1$(便 75 F6.3(c))は入力として要らない** — 本稿の補題 AB + 補題 SQ2 が**全奇数 $n_0$ で**再導出する(§3.2)。便 75 の結果は $n_0=3$ での**独立確認**として使う(二経路一致・§6.3)。
3. ゆえに結論は $n=12$ に閉じず、$\alpha=2$ 層 $\{4n_0\}$ の**条件付き族定理**になる。

**閉じなかった部分**: $\alpha\ge3$(= $n=24,40,56,\dots$)。理由と、それを閉じる**単一の**十分条件を §7 に、【n12-GAP-1〜3】を §8 に置く。**埋めていない。**

---

## 1. 前件の棚卸し(全 statement に出典)

| # | 前件 | 内容 | 格 | 出典 |
|---|---|---|---|---|
| **P-a** | isolated | $\forall n\ge3$ で $K^{(n)}$ は isolated ⟹ $\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})$ は有限群、$\mathrm{Ih}_{K^{(n)}}$ は連続群準同型 | **正典の定理** | 2405 Lemma 4.2 / Thm 4.3;Remark 1.4(isolated でなければ準同型ですらない) |
| **P-b** | 2 冪側 | $\mathrm{Ih}_{K^{(2^\alpha)}}$ は全射($\alpha\ge2$) | **正典の定理**(無条件) | 2405 **Thm 5.3** |
| **P-c** | $L_4$ の明示 | $\widetilde\chi:\mathrm{GT}(K^{(4)})\xrightarrow{\sim}(\mathbb Z/8)^\times$(位数 4 同士)かつ $\widetilde\chi\circ\mathrm{Ih}=\chi_8$ ⟹ $L_4=\mathbb Q(\zeta_8)=\mathbb Q(i,\sqrt2)$ | **紙上相互監査 PASS** | **便 75 §F6.3(b)**・裁定 111 |
| **P-d** | 群論側 fiber 積 | $n=2^\alpha n_0$($\alpha\ge2$、$n_0>1$ 奇)で $R_{n,2^\alpha}\times R_{n,n_0}$ は**単射**、像は $\chi_4$-fiber 積: $\mathrm{GT}(K^{(n)})\cong\mathrm{GT}(K^{(2^\alpha)})\times_{(\mathbb Z/4)^\times}\mathrm{GT}(K^{(n_0)})$ | **紙上 PASS**(便 73 (2.7)(2.8)(2.10))。$n=12$ の等号 $K^{(12)}=K^{(4)}\cap K^{(3)}$ は **cross-checked**(W3-23) | **裁定 101 ③④**・裁定 102 |
| **P-e** | 奇側完全列 | $n$ 奇で $1\to\mathfrak F_0(\cong C_n)\to\mathrm{GT}(K^{(n)})\xrightarrow{\widetilde\chi_{2M}}(\mathbb Z/4n)^\times\to1$、**かつ $\widetilde\chi_{2M}$ はアーベル化そのもの**($\ker=[\mathrm{GT},\mathrm{GT}]$) | **candidate**(紙上+$n\le27$ 機械検算) | `w2fam_v1.md` §3.4 別証・**裁定 120** |
| **P-f** | 奇側算術 | $\widetilde\chi_{2M}\circ\mathrm{Ih}_{K^{(n)}}=\chi_{4n}$(全奇数 $n\ge3$・二経路) | **paper-proof / framework-conditional**(Route B は (CAL)+(TB4$^{\rm u}$)) | `w2arith_v1.md` 命題 W2A/W2B″・**裁定 122** |
| **P-g** | reduction 整合 | 奇 $d\mid n$ 等で $R_{n,d}\circ\mathrm{Ih}_{K^{(n)}}=\mathrm{Ih}_{K^{(d)}}$ | **paper-proof candidate**(初等) | `E1_gt_odd_dih_canonical_v1.md` 補題 E1-3b;(1.11)(3.60) |
| **P-h** | $n_0=3$ の入力 | $\mathrm{Ih}_{K^{(3)}}$ 全射・$\mathrm{Gal}(L_3/\mathbb Q)\cong S_3\times C_2$・$L_3=\mathbb Q(\zeta_{12},\sqrt[3]2)$ | **paper-proof / two-mathematician audit PASS / framework-conditional**((K1)–(K4)+(TB1)(TB2)(TB3)(TB4$^{\rm u}$)+(CAL))。**(K4) は Lean 済**(`lean/K3/Shadows.lean` `F19_injective`) | **定理 K3**(`week4-K3飽和_opus_v3.md`)・便 27/28/29・CLAIMS W3-11 |
| **P-i** | (参考) $\mathcal E_{12}=1$ | $L_3\cap L_4=\mathbb Q(i)$ | **紙上相互監査 PASS** | 便 75 §F6.3(c)・裁定 111。**本稿の証明では入力に使わない**(§3.2 で再導出・§6.3 で照合) |

> **⚠ 委嘱の「4 部品」との対応**: 定理 K3 $=$ P-h、正典 Thm 5.3 $=$ P-b、fiber 積 $=$ P-d、$\mathcal E_{12}=1$ $=$ P-i。**このうち P-i だけは不要になった**(P-e+P-f から出る)。代わりに P-e/P-f が新たに load-bearing になっており、**格の総和は下がっていない**(§9)。

---

## 2. 補題群

記号: $\mathrm{Ih}_{K^{(n)}}$ が全射のとき、$L_n:=$ ($\ker\mathrm{Ih}_{K^{(n)}}$ の固定体)。$L_n/\mathbb Q$ は Galois で $\mathrm{Gal}(L_n/\mathbb Q)\cong\mathrm{GT}(K^{(n)})$。

> ### 補題 AB(奇窓の最大アーベル部分拡大 — **本稿で明示化**)
> $n\ge3$ 奇。$\mathrm{Ih}_{K^{(n)}}$ が全射ならば
> $$\boxed{\ L_n^{\rm ab}\ :=\ \bigl(L_n\text{ の }\mathbb Q\text{ 上最大アーベル部分拡大}\bigr)\ =\ \mathbb Q(\zeta_{4n}).\ }$$

**証明.** $G:=\mathrm{Gal}(L_n/\mathbb Q)\cong\mathrm{GT}(K^{(n)})$。$L_n^{\rm ab}$ は $[G,G]$ の固定体である。**P-e** より $[G,G]=\ker\widetilde\chi_{2M}$ かつ $G^{\rm ab}\cong(\mathbb Z/4n)^\times$。したがって $L_n^{\rm ab}$ は準同型
$$G_{\mathbb Q}\xrightarrow{\ \mathrm{Ih}_{K^{(n)}}\ }\mathrm{GT}(K^{(n)})\xrightarrow{\ \widetilde\chi_{2M}\ }(\mathbb Z/4n)^\times$$
の核の固定体。**P-f** よりこの合成は $\chi_{4n}$(円分指標の $\bmod\ 4n$ 還元)であり、その核の固定体は $\mathbb Q(\zeta_{4n})$。∎

> ### 補題 SQ2($\sqrt2$ の排除 — **本稿で明示化**)
> $n\ge3$ 奇。$\mathrm{Ih}_{K^{(n)}}$ が全射ならば $\sqrt2\notin L_n$、したがって
> $$\boxed{\ L_4\cap L_n=\mathbb Q(i)\ }\qquad(\text{すなわち }\mathcal E_{4n}=1).$$

**証明.** $\mathbb Q(\sqrt2)/\mathbb Q$ はアーベルだから、$\sqrt2\in L_n$ なら $\mathbb Q(\sqrt2)\subseteq L_n^{\rm ab}=\mathbb Q(\zeta_{4n})$(補題 AB)。$\mathbb Q(\sqrt2)$ の導手は $8$ であり、Kronecker–Weber と導手–判別式定理より $\mathbb Q(\sqrt2)\subseteq\mathbb Q(\zeta_m)\iff 8\mid m$。$n$ 奇ゆえ $8\nmid4n$。矛盾。よって $\sqrt2\notin L_n$。

次に $\mathbb Q(i)=\mathbb Q(\zeta_4)\subseteq\mathbb Q(\zeta_{4n})\subseteq L_n$ かつ **P-c** より $\mathbb Q(i)\subseteq L_4=\mathbb Q(i,\sqrt2)$。ゆえに $\mathbb Q(i)\subseteq L_4\cap L_n\subseteq L_4$ で、$[L_4:\mathbb Q(i)]=2$ だから $L_4\cap L_n$ は $\mathbb Q(i)$ か $L_4$。後者なら $\sqrt2\in L_n$ となり上に矛盾。ゆえに $L_4\cap L_n=\mathbb Q(i)$。∎

> ### 補題 KER(核の交わり)
> $n=2^\alpha n_0$($\alpha\ge2$、$n_0>1$ 奇)とすると
> $$\ker\mathrm{Ih}_{K^{(n)}}=\ker\mathrm{Ih}_{K^{(2^\alpha)}}\cap\ker\mathrm{Ih}_{K^{(n_0)}} .$$

**証明.** ($\subseteq$) **P-g** より $R_{n,2^\alpha}\circ\mathrm{Ih}_{K^{(n)}}=\mathrm{Ih}_{K^{(2^\alpha)}}$、同様に $n_0$ 側。よって $\mathrm{Ih}_{K^{(n)}}(\gamma)=1$ なら両成分も $1$。
($\supseteq$) 両成分が $1$ なら $(R\times R)(\mathrm{Ih}_{K^{(n)}}(\gamma))=1$。**P-d** の**単射性**より $\mathrm{Ih}_{K^{(n)}}(\gamma)=1$。∎

> **★ ここが「$R\times R$ 単射」(便 73 (2.7))の効き所**: 単射性がないと ($\supseteq$) が言えず、$\mathrm{Im}\,\mathrm{Ih}_{K^{(n)}}$ を合成体の Galois 群と同一視できない。

---

## 3. 定理 MIX(一般形)と定理 MIX-4

> ### 定理 MIX(一般 $\alpha$・条件付き)
> $n=2^\alpha n_0$、$\alpha\ge2$、$n_0>1$ 奇とする。
> **(a)** $\mathrm{Ih}_{K^{(2^\alpha)}}$ 全射(**P-b** より無条件に成立)、
> **(b)** $\mathrm{Ih}_{K^{(n_0)}}$ 全射、
> **(c)** $L_{2^\alpha}\cap L_{n_0}=\mathbb Q(i)$
> が成り立つならば $\mathrm{Ih}_{K^{(n)}}$ は全射である。

**証明.** $A:=\mathrm{Im}\,\mathrm{Ih}_{K^{(n)}}\le\mathrm{GT}(K^{(n)})$ と置く。補題 KER より
$$A\ \cong\ G_{\mathbb Q}\big/\bigl(\ker\mathrm{Ih}_{K^{(2^\alpha)}}\cap\ker\mathrm{Ih}_{K^{(n_0)}}\bigr)\ =\ \mathrm{Gal}\bigl(L_{2^\alpha}L_{n_0}/\mathbb Q\bigr).$$
$L_{2^\alpha},L_{n_0}$ はともに $\mathbb Q$ 上 Galois だから、**合成体の次数公式**(= Galois 群に対する Goursat・§5.1)より
$$\bigl[L_{2^\alpha}L_{n_0}:\mathbb Q\bigr]=\frac{[L_{2^\alpha}:\mathbb Q]\cdot[L_{n_0}:\mathbb Q]}{[L_{2^\alpha}\cap L_{n_0}:\mathbb Q]}
\overset{\text{(a)(b)(c)}}{=}\frac{\lvert\mathrm{GT}(K^{(2^\alpha)})\rvert\cdot\lvert\mathrm{GT}(K^{(n_0)})\rvert}{2}
=\frac{2^{2\alpha-2}\cdot2n_0\varphi(n_0)}{2}=n_0\varphi(n_0)2^{2\alpha-2}.$$
一方 正典 Thm 4.6($\alpha\ge2$)より $\lvert\mathrm{GT}(K^{(n)})\rvert=n_0\varphi(n_0)2^{2\alpha-2}$。ゆえに $\lvert A\rvert=\lvert\mathrm{GT}(K^{(n)})\rvert$ であり、$A\le\mathrm{GT}(K^{(n)})$ だから $A=\mathrm{GT}(K^{(n)})$。∎

> ### 定理 MIX-4($\alpha=2$ — **(c) が自動的に成立する**)
> $n_0>1$ 奇。$\mathrm{Ih}_{K^{(n_0)}}$ が全射ならば $\mathrm{Ih}_{K^{(4n_0)}}$ は全射。

**証明.** 定理 MIX の $\alpha=2$ の場合。(a) は **P-b**。(b) は仮定。**(c) は補題 SQ2 が与える**($L_4=\mathbb Q(i,\sqrt2)$ と $\sqrt2\notin L_{n_0}$)。∎

### 3.2 $\mathcal E$ の消滅が「自動」になった理由(**委嘱の想定との差の核心**)

委嘱は $\mathcal E_{12}=1$(便 75 F6.3(c))を**入力**として挙げた。しかし補題 AB は
$$L_{n_0}^{\rm ab}=\mathbb Q(\zeta_{4n_0}),\qquad 4n_0\ \text{の }2\text{-部分}=4$$
を与え、$L_{n_0}$ の**二次部分体はすべて $\mathbb Q(\zeta_{4n_0})$ の中にある**。$L_4=\mathbb Q(\zeta_8)$ の $\mathbb Q(i)$ を越える部分は $\sqrt2$ すなわち導手 $8$ の成分だから、**$4n_0$ の 2-部分が $4$ で止まっている限り構造的に届かない**。

$$\boxed{\ \mathcal E_{4n_0}=1\ \text{は「奇窓の}\ \widetilde\chi\ \text{がアーベル化そのもの」(P-e) の帰結であり、窓ごとの偶然ではない。}\ }$$

これが $\alpha=2$ でのみ働く理由も同時に見える: $L_{2^\alpha}$ の $\mathbb Q(i)$ を越える部分の導手が $2^{\alpha+1}\ge8$ である一方、$L_{n_0}^{\rm ab}=\mathbb Q(\zeta_{4n_0})$ の 2-部分は常に $4$ — **ただしこの比較が使えるのは $L_{2^\alpha}$ がアーベル($=$ 円分)であるとき、すなわち $\alpha=2$ のときだけ**である(§7)。

---

## 4. 系 MIX-12

> ### 系 MIX-12
> $$\mathrm{Ih}_{K^{(12)}}:G_{\mathbb Q}\twoheadrightarrow\mathrm{GT}(K^{(12)})=\mathrm{GTSh}(K^{(12)},K^{(12)})\cong\mathrm{Aff}(\mathbb Z/3)\times\widetilde H_2\ \ (\text{位数 }24),$$
> すなわち **target $K^{(12)}$ の 24 個の GT-shadow はすべて arithmetical、ゆえに genuine**。Conjecture 5.1 は $n=12$ で成立する。

**証明.** 定理 MIX-4 に $n_0=3$ を代入。前件 (b) は **P-h**(定理 K3)。∎

**具体的な体**: $L_{12}=L_4L_3=\mathbb Q(\zeta_8)\cdot\mathbb Q(\zeta_{12},\sqrt[3]2)=\mathbb Q(\zeta_{24},\sqrt[3]2)$、$[L_{12}:\mathbb Q]=24$、$\mathrm{Gal}(L_{12}/\mathbb Q)\cong\mathrm{GT}(K^{(12)})\cong S_3\times C_2\times C_2$。

> **意義**(地図との接続): $n=12$ は **混合位数($\alpha\ge2$ かつ $n_0>1$)の最小 open 対象**であった(定義ノート §3・2405 抽出ノート §5)。地図 P1 行「dihedral 予想(奇数/**混合**側)」の**混合側で最初の窓が落ちた**ことになる。

---

## 5. 「Goursat 一段」の正体と、司令塔が名指しした 2 つの非退化検査

### 5.1 Goursat は要るが、Galois 版で足りる

$L,M$ が $\mathbb Q$ 上 Galois のとき
$$\mathrm{Gal}(LM/\mathbb Q)\ \xrightarrow{\ \sim\ }\ \mathrm{Gal}(L/\mathbb Q)\times_{\mathrm{Gal}(L\cap M/\mathbb Q)}\mathrm{Gal}(M/\mathbb Q)$$
は古典的事実であり、**これは部分直積に対する Goursat の補題を Galois 群に適用したもの**(共通商 $E=\mathrm{Gal}(L\cap M/\mathbb Q)$)。抽象群の Goursat を別途持ち出す必要はなく、§3 の証明では位数を数えるだけで済んだ。

**したがって委嘱の問い「Goursat 一段で結論できるか」への答は YES**(ただし「一段」の中身は合成体の次数公式である)。

### 5.2 検査 ①「fiber 積の像が $\mathrm{GTSh}$ 全体を覆うか」

**覆う。** ただし論理は「像が覆う」を直接示すのではなく、**位数一致 + 部分群**で閉じる:
$$A\le\mathrm{GT}(K^{(n)}),\qquad \lvert A\rvert=[L_{2^\alpha}L_{n_0}:\mathbb Q]=n_0\varphi(n_0)2^{2\alpha-2}=\lvert\mathrm{GT}(K^{(n)})\rvert\ \Longrightarrow\ A=\mathrm{GT}(K^{(n)}).$$
ここで **P-d の単射性が本質**である(補題 KER)。単射性がなければ $A\cong\mathrm{Gal}(L_{2^\alpha}L_{n_0}/\mathbb Q)$ という同一視が壊れ、位数勘定が使えない。

### 5.3 検査 ②「$\mathcal E=1$ が像の非退化を保証するか」

**保証する。ただし「非退化」は二つの $C_2$ の一致として定式化する必要がある。** 検査すべきは:

$$\text{fiber 積 (P-d) の共通商 }(\mathbb Z/4)^\times\ \ \overset{?}{=}\ \ \text{Goursat の共通商 }\mathrm{Gal}(L_{2^\alpha}\cap L_{n_0}/\mathbb Q)=\mathrm{Gal}(\mathbb Q(i)/\mathbb Q).$$

**一致する**: $\mathrm{Ih}(g)=\bigl(\tfrac{\chi(g)-1}{2},f_g\bigr)$ ゆえ $\widehat{\mathbb Z}$ の中で $2\hat m+1=\chi(g)$。$m$ の水準は $K^{(i)}_{\rm ord}$ で、$4\mid 2K^{(i)}_{\rm ord}$ が全ての $i\in\{2^\alpha,n_0,n\}$ で成り立つ($K^{(2^\alpha)}_{\rm ord}=2^\alpha$、$K^{(n_0)}_{\rm ord}=2n_0$、$K^{(n)}_{\rm ord}=n$)から
$$\chi_4\bigl(\mathrm{Ih}_{K^{(i)}}(g)\bigr)=(2m+1)\bmod4=\chi(g)\bmod4,$$
すなわち $\chi_4\circ\mathrm{Ih}_{K^{(i)}}=\chi_4$(円分指標の $\bmod\ 4$ 還元)で、その固定体は $\mathbb Q(i)$。**二つの $C_2$ は同じものである。** ∎

> **⚠ この検査は論理的には不要だが、健全性の確認として必須である**: もし二つの $C_2$ が食い違っていたら、$A$($=\mathbb Q(i)$ 上の fiber 積・位数 24)が $\mathrm{GT}(K^{(12)})$($=\chi_4$-fiber 積・位数 24)に**含まれない**ことになり、$A\le\mathrm{GT}(K^{(12)})$ と矛盾する。§6 の機械検査 (iv) は $\chi_4$ が両側で全射(像 $=\{1,3\}$)であること、すなわち共通商が真に $C_2$ で潰れていないことを実データで確認している。

---

## 6. 整数検算(証明とは独立・機械)

**スクリプト**: `scratchpad/n12_goursat_check.py`(単体 $n=12$)/ `scratchpad/mix4_family_check.py`(族 $n_0=3,5,7,9,11,15$)。整数演算のみ($\gcd$・剰余・置換)。正典 Thm 4.3 (4.12)+(4.9)、合成則 (4.18)。**単系統・スクラッチ**であり、証明はこれに依存しない。

### 6.1 $n=12$ 単体(8 検査すべて PASS)

| # | 検査 | 実測 | 期待 |
|---|---|---|---|
| (i) | (4.12) による全列挙($4\mid n$ の追加条件 $k\equiv\varkappa(m)/2\ (2)$ 込み)・群性(閉性/単位元/逆元) | $\lvert\mathcal X_{12}\rvert=8$、$\lvert\mathrm{GT}(K^{(12)})\rvert=\mathbf{24}$;$\lvert\mathrm{GT}(K^{(4)})\rvert=\mathbf 4$、$\lvert\mathrm{GT}(K^{(3)})\rvert=\mathbf{12}$ | Thm 4.6 ✓ |
| (ii) | $R\times R$ の単射性(便 73 (2.7)) | 像の相異個数 **24/24** | 単射 ✓ |
| (iii) | 像 $=\chi_4$-fiber 積(便 73 (2.8)) | 集合として一致・$\lvert\cdot\rvert=24=4\cdot12/2$ | ✓ |
| (iv) | **$\chi_4$ の非退化**(§5.3) | $\chi_4(T_4)=\chi_4(T_3)=\chi_4(T_{12})=\{1,3\}=(\mathbb Z/4)^\times$ | 共通商は真に $C_2$ ✓ |
| (v) | $\mathrm{Gal}(L_3/\mathbb Q)\cong S_3\times C_2$ の指数 2 部分群 | **3 個** | $L_3$ の二次部分体はちょうど 3 個 ✓(補題 SQ2 の $n_0=3$ 実例) |
| (vi) | 合成体の次数 | $4\cdot12/2=\mathbf{24}=\lvert\mathrm{GT}(K^{(12)})\rvert$ | ✓ |
| (vii) | $\chi_4$ の well-defined 性($m$ の法 $K_{\rm ord}$ から法 4 へ) | $2K_{\rm ord}\in\{24,8,12\}$ すべて $4$ の倍数 | ✓ |
| (viii) | **位数分布による Thm 4.6 の独立確認** | $\mathrm{GT}(K^{(12)})$ の位数分布 $=\{1{:}1,\ 2{:}15,\ 3{:}2,\ 6{:}6\}$ $=$ $S_3\times C_2\times C_2$ のそれ | $\mathrm{Aff}(\mathbb Z/3)\times\widetilde H_2$ ✓ |

### 6.2 族($\alpha=2$ 層・P-d の族的確認)

| $n_0$ | $n=4n_0$ | $\lvert\mathrm{GT}(K^{(n_0)})\rvert$ | $\lvert\mathrm{GT}(K^{(4)})\rvert$ | $\lvert\mathrm{GT}(K^{(n)})\rvert$ | Thm 4.6 $=n_0\varphi(n_0)2^2$ | $R\times R$ 単射 | 像 $=\chi_4$ 積 |
|---|---|---|---|---|---|---|---|
| 3 | 12 | 12 | 4 | **24** | 24 | ✓ | ✓ |
| 5 | 20 | 40 | 4 | **80** | 80 | ✓ | ✓ |
| 7 | 28 | 84 | 4 | **168** | 168 | ✓ | ✓ |
| 9 | 36 | 108 | 4 | **216** | 216 | ✓ | ✓ |
| 11 | 44 | 220 | 4 | **440** | 440 | ✓ | ✓ |
| 15 | 60 | 240 | 4 | **480** | 480 | ✓ | ✓ |

全行で $\lvert\mathrm{GT}(K^{(4)})\rvert\cdot\lvert\mathrm{GT}(K^{(n_0)})\rvert/2=\lvert\mathrm{GT}(K^{(n)})\rvert$。**便 73 (2.10) の群論側が $n_0=3,5,7,9,11,15$ の実データで一致。**

> **⚠ $n_0=5$ 行について**: これは正典 Thm 4.6 の公開位数($\lvert\mathrm{GT}(K^{(5)})\rvert=40$・定義ノート §3 の表)と (4.12) の列挙のみを使う**群論の検算**であり、$K^{(5)}$ の**算術**(blind campaign の対象)には一切触れていない。定理 MIX-4 の $n_0=5$ への適用も「$\mathrm{Ih}_{K^{(5)}}$ が全射ならば」という条件文のままで、前件の真偽は本稿の射程外。

### 6.3 便 75 F6.3(c) との二経路照合

| 経路 | 論法 | 結論 |
|---|---|---|
| **便 75 F6.3(c)**(既存) | $\mathrm{Gal}(L_3/\mathbb Q(i))\cong S_3$ の唯一の二次商 $\to\mathbb Q(i,\sqrt3)$;$L_4=\mathbb Q(i,\sqrt2)$ は $2$ の上のみ分岐・$\mathbb Q(i,\sqrt3)/\mathbb Q(i)$ は $3$ の上で分岐 ⟹ $\sqrt3\notin L_4$ | $\mathcal E_{12}=1$ |
| **本稿 補題 AB+SQ2**(新) | $L_3^{\rm ab}=\mathbb Q(\zeta_{12})$($\widetilde\chi$ がアーベル化・P-e/P-f)⟹ $L_3$ の二次部分体は $\mathbb Q(i),\mathbb Q(\sqrt3),\mathbb Q(\sqrt{-3})$ の 3 個(機械検査 (v) と一致)⟹ $\sqrt2\notin L_3$ | 同上・**かつ全奇数 $n_0$ へ一般化** |

**二経路が独立に一致**($n_0=3$)。便 75 は分岐(ramification)で、本稿はアーベル化(導手)で殺している。

---

## 7. 射程と限界 — なぜ $\alpha\ge3$ が続かないか

$$\lvert\mathrm{GT}(K^{(2^\alpha)})\rvert=2^{2\alpha-2}\qquad\text{vs}\qquad\bigl\lvert(\mathbb Z/2^{\alpha+1})^\times\bigr\rvert=2^{\alpha}$$

| $\alpha$ | $\lvert\mathrm{GT}(K^{(2^\alpha)})\rvert$ | $\varphi(2^{\alpha+1})$ | $\widetilde\chi$ | $L_{2^\alpha}$ |
|---|---|---|---|---|
| **2** | 4 | 4 | **同型** | $=\mathbb Q(\zeta_8)$ — **円分・明示**(P-c) |
| 3 | 16 | 8 | 核の位数 2 | 非可換($\mathrm{GT}(K^{(8)})$ は非可換 — 2405 **Cor 5.4**)・**未記述** |
| 4 | 64 | 16 | 核の位数 4 | 同上・未記述 |

$\alpha\ge3$ では $\mathrm{GT}(K^{(2^\alpha)})$ が非可換ゆえ $L_{2^\alpha}$ は $\mathbb Q$ の非アーベル拡大であり、**工房にも正典にも明示記述がない**。したがって前件 (c) を検証する手段が無い(§8【n12-GAP-1】)。

### 7.1 (c) を全 $\alpha$ で一挙に閉じる**単一の**十分条件

補題 AB を使うと、$\alpha\ge3$ でも次まで言える。$M:=L_{2^\alpha}\cap L_{n_0}$ と置く。$\mathrm{Gal}(M/\mathbb Q)$ は 2-群 $\mathrm{GT}(K^{(2^\alpha)})$ の商だから 2-群。一方それは $\mathrm{GT}(K^{(n_0)})\cong\mathrm{Aff}(\mathbb Z/n_0)\times C_2$ の商でもあり、その導来部分群 $\mathbb Z/n_0$ は**奇数位数**ゆえ 2-群の中では自明に落ちる。よって $\mathrm{Gal}(M/\mathbb Q)$ はアーベル、すなわち
$$M\subseteq L_{n_0}^{\rm ab}=\mathbb Q(\zeta_{4n_0})\qquad(\text{補題 AB}).$$
$\mathbb Q(\zeta_{4n_0})$ の**2-部分の導手は 4**。したがって:

> $$\boxed{\ \textbf{十分条件 (U2)}:\ L_{2^\alpha}/\mathbb Q\ \text{が }2\text{ の外不分岐}\ \Longrightarrow\ (c)\ \text{が全 }\alpha\ge2,\ \text{全奇 }n_0>1\ \text{で成立}.\ }$$

**証明.** (U2) の下で $M=L_{2^\alpha}\cap L_{n_0}$ は $2$ の外不分岐かつ $\subseteq\mathbb Q(\zeta_{4n_0})$。$\mathbb Q(\zeta_{4n_0})$ の $2$ の外不分岐な部分体は $\mathbb Q(\zeta_4)=\mathbb Q(i)$ に含まれる($4n_0$ の $2$-部分が $4$)。$\mathbb Q(i)\subseteq M$ は既出。ゆえに $M=\mathbb Q(i)$。∎

$\alpha=2$ では (U2) は $L_4=\mathbb Q(\zeta_8)$ から**自明に成立**(定理 MIX-4 の別証にもなる)。

> ### 【文献要請】$L_{2^\alpha}$ の分岐
> **困難**: $\alpha\ge3$ で $\mathrm{GT}(K^{(2^\alpha)})$ が非可換になり、$\mathrm{Ih}_{K^{(2^\alpha)}}$ の切り出す体 $L_{2^\alpha}$ が正典・工房のどちらにも記述されていない。そのため定理 MIX の前件 (c) が検証できず、混合側は $\alpha=2$ 層で止まる。
> **欲しい結果の型**: 「$K^{(2^\alpha)}$ が切り出す体 $L_{2^\alpha}$ は $2$ の外で不分岐」— あるいはより一般に「$\widehat F_2$ の**特性的な 2-群商**への $G_{\mathbb Q}$ 作用が定める体は $2$ の外不分岐」。$G_{2^\alpha}=F_2/K^{(2^\alpha)}_{F_2}$ は位数 $2^{3\alpha-1}$ の 2-群である(正典 §3 の位数式)から、pro-$\ell$ 商($\ell=2$)の不分岐性に関する標準理論が使えるはずだが、**その理論は正典 2 論文の射程外**(2405 は「elementary tools のみ・エタール理論不使用」を明言)であり、**工房の文献ゲートを通っていない**。
> **効果**: (U2) が得られれば定理 MIX が**全 $\alpha\ge2$・全奇 $n_0$ で無条件**になり、$$\boxed{\text{混合側 Conj 5.1}\ \Longleftarrow\ \text{奇側 Conj 5.1}}$$ すなわち **dihedral 予想は完全に奇側へ帰着する**(2 冪側は Thm 5.3 で既決)。中間峰 P2 と本峰 P1 の距離が消える。
> **判断は司令塔**(文献ゲート・2026-07-25 研究者裁定)。本稿は探しに行っていない。

---

## 8. 【n12-GAP】(**埋めていない**)

| # | ギャップ | 内容 | 状態 |
|---|---|---|---|
| **n12-GAP-1** | **$\alpha\ge3$ で $L_{2^\alpha}$ が未記述** | $\mathrm{GT}(K^{(2^\alpha)})$ は $\alpha\ge3$ で非可換(2405 Cor 5.4)ゆえ $L_{2^\alpha}$ は非アーベル拡大で、明示記述が正典にも工房にも無い。**帰結: $n=24,40,56,72,\dots$($\alpha\ge3$ の混合窓)には定理 MIX が適用できない。** 単一の十分条件 (U2) に縮約済(§7.1)→【文献要請】 | **UNKNOWN**(縮約済) |
| **n12-GAP-2** | **定理 MIX-4 は条件付き** | 前件 (b)「$\mathrm{Ih}_{K^{(n_0)}}$ 全射」が要る。無条件に供給できている $n_0$ は **$n_0=3$ のみ**(定理 K3)。$n_0=5$ は blind campaign(本稿非接触)、$n_0=7$ は q=7 前線でありかつ下界装置の空白【E1-GAP-6】に阻まれている、$n_0\ge9$ は未着手。**ゆえに現時点で無条件に落ちた混合窓は $n=12$ 一つ** | **設計どおり**(奇側の進捗に従属) |
| **n12-GAP-3** | **格の継承先が P-e/P-f に移った** | $\mathcal E_{12}=1$(紙上相互監査 PASS)を入力から外した代わりに、**(W2)-fam(裁定 120・candidate)と W2-arith(裁定 122・framework-conditional・(CAL)+(TB4$^{\rm u}$) 依存)が新たに load-bearing** になった。$n=12$ 単体だけを主張するなら便 75 F6.3(c) を使う経路も残る(§6.3 の二経路)ので、**Sol 監査では「どちらの経路を正本にするか」を判定されたい** | **判定待ち**(数学の穴ではなく依存設計の選択) |
| **n12-GAP-4** | **genuine 側は別** | 系 MIX-12 は arithmetical を言う。arithmetical ⟹ genuine は 2405 §1.3.1 から従うので $n=12$ の 24 shadow はすべて genuine でもある。ただし逆向き($\mathcal{PR}_{K^{(12)}}$ の全射性を独立に示すこと)は射程外 | **射程外の明示** |

---

## 9. 格付けと出所

### 9.1 格付け(**「verified」は使わない**)

| statement | 格 | 依存 |
|---|---|---|
| **補題 AB**($L_n^{\rm ab}=\mathbb Q(\zeta_{4n})$) | **paper-proof candidate** | P-e(裁定 120・candidate)+ P-f(裁定 122・framework-conditional) |
| **補題 SQ2**($\sqrt2\notin L_n$・$L_4\cap L_n=\mathbb Q(i)$) | **paper-proof candidate** | 補題 AB + P-c(裁定 111)+ Kronecker–Weber・導手–判別式(古典) |
| **補題 KER** | **paper-proof candidate** | P-d(裁定 101 ③④)+ P-g |
| **定理 MIX**(一般 $\alpha$・条件付き) | **paper-proof candidate** | 補題 KER + 正典 Thm 4.6 + 合成体次数公式(古典) |
| **定理 MIX-4**($\alpha=2$) | **paper-proof candidate / framework-conditional** | 定理 MIX + 補題 SQ2 + P-b(正典・無条件) |
| **系 MIX-12** | **paper-proof candidate / framework-conditional** | 定理 MIX-4 + **P-h $=$ 定理 K3**((K1)–(K4)+(TB1)(TB2)(TB3)(TB4$^{\rm u}$)+(CAL);(K4) は Lean 済) |
| **(U2) ⟹ (c) 全 $\alpha$** | **paper-proof candidate**(条件文として) | 補題 AB + 導手計算 |
| 機械検算(§6) | **単系統・スクラッチ**(証明の cross-check であって証明ではない) | `scratchpad/n12_goursat_check.py`・`scratchpad/mix4_family_check.py` |

> **⚠ 「初」の語は使わない**(工房外の文献での既知性は未調査)。工房内については grep 済 — `Ih_{K^{(12)}}` の全射性・`定理 MIX`・`補題 AB`・`L_n^{ab}` に該当する既出記述は `docs/`・`sol/`・`provenance/`・`ideas/` に**発見できなかった**(裁定 257 が「Goursat 一段が未記述」と認定した状態と整合)。
> **Sol 未監査**。中間峰・本峰にまたがる主張なので Sol ゲート対象と考える。

### 9.2 出所

- **正典**: 2405.11725 Lemma 4.2 / Thm 4.3(isolated・(4.12)(4.9))・**Thm 4.4**・**Thm 4.6** (4.23)・**Thm 5.3**・**Cor 5.4**・Remark 1.4・Remark 1.5 (1.14)・§3 位数式;2401.06870 §3(合成 (3.53)・(3.49))・§5 Thm 5.2。
- **工房(便)**: **便 73 §Q2.3–Q2.5**((2.6)(2.7)(2.8)(2.10)(2.11)・★教材 73-3)/ **便 75 §F6.3(b)(c)**($L_4$・$\mathcal E_{12}=1$)/ 便 27・28・29(定理 K3 の監査)。
- **工房(裁定)**: **101**(③④⑤)・**102**(W3-23 cross-checked)・**107**・**111**・**120**・**122**・**174**・**214**・**257**(本委嘱)。
- **工房(文書)**: `docs/notes/E1_gt_odd_dih_canonical_v1.md`(E1 正典文書・本稿の親)/ `docs/week4-K3飽和_opus_v3.md`(定理 K3)/ `docs/notes/w2fam_v1.md`・`docs/notes/w2arith_v1.md` / `docs/week1-定義ノート.md` §2–§3 / `lean/K3/Shadows.lean`(F19 = (K4))。

### 9.3 申し送り(司令塔へ)

1. **地図の更新候補**: P1 行「dihedral 予想(奇数/**混合**側)」— **混合側の最小 open 窓 $n=12$ が落ちた**(candidate)。帯 0 領有の「K⁽¹²⁾ 交叉」は**「K⁽¹²⁾ 全射(条件付き族定理 MIX-4 の系)」へ格上げ可能**。ただし Sol 監査前。
2. **【文献要請】(U2) = $L_{2^\alpha}$ の 2 の外不分岐性**(§7.1)は、**通れば混合側が丸ごと奇側へ帰着する**(dihedral 予想が「奇側のみ」に縮む)。文献ゲートの費用対効果としては極めて高いと判断するが、**発注判断は司令塔の専権**。
3. **n12-GAP-3 の判定依頼**: $n=12$ 単体の正本を「補題 AB 経路(族へ伸びるが P-e/P-f に依存)」と「便 75 F6.3(c) 経路(n=12 限定だが紙上相互監査 PASS)」のどちらに置くか。**両方併記が安全**と考える(§6.3 の二経路照合は cross-check として機能している)。
4. **CLAIMS 登録**: 定理 MIX-4 / 系 MIX-12 は台帳未登録。E1 の 4 点セットが遡及登録された(裁定 226)ことに倣い、Sol 監査後の登録を検討されたい。

---

## 10. 追補ポインタ(2026-07-31・追記のみ・本文は不変)

- **便 91 F91-4.2 の裁定**: 系 MIX-12 の**正典経路は直接経路**($L_3\cap L_4=\mathbb Q(i)$ + 定理 K3 + 正典 Thm 5.3 + fibre 積単射)。**本体 §3–§4 の MIX-4 経由は副経路へ降格**(族へ伸ばすときのみ必要)。上の §9.3-3(n12-GAP-3)は**これで解決**。
  → 書き下ろし: `docs/notes/n12_goursat_v1_addendum_mix12.md` §2。**P-e/P-f を依存から落とした。**
- **便 91 F91-4.3**: **(U2) は正典 Thm 5.3 の 2-group 性からは出ない**(反例 $\mathbb Q(\sqrt3)$: 2-群だが 3 で分岐)。§7.1 の 2-群論法は (U2) の代用にならない。文献候補は**司令塔の文献ゲート経由**でのみ採択可(題名採択の禁止)。要件票 (R1)(R2)(R3) は追補 §4.1。
