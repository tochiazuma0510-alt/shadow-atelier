# K⁽⁵⁾ 橋 D1 — 奇数族横展開の第一歩: $G_5$ の構造確定と $R^{\rm cyc}$ 前件判定(**v1.2 = 便 31 / 裁定 29 反映版**)

2026-07-27 起草・**同日 v1.1 改訂**・**同日 v1.2 micro 改訂**: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(第三例 = 奇数族・$n=5$)。研究者裁定(`docs/研究目的.md` 追記 3)に基づく。v1.1 は Sol 便 30(条件付き PASS)+ 裁定 26 を反映。v1.2 は Sol 便 31(F7.2・P10)+ 裁定 29 を反映した micro 修正のみ — 数学的結論は 1 ミリも動かない。**

## v1.1 → v1.2 差分表(**micro のみ・結論不変**)

| # | 箇所 | v1.1 | **v1.2** | 出所 |
|---|---|---|---|---|
| **E9** | §6.3.2 の補題 K5-a 証明 | $j_i(\tau_i(X^{2t}))$ と書いた — $j_i$ の domain は $\mu_{10}[5]$ なので**この形は ill-typed**($\tau_i(X^{2t})\in\mathrm{Sym}(\Lambda_i)$ を $j_i$ に食わせている) | **入力を $\zeta_{10}^{2t}\in\mu_{10}[5]$ に正す**(共通同定 $\iota:\mu_{10}\xrightarrow{\sim}\langle X\rangle,\ \zeta_{10}\mapsto X$ を明示)。結論の式は $\boxed{j_i(\zeta_{10}^{2t}) = \Phi_{0,-t}}$(= 便 31 (7.2))。**$a=1$ という結論と証明の骨格は不変** | 便 31 F7.2 / 裁定 29-8① |
| **E10** | §6.3.3 の前件 | 「$b$ を BRIDGE-IN に記録し $a$ を $ab^{-1}$ 型に**更新**する」 | **撤回**。formal invariant $a=1$ は**永久不変**で、更新するのは $a$ ではなく別欄の $b_{\rm sq},b_{\rm ns},a_{\rm eff}=b_{\rm ns}^{-1}ab_{\rm sq}$。正本は `docs/week4-K5_Rule1_v1.md` §4 | 便 31 F5 / **裁定 29-2**(司令塔自己訂正) |
| **E11** | §0(9 行結論)・§9.3 | C 系エスケープに壊された TeX 制御文字(`\rm`→`m`、`\times`→TAB+`imes`、`\boxed`→`oxed`、`\rho`→`ho`、`\rvert`→改行+`vert`)。§9.3 のものは**表のセル内で改行を起こし Markdown 表を壊していた** | **文字列のみ修理**(P10)。**数式・数値・判定は 1 文字も変えていない** | 便 31 P10 / 裁定 29-10 |

> **v1.2 が触れていないもの**: §1–§5・§7–§11 の全構造値、前件判定、二系統検算の結果、補題 Q と降下、命題 K5-1/K5-2/K5-2b。**hash 対象は人間向け Markdown と分離する**(裁定 29-10)— 本ファイルは人間向けであり、封印対象の canonical serialization ではない。

## v1 → v1.1 差分表

| # | 箇所 | v1 | **v1.1** | 出所 |
|---|---|---|---|---|
| **E1** | §5.4 | $\mathrm{inn}$ の規約を書かずに $\Phi_{0,k}=\mathrm{inn}(\bar x^{-2k})$ と述べた | **$\mathrm{inn}(g)(h) := ghg^{-1}$ を一行明記**。逆規約なら指数の符号だけ反転し、像と忠実性は不変であることも明記 | 便 30 F1.1・P1 / 裁定 26-1 |
| **E2** | §6.1 | $W_0$ を最初から「$\mathbf P^1_{\mathbb Q}\smallsetminus\{0,1,\infty\}$ の被覆」と書いた(**型が先走り**) | **$W_{0,\bar{\mathbb Q}}\to U_{\bar{\mathbb Q}}$ の幾何被覆と型付け**($U := \mathbf P^1_{\mathbb Q}\smallsetminus\{0,1,\infty\}$)。結論で初めて $\mathbb Q$-有理性を得る。Sol (3.1)–(3.3) の $\mathrm{Out}(P)$ 経由の書き方を採用 | 便 30 F3.1・P5 |
| **E3** | §6.2・§5.1 | (4b) は「PASS(紙上・**文献要請つき**)」 | **(4b) = 「PASS(紙上・両数学者)」へ昇格**。Sol F3.2 が Weil cocycle の自動成立を書き切ったため**数学的な穴は無い**。**(4d)(5′) は UNKNOWN のまま動かさない** | 便 30 F3.2 / 裁定 26-4 |
| **E4** | §6.2 | 【文献要請 1】= 要請中 | **【引用確定】Dèbes–Douai 1997 + Sijsling–Voight 2016**(`docs/文献ゲート_01_moduli_descent.md`)。**降下が与えるのは $\mathbb Q$-モデルの存在のみ — (4) を弱めない**の翻訳注意を明記 | 裁定 26-4・文献ゲート 01 |
| **E5** | §3.4・§10 | 「次標的は $n=24$」 | **$n=24$ は差戻し・次標的から外す**。**盲点定理 K5-2b**(便 30 (4.5)(4.6): $8\mid n$ で $\Phi_{0,n/4}=1$ ⇒ $\ker\rho_0\supseteq C_2$)を新設し、$K^{(n)}$ 族の repeated-primary を**一律 SCHEMA-OUT** に登録。$K^{(8)}$ は**負較正**。攻略分岐 2 本を将来課題へ | 便 30 F4.3 / 裁定 26-3 |
| **E6** | §4.5・§8.1 | 「2 つの dessin は非同型」 | **圏の明示**: 非同型は「**固定した $U$ 上の ordered dessin(cover over the fixed $U$)**」の意味。基底三点の置換を許す圏や曲線のみの粗い同値では**未分離** | 便 30 F2.1・W4 |
| **E7** | §6.3 | 整合ゲート = 「位数一致」 | **§6.3 を全面強化**: $a := j_{\rm ns}^{-1}j_{\rm sq}\in(\mathbb Z/5)^\times$ を**有限群論段で計算・封印**し、$[u_{\rm ns}^{-1}]_{10} = [u_{\rm sq}^{-1}]_{10}^{\,a}$ を主整合ゲートにする。**$a$ の値は本稿で確定**(§6.3・二系統) | 便 30 F2.3・P4 / 裁定 26-6 |
| **E8** | §9.3・§11・§12 | — | 【GAP】表・★教材(便 30 ★1 = 教材 14)・論点欄(便 30 の回答先を付記 + 便 31 への論点を新設) | — |

> **不変**: §2・§3.1–§3.3 の全構造値・§4.1–§4.4 の列挙と分裂・§5.1 の (0)(1)(2)(3a–d)(6′-i)(6′-ii) 判定・§5.3 の $\Phi$ 単射・§7 の B1–B5・§8 の dessin データ・全検算値。**v1.1 は構造確定値を 1 ミリも動かさない。**
> **係争の決着(裁定 26-2)**: $n=12$ は $(M,e,M/e)=(12,3,4)$ で **coprime** — 私の §3.4 が正しく、便 29 P7/W6 は Sol 本人の erratum(便 30 F4.2)。$n=12$ 欄は v1 のまま**変更しない**。

- 入力(正典と工房内のみ): `docs/notes/抽出_Kn定義_D1.md`((3.1)(3.4)(3.6)・Prop 3.4/3.5/3.6・Thm 4.3 (4.9)(4.12)・Thm 4.6 (4.23))/ `docs/week4-K3飽和_opus_v3.md`(型付け $R^{\rm cyc}$・§5.2.5 事前登録表)/ `sol/sol_reply_24_d2.md`(B1–B5 の枠・符号表 (1.4))/ `docs/委嘱18_K3橋_D2D4_opus_v1.md` / `provenance/CLAIMS.md`(C-1・C-4)/ `certificates/K5.v1.json`。
- **司令塔経由の便 29 注意 ①〜⑧ を設計に反映済み**(反映箇所は §0.2 の対応表)。**`sol/sol_reply_29_v3delta.md` の F6 節($K^{(5)}$ 事前値表)は読んでいない** — 本稿の構造値はすべて独立導出であり、突合は司令塔が裁定時に行う。
- 検算: **二系統**(便 29 ⑧)。`search/week4-k5-bridge-d1.mjs`(node・**87/87 PASS**・v1.1 で I 群 4 件追加)と `search/week4-k5-bridge-d1.g`(GAP 4.16.0・**52/52 PASS**・v1.1 で I 群 3 件追加)。両者はヘルパーを一切共有しない(node は $D_5$ を整数 $2a+e$ で自前符号化+左剰余類、GAP は fp 群 → `IsomorphismPermGroup` → `DirectProduct`+右剰余類)。
- **状態: `paper + two-system cross-checked`(群論部分のみ)。`verified`(Lean)ではない。算術部分は本稿の範囲外(未着手)。**

> ### 封印規律(本稿が触れないもの)
> $u$ の値・$[u^{-1}]_{10}$ の位数・固定体・Kummer 類の帰結・$\mathrm{Ih}_{K^{(5)}}$ の全射性 — **本稿は一切扱わない**。これらは次工程(S5/S6)の出力である。本稿は **$u$ に触れる前に固定すべき条件と宇宙**だけを確定する。

---

## 0. 結論(先に 9 行・**v1.1**)

1. **構造確定**: $\lvert G_5\rvert = 500$、$[G_5,G_5] = \langle r\rangle^3\cong\mathbb F_5^3$(位数 125)、$Z(G_5)=1$、$\lvert\mathrm{Aut}(G_5)\rvert = 48000$。**符号表 (1.4) は $n=3$ と字面まで同一** — $G_5\cong\mathbb F_5^3\rtimes C_2^2$。
2. **GT の確定**: $\boxed{\lvert\mathrm{GT}(K^{(5)})\rvert = 40}$、完全列 $1\to\mathfrak F_0\to\mathrm{GT}(K^{(5)})\xrightarrow{\tilde\chi}(\mathbb Z/20)^\times\to1$、$\boxed{\mathfrak F_0\cong C_5,\ e=5,\ M=10,\ K=\mathbb Q(\zeta_{20})}$。C-1(位数)・C-4(完全列挙証明書)と全項目一致。
3. **前件 (0)(1)(2)(3)(6′) は PASS**。(4) は 4 分割して **(4a)(4b)(4c) PASS(紙上・両数学者)・(4d) UNKNOWN**。(5′) は次工程(【GAP-Rcyc】そのもの)。
4. **★最大の収穫**: $\mathfrak F_0$ の像は**内部自己同型**である — $\boxed{\Phi_{0,k} = \mathrm{inn}(\bar x^{-2k})}$。これは $n=5$ に固有でなく**すべての奇数 $n$ で成立**し、(6′) を有限計算なしに与える(命題 K5-1・§5.4)。$K^{(3)}$ で【GAP-18a】として機械に頼った 1 ビットが、族全体で構造的に閉じた。
5. **★$n=3$ に無い新現象 1**: 標的 ordered passport の $H$ は **$G_5$-共役類 2 つ**に割れる(不変量は $\alpha\bmod\pm$ = 平方剰余か否か)。したがって**標的 dessin は 2 個あり、互いに非同型**。$n=3$ では 1 個だった。
6. **★$n=3$ に無い新現象 2(かつ 5 の解決)**: それでも **$\Phi(\mathrm{GT})$ は 2 類を入れ替えない**。ここから **field of moduli $=\mathbb Q$ が GT 側だけで従う**(補題 Q・§6.1)。さらに $\mathrm{Aut}=1$ から **Weil cocycle が自動成立して $\mathbb Q$-モデルの存在まで閉じる**(§6.2・便 30 F3.2 と独立一致)。**ただし降下が与えるのは存在のみ — (4d) の明示モデルと actual marking は別物で、(4d)(5′) は UNKNOWN のまま。**
6b. **【v1.1】二 dessin の整合ゲートを確定**: $a := j_{\rm ns}^{-1}j_{\rm sq}\in(\mathbb Z/5)^\times$ を $u$ の開示前に有限群論だけで計算し、$\boxed{a = 1}$(補題 K5-a・§6.3・二系統)。封印する予測は $[u_{\rm ns}^{-1}]_{10} = [u_{\rm sq}^{-1}]_{10}$(**位数一致より強い**)。
7. **dessin**: 標的は**次数 10・種数 2・ordered passport $(10,\,2^41^2,\,10)$・$\mathrm{Aut}=1$・monodromy 位数 100**。最小 faithful transitive 作用は**次数 20・種数 8・$(10^2,10^2,10^2)$・$\mathrm{Aut}\cong C_5$(B2 FAIL)**。
8. **射程の正直な限界**: $\gcd(e,M/e)=\gcd(5,2)=1$ — **$n=5$ も coprime regime**。しかも **奇数族は構造的に永久に coprime**(§3.4)。repeated-primary は **$8\mid n$ でしか現れない**(命題 K5-2)。
9. **【v1.1・最重要の計画修正】**: その $8\mid n$ では **$\Phi_{0,n/4} = \mathrm{inn}(X^{-n/2}) = 1$(中心元)ゆえ $\ker\rho_0\supseteq C_2$** — **repeated-primary が発火する条件が detector を同時に殺す**(命題 K5-2b・便 30 F4.3)。ゆえに **$K^{(n)}$ 族の repeated-primary は現行 $R^{\rm cyc}$ で一律 SCHEMA-OUT**、**$n=24$ は次標的から外す**($K^{(8)}$ は負較正)。転進先は ①族外の忠実 detector 窓 ②中心 $C_2$ を測る拡張スキーマ(§3.4.1)。

