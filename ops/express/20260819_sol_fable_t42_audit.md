宛先: Fable / 司令塔
緊急度: 今すぐ

T-41/T-42 正本の Sol 再監査で修正点 2 件。

1. CHP-D6 の「完全閉鎖」は現式のままでは STOP。`p*lambda` で
   `m_lambda=H_ord*s'` とすると、新しい m は
   `m + H_ord*(2m+1)*s' = m + H_ord*u*s'`。
   従って全 `m+H_ord*s (mod K_ord)` を覆うには少なくとも
   `gcd(u,K_ord/H_ord)=1` が必要。H-stage friendly
   `gcd(u,H_ord)=1` からは従わない。加えて operad 3残差は FR-1
   が未記帳なので、braid版 CHP-2 だけでは D6 全閉鎖にならない。

2. GS-T2 の条件付き証明にも独立 gap。crossed hom の zero-fibre
   index は affine orbit の大きさであり、係数 p-group の位数を
   割る／p冪になるとは限らない。例: `O=C7` に `C3` が位数3の
   自己同型で作用し、非零 1-cocycle を取ると kernel index=3。
   ordinary hom、trivial action、または orbit-size の prime-support
   を直接束縛する追加仮説が必要。

CHP-1（自由群版の厳密合成）はこの指摘では崩れない。FC-12 の
`Xi` 実測は有用な前処理だが、`Xi` 単独では SYL3 の index 条件を
与えないため、D1/NA-5 の直接有限方程式路線を主とする。
