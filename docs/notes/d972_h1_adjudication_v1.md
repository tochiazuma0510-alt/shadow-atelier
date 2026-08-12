# 【D972-GAP-1】(H1) $M$ の isolated 性 — 正典 Prop 3.15 による帰着と規模の激減(裁定 1130)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1130(Phase 0 差し戻し)
入力 = `div_law_v1.md` §1 (INT)・`ihnec_v1.md` §B.2/§8/§571・`ent_arith_type_gate_v1/v2`・`p8_corr_v1.md` §55・census83 control
生成 script(裁定 1103 規約)= 本文中の python 1 行(規模計算)
⚠ $u$/$c$ 非接触。**格: candidate**(Sol 未監査)。

---

## §0 三行

1. ★★ **(H1) は測るべき対象を間違えていました。** 正典 **2401 Prop 3.15**(isolated $\cap$ isolated $=$ isolated)により
$$\boxed{\ K^{(9)}\ \text{isolated(Thm 4.3・正典)}\ \wedge\ N_{S4}\ \text{isolated}\ \Longrightarrow\ M=K^{(9)}\cap N_{S4}\ \text{isolated}\ }$$
⟹ **(H1) は「$N_{S4}$ の isolated 性」1 本に帰着します**。
2. ★★★ **これで計器の壁を越えます**: $\lvert PB_3/M\rvert=1{,}469{,}664=2916\times\mathbf{504}$(厳密)⟹ **測定対象は $\lvert PB_3/N_{S4}\rvert=504$**(**2916 倍の削減**・$\lvert B_3/N_{S4}\rvert=3024$)。既に計器が通っている規模帯です。
3. ⚠ **ただし Prop 3.15 には債務が 2 つ**(原論文に証明なし・**原文画像未照合**)⟹ §2 に**私の独立証明(5 行・$\Xi$ 非依存)**を置き、`ihnec` §B.2 の裏取りとします。

$$\boxed{\ \textbf{差し替え: 測るのは }M\ \textbf{ではなく }N_{S4}\ }$$

---

## §1 ★ novelty-grep の記帳(m1128-1 恒久対策の初適用)

裁定 1128 で自ら課した規律の初回適用です。**「isolated の交わりは isolated」は私の新発見ではありませんでした。**

| # | grep コマンド | ヒット | 判定 |
|---|---|---:|---|
| 1 | `grep -rn "ISO-CAP" docs/ sol/` | **0** | 名前は未使用 |
| 2 | `grep -rniE "isolated.{0,25}(交わり\|共通部分\|intersection\|cap)" docs/ sol/` | **24** | ★ **既出** |
| 3 | `grep -rniE "(isolated).{0,20}(合成\|閉じ\|閉包\|安定)" docs/ sol/` | **19** | 既出 |
| 4 | `grep -rniE "S4.{0,30}isolated\|isolated.{0,30}S4"` | 複数 | ★ **$N_{S4}$ の isolated は UNKNOWN と既記** |

**決定的なヒット(逐語)**:
- `div_law_v1.md` §61: 「**(INT)** isolated $\cap$ isolated $=$ isolated(有向性)| **2401 Prop 3.15**(**証明は原論文に無い** — ihnec 追補 B.2 の自前証明を使う)」
- `ihnec_v1.md` §571: 「2401 Prop 3.15 … ② **命題 ROOF(3)($M=K^{(9)}\cap N_{\rm S4}$ の isolated 性)**」 ⟹ ★ **ihnec は既にこの帰着を書いていました**
- `b4_original_gtshadows_extraction_v1.md` §129: B₄ 側 2008 論文の **Prop 3.6「isolated 2 元の交わりも isolated」**(同型の命題が両線にある)
- `ent_arith_type_gate_v1.md` §113: 「G1 | isolated / genuine($N_{S4}$・$M$)| ✘ **UNKNOWN**」
- `p8_corr_v1.md` §55: 「⚠ **$N_{S4}$ の isolated が閉じるまで $\rho_{S4}$ 自体が未定義**(B118-1)」

$$\boxed{\ \textbf{⟹ 私が「紙路」として出そうとした定理は正典 Prop 3.15 そのもの。grep が救いました}\ }$$
★ **規律の効果**: 前回(m1128-1)は事後に研究者が捕捉しましたが、**今回は着手前に自分で捕捉できました**。恒久対策は機能しています。

---

## §2 ★ 私の独立証明(`ihnec` §B.2 の裏取り・$\Xi$ 非依存)

Prop 3.15 は**原論文に証明がなく**(「読者演習」)、しかも `ihnec` §8 申し送り 1 で **原文画像照合が未了**と記録されています。⟹ **依存が重い割に足場が薄い**ので、独立の証明を置きます。

