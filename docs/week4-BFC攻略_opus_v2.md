# 比較橋 $B_{\rm FC}$ の紙上攻略 — 前件の精密化と一般証明(**v2.1 = 便 44 修文 T1–T7 反映版**)

2026-07-27 起草(v1)・**同日 v2 改訂・同日 v2.1 修文**: Claude(数学者レイヤー・Opus 5)。司令塔委嘱「$B_{\rm FC}$ の紙上攻略」。**v2 は `sol/sol_reply_43_bfc.md`(条件付き PASS)の必須修理 R1–R6 を反映(裁定 44)。v2.1 は `sol/sol_reply_44_bfc_v2.md`(本体 PASS 確定・付随 artifact に修文指定)の T1–T7 を反映(裁定 46)。**
**版の所在(便 44 F8)**: **v1 の原文は `docs/week4-BFC攻略_opus_v1_archive.md` に復元済み**(digest `659a9570…`)。本ファイルは v2 以降の系列を保持する。**便 44 F8 は最終正本を `docs/week4-BFC攻略_opus_v2.md` へ新規固定するよう求めており、path の改称は司令塔の裁定事項として残る**(数学的判定には影響しない)。
入力: `docs/week4-K3飽和_opus_v3.md`(v3.1–v3.3 = $B_{\rm FC}$ の定義・(5′) の型・§2.6)・`docs/week4-A5算術飽和_v4.md`(§1.4 較正・§3 FC-1〜FC-7)・`sol/sol_reply_29_v3delta.md` F1・`sol/sol_reply_31_manifest.md` F5・`docs/week4-K5_Rule1_v1.md` §1・§7・**`sol/sol_reply_43_bfc.md`(全文)**。
検算: `search/week4-bfc-antecedents.mjs`(**Node 13/13 PASS**・本稿発)+ `search/bfc-antecedents-check.g` / `certificates/bfc/bfc-antecedents.json`(**GAP 17/17**)。便 43 F1・便 44 F1 が独立再走で再現。**【v2.1・T7】序列は `source-audited candidate`** — 二系統の数値(1296/432/12)は一致するが、**便 44 F6.1 の marked-fidelity blocker($x_gy_gz_g
e1$)が未閉鎖**のため `cross-checked` とは名乗らない(§15.7)。
**規律**: $K^{(5)}$ の個別モデル・$u$ には一切触れていない(紙上の一般論のみ)。外部文献は使っていない(§12 に【文献要請 13】を 1 本立てる)。

---

## v1 → v2 差分一覧(便 43 の必須修理 R1–R6)

| # | 箇所 | v1 | v2 | 出所 |
|---|---|---|---|---|
| **R1** | §5 命題 B-2・§0-8・§3・§13.2・付録 B | 「$\lvert\Lambda\rvert=M\iff[P:H]=M\iff N_P(H)=H$」という**三者 pairwise 同値**(**偽**) | **(B2-corr) 結合形**へ置換: $\lvert\Lambda\rvert=M\iff\bigl([P:H]=M\ \text{かつ}\ N_P(H)=H\bigr)$。**Sol の反例 $P=S_3\times C_2$ を本文に採録**。「$P/H\to\Lambda$ 全単射 $\iff N_P(H)=H$」は $M$ と無関係に成立と明記 | 便 43 F2.1 |
| **R2** | §5 定理 B-3・§0-1・§4 段表 | B-3 の前件を (W1)(W2)(W4)(W5) と書いた | **(W3) を追加**((W3) なしでは $\tau(\mu_M)$ が regular にならない。**Sol の反例 $P=C_M\times C_2,\ H=C_2$ を採録**)。「型は無料」の意味を「**regular detector (W3)(W4) を払った後は追加の幾何入力が不要**」に精密化 | 便 43 F2.2 |
| **R3** | §6 定理 B-4・補題 B-4b | $K$-版の前件から (W2) が脱落 | **$K$-版に (W2) を追加**し、$\mathbb Q$-版((W5$^\mathbb Q$) 使用・(W2) 不要)と**定理文を分離**。F3.3 の「部分群の一意性 → 被覆の一意性」の一行も追加 | 便 43 F3.2・F3.3 |
| **R4** | §6.3 系 B-4c・§8 | $\mathcal H\backslash\pi_1$・$\tilde H\backslash\hat F_2$ と書き、非正規部分群で左右剰余類を無根拠に同一視 | **全編を左作用・左剰余類 $\pi_1/\mathcal H$・$\hat F_2/\tilde H$ に統一**。$\mathrm{Stab}(g\tilde H)=g\tilde Hg^{-1}$ が左剰余類の公式であることと整合。**§8 の $b=1$ の向きを支える箇所ゆえ必須修理** | 便 43 F4 |
| **R5** | §4 依存表 | II-c 欄が (TB1)(TB2)+(W4) だけ | **(TB3)(TB4) と間接依存を復帰**。さらに「**$W_0$ が与えられた局所補題**」版と「**窓から $W_0$ を構成する主定理**」版に段を分離 | 便 43 F5.2 |
| **R6** | §13.3・§10・§12.1 | (W5) 不成立 ⇒ $K$-モデルなし / 証明書未取得 ⇒ MODEL-MISMATCH / $b\ne1$ ⇒ TB2 違反 | **三つとも過剰推論として修理**: (W5) は十分条件にすぎない・`MODEL-UNKNOWN` と `MODEL-MISMATCH` を分離・$b\ne1$ の診断先を **TB2/TB4/左右作用/共役 transport** へ拡張。**§13.3 を便 43 F9 の 6 層表に差し替え** | 便 43 F6.2・F9 |
| **S1** | §12.1・§0-6 | 「(TB4) **だけ**が load-bearing」 | **射程限定**: 「**exact $b=1$ の向きについて唯一 load-bearing**」。(TB1)(TB3) も真に破れれば記法問題では済まない。札は `TB1–TB4 = global framework assumptions` / `TB4 = unique orientation-sensitive literature gate` | 便 43 F7 |
| **S2** | §11.2・§0-7 | 「(W5) は 432/1296 で非自明」 | **(W5) 自体は包含条件**(3 元/12 元が 432 元の setwise stabilizer に入る)。432/1296 はそれが自明でないことを示す**周囲のデータ**。数値は `source-audited single-system candidate` | 便 43 F8.1 |
| **S3** | §11.2・§15-5 | 「V6・V7 は定理 K3 §2.2 (P7) への独立な第二証明」 | **射程限定**: **(P7) の非標識 $\mathbb Q$-descent 部分**への第二証明。モデル認識・ordered passport・exact conjugator・$u$ 抽出は**置換しない**。また「有限群論だけ」ではなく **V6 + B-4 の descent 枠組みの合成** | 便 43 F8.2 |
| **S4** | §14 論点 1・2 | 自己申告 A-1(cocycle の向き)・A-2((TB4) 適用) | **便 43 F3.1・F6.1 でいずれも閉鎖**。A-1 は無条件、A-2 は「(TB4) をこの向きで採用する限り」条件つき。§12.3 を判定つきに更新 | 便 43 F3.1・F6.1 |

> **不変**: **主定理 B-7 の主張と結論・(9.1)・系 B-7′・補題 B-5・補題 B-6 の計算・系 B-8・§7 の全論証・二例との整合(§11.1・§11.3)・検算値 13/13。** R1–R6 は**前件欄の脱落補填・偽の同値の結合形化・剰余類記法の統一・札の射程限定**であり、**数学的結論を 1 ミリも動かさない**(便 43 F7 が同旨)。

> **状態札**(便 43 F10 → **便 44 F9 で確定**):
> $$ \boxed{\ B_{\rm FC}\ (\text{定理 B-7})\ =\ \texttt{paper-proof (framework-conditional on TB1--TB4) / two-mathematician audit PASS}\ } $$
> — ただし **(i) Lean `verified` ではない(未着手)**、**(ii) exact $b=1$ の向きは (TB4) 関所待ち**(**【v2.1・T1 で訂正】**その手前の orientation-free 版 B-7$^{\rm tw}$ は**無条件ではなく (TB4$^{\rm u}$)-条件つき** — §8.1)、**(iii) 有限計算 bundle は `source-audited candidate`**(Node 13/13 + GAP 17/17 は強い傍証だが、**便 44 F6.1 の marked-fidelity blocker が未閉鎖** — §15.7)。

---

## v2 → v2.1 差分一覧(便 44 の修文指定 T1–T7)

| # | 箇所 | v2 | v2.1 | 出所 |
|---|---|---|---|---|
| **T1** | §4 注・§9 状態札・§10・§12.1・§14.1-2 →**§8.1 を新設** | 「単位 $b$ を伴う twisted bridge は**無条件**に定理化できる」 | **撤回**。B-8 は (10.1) を**仮定したとき**の不変性補題であって、$\exists b$ の**存在**を与えない(循環)。**(TB4$^{\rm u}$)(生成元の exact 一致を要求しない局所慣性比較)を新設し、補題 B-6$^{\rm tw}$・定理 B-7$^{\rm tw}$ を §8.1 に立てる**。状態は **orientation-free だが (TB4$^{\rm u}$)-条件つき** | 便 44 F7.1・F7.2 |
| **T2** | 付録 A の $b$ | $c_\Lambda m(\zeta_M)c_\Lambda^{-1}=\tau(\zeta_M^{b^{-1}})$ と定義しながら §10 は $\kappa^b$ を使い、**Rule 1 (7.1) と逆数で食い違っていた** | **Rule 1(凍結済・正本)へ統一**: $\boxed{c_\Lambda m(\zeta_M)c_\Lambda^{-1}=\tau(\zeta_M^{b})}$。導出では $b=\varepsilon^{-1}\bmod M$。exact (TB4) は $\varepsilon=1$ すなわち $b=1$ の特殊化 | 便 44 F7.3 |
| **T3** | 付録 A の $c$ | 「定理 B-3 で**無条件に**存在」 | **「定理 B-3 の (W1)–(W5) の下で存在」**(R2 と矛盾する stale statement) | 便 44 F2.2 |
| **T4** | §6.2 (6.1) 直後 | $C_\gamma=\tilde Hc_\gamma$ を「左剰余類」と呼んでいた | **「右剰余類」**へ訂正(式と cocycle 計算は正しい・§6.2 後段の説明とも整合) | 便 44 F2.4 |
| **T5** | §7 補題 B-5(ii) | 「uniformizer にも $K$-モデルにも依らない」を 1 文で主張し、前件を (TB1)–(TB4)+(W4) と書いた | **B-5$_{\rm loc}$(所与 $W_0$・uniformizer 不変)と B-5$_{\rm win}$(モデル不変・定理 B-4 に依存)に分離** | 便 44 F2.5 |
| **T6** | §3・§6 見出し・§13.2 | 「明示 $\mathbb Q$-モデル・$\mathbb Q$-有理 cusp $\Longleftarrow$ (W3)(W4)(W5)」(**偽**) | **$K$/$\mathbb Q$ を分離**: $K$-モデルは (W1)(W2)(W3)(W5)+(CAL)、$\mathbb Q$-モデルは (W5$^\mathbb Q$) 要。cusp の有理性も **$K$-有理 = B-4(a)+(W4) / $\mathbb Q$-有理 = B-4(b)+(W4)**。**橋 B-7 には $K$-モデルで足りる**ことを理由として明記 | 便 44 F4 |
| **T7** | §15-5・§15-7・§11.2 | 「single-system candidate」「第二系統を発注」 | **GAP 第二系統は完成済(17/17 受領)だが、便 44 F6.1 の marked-fidelity blocker(下記)により `cross-checked` は保留**。§15.7 を「発注」から「**F6.3 の 5 項目の修理指示**」へ差し替え | 便 44 F6 |

> **【v2.1・T7 の中身 — 私が独立に再現した便 44 F6.1】** `search/bfc-antecedents-check.g` は $y$ を GAP 右作用側へ移送($rs\rightsquigarrow s*r$)しながら $z$ を論文座標のまま置いており、$D_3^3$ で
> $$ x_g\,y_g\,z_g\ =\ (r,\ 1,\ r^2)\ \ne\ 1 $$
> となる(**本稿で独立検算・Sol の値と完全一致**)。正しくは `zg := (xg*yg)^-1`、座標では
> $$ (x_gy_g)^{-1}\ =\ (s,\ r^{-1}s,\ r^{-1}) $$
> (**これも独立に再現・Sol の $\Phi(r^2s,r^{-1}s,r)=(s,r^{-1}s,r^{-1})$ と一致**)。**⇒ 現 GAP checker は「同じ marked object を照合した」型を満たしていない。数値の一致は強い傍証だが、bundle の公式札は `source-audited candidate` を維持する。**

> **v2.1 でも不変**: **主定理 B-7 の主張・(9.1)・証明・系 B-7′・補題 B-5 の計算・補題 B-6 の計算・系 B-8・二例との整合・Node 検算 13/13。** T1–T7 は**別番号定理の条件付け・規約の逆数統一・stale statement の除去・依存の分割**であり、**B-7 の真偽を動かさない**(便 44 F5 が同旨)。

---

## 0. 判定(先に 10 行)

1. **$B_{\rm FC}$ は 2 段に分解する。第 1 段は(regular detector を払った後は)無料、第 2 段が全内容である。**
 - **$B_{\rm FC}$-I**(型の段): $G_K$ 上で $\rho_\Lambda\circ\mathrm{Ih}_N$ が $\tau(\mu_M)$ 内の平行移動になる、すなわち $\exists!\,c\in\mathrm{Hom}(G_K,\mu_M)$ で $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(c(\gamma))$。→ **証明済み(§5・定理 B-3)。前件は (W1)(W2)(W3)(W4)(W5) の有限群論だけで、追加の幾何入力(較正・モデル・cusp)を要さない**(**【v2・R2】**: v1 は (W3) を落としていた。$P=C_M\times C_2,\ H=C_2$ が反例 — 便 43 F2.2)。
 - **$B_{\rm FC}$-II**(同定の段): その $c$ が $\kappa_{u^{-1}}$ である。→ **本稿で証明した(§6–§9・定理 B-7)。**
