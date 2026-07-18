# Luna へ — 便 02 追検査指示: G1★ ゲートの fail-closed 閉鎖

## 役割と目的

Sol 便 02 の裁定は「条件付き承認」。数学的中核は通ったが、checker の空虚 PASS、N₅ counts、Prop. 3.5 全 256 対、代表元不変性、reduction 三角形、明示同型 \(\varrho\) を機械的に閉じる必要がある。

新しい研究対象は探索しない。較正スイート v2 の既存宇宙

\[
n\in\{3,\ldots,16,18,36\}\quad\text{および }N_5
\]

だけを扱う。

## 対象

- `crosscheck/check.mjs`
- 必要な最小範囲で `search/suite-wp2-explorer.g`
- `search/suite-wp2-explorer-q1836.g`
- 再生成される `certificates/*.v1.json`
- 再生成される `crosscheck/verdicts/*.verdict.json`
- cert hash 記録（既存運用に従う）
- 報告: 司令塔が指定する `sol/luna_reply_02_*.md`

helper 非共有、用語規律（node は cross-checker、verified は Lean 専用）、宇宙の事前登録を維持する。

## 仕様 A — verdict を fail-closed にする

1. schema、family、target id/n、必須 field を検査する。必須 field の欠落は FAIL。
2. dihedral の shadow 数を \(S\) とすると:
   - `composition_table.length === S*S`。
   - 各 ordered pair `(i,j)` がちょうど 1 回、全添字が範囲内。
   - `inverse_map.length === S`、各 source 添字がちょうど 1 回。左右合成が単位。
   - \(3\mid n\) なら `ls_witness.length === S` かつ shadow の `(m,k)` を重複なく全被覆。\(3\nmid n\) なら 0 件を期待値として検査する。
   - reduction は下記の必須 source/target entry を正確に持つ。未適用対象の 0 件と、必要なのに欠けた 0 件を区別する。
3. field が `undefined` のとき項目を verdict から黙って消さない。適用対象なら FAIL、非適用なら理由つき N/A/expected-zero とする。
4. `all_pass` は必須 item set がすべて存在し PASS した時だけ true。
5. certificate の invariants を独立再計算値と比較する:
   - \(|G_n|=4n^3\)（n 奇）/\(4(n/2)^3\)（n 偶）。
   - `index_B3=6*index_PB3`。
   - \(N_{\rm ord}=\operatorname{lcm}(n,2)\)。
   - `derived_order`。
   - `raw_candidates=|X_n|*|[G_n,G_n]|`。raw 候補の hexagon 再列挙は不要。

## 仕様 B — N₅ を node 側でも完全列挙する

1. explorer の段階別 count を分離する。期待値:

   ```text
   raw_candidates = 5
   hexagon_pass = 5
   charming_pass = 4
   surjective_pass = 4
   shadows m-set = {0,1,3,4}
   ```

2. checker は証明書に載った shadow だけでなく m=0..4, f=1 を自前で全列挙し、full (3.3),(3.4)、unit、全射性の各段階を求め、上の count/set と比較する。
3. 受理した全 4 shadow で、置換として

   \[
   T_{m,1}(c)=c^{2m+1}
   \]

   を直接比較する。explorer の `tc_check_pass` を信じるだけにしない。
4. brute kernel の井戸定義性・全単射性検査は維持する。

## 仕様 C — 数値、doubling、Prop. 3.5 の全 256 対

1. node の global suite verdict（名称は実装都合でよい）を追加し、宇宙 16 対象の \(|G_n|,N_{\rm ord}\) を fail-closed にする。K18/K36 も含める。
2. 奇数 n=3,5,7,9,11,13,15 について、marked map \(x_n\mapsto x_{2n},y_n\mapsto y_{2n}\) が同型であることを独立に検査する。補助 n=22,26,30 は doubling 検査だけの一時構成と明記する。
3. 全 256 ordered pair `(q,n)` で

   \[
   K^{(q)}\le K^{(n)}\iff n\mid\operatorname{lcm}(q,2)
   \]

   と marked factor map の well-definedness を一致させる。
