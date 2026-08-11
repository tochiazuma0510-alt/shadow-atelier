# post-Lazard 窓ラボ 追補 C — $R_p$ 閉形式の**修正**と P-PL-5′ 再凍結(裁定 788)

**日付**: 2026-08-11 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・判定語の発効は司令塔専権)
**入力 cert**: `jac_chk_v1`(7d7d544)— 実装係。**私の追補 B §1.1 の閉形式候補は $p\ge11$ で外れた。**
**先行**: 追補 B(`post_lazard_window_design_v1_addendum_b.md`)・命題 NORM-1(`phase2_scoring_v1.md` §1.1)

---

## 0. 誤りの自己申告(先に置く)

| 項目 | 追補 B の主張 | 実測(cert `jac_chk_v1`) | 判定 |
|---|---|---|---|
| $\dim R_p$ | $p-1$ | $4,6,10,12$($p=5,7,11,13$) | ★ **4/4 的中** |
| $R_p$ の型 | $\mathrm{triv}\oplus\mathrm{sgn}\oplus\frac{p-3}2\mathrm{std}$ | $(1,1,1)$ $(1,1,2)$ $(2,2,3)$ $(2,2,4)$ | ✘ **$p\ge11$ で外れ** |
| P-PL-5 $\mathrm{def}_p=-\frac{p-3}2$ | $\mathrm{def}_{11}=-4,\ \mathrm{def}_{13}=-5$ | NORM-1 経由の期待は $-3,-4$ | ✘ **反証**(2 ずれ) |
| $\theta$ 整合検査(追補 B §1.2) | 「二記述が整合 ⟹ 自己無矛盾」 | 実測は別型でも同じ $\theta$ 制限 | ✘ **識別力ゼロ**(§3) |

**責任は起草者**。以下 ①②③ は裁定 788 の委嘱に 1:1 で対応する。

---

## 1. ① 閉形式の修正 — **$R_p\cong\mathrm{Sym}^p(\mathrm{std})\ominus\mathrm{std}$**

### 1.1 ★★★ 主張

> ### 命題候補 **JAC-SYM**(candidate・本追補・repo 初出)
> $p\ge5$ 素数、$\Lambda_1=\langle x,y\rangle\cong\mathrm{std}$($S_3$ の反射表現)とする。Jacobson の $p$ 冪公式が定める写像
> $$\psi:\ \mathrm{Sym}^p(\Lambda_1)\longrightarrow\Lambda_p,\qquad a^ib^{p-i}\ \longmapsto\ s_i(x,y)\quad(s_0:=x^{[p]},\ s_p:=y^{[p]}\mapsto0)$$
> は **$S_3$-同変**であり、その核は **Frobenius 像 $\mathrm{Fr}(\Lambda_1)=\langle a^p,b^p\rangle\cong\mathrm{std}$ を含む**。ゆえに
> $$\dim R_p\le p-1,\qquad\text{等号}\iff \ker\psi=\mathrm{Fr}(\Lambda_1)\iff s_1,\dots,s_{p-1}\ \text{が一次独立}$$
> **等号のとき**(実測 4/4):
> $$\boxed{\ R_p\ \cong\ \mathrm{Sym}^p(\mathrm{std})\ \ominus\ \mathrm{std}\ }$$

### 1.2 証明(§1.1 の等号以外は完全証明)

**(a) $\psi$ の定義が整合。** $w=ax+by$ に対し Jacobson 公式(追補 B §1.2 の式)は
$$w^{[p]}=a^p x^{[p]}+b^p y^{[p]}+\sum_{i=1}^{p-1}a^ib^{p-i}\,s_i(x,y)$$
で、右辺の係数関数は $a,b$ の**形式変数**としての次数 $p$ 単項式 ⟹ $\mathrm{Sym}^p$ の基底と 1:1。∎

