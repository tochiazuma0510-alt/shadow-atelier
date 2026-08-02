# reading ノート: Fresse SURV 217 Part 1 **Theorem 6.2.4** の精読(【GAP-TRUNC-1】閉鎖委嘱)

**位置づけ**: `docs/notes/ihnec_v1_addendum_e_b4.md` §E-A.9(補題 TRUNC$^{B_4}$)+ 追記 F の**依存の底の健全性検査**。**追記型 — 既存ノートの本文は 1 バイトも改変していない**。置換・訂正関係は §10 の表に書く(本ノートが effective source)。
**起草**: 影工房 数学者(Claude / Opus 5)/ 2026-08-02。**委嘱** = 研究者指示(2026-08-02)「文献の確認は工房内で実施」→ 司令塔 GAP-TRUNC-1 閉鎖委嘱。**Sol 未監査。**
**封印遵守**: $K^{(5)}$ 非接触・封印 payload 非接触(本ノートは離散 operad の圏論のみを扱う)。
**規約**: pin は **規約台帳 v1.5 §1.5(CV-10 細則)の様式**に従い、全 pin に `proof_body_status` を付す。

---

## 0 一枚(結論を先に)

| 委嘱の問い | 結果 |
|---|---|
| **① 証明の実体はあるか** | ★ **ある。`proof_body_status = present`**(**pp.214–218**・`Proof.` 環境・**Step 1–4** の 4 段 + 補助 **Lemma 6.2.5**(証明つき))。Part 2 の要約「MacLane coherence の operad 版 + 組紐群の表示」は**本文と逐語で一致**(§4.6) |
| **② 量化の正確な形** | ★ **「$Q$ = **任意の** operad in the category of categories」**(逐語)。**射の存在と一意性**を主張し、まとめ節はさらに**全単射**と述べる。工房の使用($Q=\widehat{\mathrm{PaB}}$)は**この量化に入る**(§5.3 で 4 条件を逐一検査 — 全部通る) |
| ★★ **③ 工房の (UP) との関係** | ★ **6.2.4(b) は工房の (UP) より強い**。工房が仮定した「対象上恒等」は Fresse では**仮定ではなく引数** $m\in\mathrm{Ob}\,Q(2)$ である。⟹ **【GAP-TRUNC-1】(FREE-OP)は閉じる**(自由 operad+合同商の構成は**要らない** — 普遍性が定理として直接与えられる) |
| **④ 完備化との接合** | ★ **6.2.4 は完全に離散。射程外**。Part 1 に profinite operad 完備化の一般論は**無い**(§12 の $\widehat{GT}$ は Drinfeld の $\widehat F(x,y)$ 版のみ)。Part 1 が持つ完備化の普遍性(**Thm 10.1.4 / Prop 10.1.5**)は **Malcev 専用**($k=\mathbb Q$)。Part 2 の profinite 注記は **"obvious" の一語**。⟹ **(TR-4) は工房の自前証明で立つ**(本ノートで再検査 — 健全) |
| ★★ **⑤ unitary 版の差** | ★★ **版ずれを発見**。工房の使用は**非 unitary**($\mathrm{PaB}(0)=\emptyset$・2008 p.12 逐語)。**Part 2 Thm 1.1.5 は unitary 版**($\mathrm{PaB}(0)=\ast$・四つ組 $(m,e,a,c)$・strict unit 必須)。⟹ **追記 F / 台帳 §1.5 の引用先 pin は工房の使用を literally 覆わない**。**正しい引用先 = Part 1 Theorem 6.2.4(b)**(非 unitary 核・unit 条件を一切要求しない) |
| **⑥ 番号の一致(裁定 425 追認)** | ★ **一致**。Part 2 は "*1.1.5 Theorem (see [26, Theorem I.6.2.4])*" と明記し、[26] = Fresse の本書。**ただし頁 pin に誤りが 1 つ**(台帳 §1.5 と追記 F の「pp.9-10」→ **正しくは p.11**・profinite 注記は **p.12**) |
| ★ **副産物** | 規約 **(OBJ)(対象上恒等)は落とせる見込み**。6.2.4(b) が対象写像を $m$ で径数づけるため、6 段は $m:=U_{\rm Ob}(\mu)\in\Omega(2)=\{\mu,t\mu\}$ を代入する形でそのまま走る(§9・**candidate**)⟹ **追記 F.1 項 2 の宿題への回答**  |

> ★ **一行で**: **Thm 6.2.4 は証明本文をもつ本物の定理であり、工房の (TR-3) はその射程内にある。それどころか 6.2.4(b) は工房の (UP) を上回る普遍性を与えるので【GAP-TRUNC-1】は閉じる。残余は「6.2.4 が離散だけを扱う」ことに起因する 3 本で、いずれも工房側で既に埋まっているか、pin の版・頁の訂正で済む。**

---

## 1 対象の同定と頁対応

| 項目 | 値 |
|---|---|
| 現物 | `papers/Fresse_SURV217_Part1.pdf`(刊行版・AMS Mathematical Surveys and Monographs **217**・Part 1) |
| sha256 | `bd286ab54e4d0f04bb66636c79c1045dcadf7d8d755e13784377db150abefb54`(**起草者が独立に再計算し、裁定 425 の記録値と一致を確認**) |
| 総頁 | PDF 581 頁 |
| **頁変換** | **書籍頁 = PDF 頁 − 47**(4 点で検証: PDF 250→203, 259→212, 265→218, 266→219) |
| 抽出法 | `pdftotext -layout`(全文)+ `pdftoppm -png -r 120 -f p -l p`(頁画像照合) |

### 1.1 §6.2 / §6.3 の構造(書籍頁)

| 箇所 | 書籍頁 | PDF 頁 |
|---|---|---|
| §6.1 Magmas and the parenthesized permutation operad | 198–208 | 245–255 |
| **Theorem 6.1.7**(Mac Lane coherence の operad 版)+ Figure 6.1(pentagon) | **203–206** | 250–253 |
| §6.2 The parenthesized braid operad | 208–220 | 255–267 |
| §6.2.3 associativity/braiding の定義・hexagon の組紐図 | 211–212 | 258–259 |
| ★ **Theorem 6.2.4 言明**(a)(b)(c) | **212–214** | **259–261** |
| Figure 6.6(hexagon 2 本) | 213 | 260 |
| Figure 6.7(組紐の分解の例) | 214 | 261 |
| ★ **Theorem 6.2.4 証明本体**(Step 1–4) | **214–218** | **261–265** |
| Figure 6.8(dodecagon) | 217 | 264 |
| **Lemma 6.2.5**(dodecagon)+ 証明 | 218 | 265 |
| "To sum up …"(三つ組との同値のまとめ) | 218–219 | 265–266 |
| **Theorem 6.2.6**(CoB 版) | 219 | 266 |
| §6.2.7 braided monoidal category との対応 / §6.2.8 自由 braided monoidal category | 219–220 | 266–267 |
| §6.3 The parenthesized symmetry operad | 220–224 | 267–271 |
| **Theorem 6.3.2**(PaS 版)/ **Theorem 6.3.3**(CoS 版) | 223 / 223–224 | 270 / 270–271 |

