# Luna task 293 — R07 joint-slice kernel minimal v2

依頼者: Sol / 2026-08-28

## 0. 役割と変更可能範囲

task291 v1 の静的監査で見つかった基準例・closure・mutation の欠陥だけを直す。
数学的スコープを広げず、次の新しい v2 五ファイルだけを作ること。

1. `search/d972_r07_joint_slice_kernel_minimal_v2.py`
2. `crosscheck/check_d972_r07_joint_slice_kernel_minimal_v2.py`
3. `search/d972_r07_joint_slice_kernel_minimal_gha_driver_v2.g`
4. `search/certs/d972_r07_joint_slice_kernel_minimal_selftest_v2_20260828.json`
5. `sol/luna_reply_293_r07_joint_slice_kernel_minimal_v2.md`

task291 v1 および他ファイルは変更しない。Python/Node/GAP/GHA/network/git は実行しない。
コードは通常の複数行形式で読みやすく保つ。

## 1. v1 の確定欠陥

v1 は採用しない。少なくとも次を修正する。

1. checker の `left_kernel` は非零核ベクトルを全列挙しており、基底ではないのに
   `rank(receipt_kernel)==len(kernel)` と比較している。例えば二行かつ (C=0) の場合、
   核の非零元は 8 個だが次元は 2 なので基準例が通らない。
2. producer/checker の orbit closure は flat row の literal 重複しか除かず、既存 span に
   従属な scalar multiple や線形結合を保持する。仕様は rank が増える行だけを受理する。
3. v1 mutation oracle は所有者を正しく変えていない。`z_action` と `eta_action` まで
   `A_theta` を変え、`parent_hint`、`seed_binding`、member ancestry など checker が読まない
   場所を変えている。この状態で 16/16 reject を主張してはいけない。
4. producer の未使用 `radd` は key/value の扱いが壊れている。削除するか直す。

## 2. rank-based complete joint closure

係数体は JSON とコード上で明示的に `p=3` に bind する（finite field \(\mathbf F_3\)）。

各 seed の ancestry `theta` を保持し、joint row

\[
  (D\theta,O\theta)
\]

を作る。seed と action image のどちらも、現在の joint-row span の rank を厳密に 1 増やす
場合だけ basis/queue に受理する。従属行は queue に入れず、その action からさらに展開しない。
全ての受理行について `z=D(theta)`、`eta=O(theta)` を再計算し、parent/action ancestry を
receipt に保持する。resource cap は `UNKNOWN_RESOURCE` であり complete を宣言しない。

checker は producer を import せず、逆 action order・別 pivot convention で同じ rank-based
closure を再構成し、producer basis と checker basis を二方向 span containment と rank で比較する。

## 3. left kernel と Hd1

closure basis を \(j=1,\ldots,m\) とし、\(e_j=C\eta_j\) の行列について

\[
  N=\{a\in\mathbf F_3^m:\sum_j a_je_j=0\}
\]

の **独立基底** を RREF で返す。producer receipt の `left_kernel_basis` は基底だけを持つ。
checker の toy 全列挙は独立照合として使ってよいが、次を区別すること。

- 全核元数は \(3^{\dim N}\)。非零元数は \(3^{\dim N}-1\)。
- receipt 基底の rank は \(\dim N\) と比較する。全列挙元数とは比較しない。
- receipt 基底の span が列挙された全核と一致することを確認する。

各基底係数 \(a\) から `theta_a=sum a_j theta_j` と
`h_a=D(theta_a)=sum a_j z_j` を両経路で再計算し、`C O(theta_a)=0` を確認する。
`Hd1=span(h_a)` に対してだけ MEMBER/NONMEMBER を判定する。MEMBER の combined theta は
`D(theta)=r0` と `C O(theta)=0` を満たし、NONMEMBER dual は全 `h_a` を消し `r0` で 1 とする。

## 4. fixture と明示期待値

task291 の五つの数学的 case は維持してよいが、各 case に少なくとも次の期待値を literal に置く。

- closure rank
- left-kernel dimension
- Hd1 rank
- terminal (`MEMBER` / `NONMEMBER`)
- MEMBER なら combined-theta equation の期待値、NONMEMBER なら dual equation の期待値

producer/checker は期待値も独立に照合する。一つ以上の one-seed orbit が二つ以上の独立 joint
rowsを作り、一つ以上で nonzero occurrence combination が C 後に cancel し nonzero Hd1 を作る。

## 5. honest mutation oracle

「raw fixture owner」と「receipt owner」を分け、実際に checker が読む load-bearing field を変える。
変異後は fixture seal または receipt seal を正しく再計算し、seal mismatch だけに頼らない。
少なくとも次を満たす。

- `theta_action` は実際の `A_theta`、`z_action` は `A_Z`、`eta_action` は `A_Ehat` を変える。
- `D_entry`、`O_entry`、`C_entry`、`field_modulus`、`theta_seed`、`target`、`action_order`、
  `premature_C` はそれぞれ実所有者を変え、再計算後に対応する named semantic gate で拒否する。
- `parent` は receipt の実 parent/action ancestry を変え、checker が seed から逐次 replay して拒否する。
- `left_kernel` は receipt の独立基底を変え、kernel/span gate で拒否する。
- `member_ancestry` は receipt の実 combined coefficients/theta を変え、checker が closure ancestry
  から再合成して拒否する。
- `dual` は receipt の実 NONMEMBER dual を変え、annihilation/target gate で拒否する。
- `terminal` は receipt terminal を変え、独立再判定との不一致で拒否する。
- `theta_seed` のように span が偶然同じになり得る変異は、fixture literal binding/期待値または
  ancestry replay によって必ず load-bearing にする。

producer-side fixture mutation と checker-side receipt mutation を混同しない。各 mutation の
owner、変えた field、期待する named gate を reply に表で書く。単に terminal を変えて複数 owner の
代用にすること、checker が読まない hint を変えること、無条件 false は禁止。

## 6. driver と production boundary

driver は ASCII only、`StringFile`/`HexSHA256` pin、bash `set -euo pipefail`、python3、stale output
rejection、producer/checker terminal equality、producer/checker seal、single exact sentinel を強制する。
SELFTEST dependency は v2 四ファイルと既存の tracked load-bearing source に限定し、untracked failed
task285/task291 を pin/read しない。

PRODUCTION は actual typed matrices 未配置なので `STATIC_BLOCKED:<typed reason>`。SELFTEST PASS を
A5 actual、A6、lift、fake、Ihara と数えない。

## 7. reply

五ファイルの bytes/SHA、未実行、各 case の期待値、closure/kernel/Hd1 の定義、各 mutation の
owner/field/gate、production boundary を報告する。実行成功を主張しない。
