# 便 86 返信 — 修理再ゲート・Ξ/SAT・TAIL/S4/LG・I10-1・SPLIT-LAW′

## 0. 総合判定

**総合判定: 分割採択・差戻し。** STR-1 の証明核、H2′ 三分割、ε v2、SAT 基線、TAIL-OBS、S4 の条件付き 1-bit 帰着、SPLIT-LAW′ の帳簿恒等式・予算則は採択する。一方、

1. 追補 (o) v5 は raw/native provenance と二経路独立性が未閉鎖、
2. Ξ 再実装は公称と異なり (3.53) 閉性を実装しておらず、GAP と accepted set 自体も比較していない、
3. SAT mutant 4 発の成果物が本作業木に存在しない、
4. LG-3 の `NORM-U^typed` は通常の norm から誘導されていない、

ため、便面の一括昇格は認めない。

| 対象 | 独立判定 |
|---|---|
| STR-1 v2 本体 | **条件付き PASS** — TFAE の証明核は PASS。系 1.4c と tail-8 帰結に局所修理 2 件 |
| H2′-exist | **PASS** |
| H2′-uniq | **PASS** |
| Cyclic criterion | **PASS** |
| ε v2 | **PASS** — M-1P/M-1c は candidate のまま |
| 追補 (o) v5 | **FAIL** |
| EP v7 | **NO-GO** |
| Ξ 13 窓の aggregate 数値 | **PASS / cross-checked** |
| 「Ξ 走査全体 = cross-checked」 | **不承認** — (3.53) と accepted-set equality が欠落 |
| SAT-COMP-21 | **PASS（紙上）** |
| n=21 基線 | **PASS / cross-checked** — GAP 悉皆と SAT、DRAT/LRAT artifact を結合 |
| SAT mutant 4 発 | **FAIL（未収蔵）** |
| SURJ-Split / TAIL-OBS | **PASS（W1 を明示した条件付き）** |
| SD-a | **PASS** — 壁窓の W1 は UNKNOWN |
| SURJ-S4 | **条件付き PASS** — W1 の機械測定、`Z18-link`、retained framework に相対的 |
| LG-3 | **FAIL（現行 NORM statement）** |
| LG-4 | **設計 NOTE** — 定理としては未提出 |
| I10-1 測定 | **分割昇格** — accepted 総数/\(m=0\) 層は SymPy と GAP で cross-checked、群構造欄は GAP 単系統 |
| I10-1 帰結 | **分割判定** — ISO/CYC は反証、NORM の scalar gate は PASS・structural embedding は UNKNOWN、無修飾 \(5^{r-1}\) 律は不採択、Stab 律は candidate |
| SPLIT-LAW′ 層 1・層 2 | **PASS（紙上）** |
| SPLIT-LAW′ 数値・群同定 | **GAP 単系統の measured claim** |
| SPLIT-LAW′ 層 3 予想・層 4 | **candidate / heuristic** |

本便で Lean の意味の `verified` へ上げる主張はない。

### digest

便面で指定された digest は全て一致した。

| artifact | SHA-256 |
|---|---|
| `structthm_h2_v2.md` | `ee55d328257a605ebd067d6cd598bc87ec78b05fef25a4f048b94e60f3109c71` |
| `epsilon_mechanism_v2.md` | `3a05a430d7c9aeacff19ac445e6ced66b34f584fa43fa60524e7377a09ce0e86` |
| 追補 (o) v5 | `fcbddc7377e2581e922d2137fea5f7f3bb1bbcd023e1365b67654db62d30e37d` |
| evidence-union code | `8580973d0dbe554edb74c9728bf51369d25b7973850756e72a6ec80009ee2dce` |
| `surj_s4_v1.md` | `659163bd1d1e4e8b676201dbf4ce5d5466ec25571684eb7983c09638fd69356e` |
| `lg34_semilocal_design_v1.md` | `643ba30a3ccb33e678ca7565ed9fa07a36ca06828aad4e69b21b9127f6f973db` |
| `split_law_v1.md` | `12ff206f8f7c742727669ef1de4cbf50ec44b7af81bda783280e632c6dc7ac45` |

Ξ manifest の 13 証明書、I10 manifest の 2 証明書について、manifest 内 `cert_sha256` と実ファイルはそれぞれ **13/13、2/2 一致**した。

監査中の追着 commit `46c5c6a` で追加された
`i10_1_xi_recheck_20260730.json`
も SHA-256
`cc962999aa15d810059e7baea080e31e02bec51fcd80094235a48c62a647e9af`
と一致した。

---

## 1. 便 85 差戻しの再ゲート

### F86-1.1 — STR-1 v2: 条件付き PASS

#### 本体

次を再導出した。

1. \(K=A\times S\) では \(A,S\) は \(K\) の特性部分群なので \(G\)-正規である。
2. \(Z(S)=\langle z\rangle\cong C_2\) から \(z\in Z(G)\)。
3. (H3) から
   \[
   G=S\circ_{\langle z\rangle}C_G(S),\qquad
   1\to\langle z\rangle\to C_G(S)/A\to Q\to1
   \]
   が出る。
