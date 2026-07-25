# 便 09 回答 — Opus 相互監査・語規約ゲート・PSL 封印計算

## 冒頭結論

### (a)(b) の判定

| 対象 | 判定 | 要点 |
|---|---|---|
| \(v_m=\bar\sigma _1^{\,2m+1}\) | **合格** | \(c\in N\) の全許容対象で成立する。ただし「非 charming は \(v_m=1\) となる唯一の \(m\)」という後段の一般化は偽。 |
| \(48=8\cdot3\cdot2\) と \(24\) との差 | **合格・紙上の生成穴も対象別に閉じる** | 共通商 \(C_2^2\) 上の subdirect subgroup に、これより大きい共通商がないことを示せる。差は \(N_Q\) 側の per-\(m\) 数 \(1\) と \(N_3\) 側の \(2\) だけ。 |
| 補題 D | **合格** | Goursat の正しい使用である。\(Q_8\times_{C_2^2}Q_8\) では導来群が対角 \(C_2\) となり、互いに素条件の必要な位置が見える。 |
| 【GAP-E2a】完全群の場合 | **結論は修正付き合格** | split-inner の窓では \(n_m\) は \(P\) の scalar Frobenius 公式に落ちる。ただし \(z_{2,C}\) は \(Q=P\times S_3\) の既約表現上で一般に scalar ではない。また「\(P\) 完全」だけでは仮定不足。 |
| 語規約案 v1 | **現版は併合不可・局所修正後に合格** | W-1/W-2/W-3、補題 W1 の等式、A5-CONV 主判定は正しい。一方、\(\iota\) は実は \(F_2\) の自己同型であり、「値が対合なら盲点」も一般には偽。 |

### (c) 封印予測

ここで \(n_m^{\rm all}\) は scalar 類積公式が数える全分解数、\(n_m^{\rm gen}\) はそのうち生成条件を通る数である。次表は Opus の命題 S が扱う **split-inner marking** の封印値であり、採用された四型では両者が一致する。

| \(G\) | split-inner 許容 marking（Aut\((G)\)-軌道） | charming \(m\) | 各 \(m\) の \((n_m^{\rm all},n_m^{\rm gen})\) | shadow 集合の予測総数 | 命題 S の数値予測 |
|---|---|---|---|---:|---|
| \(\mathrm{PSL}(2,7)\) | \(k=7\)、**1 軌道** | \(\{0,1,2,4,5,6\}\) | \((7,7)\) | **42** | \(42=\varphi(7)7\)、成立 |
| \(\mathrm{PSL}(2,8)\) | \(k=7\)、**1 軌道** | \(\{0,1,2,4,5,6\}\) | \((7,7)\) | **42** | \(42=\varphi(7)7\)、成立 |
| \(\mathrm{PSL}(2,8)\) | \(k=9\)、**1 軌道**（\(3\mid k\)） | \(\{0,2,3,5,6,8\}\) | \((9,9)\) | **54** | \(54=\varphi(9)9\)、成立 |
| \(\mathrm{PSL}(2,11)\) | \(k=11\)、**1 軌道** | \(\{0,1,2,3,4,6,7,8,9,10\}\) | \((11,11)\) | **110** | \(110=\varphi(11)11\)、成立 |

split-inner の範囲では、\(\mathrm{PSL}(2,7)\) と \(\mathrm{PSL}(2,11)\) に \(3\mid k\) の marking はなく、\(\mathrm{PSL}(2,8)\) では \(k=9\) がその唯一の型である。

一般の許容 marking についてはさらに外部作用を分ける必要がある。外部類は \(S_3\to\operatorname{Out}(G)\) を与える。\(\operatorname{Out}(L_2(8))=C_3\) へのそのような準同型は自明なので \(L_2(8)\) の上表は完全である。一方 \(\operatorname{Out}(L_2(7))=\operatorname{Out}(L_2(11))=C_2\) には sign 写像があり、\(\theta\) が outer となる marking を ordinary \(G\)-character table だけでは排除・計数できない。この **outer-sign 部分の存在・分類・\(n_m\) は UNKNOWN** とする。以上は shadow の個数予測であり、さらに **settled/isolated、合成の閉鎖、群同型 \(\mathrm{AGL}(1,k)\) もすべて UNKNOWN** である。

