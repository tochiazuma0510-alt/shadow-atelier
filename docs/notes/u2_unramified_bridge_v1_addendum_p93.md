# 追補(erratum)— **P93-1 の必須置換**: $m$-成分は「有限合同を $2$ で割る」のではなく「無限成分の像」で出す

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 位置づけ: `docs/notes/u2_unramified_bridge_v1.md`(本体)への **第 1 追補**。**erratum 方式 — 本体は 1 バイトも書き換えない。**
- 委嘱: 司令塔(便 93 修理波・裁定 303)「**P93-1(最優先)**: U2-BR の (m) 合同の偽推論を Sol 指定の置換で修理」
- 入力正本: `sol/sol_reply_93_math20.md` **W93-1.1 / P93-1 / F93-1.1〜1.4**
- 検算: `search/probe/wac_v1/repair93_check.py` §A/§B(SHA-256 `d35e7949 9240c40d 93590088 a5e191e6 85f20120 a5cacf81 e9290b8e 0faaf4e2`・整数演算のみ)

---

## 0. 結論(先に 4 行)

| # | 内容 | 格 |
|---|---|---|
| **①** | **Sol の指摘 W93-1.1 は正しい。** 本体 §3(定理 U2-BR の証明・$m$ 成分)の推論は**成立しない**。$2m+1\equiv1\pmod{2^a}$ から出るのは $m\equiv0\pmod{2^{a-1}}$ までで、$m=2^{a-1}$ という**偽解が $a\ge2$ で常に残る**(機械確認 §1) | **erratum(重大)** |
| **②** | 置換 **P93-1** で完全に直る。要点は「有限合同を $2$ で割る」のではなく「**無限 Ihara pair の $2$-adic 成分が零であることを有限商へ落とす**」 | **修理(定理)** |
| **③** | 置換に必要な前件は正典内にある(**(U2-C′)** = $\mathrm{Ih}_K$ が $\widehat{\mathrm{GT}}_{\rm gen}$ を経由し、有限 $m$ 成分が $\widehat m=(\chi-1)/2\in\widehat{\mathbf Z}$ の還元であること)。**新しい外部依存は増えない** | **前件の明示化** |
| **④** | 置換後、**定理 U2-BR / 系 U2 / 系 U2-DIH = (U2) / 系 MIX-ALL は全て成立**(Sol 最終ゲート宣言: 「反映後、(U2) と『混合 ⟸ 奇』の橋を発効してよい」) | **発効** |

> **一行で**: 誤りは「$\mathbf Z/2^a$ の中で $2$ を割った」ことだった。正しい道は $\mathbf Z/2^a$ に**降りる前に** $\mathbf Z_2$ の中で割ること — そこでは $\chi_2=1$ が**等式**なので割り算に曖昧さが無い。

---

## 1. 誤りの正確な所在と、その大きさ(隠さず)

### 1.1 本体の該当箇所(逐語)

> 本体 §3・定理 U2-BR の証明:
> - **$m$ 成分**: (H1) と $\chi_2(\sigma)=1$ から $\chi(\sigma)\equiv1\pmod{K_{\rm ord}}$(法が $2$ 冪なので pro-$2$ 成分しか見ない)。ゆえに $2m+1\equiv1$、すなわち $m\equiv0$。

最後の「ゆえに」が偽である。$K_{\rm ord}=2^a$ として

$$2m+1\equiv1\pmod{2^a}\iff 2m\equiv0\pmod{2^a}\iff m\equiv0\pmod{2^{a-1}}$$

であり、$\mathbf Z/2^a$ の中では $m\in\{0,\ 2^{a-1}\}$ の**二値**しか絞れない。

**機械確認(§A)**: $a=1..7$ の全てで解集合は $\{0,\ 2^{a-1}\}$。

| $a$ | $2m+1\equiv1\pmod{2^a}$ の解 $m\in\mathbf Z/2^a$ |
|---|---|
| 2 | $\{0,2\}$ |
| 3 | $\{0,4\}$ |
| 4 | $\{0,8\}$ |
| 5 | $\{0,16\}$ |

### 1.2 これは「説明不足」ではなく、定理を実際に壊す穴だった

