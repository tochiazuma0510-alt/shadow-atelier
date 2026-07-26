# 裁定素材 — 補題 D の背骨 $C_{\hat F_2}(x)=\langle x\rangle^{\rm cl}$ は無害か(Zalesskii–Zapata の「meta-procyclic」)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔の要裁定(scout 目標 3 再挑戦の地雷候補)への回答。**
対象: `docs/week4-A5算術飽和_v3.md` §1.4.3 **補題 D**。現物: `papers/delivered/zalesskii_zapata_1711.01500_profinite_extensions_centralizers.pdf`(**p.5 を実閲読**)。
状態: **紙上(Opus 単系統・Sol 未監査)**。便 18 の返信と突き合わせて裁定 16 へ。

---

## 0. 裁定(先に 3 行)

1. **(a) 無害。文脈違いである。** ZZ の当該文は **(i) 論理的に弱い主張**(procyclic ⇒ meta-procyclic なので我々の主張と矛盾しない)であり、**(ii) hyperbolic 元(どの自由因子にも共役でない元)まで含む一般形**として書かれている。**我々の $x$ は自由因子の非自明元(elliptic)**で、その場合は中心化群は因子そのもの = procyclic。
2. **(c) さらに自前証明を付けた**(§3)。$\hat F_2 = \langle x\rangle^{\rm cl}\amalg\langle y\rangle^{\rm cl}$(自由副有限積)+「相異なる因子の共役は自明に交わる」だけで閉じる。**この一行は補題 D を文献の細部から切り離す。**
3. **(b) 併せて補題 D の仮定を最小化した**(§4): 実際に要るのは $C(x)=\langle x\rangle^{\rm cl}$ と $\psi(C(y))\subseteq\hat{\mathbb Z}(0,1)$ の二つだけ。**しかも「$C(x)$ が procyclic」だけから前者が自動的に従う**(§4.2)ので、文献に求めるべき言明は **procyclic** で足り、**meta-procyclic では足りない**という切り分けを明示した。

---

## 1. ZZ の当該文(逐語・p.5 §3 冒頭)

> "In the discrete case, the centralizer of each non-trivial element in a free group is infinite-cyclic and, after performing an extension of centralizer, the centralizer of the element becomes abelian. **In the profinite case, the centralizer of each non-trivial element that generates $\widehat{\mathbb Z}$ in a free profinite group is meta-procyclic** and, after performing an extension of centralizer, the centralizer becomes either meta-abelian, or (non-trivial procyclic)-by-(infinite dihedral pro-$\pi$), or contains a non-abelian free pro-$p$ subgroup. See Lemma 4.2 and Theorem 4.3, and Proposition 4.7."

---

## 2. なぜ無害か(裁定の理由・3 点)

### 2.1 論理の向きが逆(最も単純な理由)

**procyclic な群は meta-procyclic である**(核が自明な procyclic-by-procyclic)。ゆえに ZZ の文は我々の $C(x)=\langle x\rangle^{\rm cl}$(procyclic)と**矛盾しない** — 我々の主張の方が**強い**。ZZ が弱い形で述べているのは、彼らの目的(centralizer の拡大を反復して得られる類 $\mathcal Z$ の記述)には meta-procyclic で十分だからである。

### 2.2 一般形は hyperbolic 元まで含む(本質的な理由)

$\hat F_2$ を標準 profinite tree に作用させると、元は二種に分かれる:

| 型 | 例 | 中心化群 |
|---|---|---|
| **elliptic**(ある自由因子の共役に入る) | **$x$、$y$**(基底元) | **因子そのもの = procyclic** |
| **hyperbolic**(どの因子の共役にも入らない) | $xy$、$xy^2x$ 等 | Tits straight path の安定化群に含まれる ⇒ **procyclic-by-procyclic が起こりうる** |

ZZ 自身が同論文 **Theorem 2.2 (c.3)** で「**infinite dihedral pro-$\pi$ group** $\mathbb Z/2\amalg^\pi\mathbb Z/2\cong\hat{\mathbb Z}_\pi\rtimes\mathbb Z/2$」を、(c.2) で「**Frobenius group** $\hat{\mathbb Z}_\pi\rtimes\mathbb Z/m$」を挙げており、**これらはまさに meta-procyclic であって procyclic ではない**。すなわち「meta-procyclic」という語は **hyperbolic 側を含めた一様な述語**として選ばれている。さらに p.5 の同じ文の後半(「extension of centralizer の後」)は $\Gamma *_Z(Z\times B)$ 型の**別の群**の話であり、自由副有限群の話ではない。

**我々の $x$ は基底元 = 自由因子 $\langle x\rangle^{\rm cl}$ の非自明元で、明確に elliptic 側**である。

### 2.3 「正規化群との混同」の可能性も否定できる

