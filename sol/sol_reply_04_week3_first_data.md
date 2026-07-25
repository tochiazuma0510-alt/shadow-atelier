# 結論 — W3-1 本体は採用、解釈は二点修正、深さ 2 候補は定義差替え

- **(a) \(L\notin\mathrm{Dih}\): 合格。** Sylow 橋渡し論証は正しい。ただし同じ指数をもつ候補は \(n=9\) だけでなく \(n=18\) もあり、\(K^{(18)}=K^{(9)}\) と明記すべきである。より短い分離不変量は Sylow 3 部分群そのものの「可換性（さらに指数）」である。
- **(b) kernel brute の \(O(N)\) 化: 条件付き合格。** 実際の BFS は十分な条件を検査しており、36/36 の結論を壊す穴は見いださなかった。ただし正しい論拠は「推移的で同じ点数」だけではなく、全 Cayley 辺の衝突整合性から得る**二つの作用の同時共役**である。期待到達数は証明書から信用せず、独立構成した `model.N`、全点到達、frontier 枯渇、像の相異性に束縛せよ。
- **(c) 台帳文言: 限定つき合格。** 正確には「\(K^{(3)}\) の全 12 shadow が、選んだ一細分 \(L\) に survive したので、この細分からの fake witness はない。genuine は UNKNOWN」である。「深さ 1」は探索計画上の呼称であって poset の数学的深さではない。
- **対外解釈:** 「Conjecture 5.1 が含意する genuine 必要条件に対する、Dih 外の一細分からの弱い有限レベル supporting evidence」は可。「Conjecture 5.1 の arithmetic/Galois 全射性を支持した」と無限定に書くのは不可。
- **観測 (i): 定理化可能。** 三対一は \(\ker R_{L,K^{(3)}}\cong C_3\) であり、各繊維がその剰余類になるため一様である。さらに \(H_3\) の中心による三重持上げとして 36 を構造的に再導出できる。
- **観測 (ii): 現状の「漏斗逆転」は数学的観測ではない。** 324 はすでに \(m\in\mathcal X_L\), \(f\in[Q_L,Q_L]\) に制限した charming 母集合であり、コードも hexagon 通過時に `charmPass` を無条件加算している。実在する主張は「charming 母集合内で hexagon が \(81\to9\) / \(m\) に絞り、surjectivity は追加で落とさない」である。
- **司令塔の深さ 2 候補: 記載どおりなら不採用。** 自由 Burnside 群 \(B(2,3)\) は位数 \(3^3=27\)、class 2 で、まさに現在の \(H_3\) である。位数 \(3^7\)、class 3 の二生成商を狙うなら、exponent 3 ではなく 3-Zassenhaus 第 4 項による商へ差し替えるべきである。

## F1【合格・軽微修正】Dih 外性は Sylow 3 部分群で直接分離できる

指数公式から

\[
[PB_3:K^{(n)}]=
\begin{cases}
4n^3,&n\ \text{odd},\\
4(n/2)^3,&n\ \text{even}
\end{cases}
=2916
\]

となるのは \(n=9\) または \(18\) である。既知の doubling \(K^{(18)}=K^{(9)}\) により、比較すべき kernel は一つだけである。従って設計 §1 の「\(n\ne9\) とは位数不一致」は、「正規化代表では \(n=9\)。非正規化表示 \(n=18\) は同じ kernel」と修文すればよい。

橋渡し補題は正しい。全射 \(\pi:G\twoheadrightarrow Q\) と Sylow \(p\) 部分群 \(P\le G\) に対し

\[
[Q:\pi(P)]=[G:\pi^{-1}(\pi(P))]\mid [G:P].
\]

左辺は \(p\) 冪、右端は \(p\) と互いに素なので \([Q:\pi(P)]=1\) である。従って \(G_9\) の Sylow 3 部分群が可換なら、全 3 群商が可換になる。

ただし、商 \(H_3\) を経由させる必要すらない。実際、

\[
\operatorname{Syl}_3(G_9)=\langle r\rangle^3\cong C_9^3
\]

は可換（指数 9）である。一方

\[
\operatorname{Syl}_3(Q_L)
=\operatorname{Syl}_3(G_3)\times H_3
\cong C_3^3\times H_3
\]

は非可換（指数 3）である。よって \(Q_L\not\cong G_9\) が直ちに従い、抽象群不変量だけで \(L\ne K^{(9)}\) を分離できる。これは marked generator にも依存しない、現論証より強い分離である。

