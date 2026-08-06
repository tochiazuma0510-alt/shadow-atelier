# TOR-SWEEP 追補 A — k=13 予言凍結・σ₁₃ pin 仕様・格上げ文の最終形(裁定 734③)

**状態札: `IF-FIRST 凍結 / paper derivation / candidate / Sol 未監査 / GAP 実走ゼロ・cert 発行ゼロ / ★ $\mathcal S_{13}$ の実測はしていない(凍結が先)/ 新規 S 形成ゼロ / 判定語の発効は司令塔専権 / 本体 tor_sweep_design_v1.md は不改変(versioned)`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-07 / 委嘱: 司令塔(**裁定 734③**)
- 入力: 本体 `tor_sweep_design_v1.md` / **T0–T3 の k=11 実測**(`H_rank=62`・`rank ν=60`・`dim 𝒮₁₁=2`・fixed-point 飽和)/ `weight_family_spectroscopy_design_v1.md` §2 + `_addendum_a.md` / 既報の S 梯子 $k=3..12$: $1,0,1,0,1,1,1,1,2,2$
- **自前検算の申告**: §1 の全数値は python(整数・分数のみ・GAP 不使用・cert ではない)で導出。**§1.4 に再現コマンドを併記**(裁定 668 拡張の履行)。

---

## 0. 凍結値(先に・**測定前**)

> ### ★★ k=11 実測との突合 — **3/3 厳密一致**
> | 量 | 本追補の公式による値 | **T0–T3 実測** | |
> |---|---:|---:|---|
> | $\mathrm{rank}\,H_{11}$ | **62** | **62** | ✔ |
> | $\mathrm{rank}(\nu_{11}\circ j\vert_{H_{11}})$ | **60** | **60** | ✔ |
> | $\dim\mathcal S_{11}(\mathbf Q)$ | **2** | **2** | ✔ |
> ⟹ §1 の 2 本の公式(表現論式・自由性式)は**実弾で較正済**。k=13 の予言はこの較正の外挿である。

> ### ★★★ **P-T-13(k=13 凍結予言・本追補で確定)**
> $$\boxed{\ \mathrm{rank}\,H_{13}=\mathbf{210},\qquad \dim\mathcal S_{13}(\mathbf Q)=\mathbf 3,\qquad \mathrm{rank}\bigl(\nu_{13}\circ j\vert_{H_{13}}\bigr)=\mathbf{207},\qquad \textbf{捩れ支持}=\varnothing\ }$$
> すなわち $d_{207}(N_{13})=\pm1$(TOR-DET の $\gcd=1$)。

**併せて凍結する周辺値**(T4/T5 の対象):

| $k$ | $\mathrm{Witt}(2,k)$ | $\mathrm{tr}(\tau\mid\Lambda_k)$ | $\mathrm{rank}\,H_k$ | $\dim\mathcal S_k(\mathbf Q)$ | $\mathrm{rank}\,\nu_k\vert_{H_k}$ | 捩れ支持 |
|---:|---:|---:|---:|---:|---:|---|
| 9 | 56 | $-1$ | **19** | **1** | **18** | $\varnothing$ |
| 10 | 99 | $0$ | **33** | **1** | **32** | $\varnothing$ |
| **11** | 186 | $0$ | **62** ✔実測 | **2** ✔実測 | **60** ✔実測 | $\varnothing$(T4 で検定) |
| **12** | 335 | $-1$ | **112** | **2** | **110** | $\varnothing$(T4 で検定) |
| **13** | 630 | $0$ | **210** | **3** | **207** | $\varnothing$(★本命) |
| 14 | 1161 | $0$ | **387** | **3** | **384** | (圏外候補) |

---

# 1. 委嘱① — 導出と凍結

## 1.1 $\mathrm{rank}\,H_k$ の**厳密式**(表現論)

$H_k=\ker(1+\theta)\cap\ker(1+\tau+\tau^2)\subseteq\Lambda_k=\mathrm{Lie}(x,y)_k$。本体 系 TOR-S3′ の概算 $\approx\mathrm{Witt}(2,k)/3$ を厳密化する。

