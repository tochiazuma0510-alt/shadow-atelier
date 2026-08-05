# HS 本走(NW(7) 悉皆 705,894 対)— 事前登録票 v2

- 起草: 実装担当(短命)・2026-08-05
- 委嘱: 司令塔(「HS 本走 prereg v2 + 実行 bundle の実物作成」— `sol/sol_reply_104_math31.md`(便104監査返書・数学便第31号)F104-1.2/1.3/1.5 の是正。**走らない — 705,894 宇宙の候補評価はゼロ**)
- **v1(`docs/notes/hsp7_mainrun_prereg_v1.md`)・付録C v1/v2 は不改変**。本票は v1 の宇宙定義(§1)・判定述語(§2)・停止規則の骨格(§3)を継承し、便104 が名指しした欠陥のみを修理する。数値の再測定はしていない(既存 cert/log からの転記+新規の構造検査のみ)。
- 正本参照: `sol/sol_reply_104_math31.md` §1(F104-1.1〜1.5)・`docs/notes/hs_prop7_translation_v1_addendum_nwp8_v1.md`(NW-P8 撤回・S-8′ 正本)・`docs/notes/hsp7_mainrun_prereg_v1.md`・`docs/notes/hsp7_mainrun_prereg_v1_appendixC_draft.md`(v1・実測値)・`docs/notes/hsp7_mainrun_prereg_v1_appendixC_v2.md`(v2・Actions設計)
- **本票も走行・列挙は一切行っていない**。実行 bundle(§5)は構文/dry構造検査のみで、705,894 候補宇宙のいずれも評価していない(空 shard での GAP 実行確認、後述)。

---

## 0. 便104 の裁定(受理事項の確認)

便104 F104-1.2 は「本走 705,894 対」を**不認可**とし、以下を re-application 要件 (a)〜(h) として明示した(逐語、F104-1.4 末尾):

> 再申請には、(a) S-8′ と空欄を直した prereg v2、(b) predicate library / enumeration wrapper / lane wrapper / join checker の実物と digest、(c) semantic candidate-key bijection、(d) 256 制約内の workflow 分割、(e) timeout/UNKNOWN 契約、(f) artifact 容量実測、(g) 既知 fixture の GHA receipt、(h) join mutant 全 PASS、が必要である。これらの preflight が将来通っても**自動で本走へ連鎖発火せず**、短い再 gate を通すこと。

本票は (a)(b)(c)(d)(e)(h) に対応する。(f) artifact 容量実測(GHA上でのbytes/candidate計測)と (g) 既知 fixture の GHA receipt は**GitHub Actions上での実行を要する**ため、本票(dry・ローカル)の範囲外であり、未着手として正直に開示する(§8)。

---

## 1. ★★ S-8′ の向き訂正(最優先・逐語修理)

### 1.1 誤り(v1)

`docs/notes/hsp7_mainrun_prereg_v1.md` §3 の停止規則表:

```jsonc
"S-8'":  { "trigger": "NW-P8 の完全形(全 X_N x 全 705,894 候補)で N と N0 の判定不一致が0件",
           "verdict": "CALIBRATION_FAILED / INTEGRITY_STOP", ... }
```

これは撤回済みの旧 NW-P8/S-8 の向き(「不一致 0 件 → 失敗」)をそのまま完全形へ拡大したものであり、正本 `docs/notes/hs_prop7_translation_v1_addendum_nwp8_v1.md` §3 の S-8′ 定義と**逆向き**である。便104 F104-1.2 逐語:

> 最大の blocker は ... prereg v1 §3 の S-8′ である。同 prereg は「N と N0 の判定不一致が 0 件なら CALIBRATION_FAILED / STOP」と書く。しかし effective source ... の S-8′ は**不一致が 1 件でもあれば** IMPLEMENTATION_BUG_SUSPECTED / STOP である。

理由(仲裁済み・NW-P8 追補 §2 逐語): $N\cap F_2=N_0\cap F_2=\mathcal V(F_2)$ なので、Prop. 3.4 により charming 候補の full hexagon 判定は N と N₀ で**恒等に一致する**。ゆえに一致は定理の帰結であり、**不一致は実装バグの証拠**である。

