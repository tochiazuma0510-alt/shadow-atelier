# 凍結 1(Rule 1)候補文書 — $K^{(5)}$ 橋の規約・正規形・抽出手順 v1

2026-07-27 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱**。上位文書: `docs/manifest_k5_v1.md` v1.2 §「BRIDGE-IN 構築の独立性」1.・`sol/sol_reply_31_manifest.md` F4.1/F5/F9.3・`sol/裁定_29_ben31.md` 7。姉妹文書: `docs/week4-K5_S5設計_opus_v1.md`。

---

## 0. この文書の身分と不変条項

### 0.1 身分

本文書は **凍結 1 の候補**である。**受理されるまでは効力を持たず、受理された瞬間に不変となる。**

> **凍結 1 の時点(manifest v1.2・W2)**: 両 dessin のいかなる**個別モデル候補・係数・数値近似にも接する前**、**探索コマンドを一度も実行する前**に完了する。
>
> **起草時点の申告**: 本文書の起草者(Opus)は、起草の全過程で個別モデル候補・係数・数値近似・database に**一切接していない**。用いた計算は §0.4 に列挙した 1 本のみで、その入力は凍結済み有限 fixture だけである。

### 0.2 不変条項(受理後は一切変更しない)

1. **$a = j_{\rm ns}^{-1}j_{\rm sq} = 1$ は formal invariant であり永久不変**(便 31 F5・裁定 29-2)。橋側の捻れは $b_{\rm sq},b_{\rm ns}$ に、比較指数は $a_{\rm eff}$ に記録する。**$a$ を更新しない。**
2. **$\lambda/t^{10}$ の定数項を 1 に正規化することは禁止**(それが $u$ そのもの)。
3. **規則が一意候補を返さないときは UNKNOWN で止まる**(§9)。規則を後から変えて一意化しない。
4. **漏洩した run は後から同じ規則を hash して救済しない。** 汚染 artifact を隔離し、規則を変えるなら新 version の campaign とする。

### 0.3 本文書が依存していないもの(頑健性の設計)

`docs/week4-K5_S5設計_opus_v1.md` の命題 S5-1/S5-2/S5-3(ブロック構造・$\lambda = c\mu^2$・正規形)は**単系統・未監査**である。**したがって本文書の第一次規則(§2 の (M-A))は、これらに一切依存しない形で書いてある。** S5 設計の結果は §2 の (M-B)(整合検査)と §6 の副経路にのみ現れ、そこが崩れても Rule 1 は生きる。

**例外(依存を明示)**: §9 の停止条件 I-b(**$\lambda=c\mu^2$ の $c$ の平方類の漏洩禁止**)は命題 S5-4 に依存する。ただしこれは**禁止を増やす向き**の依存であり、命題 S5-4 が誤りでも安全側に倒れる。

### 0.4 起草時に用いた計算

`scratchpad/k5_blocks.js`(node・単系統)— 入力は凍結済み有限 fixture($G_5$ の $(v,q)$ 座標と標的 $H$)のみ。曲線・$\lambda$・$u$・数値近似・database に接触なし。

---

## Q1 → §1. 座標・向き・埋め込みの凍結

### 1.1 底と基点

$$ U := \mathbf P^1_{\mathbb Q}\smallsetminus\{0,1,\infty\},\qquad \text{基点} = \text{接基点}\ \vec{01}. $$

$\mathbf C$ の**標準的向き**(反時計回りが正)を採る。$\gamma_0,\gamma_1,\gamma_\infty\in\pi_1^{\rm top}(U,\vec{01})$ を、それぞれ $0,1,\infty$ を**反時計回り**に一周する単純ループで

$$ \gamma_0\gamma_1\gamma_\infty = 1 \tag{1.1} $$

となるものとする(この順序・この向きが正本)。$\hat F_2 = \pi_1^{\rm geom}(U,\vec{01})$ の位相生成元を $x:=\gamma_0,\ y:=\gamma_1,\ z:=\gamma_\infty$、$xyz=1$。

### 1.2 ordered branch $\leftrightarrow$ $X,Y,Z$

$\pi:\hat F_2\twoheadrightarrow P = G_5$ を D1 (3.6) の marking とする:

$$ \boxed{\ 0\ \leftrightarrow\ X = \pi(x),\qquad 1\ \leftrightarrow\ Y = \pi(y),\qquad \infty\ \leftrightarrow\ Z = \pi(z),\qquad XYZ=1.\ } \tag{1.2} $$

$X = (r,s,s),\ Y = (rs,r,rs),\ Z = (r^2s,r^{-1}s,r)$(D1 §2.1・変更禁止)。

### 1.3 $\Lambda$ 上の作用と合成の向き

