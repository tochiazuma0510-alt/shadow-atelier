# Sol 便 123 返信 — R-3 / U3-2 / U3-3

作成: Sol / 2026-08-13  
対象: `ops/inbox_codex/sol_task_123_r3_unram.txt` §0–§4 全項  
格: exact producer + helper 非共有 checker による cross-checked。Lean verified ではない。

## 0. 実行境界

- 正本 `docs/notes/r2_r3_unram_execution_spec_v1.md` の SHA-256 は指定値 `da6294da1b2f359f3b80f2281570770e4db616a360a9896bc5fc6ca1055f1c26` と一致した。
- run ID: `sol123-local-20260813-v1`。
- 実行順は R3 producer → R3 checker → U3 producer → U3 checker。U3-3 artifact は R3/DESC-9 測定後にのみ生成した。
- 1 段 120 秒の hard-timeout と段別 atomic checkpoint を使用した。全 4 段は timeout なしで終了し、同一 run の再実行で全 cert hash が不変だった。
- `u` は [R-3-U9] により touched、`c` は untouched。`d_9` と `r` は未計算。封印中の K5 instance は未接触。
- 本文では blind 測定値、U3-3 の値と support、およびそれらの解釈を開示しない。

## 1. [R-3-U9] / DESC-9

状態: `CROSS_CHECKED`。

producer は生の二式に含まれる垂直成分を使わず、対象枝で `w+1` を単元として `Y` を消去した飽和局所式

```text
F = X^2*w^6 + 81*X*w^3*(w+1) + 54*w^3*(w+1) - 729*X*(w+1)^2
```

を用いた。`F = 729*(w+1)^2*E(X,Y(X,w))/X^2` と原点での `dF/dX != 0` を exact に確認し、`Fraction` 演算で次数 30 まで展開した。`E`、`W`、`F` への代入残差はいずれも同次数まで 0。

有理 uniformizer は `s_1=w` と `s_2=X/w^2` の非比例な 2 本を使用し、両経路の主係数の比が 18 乗であることを確認した。後着の工房 R-2 cert `search/certs/r2_u_uniformizer_v1_20260813.json`（SHA-256 `496c494c4299d91f0d610360bccfac7f56a91c08fe2ec44ce00695e275cafb65`）とは、Sol 測定 hash 固定後の第三レール照合で一致した。

DESC-9 は (D-i) 指数降下、(D-ii) 有理性検査、(D-iii) RES-INJ-9 による一意降下を順に実行した。[b] は在庫 rational を checker 内の trial division で独立に再因数分解し、指定された法 9 正規化および零指数を support から落とす規約と一致した。不一致時の分岐は `UNKNOWN` hard-stop として実装済み。

測定値、`a_class`、score-rule の生値は cert 内にのみ置き、本文では開示・解釈しない。

## 2. [U3-2]

- `D={0,1,infinity}` の非衝突: `COMPLETE`。三つの projective section の pairwise determinant は基礎環上の単元として確認した。
- 平滑性: `UNKNOWN_STOP_MODEL_NORMALIZATION_REQUIRED`。
- `D` 外エタール性: `UNKNOWN_STOP_MODEL_NORMALIZATION_REQUIRED`。

停止根拠は characteristic 依存ではない。宣言された affine complete intersection `E=G=0` は generic fibre 上で `X=Y=0, w arbitrary` を含む。その locus 上の 2×3 Jacobian は

```text
[ 0,          2, 0 ]
[ 0, -27*(w+1), 0 ]
```

で rank 1 となり、全 2×2 minor が消える。従って有限個の整数素点を反転しても、この宣言 raw model 自体を平滑にはできない。spec に記された `G` 単独の偏微分 ideal は ambient hypersurface `G=0` を検査するもので、`E=G=0` の complete-intersection rank 条件にはならない。

局所飽和式は R3 の対象枝を与えるが、これを global normalized finite model と同一視していない。U3-2 の再開入力は、`W -> P^1_t` の global normalized finite/projective model とその integral spreading-out である。これがないため relative-differential support の結論は出していない。

## 3. [U3-3] — 特別検閲

状態: `COMPUTED_QUARANTINED_INTERPRETATION_NOT_ASSERTED`。  
cert: `search/certs/sol123_u3_disc_v1_20260813.json`  
SHA-256: `d2f3b361d8bec47077c37017d26a9259d225c56daa9bea55b7a0306fb4af231e`

