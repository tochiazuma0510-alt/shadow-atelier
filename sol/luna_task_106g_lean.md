# Luna 委嘱 106g-Lean — LA-2〜LA-5 独立着工束

## 0. 役割・目的

あなたは Luna（Lean 実装増援）。便 106g の次波のうち、T2 に依存しない `lean/P1/BlockA.lean` の LA-2〜LA-5 を、紙 `docs/notes/oddH_full_proof_v1.md` 補題 C(2)・G・H・I と 1:1 に実装する。

現 `BlockA.lean` 末尾の「LA-2〜LA-5 は LA-6 の GAP が解消するまで着工しない」は依存方向が逆である。LA-2〜LA-5 が LA-6（Lambda-REG）の入力を供給する。まずこの注記を訂正し、実装可能な theorem island を閉じる。

## 1. 六点 delegation envelope

1. **入力**: remote branch `sol/task106-math33-20260806` の現 head、`lean/P1/{Core,FinArith,Parity,Order,BlockA}.lean`、`docs/notes/oddH_full_proof_v1.md` §2–§4、`docs/notes/lean_p1_allocation_plan_v1.md` LA-2〜LA-5。
2. **出力**: LA-2〜LA-5 の real definitions/theorems、必要最小限の補助補題、更新した statement map/axiom receipt、`sol/luna_reply_106g_lean.md`。既存 theorem 名・意味を壊さない。
3. **禁止**: `axiom` / `sorry` / `admit` / `native_decide` / no-op `True`、T2 宣言追加、Bridge B、`lean-arith/**`、`.github/**`、credential 読取、git commit/push、bare `lake build`。既存 reply・紙文書・探索資産を変更しない。
4. **停止条件**: 紙の statement と現型の間に一意に埋められない差がある、または LA-2〜LA-5 のどれかに Mathlib-only infrastructure が不可避なら、その項だけ OPEN とし、最小 counter-type/blocker を報告する。弱い別定理を同名で代用しない。
5. **検収**: `lean/` で targeted `lake build +P1.BlockA:olean` と `lake build P1`、AxiomCheck、`git diff --check`。各 theorem の paper correspondence、仮説、結論、exact axiom set を報告する。
6. **権限**: 実装と local candidate receipt のみ。paper-fidelity/PASS、T2 型批准、workflow、branch commit/push/dispatch は Sol 親に留保。

## 2. 型の最低条件

- `H_{j,alpha,beta}` は ambient `En n` の任意集合でなく actual `Gn n` 上の部分群述語として定義する。
- `j` は `{2,3}` の二値型にし、自然数の範囲仮定を毎 theorem に漏らさない。
- LA-2 は `[G_n:H]=2n` を無名の prose 仮定にせず、紙の使用形に必要な finite transversal/cardinality witness を名前つき型にする。
- LA-3 は少なくとも subgroup closure、`[G_n:H]=2n` に相当する exact finite witness、`<X> ∩ H = 1`、parameter injectivity を分離する。
- LA-4 は `normalizer(H)=H ↔ alpha ≠ 0` の両方向を actual conjugation predicate で述べる。
- LA-5 は conjugation formula と class characterizationを分け、`alpha=0` と `alpha≠0` の class-size 分岐を混同しない。
- plain Lean のため literal `Fintype.card` が不可能なら、LA-1 と同型の explicit `PlainEquiv` witness で exact cardinality を運ぶ。その場合、紙の cardinality theorem を閉じたと過大表示しない。

## 3. 作業場所

共有 dirty master には触れず、`%TEMP%` 配下に remote branch から独立 clone/worktree を作って作業する。完了時にその絶対 path と変更一覧を親へ報告する。親が差分を監査して broker commit を行う。
