# HS 本走 prereg 付録 C — v2(GitHub Actions 主経路版)

- 起草: 実装担当(短命)・2026-08-05
- 委嘱: 司令塔(研究者指示の仕様変更「付録 C の実行計画は GitHub Actions を主経路とせよ。ローカル 8GB/600秒 cap は smoke・fallback のみ」)
- **v1(`docs/notes/hsp7_mainrun_prereg_v1_appendixC_draft.md`)は不改変**。v1 のローカル単一プロセス直列見積り(2.35〜24.0日)・per-candidate rate 3 点(pessimistic/central/optimistic)・レーン別実測/推測ラベルはそのまま本票の入力として再利用する(再測定していない)。
- **本票も走行・列挙は一切していない**(委嘱範囲厳守)。GitHub Actions 上での実行は本票の認可(便104 相当)を経てから。

---

## 0. 前提・既設配管の確認(machine-piped、パス併記)

- **repo は public**(`gh repo view --json isPrivate,name` → `{"isPrivate":false,"name":"shadow-atelier"}`)。GitHub-hosted runner の Actions 分数は **public repo では無料枠課金の対象外**(billing対象は private repoのみ)。よって「無料枠内」の制約は主に**分数課金**ではなく、**同時実行 job 数の上限**(GitHub Free/Pro アカウントの既定値 = 20 concurrent jobs)と、GitHub の fair-use ポリシー(過大な継続的専有は利用規約上の配慮事項)にある。以下、同時 job 数 = **20** を前提に壁時計を計算する(司令塔指示どおり)。
- **既設 workflow**:
  - `.github/workflows/gap-run.yml`: `workflow_dispatch` で GAP スクリプトを走らせる汎用runner。`gap -q -o 12g`(ローカルの `-o 2g` よりメモリ上限が大きい — Actions runner はローカル8GB制約を受けない)。`timeout_min` 入力で job タイムアウト設定可(既定60分)。`out_dir` を artifact として回収。
  - `.github/workflows/mine-dispatch.yml`(裁定237 v0/v1): 採掘場の統一配車。**v1 差分でまさに matrix shard 対応済み**(`resources.shards` が配列のとき matrix で並列展開、各shardの `preamble` を `v0_driver.preamble` に連結して実行、実行後は「今回更新されたファイルだけ」を mtime 比較で `mine/out/<job_id>/<shard>/` へ回収)。テンプレ実例: `mine/jobs/templates/ladder-sharded.json`(`resources.shards: [{name, preamble}, ...]`、`resources.timeout_min`、`out_dir` 欄)。
  - `.github/workflows/ep-union-check.yml`: fail-closed gate の設計手本(job成功≠数学的成功、`assert_rc` を明示変数化して再送出する規律、receipt に `run_id`/`run_attempt`/`sha` を機械記録)。
  - **裁定372(`provenance/LEDGER.md` 2026-08-01)**: 採掘場の gap-ci バックエンドが「GHA success の下の隠れ失敗」(verdictベースでは done 1/13・failed 12/13)を捕獲した実績。**GitHub Actions job の緑(success)は DRIVER_DONE マーカー・候補件数一致の代わりにならない** — 本票の fail-closed 収集(§3)はこの教訓をそのまま踏襲する。
  - **G1★ era の shard+ハッシュ一致実績**(`provenance/LEDGER.md` 2026-07-19エントリ): shard-a/shard-b1/shard-b2/q1836 の4分割実行後、「宇宙分担の和の検証」(shard集合の和 = 事前登録宇宙と exact 一致)+ **証明書17件のSHA-256先頭16桁が17/17一致**。本票 §2/§3 の shard 設計・join 段突合はこの様式をそのまま踏襲する(分割数・対象は違うが手続きは同型)。

---

## 1. matrix shard 設計

### 1.1 shard 化の対象

v1 §1.2 のとおり候補全数 = 705,894(= 6 × 117,649、$m \in \mathcal X_{\mathbf N}$ × charming $\bar f \in [P,P]$)。3レーン(S/V/P)は現行アーキテクチャどおり**別 driver(別 workflow job)**として走らせる(判定ロジックの共有をしない、prereg §1.3 の digest 拘束を維持)。各レーンの入力ループを **shard 区間([f の全域を index 0..117,648 として連続区間に分割]×固定 m ループ、または m×f のフラット index を区間分割)** で割る(`mine-dispatch.yml` v1 の `resources.shards[*].preamble` 機構をそのまま流用 — 例: `SHARD_LO:=...; SHARD_HI:=...;` を driver 冒頭で束縛)。

