# 返書 137 — WHY-VOID（H-SPLIT の判定と二例の全消滅）

- 対象: ops/inbox_codex/sol_task_137_whyvoid.txt
- 実行日: 2026-08-15
- 着手時 HEAD: e18bc725fd530346a46d3859322579dda9913afc
- 数値の格: producer と helper 非共有 checker の一致による cross-checked
- Lean certificate: なし

## 0. 一行

作業仮説 H-SPLIT を、機構と結論に分けて判定する。

1. ESCAPE-28 の全 3,392 class と ESCAPE-2 の全 7 class で、相対拡大
   \[
   1\longrightarrow V\longrightarrow PB_3/K\longrightarrow PB_3/M\longrightarrow1
   \]
   はすべて通常の意味で分裂する。
2. しかし \(\theta,\tau\)-同変な補群は全 class で存在しない。従って「同変分裂が全消滅を起こした」という H-SPLIT の説明機構は成立しない。
3. 全消滅そのものは真であり、別の厳密な理由を得た。各 frozen roof 行 \(t\) で、cocycle 欠損係数 \(C_t\) は full-hexagon の \(f\)-平行移動係数 \(A_t\) を経由し、
   \[
   \boxed{\qquad C_t Z=-A_tT_t,\qquad Z:\mathbf F_p^{\,\dim Z^1(\Gamma,V)}\longrightarrow Z^1(\Gamma,V)\qquad}
   \]
   となる。従って、非零 cocycle class は \(H^1\) では消えていないにもかかわらず、その障害像は
   \[
   Z^1(\Gamma,V)\longrightarrow\operatorname{coker}A_t
   \]
   で恒等的に零である。この因子分解は 5 成分窓 \(\times\) 324 行の全 1,620 template で二系統一致した。

重要な格の区別は次である。

- 不成立なのは「同変補群が存在し、それが理由である」という説明機構。
- 成立しているのは、凍結した二宇宙で全 shadow の障害が消え、GEN-AFF も独立に正だったという結論。
- 本便は、全 compact 路に対する一般消滅定理までは立てない。

## 1. H-SPLIT の判定

### 1.1 全 class の拡大は通常の意味では分裂する

\(P=\mathrm{PSL}(2,8)\)、\(\pi:G_9\twoheadrightarrow G_3\) とする。各 SURJ class が作る affine image の純部分は

\[
E_0=V\rtimes(P\times G_3)
\]

である。NAME-COLLIDE を避けて \(W_{\rm ker}:=M/K\cong V\) と書く。\(K=K^{(9)}\cap N_E\)、\(M=K^{(9)}\cap N_{S4}\) なので、既存の fiber-product 同定をそのまま使うと

\[
\begin{aligned}
PB_3/K
 &\cong G_9\times_{G_3}\bigl(V\rtimes(P\times G_3)\bigr)\\
 &=\{(g,(v,p,h)):\pi(g)=h\}\\
 &\cong V\rtimes(P\times G_9),
\end{aligned}
\]

\[
PB_3/M\cong P\times G_9.
\]

従って

\[
s(g,p)=(g,(0,p,\pi(g)))
\]

は section である。実際、

\[
s(g,p)s(g',p')=s(gg',pp')
\]

は半直積の積から直ちに従う。この構成は affine cocycle の class に依存しない。

全 class の分類生値は次。

| 例・窓 | SURJ class | 通常分裂 | \(\theta,\tau\)-同変分裂 | 単なる分裂 | 非分裂 |
|---|---:|---:|---:|---:|---:|
| ESCAPE-28 \((\varepsilon,\eta)=(+,+)\) | 1,920 | 1,920 | 0 | 1,920 | 0 |
| ESCAPE-28 \((+,-)\) | 640 | 640 | 0 | 640 | 0 |
| ESCAPE-28 \((-,+)\) | 624 | 624 | 0 | 624 | 0 |
| ESCAPE-28 \((-,-)\) | 208 | 208 | 0 | 208 | 0 |
| ESCAPE-28 合計 | 3,392 | 3,392 | 0 | 3,392 | 0 |
| ESCAPE-2 | 7 | 7 | 0 | 7 | 0 |

ここでいう分裂は相対拡大 \(V\to PB_3/K\to PB_3/M\) の分裂である。定理 SPLIT-NULL の「純商そのものが、共通非自明商を持たない二因子の直積になる」という前件とは別である。本例の \(PB_3/K\) は \(G_3\) 上の fiber product であり、この段へ SPLIT-NULL を適用していない。

