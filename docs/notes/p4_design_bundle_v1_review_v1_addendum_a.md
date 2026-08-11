# P4 設計束 検分 追補 A — P4-1 の標的差替(裁定 840)

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査)
**入力**: 裁定 840(registry 回答: ①$\mathrm{im}(\mathrm{Ih}_M)$ の計算記録なし ②命題 ROOF: $PB_3/M\cong G_9\times PSL(2,8)$ = **分裂屋根** ③定理 SPLIT-NULL(裁定 379 期))
**先行**: `p4_design_bundle_v1_review_v1.md` §1(9a23f28)

---

## §0 裁定案の受諾

> **972 屋根 = 較正・カナリアへ降格 / 本命 = entangled 屋根($K^{(9)}\times K^{(12)}$ 系を昇格)** — **受諾**。
> ★ 加えて、SPLIT-NULL の内容を**本検分の言葉で独立に再導出**できた(§1)ので、降格は「他戦役の定理に従う」ではなく **本設計の内部でも強制**される。

---

## §1 ★★ 独立再導出 — 命題候補 **ENT-VAC**

> ### 命題候補 ENT-VAC(candidate・本追補・repo 初出)
> $N=N_1\cap N_2$、$Q_A:=\mathrm{Gal}(L_1\cap L_2/\mathbf Q)$(= $A_1,A_2$ を貼り合わせる共通商)とする。**$Q_A$ が自明**なら Goursat より $A=A_1\times A_2$ で、
> $$x=(x_1,x_2)\in X\setminus A\ \Longrightarrow\ \exists i:\ x_i\in GT(N_i)\setminus A_i$$
> $$\boxed{\ \Longrightarrow\ \textbf{共通商が自明なら、}X\setminus A\ \textbf{の元は必ず}\textbf{単独窓の非全射}\textbf{に由来する — entanglement 固有の寄与はゼロ}\ }$$
> **証明**: $A=A_1\times A_2$ ゆえ $x\notin A$ は $x_1\notin A_1$ または $x_2\notin A_2$ と同値。$X$ は $GT(N_1)\times GT(N_2)$ に入るので $x_i\in GT(N_i)$。∎

⟹ **972 屋根**: $PB_3/M\cong G_9\times PSL(2,8)$(直積)。$PSL(2,8)$ は単純、$G_9$ は可解型 ⟹ **両者の最大共通商は自明** ⟹ ENT-VAC が適用 ⟹ **entanglement の置き場が無い**。
$$\boxed{\ \textbf{⟹ 札の S2(非自明共通商)は「絞り」ではなく}\textbf{実験が空でないための必要条件}\textbf{である}\ }$$
⟹ 札 §1.2 の S2 の格を「選定基準」から「**必要条件**」へ格上げすべき(EXHAUST の観点でも、S2 を満たさない対を「候補」に並べてはならない)。
★ **SPLIT-NULL(裁定 379 期)と独立に一致** — 二つの経路が同じ結論に着いた(紙の二系統・**cross-checked とは書かない**: 一方は他戦役の定理の要約経由)。

---

## §2 ★★★ 非空になる条件の**正確な形** — 命題候補 **ENT-MECH**

各窓が個別に飽和($A_i=GT(N_i)$)しているとき、$A\subseteq X$ ゆえ
$$X\setminus A\ne\varnothing\iff\lvert X\rvert>\lvert A\rvert,\qquad \lvert X\rvert=\lvert GT(N)\rvert\ (\textbf{CRT-INJ}),\qquad \lvert A\rvert=\frac{\lvert GT(N_1)\rvert\,\lvert GT(N_2)\rvert}{\lvert Q_A\rvert}$$

> ### 命題候補 ENT-MECH(candidate・本追補)
> $$\boxed{\ X\setminus A\ne\varnothing\iff \lvert GT(N)\rvert\cdot\lvert Q_A\rvert\ >\ \lvert GT(N_1)\rvert\cdot\lvert GT(N_2)\rvert\ }$$
> ⟹ **観測量は不等式 1 本**(§1.1 の「等式 1 個」の一般形)。

