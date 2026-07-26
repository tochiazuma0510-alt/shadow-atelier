# 影工房 便 32 返信 — \(K^{(5)}\) campaign gate 再監査

## 総合判定

\[
\boxed{\textbf{差戻し（発射条件③はなお NO-GO）}}
\]

**Rule 1 v1 を凍結 1 としては受理しない。したがって、現時点では
S5 の個別モデル探索を解禁しない。**

便 31 の四 blocker の大部分は実質的に修理された。とくに、

- K5-sq / K5-ns の実データと三つの SHA-256、
- 凍結 1 の厳密な時点、両翼 atomic joint freeze、
- formal \(a=1\) と \(b_{\rm sq},b_{\rm ns},a_{\rm eff}\) の型分離、
- exact Kummer 証明書、二経路、whitelist、integrity stop、
- 補題 S5-B と、それから従う
  \(\operatorname{ord}[P_0-P_\infty]=5\)、\(\lambda=c\mu^2\)

は監査に耐える。

しかし、発射前に塞ぐべき blocker が残る。

1. Rule 1 §2 の M4「重み付き content が極小」はアルゴリズムになっていない。
   重み、各素数で除く指数、零係数の扱いが未定義であり、M3 も
   denominator clearing の仕方を一意にしていない。従って
   「Model-Builder の選択自由度はゼロ」という裁定 30 の前件がまだ立たない。
2. manifest の結果規則は
   `UNKNOWN + UNKNOWN` を落としており、結果状態から記録状態への全関数に
   なっていない。
3. K3 regression JSON の
   `tau_rho0_j_orientation` は、名前に反して \(\tau\) しか記録せず、
   \(\rho_0\) と \(j\) の実値・向きを欠く。manifest §較正三層 2 の要求を
   満たしていない。
4. 通知の「S5-1/2/3 が二系統化済み」には同名異義がある。二つの照合器が
   `S5.3` と呼ぶのは **補題 S5-B の中間部分群個数**であって、
   設計書の **命題 S5-3（曲線の二枝正規形）ではない**。
   後者には実際に符号の不整合があり、M-B を第一次規則へ昇格できない。
5. Rule 1 が要求する数体演算・因数分解器・二経路実装・第三 checker の
   版/commit はまだ値として埋まっていない。文献ゲート 02 は数学的仕様の
   出典を閉じるが、実装 seal の代用にはならない。

| 対象 | 判定 |
|---|---|
| manifest v1.2 の骨格 | **条件付き PASS** |
| K5-sq / K5-ns fixture と SHA-256 | **PASS** |
| 新設した二 tie-break | **条件付き PASS**（二つの定義追記） |
| K3 regression fixture | **差戻し** |
| 結果規則・停止規則 | stop は **PASS**、結果規則は **差戻し** |
| I-b 厳格版 | **採用** |
| Rule R1-C を緩和に使わない | **PASS** |
| 経路 B-ii の独立性 | **条件付き PASS** |
| U-c \(600\) 秒/ジョブ | **採用**（作用節へ移記） |
| 文献ゲート 02 | 仕様 provenance として **PASS** |
| 補題 S5-B / 命題 S5-1 / S5-2 / S5-4 | **PASS** |
| 命題 S5-3 と母数 \(2/3\) | **差戻し / generic count に降格** |
| M-B の第一次規則への昇格 | **NO** |
| 凍結 1 / 個別モデル探索 | **NO-GO** |

---

## F1. manifest v1.2 と付録 A

### F1.1 便 31 の主要修理

凍結 1 の時点から「または初期」を削除し、探索コマンド実行前としたこと、
凍結 2 を両翼の atomic bundle としたこと、formal \(a\) を永久不変にして

\[
a_{\rm eff}=b_{\rm ns}^{-1}ab_{\rm sq}
\]

を別欄にしたことはすべて **PASS** である。

exact witness/obstruction、二経路不一致時の救済禁止、Model-Builder の
whitelist、役割別 access log、発射錠の digest 束縛、暦日と委嘱回数の
早い方で発火する撤退条件も、便 31 P2–P8 を実質的に満たす。

### F1.2 SHA-256 と canonical serialization

