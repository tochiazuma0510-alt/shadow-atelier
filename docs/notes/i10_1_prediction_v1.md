# 凍結予言 — I10-1 三つ巴判別窓(ISO-x̄ / CYC-GEN / NORM)**v1**

**状態札: candidate(裁定前・未 commit・未凍結)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-29
設問: 発案 010 検証第一波(I10-1 / I10-2)。**凍結は司令塔が commit で行う** — 本稿は起草のみ。
前提: `ideas/ideas_010_conjectures.md`(I10-1・I10-2・全 candidate 札)/ `docs/notes/wac_reverse_design_v1.md`(補題 0.1・命題 0.3・**系 0.4**)/ `docs/notes/wac_second_strike_v1.md`(**系 0.4′**・設計則 D1–D5)/ `docs/notes/ree_capsule_v1.md`(補題 R)/ `docs/notes/a13_mathcheck_v1.md`(補題 2.1 パリティ連結)/ `docs/notes/a13_prediction_v1.md`(梯子)/ `docs/notes/structthm_h2_v1.md`(STR-1/STR-2)
番号系: 本稿の committed 欄は **`P-I10-*`**(`P-STR-*`・`P-A13-*` と衝突しない)

> ## 接触の申告
> 本稿の 2 窓は**本セッションで初めて構成**した。judge は一度も向けられていない。$N_{\rm ord}=5$ の D4 型窓の測定値は工房に存在しない。
> ## 封印遵守
> 有限群論と初等整数論のみ。封印量に触れていない。分岐データは $\mathsf w:=b_1^{-1}a_1$ と書く($\bar x=\mathsf w^2$)。

---

## 0. 結論(先出し)— 発案の最小候補は**対象非存在**、修理して 2 窓を構成した

| 項目 | 判定 |
|---|---|
| 発案の最小候補 $\bar x=(3,3,3,1^4)$・$n=13$ | **void(対象非存在)**。$N_{\rm ord}=3$ は **系 0.4′** で禁止(§1.1)。補題 R を引くまでもない |
| 修理 | $r=3$ は $\ell$ 奇を強制、系 0.4′ は $\ell\ge4$ を強制 ⟹ **$\ell=5$ が最小**。$\bar x=(5^r,1^t)$ |
| **最小の判別窓(非アーベル)** | **`W-E-A15-5x3t0`**($n=15$・$\bar x=(5,5,5)$・$t=0$)**実在を構成的に確認** |
| **最安の判別窓(アーベル)** | **`W-E-A10-5x2t0`**($n=10$・$\bar x=(5,5)$)**実在・悉皆確認**・$\Xi=\mathbf{5{,}000}$ |
| **さらに安い先行読み** | **既に凍結済の梯子 `W-E-A12-9t3`($\Xi=8{,}748$)が ISO-x̄ vs CYC-GEN をすでに判別する**(§1.5)— 新規発射ゼロで第一報が出る |
| 発案の「Ξ〜10⁷」 | ℓ=3 窓についてなら正しい($1.5\times10^7$)が窓が void。修理後は $5\times10^3$ / $1.1\times10^6$(§2) |
| 発案の「$r=2$ では奇部差が出にくい」 | **誤り**。$r=2$ でも $5$ vs $25$ で出る。出ないのは**非アーベル性**だけ(§4.3) |
| 発案の I10-2「$X'=A\Rightarrow\mathrm{dl}=3$」 | **無条件では偽**。機械で両側を実現: **Q が輪積 top を動かさなければ $\mathrm{dl}(X)=2$**(§5) |

---

## 1. 存在設計((D4) 点検・裁定 209 の恒久チェック項目を最初に)

### 1.1 【第一関門】系 0.4′ — $\bar x=(3,3,3,1^t)$ は**存在しない**

$c\in N$ 窓では $\bar x=\mathsf w^2$($\mathsf w=b_1^{-1}a_1$)。$G=\langle a_1,b_1\rangle$ は三角群 $\Delta(2,3,m)$($m=\mathrm{ord}(\mathsf w)$)の商で、$\Delta(2,3,m)$ は $m\le5$ で有限($A_4,S_4,A_5$)・$m=6$ で可解。ゆえに $G$ が $A_n$($n\ge6$)なら **$m\ge7$**(系 0.4)。

> ### 命題 1.1($N_{\rm ord}$ の定義に即した確定)
> **定義**(2401 (3.1)・定義ノート §2): $N_{\rm ord}:=\mathrm{lcm}\bigl(\mathrm{ord}(xN),\mathrm{ord}(yN),\mathrm{ord}(cN)\bigr)$。
> $c\in N$ 窓では $\mathrm{ord}(\bar c)=1$、$\bar y$ は $\bar x$ と共役ゆえ
> $$N_{\rm ord}=\mathrm{ord}(\bar x).$$
> $\bar x=(\ell^r,1^t)$ なら $\mathrm{ord}(\bar x)=\ell$(**巡回長の lcm であって $\ell^r$ ではない**)。
> ゆえに $\bar x=(3,3,3,1^t)$ では **$N_{\rm ord}=3$**。
> 一方 $\mathrm{ord}(\bar x)=m/\gcd(2,m)$ と $m\ge7$ から $\mathrm{ord}(\bar x)\ge4$(**系 0.4′**)。
> $$\boxed{\ N_{\rm ord}=3\ \text{の}\ c\in N\ \text{窓は存在しない}\ \Longrightarrow\ \bar x=(3,3,3,1^t)\ \text{型は対象非存在}.\ }$$

**直接確認**: $\mathrm{ord}(\bar x)=3$ なら $\mathsf w$ の位数は $3$ か $6$、どちらも $<7$。$\Delta(2,3,3)=A_4$・$\Delta(2,3,6)$ は可解ゆえ $\langle a_1,b_1\rangle$ は $A_n$($n\ge6$)になれない。∎