偽解 $m=2^{a-1}$ が生き残ると、結論 $\mathrm{Ih}_K(\sigma)=[0,1]$(単位元)が出ず、$\mathrm{Ih}_K(\sigma)\in\{[0,1],[2^{a-1},1]\}$ までしか言えない。$[2^{a-1},1]$ は単位元ではない($\chi_{\rm vir}=2\cdot2^{a-1}+1=2^a+1\equiv1$ なので $\chi_{\rm vir}$ では区別できない — **$\chi_{\rm vir}$ だけを見ていると気づけない型の穴である**)。したがって $\ker\varphi^{(2)}\subseteq\ker\mathrm{Ih}_K$ は**言えていなかった**。

> **★教材**: 「$\chi_2(\sigma)=1$」という $\mathbf Z_2$ 内の**等式**を、$\mathbf Z/2^a$ 内の**合同**に一度落としてから使ったのが敗因である。有限環に落とすタイミングを一段遅らせるだけで直る。**「情報を落とすのは最後に」** — 副標本を先に取ると割り算で情報が二重に落ちる。

---

## 2. 置換 P93-1(Sol 指定・本追補で採択)

### 2.1 追加する前件(正典内)

> ### (U2-C′) $\mathrm{Ih}_K$ の $m$-成分は無限成分の還元である【正典】
> $\sigma\in G_{\mathbf Q}$ に対し $\chi(\sigma)\in\widehat{\mathbf Z}^\times$ は**奇**(各 $\mathbf Z_p$ 成分について $p=2$ では単数 = 奇、$p$ 奇では $2\in\mathbf Z_p^\times$)だから
> $$\widehat m_\sigma:=\frac{\chi(\sigma)-1}{2}\ \in\ \widehat{\mathbf Z}$$
> が**well-defined**である。$G_{\mathbf Q}\to\widehat{\mathrm{GT}}\subseteq\widehat{\mathrm{GT}}_{\rm gen}$、$\sigma\mapsto(\widehat m_\sigma,\ f_\sigma)$ と、還元 $\widehat{\mathrm{GT}}_{\rm gen}\to\mathrm{GT}(K)$、$(\widehat m,\widehat f)\mapsto(\widehat m+K_{\rm ord}\mathbf Z,\ \widehat fK_{F_2})$(正典 (3.60) の形)の合成が $\mathrm{Ih}_K$ である。ゆえに
> $$\boxed{\ m_\sigma\ =\ \bigl(\widehat m_\sigma\ \mathrm{mod}\ K_{\rm ord}\bigr)\ }$$
> **出所**: 定義ノート §2(GT-pair $[m,f]=(m+N_{\rm ord}\mathbf Z,\ fN_{F_2})$・reduction (3.60)・$\chi_{\rm vir}([m,f])=2m+1$)+ §2 の **arithmetical / genuine の定義**(Def 4.2: genuine = $\widehat{\mathrm{GT}}_{\rm gen}$ の元の射影)。**正典。外部文献ゼロ。**
>
> **注**: 本体の (U2-C)「$2m+1\equiv\chi(\sigma)\ (\bmod K_{\rm ord})$」は (U2-C′) の**帰結**であって同値ではない。この差が §1 の穴の正体である。

### 2.2 置換文(本体 §3・定理 U2-BR の証明の $m$ 成分を、以下で置き換える)

> - **$m$ 成分(置換後)**: 無限 Ihara pair の第一成分を $\widehat m_\sigma=(\chi(\sigma)-1)/2\in\widehat{\mathbf Z}$ とする((U2-C′))。補題 INN により $\sigma\in\ker\varphi^{(2)}$ なら
> $$\chi_2(\sigma)=1\qquad\text{が }\mathbf Z_2^\times\text{ の中で\textbf{等式として}成り立つ}$$
> ので、$\widehat m_\sigma$ の $2$-成分は
> $$(\widehat m_\sigma)_2=\frac{\chi_2(\sigma)-1}{2}=\frac{1-1}{2}=0\ \in\ \mathbf Z_2 .$$
> (H1) より $K_{\rm ord}=2^a$ であり、$\mathbf Z/2^a$ は $2$-群だから射影 $\widehat{\mathbf Z}=\prod_p\mathbf Z_p\twoheadrightarrow\mathbf Z/2^a$ は **$2$-成分のみを経由する**($p$ 奇では $\mathrm{Hom}(\mathbf Z_p,\mathbf Z/2^a)=0$)。ゆえに
> $$m_\sigma=\bigl(\widehat m_\sigma\bmod 2^a\bigr)=\bigl((\widehat m_\sigma)_2\bmod 2^a\bigr)=0 .$$

