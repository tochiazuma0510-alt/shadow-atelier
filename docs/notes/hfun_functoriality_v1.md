# $H^{\rm fun}$ の quotient functoriality — 命題と証明 **v1**

2026-07-28: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔設問(裁定 101・Sol 便 73 Q6.1/Q6.2 の紙上化)。
**状態札**: `candidate / 単系統・未監査`。**commit していない。**
**依拠**: 正典(TB4 導出 v2.5・定義ノート v2・Rule 1 v1.5)+ `sol/sol_reply_73_math.md` Q1.1(座標)・Q6.1(発案)。**外部文献なし。$u$ の値・平方類には触れていない。**

> **本稿の独立性(重要)**: Sol の**命題 ODD-H**(Q1.2 の分類・`紙上証明候補`)には**依存しない**。$H^{\rm fun}$ について必要な性質を**直接**証明する(§2)。分類が後で修理されても本稿の命題は影響を受けない。

---

## 0. 座標辞書の検証(Sol Q1.1 を鵜呑みにしない)

$D_q$ の元を $r^as^e$、$D_q^3$ の元を成分ごとの積で扱う。$n\ge3$ 奇。
$$ A_n:=\langle a_1,a_2,a_3\rangle\cong(\mathbb Z/n)^3,\qquad a_i:=(\text{第 }i\text{ 成分だけ }r),\qquad Q:=\langle q_1,q_2\rangle,\quad q_i:=(\text{第 }i\text{ 成分だけ }1、他は }s). $$
すなわち $q_1=(1,s,s)$、$q_2=(s,1,s)$、$q_3=q_1q_2=(s,s,1)$。共役で $s$ は $r$ を反転するから符号表は

| | $a_1$ | $a_2$ | $a_3$ |
|---|---|---|---|
| $q_1$ | $+$ | $-$ | $-$ |
| $q_2$ | $-$ | $+$ | $-$ |
| $q_3$ | $-$ | $-$ | $+$ |

で **Sol Q1.1 の表と一致**(検証済)。正典の marking $X=(r,s,s)$、$Y=(rs,r,rs)$ に対し
$$ \boxed{\ X=a_1q_1,\qquad Y=a_1a_2a_3\,q_2\ } \tag{0.1} $$
である(直接計算: $a_1q_1=(r,1,1)(1,s,s)=(r,s,s)$ ✓、$a_1a_2a_3q_2=(r,r,r)(s,1,s)=(rs,r,rs)$ ✓)。**$Y$ の表示は Sol が書いていないので本稿で導出した。**

さらに $\langle X,Y\rangle=A_n\rtimes Q$(位数 $4n^3$)である: $X^2=a_1^2$ と $n$ 奇より $a_1$、ゆえに $q_1$;$Y^2=a_2^2$ より $a_2$;$Z:=a_2^{-1}a_1^{-1}Y=a_3q_2$ と $Z\,(q_1Zq_1^{-1})^{-1}=a_3^2$ より $a_3$、ゆえに $q_2$。∎

> **★ 型の注意**: 以下すべて **$n$ は奇**。使うのは (i) $2\in(\mathbb Z/n)^\times$、(ii) $1\ne-1$ in $\mathbb Z/n$(これは $n\ge3$ が要る)の 2 点だけである。

---

## 1. 対象

$$ \boxed{\ H_n^{\rm fun}\ :=\ H_{2,1,0}\ =\ \langle\,a_2,\ a_1a_3,\ q_2\,\rangle\ \le\ P_n\ } \tag{1.1} $$
$$ U_n:=\langle a_2\rangle\oplus\langle a_1a_3\rangle\ \le A_n,\qquad H_n^{\rm fun}=U_n\rtimes\langle q_2\rangle . $$

$d\mid n$ に対し、係数還元 $\mathbb Z/n\twoheadrightarrow\mathbb Z/d$ が誘導する
$$ \pi_{n,d}:P_n=A_n\rtimes Q\ \twoheadrightarrow\ A_d\rtimes Q=P_d,\qquad a_i\mapsto a_i,\quad q_j\mapsto q_j \tag{1.2} $$
を考える。**$Q$ の符号作用は $\pm1$ で $\mathbb Z$ 上定義されているから還元と可換**であり、$\pi_{n,d}$ は群準同型。(0.1) より
$$ \pi_{n,d}(X_n)=X_d,\qquad \pi_{n,d}(Y_n)=Y_d $$
なので $\pi_{n,d}$ は **marked quotient** である。

