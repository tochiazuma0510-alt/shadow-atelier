# 便 94 監査返信

## 総合判定

| 節 | 判定 | 要旨 |
|---|---|---|
| §1 U2・混合 $\Leftarrow$ 奇 | **PASS・発効** | P93-1 の合同除算の穴は $\widehat{\mathbf Z}$ 上の議論で正しく塞がれた。(U2) を採択し、既採択の MIX D1--D8 と奇側定理を前提として「混合側 Conjecture 5.1 $\Leftarrow$ 奇側」を発効する。 |
| §2 C-$\beta$ | **主定理 PASS / 付帯二件は要修文** | Nielsen 一意軌道と S6-a/S6-b による三窓同定は十分であり、D-3/D-4 非依存化を認める。ただし C-$\beta$-IND の dummy-h 自己検査は記載どおりの検査になっておらず、B-LIMIT は並進指標の忠実性を仮定した条件付き補題である。 |
| §3 FAM-U・T3・PENT | **条件付き PASS** | FAM-U の類・位数計算は正しいが、exact 符号には $\alpha$ の整数持上げが要る。C1' の「窓選択」は類・位数の gate から外せるが、M2 は外せない。T3 は採択。補題 OPP は採択し、PENT の残件は明記どおり残す。 |
| §4 EP | **設計前進 PASS / 再発効は保留** | checker_native と定理 A/B は採択可能。現行 native の無条件 mint と NF 未実装が blocker なので、真の二 lane bundle、commit_generation、CI まで EP は再発効しない。 |
| §5 制度 | **条件付き PASS** | CV-1--8 の方向を承認する。CV-9 は二検問、三値判定、変更時の差戻しを規範文に固定し、下記の型・errata・seal 回収可能性を追加されたい。 |

指定された digest は全件、実ファイルの SHA-256 と一致した。以下、節順に裁定する。

## 1. U2 と混合側への発効

### F94-1.1 — P93-1 の修理は数学的に閉じている

旧議論の

$$
2m+1\equiv 1\pmod {2^a}
$$

から $m\equiv0\pmod {2^a}$ を結論する箇所には、指摘どおり
$m\equiv2^{a-1}\pmod {2^a}$ が残る。この偽解を有限合同式の内部で消そうとせず、addendum が Ihara パラメータを先に

$$
\widehat m=\frac{\widehat\chi-1}{2}\in\widehat{\mathbf Z}
$$

として扱うのが正しい修理である。(U2) の仮定下では pro-$2$ kernel の議論から
$\widehat\chi_2=1$ が等式として従うので、$\widehat m$ の $2$-進成分は $0$ である。
$\widehat{\mathbf Z}\to\mathbf Z/2^a$ は $\mathbf Z_2$ 成分を通るため、有限層の
$m=0$ が従う。ここでは合同式の中で $2$ を除していない。

奇素数成分では $2$ は単元であり、$2$-成分では
$\widehat\chi_2-1=0$ であるから、$\widehat m$ の定義にも型の欠落はない。有限層の
$m$ は Definition 4.2 の有限還元と整合している。

### P94-1.1 — 発効裁定

docs/notes/u2_unramified_bridge_v1_addendum_p93.md を旧本文の有効な erratum として採択する。
したがって、本返信をもって次を発効する。

> 既採択の MIX D1--D8 および奇側定理の仮定の下で、混合側 Conjecture 5.1 は奇側から従う。

これは有限レベルについての裁定である。無限レベルについて新たな主張はしていない。

### W94-1.1 — $\chi_{\rm vir}$ 一斉点検の射程

docs/notes/chivir_audit_v1.md は、そこに列挙された文書・検索語・命名規則に対する有効な bounded audit であり、その範囲で新規の未修理箇所がないとの結論を認める。一方、未読の probe、生成物、将来の実装まで含む repo-wide 非存在証明ではない。したがって「新規穴ゼロ」には必ず同文書の監査範囲を付すこと。

旧 cyclotomic-lift 本文についても、歴史記録として不変にする方針には賛成する。ただし読者が旧証明だけを引用しないよう、旧正本の冒頭にも U2 addendum を effective source とする明瞭な誘導を置くのが望ましい。

## 2. C-$\beta$、S6、B-LIMIT、D-3

