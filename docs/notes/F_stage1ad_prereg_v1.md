# 段 1′(Ad) prereg カード v1(裁定 1007)

作成: 数学者(Opus 5)/ 2026-08-12 / 発注 = 司令塔裁定 1007
前提 = `F_card_v2_1_diff.md`(和則・(Ad-c) 削除・schema union)+ `fals_F_stage1_audit_v1.md`(逐語・実測 4 点)
⚠ 数値出力なし($u$ 非接触・$c$ 未評価)。**格付け: candidate**(Sol 未監査)。
⚠ **NAME-COLLIDE 行**: 本カードの $H_F=SL^\pm(2,691)\times_{C_2}S_3$ は `pair_h2_design_draft_v1.md` §2 の $\bar G$ と**同一対象**。$|H_F|=|H_6|$(位数一致・構造別)。**P-PH2-4 は再掲であり本カードの新規ではない**。

---

## §0 ⚠⚠ 起草中の発見 — **予言が紙で導出されました**(カードの性格が変わります)

司令塔の発注は「$p=691$ 実装可能性の設計(cohomolo 次数 2016 溢れの回避 = 安定元法/pair_h2 M-3 の Borel トーラス文字計算路)」でした。**その路を実際に敷いたところ、$p$ に依存しない閉じた計算になり、予言が導出できてしまいました。**

$$\boxed{\ \dim H^2(H_F,\mathfrak{sl}_2)=1,\qquad \dim H^2(H_F,\mathfrak{sl}_2\otimes\det)=0\qquad\textbf{— 紙で確定}\ }$$

⟹ ★ **$p=691$ の実装可能性問題は「解決」ではなく「消滅」します**(群計算が一切要らない)。
⟹ ⚠ **段 1 と同じく、段 1′ も測定不発火になります。** ⟹ **カードは「1 bit 測定」から「紙の決着 + 較正」へ格下げ**(教訓 F-1 の 2 度目の適用 — 今度は**設計中に**捕まえました)。
⟹ ★ ただし **prereg としての価値は残ります**: 導出が誤っている可能性があり、**較正スイートがその検査になる**(§4)。

---

## §1 ★★★ $p=691$ 実装可能性の設計 = 安定元法(pair_h2 M-3 の実体化)

### 1.1 TI Sylow ⟹ 安定元が $N_G(P)$-不変に潰れる
$SL(2,p)$ の Sylow-$p$ 部分群 $P$(単冪上三角 $\cong C_p$)は **TI**(相異なる Borel の単冪根基は自明交叉)、$N_G(P)=B=P\rtimes T$、$T=\{d(\lambda)=\mathrm{diag}(\lambda,\lambda^{-1})\}\cong C_{p-1}$。
Cartan–Eilenberg/Swan の安定元定理は TI の場合に
$$\boxed{\ H^n\bigl(SL(2,p),M\bigr)\;\cong\;H^n(C_p,M)^{T}\ }\qquad(M\ \text{は}\ \mathbf F_p\text{-加群ゆえ全体が }p\text{-torsion})$$
⟹ ★ **位数 $3.3\times10^8$ の群に触らない。$C_p$ 上の 1 次元空間に $T$ の指標が乗るかを見るだけ。**

### 1.2 指標の計算(機械確認済)
$d(\lambda)u(a)d(\lambda)^{-1}=u(\lambda^2a)$ ⟹ **$T$ は $P$ に $\lambda^2$ 倍で作用**。
$H^*(C_p,\mathbf F_p)=\Lambda(x)\otimes\mathbf F_p[y]$、$x\in H^1=\mathrm{Hom}(P,\mathbf F_p)$ は $P$ の**双対** ⟹ 重み $\lambda^{-2}$、$y=\beta(x)$ も $\lambda^{-2}$。
$N\equiv0$(既確認)⟹ $H^2(C_p,M)\cong M^P\cdot y$。

