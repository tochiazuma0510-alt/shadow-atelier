# ENT-TARGETS v1 — 反相関対の構成原理と候補(裁定 849・4R B-1/M-2 の発案問題化)

**状態札: `candidate 札 / 発案係(ideator)起草 / Sol 未監査 / 走行ゼロ(見積りは既測値と正典定理からの紙算のみ)/ 封印非接触 / 判定語なし / DOMAIN-PIN 様式 / EXHAUST 遵守(「唯一」不使用・原理と候補は現在庫の走査であり網羅主張なし)/ 数学者検分前提の candidate 格`**

- 委嘱: 裁定 849。前提 = 4R B-1(窓側共通商は発火に**不利** — 向きの反転)・M-2(発火条件 $\lvert Q_A^{\rm lb}\rvert>$ 窓側圧縮率)・`p4_design_bundle_v1_review_v1_addendum_a.md`(ENT-VAC/ENT-MECH)・`ihnec_v1.md` §6.3-6.4(命題 ROOF・定理 SPLIT-NULL の証明再読)・見立て v1.4 §3.1。
- **718④ 記録**: 本札の中心命題(§0)と SPLIT-NULL″(「fake 検出は entangled 屋根に限る」)の**見かけの衝突を検出し整理した**(§0.3 — 観測チャネルが別物・矛盾なし)。ENT-MECH との整合検算済(分裂屋根では発火 ⟺ $\lvert Q_A\rvert>\lvert\chi\text{-共有}\rvert$ — 同じ式に着地)。

---

## §0 核心の紙問題への答え — SPLIT-NULL の正確な射程(委嘱の指定問題)

### 0.1 再読の結果(前件と結論の帰属)

