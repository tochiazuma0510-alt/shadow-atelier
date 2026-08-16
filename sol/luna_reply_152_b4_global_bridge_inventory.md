# Luna reply 152 — B4-B から global genuine / cofinal / Ihara へ

**日付:** 2026-08-16
**状態:** evidence inventory（定理の主張ではない）
**範囲:** 既存の B4-B 直接 IdRel lane、正典ノート、論文抽出、Ihara 文献、Lean/PDF
設備を読み取り専用で棚卸しした。重い GAP、ローカルの大量計算、PDF 生成は行っていない。

## 0. 結論を先に

現時点で B4-B の global terminal receipt はない。`search/d972_b4_universal_v2.g`
は 972 行を数えるが、U_M の有限性・サイズ・有限作用を意図的に実行せず
`UNKNOWN_U_FINITE_UNCHECKED` を出す（同ファイル L189, L196--213）。直接 IdRel
版は、元の six-generator/158-relator presentation 上で 486 unique norms と固定
972-row duplicate map を処理し、各 rule の

```text
product(original relator_i ^ conjugator) * reduced = original norm
```

を独立 Python checker で再生する設計である。しかし bounded pass の非自明な
reduced word は A ではなく UNKNOWN であり、全 486 unique（従って全 972）が
空語になった場合だけ `B4_B_DIRECT_LOGGED_TERMINAL` を出す
（`search/d972_b4_u_idrel_direct_logged_v1.g` L4--19, L422--520）。証明書が未取得
なので、現在の安全な札は `B4_STATUS=UNKNOWN_NO_TERMINAL_GLOBAL_CERTIFICATE`
である（`sol/luna_reply_152_b4_global_b.md` L3--9）。

仮にこの lane が terminal になっても、直ちに「global genuine shadow」や
「Ihara の非全射の反例」にはならない。最小限、次の三層を別々に閉じる必要がある。

1. **local semantic layer:** 972 行が本当に対象 M の全 relevant B4
   pentagon/roof 条件を表し、6/158 presentation が論文の original B4/PB4
   shadow quotient と同じであること。
2. **cofinal/genuine layer:** M の下の isolated refinements と reduction map
   を全て（または証明された cofinal chain で）扱い、compatibility を持つ有限段
   データを作ること。
3. **arithmetic layer:** 得られた genuine element が `Ih(G_Q)` に入らないことを
   **G_Q の全像**に対して示すこと。複素共役一個を除外するだけでは足りない。

したがって B4-B は、成功してもまず「この固定した有限 presentation/roof ledger
の exact identities」の証明であり、global 結論へは以下の conditional bridge が
必要になる。

## 1. B4 の固定入力と現在の証拠

| 層 | 既存 artifact / 根拠 | 既に固定されたこと | global bridge に不足すること |
|---|---|---|---|
| universal construction | `search/d972_b4_universal_v2.g` L1--4, L102--213 | frozen K(0,5)、coface relators、rho orbit、`shadow_count=972`（L189）を構成。 | L196 で `B4Finite:=false`。U_M の exact finite evaluation、M の全 shadow への意味付けは未完。 |
| canonical source | `search/certs/d972_b4_p2_magnus_input_v2_20260816.json` と `search/d972_b4_pquotient_v1.g` L214--329 | schema、6 generators、158 relators、canonical rho、972 roof rows を fail-closed に pin。source SHA = `c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9`。 | JSON の exact row は計算入力であり、論文の all-shadow theorem や M の isolated 性を自動的には証明しない。 |
| exact digests | current contracts | relator `12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e`; six-generator norm `ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`; word rows `283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930`; roof list `3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8`。 | digest equalityは同一入力の再現性だけで、semantic completeness の証明ではない。 |
| direct B4-B | `search/d972_b4_u_idrel_direct_logged_v1.g` L4--19, L422--520; `sol/luna_reply_152_b4_idrel_direct_logged_v1.md` L21--40 | IdRel log を元158 relatorsの共役積として replay する checker 契約。全972 identityのみ B terminal。 | GHA receipt/FSA/全行 replay の実物が未取得。bounded wall/rule/pass cap の結果は UNKNOWN。 |
| independent checker | `search/check_d972_b4_rewrite_cert_v1.py` L257--343 | schema/count/digests、全972 row、元 relator の insertion/deletion と free cancellation、各 row の空語終端を再計算。証明書なしは L324--327 で UNKNOWN。 | checker は local van Kampen certificate を検査するだけで、global cofinality/Ihara image を判定しない。 |
| global audit | `search/d972_b4_global_b_audit_v1.py` L296--330 | bounded rewrite、finite exact U、structural reduction、p-quotient、proof cert を各々別 gate として fail-closed。 | L302--319 は各 global gate を未成立/未提供と明示。これを bypass する artifact は存在しない。 |
| prior Tietze trace | `search/d972_b4_norm_tietze_trace_v1.py` L1--13, L257--345; `sol/luna_reply_152_b4_global_b.md` の最新 trace 記録 | 元 RS から elementary substitution を追跡し、127 generators まで dense 化。独立 replay は通過したが、972 norms の empty は 2 行のみ。 | structural presentation reduction も全972 identityも得ていない。127-generator receiptは global B の証明ではない。 |