### 1.2 正(v2、以後この形を停止規則の唯一の正本とする)

```jsonc
"S-8'":  { "trigger": "登録 candidate key 全 705,894 件のうち、N と N0 の判定が1件でも食い違う",
           "verdict": "IMPLEMENTATION_BUG_SUSPECTED / STOP",
           "note": "N∩F2=N0∩F2=V(F2)(仲裁確定)とProp.3.4により、full hexagon判定はNとN0で恒等一致するのが定理の帰結。不一致は実装バグの検出器であり、『不一致0件』側を失敗条件にしてはならない(hs_prop7_translation_v1_addendum_nwp8_v1.md §3 正本)。" }
```

**これは撤回済みの NW-P8/S-8 の向きへ戻す修正であり、新規則の追加ではない。** v1 が誤ってこの逆向きを継承していたことが便104発送不可の直接原因だった。

---

## 2. scope 二重計数の訂正

v1 §3 の S-8′ トリガ文言「全 $\mathcal X_N$ × 全 705,894 候補」は、705,894 自体が既に $6\times117,649$(= $|\mathcal X_N|\times|[P,P]|$)の総数であるため二重計数だった(便104 F104-1.2 item 1)。

**正**: 「登録 candidate key 全 705,894 件」(上記 §1.2 の trigger 文言に反映済み)。他の停止規則(S-7′/S-9/S-3)の記述にも同種の二重計数がないか確認した — S-9(「同一窓上で Lane S と Lane V の項目別判定(705,894件のいずれか1件)」)・S-7′(機械再計数)は元々単一の705,894参照のみで二重計数はない。修理対象は S-8′ のみ。

---

## 3. timeout/UNKNOWN 具体値(付録 C v1/v2 実測からの転記)

v1 付録 C(空欄)は発送不可条件そのものだった(v1 自身が「この空欄が埋まっていない状態では便104は発送できない」と明記)。付録C v1(実測+外挿)・付録C v2(Actions設計)から次を確定する(**本票は再測定していない**、既存の実測+外挿値をそのまま転記):

```jsonc
"timeout_and_unknown_budget": {
  "per_candidate_timeout": "30秒(第一候補。付録C v1 §6: pessimistic単一候補コスト2.9364秒/候補に対し約20倍の安全マージン。500秒/shard運用上限に対しshard内timeout最大16-17件までは shard 全体を破綻させない設計)。代替案60秒も付録C v1に両論併記。",
  "unknown_recording": "UNKNOWNはPASS/FAILと同格の三値の一つとして705,894件の分布表に記録する(棄却・再試行での握りつぶし禁止)。理由(timeout/pc群評価失敗/代表元取り直し要)を候補ごとに併記(lanespec R-13、v1 §3 継承・変更なし)。",
  "unknown_rate_gate": {
    "early_warning_soft": "累積UNKNOWN率が0.1%(約706件)を超えた時点で実行は継続し司令塔へ中間報告(較正走18件でUNKNOWN0件だった前提が本走規模で崩れている兆候として注視、付録C v1 §5)",
    "operational_stop_hard": "累積UNKNOWN率が1.0%(約7,059件)を超えた時点で計算資源の問題として一旦停止・司令塔へ報告(数学的停止規則ではなく運用停止、lanespec既定どおり)",
    "caveat": "この0.1%/1.0%は較正走0/18という事実からの保守的な運用トリップワイヤであり、統計的推定量ではない(付録C v1 §5 明記のとおり、この性格を弱めずに転記する)"
  }
}
```

---

## 4. frozen digest の分離(predicate library vs 新規 wrapper)

便104 F104-1.2 item 3: 「較正走 driver と byte-identical」と「13件loop→705,894件・shard入力へ変える」は同時に満たせない。**判定 predicate/library の digest 不変**と、**新しい列挙wrapper/shard wrapper/join checkerの個別digest pin**を分離する。

### 4.1 predicate library(較正走と byte-identical)

