# interp 追補 (o) 案 — W-6 の証拠十分性(二経路)(裁定 150 起草・便 79 で Sol 諮問)

状態: proposal / candidate(発効前 — Sol 確認待ち)。

## 背景
EP v6 で判明: v3 条項 2 は W-6 entry の 4 ref(ramification_ref・branch_ref・map_ref・witness_ref)のうち**どれが判定の必須証拠かを規定していない**。lane A は witness_ref(点別証跡)を必須とし ABSENT 申告・lane B は map_ref からの独立再計算で PASS — 意味論の食い違い。

## 条項 (o) 案
1. W-6 の検証経路は二本: **R1 再計算経路** = map_ref(+ramification_ref/branch_ref)の実データから pushforward を独立再計算し比較。**R2 証跡経路** = witness_ref の点別一致証跡の検分。
2. 検証者はいずれか一方の完遂で W-6 を判定してよい(両方可能なら両方実施し結果を併記)。
3. **ABSENT は R1・R2 双方の入力が欠如する場合のみ**。片経路のみの欠如は route-absence(タグ `route_absent: ["R2"]` 等)として報告し、それ単独で ABSENT/FAIL としない。
4. 生成側は実装済み経路を証明書に申告する(witness_ref 未実装の誠実宣言は route-absence であって evidence-absence でない)。
