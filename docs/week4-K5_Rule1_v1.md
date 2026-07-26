# 凍結 1(Rule 1)候補文書 — $K^{(5)}$ 橋の規約・正規形・抽出手順 v1.1

2026-07-27 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱**。上位文書: `docs/manifest_k5_v1.md` v1.2 §「BRIDGE-IN 構築の独立性」1.・`sol/sol_reply_31_manifest.md` F4.1/F5/F9.3・`sol/裁定_29_ben31.md` 7。姉妹文書: `docs/week4-K5_S5設計_opus_v1.md`。

**v1.1(2026-07-27・便 32 P2/P6 + 裁定 31 の修理)。**

## v1 → v1.1 差分表

| # | 箇所 | v1 | v1.1 | 出典 |
|---|---|---|---|---|
| D1 | §2.2 **M3** | 「すべての係数を $\mathbb Z$ に入れる」(方法未定義) | 明示の既定手続き(分母 lcm)+ **どの clearing でもよい**ことを明記 | 便 32 F2.2 / P2 |
| D2 | §2.2 **M4** | 「重み付き content が極小」(被 floor 数なし・アルゴリズムでない) | **total algorithm** $\mathrm{wp}$: 重み $w_j$・素数ごとの $k_p=\min_{A_j\ne0}\lfloor v_p(A_j)/w_j\rfloor$・$\tau_+=\prod p^{k_p}$・$A_j\mapsto A_j/\tau_+^{w_j}$。零係数は min から除外、符号単元は M5 へ | 便 32 F2.2 (2.1)(2.2) |
| D3 | **§2.4(新設)** | — | **補題 R1-N1(denominator clearing 非依存性)**・**補題 R1-N2(残余 $=\{\pm1\}$・有限性)**+系(§3.1 の根拠)+計算可能性の注 | 便 32 F2.2「短く証明する」 |
| D4 | §2.3 (M-B) | $y^2=a(x)^2+c_5x^5$ | 符号修理($c_N$ 規約)。**M-B は第一次規則へ昇格しない**・discovery に使うなら sealed automation の別 schema | 便 32 F2.3 / F4.4 |
| D5 | §3.1 | 「有限性の証明義務」(未履行) | 補題 R1-N2 で**両枝とも証明済み**。U-b は fail-closed の札として存続 | 便 32 F2.2 |
| D6 | §4.1 の参考行 | $a(x_0)=0\Rightarrow\operatorname{ord}_{P_0}(\mu)=1$ | **直接証明**($a(x_0)=0\Rightarrow(x-x_0)^2\mid f_5\Rightarrow$ 特異)へ差替え | 便 32 F4.4 末尾 |
| D7 | §5.2 U-2 | 「モデルの単項式順序(固定)」(未定義) | **単項式順序 $(\mathrm{pol},b,a)$ 昇順辞書式**・**ambient $\mathcal A(n)$ の明示**・RREF の対象空間を $L(n_0P_\infty-P_0)$ と明記・存在の証明 | 便 32 F2.1 |
| D8 | §9.1 U-c | 条件のみ(予算値は §11) | **作用行に 600 秒を移記**(同 campaign 内で上限を増やして再分類しない) | 便 32 F2.5 / P6 |
| D9 | §11 論点 1–6 | 未決 | **1–6 すべて決着**(I-b 厳格版採用・M-B 非昇格・R1-C 非緩和・B-ii 独立・U-c 600 秒・文献ゲート 02 PASS) | 便 32 F2.1/F2.3/F2.4/F2.5・裁定 31 |

> **digest 注意(P7)**: 本改訂で canonical serialization が変わる。§10-1 の sha256 は**再取得を要する**(司令塔)。
>
> **起草時点の申告(再掲・v1.1 でも不変)**: 本改訂の全過程で個別モデル候補・係数・数値近似・database に**一切接していない**。v1.1 で新たに行った機械計算は、**§2.4 の補題を無作為な有理係数ベクトルで確認する検算スクリプト 1 本のみ**(`search/wp-check.mjs`(司令塔が恒久化・再走 11649/0 再現)・整数演算・曲線データを入力に持たない・11649 検査すべて一致)。探索コマンドは依然として一度も実行していない。

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

