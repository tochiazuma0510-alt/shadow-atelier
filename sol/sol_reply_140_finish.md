# 返書 140 — (a) の最終監査と 1-bit の不可能性裁定

- 対象: `ops/inbox_codex/sol_task_140_finish.txt`
- 実行日: 2026-08-15
- 着手中に観測した HEAD: `3b1b8687088c360f5942b6e6aa8fb1697b4ff9fd`
- 入力 SHA-256: `d28155ca844e0264081a58a611ad2df2015b5aa39d7d9ed615a8e89da97ca3ea`
- 証拠格: 紙上の線型代数・ホモロジー代数、および producer / helper 非共有 checker の有限照合。Lean certificate はない
- 処理順: §0 → §1 → §2 → §3 → §4 → §5

## 0. 最終結論と出口 II の量化監査

本便では出口 I も出口 II も発火しない。採るのは、委嘱 §1 が定めた四条件を満たす **出口 III** である。

理由は「計算が大きい」ことではない。正典 Cor 5.4 により、固定した \(g\in GT(M)\) の持上げ可能性は

\[
 g\in\mathfrak G_{\rm gen}
 \iff
 \forall K\in\mathrm{NFI}_M(B_3),\quad
 R_{K,M}^{-1}(g)\ne\varnothing                                      \tag{0.1}
\]

という全細分量化そのものである。一方、有限排除側の証明書は

\[
 \exists g\in GT(M)\setminus A\ \exists K\subseteq M,
 \quad R_{K,M}^{-1}(g)=\varnothing                                  \tag{0.2}
\]

の一件で足りる。現台帳には (0.2) の組がなく、また (0.1) を有限化する cofinal な全射族定理もない。この二つの事実は、計算時間を延ばすだけでは変わらない。

ここで委嘱 §1.2 の「**任意の** \(g\in GT(M)\)」を文字どおり \(\forall g\) と読むことはできない。算術像 \(A\) の元には整合した Galois 持上げがあるので、その読みは偽である。DICHOTOMY-972 を発火させる論理的に正しい条件は (0.2) の **ある一元**である。本書ではこの必要十分な存在量化で出口 II を監査した。

## 1. 三出口の監査

### 1.1 出口 I — COMPACT は発火しない

`MCOV-ISO-139` により isolated split 族の MCOV は閉じた。しかし split 族が \(\mathcal I_M\) に cofinal であるという定理はなく、`MONO-CNF-139` により、その cofinality を証明することは全 isolated reduction の全射性を証明することと同じ強さを持つ。

さらに、全射の三前件は次の状態である。

| 前件 | 本便後の状態 |
|---|---|
| relation 障害の消滅 | §2.1–2.3 の不変量へ正確に定式化したが、全 isolated refinement での消滅定理はない |
| GEN-AFF の一様供給 | §2.4 の有限部分空間被覆問題へ正確に定式化したが、全 refinement・全行での非被覆定理はない |
| charming と固定した base 行の同時実現 | split 族では `MCOV-ISO-139` が供給する。entangled / mixed / 多段全体では relation・generation と同時に選べる族定理がない |

従って cofinal な \(\mathcal U\) と全 \(L\in\mathcal U\) の全射を示しておらず、COMPACT の前件は成立しない。有限深度の値からこの欄を補ってはいない。

### 1.2 出口 II — 有資格な零 fiber はない

本便までに、isolated と確定した \(K\subseteq M\) と \(g\in GT(M)\setminus A\) の組で持上げ数 0 となったものは **0 件**である。§3 の有限走査では非零の relation 障害像も 0 件だった。

なお \(D_{L/K,t}\ne0\) は、それだけでは零 fiber を意味しない。本便で再収蔵した五 family は、相対複体としては大きな余核を持つのに、誘導写像 \(\omega_{L,t}\) が全て零になる実例である。必要なのは

