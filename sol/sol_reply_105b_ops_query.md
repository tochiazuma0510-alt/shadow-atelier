# 便 105b 運用照会への回答

## 1. エージェント起動・指示の可否

**可能。** 現環境には shell の codex exec とは別のセッション内 orchestration があり、概念上は次を使う。

- spawn_agent(task_name, message, fork_turns): bounded task を与えて子を起動。
- send_message / followup_task: 追加指示。
- wait_agent / interrupt_agent / list_agents: 回収・停止・状態確認。

同時 active 枠は親 Sol を含め **4** なので、子は最大 **3 並列**が目安である。全 agent は同じ working tree を共有する。現在の便は照会であって起動命令ではないため、実際には起動していない。repo 禁止事項どおり shell から codex exec/resume を自己起動する運用でもない。

## 2. Lean 修理・HS wrapper 実装の委譲

技術上は可能だが、現 AGENTS.md では親は Sol（数学監査・共同設計）で、実装は Luna の役割である。従って便 106 で、子の役を **Luna** と明示し、実装対象・許可 path・納品先を指定すれば委譲できる。便 105b だけを根拠に実装を始めることはしない。

実務上の注意は shared worktree の衝突である。同じ file を複数 agent に書かせず、例えば Lean repair、HS wrapper、親 Sol の read-only audit を disjoint path に分ける。親は回収後に diff、git status、build/fixture receipt を再監査する。commit/push は全員禁止。

## 3. 制約の継承

**可能。** filesystem・AGENTS.md・tool 制約は共通で、会話 context も fork できる。ただし暗黙継承だけに頼らず、各 spawn message に次の delegation envelope を逐語で再掲する。

1. role=Luna、許可 read/write path、唯一の reply path。
2. Mathlib local build/import 禁止。plain Lean local のみ、Mathlib 層は別 package を作り GHA 実行は工房へ返す。
3. 封印 3 量、705,894 候補、未認可 shard、kill/測定への非接触。
4. 許可された fixture と command、STOP/UNKNOWN 条件、resource cap。
5. 他 agent の file 非変更、nested delegation なし、commit/push なし。
6. 境界に疑義があれば実行せず親 Sol へ返す。

この形なら便 106 で正式な「親 Sol が裁定・子 Luna が disjoint 実装・親が最終検収」という設計に移れる。
