# 便 79 返信 — W-Exist・等号問題・CASC・WCP5-D 数学監査

## 0. 結論先取

**総合判定は条件付き PASS。** 主定理群のうち W-Exist と CASC、反例 \(L\)、WCP5-D の \(c\)-補正式および商規律 (F2) は紙上で閉じる。一方、次の主張はそのままでは採用できない。

1. **FAIL:** T-A(4)(5) の「任意の \(N\) で \(\widetilde\chi_{2N_{\rm ord}}\) は全射」。Ihara 元を target \(N\) へ射影しても、非 isolated \(N\) では一般に source が \(N\) とは限らず、isotropy group \(GTSh(N,N)\) の元にならない。
2. **FAIL:** T-G の「反例は \(|\mathfrak F_0|\) が非素数の窓にしかない」。補題 P 自体は正しいが、その系を導く群論的推論は偽である。素数位数の核をもつ可換群でも等号は破れる。GT 窓だけに限定した版を救う追加定理は提示されていない。
3. **FAIL:** I-24 の「同一 dessin」「従って \(j\) 盲目」。得られた witness は \((X,Y)\) と \((X,Z)\) の同時共役、すなわち枝値 \(1,\infty\) の入替えを伴う \(S_3\)-relabeling を示すに留まる。
4. **FAIL:** W-C-p5 の 40 個を直ちに \(GTSh(N,N)\cong C_2\times\operatorname{Aff}(\mathbf F_5)\) と呼ぶこと。full hexagon と形式的な合成閉性は確認されているが、全 40 個の source kernel \(=N\) は未確認である。
5. **修正必須:** WCP5-D の (F1) は \(e(w)\equiv0\pmod{\operatorname{ord}(c)}\) だけでは足りない。正典 Prop. 3.4 を使う安全な条件は、実際に
   \[
   w\in[F_2,F_2]\quad\Longleftrightarrow\quad e_x(w)=e_y(w)=0
   \]
   である。

§6 の予告は全文を読んだが、本便の指定どおり監査対象外とした。

---

## 1. W-Exist の二層検証

### F79-1.1 — W-Exist は CONFIRM（位相補修つき）

補修後の論証は正しい。

全 isolated \(N\) で有限群 \(GT(N)\) が可解だと仮定する。すると
\[
L:=\varprojlim_{N\ {\rm isolated}}GT(N)
\]
は prosolvable である。遷移射の全射性は不要で、\(L\) が有限可解群の積の閉部分群であることだけを使えばよい。

ここで必要なのは抽象単射ではなく、位相群としての連続単射
\[
G_{\mathbf Q}\xrightarrow{\rm Ih}\widehat{GT}_{\rm gen}
 \xrightarrow[\sim]{\Psi}L .
\]
補題 C の閉じ方も妥当である。

- \(E:\widehat{GT}_{\rm gen}\to\operatorname{Aut}(\widehat F_2)\) は連続単射。
- \(\widehat{GT}_{\rm gen}\) はコンパクト、\(\operatorname{Aut}(\widehat F_2)\) は Hausdorff なので、\(E\) は像への同相。
- 接基点つき Galois 作用 \(\rho:G_{\mathbf Q}\to\operatorname{Aut}(\widehat F_2)\) が連続なら、\({\rm Ih}=E^{-1}\circ\rho\) は連続。
- 従って \(G_{\mathbf Q}\) の像はコンパクト、よって \(L\) の閉部分群である。

このとき \(G_{\mathbf Q}\) の任意の有限**連続**商は \(L\) の有限可解商の部分商となり可解である。しかし \(x^5-x-1\) の分解体は \(S_5\) 商を与えるので矛盾する。従って非可解な \(GT(N)\) をもつ isolated \(N\) が存在する。

位相を落とした版が偽であるという反証も適切である。抽象自由群 \(F_2\) は自由 pro-\(2\) 群へ単射する一方、\(S_5\) へ全射する。prosolvable 群の**抽象**部分群の任意の抽象有限商まで可解とは限らない。

### F79-1.2 — 仮定負荷

仮定表 H1–H5 の分類を承認する。

- H1: Belyi による Ihara 単射。
- H2: \(\widehat{GT}\le\widehat{GT}_{\rm gen}\) は正典から継承し、本便では再導出しない。
- H3: isolated Main Line の逆極限同相。
- H4: 上の補題 C。ただし最終依存は接基点分裂 \(s\)／Galois 作用の連続性という標準枠組み事実である。
- H5: \(S_5\) の有限連続商。

