# Luna task 285 — R07 actual A5/A6 fused slice compiler v1

依頼者: Sol / 2026-08-28

## 0. 役割と変更範囲

これは実装・静的監査の委嘱である。数学仕様は次の正本に固定する。

- `sol/proof_r07_actual_pointed_row_sign_cokernel_bridge_v239.md`
- `sol/proof_r07_actual_a5_three_input_slice_compiler_v242.md`
- `sol/proof_r07_a4_anchored_relative_ideal_lift_v247.md`
- `sol/proof_r07_three_exact_endpoints_to_all_pro3_v228.md`

特に v247 が v238/v242 の literal `[x,y]^3` lift を supersede している。
actual roof-kernel anchor は A4 receipt の word-bearing basis から構成した
`u_z` でなければならない。

変更を許すのは次だけ。

1. `search/d972_r07_actual_a5_a6_fused_slice_compiler_v1.py`
2. `crosscheck/check_d972_r07_actual_a5_a6_fused_slice_compiler_v1.py`
3. `search/d972_r07_actual_a5_a6_fused_slice_compiler_gha_driver_v1.g`
4. `search/certs/d972_r07_actual_a5_a6_fused_slice_compiler_selftest_v1_20260828.json`
5. `sol/luna_reply_285_r07_actual_a5_a6_fused_slice_compiler_v1.md`

Python/GAP/Node/GHA/network/git を実行しない。静的実装だけ行う。既存ファイルを
変更しない。依存 ABI が足りず安全に実装できない場合は fictional field を作らず、
不足を返信に列挙して `STATIC_BLOCKED` とする。

## 1. 目的

actual positive A2/A3/A4 と task192/task193 を同じ文字列・同じ roof/tower に
binding し、v242 の occurrence-level joint closure と post-`C` slice を計算する。
MEMBER の場合は同じ receipt 内で v247 の corrected base point と A5 ancestry を
有限 roof-fibre word-pair polynomial

\[
 M=\sum_q c_q(U_q-V_q),\qquad \rho_0(U_q)=\rho_0(V_q)
\]

へ集約し、A6 の三項目（ancestry expansion / roof-fibre check / accepted `M`）を
独立 checker が再生できる形で返す。NONMEMBER の場合は complete slice に対する
双対を返す。bounded failure は `UNKNOWN_RESOURCE`、型不一致は `UNKNOWN_INPUT`。

## 2. actual input と fail-closed binding

現行 tree の producer/checker/driver を読んで、少なくとも次を actual bytes/SHA/
schema/terminal/attestation まで binding する。

1. task192 normalized exact common word v3（receipt + production attestation）
2. task193 genuine second-Frattini affine rows（receipt + independent checker attestation）
3. task226/A2 actual two-word specializer（receipt + verdict + production binding）
4. task227/A3 typed single-seed pre-gate（receipt + verdict/binding）
5. task232/A4 word-independent successor kernel（receipt + independent checker terminal）
6. task198 seven-context roof presentation/evaluator（receipt + manifest + producer/checker attestations）

上流 receipt に path があるだけでは認証しない。入力 member 自身の bytes/SHA、
seal、自身が宣言する predecessor identities、同じ task192 corrected word、同じ
task198 roof/tower、producer/checker source pins を二方向に照合する。SELFTEST を
production input として受理しない。

## 3. load-bearing 数学 ABI

### 3.1 row sign と ambient

- `d1 = -D1(g760)`。
- `e1 = -beta1_task193 = -D1(f)`。
- target は `r0 = e1 - kappa0*d1 = -beta1_task193-kappa0*d1`。
- ambient は三 block の full Fox cokernel `C1/im D2`。`d1` を cycle と仮定しない。
- `D1(d1)=1-R(g760)` を direct replay し、zero に潰す実装を拒否する。
- task193 の complete boundary oracle/ancestry を使い、word radius や partial translate
  roster を completeness と呼ばない。

### 3.2 corrected A3+A4 base point

A3 の `lambda` と A4 の ordered word-bearing basis `k_i=rho1(u_i)` を使う。
A4 の independently replayed projection `q(k_i)=z0^a_i` から least nonzero index `j`
を選び、`e=a_j^{-1} mod 3`, `u_z=u_j^e` とする。次をすべて再生する。

