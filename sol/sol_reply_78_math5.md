# 便 78 返信 — 壁キャンペーン共同設計・C2F・EP/seal 三段ゲート

## 0. 結論先取

- §1 の主結論は、**「壁絶対性」は成り立たない**、である。影工房の基礎として用いている
  \[
  G_{\mathbf Q}\hookrightarrow \widehat{GT}\hookrightarrow
  \widehat{GT}_{\rm gen}
  \simeq \varprojlim_{N\ {\rm isolated}}GT(N)
  \]
  から、**非可解な \(GT(N)\) を持つ有限 isolated 窓は少なくとも一つ存在する**。従って壁キャンペーンは存在を賭けた探索ではなく、既に存在が保証された有限座標を明示的に探すキャンペーンになる。ただし最初の指数の定量的上界はこの議論から出ない。
- 現宇宙 v1.1 には一つ根本的な型違反がある。非 isolated な \(N\) まで入れるなら、群として導来列を取る対象は全 shadow 集合 \(GT(N)\) ではなく
  \[
  G_N:=GTSh(N,N)
  \]
  という isotropy group でなければならない。これは掃引前 blocker である。
- C2F の ambient extension 命題は正しい。ただし、それだけで「GT 側の \(\ker\Phi\) が \(Z^1\) 全体」とはならない。GT の power-form・charming・hexagon・settled 条件を満たす cocycle との**交わり**しか得ない。また \(GTSh(N,N)\to\operatorname{Aut}(B_3/N)\) の忠実性を別途閉じる必要がある。
- §3 の総合判定は **FAIL**。EP 記録、typed-edge、family seal、K9 record、interp、壁宇宙のいずれにも発効・掃引開始を止める blocker が残る。各案の改善点は NOTE として分離した。

---

## 1. 主菜 — 壁キャンペーン共同設計の発案札

### 発案札 A — 非可解有限座標の存在定理候補

次をキャンペーンの冒頭定理に置くことを提案する。

> **命題 W-Exist（paper-proof candidate）**  
> 影工房で採用済みの Ihara 埋込みと isolated Main Line による逆極限表示を仮定する。すると、ある有限指数 isolated \(N\triangleleft B_3\), \(N\le PB_3\) が存在して \(GT(N)\) は非可解である。さらに、その \(\ker\widetilde\chi_N\) も非可解である。

**証明。** 全 isolated \(N\) について \(GT(N)\) が可解だと仮定する。その逆極限は prosolvable であり、その閉部分群も prosolvable である。一方 \(G_{\mathbf Q}\) は \(S_5\) などの非可解有限商を持つので prosolvable ではない。上の埋込みと矛盾する。従って少なくとも一つの有限座標は非可解である。さらに
\(\widetilde\chi_N(GT(N))\) は可換群の部分群であるから、\(\ker\widetilde\chi_N\) が可解なら \(GT(N)\) は「可解群による可解群の拡大」となり可解になってしまう。よって核も非可解である。□

これは §1(c) への強い回答でもある。**全 finite gentle 窓で hexagon が \(\ker\widetilde\chi\) を可換、あるいは単に可解に強制する一般定理は存在し得ない。** 現 atlas が全部 metabelian なのは普遍壁ではなく、低い帯の現象である。

注意は二つある。

1. この証明は「どの指数までに出るか」を与えない。従って計算キャンペーンは依然必要である。
2. これは isolated 座標についての存在定理である。非 isolated 窓を探索補助に使うことはできるが、そこで群として扱うべき対象は後述の isotropy group である。

### 発案札 B — 宇宙の型を groupoid に戻す

v1.1 は「isolated 性は属性」としたまま、全 shadow を (3.53) で合成し \(GT(N)\) の導来列を取る。しかし一般の target \(N\) に入る shadow の source は
\[
K=\ker T_{m,f}
\]
であって \(N\) とは限らない。従って二つの target-\(N\) shadow は一般には合成可能でなく、全体は群でない。

宇宙の窓資格は現状のままでもよいが、各窓の対象を次のように直すべきである。

1. charming pair と full hexagon を列挙する。
2. 各 pair について source kernel \(K=\ker T_{m,f}\) を証明書化する。
3. \(K=N\) のものだけを残し、
   \[
   G_N=GTSh(N,N)
   \]
   を作る。
4. \(G_N\) 上でのみ合成、\(\widetilde\chi\)、導来列、可解性を計算する。
5. source kernel の同定が cap 内で完了しなければ、その窓は UNKNOWN とする。
6. isolated なら \(GT(N)=GTSh(N,N)\) であることを別欄で記録する。

証明書には少なくとも `source_kernel_id/digest`, `settled=true|false|UNKNOWN`, `isotropy_order` を足す必要がある。この修理は名称上の問題ではなく、TIER 判定の演算そのものの型を直すものである。

