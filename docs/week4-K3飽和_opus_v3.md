# 定理 K3 — 奇数側 dihedral 窓 $K^{(3)}$ の算術飽和(答案 **v3**・便 28 追補反映版 / **v3.1 = 便 29 型付けゲート反映**)

2026-07-26 起草・**2026-07-27 v3.1 改訂**: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 24。便 28(PASS・昇格承認)の非 load-bearing 追補 2 件を反映。裁定 22 に基づく。v3.1 は便 29(条件付き PASS)の P1–P4 + F6 を反映。**
v1 は `docs/week4-K3飽和_opus_v1.md`、**v2 は `docs/week4-K3飽和_opus_v2.md` に保存(いずれも上書きしていない)**。
入力: `docs/notes/抽出_Kn定義_D1.md`(正典・逐語)・`docs/week4-A5算術飽和_v4.md` §1(窓非依存部品)・委嘱 18/19/20/21(自作)・`sol/sol_reply_25_u_k3.md`・`sol/sol_reply_27_k3.md`・**`sol/sol_reply_28_k3delta.md`(全文)**・`sol/裁定_22_k3_theorem.md`・`certificates/k3/gap18a.json`・`docs/scout/scout_20260726_6t9_requery.md`。
検算: `search/week4-k3-v2-repairs.mjs`(43/43)・`search/week4-u-k3.mjs`(16/16)・`search/week4-19a19e.mjs`(7/7)・`search/week4-d2d4-k3.mjs`(13/13)。**v3 で追加した §5.2.3 の縮約は `search/r6act-check.mjs` 10/10(司令塔再走で再現・commit a0792b8 で記帳済み)。**
**状態: `paper-proof / two-mathematician audit PASS`(便 28 検収・裁定 22 で確定)。ただし札の射程は項目別 — $\Lambda$ の構造と $\mathfrak F_0$-作用のみ GAP/node `cross-checked`、$\Phi$ 単射(全 12 元)と Aut-融合は紙上+node 単系統(§7.1)。定理全体は `verified`(Lean)ではない。**

---

## v2 → v3 差分一覧

| # | 箇所 | v2 | v3 | 出所 |
|---|---|---|---|---|
| **D1** | §5.2 | 前件 **(6)**: 「pushout $q:\mu_M\twoheadrightarrow\mu_e\xrightarrow{\sim}\mathfrak F_0$ が $\mathfrak F_0$ の $\Lambda$ 上の作用と一致」(語が未定義・$q$ が well-typed でない) | 前件 **(6′)** = **(R6-act)**($\tau/\rho_0$ 形)。$q$ を前件から追放し、$\mathrm{Sym}(\Lambda)$ 内の部分群の等式にする。**採択理由は §5.2.4** | 便 28 F7.3・P3・W1・W2 / 裁定 22 |
| **D2** | §5.2 | 前件は 6 本 | **(0)**(isolated / $\mathrm{Ih}_N$ が準同型)と **(5′)**(比較出力 (7.3))を明示。**未証明の所在が (6) から (5′) に移る** | 便 28 F7.4 |
| **D3** | §5.2 | 結論: 「$q_*[u^{-1}]_M$ が $H^1(G_K,\mu_e)$ で位数 $e$」 | 結論 **(R6-full)**: $\mathrm{ord}([u^{-1}]_M) = e$。固定体は安全形 $K\bigl((u^{-1})^{1/M}\bigr)$ | 便 28 F7.3 (7.4) |
| **D4** | §5.2 | 固定体を無条件に $K(u^{1/e})$ と書いた | $K(u^{1/e})$ と書けるのは $\gcd(e,M/e)=1$ (7.2) のときのみ。**3 行の証明つき**(§5.2.2 注 2) | 便 28 F7.3・W1 |
| **D5** | §5.2.3 | — | **【新規・縮約】**(1)(3)+shadow の定義から $\rho_0(\mathfrak F_0)\subseteq\tau(\mu_M)$ は**自動**。ゆえに **(6′) は「$\rho_0$ が忠実」の 1 ビットに落ちる**。$K^{(3)}$ では §4 の条件 4(【GAP-18a】)がそれ | 本稿発(検算 10/10) |
| **D6** | §5.2.5 | — | **【新規】射程条件と反証条件の事前登録**(第三例を取る前に固定・結果値を含まない) | 便 28 F8 step 1 |
| **D7** | 冒頭・§7 | 「群論部分($\Lambda$・$\mathfrak F_0$ 作用・$\Phi$ 単射)は二系統一致 = `cross-checked`」 | **項目別に射程分け**(§7.1 新表): $\Lambda$/$\mathfrak F_0$-作用は `cross-checked`、**$\Phi$ 単射(全 12 元)と Aut-融合は `gap18a.json` の独立確認範囲外**(紙上+node 単系統) | 便 28 F9・P5 / 裁定 22 |
| **D8** | §8 | ★教材 1–8 | **9・10・11 を追加**(便 28 W1・W2 + §7.1 発の 11) | 便 28 W1・W2 |
| **D9** | §9・§10 | 便 28 への論点 5 件 | 起草時のまま保存 + **便 28 の回答先を 1 行付記**。**§10 に便 29 への論点 5 件を新設** | — |
| **D10** | §3・§7 | 【GAP-20b】閉鎖(射程は本文中に限定済) | 閉鎖の**射程名を明記**: `ordered-passport-preserving normalization`。主張は不変(v2 の限定が既に正しい旨も便 28 F5.3 が確認) | 便 28 F5.3・P2 |
| **D11** | §4・§5.3・§6・§7 | — | **D1/D5 の波及注記のみ**: §4 に条件 4 と (6′) の関係、§5.3 に $\gcd(e,M/e)$ 行と (6′) の根拠行、§6 に記法の整合、§7 に **【GAP-Rcyc】** 行を追加。**新しい主張はない** | 本稿(型付けの帰結) |

