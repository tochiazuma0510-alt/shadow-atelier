# W-6 否定定理 — **erratum v2**(additive・v1 不改変)

**状態札: `candidate / paper-proof / 紙 + 整数検算(python 単系統・2 本)/ 本 erratum は Sol 未監査 / Lean 検証ではない / 実測ゼロ / 封印 3 量非接触・Im R 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設**
- 方式: **additive erratum**。`docs/notes/w6_kill_theorems_v1.md`(以下 **v1**)は **1 文字も書き換えない**。本書が v1 の該当箇所を上書きする(読む順序: v1 → 本書)。
- 委嘱: 司令塔 —「便 102 **F102-6.2 / F102-6.3** 差戻しの修理」。指示 4 点(構成は採択 2 件を先頭・D17 の両立明示・検算は cert 様式・再検問文案は『再検討を請う』形)を反映済み。
- **入力正本**: `sol/sol_reply_102_math29.md` **§6**(F102-6.1〜6.3)/ v1 / `docs/notes/k5_w6_construction_v1_addendum_b_k20paper.md`(以下 **addendum B**・SHA-256 `21cd745c2e49d7287f91ad110ed89ffd41224bab8249ff53dd7eb0d394556b97`)/ `docs/notes/k5_dn_prereg_k20_draft_v1.md` §1.3・§2.6 / `docs/week1-定義ノート.md` §2(**c ∉ N での θ/τ 語レベル評価の注意**・isolated の定義)/ 正典 arXiv 2405.11725 (3.1)(4.7)(4.8)
- **外部文献ゼロ。**【文献要請】は本書でも**発しない**。

> ## 非接触の申告(v1 から継承・差分を明示)
> - **$\mathrm{Im}\,R_{N,K^{(5)}}$ を一度も測っていない。** 封印 3 量($\hat c_\mu$ / PSL 窓の構造量 / ε bits)非接触。$u$ 値・曲線・dessin・Kummer 非接触。**証明書を 1 本も読んでいない。**
> - **差分**: v1 は python 検算 1 本だったが、本書は **2 本目・3 本目**(`scratchpad/w6_vcen_check.py`・`scratchpad/w6_lattice_check.py`)を追加した。**GAP は依然として一度も呼んでいない。**使った $n=5,20$ の情報は正典 (3.1) の $\psi_m$ の定義式と addendum B の構造だけである。

---

## 0. 判定(先に 6 行)

| # | 対象 | 判定 |
|---|---|---|
| **①** | F102-6.2 の指摘 (a) **THETA-1000 を $c\in N$ 枝へ限定せよ** | ★ **採択**(§1)。さらに v1 の**場合 2 の議論には実際の誤りがあった**(場合分けが 1 つ抜けていた)ことを自己捕獲し、併せて訂正する |
| **②** | F102-6.2 の指摘 (b) **§5.3 の「3 個中 1 個」の文言** | ★ **採択**(§2)。正しくは **2 個**(= $x\leftrightarrow y$ を法として 1 軌道)。⟹ ここから **格子の $\Gamma$-安定性**を追跡したところ、**帯そのものが空**であることが出た(下記 ③) |
| **③** ★★★ | ② の追跡から出た**新結果** | **補題 LAT-Γ**($\Gamma$-安定部分格子の分類)/ **NC-2′**(NC-2 の鋭形)/ **系 THETA-2000**($\lvert PB_3/N\rvert=2000$ は死)/ **系 THETA-4500**($p=3$・4500 は死)。⟹ **生存帯の下限が $p=2$ で 4000、$p=3$ で 13500 へ上がった**(§2.3–2.5) |
| **④** ★★ | F102-6.2 の指摘 (c) **$V\subseteq Z(G_{20})$ は偽・ROOF-KILL の K20 適用を撤回せよ** | ✗ **不採択(反監査)**。$V\subseteq Z(G_{20})$ は**真**である(§3)。二証明 + 機械計算 **$Z(G_{20})=V$(位数 8・ちょうど一致)**。⟹ **K20 への ROOF-KILL 適用は維持**、「独立な第二紙証明」も**維持** |
| **⑤** ★ | v1 §4.3 に実在した欠陥 | ★ **一行の省略**(「$r^{10}$ が各 $D_{20}$ で中心」から $V\subseteq Z(G_{20})$ への段)。**撤回ではなく補完**で閉じる(§3.4 に差替文) |
| **⑥** | F102-6.3(BOTTOM-UP v1 差戻し) | ★ **全面採択**。対応は別紙 `docs/notes/w6_bottomup_design_v2.md`(本書と同時提出) |

> ### ★ 一行で
> $$\boxed{\ \textbf{Sol が計算した }V^\Gamma=\langle(5,5,5)\rangle\ \textbf{(位数 4 の }V^\theta\textbf{ を含む)は正しい。誤っているのは、それを }Z(G_{20})\ \textbf{と同一視した点だけである。}\ }$$
> $$\boxed{\ \textbf{そして格子の }\Gamma\textbf{-安定性を使うと、生存帯は }\lvert PB_3/N\rvert\ge4000\ (p=2)\ /\ \ge13500\ (p=3)\ \textbf{まで狭まる。}\ }$$

---

## 1. 【採択 1】系 THETA-1000 を **$c\in N$ 枝限定**へ(v1 §3.5 の差替)

### 1.1 Sol の指摘(F102-6.2 末尾・逐語要旨)

> THETA-1000 は $c\in N$ の枝なら $\lvert V\rvert=2$ の正規性から $V\subseteq Z(P)$ が自動で、正しい。$c\notin N$ の枝は K5-BIT の word-level 同定が未閉であり、文書自身の【W6K-GAP-1】を飛び越えて無条件とは言えない。

**採択する。** v1 §3.5 は前件を「$N\trianglelefteq B_3$・$N\subseteq K^{(5)}$・isolated・$\lvert PB_3/N\rvert=1000$ の 3 つだけ」「**前件ゼロの否定定理**」と書いたが、これは**過剰主張**であった。

### 1.2 ★ さらに: v1 の場合 2 の議論には**実際の誤り**があった(自己捕獲)

Sol の指摘を検分する過程で、v1 の証明の**場合 2 の場合分けが 1 つ抜けている**ことが分かった。正しい分解は次である。

$c\in K^{(5)}$ かつ $PB_3=F_2\times\langle c\rangle$ ゆえ $K^{(5)}=K^{(5)}_{F_2}\times\langle c\rangle$($c\in K^{(5)}$ より、$(f,c^k)\in K^{(5)}\Rightarrow(f,1)\in K^{(5)}$)。$[K^{(5)}:N]=2$ ゆえ $N=\ker\chi$、$\chi=(\chi_F,\chi_c):K^{(5)}_{F_2}\times\langle c\rangle\twoheadrightarrow\mathbf F_2$。

| 枝 | $\chi_c$ | $\chi_F$ | $c\in N$? | $V=K^{(5)}_{F_2}/N_{F_2}$ | v1 の扱い |
|---|---|---|---|---|---|
| **(a)** | $0$ | $\ne0$ | ✓ | $\cong C_2$ | v1 **場合 1** ✓ 正しい |
| **(b)** | $\ne0$ | $=0$ | ✗ | $=1$ | v1 **場合 2** ✓ この枝のことを書いていた |
| **(c)** ★ | $\ne0$ | $\ne0$ | ✗ | $\cong C_2$ | ★ **v1 は見落としていた** |

⟹ **v1 §3.5 の「$c\notin N$ ゆえ $K^{(5)}=N\langle c\rangle$、したがって $K^{(5)}_{F_2}=N_{F_2}$、すなわち $V=1$」は枝 (c) で偽である。** 枝 (c) では $\lvert V\rvert=2$ であり、$P_N=F_2/N_{F_2}$ の位数は 1000 になる($\lvert P_N\rvert=\lvert G_5\rvert\cdot\lvert V\rvert$)。

**なお枝 (b) の結論も過小に議論されていた**: $V=1$ ゆえ $P_N\cong G_5$ は正しいが、$c\notin N$ では $N_{\rm ord}$ が $K^{(5)}_{\rm ord}$ と異なりうるので、**簡約 hexagon (3.10)(3.11) だけでなく full hexagon (3.3)(3.4) の $c^{\widetilde m}$ 項**が効く。「$\widetilde f=f_1$ 自身が 3 本を満たす」は $c\in N$ の記法での話であって、枝 (b) にそのまま移せない。

### 1.3 ★ 差替後の系 THETA-1000(v2)

> ### 系 THETA-1000(v2・candidate)
> $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$N$ isolated、$\lvert PB_3/N\rvert=1000$、**かつ $c\in N$** とする。このとき
> $$\boxed{\ d_N=5\ (\textbf{検出力ゼロ})\ }$$
> **証明**: v1 §3.5 の**場合 1 のみ**をそのまま用いる($[K^{(5)}:N]=2$、$\lvert V\rvert=2$、$V\trianglelefteq P$ かつ $\lvert V\rvert=2$ ⟹ $V\subseteq Z(P)$ ⟹ (V-cen) 自動、$W\in\{0,V\}$ の 2 択で $W=V$ なら補題 DER-SUF ⟹ THETA-KILL (I)、$W=0$ なら THETA-KILL (III))。∎
> **$c\notin N$(枝 (b)(c))は本系の射程外**とし、【W6K-GAP-1】(v1 §7.3)を**拡張**して開いたままにする(§1.4)。

**同型の訂正を系 THETA-1500(v1 §5.3 の枠)にも適用する**: 前件に **$c\in N$** を追加する((V-cen) 相対である点は v1 のまま・【W6K-GAP-2】も不変)。

### 1.4 【W6K-GAP-1】の拡張(v1 §7.3 の当該行を差し替える)

| 札 | 内容(v2) | 状態 |
|---|---|---|
| **【W6K-GAP-1】**(拡張) | **$c\notin N$ の窓の扱い全般**。(i) 枝 (b)(c) の場合分け(§1.2)(ii) K5-BIT を $c\notin N$ へ適用する規約(定義ノート §2 の警告: 「$\theta/\tau$ を商 $F_2/N_{F_2}$ 上の準同型として評価する近道は $N_{F_2}$ の $\theta,\tau$-不変性を要し、これは $c\in N$ に依存する。$c\notin N$ の対象($M_5$ 等)では近道が壊れる(**定理は無傷**)— 語レベルで適用してから評価すること」)(iii) full hexagon の $c^{\widetilde m}$ 項 | **UNKNOWN** |

> ★ **見通し(証明ではない)**: 定義ノートは「定理は無傷・語レベルで適用せよ」と言う。定理 THETA-KILL (I) の証明は **$F_2$ の恒等式**($w'\theta(w')=1$・$\tau^2(w')\tau(w')w'=1$)を使うので、まさに語レベルである。⟹ 枝 (c) も救える見込みは高いが、**(SURJ) と $\mathrm{Im}\,R$ の同定を $c\notin N$ で書き直す作業が残っている**。ここでは推測として明記し、**結論には使わない**。

---

## 2. 【採択 2】v1 §5.3 の格子の文言 — と、そこから出た**新結果**

### 2.1 文言の訂正(Sol の指摘どおり)

v1 §5.3 の表(行 $\lvert V\rvert=4$)は「**格子 3 個のうち 1 個だけが該当**」と書きながら、直後に **2 個を可・1 個を不可**と列挙していた。**内部矛盾である。**

$2\mathbf Z^2$ の指数 2 部分格子は 3 個:
$$L_1=\langle(4,0),(0,2)\rangle,\qquad L_2=\langle(2,0),(0,4)\rangle,\qquad L_3=\langle(2,2),(4,0)\rangle=\{(a,b)\in2\mathbf Z^2:a\equiv b\ (4)\}.$$
$(2,-2)\notin L_1$、$(2,-2)\notin L_2$、$(2,-2)\in L_3$。⟹ **該当は 2 個**。かつ $\theta:(a,b)\mapsto(b,a)$ が $L_1\leftrightarrow L_2$ を入れ替えるので、**$x\leftrightarrow y$ を法として 1 軌道**である。⟹ 訂正文は「**2 個、$x\leftrightarrow y$ を法として 1 軌道**」。

### 2.2 ★★★ ところが — その 3 個はいずれも $\Gamma$-安定でない

**$N\trianglelefteq B_3$ かつ $c\in N$ ならば $N_{F_2}$ は $\Gamma$-安定**である(braid 共役の $c$-因子が $N$ で消えるから — 定義ノート §2)。$\alpha:F_2\to\mathbf Z^2$ は $\Gamma$-同変ゆえ:

$$\boxed{\ \alpha(N_{F_2})\subseteq\mathbf Z^2\ \textbf{は }\Gamma\textbf{-安定部分格子である。}\ }$$

$\Gamma$ の $\mathbf Z^2=F_2^{\rm ab}$ 上の作用は $\theta(a,b)=(b,a)$、$\tau(a,b)=(-b,\ a-b)$($\tau(\bar x)=\bar y$、$\tau(\bar y)=-\bar x-\bar y$)。

> ### ★★ 補題 LAT-Γ(candidate・本書)
> $\mathbf Z^2$ を上の $\Gamma$-加群($S_3$ の標準格子)とみなし、$\mathbf Z[\omega]$($\omega$ = 1 の原始 3 乗根)と $\bar x\mapsto1$、$\bar y\mapsto\omega$ で同一視する。このとき
> **(a)** $\tau$ = $\omega$ 倍、$\theta$ = $\omega\cdot(\text{複素共役})$。
> **(b)** 有限指数の $\Gamma$-安定部分格子 = **共役安定イデアル** $=(n)\cdot(1-\omega)^a$($n\ge1$、$a\ge0$)。
> **(c)** ⟹ **指数は $n^2\cdot3^a$ の形に限る**。とくに
> $$\boxed{\ \textbf{指数 2 の }\Gamma\textbf{-安定部分格子は存在しない。}\ \textbf{2 冪指数は }4^j\ \textbf{のみ(}\Lambda=2^j\mathbf Z^2\textbf{)。}}$$

**証明.** (a) $\tau(\bar x)=\bar y$ は $1\mapsto\omega$、$\tau(\bar y)=-\bar x-\bar y$ は $\omega\mapsto-1-\omega=\omega^2$ ⟹ $\tau$ は $\omega$ 倍 ✓。$\theta$ は $1\mapsto\omega$、$\omega\mapsto1$ で、$\omega\cdot\overline{(\cdot)}$ が $1\mapsto\omega$、$\omega\mapsto\omega\cdot\omega^2=1$ ✓。
(b) $\omega$ 倍で閉じた加法部分群 = $\mathbf Z[\omega]$-部分加群 = イデアル。$\theta=\omega\sigma$ 安定 ⟺ $\sigma$(共役)安定。$\mathbf Z[\omega]$ は PID で、共役安定イデアルは、分解する素数 $p\equiv1(3)$ で $\pi,\bar\pi$ の指数が等しい ⟹ 有理整数の冪、惰性素数 $p\equiv2(3)$ で $(p)$ 自身、分岐素数 3 で $(1-\omega)$(自己共役)。⟹ $(n)(1-\omega)^a$。
(c) ノルム $N((n)(1-\omega)^a)=n^2 3^a$。$2=n^23^a$ は不可能。2 冪 $2^k=n^23^a$ ⟹ $a=0$、$k$ 偶、$n=2^{k/2}$。∎

**機械確認**(`scratchpad/w6_lattice_check.py`・§5): $(\mathbf Z/12)^2$ の全部分群を悉皆列挙して $\Gamma$-安定なものを抽出した結果、指数集合は $\{1,3,4,9,12,16,36,48,144\}$ = **144 の約数のうち $n^23^a$ 型のもの全体**と**一致**(E1/E5)。**指数 2 は現れない**(E2)。2 冪指数は $\{1,4,16\}$ のみ(E3)。上の $L_1,L_2,L_3$ が個別に $\Gamma$-非安定であることも直接確認(E6)。

### 2.3 ★★ NC-2 の鋭形(v1 §5.2 NC-2 の差替)

$\alpha(K^{(5)}_{F_2})=2\mathbf Z^2=(2)$($G_5^{\rm ab}\cong C_2^2$ から。2 は $\mathbf Z[\omega]$ で惰性ゆえ $\Gamma$-安定 ✓ 整合)。$V/W\cong2\mathbf Z^2/\alpha(N_{F_2})$(v1 §3.4)。

> ### ★★ 系 NC-2′(candidate・本書)
> $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$c\in N$ とする。
> **(a) $V/W$ が 2 群のとき**: $\alpha(N_{F_2})=(2^{j+1})=2^{j+1}\mathbf Z^2$($j\ge0$)であり、
> $$\textbf{NC-2}\ \bigl((2,-2)\notin\alpha(N_{F_2})\bigr)\iff j\ge1\iff \lvert V/W\rvert=4^{\,j}\ \ge4 .$$
> とくに **$p=2$ では NC-2 は「(V-der) が破れる」と同値**である(v1 §3.4 の「$V/W\ne0$ だけでは足りない」は、$p=2$ に関する限り**強すぎた**)。
> **(b) $V/W$ が 3 群のとき**: $\alpha(N_{F_2})=(2)(1-\omega)^a$ であり、$\bar x-\bar y=1-\omega$ が $(1-\omega)$ の生成元ゆえ
> $$\textbf{NC-2}\iff a\ge2\iff \lvert V/W\rvert=3^a\ \ge9 .$$

**証明.** (a) $\alpha(N_{F_2})\subseteq(2)$ は $\Gamma$-安定で指数 $[\,(2):\alpha(N_{F_2})]=\lvert V/W\rvert$ が 2 冪 ⟹ $[\mathbf Z^2:\alpha(N_{F_2})]=4\lvert V/W\rvert$ も 2 冪 ⟹ 補題 LAT-Γ (c) より $\alpha(N_{F_2})=2^{j+1}\mathbf Z^2$。$(2,-2)=2(1-\omega)$ が $(2^{j+1})$ に入る ⟺ $(1-\omega)\in(2^{j})$ ⟺ $j=0$(ノルム 3 は 4 で割れない)。
(b) 指数 $4\cdot3^a$ の共役安定イデアルは $(2)(1-\omega)^a$。$(2,-2)=2(1-\omega)\in(2)(1-\omega)^a$ ⟺ $(1-\omega)\in(1-\omega)^a$ ⟺ $a\le1$。∎

### 2.4 ★★★ 系 THETA-2000 と 系 THETA-4500(**帯が 2 つ空になった**)

> ### 系 THETA-2000(candidate・本書)
> $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$N$ isolated、**$c\in N$**、**(V-cen)**、$\lvert PB_3/N\rvert=2000$(⟺ $\lvert V\rvert=4$)とする。**$V$ の型は問わない**($C_2^2$ でも $C_4$ でも可)。このとき
> $$\boxed{\ d_N=5\ (\textbf{検出力ゼロ})\ }$$
> **証明.** $\lvert V/W\rvert\in\{1,2,4\}$ だが補題 LAT-Γ (c) により $\lvert V/W\rvert=2$ は不可能。
> - $\lvert V/W\rvert=1$ ⟹ $W=V$ = (V-der) ⟹ 補題 DER-SUF ⟹ **THETA-KILL (I)**。
> - $\lvert V/W\rvert=4$ ⟹ $W=0$ ⟹ **THETA-KILL (III)**。
>
> どちらでも (V-cen) と併せて THETA-KILL (IV) が発火。∎
> ★ **これは v1 §5.3 が「生存しうる」と書いた帯であり、しかも【BU-GAP-1】の $C_4$ 型核も同時に消す。**

> ### 系 THETA-4500(candidate・本書)
> 同じ前件で $\lvert PB_3/N\rvert=4500$(⟺ $\lvert V\rvert=9$)ならば $d_N=5$。
> **証明.** $\lvert V/W\rvert\in\{1,3,9\}$。NC-2′ (b) より $\lvert V/W\rvert\le3$ は NC-2 を破る ⟹ **THETA-KILL (I)**(KT-7)。$\lvert V/W\rvert=9$ ⟹ $W=0$ ⟹ **THETA-KILL (III)**(KT-4)。∎

### 2.5 ★★ 生存帯の下限(v1 §5.2 末尾・§5.3 の表を差し替える)

$\lvert W\rvert\ge2$(NC-3)と NC-2′ から:

| $p$ | $\lvert V/W\rvert$ の最小 | $\lvert W\rvert$ の最小 | $\lvert V\rvert$ の下限 | $\boxed{\lvert PB_3/N\rvert\ \textbf{の下限}}$ |
|---|---|---|---|---|
| **2** | **4** | 2 | **8** | ★ **4,000**(v1 は 2,000) |
| **3** | **9** | 3 | **27** | ★ **13,500**(v1 は 4,500) |

> ### ★★ 差替後の帯表(v1 §5.3 の置換)
> | $\lvert V\rvert$ | $\lvert PB_3/N\rvert$ | 判定(v2) |
> |---|---|---|
> | 2 | 1,000 | ★★ **死**(系 THETA-1000 v2・**$c\in N$ 限定**) |
> | 4 | **2,000** | ★★★ **死**(系 THETA-2000・**新**・(V-cen) 相対・核の型を問わない) |
> | 8 | 4,000 | ★ **生存しうる**。ただし $\lvert W\rvert=2$、$\lvert V/W\rvert=4$、$\alpha(N_{F_2})=4\mathbf Z^2$ が**強制**される($K^{(20)}$ と同じ形。ただし $K^{(20)}$ 自身は KT-6 で死ぬ) |
> | 16 | 8,000 | 生存しうる($\lvert W\rvert=4$、$\lvert V/W\rvert=4$ が強制) |
> | 3 | 1,500 | 死(系 THETA-1500・(V-cen) + $c\in N$ 相対) |
> | 9 | **4,500** | ★★★ **死**(系 THETA-4500・**新**) |
> | 27 | 13,500 | $p=3$ の**最下段の生存候補**($\lvert W\rvert=3$、$\lvert V/W\rvert=9$ 強制) |

> ⚠ **$K^{(20)}$ との三重整合**(較正): $\lvert V\rvert=8$、$\lvert W\rvert=2$、$\lvert V/W\rvert=4$、$\alpha(N_{F_2})=4\mathbf Z^2$ ⟹ $\lvert G_{20}^{\rm ab}\rvert=\lvert\mathbf Z^2/4\mathbf Z^2\rvert=16$ — これは v1 §8 B2 の機械値 **16** と一致し、本書 §5 の D7($\lvert[G_{20},G_{20}]\rvert=250$、$4000/250=16$)とも一致する。**独立に導いた 3 つの経路が同じ値を返す。**

---

## 3. 【反監査】F102-6.2 の中心性判定について — **$V\subseteq Z(G_{20})$ は真である**

### 3.1 Sol の主張(逐語)

> 各座標の $r^{10}$ が各 $D_{20}$ で中心であることから、三座標核 $V\cong\mathbf F_2^3$ 全体が $G_{20}$ で中心とは従わない。S4 は三座標を置換し、例えば $(5,0,0)$ を別座標へ移す。固定されるのは対角線 $W=\langle(5,5,5)\rangle$ であり、$V\not\subseteq Z(G_{20})$ である。

### 3.2 ★ 診断 — $Z(P)$ と $V^\Gamma$ の取り違え

$\theta,\tau$ は **$B_3/PB_3\cong S_3$ 由来の外部自己同型**であって、$P=PB_3/N$ の**内部**共役ではない。したがって

$$\boxed{\ \textbf{「}\Gamma\textbf{ が座標を置換する」}\ \textbf{は}\ V^\Gamma\subsetneq V\ \textbf{を意味するが、}\ Z(P)\ \textbf{とは無関係である。}\ }$$

補題 SURJ-CENT(v1 §2.2)が使う前件は **$V\subseteq Z(P)$、$P=P_N=F_2/N_{F_2}$**(= $PB_3/N$)のみであり、$\widehat P=B_3/N$ の中心ではない。(SURJ) の主張 $\langle\bar x,\widetilde f^{-1}\bar y\widetilde f\rangle=P$ も $P$ の中で閉じている(定義ノート §2 の「有限商では $\langle\bar x^{2m+1},\bar f^{-1}\bar y^{2m+1}\bar f\rangle=F_2/N_{F_2}$」)。

> ⚠ Sol が挙げた「$V\not\subseteq Z(\widehat P)$」に相当する事実は**真**である($\Gamma$ が座標を置換するので $V$ は $B_3/K^{(20)}$ の中心に入らない)。**しかし補題 SURJ-CENT はそれを要求していない。**
> ⚠ 記号についても: この位置で座標を置換するのは **$\Gamma$ の像 $S_3$**(3 座標の置換)であって $S_4$ ではない(addendum B §2.3: 「$p=2$ では (4.7) の符号が消えるので $\Gamma\vert_V$ の像は $S_4$ ではなく $S_3$」)。

### 3.3 ★★ $V\subseteq Z(G_{20})$ の二証明

**設定**(addendum B §1・正典 (3.1) 逐語): $D_m=\langle r,s\mid r^m,s^2,srs^{-1}r\rangle$(位数 $2m$)、
$$\psi_m:PB_3\to D_m^3,\qquad x\mapsto(r,s,s),\quad y\mapsto(rs,r,rs),\quad c\mapsto(1,1,1),$$
$G_m=\mathrm{Im}\,\psi_m\le D_m^3$、$V=\ker(G_{20}\to G_5)=\langle r^{10}\rangle^3$(addendum B §2.2)。

> ### 証明 A(周囲群の中心)
> $m=20$ は偶数ゆえ $Z(D_{20})=\langle r^{10}\rangle$(位数 2)。したがって
> $$V=\langle r^{10}\rangle^3=Z(D_{20})^3=Z(D_{20}^{\,3}).$$
> $\psi_{20}$ は**直積** $D_{20}^3$ への準同型である(正典 (3.1)・座標の置換は像に入らない)から $G_{20}\le D_{20}^3$。$V\subseteq G_{20}$ かつ $V\subseteq Z(D_{20}^3)$ ゆえ、$V$ の元は $G_{20}$ の全元と可換。∎
> $$\Longrightarrow\ \boxed{\ V\subseteq Z(G_{20})\ }$$

> ### 証明 B(座標作用・周囲群を使わない)
> $A_{20}=\langle r^2\rangle^3\cong(\mathbf Z/10)^3$ はアーベル(addendum B §2.1)で $V\subseteq A_{20}$。$G_{20}=\langle X,Y,\psi_{20}(c)\rangle$ であり、$\psi_{20}(c)=1$ は自明に $V$ を中心化する。$X,Y\in D_{20}^3$ の各座標は $D_{20}$ の元だから、$\langle r^2\rangle$ 上の共役作用は各座標で $+1$(回転)か $-1$(反射)、すなわち **$A_{20}$ 上で符号対角行列**である(実際 addendum B §2.3 / bottomup §2.2 の $X\mapsto\mathrm{diag}(1,-1,-1)$、$Y\mapsto\mathrm{diag}(-1,1,-1)$)。$V=\{5b:b\in\mathbf F_2^3\}$ は $A_{20}$ の 2-捻れ部分であり、$-5\equiv5\ (10)$ ゆえ**符号は $V$ 上で不可視**。⟹ $X,Y$ は $V$ を中心化する。∎

> ★ 証明 B は addendum B が「$p=2$ で (4.7) の符号が消える」と警告した現象そのものである(W6B-4)。**同じ符号消失が (V-cen) を保証している。**

### 3.4 ★ v1 §4.3 に実在した欠陥と、その**補完**(撤回ではない)

v1 §4.3 の当該行は
> - $V\subseteq Z(G_{20})$: $r^{10}$ は $D_{20}$ の中心元($sr^{10}s^{-1}=r^{-10}=r^{10}$)⟹ **(V-cen) ✓**

であった。**「各 $D_{20}$ で中心」から「$G_{20}$ で中心」への一行が省略されている。** 結論は正しいが、その一行が無いために Sol の再現で分岐が起きた。**差替文(v2 で採用する逐語)**:

> - **(V-cen) ✓**: $m=20$ は偶数ゆえ $Z(D_{20})=\langle r^{10}\rangle$、したがって $V=\langle r^{10}\rangle^3=Z(D_{20}^{\,3})$。正典 (3.1) の $\psi_{20}$ は**直積** $D_{20}^3$ への準同型だから $G_{20}\le D_{20}^3$ であり、$V\subseteq G_{20}\cap Z(D_{20}^3)\subseteq Z(G_{20})$。**別証**: $V$ は アーベルな $A_{20}$ の 2-捻れ部分で、$G_{20}$ は $A_{20}$ 上に符号対角 $\pm1$ で作用し、$-5\equiv5\ (10)$ ゆえ $V$ 上では自明。**なお $V$ は $\Gamma$ で点ごとには固定されない**($V^\Gamma=\langle(5,5,5)\rangle=W$)— **これは中心性とは別の量である**(補題 SURJ-CENT が使うのは $Z(P)$ であって $V^\Gamma$ ではない)。

### 3.5 ★★ 機械計算(決着)— **$Z(G_{20})=V$、同時に $V^\theta$ は位数 4**

`scratchpad/w6_vcen_check.py`(§5・17 項 ALL PASS)より、**$G_{20}$ を $D_{20}^3$ の中で明示構成**して:

| # | 検査 | 値 |
|---|---|---|
| **D1** | $\lvert G_{20}\rvert$ | **4000** ✓ |
| **D4** | $V$ の全 8 元 × $G_{20}$ の全 4000 元で可換か | ★ **真**(悉皆) |
| **D5/D6** | $\lvert Z(G_{20})\rvert$ / $Z(G_{20})=V$ か | ★★ **8 / 真** — **中心はちょうど $V$ に一致する** |
| **D7/D8/D9** | $\lvert[G_{20},G_{20}]\rvert$ / $\lvert W\rvert$ / $W=$ 対角 | 250 / 2 / 真 ✓(prereg §2.6 と一致) |
| **D10–D13** | witness $(6,4,0)=(r^{12},r^8,1)$ が $G_{20}$ と $[G_{20},G_{20}]$ に属し、$\bmod5$ で $f_1$ と一致 | ✓(v1 §4.3 の再現) |
| **D14** | $X\leftrightarrow Y$ が $G_{20}$ の自己同型($G\times G$ 内の graph の位数 $=\lvert G\rvert$) | ✓ |
| **D15** ★ | $\lvert V^\theta\rvert$ | ★ **4**(= $V$ 全体 8 ではない)— **Sol の計算はここを見ている。値は正しい** |
| **D16** | $W\subseteq V^\theta$ | ✓ |
| **D17** ★★ | ★ **$(V\subseteq Z(G_{20}))$ と $(V^\theta\ne V)$ が同時に成り立つ** | ★★ **真** |

$$\boxed{\ \textbf{D17: 「}V\ \textbf{は }G_{20}\ \textbf{の中心に入る」と「}\Gamma\ \textbf{は }V\ \textbf{を点ごとに固定しない」は両立する。前者が (V-cen)、後者が Sol の計算した量である。}\ }$$

### 3.6 ⟹ 撤回しない範囲(**明示**)

| v1 の主張 | v2 での扱い |
|---|---|
| 定理 ROOF-KILL (a)–(f) | ★ **維持**(F102-6.2 も「中心性を含む条件付き補題としては成立」と認めている) |
| 補題 SURJ-CENT | ★ **維持**(F102-6.2 も「$V\subseteq Z(P)$ の前件の下では正しい」と認めている) |
| **§4.3 の $K^{(20)}$ 適用**($\delta_{\rm roof}=0$・(V-cen) ✓・$d_{K^{(20)}}=5$) | ★★ **維持**(§3.3 の二証明 + §3.5 の機械計算で前件が満たされることを示した) |
| 「**ROOF-KILL が K20-LIFT/Thm 4.3 と独立な第二の紙証明を与えた**」 | ★★ **維持**。ただし v1 と同じく **`cross-checked` は名乗らない**(両方とも紙・同一起草者・CV-9 非当事者判読を経ていない) |
| witness $(6,4,0)$ の位置づけ | ★ **ノルム witness かつ SURJ witness**(v1 のまま)。F102-6.2 の「ノルム witness を与えるが、それだけで SURJ は出ない」は、前件 (V-cen) が満たされている以上、本件には当たらない |

---

## 4. 波及(下流文書へ)

| 文書 | 影響 | 処置 |
|---|---|---|
| `w6_bottomup_design_v1.md` **U-4** | 「$\dim_{\mathbf F_2}V=1$ / $\dim_{\mathbf F_3}V=1$ を除外」は**弱すぎた**。新たに $\lvert V\rvert=4$(2000)と $\lvert V\rvert=9$(4500)も空 | ★ v2 設計で **U-2/U-3 を再凍結**(別紙 §6) |
| 同 **U-3**($p=3$・$\dim=2$・4500) | ★ **帯が空**(系 THETA-4500) | ★ v2 では $p=3$ は cap 8000 の下で**候補ゼロ**。掘るなら 13500 以上 |
| 同 **S4**(アーベル化篩) | $p=2$ では S5(=$W\ne0$)と合わせて「$0\ne W\ne V$」に潰れる(NC-2′ (a)) | ★ v2 で段を統合 |
| v1 §5.2 **NC-2** | ★ **NC-2′ に差替**(§2.3) | 本書 |
| v1 §5.3 帯表 | ★ **差替**(§2.5) | 本書 |
| v1 §3.5 系 THETA-1000 | ★ **$c\in N$ 限定へ差替**(§1.3) | 本書 |
| `docs/地図.md` | 「2-primary 最下段 1000/2000」の記述があれば下限 4000 へ | ★ **司令塔案件**(本書は地図を書き換えない) |

---

## 5. 検算(**cert 様式**・証明とは独立・single lane python・GAP 呼び出しゼロ)

```
conventions_used:
  ledger_version:        (本書は台帳 cert ではない — 参照のみ)
  D_m_presentation:      <r,s | r^m, s^2, s r s^-1 r>,  |D_m| = 2m
  psi_m (正典 3.1):      x -> (r,s,s),  y -> (rs,r,rs),  c -> (1,1,1)
  element_encoding:      (eps,k) = r^k s^eps ;  (a,ea)*(b,eb) = (a + (-1)^ea b, ea+eb)
  A_20_basis:            a1=X^2, a2=Y^2, a3=(XY)^-2  (addendum B §2.1・(Z/10)^3 座標)
  Gamma_on_F2ab:         theta(a,b)=(b,a) ; tau(a,b)=(-b, a-b)
  Zomega_identification: x̄ -> 1, ȳ -> omega  (補題 LAT-Γ)
  perm_composition:      (置換を使わない — 直積成分ごとの積のみ)
  seal_contact:          none (Im R / ĉ_mu / PSL / eps bits いずれも非接触)
  gap_invoked:           false
