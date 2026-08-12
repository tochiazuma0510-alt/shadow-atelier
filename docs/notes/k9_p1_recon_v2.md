# 【K9-P1-RECON】v2 — ★ **判定 = 同一対象(肯定)**。$d_9$ は $\operatorname{ord}(a_9)$ そのもの

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 904 → **裁定 908 で最優先へ格上げ**
**格**: candidate(紙・単系統・**Sol 未監査**)。三値判定は CV-9 精神に従う。
**前版**: `k9_p1_recon_v1.md` = ★ **本版が supersede**(v1 の「別対象」判定は**誤り** — §0 で自己申告)
**判読対象**: `docs/notes/E1_gt_odd_dih_canonical_v1.md` §5.1(**(S1)–(S4) + 定理 $R^{\rm cyc}_{\rm formal}$**)/ `fam_u_assembly_v1.md`(P1)/ R1 第一波 `r1_k9_bridge_v1.md`

> ## ★★★ 判定(三値)
> $$\boxed{\ \textbf{同一対象}\ }$$
> $d_9$(私の R1)$=\lvert A\cap\mathfrak F_0\rvert$(E1 の (S4))であり、**(S3) $\iff d_9=9$**、**$R^{\rm cyc}_{\rm formal}$ により $\iff\operatorname{ord}(a_9)=9$**。
> ⟹ **$R2$ は公開問題の抽象受けから、$\operatorname{ord}(a_9)$ の測定 1 本へ還元される。**
> ⚠ ただし **前件 (0)(1)(2)(3)(5′)(6′) の $n=9$ での検証は未了**(§4)— **これが残る唯一の仕事**。

---

## §0 ★ 自己申告 — v1 の判定は誤りだった

| | v1 の判定 | 原因 | v2 |
|---|---|---|---|
| (2) $d_9\leftrightarrow\operatorname{ord}([u_9^{-1}]_{18})$ | ✘ **別対象**(「橋 (c-n) は循環」) | ★ **stale な文書を読んだ**: `fam_u_assembly_v1.md` は **v1(2026-08-01)+ v2 追記**で、その §V.5.1 は **P1 発効(裁定 550・2026-08-05)以前**の距離の図。**私は発効を確認せずに「未証明」と読んだ** | ★ **同一対象** |

**一次確認**(裁定 908 の指示で実施): `provenance/LEDGER.md` 2303「**FAM-U-ASM 昇格の発効を宣言**」/ 2337「**★P1 発効 = Sol 異議なし・PASS 追認**(F106-1.1・6 条件履行確認)」。⟹ **P1 は発効済**。
⚠ **私の手続き上の過ち**: 判読対象の**鮮度を一次台帳で確認せずに**「未証明」と断じた。文書内の版注記(「v1 §3/§4/§7 を単独で引用しないこと」)を読みながら、**発効の有無そのものを台帳で確かめなかった**。⟹ 台帳採番は司令塔の裁量に委ねる(本セッション内で司令塔へ流通した判定であるため、**隠さず申告する**)。

---

## §1 ★★★ 完全対応表 — E1 の (S1)–(S4) は私の R1 第一波と**同一の機械**

$n=9$、$T:=GT(K^{(9)})$、$A:=\mathrm{Ih}_{K^{(9)}}(G_\mathbf Q)$、$K:=\mathbf Q(\zeta_{4n})=\mathbf Q(\zeta_{36})$。