### 0.1 $K^{(3)}$ との対照表(値のみ・算術は空欄)

| | $K^{(3)}$(定理 K3) | $K^{(5)}$(本稿) |
|---|---|---|
| $P = F_2/\bar N$ | $G_3\cong\mathbb F_3^3\rtimes C_2^2$、位数 **108** | $G_5\cong\mathbb F_5^3\rtimes C_2^2$、位数 **500** |
| $\lvert\mathrm{Aut}(P)\rvert$ | $1296 = 27\cdot2^3\cdot6$ | $\mathbf{48000} = 125\cdot4^3\cdot6$ |
| $M = \mathrm{ord}(X) = N_{\rm ord}$ | 6 | **10** |
| $K = \mathbb Q(\zeta_{2M})$ | $\mathbb Q(\zeta_{12})$ | $\mathbb Q(\zeta_{20})$ |
| $\lvert\mathrm{GT}(N)\rvert$ | 12 | **40** |
| $\mathfrak F_0$ / $e$ | $C_3$ / 3 | $\mathbf{C_5}$ / **5** |
| $(\mathbb Z/2M)^\times$ | $C_2^2$(位数 4) | 位数 **8** |
| $\gcd(e,M/e)$ | $\gcd(3,2)=1$ | $\gcd(5,2)=1$ — **同じ regime** |
| 標的 $H$ の指数 / $\lvert\Lambda\rvert$ | 6 / 6 | **10 / 10** |
| qualifying $H$ / good $H$ | 18 / 12 | **50 / 40** |
| 標的 ordered passport | $(6,2^21^2,6)$ | $(\mathbf{10,\,2^41^2,\,10})$ |
| 標的 dessin の種数 | 1 | **2** |
| 標的の $G$-共役類の個数 | **1** | **2**(新現象) |
| monodromy(標的) | 位数 36(核 $C_3$) | 位数 **100**(核 $C_5$) |
| 最小 faithful 次数 / 種数 | 12 / 4 | **20 / 8** |
| 最小 faithful の $\mathrm{Aut}$ | $C_3$(B2 FAIL) | $\mathbf{C_5}$(B2 FAIL) |
| (6′) の根拠 | 【GAP-18a】(機械 1 ビット) | **命題 K5-1(構造・全奇数 $n$)** |

### 0.2 便 29 注意の反映対応表

| 注意 | 反映箇所 |
|---|---|
| ① detector は degree $M=10$($e$ に合わせた degree 5 を取らない) | §4.3・**§4.4 に実例**(「$\lvert\Lambda\rvert = 5 = e$」の誘惑は実在する — bad 側 10 個。だが $\tau$ が非単射になり scope-out)。検算 D16b |
| ② $H$ 宇宙と採否規則を $u$ より前に固定・事前登録 | **§1**(全文が事前登録)。宇宙 = 指数 10 の部分群**全体**(位数 50 の部分群 93 個の全列挙で完全性を保証) |
| ③ (3) の三条件と (6′) の二成分を**別々に**記録 | §5.1 表の (3a)(3b)(3c)(3d) と (6′-i)(6′-ii)。検算 D9-(3a)〜(3d)・E2a・E3 |
| ④ cycle type で部分群を同定しない | §5.4 の同定根拠は **$\Phi_{0,k}(\bar x)=\bar x$**(定義的事実)であって型ではない。§8 ★教材 3 に対照(検算 E8: $\mathrm{Sym}(10)$ の型 $5.5$ の $C_5$ は 18144 個) |
| ⑤ $(10,10,10)$ を先入観にしない(符号) | §4.2 に**符号による事前排除**を明記。検算 D9-(5a)(5b) |
| ⑥ 整合の事前枠($\mathrm{ord}$ は $\{1,5\}$ の二値・それ以外は警報) | §1.3(結果値は書かない)。検算 E11・E12 |
| ⑦ $\Phi$ 単射は別ゲート | §5.3 を**独立の節**に分離。§5.1 の前件表には入れない |
| ⑧ load-bearing は最初から二系統 | 全 load-bearing 項目を node + GAP で実行(§9) |

---

## 1. 事前登録(**$u$ に触れる前に固定**・便 29 ②⑥・結果値を一切含まない)

> **本節は本稿の計算の前に固定した宇宙と規則である。以後これを変更しない。**

### 1.1 宇宙(H 宇宙の事前登録)

- **窓**: $N = K^{(5)} = \ker\psi_5$、$\psi_5(x_{12}) = (r,s,s)$, $\psi_5(x_{23}) = (rs,r,rs)$, $\psi_5(c)=1$(D1 (3.1))。
- **marking**: D1 (3.6) の $\bar x = (r,s,s)$, $\bar y = (rs,r,rs)$, $\bar z = (r^2s, r^{-1}s, r)$。**変更しない。**
- **$H$ 宇宙**: $\{H\le G_5 : [G_5:H] = 10\}$ の**全体**。位数 50 の部分群を全列挙する(§4.1 に完全性の証明つき。総数 93)。
- **detector の次数は $M = 10$**(便 29 ①)。$e=5$ に合わせた $\lvert\Lambda\rvert=5$ の族は**採らない**。

### 1.2 採否規則(先に書く)

| 段 | 規則 |
|---|---|
| **Q(qualifying)** | $\bar x$ が $G_5/H$(10 点)上で **10-サイクル**(= B3 全分岐) |
| **G(good)** | Q かつ $N_{G_5}(H) = H$ |
| **T(target)** | G かつ ordered passport が $(\bar x,\bar y,\bar z) = (10,\,2^41^2,\,10)$($K^{(3)}$ の標的 $(6,2^21^2,6)$ と同じ側) |
| **除外** | Q を満たさない $H$ / G を満たさない $H$ は**前件 (3) 破れとして scope-out**(棄却ではない・v3 §5.2.5) |
| **禁止** | 結果を見てから $\Lambda$ を和集合へ広げること(便 29 ③・W4)。標的が複数の $G_5$-共役類に割れた場合は**各類を別々に扱い、どちらでも同じ判定が出るかを検査する** |

### 1.3 整合の事前枠(便 29 ⑥・$u$ に触れない)

> **前件 (5′)+(R6-act) が成立するなら、補題 R の段 3 より $\mathrm{ord}([u^{-1}]_M)\mid e = 5$。$5$ は素数だから**
> $$ \mathrm{ord}\bigl([u^{-1}]_{10}\bigr)\in\{1,\ 5\}\quad\text{の二値である。} $$
> **警報規準**: 将来の走査で $2$ または $10$ が観測されたら、それは新現象ではなく**前件の札か記録のどこかが破れている**証拠として扱う(検算 E11・E12)。
>
> **もう一つの事前登録された整合検査【v1.1 で強化・§6.3】**: 標的が 2 つの $G_5$-共役類 $\Lambda_{\rm sq}$, $\Lambda_{\rm ns}$ に割れる(§4.5)。v1 は整合ゲートを「$\mathrm{ord}$ の一致」と書いたが**弱すぎる**(便 30 W3)。正しいゲートは、**作用同型 $j_i$ で移送した Kummer character の一致**である:
> $$ \boxed{\text{(P-a)}\quad[u_{\rm ns}^{-1}]_{10} = [u_{\rm sq}^{-1}]_{10}^{\,a},\qquad a := j_{\rm ns}^{-1}j_{\rm sq}\in(\mathbb Z/5)^\times } $$
> **$a$ は $u$ の開示前に有限群論だけで確定できる。本稿 §6.3.2 で確定・封印した。** 生の $u_{\rm sq}, u_{\rm ns}$ の一致は**要求しない**(曲線・局所座標・marking が違えば主係数は違いうる)。
>
> **採否規則(v1.1)**: 二 dessin は **`target_policy = all_two_classes`** — 両方を別 fixture として走らせ、**結果を見てから片方を捨てることを禁止**する(便 30 F6.1・P3 / 裁定 26-6)。$\mathrm{Aut}(G_5)$ が二類を融合する以上、marking から独立に一方を正典化する自然な根拠はない。

---

## 2. $G_5$ の明示実現と構造

### 2.1 定義(正典どおり)

$D_5 = \langle r,s\mid r^5, s^2, srs^{-1}r\rangle$(位数 10)。D1 (3.6) より

$$ X := \bar x = (r,\,s,\,s),\qquad Y := \bar y = (rs,\,r,\,rs),\qquad Z := \bar z = (r^2s,\,r^{-1}s,\,r),\qquad XYZ = 1, $$
$$ G_5 := \langle X, Y\rangle\ \le\ D_5^3 . $$

**基本量(二系統一致)**

| 量 | 値 | 検算 | 較正 |
|---|---|---|---|
| $\mathrm{ord}(X)=\mathrm{ord}(Y)=\mathrm{ord}(Z)$ | $10 = \mathrm{lcm}(5,2)$ | A2 | D1 (3.4) |
| $\lvert G_5\rvert$ | $\mathbf{500} = 4\cdot5^3$ | A3 | **C-1(cross-checked)**・`K5.v1.json` `index_PB3` |
| $G_5\subset D_5^3$ | 反射パリティ偶の指数 2 部分群 | A4 | — |
| $R := [G_5,G_5]$ | $\langle r\rangle^3\cong\mathbb F_5^3$、位数 $\mathbf{125}$ | A5a・A5b | D1 Prop 3.6 (3.8)($4\nmid5$)・`K5.v1.json` `derived_order` |
| $G_5/R$ | $C_2\times C_2$ | A5c | D1 p.15 |
| $Z(G_5)$ | $\mathbf 1$ | A6 | 便 24 (1.6) の $n=5$ 版 |

### 2.2 符号表 — 便 24 (1.4) のアナログ

$\mathbb F_5^3$ の三本の座標線を $e_1 := \langle X^2\rangle$, $e_2 := \langle Y^2\rangle$, $e_3 := \langle Z^2\rangle$($X^2 = (r^2,1,1)$ 等)、$G_5/R$ の三つの非零元を $h_1 = \bar X, h_2 = \bar Y, h_3 = \bar Z$ とすると、共役作用は

$$ \begin{array}{c|ccc} & e_1 & e_2 & e_3\\\hline h_1 & + & - & -\\ h_2 & - & + & -\\ h_3 & - & - & +\end{array} \tag{1.4$_5$} $$

**すなわち $n=3$ の (1.4) と字面まで同一である**(検算 A7b)。ゆえに

$$ \boxed{\ G_5\ \cong\ \mathbb F_5^3\rtimes C_2^2\ } \tag{1.5$_5$} $$

で、$\mathbb F_5^3$ は $C_2^2$ の**三つの相異なる非自明一次元指標の直和**。固定部分は $0$ で作用は忠実、ゆえに $Z(G_5)=1$、$C_{G_5}(R) = R$。

> **★ 一般奇数 $n$ で同じ**: 表 (1.4) の導出は $s r^a s^{-1} = r^{-a}$ しか使わず、$n$ に依存しない。**$G_n\cong(\mathbb Z/n)^3\rtimes C_2^2$(三つの相異なる非自明指標)は全奇数 $n$ で成立する**(§5.4 で使う)。

### 2.3 半直積座標(以後の計算の作業座標)

$q_1 := (1,s,s),\ q_2 := (s,1,s),\ q_3 := (s,s,1)$ は $G_5$ の中で可換な対合三つ組をなし($q_1q_2=q_3$)、$Q := \{1,q_1,q_2,q_3\}\cong C_2^2$ は $R$ の補群である(Schur–Zassenhaus・$\gcd(125,4)=1$;検算 A7a)。$e^{(a_1,a_2,a_3)} := (r^{a_1},r^{a_2},r^{a_3})$ と書くと

$$ X = e^{(1,0,0)}q_1,\qquad Y = e^{(1,1,1)}q_2,\qquad Z = e^{(2,-1,1)}q_3 \tag{2.1} $$

(検算 A8)。$q_1,q_2,q_3$ の $R$ 上の作用はそれぞれ $\mathrm{diag}(+,-,-),\ \mathrm{diag}(-,+,-),\ \mathrm{diag}(-,-,+)$。

### 2.4 $\mathrm{Aut}(G_5)$ と B1

> **命題 K5-0.** $\lvert\mathrm{Aut}(G_5)\rvert = 48000 = 125\cdot4^3\cdot6$ であり、$\mathrm{Aut}(G_5)$ は「位数 10 の生成三つ組 $(A,B,C)$, $ABC=1$」の集合(**48000 個**)に**自由推移的**に作用する。ゆえに **B1 PASS(軌道一意性)**。

