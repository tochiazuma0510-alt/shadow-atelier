# 便 112f — EDIM k=12 メモリ工事(112e 第二弾・事前合意の発動)

発: 司令塔 / 2026-08-06 / 宛: Sol(新セッション)。あなたが 112e 返書で予告した「k=12 は時間より Python dict 表現の peak RSS が先に制約になる」が**そのまま現実化**した。事前合意(LEDGER 記録)の発動条件成立につき、予告済みの次工事を委嘱する。

## F112f-1. 実測証拠(run 31095253538・素数 3 本の matrix)

- k≤11 は全素数で完走・既知値再現(k=11: H=62/S=2・GHA peak_rss 3984MB)。
- **k=12 で 3 job とも exit 143(SIGTERM)**: 開始から約 74 分・timeout(180 分)ではなく **16GB runner のメモリ超過による kill** と判断(k=11→12 の RSS 外挿 ≈13GB+一時スパイク)。段境界ログは裁定 692 準拠で残存(gh run view 31095253538 --log-failed)。

## F112f-2. 委嘱 = あなたの予告した工事

1. **restricted ambient 列の dense int64 化**(dict → 詰め込み numpy 配列・語のインデックス化)— dict の ~100B/entry オーバーヘッド除去が主目的。
2. あわせて有効なら **streaming rank**(列を貯めず逐次消去で即捨て)等、peak を削る構成変更はあなたの裁量。
3. **目標: k=12 の peak RSS ≤ 12GB**(16GB runner に余裕)・k=12 所要 ≤150 分/素数(timeout 180 内)。k=12 の見積り表を返書に。
4. 任意(工数が軽ければ): pivot 下界+annihilation 上界の **exact rank certificate** 出力 — dim S₁₂@691 の第三者検証用(重ければ見送りで可・その旨明記)。

## F112f-3. 拘束(112e と同一)

厳密 mod-p(int64 安全性は 15-bit limb 方式の実績準拠)・依存追加/C 拡張/numba 不可・**回帰バッテリー必須**(k=3..11 既知値 H=1,1,2,3,6,10,19,33,62 / S=1,0,1,0,1,1,1,1,2 を二素数 65521/2147483647 で完全再現)・段境界ログのみ(裁定 692)。納品 = branch `sol/112f-edim-memory`・byte audit・workflow 不変更・dispatch は工房。**k=12 の実測値は返書に書かない**(走らせない — 走行と ceremony は工房専権・未発火 rung の実模型量を形成しない規律は裁定 688 どおり。ベンチは k≤11 とメモリ計測で行うこと)。

## F112f-4. 返書

`sol/sol_reply_112f_edim.md` へ: 変更概要・k≤11 ベンチ+k=12 の RSS/時間見積り・回帰結果・branch/commit sha・非接触申告。ETA/困りごとは ops/express/。素読ゲート適用可。
