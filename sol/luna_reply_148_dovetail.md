# Luna reply 148 — D972 A-side relative-extension dovetail

## 判定

`BLOCKED_RELATIVE_EXTENSION_ENUMERATOR`

`sol/luna_task_148_dovetail.md` は §0 から §8 まで全て読了・処理した。要求された「全ての有限 marked-over-base 相対拡張を、非可換核を含めて、重複なく列挙する」実装は、この作業ツリーには存在しない。従って、k=3,4,… の無限 dovetail を開始したとは報告しない。完全列挙器がない状態で heuristic/catalog lane を complete と扱うこと、`k_closed=true`、terminal、`cross_checked=true`、`verified` を付けることは行っていない。

このターンの変更は本返信ファイルの追加だけである。既存の dirty file は変更していない。commit/push/dispatch は行っていない。

## §0 — 目的・境界・対象ファイル

正本の対象は

\[
 M=K^{(9)}\cap N_{S_4},\quad Q_0=P B_3/M,\quad |Q_0|=1,469,664,
\]

および、全ての marked-over-base `(barE,s1,s2,rho)`、`|E|=k|Q0|`、k=3,4,… の相対拡張である。指定の isolation、`GT(E)->GT(M)` の 972 target fibers、producer/checker の独立一致、terminal 条件を確認するには、§3 の complete relative-extension engine と §5 の独立 checker が必要である。

指定された以下の対象は全て未配置だった。

~~~
search/d972_dovetail_producer_v1.py       NOT FOUND
search/d972_dovetail_worker_v1.g           NOT FOUND
search/check_d972_dovetail_v1.py           NOT FOUND
search/d972_dovetail_state_schema_v1.json  NOT FOUND
search/d972_dovetail_manifest_v1.json      NOT FOUND
search/fixtures/d972_dovetail_v1/          NOT FOUND
.github/workflows/d972-dovetail.yml       NOT FOUND
~~~

既存の `search/d972_phase0_v1.*`、`d972_phase1_v1.*`、`d972_phase2*` は関連する有限段階・候補・ゲートの記録であり、上記の complete relative-extension engine の代替ではない。

## §1 — HEAD と anchor audit

`git rev-parse HEAD` の出力:

~~~
9799237e31d12a4c35029604e26d7afa8703dcc5
~~~

SHA-256 は指定コマンドで再計算し、7 件とも指定値と一致した。

| anchor | 実測 SHA-256 | 指定値との照合 |
|---|---|---|
| `ops/inbox_codex/sol_task_148_dovetail.txt` | `8890c29cf3c399da863e6705f3ccc434164c1c233ff82f648b965f99612e71f9` | MATCH |
| `docs/week1-定義ノート.md` | `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c` | MATCH |
| `docs/notes/d972_phase2_cofinal_execution_v1.md` | `97998cac97611f10065b463efa8a417d5da200b23dd39ca7a8b2beed32de847e` | MATCH |
| `docs/notes/triad972_canonical_addendum_v2.md` | `5dc660dd0023bf9b1986cefa65ec9947ad5b3b366f210933dbe09ac2544c7659` | MATCH |
| `sol/sol_reply_143_typedfiber.md` | `ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a` | MATCH |
| `search/certs/nf972_sourcemap_a_v3_20260804.json` | `32e268c97c77446b85787c5d7750da758df67646de414eade709ca79baf98b37` | MATCH |
| `search/certs/nf972_sourcemap_b_v6_20260804.json` | `e27a71fbf00295be9a74761ef11134e3a8f324ed57f523d11d44a67fb5a207de` | MATCH |

変更ファイル（このターン）:

~~~
sol/luna_reply_148_dovetail.md  (new)
~~~

## §2 — 相対拡張の数学的対象と completeness

要求対象は abstract group の名前や SmallGroups ID の一覧ではない。`barE`、marked generators `s1,s2`、braid relation、`rho:barE -> barQ`、その lifts、kernel `E`、および `L=ker(B3 -> barE)` を同時に持つ marked-over-base equivalence class である。`|barQ|=8,817,984`、k=3 なら `|barE|=26,453,952` となる。

complete であるために必要な API/math stage は次の通りである。

1. 各 k の全 abstract kernel H を非冗長に列挙する。
2. 全ての `barQ -> Out(H)` action を列挙する。
3. obstruction-zero の全 extension class を base+kernel fixed equivalence まで列挙する。
4. `s1,s2` の全 lifts を生成し、braid、生成性、exact kernel、factor map を検査する。
5. base-fixing automorphism による marked orbit を取り、semantic key 一回だけを emit する。

