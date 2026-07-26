# 定理 K3 — 奇数側 dihedral 窓 $K^{(3)}$ の算術飽和(答案 v1)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 22。両翼一致(収束 10 号)を受けた組み立て。**
入力: `docs/notes/抽出_Kn定義_D1.md`(正典・逐語)・`docs/week4-A5算術飽和_v4.md` §1(窓非依存部品)・委嘱 18/19/20/21(自作)・`sol/sol_reply_25_u_k3.md`(便 25・開示済)・`certificates/k3/gap18a.json`・`docs/scout/scout_20260726_6t9_requery.md`。
検算: `search/week4-u-k3.mjs`(**16/16**)・`search/week4-19a19e.mjs`(**7/7**)・`search/week4-d2d4-k3.mjs`(**13/13**)。
**状態: 紙上・両翼独立一致・Sol 総合監査(便 27)未了。`cross-checked` でも `verified` でもない。**

---

## 0. 主定理

> ### 定理 K3
> $K^{(3)} = \ker\psi_3 \in \mathrm{NFI}_{PB_3}(B_3)$(D1 (3.1))とする。このとき
> $$ \boxed{\ \mathrm{Ih}_{K^{(3)}}:\ G_{\mathbb Q}\ \twoheadrightarrow\ \mathrm{GT}(K^{(3)})\ \cong\ \mathrm{Aff}(\mathbb Z/3)\times\mathcal Z_2\ \cong\ S_3\times C_2\quad(\text{位数 }12) $$
> は**全射**であり、$\ker(\Phi\circ\mathrm{Ih}_{K^{(3)}})$ の固定体は
> $$ \boxed{\ L_3\ =\ \mathbb Q\bigl(\zeta_{12},\ \sqrt[3]{2}\bigr),\qquad [L_3:\mathbb Q] = 12,\qquad \mathrm{Gal}(L_3/\mathbb Q)\ \cong\ S_3\times C_2\ } $$
> である。したがって $\mathrm{GT}(K^{(3)})$ の 12 元すべてが arithmetical、ゆえに genuine。

**体の同定**: $u = -4$ の立方剰余類は $[-4]_3 = [4]_3 = [2^2]_3$ で、$\mathbb Q(\zeta_{12},\sqrt[3]{-4}) = \mathbb Q(\zeta_{12},\sqrt[3]{4}) = \mathbb Q(\zeta_{12},\sqrt[3]{2})$($\sqrt[3]4 = (\sqrt[3]2)^2$ かつ $\sqrt[3]2 = (\sqrt[3]4)^2/2$)。
$\mathrm{Gal}$ の同定: $(\mathbb Z/12)^\times = \{1,5,7,11\}\cong C_2\times C_2$ が $\mu_3$ に mod 3 成分で作用し、$\{1,7\}$ は自明・$\{5,11\}$ は反転。ゆえに $\mathrm{Gal}(L_3/\mathbb Q)\cong C_3\rtimes(C_2\times C_2) \cong (C_3\rtimes C_2)\times C_2 = S_3\times C_2$ ✓ — **$\mathrm{GT}(K^{(3)})\cong\mathrm{Aff}(\mathbb Z/3)\times\mathcal Z_2$(D1 §4 Thm 4.6 (4.23), $n_0=3,\alpha=0$)と同型** ✓。

> **★ $A_5$ との並び**: $A_5$ 窓は $L = \mathbb Q(\zeta_5,\sqrt[5]2)$、$\mathrm{Gal}\cong F_{20}\cong\mathrm{GT}(N_A)$。$K^{(3)}$ 窓は $L_3 = \mathbb Q(\zeta_{12},\sqrt[3]2)$、$\mathrm{Gal}\cong S_3\times C_2\cong\mathrm{GT}(K^{(3)})$。**両方とも $\mathbb Q(\zeta_{2M},\sqrt[e]{2})$ 型で、根基が $2$**(§6 の観察)。

---

## 1. 仮定リスト(A₅ v4 方式で最小化)

| # | 内容 | 状態 |
|---|---|---|
| **(K1)** | $K^{(3)}$ は **isolated** | **source-closed**。D1 §4 逐語: Thm 4.3 末尾 "**Furthermore, $K^{(n)}$ is an isolated object of the groupoid GTSh**"(全 $n\ge3$)。⇒ $\bar K^{(3)}$ は $G_{\mathbb Q}$-安定、$\mathrm{Ih}$ は準同型 |
| **(K2)** | $\lvert\mathrm{GT}(K^{(3)})\rvert = 12$、$\tilde\chi:\mathrm{GT}\to(\mathbb Z/12)^\times$ の核 $\mathfrak F_0\cong C_3$ | **source-closed**。D1 §4 の Thm 4.3 (4.12)+(4.9) から直接列挙($\mathcal X_3=\{0,2,3,5\}$、$k$ は $\bmod\ \mathrm{ord}(r^2)=3$)。検算 `week4-d2d4-k3.mjs` (D2-B4) |
| **(K3‡)** | $\mathrm{Ih}$ が定める作用は正準 outer Galois 作用 $\rho$ の $\hat F_2'$-正規化持ち上げ | **A₅ v4 §1.4.4 の補題 I3‡ をそのまま import**(窓に依らない・2405 p.4 の splitting 文 + reader 照合済の表示式 + ĜT_gen 定義) |
| **(K4)** | $\Phi:\mathrm{GT}(K^{(3)})\to\mathrm{Aut}(G_3)$ が単射 | Thm 4.3 のパラメータ表示 $(m,(r^{2k},r^{-2k},r^{\kappa(m)}))$ が $(m,k)$ を一意に決めることから。**紙上**⇒【GAP-K3a】 |

> **⇒ (K1)(K2) は正典から source-closed、(K3‡) は $A_5$ で支払い済み、(K4) だけが紙上。** $A_5$ v4 の「未閉鎖仮定は (I1)(I2) のみ」と同じ水準に達している。

---

## 2. 比較鎖(窓非依存の import + $K^{(3)}$ 固有部品)

### 2.1 窓非依存部品(A₅ v4 §1 から**そのまま** import — 再証明不要)

| 部品 | 内容 | 出所 |
|---|---|---|
| **補題 C** | 標準実経路 $p\subset(0,1)$ の Galois path cocycle は $[\hat F_2,\hat F_2]^{\rm top.cl.}$ に入る(二つの Kummer 被覆 $w^n=\beta$・$u^n=1-\beta$ の両端 Galois 不動点 + 正実分枝の解析接続) | v4 §1.4.2 |
| **補題 D0** | $C_{\hat F_2}(x) = \overline{\langle x\rangle}$(ZZ Prop 4.7 + Lemma 4.2 + 初等補足 / 自由副有限積の二重装甲) | v4 §1.4.3a |
| **補題 D・系 E** | $\hat F_2'$-正規化持ち上げの存在と一意性 ⇒ $\alpha^{\rm std} = \alpha^{\rm norm}$ | v4 §1.4.3b |
| **補題 I3‡** | $\alpha^{\rm Ih} = \alpha^{\rm norm}$ ⇒ **$\alpha^{\rm Ih} = \alpha^{\rm std}$**(= FC-2b) | v4 §1.4.4 |
| **FC-3** | $\Lambda := \{H\text{ の }\hat F_2\text{-共役}\}\xrightarrow{\sim}\mathrm{Fib}_{\vec{01}}(W_0)$、$p\mapsto\mathrm{Stab}_{\hat F_2}(p)$、$G_{\mathbb Q}$-同型 | v4 §3.3(**次数 $d$ に依らない**) |
| **局所 Kummer 計算** | 全分岐点で $\lambda = u\,s^M$ ⇒ 接繊維の類は $[u^{-1}]\in\mathbb Q^\times/(\mathbb Q^\times)^M$ | v4 §3.5 |

> **★ 族化の最大の利得**: **最も高価だった絶対較正(補題 C+D0+D+I3‡)は $\lambda$-線だけの命題で、窓に一切依存しない。** $A_5$ で一度支払えば $K^{(3)}$ では無料。**便 25 F5 も同じ整理**(独立一致)。

### 2.2 $K^{(3)}$ 固有部品

| 部品 | 内容 | 出所 | 検算 |
|---|---|---|---|
| **(P1) 表現の選択** | **次数 6・非忠実**($\mathrm{monodromy} = G_3/\mathrm{core}\cong S_3\times S_3$ = 6T9・核 3)。忠実次数 12 は使わない | 委嘱 19 §A | — |
| **(P2) B1–B5** | B1 PASS(核一意: 生成対 1296/$\lvert\mathrm{Aut}(G_3)\rvert$ 1296)・**B2 PASS**($\mathrm{Aut}(\text{dessin})=1$)・B3 PASS(全分岐)・B4 PASS($\mathfrak F_0$ 巡回)・**B5 実質 moot**(決着は 3-部分・3 は素数) | 委嘱 18 §2 | 13/13 |
| **(P3) 一意性** | $\mathrm{Aut}(G_3)$-軌道 1 つ(cent = 1 の $H$ が 12 個で 1 軌道) | 委嘱 20 §2 | 7/7 |
| **(P4) marked 同定** | **exact conjugator** $h = [6,1,5,4,2,3]$、$h\bar xh^{-1}=\sigma_1$, $h\bar yh^{-1}=\sigma_\infty$, $h\bar zh^{-1}=\sigma_0$。**$h$ は $S_6$ 内で一意・三本目は独立検査** | 委嘱 21 §1 | 7/7 |
| **(P5) 分岐構造** | $F = t^2+(x-1)^2(4x-1)t+4x^6$ の分岐点は $\{0,-1,\infty\}$、型 $[6],[2^21^2],[6]$。$x=1/3$ は**節点**($F=F_x=F_t=0$) | 委嘱 21 §2 | 16/16 |
| **(P6) 接方向 rigidification(補題 B2′)** | 印付き点 $p$ とその接ベクトルを込めた三つ組の自己同型は自明。**次数 6 では $\lambda=0$ 上が 1 点ゆえ実質不要**だが、一般論として保持 | 委嘱 18 §4.2 | — |
| **(P7) 残留 descent なし** | 平面モデルと写像は $\mathbb Q$ 上・$\lambda=0$ 上は唯一点 $P_0=(0,0)$ で $G_{\mathbb Q}$-固定・$x$ は $\mathbb Q$-有理 uniformizer・$\mathrm{Aut}=1$ で twist なし | 委嘱 21 §3、**便 25 F5 と独立一致** | 16/16 |

### 2.3 ★ 3-primary pushout(便 25 F5「新たに要るもの 2」= 私の C7 の具体形)

**これが両翼の残条件の実質であり、以下で閉じる。**

> **補題 P(3-primary pushout).** 記号: $\Lambda$ = $H$ の共役集合(6 元)、$M = K_{\rm ord}^{(3)} = 6$、$K = \mathbb Q(\zeta_{12})$。
> **(a)** $H\cap\langle\bar x\rangle = 1$ かつ $\lvert\Lambda\rvert = 6 = \mathrm{ord}(\bar x)$(B3)より、**$\langle\bar x\rangle\cong C_6$ は $\Lambda$ に単純推移的に作用する** ⇒ $\Lambda$ は $C_6$-torsor。
> **(b)** FC-3 + 局所 Kummer 計算より、$G_K$ 上では線形部が消え($\chi\equiv1\bmod12$)、$\Lambda$ 上の作用は**平行移動のみ**で、その像は $[u^{-1}]\in K^\times/(K^\times)^6$ の生成する巡回群。
> **(c)** $u = -4$、$K = \mathbb Q(\zeta_{12})$ では $-1 = \zeta_{12}^6$ が 6 乗ゆえ $[-4] = [2^2]$。$\sqrt2\notin K$($8\nmid12$)、$\sqrt[3]2\notin K$(次数 3 ∤ 4・非アーベル)より **$[2]$ の位数は 6**、ゆえに **$[2^2]$ の位数は $6/\gcd(6,2) = 3$**。
> **⇒ $\Phi(\mathrm{Ih}(G_K))$ の $\Lambda$ 上の像は、単純推移的 $C_6$ の位数 3 の部分群**(= 不動点なしの 3-サイクル 2 個)。
> **(d)** 【GAP-18a】より **$\mathfrak F_0\cong C_3$ は $\Lambda$ 上に忠実に、不動点なしの 3-サイクル 2 個として作用する**。位数 3 の部分群は $C_6$ に一意だから、(c) の像と (d) の $\mathfrak F_0$ の像は**同一**。
> **(e)** $\tilde\chi(G_K) = 1$ より $\Phi(\mathrm{Ih}(G_K))\subseteq\Phi(\mathfrak F_0)$、かつ $\mathfrak F_0$ は $\Lambda$ 上忠実((d))だから $\Phi(\mathfrak F_0)\hookrightarrow\mathrm{Sym}(\Lambda)$ は単射。(c)(d) と合わせて
> $$ \boxed{\ \Phi\bigl(\mathrm{Ih}_{K^{(3)}}(G_K)\bigr) = \Phi(\mathfrak F_0)\cong C_3\ } $$

**便 25 F5-3(generator の向き)について**: actual marking の逆向き規約は $[u]_3\leftrightarrow[u]_3^{-1}$ を起こしうるが、**「自明か位数 3 か」の判定は反転で不変**(便 25 と同意見)。§0 の体 $L_3$ も $\mathbb Q(\zeta_{12},\sqrt[3]{4}) = \mathbb Q(\zeta_{12},\sqrt[3]{2})$ で反転不変 ✓。

### 2.4 主定理の証明

1. (K1) より $\bar K^{(3)}$ は $G_{\mathbb Q}$-安定 ⇒ $\beta:G_{\mathbb Q}\to\mathrm{Aut}(G_3)$ が定義され、$\beta_\gamma(\bar x) = \bar x^{\chi(\gamma)}$。
2. (K3‡) + 補題 C/D0/D/系 E より $\alpha^{\rm Ih} = \alpha^{\rm std}$(FC-2b)⇒ $\beta = \Phi\circ\mathrm{Ih}_{K^{(3)}}$。
3. $\beta_\gamma(\bar x) = \bar x^{\chi(\gamma)}$ より合成 $G_{\mathbb Q}\to\mathrm{GT}\xrightarrow{\tilde\chi}(\mathbb Z/12)^\times$ は **mod 12 円分指標**で全射 ⇒ $4\mid\lvert\mathrm{im}\rvert$。
4. **補題 P** より $\Phi(\mathrm{Ih}(G_K)) = \Phi(\mathfrak F_0)\cong C_3$ ⇒ $3\mid\lvert\mathrm{im}\rvert$。
5. $\lvert\mathrm{GT}(K^{(3)})\rvert = 12$(K2)と $3,4\mid\lvert\mathrm{im}\rvert$ ⇒ $\lvert\mathrm{im}\rvert = 12$ ⇒ (K4) の $\Phi$ 単射より $\mathrm{Ih}_{K^{(3)}}(G_{\mathbb Q}) = \mathrm{GT}(K^{(3)})$。
6. 固定体: $\beta_\gamma = \mathrm{id}\iff\chi(\gamma)\equiv1\ (12)$ かつ $\Lambda$ 上自明 $\iff\gamma$ が $\zeta_{12}$ と $\sqrt[3]{2}$ を固定 $\iff\gamma\in G_{L_3}$。∎
7. arithmetical ⇒ genuine は $G_{\mathbb Q}\hookrightarrow\widehat{GT}$ から(2405 §1.3.1)。

---

## 3. $u$ の抽出 — 両翼併記

| | **Opus(委嘱 21)** | **Sol(便 25)** |
|---|---|---|
| 経路 | 平面モデルの**分岐構造を自前確定**(臨界方程式 $(3x-1)^2(2x^2-2x+1)$・節点 $x=1/3$・$t=-1$ の 2 根)→ $\lambda = -t$ → 冪級数 | 平面モデルの**局所展開のみ** |
| 主係数 | $t = 4x^6+24x^7+\cdots$ ⇒ **$u = -4$** | **$u = -4$** |
| 基礎体 | $\mathbb Q(\zeta_{12})$(**事前固定**・W149) | $\mathbb Q(\zeta_{12})$(**事前固定**) |
| 類 | $[u]_3 = [2^2]\ne1$ | $[u^{-1}]_3 = [u]_3^{-1}\ne1$(**逆元表記・判定同値**) |
| 正規化不変性 | **$t=\infty$ 側も展開**: $y=-\frac89Z^2$, $v = \frac{256}{729}Z^6$ ⇒ $u' = -\frac{256}{729} = -\frac{2^8}{3^6}$、$[u']_3 = [2^{8\bmod3}3^{-6\bmod3}] = [2^2]$ ✓**一致** | — |
| 判定 | **飽和側** | **飽和側** |