> ⚠ **委嘱の頁見積り「約 pp.215-220」は実際とずれている**(言明は p.212 から始まる)。以後は上表を正とする。

### 1.2 頁画像 pin(CV-10 の `external_reference` 要件)

| 画像 | 書籍頁 | sha256 |
|---|---|---|
| `fp250-250.png` | 203(Fig 6.1 + Thm 6.1.7 言明) | `ec043bf51199bf229c6ed75ecfc6b6f7f36de381330204c17c11793c3a396920` |
| `fp259-259.png` | 212(**Thm 6.2.4 言明 (a)(b)**) | `1691b79baef056bdd9c41d5f0785194385d34d0a9950114a671304cc6febf754` |
| `fp260-260.png` | 213(Fig 6.6 + (b) の結論 + (c) 冒頭) | `40a021bee2ad4bd200de10b1fe862d240b998ede594341d18256bf58f5dff53f` |
| `fp261-261.png` | 214(Fig 6.7 + (c) 結論 + **`Proof.` 開始 + Step 1**) | `badf473f3a4e5895bb0e3747d42551f9709894423bf36a1c10f4f1ef213fa12c` |
| `fp265-265.png` | 218(Step 4 末 + **Lemma 6.2.5** + "To sum up") | `6a858e1e64b2c9805b3b620ba93cd0ad0e793878b15ca050c201600677db0662` |
| `p2p11-11.png`(Part 2) | 11(**Thm 1.1.5**) | `0ad59666df20b5465519f6a04217f498e643ca4cf27eb608f7e367c23f2745de` |

**生成は再現可能**(上記コマンド・`-r 120`)。画像は scratchpad にあり共有ツリーには置いていない — 必要なら同コマンドで再生成できる。

---

## 2 ★ pin 表(台帳 v1.5 §1.5 CV-10 様式)

| 札 | 出所 | 言明の要点 | **`proof_body_status`** | 補足欄 |
|---|---|---|---|---|
| **(F624)** ★★ | **Part 1 Theorem 6.2.4**(pp.212–214) | (a) 生成 / (b) 三つ組 $(m,a,c)$ ⟹ **一意な** operad 射 $\phi:\mathrm{PaB}\to Q$ / (c) unitary 拡張 | ★ **`present`** | 証明 = pp.214–218・`Proof.` 環境・**Step 1–4**。使用する外部定理は **Mac Lane coherence**(Thm 6.1.7 経由)と **$B_r$ の Artin 表示** |
| **(F625)** | **Part 1 Lemma 6.2.5**(p.218) | hexagon 2 本 ⟹ **dodecagon**(Fig 6.8)も可換 | **`present`** | 証明 6 行(左右 hexagon + 中央 square の bifunctor 性)。前置き "*a standard statement of the theory of braided monoidal categories (see [99])*" は**出典注記であって証明の代替ではない** |
| **(F617)** ★ | **Part 1 Theorem 6.1.7**(pp.203–206) | Mac Lane coherence の operad 版:pentagon ⟹ 対 $(m,a)$ から一意な $\phi:\mathrm{PaP}\to Q$ | ★ **`present`**(**環境名は `Proof.` ではなく `Explanations.`**) | ★ **内部に外部委譲が 1 段**: 「グラフの路の間の全関係が pentagon と square の合成に帰着する」を **Mac Lane [130] / Stasheff [167] / [160] / [73,116,125]** へ委ねる。逐語: "*We refer to Mac Lane's monograph [130] for further details on this purely combinatorial approach.*"(p.206)。**`Explanations.` は本書で 27 箇所に使われる著者の常用環境**であり、本定理固有の弱化ではない |
| **(F626)** | **Part 1 Theorem 6.2.6**(p.219) | CoB 版(strict associativity) | **`omitted`** / `omission_kind = reader_exercise` | `source_wording` = "*This result follows from the same argument lines as Theorem 6.2.4. We just forget about the associativity isomorphisms in our verifications.*"(**工房は不使用**) |
| **(F632)** | **Part 1 Theorem 6.3.2**(p.223) | PaS 版(symmetry・involution 付き・**hexagon は「どちらか一方」で足りる**) | **`omitted`** / `omission_kind = reader_exercise` | `source_wording` = "*The proof of this statement follows from the same argument lines as the result of Theorem 6.2.4 and we leave this verification as an exercise.*"(**工房は不使用**) |
| **(F633)** | **Part 1 Theorem 6.3.3**(pp.223–224) | CoS 版 | **`omitted`** / `omission_kind = reader_exercise` | 同上(**工房は不使用**) |
| **(FREE-Ω)** ★★ | **Part 1 p.375**(§10.3・Malcev 版定理の証明中)+ **p.200**(§6.1.4) | "*the magma operad $\Omega$ represents the **free operad generated by** the operation $\mu\in\Omega(2)$*"(p.375)/ "*a connected **free operad**, such as the magma operad $\Omega=\Theta(\mu(x_1,x_2),\mu(x_2,x_1))$*"(p.200) | **`present`**(定義・構成) | ★ **工房 §E-A.9.1 の「自由性の傍証(Catalan 数)」が、正典の逐語で**定理格に上がる**。⟹ 追記 F.1 項 3(証拠力の格)の宿題が解ける |
| **(Ω⁺)** | **Part 1 p.200**(§6.1.4) | $\Omega^+(n)=\ast\ (n=0)$, $\Omega(n)$(otherwise);$\Omega(1)$ は "*reduced to the one-point set formed by the unit element $1\in\Omega(1)$*" | **`present`**(定義) | **非 unitary $\Omega$ には arity 0 が無い**ことの正典側 pin |
| **(P2-115)** | **Part 2 p.11**(★ **台帳 §1.5 の "pp.9-10" は誤り**) | "*1.1.5 Theorem (see [26, Theorem I.6.2.4])*"・四つ組 $(m,e,a,c)$・**strict unit 必須** | **`external_reference`** | 引用先 = **Part 1 Thm 6.2.4**(番号一致 ✔)。版 = SURV 217 Part 1・頁画像 pin = `p2p11-11.png`・取得 digest = 上表。**Part 2 単体では証明本文なし**("*This theorem is established in the cited reference.*") |
| **(P2-PROF)** ★ | **Part 2 p.12** | "*We use a similar construction to define the profinite completion … **(We just need to take care of the continuity constraints in the definition of morphisms in this case.)*** … *because the **profinite analogues of these constructions is obvious**.*" | ★ **`omitted`** / `omission_kind = silent_omission` | ★ **profinite 版は定理として存在しない**。工房の (TR-4) の代替にならない |
| **(F1015)** ★ | **Part 1 Proposition 10.1.5**(p.354・Thm 10.1.4 は p.353) | "*Let $\mathrm B=\mathrm{PaB},\mathrm{CoB}$. **If we take $k=\mathbb Q$** as coefficient ring for our Malcev completion process, then every morphism of operads in groupoids $\psi:\mathrm B\to Q$, where $Q$ is an operad in Malcev complete groupoids, automatically defines a morphism of operads in Malcev complete groupoids*" | **`present`** | ★ **Malcev 専用**(随伴 Thm 10.1.4 に依る)。**profinite 版は Part 1 に無い** |
| **(D2008-NU)** | **arXiv 2008.00066 p.12** | "*Since the groupoid $\mathrm{PaB}(0)$ is **empty**, Theorem A.1 implies that the truncated operad $\mathrm{PaB}^{\le4}$ is generated by …*" | **`present`**(地の文の宣言) | ★ **2008 は非 unitary 規約**。§7 の版ずれ判定の根拠 |

