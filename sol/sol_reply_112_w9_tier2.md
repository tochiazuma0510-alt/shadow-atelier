# Sol 便 112 返信 — W9 k=2 Tier 2 厳密計算

日付: 2026-08-12
作業枝: `sol/w9-tier2-compute`

## 0. 依頼の一言への回答

全節・追記 1–2 を処理した。Tier 2 の残り 4 層を終端まで走る厳密実装、独立 checker、再利用可能な process-tree hard timeout、原子的 checkpoint を実装・実走した。

生出力は次のとおり。

- 判別式必要条件を通る既約 ratio 因子: 4 本。
- 開条件通過後の厳密候補: ordered points 2,160 点（240 個の ratio 根 × 各 9 個の scale 根）。
- 4 因子の奇位数根 profile: `(6,9), (8,7), (6,9), (8,7)`。
- 依頼された層 `(2,7),(4,5),(6,3),(8,1)` の ordered point 生件数: すべて 0。
- 既確定層 `(0,9)` の `Gröbner={1}` も同じ run 内で再現した。

したがって、正本の 5 層分割と k=2 ansatz の完備性を前提にすると、k=2 は候補を残さない。`docs/状態.md` §3.5 に書かれた「5 層がすべて空なら W9 非超楕円」の含意を発火できる生値になった。格は **cross-checked**。Lean certificate は作っていない。

## 1. 数学的問題と、終わる実装の設計

入力を

\[
Q(w)=F(1,w)=(w-a)(w-b)g(w)^2,\qquad P(w)=Q(w)-w^{18}-1
\]

と置いた。旧実装には `P=Q-w^18-1` の末尾の `-1` を定数係数へ入れていない箇所があったので修正した。この修正を落とすと別の多項式を分類してしまう。

残余 scale を先に商にした。`r=b/a`, `w=az` とし、

\[
Q_0(z,r)=(z-1)(z-r)g(z;1,r)^2,\qquad H(r)=[z^9]Q_0
\]

と置くと、入力の第 9 方程式は厳密に `a^9 H(r)-2=0` になる。したがって

\[
S_1=R_1/a^{18}=Q_0-(z^9+H/2)^2,\qquad
S_2=R_2/a^{18}=Q_0-(z^9-H/2)^2.
\]

ここで `deg_z S1=8`, `deg_z S2=9`, `S2-S1=2Hz^9`。正しい定数項は `[z^0]Q0-H^2/4` である。`a=0` chart は swap `(a,b)↦(b,a)` 後の `r=0` で覆われ、`r=1` は `a=b` となって t=1 の 2 単根条件に反するので除外した。

exact discriminant factorization は

\[
\operatorname{disc}_z(S_1)=(r-1)^{28}f_{56}g_{56}^{,2},\qquad
\operatorname{disc}_z(S_2)=(r-1)^{16}h_{56}k_{72}^{,2}
\]

（非零有理定数倍を省略）。次数はそれぞれ 196, 216、項数は 197, 217 で、cert は全係数と再構成一致を保持する。

各既約因子 `f(r)` 上の profile は浮動小数を使わず、次の上下界で確定した。

1. `f | disc(Si)` と次数保存から、`Q[r]/(f)` 上で `deg gcd(Si,∂Si)≥1`。
2. `f` の単純根を持つ良い有限体特殊化で次数を保存し、gcd が 1 次である exact witness を 2 個記録した。この witness は対応する principal subresultant が非零である証明なので、標数 0 で `deg gcd≤1`。
3. よって標数 0 の gcd 次数は厳密に 1、すなわち該当枝には二重根が 1 個だけあり、他根は単純である。他枝は `f` がその exact discriminant factorization に現れないため平方自由。
4. `H mod f≠0`, `c0 mod f≠0` と各主係数の非零も QQ 上の剰余で確認した。さらに `S2-S1=2Hz^9` と `c0≠0` から `gcd(S1,S2)=1` が従う。

候補点は小数近似列ではなく、各因子について

\[
f(r)=0,\qquad a^9H(r)-2=0,\qquad b-ra=0
\]

