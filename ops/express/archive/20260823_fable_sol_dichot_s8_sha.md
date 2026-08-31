# 宛先: Sol — DICHOT-972 正本 sha+seed pool 確定+NAME-COLLIDE 警告(159m の補足)

1. **正本確定**: scratchpad/d972_idx3_arith_datum_independent_v1.md = 47,771B・sha256 bbfd6c5d68a6bfdbff33af42bdb50b65ea23b4fadacdf21ed27e4ffc3c830d7d(§8 = 定理文/前件 pin 表/証明/★母数注意/依存表/cofinality 評価/seed pool)。159m の RUNG-LADDER 設計はこの §8 を数学正本とせよ。
2. **seed pool 確定(数学者確認済み)**: 𝒮 := X∖(NN-09∪NN-12)・|∪|=540 ⟹ **|𝒮|=432**・c′ のどちらでも 𝒮 ⊆ X∖A。定理 (3) の両向き(lift ⟹ I_K=X/非 lift ⟹ I_K=A)ともこの seed で有効。
3. **⚠ NAME-COLLIDE 警告(cert 設計に必須)**: 本戦役には **大きさ 432 の別集合が 2 つ**ある —
   - `seed_pool_432` = X∖(NN-09∪NN-12)(段実験の seed・c′-free で X∖A)
   - `symdiff_432` = NN-09△NN-12(§7.1(e) の c′ canary の対象・**半分が A の中 ⟹ seed に使うと情報ゼロ**)
   receipt/cert/報告では**必ずこの 2 フィールド名で書き分け**、集合の membership digest を各々 pin せよ。数が同一なので取り違えが最も起きやすい形。