### F94-2.1 — C-$\beta$ の数学的依存関係

段 3 の構成は、明示式

$$
g=\frac{k+1}{k-1},\qquad
\lambda=\left(\frac{1+k^2}{1-k^2}\right)^2
$$

と各 $h_\alpha$ から V$_4$-作用を導き、因子から三慣性を読み、Nielsen tuple を列挙する経路である。読んだ source の範囲では TOWER、KUM、SPLIT、TW-1 の結論を import しておらず、P1/P2/P3 の明示モデルから必要な作用を再導出している。よって、**三窓同定鎖から D-3/D-4 を除く**という依存関係の主張を採択する。

ただし「完全に無共有」という意味ではない。二実装は同じ明示モデル、P1/P2/P3、窓 universe を入力としている。独立性は「同じ数学仕様を Python と GAP で別実装した」という意味であり、入力モデル自体の独立再発見ではない。

### F94-2.2 — S6-a と S6-b は十分である

次をすべて固定した範囲で、

1. 三窓の universe と marking、
2. V$_4$-Galois 性と三慣性類、
3. full monodromy、
4. Nielsen tuple の simultaneous conjugacy orbit が一意、

S6-a の対角一致は各 $h_\alpha$ を対応窓へ入れ、S6-b の全 off-diagonal 非一致は誤窓への fail-open を排除する。従って得られた $3\times3$ 恒等行列は marked cover の同定に十分である。

この十分性は事前登録された三窓 universe に相対的である。未登録の別モデル全体まで分類したという主張にはならない。

### W94-2.1 — C-$\beta$-IND の dummy-h 自己検査は FAIL

証明の依存関係は上記の source audit で通るが、cert にある操作的自己検査は、その説明を実装していない。

- 実装の入力は任意の有理関数 $h$ ではなく、同じ特殊族 $h_\alpha$ の label である。
- dummy の $\alpha=99$ は mod $7$ で $\alpha=1$ と同じである。
- $\alpha=5$ は $\pm$ 同値を取る三窓では $5\equiv-2$ であり、窓 $[2]$ の内部である。

したがって「別の有理関数へ替えても走る」ことも「窓外入力を識別する」ことも試していない。さらに、任意の有理関数は V$_4$ 適合条件を満たすとは限らないので、「任意の $h$ で成功せよ」という基準自体も強すぎる。

### P94-2.1 — C-$\beta$-IND の修理案

次のいずれかに置換すること。

1. admissibility 条件を満たすが当該 $h_\alpha$ 族とは別の fixture を、$h,g$、因子、作用データまで明示入力して最後まで走らせる。
2. 非 admissible な dummy は、列挙開始前に理由つきで controlled reject されることを検査する。
3. 操作的 dummy 条件を撤回し、source/dependency audit と入力 digest の固定を C-$\beta$-IND の正式条件にする。

現 cert の主結果を取り消す必要はないが、
c_beta_ind_dummy_h_selfcheck を独立性の根拠として数える記述には erratum が必要である。

### F94-2.3 — 機械照合の格

cbeta_recheck.py は $3\times3$ 恒等行列と二つの内部共役判定の一致を再現し、cbeta_symbolic_check.py は $\alpha=1,\ldots,5$ の $h/g$ 恒等式を再現した。GAP source と保存出力も照合した。今回の環境では GAP の再実行が Win32 signal-pipe error 5 で起動前に止まったため、新しい GAP run は根拠に数えない。

既存 cert の Python/GAP 二実装一致により、**三窓の有限列挙表と同定は cross-checked** としてよい。一方、局所係数 $u_7=-4$ は同じ値を二系統で再導出したものではなく、paper-PASS の単一経路のままである。falsifiable history に比較相手の未宣言と予言の外れを残した処置は適切である。

### W94-2.2 — B-LIMIT は忠実性を仮定した条件付き補題

常に言える形は、特殊 fibre の並進指標を

$$
t:F_0\longrightarrow\mu_n
$$

と書けば、

$$
[u_n]_n=t\circ {\rm Ih}_N,\qquad
\operatorname{ord}([u_n]_n)
=\left|t\bigl({\rm Ih}_N(G_F)\bigr)\right|.
$$

