# sat_l1 **v2** — Sol 便 90(F90-1)の修理 3 点 + SAT-T1 の $t=0$ 補完。**定理 CENT 正式採択(裁定 266)**

> ## ⚠ 本稿の現行状態(2026-07-31・便 91 検収後)
> - **定理 CENT は正式採択**(Sol 便 91 F91-1.5・**裁定 266**)。系 CENT-ORD・系 EPS($\varepsilon=(-1)^{p+s}$)も採択。壁族四窓の核等式は確定(F91-7.3)。
> - **erratum F91-1.2 を定理 ID に pin**: 旧 §2(XI-INJ′ の補筆)は **FAIL** — 導出すべき生成等式を前件に置いていた。**§2 は正しい一段へ置換済**(旧文は**付録 A** に退避・削除していない)。
> - $\lvert\ker\widetilde\chi\rvert_\ell=\ell^{r-p}$ は**「標準域」を明示した範囲でのみ**採択(階乗因子から追加の $\ell$-因子が出ない範囲。一般の奇数部分全体を述べる式ではない)。
> - **§4 は「補題 SAT-T1 の $t=0$」の修理であり、T3-N0 の計数公式の $t=0$ 穴とは別物**(F91-1.4)。後者は **未解決 → 追補ノート `t3_quasi_purecycle_rigidity_v1_addendum_t0.md` で閉じた**(§4.2 参照)。**CENT の採択に T3-N0 は便乗しない。**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31(**§2 置換・§4 分離は同日の便 91 検収反映**)
- 位置づけ: **`docs/notes/sat_l1_v1.md` の修理版・非上書き**(v1 は不変)。本稿は**差分のみ**を正本化する。v1 の本文・表・probe 記録はすべて有効で、下記 4 点だけが v2 で置き換わる。
- 入力: `sol/sol_reply_90_math17.md`(F90-1 全節・F90-2.3)/ `sol/sol_reply_91_math18.md` F91-1(**§2 置換の根拠**)/ `sol/裁定_266_便91検収.md`。
- 状態: **CENT = 定理**(便 91 で正式採択)。**CENT-ORD と $\varepsilon=(-1)^{p+s}$ は系へ昇格**。

---

## 0. 格の更新(v1 → v2)

| 主張 | v1 の格 | **v2(現在)** |
|---|---|---|
| **CENT**: $\ker\widetilde\chi\cong C_{S_n}(w)$ | candidate(11 窓 measured) | **定理・正式採択**(便 91 F91-1.5 / 裁定 266。**erratum F91-1.2 を pin** = §2 置換版の補題 GEN を束縛)。証明鎖は XI-C + XI-INJ + SURV+(`t3_quasi_purecycle_rigidity_v1.md` §5–§6)で、**剛性 $N$ にも T3-N0 にも依存しない** |
| **CENT-ORD**(閉じた位数公式・奇部 $\ell^{r-p}$) | candidate | **系**(位数公式は無条件・**奇部の閉形は標準域のみ**・§5) |
| $\varepsilon=(-1)^{p+s}$($\mathrm{sgn}(w)=\mathrm{sgn}(a_1)$) | candidate | **系** |
| 補題 AUT-E | — | **PASS**($\varepsilon=1$ 側も・Sol 判定) |
| XI-INJ | — | **PASS**。前件 $C_{S_n}(\langle g,h\rangle)=1$ は **補題 GEN(§2 置換版)**が供給(旧補筆は F91-1.2 で FAIL) |
| **補題 SAT-T1**(transporter 非空) | 定理(ただし $t=0$ の場合分けが不明瞭) | **定理**($t=0$ を明示的に補完・§4.1・F91-1.4 で PASS) |
| **定理 T3-N0**(種数 0 の $N$ 計数公式) | (別稿) | **$t=0$ の穴は追補で閉鎖**(`t3_quasi_purecycle_rigidity_v1_addendum_t0.md`)。**本稿 §4 とは別物**・CENT は本公式に依存しない |
| 定理 SURV / SURV+ | 定理 | **不変**(修理 3 の座標補正後も結論は同一・§3) |
| 壁 P-WALL-2 の一意性系 | — | **無傷**(Sol 判定・T3-N0 の補完に依存しない) |

