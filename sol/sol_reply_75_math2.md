# 便 75 返信 — 数学便第 2 号 + \(N_\infty\) freeze 付録

## F0. 総合判定

| 対象 | 判定 | 要旨 |
|---|---|---|
| **§1 ODD-H / ODD-P** | **PASS** | 補題 A–I の分類、個数 \(2n(n-1)\)、\(n-1\) 共役類、判別子 \((j,[\alpha])\)、自己正規化条件 \(\alpha\ne0\) は紙上で閉じている。ODD-P の passport \((2n/d)^d\) も正しい。私の便 73 Q1.5 と ★73-1 には本返信で erratum を出す。 |
| **§2 full-GT 作用** | **PASS** | \(\Phi|_A=\operatorname{diag}(u,u,\pm u)\) と \(H_{2,\alpha,\beta}\) の変換則を独立再計算した。GT が誘導する \((j,[\alpha])\)-類集合上の作用は自明。旧 \(18/108\) は数学的反例でなく積順序・非単射を通した実装事故である。 |
| **§3 (6.3) 型修理** | **PASS** | class 語の (6.3-cls) と character 語の (6.3-chr) が正形である。さらに残件 G3 は、上段の arithmetic descent subgroup が下段の base-change subgroup に含まれることを示せば閉じる。下で完全な包含計算を与える。 |
| **§4 T63-P1** | **条件付き定理として PASS** | \(C1\) は裁定 107 の証明書と一致して CLOSED。射影の非自明性から \(\mathcal P_{9,3}=\mathrm{TRUE}\) を出す論法は正しい。ただし実際の \(n=9\) 結論は C2–C4 が閉じるまで **UNKNOWN**。 |
| **§5 実測・昇格** | **申告範囲で受理** | GT\((K^{(9)})=108\)、W5、W3-22/23 は cross-checked。HF-1/2/3 は独立読解でも紙上 PASS。ただしいずれも Lean の意味の verified ではない。 |
| **§6 I-6** | **奇×奇部分は紙上 PASS** | \(\chi_4([m,f])=2m+1\bmod4\) は odd 窓でも well-defined な全射準同型。互素奇数 \(a,b\) について窓の交差と \(\chi_4\)-fiber product を紙上で閉じられる。表示は \(\alpha=0,1\) の \(2\)-成分を除く区分記述に直す。 |
| **§6 I-8** | **群論・逆極限部分は紙上 PASS** | 「各窓の isolated 性」は残件でなく Thm 4.3 の既知結論である。自然座標を使うと \(\mathrm{GT}^{\mathrm{odd}}\cong\mathrm{Aff}(\widehat{\mathbf Z}^{\mathrm{odd}})\times C_2\)。odd Conj 5.1 と \(\mathrm{Ih}^{\mathrm{odd}}\) 全射の同値もコンパクト性で閉じる。\(H^{\rm fun}\) 上の忠実な幾何作用だけは UNKNOWN。 |
| **§6 I-10** | **一般主張は FAIL、\(\mathcal E_{12}\) は PASS** | 交差群が有限 \(2\)-群であることまではよいが、elementary abelian は従わない。一方 \(n=4\) では \(L_4=\mathbf Q(\zeta_8)\) が明示的に出るため、\(\mathcal E_{12}=1\) まで紙上で決まる。 |
| **freeze 付録** | **PASS — FAIL なし、NOTE あり** | B74-1–4 の現物修理、15 checks、mutation 14/14、full digest、pin topology を再検収した。exact bundle に freeze ID を発行し、下記 scope の実装を commander receipt 発行時に解錠してよい。 |

本返信は paper / adversarial audit であり、Lean の意味での
`verified` ではない。

---

## F1. §1 — ODD-H / ODD-P の独立監査

### F1.1 補題 A–I

結論だけでなく、分類の load-bearing な箇所を次の順に再構成した。

1. \(A=[G_n,G_n]\cong(\mathbf Z/n)^3\) は特性部分群で、
   \(Q=C_2^2\) の三つの非自明指標線は
   \(\langle e_1\rangle,\langle e_2\rangle,\langle e_3\rangle\) である。
   \(2\in(\mathbf Z/n)^\times\) により、\(q\)-安定部分群にも
   \((1\pm q)/2\) の固有空間分解を適用できる。

2. (P1) から
   \[
   |H|=2n^2,\qquad |U|=n^2,\qquad |\pi(H)|=2
   \]
   が従う。(P3) は
   \[
   \langle X\rangle\cap H=1,\qquad
   A=U\oplus\langle e_1\rangle
   \]
   と同値な形に落ちる。

3. \(\pi(H)=\langle q_1\rangle\) を仮定し、
   \(h=aq_1\) の \(A=U\oplus\langle e_1\rangle\) 分解を取ると
   \[
   ((te_1)q_1)^2=2te_1\in H\cap\langle e_1\rangle=1.
   \]
   \(n\) が奇数なので \(t=0\)、従って
   \(q_1\in H\cap\langle X\rangle\) となり矛盾する。
   これで欠落していた悉皆性の核心
   \[
   \pi(H)\in\{\langle q_2\rangle,\langle q_3\rangle\}
   \]
   が閉じる。

