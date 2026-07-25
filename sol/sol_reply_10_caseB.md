# Sol 第 10 便 — case B 分類監査・rigidity 消化・命題 R の補修

## 冒頭結論

| 論点 | 裁定 |
|---|---|
| case A/B の完全性 | **今回の三群に限れば PASS**。\(L_2(7),L_2(11)\) では \(\operatorname{Out}(G)=C_2\)、\(L_2(8)\) では \(C_3\) なので、外部作用の像はそれぞれ \(1/C_2\)、\(1\) に限られる。ただし定理 M2 の「任意の有限非可換単純群」という量化子では A/B だけとは限らず、修正が必要。 |
| PGL 側の類積と対象数 | **PASS**。exact order \(3\) 元と outer involution の積について、\(PGL(2,7)\) の許容二類では \(n=8\)、\(PGL(2,11)\) の order \(10\) 二類では \(n=10\)、order \(12\) 二類では \(n=12\)。全て生成対で、各積類ごとに同時共役一軌道、従って各窓二対象である。 |
| \(32,40,48\) | **各対象あたり PASS**。四 charming 層それぞれの大きさが \(e=2k\) なので \(4e=32,40,48\)。二対象を合算した数字ではない。 |
| 非 isolated 予測 | **類積表を入力とする紙上定理へ昇格できる**。三窓では settled の必要十分条件は \(w^u\sim_{\widehat G}w\)。power map より、ちょうど \(u\equiv\pm1\pmod{2k}\) の二層だけが settled で、\(16/32,20/40,24/48\)。 |
| 命題 R | **穴は補完できる**。作用の自由性は「位数の互いに素」ではなく、全ての対が \(\widehat G\) を生成し \(Z(\widehat G)=1\) であることから従う。推移性は \(n_m=|C_{\widehat G}(v_m)|\) との計数一致から従うので、命題 R は類積計算の帰結であって、その計算の独立な説明には使えない。 |
| rigidity 配達 | fixed-\(v\) centralizer torsor を「rigid triple の相対版」と読む辞書は **採用**。ただし Chen と 2508.21671 が本問題の全 centralizer 軌道または全例外窓を分類済み、という射程は **不採用**。 |
| 有理剛性と算術 | 現段階では **dihedral 予想や A5/PSL shadow の算術実現性を直接含意しない**。通常のガロア群実現と \(\operatorname{Ih}_N\) の像を結ぶ比較補題が欠け、さらに今回の個々の積類は power map で相互交換されるため rationality も自動でない。 |

★ case B 三窓では、**各 \(m\)-繊維は rigid torsor なのに対象は non-isolated** である。非 isolated の原因は一つの繊維内に複数軌道があることではなく、cyclotomic exponent \(u\) が、選んだ outer product class を別の rigid component へ移すことにある。

---

## 1. case B 分類の完全性

### F1. 今回の三群では A/B で尽きる

\(G\triangleleft Q\)、\(Q/G\simeq S_3\) とし、共役作用と商写像を合わせると

\[
Q\longrightarrow \operatorname{Aut}(G)\times S_3
\]

を得る。その核は

\[
C_Q(G)\cap G=Z(G)=1
\]

である。従って \(Q\) は、外部作用

\[
\omega:S_3\longrightarrow \operatorname{Out}(G)
\]

に関する fiber product

\[
Q\simeq
\{(a,\sigma):[a]=\omega(\sigma)\}
\]

として復元される。

- \(G=L_2(7),L_2(11)\) では \(\operatorname{Out}(G)=C_2\)。\(\omega\) は自明写像または符号写像であり、前者が A、後者が B。
- \(G=L_2(8)\) では \(\operatorname{Out}(G)=C_3\)。\(S_3\) の商に \(C_3\) はないので \(\omega\) は自明であり、B はない。

この意味で、今回の三群に対する分類の完全性は合格である。case B では

\[
Q\simeq \widetilde G\times_{C_2}S_3,\qquad
\widetilde G=PGL(2,q)
\]

となる。

### F2. 定理 M2 の一般量化子は広すぎる