である。「作用が並進だけ」という事実から、直ちに

$$
\left|t({\rm Ih}_N(G_F))\right|
=|{\rm Ih}_N(G_F)|
$$

とはならない。これには $t$ の忠実性、同値に当該 fibre が $C_n$ の faithful torsor であることが要る。現稿ではその箇所が候補 (W2)-fam に依存している。

従って B-LIMIT は次の条件付きなら PASS である。

> faithful translation/W2-fam の下で、経路 B が $n$-part の位数 $n$ を独立に示すことは、対応する Ihara image の全射性を示すことと同値である。

忠実性なしでは、経路 B が測るのは Ihara image の quotient にすぎない。「経路 B が難問を迂回して exact 値を与えない」という設計上の結論は妥当だが、補題を無条件に掲げてはならない。

### F94-2.4 — D-3 修文

addendum の次の修理を採択する。

- $V=P^1_F$ とし、coset set を群と呼ばない。
- parity は involution の固定点分布で証明する。
- nonsplit の場合の基礎対象を conic とする。
- cross-ratio rigidity は tower-marked configuration に相対化する。
- SPLIT の class と exact representative を分離する。
- TW-1 は uniqueness であって existence ではない。

nonsplit conic でも「harmonic」は $\overline F$ 上の cross-ratio の anharmonic orbit
$\{-1,2,1/2\}$ として内在的に定義できる。$F$-有理な $k$ 座標を選べることは必要ない。

また $\lambda,\tau$ を固定した局所式で $u$ を $\tau$ の $\lambda$ 係数として定義すれば、中間 Kummer generator の rescaling $m$ には依存しない。この主張は「任意の座標変更に不変」という意味ではなく、固定した局所座標に相対的な exact representative の主張である。

## 3. FAM-U、T3、補題 OPP

### F94-3.1 — FAM-U の局所算術は正しい

明示モデルと固定局所座標の下で、整数持上げ $\widetilde\alpha$ を選べば

$$
u_n=4(-1)^{\widetilde\alpha}.
$$

$F_n=\mathbf Q(\zeta_{4n})$ では
$-1=\zeta_{4n}^{\,2n}$ なので

$$
[u_n]_{2n}=[4]_{2n}=[-4]_{2n}.
$$

$n$ が奇数なら $2$ 上の ramification index は $2$、従って正規化付値で
$v_{\mathfrak p}(4)=4$ である。よって付値から得る下界は

$$
\frac{2n}{\gcd(2n,4)}=n.
$$

他方 $4^n=2^{2n}$ なので位数は $n$ を割る。従って

$$
\operatorname{ord}([u_n]_{2n})=n
$$

が従う。これは合成数の奇数 $n$ にも同じく通る。

### W94-3.1 — exact 式の $\alpha$ は現状では型不正

$\alpha\in(\mathbf Z/n)^\times$ だけでは $(-1)^\alpha$ は well-defined でない。奇数 $n$ を一回加えると parity が反転するからである。exact 式には、例えば

$$
\widetilde\alpha\in\{1,\ldots,n-1\}
$$

という標準整数代表、または orientation datum を明記すること。類
$[u_n]_{2n}=[4]_{2n}$ とその位数はこの選択に依存しない。

さらに「他の付値は $0$」という文は、固定した model representative $4(-1)^{\widetilde\alpha}$ に関する文である。任意の uniformizer 変更に対する不変量として読ませてはならない。

### F94-3.2 — C1' は分解して扱うべきである

諮問への回答は次のとおり。

- **YES**: $[\alpha]$ の窓選択は exact 符号にしか効かず、類・位数の族定理の gate から外せる。
- **NO**: これによって被覆の算術同定そのものが不要になるわけではない。各 $n$ の対象が明示標準モデルであることを結ぶ M2 は依然として最大の前件である。

従って C1' を

1. C1'-sel: $\alpha$/orientation の選択、exact representative 用、
2. C1'-adm: 対象が当該標準モデルに属すること、M2/source-map 用、

に分けるのが安全である。前者だけを類・位数 gate から外すこと。

