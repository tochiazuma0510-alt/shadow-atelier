# 鏡映理論の B₄/2008 系への移植 — 設計ノート v1

**状態札: `design only (v1.2) / paper-proof candidate / Sol 未監査 / GAP 実行ゼロ / 実測ゼロ / census 生成ゼロ / 封印非接触 / 発火請求なし`**
**v1.1 追補: 【PIN-B4-1】§8 で閉・【GAP-B4-2】§9 で閉。**
**v1.2 追補(裁定 631): 【GAP-B4-1】§11 で閉・【GAP-B4-3】§12 で閉・【GAP-B4-4】§13 で部分閉(下界 192 を確定)。v1/v1.1 本文は不改変、§11–§13 を追加のみ。**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-06
- 委嘱: 司令塔(研究者起点の新戦線)「鏡映理論を B₄/2008 系へ移植する設計ノート。**設計のみ・測定禁止**」
- 入力正本(すべて既在・**外部文献の新規取り寄せゼロ**):
  - `docs/notes/theorem_check_mirrorall_l3vacuous_v1.md`(**移植元**: MIRROR-SHADOW / PSL-GEN / MIRROR-PSL / MIRROR-ODD / ABEL-TYPE / §F MAP-DICT / §G 中心特性論法)
  - `docs/notes/twin_witness_prereg_iffirst_v1.md`(§1 層定義・§2.2 MIRROR-SHADOW(B₃ 版)・§5 出力規則・§6 停止規則 — **prereg の型紙**)
  - `docs/notes/b4_original_gtshadows_extraction_v1.md`(**2008.00066 の定義の唯一の正本**・画像照合済: (2.4)(2.18)(2.19)(2.20)(2.25)–(2.29)(2.36)(2.51)(2.61)(A.2)(A.5))
  - `docs/notes/b4_direct_adjudication_feasibility_v1_2.md`(§1.1 𝒱・§2.2 Ñ_core/補題 CORE-4・§2.5 定理 B4-CANON・§2.6 4 窓表・§5 計算量・§7.3 防壁 R1–R8・付録 A.5 Δ² 検算)
  - `docs/notes/b4_theorem_check_v1.md`(§3 verbal 論法の独立検分・§5.3 VERBAL-DESCENT)
  - `docs/notes/wall_design_audit_v1.md` §6(ι の初等的事実・**B₃ 限定**)/ `docs/notes/auto_settled_check_v1.md` §3.4(VERBAL-ISO)
  - `search/certs/lins_twin_census_v1_20260806.json` + `search/lins-twin-census-v1.g`(**B₃ census の実測コスト** = 帯見積りの唯一の錨)

> ## 非接触・規律の申告
> - **機械ゼロ**。GAP 起動なし・python なし・census 生成なし・LINS 走なし。本稿は**紙の設計のみ**。
> - 封印 3 量非接触・705,894 対宇宙非接触・`Im R` / `d_N` 非接触・L3(c∉N)層非接触。
> - **発火も凍結も unlock も請求しない**。§4 の census は**便 112 認可後**の設計案であり、本稿では登録集合を固定しない(= 事前登録ではない・**prereg の設計図**である)。
> - 全命題 **candidate**(Sol 監査未了)。**Lean 不使用 ⟹ verified と呼ばない。**

---

## 0. 一枚まとめ(先に 7 行)

| # | 内容 |
|---|---|
| **①** ★★★ | **MIRROR-SHADOW-B4 は成立する(紙・v1.1 で完備)**。$(m,f)=(-1,1)$ は 2008 の hexagon 2 本を **$B_3$ 内の恒等式**として満たし(§2.2)、pentagon は $f=1$ で自明。**v1.1 §8 で原文 (2.25)(2.26) を逐語確認** ⟹ $T^{B_4}_{-1,1}=\pi_N\circ\iota$(**厳密等式・内部ずれなし**)⟹ **全窓で charming GT-shadow**、$\ker T^{PB_4}_{-1,1}=\iota(\widetilde N)$。**PIN は閉** |
| **②** ★★ | 対称性在庫: $\{\mathrm{id},\ \iota,\ \mathrm{flip},\ \iota\!\cdot\!\mathrm{flip}\}$ のうち **flip($\sigma_i\mapsto\sigma_{4-i}$)は内部**($=\mathrm{Ad}(\Delta_4)$)⟹ $\mathrm{Out}(B_4)\supseteq\langle\iota\rangle$。等号は Dyer–Grossman(**完全性にのみ使用・工房規約どおり分離**) |
| **③** ★★ | **現用 B₄ 窓($\widetilde N^*=\mathcal V(PB_4)$・$\widetilde N_{\rm core}$)は全て $\iota$-固定** ⟹ **双子の相方になりえない**(補題 FIXED-B4)。鏡映線は現用窓では**構造的に空**であり、新しい窓層を作らない限り観測対象が存在しない |
| **④** ★★★ | ★ **MIRROR-ODD は B₄ へ移植できない**(補題 NO-PSL-B4): $B_n=\langle\Delta_n,\delta_n\rangle$ は **$n=3$ でしか成り立たない**(abelianization の gcd が $n=3$ でだけ 1)。⟹ PSL-GEN → $\widehat P_0^{\rm ab}$ 指数 3 → $\mu(W)\ne1$ の**エンジンが丸ごと消える** |
| **⑤** ★★★ | 代わりに **ABEL-FIXED-B4** が効く: $\iota$ は $PB_4^{\rm ab}\cong\mathbf Z^6$ に **$-\mathrm{id}$** で作用 ⟹ **$\widetilde N\supseteq[PB_4,PB_4]$ なる窓は全て $\iota$-固定**。低指数帯は可換商が支配的 ⟹ **帯内の鏡映双子ゼロ**が予言される |
| **⑥** ★★ | **帯の見積り**: 窓は $[B_4:\widetilde N]=24\cdot[PB_4:\widetilde N]$。B₃ census の到達($[PB_3:N]\le166$)に並ぶには $B_4$-指数 **≈3984** が必要で**射程外**。現実的上限は **$B_4$-指数 240 → 480 → 720 → 1000 の梯子**(1000 でも $[PB_4:\widetilde N]\le41$)⟹ census の価値は **witness 狩りではなく陰性の在庫**である |
| **⑦** ★ | 井原接続: 2008 系は **$\widehat{GT}\cong\varprojlim ML$**(Thm 3.8)の**錨**。$\iota$ は複素共役の像 ⟹ 鏡映対 = 「複素共役で移り合う 2 窓」= 捩れ探索の直撃点(§6) |

> ### ★ 本稿の最重要の結論(先に言う)
> **移植して得があるのは ①(witness 供給)と ⑤(陰性の紙定理)であり、④ の意味で「MIRROR-ODD の B₄ 版」は存在しない。** したがって B₄ census を「双子 witness 狩り」として設計するのは**期待値が低い**。設計は「**陰性在庫 + ORB 型直接判定の土俵づくり**」に振るべきである(§4.4 の予言はこの読みを反証可能な形に固定する)。

---

## 1. 記号と前提(**再定義しない・出所つき**)

### 1.1 2008 系の記号(正本 = `b4_original_gtshadows_extraction_v1.md`)

| 記号 | 定義 | 出所 |
|---|---|---|
| 窓 | $\widetilde N\in\mathrm{NFI}_{PB_4}(B_4)$($B_4$ で正規・$PB_4$ に含まれる・有限指数) | 2008 §1.2 (p.4) |
| $\widetilde N_{PB_3}$ | **(2.4)**: 5 本の逆像の交わり $\varphi_{123}^{-1}(\widetilde N)\cap\varphi_{12,3,4}^{-1}\cap\varphi_{1,23,4}^{-1}\cap\varphi_{1,2,34}^{-1}\cap\varphi_{234}^{-1}$。**$\widetilde N\cap PB_3$ ではない**(裁定 252 の読み違い箇所) | 2008 (2.4) |
| hexagon 1 | **(2.18)** $\sigma_1x_{12}^m\,f^{-1}\sigma_2x_{23}^m f=f^{-1}\sigma_1\sigma_2(x_{13}x_{23})^m$(in $B_3/\widetilde N_{PB_3}$) | 2008 (2.18) |
| hexagon 2 | **(2.19)** $f^{-1}\sigma_2x_{23}^m f\,\sigma_1x_{12}^m=\sigma_2\sigma_1(x_{12}x_{13})^m f$ | 2008 (2.19) |
| pentagon | **(2.20)** $\varphi_{234}(f)\varphi_{1,23,4}(f)\varphi_{123}(f)\equiv\varphi_{1,2,34}(f)\varphi_{12,3,4}(f)$(in $PB_4/\widetilde N$)。**$f$ のみ・$m$ 非依存** | 2008 (2.20) |
| GT-shadow | GT-pair + $T^{PB_4},T^{PB_3},T^{PB_2}$ の全射(Def 2.9)。friendly = $2m+1$ が $\mathbf Z/N_{\rm ord}$ の単元 (2.36) | 2008 Def 2.9 / (2.36) |
| charming | $fN_{PB_3}$ が $f_1\in[F_2,F_2]$ で代表可 ∧ **(2.61)** $T^{F_2}_{m,f}$ 全射。$N_{F_2}:=\widetilde N_{PB_3}\cap F_2$ (2.62) | 2008 Def 2.19 |
| groupoid | **(2.51)** $\mathrm{Hom}(\widetilde K,\widetilde N)=\{[(m,f)]\in GT(\widetilde N)\mid\ker T^{PB_4}_{m,f}=\widetilde K\}$ ⟹ **source = ker・target = $\widetilde N$**(B₃ 線と同じ向き) | 2008 (2.51) |
| $x_{ij}$ | **(A.2)** $x_{ij}=\sigma_{j-1}\cdots\sigma_{i+1}\sigma_i^2\sigma_{i+1}^{-1}\cdots\sigma_{j-1}^{-1}$;**(A.5)** $c=x_{23}x_{12}x_{13}=(\sigma_1\sigma_2)^3$ | 2008 (A.2)(A.5) |

### 1.2 ★★ 記号衝突の警告(**2 件・違反すると静かに壊れる**)

> **(W-1) `c₄` は $B_4$ の中心生成元ではない。** 本リポジトリの `c₄` は `Chk6` の第 4 条件(charming の $q\in[Q_P,Q_P]$)を指す(`gtpi_cv9_freeze_v1.md` L45・`gtpi_v1.md` §2)。**中心は $\Delta_4^2$ と書く**(委嘱文の「$c_4$=中心生成元」はこの規約に合わせて読み替える)。
> **(W-2) $\iota_{K,N}$**(`ihnec_v1_addendum_e_b4.md` §E-A.1)は 2008 (3.24) の自然写像であって、本稿の自己同型 $\iota$ とは**別物**。本稿では自己同型を常に $\iota$、2008 の自然写像を $\iota_{K,N}$ と添字つきで書く。