---

## 1. 修理 1 — $F_{\rm judge}$ と $q=F_{\rm judge}^{-1}$ の分離(XI-C の座標明記)

v1 は $f$ の向きを本文冒頭の注記(2026-07-31 追記)でしか断っていなかった。**v2 では XI-C を座標込みで書く**:

> ### 規約 XI-C(座標の明記)【正本】
> 二つの座標を**記号で区別する**:
> $$f_{\rm hand}\ (\text{本稿 v1 の }f;\ \bar y^{\,f}=f^{-1}\bar yf\ \text{右共役}),\qquad
> F_{\rm judge}\ (\text{judge の }f;\ \text{paper 語 }f^{-1}\bar yf=\text{GAP }f\,\bar y\,f^{-1}\ \text{左共役}),$$
> $$\boxed{\ F_{\rm judge}=q,\qquad q:=f_{\rm hand}^{-1}\ }$$
> 両者は**同一の写像 $T_{0,f}$ を与える**(`hexagon_orientation_ruling_v1.md` §1.4)。$\Xi$ の値 $\alpha$ も同一。
> **定理 SURV は judge 座標で**
> $$F_{\rm judge}(z)\ :=\ a_1\cdot\bigl(a_1^{\,z}\bigr)\qquad\bigl(=f_{\rm hand}(z)^{-1},\ f_{\rm hand}(z)=(a_1^{\,z})a_1\bigr).$$
> **証明書には必ず `f_orientation: "judge" | "handwritten"` を立てる**(混用禁止)。

---

## 2. 修理 2【**置換**・erratum F91-1.2】— 生成条件は**仮定ではなく導出**である

> **本節は差し替えである。** 旧 §2(便 90 への私の補筆)は Sol 便 91 **F91-1.2 で FAIL**:
> 証明すべき包含 $A_n\le\langle g,h\rangle$ を、**未導出の生成等式 $\langle g,h\rangle=\langle a_1,b_1\rangle$ を前件に置く**ことで済ませていた(核の元がその等式を満たすことこそが示すべき内容だった)。
> **旧文は削除せず 付録 A に退避**。以下が正しい一段(Sol 供給の骨格を、本稿の座標・記号で完全に書き下し、機械検算を付けたもの)。

### 2.0 座標の但し書き(⚠ 記号衝突を先に潰す)

F91-1.2 は shadow を $q$ と書き「hand 座標 $q$」と述べるが、**そこでの $q$ は §1 の $q:=f_{\rm hand}^{-1}=F_{\rm judge}$ ではなく、v1 の $f$($=f_{\rm hand}$)そのもの**である(定理 RED の全単射 $f\leftrightarrow(g,h)=(fa_1,\,fb_1^{-1})$ が hand 座標で書かれているため)。以下では混同を避け、**hand 座標の shadow を $f$ と書く**。座標非依存に述べたいときは
$$Y\ :=\ T_{0,f}(\bar y)\ =\ \bar y^{\,f}\ =\ f^{-1}\bar yf\ =\ F_{\rm judge}\,\bar y\,F_{\rm judge}^{-1}$$
を使う(**両座標で同一の元**・§1)。共役は右作用 $u^{g}:=g^{-1}ug$、したがって $u^{gh}=(u^{g})^{h}$。v1 §1 より
$$\bar x=w^2,\quad \bar y=v^2,\quad v=w^{a_1}\,(=a_1wa_1),\quad \bar y=\bar x^{\,a_1},\quad P=\langle\bar x,\bar y\rangle=A_n,\quad \mathrm{sgn}(b_1)=+1 .$$

### 2.1 補題 GEN【proof・erratum F91-1.2 の正本】