### 1.2 shard サイズの設計(target job 時間 45 分、Actions 6時間 job 上限に対し大きな安全マージン)

v1 §1 の per-candidate rate(pessimistic/central/optimistic、実測+推測ラベル維持)をそのまま用い、1 shard あたり 45 分(2,700秒)の「有効計算時間」を狙う設計値とする(ローカル600秒capのような外形制約ではなく、Actions側は6時間まで許容されるため、runbook運用上の可読性(shard数を過大にしない)を優先した設計選択)。

$$\text{candidates/shard} = 2700 / \text{rate(秒/候補)}$$

| レーン | pessimistic rate | candidates/shard | shard数 | central rate | candidates/shard | shard数 | optimistic rate | candidates/shard | shard数 |
|---|---|---|---|---|---|---|---|---|---|
| P(PENT, Q) | 0.7342 | 3,678 | 192 | 0.5 | 5,400 | 131 | 0.25 | 10,800 | 66 |
| S(hexagon簡約, P) | 0.7342(推測=Pと同値上限) | 3,678 | 192 | 0.05(推測) | 54,000 | 14 | 0.0125(推測) | 216,000 | 4 |
| V(hexagon full ×2, P) | 1.468(推測=Sの2倍) | 1,839 | 384 | 0.10(推測) | 27,000 | 27 | 0.025(推測) | 108,000 | 7 |
| **合計(3レーン)** | | | **768** | | | **172** | | | **77** |

(shard数は $\lceil 705{,}894 / \text{candidates/shard} \rceil$。S/V の rate は v1 §1 の推測値であり実測ではない — §5 のCI較正shardで埋める。)

---

## 2. per-shard cert + join 段突合(G1★ 様式の踏襲)

- 各 shard job は既存 driver をそのまま実行し、prereg §1.3 の schema(`gtsh-cert` 系)で shard 分の cert JSON を出力する(判定ロジック・出力スキーマは較正走から変更しない)。
- **join 段(集約 job、1本、matrixの後段に依存関係で接続)**:
  1. **shard 数の突合**: 収集した shard cert の数 = §1.2 の設計 shard 数と exact 一致すること(欠 shard があれば §3 の STOP)。
  2. **宇宙分担の和の検証(G1★ 様式そのまま)**: 全 shard の候補区間の和集合 = 705,894 件の事前登録宇宙と exact 一致(重複なし・欠落なし)。G1★ の「shard-a+shard-b1+shard-b2+q1836 = 事前登録宇宙」と同型の検査を機械実行する。
  3. **ハッシュ一致(バイト同一性、G1★ の17/17 と同型)**: 各 shard cert の SHA-256 を記録し、Lane S/V/P/Σ それぞれで shard間のスキーマ・digest整合を機械確認(内容は shard ごとに異なるので「全shard同一ハッシュ」ではなく、「各shardが宣言した候補区間・driver digest・schemaバージョンが一致していること」の突合。実測値そのものの重複チェックは §3 の分布集計で行う)。
  4. 分布表(prereg §4 の様式)への集約は全 shard 分を単純合算(新規判定基準の追加はしない、prereg §4 のルール継続)。

---

## 3. run ID + commit + digest の provenance 三点セット

prereg §5 の「commit/blob/sha256 三つ組」方式を Actions 実行の receipt にもそのまま適用する(`ep-union-check.yml` の receipt 生成パターンを踏襲):

```jsonc
{
  "run_id": "<GITHUB_RUN_ID>",       // Actions run の一意ID(gh run download で追跡)
  "run_attempt": "<GITHUB_RUN_ATTEMPT>",
  "sha": "<GITHUB_SHA>",             // このrunが checkout したcommit
  "shard_id": "<name>",
  "frozen_driver_digest": "<sha256 of driver .g、prereg §1.3の較正走digestと一致すること>",
  "shard_cert_sha256": "<このshardが出力したcert JSON全体のsha256>"
}
```

- **collection 段(join job)は各 shard の receipt から `run_id`/`sha`/`shard_cert_sha256` を読み戻し、機械記録する**(手写し禁止、`ep-union-check.yml` の `assemble receipt` ステップと同型)。
- **fail-closed 収集(§4 と連動)**: 三点セットが欠けている shard(receipt自体が無い、またはfield欠損)は「未完了」として扱い、§4 の STOP トリガに含める。

