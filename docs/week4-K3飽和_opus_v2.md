# 定理 K3 — 奇数側 dihedral 窓 $K^{(3)}$ の算術飽和(答案 **v2**・便 27 監査反映版)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 23。Sol 便 27(条件付き PASS)の必須修正 4 件・推奨 5 件を反映。**
v1 は `docs/week4-K3飽和_opus_v1.md` に保存(上書きしていない)。
入力: `docs/notes/抽出_Kn定義_D1.md`(正典・逐語)・`docs/week4-A5算術飽和_v4.md` §1(窓非依存部品)・委嘱 18/19/20/21(自作)・`sol/sol_reply_25_u_k3.md`・**`sol/sol_reply_27_k3.md`(全文)**・`certificates/k3/gap18a.json`・`docs/scout/scout_20260726_6t9_requery.md`。
検算: **`search/week4-k3-v2-repairs.mjs`(新規・43/43)**・`search/week4-u-k3.mjs`(16/16)・`search/week4-19a19e.mjs`(7/7)・`search/week4-d2d4-k3.mjs`(13/13)。
**状態: 紙上(修理済)。群論部分($\Lambda$ の構造・$\mathfrak F_0$ の作用・$\Phi$ 単射)は GAP と node の二系統一致 = `cross-checked`。定理全体は `verified` ではない。**

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
> **注 2(便 27 F3.2 より更に短くできる)**: Sol の (3.3) は $\rho_\Lambda|_{\mathfrak F_0}$ の忠実性(【GAP-18a】)を使って $\lvert\rho_\Lambda(\mathfrak F_0)\rvert=3$ を出し、像の一致から $\mathrm{Ih}(G_K)=\mathfrak F_0$ を導く。しかし上の (d′) のとおり、**包含 $\mathrm{Ih}(G_K)\le\mathfrak F_0$ と $\lvert\mathfrak F_0\rvert=3$ と $\lvert\rho_\Lambda(\mathrm{Ih}(G_K))\rvert=3$ だけで閉じ、忠実性は要らない**。忠実性が本当に load-bearing なのは **§2.6 の固定体の同定**である。依存関係を正確にするため本稿はこの形を採る(便 27 の結論は変わらない)。
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

> **強化(便 27 に無い)**: 検算 **T7b** は、12 個の $\Phi_{m,k}$ が**実際に $G_3$ の自己同型である**ことを、BFS 語表現による全 108 元への評価と準同型性の悉皆検査で確認した(全単射性も込み)。便 27 F4 は $(m,k)\mapsto$(生成元像)の単射性のみを見ており、「そもそも $\Phi_{m,k}\in\mathrm{Aut}(G_3)$ か」は前提にしている。**逆写像の向きの穴(W3 の裏面)をここで塞いだ。**
>
> **規約の頑健性**: $\Phi(\bar y) = f\bar y^{u}f^{-1}$ という逆向きの規約でも、$k\mapsto -k$ の置換になるだけで単射性の論証は不変。

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

### 5.2 $R^{\rm cyc}$(**定理候補・未証明**)— 便 27 F9 の 6 前件を採用

> **候補命題 $R^{\rm cyc}$.** 次を仮定する。
> **(1)** $1\to\mathfrak F_0\to\mathrm{GT}(N)\xrightarrow{\tilde\chi}(\mathbb Z/2M)^\times\to1$ かつ $\tilde\chi\circ\mathrm{Ih}=\chi_{2M}$。
> **(2)** $\mathfrak F_0\cong C_e$、$e\mid M$。
> **(3)** $\mathrm{ord}(X) = \lvert\Lambda\rvert = M$ で $\langle X\rangle$ が $\Lambda$ に単純推移(⇐ $N_P(H)=H$ + 全分岐)。
> **(4)** 明示 $\mathbb Q$-モデル・$\mathbb Q$-有理な全分岐 cusp・actual marked identification。**$\mathrm{Aut}=1$ だけでは field of moduli $=\mathbb Q$ は出ない**(W5)。
> **(5)** FC-2b/FC-3 による actual Galois 作用と接繊維の比較。
> **(6)** 指定された pushout $q:\mu_M\twoheadrightarrow\mu_e\xrightarrow{\ \sim\ }\mathfrak F_0$ が $\mathfrak F_0$ の $\Lambda$ 上の作用と一致する(**「$\mathfrak F_0$-成分」という語を写像 $q$ というデータに置き換える** — ★教材 4)。
> このとき
> $$ \mathrm{Ih}_N\ \text{全射}\iff q_*[u^{-1}]_M = [u^{-1}]_e\ \text{が}\ H^1(G_K,\mu_e)\ \text{で位数}\ e $$
> であり、全射時の固定体は $K(u^{1/e})$(逆元・$(\mathbb Z/e)^\times$ 乗は同じ体)。
>
> **状態: 定理候補(未証明)。** 本稿は 2 事例で (1)–(6) を個別に構成したにすぎない。**一般証明は将来課題**であり、とくに (6) の「$q$ が存在してかつ作用と一致する」を窓のデータから導く条件は未定式化。