> ### 補題 GEN(生成条件の**導出**)
> $f\in\ker\widetilde\chi$($m=0$ 層)とし、定理 RED の対応で $g:=fa_1$、$h:=fb_1^{-1}$ とおく($g^2=1$、$h^3=1$、$gh=v$)。このとき
> $$\boxed{\ A_n\ \le\ \langle g,h\rangle\ }\qquad\text{したがって}\qquad \boxed{\ C_{S_n}\bigl(\langle g,h\rangle\bigr)=1\ }\quad(n\ge5),$$
> さらに $\langle g,h\rangle=\langle a_1,b_1\rangle$(**結論**であって仮定ではない)。
>
> **証明.**
> **(1) 二つの恒等式。** $v=w^{a_1}$ より
> $$\bar x^{\,a_1}=(w^2)^{a_1}=(w^{a_1})^2=v^2=(gh)^2 .$$
> $g^2=1$ と $gh=v$ から $hg=g^{-1}(gh)g=v^{\,g}$、ゆえに($\bar y=v^2$、$fa_1=g$ を使って)
> $$Y^{a_1}=\bigl(\bar y^{\,f}\bigr)^{a_1}=\bar y^{\,fa_1}=\bar y^{\,g}=(v^2)^{\,g}=(v^{\,g})^2=(hg)^2 .$$
> **(2) shadow の全射条件を投入する。** $f$ は shadow だから($m=0$ ゆえ $u=2m+1=1$;judge の受理条件 4)
> $$\langle\bar x,\,Y\rangle=P=A_n .$$
> $A_n\trianglelefteq S_n$ ゆえ $A_n^{\,a_1}=A_n$。よって
> $$A_n=A_n^{\,a_1}=\langle\bar x,Y\rangle^{a_1}=\bigl\langle \bar x^{\,a_1},\,Y^{a_1}\bigr\rangle=\bigl\langle (gh)^2,\ (hg)^2\bigr\rangle\ \le\ \langle g,h\rangle .$$
> **(3) 中心化群。** $C_{S_n}(A_n)$ は正規部分群の中心化群ゆえ $S_n$ に正規で、$C_{S_n}(A_n)\cap A_n=Z(A_n)=1$($n\ge4$)。$n\ge5$ では $S_n$ の正規部分群は $1,A_n,S_n$ のみだから $C_{S_n}(A_n)=1$。ゆえに $C_{S_n}(\langle g,h\rangle)\le C_{S_n}(A_n)=1$。
> **(4) 生成等式。** $f\in P=A_n$ に注意する。$\langle a_1,b_1\rangle=A_n$ のときは $g,h\in A_n$ ゆえ $\langle g,h\rangle\le A_n$、(2) と併せて $\langle g,h\rangle=A_n=\langle a_1,b_1\rangle$。$\langle a_1,b_1\rangle=S_n$ のときは $\mathrm{sgn}(b_1)=+1$ ゆえ $\mathrm{sgn}(a_1)=-1$、$f$ が偶だから $\mathrm{sgn}(g)=-1$ で、(2) と併せて $\langle g,h\rangle=S_n=\langle a_1,b_1\rangle$。∎

**旧稿との差はここだけである**: 旧稿は (4) を**前件**に置いて (3) を導いた。正しい向きは **(2)(shadow 自身の全射条件)$\Rightarrow$ (2 の結論)$\Rightarrow$ (3)(4)** である。使ってよい前件は「$f$ が shadow であること」だけで、$(g,h)$ の生成は**そこから出る**。

### 2.2 効き所(この一段が支える箇所)

| # | 使う場所 | 何が要るか |
|---|---|---|
| **①** | **定理 XI-INJ**(`t3_quasi_purecycle_rigidity_v1.md` §6)の前件 $C_{S_n}(\langle g,h\rangle)=1$ | 核から来る**すべての** $(g,h)$ で成立すること ⟹ 系 XI-INJ′($\Xi$ 単射)⟹ **定理 CENT の ② 段** |
| ② | v1 §6.2 定理 SAT-RIG (b) の**自由性** | $C_{S_n}(v)$ の $\mathcal F^{\rm gen}(v)$ 上の作用の安定化群 $=C_{S_n}(\langle g,h\rangle)=1$ |
| ③ | v1 §5 定理 SURV (iv) の単射性 | v1 は $C(\langle a_1,b_1\rangle)=1$ を直接使っており**無傷**(本補題に依存しない) |