\[
 D_{L/K,t}\ne0
 \quad\text{かつ}\quad
 \operatorname{Im}\omega_{L,t}\ne0,                                \tag{1.1}
\]

さらにその行が実際の isolated roof と source-generation を持つことである。現成果物は (1.1) を満たさない。

### 1.3 出口 III — 採用理由

出口 III の四要件への対応は次のとおりである。

1. 障害の名指し: §2 の `STRICT-D-140`, `CONE-D-140`, `GEN-COVER-140`, `NO-FINITE-B-140`。
2. 経路独立性: §2.5 で Cor 5.4 路、逆極限 / Mittag--Leffler 路、導来複体 / 有限群路の三本を照合する。
3. 実例または不在理由: §3.2 で、非零の相対余核を持つ五 component と、非零障害像が出なかった全有限範囲を生値で分記する。有資格な (D_{L/K,t}) 対が作れない型上の理由も明記する。
4. 必要品の可算化: §4 で、Exit-II の次数別全列挙と Exit-I の四命題を入力・出力つきで固定する。

## 2. (a) の三停止点を一段掘る

### 2.1 `STRICT-D-140` — \(D\) の正体と、全消滅が形式的には偽であること

\(I_L=\operatorname{Im}A_{L,t}\), \(I_K=\operatorname{Im}A_{K,t}\) と略記する。`ABSORB-BC-139` の可換正方形だけから、基底を選ばず

\[
 \boxed{
 D_{L/K,t}
 =\frac{q_R^{-1}(I_K)}{I_L}.}                                      \tag{2.1}
\]

さらに \(q_U\) が全射なら

\[
 q_R^{-1}(I_K)=I_L+\ker q_R,
 \qquad
 \boxed{
 D_{L/K,t}\cong
 \frac{\ker q_R}{\ker q_R\cap I_L}.}                              \tag{2.2}
\]

**証明.** (2.1) は cokernel 上の写像の核を代表元で書いたもの。\(q_U\) が全射なら、\(q_Rr=A_Ku_K\) に対して \(q_Uu_L=u_K\) を選び、\(r-A_Lu_L\in\ker q_R\) とすれば (2.2) を得る。∎

従って全 refinement で \(D=0\) をいうために本当に必要な追加前件は

\[
 \boxed{\ker q_R\subseteq\operatorname{Im}A_{L,t}}                \tag{STRICT}
\]

である。INT、isolated 性、\(q_U,q_R\) の全射性のいずれも (STRICT) を含意しない。

これは単なる証明上の心配ではない。任意の体 \(k\) 上で

\[
 U_L=k,\ R_L=k^2,\ A_L(u)=(0,u),\qquad
 U_K=k,\ R_K=k,\ A_K(u)=u,
\]
\[
 q_U=\mathrm{id},\qquad q_R(x,y)=y
\]

と置くと、両縦写像は全射で可換正方形を作るが \(D\cong k\) である。さらに

\[
 Z_L=Z_K=k,\quad q_Z=\mathrm{id},\quad
 C_L(z)=(z,0),\quad C_K=0
\]

とすれば \(q_RC_L=C_Kq_Z\) である一方、

\[
 \omega_K=0,\qquad \omega_L\ne0.                                 \tag{2.3}
\]

よって `ABSORB-BC-139` の仮定だけから「全 refinement で \(D=0\)」または「粗段の消滅が細段へ移る」という定理を導くことは論理的に不可能である。実 roof に固有な追加恒等式 (STRICT) が必要である。

### 2.2 `CONE-D-140` — 自然な \(T_t\) を要求しない不変な定式化

二項複体

\[
 \mathcal K_{K,t}:=[U_K\xrightarrow{A_{K,t}}\mathcal R_{K,t}]
 \quad(\deg 0,1)
\]

を置けば

\[
 H^1(\mathcal K_{K,t})=\operatorname{coker}A_{K,t},\qquad
 \omega_{K,t}=H^1\text{ への }C_{K,t}\text{ の合成}
\]

