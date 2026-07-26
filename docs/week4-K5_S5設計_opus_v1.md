# S5 紙上設計 — $K^{(5)}$ 標的 dessin(次数 10・種数 2)の明示モデル探索の設計書 v1.2

2026-07-27 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱**。上位文書: `docs/manifest_k5_v1.md` v1.2(事前登録)・`sol/裁定_29_ben31.md`(工程 ③)・`sol/sol_reply_31_manifest.md` F9(Sol の紙上設計の贈り物)。姉妹文書: `docs/week4-K5_Rule1_v1.md` **v1.3**(凍結 1 候補)。

**v1.1(2026-07-27・便 32 P5 + 裁定 31 の修理)。**
**v1.2(2026-07-27・便 34 F3.3 / 便 35 F5.1 の blocker **R-4** の修理 — 分離条件 **N-0** の追記、(3.3) の $x_0$ 有限前提の明示、副枝 $(N_\infty)$ の **total な分岐表**と正規形 (3.3∞) の新設)。**

## v1.1 → v1.2 差分表(**R-4** — Rule 1 v1.2 §11.1 / 便 34 F3.3 / 便 35 F5.1)

> **v1.1 の欠陥(便 34 F3.3・便 35 F5.1・そのまま受け入れる)**: §3.3.4 の枝 (N) の正規形
> $$ a(x)^2-c_N(x-x_0)^5 = f_6(x)p_2(x)^2 \tag{3.3} $$
> は **$x_0=x(P_0)$ が有限であること**を使っている。ところが枝 (N) の六次モデルには無限遠点が $\infty_+,\infty_-$ の**二つ**あり、$P_0=\infty_-=\iota(P_\infty)$ は $P_0\ne P_\infty$ と両立する。この場合 $x_0$ は存在せず (3.3) は**書けない**。分離条件表 N-1〜N-6 にこの条件(**N-0**)が無かったため、**(3.3) を discovery engine に使うと (N$_{\rm aff}$) だけを全 (N) と誤認して候補を落とす**。
>
> **便 35 F5.1 が要求した水準**: 「少なくとも N-0 を明記し、(N$_\infty$) は別 ansatz で探索するか、その stratum を閉じられなければ **BRIDGE-UNKNOWN** とする **total な分岐表**が必要である。」— v1.2 はこれを満たす。**さらに、(N$_\infty$) の排除証明書は撤回された**(Rule 1 v1.3 §11 論点 7)ので、**この欠品を「起こらない枝だから」と延期する道はない**。

| # | 箇所 | v1.1 | v1.2 | 出典 |
|---|---|---|---|---|
| G1 | §3.3.4 分離条件表 | N-1〜N-6 | **N-0($P_0\ne\iota(P_\infty)$)を先頭に追加**。破れると何が起きるかを明記((3.3) が書けない・norm が定数化する) | 便 34 F3.3 |
| G2 | §3.3.4 (3.3) | 前提が暗黙 | **$x_0=x(P_0)\in\mathbb Q$ が有限であることを前提として明示**。$\deg a=5$・$\deg p_2=2$ の根拠も (N$_{\rm aff}$) 限定であることを明記 | 便 34 F3.3 |
| G3 | **§3.3.5(新設)** | — | **副枝 (N$_\infty$) の正規形**: **命題 S5-3∞**((3.3∞): $a^2-f_6p^2=\hat c_\mu\in\mathbb Q^\times$ = **多項式 Pell 型**、$\deg a=5$、$\deg p=2$、$[x^5]a=[x^2]p\ne0$)。**これは design count でなく global な同値**である。期待次元 2 が幾何的 stratum の期待次元と一致することも確認(**いずれも期待次元/design count であって証明された stratum 次元ではない — 便 36 F2.2 で降格**) | 本便 |
| G4 | **§3.3.6(新設)** | — | **total な分岐表**(3 枝 × 状態札 × 探索器の所在 × 閉じられない場合の処置 = BRIDGE-UNKNOWN) | 便 35 F5.1 |
| G5 | §6.2 | 命題 S5-4($c$ の平方類が (P1) を決める) | **命題 S5-4∞ を追加**: (N$_\infty$) では $\hat c=1$(Rule 1 補題 R1-N∞-S 2.)ゆえ **$\hat c_\mu$ 単独で (P1) が決まる**。新しい漏洩経路として **I-b∞**(Rule 1 v1.3 §9.2)に登録 | 本便 |
| G6 | §3.4 見積り表 / §0.1 札 | 2 枝 | **3 枝**へ。(N$_\infty$) の期待次元 **2**(= (W) と同じ・(N$_{\rm aff}$) の中の期待余次元 1 ではなく (N) の中の期待余次元 1 — いずれも期待次元であって証明された stratum 次元ではない・便 36 F2.2) | 本便 |
| G7 | §7 論点 4 | 「枝 (N) での $P_0$ の Weierstrass 性は未決」 | **(N$_\infty$) では $P_0$ は非 Weierstrass(Rule 1 補題 R1-M0 3.)**。未決なのは **(N$_{\rm aff}$) だけ**に絞られた | Rule 1 v1.2 |
| G8 | §7 論点 5 文献要請 | 退化 strata の分類 | **第二の要請を追加**: **多項式 Pell 方程式 $a^2-f_6p^2=\text{const}$($\deg f_6=6$・解の次数 5)の存在条件とパラメトリゼーション** | 本便 |

> **接触規律(v1.2 でも不変)**: 本改訂でも個別モデル候補・係数・数値近似・database に一切接していない。**v1.2 で新たに行った機械計算はない**(修理・新命題はすべて紙上。§3.3.5 の整合検査は Rule 1 v1.3 §6.2 の $\lambda$ 側の式との**手計算突合**による — §8)。

## v1 → v1.1 差分表

| # | 箇所 | v1 | v1.1 | 出典 |
|---|---|---|---|---|
| E1 | §3.3 記号 | $c_5$($N$ の定義とも (3.2) とも整合しない) | **$c_N$ に統一**($N=\mu\mu^\iota=a^2-b^2f=c_N(x-x_0)^5$)。$c_5$ の名を廃止 | 便 32 F4.4 (4.1) |
| E2 | §3.3 (3.2) | $y^2 = a(x)^2+c_5(x-x_0)^5$(**符号が逆**) | $y^2 = a(x)^2-c_N(x-x_0)^5$。「$c_N=-b_0^2\operatorname{lc}(f)$」との整合も修理 | 便 32 F4.4 (4.2) |
| E3 | §3.3 gauge | $b_0=1$ と $f$ monic を同時に置きながら $c_N$ を自由母数として数えていた(**二重計上**) | **gauge を一本化**: $b_0=1$ ∧ $f$ monic $\Rightarrow\operatorname{lc}(f)=-c_N\Rightarrow c_N=-1$。正規形 $y^2=a(x)^2+(x-x_0)^5$。$c_N$ を残す変種は**未商の scaling を名指し**して併記 | 便 32 F4.4 後半 |
| E4 | §3.3 枝 (W) の $P_0$ 非 Weierstrass | $\operatorname{ord}_{P_0}(\mu)=1\ne5$ による間接証明 | **直接証明**($a(x_0)=0\Rightarrow(x-x_0)^2\mid f_5\Rightarrow$ 特異)へ差替え | 便 32 F4.4 末尾 |
| E5 | §3.3 / §3.4 枝 (N) の母数 3 | 「正味 3 母数」・注で「第二段の未知数は正確」 | **generic design count** と明記。**分離条件 6 項目を列挙**し、**global normal form theorem としては未成立**の札を付ける | 便 32 F4.5 |
| E6 | §0.1 / §2.4 | 機械照合の対象名が曖昧(通知は「S5-1/2/3 二系統化」) | **是正**: 機械が `S5.3` と呼ぶのは**補題 S5-B の中間部分群個数**。命題 S5-3(曲線の二枝正規形)は**照合を受けていない** | 便 32 F4.3 / W1 / ★教材 22 |
| E7 | §5 A2 | 「$\lambda=c\mu^2$ の分解形も併記」 | **凍結 2 前は禁止**(I-b 厳格版採用)。分解形の併記は凍結 2 後のみ | 便 32 F2.3・裁定 31 |
| E8 | §6.1 手順 2 | 正規形の 2–3 母数で切る(無条件の推奨) | strict I-b との緊張を明記(solver が $c$ を明示変数にする)。**sealed automation 化なしにこの手順を使わない** | 便 32 F2.3 |
| E9 | §7 論点 | 5 件すべて未決 | 論点 2・3 を便 32 の判定で更新 | 便 32 F4.1/F4.3/F2.3 |

> **接触規律(v1.1 でも不変)**: 本改訂でも個別モデル候補・係数・数値近似・database に一切接していない。v1.1 で新たに行った機械計算は**ない**(修理はすべて紙上)。

> ## 接触禁止の宣言(本稿の最重要規律)
>
> **本稿は個別モデル候補・係数の数値・数値近似・database 照会に一切接していない。** 探索コマンドを一度も実行していない。本稿で行った機械計算は **1 本だけ**で、その入力は **既に凍結済みの有限 fixture($G_5$ と標的 $H$ の置換データ)のみ**である(§2.4・scratchpad の `k5_blocks.js`)。曲線・$\lambda$・$u$・局所展開には触れていない。
>
> 本稿は manifest v1.2「現在許可されている工程」= **S5 の紙上設計**の成果物であり、個別モデル探索は**修正版凍結 1(Rule 1)の受理後**に始まる。

---

## 0. 結論(先に 8 行)