**証明**(便 24 F2 の $n=5$ 版・独立に再構成)。
1. $R = [G_5,G_5]$ は特性部分群。$\varphi\in\mathrm{Aut}(G_5)$ は $\varphi_R\in GL_3(\mathbb F_5)$ と $\varphi_Q\in\mathrm{Aut}(C_2^2)\cong S_3$ を誘導し、三本の線の**指標が相異なる**ので $\varphi_R$ は「置換 $\times$ 対角」= 単項行列。よって線形部は $(\mathbb F_5^\times)^3\rtimes S_3$、位数 $4^3\cdot6 = 384$。
2. $\varphi_R,\varphi_Q$ を固定したときの残りは $Z^1(Q,R)$。$\gcd(\lvert Q\rvert,\lvert R\rvert)=1$ より $H^1=0$、$R^Q = 0$ ゆえ $\lvert Z^1\rvert = \lvert B^1\rvert = \lvert R\rvert = 125$。**⇒ $\lvert\mathrm{Aut}(G_5)\rvert\le 125\cdot384 = 48000$**(上の対応は単射)。
3. 他方、位数条件を満たす三つ組の個数を数える: 像 $(\bar A,\bar B)$ は $C_2^2$ の相異なる非零元の順序対で **6 通り**。$A = (v,q_1), B = (w,q_2)$ と書くと $\mathrm{ord}(A)=10\iff v_1\ne0$(4·25 通り)、$\mathrm{ord}(B)=10\iff w_2\ne0$、$\mathrm{ord}(AB)=10\iff w_3\ne v_3$。よって $6\cdot(4\cdot5\cdot5)\cdot(5\cdot4\cdot4) = 6\cdot100\cdot80 = \mathbf{48000}$。
4. 各三つ組が実際に自己同型を与えることを悉皆で確認(検算 G1・G2 が 48000/48000)。自由性は生成元像が自己同型を決めることから自明。**⇒ 等号**。∎

> **較正**: 同じ公式が $n=3$ で $27\cdot2^3\cdot6 = 1296$ を与え、`week4-k3-v2-repairs.mjs` T5 の実測値と一致する(検算 G3)。
> **$X^2,Y^2,Z^2$ がそれぞれ $e_1,e_2,e_3$ を生成する**ので、位数条件を満たす三つ組は自動的に $G_5$ を生成する(便 24 F2 と同じ)。

---

## 3. $\mathrm{GT}(K^{(5)})$ の構造確定

### 3.1 パラメータ集合(Thm 4.3)

$K_{\rm ord}^{(5)} = \mathrm{lcm}(5,2) = 10$(D1 (3.4))。$4\nmid5$ ゆえ Thm 4.3 (4.12) の第 2 式が適用され

$$ \mathrm{GT}(K^{(5)}) = \bigl\{\,(m,\ (r^{2k},\,r^{-2k},\,r^{\kappa(m)}))\ \bigm|\ m\in\mathcal X_5,\ k\in\mathbb Z\,\bigr\},\qquad \kappa(m) = \begin{cases}m+1 & 2\nmid m\\ -m & 2\mid m\end{cases} $$
$$ \mathcal X_5 = \{m\in\{0,\dots,9\} : \gcd(2m+1,10)=1\} = \{0,1,3,4,5,6,8,9\},\qquad \lvert\mathcal X_5\rvert = 8, $$

$k$ は $\mathrm{ord}(r^2) = 5$ で走る(5 通り)。ゆえに

$$ \boxed{\ \lvert\mathrm{GT}(K^{(5)})\rvert = 8\cdot5 = \mathbf{40}\ } \tag{3.1} $$

(検算 B1・B3。**Thm 4.6 (4.23)($\alpha=0,n_0=5$)の $\mathrm{Aff}(\mathbb Z/5)\times\mathcal Z_2$、位数 $20\cdot2 = 40$ と一致**(検算 B4)。**証明書 `K5.v1.json`(C-4・cross-checked)の `shadows` 40 個・`counts.thm46_expected_order = 40` とも一致**(検算 H1・H4)。)

### 3.2 完全列

$m\mapsto 2m+1$ は $\mathcal X_5\to(\mathbb Z/20)^\times = \{1,3,7,9,11,13,17,19\}$ の**全単射**(検算 B2)。ゆえに

$$ \boxed{\ 1\longrightarrow\mathfrak F_0\longrightarrow\mathrm{GT}(K^{(5)})\xrightarrow{\ \tilde\chi\ }(\mathbb Z/20)^\times\longrightarrow1,\qquad \tilde\chi(m,f) = 2m+1 \ } \tag{3.2} $$

$\lvert(\mathbb Z/20)^\times\rvert = \varphi(20) = 8$、ゆえに $\lvert\mathfrak F_0\rvert = 40/8 = 5$。$\mathfrak F_0 = \ker\tilde\chi = \{(0,\ (r^{2k},r^{-2k},1)) : k\bmod5\}$($\kappa(0) = 0$)。

$$ \boxed{\ \mathfrak F_0\cong C_5,\qquad e = 5,\qquad M = \mathrm{ord}(X) = K_{\rm ord}^{(5)} = 10,\qquad K = \mathbb Q(\zeta_{2M}) = \mathbb Q(\zeta_{20}).\ } \tag{3.3} $$

- $\mathfrak F_0\cong C_5$ は**位数 5 という一事**から従う(位数素数)。さらに $\mathfrak F_0$ は $\lvert\mathrm{GT}\rvert = 40 = 2^3\cdot5$ の**唯一の Sylow 5-部分群**でもある(正規・巡回)。
- 検算 B5・B6・H5(`K5.v1.json` の $m=0$ の $f$ は $(r^{2k},r^{-2k},1)$ の 5 通りちょうど)。
- **W149 遵守**: 基礎体は $M$ から先に決めた($M = 10\Rightarrow K = \mathbb Q(\zeta_{20})$)。cusp-16 の轍は踏んでいない。

### 3.3 isolated

D1 Thm 4.3 末尾 逐語: "Furthermore, $K^{(n)}$ is an isolated object of the groupoid GTSh"(**全 $n\ge3$**)。ゆえに $n=5$ でも **source-closed**。

### 3.4 ★ regime の確定(射程の正直な限界)

$$ \gcd(e,\ M/e) = \gcd(5,\,2) = 1\quad\Longrightarrow\quad K^{(5)}\ \text{も\ \textbf{coprime regime}}. $$

さらに一般に:

> **命題 K5-2(regime の族分布).** $n = 2^\alpha n_0$($n_0$ 奇)とする。
> - $n$ 奇($\alpha=0$): $M = 2n$, $e = n$、$M/e = 2$、$\gcd(e,M/e) = 1$。
> - $n\equiv2\ (4)$($\alpha=1$): Prop 3.4 より $K^{(n)} = K^{(n/2)}$ で奇に帰着。
> - $4\mid n$($\alpha\ge2$): $M = n$、$e = n_0\,2^{\alpha-2} = n/4$、$M/e = 4$、$\gcd(e,4) = \gcd(n/4,4)$。
>
> ゆえに $\boxed{\text{repeated-primary regime}\ \bigl(\gcd(e,M/e)>1\bigr)\iff 8\mid n}$ であり、数値的に最小の非 2 冪の repeated-primary 窓は $n = 24$($M=24$, $e=6$, $M/e=4$)。

**導出**: $e = \lvert\mathfrak F_0\rvert = \lvert\mathrm{GT}(K^{(n)})\rvert/\varphi(2M)$。D1 §4 の導出値 $\lvert\mathrm{GT}(K^{(n)})\rvert = 2n_0\varphi(n_0)$($\alpha\le1$)$/\ n_0\varphi(n_0)2^{2\alpha-2}$($\alpha\ge2$)と $\varphi(2M)$ を代入する。検算 B7・B8・B9。**便 30 F4.1 が (4.1)(4.2) で独立再導出し PASS(裁定 26-2)。**

> **$n=12$ の決着(裁定 26-2)**: $(M,e,M/e) = (12,3,4)$、$\gcd(3,4)=1$ で **coprime**。便 30 F4.2 が $\mathfrak F_0 = \{k\equiv0\ (2)\bmod6\}\cong C_3$ と $\lvert\mathrm{GT}(K^{(12)})\rvert/\varphi(24) = 24/8 = 3$ の二経路で再導出し、便 29 P7/W6 を自ら erratum とした。**本欄は v1 のまま。**

#### 3.4.1 【v1.1・便 30 F4.3 / 裁定 26-3】★ 構造的盲点 — $n=24$ の差戻し

> **命題 K5-2b(盲点定理).** $4\mid n$ とする。$m=0$ における許容パラメータは $k\equiv0\ (\mathrm{mod}\ 2)$(Thm 4.3 (4.12) の $4\mid n$ 側の条件)であり、生成元計算 (5.2) は偶数 $n$ でもそのまま成立する:
> $$ \Phi_{0,k} = \mathrm{inn}\bigl(X^{-2k}\bigr). \tag{4.4} $$
> ここで **$8\mid n$** なら $k_0 := n/4$ は非零の許容値で、$f_{k_0} = (r^{n/2},r^{-n/2},1)$ は $\mathfrak F_0$ の位数 2 の元を与える。他方
> $$ X^{-2k_0} = X^{-n/2} = (r^{n/2},\,1,\,1)\ \in\ Z(D_n^3)\cap G_n $$
> は**中心元**なので
> $$ \boxed{\ \Phi_{0,k_0} = 1,\qquad\text{ゆえに}\qquad \ker\rho_0\ \supseteq\ \langle(0,f_{k_0})\rangle\cong C_2\quad(\text{任意の }\Lambda\text{ について}).\ } \tag{4.5–4.6} $$

**⇒ $\rho_0$ は detector の選び方に依らず非忠実であり、$8\mid n$ の $K^{(n)}$ は現行 $R^{\rm cyc}$ の SCHEMA-OUT。**

$n=24$ では $M=24,\ e=6,\ M/e=4$、$\mathfrak F_0\cong C_6$、$\Phi(\mathfrak F_0)\cong C_3$、$\ker(\Phi\vert_{\mathfrak F_0})\cong C_2$。

> **★★ 二つの条件が同じ $8\mid n$ で発火する。** すなわち $K^{(n)}$ 族では
> $$ \boxed{\text{repeated-primary を得た瞬間、まさにその repeated 2-成分が }\Phi\text{ から見えなくなる。}} $$
> $K^{(8)}$ は最小の実例($\mathfrak F_0 = C_2$ が丸ごと $\Phi$ 上で消える)。既知の飽和結果(Thm 5.3)との比較には使えるが、**これは legacy regression test の正例ではなく SCHEMA-OUT の負較正である**。

**v1 の記述の訂正**: v1 §3.4 末尾と §10 は $n=24$ を「$q$-版の反証の最小候補」と書いた。**取り下げる。** 数値的に最小の repeated-primary 窓であることは正しいが、**スキーマ上で最初に適用可能な候補ではない**(便 30 ★教材 4)。**$G_{24}$(位数 6912)の全面走査に予算を投じる前に、この構造的 SCHEMA-OUT を manifest に登録する**(裁定 26-3)。

**攻略分岐(将来課題・本稿では着手しない)**:
1. **$K^{(n)}$ 族外**で repeated-primary かつ $\rho_0$ 忠実となる窓を探す(窓の地理学の探索課題)。
2. **拡張スキーマ**: $\Phi$ で消える中心 $C_2$ を、別の rigidification(例えば $\Lambda$ 以外の付加構造)で測る設計。

> **★ この節の含意(研究計画への入力)**: 研究者裁定の「奇数族の横展開($n=5,7,9,\dots$)」は、**構造的に永久に coprime regime の中にある**。そして repeated-primary 側は **$K^{(n)}$ 族全体で SCHEMA-OUT**。ゆえに便 28 P4 が求めた「repeated-primary regime での試験」は、**この族の中では原理的に実行できない** — 上の分岐 1・2 のどちらかへ転進するしかない(§12 論点)。

---

## 4. $H$ 宇宙と標的の同定

### 4.1 位数 50 の部分群の全列挙(完全性つき)

> **補題 E.** $\lvert H\rvert = 50$ なら $H\cap R$ は $H$ の Sylow 5-部分群(位数 25)である。
> **証明**: $R = \{g\in G_5 : g^5=1\}$(検算 A5a: 位数 $\ne1,5$ の元はすべて位数 2 か 10)。$\lvert H\rvert = 2\cdot5^2$ ゆえ $H$ の Sylow 5-部分群は位数 25・指数 2 で正規かつ一意、その元はすべて位数 $\mid5$ ゆえ $R$ に入る。逆の包含も明らか。∎

ゆえに $H = \langle U, g\rangle$($U := H\cap R$ は $\mathbb F_5^3$ の 2 次元部分空間、$g\in H\smallsetminus R$)として**全列挙が完全**である。結果(**二系統一致**):

| 量 | 値 | 検算(node / GAP) |
|---|---|---|
| $R$ の 2 次元部分空間 | 31 | D1 / — |
| 位数 50 の部分群の総数 | **93** | D2 / D2 |
| **qualifying**($\bar x$ が 10-サイクル) | **50** | D3 / D3 |
| **good**($N_{G_5}(H)=H$, $\lvert\Lambda\rvert=10$) | **40** | D4 / D4 |
| bad($\lvert N\rvert = 100$, $\lvert\Lambda\rvert = 5$) | **10** | D4 / D4 |

