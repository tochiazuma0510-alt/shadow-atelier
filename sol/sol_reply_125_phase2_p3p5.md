# 返書 125 — Phase 2 cofinal chain / C1′(S4)–P5′ / canonical addendum

日付: 2026-08-13

## 0. 受領範囲と実行概要

便 125 の §0、§1.1–§1.4、§2 を順に処理した。設計だけで止めず、二つの producer、helper 非共有 checker、原子的 checkpoint、内部 hard-timeout を作り、有限計算を実行した。

- Phase 2 は全 isolated refinements の有効列挙から累積有限交叉を取る cofinal chain とした。実行済み深度は 2、生値は順に 972, 972。全深度側は UNKNOWN、chain は継続対象である。
- C1′(S4) は quotient passport の 24 解、三つの候補生成群、その全 normalizer、固定 \(Z\) の 6 dessins を悉皆し、測定模型を intrinsic な対角 dessin に束縛した。同じ比較図式の局所環から P5′ の生成 Kummer 部分群の等式を導出した。
- B1 の式 (1)–(5) と型を独立 addendum に固定し、任意項 B3 四件、B5 二行 template、S-3/NAME-COLLIDE の修理も収録した。
- Luna 指示書は作らず、Sol 便の許可範囲内で直接実装した。

有限計算の出力格は producer/checker の一致までであり、Lean 証明書は作っていない。

## 1. Phase 2 — SINGLE-BIT の cofinal 運転

### 1.1 全 isolated refinements の列挙

\[
B_3=\langle\sigma_1,\sigma_2\mid
\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle
\]

の有限表示を用い、次を dovetail する。

1. 有限乗法表 \(Q\) と marked generating pair を全列挙する。
2. braid relation、生成性、marked epi \(Q\twoheadrightarrow B_3/M\) を有限表で検査する。
3. \(N=\ker(B_3\twoheadrightarrow Q)\subseteq M\) の有限生成系を Reidemeister--Schreier で得る。
4. \(Q\) 上の charming pairs を全列挙し、isolated 条件を有限検査して通る \(N\) だけを出力する。

任意の isolated refinement \(N\subseteq M\) は自身の marked quotient \(B_3/N\) として現れるので、この列挙は重複を許して全対象を尽くす。

列挙項を \(N^{[i]}\) とし、

\[
L_d:=\bigcap_{i=1}^{d}N^{[i]}
\]

と置く。Prop. 3.15 により各 \(L_d\) は isolated、
\(L_{d+1}\subseteq L_d\subseteq M\) である。任意の isolated \(K\subseteq M\) が
\(N^{[j]}\) として現れた時点で \(L_j\subseteq K\) となるため、この chain は cofinal である。

今回の登録先頭項は

\[
N^{[1]}=K^{(27)}\cap N_{S4},\qquad
N^{[2]}=K^{(36)}\cap N_{S4}.
\]

後着の design note が \(K^{(36)}\cap N_{S4}\) 単独を「深さ 2」と呼んだ点だけは採らず、これは列挙項 \(N^{[2]}\) と横断プローブに留めた。降下 chain の深さ 2 は定義どおり累積交叉である。

従って

\[
L_1=K^{(27)}\cap N_{S4},\qquad
L_2=K^{(27)}\cap K^{(36)}\cap N_{S4}
=K^{(108)}\cap N_{S4}.
\]

最後の等号について、producer が置換群 Schreier--Sims で

\[
|G_{27}\times_{\rm marked}G_{36}|=629856=|G_{108}|
\]

を再計算した。Prop. 3.5 の包含と位数等式を合わせている。

### 1.2 reduction、包含 (6)、半決定

\[
\boxed{
R_{L_{d+1},M}
=R_{L_d,M}\circ R_{L_{d+1},L_d}
}
\]

なので像は単調非増加である。また各 isolated \(K\subseteq M\) に対して

\[
\boxed{
P:=\mathcal{PR}_M(\widehat{GT}_{\rm gen})
\subseteq\operatorname{Im}R_{K,M}
}
\tag{6}
\]

である。これは
\(\mathcal{PR}_M=R_{K,M}\circ\mathcal{PR}_K\) から従う。

ある isolated \(K=N^{[j]}\) で標的元が像から欠ければ、
\(L_j\subseteq K\) と factorization により \(L_j\) でも欠ける。従って cofinal chain は A 型側の有限証明書を探索する半決定であり、停止深度の上界は主張しない。