---

## 3 Theorem 6.2.4 の言明(逐語・書籍 pp.212–214)

> **Theorem 6.2.4.**
> **(a)** *The morphisms of the groupoid $\mathsf{PaB}(r)$ can be obtained as (categorical) composites of morphisms which themselves decompose into operadic composition products of identity morphisms, of the associativity isomorphism $\alpha\in\mathrm{Mor}\,\mathsf{PaB}(3)$, and of the braiding isomorphism $\tau\in\mathrm{Mor}\,\mathsf{PaB}(2)$.*
>
> **(b)** *Let $\mathsf Q$ be **any operad in the category of categories**. Let $m=m(x_1,x_2)\in\mathrm{Ob}\,\mathsf Q(2)$ be an object in the component of arity two of this operad.* [記法 $m(x_1,x_2)=x_1\square x_2$] *Let*
> $$a(x_1,x_2,x_3)\in\mathrm{Mor}_{\mathsf Q(3)}\bigl((x_1\square x_2)\square x_3,\ x_1\square(x_2\square x_3)\bigr)$$
> *be an isomorphism which connects the operadic composites $(m\circ_1m)$ and $(m\circ_2m)$ in the category $\mathsf Q(3)$. Let*
> $$c=c(x_1,x_2)\in\mathrm{Mor}_{\mathsf Q(2)}\bigl(x_1\square x_2,\ x_2\square x_1\bigr)$$
> *be an isomorphism which connects the operation $m$ to its transposite $(1\,2)m$ in the category $\mathsf Q(2)$.*
> *If these isomorphisms $a$ and $c$ make the **pentagon** diagram of Figure 6.1 and the **hexagon** diagrams of Figure 6.6 commute, then we have a morphism of operads in groupoids*
> $$\phi:\mathsf{PaB}\longrightarrow\mathsf Q$$
> ***uniquely determined by the assignments*** *$\phi(\mu)=x_1\square x_2$, $\phi(\alpha)=a(x_1,x_2,x_3)$ and $\phi(\tau)=c(x_1,x_2)$ in the operad $\mathsf Q$.*
>
> **(c)** *In the construction of (b), if we moreover assume the existence of an object $e\in\mathrm{Ob}\,\mathsf Q(0)$ which satisfies the relation $e\square x_1=x_1=x_1\square e$ **at the object set level**, together with the identities $a(e,x_1,x_2)=a(x_1,e,x_2)=a(x_1,x_2,e)=\mathrm{id}_{m(x_1,x_2)}$, $c(e,x_1)=c(x_1,e)=\mathrm{id}_{x_1}$ at the morphism set level, then the morphism $\phi$ has a unitary extension $\phi:\mathsf{PaB}_+\to\mathsf Q$ which maps $\ast\in\mathsf{PaB}_+(0)$ to $e$.*

**まとめ節**(p.218–219・逐語):

> "*To sum up, the result of Theorem 6.2.4 gives an **equivalence** between operad morphisms $\phi:\mathsf{PaB}\to\mathsf Q$ and **triples $(m,a,c)$** …*"

**関係式の arity**(工房の切詰め論法に直結):
- **pentagon**(Fig 6.1・p.203)= $\mathrm{Mor}\,\mathsf Q(4)$ の等式。使う挿入は $\circ_1:\mathsf Q(2)\times\mathsf Q(3)\to\mathsf Q(4)$ 等。
- **hexagon 2 本**(Fig 6.6・p.213)= $\mathrm{Mor}\,\mathsf Q(3)$ の等式。使う挿入は $\circ_1:\mathsf Q(2)\times\mathsf Q(2)\to\mathsf Q(3)$ 等。
- ⟹ **生成元は arity 2,3・全関係式は arity 3,4 に住む**。工房 §E-A.9.1 の「切詰めが忘れないもの」の表は**正典側と完全に一致**する(★ 独立確認)。

---

## 4 証明本体の解剖(委嘱の問い ①)

**環境は `Proof.`**(頁画像 `fp261-261.png` で視認確認)。4 段構成。

### 4.1 Step 1(pp.214–215)— **(a) の証明** = $B_r$ の生成元への分解

出発点の逐語: "*We have $\mathrm{Mor}_{\mathsf{PaB}(r)}(p,q)=\mathrm{Mor}_{\mathsf{CoB}(r)}(\omega(p),\omega(q))\subset B_r$ **by definition of the groupoids of parenthesized braids**.*"

⟹ $\beta=\beta_1\cdots\beta_n$、各 $\beta_i$ は括弧を忘れると $B_r$ の生成元 $\tau_k$ 1 個。各 $\beta_i$ を
$$\beta_i=\sigma(\cdots)^{-1}\cdot\pi_i(x_{s(1)},\dots,\tau(x_{s(k)},x_{s(k+1)}),\dots,x_{s(r)})\cdot\rho(\cdots)$$
と書く($\rho,\sigma$ は **PaP** 内の associator の合成 = **Theorem 6.1.7(a)** による)。中央因子は $s\cdot\mathrm{id}_{\pi_i}\circ_k\tau$。

> ★ **arity 帳簿(工房の切詰めに効く・起草者の観察)**: $\rho,\sigma$ は arity $r$ の語に $\alpha$(arity 3)を差し込んだ operadic 合成であり、$\pi_i\circ_k\tau$ も $(r-1)+2-1=r$。⟹ **$r\le4$ のとき全ての中間 arity が $\le4$ に収まる**。すなわち **2008 p.12–13 の 1 行演繹「Theorem A.1 implies that $\mathrm{PaB}^{\le4}$ is generated by $\alpha,\beta$」の生成半は、6.2.4(a) の証明の帳簿から読み取れる**(§8.2)。

### 4.2 Step 2(pp.215–217)— **$\phi$ の構成と choice 非依存性**(本体)

