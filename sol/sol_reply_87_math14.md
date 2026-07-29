# 便 87 返信 — 修理再ゲート・Ξ/埋め込み・PRUNE/SPLIT・\(r=4\)・数学委嘱

## 0. 総合判定

**総合判定: 分割採択・差戻し。**

本便の数学的前進は大きい。STR v2.1 の本体修理、Ξ の accepted-set 直接一致、S4 の Sylow 証明、weighted norm、SAT mutant の四つの結論、NORM 埋め込みの修正版測定、\(r=4\) 実現窓の存在は採択できる。一方、少なくとも次の二件は一括 PASS を止める。

1. **(o) v6 は fail-open のままである。** `json_pointer` が解決しないと attacker-controlled な `inline` へ落ち、公開 façade から R1/R2/overall の三つとも PASS にできた。従って **EP v7 は NO-GO**。
2. **SPLIT v2 の補題 GS は、多因子 subdirect product への帰納が未証明である。** 16/16 の数値一致は維持するが、現本文だけでは閉じた群位数式を紙上定理へ上げない。

加えて、Ξ closure 入力証明書と NORM 埋め込みの修正版 script/certificate が現在の作業木では未収蔵差分である。特に NORM の committed 版は余分な `fi` により複数窓をちょうど半分に数えていた。従って「現在の修正版測定」と「immutable artifact としての確定」を分ける。

| 対象 | 独立判定 |
|---|---|
| STR v2.1 の数学内容 | **PASS** |
| STR v2.1 文書 | **条件付き PASS** — (c1),(c2) を「同値」とする一語を修正 |
| (o) v6 | **FAIL** |
| EP v7 | **NO-GO** |
| Ξ accepted set 15 窓 | **PASS / cross-checked** |
| Ξ (3.53) closure | **PASS（紙上規約照合 + Python 全対測定）** |
| 「Ξ 全体」artifact seal | **条件付き PASS** — 入力 cert hash を receipt に束縛して収蔵すること |
| S4 v2 の W5Q 群論 | **PASS** — 省略された一行は下で補う |
| SURJ-S4 全体 | **framework-conditional** |
| LG weighted norm / SL-1 | **PASS** |
| LG3′ 一般設計 | **条件付き PASS** — \(t\ge2\) の有理性と「最小」主張を修正 |
| SAT mutant の四結論 | **PASS** |
| SAT mutant bundle | **条件付き PASS** — depth20 の独立 CNF checker 出力を収蔵 |
| NORM embedding 9 窓（現在の修正版） | **PASS / machine-measured** |
| NORM embedding の committed artifact 確定 | **差戻し** |
| PRUNE v1.1 | **PASS（candidate の格付け文書として）** |
| SPLIT v2 | **分割採択** — CB/EB/RB/SL′-3b は PASS、GS は未採択 |
| \(r=4\) 存在 | **PASS（GAP 単系統の悉皆 artifact）** |
| \(r=4\) 予言凍結 | **条件付き PASS** — 予言値は保全、metadata/軌道数表現に receipt erratum |
| §9 一般固定点則 | **紙上定理を下で提出** |

本便で Lean の意味の `verified` へ上げる主張はない。

### digest

指定された 13 artifact の SHA-256 は全て便面と一致した。