補足として、direct lane の成功条件は「6/158 presentation 内の 972 exact words
が 1」であって、非成功の reduced word を「非自明」と読む契約ではない。これは
`sol/luna_reply_152_b4_idrel_direct_logged_v1.md` L21--22 の明示的な UNKNOWN
規律であり、A 候補には昇格しない。

## 2. 正典が与える global bridge と、B4 にまだ必要な仮定

### 2.1 original B4 と gentle B3 の型を混同しない

`docs/notes/b4_original_gtshadows_extraction_v1.md` L107--109 は、2008
`2008.00066` の original GT-shadow が B4/PB4 と pentagon を含む一方、2401 の
GT-shadow は最初から charming 条件を課す B3/PB3 系で、同名だが別の層だと明記する。
`docs/notes/2405.11725-抽出ノート_v1.md` L110, L143--151 も同じ注意をしている。

従って B4 の U_M receipt から 2405 の dihedral theorem を直接引用するには、
少なくとも次を証明する必要がある。

* U_M の generators/relators が original `PB_4/B_4` quotient の指定した N と
  同型である（全 generator map と全 158 relator replay）。
* 972 roof rows がその N の必要な pentagon constraints、target/source map、
  charming/all-surjectivity conditionsを漏れなく列挙している。
* B4 original shadow を 2401/2405 の `GT_gen` shadow に落とす忘却・持ち上げが
  対象 M で定義され、必要な reduction maps と可換する。

この比較が済むまでは、B4-B を「2405 Conjecture 5.1 の一対象が解決」とは
書けない。

### 2.2 isolated/cofinal の既知の枠組みと個別 M の欠落

original paper の抽出では、charming shadow の `settled` は
`ker(T_{m,f})=N`、`isolated` は N の全 shadow が settled である
（`docs/notes/b4_original_gtshadows_extraction_v1.md` L123--130、paper
pp.29--30）。Prop 3.3/Cor 3.5 は isolated subposet が cofinal であることを
述べる。同様に 2401 の Prop 3.14 は `N^diamond` が isolated で isolated
poset が cofinal としている（`docs/notes/2401.06870-抽出ノート_v1.md`
L91--94、paper pp.20--21）。これは**枠組みの定理**であって、今回の M が
isolated だという計算結果ではない。

個別の global bridge は、少なくとも次の receipt を要する。

1. U_M の target N/M と `ker(T_{m,f})` の型を固定する。
2. 全 charming shadowについて settled（または explicit `N^diamond` への
   refinement）を証明する。
3. その refinement の finite quotient、対象 inclusion、reduction map
   `R_{K,M}` を独立に replay する。
4. 2401 Thm 5.2 の Main Line `ML` に入る isolated nodesで、有限段データの
   compatibility を示す。

`docs/notes/E_identification_and_cofinality_v1.md` L82--90 は cofinality 自体は
正典で YES だが、同 L90--99 は有限深度の PASS から genuine を言えないと整理する。
`docs/notes/2401.06870-抽出ノート_v1.md` L124--137 はさらに、fake は一つの有限
refinement で証明できるが、genuine は「深さ d まで survive」までで UNKNOWN と
する。今回の 972 rows は一つの fixed M の ledger なので、この asymmetry を
埋めない。

