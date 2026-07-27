# (TB4) の自前導出 — 枠組条件 $\varepsilon=1$ の解消 **v2(便 48 Part B 修理反映版)**

2026-07-27 起草(v1)・**2026-07-28 v2**: Claude(数学者レイヤー・Opus 5・**第二インスタンス**)。司令塔委嘱「(TB4) の自前導出」。研究者 GO 済み。
**v2 は `sol/sol_reply_48_tb4_v24.md` Part B(F4–F13)の監査を反映**(司令塔指示 1–8 / Sol F14 項 5–7+α)。**解析計算(補題 TB4-2)は開け直していない** — 便 48 F6 が「解析持ち上げは正しい」と判定した部分は不変である。

**独立性の申告(v1 から不変)**: 本稿の起草者は $B_{\rm FC}$ 攻略 v2 の著者とは別インスタンスであり、その下書き・作業メモ・`docs/week4-BFC攻略_opus_v1.md` には一切接していない。**外部文献検索は一切行っていない。** `docs/文献ゲート_04_tangential_inertia.md`・`docs/scout/scout_20260727_tangential_inertia.md`・`docs/notes/覚書_ihara15代替.md` は、同主題と知りつつ**意図的に開いていない**。v2 で新たに読んだのは `sol/sol_reply_48_tb4_v24.md`(監査回答)のみ。

---

## v1 → v2 差分一覧

| # | 箇所 | v1 | v2 | 出所 |
|---|---|---|---|---|
| **V1** | §0-2・§3.2・§5.1 | 「**既存三文書だけで** $\varepsilon\equiv1\ (20)$」 | **FAIL を自認・撤回。** (TB2) の根系 $\zeta_{20}^{\rm TB2}$ と Rule 1 の体生成元 $\zeta_{20}^{\rm Rule1}$ を同一視する条項は正典にない。**(Z20-link) を normative clause として前件に立てる**(§1.2)。**Sol の countermodel($t\equiv3\ (20)$ で $\varepsilon\equiv7$・$b=3$)を独立再現し本文に採録**(§3.4) | 便 48 **F7.2 blocker B1** |
| **V2** | §3 | 定理 TB4-A 一本 | **三段分割**: **TB4-3**(比較式 (\*))/ **TB4-A20**(有限正規化・$\varepsilon\equiv1\ (20)$)/ **TB4-B**(全正規化・$\varepsilon=1$)。**finite と profinite を別札に**($K^{(5)}$ 運用は $\varepsilon\bmod10$ で足りるので、profinite 側の版事故が finite 結論を巻き込まない) | 便 48 F7.3・**F13.2** |
| **V3** | §1.1 補題 TB4-C | 「(C2) は (C1) から**従う**」 | **題名を撤回。** 左作用式は forward transport を**定義しない**。正しくは **C1 + forward path transport(A3)+ 関手性 $\Rightarrow$ right-to-left concatenation**。依存表 **A8 の「A4 から導出・独立仮定ではない」を撤回**し「**A3 または $A_5$ v4 補題 C に依存**」へ | 便 48 **F5** |
| **V4** | §2.3 補題 TB4-2 | 前件を「(C1)(C2)」とだけ書いた | 前件を **「C1, C5, chosen $\bar\iota$, radial comparison, A3」** と明記。「三本の工房規約だけ」という表現を撤回 | 便 48 **F6** |
| **V5** | §8.1 | (TB2-norm) を 1 行の追加案として提示 | **4 条の atomic seal 化**((i) $\bar\iota\supseteq\iota_\infty$ (ii) $\zeta_n^{\rm TB2}:=\bar\iota^{-1}(e^{2\pi i/n})$ (iii) **とくに $\zeta_{20}^{\rm TB2}=\zeta_{20}^{\rm Rule1}$** (iv) 全 TB4 比較は同一の $\bar\iota$・同一の根系)。**A3 は (Z-norm) が証明しない別の framework seal** として分離掲示 | 便 48 **F8** |
| **V6** | §6 反実仮想表 | (C1)(C2)(C5)(C4)(C7) の 5 経路 | **3 経路を追加**: **(C3) 反転**(前合成・右作用)/ **A3 反転**(比較の向き)/ **root-object ずれ**($t\in(\mathbb Z/20)^\times$ 任意 — $\pm1$ に限らない)。**「反転経路をすべて列挙した」という主張を撤回** | 便 48 **F9** |
| **V7** | §8.4 | 「$b_i\ne1$ は**必ず実装事故**」 | **強すぎるので修文。** TB4 は A1–A3 の framework-conditional な紙上定理なので、診断候補に**紙上前件・証明の誤り**も入る。**integrity quarantine** の 4 段監査順序へ | 便 48 **F10.2** |
| **V8** | §8.3 | 文献要請 13(ii) を「取り下げ可」 | **全面取下げでなく縮小維持**:「正の位相 transport が algebraic fiber functor の**後合成左作用**へ送られ**逆作用でない**ことの標準比較定理・記法確認」 | 便 48 **F10.3** |
| **V9** | §8.6 新設 | — | **`TB4-comparison-seal/v1`** を提案節に組込(8 フィールド・Rule 1 / BFC / 結果 record の三者が digest 参照) | 便 48 **F13.1** |
| **V10** | §1 規約表 | 単一の「$\varepsilon$ への影響」欄 | **二欄に強化**:「**対の整合の相手**」+「**両者を運ぶ比較写像 / equality の artifact ID**」。**(C4) を「凍結済」から「型不足」へ降格**し、**(C4′)=(Z20-link) を新設** | 便 48 **F4・F12 T2** |
| **V11** | §4.3 悉皆表 | $(\zeta_n)$ の使用箇所のみ | **「同じ字形の object identity」欄を追加**(v1 の悉皆表はこの型を持っていなかった) | 便 48 F8 |
| **V12** | §8.7 新設 | — | **TB4 の成立を理由に amendment の二段コミット・$b_i$ 記録・I-n を削ってはならない**ことを明記 | 便 48 **F11** |
| **V13** | §7 検算 | 15/15 | **25/25**(検査 4 = root-object countermodel の整数演算による独立再現・**$b\equiv t\ (10)$ の一般形**を新たに得た) | 本便 |

> **v2 でも不変(便 48 が PASS と判定した部分)**: **補題 TB4-1**(後合成の計算)・**補題 TB4-2 の解析持ち上げ**($w_j(t)=\bar\iota(\zeta_n)^j\delta^{1/n}e^{2\pi it/n}$ の一意性と終点)・**補題 TB4-0**(標識の平行移動は巡回 torsor の作用を変えない)・**比較式 (\*)**・**$\varepsilon=\chi_{\rm cyc}(\vartheta)$ の一般式**・**(Z-norm) 追加下の TB4-B**・**§6 の符号敏感性**・**★教材 T1/T2**(便 48 F12 が両方採用)。修理は**前件の型付け・定理の分割・条文の精密化**であり、解析計算は 1 ミリも動かない。

---

## 用いた正典

| 文書 | 使った箇所 |
|---|---|
| `docs/week4-BFC攻略_opus_v2.md` | §2 (TB1)–(TB4)/(TB4$^{\rm u}$)・(2.1)(2.2)・§6.3 系 B-4c・§7 補題 B-5・§8 補題 B-6・§8.1・§10.1・§12.1 |
| `docs/week4-K5_Rule1_v1.md` | §1.1(向き・(1.1))・§1.2・§1.3(左作用)・§1.4 (1.5)–(1.7)・§7.1・§7.4 |
| `docs/manifest_k5_appendixA_v1.md` | §1.1/§1.2 の作用規約、§2 の K3 行「$\tau$ の向き」 |
| `docs/week1-定義ノート.md` §1.5.1 **規約 W-1** | paper 規約(左作用)の凍結文。CLAUDE.md「定義の正本」による |
| `docs/week4-A5算術飽和_v4.md` §1.4.2 **補題 C**(+§1.4.3b 補題 D・§1.4.4 系 E) | 実区間解析接続の方法・forward transport の使用形。**委嘱は補題 C の所在を `manifest_k5_appendixA_v1.md` と書いたが誤り**(★教材 T4・速達で報告済) |
| `sol/sol_reply_48_tb4_v24.md` Part B(F4–F13) | **v2 の監査入力** |

---

## 0. 判定(先に 9 行)