### 1.3 $B_4$ の中心と $\iota$(既在の追認 + 本稿の追加)

$$B_4=\langle\sigma_1,\sigma_2,\sigma_3\mid \sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2,\ \sigma_2\sigma_3\sigma_2=\sigma_3\sigma_2\sigma_3,\ \sigma_1\sigma_3=\sigma_3\sigma_1\rangle,$$
$$\Delta_4:=\sigma_1\sigma_2\sigma_3\sigma_1\sigma_2\sigma_1,\qquad \Delta_4^2=(\sigma_1\sigma_2\sigma_3)^4=Z(B_4)\text{ の生成元},\qquad \delta_4:=\sigma_1\sigma_2\sigma_3 .$$
($\Delta_4^2=(\sigma_1\sigma_2\sigma_3)^4$ と $\Delta^2=\prod_{i<j}x_{ij}$ は `b4_direct_adjudication_feasibility_v1_2.md` 付録 A.5 で Artin 忠実表現上の**語同一性として証明済**。)

> ### 補題 IOTA-B4(candidate・本稿。B₃ 版 `wall_design_audit_v1.md` §6.2 の初等 3 行の $B_4$ 版)
> $\iota:\sigma_i\mapsto\sigma_i^{-1}$ は $\mathrm{Aut}(B_4)$ の元で、$\iota^2=\mathrm{id}$、$\iota(PB_4)=PB_4$、$\iota(\Delta_4^2)=\Delta_4^{-2}$、$\iota(x_{ij})$ は $x_{ij}^{-1}$ の**共役**。

**証明.** 生成元の逆転は braid 関係を**その逆関係へ**送る($(\sigma_1\sigma_2\sigma_1)^{-1}=\sigma_1^{-1}\sigma_2^{-1}\sigma_1^{-1}$、$(\sigma_2\sigma_1\sigma_2)^{-1}=\sigma_2^{-1}\sigma_1^{-1}\sigma_2^{-1}$)ので関係式は保たれ、可換関係 $\sigma_1\sigma_3=\sigma_3\sigma_1$ も同様 ⟹ $\iota$ は準同型で $\iota^2=\mathrm{id}$ ⟹ 自己同型 ✓。$B_4/PB_4=S_4$ 上で $\sigma_i\mapsto\sigma_i^{-1}$ は同じ互換 ⟹ $\iota$ は $S_4$ 上恒等 ⟹ $\iota(PB_4)=PB_4$ ✓。$Z(B_4)=\langle\Delta_4^2\rangle$ は特性ゆえ $\iota(\Delta_4^2)=\Delta_4^{\pm2}$;$B_4^{\rm ab}=\mathbf Z$ 上で $\iota=-1$、$\Delta_4^2\mapsto12$ ⟹ 符号が反転 ⟹ $\iota(\Delta_4^2)=\Delta_4^{-2}$ ✓。$x_{ij}=w\sigma_i^2w^{-1}$($w=\sigma_{j-1}\cdots\sigma_{i+1}$、(A.2))⟹ $\iota(x_{ij})=\iota(w)\sigma_i^{-2}\iota(w)^{-1}=(\iota(w)w^{-1})\,x_{ij}^{-1}\,(\iota(w)w^{-1})^{-1}$ ✓。∎

> ### 系 CENTER-B4(§G の中心特性論法の $B_4$ 版・**そのまま移る**)
> $\langle\Delta_4^2\rangle=Z(B_4)$ は特性 ⟹ **任意の $\varphi\in\mathrm{Aut}(B_4)$ について $\Delta_4^2\in\widetilde N\iff\Delta_4^2\in\varphi(\widetilde N)$**。
> ⟹ **「$\Delta_4^2\in\widetilde N$ が割れている双子対は、$\mathrm{Aut}(B_4)$ のどの元でも説明できない = exotic」**(§G.1② の逐語移植)。

---

## 2. ① 補題 MIRROR-SHADOW-B4

### 2.1 主張

> ### 補題 MIRROR-SHADOW-B4(candidate・本稿)
> 任意の $\widetilde N\in\mathrm{NFI}_{PB_4}(B_4)$ に対し($\Delta_4^2\in\widetilde N$ は**不要**)
> $$\boxed{\ [(-1,1)]\in GT(\widetilde N)\ \text{は charming GT-shadow であり、}\ \ker T^{PB_4}_{-1,1}=\iota(\widetilde N)\ }$$
> ゆえに $\mathrm{GTSh}(\iota(\widetilde N),\widetilde N)\ne\emptyset$ であり
> $$\iota(\widetilde N)\ne\widetilde N\ \Longrightarrow\ [(-1,1)]\ \text{は非 settled shadow}\ \Longrightarrow\ \widetilde N\ \text{は非 isolated}.$$
> 対偶: **isolated $\Rightarrow$ $\iota$-不変**。

### 2.2 (a) hexagon 2 本 — **$B_3$ 内の恒等式**(逐語検算)

$m=-1$、$f=1$ を (2.18)(2.19) に代入する。$B_3$ 内で $x_{12}=\sigma_1^2$、$x_{23}=\sigma_2^2$、$x_{13}=\sigma_2\sigma_1^2\sigma_2^{-1}$((A.2))。

**(2.18)**: 左辺 $=\sigma_1x_{12}^{-1}\sigma_2x_{23}^{-1}=\sigma_1\sigma_1^{-2}\sigma_2\sigma_2^{-2}=\sigma_1^{-1}\sigma_2^{-1}$。
右辺 $=\sigma_1\sigma_2(x_{13}x_{23})^{-1}=\sigma_1\sigma_2\,x_{23}^{-1}x_{13}^{-1}=\sigma_1\sigma_2\sigma_2^{-2}\bigl(\sigma_2\sigma_1^{2}\sigma_2^{-1}\bigr)^{-1}=\sigma_1\sigma_2^{-1}\cdot\sigma_2\sigma_1^{-2}\sigma_2^{-1}=\sigma_1\sigma_1^{-2}\sigma_2^{-1}=\sigma_1^{-1}\sigma_2^{-1}$ ✓ **一致**。

**(2.19)**: 左辺 $=\sigma_2x_{23}^{-1}\sigma_1x_{12}^{-1}=\sigma_2\sigma_2^{-2}\sigma_1\sigma_1^{-2}=\sigma_2^{-1}\sigma_1^{-1}$。
右辺 $=\sigma_2\sigma_1(x_{12}x_{13})^{-1}=\sigma_2\sigma_1\,x_{13}^{-1}x_{12}^{-1}=\sigma_2\sigma_1\bigl(\sigma_2\sigma_1^{-2}\sigma_2^{-1}\bigr)\sigma_1^{-2}
=(\sigma_2\sigma_1\sigma_2)\sigma_1^{-2}\sigma_2^{-1}\sigma_1^{-2}\overset{\rm braid}{=}(\sigma_1\sigma_2\sigma_1)\sigma_1^{-2}\sigma_2^{-1}\sigma_1^{-2}=\sigma_1\bigl(\sigma_2\sigma_1^{-1}\sigma_2^{-1}\bigr)\sigma_1^{-2}$。
$\sigma_2\sigma_1\sigma_2^{-1}=\sigma_1^{-1}\sigma_2\sigma_1$(braid の標準系)⟹ $\sigma_2\sigma_1^{-1}\sigma_2^{-1}=\sigma_1^{-1}\sigma_2^{-1}\sigma_1$ ⟹
右辺 $=\sigma_1\cdot\sigma_1^{-1}\sigma_2^{-1}\sigma_1\cdot\sigma_1^{-2}=\sigma_2^{-1}\sigma_1^{-1}$ ✓ **一致**。

$$\Longrightarrow\ \boxed{\ \textbf{(2.18)(2.19) は }m=-1,f=1\textbf{ で }B_3\textbf{ 内の恒等式}\ }\quad(\text{mod }\widetilde N_{PB_3}\ \text{以前に等号})$$

**⟹ 窓に依らない。** これは B₃-gentle 版(`twin_witness_prereg_iffirst_v1.md` §2.2 (a))と**同じ現象の 2008 記法版**である。

### 2.3 (b) pentagon・(c) charming・(d) kernel

- **pentagon (2.20)**: $f=1$ ⟹ 各 $\varphi_*(1)=1$ ⟹ $1\cdot1\cdot1\equiv1\cdot1$ ✓ **無条件**(pentagon は $f$ のみの条件・$m$ 非依存)。
- **friendly/charming**: $2m+1=-1$ は任意の $\mathbf Z/N_{\rm ord}$ で単元(逆元は自分自身)✓ (2.36)。$f=1\in[F_2,F_2]$ ✓。(2.61) の $T^{F_2}_{-1,1}$ 全射は (d) と同じ理由 ✓。
- **kernel**: (d) $T^{PB_4}_{-1,1}=\pi_{\widetilde N}\circ\iota$ が成り立てば、$\iota^2=\mathrm{id}$ より $\ker=\iota^{-1}(\widetilde N)=\iota(\widetilde N)$ ✓、全射性も $\iota\in\mathrm{Aut}(B_4)$ から自動 ✓。

### 2.4 ★ 【PIN-B4-1】(**唯一の未 pin 点・原文参照が要る**)

> (d) の前提「**$(m,f)=(-1,1)$ において 2008 の (2.25)(2.26)(2.28)(2.29) が $T^{B_4}_{-1,1}(\sigma_i)=\sigma_i^{-1}$($i=1,2,3$)に特殊化する**」は、**本稿では原文を開いていない**(既在の抽出ノート §1.4 に式番号のみ確認)。
> - B₃-gentle 版では Prop 3.2 が $\sigma_1\mapsto\sigma_1^{2m+1}$、$\sigma_2\mapsto f^{-1}\sigma_2^{2m+1}f$ を与え、$(-1,1)$ で $\sigma_i\mapsto\sigma_i^{-1}$ ⟹ $T=\pi\circ\iota$ ✓ となる。2008 も同型の形が期待されるが、**期待は根拠ではない**。
> - **必要な作業**: `docs/notes/b4_original_gtshadows_extraction_v1.md` §1.4 の (2.25)–(2.29) を読み、$(m,f)=(-1,1)$ を代入して 3 生成元の像を確定する(**紙 5 分・機械不要**)。$\sigma_3$ の像が $\sigma_3^{-1}$ でない(例: 別の共役子が付く)場合、$T_{-1,1}$ は $\pi\circ\iota$ ではなく $\pi\circ\iota\circ\mathrm{Inn}(u)$ 型になり、**核は $\iota(\widetilde N)$ のまま**(内部自己同型は正規部分群を動かさない)だが、**帰属の文言は書き換えが要る**。
> - ⟹ **(a)(b)(c) は本稿で確定、(d) は PIN 待ち**。ただし上記のとおり **kernel の結論は内部自己同型のずれに鈍感**なので、補題の**結論は堅い**(壊れるとしたら「$T$ が $\iota$ そのもの」という帰属の言い方だけ)。

