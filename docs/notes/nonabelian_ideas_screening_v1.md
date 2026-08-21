# 発案札 deck 2(nonabelian)N-1 / N-2 の高速判定 — 短報

**状態札: 数学者判定・司令塔検分前・Sol 未監査**
判定: Claude 数学者 / 2026-08-18 / 委嘱 = 司令塔(2 枚のみ・短報)
格: paper candidate。機械計算ゼロ。封印 3 量・$u$ の値・$c$ の値・sealed $K^{(5)}$ に非接触。
NAME-COLLIDE(本書で確定させる三者): **$c$** = 正典の中心元 $(\sigma_1\sigma_2)^3$ / **$c_{\rm cx}$** = 複素共役 / **$\iota$** = 鏡映自己同型 $\sigma_i\mapsto\sigma_i^{-1}$ / **$\varepsilon$** = strand parity 指標 $B_4\to S_4\to\{\pm1\}$ / **coset sign** = $X\to\mathrm{Sym}(X/A)\cong S_3\to\{\pm1\}$。

| 札 | 裁定 |
|---|---|
| **N-1 CHAR-BUDGET** | **条件付き成立**。核の指標予算補題は成立(検算済み)。T-35 反模型の $B_4$ 転写不能は**独立に証明できた**(T33-L8 の言い換えではない)。さらに**予想を超える一般化**が取れた: $t=1$ かつ $\mathrm{Out}(S)$ 可換なら **coupling の軌道長 3 は原理的に生じない**($A_5$ も $PSL(2,8)$ も該当)。ただし第二叉(motion の内部化で無害)は**定式化が不正確かつ不要** |
| **N-2 MIRROR-ι** | **条件付き成立。(a) は札より強い形で成立、(b) も成立、(c) の「半減」評価は過大**。(a) 単に $\iota$ だけでなく **isolated 窓は $\widehat{GT}$-安定**、従って $A$ 全体・genuine 部分 $P$ 全体が $V_r$ に作用する(補題 MIR-1)。(b) $(c_{\rm cx},c_{\rm cx})\in A$ が coset $S_3$ の transposition に落ちることを T-37 のデータから直接検算 ⟹ $s$-方向の同定は正しい。(c) **循環は半減しない**: MIR-1 (iii) により「$X\setminus A$ の元が $V_r$ に作用する」$\iff$ genuine $\iff$ **B4-B** — 循環は outside 側に丸ごと残る。$\iota$ が供給する $s$-方向は固定入力 1 によりもともと自由だった部分。ただし NA 定式化への正の寄与は 3 つ実在(§2.4) |

---

## 1. N-1 CHAR-BUDGET

### 1.1 核の補題(5 行検算 — 成立)

