# 追補 — 系 MIX-12 の**直接経路を正典化**(F91-4.2)/ (U2) の格の訂正(F91-4.3)

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 位置づけ: **`docs/notes/n12_goursat_v1.md` への追補**(**erratum 方式・本体は書き換えない**)。本体 §3–§4 の MIX-4 経由の導出は**副経路として有効なまま**残す。
- 入力: `sol/sol_reply_91_math18.md` **F91-4.1 / F91-4.2 / F91-4.3**、`sol/裁定_266_便91検収.md` 項目 4・5。
- 監査状態: 定理 MIX-4 = **条件付き PASS**(P-e/P-f + 枠組前件の継承を明示する条件)。系 MIX-12 = **条件付き PASS**、ただし **直接経路を正典にせよ**(F91-4.2)。

---

## 0. 経路の入れ替え(結論を先頭に)

| 経路 | 内容 | **本追補以後の位置** |
|---|---|---|
| **直接経路**(本追補 §2) | $L_3\cap L_4=\mathbb Q(i)$(既監査)+ 定理 K3 + 正典 Thm 5.3 + fibre 積の単射性 | **正典**(canonical) |
| MIX-4 経由(本体 §3) | 補題 AB(P-e/P-f)→ 補題 SQ2 → 定理 MIX-4 → $n_0=3$ を代入 | **副経路**(族へ伸びる利点は残るが、$n=12$ 単体の格を決めない) |

**理由**(F91-4.2): 直接経路は **candidate な P-e**(裁定 120)と **framework-conditional な P-f**(裁定 122)を**背負わない**。$n=12$ 単体の主張の格を、より強い依存だけで支えられる。

---

## 1. 直接経路の前件(これだけ)

| # | 前件 | 内容 | 格 | 出典 |
|---|---|---|---|---|
| **D-1** | isolated | $\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})$ は有限群、$\mathrm{Ih}_{K^{(n)}}$ は連続準同型($n=3,4,12$) | **正典の定理** | 2405 Lemma 4.2 / Thm 4.3 / Remark 1.4 |
| **D-2** | 2 冪側 | $\mathrm{Ih}_{K^{(4)}}$ 全射、$\lvert\mathrm{GT}(K^{(4)})\rvert=4$ | **正典の定理**(無条件) | 2405 **Thm 5.3** + Thm 4.6 |
| **D-3** | $L_4$ の明示 | $L_4=\mathbb Q(\zeta_8)$、$[L_4:\mathbb Q]=4$ | **紙上相互監査 PASS** | 便 75 §F6.3(b)・裁定 111 |
| **D-4** | 奇側の入力 | **定理 K3**: $\mathrm{Ih}_{K^{(3)}}$ 全射、$\mathrm{Gal}(L_3/\mathbb Q)\cong\mathrm{GT}(K^{(3)})\cong S_3\times C_2$(位数 12)、$L_3=\mathbb Q(\zeta_{12},\sqrt[3]2)$ | **paper-proof / two-mathematician audit PASS / framework-conditional** | `week4-K3飽和_opus_v3.md`・便 27/28/29・W3-11 |
| **D-5** | 交わり | $L_3\cap L_4=\mathbb Q(i)$($=\mathcal E_{12}=1$) | **紙上相互監査 PASS** | 便 75 §F6.3(c)・裁定 111(**§2.3 で第三経路により再導出**) |
| **D-6** | fibre 積の**単射性** | $R_{12,4}\times R_{12,3}:\mathrm{GT}(K^{(12)})\hookrightarrow\mathrm{GT}(K^{(4)})\times\mathrm{GT}(K^{(3)})$ | **紙上 PASS**;$K^{(12)}=K^{(4)}\cap K^{(3)}$ は **cross-checked**(W3-23) | 便 73 (2.7)(2.8)・裁定 101 ③④・102 |
| **D-7** | reduction 整合 | $R_{12,d}\circ\mathrm{Ih}_{K^{(12)}}=\mathrm{Ih}_{K^{(d)}}$($d=3,4$) | **paper-proof candidate**(初等) | `E1_gt_odd_dih_canonical_v1.md` 補題 E1-3b |
| **D-8** | 位数 | $\lvert\mathrm{GT}(K^{(12)})\rvert=24$ | **正典の定理** | 2405 **Thm 4.6** (4.23) |

**使わないもの(副経路との差)**: **P-e**(奇側完全列・$\widetilde\chi_{2M}$ がアーベル化・裁定 120 candidate)、**P-f**(奇側算術・裁定 122 framework-conditional)、補題 AB、補題 SQ2。

