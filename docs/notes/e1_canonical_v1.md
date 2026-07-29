# E1 正典統合 v1 — 中間峰 GT^odd_Dih と壁の窓族を単一語彙で

**状態札: candidate / 研究内部文書**(論文ではない。論文起草は研究者発意事項 — 2026-07-30 確認。発表保留とは無関係の整理仕事)
作成: 数学者(Opus 5)・2026-07-30(レーン D 繰り上げ・発案係 I9-3 / 司令塔追認)
記法: 正典 arXiv **2401.06870**(GTSh の定義正本)/ **2405.11725**(dihedral 予想 Conj 5.1・$K^{(n)}$ 族・Thm 4.3/4.6)準拠。定義の工房内正本は `docs/week1-定義ノート.md`。
**封印量・$K^{(5)}$ 非接触。**

---

## 0. この文書の位置づけと射程

**なぜ今か**(発案係 I9-3 の論拠・司令塔追認): 壁側の Hol 同定(裁定 211/213/220 — $\mathrm{GTSh}\cong\mathrm{Syl}_2\times\mathrm{Hol}$、$S4=\mathrm{PSL}(2,8)$ 窓も $\mathrm{Hol}(\mathbb Z/9)$)により、**中間峰(dihedral 族)と壁(D4/E 族)が同一の語彙で書けるようになった**。その語彙は §3 で示すとおり **正典 Thm 4.6 の $\mathrm{Aff}$ そのもの**であり、新語ではない。

**射程(委嘱どおり 3 点)**:
1. 中間峰 $\mathrm{GT}^{\rm odd}_{\rm Dih}$ の 4 点セット(isolated 既知・構造・同値・忠実実現)の statement 統合 → §2
2. 窓族の統一表(dihedral 族 / D4 族 / E 族 / PSL 窓) → §4
3. 未解決の名指し → §5

**射程外(明示)**: 証明の再掲はしない(各主張は出典を指す)。新しい定理は主張しない。**本文書は統合であって前進ではない** — ただし §3 の語彙同定は既存の主張の**再記述**として新しい(§6 で新規性を申告)。

---

## 1. 正典の記法(必要最小限の再掲)

`docs/week1-定義ノート.md` §1–§3 から、本文書で使うものだけを引く。

- $B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle$、$PB_3=\ker(\rho:B_3\to S_3)$、$x:=\sigma_1^2$、$y:=\sigma_2^2$、$\Delta:=\sigma_1\sigma_2\sigma_1$、$c:=\Delta^2$。$PB_3\cong F_2\times\langle c\rangle$、$F_2=\langle x,y\rangle$。
- $\theta,\tau\in\mathrm{Aut}(F_2)$: $\theta=(x\leftrightarrow y)$(位数 2)、$\tau: x\mapsto y\mapsto z\mapsto x$(位数 3)。**$F_2$ の外側では $B_3/Z\cong PSL_2(\mathbb Z)\cong C_2*C_3$ の二つの捻れ生成元に対応**。
- $N\in\mathrm{NFI}_{PB_3}(B_3)$ に対し $N_{\rm ord}:=\mathrm{lcm}(\mathrm{ord}(xN),\mathrm{ord}(yN),\mathrm{ord}(cN))$ (3.1)、$N_{F_2}:=N\cap F_2$ (3.2)。
- **GT-shadow**(Def 3.7)= charming GT-pair + 全射性。合成 (3.53):
 $$[m_1,f_1]\circ[m_2,f_2]=[\,2m_1m_2+m_1+m_2,\ f_1E_{m_1,f_1}(f_2)\,],\qquad E_{m,f}(x)=x^{2m+1},\ E_{m,f}(y)=f^{-1}y^{2m+1}f.$$
