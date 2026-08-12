# 【枝 P 実装指示書】+【$r$ 測定仕様】

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 977(Sol 認可済 2 本)
**格**: candidate(設計・**Sol 未監査**)。走行ゼロ。⚠ **$u$・$\operatorname{ord}$ 未計算**。
**前提**: `r13_model_design_v1.md`(枝設計)/ `r1_branch_retraction_v1.md`(枝 Q 撤回)/ `r3_cards_audit_v1.md`(TRIAD-972)

---

# 第 I 部 — 枝 P 実装指示書(R-1/R-2 のモデル構成)

## I.1 確定データ(R-0 / R-0b)

| 量 | 値 | 出所 |
|---|---|---|
| $D=\deg\lambda_9$ | **18** | R-0 cert |
| passport | $0$: $[[18,1]]$ / $1$: $[[1,2],[2,8]]$ / $\infty$: $[[18,1]]$ | R-0 cert |
| $g(W_9)$ | **4** | R-0(RH: $-36+42=6$) |
| $\mathrm{Deck}(\lambda_9)$ | **自明**($H_9^{\rm fun}$ 自己正規化) | R-0b cert |
| $\lambda_9$ は Galois か | ✘ **非 Galois**(**LAM9-NONGAL**) | 本工房・紙 |
| $\mathrm{div}(\lambda_9)$ | ★ $18\bigl(P_0-P_\infty\bigr)$($0,\infty$ が各 1 点で全分岐) | passport |
| $\dim L(18P_\infty)$ | ★ **15**($=18-g+1$・$18\ge2g-1=7$ で RR)| 機械確認 |

## I.2 ★★ 先に確認すべき 1 点(**重い R-1 を回避できる可能性**)

wac_v1 は **命題 U-LOC** により「測定は $C$ 上の**局所展開のみに還元**($u_0=-c^{-1}$・**$W$ の方程式は不要**)」を達成していた(litgate 覚書 §0 逐語)。

$$\boxed{\ \textbf{★ }K^{(9)}\ \textbf{側に }U\text{-LOC}\ \textbf{類似の還元があれば、}W_9\ \textbf{の完全なモデル構成は}\textbf{不要}\ }$$

⟹ ★ **指示書の第 0 工程を「U-LOC 類似の探索」にする**。これが当たれば **R-1 の大半が消える**。
⚠ U-LOC は **S4 窓の命題**(型境界 — W-48)。$K^{(9)}$ 側での成立は**未確認**。

## I.3 モデル構成の設計(**枝 P**・U-LOC 類似が無い場合)

### I.3.1 平面モデルの形

$W_9$ を $\mathbf P^1_t$ 上の被覆として
$$F(t,w)=0,\qquad \deg_w F=18,\qquad t=\lambda_9,\qquad F\in F_9[t,w],\ F_9=\mathbf Q(\zeta_{36})$$
と書く。**分岐条件**が係数を強く縛る:

| 素点 | 条件 | $F$ への帰結 |
|---|---|---|
| $t=0$ | 全分岐(1 点・$e=18$) | ★ **座標を $w$ の平行移動で正規化**して $F(0,w)=c_0\,w^{18}$ |
| $t=\infty$ | 全分岐(1 点・$e=18$) | ★ $w=\infty$ を $P_\infty$ に取る ⟹ $\deg_t$ の主部が単項 |
| $t=1$ | $[[1,2],[2,8]]$ | $F(1,w)=c_1\,(w-\alpha_1)(w-\alpha_2)\prod_{j=1}^{8}(w-\beta_j)^2$(**単根 2・二重根 8**) |

⟹ **未定係数法 + Gröbner**($t=1$ の重根条件は判別式の消滅で書ける)。

### I.3.2 ★ 函数階段による補助(**次元の見張り**)

