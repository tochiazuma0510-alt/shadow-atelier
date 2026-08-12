# 【retarget (F) 検分】$H_F=\mathrm{SL}^\pm(2,691)\times_{C_2}S_3$ — ★ 三値 = **GO**(前哨 1 本から)

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 950(③ 線の繰り上げ)
**格**: candidate(紙・単系統・**Sol 未監査**)。走行ゼロ・**封印非接触**。
**検分対象**: `docs/notes/ideas_w691ext_retarget_v1.md`(発案係・裁定 872)の **(F) 主候補**

> ## ★★ 三値判定
> $$\boxed{\ \textbf{GO}\ }$$
> **観点 ① EXT-NOWIN 回避 = PASS** / **② RIBET-SECTION 非移植 = ★ PASS(erratum に逐語根拠あり)** / **③ 前哨あり(秒)** / **④ 変わるのは段 0–2**
> ★ **私の新規寄与**: **Goursat の懸念を消し、C2 を 1 つの検査に落とした**(§4)⟹ **最初の機械前哨は既走 cert の読み出し 1 本で済む**。

---

## §1 観点 ① — **EXT-NOWIN の外に出ているか = PASS**

**EXT-NOWIN**(見立て §1.5): $p>3$、$W$ を任意の有限 $p$-群、$1\to W\to E\to H_d\to1$。任意の $\pi:E\to S_3$ で $\pi(W)$ は $S_3$ の $p$-部分群、$p\nmid6$ ゆえ $\pi(W)=1$ ⟹ $\pi$ は $E/W\cong H_d$ を経由 ⟹ **HD-NOWIN** で全射不能。

**(F) での挙動**: 同じ論法を $H=H_F$ で走らせると、$\pi(W)=1$ ⟹ $\pi$ は $H_F$ を経由する、**までは同じ**。しかし
$$H_F=\bigl\{(g,s)\in\mathrm{SL}^\pm(2,691)\times S_3\ :\ \det g=\mathrm{sign}(s)\bigr\}\ \xrightarrow{\ \mathrm{pr}_2\ }\ S_3$$
は**全射**($\det:\mathrm{SL}^\pm\to\{\pm1\}$ が全射ゆえ、任意の $s$ に相方 $g$ が取れる)。
$$\boxed{\ \Longrightarrow\ \textbf{EXT-NOWIN の結論(非窓)が出ない ⟹ (F) は }\textbf{外に出ている}\ }$$
★ ⚠ **出方の型を正確に**: 「$W$ が $p$-群でない」からではなく、**$H$ を $H_d$ から $H_F$ へ替えた**から。⟹ 札の C0 の整理(「$W$ の $p$-群性は無害になった」)は**正しい**。

---

## §2 ★★ 観点 ② — RIBET-SECTION の障害は (F) に**移植されない = PASS**

### 2.1 障害の機構(**一次資料の逐語**)

`docs/notes/xd2_bridge_2b_v1_erratum_a.md` 行 52:

> ★ **(d) Borel 型は RIBET-SECTION で死ぬ**: $U\cong C_{691}$ は $H_0$ の**唯一の** Sylow 691 ⟹ $H_0$ で**特性**。$H_0\trianglelefteq H$ ⟹ $U\trianglelefteq H$ ⟹ $U$ は $G$ の**両端 $G$-正規な 1 次元切片**。$T=\{\mathrm{diag}(a,a^{-1})\}$ の $U$ 上の作用は $a/a^{-1}=a^2$ ⟹ 位数 $690/\gcd(2,690)=\mathbf{345}>6$ ⟹ **TWIST-6-ABS と矛盾**。∎

⟹ ★ **これが司令塔の言う「Sylow-characteristic 橋」**: **Sylow $p$ が唯一 ⟹ 特性 ⟹ 正規 ⟹ 両端 $G$-正規な 1 次元切片 ⟹ CHI-CARRY/TWIST-6-ABS が発火**。

### 2.2 ★★★ 同 erratum の**但し書き**が (F) を救う(逐語)

