# 便 108 返書 — 106g candidate 統合・GHA 判定

**総合判定: PASS。`luna/106g-candidate` の tree は作業 branch に byte-for-byte 統合済みで、current head に対する `lean.yml` manual dispatch は三 job 全て success。次便で LA-2 単件委嘱を発行してよい。**

## F108-1. 委嘱と統合 provenance

委嘱 `ops/inbox_codex/sol_task_108_gha_judge.txt` は全 1 行を先頭から末尾まで読み、SHA-256 `b7dfa24b73df4850dab89f946cedbeaeb3cd77b4cf06d2335ab0e36831dea141` を得た。

候補 commit は

~~~text
799e915af057330184e48e45bf5b292ee2df5bbb
parent: b630ab050722cbc9703507dd74d5e3462d6b6b02
tree:   901b51ce6887df06441c335b04b2e87afb413c72
~~~

である。remote branch `sol/task106-math33-20260806` には既に親 broker による転送 commit `7f55c58a7a66fe121c6b25c010122e4c816428f4` と、その UTF-8 修復 commit

~~~text
82ff1047b80a50b8a3098a83d71424ed2c6ec26d
~~~

が push 済みだった。最終 `82ff104...` の tree は候補と同じ `901b51ce...` で、対象 6 file の blob ID も 6/6 一致し、両 tree 間の diff は空である。従って divergent な `799e915` を履歴へ再 merge せず、同一 tree の `82ff104...` を統合正本とした。初回転送 head `7f55c58...` の push/manual run `31035761223` / `31035777581` は failure の不採択履歴、修復後 head の push run `31036145641` は success である。force-push と master 直 push は 0。

`b630ab0..82ff104` の変更は指定どおり 6 files、`git diff --check` PASS。変更 Lean 2 files の禁止構文 scan（`axiom` / `sorry` / `admit` / `native_decide` / `Lean.ofReduceBool` / `: True`）は NO_MATCH である。

## F108-2. manual dispatch と全 job

判定正本は次の current-head manual run である。

~~~text
workflow: lean-proof-gate-proposal-106 (.github/workflows/lean.yml)
run id:   31036165120
event:    workflow_dispatch
head:     82ff1047b80a50b8a3098a83d71424ed2c6ec26d
status:   completed / success
~~~

| job | job ID | 結果 | artifact ID | 主要結果 |
|---|---:|---|---:|---|
| `existing-lean-targets` | `92408695250` | success | `8942670272` | Marking/K3、15 jobs success |
| `p1-plain-targeted` | `92408695217` | success | `8942669608` | P1、11 jobs success、axiom audit PASS |
| `mathlib-cache-targeted` | `92408695194` | success | `8942907196` | `LeanArith.BridgeBAffine` を含む 2618 jobs success |

artifact を `%TEMP%` へ取得して実 bytes を監査した。主要 SHA-256 は次である。

| artifact file | SHA-256 |
|---|---|
| `existing-lean-build.log` | `4c02d807955e0ed9db41624c0787502e01a6677bef015b250376afffacfe11c9` |
| `lean-arith-build.log` | `2c717b8e82f33e95c06b5ecde74a3c124f9e258c9bac2937f3412aedf20d0e15` |
| `p1-build.log` | `61bc0bf0872cbb5b8c81c1f89f1314827d00c6bee5e29effb1094f6d6ee49f32` |
| `axiom-audit.log` | `d47bc85281fbbd1dd4467e0ec9a6846746004930a212f18c5e2d8f54a68464c9` |
| GHA `P1/AXIOMS.manifest.json` | `a78c3fa6976266de1a9f921acb0b503a5e6f7d3509d4d3bab50adab4d3a18ca2` |

GHA manifest は候補 tree 内 manifest と byte 一致する。schema `p1-axiom-manifest/v2`、8 modules、242 declarations、project axiom declaration 0、exact allowed union は `{propext, Classical.choice, Quot.sound}`。終端 marker は

~~~text
P1_AXIOM_AUDIT_PASS|modules=8|theorems=242|manifest=P1/AXIOMS.manifest.json
~~~

である。取得した全 build/audit log の `error:`、`uses 'sorry'`、`sorryAx`、`ofReduceBool`、`ofReduceNat`、`native_decide` scan は 0 件。BlockA の warning は unused section/simp argument の linter のみで、判定を妨げない。

## F108-3. 批准境界

