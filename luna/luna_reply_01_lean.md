# Luna 01 — Lean F105-6.4 receipt

`ops/inbox_codex/luna_task_01_lean.txt` は先頭から末尾まで（9行、`初回任務`・`拘束`・`納品`を含む全節）読了した。turn 冒頭に `docs/対話帳.md` の T-1〜T-28 も確認した。対象は mail の指定どおり `lean/` の現 HEAD であり、Lean ソース・workflow・既存台帳は変更していない。commit/push はしていない。

## 1. F105-6.1 — local plain Lean build facts

実行したコマンド:

```text
cd lean
lake env lean P1/AxiomCheck.lean
lake env lean P1/BlockA.lean
lake env lean P1/BlockE.lean
lake env lean P1/ShadowAxioms.lean
lake build
```

個別コマンドの結果:

```text
lake env lean P1/AxiomCheck.lean    exit 0
lake env lean P1/ShadowAxioms.lean exit 0
P1/BlockE.lean:33:8: warning: declaration uses `sorry`
P1/BlockA.lean:83:23: warning: Variable name `hH` is not explicitly referenced.
P1/BlockA.lean:84:5: warning: Variable name `hstab` is not explicitly referenced.
P1/BlockA.lean:112:8: warning: declaration uses `sorry`
P1/BlockA.lean:127:8: warning: declaration uses `sorry`
```

`lake build` は約20分観測しても完了せず、標準出力を返さないまま Lean の CPU 時間だけが増加したため停止した。これは build PASS ではなく `INCOMPLETE/UNKNOWN` である。GHA の plain build receipt もこの checkout には存在しない。`.github/workflows/lean.yml` は `lake build` と `sorryAx`/`native_decide` grep を定義しているが、生成済み artifact/log は確認できなかった。

## 2. F105-6.2 — paper fidelity blocker

現状は file-level `verified` ではない。`verified-modulo-axioms` と呼ぶにも、現在の `AxiomCheck.lean` は12宣言への手動 `#print axioms` のみであり、mail が要求する全量 inventory、unexpected axiom/sorryAx の自動 fail、exact sorted per-theorem receipt、type digest、生成 AXIOMS manifest を実装していない。

確認できた blockers:

1. `BlockA.lean` に `INN_on_Y` と `inn_fixes_X` の2本の `sorry` がある。
2. `BlockE.lean` に `chiTilde_isUnit` の1本の `sorry` がある。合計3本。
3. `Gn_card_placeholder : True` は `|G_n| = 4n^3` を型に持たない no-op。
4. `Lambda_simplyTransitive ... : True` は `hH`/`hstab` を使わず、LA-6 の simply-transitive statement ではない。unused argument warning も確認した。
5. `ShadowAxioms` の次の4本は bare `Prop` axiom であり、paper theorem の exact statement・全 hypothesis・sanity instance を型に束縛していない。

   - `T2_thm43_explicit_isolated`
   - `T2_thm43_isolated`
   - `T2_15_Ih_decomp`
   - `T2_composition_hom`

6. `E_n`/`inG` は ambient model の定義であり、現 `BlockA` には実 `G_n` subtype/group closure/cardinality の完成した形式化がない。

したがって第1波全体の受入れは `FAIL / 差戻し`、個別に `sorry` なしで走った小補題だけが限定的な candidate receipt である。

## 3. F105-6.3 — allocation judgment

既存 `docs/notes/lean_p1_allocation_plan_v1.md` と policy を照合した。Block A/E/H が paper 上の候補島であることは変わらないが、現ファイルの acceptance は次のとおり。

| block | 現状 | 根拠 |
|---|---|---|
| H / TORS-U | 未実装・receipt なし | `lean/` に TORS-U の Lean declaration がない |
| A | FAIL / foundations incomplete | `True` placeholder、2 sorry、実 Gn subtype/cardinality 不在 |
| E | FAIL / sorry 残存 | `chiTilde_isUnit` が sorry、後続 LE statement は bare T2 に依存 |
| Bridge B | defer | local plain Lean での concrete finite-étale 層・Galois bridge がない |
| T2 依存 | quarantine 必須 | bare Prop 4本を exact statement 承認前に使用不可 |

Mathlib coverage survey は版相対の調査資料であり、GHA receipt ではない。したがって `T1_cyclotomic_ram2` の討ち取り見込みを closed とは扱わない。現段階では paper↔Lean fidelity の受入れ条件を満たさない。

## 4. F105-6.4 — 初回指示 8項目の処理状況