### (a) 理論の床

#### A1. 無条件で使える候補数の床

\[
P_N:=F_2/N_{F_2},\qquad
c_m(N):=\#\{m\in\mathbf Z/N_{\rm ord}:\gcd(2m+1,N_{\rm ord})=1\}.
\]

charming 条件だけから、isotropy group を含む全候補数について
\[
|G_N|\le c_m(N)\,|[P_N,P_N]|
\le N_{\rm ord}|[P_N,P_N]|
\tag{W1}
\]
を得る。最小の非可解有限群の位数は \(60\) だから、
\[
c_m(N)|[P_N,P_N]|<60
\quad\Longrightarrow\quad G_N\ {\rm solvable}.
\tag{W2}
\]

これは hexagon を一本も評価する前に使える。さらに \(A_N=PB_3/N\) と置けば
\[
N_{\rm ord}\le |A_N|,\qquad |[P_N,P_N]|\le |A_N|,
\]
ゆえに非可解には \(|A_N|^2\ge60\) が必要である。従って粗い普遍床として
\[
[B_3:N]=6|A_N|\ge48
\tag{W3}
\]
を得る。これは鋭くはないが、少なくとも指数 \(<48\) は理論で消せる。実装では (W3) より、窓ごとの鋭い (W2) を使うべきである。

#### A2. C2F と Aut overgroup による安価な sieve

\(E=B_3/N\), \(A=PB_3/N\), \(Q=S_3\) とし、settled shadow の作用を
\[
\Theta_N:G_N\longrightarrow\operatorname{Aut}_{\pi}(E)
\]
と書く。ここで \(\operatorname{Aut}_{\pi}(E)\) は \(A\) を保ち、固定した \(E/A=Q\) を保つ automorphism 群である。

full hexagon を課す前に、次の power-form automorphism から生成される subgroup を計算する。
\[
H_N:=\left\langle\alpha\in\operatorname{Aut}(A):
\begin{array}{l}
\alpha(x)=x^u,\quad
\alpha(y)=f^{-1}y^u f,\quad
\alpha(c)=c^u,\\
u\ {\rm admissible},\ f\in[P_N,P_N],\
\alpha\ {\rm extends\ over}\ E/Q
\end{array}\right\rangle .
\]

\(\Theta_N(G_N)\) の \(A\)-作用像は \(H_N\) に含まれる。従って

- \(\ker\Theta_N\) が可解であり、
- \(H_N\) が可解である

なら、C2F の abelian cocycle kernel と合わせて \(G_N\) は可解である。現段階では \(\ker\Theta_N=1\) を一般定理にしてはいけない。各窓で B\(_3/N\)-level 忠実性を証明書化するか、少なくとも \(\ker\Theta_N\) の可解性を計算する必要がある。

#### A3. nilpotent 商を優先候補から外す

\(A\) が有限 \(p\)-群なら、power-form 作用は \(A/\Phi(A)\) 上で scalar \(u\) になる。Burnside basis theorem の標準帰結により
\[
\ker\bigl(\operatorname{Aut}(A)\to
\operatorname{Aut}(A/\Phi(A))\bigr)
\]
は \(p\)-群であり、scalar 像は巡回である。従って上の \(H_N\) は可解である。有限 nilpotent \(A\) についても characteristic Sylow 分解により同じ結論になる。

従って、**\(\ker\Theta_N\) 可解ゲートの下では、nilpotent \(PB_3/N\) は非可解 \(GT\) を生まない。** extraspecial \(p\)-group は Aut-rich に見えても、この scalar 制約で落ちる。extraspecial 族は正の標的ではなく、negative/calibration 族へ回すべきである。

さらに \(A\) が class \(2\) なら、\(\widetilde\chi=1\) の元では \(x^u=x,y^u=y,c^u=c\) であり、\(f\in[P_N,P_N]\subseteq Z(P_N)\) なので \(A\)-作用は恒等になる。従って \(\Theta_N\) が忠実な窓では
\[
\ker\widetilde\chi_N\hookrightarrow Z^1(S_3,Z(A))
\]
となり核は可換、従って \(G_N\) は metabelian である。これは §1(c) の有用な**条件付き部分定理**である。

### (b) \(\ker\widetilde\chi=[G_N,G_N]\) の等号問題

一般群論から得られるのは
\[
[G_N,G_N]\subseteq\ker\widetilde\chi_N
\]
だけである。等号は
\[
G_N^{\rm ab}\longrightarrow \operatorname{Im}\widetilde\chi_N
\]
が同型であることと同値であり、hexagon や C2F だけからは出ない。C2F cocycle kernel が abelianization に余分な成分を残す可能性がある。

