# (6.3) tower compatibility — 数値偵察と形の確定 **v1**

2026-07-28: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱(裁定 104・研究リーダー新方針「値からの推測による発案は全面解禁/証明なしの採用禁止は維持」)。
**状態札**: `candidate / 単系統・未監査`。**commit していない。**
**依拠**: 正典(BFC v2.15・TB4 v2.5・Rule 1 v1.5)+ `docs/manifest_k5_appendixA_v1.md` §2(K³ 実測値)+ `docs/notes/hfun_functoriality_v1.md`(HF-1/HF-2)+ `sol/sol_reply_73_math.md` Q5.3/Q6.2。**外部文献なし。**

> ## 封印遵守
> **封印 3 量($u_9/a_9$ の値・$c$ の平方類・$\hat c_\mu$)に一切接触していない。** 使ったのは **$K^{(3)}$ の公開実測値 $u_3=-4$**(`manifest_k5_appendixA_v1.md` §2・`search/week4-u-k3.mjs` 16/16 PASS)と幾何・群論のみ。**$u_9$ を計算・推定していない。**
> ⚠ ただし §5 の予測は**$\mathrm{ord}(a_9)$ の値を条件つきで言い当てる**。**これは封印の趣旨に照らして予言先行(pre-registration)として扱うべきもの**であり、本書を測定より先に凍結・記録することを求める。

---

## 1. 使える値と幾何の棚卸し

| # | 資産 | 値/内容 | 出所 | 封印 |
|---|---|---|---|---|
| A1 | $u_3$ | $\boxed{-4}$、$\mathrm{ord}([u_3^{-1}]_6)=3$(full depth $e=3$) | appendixA §2(検算 (9)(10)(11)(12)) | **公開** |
| A2 | $u_3'$(covariance control) | $-256/729$、$[u_3]_3=[u_3']_3$ | 同上(検算 (13)–(16)) | 公開 |
| A3 | $K^{(3)}$ の局所データ | $P_0=(x,t)=(0,0)$、uniformizer $=x$($\mathbb Q$-有理)、$t=4x^6+O(x^7)$ | 同上 | 公開 |
| A4 | 体の塔 | $F_3=\mathbb Q(\zeta_{12})\subset F_9=\mathbb Q(\zeta_{36})$($12\mid36$)、$\Phi_{36}=T^{12}-T^6+1$ | 族条項・本書 §1 | 公開 |
| A5 | cover $\bar\pi_{9,3}$ | $P_9/H_9^{\rm fun}\to P_3/H_3^{\rm fun}$、次数 $3$、$\langle X\rangle$-同変、poset functorial | **HF-2**(証明済) | 公開 |
| A6 | cusp の分岐 | $M_n=\mathrm{ord}(X_n)=2n$、$\lambda_n^{-1}(0)=\{P_0^{(n)}\}$ 全分岐 | **HF-1(b)(c)** + (W4) | 公開 |
| A7 | 局所 Kummer | $\lambda=u\,s^M(1+O(s))$、$[u]_M$ は uniformizer・モデル非依存 | BFC 補題 B-5(ii-loc)(ii-win) | 公開 |
| — | $u_9$・$a_9$・$c$ 平方類・$\hat c_\mu$ | — | — | **封印(触れない)** |

---

## 2. 幾何の計算 — **形の確定**

### 2.1 cover の存在と cusp での挙動

**HF-2** は $\bar\pi_{n,d}$ を $\hat F_2$-集合の射として与える。$\bar N_n\subseteq\bar N_d$($\pi_{n,d}$ が marked ゆえ $\hat F_2\to P_n\to P_d$ が $\hat F_2\to P_d$ に一致)なので、(TB1) の圏同値により $U$ 上の被覆の射
$$ \rho:=\rho_{n,d}:\ W_n\longrightarrow W_d,\qquad \deg\rho=n/d,\qquad \boxed{\ \lambda_d\circ\rho=\lambda_n\ } \tag{2.1} $$
が対応する。