> **⚠ ② の射程**(T-18 と `t3_...` §4 の反証を継承): 定理 SAT-RIG の **(a)(c)(d) は偽**(settled 節が落ちているため $\ker\widetilde\chi\leftrightarrow\mathcal F(v)$ が全単射でない)。本補題が救うのは (b) の自由性だけで、正しい会計は
> $$\lvert\mathcal F^{\rm gen}(v)\rvert=\lvert C_{S_n}(v)\rvert\cdot N_{\rm gen},\qquad
> \lvert\ker\widetilde\chi\rvert=\lvert C_{S_n}(w)\rvert\cdot N_{\rm shadow},\qquad N_{\rm shadow}=1\ (\text{定理 CENT の帰結}) .$$
> **$N_{\rm gen}=1$(剛性)は CENT に不要**であった(`t3_...` §4)。

### 2.3 副産物と、閉じていないもの

- **副産物**: 補題 GEN は「shadow $\Rightarrow$ 分解の生成等式」を与える。これは **【GAP-S1】の逆向き**である。
- **【GAP-S1】は未閉のまま**: 必要なのは「$\langle g,h\rangle=\langle a_1,b_1\rangle\Rightarrow\langle\bar x,\bar y^{f}\rangle=P$」(定理 SURV が $f_z$ を shadow と呼ぶために要る)。$\ell$ 素数 $\wedge\ t\ge3$ では補題 HOLE(`tmax_budget_and_holes_v1` §2.1)により**「$\langle\bar x,\bar y^f\rangle$ が推移的か」まで縮む**が、一般には未証明(v2 §7)。
- **部分的に閉じた**(本稿の新規・3 行):

> ### 系 GEN-2(奇位数窓では GAP-S1 が閉じる)【proof】
> $n\ge5$、$g^2=1$、$h^3=1$、$v:=gh$、$\langle g,h\rangle\supseteq A_n$ とする。**$\mathrm{ord}(v)$(= $\mathrm{ord}(w)$)が奇**ならば
> $$H:=\bigl\langle v^2,\ (v^2)^{\,g}\bigr\rangle\ \supseteq\ A_n,\qquad\text{すなわち}\qquad \langle\bar x,\bar y^{\,f}\rangle=P .$$
> **証明.** $\mathrm{ord}(v)$ 奇 ⟹ $v\in\langle v^2\rangle\le H$。$g^2=1$ より $H^{\,g}=\langle (v^2)^g,v^2\rangle=H$ ゆえ $K:=\langle H,g\rangle=H\cup Hg$ で $H\trianglelefteq K$、$[K:H]\le2$。$h=gv\in K$ だから $K\supseteq\langle g,h\rangle\supseteq A_n$。$H\trianglelefteq K$ より $H\cap A_n\trianglelefteq A_n$ で、$A_n$ は単純($n\ge5$)。$H\cap A_n=1$ なら $\lvert H\rvert\le[K:A_n]\le2$ で $\lvert K\rvert\le4$ となり矛盾。ゆえに $A_n\le H$。最後に §2.1 (1) の恒等式で $\langle\bar x,\bar y^f\rangle^{a_1}=H$、$A_n$ の正規性と $\bar x,\bar y^f\in A_n$ から $\langle\bar x,\bar y^f\rangle=A_n=P$。∎
> **射程**: $\mathrm{ord}(w)$ 奇 $\iff w$ に偶長巡回がない $\iff p=s=0$。この範囲に入るのは **壁 P-WALL-2($w_0=(19,1^5)$)・W-CENT-B($w_0=(9,9)$)・`tmax_budget_and_holes_v1` の梯子族($w_0=(\ell,1^t)$)・W-E-A10-9t1($v=(9,1)$)**。
> **射程外**($p$ または $s$ が正): W-E-A11-9t2($v=(9,2)$)・A12-9t3・A13-9t4 のような $2$-巡回をもつ窓、r=4 の $w=(10,10)$/$(10,5,5)$、$v=(10)$ 窓。ここでは GAP-S1 は依然 machine のみ(§2.4 で 4 窓・反例 0)。