**(b) $\psi$ は $S_3$-同変。** 制限 Lie 代数の $p$ 冪 $w\mapsto w^{[p]}$ は**任意の Lie 自己同型と可換**(制限構造の canonical 性)。$L_p=\Lambda_p\oplus\Lambda_1^{(p)}$(自由制限 Lie 代数の次数 $p$ 成分の標準分解、$\Lambda_1^{(p)}=\langle x^{[p]},y^{[p]}\rangle$ は Frobenius 捻り)は**同変な直和分解**ゆえ、射影 $\pi:L_p\to\Lambda_p$ も同変。$\psi=\pi\circ(\text{偏極})$ ⟹ 同変。∎

**(c) $\ker\psi\supseteq\mathrm{Fr}(\Lambda_1)$ かつ $\mathrm{Fr}(\Lambda_1)\cong\mathrm{std}$。** $\psi(a^p)=\pi(x^{[p]})=0$、同様に $\psi(b^p)=0$。標数 $p$ の**可換**多項式環では $(\ell+m)^p=\ell^p+m^p$ ⟹ $\{\ell^p:\ell\in\Lambda_1\}$ の張る空間は加法的に閉じて**ちょうど 2 次元** $\langle a^p,b^p\rangle$ で、これは $S_3$-安定(同変写像の像)。$\mathrm{std}$ は $\mathbf F_p$ 上定義されるので Frobenius 捻り $\mathrm{std}^{(p)}\cong\mathrm{std}$。∎

**(d) 等号のもとで型が決まる。** $\dim\mathrm{Sym}^p=p+1$、$\dim R_p=p-1$ ⟹ $\dim\ker\psi=2$ ⟹ (c) より $\ker\psi=\mathrm{Fr}(\Lambda_1)\cong\mathrm{std}$。$p\ge5$ ゆえ $\gcd(|S_3|,p)=\gcd(6,p)=1$ ⟹ $\mathbf F_p[S_3]$ は半単純(Maschke)かつ $\mathrm{triv},\mathrm{sgn},\mathrm{std}$ は絶対既約 ⟹ 完全可約 ⟹ $R_p\cong\mathrm{Sym}^p(\mathrm{std})/\mathrm{std}$。∎

**【残る GAP】** 等号($s_i$ の一次独立)は依然として実測入力(4/4)— **【PLB-GAP-1】は残る**。ただし**格は変わった**: 以前は「型そのものが当てはめ」だったが、**いま当てはめているのはスカラー 1 個($\dim R_p=p-1$)だけ**で、$S_3$-型は同変性から**導出**される。

### 1.3 ★ 指標による明示形(検算可能な形)

$\mathrm{std}$ 上の固有値: $1\mapsto(1,1)$、$\theta\mapsto(1,-1)$、$\tau\mapsto(\omega,\omega^2)$。

$$\chi_{\mathrm{Sym}^p}(1)=p+1,\qquad \chi_{\mathrm{Sym}^p}(\theta)=\sum_{j=0}^p(-1)^j=0\ (p\ \text{奇}),\qquad
\chi_{\mathrm{Sym}^p}(\tau)=\begin{cases}0&p\equiv5\ (6)\\ -1&p\equiv1\ (6)\end{cases}$$

$\ominus\mathrm{std}$($\chi=(2,0,-1)$)して

$$\boxed{\ \chi_{R_p}=\bigl(\,p-1,\ \ 0,\ \ \varepsilon_p\,\bigr),\qquad \varepsilon_p:=\begin{cases}1&p\equiv5\ (6)\\ 0&p\equiv1\ (6)\end{cases}\ }$$

$$m_{\rm triv}=m_{\rm sgn}=\frac{(p-1)+2\varepsilon_p}6=\mathrm{round}\!\left(\frac p6\right),\qquad
\boxed{\ m_{\rm std}(R_p)=\frac{(p-1)-\varepsilon_p}3=\Bigl\lfloor\frac{p-1}3\Bigr\rfloor\ }$$

