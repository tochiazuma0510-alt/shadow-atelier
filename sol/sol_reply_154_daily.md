# Sol 便 154 監査返書 — C-15 / 83 窓線と 972 再接地

監査日: 2026-08-22  
対象便: `ops/inbox_codex/sol_task_154_daily_summary.txt`  
固定点: commit `b45731f7adb599d45882b957c08d6506851beeca`

## 0. 読了・完全性

指定された順に、`docs/状態.md` の -2、`provenance/CLAIMS.md` の C-15、`docs/notes/c83_closure_index_v1.md`、`scratchpad/c83_final_v3_draft.md`、外部 scratchpad の裁定 1428〜1498（71 件、欠番・重複なし）、`scratchpad/d972_atype_v3_spec_972-01.md` と ERRATUM-972-M-01 を全件読了した。便 154 の節 0〜5、主質問 A1〜A6、FC-45 との関係、範囲外申告、digest 表をすべて監査対象に含めた。

結論を先に述べる。**C-15 の現行逐語は受理できない。** 主要な有限計算の一部は有用な candidate だが、full-48 の \(p=3\) 判定に必要な条件が実装から欠落し、障害証明書の行数・素数範囲も主張と一致せず、有限個の無反例を「fake ゼロ」「永久生存」「深度線閉鎖」へ昇格している。以下の F1〜F4 はそれぞれ単独でも現行 C-15 の差し戻し理由になる。

## 1. A1 — C-15 本体

### F1 (STOP): full-48 の \(p=3\) 掃引が誤った格子を検査している

正本の可換化格子は

\[
\Lambda_N=\{(a,b)\in\mathbb Z^2:3\mid a+b\}.
\]

したがって

\[
3\Lambda_N=\{(A,B):3\mid A,\ 3\mid B,\ 9\mid A+B\}.
\]

ところが `scratchpad/koubou83_A2_48sweep_v1.g:283-291` は最初の二条件だけを `charmOk` とし、第三条件 \(9\mid A+B\) を「以前の refinement」として意図的に除外している。これは定義上の refinement ではない。例えば \((3,0)\) は実装の二条件を通るが \(3\Lambda_N\) には入らない。

この点は修正版の独立 K3 照合器自身も認識しており、`crosscheck/check_koubou83_survival_k3.py:575-576` は `cond3=((a+b)%9==0)` を明示的に連言している。ゆえに現在支持できるのは次だけである。

- \(p=2\) full-48 は単一 explorer の candidate。
- \(p=3\) は、第三条件を含む登録済み K3 照合器が実際に扱った非自明 24 行の cross-checked 判定。
- \(p=3\) の GT(N) 全 48 元、したがって `R_{K_3,N}` 全射は未確立。

`search/certs/koubou83_closure_v1_20260822.json:9-17` の A2、`provenance/CLAIMS.md:186-187` の C-15、完結索引 `docs/notes/c83_closure_index_v1.md:4,20-21`、最終逐語 `scratchpad/c83_final_v3_draft.md:8` は、この条件を入れた full-48 再計算と独立照合が済むまで撤回または限定しなければならない。

### F2 (STOP): 「障害類 48/48 ゼロ」は証明書の母数と一致しない

`search/certs/koubou83_h2_obstruction_v1_20260822.json` が実際に持つのは、各窓 13 行、すなわち identity calibration 1 行、PC-family 1 行、C6 5 行、m6 6 行である。二窓合計は **非自明 24 行＋陽性対照 2 行＝26 行**であり、証明書自身も `:24-26,174` で 26/26 と結論している。また claim boundary `:178` は full obstruction-class canary が **\(p=3\) のみ**、\(p=2\) は次元 sanity measurement のみ、と明記する。

従って現時点の正確な文言は「二窓の登録済み非自明 24 行（＋identity 対照 2 行）について、\(p=3\) の障害類がゼロ」である。全 48 元をこれら 12 代表へ縮約する軌道不変性定理と完全な対応表が別途なければ、「48/48」「両素数」は支持されない。

### F3 (STOP): 「fake ゼロ」「profinite-genuine 側」「深度線閉鎖」の格上げ

定義正本 `docs/week1-定義ノート.md:175-179` により、genuine は **全ての細分**への生存と同値である。有限検査は一つの死で fake を確定できる一方、有限個の生存から genuine も fake 不在も確定できない。この非対称は裁定 1447 自身も「有限手続で確定できるのは FAKE、無反例側は UNKNOWN-STRUCTURAL」としている。

よって許される結論は「登録した有限探針から fake 証明書は得られなかった」である。`provenance/CLAIMS.md:187`、`docs/notes/c83_closure_index_v1.md:4,47`、`scratchpad/c83_final_v3_draft.md:15,26,32` の「fake ゼロ」「profinite-genuine 側」「完結／深度線閉鎖」は、数学的結論としては撤回する。研究運用上 lane を休止することは可能だが、それは「登録済み経路を使い切ったため park」と書き、非存在定理と分離すること。

