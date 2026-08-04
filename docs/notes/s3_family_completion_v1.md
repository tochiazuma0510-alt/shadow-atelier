# (S3) 族の完成 — **(6′) の族版**と **APPLY ゲートの族版**(v1)

**状態札: `candidate(単系統・Sol 未監査)/ 第 I 部の主張自体は既出(§8 で申告)・本稿が足すのは書かれた証明と射程と会計 / Lean 検証ではない / SURJ は結論しない / 封印非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設 v1**
- 委嘱: 司令塔「P1 族一撃の残り紙仕事 2 本(1 ファイルに両方)。第 1 部 =(6′) の族版(補題 R′ の縮約を全奇数 $n\ge3$ の紙の証明へ)。第 2 部 = APPLY ゲートの族版(C1′-any の定理化)」
- **依拠(正典 + repo 内のみ・外部文献ゼロ)**
  - 正典 arXiv **2405.11725**: **Thm 4.3 (4.12)**($\mathrm{GT}(K^{(n)})$ の明示式・isolated)/ **Thm 4.6**(位数)。抽出正本 = `docs/week1-定義ノート.md` §2–§3
  - `docs/notes/oddH_full_proof_v1.md`: **補題 A**(構造)・**補題 C(2)**・**補題 G**・**補題 H = (1.3)**・**補題 I**・**命題 ODD-P**・**§11.1/§11.2**($\Phi$ の座標作用)
  - `docs/week4-K3飽和_opus_v3.md` §5.2.0–§5.2.3: **定理 $R^{\rm cyc}_{\rm formal}$** の型・前件 (0)(1)(2)(3)(5′)(6′)・**補題 R′**(縮約)
  - `docs/notes/w2fam_v1.md` §3.4/§3.5(**$\Phi_{0,f_k}=\mathrm{inn}(X^{-2k})$**・命題 K5-1 / Sol 便 73 (1.13) の再掲)・**命題 (W2)-fam**(裁定 120)
  - `docs/notes/s3_family_draft_v1.md`(**正本**・§3.2 定理 SURJ-fam・§4.3 の新札・§5 の系と gate)/ `docs/notes/c2c4_closure_v1.md` §2.1 / `docs/notes/q7_lower_bound_v1.md` §7(前件表)
  - `docs/notes/c21_draft_v1.md`(**C1′/C5**・**命題 A7-fam**・裁定 214)/ `docs/notes/fam_u_assembly_v1.md`(総組立・距離図 §V.5)/ `docs/notes/fam_u_assembly_addendum_C_draft_v1.md` §C.4(**【ASM-α】**)/ `docs/notes/asm_alpha_falsifier_v1.md`(**F-1・F-2**)
  - 実測 cert `search/certs/s3f_a3_6prime_20260804.json`(裁定 470)— **較正アンカーとしてのみ引用**

> ## 遵守申告
> - **封印非接触**: $K^{(5)}$ の値・窓データ・測定値・$\hat c_\mu$・$\varepsilon$ bits・PSL 欄に**一切触れていない**。$n=5$ は domain 内(裁定 396/398)なので $G_5$ の**純群論不変量**(部分群の位数・共役類の大きさ・置換作用)にのみ現れる。これらは既に `oddH_full_proof_v1.md` §7 の公開表にある量である。命題 K5-1 は **`w2fam_v1.md` §3.5 の再掲経由**で引用し、$K^{(5)}$ manifest は開いていない。
> - **矢印を跨がない**(v2 §V.5.2): 本稿は $\mathrm{ord}([u_n]_{2n})=n$ から $\mathrm{ord}(a_n)=n$ への橋(B-1)を**渡らない**。第 II 部はすべて「(5′) 発効後に接合」という条件文である。**SURJ を結論しない。**
> - **TB/橋の昇格を前提にしない**: (TB1)–(TB4)・BFC の格は本稿では動かさない。第 I 部は**枠組み層を一度も使わない**(§4 の会計)。
> - **機械値の手写し禁止**: §9 の値はすべて `scratchpad/s3f_sixp_fam_check.py` の出力(SHA-256 併記)。cert の値は**パスで参照**し転記しない。

---

## 0. 判定(先に 6 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | **(6′) の族版は立つか** | ★★ **立つ**。**全奇数 $n\ge3$・全 $\alpha\ne0$ の窓**で紙の証明(§5 定理 SIXP-fam)。障害札は不要。⟹ per-n 有限計算の**族化手続きは代替として要らない**(§6 に「縮約が無効になる窓」の分岐手続きだけ残す) |
| **②** | 本稿の**新規性** | ★ **主張自体は既出**。`c2c4_closure_v1.md` §2.1 の表が「(6′) の像の等式と忠実性 = **全奇 $n$ で自動**(命題 K5-1)」と既に記帳し、`q7_lower_bound_v1.md` §7 の前件表も同じ扱いをしている。**本稿が足すのは (a) 書かれた証明、(b) $\alpha$ の射程、(c) 依存の会計、(d) 機械 spot-check** の 4 点(§8) |
| **③** | 証明の**核** | ★ **既在 2 本の接合 + 新しい 1 行**。既在 = 「$\Phi\vert_{\mathfrak F_0}=\mathrm{inn}(\langle X^2\rangle)$」(`w2fam_v1.md` §3.5)と「$H_{j,\alpha,\beta}$ が (P1)(P2)(P3)($\alpha\ne0$)」(ODD-H)。**新しいのは「$\Lambda_\alpha$ への制限で忠実性が落ちない」= $\langle X\rangle$ が $\Lambda_\alpha$ に単純推移(補題 Λ-REG)**の一段 |
| **④** | **依存の会計** | ★★ 定理 SIXP-fam は **(W2)-fam(A2)も 補題 R′ も枠組み層(TB/BFC)も使わない**。使うのは**正典 Thm 4.3 (4.12) と ODD-H だけ**。⟹ $R^{\rm cyc}_{\rm formal}$ の窓側前件で残る未知は **(5′) ただ一つ**(§5.4) |
| **⑤** | **APPLY 族版** | ★★ 起草した(§12 定理 APPLY-fam)。ただし **正本 §4.3 の【S3F-A2】+【S3F-A3】は、独立の存在量化のままでは接合しない**(§11・自己捕獲)。最小形は matched な単一存在量化 **【MATCH-one】**。**第 I 部の効き目でその負担は (5′) のみに落ちる** |
| **⑥** | **方向の軸** | ★ **訂正**。「十分方向は弱化可・逆方向は不可」は**軸を取り違えている**。正しい軸は **曖昧集合 $S\subseteq$ 前件集合 $P$** であり、数学的要求は両方向で同じ(§15)。逆方向の per-n C1′ は**運用規律**(陰性主張の登録レジーム)として維持する — 裁定 214 の水準は下げない |

---

# 第 I 部 — **(6′) の族版**

## 1. 対象と記号(既存のものだけ・再定義しない)

$n\ge3$ を奇数とする。ODD-H §2 補題 A の座標で

$$G_n=A\rtimes Q,\quad A=\langle a_1,a_2,a_3\rangle\cong(\mathbf Z/n)^3,\quad Q=\{1,q_1,q_2,q_3\}\cong C_2^2,\quad \lvert G_n\rvert=4n^3,$$
$$X=a_1q_1,\qquad Y=a_1a_2a_3q_2,\qquad X^2=a_1^2,\qquad M:=\mathrm{ord}(X)=2n,\qquad K:=\mathbf Q(\zeta_{2M})=\mathbf Q(\zeta_{4n})=F_n.$$

窓は ODD-H (1.2) の $H_{j,\alpha,\beta}=\langle a_j,\ a_1^{\alpha}a_{j'},\ a_1^{\beta}q_j\rangle$($j\in\{2,3\}$、$j'=5-j$)。

$$\Lambda_{j,\alpha,\beta}:=\{\,gH_{j,\alpha,\beta}g^{-1}\ :\ g\in G_n\,\}\qquad(\textbf{共役類}\text{。}\textbf{剰余類空間 }G_n/H\textbf{ ではない} — \text{week4 §5.2.0})$$

$$\tau:\mu_M\to\mathrm{Sym}(\Lambda),\ \zeta_M^{\,i}\mapsto\bigl(H'\mapsto X^iH'X^{-i}\bigr),\qquad \mathfrak F_0:=\ker\widetilde\chi_{4n}\le\mathrm{GT}(K^{(n)}),\qquad \rho_0:=\Phi\vert_{\mathfrak F_0}\ \text{の}\ \Lambda\ \text{上への制限}.$$

$\Phi_{(m,f)}$ は shadow の定める $G_n$ の自己同型 $X\mapsto X^{2m+1}$、$Y\mapsto f^{-1}Y^{2m+1}f$(week4 §5.2.0 の型表)。

> **向きの規約について**: $\langle X\rangle\xrightarrow{\sim}\mu_M$ の生成元の向き(week4 §5.2.0 注 4)は本稿の結論に影響しない — 向きを反転すると $\tau(\zeta_M)\mapsto\tau(\zeta_M)^{-1}$ となるだけで、**忠実性も部分群 $\tau(\mu_M[e])$ も不変**である。

## 2. 示すべきこと((6′) の逐語)

week4 §5.2.1 の前件 **(6′) = (R6-act)**:

$$\Lambda\ \text{は}\ \Phi(\mathfrak F_0)\text{-安定},\qquad \boxed{\ \rho_0\ \text{は忠実},\qquad \rho_0(\mathfrak F_0)=\tau\bigl(\mu_M[e]\bigr)\ }\qquad(e:=\lvert\mathfrak F_0\rvert).$$

正本 §4.3 の【S3F-A3】は、これを「**ある一つの**単元窓で」成り立てばよいという存在形で立てていた。本稿は**存在形を経由せず全称で**示す。

## 3. 補題 Λ-REG(**新しいのはこの一段だけ**)

> ### 補題 Λ-REG【candidate】
> $n\ge3$ 奇、$j\in\{2,3\}$、$\alpha\in(\mathbf Z/n)\setminus\{0\}$、$\beta\in\mathbf Z/n$、$H:=H_{j,\alpha,\beta}$、$\Lambda:=\Lambda_{j,\alpha,\beta}$ とする。このとき
> 1. $\lvert\Lambda\rvert=2n=M=\mathrm{ord}(X)$、
> 2. $\langle X\rangle$ は共役作用で $\Lambda$ に**単純推移**、
> 3. 作用準同型 $\langle X\rangle\to\mathrm{Sym}(\Lambda)$ は**単射**。とくに $\tau:\mu_M\to\mathrm{Sym}(\Lambda)$ は単射で $\tau(\mu_M)$ は regular 可換部分群。
>
> すなわち $R^{\rm cyc}_{\rm formal}$ の**前件 (3) が全奇数 $n$・全 $\alpha\ne0$ で成立する**。

**証明.**
(1) $\alpha\ne0$ ゆえ ODD-H **補題 H(3) = (1.3)** より $N_{G_n}(H)=H$。よって $\lvert\Lambda\rvert=[G_n:N_{G_n}(H)]=[G_n:H]=2n$(ODD-H 補題 G の (P1))。他方 $\mathrm{ord}(X)=2n$(補題 A(3))。
(2) $H$ の $\langle X\rangle$-軌道の長さは $\lvert\langle X\rangle\rvert/\lvert\mathrm{Stab}\rvert$、ここで $\mathrm{Stab}=\{X^i:X^iHX^{-i}=H\}=\langle X\rangle\cap N_{G_n}(H)=\langle X\rangle\cap H$。ODD-H **補題 G** より $H$ は (P1)(P3) を満たし、**補題 C(2)**((P1) の下で (P3) $\iff\langle X\rangle\cap H=1$)から $\langle X\rangle\cap H=1$。ゆえに軌道長は $2n=\lvert\Lambda\rvert$、すなわち $\langle X\rangle$ は推移的で、群の位数と軌道長が一致するから単純推移。
(3) 作用の核は各点の固定部分群に含まれ、とくに $H$ の固定部分群 $=\langle X\rangle\cap N_{G_n}(H)=1$。∎

> **⚠ 引用の格の申告**: 使ったのは ODD-H の**補題 A・C(2)・G・H(3)** の 4 本のみ。いずれも `oddH_full_proof_v1.md` の完全証明つき命題であり、(1.3) は falsifier 判読 **F-3** でも「真に既在($\forall\alpha$ で登録済)」と確認されている。**新規の群論はこの補題の 3 行だけ**である。

## 4. 補題 INN(**既出**・本稿は再掲と独立再検算のみ)

> ### 補題 INN(既出 = 命題 K5-1(W3-15①)/ Sol 便 73 (1.13)/ `w2fam_v1.md` §3.5)
> $$\mathfrak F_0=\{\,[0,f_k]\ :\ k\in\mathbf Z/n\,\},\quad f_k=(r^{2k},r^{-2k},1)=a_1^{2k}a_2^{-2k},\qquad \Phi_{0,f_k}=\mathrm{inn}(X^{-2k}),$$
> ここで $\mathrm{inn}(c):g\mapsto cgc^{-1}$。とくに $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X^2\rangle)$ かつ $e=\lvert\mathfrak F_0\rvert=n$。

**証明(再掲・独立再導出)**。
**(a) $\mathfrak F_0$ の明示**: $\widetilde\chi_{4n}([m,f])=2m+1$ で $m$ は $\mathbf Z/2n$ の類だから
$$\widetilde\chi_{4n}([m,f])=1\iff 2m\equiv0\ (\mathrm{mod}\ 4n)\iff m\equiv0\ (\mathrm{mod}\ 2n)\iff m=0 .$$
$m=0$ は偶だから正典 (4.12) の $\varkappa(0)=-0=0$、すなわち $f=(r^{2k},r^{-2k},1)$。$n$ 奇ゆえ $2\in(\mathbf Z/n)^\times$ で $k\mapsto f_k$ は $\mathbf Z/n$ 上単射、よって $e=n$。**この段は正典 Thm 4.3 (4.12) と $\widetilde\chi$ の定義だけを使い、(W2)-fam を使わない。**
**(b) $\Phi_{0,f_k}=\mathrm{inn}(X^{-2k})$**: 両辺とも $G_n=\langle X,Y\rangle$ の自己同型だから生成元で一致を見ればよい。$X$ 上: $\Phi_{0,f_k}(X)=X^{2\cdot0+1}=X$、$\mathrm{inn}(X^{-2k})(X)=X$。$Y$ 上: $Y=a_1a_2a_3q_2$、$q_2a_iq_2^{-1}=a_i^{\varepsilon_{2i}}$($\varepsilon_{22}=+1$、他は $-1$)より
$$f_k^{-1}Yf_k=(a_1^{-2k}a_2^{2k})(a_1a_2a_3)(a_1^{-2k}a_2^{-2k})q_2=a_1^{1-4k}a_2a_3\,q_2,$$
$$\mathrm{inn}(X^{-2k})(Y)=a_1^{-2k}(a_1a_2a_3q_2)a_1^{2k}=a_1^{-2k}a_1a_2a_3a_1^{-2k}q_2=a_1^{1-4k}a_2a_3\,q_2 .$$
一致する。∎

> **記帳**: (b) は `w2fam_v1.md` §3.5 の計算と**同一**である(同節は ODD-H §11.1 の閉形式経由で同じ式 $(1-4k,1,1)q_2$ を得ている)。本稿は $q_2$ の符号表から直接引き直しただけで、**新規性はない**。再掲する理由は、第 I 部の証明を一箇所で自己完結させるためである。

## 5. 定理 SIXP-fam((6′) の族版)

> ### 定理 SIXP-fam【candidate】
> **$n\ge3$ を奇数、$j\in\{2,3\}$、$\alpha\in(\mathbf Z/n)\setminus\{0\}$、$\beta\in\mathbf Z/n$** とし、$\Lambda=\Lambda_{j,\alpha,\beta}$、$M=2n$、$e=\lvert\mathfrak F_0\rvert=n$ とする。このとき
> 1. **$\Lambda$ は $\Phi(\mathfrak F_0)$-安定**(ゆえに $\rho_0$ が定義される)、
> 2. **$\rho_0$ は忠実**、
> 3. $$\boxed{\ \rho_0(\mathfrak F_0)=\tau\bigl(\mu_M[e]\bigr)=\tau\bigl(\mu_{2n}[n]\bigr)=\bigl\langle\tau(\zeta_M)^2\bigr\rangle\ }$$
>
> すなわち **前件 (6′) = (R6-act) は全奇数 $n\ge3$ の全 $\alpha\ne0$ 窓で成立する。** 前件 (3) は 補題 Λ-REG が同じ範囲で供給する。

**証明.**
**(1)** 補題 INN より $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X^2\rangle)\subseteq\mathrm{Inn}(G_n)$。内部自己同型は $G_n$ の**すべての共役類を保つ**ので、共役類 $\Lambda$ は $\Phi(\mathfrak F_0)$-安定。
**(2)(3)** 補題 INN より、$H'\in\Lambda$ に対し
$$\rho_0([0,f_k])(H')=\Phi_{0,f_k}(H')=X^{-2k}H'X^{2k}=\tau(\zeta_M^{-2k})(H') .$$
ゆえに
$$\rho_0(\mathfrak F_0)=\bigl\{\tau(\zeta_M^{-2k}):k\in\mathbf Z/n\bigr\}=\tau\bigl(\langle\zeta_M^{2}\rangle\bigr)=\tau\bigl(\mu_M[n]\bigr)$$
($\mu_M=\mu_{2n}$ は巡回、$\langle\zeta_{2n}^2\rangle$ は位数 $n$ の唯一の部分群 $=\mu_M[n]=\mu_M[e]$)。これが 3。
忠実性: $\rho_0([0,f_k])=\mathrm{id}_\Lambda$ とすると $\tau(\zeta_M^{-2k})=\mathrm{id}$、補題 Λ-REG(3) の $\tau$ の単射性より $\zeta_M^{2k}=1$、すなわち $2k\equiv0\ (\mathrm{mod}\ 2n)$、$k\equiv0\ (\mathrm{mod}\ n)$。補題 INN(a) の $k\mapsto f_k$ の単射性より $[0,f_k]=[0,1]=1$。∎

### 5.1 第二経路(座標版)— ODD-H §11.2 との突合

補題 INN と ODD-H **§11.2** の変換則
$$\Phi_{m,f}(H_{2,\alpha,\beta})=H_{2,\ \delta\alpha,\ \beta u+c},\qquad u=2m+1,\ \delta=(-1)^m,\ c=1-u-4k$$
に $m=0$($u=1,\delta=+1,c=-4k$)を入れると $\Phi_{0,f_k}(H_{2,\alpha,\beta})=H_{2,\alpha,\beta-4k}$。他方 ODD-H **補題 I(1)** で $b=a_1^{-2k}$($x_1=-2k$, $x_{j'}=0$)として $bH_{j,\alpha,\beta}b^{-1}=H_{j,\alpha,\beta+2(x_1-\alpha x_{j'})}=H_{j,\alpha,\beta-4k}$。**両者は一致する** — これは補題 INN の独立確認である(§11.2 は $n=9$ の全 $108\times144$ 対で実測 PASS と記録されている)。
さらに $\gcd(4,n)=1$($n$ 奇)より $k\mapsto\beta-4k$ は $\mathbf Z/n$ 上自由、これだけで忠実性が再び出る。⟹ **忠実性は「$4$ が $\mathbf Z/n$ で可逆」という一点に帰着する。**

### 5.2 補題 R′ との関係

week4 §5.2.3 の **補題 R′** は「(1)(3)+shadow の定義 ⟹ $\rho_0(\mathfrak F_0)\subseteq\tau(\mu_M)$ は自動、ゆえに (R6-act) $\iff$ $\rho_0$ 忠実」という**縮約**である。本稿は縮約を**使っていない**:

| | 補題 R′ 経由 | 本稿(定理 SIXP-fam) |
|---|---|---|
| 使う前件 | (1)(2)(3)+ 中心化群論法(regular 可換部分群の自己中心性) | **正典 (4.12) + ODD-H のみ**((1) も (2) も不要 — $e=n$ は (4.12) から出る) |
| 得るもの | 包含 $\subseteq\tau(\mu_M)$ ⟹ 残りは忠実性の 1 ビット | **包含でなく等式を直接**+忠実性 |
| $\alpha$ 依存 | (3) が要る ⟹ $\alpha\ne0$ | 同じ($\alpha\ne0$) |

⟹ **二つの経路は独立に同じ結論に到達する**(中心化群論法 vs 明示同定)。正本 §4.3 が「(6′) は有限計算で決着する」と書いた見立ては正しかったが、**有限計算は要らず紙で閉じる**。

### 5.3 ⚠ 縮約が無効になる窓(週 4 §5.2.3 注の族版)

補題 R′ も本稿も**前件 (3)** を使う。$\alpha=0$ の窓では ODD-H (1.3) より $N_{G_n}(H)=\langle H,q_1\rangle\supsetneq H$、$\lvert\Lambda\rvert=n\ne2n=M$ となり **(3) が破れる**(ODD-H 補題 I(3))。この層では本稿の証明も補題 R′ も使えない。**$\alpha=0$ は (P2) を満たさないので窓族に入らない**(ODD-H 命題 ODD-H 3)から実害はないが、**分岐の存在自体は事前登録しておく**(§6)。

### 5.4 ★ 会計 — $R^{\rm cyc}_{\rm formal}$ の前件は今どうなっているか

| 前件 | 内容 | 本稿以後の状態 |
|---|---|---|
| **(0)** | $K^{(n)}$ isolated / $\mathrm{Ih}$ が準同型 | ★ **正典 Thm 4.3・Remark 1.4** |
| **(1) 前半** | $1\to\mathfrak F_0\to\mathrm{GT}(K^{(n)})\to(\mathbf Z/4n)^\times\to1$ 完全 | **(W2)-fam**(candidate・裁定 120) |
| **(1) 後半** | $\widetilde\chi\circ\mathrm{Ih}=\chi_{4n}$ | **W2-arith Route A**(paper-proof candidate・裁定 122)⟵ **算術側・本稿の射程外** |
| **(2)** | $\mathfrak F_0\cong C_e$、$e\mid M$ | ★ **正典 (4.12) から直接**($e=n\mid2n$・§4(a))。(W2)-fam を経由しなくてよい |
| **(3)** | $\mathrm{ord}(X)=\lvert\Lambda\rvert=M$、$\langle X\rangle$ 単純推移 | ★★ **本稿 補題 Λ-REG**(全奇 $n$・全 $\alpha\ne0$) |
| **(6′)** | (R6-act) | ★★ **本稿 定理 SIXP-fam**(同上) |
| **(5′)** | $\rho_0(\mathrm{Ih}(\gamma))=\tau(\kappa_{u^{-1}}(\gamma))$ | ⚠ **UNKNOWN**(= 比較橋 $B_{\rm FC}$ = 【GAP-Rcyc】) |

$$\boxed{\ \textbf{窓に依存する前件のうち、群論側は全部閉じた。残る窓依存の未知は }(5')\textbf{ ただ一つである。}\ }$$

## 6. per-n 有限計算の族化手続き(**代替としては不要**・較正としては残す)

族版が立ったので委嘱の「代替」は発動しない。ただし次の 2 点は手続きとして残す。

1. **分岐の事前登録**(§5.3): 新しい窓を導入するとき、**最初に $\alpha\ne0$($\iff N_{G_n}(H)=H$)を確認する**。破れていれば (3) が落ち、本稿も補題 R′ も使えないので **(6′) を直接確認する**線へ切り替える。
2. **較正としての per-n 検査**(証明の根拠ではない): 新しい $n$ で $\lvert G_n\rvert=4n^3$・$\mathrm{ord}(X)=2n$・$\lvert H\rvert=2n^2$・$\lvert\Lambda_\alpha\rvert=2n$・$\rho_0$ 忠実・$\rho_0(\mathfrak F_0)=\langle\tau^2\rangle$ の 6 項目。**規約(marking の向き・$\Phi$ の語順)の実装誤りを捕まえる装置**であって、数学の入力ではない(ODD-H §11.4 の `AbstractProd` 罠が実例)。

## 7. ★ 射程遮断(**この結果を $\alpha$ の量化拡大に流用してはならない**)

定理 SIXP-fam の証明は $\alpha\ne0$ で通る — **非単元 $\alpha$ を含む**。しかしこれを FAM-U / A7-fam の窓量化の拡大に使ってはならない。

| 層 | 量化 | 根拠 |
|---|---|---|
| **本稿(前件 (3)(6′) の供給)** | $\alpha\ne0$ | §3・§5 |
| **FAM-U / ASM** | $\alpha\in(\mathbf Z/n)^\times$ | `addendum_C_draft` §C.4 |
| **A7-fam(登録主張)** | $\alpha=1$($H_n^{\rm fun}=H_{2,1,0}$) | `c21_draft_v1.md` §7・裁定 214 |

- **falsifier F-1(重大)**: 量化を $\alpha\ne0$ へ広げると **命題 ODD-P・帰結 F8 に正面から抵触**する。非単元 $\alpha$($d=\gcd(\alpha,n)>1$)の窓は ordered passport が $(2n,2^{n-1}1^2,(2n/d)^d)$ で $K^{(3)}/K^{(5)}$ 型ではなく、層 1(passport)・層 2(`M2-exp`)に対応物が存在しない。
- **falsifier F-2(重大)**: 「非単元でも検査が通る」ことは**拡大の安全性の証拠にならない** — 群論述語の大半は $\alpha$ 全域で恒真だからである。**§9 の本稿の検算(非単元を含む)も同じ理由で識別力を持たない。**

$$\boxed{\ \textbf{本稿の }\alpha\ne0\ \textbf{は「前件 (3)(6′) の証明が通る範囲」であって、窓族の量化ではない。}\ \textbf{【ASM-α】は開いたままである。}\ }$$

**【ASM-α】への部分的寄与(正確に)**: 【ASM-α】(A7-fam を $\alpha\in(\mathbf Z/n)^\times$ へ拡大する未閉鎖項)のうち、**(3) と (6′) の行だけ**は本稿が全単元(さらに全 $\alpha\ne0$)で供給する。**残りの供給元(A7 の他の 7 本・層 1/層 2 の passport 整合)は本稿が触れていない。**

## 8. 新規性申告(**grep 済**・「初」という語は使わない)

**grep 語**: `SIXP`・`MATCH-one`・`APPLY-fam`・`ORD-IDX`・`Λ-REG`・`K5-1`・`inn`・`(6′)`・`ρ_0.*忠実`。

- **「(6′) は全奇 $n$ で自動」という主張は既出である**: `c2c4_closure_v1.md` §2.1 の部品表が「(6′) の像の等式 $\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$ と忠実性 / **全奇 $n$ で自動** / **命題 K5-1**($\Phi_{0,k}=\mathrm{inn}(X^{-2k})$・W3-15①)」と記帳し、`q7_lower_bound_v1.md` §7 の前件表も「(6′)【ODD-H / (W2)-fam / Φ-fam が全奇数で供給】」と扱っている。
- **本稿が足したのは 4 点だけである**:(a) **書かれた証明**(既在の記帳は「$\Phi_{0,k}=\mathrm{inn}$」への 1 行の pin であり、**$\Lambda$ への制限で忠実性が保たれる理由 = 補題 Λ-REG が書かれていなかった**);(b) **$\alpha$ の射程**($\alpha\ne0$ 全域・§7 の遮断つき);(c) **依存の会計**((W2)-fam も補題 R′ も枠組み層も不要・§5.4);(d) **機械 spot-check**(§9)。
- **補題 INN は本稿の結果ではない**(命題 K5-1 / Sol 便 73 (1.13) / `w2fam_v1.md` §3.5)。
- 工房外の文献での既知性は**未調査**。

## 9. 較正アンカーと検算

### 9.1 較正アンカー(実測 cert・**値は転記しない**)

- `search/certs/s3f_a3_6prime_20260804.json`(GAP 4.16.0・裁定 470)。$n\in\{3,7,9\}$ の**全単元窓**で `six_prime_holds`。**この cert は本稿の証明の根拠ではなく、規約(marking・$\Phi$ の語順・$\Lambda$ の定義)が本稿の紙と同じ対象を指していることの較正である。** cert 自身が `convention_sanity_check` で語順の識別力を確認している。
- 本稿の定理はこの cert の**外側**(非単元 $\alpha$、および $n\notin\{3,7,9\}$)を予言する。§9.2 はその out-of-sample 確認である。

### 9.2 自前検算(**紙の証明を書いた後に**走らせた)

- **script**: `scratchpad/s3f_sixp_fam_check.py`(SHA-256 `9ac8348e918c22d1ee9771a96ee8d2006016a0e88ee5b33ed24e8d76dcbfa715`)
- **格**: ★ **python 単系統**。**cross-checked ではない**(cert は GAP・非当事者実装だが、格付けには CV-9 仕様同一性判読が要る — 本稿は判読を経ていないので `cross-checked` を付さない)。**Lean 検証ではない。**
- **宇宙(事前登録・値を見る前に固定)**: 奇数 $n\in\{3,5,7,9,11,13,15,21\}$、$j\in\{2,3\}$、$\alpha\in(\mathbf Z/n)\setminus\{0\}$(**単元・非単元とも**)、$\beta\in\{0,1\}$。
- **検査項目**: $\lvert G_n\rvert=4n^3$ / $\mathrm{ord}(X)=2n$ / $X^2=a_1^2$ / $\lvert H\rvert=2n^2$ / $\lvert\Lambda\rvert=2n$(⟹ $N=H$)/ $\langle X\rangle$ 単純推移 / $\tau$ 単射 / **$f_k^{-1}Yf_k=X^{-2k}YX^{2k}$**(補題 INN)/ **$\rho_0$ 忠実** / **$\rho_0(\mathfrak F_0)=\langle\tau^2\rangle$** / **座標則 $\Phi_{0,f_k}(H_{2,\alpha,\beta})=H_{2,\alpha,\beta-4k}$**(§5.1・ODD-H §11.2 との突合)。
- **出力(機械生成)**: 検査窓数 **304**、**`FAILS = 0`**(`RESULT: ALL PASS`)。行(機械出力)$(n,\lvert G_n\rvert,\mathrm{ord}(X),\lvert\Lambda_\alpha\rvert,\lvert\rho_0(\mathfrak F_0)\rvert)=(3,108,6,6,3),(5,500,10,10,5),(7,1372,14,14,7),(9,2916,18,18,9),(11,5324,22,22,11),(13,8788,26,26,13),(15,13500,30,30,15),(21,37044,42,42,21)$。
- ⚠ **識別力の申告(F-2 の適用)**: 非単元 $\alpha$ が通ることは**窓族の量化拡大の安全性の証拠ではない**(§7)。この検算が試しているのは**紙の証明の写し間違いと規約の取り違え**だけである。
- ⚠ **$n=5$ 行について**: $\lvert G_5\rvert$・$\lvert\Lambda\rvert$ 等の**純群論不変量のみ**であり、$K^{(5)}$ の窓データ・$u$ 値・測定値・封印欄には一切触れていない(これらの群論値は `oddH_full_proof_v1.md` §7 の公開表に既在)。

---

# 第 II 部 — **APPLY ゲートの族版**(C1′-any の定理化)

## 10. 接合の問題設定

総組立 **FAM-U-ASM**(`fam_u_assembly_v1.md` §1)は $\mathrm{ord}([u_n]_{2n})=n$ の candidate 鎖を与える。系 **SURJ-fam-K**(正本 §5.1)は $u_n$ を**当該窓の cusp 主係数**として要求する。委嘱の問いは:

$$\textbf{総組立の類 }[u_n]_{2n}\textbf{ を、系の }a_n=[u_n^{-1}]_{2n}\textbf{ と呼んでよいのはいつか。}$$

これは**数学ではなく licensing(適用 gate)の問い**である(F91-5.3 の定理/gate 分離)。以下 §11–§16 はすべてその形で書く。

## 11. ★★ 自己捕獲 — 二つの独立な存在量化は接合しない

正本 §4.3 は残余を 2 枚の札に分けた:

$$\textbf{【S3F-A3 = BRIDGE-one】}\ \exists\alpha:\ (5')(6')\ \text{が窓}\ \alpha\ \text{で成立},\qquad \textbf{【S3F-A2 = C1′-any】}\ \exists\alpha':\ \text{手元の類}=[u_{n,\alpha'}]_{2n}.$$

> ### ⚠ 欠陥(本稿が自分で捕まえたもの)
> **この 2 本から、系 SURJ-fam-K の適用に必要な**
> $$\exists\alpha:\ \bigl[\ (5')(6')@\alpha\ \wedge\ \text{手元の類}=[u_{n,\alpha}]_{2n}\ \bigr]$$
> **は出ない。** $\alpha\ne\alpha'$ でありうるからである。$R^{\rm cyc}_{\rm formal}$ の結論は「その窓の $u$」についての言明なので、**前件が成り立つ窓と、測った量が属する窓が同一でなければ何も言えない。**

$$\boxed{\ \textbf{最小形は matched な}\textbf{単一}\textbf{存在量化である。二札の連言ではない。}\ }$$

> ### ★ 第 I 部の効き目
> 定理 SIXP-fam により **(6′) と (3) は全 $\alpha\ne0$ で成立**するから、matched 条件から (6′)(3) が落ちる。残る一致の負担は **(5′) だけ**である:
> $$\textbf{【MATCH-one】}\quad\exists\alpha\in(\mathbf Z/n)^\times:\ \bigl[\ (5')@(K^{(n)},H_{2,\alpha,0})\ \wedge\ \text{手元の類}=[u_{n,\alpha}]_{2n}\ \bigr].$$
> ($\alpha$ の走る範囲を単元に絞るのは §7 の射程遮断による — 層 1/層 2 との整合は単元窓でしか保証されていない。)

## 12. 定理 APPLY-fam(十分方向の最小形)

> ### 定理 APPLY-fam【candidate / framework-conditional】
> **$n\ge3$ を奇数**とし、前件 **(0)(1)(2)**(= 正本 §3.1 の A1・A2・A3)が $n$ で成立するとする。さらに **【MATCH-one】** の意味で $\alpha\in(\mathbf Z/n)^\times$ と類 $a\in F_n^\times/F_n^{\times2n}$ が存在して
> - **(M-a)** $(5')$ が窓 $(K^{(n)},H_{2,\alpha,0})$ で成立、
> - **(M-b)** $a=[u_{n,\alpha}]_{2n}$($u_{n,\alpha}$ は**当該窓の** cusp $P_0$ における主係数。well-posedness は A7 型の (ii-loc)+補題 LIFT+INV による)、
> - **(M-c)** $\mathrm{ord}(a)=n$
>
> が成り立つならば
> $$\boxed{\ \mathrm{Ih}_{K^{(n)}}:G_{\mathbf Q}\longrightarrow\mathrm{GT}(K^{(n)})\ \text{は全射}\ }$$
> である。**どの $\alpha$ かを同定する必要はない**(存在すれば足りる)。

**証明.** 定理 SIXP-fam と補題 Λ-REG が窓 $\alpha$ で (3)(6′) を供給する。(0)(1)(2) は仮定、(5′) は (M-a)。よって $R^{\rm cyc}_{\rm formal}$ の前件 (0)(1)(2)(3)(5′)(6′) が窓 $\alpha$ で揃い、(R6-full) より
$$\mathrm{Ih}_{K^{(n)}}\ \text{全射}\iff\mathrm{ord}\bigl([u_{n,\alpha}^{-1}]_{2n}\bigr)=e=n .$$
$\mathrm{ord}([v^{-1}]_M)=\mathrm{ord}([v]_M)$(位数は逆元で不変)と (M-b)(M-c) より右辺が成立。∎

> **★ 弱化が効く理由の正確な形**: 結論 $\mathrm{Ih}$ 全射は**窓に言及しない**。ゆえに「どの窓で右辺が成立したか」は結論に現れない。**しかしそれは「前件と測定が同じ窓でなくてよい」ことを意味しない**(§11)。正本 §4.3 の【S3F-A2】の理由づけは前者としては正しく、後者としては足りない。

## 13. 系 ORD-IDX(**窓一様の等式**)と P-S3F-1 の根拠訂正

$R^{\rm cyc}_{\rm formal}$ の証明の**第 2 段**(同値ではなく等式)を取り出す。

> ### 系 ORD-IDX【candidate / framework-conditional】
> $n\ge3$ 奇。(0)(1)(2) と、窓 $\alpha\in(\mathbf Z/n)^\times$ での $(5')$ の下で
> $$\boxed{\ \mathrm{ord}\bigl([u_{n,\alpha}]_{2n}\bigr)\ =\ \bigl\lvert\mathrm{Ih}_{K^{(n)}}(G_{F_n})\bigr\rvert\ }$$
> であり、**右辺は窓に依らない**。したがって
> 1. 前件を満たす 2 窓 $\alpha,\alpha'$ があれば $\mathrm{ord}([u_{n,\alpha}]_{2n})=\mathrm{ord}([u_{n,\alpha'}]_{2n})$;
> 2. 正本 §3.3 の**系 IDX** と併せて
> $$\lvert\mathrm{GT}_{\rm arith}(K^{(n)})\rvert=2\varphi(n)\cdot\mathrm{ord}\bigl([u_{n,\alpha}]_{2n}\bigr),\qquad \bigl[\mathrm{GT}(K^{(n)}):\mathrm{GT}_{\rm arith}(K^{(n)})\bigr]=\frac{n}{\mathrm{ord}([u_{n,\alpha}]_{2n})} .$$

**証明.** $R^{\rm cyc}_{\rm formal}$ の証明 2:(6′) の忠実性と (5′) から $\lvert\mathrm{Ih}_N(G_K)\rvert=\lvert\rho_0(\mathrm{Ih}_N(G_K))\rvert=\lvert\tau(\kappa_{u^{-1}}(G_K))\rvert=\lvert\kappa_{u^{-1}}(G_K)\rvert=\mathrm{ord}([u^{-1}]_M)$($\tau$ 単射・Kummer 理論)。(6′)(3) は定理 SIXP-fam・補題 Λ-REG が供給。$K=F_n$、$M=2n$、$\mathrm{ord}([u^{-1}]_M)=\mathrm{ord}([u]_M)$。2 は正本 §3.3 の系 IDX(証明 (i)(ii)(iii))に代入。∎

> ### ⚠ 正本 §8 の予言 **P-S3F-1** の根拠は弱すぎた(★教材)
> 正本は「系 SURJ-fam-K を両窓に適用すると**左辺が同一**」を根拠にしていた。しかし**同値**からは $\mathrm{ord}_\alpha=n\iff\mathrm{ord}_{\alpha'}=n$ しか出ず、**両方が $n$ でないときの一致は出ない**。正しい根拠は上の**第 2 段の等式**である。**予言 P-S3F-1 自体は生きる**(むしろ強い形で)。「同値の左辺が同じ」から「量が同じ」を読むのは、正本 §3.3 の ★教材(下界と全射性の混同)と同型の罠である。

## 14. C5-fam(手続きの族版)

C5(宇宙の事前登録)の族版で**増える実質は 1 つだけ**である: $S\subseteq P$ という licensing 条件が測定前に判定可能でなければならないので、**集合 $S$ と $P$ を測定前に凍結する**こと。

> ### C5-fam【gate・手続き】
> | # | 凍結する項目 | 内容 |
> |---|---|---|
> | **R-1** | **domain** | $n$ の集合(奇数 $n\ge3$・裁定 396/398。$K^{(5)}$ blind の運用制限は**別欄**に書き、数学の domain と混ぜない) |
> | **R-2** | **窓族とラベル規約** | $j=2$、$\alpha\in(\mathbf Z/n)^\times$、$\beta=0$。証明書スキーマの**必須欄** $(j,[\alpha])$(【C21-d】)。$[\alpha]$ は $\pm$ 類・$\varphi(n)/2$ 個(二重計上禁止・falsifier F-6) |
> | **R-3** ★ | **曖昧集合 $S$** | 測定される量が**どの窓のものでありうるか**の集合。「$\alpha=1$ と信じる」ではなく「$S=\{1\}$ と宣言する」と書く |
> | **R-4** ★ | **前件集合 $P$** | $(5')$ が**成立すると仮定または確認された**窓の集合。$(6')(3)$ は定理 SIXP-fam により全 $\alpha\ne0$ ゆえ $P$ の制約にならない |
> | **R-5** | **量と述語** | 量 $=[u_{n,\alpha}]_{2n}\in F_n^\times/F_n^{\times2n}$、述語 $=\mathrm{ord}=n$(および測定値が $n$ 未満のときの分岐)。**値ではなく述語を先に固定**(IF-FIRST) |
> | **R-6** | **well-posedness 入力** | 整数持上げ $\widetilde\alpha\mapsto\widetilde\alpha+n$(補題 LIFT)と一様化元 $\tau\mapsto\rho\tau$($u\mapsto u\rho^{-2n}$)に対する不変性(INV)。**exact 符号 $u_{n,\widetilde\alpha}=4(-1)^{\widetilde\alpha}$ は類・位数の水準に入れない**(falsifier F-6) |
> | **R-7** | **モデル束縛** | 整モデル・cusp section・局所助変数・正規化が 定理 B-4 / 補題 B-5(ii-loc) の規約と一致(旧 G-3) |
> | **R-8** | **provenance** | cert・入力ハッシュ・script SHA・独立再計算。**値は機械生成のみ**(手写し禁止) |
>
> **規則 R-9(族版で新しい唯一の規則)**: **測定後に $S$ を狭めること(post-hoc narrowing)は新しい登録とみなす。** 「測ってみたら $\alpha=1$ の窓だと分かった」は $S$ の事後変更であり、元の登録の下では licensing を与えない。

## 15. 逆方向の scope(**軸の訂正**)

> ### ★ 訂正: 「方向」は正しい軸ではない
> 正本 §4.3 は「十分方向では窓ラベル同定不要・逆方向(非全射結論)では弱化不可」と書いた。しかし **$R^{\rm cyc}_{\rm formal}$ が与えるのは同値**であり、真の窓 $\alpha_0\in S$ が $P$ に入ってさえいれば
> - $\mathrm{ord}(a)=n$ ⟹ 全射、
> - $\mathrm{ord}(a)<n$ ⟹ **非全射**
>
> が**どちらも**ラベルの同定なしに従う(系 ORD-IDX ならさらに $\lvert\mathrm{Ih}(G_{F_n})\rvert$ の値そのものが出る)。逆に $S\not\subseteq P$ なら**どちらの方向も出ない**。
> $$\boxed{\ \textbf{数学的な軸は「方向」ではなく }S\subseteq P\ \textbf{である。}\ }$$

**それでも逆方向に per-n C1′ を課す理由(運用規律・数学ではない)**:

1. **陰性主張の登録レジーム**: 非全射は非存在型の主張であり、独立な正経路で裏取りできない。$S$ の宣言だけに依存する licensing は、宣言が誤っていたときに**捕まらない**。
2. **裁定 214 の水準を下げない**: $q=7$ 系の C1′ は「証明書スキーマの $(j,[\alpha])$ 必須欄」として実装される(【C21-d】)。これは $S=\{[\alpha]\}$ を**機械可読な形で**固定する装置であり、$S\subseteq P$ の検証可能性そのものである。
3. ⟹ **本稿の勧告**: C1′(per-n・ラベル同定)は**逆方向では必須のまま**、十分方向では **$S\subseteq P$ が証明書上で判定できるなら** C1′-any(= MATCH-one)へ弱化してよい。**弱化の可否は方向ではなく証明書の内容で決まる。**

## 16. licensing の最終形 —「$[u_n]_{2n}$ を $a_n$ と呼ぶ」

> ### SURJ-fam-APPLY′【gate・正本 §5.2 の差し替え案】
> 総組立 FAM-U-ASM の出力類 $[u_n]_{2n}$ を系 SURJ-fam-K の $a_n=[u_n^{-1}]_{2n}$ として**代入してよい**のは、次を**すべて**満たすときに限る。
>
> | # | gate 項目 | 族版での内容 | 現状 |
> |---|---|---|---|
> | **G-1′** | **【MATCH-one】** | $(5')@\alpha$ と「組立の窓 $=\alpha$」が**同一の $\alpha$** で成立。既定の instantiation は $\alpha=1$(A7-fam の登録主張が $H_n^{\rm fun}=H_{2,1,0}$ ゆえ)であり、そのとき要求は $(5')@H_n^{\rm fun}$ | ⚠ **開**((5′) が UNKNOWN) |
> | **G-2′** | **C5-fam**(§14) | R-1…R-9。とくに $S,P$ の事前凍結と post-hoc narrowing の禁止 | 手続き |
> | **G-3** | **モデル束縛** | R-7(不変) | 開 |
> | **G-4** | **provenance** | R-8(不変) | 手続き |
>
> **系 SURJ-fam-K の真偽は gate に依存しない。** gate が支配するのは「代入してよいか」だけである(F91-5.3 の分離)。
>
> ### ⚠ 条件性の明示(矢印を跨がないための定型文)
> **$(5')$ は UNKNOWN(【GAP-Rcyc】= 比較橋 $B_{\rm FC}$)。したがって本 gate は「$(5')$ 発効後に接合」という条件文としてのみ読む。** 本稿は $[u_n]_{2n}$ の値にも $\mathrm{ord}(a_n)$ にも $\mathrm{Ih}$ の像にも触れておらず、**SURJ を結論しない**。
> ⚠ **正本 §4.3/§5 は $(5')=B_{\rm FC}$ と 橋 **B-1** を同一視している。本稿はその同一視を**引用するだけ**で再導出していない(§18 監査点 4)。もし別物なら G-1′ の未知は 1 本ではなく 2 本になる。

---

## 17. FINDING

| # | 格 | 内容 |
|---|---|---|
| **S3FC-1** | ★★ **族版が立つ** | **(6′) は全奇数 $n\ge3$・全 $\alpha\ne0$ の窓で成立**(定理 SIXP-fam)。前件 (3) も同範囲(補題 Λ-REG)。**有限計算は要らず紙で閉じる**。⟹ 委嘱の「障害札 + per-n 手続き」は発動しない |
| **S3FC-2** | ★★ **依存の会計** | 証明が使うのは**正典 Thm 4.3 (4.12) と ODD-H だけ**。**(W2)-fam も 補題 R′ も枠組み層(TB/BFC)も使わない**。$e=n$ すら (4.12) から直接出る。⟹ $R^{\rm cyc}_{\rm formal}$ の**窓依存の未知は $(5')$ ただ一つ**に確定 |
| **S3FC-3** | ★ **新規性は限定的** | 「(6′) 全奇 $n$ で自動」は `c2c4_closure_v1.md` §2.1・`q7_lower_bound_v1.md` §7 に**既出**。本稿の寄与は**書かれた証明(とくに $\Lambda$ への制限で忠実性が保たれる理由)・$\alpha$ 射程・会計・spot-check** の 4 点。補題 INN は既出(K5-1 / Sol 便 73 (1.13) / w2fam §3.5) |
| **S3FC-4** | ★★ **自己捕獲(第 II 部の中核)** | 正本 §4.3 の**【S3F-A2】+【S3F-A3】は独立の存在量化のままでは接合しない**。系の適用に要るのは **matched な単一存在量化【MATCH-one】**。第 I 部により matched の負担は $(5')$ のみに落ちる |
| **S3FC-5** | ★ **軸の訂正** | 「十分方向は弱化可・逆方向は不可」は**誤った軸**。正しくは **曖昧集合 $S\subseteq$ 前件集合 $P$**。両方向とも同じ要求。逆方向の per-n C1′ は**運用規律**(陰性主張の登録レジーム・裁定 214 の水準維持)として残す |
| **S3FC-6** | ★ **P-S3F-1 の根拠訂正** | 正本の根拠(「同値の左辺が同じ」)は弱すぎる。同値からは「$\mathrm{ord}=n$ の一致」しか出ない。**正しい根拠は $R^{\rm cyc}_{\rm formal}$ 第 2 段の等式 $\mathrm{ord}([u_{n,\alpha}]_{2n})=\lvert\mathrm{Ih}(G_{F_n})\rvert$**(系 ORD-IDX)。予言自体は強い形で生き残る |
| **S3FC-7** | ⚠ **射程遮断** | 定理 SIXP-fam の $\alpha\ne0$ は**前件 (3)(6′) の証明範囲**であって窓族の量化ではない。falsifier **F-1**(非単元は ODD-P passport で層 1/2 と乖離)・**F-2**(群論述語は $\alpha$ 全域で恒真ゆえ識別力ゼロ)に服する。**【ASM-α】は開いたまま**、本稿が供給するのはその (3)(6′) 行だけ |
| **S3FC-8** | ★ **忠実性の在処** | 座標版(§5.1)では忠実性が「**$4$ が $\mathbf Z/n$ で可逆**」の一点に帰着する($\beta\mapsto\beta-4k$)。$n$ が奇であることの使われ方がここに集約する — $n$ 偶では即座に壊れる(正典 (4.12) の分岐と整合) |

## 18. Sol への申し送り(監査点 5・優先順)

1. ★★ **【MATCH-one】の必要性(最重要)**: 「正本 §4.3 の【S3F-A2】と【S3F-A3】は**別々の存在量化**なので、系 SURJ-fam-K の適用には接合しない。要るのは matched な単一存在量化である」— この診断に同意するか。**同意する場合、正本 §4.3 の 2 札を MATCH-one へ差し替えるのが正しい修文か**(それとも A2/A3 を残したうえで「同一 $\alpha$」を注記するだけで足りるか)。
2. ★★ **定理 SIXP-fam の証明の可否**: 核は「$\rho_0$ の忠実性は $\Lambda_\alpha$ への**制限**でも保たれる — なぜなら $\langle X\rangle$ が $\Lambda_\alpha$ に単純推移だから」の一段(補題 Λ-REG)。$\mathrm{Stab}_{\langle X\rangle}(H)=\langle X\rangle\cap N_{G_n}(H)=\langle X\rangle\cap H=1$ の 2 つの等号(前者は正規化群の定義、後者は ODD-H 補題 C(2))に穴はないか。また **$\tau$ の向きの規約**(week4 §5.2.0 注 4)が結論に影響しないという読み(§1 末)に異論はないか。
3. ★ **系 ORD-IDX と P-S3F-1**: $R^{\rm cyc}_{\rm formal}$ の第 2 段を等式として取り出し、$\mathrm{ord}([u_{n,\alpha}]_{2n})=\lvert\mathrm{Ih}_{K^{(n)}}(G_{F_n})\rvert$ を**前件を満たす全窓で**主張してよいか。これが正しければ P-S3F-1 の根拠は差し替わり(★教材)、**測定値が $n$ でないときにも $\lvert\mathrm{Ih}(G_{F_n})\rvert$ が読める**ことになる — この読みに射程の見落としはないか。
4. ★ **$(5')=B_{\rm FC}$ と 橋 B-1 の同一視**: 正本 §5.1/§4.3 はこの 2 つを同じ札として扱っている(【S3F-GAP-2】)。**あなたの設計意図でこれは同一物か**。別物なら G-1′ の未知が 2 本になり、第 II 部の「残る負担は $(5')$ のみ」という会計が崩れる。
5. **方向の軸の訂正(§15)**: 「十分方向/逆方向」ではなく「$S\subseteq P$」が正しい軸である、という診断に同意するか。同意する場合でも、**陰性主張には per-n C1′ を運用規律として残す**という切り分け(数学的要求と登録レジームの分離)で足りるか。

## 19. 【GAP】(隠さず明示・埋めていない)

| 札 | 内容 | 重み |
|---|---|---|
| **【S3FC-GAP-1】** | ★★ **$(5')=B_{\rm FC}$ は UNKNOWN のまま**(= 【GAP-Rcyc】)。第 I 部はこれを一切動かしていない。**第 II 部の gate はすべてこの条件下**である | **重**(不変) |
| **【S3FC-GAP-2】** | **(1) の算術半分($\widetilde\chi\circ\mathrm{Ih}=\chi_{4n}$)は本稿の射程外**(W2-arith Route A・裁定 122 の格のまま)。第 I 部は (1) を使わないが、**第 II 部の定理 APPLY-fam は使う** | 中 |
| **【S3FC-GAP-3】** | **【ASM-α】は開いたまま**。本稿は (3)(6′) 行のみ供給。A7 の他の供給元・層 1/層 2 の passport 整合は未着手 | 中 |
| **【S3FC-GAP-4】** | 本稿は**単系統・Sol 未監査**。補題 Λ-REG・定理 SIXP-fam(の書かれた形)・【MATCH-one】・定理 APPLY-fam・系 ORD-IDX・§15 の軸訂正はいずれも工房内で本稿が初出(**工房外の既知性は未調査**) | — |
| **【S3FC-GAP-5】** | §9.2 の検算は **python 単系統**。cert(GAP)との一致を `cross-checked` と**格付けしていない**(CV-9 仕様同一性判読が未了) | 軽(手続き) |

**「verified」は本稿で一度も使っていない**(Lean 未接続)。**「cross-checked」も使っていない。**

## 20. 出所

| 節 | 主たる出所 |
|---|---|
| §1・§3 | ODD-H **補題 A・C(2)・G・H(3)=(1.3)・I**(`oddH_full_proof_v1.md`)/ week4 v3 **§5.2.0**($\Lambda,\tau,\rho_0$ の型) |
| §4 | **命題 K5-1(W3-15①)/ Sol 便 73 (1.13)** の再掲経由 = `w2fam_v1.md` §3.4/§3.5 / 正典 **Thm 4.3 (4.12)** |
| §5 | 上記 + week4 v3 **§5.2.1(6′)**・**§5.2.3 補題 R′**(比較のみ)/ ODD-H **§11.1/§11.2**(第二経路) |
| §6・§7 | week4 v3 §5.2.3 注 / ODD-H **命題 ODD-P・帰結 F8** / `asm_alpha_falsifier_v1.md` **F-1・F-2・F-3・F-6** / `fam_u_assembly_addendum_C_draft_v1.md` **§C.4【ASM-α】** |
| §9 | `search/certs/s3f_a3_6prime_20260804.json`(裁定 470・**較正**)/ `scratchpad/s3f_sixp_fam_check.py`(本稿) |
| §11–§13 | `s3_family_draft_v1.md` §4.3/§5.1/§3.3 / week4 v3 **§5.2.2 定理 $R^{\rm cyc}_{\rm formal}$ の証明 2**(系 ORD-IDX の出所) |
| §14–§16 | `c21_draft_v1.md` §5.1(C1′/C5)・§7(**命題 A7-fam**)・§9【C21-d】/ 裁定 214 / F91-5.3(定理/gate 分離)/ `fam_u_assembly_v1.md` §1(総組立)・§V.5(距離図) |

### 20.1 【文献要請】

**本稿からの新規はゼロ。** 既出の **【文献要請 G7-2】**(「$p$-深さの下界を値を測らずに出す道具」)と **【文献要請 13/14】**(TB 層)に変更はない。第 I 部が枠組み層を使わずに閉じたことで、**$(5')=B_{\rm FC}$ が窓側の唯一の未知**として一層はっきりした — これは既存要請の**優先度の報告**であって新しい要請ではない。

### 20.2 司令塔への上申(3 点)

1. ★★ **正本 §4.3 の修文**: 【S3F-A2】+【S3F-A3】を **【MATCH-one】** へ差し替えることを提案する(§11)。現行の 2 札は**独立の存在量化**であり、系 SURJ-fam-K の適用を licensing しない。**これは本稿が自分の前便の設計に見つけた欠陥**である。
2. ★ **正本 §8 の P-S3F-1 の根拠差し替え**(§13)。予言自体は生きるが、根拠を「同値の左辺が同じ」から「$R^{\rm cyc}_{\rm formal}$ 第 2 段の等式」へ替える必要がある。★教材として記録されたい。
3. ★ **【ASM-α】の (3)(6′) 行の消し込み**: 本稿の定理 SIXP-fam は【ASM-α】の一部(前件 (3)(6′) の $\alpha$ 一般化)を供給する。**ただし他の行は未着手**であり、【ASM-α】自体を閉じるものではない — 記帳の粒度を分けられたい(falsifier F-1 の射程遮断つき)。
