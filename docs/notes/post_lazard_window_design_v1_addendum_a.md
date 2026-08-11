# Lazard 後の窓 追補 A — 仕様修理(裁定 779・実装係の STOP は正しい)

**状態札: `修理 + 再凍結 / candidate / Sol 未監査 / GAP 実走ゼロ・cert 発行ゼロ / 判定語なし / 本体 post_lazard_window_design_v1.md は不改変(versioned)`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-11 / 委嘱: 司令塔(**裁定 779**・PL-LAB-1 ブロック解除)
- 実測入力: 実装係の θτ-only 段別測定 $(k{=}2,3,4)=(0,1,1)$
- **自前検算**: §1・§2 の全数値は python(整数・分数のみ・GAP 不使用・cert ではない)。再現コマンドは §3.3。

---

## 0. 判定(先に 5 行)

| # | 事項 | 結果 |
|---|---|---|
| **①** ★★ | **実装係の STOP は正しい。私の誤りが 2 件ある** | (1) **系列の取り違え**:$\mathcal S_k$ は $\ker\nu_k$($K(0,5)$ の $C_5$-ノルム)込みの 3 条件で、ラボの窓 $P_{c,p}$ には $\rho,\nu$ が存在しない。(2) ★ **幅表の誤り**:$W(c)=\sum\mathrm{Witt}(2,i)$ は **$c<p$ でのみ正しい**(§2) |
| **②** ★★★ | **修理は第三案【C】を採る** | **【A】(比較系列を $H_k$ へ差替え)を採用**+ **P-PL-0 を新設**(幅そのものを Lazard 検定にする)+ 幅表の訂正。**【B】($K(0,5)$ 系への宇宙変更)は却下**(§4) |
| **③** ★★★ | **$H_k$ は私の既在の閉形式で、実測と 3/3 一致** | TOR-SWEEP 追補 A **命題 A-1**:$H_k=\frac13\bigl[\mathrm{Witt}(2,k)-\mathrm{tr}(\tau\mid\Lambda_k)\bigr]$。$k=2,3,4$ で $0,1,1$ ⟹ **実装係の実測と完全一致** ⟹ 差替え系列は**既に検証済み**(§1) |
| **④** ★★ | **凍結値の差替え** | $p=5$:$c=4\to\mathbf{5^2}$、**$c=5\to5^4$**、$c=6\to5^7$。$p=7$:$c=6\to7^7$、**$c=7\to7^{13}$**(§3) |
| **⑤** ★★★ | **★ より安い Lazard 検定が段 W-a に既にある** | $\dim\gamma_k/\gamma_{k+1}(P_{c,p})$ 対 $\mathrm{Witt}(2,k)$。$k<p$ で一致・**$k=p$ で初めて落ちる**(落ち幅 $\ge2$)。$B(2,5)$ が位数 $5^{34}$・class 12(既知)なのに $W(12)=747$ である事実がその証拠(§2) |

---

# 1. 系列の取り違え(誤り 1)と差替え

## 1.1 何を取り違えたか

`b_type_synthesis_design_v1.md` L237 の定義(逐語):
$$\dim\mathcal S_k=\dim\Bigl(\ker(1+\theta)\cap\ker(1+\tau+\tau^2)\cap\ker\nu_k\Bigr),\qquad \nu_k=\sum_{i=0}^4\rho^i\ \text{on}\ \mathfrak t=\mathrm{gr}(K(0,5))$$
**3 条件**である。ラボの窓 $P_{c,p}=F_2/\gamma_{c+1}F_2^{\,p}$ は $B_3$-gentle 系の窓であり、$K(0,5)$ も $\rho$ も $\nu$ も**存在しない**。
$$\boxed{\ \textbf{$B_3$-gentle の GT-shadow は「hexagon 2 本 + charming」であって pentagon を持たない。ゆえに比較系列は }\mathcal S_k\ \textbf{ではなく }H_k\ \textbf{である。}\ }$$
⟹ **本体 §3 の $\mathcal S_k$ 引用は誤り**(起草者の責任)。$GT^{\rm pent}$ という記号を $B_3$ 窓に当てたのも同じ誤り。