M2 の見出しどおり「任意の有限非可換単純群」を量化すると、\(\operatorname{Out}(G)\) が \(S_3\) 型の像を許す場合の case C を排除できない。また \(\operatorname{Out}(G)\) に複数の位数 \(2\) 部分群があれば、case B 自体にも選んだ部分群による枝がある。

従って正しい記述は次のいずれかである。

1. M2 を今回の \(L_2(7),L_2(8),L_2(11)\) に限定する。
2. 一般版では \(\omega(S_3)\leq\operatorname{Out}(G)\) の全可能像を列挙し、A/B のほかに \(S_3\)-image case を残す。

また \(2\mid|\operatorname{Out}(G)|\) は case B 型が起こるための構造的必要条件であって、その \(G\) に許容 \((2,3,e)\)-marking が実在する十分条件ではない。exact outer involution、生成性、\(e\) の条件は別途必要である。

関連して M3(vi) の「case A では \(e=k\) かつ \(k\) は奇数」も、今回採用された split-inner 三窓では正しいが一般の case A からは従わない。case A でも \(e\) が偶数なら \(k=e/2\) は原理上可能である。命題 S の射程を「全 split-inner」へ一般化するときは、この偶数枝を未処理として残すべきである。

### F3. case B の候補 \(e\) は三窓

outer coset の元位数と小三角群の排除を合わせると、

| \(G\) | \(\widetilde G\) | outer coset の relevant 位数 | 排除 | 許容 |
|---|---|---|---|---|
| \(L_2(7)\) | \(PGL(2,7)\) | \(2,6,8\) | \(e=2\) は \(k=1\)、\(e=6\) は可解三角群 | \(e=8,\ k=4\) |
| \(L_2(11)\) | \(PGL(2,11)\) | \(2,4,10,12\) | \(e=2\) は \(k=1\)、\(\Delta(2,3,4)\simeq S_4\) | \(e=10,\ k=5\) と \(e=12,\ k=6\) |

各許容位数には PGL 共役類が二つある。以下の類積・生成監査により、これらは全て実在する marking を与える。

---

## 2. PGL 類積、生成性、対象数

以下では \(r\) を exact order \(3\) の inner 元、\(g\) を outer involution とし、

\[
n(z)=\#\{(r,g):r^3=g^2=1,\ |r|=3,\ rg=z\}
\]

と書く。

### F4. 類積係数の再計算は Opus と一致する

標準 character table の生値から有限和を取り直すと、

| 周囲群 | outer target classes | exact-order-\(3\) 類積係数 |
|---|---|---|
| \(PGL(2,7)\) | \(2B,6A,8A,8B\) | \(6,13,8,8\) |
| \(PGL(2,11)\) | \(2B,4A,10A,10B,12A,12B\) | \(10,12,10,10,12,12\) |

mass check も

\[
28\cdot6+56\cdot13+42\cdot8+42\cdot8
=56\cdot28
\]

および

\[
66\cdot10+110\cdot12
+2(132\cdot10)+2(110\cdot12)
=110\cdot66
\]

となり、左辺は積 \(rg\) の行き先別総数、右辺は order \(3\) 元と outer involution の全対数に一致する。

注意として、補題 N の \(S_3(\chi)=\sum_{x^3=1}\chi(x)\) は \(r=1\) も含む。許容 target は位数 \(8,10,12\) なので \(r=1\) は寄与せず、上の exact-order 係数と scalar 公式は一致する。拒否 target \(2B\) では scalar 係数は上表より \(1\) 大きくなる。この区別は許容窓の数値には影響しないが、表を再利用するときには明記すべきである。

### F5. 許容係数は全て生成係数である

- \(PGL(2,7)\), \(e=8\): order \(8\) 元を含む該当極大部分群は位数 \(16\) の二面体群で、order \(3\) 元を持たない。従って八対全てが \(PGL(2,7)\) を生成する。
- \(PGL(2,11)\), \(e=10\): order \(10\) 元を含み得る \(11{:}10\) と位数 \(20\) の二面体群はいずれも order \(3\) 元を持たない。従って十対全てが生成する。
- \(PGL(2,11)\), \(e=12\): 唯一注意を要する位数 \(24\) の二面体極大部分群では、order \(3\) 元は回転、outer involution は反射であり、その積は反射、従って位数 \(2\) である。積が位数 \(12\) にはならない。従って十二対全てが生成する。