既存の phase0/phase1 記録は `PB3/M=1,469,664`、`M_ord=18`、`|B3/M|=8,817,984`（normality の一部は derived と明記）、`GT(M)=972` などを保持する。しかし phase0 の marked-factor-map は `AutomorphismGroup(PN)` / full-B3 generators の欠落により `UNKNOWN`、phase1 の `h1_k_isolated` も `UNKNOWN` である。これは §3 の complete nonabelian enumerator ではない。

したがって、非可換 H、非 split/非 central extension、全 marked lift、orbit dedup の完全性は未実装・未立証である。`SmallGroups` の部分カタログや split/central/solvable-only の探索を complete と昇格させていない。

## §3 — engine gate / state / dedup

| 要求 | 実装・実行状態 | 判定 |
|---|---|---|
| k,H,action,extension class,marked orbit の完全列挙 | producer/worker 不在 | BLOCKED |
| nonabelian を含む extension API と obstruction stage | API/receipt 不在、既存記録は UNKNOWN | BLOCKED |
| semantic key の exactly-once/checkpoint cursor | state schema/manifest 不在 | BLOCKED |
| k の prefetch と未閉鎖扱い | 実装不在 | NOT RUN |
| `k_closed=true` の禁止、timeout の UNKNOWN/RESUME | 実装不在 | NOT RUN |

指定の exact API/math stage が実装されるまで、k=3 の列挙開始、k の closure、finite catalog の infinite dovetail への昇格はしない。

## §4 — 各 L の isolation / hexagon / GT fiber

§4 の判定順（全 `(m,f)` universe、full B3 hexagon (3.3),(3.4)、`T_{m,f}` surjectivity、全 source kernel が exactly L、isolated L のみ (3.60)、canonical 972 target key set/fiber counts）を実行できる producer は存在しない。

既存 receipt の範囲は次の通り。

| 既存 lane | 実測/記録 | §4 の不足 |
|---|---:|---|
| phase0 `PB3/M` | 1,469,664 | relative-extension L の全 universe ではない |
| phase0 shadow / `GT(M)` | 972 / 972 | `M` の isolation は `UNKNOWN` |
| phase1 m-shadow / `im R_KM` | 972 / 972 | 各 relative L の 972 fiber vector ではない |
| phase0/phase1 `h1_*_isolated` | `UNKNOWN`, not attempted | full-B3 action/marked map が未解決 |

従って、exact target-set digest、全 972 fiber counts、zero-key set、image subgroup 324 の terminal 条件は未計算である。`m mod M_ord` は使うべきだが `M_ord/2` shortcut は使っていない、という既存記録だけでは §4 の完了にはならない。

## §5 — producer/checker independence

`search/check_d972_dovetail_v1.py` と producer/worker がないため、lossless witness の受け渡しも helper-independent checker の再計算も行われていない。

| checker requirement | producer | independent checker | 結果 |
|---|---|---|---|
| kernel presentation/table または compact permutation witness | absent | absent | NOT RUN |
| marked lifts, braid, generation, exact kernel, `rho` | absent | absent | NOT RUN |
| B3 normality / quotient factorization | absent | absent | NOT RUN |
| independent charming/full-hexagon traversal | absent | absent | NOT RUN |
| (3.60), exact 972 key set, fiber vector, zero-key set | absent | absent | NOT RUN |
| isolated / GT order / image / vector agreement | absent | absent | `cross_checked=false` |

SHA と件数だけの照合は cross-check として受理していない。Lean 証明書もないため `verified` でもない。

## §6 — calibration, negative tests, terminal gate

### k=1, k=2 calibration

メールに指定された calibration の期待値は次の通りである。既存 tree に、これを producer と independent checker の両方で生の marked-orbit/fiber receipt として再現した成果物はないため、実測 PASS とは扱わない。

| calibration | 期待 raw orbit/count | 期待 GT / isolation | 期待 image / zero fiber | 実測 receipt |
|---|---|---|---|---|
| k=1 base M | 1 orbit | GT=972, isolated | image=972 | M の shadow/GT=972 は既存。full isolation receipt は UNKNOWN |
| k=2 split | 1 marked orbit | GT=972, isolated | image=972, zero=0 | 不在 |
| k=2 nonsplit | 2 marked orbits | 各 GT=1944, isolated | image=972, zero=0 | 不在 |

既存 phase0/phase1 の 972 件は k=1 の calibration の一部に対応するが、要求された complete source-kernel と full fiber histogram の代わりにはならない。

### negative fixtures

actor map、kernel order、braid relation、ord-level mode、settlement、m modulus、fiber row を変えた FAIL/STOP fixture directory は未配置である。従って expected/actual の全 negative matrix は次のようになる。

