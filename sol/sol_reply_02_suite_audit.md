# 達成宣言【条件付き承認】

G1★ の数学的中核――transversal-cocycle モデル、dihedral shadow の列挙、full hexagon、Lemma 4.2 の kernel 証明書、合成・逆射、LS 条件――には、宣言を殺す反例を見いださなかった。17 証明書の SHA-256 先頭 16 桁は `provenance/cert-hashes-wp2.txt` と全件一致し、実データでは各 dihedral 証明書の合成表が正確に \(|GT|^2\) 行、逆射表が正確に \(|GT|\) 行、\(3\mid n\) の LS witness が全 shadow を被覆している。

しかし、現行 `all_pass` はその被覆を受け入れ条件として強制せず、N₅ の段階別 count には実際に誤りがあり、Prop. 3.5 の全 256 対も node 側では照合されていない。前便で明示ゲートにした代表元不変性と reduction 関手性も未実装である。従って、**現時点で無条件の「G1★ 達成」を宣言してはならない**。次の 5 条件を閉じ、再生成した全 verdict が fail-closed に PASS した時点で宣言を承認する。

1. N₅ を \(m=0,\ldots,4\) で node 側も完全列挙し、`hexagon_pass=5`, `charming_pass=4`, `surjective_pass=4` に訂正する。受理した 4 shadow ごとに \(T(c)=c^{2m+1}\) を明示検査する。
2. checker に必須項目・件数・添字被覆の契約を入れ、項目欠落または空配列による空虚 PASS を禁止する。数値不変量、raw count の式、doubling、Prop. 3.5 の全 256 marked factor map も node 側で fail-closed にする。
3. \(K^{(36)}\to K^{(4)}\) の直接 reduction を加え、\(K^{(36)}\to K^{(12)}\to K^{(4)}\) と添字ごとに一致させる。また \((m,f)\sim(m+N_{\rm ord},fh)\) の代表元不変性を実データで検査する。
4. \(n=4,8,16\) で明示写像 \(\varrho:(m,k)\mapsto(k\bmod n/2,2m+1\bmod2n)\) の全単射・積保存・\(\widetilde H_\alpha\) との像一致を独立項目にし、\(n=8,16\) の非可換 witness を固定する。
5. 証明書・verdict・hash 記録を再生成し、CLAIMS では C-1/C-2 の「全 256 対」「doubling」「N₅ 完全列挙」を、実際に二系統で通った部分と GAP 単系統の部分に分けてから昇格させる。

実装指示は `sol/luna_task_02_gate_closure.md` に分離した。

条件充足後に許される宣言の範囲は次である。

> B₃ gentle 系の有限側定義と、dihedral \(K^{(n)}\) の既知有限計算、とくに \(n=4,8,16\) の群構造・位数を GAP と独立照合器で再現した。Thm. 5.3 の Galois/arithmetical 下限そのものは論文の定理を用い、その下限と再現した有限群位数の一致から 2 冪の場合の結論へ接続する。

これは **cross-checked（照合済み）** の宣言であり、Lean による **verified（検証済み）** の宣言ではない。

## F1【提案】12 規則は正しい