よって三窓で

\[
n(z)=|C_{\widetilde G}(z)|=e
\]

が成立する。

### F6. 各積類は一つの rigid orbit、各窓は二対象

一つの許容積類 \(C_z\) 上の生成対総数は

\[
|C_z|\,n(z)
=\frac{|\widetilde G|}{|C_{\widetilde G}(z)|}\,
|C_{\widetilde G}(z)|
=|\widetilde G|.
\]

生成対の同時共役 stabilizer は

\[
C_{\widetilde G}(\langle r,g\rangle)
=Z(\widetilde G)=1
\]

なので、一軌道の大きさも \(|\widetilde G|\) である。従って各 \(8A/8B\)、\(10A/10B\)、\(12A/12B\) ごとにちょうど一つの同時共役軌道がある。

\(q=7,11\) は素数なので \(\operatorname{Aut}(L_2(q))=PGL(2,q)\)。二つの PGL 類をさらに融合する field automorphism はなく、各窓の対象数は二である。ここでは「\(\operatorname{Aut}(PGL)\) が inner」という別の大きな主張を使う必要はない。

### F7. \(32,40,48\) は各対象あたりの shadow 数

case B 三窓はいずれも charming \(m\)-層が四つで、各層の大きさが \(e=2k\) である。従って一対象ごとに

\[
4e=
\begin{cases}
32 &(e=8),\\
40 &(e=10),\\
48 &(e=12).
\end{cases}
\]

同じ窓の二対象はこの数値を共有する。二対象全部を一つの集合として数えるならそれぞれ \(64,80,96\) だが、\(\operatorname{GTSh}(N,N)\) の値として記録すべきなのは前者である。

---

## 3. ★ case B の settled 障害

監査時点で委嘱 07 の追加文書は `docs/` に見当たらなかったため、以下は独自の紙上導出である。

### F8. shadow 候補は固定積 \((2,3)\)-対に翻訳できる

元の marking に対し

\[
r_0=t^{-1},\qquad g_0=s,\qquad w=r_0g_0=t^{-1}s,
\]

と置けば

\[
X=w^2=(r_0g_0)^2,\qquad
Y=(g_0r_0)^2.
\]

\(u=2m+1\) とし、\(m\)-繊維の候補 \(f\in G\) に対して

\[
g=sf,\qquad r=w^u g
\]

と置く。hexagon 条件は \(g^2=r^3=1\)、\(rg=w^u\) と同値である。また \(g^2=1\) と \(sXs=Y\) を使うと

\[
(rg)^2=X^u,\qquad
(gr)^2=f^{-1}Y^u f.
\]

従って settled 判定で比較する ordered marking は、元の
\(((r_0g_0)^2,(g_0r_0)^2)\) と候補の
\(((rg)^2,(gr)^2)\) そのものである。

### F9. settled なら \(w^u\) は \(w\) と PGL 共役

settled と仮定すると、ある

\[
\beta\in\operatorname{Aut}(G)=\widetilde G
\]

が

\[
\beta(X)=X^u,\qquad
\beta(Y)=f^{-1}Y^u f
\]

を満たす。

\(X,Y\) は \(G\) を生成するので、「\(X,Y\) を交換する自己同型」と「\(X\mapsto Y\mapsto (XY)^{-1}\) と巡回する自己同型」はそれぞれ生成元上の値で一意に決まる。元の対ではこれらが \(\operatorname{Ad}(g_0)\)、\(\operatorname{Ad}(r_0^{-1})\)、候補対では \(\operatorname{Ad}(g)\)、\(\operatorname{Ad}(r^{-1})\) である。

従って \(\beta\) を表す \(b\in\widetilde G\) は

\[
bg_0b^{-1}=g,\qquad br_0b^{-1}=r
\]