である。\(q:\mathcal K_{L,t}\to\mathcal K_{K,t}\) の homotopy fiber

\[
 \mathcal F_{L/K,t}:=\operatorname{Cone}(q)[-1]
\]

の長完全列は

\[
 H^0(\mathcal K_L)\to H^0(\mathcal K_K)
 \to H^1(\mathcal F_{L/K,t})
 \to H^1(\mathcal K_L)\to H^1(\mathcal K_K)
\]

を与え、従って

\[
 \boxed{D_{L/K,t}
 =\operatorname{Im}\bigl(H^1(\mathcal F_{L/K,t})
 \to H^1(\mathcal K_{L,t})\bigr).}                                \tag{2.4}
\]

これが task 140 §2.2 の「選択を経ない不変量」への回答である。個々の \(T_t\) を選ぶ必要はなく、判定対象は最初から

\[
 \boxed{\omega_{K,t}=\pi_{K,t}C_{K,t}}                            \tag{2.5}
\]

でよい。従って便 139 の停止点 2「自然な \(T_t\) がない」は、**objectwise な消滅命題には不要な余剰条件**として除去できる。

ただし (2.4) は障害を消さない。粗段で \(\omega_K=0\) のとき、細段の像を relative group に持ち上げて置き直すだけである。必要な命題は

\[
 \operatorname{Im}\omega_{L,t}=0
 \quad\text{in}\quad
 \operatorname{Im}\bigl(H^1(\mathcal F_{L/K,t})\to H^1(\mathcal K_L)\bigr) \tag{REL-VANISH}
\]

であり、これは未証明である。

補足すると、全 roof を一つの functor category \(\mathscr C\) で扱い、既に \(C:\mathcal Z\to\operatorname{Im}A\) が分かっている場合、自然な lift の障害は

\[
 \delta(C)\in
 \operatorname{Ext}^1_{\mathscr C}(\mathcal Z,\ker A)              \tag{2.6}
\]

である。しかし (2.6) は **包含が成立した後**の lift 障害であって、包含 (2.5) 自体を証明しない。従って Ext へ移っても本体の全称消滅は回避されない。

### 2.3 \(D\ne0\) の実例と、その限界

一段の可換係数 refinement を relative complex として書き、粗段の relative complex を 0 とする標準形では

\[
 D_t=\operatorname{coker}A_t.
\]

本便で再走した五 component は全 324 行で rank \(A_t\) が一定なので、次の非零値を持つ。

| component | \(\dim\mathcal R_t\) | \(\operatorname{rank}A_t\) | \(\dim D_t\) | \(\operatorname{rank}\omega_t>0\) の行 |
|---|---:|---:|---:|---:|
| orbit bundle \(+\) | 42 | 17 | 25 | 0 / 324 |
| orbit bundle \(-\) | 42 | 18 | 24 | 0 / 324 |
| trivial character \(+\) | 14 | 4 | 10 | 0 / 324 |
| trivial character \(-\) | 14 | 5 | 9 | 0 / 324 |
| support-two orbit | 24 | 9 | 15 | 0 / 324 |

従って「\(D\) が非零なら relation 障害が実現する」は偽である。五 family では \(D\) は大きいが、全 1,620 行で \(\omega_t=0\) だった。

ただしこれらは marked extension の相対線型化であり、source kernel の isolated 性と \(\mathcal I_M\) 内の配置は未証明である。従って上表を有資格な \(D_{L/K,t}\) の有限排除証明書へ格上げしない。現在の成果物で \(L,K\in\mathcal I_M\) と、三写像 \(q_U,q_Z,q_R\) を同時に cert 化した compatible pair の件数は **0**。これが「有資格な非零 \(D\) 行を作れない」直接の型上の理由である。

### 2.4 `GEN-COVER-140` — GEN-AFF の独立停止点

一段の elementary abelian refinement で、固定した下段行 \(t\) の relation 解空間は