> ### 命題 A-1(candidate・本追補)
> $\Lambda=\mathrm{Lie}(\mathrm{std})$($S_3$ の標準 2 次元表現上の自由 Lie 代数;$\mathrm{Lie}(x,y)\cong\mathrm{Lie}(x,y,z)/(x{+}y{+}z)$)とすると
> $$\boxed{\ \mathrm{rank}\,H_k=\mathrm{mult}_{\rm std}(\Lambda_k)=\tfrac13\Bigl[\mathrm{Witt}(2,k)-\mathrm{tr}(\tau\mid\Lambda_k)\Bigr]\ }$$
> $$\mathrm{tr}(\tau\mid\Lambda_k)=\frac1k\sum_{d\mid k}\mu(d)\,\chi_{\rm std}(\tau^d)^{k/d},\qquad \chi_{\rm std}(\tau^d)=\begin{cases}2&3\mid d\\-1&\text{else}\end{cases}$$
>
> **証明.** (i) 本体 定理 TOR-S3 の分解より、$H$ は std-isotypic 成分の各コピーから 1 次元ずつ寄与 ⟹ $\mathrm{rank}\,H_k=\mathrm{mult}_{\rm std}(\Lambda_k)$。
> (ii) $\mathrm{mult}_{\rm std}=\frac16\sum_{g}\chi_{\rm std}(g)\mathrm{tr}(g\mid\Lambda_k)$。$\chi_{\rm std}(1)=2$、互換 3 個で $\chi_{\rm std}=0$、3-巡回 2 個で $\chi_{\rm std}=-1$ ⟹
> $$\mathrm{mult}_{\rm std}=\tfrac16\bigl[2\dim\Lambda_k+0-2\,\mathrm{tr}(\tau\mid\Lambda_k)\bigr]=\tfrac13\bigl[\mathrm{Witt}(2,k)-\mathrm{tr}(\tau\mid\Lambda_k)\bigr].$$
> ★ **互換の項が消える**のが要点($\chi_{\rm std}(\theta)=0$)⟹ $\mathrm{tr}(\theta)$ を知らずに済む。
> (iii) 自由 Lie 代数の指標に対する Adams 作用素の公式(古典)
> $$\mathrm{tr}\bigl(g\mid\mathrm{Lie}_k(M)\bigr)=\frac1k\sum_{d\mid k}\mu(d)\,\chi_M(g^d)^{k/d}$$
> を $M=\mathrm{std}$、$g=\tau$ に適用。$\tau^d$ は $3\mid d$ で単位元、他は 3-巡回 ⟹ 上の場合分け。∎

**較正**: $k=11$ で $\mathrm{tr}(\tau)= \frac1{11}[(-1)^{11}-(-1)]=0$ ⟹ $\mathrm{rank}\,H_{11}=186/3=62$ = **実測と一致** ✔
$k=13$ で $\mathrm{tr}(\tau)=\frac1{13}[(-1)^{13}-(-1)]=0$ ⟹ $\boxed{\mathrm{rank}\,H_{13}=630/3=\mathbf{210}}$

## 1.2 $\dim\mathcal S_k(\mathbf Q)$ の導出(**自由性仮定を明示**)

> ### 仮定 (H-FREE)(**明示・検定対象**)
> $\mathcal S_\bullet=\bigoplus_k\mathcal S_k$(Ihara 括弧つき)は、**各奇数次数 $2n{+}1\ge3$ にちょうど 1 個ずつの生成元 $\sigma_{2n+1}$ をもつ自由 Lie 代数**である。
> **根拠**: (a) $\mathfrak g^{\mathfrak m}$ の自由性は **Brown Thm 1.1**(逐語 pin 済)。(b) $\mathcal S_\bullet\supseteq\mathfrak g^{\mathfrak m}$ で、両者の一致($\mathfrak{grt}=\mathfrak g^{\mathfrak m}$)は**未解決**だが、**低重みでは一致が既知**。(c) ★ **我々自身の実測 S 梯子 $k=3..12$: $1,0,1,0,1,1,1,1,2,2$ が自由性の予測と完全一致**(下表)。
> ⚠ **これは仮定であり定理ではない。$k=13$ の実測が予言と食い違えばそれ自体が一級の結果**(§1.5 の分岐表)。

