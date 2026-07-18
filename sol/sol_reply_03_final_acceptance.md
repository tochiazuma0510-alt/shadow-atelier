# 検収【条件付き】＋宣言文【承認（発令は追閉鎖後）】

最終成果物の**現データ**には、G1★ の数学的結論を壊す反例を見いださなかった。証明書別 17 verdict と global verdict は 18/18 `all_pass=true`、N₅ は 5/5/4/4、Prop. 3.5 は 256/256（true 44・false 212・mismatch 0）、K36 三角形は 216/216、
\(n=4,8,16\) の \(\varrho\) は 16/256/4096 積を保存し、17 証明書の実 SHA-256 先頭 16 桁も台帳と 17/17 一致する。

しかし、便 02 指示書の契約を **fail-closed な較正ゲート**として読むと、まだ無条件合格にはできない。現物では正しい値を出しているが、(i) dihedral raw count の式、(ii) doubling の同型性、(iii) 代表元変更後の下流値、(iv) \(\varrho\) の像と \(\widetilde H_\alpha\) の集合一致が合否へ十分に接続されていない。また主 GAP スクリプトの 687 秒は事前登録した 600 秒 cap を超えた。従って **G1★ の発令と `v1.0-g1` tag は追閉鎖後まで保留**する。

宣言文は提示された文言のままで数学的に適切であり、修文を要求しない。追閉鎖後、同じ限定と状態語彙を保ったまま宣言してよい。

## 受け入れ条件 8 項の検収

| # | 裁定 | 突合結果 |
|---:|:---|:---|
| 1 | **未充足** | 18/18 の現 verdict と `[ANOMALY]` 0 は報告どおり。ただし主 explorer は 687 秒で 10 分 cap を 14.5% 超過した。また後述 F1–F4 の必須 assertion が `all_pass` に未接続である。 |
| 2 | **合格** | `N5.v1.verdict.json` の node 自前全列挙は raw/hexagon/charming/surjective = 5/5/4/4、m-set = {0,1,3,4}、central-power 4/4 PASS。m=2 は hexagon PASS・unit/surjective FAIL と正しく分離された。 |
| 3 | **条件付き** | global 実体は numeric 16/16、doubling 7/7、Prop. 3.5 256/256、true/false = 44/212、false 212 対すべて `conflict_count>0`、mismatch 0。ただし doubling の `pass` が井戸定義性だけを見ており、報告 field `false_collision_count` の意味も誤解を招く。 |
| 4 | **合格** | 全 16 dihedral verdict で composition = \(S^2\)、ordered pair 一意・全被覆、inverse = \(S\)、LS = expected、required reduction の exact entry set を確認した。 |
| 5 | **合格** | K36→K4 直接像と K36→K12→K4 の像は全 216 source 添字で一致。 |
| 6 | **条件付き** | \(\varrho\) の全対積保存は n=4: 16/16、n=8: 256/256、n=16: 4096/4096。n=8,16 の witness は積 index 5 と 3 で非可換。ただし仕様 E3 の \(\widetilde H_\alpha\) exact set 比較が未実装である。 |
| 7 | **合格** | 記録 hash と実ファイルは 17/17 一致。旧版から内容が変わった証明書は N₅（`target.n=5`、hexagon count 4→5）と K36（K36→K4 direct entry 216 件）の 2 通で、hash はそれぞれ `9f26…→a98d…`, `27ac…→feac…`。他 15 通は決定的再生成で同一 hash。 |
| 8 | **合格** | 監査開始時は clean。本返信作成後の許可内変更は本返信と `sol/luna_task_03_acceptance_closure.md` の 2 新規ファイルだけである。commit/push は行っていない。 |

## F1【重大】raw candidate 式が合否に未接続

仕様 A5 は dihedral について

\[
\texttt{raw\_candidates}=|\mathcal X_n|\,|[G_n,G_n]|
\]

を独立再計算値と比較するよう要求した。ところが `crosscheck/check.mjs` 512–524 行は invariants 4 項だけを調べ、1109–1123 行の counts は単調性・最終 shadow 数・Thm. 4.3 の最終集合だけを見る。`raw_candidates` を別の正値へ増やしても単調性を保つ限り PASS し得る。

現物 16 通は式に一致する（例 K8: \(8\cdot16=128\)、K36: \(24\cdot1458=34992\)）ので、これはデータ反例ではなく残存 fail-open である。式の左右と PASS を verdict に残し、`all_pass` に接続せよ。

★ 最終個数が既知集合と一致しても、探索母数の記録が正しいとは限らない。「列挙結果の完全性」と「探索経路の会計」は別 assertion である。

## F2【重大】factor map の修正は正しいが doubling には適用しすぎている

Prop. 3.5 で必要なのは marked map

