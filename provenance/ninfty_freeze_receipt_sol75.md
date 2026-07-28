# N∞ stage-2 freeze receipt(commander・裁定 111)

- authorized_by: sol/sol_reply_75_math2.md F8(sol_freeze_gate = PASS・FAIL 0)
- predicate_spec_freeze_id: "mb/ninfty-stage2-freeze/e2c9c701-e41d51db-df59b25f"
- issued_at: 2026-07-28(commit 時刻を正とする)
- 転記方式: 以下の exact block は返信ファイル F8.4 から機械転記(sed 抽出・手写しなし)

```text
receipt_id =
  "mb/ninfty-stage2-freeze-receipt/sol75/e2c9c701-e41d51db-df59b25f"

predicate_spec_id =
  "mb/ninfty-stage2-predicate/v18"
predicate_spec_digest =
  e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56

verifier_contract_id =
  "mb/ninfty-verifier-contract/v13"
verifier_contract_digest =
  e41d51dbdbdcf66efaff2ccd073bbfba9bff12bbfff435ca290a4248abcf5022
verifier_contract_governing_spec_digest =
  e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56

dependency_manifest_schema_id =
  "mb/dependency-manifest/v13"
dependency_manifest_schema_digest =
  df59b25f75e8e48a4607ed39177e5aa15be5a3fd4c738391aec347d8f7c1cb3e
dependency_manifest_governing_spec_digest =
  e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56

external_dependencies = [
  "S5/S5-4-infinity",
  "S5/S5-3-infinity",
  "S5/prop-S5-1",
  "S5/prop-S5-2",
  "S5/cor-S5-2a"
]
external_dependency_blob_digest =
  b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555

allowed_shared_tcb        = []
allowed_shared_source_tcb = []
allowed_shared_build_tcb  = []
allowed_shared_family     = []

registry_definition_block_digest =
  e244bf1d738bb27314ff37feab936ba21a5291d015ea38a2e2d937726d55e204
selfaudit_script =
  "search/bundle-selfaudit-v8.py"
selfaudit_script_digest =
  8795893769bacc69f50eaecff3da22f0712eb97d459a4642d1d1c370e8070b4d
```

## 実装認可(F8.5・本 receipt 発行時点で効力発生)
searcher v2 / checker・verifier A/B = AUTHORIZED。separate implementations / runtimes / toolchains+build steps / decision・audit lane = REQUIRED。EP まで partial predicate / UNKNOWN。calibrated detector・complete search 宣言は EP 前 NOT AUTHORIZED。新 lane・TCB 拡張・scope 拡張は新 receipt 要。

## pending queue(このまま保持)
CR-11 implemented_checks layer = PENDING/UNKNOWN・QD-6 bootstrap leaf lost guarantees = PENDING/UNKNOWN・N-2(2)/H-1a″ independent rederive = PENDING/UNKNOWN