**これは裁定 207 の A₁₄ と同型の事故**(紙 30 秒で死ぬ設計)。**裁定 209 のチェック項目に、補題 R より前に「系 0.4′($N_{\rm ord}\ge4$)」を置くべき**である — 補題 R は $(k,j,m)$ の最適化が要るが、系 0.4′ は $\mathrm{ord}(\bar x)$ を見るだけで済む。

### 1.2 修理 — $\bar x=(\ell^r,1^t)$ の一般設計則

> ### 補題 1.2($\bar x=(\ell^r,1^t)$ 型の $\mathsf w$ の形とパリティ)
> $\mathsf w^2=\bar x$ を満たす $\mathsf w$ は、$\ell$-部で
> - $p$ 個の **$2\ell$-巡回**(各々が $\bar x$ の $\ell$-巡回を **2 本ずつ**生む)+ $(r-2p)$ 個の $\ell$-巡回($\ell$ 奇のときのみ可)
>
> 尾部で $m_2$ 個の互換 + $(t-2m_2)$ 個の不動点、という形に限る。したがって
> $$c(\mathsf w)=(r-p)+(t-m_2),\qquad \mathrm{ord}(\mathsf w)=\begin{cases}2\ell&(p\ge1\ \text{または}\ m_2\ge1)\\ \ell&(\text{その他})\end{cases}$$
> $$\mathrm{sign}(\mathsf w)=(-1)^{p+m_2}\ \Longrightarrow\ \boxed{\,k\equiv p+m_2\ (\mathrm{mod}\ 2)\,}$$
> ($k$ = $a_1$ の互換の本数。$\ell$ 奇なら $\ell$-巡回は偶置換、$2\ell$-巡回は奇置換。)

**系 1.3(設計の枠)**
1. **$r$ が奇なら $\ell$ は奇**($\ell$ 偶では $\ell$-巡回は $2\ell$-巡回からしか作れず $r$ は偶数に強制される)。
2. **系 0.4′**: $\ell=\mathrm{ord}(\bar x)\ge4$。1. と併せて $r=3$ なら **$\ell\ge5$**。
3. **$\ell$ 奇のとき $\ell$ は odd ⟹ $\langle\bar x\rangle$ の位数は奇** — ISO-x̄ / CYC-GEN の主張(「奇部 × 2-部」の直積)が**意味をもつための前提**。$\ell$ 偶($\bar x=(4,4)$ 等)では $\langle\bar x\rangle$ が 2-群に沈むので三つ巴は定式化できない。**$\ell$ 奇は本キャンペーンの scope 条件**。
4. 補題 R(両パリティ枝・裁定 209):$c(a')_{\min}+c(b')_{\min}+c(\mathsf w)_{\min}\le n+2$ を $\varepsilon\in\{0,1\}$ で。

### 1.3 最小窓の同定(補題 R の紙上算術)

$\ell=5$、$n=5r+t$。$c(b')_{\min}=n-2\lfloor n/3\rfloor$、$c(a')_{\min}=n-k_{\max}(n,\varepsilon)$。

| 窓 | $n$ | $r$ | $t$ | $(p,m_2)$ | $\varepsilon$ | $c(a')+c(b')+c(\mathsf w)$ | $n+2$ | 種数 |
|---|---|---|---|---|---|---|---|---|
| **`W-E-A10-5x2t0`** | 10 | 2 | 0 | $(1,0)$ | 1 | $7+4+1=12$ | 12 | **0** |
| **`W-E-A15-5x3t0`** | 15 | 3 | 0 | $(1,0)$ | 1 | $10+5+2=17$ | 17 | **0** |
| `W-E-A16-5x3t1`(予備) | 16 | 3 | 1 | $(1,0)$ | 1 | $9+6+3=18$ | 18 | 0 |
| ($\ell=3$ 系すべて) | — | — | — | — | — | — | — | **系 0.4′ で void** |

$(p,m_2)=(0,0)$ の枝は $\mathrm{ord}(\mathsf w)=5<7$ で**双曲性が落ちる**(系 0.4)ので、$t=0$ では $p=1$ が強制される。

### 1.4 実在の確認(構成的・GAP)

- **`W-E-A10-5x2t0`**: $S_{10}$ の**全対合を悉皆**。$\mathsf w=(1\dots10)$ に対し $b_1=a_1\mathsf w^{-1}$ が位数 3 になる $a_1$ は **65 個**、うち $\langle a_1,b_1\rangle\in\{A_{10},S_{10}\}$ は **50 個**(すべて $S_{10}$)。
- **`W-E-A15-5x3t0`**: $\mathsf w=(1\dots10)(11\dots15)$ に対し無作為探索 **1,558 試行で発見**(存在の構成的証明。悉皆ではない)。

### 1.5 【重要】既に凍結済の梯子が最安の第一報になる