### 1.2 同変補群は存在しない

次の短い補題で、標準補群だけでなく任意の補群を排除できる。

> **補題 EQ-COMP-VOID.**
> marked affine image を \(\widehat E=B_3/K\)、その純部分を \(E_0=PB_3/K\) とする。\(V\triangleleft\widehat E\) とし、\(\widehat E\) が marked \(\widehat\theta,\widehat\tau\) で生成され、affine image が SURJ であるとする。\(C\le E_0\) が \(V\) の補群で、\(\widehat\theta,\widehat\tau\) の共役と同変なら、商 \(C\cong PB_3/M\) の \(V\) への作用は自明である。

**証明.** 同変性により \(C\) は \(\widehat\theta,\widehat\tau\) で正規化される。二元が \(\widehat E\) を生成するので \(C\triangleleft\widehat E\)。また \(V\triangleleft\widehat E\)、\(C\cap V=1\) だから

\[
[C,V]\le C\cap V=1.
\]

従って \(C\) は \(V\) を自明に作用させる。∎

実際の二加群では純生成元 \(X,Y\) の共通固定空間は零である。

| 例 | \(\operatorname{rank}(1-\rho(X))\) | \(\operatorname{rank}(1-\rho(Y))\) | \(\dim V^{\langle X,Y\rangle}\) |
|---|---:|---:|---:|
| ESCAPE-28, \(V_{28}\) | 26 | 26 | 0 |
| ESCAPE-2, \(V_{12}\) | 10 | 10 | 0 |

従って商の作用は非自明であり、補題の結論と矛盾する。全 SURJ class で同変補群は存在しない。

この議論は、代表 cocycle が coboundary かどうかだけを見るものではない。ESCAPE-2 の 7 class は全て非零であり、ESCAPE-28 でも各 full class は両既約成分で translation kernel を作る class である。SURJ が、同変補群の不存在を強制する側に効いている。

### 1.3 H-SPLIT の条件命題と説明機構を分離する

もし section \(s\) が群準同型で、関係式に現れる \(\theta,\tau\) の全作用と同変なら、下の relation \(R_i(f)=1\) に \(s\) を適用して

\[
R_i(s(f))=s(R_i(f))=1
\]

となる。この「同変 section は hexagon を運ぶ」という条件命題自体は正しい。

ただし二点を足さなければ「全 shadow が持ち上がる」までは言えない。

1. 実例には、その同変 section が存在しない。
2. relation の成立だけから GEN-AFF は従わない。生成は独立前件である。

凍結した二例では GEN-AFF は既存本走で別に正だった。従って H-SPLIT の条件命題を棄却する必要はないが、それを二例の全消滅の説明として採ることはできない。

### 1.4 実際の機構 — cocycle 欠損の hexagon-exactness

\(\Gamma=C_2*C_3=\langle\theta,\tau\mid\theta^2=\tau^3=1\rangle\) とする。marked cocycle を

\[
z=(z_\theta,z_\tau)\in
Z^1(\Gamma,V)
=\ker(1+\theta)\oplus\ker(1+\tau+\tau^2)
\]

と書く。固定した roof 行 \(t=(m,f)\) について、上の \(f\) の translation を \(u\in V\) とする。full (3.3)(3.4) の translation 部は線型に

\[
\mathcal R_t(u,z)=A_tu+C_tz
\]

と展開される。下の shadow が full equations を満たすため定数項は零である。

> **命題 COCYCLE-ABSORB-137（凍結二宇宙）.**
> ESCAPE-28 の 4 窓を構成する orbit-bundle 2 成分窓と trivial-character 2 成分窓、および ESCAPE-2 の 1 成分窓について、全 324 roof 行で線型写像 \(T_t\) が存在し
> \[
> C_tZ=-A_tT_t
> \]
> となる。従って
> \[
> \omega_t:Z^1(\Gamma,V)\longrightarrow\operatorname{coker}A_t,\qquad
> z\longmapsto[C_tz]
> \]
> は零写像である。

**証明.** producer は cocycle 条件行列の kernel basis \(Z\) を作り、\(C_tZ\) の各列について \(A_tu=-C_tZ_j\) を RREF で解いて \(T_t\) を構成した。全 1,620 template で residual rank は零。checker は別 heart 基底、別行列 primitive で \(A_t,C_t,Z\) を再構成し、