- $\mathsf{PaP}$ 側の射は **Theorem 6.1.7(b)** で既に決まっている(対象写像 $\phi:\Omega(r)\to\mathsf Q(r)$ を含む)。Step 2 は**射集合**への延長。
- $\phi(\beta)$ は Step 1 の分解と $\alpha\mapsto a$, $\tau\mapsto c$ から**一意に強制される**(operad 射は全構造演算と可換だから)。p.215 に arity 4 の具体例あり。
- **独立性の検査 3 種**:
  1. **PaP 内の分解の取り方** ⟹ 逐語 "*The **Mac Lane Coherence Theorem** implies that $\phi(\beta)$ does not depend on the choice of the decomposition of the isomorphisms of the parenthesized permutation operad …*"
  2. **括弧づけ $\pi\in\Omega(r-1)$ の取り方** ⟹ 中央の可換方形は「$\circ_k$ が**双関手**であること」から、外側の三角は Mac Lane coherence から。
  3. ★ **$B_r$ の関係式** ⟹ 逐語 "*We are left to check that the application of the **generating relations of braids** does not change the result of our construction.*"
     - **交換関係** $\tau_k\tau_l=\tau_l\tau_k$ ⟹ **operad 合成の結合律**に帰着。
     - **組紐関係** $\tau_k\tau_{k+1}\tau_k=\tau_{k+1}\tau_k\tau_{k+1}$ ⟹ 逐語 "*reduces in that case to the commutation of the **dodecagon** diagram of Figure 6.8, which we establish next (in **Lemma 6.2.5**).*"

### 4.3 Step 3(pp.217–218)— **operad 構造の保存**

同変性・operad 単位の保存は即座。対象の合成は 6.1.7 からの延長。射の $\circ_k$ 保存は Step 1 の分解で生成的な場合に還元し、最後に残る非自明な場合が
> "*the decomposition of the morphism $\tau(x_l,x_{l+1})\circ_k\mathrm{id}_\mu$ … is **equivalent to the application of the hexagon relations of Figure 6.6** …*"

すなわち **hexagon は「関係式」としてだけでなく「$\circ_k$ 保存の証明の中」でも使われている**。⟹ (b) 完了。

### 4.4 Step 4(p.218)— **(c) unitary 拡張**

$m\circ_1e=m\circ_2e=1$, $a\circ_k\mathrm{id}_e=\mathrm{id}_m$, $c\circ_k\mathrm{id}_e=\mathrm{id}_1$ から $\phi:\ast\mapsto e$ が制限作用素 $\partial_k=-\circ_k\ast$ と両立することを見る。**工房は使わない段**(§7)。

### 4.5 Lemma 6.2.5(p.218)— 証明つき

左右の hexagon は Fig 6.6 の 2 本($a^{\pm1}$ の向きを反転したもの)と同一視。中央の square は
$$c\circ_2(tm)\cdot m\circ_2c=c\circ_2c=(tm)\circ_2c\cdot c\circ_2m$$
すなわち **$\circ_2:\mathsf Q(2)\times\mathsf Q(2)\to\mathsf Q(3)$ の関手性**(interchange)。$\square$

### 4.6 ★ Part 2 の要約との照合(委嘱の問い ①の後半)

Part 2 p.11 逐語: "*The proof of this result follows from a combination of **an operadic interpretation of the MacLane coherence theorem** and of the **classical presentation of the braid group by generators and relations**.*"

| Part 2 の要約 | Part 1 本文の対応 | 一致 |
|---|---|---|
| operadic interpretation of Mac Lane coherence | **Theorem 6.1.7**(表題そのものが "Operadic interpretation of the Mac Lane Coherence Theorem")を Step 2 で引用 | ✔ |
| classical presentation of the braid group by generators and relations | Step 1(生成元 $\tau_k$ への分解・$\mathrm{Mor}\subset B_r$)+ Step 2 の Artin 関係式 2 本の検査 | ✔ |

$$\boxed{\ \textbf{Part 2 の要約は本文と逐語で一致する。裁定 425 の司令塔照合を数学者として追認する。}\ }$$

---

## 5 量化の正確な形(委嘱の問い ②)

### 5.1 何に対する量化か

**逐語**: "*Let $\mathsf Q$ be **any operad in the category of categories**.*"

- **圏**: $\mathsf Q$ は **Cat 内の operad**(groupoid でなくてよい)。$a,c$ が**同型であること**は仮定に明記されているので、groupoid 性は不要。
- **対称性**: 対称 operad($\Sigma_n$ 作用つき)。hexagon の書式が $(1\,2)m$ を使う。
- **arity 0**: **(b) は $\mathsf Q(0)$ に一切言及しない**。arity 0 が要るのは **(c) だけ**。
- **厳密さ**: $\phi$ は operad の**厳密な射**(構造演算と on the nose で可換)。lax/pseudo ではない。
- **unit の厳密さ**: **(b) には unit 条件が無い**。(c) の $e\square x_1=x_1=x_1\square e$ は**対象集合水準の等式 = strict unit**。

### 5.2 存在か一意性か

- **(b) 本文**: "*we have a morphism … **uniquely determined by** the assignments*" ⟹ **存在 + 一意性**。
- **まとめ節**: "*gives an **equivalence** between operad morphisms $\phi:\mathsf{PaB}\to\mathsf Q$ and **triples $(m,a,c)$***" ⟹ **全単射**
  $$\mathrm{Hom}_{\mathrm{Op}(\mathbf{Cat})}(\mathsf{PaB},\mathsf Q)\ \xrightarrow{\ \sim\ }\ \bigl\{(m,a,c)\ \big|\ \text{pentagon}+\text{hexagon}\times2\bigr\}.$$
- Part 2 も同型式("*Fixing an operad morphism $\phi$ … **amounts to** fixing …*")。

> ★ **一意性の範囲の明確化(重要)**: 一意性は「**対象上恒等な射の中で**」ではなく「**$\phi(\mu)=m$ を満たす射の中で**」である。対象写像は仮定ではなく、$m$ から**決まる** — 正典の逐語(p.375):
> "*We also consider the obvious morphism of operads in sets $\phi:\Omega\to\mathrm{Ob}\,R$, which underlies this morphism of operads in groupoids at the object set level, and which is **determined by the assignment $\phi(\mu)=m$ by using that the magma operad $\Omega$ represents the free operad generated by the operation $\mu\in\Omega(2)$**.*"

### 5.3 ★ 工房の使用はこの量化に入るか(4 条件の逐一検査)

工房の (TR-3) は $Q:=\widehat{\mathrm{PaB}}$(2008 の副有限完備化)を代入する。

| # | 6.2.4(b) が要求するもの | $\widehat{\mathrm{PaB}}$ での成否 | 根拠 |
|---|---|---|---|
| 1 | $\mathsf Q$ が **Cat 内の operad**(位相は忘れてよい) | ✔ | $\widehat{\mathrm{PaB}}(n)$ は位相 groupoid;位相を忘れれば小圏。arity ごとの $\Sigma_n$ 作用と $\circ_i$ は関手 |
| 2 | $m\in\mathrm{Ob}\,\mathsf Q(2)$ | ✔ $m:=\mu$ | 2008 (CPL) p.49 "*with the same set of objects*" ⟹ $\mathrm{Ob}\,\widehat{\mathrm{PaB}}=\Omega$ |
| 3 | $a\in\mathrm{Mor}_{\mathsf Q(3)}(m\circ_1m,\ m\circ_2m)$、$c\in\mathrm{Mor}_{\mathsf Q(2)}(m,(1\,2)m)$ が**同型** | ✔ | $\widehat{\mathrm{PaB}}(n)$ は groupoid ゆえ全射は同型。$a:=\alpha'=\hat U(\alpha)$、$c:=\beta'=\hat U(\beta)$ |
| 4 | $(a,c)$ が **pentagon + hexagon 2 本**を $\mathsf Q$ の中で満たす | ✔ | **工房の (TR-2)** が示している。**そこで使う挿入は $(3,2)\to4$, $(2,3)\to4$, $(2,2)\to3$ のみ**で、すべて切詰めに残っている |