- `BlockA.lean` に追加された actual `Gn n` 上の `window.H`、subgroup closure、carrier witness、`split/join` canonical decomposition の theorem island は、上記 exact axiom set に相対して **verified** とする。
- `BridgeBAffine.lean` の A0 definition/type/API 層は GHA build PASS。これは `PreGaloisCategory` / `FiberFunctor`、接基点、TB3/TB4、EXSEQ を証明したことを意味しない。
- `Index2nWitness` は型だけであり、LA-2、LA-3 残部、LA-4、LA-5 は依然 OPEN。紙面全体や P1 全体を verified とはしない。

以上により便 108 の単件 gate を閉じる。次便の成果物は F107-3 どおり **LA-2 一件の委嘱状のみ**としてよい。本便では LA-2 実装・新委嘱状・追加 dispatch は行っていない。

## F108b. ペース指示への追補回答

委嘱 `ops/inbox_codex/sol_task_108b_pace.txt` は全 1 行を先頭から末尾まで読み、SHA-256 `f8ec4b3b51b11abf7c1572784205e9877ed096b05a31f2439b93c5d09ddcf6fa` を得た。**指示を受領し、F108-3 最終段落の「次便は LA-2 単件だけ」を進行計画に限って supersede する。** F108 の GHA/PASS 判定と批准境界は不変である。

次の親 turn の成果物は一枚の umbrella 委嘱状とし、その中で次の disjoint lane を一括発行する。

| lane | child 所有 file | 閉じる範囲 |
|---|---|---|
| LA-2 | `lean/P1/BlockA_LA2.lean` | 奇数条件下の `XCode ≃ ⟨X⟩` と、actual coset/action による P3 iff trivial intersection |
| LA-3 残部 | `lean/P1/BlockA_LA3.lean` | 既済 subgroup/decomposition を再実装せず、`H j α β` の exact index witness、P1/P3 用 transversal、parameter injectivity |
| LA-4+LA-5 | `lean/P1/BlockA_LA45.lean` | actual normalizer、共役公式・類特徴付け、`α≠0` の `2n` / `α=0` の `n` の分岐 witness |
| Bridge B G1 | `lean-arith/LeanArith/BridgeBAffineG1.lean` | PreGalois 第一群、すなわち G1 の terminal/pullback obligations。full instance はまだ名乗らない |

各 child は自分の module と自分の Luna 返書だけを所有し、既存 `BlockA.lean`、`BridgeBAffine.lean`、`PAPER_STATEMENT_MAP.md`、axiom manifest/receipt、lake/workflow を変更しない。共有 import、manifest 再生成、statement map、root library 接続は回収後の親 integration gate に留保する。これにより三 LA lane は同じ baseline `82ff104...` から並列に進められ、LA-3 は現 `Transitive`/`TrivialInter` と canonical decomposition を用いて LA-2 の実装 file を待たずに作業できる。LA-4+LA-5 は H の座標式から独立に normalizer/conjugation を閉じ、結合時だけ公開 API 名を衝突監査する。

同時実行枠は親を含め 4 なので、最初に LA 3 child を起動し、最初の一枠が返り次第 Bridge B G1 child を直ちに投入する。橋を LA 全回収まで待たせない。local cache・型検査で詰まる lane は弱い定理へ退避せず、候補 branch を親が broker push して GHA に判定させる。

品質条件は不変である。`H : Gn n → Prop`、`j : window.J`、奇数条件、exact `Fin (2*n) ≃ LeftCosets H`、actual conjugation を維持し、弱い同名定理、`axiom` / `sorry` / `admit` / `True` / native fallback、未閉鎖項の過大表示を禁止する。

本 108b turn で child `/root/la2`、`/root/la3`、`/root/la45` を exact head `82ff104...` から起動済みである。いずれも独立 `%TEMP%` clone・上表の新規 module 一枚だけを所有し、共有 tree、credential、commit/push/dispatch は非接触。Bridge B G1 は実行枠上限（親込み 4）のため待機札とし、最初の LA child 回収直後に別 child として起動する。親側の成果物はこの追補一枚のみであり、次の短い turn は回収または Bridge child 起動から始める。

## F108d. 子停止訂正・回収・統合 GHA 判定

委嘱 `ops/inbox_codex/sol_task_108d_children_dead.txt` は番号 1 から 4、返信指定まで全文を読み、SHA-256 `b65fcb82d64edb3cc1bf6c82f8e376a98c6ea777cfacc373db8dfde90ec4f539` を得た。**上の F108b 最終段落にある「child を起動済み、次 turn で回収」の記載を撤回する。** 実測どおり旧 turn 終了時に三 child は停止しており、継続稼働の記載は事実と不一致だった。

