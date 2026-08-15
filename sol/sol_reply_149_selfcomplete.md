# Sol 便 149 返信 — 役割契約改定の適用と便148の自己完結監査

## 0. 結論

研究者裁定を受領し、運用を次のとおり改めた。

- 実装を Luna へ切り出すことは維持する。
- 切り出した後は工房 broker を待たず、Sol が Luna subagent を起動し、返書の受領、欠陥の差戻し、再監査まで管理する。
- Sol 自身は数学判断・設計・敵対的監査を担当し、実装・機械計算・大量整形は Luna に担当させる。

便148についてこの運用を実行した。旧返書の
`IMPLEMENTATION_DISPATCHED_NOT_EXECUTED` は今回の最終状態ではない。Luna の初回返書
`BLOCKED_RELATIVE_EXTENSION_ENUMERATOR`（必要ファイルなし）をそのまま受理せず、producer、GAP worker、
independent checker、state/workflow の各実装を subagent に分担させ、相互の成果を統合し、独立静的監査で見つかった
欠陥を反復修正した。

ただし完成した v1 の正確な最終判定は

```text
BLOCKED_RELATIVE_EXTENSION_ENUMERATOR
subcode: NONCHECKPOINTABLE_EXTENSION_CELL
```

である。これは「実装を投げたまま」の状態ではなく、要求された無期限 dovetail が成立しない構造的理由まで実装・
監査して fail-closed に固定した結果である。A/B の数学的結論、`cross_checked`、`verified` は得ていない。

## 1. 変わる一点への対応 — Luna を起動し、往復を完了した

Sol 側で行った管理は次のとおりである。

1. 既存 `sol/luna_task_148_dovetail.md` と初回 `sol/luna_reply_148_dovetail.md` を受領し、全 §0–§8 を再監査した。
2. Luna を三系統に分け、(a) exact finite-cell GAP worker と統合返書、(b) producer・完全分類 journal・cursor、
   (c) independent checker・schema・fixtures・workflow を並行実装させた。
3. 初回実装に対し、raw candidate を shadow 判定前に ledger へ入れないこと、全 normalized Cayley-table fallback、
   crash/replay-safe classification journal、artifact-relative path、三 ledger の resume を要求して修正させた。
4. worker に対し full/pure order receipt の型、frozen 972-key digest、k=2 較正の論文前提と機械列挙の境界、
   `calibration_unlock_authority:false` を明記させた。
5. 独立監査が検出した checker の論文積順序誤りを差し戻した。checker-local `PaperProd` により
   paper の積を GAP の逆順積へ写し、`c`、(3.3)、(3.4)、`img2` を一貫して修正した。
6. checker が worker と同じ GAP helper を読んでいた独立性欠陥を差し戻した。最終 checker は `Read(...)` を使わず、
   fixed base の lossless permutation、six-coset rules、target normal form、signed-word evaluator を自身で再構成する。
7. 通常 RESUME 後の checkpoint が前 run の metadata を保持する provenance 欠陥を差し戻した。現在は復元 state の
   digest を親として保存し、新しい transition だけに現 run を束縛し、terminal no-op は同一 digest を保つ。
8. 別 Luna による最終静的監査を行い、受入表の過大評価と `git diff --check` の exit code も訂正させた。

最終 Luna 返書は `sol/luna_reply_148_dovetail.md`、SHA-256
`3543aa40845f051dbc9eb826fe9777ef473b2331fa0dec46b12dffb7b844411b` である。旧い「ファイル不在」返書は
上書きされ、現在は実装内容、試験、限界、受入 1–10 を全て収録している。

## 2. 変わらない役割境界

今回も Sol は relative-extension の列挙や GAP campaign を自分で実行・実装していない。数学的対象、完全性条件、
停止線、独立性、格付けを監査し、実装・機械試験・ファイル整形は Luna に行わせた。この分担は
`AGENTS.md` と便149の「Sol に計算をさせない」「判断・設計・監査」の双方に一致する。

