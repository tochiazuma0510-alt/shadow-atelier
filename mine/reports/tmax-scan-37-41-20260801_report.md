# mine 検収レポート -- tmax-scan-37-41-20260801

- 生成: 2026-08-01T03:40:33.274932+00:00(UTC)
- plan: `mine/jobs/queue/tmax-scan-37-41-20260801.json`
- artifact-dir: `scratchpad/mine_dl/tmax-scan-37-41-20260801`
- claim_class: `exploration`
- checker cert 出所: (plan.crosscheck.checker_certs_glob 未指定)

machine-piped 規約: 本レポートは cert JSON の値のみから生成した。run.log は参照していない。

## 分類不能な json (2 件 -- artifact-dir 内の無関係な cert。内容は表示しない、パスのみ)

- `scratchpad/mine_dl/tmax-scan-37-41-20260801\mine-run-tmax-scan-37-41-20260801-ell37\mine\out\tmax-scan-37-41-20260801\ell37\tmax_scan_37_ell37_20260731.json` (schema/generated_by が本ジョブの様式と一致しない)
- `scratchpad/mine_dl/tmax-scan-37-41-20260801\mine-run-tmax-scan-37-41-20260801-ell41\mine\out\tmax-scan-37-41-20260801\ell41\tmax_scan_41_ell41_20260731.json` (schema/generated_by が本ジョブの様式と一致しない)

## (a) 再現照合 -- artifact cert ⟷ repo 収蔵済み cert(同名ファイル)

較正再走の合否: 主要欄が全一致すれば `REPRO_MATCH`、1つでも不一致があれば `REPRO_MISMATCH`。volatile 欄(elapsed_sec 等)は参考列で判定には数えない。

(artifact 内に GAP explorer window cert が見つからなかった)


## (b) 対付け集計 -- GAP explorer cert ⟷ python checker cert

(対付け対象の窓が見つからなかった)

## 集計まとめ

- 再現照合: 0/0 REPRO_MATCH
- 対付け: agreement 0/0(全窓数 0)

(この集計は候補表記であり、裁定・LEDGER 貼付・地図 delta の確定は人が行う。)

## 付記(collector v0 未対応スキーマの直接抽出 -- machine-piped)

collect.py v0 の `classify()` は tmax-scan 系 cert(`wac_v1-tmax-scan-cert/v1`)を未対応のため上記 (a)/(b) は 0/0(tmax-scan-20260731 の先行ジョブと同様)。以下は cert JSON をその場で python で再パースした値(手入力なし、抽出スクリプト `scratchpad/extract_tmax_37_41.py`)。

### CI run / result.txt(両 shard とも machine-piped key=value)

| shard | verdict | gap_exit_code | run_id | DRIVER_DONE marker (run.log) |
|---|---|---|---|---|
| ell37 | done | 0 | 30682335065 | 検出(1件) |
| ell41 | done | 0 | 30682335065 | 検出(1件) |

### cert 出所・完走性

- `ell37`: `mine/out/tmax-scan-37-41-20260801/ell37/tmax_scan_37_ell37_20260731.json`(sha256 = `96e9a6d16ce2970973fb4272c61b3a09bd3aae5eefa47f1143c549207641c67f`)-- `total_time_cap_hit=false`、`ell_time_cap_hit=false`(t=0..18 全 19 点を cap 未超過で完走)。
- `ell41`: `mine/out/tmax-scan-37-41-20260801/ell41/tmax_scan_41_ell41_20260731.json`(sha256 = `acef861defde5a452dc2540b2aa9568e00a5dd4617b3213763c0bfb449525232`)-- `total_time_cap_hit=false`、`ell_time_cap_hit=false`(t=0..20 全 21 点を cap 未超過で完走)。

### 段階別内訳(t, stage) -- cert からの機械転記

**ell=37**(t_range 0..18):

| t | n | stage |
|---|---|---|
| 0 | 37 | HIT |
| 1 | 38 | HIT |
| 2 | 39 | GEN_FAIL |
| 3 | 40 | HIT |
| 4 | 41 | GEN_FAIL |
| 5 | 42 | GEN_FAIL |
| 6 | 43 | GEN_FAIL |
| 7 | 44 | GEN_FAIL |
| 8 | 45 | GEN_FAIL |
| 9 | 46 | BUDGET_FAIL |
| 10..18 | 47..55 | BUDGET_FAIL(全て) |

**ell=41**(t_range 0..20):