したがって枠組み負荷は (TB1)(TB3) 側の連続性一点であり、(TB4) は使わない、という整理でよい。補題 A–C は paper-proof candidate で、Lean verified ではない。

### F79-1.3 — 非 metabelian isolated 窓

この強化も承認する。しかも \(d=2\) の場合は、W-Exist 本体より位相依存が軽い。

全 \(GT(N)\) が metabelian なら、その積、逆極限、および任意の抽象部分群も metabelian である。従ってこの段では Ihara の**抽象単射**だけで矛盾を導ける。\(x^4-x-1\) の Galois 群 \(S_4\) は
\[
S_4'\!=A_4,\qquad A_4'\!=V_4,\qquad V_4'\!=1
\]
より導来長 3 で、metabelian ではない。従って非 metabelian な isolated 窓が存在する。指数の上界は依然として出ない。

### F79-1.4 — 訂正 5 件の採否

1. **採用:** W-Exist の証明に Ihara 写像の連続性と閉像の一段を挿入する。
2. **採用:** 非 metabelian isolated 窓の存在を併記する。上記のとおり、この強化には実は閉像まで要らない。
3. **採用:** 正典の character は
   \[
   \chi_{{\rm vir},N}:GT(N)\to(\mathbf Z/N_{\rm ord})^\times
   \]
   と書く。後述の法 \(2N_{\rm ord}\) の refined character は別 ID
   \(\widetilde\chi_{2N_{\rm ord}}\) とし、正典 character を上書きしない。
4. **採用:** 「全 finite gentle 窓」を「全 isolated 窓」に直す。
5. **採用:** ★教材には「prosolvable の遺伝は位相込み。制御するのは有限連続商」と明記する。

---

## 2. \(\ker\widetilde\chi=[GT,GT]\) の等号問題

### F79-2.1 — T-A の型ゲート

\[
G_N:=GTSh(N,N),\qquad M:=N_{\rm ord}
\]
と置けば、任意の \(N\) について
\[
\widetilde\chi_{2M}:G_N\to(\mathbf Z/2M)^\times,\qquad
[m,f]\mapsto 2m+1
\]
が well-defined な準同型であり、
\[
\ker\widetilde\chi_{2M}=\mathfrak F_0
\]
である、という T-A(1)–(3) は正しい。

しかし T-A(4) の証明に置かれた
\[
{\rm Ih}_N={\rm PR}_N\circ{\rm Ih}:G_{\mathbf Q}\longrightarrow G_N
\]
は、一般の非 isolated \(N\) では型が合わない。射影された shadow は target \(N\) をもつが、source は一般に別の \(N^{(g)}\) であり、\(GTSh(N,N)\) の元とは限らない。これは W-Exist ノート §6 の groupoid 警告とも一致する。

従って正しい一般形は
\[
Q_N:=\operatorname{Im}\widetilde\chi_{2M},\qquad
|G_N|=|\mathfrak F_0|\,|Q_N|.
\tag{2.1}
\]
さらに
\[
Q_N=(\mathbf Z/2M)^\times
\]
と言えるのは、少なくとも次のいずれかの場合に限る。

- \(N\) が isolated で、Main Line の射影と円分 character の全射性を使える。
- 当該 isotropy 群について独立な全射証明書がある。

25 窓の実測一致はその 25 窓の有力な regression であり、普遍定理ではない。掃引 assert は

```text
|ker_chi| * chi_image_order == |G_N|
```

を普遍形とし、

```text
chi_image_order == phi(2*N_ord)
```

は `isolated=true` または `chi_surjectivity_cert` がある場合だけ発火させるべきである。

### F79-2.2 — T-B は \(Q=\operatorname{Im}\widetilde\chi\) で PASS

完全列
\[
1\to\mathfrak F_0\to G_N\to Q_N\to1
\]
に対する LHS 5 項完全列から
\[
\frac{\mathfrak F_0}{[G_N,G_N]}
\cong
\operatorname{coker}\!\left(
H_2(Q_N;\mathbf Z)\xrightarrow{\rm tg}
(\mathfrak F_0^{\rm ab})_{Q_N}
\right),
\qquad
H_2(Q_N;\mathbf Z)\cong\Lambda^2Q_N
\tag{2.2}
\]
を得る。B1–B3 はこの修正版で正しい。K8/K16 が示すとおり、余不変量が非零であるだけでは足りず、transgression の像まで見る必要がある。

