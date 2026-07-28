# interp 追補 (o) v3 — 二経路合成の全域関数(Sol F81-3.2 反映・発効請求版)

状態: proposal / candidate(v2 を置換)。合成器名 = evidence-union/fail-closed-**v2**(P81-E)。

## 分類(受領側の義務)
- **route_status は producer 入力でなく受領 verifier の出力欄**。各 route を受領側が ABSENT / MALFORMED / PASS / FAIL に分類する。
- status 別の必須欄: **PASS** = 全域 count+coverage_digest(下記束縛)/ **FAIL** = 反例 locus / **ABSENT** = 受領側導出の欠品 mask / **MALFORMED** = schema error 記録。ABSENT/MALFORMED に PASS 形の全欄を要求しない。
- **coverage の束縛**: expected domain は native divisor/map digest から**受領側が導出**し、coverage_digest はその canonical domain digest と一致することを PASS 条件に含める。checked_domain_count 単独では全点主張にならない。

## 合成の全域関数(順序つき・swap 対称)
1. どちらかの route が **MALFORMED** ⟹ 向きによらず **INTEGRITY_STOP**。
2. 非 ABSENT が二本 ⟹ **claim_digest を status 合成より先に比較**し、不一致は常に **CONFLICT**(PASS/PASS に限らず FAIL/FAIL・FAIL/PASS でも)。
3. PASS と FAIL の衝突 ⟹ **CONFLICT**。
4. 残り: FAIL が一つでもあれば **FAIL**・PASS が一つでもあれば **PASS**・両方 ABSENT のときのみ **ABSENT**。
- 16 状態対の全域性と swap 対称性は **table-driven test** で機械検査する(P81-E)。

発効後に EP v7(最終 record)を発射する。
