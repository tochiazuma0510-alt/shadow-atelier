# 総合判定

## Part A — **PASS・(β) 版イベント発火を許可する**

指定された clean payload commit
`38e4652543db051c580a4e37489c977ae2cc577c`（以下 \(C\)）と、
receipt-only commit
`686ceeafe1c100a2a5743f57ddd63d38e5a20b0a`（以下 \(R\)）の二段
provenance は閉じた。BFC v2.11、条文案 v8、TB4 v2.4、
certificate 25/25、CLAIMS、lint v4、triage、receipt の指定状態を
**本版イベントの入力として受理する**。

これは Part A に列挙された既定 payload だけへの許可である。Part B で
本便が要求する \(N_\infty\) whitelist・探索 schema の修理を、この許可済み
版イベントへ無監査で混入してはならない。

## Part B — **INTEGRITY STOP・8 件は全件 REJECT・Freeze 2 受領不可**

結論は三段ある。

1. 報告された 8 hit は候補ではない。全件が \(x=0\) 上に指数 3 の真の
   分岐を持つため、要求される有限ファイバー型 \(2^2 1\) に反する
   **同一機構の偽陽性**である。
2. 観測された `h = ĉ_μ` という**符号込み等号**は一般恒等式ではない。
   しかし genuine な \(N_\infty\) 候補では
   \[
   h\in\{\hat c_\mu,-\hat c_\mu\}
   \]
   が構造的に従う。しかも \(K=\mathbb Q(\zeta_{20})\) では
   \(-1=i^2\) なので、`h` は \(\hat c_\mu\) と同じ \(K\)-平方類を
   漏らし、(P1) を決める。従って **`h` の pre-Freeze-2 whitelist
   掲載は廃止**しなければならない。
3. `mb/ninfty-branch-search/v1` は内部で \(\hat c_\mu\) を厳密に計算して
   stage 2 に使用し、さらに人間可視 artifact に Pell 表現
   \((a,p,f_6)\) と `h` を出していた。従って問題は最後の手計算だけでなく
   **schema/run 全体**にある。同 schema の既走 \(N_\infty\) artifact は
   全て quarantine/discovery-only とし、新 version・新 campaign ID・
   sealed 受領経路で bound \(5\) を再走するまで、\(N_\infty\) の探索結果は
   **UNKNOWN**である。

Part A の版イベントと、Part B の Model-Builder/Freeze 2 判定は独立である。
前者の PASS は後者を解禁しない。

---

## F1. Part A — commit \(C\)/\(R\) と digest の最終検収

### F1.1 二段 anchor

現物で次を確認した。

- \(C\) の tree は
  `edf1200e702b5fb402355b192d1e99ca95113a81`。
- receipt の `source_commit` は \(C\) の full ID と完全一致する。
- receipt の `source_tree` は上の tree ID と完全一致する。
- \(C\to R\) の差分は `search/preflight-receipt.json` 一点だけである。
- \(R\) 以後の本便 HEAD まで、Part A の guarded artifact には差分がない。

したがって前便 F6/F9.2 で要求した

\[
\text{clean content commit }C
\longrightarrow \text{preflight}
\longrightarrow \text{receipt-only commit }R
\]

が初めて再現可能な形で閉じた。receipt が自分自身を含む commit を
参照する自己言及もない。

### F1.2 主要成果物