## 1.2 ★ 差替え系列 $H_k$ は既在の閉形式で、実測と一致

> ### 定義・公式(TOR-SWEEP 追補 A 命題 A-1 の再掲)
> $$H_k:=\dim_{\mathbf Q}\Bigl(\ker(1+\theta)\cap\ker(1+\tau+\tau^2)\Bigr)_k\subseteq\mathrm{Lie}(x,y)_k$$
> $$\boxed{\ H_k=\frac13\Bigl[\mathrm{Witt}(2,k)-\mathrm{tr}(\tau\mid\Lambda_k)\Bigr],\qquad \mathrm{tr}(\tau\mid\Lambda_k)=\frac1k\sum_{d\mid k}\mu(d)\,\chi_{\rm std}(\tau^d)^{k/d},\ \ \chi_{\rm std}(\tau^d)=\begin{cases}2&3\mid d\\-1&\text{else}\end{cases}}$$

| $k$ | 1 | **2** | **3** | **4** | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| $\mathrm{Witt}(2,k)$ | 2 | 1 | 2 | 3 | 6 | 9 | 18 | 30 |
| $\mathrm{tr}(\tau\mid\Lambda_k)$ | $-1$ | 1 | $-1$ | 0 | 0 | 0 | 0 | 0 |
| **$H_k$** | 1 | **0** | **1** | **1** | **2** | **3** | **6** | **10** |
| 実装係の実測 | — | **0** ✔ | **1** ✔ | **1** ✔ | — | — | — | — |
| $\mathcal S_k$($\nu$ 込み) | 0 | 0 | 1 | **0** | 1 | 0 | 1 | 1 |
| $H_k-\mathcal S_k$ | 1 | 0 | 0 | **1** | 1 | 3 | 5 | 9 |

$$\boxed{\ \textbf{命題 A-1 の閉形式は実装係の実測 }(0,1,1)\ \textbf{を 3/3 で再現する ⟹ パイプラインも公式も較正合格。}\ }$$

> ### ★ 「$k=4$ 不一致」の正体 = **pentagon の最初の一噛み**(司令塔の読みを支持)
> $H_4=1$、$\mathcal S_4=0$ ⟹ **$\nu_4$ が $H_4$ を完全に潰す最初の次数**。以後 $H_k-\mathcal S_k$ は $1,1,3,5,9$ と開く。
> $$\boxed{\ \textbf{$k=4$ は「hexagon だけでは残る 1 次元が、pentagon で消える」最初の点。}\ }$$
> ⟹ 実装係の測定は**バグではなく、gentle 系と本来系の差の初出を可視化した**。副産物として価値がある(§5 の記録)。
> ★ **$k=1$ の扱い**: $H_1=1$ だが **charming 条件 $f\in[F_2/N_{F_2},F_2/N_{F_2}]=\gamma_2$** により次数 1 は寄与しない ⟹ 和は $k\ge2$ から取る(実装係が $k=2$ から報告しているのと整合 ✔)。

---

# 2. ★★ 幅表の誤り(誤り 2)と、そこから出る**より安い検定**

## 2.1 何が誤りか

本体 §2.1 は $\lvert P_{c,p}\rvert=p^{W(c)}$、$W(c)=\sum_{i\le c}\mathrm{Witt}(2,i)$ とした($p=5$:$c=5\Rightarrow5^{14}$、$c=6\Rightarrow5^{23}$)。
$$\boxed{\ \textbf{これは }c<p\ \textbf{でのみ正しい。}c\ge p\ \textbf{では指数 }p\ \textbf{の法則 }x^p=1\ \textbf{が }\gamma_p\ \textbf{以降を削る。}\ }$$
**決定的な反証(既知事実)**: 2 生成の指数 5 の Burnside 群 $B(2,5)$ は**位数 $5^{34}$・class 12**(Havas–Wall–Wamsley)。一方 $W(12)=747$。
$$5^{34}\ \lll\ 5^{747}\ \Longrightarrow\ \textbf{指数 }p\ \textbf{の法則は }c\ge p\ \textbf{で幅を桁違いに削る。}$$
⟹ 本体 §2.1 の $5^{14}$/$5^{23}$/$7^{41}$ は **$c\ge p$ の行が過大**(実際の群は**より小さい**)⟹ **実行可能性は悪化しない・むしろ改善する**。

