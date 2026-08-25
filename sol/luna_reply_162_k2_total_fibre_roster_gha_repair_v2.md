# Luna 162: K2 total-fibre roster GHA repair v2

## 1. 結論と限定

run `32810928194` の full Python が即時終了した最初の例外を再現し、原因を convention 層まで分離した。

```text
D972_K2_TOTAL_FIBRE_ROSTER_INPUTS_PASS count=13
RuntimeError: STATE_STOP TARGET_WORD_REPLAY: 81
```

zero-based row 81 では、凍結 roof word artifact の target G9 座標と旧 replay は次のように食い違う。

```text
target G9 = ((0,0),(0,0),(7,0))
v1 G9     = ((0,0),(0,0),(2,0))
v2 G9     = ((0,0),(0,0),(7,0))
PSL replay match = true
word length = 20
```

全972行の軽量 replay census は `v1 G9 mismatch=810`, `v2 roof G9 mismatch=0`, `PSL mismatch=0` である。v2 は **凍結 roof target word の G9 認証だけ**を compact word-key 規約へ分離した。K2 raw-fibre の生成、G36 source-word replay、predicate、reduction law、fixed-row36 lineage は変更していない。

これは producer-side の機械的修理であり、独立 cross-check でも数学的 claim の promotion でもない。full v2 はローカルでは走らせておらず、valid 総数と histogram は未観測である。`1944` または「各 target 2点」を acceptance に仮定していない。

run `32810606023` の欠品失敗は、親側が exact 5 dependencies を commit `059c9470` で追加した後に解消したものとして扱う。本便では git/GHA 操作をしていない。

## 2. 原因

固定 row36 K2 producer が登録した dihedral 座標は `[a,e]=r^a s^e` で、marked generator は

```text
y_K2 = ((1,1),(1,0),(1,1)).
```

一方、972-row の凍結 word-key artifact は compact permutation marking から word を直列化しており、その D9 decoder では `sr=r^-1 s` なので

```text
y_roof = ((-1,1),(1,0),(-1,1)) mod 9.
```

row36 はこの差を露出しないが、row81 が最初に露出する。v1 は target artifact 自身の認証にも `y_K2` を使ったため fail-closed した。v2 adapter は `eval_word_g(word,9)` の target-authentication 呼出しだけを `y_roof` へ dispatch し、modulus 36 の全呼出しは pin 済み v1 implementation のままにする。v1 core 内で modulus 9 の `eval_word_g` 使用箇所は全 target の事前認証一箇所だけである。

## 3. versioned repair assets

| path | bytes | SHA256 |
|---|---:|---|
| `search/d972_k2_total_fibre_roster_producer_v2.py` | 9776 | `a6af98f3f2707e4812a66568c8679b3c5fad4671e764f9c33d194743c0a41411` |
| `search/d972_k2_total_fibre_roster_gha_v2.g` | 10021 | `3e09d31ff6911a08421c6bd934c56bb1303ed011719f43891721ed2cddb30682` |
| `sol/luna_reply_162_k2_total_fibre_roster_gha_repair_v2.md` | self | not self-pinned |

producer v2 は v1 core を byte/SHA pin して明示的に再利用する adapter である。result schema は `d972-k2-total-fibre-roster-producer/v2`、claim ID は `K2-TOTAL-FIBRE-ROSTER-OVER-X-V2` となる。result 内にも v1 core pin、lineage、二つの word convention、810/0/0 診断、`K2_predicate_or_reduction_law_changed=false` を保存する。

## 4. pin audit

v2 Python は従来13入力を v1 core 経由で認証し、さらに v1 core 自身を result の `input_pins` に追加する。GHA wrapper は v2 source、v1 core、従来13入力、既存 workflow をすべて再 pin する。