**したがって本文書の第一次規則(§2 の (M-A))は、`docs/week4-K5_S5設計_opus_v1.md` の命題群に一切依存しない形で書いてある。** S5 設計の結果は §2 の (M-B)(整合検査)と §6 の副経路にのみ現れ、そこが崩れても Rule 1 は生きる。

**v1.1 での S5 側の監査状態の更新**(便 32 F4):

| S5 側の主張 | 便 32 の判定 | Rule 1 での使われ方 |
|---|---|---|
| 補題 S5-B(唯一のブロック系)・命題 S5-1($\operatorname{ord}=5$)・命題 S5-2($\lambda=c\mu^2$) | **PASS**(紙上証明が通る。有限群部分は cross-checked artifact として受理・**Lean の `verified` ではない**) | §9 I-g(A8 の破れで stop)・§6.2 の補助経路 B′ |
| **命題 S5-3(曲線の二枝正規形)** | **差戻し**(符号・gauge の不整合)→ **S5 設計 v1.1 で修理**。なお**単系統・未監査**(機械照合は受けていない — ★教材 22) | §2.3 (M-B)・§4.1 の参考行のみ。**第一次規則は依存しない** |
| 命題 S5-4((P1) $\iff c\in K^{\times2}$) | **PASS** | §8.5・**§9 I-b**(下記) |

**例外(依存を明示)**: §9 の停止条件 I-b(**$\lambda=c\mu^2$ の $c$ の平方類の漏洩禁止**)は命題 S5-4 に依存する。ただしこれは**禁止を増やす向き**の依存であり、命題 S5-4 が誤りでも安全側に倒れる。S5-4 は便 32 F4.6 で PASS。

### 0.4 起草時に用いた計算

1. `scratchpad/k5_blocks.js`(node・単系統・v1)— 入力は凍結済み有限 fixture($G_5$ の $(v,q)$ 座標と標的 $H$)のみ。
2. `search/wp-check.mjs`(node・単系統・**v1.1 で追加**・司令塔恒久化)— §2.4 の補題 R1-N1/R1-N2 の検算。入力は**無作為な有理係数ベクトル**のみ(BigInt 整数演算・11649 検査すべて一致)。

**いずれも曲線・$\lambda$・$u$・数値近似・database に接触なし。**

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

**M2(残余群・重み)**: M1 のあと残る座標変換と、それが係数に与える**重み**を次で固定する。

| 枝 | 係数の並び | 残余変換 | 係数の変換則 | 重み $w_j$ |
|---|---|---|---|---|
| **(W)** | $f_5 = x^5+\sum_{j=0}^{4}A_jx^j$ | $x\mapsto\tau^2x,\ y\mapsto\tau^5y$($\tau\in\mathbb Q^\times$) | $A_j\mapsto A_j/\tau^{2(5-j)}$ | $w_j := 2(5-j)\in\{10,8,6,4,2\}$ |
| **(N)** | $f_6 = x^6+\sum_{j=0}^{5}B_jx^j$ | $x\mapsto tx,\ y\mapsto t^3y$($t\in\mathbb Q^\times$) | $B_j\mapsto B_j/t^{6-j}$ | $w_j := 6-j\in\{6,5,4,3,2,1\}$ |

以下、両枝を統一して**係数ベクトル** $A = (A_j)_{j\in J}$($J$ は**主係数を除く**添字集合)、群作用を

$$ (\sigma\cdot A)_j\ :=\ A_j/\sigma^{w_j}\qquad(\sigma\in\mathbb Q^\times) \tag{2.0} $$

と書く(枝 (W) では $\sigma=\tau$、枝 (N) では $\sigma=t$)。**主係数の重みは $w=0$** なので M2 は主係数を動かさない — これが M1 のモニック性が M2 で保たれる理由であり、同時に主係数を $J$ から**除かねばならない**理由である($w_j$ で割るため $w_j\ge1$ が要る)。枝 (W) では群の元は $\alpha=\tau^2\in\mathbb Q^{\times2}$ であり、$w_j$ が偶数なので $\sigma^{w_j}=(\sigma^2)^{(5-j)}$、すなわち (2.0) は常に**実在する群元**の作用である。

**M3(整数化・どの clearing でもよい)**: 任意の $\sigma_3\in\mathbb Q_{>0}$ で $A\mapsto\sigma_3\cdot A$ とし、全係数を $\mathbb Z$ に入れる。

