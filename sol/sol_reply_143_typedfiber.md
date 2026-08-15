# Sol 便 143 / 143b 統合返信 — typed fiber は全元で局所通過するが、単一窓の陽性は屋根を決着しない

## 0. 結論

便 143 を §0 から §4、追補 143b を §0 から §3 まで順に処理した。入力
`ops/inbox_codex/sol_task_143_typedfiber.txt` の SHA-256 は
`4fbcf170181eb0293596c4e21b7f3211e79b423949e181a9d17adf41931e8173`
、`ops/inbox_codex/sol_task_143b_pregate.txt` の SHA-256 は
`dfe105215bbacf70c3a526679f042c84aee95c32ed3a6b837d0583a469de1b80`
である。

便 142 の `PENT-NODESCENT`、`GATE_FAILED` の撤回、および式 (4)

\[
C_M=\bigcap_{i=1}^{4}p_i^{-1}(M),\qquad
\widetilde K=C_M\cap\widetilde{\mathbf N}^{*}
\tag{1}
\]

の型は受理する。ただし、便 143 §1.3 の

\[
\text{「一つの outside-}A_{\rm ar}\text{ 元が }\widetilde K
\text{ で通過」}
\Longrightarrow
\mathfrak G_{\widehat{GT}}\ne A_{\rm ar}
\tag{2}
\]

は成立しない。単一の有限窓での通過は genuine 性の必要条件の一つにすぎない。
2008 Cor. 3.13 は genuine を **全ての**細分窓への survival と同値にしている。
原文 PDF p.38 のページ画像でもこの全称量化を再確認した。従って陰性は一窓で
確定できるが、陽性は一窓から確定できない。

さらに (1) の窓については、列挙より強い一様な紙の結論が出る。

> **定理 `TYPED-FIBER-ALLPASS-143`.** 任意の
> \(g\in GT(M)\) に対し、\(g\) へ reduce する charming B4 shadow
> \(\widetilde g\in GT^\heartsuit(\widetilde K)\) が少なくとも一つ存在する。
> とくに (2.20)-PASS を含む reduction fiber は 972 個すべてで非空である。

これは追補 143b の事前ゲートへの **YES** である。被覆台帳名を
**`B4-TYPED-BLIND-143B`** とし、B4-VAC、PENT-NODESCENT に続く三つ目の
B4 側盲目性定理とする。なお「各 fiber が 294 個の NW residue を全て含む」
という強い文は証明にも結論にも不要であり、本稿はそれを主張しない。
恒等 NW residue 一個について、`PENT_W` からの片方向含意ではなく、
§2.4 の (2.20) 直接証明が PASS witness を与えるから検出力が零になる。
従って追補 §1.1 の分岐を採り、§1.2 の「本走」は発火させない。

従ってこの typed 窓が与える局所像は

\[
\operatorname{Im}\!\left(
 GT^\heartsuit(\widetilde K)\longrightarrow GT(M)
\right)=GT(M).
\tag{3}
\]

これは **局所全通過**であり、\(\widehat{GT}\) からの大域的持上げ 972/972 ではない。
よって `SETTLED_NOT_LIFTABLE` も `SETTLED_LIFTABLE` も出せず、972 屋根の
\(\widehat{GT}\) 水準のビットは未決である。

## 1. 式 (1) の誘導 B3 窓を展開する

五つの coface を \(\Phi\)、
\(\lambda_{i,\varphi}:=p_i\circ\varphi:PB_3\to PB_3\) と書く。
2008 (2.4) と逆像の分配則、B4-CANON から

\[
\begin{aligned}
K_3:=(\widetilde K)_{PB_3}
&=\bigcap_{\varphi\in\Phi}\varphi^{-1}
   (C_M\cap\widetilde{\mathbf N}^{*})\\
&=\mathbf N_0\cap
  \bigcap_{\substack{1\le i\le4\\\varphi\in\Phi}}
  \lambda_{i,\varphi}^{-1}(M).
\end{aligned}
\tag{4}
\]