| path | bytes | SHA256 |
|---|---:|---|
| `search/d972_k2_total_fibre_roster_producer_v1.py` | 44829 | `cc518377347988c5ad531d0d5c0c5410d2c050a91439ccb27db6414ffae9c499` |
| `search/d972_rung_ordinary_idx3_producer_v2.py` | 54993 | `b8dd453f7647dacc87356b13cb5428674a21bfabe6aa5af3850ac89129eb7211` |
| `search/certs/nf972_sourcemap_a_tuples_v2_20260804.json` | 43751 | `cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801` |
| `search/certs/d972_b4_word_key_artifact_v1_20260816.json` | 176474 | `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9` |
| `search/certs/d972_rung_ordinary_idx3_prereg_v2_20260824.json` | 46928 | `1273f6050afaaba01f8dc137042ae191cecd91dea44a1618f665c2e3048e4656` |
| `ci/ordinary_idx3_artifacts_32682548731/d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json` | 62680 | `48512270d265753944ff9b86d19fa5e84095ffffd8ae78beba969088c31053e9` |
| `search/certs/b3_gentle_source_census_preflight_v1_20260823.json` | 887124 | `c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2` |
| `crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json` | 4931 | `e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e` |
| `certificates/K36.v1.json` | 727834 | `feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719` |
| `crosscheck/verdicts/K36.v1.verdict.json` | 71093 | `4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b` |
| `certificates/K9.v1.json` | 173224 | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` |
| `crosscheck/verdicts/K9.v1.verdict.json` | 20991 | `9c299baba6cd3c49296621ecfe5efbc260d7971fa874f44465fa5e968cc065f9` |
| `certificates/S4.v2.json` | 287984 | `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d` |
| `crosscheck/verdicts/S4.psl.verdict.json` | 470 | `8d9d98965e270c2130b56fd6240c3b7460fe906ef5523f5e90396280dd043b28` |
| `.github/workflows/gap-run.yml` | 11346 | `7e732a4edf49306e18067b1003b8495c858bfae79ade8855c49488bb7e4dd763` |

全 pin は本便の静的監査時に bytes/SHA 一致を確認した。

## 5. lightweight local checks

実行した範囲は preflight/selftest/parse のみである。

```text
python -B search/d972_k2_total_fibre_roster_producer_v2.py --preflight
D972_K2_TOTAL_FIBRE_ROSTER_V2_PREFLIGHT_PASS targets=972 v1_g9_mismatches=810 first_v1_mismatch=81 v2_roof_g9_mismatches=0 psl_mismatches=0 core_sha256=cc518377347988c5ad531d0d5c0c5410d2c050a91439ccb27db6414ffae9c499

python -B search/d972_k2_total_fibre_roster_producer_v2.py --selftest
D972_K2_TOTAL_FIBRE_ROSTER_CORE_V1_SELFTEST_PASS mutations=8 small_component_cases=6 inputs=13
D972_K2_TOTAL_FIBRE_ROSTER_V2_SELFTEST_PASS targets=972 v1_g9_mismatches=810 first_v1_mismatch=81 v2_roof_g9_mismatches=0 psl_mismatches=0 convention_mutant_rejected=true core_sha256=cc518377347988c5ad531d0d5c0c5410d2c050a91439ccb27db6414ffae9c499
```

- Python AST parse: PASS.
- GAP 4.16.0 `ReadAsFunction` parse-only: PASS。通常の top-level unbound-global syntax warnings のみで、syntax error はない。
- GHA wrapper ASCII-only audit: PASS.
- v2 source pin embedded in wrapper: PASS.
- full v1/v2 result は作成されていない。
- 一時 parse driver と生成された exact v2 pycache は削除済みで、persistent path は第3節の3本だけである。

## 6. GHA failure visibility and fail-closed gates

v1 wrapper は Python が非零終了すると `.ok` 欠品だけを外側の run log に出し、redirect 済み traceback を見せなかった。v2 は selftest/full の各 subprocess log を `ci/out/` に保持し、exit sentinel 不一致または forbidden diagnostic の際に内容全体を次の区間で外側の `run.log` に必ず転記してから `Error` する。

```text
D972_K2_TOTAL_FIBRE_GHA_V2_FAILURE_LOG_BEGIN phase=selftest|full|diagnostic ...
<captured Python log>
D972_K2_TOTAL_FIBRE_GHA_V2_FAILURE_LOG_END phase=selftest|full|diagnostic
```

成功時も、pin、selftest marker cardinality、`810/81/0/0` 診断、subprocess exit sentinel、forbidden diagnostics、producer terminal exact-one、result terminal exact-one、schema/status/coverage、`complete=true`, `no_early_stop=true`、repair scope、非仮定 acceptance を順に fail-closed で検査する。

想定 result/log paths:

```text
ci/out/d972_k2_total_fibre_roster_v2_20260825.json
ci/out/d972_k2_total_fibre_roster_v2_selftest.log
ci/out/d972_k2_total_fibre_roster_v2_full.log
```

terminal markers:

```text
D972_K2_TOTAL_FIBRE_ROSTER_V2_SELFTEST_PASS
D972_K2_TOTAL_FIBRE_ROSTER_PRODUCER_V2_FINAL
D972_K2_TOTAL_FIBRE_ROSTER_GHA_V2_FINAL result=ci/out/d972_k2_total_fibre_roster_v2_20260825.json python_terminal_count=1 result_terminal_count=1
```

## 7. dispatch contract

既存 `.github/workflows/gap-run.yml` に渡す値:

```text
script: search/d972_k2_total_fibre_roster_gha_v2.g
preamble: <empty>
out_dir: ci/out
timeout_min: 120
with_pquot_packages: false
```

full の所要時間と valid roster 規模はまだ未観測なので、v1 の推定を結果として再掲しない。GHA result が final marker まで完走して初めて producer candidate artifact として受理できる。

`K2_TOTAL_FIBRE_ROSTER_GHA_REPAIR_V2_READY`