登録済み停止規則は次のまま変更していない。

| 生値 \(|\operatorname{Im}R_{L_d,M}|\) | 動作 |
|---:|---|
| 324 | A 型側の有限証明書を保存して停止 |
| 972 | 情報を増やさず次深度へ継続 |
| その他 | 前件または実装の異常として即時停止・報告 |

有限個の 972 から B 型側について結論しない。

### 1.3 (3.60) 座標修理

旧 search/d972_phase1_v1.g の候補限定 helper は \(m\) の比較に
\(H_{\rm ord}/2\) を用いていた。しかし正典 (3.60)

\[
R_{N,H}([m,f])=(m+H_{\rm ord}\mathbf Z,\ fH_{F_2})
\]

が要求するのは
\(m_{\rm fine}\equiv m_{\rm coarse}\pmod{H_{\rm ord}}\) である。
\(2m+1\) の像の一致だけではこの座標一致にならない。

そのため旧 Phase 1 cert
search/certs/d972_phase1_v1_20260813.json
（SHA-256 b41c99684af7096af9b609077d2953ccd9b572d86b92ee871ff5e08cf291bb23）
を今回の生値の根拠には使わず、Thm. 4.3 (4.12) の全座標を正しい法で再列挙した。修理後も深さ 1 の生値は 972 であった。GAP producer にも同じ修理を入れた。

### 1.4 深度報告と生値

producer run ID:
d972-phase2-coord-20260813T001308Z

| 深度 | 累積窓 | source dihedral size | source roof size | 生値 \(|\operatorname{Im}R_{L_d,M}|\) |
|---:|---|---:|---:|---:|
| 1 | \(L_1=K^{(27)}\cap N_{S4}\) | 972 | 8,748 | 972 |
| 2 | \(L_2=K^{(108)}\cap N_{S4}\) | 1,944 | 17,496 | 972 |

独立な横断プローブ \(K^{(36)}\cap N_{S4}\) も生値 972 だったが、これは累積窓 \(L_2\) ではないので深度表から分離した。

座標数は

\[
|GT(K^{(9)})|_{\rm coord}=108,\quad
|GT(K^{(27)})|_{\rm coord}=972,\quad
|GT(K^{(36)})|_{\rm coord}=216,\quad
|GT(K^{(108)})|_{\rm coord}=1944.
\]

置換群から得た quotient orders は

\[
|G_9|=2916,\quad |G_{27}|=78732,\quad
|G_{36}|=23328,\quad |G_{108}|=629856,
\]

roof orders は順に

\[
1469664,\quad39680928,\quad11757312,\quad317447424.
\]

checker は標準ライブラリだけで \((m,k)\) 座標を再列挙し、
all_checks_true=true を出力した。深度 2 後の状態は UNKNOWN である。

## 2. C1′(S4) と P5′ の一比較図式

### 2.1 比較対象

\[
\begin{CD}
C_{\rm meas} @>{\iota_C}>> C_{\rm can}\\
@V{t_{\rm meas}}VV @VV{t_{\rm can}}V\\
\mathbf P^1_t @= \mathbf P^1_t\\
@A{\lambda^3-t\lambda^2+(t-3)\lambda+1=0}AA
@AA{\lambda^3-t\lambda^2+(t-3)\lambda+1=0}A\\
W_{\rm meas} @>{\iota_W}>> W_{\rm int}
\end{CD}
\]

下段は同じ Shanks cubic による上段の base change である。この一図式で quotient dessin の束縛、6 dessins の分離、局所 Kummer 比較を行った。

### 2.2 有限計算の生データ

producer run ID:
c1prime-s4-p5prime-20260813T001316Z

intrinsic triple は

\[
|P|=504,\qquad
\operatorname{ord}(X)=\operatorname{ord}(Y)=\operatorname{ord}(Z)=9,\qquad
XYZ=1,
\]

かつ \(X,Y,Z\) は同じ \(P\)-共役類に属した。\(P\) の位数 9 の元は 168 個、\(Z\) の共役類は 56 元だった。

passport \((3^3,3^3,(9))\) で第 3 branch cycle \(C\) を固定した全 24 解は次の分布になった。

| 生成群位数 | 解数 | 異なる生成部分群数 |
|---:|---:|---:|
| 81 | 6 | 1 |
| 324 | 9 | 1 |
| 504 | 9 | 1 |

