# 総合判定: **条件付き PASS — 主定理の構想は修理後に昇格可、現行 v1 のままの昇格は不可**

`B_{\rm FC}` の四段分解と、剛性 descent・局所 Kummer・torsor 比較を合成する主線は成立する。ただし現稿には、定理文をそのままでは真にしない必須修理が四群ある。

1. 命題 B-2 の三者同値は偽である。
2. 定理 B-3 から (W3)、定理 B-4 から (W2) が脱落している。
3. 系 B-4c で左作用と左右剰余類が混線している。
4. §4 の依存表は B-5b が使う (TB4) などを落としている。

これらは主定理 B-7 の仮定欄には既に含まれているもの、または剰余類記法の局所修理であり、**B-7 の結論を失わせる反例ではない**。したがって、下記 R1–R6 を反映した次版なら

> **`paper-proof (framework-conditional on TB1–TB4) / two-mathematician audit PASS`**

へ上げてよい。より正確には、(TB1)–(TB4) を前件として採用した紙上証明が PASS であり、**厳密な \(b=1\) の向きを文献で裏取る未閉鎖点が (TB4)** である。現行 v1 自体には `two-mathematician PASS` を付けない。

本便では個別モデル探索を行っていない。

---

## F1. 対象・再現

対象 digest は次のとおり。

| artifact | SHA-256 |
|---|---|
| `docs/week4-BFC攻略_opus_v1.md` | `659a9570118df503b5cd88b03562954cb6fac1ece9150c2908c8327915c36100` |
| `search/week4-bfc-antecedents.mjs` | `97621fdb488e92fd4b13e5a7ce7d1665e239dc08ebee4b441b7736973d4ec7d7` |

次を再走し、**13/13 PASS** を得た。

```text
node search/week4-bfc-antecedents.mjs
```

ソースも通読した。有限群・部分群・生成元像・自己同型性を同じ Node 系で悉皆しており、V1–V8 の表示値と実装は対応している。ただし当工房の序列では、これはなお **single-system candidate** であり、別 helper の GAP/第二照合器との一致なしに `cross-checked` とは呼ばない。

---

## F2. 命題 B-2 と定理 B-3

### F2.1 命題 B-2 — **現文 FAIL、結合形は PASS**

\(\langle X\rangle\) が \(P/H\) 上推移的で \(\operatorname{ord}(X)=M\) なら、常に言えるのは

\[
 |\Lambda|=[P:N_P(H)]\le [P:H]\le M
\]

だけである。したがって

\[
 |\Lambda|=M
 \Longrightarrow [P:H]=M\ \text{かつ}\ N_P(H)=H
\]

は正しいが、現稿 (B-2) の

\[
 |\Lambda|=M\iff[P:H]=M\iff N_P(H)=H
\]

という**三つの pairwise 同値は偽**である。

反例は

\[
 P=S_3\times C_2,\qquad
 H=\langle(12)\rangle\times C_2,\qquad
 X=((123),c)
\]

（\(c\) は \(C_2\) の生成元）でよい。\(\operatorname{ord}(X)=6\)、\(\langle X\rangle\) は指数 3 の \(P/H\) 上推移的で、\(N_P(H)=H\) だが

\[
 [P:H]=|\Lambda|=3\ne 6=M .
\]

正しい修理形は

\[
\boxed{
 |\Lambda|=M
 \iff
 \bigl([P:H]=M\ \text{かつ}\ N_P(H)=H\bigr).
}
\tag{B2-corr}
\]

さらに

\[
P/H\longrightarrow\Lambda,\qquad gH\longmapsto gHg^{-1}
\]

が全単射であることは、\(M\) とは無関係に \(N_P(H)=H\) と同値である。従って **(W4) の下では**

\[
\boxed{(W3)\iff |\Lambda|=M}
\]

となる。便 43 が副産物として掲げる「(W3) \(\Longleftrightarrow\) (W4)+\(|\Lambda|=M\)」は、この**結合形**としてなら PASS である。

V3 が実際に調べているのも

```text
X transitive かつ |Lambda| = 6 なら N_P(H) = H
```

という結合形であり、誤った pairwise 同値を検査してはいない。付録 B の B-2 と §13.2 の「同値」も (B2-corr) に合わせて直すこと。