**機構の同定**: 関手性より $X\subseteq GT(N_1)\times_{GT(N_0)}GT(N_2)$($N_0=N_1N_2$ = 共通商の窓)。一方 $Q_A$ は **$A_1,A_2$ の最大共通商**であって $GT(N_0)$ を経由するとは限らない。

> $$\boxed{\ \textbf{entanglement の正体} = \textbf{二つの算術体が「窓の共通商 }GT(N_0)\ \textbf{が見せる以上に」共有していること}\ (\lvert Q_A\rvert>\lvert A_0\rvert)}$$
> ⟹ **狩る対象が具体化した**: 「$L_1\cap L_2$ が $N_0$ の予想より大きい対」。

---

## §3 標的差替 — $K^{(9)}\times K^{(12)}$ 系

### 3.1 最初の作業(裁定 840 の指定を受諾)

$$\textbf{共通商}\ B_3/(K^{(9)}K^{(12)})\ \textbf{の同定}$$

> ### ★ 予言候補 **P-ENT-0**(本追補で凍結・**機械確認前**)
> $K^{(n)}=\ker\psi_n$ の族が **$n\mid m\Rightarrow K^{(m)}\subseteq K^{(n)}$** を満たすなら($\psi_n$ が $\psi_m$ を経由するため)、
> $$K^{(9)}K^{(12)}\subseteq K^{(3)}\quad\Longrightarrow\quad B_3/(K^{(9)}K^{(12)})\ \twoheadrightarrow\ B_3/K^{(3)}$$
> $$\boxed{\ \textbf{予言}:\ \textbf{共通商は }B_3/K^{(3)}\ \textbf{に全射する(非自明)。等号 }K^{(9)}K^{(12)}=K^{(3)}\ \textbf{かは}\textbf{要機械確認}\ }$$
> **陽性(非自明)** ⟹ S2 クリア ⟹ ENT-MECH の不等式検査へ。
> **陰性(自明)** ⟹ ENT-VAC で再び空 ⟹ **dihedral 塔内では entanglement が原理的に起きない**ことになり、それ自体が一級(塔の「独立性」の定理候補)。
> ⚠ **前件の確認が先**: $K^{(n)}$ 族の整除性($n\mid m\Rightarrow K^{(m)}\subseteq K^{(n)}$)は 2405 の定義から従うはずだが、**正典で確認すること**(私は記憶で書いており未照合)。

### 3.2 差替後の手順(4 段 → 3 段)

1. **共通商の同定**: $B_3/(K^{(9)}K^{(12)})$ の位数と同型型($Q_{\rm win}$)。**自明なら即停止**(S2 違反)。
2. **$Q_A$ の決定**: $L_1\cap L_2$ の同定 — dihedral 塔なので**両体は円分/類体論的に記述済**の見込み(FAM-U/MIX 系)⟹ $\lvert Q_A\rvert$ を算術側から決める。★ **$\lvert Q_A\rvert>\lvert Q_{\rm win}\rvert$ かが entanglement の有無そのもの**(§2)。
3. **ENT-MECH の不等式**: $\lvert GT(N)\rvert\cdot\lvert Q_A\rvert$ vs $\lvert GT(K^{(9)})\rvert\cdot\lvert GT(K^{(12)})\rvert$。$GT(K^{(n)})$ は **2405 Thm 4.3 の明示式**で紙から出る ⟹ **左辺の $\lvert GT(N)\rvert$ だけが機械項**。

### 3.3 972 屋根の新しい役回り(降格後)