> **不変**: §0 主定理の本文・§1 仮定リスト・§2 比較鎖の全論証・§3 $u$ の抽出・§4 残条件表・§6 観測列プロトコル・全検算値・全既存番号((K1)–(K4)・(P1)–(P7)・T#・【GAP-#】・★教材 1–8)。**v3 は定理を 1 ミリも動かさない。**

### 便 29 反映(v3.1・2026-07-27)

便 29(`sol/sol_reply_29_v3delta.md`)は v3 の型付けを **条件付き PASS** とした((R6-act) 採択・(7.5) 系降格・補題 R′・固定体安全形・【GAP-Rcyc】の所在はすべて PASS)。正本昇格の条件 P1–P3(+P4)を以下に反映する。**§0–§4 は再び不変。**

| # | 箇所 | v3 | v3.1 | 出所 |
|---|---|---|---|---|
| **E1(P1)** | §5.2.4 | 系 (7.5) の $\iota:\mu_e\to\mathfrak F_0$ が**未宣言**(「何らかの抽象同型」)— v2 の型穴が系側へ再侵入していた | **$j:=(\rho_0|_{\mathfrak F_0})^{-1}\circ\tau|_{\mu_M[e]}$ を正準同型として宣言**し、**$q$-free の系 (1.2) $\mathrm{Ih}_N|_{G_K}=j\circ\kappa_e$ を先に置く**(coprime 条件不要)。$\gcd(e,M/e)=1$ のときだけ $\iota:=j\circ q_e^{-1}$ (1.3) で (7.5) 形へ書き換え | 便 29 F1.2 (1.1)–(1.3)・W1 |
| **E2(P2)** | §5.2・§7 | 「$R^{\rm cyc}$」という 1 つの名前が、証明済みの形式命題・未証明の比較橋・研究プログラムの 3 つを指していた | **三札に分離**: **定理 $R^{\rm cyc}_{\rm formal}$**(paper-proof)/ **比較橋 $B_{\rm FC}$**(= 【GAP-Rcyc】・candidate/UNKNOWN)/ **$R^{\rm cyc}$ スキーマ**(設計図)。§7 の状態札表も対応 | 便 29 F4・★教材 3 |
| **E3(P3)** | §5.2.5 | 封印表 5 行(適用条件 / 反証条件 / 射程外 / $q$-版反証 / 縮約反証) | **五札に再構成**: FORMAL-IN / BRIDGE-IN / **BRIDGE-FAIL**(橋の真の falsifier)/ **BRIDGE-UNKNOWN**(scope-out ではない)/ SCHEMA-OUT。旧 $q$-版反証は **legacy regression test** へ改名し live な falsifier でないと明記 | 便 29 F5・W2 |
| **E4(P4)** | §5.2.2 注 2 | 「$\gcd(e,M/e)=1$ のときに限る」と書いたが、証明は**十分方向のみ** | **必要方向を追記**(便 29 F3.3 の $v=(a\xi)^r$ 構成)。$d:=\gcd(e,r)>1$ なら $\mathrm{ord}([v]_e)\mid e/d<e$ で次数が落ちる | 便 29 F3.3 |
| **E5(小)** | §5.3 | — | **Remark(奇数族の構造)**を追加: D1 の $K^{(n)}$ 族で $n$ 奇なら $M=2n$・$\mathfrak F_0\cong C_n$・$e=n$・$M/e=2$ ゆえ $\gcd(e,M/e)=1$ が**構造式から確定**(「見込み」ではない)。**$K^{(5)}=K^{(10)}$(Prop 3.4)で二重計上しない**注意つき | 便 29 F6 (6.1)・D1 (3.4)(4.12)/Thm 4.6/Prop 3.4 |
| **E6(小)** | §8・§10 | ★教材 1–11 | **★教材 9 に $\mu_e=\mu_M[e]$ の同一視が型穴を見えなくした機構を追記**・**★教材 12(便 29 ★教材 3)と 13(便 29 ★教材 1・補題 $R'$ が可換性に依存する旨)を追加**。§10 に便 29 の回答先を付記し §11 を新設 | 便 29 ★教材 1・3 |

> **v3.1 でも不変**: §0–§4 のすべて・§5.2.1 の前件 (0)–(6′)・§5.2.2 の証明・§5.2.3 の補題 R′・§6・§7.1 の射程分け・全検算値・全既存番号。**E1–E6 は名前と型と札の整備であり、数学的内容を足していない。**

---

## 反映一覧(便 27 の指摘に対する裁定)

| 便 27 | 内容 | 裁定 | 反映先 |
|---|---|---|---|
| **P1(必須)** | 補題 P(a): $H\cap\langle\bar x\rangle=1$ では自由性が出ない。$N_G(H)=H$ が要る | **全面採用。v1 は誤り** | §2.3 補題 P(a′)。**反例も自作**(§2.3 注・検算 T4e) |
| **P2(必須)** | 補題 P(d): 「$S_6$ 内で不動点なしの $C_3$ ゆえ同一」は偽 | **全面採用。v1 は誤り** | §2.3 補題 P(d′)。ただし**忠実性を使わない更に短い証明**に置換(§2.3 注 2) |
| **P3(必須)** | (K4): 「パラメータ表示が一意」は論証でない。生成元像の直接計算で修理 | **全面採用**。Sol の F4 計算を独立再現し、さらに**「12 個が Aut($G_3$) の元である」ことまで語評価で検査** | §1 (K4)・§2.5。**【GAP-K3a】閉鎖** |
| **P4(必須)** | 全射証明を kernel/quotient proof へ | **全面採用**。(K4) が全射段で不要になる依存関係の改善も採用 | §2.4 |
| **P5(推奨)** | 「18 個が一軌道・うち cent=1 が 12」は不可能 | **採用。v1(委嘱 20 由来)は誤り** | §2.2 (P3′)。**さらに新事実**: good 12 個は ordered passport で 6+6 の $G_3$-共役類に割れ、Aut が融合(§2.2 注) |
| **P6(推奨)** | 「原始 $M$ 乗根」→「faithful tangent action」 | **採用** | §2.2 (P6′) |
| **P7(推奨)** | 「両翼独立一致」→「二者一致・厳密な blind independence なし」 | **採用**(状態札の正直さの問題) | 冒頭・§3・§7 |
| **P8(推奨)** | Möbius の数え方 | **採用。v1 の一文は誤り**(全分岐を 0 に置くのは 4 通り、ordered passport を保つのが 2 通り) | §3。**私が計算した 2 通りはまさに後者だった** |
| **P9(推奨)** | $R^{\rm gen}$ を比較スキーマへ降格 | **採用**。定理の看板を外し、Sol の 6 前件を入れた $R^{\rm cyc}$ を**定理候補**として別立て | §5 |
| **F2** | $\mathrm{ord}([-4]_6)=3$ の短証明 | **採用**(主線に格上げ)。v1 の「$[2]_6$ の位数 6」は**正しいが不要**として注へ降格 | §2.3 (c′) |
| **F5** | FC-3 の前件明記 | **採用** | §2.1 |
| **F10** | 根基 2 を「観測列」+棄却規準に | **採用**(予測登録しない点は維持) | §6 |
| **W1–W7** | 警告 | **全採用**。W1・W2・W3 は本稿が実際に踏んだ穴なので★教材へ | §8 |

> **自認**: v1 の load-bearing な誤りは **2 件(P1・P2)**、記録の誤りが **2 件(P5・P8)**、論証欠落が **1 件(P3)**。いずれも Sol の指摘が正しい。とくに **W2(置換型は部分群を同定しない)は、私自身が委嘱 14 で立てた★教材「名前は不変量ではない」の同型物**であり、同じ穴を二度踏んだ。

---

## 0. 主定理

> ### 定理 K3
> $K^{(3)} = \ker\psi_3 \in \mathrm{NFI}_{PB_3}(B_3)$(D1 (3.1))とする。このとき
> $$ \boxed{\ \mathrm{Ih}_{K^{(3)}}:\ G_{\mathbb Q}\ \twoheadrightarrow\ \mathrm{GT}(K^{(3)})\ \cong\ \mathrm{Aff}(\mathbb Z/3)\times\mathcal Z_2\ \cong\ S_3\times C_2\quad(\text{位数 }12) $$
> は**全射**であり、$\ker(\Phi\circ\mathrm{Ih}_{K^{(3)}})$ の固定体は
> $$ \boxed{\ L_3\ =\ \mathbb Q\bigl(\zeta_{12},\ \sqrt[3]{2}\bigr),\qquad [L_3:\mathbb Q] = 12,\qquad \mathrm{Gal}(L_3/\mathbb Q)\ \cong\ S_3\times C_2\ } $$
> である。したがって $\mathrm{GT}(K^{(3)})$ の 12 元すべてが arithmetical、ゆえに genuine。

**体の同定**(便 27 F8.2 と一致): $u=-4$、$-1 = \zeta_{12}^6\in K^{\times6}$ より $K\bigl((u^{-1})^{1/6}\bigr) = K(2^{-1/3}) = K(\sqrt[3]2)$。$\sqrt[3]2\notin K$ より $[L_3:\mathbb Q] = 4\cdot3 = 12$。

**$\mathrm{Gal}$ の同定**: $L_3/K$ は $\mu_3\subset K$ ゆえ巡回 3 次で $\mathrm{Gal}(L_3/K)\cong\mu_3$。$\gcd(3,4)=1$ と Schur–Zassenhaus より $\mathrm{Gal}(L_3/\mathbb Q)\cong C_3\rtimes(\mathbb Z/12)^\times$。作用は円分指標の mod 3 還元で、$\{1,7\}$ 自明・$\{5,11\}$ 反転(検算 T9e)。作用核 $\{1,7\}\cong C_2$(固定体 $\mathbb Q(\zeta_3)$)を分離して
$$ \mathrm{Gal}(L_3/\mathbb Q)\cong C_3\rtimes(C_2\times C_2)\cong(C_3\rtimes C_2)\times C_2 = S_3\times C_2 $$
— **D1 §4 Thm 4.6 (4.23)($n_0=3,\alpha=0$)の $\mathrm{Aff}(\mathbb Z/3)\times\mathcal Z_2$ と同型** ✓。

---

## 1. 仮定リスト

| # | 内容 | 状態 |
|---|---|---|
| **(K1)** | $K^{(3)}$ は **isolated** | **source-closed**。D1 §4 Thm 4.3 末尾 逐語: "Furthermore, $K^{(n)}$ is an isolated object of the groupoid GTSh" |
| **(K2)** | $\lvert\mathrm{GT}(K^{(3)})\rvert = 12$、$\tilde\chi:\mathrm{GT}\to(\mathbb Z/12)^\times$ は**全射**で核 $\mathfrak F_0\cong C_3$ | **source-closed**。D1 Thm 4.3 (4.12)+κ (4.9) から $\mathcal X_3=\{0,2,3,5\}$、$k\bmod3$ で 12 元。$\tilde\chi(m,k)=2m+1$ が $\mathcal X_3\xrightarrow{\sim}(\mathbb Z/12)^\times$(検算 T8a) |
| **(K3‡)** | $\mathrm{Ih}$ の定める作用は正準 outer Galois 作用の $\hat F_2'$-正規化持ち上げ | **$A_5$ v4 §1.4.4 補題 I3‡ を import**(窓非依存・便 27 F5 で PASS 確認) |
| **(K4)** | $\Phi:\mathrm{GT}(K^{(3)})\to\mathrm{Aut}(G_3)$ が単射 | **紙上 PASS(§2.5・生成元像の直接計算)**。検算 T7b–T7g。**【GAP-K3a】閉鎖** |

> **⇒ 未閉鎖の数学的仮定はゼロ。** (K1)(K2) は正典、(K3‡) は $A_5$ で支払い済み、(K4) は本稿 §2.5 で閉じた。
> **★ さらに (K4) は全射性の証明には使わない**(§2.4・便 27 F8.1)。固定体の同定にのみ要る。

---

## 2. 比較鎖

### 2.1 窓非依存部品($A_5$ v4 §1 から import・便 27 F5 で全 PASS)

| 部品 | 内容 | 出所 |
|---|---|---|
| **補題 C** | 標準実経路 $p\subset(0,1)$ の Galois path cocycle は $[\hat F_2,\hat F_2]^{\rm top.cl.}$ に入る | v4 §1.4.2 |
| **補題 D0** | $C_{\hat F_2}(x) = \overline{\langle x\rangle}$ | v4 §1.4.3a |
| **補題 D・系 E** | $\hat F_2'$-正規化持ち上げの存在と一意性 ⇒ $\alpha^{\rm std}=\alpha^{\rm norm}$ | v4 §1.4.3b |
| **補題 I3‡** | $\alpha^{\rm Ih} = \alpha^{\rm norm}$ ⇒ $\alpha^{\rm Ih}=\alpha^{\rm std}$(= FC-2b) | v4 §1.4.4 |
| **FC-3** | $\Lambda := \{H\text{ の }\hat F_2\text{-共役}\}\xrightarrow{\sim}\mathrm{Fib}_{\vec{01}}(W_0)$、$G_{\mathbb Q}$-同型 | v4 §3.3 |
| **局所 Kummer** | 全分岐点で $\lambda = u\,s^M(1+O(s))$ ⇒ 接繊維の類は $[u^{-1}]\in K^\times/(K^\times)^M$ | v4 §3.5 |

> **【便 27 F5 による前件の明記】** FC-3 の「次数に依らない」は正しいが、次を要する:
> **(FC3-i)** $W_0$ が $\mathbb Q$ 上定義される、**(FC3-ii)** 幾何的連結、**(FC3-iii)** stabilizer 写像 $\mathrm{Fib}\to\Lambda$ が全単射。
> $K^{(3)}$ では (FC3-i)(FC3-ii) を (P5)(P7) が、**(FC3-iii) を $N_G(H)=H$ が**供給する(← これが §2.3(a′)と同じ前件)。
> **★ 非忠実な次数 6 表現でも import は壊れない**: FC-3 が使うのは $\hat F_2$ の有限推移集合と点 stabilizer であって、作用核の自明性ではない。

### 2.2 $K^{(3)}$ 固有部品

| 部品 | 内容 | 検算 |
|---|---|---|
| **(P1) 表現の選択** | **次数 6・非忠実**(monodromy $= G_3/\mathrm{core}$、位数 36 $=$ 6T9 $\cong S_3\times S_3$、核 $C_3$)。便 24 の B2/B5 FAIL は**次数 12 の最小忠実作用**についての判定であり、本稿の指数 6 部分群には及ばない(便 27 F6 P1 で PASS) | T3c |
| **(P2) B1–B5** | B1 PASS・**B2 PASS**($N_G(H)=H$、$\mathrm{Aut}(\text{dessin})=1$)・B3 PASS(全分岐)・B4 PASS($\mathfrak F_0\cong C_3$)・**B5 は「不要」ではなく「3-primary 核と 2-primary 円分商に分離した」**(便 27 F6 P2・§2.4 が厳密な代替) | T3b–T4d |
| **(P3′) 一意性(訂正)** | qualifying $H$ は 18 個。$\mathrm{Aut}(G_3)$-軌道は **12(=$N_G(H)=H$)と 6(=$N_G(H)/H\cong C_2$)の二つ**で、$N_G(\varphi H)/\varphi H\cong N_G(H)/H$ ゆえ**混ざらない**。v1 の「18 個で一軌道・うち cent=1 が 12」は**誤り**(便 27 P5) | T6a・T6b |
| **(P4) marked 同定** | **exact conjugator** $h = [6,1,5,4,2,3]$、$h\bar xh^{-1}=\sigma_1$, $h\bar yh^{-1}=\sigma_\infty$, $h\bar zh^{-1}=\sigma_0$。$h$ は $S_6$ 内で一意・三本目が独立検査 | 7/7 |
| **(P5) 分岐構造** | $F = t^2+(x-1)^2(4x-1)t+4x^6$、分岐 $\{0,-1,\infty\}$、型 $[6],[2^21^2],[6]$。$x=1/3$ は**節点**。$P_0=(0,0)$ で $F_t=-1\ne0$ ゆえ $x$ が uniformizer | 16/16 |
| **(P6′) 接方向 rigidification(文言訂正)** | 正: 「**標数 0 の有限自己同型群では、点 stabilizer の接直線への作用は忠実**。ゆえに非零接ベクトルまで固定する元は恒等元」。v1 の「原始 $M$ 乗根で作用」は合成数 $M$ で強すぎる(便 27 P6)。**本件は $\mathrm{Aut}=1$ ゆえ主証明から外す** | — |
| **(P7) 残留 descent なし** | 曲線と写像が $\mathbb Q$ 上・$\lambda=0$ 上は唯一の滑らかな点 $P_0$・$x$ は $\mathbb Q$-有理 uniformizer・$N_G(H)/H=1$・(P4) が actual marking を固定。**W5 に従い「$\mathrm{Aut}=1$ 単独では field of moduli $=\mathbb Q$ は出ない」ことを明記した上で、明示 $\mathbb Q$-モデル + exact marking が別途あることに依拠** | 16/16 |

> **★ (P3′)の新事実(v1 にも便 27 にも無い)**: $N_G(H)=H$ なる 12 個は **ordered passport で $6+6$ の $G_3$-共役類に割れる** — 一方は $(\bar x,\bar y,\bar z)$ の型が $(6,\,2^21^2,\,6)$、他方は $(6,\,6,\,2^21^2)$(検算 **T3c2**)。$\mathrm{Aut}(G_3)$ はこの二類を融合して一軌道にする(T6b)。
> **本定理の標的は前者**(型 $(6,2^21^2,6)$、$G_3$-共役類 1 つ、6 個)。`gap18a.json` の class #2/#4 はちょうどこの二類である。
> **これは委嘱 20 の★教材「passport は順序つきデータである」の第二の実例**であり、**(P4) の $h$ が DB 三つ組と $\lambda$ 割当を入れ替えて対応する理由**でもある: LMFDB のラベル `6T9-6_6_2.2.1.1-a` は ordered passport $(6,6,2^21^2)$ の正規化で、$\mu(\lambda)=1/(1-\lambda)$($0\mapsto1\mapsto\infty\mapsto0$)で本稿の正規化に移る。(P4) の $\bar x\mapsto\sigma_1,\bar y\mapsto\sigma_\infty,\bar z\mapsto\sigma_0$ はまさにこの入替えを実現しており、型は両側で整合する。
>
> **【v3・札の射程】** この 6+6 分裂と $\mathrm{Aut}(G_3)$-融合を直接支えるのは **node 系(T3c2・T6a・T6b)のみ**である。`gap18a.json` は 4 つの $G_3$-共役類を与えるが、**Aut-融合そのものの独立 GAP 証明書ではない**(便 28 F9)。§7.1 の札を参照。

### 2.3 補題 P(3-primary pushout)— **修理版**

> **補題 P.** $G := G_3$、$H$ を §2.2 の標的クラスの指数 6 部分群、$\Lambda := \{H\text{ の }G\text{-共役}\}$、$M := K^{(3)}_{\rm ord} = 6$、$K := \mathbb Q(\zeta_{12})$、$\mathfrak F_0 := \ker\tilde\chi\cong C_3$、$\rho_\Lambda:\mathrm{GT}(K^{(3)})\to\mathrm{Sym}(\Lambda)$。
>
> **(a′)【修理・便 27 F1】** $\langle\bar x\rangle\cong C_6$ は $\Lambda$ に**単純推移的**に作用する。
> **証明**: $\Lambda$ 上の共役作用における点 $H'\in\Lambda$ の stabilizer は $N_G(H')\cap\langle\bar x\rangle$ である(**coset stabilizer $H'$ ではない** — W1)。B2 より $N_G(H)=H$、共役でも $N_G(H^g)=H^g$。B3(全分岐)より**すべての $g$ で** $H^g\cap\langle\bar x\rangle=1$。ゆえに stabilizer は自明で作用は自由。$\lvert\langle\bar x\rangle\rvert = 6 = \lvert\Lambda\rvert$ ゆえ推移的。∎(検算 **T4a–T4d**)
>
> **(b)** FC-3 + 局所 Kummer 計算より、$G_K$ 上では $\chi\equiv1\ (\mathrm{mod}\ 12)$ ゆえ線形部が消え、$\Lambda$ 上の作用は $C_6$-torsor の**平行移動**のみ。その平行移動は Kummer 指標
> $$ \kappa_{u^{-1}}:G_K\longrightarrow\mu_6 $$
> で与えられ、$\mu_6\subset K$ ゆえ $\lvert\mathrm{im}\,\kappa_{u^{-1}}\rvert = \mathrm{ord}\bigl([u^{-1}]_6\bigr)$。
> (便 27 F2 の文言訂正を採用: 「像が Kummer 類で生成される」ではなく「**$\kappa_{u^{-1}}$ の表す類が $[u^{-1}]_6\in K^\times/K^{\times6}$ である**」。)
>
> **(c′)【便 27 F2 の短証明を主線に】** $u = -4$。$-1 = \zeta_{12}^6\in K^{\times6}$ ゆえ $[-4]_6 = [4]_6$。$[4]_6^3 = [2^6]_6 = 1$ より位数は 3 の約数。もし $[4]_6=1$ なら $a^6=4$ なる $a\in K$ があり $a^3=\pm2$、ゆえに $\sqrt[3]2\in K$ — しかし $[\mathbb Q(\sqrt[3]2):\mathbb Q] = 3\nmid[K:\mathbb Q]=4$ で矛盾。ゆえに
> $$ \boxed{\ \mathrm{ord}\bigl([u^{-1}]_6\bigr) = \mathrm{ord}\bigl([-4]_6\bigr) = 3.\ } $$
> さらに $-4 = (2i)^2$、$i=\zeta_{12}^3\in K$ ゆえ 2-primary 成分は自明。**したがって $\rho_\Lambda(\mathrm{Ih}(G_K))$ の位数はちょうど 3**(余分な $C_2$ を含まない)。(検算 T9a–T9d)
>
> **(d′)【修理・便 27 F3.2】** $G_K = \ker(\chi\bmod12)$ かつ $\tilde\chi\circ\mathrm{Ih}=\chi_{12}$ より
> $$ \mathrm{Ih}(G_K)\ \le\ \mathfrak F_0 . $$
> (c′) より $\lvert\rho_\Lambda(\mathrm{Ih}(G_K))\rvert = 3$、$\rho_\Lambda(\mathrm{Ih}(G_K))$ は $\mathrm{Ih}(G_K)$ の商だから $\lvert\mathrm{Ih}(G_K)\rvert\ge3$。一方 $\lvert\mathfrak F_0\rvert = 3$(K2)。ゆえに
> $$ \boxed{\ \mathrm{Ih}_{K^{(3)}}(G_K) = \mathfrak F_0\cong C_3 .\ } $$ ∎

> **注 1(v1 の誤りの所在)**: v1 (a) は「$H\cap\langle\bar x\rangle=1$ ⇒ 自由」と書いた。これは**共役部分群の stabilizer と coset の stabilizer の取り違え**であり、飛躍である。実際、**$H\cap\langle\bar x\rangle=1$ でも $\mathrm{Stab}_{\langle\bar x\rangle}(H)$ が位数 2 になる $H$ が $G_3$ の中に実在する**(qualifying だが $N_G(H)/H\cong C_2$ の側・$\lvert\Lambda\rvert=3$)。**検算 T4e でその反例を実際に構成した** — 便 27 の指摘は抽象的な懸念ではなく、この設定に実在する落とし穴だった。
>
> **注 2(便 27 F3.2 より更に短くできる)**: Sol の (3.3) は $\rho_\Lambda|_{\mathfrak F_0}$ の忠実性(【GAP-18a】)を使って $\lvert\rho_\Lambda(\mathfrak F_0)\rvert=3$ を出し、像の一致から $\mathrm{Ih}(G_K)=\mathfrak F_0$ を導く。しかし上の (d′) のとおり、**包含 $\mathrm{Ih}(G_K)\le\mathfrak F_0$ と $\lvert\mathfrak F_0\rvert=3$ と $\lvert\rho_\Lambda(\mathrm{Ih}(G_K))\rvert=3$ だけで閉じ、忠実性は要らない**。忠実性が本当に load-bearing なのは **§2.6 の固定体の同定**である。依存関係を正確にするため本稿はこの形を採る(便 27 の結論は変わらない)。**便 28 F2 が同意し、依存表を明示した**(全射性・$\mathrm{Ih}(G_K)=\mathfrak F_0$ には不要 / 固定体同定と「$\Lambda$ 上自明 ⇒ shadow 自明」には必要)。
>
> **注 3(v1 の「$[2]_6$ の位数は 6」)**: 正しい($[2]^2=[4]$ が位数 3、$[2]^3=[8]\ne1$ — さもなくば $a^2 = 2\zeta_3^j$ となり、$\sqrt{\zeta_3}=\pm\zeta_6\in K$ ゆえ $\sqrt2\in K$ を要して矛盾;$\sqrt2\notin\mathbb Q(i,\sqrt3)$)。**しかし定理には不要**(便 27 F2)。$C_6$-torsor が「本当に $C_6$」であることの傍証として注に残す(検算 T9f)。
>
> **注 4(便 25 F5-3・generator の向き)**: actual marking の逆向き規約は $[u]\leftrightarrow[u]^{-1}$ を起こしうるが、**「位数 3 か自明か」の判定も体 $L_3$ も反転不変**。無害。

### 2.4 主定理(全射性)の証明 —【便 27 F3.3 の kernel/quotient proof】

$T := \mathrm{GT}(K^{(3)})$、$A := \mathrm{Ih}_{K^{(3)}}(G_{\mathbb Q})\le T$ と置く。

1. **(K1)** より $\bar K^{(3)}$ は $G_{\mathbb Q}$-安定 ⇒ $\beta:G_{\mathbb Q}\to\mathrm{Aut}(G_3)$ が定義され、$\beta_\gamma(\bar x)=\bar x^{\chi(\gamma)}$。
2. **(K3‡)** + 補題 C/D0/D/系 E より $\alpha^{\rm Ih}=\alpha^{\rm std}$(FC-2b)⇒ $\beta = \Phi\circ\mathrm{Ih}_{K^{(3)}}$。
3. **完全列**(K2): $1\to\mathfrak F_0\cong C_3\to T\xrightarrow{\tilde\chi}(\mathbb Z/12)^\times\cong C_2^2\to1$、かつ $\tilde\chi\circ\mathrm{Ih}=\chi_{12}$。円分指標の全射性より
 $$ \tilde\chi(A) = (\mathbb Z/12)^\times,\qquad \lvert\tilde\chi(A)\rvert = 4. $$
4. **補題 P(d′)** より $A\cap\mathfrak F_0 = \mathrm{Ih}(G_K) = \mathfrak F_0$、$\lvert A\cap\mathfrak F_0\rvert = 3$。
5. $A\cap\mathfrak F_0 = \ker(\tilde\chi|_A)$ ゆえ
 $$ \lvert A\rvert = \lvert A\cap\mathfrak F_0\rvert\cdot\lvert\tilde\chi(A)\rvert = 3\cdot4 = 12 = \lvert T\rvert \quad\Longrightarrow\quad \boxed{A = T.} $$ ∎
6. arithmetical ⇒ genuine は $G_{\mathbb Q}\hookrightarrow\widehat{GT}$ から(2405 §1.3.1)。

> **★ この証明は (K4) を使わない**(便 27 F8.1)。**また $C_6$-torsor 全体を推移的にする必要もない** — 必要なのは核 $C_3$ を埋めることだけで、商 $C_2^2$ は独立に円分指標が埋める(W6)。これが「合成数 $M=6$ で B5 が破れても橋が架かる」ことの正確な意味である。

### 2.5 (K4) $\Phi$ の単射性 —【便 27 F4 の生成元像計算・独立再現+強化】

D1 (4.12): $\mathrm{GT}(K^{(3)}) = \{(m, f_{m,k})\}$、$f_{m,k} = (r^{2k},r^{-2k},r^{\kappa(m)})$、$m\in\mathcal X_3=\{0,2,3,5\}$、$k\bmod3$、$u_m := 2m+1$、$\kappa$ は (4.9)。marking は (3.6) の $\bar x=(r,s,s)$、$\bar y=(rs,r,rs)$。$u_m$ は奇数なので $s^{u_m}=s$、$(rs)^{u_m}=rs$ に注意して

$$ \Phi_{m,k}(\bar x) = \bar x^{u_m} = (r^{u_m},\,s,\,s),\qquad \Phi_{m,k}(\bar y) = f_{m,k}^{-1}\bar y^{u_m}f_{m,k} = \bigl(r^{1-4k}s,\ r^{u_m},\ r^{1-2\kappa(m)}s\bigr). $$

指数は $\bmod\ 3$($r^3=1$)。charming $m$ で:

| $m$ | $u_m\bmod3$ | $\kappa(m)\bmod3$ | 第 3 成分 $r^{1-2\kappa(m)}s$ |
|---|---|---|---|
| 0 | 1 | 0 | $rs$ |
| 2 | 2 | 1 | $r^2s$ |
| 3 | 1 | 1 | $r^2s$ |
| 5 | 2 | 0 | $rs$ |

$\bigl(u_m\bmod3,\ \text{第 3 成分}\bigr)$ の 4 組はすべて相異なるので $m$ が一意に決まる。次に第 1 成分 $r^{1-4k}s = r^{1-k}s$ は $k=0,1,2$ に対し $rs,\,s,\,r^2s$ と相異なるので $k\bmod3$ も一意。$\bar x,\bar y$ は $G_3$ を生成するから、生成元像が一致する 2 つの自己同型は等しい。ゆえに
$$ \boxed{\ \Phi:\mathrm{GT}(K^{(3)})\hookrightarrow\mathrm{Aut}(G_3)\ \text{は単射}.\ } $$
**【GAP-K3a】閉鎖。**(検算 **T7d–T7g** が上式と表を独立再現。)

> **強化(便 27 に無い)**: 検算 **T7b** は、12 個の $\Phi_{m,k}$ が**実際に $G_3$ の自己同型である**ことを、BFS 語表現による全 108 元への評価と準同型性の悉皆検査で確認した(全単射性も込み)。便 27 F4 は $(m,k)\mapsto$(生成元像)の単射性のみを見ており、「そもそも $\Phi_{m,k}\in\mathrm{Aut}(G_3)$ か」は前提にしている。**逆写像の向きの穴(W3 の裏面)をここで塞いだ。**(便 28 F3: 数学的主線には不要だが defensive check として有益・過剰ではない、と検収。)
>
> **規約の頑健性**: $\Phi(\bar y) = f\bar y^{u}f^{-1}$ という逆向きの規約でも、$k\mapsto -k$ の置換になるだけで単射性の論証は不変。
>
> **【v3・札の射程】** この単射性(全 12 元)を支える証拠は **紙上証明 + node 検算 T7b–T7g** の 2 本であり、**`gap18a.json` は 12 個の誘導自己同型の相異性を明示検査していない**(便 28 F9)。したがって**本項目単独では `cross-checked` と名乗らない**。§7.1 参照。

### 2.6 固定体の同定

(K4) より $\ker(\Phi\circ\mathrm{Ih}) = \ker(\mathrm{Ih}_{K^{(3)}})$。$\gamma\in G_{\mathbb Q}$ に対し

$$ \mathrm{Ih}(\gamma)=1 \iff \underbrace{\tilde\chi(\mathrm{Ih}(\gamma))=1}_{\chi(\gamma)\equiv1\ (12)} \ \text{かつ}\ \underbrace{\rho_\Lambda(\mathrm{Ih}(\gamma))=1}_{\kappa_{u^{-1}}(\gamma)=1} $$

— ここで「$\Rightarrow$」は自明、「$\Leftarrow$」に **$\rho_\Lambda|_{\mathfrak F_0}$ の忠実性(【GAP-18a】・検算 T8d)が load-bearing** である(注 2)。第 1 条件は $\gamma$ が $K=\mathbb Q(\zeta_{12})$ を固定すること、第 2 条件は $\gamma$ が $K\bigl((u^{-1})^{1/6}\bigr)$ を固定すること。$-1\in K^{\times6}$、$u=-4$ より $K\bigl((u^{-1})^{1/6}\bigr) = K(2^{-1/3}) = K(\sqrt[3]2)$。ゆえに
$$ \mathrm{Fix}\,\ker(\Phi\circ\mathrm{Ih}) = L_3 = \mathbb Q(\zeta_{12},\sqrt[3]2). $$
$\mathrm{Gal}$ の同定は §0。∎

---

## 3. $u$ の抽出 — 両翼併記(**状態札を便 27 P7 に従い訂正**)

| | **Opus(委嘱 21)** | **Sol(便 25)** |
|---|---|---|
| 経路 | 平面モデルの**分岐構造を自前確定**(臨界方程式 $(3x-1)^2(2x^2-2x+1)$・節点 $x=1/3$・$t=-1$ の 2 根)→ $\lambda=-t$ → 冪級数 | $P_0$ での局所 implicit 展開 |
| 主係数 | $t = 4x^6+24x^7+\cdots$ ⇒ **$u=-4$** | **$u=-4$** |
| 基礎体 | $\mathbb Q(\zeta_{12})$(**事前固定**・W149) | $\mathbb Q(\zeta_{12})$(**事前固定**) |
| 類 | $[u]_3=[2^2]\ne1$ | $[u^{-1}]_3 = [u]_3^{-1}\ne1$(**逆元表記・判定同値**) |
| 正規化不変性 | $\lambda=\infty$ 側も展開: $u' = -\frac{256}{729} = -\frac{2^8}{3^6}$、$[u']_3 = [2^{8}3^{-6}]_3 = [2^2]$ ✓ | — |
| 判定 | **飽和側** | **飽和側** |

> **★ 独立性の状態札(便 27 P7・訂正)**: 便 25 は計算後とはいえ Opus checker のヘッダ内の $u$ と mod 3 判定を見たと**自己申告**している。したがって本稿は
> $$ \boxed{\text{「二者の紙上経路が一致(便 25 が独立性汚染を自己申告)」\ ;\ 厳密な blind independence ではない}} $$
> と記す。v1 の「両翼独立一致」は**取り下げる**。数値結論には影響しない。

> **【便 27 P8・Möbius の数え方の訂正】** 3 分岐点の正規化は 6 通り。うち
> - **全分岐点($[6]$ 型)を $0$ に置くのは 4 通り**(v1 の「2 通りで尽きる」は誤り)、
> - そのうち **ordered passport $(6,\,2^21^2,\,6)$ を保つのは 2 通り**(恒等と、$\lambda=0\leftrightarrow\lambda=\infty$ を入れ替え $\lambda=1$ を固定する $\mu(\lambda)=1/\lambda$)、
> - 残る 2 通りは passport 順を $(6,6,2^21^2)$ に変える(LMFDB のラベル順はこちら)、
> - 最後の 2 通りは $[2^21^2]$ 点を $0$ に置くので**全分岐でなく $u$ の定義域外**。
>
> **本定理が固定した marking に必要なのは 2 番目の 2 通りで、私が計算したのはちょうどその 2 通りだった**($t=0$ と $t=\infty$)。両方で $[u]_3=[2^2]$。**⇒【GAP-20b】閉鎖**(結論は v1 のまま、説明を限定した)。
> **便 28 F5.3・P2 の限定を採用**: 閉鎖の射程は **`ordered-passport-preserving normalization`** であり、「全 $S_3$-正規化を数値的に走査した」という広い札にはしない。

---

## 4. 残条件の和集合

| # | 条件 | Opus | 便 25 | 便 27 | 現状 |
|---|---|---|---|---|---|
| 1 | isolated | C1 | 1 | — | **閉**(正典 Thm 4.3) |
| 2 | $\mathfrak F_0\cong C_3$・$\tilde\chi$ 円分 | C2 | 2 | — | **閉**(正典 Thm 4.3) |
| 3 | marked identification | C5 | 3(Sol 未計算) | P4 PASS | **閉**(exact conjugator (P4)) |
| 4 | $\Lambda$ 上で $\mathfrak F_0$ 忠実 | C4 | 4 | F3.2/F8.2 | **閉**(【GAP-18a】・T8d で二系統一致) |
| 5 | 補題 C/D0/D/E/I3‡ | C3 | 5 | F5 PASS | **閉**($A_5$ v4・窓非依存) |
| 5b | **FC-3 の前件**(ℚ-model・幾何連結・stabilizer 全単射) | — | — | **F5 で新規要求** | **閉**(§2.1・(P5)(P7)+$N_G(H)=H$) |
| 6 | 残留 descent なし | C6 | F5 | P7 PASS | **閉** |
| 7 | 3-primary pushout | C7 | F5-2 | **F1 で (a) 差戻し** | **閉**(§2.3 修理版) |
| 8 | generator の向き | — | F5-3 | — | **無害** |
| 9 | $\Phi$ の単射性 | — | — | **F4 で理由差戻し** | **閉**(§2.5・【GAP-K3a】) |

> **⇒ 未閉鎖の数学的条件はゼロ。** 残るのは (i) Lean 検証、(ii) $u$ の第三系統(【GAP-K3c】)、(iii) 平面モデルと LMFDB 54.b3 の同一性(【GAP-K3b】・**依存していない**)のみ。
> **【v3】** 条件 4(「$\Lambda$ 上で $\mathfrak F_0$ 忠実」)は、§5.2.3 の縮約により **$R^{\rm cyc}$ の前件 (6′) がこの窓で要求する全内容**でもある(残りは自動)。

---

## 5. 族の設計図(**定理ではない** — 便 27 F9/P9 に従い格下げ)

> **【格下げの理由】** v1 §5 の「定理 $R^{\rm gen}$」は $[u]$ の「$\mathfrak F_0$-成分」という語を**未定義のまま**使っていた。$\mathfrak F_0$ が $\Lambda$ 上忠実というだけでは、その像が regular $C_M$ の平行移動部分群に入るとも $\mathfrak F_0$ が巡回とも限らない。**補題 P(d) が踏んだ穴(W2)をそのまま一般定理へ持ち込んでいた**。定理の看板を外す。

### 5.1 比較スキーマ(2 事例の共通形)

| 段 | 内容 |
|---|---|
| **S1** | 窓 $N$ を固定し、$P = F_2/\bar N$、marking $(X,Y,Z)$、$M := N_{\rm ord}$、$K := \mathbb Q(\zeta_{2M})$ |
| **S2** | $\mathrm{GT}(N)$ の完全列 $1\to\mathfrak F_0\to\mathrm{GT}(N)\xrightarrow{\tilde\chi}(\mathbb Z/2M)^\times\to1$ を正典から読む |
| **S3** | 部分群 $H\le P$ を選び、dessin $W_0$ と $\Lambda$ を作る(窓ごとの設計判断) |
| **S4** | 窓非依存の絶対較正(補題 C/D0/D/E/I3‡)を import して $\alpha^{\rm Ih}=\alpha^{\rm std}$ |
| **S5** | 全分岐 cusp で $\lambda = u\,s^M(1+O(s))$ から $u$ を抽出 |
| **S6** | $\mathfrak F_0$ 部分を Kummer 類で埋め、$(\mathbb Z/2M)^\times$ 部分を円分指標で埋め、核・商で位数を突き合わせる |

**★ 最大の利得**: 最も高価な S4 は $\lambda$-線だけの命題で**窓に一切依存しない**。$A_5$ で一度支払えば $K^{(3)}$ では無料(便 25 F5 も同じ整理・独立一致)。

### 5.2 $R^{\rm cyc}$(**定理候補・未証明**)— 便 27 F9 の 6 前件を採用【v3: 前件 (6) を (6′) に型付け】

> **【v3 の変更点】** v2 の前件 **(6)**(「指定された pushout $q:\mu_M\twoheadrightarrow\mu_e\xrightarrow{\sim}\mathfrak F_0$ が $\mathfrak F_0$ の $\Lambda$ 上の作用と一致する」)を、**便 28 F7.3 の $\tau/\rho_0$ 形 (R6-act)** に置き換える。**採択理由は §5.2.4**(cocycle 等式 (7.5) を採らない理由も同節)。**定理 K3(§0–§4)・検算値・既存番号は一切変わらない。**
> **裁定 22 の中庸原則を遵守**: 二例からの一般条件の固定は行わず、**第三例で有限計算により判定できる最小の型**に留める。

#### 5.2.−1 【v3.1・便 29 P2】三札の分離 — 何が証明済みで何が未証明か

> **問題**(便 29 F4): v3 では「$R^{\rm cyc}$」という 1 つの名前が、**(i) $(5')$ を前件に含む証明済みの形式命題**・**(ii) $(4)(5)\Rightarrow(5')$ という未証明の比較橋**・**(iii) 両者を接続する研究プログラム**の 3 つを同時に指していた。このままでは「定理候補・未証明」と「補題 R 自体は証明済み」が同じ札の下に並び、**第三例が何を falsify したのかを後から選べてしまう**(便 29 ★教材 3)。以後、次の三札を厳密に使い分ける。

| 名前 | 内容 | 状態札 |
|---|---|---|
| **定理 $R^{\rm cyc}_{\rm formal}$** | 前件 $(0)(1)(2)(3)(5')(6')$ から結論 **(R6-full)** と固定体 **(7.4)**(便 29 の番号では (3.4))を導く**有限群論+Kummer 理論の命題**(§5.2.1–§5.2.2) | **`paper-proof`**(本稿 §5.2.2 の証明・便 29 F3.1/F3.2 で PASS。**Lean `verified` ではない**) |
| **比較橋 $B_{\rm FC}$**(= 【GAP-Rcyc】) | 精密化した $(4)(5)$(明示 $\mathbb Q$-モデル・$\mathbb Q$-有理な全分岐 cusp・局所助変数・actual marking・FC-2b/FC-3 比較規約)から **$(5')$ = (7.3)** を導く段 | **`candidate / UNKNOWN`**。2 例では個別に構成したが、**一般証明はない** |
| **$R^{\rm cyc}$ スキーマ** | $B_{\rm FC}$ と $R^{\rm cyc}_{\rm formal}$ を接続する設計図(§5.1 の S1–S6 + §5.2 の型) | **設計図**(定理でも定理候補でもない。窓ごとに両札を別々に検査する運用規約) |

> **★ この分離が効く理由**: **$(5')$ を前件に置いた瞬間、その先の結論試験は「未証明の橋の試験」ではなく「形式系の整合性試験」になる**(便 29 F5.2)。すなわち $R^{\rm cyc}_{\rm formal}$ の前件を全部確認したうえで結論が破れたなら、それは橋の反証ではなく**私の証明か札の誤り**である。橋を試すには $(5')$ を**前件から外して**、$(4)(5)$ だけを封印しなければならない。これを §5.2.5 の五札で実装する。

#### 5.2.0 型(記号の宣言)

| 記号 | 型 | 定義 |
|---|---|---|
| $P$ | 有限群 | $F_2/\bar N$ |
| $X$ | $P$ の元 | marking の第 1 成分。$M := \mathrm{ord}(X)$ |
| $K$ | 体 | $\mathbb Q(\zeta_{2M})$ |
| $H$ | $P$ の部分群 | 窓ごとの設計判断(S3) |
| $\Lambda$ | 有限集合 | $H$ の $P$-共役類。$P$ は共役で作用 |
| $\tau$ | $\mu_M\to\mathrm{Sym}(\Lambda)$ | $\zeta_M\longmapsto\bigl(H'\mapsto XH'X^{-1}\bigr)$、$\zeta_M^j\mapsto(\,\cdot\,)^j$。**単射性と regular 性は前件 (3) が与える** |
| $\mu_M[e]$ | $\mu_M\le$ の部分群 | 位数 $e$ の唯一の部分群 $=\langle\zeta_M^{M/e}\rangle$($e\mid M$) |
| $\Phi$ | $\mathrm{GT}(N)\to\mathrm{Aut}(P)$ | shadow $(m,f)\mapsto\bigl(X\mapsto X^{2m+1},\ Y\mapsto f^{-1}Y^{2m+1}f\bigr)$(2401 の定義) |
| $\rho_0$ | $\mathfrak F_0\to\mathrm{Sym}(\Lambda)$ | $\Phi|_{\mathfrak F_0}$ の $\Lambda$ 上への制限 |
| $\kappa_{u^{-1}}$ | $G_K\to\mu_M$ | 局所 Kummer 指標($\mu_M\subset K$ ゆえ指標) |

> **$\tau$ の $\mu_M$ 側の同定**: $\langle X\rangle\xrightarrow{\sim}\mu_M$ は「全分岐 cusp の $\mathbb Q$-有理局所助変数 $s$ に対する $s^{1/M}\mapsto\zeta_M\,s^{1/M}$」で与える(§2.1 局所 Kummer)。生成元の向きの曖昧さ(注 4)は判定にも固定体にも影響しない。

#### 5.2.1 前件(型付き)— **定理 $R^{\rm cyc}_{\rm formal}$ の前件**

> **定理 $R^{\rm cyc}_{\rm formal}$ の前件(v3 型付け版・v3.1 で名前のみ確定).** 次を仮定する。
>
> **(0)【新・便 28 F7.4】** $N$ が isolated である、あるいは少なくとも $\mathrm{Ih}_N:G_{\mathbb Q}\to\mathrm{GT}(N)$ が**準同型として定義済み**である。
> **(1)** $1\to\mathfrak F_0\to\mathrm{GT}(N)\xrightarrow{\tilde\chi}(\mathbb Z/2M)^\times\to1$ が完全、かつ $\tilde\chi\circ\mathrm{Ih}_N=\chi_{2M}$。
> **(2)** $\mathfrak F_0\cong C_e$、$e\mid M$。
> **(3)** $\mathrm{ord}(X) = \lvert\Lambda\rvert = M$ で $\langle X\rangle$ が $\Lambda$ に単純推移(⇐ $N_P(H)=H$ + 全分岐)。**⇒ $\tau$ は単射かつ regular。**
> **(4)** 明示 $\mathbb Q$-モデル・$\mathbb Q$-有理な全分岐 cusp・actual marked identification。**$\mathrm{Aut}=1$ だけでは field of moduli $=\mathbb Q$ は出ない**(W5)。
> **(5)** FC-2b/FC-3 による actual Galois 作用と接繊維の比較。
> **(5′)【新・比較出力の明示】** (4)(5) の帰結として、$G_K$ 上で
> $$ \rho_0\bigl(\mathrm{Ih}_N(\gamma)\bigr)\ =\ \tau\bigl(\kappa_{u^{-1}}(\gamma)\bigr)\qquad(\forall\gamma\in G_K) \tag{7.3} $$
> が成り立つ。
> **(6′)【差替え・(R6-act)】** $\Lambda$ は $\Phi(\mathfrak F_0)$-安定($\rho_0$ が定義されるための最低条件)で、かつ
> $$ \boxed{\ \rho_0\ \text{は忠実},\qquad \rho_0(\mathfrak F_0)\ =\ \tau\bigl(\mu_M[e]\bigr).\ } \tag{R6-act} $$

> **★ 何が変わったか**: (6) は「$q$ という**外から持ち込んだ写像**が『作用と一致』する」という、可換図の書けない語だった(便 28 W2)。(6′) は **$\mathrm{Sym}(\Lambda)$ の中の 2 つの部分群の等式**であり、窓の群論データ($P,H,X,\Phi$)だけで**有限計算で決着する**。$q$ は前件から完全に消える。

#### 5.2.2 群論段の帰結(補題 R = **定理 $R^{\rm cyc}_{\rm formal}$**)

> **定理 $R^{\rm cyc}_{\rm formal}$(= 補題 R).** (0)(1)(2)(3)(5′)(6′) の下で
> $$ \boxed{\ \mathrm{Ih}_N\ \text{が全射}\iff \mathrm{ord}\bigl([u^{-1}]_M\bigr) = e\ } \tag{R6-full} $$
> であり、そのとき(実は全射でなくとも)
> $$ \boxed{\ \mathrm{Fix}\bigl(\ker\mathrm{Ih}_N\bigr)\ =\ K\bigl((u^{-1})^{1/M}\bigr).\ } \tag{7.4} $$

**証明**(§2.3(d′)+§2.4+§2.6 の逐語的抽象化 — 新しい入力はない)。

1. (1) より $\gamma\in G_{\mathbb Q}$ について $\mathrm{Ih}_N(\gamma)\in\mathfrak F_0\iff\chi_{2M}(\gamma)=1\iff\gamma\in G_K$。ゆえに $A\cap\mathfrak F_0 = \mathrm{Ih}_N(G_K)$($A:=\mathrm{Ih}_N(G_{\mathbb Q})$)。
2. (6′) の忠実性と (5′) より $\lvert\mathrm{Ih}_N(G_K)\rvert = \lvert\rho_0(\mathrm{Ih}_N(G_K))\rvert = \lvert\tau(\kappa_{u^{-1}}(G_K))\rvert = \lvert\kappa_{u^{-1}}(G_K)\rvert = \mathrm{ord}([u^{-1}]_M)$($\tau$ 単射・Kummer 理論)。
3. (6′) の像の等式と (5′) より $\kappa_{u^{-1}}(G_K)\subseteq\mu_M[e]$、すなわち $\mathrm{ord}([u^{-1}]_M)\mid e$。
4. (1) の完全列と円分指標の全射性から $\lvert A\rvert = \lvert A\cap\mathfrak F_0\rvert\cdot\lvert(\mathbb Z/2M)^\times\rvert$。ゆえに $A = \mathrm{GT}(N)\iff\lvert\mathrm{Ih}_N(G_K)\rvert = e\iff\mathrm{ord}([u^{-1}]_M) = e$。これが (R6-full)。
5. 固定体: $\mathrm{Ih}_N(\gamma)=1$ なら 1 より $\gamma\in G_K$、(5′) と $\tau$ の単射性より $\kappa_{u^{-1}}(\gamma)=1$。逆に $\gamma\in G_K$ かつ $\kappa_{u^{-1}}(\gamma)=1$ なら $\rho_0(\mathrm{Ih}_N(\gamma))=1$ で、(6′) の忠実性より $\mathrm{Ih}_N(\gamma)=1$。ゆえに $\ker\mathrm{Ih}_N = G_K\cap\ker\kappa_{u^{-1}} = G_{K((u^{-1})^{1/M})}$。∎

> **状態(重要・v3.1 で三札に整理)**: **定理 $R^{\rm cyc}_{\rm formal}$ は証明済み(`paper-proof`)**である — が、それは (5′) を**前件に置いた**からにすぎない。**$R^{\rm cyc}$ スキーマ全体が未完であることは v2 から変わらない。** 変わったのは**未証明の所在**である:
> $$ \boxed{\ \text{未証明部} = \text{比較橋 } B_{\rm FC}\ =\ \text{「(4)(5) から (5′) を一般に導く段」}\ } $$
> であって、v2 が書いていた「(6) の $q$ を窓データから導く条件」ではない(便 29 F4 が同意)。2 事例では (5′) を個別に構成した(§2.3(b) と $A_5$ v4 §3.5)。**一般の窓で $B_{\rm FC}$ を示すことが、族の定理へ残された仕事である。**
> **札の使い分け**: 「$R^{\rm cyc}$ を証明した」とは**書かない**。書けるのは「$R^{\rm cyc}_{\rm formal}$ を証明し、$B_{\rm FC}$ を UNKNOWN として分離した」までである(§5.2.−1)。

> **注 1(前件の依存関係)**: (6′) の**忠実性**は補題 R の 2・5 で、**像の等式**は 3 で使う。(6′) を落とすと 2 も 5 も出ない — v2 §2.3 注 2 の「忠実性は $\mathrm{Ih}(G_K)=\mathfrak F_0$ には不要」は、$K^{(3)}$ では位数 3 の直接計算 (c′) が代替したためであって、一般形では代替がない。**依存関係が窓ごとに違うこと自体を型が可視化した**。
>
> **注 2(v2 の $K(u^{1/e})$ はいつ正しいか)【便 28 F7.3 (7.2)・W1】**: 安全形は (7.4) の $K\bigl((u^{-1})^{1/M}\bigr)$ である。v2 が書いた $K(u^{1/e})$ と一致するのは
> $$ \boxed{\gcd(e,\ M/e) = 1} \tag{7.2} $$
> のときに限る。
> **証明(十分方向 $\gcd=1\Rightarrow$ 一致)**: $v:=u^{-1}$、$r:=M/e$、$\mathrm{ord}([v]_M)=e$ とする。$\mu_M\subset K$ より $[K(v^{1/M}):K] = \mathrm{ord}([v]_M) = e$。次に $\mathrm{ord}([v]_e)=e$ を示す: $d:=\mathrm{ord}([v]_e)$ とすると $d\mid e$ かつ $v^d\in K^{\times e}$、ゆえに $v^{dr}\in K^{\times M}$ で $e = \mathrm{ord}([v]_M)\mid dr$。(7.2) より $e\mid d$、よって $d=e$。したがって $[K(v^{1/e}):K]=e$。他方 $\bigl((v^{1/M})^{r}\bigr)^e = v$ なので $K(v^{1/e})\subseteq K(v^{1/M})$($\mu_e\subset K$ ゆえ $e$ 乗根の取り方に依らない)。次数が等しいので等号。最後に $\alpha^e = u^{-1}\iff(\alpha^{-1})^e=u$ より $K(v^{1/e}) = K(u^{1/e})$。∎
>
> **【v3.1・便 29 P4/F3.3】必要方向($\gcd>1\Rightarrow$ 不一致)**: 同じ設定で $d:=\gcd(e,r)>1$ とする。$\mathrm{ord}([v]_M)=e$ より $v^e = a^M = (a^r)^e$ なる $a\in K^\times$ があり、$v/a^r\in\mu_e$。**$\mu_M\to\mu_e,\ \xi\mapsto\xi^r$ は全射**(像は $\langle\zeta_M^r\rangle$、位数 $M/\gcd(M,r) = e$、巡回群 $\mu_M$ の位数 $e$ の部分群は $\mu_e$ ただ一つ)だから、ある $\xi\in\mu_M$ で $\xi^r = v/a^r$、すなわち
> $$ v = (a\xi)^r. \tag{7.2$'$} $$
> よって $K^\times/K^{\times e}$(指数 $e$)において $[v]_e = [a\xi]_e^{\,r}$ であり、$d\mid r$ ゆえ
> $$ \bigl([v]_e\bigr)^{e/d} = [a\xi]_e^{\,re/d} = \bigl([a\xi]_e^{\,e}\bigr)^{r/d} = 1,\qquad\text{すなわち}\quad \mathrm{ord}([v]_e)\ \Bigm|\ e/d\ <\ e. $$
> ゆえに $[K(v^{1/e}):K] = \mathrm{ord}([v]_e) < e = [K(v^{1/M}):K]$ で、両体は**一致しない**。∎
> **⇒ 「$\gcd(e,M/e)=1$ のときに限る」は必要十分として閉じた**(便 29 F3.3 の要求を満たす)。
>
> **(7.2) が破れる例**(便 28 F7.2): $M=4,\ e=2$ では $q(z)=z^2$ が位数 2 の平行移動部分群 $\{\pm1\}$ を丸ごと殺す。$A_5$ は $(M,e)=(5,5)$、$K^{(3)}$ は $(6,3)$ でどちらも (7.2) を満たすので、**定理 K3 にも $A_5$ にも影響しない**。
>
> **注 3(どちらの固定体か)【便 28 F7.4】**: (7.4) は $\ker\mathrm{Ih}_N$ の固定体である。$\ker(\Phi\circ\mathrm{Ih}_N)$ の固定体として読むには **$\Phi$ の単射性を別に仮定する**必要がある($K^{(3)}$ では (K4)、$A_5$ では $\mathrm{Aut}(A_5)=S_5$ の $\Lambda$ 上忠実性)。§0 の定理 K3 は後者の形で述べており、(K4) がその代金である。

#### 5.2.3 【v3 新規】(6′) の縮約 — 実質は「$\rho_0$ が忠実」の 1 ビット

> **補題 R′(縮約).** (1)(3) と shadow の定義($\Phi_{(m,f)}(X) = X^{2m+1}$、$\tilde\chi(m,f)=2m+1$)の下で、$\Lambda$ が $\Phi(\mathfrak F_0)$-安定なら
> $$ \rho_0(\mathfrak F_0)\ \subseteq\ \tau(\mu_M) $$
> は**自動**である。したがって (2) と併せて
> $$ \boxed{\ \text{(R6-act)}\iff \rho_0\ \text{が忠実}\ } $$
> である(像の等式は忠実性から従う)。

**証明**(3 行)。
1. $\varphi\in\mathfrak F_0 = \ker\tilde\chi$ なら $2m+1\equiv1\ (\mathrm{mod}\ 2M)$、とくに $\mathrm{mod}\ M$ でも $1$ だから $\Phi_\varphi(X) = X^{2m+1} = X$。
2. ゆえに $\Phi_\varphi\circ\mathrm{inn}_X\circ\Phi_\varphi^{-1} = \mathrm{inn}_{\Phi_\varphi(X)} = \mathrm{inn}_X$、すなわち $\rho_0(\varphi)$ は $\Lambda$ 上で $\tau(\zeta_M)$ と**可換**。
3. (3) より $\tau(\mu_M)$ は $\Lambda$ 上の **regular 可換部分群**である。regular 可換部分群の $\mathrm{Sym}(\Lambda)$ 内の中心化群はそれ自身($\Lambda\cong\mu_M$ と同一視すると左移動の中心化群は右移動、可換なので一致)。ゆえに $\rho_0(\mathfrak F_0)\subseteq C_{\mathrm{Sym}(\Lambda)}(\tau(\mu_M)) = \tau(\mu_M)$。
最後に $\rho_0$ 忠実なら $\lvert\rho_0(\mathfrak F_0)\rvert = e$ で、巡回群 $\tau(\mu_M)$ の位数 $e$ の部分群は $\tau(\mu_M[e])$ ただ一つ。∎

> **★ これが効く理由(W2 の再発防止)**: 検算 **T8e**(および `gap18a.json` の `perms_by_k`)が与えるのは「$\rho_\Lambda(\mathfrak F_0)$ の非自明元は型 $3.3$」という**置換型**だけである。$S_6$ には型 $3.3$ の元が 40 個・それが生成する $C_3$ が **20 個**あるので、**型だけでは $\tau(\mu_6[3])$ という 1 個を同定できない**(★教材 2 = W2 そのもの)。補題 R′ は、その同定を**型ではなく「$\mathfrak F_0$ は $X$ を固定する」という定義的事実から**与える。
>
> **検算(scratchpad 単発・10/10)**: D1 (3.6)(4.9)(4.12) から $G_3\le D_3^3$ を再構成し、標的クラス $\Lambda$(6 元)上で
> (E) $\Phi_{0,k}(\bar x) = \bar x$、(G) $\rho_\Lambda(\mathfrak F_0)\subseteq\tau(\mu_6)$、(H) $\rho_\Lambda(\mathfrak F_0) = \tau(\mu_6[3]) = \langle\tau^2\rangle$、(I) $\rho_\Lambda(\mathfrak F_0)$ の各元は $\tau$ と可換、(J) $S_6$ の型 $3.3$ の元 40 個・$C_3$ 部分群 20 個(W2 対照)を確認。
> 恒久化済み: `search/r6act-check.mjs`(司令塔再走 10/10・commit a0792b8)。
>
> **2 例での (6′) の成立**:
> | | $A_5$ 窓 | $K^{(3)}$ 窓 |
> |---|---|---|
> | $(M,e)$ | $(5,5)$ | $(6,3)$ |
> | $\rho_0$ 忠実の根拠 | $\mathrm{Aut}(A_5)=S_5$ の $\Lambda$(5 点)上の作用が忠実(v4 §3 項目 6) | 【GAP-18a】・T8d(§4 条件 4) |
> | 像の等式 | 補題 R′ より自動($\tau(\mu_5[5])=\tau(\mu_5)$) | 補題 R′ より自動 |
>
> **⇒ 第三例で確認すべきは「$\rho_0$ が忠実か」の 1 項目**(有限計算)。**それ以外の (6′) は前件 (1)(3) から自動的に付いてくる。** これが「第三例で検証可能な最小の型」である。
>
> **注(縮約が無効になる場合)**: 補題 R′ は (3) の regular 性を使う。第三例が (3) を満たさない($\mathrm{ord}(X)\ne\lvert\Lambda\rvert$、あるいは単純推移でない)窓なら縮約は使えず、(6′) を**そのままの形で**直接確認する必要がある。**この分岐自体を事前登録する**(§5.2.5)。

#### 5.2.4 【v3】型の採択 — なぜ (R6-act) で、cocycle 等式 (7.5) ではないか

便 28 F7.3 は 2 案を提示した: **(A)** $\tau/\rho_0$ 形 (R6-act)、**(B)** cocycle 等式
$$ \mathrm{Ih}_N|_{G_K} = \iota\circ q\circ\kappa_{u^{-1}}. \tag{7.5} $$
**本稿は (A) を正式定式とする。** 理由は 5 つで、Sol の推奨と結論は一致するが、独立の根拠を挙げる。

1. **判定可能性(決定的)**: (R6-act) は $\mathrm{Sym}(\Lambda)$ 内の部分群の等式で、窓の**有限群論データだけで有限計算で決着**する。(7.5) は $G_K$ 上の写像の等式であり、$\mathrm{Ih}_N$(超越的)と $\kappa_{u^{-1}}$(算術的)を含むので、**窓データからは原理的に「確認」できない**。前件は checkable でなければ族の設計図の部品にならない。
2. **同語反復に近い**: (7.5) を認めれば $\mathrm{Ih}_N(G_K)$ の像はそのまま $q\circ\kappa_{u^{-1}}$ の像であり、判定したい結論をほぼ前件に書き込むことになる。命題としての情報量が落ちる(便 28 F7.3 の指摘に同意)。
3. **ill-typed な $q$ を追放できる**: (7.5) は $q$ を前件に持ち込むが、便 28 W1 のとおり $q:\mu_M\twoheadrightarrow\mu_e$ は位数 $e$ の平行移動部分群への retraction とは限らない($M=4,e=2$ が反例)。(R6-act) は $q$ を使わず、$\tau(\mu_M[e])$ という**実在する部分群**だけを使う。$q$ は (7.2) が成立するときの**書き換えの便宜**へ降格され、そこが正しい居場所である(注 2)。
4. **既存の証明と 1:1**: (R6-act)+(5′) は §2.3(b)(d′) と §2.6 の**逐語的抽象化**であり、定理 K3 の証明に仮定を 1 つも足さない。**二例から一般条件を「発明」していない**ので、裁定 22 の過適合回避に適合する。
5. **縮約が効く**: (R6-act) は §5.2.3 により「$\rho_0$ が忠実」の 1 ビットへ落ちる。(7.5) にはこの縮約の余地がない(写像の等式は分解できない)。**型が小さいほど第三例での falsify が鋭い。**

> **(7.5) の扱い**: 破棄はしない。**(7.5) は前件ではなく系**として位置づける。ただし v3 は $\iota:\mu_e\to\mathfrak F_0$ を宣言しないまま「(7.5) が従う」と書いており、**v2 の型穴が系の側へ再侵入していた**(便 29 W1)。以下で修理する。

#### 5.2.4′ 【v3.1・便 29 P1】系 (7.5) の $\iota$ の型 — 正準同型 $j$ と $q$-free 形

> **定義(正準作用同型).** (R6-act) の下で、$\rho_0|_{\mathfrak F_0}$ は単射・$\tau|_{\mu_M[e]}$ は単射で像が一致する($=\rho_0(\mathfrak F_0)$)から、
> $$ \boxed{\ j\ :=\ \bigl(\rho_0|_{\mathfrak F_0}\bigr)^{-1}\circ\tau|_{\mu_M[e]}\ :\ \mu_M[e]\ \xrightarrow{\ \sim\ }\ \mathfrak F_0\ } \tag{1.1} $$
> は**同型として一意に定まる**。$j$ は $\rho_0$ と $\tau$ だけから決まり、**外から選ぶ自由度はない** — これが「指定された同型」との決定的な違いである。

> **系(q-free 形).** (1)(5′)(6′) の下で、$\kappa_{u^{-1}}$ の像は $\mu_M[e]$ に含まれる(補題 R の 3)。その corestriction を $\kappa_e:G_K\to\mu_M[e]$ と書けば、**coprime 条件なしで**
> $$ \boxed{\ \mathrm{Ih}_N|_{G_K}\ =\ j\circ\kappa_e\ } \tag{1.2} $$
> が成り立つ。
> **証明**: $\gamma\in G_K$ に対し (1) より $\mathrm{Ih}_N(\gamma)\in\mathfrak F_0$。(5′) より $\rho_0(\mathrm{Ih}_N(\gamma)) = \tau(\kappa_{u^{-1}}(\gamma)) = \tau(\kappa_e(\gamma))$。両辺に $(\rho_0|_{\mathfrak F_0})^{-1}$ を施して $\mathrm{Ih}_N(\gamma) = j(\kappa_e(\gamma))$。∎

> **系((7.5) 形・coprime のときのみ).** $r:=M/e$、$q(z):=z^{r}:\mu_M\twoheadrightarrow\mu_e$ とする。$\gcd(e,r)=1$ のとき $q_e := q|_{\mu_M[e]}:\mu_M[e]\xrightarrow{\sim}\mu_e$ は同型だから
> $$ \boxed{\ \iota\ :=\ j\circ q_e^{-1}\ :\ \mu_e\xrightarrow{\ \sim\ }\mathfrak F_0\ } \tag{1.3} $$
> と定義でき、このとき (1.2) から
> $$ \mathrm{Ih}_N|_{G_K} = \iota\circ q\circ\kappa_{u^{-1}} \tag{7.5} $$
> が**厳密に**従う。$\gcd(e,r)>1$ のときは $q_e$ が同型でないので $\iota$ は定義されず、**(7.5) は書けない**((1.2) は書ける)。

> **★ 注(なぜ型穴が見えなかったか — ★教材 9 の機構)**: $\mu_\infty$ の中で **$\mu_e$ と $\mu_M[e]$ は同じ部分群**である。だから「$q:\mu_M\twoheadrightarrow\mu_e$ を平行移動部分群 $\tau(\mu_M[e])$ の座標として使う」という誤りは、**集合としては正しく見えてしまう**。誤っているのは**写像**の側で、$q$ をその部分群に制限したものは恒等ではなく $z\mapsto z^{r}$ であり、$\gcd(e,r)>1$ なら**同型ですらない**($M=4,e=2$ では全体を潰す)。
> **⇒ 正しい座標は $q$ ではなく $j$ である。** $j$ は「$\Lambda$ 上の平行移動としてどう作用するか」から定義されており、$q$ のような外来の商写像を経由しない。**(1.2) を正準形、(7.5) を coprime 時の書き換えとする**のが v3.1 の立場である。

#### 5.2.5 射程条件と反証条件の事前登録(便 28 F8 step 1 →【v3.1・便 29 P3】五札へ再構成)

**結果値を一切含まない。第三例の計算前にこの節を封印する。**

> **【v3.1 の修理理由】** v3 の表は scope-in に **(5′) を含めながら**、その同じ行の下で「$\mathrm{ord}([u^{-1}]_M)=e$ なのに非全射」を $R^{\rm cyc}$ の実験的 falsifier としていた。しかし (5′) と (6′) を本当に確認済みなら、その不一致は §5.2.2 の有限群論により**既に不可能**である。起きた場合に分かるのは「私の紙上証明が誤り」か「前件の確認札が誤り」のいずれかで、**未証明の比較橋 $B_{\rm FC}$ を直接 falsify したことにはならない**(便 29 F5.2・W2)。**橋を試すには (5′) を前件から外して封印しなければならない。**

| 札 | 封印する内容 | 判定 |
|---|---|---|
| **FORMAL-IN** | $(0)(1)(2)(3)(5')(6')$ | **定理 $R^{\rm cyc}_{\rm formal}$ の適用条件**。ここから (R6-full)/(7.4) が導かれる。**結論との不一致は $R^{\rm cyc}$ の反証ではなく `proof/record consistency failure`**(§5.2.2 の証明の誤り、または前件の確認札の誤り) |
| **BRIDGE-IN** | **結果を見る前に固定した**モデル・全分岐 cusp・$\mathbb Q$-有理局所助変数・actual marking・FC 比較規約 $(4)(5)$ | ここから $(5')$ = (7.3) が出るかを検査する。**$u$ の抽出と actual Galois 作用の同定を同じ等式で相互定義しない**(独立 provenance) |
| **BRIDGE-FAIL** | BRIDGE-IN を**独立に**満たすのに (7.3) が破れる | **比較橋 $B_{\rm FC}$ の真の falsifier**。これだけが $R^{\rm cyc}$ スキーマへの実弾 |
| **BRIDGE-UNKNOWN** | $(4)(5)$ から actual Galois 作用との比較を**閉じられない** | **scope-out ではなく UNKNOWN**(一級の結果)。窓は捨てず、比較が閉じない理由を記録する |
| **SCHEMA-OUT** | regular detector 不在($\mathrm{ord}(X)\ne\lvert\Lambda\rvert$ / 単純推移でない)/ $\Lambda$ が $\Phi(\mathfrak F_0)$-不安定 / $\rho_0$ が非忠実 / $\mathfrak F_0$ が非巡回 | **現スキーマの射程外**($R^{\rm cyc}$ の反例ではない)。$H$ の取り直しか前件の拡張を検討 |

> **FORMAL-IN 内の整合性検査(反証ではない)**: (1)(3) が成立する窓で $\rho_0(\mathfrak F_0)\not\subseteq\tau(\mu_M)$ が観測されたら、**補題 R′ の私の証明が誤り**である(これも `proof/record consistency failure`)。同時に (6′) の直接確認へ切替える。
>
> **legacy regression test(旧「$q$-版の反証条件」・改名)**: $\gcd(e,M/e)>1$ の窓で $K(u^{1/e})\ne\mathrm{Fix}(\ker\mathrm{Ih}_N)$ かを見る試験。**これは v2 で既に撤回した表記に対する回帰試験であり、v3.1 の安全形 (7.4)/(1.2) の live な falsifier ではない**(便 29 F5.2)。§5.2.2 注 2 で必要十分が閉じたので、**理論的には結果が予測できる**(不一致が出る)。**予測どおりでも $R^{\rm cyc}$ の支持証拠にはならない**ことを明記して記録する。
>
> **★ 第三例の選定基準(便 28 P4/W3 に同意)**: $\gcd(e,M/e)>1$ の **repeated-primary regime** を優先する。既存 2 例はどちらも (7.2) を満たす coprime regime なので、同じ regime から第三例を取ると**共有された隠れ仮定を暴けない**。
> ただし §5.2.3 の縮約により、repeated-primary regime で試されるのは **(6′) ではなく legacy regression test と $B_{\rm FC}$ の一般性**であることに注意する — (6′) 自体は $\gcd$ に依存しない。**この整理は第三例で何が falsify されうるかを鋭くする**(便 28 W3 の運用形)。
>
> **★ 便 29 ★教材 3(転記)**: **証明済みの形式帰結と未証明の比較橋を同じ候補名で呼ぶと、falsifier の宛先が失われる。** 前件・橋・帰結の三札を分けて初めて、第三例が何を試したかが残る。(★教材 12 として §8 に登録。)

### 5.3 2 適用(同一機械が動くことの確認)

| | **適用 1: $A_5$ 窓** | **適用 2: $K^{(3)}$ 窓** |
|---|---|---|
| $P$ | $A_5$(単純・**非可解**) | $G_3\cong\mathbb F_3^3\rtimes C_2^2\le D_3^3$(位数 108・**可解**) |
| marking / $M$ | $(5,5,5)$ / $M=5$(**素数**) | $(6,6,6)$ / $M=6$(**合成数**) |
| 合同性 | **合同**($\bar N_A=\bar\Gamma(10)$) | **非合同**(K-cong) |
| $\mathfrak F_0$ / $e$ | $C_5$ / $e=M=5$ | $C_3$ / $e=3\mid M=6$ |
| $q$ | 恒等 | $\mu_6\twoheadrightarrow\mu_3$(**3-primary pushout**) |
| **(v3)** $\gcd(e,M/e)$ | $\gcd(5,1)=1$ ✓ | $\gcd(3,2)=1$ ✓ — **両者とも coprime regime** |
| **(v3)** (6′) の根拠 | $\rho_0$ 忠実($S_5$ の 5 点作用)+ 補題 R′ | $\rho_0$ 忠実(【GAP-18a】・T8d)+ 補題 R′ |
| dessin | 次数 5・種数 2・$(5,5,5)$・LMFDB `5T4-5_5_5-a` | 次数 6・種数 1・ordered $(6,2^21^2,6)$・LMFDB `6T9-6_6_2.2.1.1-a`(**別正規化**) |
| $u$ | $-1/2\equiv2^4$ | $-4 = -2^2$ |
| 体 | $\mathbb Q(\zeta_5,\sqrt[5]2)$、$\mathrm{Gal}\cong F_{20}$ | $\mathbb Q(\zeta_{12},\sqrt[3]2)$、$\mathrm{Gal}\cong S_3\times C_2$ |

> **★ 論文の骨格案**: 「**比較スキーマ + 2 適用**」。**単純/可解、素数/合成数、合同/非合同という三軸で対極にある 2 窓が同一の手順で決まる**ことが説得力になる。$A_5$ は「なぜ円分だけで足りないか」を、$K^{(3)}$ は「合成数 $M$ で primary 成分をどう分けるか」を与え、**二つ合わせて Conj 5.1 の地形図になる**。
> **ただし論文の主張は「族の定理を証明した」ではなく「2 事例を同一スキーマで実行し、族の定理の前件候補を特定した」**である(便 27 F9 に同意)。
> **【v3】第四の軸は共有されている**: 2 例はどちらも $\gcd(e,M/e)=1$ の coprime regime にある。**論文でもこの共有仮定を明示する**(便 28 W3)。

> **Remark(【v3.1・便 29 F6 (6.1)】奇数族では coprime は「見込み」でなく構造的確定).**
> D1 の $K^{(n)}$ 族について、**$n$ が奇数なら**
> $$ M = K^{(n)}_{\rm ord} = \mathrm{lcm}(n,2) = 2n,\qquad \mathfrak F_0\cong C_n,\qquad e = n,\qquad M/e = 2 $$
> ゆえに
> $$ \boxed{\ \gcd(e,\ M/e) = \gcd(n,2) = 1\ } \tag{6.1} $$
> が**構造式から確定する**(便 29 F6)。
> **根拠と、私が確認した範囲**: $M=\mathrm{lcm}(n,2)$ は D1 **(3.4) 逐語**(抽出ノート D1 §3)。$\mathcal X_n=\{m\in\{0,\dots,K_{\rm ord}-1\}:\gcd(2m+1,K_{\rm ord})=1\}$ は **(4.12) 直下の定義**で、$n$ 奇なら $2m+1$ は奇数ゆえ $\gcd(2m+1,2n)=1\iff\gcd(2m+1,4n)=1$、したがって $m\mapsto2m+1$ は $\mathcal X_n\xrightarrow{\sim}(\mathbb Z/4n)^\times = (\mathbb Z/2M)^\times$(**私の 2 行導出・$n=3$ で $\{0,2,3,5\}\to\{1,5,7,11\}$ と一致 = 検算 T8a**)。$4\nmid n$ なので (4.12) の $k$ は $\bmod\ \mathrm{ord}(r^2)=n$ を走り、$\lvert\mathrm{GT}(K^{(n)})\rvert = 2\varphi(n)\cdot n$、$\lvert\mathfrak F_0\rvert = \lvert\mathrm{GT}\rvert/\lvert(\mathbb Z/4n)^\times\rvert = n$。Thm 4.6 (4.23) の $\mathrm{Aff}(\mathbb Z/n)\times\mathcal Z_2$($n_0=n,\alpha=0$)の**平行移動部 $\mathbb Z/n$ が $\mathfrak F_0$** で、これは巡回 $C_n$。**$n=3$ ではすべて本稿の値と一致($M=6$・$e=3$・$\mathfrak F_0\cong C_3$)。一般 $n$ 奇での原論文 PDF 逐語照合は本稿では未実施**(出所は便 29 (6.1) と抽出ノート D1)。
> **★ 二重計上の禁止**: D1 **Prop 3.4 逐語**「For every odd integer $n\ge3$, we have $K^{(n)} = K^{(2n)}$」より **$K^{(5)} = K^{(10)}$**。第三例に $K^{(5)}$ を取るなら、$K^{(10)}$ を**独立な第四例として数えてはならない**(便 29 F6)。
> **★ 帰結(第三例の設計に効く)**: 奇数族の窓は**どれも coprime regime**である。したがって **$n$ を奇数のまま増やしても legacy regression test(repeated-primary)には一票も入らない**(便 29 W6)。repeated-primary を試す役は $4\mid n$ 側($n=12$ 等)へ保留する。

---

## 6. 根基 2 — 観測列プロトコル(便 27 F10 を採用)

現時点の 2 点: $A_5$: $q_*[u] = [2]^4$、$K^{(3)}$: $q_*[u] = [2]^2$。$A_5$ 側の $2$ は古典的に説明がつく($\lambda(\tau)=16q^{1/2}-128q+\cdots$、$16=2^4$)。$K^{(3)}$ は**非合同なので $q$ 展開の説明は使えない**(曲線 54.b3 の導手の台は $\{2,3\}$)。

**2 点は素数/合成数・合同/非合同・非可解/可解の全てで対極にあり、族則を予測する機構はまだない。** ゆえに**予測として登録しない**(cusp-16 の轍)。代わりに:

> **観測列プロトコル**: 新規 $R^{\rm cyc}$ 窓ごとに、$q_*[u]\in K^\times/K^{\times e}$ が $\langle[2]\rangle$ に入るかを**盲検で記録**する。
> **即時棄却規準**: $2$ 以外の素点で valuation が $e$ の倍数でない一例が出れば「根基 2」候補は**即棄却**。
> **昇格条件**: 三つ以上の独立な新規窓で残ってから初めて $\mathrm{(G7_{rad2})}\ q_*[u]\in\langle[2]\rangle$ を予測候補へ上げる。

> **【v3・記法の整合】** §5.2 で $q$ を前件から外したので、本節の $q_*[u]$ は「(7.2) の下での書き換え」として読む。$\gcd(e,M/e)>1$ の窓では代わりに **$[u^{-1}]_M$ そのもの**を記録する(観測対象の定義は窓に依らず (7.4) の側で固定しておくのが安全)。

---

## 7. 【GAP】と状態札

| # | 内容 | 状態 |
|---|---|---|
| ~~【GAP-K3a】~~ | (K4) $\Phi$ 単射 | **閉**(§2.5・便 27 F4・検算 T7) |
| ~~【GAP-20b】~~ | Möbius 正規化不変性 | **閉**(§3・数え方を訂正した上で・射程は `ordered-passport-preserving`) |
| ~~C7 / 便 25 F5-2~~ | 3-primary pushout | **閉**(§2.3 修理版) |
| 【GAP-K3b】 | 平面モデルが LMFDB Weierstrass モデル(54.b3)と同じ被覆であることは未検証。**依存していない** | 低 |
| 【GAP-K3c】 | 委嘱 20 §3 の 2 段塔(経路 B・$u$ の第三系統)は未完(【GAP-20a】) | 低 |
| **【GAP-Rcyc】= 比較橋 $B_{\rm FC}$** | **「精密化した (4)(5) から (5′)(7.3) を一般に導く段」**(§5.2.2)。2 例では個別に構成済み。**$R^{\rm cyc}_{\rm formal}$(証明済)とは別札**(§5.2.−1) | 中(族の定理への本丸)・**`candidate / UNKNOWN`** |
| **【状態】** | **`paper-proof / two-mathematician audit PASS`**(便 28 検収・裁定 22 で確定)。**札の射程は §7.1 のとおり項目別。** 解析・算術部分は Opus/Sol の紙上一致(**厳密な blind independence ではない** — §3)。**`verified`(Lean)ではない** | — |

### 7.1 【v3 新規】状態札の射程分け(便 28 F9・P5 / 裁定 22)

> v2 冒頭と §7 の「群論部分($\Lambda$ の構造・$\mathfrak F_0$ の作用・$\Phi$ 単射)は GAP と node の二系統一致 = `cross-checked`」は**射程が広すぎた**。正しくは:

| 項目 | 証拠の系統 | 札 |
|---|---|---|
| $\Lambda$ の構造($\lvert\Lambda\rvert=6$・$N_G(H)=H$・qualifying 18 個・像 36/核 3) | **GAP(`gap18a.json`)+ node(T3a–T3d・T10a–T10b)** | **`cross-checked`** |
| $\mathfrak F_0$ の $\Lambda$ 上の作用(位数 3・非自明元は型 $3.3$) | **GAP(`f0_generated_order`・`perms_by_k`)+ node(T8d・T8e・T10c–T10d)** | **`cross-checked`** |
| **$\Phi$ の単射性(全 12 元)** | **紙上証明(§2.5)+ node(T7b–T7g)**。`gap18a.json` は **12 個の誘導自己同型の相異性を明示検査していない** | **紙上 + node 単系統**(項目単独では `cross-checked` と言わない) |
| **good 12 個の $\mathrm{Aut}(G_3)$-融合**(6+6 分裂を一軌道にする) | **node(T3c2・T6a・T6b)のみ**。`gap18a.json` は 4 つの $G_3$-共役類を与えるが、**Aut-融合そのものの独立 GAP 証明書ではない** | **node 単系統** |
| $u = -4$ と $[u^{-1}]_6$ の位数 3 | Opus(委嘱 21)+ Sol(便 25)の紙上二者一致。**便 25 が独立性汚染を自己申告**(§3) | **二者一致・blind independence なし** |
| **定理 K3 全体** | 便 27(条件付き PASS)→ v2 → 便 28(PASS) | **`paper-proof / two-mathematician audit PASS`** |
| **【v3.1】定理 $R^{\rm cyc}_{\rm formal}$**(§5.2.1–§5.2.2) | 本稿の紙上証明 + 便 29 F3.1/F3.2 の検収 | **`paper-proof`**(Lean `verified` ではない) |
| **【v3.1】補題 $R'$(縮約)**(§5.2.3) | 本稿の紙上証明 + 便 29 F2 の検収 + scratchpad 検算 10/10($K^{(3)}$ 実例) | **`paper-proof`**($K^{(3)}$ 実例は node 単系統) |
| **【v3.1】比較橋 $B_{\rm FC}$**(= 【GAP-Rcyc】) | 2 例で個別に構成(§2.3(b)・$A_5$ v4 §3.5)。一般証明なし | **`candidate / UNKNOWN`** |
| **【v3.1】$R^{\rm cyc}$ スキーマ** | $B_{\rm FC}$ と $R^{\rm cyc}_{\rm formal}$ の接続設計図 | **設計図**(定理でも定理候補でもない) |
| Lean 形式化 | — | **なし**(`verified` は名乗らない) |

> **★ 教訓**: 「二系統一致」は**証明書の粒度で主張する**べきで、文書の節の粒度でまとめて主張してはいけない。同じ JSON 証明書が覆う項目と覆わない項目が同居する。**(★教材 11 として §8 に登録。)**

**検算スクリプト**

| ファイル | 内容 | 結果 |
|---|---|---|
| **`search/week4-k3-v2-repairs.mjs`** | D1 (3.1)(3.6)(4.9)(4.12) から $G_3\le D_3^3$ を自前で再構成。部分群全列挙・$N_G(H)$・$\Lambda$・ordered passport 分裂・**(a′) の stabilizer 同定と v1 の反例構成**・$\lvert\mathrm{Aut}(G_3)\rvert=1296$・Aut-軌道・**12 個の $\Phi_{m,k}$ が自己同型であることと単射性**・$\mathfrak F_0$ の $\Lambda$ 上忠実性・`gap18a.json` との突合 | **43/43** |
| `search/week4-u-k3.mjs` | 臨界方程式・節点・冪級数・$u=-4$・$u'=-256/729$・3-剰余類一致 | 16/16 |
| `search/week4-19a19e.mjs` | Aut-軌道・exact conjugator の存在と一意性 | 7/7 |
| `search/week4-d2d4-k3.mjs` | B1–B5・$\lvert\mathrm{GT}\rvert=12$・$\mathfrak F_0\cong C_3$ | 13/13 |
| **`search/r6act-check.mjs`(v3)** | §5.2.3 の縮約: $\Phi_{0,k}(\bar x)=\bar x$・$\rho_\Lambda(\mathfrak F_0)\subseteq\tau(\mu_6)$・$=\tau(\mu_6[3])$・$\tau$ と可換・**W2 対照($S_6$ の型 $3.3$ の $C_3$ は 20 個)** | **10/10**(司令塔再走・commit a0792b8) |

---

## 8. ★ 教材(便 27 W1–W7 の受領・v3 で 9–11・**v3.1 で 12–13** を追加)

1. **【W1・自分が踏んだ】共役部分群の stabilizer は $N_G(H)$、coset の stabilizer は $H$。** 取り違えると「自由に作用する」を無根拠に言ってしまう。**$G_3$ の中に実在する反例を自作した**(T4e)。
2. **【W2・自分が踏んだ】置換の cycle type は部分群を同定しない。** $S_6$ の不動点なし $C_3$ は一意でない。**包含があるなら位数を数える** — 補題 P は $\mathrm{Ih}(G_K)\le\mathfrak F_0$ と両者位数 3 だけで閉じる。**委嘱 14 の★教材「名前は不変量ではない」の再演**。
3. **【W3】「shadow パラメータの一意性」と「有限商への自己同型の単射性」は別問題。** 加えて**その裏面**(「そもそも自己同型か」)も別に検査すべきで、本稿は T7b でそれを塞いだ。
4. **【W4】B2/B3/B5 は窓だけでなく permutation representation ごとの判定。** 次数 12 で FAIL でも次数 6 で PASS しうる。
5. **【W5】$\mathrm{Aut}=1$ は descent 障害を消すが field of moduli $=\mathbb Q$ を単独では与えない。**
6. **【W6】合成数 $M$ では「torsor 全体を推移的にする」と「GT 核の必要な primary 成分を埋める」を区別する。** 本件は $C_3$ を Kummer、$C_2^2$ を円分が埋める。
7. **【W7】経路が異なることと blind independence は同義でない。**
8. **【本稿発】ordered passport は $G$-共役類を分ける不変量である。** $N_G(H)=H$ なる 12 個は $(6,2^21^2,6)$ と $(6,6,2^21^2)$ の二類に割れ、$\mathrm{Aut}(G_3)$ が融合する。**LMFDB との照合で $\lambda$ 割当を揃える必要があった理由はこれ**(§2.2 注)。
9. **【v3・便 28 W1】全射 $q:\mu_M\twoheadrightarrow\mu_e$ は、位数 $e$ の平行移動部分群への retraction とは限らない。** $M=4,e=2$ では $q(z)=z^2$ が $\{\pm1\}$ を丸ごと殺す。**「商への射」と「部分群の切断」は別物** — 前者を後者のつもりで使うと前件が空回りする。$\gcd(e,M/e)=1$ がちょうどその差を消す条件(§5.2.2 注 2・必要十分)。
 **【v3.1 追記・なぜ見えなかったか】** $\mu_\infty$ の中で **$\mu_e$ と $\mu_M[e]$ は同じ部分群**である。だから「$q$ の終域を平行移動部分群の座標として使う」誤りは**集合としては正しく見える**。誤っているのは写像で、$q$ をその部分群に制限したものは恒等ではなく $z\mapsto z^{M/e}$。**型の穴は「対象が違う」形ではなく「同じ対象への別の写像を取り違える」形で現れうる**(§5.2.4′)。正しい座標は外来の $q$ ではなく、作用から定義される $j$ (1.1)。
10. **【v3・便 28 W2】「作用と一致する」は、domain / codomain / 可換図を書かない限り判定可能な前件にならない。** $R^{\rm gen}$ の「$\mathfrak F_0$-成分」→ $R^{\rm cyc}$ の「$q$ が作用と一致」→ (R6-act) の「$\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$」という 3 段の改訂は、**同じ内容を語から型へ落としていく作業**だった。**型が書けたときにはじめて、それが自動で従うか(補題 R′)も問える。**
11. **【v3・本稿発】「二系統一致」は証明書の粒度で主張せよ。** 同じ JSON 証明書が覆う項目と覆わない項目は同居する。**節の粒度で `cross-checked` とまとめると、実際には単系統の項目が紛れ込む**(§7.1)。
12. **【v3.1・便 29 ★教材 3 転記】証明済みの形式帰結と未証明の比較橋を同じ候補名で呼ぶと、falsifier の宛先が失われる。** 前件・橋・帰結の三札を分けて初めて、第三例が何を試したかが残る。**系として: 比較等式そのものを前件に置いた瞬間、その先の結論試験は「橋の試験」ではなく「形式系の整合性試験」になる**(§5.2.−1・§5.2.5)。
13. **【v3.1・便 29 ★教材 1 転記】regular 部分群は self-centralizing とは限らない — 可換性が代金である。** 左正則作用の中心化群は右正則作用であり、両者が同じ部分群になるのは作用群が可換なとき。補題 $R'$ が $\mu_M$ の可換性に依存していることを忘れない(§5.2.3)。

---

## 9. 便 28 への論点(起草時のまま保存)

> **便 28 の回答先**: 1 → F2、2 → F3、3 → F5.1、4 → F7/F8、5 → 言及なし(§6 のプロトコルは据置)。

1. **§2.3 注 2**: 忠実性を使わない (d′) の短縮は正しいか。忠実性の load-bearing な使用箇所を §2.6 に一本化した依存関係整理に同意するか。
2. **§2.5 の強化**(12 個が実際に $\mathrm{Aut}(G_3)$ の元であることの悉皆検査)は、便 27 F4 が前提にしていた部分を埋めているか。過剰か。
3. **§2.2 注の新事実**(ordered passport による 6+6 分裂)は便 27 F6 P5 の「良い 12 個が一軌道」と整合するが、**$G_3$-共役類としては 2 つ**である。標的クラスの指定を本文で固定した形で問題ないか。
4. **§5.2 $R^{\rm cyc}$ の 6 前件**は必要十分に近いか。とくに (6) の $q$ を「窓のデータから導く条件」を次に定式化すべきか、それとも 3 例目の窓を先に取るべきか。
5. **§6 の観測列プロトコル**の棄却規準($2$ 以外の素点で valuation が $e$ の倍数でない)で十分か。

---

## 10. 便 29 への論点(v3 発・起草時のまま保存)

> **便 29 の回答先**: 1 → F1.1(五理由すべて妥当・採択 PASS)、2 → F2(三段とも正しい・PASS)、3 → F4(同意・ただし三札に分けよ)、4 → F5(五札へ修理)、5 → F8(GAP 側再発注は【GAP-Rcyc】より優先しない)。**すべて v3.1 に反映済み。**

1. **§5.2.4 の採択**((R6-act) を正式定式・(7.5) は系へ降格)に同意するか。とくに理由 3(ill-typed な $q$ の追放)と理由 5(縮約可能性)は便 28 F7.3 に無い私の根拠である。
2. **§5.2.3 の補題 R′(縮約)**は正しいか。「$\mathfrak F_0$ は $X$ を固定する ⇒ $\rho_0$ は $\tau$ と可換 ⇒ regular 可換の中心化群はそれ自身」の 3 段に穴はないか。**もし正しければ、第三例で確認すべき (6′) は「$\rho_0$ が忠実」の 1 項目に減る。**
3. **§5.2.2 の「未証明部の所在の移動」**((6) の $q$ → (5′) の「(4)(5) ⇒ (7.3)」)に同意するか。**族の定理への本丸は (5′) だ**という読みでよいか。
4. **§5.2.5 の事前登録表**(適用条件 / 反証条件 / 射程外 / $q$-版の反証 / 縮約の反証)で、第三例の前に封印すべき定義は尽きているか。とくに「射程外は棄却ではない」という札の分離は運用可能か。
5. **§7.1 の射程分け**で、$\Phi$ 単射と Aut-融合を GAP 側でも独立に取るべきか(証明書の追加発注に値するか)、それとも紙上証明があるので不要か。

---

## 11. 便 30 への論点(v3.1 発)

1. **§5.2.4′ の (1.1)–(1.3)**: $j$ を「正準」と呼ぶ根拠は「$\rho_0$ と $\tau$ だけから決まる」ことだが、**$\tau$ 自身は「$\zeta_M\mapsto X$ による共役」という同定を含む**(§5.2.0 の $\tau$ 宣言)。この同定は局所助変数の選択(§2.3 注 4 の generator の向き)に依存する。**$j$ の正準性は「$\tau$ を固定したうえでの正準性」であって絶対的ではない** — この二段構えを本文に書いたが、$\tau$ の選択の曖昧さ($(\mathbb Z/M)^\times$ 分の自由度)が (1.2) の**内容**を変えないこと(体も判定も不変)は §2.3 注 4 の窓固有の議論に依存しており、**一般形での証明は書いていない**。ここは【GAP】に立てるべきか、それとも $\tau$ を BRIDGE-IN の封印項目に含めれば足りるか。
2. **§5.2.5 の五札**で、**legacy regression test の結果は「予測どおり」でも支持証拠にならない**と書いた。この非対称(反証にはなるが確証にはならない)を manifest にどう記録するのが運用可能か。
3. **§5.3 Remark (6.1)**: 私が確認したのは抽出ノート D1 経由の構造式と $n=3$ 実例のみで、**一般 $n$ 奇の原論文逐語照合はしていない**。$K^{(5)}$ manifest の事前値((6.1) と $\lvert\mathrm{GT}(K^{(5)})\rvert=40$)を封印値として使う前に、$n=5$ 実例の独立計算で較正すべきか。
4. **便 29 F7.2 の警告(passport $(10,10,10)$ を先入観にしない)**: $XYZ=1$ かつ 10-cycle 三つはすべて奇置換ゆえ符号だけで不可能 — これは私も独立に同意する。**$R^{\rm cyc}$ が要求するのは「選んだ cusp の $X$ が $\Lambda$ 上 regular」だけ**という理解でよいか(前件 (3) は $X$ についてのみの条件で、$Y,Z$ には何も要求しない、と読んでいる)。
5. **★教材 13 に関連して**: 補題 $R'$ は $\mu_M$ の可換性に依存する。**非可換な detector 群(例えば $\Lambda$ 上の regular 非可換作用)を使う窓は SCHEMA-OUT か、それとも別スキーマの入口か。**

---

## 【v3.2 addendum】(2026-07-27・便 30 F1.3 / 裁定 26-1 = P2)— **依存表のみの更新。本文は一切編集していない。**

> **この addendum が変えるもの**: 【GAP-18a】(= §4 の条件 4「$\Lambda$ 上で $\mathfrak F_0$ 忠実」)の**役割の札**だけ。
> **この addendum が変えないもの**: §0 の主定理・§1 の仮定リスト・§2 の全論証・§3 の $u$ 抽出・§5 の $R^{\rm cyc}$ 型付け・§6・§7.1 の射程分け・全検算値・全既存番号。**定理 K3 の内容は 1 ミリも動かない。**

### A. 何が起きたか

第三例($K^{(5)}$)の構造確定作業で、**奇数族全体に効く構造補題**が得られた(`docs/week4-K5橋_D1_opus_v1.md` §5.4・便 30 F1 で検分 PASS・裁定 26-1 で採用)。

> **命題 K5-1.** $n\ge3$ 奇数、marking は D1 (3.6)、$\mathfrak F_0 = \ker\tilde\chi$ とする。$\mathrm{inn}(g)(h) := ghg^{-1}$ の規約の下で
> $$ \boxed{\ \Phi_{0,k}\ =\ \mathrm{inn}\bigl(\bar x^{-2k}\bigr)\qquad(k\bmod n),\qquad \Phi(\mathfrak F_0) = \mathrm{inn}\bigl(\langle\bar x^2\rangle\bigr)\subseteq\mathrm{Inn}(G_n).\ } $$
> ゆえに**前件 (3) を満たす任意の $H$ に対して**、$\Lambda$ は $\Phi(\mathfrak F_0)$-安定(内部自己同型は共役類を保つ)であり、$\langle\bar x^2\rangle$ は $\langle\bar x\rangle$-torsor $\Lambda$ に自由に作用するので **$\rho_0$ は忠実で $\rho_0(\mathfrak F_0) = \tau(\mu_M[e])$**。

**$n=3$ への適用**: $\langle\bar x^2\rangle\cong C_3$ が標的 $C_6$-torsor $\Lambda$(6 元)に自由に作用する。ゆえに $\rho_\Lambda\vert_{\mathfrak F_0}$ の忠実性は**紙上で閉じる**。

### B. 依存表の更新(§4 の残条件表・§7 の【GAP】表に対する差分)

| 項目 | v3.1 までの札 | **v3.2 での札** |
|---|---|---|
| §4 条件 4「$\Lambda$ 上で $\mathfrak F_0$ 忠実」 | **閉**(【GAP-18a】・T8d で二系統一致)。**§2.6 の固定体同定の load-bearing な入力** | **閉**(**命題 K5-1 により紙上**)。【GAP-18a】・T8d は **命題 K5-1 の $n=3$ 較正・独立照合**へ降格 |
| 【GAP-18a】(証明書 `certificates/k3/gap18a.json` の `f0_generated_order` / `perms_by_k`) | load-bearing な数値入力 | **数値は正しいまま**(誤りになったのではない)。役割が「唯一の根拠」→「構造補題の独立確認」へ |
| §2.6「$\Leftarrow$」の依存 | 【GAP-18a】の忠実性 | **命題 K5-1**(紙上)。機械証拠は照合として併記 |
| §5.2.3 補題 $R'$ | (1)(3) から $\rho_0(\mathfrak F_0)\subseteq\tau(\mu_M)$ は自動、残る 1 ビット = 忠実性 | **不変**(補題 $R'$ 自体は正しい)。命題 K5-1 は**奇数族に限ってその 1 ビットも消す強化**であり、補題 $R'$ と競合しない(便 30 F1.2) |
| §5.2.3 末尾「⇒ 第三例で確認すべきは『$\rho_0$ が忠実か』の 1 項目」 | 第三例で有限計算が要る | **$n$ 奇なら不要**($n$ 偶・族外の窓では依然 1 項目の確認が要る) |

### C. 何が変わらないか(明示)

- **全射性の証明(§2.4)は元から忠実性を使っていない**(§2.3 注 2)。したがって主定理の全射性部分には影響ゼロ。
- **固定体 $L_3 = \mathbb Q(\zeta_{12},\sqrt[3]2)$ の同定(§2.6)は結論も証明も不変**。変わったのは「忠実性をどこから調達するか」だけである。
- **(K4) $\Phi$ 単射(§2.5)は別ゲート**であり、本 addendum は触れない。§7.1 の射程分け(紙上+node 単系統)もそのまま。
- **§7.1 の状態札の表は改訂しない。** 【GAP-18a】は依然として `cross-checked` な数値証拠である。

### D. 副次的に得た再利用可能部品(定理 K3 に遡及適用できるが、本 addendum では適用しない)

- **補題 Q**(K⁵ 橋 D1 §6.1・便 30 F3.1 検分 PASS): $\Phi(\mathrm{GT}(N))$ が標的の**個々の** $P$-共役類を保てば、$W_0$ の field of moduli は $\mathbb Q$。**(K3‡) の exact lift を必要としない**(inner ambiguity が共役類で消える)。
- 便 30 F3.3 の条件: 定理 K3 の (P7)(残留 descent なし)へ再利用するには、**$K^{(3)}$ で「$\Phi(\mathrm{GT}(K^{(3)}))$ が標的の $G_3$-共役類(6 個の側)を保つ」を先に確認**する必要がある。**本 addendum では確認していない** — 【GAP-K3d】として新規に立てる(優先度: 低。既存の明示 $\mathbb Q$-モデルで (P7) は既に閉じているため)。**既存の明示モデルや exact marking を補題 Q で置換してはならない**(便 30 F3.3)。

### E. ★教材への追加(§8 の 12–13 に続く)

14. **【便 30 ★1 / 裁定 26-3】族の中で欲しい算術 regime が現れる条件と、detector がその成分を見失う条件が一致することがある。** $K^{(n)}$ 族では**どちらも $8\mid n$**: repeated-primary($\gcd(e,M/e)>1$)が発火する窓では $\Phi_{0,n/4} = \mathrm{inn}(\bar x^{-n/2}) = 1$(中心元)ゆえ $\ker(\Phi\vert_{\mathfrak F_0})\supseteq C_2$。**ゆえに §5.2.5 の legacy regression test は $K^{(n)}$ 族の中では原理的に実行できない**(全 repeated-primary 窓が SCHEMA-OUT)。$K^{(8)}$ は最小の実例で、**負較正**として使える。
15. **【便 30 ★2】outer action の inner ambiguity は部分群の共役類には見えない。** だから field of moduli には (K3‡) の exact lift が不要(補題 Q)。**しかし actual marking と局所 $\tau$ には再び exact data が要る** — どの段が安くなり、どの段が安くならないかを取り違えない。

> **記帳**: 本 addendum は依存表の更新のみ。定理 K3 の状態札(`paper-proof / two-mathematician audit PASS`)は不変。