**cusp**: $\lambda_n^{-1}(0)=\{P_0^{(n)}\}$(A6)と (2.1) より $\rho(P_0^{(n)})\in\lambda_d^{-1}(0)=\{P_0^{(d)}\}$、すなわち $\rho(P_0^{(n)})=P_0^{(d)}$。分岐指数の乗法性から
$$ 2n=e(\lambda_n,P_0^{(n)})=e(\rho,P_0^{(n)})\cdot e(\lambda_d,P_0^{(d)})=e(\rho,P_0^{(n)})\cdot 2d $$
$$ \Longrightarrow\quad \boxed{\ e(\rho,P_0^{(n)})=n/d=\deg\rho\ }\quad(\rho\ \text{は cusp で\textbf{全分岐}}). \tag{2.2} $$

### 2.2 局所展開 — 主係数の関係

$s_n,s_d$ を $P_0^{(n)},P_0^{(d)}$ の有理 uniformizer とする。(2.2) より
$$ \rho^*s_d\ =\ w\,s_n^{\,n/d}\bigl(1+O(s_n)\bigr),\qquad w\in F_n^\times . $$
$\lambda_d=u_d\,s_d^{2d}(1+O(s_d))$ を引き戻すと
$$ \lambda_n=\rho^*\lambda_d=u_d\,w^{2d}\,s_n^{2n}\bigl(1+O(s_n)\bigr), $$
他方 $\lambda_n=u_n s_n^{2n}(1+O(s_n))$。主係数を比較して

$$ \boxed{\ \textbf{(T)}\qquad u_n\ =\ u_d\cdot w^{2d},\qquad w\in F_n^\times\ } \tag{2.3} $$

**uniformizer 非依存の確認**: $s_d\mapsto a's_d(1+\cdots)$ で $u_d\mapsto u_da'^{-2d}$, $w\mapsto a'w$ ⇒ (2.3) 不変。$s_n\mapsto as_n(1+\cdots)$ で $u_n\mapsto u_na^{-2n}$, $w\mapsto wa^{-n/d}$ ⇒ 不変 ✓。**したがって (T) は class の等式として意味をもつ。**

### 2.3 **形の確定 — Sol (6.3) の型を直す**

$v_m:=u_m^{-1}$、$a_m:=[v_m]_{2m}\in F_m^\times/F_m^{\times2m}$(BFC (7.2) の torsor 類)。

**(i) class 語での正しい形**: (2.3) より $v_n=v_d\,w^{-2d}$、ゆえに
$$ \boxed{\ \textbf{(6.3-cls)}\qquad \mathrm{res}_{F_n/F_d}\bigl(a_d\bigr)\ =\ \mathrm{pr}_{2n\to2d}\bigl(a_n\bigr)\quad\text{in }\ F_n^\times/F_n^{\times2d}\ } $$
ここで $\mathrm{res}$ は体の包含 $F_d\hookrightarrow F_n$ が誘導する写像、$\mathrm{pr}$ は $2d\mid2n$ による**射影**。**冪乗は現れない。**

**(ii) character 語での正しい形**: $\kappa^{(m)}_v(\gamma):=\gamma(v^{1/m})/v^{1/m}$ と置く。$v_n^{1/2d}:=(v_n^{1/2n})^{n/d}$、$v_d^{1/2d}:=v_n^{1/2d}w$ と取ると、$\gamma\in G_{F_n}$ は $w$ を固定するので
$$ \kappa^{(2d)}_{v_d}(\gamma)=\frac{\gamma(v_n^{1/2d})}{v_n^{1/2d}}=\Bigl(\frac{\gamma(v_n^{1/2n})}{v_n^{1/2n}}\Bigr)^{n/d}=\bigl(\kappa^{(2n)}_{v_n}(\gamma)\bigr)^{n/d} $$
$$ \boxed{\ \textbf{(6.3-chr)}\qquad \mathrm{res}_{G_{F_n}}\bigl(\kappa_{v_d}^{(2d)}\bigr)\ =\ \bigl(\kappa_{v_n}^{(2n)}\bigr)^{\,n/d}\ } $$

