# (TB4) の自前導出 — 枠組条件 $\varepsilon=1$ の解消 **v2.4(便 51 F4 status/provenance 同期版)**

2026-07-27 起草(v1)・2026-07-28 **v2**(便 48 Part B 修理)・**v2.1**(裁定 55)・**v2.2**(裁定 57 / 便 49)・**v2.3**(裁定 59 / 便 50 F2.2・F3・F4・F5・F7・F8.2 + Sol T-15)・**v2.4**(裁定 61 / 便 51 F4): Claude(数学者レイヤー・Opus 5・**第二インスタンス**)。司令塔委嘱「(TB4) の自前導出」。研究者 GO 済み。
**便 50 の判定: 数学核は全 PASS**(TB4-D/D′・TB4-E・$\hat b_i=b_{\rm op}$・四段のはしごの骨格・検査 5(d′) の算術・$K^{(3)}$ 副次記録)。**便 51 F4 も束 3 の 8 項目すべてを PASS** と判定した。**v2.3 は表示と型付けのみ、v2.4 は live status/provenance の同期と checker のラベル整合のみ** — **どちらも定理を 1 ミリも動かさない**(現物 checker `search/tb4-monodromy-check.mjs` **37/37**)。
**v2 は `sol/sol_reply_48_tb4_v24.md` Part B(F4–F13)の監査を反映**(司令塔指示 1–8 / Sol F14 項 5–7+α)。**解析計算(補題 TB4-2)は開け直していない** — 便 48 F6 が「解析持ち上げは正しい」と判定した部分は不変である。
**v2.1 は裁定 55**(§4.4 の波及指摘が B-6 所有者の検分で**確定**・BFC v2.6 で (TB2′)$=$(Z20-link) 前件化済)**の副産物「$b$ の定義差」を §3.5 に辞書として立てた**。

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

### v2 → v2.1 差分(裁定 55)

| # | 箇所 | v2 | v2.1 | 出所 |
|---|---|---|---|---|
| **V14** | **§3.5 新設**・§3.4・§5.1・§6・§8.6・付録 A | $b$ を単一の記号で扱っていた | **二つの $b$ を別記号に分離**: $b_{\rm cmp}:=\varepsilon^{-1}$(BFC (2.1) 側・$x$ と $\sigma_\zeta^{\rm TB2}$ の比較)と $b_{\rm op}$(BFC (8.1) 側・$m$ と $\tau$ の捻れ)。関係 **$b_{\rm op}=b_{\rm cmp}\cdot t^{-1}\ (\mathrm{mod}\ M)$** を私の規約で再導出(検査 5(a): $\varepsilon$ 任意の 64 対) | 裁定 55(**発見 = $B_{\rm FC}$ 著者**) |
| **V15** | §3.5.2(新設)・§5.1・§6 | (7.1) の測定値 $\hat b_i$ がどちらかを論じていなかった | **判定: $\hat b_i=b_{\rm op}$(断定)。** 導出は §3.5.2。**副次の帰結として $b_{\rm op}=1$ は (Z20-link) を要さない**((TB2) の根系が (7.1) にも (8.1) にも現れないため) | 裁定 55 依頼 2 |
| **V16** | §3.5.3・対話帳 T-13 | T-12 で「(7.1) は (Z20-link) の代替にならない/理由 = $t\equiv11$ で $b=1$」と書いた | **理由づけの誤りを自認・訂正。** 正しくは **$\hat b_i=b_{\rm op}=1$ が全 $t$ で成立**するので、(7.1) は root ずれを**構造的に一切検出できない**。**結論は不変(むしろ強まる)が、根拠が違う**(検査 5(c)) | 本便・自己訂正 |
| **V17** | §7 検算 | 25/25 | **29/29**(検査 5 = 二つの $b$ の辞書・4 項目) | 本便 |

### v2.1 → v2.2 差分(裁定 57 / 便 49・F8 条件 1–3)

| # | 箇所 | v2.1 | v2.2 | 出所 |
|---|---|---|---|---|
| **V18** | **§3.5.1(blocker)**・§3.4・§6・§8 | $t\in(\mathbb Z/M)^\times$ を $\zeta_M^{\rm TB2}=(\zeta_M^{\rm Rule1})^t$ で定め「**(Z20-link) $\iff t=1$**」と書いた | **偽。型落ちを自認・撤回。** $t$ を **$t_{2M}\in(\mathbb Z/2M)^\times$** と **$\bar t_M:=t_{2M}\bmod M$** に分離。正しくは **(Z$_{2M}$-link) $\iff t_{2M}=1$** で、**$\bar t_M=1$ は link の必要十分条件ではない**。反例(K5): $t_{20}=11$ は $\zeta_{20}^{\rm T}\ne\zeta_{20}^{\rm R}$ だが $\zeta_{10}^{\rm T}=\zeta_{10}^{\rm R}$。辞書は **$b_{\rm op}=b_{\rm cmp}\cdot\bar t_M^{-1}$** | 便 49 **F4.1 blocker** |
| **V19** | §3.5.1 TB4-D・§3.5.2 TB4-E の定理文 | TB4-D を「**定義だけから従う**」と書き、TB4-E の前件表に $c_\Lambda$ の出所がなかった | **named antecedents を定理文に掲示**。TB4-D: $\sigma_\zeta$ の Kummer 作用・$c_\Lambda$ の $x$-同変性・Rule 1 の $\tau(\zeta_M^{\rm R})=X$ marking。TB4-E: **B-4c / $c_\Lambda$ の $x$-同変性**(または Rule 1 §1.2–§1.5・§4.3 の actual marking/intertwiner)。**「付録 A に掲示」では不足**。TB4-E は TB4-3 全体でなく **TB4-2 orientation package** で足りる旨も注記 | 便 49 **F4.2・F4.4**(★教材 9-2) |
| **V20** | §3.5.4・§6 の検出表 | 「8 経路中 **7 本**が可視・盲点は root-object の 1 本」 | **偽。数え直し。** 可視 **6 本**(1,2,3,4,6,7)/ **不可視 2 本**(path 8 $=$ root-link 担当・**path 5 $=$ $n\nmid20$ で有限測定の射程外**)。母数 2 通り(**6/8** または finite 射程の **6/7**)を明記。**「(7.1) は (Z20-link) の代替でないだけでなく (Z-norm) 全体の certificate にもならない」**を追加。「8 本ですべて」とは書かず **single-axis regression set** と呼ぶ | 便 49 **F4.5・F6.4** |
| **V21** | §7・§8.6 | seal に $b$ 二欄・検査 5 は 4 項目 | **`TB4-b-dictionary/v1` schema**(F10.1 の 11 欄)へ差し替え。checker に **invariant 4 本**($b_{\rm cmp}=\varepsilon^{-1}$ / $b_{\rm op}=b_{\rm cmp}\bar t_M^{-1}$ / Z2M_link $\Rightarrow t_{2M}=1$ / **negative fixture: $\bar t_M=1\nRightarrow$ Z2M_link($M=10,t_{20}=11$)**)。regression 表を **finite operational suite**(期待 6 detected / 1 root-link blind)と **profinite root-normalization suite**(期待 out-of-scope)に**二分割**(検査 6) | 便 49 **F10.1・F10.2** |
| **V22** | §3.2・§8.1・§8.5・§8.8 | 「$b=1$」「(Z20-link) の先行凍結 $=$ (Z-norm) の一部凍結」 | **F6 の 7 回答を本文へ同期**: (F6.1) 結論の $b$ は **$b_{\rm cmp}=b_{\rm op}=1$** と型付け / (F6.5) 先行凍結は**独立 ID `Z20-link-seal/v1`**(「(Z-norm) の一部凍結」と呼ばない)/ (F6.3) 「結論の最小前件」と「現行 proof artifact の前件」を**分けて台帳化** / (F6.6) $\ell_i$ と $x=\gamma_0$ の同一性を **Rule 1 v1.4 の条文に明記**(同じ glyph に戻さない) | 便 49 **F6.1–F6.7** |

### v2.2 → v2.3 差分(裁定 59 / 便 50・束 3 = 表示・型付けの最終修文)