> **★ 相補性**: Sol は局所計算に集中、私は**分岐構造の自前確定・正規化不変性・exact conjugator** を担当。**便 25 F4.1 の条件 3(marked identification)は「exact conjugator を独立計算していない」と明記されており、私の (P4) がそれを供給する。** 逆に便 25 F4 の $[u^{-1}]$ という**向きの明示**は私の記述より正確で、採用した。

**【GAP-20b】の射程**: $A_5$ 戦は「Möbius 6 通り」で不変性を確認したが、本件は**2 通り**(二つの $[6]$ 点)のみ。残り 4 通りは $\lambda=1$($[2^21^2]$)を $0$ に置く正規化で、**そこは全分岐でないので $u$ の定義域外**(委嘱 13 の B3)。**⇒ 意味のある正規化は 2 通りで尽き、両方で一致した。**【GAP-20b】閉鎖。

---

## 4. 残条件の和集合(便 27 監査の的)

**両翼の条件リストを突合した結果、残るのは下記のみ。**

| # | 条件 | Opus §5 | 便 25 F4.1/F5 | 現状 |
|---|---|---|---|---|
| 1 | isolated | C1 | 1 | **閉**(正典 Thm 4.3) |
| 2 | $\mathfrak F_0\cong C_3$・$\tilde\chi$ 円分 | C2 | 2 | **閉**(正典 Thm 4.3) |
| 3 | **marked identification**(6T9 被覆 = 選んだ $H$ の被覆) | C5 の一部 | **3(Sol は未計算と明記)** | **閉**(私の exact conjugator (P4)) |
| 4 | $\Lambda$ 上で $\mathfrak F_0$ 忠実 | C4 | 4 | **閉**(【GAP-18a】) |
| 5 | 補題 C/D0/D/E/I3‡ | C3 | 5 | **閉**($A_5$ v4・窓非依存) |
| 6 | 残留 descent なし | C6 | F5「残留 descent」 | **閉**(両翼独立一致) |
| 7 | **3-primary pushout** | **C7** | **F5-2** | **本稿 §2.3 補題 P で閉** |
| 8 | generator の向き | — | F5-3 | **無害**(判定は反転不変) |
| 9 | $\Phi$ の単射性 | — | — | **紙上**⇒【GAP-K3a】 |

