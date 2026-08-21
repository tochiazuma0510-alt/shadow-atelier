# Golod–Shafarevich / 無限類体塔 / 鳩ノ巣 型の 3 形 — 高速判定 短報

**状態札: 数学者判定・司令塔検分前・Sol 未監査**
判定: Claude 数学者 / 2026-08-18 / 発案 = 研究者本人 / 委嘱 = 司令塔
格: paper candidate。機械計算ゼロ。封印 3 量・$u$ の値・$c$ の値・sealed $K^{(5)}$ に非接触。

## 0. 冒頭申告

### 0.1 T33-L10(witness 鳩ノ巣の死)への抵触自己申告

T33-L10(T-36 §6.9)は「単一の literal pair $(m,f)\in\mathbf Z\times F_2$ が cofinal 族の全段で shadow なら $2m+1=\pm1$」を示し、**witness への鳩ノ巣(発案札 A-5 / A-4 強形)を反証**した。以下の 3 形について:

| 形 | 抵触 | 理由 |
|---|---|---|
| 形 1(埋め込み問題/射影性) | **なし** | 逆極限の元を作るが、各段の witness は段ごとに異なってよい。T33-L10 が禁じたのは「段によらず**同一の literal pair**」であって「compatible thread の存在」ではない(後者は固定入力 4 で既に CLOSED) |
| 形 2(GS 型階数勘定) | **なし** | 次元/完全性の主張であって witness を固定しない |
| 形 3(型への鳩ノ巣) | **なし** | 有限性を主張するのは**型**(chief factor の同型類等)であって witness ではない。型レベル定理は「各段で解が存在する」を型ごとに言うだけで、共通解を主張しない |

⟹ **3 形とも T33-L10 を蘇らせない。** ただし形 1 は「proper solution の逆極限」を使うので、**もし途中で「同一の解を全段で使う」と書いたら即座に L10 に抵触する** — 本書ではその書き方をしていない(§1.3)。

### 0.2 禁止短路

centerless/Schreier だけからの自動 lift・$K(5)$ 単連結性だけからの effectivity・strict deletion-kernel・ambient exponent-3 quotient による非可換段の検出・$A$ 正規性の仮定 — **本書では一つも使わない**。

### 0.3 一行裁定

**形 1: 不成立(register 不一致を 3 点で名指し。in-house が既に同方向で否定済み、本書はより強い障害を 1 つ追加)。形 2: 不成立(GS は形が逆・counting は非斉次系の可解性を出せない・Λ 構造が存在しない)。ただし「本物の安定性」が別の場所に実在することを特定した。形 3: (a) 偽(型は無限種)・(b) 条件付き。ただし型レベル路線は正当で、その現在構想しうる内容が**すべて (CH-p) 一本に縮約する**ことを示した — (CH-p) が閉じれば「$3$ を割らない位数の chief factor は可換・非可換を問わず全部無害」が型レベル定理として一撃で出る。**

---

## 1. 形 1 — 射影性 / 埋め込み問題(Iwasawa 判定法・Shafarevich 型)

### 1.1 正しい register への書き換え(これはできる)

typed lifting は**埋め込み問題として posable である**。$K\le L$ を窓、$T=T_{m,f}:\widehat{PB_4}\twoheadrightarrow PB_4/K$(settled shadow ⟹ 全射・核 $K$)、$\pi:PB_4/L\twoheadrightarrow PB_4/K$ とすると
$$\bigl(\ \widehat{PB_4}\xrightarrow{\ T\ }PB_4/K\ ,\ \ PB_4/L\xrightarrow{\ \pi\ }PB_4/K\ \bigr)$$
は $\widehat{PB_4}$ に対する**有限埋め込み問題**であり、その proper solution $T'$ で **$T'=T_{m',f'}$ の形のもの**が求める $z_L$ に他ならない(T-38 補題 T33-L8 の言い換え)。

### 1.2 障害の名指し(3 点)