## 2.2 ★★★ そこから出る新しい観測量(**段 W-a が既に出す**)

$p$ 冪写像は $\gamma_i/\gamma_{i+1}\to\gamma_{ip}/\gamma_{ip+1}$ を誘導する(Hall–Petrescu / Lazard)。$x^p=1$ を課すと、まず $\gamma_1/\gamma_2$($2$ 次元)からの Frobenius 半線型像が $\gamma_p/\gamma_{p+1}$ で消える。

> ### ★★ 予言 **P-PL-0**(新設・**最も安い Lazard 検定**)
> $$\boxed{\ \dim_{\mathbf F_p}\gamma_k/\gamma_{k+1}\bigl(P_{c,p}\bigr)=\mathrm{Witt}(2,k)\quad(k<p);\qquad \dim\gamma_p/\gamma_{p+1}\ <\ \mathrm{Witt}(2,p)\quad(\textbf{最初の落下})\ }$$
> **落ち幅の下界**: $\gamma_1/\gamma_2$ からの $p$ 冪像が消える分 ⟹ **$\ge2$**。$p=5$:$\mathrm{Witt}(2,5)=6$ ⟹ **$\dim\gamma_5/\gamma_6\le4$**。$p=7$:$\mathrm{Witt}(2,7)=18$ ⟹ $\dim\gamma_7/\gamma_8\le16$。
> **これは段 W-a の `lcs_dims` がそのまま出す** ⟹ **hexagon を解く前に Lazard 境界が測れる**。
> **外れたら**($k<p$ で既に落ちる)⟹ 構成の誤り ⟹ STOP。($k=p$ で落ちない ⟹ 指数 $p$ の法則が効いていない ⟹ 構成が $F_2/\gamma_{c+1}$ になっている疑い ⟹ STOP。)

> ### ★ 位置づけ(**本体 §1 の主張の強化**)
> 本体 命題 BOUND-ID は「Lazard の縁 = 分冪 $\gamma_n=x^n/n!$ の $p$-整性が切れる場所」とした。P-PL-0 は**その切れ目を群の下中心因子の次元として直接見る**。
> $$\boxed{\ \textbf{Lazard 境界は「hexagon の解の個数」を見るまでもなく、群の骨格(LCS 次元)に既に現れる。}\ }$$

## 2.3 ⚠ CAL-B4 の $7^{41}$ の正体(**確認事項**)

本体 §2.1 は「$7^{41}$ = CAL-B4 既建立」と書いたが、$41=W(7)$ は **Lazard 域の幅**であり、$c=7=p$ では上記により**過大**である。
$$\boxed{\ \textbf{【PLA-GAP-1】CAL-B4 の }7^{41}\ \textbf{が「}F_2/\gamma_8F_2^7\textbf{」なのか「}F_2/\gamma_8\textbf{(指数条件なし)」なのかを段 W-a で確認せよ。}\ }$$
後者なら位数は $7^{41}$ で正しいが**指数 7 ではない** ⟹ ラボの対象として不適(Lazard 検定にならない)。

---

# 3. 再凍結(**修理後の予言**)

## 3.1 定義の差替え

> ### 定義 DEF-PL′(**本体 §3.1 の差替え**)
> $$\boxed{\ \mathrm{def}(c,p)\ :=\ \log_p\bigl\lvert GT\bigl(N_{c,p}\bigr)_{m=0}\bigr\rvert\ -\ \sum_{2\le k\le c}H_k\ }$$
> ($GT$ = $B_3$-gentle の GT-shadow = **hexagon 2 本 + charming**。$GT^{\rm pent}$ とは書かない。和は charming により $k\ge2$。)
> **段別版**:$\mathrm{def}_k(c,p):=(\text{次数 }k\ \text{の解空間の }\mathbf F_p\text{-次元})-H_k$。

