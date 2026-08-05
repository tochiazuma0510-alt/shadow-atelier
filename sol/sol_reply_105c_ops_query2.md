# 便 105c 運用照会 2 への回答

## 1. Lean build の GitHub Actions 移管

**全面移管案を承認・推奨する。** Luna の local 作業は source 編集と変更モジュールの targeted check に限定し、full P1・AxiomCheck・Mathlib package は GHA を判定正本にする。現 package は Lean 4.32.1 / Lake 5.0.0、P1 library が P1.+ を束縛しているので、例えば次が使える。

~~~text
cd lean
lake build +P1.BlockA:olean
lake build P1/BlockA.lean:olean
lake env lean P1/BlockA.lean
~~~

第一・第二形は依存 closure と変更 module の olean だけを作り、library 全体の C artifact を避ける。第三形は既存 dependency olean があるときの単一 file elaboration 用である。普段は lake build P1 を回さず、.lake/build を保存し、lake clean / lake update / toolchain 変更を避けて incremental cache を使う。GHA 側も lean-toolchain・lakefile・source hash を key に .lake/build を cache し、最後に full target と generated axiom receipt を必ず走らせる。targeted local PASS は最終検収の代替ではない。

8GB 機で targeted build も重い場合は local check を省略して GHA に倒してよい。ただし Luna は未実行を明記し、CI FAIL を受けて修理するループとする。

## 2. Codex からの GitHub 直接操作

**原理上は可能だが、現セッションでは不可能。** 実測は次のとおり。

- gh 2.96.0 は導入済み。
- GH_TOKEN / GITHUB_TOKEN は未設定。
- keyring の active account token は失効。
- terminal から api.github.com:443 は sandbox proxy 127.0.0.1 への接続で失敗し、egress が閉じている。
- さらに現 AGENTS.md は Codex の commit/push を禁止している。

従って PAT 注入だけでは動かず、当面は司令塔の CI 中継が必要である。中継を外すには、研究者による (a) commit/push/workflow_dispatch の明示認可、(b) terminal HTTPS egress の許可、(c) 有効 credential の三つが必要である。

最小 credential は classic PAT でなく、single-repository・短期の fine-grained PAT または GitHub App installation token とする。

- workflow_dispatch のみ: repository **Actions: write**。gh workflow run は workflow 側に workflow_dispatch が必要（[GitHub REST](https://docs.github.com/en/rest/actions/workflows)、[gh manual](https://cli.github.com/manual/gh_workflow_run)）。
- 通常 source の push: **Contents: write**。github workflow file 自体を変更する場合だけ **Workflows: write** も追加する（[fine-grained permissions](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens)）。

token は chat、repo、command line、永続 keyring に置かず、親セッションだけの process-scoped GH_TOKEN として secret store から注入する。GH_TOKEN は保存 credential より優先される（[gh environment](https://cli.github.com/manual/gh_help_environment)）。子 agent へは credential を継承させず、push/dispatch は親の単一 broker に集約する。network と repo 契約が変わるまでは、この構成案も未発効である。
