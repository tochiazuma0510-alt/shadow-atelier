# Luna task 286 — R07 actual three exact PB endpoints v1

依頼者: Sol / 2026-08-28

## 0. 範囲

次の数学正本を実装する。

- `sol/proof_r07_endpoint_only_word_evaluator_v198.md`
- `sol/proof_r07_combined_block_endpoint_reduction_v194.md`
- `sol/proof_r07_three_exact_endpoints_to_all_pro3_v228.md`
- upstream contract: `sol/luna_task_285_r07_actual_a5_a6_fused_slice_compiler_v1.md`

変更可:

1. `search/d972_r07_actual_three_exact_pb_endpoints_v1.py`
2. `crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v1.py`
3. `search/d972_r07_actual_three_exact_pb_endpoints_gha_driver_v1.g`
4. `search/certs/d972_r07_actual_three_exact_pb_endpoints_selftest_v1_20260828.json`
5. `sol/luna_reply_286_r07_actual_three_exact_pb_endpoints_v1.md`

Python/GAP/Node/GHA/network/git は実行しない。静的実装のみ。task285 ABI がまだ
未完成なので、現行 task285 files が現れたら読んで binding する。安全な ABI を
確定できない部分は fictional field を捏造せず `STATIC_BLOCKED` と返信する。

## 1. 目的と terminal

task285 の independently accepted MEMBER receipt が返す一つの immutable finite
roof-fibre polynomial

\[
M=\sum_i a_i(U_i-V_i)
\]

について、PB3(H1), PB3(H2), PB4(P) の三 exact group-algebra endpoint を計算し、
次のいずれかを返す。

```text
R07_THREE_EXACT_PB_ENDPOINTS_ZERO
R07_THREE_EXACT_PB_ENDPOINTS_NONZERO block=H1|H2|P
UNKNOWN_INPUT:<reason>
UNKNOWN_RESOURCE:phase=<name>:cap=<name>:value=<n>:limit=<n>
```

ZERO のときだけ v220 A7 の H1/H2/P 三 milestone を満たし得る production receipt
である。NONZERO は named `M` の exact obstruction であり、他の代表や他の lower
word の非存在を主張しない。

## 2. actual input binding

task285 receipt/checker verdict/production binding の bytes/SHA/schema/terminal/seal を
認証し、MEMBER、accepted independent checker、同じ task192 corrected word、同じ
task193 rows、同じ task198 roof/tower、同じ A4 anchor を必須とする。SELFTEST や
NONMEMBER を production input として受理しない。task285 の `M` terms と immutable
digest を receipt の他の ancestry から再集約して一致させる。

task193/task198 の load-bearing producer/checker source identities も pin し、11
occurrence records を predecessor words から再構成する。上流が運んだ計算済み
endpoint Boolean を信頼しない。

## 3. exact endpoint formula

各 occurrence `o` について typed

```text
(block, position, rho_o, sigma_o, P_o, xi_o)
```

を保持する。反復 E3 は別 position、E3/E4 の同名 C21 は別 type とする。
`xi_o=D1(d_o)` と `epsilon_B=D1(e_B)` を literal retained words から構成し、

\[
\eta_B(M)=\epsilon_B-\sum_{o\in B}\sigma_oP_o
 \sum_i a_i(\rho_o(U_i)-\rho_o(V_i))\xi_o
\]

を右記順序のまま展開する。各 term の unreduced PB word、coefficient、由来を保持し、
mod 3 で exact PB normal-form bucket を集約する。occurrence ごとの cancellation を
先に確定せず、block 全体で collection する。

PB equality key は faithful Artin action on `F_3` / `F_4` の full reduced-image tuple。
hash だけ、有限商像、KBMAG 成功 Boolean を equality key にしない。producer は一つの
Artin composition convention、checker は独立変換した convention（または実在する
独立 Garside implementation）を使い、helper/import を共有しない。

## 4. positive full-C1 replay

三 bucket が空のとき、endpoint-only 計算だけで terminal を出さない。v194 の
occurrence-diagonal full Fox chain `z_B=e_B-(M star d)_B` を literal words から別に
構成し、complete PB presentation boundary quotient の中で `D1(z_B)=0` を直接再生
する。これは task285 の projected exponent-nine endpoint ではなく infinite PB の
exact identity である。

この便では v197 の van Kampen `q_B` extraction を実装しなくてよいが、A8 consumer
が使えるよう全 finite-support `z_H1,z_H2,z_P`、literal word provenance、Artin keys、
complete presentation identities を receipt に含める。

## 5. SELFTEST / checker / driver

production-shaped SELFTEST は少なくとも:

- three-block ZERO with cross-occurrence cancellation
- H1-only NONZERO
- H2-only NONZERO
- P-only NONZERO
- repeated-E3 slot と typed C21 を交換すると失敗する case
- coefficient collision/zero deletion case

を含む。checker は endpoint words、prefixes、signs、typed substitutions、Artin tuples、
bucket collection、ZERO 時 full-C1 endpoint を独立再構成する。mutation は source word、
pair order、coefficient、block/position/type、rho、sign、prefix、inverse slot、xi、epsilon、
Artin factor order、normal form、bucket deletion、M digest、upstream seal、full-C1 row、
terminal/resource/checkpoint owner を別々に破壊し、named gate で拒否する。

driver は ASCII only、producer/checker/fixture と load-bearing upstream source の
bytes/SHA pin、stale-output rejection、single producer/checker terminal、terminal equality、
single final sentinel、typed resource terminal を強制する。

## 6. 返信

返信に files bytes/SHA、input ABI、exact normal form implementation の独立境界、
receipt schema、mutation roster、`UNEXECUTED`/`STATIC_BLOCKED` を記す。A8 boundary、
A9 lift、mixed-prime、perfect-core、fake、Ihara を宣言しない。