\[
\operatorname{rank}[A_t\mid C_tZ]=\operatorname{rank}A_t
\]

を直接検査して全行一致した。基底に依らない列空間包含

\[
C_t\bigl(Z^1(\Gamma,V)\bigr)\subseteq\operatorname{Im}A_t
\]

が得られる。∎

これは「cocycle class が ordinary \(H^1\) で coboundary になる」という主張ではない。実際、SURJ class は非零のままである。消えるのは、その class を hexagon 障害複体へ送った像であり、補正 \(u=T_tz\) は roof 行ごとに変わる。従って単一の \(\theta,\tau\)-同変 section を後から復元したことにもならない。

また \(C_tZ\) 自体は多くの行で非零である。消滅は \(C_t=0\) だからではなく、非零欠損が \(\operatorname{Im}A_t\) に入るためである。

## 2. 射程と次の設計

### 2.1 compact 路全体の一般消滅は導かない

命題 COCYCLE-ABSORB-137 が量化しているのは、次だけである。

- frozen S4/K3 roof の 324 行
- ESCAPE-28 の 4 marked 窓
- ESCAPE-2 の 1 marked 窓
- それぞれの全 \(Z^1(\Gamma,V)\)

任意の compact 加群、非半単純加群、別 roof、別 marked affine construction には量化していない。従って

\[
\text{compact 路の窓は原理的に全て検出力ゼロ}
\]

という重大な一般結論は **UNKNOWN** である。

一方、今後の preflight に安価な必要ゲートを追加できる。各 template で

\[
r_t^{\rm obs}
:=\operatorname{rank}[A_t\mid C_tZ]-\operatorname{rank}A_t
\]

を先に測る。

- 全 \(r_t^{\rm obs}=0\): class 列挙前に、その module/roof では cocycle 方向の障害像が零と分かる。
- ある \(r_t^{\rm obs}>0\): 非零障害が出るための必要条件を初めて満たす。ただし実際の SURJ class がその方向へ当たることは別ゲート。

この rank gate は、単に \(\dim H^2\) を大きくするより直接的である。

### 2.2 「より大きい \(H^2\)」の最小候補

現在の半単純軌道束 lane で、既知の入口値を加法的に大きくする最小の明示候補は標数 2 の

\[
V_{24}=V_{12}\oplus V_{12},\qquad
\dim H^2(C_2,V_{24})=4.
\]

\(H^1(\Gamma,V_{12})\) は 3 次元なので、二つの multiplicity 方向へ独立な class を置く SURJ multiplicity-rank gate は少なくとも線型代数上は可能である。標数 3 側の対応候補は

\[
V_{35}=V_{21}\oplus B_7^{\oplus2},\qquad
\dim H^2(C_3,V_{35})=4.
\]

ただし、両者の **block-diagonal duplicate marking** では命題 COCYCLE-ABSORB-137 の因子分解も直和する。従ってその最も素朴な窓は同じ roof で \(r_t^{\rm obs}=0\) と紙で予言され、単なる重複による \(H^2\) 増量には情報がない。重複成分を混ぜる新しい NORM-TWIST class はまだ分類しておらず、そこではまず \(r_t^{\rm obs}\) gate を測る必要がある。

最小の「実際に rank gate を正にし得る」候補は現時点で **UNKNOWN**。候補の型は、

1. \(\theta,\tau\)-安定な非半単純 extension で直和分解を壊す、
2. または module は同じでも affine marking / roof を変えて \(C_tZ\subseteq\operatorname{Im}A_t\) を壊す、

のいずれかである。ESCAPE-2 で未分類だった indecomposable extension lane が最初の探索場所だが、最小次元・\(H^2\) 次元・SURJ は未計算である。

## 3. 機械照合

### 3.1 因子分解の全生値

ESCAPE-28 の成分別生値。

| 成分窓 | \(\dim V\) | \(\dim Z^1\) | \(\operatorname{rank}A_t\)（324 行） | \(\operatorname{rank}(C_tZ)\) 分布 | producer failure | checker failure |
|---|---:|---:|---:|---|---:|---:|
| orbit bundle \(+\) | 21 | 25 | \(17:324\) | \(0:6,\ 4:6,\ 13:72,\ 16:240\) | 0 | 0 |
| orbit bundle \(-\) | 21 | 24 | \(18:324\) | \(0:6,\ 3:6,\ 13:72,\ 16:240\) | 0 | 0 |
| trivial character \(+\) | 7 | 10 | \(4:324\) | \(0:12,\ 3:72,\ 4:240\) | 0 | 0 |
| trivial character \(-\) | 7 | 9 | \(5:324\) | \(0:12,\ 3:72,\ 4:240\) | 0 | 0 |

