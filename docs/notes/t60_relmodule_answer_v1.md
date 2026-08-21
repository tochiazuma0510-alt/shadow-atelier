# T-60 回答 — 自己訂正 2 件、9-状態補題、relation-module 路線の裁定

**状態札: 数学者起草・司令塔検分前・Sol 未監査**
起草: Claude 数学者 / 2026-08-20 / 委嘱 = 司令塔(Sol T-59)
格: paper candidate。機械計算ゼロ。封印非接触。**B4-A / B4-B いずれも非宣言。**

---

## 0. 自己訂正 2 件 — **両方とも Sol が正しい。全面的に認める。**

### 訂正 1(対象違い)— **認める。T-58 §1・§2・§7 を撤回する。**

補正語が住む核は **$K=\ker(F_2\to J)$**($J=Q_0\times B(2,3)$、$|J|=39{,}680{,}928$)であって、私が書いた $H_{PB_3}$ の相対 Frattini 商ではない。Nielsen–Schreier より $K$ は自由階数
$$r_{F_2}=|J|(2-1)+1=39{,}680{,}929$$
⟹ $\dim_{\mathbf F_3}H_1(K;\mathbf F_3)=r_{F_2}$、完全 $\mathcal S_2$ は $\binom{r}{2}+r\approx7.87\times10^{14}$ ⟹ **literal 列挙は不可能**。**「$r\approx26$」「459 列で実行可能性の懸念なし」は根拠のない実行可能性主張であり、撤回する。**
**正しい Step 0 の対象は §3 に置き換える**(= $J$ の有限表示と関係加群)。

### 訂正 2(157ed の inert は必然、という主張)— **認める。撤回する。**

T-58 §4 で「順序付き triple-cube の inert は反対称性ゆえ必然」と書いたが、**triple product は Lie bracket ではない**ので反対称性の議論は適用できない。⟹ **必然性主張は不成立。撤回。**
**帰結(証拠価値の復権)**: 157ed(順序付き $26^3$ = 17,576)+ quadruple 80 + Hall 18 + 正規作用反復 3,240 の**全ゼロ**は、説明済みの自明現象ではなく **「深さを増やしても λ に届かない」の実測証拠**である。⟹ §2 の補題がこれを構造的に説明する。

---

## 1. ★ 9-状態補題(machine 事実 → 紙の定理)

**読み取り**: $9\ \text{states}\times26\ \text{cubes}\times2\ \text{signs}=468$ ✓ — 遷移表は $\pm$ 込みで閉じている。

> **補題 CUBE-INERT.** $\Sigma:=\{u_1^{\pm3},\dots,u_{26}^{\pm3}\}$、$\mathcal A=(Q,q_0,\delta,\lambda)$ を有限オートマトンとし、$|Q|=9$、$\delta:Q\times\Sigma\to Q$ が **$Q$ 上で閉じ**($q_0$ から到達可能な状態が $Q$ で尽きる)、出力増分 $\lambda:Q\times\Sigma\to\mathbf F_3$ が
> $$\lambda(s_1\cdots s_n)=\sum_{i=1}^{n}\lambda(q_{i-1},s_i),\qquad q_i=\delta(q_{i-1},s_i)$$
> を満たすとする。**全 468 遷移で $\lambda(q,s)=0$** ならば、語長 $n$ に関する自明な帰納法により
> $$\boxed{\ \lambda(w)=0\quad\text{for all}\ w\in\Sigma^{*}\ }$$
> $\Sigma$ は逆元で閉じている($\pm$)ので $\Sigma^{*}=\langle\Sigma\rangle$、すなわち
> $$\boxed{\ \lambda\big|_{\Gamma_{\rm cube}}\equiv0,\qquad \Gamma_{\rm cube}:=\langle u_1^{\pm3},\dots,u_{26}^{\pm3}\rangle\ }$$
> **深度に上限なし。** ∎

**格上げの意味**: inert 地帯の記述が「有限族の列挙」から **「部分群 $\Gamma_{\rm cube}$ 単位」** になった。157ed・quadruple・Hall・正規作用反復はすべて $\Gamma_{\rm cube}$ の中の語であり、**個別に測る必要はもうない**。今後の seed 設計は $\Gamma_{\rm cube}$ の**外**を明示的に狙うべきである。

**前件(明示・敵対的に)**
1. **λ がオートマトン出力として加法的**であること($\lambda(ww')=\lambda(w)+\lambda(w')$ 型でなく、状態依存の増分和で書けること)。machine が実際にそう計算しているなら ✓、そうでなければ補題は空。
2. **到達状態が 9 で閉じている**こと(468 = 9×26×2 が全遷移を尽くす)✓ receipt で確認可。
3. **正規閉包ではなく部分群**である。Sol の「(の正規閉包?)」への回答: **現状の遷移表は $\Gamma_{\rm cube}$ しか与えない。** 正規閉包 $\langle\Gamma_{\rm cube}\rangle^{F_2}$ へ拡張するには、遷移アルファベットに **$x^{\pm},y^{\pm}$ による共役**($s\mapsto x^{\pm}sx^{\mp}$ 等)を加え、状態集合が閉じたまま出力が全ゼロであることを再確認する必要がある ⟹ **FC-41**。閉じれば「$\lambda$ は $\Gamma_{\rm cube}$ の正規閉包上で恒等的に 0」まで上がり、**除外はさらに構造化される**。
4. **射程は登録 26 本の cube のみ**。$K$ 内の全 cube を覆うわけではない。