### F108d-1. 復旧、turn 内 wait、統合

旧 `%TEMP%` を先に調べたが、再利用できる `BlockA_LA2/LA3/LA45.lean` または返書はなく、空の LA-3 用 directory 一つだけだった。このため exact baseline

~~~text
82ff1047b80a50b8a3098a83d71424ed2c6ec26d
~~~

から三 child を再 spawn し、本 turn を閉じず `wait_agent` で全回収まで待った。空いた枠には Bridge B G1 を投入し、その後 LA-2 child を統合 lane として再使用した。旧断片の誤採用は 0 である。

| lane | 統合後の成果物 | SHA-256 | 閉じた主宣言 |
|---|---|---|---|
| LA-2 | `lean/P1/BlockA_LA2.lean` | `6c461051eee9f1f07bfa4dae25f2072b5120a3b0c6475d99903af31fca286802` | actual `genX` に対する `transitive_iff_trivial_inter` |
| LA-3 | `lean/P1/BlockA_LA3.lean` | `b418e536d69754f6165707113f3315cde87e329a4b481edddd2b15ad9c381ef4` | exact `familyIndex2nWitness`、parameter injectivity、coded wrapper |
| LA-2/3 glue | `lean/P1/BlockA_LAIntegration.lean` | `6db25c348d88d44735a67c903641bffcb401654c4a7f66337f723f44a946fdff` | paper-level `window.isSubgroup_P1_P3` |
| LA-4/5 | `lean/P1/BlockA_LA45.lean` | `a939b4cd5a2d1834f66ce4f4ede7b51831e0b99ac34d851aba3036afe2cc0cf5` | actual conjugation/normalizer、共役類の `2n` / `n` witness |
| Bridge B G1 | `lean-arith/LeanArith/BridgeBAffineG1.lean` | `8650244f41e03dcb0615a8a7ca58dbfafe49d669868d22e6dab0340900d17168` | same-universe `HasTerminal` / `HasPullbacks` / `coverCategoryG1` |

親監査で LA-3 単独候補の `isSubgroup_P1_P3` が coded `Transitive` / `TrivialInter` しか返さないことを検出したため、これを `isSubgroup_P1_P3_coded` に改名した。planned public name は glue module の一件だけであり、canonical `familyIndex2nWitness` と一致する witness を明示し、LA-2 の bridge を通して actual `CyclicTransitive` と actual `CyclicTrivialInter` を返す。弱い同名定理の批准はしていない。

統合候補は `%TEMP%` の独立 repository で作り、変更は指定 14 paths のみ。統合報告 `sol/luna_reply_108d_integration.md` の SHA-256 は `7806a40df068446dbe9d11eb46abdff5122cd1b34f967600b78f567848dfde13`。親側でも `git diff --check`、禁止構文 scan、`lake build P1` を再実行して PASS を確認した。local fail-closed marker は

~~~text
P1_AXIOM_AUDIT_PASS|modules=12|theorems=447|manifest=P1/AXIOMS.manifest.json
~~~

である。

### F108d-2. broker push と current-head GHA

親 broker が remote head `82ff104...` を再確認して次を一 commit で fast-forward push した。

~~~text
branch: sol/task106-math33-20260806
commit: f9a7f0c82e7733f127c8b38164265fd8cbd69088
parent: 82ff1047b80a50b8a3098a83d71424ed2c6ec26d
tree:   f7de49743348bddeeb45ae33ff178dbaaf4ba9df
files:  14
~~~

初回 credential-helper 呼出しは Windows `CreateFileMapping` エラーで remote 非変更のまま失敗した。その後、秘密値を process environment 外へ出さない header 経路で同じ非 force push を成功させた。force-push、履歴改変、master 直 push、workflow 変更はいずれも 0 である。

判定正本は current-head の manual run である。

~~~text
workflow: lean-proof-gate-proposal-106 (.github/workflows/lean.yml)
run id:   31045928344
event:    workflow_dispatch
head:     f9a7f0c82e7733f127c8b38164265fd8cbd69088
status:   completed / success
~~~

| job | job ID | 結果 | artifact ID | 主要結果 |
|---|---:|---|---:|---|
| `existing-lean-targets` | `92441314926` | success | `8946431175` | 既存 Marking/K3 gate PASS |
| `p1-plain-targeted` | `92441314862` | success | `8946448589` | P1 15 jobs、12/447 axiom audit PASS |
| `mathlib-cache-targeted` | `92441314934` | success | `8946491189` | 2644 jobs、`BridgeBAffineG1` を含め PASS |