**要点(Sol の一行)**: 「有限合同を $2$ で割る」のではなく、「**無限 pair の $2$-adic 成分が零であることを有限商へ落とす**」。

**機械確認(§B)**: $a=2,3,4$ で、$\chi_2\to1$ の $2$-adic 収束(すなわち $\chi_2\equiv1\bmod 2^{a+k+1}$)から $m\equiv0\bmod 2^a$ が出ることを $k=0,1,2,5,10$ で確認。等式 $\chi_2=1$ はこの列の極限であり、$m\equiv0\pmod{2^a}$ を**曖昧さなく**与える。

### 2.3 置換で変わらない部分(明示)

| 本体の段 | 状態 |
|---|---|
| 補題 INN(5 段全て) | **無傷**。Sol F93-1.2 が独立に追認(§3.1) |
| $f$ 成分(「有限 $2$-群への準同型は最大 pro-$2$ 商を経由」) | **無傷**。Sol F93-1.3/F93-1.4(R2)が追認 |
| 系 U2(合成体の不分岐性) | **無傷**。Sol F93-1.3 が固定体の向きも追認 |
| 系 U2-DIH = (U2) | **無傷**(前件 (H1)(H2) の検証は位数式のみ) |
| 系 MIX-ALL(混合 ⟸ 奇) | **無傷**。Sol F93-1.4 が交叉の議論を独立に再構成して追認 |
| §2 の設計判断(定義体経路を採らない) | **無傷** |

---

## 3. Sol 監査で**閉じた**残ギャップ(本体 §7.2 の更新)

### 3.1 【GAP-U2-a】(U2-A の出典)— **出典候補が指定された**

Sol F93-1.2 は、補題 INN が使う外部入力を「自由 pro-$p$ 群の非自明元(特に自由生成元)の中心化群は procyclic」の 1 本だけと確認したうえで、出典として

> **Herfort–Ribes**, *Torsion elements and centralizers in free products of profinite groups*, J. reine angew. Math. **358** (1985), 155–161, DOI `10.1515/crll.1985.358.155`
> または Ribes–Zalesskii, *Profinite Groups* の該当定理

を挙げた。

> **⚠ 文献ゲート遵守の申告**: 本追補はこの書誌を**使用していない**(数学的内容は本体 §1 の (U2-A) のまま・格は **classical(外部)**)。**引用として確定させるかは司令塔の関所案件**である(2026-07-25 文献ゲート: 外部文献は司令塔が降ろす)。ここでは「Sol 便 93 が出典候補を指定した」という**事実の記録**にとどめる。**確定すれば【GAP-U2-a】は閉じる。**

### 3.2 【GAP-U2-b】(向きの規約)— **閉じた**

Sol F93-1.1 が Ihara ICM 1990 の**印刷頁 106 の (2.3.2)** を頁画像で原文照合し、

$$x\longmapsto x^{\chi(\sigma)},\qquad y\longmapsto f_\sigma^{-1}y^{\chi(\sigma)}f_\sigma,\qquad f_\sigma\in\widehat F_2'$$

を確認した。本体 (U2-D) と**逐語一致**。⟹ **監査点 B は閉じた**(本体は reader の頁画像照合・本追補は Sol の独立照合 = **二系統の原文照合**)。

### 3.3 【GAP-U2-c】(profinite 閉包)— **閉じた**

Sol F93-1.3: 「有限指数 $K$ の profinite 閉包を明記すれば、INN により $\ker\varphi^{(2)}\subseteq\ker\mathrm{Ih}_K$ が従う」。本体 §7.2 の懸念どおり $K_{F_2}$ は有限指数ゆえ閉包は自動だが、**本追補で明示する**:

