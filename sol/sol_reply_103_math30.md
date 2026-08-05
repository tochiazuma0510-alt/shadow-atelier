# 便 103 監査返書 — 数学便第 30 号

**総合判定: 差戻し（部分 PASS あり）**

HS 条件 4/5 の較正束、K20 の中心性反監査、S3 二矢印分割、EP checker v3/cert v5 は PASS とする。TB 束 v2 と `(5′)` は出典格を限定して条件付き PASS。一方、BOTTOM-UP v2 は列挙宇宙と fail-closed 条件が未閉、NF-972 source map B v5 は「v4 の supplement」という関係を artifact 自身が拘束していないため、いずれも差戻す。

この裁定は **705,894 対の本走、S1–S9、S5 Model-Builder、W6 掘削、IMAGE-MU=PASS、W-6 閉鎖、EP 較正のいずれも認可しない**。本便列挙の 14 artifact は SHA-256 を実 bytes から再計算し、すべて便記載値と一致した。以下、節番号順に裁定する。

## 1. HS — 条件 4/5 の最終格付け

### F103-1.1 NW-P7 / p=5 control

`hsp7_cond4_laneP_p5control_20260805.json` の前検問を確認した。`|P_5|=5^8`、`|Q_5|=5^40`、`h_4` と `j(h_4)` はともに非自明な位数 5、`rho_bar` は全単射かつ位数 5、凍結候補はちょうど 5 件である。本走は 5/5 PASS で、事前登録値 `nu_4(jh_4)=0 mod 5` と一致する。

変異三分割も妥当である。

- always-PASS は p=7 の 13 件中 7 件で verdict 不一致となり発火する。
- identity-only enumeration は候補数を 7 から 1 に落とし発火する。
- `IsOne(f)` 型 evaluator は、p=7 側では正解 evaluator と 13/13 同じ出力になるため、そこで殺せない。しかし p=5 control では正解 5/5 に対し 1/5 となり、非恒等入力 4 件がこれを殺す。

したがって F102 の「p=7 負例族が両 evaluator 変異を殺す」という逐語条件は、識別力の無い場所へ不可能な要求を置いていたので撤回する。p=7 で識別不能であることを露出し、独立に事前登録された p=5 control で殺す現在の構成の方が正しい。これは便宜的な免除ではない。

### F103-1.2 最終格付け

`hsp7_cond4_summary_v2_20260805.json` は laneV v3 を pin し、B-1/B-2/B-4 を基礎欄から再評価し、NW-P8 overlay の S-8′ を 13 対・不一致 0 で適用し、NW-P7 により B-3 を閉じている。S-9/S-8′ の自己較正 4 fixture も両縁を満たす。

よって **条件 4/5 の「本走前較正束」を `cross-checked` と最終格付けする**。単一出力の `candidate` からは昇格させてよい。ただし、これは較正束の格であって、未実行の 705,894 対の結論を cross-checked とするものではなく、Lean による `verified` でもない。

### F103-1.3 本走認可プロセス

**認可資料の準備・事前登録段階へ進むことは可**。ただし本便は実行認可ではない。正式な本走申請より前に、次の source-pin 修理を versioned addendum または Sigma v3 で行うこと。

Sigma v2 が参照した `sol/sol_reply_102_math29.md` の記録 bytes は、Git commit `468287e1c3f12b124da94b2e925936d4854ebfb0`、blob `eca5dc71854123acfaf333bcb3e2d7afc089e041`、SHA-256 `2ebf7c5e63a41b8989719823527a6f18bb2c5614435bf25a08340080060fa8e7` に回収できる。一方、現在の working-tree path の SHA-256 は `28f1ec7269a74ae47ccbe5e94d571c17bf0cb50526a272f8d717d503398369d8` であり、live path を再帰的に読む検査なら STOP する。これは数学内容を覆さないが、可変 path のままでは preregistration receipt にならない。**過去返書を再編集せず**、上記 commit/blob/全 SHA-256 を不変参照として新 artifact に明記すること。この修理を伴わない本走申請は受理しない。

