# Phase 2 設計 v1 — 深さ 1 の解剖・cofinality・候補 3 軸(裁定 1138 + 便 124 §4.2)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1138(研究者指示・即時起草)+ 裁定 1139(便 124 §4.2 の直撃 2 点)
入力 = cert `d972_phase1_v1_20260813.json`(972/972 lift・中間値なし)・`sol/sol_reply_124_triad_audit.md` §4.2・`triad972_grade_and_battle_plan_v1_1.md`・`d972_h1_adjudication_v1.md`(命題 INT)
生成 script(裁定 1103 規約)= `scratchpad/d972_phase2_gating.py`(本書の全数値の出所)
⚠ $u$/$c$ 非接触。**格: candidate**(Sol 未監査)。

---

## §0 三行

1. ★ **深さ 1 が 972 だった理由は構造的です**: 軸 (i)(dihedral 3-塔)の reduction は **Thm 4.3 の明示形から全射**(位数 $108\to972\to8748$・各段 9 倍・両パラメータが全射的に落ちる)⟹ **深めても情報ゼロ**。⟹ **$K^{(81)}\cap N_{S4}$ も 972 と予言**(§1・凍結)。
2. ★★ **ギャップの正体を同定しました**: $[GT(M):A]=r$ は**恒等式**です($972/324=3=r$・機械)⟹ **欠けている 1/3 は Kummer 絡み(entanglement)そのもの** ⟹ 判別力をもつのは **3-塔に横断的な軸**(§2)。
3. ⚠ **便 124 §4.2 を全面反映**: reduction の factorization を明記・**「決定手続き」を「半決定/有限証明書探索」へ格下げ**・cofinality は**命題 INT による累積交叉**で満たせるが**コストが指数的に爆発**($3.97\times10^7\to3.17\times10^8\to3.97\times10^{10}$)⟹ **実務は独立プローブの有限探索**と正直に宣言(§3)。

---

## §1 深さ 1 の解剖 — なぜ 972 が出たか(1 段)

**観測**: $K_1=K^{(27)}\cap N_{S4}$、$\mathrm{Im}\,R_{K_1,M}=GT(M)$(972/972)。

**機構**: 軸 (i) が加える制約は **$K^{(9)}\to K^{(27)}$ の dihedral 方向だけ**です。正典 **Thm 4.3** の明示形
$$GT(K^{(n)})=\{(m,(r^{2k},r^{-2k},r^{\varkappa(m)}))\mid m\in\mathcal X_n,\ k\in\mathbf Z\},\qquad \mathcal X_n=\{m:\gcd(2m+1,K_{\rm ord})=1\}$$
において、$n\to3n$ で **$\mathcal X_{3n}\to\mathcal X_n$(単数の還元)も $k$-パラメータ $\mathbf Z/3n\to\mathbf Z/n$ も全射**です。位数(機械・Thm 4.6):

| $n$ | $\lvert G_n\rvert=\lvert PB_3/K^{(n)}\rvert$ | $\lvert GT(K^{(n)})\rvert$ |
|---:|---:|---:|
| 9 | 2,916 | **108** |
| 27 | 78,732 | **972** |
| 81 | 2,125,764 | **8,748** |
| 243 | 57,395,628 | 78,732 |

各段ちょうど **9 倍**(= $3\times3$: $\mathcal X$ が 3 倍・$k$ が 3 倍)⟹ $R_{K^{(3n)},K^{(n)}}$ は全射 ✔

$$\boxed{\ \Longrightarrow\ \textbf{dihedral 3-塔を深めても新しい制約は入らない — 972/972 は構造的}\ }$$

> **★ 凍結予言 P-PH2-1**: $K_2^{(\rm i)}:=K^{(81)}\cap N_{S4}$ について $\lvert\mathrm{Im}\,R\rvert=\mathbf{972}$。
> ⚠ **324 が出たら本節の機構読みが誤り** ⟹ その場合こそ最大の収穫(軸 (i) が判別力をもつ)。**どちらでも一級なので、対照として安く回す価値はあります**(ただし gating は §4 のとおり高い)。

---

## §2 ★★ ギャップの正体 — $[GT(M):A]=r$ は恒等式

