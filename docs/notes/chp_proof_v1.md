# (CH-p) の直接計算 — 残差の合成則の厳密決定

**状態札: 数学者起草・司令塔検分前・Sol 未監査**
起草: Claude 数学者 / 2026-08-19 / 委嘱 = 司令塔(GS screening §3.4 の勧告の実行)
格: paper candidate(紙上・機械計算ゼロ)。**cross-checked ではなく verified でもない。**
非接触: 封印 3 量・$u$ の**値**・$c$ の値・sealed $K^{(5)}$。$u=2m+1$ は形式変数。
NAME-COLLIDE: $c=(\sigma_1\sigma_2)^3$(正典の中心元)/ 補正元は $\lambda,w$ / $\Phi$ は自由群(Frattini ではない)。

---

## 0. 一行裁定

**(CH-p) は「この道では出ない」。ただし空振りではない — 求められた合成則そのものは厳密に決定でき、しかもそれは予想より良い形(自由対象の上で誤差項ゼロの完全な函手性)で成り立つ。誤差は自由対象から有限窓へ落とすときに初めて生じ、その項を 2 つ(R1)(R2)正確に同定した。副産物として D6($m$ 側補正の帳簿)は完全に閉じ、producer/checker に無料の整合性検査が 1 本増える。GS-T2 は条件付きのまま残り、私の「紙 1〜2 頁で決着」という見積もりは**過大評価だったので訂正する**。**

| 項目 | 結果 |
|---|---|
| **CHP-1** 自由持ち上げ $\tilde T_p\in\mathrm{End}(\Phi)$ と厳密な函手性 $\tilde T_{p_2\ast p_1}=\tilde T_{p_2}\circ\tilde T_{p_1}$ | **証明**(手計算で全ステップ検証) |
| **CHP-2** 全残差の厳密な合成則 $\varrho(p_2\ast p_1)=\tilde T_{p_2}(\varrho(p_1))$(自由対象の中で・**誤差項ゼロ・選択ゼロ**) | **証明**(braid 関係式版は完全検証。operad 版は同一論法・帳簿を flagged) |
| **CHP-3** 有限窓へ落としたときの誤差の正確な同定 | **証明**: $\delta(g_2g_1)\equiv\bar T_{g_2}(\delta(g_1))$ mod $\mathcal I(g_2)$、$\mathcal I(g_2)=\langle\langle\delta(g_2),\Xi(g_2)\rangle\rangle_W$ |
| **(CH-p)**(crossed hom として実現) | **出ない。**(R1) $\Xi(g_2)\ne1$(H 段 shadow は $K$-両立でない)(R2) 誤差が $\delta(g_2)$ ではなく**正規閉包**。(R3) 最寄りの古典的類似では結論自体が偽(反例つき)⟹ 形式的論法では不可能 |
| **D6**($m$ 側補正の帳簿) | **閉鎖。** $m$ 補正と $f$ 補正は $p\ast\lambda$ の単一操作に統一され、CHP-2 が両方を 1 式で処理 |
| **GS-T2**($3\nmid\lvert N\rvert$ ⟹ 全部無害) | **条件付きのまま。** (CH-p) が前件だったので発火しない |
| B4-B | **宣言しない** |

---

## 1. 設定

$K\le H\le M$:isolated 窓($NFI_{PB_4}(B_4)$)。$N=H/K$、$W=H_{PB_3}/K_{PB_3}$。
$\Phi:=F(a,b)$ を階数 2 の自由群、$\pi:\Phi\twoheadrightarrow B_3$ を $a\mapsto\sigma_1$, $b\mapsto\sigma_2$。$B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle$ なので
$$\ker\pi=\langle\langle r\rangle\rangle^\Phi,\qquad r:=aba\,(bab)^{-1}.$$
$F_2=\langle x_{12},x_{23}\rangle$、$x_{12}=\sigma_1^2$、$x_{23}=\sigma_2^2$(2008 (A.4))。
**literal pair** $p=(m,f)$:$m\in\mathbf Z$、$f=f(x_{12},x_{23})\in[F_2,F_2]$ は**語として与えられたもの**。$u:=2m+1$。
**正準持ち上げ**(本書で固定する規約):$\tilde f:=f(a^2,b^2)\in\Phi$。$\pi(\tilde f)=f$ ✓。
**合成**(2008 (2.52)/(2.55)):
$$p_2\ast p_1:=\bigl(2m_1m_2+m_1+m_2,\ \ f_2\cdot E_{p_2}(f_1)\bigr),\qquad E_{p}(x_{12})=x_{12}^{u},\ E_p(x_{23})=f^{-1}x_{23}^{u}f .$$
$u_{p_2\ast p_1}=u_1u_2$(検算:$2(2m_1m_2+m_1+m_2)+1=(2m_1+1)(2m_2+1)$ ✓)。