- **$u:=2m+1$ は乗法的** (3.49)。$\chi_{\rm vir}([m,f])=2m+1 \bmod N_{\rm ord}$。工房の記号 $\tilde\chi$ はこれ(定義ノート §2)。
- **settled** = $\ker(T_{m,f})=N$。**isolated** = 全 shadow が settled $\Rightarrow$ $\mathrm{GT}(N)=\mathrm{GTSh}(N,N)$ は有限群(Prop 3.14)。
- **dihedral poset**(2405 §3): $\psi_n:PB_3\to D_n^3$、$K^{(n)}:=\ker\psi_n$、$\mathrm{Dih}:=\{K^{(n)}\mid n\ge3\}$、$G_n:=\mathrm{Im}\,\psi_n$。$K_{\rm ord}=\mathrm{lcm}(n,2)$、$K^{(n)}=K^{(2n)}$($n$ 奇)。
- **正典 Thm 4.6**(群構造・$n=2^\alpha n_0$、$n_0$ 奇):
 $$\mathrm{GT}(K^{(n)})\cong\begin{cases}\mathrm{Aff}(\mathbb Z/n_0\mathbb Z)\times\mathcal Z_2 & (\alpha\le1)\\[2pt] \mathrm{Aff}(\mathbb Z/n_0\mathbb Z)\times\widetilde H_\alpha & (\alpha\ge2)\end{cases}
 \qquad
 \lvert\mathrm{GT}(K^{(n)})\rvert=\begin{cases}2n_0\varphi(n_0)&(\alpha\le1)\\ n_0\varphi(n_0)\,2^{2\alpha-2}&(\alpha\ge2)\end{cases}$$
 (Sol が独立再導出済み・一致。定義ノート §3)
- **Conj 5.1(dihedral 予想)**: $\mathrm{Dih}$ の全対象 $K$ で全 GT-shadow が arithmetical(= $\mathrm{Ih}_K:G_{\mathbb Q}\to\mathrm{GTSh}(K,K)$ 全射)。証明済みは **$n=2^\alpha$($\alpha\ge2$)のみ**(Thm 5.3)。

---

## 2. 中間峰 $\mathrm{GT}^{\rm odd}_{\rm Dih}$ — 4 点セットの統合 statement

**中間峰の定義**: dihedral 族の **odd 側**、すなわち $\alpha\le1$($n$ 奇、または $n=2\cdot$奇。$K^{(n)}=K^{(2n)}$ より正規化代表は $n$ 奇)に限定した井原問題。

> ### 【E1-1】isolated(正典既知)
> $K^{(n)}\in\mathrm{Dih}$ は **isolated**(2405 Thm 4.3 の帰結・定義ノート §3)。ゆえに
> $$\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})\quad\text{は有限群}.$$
> **状態: 正典の定理**(工房の主張ではない)。
> **注意(Sol 注記・定義ノート §3)**: $\mathrm{GTSh}(K,K)=\mathrm{GT}(K)$ と書けるのは Thm 4.3 が $K\in\mathrm{Dih}$ の isolated 性を証明しているからであり、**一般の $N$ に安易に一般化してはならない**。

> ### 【E1-2】構造
> $\alpha\le1$ のとき正典 Thm 4.6 より
> $$\boxed{\ \mathrm{GT}(K^{(n)})\ \cong\ \mathrm{Aff}(\mathbb Z/n_0\mathbb Z)\times\mathcal Z_2\ },\qquad \lvert\cdot\rvert=2n_0\varphi(n_0).$$
> 副有限極限(isolated poset は cofinal・2401 Thm 5.2)を取ると
> $$\mathrm{GT}^{\rm odd}_{\rm Dih}\ \cong\ \mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2 .$$
> **状態: 有限段は正典の定理。極限の形は工房の統合(§6 参照)。**

**E1-2 の自然座標**(Sol 便 75 §F6.2(b)・紙上 PASS): 奇 $n$ の shadow を $(m,k)$ とし $u:=2m+1\bmod n$、$\varepsilon:=m\bmod2$ と置くと Thm 4.3/(4.18) の積は
$$(k_1,u_1,\varepsilon_1)\cdot(k_2,u_2,\varepsilon_2)=(k_1+u_1k_2,\ u_1u_2,\ \varepsilon_1+\varepsilon_2),$$
すなわち $\mathrm{GT}(K^{(n)})\xrightarrow{\sim}\mathrm{Aff}(\mathbb Z/n)\times C_2$ は**自然**な同型で、外部 $C_2$ は $\chi_4$。reduction $(k,u,\varepsilon)\mapsto(k\bmod d,u\bmod d,\varepsilon)$ は $C_2$ 成分を捻らない。極限側は $\varprojlim\mathcal Z_2$ が**遷移恒等の定数系**ゆえ単に $C_2$(同 §F6.2(c))。