\[
 \mathcal S_t=\{v:A_tv=b_t\}=v_0+\ker A_t
\]

である。`GEN-AFF` により、生成に失敗する条件は、\(V\) の proper \(W\)-submodule \(J\) ごとに定まる affine 条件 \(\mathcal B_{t,J}\) の有限和集合になる。従って一様供給の正確な形は

\[
 \boxed{
 \mathcal S_t\setminus
 \bigcup_{J<V,\ J\ W\text{-stable}}\mathcal B_{t,J}
 \ne\varnothing
 \quad\text{for every qualified }(L/K,t).}                         \tag{GEN-COVER}
\]

relation 可解性は (GEN-COVER) を含意しない。既走の 21 次元 component でも、ある行では affine 解 81 個中 1 個が非生成、別 component では 27 個中 3 個が非生成だった。有限実例では少なくとも一つ生成解が残ったが、任意の非半単純 module、任意の composition length、任意の mixed roof で上の有限和集合が解空間全体を覆わないという下界はない。

従って便 139 の停止点 3 は、曖昧な「生成定理不足」ではなく (GEN-COVER) という有限体上の affine-subspace non-covering 命題である。これは (REL-VANISH) と論理的に独立である。

### 2.5 経路独立性 — 三経路が同じ場所で止まる

**経路 A: Cor 5.4 の有限排除路.** 固定した \(g\) について (0.1) を直接使う。一つでも空 fiber があれば出口 II、全て非空を言うには全細分量化が残る。現在は前者の一件も後者の族定理もない。

**経路 B: Thm 5.2 / Mittag--Leffler 路.**

\[
 Y_K(g):=R_{K,M}^{-1}(g)
\]

と置くと、求めるものは有限集合系の逆極限 \(\varprojlim_KY_K(g)\) の元である。全ての \(K\) で \(Y_K(g)\ne\varnothing\) まで示せれば、細分順序の directedness（有限個には共通細分がある）から有限交叉性が従い、有限離散 fiber の compactness で逆極限は非空になる。小さい名前付き族からこの全称前提を得るには cofinality と各局所 fiber の非空性が必要であり、遷移全射 / ML はその十分な構成機構である。その局所全射を示す条件が (REL-VANISH)、(GEN-COVER)、charming の同時実現である。従って逆極限へ移っても同じ三前件に戻る。

**経路 C: 導来複体 / 有限群直接路.** 線型化した最初の障害は (2.4) の relative class であり、直接有限群列挙では同じものが rank

\[
 \operatorname{rank}[A_t\mid C_tZ]-\operatorname{rank}A_t
\]

として現れる。これが零でも、非線型な source generation は (GEN-COVER) として残る。これが正なら一行の候補を直接測定できるが、既走有限宇宙では正値 0 だった。

三経路とも、選んだ \(T_t\) や基底には依存せず、結局

\[
 \text{一つの実 fiber の空性}
 \quad\text{または}\quad
 \text{全細分の fiber 非空性を与える cofinal 族定理}
\]

の二択へ戻る。従って現在の障害は chain-homotopy という一つの証明案の artifact ではない。

### 2.6 `NO-FINITE-B-140`

> **命題.** 有限部分族 \(\mathcal F\subset\mathcal I_M\) が noncofinal なら、「全 \(K\in\mathcal F\) で \(R_{K,M}\) が全射」と像の refinement-monotonicity だけから、(0.1) の全称結論は従わない。

**証明.** noncofinality により、どの \(L\in\mathcal F\) も下に入らない \(K_0\) がある。像を \(\mathcal F\) 上では \(GT(M)\)、\(K_0\) の down-set 上では真部分集合 \(A\) と置き、共通細分でも \(A\) と置く抽象逆系は monotonicity と有限成功を満たすが、全称結論を満たさない。実際の系でも `MONO-CNF-139` により、\(K_0\) で像が真部分集合ならその下は全て非全射である。逆に cofinality があれば同命題と COMPACT で閉じる。∎