### 2.4 機械検算(本稿・独立実装)

`scratchpad/gen_lemma_check.py`(SHA-256 `c7053e8b…b045b1`・Python 3 + sympy 1.14.0 の Schreier–Sims・**GAP パイプラインを一切 import しない独立実装**)。各窓で $v$ の全 $(2,3)$-分解 $(g,h)$($h:=gv$、$h^3=1$)を悉皆列挙し、
**gen** $=[\langle g,h\rangle\supseteq A_n]$、**surj** $=[\langle v^2,(v^2)^g\rangle\supseteq A_n]$(= 全射条件を $a_1$ で共役したもの)を両方判定した。

| 窓 | $n$ | $v$ の型 | $\mathrm{ord}(v)$ | 分解総数 | gen | surj | **gen $\wedge\lnot$surj**(GAP-S1 反例) | **surj $\wedge\lnot$gen**(補題 GEN 反例) |
|---|---|---|---|---|---|---|---|---|
| W-E-A10-9t1 | 10 | $(9,1)$ | 9(奇) | **90** | 54 | 54 | **0** | **0** |
| W-E-A10-5x2t0 | 10 | $(10)$ | 10(偶) | **65** | 50 | 50 | **0** | **0** |
| W-E-A11-9t2 | 11 | $(9,2)$ | 18(偶) | 90 | 54 | 54 | **0** | **0** |
| aux | 9 | $(7,2)$ | 14(偶) | 28 | 14 | 14 | **0** | **0** |
| W-E-A12-9t3 | 12 | $(9,2,1)$ | 18(偶) | 270 | 54 | 54 | **0** | **0** |

- **既存悉皆値との一致**: $(65,50)$ は `hexagon_orientation_ruling_v1.md` §1.3(judge 実物 $\mathcal J$・手書き $\mathcal M$ の両方・$A_{10}$ 全 $1.8\times10^6$ 走査)と**逐語一致**;$(90,54)$ と $(65,50)$ は `t3_quasi_purecycle_rigidity_v1.md` §4 の表(`t3_f_settled.g`・`t3_g_xiinj.g`)と**逐語一致**。**別実装・別言語(Python+sympy)での再現**である。
- **補題 GEN の反例 0**(全窓)。**GAP-S1 の反例も 0** — ただしこれは 5 窓の measured であって証明ではない(系 GEN-2 が紙で覆うのは 1 行目のみ)。
- 格: **単系統(本稿の独立器)+ 既存悉皆値との一致**。cross-checked と呼んでよいのは分解総数 $90/65$ の行だけで、gen/surj の内訳は本稿が初出。**Lean verified ではない。**

---

## 3. 修理 3 — $\Xi$ は現実装規約では**反準同型**($\Phi=\Xi^{-1}$ による補正)

**事実**(`strike-r4` の `19_xi_hom_right = true`・`19_xi_hom_left = false`、`norm_embedding` 9 窓も同じ):
$$\Xi\bigl([m_1,f_1]\circ[m_2,f_2]\bigr)=\Xi([m_2,f_2])\cdot\Xi([m_1,f_1]).$$