2. **$B_{\rm FC}$-II はさらに 3 枚に割れ、3 枚とも閉じた**: **II-a** 剛性 descent(§6・定理 B-4)/ **II-b** torsor 比較と $b=1$(§8・補題 B-6)/ **II-c** cusp の局所 Kummer(§7・補題 B-5)。
3. **前件 (4) から「明示 $\mathbb Q$-モデル」「明示局所助変数」「actual marking(exact conjugator)」は消える。** これらは橋の前件ではなく、**$u$ を計算するための窓固有の作業**であり、橋の外にある(§12.2・命題 B-9 で分離)。
4. **前件 (5)(FC-2b/FC-3)は残るが、FC-3 は前件ではなく帰結になる** — (W3)(W5) から $K$-モデルと $\mathrm{Fib}\cong\Lambda$ が**構成できる**(§6)。残る真の入力は較正 FC-2b($A_5$ v4 で証明済・窓非依存)のみ。
5. **$b$ の自由度は二重に吸収される**: (i) 規約 (TB2) の下では $b=1$ が**定理**である(§8)。(ii) 仮に $b\ne1$ でも $R^{\rm cyc}_{\rm formal}$ の結論は $b$ で不変(§10・系 B-8・検算 V8)。Rule 1 (7.1)(7.2) の $b_i$ 欄は**規約監査**であって数学的穴ではない(ただし $K^{(5)}$ の二 dessin 比較 $a_{\rm eff}$ では依然 load-bearing)。
6. **閉じなかったもの = 枠組み札ただ 1 枚**:【GAP-TB】= 接基点繊維関手の 4 性質 (TB1)–(TB4)。これは新しい穴ではなく、**$A_5$ v4 の【GAP-C3】(Deligne 1989 §15)を 4 項目に鋭くしたもの**である。両実例も暗黙に同じ 4 つを使っていた。**【v2・S1】札の書き方**: $\texttt{TB1--TB4} =$ 全体枠組み仮定 / $\texttt{TB4} =$ **exact $b=1$ の向きについて唯一 load-bearing な文献関所**。(TB1)(TB3) も真に破れれば「記法だけ」では済まない(便 43 F7)。
7. **新しい前件を 1 本発見した**: **(W5) $\Lambda$ が $\Phi(\mathfrak F_0)$-安定**(v3.1 の (6′) 第 1 節)は、$K$-モデルの存在そのものを供給する。$\mathbb Q$-モデルには $\Phi(\mathrm{GT}(N))$-安定が要る。**$K^{(3)}$ でこれは自明でない**: $\lvert\mathrm{Aut}(G_3)\rvert=1296$ のうち $\Lambda$ を setwise に保つのは **432** 個で、$\Phi(\mathfrak F_0)$(3 元)も $\Phi(\mathrm{GT})$(12 元)もその中(**検算 V6・V7**)。**【v2・S2】(W5) 自体は「432/1296」ではなく「指定された像が 432 元の stabilizer に含まれる」という包含条件**であり、432/1296 は非自明性を示す周囲のデータである(便 43 F8.1)。
8. **前件 (3) の一部は導出できる**(**【v2・R1】結合形に修正**): 「$\langle X\rangle$ が $P/H$ 上推移的かつ $\lvert\Lambda\rvert=\mathrm{ord}(X)=M$」から **$[P:H]=M$ と $N_P(H)=H$ が同時に**従う(命題 B-2 (B2-corr))。**逆向きの各個同値は偽** — $N_P(H)=H$ だけでは $\lvert\Lambda\rvert=M$ は出ない(反例 $P=S_3\times C_2$・便 43 F2.1)。$K^{(3)}$ で悉皆確認(**検算 V3**: 該当 12 個・反例 0 — V3 は初めから結合形を検査している)。
9. **$R^{\rm cyc}$ の状態札は変わる**: $B_{\rm FC}$ は `candidate / UNKNOWN` から **`paper-proof (framework-conditional on TB1–TB4) / two-mathematician audit PASS`**(便 43 F10・裁定 44)へ。したがって $R^{\rm cyc}$ 全体(= $B_{\rm FC}+R^{\rm cyc}_{\rm formal}$)も同じ札になる。**`verified`(Lean)ではない。**
10. **五札(§5.2.5)は再構成が要る**: **【v2・R6】**便 43 F9 の **6 層表**(GLOBAL-FRAMEWORK / WINDOW-SCHEMA / MODEL / EXTRACTION / BRIDGE / ARITHMETIC)へ差し替える(§13.3)。v1 が書いた「BRIDGE-UNKNOWN の入口は (W5) 不成立と【GAP-TB】の 2 つ」は**過剰推論**で、**(W5) 不成立は「この有限 schema を適用できない」までしか言えない**($K$-モデルの非存在ではない)。

> **自制**: v1 は**私一人の紙上証明**だった。**v2 は便 43 の監査を通っている**が、閉じたのは「(TB1)–(TB4) を前件として採用した紙上証明」までである。$A_5$ v4 §1.4 が一度「証明した」と書いてから Sol の指摘で 2 度書き直された前例(補題 B の循環・W133)を忘れない。**v1 で私が立てた自己申告 2 件のうち、実際に修理が要ったのはそこではなく、私が申告していなかった 4 か所(B-2 の同値・B-3 の (W3)・B-4 の (W2)・B-4c の剰余類)だった** — ★教材 7。

---

## 1. 二例の並置 — 何が窓非依存で、何が窓固有だったか

$A_5$ v4 と $K^{(3)}$ v3.1 が **(5′) を閉じた論証**を段ごとに並べる。**「一般化の可否」欄が本稿の作業リストである。**

| 段 | $A_5$ v4 での実装 | $K^{(3)}$ v3.1 での実装 | 一般化 |
|---|---|---|---|
| **(a) 較正** $\alpha^{\rm Ih}=\alpha^{\rm std}$ | §1.4 補題 C・D0・D・系 E・補題 I3‡(自前証明) | §2.1 で **import**(便 27 F5 が PASS 確認) | **窓非依存・証明済**(v4 §1.4.2 の【P173】が既に明言)。**そのまま使う** |
| **(b) $\mathbb Q$-モデルの存在と一意性** | §3.4 FC-4: passport $(5,5,5)$・次数 5 の dessin が同型を除き一意(悉皆 192→120→軌道 2→$S_5$-軌道 1)+ $\mathrm{Aut}_U(W)=C_{S_5}(A_5)=1$ + $H^1(G_\mathbb Q,1)=1$ | §2.2 (P5)(P7): 明示平面モデル $F=t^2+(x-1)^2(4x-1)t+4x^6$ + $N_G(H)=H$ + (P4) exact conjugator | **一般化できた**(§6・定理 B-4)。**悉皆一意性も明示モデルも不要** — $N_P(H)=H$ から descent の cocycle 条件が自動で立つ |
| **(c) cusp の局所理論** | §3.5: $\mathbb Q((\beta))\otimes\mathbb Q(W_0)\cong\mathbb Q((\beta))[\xi]/(\xi^5+2\beta)$ を直接計算 | §2.1「局所 Kummer」: 全分岐点で $\lambda=u\,s^M(1+O(s))$ | **一般化できた**(§7・補題 B-5)。半局所 Dedekind 環の完備化 + Eisenstein のみ |
| **(d) torsor 比較** | §3.5 (3.5): $\gamma:\ j\mapsto\chi_5(\gamma)j+\kappa(\gamma)$ | §2.3(b): $G_K$ 上で $\chi\equiv1$ ゆえ線形部が消え平行移動のみ | **一般化できた**(§8)。しかも**「平行移動である」こと自体は無料**(§5) |
| **(e) $u$ の値** | §2.3 $z'^5=2t$ ⇒ $u=-1/2$ | §3 $t=4x^6+24x^7+\cdots$ ⇒ $u=-4$ | **窓固有**。橋の外(§12.2) |
| **(f) marked 同定** | (3.3) exact conjugator $h=(1\,3\,4\,5)$ | (P4) $h=[6,1,5,4,2,3]$ | **窓固有**。橋の外(命題 B-9 の前件) |
| **(g) 正規化不変性** | §2.4 Belyi 正規化 6 通りで $[2]^4$ 不変 | §3 Möbius 4 通り / ordered-passport 保存 2 通り | **窓固有**。$u$ の抽出の頑健性であって橋ではない |

### 1.1 抽出された共通機構(3 行)

> **(i)** $G_K$ 上では円分指標が自明になるので、$\Lambda$ 上の作用は $\langle X\rangle$-torsor の**平行移動だけ**になる。
> **(ii)** その平行移動指標は、$\Lambda\cong\mathrm{Fib}_{\vec{01}}(W_0)$ を通して、**全分岐 cusp の Kummer torsor の類**である。
> **(iii)** その類は Belyi 写像の cusp での主係数 $u$ で $[u^{-1}]$ と読める。

**(i) は無料**(§5)。**(ii)(iii) が橋の本体**(§6–§9)。両実例が実際に踏んだのはこの 3 段であり、**(b)(c)(d) に見えた「窓固有の工夫」は、一般論の特殊化にすぎなかった**。

### 1.2 見落としていた点(自認)

- v3.1 §5.2.5 の BRIDGE-IN は「**明示**モデル・**明示**局所助変数・actual marking」を封印対象に入れていた。これは**橋の前件と $u$ の計算手続きを混ぜている**。両者を分けると、橋の前件からは「明示」の語が全部落ちる(§13)。
- $A_5$ の FC-4(b)(passport の悉皆一意性)と $K^{(3)}$ の (P4)(exact conjugator)は、**同じ役割 = モデル認識**を果たしていた。これは橋ではなく、**「手元の明示曲線が $W_0$ である」ことの証明書**である(命題 B-9)。

---

## 2. 枠組み前件 (TB1)–(TB4) — 接基点繊維関手から使うものの悉皆

本稿が接基点の理論から使う性質を**全部**列挙する。以後これ以外は使わない(使ったら誤り)。記号は $A_5$ v4 §1.1 に従う: $U=\mathbf P^1_\mathbb Q\smallsetminus\{0,1,\infty\}$、座標 $\beta$、$\Omega:=\bar{\mathbb Q}\{\{\beta\}\}=\bigcup_n\bar{\mathbb Q}((\beta^{1/n}))$。

> **(TB1)(繊維関手)** 有限エタール $W\to U_k$($k\subseteq\bar{\mathbb Q}$ 有限次)に対し
> $$ \mathrm{Fib}_{\vec{01}}(W):=\mathrm{Hom}_{k((\beta))\text{-alg}}\bigl(\mathcal O(W\times_U\mathrm{Spec}\,k((\beta))),\ \Omega\bigr) $$
> は $\deg(W/U)$ 個の元をもつ集合で、$\mathrm{Fib}_{\vec{01}}$ は $\pi_1(U_k,\vec{01})$-集合の圏との同値を与える(Grothendieck–Galois)。
> **(TB2)(基点規約と $\zeta$ 系)** 整合的な $1$ の冪根系 $(\zeta_n)_n$($\zeta_{mn}^m=\zeta_n$)を固定する。$G_\mathbb Q$ は $\Omega$ に**係数のみ**で作用し、すべての $\beta^{1/n}$ を固定する。これが分裂 $s_{\vec{01}}:G_\mathbb Q\to\pi_1(U_\mathbb Q,\vec{01})$ を与える(作用は $\Omega$ への後合成)。
> **(TB3)(幾何的基本群)** $\pi_1(U_{\bar{\mathbb Q}},\vec{01})\cong\hat F_2=\langle x,y\rangle$、$x,y,z=(xy)^{-1}$ はそれぞれ $0,1,\infty$ の慣性生成元、$xyz=1$。
> **(TB4)(慣性の正規化・exact 版)** $x$ は $\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))\cong\hat{\mathbb Z}(1)$ の、**$(\zeta_n)$ が定める**位相的生成元 $\sigma_\zeta:\beta^{1/n}\mapsto\zeta_n\beta^{1/n}$($\bar{\mathbb Q}$ 上恒等)の像**そのもの**である。$\hat{\mathbb Z}(1)$ は $\Omega$ への**後合成(= 左作用)**で $\mathrm{Fib}_{\vec{01}}$ に作用する — **【v2・R4】この「左」が全編の剰余類規約(§6.3 の $\pi_1/\mathcal H$・$\hat F_2/\tilde H$)と $b=1$ の向きを同時に決めている。**

> **【v2.1・T1 新設】(TB4$^{\rm u}$)(慣性の比較・向き非依存版・便 44 F7.2)** 局所慣性 $I_0=\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))$ の $\pi_1$ への像は $\overline{\langle x\rangle}$ であり、その作用は $\Omega$ への後合成(左作用)である。**ただし選んだ生成元 $\sigma_\zeta$ と $x$ の exact な一致は要求しない。**
>
> **(TB4) $\Longrightarrow$ (TB4$^{\rm u}$)** は明らか。逆は成り立たず、差は**ちょうど 1 つの単位**である: $x$ と $\iota(\sigma_\zeta)$ はどちらも同じ procyclic 群 $\overline{\langle x\rangle}$ の位相的生成元だから、**一意な $\varepsilon\in\hat{\mathbb Z}^\times$** があって
> $$ x=\iota\bigl(\sigma_\zeta^{\,\varepsilon}\bigr),\qquad\text{そして}\qquad b:=\varepsilon^{-1}\bmod M\ \in(\mathbb Z/M)^\times \tag{2.1} $$
> と置ける。**(TB4) $\iff\varepsilon=1\iff b=1$。**
> **★ なぜ分けるか**: (TB1)(TB3) の「慣性生成元」という語が与えるのは**部分群と作用の型**までで、**どの生成元を $x$ と呼ぶか**は与えない。exact $b=1$ は文献関所((TB4))に置き、**それ以前に何が言えるかを §8.1 で明示する**。

> **★ (TB1)–(TB4) の身分**: これは**当工房が §1.1 で置いた規約**((TB2))と、**接基点の理論の標準事実**((TB1)(TB3)(TB4))の混合である。標準事実側が【GAP-TB】(§12.1)。**$A_5$ v4 §3.5 も $K^{(3)}$ §2.1 も、まさにこの 4 つを暗黙に使っていた** — 本稿は使用箇所を明示化しただけで、依存を増やしていない。

> **(TB2) の一意化について**: $(\zeta_n)$ の選択は $\hat{\mathbb Z}^\times$ の自由度をもつが、**同じ $(\zeta_n)$ が $x$ の向き((TB4))と Kummer 指標 $\kappa$ の値の両方を決める**ので、選択は §8 でちょうど相殺する。**これが $b=1$ の正体である。**

---

## 3. 窓前件 (W1)–(W5) — 最小仮定リスト

以下すべて**有限群論の条件**(+ 正典からの読み取り)であり、有限計算で決着する。

| # | 内容 | 型 | 供給元 |
|---|---|---|---|
| **(W1)** | $\bar N\trianglelefteq\hat F_2$ は開・$G_\mathbb Q$-安定(= $N$ は isolated、または少なくとも $\widehat{GT}$-軌道が $\{N\}$)。$P:=\hat F_2/\bar N$、$X:=\pi(x)$、$M:=\mathrm{ord}(X)$ | 正典 | D1 Thm 4.3 等 |
| **(W2)** | $1\to\mathfrak F_0\to\mathrm{GT}(N)\xrightarrow{\tilde\chi}(\mathbb Z/2M)^\times\to1$ 完全、$\tilde\chi\circ\mathrm{Ih}_N=\chi_{2M}$。$K:=\mathbb Q(\zeta_{2M})$ | 正典 | D1 (4.12) 等 |
| **(W3)** | $H\le P$ で **$N_P(H)=H$** | 有限計算 | 窓ごと |
| **(W4)** | **$\langle X\rangle$ が $P/H$ 上推移的**(= $\lambda=0$ 上で全分岐)かつ **$[P:H]=M$** | 有限計算 | 窓ごと |
| **(W5)** | $\Lambda:=\{H\text{ の }P\text{-共役}\}$ が **$\Phi(\mathfrak F_0)$-安定** | 有限計算 | 窓ごと |
| **(W5$^{\mathbb Q}$)** | (任意) $\Lambda$ が **$\Phi(\mathrm{GT}(N))$-安定**($\mathbb Q$-モデルが欲しいとき) | 有限計算 | 窓ごと |

> **v3.1 の (3)(4)(5)(6′) との対応**:
> - v3.1 **(3)**(「$\mathrm{ord}(X)=\lvert\Lambda\rvert=M$ で $\langle X\rangle$ が単純推移」)$\Longleftarrow$ **(W3)+(W4)**(命題 B-2)。**【v2・R1】逆は結合形でのみ成立**: $\langle X\rangle$ が $P/H$ 上推移的なら $\lvert\Lambda\rvert=M\iff\bigl([P:H]=M\ \text{かつ}\ N_P(H)=H\bigr)$、すなわち **(W4) を仮定した上でなら (W3) $\iff\lvert\Lambda\rvert=M$**。**(W3) 単独から $\lvert\Lambda\rvert=M$ は出ない**(命題 B-2 の反例)。
> - v3.1 **(4)**(明示 $\mathbb Q$-モデル・$\mathbb Q$-有理全分岐 cusp・actual marking)【**v2.1・T6 で $K$/$\mathbb Q$ を分離**】:
> $$ \begin{array}{ll} K\text{-モデル}: & \text{(W1)(W2)(W3)(W5)}+\text{(CAL)}\quad(\text{定理 B-4(a)})\\ \mathbb Q\text{-モデル}: & \text{(W1)(W3)(W5}^{\mathbb Q}\text{)}+\text{(CAL)}\quad(\text{定理 B-4(b)})\\ K\text{-有理 cusp}: & \text{B-4(a)}+\text{(W4)}\\ \mathbb Q\text{-有理 cusp}: & \text{B-4(b)}+\text{(W4)} \end{array} $$
> **v2 が書いた「$\mathbb Q$-モデル・$\mathbb Q$-有理 cusp $\Longleftarrow$ (W3)(W4)(W5)」は偽**(便 44 F4)。(W5) から出るのは $K=\mathbb Q(\zeta_{2M})$ 上のモデルであり、(W4) 単独から cusp の $\mathbb Q$-有理性は出ない。**自認。**
> **⇒ 前件から「明示 $\mathbb Q$-モデル」を落としてよい正しい理由**: **橋 B-7 は $G_K$ 上の比較なので $K$-モデルで足り、それは (W1)(W2)(W3)(W5)+(CAL) から出る。追加で (W5$^\mathbb Q$) があれば $\mathbb Q$-モデルまで強化できる。**(「明示」「actual marking」が不要であることは変わらない。)
> - v3.1 **(5)**(FC-2b/FC-3)$=$ **較正 (TB1)–(TB4) + $A_5$ v4 §1.4**。FC-3 は前件ではなく帰結(§6.3)。
> - v3.1 **(6′)** の第 1 節(「$\Lambda$ が $\Phi(\mathfrak F_0)$-安定」)$=$ **(W5)**。**これが橋の前件でもあった**ことが本稿の発見。第 2 節(「$\rho_0$ 忠実」)は $R^{\rm cyc}_{\rm formal}$ 側の前件で、**橋には要らない**。