> **既定手続き(実装が迷わないため)**: $A_j$ の分母の最小公倍数を $D$ とし $\sigma_3 := 1/D$ を取る。$w_j\ge1$ ゆえ $v_p(A_j)+w_jv_p(D)\ \ge\ v_p(A_j)+v_p(D)\ \ge\ 0$ で必ず整数化する。**これは過剰 clearing でよい** — M4 が同じだけ戻す(補題 R1-N1)。

**M4(weighted-primitive 正規化・total algorithm)**: 入力は M3 の出力(零ベクトルでない整数ベクトル)。ただし以下は**任意の有理係数ベクトルに対して定義される**(それが R1-N1 の内容)。

1. $S(A) := \{\,p\ \text{素数}\ :\ \exists j\in J,\ A_j\ne0,\ v_p(A_j)\ne0\,\}$ — $A_j$ の分子・分母の素因数分解から決まる**有限集合**。
2. 各素数 $p$ について
   $$ k_p(A)\ :=\ \min_{\substack{j\in J\\ A_j\ne 0}}\ \left\lfloor\frac{v_p(A_j)}{w_j}\right\rfloor\qquad(\textbf{零係数は min から除外}). \tag{2.1} $$
   $p\notin S(A)$ なら $k_p(A)=0$。
3. $\displaystyle \tau_+(A)\ :=\ \prod_{p\in S(A)}p^{\,k_p(A)}\ \in\ \mathbb Q_{>0}$。
4. **出力** $\ \mathrm{wp}(A)\ :=\ \tau_+(A)\cdot A$、すなわち
   $$ \boxed{\ A_j\ \longmapsto\ A_j\big/\tau_+(A)^{\,w_j}\ }\qquad(j\in J). \tag{2.2} $$
5. **符号単元 $\sigma=-1$ は M4 で扱わない** — M5(§3.2)へ回す。

$\mathrm{wp}(A)$ は**整数ベクトルであり、かつ weighted primitive**($\forall p:\ k_p(\mathrm{wp}(A))=0$)である(§2.4)。具体形は、枝 (W) が便 32 (2.1)、枝 (N) が便 32 (2.2) と一致する。

> **計算可能性と凍結記録**: $S(A)$ と $(k_p(A))_{p\in S(A)}$ は **値として**凍結記録に載せる(再現に因数分解の再実行を要求しない)。$v_p$ は整数演算のみ。**浮動小数点を使わない。**

**M5(全順序で一意化)**: §3。

**M6(一意性の検査)**: M5 が一意な候補を返さなければ **UNKNOWN 停止**(§9 U-a/U-b)。

### 2.3 (M-B) 整合検査(規則ではない・**第一次規則へ昇格しない**)

S5 設計の命題 S5-3(v1.1 で符号修理済み・$c_N$ 規約)が正しければ、枝 (W) のモデルは

$$ y^2\ =\ a(x)^2-c_N\,x^5\qquad(\deg a\le2),\qquad\text{gauge を統一すれば}\ c_N=-1\ \text{で}\quad y^2 = a(x)^2+x^5 $$

の形に一致するはずである($x_0=0$ は M1 で既に固定済。符号は `docs/week4-K5_S5設計_opus_v1.md` v1.1 §3.3 の $N=\mu\mu^\iota=a^2-b^2f=c_N(x-x_0)^5$ 規約に統一した — v1 の $+c_5$ は誤り。便 32 F4.4)。**一致しない場合でも Rule 1 は M-A に従う**(M-B は自己整合の警報にすぎない)。不一致は §11 に記録し、S5 設計の命題を疑う。

> **【裁定 31 / 便 32 F2.3】M-B を第一次規則へ昇格しない。** 理由は監査の順序ではなく **I-b 厳格版との両立不能**である: M-B を通常の Model-Builder 探索規則にすると、solver は $\lambda=c\mu^2$ の $c$ を明示変数として扱う。これは §9 I-b(**$c$ の平方類・平方因子・符号を凍結 2 前に計算・報告・選択に使うことの禁止**)と同時には運用できない。
>
> **M-B / $\mu$-正規形を discovery engine に使うなら**、全候補列挙・M-A canonicalization・両翼共同 freeze までを**人間から隔離した sealed automation** として、**別 schema に事前登録**すること(本 v1 の範囲外)。v1 では **M-A を正本**、**M-B を凍結 2 後の整合検査**に留める。

