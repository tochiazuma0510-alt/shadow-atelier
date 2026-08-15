# Luna reply 148 — D972 relative-extension dovetail

## §0 — 結論・成果物

最終判定は **`BLOCKED_RELATIVE_EXTENSION_ENUMERATOR`** である。致命的 subcode は
```
NONCHECKPOINTABLE_EXTENSION_CELL
```
であり、実装された blocker receipt は `workflow_resumable:false`、
`liveness_status:"BLOCKED_NONCHECKPOINTABLE_EXTENSION_CELL"` を返す。有限な一セルを最後まで走らせた場合の数学的な全列挙設計は入ったが、そのセル内部を watchdog 境界で永続化して再開する仕組みがないため、(k=3,4,\ldots) の無期限 dovetail としては complete ではない。

作成・更新された成果物と現在の SHA-256 は次の通り。

| path | SHA-256 |
|---|---|
| `search/d972_dovetail_producer_v1.py` | `1243f3646fc05cc9ea9f5bf00ff92c0c6c6d82b4ae6b81c57a4fcab874638ac0` |
| `search/d972_dovetail_worker_v1.g` | `323d18de4fadcf4561222995f5b6590bb560cd617048d2e9b54049ae3eea9efd` |
| `search/check_d972_dovetail_v1.py` | `d2e398ebdc4333a04b726cf8fa68b76e1815c6d15a1db4e14b53fcd3511388a0` |
| `search/d972_dovetail_state_schema_v1.json` | `6b693fde5236216d0839396e19e22b168da81399788c5e4190d29b99d9d6571a` |
| `search/d972_dovetail_manifest_v1.json` | `aefba2279d291e63caef56e7c270d3d58a6a3aacbbd9801dbfb6fce0136137be` |
| `.github/workflows/d972-dovetail.yml` | `21127ce22024310b6272bfd581c7362d959d3303eccab86bdb88168c9cc5c9c2` |
| `search/fixtures/d972_dovetail_v1/README.md` | `8b0ebb27ecedb90d5b412cff7860ade9e658a60056aba33c58a6555d7970c097` |
| `search/fixtures/d972_dovetail_v1/negative_witness_mutations.json` | `261b3edc86e484de753af1b47977a473c2c36df2331317fc03ce5ff7b1225e9e` |
| `search/fixtures/d972_dovetail_v1/negative_state_mutations.json` | `dfb8030c37a0dac7093c8b177ead5e7d48e610fdd497cbac6c41d2168141dd82` |
| `search/fixtures/d972_dovetail_v1/intentional_interrupt_resume.json` | `394fdfbd310197464eab50f3e89990dc05468798aa00f76b707f8749406fe9ed` |

これらの実装ファイルは現在の worktree では未追跡である。本便では commit、push、workflow dispatch を行っていない。

## §1 — HEAD と anchor audit

作業開始時 HEAD は `9799237e31d12a4c35029604e26d7afa8703dcc5`、現在の HEAD は
`450ac2c064943ad493721a34b24f37880100e91e` である。後者への移動は同じ共有 worktree 上の司令塔側変更であり、本便で履歴操作はしていない。

| anchor | SHA-256 | 判定 |
|---|---|---|
| `ops/inbox_codex/sol_task_148_dovetail.txt` | `8890c29cf3c399da863e6705f3ccc434164c1c233ff82f648b965f99612e71f9` | MATCH |
| `docs/week1-定義ノート.md` | `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c` | MATCH |
| `docs/notes/d972_phase2_cofinal_execution_v1.md` | `97998cac97611f10065b463efa8a417d5da200b23dd39ca7a8b2beed32de847e` | MATCH |
| `docs/notes/triad972_canonical_addendum_v2.md` | `5dc660dd0023bf9b1986cefa65ec9947ad5b3b366f210933dbe09ac2544c7659` | MATCH |
| `sol/sol_reply_143_typedfiber.md` | `ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a` | MATCH |
| `search/certs/nf972_sourcemap_a_v3_20260804.json` | `32e268c97c77446b85787c5d7750da758df67646de414eade709ca79baf98b37` | MATCH |
| `search/certs/nf972_sourcemap_b_v6_20260804.json` | `e27a71fbf00295be9a74761ef11134e3a8f324ed57f523d11d44a67fb5a207de` | MATCH |

## §2 — 一セルの exact design と completeness 境界

worker は (\bar Q=B_3/M) を K9、PSL(2,8)、次数 20,520 の直積作用から再構築し、
`|barQ|=8,817,984`、`|PB3/M|=1,469,664`、`M_ord=18` を exact gate にする。
`IsomorphismFpGroupByGenerators` により marked two-generator presentation も作る。

固定された labelled kernel (H) の一セルでは、次を有限全探索する。

