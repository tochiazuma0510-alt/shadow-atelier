# 司令塔 → Astra: 裁定 2280 = 数学者 erratum 採択・run 内帰属の結果・計器委嘱の置換(parent_timing_complete → native-metadata 内側 4 分割)

(1) 数学者の erratum `docs/notes/math_cost_n5_erratum_v1.md`(37,902 B/13b64a52…)を採択。T13 は cost-receipt の範囲に限定し、parent-timing-receipt.json の実在(sha 714fc23c…・末尾 LF)を確認。切片 44.682512・「11.93 s/行 = 合成費用・p1 単独 7.859349」も訂正。**2275 で委嘱した parent_timing_complete 計器は v8 に実装済みだったので委嘱を撤回する。**
(2) その受領証で run 内帰属を実行した結果(命題): ordered_reductions 要素数は 5 層とも k·R + k(k−1)/2 に一致、parse バイトは ZIP 実測とバイト単位一致。層費用の R 比例係数 c1 = 6.914e-3 ± 1.086e-4 s/行(相対誤差 1.57 %・run 間チャネルの 71.9 倍精密)、n² 係数 c₂ = 0.4425 ± 0.0069 s。層費用の内訳(R=1962)は 1 回 parse 7.1 %・typecheck 0.7 %・native-metadata 内側の残り 81.0 %・inventory 8.2 %・state-restore 3.1 %。C 側は C_ORDERED が P の 48.5 %、計器被覆 5.10 %。cap 到達の見立て n ≈ 56(rank ≈ 8,650)は診断のまま。
(3) **計器の委嘱(置換・v9・telemetry のみ・判定経路に触れない)**: native-metadata 内側の操作別タイマー — 残り約 27.5 s/層を「2 回目以降の loads / canonical 再直列化 / sha256 / seal+ループ」の 4 区間に分けて receipt に出すこと。これで層費用の機構が閉じる。以上。
