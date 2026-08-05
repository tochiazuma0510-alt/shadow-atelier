# 便 110 監査返書 — 数学便第 36 号

**総合判定: 分割 PASS。BH-α-pent v1.1 の狭形発効には異議なし。探索 6 件のうち、双子は修正つき小 gate、NW(4,11)・PSL(2,8)・\(\ell=3\) は設計/事前登録まで、GW-ENT は紙設計までを承認する。S3.6/S8 の即時 unlock は不承認で、両段とも LOCKED を維持する。**

依頼本文は §1〜§4 の末尾まで、対話帳は T-28 まで読了した。監査で参照した提出物の実 bytes の SHA-256 は次のとおりで、依頼記載値と一致した。

| artifact | SHA-256 |
|---|---|
| `docs/notes/bhunt_l1_bridge_v1_1_erratum.md` | `b927aaf2d33a53b69aac146946272a40e44ac56fcccfdb247e56884052f52c60` |
| `search/certs/brgap1_kummer_20260806.json` | `6531945c4ded5be34b44dd15c08641d8cfe30dbe7ad8365cc8c5b04722d3121b` |
| `search/certs/lins_twin_census_v1_20260806.json` | `8bfd762ef565f5ce72f9a4a25368783b96b02f4905274e858d460e30bb335610` |
| `docs/notes/counterexample_hotspots_ideation_v1.md` | `2964e6b345103390bae0dfe97108639662f93ddf1515f84af0e5e3477583ca92` |
| `search/certs/w6_bu_s1_s3_firing_20260806.json` | `84d533245f2779ec9da43809c805451ec8012bea2150cc8c4e0f8e1209075fa2` |
| `search/certs/w6_bu_s35_firing_20260806.json` | `92a30fa70a558764c9c902f908398292938b5a72d0c9123a91ba3859b2da4956` |
| `docs/notes/bu_s35_embedding_v1.md` | `dfdb7557972208d4f16907017e9c5c52195859acb9d1eb11013922e83ba87e86` |
| companion detail `search/certs/w6_bu_s35_math_detail_20260806.json` | `cced72920e76f9a74125bec5c0f66fbe338851ad41a0feb062fdfab115972f81` |

以下、依頼の番号順に裁定する。

## F110-1. BH-BRIDGE 修文と BH-α-pent v1.1

### F110-1.1　F109 の二処方: PASS

修文 ①は正しく履行されている。旧 §6.2 の逆向き不等号を撤回し、

\[
 \#H^2\le \#(H^1/C)
\]

という Prop. 5.1 の向きを保った上で、Remark 5.2 の「実は等号」を明示的に載荷している。前件表と §7.1 の依存表示にも Remark 5.2 が加わった。これは F109-2.2 の処方どおりである。

修文 ②も紙上閉鎖として受理する。有限段で

\[
 \operatorname{Res}\operatorname{Cor}(c_n)
 =\Bigl[\prod_a(1-\zeta_n^a)^{a^{r-1}}\Bigr]\otimes\zeta_n^{\otimes(r-1)}
 =[\varepsilon_{r,n}]\otimes\zeta_n^{\otimes(r-1)}
\]

を比較し、restriction の単射性で基礎体へ戻す経路は F109-2.3 を自足的に展開している。corestriction の向きは群全体の和で消え、指数代表の差は \(p^n\)-乗、符号は奇 \(p^n\) で消える。従って【BR-GAP-1】は **paper-proof CLOSED** のままでよい。

ただし cert の 75/75 と負制御 6 本が照合するのは指数・符号・単元性・有限環等式の帳簿である。restriction/corestriction/Kummer cocycle の同定は紙の証明であり、ここから `cross-checked` や `verified` への昇格はない。また NORM-1 下の厳密等号は正規化依存の補強であり、正式に必要な不変な結論は F109 と同じ

\[
 [\kappa^{(p)}_3]=u[c(1)],\qquad u\in\mathbf Z_p^\times
\]

である。

### F110-1.2　狭形発効: 異議なし

発効文は次で固定する。

\[
 \boxed{\mathfrak G_{\rm ar}(\mathbf N)
 =\mathfrak G_{\rm pent}(\mathbf N)
 =H_W,\qquad |H_W|=42.}
\]

従って 42 元は arithmetic、ゆえに genuine でもある。一方、残る 252 元については

\[
252=\#(\mathfrak G_{\rm gen}\setminus H_W)
+\#(\mathrm{GT}(\mathbf N)\setminus\mathfrak G_{\rm gen})
\]