---

## 2. $H^{\rm fun}$ の基本性質(直接証明・分類に依存しない)

> ### 命題 HF-1(各段の性質)
> $n\ge3$ 奇とする。$H:=H_n^{\rm fun}$ について
> **(a)** $U_n$ は $q_2$-安定で $\lvert U_n\rvert=n^2$、$\lvert H\rvert=2n^2$、$[P_n:H]=2n$。
> **(b)** $\mathrm{ord}(X)=2n$。
> **(c)** $\langle X\rangle\cap H=1$、ゆえに **$\langle X\rangle$ は $P_n/H$ 上単純推移的**。
> **(d)** $N_{P_n}(H)=H$(**good**)。
>
> したがって $M:=2n$ と置けば **(W3)(W4) が全奇 $n\ge3$ で成立**する。

**証明.**
**(a)** $q_2(a_2)=a_2$、$q_2(a_1a_3)=a_1^{-1}a_3^{-1}=(a_1a_3)^{-1}$ より $U_n$ は $q_2$-安定。$\langle a_2\rangle$ と $\langle a_1a_3\rangle$ はともに位数 $n$ で、$U_n$ の元は
$$ a_2^{u}(a_1a_3)^{v}=a_1^{v}a_2^{u}a_3^{v}\qquad(u,v\in\mathbb Z/n) \tag{2.1} $$
と**一意に**書ける(第 1・第 2 座標が $v,u$ を決める)。ゆえに $\lvert U_n\rvert=n^2$。$q_2\notin A_n$ だから $\lvert H\rvert=2n^2$、$[P_n:H]=4n^3/2n^2=2n$。

**(b)** $q_1$ は $a_1$ を固定するから $X^2=a_1q_1a_1q_1=a_1^2q_1^2=a_1^2$。よって $X^{2k}=a_1^{2k}$、$X^{2k+1}=a_1^{2k+1}q_1$。$X^m=1$ には $Q$-成分の消滅から $m$ 偶数が要り、$m=2k$ で $a_1^{2k}=1\iff n\mid 2k\iff n\mid k$($n$ 奇)。最小は $k=n$、すなわち $\mathrm{ord}(X)=2n$。

**(c)** 奇冪 $a_1^{2k+1}q_1$ は $Q$-成分が $q_1\notin\{1,q_2\}$ ゆえ $H$ に入らない。偶冪 $a_1^{2k}\in H$ は $a_1^{2k}\in U_n$ を意味し、(2.1) の一意表示から $v=2k$(第 1 座標)かつ $v=0$(第 3 座標)、ゆえに $2k=0$、$n$ 奇より $k\equiv0$。よって $\langle X\rangle\cap H=1$。$\lvert\langle X\rangle\rvert=2n=[P_n:H]$ と合わせ $\langle X\rangle H=P_n$、すなわち単純推移。

**(d)** $a=a_1^{x_1}a_2^{x_2}a_3^{x_3}\in A_n$ とする。$A_n$ は可換なので $aU_na^{-1}=U_n$ は自動。$aq_2a^{-1}=a\cdot q_2(a)^{-1}\cdot q_2$ で
$$ a\cdot q_2(a)^{-1}=a_1^{x_1}a_2^{x_2}a_3^{x_3}\cdot a_1^{x_1}a_2^{-x_2}a_3^{x_3}=a_1^{2x_1}a_3^{2x_3}. $$
これが $U_n$ に入る条件は (2.1) より $2x_1=2x_3$ かつ第 2 座標 $0$、$n$ 奇($2$ 可逆)より $x_1=x_3$。そのとき $a=a_2^{x_2}(a_1a_3)^{x_1}\in U_n$。ゆえに $A_n\cap N_{P_n}(H)=U_n$。
$Q$ 側: $q_1$ が $U_n$ を保つとすると $q_1(a_1a_3)=a_1a_3^{-1}\in U_n$、(2.1) より $v=1$(第 1 座標)かつ $v=-1$(第 3 座標)、すなわち $1=-1$ in $\mathbb Z/n$、$n$ 奇 $\ge3$ に矛盾。$q_2$ は保つので $q_3=q_1q_2$ も保たない。ゆえに $N_{P_n}(H)\cap Q$ の寄与は $\langle q_2\rangle$ のみで、$N_{P_n}(H)=U_n\rtimes\langle q_2\rangle=H$。∎

