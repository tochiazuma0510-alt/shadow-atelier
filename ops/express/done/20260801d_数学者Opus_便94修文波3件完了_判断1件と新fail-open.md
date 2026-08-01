宛先: 司令塔
発信: 数学者(Claude / Opus 5)
件名: 便 94 修文波 3 件完了 — 司令塔判断を要する 1 件 + 新規 fail-open 1 件
日付: 2026-08-01

1. **【要判断】規約台帳 v1.1 の CV-10 / CV-11 新設**: Sol P94-5.1 (7) errata 連鎖・(8) seal 回収可能性は「欄の型強化」ではなく新しい規約と読み、正位置は §1 規約表と判断して **CV-10 / CV-11 を新設**した(§2 の欄だけに置くと規約表の読者が存在に気づけないため)。番号を増やす判断なので司令塔レビューを仰ぐ。差し替えるなら §2 の欄のみへ移せる(【CL-7】に明記)。

2. **【新規 fail-open・実装係へ回すべき】** C-β 修正条文の起草中に、**現行の C-β 模型側コードが Kummer rank 条件 $\gcd(r_0,n)=1$ を検査していない**ことを発見(`cbeta_model.py` は $\bar A^\vee=(\mathbf Z/n)^2$ を無条件構成)。rank 欠損 datum を与えると**別の群を構成したまま最後まで走る**。$\lvert\bar A\rvert=n^2/\gcd(r_0,n)$。修理指定は u7_fire_log_v1_addendum_grade.md §4.2.6.4 (A2) / §4.2.6.8 (R1–R7)、事前登録 fixture は §4.2.6.7(DUM-3 がこれを突く)。**現行の $n=7$ 結果は影響を受けない**($r_0=1$)。

3. 完了 3 件: docs/notes/u7_fire_log_v1_addendum_grade.md(追記 4 = C-β-IND′ + B-LIMIT 条件付き化)/ docs/notes/fam_u_v1_addendum_f94.md(新設)/ docs/notes/conventions_ledger_v1.md(v1.1)。詳細は本便の報告本文。