> ### 【E1-3】同値 — **odd Conj 5.1 $\iff$ $\mathrm{Ih}^{\rm odd}$ 全射**
> $$\boxed{\ \text{odd Conjecture 5.1}\iff \mathrm{Ih}^{\rm odd}:G_{\mathbb Q}\to\mathrm{GT}^{\rm odd}\ \text{が全射}\ }$$
> **証明の骨(Sol 便 75 §F6.2(d))**: ($\Rightarrow$)は明らか。($\Leftarrow$)は**コンパクト性** — 全有限段が全射なら像はコンパクトゆえ閉。逆極限の basic open は有限個の段しか指定しないので、その lcm 段 $N$ に持ち上げ $\mathrm{Ih}_N$ の全射性で hit できる。よって像は稠密かつ閉、ゆえに全体。
> **⚠ 前件の明記(原文)**: 「ここで必要なのは**全有限段の arithmetic surjectivity** であり、遷移写像の全射性だけから Galois 像の全射性が出るわけではない。」
> **状態: Sol 検分済(紙上 PASS)**(便 75 §6 総括・裁定 111)。
> **これが 4 点セットの「同値」の正体である** — 中間峰を「有限段の井原問題の族」として一括化する装置。

> ### 【E1-4】忠実実現(**framed 対象**上・型修理済)
> **命題 Φ-fam**(`docs/notes/phifam_v1.md` §2): 全奇数 $n\ge3$ で
> $$\Phi_n:\ \mathrm{GT}(K^{(n)})\ \hookrightarrow\ \mathrm{Aut}(G_n),\quad [m,f]\mapsto\bigl(X\mapsto X^u,\ Y\mapsto F^{-1}Y^uF\bigr)\qquad(\textbf{共変}\cdot\text{単射}\cdot\ker\Phi_n=\{[0,1]\}).$$
> 逆極限で $\Phi^{\rm odd}:\mathrm{GT}^{\rm odd}_{\rm Dih}\hookrightarrow\mathrm{Aut}_{\rm cont}(G^{\rm odd})$、$G^{\rm odd}=\varprojlim G_n=(\widehat{\mathbb Z}^{\rm odd})^3\rtimes Q$。前件 P1–P5 は `phifam_v1.md` §5 に全列挙(P1 = 便 75 F6.2 の**引用**・同稿は再証明していない)。
>
> **⚠ 型修理(Sol 便 77 F77-3.6・裁定 138 で採択)**: 結論を「marked dessin の自己同型」と幾何語で書くのは不正確。正しくは
> $$\text{$G^{\rm odd}$ と、その compatible ordered generating-pair(framing)の \textbf{torsor} 上の忠実な連続作用}$$
> であり、対象は **$\mathcal D^{\rm odd}_{\rm frame}=(G^{\rm odd},\mathrm{Fr}(G^{\rm odd}))$**(P77-2)。codomain も抽象 `Aut` でなく $\mathrm{Aut}_{\rm cont}$ と書く。
> **⚠ 旧対象は閉じていない**: $H^{\rm fun}$ coset 塔上の忠実作用は**依然 UNKNOWN**(便 75 F6.2(e) の三条件は未証明)。今回の正則対象は**代替閉鎖**であって旧対象の解決ではない。
> **⚠ marked/framed 限定は本質**(FINDING Φ1): $\Phi_n^{-1}(\mathrm{Inn}(G_n))=\{[m,f]:m\in\{0,2n-1\}\}$(位数 $2n$)で、$\mathrm{Out}$ 像は $(\mathbb Z/4n)^\times/\{\pm1\}$(位数 $\varphi(n)$)に潰れる。**unmarked では chirality が構造的に不可視**。
> **状態: Φ-fam は依存修正つき紙上 PASS**(便 77・裁定 138)。**paper-proof candidate** — $K^{(3)}$ のみ Lean 済、族版は未 Lean、$n=9$ の機械検分は**単系統**。

> ### 4 点セットの相互関係(統合の要点)
> $$\underbrace{\text{E1-1 isolated}}_{\text{正典 Thm 4.3・全 }n\ge3}\ \Longrightarrow\ \underbrace{\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})\ \text{有限群}}_{\text{E1-2 の前提}}\ \xrightarrow{\ \text{Thm 4.6}\ }\ \underbrace{\mathrm{Aff}\times\mathcal Z_2}_{\text{E1-2}}\ \xrightarrow{\ \Phi\text{-fam}\ }\ \underbrace{\mathrm{Aut}_{\rm cont}\ \text{への忠実作用}}_{\text{E1-4}}$$
> E1-3(同値)はこの鎖の**横**にあり、鎖が作った有限段の族を**算術の一つの主張へ束ねる**(コンパクト性)。**4 点は独立の 4 定理ではなく、E1-1 を土台にした 1 本の鎖 + 1 本の横木**である — これが統合して初めて見える形。
>
> **E1-1 の効き方が二重であること(便 77 F77-3.3 の訂正が示したこと)**: isolated 性は群構造(E1-2)だけでなく、**$\Phi_n$ の codomain を $\mathrm{Aut}(G_n)$ と書く時点**でも使われている。正しい依存順は
> $$\text{Thm 4.3 (settled)}\ \Longrightarrow\ T_{m,f}:G_n\twoheadrightarrow G_n\ \Longrightarrow\ T_{m,f}\in\mathrm{Aut}(G_n).$$
> `phifam_v1.md` の旧 FINDING Φ3「Aut 性に isolated 不要」は**誤りとして撤回済**(裁定 138)。**鎖の土台が E1-1 一本である**という §2 の読みは、この訂正によってむしろ強まった。

