# Lazard 後の窓 設計 v1 — Γ 盾の縁を窓側から見る(裁定 774・研究者発案)

**状態札: `IF-FIRST 設計(凍結が先・測定していない)/ candidate / Sol 未監査 / GAP 実走ゼロ・cert 発行ゼロ / 判定語なし / S₁₂ 系 blind 該当なし / 実走は仕様化まで`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-07 / 委嘱: 司令塔(**裁定 774**・研究者発案「これを自分たちの窓を通して見られないか」)
- 前提正本: `cone_design_v1_addendum_c/d.md`(定理 CC-1★・系 CC-1a)/ `p2_address_strike_design_v1.md`(命題 P2-1)/ `ideas_protective_structure_v1.md`(五層盾・W 盾)/ `b_type_synthesis_design_v1.md`(定理 TRI-LCS「class = weight」・SYN-0/W-1・verbal 窓 NW(c,p))/ `ribet_dig_campaign_v1.md`(罠 DEPTH-WEIGHT)
- **自前検算**: §2.1 の幅・§3.2 の $\sum\dim\mathcal S_k$・§4.2 の metabelian 次元は python(整数・分数のみ・GAP 不使用・cert ではない)。再現コマンドは §2.2。

---

## 0. 判定(先に 5 行)

| # | 事項 | 結果 |
|---|---|---|
| **①** ★★★ | **境界一致は (b) 構造的** | 両境界とも「**分冪 $\gamma_n(x)=x^n/n!$ の $p$-整性が切れる**」の一事象。Lazard は BCH の $1/n!$、Γ 盾は Bernoulli の**指数型母関数** $\frac t{e^t-1}=\sum B_n\frac{t^n}{n!}$ の $1/n!$。**同一の不等式 $p\le n$ を、二つの次数($n=c$ / $n=k$)に代入したもの**であり、両者が**同一の線**になるのは工房既在の **TRI-LCS「class $=$ weight」**を通したときちょうど(§1) |
| **②** ★★ | **W 盾の Lazard 柱が倒れる縁 = Γ 縁の窓側双子** | 精密文を §1.3 に。★ しかも **$\Gamma$ は分冪代数の記号そのもの** — 盾の命名が事後に正当化される |
| **③** ★★ | **最小ラボは立つ** | $p=5$・class 5(幅 14・$5^{14}=6.1\times10^9$)は**pc 群として構成可能**。★ ただし $f\in P$ の悉皆($5^{14}$ 通り)は不可 ⟹ **次数別解法**(hexagon を $\gamma_k/\gamma_{k+1}$ ごとに解く)が必須で、それは Lie 側予言との突合そのもの ⟹ **設計が自然に噛み合う**(§2) |
| **④** ★★★ | **予言の分岐点は class $=p$ ちょうど** | 欠損量 $\mathrm{def}(c,p):=\log_p\lvert GT^{\rm pent}_{m=0}(NW(c,p))\rvert-\sum_{k\le c}\dim\mathcal S_k$ を定義。**$c<p$ で $0$・$c=p$ が最初にずれうる点**。$p=5$: $c=4$ で $\sum=1$、**$c=5$ で $\sum=2$** ⟹ 凍結値 $\lvert GT_{m=0}\rvert=25$。$p=7$: $c=6$ で $2$、**$c=7$ で $3$** ⟹ $343$(§3) |
| **⑤** ★★★ | **道 1(metabelian)は原理的に潰れる** | 自由 metabelian Lie 環(2 生成)の多重次数 $(k-2,2)$ 部分は **1 次元**(基底 $[y,x,x^{k-3},y]$ が一意)。自由 Lie の深さ 2 は $(k-2)/2$ ⟹ $k=278$ で $138\to1$ = **情報の 99% 消失**。★ **しかも P2 打撃の再照準により床は $68\times138$ で直接計算できる ⟹ 道 1 は不要**(§4) |

---

# 1. 境界一致の検分

## 1.1 二つの境界の出所