全 \(S_9\) 走査による normalizer は次のとおり。

| \(|G|\) | \(|N_{S_9}(G)|\) | \(|C_{S_9}(G)|\) | 型 \((7,1,1)\) を含む |
|---:|---:|---:|---|
| 81 | 324 | 3 | false |
| 324 | 1296 | 1 | false |
| 504 | 1512 | 1 | true |

既存 exact model の structural prefix には、good-reduction factorization から得た型 \((7,1,1)\) の witness が 10 個ある。producer は measurement payload の開始位置より前で stream を止め、局所数値欄を読んでいない。算術 monodromy は幾何 monodromy の normalizer に入るので、上の全 normalizer 表と合わせると幾何 monodromy の位数は 504 に絞られる。

位数 504 の 9 解は \(C_{S_9}(C)=\langle C\rangle\) の一 orbit である。
\(C_{S_9}(P)=1\) なので、branch labels を保つ幾何学的同型は一意である。両 cover が \(\mathbf Q\) 上にあるため一意な同型は Galois 固定となり、\(\iota_C\) は \(\mathbf Q\) 上に定義される。

orbifold generators を \(A_{\rm orb},B_{\rm orb}\) として

\[
x=(B_{\rm orb}A_{\rm orb})^{-1},\qquad
y=(A_{\rm orb}B_{\rm orb})^{-1},\qquad
z=(xy)^{-1}
\]

を quotient triple に代入すると、\((x,y,z)=(X,Y,Z)\) が置換として三成分とも一致した。

さらに

\[
[S_9:N_{S_9}(P)]\,
\#\{g\in P:\operatorname{ord}(g)=9\}
=240\cdot168=40320=8!
\]

より、固定した 9-cycle \(Z\) を含む \(S_9\)-共役な \(P\) は一つである。その \(P\) 内の \(XY=Z^{-1}\) は 54 解で、\(\langle Z\rangle\)-orbit はサイズ 9 の 6 個。そのうち対角類は一つで、上の kernel-word 再構成 orbit と一致した。これにより測定 quotient、固定 base change、intrinsic 対角 dessin が同じ比較図式に入る。

helper 非共有 checker は SymPy と producer import を使わず、tuple permutations で全表を再計算し、all_checks_true=true を出力した。

### 2.3 P5′ の紙上導出

\(\lambda=0\) 上の唯一の ramification-index 9 cusp を \(P_0\) とする。labelled base を保つ \(\iota_W\) は \(P_0\) を保つ。二つの \(\mathbf Q\)-有理 local parameters に対し

\[
s_{\rm meas}=\gamma s_{\rm int}(1+O(s_{\rm int})),\qquad \gamma\ne0.
\]

\[
\lambda=u_{S4}s_{\rm int}^{9}(1+O(s_{\rm int})),\qquad
\lambda=u_0s_{\rm meas}^{9}(1+O(s_{\rm meas}))
\]

と書けば

\[
u_0=u_{S4}\gamma^{-9},\qquad
[u_0^{-1}]_9=[u_{S4}^{-1}]_9.
\]

loop の向きを unit exponent
\(\varepsilon\in(\mathbf Z/9)^\times\) で変更しても

\[
[u_0^{-1}]_9=[u_{S4}^{-1}]_9^\varepsilon
\]

なので

