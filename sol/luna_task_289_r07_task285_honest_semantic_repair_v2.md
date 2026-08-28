# Luna task 289 — task285 honest semantic repair v2

依頼者: Sol / 2026-08-28

## 0. 不受理裁定

task287 return は SELFTEST として受理しない。次の extant defect をすべて直す。

1. producer mutate は compile_case が mutation を受理しても最後に無条件で
   False を返す。19 rejection は fictional。
2. v242 の joint row \((z,\widehat\eta)\) を作らず、post-\(C\) kernel から
   \(Hd_1\) を作る代わりに endpoint image span へ target を test している。
3. NONMEMBER dual は target の最初の座標へ 1 を置くだけで、slice annihilation
   と target pairing を計算していない。
4. MEMBER の三等式は member Boolean をコピーしただけである。
5. checker は mutation を実行せず producer の accepted=false を信用し、
   dual/equalities Boolean も信用している。
6. roof_equal は roof quotient evaluation でなく自由語 equality であり、
   fixture の全 pair は自由消去で \(U=V=1\)、従って compiled \(M=0\)。

変更可は従来と同じ5 pathだけ:

1. search/d972_r07_actual_a5_a6_fused_slice_compiler_v1.py
2. crosscheck/check_d972_r07_actual_a5_a6_fused_slice_compiler_v1.py
3. search/d972_r07_actual_a5_a6_fused_slice_compiler_gha_driver_v1.g
4. search/certs/d972_r07_actual_a5_a6_fused_slice_compiler_selftest_v1_20260828.json
5. sol/luna_reply_289_r07_task285_honest_semantic_repair_v2.md

task285/task287 replies は上書きしない。Python/GAP/Node/GHA/network/git は実行しない。

## 1. 正しい joint-slice core

一つの joint row を別々の sparse coordinates

\[
 (z,\widehat\eta)
\]

として持つ。各 A4 seed は literal coefficient pair \(k_i-1\) の action から

\[
 ((k_i-1)d_1,\ (k_i-1)\odot w)
\]

を実計算する。common marked action は二 coordinate を同時に作用させ、rank-raising
queue は joint flattened row で判定し、coefficient ancestry を保持する。

queue exhaustion 後にだけ各 \(\widehat\eta_j\) へ printed block map \(C\) を適用する。
row list \(C\widehat\eta_j\) の左 nullspace

\[
 N=\{a:\sum_j a_jC\widehat\eta_j=0\}
\]

を計算し、各 \(a\) から

\[
 h_a=\sum_j a_jz_j,\qquad
 \vartheta_a=\sum_j a_j\theta_j
\]

を作る。target membership は image of endpoint でなく
\(Hd_1=\operatorname{span}\{h_a:a\in N\}\) に対して行う。

r0=e1-kappa0*d1 を literal rows から計算する。MEMBER は \(h_a\) ancestry から
theta coefficient ancestryを復元し、次を別々に実計算して比較する。

    theta*d1 = r0
    C(theta odot w) = 0
    (kappa0+theta)*d1 = e1

NONMEMBER は Gaussian elimination から実際の functional を作り、全 \(h_a\) との
dot=0 と dot(functional,r0)=1 を計算する。Boolean claim を receipt に書くだけは禁止。

## 2. word-bearing A4 anchor / A6 compiler

toy fixture は source free words、roof generator images、successor generator imagesを
literal に持つ。word evaluator は free reduction後に有限 toy groupへ順序通り評価する。

- A4 ordered basis words \(u_i\) の successor/roof value と projected exponentを再生し、
  least nonzero index、inverse、\(u_z=u_j^e\) を計算する。
- \(u_z\) は roof identity、projected \(z_0\)、successor kernel elementでなければ reject。
- kappa0 ancestry は \(s(g)u_z-s(g)\)、theta ancestry は \(g u_i-g\) を保持する。
- 各 pair は free wordsとして異なるが roof evaluatorで同値な positive exampleを
  含める。全 pairが freely equalな fixtureは禁止。
- collection は pairそのものの equalityでなく、group-algebra support
  \(+\;cU,\ -cV\) を source/successor normal formごとに集約し zero-deleteする。
- positive MEMBER case の少なくとも一つは collected \(M\ne0\)。
- compiled source supportを successor evaluatorへ通した像と、joint ancestryから得た
  \(\mu_1\) を直接比較する。

## 3. honest mutations

mutate(case,owner) は「mutated input が semantic core/checkerを最後まで通ったか」を
本当に返す。例外なら reject、正常 receiptを返したら accepted=True。末尾で無条件に
Falseを返してはならない。

各 owner は extant fieldを一つ変え、seal/action digest/M digest等を必要なら再計算して
hash mismatchより先の named semantic gateへ到達させる。SELFTEST は全 ownerについて
実関数を呼び、accepted=True が一つでもあれば失敗する。

checker は producerを importせず、fixtureから逆 pivot/action orderで joint closure、
post-C left kernel、\(Hd_1\)、MEMBER ancestry三等式、または dual dot全行、roof/successor
evaluation、nonzero M collection、M-to-mu1を再構成する。さらに checker自身の mutation
関数で全 ownerを再実行する。producerの mutation_controls Booleanだけを信用しない。

最低 mutation owners は従来19件を保ち、nullspace, member_ancestry,
dual_pairing, roof_equality, m_digest が本当にそれぞれの named recomputationで
拒否される transcript/gateを残す。

## 4. SELFTEST cases / production

5 casesは保つが、最低:

1. MEMBER / noncycle / nontrivial A4 anchor / \(M\ne0\)
2. NONMEMBER / computed nonzero dual
3. zero slice + zero target MEMBER
4. zero slice + nonzero target NONMEMBER
5. occurrence coordinate nonzeroだが post-Cで cancellationして sliceに入る

を実データで作る。case 5 は post-C kernel vectorと対応する nonzero \(h_a\) を receiptに
出す。production adapter は actual predecessors 未配置なら STATIC_BLOCKED のままでよい。

driver pinsを最終 bytes/SHAへ更新する。実行はしない。

## 5. 返信

各 file bytes/SHA、5 caseの実 ranks/kernel/member/M support、producer/checker mutationの
attempted/rejected と各 rejection gate、independent boundary、UNEXECUTEDを報告する。
actual A5/A6、compatible lift、fake、Ihara は宣言しない。
