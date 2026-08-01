# 【W2-1】(W2) の算術側 — $\widetilde\chi_{2M}\circ\mathrm{Ih}_{K^{(n)}}=\chi_{4n}$ **v1**

2026-07-28: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱(裁定 120・C3 の最終数学残件)。
**状態札**: `candidate / 単系統・未監査`。**commit していない。**
**依拠**: 正典(2405.11725 p.4 と (1.5) — `docs/week4-A5算術飽和_v4.md` §1.4.1 の reader ページ画像照合済表・`docs/notes/抽出_Kn定義_D1.md` §3 (3.4)・`docs/week1-定義ノート.md`)+ `docs/notes/w2fam_v1.md`(**第二数学者・群論側**)+ `docs/notes/c2c4_closure_v1.md`(W1-fam)+ TB4 導出 v2.5 §4.2。**外部文献なし。$u$・封印量に触れていない。**

**位置づけ**: `w2fam_v1.md` §6【W2-1】が「本稿の射程外・C3 の残りはここ」と名指しした項目。**本稿は群論側を再証明しない**(命題 (W2)-fam をそのまま使う)。

---

## 0. 判定

$$ \boxed{\ \textbf{閉鎖(全奇数 }n\ge3\textbf{)。しかも二経路で、Route B は正典の水準に依存しない。}\ } $$

| Route | 前提 | 水準 $4n$ が出るか |
|---|---|---|
| **A**(正典引用) | 2405 (1.5) + 命題 (W2)-fam の $\widetilde\chi_{2M}$ | **出る**(§2) |
| **B**(内在的) | **(CAL)** + (TB2) の分裂 + **(TB4$^{\rm u}$)** | **出る**(§3)。**正典の $\chi_{\rm vir}$ が粗い水準でも影響しない** |

---

## 1. 水準の勘定(**罠の所在**)

$n\ge3$ 奇。$M:=\mathrm{ord}(X)=2n$(HF-1(b))、$K^{(n)}_{\rm ord}=\mathrm{lcm}(n,2)=2n=M$(D1 §3 (3.4) p.14)、$2M=4n$、$K=F_n=\mathbb Q(\zeta_{4n})$。

> **補題 L(水準の持ち上げ).** 写像 $m\mapsto2m+1$ は
> $$ \mathbb Z/M\ \xrightarrow{\ \sim\ }\ \{\text{奇剰余}\}\subset\mathbb Z/2M $$
> の**全単射**であり、$\mathcal X_n=\{m:\gcd(2m+1,2n)=1\}$ を $(\mathbb Z/4n)^\times$ の上へ移す。
> **証明.** $2m+1\equiv2m'+1\ (4n)\iff2(m-m')\equiv0\ (4n)\iff m\equiv m'\ (2n)$ ✓ 単射。奇剰余は $\bmod\ 4n$ に $2n$ 個で $\lvert\mathbb Z/2n\rvert$ と一致 ✓ 全単射。$2m+1$ は奇だから $\gcd(2m+1,4n)=1\iff\gcd(2m+1,n)=1\iff\gcd(2m+1,2n)=1$ ✓。∎

$$ \boxed{\ \textbf{$m$ が }\bmod\ M=2n\ \textbf{で分かれば }2m+1\ \textbf{は }\bmod\ 2M=4n\ \textbf{で確定する — 情報は失われない。}\ } $$

> **⚠ 罠の正体**($\bmod\ 2n\ne\bmod\ 4n$・`w2fam_v1.md` §4 と同旨): $\ker\bigl((\mathbb Z/4n)^\times\to(\mathbb Z/2n)^\times\bigr)$ は**位数 2**($\varphi(4n)/\varphi(2n)=2\varphi(n)/\varphi(n)=2$;$n=3,5,9$ で実測 2)。これが **chirality $\mathcal Z_2$**。したがって「$\bmod\ 2n$ での一致」は (W2) が要求する等式より**真に弱い**。
> **⚠ 正典の $\chi_{\rm vir}$ は粗い方である**(`w2fam_v1.md` §1 の警告): 正典が $\chi_{\rm vir}([m,f])=2m+1\bmod N_{\rm ord}$ と書く量は水準 $M=2n$。**誤りではないが (W2) の $\widetilde\chi_{2M}$ ではない。** 本稿が示すのは、**その粗さは $\chi_{\rm vir}$ の書き方の粗さであって、$\mathrm{Ih}$ が運ぶ情報の粗さではない**ということである。