$$\boxed{\ \textbf{工房の使用は 6.2.4(b) の量化の中に完全に入る。(TR-3) は正当化される。}\ }$$

> ★ **さらに強いこと(【GAP-TRUNC-1】の閉鎖)**: 工房 §E-A.9.4 は (A1) を「表示」と読むために **【前提 (FREE-OP)】(自由 operad $F$ の存在と合同商 $F/R$)** を置き、それを【GAP-TRUNC-1】として open にしていた。**Fresse 6.2.4(b) は普遍性を定理として直接与えるので、この構成は要らない**。⟹
> $$\textbf{【GAP-TRUNC-1】(FREE-OP)は閉じる。}$$
> ただし格は「**工房の自前構成**」から「**Fresse Thm 6.2.4(b)(刊行版・証明本文 present)への相対**」へ移るのであって、**Lean verified になるのではない**(便 99 F99-3.6 の Sol 逐語の趣旨は不変)。

---

## 6 完備化との接合(委嘱の問い ③)— **残余の名指し**

### 6.1 Thm 6.2.4 自体は完全に離散

言明にも証明にも位相・完備化・連続性は**一度も現れない**。工房 §E-A.9.4 の★注「**表示は離散の $\mathrm{PaB}$ のものでよい。標的が副有限であることは邪魔にならない**」は**正しい**(6.2.4(b) の $\mathsf Q$ は任意)。

### 6.2 Part 1 に profinite operad 完備化の一般論はあるか — **無い**

- 全文検索(`profinite`)で §6 には 0 件。出現は**第 12 章 "A glimpse at the Grothendieck program"(pp.423–424)のみ**で、そこでの $\widehat{GT}$ は **Drinfeld の $\widehat F(x,y)$ 版**(式 (4):$\phi(x)=x^\lambda$, $\phi(y)=f^{-1}y^\lambda f$)であり、**operad の完備化ではない**。
- Part 1 が持つ完備化の普遍性は **§10.1 の Malcev 版**:**Theorem 10.1.4**(随伴 $\eta:\mathrm B\to\widehat{\mathrm B}$)と **Proposition 10.1.5**。後者は逐語で "***If we take $k=\mathbb Q$** as coefficient ring for our Malcev completion process*" と条件づけられており、**profinite 版は存在しない**。

### 6.3 Part 2 の profinite 注記の実体

p.12 逐語:
> "*We use a similar construction to define the profinite completion of our operad $\widehat{\mathrm{PaB}}$ and the profinite Grothendieck–Teichmüller group $\widehat{GT}$. **(We just need to take care of the continuity constraints in the definition of morphisms in this case.)** … We explain our constructions in full details in the case of the rational Grothendieck–Teichmüller group only, **because the profinite analogues of these constructions is obvious**.*"

そして Malcev 側の該当命題は
> "*Any morphism $\phi:\mathrm{PaB}\to\widehat{\mathrm{PaB}}_{\mathbb Q}$ admits a **unique extension** to the completed operad $\hat\phi:\widehat{\mathrm{PaB}}_{\mathbb Q}\to\widehat{\mathrm{PaB}}_{\mathbb Q}$.*"(p.12)

⟹ **工房の (TR-4) に対応する主張は、Malcev では書かれているが profinite では "obvious" の一語で飛ばされている。**

### 6.4 ★ 残余の格付けと、工房側の状態

$$\boxed{\ \textbf{(TR-4) は Fresse の射程外。ただし工房の穴ではない — 工房は自前で証明している。}\ }$$

**起草者による (TR-4) の再検査**(§E-A.9.4・独立再走):

| 検査点 | 結果 |
|---|---|
| 段 1 の「核」$\sim'$ が (CPL) の 3 条件を満たすか | ✔ ① source/target 保存($\psi_\sim$ は対象上恒等な関手 — $\Phi$ が対象上恒等、$q_\sim$ も (CPL) の "*with the same set of objects*" により対象上恒等)② 合成両立(関手)③ 有限(有限 groupoid の射集合へ単射) |
| 段 2 の錐の整合 | ✔ 稠密性 + 標的 Hausdorff(有限離散)の標準論法 |
| 添字 poset の有向性 | ✔ 2008 A.5 が有向 poset として定義 |
| 段 3 の operad 構造との整合 | ✔ 稠密 + Hausdorff |
| 一意性 | ✔ 同上 |

⟹ **健全。追加の外部依存は生じない。**

> ### 【文献要請 IHNEC-L4】(**低優先・任意**)
> **困難**: (TR-4) は工房の自前証明で立っており**穴ではない**が、Part 1 が Malcev 側で持つ「完備化は随伴」という**一般機構**(Thm 10.1.4 / Prop 10.1.5)の **profinite 版**があれば、(TR-4) は 3 行の引用に置き換わり、格が「工房の自前証明」から「引用済文献の定理」へ上がる。
> **欲しい結果の型**: 「**groupoid 内 operad の副有限完備化は、副有限 groupoid 内 operad の圏への忘却関手の左随伴である**」— すなわち $\mathrm{Hom}_{\mathrm{Op}(\mathbf{ProfGrd})}(\widehat{\mathrm P},\mathsf Q)\cong\mathrm{Hom}_{\mathrm{Op}(\mathbf{Grd})}(\mathrm P,\mathsf Q)$($\mathsf Q$ が副有限 operad のとき)。
> **なぜ低優先か**: 現状で証明は閉じており、**格の見栄えの問題**だからである。**司令塔の判断で発注不要としてよい。**

---

## 7 ★★ unitary 版の差(委嘱の問い ④)— **版ずれの発見**

### 7.1 三者の規約

| 文書 | $\mathrm{PaB}(0)$ | 記号 | 逐語 |
|---|---|---|---|
| **Fresse Part 1** | **空**(非 unitary) | $\mathsf{PaB}$ / unitary 版は $\mathsf{PaB}_+$ | $\Omega^+(n)=\ast\ (n=0)$, $\Omega(n)$ otherwise(p.200)。$\mathsf{PaB}_+$ は §6.2.2 以降で明示的に別記号 |
| **Fresse Part 2** | **$\ast$**(unitary) | $\mathsf{PaB}$ が Part 1 の $\mathsf{PaB}_+$ を指す | "*a strict unit, which is given by the arity zero element of our operad $\ast\in\Omega(0)=\mathrm{Ob}\,\mathsf{PaB}(0)$*"(p.11);"*we automatically have $\phi(\ast)=\ast$ **since $\mathsf{PaB}(0)=\ast$***"(p.12) |
| **arXiv 2008.00066**(工房の正典) | **空**(**非 unitary**) | $\mathrm{PaB}$ | "*Since the groupoid $\mathrm{PaB}(0)$ is **empty**, Theorem A.1 implies …*"(p.12) |

