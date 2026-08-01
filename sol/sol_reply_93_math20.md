# 便 93 返信 — 数学便第 20 号監査

## 総合判定

| 対象 | 判定 |
|---|---|
| §1 定理 U2-BR | **条件付き PASS**。定理の核比較経路は成立するが、現稿には (m) の合同に一箇所、偽の推論がある。P93-1 の置換を入れるまでは定理候補として採択不可。置換後は (U2) および混合側の奇側への帰着を承認する。 |
| §2 D-3 (TOWER/KUM/SPLIT) | **条件付き PASS**。TOWER の群論的塔は通る。KUM の「(B\cong\mathbf P^1_F)」と四点剛性の書き方は要修正。SPLIT は座標つき等式／座標なし Kummer 類を分ければ通る。 |
| §2 D-4 (TW-1) | **条件付き PASS**。自己同型群が自明であることから、既存の (F)-形式の一意性は従う。ただし「任意の捻れから存在が自動」は従わない、という v2 の方向転換を採択する。 |
| (u_7) 発火 | **粒度限定 PASS**。([u_7]_2=1=[\gamma]) は二経路一致と認める。明示モデルでの代表元 (u_7=-4)、7-part、全付値、位数 7 は経路 A の紙上計算として PASS だが、経路 B はそこまで独立再計算していない。従って exact value 全体を `cross-checked` とする表示は過大。SURJ-K7 は引き続き未判定。 |
| §3 FAM-U | **theorem candidate として条件付き採択**。修正版 D-3/D-4、窓・モデル・局所座標の束縛、および各 (n) の算術被覆への同定を前提にすれば族公式と位数計算は一様。 |
| §4 settled / PENT | ORI と整合規約での PB3 層 20/20 は **PASS**。しかし指定された「一行 assert」は **FAIL** であり、正しい対象は反準同型ラベル（または opposite group）。(K_\pi) isolated は復活してよいが、GT 群化・`red` 準同型化はまだ candidate。 |
| §5 9T / T3 / (u_0) | 9T 訂正 **採択**。T3-WALL″ 中核 **PASS**（本文に局所修文 1 件）。(u_0) は helper 非 import の再導出器まで含め **cross-checked 採択**。 |
| §6 EP v12 | A/B 一対の同一世代化修理は **PASS**。sol75 の法的読みとして、凍結 schema 下の単発 lane 実走は **AUTHORIZED**。ただし提示二点は外部正例でなく、実走前でもあるため、EP の較正済み正例ゲートとしての「再発効」は **現時点 FAIL**。 |

指定された正本・証明書の SHA-256 は全て便記載値と一致した。以下、必須修理を先に固定する。

## 1. U2-BR — 核比較による非分岐橋

### F93-1.1　Ihara §5.2 の引用

Ihara, ICM 1990 のページ画像で、次を原文照合した。

1. 印刷頁 106 の (2.3.2) は

   \[
   x\longmapsto x^{\chi(\sigma)},\qquad
   y\longmapsto f_\sigma^{-1}y^{\chi(\sigma)}f_\sigma,
   \qquad f_\sigma\in\widehat F_2'
   \]

   という Ihara 作用の形を与える。
2. 印刷頁 111–112 の §5.2 は、pro-(\ell) 外作用の有限下中心商の核の固定体を合併した (\mathbf Q^{(\ell)}(\infty)) が、完全 pro-(\ell) 外表現の核の固定体であり、

   \[
   \mathbf Q(\mu_{\ell^\infty})\subset
   \mathbf Q^{(\ell)}(\infty)
   \]

   が (\ell) 以外で不分岐である、と述べている。
3. この記述は (\ell=2) を除外していない。従って有限部分拡大が 2 以外で不分岐、という U2-BR の使用法は正しい。

Question 6.5.2、AI1988 の入手不能部分、moduli 上の定義体はいずれもこの証明には不要である。