### 2.5 格の限定(B₃ 版から逐語で引き継ぐ)

$(-1,1)$ は Ihara ICM の複素共役($\chi=-1,f=1$)であり **算術元**。⟹ 本経路が出す witness は「**settled 述語が FALSE を返せることの実物**」であって、**非算術証人ではない**。混同を禁止する(`twin_witness_prereg_iffirst_v1.md` §2.2 の警告をそのまま適用)。

---

## 3. ② 対称性在庫の台帳($\mathrm{Out}(B_4)$)

### 3.1 在庫(4 元・うち非自明外部は 1 つ)

| 記号 | 生成元への作用 | 内部か | 根拠 |
|---|---|---|---|
| $\mathrm{id}$ | $\sigma_i\mapsto\sigma_i$ | 内部 | — |
| **flip** $\ \phi$ | $\sigma_i\mapsto\sigma_{4-i}$($\sigma_1\!\leftrightarrow\!\sigma_3$, $\sigma_2$ 固定) | ★ **内部** $=\mathrm{Ad}(\Delta_4)$ | §3.2 |
| **$\iota$** | $\sigma_i\mapsto\sigma_i^{-1}$ | **外部** | §3.3 |
| $\iota\phi=\phi\iota$ | $\sigma_i\mapsto\sigma_{4-i}^{-1}$ | 外部($\iota$ と同じ類) | $\phi$ が内部ゆえ |

### 3.2 flip が内部であること(**Δ₄ 共役の確認**)

$\Delta_n\sigma_i\Delta_n^{-1}=\sigma_{n-i}$ は古典的事実。**$B_4$ での確認手順(紙・3 行)**: $\Delta_4=\sigma_1\sigma_2\sigma_3\sigma_1\sigma_2\sigma_1$ に対し $\Delta_4\sigma_1\Delta_4^{-1}=\sigma_3$、$\Delta_4\sigma_2\Delta_4^{-1}=\sigma_2$、$\Delta_4\sigma_3\Delta_4^{-1}=\sigma_1$ を braid 関係で書き下す。$\mathrm{Ad}(\Delta_4)^2=\mathrm{Ad}(\Delta_4^2)=\mathrm{id}$($\Delta_4^2$ 中心)⟹ flip は**位数 2 の内部自己同型**であり $\mathrm{Out}$ に寄与しない ✓。
> ⚠ **【GAP-B4-1】**: 上の 3 本の共役等式は本稿では**書き下していない**(委嘱の「測定禁止」を尊重し、Artin 忠実表現 $B_4\hookrightarrow\mathrm{Aut}(F_4)$ 上の 10 行検算も**走らせていない**)。古典的事実だが**工房内 pin は未取得** ⟹ §7 の【GAP】に起票。B₃ 側では同じ事実($\Delta\sigma_1\Delta^{-1}=\sigma_2$)が `bu_s35_embedding_v1.md` §1 で既に使用済み(そちらは検算済)。

### 3.3 $\iota$ が外部であること・$\mathrm{Out}(B_4)=\langle\iota\rangle$

- **外部性(初等・自前)**: $\iota$ は $B_4^{\rm ab}=\mathbf Z$ 上で $-1$、内部自己同型は $B_4^{\rm ab}$ 上で恒等 ⟹ $\iota\notin\mathrm{Inn}(B_4)$ ✓(**この 1 行で足り、文献不要**)。
- **完全性** $\mathrm{Out}(B_n)=\mathbf Z/2$($n\ge3$)は **Dyer–Grossman 1981**。工房規約(`wall_design_audit_v1.md` §6.2)どおり **「これ以外に外部対称が無い」の主張にのみ使用**し、本稿の補題群は**完全性を使わない**。
- ⟹ 台帳の結論: $$\boxed{\ \mathrm{Out}(B_4)\supseteq\langle\iota\rangle\cong\mathbf Z/2\ \text{(自前)},\qquad \text{等号は Dyer–Grossman(外部文献・分離管理)}\ }$$

### 3.4 なぜ在庫が要るのか(移植の設計上の意味)

「双子($B_4/\widetilde N\cong B_4/\widetilde K$)が $\mathrm{Aut}(B_4)$ で説明されるか」を問うとき、**説明の候補は $\mathrm{Out}$ の元だけ**である($\mathrm{Inn}$ は $\widetilde N$ を動かさない)。在庫が $\{1,\iota\}$ しかないなら、**非鏡映双子 = exotic** の定義が B₃ と**逐語で同じ**になる ✓。flip が外部だったなら exotic の定義に第 2 の軸が要ったが、§3.2 によりその心配は無い(**これが在庫台帳の実効**)。

---

## 4. ③④ 現用窓・census 設計

### 4.1 ③ 現用 B₄ 窓は全て $\iota$-固定

> ### 補題 FIXED-B4(candidate・本稿)
> $$\iota(\widetilde N^*)=\widetilde N^*\quad(\widetilde N^*=\mathcal V(PB_4)=\gamma_5(PB_4)PB_4^7),\qquad \iota(\widetilde N_{\rm core})=\widetilde N_{\rm core}.$$
> ゆえに**どちらも双子の相方になりえず、$[(-1,1)]$ は settled**(MIRROR-SHADOW-B4 が witness を出さない)。

**証明.** (i) $\mathcal V$ は verbal 演算子 ⟹ $\mathcal V(PB_4)$ は $PB_4$ で**完全不変**(`b4_theorem_check_v1.md` §3.1 の逐語)。$\iota(PB_4)=PB_4$(補題 IOTA-B4)⟹ $\iota|_{PB_4}\in\mathrm{Aut}(PB_4)$ ⟹ $\iota(\mathcal V(PB_4))=\mathcal V(PB_4)$ ✓。
(ii) $\widetilde N_{\rm core}=\mathrm{core}_{B_4}(\ker\widetilde\psi)$、$\ker\widetilde\psi=\bigcap_i p_i^{-1}(N)$。$\iota\in\mathrm{Aut}(B_4)$ ゆえ $\iota(\mathrm{core}_{B_4}(H))=\mathrm{core}_{B_4}(\iota(H))$ ✓。$N=\mathcal V(F_2)\times\langle c\rangle$ は $\iota$-不変($\mathcal V(F_2)$ verbal かつ $\iota(F_2)=F_2$、$\iota(\langle c\rangle)=\langle c\rangle$)✓。あとは **$p_i\circ\iota=\iota\circ p_i$**(紐忘却と鏡映の可換性)があればよい。∎(⟸ **【GAP-B4-2】** 参照)

> **【GAP-B4-2】**: $p_i\circ\iota=\iota\circ p_i$($p_i:PB_4\to PB_3$ = 第 $i$ 紐忘却)は**幾何的には自明**(鏡像を取る操作と紐を抜く操作は可換)だが、**代数的な逐語証明を本稿では書いていない**。$x_{jk}$ 生成元上での 6 行の確認で閉じる(測定禁止のため未実行)。⟹ 補題 FIXED-B4 の (ii) は**この 1 点に条件つき**。(i) は無条件。

> ### ★ 設計上の含意(重い)
> **現用の 2 窓では鏡映線は空である。** これは失敗ではなく**構造的事実**であり、B₃ 側の VERBAL-ISO(`auto_settled_check_v1.md` §3.4「$N_{F_2}$ 完全不変 ⟹ isolated」)と**同じ現象**である。⟹ **鏡映双子を見たいなら「verbal でない窓層」を作らねばならない** — それが §4.3 の census の存在理由。

### 4.2 ★★★ ④ なぜ MIRROR-ODD が移植できないか

> ### 補題 NO-PSL-B4(candidate・本稿)
> $\Delta_n\mapsto\frac{n(n-1)}2$、$\delta_n\mapsto n-1$ in $B_n^{\rm ab}=\mathbf Z$。よって
> $$\gcd\Bigl(\tfrac{n(n-1)}2,\ n-1\Bigr)=1\iff n=3 .$$
> ゆえに **$n\ge4$ では $\langle\Delta_n,\delta_n\rangle\subsetneq B_n$**(abelianization の像が真部分群)。とくに **$B_4\ne\langle\Delta_4,\delta_4\rangle$**($\gcd(6,3)=3$)。

**証明.** $n$ 偶: $\frac{n(n-1)}2=(n-1)\frac n2$ ⟹ $\gcd=n-1$。$n$ 奇: $=n\cdot\frac{n-1}2$ ⟹ $\gcd=\frac{n-1}2$。$n\ge3$ で $1$ になるのは $n=3$ のみ。∎

**帰結(移植不能の所在)**: B₃ 版のエンジンは
$$\underbrace{c\in N\Rightarrow\widehat P=\langle U,W\rangle,\ U^2=W^3=1}_{\textbf{PSL-GEN}}\ \Rightarrow\ \underbrace{\widehat P_0=\langle W,UWU\rangle,\ [\widehat P:\widehat P_0]\le2,\ \exp(\widehat P_0^{\rm ab})\mid3}_{\text{(A.1)}}\ \Rightarrow\ \mu(W)\ne1\ \Rightarrow\ \iota(N)\ne N$$
であった。$B_4$ では**第 1 段が崩れる**: $\Delta_4^2\in\widetilde N$ としても $B_4/\langle\Delta_4^2\rangle$ は「位数 2 と位数 4 の元で生成される群」にすら**ならない**(NO-PSL-B4)。$B_4/Z$ は有限巡回群の自由積ではなく(内部に $F_2$ を含む)、**「指数 3 の abelian 化」に相当する退化がない** ⟹ (A.1) の類似物が作れない。
$$\boxed{\ \textbf{MIRROR-ODD の }B_4\textbf{ 版は存在しない。移植で閉じる対の数の期待値は }\mathbf 0\ \textbf{である。}\ }$$

> ### ★ 代替エンジン(**これが B₄ 帯で実際に効く紙の定理**)
> ### 補題 ABEL-FIXED-B4(candidate・本稿)
> $\iota$ は $PB_4^{\rm ab}\cong\mathbf Z^6$ 上で $-\mathrm{id}$ として作用する。ゆえに
> $$\boxed{\ \widetilde N\supseteq[PB_4,PB_4]\ \Longrightarrow\ \iota(\widetilde N)=\widetilde N\ }$$
> すなわち**商 $PB_4/\widetilde N$ が可換な窓は全て $\iota$-固定**であり、鏡映双子になりえない。