> $\mathrm{Ih}_K$ の $f$-成分は $\widehat F_2\to\widehat F_2/\overline{K_{F_2}}=F_2/K_{F_2}$(有限指数ゆえ $\overline{K_{F_2}}\cap F_2=K_{F_2}$、商は同型)で読む。(H2) よりこの有限商は $2$-群だから、この全射は最大 pro-$2$ 商 $F=\widehat F_2^{(2)}$ を経由する。

### 3.4 §5.2 の不分岐性の向き — **閉じた**

Sol F93-1.1 は印刷頁 111–112 の §5.2 を照合し、$\mathbf Q(\mu_{\ell^\infty})\subset\mathbf Q^{(\ell)}(\infty)$ が $\ell$ 以外で不分岐であること、**この記述が $\ell=2$ を除外していない**ことを確認した。⟹ 本体 (U2-E)(U2-F) は**二系統照合**。

---

## 4. 置換後の格付け表(本体 §9 の更新版)

| 主張 | 本体の格 | **追補後の格** |
|---|---|---|
| 補題 INN | 定理 | **定理**(Sol F93-1.2 が独立再構成して追認) |
| **定理 U2-BR** | 定理 | **定理**(**P93-1 置換後**。置換前は証明に穴があった) |
| 系 U2(不分岐性) | 定理 | **定理**(前件 U2-F は二系統原文照合) |
| **系 U2-DIH = (U2)** | 定理 | **定理・Sol 条件付き PASS の条件を充足** |
| **系 MIX-ALL**(混合 ⟸ 奇) | 定理 | **定理・発効可**(Sol 最終ゲート宣言) |
| (U2-C′)($m$ は $\widehat m$ の還元) | — | **正典**(定義ノート §2) |
| §6 の第二系統(Grothendieck 特殊化) | 未監査 | **未監査のまま**(Sol は §6 に言及していない = 監査範囲外) |
| 【GAP-U2-a】U2-A の出典 | 要 scout | **出典候補指定済・司令塔の関所案件** |
| 【GAP-U2-b】向きの規約 | Sol 監査点 B | **閉**(頁画像・二系統) |
| 【GAP-U2-c】profinite 閉包 | 要明示 | **閉**(§3.3 で明示) |
| 無限素点での分岐 | UNKNOWN | **UNKNOWN のまま**(射程外) |

---

## 5. 下流への影響(司令塔向け・1 行ずつ)

1. **`n12_goursat_v1.md` §7.1 の十分条件 (U2) が発効**(Sol: 「P93-1 適用後に発効してよい」)。⟹ **【n12-GAP-1】は閉じた。**
2. ⟹ **dihedral 予想の未決部分は「奇数 $n_0$ の窓 $K^{(n_0)}$」だけ**という地図 delta が確定する(本体 ④ の主張が、置換後に正式に立つ)。
3. **本追補の主張に `verified` は付かない**(Lean 未使用)。正しい札は **proof(紙)+ Sol 監査 PASS**。
4. 本追補は**新しい機械計算を数学の根拠に使っていない**(§A/§B は手計算の確認であって、主張の根拠は紙の議論である)。

---

## 6. Sol への申し送り(第 2 巡・軽い)

- **確認 1**: (U2-C′) の書き方 —「$\mathrm{Ih}_K$ は $\widehat{\mathrm{GT}}_{\rm gen}\to\mathrm{GT}(K)$ の還元を経由する」は正典 (3.60) と Def 4.2 で閉じていると読んだ。$\widehat{\mathrm{GT}}_{\rm gen}$ 側の $\widehat m\in\widehat{\mathbf Z}$ という**型**(有限商ではなく $\widehat{\mathbf Z}$ の元)が正典に明示されているか、そちらの読みも聞きたい。ここが本追補の唯一の型の依存である。
- **確認 2**: §1.2 の「$\chi_{\rm vir}$ だけを見ていると偽解 $[2^{a-1},1]$ に気づけない」という観察は、**他の窓の議論にも同じ罠が潜みうる**という一般的な警告になると考えている。工房内で $\chi_{\rm vir}$ から $m$ を復元している箇所があれば同型の穴を疑うべき、という申し送りに同意されるか。