司令塔が挙げた第三の可能性(正規化群との混同)については、ZZ **Proposition 2.1** が **正規化群** $N_G(\overline{\langle c\rangle})=N_{G_1}(\overline{\langle c\rangle})\amalg_C N_{G_2}(\overline{\langle c\rangle})$ を**別命題として明示的に扱っている**ので、p.5 の "centralizer" は正規化群の言い換えではない。**中心化群と正規化群は同論文内で区別して使われている。**

> **⇒ 裁定(1 行)**: 「ZZ p.5 の meta-procyclic は **hyperbolic 元を含む一般形**であって、**自由因子の非自明元(= 我々の基底元 $x$)には procyclic な精密形が成り立つ**。procyclic ⇒ meta-procyclic なので矛盾はない。」

---

## 3. 自前証明(オプション (c))— 補題 D の背骨を文献から切り離す

> **補題 D0(基底元の中心化群).** $\hat F_2$ を階数 2 の自由副有限群、$x$ をその基底の一元とすると
> $$ \boxed{\ C_{\hat F_2}(x)\;=\;\langle x\rangle^{\rm cl}\;\cong\;\hat{\mathbb Z}.\ } $$

**証明.**
**(1) 自由副有限積への同定.** 有限群 $G$ に対し $\operatorname{Hom}_{\rm cont}(\hat{\mathbb Z},G)\cong G$ だから、$\langle x\rangle^{\rm cl}\amalg\langle y\rangle^{\rm cl}$ は「$G$ の元 2 個」を分類する普遍性をもつ。これは $\hat F_2$ の普遍性と同じなので
$$ \hat F_2\;\cong\;\langle x\rangle^{\rm cl}\amalg\langle y\rangle^{\rm cl}\qquad(\text{自由副有限積・因子は有限個ゆえ proper}). $$
**(2) 因子の共役の交わり.** 自由副有限積 $G=\coprod_iG_i$ では、**相異なる因子の共役は自明にしか交わらない**:
$$ 1\ne u\in G_i,\quad gug^{-1}\in G_j \;\Longrightarrow\; i=j\ \text{かつ}\ g\in G_i. \tag{3.1}$$
(離散自由積の古典的事実の副有限版。Ribes–Zalesskii の自由積の章。**これが唯一の外部入力**。)
**(3) 結論.** $g\in C_{\hat F_2}(x)$ とすると $gxg^{-1}=x\in\langle x\rangle^{\rm cl}$ なので (3.1) より $g\in\langle x\rangle^{\rm cl}$。逆の包含は自明。∎

**(2) を profinite Bass–Serre で置き換える版**(同じ結論・別経路): $\hat F_2$ は辺安定化群が自明・頂点安定化群が因子の共役である標準 profinite tree $T$ に作用する。$x\ne1$ の固定部分グラフ $T^x$ は閉部分グラフで、**頂点を 2 個以上含めば辺を含む**(辺のない連結 profinite グラフは 1 頂点)。辺安定化群は自明だから $x=1$ となり矛盾。ゆえに $T^x$ は唯一の頂点 $v_0$($\operatorname{Stab}(v_0)=\langle x\rangle^{\rm cl}$)。$g\in C(x)$ は $gT^x=T^{gxg^{-1}}=T^x$ を満たすので $gv_0=v_0$、すなわち $g\in\langle x\rangle^{\rm cl}$。∎

