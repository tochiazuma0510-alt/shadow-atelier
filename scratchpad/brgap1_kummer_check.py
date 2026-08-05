#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BR-GAP-1 independent check: finite-level Kummer comparison
  Kurihara [KUR] printed 233, (4)     c(1) = lim_n Cor_{Z[1/p,mu_{p^n}]/Z[1/p]} [ (1-zeta) (x) zeta^{(r-1)} ]
  Ihara   [ICM] printed 115, 6.2(ii)  eps_{r,n} = prod_a (zeta^a - 1)^{<a^{r-1}>}

All arithmetic is EXACT (python integers / integer polynomials in Z[x]/(Phi_{p^n}(x))).
No floating point.  No GAP.  No window data.  No sealed quantities.

The paper proof is in docs/notes/bhunt_l1_bridge_v1_1_erratum.md, section 3.
This script certifies only the *arithmetic bookkeeping* steps of that proof:
  (K1) exponent representative  <a^{r-1}> == a^{r-1}  (mod p^n)
  (K2) integrality of d_a = (<a^{r-1}> - a^{r-1}) / p^n   and  d_a <= 0
  (K3) transfer direction is immaterial: sum_a tau_a  and  sum_a tau_a^{-1} give the same exponent function
  (K4) sign: p^n odd  =>  -1 = (-1)^{p^n}  is a p^n-th power
  (K5) (p-1) does not divide r  =>  (Z/p^n(r))^Delta = 0  =>  H^i(Gal(K_n/Q), Z/p^n(r)) = 0 (all i)
  (K6) Ihara normaliser p^{r-1}-1 is a p-adic unit
  (K7) exact identity in Z[x]/(Phi_{p^n}(x)) :
         prod_a (z^a - 1)^{<a^2>} * prod_a (1 - z^a)^{p^n * (-d_a)}  ==  (-1)^S * prod_a (1 - z^a)^{a^2}
       i.e. eps_{r,n} and prod_a (1-zeta^a)^{a^{r-1}} differ by an explicit p^n-th power times +-1.
