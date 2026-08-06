# 既存 SAT 線(S8.5)の新規応用 2 件 — 設計ノート v1

**状態札: `design only / 実装ゼロ・本走ゼロ / Sol 未承認 / 発火未認可 / 封印 3 量非接触(n=5 系・Im R・d_N)/ 研究対象の値を 1 個も評価していない / 機械は付録 A の「棚と library の設計時プローブ」(GAP 3 本・研究対象非接触)のみ`**

- 起草: 影工房 数学者(Claude / Opus 5)・2026-08-06
- 委嘱: 司令塔 **裁定 626 + 626 補正**(「輸入設計」から「**既存 S8.5 線の応用 2 件**」へ再射程)
- **本ノートは新しいパイプラインを設計しない。** 器(`sat-run.yml` / `lrat-recheck.yml` / `lrat_check.py` / cake_lpr / mutant matrix 規律)は **S8.5 のものをそのまま使う**。書くのは差分だけ。
- 入力正本:
  - `provenance/LEDGER.md` 裁定 488 節(S8.5 検収)・裁定 626/626 補正
  - `docs/notes/w6_bottomup_design_v1.md` **§3.4(S8.5 本体)・§4.1 A-8・§4.3 DF-BU-8・§5.1 S-BU-SAT-1〜3**(= S8.5 の正本)
  - `search/sat/README.md`・`search/sat/manifest_tail8_n21.json`(schema `shadow-atelier/sat-encoder-manifest/v1`)・`search/sat/mutants_n21.json`(schema `shadow-atelier/sat-mutant-matrix/v1`)・`search/sat/runs/RUNS_LEDGER.md`
  - `docs/notes/hs_prop7_translation_v1.md`(定理 D2-BLIND/D3-BLIND/**D4-POWER**・系 D4-DUM/D4-PRED・定義 HSP-NW・篩 HSP-F・**§8.7.3 定義 NW(7)**)
  - `search/probe/hsp7_mainrun/predicate_lib_laneV_cf.g`(CF 閉形式の実装ヘッダ)・`search/certs/hsp7_cf_calib_20260805.json`・`search/certs/hsp7_cond2_p7_20260804.json`
  - `docs/notes/exploration_queue_candidates_v1.md`(札 N-1〜N-4・W-1/W-2)・`docs/notes/theorem_check_mirrorall_l3vacuous_v1.md`(**定理 MIRROR-ODD §A.3**・**Test ORB §F.8**・§G 兄弟クリーク)・`docs/notes/bhunt_l1_bridge_v1.md`・`docs/状態.md`・`docs/地図.md` 第 4 版
- **読んだ範囲の申告**: 上記のうち `hs_prop7_translation_v1.md` は §0〜§5 と §8.7.3 の該当箇所のみ(§6/§7/§9 は未読)。`w6_bottomup_design_v1.md` は S8.5 関連節(§3.4/§4.1/§4.3/§5.1/§3.3 表)のみ。`search/sat/README.md` は §1〜「第一標的 n=21」まで。encoder 本体(`encode_tail8_n21.py`)は未読(manifest の schema のみ参照)。

---

## 0. 先に — S8.5 との差分表と、一行の結論

### 0.1 差分表(**重複章を書かないための境界線**)

| 項目 | S8.5(既在・正本 = `w6_bottomup_design_v1.md` §3.4 ほか) | 本ノートの差分 |
|---|---|---|
| **符号化する対象** | BOTTOM-UP の**層**(加群 $V$・$H^2$ 類)に「$\Gamma$-同変・非分裂・障害類 $\ne0$ の拡大が存在するか」 | ★ **窓の中の shadow** $(m,\bar f)$ に「hexagon ∧ $\mathrm{PENT}_W$ ∧ **$\notin H_W$**」が存在するか。**対象も篩の位置も別**(S8.5 は S8→S9 の間、本件は窓確定後の悉皆レーンの代替) |
| **器**(workflow・checker・solver) | `sat-run.yml`(sha ゲート・kissat/cadical)/ `lrat-recheck.yml`(cake_lpr)/ `lrat_check.py` / 三段 checker 体制 | ★ **一切変更しない。流用宣言。**入口は同じ DIMACS ファイル 1 本 |
| **陰性レジーム** | UNSAT + LRAT ⟹ 機械検証つき悉皆陰性。**較正前は `CALIBRATION_PENDING`**・EMPTY-THM に登録しない | ★ **同一規律を継承。再掲しない。** 差分は「我々のエンコーダ用の完全性補題」= **補題 BH-COMP**(§1.8)だけ |
| **witness の扱い** | SAT witness = 候補のみ。GAP 再構成 + 独立再計算の 2 段を通ったものだけ次段へ | ★ **同一。**差分 = 再構成先が「GAP pc 群での hexagon/PENT 再評価」で、**照合器は既存 CF レーンを流用**(§1.6) |
| **較正** | A-8(mutant matrix)/ DF-BU-8(両方向 fixture) | ★ **同じ型で新設**: **A-BH / DF-BH-1〜3**(§1.7)。ES7 の `mutants/` と `search/sat/mutants_n21.json` の schema を**そのまま**使う |
| **停止規則** | S-BU-SAT-1〜3 | ★ **継承 + 本用途固有 2 本**(S-BH-1/S-BH-2・§1.10) |
| **未証明の前提** | 【BU-GAP-6】(CNF 符号化と紙篩の論理同値)・【BU-GAP-7】(統計ランキング未設計) | ★ **同型の GAP を継承**し、本件固有に【BH-GAP-1〜3】を新設(§1.10) |
| **SmallGroups 軸** | S8.5 に対応物なし | ★ **本ノート §2。SAT ではない**(列挙設計)。S8.5 の器を一切使わない |

### 0.2 一行の結論(**先に・不都合な方から**)

> $$\boxed{\ \textbf{現行の verbal 窓族 NW}(c,p)\ \textbf{に対しては、SAT は勝てない。}\ }$$
> hexagon と $\mathrm{PENT}_W$ の制約系は**下中心列に沿って層三角**であり、各層の主要項は $\mathbb F_p$-**線型**、非斉次項だけが下層の多項式である(§1.2 定理 TRI-LCS)。ゆえに「層消去 → 残差系」で自由パラメータは $D\approx2$〜$8$ 個の $\mathbb F_p$ 変数に落ち、$p^D\lesssim10^7$ 点の総当りで閉じる — **既存 CF 装置が既にやっていること**である。ここに CNF を書くのは**遅い道具を作る仕事**になる。
>
> $$\boxed{\ \textbf{SAT が稼ぐ場所は 4 つに特定できる(§1.4)。第一標的は「交差窓 NW}(4,7)\cap K^{(7)}\textbf{」。}\ }$$
> 層三角性が全域では成り立たない窓(非冪零成分をもつ交差窓・class $\ge p$ で Lazard が切れる窓・非 verbal な歪み窓)と、**窓パラメータごと存在量化する問い**の 4 つ。いずれも既存 CF 装置に対応物がない。
>
> $$\boxed{\ \textbf{SmallGroups 軸は「指数軸の壁の回避」ではない — 「構造での狙い撃ち」である(§2)。}\ }$$
> 本日実測: SmallGroups は **ID つきで位数 $\le2000$(1024 欠)+ 2401**。BOTTOM-UP の 4000/4500/8000 帯は**ライブラリに存在しない**。指数軸は 2 倍しか伸びない。**代わりに、MIRROR-ODD が原理的に届かない $2^a3^b$ 帯を悉皆で舐められる** — 帯は 6 位数、うち実行可能な 5 位数で **215,194 群・実測レートから約 4.8 分**(§2.3)。**これは今日から走れる最安の未踏領土である。**

---

## 1. 用途① — B 型狩りエンコーダ(hexagon / $\mathrm{PENT}_W$ → 既存 CNF 入口)

### 1.1 何を SAT に問うのか(述語の確定)

窓対 $\mathbf N$(NW$(c,p)$ 型)に対し、$P:=F_2/N_{F_2}$、$Q:=K(0,5)/W$、$\mathcal X_N:=\{m:\gcd(2m+1,N_{\rm ord})=1\}$。求める述語は

$$\mathrm{BH}(m,\bar f)\ :\iff\ \underbrace{N_\theta(\bar f)=1\ \wedge\ N_\tau(m,\bar f)=1}_{\text{hexagon (3.10)(3.11)}}\ \wedge\ \underbrace{\bar f\in[P,P]}_{\text{charming}}\ \wedge\ \underbrace{\textstyle\prod_{i=4}^{0}j_i(\bar f)=1\ \text{in }Q}_{\mathrm{PENT}_W}\ \wedge\ \underbrace{(m,\bar f)\notin H_W}_{\text{blocking}}$$

- $N_\theta(\bar f):=\bar f\cdot\theta(\bar f)$、$N_\tau(m,\bar f):=\tau^2(y^m\bar f)\,\tau(y^m\bar f)\,y^m\bar f$(定義ノート (3.10)(3.11)・[HS7] §1.1 表の $d=2,3$ ノルム)。
- $j_i:=\rho^i\circ j:F_2\to Q$ は 5 本の埋め込み。verbal 窓では $\rho(W)=W$ と $j(N_{F_2})\subseteq W$ が自動((W-b)(W-c)・補題 NW-2/NW-3)なので $j_i$ は $P\to Q$ の**準同型**に落ちる。$\mathrm{PENT}_W$ は定理 PENT-NORM のノルム形(量化子なし)。
- $H_W$ = 既知の算術像(NW(7) では **BH-α-pent v1.1・裁定 586 の $|H_W|=42$**)。
- **SURJ と settled は CNF に入れない。** NW 族では系 H8′(SURJ 識別力ゼロ)と VERBAL-ISO(isolated)で**紙で全通過**が確定しており(予言 EXQ-9)、CNF に入れれば節を無駄に増やすだけで識別力ゼロ。**外部 oracle 扱い**(Sol 便 84 §6.2 の「構造定数 4160 と $C(u)$-軌道を公理に入れない」と同じ設計判断)。

> ★ **格の線引き(過剰主張の防止)**: SAT が返す $(m,\bar f)$ は **B 型 candidate** であって B 型 witness ではない。$H_W$ は算術像の**下界**でしかない場合がある(NW(7) では BH-BRIDGE により等号だが、これは framework-relative の紙)。**上界(= 非算術性)は紙の仕事**であり、ソルバーは供給できない。これは「ソルバー = 候補発見器」規律(2026-07-29 裁定)の逐語適用である。

### 1.2 ★ 定理 TRI-LCS(層三角性)— 本ノートの設計上の分水嶺

> ### 定理 TRI-LCS(candidate・紙上証明)
> $P$ を class $c$、指数 $p$($c<p$)の冪零群、$\alpha$ を $P$ の自己同型で位数 $d$($d\in\{2,3,5\}$)、$\gamma_k$ を下中心列とする。Lazard 対応の下で $\bar f=\exp(F)$、$F=\sum_{k\ge2}F_k$($F_k\in\mathrm{gr}_k$)と書くと、ノルム $N_\alpha(\bar f)=\prod_{i=d-1}^{0}\alpha^i(\bar f)$ の $\mathrm{gr}_k$ 成分は
> $$\bigl[N_\alpha(\bar f)\bigr]_k\ =\ \underbrace{\Bigl(\textstyle\sum_{i=0}^{d-1}\alpha^i\Bigr)(F_k)}_{\textbf{層 }k\textbf{ について }\mathbb F_p\textbf{-線型}}\ +\ \underbrace{B_k(F_2,\dots,F_{k-1})}_{\textbf{下層のみの多項式(BCH 補正)}}$$
> の形をもつ。ゆえに $N_\alpha(\bar f)=1$ は **$k=2,3,\dots,c$ の順に解ける三角系**であり、各段は「$\mathbb F_p$-線型系 + 下層で決まる定数項」である。$y^m$ 共役(非斉次項)と $\rho$-ノルム($d=5$)も同型。∎(スケッチ)

**証明の骨**: BCH は $\log(\bar f\,\alpha\bar f\cdots)= \sum_i\alpha^i F+\frac12\sum_{i<j}[\alpha^jF,\alpha^iF]+\cdots$ で、$F$ は $\deg\ge2$ から始まる(charming)から交換子項は $\deg\ge4$、$k$ 次項に入る交換子の各因子は次数 $<k$。$c<p$ ゆえ BCH の分母(2, 12, 24, …)はすべて $\mathbb F_p^\times$ で可逆 — Lazard 対応が使えるのはこの条件による。∎

> ### ★ 裏取り(**既測の値を再現する**)
> $c=4$、$p=7$($=$ NW(7))で層ごとに数えると:
> - $k=2$: $c_2$ は $m$ で強制($c_2=m(m+1)/6$・C2-FIN)⟹ **自由度 0**。
> - $k=3$: $\ker(1+\theta)|_{\mathrm{gr}_3}=\mathbb Q\mathfrak h_3$(定理 D3-BLIND (a)(b))⟹ **自由度 1**。
> - $k=4$: hexagon の斉次解空間は $\mathbb Q\mathfrak h_4$ の 1 次元(定理 D4-POWER (a))⟹ **自由度 1**。
>
> ⟹ **$D:=\sum_k d_k=2$**、$m$ ごとの hexagon 解は $p^2=49$ 個。**これは札 P-1【EXQ-CF7】の登録予言「$\lvert\mathrm{hex}(m)\rvert\in\{0,7^2=49\}$」と一致する。** さらに $\mathrm{PENT}$ は $\mathfrak h_4$ 座標を 1 点に落とす(系 D4-PRED・検出比 $1/p$)から、通過は $m$ ごとに $49/7=7$ 個、全体で $6\times7=\boxed{42}$ — **BH-α-pent v1.1 の実測 $\lvert H_W\rvert=42$(裁定 586)と一致する**。
> **本定理は既測 2 点を独立に再現する。** これが「層三角性は本物である」ことの裏取りであり、同時に「$D$ が小さいから SAT が要らない」という結論の根拠である。
> ⚠ **格**: 定理 TRI-LCS 自体は本ノート起草の candidate(単系統・Sol 未監査)。再現した 2 点は既在の登録済み値であり、**新しい測定ではない**。

### 1.3 二つの符号化と単価表(**委嘱の「CNF にする単価」への回答**)

$\mathbb F_p$ 元は **one-hot**($p$ 個の Boolean + ALO 1 節 + AMO $\binom p2$ 節)で持つ。二項演算 1 個(加算 or 乗算)= 出力 one-hot $p$ 変数 + 含意 $p^2$ 節 + ALO/AMO。**定数倍と定数加算は literal の置換で表せるので節ゼロ**(これが線型部分がタダになる理由)。

| | $p=7$ | $p=11$ |
|---|---|---|
| $\mathbb F_p$ 変数 1 個 | 7 var / 22 節 | 11 var / 56 節 |
| 二項ゲート 1 個 | 7 var / **71 節** | 11 var / **177 節** |
| 定数係数の線型形 | **0 var / 0 節** | 同左 |

**符号化 D-CNF(直接・層消去なし)**: pc 座標をそのまま変数にし、群の積を Lazard/BCH の多項式でゲート化する。

- $\theta,\tau,\rho,j_i$ はすべて**群準同型/自己同型** ⟹ Lazard 下で **Lie 環準同型 = 座標の $\mathbb F_p$-線型写像** ⟹ **ゲート消費ゼロ**。これは設計上の大きな当たりで、「5 回の語評価」は**節を 1 本も生まない**。
- 残るコストは**群の積そのもの**だけ: hexagon 側 = $P$ 内で 3 回((3.10) 1 回・(3.11) 2 回、$y^m$ は $m$ を分岐すれば定数)、pentagon 側 = $Q$ 内で 4 回。
- 積 1 回の単項式数は、荷重つき次数 $\le c$ の BCH 項を数えて見積る(重み $=$ 層番号)。NW(7): $P$ は 8 座標(層 2,1,2,3)、$Q$ は 40 座標(層 5,4,10,21)。

| 窓 | $m$ 分岐後・1 CNF あたり(**オーダー見積り**) | 変数 | 節 |
|---|---|---|---|
| **NW(7)** $P$ 側 3 積 | 単項式 $\approx$ 120/積・平均次数 2.5 | $\approx6\times10^3$ | $\approx5\times10^4$ |
| **NW(7)** $Q$ 側 4 積 | 単項式 $\approx3.7\times10^3$/積 | $\approx2\times10^5$ | $\approx2.0\times10^6$ |
| **NW(7) 合計**(6 CNF) | | $\approx2\times10^5$ | $\approx\mathbf{2.1\times10^6}$ |
| **NW(4,11) 合計**(10 CNF) | ゲート単価 $\times2.49$・one-hot $\times1.57$ | $\approx3.2\times10^5$ | $\approx\mathbf{5.2\times10^6}$ |

> ⚠ **単項式数は導出つきの概算**(荷重つき次数 $\le4$ の括弧対を数え、構造定数の平均非零数を 3 と置いた)であり、**±1 桁の幅がある**。厳密値は `PGroupToLieRing` で 1 回走らせれば機械で確定する(§3・実装前の測定項目)。**この不確かさを設計判断の根拠に使わない**ようにするため、結論(§1.4)は下の R-CNF 側の桁で立てている。

**符号化 R-CNF(層消去後・推奨)**: 定理 TRI-LCS に従って $k=2,3,\dots$ と $\mathbb F_p$-線型系を解き、自由パラメータ $\theta=(\theta_1,\dots,\theta_D)$ と、上層の可解条件から来る**残差多項式系** $R(\theta,m)=0$ を得る(この消去は $p$ に依存しない整数演算で一度だけ)。CNF 化するのは $R$ だけ。

| 窓 | $D$ | 残差系の規模 | 変数 | 節 |
|---|---|---|---|---|
| **NW(4,$p$)** 全 $p$ | **2**(+$m$) | $E\approx2$〜4、単項式 $M\approx10$〜20 | $\approx3\times10^2$ | $\approx\mathbf{3\times10^3}$ |

> $$\boxed{\ \textbf{D-CNF と R-CNF の差は 3 桁。そして }R\textbf{-CNF は総当りより速くない —}\ p^D=49\ \textbf{点の全列挙が即答だからである。}\ }$$

### 1.4 ★ 交叉点 — SAT が実際に勝つ 4 か所(**根拠つき**)

総当りの限界を先に固定する。CF レーンの実測 per-candidate は **12.4 μs**(local)/ **14.8 μs**(GHA)(`hsp7_cf_calib_20260805.json` の Lane P `31/2500` ms・`37/2500` ms 逐語)。GHA 1 job の 6 時間予算 $=2.16\times10^{10}\,\mu$s ⟹ **総当りの上限 $\approx1.5\times10^9$ 候補**。R-CNF の規模は $p$ にも $D$ にも**指数的には**依存しない($p^2$ と $M$ の一次)。

| # | 場所 | なぜ層消去が効かないか | 規模 | 判定 |
|---|---|---|---|---|
| **(α)** ★ **交差窓 $M=\mathrm{NW}(4,7)\cap K^{(7)}$**(札 N-4) | $P_M$ は冪零でない(dihedral 因子 $D_7$ が入る)⟹ **全域の LCS 三角性が壊れる**。Goursat 層の整合条件は層をまたぐ | $\lvert[P_M,P_M]\rvert\le7^9\approx4.04\times10^7$ — 総当り可能圏だが **CF に交差版が無い**(札 N-4 自身が明記) | ★ **第一標的**。SAT なら CF 交差版を書かずに済む |
| **(β)** **class $\ge p$**(例: $p=7$ で $c=7$) | **Lazard 対応が切れる**($c<p$ が前提)⟹ BCH の分母が $\mathbb F_p$ で可逆でなくなり、層の主要項が線型でなくなる | $c=6$ で既に $\lvert[P,P]\rvert=7^{21}\approx5.6\times10^{17}$ | 総当り不能・層消去不能 ⟹ **SAT/制約系しかない** |
| **(γ)** **非 verbal(歪み)窓**(札 W-2 SKEW-WIN) | $N_{F_2}=\langle\langle\langle\theta,\tau\rangle\text{-orbit}(w)\rangle\rangle\cdot\gamma_5F_2^p$ は完全不変でない ⟹ 層作用素が自由なものでなくなり、$\rho$-安定性((W-b))も**自動でない**。可解条件が層をまたいで結合 | $w$ の選択が探索次元に加わる | **$w$ ごと存在量化できるのが SAT の本質的な利点** |
| **(δ)** ★ **窓パラメータごと存在量化** | 「族の中に B 型候補をもつ窓が**存在するか**」は $\exists w\,\exists(m,\bar f)$ の二重存在。層消去は $w$ を固定しないと始まらない | — | ★ **既存装置に対応物ゼロ**。「存在側の狩り」という委嘱文言に唯一まっすぐ答える形 |

> ### ★ 系 CROSS-p(**$p$ 軸の交叉点**)
> NW$(4,p)$ の総当り宇宙は $(p-1)p^6$。上限 $1.5\times10^9$ から $p\le19$($18\cdot19^6=8.5\times10^8$ ✓、$22\cdot23^6=3.3\times10^9$ ✗)。
> **⟹ $p\ge23$ の NW$(4,p)$ は総当り不能。** ただし**層消去は $p$ に依存しない**(整数演算 1 回)ので、$p\ge23$ でも $R$ を作れば $p^2\le p^{D}$ 点の総当りで足りる。
> **⟹ 結論: $p$ 軸だけでは SAT の出番は来ない。**「1/p 律の族データ」(札 N-1)は SAT ではなく**層消去 + $\mathbb F_p$ 線型代数**で $p=11,13,\dots,101$ まで一気に取れる — **これは本ノートの副産物で、札 N-1 の想定コスト(NW(7) 実測 $\times$ 25)を無用にする可能性がある**(§4 の推奨 ③)。

### 1.5 SAT 以外の候補との比較(**委嘱の指定項目**)

| 手法 | 適合度 | 根拠 |
|---|---|---|
| **層消去 + $\mathbb F_p$ 線型代数**(= 事実上の「等級つき Gauss 消去」) | ★★★ **現行 NW 族の最適解** | 定理 TRI-LCS。系の三角性がそのまま解法になる。既存 CF 装置がこの位置にいる |
| **可換 Gröbner**(`singular` / GAP `GroebnerBasis`) | ★★ (α)(γ)(δ) で有力 | 体方程式 $x^p=x$ を足せば $\mathbb F_p$ 上有限解。**等級に沿った消去順序を取れば Gröbner 計算はほぼ層消去そのもの**になる ⟹ 三角な部分は無料、非三角な残りだけに計算が集中する。**この「自動的に良い順序が効く」性質は SAT にはない** |
| **非可換 Gröbner**(`gbnp`) | ★ 限定的 | 自由 Lie 環側の Hall 基底計算・$\mathfrak t$ の関係式処理には使える(定理 D2-BLIND の整数証明書の再導出など)。**制約充足器としては使わない** |
| **SAT (CNF + kissat)** | ★★ (β)(γ)(δ)・**陰性主張には必須** | 唯一 **LRAT で機械検証可能な陰性**を出せる。§1.8 |
| **SMT の有限体理論**(cvc5 の finite-field solver) | ? **UNKNOWN(要確認)** | $\mathbb F_p$ 多項式系をネイティブに扱う solver が存在すると理解しているが、**本ノートは出所を確認していない**。仮に存在しても **LRAT を出さない** ⟹ 候補発見には使えても**陰性登録には使えない**。器の新設は S8.5 の流用方針に反する ⟹ **本ノートは採用しない**(実装係が調べる価値はある) |
| **整数計画(MILP)** | ✗ | mod $p$ 演算は one-hot + big-M、次数 $\ge2$ で非線型 ⟹ 二次化が必要。**CNF より必ず大きくなる**うえ証明書が出ない。**採用しない** |

> ★ **設計の分割線(これが本ノートの組織原理)**: 「**候補発見**はバグ許容・速さ優先 ⟹ Gröbner でも局所探索でもよい。**陰性主張**はバグ不許容 ⟹ **CNF + LRAT + 三段 checker + mutant matrix** 以外を使わない。」— これは既存の裁定(2026-07-29「ソルバー = 候補発見器・陰性主張時のみ登録レジーム」)を、道具選択の規則として書き下したものである。

### 1.6 「候補 1 個」を返す設計(**CF と重複させない**)

- **役割分担の宣言**: **数え上げ(悉皆・分布・$\lvert\mathrm{GT}^{\rm pent}\rvert$)は CF レーンの仕事。SAT は数えない。** SAT が返すのは「1 個の充足割当」か「UNSAT + LRAT」のみ。
- 実装形は既存 `sat-run.yml` のまま: SAT なら `model_vlines.txt` を出す。**増分 SAT(blocking clause で 2 個目を探す)は使わない** — 使えば「$k$ 個見つけた」という**数え上げの主張に化ける**ので、CF との二重計上事故を招く。**1 CNF = 1 質問 = 1 答**。
- 復号と照合(**探索器と照合器の分離**):
  1. `model_vlines.txt` → **encoder を import しない独立実装**(node)で one-hot を $\mathbb F_p$ 座標へ復号(`search/sat/tools/verify_generic_cnf_model.mjs` の型を踏襲)。
  2. 座標 → GAP pc 群の元 $\bar f$ を再構成し、**既存 CF レーン**(`predicate_lib_laneV_cf.g` の `EvalFullHexagon` 系)で hexagon を、Lane P で $\mathrm{PENT}$ を**独立に再評価**。
  3. **$H_W$ 非所属を別実装で再確認**。3 つとも通った候補だけを司令塔へ上げる(**S-BH-1 で必ず停止**)。
- ★ この設計だと、CF レーンが**照合器として無改造で再利用できる**(CF は「$\bar f$ を群の元として受け取る」設計・実装ヘッダ逐語)。**新規実装は encoder と復号器の 2 本だけ**である。

### 1.7 較正 — mutant matrix を我々のエンコーダに掛け直す手順(**委嘱の指定項目**)

S8.5 の A-8 / DF-BU-8 と**同じ規律**。ここでは**手順だけ**を書く。

**段 0(前提)**: 我々の encoder は `shadow-atelier/sat-encoder-manifest/v1` を**自己生成**すること(手打ち転記禁止)。必須欄は n21 の manifest と同じ: `encoder_source_sha256` / `universe`(窓パラメータ $c,p,e$・$\lvert P\rvert$・$\lvert Q\rvert$・$\lvert\mathcal X_N\rvert$)/ `product_order_convention`(**規約 W-1/W-2 の語の向き・D-6**)/ `variable_families` / `clause_groups` / `cnf_files{path,num_vars,num_clauses,sha256,expected_verdict}` / `symmetry_reduction` / `audit_status`。

**段 1(基線 2 本・両方向)**:

| 基線 | CNF | 期待 | 根拠 |
|---|---|---|---|
| **B-SAT** | hexagon ∧ charming のみ($\mathrm{PENT}$ も blocking も無し) | **SAT** | $\lvert\mathrm{hex}(m)\rvert=49>0$(§1.2) |
| **B-UNSAT** | hexagon ∧ charming ∧ $\mathrm{PENT}_W$ ∧ $\notin H_W$ | **UNSAT** | BH-α-pent v1.1(裁定 586・$\mathfrak G_{\rm pent}=H_W$) |

> ★ **NW(7) が理想の較正標的である理由**: 両方向の正解が**既に独立に確定している**(n=21 が「既知の 4160 解 + 非推移という oracle」を持っていたのと同じ構図・Sol 便 84 §6.1 の選定理由の逐語適用)。

**段 2(fixture・生命線)**:

| ID | 入力 | 期待 | これが外れたら |
|---|---|---|---|
| **DF-BH-1** ★★ | $\bar f_{\rm dum}=\exp(t\,\mathfrak h_4)$($t\ne0$)を**定数として固定**した CNF | hexagon **SAT** かつ $\mathrm{PENT}$ **UNSAT** | 系 D4-DUM の実効化に失敗 ⟹ **以後の UNSAT は全部情報量ゼロ**(DF-BU-5 の逐語) |
| **DF-BH-2** | $\mathfrak h_3$ 方向のみの $\bar f$ | hexagon **SAT** かつ $\mathrm{PENT}$ **SAT** | 定理 D3-BLIND の実測版。**過剰に殺していない**ことの両側較正 |
| **DF-BH-3** ★ | **玩具窓 NW(4,3)**(宇宙 $2\cdot3^6=1{,}458$・札 N-2)で **CNF の全解 = CF の全解**(集合等号) | 一致 | 符号化の忠実性の唯一の**悉皆**検査(§1.8 の (ii) を実際に閉じる唯一の場所) |

**段 3(mutant matrix)**: `search/sat/mutants_n21.json` の schema をそのまま使い、**走らせる前に**予測を凍結する(各行に `PROVEN` / `REASONED` / `UNKNOWN` の確度札 — n21 の `_note_on_confidence` 規約を継承)。最小 8 行:

| ID | 注入する欠陥 | B-SAT 予測 | B-UNSAT 予測 | 確度 |
|---|---|---|---|---|
| **MB1** | $\theta$ の向き反転($x\leftrightarrow y$ を $y\leftrightarrow x$ 以外に取り違え・**罠 D-6**) | SAT | UNKNOWN | UNKNOWN |
| **MB2** | $\tau$-ノルムの因子順を $\tau^2\tau1\to1\tau\tau^2$ に反転 | SAT | UNKNOWN | UNKNOWN |
| **MB3** | $\mathrm{PENT}$ の 5 因子を巡回でなく逆順に | UNSAT(基線と別 CNF) | — | REASONED |
| **MB4** | $c_2=m(m+1)/6$ の $6^{-1}\bmod7$ を誤る | **UNSAT**(hexagon が不整合化) | UNSAT | PROVEN |
| **MB5** ★ | 深さ 4 を切り落とす(class 3 で打ち切り) | SAT | ★ **SAT へ反転** | **PROVEN**(D2/D3-BLIND ⟹ 検出力が消える ⟹ blocking が効かなくなる) |
| **MB6** | $\mathbb F_7$ 乗算表を 1 エントリ破壊 | UNKNOWN | UNKNOWN | UNKNOWN |
| **MB7** | charming 制約 $\bar f\in[P,P]$ を落とす | SAT | ★ **SAT へ反転** | REASONED |
| **MB8** | blocking を $H_W$ の 42 個中 41 個に減らす | SAT | ★ **SAT**(残り 1 個が解になる) | **PROVEN** |

> **MB5 と MB8 が本 matrix の背骨**である。MB5 は「検出力が生きていること」、MB8 は「blocking が効いていること」を、それぞれ**反転が起きること**で証明する。片方でも反転しなければ **A-BH 不成立 ⟹ S-BU-2 相当で停止**、UNSAT は `CALIBRATION_PENDING`。

### 1.8 陰性主張の差分 — 補題 BH-COMP(**S8.5 が持っていない唯一の数学的追加**)

S8.5 の陰性レジーム(UNSAT + LRAT ⟹ 悉皆陰性)は**符号化の完全性**を前提にしている(【BU-GAP-6】が意図的な GAP 申告)。n=21 では Sol が **SAT-COMP-21** を紙で供給した。本用途にも同じ形が要る。

> ### 補題 BH-COMP(**要証明・本ノートは骨格のみ**)
> $(m,\bar f)$ が $\mathrm{BH}(m,\bar f)$ を満たすなら、対応する one-hot 割当は encoder の出力 CNF を充足する。
> **対偶: UNSAT ⟹ 当該窓に B 型候補は存在しない。**
>
> **証明義務(3 件)**:
> - **(i) 正規形の全域性と単射性**: $P$(resp. $Q$)の全元がちょうど 1 本の pc 指数ベクトルをもつ。⟸ `polycyclic` の pcgs の性質。**紙で閉じる。**
> - **(ii) ★ 乗算多項式の忠実性**: encoder が使う $\mathbb F_p$ 多項式が、**全入力対**で GAP の collection と一致する。⟸ **これが本命の穴**。全対検査は $\lvert P\rvert^2=7^{16}$ で不能。
>   **対策**: ①多項式を `PGroupToLieRing`(Lazard)+ BCH から**機械生成**し、**記号恒等式として**照合する ②**玩具窓 NW(4,3)** で $\lvert P\rvert^2=3^{16}\approx4.3\times10^7$ の**全対**を実際に突合(= DF-BH-3 の強化版・数分)③本窓ではランダム標本 $10^6$ 対。**①+② で「同じ生成規則が小さい体で悉皆一致」まで、③で本窓の標本一致まで。これでも (ii) は完全には閉じない**。
> - **(iii) blocking 集合の同一性**: CNF の 42 本の blocking 節が $H_W$ とちょうど対応する。⟸ **$H_W$ の座標を encoder と独立に読み出す第二実装**が要る(CV-9 の型)。
>
> **【BH-GAP-1】** (ii) は**閉じない**。ゆえに本用途の UNSAT の格は最良でも **`cross-checked candidate`** であり、`verified` は Lean 化(CNF ↔ 群論意味論の橋)まで来ない。**ES7 README の「Lean 級への昇格路」と同じ位置**。

### 1.9 IF-FIRST 予言枠(**発火前に単独コミット** — 裁定 543 恒久規則)

| # | 予言 | 反証条件 | 根拠 |
|---|---|---|---|
| **P-BH-1** | B-SAT 基線は **SAT**、B-UNSAT 基線は **UNSAT** | どちらか外れ ⟹ encoder バグ(数学の反証ではない) | §1.2 + 裁定 586 |
| **P-BH-2** ★ | MB5(深さ 4 切り落とし)で B-UNSAT が **SAT へ反転** | 反転しない ⟹ 検出力が CNF に載っていない ⟹ **A-BH 不成立** | 定理 D2/D3-BLIND |
| **P-BH-3** ★ | MB8(blocking 41 本)で B-UNSAT が **SAT へ反転**し、復号された解が**除いた 1 個と一致** | 不一致 ⟹ blocking と $H_W$ の対応が壊れている | 自明(較正の自己整合) |
| **P-BH-4** | 玩具窓 NW(4,3) で CNF 全解集合 $=$ CF 全解集合(**集合等号**・1,458 宇宙) | 不一致 1 件でも ⟹ `ENCODING_MISMATCH / STOP` | DF-BH-3 |
| **P-BH-5** | D-CNF の実節数が §1.3 の見積りの **$10^{\pm1}$ 以内** | 外れ ⟹ 単項式勘定の誤り(設計の訂正であって停止ではない) | §1.3 の概算の自己申告 |
| **P-BH-6** ★★ | **交差窓 (α) では層三角性が破れる** — すなわち $P_M$ の LCS 層別自由度の総和 $D_M$ が「$\mathrm{NW}$ 側 $D=2$ と $K^{(7)}$ 側の自由度の単純和」と**一致しない** | 一致する ⟹ 交差窓も層消去で閉じる ⟹ **(α) は SAT 標的から降りる**(その場合 §4 の推奨 ① は無効・撤回する) | 定理 TRI-LCS の適用限界 |

### 1.10 停止規則の差分・GAP 一覧

- **S-BH-1**: SAT が候補を 1 個返した ⟹ **即停止・司令塔へ即報**。§1.6 の 3 段照合を通す前に「B 型を見つけた」と書いたら `OVERCLAIM / STOP`(S-BU-4 の逐語適用)。**さらに札 F-1【FAKE-PROTOCOL】の着弾手順(未起草)を先に用意すること**。
- **S-BH-2**: DF-BH-1(dummy)または MB5/MB8 の反転が確認できないうちに UNSAT を陰性として台帳へ書こうとした ⟹ `CALIBRATION_PENDING / STOP`。
- 継承: S-BU-SAT-1〜3・S-BU-6(「掘らない」と「空」を混同しない)・S-8′(不一致 1 件でも STOP)。
- **【BH-GAP-1】** §1.8 (ii)(乗算多項式の全域忠実性)— 閉じない。UNSAT の格の上限を決める。
- **【BH-GAP-2】** 定理 TRI-LCS は本ノート起草の candidate(単系統)。**Sol 監査前に「$D=2$ だから SAT 不要」という結論を確定として引用しない。**
- **【BH-GAP-3】** 交差窓 (α) の $P_M$ の構造(Goursat 層の会計)は未計算。P-BH-6 が採点点。

---

## 2. 用途② — SmallGroups 軸の exotic 狙い撃ち(**SAT ではない・列挙設計**)

### 2.1 ★ 前提の訂正 — 「lins の壁 ~1000」は硬い壁ではない

裁定 626 は「lins は悉皆器(壁 ~1000)」とした。実測を並べると:

| 指数上限 | lins 本体 | 全体 | 出典 |
|---|---|---|---|
| 192 | 4,281 ms | — | `search/certs/wall_probe_20260728_stage_192.json` |
| 360 | 13,213 ms | 21,041 ms | `search/certs/wall_census_192_360_20260730.json` |
| **1000** | **149,021 ms** | **518,329 ms**(8.6 分) | `search/certs/lins_twin_census_v1_20260806.json` |
| 2000 | **前景 10 分 cap で未完** | — | `search/lins-twin-census-v1.g` L52–62 |

> **「壁」の正体は前景 10 分の壁時計 cap である。** 指数 $\to$ 時間の成長はこの 4 点で概ね指数の 2〜2.5 乗であり、2000 は 1000 の 5〜10 倍 $\approx$ **1〜1.5 時間** — **GHA の 6 時間予算の内側**である。
> ⟹ **最安の一手は SmallGroups 軸ではなく「lins を GHA へ出して 2000〜3000 まで延ばす」**(timing probe 先行は既定の作法)。本節はその**代替ではなく直交する軸**として設計する。

### 2.2 ★ 補題 SG-AB(狙い撃ちを可能にする必要条件フィルタ)

> ### 補題 SG-AB(**紙・3 行**)
> $N\trianglelefteq B_3$、$N\le PB_3$、$c\in N$ とし $\widehat G:=B_3/N$ とすると
> $$\boxed{\ \widehat G^{\rm ab}\in\{C_2,\ C_6\}.\ }$$
> **証明.** $B_3^{\rm ab}\cong\mathbb Z$($\sigma_1,\sigma_2\mapsto1$)で $c=(\sigma_1\sigma_2)^3\mapsto6$。$c\in N$ ⟹ $\widehat G^{\rm ab}$ は $\mathbb Z/6$ の商 = 位数が 6 を割る巡回群。$N\le PB_3$ ⟹ $\widehat G\twoheadrightarrow B_3/PB_3=S_3$ ⟹ $\widehat G^{\rm ab}\twoheadrightarrow C_2$ ⟹ 位数は偶数。∎

> ### 系 SG-23(**標識づけの形**)
> $c\in N$ ⟹ $\widehat G$ は $B_3/\langle\langle c\rangle\rangle\cong PSL_2(\mathbb Z)\cong C_2*C_3$ の商。$\Delta:=\sigma_1\sigma_2\sigma_1$、$\delta:=\sigma_1\sigma_2$ の像 $(r,s)$ は $r^2=s^3=1$・$\langle r,s\rangle=\widehat G$ を満たし、逆に $\sigma_1=\delta^{-1}\Delta$、$\sigma_2=\Delta^{-1}\delta^2$ で復元される。
> ⟹ **窓の探索 = 標識づけられた $(2,3)$-生成対の探索**。これは Test ORB(§F.8)の $\mathcal M$ 列挙と**同じ対象**であり、`wac_reverse_design_v1.md` 命題 0.3 の逆向きでもある。**新機構ゼロ。**

**フィルタ効果の実測**(付録 A・すでに公開されている位数のみ):

| 位数 | 全群数 | $\widehat G^{\rm ab}\in\{C_2,C_6\}$ を通る数 | 通過率 |
|---|---|---|---|
| 126(双子 census 最小・$C_7{:}(C_3\times S_3)$) | 16 | 5 | 31% |
| 432(MIRROR-ODD 射程外) | 775 | 28 | 3.6% |
| 486(MIRROR-ODD 射程外) | 261 | 107 | 41% |
| 384($h^{\rm cen}$ exotic の位数) | 20,169 | 60 | **0.30%** |
| 750($h^{\rm cen}$ クリーク) | 39 | 14 | 36% |

> ★ **2 が濃い位数ほど強く切れる**(384 で 0.30%)。これは帯の主戦場($2^a3^b$)でフィルタが最も効くことを意味する。

### 2.3 ★ 帯の確定と実測コスト(**今日の測定**)

**標的の論理**(2 本の既在の結果の交差):
1. **定理 MIRROR-ODD**(§A.3)は $q\ge5$ の巡回正規 Sylow をもつ窓を**悉皆列挙なしで**閉じる。射程外はちょうど $\lvert\widehat P\rvert=2^a3^b$ 型(および $q\ge5$-Sylow が非巡回/非正規の窓)。
2. **$h^{\rm win}(B_3,\ c\in N\ \text{層})>1000$**(裁定 618 帰結)⟹ 窓層の exotic は指数 $>1000$ にしかない。

⟹ **標的帯 = $\lvert\widehat G\rvert=2^{i}3^{j}\in(1000,2000]$、$i,j\ge1$**($\widehat G\twoheadrightarrow S_3$ ゆえ $6\mid\lvert\widehat G\rvert$)。**本日の実測**(付録 A):

| 位数 | 分解 | SmallGroups | 群数 |
|---|---|---|---|
| **1152** | $2^7\cdot3^2$ | ID あり | 157,877 |
| **1296** | $2^4\cdot3^4$ | ID あり | 3,609 |
| **1458** | $2\cdot3^6$ | ID あり | 1,798 |
| **1536** | $2^9\cdot3$ | ★ **ID なし(ライブラリのみ)** | ★ **408,641,062** |
| **1728** | $2^6\cdot3^3$ | ID あり | 47,937 |
| **1944** | $2^3\cdot3^5$ | ID あり | 3,973 |

- **実行可能 5 位数の合計 = 215,194 群。**
- 実測レート(構築 + `AbelianInvariants`)= **1.336 ms/群**(位数 1296 の先頭 2000 群・2,672 ms)。
- $$\Rightarrow\ 215{,}194\times1.336\,\mathrm{ms}\approx287\ \mathrm{s}\approx\boxed{4.8\ \text{分}}$$
- **1536 は SCOPE_OUT**(4 億群・列挙不能)。**「掘らない」であって「空」ではない**(S-BU-6 の逐語)⟹【SG-GAP-1】。

> ### ⚠ 射程の正確化(**言い過ぎの防止**)
> MIRROR-ODD が覆えないのは**2 種類**である(§A.5 逐語): (a) $\lvert\widehat P\rvert=2^a3^b$ の窓、(b) $q\ge5$-Sylow が**非巡回または非正規**の窓。
> **本節の帯 $\lvert\widehat G\rvert=2^i3^j$ は (a) しか掃かない。** (b)(例: $\lvert\widehat P\rvert$ が $5^2$ や $7^2$ を含み Sylow が非巡回、あるいは $q$-Sylow が非正規)は帯の外にあり、**本設計では未着手**⟹【SG-GAP-3】。
> ⟹ 走った後に書いてよい文は「**帯 $(1000,2000]$ の $2^i3^j$ 型で exotic ゼロ**」まで。「$(1000,2000]$ で exotic ゼロ」と書いたら `OVERCLAIM / STOP`。

> ### ★ ライブラリ射程の確定(**裁定 626 の前提に対する測定**)
> 本日の実測: **ID つきは位数 $\le2000$(ただし 1024 は不在)+ 2401 = $7^4$(15 群)。** 位数 **4000 / 4096 / 4500 / 6000 / 8000 は SmallGroups に存在しない**。
> ⟹ **BOTTOM-UP の発火宇宙(cap 8000)は SmallGroups 軸に載らない。**
> ⟹ **SmallGroups 軸は指数軸を 2 倍にしか伸ばさない。** 「壁の回避」という言い方は正確でない。**正確には「MIRROR-ODD が原理的に届かない帯を、悉皆で・5 分で舐められる」という狙い撃ちである。**

### 2.4 判定の階段(**既存装置の組み合わせのみ・新機構ゼロ**)

| 段 | 検査 | 道具 | 落ちる/残る |
|---|---|---|---|
| **G0** | 位数が帯に入る | ループ | — |
| **G1** ★ | $\widehat G^{\rm ab}\in\{C_2,C_6\}$ | `AbelianInvariants` | 実測 96〜99.7% 脱落(§2.2) |
| **G2** | 標識対 $\mathcal M=\{(r,s):r^2=s^3=1,\ \langle r,s\rangle=\widehat G\}$ が非空 | 元の位数で候補を絞って $\langle r,s\rangle$ 判定 | $(2,3)$-生成でない群が脱落 |
| **G3** | $\widehat G\twoheadrightarrow S_3$ が $(r,s)\mapsto((13),(132))$ で well-defined かつ核 $\widehat P$ が正しい指数 6 | 準同型 1 本 | $N\not\le PB_3$ の対が脱落 |
| **G4** ★ | **Test ORB**(§F.8): $\mathcal M$ を $\mathrm{Aut}(\widehat G)$-軌道に分け、各軌道の **reflexible 判定** $\exists\alpha:\alpha(r)=r^{-1}\wedge\alpha(s)=s^{-1}$ | `AutomorphismGroup` + 軌道 | ★ **non-reflexible = $\iota(N)\ne N$**(補題 REFL-EQUIV)⟹ 非 settled shadow $[-1,1]$ ⟹ **非 isolated** |
| **G5** | 同一位数・同一 $\widehat G$ の**軌道が 2 個以上**(= 双子 $K\ne N$)で、かつ**鏡映対でない** | 軌道会計 | ★ **exotic 双子** = 本節の標的 |

> ### ★ 現実的なコスト警告(**正直な見積り**)
> G4 の `AutomorphismGroup` は G1 を通った群にしか掛けない。位数 486 で 260 ms・432 で 217 ms(§F.8 実測・`scratchpad/map_id_2_run.log`)だが、**位数 1152〜1944 の 2-群寄りの群では 1〜2 桁重くなり得る**。
> ⟹ **G1 通過数を先に測る**(4.8 分の走で確定する)。G1 通過が $\gtrsim10^4$ 群なら G4 は GHA 案件、$\lesssim10^3$ ならローカルで閉じる。**この 1 数が全体の実行計画を決める** ⟹ **段階発注(まず G0–G3 だけ)を強く推奨**。

### 2.5 指数 2000 を超える唯一の道(**参考・本ノートでは設計しない**)

$\widehat G$ を直接引くのでなく **$\widehat P$ を引いて $1\to\widehat P\to\widehat G\to S_3\to1$ を組む**と、$\lvert\widehat P\rvert\le2000$ から **指数 $\le12{,}000$** に届く。これは BOTTOM-UP の $H^2$ 列挙機構の**底替え**(札 D-2 の変種)であって、本ノートの射程外。**S8.5 とも本節とも別の設計案件**として記録だけしておく。

### 2.6 IF-FIRST 予言枠(**発火前に単独コミット**)

| # | 予言 | 反証条件 | 根拠(出所ラベル) |
|---|---|---|---|
| **P-SG-1** ★ | 帯 5 位数の G1 通過数の合計は **$2\times10^3$〜$1\times10^4$** | 範囲外 | 実測通過率 0.30%〜3.6%(2 が濃い側)を 215,194 に当てた**値からの推測** |
| **P-SG-2** ★★ | 帯 5 位数で **exotic 双子(G5)は 0 件** | 1 件でも出れば ★ **$h^{\rm win}$ の初の有限値** = AS-GAP-6 の witness 候補 | **構造からの外挿**: 窓層 15 対が全て鏡映対だった(裁定 609)ことの延長。**外れる方が価値が高い予言** |
| **P-SG-3** | G4 で non-reflexible($\iota(N)\ne N$)な軌道は **出る**(exotic でなくとも) | 全軌道 reflexible | 432/486 が両方 chiral(§F.8 実測)⟹ $2^a3^b$ 帯は chiral が普通 |
| **P-SG-4** | 位数 1152 が G1 通過数で帯の過半を占める(群数が帯の 73%) | 過半でない | 単純な数の比 |
| **P-SG-5** | 帯のどの位数でも、G2($(2,3)$-生成)を通る群は G1 通過群の **半分以下** | 半分超 | **類推**: $C_2*C_3$ の商は 2 生成かつ $\widehat G^{\rm ab}$ が巡回 — G1 の後でもさらに強い制約 |

> **P-SG-2 が本節の主予言である。** 予想どおり 0 件なら「$h^{\rm win}>2000$」へ下界が前進(**帯限定・$2^a3^b$ 限定**の陰性 = bounded negative であって FAKE-VOID ではない)。1 件でも出れば AS-GAP-6 の律速が解ける。**どちらに転んでも領土。**

---

## 3. 棚の点検(**設計の前に棚を見る**規律・本日の実測)

| パッケージ | `LoadPackage` | 本設計での役割 |
|---|---|---|
| **`liering`** | ★ **true** | ★ **`PGroupToLieRing` が実在** = Lazard 対応の実装。**定理 TRI-LCS の層消去と D-CNF の多項式生成を機械化できる ⟹ BCH の手計算は不要** |
| **`guarana`** | true | Mal'cev 対応(`AttachedMalcevCollector` ほか)。冪零群の Lie 法 collection — 交差窓 (α) の非冪零部分との突合に |
| **`nq`** | true | `NqEpimorphismNilpotentQuotient` — 相対自由群 $P$(class $c$・指数 $p$)の構成そのもの。class を上げる (β) の入口 |
| **`gbnp`** | true | 非可換 Gröbner。自由 Lie 環側の基底計算(補助) |
| **`singular`** | true(**バイナリ実在は未確認 —【SG-GAP-2】**) | 可換 Gröbner over $\mathbb F_p$。§1.5 の (α)(γ)(δ) 候補 |
| `polycyclic` / `autpgrp` / `anupq` | true | pc 演算・`AutomorphismGroup`・p 群生成 |

> ★ **これは設計を変える発見である。** 「層消去には BCH を人手で次数ごとに導出せねばならない」(札 N-3 の主な障壁)という前提は、`PGroupToLieRing` の存在で**部分的に外れる**。深さ 5 の検出力(札 N-3【DEPTH-5】)も、**窓を切る前に**機械で次元を出せる可能性がある。

---

## 4. 優先順位の推奨(**採否は司令塔**)

| 順 | 何を | なぜこの順か | 費用 | 想定成果 |
|---|---|---|---|---|
| **①** ★★ | **§2 の G0–G3 だけを走らせる**(SmallGroups 帯 5 位数・4.8 分 + G2/G3) | **今日から走れる唯一の項目。**新機構ゼロ・既存装置の組合せのみ。**G1 通過数 1 個で以後の全計画が決まる**(§2.4 の警告)。MIRROR-ODD が届かない帯という**名指しされた空白**を埋める | ローカル分オーダー | P-SG-1/4/5 の採点・G4 の実行計画の確定 |
| **②** ★ | **§2 の G4/G5**(ORB + 双子会計) | ①の結果次第でローカル or GHA。**P-SG-2 は外れる方が価値が高い**唯一の予言 | ①の結果で決定 | $h^{\rm win}$ の前進 or **AS-GAP-6 witness** |
| **③** ★ | **層消去の機械化**(`PGroupToLieRing` で NW$(4,p)$ の残差系 $R$ を生成)— **SAT ではない** | §1.4 系 CROSS-p: これができれば **札 N-1(NW(4,11))は「$\times25$ の本走」ではなく「$\mathbb F_{11}$ 線型代数 1 発」になり、$p=13,\dots,101$ まで一気に取れる**。**1/p 律の族データが 2 点でなく 10 点になる** | 数学者 + 実装係の小仕事 | 系 D4-PRED の族則が実測で立つ。**地図 第 4 版「cofinal 族への族一様定理」に直接効く** |
| **④** | **定理 TRI-LCS の Sol 監査**(便 112 or 113) | ①②③の全部の前提。**【BH-GAP-2】が閉じるまで「SAT 不要」を確定として引用しない** | 紙 1 節 | 格の確定 |
| **⑤** | **交差窓 (α) の $P_M$ 構造計算**(P-BH-6 の採点) | ここで初めて **encoder を書く価値があるか**が決まる。**一致すれば §1 の encoder は不要になる**(潔く撤回する) | 紙 + GAP 小走 | encoder 起票の可否 |
| **⑥** | **encoder 実装**(⑤で GO の場合のみ)+ mutant matrix + BH-COMP | 上の 5 段を通ってから | 実装係 + Sol ゲート | LRAT つき陰性 |
| **—** | **lins を GHA へ(指数 2000〜3000)** | §2.1 の訂正。本ノートの射程外だが**①と競合しない・並走可**。timing probe 先行 | GHA 1 job | 壁の実位置の確定 |

> ### ★ 司令塔への正直な要約(**1 行**)
> **「SAT 線の新規応用」として発注された 2 件のうち、実際に価値があるのは ② の列挙(SAT を使わない)と ③ の層消去(SAT を使わない)であり、SAT そのものは ⑤ の判定を待って初めて起票に値する。** 委嘱に対して「使えます」と答える方が楽だが、それは**遅い道具を作る仕事**になる。

---

## 5. 【文献要請】

| # | 具体的な技術的困難 | 欲しい結果の型 |
|---|---|---|
| **L-1** ★ | 定理 TRI-LCS の層消去で、$\ker\bigl(\sum_i\alpha^i\bigr)|_{\mathrm{gr}_k}$ の次元を **$k$ について一様に**与えたい。現在は $k\le4$ を個別計算しているだけで、$k=5,6$ は未知(札 N-3 が空白と名指し) | 自由 Lie 環 $\mathrm{Lie}(x,y)$ 上の**有限位数自己同型($\theta$: 位数 2 の対合、$\tau$: 位数 3 の巡回)のノルム作用素の核次元の母関数**。表現論(Klyachko / Kraskiewicz–Weyman 型の $\mathrm{Lie}_n$ の $S_n$-加群分解)から出る型を期待 |
| **L-2** | $\mathbb F_p$ 上の**層三角多項式系**(冪零 Lie 環の 1-コサイクル方程式)の解集合の次元・可解条件を、class について一様に扱う枠組み | 「等級つき Gröbner 基底が三角系で自明化する」ことの定式化、または非可換 1-コサイクル方程式の障害理論($H^1(\langle\alpha\rangle,\mathrm{gr}_\bullet)$ の層別) |
| **L-3** | $(2,3)$-生成有限群($=PSL_2(\mathbb Z)$ の有限商)の **reflexibility / chirality** の族的判定 — とくに $2^a3^b$ 型 | ★ **既出の要請**(`theorem_check_mirrorall_l3vacuous_v1.md` §A.5)。**本ノートで独立に同じ壁に当たったので優先度の上申**として再掲 |

---

## 付録 A — 本ノートで走らせた設計時プローブ(全ログ・**研究対象非接触**)

3 本とも「棚と GAP ライブラリのメタデータ」の照会であり、**窓・shadow・封印量に一切触れていない**。スクリプトは scratchpad 内(commit しない)。

**A-1 SmallGroups 射程**(`shelf_check.g`):
```
2000: ID-avail nr=963      1024: NOT-AVAILABLE     1536: LIB-only-noID nr=408641062
4000: NOT-AVAILABLE        4096: NOT-AVAILABLE     4500: NOT-AVAILABLE
6000: NOT-AVAILABLE        8000: NOT-AVAILABLE     2401: ID-avail nr=15
2187: LIB-only-noID nr=9310                        2048: NOT-AVAILABLE
```

**A-2 パッケージ**(`shelf_check2.g`): `liering / guarana / nq / gbnp / singular / polycyclic / autpgrp / anupq` すべて `load=true`。
Witt 数の確認: $W(2,k)_{k=1..6}=2,1,2,3,6,9$ / $W(3,k)_{k=1..5}=3,3,8,18,48$。
⟹ $\mathrm{gr}_k(K(0,5))=W(3,k)+W(2,k)$ が $5,4,10,21$(既在)を再現し、**class 5 なら $54$、class 6 なら $125$ が加わる**($\lvert Q\rvert=7^{94}$、$7^{219}$)。
$F_2$ 側: class 5 で $\lvert[P,P]\rvert=7^{12}=13{,}841{,}287{,}201$(宇宙 $6\cdot7^{12}\approx8.30\times10^{10}$)、class 6 で $7^{21}\approx5.6\times10^{17}$。
既在値の再計算: $7^8=5{,}764{,}801$ / $7^6=117{,}649$ / $6\cdot7^6=705{,}894$ / $6\cdot7=42$ / $10\cdot11^6=17{,}715{,}610$。

**A-3 帯とフィルタ**(`sg_band_probe.g`): §2.3 の表・§2.2 の通過率表・レート 1.336 ms/群(位数 1296・先頭 2000 群・2,672 ms)。

**API 名の確認**: `PGroupToLieRing`(liering)・`NqEpimorphismNilpotentQuotient`(nq)・`GroebnerBasis`(core)・`AttachedMalcevCollector`(guarana)が `IsBoundGlobal` で実在。`Lazard` を含む大域名は**存在しない**(Lazard 対応の入口は `PGroupToLieRing`)。

---

**本ノートは設計である。1 個の窓も、1 個の shadow も評価していない。**