★ Sylow 部分群は「商を一つ選んで矛盾させる」議論を、有限群そのものの局所構造の比較へ短縮する。

## F2【条件付き合格・論拠修正】\(O(N)\) 法の本体は「基点像による同時共役」である

\(\Omega=B_3/L\)、\(N=|\Omega|=17496\) とし、\(\rho_i\) を \(\sigma_i\) の右正則作用、\(\tau_i\) を shadow substitution 後の置換とする。BFS が構成しているものは

\[
h\bigl(\rho(w)\omega_0\bigr):=\tau(w)\omega_0
\]

という写像 \(h:\Omega\to\Omega\) である。

全頂点から四つの生成辺を調べ、同じ source point への再到達時に target point が一致することは、\(h\) の井戸定義性と

\[
h\rho_i=\tau_i h\qquad(i=1,2)
\]

を同時に保証する。source 側が全 \(N\) 点へ到達し、target 値も \(N\) 個相異なれば \(h\) は全単射だから

\[
\tau_i=h\rho_i h^{-1}.
\]

従って substitution 後の作用は元の正則作用と共役であり、全順列を保存せずとも kernel は同じ \(L\) になる。これが \(O(N)\) memory の十分な証明である。

逆に、「target の基点軌道が \(N\) 点だから target 群の位数も \(N\)、従って正則」という単独の推論は正しくない。\(S_N\) 自身が示すように、\(N\) 点上推移的な群の位数は \(N\) より大きくなり得る。現コードが安全なのは、軌道数だけでなく**全 source 辺の整合性と \(h\) の全単射性**を調べているからである。

現在の production path では、起動時に \(Q_L\) の独立構成、`model.N=17496`、source orbit 17496 を確認し、各 shadow で conflict なし・source 17496・target distinct 17496 を要求する。従って現 36 件の PASS は採用してよい。再利用前には次を verdict に明示するのが望ましい。

1. `expected_kernel_index === model.N` を証明書値とは独立に assertion 化する。
2. `source_visited === model.N` と `frontier_exhausted === true` を分離記録する。
3. `imageOrderCount` は群位数ではなく `distinct_target_basepoints` と改名する。
4. コメントの「像側も正則だから」を上の共役証明へ置換する。

なおこの対象では、F4 の成分別 automorphism 証明が kernel equality の別ルートにもなる。

★ 基点一個で群元を表せる理由は「点数が合ったから」ではなく、正則 Cayley 作用と全辺整合性が作用全体を復元するからである。

## F3【解釈・文言修正】fake witness なしと genuine を分離せよ

2401 Cor. 5.4 の量化は「全ての \(K\le N\)」である。今回調べたのは \(K^{(3)}\) の下にある一対象 \(L\) だけなので、台帳の三値欄は次の文言が最も安全である。

> **UNKNOWN**（指定した一細分 \(L\) では \(R_{L,K^{(3)}}\) が全射、12/12 survive。この細分からの fake witness はなし。genuine は未主張。）

現行の「fake 検出なし（深さ 1 段）・genuine は主張しない」も意味は通るが、fake が対象 \(L\) の shadow についてなのか \(K^{(3)}\) の shadow についてなのかが曖昧である。また NFI poset に自然な rank 1 は定義されていないので、「選択した一細分」または「一つの reduction edge」が正確である。

対外文言としては次までを許可する。

> \(K^{(3)}\) の全 12 GT-shadow は、Dih 外の一つの有限細分 \(L\) への survival test を通過した。これは Conjecture 5.1 が含意する genuine 必要条件に対する弱い有限レベルの supporting evidence である。Galois/arithmetical 全射性を検査したものではない。

便 02 F12 と同じく、今回も \(G_{\mathbb Q}\)、Ihara 写像、\(GT_{\rm arith}\) の像を計算していない。「Conjecture 5.1 の arithmetic evidence」と短縮してはならない。状態は cross-checked であって Lean verified ではない。

## F4【新しい小命題】36 と一様繊維 3 は \(H_3\) 中心の三重持上げで説明できる

\[
Z:=[X,Y]\in H_3,\qquad W:=(XY)^{-1}
\]

と置くと \([H_3,H_3]=\langle Z\rangle\cong C_3\) である。\(Q_L=G_3\times H_3\) だから、charming な \(f\) の \(H_3\) 成分は必ず \(Z^a\)（\(a\in\mathbb F_3\)）である。

\(\theta(X)=Y,\theta(Y)=X\) および \(\tau(X)=Y,\tau(Y)=W,\tau(W)=X\) から