$P_\infty$ を基点とする $L(kP_\infty)$ の次元は、$k\ge7$ で $k-3$、$k<7$ は gap 列による。
$$\lambda_9\in L(18P_\infty),\qquad \dim L(18P_\infty)=15$$
⟹ **生成元の探索範囲の上限**として使う(未定係数の本数の sanity check)。
★ **$18(P_0-P_\infty)\sim0$**($\mathrm{div}(\lambda_9)$ から)⟹ $P_0-P_\infty$ は $\mathrm{Jac}(W_9)$ の **torsion 点で位数 $\mid18$** ⟹ **モデルの検算に使える**。

### I.3.3 W-d(主係数抽出)の**終結式一般形**

超楕円を仮定しない形(`r13_model_design_v1.md` §2.4 の具体化):
$$N_\tau(w):=\mathrm{Res}_{\,?}\bigl(F(t,w),\ t-\tau\bigr)\ \text{ではなく}\ \boxed{\ N_\tau(w):=F(\tau,w)\ }$$
★ **$F$ が既に $t$ について書かれているので終結式は不要** — $t=\tau$ を代入するだけ。主係数は $\mathrm{lc}_w F(\tau,w)$。
$$\lambda_9=u_9\,s_9^{18}\bigl(1+O(s_9)\bigr)\ \Longrightarrow\ u_9=\lim_{s_9\to0}\lambda_9\,s_9^{-18}$$
は $P_0$ での **Puiseux 展開**(厳密級数演算)で読む。

## I.4 実装係への指示書

```
=== 作業指示: 枝 P モデル構成(R-1/R-2)===
根拠: 司令塔裁定 977 / 設計 = docs/notes/branchP_and_r_spec_v1.md 第 I 部
★ 停止線: R-2 まで。R-3(主係数 u_9 の抽出)は prereg 凍結済(裁定 977)
          だが、モデルが立つまで実行できない。R-3 に入る前に一度報告。
⚠ 禁止: 他窓(S4/wac)の genus・次数・商・モデルを流用すること(W-48)
⚠ 禁止: 群位数から分岐を導くこと(W-51)

[P0] ★ 最優先(軽い)— U-LOC 類似の探索
  wac_v1 の命題 U-LOC「測定は C 上の局所展開のみに還元・W の方程式は不要」
  (litgate_positive_genus_belyi_v1.md §0)の K^(9) 側類似が存在するか、
  既存文書を走査して *設計可否の報告* を出す。
  ★ 当たれば [P1][P2] の大半が不要になる。
  ⚠ S4 窓の命題をそのまま適用しないこと(型境界・W-48)。
  出力: 報告(cert 不要)。所在の有無と、あれば命題番号。

[P1] 平面モデル F(t,w) = 0 の構成
  (a) deg_w F = 18。係数体 F_9 = Q(zeta_36)(★ 厳密・浮動小数点禁止)
  (b) 正規化: t=0 の全分岐点を w=0 に、t=∞ の全分岐点を w=∞ に取る
      => F(0,w) = c_0 w^18
  (c) t=1 の条件: F(1,w) が単根 2 個 + 二重根 8 個
      (判別式の消滅条件を Gröbner へ)
  (d) 未定係数法 + Gröbner。★ 設計流用元 =
      search/probe/wac_v1/u_meas_caseb_groebner*.py 系
  (e) 検算: ① exact_verification_all_zero 相当 ② 複数素点での剰余一致
      ③ ★ 18(P_0 - P_inf) ~ 0(Jac の torsion)の確認
  出力: cert (schema r13-r1p/v1)

[P2] cusp と有理 uniformizer(R-2)
  (a) lambda_9^{-1}(0) = {P_0} を機械確認(fail-closed)
  (b) P_0 が F_9-有理点か確認 → 非有理なら即停止・UNKNOWN(u3) 報告
  (c) F_9-有理な uniformizer s_9 を取る
  (d) ★ 2 通りの s_9 を取り両方 cert に記録
      (= prereg v3 の T63-UNIF-INV 検査用・[5] s9_variants 欄)
  出力: cert (schema r13-r2p/v1)

[共通の記録要件]
  u_touched : false      ★ [P0]-[P2] では必ず false
  d_no_interpretation : "machine values only; verdict は司令塔"
  window_assert / M_assert(M=18)/ F_assert(F_9 = Q(zeta_36))
  ★ dim L(18 P_inf) = 15 との整合(未定係数の本数の sanity check)
=== END ===
```

