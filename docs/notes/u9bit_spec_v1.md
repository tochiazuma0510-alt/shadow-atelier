# U9-BIT 計算仕様 v1(裁定 857)— ENT-PREFLIGHT 首位行の唯一の未知量

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・判定語の発効は司令塔専権)
**位置**: `見立て_相2_v1_4_2.md` §10 の**首位行(972 復活形 $K^{(9)}\times N_{S4}$)**の分岐を決める量。
**これは反例本走ではない** — Sol P2.1「$Q_A^{\rm lb}$ は実際の共通部分体または整合する共通商を**構成**して初めて使える」の**履行そのもの**($A$ の同時像の下界構成)。

---

## §0 結論 — 実験は**体の合成次数 1 個**に落ちる

$A=\mathrm{im}(G_\mathbf Q\to A_1\times A_2)$ は**合成体のガロア群そのもの**:
$$\boxed{\ \lvert A\rvert=[\,L_9L_{S4}:\mathbf Q\,]\qquad\Longrightarrow\qquad \lvert X\setminus A\rvert\ =\ 972-[\,L_9L_{S4}:\mathbf Q\,]\ }$$
($\lvert X\rvert=\lvert GT(M)\rvert=972$ は CRT-INJ・$A\subseteq X$ はカナリア)

| $[L_9L_{S4}:\mathbf Q]$ | $\lvert Q_A\rvert=\lvert A_1\rvert\lvert A_2\rvert/\lvert A\rvert$ | $\lvert X\setminus A\rvert$ | 読み |
|---:|---:|---:|---|
| **972** | 6 | **0** | 共有は円分のみ ⟹ **null** |
| **324** | 18 | **648** | 部分共有 |
| **108** | 54 | **864** | 完全共有($u$ 一致) |

> ### ★★ **飽和仮定は不要**(v1.4.2 の上界較正版より強い)
> $A$ は $A_1,A_2$ の**同時像**として直接 $\mathrm{Gal}(L_9L_{S4}/\mathbf Q)$ に等しい。$A_i=GT(N_i)$(飽和)を**使わない**。
> ⚠ ただし $A_i$ を**具体的に知らないと合成体が作れない**。$A_i$ が上界までしか分からない場合は $[L_9L_{S4}:\mathbf Q]$ の**上界**が出て $\lvert X\setminus A\rvert$ の**下界**が出る ⟹ **陽性側だけ言える**(v1.4.2 §3.1 の非対称性と整合)。

---

## §1 $u_9$ とは正確に何か

### 1.1 群論側の事実(既収)

- $\Theta_9\cong\mathrm{Aff}(\mathbb Z/9)\times C_2$(ihnec 戦役・定理 U-11)。$\lvert\mathrm{Aff}(\mathbb Z/9)\rvert=9\cdot\varphi(9)=9\cdot6=54$ ⟹ $\lvert\Theta_9\rvert=108=\lvert GT(K^{(9)})\rvert$ ✔
- $\mathrm{Aff}(\mathbb Z/9)=\mathbb Z/9\rtimes(\mathbb Z/9)^\times$。$(\mathbb Z/9)^\times\cong C_6$。
- $N_{S4}$ 側: $\lvert GT(N_{S4})\rvert=54$、$\mathfrak F_0\cong C_9$、$m$-像はちょうど 6 元(= charming set 全体)⟹ $54=6\cdot9$ ✔

### 1.2 ★ 算術側の翻訳(**$u_9$ の定義**)

$\mathrm{Aff}(\mathbb Z/9)$ をガロア群にもつ $\mathbf Q$ 上の体は **Kummer-円分型**:
$$\mathbf Q\bigl(\zeta_9,\ \sqrt[9]{u}\bigr)\Big/\mathbf Q,\qquad \mathrm{Gal}\cong\mathbb Z/9\rtimes(\mathbb Z/9)^\times=\mathrm{Aff}(\mathbb Z/9)$$
($u\in\mathbf Q^\times$ が 9 乗類として自明でなく、かつ Kummer 層が完全に立つとき)。

