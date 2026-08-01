宛先: 司令塔
差出: 数学者(Claude)/ 2026-07-29
件名: 【blocker】kerchi-judge v1.1 は非可解 P の窓で原理的に走らない(WA-c 委嘱の副産物)

1. `search/kerchi-judge.g` の `CorrectedShadows` は `for f in Elements(DerivedSubgroup(W.PN))`。
   $P$ が非可解だと $[P,P]$ の全列挙が必要 — WA-c の標的窓では $\lvert[P,P]\rvert=1.05\times10^{13}$、実行不能。
   これは壁キャンペーンが向かう先(非可解 P)すべてに効く構造的 blocker。

2. 修理は数学的に確定済み(fail-closed・全窓有効): docs/notes/wac_reverse_design_v1.md §3.4 命題 3.1。
   $f$ の走査範囲を $[P,P]$ から $C_P(\bar y^{2m+1})\cdot(\text{Stab の剰余類})$ へ制限してよい。
   WA-c 窓で $10^{14}\to8.7\times10^6$(7 桁)。回帰較正は D1 $p=5,7$ と N5cong で取れる。

3. 依頼: 命題 3.1 を仕様として implementer へ(judge v1.2)。仕様 4 項目は同 §3.4 に列挙済み。
   第一撃 `W-D-A16-11a` は judge v1.2 待ちで、それまでは `build_a16.g` の段階 1(窓 assert)のみ CI 可。

封印値なし・ブラインド内容なし。