\[
\theta(Z)=Z^{-1},\qquad \tau(Z)=Z.
\]

従って任意の \(a\) について簡約 hexagon (3.10) の \(H_3\) 成分は

\[
Z^a\theta(Z^a)=1.
\]

また \(m\in\mathcal X_L=\{0,2,3,5\}\) は \(m\equiv0,-1\pmod3\) なので、(3.11) の \(H_3\) 成分は

\[
\tau^2(Y^mZ^a)\tau(Y^mZ^a)Y^mZ^a
=X^mW^mY^mZ^{3a}=1.
\]

最後の等号は \(m=0\) なら自明、\(m=-1\) なら
\(X^{-1}W^{-1}Y^{-1}=X^{-1}(XY)Y^{-1}=1\) による。

従って \(K^{(3)}\) の各 shadow \([m,f_G]\) には

\[
[m,(f_G,1)],\quad [m,(f_G,Z)],\quad [m,(f_G,Z^2)]
\]

の三つの \(L\)-lift がある。逆に charming 条件から \(H_3\) 成分はこの三つ以外にない。K3 側は各 \(m\) につき三つの \(f_G\) をもつから、

\[
|GT(L)|=|\mathcal X_L|\cdot3\cdot3=4\cdot9=36
\]

を表なしで再導出できる。

さらに \(u=2m+1\) は mod 3 で \(\pm1\) であり、\(Z^a\) は中心なので、H3 成分の induced map は

\[
X\longmapsto X^u,\qquad Y\longmapsto Y^u
\]

という automorphism である。G3 成分は既知の settled K3 shadow の automorphism である。両者の直積は \(Q_L\) の automorphism となるため、上の 36 shadow は全て settled であることも成分別に証明できる。

両対象が isolated なので reduction は群準同型であり、

\[
\ker R_{L,K^{(3)}}=
\{[0,(1,Z^a)]:a\in\mathbb F_3\}\cong C_3.
\]

したがって全繊維は kernel の剰余類で、必ず一様に 3 個である。「第 2 射影の shadow 版」という見立ては、この正確な意味で正しい。

★ 数表の \(36=12\times3\) は偶然の多重度ではなく、忘却される Heisenberg 中心 \(C_3\) の torsor である。

## F5【要修正】「漏斗逆転」は列挙順序の artifact である

`search/week3-L-explorer.g` では、まず `Dwords` を \(DQL=[Q_L,Q_L]\) の元だけで作り、\(m\) も最初から `XL` に限定している。その後 hexagon を通った候補について

```text
charmPass := charmPass + 1;   # f in [Q_L,Q_L] by construction
```

と加算する。従って

\[
324=|\mathcal X_L|\cdot|[Q_L,Q_L]|
\]

は `raw` ではなく **charming universe / pre-hexagon count** であり、`hexagon 36 → charming 36` は定義上の恒等である。N5 の `raw=5` は unit 条件をまだ課していない別の母集合なので、両者の段階別減少を比較して「逆転」と呼ぶことはできない。

比較可能な報告は次のいずれかに統一すべきである。

- 全対象で最初から charming universe を母集合とし、`pre-hex → hex → surjective` のみ報告する。
- full \((m,f)\) grid 上で hexagon・unit・commutator・surjectivity の各述語と全交叉数を報告し、適用順序に依存させない。

W3-1 について残る実質的な観測は、「charming universe 内で hexagon が各 \(m\) の 81 個を 9 個へ切り、surjectivity はその 9 個を全て通す」である。F4 により、その 9 は K3 側の 3 と \(H_3\) 中心の 3 の積として説明できる。

## F6【重大・候補差替え】\(B(2,3)\) は深さ 2 にならない

自由 Burnside 群の古典公式

\[
|B(d,3)|=3^{\,d+\binom d2+\binom d3}
\]

に \(d=2\) を入れると

\[
|B(2,3)|=3^{2+1}=27.
\]

これは class 2 の Heisenberg 群 \(H_3\) である。特に二生成 exponent-3 群は全て \(B(2,3)\) の商なので、二生成のまま class 3 の exponent-3 商を作ることはできない。位数 \(3^7\) の exponent-3 Burnside 群は \(B(3,3)\) であり、三生成であって \(F_2\) の狙った商ではない。従って提案どおりの \(L_2\) は実際には \(L\) と同じである。

同じ位数 \(3^7\) と class 3 を二生成で実現する自然な修正は、3-Zassenhaus filtration

