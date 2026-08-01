# N∞ stage-2 freeze receipt(commander・便99 F99-5.2 / 裁定412)

> **本稿は機械生成である。** 生成器 `search/gen_ep_freeze_receipt_sol99.py`、正本 JSON `search/certs/ep_freeze_receipt_sol99_20260802.json`。digest は全て repository の実ファイルから再計算し、Sol 返信 §5 の宣言 block から機械抽出した値と突合して一致した場合にのみ発行される(不一致なら発行せず停止)。

- receipt_id: `mb/ninfty-stage2-freeze-receipt/sol99/92025385-8f26416b-72623050`
- freeze_id: `mb/ninfty-stage2-freeze/92025385-8f26416b-72623050`
- authorized_by: `sol/sol_reply_99_math26.md` F99-5.2 (sol_freeze_gate = PASS) / F99-5.1 (lane B independent producer 実装認可)(sha256 `8f0e9b5c2379c55867195ad7eacca4c263a6825494c5b344cd3778368bbadf9f`・裁定412)
- issued_at: 2026-08-01T15:34:31.085136+00:00

## 束縛する artifact(4 点)

| artifact_id | path | sha256 | Sol 宣言値と一致 |
|---|---|---|---|
| `mb/ninfty-stage2-predicate/v20` | `docs/week4-NInfty_stage2_spec_v20.md` | `92025385eed864ca036df3f59153597fd60dc5ca3a66a04fd21251a51563ec3a` | yes |
| `mb/ninfty-verifier-contract/v15` | `docs/mb_ninfty_verifier_contract_v15.md` | `8f26416be35a34251efdbf24188826705fe7a8417243bd61cb5ecfbcda004fab` | yes |
| `mb/dependency-manifest/v15` | `docs/mb_dependency_manifest_v15.md` | `72623050cca3fef45b09e458ef671a4d6bfc8d9038959b98b0ff586e121a66db` | yes |
| `bundle-selfaudit/v11` | `search/bundle-selfaudit-v11.py` | `fd56c4f6457926ff4897de1e6924cad0a416891f5b1253f287b327b5ceec9e37` | yes |

## byte 凍結のまま残る前版(上書きしない)

- `mb/ninfty-stage2-predicate/v19` — `docs/week4-NInfty_stage2_spec_v19.md` — `620c7b2c2c76e27c0a76c2c1ff297966e5eb70d34975d5f32e916bd94bf5e8d3`
- `mb/ninfty-verifier-contract/v14` — `docs/mb_ninfty_verifier_contract_v14.md` — `1eba5c943105d433660b0ddcf7d2e3ba2264cdeb8490e297a351a2391d1fe94e`
- `mb/dependency-manifest/v14` — `docs/mb_dependency_manifest_v14.md` — `e892be68e79244c8493e37ec77eb3a1cbdb29ee45a911f73040aadaebbb889af`

## 発効対象(scope)

- the W6KEY-plane specification bundle (spec v20 / contract v15 / manifest v15 / bundle-selfaudit v11) is ADOPTED
- the lane B independent per-point W-6 producer implementation scope (F99-5.1), under the acceptance conditions restated in `lane_b_conditions`

## 発効対象**外**(この freeze PASS から導出することを禁じる)

- **W6_CLOSED=true**
- **IMAGE-MU=PASS**
- **EP detector activation / mint**
- **positive-control event**
- **candidate acceptance or Freeze 2 unlocking**

> Sol 便99 F99-5.2 verbatim: these may not be implicitly derived from the same freeze PASS. A green suite, a green CI job and a completed lane B producer move none of them.

## lane B per-point producer の受入条件(F99-5.1)

- lane B constructs each rational root's exact witness from its OWN curve/native data
- lane B imports/reads no lane A producer, canonicaliser, branch-token helper or output token; only the normative schema and its literals are shared
- finite points carry the x-root AND the y-root rank; infinity carries its own branch; the total degree-12 accounting is reconstructed from the per-point records
- both R1' and R2' are exercised, with mutation/negative fixtures and source digests, fail-closed
- diagnostic_construction=true, W6_CLOSED=false; AGGREGATE stays ABSENT until lane B exists
- even with lane B complete, only the AGGREGATE plane closes: IMAGE-MU stays UNKNOWN, so W-6 is OPEN and EP stays uncalibrated/UNKNOWN

## era 遷移(PENDING_ADOPTION → ADOPTED)

- 根拠: governing spec sec.5.3.4 M-7 / dependency manifest Y-3c (宣言先行・採用後行)
- era: `mb/ninfty-stage2-predicate/v20` / `mb/ninfty-verifier-contract/v15` / `mb/dependency-manifest/v15`
- plane `w6_key_route`: `search/ninfty-w6-key-gate-r1p.py`, `search/ninfty-w6-key-gate-r2p.py`
- plane `w6_point_map_producer`: `search/ninfty-w6-pointmap-lanea.mjs`, `search/ninfty-w6-pointmap-laneb.py`
- before this receipt the two ERA_W6KEY planes were recorded PENDING_ADOPTION and counted as neither PASS nor FAIL. From this receipt on they are evaluated exactly like every other plane: exact era match, no 'newer is fine'. The other planes (frozen_route_verifier / native_payload_schema / nf_route / decision_lane_predicate / control_plane) are UNCHANGED -- this receipt does not move them to v20/v15/v15.

## 札(receipt が明記する状態)

- ep_status = `uncalibrated/UNKNOWN` / w6_closed = `False` / IMAGE-MU = `UNKNOWN` / calibrated_detector = `False`
- spec sec.5.3.7 RC-1..RC-4: this receipt binds ONLY the fields written in it. Suite check counts, green/red breakdowns and timings are NOT bound by it and must be cited with the suite log's own provenance.

## pending queue(そのまま保持)

- CR-11 implemented_checks layer = PENDING/UNKNOWN
- QD-6 bootstrap leaf lost guarantees = PENDING/UNKNOWN
- N-2(2)/H-1a'' independent rederive = PENDING/UNKNOWN