これは有限計算量の上限ではなく、有限観測から全称命題へ渡す論理前件の欠落である。

## 3. 資源授権の実行と有限生値

### 3.1 便 137 の \(T_t\) family を再走・収蔵

欠品は解消した。

| 成果物 | SHA-256 | 内容 |
|---|---|---|
| `search/certs/cocycle_absorb_137_t_families_v1_20260815.json` | `adf9ceb2e074792ebc6b381fb595783716e2697e85db31188f7f22163f364c34` | \(Z,A_t,C_t,T_t\) の digest、全 1,620 個の \(T_t\) 本体、行別 residual、摂動陽性対照 |
| `crosscheck/verdicts/cocycle_absorb_137_t_families_check_v1_20260815.json` | `1baba05dacd4ce0bbeefb4cbbefc62f37fbd8fc44c07fe1800024140a2b39ebf` | 別 heart 基底の標数 3 checker と pure bit-column 標数 2 checker |

producer は既存 relation symbol から \(A_t,C_t,Z\) を再構成し、辞書式 RREF particular solution で

\[
 A_tT_t+C_tZ=0
\]

を解いた。五つの family digest は便 137 本文の既開示値と全て一致した。

| family | 行 | \(Z\) shape | \(C_tZ\ne0\) 行 | family SHA-256 |
|---|---:|---|---:|---|
| orbit bundle \(+\) | 324 | \(42\times25\) | 318 | `908ab5a5ecadea831de659e7bf10e0ba9076e7358385ec8a6d3e221775aa60e3` |
| orbit bundle \(-\) | 324 | \(42\times24\) | 318 | `74aa14c12412374d5fc1dabe345b48bcddf05d85546f51da94c82709ba1defd0` |
| trivial character \(+\) | 324 | \(14\times10\) | 312 | `63370f3bb33646e6ac13964083386315163275f4353491ea08d185af204cc532` |
| trivial character \(-\) | 324 | \(14\times9\) | 312 | `25f77f013b2955a86d985062d2fd60664e03d427b63bbad6d9274717395f0697` |
| support-two orbit | 324 | \(24\times15\) | 297 | `565401498a6d2442fb671b4c04a19f3fa0d13b25e5c1f04da6e395a50065bb4c` |

producer residual 非零は 0 / 1,620。checker は producer の \(T_t\) を読まずに \(A,C,Z\) と自身の particular solution を再構成し、包含または residual failure 0 / 1,620。各 family で \(C_tZ\) の一座標を像外へ摂動した陽性対照は rank 差 \(0\to1\) を検出した。

これは既に値が開示された family の **再現走**であり、新候補の outcome を開く prospective run ではない。そのため「事前に未知値を凍結した」とは記載しない。照合済み有限結論であり、Lean による証明ではない。

再現の本体は、各 component について既存 producer の `model_data()` / `build_model()` を呼び、

```text
Z = nullspace(diag(1+theta, 1+tau+tau^2))
T[:,j] = solve_columns(A, -C*Z[:,j])
assert rank(A*T + C*Z) == 0
sha256(canonical_json([T_t for t in 0..323]))
```

を実行するものである。cert は使用した全 source SHA と \(Z,T_t\) 本体を持つ。

### 3.2 試した有限範囲と、尽きた意味

判定語を入れず、生値だけを列記する。

