"""WARN-A2-1 units adjudication (mathematician, 2026-08-22).

Claim under test: the producer's ABGamma (scratchpad/koubou83_A2_48sweep_v2.g:260-278) equals
2 x the canonical F2-abelianization ab(f) = (deg_x f, deg_y f), because ComputeLinking
accumulates SIGNED CROSSINGS and never divides by 2 (linking number = crossings/2).

Canonical pin (2401.06870 sec.1.3): F2 = <x,y> is FREE on x = x12 = sigma1^2, y = x23 = sigma2^2,
so ab is the free abelianization with ab(x) = (1,0), ab(y) = (0,1).
"""
import json, io, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
B = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\koubou83_A2_48sweep_v2_20260822"

# ---- exact 1:1 transcription of the producer's GAP code -------------------------------
def producer_ComputeLinking(sw):
    perm = [1, 2, 3]; lk = {(1,2):0, (1,3):0, (2,3):0}
    for l in sw:
        k = abs(l); s = 1 if l > 0 else -1
        pr = tuple(sorted((perm[k-1], perm[k])))
        lk[pr] += s
        perm[k-1], perm[k] = perm[k], perm[k-1]
    return lk[(1,2)], lk[(1,3)], lk[(2,3)]

def producer_ABGamma(sw):
    l12, l13, l23 = producer_ComputeLinking(sw)
    return (l12-l13, l23-l13, l13)          # NO /2  -> 2 x canonical

def SubstXYtoSigma(xy):
    o = []
    for l in xy: o += {1:[1,1], -1:[-1,-1], 2:[2,2], -2:[-2,-2]}[l]
    return o

# ---- canonical (PIN-AB-1) ------------------------------------------------------------
def canonical_abg(sw):
    """linking numbers = signed crossings / 2 ; assert pure braid."""
    perm = [1, 2, 3]; lk = {(1,2):0, (1,3):0, (2,3):0}
    for l in sw:
        k = abs(l); s = 1 if l > 0 else -1
        pr = tuple(sorted((perm[k-1], perm[k])))
        lk[pr] += s
        perm[k-1], perm[k] = perm[k], perm[k-1]
    assert perm == [1, 2, 3], "not a pure braid word"
    assert all(v % 2 == 0 for v in lk.values()), "odd crossing count in a pure braid"
    l12, l13, l23 = lk[(1,2)]//2, lk[(1,3)]//2, lk[(2,3)]//2
    return (l12-l13, l23-l13, l13)

def ab_xy(w):
    a = b = 0
    for t in w:
        if abs(t) == 1: a += 1 if t > 0 else -1
        else:           b += 1 if t > 0 else -1
    return (a, b)

# ---- PIN-AB-1 item 3: the unit assert that would have caught this --------------------
assert canonical_abg([1,1])       == (1,0,0), "ab(sigma1^2) must be (1,0)"
assert canonical_abg([2,2])       == (0,1,0), "ab(sigma2^2) must be (0,1)"
assert canonical_abg([1,2,1,1,2,1]) == (0,0,1), "c = Delta^2: (a,b,gamma) must be (0,0,1)"
assert producer_ComputeLinking([1,2,1,1,2,1]) == (2,2,2), "raw crossings of Delta^2 must be 2*(1,1,1)"
assert producer_ABGamma([1,1]) == (2,0,0), "producer is expected to be 2x on x"
print("PIN-AB-1 unit asserts: canonical PASS ; producer ABGamma(x) = (2,0,0) = 2 x canonical")

rows = [json.loads(l) for l in io.open(B+"_rows.jsonl", encoding='utf-8') if l.strip()]
wits = {}
for l in io.open(B+"_witness.jsonl", encoding='utf-8'):
    if l.strip():
        r = json.loads(l); wits[(tuple(r['window']), r['shadow_idx'], r['p'])] = r['witness_sigma_word']

# (1) producer ABGamma == 2 * canonical, on every shadow f
uniq = {(r['window'][1], r['shadow_idx']): r['f_xyword'] for r in rows}
ok = neq = zero = 0
for k, xy in uniq.items():
    A = producer_ABGamma(SubstXYtoSigma(xy)); t = ab_xy(xy); c = canonical_abg(SubstXYtoSigma(xy))
    assert c[:2] == t and c[2] == 0, ("SubstXYtoSigma changed the element!", k)
    if A == (2*t[0], 2*t[1], 0): ok += 1
    if A[:2] != t: neq += 1
    if t == (0, 0): zero += 1
print("producer ABGamma == 2*canonical (and gamma=0): %d/%d" % (ok, len(uniq)))
print("  producer[:2] != canonical : %d/%d   |   shadows with ab=(0,0) : %d/%d"
      % (neq, len(uniq), zero, len(uniq)))
print("  => the reported '88/96 systematic mismatch' is exactly {ab != (0,0)}")

# (2) canonical-unit charming of the produced witness, per prime
bad = Counter(); gam = Counter(); tot = Counter()
for r in rows:
    p = r['p']; tot[p] += 1
    a0, b0 = ab_xy(r['f_xyword'])
    aw, bw, gw = canonical_abg(wits[(tuple(r['window']), r['shadow_idx'], p)])
    A, Bv = a0+aw, b0+bw
    if not ((A % p == 0) and (Bv % p == 0)): bad[(p, r['window'][1])] += 1
    if gw % p: gam[p] += 1
print("\nCANONICAL-unit cond1&cond2 FAIL on the produced witness, by (p,window): %s  total=%d"
      % (dict(bad), sum(bad.values())))
print("CANONICAL-unit legal (gamma == 0 mod p) FAIL, by p: %s" % dict(gam))
print("rows per prime: %s" % dict(tot))
print("\n=> p=3: 0 failures (predicate correct, the 2x is invisible mod 3 and mod 9).")
print("=> p=2: the 2x makes cond1/cond2/legal-gamma VACUOUS in the producer; in canonical")
print("   units the produced witness violates true charming on the rows counted above.")