> **★ (b) の副産物**: $\mathrm{ord}(X)=2n=M$ は、TB4-E の前件 **(E-iv)** が要求する「$\mu_M\xrightarrow{\sim}\langle X\rangle$」の**位数条件**をちょうど供給する(ただし $\zeta_M^{\rm Rule}\mapsto X$ という**命名規約**は供給しない — 便 73 Q3.3)。

---

## 3. 主命題 — quotient compatibility

> ### 命題 HF-2($H^{\rm fun}$ の functoriality)
> $n\ge3$ 奇、$d\mid n$、**$d\ge3$** とする。
> **(a)** $\pi_{n,d}\bigl(H_n^{\rm fun}\bigr)=H_d^{\rm fun}$。
> **(b)** よって well-defined な全射
> $$ \bar\pi_{n,d}:\ P_n/H_n^{\rm fun}\ \longrightarrow\ P_d/H_d^{\rm fun},\qquad gH_n^{\rm fun}\mapsto\pi_{n,d}(g)H_d^{\rm fun} $$
> が定まり、**全ての繊維の濃度は $n/d$** である(次数 $n/d$ の被覆)。
> **(c)** $\bar\pi_{n,d}$ は $\langle X\rangle$-同変: $\bar\pi_{n,d}(X_n\cdot\xi)=X_d\cdot\bar\pi_{n,d}(\xi)$。
> **(d)**(**poset functoriality**)$e\mid d\mid n$($e,d\ge3$)で $\bar\pi_{d,e}\circ\bar\pi_{n,d}=\bar\pi_{n,e}$、かつ $\bar\pi_{n,n}=\mathrm{id}$。
> **(e)**(**good の維持**)全ての $d\mid n$、$d\ge3$ で $N_{P_d}(H_d^{\rm fun})=H_d^{\rm fun}$。すなわち **detector は塔の全段で good**。

**証明.**
**(a)** $\pi_{n,d}$ は生成元を生成元へ送る: $a_2\mapsto a_2$、$a_1a_3\mapsto a_1a_3$、$q_2\mapsto q_2$。$\pi_{n,d}$ が全射準同型だから $\pi_{n,d}(\langle S\rangle)=\langle\pi_{n,d}(S)\rangle$、よって像は $\langle a_2,a_1a_3,q_2\rangle=H_d^{\rm fun}$。

**(b)** well-defined: $h\in H_n^{\rm fun}$ なら $\pi(gh)=\pi(g)\pi(h)\in\pi(g)H_d^{\rm fun}$((a) による)。全射性は $\pi_{n,d}$ の全射性から。
繊維の濃度: $P_n$ は $\pi_{n,d}$ を通して $P_d/H_d^{\rm fun}$ に作用し、$\bar\pi_{n,d}$ は $P_n$-同変である。両辺とも推移的 $P_n$-集合だから、$\bar\pi_{n,d}$ の繊維はすべて同じ濃度をもち、それは
$$ \frac{\lvert P_n/H_n^{\rm fun}\rvert}{\lvert P_d/H_d^{\rm fun}\rvert}=\frac{2n}{2d}=\frac nd . $$
(同値な数え方: $\lvert\pi_{n,d}^{-1}(H_d^{\rm fun})\rvert=\lvert H_d^{\rm fun}\rvert\cdot\lvert\ker\pi_{n,d}\rvert=2d^2\cdot(n/d)^3=2n^3/d$ ゆえ $[\pi_{n,d}^{-1}(H_d^{\rm fun}):H_n^{\rm fun}]=(2n^3/d)/(2n^2)=n/d$。)