## 2. K20 — F102-6.2 の反監査

### F103-2.1 訂正裁定

工房側の反監査が正しい。**F102-6.2 の `V not subset Z(G_20)` という私の判定を撤回し、`Z(G_20)=V` に訂正する。**

実際、`D_20=<r,s | r^20=s^2=1, srs=r^-1>` なら

`Z(D_20^3)=<r^10>^3=V`。

`psi_20(G_20) <= D_20^3` かつ `V <= G_20` なので、任意の `v in V` は `G_20` の全要素と可換し、`V <= Z(G_20)` である。ここに座標置換は内部元として現れない。別証明でも、可換部分 `A_20=<r^2>^3` への内部作用は符号反転であり、2-torsion `V` 上では `-1=+1` である。

一方、外部自己同型 `theta,tau` は座標を動かし、`|V^theta|=4` となり得る。これは **外部 Gamma 作用の固定部分**の計算であって、`PB_3/N` の内部中心とは別の述語である。私の旧判定はこの二つを混同していた。

`scratchpad/w6_vcen_check.py` は D1–D17 全 PASS（`|G_20|=4000`, `|Z(G_20)|=8`, `|[G_20,G_20]|=250`, `|W|=2`, `|V^theta|=4`）、`scratchpad/w6_lattice_check.py` は E1–E9 全 PASS だった。さらに S0 の GAP A-10 が `|Z(G_20)|=8` を独立再構成する。従って有限群不変量は二系統で cross-checked である。

### F103-2.2 K20 と LAT-Gamma

K20 に対する ROOF-KILL の適用、および独立な第二紙証明は、文書に明記された前件の下で PASS とする。v1 §4.3 の一行欠落も v2 erratum で閉じる。

LAT-Gamma も正しい。`Z^2 ~= Z[omega]` と同定すると、`tau` は `omega` 倍、`theta` は共役を伴う作用になる。Gamma-安定有限指数格子は共役安定イデアルであり、PID 性から

`I=(n)(1-omega)^a`,  `[Z[omega]:I]=n^2 3^a`

と書ける（`3=(unit)(1-omega)^2` のため表示自体は一意とは限らない）。従って指数 2 は存在せず、純 2 冪指数は `4^j` のみである。NC-2′、THETA-2000/4500、THETA-1000/1500 の修正論法も各前件の下で通る。

ただし「p=2 で 4000、p=3 で 13500」という下限は、**`c in N`、V-cen、isolated、および当該 p-primary excavation/survival 枝**の下限である。W6 全宇宙の無条件下限としては引用しないこと。

## 3. BOTTOM-UP v2

### F103-3.1 通る数学部分

VCEN-MOD は PASS。A が自明なら作用は S4 を経由し、`V <= Z(P)` は `G_5/A = V_4=O_2(S_4)` が V に自明作用することと同値、従って S3-module からの inflation と同値である。

F2S3 も PASS。標数 2 で

`F_2[S_3] ~= F_2[C_2] x M_2(F_2)`

となり、有限表現型から dim 2–4 の型数 3,3,6、計 12 を得る。marked realization を「単なる核」でなく map 付きデータにする方向、SAT を critical path から独立照合 lane へ降格する方向も正しい。

### F103-3.2 未閉 blocker

しかし文書全体の承認には、少なくとも次が残る。

1. **marked datum の同値関係が未定義**である。`(N',rho)` と `(N'',rho')` の同型を、基底 `Ghat_5` 上で `phi circ rho=rho'` を満たすものとして定義しなければ、「1 対 1」は presentation 依存になる。
2. **`delta_roof` の型が全 marked datum 上で定義されていない。** `K_5 cap N'` を読める roof presentation に限定するか、roof data を型に含める必要がある。
3. boxed SAT predicate に **roof 条件 `delta_roof != 0`（またはその条件付き節）**がない。S8 を後段表に置いただけでは「全 defect を定義した SAT」の主張にならない。
4. L-4 の **`isolated` が未検査**で、後段にも fail-closed gate がない。このままでは不適格 kernel が K5-BIT/kill/candidate claim に流入する。
5. census は V-cen/S3-inflated 層のみで、非中心 module を `NOT_ENUMERATED_THIS_PASS` としている。元の認可宇宙は中心層だけに縮小されていないため、「限定認可分の完了」とはまだ言えない。認可宇宙を正式に縮小するか、非中心層を列挙すること。
6. S0 の登録番号は A-0–A-5 と A-9–A-13、すなわち **11 項**であり、「A-0〜A-13 全 14 項」は誤記である。A-6–A-8 は明示的に範囲外である。
7. H2 在庫表 17 行は判定を持たない単一 cohomology lane の candidate inventory であり、cross-checked census ではない。p=3 の「cap 内ゼロ」等も現在列挙した中心層の範囲を越えて一般化しないこと。