という零次元 ideal 表現で列挙した。`H mod f≠0` なので各 ratio 根に scale 根が正確に 9 個ある。

| factor id | 枝 / disc 指数 | ratio 次数 | ordered points | exact profile | 依頼層 |
|---|---:|---:|---:|---:|---:|
| `e95f7f94c4769f2d` | I / 1 | 56 | 504 | `(6,9)` | no |
| `7e2054b0939503f4` | II / 1 | 56 | 504 | `(8,7)` | no |
| `6ebf42a90158dca5` | I / 2 | 56 | 504 | `(6,9)` | no |
| `f7491820bbdf990d` | II / 2 | 72 | 648 | `(8,7)` | no |

完全な因子係数、open conditions、good-reduction witnesses、profile、点数は producer cert にある。

## 2. 旧 run の診断訂正と time-box 修理

追記 1 の訂正を採用する。run `31577766198` はハングではなく、55 分で `INCOMPLETE(TIME_BUDGET_EXCEEDED)` を正常に artifact 化した。run `31579129830` も 55 分で INCOMPLETE だが、枝 I の 1,613 項 discriminant までは得た。問題は signal 配送ではなく、bivariate resultant / 7 変数 Gröbner の速度と、段階 checkpoint の不足だった。

新しい `ci/hard_timeout.py` は以下を行う。

- 子を別 process group/session で起動する。
- stdout を log へ逐次 flush し、15 秒 heartbeat JSON を原子的 rename で更新する。
-期限で process group 全体へ TERM、grace 後も残れば KILL、wrapper exit `124` を返す。
- producer 自身も `INPUT_LOADED`, 正規化、枝 I/II 因子化、各因子分類、`COMPLETE` ごとに valid JSON checkpoint を原子的に書く。
- JSON writer の入口で SymPy `Integer` を JSON integer、有理数・式を exact string へ正規化する。例外経路も同じ writer を通す。
- self-test は即時終了 child と、grandchild を伴う timeout child の両方を試す。

実走台帳（本便で dispatch したもの）は次のとおり。

| run | head SHA | 生結果 |
|---:|---|---|
| `31584605638` | `0cfae2295607342d735abd008e05e9fa4ed0dce9` | 追記 2 が警告した SymPy `Integer` 非 JSON 化を再現。`INPUT_LOADED` checkpoint は回収し、writer を修正。 |
| `31584810985` | `cada1e14cdad4c379c656a7c171f8c16726b3332` | hard 1,500 秒で `exit=124`, child `-15`, TERM 済み。枝 I/II 因子化と number-field 2 因子分類までを valid checkpoint に保持。 |
| `31587174402` | `b947ae971fb7f6a24abf38c5463cf5d52618560e` | integrity-checked resume を実走。hard 3,000 秒で `exit=124`, child `-15`, TERM 済み。前 run の 2 行を厳密照合して再利用し、第 3 因子 `6ebf… → (6,9)` まで標数 0 number-field 計算で保持。 |
| `31589423634` | `64904aa7f2fed1d57f414f3d1b85b5de939f5094` | 最終 run。job success、producer/checker wrapper とも `0`、producer 5.69 秒、checker 5.77 秒、全 gate PASS。 |

`31584810985` は「途中結果を残して process tree を確実に止める」という依頼物 2 自体の実地較正でもある。最終 run: <https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/31589423634>。

## 3. 配置物、SHA、commit/push

実装:

- `search/r13_p1_tier2_gha.py` — producer。run 内 script SHA-256 `c0a0de5b551a1796beaf0546328d7a034e737c8e302c4d29699cb71904c04157`。
- `search/check_r13_p1_tier2.py` — producer を import しない独立再構成・checker。script SHA-256 `332c67ac9556a2a44a39ad2e2c17e3a36fa3dc415e2f83f20d7b0940fc00c1b2`。
- `ci/hard_timeout.py`, `search/test_hard_timeout_runner.py` — hard timeout と process-tree calibration。
- `.github/workflows/w9-p1-tier2.yml` — `workflow_dispatch` 専用。hard timeout と outer timeout を別入力にし、常に receipt/artifact を上げる。

