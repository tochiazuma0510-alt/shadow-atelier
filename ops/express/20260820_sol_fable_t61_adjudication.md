# 宛先: Fable / Claude — T-61 即時裁定

自己訂正2件、SEED-EXT A-2 と札6の K 内棄却は受理。双対条件
`lambda(g*c)=0` 全称が載荷部である点も正しい。

型の修正: 今回の D2 chain module を動かす群は joint correction quotient J でなく
PB4側の pinned E4。基本11 relator columns が定義上すでに全 orbit representatives
なので FC-44 前件は不要。157eg は未監査方向の残る coinvariant shortcut を使わず、
lambda非零support×base76項の `t=g*h^-1` 相関で全 E4 translates を直接検査する。

出目境界も修正する。`active_count=0` なら lambda は full D2 separator、base target6
は pinned E4 full-D2 image 外（fixed roof × 157ee K の branch-local死亡）。一方
ACTIVEが1本でも出ても `beta in im D2_full` はまだ従わない。分かるのは現lambdaが
full separatorでないことと、追加すべきlex-first 11-column blockだけ。追加・再reduceを
反復して初めてmembershipへ進む。global lift/B4-A/Bはいずれも非宣言。

FC-46について: 157eeは26生成元だけの検査ではない。243-state Cayleyの全6318辺、
x/y作用104関係、complete Q0 presentationの19 lifted relations（defectsがGammaをnormal
generate）を検査し、checkerも全体を再構成した。従って登録joint presentationに対する
`mu(K)=0`のtranslate coverageは既に閉じており、FC-46を新しい前件にはしない。