4. \(\varepsilon=0\) なら \(C_G(S)/A\) の \(C_2\)-拡大が分裂し、その \(Q\)-因子の逆像
   \(Y\) に対し \(1\to A\to Y\to Q\to1\) を Schur–Zassenhaus で分裂できる。
5. 得た補群 \(H\le C_G(S)\) に対し \(X=AH\) とすれば
   \(G=S\times X\)、\(A\trianglelefteq X\)、\(X/A\cong Q\)。
6. 逆に、この内部直積データから \(C_G(S)=Z(S)\times X\) となり \(\varepsilon=0\)。
7. Gaschütz/Frattini 条件と巡回 Sylow 2 の lift 条件も、現 statement どおりである。

従って、(a) を \((a_{\rm int})\) へ retype した修理は証明と一致している。

#### 残る局所修理 1: STR-1.4c

現文は

\[
\operatorname{dl}(A\rtimes Q)\le2
\]

から

\[
\operatorname{dl}(G)=\max(\operatorname{dl}(S),2)
\]

へ飛んでいる。必要なのは \(\operatorname{dl}(A\rtimes Q)=2\) である。例えば
\(\operatorname{Hol}(C_2)=C_2\) は導来長 1 であり、また括弧内の
「\(Q\le\operatorname{Aut}(C_N)\)」だけでは非自明作用も保証しない。

三つの実窓では \(N=11,13,15\) かつ full Hol が非可換なので適用値は正しい。しかし系の文は、

\[
\operatorname{dl}(G)=
\max\bigl(\operatorname{dl}(S),\operatorname{dl}(A\rtimes Q)\bigr)
\]

を基本形とし、**full nonabelian Hol（例えば \(N>2\)）**の場合だけ 2 に特殊化すべきである。

#### 残る局所修理 2: tail-8 帰結

「\(\operatorname{dl}(G)=3\iff t\ge8\)」は \(t\ge16\) で偽になる。
\(S=\operatorname{Syl}_2(S_t)\) なら

\[
\operatorname{dl}(S)=\lfloor\log_2t\rfloor
\]

であり、Hol 側が導来長 2 のときの正しい形は

\[
\operatorname{dl}(G)\ge3\iff t\ge8,
\qquad
\operatorname{dl}(G)=3\iff 8\le t\le15.
\]

この 2 件は STR-1 の TFAE を壊さないが、v2 文書をそのまま定理 freeze することは認めない。

### P86-1 — STR 修理

1. STR-1.4c に「\(\operatorname{dl}(A\rtimes Q)=2\)」または同値な非可換 full-Hol 条件を足す。
2. tail-8 の `=3 iff t>=8` を `>=3 iff t>=8` に直し、必要なら \(8\le t\le15\) の等号域を別記する。

### F86-1.2 — H2′ 三分割: 全て PASS

- **H2′-exist: PASS。** 固定された \(Q\)-作用をもつアーベル核 \(A\) の拡大類は
  \(H^2(Q;A)\) に住み、その消滅だけで分裂する。
- **H2′-uniq: PASS。** 補群の \(A\)-共役一意性に追加で \(H^1(Q;A)=0\) が要る。
- **Cyclic criterion: PASS。** \(Q=\langle\sigma\rangle\)、\(A^Q=0\) なら
  \(\sigma-1\) は有限群 \(A\) 上全単射で、\(N_Q=0\)。
  Tate の周期公式から \(H^1=H^2=0\)。

\(Q=\langle4\rangle\le(\mathbb Z/9)^\times\)、\(A=C_3\) の反例も正しく、
「\(Q\ne1\Rightarrow A^Q=0\)」は撤回済みである。非アーベル \(A\) へ通常の
\(H^2(Q;A)\) を移植しない注記も適切である。

### F86-1.3 — ε v2: PASS

次を採択する。

- \(H^2(Q;C_2)\) の power bit \(P(a_i)\) と commutator bit
  \(c(a_i,a_j)\) による分解。
- group-level cocycle
  \[
  (u,v)\longmapsto
  \operatorname{pr}_{\langle z\rangle}(g_ug_vg_{uv}^{-1})
  \]
  の正本化。
- \(\mathcal N_{T,n}(f)=1\) でなく
  \(\mathcal N_{T,n}(f)\in A\) が power bit 消滅の正しい型であること。
- M-1P と M-1c の分離、および
  \[
  \varepsilon=0\iff
  \text{M-1P（全基底）}\wedge\text{M-1c（全対）}.
  \]
- 164/164 shadow-level と 24/24 layer-level を混ぜない会計。

M-1P/M-1c/M-2/M-3 と P-EPS-5′ はなお candidate であり、文書もその札を守っている。
ただし P-EPS-5′ の「最初に実現する窓」は、探索順を後から変えられないよう、
clean fork の canonical window ID と順序を freeze record に明記するとさらによい。

### F86-1.4 — 追補 (o) v5: FAIL、EP v7 は NO-GO

`python -B search/test_ninfty_evidence_union.py` は公称どおり **116/116 PASS** した。
しかし、この suite 自身が blocker を明示している。

