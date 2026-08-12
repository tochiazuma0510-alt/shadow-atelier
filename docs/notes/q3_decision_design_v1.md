# [Q3-R1] 結果の解釈と (Q3) 決着設計(裁定 1063)

作成: 数学者(Opus 5)/ 2026-08-13 / 入力 = cert `q3_r1_prefilter_v1`(charming 30,360 中 $u\in\{1,-1\}$ の 2 個のみ生存)
前提 = `iso_family_lemma_v1.md`(SETTLE-AUTO)・`q3r1_lift_spec_v1.md`($N_{\rm ord}=47679$)
⚠ $u$/$c$ 非接触・prereg 非抵触。**格: candidate**。

---

## §0 結論(3 行)

1. ★★★ **(Q3) の決着は 1 問に還元されます**:**「hexagon(+charming+全射)が $u\notin\{\pm1\}$ で可解か」**。YES なら **非 isolated 確定**、NO なら残りは $u=\pm1$ の 2 系のみ。
2. ★★ **生存 2 個は構造的に自己同型で実現されます**:$u=+1$ は**内部共役系**、$u=-1$ は **$\iota:\sigma_i\mapsto\sigma_i^{-1}$ 系**($\iota$ が $B_3$ の自己同型であることを検算)⟹ **settled になる筋**。
3. ⚠ **前フィルタは「候補宇宙が制限される」ことを示していません** — 落としたのは $\bar x=\sigma_1^2$ 上の条件で、hexagon は $\sigma_1$ 上の条件です ⟹ **独立の測定が要る**(§3)。

---

## §1 前フィルタが落としたものの機構

$\bar x\in SL(2,\mathbf Z/p^2)$ の固有値を $\mu,\mu^{-1}$($\det=1$)とすると
$$\mathrm{tr}(\bar x^{\,u})=\mu^u+\mu^{-u}=\mathrm{tr}(\bar x)\iff \mu^u=\mu^{\pm1}\iff u\equiv\pm1\ (\mathrm{mod}\ \mathrm{ord}\,\mu)$$
⟹ ★ **生存が $\{1,-1\}$ の 2 個なのは構造的に正しい形**です。$u=-1$ の生存は「$\det=1$ ゆえ $\bar x^{-1}$ は $\bar x$ と同 trace」の**恒等的帰結**(司令塔の指摘どおり)。

---

## §2 ★★ 生存 2 個の**構造的な正体**

| $u$ | $T$ の正体 | settled か |
|---|---|---|
| **$+1$** | $T(\sigma_1)=\sigma_1$、$T(\sigma_2)=f^{-1}\sigma_2f$ ⟹ **$\sigma_1$ を固定する自己同型**の候補 = **中心化群 $C_{\tilde H}(\sigma_1)$ による共役** | ★ 共役なら自己同型 ⟹ SETTLE-AUTO で **settled** |
| **$-1$** | ★ **$\iota:\sigma_i\mapsto\sigma_i^{-1}$ は $B_3$ の自己同型**(検算: 関係式の両辺の逆をとると $\sigma_1^{-1}\sigma_2^{-1}\sigma_1^{-1}=\sigma_2^{-1}\sigma_1^{-1}\sigma_2^{-1}$ ⟹ 保たれる)⟹ $T=\iota$ の後に共役 | ★ 同上 ⟹ **settled** |

$$\boxed{\ \textbf{生存 2 個はどちらも「}\tilde H\ \textbf{の自己同型で実現される」筋 — つまり }\textbf{settled}\ \textbf{になる側}\ }$$

⚠ ただし **「その $u$ の GT-pair がすべて自己同型で実現される」は未証明** ⟹ §5。

---

## §3 ★★★ (Q3) の決着が 1 問に還元される

**SETTLE-AUTO の対偶**: well_defined でない ⟹ $N_{F_2}\not\subseteq\ker T$ ⟹ $\ker T\ne N'$ ⟹ **非 settled**。
**前フィルタ**: $u\notin\{\pm1\}$ ⟹ $\bar x^u\not\sim\bar x$ ⟹ $\bar T$ は自己同型になり得ない ⟹ **well_defined 不可**。

$$\boxed{\ u\notin\{\pm1\}\ \textbf{の}\ \textbf{shadow}\ \textbf{が 1 個でも存在}\ \Longrightarrow\ \textbf{非 settled shadow 存在}\ \Longrightarrow\ \textbf{★ 非 isolated 確定}\ }$$

