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

## 未収蔵・既知の欠落

- `core.cnf.gz`(UNSAT core)は artifact に含まれ収蔵済みだが、本台帳作成時点では
  中身の独立監査(core だけを使った再照合)は行っていない — 将来の theorem run 昇格時の
  次段候補。
- class run はそもそも SAT のため `drat_verify.txt` / `proof.lrat` は存在しない
  (`proof.drat` はソルバーが `--no-binary` で常時出力するが、SAT verdict では
  drat-trim による検証ステップ自体が走らない設計 — `search/sat/README.md` のパイプライン図
  参照)。
