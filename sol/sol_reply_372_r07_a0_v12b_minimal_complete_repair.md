# Sol task 372 — A0/v12b minimal complete repair

## 0. 完了範囲と裁定境界

task368 が列挙した九つの load-bearing reject を、一つの versioned v12b
`SELFTEST_BOOTSTRAP` source set で閉じた。これは **STATIC REPAIR COMPLETE** の報告であり、
新 candidate の監査 PASS や計算結果の報告ではない。Python、Node、GAP、GHA、workflow、git、
network、syntax compilation、candidate は一切実行していない。このため R/V、observed runtime、
observed RSS、selected pivot、selected coordinate の実測値は存在せず、v12b は引き続き
`UNEXECUTED`、A0 は `0/1` である。

変更は task372 指定の六 owner だけである。v12a は変更せず、production/resume/lift/fake/Ihara
の権限を一切増やしていない。

## 1. Versioned physical owners と封印

read-only PowerShell で最終 physical bytes と SHA-256 を再計算した。

| owner | bytes | SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.manifest.v1.json` | 27,295 | `ecd722495b02dc48cfa68e3be9751a82664fd895a4b01d185c647b4053fbfbe7` |
| `search/d972_r07_history_free_positive_fast_resume_v12b.py` | 317,154 | `614bc65bbb36c0a7504923c9ba7b4700ba04ecb66868d5a90994c65e1577dcd7` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v12b.py` | 263,911 | `1b8587de9caabc16f3a51ace1d2ea5a892281d155ea4f4270e830208ec4cd0d0` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v12b.g` | 28,740 | `631ba0d02443d8d4f142248aa098859b2e943cb86073b7021313b22c7cff7896` |
| `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12b_20260829.json` | 23,679 | `64a7dd14e26431387f6ff1dd71aad6d977a5db943c4ca42c01fb19477f3a3ddb` |

P0 の top-level `self_digest_sha256` は
`3538a629d7e3ce44d965ff796d201bee23cfca1087f3c966b84b9dfe8dcb3419`、fixture の
`self_digest_sha256` は
`cc787bc588f05a0bf49cebc385a968d10c245d906352d3b6e8e53d101f9c8ad5` である。どちらも
当該 field を除いた canonical JSON の SHA-256 と read-only PowerShell で一致した。P0 の
source rows と fixture row は上表の final physical identity を pin し、driver lines 33--36 も
P0/producer/checker/fixture の同じ値を pin する。本返信は自己参照する narrative owner なので、
その physical identity は次の独立監査側で freeze する。

authority graph は
`frozen sources -> P0 -> candidate R -> independent candidate V -> artifact gate` の一方向である。
Python owner は P0 の path/schema/self-seal/source graph を pin し、P0 が Python owner の physical
identity を pin する。P0 physical SHA は downstream の driver だけが pin する。R/V は driver
identity を持たず、実行後 manifest rewrite もないため cycle はない。

## 2. Task368 の九修理項目

### 2.1 Chronological pivots

producer の ordinary builder (lines 1330--1400) と selftest validator
`_validate_triangular_subset` (3012--3059) を、ともに逐次 `seen_pivots` だけを禁止する同じ
規則にした。future pivot は自分の row が処理されるまで合法である。untouched baseline は
mutation より先にこの validator を通り、P5/P6 witness と八 triangular mutations も同じ
validator を通る。mutation name による validator bypass はない。checker の ordinary/raw
reconstruction も lines 2927--2938, 2967--3001 で同じ chronological rule を独立に使う。

### 2.2 Actual current dual と selected owner

producer `_producer_correction_selftest_frame` (lines 3643--3799) は manufactured one-key
functional を廃止した。ordinary target reduction が保持した
`runtime["current_dual_private"]`、actual target、actual remainder、formal solution node を出発点にし、
次を baseline mutation 前に要求する。

- current dual が chronological 2,896 basis rows を全て annihilate すること。
- target pairing が `1` または `2` で、remainder pairing と一致すること。
- rank-before、pivot-order digest、basis digest、target/remainder、formal solution を一つの
  `current_epoch` に bind すること。
- actual Q0/Gamma/K0 roster と direct-column replay を走査し、current dual と nonzero pairing
  する K=0 owner を選ぶこと。
- ordinary reducer の `add_actual` を通して actual pivot、rank `2896 -> 2897`、selected formal
  solution、exact selected coordinate を導出すること。

その record は `producer_selected_statement` (3803--3864) を経て H、final heavy carrier、R に
bind される。未実行なので pivot/coordinate の具体値はここでは記載しない。source が初めて
到達した actual owner から決定的に生成し、実行前の convenient value は置いていない。

### 2.3 Checker の raw 一読独立再構成

checker `checker_reconstruct_raw_epoch` (lines 2944--3075) は、authenticated frozen raw
checkpoint DOM を一回だけ受け取り、producer の selected statement/transported dual を初期値に
しない。全 2,896 raw columns の provenance、sparse digest、ancestry、pivot order を順に読み、
独自 `CheckerLinearReducer` で P rows と P digest を再構成する。その後 raw target を reduction
して remainder、formal solution、initial/current dual、basis annihilation、target/remainder
pairing を導出する。さらに independently replay した actual correction row を同 reducer に
`add_actual` し、selected pivot、rank-after、selected formal solution、exact coordinate を照合する。

この独立値は V の必須 field `independent_raw_reconstruction` に入り、driver lines 282--285 も
`parsed_once`、annihilation、`2896 -> 2897`、pairing、coordinate を gate する。V はその独立再構成
後にのみ physical R bytes/SHA/self/semantic seals と heavy carrier を bind する。raw DOM は
triangular immutable snapshot を借用した後に解放される。

### 2.4 Real ordinary-owner mutation routes

fixture は triangular 8、boundary 13、selected-correction 30、positive 7、physical 11、phase 4、
phase-positive 2 を、owner path、ordinary validator、stage、exact first reason まで固定した。
producer/checker はそれぞれ独立に ledger を構成する。

- triangular は authenticated raw columns の untouched baseline と、変更対象の小さい最初の三
  recordsだけを使い、全 case が同じ chronological validator を通る。
- boundary は pre-heavy に実際に走らせた extant W4 outcome、実 fault cleanup、実 blocked-send
  evidence の owner/route/cleanup projection を使う。mutation はその ordinary owner の physical
  fieldを変更し、同じ transport/authority validator を通る。Boolean-only boundary frame はない。
- selected-correction/positive は上記 actual current-dual owner と ordinary correction/direct replay
  validator を使う。
- phase/phase-positive は global ordinary `producer_validate_phase_transition`
  (producer 5342--5502) および独立な checker counterpart (checker 4530--4692) を共有する。
  miniature `phase-owner-frame` と nested special validator は削除した。二つの positive gate も
  physical transition owner を同じ validator に渡す。
- physical suite は authenticated R baseline を borrow し、top carrier と変更 claims だけを
  shallow copyする。full R clone はない。

expected first reason 以外、wrong reason、mutation acceptance、arbitrary exception は narrow expected
catch の外に残る。producer/checker は最後に independently normalized ledger を fixture と比較し、
checker lines 4919--4924 は producer と checker の normalized ledger exact equality と digest まで
要求する。

### 2.5 Linear bounded ancestry DAG

producer `AncestryDAG.expand` (lines 251--300) は node ごとの full dictionary memo を削除した。
node id が children より後に発行される topological invariant を使い、descending pass で一個の
`weights` sparse mapを伝播し、一個の `answer` に literal を fold する。従って expansion は
`O(number of scanned nodes + traversed literal entries)`、live sparse entries は常に

`len(weights) + len(answer) <= 2,000,000`

である。new key は insertion 前に chargeし、node cap、answer cap、aggregate live-entry cap の
どれかで typed stop する。`dict(memo[left])` と `Theta(d^2)` live/copy witness は消えた。
checker lines 1145--1195 は helperを共有せず、独自 DAG/reducer と同じ aggregate-before-insert
bound を再実装する。

### 2.6 重複処理、Gamma、cache、phase release

P0/source/raw/fixture は各 owner を物理認証した一つの snapshot registry から再利用する。
checker の反復 P0/source/fixture reauthentication、反復 parent digest/walk、triangular full-frame
canonical clone、R 内の二重 triangular serializationを削除した。source raw/DOM、decoded task176
streams、selected K0、ten Q0 stores、qstate/qid、parents/letters、memberships、projection、walk/digest
cache は last consumer 後に clear/release する (producer 5611--5649, 5886; checker 4025,
4895--4972)。known-Q0 duplicate は coordinate work 前の early skip を維持した。

full Gamma 4,814-byte state は全243 statesを計算/hex化せず、typing canary一個と actual selected
owner一個だけに限定した。load-bearing projected Gamma は `243*970=235,710` bytes である。
`pc_cache` は cardinality `131,072` と insertion-attempt counterを pre-insertion で制限し、phase
終了時に解放する。

### 2.7 R/V publication と static live-memory model

R/V とも canonical construction 前に output hard cap 全量 `536,870,912` bytes を reserveし、
encoded sizeを再検査する。publication は exclusive temp create、file fsync、no-replace hard link、
directory fsync の順で、replaceを許さない。mutation は baseline借用 + sequential one-small-owner
copyで、triangular/R full cloneを保持しない。driver artifact gate は Rを検査して必要な小 summary
だけを残し `receipt.clear()` してから Vを読む。最後の physical R/V rehash は各一個ずつ1 MiB block
でstreamするため、R DOM + V DOM や R+2V rawを同時保持しない。

sourceに固定した producer conservative live formula は

`1,425,574,080 ten-Q0 stores`
`+ 52,907,904 Q0 roster`
`+ 243,105,472 selected K0 maximum`
`+ 345,472,156 raw bytearray/bytes/ASCII/DOM`
`+ 235,710 projected Gamma`
`+ 536,870,912 output reservation`
`= 2,604,166,234 payload/output bytes`

に CPython/COW/mutation reserve `2,295,833,766` を加えた `4,900,000,000` bytesである。
RSS hard cap `5,700,000,000` に対して static margin は `800,000,000` bytes。

checker は

`345,472,156 raw + 243,105,472 K0 + 60,492,663 decoded owners`
`+ 536,870,912 V reservation = 1,185,941,203 bytes`

に CPython/R-mutation reserve `3,414,058,797` を加えた `4,600,000,000` bytes、同じ RSS capに
対して margin `1,100,000,000` bytesである。これは source-derived conservative boundであり、
未実行なので observed peak の主張ではない。

### 2.8 IPC、typed UNKNOWN、deadlines

normal W2/W4 は一つの meter で順に走らせ、timeout/death/partial は各一回だけ sequential W2、
blocked-send は一回だけである。全 normal/fault の frames/bytes/STOP/restart 等は additive sum、
accumulator/RSS等の physical gauge は maximum、simultaneous child peakは4とした。meter は実 child
PID の RSS sumを sampleする。heavy後に新しい W4を forkする非荷重経路は削除し、pre-heavy の
extant W4 outcomeをheavy後のboundary suiteが検査する。従って post-heavy spawn/IPC/STOP/restart
は resetで隠したのではなく source上0である。OS exception class name は semantic reasonに
serializeせず、固定 typed reasonだけを記録する。

producer top-level lines 5928--5944 と checker lines 4994--5004 は、rollback/cleanup後の
`InputStop`/`ResourceStop` を canonical `UNKNOWN_INPUT`/`UNKNOWN_RESOURCE`（platform は
`UNKNOWN_PLATFORM`）terminalに正規化する。positive artifactやsentinelは生成しない。

deadlineは内部/外部の順に producer `9600/9900`、checker `5400/5700`、artifact
`1200/1500` seconds。external sumは `9,900+5,700+1,500=17,100`、outer `18,000` まで
`900` secondsのstrict margin、workflow `21,600` まで setup/cleanup/upload `3,600` secondsを
残す。v12a の zero-margin schedule はない。

### 2.9 Driver/platform/candidate-only boundary

driver は `.g` 全体をASCIIに限定し、directory作成を GAP native
`IsDirectoryPath`/`CreateDir` (lines 87--91) にした。P0 は GitHub Actions
`ubuntu-24.04`、`x86_64`、CPython 3.13、Linux fork、AF_UNIX、O_NOFOLLOW、`/proc` RSS、固定
coreutilsを明示する。driver lines 118--120 と producer/checker heavy前 preflight
(producer 5817--5822; checker 4761--4766) がこの境界をtypedに拒否する。shell paths/argumentsは
固定 quoted literalsである。

driver は heavy前に production/resume/stale/temp aliasを拒否し、producer/checker terminalを
exact-one full lineで照合し、R/V constructor field sets、false claims、physical R binding、
independent raw reconstruction、post-validation rehashを通した後だけ neutral sentinelを
no-replace/fsyncで作る。failure/UNKNOWNにはaccepted candidateが残らない。P0/R/Vはいずれも
`candidate_only=true`、`production_authorized=false`、`resume_authorized=false`、
`FORBIDDEN_PENDING_INDEPENDENT_AUDIT`である。

## 3. 静的閉鎖チェック

read-only PowerShell だけで、P0/fixture JSON parse、両self-sealのcanonical再計算、P0 source rows、
fixture physical row、driver四pin、`.g` ASCII-only、旧v12a hash/`TO_BE_RESEALED`/
`phase-owner-frame`/`mkdir -p`/OS exception-class reasonの残存がないことを照合した。これは
syntax compilationやcandidate executionではない。次の独立静的監査がこの版を受理するまで、
GHA dispatch、production、resumeは禁止のままである。

A0/V12B VERSIONED OWNERS:               COMPLETE
TASK368 F1 CHRONOLOGICAL PIVOTS:         REPAIRED
TASK368 F2 ACTUAL CURRENT DUAL:          REPAIRED
TASK368 F3 CHECKER RECONSTRUCTION:       REPAIRED
TASK368 F4 REAL MUTATION ROUTES:         REPAIRED
TASK368 F5 LINEAR BOUNDED DAG:           REPAIRED
TASK368 F6 MEMORY / DUPLICATION:         REPAIRED
TASK368 F7 R/V / DEADLINES / PLATFORM:   REPAIRED
LOCAL CANDIDATE EXECUTION:               NONE
V12B SELFTEST_BOOTSTRAP GHA:             FORBIDDEN PENDING INDEPENDENT AUDIT
PRODUCTION / RESUME:                     FORBIDDEN
ACTUAL A0 COMMON + CHECKER:               0/1
LIFT / FAKE / IHARA:                     NONE

TASK372_R07_A0_V12B_MINIMAL_COMPLETE_REPAIR
