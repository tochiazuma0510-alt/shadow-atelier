# 狩猟章 v1 — 反例狩り v6 の検分と編纂への織り込み(裁定 791)

**日付**: 2026-08-11 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・**判定語の発効は司令塔専権**)
**入力**: `docs/notes/ideas_counterexample_hunt_v1.md`(発案 v6・c39ebfc)/ 裁定 787(研究者教義)/ 裁定 791
**拘束**: 設計・証明のみ(実走なし)・S₁₂@691 封印非接触・IF-FIRST・novelty grep 済(§8)

---

# §0 要旨 — 検分の結論(先出し)

> ### ★★★ 最大の発見 2 件(いずれも**紙で出た・走行ゼロ**)
> **(I) 命題候補 GR-UB(§2)**: 各段の上層は**中心**ゆえ hexagon の摂動は**基点非依存の線形写像**になる ⟹
> $$\boxed{\ \log_p\lvert GT\rvert\ \le\ \sum_k\dim\mathcal S_k\quad\textbf{すなわち}\quad \mathrm{def}(c,p)\le0\ \textbf{は常に成立(定理)}\ }$$
> ⟹ **正札 WILD-NOEXCESS(超過なし)は測定の成果ではなく定理の帰結**。測定の内容は「超過なし」ではなく**残差ゼロ(等号)**の方である。**編纂は言い換えを要する**(§7.2)。
>
> **(II) 命題候補 STD-DIM + NORM-1 の定理化(§2.3)**: hexagon 条件 $\ker(1+\theta)\cap\ker(1+\tau+\tau^2)$ は $\mathbf F_p[S_3]$($p\ge5$)上**ちょうど std-isotypic 成分の $\theta=-1$ 線**を切る ⟹ $\dim\mathcal S_k=m_{\rm std}(\Lambda_k)$(既収の $H_k=\frac13[\mathrm{Witt}(2,k)-\mathrm{tr}(\tau|\Lambda_k)]$ と**恒等**)。Maschke で $\Lambda_p\cong R_p\oplus(\text{群側層})$ ⟹
> $$\boxed{\ \mathrm{def}_p=-m_{\rm std}(R_p)\ \textbf{(NORM-1)は 1 行の定理}\ }$$
> ⟹ 追補 C §2 の留保【PLC-GAP-1】(「P-PL-5′b は合成予言・分離不能」)は**降格**: 経験入力は $\dim R_p=p-1$ の**スカラー 1 個だけ**に落ちる。

> ### ★★ 検分の帰結(v6 への差分)
> | 札 | v6 の位置 | 本検分 | 理由 |
> |---|---|---|---|
> | **CH-1 FILT-LIFT** | 順位 1(機械・分) | ★ **紙へ再スコープ**(GR-UB) | 心臓は定理。機械部分は**残差ゼロ測定で既に回収済**(§3.1) |
> | **CH-7 FROB-SHADOW** | 順位 2 | ▼ **狩りとしては空**(mod $p$ は恒真式) | $\zeta_p(m)\equiv0\ (p)\iff(p,p-m)$ 非正則 は**定義同値**(§4.3) |
> | **CH-6 INV-CENSUS** | 順位 3 | ▼ **閉じた扉 1 と冗長** | サイズ一致窓では対合も自動的に算術(§5.3) |
> | **CH-2 M-SWEEP** | 順位 4 | ▼ **$m$ 一様は剰余類定理**(条件つき) | 残る内容は「どの $\lambda$ が出るか」だけ(§5.4) |
> | **CH-5 E2/E3 繊維** | 順位 5 | ▲ **昇格**(安い閉じた公式が立つ) | 繊維サイズ $=\#\{\text{braid 生成対}\}/\lvert\mathrm{Aut}\,G\rvert$(§5.5) |
> | **CH-4 h^cen/χ 扉** | 順位 6(定義委嘱が先) | ▲ **定義問題は既決**・表読みへ | 正典は $c\notin N$ で定義済(§3.3)・既測 h^cen=24 の ab を読むだけ |
> | **★ SAT-37(新札)** | — | ★★ **新設・上位** | $(37,32)$ の正しい読み = **飽和欠損(指数)**(§4.4) |

---

# §1 閉じた扉 5 枚の検分 — 3 枚是認・2 枚**理由を差し替えて**閉

「閉じていることの確認も全力の一部」(v6 §1.2)に同意。ただし**理由が違えば扉は閉じていない**ので、5 枚とも証明を書き直した。

## 1.1 扉 1(サイズ会計)— ★ 是認(自明だが正しい)

算術像 $\subseteq$ genuine $\subseteq GT(N)$ は定義。有限集合で $A\subseteq B$ かつ $\lvert A\rvert=\lvert B\rvert$ なら $A=B$。∎
**射程の明記**: これは「**サイズが一致した窓では**元ごとの追跡は不要」を言う。サイズが**一致しない**窓(飽和欠損)では扉は開いている — §4.4 の SAT-37 はまさにその隙間を狙う。

## 1.2 扉 2(CRT 透過)— ⚠ **理由を差し替え**(v6 の「hexagon も分解」は不正確)

**v6 の誤り**: 合成位数の梯子 $G_{pq}=(H_p\times H_q)\rtimes S_3$ は $G_p\times G_q$ **ではない**($S_3$ 上のファイバー積 $G_p\times_{S_3}G_q$)⟹「hexagon が直積に分解する」は成り立たない。