> **⇒ 残る未閉鎖は【GAP-K3a】($\Phi$ 単射・紙上)のみ。** $A_5$ v4 の【GAP-C6】と同水準。

---

## 5. ★ 定理 R^gen の 2 事例として(論文構成の骨格)

> ### 定理 R^gen(族の定理・起案)
> $N$ を許容対象、$c\in N$、$P = F_2/\bar N$、marking $(X,Y,Z)$、$M := N_{\rm ord}$、$K := \mathbb Q(\zeta_{2M})$ とする。次を仮定:
> **(T1)** $N$ は isolated;**(T2)** $\Phi:\mathrm{GT}(N)\to\mathrm{Aut}(P)$ は単射;
> **(T3)** 部分群 $H\le P$ が存在して (a) $\langle\bar X\rangle$ が $\Lambda := \{H\text{ の共役}\}$ に**単純推移**、(b) $\mathrm{Aut}(\text{dessin}) = 1$、(c) $\lambda=0$ 上が 1 点(全分岐)、(d) $\mathfrak F_0$ が $\Lambda$ 上**忠実**。
> このとき、$\lambda = u\,s^M(1+O(s))$($s$ は $P_0$ の $\mathbb Q$-有理 uniformizer)で定まる $u\in\mathbb Q^\times$ について
> $$ \boxed{\ \mathrm{Ih}_N\ \text{全射}\iff [u]\in K^\times/(K^\times)^M\ \text{の}\ \mathfrak F_0\text{-成分が}\ \mathfrak F_0\ \text{を生成する}\ } $$
> であり、そのとき $\ker(\Phi\circ\mathrm{Ih}_N)$ の固定体は $\ K\bigl(u^{1/e}\bigr)$($e = \lvert\mathfrak F_0\rvert$)。