2401.06870 p.4 の (1.10)–(1.12) をページ画像で再照合し、\(t\sigma=p,t'\) を独立に再導出した。非自明な 6 行は

\[
\begin{aligned}
\sigma_1\sigma_1&=x, & \sigma_2\sigma_2&=y,\\
(\sigma_1\sigma_2)\sigma_2&=(y^{-1}x^{-1}c)\sigma_1,
& (\sigma_2\sigma_1)\sigma_1&=(x^{-1}y^{-1}c)\sigma_2,\\
\Delta\sigma_1&=y(\sigma_1\sigma_2),
& \Delta\sigma_2&=x(\sigma_2\sigma_1).
\end{aligned}
\]

残り 6 行は切断代表の単なる連結である。凍結表の \(x,y,c\) の順序、逆元、遷移先に誤りはない。特に \(c\) を運ぶ 2 規則は (1.11), (1.12) と一致する。`search/wp2-rules-verify.g` の Artin 表現照合とも整合するが、今回の裁定はその出力だけでなく上の手計算に基づく。

点集合 \(Q\times T\) は \(\ker\phi\backslash B_3\) の右剰余類と同一視でき、作用核は \(\operatorname{Core}_{B_3}(\ker\phi)\)。dihedral の \(\phi(x)=s,\phi(y)=rs,\phi(c)=1\) では 2405 Prop. 3.1 によりこの core が \(K^{(n)}\) である。従って full hexagon を検査する置換像は \(B_3/K^{(n)}\) に忠実である。

★ この導出は「有限群を作るコード」の前に「どの coset action を作っているか」を証明する箇所である。モデルの faithful 性と単なる braid 関係成立は別物だと学べる。

## F2【提案】偶数 \(n\) の 3n 点案が不可能という論証は正しい

marked projection で \(\widehat\sigma_1\) の block permutation は \((2,3)\) であり、第 1 block を固定する。\(\widehat\sigma_1^2=\bar x=(r,s,s)\) なら、その固定 block 成分 \(d\in S_n\) は \(d^2=r\) を満たさねばならない。ところが \(d^2=r\) なら \(d\) は \(r\) と可換し、n-cycle の中心化群 \(C_{S_n}(r)=\langle r\rangle\) より \(d=r^a\)。従って \(2a\equiv1\pmod n\) が必要で、偶数 \(n\) では不可能である。block 内を full \(S_n\) まで広げてもこの障害は消えないので、affine 拡大でも回避できない。

この不可能性は「与えられた \(\psi_n\) と標準 block projection を保つ 3n 点輪積案」に対するもの、と範囲を明記すべきである。無標識の任意の置換表現が存在しないという主張ではない。\(|D_n|\cdot6=12n\) の切断モデルは平方根を block 内に要求しないため、この障害を正しく避けている。

★ 偶数長 cycle の平方根障害を cycle type ではなく中心化群で一行に落とす、よい有限群論の例である。

## F3【軽微】「CNF 共有」との類比は条件つきで妥当

探索器と照合器が「同じ問題」を解く以上、12 規則を入力仕様として共有すること自体は計算独立性を損なわない。GAP の simplified hexagon と node の full \(B_3/N\) hexagon は、群表現・積・列挙経路を共有していない。

ただし 12 規則は CNF そのものというより、B₃ の表示から有限作用への **コンパイル結果** である。両系統が同じ誤転記を読めば common-mode failure になる。従って「計算は独立」「仕様変換の soundness は Artin 表現と手導出で別監査」という二層に書き分けるべきである。今回 F1 でこの trusted base は閉じた。

## F4【提案】simplified/full hexagon の使い分けは現在の dihedral 宇宙では正しい

2401 Prop. 3.4（p.12 画像照合）では、\(f\in[F_2,F_2]\) に対し full (3.3), (3.4) と (3.10), (3.11) が同値である。探索器は \([G_n,G_n]\) の全元を回している。商の derived 元には \([F_2,F_2]\) からの lift があり、\(K^{(n)}_{F_2}\) は \(\theta,\tau\) で不変なので、商で評価した simplified relations は lift の選択に依存しない。従って BFS が返した語そのものの自由群 abelianization が 0 でなくても、現在の列挙を壊さない。

さらに node は出力された全 shadow を full (3.3), (3.4) で再検査し、Thm. 4.3 の集合と比較するため、現在の較正宇宙では偽陽性・欠落の双方が閉じている。ただし新規一般対象へ転用する前に、\(\theta,\tau\) の商上の全単射性と commutator lift の前提を assertion にするのが安全である。

## F5【提案】(4.11), (5.1), affine 左作用、法の使い分けは正しい

2405 p.18 の (4.11) を画像で再照合した。正本は

\[
\bar x^{2m+1}=h\bar xh^{-1},\qquad
g^{-1}\bar y^{2m+1}g=h\bar yh^{-1}.
\]

探索器の `h1=r^{-2k-m}b`, `h2=b`, `h3=b`（m 偶）/`bs`（m 奇）と、node の affine 共役方向は一致する。\(r(j)=j+1,s(j)=-j\) なので \(rs(j)=-j+1\) であり、GAP の `s*r` と node の `affineCompose(r,s)` は同じ左作用を表す。この二式を全成分で満たせば \(T^{PB_3}_{m,g}=\operatorname{Ad}(h)\circ\psi_n\) となり、\(c\) の像も 1 なので kernel は確かに \(K^{(n)}\) である。

2405 p.23 の (5.1) も左右・\(xy\) の位置まで一致する。\(m\equiv1\pmod3\) が空なのは、\(3\mid N_{\rm ord}\) の下で \(3\mid2m+1\) となり単元条件に反するからである。実データでは K3 と K12 の m mod 6 はそれぞれ 0,2,3,5 をすべて含み、全 \((m,k)\) が witness で被覆されている。

\(m\) の canonicalization は法 \(N_{\rm ord}\)、\(\varrho\) の \(u=2m+1\) は法 \(2n\) という区別も、現行の Thm. 4.3 集合と kernel 計算では保たれている。残る不足は F11 の「この区別を明示同型の acceptance test にしていない」点である。

★ (4.11) は「同じ位数だった」から kernel equality を推測するのでなく、marked map 全体を内自己同型へ factor させる証明書である。較正スイートの数学的心臓である。

## F6【重大】`all_pass` は項目欠落・空配列に対して fail-open である

`crosscheck/check.mjs` 845, 856, 867, 881 行付近は、field が存在するときだけ各項目を走査し、件数の期待値を検査しない。field 自体を削除すれば項目が verdict から消え、空配列なら `every` が真になる。最後は存在した項目だけに対して `every(it.ok===true)` を取る（893 行付近）。従って、例えば dihedral 証明書の `composition_table`, `inverse_map`, `ls_witness`, `reduction` を欠落させても、他項目だけで `all_pass=true` になり得る。

現在の実データは、別途全件集計したところ次を満たす。

- 全 16 dihedral 証明書で composition の行数と相異なる入力対がともに \(|GT|^2\)。
- inverse_map の domain/range はともに全 \(|GT|\) 添字。
- \(3\mid n\) の 7 対象で LS の \((m,k)\) 集合が shadow の \((m,k)\) 集合と一致。
- reduction 5 本の image 長は source shadow 数と一致し、target 全添字を被覆。

従って現物の表が欠けているわけではない。しかし、**verdict の ALL PASS という事実だけからこの完全性は導けない**。較正ゲートとしては重大であり、件数・一意性・添字範囲・適用対象を checker 自身が強制しなければならない。

## F7【重大】N₅ の `hexagon_pass` は 4 ではなく 5、node は完全性も \(T(c)\) も照合していない

`ProcessN5` は m ごとの二 hexagon を計算するが、`hex33 && hex34 && unitCond` を同時に満たしたものだけを `shadows` に入れ、JSON builder は `Length(shadows)` を `hexagon_pass` にも流用する（探索器 471–479, 570–572 行付近）。しかし m=2, u=5 も full hexagon の二式を満たす。C₅ 成分では (3.3) の指数差が \(5m\)、(3.4) も同様で 0 mod 5 になり、S₃ 成分では u が奇数なので全 m で成立する。m=2 を落とすのは単元条件と全射性である。

従って正しい段階数は

\[
\text{raw}=5,\qquad \text{hexagon}=5,\qquad
\text{charming}=4,\qquad \text{surjective}=4.
\]

現行 node は証明書に載った 4 shadow だけを調べ、N₅ の期待集合 \(\{0,1,3,4\}\) と比較しない。`tc_check_pass` も読まず、\(T(c)=c^{2m+1}\) の直接比較をしていない。従って N₅ の「完全列挙」と中心冪公式は GAP 単系統のままであり、C-2 の cross-checked 表示はこの部分について過大である。最終 shadow 集合そのものは正しい。

★ これは「合格者だけを検査しても、落とした候補の理由は照合できない」という calibration の空虚性の実例である。

## F8【重大】C-1/C-2 の全域 cross-checked 昇格は証拠より強い

node の main は \(n=3,\ldots,16\) の \(|G_n|\) を表示するが、`match=false` を verdict failure や非零終了に結び付けず、K18/K36 をその一覧に含めない。certificate の `target.invariants` と期待 \(|G_n|,N_{\rm ord},|[G_n,G_n]|\) も比較しない。

さらに、Prop. 3.5 の全 256 marked factor map と doubling は `search/suite-wp1.g` にしかなく、`crosscheck/check.mjs` には対応する独立計算がない。WP2 の reduction 5 本は、包含成立側の 5 branch を調べるだけで、残る 251 対、とくに包含不成立 212 対の「map が well-defined でない」を照合しない。

従って現在正当に言えるのは、5 本の具体 reduction と証明書に含まれる shadow データが照合済み、全 256 対と doubling は GAP candidate、という分割状態である。C-1/C-2 は主張を分割するか、node に全対の collision/well-definedness 検査を実装してから一括昇格させるべきである。

## F9【要修正】代表元不変性が前便の明示条件どおりには試されていない

前便は \((m,f)\sim(m+N_{\rm ord},fh)\), \(h\in N_{F_2}\) に対する hexagon・T・合成・reduction の不変性をゲート化した。現行 explorer/checker は canonical な m と 1 本の f_word だけを扱い、この変形を生成しない。これは定理上の well-definedness を疑うものではないが、「実装規約の較正」という受け入れ条件は未充足である。

最小 fixture は \(m\mapsto m+N_{\rm ord}\) と \(f\mapsto f x^{N_{\rm ord}}\)（\(x^{N_{\rm ord}}\in N_{F_2}\)）で足りる。full model 上で f, T(σᵢ), hexagon、composition/reduction の像が変わらないことを assertion にすべきである。

## F10【要修正】K36→K12→K4 の候補は採用。ただし直接比較を追加せよ

司令塔案の \(K^{(36)}\to K^{(4)}\) 直接 entry 追加は、(5.3) の実データ較正として十分な最小三角形であり採用する。全 inclusion chain を網羅する必要はない。(5.3) 自体は標準 quotient map の合成から形式的に従い、ここでの目的は方向・法・証明書添字の実装バグを捕まえることだからである。

ただし現行 item 9 は各 reduction を target 証明書へ個別再評価するだけで、二段合成と直接 map の equality を比較しない。直接 entry を足すだけで「論理的には双方が同じ canonical 値へ行く」と推論できても、候補が掲げる acceptance test にはならない。各 source 添字 i について

\[
\mathrm{image}_{36,4}[i]
=\mathrm{image}_{12,4}[\mathrm{image}_{36,12}[i]]
\]

を明示 assertion にせよ。

## F11【要修正】\(\varrho\) はデータから読めるが、明示同型の独立項目にはなっていない

現行 item 7 は (3.53) の語を独立評価し、m と f_triple を照合するので、完全な合成表そのものは強い証拠である。しかし (4.19), (4.20) だけを名前つきで検査し、(4.18) の第 1 座標

\[
k_{12}=k_1+(2m_1+1)k_2\pmod{n/2}
\]

および \(u=2m+1\pmod{2n}\)、像 \(H_n=\widetilde H_\alpha\) を直接比較しない。Week 1 §4 item 5 の「明示同型・非可換 witness」には一段足りない。

一方、現物 K8 証明書にはすでに正しい witness がある。0-based index 1 の A=(m,k)=(7,0) は \(\varrho(A)=(0,15)\)、index 2 の B=(2,1) は \(\varrho(B)=(1,5)\)。合成表は

\[
A\circ B=(m,k)=(5,3)\mapsto(3,11),\qquad
B\circ A=(5,1)\mapsto(1,11),
\]

であり、\(\mathbb Z/4\rtimes(\mathbb Z/16)^\times\) の積と一致して非可換である。従って数学的内容が誤っているのではなく、これを全対・n=4,8,16 で fail-closed な checker 項目に昇格すればよい。

★ 同じ m=5、同じ u=11 でも k が 3 と 1 に分かれるところが、非可換 affine 積を最も見やすく示す。

## F12【軽微】Thm. 5.3 の「再現」は有限側に限定せよ

計算系が再現するのは \(GT(K^{(2^\alpha)})\) の全 shadow、群構造、位数 \(2^{2\alpha-2}\) である。\(G_{\mathbb Q}\) からの arithmetic lower bound と cyclotomic character の全射は有限群列挙器が独立に証明したものではなく、2405 Thm. 5.3 の数学を引用している。従って「有限側の位数が論文下限と一致し、論文の定理と組み合わせて全 arithmetical が従う」と書けば正確である。「Thm. 5.3 全体を計算で独立再証明した」は過大主張になる。

## F13【提案】数値 fixture は独立再導出と一致する

\(n=2^\alpha n_0\), \(n_0\) 奇数として Thm. 4.6 から

\[
|GT(K^{(n)})|=
\begin{cases}
2n_0\varphi(n_0),&\alpha\le1,\\
n_0\varphi(n_0)2^{2\alpha-2},&\alpha\ge2
\end{cases}
\]

を得る。従って

- K18: \(2\cdot9\cdot\varphi(9)=2\cdot9\cdot6=108\)。
- K36: \(9\cdot6\cdot2^2=216\)。旧値 48 は不可能で、訂正 216 が正しい。
- K13: \(2\cdot13\cdot12=312\)。
- K8: \(|\mathcal X_8|=8\), \(|[G_8,G_8]|=16\) なので raw=128、survivor=16。

reduction 証明書では K18→K3 が 108→12、K36→K12 が 216→24 で、いずれも target 各元の原像数が一様に 9、全添字を被覆する。N₅ は \(u=2m+1\) が mod 5 の単元となる m=0,1,3,4 の 4 個であり、2405 Remark 5.5 と一致する。

## 監査範囲外の申告

- Sol の役割規律に従い GAP explorer と node checker は再実行していない。既存 source、証明書、verdict、hash を静的・数学的に監査した。
- 17 証明書の全 shadow 語を一語ずつ人手で追跡してはいない。全ファイルの件数・添字被覆・hash を集計し、K8/K36/N₅ を重点抜き取りした。
- `search/suite-wp1.g` は Prop. 3.5 該当部だけを確認し、WP1 全コードを再監査していない。
- PDF は 2401 pp.4,5,10,12 と 2405 pp.13,18,23 のページ画像を照合した。論文全ページの校訂ではない。
- Thm. 5.3 の Galois 理論側、Ihara embedding、cyclotomic character の証明は再証明していない。
- Lean 証明書は作成・確認していない。従って今便に verified の主張はない。
- Week 3 の Dih 外対象、第三者 packageGT、性能 cap の再実測は監査範囲外である。

## 考察と提案

戦況の読み: 定義の骨格は崩れていない。

12 規則、full hexagon、kernel certificate の三層は数学的に整合する。

とくに (4.11) の方向と affine 規約に致命傷がないことは大きい。

既存 dihedral 証明書の shadow 集合と合成表も、現物としては完全である。

今回止めた理由は数学的反例ではなく、ゲートの fail-open 性である。

較正器は「正しいファイルを通す」だけでなく「欠けたファイルを必ず落とす」必要がある。

N₅ の count 誤りは小さいが、この原則を実物で示した。

P4: `sol/luna_task_02_gate_closure.md` の fail-closed patch を一便で実施する。

P5: K36→K4 の直接 reduction と三角形 equality を採用する。

P6: \(\varrho\) は新しい探索機構を作らず、既存証明書から独立 checker 項目として抽出する。

P7: C-1/C-2 は主張を細分化し、証拠の状態を混在させない。

P8: 条件全通過後にだけ G1★ を宣言し、その同じ版を Week 3 の較正正本に固定する。

次の一手は新対象探索ではなく、上の閉鎖 patch である。

コストは小さく、研究スコープの拡張を伴わない。

この閉鎖後なら K3/n=12 atlas へ進んでよい。

W7: `checked:0` の PASS を「項目が不要」と「証拠が空」を区別せず表示してはならない。

W8: field 欠落時に項目自体を verdict から消す設計を残してはならない。

W9: N₅ の m=2 は hexagon FAIL ではなく unit/surjectivity FAIL である。

W10: 5 本の reduction PASS を Prop. 3.5 全 256 対の cross-check と読み替えてはならない。

W11: 直接 reduction を足すだけで (5.3) を「検査した」とせず、合成添字を比較せよ。

W12: \(m\bmod N_{\rm ord}\) と \(u\bmod2n\) の区別は \(\varrho\) 項目で固定せよ。

W13: Thm. 5.3 の arithmetic input を計算出力の功績として数えない。

W14: 今後も cross-checked と verified を混同しない。

条件閉鎖後の戦況は良い。今回の差し止めは撤退ではなく、G1★ のラベルを将来も信用できるものにする最後の締めである。
