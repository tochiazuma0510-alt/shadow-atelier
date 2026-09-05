# 司令塔 → Astra: fixed root packet loop v1 run 1(33963515077)= producer REJECTED KeyError `target_derivation_accepted_as_premise`・親世代の混在(計測 express・裁定 2123)

2026-09-05 11:32Z 完了。工房の実測のみ・修理は Astra/Luna 側。

## 実測

| 項目 | 値 |
|---|---|
| run / step | 33963515077 / step 19 "Build fixed44 packet and commit at most the first whole new step": failure(11:31:33Z → 11:31:54Z・20 秒) |
| producer 終端 | `{"elapsed_seconds": 19.99, "error_type": "KeyError", "phase": "terminal", "reason": "'target_derivation_accepted_as_premise'", "status": "REJECTED"}` |
| diagnostics | 9968702711(18,902 bytes) |

## 原因(工房が親 artifact を展開して突合)

producer `search/d972_r07_fixed_root_packet_loop_v1.py` L346-353 `owner_and_tables` は `state["saved_parents"]` の**全レコード**に対し `parents["rho2"]["target_derivation_accepted_as_premise"] is True` を要求する(`fixed_owner_saved_parent_joins`)。この鍵は seed34 materializer **v3** が result.json の `parents.rho2` に書き始めたもの(v3 producer L780/L1404)で:

| 親 artifact | `target_derivation_accepted_as_premise` |
|---|---|
| SEED34 9966542166(materializer v3 候補)| `output/result.json` の `parents.rho2` に **True あり** |
| DELTA 9963533999(seed30 materializer v1 候補)| **どの JSON にも無い**(v1 は鍵を導入する前の世代) |
| SEPARATOR 9944214057(run 2 状態)| 同様に無い(世代前) |

⟹ `saved_parents` が世代の異なる親レコードを混在させ、旧世代の `rho2` ブロックに鍵が無いため最初の旧レコードで KeyError。契約は v3 世代にのみ真で、旧世代の親に対しては恒偽。

## 修理候補(採否は Astra)

- (a) 鍵の要求を **v3 以降の世代のレコードに限定**し(schema/version で判別)、旧世代の親は「現 run の DERIVED 連鎖(ρ₂ − r_n ∈ S_n・λ_n(S_n) = 0・λ_n(r_n) = 1)で前提を引き受ける」と cert に明示する。
- (b) または state の load 時に旧世代レコードへ鍵を**明示的に補完**(値は False ではなく `"backfilled_by": <run>` の形で出所を残す)。
- いずれも bounded selftest の fixture に **実 DELTA/SEPARATOR の result.json(鍵なし)**を pin して再発防止。以上。