---

## (a) Opus 答案の監査

### F1【合格】\(v_m=\bar\sigma _1^{\,2m+1}\) は一般恒等式

\(u=2m+1\) とする。定義と \(\tau=\operatorname{Ad}(\bar\delta)\) から

\[
\begin{aligned}
v_m
 &=\bar\delta^{-1}\bar Y^m\bar\Delta^{-1}\\
 &=\bigl(\bar\delta^{-1}\bar Y^m\bar\delta\bigr)
   \bigl(\bar\delta^{-1}\bar\Delta^{-1}\bigr)\\
 &=\bar X^m\bar\sigma _1
  =(\bar\sigma _1^2)^m\bar\sigma _1
  =\bar\sigma _1^{\,2m+1}.
\end{aligned}
\]

第三等号では \(\tau^{-1}(Y)=X\)、\(c\in N\) から \(\bar\Delta^{-1}=\bar\Delta\)、および
\(\bar\delta^{-1}\bar\Delta=\bar\sigma _1\) を使った。標準 \(S_3\) 商で \(\bar\sigma _1\) は転置へ写るためその位数は偶数であり、\(\operatorname{ord}(\bar\sigma _1^2)=k\) と合わせて
\(\operatorname{ord}(\bar\sigma _1)=2k\) である。charming なら \(u\) は奇数かつ \(\gcd(u,k)=1\) なので
\(\gcd(u,2k)=1\)。従って \(v_m\) は \(\langle\bar\sigma _1\rangle\) の生成元となる。ここまで Opus の証明は正しい。

### F2【要訂正】補題 2 から先の二つの一般化

補題 2 自体とは別に、次は一般には成り立たない。

1. 「非 charming は \(v_m=1\) に潰れる唯一の \(m\)」は \(k=5\) の特殊事情である。例えば \(k=9\) では \(u\equiv3,0,6\pmod9\) の三層が非 charming で、対応する \(v_m\) の位数は \(3,1,3\) となる。
2. 【GAP-20c】の「\(k\) が合成数なら charming な \(w^u\) の位数が \(k\) の真の約数になり得る」も逆である。charming なら \(\gcd(u,2k)=1\) なので、\(\operatorname{ord}(w^u)=\operatorname{ord}(w)\) は保たれる。今回の \(k=9\) がその較正点になる。

正しい一般形は単に

\[
m\text{ charming}\iff v_m\text{ が }\langle\bar\sigma _1\rangle\text{ の生成元}
\]

である。

### F3【合格・穴を閉鎖】\(48=8\cdot3\cdot2\)

\[
R:=PB_3/M_3=G_3\times_{C_2^2}P_3
\]

では、補題 D により

\[
R' =G_3'\times P_3',\qquad |G_3'|=27,\quad |P_3'|=8.
\]

従って \(f=(f_G,f_P)\) は独立に動き、二本の hexagon も二射影で成分別に判定できる。既監査の Thm. 4.3 と H9 を使うと、各 \(m\in\mathcal X_{M_3}\) について

\[
n_{K^{(3)}}=3,\qquad n_{N_3}=2,\qquad
|\mathcal X_{M_3}|=8,
\]

したがって関係式通過数は \(8\cdot3\cdot2=48\) である。