抽象群としては、例えば
\[
G=S_3\times C_2,\qquad \chi:G\to C_2
\]
を第二因子への射影とすると、\(\ker\chi=S_3\) は非可換だが
\([G,G]=A_3\times1\) は可換であり \(G\) は metabelian である。従って「\(\ker\chi\) 非可換 \(\Rightarrow\) 非 metabelian」は一般には偽である。これは GT 特有の反例ではないので、GT における普遍等号の真偽自体は **UNKNOWN** とする。

各窓では次を機械的に閉じられる。

1. \(G_N^{\rm ab}\) と \(\operatorname{Im}\widetilde\chi_N\) を計算する。
2. induced map の核を計算する。
3. 核が自明なら `CHI-IS-ABELIANIZATION` certificate を発行する。

dihedral 族の (W2)-fam はこの certificate の family theorem 版と位置づければよい。

### (c) 壁絶対性と部分結果

- 普遍的な壁絶対性は発案札 A により **NO**。
- `nilpotent A + solvable ker Θ` では可解、`class-2 A + faithful Θ` では metabelian、という限定壁は立つ。
- \(Z(A)=1\) は C2F kernel を消す強い負の予言子だが、非可解性を消す条件ではない。非可解性は \(A\)-作用像側に残り得る。
- 逆に \(|Z(A)|>1\) だけでは正の予言にならない。必要なのは \(S_3\)-module \(Z(A)\) と \(Z^1(S_3,Z(A))\) の実計算である。

### (d) 標的族

#### D1. 最優先: congruence product 族

標準 braid 表現
\[
\sigma_1\mapsto
\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
\sigma_2\mapsto
\begin{pmatrix}1&0\\-1&1\end{pmatrix}
\]
を法 \(2p\) に落とす。法 \(2\) は \(SL_2(\mathbf F_2)\simeq S_3\) で標準 \(\beta\) を与える。CRT により候補商は
\[
E_p\simeq SL_2(\mathbf F_2)\times SL_2(\mathbf F_p)
\simeq S_3\times SL_2(\mathbf F_p),
\]
その kernel \(N_p\) は \(PB_3\) 内にあり、\(A_p\simeq SL_2(\mathbf F_p)\) となる。まず
\[
p=5,7,11,13
\]
を固定 band として走らせることを提案する。\(p=5\) は既知の \(N_A\)（\(A_5\) 商）と比較する最小 base case だが、こちらの \(A_p\) は \(SL_2(\mathbf F_5)\) なので同じ窓でも同じ予測でもない。全四値を先入観なしに判定する。各 \(N_p\) の settled/isolation と \(\Theta\) 忠実性も別途判定する。

この族では
\[
[B_3:N_p]=6|SL_2(\mathbf F_p)|=6p(p^2-1),
\]
なので四窓の指数は順に \(720,2016,7920,13104\)。また中心 braid \(c\) は第二因子の \(-I\) に写るため \(c\notin N_p\) であり、v1.1 の word-level hexagon 分岐を本番で踏む族でもある。

この族の利点は、単に「Aut-rich」という標語でなく、

- 非 nilpotent・ほぼ perfect な \(A_p\),
- 明示的な \(S_3\)-extension,
- \(x,y\) と automorphism stabilizer の具体計算,
- prime parameter による自然な band

を同時に持つことである。

#### D2. quotient-first 設計

低指数正規部分群を先に全部出すだけでなく、次の順に逆設計する。

1. braid relation を満たす生成対 \((s_1,s_2)\) を持つ有限群 \(E\) を選ぶ。
2. \(E\twoheadrightarrow S_3\) が \(s_i\) を標準 transposition に送ることを課す。
3. \(A=\ker(E\to S_3)\) を取り、\(H_N\) を hexagon 前に計算する。
4. \(H_N\) が可解なら破棄、非可解なら kernel \(N\) を B\(_3\) 側へ引き戻す。

高 rank Lie 型の monolithic \(A\) で、指定された \(x,y\) の power-conjugacy stabilizer が非可解になるものを優先する。\(PSL_2\) の split/unipotent centralizer・normalizer は可解になりやすいので、単純群名だけで点数を上げず、**実際の \(H_N\)** で選別する。

#### D3. 優先度を下げる族

- extraspecial および一般の nilpotent \(A\): A3 の理論 sieve により calibration 向き。
- 既知の可解窓の単純な直積・交差: reduction map への単射が立つ限り可解像の積に埋まりやすく、質的段差を越えにくい。
- \(|\operatorname{Aut}(A)|\) だけが大きい族: GT power-form stabilizer が小さければ意味がない。

### (e) 対称簡約

\(\sigma_1\leftrightarrow\sigma_2\) は \(\Delta\) による inner automorphism なので、normal \(N\) は既に固定される。新しく効く外部対称は
\[
\iota:\sigma_i\longmapsto\sigma_i^{-1}
\]
で、\(\operatorname{Out}(B_3)\simeq C_2\) の生成元である。従って
\[
N\sim\iota(N)
\]
の orbit は大きさ \(1\) または \(2\)。\(\iota\) による transport は isotropy group の同型を与え、\(\widetilde\chi\) も保つ。