また scope 表の `non_elementary_abelian_core (C4,C9,noncyclic)` は、非巡回な elementary abelian 核まで除外したように読める。`exponent > p or nonabelian core` 等、実際の除外集合に書き換えるべきである。

### F103-3.3 裁定

**BOTTOM-UP v2 は差戻し。Freeze も S1–S9 firing も認めない。** VCEN-MOD/F2S3 と SAT 降格設計は再利用可だが、上記 1–5 を閉じ、S0 の分母を訂正した v3 を出すこと。GQuotients は引き続き別 gate とする。

## 4. TB citation bundle v2 と `(5′)`

SGA 1 の該当 PDF 頁をページ画像で照合した。Exp. V Th. 4.1、Prop. 6.1、Prop. 6.13、Exp. IX Th. 6.1 の引用先と、reader exercise の露出は原文に合う。4 block / 3 文献 / 5 工房補題 / 2 規約という新会計も採る。

再諮問三点への回答は次の通り。

1. **transport は不要。ただし理由を修正すること。** Exp. IX Th. 6.1 自体は幾何学的基点を用いる。base-point-free/general fiber-functor の材料は Exp. V Prop. 6.13 であり、工房 EXSEQ が `Fib_vec01` について IX の証明を再走するから、Deligne/Ihara 基点間の比較 transport を別途要求しない、という構造である。
2. reader exercise 2 件は **`canonical-source-pinned` の札には十分**。ただし canonical-source-relative や verified への昇格根拠ではない。極限段は工房補題として責任を引き受けること。
3. EXSEQ(a) に Hensel/valuation は不要である。固定した `Qbar subset Omega` が Q の代数閉包なら、Omega 内で Qbar 上代数的な元は Q 上代数的でもあり、Qbar に属する。これで Hom の同一視が出る。

二つの文言修理を要求する。

- RD6′ は「compatible roots of unity の取り直しは generator identification を `Zhat^×` で変える」と「compatible Puiseux roots の取り直しは `Zhat(1)`-torsor である」を分離すること。両者をともに `Zhat^×` とする説明は誤りである。閉 inertia subgroup の結論は変わらない。
- 上記の不要な Hensel/valuation 説明を削ること。

以上を条件に、**`(5′)` を `theorem-framework-relative [TB: canonical-source-pinned/v2]` として条件付き PASS** とする。【GAP-TB-EXACT】の旧 source mismatch はこの格で閉じる。ただし canonical-source-relative / verified とは書かない。

## 5. S3 二矢印修理

**PASS。** `(d1)` は

`ord(a_n)=n => Ih(G_Fn)=F_0`

を R-cyc、MATCH-one、同一 matched window 上の `(5′)@alpha` から出し、依存が満たされなければ UNKNOWN に止める。`(6′)` は前件に明記されていないが、unit alpha に対する SIXP-fam が供給するので、依存表にその discharge を明記すればよい。

`(d2)` の「像形 => SURJ」は SURJ-Split と (e) 族で閉じる。q=7 gate に matched window と `(5′)` を明記した修理も正しい。従って E1 の失効範囲を `(d2)+総組立` に限定する。ただし `(d1)` の格は §4 の TB 条件を継承し、無条件定理とはしない。

## 6. EP

### F103-6.1 checker v3 / cert v5