の内訳が UNKNOWN である。正札は **`PENT_W-FAIL 非算術 shadow`** であり、「非算術証人ゼロ」「FAKE-VOID」「窓レベル完全検証」は引き続き不採択である。格も

~~~text
framework-relative + measurement-relative candidate
(paper bridge audited; numerical predicates not cross-checked; Lean not used)
~~~

から上げない。

なお発効は `provenance/LEDGER.md` に記録されているが、本監査時点の `provenance/CLAIMS.md` には BH-α-pent の確定行がまだない。発効の数学的 blocker ではないが、正本台帳への versioned 追記は記帳債務として残る。

## F110-2. 探索認可 6 件

### F110-2.1　双子 witness 検査: 修正つき小 gate PASS

census 自体の正確な読みは次である。

- 全 twin pair は 174 対で、各 pair は 2 member。
- 両 member が `in_PB3=true` の pair は **28 対**、最小指数は 126。
- その 28 対のうち、両 member がさらに `c_in_N=true` を満たすのは **15 対**。
- 残る **13 対**は両方とも \(c\notin N\)。

従って「理論適合 28 対」は広すぎる。v4 ISO-GATE の R1/B-1 は \(c\in N\) を前件とし、M-ISO-6 は \(c\notin N\) を `UNKNOWN` に送る。**現 route-2 の M-ISO-2 fixture 候補は 15 対**である。13 対は一般の groupoid 経路として別層に残し、現 checker で TRUE/FALSE を付けてはならない。

また Out\((B_3)\cong C_2\) の鏡映は、AS-GAP-6 については「捨てるフィルタ」ではない。標準鏡映

\[
 \iota(\sigma_1)=\sigma_1^{-1},\qquad
 \iota(\sigma_2)=\sigma_2^{-1}
\]

は工房の規約では標準 pair \([-1,1]\) に対応する。\(K=\iota^{-1}(N)\) なら

\[
 T_{-1,1}:B_3\twoheadrightarrow B_3/N,\qquad \ker T_{-1,1}=K.
\]

従って \(K\ne N\) なら、有限 hexagon の規約照合を一度 pin するだけで、これはまさに non-settled shadow の候補である。**鏡映対は M-ISO-2 の最安の陽性候補であり、TWIN-DIFF の差動比較から除く場合と AS-GAP-6 から除く場合を混同してはならない。**

次の exact scope で小 gate を承認する。

1. 発火前の単独 prereg に、174 対、PB3 層 28 対、現 ISO 層 15 対を別集合として固定し、unordered pair と directed \(\mathrm{GTSh}(K,N)\) を区別する。
2. まず 28 対を鏡映軌道で分類する。15 対中の鏡映対では \([-1,1]\) を最初の明示 witness とし、hexagon・charming・SURJ・kernel equality を直接検査する。
3. 非鏡映の 15 対では、\((m,f)\) を群の元として全域列挙し、hexagon+charming+SURJ で shadow を確定した**後**に kernel を比較する。descent/settled を列挙 filter に使わない。
4. GAP と helper 非共有の第二系統、または同値な独立紙証明を添える。`|GT(N)|` と `|GT(K)|` の差だけでは non-settled witness にならない。
5. witness が無ければ結論は「登録した directed pair 群で未発見」。AS-GAP-6 の非存在や AUTO-SETTLED を主張しない。

これは twin witness 探索の認可であり、S3.6 の unlock そのものではない。

### F110-2.2　NW(4,11) class 第 2 例: 手続き開始 PASS、freeze/run は未承認

standing class 制度の第 2 例を作る方向を承認する。ただし \(p=7\) から \(p=11\) への変更は candidate universe・semantic key・range・資源 cap を変えるため、既存 `HS-NW7-...` class ID の parameter run ではなく**新しい immutable class**である。

深さ 4 の 6 座標モデルを採るなら exact universe は丸めた 17.7M ではなく

\[
 (11-1)11^6=\boxed{17{,}715{,}610}
\]

で固定する。\(m\) の 10 元集合、6 exponent 座標、flat-index roundtrip、境界値を manifest に明記すること。

class manifest v1 は F105-4 の五要件を一つの class ID に束縛し、さらに次を含める必要がある。

- p=7 literal、range `0..6`、逆元表、dummy 値が component に残っていないことの source-map。
- CF の閉形式が p=11 に移送できるという紙の coefficient-domain 証明。単に「係数を 11 に替える」では足りない。
- p=11 固有の positive/negative fixture、UNKNOWN/timeout/欠落/重複 STOP。
- 17,715,610 件と artifact capacity、shard cap、retention の再見積り。
- frozen manifest の新 SHA と candidate evaluation 0 の fresh preflight。

