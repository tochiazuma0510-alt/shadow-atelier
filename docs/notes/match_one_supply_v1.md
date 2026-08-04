# 【MATCH-one】の **(M-a)** — 同一 matched window での **(5′)@α** の族的供給(v1)

**状態札: `candidate(単系統・Sol 未監査)/ 供給は「見込み」であって「済」ではない(§5.3)/ Lean 検証ではない / SURJ も ord(a_n) も結論しない / 封印非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設 v1**
- 委嘱: 司令塔「(M-a) = 同一 matched window での (5′)@α の族的供給を起草。(i) 便 103 F103-4 の発効見込みと B-7 系の per-window 前件((Z_{2M}-link) 型)の族整理 (ii) 供給できる窓の最小十分集合と per-n 手続き (iii) $n\in\{3,5,7,9\}$ の供給状態 (iv) 供給が立たない $n$ の fallback」
- **依拠(正典 + repo 内のみ・外部文献ゼロ)**
  - `sol/sol_reply_103_math30.md` **§4(F103-4)**((5′) の格)・**§5**(MATCH-one の受理)
  - `docs/week4-BFC攻略_opus_v2.md`: **§9 定理 B-7**(= $B_{\rm FC}$)・**系 B-7′**・**§10 系 B-8($b$-頑健性)**・**§8.1 定理 B-7$^{\rm tw}$**・**§13.1 前件表**・**【v2.7・F7】前件の型列挙(link 要否表)**・§0 の v2.12/v2.13 修理欄
  - `docs/week4-K3飽和_opus_v3.md` §5.2.1–§5.2.2(前件 (0)–(6′)・定理 $R^{\rm cyc}_{\rm formal}$ の証明 2・3・5)
  - `docs/notes/s3_family_completion_v1.md`(**【MATCH-one】**・**定理 SIXP-fam**・補題 Λ-REG)/ `docs/notes/s3_family_draft_v1.md`
  - `docs/notes/oddH_full_proof_v1.md`(補題 C(2)・補題 G・補題 H=(1.3))/ `docs/notes/w2fam_v1.md`(**(W2)-fam**)/ `docs/notes/c21_draft_v1.md` §4・§7(**A7-fam**・裁定 214)
  - `docs/znorm_apply_patches_v1.md`(`Z-norm-seal/v1` の window inventory 規則)/ `docs/notes/fam_u_assembly_addendum_C_draft_v1.md` §C.1.1・§C.4 / `docs/notes/asm_alpha_falsifier_v1.md`(F-1・F-3)

> ## 遵守申告
> - **矢印跨ぎ禁止**: 本稿は **(M-a) の供給可能性だけ**を扱う。$\mathrm{ord}([u_n]_{2n})=n$ にも $\mathrm{ord}(a_n)=n$ にも $\mathrm{Ih}$ の全射性にも**触れない**。総組立の値・測定値は一切現れない。
> - **封印非接触**: $K^{(5)}$ の値・窓データ・測定値・$\hat c_\mu$・$\varepsilon$ bits・PSL 欄に触れていない。$n=5$ について本稿が書くのは **window inventory の行の状態**(`migrated` 等)という**会計事実**のみで、これは `docs/week4-BFC攻略_opus_v2.md` §0/§13.1 の公開記述の転記である。
> - **有限計算 bundle と seal の現況は本稿を正としない**(BFC v2 §15.7 の規律): 現況の正本は `certificates/bfc/`・`provenance/CLAIMS.md`・receipt。本稿は**依存の型**を書くのであって現況台帳ではない。
> - **新規性**: §2 の twist 不感性は **既在(系 B-8)**。§5 の link-free 経路も **既在の型列挙表(BFC v2【v2.7・F7】)の行**である。本稿の寄与は**それらを (M-a) の族供給という問いに接続したこと**に限る(§9 で申告)。

---

## 0. 判定(先に 5 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | **(M-a) は本当に (5′) の exact 形を要るか** | ★★ **要らない**。$R^{\rm cyc}_{\rm formal}$ が (5′) を使う 3 箇所(証明 2・3・5)は**単元冪 $\xi\mapsto\xi^b$ に不感**であり、**twisted 形 (5′$^b$) で十分**(= **既在の系 B-8**)。⟹ **exact $\varepsilon=1$ も $(Z_{2M}$-link$)$ も (M-a) の要求側には現れない** |
| **②** | **最小十分集合はどんな形か** | ★★ **$\{\alpha=1\}$ — 全奇数 $n$ で同一の窓ラベルの単一窓**。BRIDGE-one の「ある一つ」は **$n$ ごとに探す必要がなく、族一様に $H_n^{\rm fun}=H_{2,1,0}$ で取れる**(§5)。窓前件 (W1)–(W5)+(CAL)+(2)+(F) はすべて族定理供給(§4) |
| **③** | **per-n の手続きは要るか** | ★ **経路による**。**Route T(twisted・link-free)= 要らない**(seal 行為ゼロ・versioned 行為ゼロ)。**Route E(exact・現行 proof ID)= 要る** — 窓ごとの $(Z_{2M}$-link$)$ migration(`inventory=migrated` + receipt 束縛の digest)= **$O(\#n)$ の seal 手続き** |
| **④** | **未閉の一点はどこか** | ★★ **「B-6$^{\rm tw}$ の link-free proof ID」が未提示**(BFC v2【v2.7・F7】表の自認)。⟹ **(M-a) の族供給は「見込み」であって「済」ではない**。ただしこれは **per-window ではなく 1 本の一般論**であり、**$O(\#n)$ の seal 手続きを $O(1)$ の証明仕事に替える**(§9 FINDING MOS-1) |
| **⑤** | **便 103 F103-4 との関係** | ⚠ **要確認**。F103-4 は (5′) を `theorem-framework-relative [TB: canonical-source-pinned/v2]` として条件付き PASS したが、**$(Z_{2M}$-link$)$ の per-window 行に言及していない**。この格が link を discharge したのか、link 行が会計から**黙って落ちた**のかを確定させる必要がある(§11 監査点 1) |

---

## 1. 問いの固定 —(M-a) とは何を供給することか

`s3_family_completion_v1.md` §11–§12 の **【MATCH-one】**:

$$\exists\alpha\in(\mathbf Z/n)^\times:\ \bigl[\ \underbrace{(5')@(K^{(n)},H_{2,\alpha,0})}_{\textbf{(M-a)}}\ \wedge\ \underbrace{\text{手元の類}=[u_{n,\alpha}]_{2n}}_{\textbf{(M-b)}}\ \bigr].$$

本稿の標的は **(M-a) だけ**である。(M-b)(組立/測定が当該窓の量であること)は C1′ 系の問題であり、本稿は扱わない。

**(5′) の逐語**(week4 v3 §5.2.1):
$$\rho_0\bigl(\mathrm{Ih}_N(\gamma)\bigr)=\tau\bigl(\kappa_{u^{-1}}(\gamma)\bigr)\qquad(\forall\gamma\in G_K),\qquad K=F_n=\mathbf Q(\zeta_{4n}),\ M=2n. \tag{7.3}$$

**供給者の同定**(既在): $B_{\rm FC}$ = **定理 B-7**(BFC v2 §9・boxed state「$B_{\rm FC}$(定理 B-7)」)。その結論 (9.1) が逐語で (5′) = (7.3) である。

$$\boxed{\ \textbf{(M-a) の供給}\ =\ \textbf{窓 }(K^{(n)},H_{2,\alpha,0})\textbf{ で定理 B-7 系の結論 (9.1) を得ること}\ }$$

---

## 2. 要求側の縮約 — (M-a) が本当に要るのは **twisted 形**である

### 2.1 既在の系 B-8($b$-頑健性)

> **系 B-8(BFC v2 §10・逐語)**: $b\in(\mathbf Z/M)^\times$ を任意とし、(9.1) の代わりに
> $$\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau\bigl(\kappa_{u^{-1}}(\gamma)^b\bigr)\qquad(\forall\gamma\in G_K)\tag{10.1}$$
> を仮定しても、$R^{\rm cyc}_{\rm formal}$ の結論 **(R6-full)** と **(7.4)** は**変わらない**。
> **証明**(既在): $\xi\mapsto\xi^b$ は $\mu_M$ の自己同型ゆえ (i) 像の位数不変、(ii) $\mu_M[e]$ は特性部分群、(iii) $\ker$ 不変。$R^{\rm cyc}_{\rm formal}$ の証明 2・3・5 はこれしか使わない。∎

**本稿による独立確認**(再導出・新規性なし): $R^{\rm cyc}_{\rm formal}$ の証明の 5 段を (5′$^b$) の下で走らせると
- **2**: $\rho_0(\mathrm{Ih}(G_K))=\tau(\kappa(G_K)^b)$、$b$ 単元ゆえ $\kappa(G_K)^b=\kappa(G_K)$(部分群の単元冪像は自分自身)⟹ 位数は同じ。
- **3**: $\tau(\kappa(G_K)^b)\subseteq\tau(\mu_M[e])\iff\kappa(G_K)^b\subseteq\mu_M[e]\iff\kappa(G_K)\subseteq\mu_M[e]$(特性部分群)。
- **5**: $\kappa(\gamma)^b=1\iff\kappa(\gamma)=1$。
- **1・4** は (5′) を使わない。

$$\boxed{\ \textbf{(M-a) の要求は }(5')\textbf{ ではなく }(5'^b)\ \textbf{(}\exists b\in(\mathbf Z/M)^\times,\ \gamma\ \textbf{に依らない)で足りる。}\ }$$

### 2.2 ⚠ fitting 禁止規律との整合(★教材)

BFC v2 §15.8(U5)は「**$G_K$-character を見てから $b$ を fitting することは禁止**」と定める。本稿の縮約はこれに**抵触しない** — なぜなら

> **結論が $b$ に依らない**(系 B-8)。ゆえに「都合のよい $b$ を選ぶ」という自由度が**そもそも結論に作用しない**。fitting が禁じられるのは $b$ の選択が結論を左右する場合であり、ここでは左右しない。

ただし **$b$ は $\gamma$ に依らない単一の単元でなければならない**(各 $\gamma$ ごとに別の $b$ を許すと (5′$^b$) は空虚になる)。この一様性は供給側(定理 B-7$^{\rm tw}$)が与える。⟹ **要求文には「$\gamma$ に依らない」を必ず書く**(§5.1 の形)。

---

## 3. 供給側 — B-7 系の前件と $(Z_{2M}$-link$)$ の所在(既在会計の転記)

### 3.1 link はどこで使われるか

BFC v2 の記録(v2.6 E4・v2.7 G2/G6・v2.13 A61-1)より:

- $(Z_{2M}$-link$)$ $=$ 「$\zeta_{2M}^{\rm TB2}=\zeta_{2M}^{\rm Rule1}\in K$(根 object の typed equality)」。**新しい算術仮定ではなく、未指定だった比較データの選択**。
- **使用箇所は 補題 B-6 の証明第 3 段ただ 1 つ**(および B-6$^{\rm tw}$ の対応段)。B-7 / B-7$^{\rm tw}$ はそれを継承する。
- **供給は per-window**: `inventory(window)=migrated` の窓にのみ供給され、receipt が migration record digest を束縛する。**現状: $K^{(5)}$ 供給済 / $K^{(3)}$・$A_5$ pending / その他 `not_assessed`**。
- **`Z-norm-seal/v1` が global に供給するのは TB2 側の profinite root normalization だけ**であり、Rule-side object との link は**窓ごとの migration edge** を要する(便 61 F4 の自認)。

### 3.2 link 要否の型列挙(BFC v2【v2.7・F7】表の該当行・転記)

| 主張 | 前件 | $(Z_{2M}$-link$)$ |
|---|---|---|
| B-3 / B-4(a)・B-4c / B-5 / B-5$^{\rm u}$ | (W1)–(W5)+(CAL)+TB 各種 | **不要** |
| **B-6(現行 proof)** | TB1–TB4+(W1)–(W5)+(CAL) | **必要** |
| **B-6$^{\rm tw}$(現行 proof ID)** | TB1,TB2,TB3,TB4$^{\rm u}$+link+(W1)–(W5)+(CAL) | **必要** |
| ★ **B-6$^{\rm tw}$(link-free proof ID・未提示)** | TB1,TB2,TB3,TB4$^{\rm u}$+(W1)–(W5)+(CAL) | ★ **不要**(ただし $\bar t_M$ を追った導出を**別 proof ID として全文提示**する必要 — 便 51 F2.2) |
| B-7 / B-7$^{\rm tw}$ | 対応 B-6 を継承 | 同上 |
| **B-8** | twisted identity (10.1) | **不要** |

$$\Longrightarrow\quad \textbf{link が要るのは「指数を }1\textbf{(exact)と同定する」ためだけ}\ ;\ \textbf{「}\exists\textbf{ 単元 }b\textbf{」には要らない(はず)}.$$

⚠ **「はず」と書く理由**: 上表の **link-free proof ID は未提示**であり、BFC v2 は「両者を同じ行で並記して『本稿は link-free でもある』と読ませない」と明記している。**本稿もその規律に従い、link-free 経路を「済」とは書かない。**

### 3.3 二つの経路

| | **Route T(twisted)** | **Route E(exact)** |
|---|---|---|
| 供給者 | **定理 B-7$^{\rm tw}$(link-free proof ID)+ 系 B-8** | **定理 B-7**(現行 proof ID) |
| 得る形 | (5′$^{b_{\rm op}}$)($b_{\rm op}\in(\mathbf Z/M)^\times$) | (5′) exact($b=1$) |
| 枠組み前件 | TB1,TB2,TB3,**TB4$^{\rm u}$** | TB1–**TB4**(exact $\varepsilon=1$) |
| per-window link | ★ **不要** | ★ **必要**(migrated 窓のみ) |
| per-n 手続き | ★ **なし** | ★ **窓ごとの migration**(seal 行為・receipt 束縛) |
| 未閉の一点 | **link-free proof ID の全文提示**(1 本・一般論) | **inventory の pending/not_assessed を埋める**($O(\#n)$) |
| $R^{\rm cyc}$ の結論への影響 | ★ **なし**(系 B-8) | なし |

**本稿の勧告: Route T を主線とする。** 理由は 3 点 —(a) $R^{\rm cyc}_{\rm formal}$ の結論が $b$ に不感である以上、exact を要求するのは**要らない強さ**である;(b) Route E は $n$ が増えるたびに seal 手続きが増える(族の定理に $O(\#n)$ の運用コストが付く);(c) BFC v2 自身が §12.1 で「(i)(iii) と (TB4$^{\rm u}$) が取れれば定理 B-7$^{\rm tw}$ が立ち、**系 B-8 と合わせて単一窓の結論((R6-full)・(7.4))はもう出る**」と書いている — **【MATCH-one】は定義上ちょうど「単一窓の結論」である。**

---

## 4. 族供給表 — 窓前件は $\alpha$ でどう供給されるか

定理 B-7 系の**窓前件**を、窓 $(K^{(n)},H_{2,\alpha,0})$($n$ 奇)で族的に洗う。

| # | 前件(BFC v2 §13.1) | 族供給元 | $\alpha$ の射程 | 登録の格 |
|---|---|---|---|---|
| **(W1)** | $\bar N$ 開・$G_{\mathbf Q}$-安定 | 正典 / **W1-fam**(全 $n\ge3$ 一斉・`c21_draft` §5.2) | **窓非依存** | 閉 |
| **(W2)** | 完全列 + $\widetilde\chi\circ\mathrm{Ih}=\chi_{2M}$ | **(W2)-fam**(裁定 120)+ **W2-arith Route A**(裁定 122) | **窓非依存** | candidate |
| **(W3)** | $N_P(H)=H$ | **ODD-H (1.3)**(補題 H(3)) | ★ **全 $\alpha\ne0$** | **既在・証明済**(falsifier F-3 が「真に既在」と確認) |
| **(W4)** | $\langle X\rangle$ が $P/H$ 上推移的・$[P:H]=M$ | **ODD-H 補題 G**((P1)(P3))+ **補題 C(2)** | ★ **全 $\alpha$**($\alpha=0$ も含む) | 数学は既在。⚠ **登録主張(HF-1)は $\alpha=1$ 限定**(falsifier F-3) |
| **(W5)** | $\Lambda$ が $\Phi(\mathfrak F_0)$-安定 | **Sol 便 73 (1.13)(1.14)**(内部自己同型は全共役類を保つ)+ **定理 SIXP-fam(1)** | ★ **全 $\alpha$** | 既在 + 本工房 candidate |
| **(CAL)** | $\alpha^{\rm Ih}=\alpha^{\rm std}$ | $A_5$ v4 §1.4 | **窓非依存** | 閉 |
| **(2)** | $\mathfrak F_0\cong C_e$、$e\mid M$ | 正典 **Thm 4.3 (4.12)** から直接($e=n\mid2n$) | **窓非依存** | ★ 正典 |
| **(F)** | $\rho_0$ が忠実 | ★ **定理 SIXP-fam**(`s3_family_completion_v1.md` §5) | ★ **全 $\alpha\ne0$** | candidate(本工房) |

> ### ★ 読み方(3 点)
> 1. **窓前件はすべて族定理供給であり、$n$ ごとの新規有限計算はゼロ**である(`c21_draft` §4 の A7-fam と同じ構図)。
> 2. **$\alpha$ に依存する行は (W3)(W4)(W5)(F) の 4 本だけ**で、いずれも **$\alpha\ne0$ で成立**する。⟹ **群論側は $\alpha$ の選択を制約しない。**
> 3. ⚠ **しかし $\alpha$ を単元に限る理由は別にある** — 層 1/層 2(ordered passport・`M2-exp`)との整合(falsifier **F-1**)と、登録主張(HF-1 / A7-fam)が $\alpha=1$ であること。**本稿は §5 で $\alpha=1$ を採り、【ASM-α】を開いたままにする。**

---

## 5. 最小十分集合(委嘱 (ii) への回答)

### 5.1 形

> ### 【MOS】(M-a) の最小十分集合【candidate】
> **各奇数 $n\ge3$ に対し、窓を $\alpha=1$、すなわち $H_n^{\rm fun}=H_{2,1,0}$ の**ただ一つ**に固定してよい。** そこで供給すべきものは:
> $$\boxed{\ \textbf{(MOS-1)}\ \ \exists b\in(\mathbf Z/2n)^\times\ (\gamma\ \textbf{に依らない}):\quad \rho_0\bigl(\mathrm{Ih}_{K^{(n)}}(\gamma)\bigr)=\tau\bigl(\kappa_{u^{-1}}(\gamma)^{\,b}\bigr)\quad(\forall\gamma\in G_{F_n})\ }$$
> の 1 本のみ。その供給者は **定理 B-7$^{\rm tw}$(link-free proof ID)**であり、要る前件は
> $$\text{TB1, TB2, TB3, TB4}^{\rm u}\ +\ \underbrace{(W1)(W2)(W3)(W4)(W5)+(\mathrm{CAL})}_{\textbf{§4 で族供給}}\ \ \bigl(+\ \text{結論を使う側で }(2)\ \text{と}\ (F)\bigr).$$
> **$(Z_{2M}$-link$)$ も exact $\varepsilon=1$ も要らない**(§2・§3.2)。

$$\boxed{\ \textbf{最小十分集合}\ =\ \bigl\{\,\alpha=1\,\bigr\}\quad\textbf{— 全奇数 }n\textbf{ で同一ラベルの単一窓。}\ }$$

### 5.2 BRIDGE-one の「ある一つ」がどう実現するか

正本 §4.3 の【S3F-A3 = BRIDGE-one】は「**ある一つの**単元窓で (5′)(6′)」という存在形だった。本稿の帰結は:

- **(6′) は存在形ですらない** — 定理 SIXP-fam により**全** $\alpha\ne0$ で成立(`s3_family_completion_v1.md` §5)。
- **(5′) の存在形は「探索」を要しない** — 窓前件が $\alpha$ に一様(§4)なので、**$\alpha=1$ という族一様な選択で存在が実現する**。$n$ ごとに「どの $\alpha$ なら立つか」を探す作業は**発生しない**。

⟹ **委嘱の問い「各奇数 $n$ のどの単元窓 $\alpha$ で供給されるか」への答え: 全 $n$ で $\alpha=1$。**

### 5.3 ⚠ ただし「見込み」であって「済」ではない

**未閉の一点** = **B-6$^{\rm tw}$ の link-free proof ID が未提示**(§3.2)。これは

- **per-window ではなく 1 本の一般論**である($\bar t_M$ を追った導出を別 proof ID として全文書くこと);
- 提示されるまでは、Route T の供給は **`pending(proof ID 未提示)`**、Route E の供給は **`per-window inventory 依存`**。

$$\boxed{\ \textbf{(M-a) の族供給は「}O(\#n)\textbf{ の seal 手続き」から「}O(1)\textbf{ の証明仕事」へ移せる —— が、その }O(1)\textbf{ はまだ済んでいない。}\ }$$

---

## 6. per-n で要る手続き(委嘱 (ii) 後半)

| 経路 | per-n 手続き | seal / versioned 行為か |
|---|---|---|
| **Route T** | ★ **なし**。窓は $\alpha=1$ 固定、前件は全て族定理。**新規有限計算ゼロ・seal 行為ゼロ** | **発生しない** |
| **Route E** | 窓 $(K^{(n)},H_n^{\rm fun})$ の **$(Z_{2M}$-link$)$ migration**: window inventory 行を `compatibility_status = migrated` にし、**`migrated_record_digest` が実値で解決できる**こと(`znorm_apply_patches_v1.md` P-2) | ★ **seal 手続き**(receipt が digest を束縛)。**versioned**(seal の版に紐づく) |
| 両経路共通(結論を使う段) | なし(窓前件は族供給) | — |

> ### ⚠ Route E について明示すべき 2 点(`znorm_apply_patches_v1.md` P-2 の注の転記)
> 1. **`migrated` は昇格ではない**。root object の同一性を言うだけで、その窓の `root_normalization_level` を `profinite` にはしない。
> 2. **`pending` / `not_assessed` の窓は (R3) を満たさない**ので、**seal 発効だけでは何も宣言できない**($K^{(3)}$・$A_5$ が該当)。
>
> ⟹ Route E を採る場合、**「seal が発効したから全 $n$ で link が付いた」とは書けない**(便 61 F4 が過剰一般化として自認した誤り型)。

---

## 7. $n\in\{3,5,7,9\}$ の具体供給状態(委嘱 (iii))

窓は $H_n^{\rm fun}=H_{2,1,0}$、$M=2n$、$2M=4n$。

| $n$ | $M$ / link 名 | **窓前件(§4)** | **link inventory**(既在会計) | **Route T** | **Route E** | 備考 |
|---|---|---|---|---|---|---|
| **3** | $6$ / $(Z_{12}$-link$)$ | 全て族供給 ✅ | **pending** | ✅(link 不要) | ⚠ pending ゆえ不可 | ★ **(5′)@$K^{(3)}$ は個別に構成済**(week4 v3 §5.2.2 注「2 事例では (5′) を個別に構成した(§2.3(b))」)⟹ **経路に依らず (M-a)@3 は供給されている** |
| **5** | $10$ / $(Z_{20}$-link$)$ | 全て族供給 ✅ | **migrated(供給済)**。ただし **[pre-event candidate]**: operative になるのは receipt 発効後(BFC v2 §9 状態札) | ✅ | ✅(receipt 条件つき) | ⚠ **運用**: $K^{(5)}$ は blind campaign 下。本稿は **inventory の行の状態**のみを引用し、値・窓データ・測定量に触れていない |
| **7** | $14$ / $(Z_{28}$-link$)$ | 全て族供給 ✅ | **`not_assessed`**(inventory 行なし) | ✅(link 不要) | ⚠ migration 手続きが要る | `q7_lower_bound_v1.md` §7 の前件表と整合(窓パッケージは族供給・残るのは C1′/C5 と橋) |
| **9** | $18$ / $(Z_{36}$-link$)$ | 全て族供給 ✅ | **`not_assessed`** | ✅(link 不要) | ⚠ 同上 | `c2c4_closure_v1.md` §2.1 が「(5′) = $B_{\rm FC}$ の $n=9$ instance = C3 ⚠」と記帳しているのと同じ穴 |
| （参考）$A_5$ | $5$ / $(Z_{10}$-link$)$ | — | **pending** | — | — | **$K^{(n)}$ 族の窓ではない**(第二事例)。(5′) は個別構成済($A_5$ v4 §3.5) |

> ### ★ この表が示すこと
> 1. **窓前件の列は全 $n$ で同じ**(族供給)。**$n$ ごとに違うのは link inventory の列だけ**である。
> 2. ⟹ **Route T を採れば表は全行 ✅ になる**(未閉は §5.3 の 1 本のみ)。**Route E を採ると $n=3,7,9$ が止まる**($n=3$ は個別構成が救う)。
> 3. **$n=3$ と $A_5$ は「link が pending なのに (5′) が手に入っている」** — これは個別構成が link を迂回した実例であり、**link が (5′) の本質的必要条件ではないこと**の状況証拠である(証明ではない)。

---

## 8. 供給が立たない $n$ の fallback(委嘱 (iv))

Route T の proof ID が提示されず、かつ Route E の inventory も埋まらない $n$ について。

| # | fallback | 内容 | コスト | 得られる格 |
|---|---|---|---|---|
| **FB-1** | **個別構成** | $K^{(3)}$(week4 §2.3(b))・$A_5$(v4 §3.5)の実績と同様に、その窓で (5′) を明示モデル+cusp+局所展開から直接構成する | **per-n・重**(モデル認識証明書 (R-1)(R-2) が要る — BFC v2 §12.2) | その $n$ で `paper-proof(framework-conditional)` |
| **FB-2** | **link migration** | Route E の seal 手続きを当該窓で実行 | per-n・中(手続き) | inventory 依存 |
| **FB-3** ★ | **条件文のまま止める** | (M-a)@$n$ を**供給しない**。定理 APPLY-fam の前件が満たされないので**結論を出さない** | ゼロ | ★ **UNKNOWN** |

> ### ★ FB-3 の scope(**最重要・誤読防止**)
> 1. **(M-a) 未供給は「非全射」を意味しない。** 【MATCH-one】が満たされないとき、`s3_family_completion_v1.md` §15 の軸($S\subseteq P$)により **全射も非全射も結論できない**。**両方向とも UNKNOWN** である。
> 2. これは便 103 **F103-5** の「(d1) は…依存が満たされなければ **UNKNOWN に止める**」と同じ規律である。
> 3. **UNKNOWN は一級の結果**(工房の宇宙事前登録規律)。$n$ ごとに「立った/立たない」を表に書き、**立たない $n$ を黙って除外しない**。
> 4. ⚠ **domain の書き換えではない**。有効 domain は奇数 $n\ge3$(裁定 396/398)のままで、変わるのは**その $n$ で結論が出るか**だけである(W95-1.2 が確立した「紙の証明の広さ ≠ 登録主張の広さ」の規律と同型)。

---

## 9. FINDING

| # | 格 | 内容 |
|---|---|---|
| **MOS-1** | ★★ **会計の組み替え** | **(M-a) の族供給の律速は per-window ではない。** 要求側が twisted 形で足りる(系 B-8)ため、律速は **「B-6$^{\rm tw}$ の link-free proof ID」1 本**に集約する。⟹ **$O(\#n)$ の seal 手続きを $O(1)$ の証明仕事に替えられる**(替え終わってはいない) |
| **MOS-2** | ★★ **最小十分集合** | **$\{\alpha=1\}$・全奇数 $n$ で同一ラベル**。BRIDGE-one の「ある一つ」は $n$ ごとの探索を要しない — 窓前件が $\alpha$ 一様(§4)だから |
| **MOS-3** | ★ **要求と供給の型の分離** | (M-a) が要るのは (5′$^b$)($\exists$ 単元 $b$・$\gamma$ 非依存)。**exact $\varepsilon=1$ は要求側に現れない。** これは BFC v2 §12.1 の「(TB4$^{\rm u}$)+系 B-8 で単一窓の結論はもう出る」の【MATCH-one】への適用である |
| **MOS-4** | ⚠ **便 103 の会計上の穴(要確認)** | F103-4 は (5′) を `theorem-framework-relative [TB: canonical-source-pinned/v2]` としたが、**$(Z_{2M}$-link$)$ の per-window 行に言及がない**。TB 引用束が扱ったのは TB1/TB3/TB4$^{\rm u}$ の文献 pin であり、**link は別系統の前件**である。**格が上がったときに link 行が黙って落ちていないか**を確認する必要がある(★教材: 「札の昇格で前件が 1 行消える」型) |
| **MOS-5** | ★ **状況証拠** | $K^{(3)}$ と $A_5$ は **link が `pending` のまま (5′) を個別構成で得ている**。link が (5′) の本質的必要条件でないことの状況証拠(証明ではない) |
| **MOS-6** | ⚠ **登録と数学の乖離(既在の再確認)** | (W4) は **ODD-H 補題 G が全 $(j,\alpha,\beta)$ で証明済**だが、**登録主張(HF-1)は $\alpha=1$ 限定**(falsifier F-3)。本稿は $\alpha=1$ を採るので影響を受けないが、**【ASM-α】を閉じたと読んではならない** |
| **MOS-7** | ★ **fitting 禁止との整合** | twisted 形の採用は $b$ の fitting ではない — **結論が $b$ に依らない**から(§2.2)。ただし **「$\gamma$ に依らない単一の $b$」**という一様性は要求文に明記が要る |

## 10. 【GAP】(隠さず明示・埋めていない)

| 札 | 内容 | 重み |
|---|---|---|
| **【MOS-GAP-1】** | ★★ **B-6$^{\rm tw}$ の link-free proof ID が未提示**(BFC v2【v2.7・F7】の自認)。**本稿は提示していない** — 私は $\bar t_M$ の定義に必要な Rule-1 側 root object が「窓ごとに存在を要するか」を判定できていない。**これが Route T の唯一の未閉点** | **重**(ただし 1 本) |
| **【MOS-GAP-2】** | **(5′) 自体の格は TB 相対**(便 103 F103-4・`canonical-source-pinned/v2`)。**`canonical-source-relative` でも `verified` でもない。** 本稿の供給はすべてこの格を継承する | 中(不変) |
| **【MOS-GAP-3】** | **(W2) は candidate**(裁定 120/122)。窓非依存だが (M-a) の前件に入る | 中 |
| **【MOS-GAP-4】** | **$n=5$ の operative 状態は receipt 依存**。本稿は receipt の現況を確認していない(現況の正本は `provenance/CLAIMS.md`・receipt) | 軽(手続き) |
| **【MOS-GAP-5】** | 本稿は**単系統・Sol 未監査**。§2 の再導出以外に**新しい数学はない**(§9 の FINDING はすべて既在部品の会計) | — |

**「verified」「cross-checked」は本稿で一度も使っていない。**

## 11. Sol への申し送り(監査点 4・優先順)

1. ★★ **便 103 F103-4 の格と $(Z_{2M}$-link$)$ の関係(最重要)**: (5′) を `theorem-framework-relative [TB: canonical-source-pinned/v2]` としたとき、**per-window の $(Z_{2M}$-link$)$ は前件として残るのか、それとも discharge されたのか**。TB 引用束は TB1/TB3/TB4$^{\rm u}$ の文献 pin であって link は別系統に見える。**残るなら、その旨を (5′) の札に明記する必要がある**(そうでないと $K^{(3)}$/$A_5$ の pending 行が会計から消える)。
2. ★★ **要求側の縮約の可否(§2)**: 【MATCH-one】の (M-a) は **(5′$^b$)($\exists$ 単元 $b$・$\gamma$ 非依存)で足りる**、という読みでよいか。根拠は既在の **系 B-8** と $R^{\rm cyc}_{\rm formal}$ の証明 2・3・5 の twist 不感性。**これが通れば exact $\varepsilon=1$ と link は (M-a) の要求側から消える。**
3. ★ **最小十分集合の形(§5)**: 「各奇数 $n$ で $\alpha=1$ の単一窓」で BRIDGE-one の存在形が実現する、という整理でよいか。窓前件が $\alpha$ 一様である(§4 の表)という判断に見落としはないか — とくに **(W4) の登録主張が $\alpha=1$ 限定**であること(falsifier F-3)は、$\alpha=1$ を採る限り問題にならないという読みでよいか。
4. ★ **link-free proof ID の要件(§5.3・【MOS-GAP-1】)**: 「$\exists$ 単元 $b$」だけを結論とする B-6$^{\rm tw}$ の導出に、**Rule-1 側 root object の窓ごとの存在は要るか**。要らないなら proof ID は純粋に $\Lambda$ と $\mathrm{Fib}$ が共に $\mu_M$-torsor であることから出るはずで、**per-window 性は完全に消える**。要るなら Route T も per-window 性を持ち、§5 の結論は弱まる。**ここが本稿の唯一の未閉点である。**

## 12. 出所

| 節 | 主たる出所 |
|---|---|
| §1 | `s3_family_completion_v1.md` §11–§12(MATCH-one)/ week4 v3 §5.2.1 (7.3) / BFC v2 §9($B_{\rm FC}$ = 定理 B-7・(9.1)) |
| §2 | **BFC v2 §10 系 B-8**(逐語)/ week4 v3 §5.2.2 の証明 2・3・5 / BFC v2 §15.8(U5・fitting 禁止) |
| §3 | BFC v2 §13.1 前件表・**【v2.7・F7】link 要否の型列挙**・§0 の v2.6 E4 / v2.7 G2・G6 / v2.13 A61-1 / 便 61 F4 / §12.1 |
| §4 | ODD-H 補題 C(2)・補題 G・補題 H(1.3) / `w2fam_v1.md`(W2-fam) / `w2arith_v1.md` / Sol 便 73 (1.13)(1.14) / `s3_family_completion_v1.md` 定理 SIXP-fam / `c21_draft_v1.md` §4・§5.2(W1-fam) / `asm_alpha_falsifier_v1.md` F-1・F-3 |
| §6 | `znorm_apply_patches_v1.md` P-2(dictionary 条文・注 1/注 4) |
| §7 | BFC v2 §13.1(inventory 現況)・§9 状態札([pre-event candidate])/ week4 v3 §5.2.2 注(2 事例の個別構成)/ `c2c4_closure_v1.md` §2.1 / `q7_lower_bound_v1.md` §7 |
| §8 | 便 103 F103-5 / `s3_family_completion_v1.md` §15 / W95-1.2(登録主張の規律) |

### 12.1 【文献要請】

**本稿からの新規はゼロ。**【文献要請 13/14】(TB 層)は 便 103 F103-4 で部分消費されたが、**$(Z_{2M}$-link$)$ は文献要請の対象ではない**(工房の規約選択であって外部定理ではない)。⟹ 新しい要請は立てない。

### 12.2 司令塔への上申(3 点)

1. ★★ **Route T の proof ID を 1 本発注することを提案する**(【MOS-GAP-1】)。これが済めば **(M-a) の族供給が全奇数 $n$ で $\alpha=1$ の単一窓に確定**し、$n=7,9$ の `not_assessed` を埋める seal 手続きが**不要になる**。宛先は BFC 側(週 4 BFC 攻略の改版)であり、私が書くなら「$\bar t_M$ を追った B-6$^{\rm tw}$ の全文導出」という形になる — **委嘱があれば起草する**。
2. ★ **便 103 F103-4 の格に link 行が含まれるかの確定**(監査点 1)。これは会計の穴になりうるので、**Sol への次便で明示的に問う**ことを提案する。
3. ★ **$n=3$ の扱い**: (5′)@$K^{(3)}$ は個別構成済なので、**Route の如何にかかわらず (M-a)@3 は供給されている**。族の議論とは別に、**$n=3$ を「供給済の較正点」として表に固定**されたい(§7)。