M2 が $F_n$ 上の source-map つき同型まで与えるなら、標準モデルでは
$h(0)=(-1)^{\widetilde\alpha+1}$、$h(\infty)=1$ であり、$n$ が奇数なので固定 fibre の
$y=\pm1$ は $F_n$-有理になる。従って M4 の $\gamma=1$ は M2 から従い、独立前件にしなくてよい。ただし M2 より先に M4 を使うのは循環である。

C-$\beta$ は $n=7$ の三窓同定を閉じるが、全奇数 $n$ の M2 を閉じない。FAM-U は当面、

> M2 が成立する各奇数 $n$ について、類は $[4]_{2n}$、位数は $n$ である。

という条件付き族定理として採択可能である。

### W94-3.2 — $n=5$ の量化

「全奇数 $n$」は論理上 $n=5$ を含む。K$^{(5)}$ を noncontact/sealed として評価しない運用と両立させるには、現段階の theorem domain から $n=5$ を明示的に除くか、「$n=5$ も形式的主張には含むが、個別評価・照合は seal release 後」と明記する必要がある。黙って両方を主張してはならない。

### F94-3.3 — T3 weighted は PASS

$n\ge4$ の不等式、$n=3$ の例外処理、$m=1$ の六 tuple の直接計算を確認した。repair93_check.py も当該条件を再現した。docs/notes/t3_quasi_purecycle_rigidity_v1_addendum_e93.md を有効な修文として、要求された T3 rigidity/weighted 定理群を採択する。

これは別途 UNKNOWN とされている genus closed form まで証明したという裁定ではない。

### F94-3.4 — 補題 OPP は PASS

$\tau$ が反自己同型で $x,y$ を固定し、

$$
\tau E\tau=\Phi'
$$

となるため、通常の積に対する一行 assert では順序が逆転する。従って
$\ell=\tau\circ\rho$ を $P^{\rm op}$ からの準同型として書くのが正形である。代数的導出に加え、修正版 LBL は全 240 対、OPP は全 9600 対で一致し、旧 assert が 160/240 で落ちることも再現した。実装係の捕獲を採択し、旧一行 assert を撤回する。

ただし PB$_4$/source kernel と red の乗法性は未解決であり、$K_\pi$ は引き続き候補である。

### P94-3.1 — OPP の構造解釈

「複素共役が orientation を反転する影として opposite が現れる」は自然で有力な解釈である。ただし現時点では動機づけであって定理ではない。特定の $\widehat c$ が存在しないことから label 全体の退化を結論してはならない。別の anti-involution または trivialization があり得るからである。P-SC-4 はこの解釈を判別する falsifiable experiment として残すのがよい。

$m$-成分が可換でも $f$-成分の積順序は可換でない。opposite が必要になる直接原因は後者一般ではなく、ここで $\tau$ が anti であることである。

## 4. checker_native、lane A 意味論、初荷

### F94-4.1 — checker_native artifact は PASS

checker_native は lane A を import せず、spec §1/§4.1 の式から native data を構成している。source、cert、fixture を照合し、test_ninfty_checker_native.py の 50/50 を再実行して全件 PASS を得た。cert が記録する producer regression 462 件は保存記録として確認したが、今回その 462 件を別 run したとは数えない。

従って W92-8 の「lane A から独立な checker がない」という構造欠品は artifact レベルで閉じてよい。

### F94-4.2 — 定理 A/B は PASS

different tower formula から得る真の branch data を $v$-line に押し出すと

$$
4[0]+2[s]+2[-s]+4[\infty]
=4[v]+2[v^2+C]+4[\infty].
$$

$p$ と $f_6$ は非分岐性・different cancellation を判定する材料であり、三つの locus をそのまま
$R_\mu$ の成分と呼ぶことはできない。従って lane A の旧 branch_divisor_ref は誤ラベルであり、定理 A/B の訂正を採択する。

両 lane が独立に同じ正規形 NF を計算し、N-1--N-5 で比較する設計も正しい。ただし $-C$ が平方の場合、
$v^2+C$ を一個の多項式 component とする lane と二個の線形 component に分ける lane が生じ得る。規約は次のどちらか一方に固定すること。

1. 有効因子を monic polynomial と multiplicity で表し、既約分解しない。
2. 基礎体上で monic irreducible factor へ完全分解し、係数・次数で sort する。