**(iii) 二つは同値である。** Kummer 同型 $\delta_m:F^\times/F^{\times m}\xrightarrow{\sim}\mathrm{Hom}(G_F,\mu_m)$ の下で
$$ \delta_{2d}\bigl(\mathrm{pr}_{2n\to2d}(x)\bigr)=\delta_{2n}(x)^{\,n/d} $$
が恒等的に成り立つ(**射影 $\leftrightarrow$ $\tfrac{m}{m'}$ 乗**)。したがって $n/d$ 乗は **character 側の射影の姿**である。

> ### ⚠ Sol (6.3) の型混同(本偵察の第一の発見)
> Sol の (6.3) は
> $$ \mathrm{res}_{F_n/F_d}(a_d)=a_n^{\,n/d}\quad\text{in }F_n^\times/F_n^{\times2d} $$
> と書く。**左辺と所属先は class 語**だが、**右辺の $n/d$ 乗は character 語の姿**である。class 語で $a_n^{n/d}$ を素直に読むと $[v_n^{n/d}]_{2d}$ となり、正しい $[v_n]_{2d}$ と**一般には異なる**($v_n^{(n/d)-1}\in F_n^{\times2d}$ の理由がない)。
> **⇒ 数学的核は Sol が正しい**(cover functoriality から出る)。**直すべきは語の型**であり、(6.3-cls) と (6.3-chr) のどちらかに統一すること。**★教材 T5「同じ glyph は同じ object ではない」の、量ではなく*語*の版。**

### 2.4 委嘱の 3 つの問いへの回答

| 問い | 回答 | 根拠 |
|---|---|---|
| **res の向き**($F_d\hookrightarrow F_n$ の像か norm か) | **res(包含による引き戻し)。norm ではない。** | (2.1) が与えるのは $\lambda_n=\rho^*\lambda_d$ という**引き戻し**であり、$F_d\subset F_n$ 方向にしか幾何的源がない |
| **指数** | **class 語では冪なし(射影)/ character 語では $n/d$。$2d$ を法とするのが正しい**($2n$ ではない) | (2.3) の $w^{2d}$。$w$ は $2d$ 乗でしか現れない |
| **正規化(単数倍)** | **自由度は $w\in F_n^\times$ ちょうど一つで、$2d$ 乗の形でしか効かない。uniformizer の取り替えに対し (T) は不変**(§2.2) | 直接計算 |

---

## 3. 証明戦略

**(2.3) は既に証明の形をしている。** 残る依存を名前つきで挙げる。

| # | 要る補題 | 状態 | 再利用元 |
|---|---|---|---|
| G1 | $\bar N_n\subseteq\bar N_d$(marked quotient) | **証明済**($\hat F_2\to P_n\to P_d$ が $x,y$ 上で $\hat F_2\to P_d$ に一致・HF-2 の marked 性) | HF-2 §1 |
| G2 | $\bar\pi_{n,d}$ が $\hat F_2$-集合の射 | **証明済** | HF-2(a)(c) |
| G3 | $\bar\pi_{n,d}$ が $G_{F_n}$-同変 ⇒ $F_n$ 上へ descend | **要記述**。$\alpha^{\rm std}_\gamma$ が両 $\bar N$ を保つ((W1) を両段で)+ $\pi_{n,d}$ と可換 ⇒ 従う | (W1)・BFC 定理 B-4 |
| G4 | (TB1) の圏同値で $\bar\pi\rightsquigarrow\rho$、$\lambda_d\circ\rho=\lambda_n$ | **標準**(枠組み) | (TB1) |
| G5 | $\lambda_n^{-1}(0)$ が 1 点・全分岐指数 $2n$ | **証明済**((W4)+HF-1(b)(c)) | BFC 補題 B-5(i)・HF-1 |
| G6 | $[u]_M$ の uniformizer/モデル非依存 | **証明済** | BFC 補題 B-5(ii-loc)(ii-win) |
| G7 | $P_0^{(m)}$ が $F_m$-有理・有理 uniformizer の存在 | **証明済** | BFC 補題 B-5(i)(ii) |

$$ \boxed{\ \text{⇒ (6.3-cls) は \textbf{G3 を書き下せば紙上で閉じる}。「値から推測した式」ではなく「幾何から導いた式」である。}\ } $$

**$K^{(3)}$ の 16 検算のうち再利用可なもの**: (7)(8)($P_0$ と uniformizer・$t=4x^6+O(x^7)$)/ (9)($u=-4$)/ (10)(11)(12)($\mathrm{ord}([u^{-1}]_6)=3$)/ (13)–(16)(covariance: $[u]_3=[u']_3$ — **(T) の下段側の不変性検査として直接効く**)。**(1)–(6)(モデル・分岐割当)は $n=3$ 固有で $n=9$ には移らない。**

---

## 4. 反例可能性(破れ方の分類)

| 破れ方 | 症状 | 致命度 | 救済 |
|---|---|---|---|
| **B1 単数倍のズレ** $u_n=u_d\,\varepsilon\,w^{2d}$($\varepsilon\in\mathcal O_{F_n}^\times$) | class 等式が $\varepsilon$ だけずれる | **軽**。$[\varepsilon]_{2d}=1$ なら無害 | 弱い形「$\mathrm{res}(a_d)\,\mathrm{pr}(a_n)^{-1}\in\langle\text{単数の像}\rangle$」で救える |
| **B2 指数ズレ**($w^{2d}$ が $w^{2n}$ や $w^{d}$ だった) | 法が変わり、$a_9$ の決定範囲が変わる | **致命**。§5 の予測が壊れる | 救済なし。(2.2) の $e(\rho)=n/d$ を再検証するしかない |
| **B3 向きのズレ**(res でなく norm) | $F_n\to F_d$ 方向になり $u_3$ から $u_9$ を縛れない | **致命**(用途が消える) | (2.1) の引き戻しを再検証 |
| **B4 cover の非存在**(G3 が破れる) | $\rho$ が $F_n$ 上に降りない | **致命** | $F_n$ 上でなく $\bar{\mathbb Q}$ 上でだけ成立 ⇒ Galois 降下の障害を別に測る |
| **B5 窓の取り違え**($K^{(3)}$ の実測窓 $\ne H_3^{\rm fun}$) | $u_3$ が塔の下段の値でない | **致命(用途に対して)** | §5 の caveat C1。**最優先で潰すべき** |

---

## 5. **予言先行(pre-registration)— 条件つき予測**

**(6.3-cls) を認めると、$u_9$ を一切見ずに $\mathcal P_{9,3}$ が決まる。**

**(a) $\mathcal P_{9,3}$ は射影で書ける。** $n=9$、$2n=18$。$\mu_3\subset F_9^{\times6}$($\zeta_3=\zeta_{36}^{12}=(\zeta_{36}^2)^6$)より
$$ a_9^{\,3}=1\ \text{in }F_9^\times/F_9^{\times18} \iff v_9^3\in F_9^{\times18} \iff v_9\in\mu_3\cdot F_9^{\times6}=F_9^{\times6} \iff \mathrm{pr}_{18\to6}(a_9)=1 . $$
$$ \boxed{\ \mathcal P_{9,3}\ =\ \bigl[\ \mathrm{pr}_{18\to6}(a_9)\ne1\ \bigr]\ } $$

**(b) (6.3-cls) はまさにその射影を与える**($d=3$、$2d=6$):
$$ \mathrm{pr}_{18\to6}(a_9)=\mathrm{res}_{F_9/F_3}(a_3)=[\,v_3\,]_6=[-1/4]_6\ \in F_9^\times/F_9^{\times6}. $$

**(c) $[-1/4]_6\ne1$ を証明する。** $F_9^{\times6}=F_9^{\times2}\cap F_9^{\times3}$($\gcd(2,3)=1$;$x=a^2=b^3\Rightarrow(b^2/a)^6=x$)。
- $-1/4\in F_9^{\times2}$: $i=\zeta_{36}^9\in F_9$ ゆえ $-1/4=(i/2)^2$ ✓。
- $-1/4\in F_9^{\times3}\iff-4\in F_9^{\times3}\iff4\in F_9^{\times3}\iff2\in F_9^{\times3}$($-1=(-1)^3$;$\gcd(2,3)=1$ ゆえ $2^2$ が立方 $\iff2$ が立方)。
- **$2\notin F_9^{\times3}$**: もし $2=y^3$($y\in F_9$)なら $\mathbb Q(y)$ は $\mathbb Q$ 上 3 次で $\mathbb Q(2^{1/3})$ と同型、とくに $\mathbb Q$ 上**非正規**。しかし $F_9=\mathbb Q(\zeta_{36})$ は $\mathbb Q$ 上**アーベル**で、その部分体はすべて $\mathbb Q$ 上正規。矛盾 ✓。

$$ \Longrightarrow\ \mathrm{pr}_{18\to6}(a_9)=[-1/4]_6\ \textbf{の位数は }3\ (\ne1). $$

> ### 予測 T63-P1(**条件つき・値を見ずに導出**)
> $$ \boxed{\ \text{(6.3-cls) と caveat C1–C3 が成立するならば}\quad \mathcal P_{9,3}=\textbf{TRUE},\quad \mathrm{ord}(a_9)=9,\quad\text{出力は }\texttt{FULL\_p\_DEPTH}.\ } $$

**(d) 構造的な含意 — (6.3) は「第二経路」ではなく「述語そのもの」である。**
私は `u9_extraction_plan_v1.md` §5-A で (6.3) を「第二の $u$ 抽出経路の候補」と書いた。**それは弱すぎた。** (a) が示すとおり **$\mathcal P_{9,3}$ が見ているのは $a_9$ の $\bmod\ 6$ 成分ちょうど**であり、(6.3) が決めるのも**同じ成分**である。したがって
$$ \text{(6.3) は }a_9\ \text{を完全には決めない}(\bmod\ 18\ \text{の残りは未定})\ \textbf{が、}\ \mathcal P_{9,3}\ \text{は完全に決める。} $$
**⇒ $u_9$ の抽出(二経路・Freeze 2)は $\mathcal P_{9,3}$ の**ためには**不要になりうる。** 逆に、$u_9$ を測れば (6.3) の**独立検証**になる(予測と実測の突合)。**役割が入れ替わる。**

### caveat(予測が落ちる条件・優先順)

| # | caveat | 状態 |
|---|---|---|
| **C1** | **$K^{(3)}$ の実測窓が $H_3^{\rm fun}=H_{2,1,0}$ か。** $n=3$ では good な $H$ が $2n(n-1)=12$ 個あり、$\alpha\in\{1,2\}$ の二通り。$u_3=-4$ がどの類の値かは**確認していない** | **UNKNOWN・最優先** |
| **C2** | (W1) が $n=9$ で成立(G3 が要求) | **未供給**(u9 計画 C4) |
| **C3** | $n=9$ 窓の (W5)・(W2)・BFC (5′) instance | **OPEN**(u9 計画 C3/C4/C9) |
| C4 | $\mathrm{ord}(a_9)\mid9$ の formal upper bound($e=n=9$・$\rho_0$ 忠実) | I-1 側・**要確認** |
| C5 | $u_3=-4$ の class $[-4]_6$ が $F_3$ でなく $F_9$ で評価されること(§5(c) は $F_9$ で計算済) | **閉** |

> **⚠ 誇張しない**: 本予測は **(6.3-cls) の証明(G3)と C1–C4 が閉じて初めて主張になる**。現時点では **`candidate / 条件つき予測`** であり、**$\mathrm{ord}(a_9)=9$ を既成事実として扱ってはならない**(証明なしの採用禁止)。

---

## 6. まとめ(5 行)

1. **形は確定した**: $u_n=u_d\,w^{2d}$($w\in F_n^\times$)。class 語で $\mathrm{res}_{F_n/F_d}(a_d)=\mathrm{pr}_{2n\to2d}(a_n)$、character 語で $\mathrm{res}(\kappa_d)=\kappa_n^{n/d}$。**両者は同値**(射影 $\leftrightarrow$ $n/d$ 乗)。
2. **Sol (6.3) は数学的核が正しく、語の型が混ざっていた**(class 語の等式に character 語の指数)。**直すのは型だけ。**
3. **向きは res(norm ではない)**、**法は $2d$**、**単数自由度は $w$ ちょうど一つで uniformizer 非依存**。
4. **証明は G3(Galois 同変性 ⇒ $F_n$ 上への descend)を書けば閉じる** — 他の 6 補題は既証明。
5. **最大の発見**: $\mathcal P_{9,3}$ が見る成分と (6.3) が決める成分は**同一**。ゆえに **(6.3) を認めれば $u_3=-4$ だけから $\mathcal P_{9,3}=$ TRUE($\mathrm{ord}(a_9)=9$)が従う**。**最優先の潰しどころは C1($K^{(3)}$ の窓が $H^{\rm fun}$ か)。**