---

## 4. $B_{\rm FC}$ の分解

$$ \boxed{\ B_{\rm FC}\ =\ \underbrace{B_{\rm FC}\text{-I}}_{\text{型: 平行移動である}}\ +\ \underbrace{B_{\rm FC}\text{-II}}_{\text{同定: その指標が }\kappa_{u^{-1}}} } $$

**【v2・R2/R3/R5】依存欄を修理した。** 「$W_0$ が**与えられた**ときの局所補題」と「窓から $W_0$ を**構成する**主定理」を段で分ける(便 43 F5.2)。

| 段 | 主張 | 依存(**直接**) | 依存(**間接**) | 状態 |
|---|---|---|---|---|
| **I** | $\exists!\,c\in\mathrm{Hom}_{\rm cont}(G_K,\mu_M)$: $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(c(\gamma))\ \forall\gamma\in G_K$ | **(W1)(W2)(W3)(W4)(W5)** ← **R2 で (W3) 追加** | — | **§5・定理 B-3 で証明** |
| **II-a** | 一意な $K$-モデル $W_0\to U_K$ が存在(幾何的連結) | **(W1)(W2)(W3)(W5)** + (CAL) ← **R3 で (W2) 追加** | (TB1)(TB2)(TB3) | **§6・定理 B-4 で証明** |
| **II-a$^\mathbb Q$** | $\mathbb Q$-モデル版 | **(W1)(W3)(W5$^\mathbb Q$)** + (CAL)(**(W2) 不要**) | 同上 | **§6・定理 B-4 で証明** |
| **II-c$_0$**(局所補題・**$W_0$ を与えられたものとする**) | $\lambda^{-1}(0)=\{P_0\}$・$K$-有理・$e=M$、$\mathrm{Fib}$ の Kummer 表示、torsor 類 $=[u^{-1}]$ | **(TB1)(TB2)(TB3)(TB4)** + (W4) ← **R5 で (TB3)(TB4) 追加** | — | **§7・補題 B-5 で証明** |
| **II-c**(窓から) | 上を窓データだけから主張する | II-c$_0$ + **II-a** | (W1)(W2)(W3)(W5)+(CAL) | 同上 |
| **II-b** | $\Lambda\cong\mathrm{Fib}_{\vec{01}}(W_0)$ が $G_K$-集合としても $\mu_M$-torsor としても同型($b=1$) | **(TB1)(TB2)(TB3)(TB4)** + (W3)(W4) + (CAL) | **(W1)(W2)(W5)**(B-4c と B-5 を呼ぶため) | **§8・補題 B-6 で証明** |
| **合成** | $c=\kappa_{u^{-1}}$、すなわち **(5′)** | 上の全部 | — | **§9・定理 B-7** |

> **★ 分解の効き目**: これで「$B_{\rm FC}$ が UNKNOWN」という粗い札が、**「(TB4) の向きが未裏取り」という 1 点**に縮む。委嘱の言う「$B_{\rm FC}$ の第 $k$ 段に絞る」の答えは **$k=$ II-b の (TB4)** である。
> **【v2・S1】ただし射程を限定する**(便 43 F7): 「(TB4) だけが load-bearing」は **exact $b=1$ の向きについて**の話である。(TB1) の圏同値・(TB3) の慣性生成元同定は II-a/II-c$_0$ の土台であり、真に破れれば記法問題では済まない。**単位 $b$ までの twisted 版**((10.1) 形)は (TB4) の向きに依存せず先に定理化できる(便 43 F6.3)。

---

## 5. $B_{\rm FC}$-I の証明 — 型は無料

> **命題 B-1(regular 可換部分群は自己中心化).** $A\le\mathrm{Sym}(\Omega)$ が可換かつ**正則**(単純推移)なら $C_{\mathrm{Sym}(\Omega)}(A)=A$。
> **証明.** $\omega_0\in\Omega$ を固定し $\Omega\xrightarrow{\sim}A$, $a\cdot\omega_0\leftrightarrow a$ と同一視する。$A$ は左移動として作用。$\sigma\in C(A)$、$\sigma(\omega_0)=b\cdot\omega_0$ とすると $\sigma(a\cdot\omega_0)=a\cdot\sigma(\omega_0)=ab\cdot\omega_0$、すなわち $\sigma$ は右移動 $R_b$。$A$ 可換ゆえ $R_b=L_b\in A$。∎

> ### 命題 B-2(指数の整合 — v3.1 (3) の分解)【**v2・R1 で修理**】
> $\langle X\rangle$ が $P/H$ 上推移的で $\mathrm{ord}(X)=M$ とする。このとき
> $$ \boxed{\ \lvert\Lambda\rvert=M\ \iff\ \bigl([P:H]=M\ \textbf{かつ}\ N_P(H)=H\bigr)\ } \tag{B2-corr} $$
> であり、さらに **$M$ と無関係に**
> $$ P/H\longrightarrow\Lambda,\quad gH\mapsto gHg^{-1}\ \text{が全単射}\ \iff\ N_P(H)=H \tag{B2-bij} $$
> が成り立つ。(B2-corr) の下では $P/H\to\Lambda$ は **$\langle X\rangle$-同変な全単射**で、$\tau(\zeta_M)$(共役)は左移動 $L_X$ に対応する。

**証明.** 推移性から $[P:H]\le\lvert\langle X\rangle\rvert=M$。また $\lvert\Lambda\rvert=[P:N_P(H)]\le[P:H]$。よって
$$ \lvert\Lambda\rvert\ \le\ [P:H]\ \le\ M . \tag{B2-chain} $$
$\lvert\Lambda\rvert=M$ なら (B2-chain) は全部等号で、$[P:H]=M$ かつ $[P:N_P(H)]=[P:H]$ すなわち $N_P(H)=H$。逆に $[P:H]=M$ かつ $N_P(H)=H$ なら $\lvert\Lambda\rvert=[P:N_P(H)]=[P:H]=M$。(B2-bij): 写像は well-defined・$P$-同変・全射で、$gHg^{-1}=g'Hg'^{-1}\iff g^{-1}g'\in N_P(H)$ だから単射性は $N_P(H)=H$ と同値。同変性から $\tau(\zeta_M)\leftrightarrow L_X$。∎

> **⚠【v2・R1】v1 の「$\lvert\Lambda\rvert=M\iff[P:H]=M\iff N_P(H)=H$」という三者 pairwise 同値は偽である**(便 43 F2.1)。**Sol の反例**:
> $$ P=S_3\times C_2,\qquad H=\langle(1\,2)\rangle\times C_2,\qquad X=\bigl((1\,2\,3),\,c\bigr) $$
> ($c$ は $C_2$ の生成元)。$\mathrm{ord}(X)=6=M$、$[P:H]=3$、$X$ は $P/H$(3 点)上推移的($X^3=(e,c)\in H$ は自明に作用し $X$ は 3-サイクル)、$N_{S_3}(\langle(1\,2)\rangle)=\langle(1\,2)\rangle$ より $N_P(H)=H$。しかし
> $$ \lvert\Lambda\rvert=[P:H]=3\ \ne\ 6=M. $$
> **すなわち $N_P(H)=H$ だけでは $\lvert\Lambda\rvert=M$ は出ない。** 私は (B2-chain) の「全部等号」を、両端を止めずに各段で読んでいた。**自認**。
>
> **⇒ 正しい副産物の言明**: **(W4)(= $\langle X\rangle$ 推移的 **かつ** $[P:H]=M$)を仮定した上でなら**
> $$ \boxed{\ (W3)\ \iff\ \lvert\Lambda\rvert=M\ } $$
> である。**検算 V3 は初めからこの結合形**(「$\langle X\rangle$ 推移的 **かつ** $\lvert\Lambda\rvert=6$」⇒ $N_P(H)=H$)**を検査しており、誤った pairwise 同値を検査してはいない**(便 43 F2.1 が確認)。検算 **V3**($K^{(3)}$ で該当 $H$ が 12 個・反例 0)・**V4**(同変全単射)。

> ### 定理 B-3($B_{\rm FC}$-I)【**v2・R2 で (W3) を追加**】
> **(W1)(W2)(W3)(W4)(W5)** の下で、$\rho_\Lambda\circ\mathrm{Ih}_N|_{G_K}$ の像は $\tau(\mu_M)$ に含まれる。すなわち**一意な連続準同型**
> $$ \boxed{\ c\ :=\ \tau^{-1}\circ\rho_\Lambda\circ\mathrm{Ih}_N|_{G_K}\ :\ G_K\longrightarrow\mu_M\ } \tag{5.1} $$
> が定まり、$\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(c(\gamma))\ (\forall\gamma\in G_K)$。

**証明.**
1. (W5) より $\Phi(\mathfrak F_0)$ は $\Lambda$ を保ち、(W2) より $\gamma\in G_K\Rightarrow\tilde\chi(\mathrm{Ih}_N(\gamma))=\chi_{2M}(\gamma)=1\Rightarrow\mathrm{Ih}_N(\gamma)\in\mathfrak F_0$。ゆえに $\rho_\Lambda(\mathrm{Ih}_N(\gamma))\in\mathrm{Sym}(\Lambda)$ が定義される。
2. shadow の定義 $\Phi_{(m,f)}(X)=X^{2m+1}$ と $\tilde\chi(m,f)=2m+1$ より、$\varphi\in\mathfrak F_0$ なら $2m+1\equiv1\ (2M)$、とくに $\bmod\ M$ でも $1$ だから $\Phi_\varphi(X)=X$。
3. ゆえに $H'\in\Lambda$ に対し $\Phi_\varphi(XH'X^{-1})=\Phi_\varphi(X)\Phi_\varphi(H')\Phi_\varphi(X)^{-1}=X\Phi_\varphi(H')X^{-1}$、すなわち $\rho_\Lambda(\varphi)$ は $\tau(\zeta_M)$ と**可換**。
4. **(W3)+(W4)**+命題 B-2 より $\lvert\Lambda\rvert=M$ で $\tau(\mu_M)$ は $\Lambda$ 上の **regular 可換**部分群。命題 B-1 より $C_{\mathrm{Sym}(\Lambda)}(\tau(\mu_M))=\tau(\mu_M)$。ゆえに $\rho_\Lambda(\mathfrak F_0)\subseteq\tau(\mu_M)$、とくに $\rho_\Lambda(\mathrm{Ih}_N(G_K))\subseteq\tau(\mu_M)$。
5. $\tau$ は単射(命題 B-2)だから $c$ は well-defined。$\rho_\Lambda\circ\mathrm{Ih}_N$ が連続準同型ゆえ $c$ も。∎

> **⚠【v2・R2】(W3) は落とせない**(便 43 F2.2)。**Sol の反例**: $P=C_M\times C_2$、$H=C_2$、$X=(\text{$C_M$ の生成元},1)$。$[P:H]=M$ で $\langle X\rangle$ は $P/H$ 上推移的だから **(W4) は成立する**が、$H\trianglelefteq P$ ゆえ $\Lambda$ は 1 点、$\tau$ は忠実でも regular でもなく、第 4 段が崩れる。**v1 は前件欄で (W3) を落としていた**(主定理 B-7 の前件には入っていたので結論は無事)。**自認**。

> **★ これは補題 $R'$(v3.1 §5.2.3)の $G_K$ 版であり、証明は逐語同じである。** v3.1 は補題 $R'$ を **(6′) の縮約**にしか使っていなかったが、**同じ補題が (5′) の「型」を無料で供給する**ことに気づいていなかった。これが本稿最大の構造的発見である。
>
> **★ 帰結(用語)**: $\mu_M\subset K$ ゆえ $\mathrm{Hom}_{\rm cont}(G_K,\mu_M)=H^1(G_K,\mu_M)\cong K^\times/K^{\times M}$(Kummer 理論)。よって (5.1) は窓 $(N,H)$ に**正準な類**
> $$ \boxed{\ \mathfrak s(N,H)\ :=\ [c]\ \in\ K^\times/K^{\times M}\quad(\textbf{shadow 類})\ } \tag{5.2} $$
> を与える。**$B_{\rm FC}$ とは「shadow 類 $=$ Belyi 類 $[u^{-1}]$」という主張に他ならない。**
>
> **注(較正はここでは要らない)【v2 で文言精密化】**: 定理 B-3 は $\mathrm{Ih}_N$ の**存在**と**有限群論的前件 (W1)–(W5)** しか使わない — $\alpha^{\rm Ih}=\alpha^{\rm std}$ も $\mathbb Q$-モデルも cusp も使わない。較正が要るのは **§6(descent の $\Lambda$-安定性)と §8(幾何側との同定)**である。
> **⇒「型は無料」の正確な意味**(便 43 F2.2 の言い換えを採用): **regular detector (W3)(W4) を既に払った後は、$B_{\rm FC}$-I に追加の幾何入力が要らない。** 「前件ゼロで出る」という意味ではない。

---

## 6. $B_{\rm FC}$-II-a — 剛性 descent(**$K$-モデルは (W1)(W2)(W3)(W5) の帰結・$\mathbb Q$-モデルは (W5$^\mathbb Q$) の帰結**)

> **【v2.1・T6】見出しを訂正した。** v2 は「$\mathbb Q$-モデルの存在は前件でなく帰結」と書いたが、**(W5)(= $\Phi(\mathfrak F_0)$-安定)から出るのは $K$-モデルまで**である。$\mathbb Q$-モデルには **(W5$^\mathbb Q$)**($\Phi(\mathrm{GT}(N))$-安定)が要る(便 44 F4)。**橋 B-7 に必要なのは $K$-モデルだけ。**

$\tilde H:=\pi^{-1}(H)\le\hat F_2$(開)、$\tilde\Lambda:=\{\tilde H\text{ の }\hat F_2\text{-共役}\}$ と置く。$\bar N\subseteq\tilde H$ ゆえ $\tilde\Lambda\xrightarrow{\sim}\Lambda$(自然な全単射)。

### 6.1 準備

> **補題 B-4a.** (W3) $N_P(H)=H$ $\Longrightarrow$ $N_{\hat F_2}(\tilde H)=\tilde H$。
> **証明.** $\bar N\trianglelefteq\hat F_2$ かつ $\bar N\subseteq\tilde H$ より、$n\in\bar N$, $h\in\tilde H$ に対し $nhn^{-1}=h\cdot(h^{-1}nhn^{-1})\in\tilde H\bar N=\tilde H$。ゆえに $\bar N\subseteq N_{\hat F_2}(\tilde H)$。$N_{\hat F_2}(\tilde H)/\bar N=N_P(H)=H$ だから $N_{\hat F_2}(\tilde H)=\tilde H$。∎

> **補題 B-4b【v2・R3 で (W2) を追加】.**
> **(a)($K$-版)** **(W1)(W2)(W5)** + 較正($\alpha^{\rm Ih}=\alpha^{\rm std}$)$\Longrightarrow$ $\tilde\Lambda$ は $\alpha^{\rm std}(G_K)$-安定。
> **(b)($\mathbb Q$-版)** **(W1)(W5$^\mathbb Q$)** + 較正 $\Longrightarrow$ $\tilde\Lambda$ は $\alpha^{\rm std}(G_\mathbb Q)$-安定。**(W2) は不要。**
> **証明.** (W1) より $\alpha^{\rm std}_\gamma(\bar N)=\bar N$ で、誘導自己同型 $\beta_\gamma\in\mathrm{Aut}(P)$ が定まる。較正より $\alpha^{\rm std}=\alpha^{\rm Ih}$ だから $\beta_\gamma=\Phi(\mathrm{Ih}_N(\gamma))$($\Phi$ の定義式と (1.1) が逐語同一)。
> (a): $\gamma\in G_K$ なら **(W2)** より $\tilde\chi(\mathrm{Ih}_N(\gamma))=\chi_{2M}(\gamma)=1$、すなわち $\mathrm{Ih}_N(\gamma)\in\mathfrak F_0$。(W5) より $\beta_\gamma(\Lambda)=\Lambda$。
> (b): $\beta_\gamma\in\Phi(\mathrm{GT}(N))$ は無条件だから (W5$^\mathbb Q$) が直接効く。**$\mathfrak F_0$ への所属を経由しないので (W2) を要さない**(便 43 F3.2)。
> いずれも $\alpha^{\rm std}_\gamma(\tilde H)$ は $\beta_\gamma(H)\in\Lambda$ の引き戻しゆえ $\tilde\Lambda$ に入る。∎