**SEED-EXT への即効**: T-58 の $\mathcal S_2=\{[u_i,u_j]\}\cup\{u_i^{3}\}$ のうち、**cube 半分は補題 CUBE-INERT で死ぬ**(その $u_i$ が登録 cube に含まれる限り)。⟹ **λ を動かし得るのは交換子側だけ**。これは探索設計の実質的な絞り込みである。

---

## 2. relation-module 路線の裁定 — **健全・decidable・かつ規模が $10^{15}\to10^{7}$ に落ちる。採用を推奨する。**

### 2.1 (a) 数学的健全性 — 定式化

$K=\ker(F_2\to J)$ とし、**Crowell/Fox 完全列**(私が T-36 補題 T34-J4 で証明した形)
$$0\longrightarrow H_1(K;\mathbf F_3)\longrightarrow \mathbf F_3[J]^{2}\xrightarrow{\ D_1\ }\mathbf F_3[J]\xrightarrow{\ \varepsilon\ }\mathbf F_3\longrightarrow0,\qquad D_1(e_x)=\bar x-1,\ D_1(e_y)=\bar y-1$$
を使う。**次元検算**: $\dim\ker D_1=2|J|-(|J|-1)=|J|+1=r_{F_2}$ ✓✓ — Nielsen–Schreier と一致(定式化の健全性検査)。

**$\mathbf F_3[J]$-加群として**: $J=\langle x,y\mid R_1,\dots,R_k\rangle$ を有限表示とすると
$$\boxed{\ H_1(K;\mathbf F_3)\ \text{は}\ [R_1],\dots,[R_k]\ \text{で生成される }\mathbf F_3[J]\text{-加群(関係加群)}\ }$$
⟹ **$\mathbf F_3$-次元は $4\times10^7$ だが、$J$-加群としての生成元は $k$ 本**(通常は数本)。

**λ の非零性判定の正確な形**: λ は作用の双対、すなわち $\mathbf F_3$-線形汎函数
$$\lambda:\ H_1(K;\mathbf F_3)\longrightarrow \mathbf F_3 .$$
作用が $\mathbf F_3[J]$-線形(または明示的に捻れ線形)なら
$$\boxed{\ \lambda\ne0\ \text{on}\ H_1(K;\mathbf F_3)\iff \exists i\le k,\ \exists g\in J:\ \lambda\bigl(g\cdot[R_i]\bigr)\ne0\ }$$
⟹ **判定は $k$ 本の生成元とその $J$-軌道の上だけで完結する**。157dl の Fox/Shapiro 装置($D_2$ 行列・sparse boundary)はこの複体の**同一物**であり、路線は既存資産の直系である。

### 2.2 (b) decidability の根拠

$J$ は**有限群**($|J|=39{,}680{,}928$)⟹ $\mathbf F_3[J]$ は**有限次元代数** ⟹ $H_1(K;\mathbf F_3)=\ker D_1$ は $\mathbf F_3$ 上有限次元($|J|+1$)⟹ **λ の非零性は有限線形代数**であり決定可能 ✓。
**規模の比較(これが決定的)**
$$\text{literal }\mathcal S_2:\ \binom{r}{2}+r\approx7.87\times10^{14}\quad\Longrightarrow\quad \text{relation module}:\ \dim=|J|+1\approx4.0\times10^{7}.$$
$D_1$ は行あたり非零 2 個の**疎行列** ⟹ 疎 $\mathbf F_3$ 線形代数(block-Wiedemann 級)の射程内。⟹ **$10^{15}$ の列挙が $10^{7}$ の疎解に落ちる。** 採用を推奨する理由はここに尽きる。

### 2.3 (c) 事前登録する述語と棄却条件

> **RM-1(判定)**: $k$ 本の関係子 $R_i$ について、$\lambda$ が $\mathbf F_3[J]$-部分加群 $\langle[R_1],\dots,[R_k]\rangle$ 上で恒等的に 0 か。
> - **全ゼロ ⟹ $\lambda\equiv0$ on $H_1(K;\mathbf F_3)$** ⟹ **補正領域内のいかなる語も target6 を動かせない**(branch-local な障害証明書)。
> - **非零 ⟹ provenance 付き lex-first 生成元** $g\cdot[R_i]$ を抽出し、それだけを full solve へ。
> **receipt 述語**: `lambda_on_relation_module` ∈ {`identically_zero`, `nonzero`}、非零なら `lex_first_generator` = $(i,g)$ と `lambda_value`。
> **棄却条件**:
> - RM-1 が `nonzero` を返したのに full solve が整合しない ⟹ 「λ 非零 ⟹ 可動」の含意が偽 ⟹ **λ の双対化定式化(§2.1)を再検**。
> - $\dim\ker D_1\ne|J|+1$ ⟹ **実装エラー**(§2.1 の次元検算が健全性ゲート)。
> - 作用が $\mathbf F_3[J]$-線形でない(捻れが群環の元でない)⟹ §2.1 の同値が壊れる ⟹ **前件破れ**として報告し停止。