## 4. 再現・artifact

再現コマンド:

```powershell
python search\sol123_run.py
```

設計・実行 source:

| path | SHA-256 |
|---|---|
| `search/sol123_r3_u9.py` | `f1c48431aa095be584e57e771da512753d0b662414b2f1b74a1f2316e0c2dae5` |
| `crosscheck/check_sol123_r3_u9.py` | `233538f8686c66999eb28927cdf5954ced264f3353636dd6aa4eec8e2824b710` |
| `search/sol123_u3_geometry.py` | `8d6a43137d6108be56701f2b5e92964c4dec606f7b4152e42f720f5b06097073` |
| `crosscheck/check_sol123_u3_geometry.py` | `095ea19566abb085e550189e1d0e9ef062d7bd4399e9b636ca6ebb342b73f707` |
| `search/sol123_run.py` | `585e1da97a97a4dc196c2be75059625fd0a4739ab1ba40eb7349b6ff0732b9d7` |

cert / checkpoint:

| schema / status | path | SHA-256 |
|---|---|---|
| `r3_u9/v1` / `COMPLETE_PRODUCER` | `search/certs/sol123_r3_u9_v1_20260813.json` | `cbbf5c91c5fe664d218056dae1f03a2262da53da0628a156fae6b3d1fca731c4` |
| `p8_a_class/v1` / `COMPLETE_MEASUREMENT_INTERPRETATION_WITHHELD` | `search/certs/sol123_p8_a_class_v1_20260813.json` | `dd1cf38556d0eff58ab29f0cd47bf762df782c45c43e9b27741bba3e015210b8` |
| `r3_u9-check/v1` / `CROSS_CHECKED` | `search/certs/sol123_r3_u9_check_v1_20260813.json` | `6ecb944c93d373016d19a5e3ed32ce3266fcb772ea82cee1840691ebfcf50baf` |
| `u3_smooth/v1` / `UNKNOWN_STOP_MODEL_NORMALIZATION_REQUIRED` | `search/certs/sol123_u3_smooth_v1_20260813.json` | `0a605fb7f9ba258ee74294f6ea437b32af61b566d4cf44b29a2e021091e234d4` |
| `u3_disc/v1` / `COMPUTED_QUARANTINED_INTERPRETATION_NOT_ASSERTED` | `search/certs/sol123_u3_disc_v1_20260813.json` | `d2f3b361d8bec47077c37017d26a9259d225c56daa9bea55b7a0306fb4af231e` |
| `u3-geometry-check/v1` / `CROSS_CHECKED_WITH_U3_2_UNKNOWN_STOP` | `search/certs/sol123_u3_geometry_check_v1_20260813.json` | `cb662e074b40f5fc0d06b04427940c5080a9316bc09d4d8843c77ad001ce51da` |
| `sol123-run-checkpoint/v1` / `COMPLETE_WITH_U3_2_UNKNOWN_STOP_RECORDED` | `search/certs/sol123_run_checkpoint_v1_20260813.json` | `c5e43507963fffb9eeaea0e0bdf218fb2252ab4053fc48b2a498ceea7f0ae790` |

## 5. NAME-COLLIDE / Git

- 事前 `Test-Path` で全 Sol-123 path が不存在であることを確認し、`sol123_*` namespace に限定した。sealed `u`/`c` の一般名をファイル名や一時変数名に再利用していない。
- 既存の dirty worktree の他ファイルは編集・stage していない。repository 内に追加したのは上表の source/cert/checkpoint と本返信だけ。
- 実行中に外部更新で base は `master` / `79346d5732c8b3d24389f058cd0e1c79db4d5edc`（`origin/master`）へ進んだ。
- branch 作成は `git switch -c sol/task-123-r3-unram` および flat fallback `git switch -c sol-task-123-r3-unram` の双方で `.git/refs/heads/*.lock: Permission denied`。このセッションの `.git` は read-only のため、artifact commit SHA は `NONE_PERMISSION_DENIED`、push と workflow dispatch は `NOT_EXECUTED`。外部 run ID はなく、上記 local run ID のみ。

commit/push 再開時は、上表の 12 artifact と `sol/sol_reply_123_r3_unram.md` のみを明示 stage し、既存 dirty 差分を含めないこと。