1. SmallGroups 利用可能時の全群、および正規化 Cayley table fallback（非可換群を除外しない）。
2. `Aut(H)^2`、全 base-relator defect tuple、全 (H^2) marked lift pair。
3. Cayley、共役、relator を含む defect presentation、MTC embedding/order、factor map、braid、generation、epsilon の pure-order gate。
4. base を固定し marked pair を保存する双方向 bijection による重複判定。unmarked SmallGroup ID は同値判定に用いない。
5. outer bucket は索引だけで、候補を prune しない。

order receipt の意味は `extension_order=full_b3_quotient_order=k*8,817,984`、
`pure_extension_order=k*1,469,664`、`pure_base_order=1,469,664` である。

ただし `canonical_table_relabel_enumeration`、`automorphism_enumeration`、
`presentation_subgroup_mtc_and_fp_order`、
`shadow_derived_elements_and_full_pair_scan` はセル途中の永続 cursor を持たない。
このため「各セルが返れば有限範囲を尽くす」と「watchdog-safe な無期限 dovetail」は別であり、後者は未達である。

## §3 — producer、分類 journal、cursor

producer は state/input/code SHA、canonical JSON checkpoint hash、親 hash、単調 cursor を fail-closed に扱う。
kernel table fallback は全正規化 Latin table を列挙し、同型分類の完全な representative/duplicate journal を
`producer-classification-ledger.jsonl` に残す。ledger path は artifact-relative で固定した。

raw relative-extension candidate は `RAW_RELATIVE_EXTENSION_ONLY`、
`ready_for_producer_ledger:false` とし、terminal な shadow/fiber PASS より前に producer ledger へ入らない。
分類 receipt が complete でなければ `k_closed=true` にできない。今回の blocker では engine status を
`BLOCKED` とし、cursor は進めない。

producer の自己検査は PASS し、要点は
`target_keys=972`、target digest
`9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62`、
`fallback_k4_raw=216`、`fallback_k4_groups=2`、
`classification_chain_rows=2`、`cursor_unchanged=true`、
`raw_shadow_ledger_order=true`、`portable_paths=true` であった。
Python compile/help も PASS した。

## §4 — shadow/fiber stage

各 accepted extension について worker は full (P=B_3/L) と faithful permutation model を再構築し、
derived subgroup 内の charming (m,f) を全走査する。論文 (3.3)、(3.4) は `AbstractProd` による literal
full-(B_3) equation、surjectivity、marked endomorphism の bijectivity による settlement、exact source
kernel を gate にする。(c\notin L) の場合にも theta/tau shortcut は使わない。

出力は canonical NF972 reduction、972 target vector、zero-key set、各 digest を含む。raw extension と
shadow-classification の二段 ledger 順序を強制する設計である。ただし GAP campaign 自体は起動できなかったため、
実候補の 972-vector、empty fiber、A-side witness、B-side liftはいずれも得ていない。

## §5 — independent checker

Python checker は producer/worker を import せず、生成する GAP checker も `Read(...)` を一切使わない。
`gaplib_common`、`week3-battery-common`、`week3-psl-common` と共有せず、固定 base marking、
six-coset rule、D9 serializer、paper-product evaluator を checker 内に独立実装した。paper word は逆順に
GAP 積へ写し、GAP ExtRep の signed word だけは自然順に評価する。

checker は Cayley/Aut/relator/lift/factor map、full (P/Q)、literal hexagon、surjectivity、
Cayley image と Schreier index の settlement、source kernel、target/fiber/zero set を witness から再構築する。
duplicate link も両 fp group と marked-pair bijection を再構築する。共有 helper の静的走査は PASS した。

`python -B -m py_compile` と `--self-test` は PASS。self-test は
`negative_cases=11`、`intentional_interrupt_hash_transition=PASS`、
`semantic_key_missing=0`、`semantic_key_duplicates_after_resume=0`、
`parent_hash_match=true` を返した。ただし自己検査自身が示す通り
`campaign_full_p_backend=REQUIRED_OUTSIDE_PARSE_ONLY_SELFTEST` であり、実 GAP campaign の独立照合は未実行である。
従って `cross_checked=false` である。

## §6 — calibration、negative tests、terminal gate

k=1/k=2 の数値は manifest の**期待値**であり、観測 raw receipt ではない。

| calibration | 登録モデル | 期待値（未観測） |
|---|---:|---|
| k=1 | 1 | GT 972、image 972、zero 0、histogram (1\times972) |
| k=2 | 3 | GT ([972,1944,1944])、image は全て 972、zero は全て 0、histogram ([1\times972,2\times972,2\times972]) |

k=2 は split と二つの nonsplit (Q_8) model、および全 8 個の
(H^2(V_4,\mathbf F_2)) coefficient triple を走査するコードを持つ。一方、三モデルが universe を尽くす根拠は
pinned `sol_reply_143` §5.4 の前提を使っており、独立な model-universe 証明ではない。receipt は
`independent_model_universe_proof:false`、`calibration_unlock_authority:false` とし、checker は
`INDEPENDENT_CALIBRATION_WITNESS_NOT_FROZEN` により calibration を FAILED、`search_unlocked=false` に固定する。