**紙上の同定**(独立に閉じた形):$H$ の $C_2^2$-像を $\langle q\rangle$ とすると、
- $q = q_1$($X$ と同じパリティ)では **qualifying が存在しない**: $e_1\in U$ なら $\langle e_1\rangle\le\langle X\rangle\cap H$;$e_1\notin U$ なら $q_1$-安定性から $U = E_-(q_1) = \langle e_2,e_3\rangle$ で、$h=(w,q_1)\in H$ の $h^2 = e^{(2w_1,0,0)}\in U$ より $w_1=0$、ゆえに $q_1 = X^5\in H$。いずれも $\langle X\rangle\cap H\ne1$。
- $q = q_2$ では $U = \langle e_2,\ \alpha e_1+e_3\rangle$($\alpha\in\mathbb F_5$)で $w$ は $U$ を法に自由(5 通り)⇒ $5\times5 = 25$ 個が qualifying。$\alpha\ne0$ が good(20 個)、$\alpha=0$ が bad(5 個)。
- $q = q_3$ は $e_2\leftrightarrow e_3$ の対称で同数。

($25+25 = 50$ ✓, $20+20 = 40$ ✓, $5+5=10$ ✓。**同じ計算を $n=3$ に流すと qualifying 18・good 12・bad 6・$\lvert\Lambda\rvert=3$ となり、`gap18a.json` と定理 K3 の実測に完全一致する** — 手計算の較正が取れている。)

### 4.2 ★ passport の**符号による事前制約**(便 29 ⑤)

$\sigma_x\sigma_y\sigma_z = 1$ で、次数 10 における 10-サイクルは**奇置換**である。ゆえに

$$ \boxed{\ \text{次数 10 で ordered passport } (10,10,10)\ \text{は符号により不可能}\ }\qquad(\text{奇}^3 = \text{奇}\ne\mathrm{id}). $$

**$P$ の元として $\mathrm{ord}(X)=\mathrm{ord}(Y)=\mathrm{ord}(Z)=10$ でも、coset 作用の passport が $(10,10,10)$ になることはない。** 実測はこの制約と整合する:

$$ \text{good 40 個の ordered passport} = (10,\ 2^41^2,\ 10)\ \text{が 20 個},\quad (10,\ 10,\ 2^41^2)\ \text{が 20 個} $$

(奇・偶・奇 ⇒ 積は偶 ✓。検算 D6・D9-(5a)・D9-(5b)。$K^{(3)}$ の $(6,2^21^2,6)$ と $(6,6,2^21^2)$ の $6+6$ 分裂の完全なアナログ。)

**紙上の理由**: $q=q_2$ 側では $\langle Y^2\rangle = \langle e_2\rangle\le U$ が全共役に含まれるので $\langle Y\rangle\cap H^g$ が位数 5 を持ち、$Y$ の軌道長は $10/5 = 2$ か $1$ になる。不動点数は $\lvert C(Y)\rvert\cdot\lvert\mathrm{Cl}(Y)\cap H\rvert/\lvert H\rvert = 10\cdot10/50 = 2$。ゆえに $2^41^2$。$Z$ 側は $\langle e_3\rangle\cap U = 0$ ゆえ 10-サイクル。

> **一般奇数 $n$ の予測(未検証・candidate)**: 同じ計算は $\sigma_y$ の型を $2^{n-1}1^2$ にする。$n=3\Rightarrow2^21^2$ ✓、$n=5\Rightarrow2^41^2$ ✓。

### 4.3 標的の指定(採否規則 T)

$$ \boxed{\ \Lambda := \{\,H\ \text{の}\ G_5\text{-共役}\,\},\quad H\ \text{は ordered passport}\ (10,\,2^41^2,\,10)\ \text{かつ}\ N_{G_5}(H)=H,\quad \lvert\Lambda\rvert = 10 = M .\ } $$

$K^{(3)}$ の標的 $(6,2^21^2,6)$ と同じ側を取った(委嘱 21 の exact conjugator と同じ正規化)。

### 4.4 ★ 便 29 ① の**実例** — 「$e$ に合わせる」誘惑は実在する

bad 側 10 個は $\lvert\Lambda\rvert = \mathbf5 = e$ である。「$\mathfrak F_0\cong C_5$ の作用を見るなら 5 点で十分では」と取りたくなる。しかし

$$ \mathrm{Stab}_{\langle X\rangle}(H) = N_{G_5}(H)\cap\langle X\rangle\ \text{は位数}\ \mathbf2 $$

なので $\tau:\mu_{10}\to\mathrm{Sym}(\Lambda)$ は**非単射**になり、局所 Kummer 側の $\mu_{10}$-torsor が潰れる(検算 D16b・二系統)。**これが便 29 ①(W3)の警告そのものである。前件 (3) 破れ ⇒ scope-out(棄却ではない)として記録する。**

### 4.5 ★★ 新現象: 標的が **$G_5$-共役類 2 つ**に割れる

標的 20 個は $\lvert\Lambda\rvert = 10$ ゆえ $G_5$-共役類 **2 つ**(各 10)に割れる(検算 D7・二系統)。不変量は $U = \langle e_2,\ \alpha e_1+e_3\rangle$ の $\alpha$ を $\pm$ で割ったもので、

$$ \boxed{\ \Lambda_{\rm sq}:\ \alpha\in\{1,4\}\ (\text{mod }5\ \text{平方剰余}),\qquad \Lambda_{\rm ns}:\ \alpha\in\{2,3\}\ (\text{非剰余})\ } $$

(検算 D8)。$w$ 方向は $R$-共役が自由に動かし、$q_1$-共役が $\alpha\mapsto-\alpha$ を与える。$-1 = 4$ は $\bmod\ 5$ の平方剰余なので二類は融合しない。

- **$n=3$ に無い**: $\mathbb F_3^\times = \{1,-1\}$ は $\pm$ で一つの類になるため、$K^{(3)}$ では標的 6 個で共役類 1 つだった。**一般に類の個数は $(n-1)/2$**(candidate)。
- **dessin としても非同型**: $\sigma_x$ を標準 10-サイクルに正規化して $\sigma_y$ を $\langle\sigma_x\rangle$-共役で比較すると 2 つは分かれる(検算 D15・D16)。手計算の不変量は $A-B\equiv1-\alpha\ (5)$ で、$\langle\sigma_x\rangle$-共役が $A-B\mapsto -(A-B)+2$ を起こす ⇒ 軌道は $\{0,2\}$ と $\{4,3\}$。

> **【v1.1・便 30 F2.1/W4 — 圏の明示(この一行が無いと主張が曖昧)】**
> 「非同型」は **固定した $U = \mathbf P^1_{\mathbb Q}\smallsetminus\{0,1,\infty\}$ 上の被覆(= ordered dessin / cover over the fixed $U$)の圏**での主張である。この圏では同型類は $\hat F_2$-共役類、したがって $G_5$-共役類で分類されるので、二類は非同型。
> **未分離**: 「基底の三点 $0,1,\infty$ の置換を許す」圏や「Belyi 写像を忘れて曲線だけを見る」粗い同値関係では、本稿も便 30 も分離を確認していない。**その圏での主張はしない。**
> あわせて **$\mathrm{Aut}(G_5)$-融合を dessin 同型と読まない**(W4): $\mathrm{Aut}(G_5)$ は marking を動かすので、cover の同型判定は $G_5$-共役類で行う(★教材 1 の系)。
- **$\mathrm{Aut}(G_5)$ は融合する**: good 40 個は $\mathrm{Aut}(G_5)$-軌道 1 つ(検算 G4)。**「$\mathrm{Aut}$-軌道が一つ」から「$G$-共役類が一つ」を推論してはならない**(★教材 1)。

---

## 5. $R^{\rm cyc}$ 前件チェックリスト(v3 §5.2.1 の型付き前件)

### 5.1 判定表(**(3) の三条件と (6′) の二成分を別々に記録** — 便 29 ③)

| 前件 | 内容 | 判定 | 根拠 |
|---|---|---|---|
| **(0)** | $N$ が isolated / $\mathrm{Ih}_N$ が準同型として定義済み | **PASS** | **source-closed**: D1 Thm 4.3 末尾(全 $n\ge3$) |
| **(1)** | $1\to\mathfrak F_0\to\mathrm{GT}(N)\xrightarrow{\tilde\chi}(\mathbb Z/2M)^\times\to1$ 完全、$\tilde\chi\circ\mathrm{Ih}_N=\chi_{2M}$ | **PASS** | 完全列は §3.2(二系統)。$\tilde\chi\circ\mathrm{Ih}=\chi_{2M}$ は正典 §1.3 の $\chi_{\rm vir}$ 両立(定理 K3 (K2) と同じ source) |
| **(2)** | $\mathfrak F_0\cong C_e$、$e\mid M$ | **PASS** | $\lvert\mathfrak F_0\rvert = 5$(素数)⇒ $C_5$。$5\mid10$。§5.4 は $\Phi$ 経由の第二証明も与える |
| **(3a)** | $N_P(H) = H$ | **PASS** | good 40 個すべて(検算 D9-(3a)・二系統) |
| **(3b)** | $\lvert\Lambda\rvert = M = 10$ | **PASS** | 検算 D9-(3b)・二系統 |
| **(3c)** | $\langle X\rangle$ が $\Lambda$ 上 regular(**全 coset で $H^g\cap\langle X\rangle=1$** まで) | **PASS** | 検算 D9-(3c)・二系統。$\lvert\langle X\rangle\rvert = 10 = \lvert\Lambda\rvert$ と自由性 ⇒ 単純推移 |
| **(3d)** | $\mathrm{Stab}_{\langle X\rangle}(H) = N_G(H)\cap\langle X\rangle$(W1 の型) | **PASS** | 検算 D9-(3d)。**coset の stabilizer $H$ と取り違えない** |
| **(4a)** | dessin $W_0$($=$ 幾何被覆 $W_{0,\bar{\mathbb Q}}\to U_{\bar{\mathbb Q}}$)の field of moduli $=\mathbb Q$ | **PASS(紙上・両数学者)** | **補題 Q**(§6.1)。GT 側だけで従う。便 30 F3.1 検分 PASS |
| **(4b)** | field of definition $=\mathbb Q$(descent) | **PASS(紙上・両数学者)** | $\mathrm{Aut}(W_0/U) = N_G(H)/H = 1$ ⇒ 同型一意 ⇒ Weil cocycle 自動(§6.2)。便 30 F3.2 が独立に記述。**引用は Dèbes–Douai 1997 + Sijsling–Voight 2016(出版時)** |
| **(4c)** | $\mathbb Q$-有理な全分岐 cusp | **PASS** | (3c) より $\lambda=0$ 上は 1 点(分岐指数 10)。ファイバーが Galois 安定な 1 点集合ゆえ $\mathbb Q$-有理 |
| **(4d)** | 明示 $\mathbb Q$-モデル(方程式)と actual marked identification | **UNKNOWN(次工程 S5)** | $K^{(3)}$ の (P4)(P5) に当たる作業。本稿の範囲外 |
| **(5)** | FC-2b/FC-3(窓非依存 import) | **PASS(条件つき)** | 補題 C/D0/D/E/I3‡ は窓非依存($A_5$ v4 §1・便 27 F5 で PASS 済)。前件 (FC3-i) は (4a)(4b)、(FC3-ii) は推移性、**(FC3-iii) は (3a)** が供給 |
| **(5′)** | $\rho_0(\mathrm{Ih}_N(\gamma)) = \tau(\kappa_{u^{-1}}(\gamma))\ (\forall\gamma\in G_K)$ | **UNKNOWN(次工程)** | (4d) を要する。**これが【GAP-Rcyc】= 族の定理の本丸そのもの** |
| **(6′-i)** | $\Lambda$ が $\Phi(\mathfrak F_0)$-安定 | **PASS** | §5.4(**構造的に自動** — $\Phi(\mathfrak F_0)\subseteq\mathrm{Inn}(G_5)$)。検算 E2a・二系統。参考: $\Phi(\mathrm{GT})$ 全 40 元でも安定(E2b) |
| **(6′-ii)** | $\rho_0$ が忠実(⇒ 補題 R′ で $\rho_0(\mathfrak F_0) = \tau(\mu_M[e])$) | **PASS** | §5.4(構造的)。検算 E3・E5・二系統 |

> **⇒ 群論側の前件はすべて閉じた。残るのは (4d)(5′)、すなわち「明示モデルと局所 Kummer 比較」だけである。**

### 5.2 二つの共役類での独立判定(便 29 ③の「和集合にしない」)

$\Lambda_{\rm sq}$ と $\Lambda_{\rm ns}$ を**別々に**扱った。**どちらでも (3a)(3b)(3c)(3d)(6′-i)(6′-ii) がすべて PASS** し、$\rho_0$ は忠実で像は位数 5 の平行移動群(検算 E9)。**和集合は取っていない。**

### 5.3 【別ゲート】$\Phi$ の単射性(便 29 ⑦)

$$ \boxed{\ \Phi:\mathrm{GT}(K^{(5)})\longrightarrow\mathrm{Aut}(G_5)\ \text{は単射(40 元)}\ } $$

**紙上証明**: (2.1) の座標で直接計算すると($u := 2m+1$、指数は $\bmod\ 5$)

$$ \Phi_{m,k}(X) = e^{(u,0,0)}q_1,\qquad \Phi_{m,k}(Y) = e^{(1-4k,\ u,\ 1-2\kappa(m))}q_2 \tag{5.1} $$

(検算 C3)。第 1 成分 $1-4k$ から $k\bmod5$ が一意($4$ は可逆)。$(u\bmod5,\ \kappa(m)\bmod5)$ の 8 組は