| artifact | LF / records | SHA-256 | 判定 |
|---|---:|---|---|
| `docs/week4-BFC攻略_opus_v2.md` | 1214 / 1214 | `2aa84e6762a643c10727cdca99556e660cd97ccab5088ce38262dd2679473acc` | 一致 |
| `docs/amendment_5prime_draft.md` | 358 / 358 | `ccba23a317fe6fb016d95d81143760fdd77d5edba2c2144cf6280ae23a776655` | 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 852 / 852 | `ff71e9fbc162ee613713d9ad317e8fbea635c7e4fadeae189cff1656b52634f4` | 一致 |
| `certificates/bfc/bfc-antecedents.json` | 0 / 1 | `d19b47f5c457d5cc1af5131206bf7cbb30e6a64d2afe65cb039234a83c8c85cc` | 一致 |
| `search/version-event-manifest.json` | 62 / 63 | `95db2399d1ce6c6e005f89c37fadbdab0ed9de807fefad62f2cf03e33c5ee918` | receipt と一致 |
| `search/version-event-preflight-lint.mjs` | 196 / 196 | `74801f4aaaf9b4a4a6d3ef3b783526494a44b960b684cad3622a95ec1c766599` | receipt と一致 |
| `search/preflight-triage.json` | 377 / 378 | `5f3b9fecf41e2b16d4edcbdd8cd3852dba240d85a729ec3eb891e355a4baadb2` | receipt と一致 |

receipt 自身は 77 LF / 78 records、SHA-256
`f6d8988f4e00cfa18f6f4ec233dde1725df4d9cd751cb01e40ff6420d3f64739`
である。receipt を自己 digest の対象にしていないことは正しい。

### F1.3 receipt の内容

次がすべて現物と一致する。

- artifact version:
  `v2.11 / v8 / v2.4`、parsed/input の文字列 equality。
- CLAIMS:
  W3-17 row hash `37f94a9a64024ba2`、
  W3-18 row hash `3daf3f9a2789f17d`。
- checker:
  `search/week4-bfc-antecedents.mjs` =
  digest `f7429890...`, 13/13;
  `search/tb4-monodromy-check.mjs` =
  digest `6847a76b...`, 37/37。
- certificate:
  pass 25、fail 0、`fail_closed=true`、BFC v2.11 現物 digest へ束縛。
- preflight:
  `open=0 / triaged=47 / orphans=0`、`failures=[]`、`CLEAN`。
- triage:
  47 records の reviewer/disposition 空欄はともに 0。

GAP script の現物 digest
`104e748bb44c34024bd725d608659c0265d4b5d1b3e2c669cc9908ac63d825d9`
と certificate/manifest の記録も一致する。

`--selftest` も独立に再走し、

- M1: header/manifest 版不一致、
- M2: stale な手続き token、
- M3: certificate `pass_count` 改変

が全て `BLOCKED`、`SELFTEST_PASS` となることを確認した。

---

## F2. Part A — 前便 blocker の差分検収

### F2.1 BFC v2.11 — **PASS**

current definition/statement/proof にあった「窓にも依らない」という
過大量化は除かれた。現在の型は一貫して、

- \(\varepsilon\): framework-global、
- \(t_{2M},\bar t_M,b_{\rm op}\): 固定 \(M\)・固定 Rule 1 root object
  の下で二 detector に共通、
- 再融合:
  \[
  b_{\rm op}=(\bar t_M\varepsilon)^{-1}\pmod M
  \]

である。旧文言が残る箇所は版差分・事故記録として明示された history
だけであり、live assertion ではない。前便の数学核 PASS は維持され、
artifact residual も閉じた。

### F2.2 amendment v8 — **PASS**

- live 自己参照は版番号を埋め込まない「本草案（現版）」となった。
- current BFC source は v2.11 に同期した。
- v6/v7 や旧 BFC への言及は履歴身分に限定された。
- typed union schema、R-a/R-b、exact branch の discriminator は前便
  PASS のまま変わっていない。

これで「版 bump のたびに手続き本文自身が stale になる」という構造欠陥は
閉じた。

### F2.3 TB4・CLAIMS・certificate — **PASS**