Luna が実装した有限セルの設計は、固定 kernel `H` について全 normalized Cayley tables、`Aut(H)^2`、全 relator
defect、全 marked lift、MTC/order/factor/braid/generation gate、base-fixing marked isomorphism dedup を含む。
したがって「一セルが完走した場合」の全探索候補としては substantive である。しかし、そのことを無期限 campaign の
完全性へ昇格させていない。

## 3. 工房の担当と GHA 判断

commit、push、workflow dispatch、GitHub 操作は行っていない。run ID も存在しない。

便149は「A 側 dovetail が動く形になったら GHA 要求を書く」と定めるが、今回はその前件が成立しないため、
**GHA 発火要求を書かない**。形式的な workflow YAML が存在するだけでは「動く形」と判定しない。
工房に残る担当は、将来 blocker が解消された版の GHA 発火・GitHub 操作・commit/freeze・正式検収・格付けである。
本返信の表は Sol の監査台帳であり、工房の最終検収を代行するものではない。

## 4. 便148 Luna 返書の受領結果

作成された主要成果物は次である。

| 成果物 | SHA-256 |
|---|---|
| `search/d972_dovetail_producer_v1.py` | `1243f3646fc05cc9ea9f5bf00ff92c0c6c6d82b4ae6b81c57a4fcab874638ac0` |
| `search/d972_dovetail_worker_v1.g` | `323d18de4fadcf4561222995f5b6590bb560cd617048d2e9b54049ae3eea9efd` |
| `search/check_d972_dovetail_v1.py` | `d2e398ebdc4333a04b726cf8fa68b76e1815c6d15a1db4e14b53fcd3511388a0` |
| `search/d972_dovetail_state_schema_v1.json` | `6b693fde5236216d0839396e19e22b168da81399788c5e4190d29b99d9d6571a` |
| `search/d972_dovetail_manifest_v1.json` | `aefba2279d291e63caef56e7c270d3d58a6a3aacbbd9801dbfb6fce0136137be` |
| `.github/workflows/d972-dovetail.yml` | `21127ce22024310b6272bfd581c7362d959d3303eccab86bdb88168c9cc5c9c2` |

fixtures 四件の hash、全 anchor、開始/現在 HEAD、各試験の詳細は最終 Luna 返書に lossless に記録されている。

実装・静的試験で確認できた範囲は次である。

- producer の target 972 digest、k=4 normalized-table fallback（raw 216、群 2）、classification chain、
  raw→shadow→eligible ledger 順序、cursor 不変、portable path は PASS。
- checker の compile/help/self-test と負試験 11/11 は PASS。producer/worker/shared GAP helper を import/read しない。
- schema/manifest seal、YAML、埋込 Python 4 block、GitHub script、三つの非空 ledger の二-run 復元は PASS。
- provenance 修正後、二 run の producer/checker transition、parent hash、sequence、current-run metadata、ledger binding、
  terminal no-op の focused test は PASS。
- ローカル GAP は worker の load 前に Win32 signal-pipe error 5 で停止した。したがって generated GAP backend、
  k=1/2 raw calibration、候補 campaign、wall/RSS/disk receipt は未実行である。

## 5. blocker の裁定

worker の exact cell には少なくとも次の monolithic stage が残る。

- Cayley table の canonical relabel と automorphism enumeration
- `IsomorphismFpGroupByGenerators`、MTC embedding、fp order
- derived elements と full charming/hexagon/shadow/fiber scan

これらは有限な入力上の候補 algorithm ではあるが、内部状態を artifact に直列化する continuation cursor がない。
workflow の各 run は 300 分 watchdog（job 330 分）で終了する。あるセルの必要時間が 300 分を超える場合、run は
セル開始前 checkpoint へ戻り、次 run も同じセルを最初から再実行する。外側の state/hash/ledger が正しく復元されても、
セル内で仕事が累積しないため、そのセルを永遠に越えない実行があり得る。

従ってこれは要求された fair all-k dovetail／半決定器ではない。`UNKNOWN/RESUME` と称して同じ monolithic cell を
再起動することも、有限 catalog lane を無期限列挙へ昇格させることも認めない。producer が
`workflow_resumable:false` を読み、cursor を進めず
`BLOCKED_RELATIVE_EXTENSION_ENUMERATOR / NONCHECKPOINTABLE_EXTENSION_CELL` で停止するのが正しい。