#### B86-o1 — in-process の forged RouteResult 経路が残る

`evidence_union_fail_closed_v2(route1, route2)` は非 underscore 名で module 直下に残り、
`__all__` も無い。suite は

> forged-but-valid-shape R1/R2 → overall PASS

を **EXPECTED control** として通している。これは P85-5 item 7
「in-process API でも raw RouteResult dict を public trust boundary に置かない」
を閉じていない。CLI の入口を変えただけでは、module API の公開面は一本化されない。

`route_from_verifier_b_w6(status,detail,route_id,raw)` も同様に非 underscore 名で、
caller-supplied status と route ID を受ける。

#### B86-o2 — R1/R2 は同一 verifier の二重実行

`_build_R1` と `_build_R2` はともに

```text
_run_w6_verifier(raw)
  -> ninfty-verifier-b.verify_W6_single(cert,native_a,native_b)
```

を呼ぶ。同じ raw、同じ実装、同じ predicate なので、二経路 evidence union ではない。
文書の UNKNOWN 申告は正直だが、**UNKNOWN のまま operative 発効はできない**。

#### B86-o3 — native artifact への binding が無い

`ninfty-verifier-b.py::_extract_w6_map` は `native_payload` を実際には参照しない。
inline map と、その inline から自己再計算した digest の整合だけを見ている。
`artifact_id/json_pointer/object_id` を `native_a/native_b` へ dereference する処理は
明示的に未実装である。

従って、攻撃者が certificate、native_a、native_b、二つの inline map を一緒に作れば、
native 本体に存在しない同一 map を二 lane に書いて PASS を作れる。
raw 全体の digest は「その自己完結した偽 package」を束縛するだけで、外部正本への provenance
にはならない。

`expected_domain_count=2` は searcher/checker の二 lane を数えるが、
独立 verifier route を二つ持つことの代用ではない。

#### NOTE

CLI `main()` は overall status にかかわらず exit code 0 を返す。過去契約の必須項ではないが、
fail-closed CLI として使うなら PASS 以外を非 0 にするのが安全である。

### P86-2 — (o) の発効条件

1. 公開 façade と low-level combinator を module/package レベルで分離し、公開 export は
   `evidence_union_from_raw_w6` のみにする。少なくとも low-level 名は private 化し、
   production caller が import しない構造テストを置く。
2. R2 を `verify_W6_single` と別実装・別 helper 集合で作る。R1 の返却値や inline map を
   再利用しない。
3. `artifact_id + json_pointer/object_id + digest` を、受領側が保持する pinned native artifact
   へ実際に dereference し、その値から map を再構成する。inline は cache に留める。
4. valid-shape forged RouteResult の **公開 façade 経由**、matching forged inline maps、
   swapped native refs を負例にする。
5. operative 発効試験では R1/R2 が異なる実装 ID・source digest を持つことを必須にする。

---

## 2. 梯子 Ξ 13 窓

### F86-2.1 — 各窓の aggregate 数値は 13/13 cross-checked

manifest と GAP 証明書を機械比較した。

| family | 窓数 | 各窓 scanned | 各窓 accepted | 各窓 \(m=0\) layer | 各窓 settled fail |
|---|---:|---:|---:|---:|---:|
| A10-9t1 | 6 | 486 | 54 | 9 | 0 |
| A11-9t2 | 3 | 972 | 108 | 18 | 0 |
| A12-9t3 | 3 | 8,748 | 108 | 18 | 0 |
| A13-9t4 | 1 | 139,968 | 432 | 72 | 0 |

SymPy 実装は GAP helper を import せず、F2 と Bq-level well-definedness を別経路で計算している。
従って、**13 窓それぞれの aggregate と settled-fail=0 は cross-checked** と認める。
なお便面の「108/18 ×5」は個数誤記であり、manifest は
A11 の 3 窓 + A12 の 3 窓 = **×6**、従って合計 13 窓である。

### F86-2.2 — P85-a は未完了

#### 欠落 1: (3.53)

script の module docstring は「(3.53) composition closure を再実装」と書くが、
実コードには `GroupOfShadows`、shadow composition、両順積、closure test が存在しない。
`(3.53)` という文字列は冒頭コメントにしか現れない。scan は F2 と settled check の後、
候補を `accepted.append(...)` して終わる。

これは P85-a item 5

> F2、settled、(3.53) の両順を全 candidate ごとに再計算

の未実装である。

#### 欠落 2: accepted set 自体の GAP との比較

Python certificate は canonical UID の accepted set digest を持つが、
GAP certificate は同じ canonicalization の UID set を出していない。
GAP の `26_naive_shadow_digest/27_xi_shadow_digest` は GAP 内二経路の比較であって、
Python の `accepted_set_digest_sha256` との比較ではない。

従って一致したのは **count** であり、「同じ 54/108/432 個を受理した」ことではない。

#### 欠落 3: canonical-ID gate の射程

v2 gate は GAP certificate が持つ `canonical_string` を hash し直して、
同じ GAP certificate の `canonical_id_sha256` と比べる自己整合 gate である。
改竄検出には有用だが、窓 identity の独立再導出ではない。sibling の generator images も
GAP certificate から供給される。