| レーン | predicate library ファイル | 較正走ソース(byte-identical 対象範囲) | 較正走ソース SHA-256(全体) | predicate library SHA-256(全体) | byte-identity 確認方法 |
|---|---|---|---|---|---|
| S | `search/probe/hsp7_mainrun/predicate_lib_laneS.g` | `search/probe/hsp7_cond4_laneS/driver_step3_eval_candidates.g` 1-69行(全文) | `f644f7fcd0a5e79ed805e458bc1045c25b3abafe627ed533bf122fb798b7aa47` | `1fabb7848ea5c6adb275b451c5264f8c4f7989fbc2b94f1e95db2b663453a070` | `sed -n '1,69p'` で両ファイルの対応範囲を抽出し `diff` — exit 0(差分ゼロ)を機械確認済み(実装担当・2026-08-05) |
| P | `search/probe/hsp7_mainrun/predicate_lib_laneP.g` | `search/probe/hsp7_cond4_laneP/driver_step3_eval_pent.g` 1-117行(NW-P6/P8の印字ループ+QUIT を除く全構築+PENT定義) | `9f5ba7300c071c539800a9fae1f06c440316ec458acb72bfe40308fd6db16235` | `be1fdf4883210118211f5ab26dc8e1c22a2aacd96f58e24e494779ca3fc70dcc` | 同上、`sed -n '1,117p'` diff exit 0 確認済み |
| V | `search/probe/hsp7_mainrun/predicate_lib_laneV.g` | `search/probe/hsp7_cond4_laneV/statemachine_lib.g`(全文、Read()するのみでコピーしない — 真の意味での byte-identical 再利用) | `30ea5224eec536aa995443471930c7874ebd57e61a3e2a3c6982ad5c2e5edf47`(statemachine_lib.g 自体の SHA-256。predicate_lib_laneV.g 自身の SHA-256は`0522fab0f9c928c47142b8a74420ed3783dba827a5b1d567250c2c0af1b7e029`だが、これは薄いラッパーであり、拘束対象は statemachine_lib.g の方) | — | Read() による直接参照のため diff 不要(コピーが存在しない) |

**注**: S/P は元の calibration driver がモノリシック(群構築+判定関数+印字ループ+QUITが1ファイル)だったため、判定関数部分のみを**逐語抽出**(コピー、バイト同一性を diff で機械確認)して separate library 化した。V は元々 statemachine_lib.g が別ファイル化されていたため、コピーせず同一ファイルを Read() する形にした(コピーのリスクそのものを排除)。

### 4.2 新規 wrapper(個別 digest pin、較正走との byte-identity は要求しない)

| ファイル | 役割 | SHA-256 |
|---|---|---|
| `search/probe/hsp7_mainrun/candidate_key_lib.g` | candidate key 意味論(pcgs・exponent vector・endian・全単射) | `8cab243c121c00d8b6629fb0a5b886a59d3a02bca18d793bf38cdf9057f445bf` |
| `search/probe/hsp7_mainrun/lane_wrapper_S.g` | Lane S shard 入力ループ | `afa4956e567c681f7943b124d59f665dea4bfaeaca214f8c34ec0cc805a33d31` |
| `search/probe/hsp7_mainrun/lane_wrapper_P.g` | Lane P shard 入力ループ(f-index軸、最適化採択済み §6) | `166e3a9a962908954a6e893f5e4b9a50521bc8d4932c2b1714751a01c1d8b51b` |
| `search/probe/hsp7_mainrun/lane_wrapper_V.g` | Lane V shard 入力ループ | `8396e3cb7be760c8c1b69f2cb321e32e6644bfc2f2d66a844603ea7b819f86e3` |
| `search/probe/hsp7_mainrun/shard_manifest_gen.py` | shard manifest 生成器(純粋算術、GAP非依存) | `2fdc4cbb67274a478f9251925441a838af0432d239ecf4bf5fce6a21aacbb1e3` |
| `search/probe/hsp7_mainrun/join_checker.py` | join checker(独立実装、cert JSON のみ入力) | `657aeea8c7069e41769a36f846233dddcde5288bf40e0206d4cc67223ceb06e3` |
| `search/probe/hsp7_mainrun/join_fixtures_gen.py` | join mutant fixture 生成器 | `fd7def8389c31c513ef50432d4ce82e7ee573e722605e0cc6ddcda0a4661ab6f` |
| `search/probe/hsp7_mainrun/join_fixtures_run.py` | join mutant 全件実行+期待verdict照合 | `27248add97ff91fc905bc5e66d432f05bd194476c800a48217146c2950b83e02` |