| fixture family | expected | actual |
|---|---|---|
| actor-map mutation | FAIL/STOP | NOT RUN — fixture absent |
| kernel-order mutation | FAIL/STOP | NOT RUN — fixture absent |
| braid mutation | FAIL/STOP | NOT RUN — fixture absent |
| ord-level mutation | FAIL/STOP | NOT RUN — fixture absent |
| settlement mutation | FAIL/STOP | NOT RUN — fixture absent |
| m-modulus mutation | FAIL/STOP | NOT RUN — fixture absent |
| fiber-row mutation | FAIL/STOP | NOT RUN — fixture absent |

### terminal gate

terminal の必要条件（2 系統一致、exact 972 target set/vector、zero-key nonempty、image subgroup 324、`A_ar <= Im R`、`|A_ar|=324`）を一つも全て確認していない。従って `A_WITNESS_CROSSCHECKED` は発行しない。nonempty fiber が見つかった場合の正しい次状態 `CONTINUE`、不一致の `DISAGREE_STOP`、資源不足の `UNKNOWN/RESUME` も、実行器がないため未適用である。B-refinement や genuine refinement の存続は主張していない。

## §7 — workflow

要求された `.github/workflows/d972-dovetail.yml` は存在しないため、workflow static validation は `NOT RUN / BLOCKED` である。dispatch、schedule、fixed concurrency (`cancel-in-progress: false`)、watchdog、API state restore、schema/code/input digest、parent SHA chain、monotonic cursor、fork/artifact failure の `STATE_STOP`、terminal no-op、read-only permissions、secret 非出力を確認できる workflow はない。

実行 run ID は存在せず、推測で記録していない。workflow の作成・変更、dispatch、self-dispatch、commit/push はこのターンの権限・範囲外なので行っていない。

## §8 — acceptance ledger / commands

| 要求 | 結果 |
|---|---|
| 1. HEAD, anchors, changed-file list | HEAD と 7 anchors を取得。変更は返信のみ |
| 2. completeness/API/nonabelian scope | complete engine 不在。`BLOCKED_RELATIVE_EXTENSION_ENUMERATOR` |
| 3. canonical dedup proof/gate | producer/schema 不在、未実装 |
| 4. helper independence | checker/witness 不在、`cross_checked=false` |
| 5. k=1,2 raw counts/full histogram | 期待値は記録、両系統 raw receipt は不在 |
| 6. all negative tests | fixture 不在、全て NOT RUN |
| 7. interrupt/resume and semantic-key audit | state schema/manifest 不在、NOT RUN |
| 8. commands/exit/wall/RSS/disk | blocker確認コマンドのみ実行。producer/checker の exit/resource は N/A |
| 9. workflow static validation/run ID | workflow 不在、NOT RUN、run ID なし |
| 10. diff check/status/no git mutation | 下記。commit/push/dispatch なし |

### 実行した確認コマンドと出力

~~~powershell
git rev-parse HEAD
9799237e31d12a4c35029604e26d7afa8703dcc5
~~~

~~~powershell
Get-FileHash <each anchor> -Algorithm SHA256
# 7/7 anchors: MATCH
~~~

~~~powershell
Test-Path <each requested producer/checker/schema/manifest/workflow/fixture>
# all requested paths: False / NOT FOUND
~~~

producer、GAP worker、checker の実行コマンドは、対象ファイルが存在しないため実行していない。したがって producer/checker の exit code、wall time、RSS、disk usage、fiber vector、checkpoint receipt は `N/A (blocked)` である。

~~~powershell
git diff --check
# exit 1; five pre-existing trailing-whitespace lines in search/probe/wac_v1/scan_out.txt (lines 11-15)
~~~

この返信を書いた後の `git status --short`（raw tracked/untracked lines）は次の通りである。既存変更はこのターンの変更ではない。

~~~text
 M .github/workflows/w9-p1-k3-crt-C2.yml
 D ci/smoke.g
 M search/probe/wac_v1/__pycache__/gt_thirdparty_bootstrap.cpython-313.pyc
 D search/probe/wac_v1/__pycache__/u_meas_caseb_a5.cpython-313.pyc
 M search/probe/wac_v1/scan_out.txt
 M sol/luna_task_148_dovetail.md
 M sol/sol_reply_134_survival.md
 M sol/sol_reply_135_blind3grp.md
 M sol/sol_reply_139_threetheorems.md
 M sol/sol_reply_140_finish.md
 M sol/sol_reply_148_dovetail.md
?? sol/luna_reply_148_dovetail.md
~~~

作業ツリーには上記以外にも既存の untracked scratch/artifact があるため、それらは触れていない。最終状態は `BLOCKED_RELATIVE_EXTENSION_ENUMERATOR` であり、次に必要なのは §3 の complete relative-extension enumerator、その lossless witness schema、独立 checker、k=1/k=2 calibration receipts、negative fixtures、そして workflow の事前承認付き実装である。


