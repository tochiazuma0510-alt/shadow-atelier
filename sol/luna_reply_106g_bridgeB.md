# Luna 返信 106g-BridgeB — affine A0

**総合判定: A0 local type/API spike は PASS。Bridge B 全体は引き続き NO-GO。**

## 1. 作業境界・provenance

- 独立一時 repo:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-luna106g-b0b23ce9e00145629c7479f5576be1ea`
- 基底 remote-tracking commit:
  `b630ab050722cbc9703507dd74d5e3462d6b6b02`
  (`sol/task106-math33-20260806`)
- 委嘱 SHA-256:
  `4ee5ea6a0f1bd72237c3ac457e4102dd96dc9b6a22b22ac0a09a057cfe56e50f`
- 固定 mathlib:
  `v4.32.1` / `520045ab14e26149ee970e2e617ca04b09bde5d6`
- credential 読取、commit、push、dispatch、依存更新は行っていない。

## 2. A0 実装結果

新規 file:
`lean-arith/LeanArith/BridgeBAffine.lean`

SHA-256:
`4d8d1f1b743c80a12bbf7a16b6e6b976e45dcc10637dd15137990e8879d945aa`

| 要求 | declaration | 結果 |
|---|---|---|
| `A_U=k[t,t⁻¹,(t-1)⁻¹]` | `puncturePolynomial`, `AU` | `Localization.Away (X*(X-1))` として定義済み |
| 被覆圏の向き | `CoverCategory` | `(CommAlgCat.FiniteEtale A_U)ᵒᵖ`。opposite を保持 |
| 幾何点 | `geometricPoint` | `[Field Ω] [IsSepClosed Ω] [Algebra A_U Ω]` から `algebraMap A_U Ω` を明示 |
| fiber functor | `fiber` | `CommAlgCat.FiniteEtale.fiber A_U Ω` を exact API で定義 |
| affine π₁ 候補型 | `PiOneCandidate` | `CategoryTheory.Aut fiber` |
| PreGalois 接続点 | `PreGaloisGoal` | goal type のみ。instance/theorem は生成しない |
| FiberFunctor 接続点 | `FiberFunctorGoal` | caller が `[PreGaloisCategory CoverCategory]` を供給した下での goal type のみ |

`PreGaloisGoal` と `FiberFunctorGoal` は未証明 obligation である。tangential base
point、`π₁ ≅ F̂₂`、慣性元、TB1/TB3/TB4、EXSEQ のいずれも主張していない。

## 3. exact imports

1. `Mathlib.Algebra.Polynomial.Basic`
2. `Mathlib.RingTheory.Localization.Away.Basic`
3. `Mathlib.RingTheory.Etale.Finite`
4. `Mathlib.CategoryTheory.Galois.Basic`
5. `Mathlib.CategoryTheory.Galois.Topology`

manifest/toolchain/workflow は変更していない。

## 4. 型検査

固定 rev の既存 local cache を読み取り専用で用い、次を実行した。

```powershell
lake env lean 'C:\Users\81905\AppData\Local\Temp\shadow-atelier-luna106g-b0b23ce9e00145629c7479f5576be1ea\lean-arith\LeanArith\BridgeBAffine.lean'
```

- 最終 exit code: **0**
- warning/error: **なし**
- package 全体の local build は委嘱どおり省略。親 branch 上の GHA が最終検収。

禁止構文 scan:

```text
^\s*axiom\b|\bsorry\b|\badmit\b|native_decide|Lean\.ofReduceBool|:\s*True\b
```

`BridgeBAffine.lean` 内は **NO_MATCH**。

## 5. 固定版 source search

対象を mathlib の
`Mathlib/RingTheory/Etale/**` と `Mathlib/CategoryTheory/Galois/**` に限定し、
次の四パターンを再検索した。

- `FiniteEtale.*PreGaloisCategory`
- `PreGaloisCategory.*FiniteEtale`
- `FiniteEtale.*FiberFunctor`
- `FiberFunctor.*FiniteEtale`

すべて **NO_MATCH**。したがって A0 は両 instance を既在扱いせず obligation のまま
保持する、という委嘱の停止境界と一致する。

## 6. 同じ temp repo にある LA 引取差分

親指示に従い、末尾 ledger と statement map/receipt を partial scope に同期した。

- 実装済み: actual `Gn n` 上の `window.J/Code/H`、subgroup closure、
  `Code n ≃ H` carrier witness、`split/join` canonical-decomposition foundation
  (LA-3 の核)。
- OPEN: generic LA-2、LA-3 の marking-independent coset-index witnessの family 実体化、
  `XCode=⟨X⟩` の oddness bridge、P3 theorem、parameter injectivity、LA-4、LA-5。
- `PAPER_STATEMENT_MAP.md` は上記 partial scope を明記し、弱い同名 theorem を closed と
  表示していない。
- 生成済み `AXIOMS.manifest.json`: schema `p1-axiom-manifest/v2`、
  theoremCount `242`、allowed union
  `{propext, Classical.choice, Quot.sound}`、project axiom declaration `0`。
- `Index2nWitness` は `IsSubgrp H` と
  `Fin (2*n) ≃ LeftCosets H` を同時に要求する marking-independent P1 型。
- `AxiomAudit.receipt.md` を theoremCount `242` と新規主要 theorem の exact digest/
  axiom set に同期した。
- `lake build +P1.BlockA:olean`: exit code **0** (warnings only)。

## 7. 変更一覧・hygiene

- `lean-arith/LeanArith/BridgeBAffine.lean` (new)
- `lean/P1/BlockA.lean`
- `lean/P1/PAPER_STATEMENT_MAP.md`
- `lean/P1/AxiomAudit.receipt.md`
- `lean/P1/AXIOMS.manifest.json` (generated)
- `sol/luna_reply_106g_bridgeB.md` (this reply)

`git diff --check`: **PASS**。

親への引渡し判定は「A0 の型/API は採用候補、PreGalois/FiberFunctor 以降は未証明」
である。