---

## 2. 直接証明(書き下ろし)

記号: $\mathrm{Ih}_{K^{(n)}}$ が全射のとき $L_n:=$($\ker\mathrm{Ih}_{K^{(n)}}$ の固定体)。$L_n/\mathbb Q$ は有限 Galois で $\mathrm{Gal}(L_n/\mathbb Q)\cong\mathrm{GT}(K^{(n)})$。

### 2.1 補題 KER-12(核の交わり)

> ### 補題 KER-12
> $$\ker\mathrm{Ih}_{K^{(12)}}=\ker\mathrm{Ih}_{K^{(4)}}\ \cap\ \ker\mathrm{Ih}_{K^{(3)}} .$$
> **証明.** ($\subseteq$) **D-7** より $R_{12,4}\circ\mathrm{Ih}_{K^{(12)}}=\mathrm{Ih}_{K^{(4)}}$、$R_{12,3}\circ\mathrm{Ih}_{K^{(12)}}=\mathrm{Ih}_{K^{(3)}}$。$\mathrm{Ih}_{K^{(12)}}(\gamma)=1$ なら両成分も $1$。
> ($\supseteq$) 両成分が $1$ なら $(R_{12,4}\times R_{12,3})\bigl(\mathrm{Ih}_{K^{(12)}}(\gamma)\bigr)=1$。**D-6 の単射性**より $\mathrm{Ih}_{K^{(12)}}(\gamma)=1$。∎
>
> **★ 単射性の効き所**: これがないと ($\supseteq$) が言えず、$\mathrm{Im}\,\mathrm{Ih}_{K^{(12)}}$ を合成体の Galois 群と同一視できない。

### 2.2 系 MIX-12(直接証明)

> ### 系 MIX-12【正典経路】
> $$\mathrm{Ih}_{K^{(12)}}:G_{\mathbb Q}\ \twoheadrightarrow\ \mathrm{GT}(K^{(12)})=\mathrm{GTSh}(K^{(12)},K^{(12)})\qquad(\text{位数 }24).$$
> すなわち **target $K^{(12)}$ の 24 個の GT-shadow はすべて arithmetical(ゆえに genuine)**。Conjecture 5.1 は $n=12$ で成立する。
>
> **証明.** $A:=\mathrm{Im}\,\mathrm{Ih}_{K^{(12)}}\le\mathrm{GT}(K^{(12)})$(**D-1** により部分群として意味をもつ)とおく。
> **(1)** **D-2**(Thm 5.3)と **D-4**(定理 K3)により $\mathrm{Ih}_{K^{(4)}},\mathrm{Ih}_{K^{(3)}}$ は全射で、$L_4,L_3$ が定義され
> $$[L_4:\mathbb Q]=\lvert\mathrm{GT}(K^{(4)})\rvert=4,\qquad [L_3:\mathbb Q]=\lvert\mathrm{GT}(K^{(3)})\rvert=12 .$$
> **(2)** 補題 KER-12 と Galois 対応(部分群の交わり $\leftrightarrow$ 固定体の合成)より
> $$A\ \cong\ G_{\mathbb Q}\big/\bigl(\ker\mathrm{Ih}_{K^{(4)}}\cap\ker\mathrm{Ih}_{K^{(3)}}\bigr)\ =\ \mathrm{Gal}(L_4L_3/\mathbb Q).$$
> **(3)** $L_4,L_3$ はともに $\mathbb Q$ 上 Galois だから合成体の次数公式が使え、**D-5** により
> $$[L_4L_3:\mathbb Q]=\frac{[L_4:\mathbb Q]\,[L_3:\mathbb Q]}{[L_4\cap L_3:\mathbb Q]}=\frac{4\cdot12}{2}=24 .$$
> **(4)** ゆえに $\lvert A\rvert=24$。**D-8** より $\lvert\mathrm{GT}(K^{(12)})\rvert=24$ で、$A\le\mathrm{GT}(K^{(12)})$ だから $A=\mathrm{GT}(K^{(12)})$。∎

**この証明が使う奇側の入力は D-4(定理 K3)だけである。** 本体 §3 の補題 AB・SQ2(したがって P-e/P-f)は**一度も現れない**。

### 2.3 補強 — $[L_4L_3:\mathbb Q]=24$ の**独立計算**と、$\mathcal E_{12}=1$ の第三経路