> **【命題 INT(= 2401 Prop 3.15 の再証明)】** $N_1,\dots,N_k\in\mathrm{NFI}_{PB_3}(B_3)$ がすべて isolated なら $M:=\bigcap_i N_i$ も isolated。

**証明**。$M\in\mathrm{NFI}_{PB_3}(B_3)$(有限指数正規部分群の有限交叉・$\subseteq PB_3$)✔ $t=[m,f]\in GT(M)$ を任意の shadow とし $T:=T_{m,f}:B_3\twoheadrightarrow B_3/M$ とする。

1. $M\le N_i$ ゆえ reduction $R_{M,N_i}$ が定義され、**正典 (3.60) は shadow を shadow に送る** ⟹ $R_{M,N_i}(t)\in GT(N_i)$。
2. **(R1)**: $T_{R_{M,N_i}(t)}=\pi_{M,N_i}\circ T$(生成元で確認済 — `r2_r3_unram_execution_spec_v1` §11.0)⟹ **(R2)**: $\ker T_{R_{M,N_i}(t)}=T^{-1}(N_i/M)$。
3. $N_i$ は isolated ⟹ **全 shadow が settled** ⟹ $\ker T_{R_{M,N_i}(t)}=N_i$ ⟹ $\boxed{T^{-1}(N_i/M)=N_i}$。
4. 対応定理は交わりを保つ: $\bigcap_i(N_i/M)=\bigl(\bigcap_iN_i\bigr)/M=M/M=\{1\}$。逆像も交わりを保つ ⟹
$$\ker T=T^{-1}(\{1\})=T^{-1}\Bigl(\bigcap_i(N_i/M)\Bigr)=\bigcap_iT^{-1}(N_i/M)=\bigcap_iN_i=M$$
5. ⟹ $t$ は settled。$t$ は任意 ⟹ **$M$ は isolated** ∎

★ **U6-3 の教訓への適合**: この証明は **$\Xi$(= $\Psi$)を一切使いません**。核と逆像だけの $B_3$ 水準の論証なので、「$\Xi$ で見える範囲からの論証」という循環に**構造的に陥りません** ✔ 司令塔の要求どおりです。

**依存**(すべて薄い):
| # | 使ったもの | 状態 |
|---|---|---|
| (a) | (3.60) が shadow を shadow に送る | 正典の reduction の定義 ⟹ **1 行 pin**(既出【SS-GAP-6】(a)) |
| (b) | (R1) $T_{R(t)}=\pi\circ T$ | ★ 私が生成元で確認済 |
| (c) | isolated の定義(Def 3.13: 全 shadow が settled) | 正典・`ihnec` §601 に逐語 |
| (d) | 対応定理・逆像が交わりを保つ | 初等 |

⟹ ★ **Prop 3.15 の原文画像照合が仮に取れなくても、本証明で代替できます**(`ihnec` §8 申し送り 1 の負担軽減)。

---

## §3 (H1) の帰着

$K^{(9)}$ は **正典 Thm 4.3 で isolated**(定義ノート §3・`div_law` (E1-1))。よって命題 INT より

$$\boxed{\ \textbf{(H1)}\ M=K^{(9)}\cap N_{S4}\ \text{isolated}\quad\Longleftarrow\quad N_{S4}\ \text{isolated}\ }$$

⚠ **一方向のみ**であることに注意: Prop 3.15 は**十分条件**です。$N_{S4}$ が非 isolated でも $M$ が isolated である可能性は残ります ⟹ **$N_{S4}$ の陰性は (H1) の反証ではありません**(§6)。

★ **副産物**: Phase 1 の前件 [1-2](細分 $K:=K^{(27)}\cap N_{S4}$ が isolated)も、$K^{(27)}$ が isolated(Thm 4.3)ゆえ**同じ 1 本に帰着**します。
$$\boxed{\ \textbf{1 つの測定($N_{S4}$ の isolated 性)が (H1) と Phase 1 [1-2] の}\textbf{両方}\ \textbf{を閉じます}\ }$$

---

## §4 ★★ 規模の激減(機械)

```
|PB_3/K^(9)| = |G_9| = 4*9^3 = 2916            [定義ノート §3 の数値事実]
|PB_3/M|     = 1,469,664                        [Phase 0 実測]
1,469,664 / 2916 = 504  (割り切れる: True)
  ==> |PB_3/N_S4| = 504 ,  |B_3/N_S4| = 3,024
  ==> 計器負荷は 2916 倍の削減
```

| 対象 | $\lvert PB_3/\cdot\rvert$ | 計器 |
|---|---:|---|
| $M$(現行の測定対象) | **1,469,664** | ✘ **規模外**(Aut 計算・裁定 1130) |
| ★ **$N_{S4}$**(差し替え後) | **504** | ★ **既に通っている規模帯**(census83 の窓は $\lvert PN\rvert\sim168$〜、K^(9) 系は 2916) |

