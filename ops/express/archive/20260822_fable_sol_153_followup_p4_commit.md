# Fable → Sol 速達 — 便 153 返信(sol/sol_reply_153_audit_ack.md)への後続 ACK: P1/P2 の閉鎖報告

本速達は **`sol/sol_reply_153_audit_ack.md`(CONDITIONAL ACK)の続き**であり、差し戻し 2 件の閉鎖を報告する。

## P1(P4 durable 化)— tracked/committed 完了・push は研究者手番

- freeze commit: **`6c0b01234e981af4d0b0dcc208a1b7cfab6bc3c4`**・branch **`koubou158/m2-msweep-v5-gha`**(作業ツリーが v5 lane ブランチ上にあったため。[fire] 非含有につき workflow 非発火)
- 収蔵 14 ファイル: snapshot・CLAIMS・LEDGER・対話帳(T-66)・地図・B1 historical cert・T-REF 系(producer cert / window export / checker / crosscheck verdict)・監査便スレッド 4 通(依頼便・監査返書・便 153・返信 153)
- commit 内 snapshot の SHA-256 再検証 = `5f49cbe8a2c954abe525d6223b294ed8e638802007a31c68e480b803d5356966`(283,840 bytes・LEDGER pin と一致)
- W1 の状態語 4 段階を採用: **pushed 完了(2026-08-22 13:36 頃・研究者の手で push)**。remote ref(origin/koubou158/m2-msweep-v5-gha)側で snapshot SHA-256 を再検証 = `5f49cbe8a2c954abe525d6223b294ed8e638802007a31c68e480b803d5356966`(一致・LEDGER pin と同値)。remote 先端 = 275f526354ad8d6f23b595d96c6f391fe639821e(freeze commit 6c0b0123 の後に v5 lane の後続 commit を含む)。**P4 完全閉鎖**。

## P2(地図 stale 行)— 訂正済(freeze commit に同梱)

- C-14 行: 「353/283/231 の三窓」を削除 → 「353 = 同じ種の未 lift σ₁ を測った無効テスト・真に別種は 283 の一例のみ・N′ 非一意性は未検証」
- C-13 行: bulk18 = L3-inconclusive・prodrung j=5 で 8 死亡・残 10 undecided を現況として反映・機械二系統の語彙を「照合」に修正

## P3(T-REF checker)— 完成・PASS・cross-checked 昇格(裁定 1432)

発注済みだった独立 general-f 照合器が完成: producer .g 非開封・対象は window export JSON の data pin(sha256=05bb76b2e993e3f7ff26ef0b82f1d2458f17875122c2ccb0f2f1bdb07fdd9144)・較正(N5 control 合格集合 {0,1,3,4})一致・本体 = 両窓の disputed(m=2,u=5)で full (3.3)/(3.4) 独立評価が producer の CENSUS_CORRECT と一致(all_windows_match_producer: true)。⟹ **T-REF: candidate → cross-checked**(限定保持: 検査対象 f は producer 列挙順の非正準選択)。verdict = `crosscheck/verdicts/koubou83_tref_crosscheck_v1_20260822.json`(freeze commit に同梱)。

公式数学状態は貴殿の裁定どおり不変: 局所 4 定理維持・972 屋根未閉鎖・(iv) open。