1. **(TB4) は文献関所ではない。** それは「(TB2) の根系」と「Rule 1 §1.1 の向き規約」の**整合条件**であり、外部文献ではなく**工房自身が決める事項**である。**この主張は v2 でも維持する**(便 48 F8「(Z-norm) は新しい算術仮定ではなく、未指定だった比較データの選択」が同旨)。
2. **【v2・自認】ただし「既存の凍結文だけで $\varepsilon\equiv1\ (20)$」は誤りだった。** (TB2) の根系 $\zeta_{20}^{\rm TB2}$ と Rule 1 の体生成元 $\zeta_{20}^{\rm Rule1}$ は**同じ字形だが同じ object とは書かれていない**。両者を結ぶ typed equality **(Z20-link)** を前件に置かねばならない(§1.2・§3.4)。**便 48 F7.2 の blocker B1 をそのまま受け入れる。**
3. **修理後の到達点は三段である**:
 - **TB4-3**(比較式): A1–A3 + (C1)(C5) + chosen $\bar\iota$ $\Longrightarrow$ $\zeta_n^{\,\varepsilon}=\bar\iota^{-1}(e^{2\pi i/n})\ (\forall n)$。
 - **TB4-A20**(有限): $+$ **(Z20-link)** $+$ Rule 1 (1.6) $\Longrightarrow$ $\varepsilon\equiv1\ (\mathrm{mod}\ 20)$。**$M\mid20$ の窓($K^{(5)}$ の $M=10$ を含む)で $b=1$。**
 - **TB4-B**(profinite): $+$ **(Z-norm)** $\Longrightarrow$ $\varepsilon=1$ $=$ exact (TB4)。
4. **finite と profinite は別札にする**(便 48 F13.2 採用)。$K^{(5)}$ 運用に要るのは $\varepsilon\bmod10$ だけなので、profinite 側の版事故が finite 結論を巻き込まない設計にする。
5. **導出の型は「(TB4$^{\rm u}$) $+$ 工房規約 $+$ root seal $\Longrightarrow$ (TB4)」**。**(TB4) の向き感受的な root 選択は関所から外れる**が、**A3(位相 forward transport $\leftrightarrow$ 代数 後合成左作用)は framework seal として残る** — (Z-norm) は A3 を証明しない(便 48 F8)。
6. 符号は**本当に敏感**である。**8 本の反転経路**(v1 の 5 本 + v2 の 3 本)がそれぞれ独立に $b$ を動かす。とくに root-object ずれは $\pm1$ ではなく **$(\mathbb Z/20)^\times$ 全体**を生み、**$b\equiv t\ (\mathrm{mod}\ 10)$** という明示形をもつ(§6・検査 4)。
7. $\varepsilon$ は **接基点のスケールにも方向にも、窓・dessin・モデルにも依らない**(補題 TB4-0・便 48 F4 が C6/C11 を PASS)。
8. **UNKNOWN(一級の結果)**: (a) $n\nmid20$ の $\zeta_n^{\rm TB2}$、(b) $\bar\iota$ の $K$ 外への延長、(c) **$\zeta_{20}^{\rm TB2}$ と $\zeta_{20}^{\rm Rule1}$ の同一視** — 三つとも正典に凍結文がない(便 48 F4 が grep で確認)。**(c) が blocker B1 の正体であり、v1 はこれを暗黙に仮定していた。**
9. **本稿は Rule 1 §7.4 の測定規律も amendment の二段コミットも一切緩めない**(§8.4・§8.7)。**定理があることは、実装がその定理の規約を実現したことを保証しない。**

> **状態札(便 48 F10.1 に準拠)**
>
> | 主張 | 札 |
> |---|---|
> | TB4-1 | `paper-proof PASS`(便 48) |
> | TB4-2(解析持ち上げ) | `paper-proof / A3-framework-conditional PASS`(便 48) |
> | TB4-3 の比較式 (\*) | `paper-proof / framework-conditional PASS`(便 48) |
> | **TB4-A20**($\varepsilon\equiv1\ (20)$) | **`paper-proof / conditional on (Z20-link)`** — v2 新設・**未監査** |
> | **TB4-B**($\varepsilon=1$) | **`paper-proof / conditional on (Z-norm)`**(便 48「条件付き PASS」) |
> | 数値 checker | `25/25 sanity only`(証明の一部ではない) |
>
> **$B_{\rm FC}$ の状態札は、(Z20-link)/(Z-norm) が凍結されるまで更新しないこと**(便 48 F10.1「現時点ではまだ更新しない」)。

---

## 1. 規約の完全な一覧

**【v2・V10】二欄に強化した**(便 48 F12 T2):「対の整合の相手」だけでは、今回の $\zeta_{20}$ のように**同名 object が無言で同一視される**。「両者を運ぶ比較写像 / equality の artifact」欄を追加し、**比較写像の向き**まで記録することで A3/C3 の逆転も同じ表で検査できるようにする。

| # | 規約 | 内容 | 凍結文(逐語引用) | 出所の別 | **対の整合の相手** | **比較写像 / equality の artifact** |
|---|---|---|---|---|---|---|
| **(C1)** | 群作用と積の向き | $(AB)\cdot i = A\cdot(B\cdot i)$ | 定義ノート §1.5.1 規約 W-1:「**本工房の全数学文書**は **paper 規約**」「$\textbf{paper(左作用)}:\ (AB)\cdot i = A\cdot(B\cdot i)$」 | **凍結済**(定義の正本) | (C2)(A3) | path concatenation $\leftrightarrow$ 群積(**A3 が要る** — §1.1) |
| **(C2)** | 経路の輸送の向き | 経路は**自分の向き(forward)**に輸送し、**左**から作用 | $A_5$ v4 §1.4.2 補題 C:「$p$ を…標準経路(**$\vec{10}\to\vec{01}$**)」「**$p\cdot v_1=v_0$**」「$\sigma(p)=g_\sigma\cdot p$」「$y=p\,x_1\,p^{-1}$」 | **正典の証明が依存**(実質凍結)。**【v2】(C1) からは導出できない** | (C1)(A3) | 補題 C の 4 用例(§1.1) |
| **(C3)** | 代数側の作用 | $\Omega$ への**後合成 $=$ 左作用** | (TB4):「$\hat{\mathbb Z}(1)$ は $\Omega$ への**後合成(= 左作用)**で $\mathrm{Fib}_{\vec{01}}$ に作用する」/ BFC §6.3 | **凍結済**((TB4$^{\rm u}$) に含まれる) | (A3) | §2.2 の注(逆数は入らない) |
| **(C4)** | $K$ の複素埋め込み | $\iota_\infty(\zeta_{20}^{\rm Rule1})=e^{2\pi i/20}$ | Rule 1 (1.6):「$\zeta_{20}$ が $\Phi_{20}$ の根のうち $\operatorname{Im}>0$ かつ $\operatorname{Re}$ 最大のものに写るものとして固定する」「(1.6) は**一意**に $\zeta_{20}=e^{2\pi i/20}$ を指す」 | **【v2 で降格】型不足** — 凍結しているのは**体生成元 $\zeta_{20}^{\rm Rule1}=\bar T\in K$ の像**であって (TB2) の根系ではない | **(C4′)** | **欠品 $\to$ (Z20-link)** |
| **(C4′)** | **根 object の同一視** | $\zeta_{20}^{\rm TB2}=\zeta_{20}^{\rm Rule1}\in K\subset\bar{\mathbb Q}$ | **正典に条項なし** | **【v2 新設】UNKNOWN(未凍結)・(Z20-link) として提案** | (C4)(C7) | **(Z20-link)**(§1.2・§8.1(iii)) |
| **(C5)** | 向きの正 | 反時計回りが正。$x:=\gamma_0$ | Rule 1 §1.1:「$\mathbf C$ の**標準的向き**(反時計回りが正)を採る…$x:=\gamma_0$」「**この順序・この向きが正本**」/ §7.1:「**(1.6) の埋め込みの下で** $\lambda$ の周りを**反時計回り**に一周する $\gamma_0$」 | **凍結済** | (A3) | §2.3 補題 TB4-2 |
| **(C6)** | 接基点の解析的実現 | 標識は**正の実分枝**で与える | 補題 C (a)(b):「$\{\zeta_n^j\beta^{1/n}\}$」「$\beta\in(0,1)$ では…**正の実数値**をとる分枝($\beta^{1/n}>0$)」 | **正典の証明が依存**(便 48 F4: A3 条件付き PASS) | (C11) | 補題 TB4-0(標識の平行移動で不変) |
| **(C7)** | $n\nmid20$ の $\zeta_n^{\rm TB2}$ | (TB2) の系のうち $\iota_\infty$ が届かない部分 | (TB2):「整合的な $1$ の冪根系 $(\zeta_n)_n$…を**固定する**」— **具体値の指定なし** | **UNKNOWN**(便 48 F4 が grep で確認:「近道はない」) | (C8)(C4′) | **(Z-norm)**(§8.1(ii)) |
| **(C8)** | $\bar\iota:\bar{\mathbb Q}\hookrightarrow\mathbf C$ | $\bar\iota|_K=\iota_\infty$ | **明示の凍結文なし** | **UNKNOWN。【v2】前件に明示量化が要る**(便 48 F4/F7.1) | (C4)(C7) | **(Z-norm)**(§8.1(i)(iv)) |
| **(C9)** | 置換の合成 | $(\sigma\rho)(p):=\sigma(\rho(p))$ | Rule 1 §1.3 | 凍結済(非本質) | (C1) | — |
| **(C10)** | $\mathrm{Gal}(C_n/U)\cong\mathbb Z/n$ | Kummer 被覆のガロア群の同一視 | — | **任意**(本稿は使わない・§2.4) | — | — |
| **(C11)** | 接基点のスケール $c$・方向 | $\vec{01}$ の「速度」 | $A_5$ v4 系 E:「接基点のスケール $c$ は完全に消えた」 | 凍結不要 | (C6) | 補題 TB4-0 |
| **(A3)** | **位相–代数比較の向き** | 位相の forward transport $\leftrightarrow$ 代数の後合成左作用 | **正典に条項なし**(枠組み事実) | **framework seal(未凍結)。(Z-norm) は A3 を証明しない** | (C1)(C2)(C3)(C5) | **§8.2 の framework seal + 文献要請 13(ii)(縮小版)** |