**2 適用**:

| | **適用 1: $A_5$ 窓**(定理 A₅) | **適用 2: $K^{(3)}$ 窓**(定理 K3) |
|---|---|---|
| $P$ | $A_5$(単純・**非可解**) | $G_3\le D_3^3$(位数 108・**可解**) |
| marking / $M$ | $(5,5,5)$ / $M=5$(**素数**) | $(6,6,6)$ / $M=6$(**合成数**) |
| 合同性 | **合同**($\bar N_A = \bar\Gamma(10)$) | **非合同**(K-cong) |
| $\mathfrak F_0$ | $C_5$ | $C_3$ |
| dessin | 次数 5・種数 2・$(5,5,5)$・LMFDB `5T4-5_5_5-a` | 次数 6・種数 1・$(6,2^21^2,6)$・LMFDB `6T9-6_6_2.2.1.1-a` |
| $u$ | $-1/2\equiv 2^4$(= 古典 $\lambda = 16q^{1/2}$ の主係数) | $-4 = -2^2$ |
| 体 | $\mathbb Q(\zeta_5,\sqrt[5]2)$、$\mathrm{Gal}\cong F_{20}$ | $\mathbb Q(\zeta_{12},\sqrt[3]2)$、$\mathrm{Gal}\cong S_3\times C_2$ |
| 帰結 | 単純群窓の算術飽和・初例 | **奇数側 dihedral の最初の標的**(Conj 5.1 直撃) |