ESCAPE-2 の生値。

| 成分窓 | \(\dim V\) | \(\dim Z^1\) | \(\operatorname{rank}A_t\)（324 行） | \(\operatorname{rank}(C_tZ)\) 分布 | producer failure | checker failure |
|---|---:|---:|---:|---|---:|---:|
| support-two orbit | 12 | 15 | \(9:324\) | \(0:27,\ 1:27,\ 7:162,\ 9:108\) | 0 | 0 |

従って \(C_tZ\ne0\) の行は、ESCAPE-28 の各成分で \(318,318,312,312\) 行、ESCAPE-2 で 297 行ある。それでも factor failure は全て零である。これは「標準 section の translation \(u=0\) が自動的に relation を満たす」という説明ではなく、行依存補正 \(T_tz\) が必要であることを示す。

producer が構成した \(T_t\) family の SHA-256 は

| 成分窓 | factor family SHA-256 |
|---|---|
| orbit bundle \(+\) | 908ab5a5ecadea831de659e7bf10e0ba9076e7358385ec8a6d3e221775aa60e3 |
| orbit bundle \(-\) | 74aa14c12412374d5fc1dabe345b48bcddf05d85546f51da94c82709ba1defd0 |
| trivial character \(+\) | 63370f3bb33646e6ac13964083386315163275f4353491ea08d185af204cc532 |
| trivial character \(-\) | 25f77f013b2955a86d985062d2fd60664e03d427b63bbad6d9274717395f0697 |
| support-two orbit | 565401498a6d2442fb671b4c04a19f3fa0d13b25e5c1f04da6e395a50065bb4c |

checker は factor matrix を共有せず、列空間 rank の包含だけを別基底で再計算した。escape28 preflight の既存欄との mismatch は 0。ESCAPE-2 checker は NumPy を使わず、bit-column 行列と affine word 評価から同じ rank 分布を得た。

本便では新しい class 大走査を行っていない。既存 frozen cert の complete checkpoint を再利用し、新規監査は 5 成分完了を単位とする read-only 線型監査とした。外側 hard timeout は各 lane 180 秒。

| lane | 完了 | wall |
|---|---:|---:|
| producer factor construction | 5/5 | 91.6 s |
| independent checker rank inclusion | 5/5 | 67.9 s |

### 3.2 二つの \(H^2\) 次元 2

二つの 2 は、各加群の Jordan 型からは構造的に決まるが、二例を横断する同一機構ではない。

| 例 | 非自由 cyclic block | 寄与 | 合計 |
|---|---|---:|---:|
| \(p=2\), \(C_2\) | \(\theta:J_2^5\oplus J_1^2\) の \(J_1\) 2 個 | 各 1 | 2 |
| \(p=3\), \(C_3\) | \(\tau:J_3^8\oplus J_2^2\) の \(J_2\) 2 個 | 各 1 | 2 |

\(p=2\) では \(J_2\) は自由で寄与 0、\(J_1\) が寄与する。\(p=3\) では \(J_3\) は自由で寄与 0、二つの \(J_2\) が寄与する。体も障害側も異なり、自然な同型はない。ESCAPE-28 の全 8 Jordan 型では \(H^2\) 次元 \(1,\ldots,7\) が現れ得るため、「必ず 2」という定理もない。

従って次元 2 の一致は、各選択加群に「非自由 block が二つあった」ことの一致であり、全消滅の原因ではない。全消滅を支配する生値は \(\dim H^2\) ではなく、誘導写像 \(\omega_t=0\) である。

### 3.3 入力と再現元の SHA-256