> ### 命題候補 **CRT-INJ**(candidate・本章)
> $N=N_p\cap N_q$($N_p=\ker(B_3\to G_p)$ 等)とすると $B_3/N\hookrightarrow B_3/N_p\times B_3/N_q$。$N\subseteq N_p,N_q$ ゆえ簡約 $R_{N,N_p},R_{N,N_q}$ が定義され、
> $$\boxed{\ GT(N)\ \hookrightarrow\ GT(N_p)\times GT(N_q)\ \textbf{(単射)}\ }$$
> **証明**: shadow は対 $(m,f)$ で $f\in F_2/N_{F_2}$。$N_{F_2}=N\cap F_2=(N_p\cap F_2)\cap(N_q\cap F_2)$ ⟹ $F_2/N_{F_2}\hookrightarrow F_2/(N_p)_{F_2}\times F_2/(N_q)_{F_2}$。$m$ も $N_{\rm ord}=\mathrm{lcm}$ の CRT で決まる。∎

**★ 扉を閉じるのに必要なのは単射性だけ**:「合成位数でだけ現れる隠れ shadow」があれば $\lvert GT(N)\rvert>\lvert GT(N_p)\rvert\lvert GT(N_q)\rvert$ になるが、単射性がそれを禁じる。**全射性(逆向き)は不要で、実際 UNKNOWN**。⟹ 扉は閉。**ただし「アデール的隠蔽なし」は言えても「合成位数窓に新情報なし」は言えない**(全射でない = 両立不能な組が落ちる ⟹ それ自体は情報)。**v6 の主張は正しいが理由と射程を訂正した。**

## 1.3 扉 3・4(有限指数の隠蔽不能・塔互換な偽装の不能)— ★ 是認・**強化**

> ### 命題候補 **COMPACT-COMPLETE**(candidate・本章)
> $\mathrm{Ih}:G_\mathbb Q\to\widehat{GT}=\varprojlim GT(N)$ は連続、$G_\mathbb Q$ はコンパクト ⟹ 像は閉。逆極限系の像は filtered な非空コンパクト系ゆえ
> $$\boxed{\ \mathrm{im}(\mathrm{Ih})=\varprojlim_N\mathrm{im}(\mathrm{Ih})_N\quad\Longrightarrow\quad\bigl[\forall N:\mathrm{im}_N=GT(N)\bigr]\Longrightarrow\mathrm{im}=\widehat{GT}\ }$$
> **証明**: 各 $x=(x_N)$ に対し $S_N=\mathrm{Ih}^{-1}(x_N)$ は閉・非空・filtered 減少 ⟹ $\bigcap S_N\ne\emptyset$(コンパクト性)。∎

**v6 より強い**: v6 は「指数有限なら」と条件を付けたが、**指数条件は不要**(任意の閉真部分群で成立)。⟹ **窓プログラムは原理完備**、かつ扉 4(「各層で算術・極限で非算術」)は扉 3 の同じ 1 行から従う(v6 が 2 枚に数えたのは実質 1 枚)。**残る隙間は cofinality のみ**(v6 の指摘どおり = WR-6 の主題)。

## 1.4 扉 5($M_{p^3}$ 梯子は立たない)— ⚠ **理由を差し替え**(v6 の「1 次元商なし」は不足)

**v6 の言い方**「℘ が $S_3$-同変線形 ⟹ 既約 std に 1 次元商なし」は、$Z$ の**表現型**を言わないと閉じない($\mathrm{std}\to Z$ が非零でも $Z\cong\mathrm{std}$ なら矛盾しない)。正しい鍵は $Z$ が **sgn** であること。

> ### 命題候補 **MOD-NOGO**(candidate・本章・v6 の no-go の**修理**)
> $p\ge5$、$M=M_{p^3}$(指数 $p^2$ の modular 群、位数 $p^3$)、$Z=Z(M)=[M,M]\cong C_p$、$V=M/Z$。$S_3$ が $M$ に作用し $V\cong\mathrm{std}$(忠実 std)と仮定する。すると**矛盾**。
> **証明**: (i) 交換子写像 $V\times V\to Z$ は交代双線形全射 ⟹ $Z\cong\Lambda^2V=\Lambda^2\mathrm{std}=\det(\mathrm{std})\cong\mathrm{sgn}$(鏡映の行列式 $=-1$)。
> (ii) $p$ 冪写像 $\wp:x\mapsto x^p$ は $Z$ 上自明($\exp Z=p$)ゆえ $V\to Z$ を誘導。類 2 ゆえ $(xy)^p=x^py^p[y,x]^{\binom p2}$ で、$p$ 奇 ⟹ $\binom p2=\frac{p(p-1)}2\equiv0\ (p)$、$[y,x]\in Z$ の位数 $p$ ⟹ $(xy)^p=x^py^p$ ⟹ $\wp$ は加法的、$\mathbf F_p$ 上線形。
> (iii) $\wp$ は自己同型と可換 ⟹ $S_3$-同変。$\exp M=p^2$ ⟹ $\wp\ne0$。
> (iv) ゆえに $0\ne\wp\in\mathrm{Hom}_{S_3}(\mathrm{std},\mathrm{sgn})=0$($p\ge5$ で Maschke・std は絶対既約かつ $\not\cong$ sgn)。矛盾。∎
>
> ★ **副産物**: 同じ議論で「$Z\cong\mathrm{sgn}$」は**指数 $p$ の Heisenberg でも成立** ⟹ 梯子 $G_p$ の中心の $S_3$-型は sgn(既収の TWIST-6 系と整合・独立確認)。