**証明.** 補題 IOTA-B4 より $\iota(x_{ij})$ は $x_{ij}^{-1}$ の共役 ⟹ $PB_4^{\rm ab}$ 上で $\bar x_{ij}\mapsto-\bar x_{ij}$ ⟹ $\iota|_{PB_4^{\rm ab}}=-\mathrm{id}$ ⟹ **任意の部分群が不変**。$[PB_4,PB_4]$ は特性ゆえ $\iota$ 不変で、$\widetilde N/[PB_4,PB_4]\le PB_4^{\rm ab}$ も不変 ⟹ $\widetilde N$ 不変 ✓。∎
(**B₃ 版の系 (a)「$P$ 可換 ⟹ 鏡映不変」と同じ現象**。$PB_4^{\rm ab}=\mathbf Z^6$ は `b4_direct_adjudication_feasibility_v1_2.md` §2.5 / `stage1_run.log` に既在。)

### 4.3 ④ census の prereg 設計(**設計図・登録はしない**)

#### 4.3.1 底群・道具

- 底群: **$B_4=\langle\sigma_1,\sigma_2,\sigma_3\mid\text{braid}\times2,\ \sigma_1\sigma_3=\sigma_3\sigma_1\rangle$**(3 生成 3 関係)。道具は `lins`(B₃ 版 `search/lins-twin-census-v1.g` の**表示だけ差し替え**)。**LID-1 規律**(単一プロセス・単一 `LowIndexNormalSubgroupsSearch` 呼び出し)を踏襲。
- 各 node について記録するフラグ(B₃ 版 cert の欄を逐語移植・**名前だけ B₄ 化**):
  `index` / `in_PB4`($\widetilde N\le PB_4$) / `delta2_in_N`($\Delta_4^2\in\widetilde N$ — **`c_in_N` の B₄ 版。`c₄` とは書かない**(W-1)) / `id_group` / `structure_description` / `canonical_id_words` / `n_meet_pb3_index`。

#### 4.3.2 ★ 帯の見積り(**$B_4$-指数で**・委嘱の核心)

**事実 1**: 窓は $\widetilde N\le PB_4$ ゆえ $[B_4:\widetilde N]=24\cdot[PB_4:\widetilde N]$($[B_4:PB_4]=24$)。
**事実 2**(B₃ の実績・唯一の錨): 指数 $\le1000$ で LINS 本体 **149 s**・1946 nodes・全体 8.6 分。bound=2000 は**前景 10 分を超過して未完**(`search/lins-twin-census-v1.g` 冒頭の実測メモ)。
**事実 3**: B₃ の帯 1000 は $[PB_3:N]\le166$ に相当($[B_3:PB_3]=6$)。

$$\Longrightarrow\ \textbf{B₃ と同じ「窓の細かさ」}([PB_4:\widetilde N]\le166)\textbf{ に並ぶには }B_4\textbf{-指数 }24\times166=\mathbf{3984}\ \textbf{が必要}.$$

これは**射程外**である(生成元が 1 本増え関係式も増えるので、同じ指数でも B₃ より探索木が大きい。B₃ で 2000 が未完である以上、4000 は論外)。ゆえに:

> ### 提案帯(**梯子方式・各段で停止規則つき**)
> | 段 | $B_4$-指数上界 | 窓側の到達 $[PB_4:\widetilde N]$ | 位置づけ |
> |---|---|---|---|
> | **R0** | **240** | $\le10$ | **timing probe**(必ず最初に単独で走らせる)。ここで 149 s を大きく超えるなら以降は中止 |
> | R1 | 480 | $\le20$ | 第 1 段 |
> | R2 | 720 | $\le30$ | 第 2 段 |
> | **R3** | **1000** | $\le41$ | **提案する現実的上限**(B₃ と同じ数値だが窓の細かさは 1/4) |
> - 各段の**壁時計予算 15 分**・超過で `TIME_CAP / STOP`(次段へ進まない)。
> - **`census_index_hi` は走行前に固定**し、後から広げない(広げるなら v2 で再登録)。B₃ 版 §1.7 の依存 D-1/D-2 をそのまま継承(**「未発見」の文言は上界つきでのみ有効**)。

#### 4.3.3 層の定義($L2$ 相当・**B₃ の §1.2 を逐語移植**)

| 層 | 述語(対の両 member) | 備考 |
|---|---|---|
| **L0-B4** | 全 twin pair($[B_4:\cdot]$ 同一・$B_4/\cdot$ 同型) | 同型判定は IdGroup 一致 → `IsomorphismGroups` |
| **L1-B4** | `in_PB4 = true` | **窓の必要条件**(2008 §1.2) |
| **L2-B4** | L1-B4 かつ **`delta2_in_N = true`** | ★ B₃ の $c\in N$ 層に対応。**ただし PSL-GEN が無いので「$\Gamma$ の商」という御利益は無い**(§4.2)⟹ この層分けの意味は「**中心荷重ゼロの層**」に限定される(系 CENTER-B4) |
| **L3-B4** | L1-B4 かつ `delta2_in_N = false` | 中心荷重が非ゼロ。B₃ の T-1 に相当する**別 gate**扱い(checker で TRUE/FALSE を付けない) |
| **混在層** | 対の両 member で `delta2_in_N` が割れる | **系 CENTER-B4 により自動的に exotic**(計算不要)⟹ §G の逐語再現 |

#### 4.3.4 IF-FIRST 予言(**走行前に固定する形・反証可能**)

> - **P-B4-1(主予言)**: 提案帯($B_4$-指数 $\le1000$)の **L1-B4 窓はすべて $PB_4/\widetilde N$ が可換** ⟹ **補題 ABEL-FIXED-B4 により全て $\iota$-固定** ⟹ **鏡映双子(M1)はゼロ**。
>   - 根拠: 窓は $[PB_4:\widetilde N]\le41$。$PB_4^{\rm ab}=\mathbf Z^6$ は小さい可換商を大量に供給する一方、$B_4$-正規性を課された非可換商が位数 $\le41$ で出るかは**未知**。⟹ **これは強い予言であり、外れたら「非可換窓が帯内に居る」= 良い知らせ**。
> - **P-B4-2**: **MIRROR-ODD の $B_4$ 版が紙で閉じる対の数 = 0**(補題 NO-PSL-B4 ⟹ エンジン不在)。**B₃ の 13/15 に対応する紙の収穫は無い。**
> - **P-B4-3**: 帯内に `delta2_in_N` 混在対が出たら、それは**計算ゼロで exotic 確定**(系 CENTER-B4)。B₃ では混在 5 対がすべて**窓の外**だった ⟹ **B₄ で混在対が窓の中に出るか**が新情報。
> - **P-B4-4(コスト)**: R0(240)の LINS 本体が **B₃ の 1000(149 s)を超える**。超えなければ帯を R3 まで上げる価値がある。
> - **停止・出力規則**: `twin_witness_prereg_iffirst_v1.md` §5.1/§6 を逐語移植(witness 無しの文言は「**登録した directed pair 群で未発見**」のみ・非存在を主張しない/S-TW-1〜7 の類型をそのまま採番し直す)。

#### 4.3.5 判定手続き(**MIRROR-ODD が無い以上、ここが主役**)

紙で閉じないので、**ORB 型の直接判定**(`theorem_check_mirrorall_l3vacuous_v1.md` §F.8 Test ORB の B₄ 版)を主経路に据える:
$$\iota(\widetilde N)=\widetilde N\iff \sigma_iN\mapsto(\sigma_iN)^{-1}\ (i=1,2,3)\ \text{が}\ \mathrm{Aut}(B_4/\widetilde N)\ \text{へ延びる}$$
(B₃ の MIRROR-PSL は $c\in N$ を使ったが、**この形は使わない** — 生成元 3 本の直接判定。証明は B₃ 版 §A.2 と同じ 3 行: $\sigma_i\mapsto\sigma_i^{-1}$ は常に準同型 $B_4\to B_4/\widetilde N$ を定め、その核が $\iota(\widetilde N)$)。
- コスト: $\lvert B_4/\widetilde N\rvert\le1000$ の群の `AutomorphismGroup` + 生成元 3 本の像照合 ⟹ 各窓 1 秒未満。
- **語レベルの安価版**(B₃ の MC-1 と同型): `canonical_id_words` に $\sigma_i\mapsto\sigma_i^{-1}$(**語の指数一斉反転・順序不変**)を適用し、置換表現で $\rho(\iota(w))\ne1$ なる $w\in\widetilde N$ を 1 本出せば $\iota(\widetilde N)\ne\widetilde N$ が**その 1 ビットで確定** ✓。第二系統(python・GAP helper 非共有)もそのまま移植できる。

---

## 5. 移植可否の総括表(**一目で分かる形**)

| B₃ 側の道具 | B₄/2008 への移植 | 根拠 |
|---|---|---|
| **MIRROR-SHADOW**($[-1,1]$ が常に shadow・$\ker=\iota(N)$) | ★ **移る**(§2・PIN 1 点) | hexagon 2 本が $B_3$ 内恒等式・pentagon は $f=1$ で自明 |
| **中心の特性論法**($c\in N$ の $\mathrm{Aut}$-不変性) | ★ **そのまま移る**(系 CENTER-B4) | $Z(B_4)=\langle\Delta_4^2\rangle$ 特性 |
| **VERBAL/可換 ⟹ $\iota$-固定** | ★ **移る・強化**(FIXED-B4・**ABEL-FIXED-B4**) | $\iota|_{PB_4^{\rm ab}}=-\mathrm{id}$ |
| **MIRROR-PSL**($U\mapsto U,W\mapsto W^{-1}$ 型の正規化) | ✗ **移らない** | PSL-GEN 不成立(NO-PSL-B4) |
| **MIRROR-ODD**(13/15 を閉じた定理) | ✗ **移らない**(期待収穫 0 対) | 同上・(A.1) の類似物なし |
| **MAP-DICT**(正則地図・chirality 辞書) | ✗ **移らない**(そのままでは) | $\Gamma=C_2\ast C_3$ を使う。$B_4$ では地図でなく**別の組合せ論的対象**(必要なら【文献要請】) |
| **ORB 型直接判定** | ★ **移る**(§4.3.5) | 群の $\mathrm{Aut}$ を直接探索するだけ・基底群に依存しない |
| **TWIN-CARD**($\lvert GT\rvert$ 差 ⟹ 両方向空) | ★ **移る見込み**(torsor 命題が 2008 groupoid でも成り立つなら) | 未検分 ⟹ §7【GAP-B4-3】 |

---

## 6. ⑤ 井原接続(2 行)

1. 2008 系は **$\widehat{GT}\cong\varprojlim ML$**(2008 Thm 3.8 p.33・`b4_original_gtshadows_extraction_v1.md` §3.3、`ihnec_v1_addendum_e_b4.md` §E-A.2.1 で 3 系統 pin 済)の**錨**である。ゆえに $B_4$ 窓の $\mathrm{GTSh}$ は $\widehat{GT}$ の**有限近似そのもの**であり、$\mathrm{gentle}$ 側($\widehat{GT}_{\rm gen}$)のような**別対象への迂回がない**。
2. $\iota$ の像 $[(-1,1)]$ は **Ihara $\mathrm{Ih}:G_{\mathbf Q}\to\widehat{GT}$ における複素共役**($\chi=-1,f=1$)。ゆえに**鏡映対 = 「複素共役で移り合う 2 窓」**であり、$\iota(\widetilde N)\ne\widetilde N$ の窓は「$\widehat{GT}$ の複素共役が有限水準で非自明に効いている場所」を名指す。⟹ **捩れ(非算術元)探索の直撃度は gentle 側より高い**が、**本経路の witness 自体は算術元である**(§2.5)ことを混同しない。