**規律**: 本走発注前に、上表左列(predicate library)は較正走ソースとの diff = exit 0 を毎回機械再確認し、右列(新規wrapper)は「今回発注する版のSHA-256」を発注 cert の `frozen_driver_digests` に記録する。両者を同じ意味で「digest 不変」と呼ばない(便104 item 3 の是正)。

---

## 5. candidate key の意味論(便104 F104-1.2 item 4 是正)

v1 は「$[P,P]$ の index 0..117648」に意味論がなかった(GAP の `Elements()`/BFS 順序を暗黙に使うリスク)。v2 は次を固定する(`search/probe/hsp7_mainrun/candidate_key_lib.g` に実装、dry構造検査で機械確認済み — 後述 §7)。

- **固定 pcgs**: $D:=[P,P]$ の `Pcgs(D)` を基底とする(実測: $P$ を `search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g` から構築 → $|P|=5{,}764{,}801=7^8$、$|D|=117{,}649=7^6$、`Pcgs(D)` は正確に6生成子、`RelativeOrders`は全て$[7,7,7,7,7,7]$。scratchpad/dry_check_pcgs.g→`search/probe/hsp7_mainrun/dry_check_pcgs.g` で機械確認、gap.ps1 実行ログに記録)。
- **exponent vector**: $(e_1,\ldots,e_6)\in\{0,\ldots,6\}^6$。pcgs の relative order が全て7なので、任意の $D$ の元は一意に $g_1^{e_1}\cdots g_6^{e_6}$(この左から右への積順)で表される — これは pcgs 正規形であり、`Elements()`/BFS順序ではない。
- **endian**: $e_1$ が**最上位桁**(pcgs の第1生成子の指数、base-7 flat index の最上位桁)、$e_6$ が最下位桁。$f\text{-index} := (((( e_1\cdot 7+e_2)\cdot 7+e_3)\cdot 7+e_4)\cdot7+e_5)\cdot7+e_6 \in [0,117648]$(標準の big-endian 位取り記数法)。
- **candidate key** $:= (m, e_1,\ldots,e_6)$。$m\in\mathcal X_N=\{0,1,2,4,5,6\}$(実測: `Filtered([0..6], m->Gcd(2m+1,7)=1)`、既存 cert と一致)を昇順に並べた `m_index`(0..5)を用い、**pair flat index** $:= m\_index \times 117649 + f\text{-index} \in [0,705893]$。shard manifest(§6)はこの pair flat index を分割単位とし、GAP 内部順序を分割単位にしない。

---

## 6. 高速化の採択実装方針(Sol 共同設計、便104 F104-1.5)

### 6.1 採択: Lane P の f̄-only 評価 + exact join

PENT_W の式 $\bar\rho^4(\bar f)\bar\rho^3(\bar f)\bar\rho^2(\bar f)\bar\rho(\bar f)\bar f=1$ は $m$ を含まない(Sol 便104 F104-1.5 の指摘)。よって Lane P は 705,894 対でなく**117,649 個の $\bar f$ のみ評価**し、結果を6つの $m$-key へ exact join する(評価回数が係数6で減る)。