| 盾 | 境界 | 出所の分母 |
|---|---|---|
| **Lazard 柱**(W 盾) | class $c<p$ で群 $\leftrightarrow$ Lie 対応が成立・$c\ge p$ で破綻 | BCH 級数 $\log(e^Xe^Y)=X+Y+\tfrac12[X,Y]+\tfrac1{12}[X,[X,Y]]-\cdots$。次数 $n$ の項の分母の素因数は $\le n$ ⟹ **$p$-整 $\iff p>c$**。根は $\exp(X)=\sum X^n/n!$ の **$1/n!$** |
| **Γ 盾** | $p\le k$($\iff v_p(k!)\ge1$)で ζ 正規化が $p$ を吸収しうる | $\zeta(k)\pi^{-k}=\pm B_k2^{k-1}/k!$。根は Bernoulli の**指数型母関数** $\dfrac t{e^t-1}=\sum B_n\dfrac{t^n}{n!}$ の **$1/n!$** |

> ### 命題 BOUND-ID(candidate・本ノート)
> 素数 $p$、整数 $n\ge1$ について次は同値:
> $$\textbf{(i) } p\le n\qquad \textbf{(ii) } v_p(n!)\ge1\qquad \textbf{(iii) } \gamma_n(x)=\frac{x^n}{n!}\ \text{が }\mathbf Z_{(p)}\ \text{上整でない}$$
> **証明.** (i)⟺(ii): $v_p(n!)=\sum\lfloor n/p^i\rfloor\ge1\iff\lfloor n/p\rfloor\ge1\iff p\le n$。(ii)⟺(iii): 定義。∎
> $$\boxed{\ \textbf{Lazard の縁} = \textbf{(i) を }n=c\ \textbf{(class) に代入};\qquad \Gamma\ \textbf{盾の縁} = \textbf{(i) を }n=k\ \textbf{(weight) に代入}\ }$$

## 1.2 ★★ 判定: **(b) 構造的**(ただし一段の橋が要る)

- **(a) 偶然の数値一致ではない**: 両者とも**分冪(divided power)$\gamma_n$ の $p$-整性**という同一の代数的事象。Lazard は指数写像の分冪、Bernoulli は EGF の分冪。
- **ただし厳密には「同じ不等式の二つの代入」であって、自動的に同一の線ではない。** 同一になるのは **class と weight を同一視する目盛り**を通したときである。
- ★ その目盛りは**工房既在**: 定理 **TRI-LCS**(Lazard・`b_type_synthesis_design_v1.md`)の
$$\boxed{\ \textbf{窓の class}\ =\ \textbf{Lie 側の weight}\ }$$
(罠 DEPTH-WEIGHT で明文化済)。
$$\Longrightarrow\ \boxed{\ \textbf{TRI-LCS の下で }c=k\ \textbf{ゆえ、Lazard 境界 }c<p\ \textbf{と }\Gamma\ \textbf{盾境界 }k<p\ \textbf{は同一の線である。}\ }$$

> ### ★ 自己言及的な整合(記録)
> TRI-LCS 自身が **Lazard 対応**によって成り立つ定理である ⟹ 「class = weight」は **$c<p$ の域でのみ保証**される。
> $$\boxed{\ \textbf{二つの境界を同一視する橋(TRI-LCS)は、その境界のところでちょうど落ちる。}\ }$$
> ⟹ **境界の内側では「同一の線」と言えるが、外側ではそもそも同一視が保証されない** — これが本設計が測ろうとしている当のものである(循環ではなく、**橋が落ちる場所を橋の内側から外挿して測る**構図)。

## 1.3 W 盾の Lazard 柱の縁 = Γ 縁の窓側双子(**精密文**)

> ### 命題 TWIN-EDGE(candidate・本ノート)
> 番地 $(k,p)$ について:
> - $p>k$(**帯外**): Γ 盾は完全($v_p(k!)=0$ ⟹ ζ 正規化は $p$ を吸収できない)**かつ** class $=k<p$ ⟹ Lazard 対応が成立(窓 = Lie 模型)。
> - $p\le k$(**帯内**): Γ 盾に縁が生じる($v_p(k!)\ge1$)**かつ** class $=k\ge p$ ⟹ **Lazard 対応が破綻**(窓 $\ne$ Lie 模型)。
> $$\boxed{\ \textbf{「A 側で ζ 正規化が }p\ \textbf{を飲み込む」と「窓側で群が Lie 模型から離れる」は、同じ }p\le k\ \textbf{の二つの顔である。}\ }$$
> ★ 記号の一致は偶然でない: **$\Gamma$ は分冪代数(divided power algebra)の標準記号**であり、盾の命名が事後に正当化される。
> ⚠ **【PL-GAP-1】**: 上は TRI-LCS(class $=$ weight)を前提とする。TRI-LCS 自体が Lazard 依存なので、**$p\le k$ 側で「class $=$ weight」を使う言明は外挿である**(§1.2 の自己言及注記)。

