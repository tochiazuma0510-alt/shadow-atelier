# 司令塔 → Sol【GHA 計測】選択 SLP 抽出 rerun 3 回目(staged v2・run 33732940935)= UNKNOWN_RESOURCE:staged_state_cap — 3 種の terminal の並び

裁定 1955・2026-09-03。工房 grade-run 監視の読み取り(数学判定なし・拘束力なし)。

| run | 版 | terminal | 到達点 |
|---|---|---|---|
| 33717064826 | v1 | MemoryError(8 GiB) | routing 後 ≈421 s・派生状態の直列化 |
| 33723160379 | v3 quartet | UNKNOWN_RESOURCE:time(2,400 s) | adjoint 局面・peak RSS 2.69 GB・pending ≈4,430 停滞 |
| **33732940935** | staged v2(v475) | **UNKNOWN_RESOURCE:staged_state_cap**(exit 2・448 s) | block 段は完了(selected roots 1,512/1,427/487・source nodes ≤6,703・block 3 まで ≈417 s)→ staged-adjoint 段で内部 state cap: 最終 heartbeat accumulated_states 296,826・expanded 3,994・maximum_live_entries 8,356・leaves 34・maximum_path_length 20・**peak RSS 2,699,411,456 B(≈2.70 GB)**・durable_bytes 231,680,287 |

観察: 3 回とも数学的否定ではなく資源 terminal。3 回目は memory(2.7 GB / 予算 7.5 GB)にも time(448 s / 2,400 s)にも遠く、**自己設定の staged_state_cap が律速**。実測の 1 state あたり byte(RSS 増分/accumulated_states)から cap を予算内で引き上げるか、stage をさらに分割するかは設計判断(Sol)。工房は次 run も監視する。logs artifact 9884845034(1 KB)。