> **⚠ 過剰読み取りの明示的排除(v1 から維持)**: Rule 1 (1.1) の関係式 $\gamma_0\gamma_1\gamma_\infty=1$ は**経路合成の向きを決めない**。条文は「…$\gamma_0\gamma_1\gamma_\infty=1$ **となるものとする**」であり、接続経路の**正規化**にすぎない(どちらの合成規約でも実現できる)。**本稿は (1.1) を合成規約の根拠として使っていない。** (C5) から使うのは「反時計回りが正」と「$x:=\gamma_0$」の 2 点だけである。

> **★【v2 で強化】この表の要点**: **単独では $\varepsilon$ を決めない規約が、対になると符号を決める。** そして **v1 の表が持っていなかったのが「(C4) と (C4′) の区別」である** — 凍結された $\zeta_{20}$ は $K$ の**体生成元**であり、(TB2) の**根系**ではない。**同じ glyph は同じ object ではない。**

### 1.1 【v2・V3】補題 TB4-C の修文 — 「(C2) は (C1) から従う」を撤回

> **⚠ v1 の誤り(自認・便 48 F5)**: v1 の補題 TB4-C は「(C2) は (C1) から**従う**」と題していた。**これは過大である。** 抽象的な左作用式 $(AB)\cdot i=A\cdot(B\cdot i)$ は**既に選ばれた群積に関する作用公理を言うだけ**で、**幾何経路を forward transport で読むか inverse transport で読むかを決めない** — 群積と path concatenation の対応を単独では生成しない。v1 の証明は仮定の中に「経路が自分の向きへ輸送する」を既に入れており、**それは (C2) の半分である**。

> **補題 TB4-C(修正版).**
> $$ \boxed{\ \text{(C1)}\ +\ \text{forward path transport(A3)}\ +\ \text{輸送の関手性}\ \Longrightarrow\ \text{right-to-left concatenation}\ } $$
> すなわち、**経路が自分の向きへ forward transport として左から作用すること**を認めれば、規約 W-1 は語 $AB$ に対応する経路を「**$B$ を先に、$A$ を後に**辿るもの」と一意に決める。

**証明.** $A,B$ を $\pi_1(U,\vec{01})$ のループ、$AB$ を表すループを $\gamma$ とする。輸送の関手性(1 本の道の輸送は分割した各区間の輸送の合成)により、$\gamma$ が「$B$ の後に $A$」なら $\gamma\cdot p=A\cdot(B\cdot p)$、「$A$ の後に $B$」なら $\gamma\cdot p=B\cdot(A\cdot p)$。(C1) は前者を要求する。$\pi_1=\mathrm{Aut}(\mathrm{Fib})$ は全繊維の族に忠実に作用するから、この等式は経路の同値類を決める。∎

**forward transport の独立証拠($A_5$ v4 補題 C の 4 用例)** — 便 48 F5 が「核心を捨てる必要はない」と認めた部分:
1. $y=p\,x_1\,p^{-1}$($x_1\in\pi_1(U,\vec{10})$、$p:\vec{10}\to\vec{01}$)。右から左に読めば $\vec{01}$ のループになる。**左から右では $x_1$ の基点が合わない。**
2. $g_\sigma:=\sigma(p)p^{-1}$。同じく右から左でのみ $\vec{01}$ のループ。
3. $\sigma(p)=g_\sigma\cdot p$。右から左で $\vec{10}\to\vec{01}$。**左から右だと $g_\sigma$ が $\vec{10}$ のループでなければならず矛盾。**
4. $p\cdot v_1=v_0$($v_1\in\mathrm{Fib}_{\vec{10}}$, $v_0\in\mathrm{Fib}_{\vec{01}}$)— **forward transport そのもの。**

⇒ **依存表の A8 は「A4 から導出・独立仮定ではない」を撤回し、「A3 または $A_5$ v4 補題 C に依存」とする**(§9)。

### 1.2 【v2・V1 新設】(Z20-link) — 根 object の typed equality

> **(Z20-link)(normative clause として前件に置く).**
> $$ \boxed{\ \zeta_{20}^{\rm TB2}\ =\ \zeta_{20}^{\rm Rule1}\ \in\ K\ \subset\ \bar{\mathbb Q}\ } $$
> ここで $\zeta_{20}^{\rm TB2}$ は (TB2) が固定する整合系 $(\zeta_n^{\rm TB2})_n$ の $n=20$ 項、$\zeta_{20}^{\rm Rule1}:=\bar T\in K=\mathbb Q[T]/(\Phi_{20})$ は Rule 1 (1.5) の**体生成元**である。

**なぜ条項が要るか**: (TB2) は「整合的な系を固定する」としか言わず、Rule 1 (1.6) は「体生成元 $\bar T$ の**複素像**」しか固定しない。**両者を結ぶ条項は正典のどこにもない**(便 48 F4 が grep で確認)。**同じ記号 $\zeta_{20}$ を二文書が使っていることは typed equality ではない。** §3.4 に、この条項なしで結論が壊れる具体的 countermodel を置く。

---

## 2. 有限レベルの補題 — 補題 C の方法を Kummer 塔へ延長する

記号は $B_{\rm FC}$ v2 §2 に従う: $U=\mathbf P^1_{\mathbb Q}\smallsetminus\{0,1,\infty\}$、座標 $\beta$、$\Omega=\bar{\mathbb Q}\{\{\beta\}\}$、$I_0:=\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))$、$\iota:I_0\to\pi_1(U_{\bar{\mathbb Q}},\vec{01})$ は後合成が定める準同型。**以後 $\zeta_n$ と書いたら (TB2) の系 $\zeta_n^{\rm TB2}$ を指す**(【v2】v1 はここを曖昧にしていた)。

$n\ge1$ に対し **Kummer 被覆** $C_n:\ w^n=\beta$(有限エタール・補題 C の表の 1 行目と同じ被覆)を取る。

### 2.1 繊維の明示

(TB1) の定義により
$$ \boxed{\ \mathrm{Fib}_{\vec{01}}(C_n)\ =\ \{\,\xi\,\beta^{1/n}\ :\ \xi\in\mu_n\,\}\ \subset\ \Omega\ } \tag{2.2} $$
($\bar{\mathbb Q}$-代数準同型は $w$ の行き先 $=T^n-\beta$ の $\Omega$ における根で決まる)。$\mu_n$-torsor である。標識を $\mathrm{lab}(\zeta_n^{\,j}\beta^{1/n}):=j\in\mathbb Z/n$ と定める。

### 2.2 ガロア側 —【便 48 F7.1: PASS】

> **補題 TB4-1(ガロア側の作用).** $\sigma\in I_0$ に対し
> $$ \iota(\sigma)\cdot\bigl(\xi\beta^{1/n}\bigr)\ =\ \chi_n(\sigma)\,\xi\,\beta^{1/n},\qquad \chi_n(\sigma):=\frac{\sigma(\beta^{1/n})}{\beta^{1/n}}\in\mu_n . $$
> とくに $\chi_n(\sigma_\zeta)=\zeta_n$、標識では $j\mapsto j+1$。**前件**: A1, A2。

**証明.** $f(w)=\xi\beta^{1/n}$ とすると $(\sigma\circ f)(w)=\sigma(\xi\beta^{1/n})=\xi\cdot\sigma(\beta^{1/n})$($\sigma$ は $\bar{\mathbb Q}$ 上恒等)$=\xi\chi_n(\sigma)\beta^{1/n}$。∎