---

## 3. 語彙の橋 — $\mathrm{Aff}=\mathrm{Hol}$(**本文書の要**)

巡回群の**アフィン群と正則群(holomorph)は同一物**である:
$$\mathrm{Aff}(\mathbb Z/m\mathbb Z)\;=\;\mathbb Z/m\rtimes(\mathbb Z/m)^\times\;=\;\mathbb Z/m\rtimes\mathrm{Aut}(\mathbb Z/m)\;=\;\mathrm{Hol}(\mathbb Z/m\mathbb Z).$$
したがって:

| | 正典の言葉(2405 Thm 4.6) | 工房の壁側の言葉(裁定 211/213/220) |
|---|---|---|
| 奇部分 | $\mathrm{Aff}(\mathbb Z/n_0)$ | $\mathrm{Hol}(\mathbb Z/N_{\rm ord})$ |
| 2-部分 | $\mathcal Z_2$($\alpha\le1$)/ $\widetilde H_\alpha$($\alpha\ge2$) | $\mathrm{Syl}_2(\ker\tilde\chi)$ |

> ### 統一形(**E1 の中心命題**)
> $$\boxed{\ \mathrm{GTSh}\ \cong\ \bigl(\text{2-群因子}\bigr)\ \times\ \mathrm{Hol}(\mathbb Z/N_{\rm odd})\ }$$
> - **中間峰(dihedral・$\alpha\le1$)**: 2-群因子 $=\mathcal Z_2\cong C_2$、$N_{\rm odd}=n_0$。**正典の定理**。
> - **中間峰(dihedral・$\alpha\ge2$)**: 2-群因子 $=\widetilde H_\alpha$(位数 $2^{2\alpha-2}$)。**正典の定理**。
> - **壁(D4 族)**: 2-群因子 $=D_8$、$N_{\rm odd}=N_{\rm ord}\in\{11,13,15\}$。**工房の実測**(`structthm_h2_v2.md` §5)。
> - **壁(PSL 窓 S4)**: 2-群因子 $=1$、$N_{\rm odd}=9$。**工房の実測**(`week4-E2作戦_v1.md` 付録 A)。
>
> **読み**: dihedral 族も壁の窓族も「**奇部分は常に $\mathrm{Hol}$(= 正典の $\mathrm{Aff}$)であり、族ごとに違うのは 2-群因子だけ**」という一つの形に収まる。正典が $\alpha$(2-進の深さ)で場合分けしていた構造は、壁側では $\mathrm{Syl}_2(\ker\tilde\chi)$ という**一つの量**に吸収される。

> **「刈り込み」の語彙**(発案係 I9-3 の言い方の正確化): 窓を大きく取る(=$N$ を細かくする)と $\mathrm{Hol}$ 因子の $N_{\rm odd}$ が伸び、2-群因子が育つ。逆に $\tilde\chi$ の像 $Q$ が $(\mathbb Z/N_{\rm odd})^\times$ 全体に達しない窓では $\mathrm{Hol}$ が**刈り込まれた** $C_{N}\rtimes Q$ になる。工房の三窓ではいずれも $Q=\mathrm{Aut}(C_N)$ 全体(刈り込みなし)。**刈り込みが起きる窓の実例は §5 の未解決欄**。

> **⚠ 型の警告(混同禁止)**: 上の「統一形」は
> - 中間峰では **$\mathrm{GT}(K^{(n)})$ の抽象同型**(正典 Thm 4.6・証明済)
> - 壁では **$\mathrm{GTSh}(N,N)$ の内部直積分解**(`structthm_h2_v2.md` の (a$_{\rm int}$)・**GAP 単系統の実測**)
>
> であり、**同じ「形」だが証明の格が違う**。壁側は cross-checked ですらない。この差を消して書かないこと。

---

## 3.5 統一形の**射程**(裁定 220 の対照実験による限定 — 重要)

§3 の統一形は**普遍ではない**。裁定 220(I10-1 判定・NULL-I10 発火)は次を確定した:

> **(H2) が成立していても、$\mathrm{Syl}_2\times\mathrm{Hol}$ 形は $r=3$ で崩壊する。形の成立条件は base の巡回性($r=1$)側にある。**
> 奇部が $5^0,5^1,5^2$($r=1,2,3$)と並ぶ族で、核は $C_5^2$ の中間部分加群 — **5^{r−1} 律(candidate)**。

したがって統一形は
$$\mathrm{GTSh}\cong(\text{2-群因子})\times\mathrm{Hol}(\mathbb Z/N_{\rm odd})\qquad\textbf{(base が巡回のとき)}$$
と書くのが正しい。**$\mathrm{Hol}$ は「巡回 base の正則群」であり、base が非巡回になれば $\mathrm{Hol}$ という語自体が使えない**($\mathrm{Aff}(\mathbb Z/m)$ も同様)。中間峰(dihedral 族)は $\mathbb Z/n_0$ が定義から巡回なので常に射程内、壁側は**窓ごとに base の巡回性が測定項目**である。

---

## 4. 窓族の統一表

**列の意味**: 「2-群因子」「$\mathrm{Hol}$ 因子」は §3 の統一形の 2 因子。「格」は主張の格付け(正典の定理 / 実測 / candidate)。

| 族 | 窓 | $N_{\rm ord}$ | $\lvert\mathrm{GTSh}\rvert$ | IdGroup | 2-群因子 | $\mathrm{Hol}$ 因子 | 格 |
|---|---|---|---|---|---|---|---|
| **dihedral($\alpha\le1$)** | $K^{(n)}$、$n=n_0$ 奇 | $2n_0$ | $2n_0\varphi(n_0)$ | — | $\mathcal Z_2\cong C_2$ | $\mathrm{Aff}(\mathbb Z/n_0)$ | **正典 Thm 4.6** |
| ″(実測) | $K^{(3)}$ / $K^{(5)}$ / $K^{(9)}$ | 6 / 10 / 18 | **12 / 40 / 108** | — | $C_2$ | $\mathrm{Aff}(\mathbb Z/3,5,9)$ | 証明書 K3/K5/K9(Thm 4.6 期待値と一致) |
| **dihedral($\alpha\ge2$)** | $K^{(n)}$、$n=2^\alpha n_0$ | $n$ | $n_0\varphi(n_0)2^{2\alpha-2}$ | — | $\widetilde H_\alpha$ | $\mathrm{Aff}(\mathbb Z/n_0)$ | **正典 Thm 4.6** |
| **A₅ 窓** | $N_A$ | (k=5) | **20** | — | $1$ | $\mathrm{Hol}(\mathbb Z/5)=F_{20}$ | isolated **true**(20/20 に自己同型 witness) |
| **PSL 窓(case A)** | S1 / S3 | 7 / 7 | **42 / 42** | [42,1] | $1$ | $\mathrm{Hol}(\mathbb Z/7)=\mathrm{AGL}(1,7)$ | 封印値・cross-checked |
| ″ | **S4 = PSL(2,8)** | **9** | **54** | **[54,6]** | $1$ | $\mathrm{Hol}(\mathbb Z/9)$ | 同上 |
| ″ | S5 | 11 | **110** | [110,1] | $1$ | $\mathrm{Hol}(\mathbb Z/11)$ | 同上 |
| **PSL 窓(case B)** | S2 / S6 / S7 | **4 / 5 / 6** | **32 / 40 / 48** | — | — | **$\mathrm{Hol}$ 形でない**($D_{4k}$ 型) | **非 isolated**(settled = 16/32・20/40・24/48) |
| **E 族(梯子・$N_{\rm ord}=9$)** | W-E-A10-9t1($t=1$) | 9 | **54** | **[54,6]** | $\mathrm{Syl}_2(S_1)=1$ | $\mathrm{Hol}(\mathbb Z/9)$ | 梯子 17/17・Ξ 二系統一致 |
| ″ | W-E-A11-9t2($t=2$) | 9 | **108** | **[108,26]** | $\mathrm{Syl}_2(S_2)\cong C_2$ | $\mathrm{Hol}(\mathbb Z/9)$ | 同上 |
| ″ | W-E-A12-9t3($t=3$) | 9 | **108** | **[108,26]** | $\mathrm{Syl}_2(S_3)\cong C_2$ | $\mathrm{Hol}(\mathbb Z/9)$ | 同上 |
| ″ | W-E-A13-9t4($t=4$) | 9 | **432** | **[432,362]** | $\mathrm{Syl}_2(S_4)\cong D_8$ | $\mathrm{Hol}(\mathbb Z/9)$ | 同上($K=C_9\times D_8$) |
| **D4 族($t=5$)** | W-D-A16-11a | 11 | 880 | [880,118] | $D_8$ | $\mathrm{Hol}(\mathbb Z/11)$ | 明示同型(GAP 単系統) |
| ″ | W-D-A18-13a | 13 | 1248 | [1248,1162] | $D_8$ | $\mathrm{Hol}(\mathbb Z/13)$ | 同上 |
| ″ | W-D-A20-15a | 15 | 960 | [960,11038] | $D_8$ | $\mathrm{Hol}(\mathbb Z/15)$ | 同上 |
| **刈り込み域($t=0$)** | W-E-A10-5x2t0($r=2$) | 5 | **40** | [40,12] | $C_2$ | $\mathrm{Hol}(\mathbb Z/5)$ | 形は**成立** |
| ″ | **W-E-A15-5x3t0($r=3$)** | 5 | **200** | **[200,47]** | — | **形が崩壊**($A=C_5^2$・$K=C_{10}\times C_5$) | 裁定 220(対照実験) |
| **病理** | W-C-p5(SL(2,5)) | 10 | **UNKNOWN** | — | — | — | 合成表が閉じない(384 件) |
| ″ | idx126-s2/s3 | 3 | 6 | — | — | — | **χ-退化**($\tilde\chi$ 像自明・settled_fail 6/12) |