三ファイルを静的に再読し、ローカルで SHA-256 を取り直した。

| fixture | 再計算した SHA-256 | 付録 A |
|---|---|---|
| K5-sq | `a49252af8a09031137ee2a5621b7a1eb9c2a6506849afad14dfe74a38a876716` | 一致 |
| K5-ns | `0ce28a6d6b7a3687dc07811f66a05fede464bc3a30efb1a126a913adfa2ccd81` | 一致 |
| K3-regression | `70f2a6040d0bff85e4c597a6059cfb7151193f1de0c23d20a53f0dc9b2529ed9` | 一致 |

三つとも UTF-8 BOM なし、CR なし、末尾 LF ありである。
`sortKeysDeep`、compact JSON、末尾 LF を hash 対象に含める実装も
付録 A §0 と一致する。

ただし `sha256` は当然ながら自己 hash される JSON payload 内には置けない。
manifest の「7 field」は、

\[
\text{payload の 6 field}+\text{外部 envelope の digest}
\]

であると一行明記すべきである。これは循環 hash を避ける型の明確化であり、
現在の三値を否定するものではない。

### F1.3 新設 tie-break

代表 \(H\) を共役類内の要素集合の数値辞書式最小で取る規則は、
有限集合上の全順序なので一意であり、\(u\) に依存しない。
また \(\langle X\rangle\) が 10 点上 regular なので、

\[
\operatorname{label}(X^iH)=i\qquad(0\le i<10)
\]

は全点を一意にラベルし、方向を \(X\) に固定すれば回転・反転は残らない。
従って二規則の数学的内容は **PASS** である。

ただし付録 A には次の二行を足す必要がある。

1. 「要素 \(0,\ldots,499\)」は、昇順に並べた raw \(D_5^3\) code の
   \(G_5\)-list における index であること。
2. coset と manifest の共役類作用を結ぶ写像
   \[
   gH\longmapsto gHg^{-1}
   \]
   を明記すること。これは \(N_{G_5}(H)=H\) により全単射で、
   \(X\) の左乗算と \(X\) の左共役を intertwine する。

実装では \(G\) を raw code 昇順にしてから index 化しているため、
現値はこの追記と整合している。

### F1.4 K3 regression の欠品

`K3-regression.json` の
`tau_rho0_j_orientation` に実在するのは
`tau_definition`, `note`, `source` だけである。
\(\rho_0\) の generator/image と \(j\) の表または式はない。
付録 A §2 の表も \(\tau\) の行しか持たない。

manifest は K3 regression に「\(\tau/\rho_0/j\) の向き」を要求しているので、
これは field 名で要求を満たしたことにはならない。実値を追加し、
JSON と付録 A の digest を更新すること。併せて `good[0]` の列挙順依存については、
現在書かれた明示三つ組と明示 \(h\) を authoritative value とし、
`good[0]` は再現 recipe ではなく provenance に降格するのがよい。

### F1.5 結果規則

manifest の七項目は次の unordered pair を網羅していない。

\[
(\mathrm{UNKNOWN},\mathrm{UNKNOWN}).
\]

これは FAIL を含まないので、現行の
「FAIL+UNKNOWN / 両 FAIL」の行には吸収できない。少なくとも

\[
\begin{array}{c|c}
\text{状態} & \text{記録}\\ \hline
\mathrm{UNKNOWN}+\mathrm{UNKNOWN}
& \texttt{pair\_gate=OPEN},\
  \texttt{saturation\_result=NOT\_PROVED},\
  \text{falsifier なし}
\end{array}
\]

を足すこと。また各行で
`bridge_result_sq/ns`, `pair_gate`, `saturation_result`
の値をすべて埋め、結果規則を prose でなく total transition table にすること。

即時 stop 一覧そのものは十分に fail-closed で **PASS**。
ただし親 manifest の whitelist/stop にも Rule 1 I-b と同じ
「\(c\) の平方類・平方因子・符号、分離した \((c,\mu)\)」を明記し、
親子文書の禁止集合を一致させるべきである。

---

## F2. Rule 1

### F2.1 向き、\(a/b_i\)、sheet、uniformizer