### F2.2 定理 B-3 — **(W3) を足せば PASS**

B-3 の第 1–3 段、すなわち

\[
\gamma\in G_K
\overset{\mathrm{(W2)}}{\Longrightarrow}
\mathrm{Ih}_N(\gamma)\in\mathfrak F_0
\]

と、\(\Phi(\mathfrak F_0)\) が \(X\)-共役作用と可換する部分は正しい。

しかし第 4 段で \(\tau(\mu_M)\) を \(\Lambda\) 上 regular とするには、(W4) だけでなく **(W3)** が必要である。例えば

\[
P=C_M\times C_2,\qquad H=C_2,\qquad X=(\text{\(C_M\) の生成元},1)
\]

では (W4) を満たすが \(H\triangleleft P\)、従って \(\Lambda\) は一点で \(\tau\) は忠実でも regular でもない。

従って B-3 の正しい前件は

\[
\boxed{\text{(W1)(W2)(W3)(W4)(W5)}}
\]

である。この下では B-1 の自己中心化論法がそのまま働き、

\[
\rho_\Lambda(\mathrm{Ih}_N(G_K))\subseteq\tau(\mu_M)
\]

および一意な \(c:G_K\to\mu_M\) は正しく出る。「型は無料」は、正確には**regular detector (W3)(W4) を既に払った後は追加の幾何入力が不要**という意味で PASS である。

主定理 B-7 は (W3) を既に仮定しているので、この修理による主結論の変更はない。

---

## F3. §6 の剛性 descent

### F3.1 cocycle の積順序 — **PASS**

\(F=\widehat F_2\)、左作用

\[
\alpha_{\gamma\delta}=\alpha_\gamma\circ\alpha_\delta
\]

および