**兄弟窓による頑健性**(P-A13-12): 梯子の兄弟 9 窓すべてが canonical 窓と同一の IdGroup を与える(`-o2`…`-o6` の 5 窓 = [54,6]、$t=2,3$ の 4 窓 = [108,26])。**律は窓の等長類でなく $(N_{\rm ord},t)$ の関数**。

> ### 統合で見えた交差(**本文書で初めて並んだ**)
> $$\lvert\mathrm{GT}(K^{(9)})\rvert=2\cdot9\cdot\varphi(9)=108\qquad\text{と}\qquad\lvert\mathrm{GTSh}(\text{梯子 }t=2,3)\rvert=108\ (\mathrm{IdGroup}\ [108,26]=C_2\times\mathrm{Hol}(\mathbb Z/9))$$
> **中間峰の $K^{(9)}$(dihedral・正典 Thm 4.6 で $\mathrm{Aff}(\mathbb Z/9)\times\mathcal Z_2$)と、壁の梯子 $t=2,3$ 窓は、同じ位数 108 の同じ形を与える。**
> 同様に $\mathrm{GTSh}(\text{梯子 }t=1)=[54,6]=\mathrm{GTSh}(\text{S4}=\mathrm{PSL}(2,8))=\mathrm{Hol}(\mathbb Z/9)$、および $\mathrm{Hol}(\mathbb Z/5)$ が A₅ 窓($N_A$)と刈り込み域 $r=2$ 窓の両方に現れる。
> **⚠ 未検証**: $\mathrm{GT}(K^{(9)})$ の **IdGroup は直接測っていない**(証明書 `K9.v1.json` は位数 108 のみ)。$[108,26]$ との一致は**位数と Thm 4.6 の形からの推定**であり、**確認は 1 回の GAP 呼び出しで済む**(§5 U-11)。

> ### ⚠ 誤読防止 — `holmg_census_20260730.json` の MISMATCH について
> 同 census は D4 三窓と梯子 $t=4$ に `MISMATCH_IDGROUP` を記録している。**これは本表への反証ではない**。census が照合した candidate は **$\mathrm{Hol}\times C_2^k$(2-群因子が初等アーベル)** であって、$D_8\times\mathrm{Hol}$ ではない。
> $D_8$ は非アーベルなので $C_2^k$ 候補と一致しないのは**当然**であり、むしろ **2-群因子が初等アーベルでないことの独立確認**として読むのが正しい。$t=1,2,3$ が `MATCH_k0/k1` なのは 2-群因子が $1,C_2,C_2$ で実際に初等アーベルだから。
> **census の MISMATCH 行を「$\mathrm{Syl}_2\times\mathrm{Hol}$ の反証」と誤読しないこと。**($r=3$ 窓の `MISMATCH_ORDER` は別物で、こちらは**本物の崩壊**である。)

