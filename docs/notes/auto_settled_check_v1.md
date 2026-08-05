# 検分 — 「shadow は自動的に settled か」(implementer の実測 100% の数学的検分)

**状態札: `candidate / paper-proof / 紙のみ(機械実行ゼロ)/ Sol 未監査 / Lean 検証ではない / 封印 3 量非接触・Im R 非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-05・**新設 v1**
- 委嘱: 司令塔(緊急検分)—「R3 実装係が isolated=FALSE の自然例を探索した結果、**c∈N かつ hexagon+SURJ を満たす候補は全ケースで settled=100%**。係の見立て『well-defined+SURJ の shadow は有限群の鳩の巣で自動 bijective ⟹ 自動 settled』を検分せよ」
- **入力正本**:
  - `docs/week1-定義ノート.md` §2(**Def 3.1 GT-pair / charming / Def 3.7 GT-shadow / Prop 3.2 $T_{m,f}$ / Prop 3.4 簡約 hexagon / Prop 3.6 全射性の同値 / Def 3.13 settled・isolated / Thm 3.10 groupoid / Prop 3.8 / Prop 3.14**)
  - `docs/notes/ihnec_v1.md` §6.6 注意 2・T-5・(SET) 行(**Def 3.13 の逐語**: 「$[m,f]\in\mathrm{GT}(N)$ is called **settled** if $\ker(T_{m,f})=N$ … $N$ is called **isolated** if every GT-shadow in $\mathrm{GT}(N)$ is settled」)
  - `docs/notes/k5_genuine_campaign_v1.md` **K5-8**(運用判定の逐語: 「各 shadow で $x\mapsto x^u$、$y\mapsto f^{-1}y^uf$ が $\mathrm{Aut}(PB_3/N)$ に延びるか」)・**S-6**
  - `docs/notes/w6_bottomup_design_v4.md` §5(ISO-GATE route 2 の R1〜R5・紙 bridge B-1/B-2)
- ⚠ **一次資料の非読申告**: 係の探索一覧(cert appendix)は**まだ存在しないため読んでいない**。本検分は**定義と正典命題のみ**から行った。⟹ 個々の探索ケースの正誤は判定していない(判定したのは**判定形の意味論**である)。
- **外部文献ゼロ。封印 3 量・$\mathrm{Im}\,R$ 非接触。機械実行ゼロ。**

---

## 0. 判定(先に 5 行)

| # | 委嘱事項 | 判定 |
|---|---|---|
| **①** | 運用判定(K5-8)と定義(Def 3.13)の同値性 | ★★ **同値である**(**定理 OP-SETTLED**・§2.3)。ただし前件は **(i) $c\in N$ (ii) $N\subseteq PB_3$ 有限指数正規 (iii) 当該 $[m,f]$ が GT-**shadow**(charming + 全射)**の 3 つ。**この 3 つのどれが欠けても同値は壊れる**(§4) |
| **②** | 鳩の巣論法の紙化 ⟹ 定理 AUTO-SETTLED | ⚠ **不成立**(そのままでは)。鳩の巣は**半分だけ正しい**: 「**降下(descent)+ 全射 ⟹ 全単射 ⟹ settled**」は成立する(**補題 PIGEON**)。しかし **descent($T_{m,f}(N)=1$)は hexagon からも生成性からも出ない** — これが独立の条件であり、非 settled はまさにここで生じる(§3.1) |
| **③** ★★★ | 100% という実測の意味 | ★★★ **二重に無情報である**。**(A) 方法論警報**: K5-8 は「$\mathrm{Aut}(PB_3/N)$ へ延びるか」を問う形なので、**descent を検査の前提として内包している**。これを**候補列挙のフィルタ**に使うと、非 settled 候補は**そもそも生成されない** ⟹ settled=100% は**恒真**(Sol の言う constant-TRUE 経路そのもの)。**(B) 標本バイアス**: 探索対象(bare $K^{(n)}$・その交わり)は**正典が isolated を保証/示唆する族**である($K^{(n)}$ は Thm 4.3 で isolated、成分の交わり $N^\diamond$ は Prop 3.14 で isolated)⟹ 陰性が出ないのは当然 | §3.2–3.3 |
| **④** ★★ | 係の直観の**救える部分** | ★★ **救える**。**補題 VERBAL-ISO**(本稿・新): **$N_{F_2}$ が $F_2$ の完全不変(verbal)部分群ならば、$N$ の全 GT-shadow は settled、すなわち $N$ は isolated**。⟹ 「自動 settled」は**加群の話ではなく $N_{F_2}$ の不変性の話**だった。**探索が 100% になった第 3 の(そしておそらく真の)理由**の候補 | §3.4 |
| **⑤** | v4 への波及 | ★★ ISO-GATE の意味論を更新: **R1 の列挙は descent フィルタを外して行う**(外さないと M-ISO-2/M-ISO-5 が構造的に作れない)。**S-BU-17** 新設。**W-5 の `UNKNOWN (pending route-2 gate)` は不変** | §5 |

> ### ★ 一行で
> $$\boxed{\ \textbf{settled}\ \iff\ \underbrace{T_{m,f}(N)=1}_{\textbf{descent — hexagon から出ない}}\ \wedge\ \underbrace{\text{全射}}_{\text{shadow の定義}}\ ,\qquad \textbf{K5-8 は左辺の言い換えであって、独立な検査ではない。}}$$

---

## 1. 記法と前提

$B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle$、$x=\sigma_1^2$、$y=\sigma_2^2$、$c=\Delta^2$、$PB_3=F_2\times\langle c\rangle$、$F_2=\langle x,y\rangle$。
$N\trianglelefteq B_3$、$N\subseteq PB_3$、$[B_3:N]<\infty$。$N_{F_2}=N\cap F_2$、$P_N:=F_2/N_{F_2}$、$u:=2m+1$。

**$T_{m,f}$**(Prop 3.2): $T_{m,f}:B_3\to B_3/N$、$\sigma_1\mapsto\sigma_1^{u}N$、$\sigma_2\mapsto f^{-1}\sigma_2^{u}fN$、$c\mapsto c^uN$。hexagon (3.3)(3.4) が**準同型としての well-defined 性**($B_3$ の組みひも関係式の保存)を与える。
⟹ $T_{m,f}(x)=x^uN$、$T_{m,f}(y)=f^{-1}y^ufN$。

**$\varphi$(運用側の写像)**: $\varphi:F_2\to P_N$、$x\mapsto\bar x^{\,u}$、$y\mapsto\bar f^{-1}\bar y^{\,u}\bar f$。$F_2$ は自由なので**常に**準同型として定義される(自由性のみを使う)。$f$ の取り替え($f\mapsto fn$、$n\in N_{F_2}$)で $\varphi$ は変わらない ⟹ **$\varphi$ は類 $[m,f]$ の関数**。

> ### ⚠ 二つの「well-defined」を混同しない(ihnec §6.6 注意 2 の一般形)
> | | 内容 | 何が保証するか |
> |---|---|---|
> | **(W1)** $B_3$ 上の準同型性 | $T_{m,f}$ が $B_3$ の関係式と両立 | ★ **hexagon (3.3)(3.4)** |
> | **(W2)** 商への**降下** | $T_{m,f}(N)=1$、同値に $\varphi(N_{F_2})=1$(§2.2) | ★ **何も保証しない — これが settled の実体** |

---

## 2. 同値性(委嘱事項 ①)

### 2.1 補題 PIGEON(**係の鳩の巣論法の正しい形**)

> ### 補題 PIGEON
> $G$ を群、$H\trianglelefteq G$ を**有限指数**、$t:G\to G/H$ を**全射**準同型とする。
> **(a)** $\ker t$ は $G$ の正規部分群で $[G:\ker t]=[G:H]$。
> **(b)** $$\boxed{\ H\subseteq\ker t\ \Longrightarrow\ \ker t=H\ }$$
> すなわち **descent さえあれば settled は自動**であり、そのとき誘導自己準同型は全単射。
> **証明.** (a) 第一同型定理と全射性。(b) $H\subseteq\ker t$ かつ有限指数が等しいので $\ker t=H$。誘導写像は全射な有限群の自己準同型ゆえ単射。∎

⟹ **係の「有限群の鳩の巣で自動 bijective」は (b) の後半として正しい。** 誤りは、**前件 $H\subseteq\ker t$(= descent)を無条件と見なした点**にある。

### 2.2 補題 DESCENT-c(**$c\in N$ のとき descent は $F_2$ 水準に落ちる**)

> ### 補題 DESCENT-c
> $c\in N$ とする。このとき
> **(a)** $N=N_{F_2}\times\langle c\rangle$。
> **(b)** $T_{m,f}(c)=1$。
> **(c)** $$\boxed{\ T_{m,f}(N)=1\iff\varphi(N_{F_2})=1\ }$$
> **証明.** (a) $N\subseteq PB_3=F_2\times\langle c\rangle$。$(w,c^k)\in N$ なら $c\in N$ より $(w,1)=(w,c^k)c^{-k}\in N$ ⟹ $w\in N_{F_2}$。
> (b) $T_{m,f}(c)=c^uN=N$($c\in N$ ⟹ $c^u\in N$)。
> (c) (a)(b) より $T_{m,f}(N)=T_{m,f}(N_{F_2})=\varphi(N_{F_2})$(同一視 $PB_3/N\cong P_N$ の下で)。∎

### 2.3 ★★ 定理 OP-SETTLED(**委嘱 ① の答え**)

> ### 定理 OP-SETTLED(candidate・本稿)
> $N\trianglelefteq B_3$、$N\subseteq PB_3$、$[B_3:N]<\infty$、**$c\in N$** とし、$[m,f]$ を $N$ の **GT-shadow**(charming GT-pair + 全射性)とする。このとき次は同値:
> 1. **(定義)** $\ker T_{m,f}=N$(= **settled**・Def 3.13)。
> 2. **(降下)** $\varphi(N_{F_2})=1$。
> 3. **(運用 K5-8)** $\bar x\mapsto\bar x^{\,u}$、$\bar y\mapsto\bar f^{-1}\bar y^{\,u}\bar f$ が $\mathrm{Aut}(PB_3/N)\ (\cong\mathrm{Aut}(P_N))$ の元へ延びる。

**証明.**
**(1)⟹(2)**: $\ker T_{m,f}=N$ ⟹ $\varphi$ の核 $=\ker T_{m,f}\cap F_2=N\cap F_2=N_{F_2}$ ⟹ とくに $\varphi(N_{F_2})=1$。
**(2)⟹(3)**: (2) より $\varphi$ は $\bar\varphi:P_N\to P_N$ を誘導する。GT-shadow の全射性(Prop 3.6 の $F_2$ 版: $\langle\bar x^{\,u},\bar f^{-1}\bar y^{\,u}\bar f\rangle=P_N$)より $\bar\varphi$ は全射、$P_N$ は有限ゆえ全単射 ⟹ $\bar\varphi\in\mathrm{Aut}(P_N)$。
**(3)⟹(1)**: (3) より $\varphi$ は降下し、誘導写像は単射 ⟹ $\ker\varphi=N_{F_2}$。補題 DESCENT-c (b) と合わせ
$$\ker T_{m,f}\cap PB_3=\{(w,c^k):\varphi(w)=1\}=\ker\varphi\times\langle c\rangle=N_{F_2}\times\langle c\rangle=N .$$
とくに $N\subseteq\ker T_{m,f}$。GT-shadow の全射性(Prop 3.6 により $T_{m,f}:B_3\to B_3/N$ も全射)と補題 PIGEON (b) から $\ker T_{m,f}=N$。∎

> ### ★ 系(**運用判定は正しいが、独立な検査ではない**)
> $$\boxed{\ \textbf{K5-8 は settled の}\textbf{言い換え}\textbf{であって、settled を独立に検証する検査ではない。}\ }$$
> ⟹ K5-8 を**候補列挙のフィルタ**に使うと、その出力集合では settled が**恒真**になる(§3.2)。

---

## 3. 委嘱事項 ②③ — なぜ AUTO-SETTLED が出ないか

### 3.1 descent は hexagon からも生成性からも出ない

簡約 hexagon(Prop 3.4・$f\in[F_2,F_2]$ 前提)は
$$\textbf{(3.10)}\ f\,\theta(f)\in N_{F_2},\qquad \textbf{(3.11)}\ \tau^2(y^mf)\tau(y^mf)y^mf\in N_{F_2}$$
であり、**$f$(1 元)の所属条件**である。charming は $2m+1\in(\mathbf Z/N_{\rm ord})^\times$ と $\bar f\in[P_N,P_N]$、全射性は $\langle\bar x^u,\bar f^{-1}\bar y^u\bar f\rangle=P_N$。

$$\boxed{\ \textbf{いずれも }\varphi(N_{F_2})=1\ \textbf{(= }N_{F_2}\ \textbf{全体の像が消えること)を含意しない。}\ }$$

**理由の型**: hexagon/charming/SURJ は $(u,\bar f)$ という**有限個のデータ**に対する条件だが、descent は**部分群 $N_{F_2}$ 全体**に対する条件である。前者から後者は形式的に出ない。

### 3.2 ★★★ 非 settled の構造的特徴づけ(**探索の設計に直結**)

$[m,f]$ を GT-shadow とし $K:=\ker T_{m,f}$ と置く。定理 OP-SETTLED の議論から:

| | 内容 |
|---|---|
| **(N1)** | $K\trianglelefteq B_3$、$[B_3:K]=[B_3:N]$、$B_3/K\cong B_3/N$($T$ が誘導する同型) |
| **(N2)** | $K\subseteq PB_3$(合成 $B_3\to B_3/N\twoheadrightarrow S_3$ の核は $PB_3$) |
| **(N3)** | 非 settled $\iff K\ne N$ $\iff N\not\subseteq K$ $\iff\varphi(N_{F_2})\ne1$ |
| **(N4)** | ⟹ **非 settled shadow が存在するには、$N$ と同じ指数・同型商をもつ「双子」$K\ne N$ が $\mathrm{NFI}_{PB_3}(B_3)$ に居なければならない** |

これは正典の groupoid 構造そのものである: $\mathrm{GTSh}(K,N)=\{[m,f]\in\mathrm{GT}(N):\ker T_{m,f}=K\}$ が $K\ne N$ で非空になる場合が**まさに非 settled**であり、Prop 3.8 が「$\mathrm{GTSh}(K,N)\ne\emptyset\Rightarrow K_{\rm ord}=N_{\rm ord}$・各商が同型」と述べている。

$$\boxed{\ \textbf{非 settled は理論上存在する(Thm 3.10 の groupoid が非自明であることと同値)。⟹ AUTO-SETTLED は一般には偽である。}\ }$$

### 3.3 ★★★ 実測 100% の二つの説明(**どちらも「無情報」を意味する**)

| # | 説明 | 帰結 |
|---|---|---|
| **(A) 方法論(致命的)** | K5-8 を**候補列挙のフィルタ**として使った場合、非 settled 候補(= $\varphi$ が降下しないもの)は**候補として生成されない**。⟹ settled 率は**定義により 100%** | ★ **constant-TRUE 経路**(Sol の F104-2.3 R3 の懸念の実物)。さらに悪いことに、**候補を取りこぼした列挙は isolated を偽 TRUE と判定しうる**(欠落した shadow が非 settled かもしれない)⟹ **単に無情報なのではなく、不健全(false-TRUE)である** |
| **(B) 標本バイアス** | 探索対象が **bare $K^{(n)}$**(正典 Thm 4.3 が isolated と明言)と**その交わり**(Prop 3.14: 成分の全対象の交わり $N^\diamond$ は isolated)に偏っている | ★ **陰性が出ないのは正典どおり**。この標本からは何も学べない |

⟹ **係の見立ては、実測からは支持されない**(実測が見立てを支持しうる設計になっていない)。

### 3.4 ★★ 補題 VERBAL-ISO(**係の直観の救える部分 — 新しい十分条件**)

> ### 補題 VERBAL-ISO(candidate・本稿)
> $c\in N$ とし、**$N_{F_2}$ が $F_2$ の完全不変部分群(fully invariant / verbal)** — すなわち $F_2$ の**任意の自己準同型** $\psi$ に対し $\psi(N_{F_2})\subseteq N_{F_2}$ — であるとする。このとき $N$ の**全ての GT-shadow は settled**、すなわち
> $$\boxed{\ N_{F_2}\ \textbf{が完全不変}\ \Longrightarrow\ N\ \textbf{は isolated}\ }$$

**証明.** GT-shadow $[m,f]$ を取り、$f\in F_2$ を一つ持ち上げる。$F_2$ は自由なので
$$\psi:F_2\to F_2,\qquad x\mapsto x^{u},\quad y\mapsto f^{-1}y^{u}f$$
は**自己準同型**として定義される。射影を $\pi:F_2\to P_N$ とすると $\varphi=\pi\circ\psi$。完全不変性より $\psi(N_{F_2})\subseteq N_{F_2}$ ⟹ $\varphi(N_{F_2})=\pi(\psi(N_{F_2}))\subseteq\pi(N_{F_2})=1$ ⟹ **descent**。定理 OP-SETTLED (2)⟹(1) により settled。$[m,f]$ は任意だったので isolated。∎

> ### ★ これが持つ意味
> 1. **「自動 settled」は加群や鳩の巣の話ではなく、$N_{F_2}$ の不変性の話だった。** 係の直観は**この形でなら正しい**。
> 2. ⟹ **探索が 100% になった第 3 の(おそらく真の)理由の候補**: 標本の $N_{F_2}$(下降中心列・冪・それらの交わりから作られる窓)が**完全不変に近い**。
> 3. ★ **isolated の紙証明ルートが 1 本増えた**: 「$N_{F_2}$ が verbal か」を確かめれば isolated が**機械計算なしで**出る(【SD-a】警報・W1 前提の**部分的解消**)。$\gamma_k(F_2)$、$F_2^{\,p}$、$\gamma_k(F_2)F_2^{\,p}$ 等は verbal。
> 4. ⚠ **逆は言えない**($K^{(n)}$ は isolated だが $K^{(n)}_{F_2}$ が verbal かは別問題 —【AS-GAP-2】)。

$$\Longrightarrow\ \boxed{\ \textbf{非 settled を探すなら、}N_{F_2}\ \textbf{が完全不変でない窓を狙え。}\ }$$

### 3.5 ★★★ VERBAL-ISO の即時適用 — **実在の窓 2 つが紙で isolated になる**

工房は既に **verbal / 完全不変**を**別の目的**($N\trianglelefteq B_3$ を出すため)で使っている。**同じ前件がそのまま VERBAL-ISO の前件である。**

| 窓 | $N_{F_2}$ | $c\in N$? | 既出の用途 | ★ VERBAL-ISO の帰結 |
|---|---|---|---|---|
| **HS 主標的 $\mathbf N$** = $\mathcal V(F_2)\times\langle c\rangle$ | $\mathcal V(F_2)=\gamma_5(F_2)F_2^{7}$ — **verbal**(`hsp7_hexagon_arbitration_v1.md` L38 逐語) | ✓(直積因子) | 「verbal ⟹ 完全不変 ⟹ $B_3$ 随伴で不変 ⟹ $N\trianglelefteq B_3$」 | ★★ **$\mathbf N$ は isolated**(紙・機械計算ゼロ) |
| **c2q Heisenberg 窓 $N_0$** $=\pi^{-1}(F_2^{3}\gamma_3(F_2))$ | $F_2^{3}\gamma_3(F_2)$ — **verbal** | ✓(`c2q_finite_def_v1.md` L343 が明記) | 同上 | ★★ **$N_0$ は isolated**(紙) |

> ### ★ これが何を意味するか
> 1. **【SD-a】(裁定 219: 壁窓の isolated 性は全キャンペーンで未検証)の一部が、機械計算なしで閉じる。** ⟹ `ihnec_v1.md` T-5 / (S4-ISO) 前件の扱いに直接効く。
> 2. **一般則**: $N_{F_2}$ を **verbal 部分群として構成した窓は、その構成自体によって isolated である**。⟹ 「$B_3$-正規性のために verbal を使う」設計は、**副産物として isolated も買っていた**。
> 3. ⚠ **$\mathrm{PSL}(2,8)$ 窓 $N_{\rm S4}$ には適用できない**($N_{F_2}$ が verbal として構成されていない)⟹ **(S4-ISO) は依然 UNKNOWN**。**W-5 も同様**(§5.5)。
> 4. ⚠ **未確認**: 上記 2 窓が正典の意味で $\mathrm{NFI}_{PB_3}(B_3)$ の対象であること(有限指数)は既存文書の記述に依拠しており、当方は再検算していない【AS-GAP-5】。

---

## 4. 委嘱事項 ① の続き — 同値が壊れる場所(**判定形が見逃す穴**)

| # | 条件を外すと | 何が壊れるか |
|---|---|---|
| **H-1** ★ | **$c\notin N$** | 補題 DESCENT-c (a)(b) が崩れる。$N\ne N_{F_2}\times\langle c\rangle$ であり、$T_{m,f}(c)=c^uN$ は**自明とは限らない**。⟹ $\varphi(N_{F_2})=1$ でも $T_{m,f}(N)=1$ とは限らない($c$-成分をもつ $N$ の元が検査から**完全に漏れる**)。⟹ **K5-8 は必要条件にしかならない**(定義ノート §2 の「$c\notin N$ では商の近道が壊れる($M_5$ 等)」の settled 版)。★ **これが「isolated は $PB_3$ 水準の必要条件のみ」という既存注記と整合する読みである** |
| **H-2** | **全射性(shadow でなく単なる GT-pair)** | 補題 PIGEON の前件が消える。降下しても誘導写像が全射でなければ単射も出ない ⟹ (2)⟹(3) が壊れる。⟹ **charming だけの pair に K5-8 を当ててはならない** |
| **H-3** | **$PB_4$ / $B_4$ 水準(副線)** | 証明は $PB_3=F_2\times\langle c\rangle$(自由群 × 中心)と $[B_3:PB_3]=6$ に依存する。$PB_4$ はこの形をもたない ⟹ **移送不可**。$B_4$ 系では pentagon も加わるので Prop 3.6 の類似から確認が要る【AS-GAP-1】 |
| **H-4** ★ | **語水準での判定**($\bar f$ でなく語 $f$ で列挙) | 無重複が壊れる(v4 §5.1 B-1)。さらに $\varphi$ の評価を**語のまま**行うと、$N_{F_2}$ の生成系を経由しない限り descent は検査できない |
| **H-5** ★★ | **列挙フィルタとしての K5-8** | §3.3 (A)。**候補欠落 ⟹ isolated の false-TRUE**。⟹ v4 の **M-ISO-5** が狙っていた穴が、**実際の実装で開いていた**ことになる |

---

## 5. v4 への波及(**ISO-GATE の意味論更新**)

### 5.1 R1(列挙)の仕様追加

> ### ★ R1-b(新設・必須)
> $$\boxed{\ \textbf{候補列挙は }\mathbf{descent}\ \textbf{フィルタ(K5-8 / }\mathrm{Aut}\ \textbf{へ延びるか)を}\textbf{使わずに}\textbf{行う。}}$$
> **正しい順序**: (i) $(m,\bar f)\in(\mathbf Z/N_{\rm ord})\times[P_N,P_N]$ を**群の元として**悉皆列挙(v4 §5.1 B-1)(ii) hexagon (3.10)(3.11) と charming と **SURJ** で絞る = **GT-shadow の集合**(iii) **その後で** descent を検査する = settled 判定。
> ⟹ (iii) を (ii) に混ぜた実装は **isolated を false-TRUE にしうる**(§4 H-5)。

### 5.2 descent 検査の実装仕様(**現在欠けている検査**)

$\varphi(N_{F_2})=1$ を検査するには **$N_{F_2}$ の生成系**が要る。$N_{F_2}\le F_2$ は有限指数なので:

$$\boxed{\ \textbf{Reidemeister–Schreier で }N_{F_2}\ \textbf{の自由生成系}\ \{n_1,\dots,n_r\}\ (r=1+[F_2:N_{F_2}])\ \textbf{を取り、}\varphi(n_i)=1\ \textbf{を全 }i\ \textbf{で検査する。}}$$

($F_2$ は階数 2 の自由群なので、指数 $d$ の部分群は階数 $d+1$ の自由群 — Nielsen–Schreier。$d=\lvert P_N\rvert$。)
⟹ **これが K5-8 の「$\mathrm{Aut}$ へ延びるか」を内側から実装する唯一の健全な形**であり、GAP の `GroupHomomorphismByImages` の `fail` 捕捉(v4 §5.2 B-2 の (i))と**同じ検査**である。**どちらか一方でよいが、列挙フィルタに使ってはならない。**

### 5.3 mutant matrix の更新(v4 §5.3)

| # | 変更 |
|---|---|
| **M-ISO-2**(既知 non-isolated 陰性) | ★ **作り方が判明した**: §3.2 (N4) より、**$N$ と同指数・同型商の「双子」$K$ をもつ窓**を狙う。あるいは §3.4 より **$N_{F_2}$ が完全不変でない窓**。⟹ **bare $K^{(n)}$ とその交わりを標本にしてはならない**(§3.3 (B)) |
| **M-ISO-5**(候補欠落) | ★ **優先度を最上位へ**。§4 H-5 の穴は仮説ではなく、**現行実装で開いている疑いが濃い** |
| **M-ISO-7** ★新 | **descent フィルタ混入検出**: 列挙段のコードに K5-8 相当(`Aut` への延長 / `GroupHomomorphismByImages` の成否)が現れたら**不合格**。source-map で検出する |

### 5.4 停止規則

| # | trigger | verdict |
|---|---|---|
| **S-BU-17** ★新 | shadow の**列挙段**で descent 判定(K5-8 / `Aut` 延長 / hom 構成の成否)を使った | `ENUMERATION_FILTER_CONTAMINATION / STOP`(settled 率は恒真になり、isolated は false-TRUE になりうる) |

### 5.5 v4 本文への差分(**1 節ぶん**)

- **§5.1 R1**: 上の **R1-b** を追加。
- **§5.2 B-2**: 「(i) well-defined」の実装として **Reidemeister–Schreier 版**を併記(§5.2)。
- **§5.3**: M-ISO-2 の作り方(双子/非 verbal)・M-ISO-7 を追加。
- **§7**: S-BU-17 を追加。
- ⚠ **W-5 の `UNKNOWN (pending route-2 gate)` は不変**(F104-2.3)。**本検分は gate を閉じない — むしろ現 cert の 2/2 が constant-TRUE を通す理由を特定した。**

---

## 6. 格付け・【GAP】・新規性

### 6.1 格付け

| 主張 | 格 |
|---|---|
| **補題 PIGEON** | ★ **paper-proof candidate**(初等・2 行) |
| **補題 DESCENT-c** | ★★ **paper-proof candidate**($c\in N$ の直積分解) |
| **定理 OP-SETTLED**(3 条件の同値) | ★★★ **paper-proof candidate**(Prop 3.2/3.6 と Def 3.13 に相対・**Sol 未監査**) |
| **補題 VERBAL-ISO** | ★★ **paper-proof candidate**(完全不変性のみ・**新しい isolated 十分条件**) |
| §3.2 の非 settled の構造的特徴づけ | ★★ **成立**(正典 Thm 3.10 / Prop 3.8 の読み替え) |
| §3.3 の実測 100% の説明 | ★★★ **方法論判定**(係の cert を読まずに、判定形の意味論だけから出した)。⚠ **実装が実際に K5-8 をフィルタに使ったか**は当方未確認 —【AS-GAP-3】 |
| 定理 AUTO-SETTLED(委嘱の仮説) | ✗ **不成立**(§3.1・§3.2)。条件付き形(= OP-SETTLED + VERBAL-ISO)でのみ成立 |
| `cross-checked` / `verified` | ✗ **どちらも付さない**(紙のみ・単一起草者・機械実行ゼロ) |

### 6.2 【GAP】

| 札 | 内容 | 状態 |
|---|---|---|
| **【AS-GAP-1】** | $B_4$/$PB_4$ 水準(副線)への移送。$PB_4$ は $F\times\langle c\rangle$ の形をもたない | **UNKNOWN**(射程外) |
| **【AS-GAP-2】** | VERBAL-ISO の**逆**。isolated ⟹ $N_{F_2}$ 完全不変 は言えない。$K^{(n)}_{F_2}$ が verbal かも未確認 | **UNKNOWN**(安い・reader/implementer 案件) |
| **【AS-GAP-3】** ★ | **係の実装が実際に K5-8 を列挙フィルタに使ったか**の確認(当方は cert 未読)。使っていなければ §3.3 (A) は当たらず、(B)+§3.4 だけが残る | **要確認(最優先・司令塔案件)** |
| **【AS-GAP-4】** | 非 settled の**具体例**。正典に例が載っているか(2401.06870 の groupoid 節)は当方未確認 | **UNKNOWN**(reader 案件・M-ISO-2 の一次資料になる) |
| **【AS-GAP-5】** ★ | §3.5 の 2 窓が有限指数($\mathrm{NFI}_{PB_3}(B_3)$ の対象)であることは既存文書の記述に依拠。当方は再検算していない | **要確認**(安い) |

### 6.3 新規性(**grep 済**: `AUTO-SETTLED`・`OP-SETTLED`・`VERBAL-ISO`・`PIGEON`・`DESCENT-c`・`完全不変`・`fully invariant`・`Reidemeister`)

| 項目 | 既出か | 差分 |
|---|---|---|
| K5-8(運用判定)と Def 3.13 の**区別** | ★ **既出**(`ihnec_v1.md` §6.6 注意 2: 「$T_{m,f}$ を実現する $h\in\mathrm{Aut}$ の witness 探索」と「壁 judge の well-definedness」は別物) | ★ 本稿は**両者が(3 前件の下で)同値であること**を証明した — 注意 2 とは矛盾しない(注意 2 は壁 judge 側の別の量との区別) |
| **定理 OP-SETTLED** | **発見できず** | ★★★ **本稿** |
| **補題 VERBAL-ISO** | ⚠ **概念は既出**(★ 初稿の「grep ゼロ」は**誤り**・自己訂正): `hsp7_hexagon_arbitration_v1.md` L38「$\mathcal V(F_2)=\gamma_5(F_2)F_2^7$ は verbal ⟹ 完全不変 ⟹ $B_3$ の随伴作用で不変」、`c2q_finite_def_v1.md` L343「fully invariant ゆえ $B_3$-安定・$c\in N_0$」 | ★ **用途が違う**: 既出は **$N\trianglelefteq B_3$(正規性)** を出すために使っている。本稿は**同じ性質から settled / isolated を出す**(§3.4)。⟹ 寄与は「完全不変性の**第 2 の使い道**の発見」であり、**「初」とは書かない**(完全不変部分群が自己準同型で保たれることは定義そのもの) |
| 非 settled ⟺ 双子 $K$ の存在 | ★ **正典の groupoid の言い換え**(Thm 3.10 / Prop 3.8) | ★ 本稿は**探索設計への翻訳**を与えた |

---

## 7. 司令塔への回答(要約)

1. **①同値性**: ★ **同値**(定理 OP-SETTLED)。前件は $c\in N$・$N\trianglelefteq B_3\subseteq PB_3$ 有限指数・**GT-shadow(全射性込み)**の 3 つ。$c\notin N$ では**必要条件のみ**に落ちる(§4 H-1)⟹ 既存注記「isolated は $PB_3$ 水準の必要条件のみ」と整合。$PB_4$ は射程外(H-3)。
2. **②AUTO-SETTLED**: ⚠ **不成立**。鳩の巣は「descent + 全射 ⟹ settled」の部分でのみ正しく、**descent は hexagon からも生成性からも出ない**独立条件である。ただし ★ **補題 VERBAL-ISO**(「$N_{F_2}$ 完全不変 ⟹ isolated」)という**条件付きの自動 settled 定理**が得られた — 係の直観はこの形でなら正しい。
3. **③100% の意味**: ★★★ **二重に無情報**(判定形が descent を内包・標本が既知 isolated 族)。しかも**単に無情報なのではなく、列挙フィルタに使っていたなら isolated は false-TRUE になりうる**(§4 H-5)。**【AS-GAP-3】(実装が実際にフィルタに使ったか)の確認が最優先。**
4. **v4 への波及**: **R1-b(列挙は descent フィルタ抜き)**・descent 検査の Reidemeister–Schreier 実装・**M-ISO-2 の作り方(双子/非 verbal を狙う)**・**M-ISO-7**・**S-BU-17**。**W-5 は `UNKNOWN (pending route-2 gate)` のまま。**
5. ★★ **副産物(委嘱外・報告する価値があるもの)**: VERBAL-ISO により **HS 主標的 $\mathbf N=\mathcal V(F_2)\times\langle c\rangle$ と c2q Heisenberg 窓 $N_0$ が、機械計算なしで isolated と分かる**(§3.5)。⟹【SD-a】の一部が紙で閉じる。**ただし $\mathrm{PSL}(2,8)$ 窓 (S4-ISO) と W-5 には適用できない**($N_{F_2}$ が verbal として構成されていないため)。

---
---

# 付録 A — **v1.1 addendum**(2026-08-05・裁定 529 の着弾を受けて)

> **本 addendum は additive である。上の v1 本文(§0〜§7)は 1 文字も書き換えていない。** 本文と食い違う箇所は本 addendum が優先する(該当は A.1 の 1 点のみ)。
> 起草: 影工房 数学者(Claude / Opus 5)。**紙のみ・機械実行ゼロ・新規探索ゼロ・封印非接触。**
> 入力: 司令塔経由の実装側回答(**裁定 529**)— (a) `search/week3-battery-common.g` の `EnumerateReducedHexagon` per-candidate loop(`for cand in Dwords do`)は `GroupHomomorphismByImages` / `IsBijective` を**一切呼ばない** (b) descent 検査は shadow 集合確定**後**の `SettledCheckGeneral` 下流のみ(source-map 静的検査で確認) (c) M-ISO-7 検出器は故意破壊 enumerator を **S-BU-17** で正しく検出 (d) 新経験事実: **$K^{(3)}$ の hexagon 列挙で `generation_fail=0`**、M-ISO-2 witness は **h11-fail 候補(像 36 < 108 の真部分群生成)**で構成。
> ⚠ 当方はコードも cert も読んでいない(上記は司令塔経由の報告を前提として扱う)。

## A.1 【AS-GAP-3】の解決 — **混入なし**。条件節が外れる

| 本文 §3.3 の 2 説 | v1.1 での確定 |
|---|---|
| **(A) 方法論(constant-TRUE 経路)**: K5-8 を列挙フィルタに使ったのではないか | ★ **排除**。列挙段は descent 判定を呼んでおらず、**既存列挙は本文 §5.1 の R1-b に既に適合**していた |
| **(B) 標本バイアス** | ★ **確定**。bare $K^{(n)}$ は正典 Thm 4.3、その fiber 積(成分の交わり)は Prop 3.14 により**正準に isolated** ⟹ 陰性が出ないのは**理論どおり** |

$$\boxed{\ \textbf{本文 §4 H-5 と §3.3 (A) の「不健全(false-TRUE)の疑い」は、この実装については}\textbf{解除する}\textbf{。}}$$

- **本文の訂正はこの 1 点のみ**。§3.3 の表の (A) 行は「一般に起こりうる失敗型」としては有効だが、**当該実装には当たらない**。
- **S-BU-17 / M-ISO-7 は撤回しない**: 検出器が故意破壊版を実際に捕まえた以上、**回帰項目として維持する価値がある**(将来の実装変更に対する保険)。
- **100% という観測の情報量は依然ゼロ**である(理由が (A) から (B) に変わっただけで、標本が既知 isolated 族である限り AUTO-SETTLED の証拠にはならない)。⟹ **本文 §0 ②③ の判定は不変**。

## A.2 ★ ただし **M-ISO-2 は未充足のまま**(h11-fail 候補は GT-shadow ではない)

M-ISO-2 の要求は Sol の逐語で「**既知 non-isolated 陰性**」である。isolated は Def 3.13 で「**GT-shadow が全て settled**」と定義され、**GT-shadow は charming GT-pair + 全射性**(Def 3.7)である。したがって:

$$\boxed{\ \textbf{h11(生成性)で落ちる候補は }\mathrm{GT}(N)\ \textbf{の元ではない} \ \Longrightarrow\ \textbf{isolated 性について何も語らない。}}$$

| 項目 | 判定 |
|---|---|
| h11-fail 候補が discharge するもの | ★ **M-ISO-3(constant-TRUE 検出)**: パイプラインが常に TRUE を返すわけではないことは示せる。また **M-ISO-6(前件欠落)**の一部にも当たる |
| h11-fail 候補が discharge **しない**もの | ★ **M-ISO-2 本体**。非 settled の**shadow** を 1 件も見ていない ⟹ 「settled 述語が FALSE を返せること」は未実証 |
| ⚠ 期待判定の確認要求 | h11-fail 候補に対する**正しい挙動は「shadow 段で除外(または UNKNOWN)」**であって「非 settled(FALSE)」ではない。もしパイプラインがこれを FALSE として窓の isolated 判定へ伝播させるなら、**false-FALSE の経路**になる(isolated な窓を非 isolated と誤判定する)。⟹ **fixture の期待値を「除外/UNKNOWN」で登録すること**を求める |

⟹ **本文 §5.3 の M-ISO-2 の作り方(同指数・同型商の「双子」$K\ne N$ をもつ窓、または $N_{F_2}$ が完全不変でない窓)は依然として有効な唯一の道である。**【AS-GAP-6】として起票する。

## A.3 `generation_fail=0` on $K^{(3)}$ の記録と解釈

**記録**: $N=K^{(3)}$、$P_N=G_3$、$\lvert G_3\rvert=4\cdot3^3=108$。hexagon を通った候補は**全件が生成性 (SURJ) を満たした**(`generation_fail=0`)。M-ISO-2 witness の像位数 **36**($=108/3$)は人工的に構成されたものである。

> ### ★ 命題 GEN-AB(candidate・一行の解釈)
> $n$ 奇、$P=G_n$($\lvert G_n\rvert=4n^3$、$A:=[G_n,G_n]\cong C_n^3$、$G_n^{\rm ab}\cong C_2^2$)、$[m,f]$ を **charming** GT-pair($u=2m+1$ **奇**、$\bar f\in[P,P]=A$)とし $H:=\langle\bar x^{\,u},\ \bar f^{-1}\bar y^{\,u}\bar f\rangle$ と置く。**$P^{\rm ab}\cong C_2^2$ では $u$ 倍は恒等**、かつ $\bar f\in[P,P]$ は $P^{\rm ab}$ で消えるので、2 生成元の $P^{\rm ab}$ における像は $\bar x,\bar y$ そのものである。ゆえに
> $$\boxed{\ H\cdot[P,P]=P\ \ \textbf{は charming なら常に成り立つ。}\ \Longrightarrow\ \textbf{生成性が破れうるのは }A=[P,P]\ \textbf{の内部だけ。}\ }$$

**解釈(1 行)**: ⟹ `generation_fail=0` は「hexagon を通った候補で $H\cap A$ が真部分群になるものが 1 件も無かった」という意味であり、**SURJ の識別力は事実上 $A$-成分のみに掛かっている**。人工 witness の像 $36=4\cdot9$ が「2-部は満杯・$A$-部だけ指数 3」という形になっているのは、この構造の**予言どおり**である(整合の 1 点)。
⚠ **これは「$K^{(3)}$ で SURJ が恒真」の証明ではない**(命題 GEN-AB は $H\cdot A=P$ までしか言わない)。**識別力ゼロの検査を「通った」と数えない**(S-W6-3 の趣旨)。

## A.4 不変事項(**便 105 §3 に載せる際の確認欄**)

| # | 事項 | 状態 |
|---|---|---|
| 1 | **定理 AUTO-SETTLED は不成立**(一般には偽) | ★ **不変**(A.1 は理由を (A) から (B) に確定させただけ) |
| 2 | **定理 OP-SETTLED**(K5-8 ⟺ Def 3.13・3 前件つき)・**補題 PIGEON / DESCENT-c / VERBAL-ISO** | ★ **不変**(Sol 未監査の candidate) |
| 3 | §3.5: HS 主標的 $\mathbf N$ と c2q $N_0$ が **verbal ⟹ isolated**(紙) | ★ **不変**(【AS-GAP-5】= 有限指数の再検算は未) |
| 4 | **W-5 = `UNKNOWN (pending route-2 gate)`** | ★ **不変**(F104-2.3 逐語。本 addendum は gate を閉じない) |
| 5 | ISO-GATE の格: `isolated_verdict=TRUE` ≠ `iso_gate_state=PROVEN` | ★ **不変**(v4 §5.5)。R3 は **M-ISO-2 未充足**ゆえ**未閉**(A.2) |

## A.5 【GAP】更新

| 札 | 状態(v1.1) |
|---|---|
| **【AS-GAP-3】** | ★ **閉**(裁定 529: 混入なし・標本偏りで確定・R1-b 既適合) |
| **【AS-GAP-6】** ★新 | **M-ISO-2(既知 non-isolated 陰性)の実物 witness が未取得**。h11-fail 候補では代替できない(A.2)。取得法は本文 §5.3(双子 $K$ / 非 verbal $N_{F_2}$) | **UNKNOWN(route-2 gate の律速)** |
| 【AS-GAP-1】【AS-GAP-2】【AS-GAP-4】【AS-GAP-5】 | 不変 |