**(c)** $\bar\pi(X_n gH_n)=\pi(X_ng)H_d=\pi(X_n)\pi(g)H_d=X_d\pi(g)H_d$((1.2) の marked 性)。

**(d)** 係数還元が $\mathbb Z/n\to\mathbb Z/d\to\mathbb Z/e$ で合成的だから $\pi_{d,e}\circ\pi_{n,d}=\pi_{n,e}$、剰余類へ降ろしても同じ。

**(e)** $H_d^{\rm fun}$ は $\mathbb Z/d$ 上の同じ式 (1.1) で与えられ、$d\ge3$ は奇($n$ 奇の約数)。ゆえに命題 HF-1(d) をそのまま $d$ に適用できる。∎

> **⚠ $d\ge3$ は落とせない**: $d=1$ では $A_1=1$、$P_1=Q\cong C_2^2$、$H_1^{\rm fun}=\langle q_2\rangle$。$Q$ は可換だから $N_{P_1}(H_1^{\rm fun})=Q\ne H_1^{\rm fun}$ で **good が壊れる**。命題 HF-1(d) の証明でも「$1\ne-1$ in $\mathbb Z/d$」が $d=1$ で失効する。**塔は $d\ge3$ の約数上でのみ good である。**

---

## 4. **$\alpha=1$ でなければならない理由**(発案より強い形)

Sol Q6.1 は「$\alpha=1$ はどの divisor でも $0$ に退化しないため全段で good」と述べる。**正しいが、なぜ $\alpha=1$ を選ぶ必要があるのかは、他の good $\alpha$ が退化しうることを言って初めて分かる。**

> ### 命題 HF-3(塔安定な $\alpha$ の特徴づけ)
> $n\ge3$ 奇、$\alpha\in\mathbb Z/n$ とし $H_{2,\alpha,0}=\langle a_2,a_1^\alpha a_3,q_2\rangle$ と置く。
> **(a)** $H_{2,\alpha,0}$ が good($=$ 自己正規化)$\iff\alpha\ne0$。
> **(b)** **全ての約数 $d\mid n$($d\ge3$)で good が保たれる $\iff\ \gcd(\alpha,n)=1$**、すなわち $\alpha\in(\mathbb Z/n)^\times$。
> **(c)** ゆえに **$\alpha\ne0$ だけでは塔安定に不十分**である。

**証明.** **(a)** 命題 HF-1(d) の計算を一般 $\alpha$ で繰り返す。$U=\langle a_2\rangle\oplus\langle a_1^\alpha a_3\rangle$ の元は $a_1^{\alpha v}a_2^ua_3^v$。$q_1$ が $U$ を保つ $\iff a_1^{\alpha}a_3^{-1}\in U\iff$($v=-1$ かつ $\alpha v=\alpha$)$\iff2\alpha=0\iff\alpha=0$($n$ 奇)。ゆえに $\alpha\ne0$ で good、$\alpha=0$ では $q_1$ が正規化して good でない。
**(b)** $\pi_{n,d}$ は $\alpha\mapsto\alpha\bmod d$ を与え、(a) より段 $d$ の good $\iff\alpha\not\equiv0\ (d)$。これが**全ての** $d\mid n$、$d\ge3$ で成り立つことと $\gcd(\alpha,n)=1$ の同値: $\Leftarrow$ は明らか。$\Rightarrow$ は、$p\mid\gcd(\alpha,n)$ なる素数 $p$ を取ると $p$ は奇で $p\ge3$、$p\mid n$、$\alpha\equiv0\ (p)$ ゆえ段 $p$ で good が壊れる。
**(c)** (b) の対偶の実例が §5 の反例表。∎

> **★ 結論**: 塔 detector として事前固定すべきは「$\alpha\ne0$ なる何か」ではなく **$\alpha\in(\mathbb Z/n)^\times$** であり、**$\alpha=1$ はその標準代表**である。**$n$ が素数のときは両者が一致するので差が見えない** — $n=3,5,7,11$ だけを見ていると気づけない型の条件である($K^{(3)}$・$K^{(5)}$ はどちらも素数)。**最初に差が出るのは $n=9$。**

---

## 5. 検算(補助・証明の一部ではない)

