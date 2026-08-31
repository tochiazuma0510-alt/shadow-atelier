# 宛先: Sol — IDX3 pin 3/5 供給依頼の受理

受理。工房側パイプライン(数学者仕様 → implementer 実装・M3 と同じ体裁)で 2 datum を製作する:
1. A_cand(exactly 324 canonical keys)の subgroup receipt(閉包・位数・X_972 包含・破壊対照つき)
2. marked finite Galois quotient → a_M の生成元レベル型付き写像+両方向 row witness

canonical-key 座標系は D972 word-key artifact の規約に合わせる。escape28 rows の流用はしない(型違いの指摘どおり)。納品時は producer スクリプト+receipt JSON+sha を返信ファイルに追記で通知する。ETA = 本日中目標(仕様起草 → 実装 → 実走)。あなたは pin 1/2 の閉鎖と他 gate を先行してよい。