ordered \(0,1,\infty\)、左作用、積の向き、\(\zeta_{20}\) の複素埋め込み、
\(a=1\) の不変性、\((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times\) の
別 seal は整合している。

補題 R1-U も正しい。二つの intertwiner があればその比は monodromy の
centralizer に入り、

\[
C_{S_{10}}(\operatorname{Mon})
\cong N_{G_5}(H)/H=1
\]

だから一意である。「二個返ったら UNKNOWN でなく入力破損の integrity stop」
も正しい。

Rule U-1 は \(u\) に触れず有理 uniformizer を決めるので **PASS**。
R1-C は Kummer class の covariance を示すだけであり、生の \(u\) の
二経路比較に使う \(t\) を曖昧にしてよい理由にはならない。
従って「R1-C を規則緩和に使わない」判断を **承認**する。

U-2 は検査路なので launch blocker とはしないが、
「モデルの単項式順序（固定）」の具体的な順序と、RREF を取る ambient
coefficient vector を書かないと再現不能である。次版で埋めること。

### F2.2 M4 は現在 total algorithm でない

M2 で変換則は書かれているが、M4 の

> 重み付き付値 \(\min_p\lfloor\cdot\rfloor\)

には被 floor 数さえ書かれていない。例えば枝 (W) で

\[
f_5=x^5+\sum_{j=0}^4 A_jx^j,\qquad
w_j=2(5-j)
\]

と置き、M3 後の各素数 \(p\) について

\[
k_p=\min_{A_j\ne0}
\left\lfloor\frac{v_p(A_j)}{w_j}\right\rfloor,\qquad
\tau_+=\prod_p p^{k_p}
\tag{2.1}
\]

として \(A_j\mapsto A_j/\tau_+^{w_j}\) とする、という程度まで必要である。
枝 (N) では

\[
f_6=x^6+\sum_{j=0}^5 B_jx^j,\qquad
w_j=6-j,\qquad
k_p=\min_{B_j\ne0}
\left\lfloor\frac{v_p(B_j)}{w_j}\right\rfloor .
\tag{2.2}
\]

零係数は minimum から除外し、符号単元は M5 へ回す。
さらに、M3 で余分に denominator を clear しても (2.1)/(2.2) の
\(k_p\) が同じだけずれて最終 vector は同一になることを短く証明する。
この記述があれば、weighted primitive 後に残るのが
枝 (W) の \(\tau=\pm1\)、枝 (N) の \(t=\pm1\) だけだという §3.1 が初めて立つ。

現状では M3 の過剰 clearing により無限個の integral representative を作れ、
M4 がどれを戻すか実行できない。これは表記上の軽微な欠落でなく、
blind selection function の load-bearing blocker である。

### F2.3 I-b と「可視性 \(\times\) 選択自由度」

I-b 厳格版を **採用**する。凍結 2 前には

- \(c\) の平方類・平方因子・符号を計算しない、
- \(\lambda\) を \((c,\mu)\) の対として報告しない、
- それらを候補選択に使わない、

を維持すべきである。

裁定 30 の「漏洩実害 = 可視性 \(\times\) 選択自由度」という分析も原理として
正しい。ただし「選択自由度ゼロ」は、正規化が **total, executable,
pre-frozen** であるときだけ成立する。M4 が未定義の現版では、
この分析を I-b の代替根拠に使えない。

また M-B を通常の Model-Builder 探索規則にすると、solver はまさに
\(c\) を明示変数として扱う。これは strict I-b と同時には運用できない。
M-B を使うなら、全候補列挙、M-A canonicalization、両翼共同 freeze までを
人間から隔離した sealed automation として別 schema に書く必要がある。
現 v1 では M-A を正本、M-B を凍結後の整合検査に留める。

### F2.4 \(u\) の二経路と B-ii

B-ii の

\[
u^{(B)}
=\frac{A^{(5)}(x_0)/120}{f'(x_0)^5}
\]

は曲線上の Hensel/Newton 級数を作らず、
\(\mathbb Q[x]\) 内の Taylor 係数と一点評価だけを使う。
従って、経路 A と helper/data structure を共有せず、
raw intermediate を別保存するという §6.3 が実装でも守られる限り、
**独立経路と認める**。多項式の Taylor 係数という語だけを理由に
「級数経路」と同一視しない。

B′ は \(\lambda=c\mu^2\) に依存する第三経路であり、B の代替にしないという
現規定も正しい。

### F2.5 U-c と文献ゲート 02

\(600\) 秒/判定ジョブを採用する。ただし値を未決論点 §11 に置くのでなく、
§9.1 U-c の作用行へ

> M0 の一判定ジョブにつき wall-clock 600 秒。timeout は U-c。
> 同 campaign 内で上限を増やして再分類しない。

と移すこと。

文献ゲート 02 は、\(\zeta_2,\zeta_5\in K\) のもとで
平方・五乗判定へ分解する exact Kummer 仕様と、
valuation obstruction / binomial factorization の数学的 provenance を
閉じるものとして **PASS** とする。
ただし私は本便で Cohen/Roblot の一次 PDF と定理番号を独立照合していない。
また文献は executable certificate checker ではない。凍結 1 の最終 bundle には
§8.6 が要求する library 名・版・commit、アルゴリズム、経路 A/B と第三 checker
の commit を**値として**入れること。

---

## F3. 裁定 30 の 2-part / 5-part 分析

結論は **正しい。ただし言い方に一つ但し書きが要る。**

CRT により

\[
K^\times/K^{\times10}
\longrightarrow
K^\times/K^{\times2}\times K^\times/K^{\times5}
\]

で class を 2-primary 座標と 5-primary 座標に分けられる。
\(u=cv^2\) なら

\[
[u]_2=[c]_2,\qquad
[u]_5=[c]_5[v]_5^2.
\tag{3.1}
\]

従って

\[
\text{(P1)}
\iff [u]_2=1
\iff [c]_2=1.
\]

`sqfree(c)` が漏らすのはまさにこの 2-primary bit であり、
(P1) が通った後に class の位数が \(1\) か \(5\) かを決める
5-primary 座標は \(c\) **だけ**からは読めない。

但し \([c]_5\) が式 (3.1) に寄与しないわけではない。
正確な表現は

> \(c\) の**平方類**は 2-part を完全に決めるが、
> \(c\) 単独では \([c]_5[v]_5^2\) の自明性を決めない

である。「\(c\) は 5-part を持たない」と一般化してはならない。

---

## F4. S5 設計

### F4.1 補題 S5-B

紙上証明は通る。core は

\[
\operatorname{Core}(H)=\langle e_2\rangle\cong C_5,
\qquad |\operatorname{Mon}|=100.
\]

\(\bar H\) を含む真の中間群の候補位数は \(20,50\) だけである。
位数 20 なら \(K\cap V\) は
\(\langle\alpha\bar e_1+\bar e_3\rangle\) を含む \(q_1\)-安定な線でなければ
ならないが、\(\alpha\ne0\) では不可能。位数 50 は

\[
V\rtimes\langle q_2\rangle
\]

の一個だけである。従って非自明ブロック系は
2 blocks \(\times\) size 5 の一つだけであり、\(X,Z\) は交換、\(Y\) は保存する。

開示された GAP certificate は 34/34、node は 36/36、
相互突合は 13/13 で、この有限群論部分に一致する。
両実装の探索路も GAP の subgroup/block 機能と node の自前悉皆で分かれている。
従って補題 S5-B の有限入力は **cross-checked と報告された artifact を静的に
突合済み**として受理する。Lean の `verified` ではない。

### F4.2 S5-1 / S5-2

唯一のブロック系は \(\mathbb Q\) 上 Galois-stable なので中間被覆 \(Y\) へ降りる。
\(Y\to\mathbf P^1_\lambda\) は \(0,\infty\) の二点だけで分岐する次数 2 被覆。
Riemann–Hurwitz で \(g(Y)=0\)、さらに \(\lambda=0\) 上の唯一の点が
\(\mathbb Q\)-有理なので \(Y\cong\mathbf P^1_{\mathbb Q}\)。
従って適当な \(\mathbb Q\)-座標 \(\mu\) で

\[
\lambda=c\mu^2,\qquad c\in\mathbb Q^\times.
\]

ここから

\[
(\mu)=5P_0-5P_\infty
\]

となり、位数 1 は既に排除済みなので
\(\operatorname{ord}[P_0-P_\infty]=5\) ちょうどである。
ブロック上の型 \((5,2^21,2^21,5)\) と位数 10 の非可換群から
monodromy \(D_5\) も従う。S5-1/S5-2 は **PASS**。

### F4.3 「機械 S5.3」は命題 S5-3 ではない

`search/k5-blocks-check.g` と
`crosscheck/check-k5-blocks.mjs` は自ら、

> S5.3 = \(|K|=20\) が 0 個、\(|K|=50\) が 1 個

と定義している。これは補題 S5-B の一部である。
曲線方程式、norm identity、二重根条件、母数数えを入力にも出力にも持たない。
従って通知の「S5-1/2/3 二系統化」は、

\[
\text{S5-B/S5-1/S5-2 の有限群部分}
\]

までに読み替える必要がある。命題 S5-3 の二系統証拠ではない。

### F4.4 命題 S5-3 の符号

\[
N=\mu\mu^\iota=a^2-b^2f=c_N(x-x_0)^5
\tag{4.1}
\]

とする。枝 (W) で \(b=1\) なら (4.1) から

\[
f=a^2-c_N(x-x_0)^5.
\tag{4.2}
\]

ところが設計書は同じ記号 \(c_5\) を保ったまま

\[
y^2=a^2+c_5(x-x_0)^5
\]

と書く。これは \(c_5:=-c_N\) と**改名した場合だけ**正しい。
直前の「\(c_5=-b_0^2\operatorname{lc}(f)\)」とも現表記のままでは逆符号になる。
枝 (N) の (3.3) は再び \(c_N\) 側の符号を使っているので、単なる一箇所の
typo として黙って吸収できない。

さらに \(b=1\) と \(f\) monic を同時に gauge 固定すれば
\(\operatorname{lc}(f)=-c_N\) により \(c_N=-1\) である。
\(c_N\) を自由母数として残すなら、どの scaling をまだ quotient していないかを
明記する必要がある。正規形と母数商の gauge を一つに統一すること。

枝 (W) で \(P_0\) が Weierstrass にならない結論自体はよいが、
\(a(x_0)=0\) なら (4.2) の \(f\) は \(x_0\) で少なくとも二重に消え、
滑らかさに反する、という証明が直接である。

### F4.5 母数 \(2/3\)

枝 (W) の

\[
5\text{ 変数}
-x\text{ translation}
-x\text{ scaling}
-\mu\text{ scaling}
=2
\]

は、符号と gauge を修理すれば open locus 上の次元数えとして妥当である。

枝 (N) の

\[
a^2-c_N(x-x_0)^5=f_6p_2^2
\]

について「二つの可動二重根 = 余次元 2」も generic locus では妥当な期待次元
\(8-3-2=3\) を与える。しかし、これを「未知数は正確」とはまだ呼べない。
少なくとも

- \(p_2\) の二根が相異なる、
- \(f_6\) が squarefree、
- \(\gcd(f_6,p_2)=1\)、
- \(\deg f_6=6,\deg p_2=2\) が落ちない、
- \(\infty_-\) で必要な leading cancellation が成立する、
- 退化 strata で二条件が独立である、

を分ける必要がある。従って母数 \(2/3\) は
**generic design count として条件付き PASS**、global normal form theorem としては
未成立である。

### F4.6 S5-4

\[
u=cv^2
\]

から

\[
\operatorname{ord}([u^{-1}]_{10})\in\{1,5\}
\iff c\in K^{\times2}
\iff \operatorname{sqfree}(c)\in\{1,-1,5,-5\}
\]

を得る証明は正しい。最後は
\(K=\mathbb Q(\zeta_{20})\) の三つの二次部分体に対応する。
従って S5-4 は **PASS** であり、I-b を厳格化する根拠と、
凍結 2 後の独立な P1 証明書の両方に使ってよい。

---

## 必須修理

- **P1**: manifest の結果規則へ `UNKNOWN+UNKNOWN` を追加し、
  全行で四つの record field を total に定める。
- **P2**: Rule 1 M3/M4 を (2.1)/(2.2) 型の素数ごとの total algorithm にし、
  denominator clearing 非依存性と有限性を証明する。
- **P3**: strict I-b を親 manifest にも同じ語で反映する。
  M-B は v1 の第一次規則へ上げない。
- **P4**: K3 regression に \(\rho_0,j\) の実値・向きを入れて再 hash する。
  K5 tie-break には group-index 定義と \(gH\mapsto gHg^{-1}\) を追記する。
- **P5**: 命題 S5-3 の \(c_N/c_5\) の符号と scaling gauge を修理し、
  N 枝の母数 3 を generic count と明記する。
- **P6**: U-c の 600 秒を operative table へ移し、Rule 1 の最終 freeze bundle に
  §8.6/§10 の実装版・commit・checker ID を値として埋める。
- **P7**: 上記 delta を反映した Rule 1 と付録 A の新 digest を、
  個別モデル探索コマンドを一度も走らせる前に再提出する。

P1–P7 の差分検収が通れば、M-A を canonical acceptance rule とする
個別モデル探索は解禁可能である。M-B / \(\mu\)-正規形を discovery engine に
使うなら、\(c\) を freeze 2 前に人間へ見せない sealed automation を別途
事前登録すること。

---

## 警告

- **W1**: テスト名が同じでも、テスト対象が同じとは限らない。
  今回の “S5.3” はその具体例である。
- **W2**: 「見えても舵がない」は、舵を殺す canonicalization が実行可能で
  あることを証明した後にだけ成立する。
- **W3**: 群のブロック系は中間被覆と \(\lambda=c\mu^2\) を与えるが、
  超楕円曲線上の係数正規形までは自動的に証明しない。
- **W4**: full Belyi map を許す以上、\(c\) の平方類は原理的に導出可能である。
  strict I-b は語彙 grep でなく、access control と total selection rule で担保する。
- **W5**: 文献、GAP、node の一致はいずれも Lean 証明ではない。
  本便では `verified` の札を上げない。

---

## ★教材

1. **同じラベルの検査は、同じ定理の検査とは限らない。**
   群論的 “S5.3” の PASS を曲線正規形 S5-3 の PASS へ持ち上げてはならない。
2. **blindness の主担保は「選択肢がない」という文章でなく、
   実行可能な total selection function である。**
   weighted minimality の一語では、候補選択の舵はまだ死んでいない。
3. **中間被覆の分解と源曲線の正規形は別ゲートである。**
   ブロック系は \(\lambda=c\mu^2\) を強制するが、
   norm 式の符号・無限遠 cancellation・退化 strata は別に監査しなければならない。

---

## 監査範囲外申告

本便では次を全文または該当 artifact まで静的監査した。

- `sol/sol_task_32_campaign_gate.txt` 全文、
- `docs/対話帳.md` の新着確認（T-11 より後の新着なし）、
- `docs/manifest_k5_v1.md` v1.2 全文、
- `docs/manifest_k5_appendixA_v1.md` 全文、
- `docs/week4-K5_Rule1_v1.md` 全文、
- `docs/week4-K5_S5設計_opus_v1.md` 全文、
- `sol/裁定_29_ben31.md`, `sol/裁定_30_rule1_review.md` 全文、
- `docs/文献ゲート_02_power_residue.md` 全文、
- 三つの `certificates/k5fixture/*.json`、
- `certificates/k5blocks/` の GAP/node certificate、
- `search/k5-fixture-serialize.mjs`,
  `search/k5-blocks-check.g`,
  `crosscheck/check-k5-blocks.mjs` の該当論理。

三 fixture の SHA-256、BOM/CR/LF は本便で独立に取り直した。
GAP/node の 34/34・36/36・13/13 や fixture serializer の 14/14 は
再実行していない。明示 genus-2 モデル、actual marking、\(u\)、
Kummer 実装、(5′)、個別モデル探索はまだ artifact がないため監査していない。
Cohen/Roblot の一次 PDF、外部文献、Lean も本便の範囲外である。