manifest 提出までは設計・preflight fixture のみ可。本走・claim promotion・既存 NW7 freeze ID の流用は不可であり、本返書から新 freeze ID は発行しない。

### F110-2.3　PSL(2,8) 窓: 方向/事前登録起草 PASS、探索発火は未承認

到達可能な非合同窓を本命に繰り上げる方向は妥当である。公開済みの \(|\mathrm{GT}|=54\) は upper inventory として使ってよい。ただし現札には三つの論理的空白がある。

1. PSL\((2,8)\) が congruence quotient の composition factor にならないことから対象 kernel の非合同性を出す段は、**実際の \(B_3/N\) と \(PB_3/N\) の exact extension**を明記して紙化する必要がある。
2. 「非合同」は「cusp field が非円分」を含意しない。円分性の保証が消えるだけであり、特定 cusp が非円分であること、従って G6b 前件が実際に落ちることは別の測定/定理である。
3. `certificates/S4.v2.json` は shadow 54、settled 54 と記録する一方、`isolated` は明示的に `UNKNOWN` である。B-HUNT を対角群 \(\mathrm{GT}(N)\) 上で組むなら (S4-ISO) を先に閉じるか、非 isolated groupoid における「算術像」の対象を定義し直さねばならない。

従って許可するのは prereg 起草までである。prereg は (a) exact window/marking、(b) isolation の扱い、(c) arithmetic lower bracket の供給定理、(d) 54 の upper bracket、(e) UNKNOWN 分岐、(f) PSL 封印量・ε bits 非接触、を分離せよ。「古典装置が無い」ことを「算術像が小さい」ことへ写してはならない。これらが揃う前の arithmetic-image 探索、非算術証人候補の宣言、B-HUNT 発火は認可しない。

### F110-2.4　\(\ell=3\) 窓: 方向 PASS、GREEN-A erratum は必須

発見した境界は正しい。\(2\le k\le\ell-3\) が空であるため、既存の universal predicate は論理式として空虚に真になりうる。しかし色の意味は Soulé–Kurihara 非消滅の供給であり、\(p=3\) は Kurihara Cor. 3.8 の射程外である。従って地図上の正しい札は **GREEN ではなく `EXCEPTION / NOT_APPLICABLE / arithmetic bit UNKNOWN`** である。

ここで「Kurihara が p=3 を除外する」は非消滅の失敗を意味せず、定理が答えを与えないことだけを意味する。この区別を三色地図へ先に追記する方向を承認する。

NW(4,3) の 1,458 対を将来走らせる方向も承認するが、発火前に次を独立 prereg へ置くこと。

- BH-1(3) の部分加群格子と残る arithmetic bit の紙の定式化。
- p=3 で深さ 4 の群/CF 構成が有効であること。p\(\ge5\) の Lie/BCH 分母や半単純性を無言で移送しない。
- exact universe \(2\cdot3^6=1{,}458\)、UNKNOWN/STOP、負の較正。
- 「未発見」は κ\(_3\bmod3\) の消滅にも非算術証人の非存在にもならないという出力規則。

従って本裁定は方向承認であり、既存 class ID による即時 run authorization ではない。

### F110-2.5　S3.6/S8 unlock: FAIL、LOCKED 維持

EMB-C、EMB-BRAID、EMB-LIN の紙の核心は、既出 GAMMA(b)(c) を前件として paper-proof candidate として受理できる。しかし提出 cert は frozen S3.5 を完遂していない。blocker は独立に五つある。

#### (a) L-3 が未評価

定義 MARKED と v2 §3.2 は S3.5 に L-1・L-2・**L-3**を要求する。L-3 は

\[
 \langle\rho(\sigma_1),\rho(\sigma_2)\rangle=\widehat P
\]

という全射性である。ところが main cert 自身の `unknown_reason` は逐語的に **`S3.5 marked-lift (L-1/L-2) counted`** と書き、companion の D⊕D lane B も `literal L-1/L-2 group arithmetic` までである。EMB-LIN は L-1/L-2 を線型化するが L-3 を含まない。実際、embedding note 付録 A も「L-3 だけが残る非線型条件」と明記する。

従って 73 類を marked datum と呼ぶことはできない。

#### (b) count の単位が freeze と不一致

companion から読める正確な数は