| lane | 凍結有限宇宙 | 生値 |
|---|---:|---|
| COCYCLE component | 5 × 324 = 1,620 template | residual 非零 0、§2.3 の相対余核次元は全て正 |
| C1--C3 | 10 marked orbit/class × 324 = 3,240 rank template | \(r_t^{\rm obs}>0\) は 0、class outcome 開封 0 |
| ESCAPE-28 | 3,392 class × 324 = 1,099,008 行 | nonzero obstruction 0、generation-absent 0 |
| ESCAPE-2 | 7 class × 324 = 2,268 行 | nonzero obstruction 0、generation-absent 0 |
| perfect `[16,7,3]` | 16 × 387,072 = 6,193,152 緩和行 | missing key 0、raw image 972 が 16 / 16 |
| perfect `[16,8,4]` | 32 × 774,144 = 24,772,608 緩和行 | missing key 0、raw image 972 が 32 / 32 |
| Magnus cutoff 5 | 972 target 元 | 各元の lift 数 16 |
| split MCOV 較正 | 119 組 | failure 0 |

ここで有限 inventory が「尽きた」とは、便 138 の C0--C15 のうち、既存データから prospective に有限化できた候補、構造定理で除外できた候補、および入力欠品を明記できた候補を全て処理したという意味に限る。次は未消費である。

- isolated refinement 全体。次数または指数の上界がない。
- C4/C6 の modular Ext database と cohomology-to-presentation compiler。
- C8 の非可換 quotient、C9/C11 の mixed \(S_4\) / Goursat target list。
- compatible pair の \(q_U,q_Z,q_R\) と isolated certificate を同時に持つ \(D\)-census。
- 多段 tower の cofinality。

従って「非零障害像を有限範囲で作れなかった」は正しいが、「非零障害像が存在しない」は導かない。反対に §2.3 は、\(D\) 自体の非零性なら既に容易に起き、決定力を持つのは \(\omega\) の像であることを示す。

### 3.3 GAP / GHA を使わなかった理由

本便で GHA を発火しなかった理由はローカル GAP の故障ではない。現在欠けているのは、GAP に渡す次の有限入力である。

1. \(PB_3/M\) へ標識整合に全射する有限群 \(E\) の presentation。
2. \(B_3\)-安定な kernel \(L\subset M\) と isolated certificate。
3. base-change の \(q_U,q_Z,q_R\) を作る marking / relation map。
4. 重複なしの候補リストまたは order/index bound。

GHA は指定した有限リストを走査できるが、上界のない \(\mathcal I_M\) を自動的に finite complete list へ変えない。候補なしに任意の `.g` を発火することは「環境を理由に落とさない」ことにも、出口 I/II にも寄与しない。§4.1 の次数別列挙器が用意されれば、その各有限段は GHA へそのまま渡せる。

## 4. 決着に必要な品の可算化

### 4.1 出口 II の完全に具体的な半決定計算 `ISO-FIBER-ENUM-140`

整数 \(B=1,2,3,\ldots\) の順に、次を行う。

1. 位数 \(\le B\) の有限群 \(E\) と全射 \(\phi:PB_3\twoheadrightarrow E\), \(\psi:E\twoheadrightarrow PB_3/M\) の組で、\(\psi\phi\) が固定商写像に等しいものを marked isomorphism ごとに重複なく列挙する。
2. \(L=\ker\phi\subset M\) について \(B_3\)-安定性を証明書化する。
3. 全 \([m,f]\in GT(L)\) の settled 条件を全数検査し、\(L\) の isolated certificate を作る。
4. \(R_{L,M}(GT(L))\) を producer と独立 checker で作り、位数 324 または、同値に \(GT(M)\setminus A\) の一元の fiber 0 を保存する。

これは countable で、出口 II が真なら有限段で停止する。しかし witness がない場合の停止上界はない。必要な実装欠品は **finite marked quotient enumerator + isolated certifier** の二つであって、「もっと計算する」ではない。

### 4.2 出口 I に十分な四命題

次の四本を同じ cofinal family \(\mathcal U\) について示せば COMPACT が発火する。

