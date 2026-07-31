# t=0 (and calibration t>0) check of Theorem T3-N0 by brute force.
# Universe: v of cycle type (l, 1^t) on n = l + t points.
#   F(v) = {(g,h): g^2=1, h^3=1, g^{-1}h = v}, h := g*v  (composition (g*v)(x) = g(v(x)))
#   T_trans^{(k,j)} = #{(g,h) in F(v) : <g,h> transitive, g type 2^k 1^f2, h type 3^j 1^f3}
#   claim: T_trans/|C_{S_n}(v)| = sum_M 1/|Aut M| = Cat(m-1) * m! / (t! f2! f3!),  m = t+f2+f3-1
#          for genus 0 rows, i.e. k + 2j = n + t - 1.
from math import comb, factorial
import sys

def cat(i):
    return comb(2*i, i)//(i+1)

def involutions(n):
    # all g with g^2 = 1 on {0..n-1}, as tuples
    def rec(free, cur):
        if not free:
            yield tuple(cur)
            return
        i = free[0]
        rest = free[1:]
        # i fixed
        cur[i] = i
        yield from rec(rest, cur)
        # i paired with p
        for idx, p in enumerate(rest):
            cur[i] = p
            cur[p] = i
            yield from rec(rest[:idx] + rest[idx+1:], cur)
        cur[i] = i
    return rec(list(range(n)), [0]*n)

def cycle_type(p, n):
    seen = [False]*n
    typ = {}
    for i in range(n):
        if not seen[i]:
            L = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                L += 1
            typ[L] = typ.get(L, 0) + 1
    return typ

def transitive(g, h, n):
    seen = [False]*n
    stack = [0]
    seen[0] = True
    c = 1
    while stack:
        x = stack.pop()
        for p in (g, h):
            y = p[x]
            if not seen[y]:
                seen[y] = True
                c += 1
                stack.append(y)
    return c == n

def run(l, t):
    n = l + t
    # v = (0 1 ... l-1)(l)(l+1)...
    v = list(range(n))
    for i in range(l):
        v[i] = (i+1) % l
    v = tuple(v)
    Cv = l * factorial(t)
    counts = {}
    for g in involutions(n):
        h = tuple(g[v[x]] for x in range(n))
        # h^3 = 1 ?
        ok = True
        for x in range(n):
            if h[h[h[x]]] != x:
                ok = False
                break
        if not ok:
            continue
        if not transitive(g, h, n):
            continue
        tg = cycle_type(g, n)
        th = cycle_type(h, n)
        k = tg.get(2, 0); f2 = tg.get(1, 0)
        j = th.get(3, 0); f3 = th.get(1, 0)
        counts[(k, j)] = counts.get((k, j), 0) + 1
    print(f"=== l={l} t={t} n={n} |C|={Cv}")
    for (k, j) in sorted(counts):
        T = counts[(k, j)]
        f2 = n - 2*k; f3 = n - 3*j
        genus2 = k + 2*j - (n + t - 1)   # = 2*gamma
        m = t + f2 + f3 - 1
        ratio = T / Cv
        if genus2 == 0 and m >= 1:
            pred = cat(m-1) * factorial(m) / (factorial(t)*factorial(f2)*factorial(f3))
            flag = "OK " if abs(pred - ratio) < 1e-9 else "MISMATCH"
        else:
            pred = None
            flag = "    "
        print(f"  (k,j)=({k},{j}) f2={f2} f3={f3} 2g={genus2} m={m} T_trans={T} T/|C|={ratio}"
              + (f"  formula={pred}  [{flag}]" if pred is not None else ""))

if __name__ == "__main__":
    for (l, t) in [(7,0), (9,0), (11,0), (13,0), (9,1), (7,2), (5,3)]:
        run(l, t)
        sys.stdout.flush()