> ### 訂正 XI-A(v1 §6.1 の言い回しの是正)
> v1 §6.1 は「$z\mapsto\alpha_z$ は準同型(機械確認)」と書いた。**これは正しい**($\alpha_z=z^{a_1}$ で、$z\mapsto z^{a_1}$ は準同型)。誤っていたのは、そこから **$\Xi$ 自体を準同型のように読ませた**点である。正しくは:
> $$\Xi:\ \ker\widetilde\chi\longrightarrow \mathrm{Stab}(\bar x)\quad\text{は\textbf{反}準同型},\qquad
> \boxed{\ \Phi:=\iota\circ\Xi\ (\iota:g\mapsto g^{-1})\ \text{が準同型}\ }$$
> で、$\ker\Phi=\ker\Xi$、$\mathrm{im}\,\Phi=\mathrm{im}\,\Xi$(**部分群としては同一**)。
> **したがって定理 SURV+ の結論**
> $$C_{S_n}(w)\ \subseteq\ \Xi(\ker\widetilde\chi)\ \subseteq\ C_{S_n}(\bar x)$$
> **は不変である**(反準同型の像も部分群であり、$\iota$ で写しても同じ集合)。同様に **定理 CENT-0・壁 P-WALL-2 の非可解性・W-CENT-B の 162 もすべて不変**($\ker\widetilde\chi$ が非可解群を**商にもつ**という言い方は、反準同型でも成立する — 像が部分群だから)。
> **v1 の該当箇所の読み替え**: §6.1 の「$z\mapsto\alpha_z$ は準同型・反準同型?」の欄、§5 系 SURV-2、§10.5.1 定理 SURV+ の全体で、$\Xi$ を**「反準同型 $\Xi$、その補正 $\Phi=\iota\circ\Xi$」**と読む。**位数・構造・包含の主張はすべてそのまま。**

---

## 4. $t=0$ をめぐる**二つの別問題**(F91-1.4 の分離)

> **⚠ 便 90 の指摘と本節の関係**(便 91 F91-1.4 で明示された): 「$t=0$」と呼ばれていた穴は **2 つあり、別物**である。
> - **(A) 補題 SAT-T1(transporter の非空性)の $t=0$** — 本稿 §4.1 が閉じた。**F91-1.4 で PASS**。
> - **(B) 定理 T3-N0(種数 0 の $N$ の計数公式)の $t=0$** — 母関数証明が「ループ付き黒葉で根付け、最後に $t$ で割る」ため $t>0$ しか扱っていなかった。**本稿 §4.1 はこの穴に触れない**。→ §4.2。

### 4.1 (A) 補題 SAT-T1 の $t=0$ 補完【PASS(F91-1.4)】

v1 §4(補題 SAT-T1)は $r=1,t\le1$ を「残るケース」として一括で扱い、**$t=0$ の扱いが明示的でなかった**。全場合を書き下す。

> ### 補題 SAT-T1【定理・完全場合分け】
> $\bar y$ の型を $(\ell^{\,r},1^{\,t})$($\ell$ 奇、$n=\ell r+t$)とする。$\alpha\in S_n$ に対し
> $$\mathcal T_\alpha\ne\varnothing\iff C_{S_n}(\bar y)\,\alpha\cap A_n\ne\varnothing .$$
> $C:=C_{S_n}(\bar y)=(C_\ell\wr S_r)\times S_t$ の**奇置換の有無**で場合分けする:
>
> | 場合 | $C$ は奇置換を含むか | 結論 |
> |---|---|---|
> | **$r\ge2$**(**$t=0$ を含む**) | **含む**: 2 つの $\ell$-ブロックの互換は $\ell$ 個の互換の積で、$\ell$ 奇ゆえ**奇** | $\forall\alpha\in S_n$ で $\mathcal T_\alpha\ne\varnothing$ |
> | **$t\ge2$**(任意の $r$) | **含む**: $S_t$ の互換は奇 | 同上 |
> | **$r=1,\ t=1$** | 含まない($C=C_\ell\times S_1$、$\ell$-巡回は偶) | $\mathcal T_\alpha\ne\varnothing\iff\alpha$ 偶。ただし $H=C_{S_n}(\bar x)=C_\ell\le A_n$ ゆえ**全 $\alpha\in H$ は偶** ⟹ 成立 |
> | **$r=1,\ t=0$**(**補完箇所**) | 含まない($C=C_\ell=\langle\bar y\rangle$、$n=\ell$) | 同上: $H=C_{S_\ell}(\bar x)=\langle\bar x\rangle=C_\ell\le A_\ell$($\ell$ 奇ゆえ $\ell$-巡回は偶)⟹ **全 $\alpha\in H$ は偶** ⟹ $\mathcal T_\alpha\ne\varnothing$ |
>
> **⟹ 本族の全窓・全 $\alpha\in H$ で $\mathcal T_\alpha\ne\varnothing$。**($t=0$ は $r\ge2$ か $r=1$ かで上の 1 行目/4 行目に落ちる。)
> **証明.** $\bar y^{\,f}=\bar y^{\,\alpha}\iff f\in C\alpha$。剰余類 $C\alpha$ が $A_n$ と交わるのは、$\alpha$ が偶であるか $C\not\le A_n$ のとき、かつそのときに限る。各場合の $C$ の奇置換の有無は上表のとおり。∎