---

## 2. Route A — 正典引用

> **2405.11725 p.4(reader ページ画像照合済・`A_5` v4 §1.4.1 の表)**
> 無番号式: $g(x)=x^{\chi(g)},\qquad g(y)=f_g^{-1}y^{\chi(g)}f_g$
> **(1.5)**: $\ \mathrm{Ih}(g)=\bigl(\tfrac{\chi(g)-1}{2},\ f_g\bigr)$
> **(1.6)**: 群準同型 $G_{\mathbb Q}\to\widehat{GT}_{\rm gen}$

ここで $\chi:G_{\mathbb Q}\to\hat{\mathbb Z}^\times$ は**完全な**円分指標。$\chi(g)\in\hat{\mathbb Z}^\times$ は $2$ 進成分が単元ゆえ奇で、$\tfrac{\chi(g)-1}{2}\in\hat{\mathbb Z}$ は well-defined。

> ### 命題 W2A(算術側)
> 全奇数 $n\ge3$ と全 $\gamma\in G_{\mathbb Q}$ について
> $$ \boxed{\ \widetilde\chi_{2M}\bigl(\mathrm{Ih}_{K^{(n)}}(\gamma)\bigr)\ =\ \chi(\gamma)\bmod4n\ =\ \chi_{4n}(\gamma)\ } $$

**証明.** $m_\gamma:=\tfrac{\chi(\gamma)-1}{2}\in\hat{\mathbb Z}$ と置くと $\hat{\mathbb Z}$ の中で $2m_\gamma+1=\chi(\gamma)$。$K^{(n)}$ での shadow は $m_\gamma$ を $\mathbb Z/K^{(n)}_{\rm ord}=\mathbb Z/2n$ へ還元した $\bar m_\gamma$ を第一成分にもつ。命題 (W2)-fam の $\widetilde\chi_{2M}([m,f])=2m+1\bmod4n$ を適用すると、$\bar m_\gamma=m_\gamma+2n t$($t\in\hat{\mathbb Z}$)の任意の代表に対し
$$ 2\bar m_\gamma+1=2m_\gamma+1+4nt\ \equiv\ 2m_\gamma+1=\chi(\gamma)\pmod{4n}. $$
**還元の曖昧さ $2n$ がちょうど倍されて $4n$ に吸収される**(補題 L)。∎

---

## 3. Route B — 内在的(**正典の水準に依存しない**)

**Route A は「正典の $m$ 成分が $\tfrac{\chi-1}{2}$ である」という定義的言明に乗っている。** 正典側の水準表記($\chi_{\rm vir}$ が粗い)への懸念を断つため、**$\widehat{GT}$ の $m$ 成分を工房側の量から直接同定する**経路を置く。

> ### 補題 W2B(慣性の Tate 捻れ)
> **(TB2) の分裂**(**$G_{\mathbb Q}$ は $\Omega$ に係数のみで作用し全 $\beta^{1/k}$ を固定**)の下で、$\sigma_\zeta\in I_0=\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))$ について
> $$ \gamma\,\sigma_\zeta\,\gamma^{-1}=\sigma_\zeta^{\,\chi(\gamma)}\qquad(\forall\gamma\in G_{\mathbb Q}). $$
> **証明.** $\gamma^{-1}$ は $\beta^{1/k}$ を固定するので
> $\gamma\sigma_\zeta\gamma^{-1}(\beta^{1/k})=\gamma(\zeta_k\beta^{1/k})=\gamma(\zeta_k)\beta^{1/k}=\zeta_k^{\chi(\gamma)}\beta^{1/k}$。全 $k$ で成立。∎(TB4 導出 v2.5 §4.2 と同じ計算)

> ### 系 W2B′
> **(TB4$^{\rm u}$)** の下で $x=\iota(\sigma_\zeta^{\,\varepsilon})$($\varepsilon\in\hat{\mathbb Z}^\times$)と書くと
> $$ \alpha^{\rm std}_\gamma(x)=\iota\bigl(\gamma\sigma_\zeta^{\,\varepsilon}\gamma^{-1}\bigr)=\iota\bigl(\sigma_\zeta^{\,\varepsilon\chi(\gamma)}\bigr)=x^{\chi(\gamma)} . $$
> **$\varepsilon$ は $\hat{\mathbb Z}^\times$ の可換性で相殺する — exact (TB4) は要らず (TB4$^{\rm u}$) で足りる。**

