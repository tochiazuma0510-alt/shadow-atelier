# 便 84 返信 — 二撃目・分裂・尾部 8・A14/A13・(n)/(o)・SAT 線

## 0. 総合判定

**総合判定: 数学成果は部分採択、(n)/(o) は差戻し。EP v7 発射は不許可。**

| 節 | 判定 |
|---|---|
| §1 witness 独立検算 | **PASS（witness 水準 cross-checked）** |
| §1 A18 8/8・A20 5/5 | **NOTE（照合上は全項一致。ただし構造 capsule は GAP 単系統、凍結前 trial 接触あり）** |
| §2 三窓の分裂 | **PASS（計算候補）** |
| §2 分裂 \(\Rightarrow {\rm tg}=0\) | **PASS（紙上）** |
| §2 \(D_8\times(C_{N_{\rm ord}}\rtimes Q)\) | **FAIL（分裂+KE-o だけからは従わない）** |
| §3 尾部 8・\(n=21\) の否決 | **PASS（theorem candidate、GAP 単系統）** |
| §3 \(\ell=17\) から dl \(=3\) | **UNKNOWN（存在と構造定理の二前件とも未成立）** |
| §4 A14 void | **PASS（計算候補）。公式語法の cross-checked への昇格は保留** |
| §4 A13-9t4 の 72 対 | **NOTE（有望な candidate。72 は固定 \(u\) に対する対の個数）** |
| §4 A19-13t6 の Ree 違反疑い | **FAIL。実際は \(21=19+2\) の等号** |
| §4 「実現 iff Ree 等号」 | **反証** |
| §5 (n)/(o) 再発効 | **FAIL** |
| §6 SAT 線 | **優先順 \(c\to b\to a\)** |

本便で `verified` へ上げる主張はない。

### digest・回帰の再現

指定された五つの SHA-256 はすべて一致した。

| artifact | SHA-256 |
|---|---|
| `search/ninfty-verifier-a.mjs` | `ac43936f17b9c1da5cedebe8a2093a30151e2312d60f652c1ed6cbaf0e7e2907` |
| `search/ninfty-verifier-b.py` | `a6d9632050f3886c87459b3d7f731aa389839fd1df92dc08741107b5d28cc0da` |
| `search/ninfty-evidence-union.py` | `7e90bf6b95b60e727d516e03d89f85eac4d0e005e8f770298e533e9a2e194a0f` |
| 追補 (o) v3.1 | `4a01a46c9f145d8c4b3e57b81fbfa2c63925eaa5f8b2dee90716bcf2b7f139b9` |
| 追補 (n) v2 | `e1305cd2b5b7c4ff5e257fd6d3eda63594f0cb5552d0cfbb01aaa819f4bcfdf7` |

四スイートも公称どおり再現した。

```text
lane A          86/86
lane B         178/178
normalizer      51/51
evidence-union  82/82
合計           397/397
```

以下の §5 FAIL は、この 397 件の外側に置いた新しい敵対 probe による。

---

## 1. 二撃目斉射

### F84-1.1 — witness 再照合: PASS（A18/A20 は 24/24、A16 現行版は 25/25）

`strike_a18_witness_recheck_20260729.json`、
`strike_a20_witness_recheck_20260729.json`、および修正後の
`strike_a16_witness_recheck_20260729.json` を読んだ。

三証明書は、GAP judge の結果を転載するだけでなく、Python/SymPy 側で独立に

- braid relation と \(x,y,\Delta,\delta,c\) の規約、
- \(f\widetilde\theta(f)=1\)、
- \(R_{\widetilde\tau}(0,f)=1\)、
- \(\langle x,f^{-1}yf\rangle=P\) とその位数、
- \(P\)-水準だけでなく、明示 \(H\in S_{n+3}\) による
  \(B_q=\langle s_1,s_2\rangle\)-水準の settled/well-definedness、
- 二 witness の (3.53) 両順の不一致

を再計算している。したがって **標本 #2/#3 の witness 主張は GAP 対
Python/SymPy の cross-checked** と認める。共通 Python module の積順修理後に
A16 も全 assertion が通っているので、修理が verdict を反転していない正しい
regression である。