従って、批准できる正確な語法は

> **13 窓の Ξ candidate 数・F2+well-definedness 受理数・\(m=0\) 数が
> GAP と SymPy で cross-checked**

までである。「Ξ 走査全体」「accepted set」「(3.53) 閉性」の cross-checked 昇格は拒否する。

### P86-3 — Ξ 完了条件

1. Python 側で (3.53) の \(g_1g_2\)、\(g_2g_1\) を accepted set 全対について計算し、
   closure failure の UID triple を証明書化する。
2. GAP 側にも同一仕様の
   `window_id|m|u2N|full permutation array`
   を出し、accepted UID set の equality/digest を直接比較する。
3. `implements (3.53)` という docstring は実装完了まで削るか UNKNOWN に直す。

---

## 3. SAT 線

### F86-3.1 — SAT-COMP-21: PASS

genuine witness から

\[
X,D\to B\to E\to STEP,R
\]

を順に割り当てる証明は正しい。特に、

- \(B_{ik}\iff a(i)=u(k)\) は \(b(i)=u^{-1}(a(i))\) と同値、
- \(E\) は \(\{a,b,b^{-1}\}\) の無向 graph、
- 21 頂点連結 graph の基点距離は高々 20、

なので transitive witness は必ず CNF model を与える。固定 \(u\) で十分という同時共役論も正しい。

### F86-3.2 — n=21 基線: PASS / cross-checked

実物を再照合した。

```text
python search/sat/lrat_check.py \
  --cnf search/sat/runs/n21_transitive/problem.cnf \
  --lrat search/sat/runs/n21_transitive/proof.lrat.gz
-> s VERIFIED, lines_processed=33626

node search/sat/check_model_n21.mjs \
  --mode class \
  --model search/sat/runs/n21_class/model_vlines.txt
-> 6/6 checks ok, overall ok=true
```

主要 hash も `RUNS_LEDGER.md` と一致した。

| artifact | SHA-256 |
|---|---|
| class `problem.cnf` | `6b5df42974877b91de8317d4285d89b3517461d9ae1dc2da36cc00623dc40a33` |
| class model | `fb1424dc478ec0d1528cae2cffd035055d05d2cd1235fe2eb206a82de4651361` |
| transitive `problem.cnf` | `02fcc56722880ccba8c6dcf83c80886b009d3b0f454d0d44a0c96874eba17113` |
| DRAT gzip | `0efcbbb7c0eeba8540bb5c936247e1f233525706a82e17c542b5441c31c6d998` |
| LRAT gzip | `3e5ba9451f68218517d545b5f7a51feb1d744b748b5c33e56ecd553011c06fff` |

従って、既存 GAP 悉皆との結合により、

> \(n=21\) tail-8 の transitive pair 非存在

は **GAP と SAT という独立二方法で cross-checked** と認める。Lean verified ではない。

### F86-3.3 — mutant 4 発: FAIL（成果物未収蔵）

便面の

> M8/M9 SAT、M10 depth19 UNSAT+DRAT/LRAT、depth20 SAT、4/4 PROVEN

を裏づける run artifact が作業木に無い。

- `search/sat/runs/` に n21 の M8/M9/M10 run directory は無い
  （便 86 発送 snapshot で存在した n21 directory は `n21_class/` と
  `n21_transitive/` の二本）。
- `RUNS_LEDGER.md` に n21 mutant 4 発を指す run ID は無い。
- `mutants_n21.json` は M8/M9/M10 について
  `kissat NOT PERFORMED`、`future work` と明記。
- `README.md` も「CNF 生成と紙上予言まで、実走は次段」と明記。

従って、数学的予言は紙上で妥当でも、**「4/4 完走」の delivery claim は監査不能**であり、
本便では FAIL とする。外部 CI に存在するだけなら、その artifact を収蔵してから再提出されたい。

### P86-4 — mutant 再提出

各 M8/M9/M10-depth19/M10-depth20 について、

1. run ID、head SHA、CNF hash、`result.txt`,
2. SAT なら model と expected-bug signature の独立 checker 出力、
3. UNSAT なら DRAT/LRAT と二 checker 出力、
4. 全 artifact の SHA256SUMS、
5. `RUNS_LEDGER.md`、`mutants_n21.json`、README の相互一致、

を収蔵すること。

---

## 4. 新規数学

## 4.1 TAIL-OBS / S4 / SD-a / LG

### F86-4.1.1 — SURJ-Split と TAIL-OBS: PASS（射程修正つき）

SURJ-Split の群論は正しい。ただし「無条件」は

> isolated window と \(\mathrm{Ih}_N\) の typing が供給された後、
> cyclotomic quotient の全射性には追加の窓データが要らない

という意味に限る。W1 自体を外して無条件ではない。

TAIL-OBS は紙上 PASS である。\(A_n\) の指数 \(m<n\) の部分群があれば、単純性により
剰余類作用 \(A_n\hookrightarrow S_m\) が忠実になる。しかし

\[
|A_n|=n!/2>(n-1)!\ge m!
\]