> **注(後合成が準同型であること = (C3))**: $(\sigma\tau)\circ f=\sigma\circ(\tau\circ f)$ なので $\iota$ は (C1) の意味で**準同型**であり反準同型ではない。**ここに逆数は入らない。** ただし**これは代数側の内部の話であり、位相側との比較(A3)を代替しない**(【v2】便 48 F6)。

### 2.3 位相側 — 補題 C (b) の方法の延長 —【便 48 F6: A3 条件付き PASS】

**接基点の解析的実現(規約 (C6) の明示形).** $0<\delta<1$ を十分小さく取る。**$\bar\iota:\bar{\mathbb Q}\hookrightarrow\mathbf C$ を一つ選び前件に明記する**(【v2】(C8) の明示量化・便 48 F7.1)。
$$ c_\delta:\ \mathrm{Fib}_{\vec{01}}(C_n)\to C_n(\mathbf C)_\delta,\qquad \xi\beta^{1/n}\mapsto\bar\iota(\xi)\cdot\delta^{1/n}\quad(\delta^{1/n}>0) \tag{2.4} $$
これは $\mu_n$-同変な全単射(補題 C (a)(b) の同一視と逐語同じ)。

> **補題 TB4-0(接基点のスケール・方向は $\varepsilon$ に効かない).**【便 48 F4/F6: PASS】 (2.4) の代わりに任意の $c\in\mathbf C^\times$ で標識を付け替えても、補題 TB4-2 が与える置換は変わらない。
> **証明.** 付け替えは標識全体を $\mu_n$ の一定元だけ平行移動する。巡回 torsor 上では平行移動どうしの共役は自明だから、モノドロミー乗数は不変。∎
> ⇒ **委嘱が挙げた第 3 の難所(接基点での比較の定式化)は、$\varepsilon$ に関する限り空である。ただし A3 自体は消えない**(便 48 F4 の C11 欄)。

> **補題 TB4-2(反時計回りループのモノドロミー).**
> **前件【v2・V4 で明記】: (C1), (C5), chosen $\bar\iota$, radial comparison(接基点 $\vec{01}$ から $\beta=\delta$ への正実軸経路), A3.**
> $\gamma_0$ を $\vec{01}$ を基点とする $0$ のまわりの**反時計回り**単純ループとすると、$x=[\gamma_0]$ は
> $$ x\cdot\bigl(\xi\beta^{1/n}\bigr)\ =\ \eta_n\,\xi\,\beta^{1/n},\qquad \eta_n:=\bar\iota^{-1}\bigl(e^{2\pi i/n}\bigr) $$
> として作用する。

**証明【便 48 F6 が独立に PASS】.** $\gamma_0$ を $\beta(t)=\delta e^{2\pi it}$($t\in[0,1]$)で実現する。標識 $j$ の点 $w_j(0)=\bar\iota(\zeta_n)^{\,j}\delta^{1/n}$ から出発する持ち上げは
$$ w_j(t)\ =\ \bar\iota(\zeta_n)^{\,j}\,\delta^{1/n}\,e^{2\pi it/n} $$
($w_j(t)^n=\beta(t)$ ✓・連続 ✓・始点 ✓・被覆空間の持ち上げの一意性より**唯一**)。終点は $\bar\iota(\zeta_n)^{\,j}\,\bar\iota(\eta_n)\,\delta^{1/n}$。**A3**(位相の forward transport が代数の後合成左作用に対応する)により、これが $x\cdot(\text{標識 }j)$ である。∎

> **⚠【v2・V4】v1 の「三本の工房規約だけ」という表現を撤回する**(便 48 F6)。**薄いのは解析持ち上げではなく最後の A3 である。** 本稿は A3 を消していない — 消したのは**向き感受的な root 選択の部分**だけである。

> **★ 補題 C との対応(v1 から不変)**: 補題 C (b) は「正の実分枝は $(0,1)$ 上で正の実分枝のまま接続する」で $p\cdot v_1=v_0$ を出した。本補題は「正の実分枝を原点のまわりに反時計回りに一周させると $e^{2\pi i/n}$ 倍になる」で $x\cdot v_0=\eta_nv_0$ を出す。**道具は同じ(一意の解析接続)、経路が線分か円周かだけが違う。**

### 2.4 (C10) を使っていないことの確認 —【便 48 F4: PASS】

補題 C は「ループ $g$ の作用は $\psi_{C_n}(g)$ による平行移動」と書き、表で $\psi_{C_n}:x\mapsto1$ を与えている。**本稿はこの表を証拠として使わない**(それを $\varepsilon\equiv1$ の証拠にすれば $\mathrm{Gal}(C_n/U)\cong\mathbb Z/n$ の同一視の自由度を通じて循環する)。本稿は補題 TB4-1/TB4-2 で両辺を独立に計算している。

---

## 3. 三段の定理(【v2・V2】分割)

### 3.1 第 1 段 — 比較式 —【便 48 F7.1: PASS】

> ### 定理 TB4-3(比較式)
> **前件: A1(TB4$^{\rm u}$), A2(TB1 の繊維関手), A3(位相–代数比較), (C1), (C5), (C6), chosen $\bar\iota$.**
> (2.1) の $\varepsilon\in\hat{\mathbb Z}^\times$($x=\iota(\sigma_\zeta^{\,\varepsilon})$)は
> $$ \boxed{\ \zeta_n^{\,\varepsilon}\ =\ \eta_n\ =\ \bar\iota^{-1}\bigl(e^{2\pi i/n}\bigr)\qquad(\forall n\ge1)\ } \tag{$*$} $$
> を満たす。同値に、$\vartheta\in\mathrm{Gal}(\mathbb Q(\mu_\infty)/\mathbb Q)$ を $\vartheta(\zeta_n)=\eta_n\ (\forall n)$ で定めると
> $$ \varepsilon\ =\ \chi_{\rm cyc}(\vartheta)\ \in\ \hat{\mathbb Z}^\times . \tag{3.2} $$

**証明.** A1 により $\iota:I_0\xrightarrow{\sim}\overline{\langle x\rangle}$ で $\sigma_\zeta$ は位相的生成元、ゆえに一意な $\varepsilon\in\hat{\mathbb Z}^\times$ で $x=\iota(\sigma_\zeta^{\,\varepsilon})$(= BFC (2.1))。補題 TB4-1 を $\sigma=\sigma_\zeta^{\,\varepsilon}$ に適用すると $\chi_n(\sigma_\zeta^{\,\varepsilon})=\zeta_n^{\,\varepsilon}$、他方 補題 TB4-2 は $\eta_n$ 倍。$\mathrm{Fib}(C_n)$ は $\mu_n$-torsor で作用が自由だから乗数は一意、よって ($*$)。

$(\eta_n)_n$ は整合系($\eta_{mn}^{\,m}=\bar\iota^{-1}(e^{2\pi im/(mn)})=\eta_n$)で $(\zeta_n)_n$ も整合系だから $\vartheta$ は一意に定まる。($*$) は $\zeta_n^{\,\varepsilon}=\zeta_n^{\chi_{\rm cyc}(\vartheta)}$ を全 $n$ で与え、$\hat{\mathbb Z}\hookrightarrow\prod_n\mathbb Z/n$ の単射性から (3.2)。∎

> **★ ($*$) は「$\varepsilon$ の値」ではなく「$\varepsilon$ の測り方」を与える。** $\varepsilon$ が $1$ かどうかは、($*$) の右辺 $\eta_n$ と左辺の $\zeta_n$ が**同じ object か**にかかっている — それが次の 2 段である。

### 3.2 第 2 段(有限) — $M\mid20$ の窓 —【v2 新設・未監査】

> ### 定理 TB4-A20(有限正規化)
> **前件: 定理 TB4-3 の前件 $+$ $\bar\iota|_K=\iota_\infty$ $+$ (Z20-link) $+$ Rule 1 (1.6) $+$ (TB2) の整合性.**
> $$ \boxed{\ \varepsilon\ \equiv\ 1\ \ (\mathrm{mod}\ 20).\ } $$
> したがって $M\mid20$ なら $\varepsilon\equiv1\ (M)$、BFC (2.2) より **$b=1$**。

**証明.** (Z20-link) より $\zeta_{20}^{\rm TB2}=\zeta_{20}^{\rm Rule1}$。$\bar\iota|_K=\iota_\infty$ と Rule 1 (1.6)(「$\operatorname{Im}>0$ かつ $\operatorname{Re}$ 最大」は**一意**に $e^{2\pi i/20}$ を指す)より
$$ \bar\iota\bigl(\zeta_{20}^{\rm TB2}\bigr)=\iota_\infty\bigl(\zeta_{20}^{\rm Rule1}\bigr)=e^{2\pi i/20}\ \Longrightarrow\ \eta_{20}=\bar\iota^{-1}(e^{2\pi i/20})=\zeta_{20}^{\rm TB2}. $$
($*$) を $n=20$ で読むと $(\zeta_{20})^{\varepsilon}=\zeta_{20}$、$\zeta_{20}$ は原始 $20$ 乗根だから $\varepsilon\equiv1\ (20)$。$M\mid20$ なら $\varepsilon\equiv1\ (M)$。∎