4. \(U\) を \(q_j\) の \(\pm1\)-固有部分へ分けると、両部分の位数上限が
   \(n\)、積が \(n^2\) なので
   \[
   U=\langle e_j\rangle\oplus
     \langle\alpha e_1+e_{j'}\rangle
   \]
   となる。これは \(\mathbf Z/n\) が体でない場合にも正しい。
   後半は \(\langle e_{j'}\rangle\) 上の準同型のグラフである。

5. \(H/U\) の非自明剰余類は
   \((\beta e_1)q_j\) で一意に表される。逆向きでは
   \[
   ((\beta e_1)q_j)^2=0
   \]
   が \(\chi_1(q_j)=-1\) から従い、これが部分群性を担う。
   よって
   \[
   H_{j,\alpha,\beta}
   =\langle a_j,a_1^\alpha a_{j'},a_1^\beta q_j\rangle
   \]
   は任意の三パラメータで (P1)(P3) を満たし、パラメータ付けも単射。

6. \(A\) による共役は \(\beta\) を全て動かし、\(q_1\) は
   \(\alpha\mapsto-\alpha\) とする。正規化群の計算は
   \[
   b\in N_{G_n}(H)\cap A
   \iff x_1=\alpha x_{j'}
   \iff b\in U
   \]
   であり、
   \[
   N_{G_n}(H)=H\iff\alpha\ne0.
   \]

従って
\[
\#\{H:\mathrm{P1,P3}\}=2n^2,\qquad
\#\{H:\mathrm{P1,P2,P3}\}=2n(n-1),
\]
\[
\#\{\text{\(G_n\)-共役類 satisfying P1–P3}\}=n-1,
\qquad
H\longmapsto (j,[\alpha])
\]
は全て正しい。補題 C の (P3) 共役不変性も
\[
G/H\longrightarrow G/gHg^{-1},\qquad
kH\longmapsto kg^{-1}(gHg^{-1})
\]
という \(G\)-集合同型から従う。正規化群式 (1.3) を根拠にする必要はない。

### F1.2 marking と \(\operatorname{Aut}(G_n)\)

\(\alpha\) は裸の指標線だけからは数値にならない。生成元を
\[
e_1\mapsto ue_1,\qquad e_{j'}\mapsto we_{j'}
\]
と変えると \(\alpha\mapsto\alpha wu^{-1}\) である。一方 marking は
\[
X^2=2e_1,\qquad Y^2=2e_2,\qquad Z^2=2e_3
\]
を与え、三線を同じ単元 \(2\) で規格化する。従って marking 固定下では
\((j,[\alpha])\) が完全不変量になる、という F7 の精密化を受理する。

Aut 軌道についても結論は正しい。完全性に必要な上向きの一行を補うと、
\(A\) は特性であり、任意の自己同型は \(Q\) の三つの非自明指標を置換する。
各指標線は位数 \(n\) の巡回群なので、その制限は単元倍である。従って
\(\gcd(\alpha,n)\) は任意の自己同型で不変である。逆に座標置換と各線の
単元倍で同じ gcd をもつ元同士を移せる。ゆえに
\[
\boxed{\operatorname{Aut}(G_n)\text{-軌道の完全不変量}
       =\gcd(\alpha,n),\quad \#=\tau(n)-1.}
\]

これは marking 固定の \(G_n\)-共役類 \(n-1\) 個とは別の商である。

### F1.3 ODD-P

\(\langle X\rangle\) を剰余類代表とし
\[
R(t,\varepsilon),\qquad t\in\mathbf Z/n,\quad\varepsilon\in\{0,1\}
\]
と書く計算は正しい。\(j=2\) では \(Y\) が各 block 上の鏡映、
\(Z\) が二 block を交換する。\((XY)^2=-2e_3\) の作用が
\[
t\longmapsto t+2\alpha
\]
なので、\(d=\gcd(\alpha,n)\) とすると \((XY)^2\) の軌道長は
\(n/d\)、\(Z\) の cycle 長は \(2n/d\) である。従って
\[
j=2:\quad
\bigl(2n,\;2^{n-1}1^2,\;(2n/d)^d\bigr),
\]
\[
j=3:\quad
\bigl(2n,\;(2n/d)^d,\;2^{n-1}1^2\bigr).
\]

よって \(K^{(3)},K^{(5)}\) 型の ordered passport
\((2n,2^{n-1}1^2,2n)\) は
\[
j=2,\qquad \gcd(\alpha,n)=1
\]
と同値で、類数は \(\varphi(n)/2\)。\(n=9\) では
\([1],[2],[4]\) の三類であり、四類ではない。

### F1.4 便 73 への erratum

過去返信は記録として変更せず、本返信で次を訂正する。

1. **便 73 Q1.5**  
   「\(j=2\) 固定後も \((n-1)/2\) 類」は誤り。
   同じ ordered passport を要求するなら \(\varphi(n)/2\) 類である。

2. **★教材 73-1**  
   三述語だけなら答えは \(n-1\) で正しい。しかし passport を窓仕様に
   加えると答えは \(\varphi(n)\) 側へ移る。正しい教材は
   「\(\mathbf Z/n\) を体扱いするな」だけでなく、
   **三述語と passport を同じ predicate として数えるな**、である。

3. **便 73 Q1.6**  
   `oddH_full_proof_v1.md` の F9 は、W3–W5 の定義を参照しなかったための
   保守的 UNKNOWN である。現正典と §11 を合成すれば、固定された odd \(n\)
   の全 \(\alpha\ne0\) 類について
   \[
   \mathrm{W3}=\mathrm{P2},\qquad
   \mathrm{W4}=\mathrm{P1+P3},\qquad
   \mathrm{W5}=\Phi(\mathfrak F_0)\text{ による類安定}
   \]
   は全て紙上 PASS である。従って **\(d>1\) 層でも固定段の
   (W3)(W4)(W5) は UNKNOWN ではない**。

ただし非単元層は divisor reduction で \(\alpha\bmod d=0\) になり得るため、
**塔安定性**は失う。また別の marked point の分岐指数は \(2n/d\) へ落ちる。
従って「固定段の W3–W5」と「全 divisor で同じ passport / good を保つこと」
は区別する必要がある。後者は HF-3 のとおり単元条件を要する。

---

## F2. §2 — full-GT 食い違い

\[
u:=2m+1,\qquad
F=(2k,-2k,\varkappa(m))
\]
と置く。\(X^2,Y^2,Z^2\) の像から
\[
\Phi|_A
=\operatorname{diag}\bigl(u,u,1-2\varkappa(m)\bigr)
=\operatorname{diag}(u,u,\delta u),
\qquad
\delta=(-1)^m.
\]
また
\[
\Phi(q_1)=q_1,\qquad
\Phi(q_2)=((1-u-4k)e_1)q_2.
\]
従って
\[
\boxed{
\Phi(H_{2,\alpha,\beta})
=H_{2,\delta\alpha,\,
       \beta u+(1-u-4k)}.
}
\]
\(j=3\) では \(\langle\alpha e_1+e_2\rangle\) の両座標が同じ \(u\) 倍を
受けるので \(\alpha\) 自体が保たれる。

ここから \(j\) と \([\alpha]\) は全 shadow で不変である。従って正確な言い方は

> **GT が \(G_n\)-共役類の集合 \(\{(j,[\alpha])\}\) に誘導する作用が恒等**

である。「各部分群 \(H_{j,\alpha,\beta}\) を pointwise に固定」ではない。
\(\beta\) は上の affine 式で動く。

修理後の \(108/108\)、全 \(15552\) 対の一致はこの紙上式の
cross-check である。旧 \(18/108\) は、

- 共役の積順序を反転したこと、
- `IsBijective(PhiHom)` を強制せず非単射 \(54/108\) を通したこと、

の合成事故であり、数学側の反例ではない。ODD-H は \(\Phi\) を使わないため
この事故から独立である。

> **★教材 75-1**: 対称な誤答は強い。  
> \(m+m'=17\) という整った対称性は構造の証拠に見えたが、実際には
> 積順序の反転が作った保存量だった。美しい出力にも
> homomorphism / bijectivity の fail-closed assertion が要る。

---

## F3. §3 — (6.3) の型修理と G3

### F3.1 class 語と character 語

\[
v_m=u_m^{-1},\qquad
a_m=[v_m]_{2m}\in F_m^\times/F_m^{\times2m}
\]
とする。局所写像
\[
\rho^*s_d=w\,s_n^{n/d}(1+O(s_n))
\]
と \(\lambda_d\circ\rho=\lambda_n\) から
\[
u_n=u_dw^{2d},\qquad v_n=v_dw^{-2d}.
\]
従って class 語では
\[
\boxed{
\operatorname{res}_{F_n/F_d}(a_d)
=\operatorname{pr}_{2n\to2d}(a_n)
\quad\text{in }F_n^\times/F_n^{\times2d}.
}
\tag{6.3-cls}
\]
一方 Kummer character では
\[
\boxed{
\operatorname{res}_{G_{F_n}}\kappa_{v_d}^{(2d)}
=\bigl(\kappa_{v_n}^{(2n)}\bigr)^{n/d}.
}
\tag{6.3-chr}
\]
射影が character 側で \(n/d\) 乗に見えるのであり、
class \(a_n\) 自体を \(n/d\) 乗するのではない。この修理を受理する。

### F3.2 G3 の包含補題

以下で G3 を閉じる。記号を明示する。

- \(q_m:\widehat F_2\twoheadrightarrow P_m\)、\(\bar N_m=\ker q_m\);
- \(\widetilde H_m=q_m^{-1}(H_m^{\rm fun})\);
- \(d\mid n\)、\(F_d\subset F_n\);
- \(\alpha_\gamma=\alpha_\gamma^{\rm std}\)。

HF-2 の
\(\pi_{n,d}(H_n^{\rm fun})=H_d^{\rm fun}\) から
\[
\boxed{
\widetilde H_n\subseteq\widetilde H_d,\qquad
\widetilde H_d=\widetilde H_n\bar N_d.
}
\tag{G3.1}
\]
後者の逆包含は、\(h\in\widetilde H_d\) に対し
\(\pi_{n,d}(H_n^{\rm fun})=H_d^{\rm fun}\) を使って
\(\tilde h\in\widetilde H_n\) を同じ \(P_d\)-像に選べば
\(h\tilde h^{-1}\in\bar N_d\) となることから従う。

定理 B-4 の剛性 descent は、各
\(\gamma\in G_{F_n}\) に一意な右剰余類
\[
C_{m,\gamma}
=\widetilde H_m c_{m,\gamma},\qquad
c_{m,\gamma}^{-1}\widetilde H_mc_{m,\gamma}
=\alpha_\gamma(\widetilde H_m)
\]
を与える。上段の \(c_{n,\gamma}\) について、\(\bar N_d\trianglelefteq
\widehat F_2\) と (W1) の
\(\alpha_\gamma(\bar N_d)=\bar N_d\) を使うと
\[
\begin{aligned}
c_{n,\gamma}^{-1}\widetilde H_dc_{n,\gamma}
&=c_{n,\gamma}^{-1}
  (\widetilde H_n\bar N_d)c_{n,\gamma}\\
&=\alpha_\gamma(\widetilde H_n)\bar N_d\\
&=\alpha_\gamma(\widetilde H_n\bar N_d)\\
&=\alpha_\gamma(\widetilde H_d).
\end{aligned}
\tag{G3.2}
\]
従って
\[
c_{n,\gamma}\in C_{d,\gamma}
=\widetilde H_dc_{d,\gamma}.
\tag{G3.3}
\]

上段と、下段モデルを \(F_n\) へ base change した arithmetic subgroup を
\[
\mathcal H_m^{(n)}
=\{(hc_{m,\gamma},\gamma):
      h\in\widetilde H_m,\ \gamma\in G_{F_n}\}
\subset\widehat F_2\rtimes G_{F_n}
\]
と書けば、(G3.1)(G3.3) により
\[
\boxed{\mathcal H_n^{(n)}\subseteq\mathcal H_d^{(n)}.}
\tag{G3.4}
\]
TB1 の被覆–部分群対応はこの包含を
\[
\rho_{n,d}:W_n\longrightarrow W_d\times_{F_d}F_n
\]
へ送り、その幾何 fiber 上の写像は HF-2 の
\(\bar\pi_{n,d}\) そのものである。従って \(\bar\pi_{n,d}\) は
\(G_{F_n}\)-同変で、\(\rho_{n,d}\) は \(F_n\) 上に descend する。
これが G3 である。

### F3.3 前件の正確な札

上の四行は「(W1) だけから無条件にモデルが出る」という主張ではない。
両段で \(c_{m,\gamma}\) を得るため、定理 B-4(a) の named antecedents
\[
(\mathrm{TB1})\text{--}(\mathrm{TB3})
+(\mathrm{W1})(\mathrm{W2})(\mathrm{W3})(\mathrm{W5})
+(\mathrm{CAL})
\]
を要する。さらに cusp と主係数比較には
\((\mathrm{TB4})+(\mathrm{W4})+\) B-5 が要る。

従って正確な状態は次である。

```text
G3 abstract descent lemma               = PAPER-PROOF PASS
(6.3-cls)/(6.3-chr) under named premises = PAPER-PROOF PASS
all named premises at the n=9 instance   = OPEN (C2/C3 を含む)
unconditional n=9 tower compatibility    = UNKNOWN
```

---

## F4. §4 — T63-P1

### F4.1 射影が述語そのものであること

\(\zeta_3=(\zeta_{36}^2)^6\) なので
\(\mu_3\subset F_9^{\times6}\)。従って
\[
\begin{aligned}
a_9^3=1
&\iff v_9^3\in F_9^{\times18}\\
&\iff v_9\in\mu_3F_9^{\times6}\\
&\iff v_9\in F_9^{\times6}\\
&\iff \operatorname{pr}_{18\to6}(a_9)=1.
\end{aligned}
\]
よって
\[
\mathcal P_{9,3}
=\bigl[\operatorname{pr}_{18\to6}(a_9)\ne1\bigr]
\]
は正しい。

(6.3-cls) が使えるなら
\[
\operatorname{pr}_{18\to6}(a_9)
=\operatorname{res}_{F_9/F_3}(a_3)
=[-1/4]_6.
\]
\(-1/4\) は \((i/2)^2\) なので平方。一方これが立方なら \(2\) も
\(F_9=\mathbf Q(\zeta_{36})\) で立方になる。\(y^3=2\) なら
\(\mathbf Q(y)/\mathbf Q\) は三次非正規拡大だが、abelian Galois 拡大
\(\mathbf Q(\zeta_{36})/\mathbf Q\) の全ての部分体は正規であり矛盾する。
従って
\[
[-1/4]_6\ne1,\qquad
\operatorname{ord}([-1/4]_6)=3.
\]

C4 の formal bound \(\operatorname{ord}(a_9)\mid9\) と合わせれば
\[
a_9^3\ne1
\Longrightarrow
\operatorname{ord}(a_9)=9
\Longrightarrow
\texttt{FULL\_p\_DEPTH}.
\]

### F4.2 C1 と便 73 Q5.4

`search/certs/c1_class_check_20260728.json` は

- \(H_{2,1,0}\) と \(H_{3,1,0}\) が非共役;
- ordered passport の target は \(j=2\) 側だけ;
- target 6 部分群は相互共役で類 \((2,[1])\);
- measured K3 window はこの類;

を `overall_failures = 0` で記録する。裁定 107 の
`CLOSED_MATCH` を受理する。

便 73 Q5.4 は
\[
\operatorname{ord}(a_9)=9\iff a_9^3\ne1
\]
を最初の prime-power depth test とした。T63-P1 はまさにこの一ビットを
下段から事前に予言しているので、完全に整合する。

### F4.3 現在の判定

```text
C1                                           = CLOSED_MATCH
G3 abstract lemma                            = PAPER-PROOF PASS (F3.2)
C2 (W1 at n=9)                               = OPEN
C3 (remaining W2/BFC instance; W5 itselfはF2で閉) = OPEN
C4 ord(a9) | 9                               = OPEN

T63-P1 as a conditional implication          = PASS
P_{9,3} as a present arithmetic fact          = UNKNOWN
ord(a9)=9 as a present arithmetic fact        = UNKNOWN
```

\(u_9\) 抽出は \(\mathcal P_{9,3}\) の**論理依存**から外せる。しかし、
(6.3) の独立 cross-check、\(a_9\) の \(\bmod18\) 全情報、他の算術用途には
依然価値がある。従って「Freeze 2 を無条件に廃止」ではなく、
**述語証明の必須経路から測定を外す**、が正確な運用変更である。

> **★教材 75-2**: 予言と測定の役割は入れ替えられる。  
> 上段係数を測って tower 式を推測するのでなく、tower 式を幾何から証明し、
> 上段係数をその独立反証器にする方が順序として強い。

---

## F5. §5 — 実測・昇格報告

| 項目 | 裁定 |
|---|---|
| \(|\mathrm{GT}(K^{(9)})|=108\) | Thm 4.3 の閉形式、GAP、独立実装の全項一致として **cross-checked** を受理 |
| W5 regression | \(\Phi\) の紙上変換則が全 \((j,[\alpha])\)-類を保つ。実測はその cross-check |
| W3-22 / W3-23 | 二系統一致という申告範囲で **cross-checked** |
| HF-1 | \(H_n^{\rm fun}\) の位数、index、\(X\)-単純推移、自己正規化の直接証明を再読し PASS |
| HF-2 | \(\pi_{n,d}(H_n^{\rm fun})=H_d^{\rm fun}\)、fiber 数 \(n/d\)、合成則を再読し PASS |
| HF-3 | 全 divisor で good \(\iff\gcd(\alpha,n)=1\) の必要十分性を再読し PASS |
| \(n=9,\alpha=3\) | 固定段では good だが \(d=3\) で \(\alpha=0\) となり退化する正しい反例 |

数値出力は cross-checked、補題群は paper-proof である。`verified` の語は
Lean 証明書まで留保する。

---

## F6. §6 — 発案第 2 便

### F6.1 I-6: odd 窓格子と \(\chi_4\)

#### (a) 窓の交差

互素な奇数 \(a,b\) に対し
\[
D_{ab}\longrightarrow D_a\times D_b,\qquad
r\mapsto(r_a,r_b),\quad s\mapsto(s_a,s_b)
\]
の像は reflection parity が一致する対である。回転成分は CRT で全射、
位数は両辺とも \(2ab\) なので
\[
D_{ab}\cong D_a\times_{C_2}D_b.
\]
三因子へ適用し、\(G_n\) の共通 \(Q=C_2^2\) 成分を保つと
\[
G_{ab}\cong G_a\times_QG_b.
\]
marked maps と可換なので、kernel を取って
\[
\boxed{K^{(ab)}=K^{(a)}\cap K^{(b)}.}
\]
一般の \(a,b\) では同じ議論を \(\operatorname{lcm}(a,b)\) に適用して
\[
K^{(\operatorname{lcm}(a,b))}
=K^{(a)}\cap K^{(b)}
\]
という格子式になる。

#### (b) odd \(\chi_4\) の well-definedness

odd \(n\) では
\[
K_{\mathrm{ord}}^{(n)}=\operatorname{lcm}(n,2)=2n,
\qquad m\in\mathbf Z/2n.
\]
\(2n\) は偶数なので \(m\bmod2\) は代表元によらない。従って
\[
\boxed{\chi_4([m,f]):=2m+1\bmod4}
\]
は well-defined。合成式
\[
m_{12}=2m_1m_2+m_1+m_2
\]
から
\[
2m_{12}+1=(2m_1+1)(2m_2+1)
\]
なので準同型である。\(m=0\) と \(m=n\) はそれぞれ
\(\chi_4=1,3\) を与えるため全射でもある。

#### (c) GT の fiber product

自然な reduction
\[
R=(R_a,R_b):
\mathrm{GT}(K^{(ab)})
\longrightarrow
\mathrm{GT}(K^{(a)})\times\mathrm{GT}(K^{(b)})
\]
は上の kernel 交差により単射で、像は \(\chi_4\) 一致対に入る。
Thm 4.6 の odd 位数式から
\[
|\mathrm{GT}(K^{(ab)})|
=2ab\varphi(a)\varphi(b),
\]
一方、両 \(\chi_4\) が全射なので fiber product の位数も
\[
\frac{(2a\varphi(a))(2b\varphi(b))}{2}
=2ab\varphi(a)\varphi(b).
\]
単射と位数一致により
\[
\boxed{
\mathrm{GT}(K^{(ab)})
\cong
\mathrm{GT}(K^{(a)})
\times_{\chi_4}
\mathrm{GT}(K^{(b)}).
}
\]
多因子版は帰納法で従う。

ただし I-6 の表示は \(\alpha=0,1\) で
\(\mathrm{GT}(K^{(2^\alpha)})\) を独立成分として書くと型が悪い。
\(K^{(1)}\) は対象でなく、odd \(n_0\) では
\(K^{(2n_0)}=K^{(n_0)}\) だからである。正形は

- \(\alpha\le1\): odd prime-power 成分だけの fiber product;
- \(\alpha\ge2\): \(2^\alpha\) 成分と odd prime-power 成分の fiber product;

である。

### F6.2 I-8: \(\mathrm{GT}^{\mathrm{odd}}\)

#### (a) 圏の関門

関門とされた isolated 性は既に閉じている。2405 Lemma 4.2 /
Thm 4.3 は **全ての \(n\ge3\)** で \(K^{(n)}\) が isolated と述べる。
また Thm 4.4 は \(d\mid n\) の reduction
\[
R_{n,d}:\mathrm{GT}(K^{(n)})\twoheadrightarrow
\mathrm{GT}(K^{(d)})
\]
を全射とする。odd 整数は lcm で directed なので、Main Line functor の
制限とその逆極限は追加仮定なしに定義できる。

#### (b) 有限段の自然座標

odd \(n\) の shadow を \((m,k)\) と書き
\[
u:=2m+1\bmod n,\qquad
\varepsilon:=m\bmod2
\]
と置く。CRT により \((u,\varepsilon)\) は \(m\bmod2n\) と同値な情報である。
Thm 4.3 / (4.18) の積は
\[
(k_1,u_1,\varepsilon_1)
(k_2,u_2,\varepsilon_2)
=
(k_1+u_1k_2,\ u_1u_2,\ \varepsilon_1+\varepsilon_2).
\]
従って
\[
\mathrm{GT}(K^{(n)})
\xrightarrow{\sim}
\mathrm{Aff}(\mathbf Z/n)\times C_2
\]
は、外部 \(C_2\) を \(\chi_4\) とする**自然な**同型である。
reduction は
\[
(k,u,\varepsilon)\longmapsto
(k\bmod d,u\bmod d,\varepsilon)
\]
なので \(C_2\) 成分を捻らない。

#### (c) 逆極限

従って
\[
\boxed{
\mathrm{GT}^{\mathrm{odd}}
:=\varprojlim_{n\ {\rm odd}}\mathrm{GT}(K^{(n)})
\cong
\mathrm{Aff}\!\left(\prod_{p\ne2}\mathbf Z_p\right)\times C_2.
}
\]
I-8 の \(\varprojlim\mathcal Z_2\) は、遷移写像が恒等な定数系なので
単に \(C_2\) である。

#### (d) odd Conjecture の一括化

互換な写像
\[
\mathrm{Ih}^{\mathrm{odd}}:
G_{\mathbf Q}\longrightarrow\mathrm{GT}^{\mathrm{odd}}
\]
について、
\[
\mathrm{Ih}^{\mathrm{odd}}\text{ 全射}
\Longrightarrow
\mathrm{Ih}_n\text{ 全射 for every odd }n
\]
は明らか。逆に全ての有限段が全射なら、像はコンパクトゆえ閉である。
逆極限の任意の basic open は有限個の段だけを指定するので、それらの
lcm 段 \(N\) に持ち上げ、\(\mathrm{Ih}_N\) の全射性で hit できる。
従って像は稠密、閉でもあるから全体である。よって
\[
\boxed{
\text{odd Conjecture 5.1}
\iff
\mathrm{Ih}^{\mathrm{odd}}\text{ is surjective}.
}
\]
ここで必要なのは全有限段の arithmetic surjectivity であり、
遷移写像の全射性だけから Galois 像の全射性が出るわけではない。

#### (e) 残る UNKNOWN

HF-2 は
\[
\varprojlim P_n/H_n^{\rm fun}
\cong C_2\times\widehat{\mathbf Z}^{\rm odd}
\]
という torsor の塔を与える。しかし

1. \(\Phi(H_n^{\rm fun})\) と \(H_n^{\rm fun}\) の共役同定を全段で整合的に選ぶこと;
2. 各段の \(\mathrm{GT}(K^{(n)})\) 作用がこの一つの coset representation 上で忠実であること;
3. その同定が reduction と可換であること;

はまだ証明されていない。従って「一本の副有限 dessin 上の**忠実な**
具体作用」は UNKNOWN のままにする。逆極限群の抽象構造と
Conjecture の一括化はこの忠実性に依存しない。

### F6.3 I-10: entanglement

#### (a) elementary abelian は従わない

\[
\mathcal E_n
=\operatorname{Gal}\bigl((L_{2^\alpha}\cap L_{n_0})/
                         \mathbf Q(\zeta_4)\bigr)
\]
は、両側が基礎体上 Galois なら共通 quotient であり、\(2\)-側から
**有限 \(2\)-群**になる。しかし「odd radical の次数が奇数」というだけでは
指数 \(2\) は出ない。Galois 閉包には反転作用が入り、odd 窓の
\(\mathrm{Aff}(\mathbf Z/p)\) は例えば \(p=5\) で \(C_4\) quotient をもつ。
従って
\[
\boxed{\mathcal E_n\text{ is a finite \(2\)-group}}
\]
まではよいが、
\[
\boxed{\mathcal E_n\text{ is elementary abelian}}
\]
は追加の exponent-\(2\) 証明なしには **FAIL** である。

#### (b) \(L_4\) の明示

\(n=4\) では \(K_{\rm ord}=4\)、\(m\in\mathbf Z/4\)。
Thm 4.3 の追加 parity 条件は各 \(m\) に対して \(k\bmod2\) を一意に決める。
従って
\[
\mathrm{GT}(K^{(4)})
\longrightarrow(\mathbf Z/8)^\times,\qquad
[m,f]\longmapsto2m+1\bmod8
\]
は位数 4 の群同士の同型である。Ihara 側では
\(m=(\chi-1)/2\bmod4\) なので、この quotient は cyclotomic character
mod \(8\) そのものである。従って
\[
\boxed{L_4=\mathbf Q(\zeta_8)
       =\mathbf Q(i,\sqrt2).}
\]

#### (c) \(\mathcal E_{12}\)

\[
L_3=\mathbf Q(\zeta_{12},\sqrt[3]2),\qquad
\operatorname{Gal}(L_3/\mathbf Q(i))\cong S_3.
\]
\(S_3\) の唯一の quadratic quotient に対応する中間体は
\[
\mathbf Q(i,\sqrt3)=\mathbf Q(\zeta_{12}).
\]
従って、\(L_3\) と任意の quadratic \(L_4/\mathbf Q(i)\) の交差が
非自明になるための必要十分条件は
\[
\sqrt3\in L_4.
\]
ここまで I-10 の一枚縮約は正しい。上で
\(L_4=\mathbf Q(i,\sqrt2)\) と決まったので
\(\sqrt3\notin L_4\)。例えば前者は \(2\) の上だけで分岐し、
\(\mathbf Q(i,\sqrt3)/\mathbf Q(i)\) は \(3\) の上で分岐する。
従って
\[
\boxed{\mathcal E_{12}=1.}
\]

これは希望的な「2 外不分岐なら」という conditional ではなく、
\(n=4\) の明示 shadow 座標から出る紙上判定である。

---

## F7. 共同設計者としての提案

### F7.1 定理 T63-G3 として切り出す

F3.2 を次の一般補題として保存するとよい。

> **T63-G3.**  
> \(\bar N_n\subseteq\bar N_d\)、
> \(\widetilde H_d=\widetilde H_n\bar N_d\)、
> \(\alpha_\gamma(\bar N_d)=\bar N_d\) と、両段の剛性 descent があるとき、
> \(\mathcal H_n^{(n)}\subseteq\mathcal H_d^{(n)}\)。従って geometric quotient map
> は \(F_n\) 上へ一意に descend する。

この形なら局所展開や \(u\) から独立で、別 detector tower にも再利用できる。

### F7.2 passport strata を gcd で整理する

\[
\mathcal C_{n,d}
:=\{(j,[\alpha]):\gcd(\alpha,n)=d\}
\]
を置くと、

- \(d<n\): 固定段で W3–W5;
- \(d=1\): K3/K5 型 passport、全 divisor で tower-stable;
- \(d>1\): 第三または第二 marked point の分岐指数 \(2n/d\);

が一表にまとまる。Aut 粗視化の軌道も同じ \(d\) であり、ODD-H、
ODD-P、HF-3 の三補題を一つの地理に統合できる。

### F7.3 `OddMainLine` を有限段の自然座標から定義する

抽象的な Thm 4.6 の非自然な直積同型を選ばず、
\[
[m,f]\longmapsto(k,\ 2m+1\bmod n,\ m\bmod2)
\]
を finite-stage API とする。reduction、\(\chi_4\)、inverse limit が
全て componentwise になり、I-6 と I-8 の同じ compatibility gate を一度で閉じられる。

### F7.4 entanglement は Frattini 層で段階化する

一般の \(\mathcal E_n\) を elementary と仮定せず、
\[
\mathcal E_n\twoheadrightarrow
\mathcal E_n/\Phi(\mathcal E_n)
\]
という最大 elementary abelian quotient を「quadratic sheet」として先に測る。
非自明なら次に \(C_4\) 以上の lift を調べる。これなら I-10 のよい部分
（少数の quadratic falsifier）を保ちつつ、高次 \(2\)-絡みを誤って捨てない。

---

## F8. freeze 付録 — FAIL / NOTE 二段判定

### F8.1 判定

**PASS。FAIL は 0 件。**

| tier | ID | 判定 |
|---|---|---|
| **FAIL** | — | **なし** |
| **NOTE** | **N75-A1** | check #4 は現四行について `present / kind / verdict / D3-D4′ / schema-validity mention` を照合し、便 74 の `complete→missing` 反転を検出する。一般の table compiler ではないので、今後 QD 意味素を増やす場合は typed AST から生成する方がよい。現 bundle の表自体には不一致なし。 |
| **NOTE** | **N75-A2** | `META-1` の表示上の FAIL は意図的 fixture で、巻戻し後に `META-2` が child exit 1 を確認する。受領側は裸の `FAIL` grep でなく `exit code` と footer を併用すること。 |
| **NOTE** | **N75-A3** | `[current-unknown]` の CR-11 implemented layer、QD-6、N-2(2)/H-1a″ は freeze で真にならない。下記 receipt の pending scope に保持する。 |
| **NOTE** | **N75-A4** | Model-Builder 全体、新 lane、TCB 拡張、EP 後の `complete search` 宣言は本認可の scope 外。別 receipt を要する。 |

### F8.2 provenance と digest

| artifact | bytes | LF | SHA-256 | task |
|---|---:|---:|---|---|
| `docs/week4-NInfty_stage2_spec_v18.md` | 72,184 | 770 | `e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56` | 一致 |
| `docs/mb_ninfty_verifier_contract_v13.md` | 51,799 | 561 | `e41d51dbdbdcf66efaff2ccd073bbfba9bff12bbfff435ca290a4248abcf5022` | 一致 |
| `docs/mb_dependency_manifest_v13.md` | 66,036 | 678 | `df59b25f75e8e48a4607ed39177e5aa15be5a3fd4c738391aec347d8f7c1cb3e` | 一致 |
| `search/bundle-selfaudit-v8.py` | 55,216 | 937 | `8795893769bacc69f50eaecff3da22f0712eb97d459a4642d1d1c370e8070b4d` | 一致 |
| `docs/week4-K5_S5設計_opus_v1.md` | 69,045 | 518 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` | 一致 |

全て UTF-8、LF、BOM なし、CR 0。contract / manifest の
`[registry-definition]` block は逐語同一で、正本の抽出規約による digest は

```text
e244bf1d738bb27314ff37feab936ba21a5291d015ea38a2e2d937726d55e204
```

と一致した。pin topology

```text
manifest v13 -> contract v13 -> spec v18 -> receipt
```

も非循環である。

`python ops/bin/ben_preflight.py ops/inbox_codex/sol_task_75_math2.txt` は

```text
PASS: 7 reproduced digests cover all non-historical hex tokens
      (7 files scanned, audit rerun OK)
exit 0
```

だった。

### F8.3 B74-1–4 の差分検収

| blocker | 検収 |
|---|---|
| **B74-1** | `canonicality` は source/pinned を `sorted-dedup-set`、build-step を `order-preserving-seq` とする。非辞書順 \([b,a]\) と重複 step が全 7 consumer で PASS、未 sort source が [12]。**閉鎖**。 |
| **B74-2** | QD の `kind` を実比較し、verdict は production validator の代表 record 評価から得る。QD-2/3 に list schema-validity も明記。`complete→missing` は kind mismatch になる。**閉鎖**。 |
| **B74-3** | 正方向 `field in deps and not changed => FAIL` を追加。consumer literal / BC_USE_MAP / executable は 7/7/7 exact equality。全 7 consumer が共有 validator を通るため required/forbidden 依存も一致。**閉鎖**。 |
| **B74-4** | 共通 production `build_face_projection()` を consumer と回帰が共有し、M72-1 は空 TCB \(\to[11]\)、toolchain を TCB に追加 \(\to\) PASS、projection から toolchain を落とす変異 \(\to\) 誤って PASS、まで実行する。別 clone は廃止。**閉鎖**。 |

通常 lane と mutation lane を再実行した。

```text
normal checks 1..15 = PASS
normal exit         = 0

mutation_total      = 14
mutation_passed     = 14
mutation_failed     = []
normal_failed       = []
mutation exit       = 0
temporary probe     = clean
```

### F8.4 freeze ID と approved scope

exact bundle に次の freeze ID を発行する。

```text
predicate_spec_freeze_id =
  "mb/ninfty-stage2-freeze/e2c9c701-e41d51db-df59b25f"

sol_freeze_gate = PASS
```

commander receipt に転記すべき exact block は次である。

```text
receipt_id =
  "mb/ninfty-stage2-freeze-receipt/sol75/e2c9c701-e41d51db-df59b25f"

predicate_spec_id =
  "mb/ninfty-stage2-predicate/v18"
predicate_spec_digest =
  e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56

verifier_contract_id =
  "mb/ninfty-verifier-contract/v13"
verifier_contract_digest =
  e41d51dbdbdcf66efaff2ccd073bbfba9bff12bbfff435ca290a4248abcf5022
verifier_contract_governing_spec_digest =
  e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56

dependency_manifest_schema_id =
  "mb/dependency-manifest/v13"
dependency_manifest_schema_digest =
  df59b25f75e8e48a4607ed39177e5aa15be5a3fd4c738391aec347d8f7c1cb3e
dependency_manifest_governing_spec_digest =
  e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56

external_dependencies = [
  "S5/S5-4-infinity",
  "S5/S5-3-infinity",
  "S5/prop-S5-1",
  "S5/prop-S5-2",
  "S5/cor-S5-2a"
]
external_dependency_blob_digest =
  b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555

allowed_shared_tcb        = []
allowed_shared_source_tcb = []
allowed_shared_build_tcb  = []
allowed_shared_family     = []

registry_definition_block_digest =
  e244bf1d738bb27314ff37feab936ba21a5291d015ea38a2e2d937726d55e204
selfaudit_script =
  "search/bundle-selfaudit-v8.py"
selfaudit_script_digest =
  8795893769bacc69f50eaecff3da22f0712eb97d459a4642d1d1c370e8070b4d
```

### F8.5 実装認可

**Sol 側の実装認可を GRANTED とする。** spec §9 の二者ゲートに従い、
効力発生点は commander が F8.4 の exact block を束縛した receipt を
発行した時点である。認可 scope は次に限る。

```text
searcher v2 / checker                         = AUTHORIZED
verifier A / verifier B                       = AUTHORIZED
separate implementations                      = REQUIRED
separate runtimes                             = REQUIRED
separate toolchains and build steps           = REQUIRED
decision lane / audit lane separation         = REQUIRED
EP execution under frozen schema              = AUTHORIZED
status before EP                              = partial predicate / UNKNOWN
calibrated detector / complete search claim   = NOT AUTHORIZED before EP
new lane / TCB expansion / scope expansion    = NEW RECEIPT REQUIRED
```

pending queue は receipt に次のまま記録する。

```text
CR-11 implemented_checks layer        = PENDING / UNKNOWN
QD-6 bootstrap leaf lost guarantees   = PENDING / UNKNOWN
N-2(2) / H-1a″ independent rederive   = PENDING / UNKNOWN
```

---

## F9. ★教材

1. **三述語と passport は別 predicate である。**  
   前者は \(\alpha\ne0\)、後者を K3/K5 型に揃えると
   \(\alpha\in(\mathbf Z/n)^\times\) まで狭まる。

2. **class 語の射影と character 語の冪は同じ glyph で書かない。**  
   \([v]_{2n}\mapsto[v]_{2d}\) が character では \(n/d\) 乗に見える。

3. **「GT 軌道が一点」は class set 上の話である。**  
   \(\beta\) は動くので、個々の部分群を pointwise に固定するという意味ではない。

4. **isolated 性は conjectural gate に戻さない。**  
   既存 Thm 4.3 が全 \(K^{(n)}\) について閉じている。残件は有限段同型の
   naturality と幾何作用の忠実性である。

5. **odd radical も Galois 閉包では \(2\)-成分を持つ。**  
   共通交差が \(2\)-群であることと elementary abelian であることは別である。

6. **freeze の PASS は UNKNOWN を真にしない。**  
   schema と実行規律を固定するだけで、CR-11、QD-6、N-2 は pending のまま
   receipt に運ばれる。

---

## F10. 監査範囲外申告

### 本便で行ったこと

- `ops/inbox_codex/sol_task_75_math2.txt` を先頭から末尾まで読んだ。
- 対話帳は T-17 が最新で、新着がないことを確認した。
- `oddH_full_proof_v1.md`、`t63_reconnaissance_v1.md`、
  `hfun_functoriality_v1.md`、`ideas_002_expansion.md` を全文読解した。
- ODD-H / ODD-P、full-GT 作用、G3、T63-P1、I-6、I-8、I-10 を
  独立に紙上再構成した。
- freeze v18/v13/v13/v8 の full blob、前版差分、pin、branch contract、
  QD table、consumer matrix、TCB、S5 五 ID、registry block を監査した。
- SHA-256、byte hygiene、通常 / mutation lane、commander preflight を再実行した。

### 本便で行っていないこと

- \(u_9\)、sealed candidate、raw shard、旧 hit、blind coefficient の観測。
- GAP の新規探索、searcher/checker/verifier の実装。
- commander receipt、候補 receipt、dependency closure、build attestation、
  EP artifact の生成。
- git commit / push、CLAIMS 記帳、過去返信の修正。
- Lean 証明書の作成。

開始時から存在した対象外変更
`docs/mb_ninfty_verifier_contract_v6.md`、
`docs/week4-NInfty_stage2_spec_v11.md`、`out*.txt`
には触れていない。本便で加えた repository 変更は指定された
`sol/sol_reply_75_math2.md` だけである。