⟹ ★ **司令塔の問い「存在すれば SETTLE-AUTO 経由で非 isolated 確定の筋か」への回答 = YES** ✔

⚠★ **ただし「候補宇宙が $u=\pm1$ に制限される」ことは示されていません**:
- 前フィルタの条件は **$\bar x=\sigma_1^{\,2}\in SL(2,\mathbf Z/p^2)$** 上のもの(well_defined の必要条件)
- hexagon の条件は **$\sigma_1\in SL^\pm(2,\mathbf Z/p^2)$** 上のもの(候補であるための条件)
$$\boxed{\ \Longrightarrow\ \textbf{両者は別の量。候補宇宙の判定は}\textbf{独立の測定}\ \textbf{が要る}\ }$$

---

## §4 ★ その 1 問の**測定可能な形**(M1)

$c\mapsto1$ ゆえ $T$ は $B_3/\langle c\rangle=PSL(2,\mathbf Z)=C_2*C_3$ を経由 ⟹ $T$ は次の 2 元で決まります:
$$u':=T(\Delta)\ (u'^2=T(c)=1),\qquad v':=T(\sigma_1\sigma_2)\ (v'^3=T(c)=1)$$
$$T(\sigma_1)=v'^{-1}u'=\sigma_1^{\,u}$$
shadow なら**全射** ⟹ $(u',v')$ は **$(2,3)$-生成対**。

$$\boxed{\ \textbf{(M1)}\quad \exists\,(2,3)\text{-生成対}\ (u',v')\ \text{で}\ \sigma_1^{\,u}=v'^{-1}u'\ \text{となる}\ u\notin\{\pm1\}\ \text{はあるか}\ }$$

⟹ ★ これは **$\sigma_1^{\,u}$ の共役類が「(位数 3)$^{-1}\cdot$(位数 2)」の像に入るか**の判定 ⟹ **共役類の計算で済み、巨大群の列挙は不要**。

```
=== [Q3-M1] 候補宇宙の $u$ 制限の判定 ===
前提: σ_1 ∈ SL^±(2,Z/691^2)(q3r1_lift_spec_v1 §3 の実測値)、N_ord = 47679
[M1-a] 各 u ∈ (Z/47679)^×(30,360 個)について σ_1^u を計算(冪乗・秒)
[M1-b] ★ 必要条件フィルタ: σ_1^u が「位数 2 の元 × 位数 3 の元」の積として書けるか
       ⟹ SL^±(2,Z/p^2) における位数 2・位数 3 の元の共役類は標準分類で書ける
       ⟹ 積の集合(= C_2*C_3 の像に入る元の集合)を共役類レベルで判定
[M1-c] 生存した u について、(u',v') が *生成* するかを非分裂論法で確認
       (F_stage2_completion_v1 §2.4 と同じ論法 ⟹ reduction が SL^±(2,691) を生成すれば十分)
[M1-d] ★ 判定:
   ・u ∉ {±1} で生存が 1 個でもある ⟹ ★★ 非 isolated 確定(§3)
   ・生存が u ∈ {±1} のみ ⟹ §5(M2)へ
出力: cert (schema q3_m1/v1)。u_touched=false ; c_touched=false
```

---

## §5 ★ 生存 2 個の精査設計(M2)

$u=\pm1$ に絞られた場合、isolated を言うには「**その $u$ の shadow がすべて settled**」が要ります。

**$\bar y$ 側の同時共役性**(司令塔の指摘):well_defined ⟺ $\bar T$ が自己同型 ⟺ **単一の $g$ で $\bar x^u=g\bar xg^{-1}$ かつ $\bar f^{-1}\bar y^u\bar f=g\bar yg^{-1}$**。
⟹ ★ **$\bar x$ 側だけの共役性は片側フィルタ**(ISO-GAP-2)。

**$f$ の自由度の構造**:
- $u=+1$: $\bar T$ が $\bar x$ を固定 ⟹ $g\in C_{\tilde H}(\sigma_1)$ ⟹ $f^{-1}\sigma_2f=g\sigma_2g^{-1}$ ⟹ ★ **$u=1$ の shadow 全体は $C_{\tilde H}(\sigma_1)$ の作用で記述される** ⟹ すべて共役 ⟹ **settled**
- $u=-1$: 同じ議論を $\iota$ の後に適用 ⟹ **settled**