を満たす。ここで二つの元が同じ \(G\)-自己同型を誘導したときの差は
\(C_{\widetilde G}(G)=1\) に入ることを使った。ゆえに

\[
bwb^{-1}=b(r_0g_0)b^{-1}=rg=w^u.
\]

すなわち

\[
\text{settled}\quad\Longrightarrow\quad
w^u\sim_{\widetilde G}w.
\]

### F10. 同じ積類に残れば必ず settled

逆に \(w^u\sim_{\widetilde G}w\) とする。F6 により、その積類に属する全生成 factorization は一つの \(\widetilde G\)-同時共役軌道である。従って候補 \((r,g)\) は元の \((r_0,g_0)\) と同時共役であり、その共役元が ordered marking \((X,Y)\) を候補 marking へ送る。よって候補は settled である。

以上から三窓について

\[
\boxed{\quad
(m,f)\text{ is settled}
\iff w^{\,2m+1}\sim_{\widetilde G}w
\quad}
\]

を得る。これは \(f\) に依存しない層ごとの判定である。

★ この同値が k=4 と k=6 の未解明部分も同時に閉じる。normalizer exponent map が見ていたのは \(X=w^2\) だけであり、平方を取る前の outer lift \(w\) がどちらの PGL 共役類にいるかという情報を失っていた。

### F11. power map から非 isolated 数が確定する

| 窓 | primitive power による二類の分割 | settled \(u\) | settled \(m\) | settled / 全 shadow |
|---|---|---|---|---:|
| \(L_2(7)\), \(e=8,k=4\) | 同じ類: \(u\equiv\pm1\); 相手類: \(u\equiv\pm3\pmod8\) | \(1,7\) | \(0,3\) | \(16/32\) |
| \(L_2(11)\), \(e=10,k=5\) | 同じ類: \(u\equiv\pm1\); 相手類: \(u\equiv\pm3\pmod{10}\) | \(1,9\) | \(0,4\) | \(20/40\) |
| \(L_2(11)\), \(e=12,k=6\) | 同じ類: \(u\equiv\pm1\); 相手類: \(u\equiv\pm5\pmod{12}\) | \(1,11\) | \(0,5\) | \(24/48\) |

表は 8A、10A、12A を基点に書いたが、B 類を基点にしても \(\pm1\) はその B 類に残り、残り二冪が A 類へ移るので同じ結論になる。

従って三対象型はいずれも non-isolated である。なお一般の case B まで「settled iff \(u=\pm1\)」と一般化してはならない。一般形は「\(w^u\) が元の積類に残ること」であり、\(\pm1\) だけになるのは今回の三つの power map の事実である。

---

## 4. 命題 R の補完

### F12. twisted action は固定積 factorization の同時共役である

\(v=w^u\)、\(\theta=\operatorname{Ad}(s)\) とする。\(h\in C_{\widetilde G}(v)\) に対して

\[
f^{(h)}=\theta(h)fh^{-1}
\]

と置く。外部次数で見ると \(\theta(h)\) と \(h\) は同じ parity を持つので、
\(\theta(h)fh^{-1}\in G\) であり作用は fiber を保つ。

さらに \(g=sf,\ r=vg\) とすると

\[
s f^{(h)}=hgh^{-1},\qquad
v(s f^{(h)})=hrh^{-1}.
\]

従ってこの twisted action は、固定積 \(rg=v\) を保つ factorization \((r,g)\) の同時共役作用に正確に一致する。

### F13. 自由性は生成性から従う

\(h\) が \(f\)、従って \((r,g)\) を固定すれば、

\[
h\in C_{\widetilde G}(r)\cap C_{\widetilde G}(g)
=C_{\widetilde G}(\langle r,g\rangle)
=Z(\widetilde G)=1.
\]

F5 により全 factorization が \(\widetilde G\) を生成するので、作用は自由である。

Opus §3.4(ii) の「中心化群と関係する部分群の位数が互いに素」という説明は削除すべきである。実際 outer involution の中心化群位数は \(PGL(2,7)\) で \(12\)、\(PGL(2,11)\) で \(20\) であり、\(e=8,10,12\) との gcd は一般に \(1\) でない。自由性に coprimality は不要である。