`docs/notes/cofinality_ledger_draft_v1.md` L7--8, L49--56, L96--125 は、単発の
window measurement は cofinality に寄与せず、全 isolated family の reduction
compatibility、非分裂/entanglement を含む family theorem が必要だと警告する。
`docs/notes/d972_phase2_cofinal_execution_v1.md` L5, L25--31, L48--50, L84 は、
有限 isolated refinements を列挙できたとしても、finite 972 all-pass は A-side
semi-decisionであり、B を有限深度から認定しないと明記する。

### 2.3 genuine の判定は「全下位窓」

original B4 の Corollary 3.13（paper p.38）は

```text
[m,f] is genuine  iff it survives in every finite K <= N.
```

とする（`docs/notes/b4_original_gtshadows_extraction_v1.md` L116--121）。2401
の B3/gen 表現でも Corollary 5.4 は同じ全 refinement 条件である
（`docs/notes/2401.06870-抽出ノート_v1.md` L126--137）。したがって、local
B4-B が与える「M で 972 equations が identity」は次のどちらにもまだならない。

* ある shadow `[m,f]` が全 K で survive すること。
* isolated cofinal chain 上の compatible tuple が存在すること。

global genuine element を作る最小の設計は、(i)各 isolated node N_j の有限
`GT(N_j)` 候補、(ii)全 `R_{N_i,N_j}` の可換性、(iii)全有限 prefix の nonempty
compatible set、を receipt 化することだ。有限 branching が明示されれば
König/compactness で inverse-limit element を得られるが、同じ 972 件数だけでは
この nonempty-prefix 条件は出ない。

### 2.4 Ihara の非算術性は別の、より強い除外問題

2008 の抽出は、Ihara の埋め込み `G_Q -> GT` が Belyi により injective で、
surjectivity は Ihara の ICM 問題として未解決だとする
（`docs/notes/b4_original_gtshadows_extraction_v1.md` L140--144、paper p.4）。
2401/2405 は `arithmetical := Im(Ih_N)`、`genuine := Im(PR_N)`、
`arithmetical => genuine` とし、fake の実例は知られていない
（`docs/notes/2401.06870-抽出ノート_v1.md` L114--120、
`docs/notes/2405.11725-抽出ノート_v1.md` L18--25）。

よって genuine **かつ nonarithmetic** の Ihara counterexample には、以下の
いずれかが必要である。

* ある finite isolated N の shadow s を完全列挙し、`s` が全下位窓で survive
  すること（genuine）と、`s ∉ Ih_N(G_Q)` を証明すること（nonarithmetic）。
* ある cofinal compatible tupleを構成して `Thm 5.2` で global
  `GT_gen` elementにし、その一つの projection が算術像の外であることを示す。

後者の arithmetic exclusion は「複素共役 c がその tuple を写さない」だけでは
足りない。`docs/notes/settled_layer_verdict_v1.md` L171--174 の erratum は、
`f_c != 1` から `[-1,1]` が nonarithmetic と言った以前の推論を撤回し、別の
`sigma in G_Q` の実現可能性を全て排除しなければならないとする。この point は
global bridge で最も重要な fail-closed 条件である。

### 2.5 dihedral arithmetic theoremを B4 に移す経路は未接続

2405 Conjecture 5.1 は Dih の全 target K の全 shadow が arithmetical
（paper p.23; `docs/notes/2405.11725-抽出ノート_v1.md` L20--26）。証明済みの
主結果は n=2^alpha の family（Theorem 5.3, paper p.25;同 L28--34）であり、
それ以外を B4 U_M から自動的に埋める定理ではない。さらに同 L110 と
`docs/notes/b4_original_gtshadows_extraction_v1.md` L107--109 は original B4
GT と gentle B3/GT_gen の違いを明示する。

Ihara の不分岐 tower は補助的な 2-power route に限られる。ICM §5.2 の page pin
は `docs/scout/ihara_icm_unram_pin_v1.md` L12--34（印刷 pp.111--112）で、
`Q^(l)(infinity)` が cyclotomic 上 pro-l かつ l の外不分岐、と述べる。ただし
同 L34, L135--137 は講演録内にその文の完全証明や outer-to-cocycle bridge が
ないこと、L36--46 は最大性 Question 6.5.2 が open であることを記録する。
`docs/notes/litgate_u2_ihara_v1.md` L21--30 と
`docs/notes/u2_unramified_bridge_v1.md` L17--22, L55--64, L122--130 は、2-power
dihedral に対して R1（finite quotient）、R2（tangential basepoint/Aut対Out）、
R3（definition field と moduli field）を個別に閉じる conditional route であり、
B4 の six-generator U_M や非 2-power target を含む一般定理ではない。無限素点も
`u2_unramified_bridge_v1.md` L100, L182 で UNKNOWN のままである。