> ⚠ **$H_0=SL(2,691)$ には効かない**(そこでは Sylow 691 は**正規でない**)— **この区別が §1 で私が落とした種類の注意**。

**(F) の $H_0$ 成分は $\mathrm{SL}^\pm(2,691)$**(Borel 型ではない)。$691$ は $\lvert SL(2,691)\rvert=691\cdot690\cdot692$ を**ちょうど 1 回**割り(機械確認)、$PSL(2,691)$ は単純ゆえ **Sylow 691 は正規でない**。
$$\boxed{\ \Longrightarrow\ \textbf{Sylow-characteristic 橋は (F) に}\textbf{移植されない}\ \textbf{= PASS}\ }$$

★ **整合の確認**: 命題 **W691-NARROW**($H_0\in\{$巡回 $\supseteq C_{690}$, dicyclic $\supseteq C_{690}$, $SL(2,691)\}$)で **$SL$ 枝が生き残る**とされている。(F) は**まさにその生き残り枝の上に建っている** ✔

⚠ **ただし射程の限定**: 本判定は **RIBET-SECTION(Sylow 経由の 1 次元切片論法)**についてのみ。**TWIST-GCD-ABS / CHI-CARRY 自体は生きている**ので、$W$ の $\det$ 位数条件(C5)は**別途満たす必要がある**(札の C5 ✓ は $\det=\pm1$ による)。

---

## §3 位数・構造の検算(**機械確認済**)

| 量 | 値 | 確認 |
|---|---|---|
| $\lvert SL(2,691)\rvert$ | $691\cdot690\cdot692=329{,}938{,}680$ | ✔ 見立て §4.1 cert と一致 |
| $\lvert\mathrm{SL}^\pm(2,691)\rvert$ | $659{,}877{,}360$ | ✔ **$=\lvert H_2\rvert$**(cert 値と一致) |
| $\lvert H_F\rvert$ | $659877360\times6/2=\mathbf{1{,}979{,}632{,}080}$ | ✔ 札の $\approx2.0\times10^9$ |
| ⚠ **NAME-COLLIDE 警告** | ★ **$\lvert H_F\rvert=\lvert H_6\rvert$**($6\cdot\lvert SL\rvert$ も同値)— **位数は一致するが構造は別** | ★ **本検分で新規に摘出**。位数で $H_6$ と取り違えない |
| $H_F^{\rm ab}$ | $SL(2,691)$ perfect ⟹ $[H_F,H_F]\supseteq SL\times1$、$H_F/(SL\times1)\cong S_3$ ⟹ $H_F^{\rm ab}=C_2$ | ✔ 札の C1 ✓ |

---

## §4 ★★★ 観点 ③ — 前哨(**私の新規寄与: C2 が 1 検査に落ちる**)

### 4.1 braid 関係が $\det$ を強制する(**1 行**)

braid 対 $(a,b)$ が $H_F$ を生成するとする。$aba=bab$ に $\det\circ\mathrm{pr}_1$ を適用:
$$\det(a)^2\det(b)=\det(a)\det(b)^2\ \Longrightarrow\ \boxed{\det(a)=\det(b)}$$
$H_F\to S_3$ が全射で標準 $\pi$ と整合するには $a,b$ の $S_3$-成分が**互換**(sign $=-1$)⟹ fiber 条件より
$$\boxed{\ \det(a)=\det(b)=-1\ \textbf{が}\textbf{強制}\ }$$

### 4.2 ★★ Goursat の懸念は**消える**(本検分の中核)

一般に fiber 積 $A\times_C B$ の部分群 $\Gamma$ は、両射影が全射でも $\Gamma\subsetneq A\times_C B$(graph 型)になりうる。**しかし本件では起きない**:

- $A=\mathrm{SL}^\pm(2,691)$、$B=S_3$。
- $SL(2,691)$ は **perfect** ⟹ $A$ の可解商は $A/SL\cong C_2$ が**最大** ⟹ ★ **$A$ は $S_3$ に全射できない**。
- ⟹ $A$ と $B$ の**共通商は $1$ と $C_2$ のみ**。$C_2$ 共通商が $H_F$ の**定義そのもの**。
- ⟹ Goursat により、$H_F$ 内で両射影全射な部分群は **$H_F$ 自身**。

$$\boxed{\ \Longrightarrow\ \textbf{C2 の検査は}\textbf{「}\det=-1\ \textbf{の braid 対が }\mathrm{SL}^\pm(2,691)\ \textbf{を生成するか」だけでよい}\ }$$
($S_3$ 成分は互換 2 本なので $\langle s_1,s_2\rangle=S_3$ が自動 — 互換が相異なる限り。)

### 4.3 ★ 最初の機械前哨の仕様(**既走 cert の読み出し・秒**)

```
=== 前哨 P-WR-1' (retarget (F) の C2 判定) ===
根拠: retarget_F_audit_v1.md §4 / 発案札 P-WR-1
入力: search/certs/w691_gen23_witness_v1_20260812.json(既走・H_2 の目撃者)
      + 必要なら w691_gen23_braid_backconv_v1_20260812.json(逆変換 all_ok=true)

[1] 目撃者 braid 対 (a,b) の det を読む
    期待: det(a) = det(b)(§4.1 の braid 帰結・fail-closed 検査)
[2] ★ 判定: det(a) = det(b) = -1 か?
    YES  -> C2 は即 PASS(§4.2 の Goursat 解消により H_F 全体を生成)
            ⟹ (F) は段 1(H^2)へ進める
    NO(= +1) -> 目撃者を det=-1 の対へ取り替える有限掃きが要る
            ⟹ P-WR-1 が「新しい制約」として発火(札の予想どおり)
[3] 出力: cert (schema wr1prime/v1)。u/封印には触れない。
    ⚠ 判定語は司令塔。ここは boolean のみ。
```

★ **費用 = 既走 cert の 1 フィールド読み出し**(取り替えが要る場合のみ有限掃き)。⟹ **③ 線を動かす最初の一手として最小**。

---

## §5 観点 ④ — 四段設計のどこが変わるか

| 段 | $H_2/H_6$ 時代 | ★ (F) での変化 |
|---|---|---|
| **段 0**(分類) | $H_d$ で $S_3$ 商なし ⟹ **全滅** | ★ **通過**($H_F\twoheadrightarrow S_3$)。⟹ **段 0 が初めて開く** |
| **段 1**($H^2$) | $H_d$ 上の計算 | ⚠ **$H_F$ 上へ変更**。★ 但し **Sylow 縮約は再利用可**($H^2(H_F,W)\hookrightarrow H^2(\mathrm{Syl}_{691},W)$・札の「保存する部品」)。$S_3$ 因子は位数 6 で $p=691$ と互いに素 ⟹ **$H^2$ に寄与しない**(⟹ 実質 $\mathrm{SL}^\pm$ 上の計算に落ちる) |
| **段 2**(braid lift) | $H_d$ の braid 対 | ★ **§4 の $\det=-1$ 制約が新規**(唯一の実質的変更) |
| **段 3/4**(算術 marking) | — | ⚠ **変わらない**(依然この設計の最難部)。$p=23$ control(札 §2)が唯一の入口 |

$$\boxed{\ \textbf{⟹ 実質的に変わるのは }\textbf{段 0(開く)と段 2(}\det\ \textbf{制約)}\ \textbf{。段 1 は縮約で再利用でき、段 4 は不変}\ }$$

---

## §6 ⚠ 反証側からの留保(**GO に付ける条件**)