4. JS 側は source Cayley graph の word/collision を自前管理し、同じ source 元へ至る語が target で同じ元になるかで well-definedness を判定する。GAP の helper/表を移植しない。
5. 数論式 true の全対、false の全対（既存記録では false 212 対）をともに数え、不一致 0 を acceptance condition にする。

## 仕様 D — reduction 関手性と代表元不変性

1. q1836 explorer で K4 を必要最小限再構成し、K36 certificate に既存 K12 entry に加えて K4 直接 entry を追加する。
2. 必須 reduction は

   ```text
   K8 -> K4
   K12 -> K4
   K9 -> K3
   K18 -> K3
   K36 -> K12
   K36 -> K4   (new direct entry)
   ```

3. checker は各 K36 source index i で

   ```text
   image_36_4[i] === image_12_4[image_36_12[i]]
   ```

   を直接検査する。単に 3 map を個別 PASS にして終えない。
4. 各 family の少なくとも全 canonical shadow（コストが問題なら各 target の決定的代表集合）で

   - `m -> m + N_ord`
   - `f_word -> f_word * x^N_ord`

   を作り、full hexagon、f の quotient 値、T(σ1),T(σ2)、該当する composition/reduction の値が不変であることを検査する。`x^N_ord in N_F2` を根拠として verdict に記す。
5. dihedral の \(\theta,\tau\) induced map が全単射であることも assertion にする。

## 仕様 E — Thm. 4.6 の明示同型 \(\varrho\)

純 2 冪 n=4,8,16 について証明書だけから次を独立検査する。

1. `f_triple[0]=r^(2k)` から \(k\bmod n/2\) を一意に復号する。
2. \(u=2m+1\) は必ず **mod 2n** で保持する。
3. 全 shadow に

   \[
   \varrho(m,k)=(k\bmod n/2,u\bmod2n)
   \]

   を割り当て、重複なし・期待 \(H_n=\widetilde H_\alpha\) 全被覆を検査する。
4. composition_table の全 \(S^2\) 行で

   \[
   (k_1,u_1)(k_2,u_2)=(k_1+u_1k_2\bmod n/2,\;u_1u_2\bmod2n)
   \]

   と target shadow の \(\varrho\) が一致する。
5. n=8,16 で `(0,-1)` と `(1,5)` に対応する shadow を特定し、両順序の積が異なること、その積の \(\varrho\) が上式と一致することを verdict に残す。n=4 は期待どおりの群を確認する。
6. shadow 数 4,16,64 と \(2^{2\alpha-2}\) の一致を明示する。これは Thm. 5.3 の「有限側」較正であり、Galois 下限を node が証明したとは書かない。

## 受け入れ条件

1. GAP 2 スクリプトと node checker が規定 cap 内に完走し、`[ANOMALY]` 0、必須全 item PASS。
2. N₅ verdict が `hexagon_pass=5` と最終 m-set `{0,1,3,4}`、全 4 件の central-power PASS を示す。
3. global verdict が数値全対象、doubling 全対象、Prop. 3.5 の 256/256、一致・false collision を明示する。
4. 全 dihedral verdict が composition \(S^2\)、inverse \(S\)、LS expected coverage、required reduction coverage を明示する。
5. K36 triangle が全 216 source 添字で一致する。
6. n=4,8,16 の \(\varrho\) 全対積保存、n=8,16 の非可換 witness が PASS。
7. 証明書 hash を再生成し、旧版から変わった対象と理由を報告する。
8. `git status --short` を報告し、指示対象外の変更がないことを確認する。commit/push はしない。

## 想定コストと撤退条件

- 実装 60–90 分級、再実行は既存 cap 内を想定。
- 256 factor-map の node 実装が cap を超える場合、宇宙を絞らず UNKNOWN と実測を報告する。数論式だけを再掲して PASS にしない。
- 既存数学式を変更する必要が生じた場合、独断で仕様を変えず、最小反例・該当 source 行・verdict を報告して停止する。