### 2.4 M3–M4 の正当化(便 32 F2.2 の要求)

記号は §2.2 の通り($J$・$w_j\ge1$・作用 (2.0)・$k_p$ (2.1)・$\mathrm{wp}$ (2.2))。$A\ne0$ とする。

> **補題 R1-N1(denominator clearing 非依存性).** 任意の $\sigma\in\mathbb Q_{>0}$ に対し
> $$ \boxed{\ \mathrm{wp}(\sigma\cdot A)\ =\ \mathrm{wp}(A).\ } $$

**証明.** $A_j\ne0$ なら $(\sigma\cdot A)_j\ne0$ でありその逆も真だから、(2.1) の min を取る添字集合 $\{j: A_j\ne0\}$ は $\sigma$ 作用で**不変**である。各 $j$ につき $v_p((\sigma\cdot A)_j) = v_p(A_j)-w_j\,v_p(\sigma)$、そして $v_p(\sigma)\in\mathbb Z$ なので floor の外へ出せる:

$$ \left\lfloor\frac{v_p((\sigma\cdot A)_j)}{w_j}\right\rfloor = \left\lfloor\frac{v_p(A_j)}{w_j}-v_p(\sigma)\right\rfloor = \left\lfloor\frac{v_p(A_j)}{w_j}\right\rfloor-v_p(\sigma). $$

min を取って $k_p(\sigma\cdot A) = k_p(A)-v_p(\sigma)$(全素数で)、すなわち正の有理数として $\tau_+(\sigma\cdot A) = \tau_+(A)/\sigma$。よって

$$ \mathrm{wp}(\sigma\cdot A)_j\ =\ \frac{A_j/\sigma^{w_j}}{\bigl(\tau_+(A)/\sigma\bigr)^{w_j}}\ =\ \frac{A_j}{\tau_+(A)^{w_j}}\ =\ \mathrm{wp}(A)_j. \qquad\blacksquare $$

**系 R1-N1a.** M3 でどれだけ余分に denominator を clear しても、M4 の出力は同一である。すなわち **$\mathrm{M4}\circ\mathrm{M3}$ は M3 の選択に依らず、元の有理係数ベクトル $A$ の関数 $\mathrm{wp}(A)$ である。** とくに $\mathrm{wp}$ は M2 の**正部分** $\mathbb Q_{>0}$ の軌道上の定数であり、$k_p(\mathrm{wp}(A))=k_p(A)-k_p(A)=0$ から $\mathrm{wp}\circ\mathrm{wp}=\mathrm{wp}$(冪等)。また $k_p(\mathrm{wp}(A))=0\ (\forall p)$ は $\mathrm{wp}(A)$ の**整数性**も含む(下記の同値による)。

> **補題 R1-N2(残余は符号単元のみ ⇒ 有限性).** $A$ を整数かつ weighted primitive(すなわち $\forall p:\ k_p(A)=0$)とする。$\sigma\in\mathbb Q^\times$ に対し
> $$ \sigma\cdot A\ \text{が再び整数かつ weighted primitive}\quad\Longleftrightarrow\quad \sigma=\pm1. $$

**証明.** まず $w_j\ge1>0$ より、任意の有理係数ベクトル $B$ について

$$ B\ \text{が整数}\ \iff\ \forall p,j:\ v_p(B_j)\ge0\ \iff\ \forall p:\ k_p(B)\ge0 $$

(⇐ は $\lfloor v_p(B_j)/w_j\rfloor\ge k_p(B)\ge0\Rightarrow v_p(B_j)\ge0$)。R1-N1 の計算より $k_p(\sigma\cdot A) = k_p(A)-v_p(\sigma) = -v_p(\sigma)$。したがって

- 整数性 $\iff\forall p:\ -v_p(\sigma)\ge0$、
- weighted primitive $\iff\forall p:\ -v_p(\sigma)=0$。

後者は $\forall p:v_p(\sigma)=0$、すなわち $\sigma=\pm1$。逆に $\sigma=\pm1$ なら $v_p(\sigma)=0$ で両条件を保つ。$\blacksquare$