### F79-2.3 — 反例 \(L\) は PASS、ただし a priori 証明に一行補修

`python search/kerchi-abelianization-check.py` を再実行し、18 窓の表を再現した。唯一の等号破れは L01 で、
\[
|G_L|=36,\quad |Q_L|=4,\quad
|\ker\widetilde\chi|=9,\quad
|[G_L,G_L]|=3,
\]
従って
\[
\ker\widetilde\chi/[G_L,G_L]\cong C_3
\]
である。L01 の 1296-entry composition table は既存の GAP/Node 二レーン判定があり、この有限群表に関する反例は cross-checked、Lean verified ではない。`ke_a_normality_20260729.json` は \(L\triangleleft B_3\)、指数 17496 を閉じるが、この正規性証明書自体は GAP 一レーンである。

重み \(u\)／\(u^2\) による機構も正しい。ただしノート §5.2 の

> \(Q\)-固定な一次元部分群 \(\langle g_1\rangle\) があるから、\(Q\)-自明な商がある

には一行不足している。ここでは \(|Q|=4\) と係数標数 \(3\) が互いに素なので Maschke により \(\mathbf F_3[Q]\)-加群は半単純である。従って固定直線は \(Q\)-安定補空間をもち、\(Q\)-同変射影
\[
\mathfrak F_0^{\rm ab}\twoheadrightarrow\langle g_1\rangle\cong C_3
\]
が存在する。これで B3 を適用できる。

なお「a priori・実測非依存」は少し強すぎる。重み 2 の生存機構は理論的だが、\(\mathfrak F_0^{\rm ab}\) の具体的な \(C_3^2\) 構造と中心方向の同定には登録証明書を使っている。**理論機構と有限データを組み合わせた反例**と呼ぶのが正確である。

### F79-2.4 — T-C と T-E

- **T-C: PASS.** 正典 Thm. 4.6 の群構造を前提に、奇数部、\(\alpha=1\)、\(\alpha\ge2\) の三分岐で導来部分群の位数が \(|G|/\varphi(2M)\) と一致する。dihedral \(K^{(n)}\) 全 \(n\ge3\) で等号が成立する。
- **T-E: PASS.** abelianization 層に重み \(u\)、\(\gamma_2/\gamma_3\) に重み \(u^2\) が作用する。全単元が \(u^2=1\) となる法は \(e\mid24\) であり、Heisenberg の \(e=3\) 中心が生存する説明と整合する。

### F79-2.5 — T-G は「補題 PASS・系 FAIL」

補題 P
\[
|\mathfrak F_0|=p\ {\rm prime}
\quad\Longrightarrow\quad
\bigl(\mathfrak F_0=[G,G]\iff G\ {\rm nonabelian}\bigr)
\]
は正しい。\([G,G]\le\mathfrak F_0\) なので、導来部分群は \(1\) または \(\mathfrak F_0\) しかない。

しかし「従って素数核は反例にならない」という**一般群論の系**は偽である。任意の可換群 \(Q\) と素数 \(p\) に対し
\[
G=C_p\times Q\longrightarrow Q
\]
を射影とすれば、核は \(C_p\) だが \([G,G]=1\) で、等号は破れる。従って素数核は**除外篩**ではなく、非可換性を測る一ビット判定器である。GT isotropy 群に限って「可換なら核は自明」とする追加定理が将来立てば限定版は救えるが、本ノートにはその定理がないため、現状の GT 限定主張も採用不可である。

この修正により、ノート §7.5 priority 0 の「素数または 1 を反例探索から除外」は削除すべきである。核が 1 の場合だけは無条件に等号成立である。

census v2 で \(N_3\) 本体の導来長が 2、従って非可換と確定したため、既存の \(|\mathfrak F_0|=2\) と補題 P から **\(N_3\) の等号は成立**する。`kerchi_equality_v1.md` の \(N_3\)=UNKNOWN は既に stale である。\(M_3\) は合成位数の核であり、引き続き UNKNOWN。

### F79-2.6 — TIER-1.5 は PASS

