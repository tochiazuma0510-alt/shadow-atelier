# Luna task 288 — R07 Neumann--Fox group-like gate v1

依頼者: Sol / 2026-08-28

## 0. 数学正本と範囲

`sol/proof_r07_neumann_fox_group_like_integrability_v249.md` を実装する。
これは A9 の word-integrability gate だけであり、H1/H2/P、mixed-prime、perfect-core、
fake、Ihara を宣言しない。

変更可:

1. `search/d972_r07_neumann_fox_group_like_gate_v1.py`
2. `crosscheck/check_d972_r07_neumann_fox_group_like_gate_v1.py`
3. `search/d972_r07_neumann_fox_group_like_gate_gha_driver_v1.g`
4. `search/certs/d972_r07_neumann_fox_group_like_gate_selftest_v1_20260828.json`
5. `sol/luna_reply_288_r07_neumann_fox_group_like_gate_v1.md`

Python/GAP/Node/GHA/network/git は実行しない。actual task285 MEMBER ABI が未完成なら
production adapter は fail-closed のままにし、数学 core と SELFTEST は完成させる。

## 1. finite-rung core

production input は task192 exact word/Fox ancestry と accepted A6 pair polynomial
`M=sum b_i(U_i-V_i)`、一つの finite relative pro-3 quotient の complete group/action
interface、nilpotence cap を持つ。core は:

1. literal correction wordから left Fox chain `alpha` を構成
2. A6 pair の二 source conjugation action から operator `Mcal` を構成
3. `Q_N=-sum_{r=0}^{N-1} Mcal^r alpha` を、次項が exact zero になるまで計算
4. `u=1+partial(Q_N)` を finite group algebraの full sparse supportで構成
5. support がちょうど `[(one,1)]` ではなく、**任意の一つの group basis elementに
   coefficient 1** であることを group-like PASS とする
6. support が複数、coefficient が1でない、counit不一致なら exact FAIL certificate

を返す。hashだけで support singleton を判定しない。term order、非可換 multiplication、
left/right Fox convention は固定する。bounded cap は `UNKNOWN_RESOURCE`、ABI 不一致は
`UNKNOWN_INPUT`。

## 2. compatibility receipt

複数 rung を渡す production mode を用意し、各 rung の PASS basis elementが reduction
で一つ前の basis elementへ移ることを直接検査する。全 registered rungs PASS の場合も
「registered finite familyの group-like compatibility」であり、無限 cofinality は入力
manifest が cofinal constructor を認証した場合だけ主張可能。初版は `all_rung=false`
を固定してよい。

FAIL は first preregistered rung、full support、counit/coproduct mismatchを保持し、その
named `(task192 word,M)` Neumann chainだけを rejectする。

## 3. independent checker / SELFTEST

checker は producer import禁止、異なる sparse multiplication/pivot-free support collector
で alpha、operator powers、Q、partial、u support、reduction compatibilityを再構成する。

production-shaped SELFTEST は最低5 case:

1. `Q=delta(c)` で group-like PASS、nonidentity c
2. two-support exact FAIL
3. coefficient/counit FAIL
4. noncommutative operatorで複数項後にnilpotent zeroとなる PASS
5. two-rung individual PASSだが reduction incompatibility FAIL

mutation は task192 word、Fox sign、pair U/V、pair coefficient、conjugation order、operator
power order、nilpotence cutoff、Q sign、endpoint factor order、support coefficient、support
deletion、basis element、counit、rung map、upstream digest、terminal/resource ownerを個別に
変え、seal更新後のsemantic gateで全拒否する。

driver は ASCII only、source/fixture/checker pins、stale rejection、single exact terminals、
producer/checker equality、single sentinelを強制する。

## 4. 返信

files bytes/SHA、core、5 cases、mutation数、independent boundary、`UNEXECUTED`、actual
A9/group-like/H1/H2/P/fake/Iharaを宣言していないことを報告する。
