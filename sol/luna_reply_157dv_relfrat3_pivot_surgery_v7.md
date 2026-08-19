# 157dv reply — relative-Frattini pivot surgery v7

## 結果

指定された candidate 1（empty correction）専用・positive-only の v7 bundle を実装し、GHA 発射前の静的監査と combined differential selftest を完了した。v1--v6、q3、workflow、既存 receipt は変更していない。

固定した task は SHA-256
`115d2138bc3200a4677beaa6e20124d213b1ce579cd0b8f444c05608e22fed95`
（13,874 bytes）。成果物は次のとおり。

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_relfrat3_pivot_surgery_v7.py` | 270,743 | `a19c3353c5cfc6da8ad0b7d941ba94bde043c80e69e33c889c5710c897d7a757` |
| `search/check_d972_b345_relfrat3_pivot_surgery_v7.py` | 237,285 | `fbe033704180a808320c897c52613ca6847305dd85ddcd7a70aa825161e8bfa0` |
| `search/d972_b345_relfrat3_pivot_surgery_gha_driver_v7.g` | 14,146 | `1be0ec44674108a2f6319057ba18283206756cf2ef73bfe1e1e5896a6f893d8d` |

driver は上の producer/checker SHA を hard-pin し、frozen v1--v6 と q3 driver/source/artifact pins も保持する。terminal-count gate は PASS / INCOMPLETE / UNKNOWN_RESOURCE / UNKNOWN_INPUT の4種を exact に数える。

## 実装した有限手続き

1. q3 と frozen v6 算術/Fox data を同じ job 内で再構成し、BFS shortlex の 32,768 translations と11本ずつの全 D2 columns を fresh に再生する。v6 artifact を checkpoint として輸入しない。
2. acceptance は実行前固定の33本だけである：charming cofaces 5、hexagon cofaces 10、ordered A.18 pentagon 1、S relations 11、`S(T_i)=x_i` recovery 6。T relations 11 と `T(S_i)=x_i` 6 は exact quotient value を lossless に記録する diagnostic-only であり、false でも PASS を抑止しない。
3. 完全還元 blocker `b=(component,g)` に対し、同じ component の全 canonical base occurrence `h` を `(relator index, component, canonical h bytes)` 順に走査し、
   `t=g*h^-1`
   を exact に構成する。`t*h=g` を再生し、first-seen canonical bytes ごとに11 relator の complete block を永続 basis へ挿入して直ちに同じ candidate を再試行する。
4. `h^-1*g`、`g^-1*h`、right-translation の3誤向きは selftest と checker で拒否する。新しい column が blocker を含んでも、より小さい未登録 pivot が現れ得るため、no-progress／256-round exhaustion は INCOMPLETE のままである。
5. directed translation の section は全 element pool に付けない。persistent section は BFS/direct translations のみ、base D2 support prefixes は固定、candidate target prefixes は transient とした。blocker は target prefix から、または canonical-first の登録済み `t0=g*h0^-1` と `w_g=w_t0*w_h0` から回収する。回収不能は hard FAIL であり UNKNOWN へ落とさない。
6. section provenance は canonical E4 bytes に束縛した typed expression DAG（identity / signed generator / product / inverse / directly replayed flat word）で保持する。PASS では proof leaves から reachable な部分だけを typed little-endian/base64 arrays と SHA binding で出力する。checker は producer helper を import せず、各 expression、各 `t`、全11 translated columns、elimination/blocker/round order、packed proof DAG を独立再構成する。

追加 cap は task どおり rounds 256、translations 32,768、columns 360,448、expression nodes 131,072、edges 262,144。v6 の sparse/pool/DAG/word/RSS/wall caps は不変である。

## selftest と静的監査

許可された combined command の最終 corrective run は PASS：

```text
D972_B345_RELFRAT3_PIVOT_SURGERY_V7_PRODUCER_SELFTEST_PASS ... acceptance=33 diagnostics=17 ... terminals=4 ... hard_fail=1
D972_B345_RELFRAT3_PIVOT_SURGERY_V7_CHECKER_SELFTEST_PASS ... wrong_orientations=3 ... terminals=4 acceptance=33 diagnostics=17 expression_mutation=1
```

最初の試行は diagnostic-value field を追加した後の旧 int toy、最初の corrective は両方 involution だった退化 orientation toy だけで停止した。production predicate／search は未実行・未変更であり、最終 fixture は S4 の `g=(0 1 2), h=(0 3)` にして4つの orientation words が異なることを固定した。

静的には producer/checker AST、driver の ASCII-only、全3 file の trailing-whitespace、v1--v6/q3 pins、最終 producer/checker pin chain、4-terminal loop を監査した。ローカル production GAP、full producer、Git、GHA は実行していない。

## terminal と主張境界

- `B345_RELFRAT3_PIVOT_SURGERY_PASS`: この一つの registered empty-correction pair に対する literal relative-Frattini certificate のみ。
- `..._INCOMPLETE`: no-new exact translation または256 round exhaustion。非所属・障害ではない。
- `..._UNKNOWN_RESOURCE`: 登録 cap の exact bounded prefix。数学的否定ではない。
- `..._UNKNOWN_INPUT`: 外部 pin/schema/authenticated input の欠品・不一致専用。

すべての non-PASS は `unknown_not_obstruction`、`fixed_candidate_pivot_surgery_only`、`no_mathematical_obstruction_claimed=true`、`full_universe_claimed=false`、`negative_claimed=false`。この lane は candidate 1 限定・positive-only であり、将来の full-4,096 expression/Fox lane、uniform/cofinal iteration、global B4-A/B の代替ではない。

## GHA 提案入力と見積り

まず canary：

```text
D972_B345_RELFRAT3_PIVOT_SURGERY_V7_SELFTEST=true
D972_B345_RELFRAT3_PIVOT_SURGERY_V7_RUN=false
with_pquot_packages=true
timeout_minutes=330
```

次に full：

```text
D972_B345_RELFRAT3_PIVOT_SURGERY_V7_SELFTEST=false
D972_B345_RELFRAT3_PIVOT_SURGERY_V7_RUN=true
D972_B345_RELFRAT3_PIVOT_SURGERY_V7_OUTPUT="ci/out/d972_b345_relfrat3_pivot_surgery_v7.json"
with_pquot_packages=true
timeout_minutes=330
```

source-only 見積りは q3 + frozen v6 prefix が約4--7分、短い directed closure を含む通常域が約8--20分。300分 producer wall、4.5 GiB RSS、外部330分 job limit は fail-closed safety bound であって成功時間の主張ではない。

## GHA 実行記録

実行系列は次のとおり。

- run `32219074110`: canary PASS。
- run `32219214161`: transport-only failure。数学 producer/checker の結果ではない。
- run `32219411377`: 重複便として cancel。数学的結果を持たない。
- run `32219440063`: commit `c40f4f5a0b2fe6a520439d2e921463b3d72d2b6b` 上の full run。producer と独立 checker が完走し、checker PASS。

full run の artifact は ID `9353620461`、name `gap-run-out`、size `116179` bytes、archive digest
`sha256:0a037f89e9da27eea00fe8a65879f592903c7ef5240c09643b8b38efcb7fbed0`。
receipt は `598085` bytes、SHA-256
`e91684ffefa3eab3ef51cee90758b3fcfbc7fa00e79768d499675de327155094`。

cross-checked terminal は `B345_RELFRAT3_PIVOT_SURGERY_INCOMPLETE`。停止理由は
`no_new_exact_directed_translation`、claim classification/scope はそれぞれ
`unknown_not_obstruction` / `fixed_candidate_pivot_surgery_only` である。exact ledger は以下。

- directed rounds: `32`
- directed translations added: `207`
- directed columns added: `2277`
- final round: new translations `0`, duplicate translations `10`
- unresolved target: `hexagon_1_coface_0`, ordinal `6`（1-based）
- final blocker SHA-256: `0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903`
- base translations: `32768`
- total columns: `362725`
- pivots: `362709`
- live sparse entries: `3090367`
- element pool size: `976408`
- peak RSS: `701743104` bytes
- producer runtime: `231.6906` seconds
- independent checker: PASS

これは当該 fixed candidate に対する exact directed lane が新しい translation を生成しなくなった、という saturation 記録だけである。数学的 obstruction ではなく、全 `4096` corrections の探索結果でもない。したがって B4-A、B4-B、または他の global/negative claim を一切与えない。

B345_RELFRAT3_PIVOT_SURGERY_V7_READY_FOR_GHA