1. **divisor 恒等式は係数 ansatz より遥かに強い。** Riemann–Roch により、$(C,P_0,P_\infty)$ を固定した時点で $\lambda$ は**定数倍を除いて一意**に決まる($\ell(10P_\infty-10P_0)=1$)。**$\lambda$ の 9 個の係数は自由変数ではない**(§3.1)。
2. **★ Sol の紙上フィルタ $\operatorname{ord}[P_0-P_\infty]\in\{5,10\}$ は、$\{5\}$ へ半分に絞れる**(命題 S5-1・§2.4)。根拠は幾何でも数論でもなく、**凍結済み有限 fixture の置換群のブロック構造**である。
3. **★ その帰結として $\lambda$ は分解する**: $\boxed{\lambda = c\,\mu^2}$、$\mu:C\to\mathbf P^1$ は**次数 5・monodromy $D_5$**・$(\mu) = 5P_0-5P_\infty$、分岐型 $(5,\ 2^21,\ 2^21,\ 5)$(命題 S5-2)。**探索対象は次数 10 の Belyi 写像ではなく次数 5 の $\mu$ になる。**
4. **変数削減の見積り**: 素朴な係数 ansatz は **未知数 ~20 / 方程式 ~22**(次数 10 の連立)。divisor 第一段で **未知数 4**(3 次元 moduli + スカラー)/ 条件 4。ブロック第二段の正規形で **自由母数 2((W)・open locus 上)/ 3((N$_{\rm aff}$)・generic design count)/ 2((N$_\infty$)・v1.2 新設)**。§3.4 の表。**v1.1: (N$_{\rm aff}$) の 3 は期待次元であって証明された母数ではない**(§3.3.4)。**v1.2: 枝は三つである**((W)/(N$_{\rm aff}$)/(N$_\infty$))。(N$_\infty$) の正規形は**多項式 Pell 方程式** $a^2-f_6p^2=\hat c_\mu$ で、(3.3) の探索器を流用できない(§3.3.5・§3.3.6 の total な分岐表)。
5. **$\lambda\in\mathbb Q(x)$ は禁止**(Sol F9.2)。さらに $\mu$ の段でも同じ理由で $\boxed{\mu = a(x)+b(x)y,\ b\ne0}$ が必須(§4)。
6. **★★ 漏洩警報(manifest への必須修理提案)**: $\lambda = c\mu^2$ の定数 $c$ について $\boxed{\text{(P1)}\iff c\in K^{\times2}\iff \operatorname{sqfree}(c)\in\{1,-1,5,-5\}}$(命題 S5-4)。すなわち **$c$ の平方類は「$u$ と同値な leading class」であり、Model-Builder が 1 行で封印予測 (P1) を判定できてしまう。** 便 31 F4.3 が抽象的に警告した「$u$ という語を使わずに同値量を計算できる」の**具体例が実在した**。Rule 1 の whitelist に追加を要する(§6.2)。→ **【v1.1: 採用済み】** 命題 S5-4 は便 32 F4.6 で **PASS**、(L1)–(L3) は **I-b 厳格版**として Rule 1 §9 I-b / §9.3 に入った(§7 論点 3)。さらに §3.3.2 の系で **$\operatorname{sqfree}(c)$ が gauge 不変**であることを示した — この 1 ビットは正規形の選び方で消せない。
7. **二 dessin は同一曲線とは限らない**(Sol F9.2)。ただし**両者の有限側 fixture は完全に同型な入力を与える**(§2.4 の機械検査は sq/ns で全項目一致)。同時探索は「共同凍結」の意味であって同一 ansatz の強制ではない。
8. **exact 受理物**は §5 の 8 項目。**数値近似・database label は discovery 用であり証拠でない**(Sol F9.4)。

### 0.1 状態札

| 主張 | 札(**v1.1 で更新**) |
|---|---|
| §2.1–§2.3(RH・divisor 恒等式・位数 1/2 の排除) | **紙上・Sol F9.1 と一致**(私の独立再証明) |
| **補題 S5-B**(唯一のブロック系) | **紙上証明が Sol 監査で PASS**(便 32 F4.1)。有限群部分は GAP 34/34・node 36/36・相互突合 13/13 を**静的突合済みの cross-checked artifact** として受理。**Lean の `verified` ではない**(便 32 W5) |
| **命題 S5-1**($\operatorname{ord} = 5$ ちょうど)・**S5-2**($\lambda = c\mu^2$) | **PASS**(便 32 F4.2)。**ただし機械照合が触れたのは補題 S5-B の有限群部分まで**(下記 ★) |
| §3 の変数削減見積り | **紙上・単系統**。素朴側の本数は上界の概算。**第二段の枝 (N) は generic design count**(§3.3・§3.4 の注・v1.1 で降格) |
| **命題 S5-3**(正規形・v1.1 で $c_N$ 規約へ符号修理) | **紙上・単系統・未照合**。v1 の符号と gauge の不整合は便 32 F4.4 で差戻し → **v1.1 で修理**。枝 (W) の母数 2 は open locus 上で妥当(便 32 F4.5)。**副枝 (N$_{\rm aff}$) の母数 3 は generic design count であって global normal form theorem ではない**。**v1.2: 前提として N-0($P_0\ne\iota(P_\infty)$)を明示**(§3.3.4) |
| **命題 S5-3∞**(副枝 (N$_\infty$) の正規形 (3.3∞) = 多項式 Pell・**v1.2 新設**) | **紙上・単系統・未照合**(Sol 監査へ)。**design count でなく global な同値**であり分離条件を要しない。期待次元 2 は幾何と係数の二通りの数え(design count)が一致(§3.3.5・**証明された stratum 次元ではない — 便 36 F2.2 で降格**) |
| **命題 S5-4**((P1) $\iff c\in K^{\times2}$) | **PASS**(便 32 F4.6)。**I-b 厳格化の根拠**および凍結 2 後の独立な (P1) 証明書として使ってよい |
| **命題 S5-4∞**((N$_\infty$) では (P1) $\iff\hat c_\mu\in K^{\times2}$・**v1.2 新設**) | **紙上・単系統・未照合**。**新しい漏洩経路**として Rule 1 v1.3 §9.2 **I-b∞** に登録済(§6.2) |
| §3.5(D₅ ⇒ 巡回五次被覆) | **構造の指摘のみ・実行しない**(scope 宣言) |

> ### ★ 是正: 「S5.3 照合」は命題 S5-3 の照合ではない(便 32 F4.3 / W1 / ★教材 22)
>
> `search/k5-blocks-check.g` と `crosscheck/check-k5-blocks.mjs` が自ら `S5.3` と名づけている検査項目の中身は
> $$ \text{「}\bar H\ \text{を含む中間群のうち}\ \lvert\mathcal K\rvert=20\ \text{が}\ 0\ \text{個、}\ \lvert\mathcal K\rvert=50\ \text{が}\ 1\ \text{個」} $$
> であり、これは**補題 S5-B の一部**である。両照合器は**曲線方程式・norm 恒等式 (3.1)・二重根条件・母数数えを入力にも出力にも持たない。**
>
> したがって **commit 3eb0a70 の題名「S5-1/2/3 の二系統照合」は過大**であり、正しくは「**補題 S5-B / 命題 S5-1 / 命題 S5-2 の有限群部分**の二系統照合」である。**命題 S5-3(曲線の二枝正規形)は二系統証拠を一切持たない** — しかも実際に符号の不整合があった(E1/E2)。
>
> **★教材 22: 同じラベルの検査は、同じ定理の検査とは限らない。** 以後、certificate 内に「検査名 ↔ 検査対象の命題番号」の対応を明記させる。

---

## 1. 対象の再掲(凍結済み・変更禁止)

`docs/week4-K5橋_D1_opus_v1.md` §4・§8.1 より(二系統 cross-checked):

- $P = G_5\cong\mathbb F_5^3\rtimes C_2^2$(位数 500)、marking $X=\bar x,\ Y=\bar y,\ Z=\bar z$、$XYZ=1$、$\operatorname{ord}(X)=10$。
- 標的 $H\le G_5$: $\lvert H\rvert=50$、$N_{G_5}(H)=H$、$\Lambda = \{H\text{ の }G_5\text{-共役}\}$、$\lvert\Lambda\rvert = 10 = M$。
- $\Lambda$ 上の ordered passport $(\sigma_0,\sigma_1,\sigma_\infty) = (10,\ 2^41^2,\ 10)$、$\sigma_0\sigma_1\sigma_\infty = 1$。
- monodromy 群 $\operatorname{Mon} = G_5/\operatorname{Core}(H)$、位数 **100**、$\operatorname{Core}(H)\cong C_5$。
- $\operatorname{Aut}(W_0/U) = N_{G_5}(H)/H = \mathbf 1$。
- 標的は $G_5$-共役類 **2 つ**($\Lambda_{\rm sq}$: $\alpha\in\{1,4\}$ / $\Lambda_{\rm ns}$: $\alpha\in\{2,3\}$)。**`target_policy = all_two_classes`**。
- $K = \mathbb Q(\zeta_{20})$、$M=10$、$e=5$、$\mathfrak F_0\cong C_5$。

---

## 2. divisor 恒等式を係数 ansatz より先に使う

### 2.1 Riemann–Hurwitz と三つの divisor(Sol F9.1 の再導出)

$$ 2g-2 = 10\cdot(-2) + \underbrace{9}_{\lambda=0} + \underbrace{4}_{\lambda=1} + \underbrace{9}_{\lambda=\infty} = 2,\qquad \boxed{g = 2}. \tag{2.1} $$

$\lambda=0$ と $\lambda=\infty$ の fiber は各々**幾何点 1 個**(分岐指数 10)。1 点集合は $G_{\mathbb Q}$-安定だから、$\mathbb Q$-モデル上で

$$ P_0,\ P_\infty\ \in\ C(\mathbb Q). \tag{2.2} $$

$\lambda=1$ 上の二重点を $Q_1,\dots,Q_4$、単純点を $R_1,R_2$ とすると

$$ (\lambda) = 10P_0-10P_\infty,\qquad (\lambda-1) = 2\textstyle\sum_j Q_j+R_1+R_2-10P_\infty,\qquad (d\lambda) = 9P_0+\textstyle\sum_j Q_j-11P_\infty. \tag{2.3–2.5} $$

次数検算: $0$ / $8+2-10=0$ / $9+4-11 = 2 = 2g-2$ ✓(最後は標準因子)。

### 2.2 これを「先に」使うとは何を意味するか

(2.3) は $\lambda\in L(10P_\infty-10P_0)$ を意味する。**この空間の次元は Riemann–Roch で先に分かる**:

$$ \deg(10P_\infty-10P_0)=0\ \Longrightarrow\ \ell\in\{0,1\},\qquad \ell = 1\iff 10P_0\sim10P_\infty\iff 10\,[P_0-P_\infty]=0. \tag{2.6} $$

すなわち:

> **観測 A(第一段の変数削減).** $(C,P_0,P_\infty)$ を固定し $[P_0-P_\infty]\in J(C)(\mathbb Q)[10]$ が成り立つなら、**$\lambda$ はスカラー倍を除いて一意**である。
> ⇒ **$\lambda$ の係数は独立変数ではない。** 探索すべきは「$\lambda$ の係数」ではなく「**10-torsion 差をもつ二点付き種数 2 曲線**」である。

これが「divisor 恒等式を係数 ansatz より先に使う」の数学的中身である。素朴な ansatz が $\lambda$ に 9 個の係数を割り当てるのに対し、実際の自由度は **0 個 + スカラー 1 個**しかない。

### 2.3 紙上フィルタ $\operatorname{ord}[P_0-P_\infty]\in\{5,10\}$(位数 1 / 2 の排除)

$D := [P_0-P_\infty]\in J(C)(\mathbb Q)$ と置く。(2.6) より $10D = 0$、ゆえに $\operatorname{ord}(D)\mid10$。