1. **`CHIEF-COFINAL-140`**: 任意の isolated \(K\subseteq M\) の下に \(L\in\mathcal U\) があり、\(L\to M\) は \(B_3\)-安定な chief factors の有限鎖へ分解する。非可換 chief factor も別枝として含める。
2. **`REL-VANISH-140`**: 鎖の各可換段・全 roof 行で、(2.4) の relative class から \(H^1(\mathcal K_L)\) への \(\omega\) 像が零。
3. **`GEN-NONCOVER-140`**: 同じ各段・各行で (GEN-COVER) が成立する。すなわち relation affine space が proper-submodule bad loci の和で覆われない。
4. **`CHAR-LIFT-140`**: 固定した base の \(m\)-fiber と、2・3 の同じ解との間に compatible charming representative が存在する。

`REL-VANISH-140` のさらに局所的な十分条件は、全段で (STRICT) を示すこと、または直接

\[
 H^1(\mathcal F_{L/K,t})\longrightarrow H^1(\mathcal K_{L,t})
\]

が \(\omega\) の relative lift を殺すこと。自然な chain homotopy を採る場合に限り、追加計算対象は (2.6) の特定 Ext class \(\delta(C)\) の零性である。

このリストは「自然な splitting を探す」という曖昧な依頼ではない。各項目に入力 object、量化、出力があり、反対向きに倒れればその場で §4.1 の一行候補になる。

## 5. 規律・provenance・終盤勘定

### 5.1 novelty receipt

初稿前に

```text
rg -n -S "STRICT-D-140|CONE-D-140|NO-FINITE-B-140|GEN-COVER-140" \
  docs sol search crosscheck provenance ops \
  --glob '!sol_task_140_finish.txt' --glob '!sol_reply_140_finish.md'
NO_PREEXISTING_HITS
```

を得た。これは文字列の未出だけを示し、数学的優先権の主張ではない。

### 5.2 provenance と変更範囲

- `sol/sol_reply_139_threetheorems.md` SHA-256: `f6908af4337cce3cdbcb1fe918f066ca3e0d40b256c3b56cc7e96f8974201fba`
- `sol/sol_reply_138_campaign.md` SHA-256: `63053ab9613bec1a6ed1fcdb0d2b902c77581cbb11fcd406e79917fff8b70ed6`
- `search/certs/campaign138_compact_preflight_v1_20260815.json` SHA-256: `81e25f53c1a7494481660b3bd405116020897d8f7ba94607769947980f86bec2`
- 本便で作成したものは、指定返書と、委嘱 §3 が明示要求した \(T_t\) raw cert / 独立 checker cert の三ファイルだけである。
- 作業開始前からの dirty / untracked file は変更していない。
- `.git` は read-only。commit、push、workflow dispatch は行っていない。

### 5.3 noncontact / NAME-COLLIDE / endgame

- sealed three quantities: opened = false
- \(u\): opened = false
- \(c\): opened = false
- sealed K5: opened = false
- NAME-COLLIDE: 本書の \(D_{L/K,t}\) は cokernel-kernel、\(\mathcal D\) や dihedral 群の記号ではない。\(W\) は quotient、\(V\) は相対 kernel として分記した
- 判定語は §§0–1 と最終行に隔離し、§3 の cert は raw linear-algebra / finite-group 値だけを持つ
- `endgame_scope`: gentle side only。B₄ `PENT_W-PASS` = NOT_RUN、`FAKE-KILL^{B_4}` = NOT_RUN、U-10 = NOT_RUN

### 5.4 最終裁定

出口 I に必要な全称・cofinality と、出口 II に必要な一つの有資格な空 fiber のどちらも、現前件からは導けない。さらに `STRICT-D-140` の明示反モデルにより、`ABSORB-BC-139` だけから全吸収を導くことは不可能であり、有限観測だけから反対側を認定することも `NO-FINITE-B-140` により不可能である。

これは bit の値が数学的に存在しないという主張ではない。**本便へ渡された定理・有限成果物・計算対象だけでは、その bit を厳密に導出できない**という裁定である。値を装うことなく採れる唯一の出口は III である。

VERDICT: IMPOSSIBLE_WITH_REASON