### I.5 fail-closed 条項(`r13_model_design_v1.md` §4 を継承・追加 2 件)

| # | 条件 | 動作 |
|---|---|---|
| F-1〜F-6 | 前設計のまま | — |
| ★ F-7 | $\dim L(18P_\infty)\ne15$ と整合しない | **即停止**($g=4$ or $D=18$ の再検査) |
| ★ F-8 | $18(P_0-P_\infty)\not\sim0$ | **即停止**(passport と矛盾) |

---

# 第 II 部 — $r$ 測定仕様

## II.1 ★★ 型境界(**最重要・法の統一**)

$$r:=\bigl\lvert\langle[a]\rangle\cap\langle[b]\rangle\bigr\rvert$$

| 記号 | 定義 | 法 | 類群 | 出所 |
|---|---|---|---|---|
| ★ **$a$** | $L_{9,\mathrm{Aff}}=\mathbf Q(\zeta_9,\sqrt[9]{a})$ の Kummer radicand | ★ **9** | $\mathbf Q^\times/(\mathbf Q^\times)^9$ | K9-KUMMER(R1 第一波) |
| ★ **$b$** | $L_{S4}=\mathbf Q(\zeta_9,\sqrt[9]{b})$ の Kummer radicand | ★ **9** | 同上 | R3 札 1(S4-COORD) |
| ⚠ **$a_9$** | $[u_9^{-1}]_{18}$ | ⚠ **18** | $F_9^\times/F_9^{\times18}$($F_9=\mathbf Q(\zeta_{36})$) | E1 §5.1 |

$$\boxed{\ \textbf{⚠ }a\ \textbf{と }a_9\ \textbf{は}\textbf{別の類群の元}\ \textbf{(法 9 vs 18・体 }\mathbf Q\ \textbf{vs }\mathbf Q(\zeta_{36})\textbf{)}\ }$$
★ 位数はどちらも $\{1,3,9\}$ に落ちるが、**類そのものは別**。⟹ **$r$ は法 9・$\mathbf Q$ 側で統一する**(RES-INJ-9 が $\mathbf Q\hookrightarrow K$ の単射性を保証)。

### II.1.1 ★ $a_9$(法 18)から $a$(法 9)へ落とす規約 —【**r-GAP-1**】

$\operatorname{ord}(a_9)$(R-3/R-4 の出力)から $[a]\in\mathbf Q^\times/(\mathbf Q^\times)^9$ を取り出す規約は**未確定**。
⚠ **位数だけでは $r$ は決まらない** — $r$ は**類の交わり**であって位数の関数ではない。
$$\boxed{\ \Longrightarrow\ r\ \textbf{測定には}\textbf{位数ではなく類そのもの}\ \textbf{が要る}\ }$$
★ **これが本仕様の最大の前件**。⟹ **R-3 の出力仕様に「$[a]$ の類そのもの(素因子指数ベクトル)」を含めること**を要求する。

## II.2 資産と規約(委嘱の「どの資産からどの規約で取るか」)

| 側 | 資産 | 規約 |
|---|---|---|
| **$a$($K^{(9)}$)** | ★ **R-3 の出力**($u_9$ の主係数)⟹ $a=$(K9-KUMMER の Kummer 類) | 法 9・$\mathbf Q^\times/(\mathbf Q^\times)^9$・素因子指数を $\bmod\ 9$ で記録 |
| **$b$($N_{S4}$)** | ★ **S4-RECON の出力**($u_0$)⟹ $b$ | 同上。⚠ **前件 P5($u_0=u_{S4}$)を継承**(`s4_recon_device_v1.md`)|
| **正規化** | 両側とも **$-1=(-1)^9$ ゆえ符号は自明**・$\mathbf Q^\times/(\mathbf Q^\times)^9\cong\bigoplus_p\mathbf Z/9$(素因子ごとの指数) | ★ **同一の基底**(素数の集合)で表す |