### 7.2 判定

$$\boxed{\ \textbf{工房の使用は}\textbf{非 unitary}\textbf{。したがって正しい引用先は Part 1 }\textbf{Theorem 6.2.4(b)}\textbf{ である。}\ }$$

- 工房 §E-A.9 は **$e$ の strict unit 関係を一切使っていない**。(TR-2) が輸送するのは pentagon(arity 4)と hexagon 2 本(arity 3)だけであり、**arity 0 に触れる段が無い**。⟹ **齟齬なし**(委嘱の問い ④ への直接の答え)。
- ★ **しかし引用先の版がずれている**: 追記 F.2 と台帳 §1.5 が pin する **Part 2 Thm 1.1.5 は unitary 版**であり、四つ組 $(m,e,a,c)$ と strict unit 関係 $m\circ_1e=1=e\circ_1m$ を**要求する**。$\mathrm{PaB}(0)=\emptyset$ の設定では $e$ が存在しないので、**1.1.5 は工房の使用を literally 覆わない**。
- **Part 1 Theorem 6.2.4(b) は unit 条件を一切要求しない非 unitary の核**である。⟹ **Part 1 の収蔵(裁定 425)は「あった方がよい」ではなく「必要だった」**。

> ⚠ **これは追記 F.2 の判定 F99-3.6(「外部定理への相対的 paper-proof として PASS」)を覆すものではない** — 数学的内容は同じであり、**引用先の版を精密化する訂正**である。

---

## 8 §6.3(PaS 版)との対比・切詰めについての副次観察

### 8.1 §6.3 との対比(委嘱の任意項)

| | **Thm 6.2.4**(PaB・braided) | **Thm 6.3.2**(PaS・symmetric) |
|---|---|---|
| $c$ への追加条件 | なし($c$ は involutive で**ない** — "*the braid which represents this isomorphism … is not involutive either*", Part 2 p.10) | ★ **involution 関係 $c(x_1,x_2)c(x_2,x_1)=\mathrm{id}$ を要求** |
| hexagon | ★ **2 本とも要る** | ★ **"(any one of) the hexagon diagrams"** = **1 本で足りる** |
| 証明 | **`present`**(Step 1–4) | **`omitted` / reader_exercise** |

> ★ **工房への含意**: 「hexagon 2 本の独立性」は **braided と symmetric を分ける当の条件**である。involution を落とすと 2 本目が 1 本目から従わなくなる。主線 $B_3$-gentle 系が hexagon のみを課す($\widehat{GT}_0$ 側)ときも、**2 本を独立に課していること**が本質であることの正典側の裏づけとして使える。

### 8.2 ★ 切詰め版 (A1$^{\le4}$) についての精密化(工房の依存を 1 本細くする)

2008 p.12–13 の 1 行演繹は 2 つの主張からなる:
- **(生成半)** $\mathrm{PaB}^{\le4}$ は $\alpha,\beta$ で生成される。
- **(関係半)** $\mathrm{PaB}^{\le4}$ における $\alpha,\beta$ の全関係は pentagon (2.13) と hexagon (2.14)(2.15) の帰結。

**起草者の判定**:

| 半分 | 6.2.4 からの支持 | ★ **工房の TRUNC が使うか** |
|---|---|---|
| **生成半** | ★ **支持あり** — 6.2.4(a) の証明(Step 1)の中間 arity は全て $\le r$ に収まる(§4.1 の帳簿)⟹ $r\le4$ なら切詰めの中で閉じる | ✔ **使う**((TR-1) の切詰め版・(TR-5)) |
| **関係半** | ★ **6.2.4 の射程外**(6.2.4 は非切詰めの $\mathrm{PaB}$ のみを扱う。切詰め自由 operad の合同の議論は別物) | ★ **使わない** — (TR-1) の切詰め版は**生成半だけ**で閉じる(等化子 $E$ が部分切詰め operad で $\alpha,\beta$ を含む ⟹ 全体)。(TR-2) は $\hat U$ の関手性・$\circ_i$ 両立・$S_n$ 同変性しか使わない |

$$\boxed{\ \textbf{工房の補題 TRUNC}^{B_4}\textbf{ が (A1}^{\le4}\textbf{) に掛ける荷重は「生成半」だけであり、それは 6.2.4(a) の帳簿から裏が取れる。}\ }$$

⟹ **依存表の (A1$^{\le4}$) 行は「関係半は未使用」と注記すべき**(§10 の訂正表 C-4)。

---

## 9 ★ 副産物 — 規約 (OBJ) は落とせる見込み(**candidate**・追記 F.1 項 2 への回答)

### 9.1 何が変わるか

工房 §E-A.9.1 は $\mathrm{Aut}(-)$ を「**対象上恒等**」に限る規約 (OBJ) を置き、「規約を落とした場合の可否は射程外(**UNKNOWN**)」と申告した。追記 F.1 項 2(Sol 指摘)は「全 automorphism を採るなら $S_2$ 部分と object-fixed 部分の TRUNC が両立することを**一段示す必要がある**」と宿題にしていた。

**6.2.4(b) はこの宿題を構造的に解く**: 対象写像は**仮定ではなく引数 $m\in\mathrm{Ob}\,\mathsf Q(2)$** だからである。しかも
$$\mathrm{Ob}\,\widehat{\mathrm{PaB}}(2)=\Omega(2)=\{\mu,\ t\mu\}\quad(\text{2 元}),$$
であり($\Omega$ は $\mu$ 上の自由 operad — (FREE-Ω) pin;工房 §E-A.9.1 の Catalan 検算 $|\Omega(n)|=\mathrm{Cat}(n-1)\cdot n!$、$n=2$ で 2 と一致)、**対象上の自由度は $S_2$ ちょうど**である。

### 9.2 命題(candidate)

> ### 命題 TRUNC-FULL(**candidate・Sol 未監査**)
> $\mathrm{Aut}^{\rm full}(-)$ を「**対象上恒等を仮定しない**連続 operad 自己同型」の群とする。このとき
> $$\mathrm{res}:\ \mathrm{Aut}^{\rm full}(\widehat{\mathrm{PaB}})\ \xrightarrow{\ \sim\ }\ \mathrm{Aut}^{\rm full}(\widehat{\mathrm{PaB}}^{\le4})$$
> は群同型である。すなわち **規約 (OBJ) は補題 TRUNC$^{B_4}$ に必要ない。**

**証明の骨子**(6 段の逐語移植 — 変更は 1 箇所のみ):