**壁 P-WALL-2($r=1,t=5$)への影響**: $t=5\ge2$ ゆえ 2 行目に落ち、**補完箇所とは無関係**。Sol の「壁の一意性系は無傷」と一致。

### 4.2 (B) 定理 T3-N0 の $t=0$ 穴 — **本節では閉じない**(所在の明示)

便 90/91 の T3-N0 blocker は**計数公式側**の穴である: `t3_quasi_purecycle_rigidity_v1.md` §2.2 の母関数証明は平面木を「ループ付き黒葉」で根付け、最後に $t$ で割るため、**$t=0$ では $0/0$ になって何も言えない**。§4.1 の四場合表はこの根付け・除算を一度も扱わないので、**この穴には触れていない**(F91-1.4 の指摘は正しい)。

- **閉鎖の場所**: `docs/notes/t3_quasi_purecycle_rigidity_v1_addendum_t0.md`(本日の追補)。**任意の葉で根付けて $m+1$ で割る**一様版に差し替え、$t=0$ を含む全域($m\ge2$)で同じ閉形を導いた。6 個の $t=0$ 行で独立ブルート照合済。
- **CENT との関係**: 定理 CENT の証明鎖(XI-C + XI-INJ + SURV+)は **T3-N0 の計数公式に一切依存しない**(F91-1.5)。したがって **CENT の採択に T3-N0 を便乗させない**という裁定 266 の縛りは、本稿の構成上も自動的に守られる。

---

## 5. 昇格した系(CENT が定理になったことの帰結)

> ### 系 CENT-ORD【系】
> $w=(2\ell)^p(\ell)^{r-2p}(2)^s(1)^{t-2s}$ のとき
> $$\lvert\ker\widetilde\chi\rvert=(2\ell)^p\,p!\cdot\ell^{\,r-2p}(r-2p)!\cdot2^s s!\cdot(t-2s)!$$
> は**無条件**(中心化群の位数公式そのもの)。奇部の閉形は**標準域に限る**:
> $$\boxed{\ \lvert\ker\widetilde\chi\rvert_\ell=\ell^{\,r-p}\quad\Longleftarrow\quad p<\ell,\ \ r-2p<\ell,\ \ s<\ell,\ \ t-2s<\ell\ }$$
> **(標準域の定義)** — 四つの階乗 $p!,(r-2p)!,s!,(t-2s)!$ のどれからも $\ell$ 因子が出ない範囲。**この範囲外では階乗側の $\ell$-部が加算されるので上式は一般には偽**であり、「一般の奇数部分全体を述べる式」として引用してはならない(裁定 266・F91-1.5)。

> ### 系 EPS【系】
> $$\mathrm{sgn}(w)=\mathrm{sgn}(a_1)=(-1)^{p+s}\quad\Longrightarrow\quad \varepsilon=0\iff p+s\ \text{偶},\qquad\varepsilon=1\iff p+s\ \text{奇}.$$

いずれも v1 §7.5.1 の内容で、CENT の定理化によりそのまま系となる(11/11 窓の照合表は v1 のまま有効)。

---

## 6. v1 で**変わらない**もの(確認)

- 定理 RED / 平行移動公式 / SAT-L1 の反証 / 非可換 $Z^1$ の枠組み(§2・§3)
- 定理 SURV(構成)・SURV+(閉じた式)・**定理 CENT-0**(§10.6.3)
- **壁 P-WALL-2**(n=24・$\Xi(\ker)=C_{19}\times S_5$ 非可解 ⟹ $\mathrm{GTSh}$ 非可解)
- **W-CENT-B**(n=18・162 vs PRUNE 18)
- 定理 TRI・$s=1$ トリックの撤回・計数機構(Frobenius + 巡回集合分割 Möbius)
- probe 1–13 の全出力(**ただし $f$ は $f_{\rm hand}$ 座標**・§1)