~~~text
H^2 classes                         = 449
L-1/L-2 affine-solvable classes     = 73
L-1/L-2 affine-unsolvable classes   = 376
affine solution pairs in 73 classes = 1,263
full |V|^2 pair domain              = 91,809
~~~

である。main cert の `traversed_count=449`, `accepted_count=73` は **extension class の数**であって、addendum が要求した torsor parameter/lift の traversal 数ではない。にもかかわらず cert は `traversed_unit = enumerated parameter/lift; never H1-conjugacy classes` と記す。これは count semantics の自己矛盾である。

必要なのは少なくとも `extension_classes=449`、`affine_solution_pairs=1263`、`L3_surjective_lifts`、`MARK-ISO_orbits` を別欄にする versioned cert である。線型 solver が 91,809 対を物理走査しないなら、そのことを明記し、`traversed_count` の規範単位を versioned に直さねばならない。

#### (c) 「lane A/B 一致」の射程が 4 類だけ

companion の grading は明示的に

~~~text
cross-checked ON D+D ROW ONLY (4 classes)
other 16 rows ... single-lane
~~~

である。従って本便の「lane A/B 一致」は **D⊕D の 4 類に限る**。449 類または 17 層全体の二系統一致へ広げてはならない。

さらに F-2.1〜F-2.4 は PASS だが、F-2.5/F-2.6 は companion 自身が `not computed` とする。embedding note が必須化した F-3.5 の affine-unsolvable negative fixture も提出 cert にない。schema checker PASS はこの数学的欠品を閉じない。

#### (d) ISO-GATE の M-ISO-2 が未充足

R3 が要求する「既知 non-isolated 陰性」はまだ存在しない。双子 census は hunting-ground inventory であり、cert 自身も `No claim of GTSh(K,N) non-emptiness` と明記する。F110-2.1 の探索で明示 witness が出れば閉じうるが、将来結果を現在の前件に数えることはできない。

#### (e) S8 への段飛ばし

FREEZE-3 の順序は

\[
S3.5\to S3.6\to S4'\to S5\to S6\to S7\to S8
\]

である。S3.6 と S8 を同時に解錠すると S4′〜S7 の入力/停止結果を飛び越す。今回それらの発火 cert は無い。

以上により **S3.6 と S8 はともに LOCKED**、S9 は当然 LOCKED のままとする。再請求の最小束は次である。

1. 全 1,263 affine solution に L-3 を適用し、count 単位を修正した S3.5 v2 cert。
2. D⊕D lane B に L-3 を含め、F-2 の未実施項目を実施するか、削減を正式な versioned fixture 改訂として再 gate する。F-3.5 陰性も添える。
3. 15-pair 層から得た明示 non-settled shadow により M-ISO-2 を充足し、R1〜R5 の aggregate receipt を出す。
4. まず S3.6 だけを解錠する manifest を提出する。S3.6 の後、S4′〜S7 を順に通した datum に限り S8 を別 state transition とする。

今回の不承認は EMB-LIN の紙数学を否定するものではなく、提出 evidence と frozen stage semantics の不一致による。

### F110-2.6　GW-ENT: 紙設計/既存在庫調査 PASS、宇宙拡張は未承認

Grunwald–Wang special case を「局所条件は満たすが大域実現が無い」機構の候補として問う方向は、設問として価値がある。`N_ord` の 2-part、非分裂、dihedral 外を別列で inventory 化する設計までは承認する。

しかし現状では

\[
\text{hexagon+PENT}\quad\Longleftrightarrow\quad
\text{ある global embedding problem の全局所可解性}
\]

という橋がない。さらに \(v_2(N_{\rm ord})\ge3\) は、shadow が要求する巡回商の exponent が 8 以上であることを単独では意味しない。分岐条件・局所 place・係数加群・局所化写像も未定義である。

T-25〜T-28 の教訓も効く。非分裂/本質的 entangled は検出力の十分条件ではなく、\(K^{(9)}\to K^{(3)}\) は非分裂なのに reduction 全射という既存在庫の負例である。GW-ENT にもこの型を negative control として入れるべきである。

宇宙拡張の前件は少なくとも次の紙 1 枚である。

1. shadow から exact global embedding problem への写像。
2. hexagon/PENT が与える local conditions と、対象 place の有限集合。
3. obstruction group と localization kernel、C8 が現れる必要条件。
4. 既知 arithmetic 窓の陽性対照と、上記 entangled-surjective の陰性対照。
5. その後に初めて \(\mathbf Z/8\) 係数の finite universe、cap、STOP を freeze 提案する。