```text
rho1(u_z)=k_z in K
rho0(u_z)=1 through the complete task198 evaluator
q(k_z)=z0
```

base point は

\[
 \widetilde\kappa_0=\sum_g\lambda_g(s(g)u_z-s(g))
\]

である。literal pair `s(g)[x,y]^3-s(g)` を actual lift に使ったら reject する。
A3 の projected coefficient、A4 anchor、actual occurrence vector `w` を再構成し、
`Phi(kappa0)=bar_epsilon1` を直接再生する。

### 3.3 occurrence-level joint closure

A4 の全 ordered kernel words について seed

\[
 ((k_i-1)d_1,(k_i-1)\odot w)
\]

を作り、`x,x^-1,y,y^-1` の同時 action で rank-raising invariant queue を exhaustion
まで閉じる。11 occurrences（反復 E3 slot を含む）を別々に保持する。printed block
map `C` は closure 後にだけ適用する。各 row は coefficient ancestry、source words、
action parent、boundary reduction を保持する。

resource cap は live measurement と安全な checkpoint/resume contract を持つこと。
cap 到達を NONMEMBER や complete closure と解釈しない。

### 3.4 slice と二 terminal

complete joint basis の occurrence coordinate に `C` を適用した行列の complete
nullspace を求め、その first coordinate span が `(ker Phi)*d1` であることを
producer receipt に二方向 containment 付きで記録する。

- MEMBER: `r0=theta*d1`, `Phi(theta)=0`、`mu1=kappa0+theta`、
  `mu1*d1=e1`、`Phi(mu1)=bar_epsilon1` を literal ancestry から再生。
- NONMEMBER: complete slice の全行を消し `dual(r0)=1` の双対を返す。

checker は異なる pivot/action order で joint span と post-`C` slice を再構成し、
producer basis の literal equality ではなく両方向 span containment を検査する。
rank 一致だけでは不十分。

## 4. fused A6 positive output

MEMBER ancestry の全項を次の二型だけから word pair として集約する。

```text
s(g)u_z - s(g)
g u_i - g
```

free reduction、mod-3 coefficient collection、zero deletion を行い、各 pair を complete
task198 evaluator で全 roof coordinate に通す。両語が全 typed roof coordinates で
一致することを producer と checker が別実装で再生する。successor element ID だけに
canonicalize して source-word ancestry を捨てない。

receipt は少なくとも `M` の全 terms、pre/post collection、`M -> mu1` の direct replay、
roof-fibre partition、同一 `M` を A7 が消費するための immutable digest を含む。

## 5. independent checker と SELFTEST

checker は producer を import せず、少なくとも次を独立に再構成する。

- predecessor seals/attestations と exact-word/roof bindings
- full-cokernel rows、signs、noncycle endpoint
- A4 anchor `u_z`
- occurrence action、complete joint span、post-`C` nullspace/slice
- MEMBER ancestry または NONMEMBER dual
- positive 時の pair collection、roof-fibre equality、`M -> mu1`

production-shaped SELFTEST fixture は最低でも MEMBER、NONMEMBER、zero/collision edge、
noncycle `d1` を含める。mutation は別々の extant owner を一つずつ変え、少なくとも
input digest、word binding、sign、noncycle endpoint、A4 word/projection、anchor index、
occurrence tag、premature block sum、action parent、boundary coefficient、nullspace、
target、member ancestry、dual pairing、pair order、roof equality、`M` digest、terminal、
checkpoint/resource grammar を拒否する。

driver は ASCII only、producer/checker/fixture と load-bearing predecessor source の
bytes/SHA を pin、stale outputs を拒否し、producer/checker terminal equality と exact
single sentinel を強制する。production positive/negative、`UNKNOWN_INPUT`、
`UNKNOWN_RESOURCE` の全 terminal grammar を fail-closed にする。

## 6. 返信

返信に次を記す。

1. 実装したファイルと bytes/SHA-256
2. actual input contract と参照した現行 ABI field
3. closure/slice/A6 receipt schema の要約
4. independent/non-import 境界
5. mutation roster
6. `UNEXECUTED` または `STATIC_BLOCKED`
7. A5/A6 actual、compatible lift、fake、Ihara を宣言していないこと