| # | 指示 | 今回の処理・判定 |
|---:|---|---|
| 1 | plain Lean のみ、Mathlib は隔離 | 実行は `lean/` の plain 層のみ。Mathlib build は行っていない。GHA receipt は UNKNOWN。 |
| 2 | bare-Prop T2 axiom と `True` を quarantine | 現 source は未修理。4 T2 bare-Prop、`Gn_card_placeholder`、`Lambda_simplyTransitive` を blocker として quarantine 判定。 |
| 3 | fail-closed axiom checker、inventory、sorted set、digest、manifest | 既存 checker の不足を確認。新 checker/manifest は今回生成していないため OPEN。 |
| 4 | Block H first / TORS-U | `lean/` に実装なし。着工 receipt なし。OPEN。 |
| 5 | Block A foundations | `Gn_X_eq_a1_q1`、`Gn_X_sq`、`Gn_ord_X` は存在するが、Gn subtype/cardinality/Λ は未完。FAIL。 |
| 6 | Block E | `chiTilde_welldefined` は plain Lean で通るが、`chiTilde_isUnit` は sorry。file-level grade は付与不可。 |
| 7 | T2 statement table を Sol 承認前に追加しない | 現 source の4 bare Prop を採用せず、paper↔Lean 対応を下表の candidate/open として記録。 |
| 8 | versioned 納品物 | 今回の指定納品は本返信のみ。build/manifest/receipt の新規ファイルは未生成。 |

## 5. Existing AxiomCheck per-theorem receipt

`lake env lean P1/AxiomCheck.lean` の実出力。これは **12宣言だけ** の receipt であり、全 theorem inventory の代替ではない。

| theorem | exact sorted axiom set | result |
|---|---|---|
| `X_pow_2n` | `propext`, `Quot.sound` | candidate |
| `X_pow_lt_2n_ne` | `propext`, `Quot.sound` | candidate |
| `epow_fst` | `propext` | candidate |
| `epow_snd` | `propext` | candidate |
| `epow_thd` | `propext` | candidate |
| `dpow_rot_flag` | `propext` | candidate |
| `dpow_rot_val` | `propext` | candidate |
| `dpow_refl_even` | `propext`, `Quot.sound` | candidate |
| `dpow_refl_odd` | `propext`, `Quot.sound` | candidate |
| `Gn_X_eq_a1_q1` | `∅` | candidate |
| `Gn_X_sq` | `propext` | candidate |
| `Gn_ord_X` | `propext`, `Quot.sound` | candidate |

No `sorryAx` or `ShadowAxioms.*` appeared in this 12-item output. This fact does not clear the uninspected declarations or the three source `sorry` warnings.

## 6. Paper ↔ Lean statement map (current evidence)

| paper item | Lean declaration | current fidelity |
|---|---|---|
| LA-1(a), `X=a₁q₁` | `Gn_X_eq_a1_q1` | concrete equality, no extra axiom in receipt |
| LA-1(b), `X²=a₁²` | `Gn_X_sq` | theorem passes; `propext` baseline |
| LA-1(c), `ord(X)=2n` | `Gn_ord_X` | theorem passes; `propext`, `Quot.sound` baseline |
| LA-1(d), `|G_n|=4n³` | `Gn_card_placeholder : True` | FAIL: no cardinality statement |
| LA-6, Λ simply transitive | `Lambda_simplyTransitive : True` | FAIL: no statement content; hypotheses unused |
| LA-8, `Phi_{0,f_k}=inn(X^{-2k})` | `INN_on_Y`, `inn_fixes_X` | OPEN/FAIL: both sorry |
| LE-1(a), well-defined χ~ | `chiTilde_welldefined` | concrete arithmetic theorem passes |
| LE-1(a), unit/coprime part | `chiTilde_isUnit` | OPEN/FAIL: sorry |
| LE-1(b), χ~∘Ih | `T2_15_Ih_decomp : Prop` | FAIL as Lean fidelity: bare Prop axiom |
| Thm 4.3 / isolated | `T2_thm43_explicit_isolated`, `T2_thm43_isolated` | FAIL as Lean fidelity: bare Prop axioms |
| composition (3.53) | `T2_composition_hom : Prop` | FAIL as Lean fidelity: bare Prop axiom; integer identity is separately proved |

## 7. Deliverable status / blockers

The five requested deliverable classes are recorded honestly as follows:

| requested artifact | status |
|---|---|
| local plain build log | `UNKNOWN/INCOMPLETE`: `lake build` observed for ~20 min, then stopped without completion output |
| GHA build receipt | `UNKNOWN`: workflow exists, artifact not present locally |
| generated AXIOMS manifest | `OPEN`: no generator; `lean/AXIOMS.md` is manual and incomplete for the required gate |
| per-theorem receipt | `PARTIAL CANDIDATE`: 12 `#print axioms` rows above only |
| paper↔Lean statement table | supplied above; multiple FAIL/OPEN rows |

Primary blocker is not a Lean syntax error: it is the exact policy failure already identified by F105-6.2 — incomplete statements, three sorry declarations, four bare T2 Props, and a non-exhaustive checker. No claim of `verified` is made.

## 8. Scope audit

No Lean source, `lean/AXIOMS.md`, workflow, or existing receipt was modified. The only new worktree file from this task is:

```text
?? luna/luna_reply_01_lean.md
```

The repository already had unrelated dirty/untracked files before this task; they were not touched. No commit or push was performed.