ここで \((\widetilde{\mathbf N}^{*})_{PB_3}=\mathbf N_0\) を使った。
従って \(K_3\le M\) で、便のいう reduction map は確かに存在する。

既存の 20 合成完全表には次の二種類しかない。

1. 8 本は \(F_2\) 上で自然な \(M\)-商写像そのもの。
2. 12 本は \(x,y\) の像が同一巡回群に入る退化写像。

この分類は NW(7) の特殊な元の値ではなく、\(p_i\circ\varphi\) の語の形から
出る。\(M=K^{(9)}\cap N_{S4}\) は \(c\) を含むため、direct 行に現れ得る
中心因子も \(PB_3/M\) で消える。従って

\[
PB_3/K_3\hookrightarrow
(PB_3/\mathbf N_0)\times(PB_3/M)^{20},
\qquad
F_2/(K_3\cap F_2)\hookrightarrow P_7\times H_M^{20},
\tag{5}
\]

\[
H_M=F_2/M_F\cong PB_3/M,\qquad P_7=F_2/V.
\]

という faithful な座標表示を使える。重複する direct 座標は残してよい。

また \(M_{\rm ord}=18\)、\((\widetilde{\mathbf N}^{*})_{\rm ord}=7\) で、
direct 座標が 18、NW 座標が 7 を実現するので

\[
(\widetilde K)_{\rm ord}=\operatorname{lcm}(18,7)=126.
\tag{6}
\]

## 2. `TYPED-FIBER-ALLPASS-143` の証明

### 2.1 任意の target と恒等 NW residue を同時に持ち上げる