⚠ **残る穴**: 「$u=\pm1$ の GT-pair で $T$ が自己同型に**ならない**もの」が存在しないか。存在すれば非 settled。
⟹ ★ **これは ISO-RIGID$^{\rm w}$ の $u=\pm1$ 制限版**:
$$\boxed{\ \textbf{(M2)}\quad \sigma_1\ \text{を固定する(あるいは }\iota\ \text{に付随する)braid 対がすべて }\mathrm{Aut}(\tilde H)\text{ の一軌道か}\ }$$
```
=== [Q3-M2] u=±1 の精査(M1 が「±1 のみ」を返した場合のみ)===
[M2-a] x := σ_1^{u}(u=±1)を固定。braid の相方 y は
       u' := xyx(u'^2=1)、v' := u'x^{-1}(v'^3=1)で決まる
       ⟹ ★ y ⟷ 「(u'x^{-1})^3 = 1 を満たす対合 u'」の集合
[M2-b] ⚠ |H~| ≈ 6.5e17 ⟹ 列挙不可 ⟹ ★共役類レベルで「そのような u' の類」を数える
[M2-c] 一軌道なら ⟹ 全 shadow settled ⟹ ★ isolated 確定
       複数軌道なら ⟹ 各軌道で ker T を比較(核が異なれば非 isolated)
出力: cert (schema q3_m2/v1)
```
★ **順序**: **(M1) を先に**。(M1) が YES なら (M2) は**不要**(非 isolated 確定)。

---

## §6 ★ ③ 線の帰結(どちらに転んでも一行)

| 分岐 | ③ 線の帰結 |
|---|---|
| **isolated** | $\rho_{N'}$ が群準同型として定義される ⟹ ★ **(Q4) SURG バッテリーへ**(crown 検定 + receipt)。⚠ SURG-A6 の算術の代金は不変 |
| **非 isolated** | $GT(N')$ は群でない ⟹ 段 2 の対象は ★ **集合写像 $a_{N'}$ の水準** ⟹ **TYPE-IMAGE$^\rho$ の五対象が定義できない** ⟹ ③ 線の**形を再定義**(比較の土俵が変わる) |

$$\boxed{\ \textbf{★ どちらでも段 2 の}\textbf{群論的成果}\textbf{(容器・非分裂拡大・braid 全射)は無傷}\ }$$
失われるのは**「算術像を群準同型として比較する枠」だけ**です。⟹ ★ **F4 型の否定的結果と同じく、扉が一枚閉まるだけで資産は残ります**。

⚠ **非 isolated の場合の追加所見**: census(83 窓)では **15 窓中 13 窓が非 isolated** でした ⟹ ★ **非 isolated は例外ではなく標準**。⟹ ③ 線が非 isolated でも「失敗」ではなく、**$a_N$ 水準での比較法(= 未整備の枠)を作る**という次の課題になります。

---

## §7 GAP・記帳

- **【Q3-GAP-1】(中・新)** (M1) の「$\sigma_1^u$ が (位数2)×(位数3) の積か」の共役類判定は、$SL^\pm(2,\mathbf Z/p^2)$ の共役類分類を要する ⟹ **正典外の標準事実**(Q3R1-GAP-1 と同根)。自前再導出可能 ⟹ 文献要請は不要。
- **【Q3-GAP-2】(中・新)** (M2) の「一軌道か」は ISO-RIGID$^{\rm w}$ の実体 ⟹ **未証明**。列挙不可なので共役類レベルの議論が要る。
- **【ISO-GAP-2】(継続)** $\bar x$ 側だけの共役性は**片側フィルタ** — $\bar y$ との**同時**共役が本条件。
- ★ **本ノートの新規部分**: ① 前フィルタが落としたものの **trace 機構**($u\equiv\pm1\bmod\mathrm{ord}\,\mu$)② **$\iota:\sigma_i\mapsto\sigma_i^{-1}$ が $B_3$ の自己同型**であることの検算と $u=-1$ の構造的正体 ③ ★★ **(Q3) が「hexagon が $u\notin\{\pm1\}$ で可解か」の 1 問に還元**されること ④ ★ **前フィルタの量($\sigma_1^2$)と候補宇宙の量($\sigma_1$)が別物**であることの明示(独立測定が要る)⑤ (M1)(M2) の測定仕様 ⑥ 両分岐の ③ 線帰結と「群論的成果は無傷」。
- **申告**: 機械走行ゼロ(既走 cert の解釈 + 紙)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