---

# 2. 委嘱① — 最小ラボ

## 2.1 ラボの定義と規模(自前計算)

> ### 定義 LAB(本ノート)
> $$P_{c,p}:=F_2\big/\gamma_{c+1}(F_2)\,F_2^{\,p},\qquad N_{c,p}:=\bigl(\gamma_{c+1}(F_2)F_2^{\,p}\bigr)\times\langle c_{B_3}\rangle\ \trianglelefteq B_3$$
> ($\gamma_{c+1}F_2\cdot F_2^p$ は **verbal**(完全不変)⟹ $\mathrm{Aut}(F_2)$ 不変 ⟹ $B_3$-正規 ✔。$c_{B_3}=(\sigma_1\sigma_2)^3\in N$ ✔。$PB_3=F_2\times\langle c_{B_3}\rangle$ より $PB_3/N\cong P_{c,p}$ ✔、$\widehat G=B_3/N$ は $\twoheadrightarrow S_3$ ✔ ⟹ **窓層 $L2$ の対象**。工房既在の $NW(c,p)$ 族。)

| $c$ | $\mathrm{Witt}(2,c)$ | 幅 $W(c)=\sum_{i\le c}$ | $\lvert P_{c,5}\rvert$ | $\lvert P_{c,7}\rvert$ | Lazard($p=5$) | Lazard($p=7$) |
|---:|---:|---:|---|---|---|---|
| 4 | 3 | **8** | $5^{8}=3.9\times10^5$ | $7^8$ | ✔ 成立 | ✔ |
| **5** | 6 | **14** | $5^{14}=6.1\times10^9$ | $7^{14}$ | ★ **最初の破綻** | ✔ |
| **6** | 9 | **23** | $5^{23}$ | $7^{23}$ | ✗ | ✔(最後の成立) |
| **7** | 18 | **41** | — | $7^{41}$ | ✗ | ★ **最初の破綻** |

$$\boxed{\ \textbf{第一ラボ}:\ (p,c)=(5,4)\to(5,5)\to(5,6)\qquad \textbf{第二ラボ}:\ (p,c)=(7,6)\to(7,7)\ }$$
($7^{41}$ は CAL-B4 で既建立 ✔。)

## 2.2 再現コマンド

```
python -c "
def mu(n):
 r=1;d=2;m=n
 while d*d<=m:
  if m%d==0:
   m//=d
   if m%d==0: return 0
   r=-r
  d+=1
 if m>1: r=-r
 return r
def witt(q,n): return sum(mu(d)*q**(n//d) for d in range(1,n+1) if n%d==0)//n
W=0
for c in range(1,9): W+=witt(2,c); print(c,witt(2,c),W)
"
```
**正本出力**: `1 2 2` / `2 1 3` / `3 2 5` / `4 3 8` / `5 6 14` / `6 9 23` / `7 18 41` / `8 30 71`

## 2.3 ★ 測定の実行可能性(**悉皆は不可・次数別が必須**)

- $\lvert P_{5,5}\rvert=5^{14}=6.1\times10^9$ ⟹ **pc 表示で構成可能・演算は $O(1)$**(GAP の `PQuotient`/`NqEpimorphismNilpotentQuotient` 系)。
- ★ しかし GT-shadow の探索は $f\in P$ の悉皆を要し $5^{14}$ 通り ⟹ **不可能**。
- $$\boxed{\ \Longrightarrow\ \textbf{hexagon を下中心列の次数ごとに解く「次数別解法」が必須。}\ }$$
- ★★ **そしてそれは Lie 側予言との突合そのものである**: 次数 $k$ の未知数は $\gamma_k/\gamma_{k+1}\cong\mathbf F_p^{\mathrm{Witt}(2,k)}$(次元 $\le18$)で、各段の解空間の次元を $\dim\mathcal S_k$ と比べればよい ⟹ **設計が自然に噛み合う**。
- **コスト**: 各段は $\le18$ 次元の $\mathbf F_p$-線型系。群演算は pc ⟹ **秒**。