## 3.2 凍結値(自前計算)

$\sum_{2\le k\le c}H_k$:

| $c$ | 2 | 3 | **4** | **5** | **6** | **7** | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| $\sum_{2\le k\le c}H_k$ | 0 | 1 | **2** | **4** | **7** | **13** | 23 |

> ### 予言 **P-PL-1′**(Lazard 域・外挿の起点)
> $$c<p\ \Longrightarrow\ \mathrm{def}(c,p)=0 .$$
> **凍結値**:$p=5,c=4$:$\lvert GT_{m=0}\rvert=5^{2}=\mathbf{25}$。$p=7,c=6$:$7^{7}=\mathbf{823{,}543}$。
> ★ **$p=7,c=4$ も対照に入れる**($7^2=49$)— Lazard 域で 2 点取れば外挿の信頼度が上がる。

> ### ★★ 予言 **P-PL-2′**(本試験・二枝)
> $$\boxed{\ c=p\ \textbf{が }\mathrm{def}\ne0\ \textbf{になりうる最初の class}\ }$$
> **凍結値**(Lie 模型の予言):$p=5,c=5$:$5^{4}=\mathbf{625}$。$p=7,c=7$:$7^{13}$。
> | 枝 | 観測 | 読み |
> |---|---|---|
> | **枝 L** | $\mathrm{def}(p,p)=0$ | Lazard 破綻は hexagon の解空間に効かない ⟹ W 盾の Lazard 柱が倒れても窓の観測量は守られる = **予想成立側** |
> | **枝 B** | $\mathrm{def}(p,p)\ne0$ | ★ Γ 縁の窓側双子が鳴った。$\mathrm{def}>0$ なら**窓側の S 伸び** ⟹ QUAR-TOR 型検疫を経て報告 |
> ⚠ ★ **重要な整合注意**:P-PL-0 により $c=p$ では $\dim\gamma_p/\gamma_{p+1}<\mathrm{Witt}(2,p)$ ⟹ **未知数の空間そのものが縮む** ⟹ $\mathrm{def}_p<0$ が「自明に」出る可能性がある。
> $$\boxed{\ \textbf{ゆえに }\mathrm{def}_k\ \textbf{は「実測 }\dim\gamma_k/\gamma_{k+1}\ \textbf{で正規化した比」で読むこと(下記 P-PL-3′)。}\ }$$

> ### 予言 **P-PL-3′**(段別・**正規化版**・最も鋭い)
> 各次数 $k$ で、群側の解空間の次元 $s_k^{\rm grp}$ と、**実測の $\gamma_k/\gamma_{k+1}$ に $\theta,\tau$ 条件を課した Lie 側の次元** $h_k^{\rm meas}$ を比べる:
> $$\boxed{\ \mathrm{def}_k^{\rm norm}:=s_k^{\rm grp}-h_k^{\rm meas},\qquad \textbf{予言: }k<p\ \textbf{で }0\ \textbf{(かつ }h_k^{\rm meas}=H_k\textbf{)、}k=p\ \textbf{が最初の非零候補}\ }$$
> - $k<p$:$h_k^{\rm meas}=H_k$(P-PL-0 より $\gamma_k/\gamma_{k+1}$ が Witt どおり)⟹ 従来どおり。
> - $k=p$:$\gamma_p/\gamma_{p+1}$ が縮む分は**両側に同じく効く** ⟹ 差だけが Lazard の効果。
> ★ **これが修理後の本試験の正しい形**である(縮小分を Lazard 効果と誤読しないための正規化)。

## 3.3 再現コマンド(**両梯子・裁定 668 規則**)