> ### 命題 A-2(candidate・本追補)
> (H-FREE) の下で、$g_k:=\dim\mathcal S_k$ は
> $$\prod_{k\ge1}(1-t^k)^{-g_k}\ =\ \frac1{1-A(t)},\qquad A(t)=\sum_{n\ge1}t^{2n+1}=\frac{t^3}{1-t^2}$$
> で決まる(PBW)。すなわち $\dfrac{1}{1-A(t)}=\dfrac{1-t^2}{1-t^2-t^3}$(★ **Zagier 予想 (1.1) の母関数**)。
> $S_n:=n\,[t^n]\log\frac1{1-A(t)}$ とおくと $S_n=\sum_{d\mid n}d\,g_d$、Möbius 反転で $n\,g_n=\sum_{d\mid n}\mu(n/d)S_d$。

**計算結果**(自前検算・§1.4 のコマンドで再現可):

| $k$ | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | **11** | **12** | **13** | 14 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $g_k$(公式) | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | **2** | **2** | **3** | 3 |
| 既報 S 梯子 | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | **2** ✔ | **2** ✔ | — | — |

$$\boxed{\ \dim\mathcal S_{13}(\mathbf Q)=\mathbf 3\ }$$
**内訳**(σ 長で分解・§2 の pin 仕様の土台):
$$\mathcal S_{13}=\underbrace{\langle\sigma_{13}\rangle}_{\sigma\text{ 長 }1}\ \oplus\ \underbrace{\mathcal C_{13}}_{\sigma\text{ 長 }3,\ \dim=2},\qquad \mathcal C_{13}=\bigl\langle\{\sigma_3,\{\sigma_3,\sigma_7\}\},\ \{\sigma_5,\{\sigma_3,\sigma_5\}\}\bigr\rangle$$
(重み 13 の括弧部分は分割 $3{+}3{+}7$(多重次数 $(2,1)$、$\dim1$)と $3{+}5{+}5$(多重次数 $(1,2)$、$\dim1$)のみ ⟹ $\dim\mathcal C_{13}=2$。**σ 長 2 の部分は空**($13$ は 2 つの奇数 $\ge3$ の和で偶数にならない ⟹ 実際 $13=3{+}10$ 等は不可、奇+奇=偶)。)
★ **同型の分解が $k=11$ でも成り立ち、実測 $\dim\mathcal S_{11}=2=1+\dim\mathcal C_{11}$ ⟹ $\dim\mathcal C_{11}=1$** — これは重み族分光 §2.2 で紙から出した「$\sigma_{11}$ の lift 自由度 = 1 次元」の**独立確認**である。

## 1.3 $\mathrm{rank}(\nu_{13}\circ j\vert_{H_{13}})$ と捩れ支持