| E1 §5.1(既存・裁定 120/122) | 私の R1 第一波(正典から独立再導出) | 判定 |
|---|---|---|
| **(S1)** $1\to\mathfrak F_0(\cong C_n)\to T\xrightarrow{\tilde\chi_{2M}}(\mathbf Z/4n)^\times\to1$ | **K9-COORD**: $\Theta_9:T\xrightarrow{\sim}\mathrm{Aff}(\mathbf Z/9)\times C_2=\mathbf Z/9\rtimes(\mathbf Z/36)^\times$ | ★ **同一**($\mathfrak F_0=\mathbf Z/9$ の translation・商 $=(\mathbf Z/36)^\times$、**$4n=36$** ✔) |
| **(S2)** $\tilde\chi_{2M}\circ\mathrm{Ih}=\chi_{4n}$ ⟹ $\tilde\chi(A)=(\mathbf Z/4n)^\times$ | **K9-CYC**: $u(g)=\chi(g)\bmod36$、$\chi$ 全射ゆえ unit 成分は全射 | ★★ **同一**。私は **2405 (1.3)(1.5)(1.11)(1.13)** から独立に導出した ⟹ **二系統一致** |
| **(S4)** $\lvert A\rvert=\lvert A\cap\mathfrak F_0\rvert\cdot\lvert\tilde\chi(A)\rvert=n\cdot2\varphi(n)=\lvert T\rvert$ | **K9-CYC(b)**: $\lvert A_9\rvert=12\,d_9$、$\lvert T\rvert=108=9\cdot12$ | ★ **同一**($2\varphi(9)=12$ ✔・$9\cdot12=108$ ✔) |
| **(S3)** $\mathrm{Ih}_{K^{(n)}}(G_K)=\mathfrak F_0$ | ★ $d_9:=\lvert A_9\cap\mathbf Z/9\rvert=9$ | ★★★ **同一**($G_K=\ker(\chi\bmod36)$ 上の像が translation 全体) |
| $K=\mathbf Q(\zeta_{4n})=\mathbf Q(\zeta_{36})$ | **K9-CYCLO-DICHOTOMY**: $d_9=1\iff L_9=\mathbf Q(\zeta_{36})$ | ★ **同一の体** |
| **$R^{\rm cyc}_{\rm formal}$**: $\mathrm{Ih}$ 全射 $\iff\operatorname{ord}(a_n)=n$ | **K9-CYC(b)**: $\mathrm{Ih}$ 全射 $\iff d_9=9$ | ★★ **同一の同値** |

$$\boxed{\ \Longrightarrow\ d_9\ =\ \lvert A\cap\mathfrak F_0\rvert\ =\ \operatorname{ord}(a_9),\qquad a_9:=[u_9^{-1}]_{18}\in F_9^\times/F_9^{\times18},\ F_9=\mathbf Q(\zeta_{36})\ }$$

★ **司令塔の提案した同一視 $d_9\leftrightarrow\operatorname{ord}([u_9^{-1}]_{18})$ は、E1 §5.1 の $a_n$ の定義そのもの**であった。

### 1.1 ★ 二系統一致の意味(格の申告)

私の K9-COORD / K9-CYC / K9-CYC(b) は **2405 の Prop 3.4・Prop 4.5 (4.15)・(4.18)・Thm 4.6・(1.3)(1.5)(1.13) だけ**から導いた。E1 の (S1)(S2)(S4) は **w2fam_v1 / w2arith_v1**(裁定 120/122)から導かれている。
$$\boxed{\ \textbf{独立な二経路が同じ機械に到達 — 工房内の}\textbf{相互確認}\ }$$
⚠ **cross-checked ではない**(両者とも工房の紙)。★ ただし**私の側は正典内在**なので、E1 側の (S1)(S2)(S4) に**正典からの裏づけ**が付いた形。

---

## §2 ★ 測定路の全体像(**肯定判定の帰結**)

$$\underbrace{\operatorname{ord}([u_9]_{18})=9}_{\textbf{P1/FAM-U-ASM(発効済・framework-relative)}}\ \Longrightarrow\ \underbrace{\operatorname{ord}(a_9)=9}_{a_9=[u_9^{-1}]_{18},\ \operatorname{ord}(u^{-1})=\operatorname{ord}(u)}\ \overset{\textbf{前件 (0)(1)(2)(3)(5′)(6′)}}{\underset{R^{\rm cyc}_{\rm formal}}{\Longleftrightarrow}}\ \underbrace{\text{(S3)}}_{d_9=9}\ \overset{\textbf{K9-CYC(b)}}{\underset{\textbf{無条件}}{\Longleftrightarrow}}\ \mathrm{Ih}_{K^{(9)}}\ \textbf{全射}$$