```
python -c "
from fractions import Fraction as F
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
def trtau(k): return sum(mu(d)*((2 if d%3==0 else -1)**(k//d)) for d in range(1,k+1) if k%d==0)//k
# H 梯子(hexagon-only = theta,tau のみ)
print('H:',[ (witt(2,k)-trtau(k))//3 for k in range(1,9)])
# S 梯子(nu 込み) = 自由 Lie on sigma_3,sigma_5,... の次数別次元
N=10; A=[1 if (d>=3 and d%2==1) else 0 for d in range(N+1)]
H=[F(0)]*(N+1); H[0]=F(1)
for n in range(1,N+1): H[n]=sum(A[j]*H[n-j] for j in range(1,n+1))
L=[F(0)]*(N+1)
for n in range(1,N+1): L[n]=H[n]-sum(F(k,n)*L[k]*H[n-k] for k in range(1,n))
S=[n*L[n] for n in range(N+1)]
print('S:',[int(sum(mu(n//d)*S[d] for d in range(1,n+1) if n%d==0)/n) for n in range(1,9)])
"
```
**正本出力**: `H: [1, 0, 1, 1, 2, 3, 6, 10]` / `S: [0, 0, 1, 0, 1, 0, 1, 1]`

> ### ★ 委嘱の指定 —「$0,0,1,0,1,0,1,1$」の出所
> $$\boxed{\ \mathcal S_k\ \textbf{梯子は「}\sigma_3,\sigma_5,\sigma_7,\dots\ \textbf{上の自由 Lie 代数の次数別次元」であり、母関数は }\frac1{1-t^3/(1-t^2)}=\frac{1-t^2}{1-t^2-t^3}\ (\textbf{Zagier})\ }$$
> (TOR-SWEEP 追補 A **命題 A-2**。$\nu_k$ 込みの 3 条件の解空間 $=\mathfrak{grt}_k$ と同一視した上での値であり、**$B_3$-gentle の窓には適用できない**。)

---

# 4. 二択の裁定 — **第三案【C】**

| 案 | 判定 | 理由 |
|---|---|---|
| **【A】$H_k$ へ差替え** | ★ **採用** | (i) $B_3$-gentle の GT-shadow は定義上 hexagon+charming ⟹ **$H_k$ が正しい対応物**(【A】は「差替え」ではなく**誤りの訂正**)。(ii) $H_k$ は閉形式が既在(命題 A-1)で**実測 3/3 一致済**。(iii) ★ **Γ/Lazard 縁の検定としての意味は完全に保たれる** — 検定は「群側と Lie 側に**同じ条件**を課したときに一致するか」であり、条件が hexagon だけでも分冪の破れは同じく効く(§4.1) |
| **【B】$K(0,5)$ 系へ宇宙変更** | ★ **却下** | (i) 宇宙変更は事前登録の破棄に当たる。(ii) **Lazard 検定に pentagon は不要**(§4.1)⟹ 目的に対して過剰。(iii) コスト:$K(0,5)=F_3\rtimes F_2$ の class-$c$ 指数-$p$ 商は幅 $\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$ 基準 ⟹ $c=5$ で $\sum_{i\le5}(\mathrm{Witt}(3,i)+\mathrm{Witt}(2,i))=(3{+}2)+(3{+}1)+(8{+}2)+(18{+}3)+(48{+}6)=94$ ⟹ $5^{94}$ 級(指数法則で減るとしても桁違い)。(iv) **TRI-LCS の 5 点版が要る**(class = weight の対応が $K(0,5)$ で成り立つかは未証明)⟹ 新しい【GAP】を 1 つ作る |
| **【C】= 【A】+ P-PL-0 + 幅表訂正** | ★★ **本追補の採択** | 【A】に加え、**幅そのものを Lazard 検定にする**(§2.2)⟹ hexagon を解く前に境界が測れる。かつ本体 §2.1 の誤りが同時に直る |

## 4.1 ★ hexagon-only でも分冪の破れは見えるか(**【A】採用の根拠**)