---

## 7. 【GAP】【PIN】・novelty・次の一手

### 7.1 未閉の穴

| # | 内容 | 重さ |
|---|---|---|
| **【PIN-B4-1】** | 2008 (2.25)–(2.29) が $(m,f)=(-1,1)$ で $\sigma_i\mapsto\sigma_i^{-1}$ を与えるか(§2.4)。**紙 5 分**。結論(核 $=\iota(\widetilde N)$)は内部自己同型のずれに鈍感 | 小(帰属文言のみ) |
| **【GAP-B4-1】** | $\Delta_4\sigma_i\Delta_4^{-1}=\sigma_{4-i}$ の工房内 pin(§3.2)。古典的事実だが未検算 | 小 |
| **【GAP-B4-2】** | $p_i\circ\iota=\iota\circ p_i$(紐忘却と鏡映の可換性)の代数的逐語証明。**補題 FIXED-B4 (ii) がこれに条件つき**((i) は無条件) | 中 |
| **【GAP-B4-3】** | 命題 1.5(torsor)・TWIN-CARD の 2008 groupoid 版が成り立つか(§5 の表の最終行) | 中 |
| **【GAP-B4-4】** | P-B4-1 の根拠「$[PB_4:\widetilde N]\le41$ で $B_4$-正規な非可換窓が存在するか」は**未知**。紙で詰められれば予言が定理になる | 中 |
| **【文献要請(条件付き)】** | MAP-DICT の $B_4$ 版 — 「$B_4/Z$ の有限商 + 標識づけられた生成 3 元」に対応する**組合せ論的対象(地図の一般化)と chirality 判定**があるか。**ただし §4.2 により当面は不要**(帯内に非可換窓が出て初めて要る)⟹ **今は出さない**(P-B4-1 が外れたら出す) | 保留 |

### 7.2 novelty grep(実施済・`docs/` 全域)

| 語 | 結果 |
|---|---|
| `MIRROR-SHADOW-B4` / `IOTA-B4` / `CENTER-B4` / `FIXED-B4` / `NO-PSL-B4` / `ABEL-FIXED-B4` | **0 hit**(全て本稿が初出) |
| `Out(B₄)` / `Dyer–Grossman` の $B_4$ 版 | **0 hit**(ι・DG の記述は**すべて B₃ 限定** — Explore 調査 §4 で確認) |
| `Δ₄²` / `Z(B₄)` | 既出(`b4_direct_adjudication_feasibility_v1_2.md` 付録 A.5・`hs_prop7_translation_v1.md` §1.5)。**$\iota$ との接続は未出** |
| `𝒱(PB₄)` verbal ⟹ 特性 | 既出(同 §2.5 定理 B4-CANON・`b4_theorem_check_v1.md` §3.1)。**「ゆえに $\iota$-固定・双子になれない」は未出** |
| B₄ の LINS / 双子 census | **実績ゼロ**(既存 LINS は全て B₃)⟹ §4.3 は完全な新設計 |

---

# 8. 追補 v1.1(2026-08-06)— 【PIN-B4-1】**閉**(原文逐語)

**参照**: `papers/txt/2008.00066-what-are-gt-shadows.txt`(既在・**canon 内**。新規取り寄せゼロ)。Cor 2.7 直後の **(2.25)(2.26)** を逐語で取得した。

> **(2.25)**(原文逐語・記号を本稿の書式に直しただけ)
> $$T^{B_4}_{m,f}(\sigma_1):=\sigma_1x_{12}^m\,N,\qquad
> T^{B_4}_{m,f}(\sigma_2):=\varphi_{123}(f)^{-1}\bigl(\sigma_2x_{23}^m\bigr)\varphi_{123}(f)\,N,\qquad
> T^{B_4}_{m,f}(\sigma_3):=\varphi_{12,3,4}(f)^{-1}\bigl(\sigma_3x_{34}^m\bigr)\varphi_{12,3,4}(f)\,N.$$
> **(2.26)** $\ T^{B_3}_{m,f}(\sigma_1):=\sigma_1x_{12}^m\,N_{PB_3},\qquad T^{B_3}_{m,f}(\sigma_2):=f^{-1}\bigl(\sigma_2x_{23}^m\bigr)f\,N_{PB_3}$;
> **$B_2$**: $\ \sigma_1\mapsto\sigma_1x_{12}^m\,N_{PB_2}$。
> ((2.23)(2.24) は $T^{B_n}_{m,f}(g):=ou\circ T_{m,f}\circ\mathfrak m(g)$ とその $PB_n$ への制限。(2.27) は $ou$ の乗法性であって $T$ の式ではない — v1 の式番号列挙 (2.25)–(2.29) のうち**実際に生成元の像を与えるのは (2.25)(2.26) と $B_2$ の 1 行**である。)

### 8.1 $(m,f)=(-1,1)$ での特殊化(**期待どおり・ずれゼロ**)

$f=1$ ゆえ $\varphi_{123}(1)=\varphi_{12,3,4}(1)=1$(各 $\varphi$ は群準同型)。$x_{i,i+1}=\sigma_i^2$((A.2))を使うと

$$T^{B_4}_{-1,1}(\sigma_i)=\sigma_i x_{i,i+1}^{-1}N=\sigma_i\sigma_i^{-2}N=\boxed{\ \sigma_i^{-1}N\ }\qquad(i=1,2,3)$$

$$\Longrightarrow\quad \boxed{\ T^{B_4}_{-1,1}=\pi_N\circ\iota\ \ \textbf{(内部自己同型のずれ無しの厳密等式)}\ }$$

同様に $T^{B_3}_{-1,1}(\sigma_i)=\sigma_i^{-1}$、$T^{B_2}_{-1,1}(\sigma_1)=\sigma_1^{-1}$ ✓。

### 8.2 帰結(補題 MIRROR-SHADOW-B4 が**完全に確定**)

1. **核**: $\ker T^{B_4}_{-1,1}=\iota^{-1}(N)=\iota(N)$($\iota^2=\mathrm{id}$)。$N\le PB_4$ かつ $\iota(PB_4)=PB_4$ より $\iota(N)\le PB_4$ ⟹ $\ker T^{PB_4}_{-1,1}=\ker T^{B_4}_{-1,1}\cap PB_4=\iota(N)$ ✓((2.51) の source-kernel はこれ)。
2. **全射性(Def 2.9 の 3 本)**: $T^{PB_n}_{-1,1}=\pi\circ\iota|_{PB_n}$ で $\iota(PB_n)=PB_n$ ⟹ $n=2,3,4$ すべてで全射 ✓。
3. **friendly/charming**: $2m+1=-1$ は単元 ✓ (2.36);$f=1\in[F_2,F_2]$ ✓;(2.61) の $T^{F_2}_{-1,1}$ は $\iota(F_2)=F_2$($\iota(\sigma_i^2)=\sigma_i^{-2}$)より全射 ✓。
4. §2.2 の hexagon 2 本(**$B_3$ 内恒等式**)+ §2.3 の pentagon(自明)と合わせて
$$\boxed{\ \textbf{補題 MIRROR-SHADOW-B4 は確定(candidate → 紙で完備)。}\ \ker T^{PB_4}_{-1,1}=\iota(\widetilde N)\ }$$

> ### ★ v1 の留保の後始末(委嘱の指示どおり明記)
> v1 §2.4 では「$\sigma_3$ の像に別の共役子が付く場合、$T$ は $\pi\circ\iota\circ\mathrm{Inn}(u)$ 型になり **核は $\iota(\widetilde N)$ のまま**(内部自己同型は正規部分群を動かさない)だが帰属の文言だけ書き換えが要る」と留保していた。
> **原文確認の結果、その場合分けは起きなかった**($f=1$ が両方の共役子を殺す)。⟹ **v1 の主張は文言も含めてそのまま有効**。留保は「壊れても帰属文言のみ」という**事前の見積りが正しかった**ことの記録として残す。

---

# 9. 追補 v1.1 — 【GAP-B4-2】**閉**($p_i\circ\iota=\iota\circ p_i$ を生成元べったりで)

**記号**: $p_i:PB_4\to PB_3$ = 第 $i$ 紐忘却(`b4_direct_adjudication_feasibility_v1_2.md` §2.2 の $p_i$)。生成元上は
$$p_i(x_{jk})=\begin{cases}1&i\in\{j,k\}\\ x_{\hat j\hat k}&i\notin\{j,k\}\end{cases}\qquad(\hat j:=j-[j>i])$$
$PB_3$ の生成元は $x_{12},x_{13},x_{23}$。$PB_4$ の生成元は $x_{12},x_{13},x_{14},x_{23},x_{24},x_{34}$。

### 9.1 準備 — $\iota$ の $x_{jk}$ 上の像(**6 本すべて $x$ 語で明示**)

(A.2) より $x_{12}=\sigma_1^2$, $x_{23}=\sigma_2^2$, $x_{34}=\sigma_3^2$, $x_{13}=\sigma_2\sigma_1^2\sigma_2^{-1}=\sigma_2x_{12}\sigma_2^{-1}$, $x_{24}=\sigma_3x_{23}\sigma_3^{-1}$, $x_{14}=\sigma_3x_{13}\sigma_3^{-1}$。
補助等式(初等・$\sigma_j^{-1}A\sigma_j=\sigma_j^{-2}(\sigma_jA\sigma_j^{-1})\sigma_j^{2}$ と $\sigma_j^2=x_{j,j+1}$ のみ):
$$\sigma_2^{-1}x_{12}\sigma_2=x_{23}^{-1}x_{13}x_{23},\qquad \sigma_3^{-1}x_{23}\sigma_3=x_{34}^{-1}x_{24}x_{34},\qquad \sigma_3^{-1}x_{13}\sigma_3=x_{34}^{-1}x_{14}x_{34}.$$

> ### 補題 IOTA-GEN(candidate・本稿)
> $$\boxed{\begin{aligned}
> \iota(x_{12})&=x_{12}^{-1}, &\iota(x_{23})&=x_{23}^{-1}, &\iota(x_{34})&=x_{34}^{-1},\\
> \iota(x_{13})&=x_{23}^{-1}x_{13}^{-1}x_{23}, &\iota(x_{24})&=x_{34}^{-1}x_{24}^{-1}x_{34}, &\iota(x_{14})&=x_{34}^{-1}x_{24}^{-1}\,x_{14}^{-1}\,x_{24}x_{34}.
> \end{aligned}}$$