> **★ 論文の骨格案**: 「**族の定理 R^gen + 2 適用**」。**単純/可解、素数/合成数、合同/非合同という三つの軸で対極にある 2 窓が同一の機械で決まる**ことが、族の定理の説得力になる。$A_5$ 側は「なぜ dihedral では円分だけで足りるのか」の機構的説明(v1 §1.4)を、$K^{(3)}$ 側は「奇数側でも非円分が要る」ことを与え、**二つ合わせて Conj 5.1 の地形図になる**。

---

## 6. 観察(定理ではない)— 根基がどちらも $2$

$A_5$: $u\equiv2^4$、体 $\mathbb Q(\zeta_5,\sqrt[5]2)$。$K^{(3)}$: $u = -2^2$、体 $\mathbb Q(\zeta_{12},\sqrt[3]2)$。**どちらも $\sqrt[e]{2}$**。
$A_5$ 側の $2$ は**古典的**に説明がついた($\lambda(\tau) = 16q^{1/2}-128q+\cdots$ の主係数 $16 = 2^4$・委嘱 13 §1.5)。**$K^{(3)}$ は非合同なので $q$ 展開の説明は使えない**が、LMFDB 曲線は **54.b3(導手 $54 = 2\cdot27$)** で台は $\{2,3\}$、$u = -4$ の 3-部分が $[2^2]$。
> **⇒ 問い(次の共同設計テーマ)**: **「$u$ の根基が $2$ になるのは偶然か、$\lambda$-線の $2$ への分岐に由来する構造か。」** 委嘱 13 §5 Q6 の一般化。**予測として登録しない**(cusp-16 の轍)。