> ### 命題 W2B″(Route B)
> **(CAL)**($\alpha^{\rm Ih}=\alpha^{\rm std}$・$A_5$ v4 §1.4・窓非依存の既証明)の下で、$\mathrm{Ih}(\gamma)$ の $m$ 成分は $\hat{\mathbb Z}$ の中で
> $$ 2m_\gamma+1=\chi(\gamma) $$
> を満たす。ゆえに命題 W2A の結論が従う。

**証明.** $\widehat{GT}_{\rm gen}$ の元 $(m,f)$ が定める $\hat F_2$ の自己同型は $x\mapsto x^{2m+1}$。$\overline{\langle x\rangle}\cong\hat{\mathbb Z}$ で $x$ は無限位数だから、**$\alpha(x)=x^{\lambda}$ の指数 $\lambda\in\hat{\mathbb Z}^\times$ は $\hat{\mathbb Z}$ の中で一意に決まる**。(CAL) より $\alpha^{\rm Ih}_\gamma=\alpha^{\rm std}_\gamma$、系 W2B′ より $\lambda=\chi(\gamma)$。ゆえに $2m_\gamma+1=\chi(\gamma)$。あとは命題 W2A の証明と同じ($\bmod\ 2n$ 還元 $\to$ $\bmod\ 4n$)。∎

> **★ Route B の要点**: **指数 $\lambda$ は有限商 $P_n$ ではなく $\hat F_2$ で決まる。** $P_n$ の中では $X^{\lambda}$ は $\lambda\bmod\mathrm{ord}(X)=\lambda\bmod2n$ しか見えないので、そこから読むと **chirality $\mathcal Z_2$ が失われる**。$\hat F_2$ で読めば $\lambda\in\hat{\mathbb Z}^\times$ が丸ごと決まり、shadow が $m$ を $\bmod\ 2n$ で保持するので $2m+1$ が $\bmod\ 4n$ で決まる。
> $$ \boxed{\ \textbf{水準の罠は「どの群で指数を読むか」に還元される — }\hat F_2\ \textbf{で読めば罠は消える。}\ } $$

---

## 4. 数値照合(証明に依存しない事後確認)

整数演算のみ($\varphi$・$\gcd$・剰余)。

| $n$ | $M=2n$ | $2M=4n$ | $K_{\rm ord}=\mathrm{lcm}(n,2)$ | $\lvert\mathcal X_n\rvert$ | $\varphi(4n)$ | 一致 | $m\mapsto2m+1$ が $\bmod\,4n$ で単射 | $\lvert\mathrm{GT}\rvert=2n\varphi(n)$ | $\lvert\mathrm{GT}\rvert/\varphi(4n)$ |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 6 | 12 | 6 $=M$ ✓ | 4 | 4 | ✓ | ✓ | 12 | **3** $=e$ ✓ |
| 5 | 10 | 20 | 10 ✓ | 8 | 8 | ✓ | ✓ | 40 | **5** ✓ |
| 7 | 14 | 28 | 14 ✓ | 12 | 12 | ✓ | ✓ | 84 | **7** ✓ |
| **9** | **18** | **36** | 18 ✓ | 12 | 12 | ✓ | ✓ | **108** | **9** ✓ |
| 11 | 22 | 44 | 22 ✓ | 20 | 20 | ✓ | ✓ | 220 | **11** ✓ |
| 15 | 30 | 60 | 30 ✓ | 16 | 16 | ✓ | ✓ | 240 | **15** ✓ |

- **$n=9$ の $\lvert\mathrm{GT}\rvert=108$ は便 75 F2 の実測値と一致**($2n\varphi(n)=2\cdot9\cdot6=108$)。$108/\varphi(36)=108/12=9=e$ ✓ — **完全列 (W2-fam) の位数勘定が $n=9$ で機械的に閉じている。**
- $\ker\bigl((\mathbb Z/4n)^\times\to(\mathbb Z/2n)^\times\bigr)$ の位数は $n=3,5,9$ で **2**(chirality $\mathcal Z_2$ の実在確認)。

---

## 5. 判定と残件