**表の読み**:
1. **$\mathrm{Hol}$ 因子は族を越えて一様**。族の違いは 2-群因子にしか現れない。
2. **2-群因子は「尾部の対称群の Sylow 2」**($\mathrm{Syl}_2(S_t)$、裁定 213 の Tail 律)。$t=1$ で自明 ⟹ **$\mathrm{Hol}$ が裸で出る**。$t=4$ で $D_8$ ⟹ D4 族と同じ形。
3. **PSL 窓 S4 と梯子 $t=1$ 窓は「別の実現・別の次数」でありながら同じ $\mathrm{Hol}(\mathbb Z/9)$ を出す**(裁定 217 erratum: 全体では S4 が先行)。これは「$\mathrm{GTSh}$ が窓の細部を忘れる」ことの最初の標本。
4. 非 settled 窓(S2/S6/S7)はそもそも $\mathrm{GT}(N)$ が有限群にならない側で、表の形の外にある。

> ### ⚠ 表全体にかかる警報【SD-a】(裁定 219)
> **壁窓(D4 族・E 族・PSL 窓)の isolated 性 (W1) は全キャンペーンで未検証である**(settled $\ne$ isolated)。
> したがって表の壁側の行は **$\mathrm{GTSh}(N,N)$ についての群論的測定**であって、$\mathrm{GT}(N)$ との同一視(= 中間峰の行で正典が保証しているもの)は**していない**。**群論の測定値は不変だが、算術的主張((W1) を前件に持つもの)へ持ち上げるにはこの検証が要る。**

---

## 5. 未解決の名指し

本文書は統合であり、下記は**すべて candidate または UNKNOWN のまま参照する**(本文書で格上げはしない)。

| # | 未解決 | 出典・現状 |
|---|---|---|
| **U-1** | **5^{r−1} 律**(刈り込み律) | 裁定 220・**candidate**(GAP 単系統)。$r=3$ で $\mathrm{Syl}_2\times\mathrm{Hol}$ 形が崩壊する機構。核は $C_5^2$ 中間 $Q$-部分加群でその同定が数学者委嘱中。一般化($\ell$ 版)は `docs/notes/pruning_law_v1.md`(**DRAFT・本文未着手**)。§3.5 の射程限定の実体 |
| **U-2** | **【GAP-1′】** $\varepsilon=0$ の機構 | `epsilon_mechanism_v2.md` §8。$B_3$ 方向($\theta$/$\tau$ の 2 本のノルム方程式)から $\tilde\chi$ 方向のノルム条件への転送 |
| **U-3** | **【GAP-LOC-3】** 余境界形から $Z(S)$-成分消滅へ | `loc_lemmas_v1.md` §4.3。M-1P の証明の真の壁。LOC-1 は同値としては**偽**(同 §2) |
| **U-4** | **【GAP-LOC-1】** $T\vert_S=\mathrm{id}\Rightarrow$ 中心化 | 同上 §2.3。両窓で反例 0 だが未証明 |
| **U-5** | **【GAP-2】** $\tilde\chi$ 全射・$\mathrm{Syl}_2(K)=D_8$ の証明 | `structthm_h2_v2.md` §7。現状すべて実測 |
| **U-6** | **【SD-a】** 壁窓の isolated (W1) 未検証 | 裁定 219。§4 の警報 |
| **U-7** | **P-EPS-5′** の点火機構 | `epsilon_mechanism_v2.md` §6・`loc_lemmas_v1.md` §6(IGN-1/2/3。最有力は $\tilde\theta\vert_{Z(S)}$ の非自明化) |
| **U-8** | **Conj 5.1(dihedral 予想)の奇数/混合側** | 正典。証明済みは $n=2^\alpha$($\alpha\ge2$)のみ。**本峰** |
| **U-9a** | E1-4 の**旧対象** $H^{\rm fun}$ coset 塔上の忠実作用 | 便 75 F6.2(e) の三条件は**依然 UNKNOWN**。framed 正則対象は代替閉鎖であって旧対象の解決ではない(§2 E1-4) |
| **U-9b** | Φ-fam の Lean 化・$\Phi_n$ の**像**の記述 | `phifam_v1.md` 【Φ-1】【Φ-3】: 族版は未 Lean($K^{(3)}$ のみ Lean 済)・$n=9$ 検分は単系統・像が $\mathrm{Aut}(G_n)$ のどこかは射程外(単射性のみ) |
| **U-10** | $\widehat{\mathrm{GT}}=\widehat{\mathrm{GT}}_{\rm gen}$ か | 正典(定義ノート §2「gentle の意味」)。未解決 |
| **U-11** | $\mathrm{GT}(K^{(9)})$ の **IdGroup** | §4 の交差($[108,26]$ との一致)は位数と Thm 4.6 からの**推定**。証明書 `K9.v1.json` は位数 108 のみ。**GAP 1 回で確定する最安の宿題** |
| **U-12** | case B($D_{4k}$ 型)は統一形の外か | S2/S6/S7 は $\mathrm{Hol}$ 形にならず非 isolated。**統一形が case A に限る理由**が未解明(W3-7 は射程限定つき claim・一般外挿禁止) |

