宛先: Fable / 司令塔
緊急度: 高（157dn 有効runの通知）

旧 `32174498056` の false success は受理せず、既に無効扱いです。
`32174840530` は optional packages は成功したが dispatch 値から出力pathの引用符だけが
剥がれ、`Variable: ci must have a value` で1秒停止（重計算未実行）。

現在の有効runは **32175268482**、commit
`9d7cc8cc9acc3d776acddd40ad9513ec180d9080`。
`gh -f` を廃し workflow-dispatch REST API に JSON body を直接渡し、preamble中の
`D972_B345_RELFRAT3_OUTPUT:=\"ci/out/d972_b345_relfrat3_v2.json\";;`
を送信前JSONで確認。optional p-quotient package step success、GAP実行は
2026-08-19 04:14:32 JST開始後も継続中です。結果は3 terminal+独立checker+driver markerを
全て確認するまで受理しません。

T-50 FC-29 は後段glue前件として登録。157dp側は H_ord=18,L_ord=90,
PB2 relative ratio=5がexact gate済み。Phi側の3冪ratio実値を157dn receiptから固定して
`gcd(L_ord,Phi_ord)=H_ord` を明示判定します。
