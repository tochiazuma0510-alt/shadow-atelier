# Sol 第 12 便 — E2 線型化・予想 E15・不可解性証明書の監査

## 冒頭結論

| 論点 | 裁定 |
|---|---|
| 命題 E8 | **PASS**。\(A\) 可換なら同時 torsion 方程式は \(-E_m\in\mathcal N(\ker(1+\theta))\) という有限アーベル群上の像判定と厳密に同値。個数式も正しい。 |
| 定理 E9 | **PASS**。class \(\le3\) の自由対象で \(A^\sigma\otimes\mathbb Q\) が一次元になることから \(3E_m=-T_m\kappa_m\) が出て、\(f=w^{\lambda T_m}\) は (H-a)(H-b′) の明示同時解になる。 |
| 定理 E9′ | **証明骨格 PASS、中心恒等式は未相互監査**。恒等式 \(\mathcal N(w^{3T_m}(pq)^{-B_m})=E_m^{-9}\) が自由 class-4 Hall 基底上で成立すれば、\(\mathbb Z[1/3]\) 係数と全 2 群への帰結は正しい。しかし根拠の 21 点計算と次数上界を再査読できる script／座標表が作業ツリーに無く、現状は単系統 computer-assisted candidate。 |
| 命題 E10 | **補修付き PASS**。個々の torsion 解および生成 shadow は全射で降りる。全 \(m\)-full 性を商へ降ろすには、\((\mathbb Z/2k)^\times\to(\mathbb Z/2k')^\times\) の全射、すなわち charming residue の lift 補題を一行追加する。 |
| 命題 E12 | **PASS**。選択則は twisted orbit sum と Schur の補題から出る。さらに「同時に \(\sigma,\theta\)-安定な既約表現が自明表現だけ」なら交わりは必ず非空、という系 E12-a が係数の未閉鎖部を使わず直ちに出る。 |
| 予想 E15 | **有望だが、F-1 は有限 battery にすぎない**。160 件の直接代入は各固定合同系の肯定証拠として健全。しかし \(j\le5,m\le31\) から全指数・全 \(m\)・全 metabelian 2 群を結論できない。metabelian class \(\ge6\) は依然 UNKNOWN。 |
| \(H^1(C_3,-)\) 路線 | **それ単独では証明にならない**。\(3\) 可逆なら \(H^1(C_3,A)=0\) は既に H8／Schur–Zassenhaus が与える内容で、残る \(\theta\)-反不変条件は \(2\)-一次の障害である。正しい証明目標は \(-\lambda E_m\in\ker(1+\theta)+(1-\sigma)A\)。 |
| Burkhart | **直接適用の空虚性は PASS**。原文 p.2 の Theorem 1/2 は \(J=C_2\) なら Sylow \(2\)-部分群 \(=J\) の不動点を仮定し、同じ \(J\)-不動点を結論する。ただし、これを「全ての非 coprime/Glauberman 型道具が無力」へ一般化してはならない。 |
| 不可解性証明書 | **規律採用**。\(yM=0,\ yb\ne0\pmod{2^j}\) は sound であり、Smith 標準形から常に作れるので complete でもある。matrix/hash/modulus を含む独立再検査可能な形式へ固定する。 |
| 掃引 | **E15 の有限 battery を理由に中止・大幅除外しない**。最初に完全 class-5 非 metabelian、次に metabelian class-6 の記号的 SNF、最後に有限群掃引。既存宇宙は上書きせず新 universe ID で再登録する。 |

★ E15 の核心は「\(C_3\) の norm 方程式が解けるか」ではない。これは \(3\nmid|A|\) なら既に解ける。核心は、その解の affine \(C_3\)-torsor が \(\theta(f)=f^{-1}\) という \(C_2\)-反対称部分と交わるかである。従って低 class で分母 \(3\) しか現れなかったことは強い構造的手掛かりだが、**残り得る障害はむしろ \(2\)-一次**である。

---

## 1. E8/E9/E9′/E10/E12 の監査

### F1. 命題 E8 の線型化は完全

\(A\) を加法的に書く。\(A\) が可換なら

\[
\mathcal B_\theta
=\{f:\theta(f)=-f\}
=\ker(1+\theta)
\]

は部分群である。また \(\sigma^3=\operatorname{Inn}_A(E_m)=1\) なので

\[
\mathcal N=1+\sigma+\sigma^2
\]

は準同型であり、

\[
\mathcal S_m=\{f:\mathcal Nf=-E_m\}
\]

は空集合または \(\ker\mathcal N\) の剰余類になる。従って

\[
\boxed{\quad
\mathcal S_m\cap\mathcal B_\theta\ne\varnothing
\iff
-E_m\in\mathcal N(\ker(1+\theta)).
\quad}
\]

非空なら、二つの線型方程式の同次解空間は

\[
\ker(1+\theta)\cap\ker\mathcal N
\]

なので個数式も正しい。

\(3\nmid|A|\) の場合、\(\lambda=3^{-1}\bmod\exp A\) と

\[
e_\sigma:=\lambda\mathcal N
\]

を置くと、これは \(A^\sigma\) への冪等射影である。従って

\[
A=A^\sigma\oplus\ker\mathcal N,\qquad
\mathcal S_m=-\lambda E_m+\ker\mathcal N.
\]

ここで使っているのは体上の Maschke 定理そのものというより、有限 \(\mathbb Z[1/3]\)-加群上の averaging idempotent である。証明内容に問題はない。

同時解の障害は同値に

\[
\omega_m
:=
[-\lambda E_m]
\in
A\Big/\bigl(\ker(1+\theta)+\ker\mathcal N\bigr)
\]

であり、\(\omega_m=0\) が必要十分である。これは後の cohomology 評価に最も見通しのよい形である。

### F2. 補題 E8.0 の正しい量化子

2 生成群では

\[
\gamma_2=\langle w\rangle\gamma_3,\qquad w=[X,Y].
\]

\(\langle w\rangle\) は巡回なので、その自己 commutator は消え、

\[
[\gamma_2,\gamma_2]
\le[\gamma_2,\gamma_3]\,[\gamma_3,\gamma_3]
\le\gamma_5.
\]

従って class \(\le4\) なら \(A=[P,P]\) は可換である。また

\[
A\text{ 非可換}\Longrightarrow\operatorname{class}(P)\ge5
\]

も正しい。非可換 2 生成 \(2\)-群で class \(c\) なら

\[
|P/\gamma_2|\ge2^2,\qquad
|\gamma_i/\gamma_{i+1}|\ge2\quad(2\le i\le c),
\]

ゆえに \(|P|\ge2^{c+1}\)、特に class \(\ge5\) なら \(|P|\ge64\) である。

ただし逆

\[
\operatorname{class}(P)\ge5\Longrightarrow A\text{ 非可換}
\]

は偽であり、本文 §1.5 自身が metabelian class \(\ge5\) を認めている。従って C5 や【GAP】表の「\(A\) 非可換 \(\Longleftrightarrow\) class \(\ge5\)」は

\[
A\text{ 非可換}\Longrightarrow\text{class}\ge5,
\quad
\text{class}\ge5\text{ は可換/非可換の両枝}
\]

へ直す必要がある。

### F3. 定理 E9 は紙で閉じる

自由 class-3 の

\[
A_{\mathrm{free}}
=\gamma_2/\gamma_4
=\langle w,p,q\rangle\cong\mathbb Z^3
\]

で

\[
\sigma(w)=w-p+mq,\qquad
\sigma(p)=q,\qquad
\sigma(q)=-p-q
\]

と加法的に書ける。固定ベクトル

\[
\alpha w+\beta p+\gamma q
\]

に対する方程式は

\[
\beta=-\frac{\alpha(m+2)}3,\qquad
\gamma=\frac{\alpha(m-1)}3.
\]

従って \(A^\sigma\otimes\mathbb Q\) は一次元で、

\[
\kappa_m:=\mathcal N(w)
=3w-(m+2)p+(m-1)q
\]

がこれを張る。\(E_m\) も \(\sigma\)-固定であり、mod \(\gamma_3\) の \(w\)-成分が

\[
E_m\equiv -T_mw,\qquad \kappa_m\equiv3w,
\quad T_m=\frac{m(m+1)}2
\]

なので、自由格子の中で

\[
\boxed{\ 3E_m=-T_m\kappa_m\ }.
\]

この等式は任意の class \(\le3\) 商へ降りる。

\(\theta(w)=w^{-1}\) は自由群内の厳密な恒等式なので

\[
f=w^{\lambda T_m}
\]

は (H-a) を満たす。また

\[
\mathcal N(f)
=\lambda T_m\kappa_m
=-3\lambda E_m
=-E_m
\]

なので (H-b′) も満たす。従って E9 は **paper mutual-audit PASS の candidate** に上げてよい。

ただし、ここで証明したのは (H-a)(H-b′) の同時可解性、すなわち E2 の **torsion 部**である。marked generation

\[
\langle X^u,f^{-1}Y^uf\rangle=P
\]

は別判定であり、E9 だけから「生成 shadow が存在する」とは言わない。

### F4. 定理 E9′ は一つの恒等式に還元される

class \(\le4\) でも \(A=\gamma_2/\gamma_5\) は可換で、

\[
\theta(w)=w^{-1},\qquad
\theta(p)=q^{-1},\qquad
\theta(q)=p^{-1}
\]

が成立する。従って

\[
f=w^{\lambda T_m}(pq)^{-\lambda^2B_m},
\qquad
B_m=\frac{T_m(T_m+1)}2
\]

は確かに (H-a) を満たす。

残る核心は自由 class-4 格子 \(A_{\mathrm{free}}\cong\mathbb Z^6\) 上の

\[
\tag{\(\dagger\)}
\mathcal N\!\left(w^{3T_m}(pq)^{-B_m}\right)=E_m^{-9}.
\]

\((\dagger)\) が成立すれば、\(\mathcal N\) の線型性と

\[
9\lambda^2\equiv1,\qquad
3\lambda^2\equiv\lambda
\pmod{\exp A}
\]

から

\[
\mathcal N(f)=E_m^{-1}
\]

が直ちに従う。この modular scaling に穴はない。また \((\dagger)\) が整数自由格子で成立するため、分母が \(3,9\) だけの rational witness は全ての有限 \(2\)-群商で解釈できる。「係数が \(\mathbb Z[1/3]\) に載るなら全 \(2\)-primary exponent で解ける」という帰結も正しい。

しかし、\((\dagger)\) の証明として本文が提示するのは

1. 六つの Hall 座標が \(m\) の次数 \(\le8\) の多項式であるという主張、
2. \(m=0,\ldots,20\) の 21 点における node の厳密一致、

である。これは**次数上界と全座標表が提示されれば**正しい computer-assisted proof になる。現 checkout には列挙された `scratchpad/witness4.mjs` も座標出力も無く、Sol は中心恒等式を独立に再計算できない。

従って裁定は次の二段とする。

- E9′ の論理骨格と \(\mathbb Z[1/3]\) から全 \(2\)-群へ移す議論: **PASS**。
- \((\dagger)\) 自体: **single-system candidate / mutual audit 未了**。

少なくとも Hall 基底順、六座標の多項式、次数証明、21 点 residual、script hash を恒久化するまで「紙で閉じた」とは書かない。

### F5. Magnus 再現の状態札

truncated noncommutative power-series による Magnus 経路は、H6/H9 の元の群表とは数学的に独立な較正法であり、方法の選択は良い。とくに

\[
E_m=(1,wp,wq,1),\qquad
\mathcal S_m\cap\mathcal B_\theta
=
\begin{cases}
\{1,pq\},&m=0,3,\\
\{w,wpq\},&m=1,2
\end{cases}
\]

が H9 と一致するなら強い sanity check になる。

ただし検算 script と raw output が現作業ツリーにないため、今便で監査できたのは文書化された方法と報告値までである。これは既監査 H9 との**整合**であって、新たな cross-check や verified 証明書ではない。

### F6. 命題 E10 は二版に分けると明瞭

\(N\le N'\) から得る自然な全射

\[
\pi:P\twoheadrightarrow P'
\]

は \(X,Y,\theta,\tau,\sigma_m,E_m\) と可換し、

\[
\pi([P,P])=[P',P'].
\]

従って次の二主張はいずれも正しい。

1. **E10-T（torsion 降下）**: (H-a)(H-b′) の解は解へ写る。
2. **E10-S（shadow 降下）**: さらに元の解が
   \[
   \langle X^u,f^{-1}Y^uf\rangle=P
   \]
   を満たせば、その像は \(P'\) を生成する。

また \(k'=N'_{\rm ord}\mid k=N_{\rm ord}\) である。個々の \(m\) に関する本文の命題はこれで通る。

「細かい対象が全 charming \(m\) で full なら粗い対象も full」という全称版には lift を一行足す必要がある。任意の

\[
u'\in(\mathbb Z/2k')^\times
\]

は

\[
(\mathbb Z/2k)^\times\longrightarrow(\mathbb Z/2k')^\times
\]

の全射性により単元 \(u\) へ持ち上がる。実際、\(2k\) にのみ現れる各素数について \(u'+2k't\not\equiv0\pmod p\) となる \(t\) を Chinese remainder で選べばよい。\(u=2m+1\) に対応する charming \(m\) を E10 で降ろせば \(u'\) の層を得る。

重要なのは、E9/E9′/F-1 が直接与えるのは E10-T の入力だけだという点である。これらと E10 を組み合わせて「全商に生成 shadow がある」と結論するには、元の generation を別に示さなければならない。

### F7. E12 は通り、新しい系が出る

\(\mathcal S_m\) は \(\sigma\)-twisted conjugation

\[
a*f=\sigma(a)^{-1}fa
\]

で安定であり、\(\mathcal B_\theta\) は

\[
a*f=\theta(a)^{-1}fa
\]

で安定である。各 twisted orbit の群環和に \(\rho\) を作用させると、\(\rho\) と \(\rho\circ\sigma\)、または \(\rho\) と \(\rho\circ\theta\) の intertwiner への平均になる。Schur の補題から

\[
\rho(s_m)\ne0\Longrightarrow\rho\simeq\rho\circ\sigma,
\qquad
\rho(b_\theta)\ne0\Longrightarrow\rho\simeq\rho\circ\theta.
\]

本文の proof は \(\mathcal S_m\) を一 twisted orbit と書いているが、複数 orbit でも orbit ごとに同じ議論を足せばよい。2 群では \(3\nmid|A|\) と Schur–Zassenhaus により一 orbit になる。

Plancherel 式

\[
n_m^{\rm tor}
=
\frac1{|A|}
\sum_{\rho\in\operatorname{Irr}(A)}
d_\rho\,
\operatorname{Tr}\!\left(
\rho(s_m)\rho(b_\theta)^*
\right)
\]

と選択則は正しい。具体的な非自明項の intertwiner 正規化は【GAP-E12】のままである。

一方、P-新 B には直ちに答えが出る。

> **系 E12-a.** \(3\nmid|A|\) とし、\(\sigma,\theta\) の双方で安定な既約表現が自明表現だけなら
> \[
> n_m^{\rm tor}
> =
> \frac{|\mathcal S_m|\,|\mathcal B_\theta|}{|A|}
> >0.
> \]
> 従って E2 型障害は無い。

自明表現では \(\rho(s_m)=|\mathcal S_m|\)、\(\rho(b_\theta)=|\mathcal B_\theta|\) である。H8 により \(\mathcal S_m\ne\varnothing\)、また \(1\in\mathcal B_\theta\) なので右辺は正である。これは具体的係数の未閉鎖部を一切使わない。

---

## 2. 予想 E15 と F-1

### F8. F-1 の設計は良いが、結論の射程を縮める

事前登録した \((j,m)\) ごとに candidate vector \(v\) を構成し、

\[
Mv\equiv b\pmod{2^j}
\]

を直接代入する方法は、**肯定側の証明書として健全**である。求解器が不完全でも、residual が零である限りその固定合同系には解がある。node の偽陰性を GAP/SNF が発見した経緯も、探索器と照合器を分ける規律の成功例である。

しかし、F-1 が実際に試したのは

\[
j=1,\ldots,5,\qquad m=0,\ldots,31
\]

の 160 件だけである。従って直接言えるのは

> この基底・関係格子・matrix encoding が正しいという条件の下で、指定 160 合同系は全て可解

までである。次はまだ従わない。

- 全 \(j\) で可解、すなわち \(\mathbb Z_{(2)}\) 上の解がある。
- 全整数 \(m\) で可解。
- 全 metabelian class-5 \(2\)-群商が torsion-full。
- 全 metabelian \(2\)-群が torsion-full。

最初の二つには、symbolic Smith data、全 \(m\) の Hall polynomial identity、または分母が奇数の rational/2-adic closed solution が必要である。有限個の \(j,m\) の通過だけでは、より高い \(2\)-冪で初めて現れる divisibility obstruction を排除できない。また class-5 相対自由対象は class \(\ge6\) の metabelian 群を支配しない。

さらに raw matrix、160 witness、residual、GAP 側 SNF artifact が repository に無いため、今便では例示された \(j=4,m=1\) のベクトルさえ独立再計算できない。F-1 の**証明書設計**は PASS だが、数値の状態札は現状

\[
\text{reported 160/160 witness-checked candidate}
\]

である。工房の語彙では `verified` は Lean に予約されているため、本文の `160/160 verified` は訂正する。

監査中に §4 へ追加された回収警告は、欠陥ある `solve2adic.mjs` / `f1_metab5.mjs` を再利用せず、`f1_witness.g` の Smith 標準形と直接 witness 検査を正本にする、と明記した。この追記は妥当であり、肯定側の結論が defect に依存しないことを明瞭にする。ただし当該 `scratchpad` artifact 自体は checkout に無いため、上の状態札は変わらない。

従って E15 は「第一 falsification battery を生存した」と評するのが正確であり、「metabelian 2 群は全て m-full」「生きた層は導来長 \(\ge3\) だけ」とはまだ言えない。metabelian class \(\ge6\) は線型 route L が使える重要な UNKNOWN として残る。

### F9. \(H^1(C_3,-)\) は既に H8 であり、残りは \(C_2\)

\(3\) が \(A\) 上で可逆なら

\[
H^1(C_3,A)=0
\]

および Tate cohomology の消滅から

\[
\ker\mathcal N=(1-\sigma)A,\qquad
A=A^\sigma\oplus\ker\mathcal N
\]

が出る。非可換 \(A\) での pointed-set 版は、Schur–Zassenhaus による補群共役性、すなわち H8 の twisted orbit 記述に対応する。

従って \(H^1(C_3,-)=0\) は (H-b′) の affine 解集合を理解するが、その中に \(\theta(f)=-f\) を満たす点があることを保証しない。可換の場合の残余目標は

\[
\boxed{\quad
-\lambda E_m
\in
\ker(1+\theta)+(1-\sigma)A.
\quad}
\]

である。

抽象的には \(H^1(C_3,A)=0\) だけでは不十分である。例として加法群

\[
A=C_4,\qquad \sigma=1,\qquad\theta=1,\qquad E=1
\]

を取る。\(3\) は可逆で \(H^1(C_3,A)=0\) だが、

\[
\ker(1+\theta)=\ker(2)=\{0,2\},
\qquad
\mathcal N=3\,\mathrm{id},
\]

なので

\[
\mathcal N(\ker(1+\theta))=\{0,2\}
\]

は \(-E=3\) を含まない。これは E2 由来の \(E_m\) そのものを反例にするものではないが、「\(H^1(C_3,-)\) 消滅だけで一般可解」という推論を反証する。

\(\mathbb Z[1/3]\) 上では \(3\)-averaging はできるが \(2\) は可逆でなく、\((1-\theta)/2\) による sign projection は使えない。たとえ \(\sigma,\theta\) が厳密な \(S_3\)-作用を作っても、\(\mathbb Z[1/3][S_3]\) は \(2\)-primary 部分で semisimple ではない。実際の関係はさらに

\[
\theta\sigma\theta^{-1}
=\iota_{X^u}\sigma^{-1}
\]

という inner twist を含む。

従って P-新 E は**証明の芽ではあるが、主張を次の形へ絞るべき**である。

> braid 由来の特別な \(E_m\) の obstruction class
> \[
> \omega_m\in
> A/\bigl(\ker(1+\theta)+(1-\sigma)A\bigr)
> \]
> が lower-central weight ごとに零になることを示す、\(\theta\)-equivariant contracting homotopy を構成する。

class 3/4 の閉形は、この obstruction class が weight \(2,3,4\) で消えることを示す初期条件と読める。「障害の唯一の素数は 3」ではなく、

> class \(\le4\) の自由 Hall 座標では witness の分母に \(2\) が現れなかった

という観測へ弱めるのが正しい。

### F10. 次に反例を探す層

優先順位は次である。

1. **完全 class-5、非 metabelian**:
   \[
   F_2/\gamma_6,\qquad A=\gamma_2/\gamma_6
   \]
   の整合する有限 \(2\)-quotient。これは \(A\) が初めて非可換になり、E8 が使えない最小 weight である。E15 を敵対的に試す情報量が最大。
2. **metabelian class-6**: route L/SNF が使えるため安く、class-5 battery が偶然か、weight ごとの \(\mathbb Z[1/3]\) 再帰があるかを調べる最良の proof-seed。
3. **完全 class-6**: 上二つが通った後。ここで初めて class-5 の非可換 cancellation が次 weight でも持続するかを見る。

完全 class-5 では、単に \(\mathbb Z^{12}\) を mod \(2^j\) にするのではなく、Hall–Mal'cev の積と power relation が整合する有限群 quotient を作り、非可換な \(\mathcal S_m,\mathcal B_\theta\) を直接判定する必要がある。

E15 を safe filter に使うこと、または F-1 生存だけで 2 群宇宙を Q7 側へ移すことには反対する。

---

## 3. Burkhart 空虚性

### F11. Theorem 1/2 の直接適用は確かに循環する

`papers/delivered/2308.12286.pdf` の原頁 pp.1–3 を画像で照合した。p.2 の Theorem 1 は、有限アーベル群 \(N\) と有限群 \(J\) について、

> 各素数 \(p\) で \(J\) の Sylow \(p\)-部分群が \(\Omega\) の点を固定する

ことを仮定し、\(J\)-不変点の存在を結論する。Theorem 2 は \(N\) nilpotent、\(N\rtimes J\) supersoluble の場合に同じ Sylow 不動点仮定を用いる。

\(J=\langle\rho\rangle\cong C_2\) なら、\(p=2\) の Sylow 部分群は \(J\) 自身である。従って仮定は

\[
\exists\omega\in\Omega:\rho\omega=\omega
\]

であり、欲しい結論と同一である。他の素数の Sylow 部分群は自明なので情報を加えない。よって Burkhart Theorem 1/2 のこの直接適用は空虚、という観察 B1 は PASS である。

作用群を拡大しても、その Sylow \(2\)-部分群の不動点仮定は、その中の involution \(\rho\) の不動点を既に与えるので、元の E2 目標を安くしない。この意味でも同論文から直接の進展はない。

ただし結論は

> Burkhart Theorem 1/2 の Sylow-fixed-point criterion は E2 に循環的

までである。異なる仮定をもつ非 coprime fixed-point theorem、twisted cohomology、あるいは \(\rho\)-fixed point を仮定しない構造定理まで「原理的に無力」と総括してはならない。【GAP-E2b】も「Burkhart へ接続する目的では閉鎖」と書き、別用途の inner twist 吸収という数学問題まで refuted にしない。

---

## 4. 不可解性証明書

### F12. dual witness \(y\) は sound かつ complete

合同系

\[
Mx=b\pmod n,\qquad n=2^j
\]

に対し、行ベクトル \(y\) が

\[
yM=0,\qquad yb\ne0\pmod n
\]

を満たせば解は存在しない。実際、解 \(x\) があれば

\[
yb=yMx=0
\]

となり矛盾する。従って三行の独立 verifier で確認できる sound な否定証拠である。

さらにこれは complete でもある。整数 Smith 標準形

\[
UMV=D
\]

で \(c=Ub\) とする。対角成分 \(d_i\) に対し

\[
\gcd(d_i,n)\nmid c_i
\]

となる行が不可解性を検出する。\(g=\gcd(d_i,n)\) とし、変換後の左 witness の \(i\)-成分を \(n/g\)、他を零とすれば

\[
y'D=0,\qquad y'c\ne0\pmod n.
\]

\(y=y'U\) が元の系の dual witness になる。零行で \(c_i\ne0\) の場合も同様である。

従って route L の `intersection_size=0` には、solver の `null` ではなくこの \(y\) を必須とする規律を採用する。

### F13. schema は claim の射程まで固定する

最小の `unsolvability_certificate` は次を含むべきである。

- `claim: "torsion_intersection_empty"`。
- `method: "left_kernel_mod_prime_power/v1"`。
- modulus \(2^j\)、matrix shape、Hall/abelian basis の順序、relation/slack column の順序。
- canonical \(M,b\) またはその content hash と、独立 verifier が再構成する入力 hash。
- dual witness \(y\)。
- verifier は保存済み boolean を信用せず、\(yM=0\) と \(yb\ne0\) を再計算する。

肯定側は

\[
(1+\theta)f=0,\qquad \mathcal Nf=-E_m
\]

を直接代入した `solution_witness` で足りる。この証拠型の非対称性は正しい。

非可換 route T には linear dual witness がない。次のどちらかを用いる。

1. **完全全数証明書**: \(A\) の canonical element list/hash、各 \(f\) の二述語、交わり零を独立 checker が再計算する。
2. **orbit 証明書**: \(\mathcal S_m\) の twisted orbit representatives、stabilizer generators/order、orbit-size mass check、各 orbit と \(\mathcal B_\theta\) の disjointness を保存する。

さらに `m_missing` を「shadow 不在」の意味で使うなら、二理由を分ける。

- `torsion_empty`: 上記証明書。
- `all_generation_fail`: intersection の全候補を列挙し、各候補の
  \[
  \langle X^u,f^{-1}Y^uf\rangle<P
  \]
  を subgroup order または欠落生成元の certificate で示す。

W54 の `fake-cert/v1` は、各 lift の `no-shadow-certificate` hash を参照し、その上に

1. 粗い対象の**生成まで通った**具体的 shadow、
2. 全 lift の欠落、
3. H3 の仮定、
4. 完全 reduction 像、

を載せる。E9 は粗い対象の torsion witness を無料で与えるが、generation は無料ではない。`m_missing-cert` と `fake-cert` の分離は維持する。

---

## 5. 掃引の再設計

### F14. 既存宇宙を消さず、発射順を変える

E15 の帰趨を先に見る方針には賛成する。しかし F-1 は E15 を証明しておらず、metabelian class \(\ge6\) も残るため、現在の U-E2 から「metabelian 全部」または「2 群全部」を除外することには反対する。

既存 `U-E2-2026-07-26` は事前登録記録として凍結したまま残し、次を別 ID で登録する。

**U-E2-live-v2**

- \(k=4,8\)、\(|P|\le256\)、class \(\ge5\)。
- `A_abelian=true` の metabelian 枝と `A_abelian=false` の非 metabelian 枝を分離。
- metabelian class \(5\) も F-1 の射程外指数を除外せず残し、class \(\ge6\) は明示 UNKNOWN。
- control は CT-1–CT-4 と、固定した class-4 marked representatives。全 control を live discovery count に混ぜない。
- cap 超過は従来どおり UNKNOWN。

発射順は

1. E9′ の \((\dagger)\) artifact を恒久化して control theorem を確定。
2. 完全 class-5 非 metabelian の小さな一例を二 route で撃つ。
3. metabelian class-6 の symbolic SNF／分母を調べる。
4. その結果を封印予測として有限群 U-E2-live-v2 を発射。

とする。

### F15. 本丸 route T の第二照合器

`twistedconjugacy` と独立な最小照合器は、\(Q\) 側の factor-pair 全数である。各 \(m\) について

\[
g\in\bar\Delta A,\qquad g^2=1,\qquad(v_mg)^3=1
\]

を直接列挙する。これは \(A\) 側の

\[
\theta(f)=f^{-1},\qquad E_m\mathcal N_m(f)=1
\]

を twisted package で解く route T と、データ構造も述語も異なる。

比較欄は

- `torsion_count_A_route`。
- `torsion_count_Q_factor_route`。
- \(g=\bar\Delta f\) による明示対応の全数 hash。
- `routes_agree`。

とする。marked generation は W52 に従い別欄で

\[
\langle X^u,f^{-1}Y^uf\rangle=P
\]

を正本判定する。この direct \(Q\)-route は小群では package 非共有の独立 checker になり、否定時には完全列挙証明書も同時に与える。

---

## Errata（今便で記録）

1. `docs/week4-E2作戦_v1.md` C5 および【GAP】表の「\(A\) 非可換 \(\Longleftrightarrow\) class \(\ge5\)」は誤り。正しくは \(A\) 非可換 \(\Rightarrow\) class \(\ge5\)。metabelian class \(\ge5\) がある。
2. F-1 の 160 件から「metabelian 2 群は全て m-full」「狩場は導来長 \(\ge3\) のみ」は出ない。直接の射程は \(j\le5,m\le31\) の合同系であり、metabelian class \(\ge6\) は未処理。
3. `160/160 verified` は状態語違反。Lean 証明書が無いため `160/160 witness-checked candidate` とする。
4. E9/E9′/F-1 が自動的に与えるのは torsion 同時解であり、generation ではない。§3.6 の粗い \(K\) の shadow は generation を別に検査する。
5. E10 の全 \(m\)-full 降下には charming residue の全射的 lift 補題を追加する。
6. E9′ は \((\dagger)\) の script／座標 certificate が無い現状では「紙上相互監査 PASS」ではなく single-system computer-assisted candidate。
7. 「障害の唯一の素数は 3」は、「class \(\le4\) の明示 witness の分母には 3 しか現れない」という観測へ弱める。

過去の reply・裁定・正本文書は編集していない。訂正は全て現在便に記録した。

---

## 監査範囲外の申告

- Sol の役割規律に従い、GAP、node、Python、Lean は実行していない。
- Burkhart は `papers/delivered/2308.12286.pdf` の pp.1–3 をページ画像で確認した。論文全体の全補題・証明を精読したとは主張しない。
- `scratchpad/class3.mjs`、`class4.mjs`、`witness4.mjs`、F-1 の matrix/witness artifact は作業ツリーに存在せず、raw output の再監査はできなかった。
- E9′ の中心恒等式 \((\dagger)\)、F-1 の 160 residual、例示 witness の数値代入は再実行していない。
- 予想 E15 の一般証明も反例も今便では得ていない。cohomology 節は、必要な obstruction の同定と「\(H^1(C_3)\) だけでは不足」の裁定までである。
- SmallGroups/LINS の掃引、class-5/6 の有限 quotient 構成、fake certificate の実地生成は範囲外。
- composition/reduction の完全像と \(\operatorname{Ih}_N\) の算術像は UNKNOWN。
- verified は Lean に予約する。今便の紙上 PASS は candidate、既存独立実装の一致がある場合だけ cross-checked とする。
- 契約どおり、今便で変更するのは `sol/sol_reply_12_e2.md` だけである。

---

## 考察と提案

P133【E8/E9/E10/E12 の登録】E8、E9、E10-T/E10-S、E12 を今便の限定と補修つきで paper mutual-audit PASS / candidate として CLAIMS に登録する。E9′ は分離する。

W97【torsion と generation】`torsion-full`、`generation_pass_count>0`、`shadow exists` を同義にしない。E9/E9′ の明示 \(f\) は generation を別検査する。

P134【系 E12-a】同時 \(\sigma,\theta\)-安定既約表現が自明表現だけなら
\[
n_m^{\rm tor}=|\mathcal S_m||\mathcal B_\theta|/|A|>0
\]
を新しい安価な safe criterion として登録する。

W98【E9′ の中心 certificate】自由 class-4 Hall 基底、六座標多項式、次数上界、21 点 residual、script hash が揃うまで \((\dagger)\) を相互監査済みとしない。

P135【正しい cohomology 目標】\(H^1(C_3,A)=0\) ではなく
\[
-\lambda E_m\in\ker(1+\theta)+(1-\sigma)A
\]
を lower-central filtration 上で消す \(\theta\)-equivariant contracting homotopy を証明目標にする。

W99【\(H^1\) trap】\(H^1(C_3,-)\) の消滅は H8 の再表現であり、同時 \(\theta\)-条件を含まない。「障害の唯一の素数は 3」と結論しない。

P136【F-1 証明書化】160 件の \(M,b,v\)、basis/relation order、modulus、residual、GAP SNF、input hash を versioned certificate に保存し、`witness-checked` と記録する。

W100【有限 battery の量化子】\(j\le5,m\le31\) の通過から全 \(j\)、全 \(m\)、全 metabelian class-5/6 群へ一般化しない。`verified` も用いない。

P137【不可解性 certificate v1】route L の否定には \(yM=0,\ yb\ne0\) の dual witness、route T の否定には完全列挙または orbit-mass/disjointness certificate を必須にする。

W101【solver null 禁止】`fail`、`null`、rank 不一致だけから `intersection_size=0` または `m_missing` を出力しない。

P138【独立 Q-route】本丸の第二判定器を \(Q\) 内の \(g^2=1,(v_mg)^3=1\) 全数として実装し、twistedconjugacy route と count・明示対応を照合する。

W102【fake 昇格】各 lift の `no-shadow-certificate`、粗い側の generation 済み shadow、H3 仮定、完全 reduction 像が揃うまで `fake_witness` と呼ばない。

P139【次弾 1】最優先は完全 class-5 非 metabelian の整合有限 quotient。E8 が初めて使えない層で E15 を敵対的に試す。

P140【次弾 2】次に metabelian class-6 を symbolic SNF／2-local denominator で調べ、class-5 battery を一般化する再帰の有無を見る。

W103【2 群撤退禁止】E15 の定理または反例が出る前に U-E2 から 2 群を除外しない。既存宇宙を上書きせず、新 ID で発射順だけ変える。

P141【Burkhart 記帳】「Theorem 1/2 の \(J=C_2\) 直接適用は仮定が結論と同じ」と CLAIMS に限定記帳し、この文献ルートへの追加投資を止める。

W104【固定点道具の過剰撤去】Burkhart の一定理が循環することから、全ての non-coprime fixed-point/cohomology 手法や inner-twist 吸収問題まで refuted としない。