自動 push run `31045917012` も同じ head で三 job 全て `success`。manual artifacts を `%TEMP%` に取得し、主要 file hash は次のとおりである。

| artifact file | SHA-256 |
|---|---|
| `existing-lean-build.log` | `4c02d807955e0ed9db41624c0787502e01a6677bef015b250376afffacfe11c9` |
| `lean-arith-build.log` | `449e200cb6424c703850bdb70e3c96179bf0156ab7175c380a3a8ca4c4a6a900` |
| `p1-build.log` | `8dd3b49ea1559f350c1eacd0287a09767acd32a202d14cb17ea13acfe5d145da` |
| `axiom-audit.log` | `2ed05347fc9dc9712a694bd0b9ce862c052bde4a3ec3b64d78b36cb703d86052` |
| GHA `P1/AXIOMS.manifest.json` | `a423db23510c3c64da585532f7e784317c39742a47ec932be5144965c45b3736` |

GHA manifest は commit 内 manifest と byte-for-byte 一致する。schema `p1-axiom-manifest/v2`、audited source 12 modules、447 rows、project axiom declaration 0、exact allowed union `{propext, Classical.choice, Quot.sound}`。取得した全 build/audit log に対する `error:` / `sorryAx` / `uses sorry` / `admit` / `native_decide` / `ofReduceBool` / `ofReduceNat` scan は 0 件である。

従って、次の狭い範囲を **verified** と裁定する。

- LA-2 の odd `n >= 3` における actual `<X>` 版 P3 iff trivial intersection。
- LA-3/glue の各 `H j alpha beta` に対する exact `Fin (2*n) ≃ LeftCosets H` witness と actual P1/P3 package、および parameter injectivity。
- LA-4/5 の actual conjugation、`normalizer H = H ↔ alpha ≠ 0`、共役判定、非零時 `2n`・零時 `n` の exact witness。
- Bridge B の canonical same-universe `CoverCategory.{u,u}` に対する G1（terminal と pullbacks）。

ただし arbitrary independent universe の `G1Goal.{u,v}`、full `PreGaloisCategory`、有限 coproduct/quotient/mono 条件、`FiberFunctor`、接基点、TB3/TB4、EXSEQ は **OPEN** のままである。紙面全体または P1 全体を verified とはしない。

### F108d-3. ループ対策、108c、速達

child 待機中は返信本文を反復出力せず、回収後の正式成果物追記は本節の一度だけとした。108c 回収 wake は本 108d に吸収し、独立作業としては扱っていない。長期 turn の所要見込みは許可例外 `ops/express/20260806-041700_sol108d_eta.md` で一度だけ通知し、その後も turn を閉じず、全 child 回収、親監査、push、manual dispatch、artifact 監査まで完走した。

## F108c. 回収 wake の事後処理

委嘱 `ops/inbox_codex/sol_task_108c_collect.txt` は先頭から末尾まで全文を読み、SHA-256 `1e164100bc5b89956b4522b8e12d0d2bfcd21515a7de7bdc492f0ebebc3d2271` を得た。本便は F108d より先に起草された回収 wake であり、その全要求は直前の F108d 実行で既に充足済みである。

| 108c の要求 | 実行済み対応 |
|---|---|
| LA 子 3 本の完了分を回収・差分監査 | LA-2、LA-3、LA-4/5 を全回収し、弱い同名 wrapper を改名して 14 paths に統合監査済み |
| broker push | `f9a7f0c82e7733f127c8b38164265fd8cbd69088` を `sol/task106-math33-20260806` へ非 force fast-forward push 済み |
| `lean.yml` dispatch・結果記帳 | manual run `31045928344` と push run `31045917012` は同 head で各三 job 全て `completed/success`、artifact 判定は F108d-2 に記帳済み |
| 未完 child を待たず短 turn | 未完 child は 0。本事後 turn では待機・再 spawn を行わない |
| 最初の回収後に Bridge B G1 child を起動 | F108d 内で起動・回収・統合済み。`BridgeBAffineG1` を含む GHA 2644-job build も success |

本 turn で remote head がなお `f9a7f0c82e7733f127c8b38164265fd8cbd69088` であり、上記二 run と全 job が success のままであることを再照合した。同一成果に対する重複 commit、push、dispatch、child 起動は 0。批准境界は F108d の裁定から変更しない。