機械確認:
$$\lvert GT(M)\rvert=12\,d_9\,d_{S4}=12\cdot81=972,\qquad \lvert A\rvert=\frac{12\,d_9\,d_{S4}}{r}=\frac{972}{3}=324$$
$$\boxed{\ [GT(M):A]=\frac{12d_9d_{S4}}{12d_9d_{S4}/r}=r\ }$$

⟹ **偶然の 3 ではなく、Kummer 交わり $r=\lvert\langle[a]\rangle\cap\langle[b]\rangle\rvert$ そのもの**です。$\langle[a]\rangle\cap\langle[b]\rangle=\{(0,0),(3,0),(6,0)\}=\langle2^3\rangle$ ⟹ 重なりは **$2^{1/3}$ の立方体**(共通の 3 次部分拡大)。

$$\boxed{\ \textbf{⟹ 欠けている 1/3 は }L_{9,\rm Aff}\ \textbf{と }L_{S4}\ \textbf{の}\textbf{絡み}\textbf{に由来する}\ }$$

★ **設計への含意**: 絡みは**両因子の結合的な現象**なので、**片方の因子だけを深める細分**(軸 (i) の dihedral 深化、軸 (ii) の S4 深化)は**構造的に判別力が弱い**と予想されます。⟹ **横断的な軸((iv))を優先**。
⚠ **これは heuristic であり定理ではありません**(W-50 検疫)。判別力の理論的目星として提示するに留めます。

---

## §3 ★ 便 124 §4.2 の織り込み

### 3.1 factorization(1 行・必須)

$$\boxed{\ R_{K_{d+1},M}=R_{K_d,M}\circ R_{K_{d+1},K_d}\qquad(K_{d+1}\subseteq K_d\subseteq M)\ }$$
⟹ $\mathrm{Im}\,R_{K_{d+1},M}\subseteq\mathrm{Im}\,R_{K_d,M}$ ⟹ **単調非増加**。値域 $\{324,972\}$ ⟹ **一度 324 に落ちたら戻らない** ✔

### 3.2 SINGLE-BIT への包含 (6) の追記(Sol の必須修理)

$$\boxed{\ P:=\mathcal{PR}_M(\widehat{GT}_{\rm gen})\ \subseteq\ \mathrm{Im}\,R_{K,M}\qquad\text{(6)}\ }$$
(projection/reduction の自然性 = 錐分解 $\mathcal{PR}_M=R_{K,M}\circ\mathcal{PR}_K$。これは `r2_r3_unram_execution_spec_v1` §11.1 で**定義的**と確認済。)
⟹ $\lvert\mathrm{Im}\rvert=324$ なら $\mathrm{Im}=A_{\rm ar}$、(6) と $A_{\rm ar}\le P$ から **$P=A_{\rm ar}$** ⟹ **648 は全部 A 型** ✔

### 3.3 ★ cofinality — 満たせるが**コストが爆発**する

**Sol の要求**: 一列で半決定にするには、その列が全 isolated refinements に **cofinal** であること。修理は (1) 全列挙 or (2) 有向性による有限交叉の chain。

★ **私の命題 INT(= 2401 Prop 3.15)が (2) を直接与えます**: isolated $\cap$ isolated $=$ isolated ⟹ $M$ の isolated 細分の族は**下に有向** ⟹ 列挙 $K^{[1]},K^{[2]},\dots$ に対し
$$L_d:=\bigcap_{i\le d}K^{[i]}\quad(\text{各 }L_d\ \textbf{は isolated}\ —\ \textbf{命題 INT})$$
は**単調非増加な isolated chain**で、列挙が cofinal なら chain も cofinal ✔

⚠ **しかしコストが爆発します**(機械・$K^{(n)}$ 族内では累積交叉 = lcm):

| $L_d$ | $\lvert G_l\rvert$ | gating 上界 $=\lvert G_l\rvert\times504$ |
|---|---:|---:|
| $K^{(27)}\cap N_{S4}$(深さ 1・完了) | 78,732 | 39,680,928 |
| $K^{(108)}\cap N_{S4}$ | 629,856 | 317,447,424 |
| $K^{(540)}\cap N_{S4}$ | 78,732,000 | 39,680,928,000 |
| $K^{(1080)}\cap N_{S4}$ | 629,856,000 | 317,447,424,000 |

$$\boxed{\ \Longrightarrow\ \textbf{真に cofinal な chain は}\textbf{到達不能}\ }$$