\[
\mathfrak F_0''\ne1
\quad\Longrightarrow\quad
G_N''\ne1
\]
だから、\(\ker\widetilde\chi\) の導来長が 3 以上なら \(G_N\) は非 metabelian である。等号仮定は不要である。名称は意味を直接表す

```text
KERNEL-DL3 / KERNEL-NONMETABELIAN
```

を併記するのが安全である。

---

## 3. I-23 と定理 CASC

### F79-3.1 — K1・K3・K4

いずれも PASS。

- K1 は
  \[
  [a]\mapsto1\ {\rm in}\ L^\times/L^{\times2}
  \iff K(\sqrt a)\subseteq L
  \]
  という直接の同定で、巡回性を要しない。Galois の場合の
  \(\ker\cong\operatorname{Hom}(G,\{\pm1\})\) も正しい。後者と
  \(G^{\rm ab}/(G^{\rm ab})^2\) の同型は有限 \(\mathbf F_2\)-空間としての非標準同型、と注記するとより正確である。
- \(d,m\) が奇で互いに素なら \(\gcd(d,4m)=1\) なので、
  \[
  \operatorname{Gal}(F_{dm}/F_m)\cong(\mathbf Z/d)^\times .
  \]
  その二次 characters は \(d\) の相異なる素因数ごとに一つである。\(i\in F_m\) により \(p^*\) の符号は平方類で消え、
  \[
  E_d=\langle[p]:p\mid d\rangle
  \]
  となる。従って \(E_d\) は \(\operatorname{rad}(d)\) のみの関数である。
- K4 の conductor–discriminant 論証により、\(p\nmid2m\) の素数類は独立である。

### F79-3.2 — CASC は前件つき定理として PASS

K4 で得た共通基底に関して \(E_d\) は座標部分空間なので、
\[
\bigcap_{d\in\mathcal D}E_d
=
\left\langle[p]:p\in\bigcap_{d\in\mathcal D}P(d)\right\rangle
=E_{\gcd(\mathcal D)}.
\]
従って
\[
\bigcap E_d=\{1\}\iff\gcd(\mathcal D)=1
\]
は正しい。\(d=9\) が \(d=3\) より歯を増やさないことも、\(u_9\) に触れず
\(E_9=E_3\) から従う。

補題 INV も正しい。体自己同型は平方部分群を保ち、\(\lambda\in\mathbf Q^\times\) を固定するので、合理的に定義された SQ 述語は Galois 共役で変わらない。従って C1′ の脅威を「自己同型で結ばれない曖昧性」に限定できる。

### F79-3.3 — 梃子率の scope

「第 2 の歯 \(q=7\) で全標的一斉閉鎖」は、次の限定つきなら正しい。

1. \(d=7\) 自身について U3、すなわち \([u_7]_2=1\) が公開測定または証明で得られる。
2. 各標的 \(m\) は \(\gcd(m,21)=1\)。
3. 各 \(m\) ごとに A7@\((3m)\)、A7@\((7m)\)、C1′、C5 が閉じる。

このとき \(E_3\cap E_7=E_1=\{1\}\) なので、その**限定された標的集合**に対する第 3 の歯の限界価値はゼロである。\(3\mid m\) または \(7\mid m\) の標的まで閉じるという意味ではない。

現時点で q=7 は preregistered candidate であり、本便は測定許可を出さない。特に A7 の composite-window instance と C1′/C5 は UNKNOWN のままである。CASC は paper-proof candidate として採用できるが、運用上無条件に発火できる定理ではない。

---

## 4. 修理完了 4 件 — FAIL/NOTE 二段判定

### FAIL 層

#### F79-4.1 — I-24 の解釈

証明書が示したことは次である。

- \(H_{2,1,0}\) と \(H_{3,1,0}\) は \(P_3\) 内で共役でない。
- それぞれの次数 6 表現について、独立生成対 \((X,Y)\) と \((X,Z)\) は \(S_6\) 内で同時共役である。

後者は branch label \(1\leftrightarrow\infty\) を交換する Nielsen/\(S_3\)-relabeling であり、標識付き dessin の同値ではない。従って

> 同一 dessin の別表示 \(\Longrightarrow u\) または SQ 述語は \(j\) 盲目

という帰結は現証明書からは出ない。C1′ はまだ完全には閉じていない。

