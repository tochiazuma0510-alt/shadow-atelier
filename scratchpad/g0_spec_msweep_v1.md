# G0 仕様書 — B(m掃引)が答える命題(1ページ・工房側明文化)

状態: 工房側ドラフト(数学者=T-56原文/Def 3.12の逐語を持たない検問設計のため、工房がコードとdocsから再構成)。Sol/数学者の検分前。

---

## ① T-56 §4 の全称化条件(iv)、逐語(`docs/notes/branch_sweep_design_v1.md` 30-33行より)

> T-56 §4 の全称化条件(原文):
> (i) base pair と D2-prefix の固定を外し、(ii) seed span を補正領域 Λ **全体**へ広げ、(iii) 屋根像が A の外にある**全ての** g∈ML(H)(NA-5 により Sylow 3-部分群の生成系で足りる)にわたって全称化し、(iv) side gate 込みで走査宇宙の完全性証明書を付す — この4条件をすべて満たしたときに限る。

同ファイル訂正3の帰結表(discharge/非discharge):

| 掃引で discharge されるもの | されないもの |
|---|---|
| 軸C(27補正)+軸R(凍結6屋根行) ⟹ (i)の一部 | (i)の残り: D2-prefixの固定は外れない |
| 軸R ⟹ (iii)の一部(6行ぶん) | (iii)の本体: Syl₃(ML(H))の生成系は凍結物に無い |
| — | (ii): seed spanは108のまま |
| — | **(iv): 走査宇宙の完全性証明書なし** |

**⟹ B(m掃引)は(iv)を discharge しない。** m=0 cert(`koubou158_L3_radical_v1_1_20260822.json`)の `obs_star_note` も同じ結論を明記済み: 「(i)/(iii)/(iv) of T-56 remain unaddressed by this measurement — explicitly NOT claiming OBS*」。

## ② Def 3.12 の逐語(`docs/notes/ihnec_v1_addendum_e_b4.md` 102行より)

> **(SURV-DEF)** ★ **Def 3.12** (p.38): "*[(m,f)] ∈ GT♡(N) **survives into** K if [(m,f)] belongs to the image of the map (3.24).*"

「w-宇宙」= このsurvive写像(3.24)の像に属する (m,f) 対の全体(`docs/対話帳.md` 2391行「M1(w-宇宙一致)未決」・`sol/fable_to_sol_audit_972_koubou83_20260822.md`「M1 = w-宇宙とDef 3.12の一致確認が未」と同一概念として工房は使用している — **この同一視自体は未確認**(M1決着課題そのもの)。

## ③ msweepの入力relator・係数環・∇・V+im D̄₂(コードから転記)

- **入力relator**: `h1(m) = pp[y^m++f_xy, x^m++Inv(f_xz), z^m++f_yz]`(`search/koubou158_m2_closedform_v2.py` build_h1、m=0でfrozen target6.base_gradientとSHA完全一致)。RHS=1(hexagon恒等式の右辺は単位元、m=0の凍結relatorはe4.identityへ評価される — 本セッションG1で再確認、下記)。
- **係数環**: **F₃**(`koubou158_L3_core_v1_1.py` IndependentPc、Pi4[3]がexponent 3の3-群、`fox_gradient`の係数は`% 3`)。
- **∇の定義**: `fox_gradient(e4, word)` — 自由語wordを左から読み、各文字の直前累積値(e4群元)をキーに、+1/-1の係数(mod 3)を積算するFox微分。`project_to_pi`でQ4(順列)成分を捨てPi4[3]成分のみ残す。
- **V+im D̄₂ の定義**: `build_V_and_D2bar_from_q3(_complete)`(同ファイル)——
  - V = Schreier生成子(Δ/K/転換子構成、S1-S4)由来のσベクトル群のF₃張る空間(`sigma_vectors_pi`)。
  - im(D̄₂) = PB4の11関係式それぞれのFox勾配を種とし、apply_xi_minus_1(pc生成子×(gᵢ-1)倍作用)で深さj-1までBFS閉包した部分加群(submodule_closure_with_depth)。
  - 両者を合わせた`ech_combined`のrankと、対象語のprojectベクトルの被覆判定(reduce→pivot)がMEMBER/NON-MEMBER判定そのもの。

## ④ MEMBER/NON-MEMBER が discharge する命題(m=0 certの限定句・逐語継承)

m=0 cert (`koubou158_L3_radical_v1_1_20260822.json`) の逐語:

> **`mathematician_claim_note`**: "verbatim assertion as relayed by the commander 2026-08-22: 'nabla b NOT IN Sigma(K^(31)_E4) + im D2^full'. Preconditions: quotient_direction_certified (Theorem D′...); conditions (i), (iii), (iv) of T-56 remain UNRESOLVED by this measurement — the mathematician's instruction is to co-list this fact on the SAME line as the claim."
> **`obs_star_note`**: "(i)/(iii)/(iv) of T-56 remain unaddressed by this measurement — explicitly NOT claiming OBS* even though condition (ii) discharges here."
> **`early_stop_soundness_note`**: "a NO at level j (target not in M_j) is a SOUND, FINAL answer ... NO-DIRECTION ONLY IS SAFE."

**⟹ NON-MEMBER(NO)が discharge する命題は正確には**: 「この特定の base pair × D2-prefix 固定 × 登録108-seed 族 × 凍結6屋根行という**有界な宇宙の中で**、対象語のFox勾配クラスが V+im(D̄₂) に入らない」という**有界・非全称**の言明のみ。T-56(i)(iii)(iv)の全称化は一切discharge されない。「slice_settled_no」という語は前置きなしの独立命題として扱ってはならない——常にこの限定句を伴う。

## ⑤ P0のf(FIXED_WORD押し出し)はBのw宇宙に属すか

本日実測(scratchpad/audit_P0_naive_judge_v4.pyの関数を再利用):
```
f_pb4 (FIXED_WORD をcofaceへ押し出しただけ、m=0の凍結h1構成なし) == identity in e4 ?  False
```
**属さない**。f単体(h1(0)=C·B⁻¹·A の3枝合成を経ない生のFIXED_WORD)は、そもそもe4のGT-pair候補(=identity へ評価される語)ではない——**「f単体」と「h1(0)全体」は別の対象**であり、比較不能側に倒れる。「A=YES∧B=NO=fake候補の二つの半身」という読みを成立させるには、比較対象を「f単体」ではなく「h1(m)全体」に置き換える必要がある(h1(0)は本セッションG1で e4.identity と確認済み、下記)。

---

**注記**: 本仕様書はT-56原文・2008.00066本文を直接持たない状態でのdocsからの再構成であり、①②の逐語は工房の抽出ノート経由(一次原文への遡及照合は未実施)。Sol/数学者による一次照合を推奨する。