$$ \boxed{\ \textbf{【W2-1】は閉鎖。}\ \widetilde\chi_{2M}\circ\mathrm{Ih}_{K^{(n)}}=\chi_{4n}\ \textbf{が全奇数 }n\ge3\ \textbf{で成立(paper-proof candidate)。}\ } $$

**⇒ 命題 (W2)-fam(群論側・第二数学者)と合わせて (W2) が全奇数 $n\ge3$ で閉じる。$n=9$ instance は自動。**

| 前提 | 状態 |
|---|---|
| 命題 (W2)-fam($\widetilde\chi_{2M}$ の well-defined・準同型・全射・核 $=\mathfrak F_0\cong C_n$) | `w2fam_v1.md`(paper-proof candidate・**独立監査待ち**) |
| **(CAL)** $\alpha^{\rm Ih}=\alpha^{\rm std}$ | $A_5$ v4 §1.4・**窓非依存の既証明** |
| **(TB2)** の分裂・**(TB4$^{\rm u}$)** | framework(【GAP-TB】)— **exact (TB4) は不要** |
| $K^{(n)}_{\rm ord}=\mathrm{lcm}(n,2)$ | D1 §3 (3.4) p.14【画像照合済】 |
| 2405 (1.5)(Route A のみ) | reader 照合済。**Route B は不要とする** |
| $M=\mathrm{ord}(X)=2n$ | HF-1(b)(証明済) |

**残件**:
- **【W2A-1】** 本稿は $[m,f]$ の**第一成分のみ**を扱う。$f_\gamma$ 側(charming 条件・$\varkappa$ の形)は正典引用のままで、再証明していない(`w2fam_v1.md`【W2-2】と同じ扱い)。
- **【W2A-2】** $n$ 偶数は**射程外**($K_{\rm ord}=n$ となり水準が変わる;`w2fam_v1.md`【W2-3】と同じ)。
- **【W2A-3】** paper-proof candidate。**Lean `verified` ではない。**
- **【W2A-4】** Route B は **(CAL)** に全面依存する。(CAL) が破れると Route A(正典引用)だけが残り、そのとき正典の $m$ 成分の水準表記を改めて検分する必要が生じる。**(CAL) は既証明なので現状は問題ない**が、依存として明記する。

**⇒ C3 の inventory 更新**(`c2c4_closure_v1.md` §3 に対して):

| # | 項目 | 更新後 |
|---|---|---|
| **I6** | (W2) | **閉**(群論側 = `w2fam_v1.md` / 算術側 = 本稿)。ただし両方とも **paper-proof candidate・独立監査待ち** |
| I7 | $\mathfrak F_0\cong C_n$・$e=n$ | **閉**((W2)-fam の核の同定に含まれる) |
| I8 | (5′) の $n=9$ instance | **OPEN(本体)** |
| I9 | $(Z_{36}$-link$)$+inventory 行 | **OPEN**(手続き) |
| I10 | (E-iv) 命名規約 | **OPEN**(条項起草) |

$$ \boxed{\ \textbf{C3 の数学的残件は I8((5′) 本体)ただ一つに縮んだ。I9 は手続き・I10 は条項。}\ } $$

---

# 追記 A(便 99 検収・裁定 412)— **Route A = 暫定正本**の確定と依存表の補完

> **追記型**: §0–§5 の本文を**一切改変しない**。以下は**格の確定**と**依存の明記**である。
> 起草: 数学者(Opus 5)・2026-08-02。入力 = **Sol 便 99 返信 F99-3.2**(`sol/sol_reply_99_math26.md` §3.2)。

## A.1 裁定(Sol F99-3.2)

**Route A を暫定正本として PASS。** 正典の式 $m=(\widetilde\chi-1)/2$ と W2-fam の $\widetilde\chi$ を合わせれば、必要な $\bmod\ 4n$ の主張は直接出る。**TB / 算術実現枠組みを必要としない。**

| Route | ★ 確定した格 |
|---|---|
| **Route A**(§2・正典引用) | ★ **暫定正本**。`paper-proof candidate / canonical-source-relative / framework-independent` |
| **Route B**(§3・内在的) | **同じ結論への framework-conditional な冗長経路**。**(CAL) + (TB2) の分裂 + (TB4$^{\rm u}$)** に依存する |
| 補題 CHI とその **系 DIV-SPLIT** への投入 | ★ **Route A を使う**(`div_law_v1.md` §3・§4.5) |
| Lean | ✗ **verified ではない** |

