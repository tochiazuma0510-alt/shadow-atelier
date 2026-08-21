# T-33 発案札 v1 — 標的 A(SINGLE(x) の selection theorem 設計)/ 標的 B(非可換 chief S^t の反模型排除)

**状態札**: `発案札・全札 candidate・数学者/Sol の検証前・定理口調禁止の対象文書`
作成: 発案係(ideator)/ 2026-08-18 / 発注 = 司令塔(T-33 のうち構造が薄い二箇所への札供給)
入力 = 対話帳 T-28〜T-33・`ops/express/20260818_sol_fable_b4_cofinal_step.md`(追伸: 正しい次段有限対象は relative `K_*/N_{K_*}(3)`)・sol 便 148/150/151・`set_surgery_vetting_v1.md`・`cofinality_ledger_draft_v1.md`
⚠ **非接触宣言**: 封印 3 量・u/c の値と平方類・sealed K^{(5)} インスタンスに非接触。以下で u が現れる箇所は**形式変数**(u=2m+1)としてのみ。
⚠ **NAME-COLLIDE 警告**: 本書の **K(5) = Stasheff associahedron**(arity 5・T-30/T-31 の用法)であり、**封印対象の dihedral 窓 K^{(5)} = ker(ψ₅) とは同名別物**。また sol 便 148/150/151 は **gentle/B₃ 側**(972 屋根)の先行技術であり、T-33 の **full B₄ Main-Line** とは同構造別系(T-29 §1 の混同禁止)。gentle 側の補題を B₄ に使う札は、その旨を破綻点に自己申告する。

## 0. T-33 禁止短路(5 本)との抵触自己申告

T-33 末尾の禁止: ①一段の surjectivity の自動伝播 ②strict deletion-kernel ③AP filler と PB3 correction の同一視 ④K(5) contractibility だけによる effectivity ⑤centerless/Schreier だけによる compatible lift の存在。

| 札 | 抵触の有無 |
|---|---|
| A-1〜A-7 | ①の再提案はしない。A-2 は「coarser 方向への伝播」を使う(禁止は finer 方向)— falsifier 判読を一手目に含めた |
| B-3 | **④に隣接**(K(5) を使う)。ただし contractibility「だけ」ではなく π₀ 推移性という追加 literal 条件を要求する形 — 札内に明記 |
| B-4 | **⑤に隣接**(centerless Wells を部品に使う)。ただし「だけ」ではなく coprime 条件を追加する形 — 札内に明記 |
| 他 | ②③には全札非抵触(strict kernel・AP filler を使う札なし) |

記号は T-29/T-33 のまま: X=ML(M)(|X|=972)、A(|A|=324, [X:A]=3)、I_K=im(ML(K)→X)、F_K(x)={z∈ML(K): z|_M=x}。閉済前提(T-33 §2 の 1〜6)は入力として固定し再監査しない。

---

# 標的 A — SINGLE(x) を与える inverse-system selection theorem の設計(7 札)

## 【A-1 CHAIN-REDUCE】family を matched pure-power tower の鎖そのものに取り、「family 選択問題」を消す

- **種別**: 構成 / **規模**: 現在線級 / **出所**: 閉済前提 5 と gentle 側敗因の構造比較からの推測
- **一行機構**: SINGLE(x) の C を、閉済前提 5 の matched pure-power tower(K_j = M∩N(q_j)、q_j=lcm(1..j)。次段対象は速達どおり relative `K_*/N_{K_*}(3)` 型で刻む)の**鎖**に取る。鎖には比較不能対が存在しないので、gentle 側の敗因 — 比較不能な isolated 窓同士の glue(COPRIME-GLUE-148 / MODULE-SEPARATED-GLUE-150 の適用限界)と c² 型反例(sol_reply_151 §4.3: X_s は c² を含み L=M∩N_5^cyc は含まない)— が**発生する場所ごと消える**。残債務は「鎖に沿った一段ずつの relative jump」のみ。
- **効くと思う理由**: (i) tower の cofinality は閉済前提 5 で既に持っている(指数 e の有限商は N(e) を殺す、の型)。(ii) 151 §4.3 の反例は「固定した族が**別方向の** isolated 窓の下に入れない」形であり、cofinal な鎖ではこの型が定義から起きない。(iii) SINGLE は互換 thread を要求しない(閉済前提 2/3: 段ごとに seed が違ってよい)ので、鎖上の各段独立の有限問題に完全分解する。
- **検証の一手目**(数学者への設問形): 「(i) tower の各段は isolated か。(ii) isolated でない場合、gentle 側 Prop 3.14 の isolated core(◇)の full-B₄ 類似は存在するか。(iii) core 化は単調(K≤L ⟹ K^◇≤L^◇)で、鎖の core 化は cofinal 鎖のままか」。3 つ YES なら SINGLE(x) ⟺ 鎖-STEP(A-3 へ接続)。
- **in-house grep**: cofinal/compactness 系 = `luna_reply_157br`(power cofinal theorem)・`157cq`(cofinal compactness・閉済前提の典拠)・`157n`・`157ak`(König 監査)。相対 cofinality の一般形は `luna_reply_152_relative_cofinal_v1` が**一般には偽**(direct-factor 障害)と監査済 — 本札はその一般形を使わず、閉済前提 5 の ambient tower + 速達の relative 段だけを使う。鎖化による glue 回避の明文は grep 範囲で見当たらず(「初」とは言わない — 部品は全て既在で、配置が差分)。
- **破綻しそうな点**: isolated 性が tower 段で破れ、core 類似も立たない場合は鎖が SINGLE の要求する「isolated family」にならない。また gentle の ◇ は B₃-groupoid の性質で、full B₄ の ML に同じ命題があるかは全く未検。