- **$\operatorname{ord}(D)\ne1$**: $D=0$ なら $P_0\sim P_\infty$ ゆえ $\ell(P_\infty)\ge2$、すなわち次数 1 の写像 $C\to\mathbf P^1$ が存在して $C\cong\mathbf P^1$。$g=2$ に矛盾。
- **$\operatorname{ord}(D)\ne2$**: $2D=0$ なら $2P_0\sim2P_\infty$、ゆえに $\ell(2P_\infty)=2$ で $\lvert2P_\infty\rvert$ は種数 2 の**唯一の** $g^1_2$(超楕円写像)である。その写像を $h$ とすると $(h) = 2P_0-2P_\infty$ と取れ、$(\lambda) = 5\,(h)$ ゆえ $\lambda/h^5$ は零点も極も持たない ⇒ $\lambda = c\,h^5$。$h$ の deck 変換は超楕円対合 $\iota$ であり、$\iota$ は $\lambda$ を固定する。ゆえに $\operatorname{Aut}(C/\mathbf P^1)\supseteq C_2$ で、$\operatorname{Aut}=1$ に矛盾。

$$ \Longrightarrow\qquad \boxed{\operatorname{ord}[P_0-P_\infty]\in\{5,\ 10\}} \tag{2.7} $$

(Sol F9.1 (9.4) と一致。私の独立再証明。)

### 2.4 ★★ 命題 S5-1 / S5-2 — フィルタを $\{5\}$ に絞り、$\lambda$ を分解する

(2.7) は幾何の議論だけから来ている。**凍結済み有限 fixture の置換群を見ると、さらに強い結論が出る。**

> **補題 S5-B(ブロック構造).** 標的の次数 10 の置換作用($\Lambda$ 上・$\Lambda_{\rm sq}$ と $\Lambda_{\rm ns}$ の**両方**)は、**ちょうど一つ**の非自明なブロック系をもつ:
> $$ \textbf{2 ブロック}\times\textbf{サイズ 5}. $$
> さらに $\sigma_0$ と $\sigma_\infty$ は二つのブロックを**入れ替え**、$\sigma_1$ は各ブロックを**保つ**。

**紙上証明。** $\operatorname{Core}(H)$ を決める。$R=\mathbb F_5^3$ の $C_2^2$-安定部分空間は、三つの指標が相異なるので座標部分空間だけ。$H\cap R = U = \langle e_2,\ \alpha e_1+e_3\rangle$($\alpha\ne0$)に含まれる座標線は $\langle e_2\rangle$ のみ。また $\operatorname{Core}(H)\not\subseteq R$ なら $(v,q_2)\in\operatorname{Core}$ を $e^t$ で共役して $(1-q_2)t$ が $\langle e_1,e_3\rangle$ 全体を走るので $\operatorname{Core}\supseteq\langle e_1,e_3\rangle\not\subseteq U$、矛盾。ゆえに $\operatorname{Core}(H)=\langle e_2\rangle = \langle Y^2\rangle\cong C_5$、$\operatorname{Mon} = M := G_5/\langle e_2\rangle$(位数 100)。

$M = V\rtimes C_2^2$、$V = \langle\bar e_1,\bar e_3\rangle$。$(1-q_1)V=\langle\bar e_3\rangle$, $(1-q_3)V=\langle\bar e_1\rangle$ より $[M,M]=V$、$M^{\rm ab}\cong C_2^2$。点安定化群 $\bar H$(位数 10)を含む中間群 $\bar H\le \mathcal K\le M$ を数える:

- $\lvert\mathcal K\rvert=20$: $\lvert\mathcal K\cap V\rvert=5$ かつ $\mathcal K V/V=C_2^2$ が必要。$\mathcal K\cap V$ は $\mathcal K$ で正規ゆえ $q_1$-安定でなければならないが、$\mathcal K\cap V\supseteq\bar U=\langle\alpha\bar e_1+\bar e_3\rangle$ で $q_1(\alpha\bar e_1+\bar e_3) = \alpha\bar e_1-\bar e_3$、これが $\bar U$ に入るのは $2\alpha=0$ すなわち $\alpha=0$ のときだけ。$\alpha\ne0$(good の条件)に矛盾。**⇒ 存在しない。**
- $\lvert\mathcal K\rvert=50$: $\mathcal K = V\rtimes\langle q\rangle$ で $q_2$ を含む必要 ⇒ $\mathcal K = V\rtimes\langle q_2\rangle$ **ちょうど 1 個**。

ブロック系 ↔ 中間群だから、非自明なブロック系はサイズ 5 のもの 1 つだけ。$X\mapsto q_1\notin\langle q_2\rangle$、$Z\mapsto q_3\notin\langle q_2\rangle$、$Y\mapsto q_2$ ゆえ入替/保存も従う。∎

**機械検査(単系統・node)**: `scratchpad/k5_blocks.js`(全 $2^{10}$ 部分集合をブロック判定で悉皆)。$\alpha=1$($\Lambda_{\rm sq}$)と $\alpha=2$($\Lambda_{\rm ns}$)の両方で

```
|H| = 50 / |N_G(H)| = 50 / |Lambda| = 10
cycle types = 10 / 2.2.2.2.1.1 / 10 ,  sX o sY o sZ = id : true
|Core(H)| = 5  -> |Mon| = 100 ,  Core(H) = <e_2>
nontrivial blocks containing point 0: {0,2,4,6,8}      (ちょうど 1 系・サイズ 5)
sX swaps blocks? true | sY swaps? false | sZ swaps? true
deg-5 types: sX^2|B = 5   sY|B = 2.2.1   sZ^2|B = 5
|<sX^2,sY,sZ^2>| on 5 points = 10        (= D_5)
```

**D1 §4・§8.1 の二系統値をすべて再現したうえで**、新規項目(ブロック・$D_5$)を追加した。**新規項目は起草時点では単系統である。**

> **v1.1 追記(照合の射程)**: その後 `search/k5-blocks-check.g`(GAP 34/34)・`crosscheck/check-k5-blocks.mjs`(node 36/36)・相互突合 13/13 が**この補題 S5-B の有限群部分**を二系統化した(便 32 F4.1 が静的突合済みとして受理)。**照合の射程はここまでである** — 両照合器が `S5.3` と呼ぶ項目も**補題 S5-B の中間部分群個数**であって、§3.3 の命題 S5-3(曲線の二枝正規形)ではない(§0.1 の ★・便 32 F4.3)。

> **命題 S5-2(分解).** 標的の被覆 $W_0\to\mathbf P^1_\lambda$ は
> $$ C\ \xrightarrow{\ \mu\ (\deg 5)\ }\ Y\ \xrightarrow{\ \deg 2\ }\ \mathbf P^1_\lambda $$
> と一意に分解し、$Y\cong\mathbf P^1_{\mathbb Q}$、第二の写像は $\mathbb Q$-座標で $\lambda = c\,\mu^2$($c\in\mathbb Q^\times$)である。

**証明。** 補題 S5-B の唯一のブロック系が中間被覆 $Y$ を与える($\deg(Y/\mathbf P^1)=$ ブロック数 $=2$)。$Y\to\mathbf P^1_\lambda$ が分岐するのは $\sigma_i$ がブロックを入れ替える点、すなわち $\lambda=0,\infty$ のちょうど 2 点。Riemann–Hurwitz より $2g_Y-2 = 2(-2)+1+1 = -2$、$g_Y=0$。ブロック系は**一意**ゆえ $G_{\mathbb Q}$-安定で、$Y$ は $\mathbb Q$ 上へ降下する。$\lambda=0$ 上の $Y$ の点は 1 点で $\mathbb Q$-有理、ゆえに $Y\cong\mathbf P^1_{\mathbb Q}$。$\lambda=0,\infty$ で全分岐する $\mathbb Q$-有理な次数 2 写像は、適当な $\mathbb Q$-座標 $\mu$ で $\lambda = c\mu^2$($c\in\mathbb Q^\times$)。∎

> **命題 S5-1(フィルタの半減).** 標的では
> $$ \boxed{\ \operatorname{ord}[P_0-P_\infty] = 5\quad\text{ちょうど}\ } $$

**証明。** $\lambda = c\mu^2$ で $\lambda$ は $P_0$ で 10 位の零、$P_\infty$ で 10 位の極。$t\mapsto ct^2$ は $t=0,\infty$ で 2 位に分岐するから $\operatorname{ord}_{P_0}(\mu)=5$, $\operatorname{ord}_{P_\infty}(\mu)=-5$、しかも $\mu$ の零・極は他にない。ゆえに $(\mu) = 5P_0-5P_\infty$ で $5D=0$。§2.3 より $D\ne0$、$5$ は素数ゆえ $\operatorname{ord}(D)=5$。∎

> **系 S5-2a($\mu$ の分岐データ).** $\mu:C\to\mathbf P^1$ は次数 5・monodromy 群 $D_5$(5 点上の自然作用)で、分岐は
> $$ \{0,\ s,\ -s,\ \infty\}\quad(s^2 = 1/c),\qquad \text{局所型}\ (5,\ 2^21,\ 2^21,\ 5). $$
> 検算: $\sum(e-1) = 4+2+2+4 = 12 = 2g-2+2\deg\mu = 2+10$ ✓。$D_5$ の 5 点作用では回転が 5-巡回、鏡映が $2^21$ — 型が自動的に整合する。

**この 3 つが、Sol F9.1 の贈り物を最大限まで使い切った形である。**

---

## 3. 変数削減の見積り

### 3.1 第一段 — $\lambda$ の係数を消す(観測 A)

§2.2 の通り。$(C,P_0,P_\infty)$ + torsion 条件を先に据えれば $\lambda$ は自動。次元:

$$ \dim\mathcal M_{2,2} = 3+2 = 5,\qquad 5\ \text{torsion 条件は余次元 }2\ (\dim J = 2)\ \Longrightarrow\ \dim = 3. $$

これに $\lambda$ のスカラー 1 を足して **4 母数**。切る条件は「$\lambda$ の 4 個の残余分岐点がすべて同一値」= 3 条件 +「その値を 1 にする」= 1 条件、計 **4 条件**。$4-4=0$ ✓ — **rigid(Hurwitz 空間 0 次元)であることと整合**する。

### 3.2 第二段 — $\lambda$ でなく $\mu$ を探す(命題 S5-2)

$$ \ell(10P_\infty) = 9\quad\text{に対し}\quad \ell(5P_\infty) = 4. $$

素朴 ansatz が $\lambda$ に割り当てる 9 係数は、$\mu$ の **4 係数**に落ちる。しかも $\lambda = c\mu^2$ ゆえ $\lambda$ の 9 係数は $\mu$ の 4 係数の**二次式**として自動生成される。

### 3.3 命題 S5-3 — 正規形(二枝)【**v1.1 で符号と gauge を修理**】

#### 3.3.0 記号の統一(v1.1)

**$c_5$ という記号は廃止し、以後すべて $c_N$ を使う。** 定義は norm 側に置く:

$$ \boxed{\ N\ :=\ \mu\mu^\iota\ =\ a^2-b^2f\ =\ c_N\,(x-x_0)^5\ }\qquad(x_0:=x(P_0)). \tag{3.1} $$