**補題 CB(指標予算).** $B_4^{ab}=\mathbf Z$(生成元は任意の $\sigma_i$;生成元は全て共役)。従って **$B_4$ の任意の商 $G$ の可換化 $G^{ab}$ は巡回群**であり、任意の $n$ について
$$\mathrm{Hom}(G,C_n)\cong\mathrm{Hom}(G^{ab},C_n)\ \text{は位数}\ \gcd(|G^{ab}|,n)\ \text{の巡回群}$$
(($G^{ab}$ が無限巡回なら $\cong C_n$)。特に $|\mathrm{Hom}(G,C_2)|\le2$:非自明 $C_2$ 指標は高々 1 本($\varepsilon$ が生き残るときそれ)。∎

**系 CB-1(T-35 反模型は $B_4$ 図式として転写できない).** T-35 の全空間 $E$($Q=C_2^2$ 上の三つの $E_\alpha$ の fibre product・核 $A_5^3$)について:
$A_5^3$ は完全なので $A_5^3=[A_5^3,A_5^3]\le[E,E]$;一方 $E/A_5^3=Q$ 可換なので $[E,E]\le A_5^3$。よって $[E,E]=A_5^3$ かつ
$$E^{ab}\cong Q\cong C_2^2\ (\text{非巡回}).$$
同様に単独の $E_\alpha$ でも $E_\alpha/A_5\cong\{(\bar u,q):\bar u=\alpha(q)\}\cong Q\cong C_2^2$ ゆえ $E_\alpha^{ab}\cong C_2^2$。
CB より $E\not\cong B_4/K$、$E_\alpha\not\cong B_4/K$、$Q\not\cong B_4/H$。∎
⟹ **反模型の静的図式は $B_4$-商としては存在しない。** 発案係の「5 行で立つ見込み」は**正しい**。

### 1.2 予想を超える一般化(これが本命)

反模型の要は「$Q$ 上の非零 coupling が 3 本あり、それらが推移的に回されて stabilizer の指数が 3」である。$B_4$ 水準では:

**系 CB-2(軌道長 3 の原理的排除).** $H\le PB_4$ を $B_4$-normal、$N=H/K\cong S^t$ を非可換 chief factor、$Q:=B_4/H$、coupling を $\chi\in\mathrm{Hom}(Q,\mathrm{Out}(N))$ とする。**$t=1$ かつ $\mathrm{Out}(S)$ 可換**なら:
1. $\mathcal X:=\mathrm{Hom}(Q,\mathrm{Out}(S))$ は CB により**巡回群**(位数 $\le|\mathrm{Out}(S)|$)。
2. $\mathcal X$ 上の作用($\mathrm{Aut}(Q)$ の前合成・$\mathrm{Aut}(\mathrm{Out}(S))$ の後合成)はすべて $\mathcal X$ の**群自己同型**なので、作用群は $\mathrm{Aut}(\mathcal X)$ に落ちる。巡回群 $C_m$ 上の $\mathrm{Aut}(C_m)$-軌道の長さは位数 $d\mid m$ ごとに $\phi(d)$ の約数。
3. 従って軌道長 3 が生じるには $3\mid\phi(m)$、特に $m\ge7$ が必要。
⟹ **$\mathrm{Out}(S)=C_2$($A_5$):$m\le2$ ⟹ 不可能。$\mathrm{Out}(S)=C_3$($PSL(2,8)$):$m\le3$、$\phi(3)=2$、$3\nmid2$ ⟹ 不可能。** ∎

> **実質**: 発案係が狙った「反模型排除」は、**$t=1$ の範囲で、しかも実系の最有力候補($PSL(2,8)$・札 B-2)を含む形で成立する**。T-36 の T35-R1(「$\mathrm{Out}\supseteq C_3$ なら反模型は転写されない」)を補完し、**$\mathrm{Out}=C_3$ の場合には「転写されない」だけでなく「軌道 3 機構自体が起こり得ない」**まで言える。
> **射程外**: $t>1$ では $\mathrm{Out}(S^t)=\mathrm{Out}(S)\wr S_t$ が非可換で、$\chi$ の像が可換とは限らないため CB が効かない。⟹ **新 FC-8: 実系の最初の非可換 chief の $t$ は 1 か。**

### 1.3 第二叉(motion の内部化)— 却下

札は「段が $B_4$-正規なら $\alpha$ を回す motion は $S_4$ 共役 = 内部ゆえ残差同変で無害」とする。**定式化が不正確で、かつ不要。**
正しくは: $K,H$ が $B_4$-normal なら $B_4$ は $B_4/K$ に共役で作用し $N$ を保つので、**coupling $\chi$ は自動的に $B_4$-同変**である。$\mathrm{Out}(N)$ が可換なら同変性は $\chi\circ\theta_b=\chi$($\theta_b$ = $b$ の $Q$ への作用)を意味する。従って:
- $B_4$ の $\mathrm{Aut}(Q)$ 内の像が $\chi$ を動かすなら **$\chi=0$**(段は反模型型でない)。
- 像が $\chi$ を固定するなら、$\alpha$ を回す motion は $B_4$ 図式の**中に存在しない**。
⟹ 結論は「内部化して**無害**」ではなく「**そもそも存在しない**」。二択の形は札のとおりだが、枝の中身が違う。しかも CB-2 があれば $t=1$ では第二叉を経由せずに片付く。

### 1.4 T33-L8 との関係 — 独立(言い換えではない)

- **T33-L8**: GT の持ち上げ問題に $\mathrm{Aut}$ 持ち上げ段階が無い ⟹ 反模型は**圏違い**。形式についての主張。
- **CB-1/CB-2**: 反模型の**対象そのもの**が $B_4$-図式として存在しない($E^{ab}$ 非巡回)/ 軌道 3 が原理的に起きない。対象についての主張。
⟹ **独立な第二防壁**として成立。前件も機構も異なる。
なお **CB の計算自体**($\mathrm{Hom}(B_4,C_2)=C_2$)は T-36 §4.6(3) と同じ 1 行である。**新規なのはそれを coupling の軌道長へ適用する部分**(CB-2)であり、この点は発案係の寄与として記録する。

### 1.5 そのまま使える形

> **補題 CB / 系 CB-1 / 系 CB-2**(§1.1–1.2 の枠内の文言)。前件を明示: CB-2 は $t=1$ かつ $\mathrm{Out}(S)$ 可換。$Q=B_4/H$($PB_4/H$ ではない — $PB_4^{ab}=\mathbf Z^6$ なので $PB_4$ 水準では CB が効かない。実際 $\mathbf F_2^6$ は $S_4$-安定な階数 2 商($K_4$ の辺加群 → 頂点次数 → 2 次元既約)を持つので、$PB_4/H\cong C_2^2$ 自体は起こり得る。**$B_4$ 水準を使うことが本質**)。

---

## 2. N-2 MIRROR-ι

### 2.1 (a) $\iota$ の $V_r$ への作用は well-defined か — **YES、しかも札より強い**

**予備検算(3 行).** $\sigma_i\mapsto\sigma_i^{-1}$ は braid 関係式の両辺の逆元を取る操作に一致するので $B_4$ の自己準同型を定め、$\iota^2=\mathrm{id}$ より $\iota\in\mathrm{Aut}(B_4)$。$B_4\to S_4$ で $s_i\mapsto s_i^{-1}=s_i$ なので $\iota$ は $PB_4$ を保ち $S_4$ に自明に作用。$B_4^{ab}=\mathbf Z$ 上 $\iota=-1$ ゆえ **$\iota$ は外部自己同型**。$x_{12}=\sigma_1^2\mapsto x_{12}^{-1}$、一般に $x_{ij}\mapsto$($x_{ij}^{-1}$ の共役)ゆえ $PB_4^{ab}$ 上も $-1$。

**MIRROR-SHADOW の $B_4$ 移植(札の検証項目 (2))— 一行で閉じる.**
- **pentagon**: $(m,f)=(-1,1)$ で (2.20) は $\varphi_{234}(1)\varphi_{1,23,4}(1)\varphi_{123}(1)=\varphi_{1,2,34}(1)\varphi_{12,3,4}(1)$、すなわち $1=1$ で**恒等的に成立**。$f=1$ ゆえ pentagon は無条件。
- **hexagon 2 本と全射性**: $[(-1,1)]$ は**複素共役の GT 像**である(古典;in-house LEDGER L2513 と整合)。従って arithmetic、ゆえに genuine、ゆえに 2008 Cor 3.13 により**全ての窓で shadow**。個別の語計算は不要。
⟹ **札の「新規部分(pentagon 版)」は成立。** ただし「複素共役 $\mapsto(-1,1)$」という正規化は古典的前提として明示する(本書では再証明していない)。

**補題 MIR-1(一般化 — これが本命).** $H$ を isolated 窓とする。
1. 任意の $\hat g\in\widehat{GT}$ に対し $\hat g(H)=H$。
2. 従って $\widehat{GT}$ は $H$ に、よって $H^{ab}\otimes\mathbf F_3=V$、$\Phi_3(H)$、$H_{PB_3}$、$W$ に作用する。特に $A\le P:=\mathrm{im}(\widehat{GT}\to X)$ の全体が作用する。
3. 逆に、$x\in X$ が(shadow を経由して)$V$ に作用する自然な構成は genuine 元からしか得られない。従って「$X$ が $V$ に作用する」を仮定することは $P=X$、すなわち **B4-B を仮定すること**に等しい。
*証明.* 1. $\hat g$ は $\widehat{\mathrm{PaB}}^{\le4}$ の自己同型なので $T:=\pi_H\circ\hat g$ は $H$ を target とする shadow で、source は $\ker T^{PB_4}=\hat g^{-1}(H)$。genuine ⟹ charming(2008 Prop 2.20)なので $T\in GT^\heartsuit(H)$、$H$ isolated ⟹ settled ⟹ $\hat g^{-1}(H)=H$。2. 制限。3. 2 の構成は $\hat g$ の存在(= genuine 性)を使う。∎

> ⟹ **札の (a) は正しく、しかも $\iota$ 単独ではなく $A$ 全体・$P$ 全体について成立する。** 同時にこれは **T-36 の T33-L11 を否定せず、逆に精密化する**: 作用は genuine 部分にちょうど載っており、outside への延長は B4-B と同値。

### 2.2 (b) $s$-方向の同定は正しいか — **YES(T-37 のデータから直接検算)**

T-37 の記号で $q:X\twoheadrightarrow H\times_UH$、$A=q^{-1}(\Delta H)$、$N_{\rm Gal}=\mathrm{Gal}(D/K)\cong C_3=\langle\tau\rangle$。
剰余類 $(h_1,h_2)\Delta H$ は $h_1h_2^{-1}\in N_{\rm Gal}$ で決まるので $(H\times_UH)/\Delta H\leftrightarrow N_{\rm Gal}\cong C_3$。左作用は
$$(g_1,g_2):\ n\longmapsto{}^{g_1}n\cdot n_0,\qquad n_0:=g_1g_2^{-1}\in N_{\rm Gal},$$
すなわち $\mathrm{Aff}(C_3)\cong S_3$ への**アフィン**作用。**線形部が $-1$ の元が transposition に落ちる。**
複素共役 $c_{\rm cx}$ は $c_{\rm cx}\tau c_{\rm cx}^{-1}=\tau^{-1}$(T-37)ゆえ線形部 $-1$、対角元 $(c_{\rm cx},c_{\rm cx})$ は $n_0=1$ で $n\mapsto n^{-1}$ — **恒等剰余類を固定する transposition** ✓($A$ に属することと整合)。
⟹ **coset $S_3$ の $s$-生成元は複素共役で実現される。** その braid/GT 側の実体は $[(-1,1)]=\iota$。**札の中心的な同定は正しい。**

**ただし未閉の一点(札自身も (ii) で認めている)**: 「coset sign」と「T-29 §6 の $V$ 上の sign 加群」の**同定**は依然として未証明(T-30 §4 (4) の禁止した同一視)。$\iota$ が供給するのは**作用**であって同定ではない。

**三重 NAME-COLLIDE の一行確定**:
$$\iota\in\mathrm{Aut}(B_4)\ (\text{複素共役の GT 像}\,[(-1,1)]),\qquad \varepsilon:B_4\to S_4\to\{\pm1\}\ (\text{指標}),\qquad \text{coset sign}:X\to S_3\to\{\pm1\}.$$
$\iota$ と coset sign は複素共役を介して結びつく(§2.2 で検算)。$\varepsilon$ との関係は**未確定**。なお $V_r$ 上で $\varepsilon$-isotypic 分解($G_r$-加群の分解)と $\iota$-固有分解($\langle\iota\rangle$-加群の分解)は**別のスロット**であり、直交でも同一でもない — $\iota$ は $G_r=B_4/H_r$ に作用するので $V_r$ は $G_r\rtimes\langle\iota\rangle$-加群となり、$\iota$-固有空間は $C_{G_r}(\iota)$-安定であって $G_r$-安定とは限らない(**この点は札に無い注意**)。

### 2.3 (c) NA 定式化の下でまだ価値があるか — **あるが「半減」ではない**

**過大評価の訂正.** 札は「未構成問題が $S_3$ 作用から $C_3$ 作用へ半減」とする。MIR-1 (iii) により:
$$\text{$s$-方向(位数 2)}\subseteq A\ \text{ゆえ固定入力 1 で\textbf{もともと自由}},\qquad \text{$r$-方向(位数 3・outside)}\iff\text{genuine}\iff\text{B4-B}.$$
⟹ **難所は「半分」ではなく最初から全部 outside 側にあり、$\iota$ はそこに触れない。** 「半減」は成立しない。

**それでも実在する 3 つの寄与(NA 定式化への直接の効き).**
1. **残差系の $\iota$-同変性.** MIR-1 により $\iota$ は isolated 窓 $H,K$ を保ち、$\mathcal G_3=B_3/K_{PB_3}$、$\mathcal G_4=PB_4/K$、$W$、$N$ に作用する。$[(-1,1)]$ との合成は $\mathrm{ML}(H)$ の全単射なので、NA-1 の残差系全体が $\iota$-同変。⟹ (i) 探索空間を $\iota$-軌道で半減できる、(ii) **checker の独立整合性検査**(producer の出力の $\iota$-像も解であること)が無料で 1 本増える。
2. **$\kappa$ の第三候補としての $V_r^-$.** $\mathrm{char}\,\mathbf F_3\ne2$ かつ $\iota^2=1$ なので $V_r=V_r^+\oplus V_r^-$ は常に定義される正準分解。**T-36 §4.6(3) で私は「$\kappa$ の自然候補は $\varepsilon$ のみ」としたが、それは $G_r$ の 1 次元指標に限った探索であり、自己同型固有空間という供給源を見落としていた。発案係の指摘を受諾する。** ⟹ FC-7 に姉妹検査 **FC-7′($V_r$ の $\iota$-固有分解の次元と $\varepsilon$-isotypic との交叉)** を追加。
3. **D1 への制約 1 本.** $\iota(W)\le N^5$(T-38 の D1)は、$\iota$ が五 coface と可換なら $\iota$-安定になり、決定すべき部分群の候補が絞れる。**ただし「$\iota$ が coface と可換」は未検査** — $\iota$ は $\widehat{\mathrm{PaB}}$ の operad 自己同型から来ると期待されるが、本書では証明していない。⟹ **新 FC-9: $\iota\circ\varphi_j=\varphi_j\circ\iota$($j$ = 五 coface)か。**

**間接路の遺物か.** 否。$\kappa/\Theta$ 路線(T-35)には $X$-作用の一階部分が要り、そこは MIR-1 (iii) で B4-B と同値と判明したので**間接路は依然として詰んでいる**。しかし N-2 の 3 寄与はいずれも $X$-作用を経由せず NA 定式化に直接載る。⟹ **札は「間接路の遺物」ではなく、直接路の補助具として採用可。**

---

## 3. 新規の有限検査(T-38 の FC 表への追加)

| 番号 | 検査 | 由来 |
|---|---|---|
| **FC-8** | 実系の最初の非可換 $B_4$-chief factor の $t$ は 1 か($t=1$ なら CB-2 が発火) | N-1 §1.2 |
| **FC-9** | $\iota\circ\varphi_j=\varphi_j\circ\iota$($j$ = 五 coface)か | N-2 §2.3-3 |
| **FC-7′** | $V_r=V_r^+\oplus V_r^-$ の次元と $\varepsilon$-isotypic との交叉 | N-2 §2.3-2 |

---

## 4. 申告

- 本書の全結果は paper candidate。機械計算ゼロ。**cross-checked ではなく verified でもない。**
- 前提として使い、再証明していないもの: T-37(FC-1 閉鎖・paper-proof 格)、「複素共役の GT 像は $(-1,1)$」(古典・in-house LEDGER L2513 と整合)、T-33 §2 の固定入力。
- 未閉: 「coset sign」と「T-29 §6 の $V$ 上 sign 加群」の同定(T-30 §4 (4) の禁止事項・N-2 では埋まらない)。FC-8/9/7′。CB-2 の $t>1$ 射程。
- 禁止短路との照合: centerless/Schreier からの自動 lift・$K(5)$ 単連結性・strict deletion-kernel・ambient exponent-3 quotient・$A$ 正規性の仮定 — **いずれも使っていない**($A$ 非正規は T-37 のとおり)。
- **B4-B は宣言していない。**

---

## Erratum / 追補(2026-08-18・Sol T-39 監査を受けて。本文は凍結・以下は追記のみ)

出典: `ops/express/20260818_sol_fable_t39_audit.md`。4 項目すべてを独立に検算した結果を記す。

### E-1 【訂正・受諾】CB-2 の一般仮説は「$\mathrm{Out}(S)$ **可換**」ではなく「$\mathrm{Out}(S)$ **巡回**」

§1.2 系 CB-2 の前件を訂正する。私は「$Q^{ab}$ 巡回 ⟹ $\mathcal X=\mathrm{Hom}(Q,\mathrm{Out}(S))$ 巡回」と書いたが、これは $\mathrm{Out}(S)$ が可換なだけでは**偽**である。
*独立検算.* $Q^{ab}$ が位数 $m$ の巡回群のとき $\mathrm{Hom}(Q,A)\cong\mathrm{Hom}(C_m,A)\cong A[m]$($A$ の $m$-捻れ部分群)。$A=C_2^2$、$2\mid m$ なら $A[m]=C_2^2$ で**非巡回**。しかも $\mathrm{Aut}(C_2^2)\cong S_3$ は 3 個の非零元を**軌道長 3** で推移的に回す ⟹ 反例。**Sol の指摘は正しい。**
- **正しい前件**: $t=1$ かつ **$\mathrm{Out}(S)$ が巡回**。このとき $A[m]$ は巡回群の部分群ゆえ巡回で、§1.2 の $\phi(d)$ 論法がそのまま通る。
- **本命 2 例は無傷**: $\mathrm{Out}(A_5)=C_2$、$\mathrm{Out}(PSL(2,8))=C_3$ — ともに巡回。**CB-2 の結論($t=1$ で軌道長 3 は不可能)は両例で成立**。
- 反例が空虚でないこと: $\mathrm{Out}(A_6)=\mathrm{Out}(PSL(2,9))\cong C_2^2$ が実在する。
- **CB-1(反模型の $B_4$ 転写不能)は $\mathrm{Out}$ にも $t$ にも依存しないので無傷。**

### E-2 【FC-9 取り下げ】$\iota$ と五 coface の可換性は閉じている — 私の提起は過度に慎重だった

Sol T-39 §3: $\iota_n=T^{PB_n}_{-1,1}$ は $\mathrm{PaB}$ の **operad 自己同型**で、A.18 の五 coface は operadic insertion/cabling なので $\iota_4\circ\varphi_j=\varphi_j\circ\iota_3$ が定義から従う。
*確認.* 2008 p.3 が $\widehat{GT}=\mathrm{Aut}(\widehat{\mathrm{PaB}})$ を定義し、$[(-1,1)]$ は複素共役の像すなわち $\widehat{GT}$ の元(§2.1 で確認済み)。operad 自己同型は構造射(挿入)と可換 ⟹ 主張は定義から従う。有限窓への降下は本文の補題 MIR-1($\widehat{GT}$ が isolated 窓を保つ)で閉じる。
⟹ **§2.3-3 で立てた FC-9 は取り下げる。** $\iota(W)\le N^5$ の $\iota$-安定性は**無条件に使える** — producer 出力の $\iota$-像も解であるという **checker symmetry** として実装してよい(短報 §2.3-1 の寄与①はそのまま有効、前件が消えた)。

### E-3 【FC-8 → FC-8*】「$M$ 直下の最初の非可換 chief」は登録なしには未定義

Sol T-39 §4 を受諾。有限商 $U$ と $B_4$-chief 系列(または socle layer)を登録しない限り「最初」は一意でない。置換:
> **FC-8\***: OBS-NA に実際に使う**登録済み** $H/K$ について、$N=H/K\cong S^t$、$t$、factor-permutation 作用 $Q=B_4/H\to S_t$、coupling $Q\to\mathrm{Out}(S)^t\rtimes S_t$ を決定する。

**発案札 B-2 の見立ての訂正**: 「実系の最初の非可換 chief は $PSL(2,8)$」は誤り — $PSL(2,8)^4$ は $M$ **より上**の因子であり、$M$ 直下の chief をそれだけから答えてはならない(Sol T-39 §4)。最短の具体化候補は **4 本の strand deletion からの $A_5^4$ 像**を現 roof と joint 化する lane で、**$S=A_5$, $t=4$** が最有力の実例。
⟹ **この場合 CB-2 は発火しない**($t=1$ 枝の外)。CB-1 は $t$ 非依存なので生き残る。**実戦は OBS-NA / NA-5 側へ直行する**という Sol の判断を支持する。

### E-4 【新規・$t\ge2$ でも残る CB 型制約(CB-3)】

$t\ge2$ では $\mathrm{Out}(S^t)=\mathrm{Out}(S)\wr S_t$ が非可換で CB-2 は効かないが、**可換化を経由する制約は残る**。
**系 CB-3.** $\mathrm{Out}(S)=C_2$、$t\ge2$ とすると $\bigl(C_2\wr S_t\bigr)^{ab}\cong C_2\times C_2$(第 1 成分 = $C_2^t$ の総和、第 2 成分 = $S_t$ の符号)。CB により $Q^{ab}=(B_4/H)^{ab}$ は巡回なので、coupling $\chi:Q\to\mathrm{Out}(S^t)$ の $(C_2\wr S_t)^{ab}$ への像は**巡回**、すなわち $C_2^2$ の位数 $\le2$ の部分群に入る。
⟹ **「$C_2^t$ 側の総符号」と「factor-permutation $S_t$ 側の符号」は $Q$ 上で独立になれない**(一致するか、一方が自明)。
$S=A_5$、$t=4$ で**直ちに有限検査可能**な制約であり、FC-8\* の登録データが出た瞬間に走らせられる。⟹ **FC-8\*\* として登録を提案**。

### E-5 NA-5 の $A_5^4$ 段への適用可能性

$|A_5|=60=2^2\cdot3\cdot5$(3-part $=3$)、$|A_5^4|=60^4$(3-part $=3^4$)。
- **NA-5 はそのまま適用できる。** NA-5 は $\mathrm{ML}(H)$ の Sylow 3-部分群の生成系を持ち上げる補題であり、chief factor $N$ の構造に一切依存しない。
- $3\mid|A_5|$ ゆえ「係数が 3 と互いに素だから自動」型の短絡は**使えない**が、NA-5 は coprimality を使わない。
- $5\mid|A_5|$ により、correction domain $\Lambda$ に $|X|=2^2\cdot3^5$ に現れない素数 5 が入る。3-part 判定(T33-T2)には無害だが、friendly gate($2m'+1$ が $\bmod K_{\rm ord}$ で単元)には新しい素数 5 の条件が加わり得る ⟹ **$m$ 側補正(D4/D6)が非自明になる可能性**を記録する。
- MIR-1 と E-2 により、$A_5^4$ 段でも残差系は $\iota$-同変。探索半減と checker symmetry は使える。

### E-6 MIR-1 の格

Sol T-39 §2 で (i)(ii) PASS、(iii) は「shadow を経由するこの自然構成の範囲に限定して読む」と裁定。本文 §2.1 の (iii) はまさにその限定で書いてある(「自然な構成は genuine 元からしか得られない」)ので、**訂正不要・読みを確認した**。