★ **交わりの計算**: $\langle[a]\rangle,\langle[b]\rangle$ は $\bigoplus_p\mathbf Z/9$ の巡回部分群 ⟹ **$r$ は初等的**(実装係の雛形 `r_intersection_template_v1.py`・canary 4/4 で確認済)。

## II.3 $r$ 測定の prereg カード(**様式 v3 準拠**・QUAR 8 要件を流用)

```
=== PREREG CARD: r RECEIPT (TRIAD-972) ===
card_id  : prereg-r-receipt/v1
authorisation : Sol 返書 120 P3(認可済)+ 司令塔裁定 977

[0] 前件
  A1 : R-3 が [a] を *類として* 出力していること(位数だけでは不可)★ r-GAP-1
  A2 : S4-RECON が [b] を同上で出力していること(前件 P5 = u_0 = u_S4 を継承)
  A3 : 両側の正規化が同一(法 9・Q^x/(Q^x)^9・素因子指数の基底)
  A4 : TRIAD-972 の前提(i ∉ L_S4〔次数互素〕・RES-INJ-9・R3-GAP-4/5)
  ⟹ 本 receipt は A1-A4 の下での conditional receipt

[1] 測定対象
  r := |<[a]> cap <[b]>|  in  Q^x/(Q^x)^9
  ⚠ NOT : ord(a_9)(法 18・別類群)から直接は取れない

[2] 判定(★ 三値 UNKNOWN 維持)
  r ∈ {1,3,9}(r | gcd(d_9,d_S4) ゆえ)
  ★ 972 への含意: |X\A| = 972 - 12 d_9 d_S4 / r
     非発火は (d_9,d_S4,r) = (9,9,1) ただ一つ
     ★ d_9 = d_S4 = 9 でも r >= 3 なら発火
  UNKNOWN(MISS に優先):
    (r1) A1/A2 が満たされない(類が出ていない・位数のみ)
    (r2) r ∤ gcd(d_9,d_S4) ⟹ 規約不一致 ⟹ 座標系の再検査
    (r3) 両側の素因子基底が食い違う ⟹ 正規化の再検査

[3] 同時に判定される命題
  TRIAD-972 の縮約式 / COMPOSITUM-rho(前件 2/3 = R3-GAP-4/5 は閉)
  ⚠ d_9, d_S4 が UNKNOWN のままなら |X\A| は決まらない
     ⟹ r 単独では 972 は決着しない(★ 三値が揃って初めて決まる)

[4] ★ QUAR(S4 receipt 様式 P6 の 8 要件を流用)
  発火判定(|X\A| > 0)が出た場合:
   (Q1) 即時隔離・流通禁止  (Q2) 前件 A1-A4 の再検査
   (Q3) falsifier 独立判読  (Q4) Sol 監査請求
   (Q5) 研究者報告          (Q6) 三値(d_9,d_S4,r)の出所を各々明記
   (Q7) 型境界検問(法 9/18・窓 K^(9)/N_S4 の取り違えがないか)
   (Q8) 「反例を得た」と書かない(|X\A|>0 は *非算術 shadow の存在* であって
        具体的 witness の構成ではない)
  ★ (Q8) が S4 receipt との差: あちらは d_S4<9 が直接反例だが、
    こちらは *個数* が出るだけで witness は別途構成が要る

[5] 禁止事項
  - 位数から類を推測しない(★ r-GAP-1)
  - a_9(法 18)を a(法 9)として使わない
  - 三値のうち 1 つでも UNKNOWN なら |X\A| の値を書かない
  - 格は cross-checked 止まり・verified は Lean に予約

[6] 出力
  r_value / a_class / b_class(素因子指数ベクトル・法 9)
  prerequisites_status : A1-A4(成立を主張せず状態を転記)
  quar_triggered : (|X\A| > 0 が導けた場合)
  d_no_interpretation : "machine value only; verdict は司令塔"
=== END ===
```

## II.4 ★ 実装係への注記