## 3. 最小の終端可能 certificate 設計

### 3.1 local B4-B certificate

GHA の direct IdRel が成功した場合でも、receipt の theorem field は次の限定形に
するのが安全である。

```text
For every i in {0,...,971}, the exact six-generator norm word
constructed from the pinned source/relator/roof artifacts is 1 in U_M.
```

必要な機械条件は以下。

* source SHA `c61b2b...c2b4a9`、relator digest `12fc...fccd2e`、word-row digest
  `283b...82930`、norm digest `ecf0...1683e`、roof digest `3015...461f8` を
  全て receipt と checker が再計算する。
* 158 original relators、6 generators、486 unique rows、972 duplicate mapを
  全て確認し、identity rows（JSON empty-list ambiguityを含む）を別型として
  正規化する。
* IdRel の各 derived rule と各 norm reduction を original 158 relators の
  signed conjugate productとして自由群で replayする。package の opaque rule
  count、wall cap、nonconfluent/partial の statusだけでは terminal にしない。
* independent checker が同じ sourceから 972 exact wordsを再構築し、全行が空語
  になることを確認する。

これは local finite-window の **cross-checked candidate** であり、AGENTS の
語彙では Lean proof がない限り `verified` と呼ばない。これだけから A/B の
global dichotomyを埋めない。

### 3.2 global genuine bridge certificate

上記 receipt に以下を追加する必要がある。

1. **semantic map:** U_M の各 generator と元の B4/PB4 generators、158 relators
   の双方の free-group replay、そして M/target N の正確な定義。
2. **row completeness:** 972 rows が対象 M の relevant pentagon/roof equations
   と duplicate map を尽くすことの紙上 lemma または mechanically checkable
   enumeration（単に count=972 では不足）。
3. **isolated nodes:** M または `N^diamond` の settled/isolated certificate。
   各 node の finite `GT(N)`、source/target kernel、reduction mapsを明示する。
4. **cofinal compatibility:** isolated nodesを cofinal chain/familyとして pinし、
   全有限 prefix の compatible tuples が nonempty であることを independent
   checker が検査する。これで初めて ML inverse limit/compactness を使える。
5. **global interpretation:** その compatible tuple が original `GT` または
   `GT_gen` のどちらの object を与えるか、B4→B3 gentle projection を使うなら
   forgetful/lift mapと可換 diagramを証明する。

### 3.3 Ihara counterexample certificate

global tupleを作っただけでは nonarithmetic ではない。最小の A/Ihara side
certificate は、ある有限 isolated projection N について次を全て含む。

* `s_N` が full shadow groupの元である（hexagon/pentagon、surjectivity、型を
  original/gentle のどちらかで明示）。
* `s_N` が全下位 K に survive するか、または cofinal compatible tupleの
  projectionであること（genuine）。
* `Arith_N = Im(Ih_N)` を完全に上から抑える/列挙する定理付き receipt。
* `s_N notin Arith_N` の独立判定。complex conjugation一個の不一致、cyclotomic
  bit一個、bounded absenceはこの条件を満たさない。

この finite projection exclusion が得られれば、global arithmetic elementの
projectionは常に `Arith_N` に入るので、global tupleは nonarithmetic と結論できる。
逆に、B4-B all-pass は defectを見つけないため、単独ではこの exclusion receiptを
供給しない。

## 4. 既存資料の status 台帳

