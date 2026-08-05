"""S3.5 linearisation theorem: marked lifts <-> two affine-linear systems.
Test bed: V = F2^3 = S3-permutation module inflated along S4 -> S4/V4 = S3
(the K^(20) module), P-hat = V x| Ghat5 with ARBITRARY set-theoretic lifts U0,W0."""
from itertools import product
p=2; d=3
# S4 -> S3 (on the 3 pair-partitions 1={12|34},2={13|24},3={14|23}):
# theta=(1,2) |-> (2,3) ; tau=(1,3,4) |-> (1,3,2)
def perm_act(pi, v): return tuple(v[pi[i]] for i in range(d))   # (pi.v)_i = v_{pi(i)}
TH3=(0,2,1)          # swap coords 2,3
TA3=(2,0,1)          # tau acting: verify tau^3 = id below
def comp(a,b): return tuple(a[b[i]] for i in range(d))
assert comp(TH3,TH3)==(0,1,2) and comp(TA3,comp(TA3,TA3))==(0,1,2)
def th(v): return perm_act(TH3,v)
def ta(v): return perm_act(TA3,v)
def add(*vs): return tuple(sum(x)%p for x in zip(*vs))
def neg(v):  return tuple((-x)%p for x in v)
V=[tuple(t) for t in product(range(p),repeat=d)]

# Ghat5 part is irrelevant to the count; model P-hat = V x| <Delta,delta> abstractly:
# elements (v ; g) with g in {formal words}; we only need conjugation action of
# Delta-hat and delta-hat on V, which is th / ta.
# Set-theoretic lifts U0=(u0;Delta), W0=(w0;delta).  Then
#   U = (a ; Delta)  with a ranging over V (a = u0 + shift)
#   U^2 = (a + th(a) ; Delta^2=1)  ... plus the chosen 2-cocycle contribution.
# With split model and lifts U0=(u0;D), W0=(w0;dl):
#   U = (u0 + a ; D),  U^2 = (u0+a + th(u0+a) ; 1) = eps_D + (1+th)a, eps_D=(1+th)u0
#   W = (w0 + b ; dl), W^3 = eps_d + (1+ta+ta^2)b,  eps_d=(1+ta+ta^2)w0
for (u0,w0) in [((0,0,0),(0,0,0)), ((1,0,0),(0,1,1)), ((1,1,0),(1,0,0))]:
    epsD = add(u0, th(u0))
    epsd = add(w0, ta(w0), ta(ta(w0)))
    # LANE A: linear algebra
    solA = [a for a in V if add(a, th(a)) == neg(epsD)]
    solB = [b for b in V if add(b, ta(b), ta(ta(b))) == neg(epsd)]
    laneA = len(solA)*len(solB)
    # LANE B: brute force over |V|^2 pairs (rho(sigma1),rho(sigma2)) with L-1 and L-2.
    # sigma1 = W^{-1}U, sigma2 = U^{-1}W^2 ; enumerate (U,W) = (u0+a;D),(w0+b;dl)
    # and test the two defining relations directly.
    laneB = 0
    for a in V:
        for b in V:
            U=add(u0,a); W=add(w0,b)
            if add(U, th(U)) != (0,)*d: continue          # U^2 = 1   (= L-2, rho(c)=1)
            if add(W, ta(W), ta(ta(W))) != (0,)*d: continue  # W^3 = 1 (delta^3 = c -> 1)
            laneB += 1
    print("u0=%s w0=%s : eps_Delta=%s eps_delta=%s | lane A (linear) = %d , lane B (brute) = %d  %s"
          % (u0,w0,epsD,epsd,laneA,laneB,"MATCH" if laneA==laneB else "*** MISMATCH ***"))
print("\nker N_theta =", len([a for a in V if add(a,th(a))==(0,)*d]),
      " ker N_tau =", len([b for b in V if add(b,ta(b),ta(ta(b)))==(0,)*d]),
      " (split case predicts product =",
      len([a for a in V if add(a,th(a))==(0,)*d])*len([b for b in V if add(b,ta(b),ta(ta(b)))==(0,)*d]), ")")