---

## 7. 【GAP】と状態札

| # | 内容 | 状態 |
|---|---|---|
| **【GAP-K3a】** | (K4) $\Phi$ の単射性は紙上(Thm 4.3 のパラメータ表示が $(m,k)$ を一意に決めることから)。$A_5$ の【GAP-C6】と同水準 | 中 |
| 【GAP-K3b】 | 平面モデルが LMFDB の Weierstrass モデル(54.b3)と同じ被覆であることは未検証。**依存もしていない**($\mathrm{Aut}=1$ ゆえどの ℚ-モデルでも $u$ は同じ) | 低 |
| 【GAP-K3c】 | 委嘱 20 §3 の 2 段塔(経路 B・独立第三系統)は未完(【GAP-20a】)。**経路 A が両翼で決着したため優先度低下**だが、$u$ の三系統化として価値は残る | 低 |
| ~~【GAP-20b】~~ | **閉**(§3: 意味のある正規化は 2 通りで尽き、両方で $[u]_3 = [2^2]$) | — |
| ~~C7 / 便 25 F5-2~~ | **閉**(§2.3 補題 P) | — |
| **【状態】** | **紙上・両翼独立一致(収束 10 号)・Sol 総合監査(便 27)未了**。検算は node 独立実装で 16/16 + 7/7 + 13/13。**`cross-checked`(機械二系統)でも `verified`(Lean)でもない** | — |