- **実装**: `lane_wrapper_P.g` は f-index 軸(0..117648)を shard 単位とする(pair index 軸ではない — Lane S/V との shard 軸の違いを明記)。
- **join receipt**: `f_key -> six candidate_keys` の全単射を `candidate_key_lib.g` の `FIndexToSixPairIndices(fIndex)` で機械生成する。$f$-index=$i$ の6つの pair index は $\{i + m\_index\times117649 : m\_index\in 0..5\}$。境界値($i=0$、$i=117648$)の自己テストを `lane_wrapper_P.g` に組み込み、dry実行で PASS を確認済み(§7)。
- **join checker との共有禁止事項の遵守**: join checker(`join_checker.py`)はこの全単射式を**独立に再導出**しており(GAP側の `FIndexToSixPairIndices` を import しない)、探索器/照合器分離を破っていない。

### 6.2 設計方針として採択・実装は保留: Lane S/V の m 外側 loop + 前計算

Sol 提案(便104 F104-1.5 の1番目)「Lane S/V は m を外側loopにし、固定mの$\sigma_1^{2m+1},\sigma_2^{2m+1}$・f/f^{-1}展開・固定窓側generator imageを前計算する」は**設計方針として採択**するが、**本 bundle では実装していない**。理由: Sol 自身が「最適化後のcodeは較正driverとbyte-identicalではなくなる。従って...optimized laneとbaseline laneの登録sample全一致を新しい較正として置くのが正順」と明記しており(便104末尾)、この新較正(§6.3)を経る前に最適化版wrapperを本走へ投入することはSolの指定順序に反する。`lane_wrapper_S.g`/`lane_wrapper_V.g`は現状**baseline(較正走predicate libraryをそのまま呼ぶ、m外側loop最適化なし)**の実装にとどめている。

### 6.3 新設: optimized-vs-baseline 登録サンプル全一致較正(新較正段)

**本票が新設する較正段**(実装は将来、Sol/mathematician のm外側loop最適化版が実装された時点): 較正走18件(13+5)の登録サンプルに対し、baseline evaluator(現行 predicate library、byte-identical)と optimized evaluator(将来のm外側loop版)の判定が**全一致**することを確認する。**この一致確認のみが「較正」であり、optimized版そのものはbyte-identicalでなくてよい**(便104が明示的に認めた区別)。この較正が PASS するまで、optimized版を本走wrapperとして使わない。

### 6.4 不採択(Sol指定)

- **Gray-code的巡回による群積の逐次更新**(便104 F104-1.5 提案3): 「baseline evaluatorと登録sample上で全一致させてから本走用wrapperに採る」条件つきの提案であり、Sol 指定により**今回は不採択**(諮問段階にとどめる)。
- **repsn/wedderga行列表現への移送**(便104 F104-1.5 提案4): 「faithfulnessとPENT判定のiffを別に証明する必要があり、今回の即時最適化には採らない」とSolが明記。**不採択**。

---

## 7. 実行 bundle(実物・dry構造検査のみ・0候補評価)

`search/probe/hsp7_mainrun/` に実装(全ファイル一覧・SHA-256は §4 の表を参照)。

### 7.1 dry構造検査の内容と結果

- **candidate_key_lib.g の自己検査**(`CandidateKeyLibSelfCheck()`、純粋算術・群構築なし): $6\times117649=705894$ の確認、境界+内点exponent vectorのround-trip確認(`[0,0,0,0,0,0]`→index 0、`[6,6,6,6,6,6]`→index 117648、`[3,1,4,1,5,2]`等)、`m_index`対応確認。→ 全PASS(gap.ps1実行ログ)。
- **各lane wrapperの空shard dry実行**(`SHARD_LO=1, SHARD_HI=0` のような空区間、GAP `for`ループが0回実行されることを利用): 3レーンとも `候補評価数=0` を明示的に印字して正常終了(`DRIVER_DONE: true`)。実行コマンドと結果は本票 §7.2 に原文で記録。
- **join checker の mutant fixture 全件**: `join_fixtures_run.py` が9種のfixture(good/reorder/missing_shard/missing_candidate_key/duplicate_key/overlap/pcgs_endian_mismatch/same_flat_index_different_key/receipt_missing_field)を生成し、期待verdict/reasonとの一致を確認。**`overall_pass: true`**(9/9)、`reorder_canonical_hash_matches_good: true`(shard並び替えのみのfixtureが good と同一canonical hashを持つことも確認)。これは便104 (h) 要件(join mutant 全PASS)への対応。