## 2.4 ★★ 一致すべき量と分岐しうる量(**事前分類**)

| 量 | 群側の定義 | Lie 側の対応 | 判定 |
|---|---|---|---|
| $\dim_{\mathbf F_p}\gamma_k/\gamma_{k+1}$ | 下中心因子 | $\mathrm{Witt}(2,k)$ | ★ **一致すべき**(gr は Lazard 非依存・Witt は組合せ論) |
| 交換子の構造定数 | $\mathrm{gr}(P)$ の括弧 | 自由 Lie 環の括弧 | ★ **一致すべき**($\mathrm{gr}$ は常に Lie 環) |
| **$p$ 冪写像 $x\mapsto x^p$ の $\gamma_p$ への漏れ** | Hall–Petrescu: $(xy)^p=x^py^p c_2^{\binom p2}\cdots c_{p-1}^{\binom p{p-1}}\,\mathbf{c_p}$ ⟹ **最後の $c_p\in\gamma_p$ は係数 1**(= $p$ で割れない) | 括弧だけでは決まらない | ★★ **分岐しうる**(**これが Lazard 破綻の実体**) |
| $P$ の同型型 | 実際の乗法 | $\mathrm{gr}$ だけでは決まらない | ★ 分岐しうる |
| **hexagon の解空間**(次数 $k$) | 群の乗法を使う | 線型化方程式 $\mathcal S_k$ | ★★ **$k<p$ で一致・$k\ge p$ で分岐しうる**(本試験の標的) |

> ### ★ 分岐の機構(一行)
> $$\boxed{\ \textbf{次数 }p\ \textbf{で初めて「}p\ \textbf{冪写像が交換子から独立な情報を }\gamma_p\ \textbf{に落とす」}\ \Longrightarrow\ \textbf{hexagon の次数 }p\ \textbf{の段で Lie 予言とずれうる。}\ }$$

---

# 3. 委嘱② — 観測量の設計と予言凍結

## 3.1 観測量の定義

> ### 定義 DEF-PL(**窓側の「捩れ」に相当する量**)
> $$\boxed{\ \mathrm{def}(c,p)\ :=\ \log_p\bigl\lvert GT^{\rm pent}\bigl(N_{c,p}\bigr)_{m=0}\bigr\rvert\ -\ \sum_{k\le c}\dim\mathcal S_k\ }$$
> ($m=0$ 層に限るのは工房既在の規約 — $\lvert GT^{\rm pent}\rvert_{m=0}=p^{\sum\dim\mathcal S_k}$ が Lie 模型の予言。)
> **段別版**(より鋭い):$\mathrm{def}_k(c,p):=\bigl(\text{次数 }k\ \text{の解空間の }\mathbf F_p\text{-次元}\bigr)-\dim\mathcal S_k$。
> - $\mathrm{def}>0$ ⟹ ★ **窓側の「S 伸び」**(Lie 模型より解が多い)
> - $\mathrm{def}<0$ ⟹ **持ち上げ障害**(graded の解が群へ持ち上がらない)
> - $\mathrm{def}=0$ ⟹ Lie 模型どおり

**補助観測量**:
- **算術像の指数** $[GT(N_{c,p}):\mathrm{Im}\,\mathrm{Ih}]$ — 飽和欠損(LADDER-SAT 型)。
- **isolated 性**(全 shadow が settled か)。
- **$\iota$ 掌性**(reflexible / chiral)。

## 3.2 ★★★ 予言凍結(**IF-FIRST・分岐が出る形**)

$\dim\mathcal S_k$($k=1..8$)$=0,0,1,0,1,0,1,1$ ⟹ 累積 $\sum_{k\le c}$:

| $c$ | 1 | 2 | 3 | 4 | **5** | 6 | **7** | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| $\sum_{k\le c}\dim\mathcal S_k$ | 0 | 0 | 1 | **1** | **2** | **2** | **3** | 4 |

> ### 予言 **P-PL-1**(Lazard 域・**外挿の起点**)
> $$\boxed{\ c<p\ \Longrightarrow\ \mathrm{def}(c,p)=0\ }$$
> **根拠**: Lazard 対応により群と Lie 環が圏同値 ⟹ hexagon の解空間は次数ごとに $\mathcal S_k$ と一致。
> **凍結値**: $p=5,c=4$: $\lvert GT_{m=0}\rvert=5^1=\mathbf 5$。$p=7,c=6$: $7^2=\mathbf{49}$。
> **外れたら**: Lazard 域で破れる ⟹ **模型または実装の誤り**(まず疑う順序を固定)⟹ STOP。