Opus が【GAP-48a】に残した生成性も、この対象では紙で閉じる。成分ごとに全射な候補が生成する部分群を \(H\le R\) とする。もし \(H\ne R\) なら Goursat により、\(G_3\) と \(P_3\) に \(C_2^2\) より真に大きい共通商 \(E\) が生じる。一方 \(P_3\) は 2 群なので \(E\) は 2 群であり、\(G_3'\) の像は位数が 3 冪かつ 2 冪だから自明である。従って

\[
E\text{ は }G_3/G_3'\cong C_2^2\text{ の商},\qquad |E|\le4.
\]

また \(H\subseteq R\) から、元の共通商 \(C_2^2\) は \(E\) の商になるので \(|E|\ge4\)。ゆえに \(E=C_2^2\)、従って \(H=R\) である。

★ これは「二射影が全射なら任意の fiber product でも自動的に全射」という一般論ではない。ここでは **\(G_3\) と \(P_3\) に、糊 \(C_2^2\) より大きい共通商がない**ことが決定的である。命題 C′ の一般形にはこの subdirect-rigidity を仮定として追加すべきである。

### F4【合格】\(M_Q=24\) との差は一本だけ

\(M_Q=K^{(3)}\cap N_Q\) に同じ議論を適用すると

\[
|\mathcal X_{M_Q}|=8,\qquad n_{K^{(3)}}=3,\qquad n_{N_Q}=1,
\]

ゆえに

\[
|GT(M_Q)|=8\cdot3\cdot1=24,\qquad
|GT(M_3)|=8\cdot3\cdot2=48.
\]

\(m\) 層の個数と \(K^{(3)}\) 成分は同じで、差は \(Q_8\) 側の per-\(m\) 解数 \(1\) が \(P_3\) 側で \(2\) になったことだけである。\(M_Q\) についても \(Q_8\) が 2 群なので F3 の共通商論法がそのまま生成性を閉じる。

### F5【合格】補題 D と H7′ 反例

\(R=G\times_D P\)、\(D\) 可換とする。すると

\[
G'\times P'\le R,\qquad R'\le G'\times P'.
\]

射影 \(R\to G,P\) は全射なので \(R'\to G',P'\) も全射であり、\(R'\) は \(G'\times P'\) の subdirect subgroup である。Goursat により、その欠損は \(G'\) と \(P'\) の共通商で測られる。\(\gcd(|G'|,|P'|)=1\) なら非自明な共通商はないため

\[
R'=G'\times P'.
\]

\(Q_8\times_{C_2^2}Q_8\) では、各 \(Q_8'\) は \(C_2=\{\pm1\}\) である。fiber product の二成分は同じアーベル化座標を持つため、二つの交換子の符号も常に一致し、

\[
\bigl(Q_8\times_{C_2^2}Q_8\bigr)'
 =\langle(-1,-1)\rangle\cong C_2
 \subsetneq C_2\times C_2.
\]

すなわち反例はまさに両導来群が共通商 \(C_2\) を持つ場所にあり、補題 D の互いに素条件がこれを排除している。

### F6【修正付き合格】完全群窓の scalar 化

補題 3 の最初の部分、すなわち split-inner の仮定下で

\[
f\longleftrightarrow g=sf,\qquad
r=w^ug
\]

により

\[
n_m
=\#\{(r,g)\in T_3(P)\times T_2(P):rg=w^u\}
\]

となることは正しい。従って

\[
n_m=\frac1{|P|}\sum_{\chi\in\operatorname{Irr}(P)}
\frac{S_2^P(\chi)S_3^P(\chi)}{\chi(1)}
\overline{\chi(w^u)}
\]

という \(P\) の scalar 指標表公式も正しい。

ただし Opus の「\(z_{2,C}\) が既約表現上で scalar になる」という説明は正しくない。\(Q=P\times S_3\)、\(C=P\times\{\sigma\}\) なら

\[
z_{2,C}=z_2(P)\otimes\sigma.
\]

\(\chi\otimes\psi\in\operatorname{Irr}(Q)\) に対し

\[
\rho_{\chi\otimes\psi}(z_{2,C})
=\frac{S_2^P(\chi)}{\chi(1)}I_\chi\otimes\rho_\psi(\sigma),
\]

であり、\(S_3\) の 2 次元既約表現では \(\rho_\psi(\sigma)\) は scalar でない。正しい閉じ方は、F13 の trace を \(P\) 因子と \(S_3\) 因子に分け、後者が「指定された \(\rho^{-1}\) 一個」を数えて \(1\) になることを先に和で消す方法、または上の \(f\leftrightarrow(r,g)\) の直接全単射である。

また仮定は「\(P\) 完全」だけでは足りない。少なくとも Opus 補題 1 の

\[
Z(P)=1,\quad \theta=\operatorname{Ad}(s),\quad
\tau=\operatorname{Ad}(t),\quad s^2=t^3=1
\]

が必要である。従って【GAP-E2a】は

> **有限単純群を含む split-inner・centerless・perfect の窓では閉鎖**

と記帳するのが正確である。中心を持つ完全群、または \(\theta,\tau\) が外部自己同型である完全群、および \(A\subsetneq P\) の一般対象は依然 UNKNOWN である。

---

## (b) 語規約案の併合ゲート

### F7【合格・文言修正】W-1/W-2/W-3

数学的対応

\[
\text{paper }AB\longleftrightarrow\text{GAP }B*A
\]

と、GAP で左から token を読んで `image * elt` と prepend する W-2、証明書を paper 順に保存する W-3 は正しい。これは既監査の `paper rs ↔ GAP s*r` と一致する。

ただし「\(A\) を掛けてから \(B\)」は作用順と誤読できるので削るべきである。正本には

\[
(AB)\cdot i=A\cdot(B\cdot i),\qquad
i^{\,B*A}=(i^B)^A
\]

を直接書けば曖昧さがない。

### F8【等式は合格・説明は訂正】補題 W1

\[
\operatorname{ev}^{\rm bad}(w)
=\operatorname{ev}(w^{\rm rev})
=\operatorname{ev}(\iota(w))^{-1}
\]

は正しい。しかし

\[
\iota(x)=x^{-1},\qquad \iota(y)=y^{-1}
\]

は「準同型ではない」のではなく、自由群 \(F_2\) の involutive automorphism である。混同してはいけないのは、\(\iota(w)\) と群の逆元 \(w^{-1}\) が別物だという点である。

この誤記は補題 W1 の三行証明を壊さないが、§3(d) の論拠には使えない。正しい注意は「\(\iota\) が商 \(P\) に降りるには \(N_{F_2}\) の \(\iota\)-不変性が必要で、一般には保証されない」である。

### F9【二点要修正】盲点三種

- (a) \(P\) 可換、(b) 単一生成元の語は正しい。
- (c) の正確な必要十分条件
  \[
  \operatorname{ev}(\iota w)=\operatorname{ev}(w)^{-1}
  \]
  も正しいが、「値が対合」はそれだけでは十分でない。例えば
  \(X=(12),Y=(123)\in S_3\) では、paper 語 \(xy\) と逆順 \(yx\) はそれぞれ異なる対合 \((23),(13)\) になる。
- (d) の結論「\([P,P]\) 可換だけでは安全と言えない」は正しい。ただし理由は F8 のとおり差し替える。class 2 の交換子語について bad 評価が逆元になる計算自体は正しい。

従って「盲点三種」は、(c) の対合例を削り、(d) の \(\iota\) の説明を直せば通る。

### F10【主判定は合格】A5-CONV

与えられた

\[
X=(1\,3\,2\,4\,5),\qquad Y=(1\,3\,4\,5\,2)
\]

について paper 左作用で直接追うと

\[
YX^{-1}=(1\,2\,4),\qquad X^{-1}Y=(2\,5\,3).
\]

従って `paper y x^-1 ↔ GAP X^-1 * Y` という主適合テストは正しく、逆規約も正しく識別する。

一方、補助判定の「20/20 対 4/20」は草案自身が認めるとおり単一 node 系の数値である。適合 fixture として残してよいが、GAP 側の独立再現までは cross-checked と書かない。

以上から、**語規約 v1 はそのままでは定義ノートへ併合しない**。F7 の作用式明記、F8 の「\(\iota\) は自己同型」への訂正、F9(c) の対合例削除という三つの局所修正後は併合可である。

---

## (c) PSL 三群の独立紙計算

### F11【分類法】split-inner triangle pair と marking

\[
r:=t^{-1},\qquad g:=s,\qquad w:=rg=t^{-1}s
\]

と置く。固定した \(w\) に対する

\[
N_G(w):=\#\{(r,g):r^3=g^2=1,\ rg=w\}
\]

が scalar Frobenius 公式で得る数である。非自明な高位数 \(w\) では \(r,g\) も非自明である。さらに \(\langle r,g\rangle=G\) なら

\[
X=w^2,\qquad Y=tXt^{-1},\qquad k=\operatorname{ord}(X)
\]

は命題 S の許容対称 marking を与える。実際

\[
X=(rg)^2,\qquad Y=(gr)^2,\qquad
(XY)^{-1}=r^2grgr^2
\]

であり、\(\operatorname{Ad}(g)\) は \(X,Y\) を交換し、
\(\operatorname{Ad}(r^{-1})\) は \(X,Y,(XY)^{-1}\) を巡回する。従って
\(\langle X,Y\rangle\) は \(\langle r,g\rangle=G\) の正規部分群であり、\(G\) の単純性から \(G\) 全体である。逆に \(X,Y\) が生成し \(Z(G)=1\) なら、これらの内部自己同型を実現する \(g,r^{-1}\) は一意なので、以下の triangle pair の Aut 軌道数は **split-inner marking** の Aut 軌道数でもある。

生成 pair の同時共役安定化群は \(Z(G)=1\) なので、固定共役類 \(C\) に属する生成 pair の \(G\)-軌道数は

\[
\frac{|C|\,N_G^{\rm gen}(C)}{|G|}.
\]

今回この値は採用する全クラスで \(1\) となり、外部自己同型が同位数のクラスを推移的に入れ替えるので、各 \(k\) につき Aut\((G)\)-軌道は一つである。

候補となる \(\ell=\operatorname{ord}(w)\) を全て見ると次のようになる。なお \(\ell=1,2\) は \(X=w^2=1\) となるので表から除いた。

| \(G\) | 不採用の \(\ell\) | 理由 | 採用 |
|---|---|---|---|
| \(L_2(7)\) | \(3,4\) | \(\Delta(2,3,3)=A_4\)、\(\Delta(2,3,4)=S_4\) | \(\ell=k=7\) |
| \(L_2(8)\) | \(3\) | \(A_4\) の商にしかならない | \(\ell=k=7,9\) |
| \(L_2(11)\) | \(3,5,6\) | \(A_4,A_5\)、および可解な Euclidean \(\Delta(2,3,6)\) の商 | \(\ell=k=11\) |

\(\ell=4\) なら \(k=2\)、\(\ell=6\) なら \(k=3\) であることも含め、これで三群の split-inner 型に関係する全 element order を覆う。従ってその範囲で \(3\mid k\) として採用されるのは \(L_2(8),k=9\) だけである。outer-sign 型は \(r,g\in G\) のこの表には現れない。

### F12【指標表の出所と紙上和】

入力した ordinary character table は、インストール済み GAP **CTblLib 1.3.11** の生データを読み取ったもので、GAP は実行していない。

- \(L_2(7)=L_3(2)\): `ctoline4.tbl` の table ID `L3(2)`。同ファイルは出所を *ATLAS of Finite Groups*、補助出所を McKay と記す。
- \(L_2(8)\): `ctoline1.tbl` の ID `L2(8)`。出所は ATLAS compound table。
- \(L_2(11)\): 同ファイルの ID `L2(11)`。出所は *ATLAS of Finite Groups*。

同じレコードにある centralizer orders から class size を取り、最大部分群欄も分類に用いた。各既約指標について

\[
a_\chi:=\frac{S_2(\chi)S_3(\chi)}{\chi(1)}
\]

を紙で計算すると、次数順の \(a_\chi\) は

| \(G\) | 既約次数（同次数は表の行順） | \(a_\chi\) |
|---|---|---|
| \(L_2(7)\) | \(1,3,3,6,7,8\) | \(1254,-18,-18,48,-126,-48\) |
| \(L_2(8)\) | \(1,7,7,7,7,8,9,9,9\) | \(3648,840,-504,-504,-504,-48,72,72,72\) |
| \(L_2(11)\) | \(1,5,5,10,10,11,12,12\) | \(6216,-1260,-1260,-1200,1440,396,12,12\) |

これを

\[
N_G(w)=\frac1{|G|}\sum_\chi a_\chi\overline{\chi(w)}
\]

へ代入した。以下の数値はこの有限和の手計算である。

この ordinary \(G\)-table が直接数えるのは \(r,g,w\in G\) の split-inner 型だけである。outer-sign 型では指定 outer coset の involution 和が必要になり、F6 のとおり同じ scalar 和を流用できない。

### F13【封印値】\(\mathrm{PSL}(2,7)\)

class sizes は \(7A,7B\) とも \(24\)。二つの 3 次元指標の 7-class 値の和が \(-1\) なので

\[
N_{L_2(7)}(7A)=N_{L_2(7)}(7B)
=\frac{1254+18-48-48}{168}=7.
\]

最大部分群は \(S_4,S_4,7{:}3\)。前二者は 7 元を持たず、後者は奇数位数で対合を持たないから、七つ全てが \(G\) を生成する。各 7-class について

\[
\frac{24\cdot7}{168}=1
\]

個の \(G\)-共役軌道があり、外部自己同型が \(7A,7B\) を交換するので Aut\((G)\)-軌道は一つ。

\(w\in7A\) と正規化した per-\(m\) 表は

| \(m\) | \(u=2m+1\bmod7\) | \(w^u\) | \(n_m^{\rm all}=n_m^{\rm gen}\) |
|---:|---:|---|---:|
| 0 | 1 | \(7A\) | 7 |
| 1 | 3 | \(7B\) | 7 |
| 2 | 5 | \(7B\) | 7 |
| 4 | 2 | \(7A\) | 7 |
| 5 | 4 | \(7A\) | 7 |
| 6 | 6 | \(7B\) | 7 |

従って予測総数は \(6\cdot7=42\)。

### F14【封印値】\(\mathrm{PSL}(2,8)\)

7-classes は三つ、各 size \(72\)。9-classes も三つ、各 size \(56\)。指標表の三つの円分周期の和を取ると、7-class では

\[
N_{L_2(8)}(7*)=\frac{3648-48-72}{504}=7,
\]

9-class では

\[
N_{L_2(8)}(9*)=\frac{3648+840+48}{504}=9.
\]

最大部分群は \(2^3{:}7,D_{18},D_{14}\) である。7 元を含む二つの型は 3 元または必要な対合を欠くので、7 型の全分解が生成する。9 元を含む最大部分群は \(D_{18}\) だけだが、その位数 3 元は rotation、対合は reflection であり、その積は reflection だから order 9 にはならない。従って 9 型も全分解が生成する。

各 class の軌道数は

\[
\frac{72\cdot7}{504}=1,\qquad
\frac{56\cdot9}{504}=1.
\]

field automorphism \(C_3\) が各三クラスを巡回するので、\(k=7\) と \(k=9\) にそれぞれ Aut\((G)\)-軌道が一つある。

\(w\in7A\) および \(w\in9A\) と正規化すると

| \(k\) | \(m:u\) と \(w^u\) の class | 各 \(n_m^{\rm all}=n_m^{\rm gen}\) | 総数 |
|---:|---|---:|---:|
| 7 | \(0:1:A,\ 1:3:C,\ 2:5:B,\ 4:2:B,\ 5:4:C,\ 6:6:A\) | 7 | 42 |
| 9 | \(0:1:A,\ 2:5:C,\ 3:7:B,\ 5:2:B,\ 6:4:C,\ 8:8:A\) | 9 | 54 |

\(k=9\) では charming 条件が \(u\equiv0,3,6\pmod9\) をちょうど除くため、残る全ての \(w^u\) は order 9 のままである。

### F15【封印値】\(\mathrm{PSL}(2,11)\)

\(11A,11B\) は各 size \(60\)。二つの 5 次元指標の 11-class 値の和が \(-1\)、二つの 12 次元指標の和が \(2\) なので

\[
N_{L_2(11)}(11A)=N_{L_2(11)}(11B)
=\frac{6216+1260+1200-1440+24}{660}=11.
\]

最大部分群は \(A_5,A_5,11{:}5,S_3\times C_2\)。11 元を含む \(11{:}5\) は奇数位数、他は 11 元を持たないので、十一個全てが生成する。各 11-class は

\[
\frac{60\cdot11}{660}=1
\]

個の \(G\)-共役軌道を与え、外部自己同型が二クラスを交換するため Aut\((G)\)-軌道は一つ。

\(w\in11A\) を平方剰余側に正規化すると

| \(m\) | \(u=2m+1\bmod11\) | \(w^u\) | \(n_m^{\rm all}=n_m^{\rm gen}\) |
|---:|---:|---|---:|
| 0 | 1 | \(11A\) | 11 |
| 1 | 3 | \(11A\) | 11 |
| 2 | 5 | \(11A\) | 11 |
| 3 | 7 | \(11B\) | 11 |
| 4 | 9 | \(11A\) | 11 |
| 6 | 2 | \(11B\) | 11 |
| 7 | 4 | \(11A\) | 11 |
| 8 | 6 | \(11B\) | 11 |
| 9 | 8 | \(11B\) | 11 |
| 10 | 10 | \(11B\) | 11 |

従って総数は \(10\cdot11=110\)。

比較のため order 5 の scalar 類積係数は

\[
N_{L_2(11)}(5*)=10>5
\]

である。しかし \(\Delta(2,3,5)=A_5\) なので十個は全て二クラスの \(A_5\) 最大部分群内にあり、生成通過数は 0 である。これは「scalar 数が \(k\) より大きければ命題 S が破れる」と即断してはいけず、**先に marking の生成性を通す必要がある**ことの最小 control になる。

### F16【封印の解釈】命題 S は四つの split-inner 較正点で生存

採用された四つの split-inner marking では全 charming \(m\) に

\[
n_m^{\rm all}=n_m^{\rm gen}=k
\]

が成立し、従って cardinality 予測

\[
|\mathrm{GT}(N)|=\varphi(k)\,k
\]

は四点すべてで生き残る。とくに \(k=9\) により「素数 \(k\) だけの偶然」ではないところまで進んだ。

しかし、ここから一般定理、\(\mathrm{GT}(N)\cong\mathrm{AGL}(1,k)\)、または算術実現性を推論してはならない。今回決めたのは character table と最大部分群分類を入力にした **split-inner shadow 集合の紙上予測**までであり、outer-sign marking、settled witness、合成表は未計算である。

★ もう一つの重要点は、\(L_2(11)\) の order-5 類で raw coefficient \(10>5\) が現れながら、生成フィルタで全て消えることである。命題 S を壊す候補は「大きい類積係数」ではなく、**大きい類積係数を持つ admissible generating marking**でなければならない。

---

## ★ 教材

1. \(v_m=\bar\sigma _1^u\) は、charming 層を一つの巡回部分群の primitive powers に変える。ただし非 charming 層の形は \(k\) の素因数分解に依存する。
2. fiber product の二射影全射だけでは全体生成にならない。今回の 48 を閉じたのは「糊より大きい共通商がない」という追加事実である。
3. direct product で変数分離できることと、非中心群環元が各既約表現で scalar になることは別主張である。
4. 語の指数反転 \(x\mapsto x^{-1},y\mapsto y^{-1}\) は自由群自己同型である。商へ降りるかどうかが本当の盲点である。
5. character coefficient は関係式解の数であり、marking の存在には生成フィルタが別途要る。\(L_2(11)\) の order-5 値 \(10\) がその教材である。

---

## 監査範囲外の申告

- Sol の役割規律に従い、GAP、node、Python、Lean は実行していない。CTblLib の ordinary table 生データと power map、最大部分群欄を読み、有限和は紙で計算した。
- ATLAS 印刷版または原著 PDF のページ画像は今回供与されていないため、character table 入力を第二の原典で再照合していない。従って Opus からは独立だが、将来 GAP が CTblLib を使う場合は **データ源まで独立した二系統**にはならない。
- PSL marking の明示行列 \(s,t\) は構成していない。正の類積係数、最大部分群分類、軌道数から存在と Aut 軌道を紙上で決めた。実装証明書では明示行列を出すべきである。
- PSL 四対象の settled/isolated、composition table、reduction、算術像は監査範囲外であり UNKNOWN。
- `docs/week3-20の正体_opus_v1.md` 以外の Opus 封印答案は見ていない。外部検索も行っていない。
- 今便に Lean verified の新主張はない。

---

## 考察と提案

P110【語規約 v2】F7–F9 の三修正、すなわち作用式の明記、\(\iota\) を \(F_2\) の自己同型へ訂正、対合だけでは盲点にならない旨を反映した v2 を作り、その差分だけ再ゲートに掛ける。v1 の本体併合は保留する。

W75【語規約の正本】「先に掛ける」という時間語を正本に置かず、paper と GAP の作用式を並べて定義する。

P111【E2a 訂正】補題 3 の scalar 化証明を、\(z_2(P)\otimes\sigma\) の tensor trace と \(S_3\) 係数 1 の計算で書き換える。CLAIMS の閉鎖範囲は split-inner・centerless・perfect に限定する。

W76【完全群の量化子】\(P=[P,P]\) だけから \(Q=P\times S_3\) や termwise scalar 性を推論しない。

P112【GAP-48a の対象別閉鎖】F3 の「最大共通商 \(=C_2^2\)」補題を \(M_Q,M_3\) の紙上証明へ追記する。命題 C′ の一般版には `no_larger_common_quotient` または同値な subdirect-rigidity 仮定を加える。

W77【subdirect trap】fiber product への二射影が全射でも、その部分群が全 fiber product とは限らない。

P113【PSL nonce 封印】F13–F15 の class label、\(m:u\)、\(n_m^{\rm all}\)、\(n_m^{\rm gen}\)、総数 \(42/42/54/110\) をこの版の封印値として固定し、Opus 答案との突合前に変更しない。

W78【raw と生成】`class_coefficient` と `generation_pass_count` を別欄にする。\(L_2(11)\) の order-5 control は \(10\to0\) を必ず保存する。

P114【実装証明書】各 PSL marking について明示 \(s,t,w,X,Y\)、exact order、\(\langle X,Y\rangle=G\)、Aut 軌道、power-class map、per-\(m\) staged counts、settled witness を出す。探索前に四総数を manifest へ固定する。

W79【class label】\(7A/7B/7C\)、\(9A/9B/9C\)、\(11A/11B\) は CTblLib の正規化であり、外部自己同型で入れ替わる。ラベル自体を marking の不変量にしない。

P115【独立データ源】実装後の二系統化では、GAP/CTblLib の同じ table を再読するだけでなく、ATLAS 印刷表または明示 \(2\times2\) 行列からの直接列挙を相方にする。追加の巨大探索器は不要。

W80【合成数 \(k\)】charming なら \(\gcd(u,2k)=1\) であり、合成数でも \(w^u\) の exact order は落ちない。

P116【次の反証点】命題 S の次候補は、raw coefficient \(>k\) かつ生成条件も通る marking に限定する。単に類積係数が大きい非生成 triangle pair は候補から除く。

W81【状態】PSL の数値は標準 character table に基づく独立紙計算であり、現時点では candidate。GAP/node の一致で初めて cross-checked、Lean 証明書で初めて verified と呼ぶ。

P117【outer-sign 残件】\(L_2(7),L_2(11)\) について、sign action を持つ
\(\operatorname{Aut}(G)\times_{C_2}S_3\) 型の拡大を別宇宙として事前登録し、outer involution coset の類積係数と marking 軌道を計算する。split-inner の四封印値とは混ぜない。

W82【分類の射程】「\(G\) 完全だから ordinary \(G\)-character table で全 marking を分類できる」と記帳しない。今便で完全なのは \(L_2(8)\) と、三群の split-inner 部分である。