修理には、枝値交換に対応する基底 Möbius 変換、選んだ cusp の局所座標、および主係数 \(u\) の変換則を一つの typed certificate にする必要がある。今回の交換が \(t\mapsto t/(t-1)\) 型なら 0 での一次係数は \(-1\) で、\(-1\) は \(i\in F_m\) により平方であるため SQ 不変性を救える可能性がある。しかし、その同定は現在の JSON には入っていない。

#### F79-4.2 — Q-A の定理化

`qa_orbit_count_20260729.json` は

- \(n=3\): marking 12 個、作用像位数 2、6 軌道すべてサイズ 2。
- \(n=5\): marking 96 個、作用像位数 4、24 軌道すべてサイズ 4。

を報告する。これは有用な初観測だが、単一 GAP レーンの二標本であり、Galois 作用や族的一般則は示さない。「GT の marking 作用は常に極小商を経由する」という定理への格上げは FAIL。

### NOTE 層

#### F79-4.3 — derived census v2

**NOTE（修理受理）。** 5 欄分離、本体と像の導来長の分離、\(N_Q/N_2\) の本体導来長 1、method(A) 12 対象の \(\theta\)-kernel count 1、L/M5 の `injectivity_information: none` を確認した。v1 の欄混同は解消している。

ただしこれは同一 GAP スクリプト由来の一レーン artifact であり、全欄を cross-checked と呼ばない。特に L/M5 から \(\Phi/\Theta\) の忠実性を読み取ってはならない。

#### F79-4.4 — 複素共役 fixture v3

**NOTE（常設 fixture として受理）。** 紙面正規形 \(a\cdot q\)、GAP raw product、`X^g` の対応を明示し、

- 本体軸: \(\mathrm{dv}_1=+1\)。
- 非対合軸: native conjugator が \(h\) であって \(h^{-1}\) でない。
- 人工軸: \(q_1,q_2,q_3\) による係数変換。

を \(n=3,5,7,9,11\) で exact に検査している。「対合性 canary が \(h\leftrightarrow h^{-1}\) を見分けられず、その盲点が元の符号事故と同根」という教材化も妥当である。

第三軸は実 shadow ではなく**規約変換用 synthetic fixture**なので、常にそのラベルを残すこと。計算 provenance は一つの GAP lineage であり、paper proof の併記は数学的裏づけだが機械的な第二レーンではない。

#### F79-4.5 — 規約辞書 W

**NOTE（内容承認、正本統合は未発効）。**

- (W-\*) は既存 W-1 と同じなので独立番号を与えず、W-1 の実装注へ吸収する。
- (W-^) を W-5、(W-nf) を W-6 として採る案に賛成する。
- (W-perm) は語規約と適用対象が異なるので W-7 として独立させ、各外部資料の関数合成規約を必ず併記する。

現ファイル自身が `candidate` と記しており、`docs/week1-定義ノート.md` にはまだ統合されていない。従って「定義ノートを延長済み」ではなく「延長案をゲート通過」と記録するのが正しい。

---

## 5. WCP5-D — \(\tau\) の \(c\)-落とし

### F79-5.1 — \(\operatorname{Ad}(\delta)\) の \(c\) 項は PASS

\[
\Delta=\sigma_1\sigma_2\sigma_1,\quad
\delta=\sigma_1\sigma_2,\quad
c=\Delta^2,\quad x=\sigma_1^2,\quad y=\sigma_2^2,\quad z=(xy)^{-1}
\]
とする。\(B_3=\langle a,b\mid a^2=b^3\rangle\)、\(a=\Delta,b=\delta\) を使うノートの計算を追跡し、
\[
\operatorname{Ad}(\Delta):x\mapsto y,\ y\mapsto x,
\qquad
\operatorname{Ad}(\delta):x\mapsto y,\ y\mapsto zc
\]
を確認した。論文の自由群 automorphism
\[
\tau:x\mapsto y,\quad y\mapsto z
\]
は、braid 共役 \(\operatorname{Ad}(\delta)\) の中心成分を落としたもの、という診断で正しい。

従って \(A=PB_3/N\) 上の常に定義された
\(\widetilde\tau=\operatorname{Ad}(\delta)\) について
\[
\widetilde\tau(\bar w)=\overline{\tau(w)}c^{e_y(w)},\qquad
\widetilde\tau^2(\bar w)=\overline{\tau^2(w)}c^{e_x(w)}
\]
および
\[
R_{\widetilde\tau}(m,\bar f)
=R_{\rm naive}(y^mw)c^{m+e_x(w)+e_y(w)}
\tag{5.1}
\]
も正しい。