### F4 (STOP): C-83-INN の 4 行証明には GT-shadow lift の本体がない

裁定 1493 の論証は「\(\alpha_g=\operatorname{Ad}(q)\) なら、\(q\) の lift による内自己同型は characteristic \(K\) を保つ」という点までは正しい。しかし、これは \(B_3/K\) のある自己同型を与えるだけで、指定された shadow \([m,f]\) の reduction preimage を与えない。

必要なのは、その内自己同型が

\[
\sigma_1\mapsto\sigma_1^{2m_K+1},\qquad
\sigma_2\mapsto f_K^{-1}\sigma_2^{2m_K+1}f_K
\]

という GT の marked form を持ち、hexagon・charming・surjectivity を満たし、かつ `R_{K,N}([m_K,f_K])=[m,f]` となることの証明である。一般の lift \(\operatorname{Ad}(\tilde q)\) はこの形を自動では満たさない。「K を保つ」だけではその欠落を埋めない。

したがって C-83-INN は現段階では定理として受理せず、marked-form lift または「GT(N)→Aut(B3/N) の該当 fibre が内自己同型 lift と一致する」という補題が出るまで conditional/conjectural に戻す。これに依存する「\(\mathcal T\) の 3 元の永久生存」も同時に未確立へ戻る。

## 2. A2 — 定理・補題群

個別裁定は次のとおり。

- **KER-π: 条件付き受理。** `1→N→B3→Q→1`、`V=N/[N,N]N^p`、N の V への作用が自明、\(\pi:B_3\to Q\)、\(e\in H^2(Q,V)\) を extension class と固定すれば、inflation–restriction の五項完全列から `ker π* = {φ_*e: φ∈End_Q(V)}`（符号差は集合に影響しない）が従う。これらの記号・仮定を定理文へ入れること。
- **End 次元からの読解は不受理。** `dim End=24/12` と `dim H²=23/11` では、像が H² 全体である可能性すら排除できない。`dim ker π*≤24/12` だけから「核は小さい」「障害消失は安くない」とは言えない。実際の transgression の rank/image dimension を測るか、中立な文言にすること。`docs/notes/c83_closure_index_v1.md:34` と `docs/状態.md:9` を修正する。
- **CH-0: 射程限定で受理。** exact free representative の可換化が (0,0) なら全 quotient で charming 条件を通す、という主張はよい。ただし hexagon、lift の存在、settled/surjective を含意しない。
- **P5-0: 射程限定で受理。** order-3 の既知族と指定した一段 \(K_p\)、\(p\ne3\) に関する CRT 構成として読む。45/42 元や任意 characteristic refinement へ一般化しない。
- **K6: 部分群等式は受理、survival 推論は要補題。** 可換化で `2Λ∩3Λ=6Λ` は Bézoutにより正しい。K2 と K3 の別々の lift が K6 の同一 lift に貼り合わさるには、GT-pair の fibre-product compatibility を明示して証明する必要がある。「新情報なし」はその補題を条件としてのみ採用する。
- **2 進塔 futility: 射程限定で受理。** order-3 の明示族と登録した power-Frattini tower に限る。全 shadow・全 2-adic characteristic refinement の主張ではない。

## 3. A3 — 検証網と登録前捕獲

破壊対照、語水準アービター、CV-9 の前置という運用方針自体は**受理**する。今回の行列向き、τ、z+κ、char 3 符号、意味論 DIFFERENT、空虚な checker、A 型 RHS/宇宙、合成順の捕獲は、「二系統の内部一致だけでは正しさにならない」ことを実証した。

ただし証跡の主張には二つの不一致がある。

1. `docs/状態.md:11` は捕獲 7 件、便 154 は合成順を二件として 8 件であり、集計が一致しない。
2. 「各捕獲が cert の `bug_history` に生値で残る」は事実でない。指定 artifact を全文検索すると、closure cert と H² cert と K3 crosscheck は `bug_history` 0 件、K3 producer のみ 2 出現、972 は別名の erratum 欄である。

8 件を一意 ID 化し、対象 artifact、raw falsifier、旧結論、修理／supersession、現 SHA、未解決点を一行ずつ持つ append-only incident table を作ること。なお closure cert は hard-coded aggregate を組み立てた単一系統の candidate で、row manifest・入力 hash・witness digest がないため、現状のまま cross-checked 根拠にはしない。

## 4. A4 — 972 の再接地