| $p$ | 5 | 7 | 11 | 13 | 17 | 19 | 23 | 29 |
|---|---|---|---|---|---|---|---|---|
| 予言 $(m_{\rm triv},m_{\rm sgn},m_{\rm std})$ | $(1,1,1)$ | $(1,1,2)$ | $(2,2,3)$ | $(2,2,4)$ | $(3,3,5)$ | $(3,3,6)$ | $(4,4,7)$ | $(5,5,9)$ |
| 実測(`jac_chk_v1`) | $(1,1,1)$ ✔ | $(1,1,2)$ ✔ | $(2,2,3)$ ✔ | $(2,2,4)$ ✔ | — | — | — | — |

**★ 4/4 的中(当てはめパラメータなし)。**

**検算コマンド**(裁定 668 拡張):
```bash
python -c "
def cs(p,g):
  if g=='1': return p+1
  if g=='th': return sum((-1)**(p-i) for i in range(p+1))
  t=[0,0,0]
  for i in range(p+1): t[(2*p-i)%3]+=1
  return t[0]-t[2]
for p in [5,7,11,13,17,19,23,29]:
  d,ct,cth=cs(p,'1'),cs(p,'tau'),cs(p,'th')
  S=((d+3*cth+2*ct)//6,(d-3*cth+2*ct)//6,(2*d-2*ct)//6)
  print(p,(S[0],S[1],S[2]-1),'dim',S[0]+S[1]+2*(S[2]-1),'m_std',S[2]-1,'floor((p-1)/3)',(p-1)//3)
"
```

### 1.4 ★★ 機構 — 「$7\to11$ の跳び」は跳びではない(司令塔の $\lfloor p/6\rfloor$ 予想の正体)

$S_3$ は $\mathrm{std}$ 上の**反射群**であり、Chevalley–Shephard–Todd により不変式環は次数 $2,3$ の自由多項式環。ゆえに(古典的・fake degree)

$$m_{\rm triv}(\mathrm{Sym}^p)=\#\{(i,j)\ge0:2i+3j=p\},\quad
m_{\rm sgn}(\mathrm{Sym}^p)=\#\{2i+3j=p-3\},$$
$$m_{\rm std}(\mathrm{Sym}^p)=\#\{2i+3j=p-1\}+\#\{2i+3j=p-2\}$$

$$\#\{2i+3j=n\}=\Bigl\lfloor\frac n6\Bigr\rfloor+[\,n\not\equiv1\ (6)\,]\quad\Longrightarrow\quad m_{\rm triv}(p)=\mathrm{round}(p/6)$$

- $p=5$: $2{\cdot}1+3{\cdot}1$ の 1 通り ⟹ 1  ・ $p=7$: $2{\cdot}2+3$ の 1 通り ⟹ 1
- $p=11$: $2{\cdot}4+3,\ 2+3{\cdot}3$ の **2 通り** ⟹ 2  ・ $p=13$: $2{\cdot}5+3,\ 2{\cdot}2+3{\cdot}3$ の 2 通り ⟹ 2

> $$\boxed{\ 7\to11\ \text{の}\ 1\to2\ \text{は「新現象」ではない} — \textbf{不変式 }e_2^ie_3^j\ \textbf{の表し方が }p=12\ \textbf{を跨いで 1 本増えるだけ}\ }$$
> 素数対 $(5,7),(11,13),(17,19),(23,29)$ が $6k$ を挟むので、**増分は $6$ ごとに 1**。司令塔の「$\lfloor p/6\rfloor$ 型?」は当たり(正確には $\mathrm{round}(p/6)$)。

**★ 帰結(定性)**: $R_p$ の std 成分は $p$ に**線形**($\sim p/3$)に増える。旧候補 $\frac{p-3}2$ も線形だったが**係数が違う**($1/2$ vs $1/3$)⟹ 痩せの主要項の**傾き**が変わる。編纂の PL 節はこの傾きで書き直す(§4)。

---

## 2. ② **P-PL-5′ 再凍結**(IF-FIRST・2 枝に分離)

追補 B の P-PL-5 は **反証済(撤回)**。再凍結は、**測れているもの(窓側)**と**まだ測れていないもの(会計側)**を分離する。