既製の `r_intersection_template_v1.py`(canary 4/4)は**交わりの計算器**として妥当(**$(3,9)\to9$・$(3,2\cdot3^6)\to1$** の canary は $\bigoplus_p\mathbf Z/9$ の巡回部分群の交わりとして正しい)。
⚠ ただし **入力の $[a],[b]$ が揃うのは R-3 と S4-RECON の後**。⟹ **仕様凍結 → 入力待ち → 計算**の順。

---

# 帰属・申告

- **U-LOC** = wac_v1(litgate 覚書 §0)。**$r$ 計算器雛形** = 実装係。**認可** = Sol 返書 120 P3。**委嘱** = 司令塔(裁定 977)。
- **本ノートの新規部分**: ① ★ **[P0](U-LOC 類似の探索)を第 0 工程に置く設計**(重い R-1 を回避できる可能性)② **平面モデル $F(t,w)$ の分岐条件による正規化**($F(0,w)=c_0w^{18}$)③ ★ **終結式は不要**($F$ が $t$ について書かれていれば代入のみ)④ **fail-closed F-7/F-8**($\dim L=15$・$18(P_0-P_\infty)\sim0$)⑤ ★★ **$a$(法 9)と $a_9$(法 18)が別類群であることの摘出**と【**r-GAP-1**】(**位数ではなく類そのものが要る**)⑥ **$r$ prereg カード**(三値 UNKNOWN・QUAR 8 要件・★ **(Q8) = $\lvert X\setminus A\rvert>0$ は witness の構成ではない**)。
- **申告**: ⚠ $u$・$\operatorname{ord}$・$r$ いずれも未計算。走行ゼロ。**Sol 未監査**。⟹ **verified ではない**。


---

# 【v1.1 追記】$r$ prereg カード v2 — falsifier 前哨の 3 修正(裁定 981)

**日付**: 2026-08-12 / **委嘱**: 裁定 981(B-1 blocker + should-1 + should-2)/ **方式**: additive addendum(第 I 部・第 II 部とも不改変)

> ## ★ B-1 の受諾 — **原則 3 の回帰**
> 「同時に判定される命題を**全部**先に列挙する」を、**P8 カードでは守ったのに $r$ カードで落とした**。⟹ **同じ原則を二度目に破った**(P8 v2 の B-1 と同型)。falsifier の指摘は正しい。

## A. $r$ prereg カード **v2**(★ これが正本・第 II 部 §II.3 の v1 を supersede)

**v1 からの差分のみ記す**。

```
=== PREREG CARD: r RECEIPT (TRIAD-972) v2 ===
card_id    : prereg-r-receipt/v2
supersedes : prereg-r-receipt/v1(branchP_and_r_spec_v1.md §II.3)

[3] 同時に判定される命題(★ B-1: 追加)
  TRIAD-972 の縮約式 / COMPOSITUM-rho(前件 2/3 = R3-GAP-4/5 は閉)
  ★★ P-K9U-1(★ 本修正で追加・凍結 commit bd80c44):
      L_{9,Aff} = Q(zeta_9, 3^{1/9})  ⟺  a の素因子台 = {3}
      ⟹ ★ [6] の a_class が出た時点で 的中/不的中 が確定する
      ⟹ 残前件 = 修理済み K9-COMPOSE + K9-UNRAM の二系統(Sol 便 119 F3(f))
      ⚠ a_class は素因子指数ベクトル(法 9・Q 側)なので「台」は直読できる
         ⟹ r を測る前に P-K9U-1 の判定が出てしまう ⟹ 事前列挙が必須だった
  ⚠ d_9, d_S4 が UNKNOWN のままなら |X\A| は決まらない

[2] UNKNOWN 枝(★ should-1: (r4) 新設)
  (r1) A1/A2 が満たされない(類が出ていない・位数のみ)
  (r2) r ∤ gcd(d_9,d_S4) ⟹ 規約不一致 ⟹ 座標系の再検査
  (r3) 両側の素因子基底が食い違う ⟹ 正規化の再検査
  ★ (r4) 新設: A4(i ∉ L_S4 / RES-INJ-9 / R3-GAP-4/5)のいずれかが
      *後に* 崩れた場合 ⟹ ★ r の測定値そのものは残る が
      972 への含意は消滅 ⟹ UNKNOWN
      (r 値 = Q^x/(Q^x)^9 の交わりという純代数量なので測定は無効化されない。
       無効化されるのは TRIAD-972 の縮約式を経由する解釈の方)

[4] QUAR(★ should-2: (Q8) に前件限定)
  ★ (Q8) 修正: 「(★ A1-A4 が成立する限りで)非算術 shadow の存在」
      であって具体的 witness の構成ではない ⟹「反例を得た」と書かない
      ⚠ 前件限定を落とすと、A4 が崩れた場合に無条件主張が流通する
=== END ===
```