**系 R1-N2a(§3.1 の有限性).** M1 正規形の一つの同値類内では、候補は M2 群 $\cong\mathbb Q^\times$ の**一軌道**である。M3+M4 を経た候補集合はその軌道のうち「整数かつ weighted primitive」なもの全体であり、R1-N2 によりそれは $\{\pm1\}\cdot\mathrm{wp}(A)$、すなわち**高々 2 個**。**有限性は証明された。** さらに

- 枝 (W): $w_j$ が偶数ゆえ $(-1)\cdot A = A$ ⇒ **係数ベクトルは 1 個**($\sigma=-1$ は $y\mapsto-y$ としてのみ効き、§4.1 で処理)。
- 枝 (N): $((-1)\cdot B)_j = B_j/(-1)^{6-j} = (-1)^jB_j$ ⇒ **係数ベクトルは高々 2 個**(§3.2 の tie-break が受け持つ)。

> **検算(単系統・整数演算)**: `search/wp-check.mjs`(node・BigInt 有理数・司令塔再走で 11649/0 再現)。無作為な有理係数ベクトル 400 組 × 2 枝に対し、(i) 無作為な $\sigma\in\mathbb Q_{>0}$ 6 通りでの R1-N1、(ii) 既定手続き($\sigma_3=1/\mathrm{lcm}$)での整数化と wp 一致、(iii) 出力の整数性・weighted primitivity・冪等性、(iv) $\sigma\ne\pm1$ での安定化の破れと $\sigma=-1$ での保存 — **計 11649 検査すべて一致・失敗 0**。符号作用も $(W)$ で不変・$(N)$ で $(-1)^j$ を確認。**入力は無作為な有理数のみで、曲線・$\lambda$・$u$ のデータを含まない。**

---

## Q3 → §3. 全順序と tie-break

### 3.1 有限性(**証明済み** — v1.1)

$$ \boxed{\text{M4 のあと残る候補集合が\textbf{有限}であることを、最小化の前に証明する。}} $$

有限でない(または有限性を証明できない)なら最小元は存在しないかもしれないので、**即 UNKNOWN 停止**(U-b)。

**この義務は v1.1 で履行された。** §2.4 の**補題 R1-N2**(残余 $=\{\pm1\}$)と**系 R1-N2a** により:

- 枝 (W): $\tau\mapsto-\tau$ は $A_j\mapsto A_j/(-1)^{2(5-j)} = A_j$ で係数に作用しない(作用は $y\mapsto-y$ のみ — §4 へ回る)。M3+M4 のあと $\tau\in\{\pm1\}$ ゆえ**候補は 1 個**。
- 枝 (N): $t\mapsto-t$ は $B_j\mapsto(-1)^{j}B_j$ で**係数を実際に動かす**。M3+M4 のあと $t\in\{\pm1\}$ ゆえ**候補は 2 個** ⇒ tie-break が要る(§3.2)。

**U-b は札として存続する**(fail-closed)。v1 では「有限性が未証明だから U-b が発火しうる」状態だったが、v1.1 では M1 が想定した二枝の正規形に**入らなかった**場合(例: $\deg f\notin\{5,6\}$、主係数がモニックにならない、$J$ の重みが (2.0) と異なる)にのみ発火する。**R1-N2 の前提($w_j\ge1$ の重み付き $\mathbb Q^\times$-作用・一軌道)が成り立たない入力を受け取ったら、規則を延長せずに U-b で止める。**

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

> **S5 設計 §3.3 の帰結(参考・依存しない)**: 枝 (W) では $P_0$ は自動的に非 Weierstrass になる。**直接証明**(便 32 F4.4 末尾の形・v1.1 で差替え): 命題 S5-3 の正規形 $b_0^2f_5 = a(x)^2-c_N(x-x_0)^5$($b_0\in\mathbb Q^\times$)で $a(x_0)=0$ とすると $(x-x_0)\mid a$、ゆえに $(x-x_0)^2\mid a^2$ かつ $(x-x_0)^2\mid(x-x_0)^5$ で $(x-x_0)^2\mid f_5$。**$f_5$ が $x_0$ で二重根をもつので $C:y^2=f_5$ は滑らかでない** — 種数 2 の非特異曲線という前提に反する。ゆえに $a(x_0)\ne0$、すなわち $y(P_0)=-a(x_0)/b_0\ne0$ で $P_0$ は非 Weierstrass。∎(S5 設計 v1.1 補題 S5-W) したがってこの行は**枝 (N) でのみ発火する見込み**である。ただし Rule 1 は S5 設計に依存しないので、両方書いておく。

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