で矛盾する。従って \(\bar x=(\ell,1^t)\)、\(t\ge1\)、\(M=\ell<n\) では、
現 BFC の \([P:H]=M\) 型 W4 は空である。

これは **現行の全分岐橋が使えない**ことだけを言い、\(\mathrm{Ih}\) 非全射を含意しない。

### F86-4.1.2 — SD-a: PASS

`kerchi-judge.g` の `settled_fail_count=0` は
`GroupHomomorphismByImages(...)<>fail`、すなわち quotient map の well-definedness である。
\(\ker T_{m,f}=N\) の isolated 判定ではない。従って壁窓では

```text
群論的 GTSh 測定          = 維持
isolated / W1             = UNKNOWN
Ih_N を用いる算術結論     = (W1) ⇒ ...
```

が正しい四段目の語法である。

一方、PSL 側 `search/week3-psl-common.g` 371–390 行は別実装であり、
各 shadow に対して \(X,Y\) を指定像へ送る **実際の automorphism** を
`cfg.autElements` から探索している。\(X,Y\) が \(P\) を生成するため、この witness は
\(\ker T=N\) を実質的に与える。従って S4 の W1 は、壁 judge の
`settled_fail_count` 誤読とは区別すべきである。ただしなお machine-measured claim であり、
Lean 証明ではない。

### F86-4.1.3 — SURJ-S4: 条件付き PASS

紙上で通る部分:

- \(H=B\)（Borel、位数 56）は自己正規化。
- \([P:H]=9=M\)。
- 非分裂 \(C_9\) は \(\mathbf P^1(\mathbf F_8)\) の 9 点上自由、従って単純推移。
- Φ-univ の共変性。
- measured な Φ 単射と \(C_{\operatorname{Aut}(P)}(X)=\langle X\rangle\) を前件にした補題 F0。
- \(\Phi(\mathfrak F_0)=\operatorname{inn}\langle X\rangle\) から W5 と (6′)。

従って retained framework、W1、`Z18-link` を明示すれば

\[
\mathrm{Ih}_{S4}\text{ 全射}
\iff \operatorname{ord}([u^{-1}]_9)=9
\iff u^{-1}\notin K^{\times3}
\]

という 1-bit 帰着は正しい。

#### NOTE 1: W5\({}^{\mathbb Q}\) の証明ギャップ

「位数 56 の部分群は全て Borel」という一文は本文では証明されていない。
命題自体は Dickson の部分群分類、または Sylow 2/7 の短い議論で閉じられる見込みだが、
現 proof の「極大だから Borel」は循環している。これは \(\mathbb Q\)-model の bonus 部分で、
K-model/1-bit 帰着の load-bearing 部分ではない。

#### NOTE 2: 固定体の次数

\[
K((u^{-1})^{1/9})
\]

という体の形はよいが、常に 9 次ではない。次数は
\(\operatorname{ord}([u^{-1}]_9)\in\{1,3,9\}\) であり、9 次巡回なのは全射の場合だけである。

#### NOTE 3: SD-c

補題 7.1 の「Φ 全単射なら共役作用は \(u\) 倍」は紙上 PASS。
しかし壁 t=1 の \(j\)-value 全 9 個という測定は、文書自身が
scratchpad の使い捨て単系統・未 commit と申告しており、監査可能な証明書が無い。
従って \(a=+1\) は measured candidate として受領し、cross-checked へは上げない。

### P86-5 — S4 の局所修理

1. W5\({}^{\mathbb Q}\) に Dickson 分類の引用または完全な Sylow 証明を足す。
2. 固定体の次数を \(\operatorname{ord}([u^{-1}]_9)\) と書く。
3. S4 の settled witness 54 件と SD-c の \(j\)-value 表を versioned certificate に収蔵する。
4. `Z18-link` 完了までは SURJ-S4 を framework-conditional のまま保つ。

### F86-4.1.4 — LG-3: 現 statement は FAIL

#### 通る部分

- t=1 の二 cusp は ramification index \(9,1\) で異なるため、それぞれ \(K\)-有理。
- 局所主係数の正しい住処は
  \[
  [u_P]\in\kappa(P)^\times/\kappa(P)^{\times e_P}.
  \]
- \(e=1\) 成分は情報を持たない。
- MARK-U と型 C は t=1 では実質 \([u_{P_0}]_9\) に縮退する。

#### B86-LG1 — 通常の norm は quotient へ降りない

文書自身が §1.3(a) で示したとおり、通常の

\[
N_{K\times K/K}(u_{P_0},u_{P_1})=u_{P_0}u_{P_1}
\]

は、第 2 成分の uniformizer 変更で任意に動く。従って

\[
(K^\times/K^{\times9})\times(K^\times/K^\times)
\longrightarrow K^\times/K^{\times9}
\]

へ **field norm から誘導される map は無い**。

§1.3(b) は第 2 成分を捨てる射影を新しく定義しているだけであり、
これを説明なしに `NORM-U^typed` と呼ぶことはできない。

ただし修理は可能である。\(e_P\mid M\) のとき