$$\mathrm{rank}\,\nu_k\vert_{H_k}=\mathrm{rank}\,H_k-\dim\mathcal S_k(\mathbf Q)\ \Longrightarrow\ \boxed{\ r'_{13}=210-3=\mathbf{207}\ }$$
($k=11$: $62-2=60$ = 実測 ✔)

> ### P-T-13(捩れ支持・**本命**)
> $$\boxed{\ \{p\ge5:\ p\mid d_{207}(N_{13})\}=\varnothing\quad(\text{TOR-DET の }\gcd=\pm1)\ }$$
> **根拠(予言の理由・証明ではない)**: (i) $k\le11$ の実測は**測った全素数で有理値どおり**。(ii) 本体 定理 TOR-S3 により $S_3$ ブロックは $p\ge5$ で捩れを産まない ⟹ 捩れが出るとすれば $\nu_k$(= $C_5$ のノルム)由来。(iii) $\nu_k$ の係数は $\rho$($T_i\mapsto T_{i+3}$)の置換由来で**小さい整数**しか持たない ⟹ 大きな単因子が立つ構造的理由が見当たらない。
> ⚠ (iii) は**ヒューリスティック**であり、$\lvert C_5\rvert=5$ ゆえ **$p=5$ が唯一の構造的容疑者**である(ノルム元の Tate コホモロジーは $5$ で消える)。⟹ **P-T-13′(補助予言)**: 万一捩れが出るなら **$p=5$ が最有力**。$p=5$ 以外が出たら $\nu$ の対称性で説明できない = より深い現象。

## 1.4 再現コマンド(裁定 668 拡張の履行・**本追補の全数値の正本**)

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
N=20; A=[1 if (d>=3 and d%2==1) else 0 for d in range(N+1)]
H=[F(0)]*(N+1); H[0]=F(1)
for n in range(1,N+1): H[n]=sum(A[j]*H[n-j] for j in range(1,n+1))
L=[F(0)]*(N+1)
for n in range(1,N+1): L[n]=H[n]-sum(F(k,n)*L[k]*H[n-k] for k in range(1,n))
S=[n*L[n] for n in range(N+1)]
g=[0]*(N+1)
for n in range(1,N+1): g[n]=int(sum(mu(n//d)*S[d] for d in range(1,n+1) if n%d==0)/n)
for k in range(9,15):
 w=witt(2,k); t=trtau(k); rh=(w-t)//3
 print(k,w,t,rh,g[k],rh-g[k])
"
```
**正本出力**: `9 56 -1 19 1 18` / `10 99 0 33 1 32` / `11 186 0 62 2 60` / `12 335 -1 112 2 110` / `13 630 0 210 3 207` / `14 1161 0 387 3 384`

## 1.5 ★ 分岐表(**測定前に固定**・どちらでも情報が出る)

| 観測 | 読み | 次の一手 |
|---|---|---|
| $\mathrm{rank}\,H_{13}=210$ | 命題 A-1 の再確認(表現論は $k$ に一様) | 予定どおり T2 へ |
| $\mathrm{rank}\,H_{13}\ne210$ | $S_3$-作用の実装ずれ、または $\Lambda_{13}$ の格子の取り方 | **STOP**(カナリア扱い) |
| $\dim\mathcal S_{13}=3$ | **(H-FREE) が $k=13$ でも成立** ⟹ 予言的中 | σ₁₃ pin(§2)へ |
| **$\dim\mathcal S_{13}>3$** | ★ **自由性の破れ、または $\mathcal S\supsetneq\mathfrak g^{\mathfrak m}$ の初検出** — **一級の結果** | 直ちに数学者へ差戻し・Sol 監査。**判定語は書かない** |
| **$\dim\mathcal S_{13}<3$** | 模型が解を落としている(実装欠陥の疑い) | **STOP**・$k\le12$ の回帰で切り分け |
| 捩れ支持 $=\varnothing$ | P-T-13 的中 ⟹ §3 の格上げ請求へ | — |
| 捩れ支持 $\ne\varnothing$ | **S 単独異常の第一発見候補** | 本体 §5.3 **QUAR-TOR** を発火(発表しない) |

---

# 2. 委嘱② — σ₁₃ pin 仕様

## 2.1 深さ 1 汎関数による分解(**pin の数学的土台**)

$\Lambda_k=\mathrm{Lie}(x,y)_k$ の**深さ 1**(= $y$ を 1 個だけ含む)成分は **1 次元**で、$\mathrm{ad}(x)^{k-1}(y)$ が張る(多重次数 $(k{-}1,1)$ の自由 Lie 次元 $=\frac1k\binom{k}{1}=1$)。

> ### 定義 λ(深さ 1 汎関数)
> $\lambda_k:\Lambda_k\to\mathbf Z$ := 語 $x^{k-1}y$ の係数(= 深さ 1 成分の $\mathrm{ad}(x)^{k-1}(y)$ 係数)。**$\mathbf Z$-線形**。

> ### 命題 A-3(candidate・本追補。**pin の存在と一意性の核**)
> (H-FREE) の下で、$\mathcal S_k=\langle\sigma_k\rangle\oplus\mathcal C_k$($\mathcal C_k$ = σ 長 $\ge2$ の部分)に対し
> $$\boxed{\ \mathcal C_k=\ker\bigl(\lambda_k\vert_{\mathcal S_k}\bigr),\qquad \lambda_k(\sigma_k)\ne0\ }$$
> **証明.** $\sigma_m\in\mathcal D^1$(深さ $\ge1$)で、σ 長 $\ell$ の括弧単項式は深さ $\ge\ell$(Ihara 括弧は深さについて加法的)⟹ $\mathcal C_k\subseteq\mathcal D^2$ ⟹ $\lambda_k(\mathcal C_k)=0$。一方 Brown **(1.6)** $\bar\sigma_{2n+1}=(-1)^n(\mathrm{ad}\,e_0)^{2n}e_1$ より $\sigma_k$ の深さ 1 成分は非零 ⟹ $\lambda_k(\sigma_k)\ne0$。階数・退化次数より $\dim\ker\lambda_k\vert_{\mathcal S_k}=\dim\mathcal S_k-1=\dim\mathcal C_k$ ⟹ 等号。∎

$$\Longrightarrow\ \boxed{\ \textbf{pin は「}\lambda_k\ \textbf{を規格化して }\mathcal C_k\ \textbf{で割る」だけで完結する。残る自由度はちょうど }\mathcal C_k\ \textbf{。}\ }$$

## 2.2 pin 規約 **P1**(決定的・再現可能)

> ### 規約 P1(実装係が逐語実装する形)
> 1. **核の整基底**: $\mathcal S_k^{\mathbf Z}:=\ker(\nu_k\vert_{H_k})\cap\Lambda_k^{\mathbf Z}$ を**飽和して**取る(本体 §2.2 の **SAT** を厳守。k=11 で採用した fixed-point 飽和をそのまま流用)。
> 2. **$\lambda_k$ の像**: $\lambda_k(\mathcal S_k^{\mathbf Z})=c_k\mathbf Z$($c_k\ge1$)を計算し **cert に記録**。★ $c_k\ne1$ は「格子上の原始元が正規化値を取れない」ことを意味する**整性のデータ** — 値を捨てないこと。
> 3. **符号・スケール**: $\lambda_k(\sigma_k)=\varepsilon\,c_k$ とし、$\varepsilon\in\{\pm1\}$ は**工房の既存 $y$-正規化(補題 C-4)に合わせる**。★ **新しい規約を発明しない** — 既存 pipeline の $\sigma_9$(canonical・$\dim\mathcal S_9=1$)を本経路で再計算し、**係数ベクトルが既存 $\sigma_9$ と完全一致**することで $\varepsilon$ を確定する(**較正 CAL-σ**)。
> 4. **$\mathcal C_k$ での簡約**: $\mathcal C_k^{\mathbf Z}=\ker\lambda_k\vert_{\mathcal S_k^{\mathbf Z}}$ の **Hermite 標準形**(Lyndon 語の固定順序で)を取り、$\sigma_k$ をその HNF で簡約 ⟹ **一意な代表元**。
> 5. **記録**: `sigma_pin = {"k":k, "lambda_image_c":c_k, "sign":ε, "hnf_order":"lyndon_lex", "C_basis":[...], "sigma_vector":[...]}` を cert に出す。**pin を変えたら別 cert**。

> ### ⚠ 明示(**canonical と呼ばない**)
> $\sigma_{11},\sigma_{13}$ は **canonical ではない**(Brown p.3 逐語: 「$\sigma_{11}$ is only well-defined up to addition of rational multiples of $\{\sigma_3,\{\sigma_5,\sigma_3\}\}$」)。P1 は**決定的(deterministic)かつ再現可能**な代表元を選ぶだけであり、**一意性の主張ではない**。報告文で「canonical な $\sigma_{13}$」と書かないこと。

## 2.3 ★ L 空間との整合 — **pin は $D_{16}$ の判定を動かさない**

重み族分光 §2.2 の lift 曖昧さ空間:
$$L=2\{\sigma_3,\mathcal C_{13}\}\ -\ 7\{\sigma_5,\mathcal C_{11}\}$$
$\dim\mathcal C_{11}=1$(実測 $\dim\mathcal S_{11}=2$ から確定 ✔)、$\dim\mathcal C_{13}=2$(P-T-13 の内訳)⟹ 生成元 3 本、**$\dim L\le2$**(重み 16・σ 長 4 の空間が 2 次元)⟹ **段 F0 の実測 $\dim L=2$ と整合** ✔

> ### 命題 A-4(candidate・本追補)
> P1 の 3.–4. の選び方(符号・HNF の語順序)を変えると $\sigma_{11}$ は $\mathcal C_{11}$ の元だけ、$\sigma_{13}$ は $\mathcal C_{13}$ の元だけ動く ⟹ $D_{16}$ は **$L$ の元だけ動く**。
> $$\boxed{\ \textbf{定義 QUOT-L の判定}\ \bigl(D_{16}\bmod p\in\mathrm{span}(L\bmod p)\bigr)\ \textbf{は pin 規約に不変。}\ }$$
> さらに $L\subseteq\mathcal D^4$(命題 F-1(b))⟹ **$D_{16}$ の深さ 1,2,3 成分は pin に完全不変**(定理 F-A/F-B/F-C は pin 非依存)。∎

> ### ⚠ ただし生値は pin 依存(**運用規約**)
> - **深さ $\ge4$ の生の係数・content・付値は pin 依存**。⟹ cert には必ず `sigma_pin` を同梱し、**異なる pin の生値を横断比較しない**。
> - 判定は **`in_span_L(bool)` と `in_span_L_by_depth[]`** で行う(生値は診断)。**追補 A(重み族分光)§A.3.2-4 の「判定に項数を使わない」規約と同型**。
> - $\lambda_k$ の像 $c_k$、および $\mathrm{rank}(L\bmod p)$(**P-F-7**)は毎回記録。

## 2.4 発注仕様 **SIG-PIN-1**(核基底 export → pin → $D_{16}$ 段 B/C/E)

| 段 | 入力 | 処理 | 出力 | カナリア |
|---|---|---|---|---|
| **P-a** | T1–T3 の $H_k^{\mathbf Z}$、$N_k$($k=9,11,13$) | $\mathcal S_k^{\mathbf Z}=\ker(N_k)$ を**飽和**して整基底 export | `S_basis_k.json`(Lyndon 座標の整ベクトル) | $\dim$ が §0 表と一致($k{=}9{:}1$, $11{:}2$, $13{:}3$)。不一致 ⟹ STOP |
| **P-b** ★較正 | `S_basis_9` | $k=9$ は $\dim=1$ ⟹ pin 不要。既存 pipeline の $\sigma_9$ と**係数ベクトル完全一致**を確認し $\varepsilon$ を確定 | `cal_sigma9_match(bool)`, `sign_convention` | **CAL-σ**: 不一致 ⟹ 正規化規約の取り違え ⟹ **STOP**(以降の $\sigma_{11},\sigma_{13}$ は無意味) |
| **P-c** | `S_basis_11`, `S_basis_13` | 規約 P1 の 2.–4. を適用 | `sigma_11.json`, `sigma_13.json`, `sigma_pin` | $\lambda(\sigma_k)=\varepsilon c_k$ / $\mathcal C_k$ の階数が $1,2$ |
| **P-d** | $\sigma_3,\dots,\sigma_{13}$ | **$L$ の 3 生成元**を再構成(重み族分光 §2.2 の訂正後の形)し $\dim L$、深さプロファイル、$\mathrm{rank}(L\bmod p)$ | `L_basis`, `L_depth_profile`, `rank_L_mod_p[]` | $\dim L=2$(段 F0 と一致)・**P-F-7**: 全テスト素数で $\mathrm{rank}=2$ |
| **P-e** | 同上 | $D_{16}=2\{\sigma_3,\sigma_{13}\}-7\{\sigma_5,\sigma_{11}\}+11\{\sigma_7,\sigma_9\}$(段 B/C)→ 深さ分解(段 E) | `D16_depth_profile`, `theta_check` | **F-a** 回文($d\leftrightarrow16{-}d$)・**F-b** 台 $\subseteq[4,12]$・**F-c** $\theta D_{16}=-D_{16}$ |
| **P-f** | 同上 | **QUOT-L 判定**(素数ごと・深さごと) | `in_span_L`, `in_span_L_by_depth[]`, `is_zero` | **P-F-8**: 深さ 4,5,11,12 は通る(正典+$\theta$ ⟹ 較正) |

**停止規則**: `S-SIG-1` CAL-σ 失敗 ⟹ STOP。`S-SIG-2` $\dim\mathcal S_k$ が §0 表と不一致 ⟹ STOP(§1.5 の分岐表へ)。`S-SIG-3` **判定語禁止**(cert は生値と bool のみ)。`S-SIG-4` $\mathcal S_{16}$ など**新規 S を形成しない**(本委嘱は $k\le13$ の A 側資材まで)。

> ### ★ 重み 16 開通の前提条件(一行)
> $$\boxed{\ \textbf{P-a}(k{=}13)\ \textbf{が立てば }\sigma_{13}\ \textbf{が手に入り、重み 16 の }D_{16}\ \textbf{は }\textbf{P-e/P-f}\ \textbf{で組める。F-GAP-3(深さ切り詰め)は不要。}\ }$$

---

# 3. 委嘱③ — 格上げ文の最終形($k\le12$・提出用)

**発火条件**: T4/T5 が $k\in\{9,10,11,12\}$ で捩れ支持 $=\varnothing$(TOR-DET の $\gcd=\pm1$、または候補素数が $\mathrm{rank}_p$ 検証で全て否定)。

> ## 格上げ請求文(**最終形・そのまま提出可**)
>
> ### 主張 TOR-UP(k≤12)
> $$\boxed{\ \textbf{すべての素数 }p\ge5\ \textbf{と }3\le k\le12\ \textbf{について}\quad \dim_{\mathbf F_p}\mathcal S_k@p\ =\ \dim_{\mathbf Q}\mathcal S_k\ }$$
> したがって、**S 側の梯子 $1,0,1,0,1,1,1,1,2,2$($k=3..12$)は測った素数だけでなく全ての素数 $p\ge5$ で成立する**。とくに $\dim\mathcal S_k>\dim\mathcal A_k$ となる最小の $k$(= $k^*$)について
> $$\boxed{\ k^*\ \ge\ 13\quad(\textbf{S の意味で・全素数無条件})\ }$$
>
> ### 根拠(3 段)
> 1. **定理 TOR-1**(本体 §1.3): 跳び $\iff p\mid d_r(M_k)$。
> 2. **定理 TOR-S3**(本体 §2.1): $p\ge5$ では $1{+}\theta$・$1{+}\tau{+}\tau^2$ ブロックは捩れを産まない($\mathbf Z_{(p)}[S_3]$ が最大整環)⟹ 判定は $\nu_k\vert_{H_k}$ 1 本に還元(**系 TOR-2**)。
> 3. **実測**(cert `torsweep_k*`): $k=9,10,11,12$ で $d_{r'}(N_k)=\pm1$ ⟹ 捩れ素数なし。
>
> ### ★ 限定(**必ず併記する 4 点**)
> - **(L1) 格子言明である。** 主張は「定義 LAT で指定した $\mathbf Z$-格子($\Lambda_k^{\mathbf Z}=\mathrm{Lie}_{\mathbf Z}(x,y)_k$、$\mathfrak t_k^{\mathbf Z}$ = DK 表示による $\mathbf Z$-形)上の言明」であり、**算術的対象そのものの言明ではない**。算術像への移送には【**D-GAP-1**】と同一の未証明の一段($\mathrm{gr}_k(H)=M$ の還元)が要る。
> - **(L2) $p=2,3$ は射程外。** 定理 TOR-S3 は $p\ge5$ 限定($\lvert S_3\rvert=6$)。$p=2,3$ の完全版は $M_k$ 全体で回す必要がある。
> - **(L3) S 側のみの言明。** $k^*\ge13$ は $\dim\mathcal S_k$ 側の言明であり、$\mathcal A$ 側($\dim\mathcal A_k$)との比較には別の入力が要る。**「B 型不在」を意味しない。**
> - **(L4) 格 = candidate。** 定理 TOR-1 / TOR-S3 / 系 TOR-2 は本工房起草の candidate(単系統・**Sol 未監査**)。cert は GAP/python 単系統。**「verified」は Lean に予約**(工房規約)。
>
> ### ★ 研究者の批判への回答(1 行)
> $$\boxed{\ \textbf{素数走査ではなく単因子の悉皆なので、「異常が }S\ \textbf{にしかいない」場合も }k\le12\ \textbf{では見逃しが原理的に起こらない。}\ }$$
> (見逃しが残るのは (L1)(L2)(L3) の 3 方向のみ — **どこに残っているかが明示されている**ことが本主張の値打ちである。)

---

# 4. 【GAP】・novelty・帰属

| # | 内容 | 重さ |
|---|---|---|
| **【AA-GAP-1】** ★ | **(H-FREE)**($\mathcal S_\bullet$ が $\sigma$ 上自由)は仮定。$k\le12$ の実測と Brown Thm 1.1 が支持するが、$\mathfrak{grt}=\mathfrak g^{\mathfrak m}$ は未解決 ⟹ $\dim\mathcal S_{13}=3$ は**条件付き予言** | ★ 大 |
| **【AA-GAP-2】** | 命題 A-1 の Adams 作用素公式(自由 Lie 代数の指標)は**古典的事実の引用**。工房内 pin なし。$k=11,12$ の実測一致が間接的支持 | 中 |
| **【AA-GAP-3】** | P-T-13 の捩れゼロは**予言であって証明ではない**。構造的容疑者は $p=5$($\nu_k$ が $C_5$ のノルム) | 中 |
| **【AA-GAP-4】** | 規約 P1 の $\varepsilon$(符号)は既存 pipeline から**読み取る**設計。既存規約の逐語記録が薄い場合は CAL-σ が唯一の担保 | 中 |
| **【AA-GAP-5】** | 本追補の全命題は candidate(単系統・Sol 未監査)。**判定語の発効は司令塔専権** | — |

**novelty grep**(`docs/` `provenance/` `sol/` 全域): `P-T-13` / `H-FREE` / `CAL-σ` / `SIG-PIN-1` / `TOR-UP` / `命題 A-1..A-4`(本追補の番号)/ 「Adams 作用素」「mult_std」= **0 hit**(本追補初出)。S 梯子の値・$\nu_k$・$\mathfrak t$ の定義は既在(借用)。

**帰属**: 委嘱・骨子 = 司令塔(裁定 734③)。k=11 実測(H_rank=62 / rank ν=60 / dim 𝒮₁₁=2・fixed-point 飽和)= 実装係 — ★ **この 3 値が本追補の 2 公式を較正した**。本追補の新規部分 = 命題 A-1(rank $H_k$ の厳密式)/ 命題 A-2($\dim\mathcal S_k$ の母関数導出)/ **P-T-13 の凍結**/ 命題 A-3(λ による pin の存在と一意性)/ **規約 P1** / 命題 A-4(pin 不変性)/ **SIG-PIN-1** / **TOR-UP の最終形と限定 4 点**。