**証明.** $\iota(\sigma_j^2)=\sigma_j^{-2}$ で 3 本は即。
$\iota(x_{13})=\iota(\sigma_2\sigma_1^2\sigma_2^{-1})=\sigma_2^{-1}\sigma_1^{-2}\sigma_2=(\sigma_2^{-1}x_{12}\sigma_2)^{-1}=(x_{23}^{-1}x_{13}x_{23})^{-1}=x_{23}^{-1}x_{13}^{-1}x_{23}$ ✓。
$\iota(x_{24})$ は添字を 1 つずらして同型 ✓。
$\iota(x_{14})=\iota(\sigma_3x_{13}\sigma_3^{-1})=\sigma_3^{-1}\iota(x_{13})\sigma_3=\sigma_3^{-1}\bigl(x_{23}^{-1}x_{13}^{-1}x_{23}\bigr)\sigma_3
=(x_{34}^{-1}x_{24}^{-1}x_{34})(x_{34}^{-1}x_{14}^{-1}x_{34})(x_{34}^{-1}x_{24}x_{34})=x_{34}^{-1}x_{24}^{-1}x_{14}^{-1}x_{24}x_{34}$ ✓。∎
(**二重検算**: $\iota(x_{jk})=g_{jk}x_{jk}^{-1}g_{jk}^{-1}$、$g_{jk}=\iota(w_{jk})w_{jk}^{-1}$、$w_{jk}=\sigma_{k-1}\cdots\sigma_{j+1}$ という一般形からも同じ値 — $g_{13}=\sigma_2^{-2}=x_{23}^{-1}$、$g_{24}=x_{34}^{-1}$、$g_{14}=\sigma_3^{-1}\sigma_2^{-2}\sigma_3^{-1}=x_{34}^{-1}x_{24}^{-1}$ ✓。$g_{jk}$ は $\iota$ が置換に恒等作用するので**常に純**であり、$x$ 語で書ける。)

### 9.2 24 個の照合(**全生成元 × 全 $p_i$**)

$p_i$ の生成元への作用($\hat{\ }$ は削除後の番号詰め):

| | $x_{12}$ | $x_{13}$ | $x_{14}$ | $x_{23}$ | $x_{24}$ | $x_{34}$ |
|---|---|---|---|---|---|---|
| $p_1$ | 1 | 1 | 1 | $x_{12}$ | $x_{13}$ | $x_{23}$ |
| $p_2$ | 1 | $x_{12}$ | $x_{13}$ | 1 | 1 | $x_{23}$ |
| $p_3$ | $x_{12}$ | 1 | $x_{13}$ | 1 | $x_{23}$ | 1 |
| $p_4$ | $x_{12}$ | $x_{13}$ | 1 | $x_{23}$ | 1 | 1 |

$PB_3$ 側の $\iota$ は同じ形($\iota(x_{12})=x_{12}^{-1}$, $\iota(x_{23})=x_{23}^{-1}$, $\iota(x_{13})=x_{23}^{-1}x_{13}^{-1}x_{23}$)。以下 **左辺 $=p_i(\iota(x))$・右辺 $=\iota(p_i(x))$**。

**$p_4$**: $x_{12}\!:x_{12}^{-1}=x_{12}^{-1}$ ✓ / $x_{23}\!:x_{23}^{-1}=x_{23}^{-1}$ ✓ / $x_{13}\!:x_{23}^{-1}x_{13}^{-1}x_{23}=\iota(x_{13})$ ✓ / $x_{34},x_{24},x_{14}$: 左辺は $p_4$ が $x_{34},x_{24},x_{14}$ を全て 1 に送るので $1$、右辺 $\iota(1)=1$ ✓(3 本)。

**$p_3$**: $x_{12}\!:x_{12}^{-1}$ ✓ / $x_{13}\!:p_3(x_{23}^{-1}x_{13}^{-1}x_{23})=1\cdot1\cdot1=1=\iota(1)$ ✓ / $x_{23},x_{34}\!:1=1$ ✓ / $x_{24}\!:p_3(x_{34}^{-1}x_{24}^{-1}x_{34})=1\cdot x_{23}^{-1}\cdot1=x_{23}^{-1}=\iota(x_{23})$ ✓ / **$x_{14}$**: $p_3(x_{34}^{-1}x_{24}^{-1}x_{14}^{-1}x_{24}x_{34})=1\cdot x_{23}^{-1}\cdot x_{13}^{-1}\cdot x_{23}\cdot1=x_{23}^{-1}x_{13}^{-1}x_{23}=\iota(x_{13})=\iota(p_3(x_{14}))$ ✓★

**$p_2$**: $x_{12},x_{23}\!:1=1$ ✓ / $x_{24}\!:p_2(x_{34}^{-1}x_{24}^{-1}x_{34})=x_{23}^{-1}\cdot1\cdot x_{23}=1=\iota(1)$ ✓ / $x_{34}\!:x_{23}^{-1}=\iota(x_{23})$ ✓ / $x_{13}\!:p_2(x_{23}^{-1}x_{13}^{-1}x_{23})=1\cdot x_{12}^{-1}\cdot1=x_{12}^{-1}=\iota(x_{12})$ ✓ / **$x_{14}$**: $x_{23}^{-1}\cdot1\cdot x_{13}^{-1}\cdot1\cdot x_{23}=x_{23}^{-1}x_{13}^{-1}x_{23}=\iota(x_{13})$ ✓★

**$p_1$**: $x_{12}\!:1=1$ ✓ / $x_{13}\!:p_1(x_{23}^{-1}x_{13}^{-1}x_{23})=x_{12}^{-1}\cdot1\cdot x_{12}=1$ ✓ / $x_{14}\!:p_1(x_{34}^{-1}x_{24}^{-1}x_{14}^{-1}x_{24}x_{34})=x_{23}^{-1}x_{13}^{-1}\cdot1\cdot x_{13}x_{23}=1$ ✓ / $x_{23}\!:x_{12}^{-1}=\iota(x_{12})$ ✓ / $x_{34}\!:x_{23}^{-1}=\iota(x_{23})$ ✓ / $x_{24}\!:p_1(x_{34}^{-1}x_{24}^{-1}x_{34})=x_{23}^{-1}x_{13}^{-1}x_{23}=\iota(x_{13})$ ✓★

> ### 補題 FORGET-IOTA(candidate・本稿。**24/24 一致**)
> $$\boxed{\ p_i\circ\iota=\iota\circ p_i\quad\text{on }PB_4\qquad(i=1,2,3,4)\ \textbf{— 厳密等式(内部補正なし)}\ }$$
> **証明.** 両辺は $PB_4\to PB_3$ の準同型であり、6 生成元 × 4 写像 = **24 点すべてで一致**(上表)。∎

### 9.3 帰結 — 補題 FIXED-B4 の**無条件化**

$N=\mathcal V(F_2)\times\langle c\rangle$ は $\iota$-不変($\mathcal V(F_2)$ は verbal で $\iota(F_2)=F_2$、$\iota(c)=c^{-1}$)。補題 FORGET-IOTA より
$$\iota\bigl(p_i^{-1}(N)\bigr)=p_i^{-1}\bigl(\iota(N)\bigr)=p_i^{-1}(N)\quad(\forall i)\ \Longrightarrow\ \iota(\ker\widetilde\psi)=\ker\widetilde\psi
\ \Longrightarrow\ \iota(\widetilde N_{\rm core})=\mathrm{core}_{B_4}\bigl(\iota(\ker\widetilde\psi)\bigr)=\widetilde N_{\rm core}.$$
$$\boxed{\ \textbf{補題 FIXED-B4 は (i)(ii) とも無条件で成立}\ \Longrightarrow\ \textbf{現用 B₄ 窓 2 本はともに }\iota\textbf{-固定}\ }$$
⟹ **現用窓では鏡映線は構造的に空**であり、$[(-1,1)]$ は両窓で settled。**新しい窓層(§4.3 の census)が鏡映線の唯一の入口である**ことが確定した。

> ### ★ 副産物(B₃ 側にも効く)
> 補題 IOTA-GEN の $\iota(x_{13})=x_{23}^{-1}x_{13}^{-1}x_{23}$ は **$PB_3$ 内の等式でもある**。B₃ 線の $\iota$ は $F_2=\langle x_{12},x_{23}\rangle$ 上では $x\mapsto x^{-1},y\mapsto y^{-1}$ と簡単だが、**第 3 の生成元 $x_{13}$ では共役子 $x_{23}$ が付く**。$z=(xy)^{-1}$ と $x_{13}$ の関係を扱う場面(定義ノート §1.5.2 の $\tau$ 周り)で**符号だけでなく共役子を落とさない**こと。⟹ 規約台帳への注記候補。

### 9.4 v1.1 で閉じた穴・残る穴

| # | 状態 |
|---|---|
| **【PIN-B4-1】** | **閉**(§8。原文 (2.25)(2.26) 逐語 ⟹ $T_{-1,1}=\pi\circ\iota$ 厳密。留保していた場合分けは発生せず) |
| **【GAP-B4-2】** | **閉**(§9。24/24 の生成元照合 ⟹ 厳密可換。補題 FIXED-B4 無条件化) |
| 【GAP-B4-1】 | **閉**(v1.2 §11 補題 FLIP-INNER。3 本を 1 行ずつ・$\Delta_4^2$ 中心性も紙で再現) |
| 【GAP-B4-3】 | **閉**(v1.2 §12。移植は (S2) 1 点に集約 ⟹ 補題 SOURCE-OBJ-B4。写らない段 (C1)–(C5) 明示) |
| 【GAP-B4-4】 | **部分閉**(v1.2 §13。非可換窓は $[B_4:\widetilde N]\ge192$・$\lvert Q
vert\in\{6,10\}$ 型を排除。完全解決は R0 実測) |

---

# 11. 追補 v1.2(2026-08-06・裁定 631)— 【GAP-B4-1】**閉**(flip = $\mathrm{Ad}(\Delta_4)$)

**道具は 3 本だけ**(すべて braid 関係のみから):

> **(D1)** $aba=bab\ \Longrightarrow\ aba^{-1}=b^{-1}ab$。
> **(D2)** $\delta:=\sigma_1\sigma_2\sigma_3$ に対し $\ \delta\sigma_1\delta^{-1}=\sigma_2,\quad \delta\sigma_2\delta^{-1}=\sigma_3$。
> **(D2′)** $\delta'':=\sigma_3\sigma_2\sigma_1$ に対し $\ \delta''\sigma_2\delta''^{-1}=\sigma_1$。
> **(D3)** $\Delta_3=\sigma_1\sigma_2\sigma_1$ は $\langle\sigma_1,\sigma_2\rangle$ 内で $\sigma_1\leftrightarrow\sigma_2$;$\Delta_3''=\sigma_2\sigma_3\sigma_2$ は $\langle\sigma_2,\sigma_3\rangle$ 内で $\sigma_2\leftrightarrow\sigma_3$($B_3$ の既知事実・工房既在 `bu_s35_embedding_v1.md` §1)。