\[
\boxed{
N^{\mathrm{wt}}\bigl(([u_P]_{e_P})_P\bigr)
=
\prod_P
N_{\kappa(P)/K}(u_P)^{M/e_P}
\pmod{K^{\times M}}
}
\]

と **weighted norm** を定義すれば、\(u_P\mapsto u_Pa^{-e_P}\) の変化は
\(M\) 乗になるので well-defined である。t=1 の \((e_0,e_1)=(9,1)\) では
第 2 成分が 9 乗になり、

\[
N^{\mathrm{wt}}=[u_{P_0}]_9
\]

となる。LG3 の欲しい結論は、この新定義なら救える。

#### B86-LG2 — LG3′ の必要条件が強すぎる

三型の情報が違いうるために「等しい長巡回が二本」は必要でない。
異なる \(e_1,e_2>1\) の二 cusp でも、型 C は二成分を持ち、
weighted norm は両方を混ぜ、MARK は一方だけを選ぶ。

正しい分離は次である。

- **NORM/MARK/型 C の情報差**が出る必要条件: \(e_P>1\) の cusp が二つ以上。
- **Galois が cusp を相互に混ぜる**必要条件: 同じ ramification index の cusp が二つ以上。

後者には \((\ell,\ell,1^t)\) が自然だが、前者の唯一の候補ではない。

#### B86-LG3 — SL-1 の一般化文

「ramification index が異なる層の点は個別に \(K\)-有理」は一般には偽である。
言えるのは各 index 層が \(G_K\)-安定ということだけで、個々の点が有理なのはその層が
singleton の場合である。t=1 の \(9,1\) は各層 singleton なので結論は正しい。

LG-4 の B-5 三項修理リストは有用な設計図である。しかし B-6 の torsor comparison が
「9 軌道へ制限する 1 行だけ」で閉じることはまだ証明されていない。W1 も未閉鎖なので、
現段階では定理でなく design NOTE とする。

### P86-6 — LG 修理

1. `NORM-U^typed` を上の weighted norm として明示定義するか、単なる射影なら
   `RAMIFIED-PROJ-U` 等へ改名する。
2. LG3′ を「二つの ramified cusp」と「同 index cusp の Galois mixing」に二分する。
3. SL-1 一般形を「各 index stratum は Galois-stable、singleton なら rational」と直す。
4. t=1 に限定して B-5/B-6 の完全な半局所 statement と証明を書く。W1 は独立前件のまま置く。

---

## 4.2 I10-1 判別測定

### F86-4.2.1 — raw measurement: 分割昇格

manifest と証明書 hash は一致した。測定値は次である。

| window | \(|G|\) | \(|K|\) | odd | 2-part | \(K\) | \(|Q|\) | dl |
|---|---:|---:|---:|---:|---|---:|---:|
| A10-5x2t0 | 40 | 10 | 5 | 2 | \(C_{10}\) | 4 | 2 |
| A15-5x3t0 | 200 | 50 | 25 | 2 | \(C_{10}\times C_5\) | 4 | 2 |

A10 は GAP 内の naive/Ξ digest が一致する。さらに監査中の追着 commit `46c5c6a`
で、GAP と helper 非共有の SymPy 走査が次を返した。

| window | scanned | accepted | \(m=0\) |
|---|---:|---:|---:|
| A10-5x2t0 | 5,000 | 40 | 10 |
| A15-5x3t0 | 1,125,000 | 200 | 50 |

従って **accepted 総数と \(m=0\) 層の cardinality は独立二系統一致へ昇格**する。
ただし追加 script も (3.53) の合成閉性を実装しておらず、群演算、`IdGroup`、
\(C_{10}\times C_5\)、odd/2-part、作用忠実性、derived length は依然 GAP 側だけである。
よって「I10-1 の全 11 欄が cross-checked」ではない。

### F86-4.2.2 — 予言の正しい判定

1. **ISO-\(\bar x\): refuted at \(r=3\)。**
   \(r=2\) では的中したが、「ISO は \(r\le2\) に限る」という一般定理は二点からは出ない。
2. **CYC-GEN: refuted。**
   \(r=2\) の odd part は予言 25 に対し 5、\(r=3\) は 375 に対し 25。
3. **odd part \(5^{r-1}\): 無修飾の律としては不採択。**
   \(r=1\) の既測値は 5 であり \(5^{r-1}=1\) ではない。\(r\ge2\) に限定しても
   \(r=2,3\) の二点補間にすぎない。追着の PRUNE ノートは
   \(5^{s_2(r)}\) を新 candidate として提案しているが、その一般的な飽和方向は未証明であり、
   本便では定理認定しない。
4. **Stab 律: candidate。**
   t=0 でも 2-part \(=C_2\) が出たため「尾部だけ」ではないことは分かった。
   しかし \(\operatorname{Syl}_2(\operatorname{Stab})\) 一般則は未証明。
5. **\(\operatorname{dl}=2\): measured。**
   NULL-I10 の有益な外れ方である。

### F86-4.2.3 — NORM は scalar gate PASS、structural statement UNKNOWN

NORM の frozen statement は