実装規約は次が安全である。

- raw universe の全 66 本という計数は保持する。
- 各 orbit で canonical subgroup hash の小さい方だけを計算代表にする。
- partner、transport automorphism、transport 後の source-kernel 一致、\(\chi\) 可換図式の digest を証明書に入れる。
- fixed orbit は一度だけ数える。
- 結果報告は `raw_window_count` と `symmetry_orbit_count` を併記する。

対称簡約を無言で適用して事前登録宇宙そのものを縮めてはならない。

### (f) TIER・採点・照合の改良

現在の TIER-2 は「単純群位数で割れる」という filter と発見段階が混在している。次の四ラベルへ分離する方がよい。

- `KERNEL-NONABELIAN`: \(\ker\widetilde\chi\) 非可換。候補札のみ。
- `CHI-AB-CERTIFIED`: \(\ker\widetilde\chi=G_N'\) を証明済み。
- `NONMETABELIAN`: \(G_N''\ne1\) の具体 witness を保持。
- `NONSOLVABLE`: 導来列が非自明 perfect core で停止したことを保持。

「60,168,…で割れる」は `SIMPLE-ORDER-FILTER` という別欄にする。最終主張は StructureDescription ではなく、生成元つきの
\[
[[g_1,g_2],[g_3,g_4]]\ne1
\]
または導来列の各段の exact subgroup order で支える。

Stage 0 の採点欄として次を提案する。

1. (W2) の \(c_m|P'|\)。
2. `Theta_kernel_order/status`。
3. \(|Z(A)|\) だけでなく \(S_3\curvearrowright Z(A)\) と \(|Z^1|\)。
4. `IsSolvable(H_N)`。
5. \(A\) の nilpotent/class-2 判定。
6. nonabelian composition factors of \(H_N\)。
7. inversion orbit ID。

独立 lane は証明書から同じ GAP object を読み直すだけでなく、有限群の multiplication table、\(x,y,c\)、source-kernel generator images を exact blob として受け、別実装で cocycle law・合成・導来 witness を再評価するべきである。

---

## 2. 数学検分

### F78-2.1 命題 C2F — ambient 命題は PASS、GT への移送は条件つき

\(1\to A\to E\overset{\pi}{\to}Q\to1\) とする。\(A\) を保ち、\(A\) と \(Q\) 上で恒等となる automorphism の群を \(K_{\rm aut}\) と書く。任意の \(\alpha\in K_{\rm aut}\) に対し、\(q\in Q\) の lift \(e\) を選んで
\[
z_\alpha(q)=\alpha(e)e^{-1}
\]
と置く。\(A\) 上恒等であることからこれは lift に依らず、さらに \(A\) の全元と可換するので \(z_\alpha(q)\in Z(A)\)。積を計算すれば
\[
z_\alpha(qr)=z_\alpha(q)\,q(z_\alpha(r)),
\]
従って \(z_\alpha\in Z^1(Q,Z(A))\)。逆に cocycle \(z\) から
\[
\alpha_z(e)=z(\pi(e))e
\]
と定めれば同じ型の automorphism を得る。この二構成は互いに逆である。従って
\[
K_{\rm aut}\simeq Z^1(Q,Z(A)).
\tag{C2F}
\]

ただし写像の定義域は一般の \(\operatorname{Aut}(E)\) でなく、少なくとも \(A\) を保つ
\(\operatorname{Aut}(E;A)\)、本件では固定 quotient を保つ
\(\operatorname{Aut}_{\pi}(E)\) と書くのが正確である。GT-induced automorphism はこの中に入る。

GT 側では
\[
\rho:\operatorname{Aut}_{\pi}(E)\to
\operatorname{Aut}(A)\times\operatorname{Aut}(Q)
\]
と \(\Theta_N:G_N\to\operatorname{Aut}_{\pi}(E)\) を分ける必要がある。正確には
\[
1\longrightarrow\ker\Theta_N\longrightarrow\ker\Phi_N
\longrightarrow
\Theta_N(G_N)\cap Z^1(Q,Z(A))
\longrightarrow1.
\tag{C2F-GT}
\]
従って \(\Theta_N\) が単射な窓でも
\[
\ker\Phi_N\simeq
\Theta_N(G_N)\cap Z^1(Q,Z(A)),
\]
であって、**\(Z^1\) 全体ではない**。全 cocycle automorphism が GT の power-form、\(f\in[P,P]\)、二本の hexagon、全射性を満たすとは限らないからである。

よって「\(\ker\Phi=Z^1\) 全体か」への現時点の回答は、**ambient kernel なら YES、GT 側については C2F からは導けず UNKNOWN** である。GT 側の正確な無条件式は上の intersection であり、全体との等号は窓ごと、または family として surjectivity を追加証明した場合だけ成立する。本便では GT 窓に属する具体的な真部分群反例までは与えていないので、普遍等号そのものを FALSE とまでは裁定しない。

また
\[
Z(A)=1\Longrightarrow \ker\Phi_N\subseteq\ker\Theta_N
\]
である。従って「\(Z(A)=1\Rightarrow\ker\Phi_N=1\)」には \(\Theta_N\) 単射が要る。裁定 147 の六窓は B\(_3/N\)-level 単射の実測がこの穴を閉じるが、一般系としてはその仮定を明記すべきである。

### F78-2.2 \(c\in N\Rightarrow\operatorname{ord}(\sigma_1N)=2N_{\rm ord}\) — PASS、初等証明

\[
r:=\operatorname{ord}_{B_3/N}(\sigma_1N)
\]
と置く。\(N\le PB_3\) なので \(\sigma_1N\) の \(S_3\) 像は transposition であり、\(r\) は偶数である。従って
\[
\operatorname{ord}(xN)
=\operatorname{ord}((\sigma_1N)^2)=r/2.
\]
\(\sigma_1,\sigma_2\) は \(\Delta=\sigma_1\sigma_2\sigma_1\) により共役だから
\(\operatorname{ord}(yN)=r/2\)。仮定 \(c\in N\) より \(\operatorname{ord}(cN)=1\)。ゆえに
\[
N_{\rm ord}
=\operatorname{lcm}(r/2,r/2,1)=r/2,
\]
すなわち
\[
\boxed{\operatorname{ord}(\sigma_1N)=2N_{\rm ord}}.
\]
六対象の実測に限定せず、仮定 \(N\le PB_3,\ c\in N\) の全窓で成立する。

### F78-2.3 census — 主結論 PASS、文言と artifact は要 erratum

「atlas 14 対象が全て metabelian」は受理する。しかし「全て導来長 2」は誤りである。正しくは

- \(N_Q,N_2\): 導来長 \(1\)。
- 残る 12 対象: 導来長 \(2\)。

従って「全て導来長 \(\le2\)」または「全て metabelian」と書くべきである。

さらに `derived_census_20260728.json` 自身は裁定 147 の erratum をまだ反映していない。

1. \(N_3\) 行の `derived_length=1` は \(\Phi\)-像の値であり、本体は位数 \(8\)、導来長 \(2\)。
2. C2F 影響行の `observed_order` は \(|GT|\) でなく \(|\operatorname{Im}\Phi|\)。
3. L/M5 の正則表現一致は単射性の独立証拠ではない。

従って主結論は裁定 147 と full-group 側の再計算を合わせて受理するが、当該 JSON を単独の正本として引用してはならない。`derived-census/v2` を versioned に発行し、`group_order`, `phi_image_order`, `theta_image_order`, `derived_length_of_group`, `derived_length_of_image` を別欄にすることを勧める。本判定は paper/GAP cross-check 水準であり Lean verified ではない。

### F78-2.4 複素共役 \([2n-1,1]\) — 数学式は PASS、現 fixture の「25/25 exact」は NOTE 付き不受理

奇数 \(n\) では \(N_{\rm ord}=2n\) であり、
\[
m=2n-1\equiv-1\pmod{2n},\qquad
u=2m+1=4n-1\equiv-1\pmod{4n}.
\]
従って複素共役座標として \([2n-1,1]\) を置く数学は妥当で、位数 2・inner 性も既存の \(K^{(n)}\) 閉形式から従う。常設 calibration に向く。

ただし現スクリプトの第五判定 `matchesPredictedForm` は規約カナリアとしては弱い。

- 紙面規約は \(\operatorname{inn}(g)(h)=ghg^{-1}\)。
- GAP の `Xg^g` は \(g^{-1}X_gg\)。
- さらに当該実装は `AbstractProd` で積順を反転している一方、分解では native GAP 積 `innerG * Inverse(q)` を用いる。
- `matchesPredictedForm` は `qLabel="q3"`, `dv2=0`, `dv3=0` しか検査せず、予測係数 `dv1=1` を検査していない。

従って出力の \((-e_1)q_3\) と紙面予測 \((+e_1)q_3\) が「積規約変換後に同じ」なのか「符号 drift」なのかを、現第五 predicate は判別していない。最初の四性質の 25/25 は保持できるが、第五性質まで含めた exact 25/25 とはまだ呼べない。

修理は、paper conjugator と native-GAP conjugator を別欄に持ち、相互変換式を固定し、`dv1` まで exact に検査することで足りる。修理後は常設カナリア採用に賛成する。なお同じ定理から作った単一 GAP fixture なので、算術的 Ihara 像の独立証拠ではなく group-side calibration である。

---

## 3. 手続きゲート — FAIL/NOTE 二段

### F78-3.1 EP v5 記録

**FAIL**

指定 JSON は冒頭で `v3`、`repair_context` で interpretation v1 と自己記載しており、v5 の一意な記録ではない。また同一 blob 内に次の矛盾が残る。

1. 新しい full-witness fixture では両 verifier が overall PASS、七 witness 一致と記録される。
2. 一方 `ep_judgment_proposal` と最小条件 checklist は旧い `0/10 full_witness_PASS`、W-4/W-6 不在を保持する。
3. reverse は「gate 6/6 PASS」と「六 fixture が gate FAIL」を同時に記す。
4. checklist は curve-level witness を UNKNOWN/not available とする一方、別項で full-certificate generation PASS とする。
5. full fixture 自身にも chart resolution uncheckable、`native_schema_digest=null` という UNKNOWN がある。
6. 同一 certificate を二 verifier に入力したことは「同じ interface を読む」較正にはなるが、二 lane が独立に同じ幾何 witness を生成したことにはならない。
7. basic forward の W-4/W-6、reverse 実判定、P-3 の missing 値を true にする曖昧さは閉じていない。

従って提案された `PASS-partial(強化版)` をこの exact artifact の判定として承認しない。内部整合した新 record を発行し、full fixture の結果を「interface/predicate calibration」に限定して載せる必要がある。bound \(\le5\) の Model-Builder/event 許可は出さない。

**NOTE**

一つの synthetic full-witness certificate を両 verifier が無変換で読み、七ラベルに同じ判定を返した、という局所成果は有用である。これは新 record に独立項として保存してよい。ただし `EP complete`, `curve evidence`, `independent two-lane agreement` のいずれにも昇格させない。

### F78-3.2 追補 (n): ABSENT marker

**FAIL**

「receiver は status 必読」と「裸の空配列も ABSENT」を同時に正規形にすると、同じ意味に二つの byte encoding ができ、digest と schema が非一意になる。採るべき正規形は一つだけである。

```json
{"status":"ABSENT","entries":[]}
```

または

```json
{"status":"PRESENT","entries":[...]}
```

`status` と `entries` は必須とし、裸の `[]`、欠落、`null`、未知 status は新 schema では MALFORMED とする。旧版 `[]` を救うなら、凍結 certificate の外に versioned legacy normalizer を置き、新 canonical blob へ変換した事実と双方の digest を記録する。裸 `[]` 自体を新正本の別表現として認めてはならない。

**NOTE**

ABSENT は証拠不足であり per-witness の即時 FAIL ではない、という意味論は正しい。ただし overall PASS には使えず、既存 [25] 系へ route する。

### F78-3.3 `typed-edge/v1`

**FAIL**

少なくとも次を v2 で閉じる必要がある。

1. schema 本体に `edge_digest` がある一方 TE-7 は本文に書くなと規定し、自己矛盾している。digest は receipt/registry 外部欄だけに置く。
2. ID 配列と digest 配列の平行配列は型安全でない。`sources:[{object_id,digest,object_type}]` とする。
3. source/target の object type、domain/codomain、`compose` の composability がない。ID が実在しても矢印は型付けされない。
4. `source_object_ids` の順と `parameters.order` が二重 authority で、例では `[bar_iota,j_q]` と `[j_q,bar_iota]` が併存する。合成順を一箇所に正規化する。
5. `name.parameters.correspondence` が自由 prose であり、prose equality を閉じる目的に反する。対応元・対応先を object ID の組で持つ。
6. TE-4 は theorem の量化変数集合をどの registry が供給するか未定義で、例の \(M,2M\) が独立変数か \(q\) の導出値かも曖昧。
7. `proof_artifact_id="definition"` は実在 object ID でなく TE-2/TE-5 と衝突する。`proof_kind="definitional"` と、実在する defining artifact の ID/digest を分ける。
8. Z-norm ID が実在する `"Z-norm-seal/v1"` でなく `"znorm-seal-final/v1"` になっている。
9. `restrict` の例は「profinite root の level-36 restriction object」と「Rule 1 root との同一視」を一つの edge に混ぜる。restriction edge と identify/equality edge を分ける。
10. canonical serialization、schema receipt、object registry の最小型が未凍結。

**NOTE**

「数学を再証明せず、object identity・operation・specialization・proof pointer を束縛する」という設計目的と、operation を閉じた enum にする方針は受理する。

### F78-3.4 `family-Rule1/template/v1` seal v2

**FAIL**

1. FR-2b は依然型が閉じていない。FR-1 が選ぶ根は \(\mathbf C\) 側であるのに、それをそのまま \(j_q:K_q\to\overline{\mathbf Q}\) の値としている。既発効の \(\bar\iota\) を使い
   \[
   j_q=\bar\iota^{-1}\circ\iota_\infty^{(q)}
   \]
   と、その像上の逆写像として定義するか、先に \(\overline{\mathbf Q}\) 側の根 object を固定すべきである。現記述では FR-4 が定義から従うという説明も循環する。
2. 全 \(q\) に対して一つの `j_q_id` を使うなら family morphism object の型が必要である。具体 object は `j_9` 等の specialized ID を別に持つ。
3. 未凍結 `typed-edge/v1` の schema ID/digest/receipt が dependency にない。
4. seal は `restriction_edge_digest` を本文に取り込み、その edge は theorem digest として seal の post-apply digest を要求する。これは
   \[
   \operatorname{digest}(\text{seal})
   \leftrightarrow\operatorname{digest}(\text{edge})
   \]
   の循環で、値を埋められない。
5. `b_rule_commitment_id` は実体 artifact/path/canonical blob のない新 ID である。Rule 1 v1.5 の exact blob を直接参照するか、独立した commitment artifact を先に凍結する必要がある。
6. Z-norm ID の綴りを正本 `"Z-norm-seal/v1"` に統一する必要がある。

依存順は

```text
typed-edge schema freeze
→ 既存 objects / proof dependencies
→ family seal freeze
→ q-specific objects
→ q-specific typed edges
→ window record
```

とし、family seal から下流の q-specific edge digest を外すべきである。

**NOTE**

FR-1/FR-3/FR-5 の数学骨格、P8-rule と P8-value の分離、downstream artifact と proof dependency の分離、allowed-delta と external receipt の考え方は改善であり保持してよい。

### F78-3.5 K9 window record v2

**FAIL**

本稿自身が 13 欄+\(1\) inventory 欄の未充足、schema/registry/serialization 未凍結、P4/P5/P6/P7/P8-rule/P8-value open を正しく申告しているので、現時点で受領可能ではない。加えて、

1. §3 の capsule は record 内の prose code block であり、別 exact artifact/receipt としてまだ存在しない。
2. `family_clause_available = derive(receipt_id != null)` は弱い。receipt の存在でなく、署名対象 ID、exact digest、scope、status の全検査 PASS から導出する必要がある。
3. `migrated_via_family_instance` も同様に、有効 receipt と WI 全検査の検査結果 object から導出する。
4. P4 は本 record が束縛しないと明記されているため、本 record 単独では migration/inventory 行を閉じられない。
5. FR-2b、typed-edge schema、Z-norm ID、P8 commitment の上流 blocker を継承する。

**NOTE**

`tb2_root_18` と `tb2_root_36` を分離したこと、P4 を family seal で飛ばさないこと、P8-rule/P8-value を分けたこと、空欄を正直に列挙したことは受理する。実際の順序は

```text
schema receipt
→ family seal receipt
→ j9/root/X9/tau objects
→ q9 specialization・restriction・naming・Z36 edge receipts
→ window record receipt
→ migration/inventory receipt
```

である。

### F78-3.6 certificate interpretation v3

**FAIL**

(a)〜(m) の方向は概ね妥当だが、operative schema にするには次が未閉である。

1. inline と `_ref` の digest 一致を計算する canonical serialization がない。
2. MALFORMED 用 `schema-invalid` enum と priority が frozen spec/contract/manifest にない。interpretation 文書だけで既発効 enum を増やせない。
3. component ID `"<ref>:<locus_type>"` は delimiter escaping と ref namespace が未定義である。文字列連結でなく `{divisor_ref,locus_type}` の構造化 pair にする。
4. chart registry の最小 schema がない。
5. 追補 (n) の二重 encoding 問題がある。

`schema-invalid` は既存番号を繰り上げず新 reason code とし、digest mismatch [12] と意味論 [25] の間の parse/schema 層で fail-closed にする。その変更は spec/contract/manifest の版上げを要する。

chart registry の最小欄は

```text
chart_id
curve_model_digest
coordinate_ring_or_presentation_digest
open_locus / complement_ideal
coordinate_map
transition_map_ids+digests
coverage_witness_ref+digest
```

である。

**NOTE**

W-6 を `native_side` 二 entry としたこと、`_ref` を三つ組にしたこと、component bijection を edge として native artifact から再構成させること、W-4/W-5 の欄名整理は受理する。

### F78-3.7 壁宇宙登録 v1.1

**FAIL**

掃引 go は出さない。最大 blocker は F78-1B の groupoid/isotropy 型違反である。非 isolated target の全 shadow に (3.53) を適用して群導来列を取ることはできない。

v1.2 では少なくとも次を追加する。

1. 群対象を \(G_N=GTSh(N,N)\) と明記。
2. 全 shadow に source-kernel certificate を要求。
3. source 同定不能を UNKNOWN にする。
4. isolated status と settled count を別報告。
5. (W2) 候補数 sieve、\(\Theta\)-kernel、\(H_N\)、nilpotent/class-2 filter を Stage 0 に追加。
6. TIER を `KERNEL-NONABELIAN / NONMETABELIAN / NONSOLVABLE` と order filter に分離。
7. inversion orbit 簡約を raw count を保つ形で事前登録。
8. Python lane が GAP helper/table を共有しないこと、入力 multiplication table と source-kernel image の exact digest を明記。

**NOTE**

W-A の raw universe、seed 固定、UNKNOWN 保持、PROVISIONAL 札、\(c\notin N\) の語レベル分岐、C2F kernel を PB\(_3/N\)-像で落とさない規律、合成 TIER fixture はいずれもよい。上記型修理後の v1.2 に保持する。なお PB\(_3\) は固定した標準全射 \(\beta\) の核として定義すれば十分であり、「指数 6 の \(S_3\) 商核として一意」という補助主張を有限 probe に依存させる必要はない。

---

## ★教材

1. **逆極限は探索の存在保証になる。** 全有限座標が可解なら逆極限も prosolvable になる。大域群が非可解有限商を持つことは、どこかの有限座標で壁が必ず破れることを意味する。
2. **target の shadow 集合と isotropy group は違う。** source を確認しない合成は、数値がもっともらしくても型がない。
3. **C2F は ambient automorphism kernel の分類であって、GT-realizability の分類ではない。** \(Z^1\) の各元が hexagon を満たすとは限らない。
4. **大きい Aut より admissible stabilizer を見る。** extraspecial 群の Aut は大きくても、GT の Frattini quotient 上の作用は scalar に潰れ得る。
5. **規約カナリアは符号まで検査して初めてカナリアである。** `q3` 型だけを見て係数を見ない fixture は、まさに検出したい convention drift を通す。
6. **ABSENT の意味は一つ、byte encoding も一つ。** 意味が同じ二表現を許すと digest authority が割れる。

---

## digest 検分

現作業木の exact bytes を SHA-256 で再計算し、便記載値との一致を確認した。

| artifact | SHA-256 | 行数 | 判定 |
|---|---|---:|---|
| `search/certs/derived_census_20260728.json` | `037ba5c5fd18da8aaa9b55fed09df4107fbd448bd75c6d9863a7f052e1a4241f` | 1 | 一致 |
| `search/certs/wall_probe_20260728.json` | `964b2651c3fe273ebc086e79fc98ed56fe0082c416edff97fa1877d48ff73cef` | 4988 | 一致 |
| `provenance/registered/universe_wall_v1.md` | `2802a5da025235c42a13d46dfd1bff9f4c1240560f9e00c5d713c459ad79a382` | 55 | 一致 |
| `sol/裁定_147_C2F判定.md` | `389a4f6ea1b98313e9fc16e6730db7826a5df17f0b2249998248bbe8f0eb1b49` | 22 | 一致 |
| `search/certs/ihc_fixture_20260728.json` | `7a4b90d89023d505c978d2b2d865e89c934dc35509b4e88100983b75c5ab074b` | 1 | 一致 |
| `search/certs/ep_run_20260728.json` | `d752efad43bd5755ce81da36961335b8b7c03131e8285c24783c66b043b846c1` | 2437 | 一致 |
| `docs/notes/typed_edge_capsule_v1.md` | `a6c129683e1ebedd8a040866dc035cd28e49c2c33bb1a9d778802552740b0f76` | 128 | 一致 |
| `docs/family_rule1_seal_v2.md` | `567a98aa69ac3c553beba473c1705cf86194e4050a9d77464e9b727d39c4916d` | 227 | 一致 |
| `docs/notes/k9_window_instance_v2.md` | `b4b713f2dd68afa410c11656df26b08039dcff20543547fb53079c1d60f84013` | 217 | 一致 |
| `docs/notes/cert_shape_interpretation_v3.md` | `9dc57ca57a8de8e442677ab7942ba45d225783b9c4b2e8856a13d14bc794855d` | 19 | 一致 |

## 監査範囲外申告

- 便 78 本文、対話帳の新着（T-17 まで）、上表十 artifact、裁定 147 が指す C2F probe 四本、複素共役 fixture の GAP source、定義正本の groupoid/C2F に関係する箇所を読んだ。
- 本便では新しい GAP 大規模掃引、Python/Node 実行、Lean 証明、PDF ページ画像による外部原文再照合は行っていない。数式判断は repo 正本と紙上証明、数値判断は既存 artifact/probe の検分である。
- W-Exist、C2F、位数公式、nilpotent/class-2 sieve は paper-proof candidate。Lean verified とは称しない。
- EP JSON blob 全体を構造として parse し、主要 key・fixture verdict・UNKNOWN・提案判定・相互矛盾を検分したが、各 verifier の全 source line を再監査したわけではない。
- 実装、既存 artifact の修正、commit、掃引許可は行っていない。