v1 は (3.1) を $c_5$ で書きながら (3.2) で $y^2=a^2+c_5(x-x_0)^5$ と書いており、これは $c_5:=-c_N$ と**改名した場合にだけ**正しい形だった(便 32 F4.4)。しかも直前の「$c_5=-b_0^2\operatorname{lc}(f)$」および枝 (N) の (3.3) は $c_N$ 側の符号で書かれていたため、**一箇所の typo として吸収できない不整合**だった。v1.1 は全式を (3.1) の $c_N$ に揃える。

#### 3.3.1 導出

$\mu\notin\mathbb Q(x)$(§4)なので $\mu = a(x)+b(x)y$、$b\ne0$。$\mu^\iota:=\mu\circ\iota = a-by$ と置くと

$$ \mu+\mu^\iota = 2a(x)\in\mathbb Q(x),\qquad N=\mu\mu^\iota = a^2-b^2f\in\mathbb Q(x),\qquad \operatorname{div}_0(N) = 5P_0+5\iota P_0 . $$

$N$ は $\mathbf P^1_x$ 上の関数で、その零因子は $x^*(x_0)$ の 5 倍。ゆえに (3.1)。

> **枝 (W): $P_\infty$ が Weierstrass 点**($y^2=f_5(x)$、$P_\infty=\infty$)。$\operatorname{ord}_{P_\infty}(x)=-2,\ \operatorname{ord}(y)=-5$ ゆえ $L(5P_\infty)=\langle1,x,x^2,y\rangle$、$\deg a\le2$、$b = b_0$ 定数。(3.1) の左辺で $\deg(a^2)\le4$ だから $x^5$ の係数は $-b_0^2\operatorname{lc}(f_5)$、右辺は $c_N$。すなわち
> $$ \boxed{\ c_N\ =\ -\,b_0^2\operatorname{lc}(f_5)\ } \tag{3.1W} $$
> ((3.1) から直接 $b_0^2f_5 = a^2-c_N(x-x_0)^5$ でも同じ。)したがって曲線は
> $$ \boxed{\ C:\ b_0^2\,y^2 = a(x)^2 - c_N\,(x-x_0)^5,\qquad \mu = a(x)+b_0\,y,\qquad \deg a\le2\ } \tag{3.2} $$
> — **v1 の $+c_5$ は誤り。符号は $-c_N$ である。**

#### 3.3.2 gauge の一本化(便 32 F4.4 後半)

v1 は「$y$ を再スケールして $b_0=1$、$f$ をモニックに取る」と書きながら、そのあと $c_N$ を**自由母数として数えて**いた。これは**二重計上**である。(3.1W) より

$$ b_0=1\ \wedge\ \operatorname{lc}(f_5)=1\quad\Longrightarrow\quad \boxed{\ c_N=-1\ }. $$

**v1.1 の採用 gauge(正本)**: $b_0=1$(= $\mu$-scaling を商)∧ $f_5$ monic(= $x,y$-scaling の一部を商)∧ $x_0=0$(= $x$-平行移動を商)。このとき正規形は

