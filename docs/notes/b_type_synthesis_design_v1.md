# B 型の**合成**設計 — 「条件を満たす群を先に作る」への反転(v1)

**状態札: `design / candidate / 単系統・Sol 未監査 / 窓を 1 個も切っていない・shadow を 1 個も評価していない / 封印 3 量非接触(n=5 系・Im R・d_N)/ 機械は付録 A の整数・有理演算 2 本(窓非接触)のみ / ★ 本ノートは自分の導出を 1 本、内部整合で反証している(§2.4)`**

- 起草: 影工房 数学者(Claude / Opus 5)・2026-08-06
- 委嘱: 司令塔(研究者発案)—「**B 型であれば満たす条件を明示した群を先に構成し、shadow 所属を後段で確認する**」= 探索から合成への反転。TRI-LCS が設計図の裏面になる。
- 入力正本: `docs/notes/sat_line_applications_v1.md`(**定理 TRI-LCS**・§1.4 の破れ 4 か所)/ `docs/notes/hs_prop7_translation_v1.md`(D2/D3-BLIND・**D4-POWER**・D4-DUM/D4-PRED・HSP-SOUND・定義 NW)/ `docs/notes/bhunt_l1_bridge_v1.md`(**補題 BR-3**・§4.1 の [ICM] §6.1–6.4 逐語 pin・【BR-GAP-1】)/ `docs/notes/counterexample_hotspots_ideation_v1.md`(**札 5 DEPTH-2/MOD-691**・札 3)/ `docs/状態.md`(BH-α-pent v1.1・**|H_W|=42**・裁定 586)/ `docs/地図.md` 第 4 版
- **読んだ範囲**: `bhunt_l1_bridge_v1.md` は §0〜§4.3 と §7.1、`hs_prop7_translation_v1.md` は §1〜§3、`counterexample_hotspots_ideation_v1.md` は札 3・札 5 と §末尾。それ以外は未読。
- **novelty grep 済**: `TRI-LCS`(自作・既出)/ `DEPTH2_W`(司令塔命名・本ノートが初出)/ `𝔤𝔯𝔱`・`grt`・`Deligne–Ihara`・`Ihara–Takao`・`691` は **`counterexample_hotspots_ideation_v1.md` 札 5 にのみ既出**(ideator 発)。**本ノートは札 5 の内容を独立に再導出しており、その旨を §4 で明記する(先取り主張はしない)。**

---

## 0. 先に — 反転が何を変えたか、と一行の結論

### 0.1 反転の図式

| | 従来(探索) | ★ 反転後(合成) |
|---|---|---|
| 出発点 | 窓 $\mathbf N$ を固定 → 中の shadow を全部数える | **B 型が満たすべき条件**を先に書く → その条件を持つ群 $\widehat P$ を作る → 後段で「それが本当に窓の shadow か」を確認 |
| 律速 | 窓の大きさ($p^{\dim}$) | **条件リストの正しさ**(間違った条件で作ると存在しない物を追う) |
| 失敗の形 | 走り切れない | 作った群が窓に載らない(= 後段で落ちる) |
| ★ **TRI-LCS の役割** | 「層三角だから総当りで足りる」= **探索が易しい理由** | ★ 「層三角**である限り** B 型は出ない」= **合成が満たすべき第一条件は「層三角性の破れ」** — 同じ定理の裏面 |

### 0.2 ★ 一行の結論(**先に・不都合な方から**)

> $$\boxed{\ \textbf{冪零(verbal)窓では、B 型の有無は「重み }k\textbf{ ごとの 2 つの次元の比較」に完全に還元される。}\ }$$
> 算術側 = Soulé 元 $\sigma_3,\sigma_5,\sigma_7,\dots$ が生成する Lie 環の次元 $d_k$、GT 側 = hexagon $\wedge$ pentagon の各層の解空間の次元。**この 2 数が一致する限り B 型は原理的に存在しない**(§2.1)。
> $$\boxed{\ \textbf{class 4 では }1=1\textbf{ で一致 — これが }\lvert H_W\rvert=42\textbf{ の正体である(次元勘定だけで再現した・§2.1.3)。}\ }$$
> $$\boxed{\ \textbf{ゆえに冪零窓での合成標的は class}\ \ge12\ \textbf{ — 最小の明示 }P\ \textbf{は }13^{747}\textbf{ 級。合成は事実上不能(§1.4)。}\ }$$
> $$\boxed{\ \textbf{★ 合成が現実的なのは「層三角性が壊れる窓」= 非冪零成分をもつ交差窓ただ一つ。第一標的 }M=\mathrm{NW}(4,7)\cap K^{(7)}\ \textbf{(§3)}.\ }$$
> **重要なのは、この標的が推測でなく導出になったことである** — §1.4 の否定(冪零は class ≥ 12 が要る)と §2.2 の肯定(算術像を釘付けにできるのは dihedral 側だけ)の交差で、**残る場所が 1 つしかない**。

### 0.3 ★ 本ノートが自分で反証した主張(**先に出す**)

司令塔委嘱 ②(ii) の「BR-3 を深さ 4 に降ろす」を実行したところ、**内部矛盾に当たった**:

| 出所 | 深さ 4 の主張 | 格 |
|---|---|---|
| hexagon((3.10)+(3.11)) | 解空間 $=\mathbb Q\,\mathfrak h_4$、$\mathfrak h_4=v_1+4v_2+v_3$ | ★ **本ノートで独立再導出(付録 A-1・機械)** — D4-POWER (a) と一致 |
| BR-3 の素朴な深さ 4 延長(本ノートの導出) | $F_4=a\,(v_1+v_2+v_3)$ | ★ **機械計算(付録 A-2)** |
| 既測 | $\lvert H_W\rvert=42$ ⟹ $m\equiv0$ 層は **7 元** | 発効済(裁定 586) |

$(1,1,1)\parallel(1,4,1)\iff 3\equiv0$。$p=7$ では偽 ⟹ **$a=0$、$m\equiv0$ 層は 1 元** — **既測 7 元と矛盾**。
⟹ $\boxed{\textbf{本ノートの深さ 4 延長は偽である。}}$ 原因は §2.4【BSY-GAP-1】に局在(ACDIK 公式の転記が次数 4 で不完全か、$\mathrm{pr}(B'_\sigma)=\psi^{\rm ab}_\sigma$ に補正項があるか)。**合同式経路 (ii) は深さ 4 で使えない — 閉じるまで使わない。**

> ### ★ 副産物(**設計に効く警告**): $p=3$ は退化する
> $(1,1,1)\equiv(1,4,1)\pmod 3$。⟹ **玩具窓 NW(4,3)(札 N-2)は DEPTH2_W 系の較正窓として使ってはならない** — 判別すべき 2 つの直線が $\mathbb F_3$ で一致してしまう。**踏む前に捕まえた罠。**

---

## 1. ① B 型が存在し得る窓の**群論的必要条件**

### 1.1 導出の枠 — TRI-LCS の裏面

定理 TRI-LCS(`sat_line_applications_v1.md` §1.2): class $c<p$ の冪零窓では、hexagon も $\mathrm{PENT}_W$ も **下中心列に沿って層三角**(各層の主要項が $\mathbb F_p$-線型・非斉次項は下層の多項式)。Lazard 対応の下で $P$ の Lie 化 $\mathrm{gr}(P)\otimes\mathbb F_p$ は $\mathrm{Lie}(x,y)$ の class $c$ 切詰めであり、**$m\equiv0$ 層では非斉次項も消える**(§2.1.1)。

> ### ★ 命題 SYN-0(**合成の第一条件**)
> $m\equiv0$ 層で
> $$\mathrm{GT}^{\rm pent}(\mathbf N)_{m=0}\ \bigg/\ \mathrm{GT}^{\rm arith}(\mathbf N)_{m=0}\ \ne\ 1
> \quad\Longleftrightarrow\quad
> \exists k\le c:\ \dim_{\mathbb F_p}\mathcal S_k\ >\ \dim_{\mathbb F_p}\mathcal A_k$$
> ここで $\mathcal S_k$ = 深さ $k$ の hexagon $\wedge$ pentagon 斉次解空間、$\mathcal A_k$ = 算術像の深さ $k$ 層。
> **証明の骨**: 両辺とも層三角ゆえ、各層の自由度の積で位数が決まる($\lvert\cdot\rvert=p^{\sum_k\dim}$)。$\mathcal A_k\subseteq\mathcal S_k$(命題 HSP-SOUND: 算術 ⟹ pentagon)。∎(candidate)

**⟹ 冪零窓での B 型合成は「$\dim\mathcal S_k>\dim\mathcal A_k$ となる $k$ を含む class を持つ窓」を作ることに尽きる。**

### 1.2 条件リスト W-1〜W-8

| # | 条件 | 由来 | 満たさないとどうなるか |
|---|---|---|---|
| **W-1** ★ | $c\ \ge\ k^*:=\min\{k:\dim\mathcal S_k>\dim\mathcal A_k\}$ | 命題 SYN-0 | ★ **B 型は原理的に不在**(存在しない物を追う) |
| **W-2** | $p>c$(Lazard)**または** Lazard を諦めて非線型に扱う | TRI-LCS の前件 | $c\ge p$ で層の主要項が線型でなくなる(= §1.5 の (β) ルート) |
| **W-3** | $5\nmid\lvert Q\rvert,\ 5\nmid N_{\rm ord}$ | 篩 HSP-F の F-2($\rho$ の位数 5 でノルムが退化) | $\mathrm{PENT}_W$ が死ぬ ⟹ 上界装置がゼロ |
| **W-4** | $d(N)=\lvert\gamma_2(P)/\gamma_3(P)\rvert\ge2$ | 命題 HSP-COLLAPSE | 冪零 $Q$ 越しに $\mathrm{PENT}_W$ が恒真 |
| **W-5** | $N_{F_2}\cap\gamma_{k^*}(F_2)$ が判別方向を**含まない** | 篩 F-4 | 窓が浅すぎて判別座標を持てない |
| **W-6** ★ | **算術像 $\mathrm{GT}^{\rm arith}(\mathbf N)$ が独立に釘付けできる** | §2.2 | 「$\mathrm{GT}^{\rm pent}$ の方が大きい」が言えない(上界だけあっても無意味) |
| **W-7** | $\mathrm{SURJ}$・settled が判別に効かない/効くを事前に分けてある | 系 H8′(NW 側は識別力ゼロ)・GEN-AB(dihedral 側は $A=[P,P]$ 成分に集中) | 番人が二重にかかって B 型が A 型に化ける |
| **W-8** ★ | **上の全部を、層三角性が壊れる形で満たす**(= 交差 / 非 verbal / class $\ge p$) | §1.4 の否定 | 冪零のままでは W-1 が $c\ge12$ を要求して構成不能 |

### 1.3 「この条件を満たす最小の明示 $Q$」— 規模の実測見積り

$\mathrm{Lie}(x,y)$ の次数別階数(Witt・付録 A-3 で機械確認): $2,1,2,3,6,9,18,30,56,99,186,335$($k=1..12$)。
class $c$ の verbal 窓 $\mathrm{NW}(c,p)$ で $\lvert P\rvert=p^{W(c)}$、$W(c)=\sum_{k\le c}\mathrm{Witt}(2,k)$:

| $c$ | $W(c)$ | $\lvert P\rvert$ | $\lvert[P,P]\rvert$ | 悉皆宇宙 $(p-1)p^{W(c)-2}$ | $K(0,5)$ 側 $\lvert Q\rvert$ | SmallGroups |
|---|---|---|---|---|---|---|
| 4 | **8** | $7^8=5{,}764{,}801$ | $7^6$ | **705,894**(既走) | $7^{40}$ | ✗(位数 $7^8$ は不在) |
| 5 | 14 | $7^{14}$ | $7^{12}$ | $8.3\times10^{10}$ | $7^{94}$ | ✗ |
| 6 | 23 | $7^{23}$ | $7^{21}$ | $3.4\times10^{18}$ | $7^{219}$ | ✗ |
| **12** ★ | **747** | $13^{747}$ | $13^{745}$ | 論外 | $13^{(\gg)}$ | ✗ |

> $W(12)=2{+}1{+}2{+}3{+}6{+}9{+}18{+}30{+}56{+}99{+}186{+}335=\boxed{747}$(付録 A-3・機械)。
> ★ **この 747 は ideator 札 5 が独立に出していた値と一致する**(§4)。
> **SmallGroups は ID つきで位数 $\le2000$ + $2401=7^4$ のみ**(`sg_band_sweep_prereg_iffirst_v1.md` §3.1 の実測)⟹ **本節の $\widehat P$ はどれもライブラリに存在しない。構成は `nq`(冪零商)+ `polycyclic` の pc 構成、あるいは `liering` の Lazard 対応でしか作れない。**
> **`nq` で class $c$・指数 $p$ の相対自由群を作ること自体は $c\le6$ なら現実的**(pc 生成元 23 本まで)。**$c=12$(747 本)は未知数** — ただし**構成できても宇宙は列挙不能**なので、そこは SAT/制約系(`sat_line_applications_v1.md` §1.4 (β))の領分。

### 1.4 ★ 排除される窓族(**作っても無駄なもの** — これが本節の主要産物)

> ### 命題 SYN-1(**冪零窓の no-go**・candidate)
> 命題 SYN-0 と、$\mathcal A_k$ が「$\sigma_3,\sigma_5,\sigma_7,\dots$ が生成する Lie 環の $k$ 次成分」であること(§2.1.2)、$\mathcal S_k$ が「hexagon+pentagon の $k$ 次解空間」であることを認めると:
> $$\textbf{class }c\le k^*-1\ \textbf{の verbal 窓 }\mathrm{NW}(c,p)\ \textbf{には、どの }p\ \textbf{でも B 型は存在しない。}$$
> **⟹ NW(4,7)・NW(4,11)・NW(4,3)・NW(5,3)・NW(4,$p$) 全般は、B 型狩りの標的として原理的に空である。**($\mathrm{PENT}$ の検出比 $1/p$ の族データとしての価値は別 — 札 N-1 は生きている。)

$k^*$ の値そのものは古典的知見に依存する(§4・**要文献確認**)。**本ノートが自前で確定できるのは $k^*\ge5$ のみ**:
- $k=2$: $\dim\mathcal S_2=\dim\mathcal A_2=0$($m\equiv0$ で $c_2=0$)。
- $k=3$: $\dim\mathcal S_3=1$($\mathfrak h_3$・D3-BLIND)$=\dim\mathcal A_3$($\sigma_3$)。
- $k=4$: $\dim\mathcal S_4=0$(hexagon が $\mathfrak h_4$ を許し pentagon が殺す・D4-POWER)$=\dim\mathcal A_4$(偶数次に生成元なし)。
- ★ **累積 $1=1$ ⟹ $\lvert\mathrm{GT}^{\rm pent}\rvert_{m=0}=\lvert\mathrm{GT}^{\rm arith}\rvert_{m=0}=p$**、全体 $(p-1)\cdot p=6\cdot7=\boxed{42}$。**既測と一致**(§2.1.3)。
- $k=5,6$ は**未計算**(札 N-3【DEPTH-5】が名指しした空白)⟹ **$k^*$ の下から 2 段を埋めるのが最安の前進**(§3.2)。

### 1.5 層三角性を壊す 3 経路(= W-8 の実体・TRI-LCS §1.4 の再掲でなく**合成の観点からの評価**)

| 経路 | 合成できるか | 算術像は釘付けできるか(W-6) | 総合 |
|---|---|---|---|
| **(α) 交差窓**(非冪零成分) | ★ **できる**(2 つの既在窓の交叉・Goursat) | ★ **できる**(dihedral 側は Thm 4.3・NW 側は BH-α) | ★★ **唯一の現実解** |
| **(β) class $\ge p$** | pc 構成は可能だが宇宙が列挙不能 | 冪零ゆえ SYN-1 が効く($c\ge k^*$ が要る) | 大きすぎる |
| **(γ) 非 verbal(歪み窓・札 W-2)** | できる(⟨θ,τ⟩-軌道正規閉包) | ✗ **釘付けできない** — 算術像を計算する装置が無い | W-6 で落ちる |

$$\boxed{\ \textbf{(α) だけが W-1〜W-8 を全部通る。}\ }$$

---

## 2. ② 非算術証明書の 2 経路

### 2.1 経路 (i) 勘定 — **pentagon 通過数 > 算術像サイズ**

#### 2.1.1 定式化

$m\equiv0$ 層(= $\chi^{(p)}(\sigma)=1$ の層)に限る。理由: (a) この層でのみ BR-3 型の算術記述が使える (b) $c_2=m(m+1)/6=0$ ゆえ hexagon の非斉次項が消え、**完全に斉次な層別勘定になる**。

$$\lvert\mathrm{GT}^{\rm pent}(\mathbf N)_{m=0}\rvert=p^{\,\sum_{k=3}^{c}\dim\mathcal S_k},\qquad
\lvert\mathrm{GT}^{\rm arith}(\mathbf N)_{m=0}\rvert=p^{\,\sum_{k=3}^{c}\dim\mathcal A_k}\ \ (\text{飽和なら等号}).$$

#### 2.1.2 $\mathcal A_k$ の正体

[ICM] §6.3 の ACDIK 公式(BH ノート §4.1 (iii) 逐語)は $\chi^{(p)}(\sigma)=1$ の層で
$$\psi^{\rm ab}_\sigma=\exp\Bigl\{\sum_{m\ge3,\ \rm odd}\frac{\kappa^*_m(\sigma)}{m!}\bigl((X+Y)^m-X^m-Y^m\bigr)\Bigr\}$$
(偶数 $m$ の因子は $1-\chi(\sigma)^m$ が $p$ 進的に $0$ ゆえ消える)。**パラメータは奇数 $m\ge3$ ごとに 1 個**、$\kappa^*_m$ は Soulé–Deligne 円分元。したがって

$$\boxed{\ \mathcal A_\bullet=\text{「次数 }3,5,7,9,\dots\text{ に生成元を 1 個ずつ持つ Lie 環」の次数別成分.}\ }$$

自由と仮定した場合の次元(付録 A-3・機械):

| $k$ | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\dim\mathcal A_k$(自由の場合) | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 2 | 2 |

⚠ **自由性は仮定である**(§4・要文献確認)。**自由でなければ $\dim\mathcal A_k$ は下がり、$\mathcal S_k$ との差が開く = B 型が出やすくなる。**

#### 2.1.3 ★ class 4 での検算(**枠組みの妥当性の唯一の実証**)

$\sum_{k\le4}\dim\mathcal S_k=1+0=1$、$\sum_{k\le4}\dim\mathcal A_k=1+0=1$。
$$\lvert\mathrm{GT}^{\rm pent}\rvert=(p-1)\cdot p^1\ \overset{p=7}{=}\ 6\cdot7=\boxed{42}\ =\ \lvert H_W\rvert.$$
> ★ **BH-α-pent の実測 42 が、窓を 1 個も評価せずに次元勘定だけで再現した。** これが本節の枠組みが正しいことの(唯一の、しかし強い)証拠である。
> ⚠ **格**: 42 は既測ゆえ「予言」ではない(事後の整合確認)。**枠組み自体は candidate。**

#### 2.1.4 判定基準

$$\boxed{\ \exists k\le c:\ \dim\mathcal S_k>\dim\mathcal A_k\ \Longrightarrow\ \textbf{B 型が存在}\ }$$
かつ差の総和が B 型の「個数の対数」を与える。**これが勘定経路の完全な形である。**

### 2.2 算術像を釘付けにできる窓クラス(**W-6 の実体**)

| 窓クラス | 上界(pentagon 側) | 下界(算術側) | 釘付け可? |
|---|---|---|---|
| **dihedral $K^{(n)}$** | Thm 4.3 の明示式 | Thm 4.3 + $u_n$ 測定(BFC)+ FAM-U-ASM | ★ **できる**(両側が明示式) |
| **NW$(c,p)$** | hexagon+PENT の層勘定 | ★ **BH-BRIDGE**($\kappa^*_3$ 非消滅 ⟹ 深さ 3 が飽和) | ★ **できる**(class 4 は実証済) |
| **壁窓**($A_n$ 型) | $\mathrm{PENT}$ は恒真(HSP-COLLAPSE) | 装置なし | ✗ |
| **PSL(2,8) 窓** | 悉皆 54 済 | ✗(非合同ゆえ $u$/Kummer 圏外・ideator 札 3) | ✗(**上界だけ**) |
| **歪み窓(非 verbal)** | 計算可 | 装置なし | ✗ |

> ### ★ SURJ / H8′ の適用条件(**委嘱の指定項目**)
> - **系 H8′**(NW 側): 全 charming が SURJ を通る ⟹ **SURJ の識別力はゼロ**。よって NW 系では「$\mathrm{GT}^{\rm pent}$ が大きい = B 型」がそのまま読める(A 型との混同が起きない)。★ **これは合成にとって好都合**である。
> - **GEN-AB**(dihedral 側): SURJ の識別力は $A=[P,P]$ 成分に集中。⟹ dihedral 側では「pentagon を通るが SURJ で落ちる」= **A 型**が実在し得る。**交差窓 (α) では両者が同居する** ⟹ **A 型と B 型の分離が必須**(§3.3 の停止規則)。
> - **⟹ 交差窓では「SURJ で落ちるか」を B 型判定の前に必ず先に見る。** これが札 N-4 の「fake が棲めるニッチが最も立体的」の実務上の意味である。

### 2.3 経路 (ii) 合同式 — ACDIK からの深さ別必要条件

$\chi^{(p)}(\sigma)=1$ の層で、算術元は**深さごとに次の必要条件**を満たす:

| 深さ | 必要条件 | 識別力 | 格 |
|---|---|---|---|
| **2** | $c_2=0$ | ★ **ゼロ**($m\equiv0$ から自動) | 定理(BR-3 (d)) |
| **3** | $F_3=a\,\mathfrak h_3$、$a=-\kappa^*_3(\sigma)/2$ | ★ **ゼロ**(hexagon が同じ直線を与える・D3-BLIND) | 定理(BR-3・単系統) |
| **4** | ? | ★ **不明** | ★ **【BSY-GAP-1】**(§2.4) |
| $\ge5$ | $\kappa^*_5$ 以降が入る | 未計算 | — |

> ★ **深さ 2・3 が識別力ゼロなのは偶然ではない**: pentagon 側の D2-BLIND / D3-BLIND と**同じ深さで同じように盲目**である。**算術側と pentagon 側は同じ盲点構造をもつ** — これが「class 4 で 42 = 42」の構造的理由であり、§2.1 の勘定がそれを次元の言葉で言い直したものである。

### 2.4 ★ DEPTH2_W の定義候補と、深さ 4 の内部矛盾

司令塔の命名 `DEPTH2_W` は「$\mathrm{PENT}_W$ の一階上の判別不変量」。**$\mathrm{PENT}_W$ が深さ 4 に効くので、その一階上 = 深さ 5 以上**である。一方 BR-3 の合同式は $\gamma_4$ 法(= 深さ 3)にある。**名前と深さがずれているので、以下では 3 案を分けて定義し、名前は司令塔裁定に委ねる。**

| 案 | 定義 | 識別力 | 状態 |
|---|---|---|---|
| **D2W-a**(素朴) | 「$F_3$ が $\mathfrak h_3$ 直線に乗る」 | **ゼロ**(hexagon と同値) | 却下 |
| **D2W-b**(深さ 4) | ACDIK の 4 次項から出る $F_4$ の線型条件 | 本来ここが本命 | ★ **【BSY-GAP-1】で凍結** |
| **D2W-c**(★ 推奨・構造形) | $$\mathrm{DEPTH2}_W(\bar f):\iff \bar f\ \text{の層座標が}\ (\kappa^*_3,\kappa^*_5,\dots)\ \textbf{1 本の族の像に乗る}$$ すなわち**深さ $\le c$ の座標が奇数次パラメータの個数だけで決まる** | ★ **勘定経路と同一**(§2.1) | ★ **こちらは生きている** |

> ### ★★【BSY-GAP-1】 深さ 4 の内部矛盾(**本ノートが自分で見つけた反証**)
> 委嘱 ②(ii) を実行して得た導出:
> $\mathrm{pr}(B'_\sigma)=1+\xi\eta\cdot\mathrm{pr}(h)$(BH ノート (4.2))と $\mathrm{pr}(B'_\sigma)=\psi^{\rm ab}_\sigma$((6.4.4))を**次数 4 で**突き合わせると、
> $$[\mathrm{pr}\,h]_2=-\frac{\kappa^*_3}{2}(\xi^2+\xi\eta+\eta^2)\quad\Longrightarrow\quad F_4=a\,(v_1+v_2+v_3),\ \ a=-\kappa^*_3/2$$
> (付録 A-2 で機械確認。$X=\log(1+\xi)$ の高次補正が次数 4 を生む — 奇数 $m$ の構造からは 4 次項が出ないので**この補正だけ**が残る)。
> ところが hexagon は $F_4\in\mathbb Q(v_1+4v_2+v_3)$ を要求する(**付録 A-1 で独立再導出・D4-POWER (a) と一致**)。
> $(1,1,1)\parallel(1,4,1)\iff3\equiv0$。$p=7$ で偽 ⟹ $a=0$ ⟹ $m\equiv0$ 層は **1 元**。
> **既測 $\lvert H_W\rvert=42$ は同層が 7 元であることを要求する(裁定 586・$u$-写像は $(\mathbb Z/7)^\times$ 上全射ゆえ核は 7 元)。**
> $$\boxed{\ \textbf{矛盾。ゆえに上の深さ 4 導出は偽である。}\ }$$
> **原因の候補(3 つ・いずれも未判定)**:
> 1. BH ノート §4.1 (iii) の ACDIK 公式の転記が**次数 4 で不完全**(偶数 $m$ 因子の扱い、または第 1 指数の項の欠落)。
> 2. $\mathrm{pr}(B_\sigma)=\psi^{\rm ab}_\sigma$((6.4.4))に**次数 4 で効く補正**がある。
> 3. $h$ の $\gamma_4$ 基底への値 $h(v_1)=(1-\underline x)^2$ 等の同定に規約ずれ(**罠 D-6 族**)。
>
> **処置**: **合同式経路 (ii) は深さ 4 以上で使用禁止**(【BSY-GAP-1】が閉じるまで)。**勘定経路 (i) は無傷**(ACDIK の次数 4 の値を使わず、**パラメータの個数しか使わない**から)。
> **要請**: [ICM] 印字 115–116(PDF 203–204)§6.3 の Theorem $[A_3,C_3,\rm IKY]$ と §6.4 (6.4.2)(6.4.4) の **400dpi 頁画像 pin**(reader 案件)。BH ノートは深さ 3 までしか使っておらず、**この転記は深さ 4 では未検証である**。

### 2.5 2 経路の比較

| | (i) 勘定 | (ii) 合同式 |
|---|---|---|
| 必要な入力 | 各層の**次元**だけ | ACDIK の**係数**まで |
| 現在の状態 | ★ **生きている**(class 4 で 42 を再現) | ★ **深さ 4 で凍結**(【BSY-GAP-1】) |
| 出す証明書 | 「$\lvert\mathrm{GT}^{\rm pent}\rvert>\lvert\mathrm{GT}^{\rm arith}\rvert$」= **個数** | 「この元は算術でない」= **元ごと** |
| 弱点 | 飽和(【BR-GAP-1】)に依存 — 下界が下がると差が消える | 転記の正しさに全体重 |
| ★ 推奨 | ★ **主経路** | 【BSY-GAP-1】が閉じてから**照合器**として |

---

## 3. ③ 最小実験 — 最初に作るべき 1 個

### 3.1 ★ 実は先に走らせるべき「窓ゼロ」の実験(**0 円・最優先**)

命題 SYN-1 が効く以上、**群を作る前に $k^*$ を知らねばならない**。そして $k^*$ の下 2 段は**窓なしで**計算できる:

> ### 実験 **E-DIM5/6**(窓非接触・純線型代数)
> $\mathrm{Lie}(x,y)\otimes\mathbb Q$ の次数 5・6 成分(階数 6・9)で
> $$\dim\mathcal S_k=\dim\bigl(\ker(1+\theta)\cap\ker(1+\tau+\tau^2)\cap\ker\nu_k\bigr)$$
> を厳密有理計算する($\nu_k=\sum_{i=0}^4\rho^i$ を $\mathfrak t=\mathrm{gr}(K(0,5))\otimes\mathbb Q$ 上で)。**付録 A-1 のスクリプトを次数 5,6 へ伸ばすだけ**(既存装置 `hs_prop7_hexagon_vs_pentagon.py` 系の拡張・札 N-3 の「検証の一手目」と同一)。
> **比較対象**: $\dim\mathcal A_5=1$、$\dim\mathcal A_6=0$。
> ★ **$\dim\mathcal S_6\ge1$ が出たら $k^*=6$** — その瞬間に **class 6・$p=7$ の窓($\lvert P\rvert=7^{23}$)が B 型を含むことが紙で確定する**。宇宙 $3.4\times10^{18}$ は悉皆不能だが、**層消去すれば自由度は $\sum\dim\mathcal S_k$ 個だけ**(数個)⟹ **即座に明示的な B 型 witness が構成できる**。
> **費用**: 数学者+実装係の 1 日。**窓もゼロ、GAP もゼロ。**

> $$\boxed{\ \textbf{委嘱に対する最も正直な回答: 「最初に作るべき群」より先に、「作る価値があるかを決める }10^0\textbf{ 円の計算」がある。}\ }$$

### 3.2 群を作る場合の第一標的 — $M=\mathrm{NW}(4,7)\cap K^{(7)}$

E-DIM5/6 が「$k^*\ge7$」を出した場合(= 冪零ルートが遠い場合)の標的。**§1.4 の否定と §2.2 の肯定の交差で一意に決まる**:

| 要件 | $M$ での充足 |
|---|---|
| W-8(層三角性が壊れる) | ★ $P_M$ は dihedral 因子($D_7$・非冪零)を含む ⟹ 全域の LCS 三角性が壊れる |
| W-6(算術像の釘付け) | ★ **両側で可能**: $K^{(7)}$ 側 = Thm 4.3 + $u_7$ 発火済、NW 側 = BH-α |
| W-3(標数 5 排除) | ★ $\lvert P_M\rvert$ は $2,7$ のみ |
| W-4($d(N)\ge2$) | ⚠ **要確認**: $K^{(7)}$ 側は $d=1$(命題 D-ODD: $4\nmid n$)・NW 側は $d\ge2$。**交差でどちらが勝つかが最初の計算** |
| W-7(A 型/B 型の分離) | ★ 系 H8′ と GEN-AB が**同居する唯一のクラス**(札 N-4)⟹ 分離が可能かつ必須 |

**構成**: $N_M:=\mathcal V(F_2)\cap K^{(7)}_{F_2}$、$P_M=F_2/N_M$。Goursat により $P_M\hookrightarrow P_{\rm NW}\times P_{K}$ の部分直積。$\lvert[P_M,P_M]\rvert\le7^9\approx4.04\times10^7$(札 N-4 の見積り)。
**作り方**: `nq` で $P_{\rm NW}$($7^8$)、正典 Thm 4.3 で $P_K$、`polycyclic` で部分直積 — **すべて棚にある**(`sat_line_applications_v1.md` §3)。

### 3.3 prereg 雛形(**走行しない・凍結用**)

```
docs/notes/xwin_m7_prereg_iffirst_v1.md   (雛形・未起票)
 §1 宇宙の凍結 : N_M の定義式 / |P_M| / |[P_M,P_M]| / X_N / 実行環境 / cap
 §2 述語の凍結 : hexagon(3.3)(3.4) full / PENT_W / SURJ / settled / ∉H_W
 §3 前件の確認 : W-3,W-4,W-6,W-7 を「走る前に紙で」判定(W-4 が最初の分岐)
 §4 予言(IF-FIRST):
     P-XW-1 d(N_M) の値(1 か 2 か)             ← W-4 の採点
     P-XW-2 |GT^pent(M)| と |GT^arith(M)| の比  ← 勘定経路の採点
     P-XW-3 SURJ 落ちの件数(A 型の個数)        ← GEN-AB の採点
     P-XW-4 fiber が空かどうか(札 N-4 の懸念)
 §5 較正 : DF-XW-1 dummy exp(t·h4) が PENT FAIL(系 D4-DUM の交差版)
           DF-XW-2 K^(7) 側へ落として Thm 4.3 と一致(既知への回帰)
           DF-XW-3 NW 側へ落として H_W(42)と一致
 §6 停止規則: S-XW-1 SURJ 落ち候補を B 型と書いたら OVERCLAIM/STOP(A 型と分離)
           S-XW-2 W-4 が d=1 と出たら SCOPE_OUT/STOP(HSP-COLLAPSE)
           S-XW-3 【BSY-GAP-1】が開いている間、合同式経路の値を判定に使わない
           S-XW-4 B 型候補 1 件で即停止・司令塔へ(札 F-1 の着弾 protocol)
 §7 射程限定: 「M における」までしか主張しない
```

---

## 4. ④ ideator hotspots(691 / weight 12 / Δ)との接続

**本ノートの §2.1 は、ideator 札 5【DEPTH-2 / MOD-691】と独立に同じ住所に着地した。** 先取りではない — 札 5 が先行し、本ノートは**構造から再導出した**。

| 項目 | ideator 札 5(先行・2026-08-05) | ★ 本ノート(独立再導出) |
|---|---|---|
| 場所 | 「重み 12 が見える円分 verbal 窓(class 12)」 | 命題 SYN-0/SYN-1 から $c\ge k^*$、古典的知見で $k^*=12$(§4 の要請) |
| 窓の大きさ | 「$691^{747}$ 級($\mathrm{gr}\le12$ の階数和 747)」 | ★ **$W(12)=747$ を Witt 数から独立に機械確認**(付録 A-3) |
| 機構 | 「偶重み 12 層は交換子供給のみ・$[\sigma_3,\sigma_9],[\sigma_5,\sigma_7]$ が Ihara–Takao 関係で 1 次元に落ちる」 | ★ **$\dim\mathcal A_k$ vs $\dim\mathcal S_k$ の比較**として定式化(§2.1.4)。札 5 の「落ち方の不一致」= 本ノートの「$\dim\mathcal S_{12}>\dim\mathcal A_{12}$」 |
| $\ell=691$ | Ramanujan 合同 $691\mid B_{12}$ で供給の独立性勘定が退化 | ★ **本ノートは $\ell$ を選ぶ理由を持たない** — 勘定は標数 0 でも成立する。**691 は「$\mathbb Z$ 上一致しても $\bmod\ 691$ でずれる」という第 2 段の機構**であり、札 5 の固有の貢献である(本ノートはそこに届いていない) |
| 深さ(depth) | $y$-次数フィルトレーション(MZV の depth) | ★ **本ノートは重み(LCS class)しか見ていない** — 札 5 の depth 軸は**直交する第 2 の軸**。両方要る |

> ### ★ 統合(**両者を合わせて初めて言えること**)
> $$\text{B 型の住所}=\bigl(\text{重み }k^*\ \text{= 本ノートの勘定}\bigr)\ \times\ \bigl(\text{depth 2・}\ell=691\ \text{= 札 5}\bigr).$$
> **本ノートの寄与は「重み軸で $k^*$ より下は原理的に空」を命題 SYN-1 として固定したこと**(= 札 5 が名指した class 12 より下を全部掃除したこと)。**札 5 の寄与は class 12 の中のどこを見るかを名指ししたこと。**
> ⟹ ★ **札 5 は「夢級」から「唯一残った番地」へ昇格する** — 他が全部空だと分かったから。

> ### ★ 系 SYN-IHARA(**この線の正体**・candidate)
> 命題 SYN-0 は、$\mathcal A$ = Soulé 元の生成する Lie 環、$\mathcal S$ = hexagon+pentagon の解 Lie 環 と読めば
> $$\textbf{冪零窓での B 型の存在}\ \iff\ \mathcal S\supsetneq\mathcal A\ \text{が有限次数で見える}$$
> であり、これは **Deligne–Ihara 型の主張(GT Lie 環が Soulé 元で生成される)の有限窓版**である。
> ⟹ **B 型狩りは「井原予想の Lie 環版を低重みで反証する試み」そのもの**である。地図第 4 版の軸 (i)(算術飽和)と軸 (ii)(理論同定)がここで 1 点に合流する。
> ⚠ **この同定は本ノートの読みであり、古典的知見の側は未確認**(§5 の【文献要請】L-4)。

---

## 5. GAP と【文献要請】

**未閉のギャップ**:
- **【BSY-GAP-1】**(§2.4)★ 深さ 4 の合同式が既測 42 と矛盾。**合同式経路は深さ $\ge4$ で使用禁止。**
- **【BSY-GAP-2】** 命題 SYN-0/SYN-1・系 SYN-IHARA は本ノート起草の candidate(単系統・Sol 未監査)。**「NW(4,$p$) に B 型は原理的にない」を確定として引用しない。**
- **【BSY-GAP-3】** $\dim\mathcal A_k$ の表(§2.1.2)は「$\sigma$ 達が**自由**」を仮定。自由でなければ表は下がる(= B 型が出やすくなる方向)。
- **【BSY-GAP-4】** $\dim\mathcal S_5,\dim\mathcal S_6$ は未計算(= 実験 E-DIM5/6)。$k^*$ の下限は現状 $5$ しか言えない。
- **【BSY-GAP-5】** 交差窓 $M$ の $d(N_M)$・Goursat 構造は未計算(W-4 の分岐)。

**【文献要請】**:

| # | 具体的な技術的困難 | 欲しい結果の型 |
|---|---|---|
| **L-4** ★★ | §2.1 の勘定は $\dim\mathcal S_k$(hexagon+pentagon の $k$ 次解空間)と $\dim\mathcal A_k$($\sigma_3,\sigma_5,\dots$ の生成する Lie 環)の比較に尽きる。**この 2 列の低次数の値**(とくに $k=5,\dots,12$)と、**両者が一致する最大の $k$** を知りたい | 「GT Lie 環の次数別次元」と「Soulé/motivic 側の次数別次元」の**低次数の表**(計算済みのはず)。両者の一致範囲が $k^*$ を直接与える。**これが分かれば §3.1 の実験の答え合わせが即座にできる** |
| **L-5** ★ | 【BSY-GAP-1】: [ICM] §6.3 Theorem $[A_3,C_3,\rm IKY]$ と §6.4 (6.4.2)(6.4.4) の**次数 4 における正確な形** | ★ **文献検索でなく reader の頁画像 pin で足りる**(現物 `papers/ihara-ICM1990-vol1-braids-galois-arithmetic.ocr.pdf` は既在・印字 115–116 = PDF 203–204・400dpi)。**最優先** |
| **L-6** | 札 5 の Ihara–Takao 関係 $[\sigma_3,\sigma_9]-3[\sigma_5,\sigma_7]$ の**明示係数**と、$\bmod\ 691$ での退化の有無 | ideator 札 5 の (J-ii) と同一 — **重複要請につき統合を上申** |

---

## 付録 A — 本ノートで走らせた計算(**全申告・窓非接触**)

スクリプト: `scratchpad/bsyn_check.py`(python・分数演算のみ・commit しない)。**GAP を起動していない。窓・shadow・封印量に一切触れていない。**

**A-1 $\mathrm{gr}_3,\mathrm{gr}_4$ 上の $\theta,\tau$ 作用と $\mathfrak h_4$ の独立再導出**
自由結合代数の中の Lie 元として $u=[x,y]$、$u_1=[u,x]$、$u_2=[u,y]$、$v_1=[u_1,x]$、$v_2=[u_1,y]$、$v_3=[u_2,y]$ を構成($\theta:x\!\leftrightarrow\!y$、$\tau:x\mapsto y,\ y\mapsto-x-y$)。出力:
- Hall 関係 $[[u,y],x]=v_2$ ✔
- $\theta(u_1)=-u_2,\ \theta(u_2)=-u_1$;$\tau(u_1)=u_2,\ \tau(u_2)=-u_1-u_2$;$(1+\theta)\mathfrak h_3=0$、$(1+\tau+\tau^2)|_{\mathrm{gr}_3}=0$
- $\theta(v_1)=-v_3,\ \theta(v_2)=-v_2,\ \theta(v_3)=-v_1$;$\tau(v_1)=v_3,\ \tau(v_2)=-v_2-v_3,\ \tau(v_3)=v_1+2v_2+v_3$
- ★ $\ker(1+\theta)\cap\ker(1+\tau+\tau^2)$ の整数解($\alpha=1$ 正規化)$=\{(1,4,1)\}$
$$\Longrightarrow\ \boxed{\mathfrak h_4=v_1+4v_2+v_3}\quad\textbf{— D4-POWER (a) を独立に再導出}$$

**A-2 ACDIK 級数の次数 4(【BSY-GAP-1】の機械的根拠)**
$\kappa^*_3=1$、$X=\log(1+\xi)$、$Y=\log(1+\eta)$ として $\exp\{\frac12(X^2Y+XY^2)\}$ を全次数 4 まで展開:
- 次数 2: **なし**(⟹ $c_2=0$・BR-3 (d) と一致)
- 次数 3: $\tfrac12(\xi^2\eta+\xi\eta^2)$(⟹ $a=b$・BR-3 と一致)
- 次数 4: $-\tfrac12(\xi^3\eta+\xi^2\eta^2+\xi\eta^3)$ ⟹ $[\mathrm{pr}\,h]_2=-\tfrac12(\xi^2+\xi\eta+\eta^2)$ ⟹ $(\alpha,\beta,\gamma)\propto(1,1,1)$
- 比率テスト $(1,1,1)\parallel(1,4,1)\bmod p$: $p=3$ **真**、$p=5,7,11,13$ **偽**
$$\Longrightarrow\ \textbf{A-1 と既測 42 に矛盾 ⟹ 本ノートの深さ 4 延長は偽(§2.4)。かつ }p=3\textbf{ は退化窓。}$$

**A-3 次元表**
$\mathrm{Witt}(2,k)_{k=1..12}=2,1,2,3,6,9,18,30,56,99,186,335$、累積 $W(12)=\boxed{747}$。
$\mathcal A$(次数 $3,5,7,\dots$ に生成元 1 個ずつの自由 Lie 環)の次数別次元 $k=3..12$: $1,0,1,0,1,1,1,1,2,2$(母関数 $1/(1-\sum_{m\ \rm odd\ge3}t^m)$ の分解)。

---

**本ノートは設計である。窓を 1 個も切っていない。そして自分の導出を 1 本、内部整合で反証している(§0.3・§2.4)。**