### F79-5.2 — (F2) と Prop. 3.4 の解析的同値は閉じる

正典 PDF の Prop. 3.4（p.12）の数式画像を確認した。命題は**実際の語**
\[
(m,w)\in\mathbf Z\times[F_2,F_2]
\]
に対し、full hexagon (3.3)(3.4) と
\[
w\theta(w)\in N_{F_2},\qquad
\tau^2(y^mw)\tau(y^mw)y^mw\in N_{F_2}
\tag{3.10--3.11}
\]
の同値を述べる。

charming な剰余類 \(\bar f\in[F_2/N_{F_2},F_2/N_{F_2}]\) には必ず
\(w\in[F_2,F_2]\) の lift がある。これを選べば
\[
e_x(w)=e_y(w)=0.
\]
\(\operatorname{Ad}(\Delta)\) には中心補正がなく、(5.1) は
\[
R_{\widetilde\tau}(m,\bar f)=R_{\rm naive}(y^mw)c^m
\]
となる。従って (3.10)(3.11) はちょうど
\[
\bar f\,\widetilde\theta(\bar f)=1,\qquad
R_{\widetilde\tau}(m,\bar f)=c^m
\]
に等価である。全射条件を足せば、ノートの **(F2) 商規律は full hexagon + surjectivity と解析的に同値**である。GAP 二標本一致に依存せず、Prop. 3.4 から紙上で閉じた。

### F79-5.3 — (F1) は差戻し

ノートの
\[
e(w):=e_x(w)+e_y(w)\equiv0
\pmod{\operatorname{ord}(c\bmod N)}
\]
は (5.1) の余分な中心因子を消す条件ではあるが、Prop. 3.4 の仮定
\(w\in[F_2,F_2]\) を保証しない。例えば \(e_x=1,e_y=-1\) なら総和は 0 だが、その語は自由群の交換子部分群に属さない。

従って普遍的に安全な (F1) は次である。

> \(\bar f\) の代表として、実際の commutator lift
> \(w\in[F_2,F_2]\)、すなわち \(e_x(w)=e_y(w)=0\) を選ぶ。

`w*x^5` が特定窓で FULL と一致したことは有用な witness だが、「総指数の合同だけで常に十分」の証明にはならない。実装の正典は代表選択を不要にする (F2) とすべきである。

### F79-5.4 — \(\tau\) 非降下と誤答の論理方向

三つの主張を分ける必要がある。

1. **\(\tau\) が商へ降りない \(\Rightarrow\) 旧語手続きは shadow 座標の関数でない:** PASS。代表を変えると値が変わり得る。
2. **\(\tau\) が商へ降りない \(\Rightarrow\) 固定した BFS section の最終数値が必ず FULL と不一致:** 一般には偽／少なくとも従わない。section が偶然正答することはあり得る。
3. **\(\tau\) が商へ降りる \(\Rightarrow\) 正しく実装された Prop. 3.4 手続きは代表非依存で正答:** PASS。従って、他の実装欠陥がないという条件下では「数値誤答 \(\Rightarrow\tau\) 非降下」という対偶診断を使える。他のバグも許す実運用では、この逆向きは単独の原因同定器にはならない。

従って永久記録は「非降下は**不良定義**の十分条件」とし、「必ず数値誤答」とは書かないのがよい。

### F79-5.5 — W-C-p5 の群同定は source gate で FAIL

`wcp5d_resolution_v1.md` 自身の GAP-4 が認めるとおり、40 個の formal candidates について source kernel/settled を測っていない。full hexagon と全射は
\[
B_3\longrightarrow B_3/N
\]
の source が \(N\) であることを含意しない。形式 (3.53) が 40 個の表を閉じても、groupoid の source/target が合っていなければ isotropy group の合成証明にはならない。

従って現在採用できる記述は

> W-C-p5 target に対する 40 個の full-hexagon shadow candidate は、形式合成表として \(C_2\times\operatorname{Aff}(\mathbf F_5)\) 型を示す。

までである。全候補に

```text
source_kernel_digest
settled = (source_kernel == target_kernel)
```

を付け、40/40 settled を確認して初めて
\(GTSh(N,N)\cong C_2\times\operatorname{Aff}(\mathbf F_5)\) と格上げできる。従って現段階では metabelian、\(|\ker\widetilde\chi|=5\)、D1 壁不突破も isotropy 群の結論としては UNKNOWN。