## B. 3 修正の反映

| # | 指摘 | 反映 | 受諾 |
|---|---|---|---|
| **B-1** | [3] に **P-K9U-1** を追加 | §A [3] | ★ **全面受諾**。⚠ **原則 3 の二度目の破り** — $a\_class$(素因子指数ベクトル)が出れば**台は直読できる**ので、**$r$ を測る前に P-K9U-1 の判定が出てしまう**。事前列挙が必須だった |
| **should-1** | (r4) 新設 | §A [2] | 受諾。★ **「測定値は残るが含意が消える」という区別**は重要 — $r$ は純代数量 |
| **should-2** | (Q8) に前件限定 | §A [4] | 受諾。⚠ **前件限定を落とすと A4 崩壊時に無条件主張が流通する** |

**帰属**: 前哨 = falsifier。委嘱 = 司令塔(裁定 981)。
**申告**: ⚠ $r$・$\operatorname{ord}$ 未計算。走行ゼロ。


---

# 【v1.2 追記】[P0] 可否判定 — ★ 三値 = **部分可**(mod 9 迂回は成立・[P1] は GO)

**日付**: 2026-08-12 / **委嘱**: 裁定 982 / **入力**: `docs/notes/p0_uloc_k9_inventory_v1.md`(実装係・0832041)
**方式**: additive addendum(第 I 部・第 II 部・v1.1 追記とも不改変)

> ## ★★ 三値判定
> | 問 | 判定 |
> |---|---|
> | ① mod 9 迂回で sign が無害化できるか | ★ **可**(⚠ **r-GAP-1 が前件**) |
> | ② [P1] 平面モデル本走の GO | ★ **GO**(U-LOC **全体**は流用できない) |
> | ③ 部分流用(Shanks + 自己正規化降下)の価値 | ★ **価値あり**(窓非依存部品) |
> $$\boxed{\ \textbf{総合} = \textbf{部分可}\ }$$

## A. ① mod 9 迂回 — ★ **成立する**

### A.1 実装係の指摘の確認(**私も同じ結論**)

U-LOC の sign-triviality は $-1=(-1)^M$ を要する ⟹ **$M$ 奇数が本質前提**。
$M_9=18$(**偶数**)⟹ $\mathbf Q^\times/(\mathbf Q^\times)^{18}$ で $[-1]$ は**非自明**(位数 2 — $-1=c^{18}$ なる有理 $c$ は無い、$c^{18}>0$)。
⟹ ★ **実装係の「構造的に破れる」は正しい**。

### A.2 ★★ 迂回の成立(**私の判定**)

自然な全射 $\mathrm{pr}:\mathbf Q^\times/(\mathbf Q^\times)^{18}\to\mathbf Q^\times/(\mathbf Q^\times)^{9}$ を考える。
$$\mathrm{pr}([-1]):\quad -1=(-1)^9\ \Longrightarrow\ \textbf{法 9 で自明}$$
$$\boxed{\ \Longrightarrow\ \textbf{法 18 で測ってから法 9 へ落とせば sign は}\textbf{自動的に消える}\ }$$

### A.3 ★ 情報損失の検査(**落ちない**)