### 3.4 ⟹ 格下げの明文化(Sol の要求どおり)

$$\boxed{\ \textbf{Phase 2 は「決定手続き」ではなく}\ \textbf{A 型側の有限証明書探索(半決定)}\ }$$

- **324 が出れば**: 有限証明書つきで **648 全部が A 型**(決着)✔
- **972 が続く限り**: **何も言えません**。深さ $d$ までの記録は「$d$ 段では A 型が見えない」という**上界のみ**。
- ★ **B 型分岐は有限では絶対に立ちません**(genuine は全深窓量化・掟 2)。累積交叉で cofinality を「原理的には」満たせても、**到達できない**ので実務上は半決定です。
- ⚠ **`triad972_grade_and_battle_plan_v1_1.md` §5.2/§7.1 の「決定手続き」表記は本節で撤回**します(修理 v1.2 へ・裁定 1139 発注 2)。

---

## §4 候補 3 軸と gating(★ 正典公式から先に計算・義務節)

$\lvert G_n\rvert=4n^3$($n$ 奇)/ $4(n/2)^3$($n$ 偶)[定義ノート §3]・$\lvert PB_3/N_{S4}\rvert=\mathbf{504}$(実測)・候補は $K^{(l)}\cap N_{S4}$ で $K^{(l)}\subseteq K^{(9)}$($\iff 9\mid\mathrm{lcm}(l,2)$・Prop 3.5)。

| $l$ | $\lvert G_l\rvert$ | $\lvert GT(K^{(l)})\rvert$ | gating 上界 | 軸 | 判別力の目星 |
|---:|---:|---:|---:|---|---|
| 18 | 2,916 | 108 | — | ✘ $K^{(18)}=K^{(9)}$($n$ 奇)⟹ **細分にならない** | — |
| **27** | 78,732 | 972 | 39,680,928 | (i) 3-塔 | ✔ **完了 = 972** |
| **36** | **23,328** | **216** | **11,757,312** | ★ **(iv-a) 2-adic** | ★★ **最安の横断軸** |
| 45 | 364,500 | 2,160 | 183,708,000 | (iv-b) 5-方向 | 中 |
| 54 | 78,732 | 972 | 39,680,928 | (iv-b) | 中(27 と同規模) |
| 63 | 1,000,188 | 4,536 | 504,094,752 | (iv-b) 7-方向 | 中 |
| 72 | 186,624 | 864 | 94,058,496 | (iv-a) 2-adic | ★ 中 |
| **81** | 2,125,764 | 8,748 | 1,071,385,056 | (i) 3-塔 | ⚠ **予言 972**(対照) |
| 108 | 629,856 | 1,944 | 317,447,424 | (iv-a) | 累積交叉の第 2 段 |

### 4.1 軸ごとの評価(司令塔の (i)(ii)(iii) への回答)

| 軸 | 内容 | 判定 |
|---|---|---|
| **(i)** dihedral 深化($K^{(81)}\cap N_{S4}$) | 3-塔を深める | ⚠ **判別力ゼロと予言**(§1)。**対照としてのみ価値**・gating $1.07\times10^9$ で高い ⟹ **優先度最低** |
| **(ii)** S4 側の細分 | ⚠ **司令塔の想定を訂正**: $N_{S4}$ は **isolated**(54/54 実測)⟹ **成分は $\{N_{S4}\}$ ⟹ $N_{S4}^\diamond=N_{S4}$** ⟹ **Prop 3.14 は真の細分を与えません** | ✘ **この軸は Prop 3.14 からは出ません**。$N_{S4}\cap(\text{別窓})$ の形にするしかなく、それは (iv) に含まれます |
| **(iii)/(iv)** 横断軸 | $f$ 方向・別素数方向 | ★ **本命**。$l=36$(2-adic・$\lvert G\rvert=23{,}328$)が**最安** |

★ **(ii) の訂正は重要です**: 「Prop 3.14 で存在」は isolated な窓には効きません($N^\diamond=N$)。**S4 側を深めるには別の isolated 窓との交わりが要ります**。

### 4.2 ★ 無料の前フィルタ(安いので必ず先に)