---

## 2. CHP-1 — 自由持ち上げと厳密な函手性

**定義.** literal pair $p=(m,f)$ に対し
$$\tilde T_p:\Phi\longrightarrow\Phi,\qquad \tilde T_p(a):=a^{u},\qquad \tilde T_p(b):=\tilde f^{-1}\,b^{u}\,\tilde f .$$
$\Phi$ は自由なのでこれは**任意の $p$ について自己準同型として定義される**(窓も shadow 条件も不要)。

**補題 CHP-1.** 任意の literal pair $p_1,p_2$ について
$$\boxed{\ \tilde T_{p_2\ast p_1}\;=\;\tilde T_{p_2}\circ\tilde T_{p_1}\ }\qquad(\text{$\Phi$ の自己準同型として厳密に等しい}).$$

*証明.* $u:=u_1u_2$、$f:=f_2E_{p_2}(f_1)$ と書く。
**(i) $a$ について.** $\tilde T_{p_2}(\tilde T_{p_1}(a))=\tilde T_{p_2}(a^{u_1})=a^{u_1u_2}=a^{u}=\tilde T_{p_2\ast p_1}(a)$ ✓。
**(ii) 正準持ち上げの整合.** $\tilde T_{p_2}(a^2)=a^{2u_2}$、$\tilde T_{p_2}(b^2)=(\tilde f_2^{-1}b^{u_2}\tilde f_2)^2=\tilde f_2^{-1}b^{2u_2}\tilde f_2$。よって
$$\tilde T_{p_2}(\tilde f_1)=\tilde T_{p_2}\bigl(f_1(a^2,b^2)\bigr)=f_1\bigl(a^{2u_2},\ \tilde f_2^{-1}b^{2u_2}\tilde f_2\bigr).$$
一方 $E_{p_2}(f_1)=f_1(x_{12}^{u_2},\,f_2^{-1}x_{23}^{u_2}f_2)$ の正準持ち上げは $f_1(a^{2u_2},\,\tilde f_2^{-1}b^{2u_2}\tilde f_2)$。**両者は語として一致**:
$$\boxed{\ \widetilde{E_{p_2}(f_1)}=\tilde T_{p_2}(\tilde f_1)\ }\qquad\text{よって}\qquad \tilde f=\tilde f_2\cdot\tilde T_{p_2}(\tilde f_1).$$
**(iii) $b$ について.**
$$\tilde T_{p_2}(\tilde T_{p_1}(b))=\tilde T_{p_2}\bigl(\tilde f_1^{-1}b^{u_1}\tilde f_1\bigr)
=\tilde T_{p_2}(\tilde f_1)^{-1}\bigl(\tilde f_2^{-1}b^{u_2}\tilde f_2\bigr)^{u_1}\tilde T_{p_2}(\tilde f_1)$$
$$=\tilde T_{p_2}(\tilde f_1)^{-1}\tilde f_2^{-1}\,b^{u_1u_2}\,\tilde f_2\tilde T_{p_2}(\tilde f_1)
=\bigl(\tilde f_2\tilde T_{p_2}(\tilde f_1)\bigr)^{-1}b^{u}\bigl(\tilde f_2\tilde T_{p_2}(\tilde f_1)\bigr)=\tilde f^{-1}b^u\tilde f=\tilde T_{p_2\ast p_1}(b)\ ✓.$$
生成元で一致し $\Phi$ は自由なので等号。∎

**系 CHP-1'.** literal pair 全体 $\mathcal P$ は $\ast$ について**モノイド**であり、$p\mapsto\tilde T_p$ は $\mathcal P\to\mathrm{End}(\Phi)$ のモノイド準同型。**窓に依存しない。**
> **意味**: 「GT の合成則は自由群の自己準同型の合成そのものである」— (2.52) の $m$-規則と $f$-規則が同時にこれ 1 本から出る。正準持ち上げ規約 $\tilde f=f(a^2,b^2)$ を固定することが鍵(規約を変えると (ii) が壊れる ⟹ **checker はこの規約を明示的に固定すること**)。

---

## 3. CHP-2 — 残差の厳密な合成則(誤差項ゼロ)

### 3.1 一般原理