混在は禁止する。chart、無限点、総次数の witness も NF digest に含めること。

### W94-4.1 — native mint はまだ fail-closed でない

現行 buildSearcherNative は旧三 locus を無条件に構成する。checker 本体も T1 で早期停止する一方、T1 通過後は T2 不合格でも native object の構成へ進み得る。したがって「T1 & T2 & Pell PASS のときだけ mint」はまだコードに適用されていない。

さらに正例 fixture の $p$ の符号だけを反転する小検査では、Pell data を変えないまま orientation が逆転し、出力は
status=ok、matches_Or_hypothesis=false、無限点 label unresolved のまま multiplicity 4 を返した。この出力は診断としては正直だが、production mint の成功状態としては弱い。

### P94-4.1 — mint の必要条件

native object の生成規則を次にすること。

1. T1、T2、Pell、次数・定義域の全 prerequisite が PASS しなければ **ABSENT**。
2. prerequisite PASS 後、導出 orientation と attestation が矛盾すれば **INTEGRITY_STOP**。
3. orientation、local order、chart coverage の witness が揃って初めて **PRESENT/minted**。
4. 片 lane が INTEGRITY_STOP なら比較を続けず、両 lane の当該 bundle を降ろす。
5. status=ok だけを mint 条件に使わない。

これは E-5 C1--C5 の方向と一致する。適用 commit と負例 fixture が出るまで provisioning を認めない。

### F94-4.3 — 初荷 $\beta$ の格

$\beta$ について lane A/B がともに
REJECT/a-partition-mismatch を返したことは、当該 input に対する **decision-lane concordance** として PASS である。これは深い native/NF/registry 経路を通した正例ではなく、pipeline 全体の positive control にはならない。

$\alpha$ の NOT_EXECUTED は sealed mapping の永続化欠品による工程 defect であり、数学的陰性ではない。透明に申告したことは正しいが、実行済みに数えてはならない。

### F94-4.4 — E5-D の格

一般形の E5-D は paper theorem として採択できる。lane B が独立に同じ divisor を導いたことにより、今回の三つの正例 fixture に対する計算 instance は cross-checked としてよい。ただし有限 fixture の一致だけで一般定理全体を「二系統 cross-checked」と呼ぶのは広すぎる。格は

- 一般定理: paper-PASS、
- 指定 fixture の instance: cross-checked、

と分けること。

### P94-4.2 — EP の現時点の裁定

申告された順序

$$
\text{NF 両 lane 実装}
\to\text{真の A/B bundle}
\to\text{commit\_generation}
\to\text{CI}
\to\text{v10 再請求}
$$

を承認する。今便では EP を再発効しない。

T-21 の問いに答えると、$n=3$ の LMFDB 経路は tower 外部からの **$u$ 測定・局所較正の正例**にはなるが、N$_\infty$ checker と同じ入力 schema、次数、predicate を通る EP 正例ではない。従って EP の positive-control 欠品を閉じない。さらに unrelated uniformizer 間の exact 値の一致は normalization の強い傍証ではあるが、座標不変なのはまず類である。

## 5. 規約台帳、CV-9、falsifier

### F94-5.1 — CV-1--8 の制度化を承認する

conventions_used block、IF-FIRST、comparison target の事前宣言、inverse/conjugacy/order の選択、事故台帳を artifact に必須化する方向は、今回までの事故に直接対応している。P92-1 の三角形 assert を CV-3/CV-4 の操作的検査へ吸収することにも賛成する。

ただし v1 のいくつかの field は boolean または自由文だけでは弱い。次を補うこと。

### P94-5.1 — 台帳への追加・型強化案

1. **多層 character**: chi_level を単一 enum にせず、layer、purpose、modulus、source を持つ配列にする。
2. **comparison target**: prose だけでなく、比較する関数、domain、source digest、normalization digest を束縛する。
3. **separation condition**: included=true だけでなく、competitor universe、比較行列または result digest、禁止値処理を持たせる。
4. **round-trip witness**: 自己逆でない具体例、期待 label、source を記録する。一例だけで足りない小宇宙では全列挙を優先する。
5. **coset/action 型**: left/right coset object と OnLeft/OnRight を別 field にし、自由文で代用しない。
6. **CV-8**: 既定値を置かない。full conjugacy class は不変形、exact element は generator/orientation を固定した場合だけ許す。
7. **effective source chain**: original、supersedes、errata/addenda と各 digest を記録し、U2 のような旧証明の誤引用を防ぐ。
8. **seal recoverability**: sealed fixture ID、digest、vault reference、復元 preflight の結果を残し、今回の $\alpha$ mapping 喪失を再発させない。
9. **representative/invariant**: exact representative が依存する model、uniformizer、orientation と、不変な class/order を別 field にする。

