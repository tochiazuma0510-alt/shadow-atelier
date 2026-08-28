# Luna task 287 — task285 core/SELFTEST repair v1

依頼者: Sol / 2026-08-28

## 0. 裁定

task285 の `STATIC_BLOCKED` envelope は production adapter の停止としては安全だが、
委嘱した A5/A6 数学 core と production-shaped SELFTEST を一行も実装していない。
これは task285 completion として受理しない。actual predecessor bytes が無くても、
正本 v239/v242/v247 の有限線形代数 core、独立 checker core、toy production-shaped
SELFTEST、mutation は実装できる。

変更可:

1. `search/d972_r07_actual_a5_a6_fused_slice_compiler_v1.py`
2. `crosscheck/check_d972_r07_actual_a5_a6_fused_slice_compiler_v1.py`
3. `search/d972_r07_actual_a5_a6_fused_slice_compiler_gha_driver_v1.g`
4. `search/certs/d972_r07_actual_a5_a6_fused_slice_compiler_selftest_v1_20260828.json`
5. `sol/luna_reply_287_r07_task285_core_selftest_repair_v1.md`

task285 reply は上書きしない。Python/GAP/Node/GHA/network/git は実行しない。

## 1. 必須 core

producer に production adapter から独立した typed internal ABI と、次の pure functions
を実装する。

1. sparse \(\mathbf F_3\) row canonicalization、加減、scalar、marked action
2. independent rank basis、remainder、membership ancestry、nullspace、separating dual
3. A4 ordered basis projectionから least-nonzero `u_z` anchor を作る replay
4. v247 `kappa0=sum lambda_g(s(g)u_z-s(g))` の pair ancestry と projected endpoint
5. seed `((k_i-1)d1,(k_i-1) odot w)` の occurrence-level simultaneous invariant queue
6. closure 後だけ `C` を適用する endpoint projection nullspace と exact slice
7. `r0=e1-kappa0*d1` の MEMBER または NONMEMBER
8. MEMBER 時 `mu1=kappa0+theta` の全等式と二型 pair collection
9. free reduction/mod-3 collection/zero deletion、toy complete roof evaluatorで pair 両端一致

`d1` は非 cycle case を必ず通す。producer の core には `STATIC_BLOCKED` の早期 return
を置かず、SELFTEST から全 core が実行されるようにする。production adapter は actual
manifest が無い限り引き続き fail-closed でよい。

## 2. 独立 checker

checker は producer import 禁止。producer receipt から Boolean/rank だけを読むのでなく、
fixture の literal group/action/row/pair data から別実装で以下を再構成する。

- reverse generator/action queue order
- different pivot convention
- complete occurrence joint span の両方向 containment
- post-`C` nullspace/slice の両方向 containment
- MEMBER ancestry と全等式、または dual annihilation/target pairing
- A4 anchor と corrected base point
- A6 pair collection、roof equality、`M -> mu1`

非 canonical basis list の literal equality は要求しない。

## 3. SELFTEST cases

fixture は単なる envelope でなく、literal toy inputs を持つ。最低5 case:

1. MEMBER、noncycle `d1`、nontrivial anchor、pair cancellationあり
2. NONMEMBER、support-nonzero separating dual
3. zero slice / zero target MEMBER
4. zero slice / nonzero target NONMEMBER
5. occurrence-levelでは非zeroだが post-`C` で cancellation する case

各 case で common marked action、A4 kernel words/projections、A3 lambda、`w`, `d1`,
`e1`, boundary quotient、toy roof evaluator を literal に持たせる。SELFTEST terminal は
producer `...PRODUCER_SELFTEST_PASS`、checker は mutation 全拒否数付き
`...CHECKER_SELFTEST_PASS mutation_attempted=N mutation_rejected=N` とする。

## 4. mutation

task285 の19 owner を名前だけ列挙せず、各 owner の extant literal field を一つだけ
変え、seal を更新した上で semantic gate まで到達させる。各 mutation が受理されれば
SELFTEST fail。少なくとも sign と noncycle endpoint、A4 projection と anchor index、
occurrence tag と premature block sum、action parent、boundary coefficient、nullspace、
target、member ancestry、dual pairing、pair order、roof equality、M digest はそれぞれ
異なる owner を変える。

## 5. driver と production boundary

driver は新 bytes/SHA pins に更新。SELFTEST は core と checker/mutations を実行して
single exact terminal/sentinel を強制する。PRODUCTION は actual adapter 未確定なら
`STATIC_BLOCKED` を typed artifact として返してよいが、それを PASS/A5/A6 と数えない。
SELFTEST receipt と production-blocked receipt の schema/terminal を混同しない。

## 6. 返信

files bytes/SHA、5 cases の期待 terminal、core 関数一覧、independent boundary、実 mutation
数、`UNEXECUTED` を報告する。actual A5/A6、compatible lift、fake、Ihara は宣言しない。