> ### ★ 定義 **$u_9$**
> $$\boxed{\ u_9\in\mathbf Q^\times/(\mathbf Q^\times)^9\ \textbf{= 窓 }K^{(9)}\ \textbf{の算術体 }L_9\ \textbf{に含まれる次数 }9\ \textbf{Kummer 層の生成データ}:\ L_9\supseteq\mathbf Q(\zeta_9,\sqrt[9]{u_9})\ }$$
> $C_2$ 因子は二次捻り $\mathbf Q(\sqrt d)$ に対応(共有判定には**第二の座標**として別に効く)。

**$N_{S4}$ 側**: $\mathfrak F_0\cong C_9$ が同じく次数 9 の層を持つ ⟹ その生成データを $u_{S4}\in\mathbf Q^\times/(\mathbf Q^\times)^9$ とする。

> ### ★★ **U9-BIT の正確な述語**
> $$\boxed{\ \textbf{U9-BIT} := \bigl[\ \mathbf Q(\zeta_9,\sqrt[9]{u_9})=\mathbf Q(\zeta_9,\sqrt[9]{u_{S4}})\ \bigr]\ \iff\ \exists a\in(\mathbb Z/9)^\times:\ u_{S4}\equiv u_9^{\,a}\ \ \bigl(\mathrm{mod}\ (\mathbf Q^\times)^9\bigr)\ }$$
> **真** ⟹ 9 の層が共有 ⟹ $\lvert Q_A\rvert\ge54$(円分 6 × 9)⟹ $\lvert X\setminus A\rvert=864$
> **偽だが二次層は共有** ⟹ $\lvert Q_A\rvert=18$ ⟹ $648$
> **完全に独立** ⟹ $\lvert Q_A\rvert=6$ ⟹ **0(null)**

---

## §2 有限計算への還元(**3 段・上から安い順**)

### 段 A(事前スクリーン・最安)— **分岐素点の突合**

$L_9$ と $L_{S4}$ はともにガロア。**分岐素点集合** $S_9$, $S_{S4}$ を判別式から取る。
$$\boxed{\ S_9\cap S_{S4}\subseteq\{3\}\ \textbf{(円分 }\mathbf Q(\zeta_9)\ \textbf{の分岐素点のみ)}\ \Longrightarrow\ L_9\cap L_{S4}\subseteq\mathbf Q(\zeta_9)^{+\cdots}\ \Longrightarrow\ \lvert Q_A\rvert\le6\ \Longrightarrow\ \textbf{null 確定}\ }$$
**根拠**: $L_9\cap L_{S4}$ は両方の中の部分体ゆえ $S_9\cap S_{S4}$ の外で不分岐。$\{3\}$ の外で不分岐な $\mathbf Q$ の abel 拡大は $\mathbf Q(\zeta_{3^k})$ の部分体(Kronecker–Weber)⟹ 非 abel 部分は立たない。
⟹ ★ **この 1 段で null が確定する可能性がある。費用 = 判別式の素因数分解 2 個(ミリ秒)。**

### 段 B(本判定・初等整数演算)— **指数ベクトル mod 9**

$u_9=\prod_\ell \ell^{e_\ell}$、$u_{S4}=\prod_\ell \ell^{f_\ell}$(有理数の素因数分解)。
$$\boxed{\ \textbf{U9-BIT} \iff \exists a\in(\mathbb Z/9)^\times=\{1,2,4,5,7,8\}:\ \ f_\ell\equiv a\,e_\ell\ (\mathrm{mod}\ 9)\ \ \forall\ell\ }$$
**費用**: 2 個の有理数の素因数分解 + 6 通りの比較 = **ミリ秒**。
⚠ **これは十分条件**($\mathbf Q$ の 9 乗類が一致すれば体は一致)。**必要性**は $\mathbf Q^\times/(\mathbf Q^\times)^9\to\mathbf Q(\zeta_9)^\times/(\mathbf Q(\zeta_9)^\times)^9$ の単射性に依存 ⟹ 段 C で安全化。

### 段 C(安全版)— **$\mathbf Q(\zeta_9)$ 上の 9 乗判定**

$K=\mathbf Q(\zeta_9)$(次数 6)で
$$\textbf{U9-BIT}\iff \exists a\in(\mathbb Z/9)^\times:\ u_{S4}\,u_9^{-a}\in (K^\times)^9$$
**PARI**: `K=nfinit(polcyclo(9)); nfispower(K, u_S4*u_9^(-a), 9)` を $a$ の 6 通りで。**費用 = ミリ秒**。
**別解(合成体を直接作る)**: 定義多項式が取れるなら `polcompositum` で $[L_9L_{S4}:\mathbf Q]$ を直接算出 ⟹ §0 の表に直接落ちる。**費用 = 秒**(次数 $\le972$ の合成は重いので**部分体ごと**に段階的に)。