## 1.5 扉の枚数の訂正

**5 枚 → 実質 4 枚**(扉 3 と 4 は同一の compactness 1 行)。さらに扉 2 と 5 は**理由が差し替わった**。⟹ 編纂には「閉扉 4 枚(うち 2 枚は本章で証明を書き直し)」と書く。

---

# §2 ★★★ CH-1 の心臓を紙で — 命題 GR-UB と NORM-1 の定理化

## 2.1 命題 GR-UB(graded 会計は**上界**である)

> ### 命題候補 **GR-UB**(candidate・本章・repo 初出)
> $G$ を有限群、$\gamma_k$ をその下中心列、$S_k:=\{$窓 $\ker(B_3\to G/\gamma_k)$ の hexagon 解 $\}$ とする。$\gamma_k/\gamma_{k+1}$ は $G/\gamma_{k+1}$ の**中心**ゆえ、持ち上げ $f\mapsto fu$($u\in\gamma_k/\gamma_{k+1}$)に対し hexagon 欠損は
> $$H(fu)=H(f)\cdot L_k(u),\qquad L_k:\gamma_k/\gamma_{k+1}\to\gamma_k/\gamma_{k+1}\ \textbf{加法的・}f\ \textbf{に依存しない}$$
> **($u$ が中心ゆえ全ての共役・交換子項が消え、$u$ の寄与は語の指数和だけで決まる)**。ゆえに $f$ 上の繊維は**空か $\ker L_k$ の剰余類**で、
> $$\boxed{\ \lvert S_{k+1}\rvert\le\lvert S_k\rvert\cdot\lvert\ker L_k\rvert\quad\Longrightarrow\quad \log_p\lvert GT\rvert\le\sum_k\dim\ker L_k\quad\Longrightarrow\quad\mathrm{def}(c,p)\le0\ }$$
> **等号 $\iff$ 全段で障害ゼロ**(障害 $=H(f)\bmod\mathrm{im}\,L_k$ が恒等的に自明)。∎

**【GR-GAP-1】**: $\ker L_k=\mathcal S_{k+1}$(会計で使う層空間)の同一視は、Lazard 域では実測 $\mathrm{def}_k=0$($k<p$・P-PL-1′)が保証。$k=p$ では $\S2.3$ の補正が入る。**この同一視は仕様同一性の問題**(CV-9 型)⟹ falsifier 判読を推奨。

## 2.2 ★ 帰結 1 — 「超過なし」は測定していない

$\mathrm{def}\le0$ が定理なら、**正札 WILD-NOEXCESS の「超過なし」部分は自明**。測定が実際に買ったのは
$$\boxed{\ \textbf{等号(残差ゼロ)}\ \Longleftrightarrow\ \textbf{持ち上げ障害が全段でゼロ}\ }$$
であり、これは**まさに CH-1 FILT-LIFT が測ろうとしていたもの**。⟹ ★ **CH-1 の目的は $(5,5)$・$(7,7)$ で既に達成されている**(NORM-CHK の残差ゼロ = 全段無障害・GR-UB により段ごとの打ち消しは起こり得ない: 各段が $\le$ ゆえ総和の等号は各段の等号を強制)。

## 2.3 ★★★ 帰結 2 — NORM-1 は定理(hexagon 層 = std 重複度)

> ### 命題候補 **STD-DIM**(candidate・本章・repo 初出)
> $p\ge5$、$M$ を $\mathbf F_p[S_3]$-加群とする。$\tau$ の位数 3・$p\ne3$ ゆえ $1+\tau+\tau^2$ は triv/sgn 上 $=3$(可逆)、std 上 $=0$ ⟹
> $$\ker(1+\tau+\tau^2)=M^{\mathrm{std}\text{-isotypic}},\qquad \ker(1+\theta)\cap M^{\rm std}=\textbf{各 std コピーの }\theta=-1\ \textbf{線}$$
> $$\boxed{\ \dim\bigl[\ker(1+\theta)\cap\ker(1+\tau+\tau^2)\bigr]=m_{\rm std}(M)\ }$$
> **既収の $H_k=\frac13\bigl[\mathrm{Witt}(2,k)-\mathrm{tr}(\tau\mid\Lambda_k)\bigr]$ と恒等**($m_{\rm std}=\frac13(\chi(1)-\chi(\tau))$)⟹ **独立導出による裏取り**。∎

> ### ★★ 系 **NORM-1 は定理**(v6 起点でなく本章の帰結)
> 群側の層 $\gamma_p/\gamma_{p+1}\cong\Lambda_p/R_p$($R_p$ は関係加群)。$p\ge5$ ⟹ Maschke ⟹ $\Lambda_p\cong R_p\oplus(\Lambda_p/R_p)$ ⟹ $m_{\rm std}$ は加法的 ⟹
> $$\dim\mathcal S_p^{\rm group}=m_{\rm std}(\Lambda_p)-m_{\rm std}(R_p)=\dim\mathcal S_p-m_{\rm std}(R_p)\ \Longrightarrow\ \boxed{\ \mathrm{def}_p=-m_{\rm std}(R_p)\ }$$
> (GR-UB の等号 = 障害ゼロを併用)。∎