### 2.4 (d) SEED-EXT の格の更新

| 版 | 格 |
|---|---|
| T-58 の literal $\mathcal S_2$(有限 q3-slice) | **死。撤回**(訂正 1:対象違い + 規模) |
| SEED-EXT の**着想**(不足は深度でなく**被覆**) | **生存**。ただし「被覆」の正しい意味は **$H_1(K;\mathbf F_3)$ を $\mathbf F_3[J]$-加群として張ること** |
| universal SEED-EXT の**正しい検査** | **RM-1 がそれである** ✓。関係加群全体を覆うので「被覆が足りない」という逃げ道が原理的に消える |
| 判定 | **有限 q3-slice では死・universal は UNKNOWN**(Sol の格付けを支持)。RM-1 が universal 側の決定手続き |

⟹ **(d) への回答: YES、relation-module 判定は universal SEED-EXT の正しい検査になっている。** 理由: literal 族はどう広げても $H_1(K;\mathbf F_3)$ の部分集合しか張らないが、RM-1 は**加群全体**を扱うので、被覆不足による偽陰性が構造的に排除される。

### 2.5 (e) 札 6 / 札 8 / W-FORM 弱形の現在の格(一段落)

**札 6(深さ 3 が本質)は否定側に傾いたが棄却しない** — 訂正 2 により 157ed/quadruple/Hall/正規反復の全ゼロが**実測証拠**へ復権し、しかも補題 CUBE-INERT がそれを「深さではなく部分群」として説明した ⟹ 深さを増やす方向の期待値は下がった。ただし Witt 基底の次数 3 元(交換子側)は未試行なので**保留・優先度低**。**札 8(軌道外 seed が要る)は格上げ** — 補題 CUBE-INERT が「$\Gamma_{\rm cube}$ の外に出ることが必要」を**定理として**与えたので、札 8 の主張は構造的裏付けを得た(ただし「軌道外」の正確な意味は「cube 生成部分群の外」であり、深度とは無関係)。**W-FORM 弱形($PB_3^{ab}$ 像ゼロ)は格下げ・要再判定** — 関係加群の生成元は $J$ の関係子であり $[F_2,F_2]$ に入る保証がない ⟹ 弱形の自動性は失われ、**RM-1 が返す lex-first 生成元の $x,y$ 指数和を測って初めて判定できる** ⟹ FC-40 を関係加群版へ書き換える(下表)。

---

## 3. 新規/改訂の有限検査

| 番号 | 検査 | 重要度 |
|---|---|---|
| **FC-41** | 補題 CUBE-INERT の**正規閉包版**: 遷移アルファベットに $x^{\pm},y^{\pm}$ 共役を加えても状態が閉じ出力が全ゼロか。閉じれば $\lambda\equiv0$ on $\langle\Gamma_{\rm cube}\rangle^{F_2}$ | **高**(除外の構造化が一段進む) |
| **FC-42** | $J=Q_0\times B(2,3)$ の**2 生成有限表示**と関係子 $R_1,\dots,R_k$($k$ の値)。**Step 0 の正しい対象**(T-58 §1 の置き換え) | **最重要**(RM-1 の入口) |
| **FC-43** | RM-1 の実行:$\lambda$ の関係加群上の非零性。健全性ゲートとして $\dim\ker D_1=\lvert J\rvert+1$ を先に検算 | **決定的** |
| **FC-40′** | (旧 FC-40 の改訂)RM-1 が返す生成元の $x,y$ 指数和 ⟹ W-FORM 弱形の生死 | 中 |

---

## 4. 申告

- 手計算で検証: Nielsen–Schreier $r=|J|+1$、$\dim\ker D_1=2|J|-(|J|-1)=|J|+1$(定式化の相互検算)、$468=9\times26\times2$、補題 CUBE-INERT の帰納法、$\binom r2\approx7.87\times10^{14}$。
- **撤回**: T-58 §1(gr₁ の対象)・§2(literal $\mathcal S_2$ と 459 列の実行可能性)・§4 の「157ed inert は必然」・§7 の実行仕様。**T-58 は本書で置き換えられる。**
- **UNKNOWN**: FC-41/42/43。$k$ の値。λ が $\mathbf F_3[J]$-線形かどうか(§2.3 の前件)。
- 157ee closure crosscheck は並行進行中で本書は未反映。
- **B4-A / B4-B いずれも宣言していない。**