## 【A-2 UP-SET / DIVE-UNDER】良集合は上に閉じる — 「反例窓を避ける」選択原理は不要で、「下に潜る」だけでよい

- **種別**: 構成(観察)/ **規模**: 現在線級 / **出所**: functoriality の向きの整理(gentle 側 MONO-CNF-139 からの類推)
- **一行機構**: C_good := {K isolated: F_K(x)≠∅} は**上に閉じる**: K'≤K(K' が finer)なら push-forward ML(K')→ML(K) で F_{K'}(x)≠∅ ⟹ F_K(x)≠∅。ゆえに (a) SINGLE(x) は「cofinal に深い良段の存在」と同値、(b) 「反例窓が現れたら family を曲げて回避する」必要はそもそもない — 反例窓 L の**下のどこか一段** K≤L で勝てば L 自身が自動で閉じる(151 §4.3 の c² 窓も、その下に良段を一つ作れば窓ごと吸収される)。さらに (c) 閉済前提 2(one-outside)により、outside の固定 x で F_K(x)≠∅ が一段立てば同段の I_K=X まで自動昇格。
- **効くと思う理由**: T-33 は STEP(全称・隣接伝播)か SINGLE(cofinal family)の二択で書かれているが、この観察で両者の間に**第三の中間命題「DEEP(x): 無限に深い良段が存在」**が入り、DEEP(x) ⟹ SINGLE(x)。証明義務が「任意の次の refinement」から「自分で選んだ深い段の列」へ最小化される。
- **検証の一手目**: 数学者が push-forward の 3 行確認(z∈F_{K'}(x) ⟹ z|_K ∈ F_K(x))。同時に **falsifier へ判読依頼**: 「これは禁止短路①(一段 surjectivity の自動伝播)に当たらないか」— 当たらないはず(禁止は coarser→finer の伝播。本札は finer→coarser で、写像が実在する向き)。
- **in-house grep**: 同型の単調性 = gentle 側 `MONO-CNF-139`(cofinality_ledger v1.2: Im R_{L,M} ⊆ Im R_{K,M})。full B₄ 側で SINGLE の内部構造として使った明文は grep 範囲で無し。
- **破綻しそうな点**: これは戦略の再配置であり非空性そのものは 1 個も作らない。また「isolated K の push-forward 先も isolated とは限らない」— C_good の上方閉性を isolated 圏内で言うには reduction の isolated 保存(正典 Prop 3.15 類似)を確認要。

## 【A-3 PRIME-SPLIT】鎖の各 jump を chief 分解し「q≠3 は transfer で無料・q=3 は universal split・非可換は標的 B」の三色に塗る

- **種別**: 構成+予想 / **規模**: 中間峰級(SINGLE の主経路)/ **出所**: T-29 §6・T-30 §2 の再配置
- **一行機構**: A-1 の鎖の一段 K_j → K_{j+1} は有限 jump。その chief series で分解すると各層は (α) elementary abelian q-chief(q≠3)、(β) q=3 chief、(γ) 非可換 S^t の三色。(α) は [X:A]=3 の可逆性による res-cor/transfer(T-29 §6 の p≠3 消滅・157z 型)で**typed 計算なしに**吸収、(β) は T-30 §2 の universal split correction(Z 上 split ⟹ 任意係数で exact)+ 157da 型 typed manifest(q=3 typed positive の実績)で処理、(γ) は標的 B の札群へ。SINGLE(x) の残債務が「(β) の constant-coefficient 同定(T-30 §4)+ (γ)」の二点に有限化される。
- **効くと思う理由**: q=3 の一段は 2026-08-18 の run で実際に閉じた(T-33 §1)。(α) が本当に無料なら、鎖-STEP の無限個の義務のうち測るべきは 3-層と非可換層だけになり、しかも速達の relative `K_*/N_{K_*}(3)` は「次の 3-層を一括で越える」対象としてまさに (β) 用に切られている。
- **付記(two-tower gap の観察)**: 素数冪だけで刻む反復 relative 冪塔(K/N_K(p) の列)は各段が有限 p-群で (γ) を含まないが、**perfect 商で停止する**(perfect な Q は全 p で N_Q(p)=Q)。単発 N(lcm) 塔は cofinal だが (γ) を含む。⟹ **非可換 chief は二つの塔の間隙そのもの**であり、塔の取り替えで (γ) を消す路は原理的に無い(速達の「非可換 S^t は別問題として残る」の構造的裏付け。標的 B が不可避である理由の明文化)。
- **検証の一手目**(Sol への限定質問形): 「T-29 §6 の p≠3 res-cor 消滅は S_3-model 上の縮約だが、actual literal A.18 complex の q-chief jump へ適用する際、model との同定は q≠3 でも必要か。必要なら (α) は無料でなく、同定義務が q 一様に残る」— YES/NO と正確な前件を求める。
- **in-house grep**: transfer/coprime = `157z_index3_transfer`・`157cp`・`152_b4_chief_absorption_v3`・q3 checker 内 coprime 検査。chief 分解を鎖の工程表として塗り分けた文書は grep 範囲で無し。
- **破綻しそうな点**: T-29 自身が「§6 は candidate・actual complex との比較未証明」と明記。(α) の無料化が同定ギャップで崩れると、本札は「三色に塗った」だけで債務総量が減らない。

## 【A-4 UNIFORM-WITNESS】q=3 typed witness の word schema は tower 全段で同一のまま通る、という予想

- **種別**: 予想 / **規模**: 現在線級 / **出所**: 値からの推測(witness の複雑性が最小格: exponent=2・correction_index=1・evaluated=28)+ T-30 §2 の係数独立性からの外挿
- **一行機構**: run 32135808950 の witness(exponent=2, correction_index=1)を与えた word schema が、鎖の各段(次は relative `K_*/N_{K_*}(3)`)で**同じ schema のまま** typed positive を与える。立てば鎖-STEP が「schema の全段 replay」という単一の有限計算列になる。
- **効くと思う理由**: T-30 §2 の split correction は Z 上 split で明示逆(a e12+b e14+c e34 ↦ a e12−b e13+c e23)を持ち、**任意係数・任意 mod q で有効** — witness の「形」を段に依存させる要素が correction 側には無い。段依存になり得るのは transport/prefix conjugation(T-30 §4 の 1・2)だけで、そこが同定問題(A-3 (β))と同じ一点に集中する。
- **検証の一手目**: implementer + GHA: 既存 157da manifest を relative 次段で replay し、同一 witness word class が通るか **1 run** 測る。通れば予想の最初の fixture、落ちれば即降格(その場合も A-5 が受け皿)。
- **in-house grep**: 「普遍化」の先行 = `152_cocycle_absorb_universal_v1` が「frozen finite universe では PASS・**全 layer への普遍化は前件からは出ない(UNKNOWN・自動導出は refuted)**」と裁定済。**本札はその裁定に抵触しない差分として立てる**: cohomology 前件からの導出ではなく「同一 word の直接 replay」という機械検証可能な予想(導出でなく測定)。
- **破綻しそうな点**: 152 裁定の趣旨どおり、有限段の PASS 列は普遍性を含意しない。どの段かで correction_index が増え始めたら schema 一定は偽。その場合の情報も無駄にならない(増加列自体が A-5 の入力)。

## 【A-5 BOUNDED-COMPLEXITY-KÖNIG】witness 複雑性の一様上界 ⟹ 単一普遍 witness(König の別軸使用)

- **種別**: 予想+装置提案 / **規模**: 中間峰級 / **出所**: König/compactness の使い方の別形(発注の指定方向)
- **一行機構**: 閉済前提 4 の compactness は **fibre の元**の枝分かれに使う。別軸として、各段の witness 集合 W_j を「correction index ≤ c₀・word 長 ≤ ℓ₀ の有限 schema 集合 S(c₀,ℓ₀)」の部分集合と見る。全段 W_j ≠ ∅ かつ複雑性一様上界が立てば、有限集合 S 上の減少列 ⋂_{j≤n} W_j の非空性(König/鳩の巣)から**単一 schema が全段を通る**。SINGLE(x) の証明を「複雑性の一様上界」という**測れる量**に交換する。
- **効くと思う理由**: A-4(schema 一定)より弱い仮定で同じ結論に届く: schema が段ごとに変わってもよく、「複雑性が伸びない」ことだけ要る。現物の witness が最小格(index 1)であることは上界仮説の初期証拠。
- **検証の一手目**: 既走 run の witness 複雑性統計の抽出(ops 級)+ A-4 の 1 run で index の増減を観測。増加傾向が無ければ「上界 c₀ の事前登録つき」で鎖 replay 走行を設計(装置提案: 停止規則 = index が c₀ を超えた段で STOP し、その段を T-33 設問 4 の obstruction 候補として提出)。
- **in-house grep**: König = `157ak_path_roof_count_konig_audit`(path/roof counting の監査・用途別)・Mittag-Leffler = `157cq`・cofinality_ledger(COMPACT 以外の B 側経路 1)。複雑性有界性を compactness の軸にした使用は grep 範囲で無し。
- **破綻しそうな点**: 上界が段とともに(たとえ対数的にでも)伸びるなら枝が無限化して失敗。また「schema の同一性」の定義(語の正規形)が段の群に依存すると S(c₀,ℓ₀) が固定有限集合にならない — 正規形の段独立な定義が先に要る(T-29 閉 4.2 の canonical representative 契約が流用候補)。

## 【A-6 DYNAMIC-INTERSECT】isolated 窓の枚挙+交叉吸収による動的鎖(A-1 の isolated 性が破れた場合の保険)

- **種別**: 構成(動的選択原理)/ **規模**: 中間峰級 / **出所**: 計算論の priority/dovetail 論法からの翻訳
- **一行機構**: isolated 窓は各指数ごと有限・全体で可算なので枚挙 L_1, L_2, … を固定し、鎖を K'_0=K_*、K'_{n+1}=K'_n ∩ L_{n+1} と**動的に**育てる。C={K'_n} は構成から cofinal な鎖。各吸収一手 K'_n → K'_{n+1} は相対有限 jump(相対核 K'_n/(K'_n∩L_{n+1}) ≅ K'_nL_{n+1}/L_{n+1})で、A-3 の三色塗りがそのまま適用される。「反例窓が現れたら曲げて回避」ではなく「**現れた窓を次の一手で必ず食う**」— 回避しない動的原理。
- **効くと思う理由**: gentle 側の失敗(151 §4.3)は「族を**先に**固定したら別方向の窓に入れなかった」こと。吸収順を後決めにすれば cofinality は構成で自明になり、数学的債務が「吸収一手 = 相対 jump の typed 吸収」一種類に均される。A-2 と組むと、吸収一手は「毎回勝つ」必要すらなく「無限回勝つ」でよい。
- **検証の一手目**: 数学者へ: 「isolated 窓の交叉は isolated(gentle Prop 3.15 類似)が full B₄ で立つか」+ implementer へ: 最初の非自明吸収一手(K_* と既知の別方向 isolated 窓一つの交叉)の相対 jump chief 分解を GAP で出す(三色の実測初例)。
- **in-house grep**: dovetail = `sol_reply_148`(A 側 dovetail 設計・列挙エンジン)— あちらは**空 fibre 探索**(A 証明書狙い)の dovetail で、本札は**吸収鎖構成**(B 側)の dovetail。同じ枚挙装置が両用になる点は資産の再利用。交叉 no-shortcut の警告 = `MONO-CNF-139`/`NO-FINITE-B-140`(151 §4.3 の引用)— 本札は「交叉の像が自動で 972」とは言わず、吸収一手ごとに typed 吸収を要求する側なので no-shortcut と整合。
- **破綻しそうな点**: 吸収一手の typed 吸収が(α)(β)(γ) のどれでも失敗し得るのは A-3 と同じ — 本札は債務を消さず「債務の形を一種類に均す」だけ。また枚挙の可算性・各指数有限性は full B₄ の isolated の定義に依存(未確認なら数学者設問に追加)。

## 【A-7 ADVERSARIAL-STAGE】反例側: direct scan が全滅する段を探しに行く

- **種別**: 反例狙い / **規模**: 現在線級 / **出所**: T-33 設問 4 の逆用
- **一行機構**: 157da 型 manifest を relative 次段・次々段で走らせ、direct scan が witness 0 で**全滅する段**を探す。見つかれば T-33 設問 4 の「B4-B を止める最小の actual typed obstruction」の実物(群・作用・coface・correction domain・comparison map が manifest に全部入っている)。
- **効くと思う理由**: STEP/SINGLE を証明する努力と同じ計算が反証装置を兼ねる(1 run で両睨み)。gentle 側には run 32106551371(登録宇宙の exact 全滅)という「選択 fibre の全滅」前例があり、これを「段の全滅」まで強めたものが A-witness の形。
- **検証の一手目**: A-4 の 1 run と同一(解釈だけが双対)。全滅した場合は scan 宇宙の完全性宣言(その段の correction fibre を尽くしたか)を checker 側に要求してから obstruction 札に昇格。
- **in-house grep**: 前例 = T-29 §5(run 32106551371 の「有限 slice 全滅 ≠ B4-A」の教訓)・手戻り防止ルール 5。
- **破綻しそうな点**: T-29 §5 の罠そのまま — 有限 slice の全滅を段の全滅と読み違えると過大格付け。全滅時の宇宙完全性証明は typed horn(T-31 §4 の 5 条件)込みで重い。

---

# 標的 B — 非可換 chief factor S^t で A5/V4 型反模型を排除する braid/GT 固有条件(6 札)

## 【B-1 ARITH-STAB】閉済前提 1 が abstract kernel の安定子に A を無料で入れる — S^t 段は all-or-nothing の決定手続きになる

- **種別**: 構成(観察)/ **規模**: 現在線級(標的 B の枠組み札)/ **出所**: 閉済前提 1 と Wells 理論の突合
- **一行機構**: centerless N=S^t では abstract kernel ω: G_K → Out(S^t) が拡大を(存在すれば)一意に決める(H²(G,Z(N))=0・realizability 障害 H³(G,Z(N))=0)。candidate z の lift 可否は「z が [ω] を保つか」に集中する。ここで**閉済前提 1(A ≤ I_K が全段)**により、A 由来の candidates は [ω] を保つ側に常にいる。[X:A]=3 素数ゆえ、[ω] の candidate 軌道は 1 か 3 の二択で、**軌道 1 ⟹ 全 outside が lift(段が閉じる)/ 軌道 3 ⟹ 全 outside が lift 不能(F_{K'}(x)=∅ = isolated 段の空 fibre = A 側証明書の形)**。中間が無い。⟹ S^t 段は「open のまま残る」ことができず、軌道サイズという**一個の有限量の計算が決定手続き**になる。
- **効くと思う理由**: A5/V4 反模型(T-31 §3)は stabilizer=C2=A の「軌道 3」側の実例として作られている。実系がどちら側かは未知だが、**どちらに転んでも前進**(閉じる or A-witness)という構図は、set_surgery_vetting §4.2 の「どちらに転んでも結論」型の再現で、探索の停止性を保証する。
- **検証の一手目**: falsifier へ判読依頼: 「A5/V4 反模型は閉済前提 1 の類似(全段 lift する arithmetic 部分群)を持つか」。持つなら反模型は二分論法と整合(= 二分は反模型を**排除しない**枠組みであり、排除には B-2〜B-5 の braid 固有根拠が要る)— この位置づけの確認が先。並行して数学者へ: shadow candidates は群自己同型でない(substitution/groupoid 射)ため「[ω] への作用」の typed 定式化を 1 頁で固定する設問。
- **in-house grep**: Wells = 対話帳 T-31/T-33・`157w_fixed_obstruction_class`・`152_typed_lifting_literature_v1`・`152_b4_absorption_literature_v1`(文献面は Luna が既走査)。abstract kernel = `sol_reply_148 §1.1`(relative-extension engine の列挙キー)・`157bn`・`157ba`。「閉済前提 1 ⟹ 安定子 ⊇ A ⟹ 素指数二分」の配置は grep 範囲で無し。
- **破綻しそうな点**: 「lift 可否 ⟺ [ω] 保存」は Wells の自己同型設定の話で、typed shadow 系では必要条件どまりかもしれない(hexagon/settlement の追加 gate で「[ω] を保つのに lift できない」余地)。その場合二分は「軌道 3 ⟹ 空」だけが生き、「軌道 1 ⟹ 閉」が落ちる — 半分でも決定力はある(A-witness 検出器として)。

## 【B-2 FIRST-SIMPLE-FIXTURE】実系の最初の非可換 chief は PSL(2,8)・Out=C3 — [X:A]=3 と正確に共鳴する「最危険の最初の実例」を既設装置で実測する

- **種別**: 構成+実測提案 / **規模**: 現在線級 / **出所**: 窓台帳の観察(Q_0 = G_9 × PSL(2,8))
- **一行機構**: gentle 側窓台帳で実際に現れている最初の単純 chief は PSL(2,8)(|·|=504)。**Out(PSL(2,8)) = C3(体自己同型)**であり、外側指数 [X:A]=3 と位数が一致 — 「係数が 3 と互いに素だから自動消滅」(B-4)が**使えない最初の実例**。A5/V4(Out=C2)より危険な型が、仮想でなく既設の cross-checked 装置(Phase 2b の E-窓: 1→C2^6→E→PSL(2,8)→1)の隣にある。972 類の candidates が P-因子に誘導する Out(PSL(2,8))-像を全類について表にする。
- **効くと思う理由**: 反模型の排除は「実系の最初の危険例で δ(捻り)が実際に消えている」ことの実測から始めるのが最短。全 972 survival(Phase 2b cross-checked)は「lift が存在した」ことを既に含むので、**測るのは『なぜ存在したか』の機構分解**(Out-像が自明だったのか、補正で補償されたのか)— これが B-4/B-5 の条件式の較正データになる。
- **検証の一手目**: implementer + GAP: 既存 Phase 2b 窓の producer 出力から、各 shadow の P-因子誘導自己同型を Out(PSL(2,8))=C3 に落とす後処理(新規探索なし・再集計)。A-類と outside 類で Out-像に差があるかの一表。
- **in-house grep**: 非可換測定の既在 = 便 134(非可換**核**・位数 2048 = 2-群)・便 138(PerfectGroup 504·2^7・相対核は C2^7 可換)— **chief S=PSL(2,8) 自体の Out-捻り測定は無し**(cofinality_ledger §3「非可換核: 族定理無し」)。PSL(2,8) の構造使用 = 150 便 §1.1(Z(P)=1・V^P=0)・151 便 §3.4(perfectness・multiplier 1)— Out=C3 の使用は grep 範囲で見当たらず。
- **破綻しそうな点**: **gentle/B₃ 側の fixture であり T-33 の full B₄ とは別系**(冒頭警告)— 機構の較正としてのみ有効で、B₄ の S^t 段への転写は transport/coface 込みで別途。また Phase 2b の survival は窓一枚の話で、chief「段」(K'≤K の相対)の設定に組み替える際に相対化の型ずれが出うる。

## 【B-3 HORN-CONNECT】K(5) horn の効く形を「fibre groupoid の π₀ に C_adm+ambient braid 共役が推移的に作用する」ことに求める

- **種別**: 予想 / **規模**: 中間峰級 / **出所**: T-31 §4 の欠落条件リスト (2)(3) への直接応答
- **⚠ 禁止短路④に隣接**: K(5) contractibility「だけ」による effectivity は禁止済。本札は contractibility を使わず、T-31 §4 が「必要」と明示した追加条件(horn 上 section・edge transport の全単射性)を**どの literal data が供給するか**に答える形 — 短路の再提案ではない。
- **一行機構**: A5/V4 反模型で K(5) 全平坦でも lift が無いのは、fibre groupoid の π₀(三つの E_α 成分)を transport=identity の人工設定が分断したまま X が推移的に動かすから(T-31 §4)。実系の transport は Fox/prefix conjugation を含み(T-30 §3)、さらに correction domain C_adm と ambient B_r-共役(strand relabelling・chief 成分の置換)が fibre に作用する。**この作用が π₀ 上推移的**なら、成分の分断が消え、one-outside と組んで存在が強制される — 「braid 固有の条件」の候補を「π₀ 推移性」という検証可能な一命題に固定する。
- **効くと思う理由**: 反模型は「transport 全部 identity・補正なし」という**補正貧困の極限**で作られている。実系は逆に補正の供給源(C_adm・二 hexagon 帰着後の word correction・ambient 共役)が多層にあり、q=3 typed positive で現に correction_index=1 の補正が defect を消した実績がある — 同じ供給源が π₀ を潰す側にも効くという類推。
- **検証の一手目**: 数学者へ小問: 「A5/V4 反模型に kernel correction の許容域(C_adm 類似)を最大に入れると π₀ 推移性は回復するか」— YES なら反模型の本質は補正貧困であり、実系の C_adm の下限を測る問題に変わる。NO なら本札は降格(π₀ は補正で潰れない型の障害)。
- **in-house grep**: horn/filler = T-31 §4・T-32(relative horn の retained face 条件)・`157cr`(strict kernel の zero-action no-go)。π₀ 推移性という条件名は grep 範囲で無し(T-31 §4 の (2)(3) の言い換え+供給源の指名が差分)。
- **破綻しそうな点**: B₄ の C_adm は hexagon・marking・charming・onto・settlement で削られており(T-30 §4.3)、π₀ を潰すには痩せすぎている可能性。また ambient 共役は shadow の typed data と可換に効くか(coset 作用との整合 = T-30 §4.4 の注意)が未検。

## 【B-4 δ-VANISH + 危険型リスト】coprime 消滅で「3 が Out(S^t) に触れない型」を一括排除し、残る危険型を有限リスト化する

- **種別**: 予想+縮小路 / **規模**: 現在線級 / **出所**: 可換側 transfer(157z)の非可換係数版への外挿
- **⚠ 禁止短路⑤に隣接**: centerless/Schreier「だけ」による存在主張は禁止済。本札は centerless Wells に **coprime 条件を追加**する形(使うのは Out の可解性=Schreier ではなく**位数の互いに素性**)— 短路の再提案ではない。
- **一行機構**: B-1 の捻り δ は「位数 3 の外側方向 → [ω] の捻り群 T(Out(S)^t ⋊ Sym(t) の部分商)」に値を取る 1-cocycle 型のデータ。**3 ∤ |T| なら**、coprime H¹ 消滅(Schur–Zassenhaus/Glauberman 型・complement 共役は非可換係数でも有効)で δ の消滅が自動になり、compatible pair が存在 → centerless Wells の一意性で段が閉じる。危険が残るのは **3 | |Out(S)|(field-3 型: PSL(2,2^{3k}) など・diagonal-3 型: PSL₃/PSU₃・triality: D₄)または 3 | t(成分置換 Sym(t) の 3-part)**のみ — 排除定理の標的が有限リストに縮む。
- **効くと思う理由**: A5/V4 反模型は Out(A5)=C2 なのに落ちる — が、あの反模型の acting 群は Q=C2²(2-群)で、**外側方向の位数(2)と Out の位数(2)が共鳴していた**。実系の外側方向は位数 3 型なので、共鳴条件が「3 が T に触れるか」に移る。可換側では同じ切り分け(p≠3 無料・p=3 のみ荷重)が T-29 §6 で既に立っており、その非可換版という素直な外挿。
- **検証の一手目**: 数学者が 1 頁起草: 「δ の typed 定義(A 非正規の場合は X→Sym(X/A)=S₃ 経由で定式化)+ 3 ∤ |T| ⟹ compatible pair 存在」。反証側は falsifier: 反模型の位数を付け替えた「A5/V9 型」(acting C3²・Out に C3)で同じ穴が開くかを紙で確認 — 開くなら危険型リストの必然性が裏書きされる。
- **in-house grep**: coprime = `157z_index3_transfer`(可換)・`157cp`・q3 checker 内 coprime 検査・`152_b4_chief_absorption_v3`。非可換係数の coprime H¹(complement 共役)を Out(S^t) に使った札は grep 範囲で無し。
- **破綻しそうな点**: (i) 危険型 — まさに B-2 の PSL(2,8) — には無力で、そこは B-2/B-5 が受け持つ(本札単独では標的 B を閉じない)。(ii) A 非正規のとき「1-cocycle」の定式化自体が非自明で、S₃ 経由の書き換えで係数が変わる可能性。(iii) t の 3-倍数型で Sym(t)-part の捻りが braid の strand 構造で自動固定される(= 危険でない)可能性もあり、リストは過大かもしれない — 過大側に倒れるのは安全。

## 【B-5 BURAU-FROB】Burau specialization が Out(PSL(2,8)) を実現し、δ の消滅が u-residue の合同条件に落ちる可能性

- **種別**: 予想 / **規模**: 中間峰級(braid 固有条件の最有力候補)/ **出所**: 構造からの類推(Burau parameter の Galois 捻りと体自己同型の同一視)
- **一行機構**: reduced Burau の有限体 specialization t ↦ ζ(ζ ∈ F₈^×・位数 7)は PSL(2,8) 型 chief の linear 実現を与える。shadow の σ ↦ (共役)·σ^u 置換は parameter 側の **t ↦ t^u 捻り**として作用し、Frobenius t ↦ t² が **Out(PSL(2,8)) = C3 をちょうど実現**する(specialization の三つ組 ζ, ζ², ζ⁴ は Frobenius 軌道 — A5/V4 反模型の「三つの α が S₃ で回される」構図の**実系における対応物**)。すると δ の消滅 ⟺ 「u mod 7 が ⟨2⟩={1,2,4} ⊂ (Z/7)^× に入る(= 捻りが Frobenius で補償可能)」という**合同条件**に落ちる可能性がある — braid 生成元の像の位数制約が S^t への作用を制限する、という設問方向の literal 実装。
- **効くと思う理由**: (i) B₄ Burau は忠実(2607.05283・157br/157p で in-house 監査済)なので specialization は群を「よく見る」。(ii) 反模型と実系の差が「軌道を回す群が抽象 S₃ か、それとも算術で位数制約された u-捻りか」に局在し、後者なら合同条件で排除が書ける — 「braid/GT typed 系固有の条件は何か」への最も具体的な回答候補。
- **検証の一手目**: implementer + GAP(1 時間級): reduced Burau mod 2 の t ↦ ζ specialization で PB₃(/PB₄)像が PSL(2,8)(型の群)を生成するか + u-捻り(u は形式変数・residue 類ごと)が誘導する自己同型の Out-像を表にする。B-2 の実測表と突合し、「Out-像 = u mod 7 の関数」という予言が合うかを見る。
- **in-house grep**: Burau = `d972_b4_burau_matrix_v1`・burau_joint_accel 系(157cd/157cg)・`157p`(文献監査: Burau congruence 定理は無し、と負判定済 — 本札は congruence 定理を要求せず specialization 一発でよいので 157p の負判定と両立)・`157br`(忠実性)。specialization を Out-実現として使う札は grep 範囲で無し。
- **破綻しそうな点**: (i) Burau specialization 像と該当窓の chief が**同一の実現**である保証が無い(同名別物リスク — CV-9 型の判読が要る)。(ii) u mod 7 と窓の m-法(18/36)は互いに素な法で、X∖A の類から u mod 7 が決まらない(well-defined でない)可能性が高い — その場合「合同条件」は空振りし、7 を含む法の深い段でのみ意味を持つ形に修正が要る。(iii) ⚠ MB whitelist: u の**値**・平方類の計算はしない — 本札の検証は residue **類の集合演算**に限定して設計すること(封印量に近づく計算設計になったら停止して司令塔へ)。

## 【B-6 DESSIN-SUPPLY】副線 2106.06645 の dessins 作用を「S^t 段の lift の存在供給源」として翻訳する

- **種別**: 別分野(副線)からの翻訳 / **規模**: 中間峰級 / **出所**: 副線論文(入手済・正典内)の作用定理からの類推
- **一行機構**: 2106.06645 の GT-shadow の dessins への作用は full B₄ 系(pentagon あり・T-33 と同系)で定義される。S^t chief 窓を monodromy 群 S の dessin/被覆族で実現できれば、「lift の存在」は「dessin 作用の点の存在」に**外注**される(作用は全 shadow に定義されるので存在が自動)— Wells 存在問題が「その dessin 実現が tower reduction と可換か」という naturality 一点に置き換わる。
- **効くと思う理由**: A5/V4 反模型は抽象拡大の圏で組まれており、dessin 側の実現を持たない。実系の S^t 窓が常に dessin 実現を持つなら、それ自体が「反模型が実系に埋め込めない」ことの braid/GT 固有の理由になる(排除の第三の型: 障害消滅でも π₀ 推移でもなく**実現の存在**)。
- **検証の一手目**: reader へ: 2106.06645 から「作用の naturality(reduction との可換図)」「作用が定義される shadow の範囲(全体か subgroupoid か)」を §番号つきで抽出(既入手論文・文献ゲート内)。
- **in-house grep**: dessin = 地図・triad972_canonical_addendum・ideas_set_surgery ほか多数 — いずれも背景記述で、「非可換 chief の lift 供給源」としての使用は grep 範囲で無し。
- **破綻しそうな点**: (i) 2106 の作用が特定 subgroupoid 限定なら外注が成立しない。(ii) 〔**訂正 2026-08-18**: 当初ここに「2008.00066 未入手」と書いたが**誤り** — 収蔵済(裁定 596)。型合わせは収蔵版で実施可能であり、文献要請は不要〕。(iii) monodromy S の族が tower の深い段まで届くか(有限個の dessin で cofinal 深度を覆えるか)は全く未知。

---

## 末尾整理 — 二標的の接続と最短経路(発案係の見立て・candidate)

1. **標的 A の最短経路**: A-2(観察・3 行)→ A-1 の isolated 設問(数学者)→ A-4 の 1 run(replay)。この 3 手で「SINGLE(x) = 鎖上の q=3 replay 列 + 非可換段」まで縮む見込み。q≠3 の無料化(A-3)は Sol への限定質問 1 本で白黒がつく。
2. **標的 B の最短経路**: B-1 の枠組み確認(falsifier)→ B-2 の再集計(既設装置)→ B-4 の 1 頁起草。B-5 は B-2 の表と突合できた時だけ昇格。
3. **両標的の合流点**: A-3 の色 (γ) = 標的 B。B-1 の二分により、(γ) 段は「open のまま塩漬け」にならず、計算 1 個ごとに閉 or A-witness へ落ちる — B4-B 戦役全体の停止性がここで担保される、というのが本 deck の中心主張(candidate)。

⚠ 全札 candidate。採否は司令塔の専権。検証・起草の宛先(数学者/falsifier/implementer/reader/Sol)は提案であり、振り分けも司令塔の専権。

---

## Erratum(2026-08-18・司令塔指摘)

- B-6 破綻点 (ii) の「2008.00066 未入手」は**誤記**(在庫 4 点検査を怠った)。正: **収蔵済(裁定 596)**。本文は同日訂正済。
- 後日注: 本 deck の B-1(Wells 枠)は数学者 T33-L8(対話帳 T-36)により**一般形で死亡**(圏違い・条件つき保持は t33_answer_draft §4.7)。B-2 の PSL(2,8)/Out=C3 見立ては T35-R1 の前件として採用され FC-4 に昇格。非可換 chief の新 deck は `docs/notes/nonabelian_ideas_v1.md`。