TB4 v2.4 の digest と 37/37 は不変。W3-17/W3-18 は v2.11、便 54、
\((2.1')\)、現行 \(b_{\rm op}\) 式へ同期している。BFC certificate は
新 BFC digest に再束縛され、25/25 の三値条件も閉じた。

従って Part A の既定 payload に対して、**(β) 発火を許可する**。

---

## F3. Part A — lint v4 の非 blocker hardening

今回の receipt の真偽は、commit \(C\) の blob と各 digest を直接突合して
閉じた。ただし lint を次イベントにも常設するなら、二点は v4.1 で直す
価値がある。

1. `git status --porcelain` の path を `"` だけ除いて guarded Unicode
   path と比較している。既定の `core.quotePath=true` では日本語 path が
   C-style escape されるため、日本語 artifact の dirty 状態を見逃しうる。
   `--porcelain=v1 -z` を NUL-aware に読むか、各 guarded path に
   `git diff --quiet -- <path>` を使うべきである。
2. lint は certificate 内の GAP script digest を manifest 値と比較するが、
   GAP script 現物をその場で hash していない。今回の現物は手動照合で一致した。
   次版では script path も manifest/guarded set に入れ、現物 hash を直接取る。

また三 mutant selftest を receipt の ordered steps と結果欄へ入れれば、
「selftest を実装した」と「当該 receipt 生成時に実走した」を区別できる。

これらは**今回の \(C\) の blob と receipt digest の一致を覆さない**ため、
Part A の blocker にはしない。

---

## F4. Part A と Part B の版境界

Part A の許可対象は、委嘱に列挙された Rule 1 v1.4 / manifest v1.6
イベントの既定 payload である。下記 Part B により、新たに少なくとも

- \(N_\infty\) の `h` 非開示、
- Pell 内部表現の sealed 化、
- stage 2 の exact fiber-partition 判定、
- taint/access log と候補受領 schema

が必要になった。これは Part A receipt が検査していない新差分である。
従って、Part A を先に宣言どおり発火した後、**新しい版番号・campaign ID
で別の差分ゲート**へ送ること。既存 v8 や receipt \(R\) を書き換えて
吸収してはならない。

---

## F5. Part B — 接触の起点は手計算より前にある

### F5.1 70 green の射程

Actions run `30289323147` の local artifact では、70 shard success、
skip/error/internal error 0、calibration `all_pass`、凍結文書・探索器の
digest 一致が記録されている。これは「指定された v1 program が指定範囲を
完走した」ことの証拠である。

しかし数学的 predicate と情報流 predicate の正しさは保証しない。
実際、両方に反例がある。

### F5.2 `contact_discipline` 自己申告はコードと不一致

`search/mb-ninfty-branch-search.mjs` は、stage 1 で

\[
a^2=p^2 f_6+\hat c_\mu
\]

の多項式除算を実行し、余りの定数項を `cHatMu` として厳密に取得する。
その値が 0 でないことを選別し、さらに
`computeDiscriminantPolyNinfty(..., stage1.cHatMu)` へ渡して stage 2
の判定にも使用する。

従って証明書末尾の

> `c_hat_mu` の値を一切計算・選択基準に使用していない

はコードの事実と反する。値を JSON field として直接出さなかった、という
だけである。

さらに hit 出力の \((a,p,f_6)\) は
\(\mu=a+py\) そのものという human-visible Pell representation であり、
値は一回の多項式演算で復元できる。これは Sol 便 42 F3(5) と
manifest v1.5 operative 節が要求した

> \(\mu\)/Pell ansatz は、strict I-b∞ を守る事前登録済み sealed
> automation の内部に限る

を満たさない。公開 Actions artifact と人間向け報告は sealed channel
ではない。

したがって、担当者の手計算は**最初に誠実に自己申告された human
recognition**ではあるが、情報流違反の開始点ではない。開始点は
`mb/ninfty-branch-search/v1` の設計・実走・人間可視出力である。

### F5.3 quarantine の単位

次を一単位として quarantine する。

- schema `mb/ninfty-branch-search/v1`、
- 同 schema で作られた bound 3、4、5 の全 \(N_\infty\) certificate、
- run `30289323147` の \(N_\infty\) shard とそこから派生した 8 hit 集計、
- それらを「stage 2 通過候補」と読む報告・集計。

生 artifact は削除・改変しない。immutable な discovery/事故再現物として
保存し、別 sidecar に `RETRACTED_AS_CANDIDATE`、理由、対象 digest、
taint scope を記録する。同じ artifact に後から hash や新規則を付けて
救済してはならない。

同 run の W / \(N_{\rm aff}\) shard はこの `cHatMu`/`h` バグの直接対象では
ない。既存 Freeze 1 も撤回しない。ただし三枝全体の結論は従来どおり
`BRIDGE-UNKNOWN` である。

---

## F6. Part B — 8 hit が全て偽陽性である紙上証明

\[
C:=\hat c_\mu=a^2-f_6p^2\ne0,\qquad
\mu=a+py,\qquad y^2=f_6
\]

と置く。norm 恒等式を微分すると

\[
2aa'-f_6'p^2-2f_6pp'=0.
\]

一方

\[
\frac{d\mu}{dx}=a'+p'y+\frac{pf_6'}{2y}
\]

なので、

\[
\boxed{\quad 2py\,\frac{d\mu}{dx}=2a'\mu.\quad} \tag{54.1}
\]

8 hit の exact coefficient 列を突合すると、全て

\[
a'=\epsilon\,5x^2p,\qquad \epsilon\in\{\pm1\} \tag{54.2}
\]

を満たす。また全件で \(p(0)\ne0\)、\(f_6(0)\ne0\)、\(C\ne0\) である。
従って \(x=0\) 上の二点 \(Q_\pm\) では \(x\) が uniformizer で、
\(\mu(Q_\pm)\ne0\)。式 (54.1)(54.2) から

\[
\frac{d\mu}{dx}
=\epsilon\,5x^2\frac{\mu}{y}
\]

となり、右辺の \(x^2\) 以外は \(Q_\pm\) で単元である。ゆえに

\[
\operatorname{ord}_{Q_\pm}(d\mu/dx)=2,\qquad
e_{Q_\pm}(\mu)=3. \tag{54.3}
\]

すなわち各対応ファイバーは少なくとも一つの三重点を持つ。
要求される \(2^2 1\) は「相異なる二つの二重点と一つの単純点」であり、
\(3\,1^2\) とは同じでない。これだけで 8 件は全て棄却される。

### F6.1 `quadratic_artifact_power=3` の正体

探索器が除去する二次式は

\[
q(v)=v^2-2a_0v+C.
\]

本 8 件では \(a_0=0\)。\(Q_\pm\) で
\(v_\pm=\mu(Q_\pm)=p(0)y(Q_\pm)\) だから

\[
v_\pm^2=p(0)^2f_6(0)=-C,
\qquad q(v_\pm)=0. \tag{54.4}
\]

従って `q` の根は、本件では「幾何的でない見かけの値」ではなく、
式 (54.3) の**真の分岐値**である。

開示済み代表を \(C_0=-108\) とだけ書けば、探索器自身の exact resultant
係数は非零定数倍を除いて

\[
\boxed{\quad
D(v)\doteq v^4\,(v^2+C_0)^3\,(v^2-C_0)^2.
\quad} \tag{54.5}
\]

固定次数 Sylvester 行列の次数降下が強制する `q` の基底 multiplicity は
一つである。残る `q²` は二つの \(e=3\) 点が与える genuine な判別式
multiplicity である。ところが `stripKnownQuadraticFactor` は
`while` で `q` を**割れる限り全て**除去するため、基底因子だけでなく
真の分岐を表す二乗まで消した。その後の residual quartic が平方形に
見えたことが偽陽性の直接原因である。

`quadratic_artifact_power=3` は候補の補助データではなく、本来
「予想した artifact power 1 を超えた」という integrity alarm であった。
synthetic positive calibration が power 1 を仮定していた一方、
実 \((a,p,f_6)\) から作る end-to-end positive control が無かったため、
この境界を検出できなかった。

さらに判別式の multiplicity 2 だけでは、

- 一つの三重点 \(3\,1^2\)、
- 二つの相異なる二重点 \(2^2 1\)

を区別できない。stage 2 は resultant の平方形だけでなく、fiber divisor
の partition を直接検査しなければならない。

### F6.2 bound 5 の結論

現在の 8 件を除けば「候補 0」とはしない。全 `q` power 除去は偽陽性だけで
なく、`q` の根が genuine な所望分岐値になる場合の偽陰性も起こしうる。
従って現 v1 による \(N_\infty\), bound \(\le5\) の探索結論は丸ごと
**UNKNOWN**であり、修正版による全域再走が必要である。

---

## F7. Part B 諮問 (ii) — `h` と \(\hat c_\mu\) の構造裁定

genuine な \(N_\infty\) 候補について、超楕円対合 \(\iota\) は

\[
\mu^\iota=\frac{C}{\mu},\qquad C=\hat c_\mu \tag{54.6}
\]

を満たす。所望の \(\mu\) の二つの有限分岐値を \(\{s,-s\}\)、
探索器の意味で \(h=s^2\) とする。この集合は
\(v\mapsto C/v\) で不変なので

\[
\frac{C}{s}\in\{s,-s\}.
\]

従って

\[
\boxed{\quad h=s^2=C\ \text{または}\ h=s^2=-C.\quad} \tag{54.7}
\]

よって回答は次のとおり。

- **`h ≡ ĉ_μ` は符号込みの一般恒等式ではない。**
- **`h = ±ĉ_μ` は所望の \(N_\infty\) 分岐集合から従う構造関係である。**
- 今回の符号込み一致は、候補が偽であり artifact 除去も不正なので、
  genuine candidate を裏付ける観測としては使えない。

しかし whitelist 裁定には符号の曖昧さは何の救いにもならない。
\(-1=i^2\in K^{\times2}\) だから

\[
[h]_{K^\times/K^{\times2}}=[C]_{K^\times/K^{\times2}}. \tag{54.8}
\]

Rule 1 I-b∞ は \(N_\infty\) で

\[
\text{(P1)}\iff C\in K^{\times2}
\]

を既に証明している。従って `h` 単独で (P1) が完全に決まる。
これは値の名称でなく dependency による漏洩であり、**whitelist の穴**
である。

修理は次のとおり。

1. \(N_\infty\) の human-visible pre-Freeze-2 schema から `h`、
   その符号・平方類・因数、同値な branch-value square を全て除く。
2. 内部 field が必要なら
   `branch_value_square_sealed` のように型を分け、Freeze 2 access control
   の内側に置く。
3. 既存 certificate の `h` field は消さず、artifact 全体を quarantine。
4. 他枝の `h` も同じ記号だから安全、とは仮定しない。枝ごとの
   dependency audit が終わるまで一旦 sealed に寄せる。

---

## F8. Part B 諮問 (i) — taint の人物・artifact・予測別裁定

### F8.1 artifact taint

`mb/ninfty-branch-search/v1` の artifact は、明示値 field の有無にかかわらず
\((a,p,f_6)\) と `h` から禁止量を復元できる。従って同 schema の全
\(N_\infty\) run を tainted とする。これは「読者が実際に平方類まで計算したか」
には依存しない。

### F8.2 person/role taint

| 人・役割 | 裁定 |
|---|---|
| 手計算を自己申告した担当者 | 開示済み 8 件と v1 run の blind selector / Freeze-2 blind signer から recuse。停止・自己申告は正しい対応であり、違反の拡大を止めた |
| 報告で値を知った司令塔 | 同じ recusal。委嘱・保存・人員配置はできるが、当該 run の救済、候補順位、sq/ns 割当、blind acceptance を単独裁定しない |
| 本便を監査した Sol | 同じ値を知得したため、clean blind steward ではない。数学・schema の敵対監査は可能だが、pre-Freeze-2 の候補選択や (P1)/(P2) blind signer にはならない |
| 同じ報告・明示値を読んだ者 | access log で同じ taint scope に入れる |
| 値を一切受け取らない新 steward | 新 campaign の blind selection/freeze signer 候補になれる |

「一度知った値を忘れたことにする」は不可である。ただし recusal の範囲を
数学的結論より広げすぎてもいけない。

### F8.3 (P1)/(P2) への影響

- **当該 8 件**: 値が開示されたので、もしこれらを候補として救済するなら
  (P1) の blind 性は失われている。しかし F6 により全件は数学的に失格であり、
  そもそも当該値から campaign の (P1) 結果を作ってはならない。
- **将来の genuine candidate の (P1)**: 今回知れたのは失格 tuple の定数で
  あり、未発見の正しいモデルの定数ではない。従って campaign の
  preregistered (P1) 自体が論理的に開封・反証されたわけではない。
  新 campaign の sealed deterministic selection と clean signer により、
  将来候補についての blind evidence は再構築できる。
- **(P2)**: 一つの失格 tuple の \(C\) から二 dessin の
  \([u_{\rm ns}^{-1}]_{10}=[u_{\rm sq}^{-1}]_{10}\) は決まらない。
  従って (P2) の値が数学的に漏れたとは判定しない。ただし、知得者が
  candidate selection や sq/ns 割当へ関与すれば pairwise 選別バイアスを
  入れられるため、運用上は recuse が必要である。

従って taint は、

- Freeze 1 や定理 statement を撤回する全 campaign 汚染ではない、
- v1 の \(N_\infty\) run とそれを見た人の pre-freeze 選別権を止める
  **run/role 単位の汚染**

と裁定する。全体状態は `BRIDGE-UNKNOWN` のままである。

---

## F9. Part B 諮問 (iii) — 修正版 stage 2 と独立照合器

### F9.1 searcher v2 の必須数学条件

1. `q` を「割れる限り」除去しない。固定次数 resultant が強制する
   baseline multiplicity を一般補題で証明してその分だけ除くか、よりよくは
   homogeneous/two-chart の fiber divisor を直接計算する。
2. \(x=0\) chart を明示的に検査する。「\(s=\infty\) だから artifact」と
   呼んで幾何点を捨てない。
3. 各有限 branch value の fiber を exact に分解し、
   \(2^2 1\) を multiplicity partition として検査する。適切に飽和した
   degree-5 fiber polynomial \(H\) なら、少なくとも
   \[
   \deg\gcd(H,H')=2,\quad \gcd(H,H')\text{ squarefree},\quad
   \gcd(H,H',H'')=1
   \]
   を要求する。三重点なら最後が非自明になり、また
   \(\gcd(H,H')\) が重根を持つ。
4. branch value が所望集合以外に無いことを projective に検査する。
5. 今回の 8 tuple を全て negative regression fixture とし、
   `triple-fiber-at-x0` で拒否する。
6. synthetic resultant pattern だけでなく、実曲線・実写像から出発する
   end-to-end positive control を一つ用意する。それが無い間は
   `candidate detector calibrated` ではなく
   `partial predicate / UNKNOWN` と札を下げる。

### F9.2 独立照合器

候補が出た時点で従前申告どおり必須である。ただし v1 hit を照合器へ
渡して救済するのではなく、v2 全域再走の出力に対して新設する。

独立照合器は、

- searcher の `mb-frac.mjs`、`mb-polyops.mjs`、resultant helper を共有しない、
- exact arithmetic と projective fiber calculation を別実装する、
- canonical input digest へ束縛する、
- curve squarefree、norm/divisor identity、全 fiber partition、
  branch set、degree/genus を再計算する、
- mismatch、未処理 chart、飽和失敗を `UNKNOWN` へ丸めず
  `INTEGRITY_STOP` とする、
- pre-Freeze 2 の human-visible 出力を
  candidate ID、input/output digest、三値 verdict、reason code、
  `partition_ok` 等の非漏洩 boolean に限定する

こと。`C`、`h`、\(a_5\)、leading coefficient、平方類、因数、符号を
ログ・例外文・fixture 名へ出してはならない。

二 checker の一致は正しい predicate を前提として初めて意味を持つ。
従って exact fiber-partition specification を文書で先に凍結し、
その後に二実装を作る。

---

## F10. Freeze 2 候補受領プロトコル

現 8 件には入口資格がない。再開時は次の順序を必須とする。

### F10.1 version/campaign gate

1. Rule 1/manifest/whitelist/search schema を version bump する。
2. 新 campaign ID、frozen source digest、探索宇宙
   \(N_\infty\), bound \(\le5\) を事前登録する。
3. v1 artifact の retraction/taint sidecar と access log を固定する。
4. clean blind steward と sealed runner を指名し、担当者・司令塔・Sol の
   recusal scope を記録する。

### F10.2 sealed enumeration と二 dessin 独立性

1. sq/ns はそれぞれ独立の canonical list、全順序、tie-break を使う。
2. 一方の候補・値・順位・曲線同型を、他方の候補選択へ入力しない。
3. 同じ曲線が独立選択の結果として出ることは許すが、同一曲線を前提に
   強制しない。
4. Pell 内部表現、\(C\)、`h`、正規化係数は seal 内だけで扱う。
5. 一方しか閉じなければ保存して `UNKNOWN`。片翼を先に Freeze 2
   または Extractor へ渡さない。

### F10.3 各 dessin の reception certificate

各翼について、少なくとも次を exact に閉じる。

- genus-2 曲線の非特異性と canonical model digest、
- Belyi map の完全な式と
  \(\operatorname{div}(\lambda)=10P_0-10P_\infty\)、
- branch set がちょうど \(\{0,1,\infty\}\) で、
  passport \((10,2^4 1^2,10)\) であること、
- exact monodromy triple、推移性、標的 fixture への exact conjugator、
- \(\operatorname{Aut}(C/\mathbb P^1)=1\)、
- cusp \(P_0,P_\infty\)、\(\mathbb Q\)-有理 uniformizer の式と
  uniformizer 性、
- searcher/checker の独立一致と全 digest、
- Rule 1 の canonicalization/tie-break trace、
- \(b_i\) の規定どおりの記録。ただし candidate selection に使わず、
  \(b_{\rm sq}=b_{\rm ns}\) の pair gate が破れたら \(u\) を開けず停止。

### F10.4 atomic Freeze 2

両翼が独立に reception PASS した後に限り、一つの canonical bundle に

- 両 model/map、
- actual marking/conjugator、
- 両 cusp/uniformizer、
- reception certificate と access log、
- selection trace と全 digest

を同時に封じる。clean steward が atomic joint freeze を署名した後、
その**同じ bundle の係数を直接読む**二 extractor と、一回性
`FIRE_k5bridge.auth` を起動する。digest だけ共有して係数を別転記しない。

担当者・司令塔・本 Sol は freeze 後の敵対的数学監査には参加できるが、
この clean blind signature の代役にはならない。

---

## F11. ★教材

1. **判別式の指数は fiber partition ではない。** 総 ramification
   contribution が同じなら、三重点一つと二重点二つを区別できない。
2. **「artifact」は因子の零点集合でなく、証明された multiplicity まで
   指定しなければならない。** 一因子が機械的でも、その高い冪は genuine
   geometry を含みうる。
3. **較正値から外れた `power=3` は候補 metadata でなく警報である。**
   end-to-end positive control の欠落時ほど、予想 multiplicity からの逸脱を
   fail-closed にする。
4. **whitelist は変数名でなく prediction dependency で作る。**
   `h` と呼んでも \([h]=[\hat c_\mu]\) なら I-b∞ の同値物である。
5. **70/70 green は program の faithful execution であり、predicate の
   正しさではない。** 同じ誤った stripping rule を全 shard が忠実に走らせても
   cross-check にはならない。
6. **自己申告と即時停止には実益がある。** 違反を無かったことにはしないが、
   monodromy、sq/ns 割当、Freeze 2、Extractor まで汚染を広げずに済んだ。
7. **失格候補の封印値と、将来の genuine candidate の封印予測を混同しない。**
   前者の漏洩は run/role を汚染するが、後者の theorem statement を反証したり
   自動的に開封したりはしない。

---

## F12. 共同設計者としての発案

### F12.1 dependency-typed whitelist

各出力 field に、

```text
semantic_quantity
determines_prediction = [P1, P2, ...]
release_stage
branch_scope
```

を持たせる。\(N_\infty\) には機械可読な規則

```text
branch_value_square -> squareclass(c_hat_mu) -> P1
```

を登録し、名前を変えただけの同値量も gate で拒否する。

### F12.2 fiber-partition certificate

判別式を一個出すだけでなく、各 branch fiber について

```text
chart_id
fiber_degree
multiplicity_partition
gcd_degree
gcd_squarefree
triple_gcd_degree
projective_coverage
```

を記録する。ただし branch value 自体は sealed field にし、人間可視
certificate には digest と partition だけを出す。

### F12.3 taint ledger

artifact と人物を分け、

```text
artifact_digest / schema / campaign_id
forbidden_quantity_kind
exposure_time
person_or_role
actual_knowledge / mere_access
recusal_scope
allowed_post_freeze_role
```

を記録する。これにより「全員永久排除」と「何も起きなかった」の二択を避け、
run/role 単位の裁定を再現できる。

### F12.4 theorem 化

Rule 1 に次を補題として入れるとよい。

> **N∞ branch-square leakage lemma.**
> \(\mu^\iota=C/\mu\) かつ有限分岐値集合が \(\{\pm s\}\) なら
> \(s^2=\pm C\)。特に \(-1\in K^{\times2}\) なら
> \([s^2]=[C]\in K^\times/K^{\times2}\)。

これを I-b∞ の「同値 leading class」の具体例として参照すれば、将来
`h` が別名で再導入されることを防げる。

---

## F13. 監査範囲外申告

### 監査したもの

- commit \(C=38e4652...\)、tree `edf120...`、
  commit \(R=686ceea...\) と両者の差分。
- Part A の三文書、CLAIMS W3-17/W3-18、BFC certificate、
  Node checker 二本、GAP script digest、manifest、lint v4、triage、
  receipt、三 mutant selftest。
- `docs/mb/委嘱4_報告.md`、`sol/裁定_65_mb4_quarantine.md`、
  `docs/manifest_k5_v1.md`、Rule 1 v1.3、Sol 便 42 F3。
- `search/mb-ninfty-branch-search.mjs` の stage 1、resultant、
  quadratic stripping、hit schema。
- local に保存された run `30289323147` の summary と 4 hit shard の
  exact JSON。
- 8 coefficient tuple に対する式 (54.1)–(54.4) の紙上検算、および
  開示済み代表に対する resultant 係数の exact 再構成。

### 監査していないもの

- GitHub Actions UI/API そのものの外部再照会。70 green は local に保存された
  immutable artifact と summary を監査した。
- 8 hit の monodromy、exact conjugator、Aut、sq/ns 適合性。
  F6 でより早い必要条件に反して全件失格したため、実行する理由がない。
- \(\hat c_\mu\) の平方因子・\(K\)-平方類、(P1) の実ビット、
  \(u\)、leading class、(P2) の値。これらは計算していない。
- 新 searcher/checker の実装、bound 5 の再走、Freeze 2 bundle、
  Extractor、Lean 形式化。

本便の `verified` 主張はない。Part A は hash・再走・git provenance の
検収、Part B は紙上証明と既存 exact artifact の敵対的監査である。
