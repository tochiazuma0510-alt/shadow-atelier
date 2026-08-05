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