**検算スクリプト**

| ファイル | 内容 | 結果 |
|---|---|---|
| `search/week4-u-k3.mjs` | 臨界方程式の因数分解・節点判定・$t=-1$ の 2 根・RH・$t=4x^6+24x^7$ の冪級数・$u=-4$・$t=\infty$ 側の $u'=-256/729$・3-剰余類の一致 | **16/16** |
| `search/week4-19a19e.mjs` | $\mathrm{Aut}(G_3)$-軌道一意・exact conjugator の存在と一意性・ブロック構造 | **7/7** |
| `search/week4-d2d4-k3.mjs` | 便 23 の (0.1)(0.2)(0.3) 検分・B1–B5 判定・$\lvert\mathrm{GT}\rvert=12$・$\mathfrak F_0\cong C_3$ | **13/13** |

**便 25 の数値の再現**: $u = -4$ ✓(独立経路)、$[u]_3\ne1$ ✓、$\mathbb Q(\zeta_{12})$ 事前固定 ✓、$[u^{-1}]_3 = [u]_3^{-1}$ の向き ✓(採用)。

---

## 8. 便 27(総合監査)への論点

1. **補題 P(§2.3)**が本稿の新規部分。とくに (c)(d) から「位数 3 の部分群は $C_6$ に一意」で像を同定する段。
2. **残条件の和集合(§4)**が正しく尽くされているか。とくに **9(Φ 単射)以外に未閉鎖はないか**。
3. **定理 R^gen(§5)の言明**が 2 事例を正しく包摂しているか。とくに (T3)(d)(忠実性)を前件に入れたのは $K^{(3)}$ の非忠実表現を許すためだが、$A_5$ でも成立しているか($\mathrm{Aut}(A_5)$ が $\Lambda$ に忠実 ✓)。
4. §6 の観察を**予測として登録しない**という判断の当否。
5. 固定体 $L_3 = \mathbb Q(\zeta_{12},\sqrt[3]2)$ と $\mathrm{Gal}\cong S_3\times C_2 \cong \mathrm{GT}(K^{(3)})$ の同型の突合(D1 Thm 4.6 (4.23) との整合)。