---

## 4. fail-closed 収集(欠 shard = STOP)

裁定372(「GHA job success ≠ driver 完了」)の教訓を直接反映する。join 段のゲートは**job の exit code だけでは PASS としない**:

| チェック | 内容 | 不一致時 |
|---|---|---|
| (a) job status | 全 shard job の GitHub Actions 実行結果が success | 1件でも非successなら STOP |
| (b) DRIVER_DONE マーカー | 各 shard の cert/log に `DRIVER_DONE: true`(または prereg 既存様式のマーカー)が存在 | 欠落は STOP(job成功でもdriver未完了とみなす — 裁定372の事案そのもの) |
| (c) shard数の完全性 | 収集 cert 数 = §1.2 設計 shard 数(欠 shard 0 件) | 1件でも欠ければ STOP(部分成功を全体成功と数えない) |
| (d) 宇宙分担の和 | §2.2 の和集合検査 = 事前登録宇宙と exact 一致 | 不一致は STOP |
| (e) digest一致 | §3 の `frozen_driver_digest` が全 shard で較正走 digest と同一 | 不一致は STOP(較正走と異なるコードで走らせていないことの担保、prereg §1.3 と同じ規律) |

**STOP時の扱い**: 部分結果は保存(prereg S-7′と同型の扱い)、同一runで予言を書き換えない、原因(欠shard/digest不一致/marker欠落)を明記して司令塔へ報告。**自動リトライで握りつぶさない**(欠shard検出→無条件再送出のような「fail-open修理」は裁定372が名指しした失敗パターンそのもの)。

---

## 5. CI 上での較正 shard(認可後、本走前の1ステップとして計画に組込み)

- v1 §1 で明記したとおり、**Lane S/V の per-candidate rate は実測ではなく推測**(Lane P の実測値からの類推、`docs/notes/hsp7_mainrun_prereg_v1_appendixC_draft.md` §1)。
- **提案する段取り(認可後に実施、本票では実施していない)**: 本走の matrix 発注前に、**Lane S・Lane V それぞれについて「較正走13件+NW-P7 5件と同一の18件」を GitHub Actions 上で1 shard として走らせ**(`gap-run.yml` または `mine-dispatch.yml` の非分割1entry実行)、実際の Actions runner 上での wall time を実測する。この実測値で §1.2 の rate 表(S/V の「推測」ラベル)を「実測」に更新してから、本走 matrix の shard サイズを再計算する。
- この CI 較正 shard 自体も §3 の provenance 三点セット(run_id/sha/digest)を記録し、v1 の「Lane P: driver_precheck5_mutants.log 実測」と同格の一次データとして扱う。

---

## 6. ローカル実行(smoke・fallback、1 shard 分のみ)

- **ローカルは本走の主経路ではない**(冒頭方針どおり)。用途は (a) matrix投入前のdriver動作確認 (b) Actions障害時のfallback、の2点に限定。
- **1 shard 分のみ**: ローカル `gap.ps1` 実行は v1 の**ローカル600秒cap向けshardサイズ**(v1 §3、例: Lane P 700件/shard・Lane S 700件/shard・Lane V 350件/shard、central想定)を用いる。これは §1.2 の Actions 用shardサイズ(45分/shard、数千〜数万件)とは**別の定数**である(同一driverコード・同一digestのまま、ループ境界の入力値のみが異なる — prereg §1.3の「入力ループのみ悉皆化」の精神と同じ)。
- ローカル smoke で 1 shard を通し、cert schema・DRIVER_DONEマーカー・digestが期待どおり出ることを確認してから、Actions matrixへ本発注する(既存 `mine/preflight.py` の4ゲート相当のセルフチェック)。

---

## 7. 壁時計の3点見積り(GitHub Actions・同時job数20 前提)

### 7.1 理想化(shard間の起動オーバーヘッドを無視、CPU時間/20 の単純割り)

v1 §2 の合計CPU時間(3レーン合算・単一プロセス直列相当)をそのまま 20 並列で割る:

| シナリオ | v1 合計(直列) | ÷20(理想化) |
|---|---|---|
| pessimistic | 575.75 h(24.0日) | 28.79 h |
| central | 127.45 h(5.31日) | 6.37 h |
| optimistic | 56.37 h(2.35日) | 2.82 h |