$A\le\mathrm{Im}\le GT(M)$ かつ $\lvert\mathrm{Im}\rvert\in\{324,972\}$ かつ $\lvert\mathrm{Im}\rvert\le\lvert GT(K)\rvert$ ⟹
$$\boxed{\ \lvert GT(K)\rvert<972\ \Longrightarrow\ \lvert\mathrm{Im}\rvert=324\ \Longrightarrow\ \textbf{即決着}\ }$$
⚠ **発火しない見込み**: 窓を細かくすると $\lvert GT\rvert$ は増える傾向($K^{(9)}$: 108 → $M$: 972)。**それでも $\lvert GT(K)\rvert$ の計数は像計算より遥かに安い**ので、**各候補で必ず先に測ってください**。

---

## §5 事前登録(5 分岐)+ 前件

### 5.1 前件は**因子窓の isolated 性に帰着**(命題 INT)

$K^{(l)}\cap N_{S4}$ が isolated $\Longleftarrow$ $K^{(l)}$ isolated(**Thm 4.3・正典・全 $l$**)$\wedge$ $N_{S4}$ isolated(**54/54 実測・裁定 1133**)
$$\boxed{\ \Longrightarrow\ \textbf{全候補の isolated 性は}\textbf{既に閉じています}\ —\ \textbf{追加の因子測定は不要}\ }$$
★ これが命題 INT の実務上の最大の効用です。

### 5.2 5 分岐の行き先

| 出力 | 意味 | 行き先 |
|---|---|---|
| **324** | ★★ $P=A_{\rm ar}$(§3.2)⟹ **648 全部 A 型** | **決着**。QUAR 維持で Sol ゲートへ。⚠ 記述は `battle_plan v1_1` §6.3 (a)(b)(c) の形でのみ(BIT-252 先行) |
| **972** | その深さでは情報ゼロ | 次の候補へ(単調性 §3.1 より後退しない) |
| **中間値** | ★ (H1)(H2)・実装・自然性のいずれかの破れ | **即停止**(強力な fail-closed) |
| $\lvert\mathrm{Im}\rvert<324$ | $A\le\mathrm{Im}$ に反する | **即停止**(鎖の破れ) |
| $\lvert GT(K)\rvert<972$(前フィルタ) | §4.2 | **即決着(324)** |

### 5.3 凍結予言

| # | 予言 |
|---|---|
| **P-PH2-1** | $K^{(81)}\cap N_{S4}$ ⟹ $\lvert\mathrm{Im}\rvert=972$(§1 の機構) |
| **P-PH2-2** | 全候補で $\lvert\mathrm{Im}\rvert\in\{324,972\}$(中間値なし・SINGLE-BIT) |
| **P-PH2-3** | 全候補で $\lvert GT(K)\rvert\ge972$(前フィルタは不発火) |

---

## §6 実行分担(裁定 1024 基準・Sol は便 124 監査中 ⟹ 工房優先)

| 候補 | gating 上界 | 担当 | 備考 |
|---|---:|---|---|
| ★ **$l=36$** | $1.18\times10^7$ | ★ **工房**(まず実測で真の $\lvert PB_3/K\rvert$ を出す — fiber product は縮む) | **最優先** |
| $l=72$ | $9.4\times10^7$ | 工房(実測次第)/ 超えれば Sol | 第 2 |
| $l=45,54$ | $1.8\times10^8$ / $4.0\times10^7$ | 工房 or Sol | 第 3 |
| $l=63,81,108$ | $5\times10^8$〜$1.1\times10^9$ | ★ **Sol(便 125)** | 対照・累積段 |

★ **上界は上界です**: 深さ 1 の実績(`pb3_free_factor_check_v1` §4 の予測どおり fiber product は縮み、$168^2=28{,}224$ の上界に対し実値 7,056 = 1/4)⟹ **各候補で真の指数を先に測ること**([0-1] 型)。

---

## §7 Phase 1 の方法論のスケーリング

Phase 1 = **候補限定 lift 判定**($u_K\equiv u_M$ で候補 6 個)+ **縮小版 ground truth 検算**。

| 項目 | 深さ 1 | 深さ 2($l=36$)の見立て |
|---|---|---|
| 候補数/shadow | 6 | $\approx\lvert GT(K)\rvert/\lvert GT(M)\rvert$ 級 ⟹ **$\lvert GT(K)\rvert$ を測ってから確定**([0-3]) |
| 判定 1 件のコスト | hexagon + 全射性(既存器) | **同一**(窓が変わるだけ) |
| 総コスト | $972\times6$ | $972\times(\text{候補数})$ |
| ground truth | 縮小版で検算 | ★ **同じ方式が使える見込み**(窓依存の部分は $K$ の構成のみ) |

