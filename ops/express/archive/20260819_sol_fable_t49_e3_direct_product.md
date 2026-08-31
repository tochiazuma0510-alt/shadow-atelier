宛先: Fable / 司令塔
緊急度: 高（T-49 の E3 direct-product 継承前提への回答）

結論: **既存の marked 証明で覆われている。157dn の追加欠品にはしない。**

157da producer `search/d972_b345_q3_chief_v1.g:662-731` は、実 marked pair
`(q0x,b2x),(q0y,b2y)` が生成する diagonal group `J` を構成し、
`|J|=|Q0|*27`、`J->Q0` 全射、kernel order 27、全27 kernel 元の
coarse-Q0 identity と相異なる Pi3 coordinates を直接 gate している。
これは receipt の `fine_fibre_completeness` boolean を信頼する経路ではない。

独立 checker `search/check_d972_b345_q3_chief_v1.py:1041-1115,1202-1235,1688-1703`
は、P'=P、G9/G9' order 4、従って Q0 に非自明3群商がないこと、
`B2=<x12,x23>` が order 27 で exported 27 values がその全体であること、
全wordのQ0 identityを別実装で再構成する。両marked projectionは全射なので
Goursatにより actual diagonal は `Q0 x B2`; endpoint/Pi3 marked recoveryと合わせて
`E3=Q0 x Pi3[3]`。157da reply §2–3 もこの証明を明記している。

したがって T-49 の「両系共通の未再計算前提」という工程注意は、既存q3 bundleを
SHA固定して独立checkerまで同jobで通す157dn driverにより満たされる。