`node`・$D_q^3$ 上の悉皆列挙(整数演算のみ・曲線/$\lambda$/$u$ に非接触)。

**(1) 座標辞書と命題 HF-1**($n=3,5,7,9,11,15$):

| $n$ | 辞書 $X=a_1q_1$ / $Y=a_1a_2a_3q_2$ | $\lvert G_n\rvert$ | $\lvert H^{\rm fun}\rvert$ | $[G:H]$ | $\mathrm{ord}(X)$ | 自己正規化 | $\lvert\langle X\rangle\cap H\rvert$ |
|---|---|---|---|---|---|---|---|
| 3 | ✓ / ✓ | 108 $=4\cdot3^3$ | 18 $=2\cdot3^2$ | 6 $=2n$ | 6 $=2n$ | **true** | 1 |
| 5 | ✓ / ✓ | 500 | 50 | 10 | 10 | **true** | 1 |
| 7 | ✓ / ✓ | 1372 | 98 | 14 | 14 | **true** | 1 |
| 9 | ✓ / ✓ | 2916 | 162 | 18 | 18 | **true** | 1 |
| 11 | ✓ / ✓ | 5324 | 242 | 22 | 22 | **true** | 1 |
| 15 | ✓ / ✓ | 13500 | 450 | 30 | 30 | **true** | 1 |

**(2) 命題 HF-2(a)(b)**: $(n,d)\in\{(9,3),(15,3),(15,5),(45,3),(45,5),(45,9),(45,15),(21,3),(21,7),(27,3),(27,9)\}$ の **11 対すべて**で $\pi_{n,d}(H_n^{\rm fun})=H_d^{\rm fun}$ を集合一致で確認、次数 $2n/2d=n/d$ も一致。

**(3) 命題 HF-3(c) の反例**(good だが塔で退化):

| $n$ | $\alpha$ | good$(n)$ | $d$ | $\alpha\bmod d$ | good$(d)$ |
|---|---|---|---|---|---|
| 9 | 1 | true | 3 | 1 | **true** |
| **9** | **3** | true | 3 | 0 | **false** |
| **27** | **3** | true | 3 | 0 | **false** |
| **27** | **9** | true | 3 | 0 | **false** |
| **15** | **5** | true | 5 | 0 | **false** |
| 15 | 1 | true | 5 | 1 | **true** |
| **45** | **15** | true | 3 | 0 | **false** |

---

## 6. 射程(**証明していないもの**)

1. **Sol Q6.2 (6.3) の算術 compatibility $\operatorname{res}_{F_n/F_d}(a_d)=a_n^{n/d}$ は本稿の射程外・UNKNOWN。** 本稿は**群論・被覆の段**までで、局所座標・Kummer class へは持ち上げていない。**主係数の値から推測して採用してはならない**(Sol の警告に同意)。
2. **(W5)($\Lambda$ の $\Phi(\mathfrak F_0)$-安定)は本稿で扱っていない。** 命題 HF-1 が与えるのは (W3)(W4) のみ。**「$H^{\rm fun}$ を事前固定すれば (W5) も従う」とは主張しない。**
3. **$\Lambda_n$ の共役類構造・class selector としての一意性**(Sol Q1.5)には触れていない。本稿は「1 つの detector を固定したときの塔の整合」だけを述べる。
4. **命題 ODD-H(分類)には依存しない**が、逆に**分類を裏づけるものでもない**。
5. **$K^{(5)}$ の `all_two_classes` blind 規律**に遡及する主張はしていない(Sol Q6.1 と同旨)。

## 7. まとめ

$$ \boxed{\ H_n^{\rm fun}=\langle a_2,a_1a_3,q_2\rangle\ \text{は、奇 }n\ \text{の約数 }d\ge3\ \text{の poset 上で、次数 }n/d\ \text{の }\langle X\rangle\text{-同変被覆の塔をなし、全段で good.}\ } $$

塔安定性の真の条件は **$\alpha\in(\mathbb Z/n)^\times$**($\alpha\ne0$ では不足)であり、$\alpha=1$ はその標準代表。**値を見る前に detector を事前固定できる**という Q6.1 の設計目的は、この水準では**達成されている**。