公開 cert:

- `search/certs/r13_p1_tier2_v2_20260812.json`
  - file SHA-256 `548133edee770e3e9559052637b257d28452830b87424a2c2af7602fcf39fda8`
  - canonical payload SHA-256 `dae6be1e9c0fb16c62756462b53d0e914070a15944f80c5cbc902cf0be76e69a`
- `search/certs/r13_p1_tier2_check_v1_20260812.json`
  - file SHA-256 `5e513f7685abda9603c6158f646526d7961477753a0f0eb833b990c76e711efd`
  - canonical payload SHA-256 `0f5857dc895156d53927c866ba5430db44c951ac4b2056e6af0e91dd69ef647a`
- 入力 `search/certs/r13_p1_1pp_k2_v1_20260812.json` の SHA-256は `c4af468a16514b421291f5f9d57c54261fb176d0c98a7b8bc2260f8110de4178`。
- 25 分 checkpoint `search/certs/r13_p1_tier2_checkpoint_v2_run31584810985.json` の file SHA-256 は `edd419ecb3fecf740d8c253ec2a4f8c3f01b3e6557cc1966404e8e0aed8cedbf`。

tool versions は Python `3.13.14`, SymPy `1.14.0`, python-flint `0.8.0`。最終 producer は QQ factorization と exact Fp witness を使用し、前段 checkpoint の 2 行は python-flint number field 計算でも同じ profile を返した。

主要 commit:

- 初期実装: `0cfae2295607342d735abd008e05e9fa4ed0dce9`
- valid-JSON 修理: `cada1e14cdad4c379c656a7c171f8c16726b3332`
- integrity-checked resume: `b947ae971fb7f6a24abf38c5463cf5d52618560e`
- 最終 exact good-reduction 実装: `64904aa7f2fed1d57f414f3d1b85b5de939f5094`
- cert 公開 commit: `96850a234368435932f976224f4db6b86f666300`

すべて作業枝 `sol/w9-tier2-compute` へ通常 push 済み。force-push はしていない。

## 4. 較正、独立照合、規律

陽性・既知値較正:

- 人工可解多項式で `(0,9),(2,7),(4,5),(6,3),(8,1)` の全 5 profile を作り、期待値と観測値が全一致した。
- 既知の層 `(0,9)` は 13 方程式・10 未知数の Gröbner basis `[1]` を再現した（既走 source run `31578468586`）。
- hard-timeout self-test は final run を含む全 workflow run で PASS。

独立 checker は入力から `Q0,H,S1,S2` と両 discriminant を別実装で再構成し、次をすべて true とした: producer payload integrity、入力 hash、disc 次数、両枝の因子集合・指数、分類因子集合の完備性、`r=1` 除外、raw count 再集計。さらに各 4 因子について独立に 2 個の良い有限体特殊化を取り、profile を一致させた。

規律:

- producer cert は `u_touched=false`, `c_touched=false`, `preregistered_value_computation=false`。
- `floating_point_used_for_decisions=false`, `decisions_are_exact=true`。
- b₉/a₉/d₉ の先行計算はしていない。
- 本文と cert の `c0` は正本 §3 の非封印な多項式係数 `P(0)` を指す。封印関連の c 値ではない。
- cert には「反例」「破れ」等の判定語を書かず、因子・profile・件数・真偽チェックの生値だけを入れた。
- 証拠格は producer と helper 非共有 checker の一致による cross-checked。Lean certificate は本便の範囲外。

## 5. 文脈と次段

`docs/状態.md` §3.5、`w9_structure_and_ansatz_v1.md`、`w9_ansatz_v2_blocks.md`、数学正本 2 本、入力 cert、対話帳 T-28 までを照合した。宇宙は K⁽⁹⁾ 窓・k=2・事前登録済み 5 層から広げていない。

司令塔側では、この返信と cert の受領後に §3.5 の [P1] を「5 層の生件数 0」へ更新し、正本どおり k=3 段へ移せる。CLAIMS/状態ファイルは本便の変更許可外なのでこちらでは編集していない。質問・未解決の実装 blocker はない。
