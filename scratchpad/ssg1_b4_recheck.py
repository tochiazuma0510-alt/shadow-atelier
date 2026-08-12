"""
[B4 / 裁定1109] Sol 便122 §4.2 の真の上界の独立検算(有理数厳密)。

  H~ = {(A,s) in SL^pm(2,Z/p^2) x S_3 : det A = sgn s}      (p = 691)
  J2 = #{A : A^2 = I, det A = -1} = |GL2(R)| / |R^x|^2 = p^3 (p+1)
  J3 = #{A : A^3 = I, det A = +1} = 1 + p^3 (p+1)           (p = 1 mod 3)
  i2^T = 3 J2 ,  i3^R = 2 J3 ,  |H~| = 6 p^4 (p^2-1) ,  |Z(H~)| = 2
  U_true = 2 i2^T i3^R |Z| / |H~|     (COUNT-PSL の Inn 後合成版・追補 §1)

裁定1103 規約: 本書に載せる数値はすべてここで生成する。
"""
from fractions import Fraction


def data(p):
    R2 = p * p
    GL2 = p**4 * (R2 - 1) * (R2 - p)          # |GL_2(Z/p^2)|
    units = p * (p - 1)                        # |(Z/p^2)^x|
    J2 = GL2 // units**2                       # = p^3 (p+1)
    J3 = 1 + J2
    i2T, i3R = 3 * J2, 2 * J3
    H = 6 * p**4 * (R2 - 1)
    Z = 2
    U = Fraction(2 * i2T * i3R * Z, H)
    return dict(p=p, J2=J2, J3=J3, i2T=i2T, i3R=i3R, H=H, Z=Z, U=U)


def split_model(p):
    """Stage 0 の分裂模型 S_3 x PSL(2,Z/p^2) の値(= split calibration)。"""
    e2 = 1 if p % 4 == 1 else -1
    e3 = 1 if p % 3 == 1 else -1
    i2 = 1 + p**3 * (p + e2) // 2
    i3 = 1 + p**3 * (p + e3)
    Q = p**4 * (p * p - 1) // 2
    return Fraction(2 * i2 * i3, Q)


if __name__ == "__main__":
    d = data(691)
    print("=== true H~ (fiber product) at p = 691 ===")
    for k in ("J2", "J3", "i2T", "i3R", "H", "Z"):
        print(f"  {k:5s} = {d[k]}")
    print(f"  U_true = {d['U']} = {float(d['U']):.9f}")
    print(f"  floor(U_true) = {d['U'].numerator // d['U'].denominator}")
    print(f"  matches Sol 152212029822/79465 : {d['U'] == Fraction(152212029822, 79465)}")

    us = split_model(691)
    print()
    print("=== split calibration (NOT an upper bound) ===")
    print(f"  U_split = {float(us):.9f}")
    print(f"  U_true / U_split = {d['U']/us} = {float(d['U']/us):.15f}")

    print()
    print("=== CP-D : lower bound 30360/2 = 15180 ===")
    print(f"  U_true / 15180 = {float(d['U'])/15180:.5f}")
    print(f"  U_true < 10^7 : {float(d['U']) < 1e7}")

    print()
    print("=== [C-2] literal rail predictions, p = 7 mod 12 ===")
    for p in (7, 19, 31, 43):
        e = data(p)
        print(f"  p={p:3d}  J2={e['J2']}  J3={e['J3']}")