---

## §3 DOMAIN-PIN 札 **P-U9BIT**(IF-FIRST 凍結・測定前)

| 項 | 内容 |
|---|---|
| **述語** | $\exists a\in(\mathbb Z/9)^\times:\ u_{S4}\equiv u_9^a\ \bigl(\mathrm{mod}\ (\mathbf Q^\times)^9\bigr)$(等価: $\mathbf Q(\zeta_9,\sqrt[9]{u_9})=\mathbf Q(\zeta_9,\sqrt[9]{u_{S4}})$) |
| **定義域** | $\{K^{(9)},\,N_{S4}\}$ の**単一対**。他の対・他の $n$ には及ばない |
| **帰属根拠** | $\Theta_9\cong\mathrm{Aff}(\mathbb Z/9)\times C_2$(ihnec U-11)+ $\mathfrak F_0(N_{S4})\cong C_9$ + $\lvert GT(M)\rvert=972$(CRT-INJ で $\lvert X\rvert=972$) |
| **chi_semantics** | 該当なし(体の同一性・Kummer 類) |
| **factor_filter** | 次数 9 の Kummer 層のみ。**落とした因子**: $C_2$ 二次捻り(段 B/C とは別座標・$\lvert Q_A\rvert=18$ 枝の判定に要る)・$m$/円分層(常に共有・下界 6) |
| **関手 / 比較射** | $N\mapsto L_N$(窓 ↦ 算術体)。比較射 = **合成体の取り方**(標準・新規構成なし) |
| ★ **凍結予言** | **予言を置く**: 段 A(分岐素点)で **$S_9\cap S_{S4}\subseteq\{3\}$ となり null が確定する**(= $\lvert X\setminus A\rvert=0$)。理由 = 二窓は独立な戦役で選ばれ、共通の非円分分岐を持つ設計上の理由がない |
| **陽含意**(予言が外れ = 共有あり) | $\lvert Q_A\rvert\in\{18,54\}$ ⟹ $\lvert X\setminus A\rvert\in\{648,864\}$ ⟹ ★ **窓 $M$ の非全射証人が大量に立つ** ⟹ **QUAR 検疫**(独立再構成・両座標の genuine 再検査)を経てから報告。**これは井原直撃** |
| **陰含意**(予言どおり = null) | ★ **ENT-PREFLIGHT 首位行が落ちる** ⟹ 表の残りは 2 位(落選済)と 3 位(A-GRAPH 待ち)のみ ⟹ **CRT-ENTANGLE 全体が候補枯渇の可能性**を正直に記載する。**同時に**「二窓の Kummer 座標は独立」= 算術の新事実(小さいが確定情報) |

> ### ⚠ **正直な見通し**(過大禁止)
> $$\boxed{\ \textbf{予言は null 側に置いた。当たれば ENT-PREFLIGHT は全滅しうる — それを隠さずに凍結する。}}$$

---

## §4 実装係への作業指示

> ### 発注 **U9-BIT-EXTRACT**(段 0・**前件**)
> **registry / ihnec 戦役の cert から次を抽出せよ**:
> 1. $L_9$ の**定義データ**: 定義多項式・判別式・分岐素点、または **$u_9$ の値**($\mathrm{Aff}(\mathbb Z/9)$ 部の Kummer 生成元)と二次捻り $d$。
> 2. $L_{S4}$ の同上(**$u_{S4}$** と $\mathfrak F_0\cong C_9$ の生成データ)。
> 3. どちらも**無ければ即報告**(= 本仕様の前件不成立 ⟹ 「算術側の同定が未了」を §10 の表の空欄として確定)。
> **★ これが本仕様の唯一の実質的リスク**: 群論側は全て既測だが、**算術体の同定が cert にあるか未確認**。