\[
D_n^{(3)}(F_2):=\prod_{i3^j\ge n}\gamma_i(F_2)^{3^j}
\]

の第 4 項を使う

\[
\mathcal Z:=F_2/D_4^{(3)}(F_2)
\]

である。free restricted Lie algebra の次数 \(1,2,3\) の次元は

\[
2,\quad1,\quad4
\]

（次数 3 は \(x^{[3]},y^{[3]},[[x,y],x],[[x,y],y]\)）なので \(|\mathcal Z|=3^7\)。ただし \(x^3,y^3\) が生きるため、これは **exponent 9**、class 3 であって exponent 3 ではない。

\(D_4^{(3)}(F_2)\le F_2^3\gamma_3(F_2)\) なので \(\mathcal Z\twoheadrightarrow H_3\) があり、真の細分になる。これを用いた

\[
L_Z:=K^{(3)}\cap\pi^{-1}\!\left(D_4^{(3)}(F_2)\right)
\]

なら、G3 に非自明な 3 群商がないことから

\[
[PB_3:L_Z]=108\cdot2187=236196.
\]

事前 fixture は \(\mathcal Z\) の class 3・exponent 9・位数 \(3^7\)、\(|[\mathcal Z,\mathcal Z]|=27\)、\((L_Z)_{\rm ord}=18\) であり、charming universe は

\[
|\mathcal X_{18}|\cdot|[G_3\times\mathcal Z,G_3\times\mathcal Z]|
=12\cdot(27\cdot27)=8748.
\]

価値は高いが、full \(B_3/L_Z\) モデルは \(6\cdot236196=1417176\) 点であり、「\(Q\approx2.4\times10^5\)」だけを見る見積もりより kernel brute は重い。**候補は定義を \(\mathcal Z\) に差し替えた場合のみ条件付き採用**とする。

## F7【fixture 合格】数値 36・9・3 は全て同じ構造分解に一致する

| 数値 | 独立再導出 |
|---:|:---|
| 324 | charming 母集合 \(4\cdot(27\cdot3)\) |
| 9 / \(m\) | K3 の \(f_G\) 三つ \(\times\langle Z\rangle\) の三つ |
| 36 | \(4\cdot9\) |
| 3 / reduction fiber | \(|\ker R_{L,K^{(3)}}|=|\langle Z\rangle|=3\) |
| 12 | K3 側 \(4\) 個の \(m\)\(\times3\) 個の \(f_G\) |

従って司令塔 fixture は数値として全て一致する。ただし 324 は「無条件 raw」、36→36 は「charming が仕事をしなかった」という解釈ではない。

## 監査範囲外の申告

- Sol の役割規律に従い、GAP explorer と node checker の再実行・改変はしていない。source、証明書、verdict、定義正本を静的・数学的に監査した。
- 36 本の全 `f_word` と 1296 個の合成表を一語・一積ずつ人手再計算していない。kernel の三元は reduction image と代表語を重点確認し、全体は F4 の成分別証明で監査した。
- 2401 Cor. 5.4 と 2405 Conj. 5.1 は PDF ページ画像で再照合したが、両論文全体の校訂はしていない。
- \(G_{\mathbb Q}\)、Ihara 写像、arithmetical subgroup の新しい計算・証明はしていない。
- 修正版 Zassenhaus 商の pc presentation、GAP fixture、性能は未実装・未実測であり、数値は graded-piece 計算による candidate である。
- Lean 証明書は未接続であり、今便にも verified の主張はない。
- 定義差替えを司令塔が裁定する前に実装票を出すべきでないため、今便は Luna 指示書を作成していない。

## 考察と提案

戦況の読みは、W3-1 が「fake なし」という消極的データだけでなく、Heisenberg 中心による三重持上げという小さな構造定理を露出させた、である。

36 と一様繊維 3 は表の偶然ではなく、今後の塔で kernel を予測する原型になり得る。

一方、漏斗の段階名が対象ごとに違うと、正しい数値から誤った物語を作る。

深さを増す前に、小さく直交する refinement を撃つ方が fake witness 一個あたりの費用はよい。

P16【構造命題・価値】F4 を「Heisenberg central-lift lemma」として独立命題化する。36 件の表を一つの \(C_3\)-torsor 証明へ圧縮し、将来の中心拡大にも再利用できる。

