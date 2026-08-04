# 速達: K_π 向き較正走 — 実行不可判定(既存有限商上に ρ の自然な持ち上げなし)

- 起票: 実装担当(implementer)・2026-08-04
- 委嘱: Sol 便101 W101-1.5 認可の K_π 向き較正走(PENT-NORM vs 既存 Chk6 c3-pentagon)
- 緊急度: 急ぎではない(較正 tier・走行の妨げにはならない)。設計判断の要否のみ確認したい。

## 結論(先に一行)

**不可。** PENT-NORM(HS 条件 (III) の有限版・`docs/notes/hs_prop7_translation_v1.md` §1.2)を評価するには ρ(K(0,5) の位数 5 自己同型)の作用が要るが、**K_π の既存有限商(QP・|QP|=7500・D5=Eg⁵ packing)上に ρ の自然な持ち上げは存在しない**ことを機械で確認した。委嘱の指示どおり「無ければ正直に停止」した。20 行の突合表・cert JSON は出していない(出せる状態にない)。

## やったこと

1. `search/probe/wac_v1/gtpi_closure_20260801.g` の BLOCK I(window/cof/D5/Psi/QP 構成・byte-identical import)を再利用し、D5=DirectProduct(Eg,Eg,Eg,Eg,Eg) の **5 直積因子の巡回シフト** σ を、ρ の唯一の「選択の余地がない」候補として構成した(cof[i] が PsiAt の 5 スロットに対応する唯一の自然な index であるため)。
2. σ が QP(= Chk6/Pent が実際に使う窓)を安定化するか(σ(QP)⊆QP)を GAP で直接検査。
3. 結果(`scratchpad/kpi_orient_feasibility.g` 実行原文):
   ```
   == SETUP ==  |D5|=6046617600000  |QP|=7500  |Ader|=60  |PN|=60
      SigmaMap(gens of D5) land in D5 : true
      Sigma(Psi(x)) in QP : false
      Sigma(Psi(y)) in QP : false
      Sigma(Psi(c)) in QP : false
      sigma(QP) subseteq QP (necessary for natural lift) : false
      sigma(Ader) subseteq Ader : false
      sigma^5 = identity on gensQP : true
      sigma = identity on gensQP (degenerate case) : false

   == VERDICT ==
      NOT FEASIBLE via this candidate lift -- no natural rho-action on the
      existing K_pi finite quotient without constructing K(0,5) itself.
   ```
   σ は位数 5(σ⁵=id を確認・非自明)で、まさに ρ の候補として妥当な形をしているにもかかわらず、**Psi(x),Psi(y),Psi(c) の像が QP の外に出る**(QP・Ader いずれも安定化しない)。

## 判断の根拠(なぜこの σ を「唯一の自然な候補」とみなしたか)

- `cof`(BLOCK I の cocycle 表)は 5 行を持ち、`PsiAt(w,i)` がその i 番目を評価する — これが Pent(w) の 5 スロット構造であり、Pack(D5) の 5 直積因子と 1:1 対応する。**この対応以外に、ρ の位数 5 巡回性を体現できる「作らずに済む」候補はない**(ad hoc に別の作用を発明することは「自然な持ち上げ」の趣旨に反し、CLAUDE.md が警告する向き規約の罠(f/f⁻¹ 族)を誘発しうるため見送った)。
- この結果は既存の独立な負の結果と整合する: `docs/notes/gtpi_v1.md` §6.2(GAP-GTPI-2)は「現行構成に $PB_4$ 水準の窓が存在しない」(⟨X_ij⟩ が粗窓 $P_N=A_5$ に完全に潰れる)と既に確定していた。今回の σ 不安定化は、**同じ不在を D5-packing の対称性という別角度から独立に裏付ける**。
- `docs/notes/hs_prop7_translation_v1.md` §3.1 自身も K_π を「不適」(篩 F-1/F-2/F-3 すべて落ちる)と判定済みで、この較正走の期待値は「20/20 一致だが新情報ゼロ」だった。今回の結果は「その一致自体を測る手段がこの窓には存在しない」という、さらに手前の停止である。

## 逸脱・懸念

- 委嘱は「(可なら)20 行の二経路突合表」を求めていたが、上記の理由で**実行不可のため未作成**。cert JSON(`search/certs/kpi_orientation_cal_20260804.json`)も**未作成**(実行していない結果を cert 化しないため)。
- σ 以外の「自然な」候補が存在する可能性は排除していない(束縛探索ではなく、cof 構造から論理的に一意と判断した1候補のみを試した)。司令塔/数学者が別の自然な候補を指定するなら再走可能。
- 委嘱本文が既に示唆していた通り、**この較正は K(0,5) 商構築(HS 条件2係が構築中)の後**に回すのが筋、という判定で一致した。

## 次にできること(要指示)

- (a) このまま **停止・保留**(K(0,5) 商構築完了後に再委嘱)。
- (b) 委嘱を **類 4 冪零窓 $N^{(4,p)}$($p\ge7$)**(hs_prop7_translation_v1.md §3.2 の代替第一標的)に差し替えて実装へ回す。
- 指示があれば速やかに動く。現状はここで止めている。