次版で必要なのは、上記各 stage を有限 cursor へ分解して状態を保存すること、または各 slice の仕事が将来必ず累積する
同値な step-bounded schedule を実装することである。その後に初めて k=1/2 の独立 raw calibration を実行できる。

## 6. 較正・独立性・格付けの停止線

k=1 と k=2 の期待値を hard-code して PASS にすることはしていない。worker は split 一模型と nonsplit 二模型、
および `H^2(V_4,F_2)` の係数を走査するコードを持つが、三 marked orbit が全 universe を尽くす箇所は
`sol_reply_143` §5.4 の pinned premise に依存する。独立な model-universe proof ではないため、receipt は

```text
independent_model_universe_proof:false
calibration_unlock_authority:false
```

であり、checker は `INDEPENDENT_CALIBRATION_WITNESS_NOT_FROZEN` として search unlock を拒否する。

また、checker の独立構造が静的に整ったことと、実候補について producer/checker が一致したことは別である。
後者は GAP 未実行なので `cross_checked=false`。Lean certificate は無いため `verified=false` である。

## 7. Sol 監査台帳（便148受入 1–10）

| # | 項目 | 裁定 |
|---:|---|---|
| 1 | HEAD、anchors、対象ファイル | PASS |
| 2 | complete nonabelian all-k API | **FAIL / BLOCKED** — checkpointable inner iterator がない |
| 3 | marked dedup、exactly-once、closure | PARTIAL — static/unit のみ、GAP campaign 未実行 |
| 4 | helper-independent checker | PARTIAL — static/design は通過、generated GAP backend 未実行 |
| 5 | k=1/2 raw calibration と full histogram | FAIL — raw receipt なし、independent universe authority なし |
| 6 | negative fixtures | PASS — parse/state mutation 11/11 reject |
| 7 | interrupt/resume | PARTIAL — outer hash/三 ledger/provenance は PASS、inner-cell checkpoint は FAIL |
| 8 | campaign command/resource receipt | NOT RUN — GAP host failure、campaign 未開始 |
| 9 | workflow static audit | PASS (local static only) — GHA run ID なし、blocked-only |
| 10 | terminal/math conclusion と git mutation | BLOCKED — A/B 結論なし、commit/push/dispatch なし |

これは candidate implementation の監査であり、数学結果の `cross-checked` や `verified` への格上げではない。

## 8. provenance と最終記帳

| 項目 | 値 |
|---|---|
| 便149 SHA-256 | `436e452518b610048a1bf1569e9a166b01d316140ac22b4c7a523e186f11459f` |
| 現在 HEAD | `450ac2c064943ad493721a34b24f37880100e91e` |
| 最終 Luna 返書 SHA-256 | `3543aa40845f051dbc9eb826fe9777ef473b2331fa0dec46b12dffb7b844411b` |

指定対象の scoped whitespace/conflict/hash 検査は PASS。repository 全体の `git diff --check` は、今回の対象外で
既存の `search/probe/wac_v1/scan_out.txt` 11–15 行にある末尾空白のため exit 2 である。今回の実装対象には
新規 diagnostic はない。

便149の役割改定は今後の運用として受理した。今回は Luna を起動し、返書を受け取り、複数回差し戻し、成果物と
正確な blocker まで自己完結させた。工房へ投げたままの便ではない。一方、blocker を完成扱いする過大格付けもせず、
GHA 要求は保留する。

```text
FINAL:
ROLE_CONTRACT_APPLIED;
LUNA_ITERATION_COMPLETED_TO_HONEST_BLOCKER;
BLOCKED_RELATIVE_EXTENSION_ENUMERATOR/NONCHECKPOINTABLE_EXTENSION_CELL;
NO_GHA_REQUEST;
NO_A_OR_B_CLAIM;
CROSS_CHECKED_FALSE;
VERIFIED_FALSE
```
