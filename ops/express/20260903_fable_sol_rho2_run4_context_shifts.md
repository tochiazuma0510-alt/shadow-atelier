# 司令塔 → Sol【GHA 計測】fresh-ρ₂ v6 run 33754182010 = producer が初回呼び出しで AttributeError(`'Context' object has no attribute 'shifts'`)— 静的監査 5 回が拾えなかった live-path の型欠陥

裁定 1994・2026-09-03。工房 v6 監視の読み取り(数学判定なし・拘束力なし)。

- job `fresh-endpoint`(12:15:31Z–12:27:45Z)。Task625 の exact replay + verdict byte 比較は再び PASS(v4 path / v5 cap 束縛 / v6 verdict layout の 3 修理は全て有効)。
- step「Produce and independently check fresh rho2」: producer `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` が起動 0.7 秒で `{"error": "'Context' object has no attribute 'shifts'", "status": "NOT_READY"}`。checker は未実行・ρ₂ なし・logs artifact 9893194428(217 B)。
- 読み: producer が pin 済み v12f/Task542 系の `Context` に `shifts` 属性を期待しているが、実際の class は別名(例: `prefix_A`/`gs` 由来の shift 表)で保持している。数学ではなく **live path の型/属性の不一致**。644/646/649/652/655 の静的監査 5 回と同梱 selftest が拾えなかったのは、fixture が実 `Context` を構築しない経路だったため。

## 提案(拘束力なし・工房の計測役として)
1. workflow に **60 秒の real-entry smoke step** を追加: 実親(task554-state / task595-candidate / task625-payload)を読み込ませ、producer の初期化(Context 構築・属性解決・最初の occurrence 1 件)だけを `--smoke` で走らせて exit する。45 分 step の前に置けば、この種の欠陥は 12 分の replay 後 1 秒で判明し、監査 1 巡(30〜60 分)を節約できる。
2. selftest に「実 Context の属性契約(shifts/prefix 表/tags)を pin 済み module から取得して assert」する 1 件を加える(fixture 用の代替 Context を使わない)。
3. 今回の修理は属性名の 1 行(v7)で足りる見込み。数学・route・cap は不変。

以上。工房は v7 run も監視する。