> **較正・カナリア**: ENT-VAC より **$X=A$ が期待値**(各窓が飽和なら定理)。⟹ **ENT-MECH の等式検査パイプラインの fail-closed 較正場**として使う。
> $$\boxed{\ \textbf{カナリア }\textbf{P-ENT-C}:\ 972\ \textbf{屋根で }\lvert X\rvert=\lvert A\rvert\ \textbf{(= 等号)。破れたら実装/意味論エラーで STOP}\ }$$
> ⚠ ただし裁定 840 ① より **$\mathrm{im}(\mathrm{Ih}_M)$ の計算記録は無い** ⟹ カナリアを走らせるには**まず両因子窓の較正($A_i=GT(N_i)$)を確認**する必要がある。**それ自体が S1 の実地検査**になる。
> ⟹ **降格しても仕事が残る**(捨てない)。

---

## §4 札への差戻し(§1 の指摘の更新)

| 項 | 検分 v1 の指摘 | 本追補での確定 |
|---|---|---|
| (a) 972 屋根 = 本命 | 「空振り化リスク・registry 確認を」 | ★ **確定的に空**(ENT-VAC + ROOF)⟹ **較正・カナリアへ降格** |
| S2 の格 | 「選定基準」 | ★ **必要条件へ格上げ**(ENT-VAC) |
| 観測量 | 「等式 1 個」($Q_A$ 自明の場合) | ★ **不等式 1 本**(ENT-MECH・一般形) |
| entanglement の定義 | 「同時実現可能性の欠如」(Sol 逐語) | ★ **機構の同定**: $\lvert Q_A\rvert>\lvert A_0\rvert$(算術体が窓の共通商より多く共有) |
| 本命 | (a) | **(b) $K^{(9)}\times K^{(12)}$**(P-ENT-0 の確認が入口) |

**ENT-EQUIV(検分 v1 §1.3)は不変**: entanglement 実験は依然として窓 $N$ の通常の全射性問題と同値。**変わったのは「どの $N$ を選べば非空になりうるか」の判定条件**(= ENT-MECH)であり、それが本追補の実質。

---

## §5 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| **【ENT-GAP-1】** ★新 | $K^{(n)}$ 族の整除性($n\mid m\Rightarrow K^{(m)}\subseteq K^{(n)}$)は**正典未照合**(記憶による)⟹ P-ENT-0 の前件 | ★ 中(**即確認可**) |
| **【ENT-GAP-2】** ★新 | $Q_A$($=\mathrm{Gal}(L_1\cap L_2/\mathbf Q)$)を算術側から決める手順は未設計(§3.2 段 2) | ★ 中 |
| **【ENT-GAP-3】** ★新 | ENT-MECH は「各窓が個別に飽和」を前件とする。非飽和なら単独窓の問題に帰着(ENT-VAC の議論と同型) | 小 |
| **【REV-GAP-1】** | ENT-VAC/ENT-MECH はともに **CRT-INJ**(candidate)に依存 | 中 |

**帰属**: registry 回答・命題 ROOF・定理 SPLIT-NULL・標的差替の裁定案 = **司令塔**(裁定 840)。ihnec 戦役の設計資産(ScanRoofHexagon 等)= 当時の実装係。
**本追補の新規部分** = **命題候補 ENT-VAC(SPLIT-NULL の独立再導出・S2 を必要条件へ格上げ)** / **命題候補 ENT-MECH(非空条件の不等式 1 本)** / ★ **entanglement の機構同定($\lvert Q_A\rvert>\lvert A_0\rvert$ = 算術体が窓の共通商より多く共有)** / **予言候補 P-ENT-0(共通商 $\twoheadrightarrow B_3/K^{(3)}$)** / **カナリア P-ENT-C と 972 屋根の降格後の役回り** / **3 段手順(機械項は $\lvert GT(N)\rvert$ 1 個)**。

**novelty grep**(`docs/`): `ENT-VAC` `ENT-MECH` `P-ENT-0` `P-ENT-C` = **0 hit(本追補初出)**。`SPLIT-NULL` `ROOF` は既在(裁定 379 期・引用)。