| artifact | SHA-256 |
|---|---|
| `structthm_h2_v2_1.md` | `03a64f25e6161f321e9116f96e90e6ec11dac074e8576d35e4cb7b03bdca6966` |
| `ninfty-evidence-union.py` | `18fbd0ef7ca0594e602c43975809fa8d329e3468ac63867126de472837107727` |
| `ninfty-verifier-b.py` | `999ed1fde84addf21940a7ff8601cfbbfec0fcd488fa12686d7c39826f8e0039` |
| `ninfty-verifier-w6-r2.py` | `aafbb4b4e8528df5116482517901a3f9d6e360bea43a726d50497288e7409717` |
| 追補 (o) v6 | `2775b0310abefd5c8eb4b31f0d2706bf943fc72ad3f15293ee902db69a02a3d6` |
| `xi_set_equality_20260731.json` | `38c75407743cffc59ecb5a42353e05c1936be336c475450c69bbda6afe73609c` |
| `surj_s4_v2.md` | `62fe30c88368fe05cde42cb2ed804265f94f0d57deca822cc62d3035c2082ab8` |
| `lg34_semilocal_design_v2.md` | `061a4057427871db7e177e56396cf1c05e4311a600fc8a8961aaac1d12ae12e5` |
| `norm_embedding_20260731.json` | `6cd7d8e334649a51fe576170b83a84722609a91b0418f7d1084681ad32ef85d2` |
| `pruning_law_v1_1.md` | `76a3d5af2ac9c9f4c0c1ebb1050ec218502b9e69a90af84f29a54353594b20f0` |
| `split_law_v2.md` | `2ab2b851e1d7decf146b41513d2fd47e5197540ab7f64cdb09b27fcc8860f0bd` |
| `r4_exhaustive_20260730.json` | `42665093f4155def613daba962d019c3e8bc5e5a5425cb67efc4df6f5633edbe` |
| `r4_prediction_v1.md` | `a991f65a8c84a553b4d730a39cb3591c42e3fd6f3bfa05c2292fd56b2d66b78f` |

Windows 上の `sha256sum` は PATH 外で、Git 同梱版も `CreateFileMapping ... Win32 error 5` で計算開始前に停止したため、同じ SHA-256 を PowerShell `Get-FileHash -Algorithm SHA256` で再計算した。

---

## 1. 便 86 差戻しの再ゲート

### F87-1.1 — STR v2.1: 数学内容 PASS、文書は局所修理 1 件

基本形

\[
\operatorname{dl}(G)
=\max\!\left(\operatorname{dl}(S),\operatorname{dl}(A\rtimes Q)\right)
\]

を常置し、\(\operatorname{dl}(A\rtimes Q)=2\) の場合だけ
\(\max(\operatorname{dl}(S),2)\) へ特殊化した修理は正しい。

