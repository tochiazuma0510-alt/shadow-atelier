# WO-155-1 完了報告

実装・実行完了。producer の GAP 実装、raw rows/witness、producer verdict/cert 本体は開封・import していない。判定入力は指定された witness export 2 本と、登録済み DEEP15 source の指定2レコードだけ。

## 実行

```text
python crosscheck/check_koubou83_A2_full48_v1.py
exit code: 0
elapsed: 約10.4 s
```

同一 tree で2回実行し、verdict は byte-identical。

## 成果物

| path | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_koubou83_A2_full48_v1.py` | 26805 | `519fddc25618d5f84f2b3d9e395cf1ce10b9116537ae4f41e47a3f2c1e7e347d` |
| `crosscheck/verdicts/koubou83_A2_full48_crosscheck_v1_20260822.json` | 216454 | `a144249b323774a2ecb18c1250a86b8fbe0b3a2a7fad379eb8be3404598898d5` |

Witness input SHA pins: v2(p=3) `25f902e0e8bbbe7dd8c9c60113eb239cb3b0a8a6d9a9c37491e06f6bfa1f6511`; v3(p=2) `2f665114d8ffcd35383d36a5a3d9a9c3d0dbb36e932cfd52d399913c34ced3e1`。DEEP15 は source-extraction SHA `75905c604b83058ff6406f5c115bfa3325fd4424c98125750e49c2b76bbd35ec` として embedded provenance に記録（runtime read=false）。

## 結果

- selected universe: 192/192、各 window cell 48/48、semantic key exact。
- paired `(m,f_xyword)` exact、row manifest 192件。
- legal 192/192（correction `w` の embedded window N-membership も独立評価 192/192）、charming 192/192、direct `R1/R2 ∈ K_p` 192/192。
- 各 direct R について quotient evaluation identity、full tracker remainder-zero、V-basis coefficient-zero を別々に計算し、V-coefficient-zero 192/192。
- PIN-AB-1: `coords(σ1²)=(1,0,0)`, `coords(σ2²)=(0,1,0)`, `coords(Delta²)=(0,0,1)`, raw crossings `(2,2,2)`。
- 上記3座標は signed strand tracker 由来（PB normal-form fixture は別 canary）。row/positive/variant の legal γ は strand tracker γ を使用し、PB γ一致を assert/cert（row 192/192、全 variant）した。
- positive controls は export 内の一意 semantic rows `(m=0,f_xyword=[])`（idx 1）と `(m=11,f_xyword=[])`（idx 43）の実 witness を使用し、window×p の legal/charming/direct 全件 PASS（4 controls × 2 p rows）。
- destructive `F ++ x^2`: 192/192 FAIL。
- structure-sensitive control: `w -> x*w*x^-1`, `x=[1,1]`; legal/charming/N-membership maintained. Non-empty correction rows: 186/188 direct failures (93/94 in each cell 154161 and 154163); empty `w=[]` rows are the explicit 0/4 PASS exception.
- destructive `x^2` suffix overall gate (`legal ∧ charming ∧ direct`): 192/192 FAIL (direct-only failures also 192/192)。
- environment canaries: both windows `|G|=192`, `rankD=191`, `dimKerD=193`; 154161 は `kappa=2, rankU=96, dimV=98`、154163 は `kappa=4, rankU=144, dimV=50`。
- environment は p=2,p=3 の双方を assert/cert 記録。全 defining words evaluation identity、Fox identity self-check（154161: 113語、154163: 63語）、`rankFull=rankU+dimV=dimKer+1=194` を確認。
- signed strand tracker の PIN-AB-1 と全192行の PB normal-form coords 一致（192/192）を確認。4 cell は `154161_p2/p3`, `154163_p2/p3` 各48件。
- export top-level schema/provenance、token/type domain、raw witness source SHA を fail-closed pin。
- claim-universe digest と predicate version を cert に固定。DEEP15 は embedded extraction provenance として記録し、runtime source read は false。
  claim-universe digest: `e62cdb862c4d1a2ee87a3443146a36f34b1ec84bd9f83406f280ceaaef7106d9`。

Overall: `PASS`（verdict 表記は `cross-checked candidate`）。