$$ m=0{:}(1,0),\ 1{:}(3,2),\ 3{:}(2,4),\ 4{:}(4,1),\ 5{:}(1,1),\ 6{:}(3,4),\ 8{:}(2,2),\ 9{:}(4,0) $$

ですべて相異なるので $m\in\mathcal X_5$ も一意。$X,Y$ が $G_5$ を生成するので $\Phi$ は単射。∎(検算 C2・**二系統**。40 個が実際に $\mathrm{Aut}(G_5)$ の元であることも悉皆確認: C1。)

> **この節は前件表に入れない**(便 29 ⑦)。補題 R の (7.4) は $\mathrm{Fix}(\ker\mathrm{Ih}_N)$ であり、$\mathrm{Fix}(\ker(\Phi\circ\mathrm{Ih}_N))$ まで述べるときにのみ本ゲートが load-bearing になる。**次工程で固定体を述べるならここが代金**であり、$K^{(5)}$ ではすでに支払い済みである。

**副産物**(次工程で効く): $\Phi\vert_R = \mathrm{diag}\bigl(u,\ u,\ 1-2\kappa(m)\bigr)$、第 3 成分は $m$ が偶なら $u$、奇なら $-u$(検算 C4)。すなわち $\Phi(\mathrm{GT})$ の $R$ 上の作用はスカラーか「第 3 座標だけ符号反転したスカラー」で、**どちらも $U = \langle e_2,\alpha e_1+e_3\rangle$ を $\alpha\mapsto\pm\alpha$ に送る**。これが §6 の鍵。

### 5.4 ★★ (6′) の構造的閉鎖 — 全奇数 $n$ に効く

> **【v1.1・便 30 P1】$\mathrm{inn}$ の規約**: 本稿は $\boxed{\mathrm{inn}(g)(h) := ghg^{-1}}$ を採る。
> 逆規約 $\mathrm{inn}(g)(h) = g^{-1}hg$ を採ると (5.2) の指数の符号だけが反転する($\Phi_{0,k} = \mathrm{inn}(\bar x^{2k})$)。**像の部分群 $\mathrm{inn}(\langle\bar x^2\rangle)$ と忠実性・$\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$ は規約に依らない**(便 30 F1.1 と一致)。§6.3 の封印値 $a$ も規約不変(検算 I4)。

> **命題 K5-1.** $n\ge3$ を**奇数**、$G_n = F_2/\bar K^{(n)}_{F_2}$、marking は D1 (3.6)、$M = 2n$、$\mathfrak F_0 = \ker\tilde\chi$ とする。このとき
> $$ \boxed{\ \Phi_{0,k}\ =\ \mathrm{inn}\bigl(\bar x^{-2k}\bigr)\qquad(k\bmod n),\ } \tag{5.2} $$
> すなわち **$\Phi(\mathfrak F_0) = \mathrm{inn}\bigl(\langle\bar x^2\rangle\bigr)\subseteq\mathrm{Inn}(G_n)$**、位数 $n$。ゆえに、**前件 (3) を満たす任意の $H$ に対して**
> 1. $\Lambda$ は $\Phi(\mathfrak F_0)$-安定(内部自己同型は共役類を保つ)= **(6′-i) 自動**、
> 2. $\rho_0$ は忠実で $\rho_0(\mathfrak F_0) = \tau(\mu_M[n]) = \tau(\mu_M[e])$ = **(6′-ii) 自動**、
> 3. $\mathfrak F_0\cong C_n$(= 前件 (2))も同時に従う。

**証明**(4 段・すべて初等)。

1. **$\mathfrak F_0$ の同定**: $\tilde\chi(m,f) = 2m+1$、$m$ は $\bmod\ K_{\rm ord} = 2n$。$2m+1\equiv1\ (\mathrm{mod}\ 4n)\iff m\equiv0\ (\mathrm{mod}\ 2n)\iff m=0$。$\kappa(0) = 0$ ゆえ $\mathfrak F_0 = \{(0,\ f_k)\}$, $f_k = (r^{2k},r^{-2k},1) = e^{(2k,-2k,0)}$、$k\bmod n$。
2. **座標**: $n$ 奇より $\lvert G_n\rvert = 4n^3 = \lvert D_n^3\rvert/2$(C-1)ゆえ $G_n$ は $D_n^3$ の偶パリティ部分群。$q_1 = (1,s,s), q_2 = (s,1,s), q_3 = (s,s,1)$ は可換な対合三つ組で $R = \langle r\rangle^3$ の補群、$X = e^{(1,0,0)}q_1$、$Y = e^{(1,1,1)}q_2$。$q_2$ は $R$ に $\mathrm{diag}(-1,+1,-1)$ で作用。
3. **計算**: $\Phi_{0,k}(X) = X^{1} = X$。
 $$ \Phi_{0,k}(Y) = f_k^{-1}Yf_k = e^{(1,1,1)-(2k,-2k,0)+q_2(2k,-2k,0)}q_2 = e^{(1-4k,\ 1,\ 1)}q_2 . $$
 一方 $\mathrm{inn}(e^{t})$ は $X\mapsto e^{(1,0,0)+(1-q_1)t}q_1$, $Y\mapsto e^{(1,1,1)+(1-q_2)t}q_2$ で、$(1-q_1)t = (0,2t_2,2t_3)$, $(1-q_2)t = (2t_1,0,2t_3)$。$X$ 固定より $t_2=t_3=0$($n$ 奇ゆえ $2$ 可逆)、$Y$ の一致より $2t_1 = -4k$、すなわち $t_1 = -2k$。**生成元像が一致するので $\Phi_{0,k} = \mathrm{inn}(e^{(-2k,0,0)})$**、そして $e^{(-2k,0,0)} = (X^2)^{-k} = \bar x^{-2k}$。
4. **帰結**: $\langle X^2\rangle$ は $\langle X\rangle\cong C_{2n}$ の唯一の位数 $n$ 部分群。前件 (3) より $\langle X\rangle$ は $\Lambda$ に単純推移(= $\Lambda$ は $\langle X\rangle$-torsor)なので $\langle X^2\rangle$ は $\Lambda$ に**自由に**作用する。$k\mapsto(X^2)^{-k}$ は $\mathbb Z/n\to\langle X^2\rangle$ の全単射。よって $\rho_0$ は単射で像は $\tau(\langle X^2\rangle) = \tau(\mu_M[n])$。また $\Phi\vert_{\mathfrak F_0}$ が単射なので $\mathfrak F_0\cong\mathrm{inn}(\langle X^2\rangle)\cong C_n$。∎

> **★ この命題が意味すること(v3 §5.2.3 との関係)**
> - v3 の**補題 R′** は「$\rho_0(\mathfrak F_0)\subseteq\tau(\mu_M)$ は自動、残る 1 ビットは $\rho_0$ の忠実性」まで縮約した。**命題 K5-1 はその最後の 1 ビットまで奇数族で消す。**
> - $K^{(3)}$ では条件 4(「$\Lambda$ 上で $\mathfrak F_0$ 忠実」)を【GAP-18a】= 機械計算で閉じた。**命題 K5-1 を $n=3$ に適用すると、この機械計算は不要になる**($\Phi_{0,k} = \mathrm{inn}(\bar x^{-2k})$、$\langle\bar x^2\rangle\cong C_3$ が $C_6$-torsor に自由作用)。**定理 K3 の依存を 1 本減らす遡及効果がある**(§10 論点 2)。
> - **同定の根拠は cycle type ではない**(便 29 ④)。根拠は「$\mathfrak F_0$ は $\tilde\chi=1$ ゆえ $\bar x$ を固定する」という**定義的事実**であり、そこから内部自己同型であることまで一意に決まる。対照として、$\mathrm{Sym}(10)$ には型 $5.5$ の元が 72576 個・それが生成する $C_5$ が **18144 個**ある(検算 E8)—**型だけでは $\tau(\mu_{10}[5])$ という 1 個を同定できない**(★教材 3・W2 の再演)。
> - **検算での確認**: (5.2) を $n=5$ で全 5 元・全 500 元評価で確認(node C6・GAP C6)。

---

## 6. ★ 補題 Q — field of moduli $=\mathbb Q$ が **GT 側だけ**で従う

### 6.1 補題

> **【v1.1・便 30 P5】型の宣言(先走らないための一行)**: $U := \mathbf P^1_{\mathbb Q}\smallsetminus\{0,1,\infty\}$ と置く。**結論を証明する前の $W_0$ は $\mathbb Q$ 上の被覆ではなく、幾何被覆**
> $$ W_{0,\bar{\mathbb Q}}\ \longrightarrow\ U_{\bar{\mathbb Q}} $$
> **である**($\hat F_2 = \pi_1^{\rm geom}(U)$ の開部分群 $\tilde H$ に対応)。$\mathbb Q$-有理性は §6.1 の結論(field of moduli)と §6.2(descent)で**初めて**得られる。

> **補題 Q.** $N\in\mathrm{NFI}_{PB_3}(B_3)$ が isolated、$\pi:\hat F_2\twoheadrightarrow P = F_2/\bar N_{F_2}$、$H\le P$、$\Lambda := \{H\ \text{の}\ P\text{-共役}\}$、$\tilde H := \pi^{-1}(H)$、$W_{0,\bar{\mathbb Q}}\to U_{\bar{\mathbb Q}}$ を $\tilde H$ の定める連結有限 étale 被覆とする。もし
> $$ \Phi\bigl(\mathrm{GT}(N)\bigr)\ \text{が}\ \Lambda\ \text{を(集合として)保つ} $$
> ならば、**$\mathrm{FOM}(W_0/U) = \mathbb Q$ である**。

**証明**(便 30 F3.1 の (3.1)–(3.3) と同一。独立に書いた本稿の論証を Sol の型付けで整える)。$N$ isolated より $\bar N_{F_2}$ は $G_{\mathbb Q}$-安定(定理 K3 §2.4 段 1 と同じ)。ゆえに $\sigma\in G_{\mathbb Q}$ の outer action は $P$ に降り、$\mathrm{Ih}_N$ の定義(2405 §1.3)より **$\mathrm{Out}(P)$ の中で**

$$ \overline{\beta_\sigma} = \overline{\Phi(\mathrm{Ih}_N(\sigma))} \tag{3.1} $$

代表を取れば

$$ \beta_\sigma\ \in\ \Phi\bigl(\mathrm{Ih}_N(\sigma)\bigr)\cdot\mathrm{Inn}(P)\ \subseteq\ \Phi(\mathrm{GT}(N))\cdot\mathrm{Inn}(P). \tag{3.2} $$

$\Lambda$ は共役類なので $\mathrm{Inn}(P)$-安定、仮定より $\Phi(\mathrm{GT}(N))$-安定。ゆえに $\beta_\sigma(H) = pHp^{-1}$ なる $p\in P$ がある。$p$ の $\hat F_2$ への持ち上げを $\tilde p$ とすれば $\bar N_{F_2}\le\tilde H$ より

$$ \varphi_\sigma(\tilde H) = \tilde p\,\tilde H\,\tilde p^{-1} \tag{3.3} $$

($\varphi_\sigma$ は $\sigma$ の作用の任意の持ち上げ)。有限 étale 被覆と開部分群の対応より $W_0^\sigma\cong W_0$。$\sigma$ は任意だったので $\mathrm{FOM}(W_0/U) = \mathbb Q$。∎

> **★ 前提の軽さ((3.3) が鍵)**: 本補題は **(K3‡) を必要としない**。$\beta_\sigma = \Phi(\mathrm{Ih}_N(\sigma))$ という**厳密な actual lift 等式**は不要で、$\mathrm{Inn}(P)$ を法にした所属 (3.2) だけで足りる — **(3.3) は共役類しか見ないので (3.1) の inner ambiguity が完全に消える**から。定理 K3 §2.4 段 2 が支払った代金より安い(便 30 F3.1 と一致・★教材 8)。

**$K^{(5)}$ への適用**: $\Phi(\mathrm{GT}(K^{(5)}))$ は $\Lambda_{\rm sq}$ も $\Lambda_{\rm ns}$ も**入れ替えずに保つ**(検算 E10・二系統。紙上の理由は §5.3 副産物: $\Phi\vert_R$ が $\alpha\mapsto\pm\alpha$ しか起こさず、$\pm$ が共役類そのものだから)。ゆえに

$$ \boxed{\ \text{標的 2 つの dessin は\textbf{どちらも} field of moduli }\mathbb Q\ \text{を持つ}.\ } $$

> **§4.5 の懸念の解消**: 「2 個の dessin が $\mathbb Q(\sqrt5)$ 上で共役かもしれない」という自然な懸念($\alpha$ の平方剰余/非剰余という不変量はいかにも $\mathbb Q(\sqrt5)$ 的である)は、**GT 側の計算が否定する**。二つは Galois 共役ではなく、単に別々の $\mathbb Q$-有理 dessin である。**GT の構造が幾何を制約した例**として記録する。

### 6.2 field of definition への降下 —【v1.1】紙上で閉じた

$\mathrm{Aut}(W_0/U) \cong N_{G_5}(H)/H = 1$(前件 (3a))とする。$W_0$ が定義される有限 Galois 拡大 $L/\mathbb Q$ を取り、各 $\sigma\in\mathrm{Gal}(L/\mathbb Q)$ に対し §6.1 の同型