### 6.2 定理

> ### 定理 B-4(剛性 descent)【**v2・R3 で $K$-版と $\mathbb Q$-版を分離**】
> **(a)($K$-版)** (TB1)–(TB3)・**(W1)(W2)(W3)(W5)** と較正 (CAL) の下で、$\tilde H$ に対応する $\bar{\mathbb Q}$-被覆 $W\to U_{\bar{\mathbb Q}}$ は **$K$ 上の幾何的連結モデル $W_0\to U_K$ をもち、それは一意な同型を除いて一意**である。
> **(b)($\mathbb Q$-版)** (TB1)–(TB3)・**(W1)(W3)(W5$^\mathbb Q$)** と (CAL) の下で、$\mathbb Q$-モデルが同様に取れる。**(W2) は要らない。**

**証明.** (TB2) の分裂により $\pi_1(U_K,\vec{01})=\hat F_2\rtimes_{\alpha}G_K$($\alpha:=\alpha^{\rm std}$)と書ける。(TB1) より、求める $K$-モデルは
$$ \mathcal H\le\hat F_2\rtimes G_K\ \text{開},\quad \mathcal H\cap\hat F_2=\tilde H,\quad \mathcal H\cdot\hat F_2=\pi_1(U_K,\vec{01}) $$
なる部分群と 1:1 に対応する(第 3 条件が幾何的連結性)。

**構成.** 補題 B-4b より各 $\gamma\in G_K$ について $\alpha_\gamma(\tilde H)\in\tilde\Lambda$。そこで
$$ C_\gamma:=\{c\in\hat F_2:\ c^{-1}\tilde Hc=\alpha_\gamma(\tilde H)\}\ \ne\ \emptyset . $$
$c,c'\in C_\gamma$ なら $d:=c'c^{-1}$ が $d^{-1}\tilde Hd=\tilde H$ を満たす(直接計算)ので補題 B-4a より $d\in\tilde H$。ゆえに
$$ C_\gamma=\tilde H\,c_\gamma\quad(\text{1 つの }c_\gamma\text{ による}\ \textbf{右剰余類}) \tag{6.1} $$
【**v2.1・T4**】v2 はここを「左剰余類」と書いていた(便 44 F2.4)。$\tilde Hc_\gamma$ は**右**剰余類($\tilde H\backslash\hat F_2$ の元)である。§6.2 後段の閉性の議論と §6.3 の**左**剰余類 $\hat F_2/\tilde H$(そちらは $\pi_1$ が作用する側)を混同しないこと。**式と cocycle 計算は v2 のまま正しい。**
は**一意に定まる**。写像 $\gamma\mapsto\tilde Hc_\gamma$ は、連続写像 $\gamma\mapsto\alpha_\gamma(\tilde H)\in\tilde\Lambda$(有限集合)を経由するので**連続**。

**cocycle 条件(ここで (W3) が効く).** $\gamma,\delta\in G_K$ に対し
$$ \alpha_{\gamma\delta}(\tilde H)=\alpha_\gamma\bigl(c_\delta^{-1}\tilde Hc_\delta\bigr)=\alpha_\gamma(c_\delta)^{-1}\,\alpha_\gamma(\tilde H)\,\alpha_\gamma(c_\delta) =\bigl(c_\gamma\alpha_\gamma(c_\delta)\bigr)^{-1}\tilde H\bigl(c_\gamma\alpha_\gamma(c_\delta)\bigr), $$
すなわち $c_\gamma\alpha_\gamma(c_\delta)\in C_{\gamma\delta}=\tilde Hc_{\gamma\delta}$。**(6.1) の一意性から cocycle 条件は自動で成立する。**

**部分群であること.** $\mathcal H:=\{(hc_\gamma,\gamma):h\in\tilde H,\ \gamma\in G_K\}$ と置く。
$$ (hc_\gamma,\gamma)(h'c_\delta,\delta)=\bigl(h\,c_\gamma\alpha_\gamma(h')\alpha_\gamma(c_\delta),\ \gamma\delta\bigr), $$
$c_\gamma\alpha_\gamma(\tilde H)c_\gamma^{-1}=\tilde H$ より $c_\gamma\alpha_\gamma(h')=h''c_\gamma$($h''\in\tilde H$)、そして $c_\gamma\alpha_\gamma(c_\delta)\in\tilde Hc_{\gamma\delta}$。ゆえに積は $\mathcal H$ に入る。
**閉性と開性**: $\mathcal H=\{(g,\gamma):\tilde Hg=\tilde Hc_\gamma\}$ は、連続写像 $(g,\gamma)\mapsto(\tilde Hg,\ \tilde Hc_\gamma)\in(\tilde H\backslash\hat F_2)^2$(**右辺は有限集合**)による対角線の逆像なので**閉**。
【**v2・R4 の注意**】ここで現れる $\tilde H\backslash\hat F_2$ は **$C_\gamma=\tilde Hc_\gamma$ が右剰余類だから**であって、§6.3 で $\pi_1$ が作用する**左**剰余類空間 $\pi_1/\mathcal H$ とは別物である。**両者を混ぜない**(R4 の修理はこの区別を明示化したもので、本段は修理前から正しい)。$C_1=N_{\hat F_2}(\tilde H)=\tilde H$ より $c_1=1$ と取れて $\mathcal H\cap\hat F_2=\tilde H$、$\mathcal H\to G_K$ は全射ゆえ $\mathcal H\hat F_2=\pi_1$、したがって $[\pi_1:\mathcal H]=[\hat F_2:\tilde H]<\infty$。副有限群の有限指数閉部分群は**開**。
**逆元(補題を一行明記・便 43 F3.1 の助言)**: *コンパクト位相群の空でない閉部分半群は部分群である*($a\in\mathcal H$ に対し $\overline{\{a^n:n\ge1\}}$ はコンパクト可換半群ゆえ群を含み、$a^{-1}$ を含む)。$\mathcal H$ は閉・非空・積で閉じているので部分群。∎(存在)

**一意性.** $\mathcal H'$ を別の解とすると、$\gamma$ ごとに $(c'_\gamma,\gamma)\in\mathcal H'$ が取れ、$\mathcal H'\cap\hat F_2=\tilde H$ の正規性から $c'_\gamma\in C_\gamma=\tilde Hc_\gamma$。ゆえに $\mathcal H'=\mathcal H$。∎(一意性)

**(b)($\mathbb Q$-版)**: 上の議論の $G_K$ を $G_\mathbb Q$、補題 B-4b(a) を (b) に置換すればよい。∎

> **【v2・R3 / 便 43 F3.3】一意性の射程 — 「部分群の一意性」から「被覆の一意性」へ**: 上の一意性は、**幾何 stabilizer を文字どおり $\tilde H$ に固定した pointed 記述**での部分群の一意性である。非標識被覆へ戻すと別の幾何同定は $\hat F_2$-共役を生むが、
> $$ \mathrm{Aut}_U(W)\ \cong\ N_{\hat F_2}(\tilde H)/\tilde H\ \overset{\text{補題 B-4a}}{=}\ 1 $$
> なので、**$K$-モデルは一意な同型を除いて一意**になる。この一段を明示しないと、定理文の「一意な同型を除いて一意」が pointed 版の主張と混ざる。

> **★ 何が起きたか**: これは Weil descent の**剛性版**($\mathrm{Aut}_U(W)=N_P(H)/H=1$ ゆえ descent データが一意 ⇒ cocycle 条件が自動)を、$\pi_1$ の言葉で直接書いたものである。**外部文献を引かずに閉じた。**
>
> **★ $A_5$/$K^{(3)}$ が払っていた代金との比較**: $A_5$ は「$H^1(G_\mathbb Q,\mathrm{Aut})=H^1(G_\mathbb Q,1)=1$」(FC-4(c))という**同じ論法**を使っていたが、「dessin の同型類が一意」(FC-4(b))という悉皆計算と抱き合わせだった。$K^{(3)}$ は明示モデルを外から持ってきた。**どちらも不要**だったことになる。
>
> **⚠ 注意(W5 の非自明性)【v2・S2 で射程限定】**: $K^{(3)}$ では $\lvert\mathrm{Aut}(G_3)\rvert=1296$ のうち $\Lambda$ を **setwise に**保つのは **432 個**(検算 **V7**)。$\Phi(\mathfrak F_0)$ の 3 元も $\Phi(\mathrm{GT}(K^{(3)}))$ の 12 元もすべてその中(検算 **V6**)。**つまり (W5)/(W5$^{\mathbb Q}$) は「自明に成り立つ条件」ではない** — v3.1 §2.2 が記録した「$\mathrm{Aut}(G_3)$ が二つの $G_3$-類を融合する」現象は、まさにこの条件が破れうることの実例である。
> **ただし (W5) は「432/1296」という比ではない**(便 43 F8.1): **(W5) は「指定された 3 元(または 12 元)の像が、その 432 元の setwise stabilizer に含まれる」という包含条件**である。432/1296 は条件の非自明性を示す**周囲の有限群データ**であって、条件そのものではない。数値の状態札は **`source-audited candidate`**(GAP 第二系統は 17/17 で走ったが §15.7 の fidelity gate が未閉鎖)。

### 6.3 FC-3 は帰結である

> ### 系 B-4c(= FC-3)【**v2・R4 で左作用・左剰余類へ統一**】
> 定理 B-4 の $W_0$ について、$p\mapsto\mathrm{Stab}_{\hat F_2}(p)$ は $G_K$-同型
> $$ c_\Lambda:\ \mathrm{Fib}_{\vec{01}}(W_0)\ \xrightarrow{\ \sim\ }\ \tilde\Lambda\ \xrightarrow{\ \sim\ }\ \Lambda $$
> を与える。$\hat F_2$-同変でもあり、$x$ の作用が $\tau(\zeta_M)$ に対応する。

**証明.** **(TB4) が採る「$\Omega$ への後合成」は左作用**なので、stabilizer $\mathcal H$ をもつ推移的 $\pi_1$-集合は**左剰余類空間**
$$ \mathrm{Fib}_{\vec{01}}(W_0)\ \cong\ \pi_1(U_K,\vec{01})/\mathcal H,\qquad g\cdot(f\mathcal H)=gf\mathcal H $$
である((TB1))。$\hat F_2$-集合としての制限は、$\mathcal H\cap\hat F_2=\tilde H$ と $\mathcal H\hat F_2=\pi_1$(幾何的連結性 = $\hat F_2$ の推移性)から
$$ \mathrm{Fib}_{\vec{01}}(W_0)\big|_{\hat F_2}\ \cong\ \hat F_2/\tilde H . $$
左剰余類の stabilizer は $\mathrm{Stab}(g\tilde H)=g\tilde Hg^{-1}$ で、これが $\tilde\Lambda$ への全単射になるのは補題 B-4a($N_{\hat F_2}(\tilde H)=\tilde H$)による。$G_K$-同変性は
$$ \mathrm{Stab}\bigl(s_v(\gamma)\cdot p\bigr)=s_v(\gamma)\,\mathrm{Stab}(p)\,s_v(\gamma)^{-1}=\alpha^{\rm std}_\gamma\bigl(\mathrm{Stab}(p)\bigr) $$
(接基点の定義そのもの)。最後に命題 B-2 (B2-bij) で $\tilde\Lambda\cong\Lambda$、左移動 $L_X\leftrightarrow\tau(\zeta_M)$。∎

> **⚠【v2・R4】v1 は $\mathcal H\backslash\pi_1$・$\tilde H\backslash\hat F_2\cong\hat F_2/\tilde H$ と書いていた**(便 43 F4)。$\tilde H$ は非正規なので**左右剰余類を無根拠に同一視していた**。直後に使う $\mathrm{Stab}(g\tilde H)=g\tilde Hg^{-1}$ は**左**剰余類の公式であり、記法と整合していなかった。**組版の問題ではなく §8 の $b=1$ の向きを支える箇所**なので必須修理として直した。**自認。**
>
> **⇒ v3.1 の前件 (5) のうち FC-3 部分(と便 27 F5 が要求した (FC3-i)(FC3-ii)(FC3-iii))は、すべて (W1)(W2)(W3)(W5)+(CAL) からの帰結になった。** 前件に残る幾何入力は **FC-2b(較正)だけ**である。

---

## 7. $B_{\rm FC}$-II-c — cusp の局所理論と Kummer torsor

$W_0^c$ を $W_0$ の滑らかな射影モデル($\mathbf P^1_K$ の $K(W_0)$ における正規化)、$\lambda:W_0^c\to\mathbf P^1_K$ を延長した Belyi 写像とする。

> **補題 B-5a(繊維の分解).** $R:=\mathcal O_{\mathbf P^1_K,0}$(DVR・uniformizer $\beta$)、$B:=$ $K(W_0)$ における $R$ の整閉包(半局所 Dedekind)とすると
> $$ \mathcal O\bigl(W_0\times_U\mathrm{Spec}\,K((\beta))\bigr)\ \cong\ B\otimes_R K((\beta))\ \cong\ \prod_{P\mid 0}\ \kappa(P)((s_P)) $$
> ($P$ は $\lambda^{-1}(0)$ の閉点、$s_P$ は $P$ での uniformizer)。
> **証明.** $\mathrm{Spec}\,K((\beta))\to\mathbf P^1_K$ は $\beta,\beta-1$ が単元ゆえ $U$ を経由し、$W_0\times_U\mathrm{Spec}\,K((\beta))=W_0^c\times_{\mathbf P^1}\mathrm{Spec}\,K((\beta))$。$B$ は有限 $R$-加群だから $B\otimes_RR^\wedge=B^\wedge$(($\beta$)-進完備化)、半局所 Dedekind の完備化は CRT で $\prod_P B_P^\wedge$ に分解。$\beta$ を可逆にして $\prod_P\mathrm{Frac}(B_P^\wedge)=\prod_P\kappa(P)((s_P))$。∎

> **補題 B-5b(幾何点 $\leftrightarrow$ 慣性軌道).** $\lambda^{-1}(0)$ の**幾何**点は $\mathrm{Fib}_{\vec{01}}(W_0)$ 上の $\langle x\rangle$-軌道と 1:1 に対応し、軌道の長さが分岐指数である。
> **証明.** 補題 B-5a を $\bar{\mathbb Q}$ 上で読むと $\prod$ の各因子は $\bar{\mathbb Q}((s_P))/\bar{\mathbb Q}((\beta))$ で全分岐次数 $e_P$、その $\Omega$ への埋め込みは $e_P$ 個で $\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))=\hat{\mathbb Z}(1)$ が推移的に置換する((TB4))。∎