### 5.3 2 適用(同一機械が動くことの確認)

| | **適用 1: $A_5$ 窓** | **適用 2: $K^{(3)}$ 窓** |
|---|---|---|
| $P$ | $A_5$(単純・**非可解**) | $G_3\cong\mathbb F_3^3\rtimes C_2^2\le D_3^3$(位数 108・**可解**) |
| marking / $M$ | $(5,5,5)$ / $M=5$(**素数**) | $(6,6,6)$ / $M=6$(**合成数**) |
| 合同性 | **合同**($\bar N_A=\bar\Gamma(10)$) | **非合同**(K-cong) |
| $\mathfrak F_0$ / $e$ | $C_5$ / $e=M=5$ | $C_3$ / $e=3\mid M=6$ |
| $q$ | 恒等 | $\mu_6\twoheadrightarrow\mu_3$(**3-primary pushout**) |
| dessin | 次数 5・種数 2・$(5,5,5)$・LMFDB `5T4-5_5_5-a` | 次数 6・種数 1・ordered $(6,2^21^2,6)$・LMFDB `6T9-6_6_2.2.1.1-a`(**別正規化**) |
| $u$ | $-1/2\equiv2^4$ | $-4 = -2^2$ |
| 体 | $\mathbb Q(\zeta_5,\sqrt[5]2)$、$\mathrm{Gal}\cong F_{20}$ | $\mathbb Q(\zeta_{12},\sqrt[3]2)$、$\mathrm{Gal}\cong S_3\times C_2$ |

> **★ 論文の骨格案**: 「**比較スキーマ + 2 適用**」。**単純/可解、素数/合成数、合同/非合同という三軸で対極にある 2 窓が同一の手順で決まる**ことが説得力になる。$A_5$ は「なぜ円分だけで足りないか」を、$K^{(3)}$ は「合成数 $M$ で primary 成分をどう分けるか」を与え、**二つ合わせて Conj 5.1 の地形図になる**。
> **ただし論文の主張は「族の定理を証明した」ではなく「2 事例を同一スキーマで実行し、族の定理の前件候補を特定した」**である(便 27 F9 に同意)。

---

## 6. 根基 2 — 観測列プロトコル(便 27 F10 を採用)

現時点の 2 点: $A_5$: $q_*[u] = [2]^4$、$K^{(3)}$: $q_*[u] = [2]^2$。$A_5$ 側の $2$ は古典的に説明がつく($\lambda(\tau)=16q^{1/2}-128q+\cdots$、$16=2^4$)。$K^{(3)}$ は**非合同なので $q$ 展開の説明は使えない**(曲線 54.b3 の導手の台は $\{2,3\}$)。

**2 点は素数/合成数・合同/非合同・非可解/可解の全てで対極にあり、族則を予測する機構はまだない。** ゆえに**予測として登録しない**(cusp-16 の轍)。代わりに:

> **観測列プロトコル**: 新規 $R^{\rm cyc}$ 窓ごとに、$q_*[u]\in K^\times/K^{\times e}$ が $\langle[2]\rangle$ に入るかを**盲検で記録**する。
> **即時棄却規準**: $2$ 以外の素点で valuation が $e$ の倍数でない一例が出れば「根基 2」候補は**即棄却**。
> **昇格条件**: 三つ以上の独立な新規窓で残ってから初めて $\mathrm{(G7_{rad2})}\ q_*[u]\in\langle[2]\rangle$ を予測候補へ上げる。

---

## 7. 【GAP】と状態札

| # | 内容 | 状態 |
|---|---|---|
| ~~【GAP-K3a】~~ | (K4) $\Phi$ 単射 | **閉**(§2.5・便 27 F4・検算 T7) |
| ~~【GAP-20b】~~ | Möbius 正規化不変性 | **閉**(§3・数え方を訂正した上で) |
| ~~C7 / 便 25 F5-2~~ | 3-primary pushout | **閉**(§2.3 修理版) |
| 【GAP-K3b】 | 平面モデルが LMFDB Weierstrass モデル(54.b3)と同じ被覆であることは未検証。**依存していない** | 低 |
| 【GAP-K3c】 | 委嘱 20 §3 の 2 段塔(経路 B・$u$ の第三系統)は未完(【GAP-20a】) | 低 |
| **【状態】** | **紙上(便 27 の必須修正 4 件反映済)**。群論部分($\Lambda$・$\mathfrak F_0$ 作用・$\Phi$ 単射・軌道)は **GAP(`gap18a.json`)と node(本稿 T10)の二系統一致 = `cross-checked`**。解析・算術部分は Opus/Sol の紙上一致(**厳密な blind independence ではない** — §3)。**`verified`(Lean)ではない** | — |