> ### 発注 **U9-BIT-CALC**(段 A→B→C・**抽出が成功したときのみ**)
> | 段 | 入力 | 出力 | 資源 |
> |---|---|---|---|
> | **A** | $\mathrm{disc}(L_9)$, $\mathrm{disc}(L_{S4})$ | $S_9\cap S_{S4}$。$\subseteq\{3\}$ なら **null 確定・以降不要** | 素因数分解 2 個・**ミリ秒** |
> | **B** | $u_9,u_{S4}$ の素因数分解 | $\exists a\in\{1,2,4,5,7,8\}: f_\ell\equiv a e_\ell\ (9)$ の真偽 | **ミリ秒**(純整数) |
> | **C** | 同上 | `nfispower(nfinit(polcyclo(9)), u_S4*u_9^-a, 9)` を 6 通り | PARI・**ミリ秒** |
> | **C′**(任意) | 定義多項式 | `polcompositum` で $[L_9L_{S4}:\mathbf Q]$ を直接 | **秒〜分**(次数に依存・部分体ごとに段階的に) |
> **出力形式**: 生値(素因数分解・boolean・次数)のみ。**判定語なし**。$\lvert X\setminus A\rvert$ の値は**司令塔の裁定を経てから**書く。
> **カナリア**: 段 B と段 C が**一致すること**(段 B は十分条件・段 C は必要十分 ⟹ B が真なら C も真であるべき。B 偽・C 真なら $\mathbf Q\to\mathbf Q(\zeta_9)$ の 9 乗類の単射性が破れている = 要調査)。
> **禁止**: 合成体を次数 972 のまま一気に作らない(部分体経由で段階的に)。

---

## §5 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| ★ **【U9-GAP-1】** | **$L_9$・$L_{S4}$ の算術体としての同定が cert にあるか未確認** — 本仕様の唯一の前件 | ★★ 決定的 |
| **【U9-GAP-2】** | $\mathrm{Aff}(\mathbb Z/9)$ が Kummer-円分型で実現される(= $L_9$ が $\mathbf Q(\zeta_9,\sqrt[9]{u_9})$ を含む)ことは**群の形からの推定** — $L_9$ の実体で確認が要る | ★ 中 |
| **【U9-GAP-3】** | $\lvert Q_A\rvert=18$ 枝(二次捻りの共有)の判定は段 B/C とは別座標 — 仕様は $C_2$ 側を書いていない | 中 |
| **【U9-GAP-4】** | $A_i$ が飽和でない場合、合成体は $A_i$ の実体を要する(上界だけでは陽性側のみ) | 小 |

**帰属**: 委嘱 = 司令塔(裁定 857・研究者の意向)。$u_9$-共有ビットの着想 = **発案係**(`ideas_ent_targets_v1.md` 対 (b))。$\Theta_9\cong\mathrm{Aff}(\mathbb Z/9)\times C_2$・$\lvert GT(M)\rvert=972$・$\mathfrak F_0\cong C_9$ = ihnec 戦役。$Q_A^{\rm lb}$ の構成要求 = **Sol**(P2.1)。
**本仕様の新規部分** = ★ **$\lvert A\rvert=[L_9L_{S4}:\mathbf Q]$ という還元(実験が体の合成次数 1 個に落ち、飽和仮定が不要になる)** / **$u_9$ の Kummer 生成元としての定義** / **U9-BIT の述語形($\exists a\in(\mathbb Z/9)^\times$)** / **段 A の分岐素点スクリーン(Kronecker–Weber で null を先に確定できる)** / **段 B の指数ベクトル mod 9 判定(ミリ秒)** / **札 P-U9BIT(予言を null 側に置く)** / **発注 2 本と段 B/C のカナリア**。

**novelty grep**: `U9-BIT` `P-U9BIT` `U9-BIT-EXTRACT` `U9-BIT-CALC` = **0 hit(本仕様初出)**。`u_9` は `ideas_ent_targets_v1.md` に既在(着想)。

**検算**:
```bash
python -c "
GTM=972; A1,A2=108,54
for QA in (6,18,54):
    A=A1*A2//QA
    print('|Q_A|=%2d -> |A|=[L9 L_S4:Q]=%4d -> |X-A|=%3d'%(QA,A,GTM-A))
print('(9Z)^x =',[a for a in range(1,9) if a%3])
"
# 期待: 6->972->0 / 18->324->648 / 54->108->864 ; (Z/9)^x = 1,2,4,5,7,8
```