U-1 は超楕円座標に依存する。モデル非依存の仕様を併記し、**両者が一致することを検査する**(U-3)。U-2 は**検査路**であって launch blocker ではない(便 32 F2.1)が、再現可能でなければ検査にならないので、v1.1 で ambient と単項式順序を値として固定する。

#### 5.2.0 ambient と単項式順序(v1.1 で明記・便 32 F2.1)

$C$ のアフィン座標環を $R := \mathbb Q[x,y]/(y^2-f(x))$ とする。$R$ の $\mathbb Q$-基底は単項式 $x^ay^b$($a\in\mathbb Z_{\ge0},\ b\in\{0,1\}$)。$P_\infty$ での極位数を $\operatorname{pol}(x^ay^b) := -\operatorname{ord}_{P_\infty}(x^ay^b)$ と書く。

| 枝 | $\operatorname{ord}_{P_\infty}(x),\ \operatorname{ord}_{P_\infty}(y)$ | $\operatorname{pol}(x^ay^b)$ | ambient $\mathcal A(n)$ | 同値 |
|---|---|---|---|---|
| **(W)** | $-2,\ -5$ | $2a+5b$ | $\operatorname{span}_{\mathbb Q}\{x^ay^b:\ b\in\{0,1\},\ 2a+5b\le n\}$ | $=L(nP_\infty)$ |
| **(N)** | $-1,\ -3$ | $a+3b$ | $\operatorname{span}_{\mathbb Q}\{x^ay^b:\ b\in\{0,1\},\ a+3b\le n\}$ | $=L(n\infty_++n\infty_-)$($\dim=2n-1$、$n\ge3$) |

枝 (N) では $x^ay^b$ は $\infty_+$ と $\infty_-$ の**両方**に極をもつので $\mathcal A(n)\ne L(nP_\infty)$ である。この場合

$$ L(n P_\infty)\ =\ L(n\infty_+)\ =\ \{\,g\in\mathcal A(n)\ :\ \operatorname{ord}_{\infty_-}(g)\ge0\,\} $$

は $\mathcal A(n)$ の**線型部分空間**($\infty_-$ での局所展開の主要部が消える、という $\mathbb Q$-線型条件)であり、局所展開は厳密に(冪級数の切断で)計算する。