### 7.2 実行ログ原文(実装担当・2026-08-05、gap.ps1 経由)

```
[dry_check_pcgs.g]
|P| = 5764801
|D|=|[P,P]| = 117649
NumberOfGenerators(pcgsD) = 6
RelativeOrders(pcgsD) = [ 7, 7, 7, 7, 7, 7 ]
gens listable: 6
elt for e=[0,0,0,0,0,1] computed OK: true
6 * 7^6 = 705894 (expect 705894)
DRY_CHECK_DONE

[lane_wrapper_S.g, SHARD=[1,0]]
=== lane_wrapper_S: shard [1, 0] ===
candidate_key_lib self-check: true total=705894
candidates evaluated this shard: 0
DRY_STRUCTURAL_CHECK: zero candidates evaluated (empty shard by design)
DRIVER_DONE: true
LANE_S_WRAPPER_DRY_CHECK_DONE

[lane_wrapper_V.g, SHARD=[1,0]]
=== lane_wrapper_V: shard [1, 0] ===
candidate_key_lib self-check: true total=705894
basisV built from Lane V's own PQ_OUTPUT_P.g (own measurement)
candidates evaluated this shard: 0
DRY_STRUCTURAL_CHECK: zero candidates evaluated (empty shard by design)
DRIVER_DONE: true
LANE_V_WRAPPER_DRY_CHECK_DONE

[lane_wrapper_P.g, SHARD_F=[1,0]]
=== lane_wrapper_P: f-index shard [1, 0] ===
candidate_key_lib self-check: true total=705894
f-values evaluated this shard: 0
DRY_STRUCTURAL_CHECK: zero f-values evaluated (empty shard by design)
join receipt boundary self-test PASS (f_index=0 and f_index=117648)
DRIVER_DONE: true
LANE_P_WRAPPER_DRY_CHECK_DONE

[join_fixtures_run.py]
overall_pass: true (9/9 fixtures, reorder_canonical_hash_matches_good: true)
```

### 7.3 shard_manifest_gen.py の構造テスト(算術のみ、GAP呼び出しなし)

```
$ python search/probe/hsp7_mainrun/shard_manifest_gen.py --lane S --shard-size 3678 --timeout-min 45 --frozen-driver-digest <predicate_lib_laneS.g sha256>
n_shards=192, partition_self_check="exact cover confirmed"

$ python search/probe/hsp7_mainrun/shard_manifest_gen.py --lane P --shard-size 5400 --timeout-min 45 --frozen-driver-digest <predicate_lib_laneP.g sha256>
n_shards=22, total_candidates=117649, partition_self_check="exact cover confirmed"
```

Lane P の shard数がLane S/Vの1/6軸(117,649件)になっていることに注意 — §6.1 の採択最適化がshard設計にも反映されている。

### 7.4 workflow 分割(便104 F104-1.3 是正、256 job/workflow 制約)

`shard_manifest_gen.py` は `n_workflow_batches_needed = ceil(n_shards / 256)` を manifest に含める。付録C v2 §1.2 の pessimistic シナリオ(Lane V 384 shard、3レーン合計768 shard)は256を超えるため、**1つのmatrixに全shardを入れることはできない**(便104 F104-1.3 逐語指摘のとおり)。本票は分割を「複数回の逐次workflow run」として明示し、単一matrix前提の記述を prereg から削除する(v1・付録C v2 は不改変のまま、本票がこの点を上書きする最新記述とする)。

### 7.5 artifact 容量・per-candidate watchdog(便104 F104-1.3 是正)

- **bytes/candidate 実測計画**(未実施・GHA実行を要する): 既知18fixtureをGHA上で走らせるcert出力サイズを実測し、705,894件相当のartifact総容量を外挿する。この実測は本票の範囲外(§8 未着手事項)。
- **per-candidate watchdog 未実装のため**: `timeout-minutes`はjob全体を殺すのみである(便104指摘のとおり)。本 bundle は per-candidate watchdog を実装していないため、**shard全体のhang時はshard丸ごとINCOMPLETE/STOPとし、未評価候補をUNKNOWNへ水増ししない**(便104が明示した代替規律をそのまま採用)。