| 入力 | SHA-256 |
|---|---|
| ops/inbox_codex/sol_task_137_whyvoid.txt | 3b85de5c8ebf6d02802cde0f0511d7b5017e212ba7df7316316184c147c9ea75 |
| sol/sol_reply_133_escape28.md | c31b93797b36630c1d039a23d4ac0aa96709d55c339afa05f7701f8cc4888a1a |
| sol/sol_reply_135_blind3grp.md | 74aa609b0eeab91e0de0029da0598d9f3b28459d8a3dd676751fa09d17d61097 |
| sol/sol_reply_136_escape2.md | 84f11e8f63257c89bfbf2784e21b235814d6842af2219129d0760a08cd9c8df7 |
| docs/notes/vnbit_compact_route_v3.md | ff9febbcb47142cbc1716b326b4ca5684a2a57ca1639a44142d697aefe2e6432 |
| docs/notes/entangled972_reading_v1.md | 0a439e48b8df64b0472402125abe887b026a637633db7953942e6688a897887a |
| docs/notes/ihnec_v1.md | 498b24ef9e907b0708c0915c36aa3e2a13bf07e63c753967e920d4731bfe663f |
| search/escape28_mainrun_v1.py | 2acdbdd17c30f28ea3709cf6f44ee47dd81e9868a8ae64b364926f3c4e1ea6b8 |
| search/check_escape28_mainrun_v1.py | aa371e68fd24151f5225eb9ddd4a3a45d7e8172e1a301ae1aa8e2250c8615975 |
| search/escape2_producer_v1.py | 3bf3c92fe66f2a121753a092135e2155e1878660bd411f88311abaff43b24996 |
| crosscheck/check_escape2_v1.py | c7fcbfb4b3bafd3504420158827f4dd6c5d42a9c4433cc271e3d3bdc62529383 |
| search/certs/escape28_preflight_v1r2_20260813.json | 50b614660db17a560d2e4ef8fc954dcf23705765cb2d2721d28fe19d15f4ce45 |
| search/certs/escape2_preflight_v1_20260815.json | d5942eae32b038eaafd3a0bc8a9b67ba78df35b073c4973c98352c4ceefd2a76 |

## 4. 終盤勘定

| 欄 | 生値 |
|---|---|
| endgame_scope | gentle side only; no finite-depth type adjudication |
| PENT_W | NOT_RUN |
| FAKE-KILL^{B4}/U-10 | NOT_RUN |
| required elevation order | PENT_W-PASS, then FAKE-KILL^{B4}/U-10 |

本便の因子分解から有限深度の型認定は行わない。両例の \(N_E\) isolatedness は既存便どおり **UNKNOWN**。

## 5. 規律・novelty・noncontact

### 5.1 novelty grep

数値実行後、受信便と本返書を除いて固定文字列を検索した。

| 文字列 | hit |
|---|---:|
| COCYCLE-ABSORB-137 | 0 |
| cocycle defect factorization | 0 |
| hexagon deformation complex | 0 |
| 同変補群 | 0 |

これは文字列の未出だけを示し、数学的優先権の証明ではない。

### 5.2 noncontact

既存 cert の非接触境界を継承し、本便でも次に触れていない。

| sealed 欄 | opened |
|---|---|
| \(u\) | false |
| \(c\) | false |
| sealed three quantities | false |
| sealed \(K5\) | false |

git commit、push、workflow dispatch は行っていない。巨大な既存 dirty worktree には触れず、指定返書だけを追加した。

## 6. FINDING

| # | 生値・未閉鎖 |
|---|---|
| F1 | ESCAPE-28 の 3,392 class と ESCAPE-2 の 7 class は全て通常分裂、同変分裂 0、非分裂 0。 |
| F2 | 同変補群があれば補群は full marked image で正規となり、\(V\) を中心化する。しかし実作用の共通固定空間は両例で 0。 |
| F3 | H-SPLIT の「同変 section は relation を運ぶ」という条件部は成立するが、実例には前件がなく、GEN-AFF も別前件。従って説明機構としては不成立。 |
| F4 | 実際の理由は全 1,620 template における \(C_tZ=-A_tT_t\)。誘導障害写像は全 \(Z^1\) 上で零。producer/checker failure 0。 |
| F5 | \(\dim H^2=2\) の一致は、各例で非自由 Jordan block が二つだったことによる。二例を横断する強制則ではなく、全消滅の原因でもない。 |
| F6 | compact 路全体の一般消滅は UNKNOWN。次走には \(r_t^{\rm obs}>0\) の preflight gate が必要。 |
| F7 | 最小の明示的な larger-\(H^2\) 半単純候補は \(V_{24}=V_{12}^{\oplus2}\)、\(H^2\) 次元 4。block-diagonal marking は直和因子分解で \(r_t^{\rm obs}=0\)。multiplicity を混ぜる twist を含む最小の有効候補は UNKNOWN。 |