> ### 補題 B-5(局所 Kummer)【**v2・R5 で依存欄を明記**】
> **これは「$W_0$ が与えられたときの局所補題」である**(窓から $W_0$ を構成する部分は定理 B-4 が担う — 便 43 F5.2 の分離要求)。前件は **(TB1)(TB2)(TB3)(TB4) + (W4)**: B-5b が「$x$ が $0$-慣性で、局所 Galois 群が**後合成(左作用)**で $\mathrm{Fib}$ に作用する」を使うので、**v1 の (TB1)(TB2) だけでは足りない**。**自認。**
> (W4) を仮定する。すると
> **(i)** $\lambda^{-1}(0)$ はただ 1 点 $P_0$ からなり、$P_0$ は **$K$-有理**で分岐指数 $M$。
> **(ii)【v2.1・T5 で 2 つに分離】** $P_0$ での任意の $K$-有理 uniformizer $s$ について $\lambda=u\,s^M(1+O(s))$、$u\in K^\times$。さらに
> - **(ii-loc)(B-5$_{\rm loc}$・所与の $W_0$ に対する主張)** $[u]_M\in K^\times/K^{\times M}$ は **$s$ の選び方に依らない**。前件は **(TB1)–(TB4)+(W4)** のみ。
> - **(ii-win)(B-5$_{\rm win}$・窓の主張)** $[u]_M$ は **$K$-モデルの取り方にも依らない**。**この一節だけは定理 B-4 の一意性を使う**ので、前件に **(W1)(W2)(W3)(W5)+(CAL)** が加わる。
> **(iii)** $K((\beta))$-代数として
> $$ \mathcal O\bigl(W_0\times_U\mathrm{Spec}\,K((\beta))\bigr)\ \cong\ K((\beta))[T]/(T^M-u^{-1}\beta), $$
> したがって
> $$ \mathrm{Fib}_{\vec{01}}(W_0)=\bigl\{\,\xi\,(u^{-1})^{1/M}\beta^{1/M}\ :\ \xi\in\mu_M\,\bigr\}\subset\Omega \tag{7.1} $$
> は $\mu_M$-torsor($\mu_M$ は乗法で作用・$m(\xi)$ と書く)であり、
> $$ \boxed{\ \gamma\cdot p\ =\ m\bigl(\kappa_{u^{-1}}(\gamma)\bigr)\,p\qquad(\forall\gamma\in G_K,\ p\in\mathrm{Fib}) \ } \tag{7.2} $$
> すなわち **torsor 類は $[u^{-1}]\in K^\times/K^{\times M}=H^1(G_K,\mu_M)$**。

**証明.**
**(i)** (W4) と補題 B-5b: $\langle X\rangle=\langle x\rangle$ の像は $\mathrm{Fib}\cong P/H$ 上推移的だから幾何点は 1 個、分岐指数 $=[P:H]=M$。$G_K$ はこの唯一の幾何点を保つので、対応する閉点 $P_0$ の剰余体は $\kappa(P_0)=K$($\lvert\{\text{幾何点}\}\rvert=[\kappa(P_0):K]=1$)。
**(ii)** $P_0$ は滑らかな $K$-有理点なので $\mathfrak m_{P_0}/\mathfrak m^2\cong K$、$K$-有理 uniformizer $s$ が取れる。$v_{P_0}(\lambda)=e_{P_0}=M$ より $\lambda=us^M+\cdots$、$u\in K^\times$。
**(ii-loc)**: $s'=as(1+O(s))$($a\in K^\times$)に取り替えると $u\mapsto ua^{-M}$ なので $[u]_M$ は不変。**ここまでは $W_0$ を所与とした局所計算だけ。**
**(ii-win)**: $K$-モデルは**定理 B-4 で一意**なので $[u]_M$ は窓のデータだけで決まる。**この一行が B-4 の全仮定に依存する**(便 44 F2.5)。**v2 は (ii) を 1 文にまとめ、前件を (TB1)–(TB4)+(W4) と書いていた — その一節については強すぎた。自認。**(主定理 B-7 は B-4 の仮定を既に持つので結論に影響なし。)
**(iii)** $h:=u^{-1}\lambda s^{-M}\in K[[s]]$ は $h(0)=1$、$M\in K^\times$ だから $h^{1/M}\in K[[s]]$(定数項 1)が**一意に**存在する。$\tilde s:=s\,h^{1/M}$ は uniformizer で $\tilde s^M=u^{-1}\lambda=u^{-1}\beta$。補題 B-5a と (i) より $\mathcal O(\cdots)=K((s))=K((\tilde s))$、次数は $M$、$T^M-u^{-1}\beta$ は $K((\beta))$ 上 Eisenstein ゆえ既約。よって同型。
(7.1) は $T^M-u^{-1}\beta$ の $\Omega$ における根の集合。$\gamma\in G_K$ は (TB2) より $\beta^{1/M}$ を固定し係数に作用するので $\gamma\bigl(\xi(u^{-1})^{1/M}\beta^{1/M}\bigr)=\xi\,\kappa_{u^{-1}}(\gamma)\,(u^{-1})^{1/M}\beta^{1/M}$。$\mu_M\subset K$ ゆえ $\kappa_{u^{-1}}:G_K\to\mu_M$ は準同型で $M$ 乗根の選び方に依らない。∎

> **★ $A_5$ v4 §3.5 との照合**: そこでは $\xi^5=-2\beta$、すなわち $u^{-1}=-2$、$u=-1/2$。(7.1) は $\{\zeta_5^j(-2)^{1/5}\beta^{1/5}\}$ で**逐語一致**。$K^{(3)}$ §2.1 の「$\lambda=us^M(1+O(s))$ ⇒ $[u^{-1}]$」も (ii)(iii) の特殊化。

---

## 8. $B_{\rm FC}$-II-b — torsor 比較と $b=1$

> ### 補題 B-6(torsor 比較)【**v2・R4/R5 で依存欄を修理**】
> (TB1)–(TB4)・**(W1)(W2)(W3)(W4)(W5)** と較正 (CAL) の下で(系 B-4c と補題 B-5 を呼ぶので (W2)(W5) も間接依存に入る)、系 B-4c の**左作用に統一した**同型 $c_\Lambda:\mathrm{Fib}_{\vec{01}}(W_0)\xrightarrow{\sim}\Lambda$ は
> $$ \boxed{\ c_\Lambda\circ m(\xi)\circ c_\Lambda^{-1}\ =\ \tau(\xi)\qquad(\forall\xi\in\mu_M)\ } \tag{8.1} $$
> を満たす。すなわち **$b=1$**。

**証明.**
1. (TB4) より $x$ は $\mathrm{Fib}$ に $\sigma_\zeta$ の後合成で作用する。(7.1) の点 $p=\xi'(u^{-1})^{1/M}\beta^{1/M}$ に対し、$\sigma_\zeta$ は $\bar{\mathbb Q}$(ゆえに $(u^{-1})^{1/M}$ と $\xi'$)を固定し $\beta^{1/M}\mapsto\zeta_M\beta^{1/M}$ を与えるから
$$ x\cdot p=\zeta_M\,p=m(\zeta_M)\,p . $$
2. 系 B-4c より $c_\Lambda$ は $\hat F_2$-同変で、$x$ の $\Lambda$ 上の作用は $\tau(\zeta_M)$(命題 B-2)。ゆえに $c_\Lambda\circ m(\zeta_M)\circ c_\Lambda^{-1}=\tau(\zeta_M)$。
3. $m,\tau$ はともに準同型 $\mu_M\to\mathrm{Sym}(\Lambda)$ で、$c_\Lambda$ による共役も準同型。生成元 $\zeta_M$ で一致するから全体で一致。∎

> **★ $b=1$ の正体**: (TB2) の $(\zeta_n)$ が **$x$ の向き**((TB4))と **$\kappa$ の値**((7.2))の**両方**を決めているので、$(\zeta_n)\mapsto(\zeta_n^t)$($t\in\hat{\mathbb Z}^\times$)に取り替えると $\tau$ の生成元と $\kappa$ の値が**同時に**ひねられて相殺する。**$b$ は「二つの独立な規約のずれ」ではなく、「一つの規約を二度使う」ことで消える。**
>
> **⚠【v2・R6/S1】$b=1$ の状態札を正確に**(便 43 F6.2): $b=1$ は「規約から独立な裸の定理」**ではない**。
> $$ \boxed{\ b=1\ \text{は}\ \textbf{(TB2) の根系・係数分裂と (TB4) の }x=\sigma_\zeta\textbf{・後合成規約を同時に固定した枠組みに相対的な定理}\ } $$
> である。**(TB4) はまさに結論の向きを含んでいる** — 原典照合で $x^{-1}$・前合成・右作用が採られていれば、単位 $b$ が出る。したがって **v1 の「$b_i\ne1$ は必ず (TB2) 違反」という診断は狭すぎた**。正しい診断先は
> $$ \texttt{TB2 / TB4 / 左右作用 / 共役 transport 規約の不一致} $$
> **全体の検出器**である。**自認。**
> **⇒ $b_i$ 欄の厳格運用(Rule 1 (7.1)・受理条件 (7.3))は本稿によっても撤回されない**(§10)。実装が (a) GAP の右共役規約、(b) 埋め込み (1.6) と別の原始根、(c) 惰性生成元の反転を踏めば $b\ne1$ が出るが、それは**規約 transport の記録事項**であって数学的発見ではない。
>
> **★ 便 43 F6.1 の判定**: 左作用へ統一した後の上の計算は **PASS**。「半直積の向きによる追加の逆数は現れない」。自己申告 A-2 は **(TB4) をこの向きで採用する限り閉じた**。

### 8.1 【v2.1・T1 新設】orientation-free 版 — 補題 B-6$^{\rm tw}$ と定理 B-7$^{\rm tw}$

> **⚠ 先に v2 の誤りを撤回する**(便 44 F7.1)。v2 は「単位 $b$ を伴う twisted bridge は**無条件**に定理化できる」と書いた。**これは循環である。** 系 B-8 は
> $$ \rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau\bigl(\kappa_{u^{-1}}(\gamma)^b\bigr) \tag{10.1} $$
> を**仮定したとき**に位数・核・固定体が $b$ に依らないことを示す補題であって、**$\exists b\in(\mathbb Z/M)^\times$ で (10.1) が成り立つ、という存在命題を与えない**。**自認。** 正しくは、(TB4) を (TB4$^{\rm u}$) へ弱めた上で存在を**証明する**。

> ### 補題 B-6$^{\rm tw}$(orientation-free torsor comparison).
> **(TB1)(TB2)(TB3)(TB4$^{\rm u}$)**・(W1)–(W5)・(CAL) の下で、(2.1) の $b=\varepsilon^{-1}\bmod M$ について
> $$ \boxed{\ c_\Lambda\circ m(\xi)\circ c_\Lambda^{-1}\ =\ \tau\bigl(\xi^{\,b}\bigr)\qquad(\forall\xi\in\mu_M)\ } \tag{8.2} $$

**証明.** (TB4$^{\rm u}$) より $x$ の $\mathrm{Fib}$ 上の作用は $I_0$ の像に属し、$\sigma_\zeta$ は $m(\zeta_M)$ として作用する(補題 B-6 の 1 と同じ計算)。(2.1) より
$$ x\ \text{の作用}\ =\ m(\zeta_M)^{\varepsilon}\ =\ m(\zeta_M^{\,\varepsilon}) $$
($\mu_M$ 上では $\varepsilon$ は $\bmod\,M$ でしか効かない)。他方 $\tau$ の**定義**により $c_\Lambda\circ(x\text{ の作用})\circ c_\Lambda^{-1}=\tau(\zeta_M)$(系 B-4c)。ゆえに
$$ c_\Lambda\, m(\zeta_M^{\,\varepsilon})\, c_\Lambda^{-1}=\tau(\zeta_M). $$
$\xi=\zeta_M^{\,k}$ と書き $k=\varepsilon j$ すなわち $j=bk$ と置き換えると $c_\Lambda m(\zeta_M^{\,k})c_\Lambda^{-1}=\tau(\zeta_M^{\,bk})=\tau\bigl((\zeta_M^{\,k})^b\bigr)$。∎

> ### 定理 B-7$^{\rm tw}$(twisted comparison bridge).
> **(TB1)(TB2)(TB3)(TB4$^{\rm u}$)**・(CAL)・(W1)–(W5) の下で、**一意な $b\in(\mathbb Z/M)^\times$**(= (2.1) の $\varepsilon^{-1}$、**窓に依らず枠組みだけで決まる**)が存在して
> $$ \boxed{\ \rho_\Lambda\bigl(\mathrm{Ih}_N(\gamma)\bigr)\ =\ \tau\bigl(\kappa_{u^{-1}}(\gamma)^{\,b}\bigr)\qquad(\forall\gamma\in G_K)\ } \tag{B7tw} $$
> **証明.** 定理 B-7 の証明の最終行で補題 B-6 (8.1) を補題 B-6$^{\rm tw}$ (8.2) に置換すればよい。∎

> **★ 状態札(正確に)**:
> | 主張 | 前件 | 状態 |
> |---|---|---|
> | **B-7**(exact, $b=1$) | (TB1)–(TB4)+(CAL)+(W1)–(W5) | `paper-proof / two-mathematician PASS`。**(TB4) が文献関所** |
> | **B-7$^{\rm tw}$**(orientation-free) | (TB1)(TB2)(TB3)**(TB4$^{\rm u}$)**+(CAL)+(W1)–(W5) | `paper-proof`。**「無条件」ではなく (TB4$^{\rm u}$)-条件つき** |
> | **系 B-8** | (10.1) を**仮定**したときの不変性 | 補題(存在命題ではない) |
>
> **★ 使い分け**: (TB4) が関所を通る前は **B-7$^{\rm tw}$ + 系 B-8** で単一窓の結論((R6-full)・(7.4))が出る。**exact $b=1$ が要るのは二 dessin 比較 $a_{\rm eff}$ の側だけ**である(§10)。
> **★ $b$ は窓ごとの自由変数ではない**(便 44 F7.3): (2.1) の $\varepsilon$ は **$x$ と $(\zeta_n)$ と局所比較だけから決まる枠組みレベルの 1 単位**であり、その $\bmod\,M$ 還元が $b$。ゆえに同じ $M$ の二 dessin では**数学上 $b_{\rm sq}=b_{\rm ns}$ が従う**。Rule 1 §7.3 が両方を記録するのは、**実装 transport が同じ規約を実現したかの検査**であって、数学的自由度の記録ではない — この読み替えにより Rule 1 の受理条件はいっそう正当化される。

---

## 9. 主定理

> ### 定理 B-7(比較橋 $B_{\rm FC}$).
> **枠組み** (TB1)–(TB4)、**較正** $\alpha^{\rm Ih}=\alpha^{\rm std}$($A_5$ v4 §1.4・窓非依存)、**窓前件** (W1)(W2)(W3)(W4)(W5) の下で:
> **(a)** 一意な $K$-モデル $W_0\to U_K$ が存在し、$\lambda^{-1}(0)$ は唯一の $K$-有理点 $P_0$(分岐指数 $M$)。
> **(b)** $[u]_M\in K^\times/K^{\times M}$ が窓のデータだけから定まる。
> **(c)** すべての $\gamma\in G_K$ について
> $$ \boxed{\ \rho_\Lambda\bigl(\mathrm{Ih}_N(\gamma)\bigr)\ =\ \tau\bigl(\kappa_{u^{-1}}(\gamma)\bigr) \ } \tag{9.1} $$
> — すなわち **v3.1 の (5′) = (7.3)**。同値に、shadow 類 $=$ Belyi 類: $\mathfrak s(N,H)=[u^{-1}]$。

**証明.** (a) は定理 B-4 + 補題 B-5(i)。(b) は補題 B-5(ii)。(c): 定理 B-3 より $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(c(\gamma))$。他方、系 B-4c の $c_\Lambda$ は $G_K$-同変だから、$\Lambda$ 上の $G_K$-作用は $\mathrm{Fib}$ 上の作用の輸送であり、(7.2) と補題 B-6 (8.1) より
$$ \rho_\Lambda(\mathrm{Ih}_N(\gamma))\ \overset{\text{系 B-4c}}{=}\ c_\Lambda\circ\bigl(\gamma\text{-作用}\bigr)\circ c_\Lambda^{-1}\ \overset{(7.2)}{=}\ c_\Lambda\circ m(\kappa_{u^{-1}}(\gamma))\circ c_\Lambda^{-1}\ \overset{(8.1)}{=}\ \tau(\kappa_{u^{-1}}(\gamma)). $$
$\tau$ 単射より $c=\kappa_{u^{-1}}$。∎

> **系 B-7′(族定理).** 定理 B-7 の前件に加えて $R^{\rm cyc}_{\rm formal}$ の前件 **(2)**($\mathfrak F_0\cong C_e$, $e\mid M$)と **(6′) の忠実性**($\rho_0$ が忠実)を仮定すれば、v3.1 §5.2.2 の証明と合わせて
> $$ \mathrm{Ih}_N\ \text{が全射}\iff\mathrm{ord}\bigl([u^{-1}]_M\bigr)=e,\qquad \mathrm{Fix}(\ker\mathrm{Ih}_N)=K\bigl((u^{-1})^{1/M}\bigr) $$
> が**前件から結論まで一貫した定理として**成立する。**これが「族定理 $R^{\rm cyc}$」の完成形である。**
> **前件の総数は 7 本**: (W1)(W2)(W3)(W4)(W5) + (2) + 「$\rho_0$ 忠実」。**すべて有限計算か正典読み取りで決着する。**

