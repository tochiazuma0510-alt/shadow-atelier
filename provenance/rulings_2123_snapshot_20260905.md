# 裁定 2123 snapshot(2026-09-05・司令塔記帳)

- 2123: **fixed root packet loop v1 run 1(33963515077)= producer REJECTED KeyError target_derivation_accepted_as_premise(20 秒)**: producer L346-353 が state.saved_parents の全レコードに v3 世代の鍵を要求 → 旧世代の親(seed30 mat v1 候補 9963533999・separator run 2 9944214057)の rho2 ブロックに鍵が無く KeyError(seed34 v3 候補 9966542166 の result.json には True あり)= 親世代の混在。工房が親 artifact を展開して確定・計測 express `ops/express/20260905_fable_astra_packet_loop_run1_keyerror.md`(世代限定 or 明示 backfill・実 result.json を fixture に)。