**(O1) 適用対象が無い — $\widehat{PB_4}$ は射影的でない。**
$PB_3\cong F_2\times\mathbf Z\supseteq\mathbf Z\times\mathbf Z$ なので $\mathrm{cd}_p(\widehat{PB_3})\ge2$、同様に $\widehat{PB_4}$ も。射影的 $\iff\mathrm{cd}\le1$ ⟹ **$\widehat{PB_3},\widehat{PB_4}$ はいずれも射影的でない。** 従って「射影的対象の上では全ての有限埋め込み問題が可解」という前提が**そもそも braid 側で成立しない**。射影的なのは $\widehat{F_2}$(と その閉部分群)だけだが、hexagon/pentagon の**方程式は $\widehat{B_3}$ と $\widehat{PB_4}$ の中にあり $\widehat{F_2}$ の中にはない**。
*(この指摘は in-house に無い — §5 grep 参照。)*

**(O2) 解の集合が部分群でも主等質空間でもない。**
仮に (O1) を迂回して weak solution が得られても、必要なのは **GT 型の解**($T'=T_{m',f'}$)。T-38 補題 NA-1 の変換公式
$$\rho_1(fw)=\rho_1\cdot{}^{C_1}[B_1,w]\cdot w,\quad \rho_2(fw)=w^{-1}\rho_2\,{}^{C_2}(w^{A_1^{-1}}w^{-1}),\quad \rho_3(fw)=\rho_3\cdot{}^{(a_4a_5)}(PQ^{-1})$$
は**準同型でない**(T-38 系 NA-1':解集合はトーサーですらない)。従って埋め込み問題の可解性(群論的)から GT 制限版の可解性へ渡る**射がない**。これは既在 `sol/luna_reply_152_typed_lifting_literature_v1.md:146-152` と `sol/luna_reply_152_b4_global_proof_v1.md:150-155` の指摘(「射影性は指定された埋め込み問題を解くが、**三つの B4 残差を一つの埋め込み問題と同定せず、marked A.18 coface を保たない**」)と**同一の障害**であり、本書はそれを支持する。NA-1 はその「三つの残差」を明示式にした分だけ、障害の所在をより鋭く指し示す。

**(O3) 塔に沿った伝播には射影性でなく extension property が要り、それは偽。**
Iwasawa 判定法(可算階数の profinite 群が自由 $\iff$ 全有限埋め込み問題が proper に可解)は「$G$ が自由である」を**結論**する定理であって、我々が欲しい「特定の写像 $\widehat{GT}\to\mathrm{ML}(K)$ の全射性」を与える向きではない。塔に沿って解を伝播させるには **extension property** が必要だが、既在 `sol/luna_reply_152_b4_absorption_literature_v1.md:36-41`(Ershov–Fried, *Math. Ann.* 253 (1980), Thm 2.1)が「**universal Frattini cover は射影的だが extension property を持たない**」を記録している。⟹ 射影性から塔の伝播は出ない。

### 1.3 T33-L10 との整合(念のため)

形 1 が仮に通ったとしても、得られるのは「各段で解が存在し、逆極限が非空」であって「全段で同一の $(m,f)$」ではない。前者は固定入力 4 で既に CLOSED、後者は T33-L10 で死んでいる。**両者を混同しないこと。**

### 1.4 裁定と最小の検証手順

> **形 1: 不成立。** (O1) が新しい決定打で、(O2)(O3) は in-house 既在の再確認。
> **最小検証手順(もし誰かが再挑戦するなら)**: (i) $\mathrm{cd}_p(\widehat{PB_4})$ の下界 2 を明示的に書く(($\mathbf Z_p)^2$ の埋め込み 1 行)。(ii) NA-1 の 3 公式から「解集合が部分群/トーサーでない」ことを 1 例で示す。(iii) extension property を主張する文献を要求する場合は Ershov–Fried の反例との整合を先に示させる。

---

## 2. 形 2 — GS 型の階数勘定 / Fox 複体の塔に沿った安定性

### 2.1 GS は形が逆である

Golod–Shafarevich($r<d^2/4\Rightarrow$ 群が無限)は**塔が終わらない**ことを示す否定的装置である。無限類体塔の応用はすべて「終わらない」という結論。山 2 が要求するのは「全段で一様に**解ける**」という肯定的結論であり、GS の出力型と噛み合わない。塔が無限であること自体は我々には既知かつ無害(むしろ前提)。

### 2.2 決定打 1 — 次元勘定は非斉次系の可解性を出せない

補正 $\lambda$ と残差 $\mathcal R$ について、解くべきは
$$\mathcal T(\lambda)\ \text{が}\ \mathcal R\ \text{を}\ (1,1,1)\ \text{へ送る}$$
という**非斉次**問題である。可換層では $\mathbf F_3$ 線形系 $D\gamma=-\beta$(T-38 補題 T34-J12)。線形代数の初等的事実として、**未知数の数が式の数より多くても可解性は従わない**(可解性は $\beta\in\mathrm{im}\,D$ という位置の問題)。GS 型の不等式は次元の比しか制御しないので、原理的に到達できない。

### 2.3 決定打 2 — そもそも $D$ は全射になり得ない

T-38 補題 NA-3 の勘定: 補正空間は $\le5\dim V$、残差空間は $\le11\dim V$($W\hookrightarrow N^5$、残差三つ組が $W\times W\times N$)。しかもこの比は**塔に沿って尺度不変**である:
$\dim V_j=\dim H_1(H_j;\mathbf F_3)$ は Schreier 上界 $\le[\widehat{PB_4}:H_j](d-1)+1$ で指数に比例して増えるが、補正側も残差側も**同じ $\dim V_j$ に比例**する($W\hookrightarrow N^5$ が効いて、arity-3 の指数が幾ら大きくても補正は $5\dim V$ で頭打ち)。
⟹ **「いずれ補正が制約を追い越す」という GS 的な逆転は起きない。** 内容は最初から最後まで syzygy(定性的な完全性)側にある。

### 2.4 決定打 3 — Iwasawa 型の Λ-加群構造が存在しない

Iwasawa 理論の安定性($\mu,\lambda$ 不変量)は $\Gamma\cong\mathbf Z_p$(より一般に $p$-進解析的)を要する。ここで $\Gamma:=\varprojlim_j H_0/H_j$ は $H_0$ の最大 pro-3 商であり、$H_0$ が $\widehat{PB_4}$ の開部分群なので $\Gamma$ は**階数の大きい自由 pro-3 群**、すなわち **$p$-進解析的でない**(解析的 pro-$p$ 群は有限階数)。従って完備群環 $\mathbf F_3[[\Gamma]]$ は Noether でなく、**構造定理も特性イデアルも存在しない。** ⟹ 「$\mu,\lambda$ 型の有限個の不変量で全段を覆う」という形の安定定理は取れない。

### 2.5 それでも本物の安定性は別の場所に実在する(これが収穫)

**観察 GS-S(Fox 複体のランク安定性).** 各段 $j$ で Fox/Shapiro 複体
$$\mathbf F_3[E_j]^{R}\xrightarrow{D_2}\mathbf F_3[E_j]^{S}\xrightarrow{D_1}\mathbf F_3[E_j]$$
は**自由 $\mathbf F_3[E_j]$-加群のランクが $(|R|,|S|,1)$ で段に依らず一定**である($R,S$ は $PB_4$ の固定有限表示の関係子/生成元)。段が変わって動くのは**係数環 $\mathbf F_3[E_j]$ だけ**であり、行列 $D_2$ は $\mathbf Z[PB_4]$ 上の**ただ一つの固定サイズ行列**(Fox Jacobian)の基底変換像である。
⟹ **正しい定式化は「GS 型の階数比」ではなく「固定行列 $D_2$ の、基底変換 $\mathbf Z[PB_4]\to\mathbf F_3[E_j]$ に沿った振る舞い」である。** これは T-34 が既に採っている枠組みの正確な言語化であり、研究者の直観(「Fox 複体の塔に沿った安定性」)は**この形でなら正しい**。

**そして中央での完全性は偽である(syzygy が実在する理由).**
Shapiro により $\mathrm{coker}/\ker$ は $H_*(H_j;\mathbf F_3)$ を計算する。中央での完全性 $\iff H_2(H_j;\mathbf F_3)=0$。しかし $PB_3\cong F_2\times\mathbf Z$ は $H_2\ne0$(Künneth)であり、その開部分群でも消えない。⟹ **$H_2\ne0$ ⟹ 真の syzygy が存在 ⟹ arity-5(B5/K(5))の複体が必要。** T-30/T-31 の設計は正しく、それを迂回する counting は存在しない。

### 2.6 裁定と最小の検証手順

> **形 2: GS としては不成立。** ただし「Fox 複体のランク安定性(観察 GS-S)」という別形の安定性は本物で、**T-34/157dl の設計を正当化する**。
> **最小検証手順**: (i) $PB_4$ の固定有限表示 (A.3) から $|R|,|S|$ を確定し、$D_2$ を $\mathbf Z[PB_4]$ 上の $|R|\times|S|$ 行列として一度だけ書き下す(これは段に依らない一回作業・157dl の資産と重複するか要確認)。(ii) 2 段($j$ と $j+1$)で $\dim_{\mathbf F_3}H_2(H_j;\mathbf F_3)$ を実測し、「段 $j+1$ の新しい syzygy が段 $j$ からの induced で尽きるか」を**測る**(証明でなく測定として)。尽きないことが観測されれば形 2 の残りの希望も消える。

---

## 3. 形 3 — 型への鳩ノ巣

### 3.1 (a) 型は有限種か — **偽**

**補題 GS-T1.** 塔 $\{N_4(q_j)\}$($q_j=\mathrm{lcm}(1,\dots,j)$)に沿って現れる非可換 chief factor の同型類 $S$ は**無限種**である。
*証明.* (i) $PB_4\twoheadrightarrow PB_3\twoheadrightarrow F_2$(2008 (A.4) の $PB_3\cong F_2\times\mathbf Z$)。(ii) CFSG により全ての有限単純群は 2 生成 ⟹ 任意の $S$ について $F_2\twoheadrightarrow S$。(iii) 152_b4_chief_obstruction_v2 §4 の core 化で $B_4$-stable な有限商を作れば、$S$ 型の非可換 chief factor が $M$ の下に現れる。(iv) $\exp(S)\mid q_j$ は $j\ge\exp(S)$ で成立するので、その段までに $S$ 型は塔の中に入る。単純群は無限個。∎
⟹ **「有限本の定理で全段を覆う」は、型の粗さをこのままにする限り実現しない。** 札 N-3 の Suzuki 刈り取りは $3\nmid|S|$ の型(= Suzuki 群のみ)を落とすが、$3\mid|S|$ の型が無限に残る。

### 3.2 (b) 同型の段の間の transfer — 一般には無い

NA-5 の持ち上げが依存するのは **literal residual $\mathcal R(g)\in W\times W\times N$ と共役子**であり、これらは型 $(S,t,Q\to S_t,\text{coupling})$ では決まらない(同じ型で残差だけ違う配置が排除できない)。⟹ 型から型へ答えを移す機構は一般には無い。
唯一の例外は「型だけで**排除**できる」場合で、それが CB-1/CB-2/CB-3 である ⟹ **型レベル定理の路線自体は正当**。

### 3.3 収穫 — 型レベル路線は (CH-p) 一本に縮約する

**命題 GS-T2.** T-36 §2.5 の未証明補題
> **(CH-p)**: 障害写像 $\mathrm{ob}:\mathrm{ML}(H)\to\mathcal O$($J=\mathrm{ob}^{-1}(0)$)が有限群 $\mathcal O$ への **crossed homomorphism** として実現でき、$\mathcal O$ の位数が chief factor $N$ の位数の素因子のみを持つ

が成り立てば、**$3\nmid|N|$ なる chief factor は可換・非可換を問わずすべて無害**である。
*証明.* $3\nmid|N|$ とする。T-38 補題 T33-L9/NA-2 により $W=H_{PB_3}/K_{PB_3}\hookrightarrow N^5$、$H_{PB_2}/K_{PB_2}\hookrightarrow W^4$ なので $|W|$ も $K_{\rm ord}/H_{\rm ord}$ も 3 と互いに素。従って補正領域 $\Lambda$ と残差空間 $W\times W\times N$ はすべて $3'$-群。(CH-p) により $[\mathrm{ML}(H):J]=|\mathrm{im\,ob}|$ は $|\mathcal O|$ を割り、これは $3'$-数。⟹ $3\nmid[\mathrm{ML}(H):J]$ ⟹ **T-38 定理 T33-T2(SYL3)が発火して $I_K=X$。** ∎

⟹ **(CH-p) 一本で次がまとめて片付く**:
- 全ての elementary abelian $p$-層($p\ne3$)— T-36 §2.5 の主張の再確認;
- 全ての非可換 chief factor $S^t$ で $3\nmid|S|$ — すなわち **Suzuki 型(札 N-3 の刈り取り対象)** が定理として落ちる;
- 残るのは **$3\mid|N|$ の型のみ**、すなわち $p=3$ の elementary abelian 層(157dl の lane)と、Suzuki 以外の全単純群($3\mid|S|$)。

> **これが形 3 の実質**: 「型ごとに一回検証」路線は正しい方向だが、**現在構想しうる型レベル定理の総和は (CH-p) 一本に等しい**。型を個別に潰す作業を増やすより、**(CH-p) を証明する**のが同じ労力で最大の被覆を与える。

### 3.4 裁定と最小の検証手順

> **形 3: (a) 偽・(b) 条件付き。路線は正当だが、その内容は (CH-p) に集約される。**
> **最小検証手順**: (CH-p) は **紙の有限作業**である。2008 合成則 (2.52)($m=2m_1m_2+m_1+m_2$、$fN=f_2N\cdot T^{PB_3}_{m_2,f_2}(f_1)$)を NA-1 の 3 公式に代入し、$\mathcal R(g_2\circ g_1)$ が $\mathcal R(g_2)$ と $g_2$-捻り $\mathcal R(g_1)$ の積で書けるかを確かめる。**1〜2 頁**。成れば §3.3 が全部発火する。

---

## 4. 三形から出た実質(まとめ)

| # | 内容 | 格 |
|---|---|---|
| 1 | **(O1)** $\widehat{PB_3},\widehat{PB_4}$ は射影的でない($\mathbf Z^2$ を含み $\mathrm{cd}_p\ge2$)⟹ 形 1 は適用対象の段階で止まる | 新規(in-house 未指摘)・証明 1 行 |
| 2 | **観察 GS-S** Fox 複体は各段で $(|R|,|S|,1)$ の自由加群・$D_2$ は $\mathbf Z[PB_4]$ 上の固定行列の基底変換像 ⟹ 「塔に沿った安定性」の正しい形。T-34/157dl 設計の正当化 | 新規の言語化・自明に近いが有用 |
| 3 | **中央完全性 $\iff H_2(H_j;\mathbf F_3)=0$ は偽**($PB_3=F_2\times\mathbf Z$ で $H_2\ne0$)⟹ syzygy は実在し arity-5 が必須 | 証明つき |
| 4 | **補題 GS-T1** 塔の非可換 chief 型は無限種(CFSG + $F_2$ 商)⟹ 素朴な型有限性は偽 | 証明つき |
| 5 | **命題 GS-T2** (CH-p) ⟹ $3\nmid\lvert N\rvert$ の chief factor は可換・非可換を問わず全部無害(Suzuki 刈り取りを含む)⟹ **型レベル路線は (CH-p) 一本に縮約** | 条件付き定理・(CH-p) 待ち |

**最優先の勧告**: 3 形の screening が共通に指し示すのは **(CH-p)** である。T-36 §2.5 で【GAP: CH-p】として立て、そこに【文献要請】(groupoid/operad 版 Wells 完全列・障害の加法性)を添えたが、**§3.4 のとおり紙 1〜2 頁の直接計算で決着する可能性が高い**。文献待ちにせず、直接計算を先に試すことを提案する。

---

## 5. novelty grep 領収書(2026-08-18 実施)

| 語彙 | 結果 | 扱い |
|---|---|---|
| `Golod` / `Shafarevich` | **repo 全体で該当ゼロ** | 本書が初出。ただし結論は否定的 |
| `embedding problem` / 埋め込み問題 | 既在: `152_b4_absorption_literature_v1`, `152_b4_global_proof_v1:150-155`, `152_typed_lifting_literature_v1:146-152`, `152_m_special_cofinal_v1`, `152_u158_global_audit_v1` | **形 1 は既に in-house で否定済み**。本書は (O1) を追加し (O2)(O3) を支持 |
| `projective profinite` / `Frattini cover` | 既在: `152_b4_absorption_literature_v1:36-41`(Ershov–Fried Thm 2.1: 射影的だが extension property なし) | 引用して (O3) に使用 |
| `free pro-p` / `cd` / cohomological dimension | 該当は $\gcd$ の誤ヒットのみ。**$\mathrm{cd}(\widehat{PB_n})$ への言及は無し** | (O1) は新規 |
| 安定性 / stability(塔に沿った) | 既在は別文脈(`u7_twist_determination_v1` 等) | 観察 GS-S は新規の言語化 |
| Suzuki 刈り取り | 発案札 N-3(同日・candidate) | 命題 GS-T2 に吸収(型ごとでなく (CH-p) 一本で covered) |
| (CH-p) | T-36 §2.5(自書・candidate) | §3.3 で $S^t$ へ射程拡大 |

---

## 6. 申告

- 全結果 paper candidate。機械計算ゼロ。**cross-checked ではなく verified でもない。**
- 使用した外部前件: CFSG(全有限単純群が 2 生成 — GS-T1)、$p$-進解析的 pro-$p$ 群は有限階数(§2.4)、Ershov–Fried(既在引用)。いずれも再証明していない。
- **UNKNOWN**: (CH-p)。$\dim H_2(H_j;\mathbf F_3)$ の実測値。「段 $j+1$ の syzygy が induced で尽きるか」。
- 3 形とも **T33-L10 を蘇らせない**(§0.1 で逐一確認)。禁止短路は一つも使っていない(§0.2)。
- **B4-B は宣言していない。**

---

## Erratum(2026-08-19・本文凍結・追記のみ)

**§3.3 命題 GS-T2 の証明は誤っている。** 「$[\mathrm{ML}(H):J]=|\operatorname{im\,ob}|$ は $|\mathcal O|$ を割り、これは $3'$-数」という段が偽である — crossed homomorphism $\omega$ のファイバーは $J$ の剰余類なので $[G:J]=|\operatorname{im}\omega|$ は正しいが、$\operatorname{im}\omega$ は一般に**部分群でない**ので $|\mathcal O|$ を割らない。反例: $C_3\curvearrowright C_7$ で $[G:J]=3$、$|\mathcal O|=7$。
⟹ **GS-T2 は (CH-p) の成否と無関係に破れている**(独立の第二の理由)。必要なのは (CH-p) ではなく
> **(CH-p′)**: 障害写像が $3'$-群への**真の準同型**(または zero-fibre index が直接 $3'$-数)であること。
詳細と検算は `docs/notes/chp_proof_v1.md` の **Erratum E-2**。出典 = Sol T-42 監査(`ops/express/20260819_sol_fable_t42_audit.md`)。
**§3.3–3.4 の「型レベル路線は (CH-p) 一本に縮約する」という結論も、この訂正により (CH-p′) へ読み替える必要がある。** §1(形 1)・§2(形 2)の裁定は影響を受けない。