\[
\boxed{
\langle[u_0^{-1}]_9\rangle
=\langle[u_{S4}^{-1}]_9\rangle
}
\tag{P5'}
\]

を得る。まず \(K^\times/(K^\times)^9\), \(K=\mathbf Q(\zeta_9)\) での等式であり、rational classes として読む箇所だけ RES-INJ-9 で
\(\mathbf Q^\times/(\mathbf Q^\times)^9\) に戻す。代表元の厳密等号は主張しない。

### 2.4 測定部分と紙部分

| 対象 | 根拠 |
|---|---|
| intrinsic \(P,XYZ\)、order-9 class | producer と helper 非共有 checker の全数計算 |
| quotient 24 解と \(81/324/504\) 分布 | 同上 |
| 三 normalizer と 7-cycle 可否 | 二実装による全 \(S_9\) 走査 |
| 位数 504 の一 orbit、fixed-\(Z\) 54 解、6 dessins、対角 1 | 同上 |
| kernel words による \(XYZ\) 再構成 | 同上 |
| exact model の 7-cycle witness | 既存 cert の structural prefix のみ |
| \(G_{\rm arith}\le N_{S_9}(G_{\rm geom})\)、一意同型の \(\mathbf Q\)-降下 | 紙上導出 + centralizer 全数計算 |
| base change の関手性、local parameter 比較、(P5′) | 紙上導出 |

この比較リンクが扱うのは C1′/P5′ と既登録 marking である。P1/P2、
\((Z_{18}\text{-link})\)、算術像の別解釈は射程外であり、状態を変更していない。

## 3. B1 canonical addendum と任意修理

### 3.1 型と式 (1)–(5)

\[
K:=\mathbf Q(\zeta_9),\quad
E:=L_{9,\mathrm{Aff}}=K(\sqrt[9]{a_{\rm mod9}}),\quad
F:=L_{S4}=K(\sqrt[9]{b_{\rm mod9}}),
\]

\[
L_{9,\mathrm{full}}:=E(i),\qquad
d_9=[E:K],\quad d_{S4}=[F:K],
\]

\[
r:=\left|\langle[a_{\rm mod9}]\rangle
\cap\langle[b_{\rm mod9}]\rangle\right|.
\]

\[
[EF:K]=\frac{d_9d_{S4}}r. \tag{1}
\]

\[
|X_{\rm shadow}|=|GT(M)|
=\frac{108\cdot54}{6}=972. \tag{2}
\]

\[
|A_{\rm arith}|
=[L_{9,\mathrm{full}}F:\mathbf Q]. \tag{3}
\]

\[
\boxed{
|A_{\rm arith}|
=6[L_{9,\mathrm{full}}F:K]
=12[EF:K]
=\frac{12d_9d_{S4}}r
}. \tag{4}
\]

\[
\boxed{
|X_{\rm shadow}\setminus A_{\rm arith}|
=972-\frac{12d_9d_{S4}}r
}. \tag{5}
\]

係数 12 を使う表記は
\(12[L_{9,\mathrm{Aff}}L_{S4}:K]\)、
\(L_{9,\mathrm{full}}\) を使う表記は係数 6 と固定した。
\(a_{\rm mod9}\) と \(a_{9,\rm mod18}\)、
\(A_{\rm arith}\) と A 型を共有しない。

### 3.2 B3 四件

1. D9-VAL の補助証明は「唯一の三次部分体」を使わず、\(x^9-2\) の Eisenstein 分岐と \(K/\mathbf Q\) の 2 での不分岐を比較する。
2. GAUGE-18 は \(P_0,P_\infty\) と target \(0,1,\infty\) の labels を固定した文として記す。
3. \(\zeta_{12}\) を使う ambient field は \(\mathbf Q(\zeta_{36})\) とする。
4. \(\mathbf Q^\times/(\mathbf Q^\times)^{18}\) の符号 \(\mathbf Z/2\) を残し、法 9 でのみ符号が消える。

### 3.3 B5 二行 template

> raw: 宣言模型、cert、再現 command、得られた class/vector/order と測定格。
>
> interpretation: raw object を \(L_{9,\mathrm{Aff}},L_{S4},r,A_{\rm arith}\) のどれとして読むか、必要な model/dessin/framework 前件と解釈格。

raw の格から interpretation の格を自動的に上げない。

### 3.4 S-3 / NAME-COLLIDE

P8-v3.2-S-3 は「法 9 へ降下した
\([a_{\rm mod9}]\) 側」と書き、法 18 は
\([a_{9,\rm mod18}]\) とする。S3 は少なくとも
E1-S3、FAM-V2-S3、P8-v3.2-S-3 と namespace を付ける。

## 4. 再現コマンド、証明書、SHA-256

### 4.1 再現コマンド

    python search/d972_phase2_coord_v1.py --hard-timeout-seconds 900
    python search/check_d972_phase2_coord_v1.py
    python search/c1prime_s4_p5prime_v1.py --hard-timeout-seconds 900
    python search/check_c1prime_s4_p5prime_v1.py

両 producer は stage ごとに checkpoint を原子的に置換し、watchdog の hard timeout 時には停止 stage を同 path に残す。今回の二 checkpoint は complete である。

GAP producer search/d972_phase2_v1.g も作成したが、規約どおり
gap.ps1 から起動すると、既存 GAP script を含め runtime が起動前に
couldn't create signal pipe, Win32 error 5
で停止した。従って GAP file は未実行であり、生値の根拠には含めていない。

### 4.2 Artifact hashes

| path | SHA-256 |
|---|---|
| search/d972_phase2_v1.g | d6cc191259a4f722be1ee0723e17e92312262b46a087ef1326b320128f34e38a |
| search/d972_phase2_coord_v1.py | 062bdab1c483e95046a690e75076ac5ec84344126f4f649e6749fcf6bb634b27 |
| search/check_d972_phase2_coord_v1.py | 766b0560d98c1f6a4e6cade08c7af26a6eb198adb51f8b56dd1b4a234f5f66d0 |
| search/certs/d972_phase2_coord_v1_20260813.json | b01a34d0b37c2477eeefb46988b879dd75feca849110750ecdf509afeb2dd28c |
| search/certs/d972_phase2_coord_v1_check_20260813.json | 5325574086845ead4c20cac1bfebd5e0aee76cb92fc2add70d9977342048f297 |
| search/certs/d972_phase2_coord_v1_checkpoint.json | 9181bfeebaf50bc58c7c11b299117fe329f47fb86e46373c818aecc99f18018d |
| docs/notes/d972_phase2_cofinal_execution_v1.md | 97998cac97611f10065b463efa8a417d5da200b23dd39ca7a8b2beed32de847e |
| search/c1prime_s4_p5prime_v1.py | 593673a6e38c12c1890fa8cca81d0469d5e78fbe119e1b32aa7286e8517ebb83 |
| search/check_c1prime_s4_p5prime_v1.py | 80b77841e3df0c180aa78170797074f2333740fad10b1845b55fb888f8493f5e |
| search/certs/c1prime_s4_p5prime_v1_20260813.json | 300137458b0b05095edacd6b80c979f98a6ad8a01a6f72e0cbe86aed694f2eda |
| search/certs/c1prime_s4_p5prime_v1_check_20260813.json | 5ec4f7926a0f337a29771b85c782bfedb0c46c6cd1515389942088a1553016df |
| search/certs/c1prime_s4_p5prime_v1_checkpoint.json | 6b39781096a8f5219eae4bd6668f641d636b0ef0d6dad9b5efbb1ee1b7a4a1ce |
| docs/notes/c1prime_s4_p5prime_closure_v1.md | ea4c4c504c17df332054713abd7b742fd694b1fdf657b242f1929fa724921c37 |
| docs/notes/triad972_canonical_addendum_v1.md | 33288940832d86b81124ad229f01e37a474f3891041c1786e9c4f420c9bb9097 |

## 5. 非接触・有限深度規律

- 二つの producer cert と checker cert は
  u_touched=false、c_touched=false を記録する。
- C1′ producer は既存 model cert を opaque SHA-256 で束縛し、必要な structural prefix だけを stream して measurement payload より前で停止した。
- sealed \(K^{(5)}\) instance と prereg quantities は未接触であり、各 cert に false/untouched flag を残した。
- 数値 local class は読んでいない。
- 有限深度 2 の生値は 972, 972 のみであり、B 型側について有限深度由来の結論は置かない。
- 指定された記号衝突を避け、\(L_{9,\mathrm{full}}/L_{9,\mathrm{Aff}}\)、
  \(a_{9,\rm mod18}/a_{\rm mod9}\)、
  \(A_{\rm arith}\)/A 型、namespace 付き S3 を使った。
- 指定禁句は新規 artifact に入れていない。

## 6. Git 記録

最終 Git 監査時の base は master
21c244ef86b5ca42ce73e983105c1c47f7e67166
（origin/master も同値）だった。作業中に共有 worktree の base が外部更新されたため、開始時 base との同一性は主張しない。

作業 branch sol/task125-phase2-p3p5 の作成を再試行したが、

    fatal: cannot lock ref 'refs/heads/sol/task125-phase2-p3p5':
    unable to create directory for .git/refs/heads/sol/task125-phase2-p3p5

となった。filesystem profile で .git が read-only のためである。

- commit SHA: NONE — branch/ref と index を書けないため commit 未作成。
- push: NOT EXECUTED — push 対象 commit が無いため。
- workflow dispatch: なし。

既存の dirty entries は変更せず、上の task-owned artifact と本返書だけを追加した。Git 書込みが可能な親環境では、表の artifact 一式を task branch に stage、commit、push する工程だけが残る。