### F14. 推移性は類積係数から従う

自由作用の各軌道の大きさは \(|C_{\widetilde G}(v)|=e\)。一方 F4 の類積計算で fiber 全体の大きさも

\[
n_m=e
\]

と判明しているので、軌道は一つである。従って

\[
\mathcal F_m
\quad\text{is a simply transitive }
C_{\widetilde G}(v_m)\text{-set}.
\]

これで命題 R の論理的な穴は埋まる。ただし証明順序は

\[
\text{類積係数}
\Longrightarrow n_m=e
\Longrightarrow \text{自由作用が推移的}
\]

である。命題 R を逆向きに使って \(n_m=e\) を「説明」すると循環する。独立の character-free 証明が必要なら、別途 rigid triple の一軌道定理をこの具体的 class triple に適用しなければならない。

---

## 5. rigidity 配達の消化

### F15. fixed-\(v\) torsor は rigid triple の相対版

三共役類 \(C_3,C_2,C_e^{-1}\) に対し

\[
\mathcal T=
\{(r,g,z^{-1})\in C_3\times C_2\times C_e^{-1}:
rgz^{-1}=1,\ \langle r,g\rangle=\widetilde G\}
\]

を考える。これが同時共役で一軌道なら geometric rigidity である。第三成分 \(z^{-1}\) を一つに固定すると、許される共役元は
\(C_{\widetilde G}(z)\) に縮み、その fiber が centralizer torsor になる。

従って便 08 の \(A_5\) の \(C_5\)-torsor と今回の命題 R は、同じ orbit-stabilizer 機構である。今回の case B では ambient group が \(G=PSL\) ではなく \(\widetilde G=PGL\) であり、

\[
(\text{inner }3,\ \text{outer }2,\ \text{outer }e)
\]

の各積類ごとに rigid triple が一つある、と読むのが正確である。

### F16. 「rigid fiber」と「isolated」は別の軸

rigidity は一つの積類を固定したときの factorization 軌道を述べる。isolated は全 charming exponent が元の ordered marking の \(\operatorname{Aut}(G)\)-軌道へ戻るかを述べる。

case B は

\[
\text{全 fiber が rigid}
\quad+\quad
\text{power map が二つの rigid product classes を交換}
\]

という組合せで non-isolated になる。従って「非 isolated または非一様 fiber を探すなら non-rigid triple だけを探せばよい」という狩場設計は狭すぎる。少なくとも次の二軸を分けるべきである。

1. 一つの積類内の generating orbit 数。
2. charming power map が積類間をどう移動するか。

### F17. 配達 04 の文献射程には訂正が要る

- Chen, *Nonabelian level structures, Nielsen equivalence, and Markoff triples* は、Nielsen equivalence、Markoff triples、および一標点分岐楕円被覆の Hurwitz 空間を扱い、特定の Markoff 設定で推移性を導く枠組みを与える。しかし任意の有限群の固定 \((2,3)\)-factorization fiber が centralizer torsor になるという一般定理を、そのまま供給するものではない。
- arXiv:2508.21671 は \(SL_2(\mathbf F_p)\) の Markoff level set 上の Vieta/Nielsen 軌道と、主に非生成対から来る例外軌道を分類する。影工房の任意の PSL/PGL 窓、任意の \((2,3,e)\) class triple、または \(C(v)\)-torsor が失敗する全場合の分類ではない。
- MapClass 型の計算は共役類 tuple の braid/Hurwitz 軌道を独立に調べる候補にはなる。ただし braid action と、第三積を固定した centralizer action は同じ作用ではない。入力した三共役類、積 \(1\)、生成フィルタ、同時共役軌道から fixed-\(v\) fiber へ移す対応を証明書に含める必要がある。

従って配達 04 の「rigidity という既存語彙との一致」は採用するが、「例外軌道の完全分類が現在の狩場を覆う」という読みは撤回すべきである。

---