> **注(なぜ $n=20$ だけでよいか)**: (TB2) の整合性 $\zeta_{mn}^m=\zeta_n$ に $m=20/n$ を入れると $\zeta_n=\zeta_{20}^{20/n}$($n\mid20$)なので、$n\mid20$ の全項が $n=20$ から従う。**したがって (Z20-link) 1 本で $M\mid20$ の窓全体を賄う。**

### 3.3 第 3 段(profinite) — exact (TB4) —【便 48 F8: 条件付き PASS】

> ### 定理 TB4-B(全正規化)
> **前件: 定理 TB4-3 の前件 $+$ (Z-norm)(§8.1 の 4 条 atomic seal).**
> $$ \boxed{\ \varepsilon=1,\qquad x=\iota(\sigma_\zeta),\qquad\text{すなわち (TB4) が定理.}\ } $$
> **証明.** (Z-norm)(ii) より $\zeta_n=\bar\iota^{-1}(e^{2\pi i/n})=\eta_n\ (\forall n)$、ゆえに $\vartheta=\mathrm{id}$、(3.2) より $\varepsilon=1$。∎
> **(Z-norm) の実現可能性**: $\bar\iota_0$ を $\iota_\infty$ の任意の延長とし $\zeta_n:=\bar\iota_0^{-1}(e^{2\pi i/n})$ と**定義**すればよい。(i) 整合系 ✓ (ii) $n\mid20$ で Rule 1 (1.6)(1.7) と一致 ✓ (iii) (Z20-link) を含む ✓。**新しい算術仮定ではなく、未指定だった比較データの選択である**(便 48 F8)。

> **★【v2・V2 / 便 48 F13.2】なぜ二段に分けるか**: $K^{(5)}$ 運用に必要なのは $\varepsilon\bmod10$ だけである。**(Z-norm)(全 $n$ の profinite normalization)の版上げ事故が、$M\mid20$ の finite 結論を巻き込まない**ようにする。**TB4-A20 と TB4-B は別札で管理すること。**

### 3.4 【v2・V1 新設】blocker B1 の記録 — countermodel の独立再現

> **v1 の誤り(自認)**: v1 の定理 TB4-A(a) は「**既存三文書だけで** $\varepsilon\equiv1\ (20)$」と主張した。**これは偽である。** (Z20-link) を前件に置かねばならない。

**便 48 F7.2 の countermodel(本稿で独立再現・検査 4)**: $t\in\hat{\mathbb Z}^\times$ を任意に取り、(TB2) の系を
$$ \zeta_n^{\rm TB2}\ :=\ \bigl(\zeta_n^{\rm can}\bigr)^{t},\qquad \zeta_n^{\rm can}:=\bar\iota^{-1}(e^{2\pi i/n}) $$
と選ぶ一方、Rule 1 の体生成元は $\zeta_{20}^{\rm Rule1}=\zeta_{20}^{\rm can}$ のままとする。

- **整合系である**: $(\zeta_{mn}^{\rm TB2})^m=((\zeta_{mn}^{\rm can})^m)^t=(\zeta_n^{\rm can})^t=\zeta_n^{\rm TB2}$ ✓
- **原始冪根である**: $t\in\hat{\mathbb Z}^\times$ ゆえ全 $n$ で $\gcd(t,n)=1$ ✓
- **現行文面をすべて満たす**: (TB2) は「整合系を固定する」としか言わず、(1.6) は体生成元の像しか言わない ✓

このとき $\eta_n=\zeta_n^{\rm can}=(\zeta_n^{\rm TB2})^{t^{-1}}$ なので ($*$) は $\zeta_n^{\,\varepsilon}=\zeta_n^{\,t^{-1}}$、すなわち
$$ \boxed{\ \varepsilon\equiv t^{-1}\ (\mathrm{mod}\ 20),\qquad b\ =\ \varepsilon^{-1}\bmod10\ \equiv\ t\ \ (\mathrm{mod}\ 10).\ } \tag{3.3} $$

**$t\equiv3\ (20)$ なら $\varepsilon\equiv7$、$b=3$** — **便 48 の値と完全一致**(検査 4 で $(\mathbb Z/20)^\times$ の 8 元すべてを整数演算で再現)。

> **★【v2 で得た一般形 (3.3)】観測される捻れ $b$ は、root-object のずれ $t$ そのもの($\bmod\ 10$)である。** v1 が持っていなかった知見で、二つの帰結をもつ:
> 1. **反転経路は $\pm1$ ではない** — $t$ は $(\mathbb Z/20)^\times$ 全体(8 通り)を走り、$b$ は $(\mathbb Z/10)^\times$ 全体(4 通り)を取る(§6 経路 8)。
> 2. **$t\equiv11\ (20)$ は $b=1$ を与える**(検査 4)。すなわち **root-object がずれていても単一の $M=10$ では検出できない場合がある** — BFC (2.2)「単一の $M$ で $b=1$ を観測しても exact (TB4) は戻らない」の**具体的 witness** である。

---

## 4. (TB4)/(TB4$^{\rm u}$) の言明との突合(語まで)

### 4.1 (TB4) 逐語との対照

| (TB4) の節 | v2 での身分 | 前件 |
|---|---|---|
| 「$\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))\cong\hat{\mathbb Z}(1)$」 | **枠組みのまま**(向きに鈍感) | A1 |
| 「$\Omega$ への**後合成(= 左作用)**で $\mathrm{Fib}$ に作用する」 | **枠組みのまま**(向きに鈍感)。逆数は入らない | A1, (C3) |
| 「$\sigma_\zeta:\beta^{1/n}\mapsto\zeta_n\beta^{1/n}$」 | **定義**((TB2) の系による $I_0$ の位相的生成元の指定) | (TB2) |
| **「$x$ は…$\sigma_\zeta$ の像そのものである」** | **本稿で証明**(TB4-B)。**ただし A3 は残り、(Z-norm) が要る** | TB4-3 + (Z-norm) |

⇒ **(TB4) $=$ (TB4$^{\rm u}$) $+$ A3 $+$ (Z-norm) $+$ [本稿の定理]**。**向き感受的な root 選択は関所から外れるが、A3 は framework seal として残る。**

### 4.2 (2.1)(2.2) との整合

BFC (2.2)「単一の $M$ で $b=1$ を観測しても exact (TB4) は戻らない」を本稿は**否定しない**どころか §3.4 で witness($t\equiv11$)を与えた。本稿は観測ではなく**規約から $\varepsilon$ を計算する**方向なので (2.2) の警告の射程外である。

### 4.3 【v2・V11】$(\zeta_n)$ の使用箇所の悉皆 $+$ **object identity 欄**

> **v1 の欠陥(自認・便 48 F8)**: v1 の悉皆表には「**同じ字形の object identity**」の型がなかった。$\zeta_{20}$ が二文書で別 object でありうることを、表そのものが表現できていなかった。

| 使用箇所 | どの $\zeta$ か | **object** | (Z-norm) との整合 |
|---|---|---|---|
| (TB2)「整合系を固定する」 | $(\zeta_n^{\rm TB2})_n$ 全体 | **TB2 根系** | 具体値未指定 ⇒ (Z-norm) はその具体化 ✓ |
| (TB4) $\sigma_\zeta$ | $(\zeta_n^{\rm TB2})_n$ 全体 | **TB2 根系** | 本稿の対象 ✓ |
| Rule 1 (1.5) $K=\mathbb Q[T]/\Phi_{20}$, $\zeta_{20}:=\bar T$ | $n=20$ | **$K$ の体生成元** | **(Z20-link) が要る** ⚠ |
| Rule 1 (1.6) $\iota_\infty$ | $n=20$ | **$K$ の体生成元の像** | 同上 ⚠ |
| Rule 1 (1.7) $\zeta_{10}:=\zeta_{20}^2$, $\zeta_5:=\zeta_{20}^4$ | $n=10,5$ | **$K$ の体生成元の冪** | (Z20-link) 経由 ✓ |
| Rule 1 (1.8) $\iota:\mu_{10}\to\langle X\rangle,\ \zeta_{10}\mapsto X$ | $n=10$ | **$K$ の体生成元の冪**($\tau$ の型) | 同上 ✓ |
| Rule 1 (7.1) $\tau_i(\zeta_{10}^{b_i})$ | $n=10$ | **$K$ の体生成元の冪** | 同上 ✓ |
| **BFC 補題 B-6 (8.1)・B-6$^{\rm tw}$ (8.2)** | $n=M$ | **⚠ 両者を混用**($m$ 側は TB2 根系、$\tau$ 側は体生成元) | **BFC の証明が (Z20-link) を暗黙に使っている**(§4.4) |
| Rule 1 (1.9) $\kappa_w$ | **使わない**($\mu_{10}$ の元をそのまま値に取る) | — | 無関係 ✓ |
| (W2) $\tilde\chi\circ\mathrm{Ih}_N=\chi_{2M}$ | **使わない**(円分指標は系の選び方に依らない) | — | 無関係 ✓ |
| BFC 補題 B-5 (7.1)(7.2) | **使わない**($\kappa_{u^{-1}}$ は $M$ 乗根の取り方に依らない) | — | 無関係 ✓ |
| $A_5$ v4 補題 C・D・系 E((CAL)) | **使わない**(補題 C は $\zeta_n$ の具体値を使わない) | — | 無関係 ✓ |
| $n\nmid20$ の $\zeta_n^{\rm TB2}$ | — | **どこにも現れない** | **純粋な空白** ⇒ (Z-norm)(ii) は無償 ✓ |