| $M$ | $M^P$ | $T$-重み($M^P$) | $H^2$ の重み | $T$-不変 |
|---|---|---|---|---|
| $\mathfrak{sl}_2$ | $\langle e\rangle$(1 次元) | $\lambda^{2}$ | $\lambda^{2}\cdot\lambda^{-2}=\lambda^0$ | ★ **自明 ⟹ 1 次元** |
| $W$(自然加群) | $\langle v_1\rangle$(1 次元) | $\lambda^{1}$ | $\lambda^{1}\cdot\lambda^{-2}=\lambda^{-1}$ | 非自明 ⟹ **0** |

$$\boxed{\ \dim H^2(SL(2,p),\mathfrak{sl}_2)=1,\quad \dim H^2(SL(2,p),W)=0\qquad(p>3\ \textbf{・}p\ \textbf{に依存しない})\ }$$
★ **falsifier 実測($p=5,7,11,23$)と完全一致** ⟹ **方法の較正 PASS**(逐語 §D の表が独立検証になっています)。

### 1.3 ★ $S_3$ の作用 = 1 bit の決着
$H_F/SL(2,691)\cong S_3$。3-cycle の持ち上げは $\det=+1$ ⟹ $SL$ 内 ⟹ **内部自己同型 ⟹ 自明作用**。
⟹ 作用は $S_3\to C_2=\mathrm{sgn}$ を経由 ⟹ **互換の持ち上げ 1 個で決まる**(異なる持ち上げは $SL$ 倍 = 内部 ⟹ 同じ作用)。

$A=\mathrm{diag}(1,-1)$($\det A=-1$ ✔・$A^2=I$ ✔)を取ると(機械確認):
- $A\,u(a)\,A^{-1}=u(-a)$ ⟹ **$P$ に $-1$ 倍**
- $\mathrm{Ad}(A)e=-e$ ⟹ **$M^P$ に $-1$ 倍**
- $P$ に $-1$ ⟹ $\mathrm{Hom}(P,\mathbf F_p)$ にも $-1$ ⟹ $x$ に $-1$ ⟹ $y=\beta(x)$ に $-1$

$$\Longrightarrow\ A\ \text{の}\ H^2\ \text{への作用}=(-1)\cdot(-1)=+1\quad\textbf{= 自明}$$

$$\boxed{\ H^2(H_F,\mathfrak{sl}_2)=(\text{1 次元})^{S_3}=\mathbf 1,\qquad H^2(H_F,\mathfrak{sl}_2\otimes\det)=(\text{sign 成分})=\mathbf 0\ }$$

⟹ ★★ **$i_0=0$ は 4 点の外挿ではなく導出**です。和則(和 $=1$)とも整合 ✔

---

## §2 事前登録(prereg)

| 欄 | 内容 |
|---|---|
| **対象** | $H_F=SL^\pm(2,691)\times_{C_2}S_3$、係数 $\mathbf F_{691}$、加群 $\mathrm{Ad}=\mathfrak{sl}_2$、捻り $\det^i$($i\in\{0,1\}$) |
| **★ 予言 1** | $\dim H^2(H_F,\mathfrak{sl}_2)=\mathbf 1$($i=0$) |
| **★ 予言 2** | $\dim H^2(H_F,\mathfrak{sl}_2\otimes\det)=\mathbf 0$($i=1$) |
| **★ 予言 3(和則 assert)** | $\dim H^2(H_F,M)+\dim H^2(H_F,M{\otimes}\det)=\dim H^2(SL,M)\le1$ ⟹ **和 $=1$** |
| **★ 予言 4** | $\dim H^2(H_F,W)=\dim H^2(H_F,W{\otimes}\det)=0$(段 1・補題 CENT-SCAL) |
| **導出の格** | ★ **紙**(§1)。★ **測定は確認であって発見ではない** |
| **凍結時刻** | 本カード commit 時(実装発火前) |
| **EXHAUST** | 捻りは 2 本で尽きる。根拠 2 段: (i) $H_F^{ab}=C_2$ かつ 691 奇 ⟹ $\mathrm{Hom}(H_F,\mathbf F_{691}^\times)=\{1,\det\}$ (ii) $SL$ を含む作用群の 2 次元 $\mathbf F_{691}$-既約は自然加群のみ(素体上 Frobenius 捻り無し・$W^*\cong W\otimes\det$) |
| **事前登録項目**(UNKNOWN 枝ではない) | $S_3$ 作用の持ち上げ・向き・$\mathfrak{sl}_2$ の基底($e,h,f$)・$\det$ の $\mathbf F_{691}^\times$ への埋め込み・$T$ の取り方(分裂トーラス) |
| **⚠ R-1 留保** | **維持**。③→① 非円分供給は未証明 ⟹ 予言 1 が当たっても ① には届かない |
| **⚠ 非結論** | いずれの結果でも **「窓資格」は結論しない**(段 2/3/4 が残る) |