| 主張/道具 | 現在の札 | 根拠・限界 |
|---|---|---|
| exact 6/158/972 input と digest | cross-checked computational input | canonical JSON、`search/d972_b4_pquotient_v1.g`、word-key checker。意味論的 all-shadow theoremではない。 |
| B4 direct IdRel all 972 identities | UNKNOWN / GHA pending | `sol/luna_reply_152_b4_idrel_direct_logged_v1.md` L33--40；証明書未提供。 |
| bounded KBMAG/Tietze output | UNKNOWN | `search/d972_b4_global_b_audit_v1.py` L302--319；127-gen traceで empty 2/972のみ。 |
| isolated subposet cofinal | paper-framework candidate | original 2008 Cor 3.5 / 2401 Prop 3.14、抽出ノート L129 / L93--94。特定 M の membershipは未証明。 |
| Main Line inverse limit | paper-framework candidate | 2401 Thm 5.2（抽出ノート L124--127）。B4 U_Mからの compatible tupleは未構成。 |
| finite-depth all-pass ⇒ genuine | **成立しない/UNKNOWN** | 2401 Cor 5.4の非対称性、`d972_phase2_cofinal_execution_v1.md` L5, L84。 |
| Dih全 target の arithmetic surjectivity | Conjecture | 2405 Conj 5.1（抽出ノート L20--26）。2-powerのみ Thm 5.3。 |
| Ihara global surjectivity | open | original note L140--144; ICM question pins。 |
| genuine nonarithmetic shadow | UNKNOWN | fake実例なし（2401 L118--120）；settled-layerの `f_c` shortcutは L171--174 で撤回。 |
| U2 unramified bridge | conditional / scoped | `u2_unramified_bridge_v1.md` L17--22, L122--130。B4一般化なし、最大性禁止、無限素点UNKNOWN。 |
| Lean global B4/Ihara proof | absent | `lean-arith/LeanArith/BridgeBAffine.lean` L4--8 は affine base/candidateのみで、PreGalois、fiber、tangential basepoint、freeness、inertia、exactnessを主張しない。`ShadowAxioms.lean` L1--5 は project axioms と明記。 |
| repository claim vocabulary | authoritative policy | `provenance/CLAIMS.md` L3--9：candidate / cross-checked / verified(Lean限定) / UNKNOWN。 |

## 5. 文献・PDF の再現手順

一次資料として対応するファイルは次で固定されている。

* `papers/2008.00066-what-are-gt-shadows.pdf`（original B4/PB4、settled/isolated
  pp.29--38、Cor 3.13 p.38、Ihara/Belyi p.4、Abelian Remark B.3 p.52）。
* `papers/2401.06870-gt-shadows-gentle-version.pdf`（isolated/cofinal pp.20--21、
  Main Line Thm 5.2 pp.28--30、genuine/fake pp.21--25）。
* `papers/2405.11725-nonabelian-quotients-gt-elementary.pdf`（Conj 5.1 p.23、
  isolated Dih pp.17--22、2-power Thm 5.3 p.25、inverse-limit Dih_2 pp.29--31）。
* `papers/ihara-ICM1990-braids-galois-arithmetic-functions.pdf` と OCR版
  （ICM §5.2 印刷 pp.111--112、Question 6.5.2 p.118付近）。

数式・定理文を最終引用する場合は AGENTS の Poppler 手順で**ページ画像を先に**
作る。

```powershell
& "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin\pdftocairo.exe" -png -r 150 -f <page> -l <page> papers\<paper>.pdf $env:TEMP\d972_bridge_<tag>
```

`papers/txt/` は検索用に限り、最終的な式番号・定理文は画像と対応付ける。
PDF、page images、OCR は `%TEMP%` に置き、receiptには input PDF SHA、ページ番号、
画像SHA、抽出ノートの該当行を記録する。Lean を使う場合は build と `#print axioms`
の出力を添え、project axiom を使ったものを `verified` と呼ばない。

## 6. 親への handoff

* 直接 IdRel GHA が `B4_B_DIRECT_LOGGED_TERMINAL` を出すまでは、B4-B は UNKNOWN。
* それが出ても、上の local theorem（972 exact identities）を超える主張をしない。
* 次の最短 global bridge は、(a) U_M↔original B4 semantic map、(b) M または
  `N^diamond` の isolated/cofinal refinement、(c) compatible finite-prefix receipt、
  (d) arithmetic image exclusion、の順で別々に実装・監査すること。
* 「全972が通った」「complex conjugationが違った」「finite depthで全pass」は、
  いずれも genuine nonarithmetic Ihara counterexample の証明ではない。
* したがって本棚卸しの最終判定は、**global genuine/cofinal shadow と Ihara
  counterexample は未確立。現時点で安全な status は UNKNOWN** である。