**D-5 を入力にしない**別の勘定を置く(証明の (3) の独立照合になる)。$L_3=\mathbb Q(\zeta_{12},\sqrt[3]2)$(D-4)、$L_4=\mathbb Q(\zeta_8)$(D-3)より
$$L_4L_3=\mathbb Q(\zeta_8)\cdot\mathbb Q(\zeta_{12},\sqrt[3]2)=\mathbb Q(\zeta_{24},\sqrt[3]2)\qquad(\mathrm{lcm}(8,12)=24).$$
$[\mathbb Q(\zeta_{24}):\mathbb Q]=\varphi(24)=8$ で、$3\nmid8$ ゆえ $\sqrt[3]2\notin\mathbb Q(\zeta_{24})$、したがって $x^3-2$ は $\mathbb Q(\zeta_{24})$ 上既約(3 次で根をもたない)。よって
$$[L_4L_3:\mathbb Q]=8\cdot3=\mathbf{24}.$$
逆に次数公式を解いて
$$[L_4\cap L_3:\mathbb Q]=\frac{4\cdot12}{24}=2,\qquad \mathbb Q(i)\subseteq L_4\cap L_3\ (\mathbb Q(i)\subset\mathbb Q(\zeta_8),\ \mathbb Q(i)\subset\mathbb Q(\zeta_{12}))$$
から **$L_4\cap L_3=\mathbb Q(i)$**、すなわち $\mathcal E_{12}=1$ が**再導出**される。

> **⟹ $\mathcal E_{12}=1$ には三つの独立経路がある**:
> | 経路 | 論法 | 依存 |
> |---|---|---|
> | 便 75 F6.3(c) | 分岐($\mathbb Q(i,\sqrt3)/\mathbb Q(i)$ は 3 で分岐・$L_4$ は 2 の外不分岐) | 既監査 |
> | 本体 §3.2(補題 AB+SQ2) | 導手($L_{n_0}^{\rm ab}=\mathbb Q(\zeta_{4n_0})$ の 2-部分は 4) | **P-e/P-f** |
> | **本追補 §2.3** | **明示体の次数**($x^3-2$ が $\mathbb Q(\zeta_{24})$ 上既約) | D-3 + D-4 のみ・初等 |
>
> 三経路とも $n=12$ で一致。**正典経路(§2.2)は最初と三番目だけで閉じる。**

---

## 3. 格付けの更新

| statement | 追補前 | **追補後(正典経路)** |
|---|---|---|
| **系 MIX-12** | paper-proof candidate / framework-conditional(**MIX-4 + P-e + P-f + 定理 K3** に依存) | **paper-proof candidate / framework-conditional**(依存は **定理 K3 + 正典 Thm 5.3/4.6 + 便 75(D-3,D-5)+ 便 73 単射性 + D-7** に縮小。**P-e/P-f を落とした**) |
| 定理 MIX-4(族・$\alpha=2$) | 同上 | **不変**(条件付き PASS・P-e/P-f と枠組前件の継承を明示)。**族へ伸ばす主張にはなお必要** |
| 定理 MIX(一般 $\alpha$・条件付き) | 不変 | 不変 |
| **n12-GAP-3**(どちらを正本にするか) | 判定待ち | **解決**: 正典 = 直接経路、副 = MIX-4 経由(F91-4.2) |
| (U2) | 十分条件・未証明 | **未証明のまま。§4 の訂正を pin** |

**Sol の指摘のうち本追補で反映しないもの**: F91-4.1(Goursat 段の条件付き PASS)は本体 §5.1 のままでよい。$\mathbb Q(\sqrt2)$ の導手 8 と $8\nmid4n$ による排除も正しい(F91-4.1)。

---

## 4. (U2) の格 — **2-group 性からは出ない**(F91-4.3 の反映)

本体 §7.1 は
$$\textbf{(U2)}:\ L_{2^\alpha}/\mathbb Q\ \text{が }2\text{ の外不分岐}\ \Longrightarrow\ \text{定理 MIX の前件 (c) が全 }\alpha\ge2,\ \text{全奇 }n_0>1\ \text{で成立}$$
を示した(この含意そのものは正しい)。**しかし (U2) 自身は未証明であり、次を明記する**:

> ### 訂正 U2-a(**2-group ≠ 2 の外不分岐**)
> 正典 Thm 5.3 系統が与えるのは $\mathrm{GT}(K^{(2^\alpha)})$ が 2-群であること(および $\alpha\ge3$ で非可換であること)にすぎない。**「Galois 群が 2-群」は「2 の外不分岐」を意味しない。**
> **反例**: $\mathbb Q(\sqrt3)/\mathbb Q$ は $\mathrm{Gal}\cong C_2$(2-群)だが $3$ で分岐する。
> したがって本体 §7.1 の 2-群論法($\mathrm{Gal}(M/\mathbb Q)$ がアーベル ⟹ $M\subseteq\mathbb Q(\zeta_{4n_0})$)は (U2) の**代用にならない**。**(U2) は依然として外部入力である。**

