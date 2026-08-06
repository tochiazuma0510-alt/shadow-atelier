# 便 112e — EDIM 疎ソルバーの高速化委嘱(工学・研究者指示)

発: 司令塔 / 2026-08-06 / 宛: Sol(新セッション)。本便は工学委嘱(数学監査便でない)。研究者指示「並列化の前に Sol に高速化してもらう」による。参照正本: AGENTS.md・docs/notes/edim_semidirect_model_design_v1.md(模型仕様)・docs/notes/edim_sparse_solver_design_v1.md(疎設計)。

## F112e-1. 対象と現状性能

- コード: `search/edim_semidirect_v1.py`(半直積 Lie 模型・Lyndon 基底・疎ソルバー・厳密 mod-p 線型代数)+ 走行系 `search/edim_run_c9_c10_v3_single_prime.py`。
- 計算内容: 次数 k の dim H_k / dim S_k(ker(1+θ)∩ker(1+τ+τ²)∩ker ν_k の次元)を素数 p で厳密計算。
- 実測(ローカル): k=9 = 約 214 秒/素数・k=10 = **約 56 分/素数**(delta table 構築 26.5 分+H,S 計算 27.8 分)。GHA ubuntu runner は約 1.5〜2 倍遅く、timeout 90 分に抵触(実害発生済み)。
- 今後の需要: **k=11(dim 𝔱₁₁=16,290)と k=12(44,555・p=691 含む 3 素数)が本番** — 現行速度の外挿では時間外の恐れ。

## F112e-2. 委嘱内容

1. **プロファイルと高速化**: ボトルネック特定(coords_of_ambient の疎前進消去・delta table 構築・BCH/括弧再帰のどこが支配的か)→ アルゴリズム/実装の両面で改善。狙い目の例(あなたの裁量で取捨): 疎行列の permanent なピボット順(Markowitz 改良)・行削減の numpy ブロック化(**int64 オーバーフロー安全性必須** — p≈2³¹ で単純 @ は破綻することが実測済み・mat_mul_modp_np_safe 参照)・Lyndon 展開のメモ化・delta table の増分構築・(必要なら)C 拡張や numba は**不可**(依存追加禁止)— 純 python+numpy 内で。
2. **性能目標**: k=10 ≤ 15 分/素数(GHA)・k=11 ≤ 45 分/素数(GHA)見込みを提示。k=12 の外挿見積りを報告。
3. **正しさの拘束(絶対)**: 厳密 mod-p(浮動小数の近道は安全証明つきのみ)・**回帰バッテリー necessário**: k=3..10 の既知値(H = 1,1,2,3,6,10,19,33 / S = 1,0,1,0,1,1,1,1)を両素数(65521・2147483647)で完全再現してから納品。既存 cert(search/certs/edim_semidirect_c1c4_v1_20260806.json・edim_c78_scoring_v1_20260806.json)との一致。
4. **納品形態**: Lean 線と同じ様式 — 親子方式(turn 内 wait・Luna xhigh)・broker Git Data API・work branch `sol/112e-edim-speedup`・byte audit・force-push 禁止・workflow 変更禁止(edim.yml は工房が後で並列化改修する)・merge 候補 branch+ベンチ表を返書へ。実行環境の GHA dispatch は工房専権。
5. 高速化版が**実装として独立性を持つ場合**(アルゴリズム再構成など)、その旨を返書に明記 — 監査上「第二実装」として扱える可能性がある(判定は工房)。

## F112e-3. 非接触

封印値・blind 値・探索系 cert の改変・K^(5)/PSL/epsilon 系・GAP 実行は全て非接触。対象は上記 2 ファイル(+新規ファイル追加は可)のみ。

## F112e-4. 返書

`sol/sol_reply_112e_edim.md` へ: 変更概要・ベンチ表(k=9,10 の before/after・k=11,12 見積り)・回帰バッテリー結果・branch/commit sha・非接触申告。ETA/困りごとは ops/express/ へ。素読ゲート適用可。