| 項目 | 判定 |
|---|---|
| $\mathrm{pr}$ の核 | 位数 2 の部分(**2-part**) |
| $d_9=[L_{9,\mathrm{Aff}}:\mathbf Q(\zeta_9)]\in\{1,3,9\}$ | ★ **3-part のみ**に依存 |
| ⟹ | ★ **2-part は $d_9$ に不要** ⟹ **迂回で必要な情報は落ちない** |

★★ **さらに強い理由**: **K9-C2**($L_9=L_{9,\mathrm{Aff}}(i)$・$C_2$ 因子は $\chi\bmod4=\mathbf Q(i)$)により、**2-part は既に別記帳されている**。⟹ **法 9 側に押し込むのは記帳の整合とも合う**。

### A.4 ⚠ 前件 —【r-GAP-1】

迂回の実体は「$a_9$(法 18)→ $a$(法 9)」であり、これは私が $r$ 仕様 §II.1.1 で立てた【**r-GAP-1**】そのもの。
$$\boxed{\ \textbf{⚠ }\mathrm{pr}\ \textbf{の存在は自明だが、}\textbf{類として何が出るか}\ \textbf{の規約は未確定}\ }$$
★ **ただし本判定にとっては十分**: 「sign が無害化されるか」という問いには **YES** と答えられる(射影の存在だけで足りる)。⚠ 「$a$ の類が出るか」は別問題で **R-3 の出力仕様**の話。

## B. ② [P1] 平面モデル本走 = ★ **GO**

**理由**: U-LOC の**未確立部分(商被覆の $K^{(9)}$ 対応物)**が残る。sign が無害化されても、**「$W$ の方程式が不要」という U-LOC の本体は移植できていない**。
$$\boxed{\ \Longrightarrow\ \textbf{モデル構成は依然必要 ⟹ }[P1]\ \textbf{を発注してよい}\ }$$
⚠ ★ **ただし目標の再設定を提案**: モデルの用途は「$u_9$(法 18)の抽出」だが、**下流で法 9 に落とすなら、モデル段階から法 9 の情報だけ追えばよい場面がある**かもしれない。⟹ **[P1] の実行中に判明する** ⟹ **今は [P1] をそのまま走らせる**のが正しい(先回りして設計を歪めない)。

## C. ③ 部分流用の価値 = ★ **あり**

| 部品 | 判定 |
|---|---|
| **Shanks 三次公式**(窓非依存) | ★ **そのまま使える**(窓に依存しないと実装係が確認済) |
| **自己正規化降下** | ★ **使える**。⚠ ただし **R-0b で $\mathrm{Deck}=1$(自己正規化)が確定済** ⟹ **降下の余地がどこにあるか**は要確認 |
| 商被覆の $K^{(9)}$ 対応物 | ✘ **未確立**(実装係の申告どおり) |

$$\boxed{\ \textbf{⟹ 中間形の価値は「}[P1]\ \textbf{の一部を軽くする」ところにある — }[P1]\ \textbf{の代替ではない}\ }$$

## D. ⟹ 実装係への発注(推薦)

1. ★ **[P1] を発注**(`branchP_and_r_spec_v1.md` 第 I 部 §I.4 の指示書のまま)。
2. ★ **Shanks 三次公式と自己正規化降下は [P1] の中で流用**(部分流用は独立工程にしない — **[P1] の部品として使う**)。
3. ⚠ **R-3 の出力仕様に $a\_class$(法 9 の素因子指数ベクトル)を明記**(★ **r-GAP-1** と **P8 v3.1** の要求と同一)。

**帰属**: [P0] 棚卸し = 実装係(0832041)。委嘱 = 司令塔(裁定 982)。
**本追記の新規部分**: ① **迂回の成立判定**($\mathrm{pr}$ で sign が消える)② ★ **情報損失がないことの確認**(2-part は $d_9$ に不要・K9-C2 で既に別記帳)③ **[P1] GO の理由**(U-LOC 本体 = 商被覆対応物が未確立)④ **部分流用を独立工程にせず [P1] の部品にする**という発注形。
**申告**: 走行ゼロ・$u$/$\operatorname{ord}$ 未計算・**Sol 未監査**。
