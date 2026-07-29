# SAT run artifact ledger — n=21 tail-8 calibration (裁定 214 工程 4)

CI artifact 収蔵の台帳(F85-8.4 の要求: artifact を台帳へ束縛して初めて「独立方法による
cross-check」と記録できる、という Sol の指摘への対応)。全ハッシュは機械出力(`sha256sum`)を
そのまま貼り付け — 手写しなし。

## Run metadata

| | class run | transitive run |
|---|---|---|
| GitHub Actions run ID | `30454823288` | `30454826413` |
| workflow | `sat-run` (`.github/workflows/sat-run.yml`) | 同左 |
| workflow_dispatch `run_label` | `calibration` | `calibration` |
| trigger `createdAt` | 2026-07-29T13:10:41Z | 2026-07-29T13:10:43Z |
| commit (`headSha`) | `0b148018a058efdbdd2737a375de76853189e0f6` | `0b148018a058efdbdd2737a375de76853189e0f6` (同一 commit、2 本並列発火) |
| kissat commit (pinned in workflow at that commit) | `8af8e56f174b778aef3aa45af9f739b2a5f492c2` (arminbiere/kissat) | 同左 |
| drat-trim commit (pinned) | `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (marijnheule/drat-trim) | 同左 |
| CNF input | `search/sat/out/tail8_n21_class.cnf` | `search/sat/out/tail8_n21_transitive.cnf` |
| CNF sha256 (per `search/sat/manifest_tail8_n21.json`) | `6b5df42974877b91de8317d4285d89b3517461d9ae1dc2da36cc00623dc40a33` | `02fcc56722880ccba8c6dcf83c80886b009d3b0f454d0d44a0c96874eba17113` |
| CNF sha256 re-hashed from downloaded artifact (`problem.cnf`) | `6b5df42974877b91de8317d4285d89b3517461d9ae1dc2da36cc00623dc40a33` — **一致** | `02fcc56722880ccba8c6dcf83c80886b009d3b0f454d0d44a0c96874eba17113` — **一致** |
| verdict (`result.txt`) | `exit=10` / `verdict=SAT` | `exit=20` / `verdict=UNSAT` |
| local storage | `search/sat/runs/n21_class/` | `search/sat/runs/n21_transitive/` |

## SHA256SUMS — n21_class (search/sat/runs/n21_class/)

CI が出した元の SHA256SUMS.txt(`SHA256SUMS_orig.txt`、`proof.drat` 単体のみ収録)に加え、
ローカルで収蔵した全ファイル一式(`proof.drat.gz` はこの台帳作成時にローカルで gzip -k した
もの — CI 自体は SAT run では drat-trim を走らせないため `.gz` を出力しない設計。中身は
`proof.drat` と同一、gzip 圧縮のみ)を機械出力したものが `SHA256SUMS.txt`:

```
669acddec2df170cd53cf6b235d64c49d1724c3ea24bec562d3b6bfa81822f8d *kissat_out.txt
52c4ebbd557312ab5a2170f41c623963f6ea81494f5bf59229bdd66e06126afa *kissat_time.txt
fb1424dc478ec0d1528cae2cffd035055d05d2cd1235fe2eb206a82de4651361 *model_vlines.txt
6b5df42974877b91de8317d4285d89b3517461d9ae1dc2da36cc00623dc40a33 *problem.cnf
b5226752122204718905494fa9ea066e0424bb978ff9c22871a9a40ddcdb724f *proof.drat
46e9885aa3465dc248c9305e7fcb6968ef0026bdd718f9fe3fe5c64c13ecd452 *proof.drat.gz
b70f5c10f578a5addc58babb6e3d6d9b0401d0ec4311aed698d89f4c7993a34c *result.txt
96111b4844620785eaec7f2fd4495c2ea279439ac6534d787ba57df3636f544a *run_label.txt
```

CI 自身が出した元の SHA256SUMS.txt(`proof.drat` のハッシュ `b52267...` が上と一致すること
を確認済み — ローカル収蔵で改変していないことの傍証):

```
669acddec2df170cd53cf6b235d64c49d1724c3ea24bec562d3b6bfa81822f8d  kissat_out.txt
52c4ebbd557312ab5a2170f41c623963f6ea81494f5bf59229bdd66e06126afa  kissat_time.txt
fb1424dc478ec0d1528cae2cffd035055d05d2cd1235fe2eb206a82de4651361  model_vlines.txt
6b5df42974877b91de8317d4285d89b3517461d9ae1dc2da36cc00623dc40a33  problem.cnf
b5226752122204718905494fa9ea066e0424bb978ff9c22871a9a40ddcdb724f  proof.drat
b70f5c10f578a5addc58babb6e3d6d9b0401d0ec4311aed698d89f4c7993a34c  result.txt
96111b4844620785eaec7f2fd4495c2ea279439ac6534d787ba57df3636f544a  run_label.txt
```

## SHA256SUMS — n21_transitive (search/sat/runs/n21_transitive/)

`SHA256SUMS.txt`(ローカル再計算、CI が出した元 `SHA256SUMS_orig.txt` とバイト同一の値):

```
4cc3f76fe550b0a415709123fd7b2802e39ccbbbc8846dff9c09767732b6c228 *core.cnf.gz
45b14b1de5fc15ab293c6921ac4e7fd5b87401a368a56aa31e6af18c21cd678d *drat_verify.txt
6e0bd57c9119aeece7cbfef1683ccf9f08f22af2420d5ad9e03779634cb51482 *kissat_out.txt
ee9eacf8d00df2e268a9e984db59c9601aede83adf8e982a3d98b29dca33b1b2 *kissat_time.txt
02fcc56722880ccba8c6dcf83c80886b009d3b0f454d0d44a0c96874eba17113 *problem.cnf
0efcbbb7c0eeba8540bb5c936247e1f233525706a82e17c542b5441c31c6d998 *proof.drat.gz
3e5ba9451f68218517d545b5f7a51feb1d744b748b5c33e56ecd553011c06fff *proof.lrat.gz
f7f55c9281045e79a5e7016b0b229fdd33551726e9087a59b8d6165eec67f163 *result.txt
96111b4844620785eaec7f2fd4495c2ea279439ac6534d787ba57df3636f544a *run_label.txt
```

`drat_verify.txt` の要旨: `16364 of 50128 clauses in core`, `20477 of 32475 lemmas in core
using 2262363 resolution steps`, `5321 RAT lemmas in core`, `s VERIFIED`
(`verification time: 2.993 seconds`)。

## 独立照合(この台帳作成時にローカルで実施)

- `node search/sat/check_model_n21.mjs --mode class --model search/sat/runs/n21_class/model_vlines.txt`
  → `ok: true`(全 6 check: a decodes to total function・involution 型 2¹⁰1・
  B が独立再計算の b=u⁻¹(a(・)) と一致・b³=1・b fixed-point-free・b 型 3⁷、全て
  `ok:true`)。encoder の変数配線・model の decode ともにモデルの B 変数自体は信用せず
  再計算した結果と突合済み。
- `python search/sat/lrat_check.py --cnf search/sat/runs/n21_transitive/problem.cnf --lrat search/sat/runs/n21_transitive/proof.lrat.gz`
  → `s VERIFIED`(`lines_processed: 33626`, `elapsed_seconds: 3.306`)。
  drat-trim(CI・`drat_verify.txt`)とは**別実装**(本便で新規に自前実装、drat-trim を
  import・呼び出ししていない)による独立 LRAT 再照合。両者の verdict が一致 —
  **cross-checked**(「検証済み」ではない、CLAUDE.md 語法規約・`docs/notes/sat_completeness_n21_v1.md` §0)。
  fail-closed の確認: 同じ proof の 1 ヒント id を意図的に破壊したコピーを用意し
  (`scratchpad/proof_corrupted.lrat`)、`lrat_check.py` が `s NOT VERIFIED`
  (`hint clause id 80677 not active in database`)を即座に返すことを確認済み
  (silent leniency がないことの動作確認)。

## mutant 4 発(M8/M9/M10-depth19/M10-depth20)— 裁定 227(Sol P86-4)収蔵

Sol 便 86(`sol/sol_reply_86_math13.md` F86-3.3)が「4/4 完走の delivery claim は
artifact 未収蔵につき FAIL」と裁定した 4 run を実際に `gh run download` で回収し、
本節に台帳化する。全ハッシュは機械出力(`sha256sum`)そのまま。

| | M8 (reach_reverse_drop) | M9 (edge_reverse_drop) | M10 depth19 | M10 depth20 |
|---|---|---|---|---|
| GitHub Actions run ID | `30462013453` | `30462017651` | `30462021827` | `30462026033` |
| workflow | `sat-run` | 同左 | 同左 | 同左 |
| workflow_dispatch `run_label` | `calibration` | `calibration` | `calibration` | `calibration` |
| trigger `createdAt` | 2026-07-29T14:40:09Z | 2026-07-29T14:40:12Z | 2026-07-29T14:40:16Z | 2026-07-29T14:40:19Z |
| commit (`headSha`) | `5be1f07b579c01c1537725f61f79b64f56e5a3f1` | 同左 | 同左 | 同左 |
| kissat commit (pinned) | `8af8e56f174b778aef3aa45af9f739b2a5f492c2` | 同左 | 同左 | 同左 |
| drat-trim commit (pinned) | `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` | 同左 | 同左 | 同左 |
| CNF input (`cnf_path` の実 log 値) | `search/sat/out/mutants/tail8_n21_mutant_reach_reverse_drop.cnf` | `search/sat/out/mutants/tail8_n21_mutant_edge_reverse_drop.cnf` | `search/sat/out/mutants/tail8_diam20_path21_depth19.cnf` | `search/sat/out/mutants/tail8_diam20_path21_depth20.cnf` |
| CNF sha256 (`mutants_n21.json` 記載値) | `175671de52bcfceb8e35d8f016d8b384be04374153d4da606fd13452e29d01fe` | `dfae54b8d9bb02827c28570dc808890f062705a3ec32b81e704d69c6f66b0fc4` | `e9bb1713fa0456b865f9a8ac11687640c511979cfb22dadab32e197a79a8669b` | `befa6f1b05a4a3633f751abd030d913da2dc41d59567b91dd94c92c68b531cc6` |
| CNF sha256 (downloaded `problem.cnf` 再計算) | 同上 — **一致** | 同上 — **一致** | 同上 — **一致** | 同上 — **一致** |
| verdict (`result.txt`) | `exit=10` / `verdict=SAT` | `exit=10` / `verdict=SAT` | `exit=20` / `verdict=UNSAT` | `exit=10` / `verdict=SAT` |
| 事前登録 prediction (`mutants_n21.json`) との一致 | 一致(PROVEN: SAT) | 一致(PROVEN: SAT) | 一致(PROVEN: UNSAT) | 一致(PROVEN: SAT) |
| local storage | `search/sat/runs/n21_m8_reach_drop/` | `search/sat/runs/n21_m9_edge_drop/` | `search/sat/runs/n21_m10_depth19/` | `search/sat/runs/n21_m10_depth20/` |

### SHA256SUMS(各 local storage、収蔵時にローカル再計算・機械出力)

`search/sat/runs/n21_m8_reach_drop/SHA256SUMS.txt`:
```
71080db56b8e064faabf9de578c94231590f018c087042150e7049727cf80cc1 *check_model_output.txt
926e9c9fd94732f7c2092c4d1d8ad7fa7ec4cde6082cfba67ba5e0debf75ce27 *kissat_out.txt
4d0e79cbbe0d7dcb6f11fc7c1eec9e8378c8e478768cb6bea70b66d1b212bfb6 *kissat_time.txt
19c324e90b6422445e8956473287273c45474fb6b4fb3c4625f65e138fa8a132 *model_vlines.txt
175671de52bcfceb8e35d8f016d8b384be04374153d4da606fd13452e29d01fe *problem.cnf
2f8f98eccebfd33ce03fe2b1b6101fdb12e0d4256e22bb6822b58e7be16cb3ac *proof.drat
b70f5c10f578a5addc58babb6e3d6d9b0401d0ec4311aed698d89f4c7993a34c *result.txt
96111b4844620785eaec7f2fd4495c2ea279439ac6534d787ba57df3636f544a *run_label.txt
```
(`check_model_output.txt` はローカル追加分。CI が出した元 `SHA256SUMS.txt` はこの
7 行のうち `check_model_output.txt` を除く 7 行とバイト同一 — CI artifact 自体に
改変なし。)

`search/sat/runs/n21_m9_edge_drop/SHA256SUMS.txt`:
```
26b9659ef20ec6ed349a1de46cb99ba497bbad8f3e18d8914a1209d44a8a23ba *check_model_output.txt
f2f94113897f860aeb0a8003483fdbc315ff3e38645c9879340ffbd14e97099d *kissat_out.txt
a755933776e4048924626961361f432424d54db45dadc249a41d8814c28da0ba *kissat_time.txt
fd0548ce332cbeb50d19ceef348b92404592c55c925d35b0af892ad71c4e5554 *model_vlines.txt
dfae54b8d9bb02827c28570dc808890f062705a3ec32b81e704d69c6f66b0fc4 *problem.cnf
ce95dd17b5239377eeb8da360ba7fdd1d0ddd3a31ea97341f4649625e9897e83 *proof.drat
b70f5c10f578a5addc58babb6e3d6d9b0401d0ec4311aed698d89f4c7993a34c *result.txt
96111b4844620785eaec7f2fd4495c2ea279439ac6534d787ba57df3636f544a *run_label.txt
```

`search/sat/runs/n21_m10_depth19/SHA256SUMS.txt`:
```
669e36078502de1e8e35262e4503106e3b8abd30dfb67bd574dc4a72ddb452a6 *core.cnf.gz
f6bd44eb17a40e2f29db4ead4a77ee3e4fc22aa737bf752523fa26a065b19f20 *drat_verify.txt
1e5d148f50aa09a9bfebfa52172f667bf3202804f09114eca4c3d122f311281c *kissat_out.txt
6c08805a6ee05dbb3e62cf07a0582f4a7c052d5b760b42b97b0afaacb3926d6a *kissat_time.txt
220752a44288ae30fac47941e615ecb15fcf22b2fcc8fa579f679eb431f1eb0a *lrat_check_output.txt
e9bb1713fa0456b865f9a8ac11687640c511979cfb22dadab32e197a79a8669b *problem.cnf
a62066905318a8d8fed1480f2e9fdadfaddcdb838e4964f5baa42cb266739494 *proof.drat.gz
5bf72bacd42375fa8052e127fa0859c9e75b194dc787d9757e958ea89254931b *proof.lrat.gz
f7f55c9281045e79a5e7016b0b229fdd33551726e9087a59b8d6165eec67f163 *result.txt
96111b4844620785eaec7f2fd4495c2ea279439ac6534d787ba57df3636f544a *run_label.txt
```

`search/sat/runs/n21_m10_depth20/SHA256SUMS.txt`:
```
1508c9272ce5fd4334d0144f45f708c3cb0e2b71a89751d6ad4aeefa70aa45a0 *check_model_output.txt
3c6c45b617d5068c6f93b866f1375de7be0d6e5f2e32767b651a93878c81b4e3 *kissat_out.txt
a0a247744687be88eba90e2ef5d32ea745af2f2f649b4a858b3adb9ae405c3c1 *kissat_time.txt
787f3b228f5c73a6de089ac04bccedcdea32eb44f4308f2cbb92f11936267399 *model_vlines.txt
befa6f1b05a4a3633f751abd030d913da2dc41d59567b91dd94c92c68b531cc6 *problem.cnf
a19d7d365332396138aa0f689071f836e8f2d2e83534fa42dabdda3f6684d468 *proof.drat
b70f5c10f578a5addc58babb6e3d6d9b0401d0ec4311aed698d89f4c7993a34c *result.txt
96111b4844620785eaec7f2fd4495c2ea279439ac6534d787ba57df3636f544a *run_label.txt
```

### 独立照合(この節作成時にローカルで実施)

- `node search/sat/check_model_n21.mjs --mode transitive --model search/sat/runs/n21_m8_reach_drop/model_vlines.txt`
  および同じく `n21_m9_edge_drop/model_vlines.txt` に対して実行:
  いずれも `ok:false`。decoded a,b は involution 型・order・独立再計算 B=u⁻¹(a(・))
  一致など個々の check は `ok:true` だが、最後の `generated_group_is_transitive_on_1..21`
  だけ `ok:false`(orbits `[6,15]`)。これは M8/M9 の事前登録 prediction が明記した
  「decoded_counterexample_property」(モデル自身の R/E 変数は充足を主張するが、
  実際に生成される群は推移的でない)そのものであり、caught bug の signature が
  実測でも再現したことを意味する(mutant が壊した wiring 自体の証拠ではなく、
  独立チェッカーが「モデルの主張と実際の群論的事実の乖離」を検出した、という意味での
  cross-check)。
- `search/sat/lrat_check.py --cnf search/sat/runs/n21_m10_depth19/problem.cnf --lrat search/sat/runs/n21_m10_depth19/proof.lrat.gz`
  → `s VERIFIED`(`lines_processed=2`, `elapsed_seconds=0.102`)。drat-trim(CI・
  `drat_verify.txt` の `s VERIFIED`)とは別実装による独立再照合、一致 —
  cross-checked(検証済みではない)。
- `node search/sat/check_model_n21.mjs --mode transitive --model search/sat/runs/n21_m10_depth20/model_vlines.txt`
  は **対象外**: このフィクスチャの X/D/B は宣言のみで未使用(実 witness に配線
  されていない)。チェッカーは X/D の one-hot 制約を仮定して復号しようとするため
  全 21 行で「両方 true」の矛盾を報告し `ok:false` になるが、これはフィクスチャの
  正しさ(固定 path グラフの BFS 到達性)とは無関係な、チェッカーの前提が合わない
  ことによる `ok:false` である。生出力は `check_model_output.txt` に保存し、
  「対象外」の理由を明記した。

## 未収蔵・既知の欠落

- `core.cnf.gz`(UNSAT core)は artifact に含まれ収蔵済みだが、本台帳作成時点では
  中身の独立監査(core だけを使った再照合)は行っていない — 将来の theorem run 昇格時の
  次段候補。
- class run はそもそも SAT のため `drat_verify.txt` / `proof.lrat` は存在しない
  (`proof.drat` はソルバーが `--no-binary` で常時出力するが、SAT verdict では
  drat-trim による検証ステップ自体が走らない設計 — `search/sat/README.md` のパイプライン図
  参照)。

---

# 追補: n=25 ell=17 2-transitivity 標的(裁定 210 系・commander task・Sol 便 84 sec 6.3)

## Run metadata

| | class run | 2transitive(depth=5)run |
|---|---|---|
| GitHub Actions run ID | `30467980820` | `30467990745` |
| workflow | `sat-run` | 同左 |
| workflow_dispatch `run_label` | `calibration` | `calibration` |
| CNF input | `search/sat/out/a25_class.cnf` | `search/sat/out/a25_2transitive_depth5.cnf` |
| CNF sha256(`search/sat/manifest_a25.json` と一致) | `9422163fcf9aab843cb1ecfd31ef6f2fde02560ddc29770585a9628ebf389f2a` | `0408f2d67ab3d64a12032299bd8355715b58a7942ba3f671d9bd82890bfa3286` |
| CNF sha256 再計算(artifact 内 `problem.cnf`) | 同上 — **一致** | 同上 — **一致** |
| verdict(`result.txt` 原文) | `exit=10` / `verdict=SAT` | `exit=20` / `verdict=UNSAT` |
| kissat wall time | 0.00s(即座、`kissat_time.txt`) | UNSAT verdict 到達まで含め run 全体 12m47s |
| drat-trim 検証(UNSAT のみ) | N/A(SAT run) | `s VERIFIED`(`943526/1898102` 節が core、`464638/1604226` lemma が core、`95172296` resolution steps、検証時間 467.971 秒) |
| 独立照合(`check_model_a25.mjs`、encoder 非 import) | class 側 6 項目 **全 true**(a 型 2¹²1・model B と再計算 b の一致・b³=1・固定点ちょうど 1・b 型 3⁸1) | 未実施(UNSAT のため decode 対象モデルなし) |
| local storage | `search/sat/runs/a25_class/` | `search/sat/runs/a25_2transitive_depth5/` |

## 解釈上の注記(depth=5 の非情報性)

`a25_2transitive_depth5.cnf` の UNSAT は **「点対 (1,2) から 5 手(対角生成元 3 個の
BFS)以内には 600 個の順序対全てへ到達する解が存在しない」という事実**のみを証明する
(drat-trim 独立検証済み)。depth=5 は独立に発見済みの実 witness の真の直径 43
(`search/sat/fixtures/witness_a25_2transitive.json`)よりはるかに浅いため、
**この UNSAT は 2-transitivity の非存在の証拠にはならない**(`mutants_a25.json` M5 に
事前登録済みの通り)。存在問題そのものは、この SAT run とは独立に、直接構成
+ 無制限 BFS による Python 照合で既に解決している(下記コミットメッセージ・README 参照)。

## 除外ファイル

`search/sat/runs/a25_2transitive_depth5/proof.lrat.gz`(260,287,433 バイト、sha256
`bd251e9b83a3831d5856be23a4ea623cd43d41a84609d06fd4dd17f64d7a4d1f`)は GitHub の
1 ファイル 100MB 上限を超えるため commit していない — 詳細は同ディレクトリの
`NOTE.md`。`proof.drat.gz`(21,039,286 バイト)・`core.cnf.gz`(4,179,187 バイト)は
committed。