| # | 箇所 | v2.2 | v2.3 | 出所 |
|---|---|---|---|---|
| **V23** | **§3.5.1a**(はしご) | 1 枚の表に**条件・結論・定理名を同列で混在**させ、行間に含意矢印がなかった | **条件鎖 (3.6)** ((Z-norm)$\Rightarrow$(Z$_{2M}$-link)$\Rightarrow$($\bar t_M=1$))と**結論鎖 (3.7)** ($\varepsilon=1\Rightarrow\varepsilon\equiv1(2M)\Rightarrow b_{\rm cmp}=1$)を**別行に分離**。「共通 package の下で **L4$\Rightarrow$L3$\Rightarrow$L2$\Rightarrow$L1**、各逆向きは witness により偽」と明記。**witness 3 本**を表に(L1$\nRightarrow$L2: $t_{20}=3$ / L2$\nRightarrow$L3: $t_{20}=11$ / **L3$\nRightarrow$L4: 便 50 提供の $\hat{\mathbb Z}^\times$ unit**(2・5 進成分 $1$、**3 進成分 $-1$**、他 $1$ — $\bmod\ 20$ で $1$ だが exact でない)) | 便 50 **F3.2** |
| **V24** | 同上 | 命題 TB4-E を「**無条件**」と呼んだ | **全置換**: **root-link-free(ただし (E-i)–(E-iv) に相対的)**。**「無条件」は空の前件を意味する**(★教材 T11) | 便 50 **F3.2・F7-5** |
| **V25** | §3.5.3 | 導出本文には (B-i)–(B-iv) を書いたが、**判定 statement 自体に前件欄がなかった** | **statement 直下に named antecedents 4 点を掲示**: (B-i) $c_i=c_\Lambda$ は Rule 1 §4.3/B-4c の actual intertwiner / (B-ii) $\ell_i$ は **§1.1 の同じ** $x=[\gamma_0]$ が Fib に誘導する作用 / (B-iii) (7.1) の $\zeta_{10}$ は Rule 1 field generator の冪 / (B-iv) $\tau_i$ は Rule 1 (1.8) の marking | 便 50 **F2.2** |
| **V26** | **§3.5.1b 新設**・§3.5.4・§7 | (d′) を「$t_{20}=11\Rightarrow b=1$」という**普遍含意**に読める形で書いた | **full-tuple negative regression fixture 化**: `NF-root-link/K5` $=(M,t_{20},\bar t_{10},\varepsilon,b_{\rm cmp},b_{\rm op},\text{link})=(10,11,1,11,1,1,\textbf{false})$。**$\varepsilon$ の束縛(TB4-3)を明示**($t_{20}=11$ 単独からは $b_{\rm cmp}=1$ は出ない)。$K^{(3)}$ 同型 fixture `NF-root-link/K3` $=(6,7,1)$ も同形式で。**checker の実計算は初めからこの読みだった**ので修理は文書側と表示のみ | 便 50 **F4.2**・Sol **T-15** |
| **V27** | §8.9 | Rule 1 条文案が「$\lambda$ の値域が $U$ の座標 $\beta$-線」— **map・base・接基点を一つの typed equality にしていない** | **便 50 F5-4 の型へ差し替え**: 底を $U_\lambda$ と書き、**座標同型 $\beta=\lambda$ により接基点 $\vec{01}$・標準向き・ループ $\gamma_0$ を保って $U_\beta$ と同一視**する。$\ell_i$ は**この同じ** $x=[\gamma_0]$ が $\mathrm{Fib}_{\vec{01}}(W_0^{(i)})$ に誘導する permutation であり、**別の local generator の再定義ではない** | 便 50 **F5-4** |
| **V28** | §8.6a | dictionary schema に normalization 水準の欄がなかった | **`root_normalization_level = none \| mod_M \| level_2M \| profinite` を追加**し、各値に許される結論を固定(四段のはしごと 1:1)。**L2/L3 の同欄圧潰を schema が拒否できる** | 便 50 **F8.2** |
| **V29** | §7 検算 | 33/33 | **34/34**(検査 5(d)(d′) を full-tuple 形へ・**(e) $K^{(3)}$ 同型 fixture を新設**) | 本便 |

### v2.3 → v2.4 差分(裁定 61 / 便 51 F4・**status/provenance の小修理のみ**)

