# 便 105 監査返書 — 数学便第 32 号

**総合判定: 分割裁定（P1 総組立は条件付き昇格、HS 本走と BOTTOM-UP freeze は差戻し、EP は実装設計まで限定承認、Lean 第 1 波は忠実性 FAIL）**

最優先請求への結論を先に固定する。

| 請求 | 裁定 |
|---|---|
| P1 / FAM-U-ASM | **条件付き PASS**。Route T の link-free 補題 TORS-U は生きており、総組立が使う一様 twisted 形 \((5'^b)\) から per-window \((Z_{2M}\text{-link})\) を外せる。格は **theorem-framework-relative [TB: canonical-source-pinned/v2]（条件履行 = v2.1）**。ただし B-4c を \((TB4^{\rm u})\) 依存として明示した versioned proof ID と、FAM-U-ASM の要求を exact \((5')\) でなく \((5'^b)\) とする記帳を条件とする。W2-fam・始点算術は昇格しない。 |
| HS 705,894 対本走 | **FAIL / 不認可**。CONV-WD/INJ と CF 数式・登録 fixture 較正は通るが、P/V wrapper は OPEN_ITEM のまま、三 wrapper とも cert を書かず、join checker は flat index と semantic key の対応を検査しない。(f) 容量要件も未充足。本走候補・較正 shard とも触れてはならない。 |
| BOTTOM-UP v4 freeze | **FAIL / freeze なし**。紙数学の主要修理は通るが、FREEZE-2 の発火宇宙と cert 仕様の次元集合が不一致である。IF-FIRST の M-ISO-8 表も v2.1 の実際の kill 機構と不一致。S1–S3.5 は unlock しない。 |
| 探索類型の standing authorization | **制度として条件付き承認**。ただし immutable class ID、exact universe、schema/source-map/output exposure/resource cap まで class manifest に入れること。現 §2/§3 は freeze 未成立なので第一適用にはならない。 |
| EP 第四陣 | 台帳 r3 は **DRAFT 設計 PASS**。IMAGE-MU v3 は **設計 PASS、実装準備のみ再開可**（route B、v1 は \(e=2\) 限定を採択）。suitelog v2 は従来の条件付き PASS。三状態札は不動。 |
| Lean 第 1 波 | lake build P1 自体は通ったが、**第 1 波全体の paper-fidelity は FAIL**。sorry 3 本、: True の no-op 2 本、内容を型に持たない T2 公理 4 本、手動 #print axioms が残る。正確な小補題だけを限定受領し、全面差戻し。 |

対話帳は T-28 まで読了した。本便指定の **22 artifact は SHA-256 を実 bytes から再計算し 22/22 一致**した。以下、本便の節順に裁定する。

## 1. P1 総仕上げ束

### F105-1.1　最優先点 B-4c の \(\zeta_M\): link-free 核は PASS

docs/notes/b6tw_linkfree_proof_v1.md の補題 TORS-U は正しい。有限巡回群 \(A\) と二つの忠実な正則作用

\[
 m:A\hookrightarrow\operatorname{Sym}(S),\qquad
 \tau:A\hookrightarrow\operatorname{Sym}(T)
\]

に対し、全単射 \(c:S\to T\) と、ある生成元の対 \(a_0,a_1\in A\) について

\[
c\,m(a_0)c^{-1}=\tau(a_1)
\]

を仮定する。この一回の生成元一致から
\(c\,m(A)c^{-1}=\tau(A)\) が従い、\(\tau^{-1}\circ(cmc^{-1})\) は \(A\) の自己同型となる。従って一意な

\[
 b\in(\mathbf Z/M)^{\times},\qquad
 c\,m(a)c^{-1}=\tau(a^b)\quad(\forall a\in A)
\]

が存在する。これは character fitting ではなく、巡回群全体上の自己同型の分類である。従って \(b\) は \(\gamma\) に依らず、root の同一視も要らない。

系 B-4c の「\(x\) の作用が \(\tau(\zeta_M)\) に対応する」の \(\zeta_M\) は、命題 B-2/Rule 側で \(X\leftrightarrow\tau(\zeta_M)\) と**命名するための生成元**である。TB2 の Puiseux root と同じ元だという主張ではない。既存 BFC 本文も root comparison を B-4c ではなく B-6 第 3 段に置いている。従って link は B-4c へ遡及せず、TORS-U の抽象比較に \((Z_{2M}\text{-link})\) は潜んでいない。

root object が別途与えられる場合には、二生成元のずれを追って

\[
 b=(\bar t_M\varepsilon)^{-1}=b_{\rm op}\pmod M
\]

となり、link と exact TB4 の下で \(b=1\) を回復する。よって link-free proof ID と現行 proof ID は競合せず、前者が後者を特殊化として含む。

ただし B-4c の既存証明は「(TB4) が採る後合成/左作用」と書く一方、表示上の前件は定理 B-4 だけである。link-free 論証が要るのは exact generator equality でなく左作用規約なので、数学的には \((TB4^{\rm u})\) で足りる。しかし依存欄を黙って弱めてはならない。次の versioned 記帳を条件とする。

> **B-4c\(^{\rm u}\)**: B-4c の全単射・\(G_K\)-同変性・\(\widehat F_2\)-同変性と Rule 側の \(\tau\) 命名は (TB1)–(TB3)+\((TB4^{\rm u})\) の左作用規約の下で成立する。TB2 root と Rule root の equality は主張しない。

凍結命名がある窓ではその \(\tau\) 名を使い、族文書にも一行記録すること。これは per-window seal/migration ではない。

### F105-1.2　MOS / MATCH-one / family completion

docs/notes/match_one_supply_v1.md の縮約は正しい。\(R^{\rm cyc}_{\rm formal}\) が \((5')\) を使う箇所は、単元冪写像が像の位数・特性部分群への包含・核を変えないことしか使わない。従って必要十分な要求は

\[
 \exists b\in(\mathbf Z/2n)^\times\ \text{（全 }\gamma\text{ に共通）}:\quad
 \rho_0(\mathrm{Ih}(\gamma))
 =\tau\!\left(\kappa_{u^{-1}}(\gamma)^b\right)
\]

であり、exact \((5')\) ではない。B-6\(^{\rm tw}\)-lf と B-7\(^{\rm tw}\)-lf がこれを一般に供給するので、Route T の窓は \(\alpha=1\) 一つで全奇数 \(n\) に一様、有限探索・root migration・per-\(n\) 手続きはいずれもゼロでよい。

MOS-4 への回答は次のとおりである。

- 便 103 F103-4 は per-window link を discharge していない。既存 proof ID の exact \((5')\) を TB 格で裁定した際に、link 行への言及が抜けていただけである。
- 従って過去会計では link が黙って消えたと読んではならない。
- **今回**監査した別 proof ID が初めて、総組立に使う twisted route から link を正当に除去する。

docs/notes/s3_family_completion_v1.md の紙数学も通る。

- Λ-REG: \(N_{G_n}(H)=H\)、\(|\Lambda|=2n\)、\(\langle X\rangle\cap H=1\) から \(\langle X\rangle\) の作用は正則。
- INN/SIXP-fam: \(\Phi_{0,f_k}=\operatorname{inn}(X^{-2k})\) の生成元計算は整合し、\(\rho_0\) の像は \(\tau(\langle\zeta_{2n}^2\rangle)\)、全 \(\alpha\ne0\) で忠実。
- MATCH-one: 独立な二つの存在窓は接合できず、同じ \(\alpha\) を要求する修理は必須かつ正しい。
- 追補の二矢印分割も正しい。(d1) は \(R^{\rm cyc}\)+MATCH-one+\((5'^b)\) に相対的、(d2) の含意は SURJ-Split で閉じる。ただし全族への適用は A2=(W2)-fam の candidate 性を継承する。

従って FAM-U-ASM は次の**限定された言明**として昇格を認める。

~~~text
theorem-framework-relative [TB: canonical-source-pinned/v2]
(条件履行 = v2.1; bridge proof ID = B-6^tw-lf/B-7^tw-lf;
 required bridge form = uniform (5'^b), not exact (5'))
~~~

これは「W2-fam が全奇数で成立」「全奇数で \(\operatorname{ord}(a_n)=n\)」「算術的始点が閉じた」を意味しない。それらは従来の candidate/open を保つ。昇格対象は、前件を明記した含意定理と族一様の窓側補題である。

また \(n=5\) は**純定理の domain からは外れない**。全奇数 \(n\ge3\) の群論証明は \(n=5\) でも成立する。封印除外とは \(K^{(5)}\) の値・窓データ・測定量へ接触しないという運用上の除外であり、定理の量化域除外とは分けて記帳せよ。

### F105-1.3　EXSEQ-LIM: 核心 PASS、完全証明の札は差戻し

docs/notes/tb_exseq_lim_proof_v1.md の代数的核心は正しい。

- \(A_L=L[\beta,\beta^{-1},(\beta-1)^{-1}]\) は PID。
- 有限 étale \(A_L\)-代数は有限 projective、従って有限 free。
- 有限個の構造定数・射の係数を有限段へ降ろせる。
- \(\Omega_{B/A}=0\) の base change と忠実平坦降下により étale 性を有限段へ降ろせる。
- SGA 1 Exp. I Prop. 3.1、Déf. 4.1、Cor. 4.8、Déf. 4.9 の引用内容は、papers/sga1-grothendieck-raynaud-arxiv0206203.pdf の該当ページ画像（PDF pp.17–21）で照合し、実質的に一致した。

しかし「完全証明」「債務全消滅」の札には次の補筆が要る。

1. 冒頭は SGA 入力を 3 件と数えるが、§7.4 で Cor. 4.8 を使うので実際は 4 件である。
2. affine finite étale cover と有限 étale algebra の対応、および affine sheaf \(\Omega\) と Kähler module の同定を「認める」としており、自前証明だけという会計ではない。
3. 有限段で射が isomorphism になる箇所は、射だけでなく inverse と二つの恒等式をさらに有限段へ降ろす一行が要る。
4. EXSEQ-LIM (3) は abstract group isomorphism までしか書いていない。profinite exact sequence に使うなら、fiber functor automorphism group の topology、極限写像の continuity、従って compact-to-Hausdorff による homeomorphism を明記せよ。
5. §0 は relative への障害を Ihara ③-1 一点とするが、§10 は ③-1 と block ④ Abhyankar の二点を正しく列挙する。前者を二点へ訂正せよ。

従って EXSEQ-LIM の核心は paper proof として条件付き PASS だが、v1 の「完全」は未批准である。上記を v1.1/addendum で閉じるまで、TB を canonical-source-relative や無条件へ上げない。既存の

~~~text
[TB: canonical-source-pinned/v2]（条件履行 = v2.1）
~~~

は維持し、今回の補筆不足を理由に旧 PASS を巻き戻す必要もない。

## 2. HS 本走 705,894 対

### F105-2.1　CONV と CF の紙数学: PASS（射程限定）

CONV-WD は \(N_{F_2}\) が verbal subgroup である範囲で正しい。語写像は quotient に降りる。CONV-INJ も、\(K(0,5)=F_3\rtimes F_2\to F_2\) の retraction と verbal subgroup の函手性から、P 側の 117,649 元が Q 側で衝突しないことを与える。この結論を非 verbal な一般窓へ広げてはならない。

CF の二式も独立に展開して一致した。\(A_{12}=A_1A_2,\ A_{21}=A_2A_1\) と書けば

\[
x^mA_1(f^{-1})\beta^mA_{12}(f)=f^{-1}A_{12}(x^{-m})c^m,
\]

\[
f^{-1}y^mA_2(f)\alpha^m=A_{21}(y^{-m})c^mA_{21}(f)
\]

である。登録 18 fixture の literal/CF 一致、二経路 mismatch 0、GHA 18/18、643.75× local / 586.9× GHA は **registered-fixture tool calibration** として受領する。本走定常速度への外挿ではない。

軽微補正として、現 EvalFullHexagonCF の ImageElm 呼出しは「ちょうど 4 回」でなく 5 回である。また A1/A2 の構築には、指定 generator images が本当に同じ群を生成することと、得た map が bijective であることの fail-closed 検査を本走以前に入れよ。

### F105-2.2　(a)〜(h) 完備という申告: FAIL

速度ではなく実行契約がまだ閉じていない。

1. lane_wrapper_P.g は P→Q 変換を OPEN_ITEM と印字し、PENT predicate を一件も呼ばない。
2. lane_wrapper_V.g は pcgs exponent vector→free word preimage を OPEN_ITEM と印字し、full hexagon を一件も呼ばない。
3. lane_wrapper_S.g は loop の形を持つが、三 wrapper とも would_write_records を印字するだけで cert JSON を書かない。従って (b) の「実行 bundle 実物」でも (c) の lane output schema 実物でもない。
4. join_checker.py は key の重複・欠落・coverage を調べるが、flat_index から \((m,e_1,\ldots,e_6)\) を**独立に再導出しない**。Lane P の f_key → six candidate_keys も再計算しない。全 key を同じ誤った permutation で並べても通る。pcgs_endian fixture は metadata の差を検出するだけで semantic bijection の反証にならない。
5. prereg v2 の digest/主経路は CF 採用前の wrapper 設計を含み、付録 C v2 の shard 数も現提案と同期していない。新しい versioned prereg/appendix が要る。
6. F104 が本走再申請**前**に要求した (f) bytes/candidate・retention・回収可能性は未測定である。「認可後の較正 shard/第 1 shard で確定」は順序を逆転する。18 fixture は機能較正であり、steady-state artifact 容量の標本ではない。

従って現状は (a) の多く、(g)、(h) の人工 fixture、CONV/CF の数学を受領できるに留まり、(b)(c)(f) が FAIL、(d)(e) も current execution path へ再 pin が必要である。

### F105-2.3　発火裁定

**705,894 対本走を認可しない。較正 shard も本走宇宙の候補に触れるため認可しない。** 今回許すのは次だけである。

- wrapper/schema/join checker/workflow の実装完成。
- 既登録 18 fixture と人工 join fixture の再走。
- 本走候補を一件も含まない純粋な key arithmetic/schema fixture。

再 gate には、少なくとも次を一束で出せばよい。

1. P/S/V の runnable wrapper と実 cert JSON。
2. CF/CONV-P を主経路へ統合した digest 束縛と、baseline/CF の登録 fixture 一致。
3. checker 自身が flat index↔semantic tuple と P-lane six-key expansion を再導出する fixture。
4. exact shard universe・workflow 分割・timeout/STOP を同期した versioned prereg/appendix。
5. 本走候補非接触で容量を測れるならその receipt。どうしても候補が必要なら、blind timing-only microgate を別に申請すること。

この小 gate が通るまで main matrix への自動連鎖発火はない。

## 3. BOTTOM-UP v4 / AUTO-SETTLED / ISO R3-R4

### F105-3.1　v4 の紙修理: 大部分 PASS

次を受理する。

- MARK-BIJ-adm: \(V=K^{(5)}/N\) 上の \(K^{(5)}\) の内作用は \([K^{(5)},K^{(5)}]\subseteq N\) により自明で、作用は \(\widehat G_5\) を経由する。
- roof survival は「良い lift が存在しない」すなわち \(\neg\exists U\trianglelefteq\widehat P\) の形であり、旧 existential SAT の穴を閉じる。
- LIFT-ENUM は非空なら \(Z^1\)-torsor。全 \(Z^1\) parameter を走査し、その後に normality を filter する順序が正しい。traversed_count=\(|Z^1|\) と accepted count は別欄にせよ。
- B-1 の \((m,f)\) 全列挙・dedup、B-2 の well-defined descent+有限 quotient bijective という settled 判定は正しい。
- \(\mathbf F_3S_3\)-module 型数 dim 2/3/4 = 5/10/18 は母関数と一致する。

### F105-3.2　freeze blocker: exact firing universe が一意でない

FREEZE-2 と §2.3 は

~~~text
(V-cen), p in {2,3}, dim <= 4, window_order <= 8000
~~~

と書く。他方 cert 仕様は

~~~text
p=2: dim in {2,3,4}; p=3: dim={2}
~~~

である。cap は p=3 dim 3/4 を除くが、p=2 dim 0/1 と p=3 dim 0/1 を除かない。従って両者は同じ集合ではない。意図が現 17 行なら、正文を

~~~text
dim_p2 in {2,3,4}; dim_p3={2}; window_order <= 8000
~~~

へ versioned に直せ。別の意図なら cert 分母を作り直す必要がある。悉皆/EMPTY/下限の量化域なので、これは軽微な prose ではなく freeze blocker である。

さらに docs/notes/iso_r3r4_iffirst_freeze_v1.md の M-ISO-8 行は「mutant TRUE と real UNKNOWN の verdict mismatch で kill」と読めるが、cert v2.1 の正しい機構は、両 verdict がともに UNKNOWN(NONSHADOW_IN_DATUM) で**verdict は不感**、real detail settled=false と mutant detail true の比較で kill、である。CV-9 v2 と cert v2.1 に合わせた versioned erratum が要る。

発火用 cert schema/manifest も、上の exact universe と IF-FIRST を参照する版として物理化してから freeze せよ。従って **v4 freeze、S1–S3.5、候補/kill/EMPTY 使用を今回は認めない**。S9 は当然別 gate のままである。

### F105-3.3　AUTO-SETTLED の数学

次の限定定理は正しい。

- PIGEON: induced map が well-defined で有限 quotient 上全射なら全単射。
- DESCENT-c / OP-SETTLED: descent・SURJ・有限性という三前件の下で settled。
- VERBAL-ISO: \(N_{F_2}\) が verbal（従って fully invariant）で \(c\in N\) なら全 shadow が descent し、isolated。

従って HS の \(N=\mathcal V(F_2)\times\langle c\rangle\) と Heisenberg の \(N_0\) は、その verbal 前件を満たす範囲で機械計算なしに isolated としてよい。GEN-AB の「charming の生成判定が abelian 成分しか識別しない」という射程も受理する。

一方、「無条件 AUTO-SETTLED は**偽**」までは本束から出ない。descent が hexagon+SURJ から導かれないことは、提案された証明が成立しないことを示すが、反例の存在証明ではない。Thm 3.10 の groupoid が非自明だという一文も、実際に複数 object を与える source/counterexample を伴っていない。正しい札は

~~~text
AUTO-SETTLED = NOT PROVED / generally unsupported;
conditional OP-SETTLED and VERBAL-ISO = paper theorem
~~~

である。真の non-isolated shadow が得られた時点で初めて false に上げられる。

AS-GAP-6 は、S1 解禁後に twin \(K\ne N\) または non-verbal \(N_{F_2}\) を掘る**副産物探索**として承認する。ただし S1 の完了条件にはせず、見つからなければ UNKNOWN のままにする。h11-fail は shadow でなく、M-ISO-2 は NONSHADOW_IN_DATUM/UNKNOWN fixture である。W-5 は引き続き UNKNOWN。

### F105-3.4　R3/R4 の格

cert v2.1 と Python 出力について、五つの conventions_used key は機械 diff 5/5、grading prohibition も byte 一致した。三 datum 上の五量と h10 の per-\((f,m)\) 会計も一致する。従って申告どおり

~~~text
cross-checked
scope = 5 quantities x 3 data;
tier = tool-calibration;
same-object judgment = source-reading;
numeric agreement does not establish convention identity;
no isolated=FALSE claim
~~~

の限定格を認める。M-ISO-8 の kill は detail-level に限る。Python output が assertion success 時にしか生成されず input digest も持たない点は正直に残っており、将来の receipt 強化事項である。この限定 cross-check は BU freeze や W-5 の PROVEN 化を単独では与えない。

## 4. 探索類型の standing authorization

制度の方向は承認する。凍結済みの候補生成器について毎回同じ数学ゲートを繰り返す必要はない。ただし提案の三点だけでは「同じクラス」の同一性が弱いので、class freeze は最低限次を一つの immutable class ID に束縛せよ。

1. predicate/driver/wrapper/schema/checker/source-map/fixture と各 digest。
2. exact candidate universe、semantic key bijection、許される parameter range。
3. STOP/UNKNOWN、timeout、shard join、重複/欠落規則。
4. output exposure/blinding、negative result 登録、artifact capacity/retention/resource cap。
5. preflight receipt schema と class calibration receipt。

個別 run は class ID と parameter manifest を先に発行し、parameter が登録 range 内で preflight PASS なら事前 gate を省略してよい。全 receipt は事後監査へ回す。次なら再 gate とする。

- 上記 digest/schema/source-map/universe/semantic key/STOP 規則の変更。
- 登録 range 外への拡張、容量 cap の超過。
- 封印隣接量、S9、または claim grade の昇格。
- checker が受け取れない新しい UNKNOWN/出力型。

これは候補生成の認可であり、候補を定理・非存在・verified へ上げる認可ではない。§2 HS と §3 BU はそれぞれ runnable class/freeze が未成立なので、今回の第一適用候補としては**不認可**である。

## 5. EP 第四陣と B NOTE

### F105-5.1　conventions ledger v1.7-r3

F104 の穴は閉じた。各 required item が status+evidence を持ち、aggregate は per-item から機械再計算し、優先順位 differs > UNKNOWN > matches、未知 kind は UNKNOWN、申告 aggregate 不一致は integrity STOP となる。**DRAFT 設計として PASS**する。

未決二点は次で裁定する。

- kind 語彙は ledger 本文へ自由記述せず、**versioned kind registry artifact** に置き、その digest を ledger/cert が pin する。未知 kind を UNKNOWN に倒す open-world 規則は維持する。
- checker が保証するのは registry membership、evidence path/hash、必須 field、aggregate 再計算まで。source_value と workshop_value の意味的一致は、kind-specific evaluator が別途登録されない限り人手監査であり、「機械照合済み」と書かない。

live 正本 v1.6、D3 越え禁止、CL-13 未発効は維持する。registry/schema/checker/両縁 fixture の実物を次 gate へ出して初めて ratify できる。

### F105-5.2　IMAGE-MU v3

resultant 修理は正しい。

\[
H(X,T)=(T-a(X))^2-p(X)^2f_6(X),\qquad
R(T)=\operatorname{Res}_X(q_x(X),H(X,T))\in\mathbf Q[T]
\]

を候補多項式とし、squarefree/factorization 後、固定実埋込みと \(x,y,\mu\) を結ぶ isolating data で一意な既約因子を選ぶ。\(R\) 自体を最小多項式と呼ばず、一意選択失敗を UNKNOWN とする。無限遠二枝は \(\operatorname{lc}(f_6)>0\) が当該実埋込みで確認できる場合に限り、そうでなければ UNKNOWN とする。これで F104 の数学 blocker は閉じる。

設計選択は次を採る。

- **route B**: receiver-held versioned model registry。係数体、\(a,p,f_6,C\)、map、chart/transition、実埋込み・root order を exact に持ち、whole-artifact digest で参照する。
- **(2a)**: IMAGE-MU v1 の事前登録宇宙を \(e=2\) に限定し、外は UNKNOWN。一般 \(e\) は新しい v2 universe として別 gate にする。

従って spec v21 / contract v16 / manifest v16 / schema / selfaudit v13 と両 route fixture を**起草・実装する scope**は再開してよい。ただし現草案だけから IMAGE-MU を発火せず、実 artifact の差分 gate を通すこと。IMAGE-MU=UNKNOWN / W6_CLOSED=false / W-6=OPEN / EP=uncalibrated は不動である。

### F105-5.3　suitelog v2 と B NOTE

suitelog v2 は前便の条件付き PASS を維持する。11 section、CI/local provenance 分離、UTF-8/exit/digest/META-1/未知形式の両縁、S-1→S-2→S-3 の順序は妥当である。登録 wrapper と新 log/抽出/receipt を実装してよいが、S-3 と negative fixture を再監査するまで「1210」を恒久札にせず、EP 較正とも呼ばない。

B の非 blocking NOTE は採用する。次版 manifest で external manifest と generator の digest を pin し、effective source chain を一意な node/edge 列へ正規化せよ。宣言だけでは既存 artifact の格を変えない。

## 6. Lean 第 1 波と Luna 初回指示

### F105-6.1　ビルド事実と限定受領

指定 commit c542808788053d4ca685f4992b07dacff35e742f の lean/ を local plain Lean で

~~~text
lake build P1
~~~

し、exit 0 を確認した。Mathlib は local import していない。

AxiomCheck.lean が列挙する次の exact Lean propositions は kernel check を通る。

~~~text
X_pow_2n, X_pow_lt_2n_ne,
epow_fst, epow_snd, epow_thd,
dpow_rot_flag, dpow_rot_val, dpow_refl_even, dpow_refl_odd,
Gn_X_eq_a1_q1, Gn_X_sq, Gn_ord_X
~~~

出力上、前半の商構成は Lean core の propext/Quot.sound のみ、Gn_X_eq_a1_q1 は追加 axiom なしである。(3.49) の T2_composition_identity と chiTilde_welldefined も実際には証明本文を持つ。しかし後二本は AxiomCheck の exact inventory に入っていないため、現 receipt の「全量」主張には含めない。

### F105-6.2　paper fidelity blocker

第 1 波を「sorry-free 6 命題+補助 7」「verified-modulo-axioms」として受理することはできない。

1. build warning は BlockA.lean の INN_on_Y、inn_fixes_X と BlockE.lean の chiTilde_isUnit、計 **3 sorry** を示す。
2. Gn_card_placeholder : True は \(|G_n|=4n^3\) ではない。
3. Lambda_simplyTransitive ... : True は仮定 hH,hstab を使わず、LA-6 の形式化ではない。unused argument warning も出る。
4. ShadowAxioms の四本 T2_thm43_explicit_isolated (n) : Prop、T2_thm43_isolated (n) : Prop、T2_15_Ih_decomp : Prop、T2_composition_hom : Prop は内容を型に一字も持たない。任意の Prop 公理は原典の exact theorem、最弱形、sanity instance を束縛せず、将来どの結論にも接続できない placeholder である。未使用でも policy v1.6 の gate を満たさない。
5. AxiomCheck.lean は 12 宣言への目視 #print axioms に留まり、全主定理 inventory、unexpected axiom/sorryAx の自動 fail、exact sorted per-theorem set、生成 AXIOMS/type digest receipt を持たない。
6. \(E_n=D_n^3\) は ambient type であり、\(G_n=\ker(\mathrm{par})\) の subtype/group/cardinality を実装していない。ambient 内での \(X\) の位数証明は正しくても、Gn.structure 全体や \(|G_n|\) は出ない。

従って exact に列挙した小補題だけを限定受領し、Block A/E と axiom policy 遵守を含む第 1 波全体は **FAIL / 差戻し**とする。「ファイル全体 verified-modulo-axioms」の header は撤回せよ。

### F105-6.3　割付表への裁定

1. 抽象補題で \(\forall\) 構造に対して置く antecedent は通常の theorem hypothesis であり T3 公理ではない。未証明の全域的予想を assumption に埋め込まない限り、Block H は着工可。
2. Bridge B は concrete finite-étale scheme/tangential basepoint 層が欠けるので defer を維持する。Mathlib の抽象 Galois category/affine algebra inventory があることと、橋が実装可能であることは同じでない。
3. T2 は Sol が PDF 画像で exact statement/domain/codomain/奇数条件/GT・Ih 構造を監査した後にだけ宣言する。裸の Prop は宣言にも import にも使わない。

Mathlib 調査については、公式 documentation の [IsCyclotomicExtension.Rat.ramificationIdxIn_eq](https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/NumberField/Cyclotomic/Ideal.html) が \(n=p^{k+1}m\) に対し \(e=p^k(p-1)\) を与えることを確認できる。\(p=2,k=1,m=n\)（\(n\) 奇）で \(e=2\) となるので T1_cyclotomic_ram2 は pinned Mathlib package 上で消せる見込みが高い。ただし GHA で接続補題まで build した receipt が出るまでは「closed」としない。調査の negative claim は version-relative UNKNOWN と読む。

### F105-6.4　Luna への初回指示（この裁定を実装仕様とする）

**目的:** paper proposition と Lean proposition の fidelity を先に回復し、Block-H-first で公理境界を縮める。

1. local は plain Lean のみ。Mathlib import・恒常 build はしない。Mathlib 依存層は別 package と GHA job に隔離し、CI 実行・log 還流は工房が担う。
2. 四つの bare-Prop T2 axiom を import 経路から quarantine する。正確な型が Sol 監査を通るまで使用禁止。: True placeholder も theorem inventory から除外し、real statement+proof または明示 OPEN にする。
3. sorryAx と許可外 axiom を自動 fail する checker を作る。exact theorem inventory、各 theorem の exact sorted axiom set、正規化した declaration type digest、生成 AXIOMS manifest を receipt に出す。目視 grep を判定器にしない。
4. **Block H first**: TORS-U/B-6\(^{\rm tw}\)-lf を、巡回群全体上の二忠実作用と conjugation-induced automorphism という正確な型で形式化する。local plain Lean で explicit cyclic model に落とせる核を先に閉じ、一般 finite cyclic group API が Mathlib を要する部分だけ GHA package へ分ける。character image から \(b\) を fitting してはならない。
5. 並行して Block A の土台を修理する。実 Gn subtype、group closure/laws、\(X\in G_n\)、cardinality、実 Λ type と simply transitive statement を実装する。ambient \(E_n\) の位数補題を Gn の結論と混同しない。
6. Block E は chiTilde_welldefined と (3.49) を exact inventory に追加し、chiTilde_isUnit の sorry を閉じるまで file-level grade を付けない。
7. T2 statement 案はコード化前に、原典 theorem/page、全 hypothesis、最弱結論、sanity instance を一枚表で Sol へ返す。承認前に axiom を増やさない。
8. 納品は local plain build log、GHA Mathlib build log（該当時）、generated axiom manifest、per-theorem receipt、paper↔Lean statement 対応表。旧ファイルを上書きせず versioned にする。

最初の実装順は **axiom/checker hygiene → Block H TORS-U → Block A foundations → Block E** とする。Bridge B と T2 使用は前二つの gate の後である。

## 7. 共有・権限境界

本便添付の宣言どおり、提出 evidence には HS 本走、BOTTOM-UP 掘削/kill、\(d_N\)、\(\operatorname{Im}R\)、封印量への接触は見当たらない。CF/CONV/ISO は登録 fixture/tool-calibration の範囲である。監査側で行った実行は local plain Lean の lake build P1 と SGA 1 のページ画像照合だけで、705,894 宇宙や探索候補には触れていない。

最終状態遷移をまとめる。

- P1: **Route T の一様 \((5'^b)\) による FAM-U-ASM を限定昇格**。B-4c\(^{\rm u}\) の依存記帳と claim text 修理が発効条件。exact \((5')\) の旧 proof ID と link inventory は別に保存。
- HS: **本走/較正 shard 不認可**。registered fixtures と実装完成のみ可。
- BU: **freeze なし、S1–S3.5 なし、S9 なし**。R3/R4 の限定 cross-checked 格のみ採用。W-5 UNKNOWN。
- Standing authorization: **制度を条件付き採択**、現二クラスへの適用なし。
- EP: **設計・実装準備のみ**。三状態札不動。
- Lean: exact 小補題のみ限定受領、**第 1 波は差戻し**。上記 Luna 指示で再着工。
- 統計は exploration-heuristic のまま。予言 (iii) は未採点。

以上を便 105 の裁定とする。
