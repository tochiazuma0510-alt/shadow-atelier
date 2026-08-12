# 【検算 B′】I-SET-4 座標捻りの再測定 spec(prereg)— 裁定 1089

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1089
前提 = `set_surgery_vetting_v1.md` §6(型の 2 か所の誤り・charming 交絡)・定義ノート L153–173・cert `set_surgery_fixture_v1_20260813`
⚠ $u$/$c$ 非接触・封印非接触・prereg 非抵触・算術入力ゼロ。**格: candidate**。

---

## §0 このターンで測るべき唯一のこと

前回の測定(生存率 1/12・1/28)は、**総率としては原理的に情報を持ちません**(§1 の定理 SURV-EXACT で率が先に決まってしまう)。
$$\boxed{\ \textbf{情報があるのは}\ \mathrm{Surv}(t)\cap C_Q(\bar\sigma_1)\ \textbf{の構造だけ}\ }$$
本 spec はそこへ一直線に向かい、途中の落ちた理由を 3 分類して**交絡を切ります**。

---

## §1 ★ 定理 SURV-EXACT — 生存数は測る前に決まっている(fail-closed の親)

$N\in\mathrm{NFI}_{PB_3}(B_3)$、$Q:=F_2/N_{F_2}$。shadow は対 $[m,f]\in(\mathbf Z/N_{\rm ord})\times Q$ そのもの(定義ノート Def 3.1/3.7)。
$t=[m,f]\in GT(N)$ を固定し $\mathrm{Surv}(t):=\{q\in Q\ :\ [m,fq]\in GT(N)\}$ とおく。