⟹ **$d_9=9$ が framework-relative に従う**(前件が立てば)。⟹ **Conj 5.1@$n=9$ が framework-relative に閉じる**。

> ### ⚠⚠ 過大評価の三重の歯止め(**自戒として先に書く**)
> 1. **framework-relative**: P1 の格は `theorem-framework-relative [TB: canonical-source-pinned/v2]`。candidate 性の残余 = **W2-fam / W5 / Λ-REG / (M-b) / ASM-α / 始点算術**(裁定 908・便 106 erratum)。⟹ **無条件の定理ではない**。
> 2. ★ **前件 (0)(1)(2)(3)(5′)(6′) は $n=9$ で未検証**(§4)— **これが立たなければ矢印 2 が渡れない**。
> 3. **E1 自身の記述**: 「$n\ge9$: **未着手** / 族定理待ち($n=9$ のみ **T63-P1** が塔経路で下界を出す枝を持つ)」⟹ ★ **$n=9$ の枝は既知だが未着手**。本 RECON はその枝を**開けた**が、**通したわけではない**。
> $$\boxed{\ \textbf{現時点で言ってよいのは「}d_9\ \textbf{は測定問題へ還元された」まで。「}d_9=9\ \textbf{が示された」は}\textbf{禁止}\ }$$

---

## §3 ⚠★ 型境界の検問 — **Hol$(\mathbf Z/9)$ 測定は $\rho_9$ と同一か**(司令塔の警告への回答)

裁定 908 は「u 測定パイプライン M0→M7 の完走実績(裁定 821 = PΓL$(2,8)$・**Hol$(\mathbf Z/9)$** の飽和 candidate)が $\rho_9$ と同一対象かは未判読」と警告した。**私の回答**:

| 対象 | 型(TYPE-IMAGE$^\rho$) | 注意 |
|---|---|---|
| **Hol$(\mathbf Z/9)=\mathbf Z/9\rtimes(\mathbf Z/9)^\times=\mathrm{Aff}(\mathbf Z/9)$** | ★ **(1) marked target**(群の型) | $\Theta_9$ の Aff 因子と**同型**。⚠ **これは型の一致にすぎない** |
| $u_n$(P1/E1 の測定対象) | ★ **幾何模型 $W_n$ 側の Kummer データ**(窓の局所 torsor 類) | $F_n=\mathbf Q(\zeta_{4n})$ 上の類 |
| $d_9=\lvert A_9\cap\mathfrak F_0\rvert$ | ★ **(3) embedded image** | $\rho_9(G_\mathbf Q)$ の translation 部分 |

$$\boxed{\ \textbf{型の一致(Hol}(\mathbf Z/9)\cong\mathrm{Aff}(\mathbf Z/9)\textbf{)から算術像の主張へ渡ってはならない — これが }\textbf{B116-1}\ \textbf{の正体}\ }$$

★ **では何が渡るのか**: 渡すのは**型の同型ではなく $R^{\rm cyc}_{\rm formal}$ という定理**である。$R^{\rm cyc}_{\rm formal}$ は「窓側の Kummer 類の位数」と「算術像の (S3)」を**前件つきで**結ぶ。
$$\boxed{\ \textbf{橋は }R^{\rm cyc}_{\rm formal}\ \textbf{ただ一本。その前件 (0)(1)(2)(3)(5′)(6′) が}\textbf{型境界の関所}\ \textbf{である}\ }$$
⟹ ★ **$u_9=3$ の撤回はそのまま**(あれは前件を検証せずに型から算術へ渡った)。**本 RECON は撤回を復活させない** — 復活させるのは前件検証だけである。

---

## §4 ★ 残る唯一の仕事 — 前件 (0)(1)(2)(3)(5′)(6′) の $n=9$ 検証

### 4.0 ★★★ M-0 完了 — 前件は **C1 と C3 の二つ**に絞れた

