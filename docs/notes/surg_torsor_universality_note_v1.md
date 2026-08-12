# 展望ノート — 手術とトーサーを普遍性の言葉で

作成: 数学者(Opus 5)/ 2026-08-13 / **帰属 = 研究者の余興発注**(発案 4「普遍性で書けそう」・発案 5「圏論の言葉で非可換 crown へ」・発案 7 の系譜)
**格: candidate・展望ノート(Sol 監査対象外)**。★ **新規の数学的主張はありません** — 既に証明した範囲の再組織化です。思弁部には【思弁】と明記します。
⚠ $u$/$c$ 非接触・封印非接触・prereg 非抵触。

---

## §0 一段落の要約

三層列 $\mathrm{settled}(-)\hookrightarrow GT(-)\twoheadrightarrow\mathcal C(-)$ は、**groupoid $\mathcal{GTSh}$ 上の表現可能前層 $h_N=\mathcal{GTSh}(-,N)$ のパッケージそのもの**である(§1)。この視点では定理 TORSOR は「**自由 $G$-集合の圏は $\mathbf{Set}$ と同値**」の脱圏化にすぎず(§3.1)、定理 SUBTOR は「**groupoid 射の像は部分 groupoid**」+ TORSOR である(§3.2)。Cor 5.4 は「**有限逆系のコンパクト性**」(§3.3)。⟹ **形式は全部普遍性で書けます。** しかし**実質はそこにありません**: 本当に効いたのは補題 COMP-T(正典の合成 (3.53) が誘導写像の合成であることの同定)と補題 DIFF-S(isolated ⟹ 誘導写像が全単射)で、どちらも**正典の具体式に依存し、普遍性からは出ません**(§5)。一方 Frattini 手術の「反射(左随伴)」化は **$p$ 群では成立し、我々の設定では成立しません**(§2)— ただし必要な範囲(**全射の圏**)では関手であり、そこでは族公式の自然性が無料になります。最後に、普遍性が触れないものが 1 つだけ明確にあります: **算術像の大きさ**(§5.3)。

---

## §1 三層列の普遍性による特徴づけ

$\mathcal{GTSh}$ を正典の groupoid(対象 = 窓 $N\in\mathrm{NFI}_{PB_3}(B_3)$、射 = shadow、合成 (3.53)、逆 (3.54))とする。

### 1.1 三層の正体

| 層 | 圏論的正体 | 普遍性 |
|---|---|---|
| $\mathrm{settled}(N)=GTSh(N,N)$ | ★ **頂点群 $\mathrm{Aut}_{\mathcal{GTSh}}(N)$** | 自己射のなす群(定義そのもの) |
| $GT(N)=\coprod_K GTSh(K,N)$ | ★ **表現可能前層 $h_N:=\mathcal{GTSh}(-,N)$ の元の圏 $\int h_N$**(= $N$ への costar) | **米田**: $\mathrm{Nat}(h_N,F)\cong F(N)$ ⟹ $h_N$ は $N$ が表現する前層 |
| $\mathcal C(N)$ | ★ **$h_N$ の台 $\mathrm{supp}(h_N)$**(= $N$ の連結成分) | §1.2 の**余等化子** |

⟹ **層の名前がそのまま普遍的対象になります**。「settled 層」= 自己同型群、「$GT(N)$」= 表現可能前層の全空間、「$\mathcal C(N)$」= その台。

### 1.2 $\mathcal C(N)$ は余等化子(軌道空間の普遍商)— **YES**

$\mathrm{settled}(N)$ は左合成で $GT(N)$ に作用し(補題 COMP-T)、核類を保つ(補題 2)。核写像 $\kappa:GT(N)\to\mathcal C(N)$ について:

$$\boxed{\ \kappa\ \textbf{は }\mathbf{Set}\ \textbf{における余等化子}\quad \mathrm{settled}(N)\times GT(N)\ \underset{\mathrm{pr}_2}{\overset{\text{作用}}{\rightrightarrows}}\ GT(N)\ \xrightarrow{\ \kappa\ }\ \mathcal C(N)\ }$$

すなわち $\mathcal C(N)$ は「**軌道上で定数になる写像の普遍的な受け皿**」。⟹ 発注の問い「$\mathcal C(N)$ は settled 作用の余等化子か」への答えは **YES** です。
★ **証明は定理 TORSOR の推移性そのもの**(軌道 = ファイバー)。⟹ 普遍性の言明としては**新しい内容を含みません**(§5.2)。

### 1.3 三層列の「完全性」の意味

$GT(N)$ は群ではないので群の完全列にはなりません。正しい言い方:

$$\boxed{\ GT(N)\ \textbf{は }\mathrm{settled}(N)\ \textbf{の}\textbf{自由}\textbf{作用をもつ集合で、}\ \mathcal C(N)=GT(N)/\mathrm{settled}(N)\ }$$
$$\Longleftrightarrow\quad GT(N)\to\mathcal C(N)\ \textbf{は主 }\mathrm{settled}(N)\textbf{-束(各ファイバーがトーサー)}$$

⟹ 「三層の短完全列」は**主束の言葉**に翻訳するのが正確です。⚠ AT-4 の Q-STAB の関門もこの言葉で綺麗に出ます: $GT(-)$ は $R$ により**常に**前層だが、$\mathcal C(-)$ への商が自然になるには構造群の作用が窓区間を安定化する必要がある ⟹ **前層の射が主束の射に持ち上がるか**という問い。

---

## §2 手術の普遍性 — Frattini 商は反射か

### 2.1 $p$ 群なら **YES**(左随伴・単位射は商写像)

$A$ を基本可換 $p$ 群とすると、任意の $\varphi:G\to A$ は $\Phi(G)=[G,G]G^p$ を殺す($G/\ker\varphi$ が基本可換 ⟹ $\ker\varphi\supseteq\Phi(G)$)⟹
$$\mathrm{Hom}_{\mathbf{ElAb}_p}\bigl(G/\Phi(G),A\bigr)\ \cong\ \mathrm{Hom}_{\mathbf{Grp}_p}(G,A)$$
$$\boxed{\ \Longrightarrow\ \mathbf{ElAb}_p\subseteq\mathbf{Grp}_p\ \textbf{は反射部分圏、}L=(-)/\Phi(-)\ \textbf{は左随伴、単位 }\eta_G:G\twoheadrightarrow G/\Phi(G)\ }$$

⟹ 発注の問い「反射 = 左随伴として書けるか」への答えは **$p$ 群では YES**。

### 2.2 ⚠ しかし我々の設定では **NO**(2 つの理由)

**(理由 1)対象が $p$ 群でない**: $Q\cong SL(2,\mathbf Z/691^2)$ 型で、SL-GAP-3 の $\Phi(Q)$ は $\{\pm I\}$ の逆像、$Q/\Phi\cong PSL(2,691)$ — **基本可換ではありません**。⟹ 「基本可換への反射」ではない。

**(理由 2)★ $(-)/\Phi(-)$ は一般には関手ですらない**: $f:G\to H$ に対し $f(\Phi(G))\subseteq\Phi(H)$ は**全射 $f$ でのみ**成立します(非生成元の像が非生成元になるのは全射のとき)。包含写像では偽。
$$\boxed{\ \Longrightarrow\ \textbf{「手術 = reflector・手術検定 = 単位射の同型判定」という定式化は}\textbf{不成立}\ }$$
⚠ さらに「単位射の同型判定」は意味がずれます: $\eta_G$ が同型 $\iff\Phi(G)=1\iff G$ が既に基本可換 — これは「手術する必要がない」であって「手術が情報を保つ」ではありません。**正しい問いは $L$ が当該対象の上で忠実(単射)か**です。

### 2.3 ★ 救済 — 必要な範囲では成立し、しかも自然性が無料

我々が実際に使う圏は **窓と reduction**、すなわち
$$\mathcal W:\quad \text{対象 }=\ \mathrm{NFI}_{PB_3}(B_3),\qquad \text{射 }=\ M\le N\ \text{に対する全射 }B_3/M\twoheadrightarrow B_3/N$$
— **すべて全射**です。⟹ 理由 2 は消え、$\mathcal W$ 上で $(-)/\Phi(-)$ は**関手**。

$$\boxed{\ \Longrightarrow\ \textbf{族公式(T3)の自然性は「関手の間の自然変換」であり、}\eta\ \textbf{の自然性として}\textbf{無料}\ }$$

★ **これが §2 の唯一の実質的な収穫**です: 反射(随伴)は諦める代わりに、**全射の圏に制限すれば自然性は証明不要**になります。⚠ ただし $\Phi$-商が「何への普遍近似か」は $p$ 群を離れると言えません — **手術は普遍構成ではなく、単なる関手**です。

---

## §3 定理 TORSOR / SUBTOR の位置

### 3.1 TORSOR = 「自由 $G$-集合の圏 $\simeq\mathbf{Set}$」の脱圏化