> **★【v2】B-7 の前件欄は v1 から不変である。** R2(B-3 の (W3))・R3(B-4 の (W2))はいずれも**下位補題の前件欄の脱落**であり、**主定理 B-7 は初めから (W1)–(W5) を全部仮定していた**ので、修理により結論は 1 ミリも動かない(便 43 F7 が同旨)。R4 の剰余類修理後も上の合成は同じ式になる(便 43 F7 が独立に再構成)。
>
> **⚠ 状態札(誇張しない)【v2 更新】**: 系 B-7′ は **`paper-proof (framework-conditional on TB1–TB4) / two-mathematician audit PASS`**(便 43 F10・裁定 44)。(i) **Lean `verified` ではない(未着手)**、(ii) **exact $b=1$ の向きは (TB4) 関所待ち**(**【v2.1・T1】**その手前は **定理 B-7$^{\rm tw}$**(§8.1)が **(TB4$^{\rm u}$)-条件つき**で使える — **「無条件」ではない**)、(iii) $u$ の**計算**は依然窓固有(§12.2)、(iv) 有限計算 bundle は **`source-audited candidate`**(§15.7)。

---

## 10. $b$ の自由度 — Rule 1 (7.1)(7.2) の型で吸収できるか

**答: できる。しかも二重に。**

> **系 B-8($b$-頑健性).** $b\in(\mathbb Z/M)^\times$ を任意とし、(9.1) の代わりに**ひねった形**
> $$ \rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau\bigl(\kappa_{u^{-1}}(\gamma)^b\bigr)\qquad(\forall\gamma\in G_K) \tag{10.1} $$
> を仮定しても、$R^{\rm cyc}_{\rm formal}$ の結論 **(R6-full)** と **(7.4)** は**変わらない**。
> **証明.** $\xi\mapsto\xi^b$ は $\mu_M$ の自己同型なので (i) $\lvert\kappa^b(G_K)\rvert=\lvert\kappa(G_K)\rvert=\mathrm{ord}([u^{-1}]_M)$、(ii) $\mu_M[e]$ は $\mu_M$ の特性部分群ゆえ $\kappa^b(G_K)\subseteq\mu_M[e]\iff\kappa(G_K)\subseteq\mu_M[e]$、(iii) $\ker\kappa^b=\ker\kappa$。v3.1 §5.2.2 の証明の 2・3・5 はこれらしか使わない。∎(検算 **V8**)

**吸収の二層**:

| 層 | 内容 | 帰結 |
|---|---|---|
| **第 1 層(数学)** | **(TB2)+(TB4) の規約に相対的に** $b=1$ が定理(補題 B-6)【v2・R6 で「相対的」を明記】 | 規約どおりの実装なら $b_i=1$ が出る「はず」 |
| **第 2 層(頑健性)** | $b\ne1$ でも結論不変(系 B-8) | 万一 $b_i\ne1$ でも**単一窓の $R^{\rm cyc}$ は生き残る** |

> **⚠ ただし $K^{(5)}$ の二 dessin 比較 (P2) では $b$ は依然 load-bearing**: Sol 便 31 F5.2 の $a_{\rm eff}=[b_{\rm ns}]^{-1}a[b_{\rm sq}]$ は**二つの窓の間の比較**であり、系 B-8 の「単一窓では相殺」は効かない。$b_{\rm sq}\ne b_{\rm ns}$ なら $[u_{\rm ns}^{-1}]_{10}=[u_{\rm sq}^{-1}]_{10}$ という完全一致形が崩れる。**Rule 1 §7.3 の受理条件 $b_{\rm sq}=b_{\rm ns}$ は正しく、本稿は撤回を要求しない。**
> **【v2・R6】本稿が言えることの正確な形**(便 43 F6.2・F6.3): 「$b_i\ne1$ が出たら、それは発見ではなく **TB2 / TB4 / 左右作用 / 共役 transport のいずれかの不一致**である」。v1 は診断先を **(TB2) 単独**に絞っていたが、**(TB4) の向き自体が結論の向きを含む**ので狭すぎた。**自認。**
> **★ 段階的定理化【v2.1・T1 で修理】**: **(TB4) が文献関所で閉じる前でも、「ある単位 $b\in(\mathbb Z/M)^\times$ を伴う twisted bridge」((B7tw) 形)が使える** — ただしそれは **定理 B-7$^{\rm tw}$**(§8.1)であって、**前件は (TB4$^{\rm u}$) である。「無条件」ではない。**
> **v2 の誤り(自認・便 44 F7.1)**: v2 はこれを「無条件」と書いた。系 B-8 は **(10.1) を仮定したときの不変性**しか言わないので、そこから **$\exists b$** は出ない — **循環していた**。存在は §8.1 の (2.1)(「$x$ と $\iota(\sigma_\zeta)$ は同じ procyclic 慣性の位相的生成元だから一意な $\varepsilon\in\hat{\mathbb Z}^\times$ で結ばれる」)から**証明**される。

---

## 11. 実例二つとの整合検査

### 11.1 $A_5$ 窓

| 前件 | 値 / 根拠 | 判定 |
|---|---|---|
| (W1) | $N_A$ isolated(裁定 15 A1.v2.2・二系統) | ✓ |
| (W2) | $\lvert\mathrm{GT}\rvert=20$、$(\mathbb Z/10)^\times\cong C_4$、$\mathfrak F_0\cong C_5$、$K=\mathbb Q(\zeta_{10})=\mathbb Q(\zeta_5)$ | ✓ |
| (W3) | $N_{A_5}(A_4)=A_4$(v4 (3.2)) | ✓ |
| (W4) | $X$ は 5-サイクル ⇒ $A_5/A_4$(5 点)上推移的、$[P:H]=5=M$ | ✓ |
| (W5)/(W5$^\mathbb Q$) | $\mathrm{Aut}(A_5)=S_5$ は指数 5 部分群の唯一の類を保つ | ✓(自明に成立) |
| **帰結** | $\mathbb Q$-モデル存在・$P_0$ が $\mathbb Q$-有理・全分岐 5 | v4 §2.1 の LMFDB モデルと一致 |
| **(9.1)** | $\tau(\kappa_{-2}(\gamma))$ = v4 (3.5) の $j\mapsto j+\kappa(\gamma)$($G_K$ 上 $\chi_5=1$) | **逐語一致** ✓ |

**★ $A_5$ で FC-4(b)(passport 悉皆一意性)が要らなかったこと**の確認: 定理 B-4 は $H$ から直接 $W_0$ を作るので、「その型の dessin が一意」は不要。v4 の悉皆は**モデル認識**(LMFDB モデル = $W_0$)にのみ使われていた。実際 v4 §3.4 の【v3 追加】自身が「(3.3) の exact conjugator で FC-4(d) の load-bearing 部分は直接閉じるので、(b) の悉皆は補助証拠に落とす」と書いており、**本稿の分離と独立に同じ結論に達していた**。

### 11.2 $K^{(3)}$ 窓 — 検算 `search/week4-bfc-antecedents.mjs`(13/13)

| # | 検査 | 結果 |
|---|---|---|
| **V1** | $[P:H]=6=M=\mathrm{ord}(X)$、$\langle X\rangle$ が $P/H$ 上推移的 | PASS |
| **V2** | $N_P(H)=H$ | PASS |
| **V3** | 命題 B-2 の悉皆: 「$\langle X\rangle$ 推移的 かつ $\lvert\Lambda\rvert=6$」を満たす $H$ は 12 個、**すべて** $N_P(H)=H$(反例 0) | PASS |
| **V4** | $P/H\to\Lambda$ が $\langle X\rangle$-同変全単射・$\tau$ は 6-サイクル | PASS |
| **V5** | $\Lambda$ は $\Phi(\mathfrak F_0)$(3 元)で安定 | PASS |
| **V6** | **【新規】**$\Lambda$ は $\Phi(\mathrm{GT}(K^{(3)}))$ 全 12 元で安定 ⇒ **$\mathbb Q$-モデルが (W5$^\mathbb Q$) から従う** | PASS |
| **V7** | **【新規】**$\lvert\mathrm{Aut}(G_3)\rvert=1296$、$\Lambda$ を保つのは **432 個**のみ ⇒ (W5) は自明でない | PASS |
| **V8** | $b\in(\mathbb Z/6)^\times$ のひねりで $\mathrm{ord}(\kappa)$・$\ker\kappa$・$\tau(\mu_6)$ が不変(系 B-8) | PASS |

> **★ V6 の意味(v3.1 への上向きの寄与)【v2・S3 で射程限定】**: 定理 K3 §2.2 (P7) は「残留 descent なし」を、明示 $\mathbb Q$-モデル + exact marking + $N_G(H)/H=1$ に依拠して主張していた(W5 に従い「$\mathrm{Aut}=1$ 単独では不十分」と正しく限定した上で)。**V6 が埋めるのは「$\Phi(\mathrm{GT}(K^{(3)}))$ が標的の個々の $G_3$-共役類を保つ」という一点**であり、これと (W3)・較正・剛性 descent を合わせると、**標的の抽象的な非標識被覆が $\mathbb Q$ 上へ一意に下降することを、明示曲線なしに再導出できる**。
> **⇒ 正確な記録**(便 43 F8.2): 「(P7) 全部を明示モデル非依存に置換」**ではなく**、
> $$ \boxed{\text{(P7) の\ }\textbf{非標識 }\mathbb Q\textbf{-descent 部分}\text{\ に独立な抽象証明を追加}} $$
> である。**次の 4 つは置換しない**: (i) 手元の明示曲線がその抽象被覆であるというモデル認識、(ii) ordered passport と actual marking、(iii) exact conjugator (P4)/(R-2)、(iv) そのモデル上の $u$ の抽出。また**「有限群論だけ」の証明でもない** — 有限事実 V6 に **B-4 の descent 枠組み**(較正込み)を合成した証明である。**v1 の「有限群論だけで再導出」は言い過ぎ。自認。**
>
> **★ V7 の意味**: $\Phi(\mathrm{GT})\subsetneq\{$ $\Lambda$ を setwise に保つ 432 元 $\}\subsetneq\mathrm{Aut}(G_3)$。**もし $\Phi(\mathrm{GT})$ が 432 の外にはみ出していたら (W5$^\mathbb Q$) が破れ、この経路では $\mathbb Q$-モデルを得られなかった。** 実例が「たまたま」ではないことの確認。**【v2.1・T7】数値 432/1296 と V6 の機械状態は、GAP 側が 17/17 で一致した後も `source-audited candidate` のまま** — 便 44 F6.1 の marked-fidelity blocker($z$ が未移送で $x_gy_gz_g=(r,1,r^2)
e1$・本稿で独立再現)が閉じるまで昇格しない(§15.7)。

### 11.3 整合の総括

**二例とも、本稿の前件 (W1)–(W5) を満たし、本稿の結論 (9.1) が既存の個別計算と逐語一致する。** 一般化が二例を再現できないという事故はない。

---

## 12. 閉じなかったもの — 障害の同定

### 12.1 【GAP-TB】(唯一の残存)— 接基点繊維関手の 4 性質

> **【GAP-TB】** (TB1)(TB3)(TB4) の標準事実部分に、原典の §/定理番号を付けた照合が無い。
> - **(TB1)** 接基点での繊維関手が $\pi_1$-集合の圏同値を与えること。
> - **(TB3)** $\pi_1(U_{\bar{\mathbb Q}},\vec{01})\cong\hat F_2$ と慣性生成元の指定。
> - **(TB4)(最重要)** $\vec{01}$ における慣性が $\mathrm{Gal}(\Omega/\bar{\mathbb Q}((\beta)))\cong\hat{\mathbb Z}(1)$ と**正準に**同一視され、$\mathrm{Fib}$ への作用が $\Omega$ への後合成であること。
>
> **障害の正確な所在【v2・S1 で射程限定】**: **exact $b=1$ の向きについては (TB4) が第 $k$ 段**である。**(TB4) が破れると補題 B-6 の 1(「$x\cdot p=\zeta_Mp$」)の向きが決まらず、$\Lambda$ と $\mathrm{Fib}$ の $\mu_M$-torsor 構造の同一視が単位 $b$ だけずれる。すると (9.1) は「$\tau(\kappa_{u^{-1}}^{\,b})$」までしか言えない**(結論は系 B-8 で救われるが、二 dessin 比較には効く)。
> **⚠ v1 の「(TB1)(TB3) は破れても記法の問題にとどまる」は言い過ぎ**(便 43 F7)。**(TB1) の圏同値も (TB3) の慣性生成元同定も、論理上は B-4/B-5 の土台**であり、真に破れれば記法では済まない。正しい札の書き方は
> ```text
> TB1–TB4 = global framework assumptions
> TB4     = unique orientation-sensitive literature gate for exact b = 1
> ```
> **自認。**
>
> **新しい穴ではない**: $A_5$ v4 §6 の【GAP-C3】(「枠組みそのもの — 接基点での繊維関手の存在と Galois 同変性」)と同じもの。**本稿はそれを 4 項目に分解し、うち (TB4) が向き感受性の唯一の関所であることを特定した。** これは前進(粗い札 → 名指しの 1 項目)。
>
> **両実例も同じ札に依存していた**: $A_5$ v4 §3.5 の「$\gamma$ は $\beta^{1/5}$ を固定し係数のみに作用」と「$\hat F_2$ の $\mathrm{Fib}$ への作用」の突合、$K^{(3)}$ §2.1 の「局所 Kummer」。**本稿は依存を増やしていない。**

> ### 【文献要請 13】接基点における慣性の正準同一視
> **困難**: 補題 B-6 の第 1 段(= (TB4))。$U=\mathbf P^1-\{0,1,\infty\}$ の $0$ での接基点 $\vec{01}$ について、
> (i) 繊維関手 $\mathrm{Fib}_{\vec{01}}(W)=\mathrm{Hom}_{k((\beta))}(\mathcal O(W\times_U k((\beta))),\Omega)$ が $\pi_1(U_k,\vec{01})$-集合の圏同値を与えること、
> (ii) $\mathrm{Gal}(\Omega/\bar k((\beta)))\cong\hat{\mathbb Z}(1)$ の像が $0$ の慣性部分群であり、$(\zeta_n)$ が定める生成元が標準生成元 $x$ に対応すること、
> (iii) $G_k$ の**係数作用**が定める分裂と (ii) の慣性作用が、どちらも $\Omega$ への後合成として**同時に**記述されること。
> **欲しい結果の型**: 上の (i)–(iii) を、$\S$/定理番号つきで述べた文献 1 本(または各項目に 1 本ずつ)。第一候補は Deligne, *Le groupe fondamental de la droite projective moins trois points*(1989)の §15(既に $A_5$ v4 §1.4.4 が名指ししている)。**優先度は中**: 本稿の結論は (TB1)–(TB4) を定義/規約として採る限り自己完結しており、これは**枠組みの裏取り**である。
> **注意【v2.1・T1 で精密化】**: 降ろされた場合、確認すべきは「**(TB4) の生成元の向きが $(\zeta_n)$ とどう結びつくか**」の 1 点、すなわち (2.1) の $\varepsilon$ が $1$ かどうかである。
> **⇒ 関所の射程は狭い**: (i)(iii) と **(TB4$^{\rm u}$)**(慣性の部分群と作用の型のみ)が取れれば **定理 B-7$^{\rm tw}$** が立ち、系 B-8 と合わせて**単一窓の結論((R6-full)・(7.4))はもう出る**。**文献が要るのは exact $\varepsilon=1$ だけ**で、それが効くのは二 dessin 比較 $a_{\rm eff}$ の側である。
> **★ 追加の論点(便 44 F7.2)**: 「(TB1)+(TB3) の『inertia generator』という語から (TB4$^{\rm u}$) が既に従う」と主張するなら、その導出を一段書く必要がある。**本稿は現状 (TB4$^{\rm u}$) を独立の枠組み仮定として立てている**(§14.1-2)。

### 12.2 橋の外へ出したもの — 「モデル認識段」(命題 B-9)