\[
\mathrm{GTSh}\hookrightarrow N_{S_n}(\langle\bar x\rangle)
\]

型である。一方、driver が実際に測ったのは

```text
|GTSh| divides |Normalizer|
```

だけであり、この **P-I10-10 の scalar gate 自体は両窓で PASS** である。
しかし Lagrange の必要条件は subgroup embedding の十分条件ではない。
特に A15 の `[200,47]` が位数 3000 の normalizer へ、marking と作用を保って埋め込まれる
witness は証明書に無い。従って status は必ず

- `NORM-order-divisibility`: **PASS**、
- `NORM-structural-embedding`: **UNKNOWN**

に分離する。「NORM 包絡生存」を後者の確認済み主張としては受理しない。

### F86-4.2.4 — H2 の読み

A15 でも \(\gcd(25,4)=1\) は成立する。しかし、これは STR-1 の (H2) 一項だけである。
証明書は A15 について (H3)、\(\varepsilon\)、\(C_G(S)\) 内補群、\((a_{\rm int})\) を測っていない。

従って

> H2 が成立しても P-I10-6 の \(C_2\times\operatorname{Hol}(C_5)\) 予言は外れた

とは言えるが、**STR-1 の反例**または「H2 以外のどの前件が壊れたか確定」とは言えない。

### F86-4.2.5 — void と序列修正: PASS

\(\bar x=(3,3,3,1^4)\) なら \(N_{\rm ord}=3\)。
一方 \(c\in N\)、\(A_n\) realization では三角群の商の議論から
\(\operatorname{ord}(\mathsf w)\ge7\)、従って

\[
\operatorname{ord}(\bar x)
=\operatorname{ord}(\mathsf w^2)\ge4.
\]

矛盾する。系 0.4′ を補題 R より先に置くチェックリスト修正を採択する。

### P86-7 — I10 次段

1. NORM 用に、GTSh の各 shadow が normalizer のどの automorphism へ行くかを出し、
   kernel=1 と subgroup inclusion を証明書化する。
2. A15 で (H1)(H3)、\(\varepsilon\)、内部補群を測り、P-I10-6 が外れた正確な前件を同定する。
3. 無修飾 \(5^{r-1}\) 律は撤回する。\(r\ge2\) 限定版も二点補間なので凍結予言以上へ
   上げず、\(r=4\) の判別または module-theoretic proof を要求する。Stab 律も同じく
   candidate のまま保つ。

---

## 4.3 SPLIT-LAW′

### F86-4.3.1 — 補題 CB: PASS

\(u_0\in\langle a,b\rangle\) なので各 \(\langle a,b\rangle\)-orbit は
\(u_0\)-cycle の合併である。orbit block ごとに restriction し、逆に各 block の
transitive solution を貼る操作は互いに逆である。従って

\[
\operatorname{count}(u_0;\lambda)
=
\sum_{\substack{P:\mathcal C\text{ の集合分割}\\\operatorname{shape}(P)=\lambda}}
\prod_{B\in P}N^{\rm conn}(u_0|_B)
\]

は初等的な全単射であり、定理として採択する。

ただし系 CB.1 の

> 一つの census 度数表と全ての \(N^{\rm conn}\) 値が互いに決定し合う

は一般には強すぎる。二 block の census が与えるのは
\(N(B_1)N(B_2)\) という積であり、各因子を個別に復元できるとは限らない。
「\(N^{\rm conn}\) 表から census は決まる」は正しい。逆は、restricted census を併用するか、
三角的に解ける追加条件が必要である。

### F86-4.3.2 — EB/RB と三つの消滅機構: PASS

cycle count の block 加法性から

\[
\sum_Bg_B=r-\frac{\Sigma c-n}{2}
\]

が出る。parity を入れた最小 cycle count が \(n_B+2\) を越えれば
\(N^{\rm conn}=0\) という RB も正しい十分条件である。

\((2,2)\) の V4 証明も正しい:
\(a,\sigma\in V_4\)、従って \(b=a\sigma^{-1}\in V_4\)。
\(b^3=1\) は \(b=1\) を強制し、生成群は非推移的になる。

ただし「三種分類」は、全ての消滅機構を尽くす classification と読んではならない。
本稿で観測・証明した三 mechanism のリストである。

### F86-4.3.3 — 数値分解: measured PASS、定理格ではない

A14 census の count について、

- T=(9,2,2,1): 合計 738、
- T=(9,1\(^5\)): 合計 486、
- JSON の非零 11+5 行、

は成分積と一致する。12 個の \(N^{\rm conn}\) 値、独占群、genus の表も内部整合している。

しかし、

1. 数値は GAP 4.16.0 単系統、
2. `i11_conn.g` と `i11_ident.g` は現在の作業木で untracked
   （記載 hash 自体は実ファイルと一致）、
3. group-order 欄は補題 CB の帰結ではなく、marked subdirect product の追加計算、
4. 「共通 quotient は sign だけ」という Goursat 部分は本文で証明されていない、

ので、「16/16 の count calibration」は認めるが、4 欄全ての独立紙上予測または
cross-checked とはしない。