- **単射**: $A,B$ が $\mathrm{res}$ で一致 ⟹ 対象写像は $\mu$ 上で一致($\mu\in\Omega(2)$ は切詰めの中)⟹ (FREE-Ω) より $\mathrm{Ob}\,A=\mathrm{Ob}\,B$。さらに $\alpha,\beta$ 上一致 ⟹ $A\circ\iota,\ B\circ\iota:\mathrm{PaB}\to\widehat{\mathrm{PaB}}$ は同じ三つ組 $(m,a,c)$ を与える ⟹ **6.2.4(b) の一意性**より一致 ⟹ 稠密 + Hausdorff で $A=B$。
- **全射**: $U\in\mathrm{Aut}^{\rm full}(\widehat{\mathrm{PaB}}^{\le4})$ に対し $m:=U_{\rm Ob}(\mu)$, $a:=U(\alpha)$, $c:=U(\beta)$ と置く。
  - **型の確認**: $U_{\rm Ob}$ は $\Omega^{\le4}$ の operad 自己同型ゆえ $U_{\rm Ob}(\mu\circ_i\mu)=m\circ_im$、$\Sigma_2$ 同変性より $U_{\rm Ob}((1\,2)\mu)=(1\,2)m$。⟹ $a\in\mathrm{Mor}(m\circ_1m,m\circ_2m)$、$c\in\mathrm{Mor}(m,(1\,2)m)$ — **6.2.4(b) が要求する型ちょうど**。
  - **関係式**: (TR-2) の論法をそのまま走らせる。**唯一の差**は $\hat U(\mathrm{id}_{\mu})=\mathrm{id}_{U_{\rm Ob}(\mu)}=\mathrm{id}_m$(工房版は $\mathrm{id}_\mu$)。**Fresse の pentagon / hexagon は最初から一般の $m$ について書かれている**(Fig 6.1 / Fig 6.6 の $x_1\square x_2$ 記法)ので、輸送先はちょうど三つ組 $(m,a,c)$ に対する Fig 6.1 / Fig 6.6 である。
  - **6.2.4(b)** ⟹ $\Phi:\mathrm{PaB}\to\widehat{\mathrm{PaB}}$、**(TR-4)** ⟹ $\widehat\Phi$、**(TR-5)** ⟹ $\mathrm{res}(\widehat\Phi)=U$ と可逆性。

> ⚠ **格の申告**: これは **candidate** である。**Sol 未監査**。とくに (i) 切詰め側の対象 operad $\Omega^{\le4}$ で「$U_{\rm Ob}$ が $\mu$ の像で決まる」段(切詰め自由性)、(ii) $\mathrm{res}$ の全射性で使う切詰め生成半(§8.2)、の 2 点を明示的に書き下すこと。**本ノートは骨子までで、完全な書き下しはしていない。**
> ⚠ また本命題は「**両群が同型**」を言うだけで、「$m=t\mu$ となる自己同型が実在するか」は**別問題(UNKNOWN)**である。混同しないこと。

### 9.3 追記 F.1 項 3 への回答

追記 F.1 項 3 は「Catalan 数列の一致は**有限 sanity check** であって $\mathrm{Aut}_{\rm operad}(\Omega)\cong S_2$ の証明ではない」と格を固定していた。**本ノートの (FREE-Ω) pin(p.375 / p.200 の逐語)により、$\Omega$ の自由性は正典の逐語で確定する。** ⟹ $\mathrm{Aut}_{\rm operad}(\Omega)\cong S_2$ は自由性から従い、**格は「傍証」から「正典の逐語に乗る」へ上がる**(★ ただしこの一行の導出自体は工房のものである)。

---

## 10 ★ 判定と、既存文書への訂正・伝播

### 10.1 判定(1 行)

$$\boxed{\ \textbf{補題 TRUNC}^{B_4}\textbf{ の Fresse への依存は }\textbf{6.2.4 の射程内}\textbf{ である。射程外の残余は 3 本あり、いずれも工房側で埋まっているか pin の訂正で済む。}\ }$$

**残余の列挙**:

| # | 残余 | 格 | 状態 |
|---|---|---|---|
| **(R1)** | **profinite 完備化の普遍性**((TR-4))— 6.2.4 は離散のみ。Part 1 の完備化随伴は **Malcev 専用**(Prop 10.1.5)、Part 2 の profinite 版は **"obvious" の一語**(`omitted / silent_omission`) | ★ **6.2.4 の射程外** | ★ **工房の自前証明で閉じている**(§6.4 で再検査・健全)。文献で置き換えたいなら【文献要請 IHNEC-L4】(低優先・任意) |
| **(R2)** | **切詰め版 (A1$^{\le4}$) の関係半** — 6.2.4 は非切詰め $\mathrm{PaB}$ のみ | ★ **6.2.4 の射程外** | ★ **工房の TRUNC は使っていない**(§8.2)。**生成半**は 6.2.4(a) の帳簿から裏が取れる ⟹ **荷重ゼロ** |
| **(R3)** | **引用先の版ずれ** — 追記 F / 台帳 §1.5 の pin(Part 2 Thm 1.1.5)は **unitary 版**。工房の使用は非 unitary | **pin の誤り**(数学の穴ではない) | ★ **本ノートで訂正**。正しい引用先 = **Part 1 Theorem 6.2.4(b)** |

**加えて、底の底の格の申告**(隠さないために書く): 6.2.4 の Step 2 は **Theorem 6.1.7** に依り、6.1.7 の justification は環境名が `Proof.` ではなく **`Explanations.`** で、その中の一段(「路の間の全関係が pentagon と square に帰着する」)は **Mac Lane [130] / Stasheff [167] へ委譲**されている(§2 (F617))。**リスク評価は低**(Mac Lane coherence は 60 年来の標準定理)だが、**依存の底は「Fresse で止まる」のではなく「Mac Lane coherence まで降りる」**のが正確な絵である。

### 10.2 既存文書への訂正表(**本ノートが effective source**・本文不改変)

