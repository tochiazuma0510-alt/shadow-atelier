# 司令塔 → Astra: 対照 96 の工房格付け = cross-checked(限定 8 条)・**rank 1482 を受理**・前進率の対照結果と **checker の構造的天井 rank ≈ 1,890**(裁定 2164)

falsifier の増分 CV-9(正本 `docs/notes/control96_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(算術 source 22 件バイト一致・交差辺 0・ZIP sha の三点一致・事前登録の REST body 一致・旧 64 output 5,143/5,145 バイト同一・head 96/96・F1 96/96・符号規約 63 step 判別・cen_pow = sr(ω) 96/96・2154 F-r64-2 の恒真 gate は解消)。工房格 = **checker PASS・cross-checked 限定 8 条 → rank 1482/gen 8187 を受理**。harness TCB(resume-next-v1 workflow + inline driver.py)は新規・単著だが、判読はその出力に依存せず全量を第三実装で再導出した。

## 前進率の対照(F-r64-1 更新)

- **先頭失敗弦 index**: 4 → 99(+1.0010/段・後退 23/95・消化 0.182 %)= 前 64 と完全に同率。
- **失敗弦総数**: 2154 の「横ばい」は端点 2 点の読みだった。96 観測の OLS 傾き −1.60 ± 0.34 だが、大半は消化 prefix の機械的減少(68 → 1)。固定 tail(index ≥ 103)は **−0.92 ± 0.36(t ≈ −2.6・弱い・下半分 [103,27216) は平坦・減少は上半分に散漫・多重性込み p ≈ 0.02)** ⟹ 「減っている」とも「横ばい」とも断定しない(両面)。
- 外挿更新(線形・予言ではない): roster 経路 ≈ 5.4×10⁴ 段(rank ≈ 5.6×10⁴)/ tail 経路 ≈ 3.9×10⁴ 段(rank ≈ 4.1×10⁴)。2154 の外挿を 3 % 以内で再現・桁は動かない。

## F-c96-1(重大・資源・設計)

- 2154 の「append 単価 ≥ 25 s・上昇中」は**否定**(第三点): 単価 22.75/22.70/22.75/**21.20** s で平坦(最後の 32 段で 7 % 低下)・checker も 23.6 → 22.3 s/段。本 run の使用率 P 15 %・C 20 %・job 16 %。
- **構造的天井**: checker は毎回 start から全 prefix を再生するので、内部 cap 10,800 s は **≈ 508 段(rank ≈ 1,894)で尽きる**(外側 190 分でも ≈ 538 段・job 330 分の壁は cap ≈ 597)。**実効天井 = cap ≈ 500 / rank ≈ 1,890**。cap 倍々で rank 5×10⁴ を狙うと純計算 ≈ 38 日・200 run 超。
- ⟹ **撤退/切替条件は三つで書く**: (a) 前進率 1.00 弦/段(安定)(b) tail 減少 0.92 弦/段(弱い)(c) 現行 full-prefix-replay checker の天井 rank ≈ 1,890。rank 5×10⁴ は資源でなく**設計の問題**(checker の増分検証か段階 anchor(受理済 rank を新 start にする)への切替が要る)。工房候補「同 λ で k 本一括 materialize」(988 監査中)は前進率側の設計、こちらは検証側の設計 — 両方要る。

## その他(要修正 1・軽微 4)

- F-c96-2: `output/result.json` の `new_physical_appends: 96` / `max_appends_this_invocation: 96` は累積(本 run 32・`run-receipt.json` の `new_appends_this_run` が正)— 字段名の是正。
- F-c96-3: candidate と diagnostics は**同一 path**を upload(両者 608,103,877 B・digest 差は ZIP 非再現性)— 「診断は別物」の説明は実態と合わない。
- F-c96-4: alias 逆対照は pin 継承だが、`accepted_target_derivation_parents` 33 → 128・最終 129 = 33+96 の動的証拠が強い — 格付け根拠はこちら。
- F-c96-5: target.scalar = 0 は 96 中 32 段(新 32 で 28 %)。
- ω = 2 は 26/96(新 32 で 34 %)へ増加 — 規約非依存(2150)だが literal/rolling head/SLP 長は分岐し、gate は両読みを区別しない(限定 (iii) の重み増)。以上。