定理 B-7 は $W_0$ の**存在と一意性**を言うが、**手元の明示曲線 $C$ が $W_0$ であること**は言わない。$u$ を数値として計算するにはこれが要る。

> **命題 B-9(モデル認識).** $(C,\lambda_C)$ を $K$ 上の滑らかな射影曲線と Belyi 写像で、$C|_U\to U$ が有限エタール・幾何的連結とする。**証明書**として
> **(R-1)** $C_{\mathbb C}$ の分岐 cycle 三つ組 $(\sigma_0,\sigma_1,\sigma_\infty)$($\sigma_0\sigma_1\sigma_\infty=1$、標準的向き・$0,1,\infty$ の順)、
> **(R-2)** 明示的共役元 $h$ で $h\sigma_0h^{-1}=X_{|P/H},\ h\sigma_1h^{-1}=Y_{|P/H},\ h\sigma_\infty h^{-1}=Z_{|P/H}$(同時共役)
> が与えられれば、$C\cong W_0$($U$ 上の $K$-同型)であり、したがって $[u_C]_M=[u]_M$。
> **証明(素描).** (R-2) は $C$ の幾何 monodromy 表現の核が $\bar N$ を含み、点 stabilizer が $\tilde H$ の共役であることを与える(3 点球面の pure mapping class group は自明ゆえ標準生成三つ組は同時共役を除き一意)。ゆえに $C\times_K\bar{\mathbb Q}\cong W$。$C$ が $K$-モデルだから定理 B-4 の一意性で $C\cong W_0$。∎
>
> **状態**: 素描である。**「3 点球面の標準生成三つ組は同時共役を除き一意」という位相的事実**と、**位相的 $\pi_1$ と接基点 $\pi_1$ の比較**(Riemann existence + 経路の取り替え = 共役)を使っており、これは (TB1)–(TB4) と同格の枠組み事実である。**【GAP-TB】に相乗りする。**
>
> **★ これが両実例の「一番手間のかかった部分」の正体**: $A_5$ の (3.3)($h=(1\,3\,4\,5)$)も $K^{(3)}$ の (P4)($h=[6,1,5,4,2,3]$)も、**命題 B-9 の (R-2) そのもの**である。$K^{(3)}$ §3 の Möbius 正規化の数え方(ordered passport 保存 2 通り)は、(R-1) の「$0,1,\infty$ の順」を手元のデータベース記法に合わせる作業であった。
>
> **⇒ 運用上の帰結【v2・R6 で用語修正】**: 封印対象は「明示モデル」ではなく **MODEL 層の (R-1)(R-2) 証明書**である(§13.3)。**橋(定理 B-7)は封印の外に出せる**(結果に依存しない一般論だから)。**証明書が取れないのは `MODEL-UNKNOWN`、証明書が別の標的を指したときだけ `MODEL-MISMATCH`**(便 43 F9)。

### 12.3 自己申告 2 か所 —【**v2: 便 43 の判定を記入**】

| # | 箇所 | v1 の不安 | **便 43 の判定** |
|---|---|---|---|
| **A-1** | **§6 定理 B-4 の cocycle 自動性** | (6.1) の一意性から cocycle 条件を導く 3 行。$\alpha$ が左作用であること・$\rtimes$ の積の向きの取り違え | **PASS(閉鎖)**。便 43 F3.1 が同じ半直積規約 $(g,\gamma)(g',\delta)=(g\alpha_\gamma(g'),\gamma\delta)$ で独立再計算し「**積順序・逆元位置の反転はない**」と確認。助言に従いコンパクト半群補題を一行明記した |
| **A-2** | **§8 補題 B-6 の 1** | (TB4) から「$x\cdot p=m(\zeta_M)p$」を出す段。後合成が左作用であること | **条件つき PASS**。便 43 F6.1 が「**左作用修理(R4)後**は追加の逆数は現れない」と確認。ただし **(TB4) をこの向きで採用する限り**であり、向き自体は【GAP-TB】の関所に残る |

> **★ 自己申告の当たり外れ(★教材 7 の素材)**: 私が申告した 2 件は**どちらも通った**。実際に修理が要ったのは**申告していなかった 4 か所**(B-2 の同値・B-3 の (W3)・B-4 の (W2)・B-4c の剰余類)だった。**「自分が不安な場所」と「実際に弱い場所」は別物である。** 前者は証明の最終段(派手な箇所)、後者は**前件欄と記法の統一**(地味な箇所)に集中した。

> **さらに小さいが記録しておく点**: 補題 B-5(i) の「唯一の幾何点 ⇒ $\kappa(P_0)=K$」は標数 0 の分離性を使う(幾何点の個数 $=[\kappa(P_0):K]$)。$K$ 完全体ゆえ問題ないが、書いておく。

---

## 13. 前件リストの最終形(封印用)

### 13.1 定理 B-7($B_{\rm FC}$)の前件

| 層 | # | 内容 | 型 | 状態 |
|---|---|---|---|---|
| **枠組み** | (TB1) | 接基点繊維関手の圏同値 | 標準事実 | **【GAP-TB】** |
| | (TB2) | $(\zeta_n)$ 固定・$G_\mathbb Q$ は $\Omega$ に係数作用・$\beta^{1/n}$ 固定 | **当工房の規約** | 閉 |
| | (TB3) | $\pi_1(U_{\bar{\mathbb Q}},\vec{01})=\hat F_2=\langle x,y\rangle$ | 標準事実 | **【GAP-TB】** |
| | (TB4) | $x=$ $(\zeta_n)$ が定める $\hat{\mathbb Z}(1)$ の生成元の像・作用は**左作用としての後合成** | 標準事実 | **【GAP-TB】(exact $b=1$ の向きの唯一の関所)** |
| **較正** | (CAL) | $\alpha^{\rm Ih}=\alpha^{\rm std}$ | 証明済 | **閉**($A_5$ v4 §1.4・窓非依存) |
| **窓** | (W1) | $\bar N$ 開・$G_\mathbb Q$-安定 | 正典 | 窓ごと |
| | (W2) | 完全列 + $\tilde\chi\circ\mathrm{Ih}=\chi_{2M}$ | 正典 | 窓ごと |
| | (W3) | $N_P(H)=H$ | 有限計算 | 窓ごと |
| | (W4) | $\langle X\rangle$ が $P/H$ 上推移的・$[P:H]=M$ | 有限計算 | 窓ごと |
| | (W5) | $\Lambda$ が $\Phi(\mathfrak F_0)$-安定 | 有限計算 | 窓ごと |

**$R^{\rm cyc}$(系 B-7′)にはこれに 2 本足す**: **(2)** $\mathfrak F_0\cong C_e,\ e\mid M$(正典)/ **(F)** $\rho_0$ が忠実(有限計算)。

**$u$ を数値で得るにはさらに**: **(R-1)(R-2)** モデル認識証明書(命題 B-9)+ 局所展開の計算。

> **【v2】下位補題ごとの前件**(R2/R3/R5 の反映先・§4 の依存表と一致):
> | 補題 | 前件 |
> |---|---|
> | B-3($B_{\rm FC}$-I) | (W1)(W2)(W3)(W4)(W5) |
> | B-4(a)($K$-descent) | (TB1)(TB2)(TB3) + (W1)(W2)(W3)(W5) + (CAL) |
> | B-4(b)($\mathbb Q$-descent) | (TB1)(TB2)(TB3) + (W1)(W3)(W5$^\mathbb Q$) + (CAL)。**(W2) 不要** |
> | B-5(局所・$W_0$ 所与) | (TB1)(TB2)(TB3)(TB4) + (W4) |
> | B-6(torsor 比較) | (TB1)–(TB4) + (W1)–(W5) + (CAL) |
> **⇒ 主定理 B-7 の総前件はこれらの和集合であり、上の表と一致する**(便 43 F5.2 の要求)。

### 13.2 消えた前件(v3.1 からの差分)

| v3.1 | 扱い |
|---|---|
| (4)「明示 $\mathbb Q$-モデル」 | **「明示」を削除・体を分離**【**v2.1・T6**】。**橋には $K$-モデルで足り**、それは **(W1)(W2)(W3)(W5)+(CAL)** から**導かれる**(定理 B-4(a))。**$\mathbb Q$-モデルが要るなら (W5$^\mathbb Q$)**(定理 B-4(b)) |
| (4)「$\mathbb Q$-有理な全分岐 cusp」 | **体を分離**【**v2.1・T6**】。**$K$-有理 cusp $=$ B-4(a)+(W4)**、**$\mathbb Q$-有理 cusp $=$ B-4(b)+(W4)**(補題 B-5(i))。**(W4) 単独からは出ない** |
| (4)「actual marked identification」 | **橋の外へ移動**(命題 B-9 の (R-2)) |
| (5) FC-3 | **削除**。(W1)(W2)(W3)(W5)+(CAL) から**導かれる**(系 B-4c) |
| (5) FC-2b | **残る**(= (CAL))。ただし既に証明済・窓非依存 |
| (3)「$\mathrm{ord}(X)=\lvert\Lambda\rvert=M$・単純推移」 | **(W3)+(W4) に分解**。**【v2・R1】同値は結合形でのみ**: (W4) の下で (W3) $\iff\lvert\Lambda\rvert=M$(命題 B-2 (B2-corr))。**各個 pairwise 同値は偽** |

### 13.3 札の再構成 —【**v2・R6: 便 43 F9 の 6 層表を採用**】

> **v1 の三つの過剰推論を先に自認する**(便 43 F9):
> 1. **「(W5) 不成立 ⇒ $K$-モデルなし」は偽。** (W5) は $\Phi(\mathfrak F_0)$ **全体**の安定性という、実際に必要な $\Phi(\mathrm{Ih}_N(G_K))$-安定性より**強い十分条件**である。$\mathfrak F_0$ に実 Galois 像へ来ない元があれば、**(W5) が破れても $K$-モデルは存在しうる**。不成立時に言えるのは「**この有限 schema では定理を適用できない**」までである。
> 2. **「証明書が取れない ⇒ MODEL-MISMATCH」は偽。** 探索不成功は **`MODEL-UNKNOWN`**。**exact triple/conjugator が別の標的を指したときだけ** `MODEL-MISMATCH`。
> 3. **「BRIDGE-FAIL を削除」は運用として乱暴。** 数学的ケースとしては空にしてよいが、**版管理つきで改名**するのが正しい。

| 層 | IN(封印する内容) | OUT / UNKNOWN / conflict |
|---|---|---|
| **GLOBAL-FRAMEWORK** | (TB1)–(TB4) + (CAL) を固定 | 原典未閉鎖は **`FRAMEWORK-UNKNOWN`**。**TB4 は exact orientation gate**(閉じる前は単位 $b$ までの twisted 版を使う) |
| **WINDOW-SCHEMA** | (W1)–(W5)($R^{\rm cyc}$ ならさらに (2)(F)) | いずれか不成立は **`SCHEMA-OUT`**。**「$K$-モデルが存在しない」とは断言しない** |
| **MODEL** | (R-1)(R-2) の exact 証明書 | 未取得は **`MODEL-UNKNOWN`**、反対証明書は **`MODEL-MISMATCH`** |
| **EXTRACTION** | 同一 sealed model から $u$ の二経路一致 | 不一致は **`EXTRACTION-CONFLICT`** |
| **BRIDGE** | **一般定理として封印の外** | 全前件を満たして等式が破れれば **`THEOREM/RECORD-CONSISTENCY-FAIL`** |
| **ARITHMETIC** | $\mathrm{ord}([u^{-1}]_M)$ | **ここが窓固有の算術結果** |