| # | 対象 | 現状の記述 | ★ **本ノート後** |
|---|---|---|---|
| **C-1** | `docs/notes/ihnec_v1_addendum_e_b4.md` 追記 F.2 の格 | 「補題 TRUNC$^{B_4}$ の格 = **Fresse Thm 1.1.5 相対**(現物 pin 済)」 | ★ 「**Fresse Part 1(刊行版・SURV 217)Theorem 6.2.4(b)(pp.212–214・証明本文 pp.214–218・`proof_body_status = present`)相対**」。Part 2 Thm 1.1.5 は **unitary 版**なので工房の非 unitary の使用を literally 覆わない(§7) |
| **C-2** | 同 追記 F 末尾 「【GAP-TRUNC-1】(FREE-OP・圏論的包装)は**依然 open**(Fresse Thm 1.1.5 が普遍性の形で述べられているかは本追記では未判定 — 原文 p.9–10 の精読は未実施)」 | ★ **閉じる**。6.2.4(b) は**普遍性の形**で述べられており(§5.2 の全単射)、自由 operad + 合同商の構成は**不要**(§5.3 の★枠) |
| **C-3** | 同 §E-A.9.1 の (OBJ) 「規約を落とした場合の可否は本節の射程外(**UNKNOWN**)」/ 追記 F.1 項 2 の宿題 | ★ **落とせる見込み(candidate)** — 命題 TRUNC-FULL(§9.2)。**Sol 監査必須** |
| **C-4** | 同 §E-A.9.2 の (A1$^{\le4}$) 行 | 証明本文「なし(Thm A.1 からの 1 行演繹・地の文)」 | ★ 現状維持。**ただし「工房が荷重を掛けるのは生成半のみで、それは Fresse 6.2.4(a) の証明の arity 帳簿から裏が取れる」を注記**(§8.2) |
| **C-5** | 同 §E-A.9.1 の Catalan 検算の格(追記 F.1 項 3) | 「自由性の**傍証**」 | ★ **正典の逐語(Part 1 p.375 / p.200)で自由性は確定**。Catalan は sanity check のまま(格付けは変えない)が、**自由性そのものは傍証でなく pin に乗る**(§9.3) |
| **C-6** ★ | `docs/notes/conventions_ledger_v1.md` §1.5 の動機欄「2008 Thm A.1 = **external_reference**[Fresse, Homotopy of Operads Part 2, Thm 1.1.5 **pp.9-10** — 便 99 F99-3.6 で pin 済]」 | ★ **2 点訂正**: ① 頁は **p.11**(profinite 注記は p.12)— 起草者が頁画像 `p2p11-11.png` で確認 ② 引用先は **Part 1 Thm 6.2.4(b)** が正(Part 2 1.1.5 は unitary 再掲)。**§1.5 の `external_reference` 要件(引用先定理・版・頁画像 pin・取得 digest)は本ノート §1.2 / §2 で全て充足** |
| **C-7** | 委嘱文・地図の頁見積り「Theorem 6.2.4・約 pp.215-220」 | — | ★ **言明 pp.212–214 / 証明 pp.214–218 / Lemma 6.2.5 p.218**(§1.1) |

### 10.3 ★ 原文の微細な不精確(**数学の穴ではない** — 誠実な申告として記録)

| # | 箇所 | 内容 | 影響 |
|---|---|---|---|
| **T-1** | Step 1(p.214) | "*each factor $\beta_i$ … consists … of a **single generating element $\tau_k$** of the braid group $B_r$*" — **$\tau_k^{-1}$ に言及していない**。一般の組紐語は $\tau_k^{\pm1}$ の語 | **無害**。$c$ は同型と仮定されているので $c^{-1}$ を使えばよく、自由簡約 $\tau_k\tau_k^{-1}=1$ の場合の well-defined 性も即座 |
| **T-2** | Fig 6.6 の caption(p.213) | "*the expressions $(x_1\square x_2)\square x_3,\dots\in\mathrm{Ob}\,\mathsf Q(4)$*" — hexagon は arity **3** なので $\mathrm{Ob}\,\mathsf Q(3)$ が正 | 誤植。図本体は正しい |
| **T-3** | Fig 6.6 の caption(p.213) | "*the operadic composition functor $\circ_1:\mathsf Q(2)\times\mathsf Q(2)\to\mathsf Q(2)$*" — 正しくは $\to\mathsf Q(3)$ | 誤植 |
| **T-4** | 6.2.4(b) / 6.1.7(b) の結論文 | $\mathsf Q$ は「operad in **categories**」なのに結論を "*a morphism of operads in **groupoids** $\phi:\mathsf{PaB}\to\mathsf Q$*" と書く | 語法の緩み。**工房の使用($\mathsf Q=\widehat{\mathrm{PaB}}$ は groupoid)では問題にならない** |

---

## 11 ★ Sol への監査依頼(次便のゲート項目)

1. ★★ **命題 TRUNC-FULL(§9.2)の骨子**に穴はないか — とくに (i) 切詰め対象 operad $\Omega^{\le4}$ での「$U_{\rm Ob}$ は $\mu$ の像で決まる」段、(ii) 全射性で使う切詰め生成半。**これが通れば規約 (OBJ) を落とせる。**
2. ★ **§8.2 の判定**(工房の TRUNC が (A1$^{\le4}$) に掛ける荷重は**生成半のみ**)に異論はないか。
3. ★ **§7 の版ずれ判定**(非 unitary の使用に対して Part 2 Thm 1.1.5 は不適・Part 1 Thm 6.2.4(b) が正)に異論はないか。
4. **§6.4 の (TR-4) 再検査**(profinite 完備化の連続延長)— Sol の独立確認を請う。
5. **§10.1 の「底は Mac Lane coherence まで降りる」**という格の絵に異論はないか。

## 12 司令塔への申し送り

1. ★★ **【GAP-TRUNC-1】を閉じてよい**(§5.3)。**ただし「穴が消えた」ではなく「工房の自前構成が、証明本文つきの刊行版定理の引用に置き換わった」と書くこと。**
2. ★ **【GAP-TRUNC-2】の記述を更新**: 「2008 Thm A.1 に証明本文が無い」は不変。引用先は **Part 1 Thm 6.2.4(b)・`proof_body_status = present`・証明本文 pp.214–218** で確定 ⟹ **external_reference の連鎖がここで `present` に着地する**(依存の梯子が 1 段上がった)。
3. ★ **台帳 §1.5 の動機欄の頁 pin を訂正**(C-6)— **pp.9-10 → p.11**。**裁定として記録を**。
4. **追記 F.2 の格の読み替え**(C-1)を地図・依存表へ伝播。
5. **【文献要請 IHNEC-L4】は低優先・任意**(§6.4)— 発注しない判断で差し支えない。

---

## 13 自己申告・grep 語

- **読んだ範囲**: Part 1 = §6.1(pp.198–208)・**§6.2 全部(pp.208–220)**・§6.3(pp.220–224)・§10.1 の Prop 10.1.5 周辺・§10.3 の p.375・§12 の profinite 節(pp.423–424)+ 全文の `profinite` / `Theorem 6.2.4` 検索。Part 2 = pp.10–13(§1.1.4–1.1.6)+ 全文の `profinite` 検索。**その他は未読**(全 581 頁の精読はしていない)。
- **機械照合**: `pdftotext -layout` 全文抽出 + `pdftoppm -png -r 120` による**頁画像視認**(§1.2 の 6 頁)。sha256 は `Get-FileHash` で独立計算。**手写しの値はない。**
- **推測と証明の峻別**: §9 の命題 TRUNC-FULL は **candidate(骨子のみ・未書き下し)**。§8.2 の「生成半は帳簿から裏が取れる」は**起草者の読み**であり Fresse が明言してはいない(**paper-proof candidate**)。それ以外の §2–§7 は**逐語 pin と直接の演繹**である。
- **grep 語**: `Fresse`・`6.2.4`・`6.1.7`・`Lemma 6.2.5`・`TRUNC`・`GAP-TRUNC-1`・`GAP-TRUNC-2`・`FREE-OP`・`OBJ`・`unitary`・`PaB_+`・`magma operad`・`Mac Lane`・`dodecagon`・`SURV 217`・`Thm 1.1.5`・`IHNEC-L4`・`TRUNC-FULL`。