> **【定理 SURV-EXACT】** $q\mapsto[m,fq]$ は $Q$ から「第 1 座標が $m$ の対全体」への**全単射**(左移動)。ゆえに
> $$\boxed{\ \bigl\lvert\mathrm{Surv}(t)\bigr\rvert\ =\ N_m:=\#\{[m',f']\in GT(N)\ :\ m'=m\}\ }$$
> 特に **$\lvert\mathrm{Surv}(t)\rvert$ は $t$ の $m$ にしか依らず**、$1\in\mathrm{Surv}(t)$ ゆえ $N_m\ge1$。

**帰結(前回測定の診断)**: $Q$ 全体を走らせた総生存率は $\bigl(\sum_t N_{m_t}\bigr)/(\lvert GT(N)\rvert\cdot\lvert Q\rvert)$ で、**$GT(N)$ の $m$-分布だけで決まります** ⟹ 率の報告は**新情報ゼロ**。
[1008,521]: $N_{\rm ord}=24$・$u\in\{1,5,7,11,13,17,19,23\}$(8 値)・48 shadow ⟹ 一様なら **$N_m=6$**(実測せよ)。

---

## §2 型の修正(2 か所・裁定 1089 で受諾済)

### 2.1 中心化群は **$Q$ 内**

$f\in Q=F_2/N_{F_2}$ ゆえ捻り $q$ も $Q$ の元。$PB_3=F_2\times\langle c\rangle$ より $Q\cong F_2N/N\le PN:=PB_3/N$ で、83 窓は $c\notin N$ ゆえ **$[PN:Q]=\mathrm{ord}(\bar c)>1$**。⟹ $PN$ 内で取ると型が壊れます。

### 2.2 捻りが内部自己同型になる条件は $C(\bar\sigma_1^{\,u})$ — ★ しかも $u$ に依りません

$T_{m,fq}(\sigma_2)=\mathrm{inn}_q\bigl(T_{m,f}(\sigma_2)\bigr)$ は自動。$\sigma_1$ 側は $\sigma_1^u$ 対 $q^{-1}\sigma_1^uq$ ⟹ 条件は $q\in C(\bar\sigma_1^{\,u})$。
★ charming より $\gcd(u,N_{\rm ord})=1$ かつ $u$ 奇 ⟹ $\gcd(u,\mathrm{ord}\,\bar\sigma_1)=1$($\mathrm{ord}\,\bar\sigma_1\mid2N_{\rm ord}$)⟹ $\langle\bar\sigma_1^{\,u}\rangle=\langle\bar\sigma_1\rangle$ ⟹
$$\boxed{\ C(\bar\sigma_1^{\,u})=C(\bar\sigma_1)\quad(\textbf{全 shadow 共通・}u\ \textbf{非依存})\ }$$
⟹ 正しい捻り集合は $\;\boxed{D_1:=C_Q(\bar\sigma_1)=C_{B_3/N}(\bar\sigma_1)\cap Q}$。発案係の $C_Q(\bar x)=C_Q(\bar\sigma_1^{\,2})\supseteq D_1$ は**広すぎます**。

### 2.3 charming が先に切る(交絡の正体)

charming は $\bar f\in[Q,Q]$。$\bar f\in[Q,Q]$ かつ $\bar f\bar q\in[Q,Q]$ ⟹ **$\bar q\in[Q,Q]$ が必要**。ゆえに
$$\boxed{\ \mathrm{Surv}(t)\subseteq[Q,Q]\quad(\textbf{常に・hexagon を見るまでもなく})\ }$$
⟹ **RIGID の正しい分母は $\;D_0:=C_Q(\bar\sigma_1)\cap[Q,Q]$**。

---

## §3 測定仕様 [B′]

```
=== [B'] 座標捻りの再測定 + 3 分類 ===
根拠: docs/notes/iset4_remeasure_spec_v1.md
対象: (i) N = [1008,521] slot1(既列挙 48 shadow)  (ii) K^(9)(isolated・陽性対照)
⚠ 算術入力ゼロ・u/c 非接触・封印非接触

[B'-0] 土台量を先に出す(これ自体が cert 行)
   |Q| = |F_2/N_{F_2}| ,  |PN| = |PB_3/N| ,  ord(c̄) = [PN:Q]
   [Q,Q] とその指数 ,  D_1 = C_Q(σ̄_1) ,  D_0 = D_1 ∩ [Q,Q] , 各位数
   ★ |D_0| = 1 なら本 fixture は RIGID について *空虚* ⟹ そう報告して終了(一級の陰性)

[B'-1] 全数走査: 各 shadow t=[m,f] × 各 q ∈ Q について 3 述語を *独立に* 評価
   (C) charming :  f̄q̄ ∈ [Q,Q]        （u 側の gcd 条件は捻りで不変ゆえ再評価不要）
   (S) 全射性   :  T_{m,fq} : B_3 → B_3/N が全射
                   ★ Prop 3.6 の同値は charming 前提 ⟹ (C) が偽の対では
                      full B_3/N 版で評価すること(近道禁止)
   (H) hexagon  :  full (3.3)(3.4) を B_3/N 内で評価
                   ★ 簡約版 (3.10)(3.11) は f ∈ [F_2,F_2] 前提(Prop 3.4)ゆえ使用禁止
                   ★ θ/τ は自由群の語レベルで適用してから φ で評価(定義ノート §2 の注意)
   出力: 各 (t,q) に (C,S,H) の 3 ビット。生存 = C∧S∧H
[B'-2] 集計(cert に生値のみ)
   (a) shadow ごとの |Surv(t)| と、m ごとの N_m
   (b) 落ちた理由の同時分布: (C,S,H) の 8 パターンの度数
   (c) ★ 主測定: 各 t について Surv(t) ∩ D_0 と Surv(t) ∩ D_1 の元(個数と元そのもの)
   (d) ★ 分離指標: D_0 \ {1} の中で「C は真・H が偽」の個数
       = *hexagon が単独で切った* 捻りの数 ⟹ これが 0 なら RIGID の証拠にならない
[B'-3] 見張り(fail-closed)
   (W1) |Surv(t)| = N_m を全 t で確認 ← 定理 SURV-EXACT。破れたら実装が誤り ⟹ 即停止
   (W2) 1 ∈ Surv(t) を全 t で確認(自明・恒等の陽性対照)
   (W3) q̄ ∉ [Q,Q] の全ての q で (C)=偽 かつ生存なし(定義の回帰)
   (W4) K^(9)(c ∈ N ⟹ Q = PN)で同じコードが走ること(型の縮退対照)
出力: cert (schema iset4_bprime/v1)。u_touched=false ; c_touched=false ; 判定は司令塔
★ 規模: 48 × |Q| の 3 述語評価 ⟹ 秒〜分級。|Q| が大きければ [B'-1] を D_1 ∪ [Q,Q] に制限してよい
   (その場合 (W1) は制限内の部分集合検査に格下げ ⟹ cert に明記)
```

---

## §4 ★ 事前登録(発火前に凍結)

| # | 予言 | 根拠 | 外れたときの行き先 |
|---|---|---|---|
| **T1** | $\lvert\mathrm{Surv}(t)\rvert=N_m$(全 $t$) | ★ **定理**(§1) | ⚠ **即停止** — 実装または核判定の誤り(型の取り違えを最初に疑う) |
| **T2** | $\mathrm{Surv}(t)\subseteq[Q,Q]$ | ★ **定理**(§2.3) | ⚠ 即停止(charming 実装の誤り) |
| **T3** | $C(\bar\sigma_1^{\,u})$ は $u$ に依らず $=C(\bar\sigma_1)$ | ★ **定理**(§2.2) | ⚠ 即停止($\gcd$ 条件の実装誤り) |
| **R1** | $\mathrm{Surv}(t)\cap D_1=\{1\}$(全 $t$) | ⚠ **予想 RIGID**(未証明) | ★ 反証なら**軌道手術が復活** ⟹ 発案 6 号札 4 の再評価・地図更新 |
| **R2** | $D_0\setminus\{1\}$ のうち「C 真・H 偽」が **過半** | ⚠ **予想**(交絡が小さいことの主張) | ★ 少数なら **fixture は RIGID について空虚** ⟹ 正直にそう記帳し、$N'$($[Q,Q]=Q$ ゆえ交絡なし)の SG-GAP-1 のみを証拠として残す |

⚠ **W-48**: 本 fixture の結果を $N'$ へ運ぶのは**外挿**。装置の較正であって $N'$ の結論ではありません。
⚠ **T1–T3 は定理なので「予言が当たった」ことに証拠力はありません** — 実装の健全性検査です。証拠力があるのは **R1・R2 のみ**。

---

## §5 記帳

- ★ **本 spec の新規部分**: ① **定理 SURV-EXACT**(生存数が $m$ だけで決まる ⟹ 総率は情報ゼロ)② $C(\bar\sigma_1^{\,u})=C(\bar\sigma_1)$($u$ 非依存化)③ $\mathrm{Surv}\subseteq[Q,Q]$ の定理化と**分母 $D_0$** の確定 ④ 3 述語の**独立評価**による交絡の切断と分離指標 (d) ⑤ 「$\lvert D_0\rvert=1$ なら空虚」という**早期打ち切り**。
- **【SS-GAP-2】** RIGID の紙証明は依然未着手。本測定は証拠の質を上げるだけで、証明にはなりません。
- **申告**: 紙のみ(機械走行ゼロ)。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
