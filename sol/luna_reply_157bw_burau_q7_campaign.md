# Luna reply 157bw — q=7 Burau campaign

判定: Q7_CAMPAIGN_READY

## 実装したもの

- search/d972_b4_burau_fiber_v5.py
  - v4 の凍結入力をそのまま保持: 972 行、word/target/tuple/semantic SHA、屋根の位数
    (1469664)、導来射影 (367416)、H'、完全 Schreier kernel、全 fiber。
  - B4 Burau の generator、pure generator、A.18 の5組、matrix defect
    (pentagon) を変更せず versioned v5 に移植。
  - prime field q=7 の全ての非零 a=1,2,3,4,5,6 を登録。q=7 の braid、
    distant commutation、行列可逆性を self-test で確認し、a=0 の拒否も確認。
  - q=5/q=7 の本走査は q3=(-1), q4=(2) の完全校正 receipt を必須にし、
    receipt の source SHA、972 行、各校正 fiber=8、identity=1、nonidentity=7
    を認証する。resource/error は zero として扱わない。
  - q=7 の terminal status は
    CANDIDATE_B4_A_BURAU_Q7_ZERO_FIBER または
    UNKNOWN_BURAU_Q7_SPECIALIZATION_ALLPASS の二択（校正不備は
    UNKNOWN_RESOURCE）。

- search/check_d972_b4_burau_fiber_v5.py
  - producer を import しない独立 namespace。
  - 屋根、Burau 行列、braid/commutation、A.18、tuple RS closure、H'、kernel、
    全 kernel element、972 target key、全 fiber digest、各 defect count を receipt
    から再構成して照合。
  - q=7 の6値を独立に行列関係・可逆性 self-test。PaperProd 反転、x13、
    A.18 defect、roof word/key、kernel deletion、q7 a=0 の敵対的 fixture を含む。

- .github/workflows/d972-burau-q7-v1.yml
  - q3/q4 calibration job 成功後に q=7, a=1..6 の6 laneを起動する。
  - workflow_dispatch と対象 branch/path の push trigger を登録。
  - actions: read, contents: read のみ、checkout は全て persist-credentials: false。
  - Python 3.13.5、SymPy 1.14.0 と mpmath 1.3.0 を SHA256 hash pin。
    各 job は timeout-minutes: 360, ulimit -v 12000000。
  - calibration/q7 の全 evidence を if: always(), compression-level: 0 で保存。
    producer/checker source SHA と frozen word artifact SHA を実行時に固定照合。
  - aggregate は6 receipt、6 producer terminal marker、6 independent checker pass、
    status/count整合、resource/error不存在を全て確認してから一つだけ
    D972_B4_BURAU_Q7_CAMPAIGN_FINAL を出す。欠 lane・UNKNOWN_RESOURCE・checker
    欠落時は terminal marker を出さず失敗する。zero は checker PASS 後のみ candidate
    に昇格する。

## 軽量ローカル検査

実行したコマンド:

- python -m py_compile search/d972_b4_burau_fiber_v5.py search/check_d972_b4_burau_fiber_v5.py
- python search/d972_b4_burau_fiber_v5.py --self-test
- python search/check_d972_b4_burau_fiber_v5.py --self-test
- python -c "import pathlib,yaml; ..." による YAML/jobs/matrix/permissions/placeholder 静的監査

producer 出力:

- D972_B4_BURAU_FIBER_V5_Q7_PARAMETER_NEGATIVE_PASS
- D972_B4_BURAU_V5_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS
- D972_B4_BURAU_FIBER_V5_NEGATIVE_FIXTURES_PASS
- D972_B4_BURAU_FIBER_V5_SELFTEST_PASS

checker 出力:

- D972_B4_BURAU_FIBER_V5_Q7_PARAMETER_NEGATIVE_PASS
- D972_B4_BURAU_FIBER_V5_SOURCE_WORD_ROOF_ONLY_NEGATIVE_PASS
- D972_B4_BURAU_FIBER_V5_CHECKER_SELFTEST_PASS
- D972_B4_BURAU_FIBER_V5_CHECKER_FINAL_MARKER status=PASS
- Q7_WORKFLOW_STATIC_PASS

q=7 の972行本走査はローカルでは実行していない。したがってこの便は数学的な zero/all-pass の結果を主張せず、GHAで実行可能な versioned campaign の準備完了を報告する。

## SHA-256

- producer
  706b094b6fd434a04abdaf88b64e023c88151e4132dbceed765e2f9dc942a1e7
- checker
  eed56e60ff92bf819e80b42b68a7fcf97aaa65c3c16cc6e8dfdc38c678114a1b
- workflow
  3c045582b3dfcdda69bda732d1c8760b373a038d34ea9e861a6737adde26e9d9
- frozen word artifact
  564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9

ローカル GAP、Git、push、dispatch、GHA、本走査は行っていない。

Q7_CAMPAIGN_READY

Parent pre-dispatch audit repaired the mpmath wheel hash typo and added an
RLIMIT_AS byte-level assertion in both compute stages; the workflow hash above
is the post-repair value.