> ### 命題 PLA-1(candidate・本追補)
> Lazard 対応は**群と Lie 環の圏同値**($c<p$)である。ゆえに $c<p$ では、群側で書かれた任意の方程式系(hexagon でも hexagon+pentagon でも)の解空間は、対応する Lie 側の線型化系の解空間と次数ごとに一致する。
> $c\ge p$ では圏同値が壊れ、**群の乗法が $\mathrm{gr}$ の括弧から決まらない**(Hall–Petrescu の $c_p\in\gamma_p$ が係数 1 で残る)。
> $$\boxed{\ \textbf{破れは「方程式の種類」ではなく「群 }\leftrightarrow\ \textbf{Lie の辞書」に生じる ⟹ hexagon だけでも同じく効く。}\ }$$
> ⟹ pentagon を足す利得は「$\mathcal S$ 側との接続」であって「Lazard 検定の感度」ではない。∎

---

# 5. 差分・記録

| 対象 | 差分 |
|---|---|
| 本体 §2.1 幅表 | ★ **$c\ge p$ の行を訂正**:$p^{W(c)}$ は $c<p$ のみ。$c\ge p$ は**測定値**(段 W-a の `order`)を正本とする |
| 本体 §3.1 定義 DEF-PL | ★ **DEF-PL′ へ差替え**($\mathcal S_k\to H_k$、$GT^{\rm pent}\to GT$) |
| 本体 §3.2 P-PL-1/2/3 | ★ **P-PL-1′/2′/3′ へ差替え**(凍結値 $25/343\to25/625$、$49/343\to7^7/7^{13}$) |
| 本体 §3.2 | ★ **P-PL-0 を新設**(§2.2) |
| 発注仕様 PL-LAB-1 段 W-c | 「$\dim\mathcal S_k$ と比較」→「**$H_k$ と比較**、かつ $h_k^{\rm meas}$ で正規化」 |

> ### ★ 実装係の測定の副産物(記録)
> $(k{=}2,3,4)=(0,1,1)$ は
> 1. **命題 A-1 の閉形式を独立に検証**(3/3)
> 2. **$k=4$ で $H_4=1\ne\mathcal S_4=0$** = **pentagon の最初の一噛みの可視化**(gentle 系と本来系の差の初出)
> の 2 点を同時に与えた。**仕様が曖昧なまま走らせず STOP した判断が、この 2 点を汚さずに残した。**

---

# 6. 【GAP】・帰属

| # | 内容 | 重さ |
|---|---|---|
| **【PLA-GAP-1】** | CAL-B4 の $7^{41}$ が指数 7 込みか否か(§2.3)⟹ 段 W-a で確認 | 中 |
| **【PLA-GAP-2】** ★ | P-PL-0 の落ち幅の**正確な値**は未導出(下界 $\ge2$ のみ)。$B(2,5)$ の LCS 因子次元列は既知文献にあるはず ⟹ 突合すれば較正になる【文献要請候補】 | 中 |
| **【PLA-GAP-3】** ★ | $\mathrm{def}_k^{\rm norm}$ の「両側に同じく効く」(§3.2 の正規化の根拠)は**直観であって証明ではない** — $\gamma_p$ の縮小が群側と Lie 側で同じ次元だけ効くかは未証明 | ★ 大 |
| **【PLA-GAP-4】** | 本体 §1 の TWIN-EDGE は TRI-LCS(Lazard 依存)の上に立つ【PL-GAP-1】— 本修理では変わらず | ★ 大 |
| **【PLA-GAP-5】** | 本追補の全命題は candidate(単系統・Sol 未監査)・判定語なし | — |

**帰属**: STOP の判断と θτ-only 実測 = **実装係**(★ 仕様曖昧で走らせなかったのは正しく、副産物 2 点を残した)。系列取り違えの指摘 = 司令塔(裁定 779)。**誤り 2 件の責任は起草者(数学者)**。本追補の新規部分 = §1.2 の $H_k$ 差替えと実測 3/3 照合 / §1.2 の「$k=4$ = pentagon の最初の一噛み」の同定 / ★ **§2 の幅表の誤りの発見($B(2,5)=5^{34}$ vs $W(12)=747$)** / **P-PL-0(最も安い Lazard 検定)** / **DEF-PL′ と P-PL-1′/2′/3′(正規化版)** / **命題 PLA-1(hexagon-only で十分の根拠)** / 【B】却下の費用会計。