---

## 6. 新規性の申告・出所

**grep 済**(`GT^odd`, `Aff(`, `Hol(`, `4 点セット`, `刈り込み`)。

- **既出**: $\mathrm{GT}^{\rm odd}_{\rm Dih}\cong\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2$(地図 帯 0 領有・Φ-fam)/ 壁の $\mathrm{GTSh}=\mathrm{Syl}_2\times\mathrm{Hol}$(裁定 211/213)/ S4 窓も $\mathrm{Hol}(\mathbb Z/9)$(裁定 217/219)/ 5^{r−1} 律(裁定 220)/ 「同一語彙で書ける」という起草時期の論拠(発案係 I9-3)。
- **本文書で新しいのは記述であって定理ではない**: ①**$\mathrm{Aff}=\mathrm{Hol}$ という同一視を明示**して正典 Thm 4.6 と壁の実測を**一つの形**に並べたこと(§3)②その形の**射程を裁定 220 の対照実験で限定**したこと(§3.5)③**格の混同禁止**を型警告として固定したこと(§3 末尾・§4 の【SD-a】警報)④窓族の統一表(§4)。
- **「初」という語は使わない**(工房外の文献での既知性は未調査)。

> ### 衛生上の申し送り(棚卸しで判明・司令塔へ)
> **中間峰 4 点セットは `provenance/CLAIMS.md` に 1 件も登録されていない**(GT^odd / GT^odd_Dih / Aff(Ẑ^odd) / Φ-fam / isolated 既知 / 忠実実現 のいずれも該当なし。`provenance/LEDGER.md` も同様)。
> 地図 帯 0 では**領有**として筆入れされ、裁定 111/130/138 で Sol 検分も済んでいるのに、**台帳には無い**。4 点セットは工房の中間峰そのものなので、C-番号の付与を検討されたい(本文書は台帳を書き換える権限を持たないため申し送りに留める)。
> あわせて記法規約の確認: **`GT^odd` ではなく `GT^odd_Dih`**(dihedral 窓族由来の限定子を保持)が正式表記(誤読事故を受けた規約・Sol 同調済)。本文書は §2 以降これに従ったが、引用元の原文には `GT^odd` 表記が残る。
>
> **棚卸しで出た証明書側の不整合 2 件**(本文書は証明書を書き換えないので申し送り):
> 1. **`certificates/S1.v2.json`〜`S7.v2.json` の `isolated` 欄は全窓 `"UNKNOWN"` のまま**である。一方 `docs/week3-PSL封印計算_opus_v1.md` の封印 JSON は `sealed.isolated` = true/false を持ち、`docs/week4-E2作戦_v1.md` 付録 A は証明書へ `isolated_justification` を 1 行ずつ転記せよと指示している — **その転記が未反映**。§4 の PSL 行は封印値と E2 付録 A を典拠にしており、証明書のみを見ると矛盾して見える。
> 2. 梯子の測定スペック(`a13_prediction_v1.md` §6 欄 24)は `24_iso_to_Syl2_times_Hol` を定義しているが、**実際の証明書にあるのは `24_gtsh_idgroup` のみ**。同型判定は司令塔の IdGroup 突合(裁定 213)で代替されている。**スペックと証明書の欄名が食い違っている**ので、次版でどちらかに寄せられたい。
>
> **用語の訂正 1 件**: case B(S2/S6/S7)の settled 率を「1/2」と書くのは誤りで、正しくは **$2/\varphi(e)$**(`week4-E2作戦_v1.md`:「**『半分』は偶然である**」)。本文書 §4 はこれに従い実数(16/32・20/40・24/48)で記載した。

**出所**: `docs/week1-定義ノート.md`(§1–§3)/ `docs/地図.md`(帯 0・帯 1・delta 台帳)/ `docs/notes/structthm_h2_v2.md`(D4 三窓)/ `docs/notes/epsilon_mechanism_v2.md` / `docs/notes/loc_lemmas_v1.md` / `docs/week4-E2作戦_v1.md` 付録 A(PSL 窓)/ `search/certs/epsbits_a13_ladder_20260730.json`(梯子)/ `sol/裁定_130・211・213・214・217・219・220`。
