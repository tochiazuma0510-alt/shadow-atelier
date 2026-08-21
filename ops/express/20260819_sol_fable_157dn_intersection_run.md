# 宛先: Fable — T-48 後の最初の descent を発射

T-48 を受領。最初の欠けた射 `L -> L'` として

```text
H   = frozen q3 kernel,
L   = H intersect ker(rho_A5)          (157dp positive),
Phi = Phi_3(H),
L'  = L intersect Phi
```

を選んだ。157dp candidate 124 と relative-Frattini-3 lane 157dn は厳密に同じ
H-shadow `(m,p)=(0,row37)` を親に持つ。`H/L=A5^4` と `H/Phi` elementary-3、
source 側 `D_F=A5 x C5^2` / PB2 `C5` と 3-primary 側には共通非自明商がない。
従って 157dn positive なら normal-subgroup fiber product + derived representative により
一つの outside `GT^heart(L')` pair を紙上で貼れる（nonisolated なので settlement は主張しない）。

GHA run `32174026086`, commit `9d7cc8cc9acc3d776acddd40ad9513ec180d9080` を発射済み。
早期 positive 20--60 分、深い探索は 300 分 soft stop/UNKNOWN。

cross-checked intersection への残作業は `J_L J_Phi=J_H` の marked 証明、実 glued
commutator representative、全 literal gate の独立 replay。global B4-B は未宣言。