\[
B_3/K^{(q)}\longrightarrow B_3/K^{(n)}
\]

の**存在**であり、source の同じ元へ至る語が target でも一致するという井戸定義性が必要十分である。reduction は一般に非単射なので、Luna の「単射性→井戸定義性」修正を **追認する**。`crosscheck/check.mjs` 725–739, 761–768 行の collision 検査は仕様 C3–C4 の正しい読みである。

一方、doubling 仕様 C2 は \(K^{(n)}=K^{(2n)}\) に対応する marked **isomorphism** を要求する。750–754 行は全行で `injective=true` を計算・記録しているのに、`pass: r.well_defined` としかしていない。現データ 7/7 は単射かつ同位数で正しいが、将来 `injective=false` でも PASS する。doubling に限っては井戸定義性・単射性・target 全被覆（または両群同位数）を合否に結べ。

★ 商写像の存在条件と、二つの商が同一 kernel をもつ条件は違う。ここで単射性を一律に捨てると Prop. 3.5 は直るが doubling の主張が弱くなる。

## F3【重大】代表元不変性は下流の実装を直接試していない

仕様 D4 は全 canonical shadow に対し

\[
(m,f)\mapsto(m+N_{\rm ord},f x^{N_{\rm ord}})
\]

を実際に作り、full hexagon、\(f\) の商値、\(T(\sigma_1),T(\sigma_2)\)、composition、該当 reduction の値が不変であることを要求した。ところが `checkRepresentativeInvariance`（630–638 行）が保存する行は `hexagon_periodic`, `quotient_f`, `induced_u`, `x_Nord_in_N_F2` だけで、`hexagon_periodic` も full hexagon の再評価ではなく \(x^{N_{\rm ord}}=1\) と \(u\) の周期性から設定している。T・composition・reduction の直接比較はない。

数学的には商値が同じなら下流値も同じである。しかしこのゲートの目的は、その数学をコードが正しく実装したかを較正することだった。各下流計算を実際に二代表へ適用し、名前つき assertion として verdict に残す必要がある。

★ 「理論上同じだからテストを省く」は定理の証明としてはよくても、代表の取り方に依存する実装バグを捕える回帰試験にはならない。

## F4【要修正】\(\varrho\) は積を保つが、期待像を構成していない

`checkVarRho`（668–701 行）は \((k,u)\) の重複なし、期待**個数** \(2^{2\alpha-2}\)、全対積保存を調べる。しかし仕様 E3 の期待集合

\[
\widetilde H_\alpha=
\{(k,(-1)^a5^b): k\equiv b\pmod2\}
\]

を独立に列挙して exact set equality を比較していない。期待個数だけでは、同じ大きさの誤った部分集合を排除できない。現物は item 5 の Thm. 4.3 集合一致と全積表から強く支持されるが、「\(\widetilde H_\alpha\) への明示同型」という独立 acceptance item は未閉鎖である。witness についても \(AB,BA\) の expected/actual \(\varrho\) を verdict に明記せよ。

## F5【要修正】global の collision 集計名と status を fail-closed にせよ

最終 JSON を行単位で集計すると、number-theory false 212 対は 212/212 で `conflict_count>0`、false なのに井戸定義だった対は 0、true なのに conflict があった対も 0 である。これは期待どおりである。

しかし 782–783 行の `false_collision_count` は「false 対のうち `well_defined=true`」を数えるため値 0 であり、「検出した collision 数」を読む名称ではない。`false_pairs_with_collision=212` と `false_accept_count=0` を分けよ。また `status:'PASS'` が固定値なので、必須 suite が落ちた場合は FAIL、cap/例外時だけ UNKNOWN となるよう `all_pass` と同期させよ。最終 artifact の `elapsed_ms` は 3353 ms であり、課題票の 3475 ms、Luna 報告の 3816 ms は別実行の実測として扱えば矛盾ではない。

## F6【運用重大】10 分 cap は実際に超過した

主 explorer の 687 秒は、事前登録した「GAP 1 スクリプト ≤ 10 分」を満たさない。14%程度でも、cap は結果を見た後に黙って免除できない。数学的 PASS を覆す事情ではないが、受け入れ条件 1 の文言上は明確な未充足である。宇宙を変えず決定的 shard に分割し、各 invocation が 600 秒以内で同じ証明書/hash を出すことを確認せよ。q1836 側 448 秒と node global 3.353 秒は cap 内である。

## F7【提案】G1★ 宣言文は原文のまま承認

承認文は次のとおりである。

> B₃ gentle 系の有限側定義と、dihedral K⁽ⁿ⁾ の既知有限計算、とくに n=4,8,16 の群構造・位数を GAP と独立照合器で再現した。Thm 5.3 の Galois/arithmetical 下限そのものは論文の定理を用い、その下限と再現した有限群位数の一致から 2 冪の場合の結論へ接続する。これは cross-checked(照合済み)の宣言であり、Lean による verified(検証済み)の宣言ではない。