### 4.4 【v2 新設】$B_{\rm FC}$ 側への波及(司令塔裁定事項)

上表の ⚠ 行が示すとおり、**BFC 補題 B-6/B-6$^{\rm tw}$ の証明は $m(\zeta_M)$(TB2 根系側)と $\tau(\zeta_M)$($K$ の体生成元側)を同じ記号で書いており、(Z20-link) を暗黙に使っている。** 本稿の (Z20-link) は $B_{\rm FC}$ 自身の前件でもある。

- **$B_{\rm FC}$ の結論は変わらない**((Z20-link) は無償の規約であり、加えれば済む)。
- しかし **$B_{\rm FC}$ v2 §2 の (TB2) 条文に (Z20-link) を追記する**か、**§8.1 の seal を参照させる**必要がある。**本稿の権限外なので司令塔の裁定に上げる**(§8.5・§8.8-3)。

---

## 5. 補題 B-6 の $b=1$ に必要な exact 形は出るか(委嘱 (iv))

### 5.1 出る — **ただし (Z20-link) の下で**【v2 で条件を明記】

補題 B-6 の証明第 1 段「$x\cdot p=m(\zeta_M)p$」に対し、本稿の補題 TB4-2 は **exact (TB4) を経ずに直接** $x\cdot p=m(\eta_M)p$ を与える。定理 TB4-A20 により、**(Z20-link) の下で** $M\mid20$ なら $\eta_M=\zeta_M$ である。

$$ \boxed{\ \text{(Z20-link)}+\text{A1--A3}+\text{(C1)(C5)(C6)}+\text{chosen }\bar\iota\ \Longrightarrow\ M\mid20\ \text{の窓で補題 B-6 の (8.1) と }b=1 . } $$

$K^{(5)}$ は $M=10\mid20$ なので該当する。**v1 は前件から (Z20-link) と A3 を落としていた。自認。**

### 5.2 それでも Rule 1 §7 の測定規律は緩めない

Rule 1 §7.4「$b_i=1$ を仮定してはならない。必ず (7.1) を計算して記録する」を**一切緩めない**。修文案は §8.4(便 48 F10.2 の文言を採用)。

### 5.3 射程の限界 — $M\nmid20$ の窓は未決(UNKNOWN)

$K^{(3)}$ 回帰は $M=6$、$K=\mathbb Q(\zeta_{12})$、$6\nmid20$、$\zeta_6\notin\mathbb Q(\zeta_{20})$。**Rule 1 (1.6) はこの窓の埋め込みを凍結していない。**

- 現状の正典は `docs/manifest_k5_appendixA_v1.md` §2 K3 行が「生成元の向きの曖昧さは判定にも固定体にも影響しない」と**無害宣言**しており、$K^{(3)}$ の既存判定は本稿の影響を受けない。
- $\iota_{12}(\zeta_{12}^{\rm Rule})=e^{2\pi i/12}$ と対応する (Z12-link) を凍結すれば $\varepsilon\equiv1\ (12)$、$b=1$。**無償だが現時点では凍結文がないので UNKNOWN。**
- **(Z-norm) を採れば全 $M$ で一斉に解決する** — これが §8.1 を「$M$ ごとの埋め込み」でなく「根系の一括指定」として書く理由。

---

## 6. 反実仮想 — $\varepsilon\ne1$ が出る条件(委嘱 (v)・【v2・V6 で 3 経路追加】)

> **⚠ v1 の誤り(自認・便 48 F9)**: v1 は 5 経路を挙げて「反転経路をすべて列挙した」かのように書いた。**不完全だった。** とくに **root-object ずれは $\pm1$ ではなく $(\mathbb Z/20)^\times$ 全体を生む**。

| # | 反実仮想 | 帰結 | 現状の正典での身分 |
|---|---|---|---|
| 1 | **(C1)** を $(AB)\cdot i=B\cdot(A\cdot i)$ と読む | 合成が逆順、$x$ の作用は $L_{\gamma_0}^{-1}$。$\varepsilon=-1$、$b=9$ | **排除済**。規約 W-1 が作用式で明示凍結(「時間語は正本に置かない」設計) |
| 2 | **(C2)** を inverse transport と読む | 同上 $\varepsilon=-1$ | **排除済**。補題 C の 4 用例(§1.1)。**ただし (C1) からは導出できない** |
| 3 | **(C5)** を時計回り正と読む | $\varepsilon=-1$ | **排除済**。Rule 1 §1.1「この向きが正本」+ §7.1 |
| 4 | **(C4)** の $\iota_\infty$ を $\operatorname{Im}<0$ 側に取る | $\varepsilon\equiv-1\ (20)$、$b=9$ | **排除済**。(1.6) は**一意** |
| 5 | **(C7)** を $\zeta_n\ne e^{2\pi i/n}$($n\nmid20$)と取る | $\varepsilon\ne1$ だが $\varepsilon\equiv1\ (20)$ は不変、**$b=1$ は不変** | **UNKNOWN**。(Z-norm)(ii) で閉じる |
| **6** | **【v2 追加】(C3) の反転** — 後合成左作用を**前合成・右作用**として読む | $\iota$ が反準同型になり $\varepsilon=-1$、$b=9$ | **排除済**((TB4$^{\rm u}$) が明記)。**だが反転表に載せるべきだった**(便 48 F9) |
| **7** | **【v2 追加】A3 の反転** — 位相 forward transport を代数作用の**逆**へ送る比較 | $\varepsilon=-1$、$b=9$ | **UNKNOWN(framework seal)**。正典に条項なし ⇒ §8.2 の seal + 文献要請 13(ii)(縮小版)で押さえる |
| **8** | **【v2 追加】root-object ずれ** — $\zeta_{20}^{\rm TB2}=(\zeta_{20}^{\rm Rule1})^t$、$t\in(\mathbb Z/20)^\times$ **任意** | $\varepsilon\equiv t^{-1}\ (20)$、**$b\equiv t\ (\mathrm{mod}\ 10)$** — $b$ は $\{1,3,7,9\}$ **全体**を取る。$t\equiv3$ で $b=3$ | **UNKNOWN $\to$ (Z20-link) で閉じる**。**便 48 の具体的 countermodel**(§3.4・検査 4) |

> **★ 符号の敏感性は本物である。** 8 経路のうち **1–4, 6 は凍結文で排除済、5, 7, 8 は未凍結**である。**したがって v1 の「$\varepsilon=-1$ の枝は工房規約では立たない」は経路 1–4, 6 についてのみ正しく、経路 7, 8 については立ちうる。自認。** §7 の検査 3(時計回り)と検査 4(root-object)は 2 種の敏感性を機械で再現している。

---

## 7. 用いた計算(全列挙・Rule 1 §0.4 の申告様式)

**本稿の証明は閉形式であり、機械計算に依存しない。** 以下は取り違え検出のための補助検査である。

`scratchpad/tb4-monodromy-check.mjs`(node・**リポジトリ外**・**25/25 PASS**):