| # | 留保 | 重さ |
|---|---|---|
| **R-1** | ★ **③ 線が ① 線(972 屋根)の $\lvert Q_A\rvert>6$ を供給する**という司令塔の戦略観は**魅力的だが未証明** — (F) の窓が実現しても、その**算術像**が $L_9\cap L_{S4}$ に非円分成分を与える保証はない(**型 vs 実像**)。⟹ **段 4 の marking が閉じるまで供給源とは言えない** | ★★ 大 |
| **R-2** | 札の候補族は **EXHAUST を満たさない**(札自身が「$\dim\ge3$ の一般層・非分裂 $S_3$-拡大型は OPEN と登録」)⟹ **(F) が死んでも ③ 線は死なない**が、**(F) が生きても族の網羅は主張できない** | 中 |
| **R-3** | $H_\Delta$($p=23$ 陽性 control)の**位数・ab が未計算**(札の自認)⟹ control の前件が未確認 | 小(1 行) |
| **R-4** | ⚠ **$\lvert H_F\rvert=\lvert H_6\rvert$**(§3)— **位数だけで同定しない**(NAME-COLLIDE) | 小(本ノートで警告済) |

---

## §7 【付】修理見積り 2 本(裁定 943 の宿題・**簡潔形**)

| 修理 | Sol 指定 | ★ 私の見積り |
|---|---|---|
| **TOWER-α-INV**(M119-6) | 3 路: ① T63-P1 を fixed window $H_{2,1,0}$ の主張として書き直す ② 接続は同窓上の MATCH-one/BRIDGE-one+(5′) ③ C1′-any を一行ずつ写して適用 | ★ **① が最安**(**紙のみ・小**)。「C1′ 非依存を主張しない」形に書き直すだけで、**新しい数学が要らない**。⟹ **① を推薦**。③ は C1′-any の定理文の入手が要る(中)。② は (5′) の窓一致確認が要る(中) |
| **K9-UNRAM**(B119-1) | 2 択: ① $\psi_9(f_g)_{\rm trans}=\Lambda(f_g^{(3)})$ の明示比較式 ② $p\ne3$ ごとの based inertia 直接計算($p=2$ 別段) | ⚠ **どちらも重**。★ **② の方が構造が見える**(局所ごとに閉じるので部分的成功が記録できる)が、**$p=2$ の別段**が読めない。★ **① は Ihara power series / Soulé character の explicit evaluation が要り、正典外の入力に依存**。⟹ ★ **推薦 = ② を $p$ 奇素数に限って先に走らせ、$p=2$ を切り離す**(部分的前進が台帳に残る形) |

---

## §8 帰属・申告

- **(F) の構成と C0–C6 カスケード・$p=23$ control 設計** = **発案係**(裁定 872)。
- **RIBET-SECTION の機構と $SL$ 但し書き** = `xd2_bridge_2b_v1_erratum_a.md`(既存)。$GL(2,7)$ 反例 = falsifier。
- **委嘱・戦略観**(③ は ① の供給源)= 研究者 → 司令塔(裁定 950)。
- **本検分の新規部分**: ① **EXT-NOWIN 回避の型の明示**(「$W$ が $p$-群でない」からではない)② **RIBET-SECTION 非移植の逐語根拠の特定**(erratum の $SL$ 但し書き)③ ★ **braid 関係から $\det(a)=\det(b)=-1$ の強制**(1 行)④ ★★ **Goursat の懸念の解消**($SL$ perfect ⟹ 共通商 $\le C_2$ ⟹ 両射影全射なら $H_F$ 全体)⟹ **C2 が 1 検査に落ちる** ⑤ **$\lvert H_F\rvert=\lvert H_6\rvert$ の NAME-COLLIDE 警告** ⑥ **段 1 が $S_3$ 因子を落として $\mathrm{SL}^\pm$ 上へ縮約されること** ⑦ **前哨 P-WR-1′ の仕様**(既走 cert 読み出し)⑧ **留保 R-1**(③ が ① の供給源という戦略観は型 vs 実像で未証明)。
- **検算**: 位数・perfect 性・braid det の帰結(python 単系統)⟹ **cross-checked ではない**。
- **未実施**: 段 1 の $H^2$ 計算・段 4・**Sol 未監査**。⟹ **verified ではない**。