```

| script | SHA-256 | 項目 | 結果 |
|---|---|---|---|
| `scratchpad/w6_vcen_check.py` | `6f8b1f0435a1450070b9eb3005d8f1f654de511d50e6a6e8e5623d7c92453fcd` | **D1–D17**(17 項・内訳は §3.5 の表) | **FAILS = 0** |
| `scratchpad/w6_lattice_check.py` | `c4f321d4d211fbff4b5c49882ef4a19e41ef6346836d22c47c6dffcba080737f` | **E1–E9**(11 行・$(\mathbf Z/12)^2$ 内の部分群悉皆 → $\Gamma$-安定の指数集合) | **FAILS = 0** |

**Python 3.13.14 / 両者とも `RESULT: ALL PASS`。**

> ⚠ **E4 は初稿で FAIL した。** 当方の期待値「3 冪指数は $1,3,9,27,81$ が現れる」が誤りで、走査窓が $(\mathbf Z/12)^2$($144=16\cdot9$)である以上 $27\nmid144$ ゆえ $\{1,3,9\}$ しか現れ得ない。**期待値を訂正して PASS**(検査自体は残した)。⟹ **理論が偽だったのではなく当方の窓の読み違えを機械が捕まえた事例**であり、v1 §8 の B16 と同型の記録である(S-8 の趣旨: 値を後から弱めたのではなく、窓が決める正しい値に直した)。
> ⚠ **E1 の期待値は `stable` 自身から作っているので、E1 単体は記述**である。**荷重は E2/E3/E5/E6** にある(指数 2 の非存在・2 冪指数の限定・全指数が $n^23^a$ 型・3 個の格子の個別非安定)。

---

## 6. 格付け・【GAP】・新規性

### 6.1 格付け

| 主張 | 格 |
|---|---|
| **§3 の $V\subseteq Z(G_{20})$**(二証明 + 悉皆機械計算) | ★★★ **paper-proof candidate + 整数検算(悉皆)**。$Z(G_{20})=V$ は $\lvert G_{20}\rvert=4000$ の**有限悉皆**なので紙と機械が同じ対象を見ている |
| **補題 LAT-Γ** | ★★ **paper-proof candidate**($\mathbf Z[\omega]$ の初等整数論・機械側は $(\mathbf Z/12)^2$ の悉皆) |
| **系 NC-2′** | ★★ **paper-proof candidate** |
| **系 THETA-2000 / THETA-4500** | ★★★ **paper-proof candidate**((V-cen) + $c\in N$ 相対) |
| **系 THETA-1000 (v2)** | ★★ **paper-proof candidate**($c\in N$ 限定・前件 4 つ) |
| §1.2 の場合分け (a)(b)(c) | ★ **成立**(初等・v1 の誤りの自己捕獲) |
| `cross-checked` / `verified` | ✗ **どちらも付さない**(単一起草者・python 単系統・Lean なし) |

### 6.2 【GAP】(新設・更新)

| 札 | 内容 | 状態 |
|---|---|---|
| **【W6K-GAP-1】**(拡張) | $c\notin N$ の窓の扱い全般(§1.4) | **UNKNOWN** |
| **【W6K-GAP-6】** ★新 | 系 THETA-2000 / THETA-4500 の **(V-cen)**。$\lvert V\rvert=4,9$ では中心性は自動でない | **UNKNOWN**(【K5-GAP-W1】と同根) |
| **【W6K-GAP-7】** ★新 | 補題 LAT-Γ は **$c\in N$**(⟹ $N_{F_2}$ の $\Gamma$-安定性)に依存する。$c\notin N$ では $\alpha(N_{F_2})$ の $\Gamma$-安定性そのものが不明 | **UNKNOWN**(【W6K-GAP-1】に従属) |
| 【W6K-GAP-2〜5】 | v1 のまま(THETA-1500 の (V-cen)・witness 同定・非可換 $W$・THETA-KILL (I) の逆) | 不変 |

### 6.3 新規性(**grep 済** — `docs/ sol/ provenance/` 全文)

**grep 語**: `THETA-2000`・`THETA-4500`・`LAT-Γ`/`LAT-Gamma`・`NC-2′`・`Z[\omega]`・`共役安定イデアル`・`Γ-安定`・`Frattini`・`Phi(P)`・`2\mathbf Z^2`。

| 項目 | 既出か | 差分 |
|---|---|---|
| **補題 LAT-Γ**($\Gamma$-安定部分格子 = 共役安定イデアル) | **発見できず** | ★★ **本書**。ただし「$S_3$ 格子 = $\mathbf Z[\omega]$、安定部分格子 = イデアル」は**代数的整数論では標準**であり **「初」とは書かない** — **本設定($\alpha(N_{F_2})$ への適用)への翻訳が寄与**である |
| **系 NC-2′ / THETA-2000 / THETA-4500** | **発見できず** | ★★★ **本書** |
| $V\subseteq Z(G_{20})$ | v1 §4.3 に**一行だけ**既出(省略つき) | ★ 本書は**証明を 2 本与え、悉皆機械計算で $Z(G_{20})=V$ まで確定** |
| Frattini 経路の (SURJ) | ★ **既出**(補題 SURJ-W6・`ideas_020_review_v1.md` §1.2 (e)) | 本書は使わない(§7 の設計側で再利用) |
| $c\notin N$ の枝 (c) | **発見できず** | ★ **本書**(v1 の誤りの自己捕獲) |

---

## 7. Sol への再検問文案(**便 103 同梱用・逐語**)

> ### 【収載原稿ここから】(便 103 §x)

### W103-x 【再検討の請求】F102-6.2 の中心性判定について

**F102-6.2 の 3 点のうち 2 点を採択し、1 点について再検討をお願いします。**

**採択 1(THETA-1000)**: ご指摘のとおり、$c\notin N$ の枝は【W6K-GAP-1】を跨いでおり「前件ゼロ」は過剰主張でした。**$c\in N$ 限定へ差し替えます**。さらに検分の過程で、$c\notin N$ の枝には当方の**実際の誤り**があったことが分かりました。$K^{(5)}=K^{(5)}_{F_2}\times\langle c\rangle$ の指数 2 部分群は $\chi=(\chi_F,\chi_c)$ で 3 枝に分かれ、当方が書いた $V=1$ は $\chi_F=0$ の枝だけです。$\chi_c\ne0$ かつ $\chi_F\ne0$ の枝では $\lvert V\rvert=2$ で、当方はこれを見落としていました。系 THETA-1500 にも同じ限定を掛けます。

**採択 2(格子の文言)**: ご指摘のとおり内部矛盾でした。正しくは **2 個**(かつ $x\leftrightarrow y$ を法として 1 軌道)です。**この指摘を追跡した結果、当該帯そのものが空であることが出ました**: $N\trianglelefteq B_3$ かつ $c\in N$ なら $N_{F_2}$ は $\Gamma$-安定ゆえ $\alpha(N_{F_2})\subseteq\mathbf Z^2$ も $\Gamma$-安定です。$\mathbf Z^2$ を $\mathbf Z[\omega]$($\bar x\mapsto1,\bar y\mapsto\omega$)と見ると $\tau$ = $\omega$ 倍、$\theta$ = $\omega\cdot$共役なので、**$\Gamma$-安定部分格子 = 共役安定イデアル $(n)(1-\omega)^a$、指数 $n^23^a$**。⟹ **指数 2 の $\Gamma$-安定部分格子は存在しません。** ⟹ $\lvert V\rvert=4$($\lvert PB_3/N\rvert=2000$)は $\lvert W\rvert=\lvert V/W\rvert=2$ を強制されるので**空**(系 THETA-2000)、$p=3$ の $\lvert V\rvert=9$(4500)も同様(系 THETA-4500)。**生存帯の下限は $p=2$ で 4,000、$p=3$ で 13,500 に上がりました。** ここも監査をお願いします(とくに $\alpha(N_{F_2})$ の $\Gamma$-安定性が $c\in N$ に依存する点)。

**再検討の請求(中心性判定)**: $V\subseteq Z(G_{20})$ は**真である**と当方は判断しています。根拠:

1. **$\theta,\tau$ は外部自己同型**($B_3/PB_3\cong S_3$ 由来)であり、$P=PB_3/N$ の内部共役ではありません。「$\Gamma$ が三座標を置換する」は $V^\Gamma\subsetneq V$ を与えますが、$Z(P)$ とは別の量です。補題 SURJ-CENT が要求するのは $V\subseteq Z(P)$($P=PB_3/N$)だけで、$\widehat P=B_3/N$ の中心ではありません((SURJ) の主張 $\langle\bar x,\widetilde f^{-1}\bar y\widetilde f\rangle=P$ も $P$ の中で閉じています)。
2. **証明 A**: 正典 (3.1) の $\psi_{20}$ は**直積** $D_{20}^3$ への準同型で、$m$ 偶ゆえ $Z(D_{20})=\langle r^{10}\rangle$。したがって $V=\langle r^{10}\rangle^3=Z(D_{20}^{\,3})$ であり、$V\subseteq G_{20}\le D_{20}^3$ から $V\subseteq Z(G_{20})$。
3. **証明 B**(周囲群を使わない): $V$ はアーベルな $A_{20}=\langle r^2\rangle^3$ の 2-捻れ部分。$G_{20}$ の $A_{20}$ 上の共役作用は各座標で $\pm1$ の符号対角なので、$-5\equiv5\ (10)$ より **$V$ 上では自明**。これは追補 B が W6B-4 で警告した「$p=2$ で (4.7) の符号が消える」現象そのものです。
4. **機械(python 単系統・悉皆)**: $G_{20}$ を $D_{20}^3$ の中で明示構成し、$\lvert G_{20}\rvert=4000$、**$Z(G_{20})=V$(位数 8・ちょうど一致)**、$\lvert[G_{20},G_{20}]\rvert=250$、$\lvert W\rvert=2$、witness $(6,4,0)\in[G_{20},G_{20}]$ を確認しました(`scratchpad/w6_vcen_check.py`・SHA-256 `6f8b1f04…3fcd`・17 項 FAILS=0)。
5. ★ **同じ走行で $\lvert V^\theta\rvert=4$ も確認しています**(D15)。**ご指摘の「固定されるのは対角線」という計算自体は正しく**、当方の機械値とも一致します。**両立する 2 つの事実**(D17)であり、食い違っているのは対象($Z(G_{20})$ か $V^\Gamma$ か)だけだと当方は見ています。

⟹ したがって **K20 への ROOF-KILL 適用は維持**し、「K20-LIFT/Thm 4.3 と独立な第二の紙証明」も維持したい、というのが当方の請求です。**ただし v1 §4.3 の当該行が「$r^{10}$ は各 $D_{20}$ で中心」で止まっており、そこから $Z(G_{20})$ への一行を省略していたことは当方の欠陥です**(ご指摘で判明しました)。erratum で上の 2 証明に差し替えました。`cross-checked` を名乗らない点は v1 のままです。

**もしなお $V\not\subseteq Z(G_{20})$ と判断される場合**は、$Z(G_{20})=V$ という上の悉皆計算(または $\psi_{20}$ が $D_{20}^3$ の**直積**へ写るという読み)のどこが誤りかをご指摘ください。当方はそこを一次容疑として再検算します。

> ### 【収載原稿ここまで】

---

## 8. 司令塔への申し送り

1. ★★★ **生存帯の下限が上がった**($p=2$: 2000 → **4000**、$p=3$: 4500 → **13500**)。⟹ **BOTTOM-UP v2 の宇宙 U-2/U-3 を再凍結**する必要がある(別紙 §6)。**cap 8000 の下では $p=3$ の候補はゼロ**。
2. ★★ **$\lvert V\rvert=8$(4000)の帯では $\lvert W\rvert=2$・$\lvert V/W\rvert=4$・$\alpha(N_{F_2})=4\mathbf Z^2$ が強制**される。⟹ 掘る対象の形がほぼ決まる(別紙で加群まで一意に決まることを示す)。
3. ★ 系 THETA-2000 は **$C_4$ 型核も同時に消す** ⟹【BU-GAP-1】(非初等アーベル核)の一部が閉じた。**ただし「除外帯が空」と読ませない**(S-BU-6 は不変 — 消えたのは $\lvert V\rvert=4$ の段だけ)。
4. ★ **`docs/地図.md` に 1000/2000 帯の記述があれば更新が要る**(本書は地図を書き換えていない)。
5. ⚠ **本書は Sol 未監査**。§2 の新結果 4 本(LAT-Γ / NC-2′ / THETA-2000 / THETA-4500)は**便 103 の監査対象**に載せられたい。