| 検査 | 内容 | 型 | 検証対象 |
|---|---|---|---|
| **1** | $w^n=\beta$ の反時計回り解析接続(離散連続分枝追跡・4000 ステップ)。$n=2,3,5,6,10,12,20$ で置換 $j\mapsto j+1$ | 浮動小数点 | 補題 TB4-2 の独立再現(閉形式の持ち上げを使わない) |
| **2** | 局所 Kummer $\lambda=u\,s^M(1+c_1s+c_2s^2)$ の正規化 uniformizer $\tilde s=s\,h(s)^{1/M}$ が反時計回りで**厳密に $\zeta_M$ 倍**($M=5,6,10$・機械精度 $\sim10^{-16}$)。生の $s$ は $O(|s|)$ ずれる | 浮動小数点 | BFC 補題 B-5(iii) $+$ B-6 第 1 段の幾何側からの確認 |
| **3** | 時計回りで標識が $0\mapsto n-1$($n=5,10,20$) | 浮動小数点 | §6 経路 1–3, 6 の符号敏感性 |
| **4** | **【v2 追加】root-object ずれ $t\in(\mathbb Z/20)^\times$ の 8 元すべてで $\varepsilon\equiv t^{-1}\ (20)$・$b\equiv t\ (10)$。$t=3\Rightarrow\varepsilon\equiv7,\ b=3$。$t=11\Rightarrow b=1$** | **整数演算のみ** | **便 48 F7.2 countermodel の独立再現**(§3.4)$+$ 一般形 (3.3) の発見 |

**入力**: すべて一般の玩具データ($u,c_i$ は任意の小整数)と整数。**$K^{(5)}$ の個別モデル候補・係数・数値近似・database・$\lambda$・$u$・$c$ には一切接触していない。** 探索コマンドは実行していない。上記以外の機械計算は行っていない。

---

## 8. 司令塔への提案

### 8.1 【v2・V5】(Z-norm) — **atomic seal** としての条文案

$B_{\rm FC}$ v2 §2 の (TB2)、および Rule 1 §1.4 に、**次の 4 条を分割不能な 1 つの seal として**加えることを提案する(便 48 F8 の文面を採用)。

```text
TB2-norm / comparison-root seal:
  (i)   bar_iota extends Rule1 iota_infty;
  (ii)  zeta_n^TB2 = bar_iota^{-1}(exp(2*pi*i/n))  for every n;
  (iii) in particular  zeta_20^TB2 = zeta_20^Rule1;      # = (Z20-link)
  (iv)  all TB4 comparisons use this same bar_iota and this same root system.
```

- **(iii) 単独でも有限レベル(定理 TB4-A20)には足りる** — $M\mid20$ の窓だけを運用するなら (Z20-link) を先に凍結する選択肢がある(便 48 F7.2「一行入れるだけでも有限レベルには足りる」)。**ただし §3.3 の profinite 結論には (ii) 全体が要る。**
- **無償である**: §4.3 の悉皆確認により、既存のどの条項とも衝突しない($n\nmid20$ は純粋な空白)。
- **分割不能にする理由**: (i) だけ・(ii) だけを採ると (iv) の「同一の $\bar\iota$」が保証されず、窓ごとに別の比較データが混入しうる。

### 8.2 【v2・V5】A3 は**別の** framework seal として分離掲示

```text
TB4-comparison / orientation seal (framework, NOT implied by TB2-norm):
  positive topological forward transport  <->  algebraic postcomposition-left action
```

**(Z-norm) は A3 を証明しない**(便 48 F8)。A3 は (TB1)(TB3) と同格の枠組み事実であり【GAP-TB】に残る。**本稿が消したのは root 選択の自由度であって、比較の向きではない。**

### 8.3 【v2・V8】文献要請 13 の処分案(**縮小維持**・全面取下げではない)

| 項目 | 処分 |
|---|---|
| (i) 繊維関手の圏同値 | **維持**(向きに鈍感・優先度 中) |
| **(ii)** | **【v2 で訂正】全面取下げではなく縮小維持**:「**正の位相 transport が algebraic fiber functor の後合成左作用へ送られ、逆作用でないことの標準比較定理・記法確認**」= **A3 の裏取り**。root 正規化そのものは工房規約なので文献に決めてもらう必要はないが、**A3 は load-bearing のまま**である |
| (iii) 係数分裂と慣性作用が同時に後合成として記述されること | **維持**(向きに鈍感) |

> **v1 の誤り(自認)**: v1 は (ii) を「取り下げ可」と書いた。**(ii) には root 選択(工房の仕事)と comparison orientation(A3・文献の仕事)が混ざっており、後者は残る。**

### 8.4 【v2・V7】Rule 1 §7.4 の条文修正案(便 48 F10.2 の文言)

> **現行**: 「…$b_i=1$ が**期待される**」
> **v1 案(撤回)**: 「$b_i\ne1$ は**必ず実装事故**」 — **強すぎる。** TB4 は A1–A3 の framework-conditional な紙上定理なので、診断候補に**紙上前件・証明の誤り**も入る。
> **v2 案(採用)**:
> > **採用済み framework、TB2-norm / comparison seal、凍結 input がすべて正しく実現されている限り $b_i=1$ は定理である。$b_i\ne1$ は新しい算術現象として受理せず integrity quarantine とし、次の順に監査する: (1) 実装(左右・向きの事故)→ (2) transport → (3) input / root-system seal → (4) 紙上 framework 前件および証明。**
> **不変**: 「$b_i=1$ を仮定してはならない。必ず (7.1) を計算して記録する」以下はそのまま。

### 8.5 状態札の更新案(**(Z20-link)/(Z-norm) 凍結後に限る**)

$$ \begin{array}{ll}
\text{現行:} & \texttt{TB4 = unique orientation-sensitive literature gate for exact }b=1\\[4pt]
\text{提案:} & \texttt{TB1, TB3, TB4}^{\rm u}\texttt{, A3 = global framework assumptions}\\
& \texttt{TB2 + TB2-norm seal = workshop conventions}\\
& \texttt{TB4-A20 = finite theorem (M | 20), conditional on Z20-link}\\
& \texttt{TB4-B = profinite theorem, conditional on Z-norm}\\
& \texttt{no root-selection literature gate remains; A3 orientation gate remains}
\end{array} $$

**便 48 F10.1「現時点ではまだ更新しない」に従う。** 加えて **§4.4 の $B_{\rm FC}$ 側への波及**((TB2) 条文への (Z20-link) 追記)を同一 version event で裁定されたい。

### 8.6 【v2・V9】`TB4-comparison-seal/v1`(便 48 F13.1 を採用)

```text
TB4-comparison-seal/v1
  root_system_id                               # (TB2) の系の識別子
  rule1_zeta20_id                              # K の体生成元の識別子
  zeta20_equality_certificate                  # (Z20-link) の証明書
  bar_iota_id                                  # 選んだ Q̄ ↪ C の識別子
  topological_loop_orientation = ccw           # (C5)
  path_transport = forward                     # (C2)
  algebraic_action = postcomposition_left      # (C3)
  top_etale_comparison_orientation_certificate # A3
```

**Rule 1・$B_{\rm FC}$・結果 record の三者がこの seal の digest を参照する設計**とする。**同じ root name を人間が再解釈する余地を物理的に消せる** — 本稿の blocker B1 はまさにその再解釈で生じた。

### 8.7 【v2・V12】amendment を削ってはならない(便 48 F11)

**TB4-A20/TB4-B が成立しても、amendment の次の規律を削ってはならない**:

- Freeze 1 で rule を事前コミット / Freeze 2 で actual $b_i$ を $u$・$G_K$ 観測**前**に記録 / 観測後 fitting と $\exists b$ PASS の禁止 / $b_i\ne1$ の integrity quarantine 送り。

$$ \boxed{\ \textbf{定理があることは、実装がその定理の規約を実現したことを保証しない。}\ } $$

### 8.8 Sol への突合依頼(v2 の新規部分のみ)

1. **§3.2 定理 TB4-A20 の前件**が過不足ないか(とくに $\bar\iota|_K=\iota_\infty$ を (Z20-link) と別立てにした点)。
2. **§3.4 の (3.3) $b\equiv t\ (\mathrm{mod}\ 10)$** — 便 48 の $t=3$ の値は再現したが、一般形は本稿の新規主張であり**単系統・未監査**。
3. **§4.4 の $B_{\rm FC}$ 側への波及の見立て**(補題 B-6 の証明が (Z20-link) を暗黙に使っているという読み)が正しいか。**もし正しければ $B_{\rm FC}$ v2 の前件欄も 1 行増える。**
4. §6 の反転表 — **8 経路でまだ不足がないか**(v1 は「全部」と言って外した)。
5. §8.1 の seal を **(iii) だけ先に凍結する**運用(finite だけ先行)に危険がないか。

---

## 9. 依存の総まとめ(【v2 で A8 を修正・A12 を新設】)