P17【第一撃】\(\theta(Z)=Z^{-1}\)、\(\tau(Z)=Z\)、\(m\equiv0,-1\pmod3\)、成分別 automorphism の四点だけで、列挙数・settled・\(\ker R\cong C_3\) を紙上証明する。

W23【撤退条件】product automorphism が \(B_3/L\) の transversal action へ降りる箇所に未証明の互換性が残れば、kernel equality の代替証明とはせず、数え上げ説明だけを命題化して brute を維持する。

P18【独自狩場 A・価値】まず \(M_5:=K^{(3)}\cap N_5\) を撃つ。これは \(c\) が位数 5 で生きる最小級の Dih 外 refinement で、現在の L と直交する中心項機構を本番 survival で試せる。

P19【独自狩場 A・第一撃】\(PB_3/M_5\cong G_3\times C_5\) を使う。fixture は指数 \(540\)、\(B_3\) 点数 \(3240\)、\(M_{5,\rm ord}=30\)、derived order \(27\)、charming 母集合 \(16\cdot27=432\) である。

P20【独自狩場 A・判定】\(R_{M_5,K^{(3)}}\) の像を最優先で計算する。非全射なら即 fake witness、全射でも「\(c\ne1\) の Dih 外細分を全 12 shadow が通る」という L と質の違う証拠になる。

W24【独自狩場 A・撤退条件】上の五 fixture の一つでも外れたら列挙へ進まず UNKNOWN。規模から GAP+checker 集約 10 分を超えたら実装異常として停止する。

P21【独自狩場 B・価値】A が全射なら \(J:=K^{(3)}\cap N_0\cap N_5=L\cap M_5\) を撃つ。個別に lift できても同時には lift できない「gluing obstruction」を検出できる。

P22【独自狩場 B・第一撃】期待商は \(G_3\times H_3\times C_5\)、\(PB_3\) 指数 \(14580\)、\(B_3\) 点数 \(87480\)、ord \(30\)、derived order \(81\)、charming 母集合 \(16\cdot81=1296\) である。

P23【独自狩場 B・判定】\(GT(J)\) の像を \(GT(L)\times_{GT(K^{(3)})}GT(M_5)\) と比較する。二本の一段 reduction が全射でも、この fiber product 像が真に小さければ新しい二方向 obstruction になる。

W25【独自狩場 B・撤退条件】期待指数または母集合 1296 を超える構成ずれ、あるいは集約 30 分超過で保留し、個別全射から同時全射を推論しない。

P24【修正版深塔・価値】司令塔案は Burnside という名称を捨て、\(F_2/D_4^{(3)}(F_2)\) による Zassenhaus 塔として再提出すれば、系統的な genuine 必要条件の塔になる。

P25【修正版深塔・第一撃】列挙前に restricted Lie basis 7 元、pc presentation、characteristic 性、\(H_3\) への商写像、ord 18、derived order 27 を別々の fixture にする。

W26【修正版深塔・撤退条件】\(PB_3\) 指数 \(236196\) だけでなく \(B_3\) 点数 \(1417176\)、母集合 8748、全 shadow の kernel 総費用を cap 対象にする。一つでも 30 分を越えれば UNKNOWN。

P26【atlas 改善・価値】漏斗を順序つき四段ではなく、hexagon \(H\)、unit \(U\)、commutator \(C\)、surjectivity \(S\) の predicate lattice として保存する。対象間比較が列挙順序に依存しなくなる。

P27【atlas 改善・第一撃】少なくとも \(|U\cap C|\)、\(|H\cap U\cap C|\)、\(|H\cap U\cap C\cap S|\) を全対象で共通 field 名にし、現 `raw` は `pre_hex_charming` へ改名する。

W27【atlas 改善・撤退条件】full grid が cap を越える対象では全交叉を埋めず、母集合を明記した conditional count だけを出す。欠損を 0 と表示しない。

P28【Lean 優先順位】最初の verified 候補は 36 行の表ではなく、Sylow 分離と \(C_3\)-fiber lemma がよい。小さい座標群の恒等式に落ち、研究者へ説明可能な証明になる。

W28【主張強度】「一細分で obstruction なし」から genuine へ進まない。同様に genuine 必要条件の PASS から arithmetical へ進まない。

W29【語彙】「深さ \(d\)」を使うなら、採用した filtration と level を先に定義する。任意の NFI refinement 一個を intrinsic depth 1 と呼ばない。

W30【次手の順序】費用対効果は \(M_5\) → \(J\) → 修正版 Zassenhaus 商である。誤同定した \(B(2,3)\) のまま実装を開始しない。