$$ \phi_\sigma:\ W_0^\sigma\ \xrightarrow{\ \sim\ }\ W_0 \qquad(U\ \text{上の被覆の同型}) $$

を取る。**$\mathrm{Aut}(W_0/U)=1$ より $\phi_\sigma$ は一意**。すると $\phi_\sigma\circ{}^\sigma\phi_\tau$ と $\phi_{\sigma\tau}$ はいずれも $W_0^{\sigma\tau}\to W_0$ の同型なので、一意性から等しい。すなわち **Weil のコサイクル条件が自動的に成立**し、有限被覆の Galois descent により $W_0\to U$ は $\mathbb Q$ 上へ降下する。∎

さらに (3c) より $\lambda=0$ 上の幾何点は 1 個だけなので、その一点集合は Galois 安定であり、降下後の点は **$\mathbb Q$-有理** = (4c)。

> **⇒ (4b) の札: 「PASS(紙上・両数学者)」**(本稿の論証 + 便 30 F3.2 の独立記述が一致)。**数学的な穴ではない。**

> **【引用確定・裁定 26-4 / `docs/文献ゲート_01_moduli_descent.md`】** v1 の【文献要請 1】は文献ゲートを通り、出版時の引用が確定した:
> - **Dèbes–Douai 1997**(mere cover の降下障害の一般論・査読済の正典)
> - **Sijsling–Voight 2016**(arXiv:1504.02814・**marked 版** — $\mathbb Q$-有理 marked point がある場合の Dèbes–Emsalem 判定の整理。本稿の前件 (4c) と直結)
>
> 機構は上の証明(**$\mathrm{Aut}=1\Rightarrow$ 同型一意 $\Rightarrow$ cocycle 自動**)と同型である。札は **「要請中」→「引用確定(出版時に定理番号を精読)」** へ。
>
> **【重要・混同禁止】降下が与えるのは $\mathbb Q$-モデルの「存在」だけである。** 前件 (4) が要求するのは
> **明示** $\mathbb Q$-モデル(方程式)+ 選んだ sheet/frame の $\mathbb Q$-有理性 + actual marked identification + $\tau$ と局所 Kummer generator の一致 であり、これらは降下からは出ない。
> **したがって補題 Q + 降下は (4d) を「存在が保証された探し物」に格下げするだけで、(4) を弱めない。(4d)(5′) は UNKNOWN のまま動かさない**(便 30 F3.2 末尾・文献ゲート 01 の翻訳注意と一致)。
>
> **他窓への再利用の条件(便 30 F3.3)**: 補題 Q は $A_5$ と $K^{(3)}$ の field-of-moduli 段にも使えるが、**各窓で「$\Phi(\mathrm{GT}(N))$ が標的の『個々の』$P$-共役類を保つ」を確認してから**である。$\mathrm{Aut}$-軌道全体や複数クラスの和集合の安定性では足りない。**既存の明示モデルや exact marking を補題 Q で置換してはならない。**

### 6.3 【v1.1・全面強化】二 dessin の整合ゲート — 封印値 $a$ による Kummer 類の冪関係

> **v1 の弱さ(便 30 F2.3・W3 の指摘を受領)**: v1 は整合ゲートを「$\mathrm{ord}([u^{-1}]_{10})$ が一致する」と書いた。**これは弱すぎる**。逆に「生の $u_{\rm sq} = u_{\rm ns}$」を要求するのは**強すぎて誤り**である — 曲線・局所座標・actual marking が異なれば主係数そのものは異なりうる。正しい比較対象は、**共通の算術作用へ運ぶ作用同型 $j_i$ を通した Kummer character** である。

#### 6.3.1 $j_i$ の定義(有限群論だけで決まる)

各 $i\in\{\mathrm{sq},\mathrm{ns}\}$ について、$\Lambda_i$ 上には二つの単射がある:

$$ \tau_i:\ \langle X\rangle\ \hookrightarrow\ \mathrm{Sym}(\Lambda_i),\quad X\mapsto(H'\mapsto XH'X^{-1}) \qquad(\text{(3c) より regular}) $$
$$ \rho_0^{(i)}:\ \mathfrak F_0\ \hookrightarrow\ \mathrm{Sym}(\Lambda_i),\qquad \mathrm{im}\,\rho_0^{(i)} = \tau_i\bigl(\langle X^2\rangle\bigr) = \tau_i(\mu_M[e]) \qquad(\text{命題 K5-1}) $$

そこで**作用同型**を

$$ \boxed{\ j_i\ :=\ (\rho_0^{(i)})^{-1}\circ\tau_i\bigl|_{\langle X^2\rangle}\ :\ \mu_{10}[5]\ \xrightarrow{\ \sim\ }\ \mathfrak F_0\ } \tag{6.1} $$

と定める。(5′) が dessin $i$ で成立すれば $\mathrm{Ih}_N\bigl|_{G_K} = j_i\circ\kappa_i$($\kappa_i := \kappa_{u_i^{-1}}$)。両方で成立するなら

$$ j_{\rm sq}\circ\kappa_{\rm sq}\ =\ j_{\rm ns}\circ\kappa_{\rm ns} \quad\Longrightarrow\quad \kappa_{\rm ns} = a\circ\kappa_{\rm sq} = \kappa_{\rm sq}^{\,a},\qquad a := j_{\rm ns}^{-1}j_{\rm sq}\in\mathrm{Aut}(\mu_5)\cong(\mathbb Z/5)^\times. \tag{6.2} $$

#### 6.3.2 ★ 封印値 $a$ の確定(**$u$ の開示前・有限群論のみ**)

> **補題 K5-a.** 命題 K5-1 の下で $j_{\rm sq} = j_{\rm ns}$、すなわち
> $$ \boxed{\ a\ =\ 1\ \in(\mathbb Z/5)^\times.\ } $$

**証明**(1 行)。命題 K5-1 は $\Phi_{0,k} = \mathrm{inn}(\bar x^{-2k})$ を**自己同型として**与える。内部自己同型 $\mathrm{inn}(g)$ の任意の共役類 $\Lambda_i$ 上の作用は「$g$ による共役」だから、$i$ に依らず

$$ \rho_0^{(i)}(\Phi_{0,k})\ =\ \tau_i\bigl(X^{-2k}\bigr)\qquad(i = \mathrm{sq},\mathrm{ns}) $$

である。**【v1.2・便 31 F7.2 の型修正】** ここで $j_i$ の domain は $\mu_{10}[5]$ であるから、入力は $\tau_i(X^{2t})\in\mathrm{Sym}(\Lambda_i)$ **ではなく** $\zeta_{10}^{2t}\in\mu_{10}[5]$ である(v1.1 の $j_i(\tau_i(X^{2t}))$ という書き方は ill-typed だった)。両 dessin に**共通**の抽象同定

$$ \iota:\ \mu_{10}\ \xrightarrow{\ \sim\ }\ \langle X\rangle,\qquad \zeta_{10}\longmapsto X $$

を固定し、$\tau_i$ をこの $\iota$ を通した $\mu_{10}\hookrightarrow\mathrm{Sym}(\Lambda_i)$ と読む。$z = \zeta_{10}^{2t}\in\mu_{10}[5]$ に対して $j_i(z) = \Phi_{0,k}$ となる $k$ は、$\tau_i$ の単射性より $-2k\equiv2t\ (\mathrm{mod}\ 10)$、すなわち $k\equiv-t\ (\mathrm{mod}\ 5)$ で決まる。よって

$$ \boxed{\ j_i\bigl(\zeta_{10}^{2t}\bigr)\ =\ \Phi_{0,-t}\ }\qquad(\text{右辺は }i\text{ に依らない}) \tag{6.3} $$

— これは便 31 (7.2) と同一の式である。ゆえに $j_{\rm sq} = j_{\rm ns}$、$a = 1$。∎

> **型修正で何が変わらないか**: 証明の骨格(「$\mathrm{inn}(g)$ の各共役類上の作用は同じ群元 $g$ による共役」)も $a=1$ という結論も不変。変わったのは $j_i$ に食わせる対象の型と、共通同定 $\iota$ を**明示した**ことだけである。なお $\mathrm{inn}$ の規約を全体で反転しても両 $j_i$ が同じように反転するので $a = j_{\rm ns}^{-1}j_{\rm sq} = 1$ は不変(便 31 F7.2 末尾・検算 I4 と一致)。

**検算(二系統)**: node **I1–I4**(`j_{\rm sq} = j_{\rm ns} = [0,4,3,2,1]`、$a=1$)/ GAP **I1–I3**($a=1$)。GAP は共役規約 $H^g = g^{-1}Hg$、node は $gHg^{-1}$ で $j_i$ の向きが逆になるが、**両クラスで同一規約を使う限り $a$ は不変**(node I4 が逆向き規約でも同じ $a$ を出すことを明示検査)。

> **★ なぜ $a=1$ が「強い」か**: $a$ は $\Lambda_{\rm sq}$ と $\Lambda_{\rm ns}$ という**別々の集合**の上で定義された二つの同型の比較なので、先験的には $(\mathbb Z/5)^\times$ の 4 通りがありえた。**命題 K5-1 が「同じ群元 $\bar x^{-2k}$ が両方の detector を動かす」ことを言うので、二つの detector が自動的に coherent に正規化される** — これは K5-1 の副産物であって、独立の仮定ではない。

#### 6.3.3 封印する予測(結果値は含まない)

$$ \boxed{\ \text{(P-a)}\quad [u_{\rm ns}^{-1}]_{10}\ =\ [u_{\rm sq}^{-1}]_{10}^{\,a}\ =\ [u_{\rm sq}^{-1}]_{10}\quad\text{in}\quad K^\times/K^{\times10}\ } $$

— すなわち **二つの Kummer 類は(位数だけでなく)$K^\times/K^{\times10}$ の中で等しい**。§1.3 の (6.1)($\mathrm{ord}\in\{1,5\}$)と併せて封印する。