---

## 8. 未着手・懸念(正直な開示)

1. **(f)(g) artifact容量実測・既知fixtureのGHA receipt**: GitHub Actions上での実行を要するため本票(dry・ローカル)の範囲外。次段の委嘱事項として残る。
2. **Lane P の P→Q 変換の未解決**(dry実装中に発見): candidate_key_lib.g の候補は $P=F_2/N_{F_2}$ 側の $[P,P]$ 上のpcgs exponent vectorとして定義されるが、Lane P の PENT 述語は $Q=K(0,5)/W$ 上で評価される(較正走の候補 `jh4^t, jh3` は最初から $Q$/$K(0,5)$ の語として直接与えられており、$P$側pcgsからの変換を経ていない)。117,649件全体を評価するには、$P$側exponent vectorから$Q$側の対応する元への明示的な写像が要る。**本bundleでは未解決**(`lane_wrapper_P.g` に `OPEN_ITEM` として明記、数学者判読待ち)。
3. **Lane V の pcgs→自由語 preimage の未解決**(dry実装中に発見): Lane V の判定述語 `EvalFullHexagonFixed(m, freeElt, ...)` は `FreeGroup(x,y)` の**語**を消費する(内部で`LetterRepAssocWord`)。較正走候補(`h4^t, h3`)は元々自由語として直接与えられていたが、candidate_key_lib.g のpcgs exponent vectorから語を得るには preimage 計算(`EpimorphismFromFreeGroup`+`PreImagesRepresentative`)が必要になる。これは数学的には健全(Pは$F(x,y)$の商なのでpreimageは必ず存在)だが、**そのコストは付録C v1/v2のLane V rate見積りに反映されていない**(見積りは短い明示語のみを想定)。**本bundleでは未実装**(`lane_wrapper_V.g` に `OPEN_ITEM` として明記)。この2点は Lane P/V の実コスト見積りそのものを変える可能性があり、本走発注前に数学者/Solへの追加諮問が要ると考える。
4. **PQ_READ_AS_FUNC_WITH_VARSの非冪等性**(dry実装中に発見・修理済み): 同一PQ_OUTPUTファイルを2度読むと、GAPオブジェクトとして`<>`な(isomorphicだが同一でない)群が構築される。当初 `candidate_key_lib.g` の `BuildCandidateBasis()` を lane wrapper 内で独立に呼び出す設計だったため、predicate libraryが閉じるP/Qと candidate basis のPが別オブジェクトになり、fail-closed チェック(`LANE_S_BASIS_MISMATCH_STOP`)が実際に発火した。`BasisFromP(既存のPオブジェクト)`への差し替えで修理し、以後は同一オブジェクトを共有する設計にした(§5・`candidate_key_lib.g`のコメント参照)。これ自体は「宇宙の事前登録」を守るための fail-closed 機構が意図通り動いた例であり、隠さず報告する。
5. **完全性主張の限定**(便104 item 5 是正、prereg v1 §4 の未確定一点への回答): 「全705,894件でLane S/Vが一致した」は、**凍結した有限候補宇宙に相対する悉皆性**を与えるのみであり、**genuine GT-shadowの完全性・source kernel全体の完全性・HS Prop.7の無条件証明とは書かない**(便104 F104-1.2 item 5 逐語のとおり、本票のどこにもそのような書き方をしていないことを確認済み)。
6. **再申請の位置づけ**: 本票+bundleが将来preflightを通過しても、**自動で本走へ連鎖発火しない**。短い再gate(Sol便への再申請)を経ること(便104 F104-1.4 末尾の条件、§0 に転記済み)。

---

以上、v2。走行・列挙は行っていない。次段は §8 の未着手事項(GHA実測・P→Q/pcgs→word変換)を数学者/司令塔が判断し、その後にSolへの再申請文を起草すること。