$$ \boxed{\ C:\ y^2 = a(x)^2+x^5,\qquad \mu = a(x)+y,\qquad \deg a\le 2,\qquad \lambda = c\,\mu^2\ } \tag{3.2$'$} $$

で、**残る母数は $(a_0,a_1,a_2)$ の 3 個**。まだ商していない残余は次の一次元トーラス(+符号)だけである:

$$ x\mapsto\tau^2x,\quad y\mapsto\tau^5y,\quad \mu\mapsto\tau^{-5}\mu\ \Longrightarrow\ a_i\mapsto\tau^{2i-5}a_i\ (i=0,1,2),\qquad c\mapsto\tau^{10}c \tag{3.2$''$} $$

(この $\tau$-作用は $\deg a\le2$・monic・$b_0=1$・$x_0=0$ をすべて保つ。Rule 1 §2.2 の M2 と**同一の群**である。)ゆえに

$$ \textbf{枝 (W) の正味母数}\ =\ 3-1\ =\ \boxed{2}. $$

**v1 と同じ 2 だが、内訳が違う**(v1 は「5 母数 − 3 正規化」、v1.1 は「3 母数 − 1 残余トーラス」)。v1 の数え方は $c_N$ を自由に残したまま $b_0=1$ と monic を課しており、前提と数えが食い違っていた。

> **$c_N$ を自由母数として残す変種(併記・どの scaling が未商かを名指しする)**: $b_0=1$ を**課さず**($\mu$-scaling を未商のまま)$f_5$ monic だけを課すなら、(3.1W) は $c_N=-b_0^2$ となり $c_N$ は $\mathbb Q^{\times}$ の**平方の $-1$ 倍**を走る 1 母数。逆に $b_0=1$ だけを課して monic を課さないなら($x,y$-scaling が未商)$c_N=-\operatorname{lc}(f_5)$。**いずれの変種でも、正規形と母数商の gauge は一つだけ選ぶ** — v1.1 の正本は (3.2$'$) である。

> **★ 系(gauge 不変性 — 命題 S5-4 / I-b の健全性チェック)**: $(\mu)=5P_0-5P_\infty$ と $\ell(5P_\infty-5P_0)=1$ から **$\mu$ は $\mathbb Q^\times$ 倍を除いて一意**。$\mu\mapsto\delta\mu$ は $\lambda=c\mu^2$ 固定のもと $c\mapsto c\delta^{-2}$ を与えるので、
> $$ \boxed{\ \operatorname{sqfree}(c)\in\mathbb Q^\times/\mathbb Q^{\times2}\ \text{は正規形の選び方に依らない真の不変量}\ } $$
> である((3.2$''$) の $c\mapsto\tau^{10}c$ も平方倍)。すなわち命題 S5-4 が読む 1 ビットは **gauge の artefact ではない** — これが §9 I-b(Rule 1)を「厳格版」で運用すべき数学的理由である。

#### 3.3.3 枝 (W) では $P_0$ は非 Weierstrass(**直接証明**・v1.1 で差替え)

> **補題 S5-W.** 枝 (W) の正規形 (3.2) において $a(x_0)\ne0$。同値に、$P_0$ は Weierstrass 点でない。

**証明(便 32 F4.4 末尾の形)。** $\mu(P_0)=0$ と $\mu=a+b_0y$ から $y(P_0)=-a(x_0)/b_0$、ゆえに「$P_0$ が Weierstrass」$\iff y(P_0)=0\iff a(x_0)=0$。いま $a(x_0)=0$ と仮定すると $(x-x_0)\mid a$ ゆえ $(x-x_0)^2\mid a^2$、また $(x-x_0)^2\mid (x-x_0)^5$ だから (3.2) の右辺より

$$ (x-x_0)^2\ \bigm|\ b_0^2f_5 . $$

$b_0\in\mathbb Q^\times$ ゆえ $f_5$ は $x_0$ で**二重根**をもち、$C:y^2=f_5(x)$ は $(x_0,0)$ で特異になる。これは $C$ が種数 2 の非特異曲線であることに反する。∎

(v1 は $\operatorname{ord}_{P_0}(\mu)=1\ne5$ を経由する間接証明を使っていた。上の議論は滑らかさだけを使い、$\mu$ の位数計算を要しない。)

#### 3.3.4 副枝 (N$_{\rm aff}$)(**generic design count** — global normal form theorem ではない)

> **【v1.2 の前提の明示・R-4】この節が扱うのは副枝 (N$_{\rm aff}$) だけである。** すなわち
> $$ \boxed{\ \textbf{N-0}:\quad P_0\ \ne\ \iota(P_\infty)\qquad(\Longleftrightarrow\ x_0:=x(P_0)\in\mathbb Q\ \text{が\textbf{有限}}) } $$
> を**前提とする**。枝 (N) の六次モデルの無限遠 fiber は $x^{-1}(\infty)=\{\infty_+,\infty_-\}$ の**二点**であり(Rule 1 v1.3 §5.1 補題 R1-U∞ 1.)、$P_0=\infty_-=\iota(P_\infty)$ は $P_0\ne P_\infty$ と**両立する**。その場合 $x_0$ は存在せず、下の (3.3) は**そもそも書けない**。**(N$_\infty$) は §3.3.5 で別 ansatz として扱う。**

> **副枝 (N$_{\rm aff}$): $P_\infty$ が Weierstrass 点でなく、$P_0$ がアフィン**($y^2=f_6(x)$、$f_6$ monic、$P_\infty=\infty_+$、$x_0=x(P_0)\in\mathbb Q$)。$\mu+\mu^\iota=2a$ は $\infty_\pm$ の両方で 5 位の極 ⇒ $\deg a = 5$;$\mu-\mu^\iota = 2by$ も同様で $b = p_2(x)$($\deg p_2 = 2$)。$\operatorname{div}_0(N)=5P_0+5\iota P_0$ が**アフィン**なので (3.1) は
> $$ \boxed{\ a(x)^2 - c_N\,(x-x_0)^5\ =\ f_6(x)\,p_2(x)^2\ }\qquad(\textbf{N-0 を仮定}) \tag{3.3} $$
> となる(**v1 と同じ符号** — (3.3) はもともと $c_N$ 規約で書かれていた)。すなわち**次数 10 の多項式 $a^2-c_N(x-x_0)^5$ が二重根を 2 個もつ**という条件。母数 $(a:6,\ c_N,\ x_0) = 8$、正規化 3 個($x$-平行移動・$x$-scaling・$\mu$-scaling)、条件 2 個(可動二重根 2 個 = 余次元 2)⇒ **期待次元 $8-3-2 = 3$**。

$$ \boxed{\ \textbf{副枝 (N}_{\rm aff}\textbf{) の「3」は generic design count(期待次元)であって、証明された母数ではない.}\ } $$

**便 32 F4.5 を受けた降格。** 上の数えが実際の母数数えになるためには、少なくとも次の条件を**分けて**扱う必要があり、v1.1 の時点でどれも証明していない(**N-0 は v1.2 で追加**):

| # | 分離条件 | それが破れると何が起きるか |
|---|---|---|
| **N-0**(v1.2) | **$P_0\ne\iota(P_\infty)$**(= $x_0$ が有限) | **(3.3) が書けない。** $\operatorname{div}_0(N)=5P_0+5\iota P_0 = 5\infty_-+5\infty_+$ が無限遠に乗るので $N=\mu\mu^\iota$ は**定数**になり、右辺の $(x-x_0)^5$ が消える(§3.3.5 (3.3∞))。**(3.3) を discovery engine にすると、この stratum の候補を丸ごと落とす**(便 35 F5.1) |
| N-2 | $f_6$ が squarefree | $C$ が非特異(種数 2)であるための必要条件。破れれば (3.3) の解は曲線を与えない |
| N-3 | $\gcd(f_6,p_2)=1$ | $p_2$ の根が $f_6$ の根でもあると、その点は Weierstrass 点で $\mu=a+p_2y$ の局所位数が変わる |
| N-4 | $\deg f_6=6$ と $\deg p_2=2$ が落ちない | 主係数が退化すると枝 (W) 側または別配置へ落ち、$P_\infty$ の Weierstrass 性の場合分けが変わる |
| N-5 | $\infty_-$ での leading cancellation が成立 | $\mu=a+p_2y$ が $\infty_-$ で極を持たない($\operatorname{ord}_{\infty_-}(\mu)=0$)ための条件。$y$ の分枝の符号選択と結びついており、(3.3) を満たすだけでは $(\mu)=5P_0-5\infty_+$ は従わない |
| N-6 | 退化 strata で二条件が独立 | 「二重根 2 個」の 2 条件が横断的でない層では余次元が 2 未満になりうる |

**したがって v1.1 の札は**: 副枝 (N$_{\rm aff}$) の (3.3) は **generic locus 上の設計見積り(条件付き PASS)**。**global normal form theorem としては未成立。**

**枝 (W) の側**は、符号と gauge を修理した (3.2$'$)(3.2$''$) の下で「open locus 上の次元数え」として妥当である(便 32 F4.5 前半)。

**枝の次元が違う** — (W) は (N) の中の余次元 1 の軌跡である($\dim\mathcal M_{2,2}$ で $P_\infty$ を Weierstrass 点に限ると $5\to4$、torsion 2 を引いて $2$)。**この比較も generic locus 上の主張である。**

> **【GAP-S5a】どちらの枝かは紙上で決まっていない。** 次元の一般性からは **(N) が期待される**が、これは**発見的**であって証明ではない(解は 0 次元なので余次元 1 の軌跡上にあってもよい)。**Rule 1 は三枝すべてを先に書く**(`docs/week4-K5_Rule1_v1.md` v1.3 §2.2・§3・§5)。$P_0$ の Weierstrass 性については、**枝 (W) では補題 S5-W で決着**(非 Weierstrass);**副枝 (N$_\infty$) でも決着**(非 Weierstrass — Rule 1 補題 R1-M0 3.);**未決なのは副枝 (N$_{\rm aff}$) だけ**である(v1.2 で絞り込み・§7 論点 4)。

#### 3.3.5 副枝 (N$_\infty$) の正規形 — 多項式 Pell 型(**v1.2 新設・R-4**)

**設定**: 枝 (N) のモデル $y^2=f_6(x)$($f_6$ は $\mathbb Q$ 上モニック・**squarefree**・$\deg=6$)、$P_\infty=\infty_+$、そして
$$ \boxed{\ P_0\ =\ \infty_-\ =\ \iota(P_\infty)\ }\qquad(\textbf{N-0 の破れ}). $$
Rule 1 v1.3 の正規化 M1 (2.-3) に合わせ、$x$-平行移動は $B_5=0$(depressed form)に使い切る。$s:=1/x$、$w:=y/x^3$、$F(s):=s^6f_6(1/s)$、$W\in\mathbb Q[[s]]$ を $W^2=F,\ W(0)=1$ とする(Rule 1 補題 R1-U∞ 1.)。

$\mu$ は $\operatorname{div}(\mu)=5P_0-5P_\infty$(命題 S5-1/S5-2)ゆえアフィン部分で正則、したがって
$$ \mu\ =\ a(x)+p(x)\,y,\qquad a,p\in\mathbb Q[x],\qquad p\ne0\ (\text{補題 S5-H}). $$

> **命題 S5-3∞(副枝 (N$_\infty$) の正規形 — global な同値).** 上の設定で、次の 1. と 2. は同値:
> 1. $\operatorname{div}(\mu)=5P_0-5P_\infty$(すなわち $\mu$ が命題 S5-2 の次数 5 写像である);
> 2. 次が成り立つ:
> $$ \boxed{\ a(x)^2-f_6(x)\,p(x)^2\ =\ \hat c_\mu\ \in\ \mathbb Q^\times\quad(\textbf{定数}),\qquad \deg a=5,\quad \deg p=2,\quad a_5:=[x^5]a\ =\ [x^2]p\ \ne0.\ } \tag{3.3∞} $$
>
> このとき、$t:=1/x$($=P_0$ の $\mathbb Q$-有理 uniformizer・Rule 1 補題 R1-U∞ 2.)に関して
> $$ \mu\ =\ v\,t^5\bigl(1+O(t)\bigr),\qquad \boxed{\ v\ =\ \frac{\hat c_\mu}{2a_5}\ }. \tag{3.4∞} $$
> さらに $\gcd(a,p)=1$ と $\gcd(a,f_6)=1$ は **(3.3∞) から自動**である。

**証明.** $\tilde a(s):=s^{M}a(1/s)$、$\tilde p(s):=s^{M-3}p(1/s)$、$M:=\max(\deg a,\deg p+3)$、$G_\pm:=\tilde a\pm W\tilde p$ と置くと $\mu=s^{-M}(\tilde a+w\tilde p)$ で、$\infty_+$ では $w=W$、$\infty_-$ では $w=-W$。

1.⟹2.: $\operatorname{ord}_{\infty_-}\mu=+5$ は $\operatorname{ord}_sG_-=M+5>0$ を与えるから $G_-(0)=\tilde a(0)-\tilde p(0)=0$。$M$ の定義より $(\tilde a(0),\tilde p(0))\ne(0,0)$ なので $\tilde a(0)=\tilde p(0)\ne0$、すなわち $\deg a=M$、$\deg p=M-3$、$a_M=p_{M-3}\ne0$。すると標数 0 で $G_+(0)=2a_M\ne0$ ゆえ $\operatorname{ord}_sG_+=0$、他方 $\operatorname{ord}_{\infty_+}\mu=-5=\operatorname{ord}_sG_+-M$ より $M=5$。norm については $\operatorname{div}(\mu\mu^\iota)=\operatorname{div}(\mu)+\iota_*\operatorname{div}(\mu)=(5P_0-5P_\infty)+(5P_\infty-5P_0)=0$ で $\mu\mu^\iota=a^2-f_6p^2\in\mathbb Q[x]$ だから定数、しかも $\mu\ne0$ ゆえ $\ne0$。

2.⟹1.: $\mu\mu^\iota=\hat c_\mu\ne0$ より $\mu$ はアフィン部分に零点も極ももたないので $\operatorname{div}(\mu)$ は $\{\infty_\pm\}$ に台をもつ。$M=\max(5,2+3)=5$ で $G_+(0)=a_5+p_2=2a_5\ne0$ ゆえ $\operatorname{ord}_{\infty_+}\mu=0-5=-5$。$G_-(0)=a_5-p_2=0$ ゆえ $\operatorname{ord}_{\infty_-}\mu\ge1-5=-4$、次数 0 と合わせて $\operatorname{ord}_{\infty_-}\mu=+5$。すなわち $\operatorname{div}(\mu)=5\infty_--5\infty_+=5P_0-5P_\infty$。

(3.4∞): $G_+G_-=\tilde a^2-W^2\tilde p^2=\tilde a^2-F\tilde p^2=s^{10}\bigl(a(1/s)^2-f_6(1/s)p(1/s)^2\bigr)=\hat c_\mu\,s^{10}$、ゆえに
$$ \frac{\mu}{s^5}=\frac{G_-}{s^{10}}=\frac{\hat c_\mu}{G_+}\ \xrightarrow[s\to0]{}\ \frac{\hat c_\mu}{2a_5}. $$
最後に、既約 $q\in\mathbb Q[x]$ が $a$ と $p$ を共に割れば $q^2\mid\hat c_\mu$、$a$ と $f_6$ を共に割れば $q\mid\hat c_\mu$ となり、いずれも $\deg q\ge1$ と定数性に反する。$\blacksquare$

> **★ (3.3∞) は多項式 Pell 方程式である。** $\deg f_6=6$ の超楕円曲線に対する
> $$ a^2-f_6\,p^2\ =\ \text{const}\qquad(\text{Abel--Chebyshev の Pell 方程式}) $$
> の**次数 5 の解**を求めよ、という問題に他ならない。これは命題 S5-1($\operatorname{ord}[P_0-P_\infty]=5$)の副枝 (N$_\infty$) における顔である。**探索は「二重根 2 個」型の条件から「Pell 解の存在」型の条件へ完全に姿を変える** — (3.3) の探索器を流用できない実体的な理由がここにある。
>
> **状態の区別(重要)**: 本稿が**証明した**のは $n=5$ の場合(命題 S5-3∞)だけである。「$[\infty_+-\infty_-]$ が位数 $n$ の torsion $\iff$ 次数 $n$ の Pell 解が存在」という**一般 $n$ の言明は古典的とされるが、私は一次文献を照合していない**(§7 論点 5 の**文献要請 2**)。**この一般形に依存する議論は本稿では一切していない。**

> **命題 S5-3∞ の状態札**: **紙上・単系統・未照合**(Sol 監査へ)。ただし v1.1 の命題 S5-3 と違い、**これは design count でなく同値命題**であり、N-1〜N-6 型の分離条件を**要しない**(上の証明は $f_6$ の squarefree 性以外に一般位置の仮定を使っていない)。

**次元(二通りの独立な数え・数値としては一致 — いずれも期待次元/design count であり、証明された stratum 次元ではない)**

> **【便 36 F2.2 の降格・出典明記】** 下表の「余次元 2」「次元 2」は Sol 便 36 F2.2 の指摘により **期待次元 2 / design count** へ一貫して降格する(裁定_37_ben36 条件 6)。理由は二つ: (i) 幾何側では section $(C,P)\mapsto[K-2P]$ が相対 $J[5]$ と交わる零点 locus の codimension が 2 であるための横断性・次元定理を本稿は示していない(各 fiber の $J[5]$ が有限であることだけからは codimension 2 は自動でない)。(ii) 係数側でも、10 本の係数方程式が該当成分上で独立(regular sequence)であることを示していない。二通りの数えが**数値として一致すること自体**は Pell 同値・total 分岐表を壊さない事実として有効だが、それは「期待次元が二通りの方法で 2 と算出される」という設計上の整合であって、stratum の次元が厳密に 2 であるという定理ではない。

| 数え方 | 内訳 | 結果(期待次元) |
|---|---|---|
| **幾何(stratum)** | $\{(C,P_\infty):P_\infty\ \text{非 W}\}$ は $3+1=4$ 次元。条件は $[\iota(P_\infty)-P_\infty]=[K-2P_\infty]\in J[5]\smallsetminus\{0\}$ で、$J$ は 2 次元・$J[5]$ は有限 ⇒ **期待余次元 2**(横断性・次元定理は未証明) | $4-2=\boxed{2}$(期待値) |
| **係数(design count)** | 未知数: $f_6$ の $B_0..B_4$(monic・$B_5=0$)$=5$、$a$ の $a_0..a_5=6$、$p$ の $p_0,p_1,p_2=3$ ⇒ 14。gauge: $x$-scaling 1 + $\mu$-scaling 1 ⇒ 12。条件: $a^2-f_6p^2$ の $x^1,\dots,x^{10}$ の係数が消える **10 本**(独立性・regular sequence 性は未証明) | $12-10=\boxed{2}$(design count) |

**両者の数値が一致する。** ゆえに副枝 (N$_\infty$) は **(N) の中の期待余次元 1**(期待次元 2)であり、枝 (W) と**同じ期待次元**である(証明された stratum 次元としての一致ではない)。

> **【重要】次元が低いことは排除ではない。** 解は 0 次元(rigid)なので、期待余次元 1 の stratum 上にあってよい。しかも **(N$_\infty$) の組合せ的排除証明書は撤回された**(Rule 1 v1.3 §11 論点 7: 正しい $(0\,\infty)$ 述語 (35.4) の witness が**両 fixture に実在**する)。**「一般には起こらないから後回し」は、この設計書では使えない論法である。**

> **【文献要請 2(v1.2 新設)】** §7 論点 5 に第二の要請を追加した(多項式 Pell の存在条件とパラメトリゼーション)。**降ろされても §3.3.5 は自前導出を正本とし、文献は照合にのみ使う。**

#### 3.3.6 **total な分岐表**(便 35 F5.1 の要求)

**Model-Builder の枝列挙は、次の表を網羅しなければならない。** 表に無い枝へ落ちた入力は既定枝へ丸めず停止する(Rule 1 v1.3 §9.2 **I-m**)。

| 枝 | intrinsic 判定(Rule 1 M0) | 正規形 / ansatz | 期待次元 | 状態札 | 探索器の所在 | **閉じられない場合の処置** |
|---|---|---|---|---|---|---|
| **(W)** | $\ell(2P_\infty)=2$ | (3.2$'$): $y^2=a(x)^2+x^5$、$\mu=a+y$、$\deg a\le2$ | 2 | open locus 上妥当(便 32 F4.5) | 既設計 | 探索失敗は非存在の証明でない ⇒ **BRIDGE-UNKNOWN** |
| **(N$_{\rm aff}$)** | $\ell(2P_\infty)=1$ かつ $\ell(P_0+P_\infty)=1$ | (3.3): $a^2-c_N(x-x_0)^5=f_6p_2^2$ | 3 | **generic design count**(N-0〜N-6 未分離) | 既設計(ただし退化 strata 未分類) | 同上 |
| **(N$_\infty$)** | $\ell(2P_\infty)=1$ かつ $\ell(P_0+P_\infty)=2$ | **(3.3∞): $a^2-f_6p^2=\hat c_\mu$(多項式 Pell)**、$\deg a=5$、$\deg p=2$、$a_5=p_2\ne0$ | 2 | **命題 S5-3∞ = global な同値**(紙上・単系統) | **未設計**(v1.2 で ansatz のみ確定) | **この stratum を走らせずに「候補なし」を宣言してはならない。** 走らせられないなら campaign の結論は **BRIDGE-UNKNOWN** |

> **総括**: 三枝は Rule 1 v1.3 §2.2 M0 の判定で**排他かつ網羅**である(補題 R1-M0)。したがって「三枝すべてで探索が閉じた」場合にのみ非存在方向の議論に進める。**一枝でも探索器が無ければ、結論は BRIDGE-UNKNOWN であって「見つからなかった」ではない**(§5 の受理規律: 「探索して見つからなかった」型の否定は証拠でない)。

### 3.4 見積り表

| 段 | 未知数 | 方程式 | 備考 |
|---|---|---|---|
| **素朴**(枝 (W) で $\lambda$ を直接) | $f_5$: 6、$A$: 6、$B$: 3、$x_0,\hat c$: 2、$\lambda=1$ 側の $h,k$: 6 ⇒ **~20**(正規化 3 を引いて ~17) | $A^2-B^2f = \hat c(x-x_0)^{10}$: 11 本、$(A-1)^2-B^2f = \hat c\,h^2k$: 11 本 ⇒ **~22** | 係数次数 10 の連立。**Gröbner 非現実的**(この規模は 8GB 機で通らない) |
| **第一段**(divisor) | 3(moduli)+ 1(スカラー)= **4** | 4 | $\lambda$ の 9 係数が消える。torsion 条件は Mumford 演算で判定(消去法でない) |
| **第二段**(ブロック・命題 S5-3) | (W): **2**(open locus 上・(3.2$'$))、(N$_{\rm aff}$): **3**(**generic design count**)、**(N$_\infty$): 2**(**幾何と係数の二通りの数えが一致**・§3.3.5・v1.2) | 分岐型 $(5,2^21,2^21,5)$ + 調和条件。**(N$_\infty$) だけは形が変わる: 多項式 Pell $a^2-f_6p^2=\hat c_\mu$**(§3.3.5) | $\mu$ の係数 4(枝 (W) では $a$ の 3 + $b_0$、gauge 固定後は $a$ の 3 のみ)。**方程式の次数も 10 → 5 に落ちる** |
| **第三段**(§3.5・**着手しない**) | 巡回五次被覆の分岐指数 $(n_1,\dots,n_4)\in(\mathbb Z/5)^4$ の**有限個** | — | 連続母数がほぼ消える |

> **注(誠実な但し書き・v1.1 で修理)**: 「素朴」欄の本数は**上界の概算**である。$\iota$-対称性による冗長性を除けば実効本数は減る。主張は「桁が違う」ことであって、正確な Gröbner 複雑度ではない。
>
> **第一段の未知数は正確**(Riemann–Roch から)。**第二段はそうではない**: v1 は「第一段・第二段の未知数は正確」と書いたが、これは**過大な主張だった**(便 32 F4.5)。正しくは —
> - **枝 (W) の 2**: 符号と gauge を修理した (3.2$'$)(3.2$''$) の下で、**open locus 上の次元数えとして妥当**。
> - **副枝 (N$_{\rm aff}$) の 3**: **generic design count(期待次元)**。§3.3.4 の **N-0**〜N-6 が分離されるまで、**global normal form theorem としては未成立**。
> - **副枝 (N$_\infty$) の 2(v1.2)**: **正規形 (3.3∞) 自体は global な同値(命題 S5-3∞)**で分離条件を要しない。**期待次元 2 は依然 design count**であり(便 36 F2.2 で「次元 2」の断定を降格)、**幾何(stratum)と係数(design)の二通りの独立な数えが数値として一致**している(§3.3.5 の表)。**この枝の探索器は未設計**であり、走らせられなければ結論は **BRIDGE-UNKNOWN**(§3.3.6)。

### 3.5 第三段(構造の指摘のみ・本稿では着手しない)

系 S5-2a より $\operatorname{Mon}(\mu)\cong D_5$。ゆえに $C\to\mathbf P^1_\mu$ は**二面体的五次被覆**であり、その Galois 閉包 $\tilde C$($\deg 10$、$g=4$)は

$$ \tilde C\ \longrightarrow\ \tilde C/C_5\ \longrightarrow\ \mathbf P^1_\mu $$

を経由し、$\tilde C/C_5$ は $\{s,-s\}$ の 2 点でのみ分岐する次数 2 被覆ゆえ $\cong\mathbf P^1$。したがって **$\tilde C$ は $\mathbf P^1$ の巡回 5 次(superelliptic)被覆 $v^5 = \prod_{i}(w-w_i)^{n_i}$ であり、$C = \tilde C/\langle\text{鏡映}\rangle$**。

> **scope 宣言**: この還元は「探索を有限の指数選択に帰着させる」という意味で第二段よりさらに強い。しかし**これ以上進めると個別モデルの構成そのものになる**ため、**本稿では指数 $(n_i)$ の決定も $w$-座標の正規化も行わない**。Rule 1 受理後の Model-Builder の作業とする。**司令塔・Sol へ**: この第三段を S5 の作業指示に含めるか(含めると探索は劇的に軽くなるが、Rule 1 の正規形規則を第三段の座標で書き直す必要がある)を裁定されたい(§7 論点 1)。

---

## 4. ansatz の必須形 — $B\ne0$(Sol F9.2)と、その $\mu$ 版

> **補題 S5-H.** $\lambda\notin\mathbb Q(x)$。さらに $\mu\notin\mathbb Q(x)$。

**証明。** $\lambda\in\mathbb Q(x)$ なら $\lambda$ は超楕円写像 $x$ を経由するので $\lambda\circ\iota=\lambda$、すなわち $\iota\in\operatorname{Aut}(C/\mathbf P^1_\lambda)$。$\operatorname{Aut}=1$ に矛盾。$\mu\in\mathbb Q(x)$ なら $\lambda = c\mu^2\in\mathbb Q(x)$ で同じ矛盾。∎

$$ \Longrightarrow\qquad \boxed{\ \lambda = A(x)+B(x)y,\ B\ne0\ }\qquad\text{かつ}\qquad \boxed{\ \mu = a(x)+b(x)y,\ b\ne0\ } \tag{4.1} $$

$\lambda = c\mu^2 = c\bigl(a^2+b^2f\bigr) + 2cab\,y$ なので $A = c(a^2+b^2f)$, $B = 2cab$。**$B\ne0$ は $b\ne0$ かつ $a\ne0$ を要求する**($a=0$ なら $\mu = by$ で $\mu^2\in\mathbb Q(x)$、上と同じ矛盾)。

> **★ 教材候補 1**: 「$\operatorname{Aut}=1$ ゆえ $\lambda\notin\mathbb Q(x)$」は、**分解 $\lambda=c\mu^2$ を見つけたあとも消えない**。分解は $\mathbf P^1_\lambda$ 側の話で、超楕円対合は $C$ 側の話だから、二つは独立である。$\mu$ が「$x$ の関数でない」ことを毎回確認せよ。

---

## 5. exact 受理物の一覧(Sol F9.4)

**凍結 2 に入れてよいのは、次の 8 項目が exact に閉じたものだけである。**

| # | 受理物 | 形式 |
|---|---|---|
| A1 | **曲線方程式** $C/\mathbb Q$ | $\mathbb Q$-係数の明示式(§3.3 の正規形・Rule 1 §3 の全順序で一意化) |
| A2 | **Belyi 写像** $\lambda$ | $\mathbb Q(C)$ の元としての**完全な式**。**【v1.1 修理】$\lambda=c\mu^2$ の分解形の併記は凍結 2 前は禁止**($(c,\mu)$ の対に分離した瞬間に封印予測 (P1) が読める — Rule 1 §9 I-b 厳格版・便 32 F2.3・裁定 31)。分解形の記録は**凍結 2 のあと**に、独立な (P1) 証明書(§6.2 (L3))として行う |
| A3 | **divisor 恒等式** (2.3)(2.4)(2.5) | 各点の座標つき。**成立の exact 証明**(数値評価でない) |
| A4 | **種数・分岐型** | $g=2$、passport $(10,2^41^2,10)$ の exact 検証 |
| A5 | **monodromy 群と exact conjugator** | $(\sigma_0,\sigma_1,\sigma_\infty)\in S_{10}^3$ と、標的三つ組への**明示置換**(**一意** — 補題 S5-U・下記) |
| A6 | $\operatorname{Aut}(C/\mathbf P^1)=1$ | exact 証明(数値的な「見つからなかった」は不可) |
| A7 | $P_0,\ P_\infty$ と **uniformizer $t$** | $\mathbb Q$-有理点の明示座標 + Rule 1 §5 のアルゴリズムが返した $t$ の式 |
| A8 | **$\operatorname{ord}[P_0-P_\infty]=5$ の exact 検証** | 命題 S5-1 の独立確認(Jacobian 上の exact 演算)。**不一致なら integrity stop** |

> **補題 S5-U(exact conjugator の一意性).** $\operatorname{Aut}(W_0/U)=1$ ゆえ $C_{S_{10}}(\operatorname{Mon})\cong N_{\operatorname{Mon}}(\text{点安定化群})/(\text{点安定化群}) = N_{G_5}(H)/H = 1$。したがって幾何 fiber と $\Lambda$ の間の、monodromy を intertwine する全単射は**ちょうど一つ**。**A5 に tie-break は不要**である。

**受理しないもの(discovery 用であり証拠でない)**: 数値近似(浮動小数点の根・数値 monodromy)、database label(LMFDB 等)、「探索して見つからなかった」型の否定、他窓($K^{(3)}$・$A_5$)からの類推。

---

## 6. 探索戦略と、その最中に守るべきこと

### 6.1 推奨する探索順序(Rule 1 受理後)

1. **枝の決定(v1.2: 三枝)**: Rule 1 v1.3 §2.2 M0 の intrinsic 判定 — $\ell(2P_\infty)=2$?(Weierstrass 性)**および $\ell(P_0+P_\infty)=2$?($P_0=\iota(P_\infty)$ 判定)。**三枝 (W)/(N$_{\rm aff}$)/(N$_\infty$) を**同時に**走らせる(一枝で見つからないことは非存在の証明でない)。**(N$_\infty$) を「排除済み」として省いてはならない** — その排除証明書は撤回された(Rule 1 v1.3 §11 論点 7)。枝ラベルは三値 enumeration で、未知ラベルの既定値 fallback は停止(Rule 1 **I-m**)。
2. **正規形 (3.2$'$) / (3.3) / (3.3∞) の 2–3 母数**を、$\mu$ の分岐条件(型 $(5,2^21,2^21,5)$ + 分岐点が $\{0,\pm s,\infty\}$ = **調和条件**)で切る。**(N$_\infty$) では (3.3∞) が多項式 Pell 方程式なので、(3.3) の探索器を流用できない**(§3.3.5・§3.3.6)。
   > **【v1.1 の必須留保・便 32 F2.3】この手順は strict I-b と緊張する。** $\mu$-正規形で探索する solver は $\lambda=c\mu^2$ の $c$ を**明示変数として扱う**ため、「$c$ の平方類・平方因子・符号を凍結 2 前に計算・報告・選択に使わない」という Rule 1 §9 I-b 厳格版と**同時には運用できない**。
   > したがって: (a) **正本は Rule 1 §2.2 の (M-A)**(S5 設計に依存しない total な正規形)であり、(b) 本手順 2 を discovery engine として使うなら、**全候補列挙・M-A canonicalization・両翼共同 freeze までを人間から隔離した sealed automation** として**別 schema に事前登録**しなければならない。**その schema が事前登録されるまで、手順 2 を人間が回す形で実行しない。**
3. **exact に閉じる**(A1–A8)。**この段階まで $u$ に触れない。**
4. 両 dessin(sq/ns)を **atomic joint freeze**(凍結 2)。**片翼だけで Extractor を起動しない。**
5. 発射錠のあとに Extractor(B)が $u$ 二経路(Rule 1 §6)。

### 6.2 ★★ 漏洩警報 — $c$ の平方類は $u$ と同値である(命題 S5-4)

> **命題 S5-4.** $\lambda=c\mu^2$、$\mu = v\,t^5+O(t^6)$($t$ は $P_0$ の $K$-有理 uniformizer)とすると $u = c\,v^2$。ゆえに
> $$ \boxed{\ \text{(P1)}\ \operatorname{ord}\bigl([u^{-1}]_{10}\bigr)\in\{1,5\}\ \iff\ c\in K^{\times2}\ \iff\ \operatorname{sqfree}(c)\in\{1,\,-1,\,5,\,-5\}\ } $$
> ($c\in\mathbb Q^\times$・$K=\mathbb Q(\zeta_{20})$ の二次部分体は $\mathbb Q(i),\mathbb Q(\sqrt5),\mathbb Q(\sqrt{-5})$ の 3 つ)。

**証明。** $\lambda = c\mu^2 = c v^2t^{10}(1+O(t))$ ゆえ $u = cv^2$。(P1) $\iff u^5\in K^{\times10}$。$u^5 = c^5v^{10}$ で $v^{10}\in K^{\times10}$ ゆえ $\iff c^5\in K^{\times10}$。$c^5=d^{10}\iff(c/d^2)^5=1\iff c/d^2\in\mu_5(K)$、そして $\mu_5\subseteq K^{\times2}$($\zeta=(\zeta^3)^2$)ゆえ $\iff c\in K^{\times2}$。逆は $c=e^2\Rightarrow u=(ev)^2\Rightarrow u^5=(ev)^{10}$。最後の同値は $\mathbb Q^\times\cap K^{\times2}$ が $K$ の二次部分体で決まることから。∎

> **★ これが意味すること(必須修理の提案)。**
> 便 31 F4.3 / 裁定 29-5 の whitelist は「許可: 明示モデル・**Belyi map**・…/ 禁止: $\lambda/t^{10}$ の非零定数項とその同値物」と書く。ところが **Belyi map の出力そのものに含まれる定数 $c$ の平方因子を 1 行で計算するだけで、封印予測 (P1) の真偽が決まってしまう。** これは W5(「二つの抽出器の一致」と「Kummer 類の等号証明」は別ゲート)ともまた別の、**whitelist 内部の抜け穴**である。
>
> **提案(manifest v1.3 / Rule 1 への追加)**:
> - **(L1)** Model-Builder(A)の禁止項目に「$\lambda$ の分解 $\lambda = c\mu^2$ における $c$ の**平方類・平方因子・符号**を計算すること、およびそれを候補選択に使うこと」を明記する。
> - **(L2)** A が $\lambda$ を出力すること自体は不可避なので、**A の出力形式を「$\lambda$ の完全な式」に固定**し、$c$ を分離した形($c$ と $\mu$ の対)で報告することを**禁止**する(分離した瞬間に (P1) が読める)。
> - **(L3)** 逆に、これは **(P1) を「実行可能な exact 判定」に格上げする**朗報でもある。凍結 2 のあと、Extractor(B)は $u$ の 10 次展開を待たずに $\operatorname{sqfree}(c)$ の 1 行で (P1) を**閉じられる**。**(P1) の証明書型として (L3) を Rule 1 §7 に登録する**(cusp 展開経路の独立な裏取りになる)。
> - **(L4)** 同型の抜け穴が他にないかの点検: $u=cv^2$ の $v$ 側は? $v$ は局所展開の量なので whitelist ですでに禁止側にある。$c$ だけが「大域的な模型データ」の顔をして通っていた。
>
> **★ 教材候補 2**: **「局所量の禁止」は、大域量が局所量の一部を決めるときに漏れる。** $u$ は局所係数だが、$\lambda$ の分解定数 $c$ という**大域データ**が $u$ の**平方類**を決めていた。禁止リストは「量の出自(局所/大域)」でなく「**封印予測のどのビットを決めるか**」で書かねばならない。

### 6.3 ★★ 漏洩警報 2(**v1.2 新設**)— 副枝 (N$_\infty$) では $\mu$ の norm 定数だけで (P1) が決まる

> **命題 S5-4∞.** 副枝 (N$_\infty$) において、$\hat c_\mu:=a^2-f_6p^2\in\mathbb Q^\times$(命題 S5-3∞)とすると
> $$ \boxed{\ \text{(P1)}\ \iff\ c\in K^{\times2}\ \iff\ \hat c_\mu\in K^{\times2}\ \iff\ \operatorname{sqfree}(\hat c_\mu)\in\{1,-1,5,-5\}.\ } $$
> すなわち **$c$ を見なくても、$\mu$ 側の norm 定数 $\hat c_\mu$ 単独で封印予測 (P1) が完全に決まる。**

**証明。** $\lambda=c\mu^2$ より $\lambda$ の norm は $N(\lambda)=c^2N(\mu)^2=c^2\hat c_\mu^2$。副枝 (N$_\infty$) では $N(\lambda)=\hat c$ が定数(Rule 1 補題 R1-B∞ 2.)で、しかも **$\hat c=1$**(Rule 1 補題 R1-N∞-S 2.;前提 $\sigma_1\ne\mathrm{id}$ は本 campaign では定理)。ゆえに $c^2\hat c_\mu^2=1$、すなわち $c=\pm\hat c_\mu^{-1}$。$K=\mathbb Q(\zeta_{20})$ は $i$ を含むので $-1=i^2\in K^{\times2}$、また $\hat c_\mu^{-1}\in K^{\times2}\iff\hat c_\mu\in K^{\times2}$。したがって符号の不定性は消え、$c\in K^{\times2}\iff\hat c_\mu\in K^{\times2}$。あとは命題 S5-4。$\blacksquare$

> **★ これが意味すること。**
> - **他の二枝ではこうならない。** (W)/(N$_{\rm aff}$) では $N(\lambda)=c^2c_N^2(x-x_0)^{10}$ で、$\hat c=1$ に相当する定理が**ない**。ゆえに $c_N$ 単独では (P1) は決まらず、$\hat c$($u$ 側・既に封印対象)と併せて初めて決まる。**非対称は $\hat c=1$ が (N$_\infty$) だけで成り立つことから生じる。**
> - **(L5)(新設)**: Model-Builder(A)の禁止項目に「**$\mu$ の norm 定数 $\hat c_\mu=a^2-f_6p^2$ の値・平方類・平方因子・符号を計算すること、およびそれを候補選択に使うこと**」を明記する。**Rule 1 v1.3 §9.2 I-b(I-b∞)に登録済み。**
> - **★ 教材候補 3(教材候補 2 の続き)**: 禁止リストは**枝ごとに再点検**しなければならない。同じ名前の量($c$、norm 定数、主係数)でも、**枝が変われば「決めるビット」が変わる**。(N$_\infty$) では、(N$_{\rm aff}$) なら安全だった $\mu$ 側の norm 定数が、$\hat c=1$ という**その枝だけの定理**によって完全な (P1) オラクルに昇格した。
> - **(L3) の (N$_\infty$) 版(凍結 2 後のみ)**: 逆に、凍結 2 のあとは $\operatorname{sqfree}(\hat c_\mu)$ の 1 行で (P1) を閉じられる。$u$ の 10 次展開を待つ必要はない(cusp 展開経路の独立な裏取り)。

---

## 7. 論点(便 32 / 司令塔裁定へ・**v1.1 で 2・3 を更新**)

1. **第三段(§3.5・$D_5$ ⇒ 巡回五次被覆)を S5 の作業指示に含めるか。**(**未決**)含めれば探索は劇的に軽くなる(連続母数がほぼ消える)が、Rule 1 の正規形規則を $\tilde C$ の座標で書き直す必要があり、**凍結 1 の再起草**になる。私は「含めるべきだが、Rule 1 v1 は $(C,\lambda)$ の座標で凍結し、第三段は**発見の補助**としてのみ使う(受理物 A1–A8 は必ず $(C,\lambda)$ で書く)」が安全だと見ている。
   > **v1.1 の追記**: 第三段を発見の補助に使う場合も、§6.1 手順 2 と同じ strict I-b の緊張がある(座標変換の途中で $c$ が露出しうる)。**sealed automation の別 schema に入れる**のが筋である。
2. **命題 S5-1/S5-2 の監査。** → **【決着・PASS】**(便 32 F4.1/F4.2)。GAP 再現も実施済み(`search/k5-blocks-check.g` 34/34・`crosscheck/check-k5-blocks.mjs` 36/36・相互突合 13/13)。
   > **ただし射程の是正(★教材 22・便 32 F4.3)**: **二系統化されたのは補題 S5-B / 命題 S5-1 / 命題 S5-2 の「有限群部分」まで**である。両照合器が `S5.3` と呼ぶ項目も**補題 S5-B の中間部分群個数**であって、**命題 S5-3(曲線の二枝正規形)ではない**。命題 S5-3 は曲線方程式・norm 恒等式・二重根条件・母数数えを扱うが、両照合器はそれらを入力にも出力にも持たない。**命題 S5-3 は現時点で単系統・未照合**(§0.1 の ★)。
3. **命題 S5-4 と (L1)–(L3) の採否。** → **【決着・(L1)(L2)(L3) すべて採用。代案(access log のみでの担保)は不採用】**(便 32 F2.3・F4.6・裁定 31)。命題 S5-4 自体も **PASS**。
   > (a) **I-b 厳格版**が Rule 1 §9 に入り、(L1)(L2) はその中身になった。(b) 担保は **access control と total selection rule** の二重であり、**語彙 grep は補助にすぎない**(便 32 W4)。(c) (L3)((P1) の第二証明書)は **凍結 2 のあとにのみ**使う。(d) §3.3.2 の系(**$\operatorname{sqfree}(c)$ は gauge 不変**)により、この 1 ビットは正規形の選び方に依らず実在する — 「別の正規形を選べば漏れない」という逃げ道はない。
4. **$P_0$/$P_\infty$ の Weierstrass 性(【GAP-S5a】)を紙上で決められるか。**(**部分的に決着・v1.2 でさらに前進**)$P_\infty$ の枝(W)/(N)は依然として紙上で決まっていない(次元の一般性からは (N) が期待される、という発見的議論のみ)。**$P_0$ については枝 (W) 内で決着**(補題 S5-W: 枝 (W) なら $P_0$ は必ず非 Weierstrass・§3.3.3)。
   > **v1.2 の絞り込み**: 副枝 **(N$_\infty$) でも決着** — $P_0=\iota(P_\infty)$ は $\iota$ の不動点でない($\iota(P_0)=P_\infty\ne P_0$)ので**非 Weierstrass**(Rule 1 v1.3 補題 R1-M0 3.)。したがって
   > $$ \boxed{\ P_0\ \text{の Weierstrass 性が未決なのは副枝 (N}_{\rm aff}\textbf{) だけ}\ } $$
   > である。$5$-torsion 点 $[P_0-P_\infty]$ と超楕円対合の相互作用に、私が見落としている制約はないか(**残る問いは (N$_{\rm aff}$) に限定された**)。
   > **副産物**: 副枝 (N$_\infty$) では $[P_0-P_\infty]=[\iota(P_\infty)-P_\infty]=[K-2P_\infty]=2[W-P_\infty]$($W$ は任意の Weierstrass 点・$K\sim2W$)。ゆえに $\operatorname{ord}[P_0-P_\infty]=5$ は **$\operatorname{ord}[W-P_\infty]\in\{5,10\}$** と同値であり、$P_0$ を独立変数として持たない(**$P_\infty$ だけで決まる**)。§3.3.5 の期待次元 2 はこの縮約の帰結でもある。
5. **【文献要請】**(文献ゲート・要請駆動): 「**種数 2・$\mathbb Q$ 上・$J(\mathbb Q)$ に位数 5 の点をもち、その点が二つの $\mathbb Q$-有理点の差 $[P_0-P_\infty]$ で表される曲線族**」の明示パラメトリゼーションが文献にあれば、§3.3 の正規形 (3.2$'$)/(3.3) の独立な裏取りになる(私の導出は単系統)。欲しい結果の型: **$X_1(5)$ 類似のモジュラー的パラメトリゼーション、または「$P_0-P_\infty$ が $n$-torsion」条件の Mumford 表現による明示方程式**。降ろされた場合でも **§3.3 は自前導出を正本とし、文献は照合にのみ使う**(降下の轍を踏まない)。
   > **v1.1 で要請の焦点が鋭くなった**: 最も効くのは **§3.3.4 の N-1〜N-6 を分離した形の主張**、すなわち「副枝 (N$_{\rm aff}$) の (3.3) が **generic locus の外でも**正規形になる(または、ならない strata の記述)」である。**枝 (W) は (3.2$'$) で閉じているので照合の価値は低い。** 欲しいのは「$a^2-c_N(x-x_0)^5$ が二重根を 2 個もつ」条件の**退化 strata の分類**。
   >
   > **【文献要請 2・v1.2 新設】多項式 Pell 方程式.** §3.3.5 で副枝 (N$_\infty$) の探索は
   > $$ a(x)^2-f_6(x)\,p(x)^2\ =\ \text{const}\ \in\mathbb Q^\times,\qquad f_6\ \text{monic squarefree }\deg 6,\quad \deg a=5,\ \deg p=2 $$
   > という **Abel–Chebyshev 型の多項式 Pell 方程式の次数 5 の解**の探索に帰着した。**具体的な技術的困難**: (i) この解が存在する $f_6$ の族を**明示的に**($\mathbb Q$ 上で)書き下す方法が私にはない。(ii) 素朴には未知数 14・方程式 10 の連立で、(3.3) 用の探索器を流用できない。(iii) 「解が存在しない」を証明する手段(= この stratum を閉じて BRIDGE-UNKNOWN を回避する道)も持っていない。
   > **欲しい結果の型**: (a) $\deg f=2g+2$ の超楕円 Pell 方程式について「解が存在 $\iff[\infty_+-\infty_-]$ が torsion、位数 $=\deg a$」の**正確な言明と出典**(私の導出は単系統);(b) **$g=2$・位数 5 の場合の明示パラメトリゼーション**(連分数展開・Mumford 表現・モジュラー曲線 $X_1(5)$ 類似のいずれでも);(c) **$\mathbb Q$ 上で位数 5 の解をもつ $f_6$ の有理点の有限性/無限性**に関する既知結果。
   > **降ろされた場合でも §3.3.5 は自前導出(命題 S5-3∞)を正本とし、文献は照合と探索器の設計にのみ使う。**

---

## 8. 検算と出所

- 機械検査 1 本: `scratchpad/k5_blocks.js`(node・自己完結・$G_5$ を $(v,q)$ 座標で自前実装)。入力は凍結済み有限 fixture のみ。**D1 §4/§8.1 の二系統既知値(|H|=50・|N|=50・|Λ|=10・passport・$\sigma_0\sigma_1\sigma_\infty=1$・$\lvert\operatorname{Core}\rvert=5$・$\lvert\operatorname{Mon}\rvert=100$)をすべて再現**したうえで、新規項目(ブロック系の一意性・$D_5$)を得た。
- **起草時点で新規項目は単系統**。その後 `search/k5-blocks-check.g` / `crosscheck/check-k5-blocks.mjs` が**補題 S5-B の有限群部分**を二系統化した(§2.4 の v1.1 追記)。`verified`(Lean)ではない。
- **v1.1 で新たに行った機械計算はない**(修理はすべて紙上)。**命題 S5-3 は依然として単系統・未照合**であり、機械照合の `S5.3` という名前はこの命題を指していない(§0.1 の ★・★教材 22)。
- **v1.2 でも新たな機械計算はない**(§3.3.5・§6.3 はすべて紙上)。**v1.2 で行った照合は手計算の突合 1 件**: 命題 S5-3∞ の $\mu$ 側の帰結を $\lambda=c\mu^2$ で押し出し、Rule 1 v1.3 §6.2 の $\lambda$ 側の独立導出(補題 R1-B∞)と一致することを確認した —
  $$ A=c(a^2+p^2f_6),\quad B=2cap\ \Longrightarrow\ \deg A=10,\ \deg B=7,\ a_{10}=b_7=2ca_5^2\ (\ne0),\ \hat c=c^2\hat c_\mu^2,\ u=\frac{\hat c}{2a_{10}}=c\Bigl(\frac{\hat c_\mu}{2a_5}\Bigr)^2=cv^2 $$
  で、**Rule 1 の $\deg A=10$・$\deg B=7$・$b_7=a_{10}$(補題 R1-B∞ 1.)と命題 S5-4($u=cv^2$)が同時に再現される**。$\lambda$ 側と $\mu$ 側は別々に導出したので、これは**紙上の二経路一致**である(機械照合ではない)。
- 曲線・$\lambda$・$u$・数値近似・database には一切接触していない(v1.2 でも同じ)。

### 8.1 v1.1 が閉じた項目 / 残した項目(**v1.2 で更新**)

| | 項目 |
|---|---|
| **閉じた(v1.1)** | 命題 S5-3 の符号($c_N$ 規約・(3.2))・gauge の一本化((3.2$'$)(3.2$''$)・$c_N=-1$)・枝 (W) の $P_0$ 非 Weierstrass(補題 S5-W・直接証明)・機械照合の対象名の是正・A2 の分解形併記の禁止 |
| **閉じた(v1.2 = R-4)** | **N-0 の明記**と (3.3) の $x_0$ 有限前提(§3.3.4)・**副枝 (N$_\infty$) の正規形 命題 S5-3∞ / (3.3∞)**(§3.3.5)・**total な分岐表**(§3.3.6)・**漏洩経路 命題 S5-4∞ / (L5)**(§6.3)・**副枝 (N$_\infty$) での $P_0$ 非 Weierstrass**(§7 論点 4) |
| **残した(明示の札)** | **副枝 (N$_{\rm aff}$) の母数 3 = generic design count**(N-1〜N-6 未分離・global normal form theorem 未成立)・**命題 S5-3 / S5-3∞ / S5-4∞ の二系統照合は未実施**(いずれも紙上・単系統)・**副枝 (N$_{\rm aff}$) での $P_0$ の Weierstrass 性は未決**・**§6.1 手順 2 を回すための sealed automation schema は未起草**・**副枝 (N$_\infty$) の探索器は未設計**(多項式 Pell・§3.3.5;閉じられなければ **BRIDGE-UNKNOWN**) |
