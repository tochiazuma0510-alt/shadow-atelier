# Luna task 291 — R07 joint-slice kernel minimal v1

依頼者: Sol / 2026-08-28

## 0. 分割裁定と変更範囲

task289の一体実装は不受理。failed task285 filesはこれ以上変更しない。A5の数学中心だけを
新しいversioned pathsへ分離する。

変更可:

1. search/d972_r07_joint_slice_kernel_minimal_v1.py
2. crosscheck/check_d972_r07_joint_slice_kernel_minimal_v1.py
3. search/d972_r07_joint_slice_kernel_minimal_gha_driver_v1.g
4. search/certs/d972_r07_joint_slice_kernel_minimal_selftest_v1_20260828.json
5. sol/luna_reply_291_r07_joint_slice_kernel_minimal_v1.md

Python/GAP/Node/GHA/network/gitは実行しない。コードは監査可能な通常の複数行形式で書き、
一行へ圧縮しない。fixtureを唯一のSELFTEST入力とし、内部に別のshadow casesを持たない。

## 1. typed coefficient ABI

全空間は \(\mathbf F_3\) 上。coefficient module \(\Theta\)、full-cokernel coordinate
\(Z\)、eleven-occurrence coordinate \(\widehat E\)、printed endpoint coordinate \(E\) を
別々の named sparse basisで持つ。

fixtureは次をliteralに持つ。

- coefficient seeds \(\theta_i\in\Theta\)
- marked generatorsのinvertible matrices
  \(A_\Theta,A_Z,A_{\widehat E}\)
- linear maps \(D:\Theta\to Z\)、\(O:\Theta\to\widehat E\)
- printed block map \(C:\widehat E\to E\)
- target \(r_0\in Z\)

producerは各 actionについて

\[
 D A_\Theta=A_ZD,\qquad O A_\Theta=A_{\widehat E}O
\]

を全basis vectorで検査する。seed joint rowは arbitrary input rowでなく

\[
 (D\theta_i,O\theta_i)
\]

をmapから計算する。

## 2. complete joint closure

coefficient ancestry \(\theta\) を保持し、joint flattened row
\((D\theta,O\theta)\) のrankが上がる時だけqueueへ追加する。全 marked actionsを
exhaustする。resource cap stopはUNKNOWN_RESOURCEでありcompleteを宣言しない。

各accepted rowについて以下を再計算しreceiptへ持つ。

    z = D(theta)
    eta = O(theta)
    parent/action ancestry

noncanonical basis orderは主張しない。

## 3. post-C left kernel and Hd1

closure終了後だけ

\[
 e_j=C\eta_j
\]

を計算する。row list \(e_j\) のleft nullspace

\[
 N=\{a:\sum_j a_je_j=0\}
\]

をexact RREFで計算する。各 \(a\in N\) から

\[
 \theta_a=\sum_ja_j\theta_j,\qquad
 h_a=D\theta_a=\sum_ja_jz_j
\]

を両方の式で再生し、\(C O(\theta_a)=0\) を検査する。

\[
 Hd_1=\operatorname{span}\{h_a:a\in N\}
\]

に対してだけr0 membershipを判定する。endpoint image spanへのmembershipは禁止。

MEMBERは係数を返し、combined thetaについて

    D(theta)=r0
    C O(theta)=0

を再計算する。NONMEMBERはGaussian eliminationからfunctional phiを構成し、
全h_aでphi(h_a)=0、phi(r0)=1を実dotで検査する。

rankはindependent basis rankを記録し、len(raw rows)で代用しない。

## 4. independent checker

checkerはproducer import禁止。fixtureから:

- reverse generator order
- reverse pivot convention
- typed equivariance
- complete joint closure
- left kernel
- Hd1
- MEMBER combined theta、またはNONMEMBER dual

を再構成する。toy dimensionは小さく保ち、second cross-checkとして全
\(\mathbf F_3^n\) coefficient enumerationでleft-kernelとmembershipを照合する。
base-3 enumerationは各digitを正しく更新すること。同じ係数を全rowへ置く実装は禁止。

producer/checker basisは両方向span containmentで比較し、literal list equalityは禁止。

## 5. five literal cases

fixtureだけに最低5 casesを置く。

1. nonzero Hd1 MEMBER
2. same Hd1に対するoutside target NONMEMBER
3. zero Hd1 / zero target MEMBER
4. zero Hd1 / nonzero target NONMEMBER
5. occurrence combinationはnonzeroだがC後にcancelし、対応するnonzero hがHd1へ入る

最低一caseはone seedのmarked orbitから二つ以上のindependent joint rowsを生成する。
最低一caseはleft-kernel dimension>0かつHd1 rank>0。case 5は
eta combination nonzero、C eta combination zeroをreceiptに持つ。

## 6. honest mutations and driver

最低16 owners:

    field_modulus, theta_seed, theta_action, z_action, eta_action,
    D_entry, O_entry, C_entry, action_order, parent, premature_C,
    left_kernel, target, member_ancestry, dual, terminal

mutationはraw fixture fieldを一つ変え、fixture sealを更新し、producer coreを再実行する。
accepted receiptが返ればaccepted=true、例外ならnamed gate付きreject。無条件falseは禁止。
checkerも独自mutation関数で全ownersを再実行しproducer Booleanを信用しない。

driverはASCII、StringFile/HexSHA256 pins、bash set -euo pipefail、python3、stale rejection、
single exact terminals、producer/checker seals、sentinelを強制する。

## 7. production boundary / reply

初版PRODUCTIONはactual typed matrices未配置ならSTATIC_BLOCKED。SELFTEST PASSをA5 actualと
数えない。

replyはfile identities、各caseのclosure rank/kernel dim/Hd1 rank/terminal、
MEMBER thetaまたはdual support、producer/checker mutation gate一覧、UNEXECUTEDを報告。
actual A5/A6/lift/fake/Iharaは宣言しない。