$\mathcal X=\langle\text{生成元}\mid R_1,\dots,R_k\rangle$ を表示、$\Phi_{\rm free}$ を自由対象、$\pi:\Phi_{\rm free}\to\mathcal X$。生成元の像で定義された自己準同型の族 $\{\tilde T_p\}$ が $\tilde T_{p_2\ast p_1}=\tilde T_{p_2}\tilde T_{p_1}$ を満たすなら、**残差**
$$\varrho_i(p):=\tilde T_p(R_i)\in\Phi_{\rm free}$$
は
$$\boxed{\ \varrho_i(p_2\ast p_1)=\tilde T_{p_2}\bigl(\varrho_i(p_1)\bigr)\ }$$
を**厳密に**満たす(選択なし・誤差項なし)。*証明:* $\varrho_i(p_2\ast p_1)=\tilde T_{p_2\ast p_1}(R_i)=\tilde T_{p_2}(\tilde T_{p_1}(R_i))$。∎

### 3.2 実例 1(完全検証済み)— braid 関係式の残差

$\varrho(p):=\tilde T_p(r)\in\Phi$、$\Delta(p):=\pi(\varrho(p))\in B_3$。
- $T^{B_3}_{p}$ が $B_3\to B_3/N_{PB_3}$ の準同型として降りる $\iff\Delta(p)\in N_{PB_3}$
 (∵ $\hat T_p(\ker\pi)$ は $\Delta(p)^{\pm1}$ の $B_3$-共役で生成され、$N_{PB_3}\trianglelefteq B_3$)。
- 合成則:$\varrho(p_2\ast p_1)=\tilde T_{p_2}(\varrho(p_1))$ ✓(§3.1)。
- 特に **冪の残差**:$\varrho(p^{\ast n})=\tilde T_p^{\,n-1}(\varrho(p))$。

### 3.3 実例 2 — actual な 3 残差(hexagon×2 + pentagon)

2008 **Theorem A.1**(= Fresse Thm 6.2.4;逐語は `docs/notes/ihnec_v1_addendum_e_b4.md:536`)により $\mathrm{PaB}$ は $\alpha,\beta$ で生成され、**全関係式は (A.13) pentagon と (A.14)(A.15) hexagon 2 本の帰結**。従って §3.1 の一般原理が $\mathcal X=\mathrm{PaB}^{\le4}$、$R_1,R_2,R_3=$(hexagon 1, hexagon 2, pentagon)にそのまま適用でき、
$$\boxed{\ \bigl(\varrho_{\rm hex1},\varrho_{\rm hex2},\varrho_{\rm pent}\bigr)(p_2\ast p_1)=\tilde T_{p_2}\Bigl(\bigl(\varrho_{\rm hex1},\varrho_{\rm hex2},\varrho_{\rm pent}\bigr)(p_1)\Bigr)\ }$$
が**自由対象の中で厳密に**成り立つ。有限窓で評価したものが T-38 補題 NA-1 の $(\rho_1,\rho_2,\rho_3)$ である。
> **【要確認 FR-1】** §3.2(群 $B_3$・$\Phi=F(a,b)$)は全ステップを手で検証した。§3.3 は**同一論法**だが、自由 braided monoidal 対象の上での $\tilde T_p$ の定義と $\tilde T_{p_2\ast p_1}=\tilde T_{p_2}\tilde T_{p_1}$ の帳簿は書き下していない(生成元 $\alpha\mapsto\alpha\cdot\mathfrak m(\tilde f)$、$\beta\mapsto\beta\cdot\mathfrak m(\tilde x_{12}^m)$ の合成が (2.52) を再現することの確認)。**紙 1 頁の作業**であり、CHP-1 の (ii) と同型の計算になるはず。

---

## 4. D6 の閉鎖 — $m$ 補正と $f$ 補正の統一

