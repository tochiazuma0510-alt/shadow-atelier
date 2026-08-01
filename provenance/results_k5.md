# results_k5.md — K⁵ 橋の結果記録(versioned・manifest の「結果規則表と結果記録の分離」条項に基づく正本)

**規則**: manifest(docs/manifest_k5_v1_*.md)は開示後も不変。結果・状態変化は本ファイルへ追記のみで記録する(過去 entry の編集禁止)。

---

## Entry 1(2026-08-02・裁定 412・Sol F99-4.3)— (P1)(P2) の外部解決の記帳(bridge 実行ではない)

- **種別**: 外部解決の記帳。**bridge_result_sq = UNKNOWN・bridge_result_ns = UNKNOWN・pair_gate = OPEN・saturation_result = NOT_PROVED**(いずれも不変 = K⁵ 橋の本測定は未発火)。
- **追記(Sol 指定文)**: (P1)(P2) **resolved externally by authorized FAM-U n=5 lane; provenance = search/certs/u5_fire_20260801.json(sha256 = 2653ab9c04610a13c2fdc6eb39c907c5839a5303f429faf4f61605bfb7404e23)+ 裁定 398**。
  - 内容: u₅(α̃=1) = −4・u₅(α̃=2) = +4 ⟹ 双方の mod 10 類の位数は 5 =(P1)の {1,5} 側(5 で成立)。[−4]₁₀ = [4]₁₀(比 −1 は十乗類で自明)⟹(P2)一致。
  - **これは K5 Model-Builder / Freeze2 / BRIDGE-IN が実行されたことを意味しない**。K⁽⁵⁾ genuine 戦役自身の status = **BRIDGE-UNKNOWN・本測定未発火**のまま。過去の封印記録(manifest v1.x)は上書きしない。
- manifest 参照: docs/manifest_k5_v1_7.md(sha256 = 307c57942c1ba9050fc3d9ee424ca812300da41665d39387defc4cbdfc57377d)
- 出所: sol/sol_reply_99_math26.md F99-4.3・provenance/LEDGER.md 裁定 412。