> ### ★★ 予言 **P-PL-5′a**(窓側・NORM-1 に依存しない・本追補で凍結)
> $$\boxed{\ R_p\cong\mathrm{Sym}^p(\mathrm{std})\ominus\mathrm{std}\quad\Longrightarrow\quad m_{\rm std}(R_p)=\Bigl\lfloor\frac{p-1}3\Bigr\rfloor,\quad m_{\rm triv}=m_{\rm sgn}=\mathrm{round}(p/6)\ }$$
> **未測定域の予言**: $p=17\Rightarrow(3,3,5)$、$p=19\Rightarrow(3,3,6)$、$p=23\Rightarrow(4,4,7)$。
> **検定 = JAC-CHK-2**(発注・下記 §2.1)。**外れたら** $s_i$ の一次独立が破れた($\dim R_p<p-1$)ことになり、それ自体が新データ。

> ### ★★ 予言 **P-PL-5′b**(会計側・**NORM-1 の $p\ge11$ への延長に条件付き**)
> $$\boxed{\ \mathrm{def}_p\ =\ -\Bigl\lfloor\frac{p-1}3\Bigr\rfloor\ }\qquad\text{(NORM-1 が }p\ge11\text{ でも成り立つならば)}$$
> | $p$ | 5 | 7 | **11** | **13** | 17 | 19 | 23 |
> |---|---:|---:|---:|---:|---:|---:|---:|
> | $\mathrm{def}_p$ | $-1$ ✔実測 | $-2$ ✔実測 | $\mathbf{-3}$ | $\mathbf{-4}$ | $-5$ | $-6$ | $-7$ |
> **司令塔が裁定 788 で書いた「NORM-1 経由の新期待 $\mathrm{def}_{11}=-3,\ \mathrm{def}_{13}=-4$」と一致**(独立に導出・§1.3 の閉形式から)。

> ### ⚠ 正直会計 — **$p\ge11$ の $\mathrm{def}_p$ は測っていない**
> cert `jac_chk_v1` が測ったのは **$R_p$ の型だけ**(Lie 側・群を作らない)。$\mathrm{def}_p$ は群側の量($\mathrm{def}(c,p)=\log_p|GT^{\rm pent}_{m=0}(NW(c,p))|-\sum_{k\le c}\dim\mathcal S_k$、正本 `post_lazard_window_design_v1.md` §④)であり、**NORM-1 自体が 2/2 の経験則**(証明なし)。
> ⟹ **P-PL-5′b は「閉形式 × NORM-1」の合成予言**。$-3,-4$ が出ても**二つの主張が同時に立った**ことしか言えず、外れても**どちらが折れたかは分離できない**。分離するには群側の実測(§2.2)が要る。

### 2.1 発注 **JAC-CHK-2**(安い・即撃ち可)

> $p=17,19$(可能なら $23$)で $s_1,\dots,s_{p-1}\in\Lambda_p$ を Jacobson 公式から構成し、$\dim$ と $S_3$-型を測る。
> **判定**: $(3,3,5)$ / $(3,3,6)$ / $(4,4,7)$ ⟹ P-PL-5′a 6/6。**$\dim<p-1$ が出たら即停止・報告**(JAC-SYM の等号仮定が破れた)。
> **コスト**: $\dim\Lambda_p=\mathrm{Witt}(2,p)$。$p{=}17$: **7,710** / $p{=}19$: 27,594 / $p{=}23$: 364,722。（初稿で $p{=}17$ を 3,855 と誤記 — 検算コマンドで自己捕獲・訂正済)
> 検算: `python -c "from sympy import mobius,divisors; f=lambda n,q:sum(mobius(d)*q**(n//d) for d in divisors(n))//n; print([(p,f(p,2)) for p in [17,19,23]])"`
> ⟹ $p=17,19$ は秒〜分。$p=23$ は 36 万次元の基底を明示に持つと RAM 8GB で危険 ⟹ **$17,19$ までを本発注、$23$ は保留**。
> **カナリア**: $p=5,7,11,13$ の再現(cert `jac_chk_v1` とバイト一致でなくてよいが型は一致)。