> ### ⚠ §0 の判定表の読み方の訂正(erratum ではなく**読み違いの予防**)
> §0 は Route B を「正典の水準に依存しない」と書いた。**これは正しい**(正典の $\chi_{\rm vir}$ の粗さに影響されない、という意味)。しかし **framework(TB 系)には依存する**ので、「Route B の方が強い/安全」と読んではならない。**枠組み非依存なのは Route A の方である。**
> 二経路の関係の正しい要約:
> $$\boxed{\ \textbf{Route A} = \textbf{正典に相対だが枠組み非依存}\qquad\textbf{Route B} = \textbf{正典の水準に非依存だが枠組み条件つき}\ }$$

## A.2 依存表の補完 — **Kronecker–Weber 入力の明記**(Sol の要求)

本稿および下流(補題 CHI・系 DIV-CHI-NULL・系 DIV-SPLIT)は、$\widetilde\chi$ の**全射性**を使う箇所で次の標準外部定理を入力にしている。**依存表に明記する。**

| 入力 | 正確な言明(本稿が使う形) | 格 |
|---|---|---|
| **(KW)** 円分指標の全射性 | $\chi_{4n}:G_{\mathbb Q}\to(\mathbb Z/4n)^\times$ は**全射**。同値に $\mathrm{Gal}(\mathbb Q(\zeta_{4n})/\mathbb Q)\cong(\mathbb Z/4n)^\times$(円分多項式 $\Phi_{4n}$ の $\mathbb Q$ 上の既約性) | ★ **標準外部定理**(Sol は「Kronecker–Weber 入力」と呼んだ)。**自前再導出も Lean 化もしない**(【framework assumptions policy】と同じ扱い: Mathlib 待ち)。⚠ **Mathlib に円分多項式の既約性・円分拡大のガロア群があるかは当方未確認**(記憶に基づく見込みでしかない)— Lean 化の日に**公理化が要るか不要か**は、実装係が実物で確認すること |

**使用箇所**: 命題 W2A の結論を「$\widetilde\chi(\mathrm{GT}_{\rm arith})=(\mathbb Z/4n)^\times$(全像)」として使う下流 — すなわち **補題 CHI**(`div_law_v1.md` §3)・**系 DIV-CHI-NULL**・**系 DIV-SPLIT**・`kerchi_equality_v2.md` T-A(4′)。**本稿 §2 の命題 W2A 自身は等式 $\widetilde\chi_{2M}\circ\mathrm{Ih}=\chi_{4n}$ を示すだけで (KW) を要さない** — (KW) が要るのは「その像が全体」を言う段である。この分離を明記する。

## A.3 ihnec §6.4 との整合(記帳の食い違いの解消)

`docs/notes/ihnec_v1.md` §6.4 は (S2) を **framework-conditional** と記帳し、本稿 §0 は「閉鎖・二経路」と記帳していた(`div_law_v1.md` §9 申し送り 1 が裁定を請うた食い違い)。**裁定 = Route A 採用**により:

| 文書 | 訂正後の読み |
|---|---|
| **ihnec §6.4**(本文不改変) | 「(S2) は framework-conditional」は **Route B のみを見た記帳**であった。**Route A の存在により (S2) 自体は framework-independent** である。ihnec 本文は erratum 方式で不改変とし、**本追記を effective source** とする |
| **`div_law_v1.md` §10.1 の補題 CHI 行**「格の食い違いあり(§9-1)」 | ★ **解消**(同日の `div_law_v1.md` 追記 A §A.3) |
| **本稿 §5 の前提表** | 「2405 (1.5)(Route A のみ)」行は **正本入力**へ格上げ。「(TB2) の分裂・(TB4$^{\rm u}$)」行は **Route B 専用の依存**へ限定 |

## A.4 残件(不変)

【W2A-1】(第一成分のみ)・【W2A-2】($n$ 偶は射程外)・【W2A-3】(Lean 未)・【W2A-4】(Route B は (CAL) に全面依存)は**すべて不変**。加えて:

- **【W2A-5】(新設・記帳のみ)**: (KW) は外部定理として使う。**自前証明も Lean 化もしない**方針(framework assumptions policy と同型の扱い)。使用箇所は §A.2 のとおり。