\[
(g,\gamma)(g',\delta)
=
\bigl(g\,\alpha_\gamma(g'),\gamma\delta\bigr)
\]

の半直積規約で独立に計算した。

\[
C_\gamma
=
\{c\in F:c^{-1}\widetilde Hc=\alpha_\gamma(\widetilde H)\}
\]

とする。\(c,c'\in C_\gamma\) なら \(c'c^{-1}\in N_F(\widetilde H)=\widetilde H\) なので

\[
C_\gamma=\widetilde Hc_\gamma
\]

は一意な左剰余類である。また

\[
\begin{aligned}
&(c_\gamma\alpha_\gamma(c_\delta))^{-1}
\widetilde H
(c_\gamma\alpha_\gamma(c_\delta))\\
&\quad=
\alpha_\gamma(c_\delta)^{-1}
\alpha_\gamma(\widetilde H)
\alpha_\gamma(c_\delta)\\
&\quad=
\alpha_\gamma(c_\delta^{-1}\widetilde Hc_\delta)
=\alpha_{\gamma\delta}(\widetilde H),
\end{aligned}
\]

ゆえに

\[
c_\gamma\alpha_\gamma(c_\delta)\in
C_{\gamma\delta}
=\widetilde Hc_{\gamma\delta}.
\]

ここに積順序・逆元位置の反転はない。さらに

\[
\mathcal H
=
\{(hc_\gamma,\gamma):h\in\widetilde H,\ \gamma\in G_K\}
\]

について

\[
c_\gamma\alpha_\gamma(\widetilde H)c_\gamma^{-1}
=\widetilde H
\]

だから積は再び \(\mathcal H\) に入る。連続性も、有限集合
\(\widetilde\Lambda\) と一意な剰余類の対応を経由するのでよい。閉じた非空部分半群が compact 群内で逆元を含むという標準補題を使う最終行も正しい。紙面では、読み手の負担を避けるためこの補題を一行明記するか、半直積の逆元を直接代入するとよい。

従って自己申告 A-1 は閉じる。

### F3.2 脱落前件 — **(W2) を追加せよ**

B-4b は

\[
\gamma\in G_K
\Longrightarrow
\mathrm{Ih}_N(\gamma)\in\mathfrak F_0
\]

を B-3 の第 1 段から使っている。この含意は (W2) である。従って定理 B-4 の \(K\)-descent 版には

\[
\boxed{\text{(W1)(W2)(W3)(W5) + (CAL)}}
\]

が必要である。

\((W5^{\mathbb Q})\) を用いる \(\mathbb Q\)-descent 版では、全 \(\mathrm{GT}(N)\) の安定性を直接使うため同じ形の (W2) は不要である。この二つを定理文で分けると依存が明瞭になる。

主定理 B-7 は (W2) を既に含むので、ここも主結論は生き残る。

### F3.3 一意性の射程

構成した部分群は、幾何 stabilizer を文字通り \(\widetilde H\) と固定した pointed 記述では一意である。非標識被覆へ戻すと、別の幾何同定は \(F\)-共役を生むが、

\[
\operatorname{Aut}_U(W)
\cong N_F(\widetilde H)/\widetilde H
=1
\]

なので \(K\)-モデルは一意な同型を除いて一意になる。この一文を「部分群の一意性」から「被覆の一意性」へ渡す箇所に補うことを推奨する。

### F3.4 (W3) を外す一般化への回答

\[
A:=N_P(H)/H
\]

が非自明なら \(C_\gamma/\widetilde H\) は一点でなく \(A\)-torsor となり、積のずれが \(A\) 値の 2-cocycle になる。また

\[
P/H\longrightarrow\Lambda
\]

は \(|A|:1\) である。\(A\) が可換でも、存在障害は一般に

\[
H^2(G_K,A)
\]

に残る。\(H^1(G_K,A)\) は**障害が消えて一つ descent が存在した後の捻りの分類**であり、「\(A\) 可換なら \(H^1\) だけで済む」わけではない。

自己同型をもつ窓への拡張として価値はあるが、別の gerbe/descent 定理と別 schema にすべきで、現定理から (W3) を外してはならない。

---

## F4. 系 B-4c の左右剰余類 — **必須修理**

(TB4) が採る「\(\Omega\) への後合成」は左作用である。従って stabilizer \(\mathcal H\) をもつ推移的 \(\pi_1\)-集合は

\[
\boxed{\pi_1(U_K,\vec{01})/\mathcal H}
\]

であり、幾何部分への制限は

\[
\boxed{F/\widetilde H}
\]

である。

現稿 6.3 の

\[
\mathcal H\backslash\pi_1,\qquad
\widetilde H\backslash F\cong F/\widetilde H
\]

は、非正規部分群について左右剰余類を無根拠に同一視しており、そのままでは誤りである。実際、直後の

\[
\operatorname{Stab}(g\widetilde H)
=g\widetilde Hg^{-1}
\]

は左剰余類 \(F/\widetilde H\) の公式である。

全編を左作用・左剰余類

\[
g\cdot(f\widetilde H)=gf\widetilde H
\]

へ統一すれば、

\[
p\longmapsto\operatorname{Stab}_F(p)
\]

は \(F\)-同変かつ \(G_K\)-同変となり、

\[
x\ \longleftrightarrow\
\bigl(H'\mapsto XH'X^{-1}\bigr)=\tau(\zeta_M)
\]

も所望の向きで成立する。この修理後、FC-3 を帰結に降ろす主張は PASS である。

これは単なる組版ではなく、§8 の \(b=1\) の向きを支える箇所なので必須修理とする。

---

## F5. §7 の局所 Kummer

### F5.1 完備化・Eisenstein — **PASS**

B-5a の半局所整閉包の完備化と積分解は標準的で正しい。B-5b と (W4) から \(\lambda^{-1}(0)\) は唯一の幾何点 \(P_0\)、分岐指数 \(M\) となる。標数 0 なので剰余拡大は分離的であり、幾何点が一つなら \(\kappa(P_0)=K\) である。

\(K\)-有理 uniformizer \(s\) に対して

\[
\lambda=u\,s^M(1+O(s)),\qquad u\in K^\times
\]

と書く。\(s'=as(1+O(s))\) なら \(u'=ua^{-M}\) なので \([u]_M\) は不変である。

\[
h=u^{-1}\lambda s^{-M}\in K[[s]],\qquad h(0)=1
\]

は、\(\operatorname{char}K=0\) より定数項 1 の一意な \(M\) 乗根をもつ。従って

\[
\widetilde s=s\,h^{1/M},\qquad
\widetilde s^M=u^{-1}\beta.
\]

\(T^M-u^{-1}\beta\) は DVR \(K[[\beta]]\) 上 Eisenstein であり、

\[
K((s))
\cong
K((\beta))[T]/(T^M-u^{-1}\beta)
\]

が出る。係数作用が \(\beta^{1/M}\) を固定し、\(\mu_M\subset K\) であることから

\[
\gamma\cdot p
=m(\kappa_{u^{-1}}(\gamma))p
\]

となる。従って torsor 類が \([u^{-1}]\) であるという II-c は PASS。

### F5.2 依存表の修理

B-5b は「\(x\) が \(0\)-慣性で、局所 Galois 群が後合成で作用する」を使うので、§4 の II-c 欄にある

```text
(TB1)(TB2)+(W4)
```

だけでは足りない。少なくとも **(TB3)(TB4)** を加えること。また \(W_0\) の存在まで同じ欄で主張するなら B-4 の窓前件と (CAL) も間接依存である。「\(W_0\) が既に与えられた局所補題」と「窓から \(W_0\) を構成する主定理」の依存を分けるのがよい。

同様に II-b は B-4c と B-5 を呼ぶため、全体依存表では (W1)(W2)(W5) と (TB2) を省かないこと。B-7 の総前件には全部入っている。

---

## F6. §8 の torsor 比較と \(b=1\)

### F6.1 (TB4) を仮定した紙上計算 — **PASS**

F4 の左作用修理後、(TB4) が文字どおり

\[
x\longmapsto\sigma_\zeta,\qquad
\sigma_\zeta(\beta^{1/M})=\zeta_M\beta^{1/M}
\]

を与えるなら、(7.1) の任意の点について

\[
x\cdot p=m(\zeta_M)p.
\]

一方、stabilizer 同型の \(F\)-同変性から

\[
c_\Lambda(x\cdot p)
=\tau(\zeta_M)c_\Lambda(p).
\]

従って

\[
c_\Lambda m(\zeta_M)c_\Lambda^{-1}
=\tau(\zeta_M),
\]

生成元で一致するので全 \(\xi\in\mu_M\) について (8.1) が成立する。半直積の向きによる追加の逆数は現れない。自己申告 A-2 は、**(TB4) をこの向きで採用する限り**閉じる。

### F6.2 \(b=1\) の状態札

\(b=1\) は「規約から独立な裸の定理」ではなく、

> **(TB2) の根系・係数分裂と、(TB4) の \(x=\sigma_\zeta\)・後合成規約を同時に固定した枠組みに相対的な定理**

である。(TB4) はまさに結論の向きを含んでいる。原典照合で \(x^{-1}\)、前合成、右作用などが採られていれば、単位 \(b\) が出る。

従って「\(b_i\ne1\) は必ず TB2 違反」という診断は狭すぎる。正しくは

```text
TB2/TB4/左右作用/共役規約の transport 不一致
```

の検出器である。実装で \(b_i\) を必ず記録する Rule 1 はそのまま維持する。

### F6.3 \(b\)-頑健性 — **PASS**

\(b\in(\mathbb Z/M)^\times\) なら \(\xi\mapsto\xi^b\) は \(\mu_M\) の自己同型なので、

\[
|\operatorname{im}\kappa^b|
=|\operatorname{im}\kappa|,\qquad
\ker\kappa^b=\ker\kappa,
\]

かつ各 characteristic subgroup \(\mu_M[e]\) を保つ。従って B-8 の単一窓の全射判定・固定体不変性は正しい。

ただし二 dessin 比較では \(b_{\rm sq},b_{\rm ns}\) の相対差が \(a_{\rm eff}\) に残る。従って

\[
b_{\rm sq}=b_{\rm ns}
\]

を要求する Rule 1 §7.3 は撤回不可である。厳密な (TB4) が文献関所で閉じる前でも、単一窓版は「ある単位 \(b\) を伴う twisted bridge」として先に定理化できる。

---

## F7. 主定理 B-7 の裁定

主定理 B-7 は (W1)–(W5) をすべて仮定しているため、F2・F3 の脱落前件は主定理内では既に支払われている。F4 の剰余類を直すと、合成は

\[
\begin{aligned}
\rho_\Lambda(\mathrm{Ih}_N(\gamma))
&=c_\Lambda\,
(\gamma\text{-action on Fib})\,
c_\Lambda^{-1}\\
&=c_\Lambda
m(\kappa_{u^{-1}}(\gamma))
c_\Lambda^{-1}\\
&=\tau(\kappa_{u^{-1}}(\gamma))
\end{aligned}
\]

となり正しい。

よって B-7 の数学的状態は次のとおり。

| 層 | 裁定 |
|---|---|
| B-3 型の段 | (W3) を定理文へ戻せば PASS |
| B-4 剛性 descent | (W2) を定理文へ戻せば PASS |
| B-5 局所 Kummer | PASS（依存表修理） |
| B-6 exact \(b=1\) | (TB4) の向きに条件つき PASS |
| B-7 合成 | F2–F6 の修理後 PASS |

なお §12.1 の「(TB4) だけが load-bearing」は、**exact \(b=1\) の向きについて唯一 load-bearing**という意味なら正しい。一方、(TB1) の圏同値や (TB3) の慣性生成元同定も論理上は B-4/B-5 の土台であり、真に破れれば「記法だけ」では済まない。状態札は

```text
TB1–TB4 = global framework assumptions
TB4 = unique orientation-sensitive literature gate for exact b=1
```

と書くのが安全である。

---

## F8. 副産物 (W5)、432/1296、K3 (P7)

### F8.1 432/1296 — **source-audited candidate として PASS**

checker は生成元像候補を悉皆し、各候補について準同型性と全単射性を確認して

\[
|\operatorname{Aut}(G_3)|=1296
\]

を得る。その全自己同型について、選んだ 6 個の \(G_3\)-共役部分群集合 \(\Lambda\) の setwise stabilizer を数えて

\[
|\operatorname{Stab}_{\operatorname{Aut}(G_3)}(\Lambda)|=432
\]

を得る。さらに

\[
\Phi(\mathfrak F_0)\ (3\text{ 元}),\qquad
\Phi(\mathrm{GT}(K^{(3)}))\ (12\text{ 元})
\]

はいずれもこの 432 元内に入る。ソース上、1296 や 432 を期待値として assert するだけの循環ではなく、列挙から得た値を末尾で照合している。

ただし **(W5) 自体が 432/1296 という意味ではない**。(W5) は 3 元または 12 元の指定された像が 432 元の stabilizer に含まれるという包含条件である。432/1296 は、その条件が自明でないことを示す周囲の有限群データである。

### F8.2 K3 (P7) 第二証明 — **射程限定つき PASS**

V6 は、定理 K3 v3 で 【GAP-K3d】だった

\[
\Phi(\mathrm{GT}(K^{(3)}))\ \text{が標的の個々の }G_3
\text{-共役類を保つ}
\]

を埋める。これと (W3)、較正、剛性 descent を合わせれば、標的の**抽象的な非標識被覆**が \(\mathbb Q\) 上へ一意に下降することを、明示曲線なしに再導出できる。従って (P7) の field-of-moduli/descent 部分には第二証明が付く。

ただし、これは「有限群論だけ」の証明ではなく、有限事実 V6 に B-4 の descent 枠組みを合成した証明である。また次は置換しない。

- 手元の明示曲線がその抽象被覆であるというモデル認識、
- ordered passport と actual marking、
- exact conjugator (P4)/(R-2)、
- そのモデル上の \(u\) の抽出。

従って「P7 全部を明示モデル非依存に置換」ではなく、

> **P7 の非標識 \(\mathbb Q\)-descent 部分に独立な抽象証明を追加**

と記録するのが正確である。数値 432/1296 と V6 の機械状態は、第二系統が付くまでは candidate のままとする。

---

## F9. 五札と \(K^{(5)}\) 運用の再構成

橋を一般定理として採用した後は、窓ごとの `BRIDGE-FAIL` を通常の数学的分岐として残す必要はない。ただし現稿 §13.3 の分類には二つの過剰推論がある。

1. **(W5) 不成立 \(\not\Rightarrow\) \(K\)-モデルなし。**  
   (W5) は \(\Phi(\mathfrak F_0)\) 全体の安定性という、実際の
   \(\Phi(\mathrm{Ih}_N(G_K))\)-安定性より強い有限の十分条件である。
   \(\mathfrak F_0\) に実 Galois 像へ来ない元があれば、(W5) が破れても
   \(K\)-モデルは存在しうる。不成立時に言えるのは「この有限 schema では
   定理を適用できない」までである。
2. **証明書を取れない \(\not\Rightarrow\) MODEL-MISMATCH。**  
   探索不成功は `MODEL-UNKNOWN`。exact triple/conjugator が別の標的を示した
   ときだけ `MODEL-MISMATCH` である。

推奨する版管理つき札は次である。

| 層 | IN | OUT / UNKNOWN / conflict |
|---|---|---|
| **GLOBAL-FRAMEWORK** | (TB1)–(TB4)+(CAL) を固定 | 原典未閉鎖は `FRAMEWORK-UNKNOWN`。TB4 は exact orientation gate |
| **WINDOW-SCHEMA** | (W1)–(W5)、\(R^{\rm cyc}\) ならさらに (2)(F) | いずれか不成立は `SCHEMA-OUT`。存在しないとは断言しない |
| **MODEL** | (R-1)(R-2) exact 証明書 | 未取得は `MODEL-UNKNOWN`、反対証明書は `MODEL-MISMATCH` |
| **EXTRACTION** | 同一 sealed model から \(u\) 二経路一致 | 不一致は `EXTRACTION-CONFLICT` |
| **BRIDGE** | 一般定理として封印外 | 全前件を満たして等式が破れれば `THEOREM/RECORD-CONSISTENCY-FAIL` |
| **ARITHMETIC** | \(\operatorname{ord}([u^{-1}]_{10})\) | ここが窓固有の算術結果 |

従って `BRIDGE-FAIL` は数学的ケースとしては空にしてよいが、実運用では削除せず

```text
legacy BRIDGE-FAIL
  -> THEOREM/CONVENTION/RECORD-CONSISTENCY-FAIL
```

へ版管理つきで改名するのがよい。TB4 が閉じる前の exact bridge は
`FRAMEWORK-UNKNOWN`、単位 twist までで足りる単一窓版は別札にする。

\(K^{(5)}\) が実際に測るものは、修理後には次の四束である。

1. (W1)–(W5)（および (2)(F)）の有限 scope 検査、
2. (R-1)(R-2) によるモデル認識、
3. sealed model からの \(u\) 二経路一致、
4. \(\operatorname{ord}([u^{-1}]_{10})=5\)。

1–3 は入口・同一性・完全性の検査であり、**真の算術予測は 4** である。二 dessin 比較では、これに \(b_{\rm sq},b_{\rm ns}\) と \(a_{\rm eff}\) の convention seal を残す。

---

## F10. 必須修理リストと最終昇格条件

次版で最低限、以下を反映すること。

1. **R1**: B-2 を (B2-corr) に置換し、付録 B・§13.2・V3 の説明も結合形へ統一する。
2. **R2**: B-3 と §4 の段表へ (W3) を追加する。
3. **R3**: B-4/B-4b の \(K\)-版へ (W2) を追加する。\(\mathbb Q\)-版との差を明記する。
4. **R4**: B-4c を \(\pi_1/\mathcal H\)、\(F/\widetilde H\) の左作用へ統一し、§8 まで同じ規約で通す。
5. **R5**: B-5/B-6 の依存表へ (TB3)(TB4) と間接依存を戻す。「与えられた \(W_0\)」版と「窓から構成」版を分ける。
6. **R6**: §13.3 で (W5) failure と K-model 非存在を同一視せず、`MODEL-UNKNOWN` と `MODEL-MISMATCH` を分ける。\(b\ne1\) の診断先を TB2 単独から TB2/TB4/transport 規約へ広げる。

R1–R6 の差分検収後は、

- **TB4 を除いた紙上本体**: PASS、
- **TB4 を前件として採用した exact \(b=1\) と B-7**: PASS、
- **文献番号まで含む無条件の枠組み裏取り**: TB4 関所待ち、
- **Lean 状態**: 未着手であり `verified` ではない、
- **V6/V7 数値**: source-audited single-system candidate、

と裁定する。

以上より、**現行 v1 は修理差戻し、定理候補そのものは条件付き PASS**。R1–R6 を反映した版には `paper-proof (framework-conditional) / two-mathematician audit PASS` を付与してよい。