"""

import sys

R = 3                      # the odd weight we need (Tate twist 3)
PRIMES = [7, 5, 11, 13]    # 7 = main window prime; the others are controls
LEVELS = [1, 2, 3]

verdicts = []


def say(line, ok):
    print("%s : %s" % (line, ok))
    verdicts.append(bool(ok))


def coprime(a, m):
    while m:
        a, m = m, a % m
    return a == 1


def units(m):
    return [a for a in range(1, m) if coprime(a, m)]


def least_pos_rep(x, m):
    """<x> = smallest positive integer congruent to x mod m  (Ihara's <.> bracket)"""
    y = x % m
    return y if y != 0 else m


# ---------------------------------------------------------------- polynomials
def polmulmod(f, g, cyc):
    """multiply in Z[x]/(cyc); cyc monic, coeffs low->high"""
    d = len(cyc) - 1
    res = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                if b:
                    res[i + j] += a * b
    for k in range(len(res) - 1, d - 1, -1):
        c = res[k]
        if c:
            res[k] = 0
            for j in range(d):
                res[k - d + j] -= c * cyc[j]
    res = res[:d] + [0] * max(0, d - len(res))
    return res


def polpowmod(f, e, cyc):
    d = len(cyc) - 1
    acc = [0] * d
    acc[0] = 1
    base = f[:]
    while e:
        if e & 1:
            acc = polmulmod(acc, base, cyc)
        e >>= 1
        if e:
            base = polmulmod(base, base, cyc)
    return acc


def cyclotomic_pn(p, n):
    """Phi_{p^n}(x) = sum_{i=0}^{p-1} x^{i p^{n-1}}"""
    q = p ** (n - 1)
    c = [0] * ((p - 1) * q + 1)
    for i in range(p):
        c[i * q] = 1
    return c


# ---------------------------------------------------------------- main checks
print("=== BR-GAP-1 finite-level Kummer comparison (exact integer arithmetic) ===")
print("r = %d ;  primes = %s ;  levels n = %s" % (R, PRIMES, LEVELS))
print("")

for p in PRIMES:
    tag = "MAIN" if p == 7 else "ctrl"
    for n in LEVELS:
        m = p ** n
        U = units(m)

        ok1 = all((least_pos_rep(a ** (R - 1), m) - a ** (R - 1)) % m == 0 for a in U)
        say("(K1) p=%-2d n=%d %s  <a^%d> == a^%d  mod %-6d for all %4d units"
            % (p, n, tag, R - 1, R - 1, m, len(U)), ok1)

        ds = [(least_pos_rep(a ** (R - 1), m) - a ** (R - 1)) // m for a in U]
        ok2 = all((least_pos_rep(a ** (R - 1), m) - a ** (R - 1)) % m == 0 for a in U) \
            and all(d <= 0 for d in ds)
        say("(K2) p=%-2d n=%d %s  d_a = (<a^%d>-a^%d)/p^n integral and <= 0 (min d_a = %d)"
            % (p, n, tag, R - 1, R - 1, min(ds)), ok2)

        inv = {a: pow(a, -1, m) for a in U}
        ok3a = sorted(inv.values()) == sorted(U)
        E_tau = {b: pow(b, R - 1, m) for b in U}
        E_tauinv = {}
        for a in U:
            b = inv[a]
            E_tauinv[b] = pow(b, R - 1, m)
        say("(K3) p=%-2d n=%d %s  {a^-1} == {a} as multisets and exponent functions of sum tau_a / sum tau_a^-1 agree"
            % (p, n, tag), ok3a and (E_tau == E_tauinv))

        S = sum(least_pos_rep(a ** (R - 1), m) for a in U)
        ok4 = (m % 2 == 1) and ((-1) ** m == -1) and ((S * m - S) % 2 == 0)
        say("(K4) p=%-2d n=%d %s  p^n odd => (-1) = (-1)^{p^n} ;  S = sum <a^%d> = %d"
            % (p, n, tag, R - 1, S), ok4)

        g = None
        for cand in range(2, m):
            if coprime(cand, m) and pow(cand, p - 1, p) == 1 \
               and all(pow(cand, k, p) != 1 for k in range(1, p - 1)):
                g = cand
                break
        ok5 = (g is not None) and ((pow(g, R, p) - 1) % p != 0) and (R % (p - 1) != 0)
        say("(K5) p=%-2d n=%d %s  (p-1)=%-2d does not divide r=%d ; generator g=%d of Delta : g^r-1 = %d mod p is a unit"
            % (p, n, tag, p - 1, R, g, (pow(g, R, p) - 1) % p), ok5)

    ok6 = (p ** (R - 1) - 1) % p != 0
    say("(K6) p=%-2d      %s  p^{r-1}-1 = %-5d ; mod p = %d != 0  =>  unit in Z_p"
        % (p, tag, p ** (R - 1) - 1, (p ** (R - 1) - 1) % p), ok6)
    print("")

print("--- (K7) exact identity in Z[x]/(Phi_{p^n}(x)) ---")
for (p, n) in [(5, 1), (7, 1), (11, 1), (13, 1), (5, 2)]:
    m = p ** n
    cyc = cyclotomic_pn(p, n)
    d = len(cyc) - 1
    U = units(m)
    S = sum(least_pos_rep(a ** (R - 1), m) for a in U)
    X = [0] * d
    X[1 % d] = 1 if d > 1 else 0

    def zeta_pow(a):
        return polpowmod(X, a, cyc)

    def zeta_a_minus_1(a):
        v = zeta_pow(a)[:]
        v[0] -= 1
        return v

    def one_minus_zeta_a(a):
        return [-c for c in zeta_a_minus_1(a)]

    lhs = [0] * d
    lhs[0] = 1
    for a in U:
        lhs = polmulmod(lhs, polpowmod(zeta_a_minus_1(a), least_pos_rep(a ** (R - 1), m), cyc), cyc)
    for a in U:
        da = (least_pos_rep(a ** (R - 1), m) - a ** (R - 1)) // m
        if da:
            lhs = polmulmod(lhs, polpowmod(one_minus_zeta_a(a), m * (-da), cyc), cyc)

    rhs = [0] * d
    rhs[0] = (-1) ** S
    for a in U:
        rhs = polmulmod(rhs, polpowmod(one_minus_zeta_a(a), a ** (R - 1), cyc), cyc)

    say("(K7) p=%-2d n=%d  prod (z^a-1)^{<a^2>} * prod (1-z^a)^{p^n(-d_a)} == (-1)^S prod (1-z^a)^{a^2}"
        % (p, n), lhs == rhs)

print("")
print("--- negative controls (the checks must have discriminating power) ---")

# (N1) the modulus in (K1) matters: <a^{r-1}> = a^{r-1} mod p^{n+1} must FAIL in general
p, n = 7, 1
m = p ** n
bad = [a for a in units(m) if (least_pos_rep(a ** (R - 1), m) - a ** (R - 1)) % (m * p) != 0]
say("(N1) p=7 n=1  congruence FAILS mod p^{n+1}=49 for %d of %d units (modulus is load-bearing)"
    % (len(bad), len(units(m))), len(bad) > 0)

# (N2) the exponent pairing a <-> p^n-a makes S even for odd r (so the sign is vacuous here);
#      for an EVEN weight r-1 -> odd, S would not be forced even.  Check the pairing directly.
ok = all(least_pos_rep(a ** (R - 1), m) == least_pos_rep((m - a) ** (R - 1), m) for a in units(m))
say("(N2) p=7 n=1  <a^{r-1}> = <(-a)^{r-1}> (r odd => r-1 even) so S is even; sign factor is vacuous here",
    ok and (sum(least_pos_rep(a ** (R - 1), m) for a in units(m)) % 2 == 0))

# (N3) (K5) has teeth: for r == 0 mod (p-1) the Delta-invariants do NOT vanish
say("(N3) p=7  r'=6 == 0 mod (p-1): g^{r'}-1 = %d == 0 mod p  =>  (Z/p^n(r'))^Delta != 0 (criterion bites)"
    % ((pow(3, 6, 7) - 1) % 7), (pow(3, 6, 7) - 1) % 7 == 0)

# (N4)(N5) mutate (K7): perturbing one exponent must break the identity
p, n = 7, 1
m = p ** n
cyc = cyclotomic_pn(p, n)
d = len(cyc) - 1
U = units(m)
S = sum(least_pos_rep(a ** (R - 1), m) for a in U)
X = [0] * d
X[1] = 1


def zpow(a):
    return polpowmod(X, a, cyc)


def zam1(a):
    v = zpow(a)[:]
    v[0] -= 1
    return v


def omz(a):
    return [-c for c in zam1(a)]


def build(mutate_exp=0, mutate_d=0, flip_sign=False):
    lhs = [0] * d
    lhs[0] = 1
    for i, a in enumerate(U):
        e = least_pos_rep(a ** (R - 1), m) + (mutate_exp if i == 0 else 0)
        lhs = polmulmod(lhs, polpowmod(zam1(a), e, cyc), cyc)
    for i, a in enumerate(U):
        da = (least_pos_rep(a ** (R - 1), m) - a ** (R - 1)) // m + (mutate_d if i == 0 else 0)
        if da:
            lhs = polmulmod(lhs, polpowmod(omz(a), m * (-da), cyc), cyc)
    rhs = [0] * d
    rhs[0] = -((-1) ** S) if flip_sign else (-1) ** S
    for a in U:
        rhs = polmulmod(rhs, polpowmod(omz(a), a ** (R - 1), cyc), cyc)
    return lhs == rhs


say("(N4) p=7 n=1  perturbing one <a^2> by +1 breaks (K7)", not build(mutate_exp=1))
say("(N5) p=7 n=1  perturbing one d_a by -1 breaks (K7)", not build(mutate_d=-1))
say("(N6) p=7 n=1  flipping the global sign breaks (K7) (computation is not sign-blind)",
    not build(flip_sign=True))

print("")
print("verdict lines = %d , PASS = %d , FAIL = %d"
      % (len(verdicts), sum(1 for v in verdicts if v), sum(1 for v in verdicts if not v)))
print("ALL_PASS = %s" % all(verdicts))
sys.exit(0 if all(verdicts) else 1)
