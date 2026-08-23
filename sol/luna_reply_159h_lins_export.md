# Luna 便 159h — LINS marked strictness export

STATUS: READY_FOR_PARENT_BROKER_GHA_DISPATCH

FULL_RESULT: UNKNOWN_NOT_YET_DISPATCHED

`ops/inbox_codex/sol_task_159h_next_axis.txt` の「次の判別軸」2 を処理した。既存
LINS-2000 twin 証明書を marked-map 証明書へ再ラベルせず、全 node を同じ 1 回の
`LowIndexNormalSubgroupsSearch(B3,2000)` 内で再構成する versioned producer を新設した。
子 agent は契約どおり commit / push / credential / workflow dispatch を行っていない。

## 1. 固定宇宙と CLAIM-COVER

production 宇宙は

```text
B3=<sigma1,sigma2 | sigma1 sigma2 sigma1=sigma2 sigma1 sigma2>
one LowIndexNormalSubgroupsSearch(B3,2000) call
identity node 1 を除く全 4,265 nonidentity nodes
```

である。full mode は `nodes_total=4266`, `identity_nodes_excluded=1`,
`nonidentity_rows=4265` の三値を fail-closed に要求する。一つでも異なれば output を完成させない。
bound を下げた preflight は `claim_cover.complete=false` とし、4,265 行の悉皆を名乗らない。

各 row は LINS 訪問順ではなく canonical generator-word set の SHA256 で整列する。node-id の重複も
fail-closed である。したがって full artifact が `ALL_DONE` まで到達した時に限り
`CLAIM-COVER = 4265/4265` を主張できる。現段階では未走行なので CLAIM-COVER は **OPEN / UNKNOWN**。

## 2. marked map / Core / joint image の exact typing

LINS が返す各 `L` は定義上 `L normal B3` なので

```text
Core_B3(L)=L.
```

これを abstract `IdGroup` の一致から推定せず、各 row で normality を検査し、同じ canonical
generator words を `core_B3_L` に保存する。有限商 `q_L:B3 -> B3/L` を permutation group に移し、

```text
q_L(sigma1), q_L(sigma2),
q_L(x)=q_L(sigma1)^2,
q_L(y)=q_L(sigma2)^2,
q_L(c)=q_L((sigma1 sigma2 sigma1)^2)
```

をすべて exact permutation string と degree とともに保存する。braid relation と `x,y,c` の
二通りの評価一致は row ごとに gate する。

roof は `M=K^(9) cap N_S4`。既存 component builder から compact marked model

```text
PB3/M = G9 x PSL(2,8),
|G9|=2,916, |PSL(2,8)|=504,
|PB3/M|=1,469,664,
c -> 1
```

を degree 36 で再構成する。各 node について

```text
J_F2  = <(x_M,q_L(x)),(y_M,q_L(y))>,
J_PB3 = <(x_M,q_L(x)),(y_M,q_L(y)),(1,q_L(c))>
```

を直接生成し、`K=M cap Core_B3(L)` に対して

```text
|J_F2| / 1,469,664  = [M_F2 : K_F2],
|J_PB3| / 1,469,664 = [M : K]
```

を保存する。両者の整除性も gate する。これにより `PB3_CENTER_ONLY` と `STRICT_F2` を分離し、
`L != 1`、同じ `IdGroup`、twin label のどれも F2 真細分性の代用にしない。

各 row の source digest は canonical node id、index、permutation degree、marked
`sigma1,sigma2,x,y,c` を結合した bytes の SHA256。全 sorted rows にも集約 SHA256 を付ける。

## 3. versioned files

| path | bytes | SHA256 |
|---|---:|---|
| `search/lins_marked_strictness_export_v1.g` | 14,402 | `e2c1182994bde5b6f5db4c4fa71aeb2c55c13cda9798d95cf6fdea4df3f34b86` |
| `search/certs/lins_marked_strictness_export_manifest_v1_20260823.json` | 4,347 | `c12b3874d1319fa285d898328d6ae656549b441473a590f23b53cbf3cc03809d` |

producer が hard-pin する既存 census は 3,395,546 bytes、SHA256
`d0832df8a4e61adff45c5c24c8eba32f5d388f55412907ed5ffdf714b2b4b958`。
ただしこれは provenance anchor であり、旧 476 twin-pair inventory が 4,265 marked rows を保存したと
読み替えていない。producer 自身、共通 helper 3 本、output prelude、既存 workflow の digest は execution
manifest に列挙した。

## 4. local preflight

bound 12 と bound 8 の二回を `gap.ps1` 経由で試みたが、どちらも script parse 前に local GAP runtime が

```text
fatal error - couldn't create signal pipe, Win32 error 5
```

で終了した。従って syntax/runtime preflight は **UNKNOWN_ENV_BLOCKED**。これは数学的陰性ではない。
一時 output は生成されず、production 値も一切得ていない。

## 5. 親 broker 用 GHA launch 契約

既存 workflow は変更しない。

```text
workflow name/path : gap-run / .github/workflows/gap-run.yml
workflow SHA256    : 7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763
branch/ref         : koubou158/m2-msweep-v5-gha
script             : search/lins_marked_strictness_export_v1.g
preamble           : LINS_MARKED_OUTPUT:="ci/out/lins_marked_export/lins_marked_strictness_export_v1_20260823.json";;
out_dir            : ci/out/lins_marked_export
timeout_min        : 240
with_pquot_packages: false
marker             : [fire] を付けない
```

exact argv は manifest の `gha_dispatch.gh_cli_argv` に保存した。期待 artifact は `gap-run-out`、必須 payload は

```text
ci/out/lins_marked_export/lins_marked_strictness_export_v1_20260823.json
ci/out/run.log
ci/out/driver.g
```

であり、log の必須終端は `LMEV1_OUTPUT`, `LMEV1_SUMMARY rows=4265`, `ALL_DONE`。

既存 LINS-2000 実績は LINS 本体 616,926 ms、旧 twin pairing 込み 2,846,337 ms。この exporter は
4,265 個の exact joint-image order を追加するため 60–180 分を見積もり、240 分 cap とした。timeout / runner
資源切れは `UNKNOWN_RESOURCE` であり、strict source の不存在を意味しない。

## 6. publish 注意

観測時点の branch は `koubou158/m2-msweep-v5-gha`、remote tip は
`fbd427a8328a8d4e221cc05b821d027b0f2ac3f0`。local branch は remote に対し diverged しており、通常の
push は reject の見込み。親 broker は上記 producer と manifest の二ファイルだけを remote tip の子 commit
へ選択的に載せ、fast-forward push してから dispatch する必要がある。dirty worktree の既存 user changes や
workflow files を commit に混ぜてはならない。

run id と dispatched commit SHA は未発行なので `null`。親 dispatch 後、最終返書には両方を記録すること。

## 7. claim level

現在成立したのは schema と producer の **candidate / static-audited** 段だけである。full 4,265-row artifact は
未走行、独立 checker も無く、cross-checked でも Lean verified でもない。最初の欠品は

```text
GHA_RUN_ID_AND_COMPLETE_4265_ROW_ARTIFACT
```

である。