また、この congruence kernel を \(N_5\) と呼ぶと、既存の
\(\ker(\beta_5:B_3\to S_3\times C_5)\) の \(N_5\) と衝突する。
\[
N^{\rm cong}_5\quad\text{または}\quad N_{\rm WCP5}
\]
へ即時改名すべきである。

### F79-5.6 — provenance 判定

`search/wcp5d-verify.g` の digest とソースは確認した。同一 GAP script 内の「full predicate と (F2) predicate の一致」は internal dual check であり、helper 非共有の Node/Python レーンとの一致ではないため、工房の序列上 **cross-checked とは呼べない**。ただし F79-5.2 の紙上証明により、二述語の数学的同値自体は機械一致より強く閉じた。

指定 wrapper

```powershell
.\gap.ps1 search\wcp5d-verify.g
```

で再実行を試みたが、このセッションでは GAP 起動時に

```text
fatal error - couldn't create signal pipe, Win32 error 5
```

となり、fresh な `FAILS = 0` は取得できなかった。従って 66/66、1600/1600、二標本の個数値は受領 artifact の single-GAP result として扱い、再実行済みとはしない。

既存 miner の `c_in_N=false` 17 行は (F2) で再計算するまで UNKNOWN、という差戻しに賛成する。

---

## 6. ★教材として常設すべき事項

1. **pro-\(\mathcal C\) は位相語である。** 閉部分群／連続有限商には遺伝しても、抽象部分群の抽象有限商には遺伝しない。
2. **character の target order と image order を混同しない。** 全射定理が typed でない限り、個数式の分母は \(\varphi(2N_{\rm ord})\) ではなく実像 \(|Q_N|\) である。
3. **素数核は反例除外器ではない。** 等号問題を「群が可換か」の一ビットへ還元するだけである。
4. **枝値 relabeling と同一の標識付き dessin は別物である。** 局所不変量を運ぶには基底 Möbius 変換と局所座標の transport が要る。
5. **自由群の仮定は語そのものへ課す。** 総指数の合同は \(w\in[F_2,F_2]\) の代用にならない。代表に依らない商内式があるなら、それを正典実装にする。
6. **full target shadow の集合と isotropy group は別物である。** source kernel を確定する前に群構造・導来列・壁判定を宣言しない。
7. **canary 自身の対称性を監査する。** 対合性検査は \(h\) と \(h^{-1}\) を区別できず、ちょうど符号事故を見逃し得る。

---

## 7. 共同設計者提案（常設）

### P79-A — character registry

証明書に次を分離して常設する。

```text
canonical_character_modulus = N_ord
refined_character_modulus   = 2*N_ord
chi_image_order
chi_surjective_status = PROVED | CROSS_CHECKED_WINDOW | UNKNOWN
chi_surjective_evidence_digest
is_isolated
```

普遍個数 assert は実像位数で行い、\(\varphi(2N_{\rm ord})\) は全射 gate 後だけ使う。

### P79-B — equality ladder v2

1. \(|\ker\chi|=1\): 等号 PASS。
2. \(|\ker\chi|=p\): 可換性を一ビット測定し、補題 P を適用。探索から除外しない。
3. \(\ker\chi\) の導来長 \(\ge3\): `KERNEL-DL3` で非 metabelian PASS。
4. 合成位数核: LHS coker／余不変量／transgression を計算。

### P79-C — WCP 列挙順序

1. (F2) で target shadow candidates を列挙。
2. 各候補の source kernel を証明書化。
3. settled な候補だけで isotropy group を作る。
4. そこで初めて (3.53)、導来列、\(\widetilde\chi\) を計算。
5. 独立 Node/Python レーンは GAP の候補 helper を共有せず、full hexagon、source kernel、合成表を再構成する。

### P79-D — CASC tooth ledger

歯 \(d\) ごと、標的 \(m\) ごとに

```text
U1 arithmetic
A7@(dm,d)
A7@(dm,m)
U3 square-class provenance
U4 window identity
C1prime
C5
```

を行列化する。「歯 \(d\) を取得」と「全標的に使用可能」を別状態にする。

### P79-E — relabel transport capsule

I-24 型の主張には

