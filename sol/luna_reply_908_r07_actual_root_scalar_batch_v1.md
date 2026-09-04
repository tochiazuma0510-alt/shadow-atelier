# Task908 — actual four-character root scalar batch v1

実装・bounded 検証・workflow を完了した。Task913の修理は指定の3ファイルだけに適用し、workflowは変更していない。GHA/Git と実データ本走査はこのセッションでは実行していない。

## 固定した親

- P1: run/attempt `33851744070/1`, head `6673eb2ea15ca6022acc2ddc5a8a204a0380172f`, artifact `9931437113`, `641518300` bytes, `sha256:6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c`。
- Task554: run/attempt `33677346616/1`, head `22c6dddb43d107c05e65f53ad898823ae8ebe276`, accepted conclusion `completed/failure`; prepare + four block artifact identity/size/digest を workflow で全照合する。
- Task712: run/attempt `33814194630/1`, head `5ff2c5a30b604536df12acba8801828a5a7e5fe0`, artifact `9915928157`, `sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858`。
- separator: run/attempt `33891714539/1`, head `7b7b9de20faaa3b8f26e331bb738b374f6f5708c`, artifact `9944214057`, `sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017`。

実装は P1 cache を1回だけストリーム走査し、active な character 0 の root+4 actor の5 sparse packed projectionだけを計算する。character 1–3 は認証済み exact zero として保持する。Task554 は prepare と block を一つずつ開き、offset 付きの 44 seed + `4*8059` actor = `32280` 個の uint8 accumulator へ直接 fold し、巨大な global relation tree/raw body duplicate は作らない。relation receipt は5 body digest、ranks/offsets、actor order、`8232` origins、`32280` relations、evaluator version による固定 digest (`47effc68794b6d5d9616d5378396a7f10a5d9e0412bfe2ccf95c7e67b1fcf8dc`) とした。

actual preflight の固定 root/child は char0 support `2742`, lead `3`, lead value `2`, root packed SHA `af62027aa99fbd1a4b7b53c6b380b4e7fa7403915ea91f9d51d7cb2198c7e053` と4 child SHAをコードへ固定し、char1–3 の root/child は全て zero SHA `8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838` とした。root EOF の normalized state は raw q、scale、normalized packed SHA、prior zero state、`_dual_next_state_head` による next-state head、future orbit bound `504`/remaining independent `503` を含む。

## 検証

```text
python -m py_compile search/d972_r07_actual_grade2_root_scalar_batch_v1.py search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py   PASS
python -u search/d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest             PASS
python -u search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py --selftest       PASS
```

両 selftest は sparse-vs-dense の4 offset、vectorized chunk（短い最終 chunk を含む）と20値 batch equivalence、実際の二つの非空block/four-slot accumulator、全 `32280` origin EOF scan、seed/actor ordering、zero/all-four EOF、separator/Task712/P1/Task554 validator mutationを実行する。checkerはcoherently resealed relation/child/prefix/terminal-claim/result-joinを完全比較ゲートへ通して拒否し、canonical launch fileを`validate_launch`へ通してauthenticated raw SHAをhandoffする。real 641 MB P1 object のローカル parse/run はしていない。

workflow marker は `[task908-r07-actual-root-scalar-v1]`、job cap は90分、producer/checker cap は各40分。artifact metadata（repository/run/attempt/head/status/conclusion、全 artifact id/name/archive bytes/digest/expiry/repository linkage）を download 前に照合し、producer と checker の双方が成功した時だけ candidate artifact を公開する。diagnostic logs は常時保存する。

## ファイル receipt

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_actual_grade2_root_scalar_batch_v1.py` | 78662 | 1361 | `aa76f1ff16314f6e3b6253d3d0276a21934ae493c0bd0318065ec73c50b98d72` |
| `search/check_d972_r07_actual_grade2_root_scalar_batch_v1.py` | 81753 | 1321 | `dea105cd8c196565d95c6828c4afdfdd7f1d6395b5d85dfb7d3447fdfe4f0fa2` |
| `.github/workflows/d972-r07-actual-grade2-root-scalar-batch-v1.yml` | 23735 | 433 | `cfa9814863e2c61db3158b5940854b72e9c0cd0bbd4b0ab53ea4a29fa7a238c3` |

The reply is the receipt document itself and is therefore not self-hashed.

Claim boundary remains:

```text
ROOT_SCALAR_BATCH_CANDIDATE=true
COMPLETE_DUAL_ORBITS=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```

READY_FOR_SOL_REAUDIT=yes