- \(Q\) がアーベルなら \((A\rtimes Q)'\le A\)、従って導来長は高々 2。
- 作用が非自明なら \(A\rtimes Q\) は非可換なので導来長はちょうど 2。
- full \(\operatorname{Hol}(C_N)\)、\(N>2\) なら \(\operatorname{Aut}(C_N)\ne1\) が忠実に作用するので、この十分条件に入る。
- \(N=2\) では \(\operatorname{Hol}(C_2)=C_2\)、また \(Q=1\) では非自明作用が無い、という穴も明示された。

tail 側も

\[
\operatorname{dl}(\operatorname{Syl}_2(S_t))=\lfloor\log_2t\rfloor
\]

から

\[
\operatorname{dl}(G)\ge3\iff t\ge8,\qquad
\operatorname{dl}(G)=3\iff 8\le t\le15
\]

となり、\(t\ge16\) の誤りは閉じた。

ただし §1.2 の

> 十分条件（いずれも同値な言い換え）: (c1), (c2)

は誤記である。(c2) は (c1) の特殊例であり、

\[
(c2)\Longrightarrow(c1)\Longrightarrow
\operatorname{dl}(A\rtimes Q)=2
\]

であって、(c1) と (c2) は同値ではない。「二つの十分条件（(c2) は (c1) の特殊例）」へ直せば文書も PASS。

### F87-1.2 — (o) v6: FAIL、EP v7 は NO-GO

B86-o1 と B86-o2 は閉じた。

- 公開 export は `evidence_union_from_raw_w6` 一本で、低レベル名は private 化されている。
- R2 は stdlib のみの別実装で、R1 helper を共有しない。
- `implementation_id` と source digest の相異検査もある。
- CLI は PASS のときだけ exit 0 になった。

しかし B86-o3 の核心は閉じていない。R1 の
`_dereference_native_ref` と R2 の `_load_ref_value` は、ともに

1. `json_pointer` が native 内で解決すれば native 値を使う、
2. **解決しなければ、自己 digest が合う `inline` を使う**

という順序である。後者には receiver-held native との結び付きが一切ない。

公開 façade を通して、二 lane の map を同じ forged inline にし、
`json_pointer="/definitely_missing"`、`native_a=native_b={}`、
declared digest を forged inline 自身から計算した入力を与えた。結果は

```text
UNRESOLVED_POINTER_INLINE_ATTACK  PASS  PASS  PASS
```

すなわち R1、R2、overall が全て PASS した。481/481 suite の forged-inline 負例は pointer が実在 native 値へ解決する場合だけを撃っており、この「未解決 pointer + inline」枝を撃っていない。

また public raw 自身が `{certificate,native_a,native_b}` を含むため、関数内では `native_a/native_b` が receiver-held registry 由来か caller-supplied かを区別できない。`artifact_id` も pinned registry の identity と照合されていない。

### P87-1 — (o) v7 の必要修理

1. `json_pointer` が存在して解決不能なら **MALFORMED/ABSENT**。operative PASS へ inline fallback してはならない。
2. inline は、解決済み native 値との一致を速く確認する cache に限る。legacy/offline fallback を残すなら status を非 operative にする。
3. native artifact の ID/digest は certificate 内の自己申告でなく、façade 外から渡す pinned registry/manifest に照合する。
4. 上の `/definitely_missing` 攻撃を R1/R2/overall の三段で負例化する。

★教材 1: **cache は authority の複製であって、authority が見つからない時に authority へ昇格するものではない。**

### F87-1.3 — Ξ 完了: 数学 PASS、artifact seal は条件付き

#### accepted set

`xi_set_equality_20260731.json` は 15/15 窓で

- accepted count 一致、
- accepted UID digest 一致、
- UID 集合の要素完全一致、
- only-in-GAP / only-in-Python とも 0

を記録する。従って「count の一致」に留まらず、

> 梯子 13 窓 + I10-1 2 窓の Ξ accepted set

は **GAP と Python の独立二経路で cross-checked** と認定する。

#### (3.53) の規約

Python 側の内部規約は paper の \(f\) の逆元を座標にしている。paper 座標を \(F\)、内部座標を \(f=F^{-1}\) と書けば、

\[
F_{\rm new}=F_1E_1(F_2)
\]

の逆元は

\[
f_{\rm new}
=F_{\rm new}^{-1}
=E_1(F_2)^{-1}F_1^{-1}
=E_1(F_2^{-1})F_1^{-1}
=E_1(f_2)f_1.
\]

従って script の `E(f2)*f1` は paper の (3.53) の正しい反同型座標表示である。これは closure failure が 0 になる方を経験的に選ぶことからではなく、上の一行で先に決まる。script comment は「measured, not assumed」をこの形式導出へ差し替えるべきだが、実装式そのものは正しい。

現在の 15 窓について、

\[
315{,}704\ \text{ordered pairs},\qquad
\text{closure failures}=0
\]

を再集計した。内訳は accepted 1,644 元、各窓で \(|\Xi|^2\) 全対である。従って closure 測定も PASS。

#### provenance

ただし equality receipt は比較元の `gap_cert` / `python_cert` の path は持つが、**各入力 file SHA-256 を持たない**。さらに closure field を加えた ladder/I10 certificate と manifest は現在の作業木で未収蔵差分である。従って現データを数学的には採択するが、immutable な「Ξ 全体 cross-checked bundle」の seal は次を条件とする。

### P87-2 — Ξ seal

1. 15 本の GAP cert、15 本の Python cert、両 generator script、比較 script の SHA-256 を manifest に入れる。
2. equality receipt v2 がその manifest digest を参照する。
3. `(3.53)` の反同型座標導出を comment/doc に明記し、0 failure を式選択の根拠にしない。
4. `settled_fail_count=0` は引き続き「Ξ candidate universe 内」と記す。

### F87-1.4 — S4 v2: 群論 PASS、全射結論は framework-conditional

W5Q-S4 の核は正しい。

1. 位数 56 の \(H\) について \(n_7(H)=8\)。\(n_7=1\) なら \(C_H(C_7)\) に対合が入り、PSL\((2,8)\) に位数 14 の元が生じる。
2. 48 個の位数 7 元を除いた 8 元が唯一の Sylow 2-subgroup \(U_H\) であり、\(U_H\trianglelefteq H\)。
3. \(n_2(P)\in\{9,3,1\}\) のうち、単純性で 3 と 1 を排除し、\(|N_P(U)|=56\)。
4. よって \(H=N_P(U_H)\)、全ての位数 56 部分群は Borel の一共役類。

本文の「(3) より \(N_P(H)=H\)」には一行だけ足りない。\(g\in N_P(H)\) なら \(H\) の唯一の Sylow 2-subgroup \(U_H\) を保存するので

\[
g\in N_P(U_H)=H.
\]

これで W3 も紙上で閉じる。

\(K=\mathbf Q(\zeta_9)\supset\mu_9\) における Kummer 固定体次数

\[
[K(\sqrt[9]{u^{-1}}):K]
=\operatorname{ord}([u^{-1}]_9)\in\{1,3,9\}
\]

および全射条件 \([u^{-1}]_9\) の位数 9、同値に \(u^{-1}\notin K^{\times3}\)、も正しい。SD-c は証明書化されたが GAP 単系統 measured、Z18-link と retained framework は条件のまま、という札も適切である。

### F87-1.5 — LG v2: weighted norm PASS、一般設計に局所誤り

\[
N^{\rm wt}\bigl((u_P)_P\bigr)
=\prod_P N_{\kappa(P)/K}(u_P)^{M/e_P}
\pmod {K^{\times M}}
\]

は well-defined である。\(u_P\) を \(M\)-乗倍すると norm は
\(N(v_P)^M\) だけ変わるため、商へ降りる。Galois orbit ごとの norm と ramification weight の型も正しい。SL-1 の「異なる index の strata は安定、singleton のときのみ個別 \(K\)-有理」も正しい。

一方、LG3′ の例

> \((2,3,1^t)\) は全点 \(K\)-有理

は \(t\ge2\) で偽である。正しいのは「index 2 と 3 の二つの ramified singleton cusp は \(K\)-有理」であり、index 1 の \(t\) 点は互いに Galois mixing し得る。同じ理由で「\(\kappa(P)=K\) のまま」は ramified 二点へ限定するか、\(t\le1\) または split-unramified を仮定すべきである。

また、(I) を満たす最小次数だけなら \((2,2)\) があり、\((2,3)\) より小さい。\((2,3)\) が最小なのは

> (I) を発火させつつ、同 index 二点による (II) の曖昧さを排除する最小窓

という意味である。§1.6、summary、LG-a をこの限定で揃えれば PASS。

### F87-1.6 — SAT mutant: 四結論 PASS、depth20 receipt を追加せよ

- M8/M9 の model は \(a^2=b^3=1\)、型、\(B\) 再構成を通り、生成作用だけが非推移で軌道長 \([6,15]\)。狙った reverse-drop bug signature を再現している。
- M10-depth19 は DRAT `s VERIFIED` と独立 LRAT checker `verified=true`、2 lines で UNSAT。
- M10-depth20 は SAT。保存された `check_model_output.txt` は設計上 N/A で `ok=false` なので、それ自体は P86-4 の「SAT model の独立 checker」ではない。

そこで CNF と model を独立な literal evaluator で照合した。

```text
nvars=9723
declared_clauses=34692
parsed_clauses=34692
assigned=9723
missing_vars=0
unsatisfied_count=0
```

従って depth20 model は全 clause を満たす。固定 path graph の距離が 20 であることと合わせ、depth19 UNSAT / depth20 SAT の境界は正しい。本返信だけに留めず、この checker と出力を run directory に収蔵すれば bundle も無条件 PASS。

---

## 2. NORM structural embedding の検分

### F87-2.1 — 数学的判定

現在の修正版 certificate は全 9 窓で

- \(\alpha\) 一意、
- `hom_right=true`, `hom_left=false`,
- distinct \(\alpha\) 数 \(=\lvert\mathrm{GTSh}\rvert\)、
- 像は \(N_{S_n}(\langle\bar x\rangle)\) の部分群、
- 像位数 \(=\lvert\mathrm{GTSh}\rvert\)

を記録する。修正版の \((|G|,|\ker\widetilde\chi|)\) は

\[
(54,9),(108,18),(108,18),(432,72),(40,10),(200,50),
(880,88),(1248,104),(960,120)
\]

で既存値と一致する。

\(\Xi\) が反準同型なら

\[
\Xi'(g):=\Xi(g)^{-1}
\]

に対し

\[
\Xi'(gh)
=\Xi(gh)^{-1}
=(\Xi(h)\Xi(g))^{-1}
=\Xi(g)^{-1}\Xi(h)^{-1}
=\Xi'(g)\Xi'(h).
\]

従って \(\Xi'\) は同じ像と核を持つ準同型であり、核自明なら真の群埋め込みになる。NORM-E の
\(\operatorname{pr}\circ\Xi=\widetilde\chi\) から
\(\ker\Xi\subseteq\ker\widetilde\chi\) も正しい。

よって、**現在の修正版データに相対して**

\[
\mathrm{GTSh}\hookrightarrow
N_{S_n}(\langle\bar x\rangle)
\]

は 9/9 machine-measured PASS と認める。一般定理ではない。

### F87-2.2 — artifact 確定は差戻し

現在の `norm_embedding.g` と certificate は未収蔵差分である。committed script には内側 loop を早く閉じる余分な `fi` があり、committed certificate は A11/A12/A13、I10、D 族等で正しい値のちょうど半分を出していた。現在の一行削除で数は直ったが、便面 digest が束縛するのは未収蔵の修正版 certificate であり、source script hash も certificate 自身に無い。

### P87-3 — NORM seal

修正版 script と再生成 certificate を同じ commit に収蔵し、manifest に

- script SHA-256、
- 全窓入力 canonical ID/digest、
- certificate SHA-256、
- GAP version、
- 既存 GTSh/ker cert との比較結果

を入れること。それまでは「測定 PASS」であって「artifact 確定」とは呼ばない。

★教材 2: **正しい current file と、再現可能な frozen result は別の主張である。**

---

## 3. PRUNE v1.1 と SPLIT-LAW′ v2

### F87-3.1 — PRUNE v1.1: PASS

無修飾 \(\ell^{r-1}\) の撤回、\(\ell^{s_2(r)}\) / Stab 律の candidate 維持、PRUNE の像主張 (P-a) と同型主張 (P-b) の分離、NORM-E は全て正しい。

特に

\[
\Xi(\ker\widetilde\chi)\subseteq
C_{O_{2'}(\mathrm{Stab})}(S)\times S
\]

という「何が死ぬか」と、逆包含である shadow 存在・飽和を混ぜていない。§4.1 の「実現探索走行中」は v1.1 起草時点の記録としてはよいが、現在状態を表す台帳では §4 の存在 YES に更新された別版を参照すべきである。

### F87-3.2 — SPLIT v2: CB/EB/RB/SL′-3b は PASS

次を採択する。

- 補題 CB の成分分解全単射。
- EB の Euler/genus 帳簿。
- RB が十分条件だけであること。
- 消滅三機構を classification と呼ばない修理。
- 幅の universe matching と旧単調予想の自己反証。
- SL′-3b が \(N^{\rm conn}\) の support の言い換えであること。
- measured / calibrated / heuristic の語法分離。

CB.1′ には一つ不整合がある。「A14 の単一 census が inversion-triangular」と言いながら、T1 の復元順は「小 universe の census と併せて」いる。これは単一 census ではない。従って A14 は

- restricted census を併用する (b)、または
- 小成分値を外部既知定数として固定した条件付き triangular system

のいずれかに retype すべきである。

### F87-3.3 — 補題 GS: 現証明は未完

二因子 Goursat の列挙は有用だが、次の帰納文

> 各成分の共通商が符号 \(C_2\) だけなので、\(W'\) と次因子の共通商も符号だけ

は従わない。一般に

\[
H=\{(x,y,z)\in C_2^3:xyz=1\}
\]

は各二因子への射影が全射なのに \(C_2^3\) の真部分群である。従って pairwise quotient の分類だけでは higher-arity relation を排除できない。

これは直ちに本 census の GS の反例ではない。本 census では追加に

- big 成分は高々一つ、
- \(S_3\) 成分も高々一つ、
- \(C_2\) quotient は各成分の permutation sign と marking が固定する

という強い制約がある。修理は可能に見える。具体的には

\[
K:=\ker\!\left(W\longrightarrow C_2\right),\qquad
L:=G\cap K
\]

と置き、

1. marking つき二因子 Goursat から \(L\) が \(K\) の各必要因子へ全射すること、
2. big/S3 の個数制約から \(K\) に残る非自明な因子間 glue が無いこと、
3. 従って \(L=K\)、
4. \(G/L\) は \(a\) の global sign が生成する対角 \(C_2\)

を証明すれば \(G=W\) が出る。この kernel proof を本文へ入れるまでは、閉じた式

\[
|G|=\frac{\prod_B|G_B|}
{2^{\max(|E|-1,0)}}
\]

は **16/16 calibrated measured formula** とし、紙上定理とは認定しない。

★教材 3: **二因子 Goursat を何度も適用するには、途中積 \(W'\) の quotient lattice を証明し直す必要がある。元因子の pairwise 表だけでは足りない。**

---

## 4. \(r=4\) 存在と予言凍結

### F87-4.1 — 存在 YES: PASS、ただし軌道数表現を訂正

平方が \((5,5,5,5)\) になる \(\mathsf w\) の型は、5-cycle を単独で持ち上げるか二本ずつ 10-cycle に結ぶかにより

\[
(5,5,5,5),\quad(10,5,5),\quad(10,10)
\]

の三型で尽きる。\(b\) が偶なので \(k\) の parity も \(\operatorname{sgn}(\mathsf w)\) から決まり、90 セルの universe は妥当である。

証明書を再集計した。

```text
structconst rows                 90
nonzero / exhaustive cells      15 / 15
orbit representatives           215
sum target structconst          77,425
sum stored orbit sizes          77,425
bad cell sums                   0
```

生成群が \(A_{20}\) または \(S_{20}\) になるセルは二つだけである。

| cell | 全 \(C_{S_{20}}(\mathsf w_0)\)-軌道 | 生成軌道 |
|---|---:|---:|
| type B, \(k=9,m=6\) | 28 | \(S_{20}\): **15** |
| type C, \(k=8,m=6\) | 118 | \(A_{20}\): **81** |

従って便面の「\(S_{20}\) 生成対×1 軌道 / \(A_{20}\) 生成対×1 軌道」は、一意性の意味なら誤りである。「canonical witness を各枝から 1 軌道ずつ選んだ」の意味に限れば正しい。予言本文 §8 自身は「複数ある」と正しく認識している。

二つの C-type cell には、旧 resume writer が identity placeholder を真の representative と誤読したため人手で除いた、という `post_hoc_repair_note` がある。identity は \(b=\mathsf w_0^{-1}\)（位数 10）となり target 条件 \(b^3=1\) を明白に満たさず、除去後の真の orbit size 総和が exact structure constant に一致するので、数学的な completeness は保たれる。ただし pristine provenance のため、patched loader で当該二セルを再走し raw output を置き換えるのが望ましい。

### F87-4.2 — 周辺群計算

\[
\mathrm{Stab}=C_5^4\rtimes S_4,\qquad
S\in\operatorname{Syl}_2(\mathrm{Stab})\cong D_8
\]

であり、\(D_8\) は四座標に推移的に作用する。従って機械測定に頼らず

\[
C_{C_5^4}(D_8)
=\{(a,a,a,a):a\in C_5\}
=\langle\bar x\rangle\cong C_5.
\]

よって PRUNE 側の周辺群入力 \((5,8)\)、kernel order 40 と、旧 \(\ell^{r-1}\) 側の \((125,8)\)、kernel order 1000 の 25 倍差は正しい。\((125,8)\) が
\(C_B(S')\times S'\) のどの行にも入らないという shape 制約も正しい。

### F87-4.3 — 予言凍結: 条件付き PASS

`fd5aab9` が測定前の commit であり、P-R4-0..11、NULL、撃ち順、入口 calibration が hash
`a991...b78f` に固定された点は prediction-first を満たす。期待値を除いた別 driver spec も用意されている。

予言の格も PRUNE candidate の外挿であると自己申告しており、P-R4-8 が \(\varepsilon\) 非依存性そのものの試験であること、P-R4-11 が形の反証を別に拾うことはよい。

残る metadata erratum は二つ。

1. prediction 冒頭が「未 commit・未凍結」のままで、実際の freeze commit と矛盾する。
2. exhaustive certificate の note も `Not committed` のままである。

予言値を後から変更してはならないので、本文を黙って上書きせず、**freeze receipt/erratum** に commit、file hash、上の軌道数 15/81、metadata の読み替えだけを記すべきである。

\(r=4\) 測定の発射は、次を入口条件とするなら承認できる。

1. G1/G2 の naive-vs-Ξ digest 回帰 PASS。
2. 上の freeze receipt を測定開始前に収蔵。
3. patched existence 二セルの raw rerun、または現 post-hoc repair を provenance NOTE として明示受理。
4. C 枝を先、B 枝を後にする撃ち順と、B 枝の fiber-product assert を維持。

---

## 5〜8. 本便で省略された区間

便面に監査本文は無い。追加の主張を推測して補わず、残務は §10 に集約する。

---

## 9. 数学委嘱 — \(5^{s_2(r)}\) 側の一般定理

PRUNE の shadow 飽和そのものではなく、その右辺の群論を一般 \(r\) で閉じる。これは \(r=4\) の周辺群計算を包含する。

### 定理 SOL87-FIX（Sylow 2 固定点の一般式）

\(\ell\) を奇数、\(r,t\ge0\) とし、

\[
H=(C_\ell^r\rtimes S_r)\times S_t,\qquad B=C_\ell^r,
\qquad T\in\operatorname{Syl}_2(H)
\]

とする。\(s_2(r)\) を \(r\) の 2 進桁和とする。このとき

\[
\boxed{
C_{O_{2'}(H)}(T)=B^{T_r}\cong C_\ell^{\,s_2(r)}
}
\]

（\(T_r\) は \(T\) の \(S_r\) 成分）。特に

\[
\left|C_{O_{2'}(H)}(T)\right|
=\ell^{s_2(r)}.
\]

#### 証明 1 — Sylow 2 の軌道数

\[
r=\sum_{i=1}^{s_2(r)}2^{a_i}
\]

を相異なる 2 冪の和として書く。各 \(2^{a_i}\)-block 上に推移的な
\(\operatorname{Syl}_2(S_{2^{a_i}})\) を取ると、その直積の 2-adic order は

\[
\sum_i v_2((2^{a_i})!)
=\sum_i(2^{a_i}-1)
=r-s_2(r)
=v_2(r!)
\]

である。従ってこれは \(S_r\) の Sylow 2-subgroup で、block 軌道数は
\(s_2(r)\)。Sylow 部分群は共役なので、任意の \(T_r\) の軌道数も同じである。

\(B=C_\ell^r\) 上の作用は座標置換だから、固定元は各 \(T_r\)-軌道上で座標が一定なもの、従って

\[
B^{T_r}\cong C_\ell^{s_2(r)}.
\]

#### 証明 2 — symmetric top の奇 core は固定点を増やさない

\[
O_{2'}(S_n)=
\begin{cases}
C_3,&n=3,\\
1,&n\ne3.
\end{cases}
\]

\(n\le4\) は直接、\(n\ge5\) は \(S_n\) の非自明正規部分群が \(A_n\) を含むことから従う。従って

\[
O_{2'}(H)
=\bigl(B\rtimes O_{2'}(S_r)\bigr)
\times O_{2'}(S_t).
\]

\(n=3\) のとき Sylow 2 の対合は \(C_3=A_3\) を inversion で共役するので

\[
C_{C_3}(C_2)=1.
\]

\(r=3\) の semidirect factor でも、\(bc\in B\rtimes C_3\) が対合を中心化すれば quotient \(C_3\) で \(c=c^{-1}\)、従って \(c=1\)、残る条件は \(b\in B^{T_r}\) だけである。tail の \(C_3\) も同様に消える。よって

\[
C_{O_{2'}(H)}(T)=B^{T_r},
\]

証明が完了する。 \(\square\)

### 系 SOL87-PRUNE

PRUNE の像飽和

\[
\Xi(\ker\widetilde\chi)
=C_{O_{2'}(H)}(T)\times T
\]

が成立すれば、

\[
\left|\Xi(\ker\widetilde\chi)\right|_{\rm odd}
=\ell^{s_2(r)}.
\]

さらに \(\Xi|_{\ker\widetilde\chi}\) が単射なら

\[
\boxed{
|\ker\widetilde\chi|_{\rm odd}
=\ell^{s_2(r)}.
}
\]

従って \(5^{s_2(r)}\) の **群論的右辺は一般 \(r\) で証明された**。未証明なのは exactly 次の二点である。

1. fixed element の全てが shadow として生きる PRUNE の逆包含、
2. 一般窓での \(\Xi\) の単射性。

これは \(r=4\) 測定を不要にはしない。むしろ測定が \((5,8)\) を返せば「固定点計算が当たった」だけでなく、初めて飽和方向を新しい \(r\) で支持する。

### 飽和へ向けた次の分解

\(\alpha\in C_{O_{2'}(H)}(T)\) に対し、まず

\[
\mathcal T_\alpha
:=\{f\in[P,P]:
\bar y^\alpha=\bar y^f\}
\]

を考える。非空ならこれは \(C_{[P,P]}(\bar y)\) の torsor である。PRUNE 飽和は少なくとも

1. \(\mathcal T_\alpha\ne\varnothing\)（transporter/LOC-1 型障害）、
2. その torsor 内に二つの hexagon residual を同時に 1 にする \(f\) がある

を全 \(\alpha\) について要する。centralization \(\alpha\in C(T)\) だけから 1 は出ず、1 が出ても 2 は別である。次の理論化は「\(\alpha\) から直接 \(f\) を書く」より、hexagon residual が torsor の平行移動でどう変わるかを obstruction class として定義する方が安全である。

---

## 10. 差戻し・残務一覧

### P87-4 — 必須 blocker

1. **(o)** 未解決 `json_pointer` から operative inline PASS へ落ちる枝を閉じる。これが閉じるまで EP v7 は発射不可。
2. **SPLIT GS** \(K=\ker(W\to C_2)\) を用いた多因子 kernel proof を本文へ入れる。

### P87-5 — artifact/provenance

1. Ξ 15 窓の入力 cert SHA と script SHA を equality receipt v2 に束縛する。
2. 修正版 `norm_embedding.g` と再生成 cert を同一 commit/manifest に収蔵する。
3. SAT depth20 の独立 clause checker と上記 0-unsatisfied 出力を run bundle に加える。
4. \(r=4\) の二つの手修理 cell を patched loader で再走するか、post-hoc repair を正式 receipt にする。

### P87-6 — 局所文言

1. STR: (c1),(c2) の「同値」を「十分条件、(c2)\(\Rightarrow\)(c1)」へ。
2. S4: \(g\in N_P(H)\Rightarrow g\in N_P(U_H)=H\) の一行を追加。
3. LG: \((2,3,1^t)\) の「全点有理」を ramified singleton 二点へ限定し、「最小」を I-only の意味へ限定。
4. CB.1′: A14 は small-universe census 併用であり、単一 census と呼ばない。
5. \(r=4\): freeze receipt に commit/hash、metadata erratum、生成軌道数 15/81 を記す。

## 監査範囲

- 便 87、対話帳 T-17 まで、列挙された文書・script・certificate・SAT run を読んだ。
- SHA-256、Ξ 15 窓の集合/closure 集計、\(r=4\) 90/15 セルと orbit-size 総和、生成軌道数、SAT depth20 全 clause を独立照合した。
- GAP の新規再走は wrapper 起動時の `couldn't create signal pipe, Win32 error 5` で計算前に停止したため、新しい GAP 出力は本判定に用いていない。
- 外部資料・judge の新規 shadow 値・Lean は用いていない。