---

## 7. 残ギャップ(2026-07-31・便 91 検収後の現況)

- ~~**剛性 $N=1$**(CENT の $\subseteq$)~~ → **不要になった**。CENT は settled 節 + $\Xi$ 単射で閉じる(`t3_quasi_purecycle_rigidity_v1.md` §4–§6)。$N_{\rm gen}\ge2$ の窓でも CENT は成立する。
- **【GAP-S1】**「$\langle g,h\rangle=\langle a_1,b_1\rangle\Rightarrow\langle\bar x,\bar y^{f}\rangle=P$」の紙上証明。**逆向きは §2.1 補題 GEN で閉じた**。本向きは:
  - **$\mathrm{ord}(w)$ 奇($p=s=0$)では §2.3 系 GEN-2 で閉じた**(壁 P-WALL-2・W-CENT-B・梯子族 $w_0=(\ell,1^t)$ を含む)。
  - $\ell$ 素数 $\wedge\ t\ge3$ では補題 HOLE により「推移性」まで縮む。
  - **$p$ または $s$ が正の窓は未閉**(5 窓 machine で反例 0・§2.4)。
- **【GAP-T3-t0】は閉じた**(追補 `t3_quasi_purecycle_rigidity_v1_addendum_t0.md`)。§4.2。
- $m\ne0$ 層の一般公式(candidate・未検証)。
- $\ell=25,t=5$ の $T_{\rm trans}$(クラウド発注済)。

---

## 付録 A — 旧 §2(2026-07-31・**F91-1.2 で FAIL**・記録として保存)

> **⚠ 以下は誤りであり、§2 に置換された。** FAIL の理由: 補題の**前件**に $\langle g,h\rangle=\langle a_1,b_1\rangle$ を置いているが、これは核の元について**導出すべき内容**であって与えられた前件ではない(shadow の定義が直接与えるのは全射条件 $\langle\bar x,\bar y^f\rangle=P$ の方である)。削除せず、誤りの型(「示すべき包含を仮定に繰り上げる」)の実例として残す。

> ### ~~補題 XI-INJ′【proof・補筆版】~~(旧稿・無効)
> ~~生成条件つきの分解 $(g,h)$($\langle g,h\rangle=\langle a_1,b_1\rangle$)に対し~~
> $$C_{S_n}\bigl(\langle g,h\rangle\bigr)=1 .$$
> ~~**証明.** $\langle a_1,b_1\rangle\in\{A_n,S_n\}$ ゆえ **$A_n\le\langle g,h\rangle$**。$n\ge5$ で $A_n$ は $\{1,\dots,n\}$ 上**推移的**かつ点安定化群 $A_{n-1}$ は自己正規化的だから、$C_{S_n}(A_n)=Z(S_n)=1$($n\ge3$)。$C_{S_n}(\langle g,h\rangle)\subseteq C_{S_n}(A_n)=1$。∎~~
> ~~**⟹ $C_{S_n}(v)$ の $\mathcal F(v)$ への作用は自由**(v1 §6.2 (b))。**⟹ $\lvert\ker\widetilde\chi\rvert=\lvert C_{S_n}(v)\rvert\cdot N$**(v1 §6.2 (c))。~~

**旧稿のもう一つの瑕疵**(便 91 とは独立に、T-18 / `t3_...` §4 で判明済): 最後の一行 $\lvert\ker\widetilde\chi\rvert=\lvert C_{S_n}(v)\rvert\cdot N$ は **settled 節を落としているので偽**。正しい会計は §2.2 の枠に置いた。

**★ 自己教材**: 「$A_n\le\langle g,h\rangle$」を**結論**として要求されている場面で、それを**前件の言い換え**として書くと、証明は形式上通って見える。前件表に「窓の構成から与えられているもの」と「核の元だから満たすもの」を分けて書いていれば、この型は起票時に潰せた。