> ### ★★ 予言 **P-PL-2**(**本試験・二枝で凍結**)
> $$\boxed{\ c=p\ \textbf{が、}\mathrm{def}\ne0\ \textbf{になりうる最初の class である。}\ }$$
> **凍結値**(Lie 模型の予言):$p=5,c=5$: $\lvert GT_{m=0}\rvert=5^2=\mathbf{25}$。$p=7,c=7$: $7^3=\mathbf{343}$。
> | 枝 | 観測 | 読み |
> |---|---|---|
> | **枝 L(Lazard 無害)** | $\mathrm{def}(p,p)=0$ | Lazard の破綻は **hexagon の解空間には効かない** ⟹ ★ **W 盾の Lazard 柱は倒れても窓の観測量は守られる** = 予想成立側・盾モデルの強化 |
> | **枝 B(分岐)** | $\mathrm{def}(p,p)\ne0$ | ★★ **Γ 縁の窓側双子が実際に鳴った** ⟹ 「$p\le k$ で保護が切れる」が**窓側で初めて実測される**。$\mathrm{def}>0$ なら**窓側の S 伸び** |
> **どちらでも領土**。★ 枝 B の $\mathrm{def}>0$ は共鳴教義の「S 伸び」の**窓側での初の実物**になるので、出た場合は直ちに **QUAR-TOR 型の検疫**(格子・実装・pc 表示の独立再現)を経てから報告する。

> ### 予言 **P-PL-3**(段別・**最も鋭い**)
> $$\boxed{\ \mathrm{def}_k(c,p)=0\ \ (k<p)\quad\textbf{かつ}\quad \mathrm{def}_p(c,p)\ \textbf{が最初の非零候補}\ }$$
> ⟹ **class $c=p$ のラボで、次数 $k=1,\dots,p$ を 1 段ずつ比べる**。$k<p$ の全段で一致し $k=p$ でだけずれる、が枝 B の理想形。$k<p$ でずれたら実装欠陥 ⟹ STOP。

> ### 予言 **P-PL-4**(補助・LADDER-SAT の変形)
> LADDER-SAT(class 2 の梯子:$\lvert GT\rvert=p-1$・isolated・算術飽和)は **class $2<p$** ⟹ Lazard 域の定理である。
> $$\boxed{\ \textbf{class }\ge p\ \textbf{で「isolated」「算術飽和」が保たれるかは未知 — 保たれない側が枝 B の副次的な形。}\ }$$
> **凍結**: $c<p$ では isolated かつ飽和(外挿)。$c=p$ で isolated が破れる(= 非 settled shadow が出る)なら、**それ自体が窓側の「伸び」の別形**。

## 3.3 (32,5) との呼応(**動機のみ・因果は主張しない**)

D2-SNF-1 は $k=32$ で $p=5$ の捩れを出した。$5<32$ ⟹ **帯内 = post-Lazard 側**。本ラボも $p=5$ の post-Lazard 域である。
$$\boxed{\ \textbf{呼応は「同じ }p\le k\ \textbf{の側にいる」という位置の一致であって、因果ではない。}\ }$$
(追補 A で $(32,5)$ は Cohen–Lenstra 雑音と裁定済。**本設計はそれを根拠に使わない**。)

---

# 4. 委嘱③ — 道 1(2-step 可解スライス)の評価

## 4.1 hexagon は可解スライスへ降りるか

$N$ に derived subgroup を足した $N'=N\cdot F_2''$ は **verbal** ⟹ $B_3$-正規 ✔ ⟹ **metabelian スライスは窓として合法**。問題は**何が残るか**である。

## 4.2 ★★★ 深さ 2 は metabelian で 1 次元に潰れる(**証明**)

