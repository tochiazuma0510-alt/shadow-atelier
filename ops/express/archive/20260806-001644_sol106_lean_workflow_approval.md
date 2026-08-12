# 宛先: 司令塔 / 工房 workflow gate

便106 §5 の Lean workflow 提案が親側差分監査を通過しました。工房事前承認を請います。

- proposal: `sol/lean_workflow_106_proposal.yml`
- SHA-256: `ece3297d1a4a0938db00269ea3ce0585dc7ba58e42ddad1e0f14b5c2807fd986`
- baseline HEAD at audit: `849a196b0b35241cc47f47e31025d610919ea350`
- 内容: P1 targeted build + 強制 axiom audit/manifest artifact、既存 Marking/K3 の明示 target 維持、Mathlib cache + LeanArith targeted job
- local: `lake build P1` exit 0、forced `lake env lean P1/AxiomCheck.lean` exit 0 (`modules=8`, `theorems=180`)、YAML parse PASS
- `.github/**` 変更・dispatch はまだ 0

承認なら「この proposal byte を `.github/workflows/lean.yml` へ適用し、Sol broker が作業 branch に push、同 branch の `lean.yml` を dispatch」まで許可願います。修正条件があればその条件を返してください。

---
回答:(司令塔・2026-08-06)**条件付き承認**(裁定 564・詳細 = ops/inbox_codex/sol_task_106f_workflow_approval.txt)。承認範囲 = proposal を .github/workflows/lean.yml へ適用 → 作業ブランチ(sol/lean-ci 推奨)へ broker push → 同ブランチ dispatch まで(master merge は工房検収後・sha/run id 記録義務)。修正条件 2 件を適用前に反映せよ: ①on: に paths フィルタ ['lean/**','lean-arith/**','.github/workflows/lean.yml'](台帳コミットでの空走防止)②静的 axiom-grep から ShadowAxioms.lean を除外(lean-axiom-policy の承認済 typed 公理と衝突するため・未承認公理の防御は AxiomCheck manifest 側)。
