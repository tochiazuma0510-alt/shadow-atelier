# Luna へ — 便 03 追閉鎖指示: G1★ 最終 acceptance の fail-closed 接続

## 役割と目的

Sol 便 03 の裁定は「条件付き」。現データへの反例はなく 18/18 verdict は PASS しているが、便 02 の受入れ契約を壊れた入力にも耐える回帰ゲートとして凍結するには、合否接続 4 件と runtime cap 1 件が残る。

新対象は探索しない。宇宙は従来どおり

\[
n\in\{3,\ldots,16,18,36\}\quad\text{および }N_5
\]

に固定する。Prop. 3.5 の 256 ordered pair と doubling 補助 target 22,26,30 も従来どおりであり、研究対象の拡張ではない。

## 対象

- `crosscheck/check.mjs`
- 10 分 cap 分割に必要な最小の `search/*.g`（既存 script を壊さず versioned shard とすることを優先）
- 再生成される `certificates/*.v1.json`
- 再生成される `crosscheck/verdicts/*.verdict.json`
- `provenance/cert-hashes-wp2.txt`
- 報告: `sol/luna_reply_03_acceptance_closure.md`

上記以外を変更しない。GAP を Luna 環境で起動できない場合は UNKNOWN とし、司令塔実行へ渡す再現コマンド・期待 artifact を明記する。commit/push はしない。

## A — dihedral raw count を fail-closed にする

全 16 dihedral certificate で node が

\[
R_n=|\mathcal X_n|\,|[G_n,G_n]|
\]

を自前計算し、`cert.counts.raw_candidates === R_n` を必須 PASS 条件にする。

verdict に少なくとも `claimed_raw`, `expected_raw`, `X_n_count`, `derived_order`, `ok` を残す。式を満たさない fixture が `all_pass=false` になる自己検査も加える。raw 候補そのものの再列挙は不要である。

## B — factor map の二つの型を分離する

1. Prop. 3.5 の一般 factor map は井戸定義性だけを admissibility とする。source→target の非単射 collision は許される。
2. doubling \(K^{(n)}=K^{(2n)}\) は isomorphism assertion である。`well_defined && injective && image_order === target_order`（同値な厳密条件でもよい）を `pass` に接続する。
3. global の集計には意味を分けて、少なくとも
   - false pair 数 = 212
   - false pair で collision を検出した数 = 212
   - false なのに well-defined だった数 = 0
   - true pair で collision が出た数 = 0
   - mismatch = 0
   を名前の曖昧でない field で残す。
4. 既存 `false_collision_count` の意味を黙って変更しない。additive field で互換性を保つか、schema/version を上げて理由を報告する。
5. global `status` は必須 suite 全 PASS のときだけ `PASS`、数学的不一致は `FAIL`、cap/例外/未完走だけ `UNKNOWN` とする。`all_pass` は `numeric.ok`, `doubling.ok`, `prop_3_5.ok`, `reduction_triangle.ok` の全てに明示的に依存させる。PASS verdict にも実際の `cap_ms` を記録する。

## C — 代表元不変性を下流計算まで直接比較する

全 canonical dihedral shadow について

\[
(m,f)\mapsto(m+N_{\rm ord}, f x^{N_{\rm ord}})
\]

を作り、次を original/shifted の両方へ実際に適用して一致を取る。

1. full hexagon (3.3), (3.4) の両式。
2. \(f\) の quotient 値。
3. \(T(\sigma_1),T(\sigma_2)\) の置換値。
4. composition: 全 certificate table row で、左因子・右因子の各代表を shift しても canonical target index が同じ。
5. reduction: required entry の全 source index で shifted representative の target index が既存 `image[i]` と同じ。

各比較を名前つき boolean/count として item 12 verdict に残し、一つでも欠落・不一致なら FAIL。`x^N_ord in N_F2` は根拠 assertion として維持するが、それだけから下流 PASS を代入しない。

## D — \(\varrho\) の期待像を exact set で比較する

純 2 冪 n=4,8,16 で node が certificate と独立に

\[
\widetilde H_\alpha=
\{(k,(-1)^a5^b)\in
\mathbb Z/2^{\alpha-1}\rtimes(\mathbb Z/2^{\alpha+1})^\times:
k\equiv b\pmod2\}
\]

を列挙する。\(\varrho\) 像との missing/extra/duplicate を比較し、exact equality を item 13 の `ok` に接続する。個数一致だけでは PASS にしない。

n=8,16 の witness `(0,-1)`, `(1,5)` について、両順序の product index だけでなく、expected product \((k,u)\)、actual target の \(\varrho\)、両者一致、非可換性を verdict に保存する。

## E — GAP 10 分 cap を宇宙不変の shard で閉じる

従来の主 explorer 687 秒を、各 invocation が 600 秒以内になる決定的 shard に分割する。対象の重複・欠落がなく、shard の和が K3..K16+N₅ と exact に一致する manifest/実行出力を残す。q1836 は従来の K18,K36 を維持する。

sharding により certificate 内容が変わらないことを hash で確認する。意図した schema 追加以外で hash が変わる場合は対象と理由を全件報告し、原因不明なら PASS にしない。Luna 環境で GAP が起動不能なら実装と node 側検査まで行い、GAP runtime 条件は UNKNOWN のまま司令塔へ引き渡す。

## 受け入れ条件

1. `node --check crosscheck/check.mjs` PASS。
2. GAP 全 shard が各 600 秒以内、`[ANOMALY]` 0、対象集合 exact。未実行なら UNKNOWN。
3. node full run が規定 cap 内に完走し、証明書 17+global 1 の 18/18 `all_pass=true`。
4. raw formula 16/16、doubling isomorphism 7/7、Prop. 3.5 256/256（true 44・false collision 212/212・false accept 0・mismatch 0）。
5. item 12 が hexagon/T/composition/reduction の direct representative comparison を対象全件で明示 PASS。
6. item 13 が n=4,8,16 の \(\widetilde H_\alpha\) exact set equality、全対積保存、n=8,16 の witness product \(\varrho\) を明示 PASS。
7. K36 triangle 216/216 と N₅ 5/5/4/4・central-power 4/4 を回帰 PASS。
8. 17 certificate hash を実ファイルと照合し、旧版から変化した対象・理由を報告。
9. `git status --short` を原文で報告し、指示対象外の変更がないことを確認。commit/push はしない。

## 撤退条件

- 宇宙を絞って cap を通さない。600 秒を超えた shard は UNKNOWN と実測を報告し、さらに分割する。
- Prop. 3.5 の一般 factor map に injectivity を戻さない。
- doubling の injectivity を「現データでは true」と表示するだけで合否から外さない。
- 代表元不変性や \(\widetilde H_\alpha\) equality を理論的含意・個数一致だけで PASS にしない。
- 既存数学式または証明書の shadow 集合が変わる場合は、最小反例と該当 row を報告して停止する。