```text
source ordered triple
target ordered triple
branch permutation in S3
base Mobius transform
chosen cusp/local parameter
leading-coefficient transport factor
square-class effect
```

を一体化した certificate を要求する。これで「unlabelled 同型」から「SQ 述語不変」への飛躍を防げる。

---

## 8. digest 検証

PowerShell の `Get-FileHash -Algorithm SHA256` で照合し、指定された 13 件はすべて一致した。

```text
OK  c613f5820d17c897a962177524df44010a3f55677fc815ee800a0150476208ba  docs/notes/wexist_check_v1.md
OK  f764c2d4dec490180401e8d1941ae57bf25cff3e84b3bd5704af2b5618198d16  docs/notes/kerchi_equality_v1.md
OK  08eec1a7eac8595614b0b6242c17a34c3cf98c30f5c2b72b4080cd9f619b90cc  search/certs/ke_a_normality_20260729.json
OK  bbcc5bf058069dff9154a067a4fee27880c50e4585744a6cafe24a0f52f9ea26  search/kerchi-abelianization-check.py
OK  0e0b3adc439a406e42a0507fb63a09de87c5d93a647528e5f3f6b5fc43b68136  docs/notes/i23_cascade_lemma_v1.md
OK  d30ac11505eb4d46230d4f8b195ddc4888fd3e2bbabe96f265aaeeed9167e983  search/certs/derived_census_v2_20260729.json
OK  65dece56016a2d38023190b6e6c9eb4c365e4341e349a9307f6653fff711de8d  docs/notes/sgn_c_resolution_v1.md
OK  bd7819129c3db3e66a79c646ea0c7c473dc68d7d1894c4cc215cb9ed4c87925e  search/certs/ihc_fixture_v3_20260729.json
OK  be0f1249c24d2861636b9491dd45a8c731f8ddae782f886eab34e4b8585fc58c  docs/notes/convention_dictionary_W_v1.md
OK  9a1fe84c22d6b3eff4bf79bdff874e867f6930ebce4c57f48ccfd21d7106caa3  search/certs/i24_u3_recheck_20260729.json
OK  23e7d3e6d998a7a06f96529332b17cab48b89f4e65dbf17aef075130eb1df561  search/certs/qa_orbit_count_20260729.json
OK  eb789793a3107269b93cc3575d47063c30799eba9d336fb38b638c2a814d341a  docs/notes/wcp5d_resolution_v1.md
OK  a5d4fc60cd3221e0badbffb176d270d732a57514602a372d6d25810dd1413707  search/wcp5d-verify.g
```

証明書内に記録された生成 script digest も現物と一致した。

```text
OK  d65547534b86c8efbd5b964c1dd835b17a509197b4d5bb094d839fdb60415662  search/derived-census-v2.g
OK  964e15030bd1c808ece190523c363b78ac13cd8e7859f5cd9acdf09f94e697da  search/ihc-fixture-v3.g
OK  3796e4c2b23259c2b5b45b0b7b8e4fb575d78468c3d5c7b6f7c0a60f6ad8c731  search/i24-u3-recheck.g
OK  b63898d9f0e15e03e3cff97ba3a70bd19c2aedebd731f4637e3baf2452913715  search/qa-orbit-count.g
```

---

## 9. 監査範囲

- 便 79 の §0 から §6 まで全文、対話帳 T-17 までの新着、指定ノート 6 件、JSON 6 件、Python/GAP script 5 件、および関連する定義ノートを読んだ。
- `search/kerchi-abelianization-check.py` は再実行し、18 窓の全行と唯一の反例 L01 を再現した。
- 正典 `papers/2401.06870-gt-shadows-gentle-version.pdf` p.12 をページ画像化し、Prop. 3.4 の仮定 \(f\in[F_2,F_2]\) と式 (3.10)(3.11) を画像で照合した。
- WCP GAP script は指定 wrapper からの起動が Win32 signal-pipe error で失敗したため、fresh run は未取得。受領 JSON/ノートの計算値を独立再計算したとは主張しない。
- Lean 化、q=7 の値測定、17 miner 窓の再採掘、W-C-p5 の source-kernel 計算、I-24 の局所係数 transport は行っていない。
- §6 の次便予告（壁宇宙 v1.3、掃引、EP record、W-A 再採掘）は監査対象外。
- 変更した作業ツリー上のファイルは本返信 `sol/sol_reply_79_math6.md` のみである。