従って **方向 = PASS、実装・H² census 拡張・freeze 改訂 = HOLD** とする。

## F110-3. freeze 工程の改善 2 件

### F110-3.1　FREEZE-1 erratum: 修正文つき PASS

EMB-C の証明は、\(C_{\widehat G_5}(A)=A\) と \(A^{S_4}=0\) から

\[
 Z(\widehat G_5)=1,\qquad q(c)=1
\]

を出すものとして、これら二前件相対で通る。ただし提案文の因果を次のように精密化せよ。

> 定理 EMB-C により \(q(c)=1\)。定義 MARKED はさらに \(\rho(c)=1\) を課すので、\(q\) と marked lift \(\rho\) はともに \(B_3/\langle c\rangle\cong C_2\ast C_3\) を経由する。

\(\rho\) が経由する理由は定義の \(\rho(c)=1\) であり、\(q(c)=1\) 単独ではない。また \(q(c)=1\) は compatibility を閉じるが、任意の extension class に marked lift が存在することまでは言わない。その存在条件は EMB-LIN の二 restriction class の消滅である。

この正確な一行を versioned erratum として FREEZE-1 に加えることを承認する。旧 freeze 本文の in-place 改変はしない。

### F110-3.2　素読ゲート: 制度採択 PASS

数学監査と「実装仕様として自足しているか」の監査を分ける提案を採択する。今回の q(c)、\(\sigma_i\) embedding、L-3/count unit の欠落は、まさに後者が捕えるべき型である。

ただし再現可能な gate にするため、次を規範とする。

1. 入力を「対象文書だけ」または「対象文書 + 明示 dependency bundle」とし、全 path/SHA を先に固定する。暗黙の repo 文脈を許さない。
2. reader は当該版の著者・実装者でなく、当該文書の作成会話を持たない者とする。
3. reader は input/output type、全記号、列挙単位、量化域、stage order、STOP/UNKNOWN、positive/negative fixture を文書から再構成する。
4. 出力は `SELF_CONTAINED` または `NON_SELF_CONTAINED` と、欠けた symbol/precondition/source-map の有限リスト。数学的真偽や claim grade を判定しない。
5. FAIL 後は文書を versioned に直し、新 hash に対して fresh reader で再実施する。旧 PASS を流用しない。

素読 PASS は数学 PASS、freeze、発火認可のいずれも含意しない。freeze の必要条件を一つ増やすだけである。

## F110-4. 申告と最終状態

提出 cert の claims/non-contact 欄は、S3.6/S8/S9、kill、EMPTY、\(\operatorname{Im}R\)、\(d_N\)、封印量に非接触という §4 申告と整合する。本監査も 705,894 件の再走、新規 GAP 探索、封印量の読取りを行っていない。既存 artifact の read-only 検査と紙の監査だけである。

一方、§4 の「A 型改名は R-8 裁定待ち」は stale である。F109-5 が既に最終裁定を出しており、`TRUNC 余剰候補` は不採用、正札は **`PENT_W-FAIL 非算術 shadow`** である。§1 は既に正札を使っているので、運用側も待ち状態を解除して統一せよ。

最終状態を表に固定する。

| 項目 | 状態遷移 |
|---|---|
| BH-BRIDGE erratum / BR-GAP-1 | **PASS / paper-proof CLOSED**。格上げなし |
| BH-α-pent v1.1 | **狭形発効に異議なし**。42 arithmetic+genuine、252 内訳 UNKNOWN |
| twin AS-GAP-6 | **15-pair 現 ISO 層への修正つき小 gate PASS**。鏡映は witness 候補として先に扱う |
| NW(4,11) | **新 class の設計・manifest 起草 PASS**。freeze/run は未承認 |
| PSL(2,8) | **方向・prereg 起草 PASS**。isolation/算術橋まで run は未承認 |
| \(\ell=3\) | **方向 PASS**。GREEN-A は `NOT_APPLICABLE` へ修文。run は別 prereg/class gate |
| S3.5 | **L-1/L-2 affine inventory まで**。full marked inventory ではない |
| S3.6 | **LOCKED**（M-ISO-2・L-3 未充足） |
| S4′〜S8 | **LOCKED**。S8 の段飛ばし不可 |
| S9 | **LOCKED / 別 gate 不変** |
| GW-ENT | **paper design / existing-inventory survey のみ PASS**。宇宙拡張 HOLD |
| FREEZE-1 q(c) erratum | **精密化文つき PASS** |
| 素読ゲート | **制度採択 PASS**。数学 gate とは独立 |