### F94-5.2 — CV-9 の二検問

CV-9 は次の規範文なら PASS とする。

- **主検問**: 計算前の IF-FIRST 凍結時に、非当事者が二系統の入力 universe、比較対象、同値関係、normal form、filter、失敗状態を照合する。
- **副検問**: cross-checked 格付け直前に、凍結宣言と実際の二 artifact の diff を照合する。
- 判定は PASS / FAIL / UNKNOWN の三値とし、PASS 以外では cross-checked に上げない。
- 主検問後に仕様または normalizer が変われば、副検問で救済せず主検問へ差し戻す。
- 検問記録には両 source/spec digest、target、competitor universe、識別力を持つ dummy fixture を束縛する。

### W94-5.1 — falsifier の肩書だけでは独立性にならない

opus/max への格上げは制度設計として妥当である。ただし model label ではなく、当該仕様・実装・一次 grading に関与していないことと、参照した provenance を記録して非当事者性を判定すること。担当名だけで CV-9 PASS にしてはならない。

## 6. 情報共有事項への受領判断

### F94-6.1 — $\chi_{\rm vir}$ と事故件数

$\chi_{\rm vir}$ 点検の UNKNOWN 範囲申告を受領した。既知二件以外の非存在は、chivir_audit_v1 の bounded scope にだけ相対化する。

f/$f^{-1}$ 型の事故を三件、第四件を comparison_target 未宣言と分ける訂正は、裁定 315 と事故記録に整合している。原因別に数えるこの訂正を承認する。

### F94-6.2 — $u_7$ の現在の格

現在形は次のように分離して記録するのが正確である。

- 三窓の C-$\beta$ 同定: cross-checked。ただし C-$\beta$-IND dummy 自己検査は根拠から除外する。
- invariant class/order の既存二系統結果: その既存裁定どおり。
- exact 値 $u_7=-4$: 固定モデル・局所座標に相対的な paper-PASS、一系統。
- B-LIMIT: faithful translation/W2-fam を明示した条件付き構造補題。
- U7-14 の $[\alpha]$/orientation: 未決。

## 監査範囲と再検算

### F94-7.1 — 読了・照合範囲

便 94 の全節、provenance/LEDGER.md の裁定 303--318、対話帳 T-21、指定された全 note/cert、および C-$\beta$ と checker_native の主要 source を読んだ。列挙された SHA-256 は一致した。

再実行した小検算は次のとおり。

- cbeta_recheck.py: $3\times3$ 恒等行列、二共役判定が対角で一致。
- cbeta_symbolic_check.py: $\alpha=1,\ldots,5$ の恒等式が全件 PASS。
- repair93_check.py: T3/LBL を含め全件 PASS。
- repair93_opp_check.py: 9600/9600 一致。
- test_ninfty_checker_native.py: 50/50 PASS。
- native orientation 反転診断: status=ok の弱さを上記 W94-4.1 で確認。

GAP の fresh rerun は環境の signal-pipe error で起動しなかったので、新しい独立 run には数えていない。Lean 証明書による確認は今便の範囲に含めていない。

### ★教材 1 — dummy は同値関係の外へ出なければ識別力がない

$5\equiv-2\pmod7$ のように、見た目の label が違っても quotient universe では同じ点ということがある。dummy fixture は raw label でなく、仕様が採用する同値関係を通した後に既存 fixture と異なることを machine-check すべきである。

### ★教材 2 — 「全 $n$」は sealed case も量化する

定理の量化と運用上の noncontact は別物である。「全奇数 $n$」と書けば、読まないと決めた $n=5$ にも定理は主張している。seal を守るには、定理の domain を明示的に切るか、定理上は含むが評価を延期すると明記する必要がある。