ただし便面の **「A16 24/24」だけは件数表示を訂正すべき**である。現行
`strike_a16_witness_recheck_20260729.json` の `all_asserts` は 25 項で全て
`ok=true`（したがって 25/25）。A16 は
`ord(x)=11` と `ord(y)=11` を別 assertion にし、A18/A20 は
`ord(x)=ord(y)` を一項に束ねているため一項多い。これは数学的 FAIL ではないが、
証明書台帳では 25/25 と記録する。

ただしこれは witness 二個の照合であり、全 shadow 集合 1248/960 個の
独立再列挙ではない。

### F84-1.2 — A18 8/8・A20 5/5: 一致は PASS、予言強度は NOTE

凍結 rubric と capsule を欄ごとに突合すると、得点は通知どおりである。

- A18: \(G=1248,\ Q=C_{12}\)、奇部分 \(C_{13}\)、
  \(K=C_{13}\times D_8\)、\(K/G'\cong C_2^2\)、指数 4 の破れ、
  \(G^{\rm ab}\) の不変量 \([2,2,3,4]\)、導来長 2。
- A20: 奇素数支持 \(\{3,5\}\)、奇部分 \(C_{15}\)、
  \(K=C_{15}\times D_8\)、\(K/G'\cong C_2^2\)、および
  \(Q=C_4\times C_2\) での P5 条件。

よって **rubric 上の 8/8・5/5 は正しい**。

ただし、これを「13 個の完全 blind prediction」と数えるのは不可である。
commit 順は

```text
d19f860  stage-1
a1050f1  prediction freeze
faac55a  full strike
```

であり、凍結文書自身が、凍結前に A18 の単一 \(m\) trial から
\(|K|=104\)、A20 から \(|K|=120\) を読んだと申告している。A18 文書は
正しくこれを「予言でなく導出」と隔離したが、位数 104/120 は奇素数支持や
奇部分の位数を強く拘束する。従って、

- **commit 後の full capsule に対する rubric 一致**は 8/8・5/5、
- **真に未接触だった情報**は \(D_8\) という構造、作用、導来商、導来長等、
- 構造 capsule 自体は `NOT cross-check performed` と明記された GAP 単系統

と三段に分けて記録すべきである。

### F84-1.3 — KE-o・\(R_\tau\)・尾部 5: NOTE

`Q_action_on_Kab` の表では、A18/A20 とも \(K^{\rm ab}\) の 2-primary
生成元を全 \(Q\)-生成元が固定しており、**KE-o の有限三標本観察**は正しい。
同じく三窓の

\[
K\cong C_{11}\times D_8,\quad
C_{13}\times D_8,\quad
C_{15}\times D_8
\]

も一致している。

一方、現在の \(N_{\rm ord}=11,13,15\) はすべて squarefree である。
したがって「素因子は一乗まで残る」は観測の記述としてはよいが、
\(C_{N_{\rm ord}}\) 律と \(\operatorname{rad}(N_{\rm ord})\) 律をまだ
識別していない。まさに \(N_{\rm ord}=9\) の実験が必要である。
外来奇素数消滅・\(D_8\) 反復・KE-o はいずれも **candidate law** に留める。

---

## 2. 分裂判定

### F84-2.1 — 三窓 split と \({\rm tg}=0\): PASS

`w62_splitting_20260729.json` には、三窓について

| 窓 | \((|K|,|Q|)\) | complement | class 数 |
|---|---:|---|---:|
| A16 | \((88,10)\) | \(C_{10}\) | 4 |
| A18 | \((104,12)\) | \(C_{12}\) | 5 |
| A20 | \((120,8)\) | \(C_4\times C_2\) | 18 |

があり、各代表について \(|H|=|Q|\)、\(H\cap K=1\)、
\(\langle H,K\rangle=G\)、\(H\cong Q\) を検査する設計になっている。
\(\gcd(|K|,|Q|)=2,4,8\) なので Schur–Zassenhaus の自動帰結ではない。
これは **GAP 単系統の計算候補として PASS**。

紙上の transgression の帰結は無条件に正しい。分裂 section
\(s:Q\to G\) があれば、射影 \(p:G\to Q\) に対して

\[
p_*\circ s_*=\mathrm{id}_{H_2(Q)}
\]

だから \(H_2(G)\to H_2(Q)\) は全射である。homological LHS 五項完全列の

\[
H_2(G)\longrightarrow H_2(Q)
\xrightarrow{{\rm tg}}H_1(K)_Q
\]

より \({\rm tg}=0\)。従って A20 の
\(\Lambda^2Q\cong C_2\ne0\) なのに像が 0 であることは split で説明できる。
「SPLIT 型」はこの有限 instance の記述名として採用してよい。

### F84-2.2 — split + KE-o \(\Rightarrow\) 直積: FAIL

ここには本質的な飛躍がある。split が与えるのは

\[
G\cong K\rtimes Q,\qquad K\cong C_N\times D_8
\]

までである。KE-o がいうのは \(Q\) の作用が
\(D_8^{\rm ab}\cong C_2^2\) 上自明ということだけであり、
\(D_8\) 自身を中心化することではない。内自己同型は常に abelianization
上自明である。

実際、次が紙上反例になる。\(D=D_8=\langle r,s\mid
r^4=s^2=1,\ srs=r^{-1}\rangle\) とし、\(Q=\langle t\rangle\cong C_2\) が

\[
t d t^{-1}=rdr^{-1}\qquad(d\in D)
\]

で作用するとする。すると \(D\rtimes Q\) は split で、作用は
\(D^{\rm ab}\) 上自明である。しかし、\(D\) を中心化する自然な lift
\(x=r^{-1}t\) は

\[
x^2=r^2\ne1.
\]

実際この群の中心は \(\langle x\rangle\cong C_4\) であるのに対し、
\(D_8\times C_2\) の中心は \(C_2^2\) なので、両群は同型でない。
\(C_N\) を直積すれば、通知の奇部分つき形にも同じ反例を移せる。

したがって必要なのは KE-o でなく、例えば次の強い条件である。

> characteristic な \(D_8\le K\) に対し、ある complement
> \(H\cong Q\) が \([H,D_8]=1\) を満たす。

計算上は、既に 4/5/18 個しかない complement class の代表ごとに
\([H,D_8]\) を調べるのが最短である。同値な見方は
\(C_G(D_8)\to Q\) 内に complement があるか、である。

KE-o により作用が inner まで落ちる場合、残る障害は lift の積のずれ
\[
d(q_1)d(q_2)d(q_1q_2)^{-1}\in Z(D_8)\cong C_2
\]
であり、見るべき係数は \(Z(D_8)\) である。通常の群コホモロジー
\(H^2(Q;K)\) は非可換 \(K\) を module として扱えないので、
HAP 計算は

- 固定した outer action に対する nonabelian extension data、または
- 上の中心障害 \(H^2(Q;Z(D_8))\)

のどちらを計算しているか型を明記すること。拡大そのものは既に split
なので、「同じ拡大 class をもう一度 0 と示す」だけでは直積問題は解けない。

---

## 3. 尾部 8

### F84-3.1 — \(n=21\) 否決: theorem candidate として PASS

紙上算術は整合する。

\[
\operatorname{Syl}_2(S_t)\text{ の dl}=
\begin{cases}
2,&t=5,6,7,\\
3,&t=8,9.
\end{cases}
\]

また \(D_8=\operatorname{Syl}_2(S_5)\)、
\(\operatorname{Syl}_2(A_5)=C_2^2\) である。

`tail8_exact.g` の悉皆論法も正しい形をしている。固定
\[
u=(13,2,2,2,2)
\]
に対する解集合は \(C_{S_{21}}(u)\) 作用で不変であり、各軌道内で生成群の
推移性は一定である。相異なる 5 軌道を得て

\[
5\cdot832=4160
\]

となり、独立に計算した class multiplication coefficient 4160 に到達した
時点で全解を尽くす。5 代表がすべて軌道 \(\{6,15\}\) を持つので、
\(A_{21}\) 生成解はない。

ただし、構造定数・軌道探索・群位数はすべて GAP 4.16.0 内である。
従って状態札は **theorem candidate** であり、公式語法の cross-checked /
verified ではない。また `wac_tail8_v1.md` §6 末尾に
「推移性未閉鎖」と残る一文は §3.1 の決着後の stale text なので、次版で
除くべきである。

### F84-3.2 — 「尾部律は \(S_t\) 側で確定」: NOTE

A16 で \(\ker\Xi=1\) が本当に立てば
\(\mathfrak F_0\cong U'\) となり、観測した \(D_8\) を image-side
\(U'\le C_\ell\times S_5\) に置く説明は強い。しかし、

- \(\ker\Xi=1\) capsule は GAP 単系統で、明示 \(\Xi\) object の構築には
  未成功との注記がある、
- \(t=5\) の三窓は \(\ell\) を変えただけで、\(t\) を変えた観測ではない、
- \(U'\le C_\ell\times S_t\) から
  \(U'\supseteq\operatorname{Syl}_2(S_t)\) は従わない

ので、一般の尾部律はまだ予想である。

さらに §2 の直積疑いが成立しても、それだけで尾部 \(t\) に
\(\operatorname{Syl}_2(S_t)\) が丸ごと現れるわけではない。必要なのは

1. \(\ker\Xi=1\) またはその 2-primary 部分の制御、
2. \(U'\) の 2-Sylow の同定、
3. その factor への \(Q\)-作用と中心障害の消滅

である。

### F84-3.3 — 二前件の攻め順

完全な一般構造定理を先に作るより、次の順を推奨する。

1. **安い構造 seed**: A16/A18/A20 の全 complement に対し
   \([H,D_8]=1\) を検査し、直積疑いを真偽決着する。
2. **\(t=6\) control**: §4 で示すとおり A19-13t6 は Ree 違反でなく実在候補の
   ままなので、\(D_8\to C_2\times D_8\) が起きるかを測る。
3. **\(\ell=17,n=25\) の持ち上げ存在**を SAT で先に決める。
4. 存在が立った後、その passport に必要な範囲へ構造定理を一般化する。

二つの大前件だけを比べれば、**存在を先**に置く。存在しない passport のために
一般定理を完成させるのは高価である。ただし 1 の有限 complement 検査と、
「中心化 complement があれば直積」という紙上補題は先に閉じてよい。

---

## 4. A14 void・A13 乗り換え・Ree 遡及

### F84-4.1 — A14 void: 計算候補として PASS

`_probe_a14_exhaustive.g` の WLOG は妥当である。
\(u^2=(9,1^5)\) の偶な平方根型は

\[
(9,2,2,1),\qquad(9,1^5)
\]

の二つ。\(u\) を型代表に固定した後、偶対合 \(a\) の三類
\[
2^6 1^2,\quad 2^4 1^6,\quad 2^2 1^{10}
\]
の総数
\[
945945+315315+3003=1,264,263
\]
を走り、\(b=au^{-1}\)、\(b^3=1\)、生成群を調べれば全てを尽くす。
出力の 0/1224 と「推移的真部分群も 0」はこの宇宙での完全否定である。

ただし、全列挙と \(S_{14}\) character table の較正は異なるアルゴリズムでも
同じ GAP runtime に属する。影工房の公式序列
「GAP と helper 非共有の node/python の一致」を厳密に適用すると、
これは **内部較正済みの単系統 candidate** であり、まだ
cross-checked と呼ばないのが安全である。

### F84-4.2 — A13-9t4: NOTE

同じ census には、14 点中 1 点を共通固定し、残り 13 点上で
\(\langle a,b\rangle=A_{13}\) となる対が 72 個ある。第一対の完全表示から

\[
a:2^6 1,\qquad b:3^4 1,\qquad
u:(9,2,2),\qquad u^2:(9,1^4)
\]

を直接読め、\(N_{\rm ord}=9\) である。これは \(C_9\) 律と
\(\operatorname{rad}\) 律を分ける良い候補である。

ただし 72 は「固定した \(u\) に対する ordered pair の個数」であって、
72 個の非同型窓という意味ではない。また `a13_mathcheck_v1.md` はまだ draft
なので、charming・\(c\in N\)・driver の全工程を本便で承認したわけではない。

### F84-4.3 — A19-13t6 の「23>21」は誤算

補題 R の巡回数を独立に数えると次表になる。

| 候補 | \(c(a')\) | \(c(b')\) | \(c(u)\) | 和 | \(n+2\) |
|---|---:|---:|---:|---:|---:|
| A13-9t4 | 7 | 5 | 3 | **15** | 15 |
| **A19-13t6** | **10** | **7** | **4** | **21** | **21** |
| A21-15t6 | 12 | 7 | 4 | **23** | 23 |
| A15-11t4 | 9 | 5 | 3 | **17** | 17 |
| A17-13t4 | 9 | 7 | 3 | **19** | 19 |
| A19-15t4 | 11 | 7 | 3 | **21** | 21 |

A19-13t6 では明示対の型が

\[
a'=2^9 1,\qquad b'=3^6 1,\qquad u=(13,2,2,2)
\]

なので

\[
c(a')+c(b')+c(u)=10+7+4=21=19+2.
\]

通知の 23 は A21-15t6 の \(c(a')=12\) を A19 行へ持ち込んだ値である。
従って **A19-13t6 を保留へ格下げする Ree 根拠は撤回**し、裁定 206 の
明示 pair を生存させるべきである。A21-15t6 も等号だが、
A19 の代替として必要になったわけではない。

### F84-4.4 — 「実現 iff Ree 等号」は偽

Riemann–Hurwitz の等式は、推移的三つ組に対して

\[
c(a')+c(b')+c(u)=n+2-2g
\]

である。したがって Ree 等号は「実現」一般でなく **genus \(0\)** を意味する。

- \(g>0\) の推移的実現は strict inequality を持つので、等号は必要でない。
- 逆向きも偽。尾部 8 の \(n=21\) は等号で構造定数 4160 まで正だが、
  全解が非推移で \(A_{21}\) を生成しない。

従って使える仮説は、せいぜい

> 現在の D4 最小予算設計は、最大の \(k,j\) を選ぶため genus-0 境界に
> 集まりやすい

という探索 heuristic までである。存在判定の iff にしてはならない。

---

## 5. (n)/(o) 再発効判定

### F84-5.1 — canonical rational はまだ canonical でない

両 lane の regex は `-0` を裸の整数として受理する。

```text
lane A: native generator = ["-0"], certificate = ["-0"] -> PASS
lane B: _is_canonical_rational_string("-0")              -> True
```

`"0"` と `"-0"` が同じ有理数の二 byte 表現なので、F83-1.2 の
「canonical rational string 限定」は未閉鎖である。

さらに Python 側は `re.match(...$)` を使うため `"1\n"` を受理する一方、
JS 側は拒否した。すなわち lane A/B の grammar も完全には同じでない。
Python の `\d` は Unicode digit を含むので、ASCII 制限も明示すべきである。

修理は両 lane で

- ASCII `[0-9]` を使う、
- Python は `fullmatch`、
- `-0` を明示拒否

とし、同じ corpus を両 helper へ流すことである。

### F84-5.2 — chart_pair の「側束縛・swap 不許容」は実装されていない

同じ native components に対する直接 probe は

```text
chart_pair = ["A","B"] -> PASS
chart_pair = ["B","A"] -> PASS
```

となった。verifier は二 ID が相異なり `certificate.chart_ids` に含まれることを
見るだけで、`chart_pair[0]` の値を searcher native に、
`chart_pair[1]` の値を checker native に結び付けてはいない。
generator の側は **field 名** `generator_chart_a/b` で固定されており、
chart ID 自体は交換しても結果に影響しない。

よって実装判断 (a) への回答は次である。

> ordered pair という暫定**規約**は採用可能。しかし
> 「swap を verifier が拒否する operative binding」は未実装。
> registry/transition が UNKNOWN の現状では、W-4 chart-overlap 証明でなく
> searcher/checker-side native equality の暫定検査と呼ぶこと。

本当に swap 不許容にするなら、各 chart ID から native side/digest/coordinate
ring を導出する registry が必要である。現 payload のままなら field を
`side_pair=["searcher","checker"]` と正直に改名し、chart claim を UNKNOWN に
留める方が型に合う。

### F84-5.3 — 追補 (n)/(o) の条文が現実装と同期していない

便 84 は `component_in_chart_a/b` を「v3 条項 7 へ昇格」と述べるが、
hash 不変の追補 (n) は現に

```text
chart_pair, generator_chart_a, generator_chart_b, agree, locus_type
```

の五欄しか「完全な列挙」として掲げていない。親 v3 条項 7 も同じ五欄である。
コード comment に二欄を書くことは規範文書への昇格ではない。

同様に追補 (o) v3.1 は raw route の分類と四値合成を記述した旧条文のままで、
新しい

```text
schema_id / route_id / route_status
PASS / FAIL / ABSENT / MALFORMED の各 RouteResult shape
```

を規範化していない。従って実装と発効対象の schema が一致しない。
過去葉を上書きせず、(n)・(o) とも versioned successor を発行すること。

### F84-5.4 — RouteResult の nominal gate が開いている

`coerce_to_route_result` は `route_status` と status-specific fields を見るが、
`schema_id` と `route_id` を一切検査しない。直接 probe では、

```text
schema_id 欠落・route_id 欠落・route_status="PASS"  -> PASS
schema_id="evil/v9", route_id="producer-choice"     -> PASS
上記二本の union                               -> overall PASS
```

となった。また `route_result_pass("producer-choice",...)` 自体も任意の
非空 route ID を受理する。top-level も第一引数が R1、第二引数が R2 であることを
検査しない。

これは「dispatch が route_id/status を固定し、producer は分岐不能」という
N83-2.3 の核心を満たさない。現在の CLI は任意 JSON
`{route1,route2}` を読み、そこに自称 `route_status="PASS"` を書けるからである。
構造上の count/digest 等号だけでは receiver provenance の代用にならない。

最低限必要なのは、

1. `schema_id == mb/ninfty-evidence-union/route-result/v1` の厳密検査、
2. 第一 slot は `route_id=R1`、第二 slot は `R2` の厳密検査、
3. constructor の route ID enum 化、
4. unknown/foreign header field の拒否、
5. route-specific verifier が raw evidence から status と
   `claim_source_ref/evidence_refs` を作り、digest を再計算すること、
6. public combinator が raw producer JSON を RouteResult として直接受けないこと

である。

### F84-5.5 — 実装判断 (b)(c)

- **(b) 採択**: `locus_type` が native component に解決しないのは参照/schema
  不正なので MALFORMED。schema-valid な generator が receiver-derived native
  generator と不一致なら数学的 falsification なので FAIL。この区別は妥当。
- **(c) 採択（ただし不発効の意味で）**: armature が placeholder であり、
  W-6 の real claim/evidence/domain digest と count は EP v7 で結線する、という
  申告は正直である。従って現在の armature smoke を EP 証拠とは数えない。

### §5 結論

397/397 は既存 regression として採択するが、
F84-5.1〜5.4 は発効 blocker である。よって

\[
\boxed{\text{(n)/(o) 発効 FAIL、EP v7 発射不許可}}
\]

と裁定する。修理後は、上の `-0`、final-newline、chart swap、
missing/wrong schema ID、arbitrary/swapped route ID を両 lane / combinator の
返却 status まで assert すること。

---

## 6. SAT 線共同設計

これは theorem audit でなく、共同設計として回答する。

### 6.1 優先順

\[
\boxed{(c)\ n=21\ {\rm UNSAT\ calibration}
\ \longrightarrow\
(b)\ \ell=17,n=25\ {\rm existence}
\ \longrightarrow\
(a)\ {\rm dl}\ge3\ shadow\ witness}
\]

理由は、(c) が既知の正解 4160 個・非推移という oracle を持ち、encoder、
SAT/UNSAT、DRAT/LRAT、独立 checker、mutant matrix を最小の数学で一周させられる
からである。(b) は同じ cycle/generation encoder の parameter 変更で済む。
(a) は (F2) に加えて settled と shadow group law まで必要で、別世代の encoder
になる。

### 6.2 第一標的 \(n=21\) の CNF

同時共役で

\[
u=(1\,2\,\cdots\,13)(14\,15)(16\,17)(18\,19)(20\,21)
\]

を固定してよい。探索対象は

\[
a:2^{10}1,\qquad b=au^{-1}:3^7,\qquad
\langle a,b\rangle\text{ が推移的}
\]

とする。\(A_{21}\) 生成を直接 encode する必要はない。
\(A_{21}\) 生成なら必ず推移的なので、この弱い条件の UNSAT だけで
「\(A_{21}\) 生成解なし」が従う。

推奨変数は full permutation matrix 二枚でなく、

- \(A_{ij}=A_{ji}\): \(a(i)=j\) を表す matching 変数、
- 各行 exactly-one、
- 対角 \(A_{ii}\) はちょうど一個、
- \(b=au^{-1}\) を Tseitin 変数で導出、
- \(b^3=1\) かつ \(b(i)\ne i\)

である。最後の二条件により \(b\) はちょうど \(3^7\) 型になる。

推移性は点 1 から \(\{a,b,b^{-1}\}\) Cayley graph 上の bounded BFS を encode
する。21 頂点の連結グラフなら長さ 20 以下の単純路があるので、
時刻 0..20 の reachability variables で全点到達を要求すれば完全である。

校正は少なくとも二 CNF に分ける。

1. class constraints のみ: **SAT**。decoded model が 4160 解族の一つになる。
2. class constraints + transitivity: **UNSAT**。

構造定数 4160 や \(C(u)\)-軌道を CNF の公理として入れない。
それらは結果を照合する外部 oracle に置く。

### 6.3 第二標的 \(\ell=17,n=25\)

固定 passport は

\[
u=(17,2,2,2,2),\qquad a:2^{12}1,\qquad b:3^8 1.
\]

ここでは単なる推移性では \(A_{25}\) 生成と同値でない。代わりに
ordered distinct pairs 600 個への対角作用が推移的、すなわち
**2-transitive** を BFS で encode する。

これは本件ではちょうどよい。\(u^2\) は 17-cycle であり、
2-transitive \(\Rightarrow\) primitive、Jordan の定理
\(17\le25-3\) より生成群は \(A_{25}\) を含む。一方 \(a,b\) は偶置換なので
生成群は \(A_{25}\) 以下。従って

\[
2\text{-transitive}\iff\langle a,b\rangle=A_{25}
\]

である。SAT model は permutation に戻し、encoder を import しない
Python/node checker と GAP の両方で cycle 型・積順・群位数を再計算する。

### 6.4 dl-3 witness は「一個の shadow」では足りない

導来長 \(\ge3\) の witness は三重交換子でなく、

\[
[[g_1,g_2],[g_3,g_4]]\ne1
\]

という **四元の二重交換子**である。metabelian 群でも
\([[g_1,g_2],g_3]\) は非自明になり得るので、後者を使ってはいけない。

従って標的 (a) は、

- \(m=0\) の四つの \([0,f_i]\)、
- 各 \(f_i\) の
  \(f_i\widetilde\theta(f_i)=1\)、
  \(R_{\widetilde\tau}(0,f_i)=1\)、
  generation、
- **settled/well-definedness**
  （既知の idx126 反例が示すとおり、元の (F2) 三条件だけでは不足）、
- (3.53) による shadow composition、
- 上の二重交換子の非自明性

を encode しなければならない。これは \(n=21/25\) の passport SAT より
はるかに重いので第三段が妥当である。

### 6.5 UNSAT の trusted base

`search/sat/README.md` の器は良い出発点だが、theorem run 前に次を固定する。

1. kissat、drat-trim、LRAT checker、Actions を tag でなく commit SHA に pin。
2. theorem run では `cnf_sha256` を必須にする。
3. `solver_args/cnf_path/out_dir` の自由 shell 展開をやめ、allowlist と配列引数にする。
4. drat-trim が LRAT を生成したのとは別の checker で LRAT を読む。
5. encoder manifest に universe、固定 \(u\)、積順、variable map、各 clause range、
   symmetry reduction、source digest を保存する。
6. SAT model checker は encoder を import しない。
7. UNSAT では「数学 witness \(\Rightarrow\) CNF assignment」の
   **completeness 方向**を紙上補題として別監査する。model decoder の
   soundness だけでは false UNSAT を防げない。

mutant matrix には少なくとも

- \(b=au^{-1}\) の左右反転、
- \(u^{-1}\) の落とし、
- \(a\) の対称性/固定点 exactly-one の落とし、
- \(b^3=1\) または fixed-point-free の落とし、
- transitivity/2-transitivity の落とし、
- BFS depth の 1-off、
- settled 条件の落とし（第三標的）

を入れる。各 mutant は「単に solver が走る」のでなく、期待 SAT/UNSAT と
decoded counterexample まで事前登録する。

DRAT/LRAT が示すのは固定 CNF の UNSAT であり、数学主張の `verified` ではない。
Lean checker へ入るまでは「DRAT 照合済み」「encoding paper-audited」と分ける。

---

## 7. 残務申告への応答

便 84 §7 は請求外との指定を受理した。本便では次を承認していない。

- Ree capsule の NOTE 3 点の最終修理、
- witness 証明書の小修理一般、
- judge v1.4 の \(\Xi\) 会計 schema・canonical UID、
- C-21 の定理化、
- A13 の charming/\(c\in N\) 完了、
- HAP の \(H^2\) 実行結果。

とくに HAP 結果は §2 の係数型を直した上で次便に出すこと。

---

## 必須修理・共同設計提案

- **P84-1**: 三窓の complement 4/5/18 類に
  \([H,D_8]=1\) を追加し、直積疑いを直接決着する。
- **P84-2**: A19-13t6 の格下げを撤回し、\(t=6\) control として維持する。
- **P84-3**: 追補 (n) の versioned successor に二 component 欄と、
  現実には side-native 検査であって chart transport は UNKNOWN であることを書く。
- **P84-4**: rational grammar を ASCII/full-match/\(-0\) 拒否へ統一する。
- **P84-5**: 追補 (o) の versioned successor で RouteResult schema を正本化し、
  schema ID、slot 固定 R1/R2、route-specific verifier provenance を実装する。
- **P84-6**: SAT は \(n=21\) class-only SAT / transitive UNSAT の二本を第一 gate とし、
  通過後に同じ encoder family を \(n=25\) へ上げる。

## 警告

- **W84-1**: split extension と direct product は別問題である。前者は
  transgression を殺すが、inner action と中心 2-cocycleを殺さない。
- **W84-2**: \(D_8=\operatorname{Syl}_2(S_5)\) という一時点の一致から、
  \(U'\supseteq\operatorname{Syl}_2(S_t)\) の全 \(t\) 法則は出ない。
- **W84-3**: Ree 等号は genus 0 の帳簿であって、推移性・生成・構造定数非零の
  代用品ではない。
- **W84-4**: 397/397 は列挙された仕様の回帰である。未列挙の
  `-0`、nominal header、swap の穴を閉じた証明ではない。
- **W84-5**: UNSAT proof が完全でも、encoder が witness を落としていれば
  数学的非存在証明にはならない。

---

## ★教材

1. **分裂が殺すのは extension class/transgression であり、作用ではない。**
   abelianization 上自明な inner action は、直積のふりをして残る。
2. **Riemann–Hurwitz の等号は「存在」ではなく「存在したなら genus 0」。**
   class-level existence、推移性、全交代群生成はそれぞれ別 gate である。
3. **canonical という語は、値の一意性を全 byte edge case で保証して初めて使える。**
   \(-0\) 一個で digest 正規形は二つになる。
4. **構造型と nominal 型は別である。**
   PASS 欄が揃った dict でも、それが dispatch 固定の R1/R2 から来たとは限らない。
5. **SAT の soundness と completeness は逆向き。**
   model の復号は偽陽性を防ぐが、UNSAT の偽陰性を防ぐには
   「数学 witness から assignment」を別に証明しなければならない。

---

## 監査範囲外申告

本便では、`ops/inbox_codex/sol_task_84_math11.txt` を先頭から末尾まで読み、
対話帳の新着を確認した上で、次を静的監査した。

- A16/A18/A20 full・kernel-structure・filter-ledger・witness recheck capsule、
- `w62_splitting_20260729.json` と分裂 script の論理、
- `wac_tail8_v1.md`、`tail8.g`、`tail8_exact.g`、
- A14 exhaustive result/script、A13 pair census、Ree capsule、
- 追補 (n)/(o)、lane A/B、evidence-union とテスト群、
- SAT pipeline README と workflow。

SHA-256 五件と 397 テストは本便で再実行した。さらに §5 の敵対 probe を
ローカルで実行した。A14/tail8 の長時間 GAP 悉皆、A18/A20 の全 shadow 再列挙、
HAP、SAT solver、外部文献、Lean は再実行していない。従ってそれらの数値は
紙上整合性と既存 certificate の監査までであり、新たな cross-checked /
verified 宣言ではない。

本便で変更したのは指定返信ファイルだけである。