### 2.2 【文献要請】/ 発注案 **NORM-CHK-2**(高い・分離用)

NORM-1 を $p=11$ で独立に検定するには群側 $GT^{\rm pent}_{m=0}(NW(11,11))$ が要る。自由冪零 class 11・2 生成の位数は $p^{\sum_{k\le11}\mathrm{Witt}(2,k)}=11^{412}$ ⟹ **pc 表示 412 生成**。RAM 8GB での可否は **UNKNOWN**(私は実行しない)。

> **【文献要請 PL-LIT-1】**
> **困難**: 制限 Lie 代数の次数 $p$ 成分と、対応する $p$ 群の $\gamma_p/\gamma_{p+1}$ の**ずれ**(Lazard 破綻の初段)を、群を構成せずに Lie 側だけで計算する公式。
> **欲しい結果の型**: 「自由冪零 $p$ 群の LCS 層 $\cong$ 自由**制限** Lie 代数の層 $\ominus$($p$ 冪由来の補正項)」型の明示定理(Lazard 対応が切れる最初の段での補正の記述)。Jennings/Zassenhaus 次元部分群の言葉でもよい。
> **効用**: これがあれば NORM-1 は経験則から**定理**に格上げでき、P-PL-5′b の合成が解ける。

---

## 3. ③ $\theta$ 検査の盲点 — **教訓 1 行と規約案**

> ### ★★★ 教訓(1 行)
> $$\boxed{\ \mathrm{std}\!\downarrow_{\langle\theta\rangle}=\mathrm{triv}\oplus\mathrm{sgn}\ \textbf{ゆえ、}\theta\ \textbf{制限は }\mathrm{std}\leftrightarrow\mathrm{triv}\oplus\mathrm{sgn}\ \textbf{の交換に構造的に盲} — \textbf{私の二候補はまさにその方向だけ違っていた。}\ }$$

**盲の方向は計算できる**: 制限写像 $\mathrm{Res}:R(S_3)\to R(\langle\theta\rangle)$ は $\mathrm{triv}\mapsto\mathrm{triv}$、$\mathrm{sgn}\mapsto\mathrm{sgn}$、$\mathrm{std}\mapsto\mathrm{triv}+\mathrm{sgn}$ ⟹
$$\ker(\mathrm{Res})=\mathbf Z\cdot(\mathrm{std}-\mathrm{triv}-\mathrm{sgn})\quad(\text{階数}1)$$
旧候補 $(1,1,\frac{p-3}2)$ と実測 $(2,2,\frac{p-1}3)$ の差は $p=11$ で $(-1,-1,+1)\cdot$…すなわち $\ker(\mathrm{Res})$ の元の整数倍**そのもの** ⟹ 私の検査の**識別力は厳密にゼロ**だった(「整合した」のは当然で、情報がなかった)。

> ### 規約案 **REP-3CLASS**(規約台帳 pending へ・司令塔裁定を請う)
> $$\boxed{\ \textbf{有限群 }G\ \textbf{の表現型を主張するときは、既約指標の個数だけ独立な指標値を取る。真部分群 }H\ \textbf{への制限で「整合」しても、}\ker(\mathrm{Res}:R(G)\to R(H))\ \textbf{の方向は検査していない。}}$$
> **運用**: ①「$H$ で通った」と書くときは $\ker(\mathrm{Res})$ を明示的に計算して併記する。②$\ker\ne0$ なら**その検査は同定の証拠にならない**(自己無矛盾性の確認にすぎない)と札を貼る。③$S_3$ の場合は $(1,\theta,\tau)$ の 3 値 = 未知数 3 個に方程式 3 本。

> ### ⚠ 二度目の同型 — 「識別力ゼロの検査」
> 直近の **P100-1.1 の自己捕獲**(SURJ の理由づけ誤り = **SURJ 識別力ゼロ窓族**を根拠にしていた・裁定 426)と**同じ失敗型**。⟹ 一般規約に格上げする価値がある:
> $$\boxed{\ \textbf{検査を根拠として引く前に、その検査が区別できない対象の集合(識別力の核)を書け。}\ }$$