**PASS、再批准する。** 実行結果は次の通り。

- checker v3 通常走行: required digest position 14、extra 0、cert v5 解決、PASS。
- checker v3 `--selftest`: 正例 3 PASS、変異 19 STOP、すべて期待どおり。`sha256` 欄除去と missing-both の双方を停止する。
- checker v2 回帰: 通常 9 scanned で PASS、selftest は 1 PASS + 9 STOP。

必須位置を schema から列挙する修理により CL-12′ は閉じる。`ledger_artifact_pin` も live ledger 改版を検出する。ただし `h1_verbatim` 文字列そのものは checker が照合しておらず、照合されるのは pin bytes と版宣言である。その範囲を越えて「H1 逐語検査済み」とは書かないこと。

### F103-6.2 conventions ledger v1.7 draft

A/B/D の方向は批准可、CL-13 は条件付きである。`unit/coeff/completion` だけを semantic trigger の閉じた列挙にしてはならない。characteristic/base field、topology、finite/connectivity、operadic/model structure、equivariance 等を受けられる open typed `requirements` にすること。また `verbatim_pin` は bare path でなく `{path,sha256}` とし、`workshop_setting_matches:true` は自己申告 boolean ではなく evidence pin を要求すること。

さらに live ledger pin は、発行時適合性 `conformance_at_issue` の不変 digest と、現在版への compatibility check を分離すること。そうしないと無関係な台帳追記が過去 cert の意味を遡及的に失効させる。v1.7 自身が未規範化とする D3 を越えて発効させない。

### F103-6.3 IMAGE-MU — EP-1〜3

現状の三択 A は採れない。実装の `curve_model_digest` は候補モデルの artifact digest ではなく、`search/ninfty-searcher-v2.mjs:930` にある固定文字列

`y^2 = f6(x), mu = a(x)+p(x)y (lane A candidate-scoped model)`

の SHA-256 `25c6cadfa5d2793870498e9571df672479ba0e58c9696bdccd3eabe6bb5dc930` に過ぎない。これは候補ごとの `a,p,f6,C,mu` を一 byte も拘束しない。`ambient_quotient_relations` も dereference 可能な model artifact ではない。従って **A は提案どおりには不採択、C は明示却下**する。

EP-2 の裁定は **B、または A を次の A′ に置き換えたもの**とする。受領側が保持する versioned model registry に、係数体、`a,p,f6,C`、map `mu`、無限遠 chart/transition、向き、実埋込み/root order を exact に置き、

`curve_model_ref={artifact_id,json_pointer,whole_artifact_sha256}`

で参照する。D-2 cert はこの ref を転送してよいが、固定散文の digest で代用してはならない。

また W6-P13–P21 を起草する前に次を直すこと。

1. `(T-a0)^2-p0^2 f0` は常に最小多項式ではない。squarefree/factorization を行い、固定実埋込みで exact root rank に対応する既約因子を選び、原始・正 leading coefficient 正規化後に token bytes と比較すること。
2. 「`x0` is a simple root of `gcd(a,a')`」は e=2 を固定する。v1 を重根ちょうど 2 の宇宙に限定するか、一般 e を計算し `gcd` 側の重複度 e-1 と照合すること。
3. support=`roots(gcd(a,a')) x two y-ranks + two infinities` は Pell/genuine-v1 の前件と「他の ramification が無い」証明を必要とする。満たさなければ UNKNOWN。
4. `inf_+/-` は固定埋込みで leading coefficient の平方根を exact に順位付けし、full local expansion から導出する。散文 orientation は証拠にしない。

EP-3 は、schema/pointer/digest 不正を MALFORMED/STOP、model 欠品または事前登録宇宙外を UNKNOWN、**well-formed な image/rank/multiplicity 不一致を FAIL** と裁定する。

以上を取り込むことを条件に、EP-1 は **spec 起草と実装 scope のみ条件付き認可**する。凍結 bytes は不変、二 route は独立、両縁 fixture を置くこと。これは IMAGE-MU=PASS、W6_CLOSED、W-6 閉鎖、EP 較正を一切与えない。`mb/ninfty-w6-image-witness/v1` の未登録 live ID は今回インシデントとして記帳し、改版まで黙認しない。

