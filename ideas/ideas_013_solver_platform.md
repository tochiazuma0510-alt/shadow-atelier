# ideas_013 — 大規模探索基盤「採掘場(mine)」: ソルバー調査+アーキテクチャ設計

**【札】本文書の全体が candidate(発案係の提案)である。採否は司令塔・研究者の専権。** 本便は通常の予想札と異なり、研究者による発案係名指しの直接依頼(2026-07-30「調査から設計まで一気に」)への応答。なお同名の旧文書は研究者裁定で破棄済みであり、本文書はゼロから新規に起草した(旧内容は参照していない)。

- 起草: 発案係(ideator・第 13 便)・2026-07-30。
- 規模ラベル: **現在線級〜中間峰級**(工程インフラの再設計 — 数学の主張は含まない)。
- 出所ラベル: §1 = 実ファイル確認(全て本日開いて確認・推測記述なし)。§2 = ライブ外部検索(URL 併記・付録 A)。§3〜6 = 発案係の設計判断。
- 依頼の核心 1 行: **「新しい事実(律・不変量・判定条件)がわかったら条件を追加するだけで手直し最小」の大規模探索システム。環境 = CI。実行者に専任を付ける。**

## 先に結論(設計の骨子 5 行)

1. **単一ツールへの乗り換えはしない**。工房の主対象(窓 = B₃ の有限商の置換群・shadow 走査)には GAP が最適で代替が存在しない。答えは「**複数ツールの組み合わせ、ただし接続面を一つに統一**」。
2. 統一面は三枚: **述語台帳(条件レジストリ)** ・ **ジョブ仕様 mine-job/v1(宇宙の事前登録の機械化)** ・ **統一配車 CI(plan push 駆動)**。三枚とも既存資産(kerchi-judge.g の述語群・mb-search.yml の plan 駆動 matrix・certs 文化)の**再配線**であり、ゼロから作る物はほぼ無い。
3. 新規導入ツールは 4 つに絞る: **CaDiCaL 2.x**(incremental・LRAT native)・**cake_lpr**(形式検証済み proof checker)・**ganak**(#SAT = 解数勘定の独立第二系統)・**Vole**(正準化・normalizer の強化、CI 専用)。Magma は不要と明言する。
4. 「条件を追加するだけ」は三経路で実現: 新しい**律** = 述語カード 1 枚 + fixture + 対付け 1 行/新しい**窓族** = universe generator のパラメータ JSON/新しい**非存在標的** = CNF fragment の追加(incremental)。
5. v0 の載せ替え第一号は**梯子走査**(理由 §6)。r=4 セル悉皆が第二号、帯採掘は述語差し替えのデモ。

---

# §1 手元棚卸し(機能表 — 実物確認に基づく)

凡例: 【対】= 独立系統の対(探索器⟷照合器)。全て本日実ファイルを開いて確認した。

## 1.1 GAP 探索器層(search/*.g 142 本)

| 資産 | 入力 | 何をする | 独立系統の対 | 再利用可能な部品 |
|---|---|---|---|---|
| `search/kerchi-judge.g` v1.3 | 窓の指定 2 方式: (a) LINS node(`JUDGE_INDEX_BOUND`+`JUDGE_WINDOW_ID`)(b) 直接生成元 images(`JUDGE_S1_IMG/S2_IMG`・行列も可) | ker χ̃ の可換/非可換判定・shadow 走査((F2)+settled)・scan_mode 自動 dispatch(legacy ⟷ xi_restricted・Prop 3.1 の Ξ 制限走査)・fail-closed assert | 【対】`ladder-xi-recheck.py`(Ξ 走査部) | `MakeWindow`・`CorrectedShadowsXi`・`AbstractProd`・`TH`/`RtOf`。**事実上の述語ライブラリ**(ただし密結合) |
| `strike-a16/a18/a20.g`+`*-kernel-structure.g`+`*-filter-ledger.g` | 窓 1 つ | 窓の深掘り(STAGE1 assert → STAGE2 判定・核構造・filter 台帳) | witness 部のみ `strike-witness-recheck*.py` | STAGE assert の型(fail-closed で JSON cert へ) |
| `wall-miner-v1..v5.g` | LINS 指数帯 | 帯採掘(非可換核ハント・T5 型) | 単系統(裁定 225 は単一 LINS) | LINS 反復順の規約(窓 ID 規約と一体) |
| `canonical-uid.g`+`test-canonical-uid.g`+`xi-uid-export.g` | 窓 | **窓作用グラフの bliss 正準化 → canonical UID**(回帰 PASS: `certs/canonical_uid_selftest_20260730.json`) | — | §4 のキャッシュ鍵の土台。**既に存在することが本設計の急所** |
| `search/probe/wac_v1/`(r4_existence_search.g・r4_cell_logic.g・r4cells/・enum2.g・ree.g 等) | 族パラメータ(n, ℓ, r, t) | セル悉皆(T3 型)・Ree 篩・存在探索。cert は method_note+script_sha256+「raw measurements only」型 | `_probe_a14_exhaustive.g` が enum2.g の独立第二系統になった実績(裁定 207) | r4 cert の段構造(step0 分類 → step1 パリティ → step2 探索)は**ジョブ仕様の原型** |
| `suite-wp1/wp2*.g`・`week3-battery*.g`・`week3-psl-S*.g` | 較正宇宙 | 較正スイート(shard 分割済み・全 GAP 実行 600 秒 cap 内の実績) | check-*.mjs 群 | shard 分割の前例 |

## 1.2 独立照合器層(GAP 非共有)

| 資産 | 実装系 | 照合範囲 | 備考 |
|---|---|---|---|
| `search/ladder-xi-recheck.py` | python + sympy BSGS(Schreier-Sims) | F2/RtOf/TH/settled/(3.53) 合成閉包の**数学仕様からの再実装**(コード翻訳禁止を冒頭 40 行で宣言・規約は AbstractProd 逆順まで文書化) | 二系統一致 13/13 の実績(裁定 216)。**T2 型の照合器の完成品** |
| `search/xi-set-equality-check.py` | python | 受理集合の集合等価 | |
| `crosscheck/check-*.mjs` 群(check-psl 等) | node | 窓 census 系の独立再計算(GF(q) 行列直接構成など、経路まで独立) | T1 型の照合器 |
| `search/strike-witness-recheck*.py` | python | witness 水準の検算(規約バグを 2 度捕獲した実績 — 裁定 201) | |
| `search/sat/check_model_n21.mjs`・`check_model_a25.mjs` | node(**非 import**) | SAT model の decode と再検査(a・b・reachability を model から再導出) | T4 の SAT 側 witness checker |
| `search/sat/lrat_check.py` | python(from scratch) | **自前 LRAT checker**(drat-trim 非依存・RAT 完全性検査に occurrence index・vacuous RAT 対応) | drat-trim の出力を独立検査する第二 checker |

## 1.3 SAT 線(search/sat/)

- **encoder**: `encode_tail8_n21.py`・`encode_a25.py`・`encode_diam20_path21.py`。fixture(GAP 機械抽出 witness)を import 時に assert する設計。
- **manifest**: `manifest_tail8_n21.json` = `shadow-atelier/sat-encoder-manifest/v1`。変数族(id 範囲・意味)・**clause_groups(節グループの開始/終了番号)**・cnf sha256・expected_verdict・**audit_status(soundness は checker で・completeness は数学者の紙補題と明示分離)**。この clause_groups 構造が §4.4 の fragment 化の土台。
- **mutant**: `gen_mutants_reverse_drop.py`+`mutants_n21.json`/`mutants_a25.json`(エンコーダ健全性の変異試験)。
- **runs/ 収蔵**: `result.txt`(exit=NN / verdict=SAT|UNSAT|UNKNOWN)・`SHA256SUMS.txt`・`proof.drat(.gz)`・`proof.lrat.gz`・`core.cnf.gz`・`kissat_time.txt`。**判定は result.txt からのみ取得する machine-piped 規約が既に成立**。
- `calibrate_small_n.py`: 小 n 較正。

## 1.4 CI 資産(.github/workflows/ 6 本)

| workflow | 駆動 | 要点 |
|---|---|---|
| `gap-run.yml` | 手動 dispatch | setup-gap@v3.8.0(GAP 4.16.0)・**preamble 注入**(`SHARD:=2;;` を driver.g に前置)・`-o 12g`(CI は 12GB — ローカル 2g の 6 倍)・certs artifact 回収 |
| `sat-run.yml` | 手動 dispatch | kissat/drat-trim を **commit SHA pin でビルド**・**run_label = calibration/theorem の二値ゲート**(theorem は cnf_sha256 必須・fail-fast)・入力の文字クラス allowlist(shell injection 防止)・UNSAT なら drat-trim 検証 + core/LRAT 抽出・SHA256SUMS |
| `mb-search.yml` | **plan JSON push 駆動** | `mb-shard-plan.json` を push すると発火 → schema validate → **integrity gate(凍結 5 文書+探索器の sha256 を plan 記載値と照合・不一致 fail)** → shard matrix 実行 → concurrency 制御。**本設計の統一配車の原型はこれ** |
| `wall-smoke.yml` | — | B₃ 正規部分群の二環境一致 smoke(33 本) |
| `lean.yml`・`lean-arith.yml` | — | Lean 検証線(verified 予約語の実体) |

## 1.5 証明書・台帳・ops

- `search/certs/` **132 個**。JSON + `script_sha256` + `gap_invocation` + method_note +「NOT a ledger claim」明記の文化。**checkpoint ファイル**(`.i10_1_xi_recheck_checkpoint_*.json`)= レジューム機構も既にある。
- `provenance/CLAIMS.md`: 状態語彙 = candidate / cross-checked / verified(Lean 専用)/ UNKNOWN / refuted。`provenance/LEDGER.md`: 出所記帳(CI run 番号・sha256・環境)。
- `ops/bin/ben_preflight.py`(便の機械 preflight)・`deliver_task.ps1`(Sol/Luna 配達)。

## 1.6 GAP パッケージ棚(導入済み・実棚を確認)

`C:\Program Files\GAP-4.16.0\runtime\opt\gap-4.16.0\pkg` を実開して確認。本設計に効く物:

- **導入済で現用**: `lins`(低指数正規部分群 = T5)・`digraphs`(**bliss 同梱** = canonical-uid.g の土台)・`ctbllib`・`anupq`/`autpgrp`・`twistedconjugacy`・`repsn`/`wedderga`。
- **導入済で未使用(眠っている強力棚)**: **`ferret`**(Leon の partition backtrack の C++ 再実装 — 集合安定化・正準化系の高速探索)・**`orb`**(大軌道の分散列挙)・**`genss`**(generic Schreier-Sims — 巨大次数の BSGS)・**`recog`**(行列群認識)・`primgrp`/`transgrp`(原始群・可移群ライブラリ = 窓分類の照合表)・`atlasrep`・`semigroups`・`grape`。
- **未導入**: **Vole**(ferret の後継・Rust)・images パッケージ。→ §3 で Vole を CI 側採用候補に。

## 1.7 ES7 輸入可能資産(別リポ C:\Users\81905\Desktop\atelier_lean)

- `es7_sat_matrix.yml`: **manifest + jq_map → {id, file, sha256} 配列 → 256 上限の matrix 化・offset/count スライス**。SHA ゲート → kissat → 検証 → 収蔵。**多 CNF 一斉射の完成品**(mutant matrix もこの型)。
- `ES7/abstract_sat/`: 496 変数 110 万節を 4.43 秒で UNSAT・drat-trim VERIFIED・UNSAT core 抽出(1.1M→12k 節)・LRAT 保存・**「Lean 級への昇格路 = LRAT を Lean 内の検証済み checker で再検査」と README に明記済み**。この昇格路設計は §3 の cake_lpr/PBLean と直結。

## 1.8 EP(N∞ evidence pipeline)— 接続点の予約のみ

`ninfty-ep-runner.py` v3 = cert-validator GATE を全証明書に強制する**評価**パイプライン(探索ではない)。schema 隔離中(裁定 234: 発効 gating は Sol 便 88 判定へ)。**本設計では統合対象にしない**。予約する接続点は一つ: §4.3 のジョブ仕様に `ep_handoff`(EP へ渡す証明書の出力先とスキーマ版の欄)を空欄のまま持たせ、EP v7 発効後に埋める。

## 1.9 棚卸しの総括 — 何が問題か(研究者の指摘の裏取り)

研究者の現状認識「ソルバーが既製品と自作でバラバラに点在・新事実のたびに設計と実装をやり直し」は実物と一致する。具体的には:

- **G1(最大)**: ジョブの定義(宇宙・述語・出力)が各 driver .g に手書きで埋め込まれている。新しい律が出るたびに新 driver を書く。kerchi-judge.g は述語ライブラリとして再利用されているが、**述語の追加・組み合わせ変更 = GAP コード編集**である。
- **G2**: 探索器⟷照合器の対付けが暗黙(どの cert とどの cert が対か、照合が揃ったかは裁定の人力管理)。
- **G3**: CI 起動の大半が手動 dispatch(plan push 駆動は mb-search だけ)。
- **G4**: LEDGER 記帳・地図 delta が手動。
- **G5**: 解数勘定(T3)が GAP 単系統(独立第二系統が無い)。
- **G6**: SAT の条件追加 = encoder 書き直し(incremental 未使用・fragment 未分離)。
- **G7**: LRAT の独立検査が自前 python のみ(形式検証済み checker 不在)。
- **G8**: 窓 canonical UID があるのに、(窓, 述語) の評価結果キャッシュが無い — 同じ窓に同じ述語を何度も走らせている。

---

# §2 外部調査(2024〜2026 の実勢)

評価軸: 工房の仕事の型(T1 窓 census/T2 梯子走査/T3 セル悉皆/T4 SAT 非存在/T5 帯採掘)への効き・ライセンス・Windows/GitHub Actions 適合・**証明証書(proof artifact)の有無**。出典 URL は付録 A に一括。

## 2.1 SAT 核ソルバー

| 候補 | 実勢 | 効く型 | ライセンス | GHA 適合 | 証明 |
|---|---|---|---|---|---|
| **kissat**(現用) | SAT Comp 2025 主系列は Kissat 系変種が上位独占(UNSAT トラック 2 位 Kissat-VSA 160 問) | T4 | MIT | 実績あり(commit pin 運用中) | DRAT 出力 → drat-trim で LRAT |
| **CaDiCaL 2.x** | SAT Comp 2025 UNSAT トラック 1 位(CaDiCaL-SC2025・161 問)。**CAV24 論文で LRAT native 生成**・incremental(IPASIR)・**IPASIR-UP**(探索中の外部 propagator/動的節追加)・iCNF 対応。「Certifying Incremental SAT Solving」(LPAR24)で **incremental 求解の証明**まで整備 | T4 +「条件追加で再走」 | MIT | 良(ビルド容易) | **LRAT を solver 自身が直接出力**(drat-trim 変換不要 = 証明経路が 1 段短い) |
| Gimsatul | 並列(共有メモリ)。GHA の 2〜4 vCPU では効き薄 | — | MIT | 可 | DRAT |
| IsaSAT | 形式検証済み**ソルバー**。速度で劣る。checker 側検証(cake_lpr)で足りるため不要 | — | — | — | — |

## 2.2 証明形式と検証済み checker

| 候補 | 実勢 | 位置づけ |
|---|---|---|
| DRAT/LRAT(現用) | 標準。drat-trim(現用)+ 自前 `lrat_check.py`(現用) | 維持 |
| **cake_lpr** | **CakeML でバイナリまで形式検証された LRAT/LPR checker**。SAT Comp 2025 の公式 checker。2025-02 に性能 5-10% 改善。バイナリ LRAT 対応 | **採用推奨**: drat-trim(生成側)⟷ lrat_check.py(自前)⟷ cake_lpr(形式検証済)の三系統。ES7 README の「Lean 級昇格路」の実装候補そのもの |
| FRAT | solver 側フォーマット。CaDiCaL LRAT native 採用なら不要 | 見送り |
| **VeriPB + CakePB** | pseudo-Boolean 証明。**対称性破り・cardinality・XOR・CP・MaxSAT 前処理まで証明可能**。SAT Comp 2025 公式・CakePB は検証済み checker(CP2025) | 将来枠: 対称性破り節を CNF に入れる時(§2.6)の証明経路。現行 CNF は対称性破り無しなので今は不要 |
| **PBLean**(arXiv 2602.08692) | **PB 証明書の Lean 4 checker**(2026) | 装置提案: 「verified は Lean 専用」文化との接続点。監視対象 |

## 2.3 計数(#SAT)・列挙(AllSAT)

| 候補 | 実勢 | 効く型 |
|---|---|---|
| **ganak**(meelgroup) | **2024・2025 Model Counting Competition 全トラック優勝**。exact・probabilistic・**projected counting**・weighted(**有限体係数まで**)・**d-DNNF 回路出力**(再クエリ・列挙に使える)。MIT。ビルドは GMP/MPFR 依存(GHA workflow が upstream にあり流用可) | **T3 の独立第二系統**: セル悉皆の解数(例: r=4 の 40)を GAP 軌道法と全く別原理(component caching + 決定図)で数え直す。**証明証書は出さない**(ddnnf_verify.py のみ)→ 使い方は「二系統一致の一翼」限定・陰性(解 0)主張は SAT UNSAT 証明経路へ回す |
| sharpSAT-TD | 2021-2023 の覇者(tree decomposition 前処理)。MIT | ganak の代替(第二候補) |
| d4 | 2024 で ganak に 89 問差で敗退 | 見送り |
| TabularAllSAT(AIJ 2025) | blocking clause 無しの disjoint 列挙(chronological backtracking)。**AllSAT の最新** | 将来枠: witness 全列挙が #SAT で足りなくなったら。成熟度・入手性で今回は見送り |
| ApproxMC | 近似計数 | 射程外(工房は exact 勘定が必要) |

## 2.4 分割・分散

| 候補 | 実勢 | 判断 |
|---|---|---|
| **cube-and-conquer**(march_cu / CnC) | 「困難インスタンスを look-ahead で cube に分割 → 各 cube を incremental CDCL で並列求解」。現在も困難問題の標準戦術 | **採用(v2)**: cube リスト → GHA matrix job への配分は `es7_sat_matrix.yml` の offset/count スライスの自然延長。「Smart Cubing for Graph Search」(2025)は同型除去付き探索での cube 設計も扱う |
| mallob | 分散ジョブスケジューラ+malleable SAT。クラスタ/クラウド前提 | **落選**: GHA の job 分離モデルと合わない(MPI/常駐前提)。工房規模では cube+matrix で足りる |
| Paracooba / D-Painless | 同上(分散 CnC・portfolio) | 落選(同上) |

## 2.5 SMT

| 候補 | 実勢 | 判断 |
|---|---|---|
| **cvc5** | CPC 証明形式(662 規則)+ **Ethos checker**・Alethe 出力・**Lean-SMT**(CAV 2025: cvc5 証明の Lean 再構成)・finite model finding | **装置提案(将来枠)**: 現行の標的(置換の存在/非存在)は SAT 直 encode が既に動いており、SMT を挟む翻訳の監査コストが上回る。非線形整数制約(構造定数の Diophantine 条件等)が標的化したら再訪 |
| Z3 | 証明出力が弱い(unsat core 止まり・独立 checker なし) | 落選(証明証書の無い判定は工房で主張に使えない) |

## 2.6 対称性・同型除去

| 候補 | 実勢 | 判断 |
|---|---|---|
| **SMS**(SAT Modulo Symmetries) | CDCL + minimality propagator で**同型除去済み列挙**(TOCL 2024)。QBF 対応(2025)・専用 propagator による枝刈り(CP 2025)。co-certificate 論文あり、だが propagator の soundness は自前監査になる | **将来枠(候補発見器)**: ソルバー哲学(バグ許容・候補発見)には合致。ただし「窓の同型」は グラフ同型でなく群作用同型なので、encode 設計が一仕事。T1 の大規模化(S>D₈ 窓ハント等)で再訪 |
| **Vole**(peal) | **ferret の後継・Rust 実装の graph backtracking**(JPWW21)。canonical image・normaliser・stabiliser・intersection。「既存ツールでは不可能な canonical image 機能」を含む(公式 doc)。GAP パッケージとして GAP から呼ぶ | **採用(v3・CI 専)**: canonical-uid.g の bliss 経路の**強化+独立第二正準化系**。normalizer 計算は P3(GTSh 構造 = 正規化群の 2-局所化)の実測に直結。Windows ローカル(cygwin GAP)でのビルドは未検証 → CI(ubuntu)専とし、ローカル bliss 経路を対に残す |
| nauty/Traces 2.9.3(2026-01) | 正準ラベリングの старейший 標準。bliss は Digraphs 同梱で現用 | 現状維持(bliss で足りる)。外部独立正準化が要る時の第三系統 |

## 2.7 有限モデル発見・ATP

- mace4/SEM/paradox: 有限モデル発見の古典。「関係式を満たす位数 n の群を探す」は工房では GAP(構成的)+ SAT(存在/非存在)で被覆済み。**落選**。
- Vampire(fmf)・E: 一階証明。工房の主張は具体有限群上の等式/存在で、ATP の射程(一般量化)と合わない。**落選**。

## 2.8 CP

- OR-Tools CP-SAT: 高速だが**証明証書なし**・置換群語彙なし。候補発見器としても SAT 直 encode に対する優位が示せない。**落選**。
- MiniZinc: モデリング層(下は各ソルバー)。証明なし。**落選**。ただし「ジョブ仕様 → 各バックエンド」という**アーキテクチャ思想**は §4 が翻訳して輸入する(モデル 1 枚から複数ソルバーへ、の形だけ)。

## 2.9 Magma の要否

**不要と明言する。** 理由: (a) ライセンス閉・CI で走らない = 再現性の思想と非互換(証明書に「Magma でしか再計算できない値」を作ってしまう)。(b) 置換群アルゴリズム(BSGS・正準化・正規化群)は GAP + ferret/Vole + bliss で代替可能。(c) 二系統独立の相方としては sympy(現用)と node 直実装(現用)が既に機能している。

---

# §3 ギャップ分析とツール選定(結論)

§1.9 のギャップ G1〜G8 に対し:

| ギャップ | 解 | 新規ツール |
|---|---|---|
| G1 ジョブ定義の手書き埋め込み | §4.3 ジョブ仕様 mine-job/v1 + §4.2 述語台帳 | なし(自前 JSON) |
| G2 対付けが暗黙 | §4.2 pairs(explorer⟷checker 欄の必須化)+ §4.6 collector の自動対付け | なし |
| G3 手動 dispatch | §4.5 統一配車(mb-search 型の一般化) | なし |
| G4 記帳が手動 | §4.6 collector(artifact→LEDGER 行・地図 delta 案の生成) | なし |
| G5 解数勘定が単系統 | T3 に #SAT の独立第二系統 | **ganak**(MIT) |
| G6 SAT 条件追加 = encoder 書き直し | §4.4 fragment 化 + incremental | **CaDiCaL 2.x**(MIT) |
| G7 検証済み checker 不在 | 三系統目の checker | **cake_lpr**(検証済みバイナリ) |
| G8 キャッシュ不在 | §4.7 certs メモ化(canonical UID 鍵) | なし(既存 UID) |

**採用(新規 4 つ)**: CaDiCaL 2.x・cake_lpr・ganak・Vole(v3・CI 専)。
**維持**: GAP 4.16.0 生態系(+眠っている ferret/orb/genss の起用)・kissat(pin 継続 — CaDiCaL とのポートフォリオ)・drat-trim・sympy/node 照合器群・bliss。
**落選(主要)**: Magma(§2.9)・mallob/Paracooba(GHA 不適合)・Z3(証明弱)・OR-Tools/MiniZinc(証明なし)・mace4 系(被覆済み)・d4(競技で敗退)・IsaSAT(checker 側検証で足る)。
**将来枠(装置提案)**: SMS・cvc5+Ethos/Lean-SMT・VeriPB+CakePB・PBLean・TabularAllSAT・sharpSAT-TD。

---

# §4 アーキテクチャ設計 — 採掘場(mine)

命名: 地図文化(帯・採掘・封緘)に合わせ、リポジトリ内の新設面を `mine/` と呼ぶ(仮称・裁定で変更可)。

## 4.0 全体図

```
 述語台帳 registry ──┐
                     ▼
 ジョブ仕様 plan ──► preflight ──► [push] ──► 統一配車 CI(mine-dispatch)
 (宇宙の事前登録)   (機械検査)              │ validate → integrity gate → 予言ゲート
                                            ▼
                              backend 分岐: gap-ci / sat-ci / py-ci
                                            │ shard matrix(≤256)・timeout・checkpoint
                                            ▼
                              artifact(certs JSON + result.txt + SHA256SUMS)
                                            ▼
 collector(検収)◄─────────────────────────┘
   │ 対付け照合(explorer⟷checker 両系統が揃ったか)
   │ 予言照合(prediction-first)・NULL 発火判定
   ├─► 検収レポート(機械生成)─► 司令塔・研究者(裁定は人間)
   ├─► LEDGER 追記行+地図 delta 案(機械生成・貼るのは人)
   └─► certs キャッシュ索引の更新
```

**設計原理**: 探索の数学(述語の中身)と、探索の工程(配車・分割・収蔵・照合)を物理で分離する。工程は本基盤が持ち、数学は述語カードと encoder fragment だけが持つ。**「新しい事実」は必ずカード 1 枚の形で入ってくる**ので、手直しはカードの追加で閉じる。

## 4.1 統一面その 0 — 語彙

- **窓(window)**: 現行どおり。ID は現行規約(W-D-A16-11a 等)+ canonical UID(bliss 正準形)。
- **述語(predicate)**: 窓(または窓+パラメータ)を入力に、値・真偽・集合を返す判定/測定の単位。例: (F2)・settled・ker χ̃ 位数・PRUNE 律・Ree 篩・dl 計算・ε 判定。
- **ジョブ(job)**: 宇宙 × 述語列 × 資源 × 予言 × 出力スキーマの束(= 事前登録の機械化)。
- **claim_class**: `exploration`(候補発見・バグ許容・速い)/`negative-claim`(登録レジーム — 宇宙 sha 焼き込み・fail-closed・証明証書必須)。ソルバー哲学(2026-07-29 裁定)の機械化。

## 4.2 統一面その 1 — 述語台帳(条件レジストリ)`mine/registry/`

**核心。** 1 述語 = 1 カード(JSON)。必須欄は 6 つだけに絞る(官僚化の防止):

```json
{
  "id": "PRUNE-ODD", "version": 2,
  "statement": "odd(|ker chi~|) = 5^{s2(r)}(D 型窓・出典: 裁定233 SOL87-FIX)",
  "explorer": {"lang": "gap", "file": "search/kerchi-judge.g", "symbol": "…", "impl_sha256": "…"},
  "checker":  {"lang": "python", "file": "search/ladder-xi-recheck.py", "symbol": "…", "impl_sha256": "…"},
  "fixtures": ["search/certs/…(正例)", "…(負例)", "…(adversarial)"],
  "scope": "D 型窓・r≤4 実測済/r≥5 UNKNOWN",
  "map_ref": {"polestar": "P3", "band": 1}
}
```

規律との接続(ここが要):

- **checker 欄が空のカードは合法**だが、そのカードだけで出た結果は collector が**自動で candidate 止まりにラベル**する(cross-checked 昇格には checker 欄+両系統 cert が必要)。→ 探索器/照合器分離が「規範」から「機構」になる。
- fixtures は positive/negative/adversarial の三分(既存規律)をそのまま欄にする。カード追加時に fixture が無ければ preflight が拒否。
- **述語の追加は数学の行為**なので、カードの起草 = 数学者・レビュー = 司令塔・(定理級は)Sol ゲート、という既存のルール文書三段(memory: commander-reviews-rules)に従う。実行係はカードを書けない(§5)。
- 既存資産の棚入れ: kerchi-judge.g の (F2)/settled/Ξ 走査・Ree 篩(ree.g)・パリティ勘定(r4)・PRUNE/Cyc/Tail 律・KERNEL-DL3 前件などを 10〜15 枚のカードに写す(v1 工程)。**GAP コードの改変はしない** — カードは既存関数への「名前付きポインタ+較正 fixture+対付け」であり、まず台帳が実装を指す形から始める(実装のモジュール分割は後続・§7-2)。

**「新しい律が出たら」の手順(これが依頼の核心の答え)**: ①カード 1 枚起草 ②fixture cert を 1〜3 個指名 ③(あれば)checker 実装を対に書く ④既存ジョブテンプレの `pipeline` 配列に `{"predicate": "NEW-LAW", "version": 1}` を 1 行足す — 以上。driver の新造も CI の変更も不要。

## 4.3 統一面その 2 — ジョブ仕様 `mine-job/v1``mine/jobs/`

宇宙の事前登録を機械可読にしたもの。r4 cert の段構造・mb-shard-plan・SAT manifest の三既存様式の統合:

```json
{
  "schema": "mine-job/v1",
  "job_id": "ladder-9t5-20260801",
  "claim_class": "exploration",
  "map_ref": {"polestar": ["P3"], "band": 1},
  "universe": {
    "generator": "ladder-family",
    "params": {"N_ord": 9, "t": [5, 6], "sibling_scan": true},
    "frozen_docs": [{"path": "docs/notes/…", "sha256": "…"}]
  },
  "pipeline": [
    {"predicate": "F2", "version": 3},
    {"predicate": "SETTLED", "version": 2},
    {"predicate": "XI-SCAN", "version": 1, "params": {"mode": "xi_restricted"}},
    {"predicate": "PRUNE-ODD", "version": 2}
  ],
  "predictions": {"frozen": "docs/notes/…_prediction.md", "sha256": "…"},
  "resources": {"backend": "gap-ci", "shards": "auto-by-window", "timeout_min": 60, "checkpoint": true},
  "outputs": {"cert_schema": "…/v1", "out_dir": "search/certs"},
  "crosscheck": {"mode": "auto-pair", "checker_backend": "py-ci"},
  "ep_handoff": null
}
```

- `universe.generator` は少数の登録制(`lins-band` / `ladder-family` / `cell-family(n,ℓ,r,t)` / `direct-windows(ID 列挙)` / `cnf-manifest`)。**位数・生成系を動かす変更 = generator params の変更 = 事前登録の変更**なので、plan の diff がそのまま停止ゲート審査の対象物になる(宇宙変更が「コード改変」でなく「登録変更」として可視化される)。
- `predictions`: 非空か、または `{"declared_none": "理由"}` の明示宣言が必須(preflight が強制)。prediction-first の機械化。
- `claim_class: negative-claim` の場合の追加必須欄: `universe.sha256`(cert へ焼き込み)・`proof_artifacts: ["drat","lrat"]`・`mutants: {...}`・fail-closed 検査群の指名。sat-run.yml の run_label=theorem ゲートの一般化。

## 4.4 SAT 線の「条件追加」= fragment 化 + incremental

- 現行 encoder の `clause_groups`(§1.3)を **fragment モジュール**(群公理 fragment・対合型 fragment・b³=1 fragment・BFS 可達 fragment・新条件 fragment…)に分割し、manifest には fragment 合成列と各 fragment の sha256 を記す。**新しい非存在条件 = fragment を 1 個書いて合成列に足す**。encoder 全体の書き直しを廃止。
- **incremental 経路(CaDiCaL iCNF)**: 条件は**追加(節の追加)は安い・削除は不可**(削除は fresh 再走)。「基底 CNF を solve → 新律を fragment で追加 → 同じ solver 状態で再 solve」が回る。LPAR24 の incremental 証明を添える。**assumption 方式**(条件リテラルで条件の on/off)も fragment 側で選択可にし、「条件の組み合わせ探索」(どの律が締めているか = 独立性検査)に使う。
- 検証は三段: drat-trim(現用)→ lrat_check.py(自前・現用)→ **cake_lpr(形式検証済・新規)**。theorem 級 UNSAT は三段全通過を検収基準にする。completeness 補題(encoder の忠実性の紙側)は現行どおり数学者供給(SAT-COMP-21 の型)で、manifest の audit_status 欄が紙補題の文書 sha を指す。
- **解数勘定(T3)**: GAP 軌道法(現用)⟷ **ganak projected count(新規)** の二系統一致で cross-checked。ganak は証明を出さないので、**解 0 の主張だけは必ず SAT UNSAT(証明つき)経路に回す**、を collector が機械強制(count=0 の ganak cert 単独では candidate 止まり)。

## 4.5 統一面その 3 — 統一配車 CI `mine-dispatch.yml`

mb-search.yml の一般化(新造ではなく複製改造):

1. **発火**: `mine/jobs/queue/*.json` の push(workflow_dispatch も残す)。
2. **validate**: mine-job/v1 schema 検査(mb-plan-validate.mjs の拡張)。
3. **integrity gate**: frozen_docs・述語カードの impl_sha256・encoder fragment sha を plan 記載値と照合(mb-plan-integrity-check.mjs の拡張)。**探索実装が plan 凍結時から 1 バイトでも変わっていれば発車しない**。
4. **予言ゲート**: predictions 欄の検査(§4.3)。
5. **backend 分岐**: `gap-ci`(gap-run 型 step・setup-gap・-o 12g)/`sat-ci`(sat-run 型 step・pin ビルド+CaDiCaL)/`py-ci`(照合器用 python/node)。既存 3 workflow は下請け step 化して温存(URL・run 番号の記録型は不変)。
6. **shard matrix**: es7_sat_matrix 型(≤256・offset/count)+ gap 側は preamble 注入(SHARD 変数)を流用。checkpoint 欄が true なら中断 job の再開入力に checkpoint cert を許す(既存 .checkpoint JSON 型)。
7. **収蔵**: artifact = certs + result.txt + SHA256SUMS(machine-piped: collector は artifact のみ読む・ログ grep 禁止を機構で強制 — collector に log reader を実装しない)。

## 4.6 collector(検収の機械化)`mine/collector/collect.py`

- 入力: run の artifact 一式+plan+registry。出力: **検収レポート**(機械生成 md)・LEDGER 追記行(貼るのは人)・地図 delta 案(map_ref 欄から・裁定番号は空欄で人が埋める)。
- **自動対付け**: plan の pipeline 各述語につき、explorer cert と checker cert の対応(窓 UID × 述語 id × version で突合)を照合し、`agreement: 13/13` 型の集計を出す。**片系統しか無い項目は candidate、両系統一致は cross-checked 候補**(最終昇格の裁定は人)。
- **NULL/予言照合**: predictions の凍結値と実測を突合し、的中/外れ/NULL 発火を機械判定(判定の意味づけは人)。

## 4.7 certs メモ化(差分実行)

- 索引: `(canonical_uid, predicate_id, predicate_version, impl_sha256) → cert パス`。collector が certs 132 個から初期索引を構築。
- ジョブ発車時、pipeline の各 (窓, 述語) で索引に既存 cert があれば**スキップし cert 参照を出力に併記**(再計算は `force: true` でのみ)。→ **「新しい律を全既知窓に当てる」ジョブが、新述語 1 個分の計算だけで済む**。impl_sha256 が鍵に入っているので、実装が変われば自動でキャッシュ無効(§7-3 の事故対策)。

## 4.8 既存規律との互換表

| 不変条件 | 本設計での担保 |
|---|---|
| 探索器と照合器の分離・verified は Lean 専用 | カードの explorer/checker 二欄+collector の自動ラベル(§4.2/4.6)。verified の語は本基盤のどの出力にも現れない(Lean 線は別 workflow のまま) |
| ソルバー哲学(候補発見はバグ許容・陰性のみ登録レジーム) | claim_class 二値(§4.1)。negative-claim だけ重装備(§4.3)。exploration は preflight 最小で速く回す |
| 宇宙の事前登録・UNKNOWN 一級 | universe 欄+integrity gate(§4.3/4.5)。UNKNOWN は cert の一級値(現行どおり)で、collector が UNKNOWN を成果として集計 |
| prediction-first | 予言ゲート(§4.3)。宣言なしは発車不可 |
| machine-piped | collector が artifact のみ読む(§4.5-7)。LEDGER 行・レポートは機械生成 |
| MB whitelist・封印・blind | 封印 payload は金庫(リポ外)のまま — 本基盤は触れない。blind 進行ジョブは predictions を封印 sha 参照(値でなくハッシュ)で持つ(PSL 7 窓封印の既存様式) |
| 文献ゲート | 本基盤は外部論文を読まない。§2 は工程ツールの調査であり数学文献ではない(数学的機構の輸入が要る時は paper-hunter 経路) |

---

# §5 運用設計 — 専任実行係への引き渡し面

前提: 研究者は「探索の実行者に専任を付ける」。実行係(miner 係と仮称)は**判定ロジック・述語カード・registry に触れない**(mb-search.yml 冒頭の原則「探索器の判定ロジックには一切触れない」の人員版)。

## 5.1 職務境界

| 行為 | 実行係 | 司令塔/数学者 |
|---|---|---|
| ジョブ plan の起票(テンプレから params を埋める) | ○ | 承認(negative-claim は必須承認) |
| preflight・発車(push)・監視・再開(checkpoint) | ○ | — |
| collector 実行・検収レポート提出 | ○ | レポートを受けて裁定 |
| 述語カードの追加・改版 / universe generator の追加 | × | ○(三段レビュー) |
| 予言の作成・封印 | × | ○ |
| LEDGER・地図への貼り付け | ×(行の生成まで) | ○(貼付と裁定) |

## 5.2 引き渡し物(実行係が受け取る 4 点)

1. **ジョブテンプレ 5 型**(`mine/jobs/templates/`): census 型(T1)・ladder 型(T2)・cell 型(T3)・sat 型(T4)・band 型(T5)。各テンプレは params の穴埋め箇所と、埋めてよい欄/触ってはならない欄の注記つき。
2. **起動手順書**(3 コマンド以内): ①`python mine/preflight.py jobs/queue/X.json`(schema・integrity・予言ゲートのローカル前哨)②`git push`(発車)③完走後 `python mine/collector/collect.py --run <run_id>`。
3. **検収チェックリスト**: all_pass の確認は result.txt/certs のみから(ログ閲覧は診断用で判定に使わない)・SHA256SUMS 照合・予言照合欄の確認・**FAIL/NULL 発火時は手を入れず司令塔へエスカレーション**(実行係による再走 retry は同一 plan の再発車のみ許可)。
4. **禁止事項票**: registry 改変禁止・plan の universe/pipeline/predictions 欄の実行係による書き換え禁止(params の指定範囲のみ可)・封印関連欄の閲覧禁止。

## 5.3 司令塔側の検収基準(collector レポートの読み方)

- `agreement` が全項目一致 → cross-checked 候補として裁定へ。片系統 → candidate(自動ラベル済み)。
- `prediction` 欄: 的中/外れ/NULL。外れは負の結果として地図 delta 案に自動反映(裁定で確定)。
- negative-claim: 三段 checker(drat-trim・lrat_check・cake_lpr)全通過+mutant matrix 全緑+宇宙 sha 一致、が昇格の必要条件。

---

# §6 導入ロードマップ

## v0 — 最小再配線(工数感: 2〜4 日・新造コードは schema/preflight/collector 最小の 3 本)

1. `mine-dispatch.yml` を mb-search.yml の複製改造で作る(validate/integrity/matrix は流用・backend 分岐 gap-ci のみ)。
2. mine-job/v1 schema+preflight(ben_preflight.py の型を流用)。
3. collector 最小(検収レポートと対付け集計のみ。LEDGER 行生成は v1)。
4. **第一号ジョブ = 梯子走査(T2)**。

**第一号に梯子走査を指名する理由**(候補比較):

| 候補 | 判定 | 理由 |
|---|---|---|
| **梯子走査** | **◎ v0** | (a) 探索器(kerchi-judge Ξ 走査)と照合器(ladder-xi-recheck.py)の**両系統が完成済み**で、自動対付け(§4.6)まで含む full pipeline を初回から実証できる。(b) 窓単位の shard が自然(13 窓実績)。(c) prediction-first の実績(17/17・裁定 213)があり検収基準が既に明文。(d) **次の実弾がすべて同型**: N_ord=9 の t=5,6 延長・兄弟窓・q=7 の u 測定(梯子型の窓走査)・S>D₈ 窓ハント(P-EPS-5′ 判定)。載せ替えの投資が即、次弾で回収される |
| r=4 セル悉皆 | ○ v0.5 | 現在進行形(B 枝 ε=1・S₂₀ が未着で丁度よい)だが、照合器の第二系統(ganak か GAP 内独立実装)が未整備なので、v0 の「対付け実証」に使えない。**v2 の ganak 導入と同時に載せると二系統が初めて揃う** — B 枝を ganak 導入の初弾に指名 |
| 帯採掘 | ○ v1 デモ | 単発 LINS+述語列挙で構造が最も単純。**v1 の述語差し替えデモに最適**: 裁定 225 の (192,360] 帯ジョブを plan 化 → 「>360 帯」へ params 変更だけで発車 → さらに KERNEL-DL3 前件カード(dl≥3 篩)を pipeline に 1 行足して P4(壁・最大空白)の dl-3 核ハントへ — **「条件を追加するだけ」の初の実演をここでやる** |

## v1 — 述語台帳(工数感: 1〜2 週)

- 既存述語 10〜15 枚の棚入れ(カード化・fixture 指名・pairs)。kerchi-judge.g のコード改変はしない(カードは既存関数を指す)。
- certs メモ化索引(§4.7)・LEDGER 行/地図 delta 案の生成(§4.6)。
- 帯採掘デモ(上表)。**v1 完了の受け入れ試験 = 「新律カード 1 枚追加 → 既知 16 標本への適用ジョブが driver 新造ゼロで走る」**。

## v2 — SAT 線統合(工数感: 1〜2 週)

- encoder fragment 化(clause_groups 単位の分割)・CaDiCaL 2.x 導入(LRAT native・iCNF/assumption)・cake_lpr を三段目 checker に・cube-and-conquer shard(march_cu → matrix)。
- ganak 導入(T3 第二系統)。初弾 = r=4 B 枝(上表)・r=5 の 5^{s₂(r)} 律検証(P3 進捗指標)。
- SAT-L1(飽和逆包含・P3 の残)と n=25 存在判定(裁定 210 の Sol 攻め順③)をこの基盤の sat 型ジョブとして定義。

## v3 以降 — 拡張(必要駆動)

- Vole(CI 専・canonical 第二系統+normalizer 高速化 — P3 の正規化群実測の大規模化)・SMS(S>D₈ 窓ハントの候補発見器)・cvc5/PBLean(Lean 昇格路)・orb/genss の起用(Ξ 10⁸ 級のローカル分散)。

---

# §7 破綻しそうな点(自己監査 — 一番怪しい所から)

1. **官僚化リスク(最大)**: 述語台帳が「書くのが重い管理面」になり、探索の速度(工房の強み: 裁定 235 の r=4 は依頼から当日完走)を殺す危険。対策 = カード必須欄 6 個限定・exploration ジョブの preflight は schema 検査のみ・**「カード化は走った後でよい」**(初回は direct-windows + 生 driver で走り、昇格したくなった時に棚入れ)を明文で許す。
2. **kerchi-judge.g の密結合**: 述語を「名前で呼べる単位」に切り出す時、MakeWindow の内部状態共有と衝突しうる。v1 では**切り出さない**(カードは関数ポインタ+fixture)と決めたが、いずれ必要になるモジュール分割は判定ロジックに触る作業なので、v13-calibration 型の較正回帰を義務にする — それでも regression fixture の網羅漏れが単一の最大事故点。
3. **キャッシュ事故**: (UID, 述語, 版) 鍵は「実装を変えたのに版を上げ忘れ」で腐る。impl_sha256 を鍵に含めて機械側で防ぐが、**GAP の Read 連鎖(gaplib_common.g 等の依存先変更)は単一ファイル sha では捕まらない**。対策 = 依存ファイル列の連結 sha をカードに持つ(preflight が計算)。それでも GAP 本体の版上げは全キャッシュ無効化で対応するしかない。
4. **incremental の片道性**: 節の追加はできるが削除はできない(条件の緩和 = fresh 再走)。「律の候補を外す」実験が多い時期には incremental の利得が消える。assumption 方式(on/off リテラル)で緩和できるが、assumption だらけの CNF は求解が遅くなる — どちらが得かは較正(v2 で n=21 を両方式で測る)まで不明。
5. **ganak の証明レス**: 解数の cross-check は「二系統一致」どまりで、一致しても両方間違う余地は残る(特に projection の指定ミスは両系統に同時混入しうる — 射影変数リストは manifest で一元管理し fixture で較正する)。
6. **GHA の物理制約**: per-job 6h・matrix 256・public repo 前提の無制限。Ξ=4.5×10⁸ 級(r=4 可能圏)は shard 設計が本体で、本基盤は配車を楽にするだけで**計算量そのものは減らさない**(減らすのは数学 = PRUNE 律のような刈り込みの発見)。基盤に過度の期待を載せない。
7. **過渡期の二重構造**: mine/ と search/ が並立する期間、「どちらが正か」の混乱が起きうる。対策 = mine/ は**配車と台帳だけ**を持ち、実装(.g/.py)と certs は search/ に置いたまま動かさない(パス不変・移動ゼロ)。
8. **EP との境界**: ep_handoff を「予約」に留めたが、EP v7 発効後に schema の版整合(cert_schema 欄)で揉める可能性。予約欄に EP 側 schema 版の pin 欄を含めておく。

---

# 付録 A 出典一覧(外部調査・アクセス日 2026-07-30)

- SAT Competition 2025 結果: https://satcompetition.github.io/2025/satcomp25slides.pdf / Biere 系ソルバー記述: https://cca.informatik.uni-freiburg.de/papers/BiereFallerFleuryFroleyksPollitt-SAT-Competition-2025-solvers.pdf
- kissat: https://github.com/arminbiere/kissat
- CaDiCaL 2.0(CAV 2024): https://cca.informatik.uni-freiburg.de/papers/BiereFallerFazekasFleuryFroleyksPollitt-CAV24-Springer.pdf / Certifying Incremental SAT Solving(LPAR 2024): https://cca.informatik.uni-freiburg.de/papers/FazekasPollittFleuryBiere-LPAR24.pdf
- cake_lpr(検証済み LRAT/LPR checker): https://github.com/tanyongkiam/cake_lpr / SAT Comp 2025 checker 文書: https://satcompetition.github.io/2025/downloads/checkers/cakelpr.pdf / TACAS 2021 論文: https://cakeml.org/tacas21.pdf
- VeriPB: https://github.com/StephanGocht/VeriPB / SAT Comp 2025 文書(CakePB 含む): https://satcompetition.github.io/2025/downloads/checkers/veripb.pdf / 証明つき PB 最適化(CP 2025): https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2025.21 / 対称性破りの高速証明(2025): https://arxiv.org/pdf/2511.16637
- PBLean(PB 証明書の Lean 4 checker): https://arxiv.org/pdf/2602.08692
- ganak(2024/2025 Model Counting Comp 全冠・MIT): https://github.com/meelgroup/ganak / 実装論文(SAT 2025): https://link.springer.com/content/pdf/10.1007/978-3-031-98682-6_5.pdf
- sharpSAT-TD: https://arxiv.org/pdf/2308.15819 / Model Counting Competitions 2021-2023 総括: https://arxiv.org/pdf/2504.13842
- TabularAllSAT(AIJ 2025・blocking clause なし列挙): https://cca.informatik.uni-freiburg.de/papers/SpallittaSebastianiBiere-AIJ25.pdf / arXiv: https://arxiv.org/abs/2410.18707
- Cube-and-Conquer(CnC): https://github.com/marijnheule/CnC / Paracooba(SAT 2020): https://fmv.jku.at/papers/HeisingerFleuryBiere-SAT20.pdf / Smart Cubing for Graph Search(2025): https://arxiv.org/pdf/2501.17201 / D-Painless(2025): https://www.researchgate.net/publication/391418351_D-Painless_A_Framework_for_Distributed_Portfolio_SAT_Solving
- SAT Modulo Symmetries: https://sat-modulo-symmetries.readthedocs.io/en/latest/ / TOCL 2024: https://dl.acm.org/doi/10.1145/3670405 / 専用 propagator(CP 2025): https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2025.39
- cvc5 CPC/Ethos: https://cvc5.github.io/docs/cvc5-1.2.0/proofs/output_cpc.html / Lean-SMT(CAV 2025): https://arxiv.org/pdf/2505.15796
- Vole(GAP・Rust graph backtracking): https://peal.github.io/vole/doc/chap1.html / https://github.com/peal/vole / canonical image 論文: https://arxiv.org/pdf/2209.02534
- ferret(GAP): https://gap-packages.github.io/ferret/
- nauty/Traces(2.9.3・2026-01): https://pallini.di.uniroma1.it/
- MACE4/SEM 比較: https://link.springer.com/chapter/10.1007/978-3-642-36675-8_5

(手元資産の記述は全て実ファイル確認による — §1 に列挙したパスが一次出所。)