## 6. 有理剛性と算術実現性への裁定

### F18. 標準的 rational rigidity theorem の入力はまだ満たしていない

標準的な rigidity method は、中心のない群について、生成する rigid tuple と適切な有理共役類条件から regular Galois realization over \(\mathbf Q(t)\) を得る。しかし今回の PGL 積類は、primitive power により

\[
8A\leftrightarrow8B,\qquad
10A\leftrightarrow10B,\qquad
12A\leftrightarrow12B
\]

と交換される。従って個々の rigid class triple は \(\mathbf Q\)-rational であるとは限らない。二類の union は power-stable でも、union 上では geometric orbit が二つになるので、古典的な「一つの rational rigid class triple」をそのまま適用することはできない。weak rigidity、\(\operatorname{Aut}(G)\)-rigidity、field of moduli のどれを使うかを別途監査する必要がある。

\(A_5\) や split PSL の分裂 semisimple 類にも同種の class splitting があるため、「torsor が見えたから rational rigidity も成立」とは言えない。

### F19. ガロア群の実現と shadow の算術像は別問題

仮に rigidity method で \(G\) または \(\widetilde G\) を regular Galois group として実現しても、それだけでは

\[
\operatorname{Ih}_N:G_{\mathbf Q}\longrightarrow
\operatorname{GTSh}(N,N)
\]

の像、まして全 settled shadow の実現を決めない。必要なのは少なくとも、

\[
\begin{array}{c}
\text{branch-cycle / Nielsen class への Galois 作用}\\
\downarrow\\
\text{本工房の marking }(X,Y)\text{ と shadow }(m,f)
\end{array}
\]

を結び、その cyclotomic power が \(u=2m+1\) と一致することを示す比較補題である。現時点ではこの矢印がない。

また dihedral 予想の正面は Dih の isolated objects であり、今回の \(A_5/PSL\) 窓、とくに non-isolated case B はその直接の部分問題ではない。従って司令塔の推測への裁定は、

> rational rigidity は算術作用を設計する有望な辞書ではあるが、現時点で dihedral 予想または A5/PSL shadow の算術実現性を証明する経路ではない

である。

ただし case B の

\[
\text{settled}\iff w^u\sim w
\]

は、将来 branch-cycle の cyclotomic power action と比較するには非常に明瞭な target である。ガロア作用が同じ class-preservation 条件を返す可能性はあるが、これは現在は推測としてのみ登録すべきである。

---

## ★ 教材

1. extension の分類は \(|\operatorname{Out}(G)|\) だけでなく、実際の準同型 \(S_3\to\operatorname{Out}(G)\) の像で行う。
2. \(n(v)=|C(v)|\) と全対生成がそろうと、global triple は一軌道、fixed-\(v\) fiber は centralizer torsor になる。
3. twisted conjugation の自由性は coprimality ではなく、factor pair の生成性と周囲群の中心消滅から出る。
4. \(X=w^2\) の normalizer は outer square root \(w\) の PGL class を忘れる。settled 判定には ordered marking を復元する lift invariant が要る。
5. rigid fiber であっても、power map が別の rigid component へ移れば対象は non-isolated になり得る。
6. rational rigidity によるガロア群実現と、Grothendieck–Teichmüller shadow の算術像の全射性は、比較写像なしには結び付かない。

---

## 監査範囲外の申告

- Sol の役割規律に従い、GAP、node、Python、Lean は実行していない。明示行列と Opus の直接列挙も再実行していない。
- PGL 類積は標準 character table の生値から紙上で有限和と mass check を行い、最大部分群欄で生成性を監査した。独立な行列列挙による第二データ源はまだない。
- Chen 2011.12940、arXiv:2508.21671、MapClass 論文については、配達覚書に加えて PDF の abstract と introduction の関係箇所だけを読んだ。各論文の全定理・全例外表を精読したという主張はしない。
- standard rational rigidity theorem の原典・仮定一覧をページ単位では再監査していない。本返信では「適切な rationality と rigidity が regular realization を与える」という標準的射程だけを用いた。
- 監査時点で委嘱 07 の case B settled 機構に関する追加文書は `docs/` に見当たらなかった。
- composition table、reduction、\(\operatorname{Ih}_N\) の実像、塔での fake 判定は範囲外であり UNKNOWN。
- 今便の数値は Opus の scalar/列挙と Sol の紙計算が一致した candidate である。独立実装との一致前に cross-checked、Lean 証明書なしに verified とは呼ばない。
- 過去の reply ファイルは記録として変更せず、今便は `sol/sol_reply_10_caseB.md` だけを書いた。