⚠ **$504=1{,}469{,}664/2916$ が厳密に割り切れる**のは「両成分の像が相補的」であることの傍証ですが、**$\lvert PB_3/N_{S4}\rvert=504$ 自体は実測で確認してください**(私の推論は割り算 1 本です)。

---

## §5 測定 spec — $N_{S4}$ の isolated 性

```
=== [H1-A] N_S4 の isolated 判定(差し替え後の Phase 0)===
根拠: docs/notes/d972_h1_adjudication_v1.md §3(命題 INT による帰着)
⚠ u/c 非接触・prereg 非抵触

[A-0] |PB_3/N_S4| , |B_3/N_S4| を実測(★ 予言: 504 / 3024)
      ⟹ 504 と大きく違えば §4 の割り算の前提が壊れている ⟹ 報告
[A-1] N_S4 の全 shadow を列挙(charming + hexagon + 全射性)
      ★ 規模 504 は census83 の実績帯(168〜2916)の内側
[A-2] 各 shadow で ker T_{m,f} = N_S4 か(marked factor map)
      = census83 の well_defined ∧ kernel_trivial と同じ述語(意味論は census83_readout §1 で確定済)
[A-3] 判定: 全 shadow が settled ⟹ N_S4 は isolated ⟹ ★ (H1) 成立(命題 INT)
              1 つでも非 settled ⟹ N_S4 は非 isolated ⟹ ⚠ (H1) は *未決のまま*(§6)
[A-4] 併せて #C(N_S4) と |GT^settled(N_S4)| を記録(定理 TORSOR の回帰: |GT| = |settled|·#C)
[A-5] 見張り: c ∈ N_S4 か(census83 の control「S4(c∈N)」との同一性確認)
      ⚠ census83 の control S4(54 shadow・isolated 既知)が *この* N_S4 と同一物かは未確認
      ⟹ 同一なら [A-1]〜[A-3] は既済の再確認になる ⟹ ★ 先にこれを見ること
出力: cert (schema h1_ns4_isolated/v1)。整数のみ。u_touched=false
★ 規模: 秒〜分級。
```

★ **[A-5] を最優先に**: census83 の control 行「S4($c\in N$)| 54 | 54 | 率 1 | `all_kernel_trivial=True` | ★ isolated ✔(既知)」が**この $N_{S4}$ と同一窓なら、測定は既に済んでいます**。⚠ ただし `ent_arith_type_gate` が「$N_{S4}$ の isolated は UNKNOWN」と書いているので、**同一物ではない公算が高い**(census83 の S4 は control 用の別窓の疑い)⟹ **同定を先に**。

---

## §6 ⚠ (H1) が閉じない場合 — 作戦書 v1.2 の骨(一言)

**場合分け**:
| $N_{S4}$ の判定 | (H1) | DICHOTOMY-972 |
|---|---|---|
| **isolated** | ★ **成立**(命題 INT) | ★ **生存** ⟹ v1.1 のまま Phase 1 へ |
| **非 isolated** | ⚠ **未決**(Prop 3.15 は十分条件のみ) | ⚠ **保留** — $M$ の直接判定が要るが計器の壁に戻る |
| ($M$ が非 isolated と判明した場合) | ✘ **反証** | ✘ **落ちる** ⟹ 下記 v1.2 |

**v1.2 の骨(DICHOTOMY が落ちた場合)**:
1. $GT(M)$ は群でない ⟹ $\mathcal{PR}_M(\widehat{GT}_{\rm gen})$ の部分群性が消える ⟹ **指数 3 の素数性による二分法は使えません**。
2. ★ **しかし定理 TORSOR と SUBTOR は生きます**(どちらも isolated を $M$ に要求しません — SUBTOR が要求するのは**細分 $K$ の isolated 性**であり、それは Thm 4.3 + 命題 INT で別途出ます)。
 - $\lvert GT(M)\rvert=\lvert GT^{\rm settled}(M)\rvert\cdot\#\mathcal C(M)$(TORSOR)
 - $\mathrm{Im}\,R_{K,M}$ は各核類で $S_X$-トーサーか空(SUBTOR)⟹ $\lvert\mathrm{Im}\rvert=\lvert S_X\rvert\cdot\#\mathcal C_X$
3. ⟹ **Phase 1 の「1 ビット」は「$\lvert S_X\rvert$ の倍数のどれか」という粗い量子化に格下げ**されますが、**fail-closed は残ります**($\lvert S_X\rvert$ の倍数でない値が出たら停止)。
4. ⟹ **A 型の一括証明書は生きます**(Cor 5.4 の易しい向きは isolated を要さない)。失うのは「残り全部が同時に決まる」という二分法の恩恵だけです。
$$\boxed{\ \textbf{v1.2 = 「1 ビット」→「トーサー量子化」への置き換え。A 型検出そのものは生き残る}\ }$$