### F93-1.2　補題 INN

補題 INN の群論は正しい。自由 pro-2 群 (P=\widehat F_2^{(2)}=\langle x,y\rangle) で外作用が自明なら、ある (g\in P) により作用は内共役である。(\chi_2=1) なので (x) は固定され、従って

\[
g\in C_P(x)=\overline{\langle x\rangle}.
\]

また (g^{-1}yg=f^{-1}yf) から (h:=gf^{-1}\in C_P(y)=\overline{\langle y\rangle})。Ihara の (f\in P') を使うとアーベル化で (\bar h=\bar g)。一方、(\bar g) は (x)-軸、(\bar h) は (y)-軸にあるので、両者は 0 である。各 procyclic 軸から (P^{\rm ab}\cong\mathbf Z_2^2) への写像は単射だから (g=h=1)、従って (f=1)。

外部入力は「自由 pro-(p) 群の非自明元、特に自由生成元の中心化群は procyclic」という古典結果だけで足りる。最終稿では Herfort–Ribes, *Torsion elements and centralizers in free products of profinite groups*, J. reine angew. Math. **358** (1985), 155–161, DOI `10.1515/crll.1985.358.155`、または Ribes–Zalesskii の *Profinite Groups* の該当定理番号まで固定するとよい。

### W93-1.1　現稿の (m)-成分はそのままでは誤り

`u2_unramified_bridge_v1.md` の

\[
\chi\equiv1\pmod {2^a},\qquad 2m+1\equiv1\pmod {2^a}
\quad\Longrightarrow\quad m\equiv0\pmod {2^a}
\]

は成立しない。ここから直接得られるのは (m\equiv0\pmod {2^{a-1}}) までである。これは単なる説明不足ではなく、有限合同環で 2 を割った偽推論なので、現稿の証明をそのまま PASS にはできない。

### P93-1　U2-BR の必須置換文

この箇所は次で完全に直る。

> Ihara の無限 pair の第一成分を
> \[
> \widehat m=(\chi-1)/2\in\widehat{\mathbf Z}
> \]
> とする。(\sigma\in\ker\varphi^{(2)}) なら (\chi_2(\sigma)=1) が (\mathbf Z_2^\times) 内で**等式として**成り立つので、(\widehat m_2=0\in\mathbf Z_2)。有限 Ihara pair の (m)-成分はこの無限成分の (\mathbf Z/2^a\mathbf Z) への像であるから (m=0\pmod {2^a})。

重要なのは「有限合同を 2 で割る」のではなく、「無限 pair の 2-adic 成分が零であることを有限商へ落とす」ことである。

### F93-1.3　有限 2-群商と固定体

(F_2/K) が 2-群なら、その完備化への写像は最大 pro-2 商を通る。有限指数 (K) の profinite 閉包を明記すれば、INN により

\[
\ker\varphi^{(2)}\subseteq\ker\operatorname{Ih}_K
\]

が従う。固定体の向きも正しく、

\[
L_K=\overline{\mathbf Q}^{\ker\operatorname{Ih}_K}
\subseteq
\overline{\mathbf Q}^{\ker\varphi^{(2)}}
=\mathbf Q^{(2)}(\infty).
\]

よって (L_K/\mathbf Q(\mu_{2^\infty})) の該当有限部分は 2 以外で不分岐である。

### F93-1.4　(R1)–(R3) と混合帰着

- (R1): (K_{\rm ord}=2^a) により上の (m)-成分修理が使える。
- (R2): (F_2/K) が 2-群なので (f)-成分が最大 pro-2 商を通る。
- (R3): §5.2 の固定体包含と非分岐性で閉じる。

混合交叉の議論も通る。2-primary 側との共通有限商では、奇側の導来平行移動部分が消え、共通部分はアーベル、従って (\mathbf Q(\zeta_{4n})) 内に入る。他方 U2-BR により 2 以外で不分岐なので、導手を比較すれば共通部分は (\mathbf Q(i)) 以下であり、逆包含は既知だから交叉は (\mathbf Q(i))。従って既存の奇側定理を仮定した n12_goursat §7.1 の「混合側 (\Leftarrow) 奇側」を、P93-1 適用後に発効してよい。

**§1 最終判定:** 定理命題は正しい。文書は P93-1 を入れた版へ更新することを条件に PASS。

## 2. D-3 / D-4 と (u_7) 発火

### F93-2.1　TOWER-n

TOWER-n の中間部分群の議論は通る。(J=\bar A\bar H) は (\bar H) を含む指数 2 の一意な中間部分群で、下段 (V\to\mathbf P^1_\lambda) は 0 と (\infty) だけで分岐する二重被覆である。従って (V) は種数 0 であり、分岐点が (F)-有理なので正確には

\[
V\cong\mathbf P^1_F
\]

と書ける。

上段の (D_n) モノドロミーも正しい。ただし (\bar H\) は一般に (J) の正規部分群ではないため、「群 (J/\bar H)」とは書かず、「左剰余類集合 (J/\bar H) 上の (J) の置換作用」と書くべきである。

(Y) の二つのブロックへの固定点の分配には一行必要である。各ブロックは (Y)-不変で大きさが奇数 (n)、従って各ブロック上の involution は少なくとも一固定点を持つ。全体の固定点が 2 個なので、各ブロックにちょうど 1 個となる。「対称だから均等」だけでは証明にならないが、この parity 論で閉じる。

### W93-2.1　KUM-n の (F)-有理性と剛性の過大記述

一般の二次不変量を保ったままでは、(B\cong\mathbf P^1_F) は従わない。(m)-座標での正しい一般形は

\[
F(B)=F(m)\!\left(\sqrt{\delta_0(\gamma m^2-1)}\right),
\]

であり、(B) の Brauer 類は ((\gamma,-\delta_0))。分岐点 (\mu_\pm=\pm\gamma^{-1/2}) は unordered divisor として (F)-有理だが、個別に (F)-有理なのは ([\gamma]=1) の場合だけである。さらに (B\cong\mathbf P^1_F) にはこの conic の分裂が必要である。

Kummer 記述

\[
F(\widetilde W)=F(B)(h^{1/n})
\]

自体は (\mu_n\subset F) により (F(B)) 上で成立する。しかし「四分岐点と指数だけで (\overline F) 上剛」という文は一般には偽で、四点には cross-ratio moduli がある。本件で剛になる理由は、四点が既知の二重写像 (B\to V) の二組の逆像で、正規化後

\[
\{\kappa_1,\kappa_2,\kappa_3,\kappa_4\}=\{i,-i,1,-1\}
\]

という関係まで塔データに固定されるからである。KUM-n の命題には「TOWER-n の写像と標識を保つ」という条件を入れる必要がある。Kummer 定数が奇数 (n) で吸収される部分は正しい。

### F93-2.2　SPLIT

固定した (m)、(B\to V)、局所一様化元 (\tau) のもとで

\[
m=c\tau^n(1+O(\tau)),\qquad
\lambda=\gamma m^2
\]

から (u_n=\gamma c^2) は正しい。ただし (m) や (\tau) の再尺度で代表元は変わる。座標なしで不変なのは

\[
[u_n]_{2n},\qquad [u_n]_2=[\gamma],\qquad
[u_n]_n=[\gamma]_n[c]^2_n
\]

である。従って「等式」はモデル・座標つき、「類」は抽象被覆の主張、と明記すべきである。

### F93-2.3　TW-1 / D-4


\[
\operatorname{Aut}_{\overline F}(W/\mathbf P^1)
=N_{\mathcal M_n}(\bar H)/\bar H=1
\]

は W3 の normalizer 計算から正しい。このため、**存在が既に分かっている** (F)-形式の同型類は一意である。既存の算術被覆の関数体、その一意な中間部分群から (V,B) を取れば各中間体も (G_F)-安定で、descent は閉じる。

一方、自己同型群が自明であることは「任意の (\gamma',\delta_0') に対して (F)-形式が存在する」ことを意味しない。従って v2 の結論、すなわち ([\gamma])、([\delta_0]) は自由な twist parameter ではなく、存在する被覆から一意に読まれる invariant である、を採択する。

### P93-2　P-7 の座標非依存な修正文

凍結 P-7 の

\[
\frac{m-\mu_+}{m-\mu_-}=\delta k^2
\]

は ([\gamma]=1) と (B\cong\mathbf P^1_F) を先取りする。事前登録は次に置換すべきである。

> (f_\gamma(m)=\gamma m^2-1) とし、
> \[
> F(B)=F(V)\left(\sqrt{\delta_0 f_\gamma(m)}\right)
> \]
> を基礎定義とする。([\gamma])、([\delta_0])、Brauer 類 ((\gamma,-\delta_0)) を先に測る。([\gamma]=1) かつ conic が分裂した枝でのみ (k)-座標を選び、従来の (\delta) と比較する。

この修理は答の一方の枝への事前コミットを除く。

### F93-2.4　経路 A の (u_7=-4)

明示モデル

\[
h(k)=\frac{k-i}{k+i}\left(\frac{k+1}{k-1}\right)^\alpha,quad
m_0=\frac{1+k^2}{1-k^2},\quad \lambda=m_0^2
\]

で、(k=i) における

\[
h_1=\lim_{k\to i}\frac{h(k)}{k-i}
=\frac{(-i)^{\alpha+1}}2,qquad m_0'(i)=i
\]

を使うと、(y^n=h(k)) の (y) を一様化元として

\[
u_{n,\alpha}=\frac{-1}{h_1^2}=4(-1)^\alpha.
\]

(n=7,alpha=1) では (u_7=-4)。これは浮動小数点や class-group 計算を使わない紙上の局所展開であり、経路 A として PASS である。抽象 C5 の任意一様化元に対して主張できるのは ([-4]_{14}) で、exact equality は上記の (k,h,y) を束縛した代表元の主張である。

二つの (\mathfrak p\mid2) で (v_\mathfrak p(2)=2) だから (v_\mathfrak p(-4)=4)、他では 0。従って局所付値像 (4\in\mathbf Z/14\mathbf Z) の位数は 7。さらに

\[
(-4)^7=(2\zeta_{28})^{14}
\]

なので全体の Kummer 類の位数も正確に 7 である。

### F93-2.5　二経路一致の正しい格付け

経路 B は B-5 torsor の (\mu_2) 押し出しから

\[
[u_7]_2=\chi_{\rm blk}=[\gamma]
\]

を導く。明示モデルでは二つの非分岐点が個別に (F)-有理なので ([\gamma]=1)。これは経路 A の ([-4]_2=1) と一致し、共有前提を明記した **square-class 層の cross-check** と認める。

しかし経路 B は (c) の 7-part、(-4) という代表元、または (v_\mathfrak p=4) を独立に再計算していない。第二系統の GAP 19/19 もブロック・回転指数・Kummer 記号という有限群層の照合であり、局所係数の独立算出ではない。従って `u7_fire` の `agree=true` は

```text
agreement_scope = square_class_mu2
exact_value_source = path_A_explicit_local_model
shared_assumptions = [TOWER-n, SPLIT, B-5]
```

という粒度で解釈・記録すべきである。

NULL 枠が不発動し、LB-RES が付値で決着したことは承認する。ただし G-1〜G-4 は未評価なので、ここから SURJ-K7 や functional window の算術同定を主張してはならない。C1′(7) の回転指数比は次段の必須 gate のままである。

**§2 最終判定:** D-3/D-4 は W93-2.1、P93-2、座標つき／なしの区別を反映した改訂版に条件付き PASS。(u_7) は上記の層別格付けで採択。

## 3. FAM-U — 全奇数 (n) の族候補

### F93-3.1　一様公式と位数

経路 A の計算では (n) は (y^n=h) の ramification index にしか現れず、(h_1) と (m_0'(i)) の計算には現れない。従って、奇数 (n\ge3)、単元窓 (H_{2,\alpha,0}) の固定した明示モデルで

\[
u_{n,\alpha}=4(-1)^\alpha
\]

が一様に従う。

(\alpha) は本来 ([\alpha]\in(\mathbf Z/n)^\times/\{\pm1\}) なので、exact sign は選んだ整数代表・向きに依存する。しかし

\[
-1=\zeta_{4n}^{,2n}\in F_n^{\times,2n}
\]

であるため

\[
[u_{n,\alpha}]_{2n}=[4]_{2n}=[-4]_{2n}
\]

は代表と向きに依存しない。各 (\mathfrak p\mid2) で (v_\mathfrak p(u)=4) だから、付値像の位数は

\[
\frac{2n}{\gcd(2n,4)}=n
\]

である。一方 ((\pm4)^n) は (F_n) 内の (2n) 乗なので、全体の類の位数はちょうど (n)。この算術は合成数の奇 (n) にも同じである。

### W93-3.1　族定理へ上げる前に残る束縛

次の依存を定理文に隠してはならない。

1. W93-2.1 を直した TOWER/KUM と、塔の四点 cross-ratio の束縛。
2. 明示した標準 (F_n)-モデルが、対象の算術被覆の一意な (F_n)-形式であること。TW-1 は**一意性**を与えるが、モデルの存在・同定を代用しない。
3. (H_{2,\alpha,0})、回転指数比、cusp、局所一様化元の source-map。特に exact equality と Kummer class を分けること。
4. 各 (n) の functional window をこの窓に結ぶ C1′／reduction-functoriality。現状 ([\alpha]=[1]) を採る根拠は規約で、一般定理ではない。
5. (W1)–(W5)、BFC、および幾何／算術モノドロミーの区別。族公式だけから Ihara 全射性は出ない。

### P93-3　推奨する theorem-candidate 文

> 奇数 (n\ge3) と単元 (\alpha\) に対し、指定された (K^{(n)}) 窓の TOWER/KUM 標準モデルおよび指定 cusp/source-map を取る。このモデルの主係数は (u_{n,\alpha}=4(-1)^\alpha) であり、その座標不変 Kummer 類は ([u_{n,\alpha}]_{2n}=[-4]_{2n})、位数は (n) である。

この形なら paper theorem candidate として採択する。各窓が算術的に対象であること、また SURJ を結論することは別 gate とする。

## 4. PENT settled / ORI / isolated

### F93-4.1　ORI と 20/20

ORI の向き

\[
\rho(q)=\widehat c(f)^{-1},\qquad
\ell(q):=\tau(\rho(q))=f
\]

は証明・7500 元照合・v3.2 の全行と整合する。従って v3.1 の 4/8/8 は、(f) と (f^{-1}) を混ぜた規約 artifact であり、自己逆元だけ 4 個残るという指紋も説明できる。整合規約 (T') での `well_defined=20/20`, `settled=20/20` は採択する。旧 4/8/8 は反例でなく、廃止した混成規約の回帰 fixture として保存すればよい。

### W93-4.1　指定された一行 assert は偽

指数を (a^g=g^{-1}ag) とすると、(T') について直接 (\rho) を取った値は

\[
\begin{aligned}
\rho\bigl(T'(\Psi(y))\bigr)
 &=\rho(q)y^u\rho(q)^{-1}\\
 &=\widehat c(f)^{-1}y^u\widehat c(f)\\
 &=(y^u)^{\widehat c(f)}.
\end{aligned}
\]

従ってこれを ((y^u)^f) と同一視する assert は、非自己逆元で一般に偽である。cert の失敗行は実装事故でなく型の不一致を正しく捕獲している。

### P93-4　正しい可換図と残る gate

正しい式は粗いラベルを通した

\[
\boxed{\ \ell\bigl(T'(\Psi(y))\bigr)=(y^u)^f\ }
\]

である。ただし (\ell) は通常の準同型でなく反準同型なので、対象を (P^{\rm op}) とするか、合成則を反転して formalize しなければならない。群化へ進む前に少なくとも次を要求する。

1. (\ell(q_1q_2)=\ell(q_2)\ell(q_1)) を型として固定する。
2. (T') の合成と opposite 側の積が一致することを証明する。
3. PB3 層の 20/20 と、PB4 の source kernel／Prop. 2.11 相当を分離する。
4. `red` が積を保つことを上の型で証明する。

従って (K_\pi) を `isolated (candidate)` に戻すのは承認するが、(GT(K_\pi)) の群化や `red` の準同型性を既成定理として復活させるのはまだ不可。Lean による verified 状態でもない。

## 5. 訂正・修文・再請求

### F93-5.1　9T27 訂正

訂正を採択する。

\[
9T27=\operatorname{PSL}(2,8),\quad |9T27|=504;
\qquad
9T32=\operatorname{P\Gamma L}(2,8),\quad |9T32|=1512.
\]

passport 上界から (A_9,S_9) を除けず、branch-cycle の (C_3) と外部自己同型の (C_3) が一致するため有理性だけで六候補を分離できない、という二つの安価な経路の死亡も妥当である。C1′/S4 の生存経路は fibre-product 構成だけで、状態は引き続き UNKNOWN。

### F93-5.2　T3 weighted

加重定義、軌道和、T3-N0″、J-AUT、T3-WALL″ の中核は正しい。Jordan を使う領域は Aut divisor 条件で安全に切られている。

(m=1) の五 passport は実現可能なものを尽くしている。見かけ上の第六候補 ((0,2,0)) は方程式から (n=0) を強制し、(n\ge1) で不可能、と一行明記すると列挙が自己完結する。

ただし「(N_w) と (N_{\rm gen}) には大小関係がなく (N_w<N_{\rm gen}) もありうる」という一般文は、本書の (n\ge4) の領域では誤りである。J-AUT により生成する各クラスは (\operatorname{Aut}=1) だから

\[
\boxed{\ N_{\rm gen}\le N_w\le N_{\rm tr}\ }
\]

である。左辺は生成クラスが各々 weight 1 を寄与し、非生成クラスの weight が非負であること、右辺は各 weight が高々 1 であることから従う。この局所修文は T3-WALL″ の結論を壊さない。

**判定:** 上の一文を直す NOTE つきで T3 theorem group と weighted addendum の完全採択を承認する。旧記法との衝突では weighted addendum を正本とする。

### F93-5.3　(u_0) cross-check

v2 checker は主 checker/helper を import せず、入力曲線上で (t=A+yB)、ノルム (N_\tau)、(\kappa/\delta) を再構成している。ソースコメントに `3*t` と書かれた一箇所はコメントの typo で、実コードは主モデルと一致する (t) を使うため数値に影響しない。

証明書は checker、入力、raw output の digest と再現 command を束縛しており、raw log も証明書内に封印されている。共有物は入力曲線データであることも開示されている。結果

\[
u_0^{-1}=-\frac{1423828125}{256}
=-\frac{3^6 5^9}{2^8}
\]

および付値は整合する。B4 は値の独立計算でなく構造照合、という格付けも正しい。従って (u_0) は cross-checked として採択する。ただし C1′/S4 全射性は別 gate であり、ここからは出ない。

## 6. (o)/EP v12 と単発実走案

### F93-6.1　v12 の A/B 原子化修理

`resolve_bundle` は well-shaped な参照を受けた後、`CURRENT` を一度だけ読み、捕捉した generation を一度だけ load/verify し、その generation ID、freeze、artifact 群をまとめて返す。consumer は候補一件の A/B についてこの入口を一回だけ使う。generation directory は immutable で、既存 generation の上書きも拒否される。従って W92-6 の「A は旧世代、B は新世代」という race は閉じた。

16a は旧 per-side 経路で同一 freeze の混成が実際に起きること、16b/16c は v12 経路が swap 中にも一 generation だけを返すことを検査しており、負例として適切である。失敗後の `index_exists()` による coarse 分類は内容を PASS に昇格しないので、安全性を壊さない。

### F93-6.2　試験の再実行範囲

この監査環境で次を実行し、全件 PASS を再現した。

- `python test_ninfty_laneB.py`: 184/184
- `node ninfty-selftest-lanea.mjs`: 93/93
- `python test_ninfty_legacy_normalizer.py`: 51/51

合計 328/328。registry suite 227 件は sandbox が一時 generation directory を作る段で `PermissionError` となり、この環境では再実行できなかった。これはテスト反例ではない。ソースと便の producer receipt 上は 227/227 を確認したが、私の独立再実行としては数えない。従って `555/555` は「producer receipt + Sol による 328 件再現」と記録するのが正確である。

### F93-6.3　sol75 の法的読み

sol75 L55 は searcher/checker/verifier の凍結 schema 下での実行を **AUTHORIZED** とし、EP 前に禁じているのは `calibrated detector` や `complete search` などの宣言である。従って研究者認可も得た現在、事前登録した候補に対する一回の partial-predicate 実走は法的に許される。この点の便 93 の読みを承認する。

実走後も許される表示は

```text
run_mode = partial_predicate
complete_search = false
calibrated_detector = false
mathematical_status = UNKNOWN
```

までである。これらが frozen artifact schema の未定義 field なら、既存の許可済み metadata extension または別 receipt に置き、schema を黙って増やしてはならない。

### W93-6.1　二点案は「外部正例 EP」ではない

(\alpha) は既知の negative fixture、(\beta) は同じ campaign の stage1 通過候補で、既存 lane では stage2 `hits=0` である。従ってどちらも independently known positive ではない。この二点は transport、schema、reject path の production artifact を作る engineering unit には使えるが、感度を較正する external-positive control にはならない。

また (\beta) について `REJECT guaranteed by hits=0` と事前記載してはならない。独立 lane の結論が違えば、それ自体が重要な不一致だから、正しくは「既存 lane の予測は REJECT、独立 lane の結果は未観測」である。指定順序での辞書順最小ベクトル

\[
(-1,-2,-2,2,0,0,-1,-2,-2)
\]

と「(R(v)) が偶数でない」という既存 stage2 理由の束縛は確認した。

86,410,020 件で stage2 accept が 0 という報告は、「その凍結 predicate が登録宇宙で accept を返さなかった」という結果としては価値がある。しかし detector の完全性が未較正なので、「数学的正例が存在しない」や「探索が完全」という結論には使えない。正例存在の紙上構成または campaign 外で独立にラベル済みの同次数・同 schema 正例を先に置く順序を推奨する。

### W93-6.2　二候補を一束にする場合の batch-level race

v12 が原子化したのは**一候補の A/B pair**である。(\alpha) と (\beta) を consumer が二回別々に解決すれば、その二回の間に `CURRENT` が変わり、二点全体は異なる generation になりうる。従って「四 artifact が一 generation の two-point bundle」という主張には、pair-level 修理だけでは足りない。

### P93-6　許可する単発 protocol

1. (\alpha,eta) は negative/unknown engineering controls と明記し、EP positive calibration とは呼ばない。
2. 四 artifact を一 generation に置くなら、workflow 冒頭で generation ID を一度 pin し、その ID から四つ全部を読む batch resolver を使う。さもなければ候補ごとに generation と receipt を分け、二点同世代を主張しない。
3. runner/steward、source digest、build metadata、freeze ID、各 lane の独立 toolchain を production receipt に束縛する。新 CI wrapper が依存閉包を増やすなら新 receipt を発行する。
4. 不一致を fail-closed で保存し、結果を見て候補・順序・predicate を交換しない。
5. 実走は一回の engineering bundle として **AUTHORIZED**。これにより W92-8(c)(d) の production-artifact 条件を満たすことはできる。
6. ただし independently known positive がない限り、CR11/QD6/N2 等の数学的 UNKNOWN、較正済み detector、complete search、EP positive gate の発効は主張しない。

**§6 最終判定:** v12 修理と限定実走を承認する。「EP 再発効」が pipeline の限定再入場を意味するなら条件付き PASS、外部正例で較正された数学ゲートを意味するなら現時点 FAIL。

## 7. 情報共有物と対話帳

### F93-7.1　壁 r2 receipt

二つの r2 証明書は window-specific schema、`DRIVER_DONE`、freeze/source digest を束縛し、SURV はそれぞれ 3720/3720、22320/22320、failure 0 で前回値と一致している。GAP workflow の成功語が `done`、Python workflow が `passed` という注記も実装に整合する。今回 GAP を独立再走してはいないが、receipt の整合監査上 C-WALL-FAM の CLAIMS 登録に異議はない。

### F93-7.2　prefire と (h^-)

`u7_prefire` の CAL-3 17/17 と MP-4 の 787 素点は発火前 gate の記録として整合する。ただし 787 素点は登録 pool に対する必要条件検査であり、MP-4 の全数学的分離定理とは呼ばない。

`hminus_zeta28` は (h^-(\mathbf Q(\zeta_{28}))=1)、較正 (n=23\mapsto3)、(n=20\mapsto1) を正確に記録している。F92 の紙上採択と整合する。今回の (u_7) 位数は付値だけで閉じるため、この class-number 計算には依存しない。

### F93-7.3　T-19 / T-20 への回答

T-19 の TOWER/KUM/SPLIT は、上界層の第二系統を設計する骨格として有効である。ただし第二系統が独立に二重化するのは ([u_n]_2=[\gamma]) までで、(n)-part や exact (u_n) までではない。

T-20 の「([\gamma],[\delta_0]) は自由 twist でなく一意決定 invariant」という訂正を採択する。同時に T-20(3) の P-7 批判は正しく、P93-2 の座標非依存形への置換が必要である。TW-6 の符号つき回転指数は二つの候補 descent を分ける機構として使えるが、存在そのものは既存算術被覆または明示モデルから別途供給すること。

## 最終ゲート宣言

- **U2-BR:** P93-1 を本文へ反映した改訂版に限り PASS。反映後、(U2) と「混合 (\Leftarrow) 奇」の橋を発効してよい。
- **D-3/D-4:** W93-2.1、P93-2、座標依存性を直した改訂版に条件付き PASS。
- **(u_7):** exact model value (-4) と ord 7 は PASS。([u_7]_2) の二経路 cross-check は PASS。exact value 全体の cross-check 表示は却下。SURJ-K7 は UNKNOWN。
- **FAM-U:** P93-3 の形で theorem candidate 採択。算術窓同定・SURJ は別 gate。
- **PENT:** PB3 settled 20/20 は採択。偽 assert を廃棄し opposite/anti-label を formalize するまで群化は candidate。
- **T3:** 局所不等式修文つきで完全採択。
- **(u_0):** cross-checked 採択。
- **EP:** v12 pair atomicity と限定 unit run は承認。外部正例による EP 発効は未成立。

本便で Lean 証明書は作成・確認していないため、いずれの新規主張にも `verified` の語は付さない。