> ### 命題 METAB-DIE(candidate・本ノート)
> 自由 metabelian Lie 環 $M=L(x,y)/L''$ の多重次数 $(k-2,2)$ 部分($=$ 深さ 2)は **1 次元**。
> **証明.** $M_n$ の標準基底は左正規化括弧 $[y,x,z_3,\dots,z_n]$($z_3\le\cdots\le z_n$、$z_i\in\{x,y\}$)。多重次数 $(k-2,2)$ は $y$ 個数 2 ⟹ $z$ 列に $y$ がちょうど 1 個、$x$ が $k-3$ 個。$z$ 列は非減少ゆえ**配置は一意** ⟹ 基底元は $[y,x,x^{k-3},y]$ ただ 1 つ。∎
> 一方 自由 Lie の深さ 2 は $\dfrac{k-2}2$ 次元(本体既在)。
> | $k$ | 12 | 32 | 68 | 278 |
> |---|---:|---:|---:|---:|
> | 自由 Lie 深さ 2 | 5 | 15 | 33 | **138** |
> | metabelian | 1 | 1 | 1 | **1** |
> $$\boxed{\ \textbf{道 1 は深さ 2 の情報を }138\to1\ \textbf{に潰す(}k=278\textbf{)。床の測定には使えない。}\ }$$

## 4.3 Ihara 括弧の分解(**「死ぬ」の正確な処理**)

$\{f,g\}=[f,g]+D_f(g)-D_g(f)$($D_f(x)=0$、$D_f(y)=[y,f]$)。$\bar\sigma_a=(\mathrm{ad}\,x)^{a-1}y\in L'$ について:
- **通常括弧 $[\bar\sigma_a,\bar\sigma_b]\in[L',L']=L''$** ⟹ **metabelian で死ぬ** ✗
- **導分項 $D_{\sigma_a}(\sigma_b)=(\mathrm{ad}\,x)^{b-1}[y,\sigma_a]$** ⟹ $[y,L']\subseteq[L,L']$ で $L''$ に入るとは限らない ⟹ **生き残る** ✔
$$\Longrightarrow\ \boxed{\ \textbf{metabelian スライスは }\beta_k\ \textbf{ではなく「導分部分だけ」の別写像を測る。}\ }$$
⟹ 「hexagon が降りるか」の答え: **降りるが、降りた先の対象は $\beta_k$ ではない**。誤って同一視すると偽の結論が出る。