**(D2) の検算**: $\delta\sigma_1\delta^{-1}=\sigma_1\sigma_2(\sigma_3\sigma_1\sigma_3^{-1})\sigma_2^{-1}\sigma_1^{-1}=\sigma_1\sigma_2\sigma_1\sigma_2^{-1}\sigma_1^{-1}\overset{\rm braid}{=}\sigma_2\sigma_1\sigma_2\sigma_2^{-1}\sigma_1^{-1}=\sigma_2$ ✓(遠可換 $\sigma_1\sigma_3=\sigma_3\sigma_1$)。
$\delta\sigma_2\delta^{-1}=\sigma_1\sigma_2(\sigma_3\sigma_2\sigma_3^{-1})\sigma_2^{-1}\sigma_1^{-1}\overset{\rm (D1)}{=}\sigma_1\sigma_2(\sigma_2^{-1}\sigma_3\sigma_2)\sigma_2^{-1}\sigma_1^{-1}=\sigma_1\sigma_3\sigma_1^{-1}=\sigma_3$ ✓。
**(D2′) の検算**: $\delta''\sigma_2\delta''^{-1}=\sigma_3(\sigma_2\sigma_1\sigma_2)\sigma_1^{-1}\sigma_2^{-1}\sigma_3^{-1}\overset{\rm braid}{=}\sigma_3(\sigma_1\sigma_2\sigma_1)\sigma_1^{-1}\sigma_2^{-1}\sigma_3^{-1}=\sigma_3\sigma_1\sigma_3^{-1}=\sigma_1$ ✓。

**2 つの分解(どちらも braid 関係で書き下せる)**:
$$\Delta_4=\sigma_1\sigma_2\sigma_3\sigma_1\sigma_2\sigma_1=\underbrace{(\sigma_1\sigma_2\sigma_3)}_{\delta}\underbrace{(\sigma_1\sigma_2\sigma_1)}_{\Delta_3}
=\underbrace{(\sigma_3\sigma_2\sigma_1)}_{\delta''}\underbrace{(\sigma_2\sigma_3\sigma_2)}_{\Delta_3''}.$$
**第 2 分解の検算**: $\sigma_3\sigma_2\sigma_1\sigma_2\sigma_3\sigma_2\overset{\rm braid}{=}\sigma_3\sigma_1\sigma_2\sigma_1\sigma_3\sigma_2\overset{\rm 遠可換}{=}\sigma_1\sigma_3\sigma_2\sigma_3\sigma_1\sigma_2\overset{\rm braid}{=}\sigma_1\sigma_2\sigma_3\sigma_2\sigma_1\sigma_2\overset{\rm braid}{=}\sigma_1\sigma_2\sigma_3\sigma_1\sigma_2\sigma_1=\Delta_4$ ✓。

> ### 補題 FLIP-INNER(candidate・本稿)
> $$\boxed{\ \Delta_4\sigma_1\Delta_4^{-1}=\sigma_3,\qquad \Delta_4\sigma_2\Delta_4^{-1}=\sigma_2,\qquad \Delta_4\sigma_3\Delta_4^{-1}=\sigma_1\ }$$
> すなわち flip $\phi:\sigma_i\mapsto\sigma_{4-i}$ は**内部自己同型** $\mathrm{Ad}(\Delta_4)$ である。