> ### 訂正 U2-b(**題名採択の禁止**)
> Sol は便 91 で pro-$\ell$ tripod / branched-covering 系の一次資料候補を 2 件挙げた。**私(数学者)は文献を漁らない**(文献ゲート・2026-07-25 研究者裁定)。**候補の検索・読解・機構抽出・降ろす判断はすべて司令塔の専権**であり、**題名や一般的な pro-$\ell$ 不分岐性だけで (U2) を採択してはならない**。

### 4.1 【文献要請】(U2) — **要件票**(私が書けるのは要件だけ)

> **困難**: $\alpha\ge3$ で $\mathrm{GT}(K^{(2^\alpha)})$ が非可換になり、$\mathrm{Ih}_{K^{(2^\alpha)}}$ の切り出す有限 Galois 拡大 $L_{2^\alpha}/\mathbb Q$ の**分岐**が正典・工房のどちらにも記述されていない。そのため定理 MIX の前件 (c) が検証できず、混合側は $\alpha=2$ 層で止まる。
>
> **採択の必要条件(この 3 つを同時に満たす定理でなければ使えない)**
>
> | # | 要件 | なぜ要るか |
> |---|---|---|
> | **(R1) 当該有限 quotient** | 主張の対象が **$K^{(2^\alpha)}=\ker\psi_{2^\alpha}$ に対応する有限商 $G_{2^\alpha}=\hat F_2/K^{(2^\alpha)}_{\hat F_2}$**(位数 $2^{3\alpha-1}$・正典 §3 の位数式)であること。一般の pro-2 完備化や「ある特性的 2-群商」ではなく、**この族**でなければ (c) に接続しない | 分岐は商の取り方に依存する。別の商についての不分岐性は移らない |
> | **(R2) 基点規約の一致** | 採用する基点(通常の有理点/接ベクトル基点)が**工房の設定と同じ**であること。基点が違えば $G_{\mathbb Q}$ 作用の切る体が変わりうる | $L_{2^\alpha}$ は $\mathrm{Ih}$ の核の固定体として定義されており、$\mathrm{Ih}$ は基点規約込みで定まる |
> | **(R3) 実際の有限 Galois 拡大についての主張** | 「外作用 $G_{\mathbb Q}\to\mathrm{Out}$ が…」ではなく、**$L_{2^\alpha}/\mathbb Q$ という具体的な有限 Galois 拡大が $2$ の外で不分岐**であること(または $L_{2^\alpha}\subseteq$ 2 の外不分岐な既知体) | 前件 (c) は体の交わり $L_{2^\alpha}\cap L_{n_0}$ の計算に使う。外作用レベルの主張では交わりが計算できない |
>
> **欲しい結果の型**: 上の (R1)–(R3) を満たす「$L_{2^\alpha}/\mathbb Q$ は $2$ の外不分岐」型の定理、またはその**反例**(どちらも一級)。
> **効果**: (U2) が得られれば定理 MIX が**全 $\alpha\ge2$・全奇 $n_0$ で無条件**になり、$$\text{混合側 Conj 5.1}\ \Longleftarrow\ \text{奇側 Conj 5.1}$$ すなわち **dihedral 予想が丸ごと奇側へ帰着**する(2 冪側は Thm 5.3 で既決)。
> **判断は司令塔**。本追補は探索していない。

---

## 5. 申し送り

1. **台帳・地図**: 系 MIX-12 の依存を「**定理 K3 + 正典 Thm 5.3/4.6 + 便 75(F6.3(b)(c))+ 便 73 単射性**」に書き換え(P-e/P-f は副経路側へ)。本体 §9.3 の申し送り 3(n12-GAP-3 の判定依頼)は **F91-4.2 で解決済**。
2. **$\mathcal E_{12}=1$ は三経路一致**(§2.3)。$n=12$ 単体についてはこの点が最も強い。族($\alpha=2$ 層全体)へ伸ばすときだけ補題 AB/SQ2(P-e/P-f)が要る、という切り分けを台帳に明記されたい。
3. **(U2) の要件票**(§4.1)は司令塔の文献ゲートへ。**私は候補文献を読んでいない**(規律 6)。
4. 本体 §6 の機械検算(8 検査・族 6 行)は**直接経路でもそのまま有効**(位数 24・単射性 24/24・$\chi_4$ 非退化)。証明はこれに依存しない。