| # | 仮定 | 型 | 状態 |
|---|---|---|---|
| **A1** | **(TB4$^{\rm u}$)**: $\mathrm{im}(I_0)=\overline{\langle x\rangle}$、$\iota:I_0\xrightarrow{\sim}\overline{\langle x\rangle}$、後合成(左) | 枠組み | **【GAP-TB】のまま** |
| **A2** | **(TB1)** の繊維関手の定義式($C_n$ でのみ使用・明示計算) | 枠組み | 【GAP-TB】のまま |
| **A3** | **位相 forward transport $\leftrightarrow$ 代数 後合成左作用**($C_n$ についてのみ) | **枠組み(向き感受的)** | **【GAP-TB】のまま。§8.2 の seal $+$ 文献要請 13(ii) 縮小版で押さえる。(Z-norm) は A3 を証明しない** |
| **A4** | **規約 W-1**(C1) | 工房の規約 | **凍結済**(定義の正本) |
| **A5** | **Rule 1 §1.1**(C5): 反時計回りが正、$x=\gamma_0$ | 工房の規約 | **凍結済** |
| **A6** | **Rule 1 (1.6)(1.7)**(C4): $\iota_\infty(\zeta_{20}^{\rm Rule1})=e^{2\pi i/20}$ | 工房の規約 | **凍結済**(ただし**体生成元について**) |
| **A7** | **(TB2)** の整合性 $\zeta_{mn}^m=\zeta_n$ | 工房の規約 | **凍結済** |
| **A8** | (C2) forward transport | 正典の証明が依存 | **【v2 で訂正】「A4 から導出・独立仮定ではない」を撤回。$\Rightarrow$ A3 または $A_5$ v4 補題 C に依存**(便 48 F5) |
| **A9** | (C6) 正の実分枝による標識 | 正典の証明が依存 | **$\varepsilon$ に無影響**(補題 TB4-0) |
| **A10** | **(Z20-link)**(定理 TB4-A20) | 工房の規約(**新設提案**) | **未凍結**(§8.1(iii)) |
| **A11** | **(Z-norm) 全体**(定理 TB4-B のみ) | 工房の規約(**新設提案**) | **未凍結**(§8.1) |
| **A12** | **【v2 新設】chosen $\bar\iota:\bar{\mathbb Q}\hookrightarrow\mathbf C$ with $\bar\iota|_K=\iota_\infty$** | **比較データ(前件に明示量化)** | **未凍結**(§8.1(i)(iv)) |
| **A13** | 被覆空間の持ち上げの一意性・$\hat{\mathbb Z}\hookrightarrow\prod_n\mathbb Z/n$ | 標準・初等 | 閉 |

**使っていないもの(明示)**: 論文 2401/2405 の言明、$\mathrm{Ih}_N$、較正 (CAL)、(W1)–(W5)、定理 B-3/B-4、$u$、$K$-モデル、dessin、$K^{(5)}$ の個別データ、外部文献。**補題 C も「方法」と「forward transport の証拠」を借りただけで、その結論($g_\sigma\in[\hat F_2,\hat F_2]$)は使っていない。**

---

## ★教材

> ### ★教材 T1(便 48 F12 が採用・**v2 で自分に返ってきた**): 「文献関所」と札を貼る前に、**姉妹の凍結文書どうしを突き合わせよ**
> (TB4) は工房内の凍結文の連立で決まっていた。**しかし v1 は、まさにその突合を自分の稿で失敗した** — (TB2) の**根系** $\zeta_{20}^{\rm TB2}$ と Rule 1 の**体生成元** $\zeta_{20}^{\rm Rule1}$ を、**同じ字形だから同じ object と誤認**した。
> **⇒ T1 の完全形**: 「凍結文の対を突合せよ」だけでは足りない。**突合の際は、両者を結ぶ typed equality が正典にあるかを確認せよ。** 単独項目がそれぞれ正しくても、橋の equality がなければ結論は出ない。

> ### ★教材 T2(便 48 F12 が採用・**二欄に強化**): 規約表は「対の整合の相手」$+$「**比較写像 / equality の artifact ID**」の二欄を持て
> 「相手」だけでは、今回の $\zeta_{20}$ のように**同名 object が無言で同一視される**。比較写像の**向き**まで記録すれば、A3/C3 の逆転も同じ表で検査できる。§1 の表を二欄化した。

> ### ★教材 T5(**v2 新設**・便 48 の追加教材 1): **同じ glyph は同じ object ではない**
> 別文書の $\zeta_{20}$ を使って剰余結論($\varepsilon\equiv1\ (20)$)を出すなら、**equality を前件に置く**。「同じ記号を使っている」は型付けではない。
> **⇒ 検出法**: 結論に $\bmod\ N$ が出たら、「$N$ を決めている object は、$\varepsilon$ を定義している object と**同一であることが証明書つきで言えるか**」を必ず問う。

> ### ★教材 T6(**v2 新設**・便 48 の追加教材 2): **左作用式は forward transport を定義しない**
> 次の 4 つを分けて記録すること。v1 の補題 TB4-C は 1 と 3 を融合していた。
> $$ \underbrace{\text{action law}}_{(AB)\cdot i=A\cdot(B\cdot i)}\ /\ \underbrace{\text{path concatenation}}_{\text{どちらを先に辿るか}}\ /\ \underbrace{\text{transport direction}}_{\text{forward か inverse か}}\ /\ \underbrace{\text{topological--étale comparison}}_{\text{A3}} $$

> ### ★教材 T7(**v2 新設**・自己観察): **自己申告した弱点と、実際に落ちた場所は今回もずれた**
> v1 で私が「最も薄い一段」と自己申告したのは **A3(位相–代数比較)**であり、便 48 は確かにそこを条件付きにした(F6)。しかし **FAIL 判定を受けたのは申告していなかった (C4) の型付け**(F7.2)だった。
> **BFC v2 §12.3 の★教材 7「自分が不安な場所と実際に弱い場所は別物」が、独立のインスタンスでも同じ形で再現した。** 前者は**証明の最終段**、後者は**前件欄の型**に集中する。**⇒ 監査依頼は「不安な箇所」だけでなく「前件表の各行の型」を明示的に列挙して出すべきである。**

> ### ★教材 T3(v1・維持): 「向きの曖昧さは判定に影響しない」という無害宣言は、**射程を書かないと後で関所になる**
> `manifest_k5_appendixA_v1.md` の K3 行は正しいが「**何に**影響しないか」が書かれていない。

> ### ★教材 T4(v1・維持): 委嘱の出所指定は**開いて確かめる**
> 本委嘱は補題 C の所在を `manifest_k5_appendixA_v1.md` と指定したが、実在は `docs/week4-A5算術飽和_v4.md` §1.4.2。指定を信じていたら本稿の中核 (C2) に到達できなかった。**指定が空振りしたら正典内の名指し参照を辿り、その旨を報告する(黙って別文書を使わない)。**

---

## 付録 A: 主張一覧

| # | 主張 | 前件 | 検算 | 状態 |
|---|---|---|---|---|
| **TB4-C** | (C1)$+$forward transport(A3)$+$関手性 $\Rightarrow$ right-to-left | A4, **A3** | 補題 C の 4 用例 | 紙上(**v2 で修文**) |
| **TB4-0** | $\varepsilon$ は接基点のスケール・方向に依らない | — | — | 便 48 PASS |
| **TB4-1** | $\iota(\sigma)$ は $\chi_n(\sigma)$ 倍で作用 | A1, A2 | — | 便 48 PASS |
| **TB4-2** | $x=[\gamma_0]$ は $\eta_n$ 倍で作用 | **C1, C5, chosen $\bar\iota$, radial comparison, A3** | 検査 1 | 便 48 **A3 条件付き PASS** |
| **TB4-3** | 比較式 ($*$): $\zeta_n^{\,\varepsilon}=\eta_n$、$\varepsilon=\chi_{\rm cyc}(\vartheta)$ | A1–A3, C1, C5, C6, A12 | — | 便 48 **framework-conditional PASS** |
| **TB4-A20** | **$\varepsilon\equiv1\ (20)$**、$M\mid20$ で $b=1$ | TB4-3 $+$ **A10 (Z20-link)** $+$ A6, A7 | 検査 1・4 | **v2 新設・未監査** |
| **TB4-B** | **$\varepsilon=1$**($=$ exact (TB4)) | TB4-3 $+$ **A11 (Z-norm)** | — | 便 48 **条件付き PASS** |
| **(3.3)** | root-object ずれ $t$ で $\varepsilon\equiv t^{-1}(20)$、**$b\equiv t\ (10)$** | TB4-3 | **検査 4**(8 元悉皆) | **v2 新設・単系統・未監査** |
| ~~TB4-A(a)~~ | ~~既存三文書だけで $\varepsilon\equiv1\ (20)$~~ | — | — | **v2 で撤回(便 48 F7.2 blocker B1)** |