### 7.2 shard起動オーバーヘッド込み(§1.2 の45分/shard設計 + checkout/setup-gap/artifact-upload オーバーヘッド概算5分/shard、20並列での「ラウンド」単位)

| シナリオ | 総shard数(§1.2) | ラウンド数(⌈shard数/20⌉) | 1ラウンド ≈ 45分+5分=50分 | 壁時計 |
|---|---|---|---|---|
| pessimistic | 768 | 39 | 50分 | 1950分 = **32.5時間 ≈ 1.35日** |
| central | 172 | 9 | 50分 | 450分 = **7.5時間** |
| optimistic | 77 | 4 | 50分 | 200分 = **3.33時間** |

**結論(見出し数値)**: ローカル直列 2.35〜24.0 日(v1)が、GitHub Actions 主経路(同時job数20 前提)では **約 3.3 時間〜約 1.35 日** に短縮される(オーバーヘッド込みの現実的側の見積り。理想化なら 2.8〜28.8 時間)。

---

## 8. 無料枠見積り(job分数 × shard数)

- **repo が public のため、Actions の compute分数そのものは無料枠課金の対象外**(§0)。よって「分数の枠外課金」という意味でのハード制約は存在しない。
- 参考として **総 job-hours**(shard数 × 45分、資源占有量の目安・fair-use上の配慮材料)を記録する:

| シナリオ | shard数(合計) | job-hours(45分×shard数) |
|---|---|---|
| pessimistic | 768 | 576.0 h |
| central | 172 | 129.0 h |
| optimistic | 77 | 57.75 h |

- **枠外判定はしない**(委嘱どおり)。576 job-hours(pessimistic)規模は無視できない占有量であり、**この数字自体を研究者に開示し、実行判断(特に pessimistic シナリオでの発注可否)は研究者/司令塔に委ねる** — 本票はここで「要研究者判断」と明記するに留める。

---

## 9. 未解決・懸念(v1から持ち越し+今回追加分)

1. Lane S/V の per-candidate rate は依然として推測(§5 のCI較正shardで実測へ更新する計画のみ、未実施)。
2. §1.2 の「45分/shard」という設計値自体が任意の運用選択(Actions 6時間上限に対し安全側に倒しただけ)であり、Sol/司令塔がより大きい shard(オーバーヘッド比率を下げる)やより小さい shard(1件あたりの障害影響を小さくする)を選ぶ余地がある。本票はこの1点も選び直していない。
3. GitHub の同時job数上限20はアカウントプランの一般的既定値であり、**この repo/アカウントで実際に20が適用されるかは未確認**(司令塔指示の前提をそのまま採用したのみ、`gh api` 等での実測確認はしていない)。
4. §1.2のshard数(pessimistic 768・central 172・optimistic 77)は §1.2の rate表(Lane S/V推測込み)に直接依存するため、§5のCI較正が完了すればこの表全体が再計算対象になる。

## 10. Sol への高速化諮問の材料(便 104 §用・自分では最適化しない)

**位置づけ**: 本節は Sol との共同設計への入力であり、司令塔・実装担当が最適化を決定するものではない。以下は v1 の実測(§0・driver ソース読解)から推定した「現行 per-candidate 0.7342〜3.1283 秒の内訳がどこに支配されているか」の構造的推定と、諮問すべき観点の列挙に限定する。

### 10.1 何が支配的か(driver ソースからの構造推定、実測プロファイラなし)

v1 では `Runtime()` 等の内部計装が無いため(v1 §0)、以下は**コードパスの読解からの推定**であり、行単位の実測時間分解ではない。