群 $G$ に対し
$$\{\text{自由 }G\text{-集合}\}\ \xrightarrow{\ X\mapsto X/G\ }\ \mathbf{Set}\qquad(\text{準逆 }S\mapsto G\times S)$$
は**圏同値**。$GT(N)$ は自由 $\mathrm{settled}(N)$-集合(§1.3)⟹ 対応する集合が $\mathcal C(N)$。基数を取ると
$$\boxed{\ \lvert GT(N)\rvert=\lvert\mathrm{settled}(N)\rvert\cdot\#\mathcal C(N)\ }$$
$$\Longrightarrow\ \textbf{計数公式は圏同値の}\textbf{脱圏化}\textbf{(= 基数を取っただけ)}$$
★ しかも「表現可能前層は台の上でトーサー」は **groupoid では米田レベルの形式的事実**です。⟹ **TORSOR の「トーサーである」部分に数学的内容はありません**(§5.2 で正直に記帳)。

### 3.2 SUBTOR = 「groupoid 射の像は部分 groupoid」+ TORSOR

$M$ isolated、$G\le GT(M)$。reduction $R_{M,N}$ は(定義可能な範囲で)groupoid の構造と両立し、像 $X=R(G)$ について:
- **像が部分 groupoid をなす**ことの検証 = 補題 R-MULT(合成で閉じる)+ **補題 DIFF-S**(同核な差が settled = 頂点群に落ちる)
- 部分 groupoid の頂点群 $S_X$ に対し、その star は §3.1 で再びトーサー

$$\boxed{\ \lvert X\rvert=\lvert S_X\rvert\cdot\#\mathcal C_X\ }$$
⟹ **SUBTOR = 「像は部分 groupoid」+ TORSOR**。★ ここで isolated 性が効くのは DIFF-S の**ただ 1 点**($\bar T_T$ が全単射)であり、それは**普遍性ではなく有限性**(全射自己準同型 + 有限 ⟹ 単射)から来ます。

### 3.3 cofinality と pro-対象 — Cor 5.4 は**コンパクト性**

Thm 5.2: $\widehat{GT}_{\rm gen}\cong\varprojlim_{\text{isolated}}GT(N)$。Prop 3.14 で isolated poset は cofinal ⟹ **cofinal 部分図式上の極限は一致**(極限の普遍性の標準補題)。
Cor 5.4(genuine $\iff$ 全細分に survive)を圏論で読むと:
$$\mathcal{PR}_N\bigl(\varprojlim_K GT(K)\bigr)\ =\ \bigcap_K \mathrm{Im}\,R_{K,N}$$
⚠ 「極限の像 = 像の共通部分」は**一般の逆極限では偽**です(Mittag-Leffler 条件が要る)。ここで成立する理由は
$$\boxed{\ \textbf{各 }GT(K)\ \textbf{が}\textbf{有限}\ \Longrightarrow\ \text{空でない有限集合の逆系の極限は空でない(コンパクト性 / König)}\ }$$
$$\Longrightarrow\ \textbf{Cor 5.4 は「pro-有限性」そのもの — 普遍性 + 有限性}$$
★ これは**綺麗な同定**だと思います: 正典の主定理級の言明が、pro-対象の圏の標準性質に帰着します。⚠ もちろん Cor 5.4 自体は正典の定理で、私は**読み替えただけ**です。

---

## §4 発案 7 の 2 因子分解は「積の普遍性」か — **NO(index の乗法性です)**

$$\frac{\lvert GT(N)\rvert}{\lvert a_N(G_{\mathbf Q})\rvert}=\underbrace{\frac{\lvert\mathrm{settled}(N)\rvert}{\lvert S_{\rm arith}\rvert}}_{\textbf{構造群の指数}}\times\underbrace{\frac{\#\mathcal C(N)}{\#\mathcal C_{\rm arith}}}_{\textbf{底空間の指数}}$$

圏論的な内容は「主 $S$-束 $P\to B$ の部分主 $S'$-束 $P'\to B'$ について指数が乗法的」という**主束の初等的事実**であり、極限・余極限・随伴のいずれの普遍性でもありません。
$$\boxed{\ \textbf{答え: 積の普遍性ではない。三層列(= 主束構造)に沿った}\textbf{指数の乗法性}\ }$$
★ ただし**効用はあります**: 発案 5 の「非可換 crown」— crown 検定は $A=a_N(G_{\mathbf Q})$ が**部分群**であることを要求し、非 isolated 窓($GT(N)$ が群でない)で破綻しました。主束の言葉ではこれが自然に置き換わります:
$$\boxed{\ \textbf{「部分群の指数」}\ \rightsquigarrow\ \textbf{「部分主束の 2 つの指数(構造群・底空間)」}\ }$$
⟹ ★ **群の枠を失った代わりに束の枠が入る** — これが発案 5 の圏論的な着地点だと思います(【思弁】: crown 検定の具体的な再構成は未着手)。

---

## §5 ★ 限界の正直な三分

### 5.1 普遍性で**書けること**

| 事項 | 普遍性 |
|---|---|
| 三層列 | groupoid 上の表現可能前層 $h_N$(米田) |
| $\mathcal C(N)$ | 余等化子(軌道の普遍商) |
| $GT(N)\to\mathcal C(N)$ | 主 $\mathrm{settled}(N)$-束 |
| Cor 5.4 | 有限逆系のコンパクト性(+ cofinality) |
| reduction の関手性・T3 自然性 | **全射の圏 $\mathcal W$ 上での**関手性と単位の自然性 |
| Q-STAB | 前層の射が主束の射に持ち上がる条件 |

### 5.2 ⚠ **書き直しただけ**のこと(内容は普遍性の外にある)

| 見かけ | 実際に効いた中身 |
|---|---|
| 定理 TORSOR の「トーサー性」 | ★ groupoid では**形式的**。実質は **補題 COMP-T** — 正典の合成 (3.53) が誘導写像の合成 $\bar T_s\circ T_t$ **であること**の生成元計算。これは $\mathcal{GTSh}$ が groupoid であるという抽象論からは出ません(source/target 規約が決まらない) |
| 計数公式 $\lvert GT\rvert=\lvert\mathrm{settled}\rvert\cdot\#\mathcal C$ | 圏同値の脱圏化(基数を取っただけ) |
| SUBTOR | ★ 実質は **補題 DIFF-S**。しかもその鍵は「isolated ⟹ $\bar T_T$ 全単射」= **有限性**であって普遍性ではない |
| 2 因子分解 | 指数の乗法性(§4) |

$$\boxed{\ \textbf{教訓: 普遍性は}\textbf{整理}\textbf{はするが}\textbf{証明}\textbf{はしない。本線の 2 定理の証明は正典の具体式 (3.53)(3.60) に依存する}\ }$$

### 5.3 ⚠⚠ 普遍性で**書けないこと** — 算術入力の在処

$\mathrm{Ih}:G_{\mathbf Q}\to\widehat{GT}_{\rm gen}$ は群準同型で、$a_N=\mathcal{PR}_N\circ\mathrm{Ih}$ は極限の射影との合成 — **ここまでは完全に圏論的**です。しかし:

$$\boxed{\ \textbf{像の}\textbf{大きさ}\ \bigl(\lvert S_{\rm arith}\rvert\ \textbf{と}\ \#\mathcal C_{\rm arith}\bigr)\ \textbf{は圏論から一切出ません}\ }$$

- $S_{\rm arith}$ が $\mathrm{settled}(N)$ の**どの**部分群か = 算術(Belyi/Kummer receipt)
- $\mathcal C_{\rm arith}$ が $\mathcal C(N)$ の**どの**部分集合か = 同上
- $N'$ ではこれが $f_c$ の 1 ビットに落ちますが、**その 1 ビットの値は圏論では決まりません**

⟹ ★ **普遍性は分母($GT$ 側)を完全に整理するが、分子(算術像)には何も言わない。** これは検分の結論「どの装置も SURG-A6 の代金を 1 円も安くしない」の圏論版です。

$$\boxed{\ \textbf{手術とトーサーの関係}:\ \textbf{手術は}\mathcal W\ \textbf{上の関手、トーサーは各対象上の主束構造 — }\textbf{両者は「窓の圏の上の束の幾何」で一つに書ける}\textbf{。}\ }$$
$$\textbf{ただしその幾何は分母だけを記述し、算術は「どの部分束か」という}\textbf{余分なデータ}\textbf{として外から入る。}$$

---

## §6 記帳

- **格**: candidate・**展望ノート**(Sol 監査対象外)。**新規の数学的主張なし**。
- ★ **本ノートで新しく言えたと思う点**(いずれも既証明範囲の再組織化):
 ① 三層列 = groupoid 上の表現可能前層のパッケージという同定(§1.1)
 ② $\mathcal C(N)$ の余等化子性(発注の問いに YES・§1.2)
 ③ **Frattini 反射は $p$ 群限定で、我々の設定では不成立**。ただし全射の圏では関手で、T3 自然性は無料(§2)— ★ 発注の問いに対する**明確な NO + 救済**
 ④ Cor 5.4 = **有限逆系のコンパクト性**(§3.3)
 ⑤ 2 因子分解は積の普遍性ではなく指数の乗法性(§4)、ただし**非可換 crown の置換先が「部分主束の 2 指数」**(§4・【思弁】)
 ⑥ ★ **実質は COMP-T と DIFF-S にあり、普遍性からは出ない**という正直な三分(§5)
- 【思弁】ラベル: §4 の crown 検定の再構成、§1.3 末尾の Q-STAB の持ち上げ解釈。
- **申告**: 紙のみ(機械走行ゼロ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**。