**補題 CHP-D6.** 補正 $(m,f)\mapsto(m+H_{\rm ord}s,\ f\cdot w)$ は、$\mathcal Z_H:=\{\lambda\in\mathcal P:\lambda\equiv(0,1)\bmod(H_{\rm ord},H_{PB_3})\}$ を用いて
$$p\longmapsto p\ast\lambda,\qquad \lambda=(H_{\rm ord}s',\ f_\lambda)\in\mathcal Z_H$$
の形で実現される($w=E_p(f_\lambda)$、$u_{p\ast\lambda}=u_pu_\lambda$)。$\mathcal Z_H$ は $\ast$ について**部分モノイド**($u\equiv1$ は乗法的 ✓、$E_{\lambda_2}(H_{F_2})\subseteq H_{F_2}$ ✓)。このとき CHP-2 から**一式で**
$$\boxed{\ \varrho_i(p\ast\lambda)=\tilde T_p\bigl(\varrho_i(\lambda)\bigr)\ }$$
が従う。特に $\lambda=(0,1)$ で $\varrho_i(p)=\tilde T_p(R_i)$ ✓(整合)。

> **⟹ T-38 の【GAP: D6】は閉じた。** $m$ 側補正($\xi=x_{12}^{H_{\rm ord}}$, $\eta=x_{23}^{H_{\rm ord}}$, $\gamma=c^{H_{\rm ord}}$ の literal 挿入)を個別に帳簿する必要はない — **補正はすべて $\ast\lambda$ という単一操作**であり、残差への効果は $\tilde T_p(\varrho_i(\lambda))$ の一式で尽きる。
> **留保**: $p\ast\mathcal Z_H$ が補正領域 $\Lambda(p)$ **全体**を尽くすかは別問題($w=E_p(f_\lambda)$ が $H_{F_2}/K_{F_2}$ を覆うか = $E_p(H_{F_2})K_{F_2}=H_{F_2}$ か)。覆わない場合、CHP-D6 は**十分条件側**の道具として正しく、必要十分の走査には $\Lambda$ 全体を使うこと ⟹ **新 FC-11**。

---

## 5. (CH-p) の裁定

### 5.1 有限窓へ落とすと何が起きるか(誤差の正確な同定)

$g_1,g_2\in\mathrm{ML}(H)$、literal 代表 $p_1,p_2$、$\delta(p_i):=[\Delta(p_i)]\in W$($shadow at $H$ ゆえ $\Delta(p_i)\in H_{PB_3}$ ✓)。

**補題 CHP-3.** $\hat T_{p_2}:=\pi\circ\tilde T_{p_2}:\Phi\to B_3$ とおくと
$$\Delta(p_2\ast p_1)=\hat T_{p_2}\bigl(\varrho(p_1)\bigr),$$
であり、$\hat T_{p_2}$ は $B_3\to B_3/\mathcal J(p_2)$ を誘導する($\mathcal J(p_2):=$ $\hat T_{p_2}(\ker\pi)$ の $B_3$-正規閉包)。従って
$$\boxed{\ \delta(p_2\ast p_1)\ \equiv\ \bar T_{p_2}\bigl(\delta(p_1)\bigr)\quad\text{in}\quad W/\mathcal I(p_2)\ },\qquad
\mathcal I(p_2)=\bigl\langle\!\bigl\langle\ \delta(p_2),\ \Xi(p_2)\ \bigr\rangle\!\bigr\rangle_W,$$
$$\Xi(p_2):=\bigl[\,T_{p_2}(K_{PB_3})\,K_{PB_3}/K_{PB_3}\,\bigr]\le W .$$
*証明.* 第 1 式は CHP-2 + $\pi$。$\hat T_{p_2}(\ker\pi)$ は $\Delta(p_2)^{\pm1}$ の $\hat T_{p_2}(\Phi)$-共役で生成される。$\mathcal K_K=\pi^{-1}(K_{PB_3})$ 上では $\hat T_{p_2}$ は $T_{p_2}(K_{PB_3})$ を生む。両者の $W$ における正規閉包が $\mathcal I(p_2)$。∎

### 5.2 (CH-p) が出ない理由 — 2 つの誤差項

**(R1) $\Xi(p_2)\ne1$:$H$ 段の shadow は $K$-両立でない。**
crossed hom を得るには $\hat T_{p_2}$ が $W$ 上に降りる必要があり、それは $T_{p_2}(K_{PB_3})\subseteq K_{PB_3}$ と同値。$p_2$ は**$H$ で settled**($\ker T^{PB_3}_{p_2}=H_{PB_3}$)であって $K$ については何も言えない。$\Xi(p_2)=1$ が成り立つのは $p_2$ が $K$ 段まで持ち上がるとき、すなわち $g_2\in J$ のとき **だけ**。
> これは **T-36 補題 T33-L11 と同一の構造的事実**である:「$H$ 段の元は、より細かい窓の上のデータに作用しない — 作用するのは持ち上がる元だけ」。GS screening §1 の (O1)〜(O3) と同じ壁である。

**(R2) 誤差が $\delta(p_2)$ ではなく正規閉包 $\langle\langle\delta(p_2)\rangle\rangle$。**
仮に $\Xi(p_2)=1$ でも、$\hat T_{p_2}(\ker\pi)$ は $\Delta(p_2)$ の**共役の積**であり、どの積になるかは $\varrho(p_1)\in\Phi$ の $\ker\pi$-成分、すなわち $p_1$ に依存する。crossed hom($\mathrm{ob}(g_2g_1)=\mathrm{ob}(g_2)\cdot{}^{g_2}\mathrm{ob}(g_1)$)が要求するのは誤差が**ちょうど $\delta(p_2)$** であることで、正規閉包では足りない。可換 $W$ でも $\langle\langle\delta_2\rangle\rangle=\mathbf F_p[\mathcal G_3]\delta_2\supsetneq\{\delta_2\}$。
> **より細かい不変量は $\varrho(p)\in\Phi$ 自身**であり、そこでは誤差ゼロ(CHP-2)。有限化の際に情報が落ちるのが誤差の出所である。$\tilde T_p(\ker\pi)\subseteq\ker\pi$ なら救えるが、$\tilde T_p(r)=\varrho(p)\notin\ker\pi$(それが残差の定義!)なので救えない。

**(R3) 形式的論法では不可能であることの証拠(反例).**
最寄りの古典的類似(Wells 型:$1\to V\to E\to Q\to1$、$\mathrm{Aut}(E)\to\mathrm{Aut}(Q)$ の像の指数は $|V|$ の素因子のみか?)は**偽**である。
$$Q=C_2^2,\quad V=\mathbf F_5,\quad \chi:Q\to\mathrm{Aut}(V)=\mathbf F_5^\times,\ \mathrm{im}\,\chi=\{\pm1\},\quad E=V\rtimes_\chi Q\ (|E|=20).$$
$V$ は $E$ の唯一の Sylow 5 ゆえ characteristic。$\mathrm{Aut}(V)$ 可換なので、誘導 $\theta_Q\in\mathrm{Aut}(Q)$ は $\chi$ を保たねばならず $\ker\chi$ を固定 ⟹ 像 $=\mathrm{Stab}_{S_3}(\ker\chi)\cong C_2$、**指数 3**。しかし $|V|=5$ で $3\nmid5^k$。∎
⟹ **(CH-p) は純形式的には成立しない。** 成立するとすれば GT 固有の入力(T33-L8:compatibility 段階が存在しない)を使う証明が要る。本書の計算は、その GT 固有性が (R1) では**効かない**ことを示している(GT でも「作用しない」は同じ形で起きる)。

### 5.3 裁定

> **(CH-p) は本計算では得られない。反証でもない**(上の (R3) は類似の反例であって GT 系の反例ではない)。正確には:
> - **crossed hom の骨格は自由対象の上で完全に成立する**(CHP-2、誤差ゼロ)。
> - **有限窓へ落とすと (R1)(R2) の 2 つの誤差項が発生し、(R1) は $J$ の外では原理的に消えない。**
> - 従って (CH-p) を目指すなら、狙うべきは「crossed hom を作る」ではなく「**$\Xi(p_2)$ を制御する**」= 「$H$ 段 shadow の $K$-両立性の欠如を測る」ことである。これは T33-L11 / GS §1 (O1) と同じ標的に合流する。

---

## 6. GS-T2 への影響と自己訂正

- **GS-T2($3\nmid|N|\Rightarrow$ 全部無害)は発火しない。** 前件 (CH-p) が得られなかったため。$p\ne3$ の elementary 層も Suzuki 型も、**依然として個別に扱う必要がある**。
- **自己訂正**: GS screening §3.4 で私は「(CH-p) は紙 1〜2 頁の直接計算で決着する見込みが高い」と書いた。**これは過大評価だった。** 実際に計算すると、合成則自体は 1 頁で厳密に出る(CHP-1/CHP-2)が、それが crossed hom に**ならない**理由が構造的(R1)であり、1〜2 頁で埋まる種類のギャップではない。勧告を出した者として明記する。
- **【文献要請の絞り込み】** T-36 §2.5 に添えた要請は広すぎた。正しい要請は:
 > 困難: 有限表示から定まる残差 $\varrho(p)=\tilde T_p(R)$ が自由対象上では完全に函手的($\varrho(p_2p_1)=\tilde T_{p_2}\varrho(p_1)$)であるのに、有限商へ落とすと「関係子の正規閉包」だけ不定になる。欲しい結果の型:**この不定性を、関係加群 $\ker\pi/[\ker\pi,\ker\pi]$ 上の $\mathbf Z[B_3]$-加群論で $\delta(p_2)$ の生成する部分加群へ縮約する定理**(= Fox/Jacobi 型の「relation module による正規閉包の線形化」)。可換係数なら $\langle\langle\delta_2\rangle\rangle=\mathbf Z[\mathcal G_3]\delta_2$ となり、crossed hom ではなく「**$\mathbf Z[\mathcal G_3]$-捻れ crossed hom**」になる — その場合の指数評価定理があるか。

---

## 7. 使える形になったもの(実務への還元)

1. **checker symmetry(無料の独立検査).** producer が $g_1,g_2$ とその残差を出したら、checker は $\varrho(p_2\ast p_1)=\tilde T_{p_2}(\varrho(p_1))$ を**独立に**検証できる(自由群の語計算のみ・群環不要)。誤差項ゼロなので**厳密な等式検査**である。OBS-NA / NA-5 の受領票に組み込める。
2. **正準表現の固定.** CHP-1 は literal pair の代表選択の曖昧さを消す:$p\leftrightarrow\tilde T_p\in\mathrm{End}(\Phi)$ が単射的な正規形を与える(規約 $\tilde f=f(a^2,b^2)$ を固定すること)。T-38 の D2(共役子の $\mathrm{Aut}$ 像)の帳簿もこの規約の上で一意化される。
3. **D6 閉鎖**(§4)。補正は $\ast\lambda$ の単一操作。
4. **冪の残差公式** $\varrho(p^{\ast n})=\tilde T_p^{\,n-1}(\varrho(p))$ — NA-5 で Sylow 3 生成元を扱うとき、生成元の冪の残差を再計算せずに済む。

---

## 8. 新規の有限検査

| 番号 | 検査 | 由来 |
|---|---|---|
| **FR-1** | §3.3 の自由 operad 版帳簿(生成元 $\alpha,\beta$ の合成が (2.52) を再現するか) | §3.3 |
| **FC-11** | $E_p(H_{F_2})\,K_{F_2}=H_{F_2}$ か(= $p\ast\mathcal Z_H$ が補正領域 $\Lambda(p)$ を尽くすか) | §4 の留保 |
| **FC-12** | 与えられた $H$ 段 shadow $p_2$ について $\Xi(p_2)=[T_{p_2}(K_{PB_3})]\le W$ を実測(= $K$-両立性の欠如の大きさ) | §5.2 (R1)。(CH-p) 再挑戦の唯一の入口 |

---

## 9. novelty grep 領収書(2026-08-19)

| 語彙 | 結果 | 扱い |
|---|---|---|
| 合成則 $m=2m_1m_2+m_1+m_2$ | 既在(`157bh:234`, `157o:25`, `157q:29`, 2008 (2.52)) | 引用 |
| $E_{m,f}$($F_2$ 上の自己準同型) | 既在(`152_b3_direct_terminal:48-49`) | 引用。**自由群 $\Phi=F(a,b)$ への正準持ち上げ $\tilde T_p$ と厳密函手性は grep 範囲で該当なし** ⟹ CHP-1 は新規 |
| 残差の合成則 / $\varrho(p_2p_1)=\tilde T_{p_2}\varrho(p_1)$ | **該当なし** | **CHP-2 は新規** |
| crossed homomorphism | 既在(`157bh:276` は Cohen–Wu 商について**否定的**判定;T-36 §2.5 と GS §3.3 は自書) | (R1)(R2) による本書の否定判定は、`157bh` の否定と**同方向**(独立事例) |
| Theorem A.1 の逐語 | 既在(`ihnec_v1_addendum_e_b4.md:536`・外部引用として格を申告済) | §3.3 で引用。**格は「正典+未入手外部定理」を継承** |
| Wells 型の指数反例($V\rtimes_\chi Q$) | 該当なし | (R3) は新規(ただし古典的に自明な例) |

---

## 10. 申告

- 全結果 paper candidate。機械計算ゼロ。**cross-checked ではなく verified でもない。**
- 手計算で全ステップ検証したのは **CHP-1**(§2)と **CHP-2 の braid 関係式版**(§3.2)、**CHP-3**(§5.1)、**(R3) の反例**(§5.2)。
- **【要確認 FR-1】** §3.3(operad 版)は同一論法だが帳簿未記述。
- **UNKNOWN**: (CH-p) の真偽(本書は「この道では出ない」であって反証ではない)。$\Xi(p_2)$ の大きさ。FC-11。
- **自己訂正 1 件**: GS screening §3.4 の「紙 1〜2 頁で決着」という見積もりは過大評価だった(§6)。
- Theorem A.1 に依拠する部分は **未入手外部定理(Fresse Thm 6.2.4)への依存**を継承する(既在 `ihnec_v1_addendum_e_b4.md:752` の格申告と同じ)。
- **B4-B は宣言していない。**

---

# Erratum / 追補(2026-08-19・Sol T-42 監査を受けて。本文 §0–§10 は凍結・以下は追記のみ)

出典: `ops/express/20260819_sol_fable_t42_audit.md`。2 件とも**独立に検算し、両方とも Sol が正しい**。

## E-1 【訂正】D6 は「完全閉鎖」ではない — ただし修理可能(仮説の追加ではなく**規約の追加**)

### E-1.1 Sol の指摘の独立検算 — 正しい

$p\ast\lambda$ の $m$-成分は $m=2m_pm_\lambda+m_p+m_\lambda=m_p+m_\lambda(2m_p+1)=m_p+m_\lambda u_p$。$m_\lambda=H_{\rm ord}s'$ とすると
$$\boxed{\ m_{\rm new}=m_p+H_{\rm ord}\,u_p\,s'\ }$$
従って $s'$ を $\mathbf Z/(K_{\rm ord}/H_{\rm ord})$ 全体で振っても、$m_{\rm new}$ が $m_p+H_{\rm ord}\mathbf Z/K_{\rm ord}\mathbf Z$ を**尽くすのは $u_p$ が $\bmod\ (K_{\rm ord}/H_{\rm ord})$ 可逆なときに限る**。$H$ 段 friendly $\gcd(u_p,H_{\rm ord})=1$ からはこれは従わない($K_{\rm ord}/H_{\rm ord}$ が $H_{\rm ord}$ を割らない新素数を含み得る)。**Sol の指摘は正しい。§4 の「D6 完全閉鎖」は言い過ぎだった。**

**合成順の入替は効かない**(司令塔の候補 1 の否定): $\lambda\ast p$ の $m$-成分は $m_\lambda+m_pu_\lambda=H_{\rm ord}s'+m_p(1+2H_{\rm ord}s')=m_p+H_{\rm ord}s'u_p$ で、$p\ast\lambda$ と**恒等的に同じ**((2.52) の $m$-規則が $m_1,m_2$ について対称なため)。

### E-1.2 修理 — 代表元の正規化で閉じる(条件ではなく規約)

**補題 E-1.** $K$ 段の friendly gate は $\gcd(2m'+1,K_{\rm ord})=1$ を要求し、$2m'+1=u_pu_\lambda$ なので **$\gcd(u_p,K_{\rm ord})=1$ は必要条件**である。$K_{\rm ord}/H_{\rm ord}\mid K_{\rm ord}$ ゆえ、そこから $\gcd(u_p,K_{\rm ord}/H_{\rm ord})=1$ が**自動で従う**。
**補題 E-2(正規化の存在).** $H$ 段 shadow の任意のクラスに対し、$\gcd(2m_p+1,K_{\rm ord})=1$ を満たす literal 代表 $m_p$ が**必ず存在する**。
*証明.* $m$ を $m_p+H_{\rm ord}\mathbf Z$ で動かすと $2m+1$ は $2m_p+1+2H_{\rm ord}\mathbf Z$ を動く。$\ell\mid K_{\rm ord}$、$\ell\nmid H_{\rm ord}$ なる素数は奇数($2m+1$ は常に奇数なので $\ell=2$ は自動回避)で $\gcd(2H_{\rm ord},\ell)=1$、よって $2m+1$ は $\bmod\ \ell$ の全剰余を取る ⟹ $0$ を避けられる。有限個の $\ell$ に CRT。$\ell\mid H_{\rm ord}$ の側は $H$ 段 friendly で既に回避済み。∎

⟹ **修理**: CHP-1 の正準持ち上げ規約に**もう 1 本の規約**を加える:
> **規約 N2**: literal 代表 $m_p$ は $\gcd(2m_p+1,K_{\rm ord})=1$ を満たすものを取る(補題 E-2 で常に可能、補題 E-1 で $K$ 段 friendly の必要条件でもあるので**何も失わない**)。

この規約の下で $u_p$ は $\bmod\ (K_{\rm ord}/H_{\rm ord})$ 可逆となり、**$p\ast\mathcal Z_H$ は $m$-方向の補正を尽くす** ⟹ §4 の被覆は回復する。

### E-1.3 用途側の要件(司令塔の候補 3)— 先に確定しておく

NA-5 が要求するのは「Sylow 3-部分群の生成系 2〜3 元の**各々に**、$K$ 段の shadow が 1 つ」であって $m$-方向の**全被覆ではない**。従って規約 N2 が万一使えない場面でも、必要なのは「各 $f$-成分に対し friendly な $m'$ が 1 つ」に過ぎない。⟹ **被覆命題は用途に対して過剰**であり、E-1.2 の修理は十分以上である。

### E-1.4 帳簿の修正(格の確定)

| 項目 | 旧 | 新 |
|---|---|---|
| D6($m$ 側補正の帳簿) | 「完全閉鎖」 | **braid 版(hexagon 残差)について閉。前件は規約 N2(常に充足可能なので実質無条件)。** |
| pentagon 残差の補正帳簿 | (D6 に含めていた) | **FR-1 待ち**(§3.3 の自由 operad 版帳簿が未記帳なので、braid 版 CHP-2 だけでは pentagon 側の補正則は保証されない)。Sol の第 2 指摘は正しい |

⟹ **D6 は「条件付き閉」ではなく「braid 版は閉(規約つき)・pentagon 版は FR-1 条件付き」**と記録する。FC-11(補正領域の被覆)は E-1.2 により $m$ 方向は解決、$f$ 方向($E_p(H_{F_2})K_{F_2}=H_{F_2}$)は**未解決のまま維持**。

## E-2 【重大な自己訂正】GS-T2 は (CH-p) とは独立に、第二の理由でも死んでいる

Sol の指摘: **crossed homomorphism の zero-fibre index は affine 軌道サイズであり、係数群の位数の素因子とは限らない。**

### E-2.1 独立検算 — 正しい

$\omega:G\to\mathcal O$ を crossed hom($\omega(g_1g_2)=\omega(g_1)+g_1\omega(g_2)$)、$J:=\omega^{-1}(0)$ とすると
$$\omega(g_1^{-1}g_2)=g_1^{-1}\bigl(\omega(g_2)-\omega(g_1)\bigr)\ \Longrightarrow\ \omega(g_1)=\omega(g_2)\iff g_1^{-1}g_2\in J$$
すなわち $\omega$ のファイバーは $J$ の剰余類で、$[G:J]=|\operatorname{im}\omega|$。**しかし $\operatorname{im}\omega$ は一般に部分群ではない**ので、$|\operatorname{im}\omega|$ が $|\mathcal O|$ を割る保証はない。
**Sol の反例(検算済み)**: $G=C_3$ が $\mathcal O=C_7$ に非自明に作用($3\mid7-1$)。$\gcd(3,7)=1$ より $H^1(C_3,C_7)=0$ なので $\omega(g)=(g-1)a$。$a\ne0$ なら $J=\operatorname{Stab}_{C_3}(a)=1$ で **$[G:J]=3$、$|\mathcal O|=7$、$3\nmid7^k$** ✓。

### E-2.2 影響 — 私の 2 文書に同一の誤りがある

- **T-36 §2.5 命題 T33-P2**:「(CH-p) が成り立てば $[\mathrm{ML}(K):J]=|\operatorname{im\,ob}|$ は $p$ 冪」— **誤り**($|\operatorname{im}\omega|$ が $|\mathcal O|$ を割るとは限らない)。
- **GS screening §3.3 命題 GS-T2** の証明中「$[\mathrm{ML}(H):J]=|\operatorname{im\,ob}|$ は $|\mathcal O|$ を割り、これは $3'$-数」— **同じ誤り**。
⟹ **GS-T2 は (CH-p) の成否と無関係に、この段階で既に破れている。** Sol の「第二の殺し」という位置づけは正確である。

### E-2.3 修理可能性 — 一般には不可

Sylow に制限しても救えない: $S\in\mathrm{Syl}_3(G)$、$\mathcal O$ が $3'$-群なら $H^1(S,\mathcal O)=1$(coprime)なので $\omega|_S$ は principal $\omega(s)=(s-1)a$、$J\cap S=\operatorname{Stab}_S(a)$ で $[S:J\cap S]$ は $3$ 冪(1 とは限らない)。E-2.1 の反例が $S=C_3$ でまさにこの形。⟹ **救えない。**
**唯一の修理**: $\operatorname{im}\omega$ が部分群であること(例えば $G$ の $\mathcal O$ への作用が自明で $\omega$ が真の準同型)を追加要求する。従って将来の再挑戦で狙うべきは
> **(CH-p′)**: 障害写像が **$3'$-群への真の準同型**(または zero-fibre index が直接 $3'$-数)であること。
であって、単なる crossed hom ではない。**(CH-p) だけでは足りない** — これが本追補の最重要の帰結である。

### E-2.4 生き残るもの

- **T33-T2(SYL3)は無傷**。crossed hom を使わず Sylow と Lagrange($243\nmid324$)だけで動く ✓。
- **NA-5 も無傷**($J$ が部分群であることしか使わない)✓。
- **CHP-1 / CHP-2 / CHP-3 / D6(E-1 修理後)も無傷** ✓。
- 従って主線(D1 / NA-5 の直接有限方程式)は影響を受けない。**Sol の「FC-12 の $\Xi$ 実測は有用な前処理だが単独では SYL3 の index 条件を与えない・主線は D1/NA-5」という結論に同意する。**

## E-3 申告(追補分)

- E-1.1、補題 E-1、補題 E-2、E-1.1 の合成順対称性、E-2.1 の crossed hom ファイバー計算と $C_3\curvearrowright C_7$ 反例 — すべて手計算で検証した。
- **自己訂正 2 件**: §4「D6 完全閉鎖」→ E-1.4 の格へ。T33-P2 / GS-T2 の index 議論 → E-2 で撤回。
- 影響先へのポインタ: `docs/notes/t33_answer_draft_v1.md` §2.5(T33-P2)、`docs/notes/gs_tower_screening_v1.md` §3.3(GS-T2)。両文書は凍結済みなので、それぞれ 1 行の erratum ポインタのみ追記した。
- **B4-B は宣言していない。**