---

## §3 判定枝

| 枝 | 条件 | 帰結 |
|---|---|---|
| **(Ad-b)** ★ 予言どおり | $(1,0)$ | ★ **段 2 入口が実在**($i=0$ の容器)⟹ 段 2(拡大の構成と非分裂性)へ。⚠ 窓資格は結論しない |
| **(Ad-a)** | $(0,0)$ | ✘ $\mathrm{Ad}$ 層にも容器なし ⟹ ③ 線を閉じる。⚠ **§1 の導出と矛盾** ⟹ STOP 相当(下記) |
| **(Ad-b′)** | $(0,1)$ | 和則は満たすが $i_0$ が予言と逆 ⟹ ★ **§1.3 の符号計算を疑え**。容器はあるので段 2 へ進んでよいが、**導出の誤りを先に特定**すること |
| ~~(Ad-c)~~ | $(1,1)$ | ★ **削除**(和則により不可能) |
| **STOP** | 和 $\ge2$ / $(1,1)$ / $(0,0)$ | ⚠ 理論と矛盾 ⟹ 即停止(群/加群/器具/安定元法の前件を疑う) |

---

## §4 較正スイート(falsifier 実測 4 点を較正資産として使用)

```
[cal-1] (C_691, W)                       予言 dim H^2 = 1     陽性対照(Sylow 層)
[cal-2] (H_F, W), (H_F, W⊗det)           予言 0, 0            段 1 本題(紙で決着済)
[cal-3] (H_F, sl_2), (H_F, sl_2⊗det)     予言 1, 0(和 = 1)   ★ 本カードの本題
[cal-4] p=23 リハーサル(全 3 本)          予言 0/0, 1/0        ★ falsifier 実測済(逐語 §D)
★ [cal-5] 新設: 安定元法の *独立実装* — H^n(C_p,M)^T を直接計算し、
          cohomolo の値(p=5,7,11,23)と突合。⟹ ★ 二系統(§5)
不変量 assert: dim H^2(H_F,M) + dim H^2(H_F,M⊗det) <= dim H^2(SL,M) <= 1
判定は 0/1 ではなく *予言との一致*。1 本でも外れたら UNKNOWN + STOP(MISS ではない)
```
★ **cal-1〜4 は falsifier 逐語の番号をそのまま踏襲**(番号の食い違いは v2.1 D-3 で解消済)。

---

## §5 二系統(§C-6 の充足)

| 系統 | 内容 |
|---|---|
| **系統 A** | cohomolo(GAP)による直接計算。⚠ 次数選択が生死を分ける(逐語 §B-2: 次数 2016 で溢れ・次数 51 で 0.1 秒) |
| **★ 系統 B** | **安定元法**($H^n(C_p,M)^T$ の線形代数)。★ **$p=691$ でも秒**(群を構成しない)⟹ **本番値はこちらで出す** |
⟹ ★ 一致すれば **cross-checked**。⚠ **verified ではない**(Lean 予約)。単系統なら **candidate/single-run** 止まり。

