# Task1110公開追補 — C第五群の実例外文字列
宛先: packet_checker/packet_bounds_audit。1107の公開wire v2とC八case/目的label/四key拒否票を保持し、実行時の接頭辞だけを明確化する。旧C require の公開拒否規約は cycle_batch: を裸labelに前置する。旧require/旧拒否群/rawは変更しない。

C第五群の rejection.json は plain exact {case_name,expected_label,observed_label,status}。expected_label は C-rejection-group-proposed-v1.json の当該 c6_* 裸目的label、observed_label は通常helperから実際に捕えた ValueError の原文字列をそのまま保存する。成功条件は expected_label が登録裸labelと一致し、observed_label == "cycle_batch:" + expected_label の完全一致である。substringやtrim/stripで原例外を作り替えず、無関係なparse/hash拒否を数えない。status=REJECTED_AS_EXPECTEDはこの実拒否を観測してから。P側の接頭辞や私的helperは使わない。

全8caseの正対照→一つの意味変異、必要な囲みseal/pinの更新、通常production helperへの到達、元body/空dir/全inventoryの保全を保持する。目的label・公開field名・旧C[28,9,6,7]・新8件・数学宇宙/capsに変更なし。source/自己試験/数学実行0、verified=false。本追補は実装指示であり実テスト合格票ではない。