`docs/notes/c2c4_closure_v1.md` が $n=9$ の前件を**既に個別札に分解済**であった(私の判読で発見)。逐語:

| 前件 | $n=9$ での供給元 | 状態 |
|---|---|---|
| $e=\lvert\mathfrak F_0\rvert=9$ | 正典(便 29 (6.1)) | ✔(**要転記確認**と原文が注記) |
| **(6′) の像の等式** $\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$ + 忠実性 | **命題 K5-1**($\Phi_{0,k}=\mathrm{inn}(X^{-2k})$・W3-15①) | ★ **全奇 $n$ で自動** |
| $\mathrm{Ih}_N(G_K)\subseteq\mathfrak F_0$ | (W2) の完全列 + $\tilde\chi\circ\mathrm{Ih}=\chi_{2M}$ | ⚠ **(W2) = C3** |
| **(5′)** $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(\kappa_{u^{-1}}(\gamma))$ | **$B_{\rm FC}$ の $n=9$ instance** | ⚠ **= C3** |
| **C2**((W1) の $n=9$ 供給) | (CAL)(既証明)のみ | ★ **閉鎖済**(しかも全奇 $n\ge3$ で一斉) |
| **G3** | 便 75 F3.2 | ★ **PAPER-PROOF 済** |

同文書 §2.3 の整理(逐語): 「残る条件は **C1**((6.3) の下段窓が $H^{\rm fun}$ か)・**C2**(本メモで閉鎖)・**C3**・**G3**(PAPER-PROOF 済)に整理される」「⚠ **C1 は依然として最優先**」。

$$\boxed{\ \Longrightarrow\ \textbf{前件検証の実体は }\textbf{C1 と C3 の二枚だけ}\ \textbf{(C2/G3 は閉・(6′) と }e\ \textbf{は自動)}\ }$$

> ### ★ さらに上界と下界が分離している(**c2c4 §2.4**)
> - **上界 $\operatorname{ord}(a_9)\mid9$ = C4**: Route 1(補題 R 段 3)は **C3 依存**/ **Route 2 は (6.3) から無償**(ただし **C1 を相続**)。
>   ★ **等価な言い換え**(同文書 §2.2・私が検算): $F_9=\mathbf Q(\zeta_{36})$、$\mu_9\subset F_9^{\times2}$($\zeta_9=\zeta_{36}^4=(\zeta_{36}^2)^2$)より $$\operatorname{ord}(a_9)\mid9\iff u_9\in F_9^{\times2}.$$
> - **下界 $\operatorname{ord}(a_9)\ne$ 真の約数**: ★ **T63-P1(塔経路)が別途扱う**(c2c4 §2.3 が明記)。⟹ E1 の「$n=9$ のみ T63-P1 が塔経路で**下界**を出す枝を持つ」と**一致** ✔
> ⟹ ★ **P1/FAM-U-ASM の $\operatorname{ord}([u_n]_{2n})=n$ は上下両方**を与えるので、**C1/C3 が立てば P1 が下界装置(【E1-GAP-6】)を埋める**構図。

### 4.0.1 ⚠ 私が**まだ確認していないこと**(honest)

- **C1 と C3 の現在の状態**(閉/開)を地図・台帳で**確認できていない** — `docs/地図.md` の grep が空振り。⟹ ★ **C1/C3 が既に閉じているなら測定路は即座に通る。開いているならそこが残件。**司令塔の在庫確認を請う。
- 前件 **(0)(1)(2)(3)** の逐語(上表は (5′)(6′) と付随条件のみ)。

**旧記述**: 前件の**内容そのもの**を私はまだ読めていない(E1 §5.1 は「台帳 W3-13・裁定 24」を参照するのみで、本文に列挙が無い)。⟹ ★ **上記 4.0 で (5′)(6′) 側は解消**。

### 4.1 測定計画(**前件検証込み**・着手は裁定待ち)