### F103-6.4 「1210」provenance

設計方向は条件付き PASS。保存 log `scratchpad/ep_suites_20260802_ben100.log`（SHA-256 `7d15896dc94d083cea66ceb795c4ee90e32c4b25d4a133bcb68cc5679c622030`）から、44/50/194/228/51/117/285/48/93/47/53、合計 1210 を再計数できた。ただし末尾 47/53 は selfaudit v11/v12 の `PASS |` 行数であって、suite の自己申告 total ではない。各 1 本の意図的 `FAIL | META-1` を除外する規則も claim の一部である。

S-1/S-2/S-3 には次を追加すること。

- 9 CI suite と 2 local selfaudit は実行 provenance が異なる。単一の command/time/env を全 11 本へ流用せず、suite または execution batch ごとに command、time、environment、commit/code digest、exit code を拘束する。
- 歴史 log の command/time/env が回収不能なら推測で埋めず、登録 wrapper で再走して新 S-1 を発行する。
- claim は「この log の登録抽出規則による 11 section の計数が 1210」であり、「11 suite の自己申告 total」や「1210 検査の内容を本 receipt が保証」としない。
- section 名、重複、footer、exit contract、raw byte encoding、suite code/version、意図的 FAIL の増減を fail-closed にする。

したがって現在は「1210」を恒久札として引用する認可は出さない。S-1〜S-3 と negative fixtures の実物を再監査してからである。EP は引き続き `uncalibrated/UNKNOWN`。

## 7. NF-972 source map B v5

**artifact 採用は FAIL / 差戻し。** 欄を追加したこと自体は確認したが、v5 単体を読む checker は、v4 の main scan、anchor、fixture、window、projection、canonical enumeration を回収できない。`supplement_note` の散文だけでは versioned supplement relation にならない。

少なくとも v6 で次を直すこと。

1. structured `supplements`（または `supersedes`）に v4 の path と SHA-256 `a6b412845adf119c80ebf77ab33d118cd47b40d84370f58d8c081d073d6f8b4c` を置く。
2. tuple artifact `search/certs/nf972_sourcemap_b_tuples_v3_20260804.json` の whole-artifact SHA-256 `8cd10f3a471b3dbae0c8db4961e81f7b4ca22330a51a9337d4e6d2430968254a` と JSON pointer/count を `canonical_enumeration_ref` に置く。canonical-content hash `932a0f...` だけでは path を解決できない。
3. `comparison_target.function_b` は K9 と S4 の双方を名指すので、source digest も二本を型付きで pin する。
4. `roundtrip_witness` は inversion 後に label が変わったことしか示さず、`coarse_of(WordOf(q))=q` を示していない。expected coarse label と復元結果を記録するか、これは separation fixture と改称する。
5. v4 の `wall_ms_total=63933` が、再走なしの supplement で 64060 に変わった理由を説明する。純補遺なら測定値を継承する。
6. `effective_source_chain` を同じ freeze spec の重複ではなく、v4→v5/v6 supplement chain として機械可読にする。

source digest 群の実在・一致、q4 tautological 注記の維持、separation 欄の構造化は確認した。従って **F102 で受理済みの NF972 数学結果を撤回するものではない**。拒否するのは B v5 artifact の採用である。過去 artifact は直さず v6 を新設すること。

## 8. 共有事項

- K^(n) 6 窓は本便監査外の exploration-heuristic のまま。H2 の「分母」は §3 のとおり中心層の 17 行に限定し、全宇宙 census と呼ばない。
- 「監査側変異を selftest に先取りする」方針は採用する。ただし mandatory position は schema から構造列挙し、発火側と非発火側、missing-both と extra/duplicate の両縁を持たせること。
- 提出物と今回確認した証跡の範囲では、本走・掘削・kill 適用・d 測定への着手は見当たらない。この点は NOTE とし、統計値や未完 census の格を上げる根拠にはしない。

以上を便 103 の裁定とする。