---

## 4. 編纂 PL 節への差分(追補 B §2 の**訂正**)

追補 B §2 の骨格 1–6 は**不変**(BOUND-ID・最小ラボ・P-PL-0/1′/2′/3′・完全会計・WILD-NOEXCESS)。**7 のみ差し替え**:

> **7′. 閉形式(修正)**: $R_p\cong\mathrm{Sym}^p(\mathrm{std})\ominus\mathrm{std}$(**JAC-SYM**・同変性から導出・スカラー 1 個のみ実測入力・**4/4**)⟹ $\mathrm{def}_p=-\lfloor\frac{p-1}3\rfloor$(**P-PL-5′b**・NORM-1 条件付き)。
> **7′-a. 読み**: 痩せの正体は **$S_3$ 反射群の不変式論**(Chevalley: 次数 2,3)。すなわち **Lazard 破綻の初段の痩せ幅は、窓の $S_3$ 対称性だけで決まる**(算術的な入力を一切使わない)。
> **7′-b. ★ 一行(編纂用・更新)**:
> $$\boxed{\ \textbf{Lazard の柱は倒れたが、倒れ方は }S_3\ \textbf{の不変式論で完全に書ける — 痩せ幅 }\lfloor(p-1)/3\rfloor\ \textbf{は対称性だけの帰結で、算術は入っていない。}\ }$$

**★ これは編纂にとって良い知らせでもあり悪い知らせでもある**: 痩せが**純粋に表現論的**なら、そこに**算術の情報(非正則性・Ihara の像)は乗っていない** ⟹ post-Lazard 帯は「反例の棲む場所」としては**期待度が下がる**(裁定 791 の狩猟章の順位づけに効く — §5)。

---

## 5. 【GAP】更新・帰属

| # | 内容 | 変化 |
|---|---|---|
| **【PS-GAP-1】** | ★★ **ほぼ閉**:$R_p$ の型は JAC-SYM で**導出**(当てはめは $\dim R_p=p-1$ の 1 スカラーのみ)・4/4 | 小 → **極小** |
| **【PLB-GAP-1】** | $s_1,\dots,s_{p-1}$ の一次独立(= JAC-SYM の等号)は未証明・4/4 の状況証拠 | 中(**格が変化**: 型全体 → スカラー 1 個) |
| **【PLB-GAP-2】** | $R_p$ が $\gamma_p$ の関係加群の全体か(高次からの寄与)は未検分 | 中(不変) |
| **【PLC-GAP-1】** ★新 | **NORM-1 は $p\ge11$ で未検定**(P-PL-5′b は合成予言・分離不能)⟹ 【文献要請 PL-LIT-1】 | ★ 中 |
| **【PL-GAP-1】** | TRI-LCS は Lazard 依存 ⟹ $p\le k$ 側は外挿 | ★ 大(不変) |

**帰属**: 委嘱 = 司令塔(裁定 788)。生値 = 実装係(cert `jac_chk_v1`・7d7d544)。**閉形式候補 P-PL-5 の誤りは起草者の責任**。本追補の新規部分 = **命題候補 JAC-SYM(同変写像 $\psi$・$\ker\supseteq\mathrm{Fr}(\mathrm{std})$・型の導出)** / **指標閉形式 $\chi_{R_p}=(p-1,0,\varepsilon_p)$** / **Chevalley 読み($\mathrm{round}(p/6)$ の正体)** / **P-PL-5′a/b の分離凍結** / **発注 JAC-CHK-2** / **【文献要請 PL-LIT-1】** / **規約案 REP-3CLASS と「識別力の核」規約**。
**novelty grep**: `Sym^p` / `対称冪` / `Chevalley` / `Shephard` / `fake degree` / `Molien` / `Frobenius twist` を `docs/` `provenance/` で検索 — 本設定での使用は**初出**(`余不変式` は ribet_dig 系で別文脈に既出)。