| レーン | 評価1候補あたりの構成要素(driver ソース読解ベース) | 推定される支配項 |
|---|---|---|
| P(PENT_W、`search/probe/hsp7_cond4_laneP_p5control/driver_precheck5_mutants.g` L77-84) | `NrhoQ_real`: `ImageElm(rhoQ, ·)` を **4 回連鎖適用**(ρ̄⁴,ρ̄³,ρ̄²,ρ̄の合成)+ 積 `r4*r3*r2*r1*fbar` + `IsOne` 判定。対象は Q(pc群、生成子40個、位数7^40)。 | pc群での準同型像計算(`ImageElm`)— pc collection のコストは生成子数(40)・冪零類に依存。4回の連鎖適用が1候補あたりの主要コストと推定(単純な積・IsOneは相対的に軽いと推定)。 |
| V/S(hexagon、`search/probe/hsp7_cond4_laneV/statemachine_lib.g` L175-199 `EvalFullHexagonFixed`) | LHS(3.3)/RHS(3.3)/LHS(3.4)/RHS(3.4) の **4 系列**をそれぞれ `ApplyWordSeq` で状態機械的に1文字ずつ適用(`ExpandXYLettersToSigma`+`LetterRepAssocWord` で語を展開後、`SeqPow([1],u)` 等 **u=2m+1 文字**+f/f^-1 の語長ぶんを逐次群積)。対象 P(位数7^8、Lane V の N0 側はP×C7で位数7^9)。Lane V は N と N0 の**両方**で評価(§1 の「2倍」係数の実体はこの4系列×2ウィンドウ)。 | 語長 O(u + \|f\|) に比例した**逐次群積の連鎖**(状態機械が1文字ずつ`ApplyGen`)が支配項と推定。u=2m+1 は m(0..6程度)に依存するため、**m が大きい候補ほど1候補あたりコストが増える可能性**(v1 のrate表はm依存性を平均化した blended rate であり、m別のコスト分解はしていない)。 |

### 10.2 諮問したい観点(列挙のみ、司令塔・実装担当は選択しない)

1. **前処理・キャッシュ**: 固定 m に対する `sigma1^u`・`sigma2^u`(u=2m+1文字ぶんの逐次積)は同一 m を共有する 117,649 件の f 候補すべてで共通の接頭辞/接尾辞になりうる。ループ順序を m 外側・f 内側に固定した上で、m ごとに sigma^u 部分の状態を1度だけ計算し使い回すことは可能か(現行 `EvalFullHexagonFixed` は候補ごとに `Identity(phiX)` から再計算している、L181 `base := [1, Identity(phiX)]`)。
2. **バッチ化・プロセス常駐**: 群構築(ANUPQ pq、v1 §0 実測で P5構築62秒・Q5構築46秒の一回性オーバーヘッド)は shard 単位で払い直しになる設計(§1.2、pessimistic 768 shard = 768 回分のオーバーヘッド)。1 レーンにつき長時間常駐する少数プロセス(shard 分割を評価ループ側だけに閉じ、群構築は使い回す)にする余地はあるか。ただしこれは §4 の fail-closed 収集・shard 独立性(耐障害性)とのトレードオフになるため、諮問止まりとし選択しない。
3. **語の共通部分式の再利用**: Lane V の 4 系列(LHS/RHS ×2式)は base 状態からそれぞれ独立に `ApplyWordSeq` を再実行している(L184,188,192,195)。f/f^-1 の展開語(`fSeq`/`fInvSeq`)自体は1候補内で共有されているが、系列間・候補間での部分積の再利用(メモ化)は行っていない。これに数学的な余地があるか(状態機械の性質上、部分状態の再利用が判定の意味論を変えないか)は数学者判読が要る観点として諮問する。
4. **群の表現形式**: Q(7^40、pc群40生成子)での `ImageElm` の collection コストは pc 生成子数に強く依存する可能性がある。同梱パッケージ(`repsn`/`wedderga`、CLAUDE.md 記載)による行列表現への置き換えで `ImageElm` 相当の計算が高速化しうるか、または pc群のまま順序を最適化する余地があるか。
5. **N と N0 の重複評価(Lane V の2倍係数)**: 現行は N・N0 を独立呼び出しで評価している(§10.1 表、`driver_step4_evaluate_v3.g` L167-182)。両ウィンドウで共有可能な部分計算(例えば f/f^-1 の展開語生成 `ExpandXYLettersToSigma`/`LetterRepAssocWord` はウィンドウ非依存)があるか。

**本節は諮問の形にとどめる**(実装担当・司令塔は最適化を決定・実施しない)。§9 の懸念(Lane S/V rate 推測)とあわせて、便 104 §(Sol への高速化諮問)の材料として提供する。

---

以上、v2。走行・列挙は行っていない。数値は v1 の実測+推測値からの外挿と、Actions既設配管(gap-run.yml/mine-dispatch.yml v1/ep-union-check.yml)の仕様・裁定372/G1★実績からの設計提案、および §10 のdriverソース読解(実測プロファイラなし)のみで構成。司令塔が本票を確認し、便相当の申請へ進めるかどうかを判断すること。