**検算スクリプト**

| ファイル | 内容 | 結果 |
|---|---|---|
| **`search/week4-k3-v2-repairs.mjs`(新規)** | D1 (3.1)(3.6)(4.9)(4.12) から $G_3\le D_3^3$ を自前で再構成。部分群全列挙・$N_G(H)$・$\Lambda$・ordered passport 分裂・**(a′) の stabilizer 同定と v1 の反例構成**・$\lvert\mathrm{Aut}(G_3)\rvert=1296$・Aut-軌道・**12 個の $\Phi_{m,k}$ が自己同型であることと単射性**・$\mathfrak F_0$ の $\Lambda$ 上忠実性・`gap18a.json` との突合 | **43/43** |
| `search/week4-u-k3.mjs` | 臨界方程式・節点・冪級数・$u=-4$・$u'=-256/729$・3-剰余類一致 | 16/16 |
| `search/week4-19a19e.mjs` | Aut-軌道・exact conjugator の存在と一意性 | 7/7 |
| `search/week4-d2d4-k3.mjs` | B1–B5・$\lvert\mathrm{GT}\rvert=12$・$\mathfrak F_0\cong C_3$ | 13/13 |

---

## 8. ★ 教材(便 27 W1–W7 の受領)

1. **【W1・自分が踏んだ】共役部分群の stabilizer は $N_G(H)$、coset の stabilizer は $H$。** 取り違えると「自由に作用する」を無根拠に言ってしまう。**$G_3$ の中に実在する反例を自作した**(T4e)。
2. **【W2・自分が踏んだ】置換の cycle type は部分群を同定しない。** $S_6$ の不動点なし $C_3$ は一意でない。**包含があるなら位数を数える** — 補題 P は $\mathrm{Ih}(G_K)\le\mathfrak F_0$ と両者位数 3 だけで閉じる。**委嘱 14 の★教材「名前は不変量ではない」の再演**。
3. **【W3】「shadow パラメータの一意性」と「有限商への自己同型の単射性」は別問題。** 加えて**その裏面**(「そもそも自己同型か」)も別に検査すべきで、本稿は T7b でそれを塞いだ。
4. **【W4】B2/B3/B5 は窓だけでなく permutation representation ごとの判定。** 次数 12 で FAIL でも次数 6 で PASS しうる。
5. **【W5】$\mathrm{Aut}=1$ は descent 障害を消すが field of moduli $=\mathbb Q$ を単独では与えない。**
6. **【W6】合成数 $M$ では「torsor 全体を推移的にする」と「GT 核の必要な primary 成分を埋める」を区別する。** 本件は $C_3$ を Kummer、$C_2^2$ を円分が埋める。
7. **【W7】経路が異なることと blind independence は同義でない。**
8. **【本稿発】ordered passport は $G$-共役類を分ける不変量である。** $N_G(H)=H$ なる 12 個は $(6,2^21^2,6)$ と $(6,6,2^21^2)$ の二類に割れ、$\mathrm{Aut}(G_3)$ が融合する。**LMFDB との照合で $\lambda$ 割当を揃える必要があった理由はこれ**(§2.2 注)。

---

## 9. 便 28 への論点

1. **§2.3 注 2**: 忠実性を使わない (d′) の短縮は正しいか。忠実性の load-bearing な使用箇所を §2.6 に一本化した依存関係整理に同意するか。
2. **§2.5 の強化**(12 個が実際に $\mathrm{Aut}(G_3)$ の元であることの悉皆検査)は、便 27 F4 が前提にしていた部分を埋めているか。過剰か。
3. **§2.2 注の新事実**(ordered passport による 6+6 分裂)は便 27 F6 P5 の「良い 12 個が一軌道」と整合するが、**$G_3$-共役類としては 2 つ**である。標的クラスの指定を本文で固定した形で問題ないか。
4. **§5.2 $R^{\rm cyc}$ の 6 前件**は必要十分に近いか。とくに (6) の $q$ を「窓のデータから導く条件」を次に定式化すべきか、それとも 3 例目の窓を先に取るべきか。
5. **§6 の観測列プロトコル**の棄却規準($2$ 以外の素点で valuation が $e$ の倍数でない)で十分か。