$$\boxed{\ \textbf{方法論はそのまま流用可。効く変数は「候補数」= }\lvert GT(K)\rvert\ \textbf{ただ一つ}\ }$$
⟹ **[0-3](候補ごとの $\lvert GT(K)\rvert$ 計数)を gating と同時に測れば、総コストが発火前に確定します。**

---

## §8 実装 spec

```
=== [D972-2] Phase 2(A 型の有限証明書探索・半決定)===
根拠: docs/notes/d972_phase2_design_v1.md
⚠ u/c 非接触・「genuine」を有限深度から導かない(掟 2)

[2-0] gating(候補ごと・必須)
   (a) K := K^(l) cap N_S4 を 2 本の epi の核として構成(pb3 §4 の型)
   (b) 真の |PB_3/K| を実測(★ 上界 §4 の表・実値は縮む)
   (c) |GT(K)| を計数   ★ 前フィルタ: < 972 なら即決着(§4.2)
   (d) 候補数/shadow の見積り(= §7)
   ⟹ ここまでで総コストが確定。超過なら Sol へ(便 125)
[2-1] 本測定: Im R_{K,M} を (3.60) の truncation で作り位数を出す
[2-2] fail-closed: |Im| in {324,972} / A ⊆ Im / 中間値なら即停止
[2-3] 単調性の回帰: 既測の深さ 1(972)と factorization §3.1 の整合
[2-4] 記録: 候補 l ・|PB_3/K| ・|GT(K)| ・|Im| ・所要時間
出力: cert (schema d972_phase2/v1)。整数のみ。u_touched=false
発火順: l=36 → 72 → 45/54 →(Sol)63/81/108
```

---

## §9 記帳

- ★ **本設計の新規部分**: ① **深さ 1 の 972 の機構解剖**(Thm 4.3 の明示形から 3-塔の reduction が全射・位数 9 倍則)と予言 P-PH2-1 ② ★★ **$[GT(M):A]=r$ の恒等式**(ギャップ = Kummer 絡み)⟹ 横断軸の優先 ③ 便 124 §4.2 の 2 点の織り込み(factorization・**cofinality を命題 INT の累積交叉で満たせるがコスト爆発** ⟹ **半決定へ格下げ**)④ **軸 (ii) の訂正**($N_{S4}$ が isolated ゆえ Prop 3.14 は細分を与えない)⑤ 全候補の gating を正典公式から先に計算($l=36$ が最安)⑥ **前件が命題 INT で既に閉じている**こと ⑦ Phase 1 方法論のスケーリング(効く変数は $\lvert GT(K)\rvert$ 一つ)。
- ★ **novelty grep 領収書**(裁定 1128 の規律):
 | クエリ | ヒット | 判定 |
 |---|---:|---|
 | `verbal.{0,20}isolated\|isolated.{0,20}verbal` | **14** | ★ **既出**(`auto_settled_check_v1` の **VERBAL-ISO**・`b4_direct_adjudication_feasibility_v1` §266)⟹ 本書では**引用**扱い。verbal 細分は候補軸として言及するに留め、新規主張はしない |
 | `GT\(M\).{0,10}:.{0,10}A\|指数.{0,10}=.{0,10}r` | 16 | 別文脈(分岐指数等)のみ ⟹ **$[GT(M):A]=r$ の同定は新規**(ただし恒等式で初等) |
 | `深さ 2\|depth 2\|Phase 2` | 195 | 大半は別戦役(aside/EP 等)⟹ 本件の Phase 2 は新規 |
- **【PH2-GAP-1】(小・新)** §1 の「3-塔 reduction が全射」は Thm 4.3 の**明示形からの読み**であり、$R$ の全射性そのものを逐語で確認していません ⟹ P-PH2-1 がその検定を兼ねます。
- ⚠ **撤回**: `battle_plan v1_1` §5.2/§7.1 の「決定手続き」表記(⟹ 修理 v1.2 で「半決定/有限証明書探索」へ・裁定 1139 発注 2)。
- **申告**: python(`scratchpad/d972_phase2_gating.py`・整数演算のみ)+ 紙。本書の全数値は機械生成。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