**★ 追補 C への訂正**: 追補 C §2 の【PLC-GAP-1】(「P-PL-5′b は閉形式 × NORM-1 の合成予言で分離不能」)は**降格**。NORM-1 が定理なら、$\mathrm{def}_p=-\lfloor\frac{p-1}3\rfloor$ の経験入力は **$\dim R_p=p-1$ のスカラー 1 個だけ**。ただし **GR-UB の等号($p\ge11$ での障害ゼロ)は依然として未検定** ⟹ 留保は「NORM-1 の未検定」から「**持ち上げ障害の未検定**」へ**移動**した(消えてはいない)。

## 2.4 ⚠ 編纂への影響(悪い知らせを先に)

- 「野生帯完全会計」の証拠力は**下がる**: 会計恒等式のうち $\le$ は定理・$m_{\rm std}$ 加法性も定理 ⟹ **測定が独自に買ったのは「障害ゼロ」1 ビット × 2 段**。
- しかしその 1 ビットこそ v6 が順位 1 に置いた量 ⟹ **v6 の狙いは正しく、既に部分的に当たっていた**。
- ⟹ 編纂は「完全会計」を**「障害ゼロの実測(2 段)+ 会計恒等式(定理)」**と分解して書く(§7.2)。

---

# §3 開扉の検分

## 3.1 CH-1 FILT-LIFT — ★ **紙へ再スコープ**(発注 GR-UB-PF)

- **不要になった部分**: $(5,5)$・$(7,7)$ の per-step 障害測定(§2.2 により残差ゼロが全段無障害を強制)。
- **残る仕事(紙)**: ① GR-UB の $\ker L_k=\mathcal S_{k+1}$ 同一視の厳密化(【GR-GAP-1】)。② $L_k$ の明示形($u$ の指数和 = hexagon 語の $\theta,\tau$-軌道和)を書き下す。
- **残る仕事(機械・安い)**: $p=11$ で **群を作らずに** $\dim\ker L_p$ を Lie 側で計算し、$\mathcal S_p^{\rm group}$ の予言 $m_{\rm std}(\Lambda_{11}/R_{11})$ と突合 ⟹ JAC-CHK-2(追補 C §2.1)と**同乗できる**。
- ⟹ **順位 1 の座は維持するが、費用は「分の機械」から「紙+既発注への相乗り」へ落ちる。**

## 3.2 CH-5 E2/E3 繊維狩り — ▲ **昇格**(閉じた公式で安くなる)