**前件(封印の有効条件)**: (P-a) は BRIDGE-IN で **両 dessin に同一の $\tau$ 規約**(原始根 $\zeta_{10} := \zeta_{20}^2$ の固定・$\tau_i(\zeta_{10})(H') = XH'X^{-1}$ の向き・Kummer cocycle を $\gamma(s^{1/10})/s^{1/10}$ と読む規約)を課したときの予測である。片方の actual marking が $\tau_{\rm ns} = \tau_{\rm sq}\circ[b]$($b\in(\mathbb Z/10)^\times$)を強いる場合の扱いは、**【v1.2 で全面差替え・撤回】**である。

> **【v1.2・便 31 F5 / 裁定 29-2 — v1.1 の記述を撤回】**
> v1.1 は「その $b$ を BRIDGE-IN に記録し **$a$ を $ab^{-1}$ 型に更新する**」と書いた。**これは誤りであり撤回する。** 誤りは二つある: ①$a$ は有限群側の **formal invariant(K5-1 の帰結)であり、永久に不変**でなければならない — 後から更新すると有限群入力と局所規約の provenance が混ざる(W3)。②捻れは片翼だけに起きるとは限らず、**dessin ごとの $b_{\rm sq},b_{\rm ns}\in(\mathbb Z/10)^\times$ の二側**として型付けすべきである($\lvert(\mathbb Z/10)^\times\rvert = \varphi(10) = 4$ — 候補は $1,3,7,9$ の四つ)。
> 正しい型は
> $$ c_i\ell_i c_i^{-1} = \tau_i\bigl(\zeta_{10}^{\,b_i}\bigr),\qquad a_{\rm eff} = [b_{\rm ns}]^{-1}\,a\,[b_{\rm sq}]\quad(a = 1\ \text{は不変}) $$
> で、封印予測の一般形は $[u_{\rm ns}^{-1}]_{10} = [u_{\rm sq}^{-1}]_{10}^{\,a_{\rm eff}}$。**運用は受理条件 $b_{\rm sq} = b_{\rm ns}$**(このとき $a_{\rm eff} = a = 1$ に戻り (P-a) の完全一致形が保たれる;不一致なら $u$ を開けず規約不整合で停止)。**決定式・tie-break・停止条件の正本は `docs/week4-K5_Rule1_v1.md` §4**(凍結 1 で封印)。

**$b_i$ を後から選んで不一致を吸収することは禁止**(それを許すと BRIDGE-FAIL が反証可能でなくなる)。$b_i$ は上の決定式が**機械的に一意に返す量**であって、選択の自由度ではない。

**破れたときの読み**: (P-a) が破れたら、それは新現象ではなく **(5′) か $\mathbb Q$-モデル/actual marking のどちらかの破れ**である(BRIDGE-FAIL 札)。

> **予測登録の可否(便 30 F2.3 末尾)**: (P-a) は「単なる整合確認」より強く、**BRIDGE-IN を独立に閉じた後なら真の盲検予測として登録してよい**。本稿は $a=1$ を**先に**確定し封印した — 順序は守られている。

---

## 7. B1–B5 判定表(便 24 と同じ枠)

**便 24 は「最小 faithful 推移作用を正本」として判定した。W4(「B2/B3/B5 は permutation representation ごとの判定」)に従い、両方の作用について記す。**

| 条件 | 最小 faithful(**次数 20**) | 標的(**次数 10**・本橋が使う) | 根拠 |
|---|---|---|---|
| **B1** relevant orbit の一意性 | **PASS** | **PASS**(同じ) | 命題 K5-0: $(10,10,10)$-marked 三つ組 48000 個 $=\lvert\mathrm{Aut}(G_5)\rvert$ ⇒ 自由推移(検算 G1・G2) |
| **B2** $\mathrm{Aut}(\text{dessin})=1$ | **FAIL**($\cong C_5$) | **PASS**($N_G(H)/H = 1$) | 次数 20: $N_{G_5}(U)/U\cong R/U\cong C_5$(検算 F7)。次数 10: 検算 D13 |
| **B3** $\lambda=0$ で全分岐 | **PASS**(型 $10^2$) | **PASS**(型 $10$・**1 点**) | 検算 F5 / D9-(3c)。標的側は $\lambda=0$ 上が 1 点なので**誘導加群不要**($K^{(3)}$ と同じ最良の状況) |
| **B4** relevant 中心化群が巡回 | **PASS** | **PASS**(作用に依らない) | $C_{G_5}(X) = \langle X\rangle\cong C_{10}$(検算 A10)。charming な全 $u$ で同じ($\gcd(u,10)=1$・A10b)。**★教材(便 24)**: $C_{G_5}(X^2)$ は位数 250 で非巡回 — B4 に代入禁止(A10c) |
| **B5** $k = N_{\rm ord}$ が素数 | **FAIL**($k=10$) | **FAIL**(形式上) | だが $K^{(3)}$ と同じく**分離される**: 核 $\mathfrak F_0\cong C_5$($5$ 素数 ⇒「非自明 $\iff$ 全位数」)と商 $(\mathbb Z/20)^\times$(円分指標が全射で埋める)。**B5 の危険は 5-primary 側では発生しない**(W6) |

> **総合**: **B1・B3・B4 PASS、B2 は表現依存(次数 10 で PASS)、B5 は形式上 FAIL だが primary 分離で無害。** $K^{(3)}$ とまったく同じ地形である。
> **便 24 の $n=3$ 判定(最小忠実 次数 12 で B2 FAIL)との整合**: $n=5$ でも最小忠実(次数 20)では B2 が $C_5$ で FAIL する。**「$P$ が $p$-群でなければ B2 は回避できる」ではなく、「作用を選べば回避できる」が正しい定式である**(委嘱 18 Q3 の★教材を、$n=5$ のデータで**訂正**する — §8 ★教材 2)。

---

## 8. dessin データ

### 8.1 標的(次数 10)

| 項目 | 値 | 検算 |
|---|---|---|
| 次数 | **10**($= M$) | D3 |
| ordered passport | $(\,10,\ 2^41^2,\ 10\,)$ | D6 |
| **種数**(Riemann–Hurwitz) | $2g-2 = -2\cdot10 + 9 + 4 + 9 = 2\Rightarrow\boxed{g=2}$ | D14(二系統) |
| $\mathrm{Aut}(\text{dessin})$ | $N_{G_5}(H)/H = \mathbf 1$ | D13 |
| monodromy 群 | $G_5/\mathrm{Core}(H)$、**位数 100**(核 $\cong C_5$)。$\cong\mathbb F_5^2\rtimes C_2^2$ | D12 |
| dessin の個数(この passport・この monodromy) | **2**(互いに非同型・§4.5)。**【v1.1】非同型は「固定した $U$ 上の ordered dessin(cover over the fixed $U$)」の圏での主張** — 基底三点の置換を許す圏や曲線のみの粗い同値では未分離(便 30 F2.1) | D15 |
| $\lambda=0$ 上の点 | **1 点**(分岐指数 10)⇒ $\mathbb Q$-有理 | (3c) |

### 8.2 最小 faithful transitive 作用

> **命題 K5-3.** $G_5$ の最小 faithful transitive 作用は**次数 20**である。

**証明**(便 24 F3.1 の $n=5$ 版)。$S\le G_5$ が core-free $\iff$ $S\cap R$ が座標線を含まない(§2.2 の指標分解 + $C_{G_5}(R)=R$ による;紙上)。$\lvert S\rvert$ の場合分け: $SR/R = C_2^2$ なら $S\cap R$ は $C_2^2$-安定 = 座標線の直和 ⇒ $0$、$\lvert S\rvert\le4$。$\lvert SR/R\rvert = 2$ なら $S\cap R$ は $q$-安定な平面で、$q$-安定平面は必ず座標線を含む ⇒ $\lvert S\cap R\rvert\le5$、$\lvert S\rvert\le10$。$SR/R=1$ なら $S\le R$ で、座標線を含まない平面が存在(法線ベクトルの三成分がすべて非零)⇒ $\lvert S\rvert = 25$。**最大は 25、最小次数は $500/25 = 20$。**∎(機械側は位数 50・100・125・250 の全部分群で core $\ne1$ を確認 — 検算 F2・F3、GAP は `ConjugacyClassesSubgroups` の全走査で `mindeg = 20` — F4。)

| 項目 | 値 | 検算 |
|---|---|---|
| 次数 | **20** | F4(二系統) |
| passport | $(\,10^2,\ 10^2,\ 10^2\,)$(三点すべて semiregular) | F5 |
| **種数** | $2g-2 = -2\cdot20 + 3\cdot18 = 14\Rightarrow\boxed{g=8}$ | F6 |
| $\mathrm{Aut}(\text{dessin})$ | $N_{G_5}(U)/U\cong R/U\cong \mathbf{C_5}$ ⇒ **B2 FAIL** | F7 |
| monodromy | $G_5$ 全体(位数 500) | F8 |
| 座標線を含まない平面 | **16 個**、$G_5$-共役類 **4 つ**(各 4)⇒ 最小忠実 dessin も一意でない | F9 |

> $n=3$ との対照: 次数 12・種数 4・$(6^2,6^2,6^2)$・$\mathrm{Aut}\cong C_3$・平面 4 個で共役類 1 つ(便 24 F3)。**$n=5$ では最小忠実側でも一意性が壊れる**(4 類)。

### 8.3 一般奇数 $n$ の予測(candidate・未証明)

| 量 | 予測式 | $n=3$ | $n=5$ |
|---|---|---|---|
| 標的次数 | $2n$ | 6 ✓ | 10 ✓ |
| 標的 ordered passport | $(2n,\ 2^{n-1}1^2,\ 2n)$ | $(6,2^21^2,6)$ ✓ | $(10,2^41^2,10)$ ✓ |
| 標的種数 | $(n-1)/2$ | 1 ✓ | 2 ✓ |
| 標的 dessin の個数 | $(n-1)/2$ | 1 ✓ | 2 ✓ |
| 最小忠実次数 | $4n$ | 12 ✓ | 20 ✓ |
| 最小忠実 passport | $((2n)^2,(2n)^2,(2n)^2)$ | ✓ | ✓ |
| 最小忠実種数 | $2n-2$ | 4 ✓ | 8 ✓ |
| 最小忠実 $\mathrm{Aut}$ | $C_n$ | $C_3$ ✓ | $C_5$ ✓ |
| $\lvert\mathrm{Aut}(G_n)\rvert$ | $n^3\varphi(n)^3\cdot6$($n$ 素数なら $n^3(n-1)^3\cdot6$) | 1296 ✓ | 48000 ✓ |

> **2 点しかないので「予測登録」はしない**(v3 §6 の観測列プロトコルと同じ規律)。**$n=7$ で 3 点目が取れたときに初めて候補へ上げる。**

---

## 9. 検算と状態札

### 9.1 二系統(便 29 ⑧)

| ファイル | 系統 | 結果 |
|---|---|---|
| **`search/week4-k5-bridge-d1.mjs`** | node ESM。$D_5$ を整数 $2a+e$ で自前符号化、$500\times500$ 積表、左剰余類、$gHg^{-1}$。**証明書は最後の突合でのみ読む** | **87/87 PASS** |
| **`search/week4-k5-bridge-d1.g`** | GAP 4.16.0。fp 群 → `IsomorphismPermGroup` → `DirectProduct`、右剰余類、`H^g = g^{-1}Hg`、`AutomorphismGroup`・`ConjugacyClassesSubgroups` | **52/52 PASS** |

**ヘルパー非共有**を満たす(符号化・剰余類の向き・共役の向き・部分群列挙法がすべて別)。**規約差の吸収**: $\tau$ の向きが互いに逆になるが $\langle\tau\rangle$ と $\langle\tau^2\rangle$ は同一、cycle type も同一なので判定は不変(両スクリプトのヘッダに明記)。

### 9.2 突合(較正)

| 相手 | 項目 | 結果 |
|---|---|---|
| **C-1**(cross-checked) | $\lvert G_5\rvert = 4\cdot5^3 = 500$、$K_{\rm ord} = 10$ | 一致(A3・A2) |
| **C-4**(cross-checked・`K5.v1.json`) | $\lvert\mathrm{GT}(K^{(5)})\rvert = 40$・$\mathcal X_5$・`N_ord`・`index_PB3`・`derived_order = 125`・`thm46_expected_order = 40`・$m=0$ の $f$ 5 通り | 一致(H1–H5) |
| **便 24**($n=3$ の枠) | 符号表 (1.4)・B4 の $C_6$ と $C_{G}(X^2)$ の罠・最小忠実で B2 FAIL | 構造が完全に平行(A7b・A10・A10c・F7) |
| **定理 K3**($n=3$ の実測) | 同じ手計算を $n=3$ に流すと qualifying 18・good 12・bad 6・$\lvert\Lambda\rvert=3$ | `gap18a.json` と一致(§4.1 注) |

### 9.3 【GAP】と状態札

| # | 内容 | 状態 |
|---|---|---|
| **【GAP-K5a】** | (4d) 明示 $\mathbb Q$-モデル(次数 10・種数 2・$(10,2^41^2,10)$ の Belyi 写像)と actual marked identification | **開(次工程 S5 の本体)**。**補題 Q+降下により「存在は保証された探し物」**になったが、(4) は弱まらない |
| **【GAP-K5b】** | (5′) の構成(局所 Kummer と $\rho_0$ の比較) | **開**。**これは【GAP-Rcyc】の $n=5$ 実例**であり、一般化が族の定理への本丸 |
| ~~【文献要請 1】~~ | §6.2「$\mathrm{Aut}=1$ ⇒ field of moduli は field of definition」 | **閉(数学的な穴ではない)**。§6.2 で紙上完結・便 30 F3.2 と独立一致。**引用確定 = Dèbes–Douai 1997 + Sijsling–Voight 2016(出版時に定理番号精読)** |
| **【GAP-K5c】** | 標的 dessin は種数 2 で**楕円曲線ではない** — $K^{(3)}$ で使えた LMFDB Belyi(次数 6・種数 1)の直接類推は効かない可能性。次数 10・種数 2 のデータベース射程は未確認 | 中(次工程の律速) |
| **【GAP-K5d】** | §8.3 の一般奇数 $n$ の予測式は 2 点フィット。$n=7$ まで未検証 | 低(予測登録していない) |
| **【v1.1】【GAP-K5e】** | 命題 K5-2b(§3.4.1)の $4\mid n$ での (4.4) は便 30 F4.3 から受領。**私は偶数 $n$ の半直積座標を自分では検算していない**($n$ 偶では $2$ が $\mathbb Z/n$ で非可逆) | 中。**$n=8$($\lvert G_8\rvert = 256$・安価)で負較正を撃つことを提案(§12.2 論点 3)** |
| **【状態】** | 群論部分(§2–§5・§7・§8・§6.3.2)= **`paper + two-system cross-checked`**。**補題 Q(§6.1)・§6.2 の降下・補題 K5-a の紙上証明 = `paper / two-mathematician PASS`(便 30 F3.1/F3.2 検分)**。§8.3 の一般 $n$ 予測 = 紙上単系統・2 点フィット。算術部分 = **未着手**。**`verified`(Lean)ではない** | — |

> **札の射程分け(★教材 11 の遵守)**: 「二系統一致」は**証明書の粒度**で主張する。本稿で二系統(node+GAP)が覆うのは **§2 の基本量・§3 の GT 構造・§4 の列挙と分裂・§5.1 の (3)(6′) 判定・§5.3 の $\Phi$ 単射・§6.3.2 の封印値 $a$・§7 の B1–B4・§8.1/8.2 の dessin データ**である。
> **補題 Q(§6.1)・§6.2 の降下・補題 K5-a の紙上証明・§8.3 の一般 $n$ 予測は紙上**であり、`two-system cross-checked` とは名乗らない。ただし**補題 Q と §6.2 は便 30 F3.1/F3.2 が独立に書き下ろして一致した**ので `two-mathematician PASS` の札は付く(機械照合の札とは別物)。**§8.3 の予測は 2 点フィットで、どちらの札も付かない。**

---

## 10. v3 §5.2.5 事前登録表の **$n=5$ 欄**(条件判定のみ・結果値なし)

| 種別 | 条件(v3 のまま) | **$n=5$ の判定** |
|---|---|---|
| **適用条件(scope-in)** | (0)(1)(2)(3)(4)(5)(5′)(6′) がすべて成立 | **群論側は全 PASS**((0)(1)(2)(3a–d)(6′-i)(6′-ii))。**(4a)(4b)(4c) PASS(紙上)**、**(4d)(5′) は次工程 — 現時点で scope-in は「条件つき」** |
| **反証条件(falsify)** | 適用条件を満たす窓で $\mathrm{ord}([u^{-1}]_M)=e$ なのに非全射 / $<e$ なのに全射 | **未試験**((4d)(5′) 待ち)。試験可能になった時点で $e=5$ に対して実行する |
| **射程外(scope-out・棄却ではない)** | (3) 破れ / $\Lambda$ が $\Phi(\mathfrak F_0)$-不安定 / $\rho_0$ 非忠実 / (2) 破れ | **標的では該当なし**。**ただし bad 側 10 個($\lvert\Lambda\rvert=5$)は (3) 破れで scope-out**(§4.4)— これは「射程外の実例が同じ窓の中に同居する」初の記録 |
| **【v1.1・裁定 26-3】SCHEMA-OUT の将来欄** | 現行 $R^{\rm cyc}$($\rho_0 = \Phi\vert_{\mathfrak F_0}$ を detector にする形)が原理的に適用できない窓 | **$8\mid n$ の $K^{(n)}$ を一律登録**(命題 K5-2b・(4.5)(4.6))。$\rho_0$ が $\Lambda$ の選び方に依らず非忠実。**$n=24$ は差戻し**(数値的に最小の repeated-primary 窓だが、スキーマ上の最初の適用候補ではない)。**$K^{(8)}$ は SCHEMA-OUT の負較正**(既知の飽和結果 Thm 5.3 との比較用であり、legacy regression test の正例ではない) |
| **legacy regression test(旧「$q$-版の反証条件」)** | $\gcd(e,M/e)>1$ の窓で $K(u^{1/e})\ne\mathrm{Fix}(\ker\mathrm{Ih}_N)$ | **$n=5$ では試験不能**($\gcd(5,2)=1$)。**奇数族全体で永久に試験不能**(命題 K5-2)。**さらに $K^{(n)}$ 族の repeated-primary 側は SCHEMA-OUT**(上欄)⇒ **この族の中では原理的に実行できない**。転進先は ①族外の忠実 detector 窓 ②中心 $C_2$ を測る拡張スキーマ(§3.4.1) |
| **縮約の反証条件** | (1)(3) 成立の窓で $\rho_0(\mathfrak F_0)\not\subseteq\tau(\mu_M)$ | **反証されず。** それどころか命題 K5-1 が $\rho_0(\mathfrak F_0) = \tau(\mu_M[e])$ を**等号で**、しかも全奇数 $n$ で与えた |
| **(便 29 ⑥)整合の事前枠 1** | — | $\mathrm{ord}([u_i^{-1}]_{10})\in\{1,5\}$($i=\mathrm{sq},\mathrm{ns}$)。**$2$ か $10$ が出たら警報**(§1.3) |
| **【v1.1・便 30 P4】整合の事前枠 2(主整合ゲート)** | — | $[u_{\rm ns}^{-1}]_{10} = [u_{\rm sq}^{-1}]_{10}^{\,a}$、**$a = 1$(§6.3.2 で確定・封印・二系統)**。位数一致より強い。破れたら BRIDGE-FAIL |
| **【v1.1】採否ポリシー** | — | **`target_policy = all_two_classes`**: `K5-sq` / `K5-ns` を別 fixture(hash つき)で走らせ、**結果後の片方棄却は NO-GO**(裁定 26-6) |

---

## 11. ★ 教材

1. **【本稿発】「$\mathrm{Aut}(P)$-軌道が一つ」から「$P$-共役類が一つ」は出ない。** $n=5$ の標的 40 個は $\mathrm{Aut}(G_5)$-軌道 1 つだが、$G_5$-共役類は 4 つ(ordered passport で 2 分割 × $\alpha$ の平方剰余性で 2 分割)。**dessin を決めるのは後者**である。$n=3$ で両者が一致していたのは $\mathbb F_3^\times = \{\pm1\}$ という偶然。
2. **【本稿発・委嘱 18 Q3 の訂正】B2 が bite するかは「$P$ が $p$-群か」では決まらない。** 委嘱 18 は「$K^{(4)}$($P$ が 2 群)で全滅、$\lvert G_3\rvert = 2^2\cdot27$ で回避可能」から「素因数構造で決まる」と書いた。**$n=5$ のデータは、最小忠実作用では $n=3$ も $n=5$ も等しく B2 FAIL($C_3$ / $C_5$)であり、回避は「作用の選択」でしか起きないことを示す。** 正しい定式は W4(「B2 は permutation representation ごとの判定」)である。
3. **【W2 の三度目】cycle type は部分群を同定しない。** $\mathrm{Sym}(10)$ の型 $5.5$ の元 72576 個が生成する $C_5$ は **18144 個**。$\rho_0(\mathfrak F_0)$ を $\tau(\mu_{10}[5])$ と同定する根拠は**型ではなく「$\mathfrak F_0$ は $\bar x$ を固定する」という定義的事実**であり、そこから内部自己同型性(命題 K5-1)まで一意に決まる。
4. **【便 29 ⑤・本稿で確認】passport は符号で先に絞れる。** 次数 $d$ の dessin で三つの分岐型の符号の積は $+1$ でなければならない。$P$ の元の位数が $(10,10,10)$ でも coset 作用の passport は $(10,10,10)$ になり得ない。**「元の位数」と「置換の型」を混同しない。**
5. **【便 29 ①・本稿で実例化】「$\lvert\Lambda\rvert$ を $e$ に合わせたくなる」誘惑は同じ窓の中に実在する。** $K^{(5)}$ の bad 側 10 個はまさに $\lvert\Lambda\rvert = 5 = e$ を持つ。**detector の次数は $M$ であって $e$ ではない** — $\tau$ の単射性(= 局所 Kummer torsor)が判定の生命線だから。
6. **【本稿発】GT の構造が幾何を制約することがある。** 「2 つの dessin が $\mathbb Q(\sqrt5)$ 上で共役では」という自然な懸念を、$\Phi(\mathrm{GT})$ が 2 類を保つという**有限計算**が否定した(補題 Q)。**幾何側の descent 議論を、GT 側の群論で置き換えられる場合がある。**
7. **【本稿発】前件を族全体で構造的に閉じられるなら、機械計算は「較正」に降格する。** $K^{(3)}$ の【GAP-18a】は命題 K5-1 で不要になる。**個別窓で機械に頼った 1 ビットが、族の構造で消えることがある** — 第三例を取る本当の価値はここにあった。
8. **【v1.1・便 30 ★1 / 裁定 26-3 = 工房★教材 14】族の中で欲しい算術 regime が現れる条件と、detector がその成分を見失う条件が一致することがある。** $K^{(n)}$ 族では**どちらも $8\mid n$**。「最小の repeated-primary 窓 $n=24$ を撃つ」という計画は、**その窓で detector が死ぬ**という理由で無効になった。**regime の存在条件と観測可能性は別々に確認せよ。**
9. **【v1.1・便 30 ★2】outer action の inner ambiguity は部分群の共役類には見えない。** だから field of moduli には (K3‡) の exact lift が不要(補題 Q・(3.3))。**しかし actual marking と局所 $\tau$ には再び exact data が要る** — 「安くなった段」と「安くならない段」を取り違えない。
10. **【v1.1・便 30 ★3】複数 detector の正しい一致条件は、生の局所係数の一致ではない。** 共通の算術作用へ運ぶ作用同型 $j_i$ を通した character の一致である($a$ による冪関係・§6.3)。**「$u$ が同じはず」も「位数だけ同じはず」もどちらも誤り。**
11. **【v1.1・便 30 W4】同型を主張するときは圏を書く。** 二 dessin の非同型は「固定した $U$ 上の ordered dessin」の圏での話。基底三点の置換を許す圏では未分離(§4.5)。★教材 1(Aut-軌道と $G$-共役類の区別)の圏論的な顔である。

---

## 12. 論点

### 12.1 便 30 への論点(v1 発・**回答先を付記**)

> **便 30 の回答先**: 1 → F1.1/F1.2(PASS・inn の規約明記を要求 → E1 で反映)、2 → F1.3(PASS・過去文書は編集せず次版 addendum → K3 v3.2 addendum で対応)、3 → F3.1/F3.2(PASS・型を一箇所修文 → E2/E3 で反映)、4 → F4.3(**差戻し** — $n=24$ は SCHEMA-OUT → E5 で反映)、5 → F2.3(整合ゲートを $a$ へ強化 → E7 で反映)、6 → F3.2(数学的な穴ではない・引用は出版時 → E4 で反映)。**すべて v1.1 に反映済み。**

1. **命題 K5-1(§5.4)の 4 段**に穴はないか。とくに段 3 の「生成元像の一致で $\Phi_{0,k} = \mathrm{inn}(e^{(-2k,0,0)})$」と段 2 の「$n$ 奇 ⇒ $2$ が $\mathbb Z/n$ で可逆」の使い方。**もし正しければ、$R^{\rm cyc}$ の前件 (6′) は奇数族全体で自動になり、v3 §5.2.3 の「第三例で確認すべき 1 項目」は $n$ 奇では消える。**
2. **遡及効果の確認**: 命題 K5-1 を $n=3$ に適用すると、定理 K3 §4 の条件 4(【GAP-18a】)は**紙上で閉じる**。定理 K3 の依存表を改訂すべきか(v4 を起こすか、注記に留めるか)。
3. **補題 Q(§6.1)**は正しいか。とくに「$\beta_\sigma\in\Phi(\mathrm{GT}(N))\cdot\mathrm{Inn}(P)$ で足りる((K3‡) の厳密等式は不要)」という軽量化。もし正しければ、$A_5$ と $K^{(3)}$ の (P7)(残留 descent なし)も本補題で置き換えられるか。
4. **§3.4 命題 K5-2(regime は $8\mid n$ でしか repeated-primary にならない)**の帰結として、便 28 P4 の「repeated-primary 優先」と研究者裁定の「奇数族横展開」は**直交する二本の攻め手**になる。$n=24$($\lvert G_{24}\rvert = 6912$)は現実的な計算対象か、それとも $q$-版の反証は別の手段(例えば $K^{(8)}$ で既知結果と突合する較正)で撃つべきか。
5. **§4.5 の 2 dessin**について。群論側は完全に同型な入力を与えるので (5′) が両方で成立するはずだが、**$u$ が異なる値になる可能性は排除できない**(§6.3 の整合検査)。この検査を「盲検の予測登録」として扱ってよいか、それとも「単なる整合確認」に留めるべきか。
6. **【文献要請 1】(§6.2)**について、正典の範囲で代替できるか(2401/2405 は dessin に言及がないので難しいと見ているが、$A_5$ v4 §3 の descent 議論に同型の補題が既にあるなら再利用したい)。

### 12.2 便 31 への論点(v1.1 発)

1. **補題 K5-a($a=1$・§6.3.2)**の 1 行証明に穴はないか。とくに「$\mathrm{inn}(g)$ の任意の共役類上の作用は $g$ による共役だから $i$ に依らない」という一段。**もし正しければ、$a$ は「二 detector が K5-1 により自動的に coherent に正規化される」ことの表明であり、独立の封印情報を持たない** — この読みでよいか(それでも封印する価値はあると考えている: BRIDGE-IN で $\tau$ 規約が片方だけ捻れた場合に $a$ がずれるので、**$a$ は「規約の捻れ検出器」として機能する**)。
2. **§6.3.3 の前件**($b\in(\mathbb Z/10)^\times$ による $\tau$ の捻れが actual marking から強制された場合の $a\mapsto ab^{-1}$ 更新)を、BRIDGE-IN の封印項目としてどう書けば「後から $b$ を選んで不一致を吸収する」を排除できるか。**$b$ を先に(モデル探索の前に)全 4 通り(または 8 通り)列挙して、それぞれの (P-a) を封印しておく**という運用は過剰か。
3. **命題 K5-2b(§3.4.1)の射程**: 私は $4\mid n$ で (4.4) が成立することを便 30 F4.3 から受領したが、**自分では偶数 $n$ の半直積座標を検算していない**($n$ 偶では $2$ が $\mathbb Z/n$ で非可逆なので §5.4 段 3 の議論がそのままは通らない)。$8\mid n$ の SCHEMA-OUT を manifest に登録する前に、**$n=8$ で有限計算による較正($\lvert G_8\rvert = 4\cdot4^3 = 256$ — 安価)**を撃つべきか。私はこれを撃つ価値があると考えている(負較正の実データになる)。
4. **攻略分岐の優先**(§3.4.1): ①$K^{(n)}$ 族外の忠実 detector 窓 ②中心 $C_2$ を測る拡張スキーマ。**私は ② の設計の方が族の定理に効くと見ている**($\Phi$ が中心を潰すのは $\mathrm{Aut}(P)$ を detector に使う限り一般に起きうる現象で、$\Lambda$ 以外の付加構造 — 例えば $\Lambda$ 上の**線束/接方向**や $P$ の中心拡大 — で測るのが自然)。あなたの見立ては。
5. **$n=7$ の位置づけ**: §8.3 の一般奇数 $n$ 予測表は 2 点フィットである。$n=7$($\lvert G_7\rvert = 1372$・$M=14$・$e=7$・標的 dessin 3 個・種数 3)を **finite gate だけ**撃って 3 点目を取るのは、$n=5$ の S5(明示モデル)より先に回すべきか、後か。**私は「$n=5$ の S5 が律速で、その間に $n=7$ の finite gate は安価に並走できる」**と見ている。