CYC-GEN の奇部 $=O_{2'}(\mathrm{Stab})$ は**単一巡回窓でも $t=3$ でだけ** ISO-x̄ とずれる:
$$O_{2'}(C_\ell\times S_t)=C_\ell\times O_{2'}(S_t),\qquad O_{2'}(S_t)=\begin{cases}C_3&t=3\\ 1&t=1,2,4,5,\dots\end{cases}$$

> ### 系 1.4(新規発射ゼロの判別)
> 梯子の $t=3$ 段 **`W-E-A12-9t3`**($\Xi=8{,}748$・`a13_prediction_v1.md` §1.4)で
> $$\text{ISO-}\bar x:\ \lvert\ker\widetilde\chi\rvert=9\cdot2=\mathbf{18}\qquad\text{vs}\qquad\text{CYC-GEN}:\ 27\cdot2=\mathbf{54}.$$
> ($\mathrm{Stab}=C_9\times S_3$(54)、$O_{2'}=C_9\times C_3$(27)、$\mathrm{Syl}_2=C_2$ — すべて実測済 `a13_check2.g`。)
> **すなわち `P-A13-3`($=18$)は、凍結時点では気づかれていなかったが ISO-x̄ vs CYC-GEN の判別欄でもある。**

**帰結**: I10-1 の第一報は**追加費用ゼロ**で出る。本稿の 2 窓は (i) $N_{\rm ord}$ を $9\to5$ に変えた独立確認、(ii) **非アーベル奇部**($r=3$ でしか出ない・I10-2 に必須)、(iii) **$t=0$ で「2-部は尾部の Sylow か Stab の Sylow か」を分離**、の 3 点で追加価値をもつ。

---

## 2. 対象 — 2 窓の同定情報

canonical 文字列 $=$ `<ID>|n=<n>|ell=5|r=<r>|t=<t>|a1=<perm>|b1=<perm>|S1=<perm>|S2=<perm>`(GAP 印字形・UTF-8)。

| 窓 ID | canonical SHA-256 |
|---|---|
| `W-E-A10-5x2t0` | `5848b4bffe7878f048a34379cd4042d1efbed1df6596aa0b5106694f46589df4` |
| `W-E-A15-5x3t0` | `47d73376614720d4cc4b14bdbbc83ef77ba984b71bd2100fcaf9709f59fe26f0` |

### 2.1 `W-E-A10-5x2t0`($n=10$・$\bar x=(5,5)$・$r=2$・$t=0$)

```gap
a1 := ( 1, 2)( 3, 6)( 7,10);;                    # 2^3 1^4   k=3 (奇)
b1 := ( 2,10, 6)( 3, 5, 4)( 7, 9, 8);;           # 3^3 1     j=3
## w := b1^-1*a1 = (1..10)  ord 10 ;  xbar = w^2 = (5,5)  ord 5
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12);;
JUDGE_S2_IMG := ( 1, 6, 4, 5, 3,10, 8, 9, 7, 2)(12,13);;
JUDGE_ID := "W-E-A10-5x2t0";;   ## degree(E) = 13
```

| 項目 | 値(GAP・`i10_check.g`) |
|---|---|
| $\langle a_1,b_1\rangle$ / $E$ | $S_{10}$ / $S_3\times_{C_2}S_{10}$(ファイバー積)、$\lvert E\rvert=10{,}886{,}400=6\lvert A_{10}\rvert$ ✓ |
| braid / $c=(s_1s_2)^3$ | true / **$=1$**(**$c\in N$**)✓ |
| $P$ / $N_{\rm ord}$ | $A_{10}$ ✓ / **5**($\mathrm{ord}\bar x=\mathrm{ord}\bar y=5$、$\mathrm{ord}\bar c=1$) |
| charming $m$ / $c_m$ | $\{0,1,3,4\}$ / $4=\varphi(10)$ ✓、$[P,P]=P$ ✓ |
| $C_P(\bar y)$ | $C_5\times C_5$、**25** |
| $\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)$ | $C_5\times D_{10}\ (\cong C_5\wr S_2)$、**50** |
| $\langle\bar x\rangle$ / $O_{2'}(\mathrm{Stab})$ / $\mathrm{Syl}_2(\mathrm{Stab})$ | $C_5$ (5) / $C_5\times C_5$ (**25**) / $C_2$ (2) |
| $N_{S_{10}}(\langle\bar x\rangle)$ | **200** |
| **$\Xi$ 走査数** | $4\times25\times50=\mathbf{5{,}000}$ |
| 素の経路 $c_m\lvert[P,P]\rvert$ | $4\times1{,}814{,}400=\mathbf{7{,}257{,}600}$ ← **走る(第二の較正ゲート)** |

### 2.2 `W-E-A15-5x3t0`($n=15$・$\bar x=(5,5,5)$・$r=3$・$t=0$)

```gap
a1 := ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11);;                        # 2^5 1^5   k=5 (奇)
b1 := ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11);;         # 3^5       j=5
## w = (1..10)(11..15)  ord 10 ;  xbar = w^2 = (5,5,5)  ord 5
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15)(16,17);;
JUDGE_S2_IMG := ( 1, 9,15,13,11, 5,10, 4, 2, 3)( 6, 8,12, 7,14)(17,18);;
JUDGE_ID := "W-E-A15-5x3t0";;   ## degree(E) = 18
```

| 項目 | 値 |
|---|---|
| $\langle a_1,b_1\rangle$ / $E$ | $S_{15}$ / $S_3\times_{C_2}S_{15}$、$\lvert E\rvert=3{,}923{,}023{,}104{,}000=6\lvert A_{15}\rvert$ ✓ |
| braid / $c$ | true / **$=1$**(**$c\in N$**)✓ |
| $P$ / $N_{\rm ord}$ | $A_{15}$ ✓ / **5** |
| charming $m$ / $c_m$ | $\{0,1,3,4\}$ / **4**、$[P,P]=P$ ✓ |
| $C_P(\bar y)$ | $C_5\times((C_5\times C_5){:}C_3)\ (\cong C_5\wr C_3)$、**375**、**非アーベル** |
| $\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)$ | $C_5\wr S_3$、**750** |
| $\langle\bar x\rangle$ / $O_{2'}(\mathrm{Stab})$ / $\mathrm{Syl}_2(\mathrm{Stab})$ | $C_5$ (5) / $C_5\wr C_3$ (**375**・非アーベル・$\mathrm{dl}=2$) / $C_2$ (2) |
| $N_{S_{15}}(\langle\bar x\rangle)$ | **3000**($\mathrm{dl}=3$) |
| **$\Xi$ 走査数** | $4\times375\times750=\mathbf{1{,}125{,}000}$ |
| 素の経路 | $2.6\times10^{12}$(不能) |

---

## 3. パリティ会計(裁定 209 の恒久項目・補題 1.2 の適用実績)

| 窓 | $k$ | $p$ | $m_2$ | $\mathrm{sign}(a_1)$ | $\mathrm{sign}(\mathsf w)=(-1)^{p+m_2}$ | 一致 | $\varepsilon$ | $\langle a_1,b_1\rangle$ | $E$ |
|---|---|---|---|---|---|---|---|---|---|
| `W-E-A10-5x2t0` | 3 | 1 | 0 | $-1$ | $-1$ | ✓ | 1 | $S_{10}$ | ファイバー積 |
| `W-E-A15-5x3t0` | 5 | 1 | 0 | $-1$ | $-1$ | ✓ | 1 | $S_{15}$ | ファイバー積 |

**両窓とも奇枝($\varepsilon=1$)**。$t=0$ では尾部の互換が使えず($m_2=0$)、双曲性が $p\ge1$ を強制し、$p=1$ が $\mathrm{sign}(\mathsf w)=-1$ を強制する — **$t=0$ の $(\ell^r)$ 型窓は構造的に必ず奇枝**である。$\varepsilon=0$ しか見ない設計では**この族は丸ごと見えない**(裁定 207 の誤りの一般形)。

**Ree 台帳**: 両窓とも等号(種数 0)。§1.3 の表。

---

## 4. 三つ巴の予言表

### 4.1 三つの処方を定義に落とす

$S:=\mathrm{Syl}_2(\ker\widetilde\chi)$、$A:=$ $\ker\widetilde\chi$ の奇部、$\mathrm{Stab}=\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)$。

| 札 | 奇部 $A$ の処方 | 2-部の処方 | 出所 |
|---|---|---|---|
| **ISO-x̄**(最小生存) | $A=\langle\bar x\rangle\cong C_\ell$ | $\mathrm{Syl}_2(\mathrm{Stab})$ | I10-1 |
| **CYC-GEN**(最大生存) | $A=O_{2'}(\mathrm{Stab})=O_{2'}(C_P(\bar y))$ | $\mathrm{Syl}_2(\mathrm{Stab})$ | I10-1 |
| **NORM**(包絡・umbrella) | $\langle\bar x\rangle\le A\le O_{2'}(\mathrm{Stab})$ かつ $\mathrm{GTSh}\hookrightarrow$ $N_{S_n}(\langle\bar x\rangle)$ 型 | 同上 | I10-1 |

**NORM は数値予言ではなく包絡**である(発案自身が「刈り込みの処方を書き下すこと自体が本予想の内容」と書いている)。したがって **ISO-x̄ = 床・CYC-GEN = 天井・NORM = 包絡の主張**という論理構造で凍結する。測定が床と天井の**間**に落ちれば両極端が死に、NORM の中身が新発見になる。

**単一巡回窓での一致**(発案の主張の確認): $\bar x=(\ell,1^t)$ で $\mathrm{Stab}=C_\ell\times S_t$、$O_{2'}=C_\ell\times O_{2'}(S_t)$。$t\ne3$ なら $O_{2'}(S_t)=1$ で三者一致 ✓。**$t=3$ でのみずれる**(系 1.4)。

### 4.2 committed 予言表

| 窓 | $\lvert\ker\rvert$ **ISO-x̄【本命】** | 構造 | $\lvert\ker\rvert$ CYC-GEN | 構造 | $\lvert\mathrm{GTSh}\rvert$ ISO / CYC |
|---|---|---|---|---|---|
| `W-E-A12-9t3`(既凍結) | $\mathbf{18}$ | $C_{18}$ | $54$ | $C_9\times C_3\times C_2$ | $108$ / $324$ |
| `W-E-A10-5x2t0` | $\mathbf{10}$ | $C_{10}$ | $50$ | $C_5^2\times C_2$ | $40$ / $\mathbf{200}=\lvert N_{S_{10}}(\langle\bar x\rangle)\rvert$ |
| `W-E-A15-5x3t0` | $\mathbf{10}$ | $C_{10}$ | $\mathbf{750}$ | $(C_5\wr C_3)\times C_2$ | $40$ / $\mathbf{3000}=\lvert N_{S_{15}}(\langle\bar x\rangle)\rvert$ |

**気づき(NORM の内容の候補)**: $t=0$ の 2 窓では **CYC-GEN $\iff$ $\lvert\mathrm{GTSh}\rvert=\lvert N_{S_n}(\langle\bar x\rangle)\rvert$**、すなわち「GTSh は $\langle\bar x\rangle$ の正規化群**丸ごと**」。ISO-x̄ は「$\mathrm{Syl}_2(\mathrm{Stab})\times\mathrm{Hol}(\langle\bar x\rangle)$ まで刈り込む」。**NORM の「刈り込み」はこの 2 極の間のどこか**という形で定量化できる — これが $t=0$ を選んだ設計上の利得(尾部があると $S_t\to\mathrm{Syl}_2(S_t)$ の刈り込みが混じって 2 極が離れすぎる)。

**さらに位数 750 は 2 群を区別しない**: $(C_5\wr C_3)\times C_2$(直積形)と $C_5\wr S_3=\mathrm{Stab}$ 自身は**ともに位数 750 で非同型**。構造欄まで測ること。

### 4.3 【札の訂正】発案の未監査手計算

| 発案の記述 | 判定 | 正しい値 |
|---|---|---|
| 「最小候補 ℓ=3・t=4・n=13」 | **誤り(対象非存在)** | 系 0.4′ で $N_{\rm ord}\ge4$。$\ell=5$・$r=3$・$t=0$・$n=15$ が最小(§1) |
| 「ISO-x̄ の核 $=C_3\times C_2\times\mathrm{Syl}_2(S_t)$」 | 形は正しいが窓が void | $\ell=5$ 版: $C_5\times C_2=C_{10}$ |
| 「CYC-GEN の奇部 $=C_3\wr C_3$(81・非アーベル)」 | **算術は正しい**(void 窓について) | $\ell=5$ 版: $C_5\wr C_3$(**375**・非アーベル) |
| 「奇部 3 vs 81 で一発判別」 | 判別構造は正しい | $\ell=5$ 版は **5 vs 375** |
| 「Ξ 概算 〜10⁷」 | void 窓についてなら正しい($1.5\times10^7$) | 修理後: **5,000**($r=2$)/ **1,125,000**($r=3$) |
| 「$r=2$ では両予想の奇部差が出にくい」 | **誤り** | $O_{2'}(C_\ell\wr S_2)=C_\ell^2$ で **5 vs 25**。差は出る。出ないのは**非アーベル性**だけ($O_{2'}(S_2)=1$ は**天井の top 側**にしか効かず、**base $C_\ell^r$ が伸びる**のが差の主因) |
| 「$r=2$ は既出($(9,9,1^5)$・$n=23$)」 | 参照は正しいが窓が違う | $n=23$ 版は $t=5$・非可解 Stab・$\Xi\approx1.1\times10^9$、実現 UNKNOWN。本稿の $n=10$ は $t=0$・$\Xi=5{,}000$・**実現確認済** |

---

## 5. I10-2(DL3-ODD)の検分 — **無条件では偽**、条件を機械で分離した

### 5.1 発案の主張と、その穴

> 発案: 「CYC-GEN なら $A=C_3\wr C_3$ で $X'=A$、$X''=A'\cong C_3^2\ne1$、$X'''=1$ ⟹ $\mathrm{dl}(X)=3$」

$X=A\rtimes Q$、$A=B\rtimes T$($B=C_\ell^r$ = base、$T=C_r$ = 輪積 top)、$Q\le\mathrm{Aut}(C_\ell)$ とすると
$$X/B\cong T\times Q\ (\text{$Q$ が $T$ に自明作用のとき})\ \text{は\textbf{アーベル}}\ \Longrightarrow\ X'\subseteq B\ \Longrightarrow\ X''=1\ \Longrightarrow\ \mathrm{dl}(X)\le2 .$$
**$X'=A$ は自動ではない**。必要十分は $[T,Q]\ne1$、すなわち **$Q$ を実現する $\mathrm{Aut}(P)$ の元が輪積の block を動かすこと**。$\chi_{\rm vir}$ が測るのは $\bar x\mapsto\bar x^{2m+1}$ という**対角スカラー作用**だけで、block の置換は $\chi$ からは見えない自由度である。

### 5.2 機械での分離(`i10_dl.g`・$\ell=5$、$r=3$)

$N_{S_{15}}(\langle\bar x\rangle)$($=3000$)の中で $\bar x\mapsto\bar x^2$ を実現する元 $q$ を 2 通り取った:

| 作用 | $q$ | $\lvert X\rvert$ | $\lvert X'\rvert$ | $X'=A$? | **$\mathrm{dl}(X)$** |
|---|---|---|---|---|---|
| **(a) スカラーのみ**(block 保存) | $(2,3,5,4)(7,8,10,9)(12,13,15,14)$ | 1500 | **125** $(=B)$ | false | **2** |
| **(b) block を動かす** | $(1,6)(2,8,5,9)(3,10,4,7)(12,13,15,14)$ | 1500 | **375** $(=A)$ | true | **3**($X''=25$) |

> ### 訂正 5.1(I10-2 の正しい形)
> $$\boxed{\ \text{CYC-GEN}\ \wedge\ [T,Q]\ne1\ \Longrightarrow\ \mathrm{dl}(X)=3\ \Longrightarrow\ \mathrm{dl}(\mathrm{GTSh})=3;\qquad
> \text{CYC-GEN}\ \wedge\ [T,Q]=1\ \Longrightarrow\ \mathrm{dl}(\mathrm{GTSh})=2 .\ }$$
> 発案の caveat (ii)(「inversion が base と top の両方に効く」)が**本質的な前件**であり、本文の導出はそれを落としている。

### 5.3 発案の「正直な注意」の確認 — 正しい

- **核 $\mathrm{dl}$ は 2 のまま**: $\ker=(C_5\wr C_3)\times C_2$ の $\mathrm{dl}$ は **2**(機械確認)。$C_5\wr C_3$ の導来部分群は $C_5^2$(25)、その次で 1。**KERNEL-DL3 は発火しない** ✓ 発案の記述どおり。
- したがって非 metabelian 性は $\mathrm{GTSh}$ 全体の $\mathrm{dl}$ で直接言うしかなく、それには **STR-1 を $A$ 非アーベルへ拡張**する必要がある(STR-1 の (H1) は $A$ アーベルを課す)。**CYC-GEN が勝てば STR-1 の (H1) がその窓で破れる** — 発案の言う「需要側の理由」はこの形で正確に立つ。
- **$\mathrm{dl}$ の天井**: $N_{S_{15}}(\langle\bar x\rangle)$ 自身が $\mathrm{dl}=3$。NORM の包絡が $\mathrm{dl}\le3$ を与える。

---

## 6. committed 欄(`P-I10-0` … `P-I10-10`)

> ### P-I10-0(較正・`W-E-A10-5x2t0` のみ)
> $$\boxed{\ \text{素の経路}(7{,}257{,}600)\ \text{と}\ \Xi\text{-制限経路}(5{,}000)\ \text{が同一の shadow 集合を返す}\ }$$
> `W-E-A10-9t1`(梯子)に続く**第二の較正ゲート**。$N_{\rm ord}$ が違う($5$ vs $9$)ので charming 層の本数も違い($4$ vs $6$)、判定器の $m$-ループを独立に検証できる。

> ### P-I10-1 $\lvert\ker\widetilde\chi(\texttt{W-E-A10-5x2t0})\rvert=\mathbf{10}$、構造 $C_{10}$(**ISO-x̄ に賭ける**)
> ### P-I10-2 $\lvert\ker\widetilde\chi(\texttt{W-E-A15-5x3t0})\rvert=\mathbf{10}$、構造 $C_{10}$

> ### P-I10-3(判別スカラー — 奇部)
> $$\boxed{\ \ker\widetilde\chi\ \text{の奇部}=\langle\bar x\rangle\cong C_5\ (\text{位数}\ \mathbf 5)\ \text{— 両窓}\ }$$
> CYC-GEN なら $25$($r=2$)/ $375$($r=3$)。**中間値(例 $r=3$ で $25$ や $75$)なら両札とも死に、NORM の刈り込みが非自明**。

> ### P-I10-4(判別 — 奇部の可換性)
> $$\boxed{\ \ker\widetilde\chi\ \text{はアーベル}(\cong C_{10})\ \text{— とくに}\ \texttt{W-E-A15-5x3t0}\ \text{でも非アーベル核は出ない}\ }$$
> CYC-GEN なら $r=3$ 窓の核は**非アーベル**($C_5\wr C_3\times C_2$)。**非可換核の第一標本**になるので、外れ方として一級。

> ### P-I10-5(2-部の帰属 — $\mathrm{Syl}_2(\mathrm{Stab})$ か $\mathrm{Syl}_2(S_{\rm tail})$ か)
> $$\boxed{\ 2\text{-部}=\mathrm{Syl}_2(\mathrm{Stab})=C_2\ (\text{位数}\ \mathbf 2)\ \text{— 両窓}\ }$$
> **$t=0$ なので「尾部 $S_t$ の $\mathrm{Syl}_2$」読みなら $1$**。$C_2$ が出れば **2-部の出所は尾部ではなく $\mathrm{Stab}$ 全体**(ここでは輪積 top $S_r$)であることが確定し、`wac_tail8_v1.md` の「尾部律」は**「Stab 律」に一般化される**。$1$ が出れば尾部律が字義どおりで、$(\ell^r)$ 型では 2-部が消える。**どちらでも尾部律の帰属が確定する**。

> ### P-I10-6($\mathrm{GTSh}$ の形・STR-1/STR-2 の $N_{\rm ord}=5$ 版)
> $$\boxed{\ \mathrm{GTSh}(N,N)\cong C_2\times\mathrm{Hol}(\mathbf Z/5),\qquad\lvert\mathrm{GTSh}\rvert=2\cdot20=\mathbf{40}\ \text{— 両窓}\ }$$
> STR-1 の (H2) は $\gcd(\lvert A\rvert,\lvert Q\rvert)=\gcd(5,4)=1$ で**成立**(梯子の $N_{\rm ord}=9$ と違い、ここは前件が素直に通る)。ゆえに **$N_{\rm ord}=5$ での STR-2 の清潔な再試験**になる。
> CYC-GEN なら $200$($r=2$)/ $3000$($r=3$)$=\lvert N_{S_n}(\langle\bar x\rangle)\rvert$。

> ### P-I10-7($\widetilde\chi$ の全射性)
> $$\boxed{\ \lvert Q\rvert=\varphi(5)=\mathbf 4,\ Q\cong C_4\ \text{が}\ \langle\bar x\rangle\ \text{に忠実}\ }$$

> ### P-I10-8(**I10-2 の判定** — $\mathrm{dl}$)
> $$\boxed{\ \mathrm{dl}(\mathrm{GTSh})=\mathbf 2\ \text{— 両窓。DL3-ODD は発火しない}\ }$$
> **賭けの理由**: P-I10-3(ISO-x̄)に賭けている以上 $A=C_5$ アーベルで $\mathrm{dl}(X)\le2$。
> **発火条件(訂正 5.1)**: CYC-GEN **かつ** $[T,Q]\ne1$。この 2 条件が両方立ったときのみ $\mathrm{dl}=3$。

> ### P-I10-9(条件付き・**CYC-GEN が勝った場合にだけ判定**)
> $$\boxed{\ [T,Q]\ne1\ \text{か}\ (\text{$Q$ の実現元が輪積 block を動かすか})\ \text{を測る}\ }$$
> 測り方: $X'=\ker\widetilde\chi$ の奇部 $A$ に一致するか($\mathrm{dl}=3$)、$B=C_5^3$ 止まりか($\mathrm{dl}=2$)。**CYC-GEN が負ければ本欄は判定不要(空振りではなく前提消滅)**。

> ### P-I10-10(NORM の包絡)
> $$\boxed{\ \langle\bar x\rangle\le A\le O_{2'}(\mathrm{Stab})\quad\text{かつ}\quad \mathrm{GTSh}\ \text{は}\ N_{S_n}(\langle\bar x\rangle)\ \text{の部分群と同型な形をもつ}\ }$$
> すなわち $\lvert\mathrm{GTSh}\rvert\mid\lvert N_{S_n}(\langle\bar x\rangle)\rvert$($200$ / $3000$)、かつ $Q\le\mathrm{Aut}(C_5)=C_4$。
> **NORM は床でも天井でもなく包絡なので、P-I10-3 が中間値を出しても NORM だけは生き残りうる。逆に包絡を外れたら NORM ごと死ぬ** — これが唯一 NORM を反証しうる欄。

**committed 欄の総数 = 11(`P-I10-0` … `P-I10-10`。うち `P-I10-9` は条件付き)。**

---

## 7. NULL 枝(事前登録)

> ### NULL-I10(三つ巴のどれでもない)
> $$\boxed{\ \text{奇部が}\ 5\ \text{でも}\ 25/375\ \text{でもない第三の値}\ }$$

**解釈(凍結時点で固定)**:
1. **刈り込みの処方が非自明** — これは NORM の**中身の発見**であり、I10-1 の本来の目的(「処方を書き下す」)が測定から直接得られる。例えば $r=3$ で奇部 $=25$($=B$ の一部)や $75$ なら「奇部は $\langle\bar x\rangle$ と $B$ の間の $Q$-部分加群」という新しい形が立つ。
2. **2-部が $1$ か $4$**(P-I10-5 の外れ)— 尾部律の帰属が「Stab の $\mathrm{Syl}_2$」でも「尾部の $\mathrm{Syl}_2$」でもない第三の規則。
3. **$\lvert\mathrm{GTSh}\rvert\nmid\lvert N_{S_n}(\langle\bar x\rangle)\rvert$** — NORM の包絡そのものの反証。13 窓の「正規化群の 2-局所化」という読み全体が崩れる。**最も情報量が大きい外れ方**。
4. **STR-1 側**: (H2) は成立($\gcd(5,4)=1$)なので、ここで STR-2 の形($\mathrm{Syl}_2\times\mathrm{Hol}$)が崩れれば **(H2) 以外の理由**で崩れたことになる。梯子($N_{\rm ord}=9$・(H2) 破れ)との**対照実験**として機能する。

**部分 NULL**: `W-E-A12-9t3`(既凍結)と本稿 2 窓で結論が割れた場合は、$N_{\rm ord}$($9$ vs $5$)・$r$($1$ vs $2,3$)・(H2) の成否のどれが効いたかを記録する。

---

## 8. 撃ち順(凍結時点で固定)

| 順 | 窓 | $\Xi$ | 目的 | 備考 |
|---|---|---|---|---|
| **0** | `W-E-A12-9t3`(**既凍結・追加発射なし**) | 8,748 | `P-A13-3` の判定がそのまま **ISO-x̄ vs CYC-GEN の第一報**(18 vs 54) | 梯子の順序どおりに走れば自動的に出る |
| **1** | `W-E-A10-5x2t0` | **5,000** | **P-I10-0 較正ゲート**(素経路 $\times$ $\Xi$ 経路)+ P-I10-1/3/5/6/7 | **P-I10-0 が PASS しなければ以降を撃たない** |
| 2 | `W-E-A15-5x3t0` | 1,125,000 | **P-I10-4**(非アーベル核の有無)+ **P-I10-8/9**(I10-2 の判定) | 順 1 で CYC-GEN が勝った場合は最優先(非アーベル核が確定する) |

**根拠**: (i) 順 0 は追加費用ゼロ。(ii) 順 1 は $\Xi=5{,}000$ で**梯子の最安段($486$)に次ぐ安さ**、しかも素の経路も走るので較正を兼ねる。(iii) 順 2 だけが**非アーベル奇部**と $\mathrm{dl}$ を測れるが $225$ 倍高い — 順 0/1 で ISO-x̄ が 2 連勝したら順 2 は「確認」の位置づけに下がる(それでも $N_{\rm ord}$ 不変・$r$ だけ動かす対照として価値が残る)。

---

## 9. 測定スペック

```text
0.  canonical_id            = SHA-256(canonical 文字列)      # §2 と一致しなければ Error
1.  group_order             = |GTSh(N,N)|                     # P-I10-6
2.  ker_size                = |ker chi~|                      # P-I10-1,2
3.  ker_odd_part_order      = ker_size の奇部分                # P-I10-3(判別スカラー)
4.  ker_2_part_order        = ker_size の 2 部分               # P-I10-5
5.  K_struct                = ker chi~ の構造記述              # P-I10-1,2,4
6.  K_is_abelian            = ker chi~ はアーベルか            # P-I10-4
7.  K_odd_derived_order     = |[A,A]| (A = 核の奇部)           # 非アーベルなら >1
8.  chi_image_order         = |Q| ,  Q_struct                  # P-I10-7
9.  iso_to_C2_times_HolC5   = IsomorphismGroups(G, C2 x Hol(Z/5)) != fail   # P-I10-6
10. G_divides_normalizer    = group_order | |N_{S_n}(<xbar>)|  # P-I10-10 (200 / 3000)
11. derived_length_G        = dl(GTSh)                         # P-I10-8
12. derived_series_G        = |G'|, |G''|, |G'''|              # P-I10-9(X'=A か B 止まりか)
13. xi_count_measured / xi_count_bound                          # fail-closed
##  W-E-A10-5x2t0 のみ
14. naive_shadow_digest / xi_shadow_digest                      # P-I10-0
```

**判定表**

| 欄 | PASS 条件 | FAIL の意味 |
|---|---|---|
| P-I10-0 | 欄 14 の 2 digest が一致 | $\Xi$-制限の実装障害 ⟹ 全測定の再検査 |
| P-I10-1/2 | 欄 2 $=10$ | $50$/$750$ なら CYC-GEN。他値は NULL |
| P-I10-3 | 欄 3 $=5$ | $25$/$375$ = CYC-GEN。中間値 = **NORM の処方が非自明**(§7-1) |
| P-I10-4 | 欄 6 $=$ true | **非可換核の第一標本**。STR-1 (H1) がその窓で破れる |
| P-I10-5 | 欄 4 $=2$ | $1$ なら 2-部は尾部由来(尾部律が字義どおり)・$4$ 以上なら第三の規則 |
| P-I10-6 | 欄 9 $\ne$ fail かつ 欄 1 $=40$ | (H2) は成立しているので、崩れれば **(H2) 以外の理由**(梯子との対照) |
| P-I10-7 | 欄 8 $=4$ | $Q$ が真部分群 ⟹ 第二 hexagon が層を落とす |
| P-I10-8 | 欄 11 $=2$ | $3$ なら **DL3-ODD 発火** = 尾部を伸ばさない非 metabelian 経路が開く(**一級**) |
| P-I10-9 | (CYC-GEN 時のみ)欄 12 で $\lvert G'\rvert$ が $A$ か $B$ か | $A$ なら $[T,Q]\ne1$、$B$ なら $=1$ |
| P-I10-10 | 欄 10 $=$ true | **NORM の包絡そのものの反証**(§7-3) |

---

## 10. 自己監査

| # | リスク | 判定 |
|---|---|---|
| R-1 | 発案の算術を鵜呑みにしていないか | ○ 全項目を再導出。**3 件の誤り**(最小候補 void・$r=2$ の判別力・I10-2 の $X'=A$)を §4.3 / §5 に訂正として明記 |
| R-2 | $\bar x=(3,3,3,1^t)$ の否決は本当か | ○ 系 0.4′ は既存の紙上系(第二撃ノート §0)。本稿は $N_{\rm ord}$ の**定義に即した**再導出(命題 1.1)を添えた。$\mathrm{ord}(\bar x)=\ell$($=\ell^r$ ではない)が要点 |
| R-3 | `W-E-A15-5x3t0` の存在は確実か | ○ **構成的**(明示対+全 assert)。ただし実現対の**個数**は無作為探索なので悉皆ではない(存在のみ主張) |
| R-4 | ISO-x̄ の「13 窓全一致」は検証したか | △ **未検証**。発案の申告をそのまま引いている。私が確認したのは (i) 単一巡回窓で三者が一致する代数的理由(§4.1)と (ii) 梯子の予言値との整合であって、13 窓の**実測**との突合ではない |
| R-5 | 三者が本当に判別されるか | ○ 床 $5$ / 天井 $25,375$ が相異なることを機械値で確認。NORM だけは包絡なので P-I10-10 でしか反証されない — **この非対称は明示** |
| R-6 | $t=0$ に固有の落とし穴 | △ $t=0$ では「尾部」が存在せず、2-部の出所が輪積 top $S_r$ に移る。既存 13 窓(すべて $t\ge1$)との**構造的な断絶**であり、P-I10-5 が外れたらそれは律の反証ではなく **$t=0$ が別レジームだった**可能性がある |
| R-7 | 予言が当たっても機構は分からない | ○ ISO-x̄ が 3 連勝しても「奇部は $\langle\bar x\rangle$ ちょうど」という**現象法則**が増えるだけ。証明は open(発案 I10 の「誰も聞いていない問い 2」がまさにその穴) |
| R-8 | 接触遮断 | ○ 2 窓は本セッション構成・judge 未使用 |

---

## 11. 未閉鎖項

* 【I10-a】凍結手続き: 司令塔の commit で凍結。凍結前に driver を起動しない。
* 【I10-b】**ISO-x̄ の「13 窓全一致」の実測突合**(R-4)。発案の申告を台帳の実測値と突き合わせる作業は未実施 — 本予言の土台なので司令塔側で確認されたい。
* 【I10-c】`W-E-A15-5x3t0` の実現対の**悉皆**(現状は存在のみ)。$C_{S_{15}}(\mathsf w)$($=50$)軌道での完全列挙 + 構造定数照合で決着する(`tail8_exact.g` の流用)。兄弟軌道の有無は `P-A13-12` と同型の問題。
* 【I10-d】$r=4$ 以上($O_{2'}(S_4)=1$ なので天井は $C_\ell^4$、$r=5$ で再び非アーベル top)の族設計は未着手。
* 【I10-e】**設計チェックリストへの追加要請**: 「補題 R の紙上算術」の**前に**「系 0.4′($N_{\rm ord}=\mathrm{ord}(\bar x)\ge4$)」を置く。今回の void はこれで 10 秒で捕まった。

## 12. 検算(GAP 4.16.0・単系統)

| スクリプト | 内容 |
|---|---|
| `search/probe/wac_v1/i10_check.g` | $n=10$ 悉皆(65 → 50 実現)・$n=15$ 無作為探索(1,558 試行で発見)・両窓の全 assert・$\Xi$ |
| `search/probe/wac_v1/i10_dl.g` | $C_5\wr C_3$ の導来列・$\ker$ の $\mathrm{dl}$・$N_{S_{15}}(\langle\bar x\rangle)$・**$Q$ の 2 作用での $\mathrm{dl}(X)=2$ vs $3$ の分離** |

**登録宇宙の掃引結果ではない。台帳請求権は発生していない。**

---

---

> # ⛔ 接触遮断の注意書き
>
> **本ファイルは測定 driver の実行エージェントに読ませてはならない。**
>
> - driver へ渡してよいのは **§2 の窓同定情報(canonical ID・生成対・judge preamble・$\Xi$ 上界)と §9 の欄定義(左半分のみ)**。
> - **§4 の予言表・§5 の $\mathrm{dl}$ 分離・§6 の committed 欄・§7 NULL・§8 の目的欄・§9 判定表・§10 は渡さない。** §9 のコード欄右側の `# P-I10-…` コメントも削ること。
> - 判定は測定完了・証明書ハッシュ確定後に司令塔が行う。
> - 番号系は `P-STR-*`(W4)・`P-A13-*`(梯子)と分離済み。