negative fixture は witness mutation 8件（factor map、kernel、braid、word level、settlement、m modulus、
fiber row、relator shape）と state mutation 3件（parent hash、sequence gap、duplicate semantic key）の計11件で、
self-test は 11/11 を拒否した。intentional interrupt/resume fixture は親 hash、sequence +1、cursor 保存、
semantic key の欠落0・重複0を通過した。parse-only fixture は campaign ledger に昇格できない。

従って `A_WITNESS_CROSSCHECKED` は発行していない。A、B、genuine refinement、dihedral/non-dihedral の
いずれの結論も主張しない。Lean 証明書もなく、`verified=false` である。

## §7 — workflow と二-run provenance

workflow は dispatch と schedule、固定 concurrency（`cancel-in-progress:false`）、300分 watchdog、
read-only permissions、単一 predecessor artifact、schema/input/code digest、三 ledger の exact restore、
emergency artifact、terminal no-op を実装する。manifest の seed checkpoint
`06d33ce0184df90add797d8e978bee1c7c2eebb47a75a5cb63c063ed3a491daf` は再計算と一致し、
schema binding、9 input binding、runtime code-set binding も静的検査を通過した。AJV Draft 2020 manifest、
YAML parse、埋込み Python 4 block の compile、fixture JSON、trailing whitespace の各検査は PASS した。

最終 provenance 修正後の focused two-run test も PASS した。RESUME は restored parent の bytes/digest を変更せず、
producer/checker の**新しい transition だけ**に `CURRENT_RUN_ID`、`CURRENT_RUN_ATTEMPT`、
`CURRENT_EVENT`、`CURRENT_COMMIT`、`SOURCE_RUN_ID` を束縛する。各 transition の parent hash は直前 checkpoint
digest、sequence は +1 であり、三つの非空 ledger は二 run 間で byte-for-byte restore された。
既に terminal な入力の no-op は transition を作らず digest を保存する。

これは workflow の局所的な resume/hash-chain 検査であり GitHub-hosted execution ではない。
top blocker のため GHA dispatch request はせず、run ID はない。blocked-only v1 は `COMPLETE` を受理しない。

## §8 — acceptance matrix と実行記録

| # | 受入項目 | 最終結果 |
|---:|---|---|
| 1 | HEAD、7 anchors、変更対象 | **PASS** — §0–§1 に固定 |
| 2 | complete API / nonabelian scope | **FAIL / BLOCKED** — 一セルの有限全探索設計はあるが、要求された checkpointable all-k API は存在しない |
| 3 | canonical dedup / exactly-once / closure gate | **PARTIAL (static/unit)** — marked-over-base 双方向判定、分類 journal、incomplete 時 cursor/closure 不変は実装したが、marked dedup は GAP で未実行 |
| 4 | checker helper independence | **PARTIAL (static/design)** — import/Read/shared GAP helper はないが、独立 backend は GAP で未実行 |
| 5 | k=1,2 raw counts / full histogram | **FAIL (authority)** — 期待値のみ、独立 universe 証明と観測 raw receipt なし、unlock false |
| 6 | negative tests | **PASS** — 11/11 rejection |
| 7 | interrupt/resume、semantic key、current-run provenance | **PARTIAL** — outer 二-run、三 ledger restore、current-run provenance、terminal no-op は PASS。inner-cell checkpoint は FAIL |
| 8 | campaign exit/wall/RSS/disk と数学 receipt | **NOT RUN** — GAP が script load 前に停止 |
| 9 | workflow static/resume audit | **PASS (local only)** — YAML/embedded code/schema/prepare-resume。GHA run なし |
| 10 | terminal A/B decision と git mutation | **BLOCKED** — A/B/genuine の主張なし、commit/push/dispatch なし |

主要な実行結果は以下である。

- producer Python compile/help/self-unit: PASS。
- checker Python compile/self-test: PASS、negative 11/11。
- worker static audit: delimiter/string、45 function/45 end、if/fi、loop/od、ASCII、末尾空白を PASS。
- workflow local audit: AJV、YAML、埋込み Python、二-run restore/hash-chain/current-run provenance を PASS。
- `.\gap.ps1 search\d972_dovetail_worker_v1.g`: exit 1、script load 前に
  `fatal error - couldn't create signal pipe, Win32 error 5`。
- `git diff --check`: repository 全体では既存
  `search/probe/wac_v1/scan_out.txt` 11–15行の末尾空白により exit 2。今回の対象ファイルには新規の whitespace
  diagnostic はない。

GAP worker が一度も起動していないため、calibration raw count、候補 campaign、生成 GAP checker、
wall/RSS/disk receipt は存在しない。最終的に
`workflow_resumable:false` / `NONCHECKPOINTABLE_EXTENSION_CELL` を維持し、
`cross_checked=false`、`verified=false`、A/B 判定なし、GHA runなし、commit/pushなし、と報告する。