| t | n | stage |
|---|---|---|
| 0 | 41 | HIT |
| 1 | 42 | GEN_FAIL |
| 2 | 43 | GEN_FAIL |
| 3 | 44 | GEN_FAIL |
| 4 | 45 | HIT |
| 5 | 46 | GEN_FAIL |
| 6 | 47 | GEN_FAIL |
| 7 | 48 | GEN_FAIL |
| 8 | 49 | GEN_FAIL |
| 9 | 50 | BUDGET_FAIL |
| 10..20 | 51..61 | BUDGET_FAIL(全て) |

### HIT 一覧(witness literal 込み・cert からの機械転記)

| ell | t | n | k | j | gen | braid_holds | centralizer_w0 |
|---|---|---|---|---|---|---|---|
| 37 | 0 | 37 | 14 | 11 | A_n | true | size=37, `C37`, solvable, derived_length=1 |
| 37 | 1 | 38 | 18 | 11 | A_n | true | size=37, `C37`, solvable, derived_length=1 |
| 37 | 3 | 40 | 20 | 12 | A_n | true | size=222, `C37 x S3`, solvable, derived_length=2 |
| 41 | 0 | 41 | 20 | 11 | A_n | true | size=41, `C41`, solvable, derived_length=1 |
| 41 | 4 | 45 | 22 | 14 | A_n | true | size=984, `C41 x S4`, solvable, derived_length=3 |

**S₇ 型窓(核 C_ℓ×S₇)の HIT**: **無し**。今回の HIT で観測された最大の対称因子は `S4`(ell=41, t=4, |C(w0)|=984)。t=2 以降の大半(ell=37: t=2,4-8 / ell=41: t=1-3,5-8)は `GEN_FAIL`(予算・パリティは可行だが 2-opt Hunt 予算内で A_n/S_n 生成対を未発見 -- 陰性主張ではなく UNKNOWN)であり、`BUDGET_FAIL` に達する前(ell=37: t=9〜、ell=41: t=9〜)に生成の壁が先に立ちはだかっている。

### t_max 閉形(5t ≤ ℓ+6−6δ(n))との照合について

**照合は未実施として上申する(事実提示に留める)**。理由: `docs/notes/tmax_budget_and_holes_v1.md` の δ(n) 早見表(n mod12 表)を用いて ell=37,41 の budget 境界を再計算しようと試みたが、同ノート内の代数定義 δ(n)=(n mod4)/2+(2/3)(n mod3) から機械的に再計算した 6δ(n) の値と、ノート掲載の早見表の値が n mod12 ∈ {1,2,5,6,9,10} で食い違った(例: n mod12=9 のとき、早見表は 6δ=13 だが代数定義からの直接計算では 6δ=3(実際 ell=37,t=8, n=45 の cert 実測は budget_feasible_k=[22]=非空 -- BUDGET_FAIL でない -- であり、6δ=3 側の予測(feasible)と整合、6δ=13 側の予測(infeasible)とは不整合)。この不一致がノート早見表の転記誤りか、miner の再計算の誤りかは判定しない(数学の再導出は職務外)。**生の段階別内訳表(上記)を一次情報として提示し、閉形との突合自体は司令塔/数学者に委ねる。**

### 結論(事実記載のみ・的中/外れ・段2要否の裁定は司令塔)

- 両 shard とも `verdict=done`・`gap_exit_code=0`・`DRIVER_DONE` マーカー検出・`total_time_cap_hit=false`(自己上限 170分に対し余裕を持って完走)。
- HIT 5 件(ell=37×3, ell=41×2)、いずれも witness(`a1`/`b1`/`braid_holds=true`/centralizer 構造)が cert に収録済み。
- **S₇ 型窓は本ラウンドでは未発見** -- 段2(初の S₇ 型窓 wall cert 起票)は**現時点では起票の根拠なし**。GEN_FAIL が t の早い段階(ell=37: t=2 で早くも初出)から支配的であり、より広い 2-opt 予算での再走(TMAX_MAXRESTART/TMAX_MAXSTEP 拡大)か、S₇ 型に達するさらに大きい ell への拡張が必要かは数学的判断(司令塔/数学者)に委ねる。
- δ(n) 早見表と代数定義の不一致(上記)は、既存 86 行照合(ell 11..31)の結果自体を疑うものではない(その照合は別スクリプトで別途 0 不一致と記録済み)が、ell=37,41 の新規データへ closed-form を適用する際は表の再検証が要る旨、上申する。