---

## 考察と提案

P118【M2 の正しい封印】今回の三群について、外部作用 \(\omega:S_3\to\operatorname{Out}(G)\) から A/B が尽きる証明を封印する。一般定理の見出しは \(\omega(S_3)\) の全可能像を含む版へ直し、A/B 二分を全有限単純群へ量化しない。

W83【divisibility trap】\(2\mid|\operatorname{Out}(G)|\) は case B marking の存在十分条件ではない。outer involution、\((2,3,e)\)-生成、exact order を別欄で証明する。

P119【case B settled 定理】三窓の settled 判定を
\[
(m,f)\text{ settled}\iff w^{2m+1}\sim_{\widetilde G}w
\]
として CLAIMS に追加し、power map から \(16/32,20/40,24/48\) を導く。状態札は character table 入力に依存する紙上 candidate とする。

W84【square-root class】\(X=w^2\) の exponent image が全射でも settled とは限らない。`x_power_reachable` と `outer_product_class_preserved` を別の判定欄にする。

P120【命題 R の差し替え】Opus §3.4(ii) の coprimality 説明を削除し、F12–F14 の「twisted action = simultaneous conjugation」「全対生成による自由性」「\(n=|C|\) による推移性」で置き換える。

W85【非循環化】命題 R は類積係数から \(n=|C|\) を得た後の帰結である。命題 R を \(n=|C|\) の独立証明として引用しない。

P121【rigidity schema】今後の manifest に、各 class triple について `raw_structure_constant`、`generation_pass_count`、`global_conjugacy_orbits`、`fixed_product_centralizer_orbits` を分けて保存する。

W86【二つの軸】`fiber_rigid` と `isolated` を同義にしない。前者は固定積類内、後者は charming power map をまたぐ条件である。

P122【配達 04 の射程訂正】Chen は特定の Nielsen/Markoff/Hurwitz 枠組み、2508.21671 は \(SL_2(\mathbf F_p)\) Markoff level set の Vieta/Nielsen 例外軌道、と正本に記す。「本工房の全 torsor 失敗窓の完全分類」という文言は外す。

W87【文献 transfer】Markoff の生成対軌道から任意の \((2,3,e)\) factorization 軌道へ、仮定なしに transfer しない。

P123【MapClass を使う場合の証明書】braid orbit 計算を独立照合に使うなら、三共役類、積 \(1\)、生成フィルタ、同時共役軌道、固定第三成分への制限を出力し、centralizer torsor への翻訳を明示する。

W88【action mismatch】braid/Hurwitz action と fixed-product centralizer action は別作用である。軌道数の一致だけで同一視しない。

P124【算術ルートの事前ゲート】inverse Galois 側へ予算を投じる前に、branch-cycle Galois action と \(\operatorname{Ih}_N\) の shadow action を結ぶ比較命題を一枚で起案し、cyclotomic exponent \(u\) と class power map の一致を証明目標にする。

W89【rationality】二つの PGL 類の union が power-stable でも、個々の class triple が rational rigid とは限らない。class rationality、Aut-rationality、weak rigidity を区別する。

P125【case B 実装証明書】各対象に `ambient_product_class`、全 charming \(u\) の `powered_product_class`、`same_class_as_base`、fiber size、settled witness の有無を保存する。k=4 と k=6 では \(X\)-normalizer exponent だけを証明書にしない。

W90【状態語】三窓の分類・非 isolated・命題 R 補修は紙上監査 PASS だが candidate。独立行列列挙との一致で cross-checked、Lean 証明書で初めて verified とする。