**証明(3 本とも 1 行)**。
$$\Delta_4\sigma_1=\delta\Delta_3\sigma_1=\delta(\Delta_3\sigma_1\Delta_3^{-1})\Delta_3\overset{\rm(D3)}{=}\delta\sigma_2\Delta_3=(\delta\sigma_2\delta^{-1})\delta\Delta_3\overset{\rm(D2)}{=}\sigma_3\Delta_4 .$$
$$\Delta_4\sigma_2=\delta\Delta_3\sigma_2=\delta(\Delta_3\sigma_2\Delta_3^{-1})\Delta_3\overset{\rm(D3)}{=}\delta\sigma_1\Delta_3=(\delta\sigma_1\delta^{-1})\delta\Delta_3\overset{\rm(D2)}{=}\sigma_2\Delta_4 .$$
$$\Delta_4\sigma_3=\delta''\Delta_3''\sigma_3=\delta''(\Delta_3''\sigma_3\Delta_3''^{-1})\Delta_3''\overset{\rm(D3)}{=}\delta''\sigma_2\Delta_3''=(\delta''\sigma_2\delta''^{-1})\delta''\Delta_3''\overset{\rm(D2')}{=}\sigma_1\Delta_4 .\qquad\blacksquare$$

> ### 系(**無料**)
> $\mathrm{Ad}(\Delta_4)^2=\mathrm{Ad}(\Delta_4^2)$ は生成元上恒等 ⟹ **$\Delta_4^2\in Z(B_4)$**(工房既在の機械検算 `付録 A.5` を**紙で再現**)。また $\phi$ は $\mathrm{Out}(B_4)$ に寄与しない ⟹ §3 の在庫台帳が**無条件で確定**。

---

# 12. 追補 v1.2 — 【GAP-B4-3】torsor / TWIN-CARD の 2008 版

### 12.1 何が要るか(B₃ 版の証明を段ごとに分解)

B₃ 版(`twin_witness_prereg_iffirst_v1.md` §4.2・`wall_design_audit_v1.md` §1.5)は次の 4 段でできている:
**(S1)** 射はすべて可逆(groupoid)/ **(S2)** 各 shadow の**source kernel が再び対象**である/ **(S3)** $GT(N)=\bigsqcup_{K}\mathrm{Hom}(K,N)$ かつ各非空 $\mathrm{Hom}(K,N)$ は $G_N:=\mathrm{Hom}(N,N)$ の**torsor**/ **(S4)** $\mathrm{Hom}(K,N)\ne\emptyset$ なら $G_N\cong G_K$ かつ連結成分が一致。

**(S1)** は 2008 では**定義から**: (2.51) は $\mathrm{Hom}(\widetilde K,\widetilde N):=\mathrm{Isom}\bigl(\mathrm{PaB}^{\le4}/\!\sim_{\widetilde K},\ \mathrm{PaB}^{\le4}/\!\sim_{\widetilde N}\bigr)$ と**同型の集合**として定義される ✓。
**(S3)(S4)** は**純粋な groupoid の組合せ論**であり、基底群にも pentagon にも依存しない ✓(合成 (2.52) が群oid 則を満たすことだけを使う)。
⟹ **移植の可否は (S2) ただ 1 点に集約される。**

### 12.2 (S2) の 2008 版 — **紙で閉じる**

> ### 補題 SOURCE-OBJ-B4(candidate・本稿)
> 任意の GT-shadow $[(m,f)]\in GT(\widetilde N)$ に対し
> $$\ker T^{B_4}_{m,f}\ \in\ \mathrm{NFI}_{PB_4}(B_4),\qquad \ker T^{PB_4}_{m,f}=\ker T^{B_4}_{m,f}.$$

**証明.** $\widetilde N\le PB_4$ ゆえ $B_4/\widetilde N\twoheadrightarrow B_4/PB_4=S_4$ が定まる。(2.25) より $T^{B_4}_{m,f}(\sigma_i)=\varphi_*(f)^{-1}(\sigma_ix_{\bullet}^m)\varphi_*(f)\widetilde N$ であり、$x_\bullet$ と $\varphi_*(f)$ は**すべて純**($\in PB_4$)⟹ $S_4$ への合成は $\sigma_i\mapsto s_i$、すなわち**標準射影 $B_4\twoheadrightarrow S_4$ に一致**する。ゆえに
$$\ker T^{B_4}_{m,f}\subseteq\ker(B_4\to S_4)=PB_4 .$$
$\ker$ は正規、像は有限($B_4/\widetilde N$ が有限)⟹ 有限指数 ⟹ $\mathrm{NFI}_{PB_4}(B_4)$ の元 ✓。最後の等式は $\ker T^{B_4}\subseteq PB_4$ から。∎

### 12.3 帰結

> ### 命題 TORSOR-B4 / 系 TWIN-CARD-B4(candidate・本稿)
> $\heartsuit$ 層(charming・2008 Prop 2.22 の部分 groupoid $\mathrm{GTSh}^\heartsuit$)で
> $$\lvert GT^\heartsuit(\widetilde N)\rvert=\lvert G_{\widetilde N}\rvert\cdot\#\{\widetilde K:\mathrm{GTSh}^\heartsuit(\widetilde K,\widetilde N)\ne\emptyset\},$$
> $$\boxed{\ \mathrm{GTSh}^\heartsuit(\widetilde K,\widetilde N)\ne\emptyset\ \Longrightarrow\ \lvert GT^\heartsuit(\widetilde N)\rvert=\lvert GT^\heartsuit(\widetilde K)\rvert\ }$$
> **⟹ $\lvert GT^\heartsuit(\widetilde N)\rvert\ne\lvert GT^\heartsuit(\widetilde K)\rvert$ は「両方向とも空」の証明**(B₃ 版 §4.2 の表がそのまま使える)。

**証明.** (S1)(S2) より $GT^\heartsuit(\widetilde N)$ は source kernel で類別され、各非空クラスは $\psi\mapsto\psi\circ\varphi$ で $G_{\widetilde N}$ と全単射(groupoid ⟹ 可逆)。$\varphi\in\mathrm{Hom}(\widetilde K,\widetilde N)$ による共役が $G_{\widetilde N}\cong G_{\widetilde K}$ を与え、連結成分は共通。有限性は $(m,f)\in\mathbf Z/N_{\rm ord}\times PB_3/\widetilde N_{PB_3}$ が有限集合であることから ✓。∎

### 12.4 ★ **写らない/注意が要る段**(委嘱の「明示せよ」)

| # | 事項 | 扱い |
|---|---|---|
| **(C1)** | **$\heartsuit$ を外した $GT(\widetilde N)$ 全体では torsor を主張しない。** 合成 (2.52) が閉じ・逆射が存在するのは 2008 Prop 2.22 の $\mathrm{GTSh}^\heartsuit$ において保証される | **$\heartsuit$ 層に限定して述べる**(B₃ 版も同じ制限) |
| **(C2)** | **濃度を B₃-gentle 側と混ぜてはならない。** 2008 の $GT(\widetilde N)$ は $\mathbf Z/N_{\rm ord}\times PB_3/\widetilde N_{PB_3}$ 上の類であり、$\widetilde N_{PB_3}$ は **(2.4) の 5 重逆像交わり**。gentle 側の $GT(N)$ とは**同名別物** | 数値の横断比較を禁止(既在の「同名別物」規律) |
| **(C3)** | **source/target の向き**: (2.51) は source $=\ker$。B₃ 版と**同じ向き**だが、cert には必ず `(target_window, source_kernel)` の順序つきで書く | 逐語移植 |
| **(C4)** | 「$\lvert GT\rvert$ 差 ⟹ witness 不在」の**逆は言えない**(等しくても無情報) | B₃ 版 §4.2 の表を逐語移植 |
| **(C5)** | (S2) の証明は **(2.25) の共役子 $\varphi_*(f)$ が純である**ことに依存する。$f\in PB_3/\widetilde N_{PB_3}$ ゆえ $\varphi_*(f)\in PB_4$ ✓(2008 の $\varphi$ は operad の cabling で $PB$ を $PB$ に送る) | 依存として明記 |

---

# 13. 追補 v1.2 — 【GAP-B4-4】P-B4-1 の紙化(**部分的に成功・下界を確定**)

### 13.1 算術(確定)

窓 $\widetilde N$ は $\widetilde N\le PB_4$、$[B_4:PB_4]=24$ ⟹
$$[B_4:\widetilde N]=24\cdot[PB_4:\widetilde N]\quad\Longrightarrow\quad [B_4:\widetilde N]\le1000\iff \lvert Q\rvert:=[PB_4:\widetilde N]\le41 .$$
また $\widetilde N\trianglelefteq B_4$ より **$S_4=B_4/PB_4$ が $Q:=PB_4/\widetilde N$ に自己同型として作用**し、$B_4\to\mathrm{Aut}(Q)$ の $PB_4$ への制限は $\mathrm{Inn}(Q)$。

### 13.2 3 本の紙の道具

$a_{ij}:=x_{ij}\widetilde N\in Q$($1\le i<j\le4$、6 個)と置く。

> **(T1) 同位数**: $S_4$ は 6 個の対 $\{i,j\}$ に**推移的**に作用し、$B_4$-共役は $x_{ij}$ を $x_{s(i)s(j)}$ の共役へ送る ⟹ **6 個の $a_{ij}$ はすべて同じ位数**(自己同型は位数を保つ)。
> **(T2) 遠可換**: $\{i,j\}\cap\{k,l\}=\emptyset$ ⟹ $[x_{ij},x_{kl}]=1$(既在: 付録 A.5 の $[x_{14},x_{23}]=1$ 等)⟹ $[a_{12},a_{34}]=[a_{13},a_{24}]=[a_{14},a_{23}]=1$。
> **(T3) 三角の中心**: 各三つ組 $\{i,j,k\}$ に対し $\langle x_{ij},x_{ik},x_{jk}\rangle\cong PB_3$ で、その中心生成元は $c_{ijk}=x_{ij}x_{ik}x_{jk}$(順序は (A.5) の巡回形)⟹
> $$T_{ijk}:=\langle a_{ij},a_{ik},a_{jk}\rangle\ \ni\ a_{ij}a_{ik}a_{jk}\in Z(T_{ijk}).$$

> ### 補題 TRI-ABEL(candidate・本稿)
> $$\boxed{\ Q\ \text{が非可換}\iff \text{ある三つ組 }\{i,j,k\}\text{ で }T_{ijk}\text{ が非可換}\ }$$
> **証明.** 2 つの対はいずれか: (a) 交わらない ⟹ (T2) で可換、(b) 添字を共有 ⟹ 共通の三つ組に属する。全三角が可換なら全生成元対が可換 ⟹ $Q$ 可換。逆は自明。∎

### 13.3 下界の確定

> ### 命題 NO-SMALL-NONAB(candidate・本稿)
> $Q$ は **$S_3$(位数 6)にも $D_5$(位数 10)にもなりえない**。より一般に:
> $$\boxed{\ Z(Q)=1\ \wedge\ \text{全 }a_{ij}\text{ が位数 }2\ \wedge\ Q\ \text{が符号指標 }\varepsilon:Q\to\{\pm1\},\ \varepsilon(a_{ij})=-1\ \text{をもつ}\ \Longrightarrow\ \text{矛盾}\ }$$

**証明.** (T1) より全 $a_{ij}$ は同位数 $d$。$d=1$ なら $Q=1$。
**$Q=S_3$**: $d=3$ なら全 $a_{ij}\in A_3$ ⟹ $Q\le C_3$ ✗。ゆえに $d=2$(互換)。三つ組 $\{1,2,3\}$ で $T=T_{123}=\langle a_{12},a_{13},a_{23}\rangle$ は互換で生成される部分群 ⟹ $T=S_3$ か $T=C_2$。
 - $T=S_3$: $Z(S_3)=1$ と (T3) より $a_{12}a_{13}a_{23}=1$。しかし符号 $\mathrm{sgn}$ で見ると $(-1)^3=-1\ne+1$ ✗。
 - $T=C_2$: $a_{12}=a_{13}=a_{23}$。これが**全 4 三つ組**で起きると三つ組が添字を共有して連結ゆえ 6 個すべてが等しく $Q=C_2$ ✗($Q=S_3$ に矛盾)。よってどれかの三つ組で $T=S_3$ ⟹ 上の矛盾。∎
**$Q=D_5$**(位数 10): 位数 5 の元だけでは $Q\le C_5$ ✗ ⟹ $d=2$(鏡映)。$T_{ijk}$ は鏡映生成 ⟹ $D_5$ か $C_2$。$Z(D_5)=1$ ⟹ 積 $=1$、しかし符号指標($D_5\to\{\pm1\}$、鏡映 $\mapsto-1$)で $-1\ne1$ ✗。$C_2$ 側は同上で $Q=C_2$ ✗。∎
(同じ論法で **奇数 $n$ の二面体群 $D_n$(位数 $6,10,14,18,22,26,34,38$)と一般二面体群 $\mathrm{Dih}(C_3^2)$(位数 18)は全て排除**される — いずれも中心自明・involution 生成・符号指標をもつ。)

> ### 系 INDEX-LB(**帯設計への直接の帰結**)
> $$\boxed{\ \textbf{非可換な窓が存在するなら }\lvert Q\rvert\ge8,\ \text{すなわち }[B_4:\widetilde N]\ \ge\ 24\times8=\mathbf{192}\ }$$
> (位数 6 は排除済・7 以下の非可換群は存在しない。)

### 13.4 P-B4-1 の格の訂正(**正直な結論**)

- **紙で言えること**: 非可換窓は $[B_4:\widetilde N]\ge192$。$\lvert Q\rvert\in\{6,10\}$ とその親戚(奇二面体・一般二面体)は**排除**。
- **紙で言えないこと**: $\lvert Q\rvert=8$($D_4$/$Q_8$)・$12$($A_4$ 等)・$16,20,21,24,27,\dots\le41$ の**排除は未達**。実際 $Q_8$ は (T1)(T2)(T3) をすべて通過する(遠可換 ⟹ $a_{34}=a_{12}^{\pm1}$ 等、三角積は $\pm1\in Z(Q_8)$ で矛盾なし)。
- ⟹ $$\boxed{\ \textbf{P-B4-1 は「定理」ではなく「部分的支持つき予想」へ格下げ}\ }$$ 予言の文言を「帯内の窓は**すべて**可換」から「**非可換窓があるとすれば $[B_4:\widetilde N]\in[192,1000]$ かつ $\lvert Q\rvert\in\{8,12,16,\dots\}$ に限る**」へ**強化・限定**する(反証可能性は上がる)。
- ★ **設計の追認**: 最初の rung **R0 = 240** は $\lvert Q\rvert\le10$ を覆う。命題 NO-SMALL-NONAB により $\lvert Q\rvert\in\{6,10\}$ は紙で消えているので、**R0 が実際に検定するのは $\lvert Q\rvert=8$(B₄-指数 192)ちょうど 1 点**である。⟹ **R0 は「最小の非可換窓が存在するか」を単一の的に絞った実験**になっており、帯の選び方が結果的に最適だった。

### 13.5 v1.2 で閉じた穴

| # | 状態 |
|---|---|
| **【GAP-B4-1】** | **閉**(§11。3 本 1 行ずつ・$\Delta_4^2$ 中心性も紙で再現) |
| **【GAP-B4-3】** | **閉**(§12。移植は (S2) 1 点に集約 ⟹ 補題 SOURCE-OBJ-B4 で解決。写らない段 (C1)–(C5) を明示) |
| **【GAP-B4-4】** | **部分閉**(§13。下界 $[B_4:\widetilde N]\ge192$ を確定・$\lvert Q\rvert\in\{6,10\}$ 型を排除。**完全解決は R0 実測**) |

# 10. 次の一手(**優先順・司令塔裁定用**・v1.2 で更新)

1. ~~【PIN-B4-1】~~ ⟹ **v1.1 §8 で閉**(原文 (2.25)(2.26) 逐語・$T_{-1,1}=\pi\circ\iota$ 厳密)。
2. ~~【GAP-B4-2】~~ ⟹ **v1.1 §9 で閉**(24/24 生成元照合・厳密可換)。**補題 FIXED-B4 が無条件化**し、「現用窓では鏡映線が空」が確定 ⟹ **新窓層の必要性が正式な動機になった**。
3. **R0(240)の timing probe のみ**を便 112 認可後に走らせ、P-B4-4 を判定。**そこで初めて帯を決める**(先に帯を固定して走らせない)。← **現在の唯一の実行待ち**
4. **P-B4-1 が外れた場合のみ**、MAP-DICT の B₄ 版の【文献要請】を起票。
5. ~~【GAP-B4-1】~~ ⟹ **v1.2 §11 で閉**。~~【GAP-B4-3】~~ ⟹ **v1.2 §12 で閉**。【GAP-B4-4】は **v1.2 §13 で部分閉**(下界 192)⟹ 残りは **R0 実測が唯一の決着手段**。
6. ★ **R0 の的が 1 点に絞れた**: 命題 NO-SMALL-NONAB により $\lvert Q\rvert\in\{6,10\}$ は紙で消えたので、R0(B₄-指数 $\le240$)が実際に検定するのは **$\lvert Q\rvert=8$(B₄-指数 192)ちょうど 1 点**である。

> ### 研究者・司令塔への一言(正直な見立て)
> **この戦線の主産物は「陰性の構造定理」である。** ①③⑤ は紙で閉じる(または 2 つの小さな穴だけ)一方、②④ の意味で **B₃ の華($13/15$ を紙で閉じた MIRROR-ODD)は $B_4$ には無い**。それは移植の失敗ではなく、**$B_3$ の $PSL_2(\mathbf Z)$ miracle が $n=3$ 限定であること(NO-PSL-B4)の帰結**であり、この 1 行自体が**「なぜ gentle 系が計算しやすいか」の構造的説明**として一級の収穫である。census は**その説明を反証可能にする装置**として設計した。