| # | 箇所 | v2.3 | v2.4 | 出所 |
|---|---|---|---|---|
| **V30** | §0 状態札・§3.2 見出し・付録 A | TB4-A20 を **「未監査」**(3 箇所) | **便 50 F2.1 で型修理後 PASS 済み**へ同期。**過大にしないため「two-mathematician audit 前・Lean `verified` ではない」を併記** | 便 51 **F4** |
| **V31** | §0 状態札 | 数値 checker **25/25**(v2.1 時点で止まっていた) | **37/37**(現物) | 便 51 F4 |
| **V32** | §7 | checker path を **`scratchpad/`(リポジトリ外)** と記載 | **`search/tb4-monodromy-check.mjs`(tracked 現物)**。司令塔が恒久化済み(内容は scratchpad 版と byte 同一を確認) | 便 51 F4 |
| **V33** | §7 検査 5(e)・checker | **ラベル過大**: ラベルは $\ker((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times)=\{1,7\}$ を検査すると書きながら、コードは $7\bmod6=1$・$7\ne1$・$12/6=2$ しか見ていなかった | **units 列挙による核の完全一致検査へ強化**。(e) $\ker((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times)=\{1,7\}$ / (e′) $t_{12}=7\in\ker\smallsetminus\{1\}$ / **(f) $\ker((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times)=\{1,11\}$**(§3.5.1 の反例の出所・**同じラベル過大の危険が K5 側にもあったので同時に閉じた**)/ (f′) $t_{20}=11$ がその非自明元。**34/34 → 37/37** | 便 51 **F4**(+ 本便の自主拡張) |

> **v2.4 で数学は一切動かない。** 便 51 F4 は束 3 の 8 項目すべてを **PASS** と判定しており、修理は **live status の同期**と **checker のラベル整合**のみである。

> **v2.3 でも不変(便 50 が PASS と判定した部分)**: **TB4-D/D′ の辞書と証明核**・**TB4-E の証明核と依存削減**(TB4-3 全体でなく TB4-2 orientation package で足りる)・**$\hat b_i=b_{\rm op}$**・**四段のはしごの数学的骨格**(F3.1「支持」)・**検査 5(d′) の算術**(F4.1・独立再計算で一致)・**$K^{(3)}$ 副次記録**(F4.3)・suite 二分割(F5-2)。**v2.3 は表示と型付けのみ。**

> **v2.2 でも不変(便 49 が PASS と判定した部分)**: **TB4-D / D′ の辞書**(型修理後)・**$\hat b_i=b_{\rm op}$(F4.3 で確定)**・**TB4-E の証明核**(F4.4)・TB4-1/2/3・TB4-0・比較式 ($*$)・(Z-norm) 下の TB4-B・命題 TB4-E が (Z20-link) を要さないこと(F6.7)。修理は**型の分離・前件の明示・数え直し・schema 化**であり、定理核は動かない。

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
> | **TB4-A20**($\varepsilon\equiv1\ (20)$) | **`paper-proof / conditional on (Z20-link)` — 便 50 F2.1 で型修理後 PASS**(**two-mathematician audit 前**・Lean `verified` ではない) |
> | **TB4-B**($\varepsilon=1$) | **`paper-proof / conditional on (Z-norm)`**(便 48「条件付き PASS」) |
> | 数値 checker | **`37/37 sanity only`**(`search/tb4-monodromy-check.mjs`・**証明の一部ではない**・網羅性は検査していない) |
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

### 3.2 第 2 段(有限) — $M\mid20$ の窓 —【v2 新設・**便 50 F2.1 で型修理後 PASS**】

> ### 定理 TB4-A20(有限正規化)
> **前件: 定理 TB4-3 の前件 $+$ $\bar\iota|_K=\iota_\infty$ $+$ (Z20-link) $+$ Rule 1 (1.6) $+$ (TB2) の整合性.**
> $$ \boxed{\ \varepsilon\ \equiv\ 1\ \ (\mathrm{mod}\ 20).\ } $$
> したがって $M\mid20$ なら $\varepsilon\equiv1\ (M)$、BFC (2.2) より **$b_{\rm cmp}=b_{\rm op}=1$**(**【v2.2・V22】結論の $b$ は必ず型付けする** — 便 49 F6.1。無注記の単一文字 $b$ は以後使わない)。

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
$$ \zeta_n^{\rm TB2}\ :=\ \bigl(\zeta_n^{\rm can}\bigr)^{t},\qquad \zeta_n^{\rm can}:=\bar\iota^{-1}(e^{2\pi i/n})\qquad\bigl(\text{その }2M=20\ \text{成分が }t_{20}:=t\bmod20\bigr) $$
と選ぶ一方、Rule 1 の体生成元は $\zeta_{20}^{\rm Rule1}=\zeta_{20}^{\rm can}$ のままとする。

- **整合系である**: $(\zeta_{mn}^{\rm TB2})^m=((\zeta_{mn}^{\rm can})^m)^t=(\zeta_n^{\rm can})^t=\zeta_n^{\rm TB2}$ ✓
- **原始冪根である**: $t\in\hat{\mathbb Z}^\times$ ゆえ全 $n$ で $\gcd(t,n)=1$ ✓
- **現行文面をすべて満たす**: (TB2) は「整合系を固定する」としか言わず、(1.6) は体生成元の像しか言わない ✓

このとき $\eta_n=\zeta_n^{\rm can}=(\zeta_n^{\rm TB2})^{t^{-1}}$ なので ($*$) は $\zeta_n^{\,\varepsilon}=\zeta_n^{\,t^{-1}}$、すなわち
$$ \boxed{\ \varepsilon\equiv t_{20}^{-1}\ (\mathrm{mod}\ 20),\qquad b_{\rm cmp}\ :=\ \varepsilon^{-1}\bmod10\ \equiv\ \bar t_{10}\ \ (\mathrm{mod}\ 10).\ } \tag{3.3} $$

**$t_{20}=3$ なら $\varepsilon\equiv7$、$b_{\rm cmp}=3$** — **便 48 の値と完全一致**(検査 4 で $(\mathbb Z/20)^\times$ の 8 元すべてを整数演算で再現。**便 49 F6.2 が型修理後 PASS**)。

> **★【v2 で得た一般形 (3.3)・v2.1 で $b_{\rm cmp}$ に確定・v2.2 で型修理】BFC (2.1) の帳簿量 $b_{\rm cmp}$ は、root-object のずれの $\bmod\ M$ 成分 $\bar t_M$ である($t_{2M}$ ではない — §3.5.1)。**
> **⚠【v2.1】これは (8.1) の捻れ指数 $b_{\rm op}$ とは別物である** — §3.5 で辞書を立てる。**反転経路が $\pm1$ でなく $(\mathbb Z/20)^\times$ 全体を生む**という §6 経路 8 の主張は $b_{\rm cmp}$ についてのものであり、$b_{\rm op}$ については**逆に何も動かない**(§3.5.2)。

---

## 3.5 【v2.1・V14 新設】二つの $b$ の辞書(裁定 55)

> **発端**: $B_{\rm FC}$ 著者(B-6 所有者)の検分の副産物。**countermodel の下で、私の (3.3) の $b$ と BFC (8.1) の捻れ指数が別物になる。** (Z20-link) の下では $t=1$ で両者は一致するので現行本文に矛盾はないが、**$t\ne1$ を許すと分岐する。**

### 3.5.1 定義と関係式

記号: $M\mid20$、$K=\mathbb Q(\zeta_{2M})$。$\zeta_{2M}^{\rm Rule1}$ は Rule 1 (1.5) の**体生成元**、$\zeta_{2M}^{\rm TB2}$ は (TB2) の根系の $2M$ 項。

> ### 【v2.2・V18】$t$ の型 —(便 49 F4.1 blocker の修理)
> $$ \boxed{\ t_{2M}\in(\mathbb Z/2M)^\times:\ \ \zeta_{2M}^{\rm TB2}=(\zeta_{2M}^{\rm Rule1})^{t_{2M}},\qquad \bar t_M:=t_{2M}\bmod M\in(\mathbb Z/M)^\times.\ } $$
> $$ \boxed{\ \textbf{(Z}_{2M}\textbf{-link)}\ \iff\ t_{2M}=1\ }\qquad\text{であって、}\quad \bar t_M=1\ \textbf{は link の必要十分条件ではない.} $$

> **⚠ v2.1 の誤り(自認・便 49 F4.1)**: v2.1 は $t\in(\mathbb Z/M)^\times$ を $\zeta_M^{\rm TB2}=(\zeta_M^{\rm Rule1})^t$ で定めた直後に「(Z20-link) $\iff t=1$」と書いた。**偽である。**
> **反例($K^{(5)}$ の実データ)**: $t_{20}=11$ とすると
> $$ \zeta_{20}^{\rm TB2}=(\zeta_{20}^{\rm Rule1})^{11}\ne\zeta_{20}^{\rm Rule1}\quad\text{(link は破れている)},\qquad\text{しかし}\quad \zeta_{10}^{\rm TB2}=(\zeta_{10}^{\rm Rule1})^{11}=\zeta_{10}^{\rm Rule1}\quad(\bar t_{10}=1). $$
> **これは $\ker\bigl((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times\bigr)=\{1,11\}$ そのものであり、Rule 1 §1.6 が「$b_i$ とは別の項目であり混同しない(便 31 F5.1)」と既に警告していた 2:1 である。** 私は正典の警告文をそのまま踏んだ。**自認。**(★教材 T8)

> **定義(二つの $b$).**
> $$ \textbf{(比較側)}\quad b_{\rm cmp}\ :=\ \varepsilon^{-1}\bmod M \qquad\bigl(\varepsilon:\ x=\iota(\sigma_\zeta^{\,\varepsilon}),\ \sigma_\zeta\ \text{は}\ \zeta^{\rm TB2}\ \text{で定義}\bigr)\qquad\text{— BFC (2.1)} $$
> $$ \textbf{(作用側)}\quad c_\Lambda\circ m(\xi)\circ c_\Lambda^{-1}\ =\ \tau\bigl(\xi^{\,b_{\rm op}}\bigr)\quad(\forall\xi\in\mu_M)\qquad\text{— BFC (8.1)/(8.2)} $$
> **型の違い**: $b_{\rm cmp}$ は「**$\pi_1$ の生成元 $x$ と (TB2) の根系が定める $\sigma_\zeta$ のずれ**」を測る。$b_{\rm op}$ は「**Kummer torsor の乗法 $m$ と、$\Lambda$ 上の共役作用 $\tau$(Rule 1 (1.8) で $\zeta_M^{\rm Rule1}\mapsto X$)のずれ**」を測る。$m$ は根系に依らず、$\tau$ は **Rule 1 側**に固定されている。**どちらも $\bmod\ M$ の量であり、$\bmod\ 2M$ の link を見ない**(これが上の反例の意味)。

> ### 命題 TB4-D(辞書)【**v2.2・V19 で named antecedents を掲示**】
> **前件(証明が実際に呼ぶもの・便 49 F4.2)**:
> **(D-i)** $x=\iota(\sigma_\zeta^{\,\varepsilon})$ と $\sigma_\zeta$ の **Kummer 作用**(補題 TB4-1 $=$ (TB4$^{\rm u}$)$+$(TB1) の繊維関手)、
> **(D-ii)** **$c_\Lambda$ の $x$-同変性**(系 B-4c。$K^{(5)}$ 版なら Rule 1 §4.3 の actual intertwiner)、
> **(D-iii)** Rule 1 (1.8) の **$\tau(\zeta_M^{\rm Rule1})=\tau(X)$ marking**。
> このとき
> $$ \boxed{\ b_{\rm op}\ =\ b_{\rm cmp}\cdot\bar t_M^{\,-1}\ =\ (\bar t_M\,\varepsilon)^{-1}\qquad(\mathrm{mod}\ M)\ } \tag{3.4} $$
> **$\varepsilon$ の値(したがって TB4-3)は使わない**が、**「定義だけから従う」ではない** — 上の (D-i)(D-ii)(D-iii) が要る(**v2.1 の「定義だけ」は過大だった。自認**)。

**証明(私の規約で再導出).** BFC 補題 B-6$^{\rm tw}$ の第 1・2 段を、二つの $\zeta_M$ を分離して書き直す。
1. (D-i) より $x$ の $\mathrm{Fib}$ 上の作用は $m\bigl((\zeta_M^{\rm TB2})^{\varepsilon}\bigr)=m\bigl((\zeta_M^{\rm Rule1})^{\bar t_M\varepsilon}\bigr)$。
2. (D-ii)$+$(D-iii) より $c_\Lambda\circ(x\text{ の作用})\circ c_\Lambda^{-1}=\tau(X)=\tau\bigl(\zeta_M^{\rm Rule1}\bigr)$。
3. ゆえに $c_\Lambda\, m\bigl((\zeta_M^{\rm Rule1})^{\bar t_M\varepsilon}\bigr)\,c_\Lambda^{-1}=\tau\bigl(\zeta_M^{\rm Rule1}\bigr)$。$\xi=(\zeta_M^{\rm Rule1})^{k}$ と置き $k=\bar t_M\varepsilon j$ とすると
$$ c_\Lambda\,m(\xi)\,c_\Lambda^{-1}=\tau\bigl((\zeta_M^{\rm Rule1})^{j}\bigr)=\tau\bigl(\xi^{(\bar t_M\varepsilon)^{-1}}\bigr). $$
よって $b_{\rm op}=(\bar t_M\varepsilon)^{-1}=b_{\rm cmp}\,\bar t_M^{-1}$。∎(**検査 5(a)**: $\varepsilon,t_{2M}$ を $(\mathbb Z/20)^\times$ 全体に走らせた **64 対**で確認)

> **系 TB4-D′.** TB4-3 の $\varepsilon\equiv t_{2M}^{-1}\ (\mathrm{mod}\ 2M)$ を代入すると $\bar t_M\varepsilon\equiv1\ (M)$、ゆえに
> $$ \boxed{\ b_{\rm cmp}\equiv\bar t_M,\qquad b_{\rm op}\equiv1\quad(\mathrm{mod}\ M)\ \ \text{— $b_{\rm op}$ は $t_{2M}$ に依らない.}\ } \tag{3.5} $$
> **(検査 5(b): 8 元悉皆で確認。$B_{\rm FC}$ 著者の整数演算と一致。)**

### 3.5.1a 【v2.2 新設・**v2.3 で表示修文**】四段のはしご — 条件鎖と結論鎖を分ける

> **⚠ v2.2 の表示の欠陥(自認・便 50 F3.2)**: v2.2 は 1 枚の表に**条件・結論・定理名を同じ列で混ぜ**、行間に含意矢印を置かなかった。**数学的骨格は便 50 F3.1 が支持したが、表示は差し戻し。** また TB4-E を「**無条件**」と呼んだのは**過大**である — **「無条件」は空の前件を意味する**(★教材 T11)。正しくは **root-link-free(ただし (E-i)–(E-iv) に相対的)**。

**共通前件(package)**: 以下すべて、**命題 TB4-D の (D-i)–(D-iii)・命題 TB4-E の (E-i)–(E-iv)・定理 TB4-3** を共通に固定した下での話である。

**四つの言明**
$$ \begin{array}{ll}
\textbf{L1}: & b_{\rm op}=1\\
\textbf{L2}: & b_{\rm cmp}=1\iff\bar t_M=1\\
\textbf{L3}: & \varepsilon\equiv1\ (\mathrm{mod}\ 2M)\iff t_{2M}=1\\
\textbf{L4}: & \varepsilon=1
\end{array} $$

**条件鎖**(規約 seal の強さ):
$$ \boxed{\ \textbf{(Z-norm)}\ \Longrightarrow\ \textbf{(Z}_{2M}\textbf{-link}:\ t_{2M}=1\textbf{)}\ \Longrightarrow\ \bigl(\bar t_M=1\bigr)\ } \tag{3.6} $$

**結論鎖**(得られる等式の強さ):
$$ \boxed{\ \varepsilon=1\ \Longrightarrow\ \varepsilon\equiv1\ (\mathrm{mod}\ 2M)\ \Longrightarrow\ b_{\rm cmp}=1,\qquad\text{他方}\quad b_{\rm op}=1\ \text{は{\bf 命題 TB4-E により root-link-free}}\ } \tag{3.7} $$

> **⇒ 共通 package の下では $\textbf{L4}\Rightarrow\textbf{L3}\Rightarrow\textbf{L2}\Rightarrow\textbf{L1}$、そして各逆向きは下の witness により偽である。**

**逆向きを断つ witness(3 本)**

| 断つ含意 | witness | 内容 |
|---|---|---|
| $\textbf{L1}\nRightarrow\textbf{L2}$ | $M=10,\ t_{20}=3$ | TB4-3 下で $b_{\rm op}=1$ だが $b_{\rm cmp}=3$(検査 5(b)) |
| $\textbf{L2}\nRightarrow\textbf{L3}$ | $M=10,\ t_{20}=11$ | $\bar t_{10}=1$ だが $t_{20}\ne1$(**§3.5.1 の反例**・検査 5(d)) |
| $\textbf{L3}\nRightarrow\textbf{L4}$ | **$\hat{\mathbb Z}^\times$ の unit**: $2$-進・$5$-進成分 $=1$、**$3$-進成分 $=-1$**、他の素点は $1$ | $\bmod\ 20$ では $1$ だが exact に $1$ ではない(**便 50 F3.1 提供**) |

> **★ 便 49 F4.1 の要点は「L2 と L3 を同じ欄に潰していた」ことである。** witness $t_{20}=11$ はちょうど **L2 を満たし L3 を満たさない**点であり、しかも **$b_{\rm cmp}$ も $b_{\rm op}$ も $1$ になるので $b$ の測定にも帳簿にも映らない**(§3.5.1b の negative fixture)。**seal の equality level($=2M$)と、定理が見る modulus($=M$)を同じ欄に潰してはならない。**
>
> **★ L3 $\nRightarrow$ L4 の witness の役割**: これは **(Z$_{2M}$-link) を凍結しても exact $\varepsilon=1$ は戻らない**ことの具体例であり、**`Z20-link-seal/v1` を (Z-norm) の「一部凍結」と呼んではならない**(便 49 F6.5)理由を数学的に裏づける。

### 3.5.1b 【v2.3 新設】negative regression fixture(便 50 F4.2 / T-15 の full-tuple 形)

> **⚠ v2.2 の書き方の欠陥(自認・便 50 F4.2)**: v2.2 は (d′) を「$t_{20}=11$ ならば $b_{\rm cmp}=b_{\rm op}=1$」という**普遍含意**のように読める形で書いた。**$t_{20}=11$ だけからは $b_{\rm cmp}=1$ は出ない** — $\varepsilon\equiv t_{20}^{-1}\ (20)$(= TB4-3)の束縛が要る。**反例の全自由変数を束縛した fixture として保存する**(★教材 T12)。**checker の実装(`e = inv(t2bad,20)`)は初めからこの正しい読みだった**ので、修理は文書側だけである。

> ### negative regression fixture `NF-root-link/K5`
> $$ \boxed{\ \bigl(M,\ t_{20},\ \bar t_{10},\ \varepsilon,\ b_{\rm cmp},\ b_{\rm op},\ \text{Z20-link}\bigr)\ =\ \bigl(10,\ 11,\ 1,\ 11,\ 1,\ 1,\ \textbf{false}\bigr)\ } \tag{3.8} $$
> **束縛の出所**: $\varepsilon=11$ は TB4-3($\varepsilon\equiv t_{20}^{-1}$、$11^{-1}\equiv11\bmod20$)。$b_{\rm cmp}=\varepsilon^{-1}\equiv1\ (10)$、$b_{\rm op}=b_{\rm cmp}\bar t_{10}^{-1}=1$(命題 TB4-D)。
> **主張**: $$ \boxed{\ \text{「}b\ \text{が }1\ \text{だから root object も一致する」は }b_{\rm cmp},\ b_{\rm op}\ \textbf{のどちらで読んでも偽}.\ } $$
> **(便 50 F4.1 が独立再計算で一致・T-15 で採用。)**

> ### 同型 fixture `NF-root-link/K3`(便 50 F4.3)
> $$ \bigl(M,\ t_{12},\ \bar t_6\bigr)=\bigl(6,\ 7,\ 1\bigr),\qquad \ker\bigl((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times\bigr)=\{1,7\} $$
> **これは $K^{(3)}$ の既存判定を反転させる主張ではない** — **level $12$ の equality を level $6$ の指数から復元してはならない**という**型警告**である(便 50 F4.3)。

### 3.5.2 **$b_{\rm op}=1$ は (Z20-link) を要さない**(v2.1 の主たる新結果)

$t$ を経由せずに直接示せる。**この一段が「二つの $b$ を分ける」ことの実質的な価値である。**

> **命題 TB4-E**【**v2.2・V19 で前件を補填**】**.** $M\mid20$ とする。前件は
> **(E-i)** **補題 TB4-2 の orientation package**(A2, **A3**, C1, C5, C6, chosen $\bar\iota$)— **定理 TB4-3 全体は要らない**(A1$=$(TB4$^{\rm u}$) も $\varepsilon$ の形式も使わない・便 49 F4.4)、
> **(E-ii)** $\bar\iota|_K=\iota_\infty$(A12)$+$ Rule 1 (1.6)(1.7)(A6)、
> **(E-iii)** **$c_\Lambda$ の $x$-同変性 = 系 B-4c**(一般 BFC 版)**または Rule 1 §1.2–§1.5・§4.3 の actual marking / intertwiner**($K^{(5)}$ 版)、
> **(E-iv)** Rule 1 (1.8) の $\tau(\zeta_M^{\rm Rule1})=\tau(X)$ marking。
> このとき
> $$ \boxed{\ b_{\rm op}\ =\ 1 . } $$
> **(Z$_{2M}$-link) も (TB2) の根系も前件に現れない。**
>
> **⚠ v2.1 の誤り(自認・便 49 F4.4)**: v2.1 の前件表は A1–A3/C1/C5/C6/A12/A6/(1.8) だけを挙げ、**証明が呼ぶ (E-iii)($c_\Lambda$ の出所)を落としていた**。**証明が named object を呼んだら定理文の前件表にも出す** — ★教材 T9。逆に A1 は**使っていないのに載せていた**(過剰は偽ではないが、脱落は許されない)。

**証明.** 補題 TB4-2 より $x$ の作用は $m(\eta_M)$、$\eta_M=\bar\iota^{-1}(e^{2\pi i/M})$。A12 $+$ A6 より $\bar\iota(\zeta_M^{\rm Rule1})=\iota_\infty(\zeta_{20}^{\rm Rule1})^{20/M}=e^{2\pi i/M}$、ゆえに $\eta_M=\zeta_M^{\rm Rule1}$。他方 系 B-4c $+$ (1.8) より $c_\Lambda(x\text{ の作用})c_\Lambda^{-1}=\tau(\zeta_M^{\rm Rule1})$。よって
$$ c_\Lambda\,m\bigl(\zeta_M^{\rm Rule1}\bigr)\,c_\Lambda^{-1}\ =\ \tau\bigl(\zeta_M^{\rm Rule1}\bigr), $$
生成元で一致するから全 $\mu_M$ で $b_{\rm op}=1$。∎

> **★ なぜ根系が消えるか**: **(8.1) の両辺はどちらも「Rule 1 側 $+$ 幾何側」の量である** — $m$ は $\mu_M\subset K$ の乗法(根系の名前を使わない)、$\tau$ は (1.8) で $\zeta_M^{\rm Rule1}$ に固定、$x$ の作用は (1.6) の埋め込みと反時計回りで固定。**(TB2) の根系はこの等式のどこにも現れない。** 根系が現れるのは $\sigma_\zeta$ を経由する $b_{\rm cmp}$ のほうだけである。
>
> **⇒ 帰結(BFC 側へ)**: **BFC 補題 B-6 の結論 (8.1) 自体は (Z20-link) なしで成立する**(上の別証)。**(Z20-link)$=$(TB2′) が要るのは、BFC が (8.1) を $\sigma_\zeta$ 経由で証明する経路と、(2.1) の帳簿等式 $b=\varepsilon^{-1}$ のほうである。** BFC v2.6 の (TB2′) 前件化は正しい(**現行の証明経路には必要**)が、**結論の射程はそれより広い**ことを記録しておく。§8.8-7 で Sol に突合を依頼する。

### 3.5.3 Rule 1 (7.1) の測定値 $\hat b_i$ はどちらか(裁定 55 依頼 2)

> ### 判定: $\ \boxed{\hat b_i\ =\ b_{\rm op}}\ $ — **断定できる**($B_{\rm FC}$ 著者の見立てを支持・便 49 F4.3 で確定)。
>
> **前件(named antecedents)【v2.3・便 50 F2.2 で statement 直下へ掲示】**
> **(B-i)** $c_i=c_\Lambda$ — Rule 1 §4.3 / 系 B-4c の **actual intertwiner**(同じ source/target・同じ $\hat F_2$-同変性)。
> **(B-ii)** $\ell_i$ は **Rule 1 §1.1 の同じ** $x=[\gamma_0]$ が $\mathrm{Fib}_{\vec{01}}(W_0^{(i)})$ に誘導する作用である(**別の local generator の再定義ではない** — §8.9 の条文要請)。
> **(B-iii)** (7.1) 右辺の $\zeta_{10}$ は **Rule 1 field generator $\zeta_{20}^{\rm Rule1}$ の冪**((1.7))であり、(TB2) の根系ではない。
> **(B-iv)** $\tau_i$ は **Rule 1 (1.8) の marking** $\zeta_M^{\rm Rule1}\mapsto X$。
>
> **⚠ v2.2 の欠陥(自認・便 50 F2.2)**: 導出本文には (B-i)–(B-iv) を書いていたが、**statement 自体に前件欄がなかった**。**数学核の穴ではないが、TB4-E と同型の「証明本文にはあるが statement から落ちる」事故を残す**(★教材 T9)。

**導出.** Rule 1 (7.1) は $c_i\,\ell_i\,c_i^{-1}=\tau_i\bigl(\zeta_{10}^{\,\hat b_i}\bigr)$ である。三つの記号の型を一つずつ辿る。

1. **$c_i$** = §4.3 の一意な intertwiner $\mathrm{Fib}_{\vec{01}}(W_0^{(i)})\xrightarrow{\sim}\Lambda_i$ $=$ 系 B-4c の $c_\Lambda$。**同じ対象。**
2. **$\zeta_{10}$**(右辺)= Rule 1 (1.7) $\zeta_{10}:=\zeta_{20}^2$、すなわち **$\zeta_{10}^{\rm Rule1}$**(体生成元の冪)。**(TB2) の根系ではない。**
3. **$\ell_i$** = 「$P_0$ における惰性群($\cong\mu_{10}$・全分岐)の生成元で、**(1.6) の埋め込みの下で $\lambda$ の周りを反時計回りに一周する $\gamma_0$ に対応するもの**」。
 - **★教材 T5 の自己適用**: ここの「$\gamma_0$」が Rule 1 §1.1 の $\gamma_0$ と**同じ object か**を確かめる。§1.1 の $\gamma_0$ は「$U$($\beta$-線)の $0$ を反時計回りに一周する $\vec{01}$ 基点の単純ループ」、§7.1 の $\gamma_0$ は「$\lambda$ の周りを反時計回りに一周する $\gamma_0$」。**$\lambda$ は $U$ 上の座標 $\beta$ を値に取る Belyi 写像**なので、$\lambda=0$ のまわりのループ $=$ $\beta$-線の $0$ のまわりのループ。**同一文書・同一記号・同一定義で、実際に同じ object である。** ✓(今回は一致したが、確認を省かない。)
 - ゆえに $\ell_i$ $=$ $x=[\gamma_0]$ の $\mathrm{Fib}$ 上の作用 $\overset{\text{補題 TB4-2}}{=}m(\eta_{10})$。

これを (7.1) に入れ、命題 TB4-E の途中式 $\eta_{10}=\zeta_{10}^{\rm Rule1}$ を使うと
$$ c_\Lambda\,m\bigl(\zeta_{10}^{\rm Rule1}\bigr)\,c_\Lambda^{-1}\ =\ \tau_i\bigl((\zeta_{10}^{\rm Rule1})^{\hat b_i}\bigr). $$
$b_{\rm op}$ の定義式を $\xi=\zeta_{10}^{\rm Rule1}$ で読むと左辺 $=\tau_i\bigl((\zeta_{10}^{\rm Rule1})^{b_{\rm op}}\bigr)$。$\tau_i$ は単射(Rule 1 §7.1)だから $\hat b_i=b_{\rm op}$。∎

> **★ 構造的な理由(一行)**: **(7.1) は「(1.6) で固定した幾何」と「(1.8) で固定した $\tau$」を突き合わせるだけで、(TB2) の根系に一度も触れない。** だから測るのは $b_{\rm op}$ であって $b_{\rm cmp}$ ではない。

> ### ⚠【v2.1・V16】T-12 の先出し 1 の**理由づけ**を自己訂正する
> 対話帳 T-12 で私は「**(7.1) の $b_i$ 測定は (Z20-link) の代替にならない**」と書き、その根拠に「$t\equiv11\ (20)$ なら $b=1$ なので検出できない場合がある」を挙げた。**根拠が誤っていた**(その $b$ は $b_{\rm cmp}$ であって測定値ではない)。**正しくは、命題 TB4-E と (3.5) により**
> $$ \boxed{\ \hat b_i\ =\ b_{\rm op}\ =\ 1\quad\text{が}\ \textbf{すべての}\ t\ \text{で成り立つ}\ } $$
> **したがって (7.1) は root-object ずれ $t$ を「ある $t$ で検出できない」のではなく、構造的に一切検出できない**(検査 5(c))。**結論(測定は (Z20-link) の代替にならない)は不変で、むしろ強まる。自認。** 訂正は対話帳 T-13 で Sol に送る。

### 3.5.4 検出能力の対照表(amendment `b_value_i` の意味論へ)

> **⚠ v2.1 の誤り(自認・便 49 F4.5)**: v2.1 は「**8 経路中 7 本が $\hat b=9$ として可視・盲点は root-object の 1 本だけ**」と書いた。**どちらの数え方でも偽である。**

$\hat b_i=b_{\rm op}$ が**何を検出し何を検出しないか**を、§6 の反転経路ごとに書く($M=10$)。**便 49 F10.2 に従い suite を二分割する。**

**(A) finite operational orientation suite**(有限測定 $M\mid20$ の宇宙内・**7 経路**)

| §6 の経路 | $b_{\rm cmp}$ | $\hat b_i=b_{\rm op}$ | 判定 |
|---|---|---|---|
| 1 (C1) / 2 (C2) / 6 (C3) / 7 (A3) の反転 | $9$ | $9$ | **detected** |
| 3 (C5) 時計回り | $9$ | $9$ | **detected** |
| 4 (C4) $\iota_\infty$ 反転 | $9$ | $9$ | **detected**(検査 5(d)) |
| **8 root-object ずれ $t_{2M}$** | $\bar t_M$ | **$1$(全 $t_{2M}$)** | **root-link blind** |

$$ \boxed{\ \text{期待値: } \textbf{6 detected / 1 root-link blind}\ } $$

**(B) profinite root-normalization suite**(**1 経路**)

| §6 の経路 | 判定 |
|---|---|
| **5 (C7) $n\nmid20$ の根の変更** | **finite $b$ measurement out-of-scope**(「検出できない」のではなく**測定宇宙に入っていない**) |

**⇒ 数え方は 2 通りある。母数を必ず明記すること**:
$$ \text{8 経路を母数: }\ \mathbf{6/8}\ \text{可視・}2/8\ \text{不可視}\qquad\text{finite 射程 7 経路を母数: }\ \mathbf{6/7}\ \text{可視・}1/7\ \text{盲点} $$

> **⚠ この表は「単一 axis の代表例」であって全 counterfactual の悉皆ではない**(便 49 F6.4)。**複数反転の合成は含まない。** ゆえに「8 本ですべて」とは書かず、**single-axis regression set** と呼ぶ。**検査 6 はこの数え(6/1/1)を機械で検査する**が、**網羅性そのものは検査していない** — **checker の 37/37 は regression lint であって網羅証明ではない**(便 49 F4.5・便 50 F5-2)。

> **⇒ 運用への含意(便 49 F5 の裁定を反映)**: **amendment の `b_value_i` は $b_{\rm op}$ と確定**(`b_semantics="op"` を固定値)。それは向き・埋め込み・比較の事故を検出するが、
> $$ \boxed{\ \text{(7.1) は (Z}_{2M}\text{-link) の代替でないだけでなく、\textbf{(Z-norm) 全体の certificate にもならない}.}\ } $$
> 前半は path 8、後半は path 5 による。**したがって root seal は測定と独立に凍結するほかない**(§8.1・`Z20-link-seal/v1`)。**$b_{\rm cmp}$ を記録したいなら根系 ID 付きの別欄でのみ許す**(§8.6)。
>
> **★ さらに強い形(検査 5(d′))**: negative fixture $t_{20}=11$ では **$b_{\rm cmp}=b_{\rm op}=1$** である。すなわち **$b$ の測定でも帳簿でも link 破れは映らない**。**「$b$ が 1 だから根も合っている」は成立しない。**

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

## 5. 補題 B-6 の $b_{\rm op}=1$ に必要な exact 形は出るか(委嘱 (iv))【**v2.2 で $b$ を型付け**】

### 5.1 出る — **ただし (Z20-link) の下で**【v2 で条件を明記】

補題 B-6 の証明第 1 段「$x\cdot p=m(\zeta_M)p$」に対し、本稿の補題 TB4-2 は **exact (TB4) を経ずに直接** $x\cdot p=m(\eta_M)p$ を与える。定理 TB4-A20 により、**(Z20-link) の下で** $M\mid20$ なら $\eta_M=\zeta_M$ である。

$$ \boxed{\ \text{(Z20-link)}+\text{A1--A3}+\text{(C1)(C5)(C6)}+\text{chosen }\bar\iota\ \Longrightarrow\ M\mid20\ \text{の窓で }\varepsilon\equiv1\ (M)\ \text{と }b_{\rm cmp}=1 . } $$

$K^{(5)}$ は $M=10\mid20$ なので該当する。**v1 は前件から (Z20-link) と A3 を落としていた。自認。**

> **【v2.1・V15 で射程を精密化】上の $b$ は $b_{\rm cmp}$ である。** **補題 B-6 の結論 (8.1) そのもの($=b_{\rm op}=1$)は、(Z20-link) なしで成立する**(命題 TB4-E)。整理すると:
> $$ \begin{array}{lll} \textbf{(8.1)}\ (b_{\rm op}=1) & \Longleftarrow & \text{A1--A3}+\text{(C1)(C5)(C6)}+\text{A12}+\text{A6}+\text{Rule 1 (1.8)}\quad(\textbf{(Z20-link) 不要})\\ \textbf{(2.1) の帳簿等式}\ (b_{\rm cmp}=1) & \Longleftarrow & \text{上}+\textbf{(Z20-link)}\\ \textbf{exact }\varepsilon=1 & \Longleftarrow & \text{上}+\textbf{(Z-norm)} \end{array} $$
> **⇒ 橋の式 (9.1) が要求するのは第 1 行だけ**なので、**$K^{(5)}$ の運用は (Z20-link) が凍結される前でも (8.1) の水準では立つ**。ただし BFC の**現行の証明経路**は $\sigma_\zeta$ を経由するので (TB2′)$=$(Z20-link) を要する — **BFC v2.6 の前件化は現行証明に対して正しい**(§3.5.2 末)。

### 5.2 それでも Rule 1 §7 の測定規律は緩めない

Rule 1 §7.4「$b_i=1$ を仮定してはならない。必ず (7.1) を計算して記録する」を**一切緩めない**。修文案は §8.4(便 48 F10.2 の文言を採用)。

### 5.3 射程の限界 — $M\nmid20$ の窓は未決(UNKNOWN)

$K^{(3)}$ 回帰は $M=6$、$K=\mathbb Q(\zeta_{12})$、$6\nmid20$、$\zeta_6\notin\mathbb Q(\zeta_{20})$。**Rule 1 (1.6) はこの窓の埋め込みを凍結していない。**

- 現状の正典は `docs/manifest_k5_appendixA_v1.md` §2 K3 行が「生成元の向きの曖昧さは判定にも固定体にも影響しない」と**無害宣言**しており、$K^{(3)}$ の既存判定は本稿の影響を受けない。
- $\iota_{12}(\zeta_{12}^{\rm Rule1})=e^{2\pi i/12}$ と対応する **(Z$_{12}$-link)**($t_{12}=1$・$2M=12$ 水準の等式)を凍結すれば $\varepsilon\equiv1\ (12)$、$b_{\rm cmp}=b_{\rm op}=1$。**無償だが現時点では凍結文がないので UNKNOWN。**
- **【v2.2】$K^{(3)}$ でも $2M=12$ と $M=6$ の水準を混同しないこと**: $\ker\bigl((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times\bigr)=\{1,7\}$ が非自明なので、**$K^{(5)}$ と同型の落とし穴がそのまま存在する**(★教材 T8)。
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
| **8** | **【v2 追加・v2.2 で型修理】root-object ずれ** — $\zeta_{20}^{\rm TB2}=(\zeta_{20}^{\rm Rule1})^{t_{20}}$、$t_{20}\in(\mathbb Z/20)^\times$ **任意** | $\varepsilon\equiv t_{20}^{-1}\ (20)$、**$b_{\rm cmp}\equiv\bar t_{10}$** — $b_{\rm cmp}$ は $\{1,3,7,9\}$ **全体**を取る。$t_{20}=3$ で $b_{\rm cmp}=3$。**$b_{\rm op}=\hat b_i=1$(全 $t_{20}$)。$t_{20}=11$ では $b_{\rm cmp}=b_{\rm op}=1$ で両方が盲** | **UNKNOWN $\to$ `Z20-link-seal/v1` で閉じる**。**便 48 の具体的 countermodel**(§3.4・検査 4)。**測定 (7.1) では検出不能**(§3.5.4) |

> **★ この表は single-axis regression set である**(便 49 F6.4)。**単一 axis の代表例**であって、**複数反転の合成まで含む全 counterfactual の悉皆ではない**。**「8 本ですべて」とは書かない**(v1 の「全部列挙した」に続く 2 度目の射程過大を避ける)。
>
> **★ 符号の敏感性は本物である。** 8 経路のうち **1–4, 6 は凍結文で排除済、5, 7, 8 は未凍結**である。**v1 の「$\varepsilon=-1$ の枝は工房規約では立たない」は経路 1–4, 6 についてのみ正しく、経路 7, 8 については立ちうる。自認。**
>
> **★【v2.1・V15 / v2.2・V20 で数え直し】どの経路が測定 (7.1) に映るか**: 可視は **6 本**(1,2,3,4,6,7)、**不可視は 2 本** — **経路 8**(root-link blind)と **経路 5**($n\nmid20$ ゆえ**有限測定の射程外**)。母数 2 通りで **6/8**(全体)/ **6/7**(finite 射程)。**v2.1 の「8 中 7 可視」は偽。自認**(§3.5.4・検査 6)。

---

## 7. 用いた計算(全列挙・Rule 1 §0.4 の申告様式)

**本稿の証明は閉形式であり、機械計算に依存しない。** 以下は取り違え検出のための補助検査である。

**`search/tb4-monodromy-check.mjs`**(node・**tracked 現物**・**37/37 PASS**)【**v2.4 で path と件数を現物へ同期**】:

| 検査 | 内容 | 型 | 検証対象 |
|---|---|---|---|
| **1** | $w^n=\beta$ の反時計回り解析接続(離散連続分枝追跡・4000 ステップ)。$n=2,3,5,6,10,12,20$ で置換 $j\mapsto j+1$ | 浮動小数点 | 補題 TB4-2 の独立再現(閉形式の持ち上げを使わない) |
| **2** | 局所 Kummer $\lambda=u\,s^M(1+c_1s+c_2s^2)$ の正規化 uniformizer $\tilde s=s\,h(s)^{1/M}$ が反時計回りで**厳密に $\zeta_M$ 倍**($M=5,6,10$・機械精度 $\sim10^{-16}$)。生の $s$ は $O(|s|)$ ずれる | 浮動小数点 | BFC 補題 B-5(iii) $+$ B-6 第 1 段の幾何側からの確認 |
| **3** | 時計回りで標識が $0\mapsto n-1$($n=5,10,20$) | 浮動小数点 | §6 経路 1–3, 6 の符号敏感性 |
| **4** | **【v2 追加】root-object ずれ $t\in(\mathbb Z/20)^\times$ の 8 元すべてで $\varepsilon\equiv t^{-1}\ (20)$・$b_{\rm cmp}\equiv t\ (10)$。$t=3\Rightarrow\varepsilon\equiv7,\ b_{\rm cmp}=3$** | **整数演算のみ** | **便 48 F7.2 countermodel の独立再現**(§3.4)$+$ 一般形 (3.3) の発見 |
| **5** | **【v2.1 追加・v2.2 で型修理・`TB4-b-dictionary/v1` の invariant 4 本】(a) $b_{\rm op}=b_{\rm cmp}\cdot\bar t_M^{-1}$ を **$\varepsilon,t_{2M}$ 任意の 64 対**で(TB4-3 を仮定しない)/ (b) TB4-3 下で $b_{\rm cmp}\equiv\bar t_M$・**$b_{\rm op}\equiv1$(全 $t_{2M}$)** / (c) `Z2M_link` $\Rightarrow t_{2M}=1$ / **(d) NEGATIVE fixture: $\bar t_M=1\nRightarrow$ `Z2M_link`($M=10,\ t_{20}=11$)**+**(d′) その fixture で $b_{\rm cmp}=b_{\rm op}=1$** | **整数演算のみ** | **命題 TB4-D / D′ / E**(§3.5)・**§3.5.1 の型分離**(便 49 F10.1) |
| **5(d)(d′)(e)** | **【v2.3 で full-tuple 化】(d) `NF-root-link/K5`$=(M,t_{20},\bar t_{10},\varepsilon,b_{\rm cmp},b_{\rm op},\text{link})=(10,11,1,11,1,1,\textbf{false})$ を**タプル一致**で検査($\varepsilon$ は TB4-3 で束縛 — 普遍含意ではない)/ (d′) 同 fixture で $b_{\rm cmp}=b_{\rm op}=1$ かつ link$=$false / **【v2.4 で強化】(e) $\ker((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times)=\{1,7\}$ を units 列挙で完全一致検査**/ (e′) `NF-root-link/K3`$=(6,7,1)$ かつ $t_{12}\in\ker\smallsetminus\{1\}$ / **(f) $\ker((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times)=\{1,11\}$**(同上)/ (f′) $t_{20}=11$ がその非自明元 | **整数演算のみ** | **§3.5.1・§3.5.1b**(便 50 F4.2 / T-15・**便 51 F4 のラベル過大解消**)。**(d)(d′) の実計算は v2.2 から不変** |
| **6** | **【v2.2 追加・3 項目】single-axis regression set の二分割: **finite operational orientation suite**(7 経路・期待 **6 detected / 1 root-link blind**)/ **profinite root-normalization suite**(経路 5・期待 **out-of-scope**)/ 母数 8 での数え(**6/8 可視・2/8 不可視 — 「7/8」は偽**) | **整数演算のみ** | **§3.5.4 の検出表**(便 49 F4.5・F10.2)。**⚠ 数えを検査するだけで網羅性は検査していない** |

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

- **(iii) 単独でも有限レベル(定理 TB4-A20)には足りる** — $M\mid20$ の窓だけを運用するなら先に凍結する選択肢がある(便 48 F7.2)。**ただし §3.3 の profinite 結論には (ii) 全体が要る。**
- **【v2.2・V22 / 便 49 F6.5】先行凍結するときは独立 ID `Z20-link-seal/v1` とし、「(Z-norm) の一部凍結」とは呼ばない。** Rule 1 / TB4 / $B_{\rm FC}$ / 結果 record が**同じ root IDs と equality certificate digest** を参照しなければならない。**一般定理の (Z$_{2M}$-link) と $K^{(5)}$ の (Z20-link) も別物として台帳化する**(便 49 F8-4)。
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

### 8.6a 【v2.2・V21】`TB4-b-dictionary/v1`(便 49 F10.1 を採用)

$b$ の意味論を機械可読にする**別 schema**。上の comparison-seal と対で運用する。

```text
TB4-b-dictionary/v1
  modulus_2M                                   # = 20 for K^(5)
  root_system_tb2_id                           # (TB2) の根系の識別子
  rule1_root_2M_id                             # K の体生成元 ζ_{2M}^Rule1 の識別子
  root_twist_2M_value                          # t_{2M} ∈ (Z/2M)^×   ← link はこの水準
  root_twist_mod_M_value                       # t̄_M = t_{2M} mod M  ← b はこの水準しか見ない
  epsilon_cmp_value                            # ε mod 2M
  b_cmp_value                                  # = ε^{-1} mod M
  b_op_value                                   # = b_cmp · t̄_M^{-1} mod M
  b_dictionary_proof_id                        # 命題 TB4-D
  b_value_i = b_op_value                       # Rule 1 (7.1) の測定値(F4.3 で確定)
  b_semantics = "op"                           # 固定値。既定値への fallback 禁止
  # ---- v2.3・便 50 F8.2 で追加 ----
  root_normalization_level = none | mod_M | level_2M | profinite
```

**`root_normalization_level` に許される結論(§3.5.1a の四段と 1:1)【v2.3・F8.2 採用】**:
```text
none       -> b_op = 1 only          # 命題 TB4-E(root-link-free)          = L1
mod_M      -> b_cmp = 1              # t̄_M = 1                             = L2
level_2M   -> epsilon = 1 mod 2M     # (Z_{2M}-link): t_{2M} = 1・定理 TB4-A20 = L3
profinite  -> epsilon = 1            # (Z-norm)・定理 TB4-B                  = L4
```

> **★ この enum の効き目**: **四段のはしごを prose ではなく schema に載せることで、L2 と L3 の同欄圧潰を機械が拒否できる**(便 50 F8.2)。`mod_M` を宣言した record が $\varepsilon\equiv1\ (2M)$ を主張したら fail-closed で止まる — **v2.2 の blocker と同型の事故が二度と通らない。**

**checker invariant(検査 5)**:
```text
b_cmp = epsilon_cmp^{-1} mod M
b_op  = b_cmp * root_twist_mod_M^{-1} mod M
Z2M_link_pass => root_twist_2M = 1
root_twist_mod_M = 1 !=> Z2M_link_pass        # NEGATIVE fixture: M=10, t_20=11
```

> **★ `root_twist_2M` と `root_twist_mod_M` を別欄にする理由が本 version の核心である**: **link は $2M$ 水準の等式、$b$ は $M$ 水準の量**。一つの欄に潰すと $t_{20}=11$ が「$t=1$」として通ってしまう(§3.5.1 の反例・検査 5(d))。**`root_twist_mod_M=1` から `(Z$_{2M}$-link)` を推論してはならない**(便 49 F4.6)。
>
> **【v2.1・V14 / v2.2 で強化】$b$ 欄を割る理由**: $b_{\rm op}$ と $b_{\rm cmp}$ は $\bar t_M\ne1$ で別の値になる(命題 TB4-D)。**$b_{\rm cmp}$ は `root_system_tb2_id` を伴わなければ定義すらできない**($\zeta^{\rm TB2}$ がなければ $\varepsilon$ が定まらない)。**`b_semantics` に既定値を置くことを禁止する**(未指定なら fail-closed)— Rule 1 v1.3 §F2 の「三値 enumeration の既定値 fallback で live な枝が黙って消えた」と同じ事故型。

### 8.7 【v2・V12】amendment を削ってはならない(便 48 F11)

**TB4-A20/TB4-B が成立しても、amendment の次の規律を削ってはならない**:

- Freeze 1 で rule を事前コミット / Freeze 2 で actual $b_i$ を $u$・$G_K$ 観測**前**に記録 / 観測後 fitting と $\exists b$ PASS の禁止 / $b_i\ne1$ の integrity quarantine 送り。

$$ \boxed{\ \textbf{定理があることは、実装がその定理の規約を実現したことを保証しない。}\ } $$

### 8.8 【**v2.2: 旧 7 問は便 49 F6 で全問回答済み**】

> | 問 | 便 49 の判定 | 本稿の同期先 |
> |---|---|---|
> | 1 TB4-A20 前件 | **PASS**($\bar\iota|_K$・(Z20-link)・(1.6) の別立ては正しい)。結論の $b$ は $b_{\rm cmp}=b_{\rm op}=1$ と型付けせよ | §3.2 |
> | 2 (3.3) | **PASS**($t_{20}$ を使えば正しい) | §3.4 |
> | 3 BFC 波及 | **PASS**(B-6 第 3 段が link を使う)。「結論の最小前件」と「現行 proof artifact の前件」を**分けて台帳化**せよ | §3.5.2 末・§4.4 |
> | 4 8 経路 | **FAIL** → 数え直し・**single-axis regression set** と改称 | §3.5.4・§6 |
> | 5 先行凍結 | **条件付き PASS** → 独立 ID **`Z20-link-seal/v1`** | §8.1 |
> | 6 $\hat b_i$ | **PASS**($\hat b_i=b_{\rm op}$ **確定**・`b_value_i`$=b_{\rm op}$)。$\ell_i$ と $x=\gamma_0$ の同一性を **Rule 1 v1.4 の条文にも明記**せよ | §3.5.3・§8.9 |
> | 7 TB4-E | **定理文修理を条件に PASS** → 前件補填済。**別 proof ID として射程を記録**せよ | §3.5.2 |

### 8.9 【v2.2 新設】Rule 1 v1.4 への条文要請(便 49 F6.6)

$\hat b_i=b_{\rm op}$ の根拠は (B-ii)、すなわち「$\ell_i$ と $x=[\gamma_0]$ が**同じ対象**である」ことである。**この同一性を Rule 1 v1.4 の条文に明記されたい** — さもないと ★教材 T5 の言う「同じ glyph」に戻り、次の版で再び typed equality が失われる。

> **⚠ v2.2 の条文案の欠陥(自認・便 50 F5-4)**: v2.2 案「$\lambda$ の値域が $U$ の座標 $\beta$-線であることによる」は**意図は読めるが、map・base・接基点を一つの typed equality にしていない**。**★教材 T5 に耐えない。** 便 50 の推奨文へ差し替える。

> **Rule 1 §7.1 追記案(v2.3・便 50 F5-4 の型)**:
> 「Rule 1 §1.1 の底を $U_\lambda=\mathbf P^1_\lambda\smallsetminus\{0,1,\infty\}$ と書き、TB4/$B_{\rm FC}$ の $U_\beta$ と**座標同型 $\beta=\lambda$ により、接基点 $\vec{01}$・標準向き・ループ $\gamma_0$ を保って同一視する**。§7.1 の $\ell_i$ は、この**同じ** $x=[\gamma_0]$ が $\mathrm{Fib}_{\vec{01}}(W_0^{(i)})$ に誘導する permutation であり、**別の local generator を再定義したものではない**。」

### 8.10 Sol への突合依頼(**v2.2 の新規部分のみ**)

1. **§3.5.1a の四段のはしご (L1)–(L4)** — 型分離を私なりに整理したもので便 49 にはない形。**(L2) $\nRightarrow$ (L3)** という要点が正しく表現できているか。
2. **§3.5.4 の suite 二分割**が F10.2 の意図どおりか(期待値 `6 detected / 1 root-link blind` と `out-of-scope`)。
3. **検査 5(d′)**($t_{20}=11$ で $b_{\rm cmp}$ と $b_{\rm op}$ の**両方**が $1$)— 便 49 は (d) までを指定した。**(d′) は本稿の追加**で、「$b$ が $1$ だから根も合っている」という推論を封じる直接の反例になる。この強化が正しいか。
4. §8.9 の Rule 1 条文案の書きぶり。

---

### ~~8.8(旧)~~ v2 時点の突合依頼(**上記で回答済み・記録として残す**)

1. **§3.2 定理 TB4-A20 の前件**が過不足ないか(とくに $\bar\iota|_K=\iota_\infty$ を (Z20-link) と別立てにした点)。
2. **§3.4 の (3.3)** — 便 48 の $t=3$ の値は再現したが、一般形は本稿の新規主張。**→ 便 49 F6.2 で PASS**($t_{20}$ を使えば正しい)。
3. **§4.4 の $B_{\rm FC}$ 側への波及の見立て**(補題 B-6 の証明が (Z20-link) を暗黙に使っているという読み)が正しいか。**もし正しければ $B_{\rm FC}$ v2 の前件欄も 1 行増える。**
4. §6 の反転表 — **8 経路でまだ不足がないか**(v1 は「全部」と言って外した)。
5. §8.1 の seal を **(iii) だけ先に凍結する**運用(finite だけ先行)に危険がないか。
6. **【v2.1】§3.5.3 の判定 $\hat b_i=b_{\rm op}$** — 私は断定したが、依拠したのは (a) $c_i=c_\Lambda$(Rule 1 §4.3 $=$ 系 B-4c)、(b) (7.1) 右辺の $\zeta_{10}$ が (1.7) の**体生成元**であること、(c) $\ell_i$ が §1.1 の $\gamma_0$ のモノドロミーであること、の 3 点である。**(c) は「同一文書内で同じ記号 $\gamma_0$」という読みを含む**ので、★教材 T5 に照らして第三者確認を求めたい(私は $\lambda$ の値域が $\beta$-線であることから同一と判断した)。**amendment の `b_value_i` の意味論に直結する**(裁定 55・便 49 の裁定事項)。
7. **【v2.1】命題 TB4-E**($b_{\rm op}=1$ が (Z20-link) を要さないこと)— **もし正しければ、BFC v2.6 の (TB2′) 前件化は「現行証明経路には必要だが結論の射程はより広い」**という位置づけになる。**BFC の前件欄を弱めるべきだとは主張しない**(現行の証明は $\sigma_\zeta$ を経由する)が、**射程の記録**は残す価値があると考える。誤読なら早く潰したい。

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
> ### ★教材 T8(**v2.2 新設**・便 49 F9-1): **剰余へ射影した unit は、元の root equality を証明しない**
> $\bar t_{10}=1$ でも $t_{20}=11$ は残る。**seal の equality level($=2M$)と、定理が見る modulus($=M$)を同じ欄に潰してはならない。**
> **⇒ 自認の重み**: $\ker\bigl((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times\bigr)=\{1,11\}$ は **Rule 1 §1.6 が「$b_i$ とは別の項目であり混同しない」と名指しで警告していた**。私は**正典が警告している当の落とし穴に、その警告文を読んだ上で落ちた**。★教材 T1 が言う「凍結文どうしを突き合わせよ」は、**警告文にも適用しなければならない**。
> **⇒ 検出法**: 「$X\bmod m$ が $1$」から「$X$ が $1$」を結論していないか、**射影の核が自明かを毎回明示せよ**。

> ### ★教材 T11(**v2.3 新設**・便 50 F7-5): **「無条件」は空の前件を意味する**
> 「**root-link を使わない**」と「**何も仮定しない**」は別である。命題 TB4-E は前者であって後者ではない((E-i)–(E-iv) に相対的)。
> **⇒ 語の規律**: 定理を「無条件」と呼んでよいのは前件表が空のときだけ。**「$X$ を使わない」と言いたいときは「$X$-free(ただし $\{$前件$\}$ に相対的)」と書く。** 本稿は該当箇所を全置換した(V24)。
> **⇒ ★教材 T2 の系**: 規約表の「対の整合の相手」欄が空でも、それは「無条件」ではなく「**その軸について**自由」にすぎない。

> ### ★教材 T12(**v2.3 新設**・便 50 F7-3): **negative fixture は入力 1 個ではなく反例の全自由変数を束縛する**
> $t_{20}=11$ **だけ**では $b_{\rm cmp}=1$ は出ない — $\varepsilon=11$(TB4-3 による束縛)と link$=$false を含めて初めて (d′) になる。
> **⇒ 事故の型**: 反例を「入力 1 個 $\Rightarrow$ 出力」の**普遍含意**の形で書くと、**実際には成り立たない含意を主張してしまう**(本稿 v2.2 がそう書いた)。**⇒ negative fixture は必ずタプル全体+導出 proof-ID で保存し、checker もタプル一致で検査する。**
> **★ 自己観察**: 今回**実装(checker)は初めから正しい読み($\varepsilon$ を `inv(t2bad,20)` で束縛)で、文書だけが緩い含意形になっていた。** ★教材 T9 の逆向きの事故 — **「証明本文にはあるが statement から落ちる」だけでなく、「実装にはあるが文書が緩い」も起きる。**

> ### ★教材 T9(**v2.2 新設**・便 49 F9-2): **proof が named object を呼んだら、theorem statement の前件表にも出す**
> 命題 TB4-E の最終行が正しくても、**$c_\Lambda$ の出所を前件から落とせば theorem gate は閉じない**。付録 A の一覧に載っていることは前件掲示の代替にならない。
> **⇒ 逆向きの非対称性**: **前件を強く置きすぎるのは偽ではない**(TB4-E に A1 を載せていたのは無害)が、**使う前件を落とすのは許されない**。**⇒ 定理を書き終えたら、証明の各行が呼ぶ named object を機械的に拾って前件表と差分を取る。**

> ### ★教材 T10(**v2.2 新設**・便 49 F9-3): **有限 diagnostic は profinite normalization の証明書にならない**
> 経路 5($n\nmid20$ の根)は $M=10$ の測定に映らない。**これは「盲点」ではなく「測定宇宙に入っていない」**。両者を混ぜて数え直し「$7/8$ 可視」としたのが v2.1 の誤りである。**検査対象外を分母から落として検出率を上げてはならない** — regression 表は **finite suite** と **profinite suite** に分ける(§3.5.4・検査 6)。

> **⇒【v2.1 追記】同じ検出法を「同名の量」にも適用せよ**: T5 の初出は object($\zeta_{20}$)についてだったが、**裁定 55 が示したのは「同名の**量**」でも同じ事故が起きる**ことである — $b$ という 1 文字が、**$b_{\rm cmp}$(根系との比較)と $b_{\rm op}$($m$ と $\tau$ の捻れ)という別の量**を指していた。(Z20-link) の下では一致するので、**正しい規約のもとでは永久に見えない**。**⇒ 量にも型を付け、seal に `b_semantics` のような判別欄を必須(既定値禁止)で持たせる**(§8.6)。**「一致している間は区別が要らない」は、規約が壊れた瞬間に最も高くつく。**

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
| **TB4-A20** | **$\varepsilon\equiv1\ (20)$**、$M\mid20$ で $b_{\rm cmp}=b_{\rm op}=1$ | TB4-3 $+$ **A10 (Z20-link)** $+$ A6, A7 | 検査 1・4 | **便 50 F2.1 で型修理後 PASS**(two-mathematician 前) |
| **TB4-B** | **$\varepsilon=1$**($=$ exact (TB4)) | TB4-3 $+$ **A11 (Z-norm)** | — | 便 48 **条件付き PASS** |
| **(3.3)** | root-object ずれで $\varepsilon\equiv t_{20}^{-1}(20)$、**$b_{\rm cmp}\equiv\bar t_{10}\ (10)$** | TB4-3 | **検査 4**(8 元悉皆) | **便 49 F6.2 で PASS**($t_{20}$ を使えば正しい・型修理後) |
| **型分離** | **$t_{2M}\in(\mathbb Z/2M)^\times$ と $\bar t_M$ の分離・(Z$_{2M}$-link)$\iff t_{2M}=1$・$\bar t_M=1$ は不十分** | — | **検査 5(c)(d)**(negative fixture $t_{20}=11$) | **v2.2**(便 49 F4.1 blocker を受諾) |
| **TB4-D** | **辞書 $b_{\rm op}=b_{\rm cmp}\cdot\bar t_M^{-1}$** | **(D-i)(D-ii)(D-iii)**(§3.5.1・**「定義だけ」を撤回**) | **検査 5(a)**(64 対) | **便 49 F4.2 で PASS**(型修理後) |
| **TB4-D′** | TB4-3 下で $b_{\rm cmp}\equiv\bar t_M$、**$b_{\rm op}\equiv1$(全 $t_{2M}$)** | TB4-D + TB4-3 | **検査 5(b)**(8 元悉皆) | **便 49 F4.2 で PASS** |
| **TB4-E** | **$b_{\rm op}=1$ は (Z$_{2M}$-link) を要さない** | **(E-i)(E-ii)(E-iii)(E-iv)**(§3.5.2・**$c_\Lambda$ の出所を補填**) | 検査 5(b)(c) | **便 49 F4.4: 証明核 PASS / 定理文は v2.2 で修理** |
| **判定** | **$\hat b_i$(Rule 1 (7.1) の測定値)$=b_{\rm op}$** | §3.5.3 の (a)(b)(c) | 検査 5・6 | **便 49 F4.3 で確定**(`b_value_i`$=b_{\rm op}$・`b_semantics="op"`) |
| **検出表** | finite suite **6 detected / 1 root-link blind**、profinite suite **out-of-scope** | — | **検査 6** | **v2.2**(便 49 F4.5 の FAIL を受諾。**網羅性は未検査**) |
| **はしご L1–L4** | 条件鎖 (3.6) / 結論鎖 (3.7)・**L4⇒L3⇒L2⇒L1**・逆は witness 3 本で偽 | 共通 package(D/E/TB4-3) | 検査 5(b)(d) | **便 50 F3.1 で骨格 PASS / 表示は v2.3 で修文** |
| **`NF-root-link/K5`** | full tuple $(10,11,1,11,1,1,\textbf{false})$ — 「$b=1$ だから根も一致」は**どちらの $b$ でも偽** | TB4-D + TB4-3 | **検査 5(d)(d′)** | **便 50 F4.1 で PASS**(独立再計算一致・T-15 で採用) |
| **`NF-root-link/K3`** | $(6,7,1)$・$\ker\bigl((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times\bigr)=\{1,7\}$ | — | **検査 5(e)** | **便 50 F4.3 で PASS**(型警告であって K3 判定の反転ではない) |
| ~~「8 中 7 可視」~~ | ~~盲点は root-object の 1 本だけ~~ | — | — | **v2.2 で撤回**(便 49 F4.5) |
| ~~「(Z20-link)$\iff t=1$」~~ | ~~$t\in(\mathbb Z/M)^\times$~~ | — | — | **v2.2 で撤回**(便 49 F4.1 blocker) |
| ~~TB4-D「定義だけから従う」~~ | — | — | — | **v2.2 で撤回**(便 49 F4.2) |
| ~~TB4-A(a)~~ | ~~既存三文書だけで $\varepsilon\equiv1\ (20)$~~ | — | — | **v2 で撤回(便 48 F7.2 blocker B1)** |
| ~~T-12 先出し 1 の理由~~ | ~~$t\equiv11$ で $b=1$ ゆえ (7.1) は代替にならない~~ | — | — | **v2.1 で理由を訂正**(正しくは $\hat b_i=1$ が全 $t$ — 結論は不変・§3.5.3) |