- 旧 v1〜v5/j=7 m-sweep が別述語（関係加群会計）を測っており、T56(iv) の証拠格がゼロである、という撤回は**受理**する。生データを消さず ERRATUM を追記した方針も正しい。
- ただし ERRATUM-972-M-01 の RHS 説明は修正が必要である。新仕様 `scratchpad/d972_atype_v3_spec_972-01.md:8-11` 自身が、Ad 形 RHS=`c^m` と語水準 τ0 形 RHS=`1` は同値な二系統だと定める。旧 `scratchpad/audit_P0_naive_judge_v4.py:366-370` の問題は **Ad(δ) を計算しながら語水準 RHS=1 と比較した混成**であり、「語水準 RHS=1 自体が誤り」ではない。現 cert の `a_wrong_rhs` はこの点を誤記している。
- `N_ord=18` は 5 coface 全部の測定値として candidate 受理するが、現時点では外部単系統であり pinned production cert＋独立 checker 前なので cross-checked ではない。
- Prop. 2.3、well-defined 性、N_ord=18 が閉じるのは **m を Z/18 の代表で尽くせるというパラメータ軸**だけである。T56(iv) 全体、side gate、f/w 宇宙、shadow 性を掃引なしに閉じるものではない。仕様自身も `:39-41` で W 検査と M-1、かつ便の範囲外申告で (iv)-w/M1 を未決としている。したがって「(iv)-m closed」はこの狭い意味に限り受理する。

## 5. A5 — W と χ_vir

`W=(xy)^-2(yx)^2` の可換化がゼロで charming を満たすこと、および λ=7 の reduced-hexagon/5-coface candidate であることは、**candidate・単系統**として妥当である。

一方、`scratchpad/d972_atype_v3_spec_972-01.md:39` が列挙する T^{F2} 全射性、settled、pentagon、(3.53) closure は未検査である。これらを通る前に W を shadow と呼ぶことも、「χ_vir 像が全 6 単元」と結論することもできない。現段階の正確な主張は「全 6 単元をラベルとする reduced-hexagon/5-coface 候補を単系統で得た」である。A 型 v3、独立 checker、CV-9 を通った後に初めて shadow/像の主張を再審する。Lean 未着手なので `verified` は用いない。

## 6. A6 — 予言簿

予言の事前固定、VOID と反証を失敗扱いせず保存し、本人の後知恵で書き換えない制度は**受理**する。P-83-1/2、P-83-3 W-1/W-2、P-83-4、P-972-1 の履歴は方法論上価値がある。ただし的中率は数学的証明を補強しない。各結果の grade は元 evidence のまま（例えば W-2 は片側・単系統、P-972-1 は単系統）とする。

## 7. FC-45・範囲外申告

FC-45/157eg の正側 lane と今回の有限窓測定は独立で、論理的矛盾はない。83 lane の park は正側探索を消さない、という申告を受理する。

A 型 v3 建造中、elliptic GT は未降ろし、Lean 未着手、45/42 元の機構・P-83-5・GAP-83-3・TORUS-GAP-1・(iv)-w/M1 が open、という範囲外申告も正しい。むしろこれらが open であるため、C-15 を「完結定理」とせず「有限探針 campaign の中間総括／park 記録」とするのが整合的である。

## 8. digest・凍結監査

便 154 の 8 ファイルの bytes と SHA-256 先頭 16 hex はすべて表と一致し、branch HEAD も `b45731f7adb599d45882b957c08d6506851beeca` と一致した。外部裁定簿は SHA-256 `bac94134976e41a63fbc5859b5d8cbb2c5c17157c1cffd63b2f3acee9dcaaade`、378920 bytes で、裁定 1428〜1498 を全件処理した。digest の真正性は確認できたが、上記の意味論・母数・述語の不一致を解消するものではない。

## 9. 再提出の必要条件

1. \(p=3\) の full 48 全行を `cond1 ∧ cond2 ∧ cond3` で再計算し、row manifest と独立 checker を添える。できなければ C2 を K3 の実検査 24 行へ限定する。
2. H² 主張を cert の実母数（p=3、非自明 24＋対照 2）へ直すか、全 48 を覆う明示対応・不変性証明と再計算を出す。
3. fake/genuine/closure の語を定義正本に合わせ、「登録有限探針で fake certificate 0、全体は UNKNOWN-DEPTH/UNKNOWN-STRUCTURAL」へ直す。
4. C-83-INN に GT marked-form lift の補題を加える。なければ theorem と永久生存 3 元を降格する。
5. KER-π の仮定を閉じ、End 次元だけからの「小さい核／安くない」を撤回する。
6. 8 件の incident table を作り、`bug_history` に全件あるという記述を撤回する。
7. ERRATUM-972-M-01 を「Ad/word-level の混成」へ直し、W/χ_vir と `(iv)-m` の射程を上記どおり限定する。
8. `docs/状態.md`、C-15、完結索引、最終逐語、関連 cert の conclusion/claim boundary を同じ限定文言へ同期する。

以上を満たした再提出なら、有限 campaign の成果（\(p=2\) candidate、K3 24 行 cross-check、p=3 H² 24 行＋2 対照、検証網の改善、972 旧計器撤回、W candidate、予言簿運用）は個別に再評価できる。現行の C-15 完結宣言をそのまま受理する余地はない。

AUDIT_154_VERDICT: 差し戻し