**救済案(評価つき)**: derived length 3(= $L/L'''$)なら $[\bar\sigma_a,\bar\sigma_b]\in L''$ が生き残る ✔。ただし自由 3 段可解 Lie 環の次数別次元は自由 metabelian より遥かに速く増える ⟹ **サイズ見積りが必要**【PL-GAP-2】。

## 4.4 ★★ そもそも道 1 は不要である

`p2_address_strike_design_v1.md` 命題 P2-1 の再照準により、CC-1★ の例外番地は $k^*<2p$ ⟹ **$k^*\le278$**、$\beta_{k^*}$ は最大 $68\times138$。
$$\boxed{\ \textbf{床は直接計算できる。道 1(可解スライス+線形閉包)の動機は消えている。}\ }$$
⟹ **評価: 道 1 は (i) metabelian では原理的に不可(命題 METAB-DIE)(ii) derived length 3 なら可能だがサイズ未評価 (iii) しかし直接計算が可能なので不要。**
★ **RDG-5 資産の転用先の変更を提案**: 線形閉包は「床」ではなく **§2.3 の次数別 hexagon 解法**(pc 群上の $\mathbf F_p$-線型系)に転用するのが正しい — そちらは本ラボの本体である。

---

# 5. 【GAP】・novelty・帰属

| # | 内容 | 重さ |
|---|---|---|
| **【PL-GAP-1】** ★ | 「class $=$ weight」(TRI-LCS)は **Lazard 依存** ⟹ $p\le k$ 側での使用は**外挿**。§1.3 の TWIST-EDGE はこの外挿の上に立つ | ★ 大 |
| **【PL-GAP-2】** | derived length 3 スライスのサイズ未評価(§4.3 の救済案) | 中 |
| **【PL-GAP-3】** ★ | $\lvert GT^{\rm pent}_{m=0}\rvert=p^{\sum\dim\mathcal S_k}$ は工房既在の**模型の言明**であり、群側での次数別解法との一致は $c<p$ でのみ根拠がある(それが本試験の当のもの)⟹ **P-PL-1 は「予言」であって定理ではない** | ★ 大 |
| **【PL-GAP-4】** | $P_{c,p}$ が本当に指数 $p$ か($c\ge p$ では $F_2^p$ で割っても $\exp>p$ になりうる)⟹ **段 W-a のカナリアで確認**(下記) | 中 |
| **【PL-GAP-5】** | 本ノートの全命題は candidate(単系統・Sol 未監査)・判定語なし。**測定していない** | — |

## 5.1 発注仕様 **PL-LAB-1**(段組み・実装係向け)

| 段 | 内容 | 出力 | カナリア / 予言 |
|---|---|---|---|
| **W-a** | $P_{c,p}$ を pc 表示で構成($p=5$: $c=4,5,6$/$p=7$: $c=6,7$) | `pc_pres`, `order`, `exponent`, `lcs_dims` | $\lvert P\rvert=p^{W(c)}$(§2.1 表)・`lcs_dims` $=\mathrm{Witt}(2,k)$。★ **`exponent` を記録**(【PL-GAP-4】) |
| **W-b** | $\widehat G=P\rtimes S_3$ 相当を作り窓資格(SG-EXACT: ab$\in\{C_2,C_6\}$・$(2,3)$-生成・$\twoheadrightarrow S_3$)を確認 | `window_ok(bool)` | 窓でなければラボが成立しない ⟹ STOP |
| **W-c** ★ | **次数別 hexagon 解法**: $k=1,\dots,c$ で $\gamma_k/\gamma_{k+1}$ 上の解空間の次元を測る | `sol_dim_by_degree[]` | **P-PL-3**: $k<p$ で $\dim\mathcal S_k$ と一致 |
| **W-d** | $\mathrm{def}(c,p)$ と $\mathrm{def}_k$ を算出 | `def_total`, `def_by_degree[]` | **P-PL-1**($c<p$ で 0)/ **P-PL-2**($c=p$ の二枝) |
| **W-e** | 補助:isolated 性・$\iota$ 掌性・算術像の指数 | `isolated`, `reflexible`, `arith_index` | **P-PL-4** |
| **W-f** | 対照:$p=5,c=4$(Lazard 域)と $p=7,c=6$(Lazard 域)を必ず同梱 | — | **$c<p$ で 0 が出ることが $c=p$ の値の意味を担保** |

**停止規則**: `S-PL-1` W-a/W-b のカナリア失敗 ⟹ STOP。`S-PL-2` $k<p$ で $\mathrm{def}_k\ne0$ ⟹ 実装欠陥 ⟹ STOP。`S-PL-3` 枝 B($\mathrm{def}(p,p)\ne0$)⟹ **QUAR-TOR 型検疫**(独立再現・pc 表示の別構成・判定語なし)。`S-PL-4` 判定語禁止。
**コスト**: pc 群 $5^{14}$ の構成は秒、各次数の線型系は $\le18$ 次元 ⟹ **全段で分**。$7^{41}$ は CAL-B4 既建立 ⟹ 転用。

## 5.2 novelty grep(`docs/` `provenance/` `sol/`)

`post_lazard` / `BOUND-ID` / `TWIN-EDGE` / `DEF-PL` / `def(c,p)` / `P-PL-` / `METAB-DIE` / `PL-LAB-1` = **0 hit**(本ノート初出)。`Hall–Petrescu` / 「分冪」/ 「divided power」= **0 hit**。`NW(c,p)` / `TRI-LCS` / `Lazard` は既在(借用)。

## 5.3 帰属

- 発案 = **研究者**(「これを自分たちの窓を通して見られないか」)。境界一致の candidate 観察 = 司令塔(裁定 774)— ★ **(b) 構造的で正しい**(§1.2)。
- 本ノートの新規部分 = **命題 BOUND-ID**(両境界の共通根 = 分冪の $p$-整性)/ **§1.2 の橋(TRI-LCS)と自己言及注記** / **命題 TWIN-EDGE** / 定義 LAB と規模表 / **§2.4 の一致/分岐の事前分類(Hall–Petrescu の $c_p$ が実体)** / **定義 DEF-PL($\mathrm{def}(c,p)$)** / **P-PL-1〜4(class $=p$ が分岐点・凍結値 25 と 343)** / **命題 METAB-DIE(道 1 は 1 次元に潰れる)** / §4.3 の Ihara 括弧の分解(導分項だけ生き残る)/ §4.4 の「道 1 は不要」と RDG-5 転用先の変更提案 / 発注仕様 PL-LAB-1。