---

## §6 cert schema `F_stage1_ad/v1`

```
module              : "Ad" | "W"                      ★ 型境界
twist_i             : 0 | 1
dim_H2              : 非負整数                         ★ 「0 or 1」型で縛らない
bound_violated      : bool                             ★ (u1) の「2 が出た」を記録できる形
sum_rule_value      : dim(i=0) + dim(i=1)              ★ 本当の fail-closed 不変量
i0_predicted        : 0                                ★ prereg
i0_observed         : 0 | 1 | null
r_value             : 690 (W 層) | 345 (Ad 層)         ★「満額と容器は両立しない」の指紋
central_lemma_fires : bool                             ★ W なら true / Ad なら false
lhs_degenerate      : bool
method              : "stable_elements" | "cohomolo" | "paper_lemma"
group_fingerprint   : {|H_F|, |H_F^ab|, |Z(H_F)|, 合成因子, 生成系ハッシュ}
                      ★ |H_F| = |H_6| の NAME-COLLIDE 対策 — 位数だけでは同定にならない
s3_action_variant   : 捻りごと 2 欄(1 欄では必ずどちらかが誤記される)
positive_control    : {cal-1, cal-3} の PASS/FAIL      ★ 裁定 961
calib               : {cal-1..cal-5} の PASS/FAIL
r1_reservation      : "unproven(型 vs 実像・段 4 未閉)" ★ 必須欄(下流テンプレが必ず引く)
name_collide_note   : "pair_h2_design_draft_v1.md の Ḡ と同一対象・P-PH2-4 は再掲"
tool_version, input_hash, wall_clock_ms, cap_ms
u_touched           : false
```

---

## §7 撤退条件

| 事象 | 行き先 |
|---|---|
| 系統 A(cohomolo)が壁時計 cap 超過 or `-o 2g` 超過 | ★ **系統 B(安定元法)へ切替**(本番値は元々こちら) |
| 系統 B が §1 と異なる値 | ⚠ **即停止** — 安定元定理の前件(TI・$N_G(P)=B$)を再検査 |
| cal-1〜5 のいずれかが外れる | **UNKNOWN + STOP**(MISS ではない) |
| $p=23$ リハで逐語 §D の表と不一致 | ⚠ **器具の較正が壊れている** ⟹ 実装係へ差し戻し |
| **cap 目安** | 系統 A: 壁時計 600 秒・`-o 2g`。系統 B: 60 秒(線形代数のみ) |

---

## §8 GAP・記帳

- **【F-GAP-7】(小)** 安定元定理の前件($SL(2,p)$ の Sylow-$p$ が TI・$N_G(P)=B$)は標準ですが、**私は正典外の知識から使っています** ⟹ 【文献要請】には至らないと判断(教科書事実)。⚠ ただし **cal-5 で数値的に裏取り**する設計にしました。
- **【F-GAP-8】(小)** $y=\beta(x)$ の $T$-重みが $x$ と同じ($\beta$ が $T$-同変)は標準。§1.2 の帰結はこれに依存。
- **★ 教訓 F-1 の 2 度目の適用**: 「計器を設計する前に紙で決まらないか検査せよ」を、今度は**設計中に自分で発火させました**。⟹ 段 1(裁定 983・事後に falsifier が指摘)→ 段 1′(設計中に自己捕捉)で**改善**しています。
- **★ 上申**: 予言が紙で出た以上、**falsifier 前哨 → 凍結 → 実装 の標準列を「凍結 → 較正のみ実装(系統 B・秒)」へ短縮できます**。実装予算を「答えの分かっている測定」に使わない、という falsifier の P-1 の趣旨そのものです。⟹ **司令塔裁定を仰ぎます**。
- **申告**: GAP 走行ゼロ(記号計算のみ)・$u$ 非接触・$c$ 未評価・**Sol 未監査**・**verified ではない**(candidate 格)。
