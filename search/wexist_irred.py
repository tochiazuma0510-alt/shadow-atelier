"""x^5-x-1 の Z 上既約性を、係数の消去で exhaustive に閉じる(範囲探索でなく制約解)."""
# (x^2+a x+b)(x^3+c x^2+d x+e) = x^5 - x - 1  (monic, b*e = -1 なので b,e in {(1,-1),(-1,1)})
# 係数比較:
#   x^4: c + a = 0                 -> c = -a
#   x^3: d + a*c + b = 0           -> d = a^2 - b
#   x^2: e + a*d + b*c = 0
#   x^1: a*e + b*d = -1
#   x^0: b*e = -1
found = []
for b, e in ((1, -1), (-1, 1)):
    # x^1 の式に c,d を代入して a の整数方程式にする
    # a*e + b*(a^2 - b) = -1  <=>  b*a^2 + e*a - b^2 + 1 = 0
    A, B, C = b, e, -b*b + 1
    disc = B*B - 4*A*C
    r = int(abs(disc)**0.5)
    while r*r > abs(disc): r -= 1
    while (r+1)*(r+1) <= abs(disc): r += 1
    exact = (disc >= 0 and r*r == disc)
    roots = []
    if exact:
        for sgn in (1, -1):
            num = -B + sgn*r
            if num % (2*A) == 0: roots.append(num // (2*A))
    # 検算: 得られた a が x^2 の式も満たすか
    for a in roots:
        c, d = -a, a*a - b
        if e + a*d + b*c == 0: found.append((a, b, c, d, e))
    print(f"  (b,e)=({b},{e}): a の方程式 {A}a^2+{B}a+{C}=0  disc={disc} 平方?={exact} 整数根={roots}")
print("x^5-x-1 の Z 上 deg2*deg3 分解:", found if found else "なし")
print("=> 有理根なし(既出)+ deg2*deg3 なし => Z 上既約 => Gauss より Q 上既約")