定理 SPLIT-NULL(ihnec §6.4)の**前件は純粋に窓側**($PB_3/K^{(n)}$ と $PB_3/N'$ に共通の非自明商なし)。証明は「共通商 $=1$」と hexagon/charming の成分分解だけを使い、**結論が拘束するのは genuine 側 $X$ のみ**:
$$X=\mathrm{GT}(M)\ \cong\ \mathrm{GT}(N_1)\times_{\chi\text{-水準}}\mathrm{GT}(N_2)\qquad(\text{ROOF(4) 型・}\chi\text{-fiber 積で最大})$$
**算術側 $A$ には一言も触れない。** 一方 ENT-VAC の前件は算術側($Q_A$ 自明)だが、$Q_A$ は円分部分を常に含む(W-30)ので実質空。⟹ falsifier B-3 の指摘どおり、**「窓側 split ∧ 算術側 entangled」は両定理のどちらの前件にも入らない未整理地帯として実在する**。

### 0.2 ★ 未整理地帯の解(命題候補 ENT-SPLIT-SCOPE)

> ### 命題候補 **ENT-SPLIT-SCOPE**(candidate・本札・数学者検分対象)
> 分裂屋根($X=\mathrm{GT}_1\times_\chi\mathrm{GT}_2$・CRT-INJ で $\lvert X\rvert=\lvert\mathrm{GT}(N)\rvert$)で両窓が個別飽和なら、$A=A_1\times_{Q_A}A_2$(Goursat)と併せ
> $$\lvert X\setminus A\rvert\ =\ \lvert X\rvert\Bigl(1-\frac{\lvert\chi\text{-共有}\rvert}{\lvert Q_A\rvert}\Bigr)\qquad\Longrightarrow\qquad \boxed{\ \textbf{発火}\iff \lvert Q_A\rvert>\lvert\chi\text{-共有}\rvert\iff L_1\cap L_2\ \textbf{が非円分部分体を含む}\ }$$
> **⟹ 窓側 split は無害どころか有利**($X$ を χ-fiber 積の最大値まで膨らませる)。殺すのは「算術共有が円分に限られること」だけ。ENT-MECH と整合(分裂時 $\lvert\mathrm{GT}(N)\rvert=\lvert\mathrm{GT}_1\rvert\lvert\mathrm{GT}_2\rvert/\lvert\chi\rvert$ を代入すると同値)。

### 0.3 SPLIT-NULL″ との整理(衝突ではない — チャネルが別)

SPLIT-NULL″「fake を検出しうる細分は entangled 屋根に限る」は **reduction 像チャネル**($\mathrm{Im}\,R_{M,K}$ を削って $K^{(n)}$ 側の fake を炙る・ML-ODD 量化の経路)の言明。ENT 観測量は **joint 算術性チャネル**($M$ 上の $X\setminus A$ — $M$ 自身の非全射証人)であり別物。
$$\boxed{\ \textbf{972 屋根はチャネル 1 では死(証明済)・チャネル 2 では「非円分共有があるか」次第で生きている}\ }$$

---

## §1 反相関の構成原理(候補 3 本 — 網羅主張なし)

| # | 原理 | 機構 | 実現族 |
|---|---|---|---|
| **P1 グラフ原理(鏡映)** | 同一の $\gamma$ が両座標に作用し、第二座標が第一座標の**固定変換**で決まる($s_{\iota(N)}(\gamma)=\Phi(s_N(\gamma))$ — 補題候補 A-GRAPH・§3)⟹ $A$ = 捻れグラフ ⟹ $\lvert A\rvert\le\lvert A_1\rvert$: **$Q_A$ = 算術群全体 = 最大**。窓側: chiral なら $N\ne\iota(N)$ で交差は真に細かい | **鏡映対 $(N,\iota(N))$**(chiral)— census L2 15 対・帯 5 対 |
| **P2 κ-共有原理(クロス族)** | 窓側は単純因子で共通商を強制的に潰し(split = 無害・§0.2)、算術側で**同じ Kummer 座標**(同じ $u$-torsor・同水準)を共有させる ⟹ $Q_A\supsetneq\chi$-共有 | **$K^{(9)}\times N_{S4}$(972 屋根の復活形)** — 両者の算術が同じ $[u]_9$ に駆動されるか、が発火ビット |
| **P3 同族禁止(負の原理)** | 同一塔内の対(dihedral×dihedral 等)は、共有算術($\zeta$・$u$-塔)を**窓の共通商が先取り**する(塔の透明性)⟹ $Q_A\approx$ 窓側共有 ⟹ 発火不能の見込み | dihedral×dihedral は**対照(予言 null)**へ回す |

## §2 候補対(現在庫走査・粗見積り・序数評価)

記号: 圧縮率 $C:=\lvert\mathrm{GT}_1\rvert\lvert\mathrm{GT}_2\rvert/\lvert\mathrm{GT}(N)\rvert$・発火 ⟺ $\lvert Q_A^{\rm lb}\rvert>C$。

| 対 | 原理 | $C$(窓側圧縮率) | $Q_A^{\rm lb}$ | 発火見込み(序数) | 較正状態($A^{\rm ub}$ に使える既測) | 費用 |
|---|---|---|---|---|---|---|
| **(b) $K^{(9)}\times N_{S4}$(972 復活)** | P2 | $108\cdot54/972=\mathbf 6$(**実測値のみで確定**) | 円分 $=6$(無料)+**$u_9$-共有なら $\times9$(+ε 共有で $\times2$)$=54$** | ★ **1 位**: 発火 ⟺ $u$-共有ビット。branch 表: $\lvert Q_A\rvert=6\Rightarrow\lvert X\setminus A\rvert=0$ / $18\Rightarrow648$ / $54\Rightarrow\mathbf{864}$ | $K^{(9)}$: **飽和定理級**(U-11/Θ₉)・$N_{S4}$: 1 ビット帰着済($\mathrm{ord}[u^{-1}]_9$)— **$u_9$ 実測状態は registry 確認要** | ★ **最小**: GT 新走行ゼロ — 「$f_P$-座標が $K^{(9)}$ と同じ $\kappa_9$ を経由するか」の**指標同一性監査**(amendment_5prime の (5′_b) 橋・oriented torsor 証明書技術の転用) |
| **(a) 鏡映対の交差 $N\cap\iota(N)$(最小 chiral 対 = 504 帯から)** | P1 | $\lvert\mathrm{GT}\rvert^2/\lvert\mathrm{GT}(N\cap\iota N)\rvert$($\mathrm{GT}(N\cap\iota N)$ が**新規測定 1 本**) | **$\lvert A_1\rvert$(グラフ — A-GRAPH 成立なら)** | **2 位**: A-GRAPH 下で発火 ⟺ $\boxed{\lvert\mathrm{GT}(N\cap\iota N)\rvert>\lvert\mathrm{GT}(N)\rvert}$ — **飽和仮定不要**($\lvert A\rvert\le\lvert\mathrm{GT}_1\rvert$ が無条件上界)| 単窓 GT は wall-campaign cert(witness 水準)— **飽和不要が本対の強み** | 中: 交差窓(指数 ~$504^2/\lvert$共通商$\rvert$)の GT 1 本(Ξ 走査圏内の見込み) |
| **(d) 486 鏡映対の交差** | P1 | 同上(486 版) | 同上 | 3 位(504 と同型・ORB/掌性の既測が最厚) | witness word+ORB 済 | 中 |
| **(c) $K^{(9)}\times K^{(12)}$(現行本命)** | — (P3 該当) | 共通商 $K^{(3)}{=}K^{(6)}$ が**大** ⟹ $C$ 大 | 円分+$u$-塔 — **窓共有が先取り** | ★ **予言 null ⟹ 対照へ転用**(B-1 の向き反転の帰結 — 検分事項として明示) | 両側 dihedral 系定理 | 小(交差既知) |
| **(e) 帯 chiral 対((1944,826)/(1944,921) 等)× 円分相手** | P1/P2 混成 | 要算出 | 要算出 | 4 位(層 3 掌性の住人 — 算術計器が未整備) | FRAT-CHIR 系 cert | 大(算術側未整備) |

**★ (b) の分岐表が本札の中心成果物**: 全ての数($108,54,6,972$)が実測済みで、未知は $u$-共有ビット 1 個。同 κ なら $\lvert X\setminus A\rvert=864$ = **$M$ 上の genuine 非 joint-算術 shadow の大量予言**(= $M$ の非全射証人候補・井原直撃)/独立なら**厳密 null**(= 「二窓の Kummer 座標は独立」という算術の新事実)。**どちらに転んでも算術構造の決定的情報**。

## §3 補題候補 A-GRAPH(P1 の根拠・数学者検分対象)

> ### 補題候補 **A-GRAPH**(candidate)
> $\iota\in\mathrm{Aut}(B_3)$(鏡映)・$N$ 窓・$\gamma\in G_\mathbb Q$ に対し、$s_{\iota(N)}(\gamma)=\Phi\bigl(s_N(c_\infty\gamma c_\infty)\bigr)$($\Phi$ = ι-移送の固定同型・$c_\infty$ = 複素共役)。像の群構造より第二座標は第一座標の**固定元共役+固定同型**で決まり
> $$\lvert A\rvert=\lvert A_1\rvert\qquad(\textbf{捻れグラフ})$$
> **含意**: 発火判定が「交差窓の GT が単窓より真に大きいか」の **1 不等式**に落ち、**飽和較正を要しない**(上界 $\lvert A\rvert\le\lvert\mathrm{GT}_1\rvert$ が無条件)。
> **怪しい点**: groupoid 合成の bookkeeping($s$ は準同型でなく cocycle 的)— $\Phi$ の存在と「固定」性の厳密化が検分の本体。[-1,1]-witness 系(複素共役カナリア v3)が較正 fixture に使える。

## §4 DOMAIN-PIN 表(凍結案)

| 述語 | 関手 | 比較射 | chi_semantics | factor_filter | 陽含意 | 陰含意 |
|---|---|---|---|---|---|---|
| **P-ENT-U9**(対 (b)): $N_{S4}$ の算術 $f_P$-座標は $K^{(9)}$ と同一の $\kappa_9$ を経由する | 算術像の指標分解 | (5′_b) 橋(oriented torsor 証明書) | n/a(Kummer 指標) | 指標の族を全列挙(落とし なし) | 同一 ⟹ $Q_A\ge54$ ⟹ **864 予言が立つ**(→ QUAR 検疫つき joint 実測へ) | 独立 ⟹ 対 (b) は**厳密 null**(円分先取り)= Kummer 独立性の新事実 |
| **P-ENT-MIR**(対 (a)): $\lvert\mathrm{GT}(N\cap\iota N)\rvert>\lvert\mathrm{GT}(N)\rvert$ | GT 計数 | CRT-INJ | n/a | — | A-GRAPH 下で**非 joint-算術 shadow の存在**(検疫へ) | 等号 ⟹ 交差窓の genuine は ι-対称移送で尽きる = 剛性の新事実 |
| **P-ENT-CTRL**(対 (c)): $X\setminus A=\emptyset$ | 同 P4-1 | 同 | n/a | — | 破れ = P3 原理の反例 = 一級(同族でも発火) | null = P3 の初検証+パイプライン陰性対照 |

## §5 リスク・規律

- (b) の分岐表は「両窓個別飽和」を計数に使う — $N_{S4}$ 飽和未証明につき、報告語は $A^{\rm ub}/A^{\rm lb}$ の**挟み撃ち形**で凍結(飽和は仮定でなく挟みの片側)。
- A-GRAPH 不成立なら P1 系の序数は崩れる(P2 系 (b) は独立に立つ — 二本柱設計)。
- 数値($108/54/6/972$)は cert 台帳からの引用 — v1.4.1 パッチ後の数学者検分で照合(手写し禁止規律に従い、実行段では機械生成で再取得)。
- EXHAUST: 原理 3 本・候補 5 対は現在庫の走査であり網羅でない。「唯一」不使用(grep 自己点検済)。

---

**novelty grep 申告**: ENT-SPLIT-SCOPE・A-GRAPH・P-ENT-U9/MIR/CTRL・「捻れグラフ」・972 復活形 = repo 0 hit(本札初出)。ENT-VAC/ENT-MECH/SPLIT-NULL/ROOF/CRT-INJ = 既在(前提引用)。$u_9$-共有の着想は LG-6(裁定 219「2-群因子 = 不分岐 cusp の Galois 置換」)と M0-M7 線の延長 — 同一視はしない(あちらは機構仮説・こちらは指標同一性の監査可能述語)。
**帰属**: 問題の定式化(向きの反転・発火条件)= falsifier 4R B-1/M-2+Sol M-1 系。ENT-VAC/ENT-MECH = 数学者(追補 A)。本札の新規部分 = §0.2 ENT-SPLIT-SCOPE(未整理地帯の解・「split 無害・円分限定が殺す・非円分共有が発火」)/§0.3 チャネル分離(SPLIT-NULL″ との無矛盾整理)/原理 P1-P3/972 復活形と分岐表($6/18/54\to0/648/864$)/A-GRAPH と飽和不要の鏡映判定式/対 (c) の対照転用提案。