| 段 | 内容 | 費用 | kill 条件 |
|---|---|---|---|
| **M-0** | ★ **前件 (0)(1)(2)(3)(5′)(6′) の逐語取得**(台帳 W3-13 / 裁定 24 / 便 29 (6.1) を当たる)。**これが無ければ以降は全て空論** | 小(内部文書) | 前件が $n=9$ で**構造的に破れる**(例: coprime regime $\gcd(e,M/e)=\gcd(9,2)=1$ ✔ なので**ここは通る見込み**) |
| **M-1** | 各前件を $n=9$ で**個別に検証**(型を明記: 窓側 / 算術側 / 枠組み) | 中 | いずれかが $n=9$ 固有の理由で破れる |
| **M-2** | P1 の結論 $\operatorname{ord}([u_9]_{18})=9$ の**domain 適合確認**(奇 $n\ge3$・$n\ne5$ ⟹ $n=9$ ✔)と**枠組み依存の棚卸し**(W2-fam/W5/Λ-REG/(M-b)/ASM-α/始点算術) | 小 | domain 外・枠組み仮定が $n=9$ で追加要求を生む |
| **M-3** | ★ **独立検算**: $\operatorname{ord}(a_9)$ を $F_9=\mathbf Q(\zeta_{36})$ 上で**直接**計算(既存 M0→M7 パイプラインの Hol$(\mathbf Z/9)$ 実績を**窓側の測定として**再利用 — ⚠ **算術像として読まない**) | 中(実装係) | 測定値が $9$ でない ⟹ ★ **Conj 5.1@$n=9$ の反例候補**(QUAR 検疫必須) |
| **M-4** | 結論の格付け: `theorem-framework-relative` を継承。**verified とは呼ばない** | 小 | — |

### 4.2 ★ 私の見立て(**未検証・candidate**)

- **coprime regime は通る**: $M=2n=18$、$e=n=9$、$\gcd(e,M/e)=\gcd(9,2)=1$ ✔(便 29 (6.1) の regime 条件)。$n=3$ の成功例と**同じ regime**。
- **$n=3$ の先例**: $u_3=-4$、$\operatorname{ord}([-4]_6)=3=e$ ✓ で **定理 K3 = Conj 5.1@$n=3$ が閉じている**。⟹ **$n=9$ は $n=3$ と同じ路である**(族が $n=3$ で一度通っている = **既知答えテストの母型がある**)。
- ⚠ **ただし $n=9$ は素数冪で $n=3$ の「塔」の上にある** — E1 が「$n=9$ のみ T63-P1 が**塔経路**で下界を出す枝を持つ」と書いたのはこの構造。**塔経路特有の前件**があり得る。

---

## §5 帰属・依存申告

- **(S1)–(S4) の標準機械・$R^{\rm cyc}_{\rm formal}$・$a_n:=[u_n^{-1}]_M$ の定義** = `E1_gt_odd_dih_canonical_v1.md` §5.1(台帳 W3-13・裁定 24・120/122)。
- **P1/FAM-U-ASM の発効** = 裁定 550(発効宣言)+ 便 106 F106-1.1(Sol PASS 追認)。**私が LEDGER で一次確認**。
- **訂正の起点** = 研究者 → 司令塔(裁定 908)。**v1 の誤りの直接原因は私の鮮度未確認**(§0)。
- **本ノートの新規部分**: ① **完全対応表**(E1 (S1)(S2)(S3)(S4) ↔ K9-COORD/K9-CYC/K9-CYC(b) の同一対象判定・正典内在の裏づけ)② **測定路の全体像**(4 本の矢印と各々の格)③ **型境界の検問**(Hol$(\mathbf Z/9)$ の型一致から算術へ渡らない・橋は $R^{\rm cyc}_{\rm formal}$ 一本・前件が関所)④ **測定計画 M-0〜M-4** ⑤ **coprime regime と $n=3$ 先例の指摘**。
- **未実施**: 前件 (0)(1)(2)(3)(5′)(6′) の逐語取得・$n=9$ 検証・独立測定。**Sol 未監査**。⟹ **verified ではない**。
