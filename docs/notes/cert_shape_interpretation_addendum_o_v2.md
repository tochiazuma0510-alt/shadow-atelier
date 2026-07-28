# interp 追補 (o) v2 — W-6 二経路の合成規則(Sol F80-4.3 反映・発効前 draft)

状態: proposal / candidate(v1 draft を置換)。合成器の一般名 = **evidence-union/fail-closed-v1**(P80-D — W-6 固有でなく複数証明経路の共通規則)。

## 経路欄(R1 = 再計算経路・R2 = 証跡経路、各々必須)
route_status ∈ {ABSENT, MALFORMED, PASS, FAIL}・claim_digest・evidence_digest・checked_domain_count・coverage_digest。
- 必須 ref の**一部だけ**存在 = MALFORMED(ABSENT でない)。
- route_absent は producer 自己申告を信じず**受領側が入力欄から導出**。
- R1 = map/ramification/branch の digest 解決+全点・重複度の再計算。R2 = 点別 witness の全域被覆+重複度保存。両経路併存時は同一 W-6 claim/object の検査であることを digest で束縛。

## 合成表(fail-closed)
| R1 | R2 | W-6 全体 |
|---|---|---|
| ABSENT | ABSENT | ABSENT |
| PASS | ABSENT(逆も) | PASS |
| PASS | PASS | 同一 claim_digest なら PASS(不一致は CONFLICT) |
| FAIL | ABSENT(逆も) | FAIL |
| FAIL | FAIL | FAIL |
| PASS | FAIL(逆も) | **INTEGRITY_STOP / CONFLICT** |
| MALFORMED | 任意 | **INTEGRITY_STOP** |

発効: Sol 確認後・EP v7 の最終 record に採用(N80-4.2)。