---

## §7 σ₁,σ₂ の $B_3$ 実現(副次・債務返済)

★ **critical path から外れました**(§3 の帰着で不要)。ただし **W4 対照と $d_9$ 線の恒久資産**なので、実装係の負の知見を踏まえた設計だけ置きます。

**実装係の負の知見**: block-swap ansatz は **$D_9$ に位数 4 の元が無いため原理的に 0 件**(`scratchpad/try_sigma_k9.g`)。
★ **診断**: これは**探索場所の誤り**です。$\sigma_1$ は $PB_3/K^{(9)}=G_9$ の**中には居ません**($\sigma_1\notin PB_3$)。居るのは $B_3/K^{(9)}$(位数 $6\cdot2916=17{,}496$)の中で、$G_9$ の**外側のコセット**です。

**設計(ansatz を使わない)**: 正典 (1.11)(1.12) は $\sigma_i$ の $F_2$ への共役作用を**明示**しており、$c\in K^{(9)}$ ゆえ **$c$ 因子が消えます**:
$$\bar\sigma_1:\ x\mapsto x,\quad y\mapsto y^{-1}x^{-1};\qquad \bar\sigma_2:\ x\mapsto x^{-1}y^{-1},\quad y\mapsto y$$
$$\boxed{\ \Longrightarrow\ \alpha_1,\alpha_2\in\mathrm{Aut}(G_9)\ \textbf{が}\textbf{式で与えられる}\ }$$

```
=== [SIG-1] sigma_1, sigma_2 の実現(ansatz 不要)===
[S-1] G_9 = <(r,s,s),(rs,r,rs)> <= D_9^3 を構成(既存資産・位数 2916 を確認)
[S-2] alpha_1 := GroupHomomorphismByImages(G_9,G_9,[x,y],[x, y^-1*x^-1])
      alpha_2 := GroupHomomorphismByImages(G_9,G_9,[x,y],[x^-1*y^-1, y])
      ★ 自己同型であること・braid 関係 alpha_1 alpha_2 alpha_1 = alpha_2 alpha_1 alpha_2 を検算
[S-3] H := <alpha_1, alpha_2> <= Aut(G_9) を作り |H| を測る
      ★ Z(G_9) = 1 なら B_3/K^(9) -> Aut(G_9) は単射の見込み ⟹ |H| = 17,496 を予言
      ⚠ |H| < 17,496 なら中心化群が非自明 ⟹ その分だけ持ち上げが要る(報告)
[S-4] alpha_i^2 が Ad(x), Ad(y) と一致するか検算(sigma_1^2 = x の整合)
出力: cert (schema sigma_realization/v1)
```
★ **要点**: $\sigma_i$ を**群の元として探す**のではなく、**自己同型として構成する**。正典の (1.11)(1.12) が式を与えているので ansatz は不要です。

---

## §8 記帳

- ★ **本書の新規部分**: ① **novelty-grep の記帳**(m1128-1 恒久対策の初適用・4 本のコマンドとヒット数)⟹ **ISO-CAP は正典 Prop 3.15 として既出**と判明 ② **命題 INT の独立証明**($\Xi$ 非依存・5 行・`ihnec` §B.2 の裏取り・原文画像未照合の負担を軽減)③ ★★ **(H1) の $N_{S4}$ への帰着**と **Phase 1 [1-2] も同じ 1 本に落ちる**こと ④ ★★ **規模の激減**($1{,}469{,}664=2916\times504$・**2916 倍**)⟹ 計器の壁を越える ⑤ [A-5] の**同定を最優先にする設計**(census83 の control S4 との同一性)⑥ **$N_{S4}$ 陰性は (H1) の反証ではない**という論理の明示 ⑦ v1.2 の骨(二分法 → トーサー量子化・A 型検出は生存)⑧ **σ₁ は群の元でなく自己同型として構成する**という診断と ansatz 不要の spec。
- ⚠ **私の誤り(裁定 1130 で顕在化)**: 「Phase 0 で測れます」と書いたとき、**測定対象を $M$ に固定してしまい、正典 Prop 3.15 による帰着を見落としていました**。⟹ 教訓: **測定を設計する前に、対象を分解できないかを正典で確認する**。
- **【H1-GAP-1】(小・新)** census83 の control「S4」窓と TRIAD の $N_{S4}$ の同一性(⟹ [A-5])。
- **【H1-GAP-2】(小)** 2401 Prop 3.15 の**原文画像照合**は依然未了(`ihnec` §8 申し送り 1)。★ ただし §2 の独立証明があるので**本線の依存は解消**。
- **申告**: 紙 + 割り算 1 本(機械)。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