> **legacy 改名**(削除しない):
> ```text
> legacy BRIDGE-FAIL
>   -> THEOREM / CONVENTION / RECORD-CONSISTENCY-FAIL
> ```
>
> **★ 運用への含意(重要)**: $K^{(5)}$ の封印は「$B_{\rm FC}$ が架かるか」を試す実験だと位置づけられてきたが、修理後にはそうではない。$K^{(5)}$ が実際に測るのは**四束**(便 43 F9 と一致):
> (i) **(W1)–(W5)(および (2)(F))の有限 scope 検査**、
> (ii) **(R-1)(R-2) によるモデル認識**、
> (iii) **sealed model からの $u$ 二経路一致**、
> (iv) **$\mathrm{ord}([u^{-1}]_{10})=5$**。
> **(i)–(iii) は入口・同一性・完全性の検査であり、真の算術予測は (iv) だけ**である。そこが外れたら疑うべきは(橋ではなく)**私の証明か、(W#) の検査か、$u$ の抽出**である。二 dessin 比較ではさらに $b_{\rm sq},b_{\rm ns},a_{\rm eff}$ の **convention seal** を残す。**司令塔の裁定を要する運用変更**なので §14・§15 に上げる。

---

## 14. Sol への論点 —【**v2: 便 43 の回答を記入**】

| # | v1 の論点 | **便 43 の回答** | 残 |
|---|---|---|---|
| 1 | §6 cocycle 自動性(A-1) | **PASS**(F3.1)。同じ半直積規約で独立再計算・反転なし | 閉 |
| 2 | §8 補題 B-6 の 1(A-2) | **条件つき PASS**(F6.1)。左作用修理後は追加の逆数なし。向きは (TB4) 依存 | (TB4) 関所 |
| 3 | 定理 B-3 の射程(補題 $R'$ を $\mathrm{Ih}_N(G_K)$ へ) | **PASS**(F2.2)。ただし **(W3) を前件に足せ**。「型は無料」は「regular detector を払った後は追加の幾何入力が不要」の意 | R2 で反映 |
| 4 | 命題 B-2 の同値 | **FAIL → 結合形で PASS**(F2.1)。反例 $P=S_3\times C_2$ | R1 で反映 |
| 5 | 命題 B-9 の素描 | (直接の裁定なし。§12.2 の【GAP-TB】相乗り扱いは維持) | **論点として残す** |
| 6 | 五札改訂 | **二つの過剰推論を指摘**(F9)。6 層表を採用 | R6 で反映 |
| 7 | (W3) を外す一般化 | **回答あり**(F3.4)。下記 | 閉(結論: 外すな) |

> **【便 43 F3.4 の回答・全文要旨】** $A:=N_P(H)/H$ が非自明なら $C_\gamma/\tilde H$ は一点でなく **$A$-torsor** になり、積のずれが **$A$ 値の 2-cocycle** になる。また $P/H\to\Lambda$ は $\lvert A\rvert:1$。**$A$ が可換でも存在障害は一般に $H^2(G_K,A)$ に残る。** $H^1(G_K,A)$ は「**障害が消えて descent が一つ存在した後の捻りの分類**」であって、「$A$ 可換なら $H^1$ だけで済む」わけではない。
> **⇒ 私の見立て(「$A$ 可換なら $H^1$ の捻れで済む」)は誤りだった。自認。** 自己同型をもつ窓への拡張には価値があるが、**別の gerbe/descent 定理として別 schema にすべきで、現定理から (W3) を外してはならない。**

### 14.1 v2 で残る論点(次便へ)

1. **【推奨】命題 B-9(モデル認識)の素描を定理に格上げできるか。** 「3 点球面の pure mapping class group が自明ゆえ標準生成三つ組は同時共役を除き一意」を私は証明していない。**【文献要請 13】に含めるか別立てか**の判断を仰ぐ。**$K^{(5)}$ の MODEL 層の土台**なので優先度は上がった。
2. ~~**【推奨】単位 $b$ 版の定理化**~~ →**【v2.1・T1 で決着】**便 44 F7.2 の指示どおり **(TB4$^{\rm u}$) を新設し、補題 B-6$^{\rm tw}$・定理 B-7$^{\rm tw}$ を §8.1 に立てた**。**「無条件」は撤回**。$K^{(5)}$ の BRIDGE 層は、(TB4) 関所を待たずに **B-7$^{\rm tw}$ + 系 B-8** で閉じられる(単一窓の結論のみ)。**残る論点**: (TB1)+(TB3) の「inertia generator」という語から **(TB4$^{\rm u}$) が既に出る**と主張してよいか(便 44 F7.2 は「主張するならその導出を一段書け」と指定)。**私は現状 (TB4$^{\rm u}$) を独立の枠組み仮定として立てている。**
3. **【推奨】§13.3 の 6 層表の運用移管先**。この表は本稿(数学)ではなく **manifest / Rule 1 側の正本**に置くべきではないか。

---

## 15. 司令塔への提案

1. **札の更新【v2】**: 【GAP-Rcyc】= $B_{\rm FC}$ を `candidate/UNKNOWN` → **`paper-proof (framework-conditional on TB1–TB4) / two-mathematician audit PASS`**(便 43 F10・裁定 44)。**`verified`(Lean)ではない。**
2. **【GAP-C3】と【GAP-TB】の統合**: 同じ札である。札の本文は便 43 F7 の 2 行(`TB1–TB4 = global framework assumptions` / `TB4 = unique orientation-sensitive literature gate for exact b=1`)をそのまま採る。
3. **【文献要請 13】**(§12.1)を関所へ。優先度中。**§14.1-1(pure mapping class group の自明性)を同梱するか要判断。**
4. **$K^{(5)}$ 運用の再検討**(§13.3): 封印が測る対象が四束に変わる。**凍結 1/2 の内容自体は変更不要**(むしろ (R-1)(R-2) と $u$ 抽出に集中するのが正しい)だが、**「$K^{(5)}$ で $B_{\rm FC}$ を試す」という位置づけの文言**は裁定で更新すべき。**§13.3 の 6 層表の正本を manifest 側へ移すかも同時に裁定を(§14.1-3)。**
5. **検算の恒久化**【**v2.1・T7 で状態を更新**】: `search/week4-bfc-antecedents.mjs`(Node 13/13・便 43 F1 と便 44 F1 が独立再走で再現)+ `search/bfc-antecedents-check.g` / `certificates/bfc/bfc-antecedents.json`(GAP 17/17・便 44 F1 が受領)。**両者は 1296/432/12 で一致しており強い傍証**だが、**§15.7 の marked-fidelity blocker のため公式札は `source-audited candidate` を維持**(`cross-checked` に上げない)。**V6 は定理 K3 §2.2 (P7) の非標識 $\mathbb Q$-descent 部分への第二証明**(モデル認識・marking・$u$ 抽出は置換しない)だが、**登録は fidelity gate 閉鎖後**(便 44 F9)。
6. **可視化**: 「shadow 類 = Belyi 類」という一行と、$B_{\rm FC}$-I/II-a/II-b/II-c の 4 枚分解は図にすると効く(🌒 の拡張候補)。**$B$-7 と $B$-7$^{\rm tw}$ の関係((TB4) と (TB4$^{\rm u}$) の差が単位 $\varepsilon$ 一つ)も図示候補。**
7. **【v2.1・T7】GAP 第二系統の修理指示**(発注ではなく修理 — 便 44 F6): 現 `search/bfc-antecedents-check.g` は **$y$ を GAP 右作用側へ移送($rs\rightsquigarrow s*r$)しながら $z$ を論文座標のまま**置いており、
> $$ x_g\,y_g\,z_g=(r,1,r^2)\ne1\qquad(\textbf{本稿で独立検算・Sol の値と一致}) $$
> **すなわち同じ marked object を照合していない。** 修理は `zg := (xg*yg)^-1`(座標では $(s,\,r^{-1}s,\,r^{-1})$ — **これも独立に再現**)。加えて便 44 F6.3 の 5 項目を **fail-closed** で証明書に入れること:
> **(1)** $x_gy_gz_g=1$ を fixture 化 / **(2)** V3 の件数 `v3n = 12` を assert し JSON に保存(現行は `v3n > 0` のみ)/ **(3)** 便 43 F2.1 の反例 $S_3\times C_2$ で **$\langle X\rangle$ が $P/H$ 上推移的**であることまで検査(現行は位数・指数・normalizer のみ)/ **(4)** $\Phi$ による **$x,y,z,f_{m,k}$ の同時移送**を証明書化 — とくに `kapExp := -kap` は「全単射になる符号を選んだ」ではなく **$\phi_3(r)=r^{-1}$ からの紙上導出**を根拠にし、自己同型性はその後の**反証テスト**にする / **(5)** script/input digest と各値の JSON 記録。
> **これを再走して再現した時点で V1–V8 bundle を `cross-checked` へ上げてよい。** implementer 案件。

---

## 16. ★教材(本稿で学んだこと)

1. **「未証明の橋」は分解すると型の段と同定の段に割れ、型の段は無料であることが多い。** $B_{\rm FC}$-I は既に手元にあった補題 $R'$ の別の適用先にすぎなかった。**同じ補題を二度使えることに気づかないと、未証明部を過大に見積もる。**
2. **「明示モデル」は前件ではなく計算手段である。** 存在と一意性が言えれば橋は架かる。両実例が明示モデルから出発したので、それが前件に見えていた。**出発点と前件を混同しない。**
3. **規約の自由度は、同じ規約を二度使うと消える。** $b$ は「$x$ の向き」と「$\kappa$ の値」の両方を $(\zeta_n)$ が決めるので相殺する。**独立に見える二つの規約が同一起源かを必ず問う。**
4. **前件の非自明性は数えて確かめる。ただし「数えた比」と「条件そのもの」を混同しない。** (W5) の非自明性は $\mathrm{Aut}(G_3)$ の 1296 元中 432 元という周囲データで示されるが、**(W5) 自体は「指定された 3 元/12 元がその 432 元に入る」という包含条件**である(便 43 F8.1)。「たぶん成り立つ」で済ませていたら族の一般化で最初に破れる項目を見逃したが、**比を条件そのものと呼ぶのも別の粗さ**である。
5. **橋が定理になると falsifier の宛先が移る(消えるのではない)。** ★教材 12(便 29)の裏面: 未証明部を証明したら BRIDGE-FAIL は**数学的ケースとしては**空になるが、**削除ではなく版管理つきの改名** `THEOREM/CONVENTION/RECORD-CONSISTENCY-FAIL` が正しい(便 43 F9)。さらに**層を割る**と、失敗の宛先は `FRAMEWORK-UNKNOWN` / `SCHEMA-OUT` / `MODEL-UNKNOWN` / `MODEL-MISMATCH` / `EXTRACTION-CONFLICT` に**分配される**。実験の意味づけを同時に更新しないと、「何も試していない試験」を走らせることになる。**【v2 追記】v1 はここで「空になる」と書き、(W5) 不成立や証明書未取得を強い札に直結させた — 過剰推論だった。**
6. **枠組み札は「粗いまま放置」ではなく「項目に割って load-bearing を名指し」する。**【GAP-C3】→ (TB1)–(TB4) → **(TB4) が向き感受性の関所**。同じ未閉鎖でも、次に何を取りに行くかが決まる。**ただし「名指ししなかった項目は無害」ではない**(v1 は (TB1)(TB3) を「記法の問題」と書いて言い過ぎた・便 43 F7)。**名指しは優先順位であって免責ではない。**

### 【v2 追加】

7. **自分が不安な場所と、実際に弱い場所は別物である。** v1 で自己申告した 2 件(cocycle の向き・(TB4) の適用)は**どちらも監査を通った**。実際に修理が要ったのは**申告していなかった 4 か所** — 命題 B-2 の同値・定理 B-3 の (W3)・定理 B-4 の (W2)・系 B-4c の剰余類。**不安は「証明の派手な段」に集まり、欠陥は「前件欄と記法の統一」という地味な場所に出た。** ⇒ 次回は**定理文の前件欄を、証明本文とは独立にもう一度読み直す**手順を入れる。
8. **不等式の連鎖で「全部等号」を出したら、どの端を止めたから等号になったのかを書く。** 命題 B-2 の $\lvert\Lambda\rvert\le[P:H]\le M$ は、**両端を止めて初めて**中間が決まる。v1 は各段を独立の同値として読み、**pairwise 同値という偽の主張**を書いた。⇒ **「$\iff$ を 2 つ並べる前に、片方向の反例を 30 秒探す。」**
9. **左右剰余類は、部分群が正規でない限り書き分ける。** $\mathcal H\backslash\pi_1$ と $\pi_1/\mathcal H$ を混ぜると、**その先の作用の向き($b$ の値)が決まらない**。作用が左なら剰余類も左に統一する。**組版に見えて、実は結論の向きを支えている。**

### 【v2.1 追加】

10. **「$X$ を仮定すれば結論が $X$ に依らない」から「$X$ が存在する」は出ない。** 系 B-8 は (10.1) を**仮定したとき**の不変性補題である。v2 はそこから「単位 $b$ 版は無条件」と書いた — **不変性を存在証明に読み替える**という循環だった。存在は別途 (2.1)(procyclic 慣性の生成元は単位一つで結ばれる)から証明する必要があった。**⇒「無条件」と書く前に、その主張の $\exists$ をどの補題が出しているかを指さす。**
11. **凍結済みの規約と衝突したら、必ず凍結側に合わせる — しかも「$b$ か $b^{-1}$ か」は 1 行で検算できる。** v2 は付録 A で $\tau(\zeta_M^{b^{-1}})$、§10 で $\kappa^b$ と書き、**同じ文書の中で逆数がずれていた**。Rule 1 (7.1) は凍結済みなのでそちらが正。**⇒ 新しい記号を定義したら、既存の凍結文書の対応式と生成元 1 個で突き合わせる。**
12. **「値が一致した」は「同じ対象を照合した」ではない。** GAP 第二系統は 1296/432/12 を Node と一致させたが、$z$ の移送漏れで $x_gy_gz_g\ne1$ — **別の marked object を数えて同じ数に着地していた**。★教材 2(★教材 12・便 29 系)の変奏: **cross-check の型は「値の一致」ではなく「同一対象の独立照合」である。** ⇒ **照合器には必ず「同じ対象か」を問う fixture($xyz=1$ 等)を fail-closed で入れる。**

---

## 付録 A. 記号表(本稿で新規に導入したもの)

| 記号 | 型 | 定義 |
|---|---|---|
| $\tilde H$ | $\hat F_2$ の開部分群 | $\pi^{-1}(H)$ |
| $\tilde\Lambda$ | 有限集合 | $\tilde H$ の $\hat F_2$-共役全体($\cong\Lambda$) |
| $m$ | $\mu_M\to\mathrm{Sym}(\mathrm{Fib})$ | (7.1) の乗法作用($\mu_M$-torsor 構造) |
| $c$ | $G_K\to\mu_M$ | (5.1)。**【v2.1・T3】定理 B-3 の前件 (W1)–(W5) の下で存在**(v2 の「無条件に存在」は R2 と矛盾する stale statement だった・便 44 F2.2) |
| $\mathfrak s(N,H)$ | $K^\times/K^{\times M}$ | **shadow 類** $=[c]$(5.2) |
| $c_\Lambda$ | $\mathrm{Fib}\xrightarrow{\sim}\Lambda$ | 系 B-4c(= FC-3)の同型 |
| $\tilde s$ | $K[[s]]$ の uniformizer | $s\,h^{1/M}$、$\tilde s^M=u^{-1}\beta$(補題 B-5(iii)) |
| $\varepsilon$ | $\hat{\mathbb Z}^\times$ | **【v2.1・T1 新規】**$x=\iota(\sigma_\zeta^{\,\varepsilon})$ を定める一意な単位(2.1)。**(TB4) $\iff\varepsilon=1$** |
| $b$ | $(\mathbb Z/M)^\times$ | **【v2.1・T2 で Rule 1 規約へ統一】** $$\boxed{\ c_\Lambda\, m(\zeta_M)\, c_\Lambda^{-1}\ =\ \tau\bigl(\zeta_M^{\,b}\bigr)\ }$$ で定義($b=\varepsilon^{-1}\bmod M$・(8.2))。**これは Rule 1 (7.1) $c_i\ell_ic_i^{-1}=\tau_i(\zeta_{10}^{\,b_i})$ および §10 (10.1) $\rho=\tau\circ[b]\circ\kappa$ と同一規約**。exact (TB4) は $\varepsilon=1$、すなわち **$b=1$** の特殊化(補題 B-6) |

> **⚠【v2.1・T2】v2 の付録 A は $\tau(\zeta_M^{\,b^{-1}})$ と定義しながら §10 では $\kappa^b$ を使っており、Rule 1 と逆数で食い違っていた**(便 44 F7.3)。**Rule 1 は凍結済みなので Rule 1 側を正とし、BFC 側を上の形へ統一した。** 逆数規約を残すと (10.1) と $a_{\rm eff}$ を全部裏返す必要が生じるので採らない。**自認。**
> **$b$ は窓ごとの自由変数ではない**: $\varepsilon$ は $x$・$(\zeta_n)$・局所比較だけから決まる**枠組みレベルの 1 単位**であり、その $\bmod M$ 還元が $b$。ゆえに同じ $M$ の二 dessin では**数学上 $b_{\rm sq}=b_{\rm ns}$**(§8.1 末)。

## 付録 B. 番号つき主張の一覧(機械照合用)

**【v2.1・T6】**旧 3 列 header の残骸を除去した(便 44 F8-6)。

| # | 主張 | 前件 | 検算 | 監査判定 |
|---|---|---|---|---|
| **B-1** | regular 可換部分群は $\mathrm{Sym}$ 内で自己中心化 | — | 紙上(3 行) | PASS |
| **B-2** | **【v2・R1】**(B2-corr): $\lvert\Lambda\rvert=M\iff([P:H]=M$ かつ $N_P(H)=H)$。**pairwise 同値ではない**。(B2-bij): $P/H\to\Lambda$ 全単射 $\iff N_P(H)=H$($M$ 無関係) | $\langle X\rangle$ 推移・$\mathrm{ord}(X)=M$ | **V3・V4** | v1 FAIL → 結合形 PASS |
| **B-3** | $B_{\rm FC}$-I: $c\in\mathrm{Hom}(G_K,\mu_M)$ の存在と一意性 | **(W1)(W2)(W3)(W4)(W5)**【R2】 | **V5**(前件)・紙上 | (W3) 追加で PASS |
| **B-4** | 剛性 descent: (a) $K$-モデル / (b) $\mathbb Q$-モデルの存在と一意性 | (a) **(W1)(W2)(W3)(W5)**+(CAL)【R3】 / (b) (W1)(W3)(W5$^\mathbb Q$)+(CAL) | **V2・V5・V6** | (W2) 追加で PASS |
| **B-4c** | FC-3(**左作用・左剰余類**)【R4】 | B-4 | **V4** | 記法修理で PASS |
| **B-5** | 局所 Kummer: $\mathrm{Fib}$ の Kummer 表示と torsor 類 $[u^{-1}]$ | (TB1)–(TB4)+(W4)【R5】 | 紙上($A_5$ §3.5 と逐語一致) | PASS |
| **B-6** | torsor 比較・**$b=1$((TB2)+(TB4) に相対的)** | (TB1)–(TB4)+(W1)–(W5)+(CAL) | 紙上 | (TB4) 条件つき PASS |
| **B-6$^{\rm tw}$** | **【v2.1・T1 新規】**orientation-free torsor comparison: $c_\Lambda m(\xi)c_\Lambda^{-1}=\tau(\xi^b)$、$b=\varepsilon^{-1}$ (8.2) | (TB1)(TB2)(TB3)**(TB4$^{\rm u}$)**+(W1)–(W5)+(CAL) | 紙上 | 便 44 F7.2 の指定形 |
| **B-7** | **$B_{\rm FC}$**: $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(\kappa_{u^{-1}}(\gamma))$ | (TB1)–(TB4)+(CAL)+(W1)–(W5) | 二例で逐語一致(§11) | **PASS(便 44 F5/F9 で確定)** |
| **B-7$^{\rm tw}$** | **【v2.1・T1 新規】**twisted bridge (B7tw): $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(\kappa_{u^{-1}}(\gamma)^b)$ | (TB1)(TB2)(TB3)**(TB4$^{\rm u}$)**+(CAL)+(W1)–(W5) | — | **orientation-free だが (TB4$^{\rm u}$)-条件つき。「無条件」ではない** |
| **B-7′** | 族定理 $R^{\rm cyc}$(前件 7 本) | B-7 + (2) + (F) | — | PASS |
| **B-8** | $b$-頑健性(単一窓)。**(10.1) を仮定したときの不変性補題であり、$\exists b$ の存在命題ではない** | (10.1) | **V8** | PASS |
| **B-9** | モデル認識(**素描**・【GAP-TB】相乗り) | (R-1)(R-2) | $A_5$ (3.3)・$K^{(3)}$ (P4) | 未裁定(§14.1-1) |