> ### 命題候補 **FIB-COUNT**(candidate・本章)
> $B_3=\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle$。有限群 $G$ に対し
> $$\boxed{\ \#\{N\trianglelefteq B_3:\ B_3/N\cong G\}=\frac{\#\{(a,b)\in G^2:\ \langle a,b\rangle=G,\ aba=bab\}}{\lvert\mathrm{Aut}\,G\rvert}\ }$$
> **証明**: 全射 $B_3\to G$ ↔ braid 関係を満たす生成対。二つの全射が同じ核 $\iff$ $\mathrm{Aut}(G)$ で移り合う(自由作用)。∎
> **窓条件**: $N\le PB_3$ $\iff$ $(a,b)$ が $G\twoheadrightarrow S_3$ で標準互換に落ちる ⟹ **$a$ を「$S_3$ で互換に落ちる元」に制限できる**(強い枝刈り)。
> **コスト**: 共役類代表で $a$ を走らせ $\lvert C\rvert$ 倍 ⟹ $O(\#\text{classes}\times\lvert G\rvert)$。$\lvert G\rvert\le10^5$ なら**秒〜分**。
> **⟹ v6 の「中(設計次第)」は過大見積り。SmallGroups 掃引として実装係に即出せる。**

**★ 発注 FIB-SWEEP(仕様)**: 位数 $\le N_{\max}$(まず $2000$、次に $S_3$ 商を持つ既知族)の群 $G$ について上式で繊維サイズを算出し、**$\ge3$ を全報告**。カナリア: 既知の繊維サイズ $\le2$ 域(指数 $\le1000$)を再現。**IF-FIRST 凍結**: 「掃引域で $\ge3$ はゼロ」を予言(v6 の既測傾向の外挿)。

## 3.3 CH-4 h^cen/χ 扉 — ★ **定義問題は既決**(委嘱は不要)

**正典照合の結果**(`docs/week1-定義ノート.md` §2・2026-07-25 注記、逐語):
> 「c ∉ N の対象(M₅ 等)では近道が壊れる(**定理は無傷**)— θ/τ は自由群の**語レベル**で適用してから φ で評価すること。」

⟹ **gentle GTSh の述語は $c\notin N$ で定義済**(壊れるのは商上評価の近道だけ)。しかも $M_5$ という**実物が既に工房内にある**。⟹ v6 の「(i) 数学者委嘱: L3 層の意味論の確定」は**既に済んでいる**。

> ### 命題候補 **AB-2J**(candidate・本章 — v6 の ab 会計の厳密形)
> $N\trianglelefteq B_3$、$N\le PB_3$、$G=B_3/N$ 有限。$B_3^{\rm ab}=\mathbf Z$($\sigma_i\mapsto1$)、$PB_3$ の像 $=2\mathbf Z$($PB_3$ = 指数和が偶の元)⟹
> $$\boxed{\ G^{\rm ab}=C_{2j}\ \ (\exists j\ge1)\ ;\quad c\in N\Longrightarrow 6\in\mathrm{im}(N)\Longrightarrow G^{\rm ab}\in\{C_2,C_6\}\ }$$
> **逆は不成立**($G^{\rm ab}\in\{C_2,C_6\}$ は $6\in\mathrm{im}(N)$ を言うだけで $c\in N$ を言わない)⟹ **G1 は $c\in N$ より真に弱い**。∎

⟹ **χ 情報($C_{2j}$, $j\nmid3$)の唯一の再入口は「$c\notin N$ かつ $j\nmid3$」窓**で確定。そして

> ### ★ 再スコープ: **CH-4 の第一手は「表読み」**
> 既測の **h^cen 層 24 個**(地図 §軸(iv))について $G^{\rm ab}=C_{2j}$ の $j$ を読むだけ。**T-1(c∉N への checker 発射禁止)は $G^{\rm ab}$ の読み取りを妨げない**(述語評価ではない)⟹ **認可請求なしで撃てる**。
> **IF-FIRST 凍結**: 「h^cen 24 個の $j$ はすべて $j\mid3$(= ab は $C_2$ か $C_6$)」を予言。**外れ($j\nmid3$ が出る)= χ 扉の実在する入口が既測データ内にあった** ⟹ その時点で T-1 解除の認可請求に**実物の根拠**がつく。

## 3.4 CH-3 三格子照合 — 是認(変更なし)

SAT-JOIN 規約(N-4 の共同飽和)と整合。追加の紙仕事なし。順位は中位で妥当。

---

# §4 実現間の乖離(v6 §4)の検分 — パリティ罠・(37,32)・三扉

## 4.1 ★★ パリティ罠の検分 — **v6 の自己捕獲は正しい**(独立に確認)

$p$ 奇、$\Delta=\mathrm{Gal}(\mathbb Q(\mu_p)/\mathbb Q)$、$A=\mathrm{Cl}(\mathbb Q(\mu_p))\otimes\mathbf Z_p=\bigoplus_i A^{(i)}$($\omega^i$-固有空間)。

| 事象 | 固有空間 | 根拠 |
|---|---|---|
| $p\mid B_{p-m}$($m$ 奇 ⟹ $p-m$ 偶) | $A^{(1-(p-m))}=A^{(m)}$、$m$ **奇** | Herbrand–Ribet($1-p+m\equiv m\ \mathrm{mod}\ (p-1)$) |
| $\kappa_m$(Soulé)の mod-$p$ 退化 | $H^2(\mathbb Z[1/p],\mathbf Z_p(m))\leftrightarrow A^{(1-m)}$、$1-m$ **偶** | Quillen–Lichtenbaum / $K_{2m-2}(\mathbf Z)$・Vandiver 域 |

**反射(Spiegelungssatz)は片道**: $A^{(\text{偶})}\ne0\Rightarrow A^{(\text{奇})}\ne0$ のみ。逆は成り立たない(非正則素数は $\sim39\%$ で頻出・Vandiver 反例は $2^{31}$ まで皆無)。
⟹ **非正則対から $\kappa$ の死は導けない。** v6 の捕獲は正しく、私も同じ穴に落ちうる形だった。**規約化に賛成**(§4.2)。

## 4.2 ★★★ 規約案 **PARITY-EIG**(規約台帳 pending へ・司令塔レビュー請う)

> $$\boxed{\ p\mid B_{p-m}\ (m\ \text{奇})\ \textbf{は奇固有空間}\ A^{(m)}\ne0\ \textbf{(Herbrand–Ribet)};\ \kappa_m\ \textbf{の mod-}p\ \textbf{退化は偶固有空間}\ A^{(1-m)}\ \textbf{(Vandiver}/K_{4k}\ \textbf{域)}.\ \textbf{Spiegelung は偶}\Rightarrow\textbf{奇の片道のみ ⟹ 非正則対から }\kappa\ \textbf{の死は導けない。}}$$
> **運用**: 反例案に「非正則対 $(p,k)$ だから算術スロットが空になる」型の推論が現れたら、**固有空間のパリティを書かせる**。書けないなら棄却。

## 4.3 ▼ CH-7 FROB-SHADOW — **mod $p$ の狩りは恒真式(空)**

> ### 命題候補 **LOC-TAUT**(candidate・本章)
> Kummer 合同 + Kubota–Leopoldt: $m$ 奇に対し $n:=p-m$ とおくと $1-n\equiv m\ (p-1)$ ゆえ
> $$\zeta_p(m)\ \equiv\ L_p(1-n,\omega^{1-m})\ =\ -(1-p^{\,n-1})\frac{B_n}{n}\ \equiv\ -\frac{B_{p-m}}{p-m}\pmod p$$
> $$\Longrightarrow\quad\boxed{\ \zeta_p(m)\equiv0\ (\mathrm{mod}\ p)\iff p\mid B_{p-m}\iff (p,\,p-m)\ \textbf{が非正則対}\ }$$
> ∎(自前導出・要 pin は正規化のみ)

⟹ v6 の「**予言外の局所退化(反射対にない $(k,p)$ での零)**」は **mod $p$ では存在し得ない**(同値だから)。⟹ CH-7 の「新しい狩り」は空。
- **$(37,32)$ の計算は正しい**: $37-5=32$、$(37,32)$ は古典的な最初の非正則対 ⟹ $\zeta_{37}(5)\equiv0\ (37)$ ✔。
- **残る価値**: 局所列を**辞書として常設**すること(v6 の「空振りの価値」の方)。狩場としては **mod $p^2$**(= 既存の P2-STRIKE / KELL-DECIDE 領域)か**深さ $\ge2$**(= CH-9)へ移す。
- ⟹ **順位 2 から降格。ただし「辞書の常設」は編纂に載せる。**

## 4.4 ★★★ $(37,32)$ の読みの**訂正** — 「大域満杯・局所零」ではなく**飽和欠損(指数)**

**v6 の読み**:「大域算術像は満杯・局所 Frobenius 影の重み 5 座標だけが零」。**これは危うい**。

**検分**: $m=5$ 奇。$H^2(\mathbb Z[1/37],\mathbf Z_{37}(5))\leftrightarrow A^{(1-5)}=A^{(32)}$(**偶** ⟹ Vandiver 域・$p=37$ は検証済で $0$)⟹ $\dim H^1(\mathbb Z[1/37],\mathbf Z_{37}(5))=1$。さらに Vandiver ⟹ 局所化 $H^1(\mathbb Z[1/p],\cdot)\to H^1(\mathbb Q_p,\cdot)$ は**単射**(厳 Selmer 群が消える)。
⟹ もし $\zeta_{37}(5)\equiv0\ (37)$ が「$\kappa_5$ の局所像が mod 37 で零」を意味するなら、単射性より **$\kappa_5\equiv0\ (\mathrm{mod}\ 37)$**。しかし $H^1$ は 1 次元で**空ではない** ⟹ 正しい結論は

> ### ★★ 訂正された読み(candidate)
> $$\boxed{\ \textbf{大域スロットは 1 次元のまま「満杯」だが、円分元 }\kappa_5\ \textbf{は生成元ではなく }37\ \textbf{倍だけ深い} — [\,H^1:\mathbf Z_p\kappa_5\,]\equiv0\ (37)\ }$$
> すなわち **$(37,32)$ は「欠損(gap)」でも「単なる局所零」でもなく、飽和欠損(index/saturation defect)**。岩澤主予想(Mazur–Wiles)で「この指数 $=$ $p$ 進 $L$ 値」が本来の内容であり、$\zeta_{37}(5)\equiv0$ はその**指数が $p$ で割れる**ことの言い換え。

> ### ★★★ 新札 **SAT-37** — 窓側の予言(IF-FIRST 凍結)
> **観測量**: $p=37$ の窓における **$[\,GT(N):\mathrm{im}\,\mathrm{Ih}\,]$**(LADDER-SAT 型の飽和欠損)の重み 5 成分。
> $$\boxed{\ \textbf{予言 P-SAT-37}:\ \textbf{重み }5\ \textbf{の算術スロットを見る }p=37\ \textbf{窓では、算術像の指数が }37\ \textbf{で割れる。}}$$
> **対照**: $p=31,41,43$(正則)では指数 $37$-可除なし。$p=59$($(59,44)$ ⟹ $m=15$)・$p=67$($(67,58)$ ⟹ $m=9$)は**重みを変えた同型予言**。
> **なぜ良い狩りか**: ①**当たり外れが両方情報**(指数は測れる量・現行の会計装置がそのまま使える)②反例側の主張ではなく**井原の像の細かさ**の主張 ⟹ 全射性予想と**矛盾しない**(=「安全な較正」)が、**装置が算術を読めていること**の初の実証になる。
> **【文献要請 HUNT-LIT-1】**(一点 pin): 「$[\,H^1(\mathbb Z[1/p],\mathbf Z_p(m)):\mathbf Z_p\,c(m)\,]$ が $L_p(m,\omega^{1-m})$ で測られる」の**正確な形と仮定**(Vandiver 依存か否か・$m$ 奇の範囲)。出所つきの 1 定理でよい。
> **【文献要請 HUNT-LIT-2】**: 「crystalline Frobenius の窓像の深さ 1 重み $m$ 座標 $=\zeta_p(m)$(正規化込み)」の一点 pin(v6 が自ら要 pin と申告した箇所)。

## 4.5 CH-8 κ-death 台帳・CH-9 CUP-METER — 是認(修正 1 点)

- **CH-8**: パリティ罠訂正後の形($p\mid\#K_{2m-2}(\mathbf Z)$ = 偶固有空間)は §4.1 と一致 ✔。「住人なし・恒久監視」は妥当。**ただし** $m=3$ の恒久生存は Kurihara の $c(1)$ 生成(工房 pin)で**深さ 1 のみ** — 深さ $\ge2$ には及ばない旨を明記すべき。
- **CH-9**: §4.3 で CH-7 の狩り機能が消えた分、**CH-9 が「局所側の唯一の非自明な狩場」に繰り上がる**。ただし設計は重い(cup の正規化 pin が全て)⟹ 順位は中位のまま、**ただし理由が変わった**(代替がなくなった)。

---

# §5 6 実験の仕様検分 — 実装係に出せる粒度か

| # | 札 | 実装係に出せるか | 不足している pin / 修正 |
|---|---|---|---|
| 1 | **CH-1 FILT-LIFT** | ▲ **紙が先**(§3.1)。機械部分は JAC-CHK-2 に相乗り | $\ker L_k=\mathcal S_{k+1}$ の同一視(【GR-GAP-1】)= CV-9 型 ⟹ falsifier 判読 |
| 2 | **CH-7 FROB-SHADOW** | ○ 計算自体は秒(整数合同)だが**測る意味がない**(§4.3) | 狩りとしては棄却・辞書として常設・SAT-37 へ振替 |
| 3 | **CH-6 INV-CENSUS** | △ **冗長**(§5.3) | サイズ不一致窓に限定すれば非冗長 |
| 4 | **CH-2 M-SWEEP** | △ **一様性は定理**(§5.4) | 残る問い =「$\lambda$-スペクトル」= 既存 cert の表読み |
| 5 | **CH-5 E2/E3 繊維** | ★ ○ **即出せる**(§3.2 の FIB-COUNT で仕様完結) | なし。カナリア込みで発注可 |
| 6 | **CH-4 h^cen/χ 扉** | ★ ○ **表読みなら即**(§3.3) | T-1 は $G^{\rm ab}$ 読み取りを妨げない |

## 5.3 CH-6 の冗長性(詳細)

閉じた扉 1(§1.1)より、**$\lvert GT(N)\rvert=\lvert$算術予測$\rvert$ の窓では全元が算術** ⟹ 対合も自動的に算術。⟹ 「軌道外対合」は**サイズが一致しない窓でしか存在し得ない**。現行データ(梯子は LADDER-SAT で飽和・壁/屋根はサイズ一致)ではほぼ空。
**さらに**: 有限商 $GT(N)$ の対合は $\widehat{GT}$ の対合に**持ち上がるとは限らない**(捩れは持ち上がらない)⟹ Artin–Schreier は「探す場所のヒューリスティック」であって推論機構ではない。**v6 の的中欄「最剛の B 型候補」は言い過ぎ** — 正しくは「非全射の証人の一種」。
⟹ **再スコープ**: 「**飽和欠損のある窓**の対合を見る」= **SAT-37 と合流させる**(そこでは指数 $>1$ が予言されている)。

## 5.4 CH-2 の一様性(詳細)

> ### 命題候補 **M-COSET**(candidate・本章)
> $\lambda=2m+1$ は合成で乗法的 ⟹ $m=0$ 部分 $GT_0(N)=\{\lambda=1\}$ は部分モノイド、各 $m$ 層に左から作用し層を保つ。**$GT(N)$ が群ならば**、同一層の $z,z'$ に対し $z'z^{-1}\in GT_0$ ⟹
> $$\boxed{\ \textbf{非空な }m\ \textbf{層はすべて }GT_0(N)\ \textbf{の剰余類 ⟹ サイズが等しい}\ }$$
> ∎(群でない場合は左簡約性で十分)

⟹ v6 の「Lie 模型は $m$-一様を予言 ⟹ 野生段の $m$-非一様 = 新種」は、**$m$-非一様が起きたら $GT(N)$ が群でない**ことを意味する(それはそれで大事件だが、狙いが変わる)。⟹ **M-SWEEP の実質的な内容は「$\lambda$-スペクトル $\mathrm{im}(GT(N)\to(\mathbf Z/N_{\rm ord})^\times)$」**で、これは既存 cert から**表読みできる可能性が高い**。⟹ 費用 $\times(p-1)$ の掃引は**後回し**。

---

# §6 順位の改訂提案(司令塔裁定を請う)

| 新順位 | 実験 | 費用 | 空振りが買う確信 | v6 比 |
|---|---|---|---|---|
| **1** | **GR-UB-PF**(§2 の紙 + $\ker L_k$ 同一視の厳密化 + falsifier 判読) | 紙 | **会計恒等式が定理になり、測定が買った 1 ビット(障害ゼロ)が孤立して見える** ⟹ 編纂の主張が正確になる | CH-1 の心臓を紙へ |
| **2** | **FIB-SWEEP**(§3.2・繊維サイズ $\ge3$ 掃引) | 秒〜分 | 「窓繊維サイズ $\le2$」の実効域が一気に拡大 ⟹ exotic 不在会計の完成度 | CH-5 を 5→2 へ |
| **3** | **h^cen-AB**(§3.3・既測 24 個の $G^{\rm ab}$ 読み) | 表読み | χ 扉の入口が既測データ内に**ない**ことの確定 ⟹ TWIST-6 の実効域拡大 | CH-4 を 6→3 へ |
| **4** | **SAT-37**(§4.4・飽和欠損の窓側予言) | 設計 1 頁 + 既存会計 | 「装置は算術の細かさを読めていない」が確定 = 計器の分解能の下界 | **新札** |
| **5** | **CH-3 三格子照合** | 分〜時間 | 格子アーティファクト仮説がさらに窮屈に | 据置 |
| **6** | **CH-9 CUP-METER**(設計委嘱) | 重 | M-S 検証域の自前拡張 | 据置(理由変化: 局所側の唯一の狩場) |
| — | CH-7 / CH-6 / CH-2 | — | **辞書・冗長・定理**として編纂に載せるが実験列からは外す | 降格 3 件 |

**全空振り世界の記述(v6 §6 末の更新形)**: 上記 6 件が全空振りなら、閉じるのは【会計恒等式・繊維多重度・χ 扉・計器分解能・格子・深さ 2 の一部】。**残る開放扉は Vandiver 域(CH-8)・M-S 域外(CH-9 の本体)・塔成長(CH-10)・そして本章が新設した「持ち上げ障害の $p\ge11$ 未検定」(【GR-GAP-1】系)の四つ**。

---

# §7 編纂への織り込み(見立て = 三点セット)

## 7.1 構成(裁定 791 ①の実装)

```
見立て(便 114)
├─ 第 1 部 現在の証拠      = 相 2 章(既納品: CB-RECON / cone / PL / P2 / T2 / Kellner)
├─ 第 2 部 残る扉          = 本章 §1(閉扉 4 枚・証明つき)+ §3–§5(開扉の正確な形)
└─ 第 3 部 扉を閉じる実験列 = 本章 §6(順位・費用・空振りが買う確信)
```

## 7.2 ★ PL 節の**言い換え**(§2 の帰結・必須)

> **旧**: 「野生帯は完全会計 — 超過なし・痩せは辞書補正で尽きる」
> **新**:
> $$\boxed{\ \textbf{会計の不等式 }(\mathrm{def}\le0)\ \textbf{と痩せ幅の恒等式 }(\mathrm{def}_p=-m_{\rm std}(R_p))\ \textbf{はいずれも定理}(\textbf{本章 }\S2)\textbf{。}}$$
> $$\boxed{\ \textbf{測定が買ったのは「持ち上げ障害ゼロ」の }1\ \textbf{ビット}\times2\ \textbf{段}(p=5,7)\textbf{と、}\dim R_p=p-1\ \textbf{の }4\ \textbf{点。}}$$
> $$\boxed{\ \textbf{痩せ幅 }\lfloor(p-1)/3\rfloor\ \textbf{は }S_3\ \textbf{の不変式論だけで決まる — 算術は入っていない(追補 C }\S1.4)\textbf{。}}$$

**★ 狩猟章にとっての含意**: post-Lazard 帯の痩せが純表現論なら、そこに算術情報は乗っていない ⟹ **反例の棲息地としての期待度は低い**。⟹ 狩りの重心は **§4 の実現間乖離(SAT-37 / CH-9)と §3.2 の繊維**へ移すべき。

## 7.3 「空振りの価値」の様式(研究者教義の術語化 — v6 §6 末を継承)

各実験は「的中 = 反例側の前進」と「空振り = **名指しの扉を 1 行消す**」が対。編纂では**扉の表を先に置き、実験列がその表のどの行を消すかを矢印で示す**(v6 の設計原理をそのまま採用・本章はその表を証明つきに置き換えた)。

---

# §8 【GAP】・帰属・novelty grep

| # | 内容 | 重さ |
|---|---|---|
| **【GR-GAP-1】** ★新 | $\ker L_k=\mathcal S_{k+1}$ の同一視(GR-UB と会計の**仕様同一性**)⟹ CV-9 判読対象 | ★ 中 |
| **【GR-GAP-2】** ★新 | GR-UB の等号(持ち上げ障害ゼロ)は $p=5,7$ のみ実測・$p\ge11$ 未検定 | 中 |
| **【HUNT-GAP-1】** ★新 | SAT-37 の岩澤側(指数 $=L_p$ 値)は【文献要請 HUNT-LIT-1】待ち | 中 |
| **【HUNT-GAP-2】** ★新 | Frobenius 影 $=\zeta_p(m)$ の正規化は【文献要請 HUNT-LIT-2】待ち | 中 |
| **【HUNT-GAP-3】** ★新 | CRT-INJ の**全射性**は UNKNOWN(合成位数窓に新情報が「ある」かは未決) | 小 |
| **【PLC-GAP-1】** | ★ **降格**(§2.3 で NORM-1 が定理化)⟹ 留保は「持ち上げ障害の未検定」へ移動 = 【GR-GAP-2】 | 降格 |

**帰属**: 発案・作戦図・パリティ罠の自己捕獲・$M_{p^3}$ no-go の着想・6 実験の骨格 = **発案係(v6・c39ebfc)**。委嘱 = 司令塔(裁定 791)。$(37,32)$ の元の読み = 発案係、**その訂正(飽和欠損)= 本章**。
本章の新規部分 = **命題候補 GR-UB / STD-DIM / NORM-1 の定理化** / **CRT-INJ(扉 2 の修理)** / **COMPACT-COMPLETE(扉 3+4 の統合・強化)** / **MOD-NOGO(扉 5 の修理: $Z\cong\Lambda^2\mathrm{std}\cong\mathrm{sgn}$)** / **AB-2J** / **FIB-COUNT と発注 FIB-SWEEP** / **M-COSET** / **LOC-TAUT(CH-7 の恒真性)** / **$(37,32)$ の飽和欠損読みと新札 SAT-37・予言 P-SAT-37** / **規約案 PARITY-EIG** / **順位改訂 §6** / **編纂三点セット §7**。

**novelty grep**(`docs/` `provenance/` 全域): `GR-UB` `STD-DIM` `CRT-INJ` `COMPACT-COMPLETE` `MOD-NOGO` `AB-2J` `FIB-COUNT` `M-COSET` `LOC-TAUT` `SAT-37` `PARITY-EIG` `Spiegelung` = **0 hit(本章初出)**。`パリティ罠` = v6 ほか既在(**本章はその規約化**)。`Herbrand` `Vandiver` = 既在(cone/p2/ribet 系)。`反射定理` = `ideas_resonance_addresses_v1.md` 既在(本章の §4.1 とは別文脈)。

**検算コマンド**(裁定 668 拡張):
```bash
# LOC-TAUT の数値確認: 非正則対 (37,32) ⟺ 37 | B_32 ⟺ zeta_37(5) ≡ 0 (37)
python -c "
from sympy import bernoulli, Rational
for (p,k) in [(37,32),(59,44),(67,58),(31,None),(41,None)]:
    if k is None:
        print(p,'regular control: ', [ (kk, bernoulli(kk).p % p == 0) for kk in range(2,p-1,2)].count((0,True)))
    else:
        B=bernoulli(k); print('p=%d k=%d  m=p-k=%d  p|num(B_k)? %s'%(p,k,p-k, B.p % p == 0))
"
# STD-DIM の恒等確認: m_std(Lambda_k) == (Witt(2,k) - tr(tau|Lambda_k))/3
```
