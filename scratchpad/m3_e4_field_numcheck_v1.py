import cmath, itertools
a = 2**(1/3); w = complex(-0.5, 3**0.5/2)          # alpha, omega
e = [-2*a*w**k for k in range(3)]
print("roots of X^3+16 ok:", [abs(x**3+16) < 1e-9 for x in e])
d1, d2, d3 = e[0]-e[1], e[0]-e[2], e[1]-e[2]
s3 = complex(3**0.5,0); sm3 = w - w**2                     # sqrt3, sqrt(-3)
print("d1*d2 == (2a*sqrt3)^2 :", abs(d1*d2 - (2*a*s3)**2) < 1e-9)
print("d1*d3 == (2a*w*sqrt-3)^2:", abs(d1*d3 - (2*a*w*sm3)**2) < 1e-9)
# halving of (e0,0): x = e0 + r*s with r^2=d1, s^2=d2 ; check 2Q = (e0,0)
r, s = cmath.sqrt(d1), cmath.sqrt(d2)
x = e[0] + r*s; y = r*s*(r+s)
print("x == 2a(sqrt3-1) (up to sign of rs):", abs(x - 2*a*(s3-1)) < 1e-8 or abs(x - 2*a*(-s3-1)) < 1e-8)
print("y^2 == x^3+16 :", abs(y*y - (x**3+16)) < 1e-7)
print("x root of x^6+320x^3-2048:", abs(x**6+320*x**3-2048) < 1e-6)
# duplication on Y^2=X^3+16 : x(2Q) = (x^4 - 8*16*x)/(4(x^3+16))
x2 = (x**4 - 8*16*x)/(4*(x**3+16))
print("x(2Q) equals some e_k:", min(abs(x2-t) for t in e) < 1e-7)
print("   -> which e_k:", [abs(x2-t)<1e-7 for t in e])
# y^8 - 96768 y^4 + 47775744 = 0 ?
print("y minpoly candidate deg8 vanishes:", abs(y**8 - 96768*y**4 + 47775744) < 1e-3)