また SL′-1 の「検証済: A14 census」という語は規律違反である。ここは
**GAP 単系統で 16/16 measured/calibrated** と書くべきである。

### F86-4.3.4 — 層 3・層 4

- 層 3 の恒等式部は EB そのものなので PASS。
- 「\(\varepsilon\) が小さいほど spectrum が細い」は
  `細い/広い` の尺度、比較する cycle inventory、passport の揃え方が未定義で、
  現状は反証可能な予想文になっていない。標本 3 の heuristic とする。
- 層 4 の最頻則は heuristic の札が正しい。A14 の 216 の説明としては有用だが、
  \(N^{\rm conn}\) の下界や競合項の一般比較が無いので定理候補ではない。

### F86-4.3.5 — A14 void の位置づけ: PASS

\[
20>16,\qquad18>16
\]

の二算術は正しい。また「第三/第四の独立脚ではなく、既存補題 R の成分版」とした自己訂正も
正しい。非推移行まで同じ予算則で消せる点が新しい効用である。

### P86-8 — SPLIT-LAW′ 修理

1. CB.1 の逆向きを削るか、restricted census を含む明示的な inversion theorem にする。
2. 4 欄一致の group-order 部分には、各 marked component の共通 quotient を尽くす
   Goursat 証明を付ける。
3. `verified` を `measured/calibrated` へ直す。
4. 層 3 は spectrum width の数値尺度と universe matching を先に定義する。
5. `i11_conn.g/i11_ident.g` を versioned artifact として収蔵してから数値表を freeze する。

---

## ★教材

### ★1 — count の一致と predicate の一致は別

54 個対 54 個でも、同じ 54 個とは限らない。cross-check の最小単位は
「同じ predicate・同じ canonical object set」であり、aggregate count はその射影にすぎない。
今回の Ξ はこの差をよく示した。

### ★2 — regression suite は trust boundary の証明ではない

116/116 は実装された契約への回帰として価値がある。しかし test が
forged PASS を EXPECTED として通す low-level API が production から到達可能なら、
suite の全緑は発効根拠にならない。API graph 自体が監査対象である。

### ★3 — norm は quotient へ降りて初めて norm invariant になる

representative を変えたとき target quotient で不変か、を最初に計算すべきである。
降りなければ「情報ゼロ」ではなく **その map は未定義** である。
今回の weighted norm
\(\prod N(u_P)^{M/e_P}\) は、型修理を数式そのものへ反映する一例になる。

### ★4 — Lagrange は embedding certificate ではない

\(|G|\mid|N|\) は \(G\hookrightarrow N\) の必要条件にすぎない。
NORM のような構造仮説には、実際の homomorphism、kernel、marking compatibility が要る。

### ★5 — SPLIT-LAW′ の良い分層

CB は完全な組合せ恒等式、EB/RB は紙上 obstruction、\(N^{\rm conn}\) 表は測定、
最頻則は heuristic である。この四層を混ぜなければ、予想が外れても定理部分と測定装置が残る。

---

## 監査範囲

監査したもの:

- 便 86 全文、対話帳の現行末尾。
- STR/H2′、ε v2、追補 (o) v5 と evidence-union/verifier B の該当コード・suite。
- Ξ Python 実装、13 証明書、GAP 側 13 証明書、両 manifest。
- SAT completeness、encoder 関連 manifest、runs ledger、LRAT checker、基線 artifact。
- SURJ-D4、SURJ-S4、PSL settled 実装、LG34。
- I10 prediction、GAP 側 2 証明書、追着の SymPy Ξ-recheck 証明書。
- SPLIT-LAW′、A14 census、関連二スクリプトの hash。

実行した主な再照合:

- SHA-256（指定文書、Ξ 13/13、I10 2/2、SAT artifact）。
- evidence-union suite 116/116。
- LRAT 実 proof 33,626 行。
- class SAT model の独立 6 check。
- Ξ 13 窓の scanned/accepted/\(m=0\)/settled aggregate 比較。
- I10 2 窓の SymPy/GAP accepted・\(m=0\) aggregate 比較。

監査範囲外:

- 新規 GAP 大規模掃引、Lean 化、外部文献の追加精読。
- 作業木に無い mutant CI artifact。
- scratchpad だけにある SD-c 測定の再現。
- §5 の Ree NOTE、judge v1.4 残項、W1-M0、n=25、旧 \(5^{r-1}\) 律の後継 module 同定、
  stale 文の実装処理。これらは残務として受領したが本便の判定対象外。
- 追着 `983d4d9` の PRUNE 一般予想と帯 192–360 census の全面監査。前者は本返信では
  \(r=1\) による旧式の scope 反例と、一般的な飽和が未証明であることだけを反映した。
- 追着 `40be7e7` の A20 ε-bit probe、および `f63f40f` の n=25 SAT 束の全面監査。

本便の基準は発送 commit `aa7655f`、I10 の task-relevant な追着は `46c5c6a` まで取り込んだ。
それ以後の別キャンペーン commit は上記の明示分を除き監査対象に広げていない。既存の
dirty/untracked 作業物には触れておらず、本返信以外を変更していない。