\(g=[m,\bar f]_M\in GT(M)\) を任意に取る。charming 性から
\(\bar f\in H_M'\) である。便 142 の Goursat 計算は

\[
(\alpha,\beta)([F_2,F_2])=H_M'\times P_7'
\tag{7}
\]

を与える。従って

\[
f^\sharp\in[F_2,F_2],\qquad
\alpha(f^\sharp)=\bar f,qquad
\beta(f^\sharp)=1
\tag{8}
\]

を選べる。さらに中国剰余定理で

\[
\mu\equiv m\pmod {18},\qquad
\mu\equiv0\pmod7
\tag{9}
\]

を選ぶ。すると \([\mu,f^\sharp]\) は \(M\) 側で \(g\)、NW 側で恒等
shadow \([0,1]_{\mathbf N_0}\) に reduce する。さらに
\(u=2\mu+1\) は 18 と 7 の双方に素、従って 126 に素である。

### 2.2 hexagon は (4) の全座標で成立する

式 (5) の座標ごとに簡約 hexagon の二つの defect を調べる。

- NW 座標では (8)(9) により恒等 shadow なので成立する。
- 8 本の direct \(M\) 座標では、\([\mu,f^\sharp]\) は
  \([m,\bar f]_M=g\) と同じなので成立する。
- 12 本の退化座標では \(\lambda(x),\lambda(y)\) が一つの巡回群に入る。
  \(f^\sharp\in[F_2,F_2]\) だから、\(f^\sharp\) および
  \(\theta(f^\sharp),\tau(f^\sharp),\tau^2(f^\sharp)\) の像は 1 である。
  第 1 hexagon は直ちに 1、第 2 hexagon の残りは、巡回群内で
  \[
  \lambda(x)^\mu\lambda((xy)^{-1})^\mu\lambda(y)^\mu=1
  \]
  となる。

(5) は単射なので、二つの hexagon defect は \(K_3\cap F_2\) に入る。

### 2.3 charming/SURJ も自動である

\(f^\sharp\) は交換子語そのものなので charming の代表条件を満たす。
\(T^{PB_3}_{\mu,f^\sharp}\) とその \(F_2\) 制限を (5) の各座標へ写すと、

- NW 座標では恒等 shadow の自己同型、
- direct \(M\) 座標では settled な \(g\) の自己同型、
- 退化巡回座標では \(u\) 乗写像

になる。最後の写像も \(\gcd(u,18)=1\) により自己同型である。生成元上の
この可換性から \(T(K_3)\subseteq K_3\) および
\(T(K_3\cap F_2)\subseteq K_3\cap F_2\) が従い、両写像は対応する有限商の
自己準同型になる。もしその核元があれば、各座標自己同型の逆を使って元自身の
全座標が 1、(5) の単射性から元は 1 である。従って
\(T^{PB_3}\) と \(T^{F_2}\) はともに有限群上の単射、したがって全射である。
(6) と \(\gcd(u,126)=1\) は PB2 の全射も与える。2008 Prop. 2.10 により
GT-shadow の全射条件が揃い、\(F_2\) 全射と交換子代表により charming 条件も揃う。

### 2.4 pentagon は二つの因子で同時に成立する

\(D(f^\sharp)\) を (2.20) の pentagon defect とする。

まず \(C_M\) 側を見る。各 \(p_i\) 座標では、五つの
\(p_i\circ\varphi\) のうち二つが direct、三つが巡回退化である。
交換子語は退化三項で 1 となり、direct 二項は (2.20) の両辺で同じ項として
残る。これは B4-VAC の証明を \(M\) に適用した同じ語計算であり、

\[
D(f^\sharp)\in C_M.
\tag{10}
\]

次に (8) の \(\beta(f^\sharp)=1\) は \(f^\sharp\in V\) をいう。
\(V=\gamma_5(F_2)F_2^7\) は verbal なので、五つの coface の各々が
\(f^\sharp\) を \(\mathcal V(PB_4)=\widetilde{\mathbf N}^{*}\) に送る。
従って

\[
D(f^\sharp)\in\widetilde{\mathbf N}^{*}.
\tag{11}
\]

(10)(11) から \(D(f^\sharp)\in\widetilde K\)。よって
\([\mu,f^\sharp]\in GT^\heartsuit(\widetilde K)\) は pentagon-pass で、
しかも \(g\) へ reduce する。\(g\) は任意だったから定理と (3) が従う。∎

## 3. 便 143 §1.2–§1.3 の裁定

### 3.1 陰性方向

便 143 §1.2 の陰性規則は正しい。一つの outside-\(A_{\rm ar}\) 元について、
ある有限 B4 窓への **全** reduction fiber が空、または全て (2.20)-FAIL
なら、その元は \(\widehat{GT}\) から来ない。実像が
\(A_{\rm ar}\) を含む部分群で指数 3 の二択にあることから、実像は
\(A_{\rm ar}\) に確定する。

ただし今回の \(\widetilde K\) では定理により全 972 fiber が少なくとも一つの
PASS を含む。従ってこの窓から陰性証明書は出ない。

### 3.2 陽性方向

便 143 §1.3 は **FAIL** と裁定する。正しい包含は

\[
\mathfrak G_{\widehat{GT}}(M)
\subseteq
\operatorname{Im}\bigl(GT^\heartsuit(\widetilde K)\to GT(M)\bigr),
\tag{12}
\]

であって逆包含ではない。今回 (3) により (12) の右辺が \(GT(M)\) 全体に
なっただけである。2008 Cor. 3.13 の正しい陽性条件は、一窓の PASS ではなく
**全ての** B4 細分窓での survival、同値に互換な逆極限元の存在である。

実際、既存の `b4_direct_adjudication_feasibility_v1_2.md` §4.1 も
「陰性は 1 窓で有限、陽性は切り詰めから出ない」と明記している。
従って (3) と指数 3 の二分法を合成して `SETTLED_LIFTABLE` とするのは
有限-to-family の過大格付けになる。

## 4. 要求された実装・較正・資源への回答

便は「全数列挙に固執せず、代数で決まるならそれでよい」と明記している。
本便ではその代数路が (3) まで閉じたため、
`m972_b4_fiber.g` と `check_b4_m972_fiber.py` を新造して巨大 fiber を走査する
必要はない。存在判定の witness は各 target に対し (8)(9) で一様に構成される。

したがって本便で新しい producer/checker、GHA workflow、commit、push、dispatch は
作っていない。新実装が無いので N⁽¹⁹⁾ の 216 を「各新実装で再現した」とも
申告しない。既存の GAP/Package GT による 216 の一致は便 142b の在庫 5 として
そのまま維持する。

この紙の閉鎖が依存する既存有限入力は、20 合成表の direct 8 / cyclic 12 分解、
\(M_{\rm ord}=18\)、\(\mathbf N_{0,\rm ord}=7\)、および便 142 の
導来 Goursat 全射 (7) である。新しい生値や封印値は使っていない。

## 5. 追補 143b — 空振り後の在庫を続行する

### 5.1 一般ゲートを先に置く

追補 §2 の要求を、以後用いた全計器について先に記録する。

| 計器 | 述語の定義域 | 検出力の事前判定 |
|---|---|---|
| \(\widetilde K=C_M\cap\widetilde{\mathbf N}^{*}\) | \((\widetilde K)_{PB_3}\le M\) なので一致 | **零**。`B4-TYPED-BLIND-143B` |
| Prop. 3.3 を \(\widetilde K\) に適用 | 同じ B4 target 上なので一致 | **零**。§5.2 で \(\widetilde K\) 自身が isolated |
| 四つの裸の \(Q_8\) 窓 \(N_j\) | \((N_j)_{PB_3}\) と \(M\) は比較不能なので不一致 | 裸の値は 972 を裁定しない。正しい型 \(C_M\cap N_j\) でも §5.3 により零 |
| \(B=2|Q|\) の central \(C_2\) event | 全候補 \(L\le M\) なので一致 | 当該 event では **零**。§5.4 で全三 marked orbit が全射 |
| 四 cofinal 命題 | 同一 cofinal family 上なら一致 | kernel-2 の三行族は noncofinal。従って現段では発火しない |

### 5.2 在庫 3 — `ISO-INTERSECTION-B4-143B`

> **補題 `ISO-INTERSECTION-B4-143B`.** 同じ braid arity の isolated 窓
> \(A,B\) の交叉 \(A\cap B\) は isolated である。さらに isolated な B3 窓
> \(M\) に対し \(C_M=\bigcap_i p_i^{-1}(M)\) は isolated である。

CORE-4 により \(C_M=\operatorname{core}_{B_4}(p_4^{-1}(M))\) なので、これは
確かに B4-normal な有限窓である。

実際、\(A\cap B\) 上の shadow を \(A,B\) へ reduce すると、二つの source
kernel は isolated 性によりそれぞれ \(A,B\) である。商の単射

\[
 PB_4/(A\cap B)\hookrightarrow PB_4/A\times PB_4/B
\tag{13}
\]

から元の source kernel はちょうど \(A\cap B\) になる。同じ議論を

\[
 PB_4/C_M\hookrightarrow\prod_{i=1}^{4}PB_3/M
\tag{14}
\]

と GT 写像の forgetful naturality に適用すれば後半が従う。これは 2401
Prop. 3.15 の交叉補題の B4/forgetful 版であり、代表 \(f\) の変更は各商への
射影後に消えるので影響しない。

一方 \(\widetilde{\mathbf N}^{*}=\mathcal V(PB_4)\) は verbal である。任意の
準同型は \(\mathcal V\) を \(\mathcal V\) へ送り、charming B4 map は全射なので、
その source kernel は包含と指数一致により \(\widetilde{\mathbf N}^{*}\) 自身である。
従って \(C_M\) と \(\widetilde{\mathbf N}^{*}\) はともに isolated、ゆえに

\[
 \widetilde K=C_M\cap\widetilde{\mathbf N}^{*}
 \quad\text{is isolated}.
\tag{15}
\]

よって 2008 Prop. 3.3 の connected source objects は \(\widetilde K\) 一個で、
\(\widetilde K^\sharp=\widetilde K\)。source-kernel orbit は 1、交叉前後の指数は
同じである。§2 の像 972/972 と合わせると outside-\(A_{\rm ar}\) の 648 元も
この isolated 窓では全て survive する。ここから下の **全** isolated 細分での
survival は従わないが、在庫 3 が指定したこの target の Prop. 3.3/source
refinement は恒等 refinement 一個として完了した。

### 5.3 在庫 4 — 四つの非可換窓は各 4/4 全通過する

まず追補本文の母集団表記を再訂正する。正しい四窓は

\[
 (192,1489)\text{ の二 epi},\qquad(192,1490)\text{ の二 epi}
\tag{16}
\]

である。`1492/1494` の具体的 epi では \(\psi(PB_4)\cong C_2^3=[8,5]\) で
`is_window=false` であり、\(Q_8\) 四窓へ混入させない。

四窓の一つを \(N\)、\(Q=\psi(PB_4)\cong Q_8\)、
\(z=Z(Q)=Q'\) の非自明元とする。各 pure edge \(x_{ij}\) は位数 4 の像を持つ。
\(Q/\langle z\rangle=V_4\) では、遠可換する opposite edges は同じ非零類、
adjacent edges は異なる類になる。後者が同じなら \(S_4\) の edge 推移性により
六辺が全て同じ類となり、pure image が \(Q_8\) を生成することに反する。従って

\[
 \bar x_{12}=\bar x_{34}=a,\quad
 \bar x_{23}=\bar x_{14}=b,\quad
 \bar x_{13}=\bar x_{24}=a+b.
\tag{17}
\]

と書ける。特に最初の三 strand の \(x_{12},x_{23}\) が \(Q_8\) を生成するので

\[
 [PB_4:N]=[PB_3:N\cap PB_3]=[F_2:N\cap F_2]=8,\qquad N_{\rm ord}=4.
\tag{18}
\]

候補 \(f\) は \(1,z\) の二つだけである。二本の hexagon を \(Q_8\) で計算すると

\[
 (m,f)=(0,1),(1,z),(2,z),(3,1)\pmod4
\tag{19}
\]

がちょうど全解で、四つとも \(x^{2m+1},y^{2m+1}\) が \(Q_8\) を生成する。
非自明候補を \(f=[x,y]\) で代表させ、(2.20) の五 coface を直接評価する。
(17) の加法記号を \(V_4\) のものとすると、五つの引数対の像は順に

\[
 (b,a),\ (b,b),\ (a,b),\ (a,a),\ (a,a).
\tag{20}
\]

従って (2.20) の左辺は \(z\cdot1\cdot z=1\)、右辺は
\(1\cdot1=1\) である。この計算は \(PB_4/N\) 内の (2.20) を直接使うので、
\(\Delta_4^2\in N\) の真偽に依存しない。

\(f=1\) は自明に通るから、pentagon-pass は \(f\) で 2/2、pair で 4/4 である。
各 map は PB3 image \(Q_8\) 上で自己同型、\(S_4\) 上で恒等なので B4 商全体へ
全射である。また標準中心公式
\(T_{m,f}(\Delta_4^2)=(\Delta_4^2)^{2m+1}\) と \(2m+1\) の奇性により
`delta2_in_ker` は source と target で同じである。固定した各群の二 epi class は
この bit で一意に分かれるため source kernel は元の \(N\)。従って四窓はいずれも

| quantity | 各窓の値 |
|---|---:|
| \([B_4:N]\) / \([PB_4:N]\) | 192 / 8 |
| \([PB_3:N\cap PB_3]\) / \([F_2:N\cap F_2]\) | 8 / 8 |
| \(N_{\rm ord}\) / candidate \(f\) | 4 / 2 |
| hexagon + SURJ / pentagon on (19) / charming | 4 / 4 / 4 |
| source-kernel orbit / settled | 1 / 4 |

であり、全て isolated である。

ただし裸の \(N\) と target \(M\) は比較不能である。\(N_{PB_3}\le M\) なら
巨大な \(PB_3/M\) が \(Q_8\) の商となり不可能。逆包含なら \(Q_8\) は
\(G_9\times\mathrm{PSL}(2,8)\) の商となるが、odd normal subgroup を殺した
\(G_9\) の 2-群商は \(V_4\) の商で可換、PSL 因子からの像は自明なので不可能である。

正しい型は \(K_N=C_M\cap N\)。ここでは共通商 \(V_4\) があり、PB3 商は

\[
 (PB_3/M)\times_{V_4}Q_8
\tag{21}
\]

となるので、便 142 の「共通商なし」の Goursat 独立性は使えない。それでも任意の
\(g=[m,\bar f]_M\) について、\(m\) が偶数なら \(r=0\)、奇数なら \(r=3\) と置けば
\(r\equiv m\pmod2\) であり、

\[
 \mu\equiv m\pmod {18},\qquad \mu\equiv r\pmod4
\tag{22}
\]

は解を持つ。導来部分では \((\bar f,1)\) を選べる。(19) でこれは \(Q_8\) 側の
identity/mirror shadow、pentagon は \(f_Q=1\) で自明であり、\(M\) の二十座標は
§2.4 と同じ B4-VAC cancellation で通る。従って全 972 target が \(K_N\) でも通過する。
さらに \(C_M,N\) が isolated なので §5.2 により \(K_N\) も isolated である。
これを **`Q8-TYPED-ALLPASS-143B`** と呼ぶ。項目 4 は裸窓でも型付き窓でも
陰性 detector を与えず、ここで消化する。

### 5.4 在庫 7 — kernel order 2 event の完全分類

ここでは \(Q_0:=PB_3/M=G_9\times P\)、\(P=\mathrm{PSL}(2,8)\) と書く。
\(G_9=A\rtimes V_4\)、\(|A|\) は奇数で、\(P\) は perfect かつ Schur multiplier
の 2-primary part を持たないので \(H^1(P,C_2)=H^2(P,C_2)=0\) である。
Lyndon–Hochschild–Serre と積の Künneth から

\[
 H^2(Q_0,C_2)\cong H^2(V_4,\mathbf F_2)
 =\mathbf F_2\{a^2,ab,b^2\}.
\tag{23}
\]

\(B_3\) の二共役作用は \(V_4=G_9^{\rm ab}\) 上で二つの transvection を与え、
\(GL_2(2)\cong S_3\) 全体を生成する。従って不変部分は

\[
 H^2(Q_0,C_2)^{B_3}
 =\mathbf F_2\,(a^2+ab+b^2).
\tag{24}
\]

零類は split \(E_0=Q_0\times C_2\)、非零類は全ての非零 \(V_4\) 元の lift が
位数 4 となる

\[
 E_1=Q_0\times_{V_4}Q_8
\tag{25}
\]

である。base 固定 automorphism の作用で \(x,y\) の central lift bit は消せる。
split 類は全射性のため \(c\mapsto z\) が必要で marked orbit 1 個。nonsplit 類は
\(x,y\) の lift 自体が \(E_1\) を生成し、\(c\mapsto1,z\) が同値でない二 orbit。
不変 extension class と \(B_3\) が固定する \(c\)-image により三 kernel は全て
\(B_3\)-安定である。従って kernel order 2 event の候補はちょうど三 marked orbit である。

全 fiber も紙で数えられる。split 行では \(N_{\rm ord}=18\) で、任意の
\(g\in GT(M)\) は C2 座標を恒等にして一意に持ち上がる。nonsplit 行では
\(N_{\rm ord}=36\)。各 base \(m\bmod18\) には二つの \(\mu\bmod36\) があり、
各 \(\mu\) について kernel 元 \(z\in E_1'\) により二つある \(f\)-lift の一方だけが
(19) の hexagon を満たす。誘導写像は \(Q_0\) 上の settled automorphism と
\(Q_8\) 上の identity または同時 inversion の fiber product なので自己同型である。
逆に任意の shadow も二因子へ射影するとこの形になるから、三 kernel は全て isolated。

| extension class | marked orbit | \(N_{\rm ord}\) | 各 orbit の \(|GT(L)|\) | \(|\operatorname{Im}R_{L,M}|\) | zero fiber | isolated |
|---|---:|---:|---:|---:|---:|---|
| split \(Q_0\times C_2\) | 1 | 18 | 972 | 972 | 0 | yes |
| nonsplit \(Q_0\times_{V_4}Q_8\) | 2 | 36 | 1,944 | 972 | 0 | yes |

これを **`C2-EVENT-ALLPASS-143B`** とする。従って
\(B=2|Q_0|=2{,}939{,}328\) の order event は三 class、image 972、zero fiber 0
として完走した。これは paper enumeration であり独立 checker も Lean 証明書もない。
ISO-FIBER-ENUM 全体は kernel order \(3,4,\ldots\) に続くので、在庫 7 全体を
消化済みとは数えない。

### 5.5 在庫 8 — 四命題は kernel-2 では通るが cofinality が無い

§5.4 の三行では kernel が chief \(C_2\)、relative obstruction は全 972 行で零、
生成は自己同型により成立し、同じ代表が charming である。従ってこの有限三行だけなら
`REL-VANISH` / `GEN-NONCOVER` / `CHAR-LIFT` の三局所条件は全て通る。

しかし三つの distinct index-2 kernel を \(L_1,L_2,L_3\) とし
\(K_0=L_1\cap L_2\cap L_3\) と置くと、交叉閉性により \(K_0\) は isolated で、
どの \(L_i\) も \(K_0\) 以下ではない。従って
\(\mathcal U_2=\{L_1,L_2,L_3\}\) は \(\mathcal I_M\) で cofinal でない。
`CHIEF-COFINAL-140` は発火せず、有限三行の成功を COMPACT へ格上げできない。

したがって在庫 8 の四命題を **同一 cofinal family** 上で証明した本数は依然 0。
次の非零計器は、kernel order \(\ge3\) の event を昇順に足し、各実在 chief step で
relative class、bad-locus noncover、charming compatibility を同時に出すものに限られる。

### 5.6 在庫 6 — mirror 線の消化を維持する

MIRROR-SHADOW-B4 の状態は便 142b から変わらない。四つの \(Q_8\) 窓では
`delta2_in_ker` の二層が各群の二 Aut-orbit を一意に分け、\(\iota\) はこの bit を
保存するので各窓を固定する。これは §5.3 の \((m,f)=(3,1)\) が settled である
こととも一致する。従って distinct mirror twin は 0、在庫 6 は消化済みのままである。

## 6. 在庫 1–8

| # | 状態 | 本便後の正確な会計 |
|---:|---|---|
| 1 | **保留** | 便 143b の続行指定は 3,4,6,7,8。\(R_7\) の direct full table 自体は未実行であり、消化済みには数えない |
| 2 | **消化** | 型付き \(\widetilde K=C_M\cap\widetilde{\mathbf N}^{*}\) の reduction fiber の存在判定を代数で完了。全 972 target で PASS fiber 非空、局所像は 972/972 |
| 3 | **消化** | \(\widetilde K\) は isolated。Prop. 3.3 は \(\widetilde K^\sharp=\widetilde K\)、source orbit 1、648 outside 元も全 survive |
| 4 | **消化** | 正しい四 \(Q_8\) 窓は各 charming 4、pentagon 4、settled 4。型付き \(C_M\cap N_j\) も 972/972 |
| 5 | **消化済みを維持** | 既存 Package GT 較正。N⁽¹⁹⁾ pentagon-pass 216 が GAP と一致。本便で再実行したとは数えない |
| 6 | **消化済みを維持** | MIRROR-SHADOW-B4。現用六窓の mirror 線は既裁定どおり空 |
| 7 | **部分消化** | kernel order 2 event は三 marked orbit、全て isolated、image 972、zero fiber 0。kernel order \(3,4,\ldots\) は未走 |
| 8 | **未消化** | kernel-2 三行では三局所条件が通るが族は noncofinal。同一 cofinal family 上の四命題は 0 本 |

従って番号単位の消化済みは **2, 3, 4, 5, 6**。未消化は **1, 7, 8** で、
追補 143b が列記した在庫に限れば未消化は **7（kernel order 3 以後）と 8** である。

## 7. endgame scope と格

- 本便で測ったのは、\(\widetilde K\)、四つの \(Q_8\) 窓とその型付き交叉、
  および三つの kernel-2 B3 窓という有限個の **局所** reduction 像である。
- \(\widehat{GT}\) 水準の像 \(\mathfrak G_{\widehat{GT}}(M)\) は未決。
- \(\widehat{GT}_{\rm gen}\) 水準の A 型/B 型二分法や (U-10) について新しい
  結論を出していない。
- `TYPED-FIBER-ALLPASS-143`、`ISO-INTERSECTION-B4-143B`、
  `Q8-TYPED-ALLPASS-143B`、`C2-EVENT-ALLPASS-143B` は paper-proof。
  20 合成表と四窓の母集団には既存の独立再導出があるが、本便の新しい定理全体の
  独立 checker は無く、Lean certificate も無い。
- `verified` とは呼ばない。finite-to-family の格上げも行わない。
- \(A_{\rm ar}\), \(S=\mathrm{PSL}(2,8)\), \(P_7\), \(R_7\),
  \(C_M\), \(\widetilde K\) は分記した。
- 封印 3 量、`u`、`c`、sealed K5 は非接触。本便で変更した作業木対象は
  この返信だけである。

## 8. provenance

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_143_typedfiber.txt` | `4fbcf170181eb0293596c4e21b7f3211e79b423949e181a9d17adf41931e8173` |
| `ops/inbox_codex/sol_task_143b_pregate.txt` | `dfe105215bbacf70c3a526679f042c84aee95c32ed3a6b837d0583a469de1b80` |
| `sol/sol_reply_142_b4.md` | `c5c8b685a856003a0515ad5c1bbae2922fba7e0a7bc47b0f06a77064a0f12dcc` |
| `sol/sol_reply_141_enum.md` | `1f9f390552b945c56587cb96270b04bd8f6a1f67ddd361b1b9f2ffbf2a98587e` |
| `sol/sol_reply_140_finish.md` | `3463fe6ca0d876b2b512a270e907c32ea82afa6183848c92de63fee8a0ba0da2` |
| `docs/notes/b4_direct_adjudication_feasibility_v1_2.md` | `7d1f882da75fce8fddaa2303afb8fb0515231771a15984d61718175c35bee990` |
| `docs/notes/b4_theorem_check_v1.md` | `70ef1991ea3d4728e4a61bc43e4a468269a396c8db8dec3270f61f9818eae8b6` |
| `papers/2008.00066-what-are-gt-shadows.pdf` | `c44eba890f83c1ac84a44a5b52fd5c6849250b242331d7eaaff9dd983167fb33` |
| `search/certs/d972_phase0_v1_20260813.json` | `dbd34c59638363762cee1eb77720625704935e50a269528df0f88daeaf3841fe` |
| `search/certs/d972_h1_ns4_v1_20260813.json` | `a100893d151b4f4885bab8d950d09fc9d7b875d5651481ae9496f6edc93c8292` |
| `search/certs/cal_b4_integrated_v2_20260806.json` | `71b6fa73b99c4afafc624df844bda61d654248908bc813a4651864d603d44f1b` |
| `search/certs/b4_r0_probe_v2_p2fix_20260806.json` | `eb62d2bb1a884dd36e525e55f2580df8215279a311717b0f903f7f276e09a024` |
| `docs/notes/b4r0v2_second_system_verification_v1.md` | `3912a295152e1dcb51f34678349f824b9c697bd60cb8d19d5a3ad9f9f312b75a` |
| `docs/notes/b4_mirror_transfer_design_v1.md` | `3f898e6ba1f98f77280f3fadaade5fd2a3f064652cb8bfde1b8d9a4fc2212c28` |
| `docs/notes/d972_h1_adjudication_v1.md` | `42cc54b38dab0f035e064e8fa74def91be68d67fbe501b8f49350245bbe1dc0d` |

便 143 時点の novelty grep は `TYPED-FIBER-VAC` / `TYPED-PASS-ALL` /
`LOCAL-PASS-972` / `ONE-WINDOW-PASS` の四語で 0 hit。追補名
`B4-TYPED-BLIND-143B` / `ISO-INTERSECTION-B4-143B` /
`Q8-TYPED-ALLPASS-143B` / `C2-EVENT-ALLPASS-143B` は本返信を除いて 0 hit である。

FIBER_VERDICT: INVENTORY_2_3_4_5_6