> **【GAP-D0】** (3.1)(および Bass–Serre 版の「辺安定化群自明」「頂点安定化群 = 因子の共役」)は**標準事実として引用**しており、原典の §/定理番号は未特定。**ただし ZZ 論文が同じ枠組み(Mel'nikov–Ribes–Zalesskii の副有限 Bass–Serre 理論)を前提として明示的に使っている**ので、出所は共有ツリー内で辿れる。**scout に投げるならこの形**(§5)。

---

## 4. 補題 D の仮定の最小化(オプション (b))

### 4.1 実際に使っている二点

補題 D の証明を追うと、中心化群は**二箇所**でしか使っていない。$\psi:\hat F_2\twoheadrightarrow\hat F_2^{\rm ab}=\hat{\mathbb Z}^2$(連続アーベル化、$x\mapsto(1,0)$、$y\mapsto(0,1)$)と書くと:

| 使用箇所 | 必要な言明 |
|---|---|
| (i) を満たす持ち上げが $\langle x\rangle^{\rm cl}$-torsor | **(H1)** $C(x)=\langle x\rangle^{\rm cl}$(⟺ $\psi(C(x))\subseteq\hat{\mathbb Z}(1,0)$ かつ $\psi\vert_{C(x)}$ 単射) |
| $f$ の取り替えの自由度が左からの $\langle y\rangle^{\rm cl}$ 倍 | **(H2)** $\psi(C(y))\subseteq\hat{\mathbb Z}(0,1)$ |

**最小形の証明**: $\alpha'=\mathrm{Ad}(g)\circ\alpha$、$g\in C(x^\chi)=C(x)$、$f'=h\,f\,g^{-1}$($h\in C(y^\chi)=C(y)$)。(ii) を両方に課すと $\psi(f)=\psi(f')=0$ より
$$ \psi(g)=\psi(h)\ \in\ \psi(C(x))\cap\psi(C(y))\ \overset{\rm (H1),(H2)}{\subseteq}\ \hat{\mathbb Z}(1,0)\cap\hat{\mathbb Z}(0,1)=0, $$
ゆえに $\psi(g)=0$、(H1) の単射性から $g=1$、すなわち $\alpha'=\alpha$。∎
(※ $C(x^\chi)=C(x)$ は $\chi\in\hat{\mathbb Z}^\times$ ゆえ $\langle x^\chi\rangle^{\rm cl}=\langle x\rangle^{\rm cl}$ から**構造理論なしで**従う。)

### 4.2 「procyclic」で足りるが「meta-procyclic」では足りない

> **補題 D1.** $C(x)$ が **procyclic** ならば自動的に $C(x)=\langle x\rangle^{\rm cl}$。
> **証明.** $\langle x\rangle^{\rm cl}\subseteq C(x)=\langle t\rangle^{\rm cl}\cong\hat{\mathbb Z}$ とすると $x=t^n$($n\in\hat{\mathbb Z}$)。$\psi(x)=(1,0)=n\,\psi(t)$ の第一成分から $n\alpha=1$、すなわち $n\in\hat{\mathbb Z}^\times$。ゆえに $\langle x\rangle^{\rm cl}=\langle t\rangle^{\rm cl}=C(x)$。∎
>
> **一方 meta-procyclic では足りない**: 例えば $C(x)\cong\hat{\mathbb Z}\rtimes\mathbb Z/2$ なら $\psi\vert_{C(x)}$ は単射でありえず(位数 2 の元は $\hat{\mathbb Z}^2$ で消えるか捻れを作る)、(H1) が壊れて**余剰の持ち上げが (i)(ii) を両立しうる**。司令塔の懸念は**この形で正確**である。

> **⇒ 文献に求めるべき言明は「$C(x)$ は procyclic」**(または (3.1))であって、**「meta-procyclic」では本当に足りない**。この切り分けが本裁定の実務的な核心。

### 4.3 仮に (H1) が壊れたときの被害範囲(退避線)

万一 $C(x)\supsetneq\langle x\rangle^{\rm cl}$ だとしても、余剰 $g_\gamma\in C(x)\cap\ker\psi$ の $A_5$ への像は $C_{A_5}(X)=\langle X\rangle\cong C_5$ に入るので、被害は **$\Lambda$ 上の affine 作用の平行移動部が 1-cocycle $a:G_{\mathbb Q}\to\mathbb F_5(1)$ だけずれる**ことに限局される(= 系 B′ と同型の被害)。すなわち **定理 A₅ の骨格は壊れず、Kummer 類が $[2]\cdot[c]^{\pm1}$ 型にずれるだけ**である。**ただしそれは判定を反転させうるので、退避線であって安全弁ではない。**

---

## 5. 司令塔への依頼(scout スペックの差し替え・1 行)

**現行の「Herfort–Ribes 1985 の中心化群定理」という狙いは外れている**(H–R は自由積の**捻れ元**の中心化群が主題)。差し替え先:

> **「自由副有限積 $G=\coprod_iG_i$ において、$1\ne u\in G_i$ かつ $gug^{-1}\in G_j$ ならば $i=j$ かつ $g\in G_i$」**(= 相異なる因子の共役は自明に交わる)の**定理番号**。第一候補 **Ribes–Zalesskii, *Profinite Groups*, 第 9 章(自由積)**。**「centralizer」ではなく「conjugates of free factors intersect trivially」で探すのが正しい検索語。**

これが取れれば §3 の補題 D0 が引用つきで閉じ、【GAP-D0】が消える。**取れなくても §3 の Bass–Serre 版が自前証明として残る**(枠組みは ZZ 論文が同じものを使っており共有ツリー内で辿れる)。

---

## 6. 便 18 との突き合わせ(司令塔へ)

Sol には補題 D を「$C_{\hat F_2}(x)=\langle x\rangle^{\rm cl}$($x$ は真の冪でない)」という形で監査に出している(v3 §1.4.3・対話帳 T-5 の (c))。**本裁定はその背骨を (a) 文脈判定 + (c) 自前証明 + (b) 仮定最小化の三重で補強するもので、Sol の判定と衝突しない**。もし便 18 が (H1) に疑義を出したら、**§4.2 の「procyclic で足りる/meta-procyclic では足りない」の切り分けと §3 の自前証明**をそのまま回答として使える。

**状態札**: 本裁定は **紙上・単系統・未監査**。ZZ p.5 と Prop 2.1・Thm 2.2 は**現物のページ画像で実閲読**した(テキスト抽出のみに依拠していない)。