$$ \Lambda_i := \{\,gH_ig^{-1}\ :\ g\in G_5\,\},\qquad \tau_i(g)(H') := g\,H'\,g^{-1}\quad(\textbf{左作用}). \tag{1.3} $$

$\tau_i:G_5\to\operatorname{Sym}(\Lambda_i)$ は**準同型**。置換の合成は $(\sigma\rho)(p) := \sigma(\rho(p))$ とする。そこで

$$ \sigma_0 := \tau_i(X),\quad \sigma_1 := \tau_i(Y),\quad \sigma_\infty := \tau_i(Z),\qquad \sigma_0\sigma_1\sigma_\infty = \mathrm{id} \tag{1.4} $$

($XYZ=1$ と $\tau_i$ の準同型性から自動)。

> **第二系統の規約差の扱い**: GAP は $H^g = g^{-1}Hg$(右共役)を使う。**規約を暗黙に吸収してはならない。** 第二系統は「$\tau^{\rm GAP} = \tau\circ(\ )^{-1}$ を使った」ことを**出力に明記**し、突合器はその反転を明示的に適用する。(D1 検算 I4 が「$a$ はこの反転で不変」を確認済だが、それは $a$ についてのみの結果であり、$b_i$ については§7 で改めて記録する。)

### 1.4 $K$ の複素埋め込み(**$b_i$ の一意性の生命線**)

$$ K := \mathbb Q(\zeta_{20}) = \mathbb Q[T]/(\Phi_{20}),\qquad \Phi_{20}(T) = T^8-T^6+T^4-T^2+1 . \tag{1.5} $$

($\Phi_{20}(T)=\Phi_{10}(T^2)$ — $10$ が偶数だから。)

$$ \boxed{\ \iota_\infty: K\hookrightarrow\mathbf C\ \text{を、}\ \zeta_{20}\ \text{が}\ \Phi_{20}\ \text{の根のうち}\ \operatorname{Im}>0\ \text{かつ}\ \operatorname{Re}\ \text{最大のもの}\ \text{に写るものとして固定する}. } \tag{1.6} $$

$\Phi_{20}$ の根は $e^{2\pi ik/20}$($k\in\{1,3,7,9,11,13,17,19\}$)。上半平面にあるのは $k=1,3,7,9$ で、$\operatorname{Re}$ 最大は $k=1$。ゆえに (1.6) は**一意**に $\zeta_{20}=e^{2\pi i/20}$ を指す。

$$ \zeta_{10} := \zeta_{20}^2,\qquad \zeta_5 := \zeta_{20}^4 . \tag{1.7} $$

### 1.5 $\tau_i$ の $\mu_{10}$ 版・Kummer 規約・$j_i$

$$ \iota:\ \mu_{10}\xrightarrow{\ \sim\ }\langle X\rangle,\ \ \zeta_{10}\mapsto X\quad(\textbf{両 dessin 共通}),\qquad \tau_i:\mu_{10}\hookrightarrow\operatorname{Sym}(\Lambda_i),\ \ \tau_i(\zeta_{10}) = \tau_i(X). \tag{1.8} $$

$$ \kappa_w(\gamma) := \frac{\gamma(w^{1/10})}{w^{1/10}}\in\mu_{10}\qquad(\gamma\in G_K,\ w\in K^\times). \tag{1.9} $$

$\mu_{10}\subset K$ ゆえ $\kappa_w$ は**準同型**であり、しかも **$10$ 乗根の取り方に依らない**(二つの根は $\mu_{10}\subset K$ の元だけ違い、$G_K$ 不変)。

$$ j_i:\ \mu_{10}[5]\xrightarrow{\ \sim\ }\mathfrak F_0,\qquad j_i\bigl(\zeta_{10}^{2t}\bigr) = \Phi_{0,-t}\qquad(\text{D1 v1.2 }(6.3)\text{・}i\ \text{に依らない}). \tag{1.10} $$

$$ \boxed{\ a := j_{\rm ns}^{-1}j_{\rm sq} = 1\ \in(\mathbb Z/5)^\times\quad(\textbf{永久不変}).\ } \tag{1.11} $$

### 1.6 $(\mathbb Z/20)^\times\to(\mathbb Z/10)^\times$ の $2:1$ lift(別封印項目)

$\ker\bigl((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times\bigr) = \{1,11\}$(位数 2)。すなわち $\tilde\chi$ の値 8 通りは $\mu_{10}$ 上では 4 通りに潰れる。**この $2:1$ は $b_i$($\varphi(10)=4$ 通り)とは別の項目**であり、混同しない(便 31 F5.1)。付録として凍結記録に別欄で記載する。

---

## Q2 → §2. モデルの同値関係と正規形アルゴリズム

### 2.1 同値関係

$(C,\lambda)$ と $(C',\lambda')$ が同値 $:\iff$ $\mathbb Q$ 上の同型 $\varphi:C\to C'$ で $\lambda'\circ\varphi = \lambda$ となるものが存在する。**$\operatorname{Aut}(C/\mathbf P^1_\lambda)=1$ ゆえ $\varphi$ は存在すれば一意。**

$\lambda$ 側に Möbius の自由度は**ない**: dessin は ordered($0,1,\infty$ が区別されている)なので、$\lambda\mapsto1-\lambda,\ 1/\lambda,\dots$ の 6 元 Möbius 群は**使えない**。$\lambda$ は「$0$-分岐で $0$、$1$-分岐で $1$、$\infty$-分岐で $\infty$」という条件で完全に決まる。

### 2.2 (M-A) 第一次正規形パイプライン(S5 設計に依存しない)

**M0(intrinsic な枝の決定)**: $P_\infty$ が Weierstrass 点か否かを、**モデルに依らない判定**
$$ P_\infty\ \text{は Weierstrass 点}\ \iff\ \ell(2P_\infty) = 2 $$
で決める。同様に $P_0$ についても決める。以後の枝を
$$ \text{(W)} := \{P_\infty\ \text{Weierstrass}\},\qquad \text{(N)} := \{P_\infty\ \text{非 Weierstrass}\} $$
と書く。**両枝を先に書く**(以下)。

**M1(超楕円モデル)**

- **枝 (W)**: $\deg f = 5$ のモデル $y^2=f_5(x)$ を取り、$P_\infty = \infty$(唯一の無限遠点)とする。$f_5$ は $\mathbb Q$ 上**モニック**にできる($x\mapsto tx,\ y\mapsto sy$ で主係数 $\mapsto s^{-2}t^5\cdot(\text{主係数})$;$t=\mathrm{lc},\ s=\mathrm{lc}^3$ と取れば $\mathrm{lc}\mapsto1$)。次に $x$-平行移動で $\boxed{x(P_0)=0}$。
- **枝 (N)**: $\deg f = 6$ のモデル $y^2=f_6(x)$ を取り、$x(P_\infty)=\infty$ とする。$P_\infty\in C(\mathbb Q)$ ゆえ $\mathrm{lc}(f_6)\in\mathbb Q^{\times2}$、$y$-スケールで $f_6$ を**モニック**にできる。$P_\infty = \infty_+$($y\sim+x^3$ の枝)と**定義する**(これが $y\mapsto-y$ を固定する — §4)。次に $x$-平行移動で $\boxed{x(P_0)=0}$。

**M2(残余群)**: M1 のあと残る座標変換は

- 枝 (W): $x\mapsto\tau^2x,\ y\mapsto\tau^5y$($\tau\in\mathbb Q^\times$)。係数 $a_j\mapsto a_j/\tau^{2(5-j)}$。
- 枝 (N): $x\mapsto tx,\ y\mapsto t^3y$($t\in\mathbb Q^\times$)。係数 $b_j\mapsto b_j/t^{6-j}$。

**M3(整数性)**: すべての係数を $\mathbb Z$ に入れる。

**M4(極小性)**: M2 の作用の中で M3 を保つものの中で、**重み付き content が極小**なものを取る。すなわち、係数ベクトルの重み付き付値 $\min_p\lfloor\cdot\rfloor$ をこれ以上下げられない状態にする。

**M5(全順序で一意化)**: §3。

**M6(一意性の検査)**: M5 が一意な候補を返さなければ **UNKNOWN 停止**(§9 U-a/U-b)。

### 2.3 (M-B) 整合検査(規則ではない)

S5 設計の命題 S5-3 が正しければ、枝 (W) のモデルは
$$ y^2 = a(x)^2+c_5x^5\qquad(\deg a\le2) $$
の形に一致するはずである。**一致しない場合でも Rule 1 は M-A に従う**(M-B は自己整合の警報にすぎない)。不一致は §11 論点として記録し、S5 設計の命題を疑う。

---

## Q3 → §3. 全順序と tie-break

### 3.1 有限性の証明義務(先に書く)

$$ \boxed{\text{M4 のあと残る候補集合が\textbf{有限}であることを、最小化の前に証明する。}} $$

有限でない(または有限性を証明できない)なら最小元は存在しないかもしれないので、**即 UNKNOWN 停止**(U-b)。

- 枝 (W): $\tau\mapsto-\tau$ は $a_j\mapsto a_j/(-1)^{2(5-j)} = a_j$ で係数に作用しない(作用は $y\mapsto-y$ のみ — §4 へ回る)。整数性 + 極小性のあと $\tau\in\{\pm1\}$ ゆえ**候補は 1 個**。
- 枝 (N): $t\mapsto-t$ は $b_j\mapsto(-1)^{j}b_j$ で**係数を実際に動かす**。整数性 + 極小性のあと $t\in\{\pm1\}$ ゆえ**候補は 2 個** ⇒ tie-break が要る(§3.2)。

### 3.2 全順序

$\mathbb Z$ に全順序
$$ 0\ \prec\ -1\ \prec\ 1\ \prec\ -2\ \prec\ 2\ \prec\ -3\ \prec\ \cdots\qquad(\text{絶対値優先・同値なら負が先}) $$
を入れる。モデルの鍵を

$$ \kappa(\text{model}) := \Bigl(\ \lvert\operatorname{disc}\rvert,\ \ (\text{係数ベクトルを高次から低次へ並べたもの})\ \Bigr) $$

とし、第一成分は通常の $\mathbb Z_{\ge0}$ の順、第二成分は $\prec$ の**辞書式**で比較する。**最小のものを取る。**

- 枝 (N) の 2 候補は $\operatorname{disc}$ が等しいので第二成分で決まる。$b_j\mapsto(-1)^jb_j$ ゆえ、$(b_5,b_3,b_1)$ のうち**最初の非零成分が正**になる方を取る。すべて零なら $f_6$ は偶関数で $t\mapsto-t$ が真の自己同型 ⇒ **候補は 1 個**(曖昧さ消滅)。

### 3.3 「最小係数」型のアルゴリズムを名指しで禁止する

> **禁止**: 「reduction algorithm が返した最小モデル」「CAS の `reduce`/`minimize` の出力」を**アルゴリズム名と版を書かずに**採用すること。それは数学的不変量ではない。
> **許可**: §3.2 のように**純粋に算術的な全順序**を書き下し、任意の実装が再現できる形にすること。外部アルゴリズムを使う場合は、その出力を §3.2 の順序で**再検証**する(出力が最小でなければ、順序に従って修正する)。

---

## Q4 → §4. $y\mapsto-y$・Möbius・sheet numbering の tie-break

### 4.1 $y\mapsto-y$

$y\mapsto-y$ は超楕円対合 $\iota$ の座標表示である。**印付きデータ $(C,P_0,P_\infty,\lambda)$ に対しては、多くの場合そもそも自由度でない。**

| 状況 | $y\mapsto-y$ の効果 | 規則 |
|---|---|---|
| 枝 (N)($P_\infty$ 非 Weierstrass) | $\infty_+\leftrightarrow\infty_-$ を入れ替える | **$P_\infty = \infty_+$ の定義(M1)で固定済**。自由度なし |
| 枝 (W) かつ $y(P_0)\ne0$ | $P_0 = (0,y_0)\mapsto(0,-y_0)$ — **別の点** | **$y(P_0)$ が正になる符号**を取る($y_0\in\mathbb Q^\times$ なので判定可能)。自由度なし |
| 枝 (W) かつ $y(P_0)=0$($P_0$ も Weierstrass) | $P_0,P_\infty$ をともに固定し、$\lambda\mapsto\lambda\circ\iota\ne\lambda$ | **真の 2 択**。下記 |

**$P_0$ も Weierstrass の場合の規則**: $\iota$ は印付き被覆の同型 $(C,\lambda\circ\iota)\xrightarrow{\sim}(C,\lambda)$ を与えるので、**§5 の uniformizer 規則が $\iota$-同変である限り $u$ は同じ**($t=y\mapsto-y$ で $u\mapsto u\cdot(-1)^{10}=u$)。ゆえに数学的曖昧さはない。再現性のためだけに tie-break を置く:
$$ \lambda = A(x)+B(x)y\ \text{と書いたとき、}\ B\ \text{の係数ベクトルが §3.2 の順序で小さい方の}\ \lambda\ \text{を取る}. $$

> **S5 設計 §3.3 の帰結(参考・依存しない)**: 枝 (W) では $P_0$ は自動的に非 Weierstrass になる(命題 S5-3 の正規形から $a(x_0)=0\Rightarrow\operatorname{ord}_{P_0}(\mu)=1\ne5$)。したがってこの行は**枝 (N) でのみ発火する見込み**である。ただし Rule 1 は S5 設計に依存しないので、両方書いておく。

### 4.2 Möbius

- **底 $\mathbf P^1_\lambda$**: 自由度**なし**(§2.1)。
- **源の $x$-直線**: M1(平行移動で $x(P_0)=0$、$x(P_\infty)=\infty$)と M2–M5 で**使い切っている**。追加の Möbius は使わない。

### 4.3 sheet numbering

> **補題 R1-U.** $\operatorname{Aut}(W_0/U)=1$ ゆえ
> $$ C_{S_{10}}\bigl(\operatorname{Mon}\bigr)\ \cong\ N_{\operatorname{Mon}}(\text{点安定化群})/(\text{点安定化群})\ =\ N_{G_5}(H)/H\ =\ 1 . $$
> したがって、幾何 fiber $\operatorname{Fib}_{\vec{01}}(W_0)$ と $\Lambda_i$ の間の、monodromy を intertwine する全単射 $c_i$ は **ちょうど一つ**。

$$ \Longrightarrow\qquad \boxed{\text{sheet numbering に tie-break は不要。}\ c_i\ \text{は一意である。}} \tag{4.1} $$

**もし実装が 2 個以上の intertwiner を返したら**、それは補題 R1-U に反するので**入力が壊れている** ⇒ **integrity stop**(§9 I-f)。UNKNOWN ではない。

---

## Q5 → §5. $u$ を使わない uniformizer 決定アルゴリズム

### 5.0 底側の局所助変数は選択の対象ではない

$\lambda=0$ における底の局所助変数は **$\lambda$ 自身**である($0,1,\infty$ が印付きなので $\lambda$ に自由度がない — §2.1)。**選ぶのは源の $P_0$ における $t$ だけ。**

### 5.1 Rule U-1(実務規則・超楕円座標)

$$ \boxed{\ t := \begin{cases} x - x(P_0)\ (= x,\ \text{M1 で}\ x(P_0)=0) & f(x(P_0))\ne0\quad(P_0\ \text{非 Weierstrass}) \\[2pt] y & f(x(P_0))=0\quad(P_0\ \text{Weierstrass}) \end{cases}\ } \tag{5.1} $$

**根拠**: $P_0$ 非 Weierstrass なら $\operatorname{ord}_{P_0}(x-x_0)=1$;Weierstrass なら $\operatorname{ord}_{P_0}(x-x_0)=2$ かつ $\operatorname{ord}_{P_0}(y)=1$。$P_0\ne P_\infty$ ゆえ $x(P_0)$ は有限で、無限遠の場合分けは不要。

**$t$ は $\mathbb Q$-有理**である(どちらの場合も)。

### 5.2 Rule U-2(モデル非依存の仕様・Riemann–Roch)

U-1 は超楕円座標に依存する。モデル非依存の仕様を併記し、**両者が一致することを検査する**(U-3)。

1. $n_0 := \min\{\,n\ge1\ :\ \ell(nP_\infty-P_0) > \ell(nP_\infty-2P_0)\,\}$ を計算する(有限:$n\ge5$ で必ず成立)。
2. $L(n_0P_\infty)$ の**順序付き生成系**を固定する: $P_\infty$ での極位数の**昇順**、同位数内はモデルの単項式順序(固定)。
3. その生成系に関する **reduced row echelon form**(一意)で基底を取る。
4. $\operatorname{ord}_{P_0}(g)=1$ を満たす基底元のうち **添字最小のもの**を $t_0$ とする。
5. $\boxed{t := t_0}$ — **再スケールしない。**

> **禁止(明示)**: $\lambda/t^{10}$ の定数項が $1$ になるように $t$ をスケールすること、および $\lambda$ の局所展開から計算した任意の量で $t$ をスケールすること。**それが $u$ である。**

### 5.3 Rule U-3(整合検査)

U-1 の $t$ と U-2 の $t_0$ は $t_0 = \varepsilon\,t\,(1+O(t))$、$\varepsilon\in\mathbb Q^\times$ を満たすはずである。$\varepsilon$ を記録する。**$\varepsilon\notin\mathbb Q^\times$、または一方が uniformizer でない ⇒ integrity stop**(§9 I-e)。

**正本は U-1** とする(実装が単純で監査しやすい)。U-2 は仕様と検査。

### 5.4 ★ なぜ規則を緩めないか(緩めてよい理由があるのに)

> **観測 R1-C.** $t,t'$ がともに $K$-有理な $P_0$ の uniformizer なら $t' = ct(1+O(t))$、$c\in K^\times$、したがって $u\mapsto uc^{-10}$。ゆえに
> $$ \boxed{\ [u]_{10}\in K^\times/K^{\times10}\ \text{は}\ K\text{-有理 uniformizer の取り方に依らない}.\ } $$

すなわち**封印予測 (P1)(P2) は uniformizer の選択に影響されない**(manifest の covariance control 2 と同じ内容)。

**それでも §5 の規則を緩めない理由は二つ**:
1. **生の $u$** は二経路突合(§6)の対象であり、経路間で同じ $t$ を使わなければ比較にならない。
2. 「$K$-有理」という条件自体が規則を要する。アルゴリズムが非有理な $t$ を返せば類も動く。

---

## §6. $u$ の二経路(数式・実装版・受理規則)

$$ \lambda\ =\ u\,t^{10}\,\bigl(1+O(t)\bigr)\quad\text{at }P_0,\qquad u\in K^\times\ (\text{実は}\ \mathbb Q^\times). $$

### 6.1 経路 A(cusp 展開)

1. モデルの定義方程式を $P_0$ で Hensel/Newton 持ち上げし、$K[[t]]$ の中で $x,y$ の展開を精度 $t^{13}$ まで**厳密に**求める。
2. $\lambda = A(x)+B(x)y$ に代入し、$\lambda = \sum_{k\ge10}u_kt^k$ を得る。
3. $\boxed{u^{(A)} := u_{10}}$。$u_{10},\dots,u_{13}$ を**生出力として別保存**する。
4. 検査: $u_k = 0$($k<10$)を厳密に確認。破れたら integrity stop。

**中間表現**: $K[[t]]$(切断冪級数)。

### 6.2 経路 B(Vieta / ノルム・**級数を使わない**)

$\lambda^\iota := \lambda\circ\iota = A(x)-B(x)y$、$N(\lambda) := \lambda\lambda^\iota = A^2-B^2f\in\mathbb Q[x]$ と置く。$\operatorname{div}(\lambda) = 10P_0-10P_\infty$ から $N(\lambda)$ の $x_0:=x(P_0)$ における零位数は $10$ であり、$\hat c := \bigl[N(\lambda)/(x-x_0)^{10}\bigr]_{x=x_0}\ne0$。

- **B-i($P_0$ 非 Weierstrass・$t=x-x_0$)**: $\iota P_0\ne P_0$ かつ $\lambda^{-1}(0)=\{P_0\}$ ゆえ $\lambda^\iota(P_0)\ne0$。したがって
  $$ \boxed{\ u^{(B)}\ =\ \frac{\hat c}{\lambda^\iota(P_0)}\ =\ \frac{\hat c}{A(x_0)-B(x_0)\,y_0}\ }\qquad(y_0:=y(P_0)). \tag{6.1} $$
- **B-ii($P_0$ Weierstrass・$t=y$)**: $\lambda+\lambda^\iota = 2A(x)$ で、$\lambda = ut^{10}+u_{11}t^{11}+\cdots$, $\lambda^\iota = \lambda(-t)$ ゆえ $\lambda+\lambda^\iota = 2ut^{10}+O(t^{12})$。他方 $y^2=f(x)$ と $f(x_0)=0$ から $x-x_0 = y^2/f'(x_0)+O(y^4)$。ゆえに $A(x) = \alpha(x-x_0)^5+O((x-x_0)^6)$ と書けば
  $$ \boxed{\ u^{(B)}\ =\ \frac{\alpha}{f'(x_0)^5},\qquad \alpha := \bigl[(x-x_0)^5\bigr]A(x)\ =\ \frac{A^{(5)}(x_0)}{120}.\ } \tag{6.2} $$

**中間表現**: $\mathbb Q[x]$(多項式・評価・Taylor 係数)。**冪級数を使わない。**

> **補助経路 B′(S5 設計に依存・任意)**: 命題 S5-2 が成立するなら $\lambda=c\mu^2$、$\mu = v t^5(1+\cdots)$ で $u = cv^2$、かつ $\mu\mu^\iota = c_5(x-x_0)^5$ から $v = c_5/\mu^\iota(P_0)$(級数不要)。**B′ は第三経路であって B の代用ではない。** 用いる場合は独立な札で記録する。

### 6.3 独立性の要件(manifest v1.2 §4 の実体化)

1. **非共有 helper**: 経路 A の級数モジュールと経路 B の多項式モジュールは、**共通の関数・共通のデータ構造を一切共有しない**。共有してよいのは数体 $K$ の元の表現(§8)だけで、それも**別実装を推奨**。
2. **別中間表現**: $K[[t]]$ vs $\mathbb Q[x]$(上記)。
3. **raw 出力の別保存**: `u_pathA.json` / `u_pathB.json`(それぞれ生の中間量も含む)。
4. **第三の checker**: 二つの生出力**だけ**を読み、$u^{(A)} = u^{(B)}$ を $K$ の中で厳密に判定する小さな独立プログラム。**それ以外の計算をしない。**

### 6.4 受理規則

| 結果 | 処置 |
|---|---|
| $u^{(A)} = u^{(B)}$($K$ 内の厳密等号) | **受理**。$u := u^{(A)}$ を凍結記録へ |
| 不一致 | **即 integrity stop / BRIDGE-UNKNOWN**。**平均・符号調整・座標再選択を禁止**。数学的結論を一切宣言しない |
| 一方が計算不能(予算超過・分岐未対応) | **二経路不成立** ⇒ BRIDGE-UNKNOWN(§9 U-e)。片方だけで $u$ を採用しない |

---

## §7. $b_i$ の決定式と受理条件

### 7.1 定義

- $\ell_i$ := **正の向きの実 local monodromy**。すなわち、$P_0$ における惰性群($\cong\mu_{10}$、全分岐)の生成元で、(1.6) の埋め込みの下で $\lambda$ の周りを**反時計回り**に一周する $\gamma_0$ に対応するもの。
- $c_i$ := §4.3 の**一意**な intertwiner $\operatorname{Fib}_{\vec{01}}(W_0^{(i)})\xrightarrow{\sim}\Lambda_i$。

$$ \boxed{\ c_i\,\ell_i\,c_i^{-1}\ =\ \tau_i\bigl(\zeta_{10}^{\,b_i}\bigr),\qquad b_i\in(\mathbb Z/10)^\times = \{1,3,7,9\}.\ } \tag{7.1} $$

$\tau_i$ は単射なので、右辺が $\tau_i(\langle\zeta_{10}\rangle)$ に属せば $b_i$ は**一意**。

$$ \text{属さない}\ \Longrightarrow\ \text{actual marking が閉じていない}\ \Longrightarrow\ \textbf{BRIDGE-UNKNOWN}\ (\S9\ \text{U-f}). $$

### 7.2 比較指数

$$ \boxed{\ a_{\rm eff}\ =\ [b_{\rm ns}]^{-1}\,a\,[b_{\rm sq}],\qquad a = 1\ \text{(永久不変)}\ } \tag{7.2} $$

($[b_i]$ は $\mu_{10}[5]$ への制限。$(\mathbb Z/10)^\times\to(\mathbb Z/5)^\times$ は全単射ゆえ lift の曖昧さはない。)

### 7.3 受理条件(**厳格運用**)

$$ \boxed{\ b_{\rm sq} = b_{\rm ns}\ }\quad\Longrightarrow\quad a_{\rm eff} = a = 1\quad\Longrightarrow\quad \text{(P2) は完全一致形}\ [u_{\rm ns}^{-1}]_{10} = [u_{\rm sq}^{-1}]_{10}. $$

$$ b_{\rm sq}\ne b_{\rm ns}\ \Longrightarrow\ \textbf{規約不整合として停止・}u\ \textbf{を開けない}\ (\S9\ \text{I-d}). $$

### 7.4 事前の見込みと、それを仮定しない規律

§1.2–§1.3 の規約の下では $\sigma_0 = \tau_i(X)$ が定義であり、$c_i$ が一意な intertwiner であることから **$b_i = 1$ が期待される**。しかし

> $b_i = 1$ を**仮定してはならない**。必ず (7.1) を**計算して記録**する。

$b_i\ne1$ が出る現実的な原因は (a) 実装内の向きの反転(§1.3 の GAP 規約差の吸収漏れ)、(b) 埋め込み (1.6) と異なる原始根の使用、(c) 惰性生成元の取り方の反転である。**いずれも「発見」ではなく規約の記録事項**であり、$a$ を更新して吸収してはならない(裁定 29-2)。

---

## §8. exact 数体・Kummer 判定器の仕様

### 8.1 数体

$$ K = \mathbb Q[T]/(T^8-T^6+T^4-T^2+1),\qquad \zeta_{20} := \bar T,\qquad \text{埋め込みは }(1.6). $$

すべての演算は**厳密**(有理数係数の多項式剰余環)。**浮動小数点を判定に用いない。**

### 8.2 $K^{\times10}$ 判定の骨(算術的単純化)

$\mu_{10}\subset K$ であり $10 = 2\cdot5$、$\gcd(2,5)=1$ なので

$$ \boxed{\ w\in K^{\times10}\ \iff\ w\in K^{\times2}\ \textbf{かつ}\ w\in K^{\times5}.\ } \tag{8.1} $$

($\Leftarrow$: $w=p^2=q^5$ なら $w = w^5(w^2)^{-2} = p^{10}q^{-20} = (p/q^2)^{10}$。)

したがって判定は **$T^2-w$ と $T^5-w$ の $K[T]$ における厳密な因数分解**に帰着する(根の存在判定)。**「根が見つからなかった」ではなく「因数分解の結果、一次因子がない」**という証明書を出す。

### 8.3 証明書型($v_i := u_i^{-1}$)

| 判定 | 陽性証明書 | 陰性(obstruction) |
|---|---|---|
| $\operatorname{ord}([v]_{10}) = 1$ | 明示 $c\in K^\times$ with $c^{10}=v$ | — |
| $\operatorname{ord}([v]_{10}) = 5$ | 明示 $c$ with $c^{10}=v^5$ **かつ** $v\notin K^{\times10}$ の exact obstruction | 下記メニューのいずれか |
| **(P2)** | $r := v_{\rm ns}/v_{\rm sq}^{\,a_{\rm eff}}$ について $c^{10}=r$ の明示 witness | $r\notin K^{\times10}$ の exact obstruction |

**obstruction メニュー(いずれか一つで足りる)**

- (O-a) 素イデアル $\mathfrak p$ で $v_{\mathfrak p}(v)\not\equiv0\pmod{10}$($(v)$ のイデアル分解を厳密に取る)。**最も安価で最も強い。**
- (O-b) $T^2-v$ が $K[T]$ で既約(2-part の障害)。
- (O-c) $T^5-v$ が $K[T]$ で既約(5-part の障害)。

**探索失敗しか無い場合は UNKNOWN**(§9 U-e)。浮動小数点の root search は証明書にならない。

### 8.4 (5′) の量化子

$$ \rho_i(\operatorname{Ih}(\gamma)) = \tau_i(\kappa_i(\gamma))\qquad(\forall\gamma\in G_K). $$

**有限個の Frobenius サンプル一致は較正であって PASS の証明ではない。** PASS は character 恒等の普遍的導出、または同値な Kummer 拡大の厳密同定を要する。**FAIL は exact な $\gamma$ 一つで足りる。**

### 8.5 (P1) の補助証明書(**S5 設計 命題 S5-4 に依存・凍結 2 後にのみ使用可**)

$\lambda = c\mu^2$($c\in\mathbb Q^\times$)なら
$$ \text{(P1)}\ \iff\ c\in K^{\times2}\ \iff\ \operatorname{sqfree}(c)\in\{1,-1,5,-5\} $$
($K=\mathbb Q(\zeta_{20})$ の二次部分体は $\mathbb Q(i),\mathbb Q(\sqrt5),\mathbb Q(\sqrt{-5})$)。

> **★ この事実は同時に漏洩経路である。** §9 I-b を参照。**$\operatorname{sqfree}(c)$ の計算は凍結 2 より前は禁止**であり、凍結 2 のあとに (P1) の**独立な第二証明書**としてのみ用いてよい。

### 8.6 版の固定

凍結記録に: 数体演算ライブラリ名 + 版 + commit、因数分解アルゴリズム名、イデアル分解アルゴリズム名、経路 A/B の実装 commit、第三 checker の commit。

---

## Q6 → §9. 停止条件

### 9.1 UNKNOWN 停止(札であって失敗ではない)

| # | 条件 |
|---|---|
| **U-a** | §2 のパイプラインが 2 個以上の候補を返し、§3.2 の全順序でも同点 |
| **U-b** | §3.1 の**有限性が証明できない**(残余群の軌道が無限かもしれない) |
| **U-c** | M0 の Weierstrass 枝判定が、事前登録した計算予算内に閉じない |
| **U-d** | 明示モデルそのものが得られない(撤退条件 2026-08-10 / 8 委嘱とは別枠の即時札) |
| **U-e** | exact Kummer 証明書が得られない(探索失敗のみ)/ $u$ の一方の経路が計算不能 |
| **U-f** | $b_i$ が $\tau_i(\langle\zeta_{10}\rangle)$ に属さない(actual marking 未閉) |

**UNKNOWN で止まったら、規則を変えて一意化しない。** 規則を変えるなら**新 version の campaign** とする。

### 9.2 即時 integrity stop(救済不可)

| # | 条件 |
|---|---|
| **I-a** | 凍結 1 前に個別モデル候補・係数・数値近似に接触した |
| **I-b** | 凍結 2 前に $u$ **または同値な leading class** が漏れた。**同値物には $\lambda=c\mu^2$ の $c$ の平方類・平方因子・符号を含む**(命題 S5-4)。$\lambda$ を「$c$ と $\mu$ の対」に分離して報告することも禁止 |
| **I-c** | $u$ 二経路の不一致(§6.4) |
| **I-d** | $b_{\rm sq}\ne b_{\rm ns}$(§7.3) |
| **I-e** | モデル検査二系統の不一致 / U-3 の $\varepsilon\notin\mathbb Q^\times$ |
| **I-f** | intertwiner $c_i$ が一意でない(補題 R1-U に反する ⇒ 入力破損) |
| **I-g** | S5 設計の受理物 A8($\operatorname{ord}[P_0-P_\infty]=5$)が破れる |
| **I-h** | hash・serialization・発射錠の対象が一致しない / 両翼共同凍結前に片翼の $u$ を開けた |
| **I-i** | exact Kummer 証明書なしに PASS/FAIL を宣言した |

### 9.3 Model-Builder(A)の入出力 schema(凍結 1 の一部)

**許可される出力**: 明示モデル $C/\mathbb Q$、Belyi 写像 $\lambda$(**完全な式として**)、分岐 divisor、cusp $P_0,P_\infty$、uniformizer $t$ の式、target triple への exact conjugator、分岐指数 10 の証明、$t$ が uniformizer であることの証明、$\operatorname{Aut}(C/\mathbf P^1)=1$ の証明。

**禁止される計算**: $\lambda/t^{10}$ の非零定数項およびその同値物(leading coefficient・その valuation・その Kummer class)、**$c$ の平方類・平方因子・符号**、そしてそれらを**候補選択に使うこと**。

**A は「$u$ 未計算」および「$\operatorname{sqfree}(c)$ 未計算」を申告し、全 transcript を保存する。** 主根拠は本 schema と役割別 access log であり、**grep は補助検査**にすぎない(W4)。

---

## §10. 凍結記録に載せるもの

1. 本文書の **canonical serialization**(UTF-8・改行 LF・末尾改行あり・BOM なし)と **sha256**。
2. UTC/JST timestamp、commit ID、凍結対象の全ファイル一覧。
3. §8.6 の実装版一覧。
4. §1.6 の $(\mathbb Z/20)^\times\to(\mathbb Z/10)^\times$ の $2:1$ lift の記載(別欄)。
5. 発射錠 `FIRE_k5bridge.auth` が束縛する digest 組(**一回性・別 artifact へ再利用不可**)。
6. **記録欄(値は凍結 2 まで空)**: $b_{\rm sq}$, $b_{\rm ns}$, $a_{\rm eff}$, $\varepsilon$(U-3)、枝 (W)/(N) の別、$P_0$ の Weierstrass 性。**$a=1$ の欄は不変値として先に埋める。**

---

## §11. 論点(便 32 / 司令塔裁定へ)

1. **§9 I-b(命題 S5-4 由来の漏洩禁止)を採るか。** 採ると Model-Builder は $\lambda$ を分解形で報告できなくなる。代案: 「分解形の報告は許すが $\operatorname{sqfree}(c)$ の計算は禁止し、access log で担保する」。**私は I-b の厳格版を推す**(便 31 F4.3 の「同値な leading coefficient」は、まさにこれを指していたと読む)。
2. **§2 (M-A) と (M-B) の分離**は過剰か。S5 設計の命題 S5-2/S5-3 が Sol 監査を通れば (M-B) を第一次規則へ格上げでき、正規形はずっと単純になる(枝 (W) は母数 2)。**しかし凍結 1 は単系統結果に依存させたくない**ため v1 では分離した。監査結果を待って v2 で統合するか。
3. **§5.4 の観測 R1-C**(類は uniformizer に依らない)は既知の covariance control の再述だが、**規則の緩和には使わない**と書いた。この判断でよいか。
4. **§6.2 B-ii の式 (6.2)** は Taylor 係数の抽出を使う。これを「級数」と見なして経路 A との独立性を疑うべきか、それとも多項式演算として独立と認めてよいか。**私は独立と考える**(曲線上の冪級数持ち上げを一切行わないため)が、独立性の判定は監査側の権限である。
5. **U-c の計算予算**の具体値(秒数・ステップ数)を凍結 1 に書き込むべきか、それとも委嘱ごとに定めるか。書き込むなら値の提案を求めたい。
6. **【文献要請】** §8.2 の $K^{\times10}$ 判定について、$K=\mathbb Q(\zeta_{20})$ のような**円分体での $n$ 乗剰余判定の標準的な exact アルゴリズムと、その証明書型**(とくに (O-a) の「$v_{\mathfrak p}(v)\not\equiv0$」型 obstruction の標準的な提示法)の定番文献があれば、実装仕様の裏取りになる。欲しい結果の型: **アルゴリズムの正当性証明つきの記述**であって、ライブラリのマニュアルではない。