$$ \boxed{\ \textbf{単項式順序(固定)}:\quad x^ay^b\ \prec\ x^{a'}y^{b'}\ :\Longleftrightarrow\ \bigl(\operatorname{pol},\,b,\,a\bigr)\ <_{\rm lex}\ \bigl(\operatorname{pol}',\,b',\,a'\bigr)\quad(\text{三成分とも昇順}).\ } \tag{5.2} $$

- 枝 (W) では $\operatorname{pol}=2a+5b$ が $b=0$ で偶数・$b=1$ で奇数($\ge5$)ゆえ**すべて相異なる**。第一成分だけで順序が確定し、tie-break $(b,a)$ は発火しない。
- 枝 (N) では $\operatorname{pol}=a+3b$ が同値になりうる(例: $x^3$ と $y$ はともに $3$)ので $(b,a)$ が実際に効く。(5.2) は $x^3\prec y$ を意味する。

$\mathcal A(n)$ の単項式を (5.2) の昇順に並べた列を $(m_1\prec\cdots\prec m_N)$ とし、$g=\sum c_{a,b}x^ay^b\in\mathcal A(n)$ の **ambient coefficient vector** を

$$ \operatorname{vec}(g)\ :=\ \bigl(c_{m_1},\,c_{m_2},\,\dots,\,c_{m_N}\bigr)\ \in\ \mathbb Q^N \tag{5.3} $$

と定める。**RREF はこの $\operatorname{vec}$ を行に並べた行列に対し、列を $m_1,\dots,m_N$ の順(左端が $m_1$)として取る**(pivot は最左優先)。RREF は部分空間と列順序だけで決まるので**一意**である。

#### 5.2.1 手順

1. $n_0 := \min\{\,n\ge1\ :\ \ell(nP_\infty-P_0) > \ell(nP_\infty-2P_0)\,\}$ を計算する(有限:$n\ge5$ なら $\deg(nP_\infty-2P_0)=n-2\ge3=2g-1$ で両者非特殊、$\ell$ は $n-2$ と $n-3$ で必ず相異なる。ゆえに $n_0\le5$)。
2. **対象空間**を $V := L(n_0P_\infty-P_0)\subseteq\mathcal A(n_0)$ とする(v1.1 修理: v1 は $L(n_0P_\infty)$ と書いていたが、それでは 4. の存在が保証されない)。$V$ は $\mathcal A(n_0)$ 内の線型条件($P_0$ での消滅、枝 (N) では加えて $\infty_-$ での正則性)で切り出す。
3. $V$ の任意の生成系の $\operatorname{vec}$ を行に並べ、(5.3) の列順序で **reduced row echelon form**(一意)を取る。得られた行を pivot 列の添字の昇順に $g_1,\dots,g_r$ と番号づける。
4. $\operatorname{ord}_{P_0}(g_i)=1$ を満たす $i$ のうち **最小のもの**を取り、$t_0 := g_i$ とする。
   **存在**: $\ell(n_0P_\infty-P_0)>\ell(n_0P_\infty-2P_0)$ なので、$V$ の**どの**基底にも $\operatorname{ord}_{P_0}=1$ の元が少なくとも一つある(全て $\operatorname{ord}_{P_0}\ge2$ なら $V\subseteq L(n_0P_\infty-2P_0)$ となり次元が矛盾)。存在しない出力が返ったら**入力破損 ⇒ integrity stop**(§9 I-e)。
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

> **補助経路 B′(S5 設計に依存・任意)**: 命題 S5-2 が成立するなら $\lambda=c\mu^2$、$\mu = v t^5(1+\cdots)$ で $u = cv^2$、かつ $\mu\mu^\iota = c_N(x-x_0)^5$(**v1.1: 記号を $c_N$ に統一** — S5 設計 v1.1 §3.3.0)から、$P_0$ 非 Weierstrass・$t=x-x_0$ の場合に $v = c_N/\mu^\iota(P_0)$(級数不要)。**B′ は第三経路であって B の代用ではない。** 用いる場合は独立な札で記録する。
>
> **【v1.1 の運用制限】B′ は $\lambda$ を $(c,\mu)$ に分離した形を要求するので、§9 I-b 厳格版の下では凍結 2 より前に走らせてはならない。** 凍結 2 のあとの独立な裏取りとしてのみ使う。

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
| **U-c** | M0 の Weierstrass 枝判定が、事前登録した計算予算内に閉じない。**予算 = M0 の一判定ジョブにつき wall-clock 600 秒**(v1.1 で §11 から本行へ移記・便 32 F2.5)。**timeout は U-c**(FAIL でも「非 Weierstrass」でもない)。**同 campaign 内で上限を増やして再分類しない** — 上限を変えるなら新 version の campaign |
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

**許可される出力**: 明示モデル $C/\mathbb Q$、Belyi 写像 $\lambda$(**完全な式として**)、分岐 divisor、cusp $P_0,P_\infty$、uniformizer $t$ の式、target triple への exact conjugator、分岐指数 10 の証明、$t$ が uniformizer であることの証明、$\operatorname{Aut}(C/\mathbf P^1)=1$ の証明、**および (7.1) による $b_i$ の計算と記録**(【司令塔修正 C1】: $b_i$ は $u$ に接触しない置換計算であり、BRIDGE-IN 組立ての一部として Model-Builder が計算・記録する。所有者の空白を残さないための明示)。

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

## §11. 論点(**v1.1 で 1–6 すべて決着** — 便 32 / 裁定 31)

1. **§9 I-b(命題 S5-4 由来の漏洩禁止)を採るか。** → **【決着・I-b 厳格版を採用】**(便 32 F2.3・裁定 31)。凍結 2 前は (i) $c$ の平方類・平方因子・符号を**計算しない**、(ii) $\lambda$ を $(c,\mu)$ の対として**報告しない**、(iii) それらを**候補選択に使わない**。代案(「分解形の報告は許し access log で担保」)は**採らない**。
   > **採用理由の補足(裁定 30 の但し書きつき)**: 「漏洩実害 = 可視性 × 選択自由度」という分析は原理として正しいが、**「選択自由度ゼロ」は正規化が total, executable, pre-frozen であるときにだけ成立する**(便 32 F2.3・★教材 23)。v1 は M4 が未定義でその前件が立っていなかった。**v1.1 の §2.2 M4 + §2.4 の R1-N1/N2 が前件を初めて成立させる**が、それでも I-b の緩和には使わない — 便 32 W4 の通り、full Belyi map を許す以上 $c$ の平方類は原理的に導出可能であり、担保は語彙 grep でなく **access control と total selection rule** の二重である。親 manifest 側にも同語で反映される(P3・司令塔)。
2. **§2 (M-A) と (M-B) の分離**は過剰か。 → **【決着・分離を維持。M-B は第一次規則へ昇格しない】**(便 32 F2.3・裁定 31)。理由は「S5 設計が未監査だから」ではなく、**M-B が strict I-b と両立しないから**である(solver が $c$ を明示変数として扱う)。監査が通っても自動昇格はしない。**M-B / $\mu$-正規形を discovery engine に使うなら、$c$ を凍結 2 前に人間へ見せない sealed automation を別 schema として事前登録する**(§2.3 の枠内)。v1.1 では M-A が正本、M-B は凍結 2 後の整合検査。
3. **§5.4 の観測 R1-C** を規則の緩和に使わないという判断でよいか。 → **【決着・承認】**(便 32 F2.1)。「R1-C は Kummer class の covariance を示すだけであり、生の $u$ の二経路比較に使う $t$ を曖昧にしてよい理由にはならない」。
4. **§6.2 B-ii の式 (6.2)** を経路 A と独立と認めてよいか。 → **【決着・独立と認定】**(便 32 F2.4)。B-ii は曲線上の Hensel/Newton 級数を作らず $\mathbb Q[x]$ 内の Taylor 係数と一点評価だけを使うため、§6.3(非共有 helper・raw 中間量の別保存)が実装でも守られる限り独立経路。**「多項式の Taylor 係数」という語だけを理由に級数経路と同一視しない。** B′ は第三経路であり B の代替にしない(現規定どおり)。
5. ~~U-c の計算予算の具体値を凍結 1 に書き込むべきか~~ → **【決着・§9.1 U-c の作用行へ移記済(v1.1・D8)】**(便 32 F2.5)。値 = M0 の一判定ジョブにつき wall-clock 600 秒。**論点欄に予算値を置かない**(未決パラメータに見えるため)。委嘱全体の cap は従来どおり委嘱ごと。
6. **【文献要請・充足】** §8.2 の $K^{\times10}$ 判定 → **`docs/文献ゲート_02_power_residue.md` が仕様 provenance として PASS**(便 32 F2.5)。$\zeta_2,\zeta_5\in K$ のもとで平方・五乗判定へ分解する exact Kummer 仕様と、valuation obstruction / binomial factorization の数学的出所は閉じた。
   > **ただし二つの留保(便 32 F2.5・そのまま採録)**: (i) Sol は Cohen/Roblot の一次 PDF と定理番号を独立照合していない。(ii) **文献は executable certificate checker ではない。** 凍結 1 の最終 bundle には §8.6 が要求する library 名・版・commit、アルゴリズム名、経路 A/B と第三 checker の commit を**値として**埋めること(P6 後半・実装別便)。

### 11.1 v1.1 時点で残る未充足項目(凍結 1 受理の前提)

| # | 項目 | 担当 | 状態 |
|---|---|---|---|
| R-1 | §8.6/§10-3 の実装版・commit・checker ID を**値として**記入 | 実装(P6 後半) | **未** |
| R-2 | 本文書 + 付録 A の新 digest 再取得と再提出 | 司令塔(P7) | **未**(本改訂で serialization が変わる) |
| R-3 | 親 manifest 側の whitelist/stop に I-b と同語を反映 | 司令塔(P1+P3) | 別便 |

**R-1〜R-3 が閉じるまで凍結 1 は受理されず、個別モデル探索コマンドは実行しない。**