有限側の再現と arithmetic input を分離し、cross-checked と verified も分離しているため、修正は不要である。ただし、上の追閉鎖後に全 18 verdict を再生成し、研究者が検分してから発令するという時間条件を付す。

## G1★ 版の凍結候補への裁定

凍結の原則は**採用**する。ただし現在の commit を `v1.0-g1` として固定してはならない。追閉鎖後の同一版で explorer shard、17 証明書と hash、18 verdict、checker、再現コマンドを束ね、その exact commit に annotated tag を付すべきである。

「撤退条件なし」は、tag を後から動かさないという意味ならよい。回帰失敗や trusted base の変更が出た場合は旧 tag を改変せず、新しい版を作る。Week 3 の機構変更は、凍結版の全較正ゲートが PASS しなければ atlas の主張へ昇格させない。

追閉鎖の実装票は `sol/luna_task_03_acceptance_closure.md` に分離した。

## 監査範囲外の申告

- Sol の役割規律に従い、GAP explorer と node checkerは再実行していない。source、証明書、verdict、git 履歴、hash を静的・数学的に監査した。
- 17 証明書の全 shadow 語と全 256 factor-map 行を人手で再計算してはいない。件数・集合・合否接続を全件集計し、N₅/K8/K36/global を重点監査した。
- GAP の 687/448 秒と `[ANOMALY]` 0 は司令塔実行記録の監査であり、Sol 環境での独立再実測ではない。
- Thm. 5.3 の Galois 理論、Ihara embedding、cyclotomic character は再証明していない。
- Lean 証明書は未接続であり、今便に verified の主張はない。
- Week 3 の新対象 \(L=K^{(3)}\cap N_0\)、第三者 packageGT、atlas の新規計算は監査範囲外である。
- tag の作成、commit、push は司令塔の権限であり、Sol は実施していない。

## 考察と提案

戦況の読みは「数学データは通過、凍結ゲートは最後の接続不足」である。

これは G1★ の撤回ではなく、G1★ というラベルの意味を守るための短い保留である。

今回も現物の正しさと、壊れた現物を必ず拒否する性質を分けて裁定した。

P9: factor map の井戸定義性への修正を Prop. 3.5 について正式追認する。

P10: doubling だけは同型性を別 assertion とし、単射・全射を合否へ戻す。

P11: raw count、代表元不変性、\(\widetilde H_\alpha\) exact image を一便で追閉鎖する。

P12: 687 秒の主 explorer は宇宙を変えず決定的 shard に分割する。

P13: 追閉鎖後の exact commit にのみ annotated `v1.0-g1` tag を付す。

P14: tag には cert hash 17 件だけでなく verdict 18 件と実行コマンドも束縛する。

P15: Week 3 の atlas 作業は凍結 tag の回帰 PASS を入口条件にする。

G2 の第一撃では、既知 Dih の正解表と未知対象の探索表を同じ台帳行に混ぜない。

\(L=K^{(3)}\cap N_0\) は Dih 外なので、\(c=1\) を暗黙に使う helper を入口で拒否する。

N₅ control は Week 1 の飾りではなく、Dih 外で中心項が生きることを監視する回帰標本である。

atlas の各行は genuine/fake/UNKNOWN の三値を保持し、未探索を fake と表示しない。

fake は有限の survival 失敗証明書で閉じられるが、有限深度 PASS から genuine は従わない。

reduction の向き \(N\le H\Rightarrow GT(N)\to GT(H)\) は atlas schema に型として埋め込むべきである。

候補の全列挙、kernel equality、survival は別 column・別証拠に保つべきである。

性能 shard は数学的宇宙の分割であり、宇宙の縮小であってはならない。

各 shard は対象集合、件数、hash の和が事前登録宇宙と exact に一致することを証明する。

W15: `all_pass=true` を、合否に接続されていない表示 field の存在と取り違えない。

W16: quotient factor map に一律の injectivity を要求しない。

W17: isomorphism を主張する doubling から injectivity を落とさない。

W18: expected cardinality と expected set equality を同一視しない。

W19: 代表元不変性を理論的同値だけで済ませず、下流 API の回帰試験にする。

W20: collision 0 と collision 検出 212 を同じ field 名で報告しない。

W21: cap 超過を結果判明後の便宜的例外にしない。

W22: `v1.0-g1` tag を後から動かさず、変更時は新しい較正版を作る。

この追閉鎖が通れば、G1★ 宣言文をそのまま発令し、K3/n=12 atlas と Dih 外第一撃へ進んでよい。
