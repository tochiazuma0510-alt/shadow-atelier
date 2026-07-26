# search/e2-sweep-r2.g -- workorder5 continuation: item1 (synthetic negative smoke test) +
# item3 (sweep (1) r2), per docs/week4-掃引宇宙_v3.md + search/manifest_spec_e2_actions.md +
# docs/week4-掃引宇宙_v3.1補正.md (all three spec-projection files, per coordinator's read list).
#
# Model reuse: Abar's 10-dim basis (w,p,q,r1,r2,r3,t1,t2,t3,t4) is stated (v3 sec.1.3) to be in
# exact bijection with the E19 c=5 monomial basis (S^aT^b, a+b<=3, deg-asc/within-deg a-desc order)
# -- so bar_theta=ThetaP, bar_sigma(.,m)=SigmaP(.,m), bar_E_m=EmP(m) at class 5, copied here
# UNCHANGED from search/e19.g (same functions, this is the SAME object, not a coincidence).
#
# Quadratic-stage derivation (own reasoning, flagged for review -- see report to commander): the
# spec gives beta (full bracket on Abar->C) and sigma|_C/theta|_C explicitly, but NOT a literal
# formula for q_theta/q_N as functions on general Abar elements. Key observation used here: q_theta,
# q_N are ONLY EVER evaluated at f in L = ker(1+bar_theta) cap {bar_N f = -Ebar_m}, i.e. exactly
# where bar_theta(f)+f=0 and f+sigma(f)+sigma^2(f)+Ebar_m=0 (additively, Abar free abelian). This
# means the "Abar-part" of the defining group products s(theta f).s(f) and s(Ebar_m).s(sigma^2 f).
# s(sigma f).s(f) collapses to s(0)=identity EXACTLY on this domain, so BOTH q_theta and q_N reduce
# to iterated section-cocycle terms c_s(.,.) alone (a standard nilpotent-group collection fact),
# and c_s itself is DERIVABLE from the given beta: since the ONLY nonzero brackets among the 10
# generators are [w,p]=t5, [w,q]=t6 (confirmed: beta(p,q)=0 since both have zero w-coordinate,
# matching beta's given formula depending only on w,p,q-coordinates), the "upper-triangular"
# (Hall-order w<p<q<...) section cocycle is c_s(a,b) := a_w*(b_p, b_q) -- i.e. (a_w*b_p, a_w*b_q)
# in the (t5,t6) basis, where a_w=a[1] is the w-coordinate of vector a. This was verified by hand
# (report to commander) to reproduce the known im(Lambda)=<(t5+t6,0)> structural fact.

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;
JoinC := function(strs, sep)
  local r, i;
  if Length(strs) = 0 then return ""; fi;
  r := strs[1];
  for i in [2..Length(strs)] do r := Concatenation(r, sep, strs[i]); od;
  return r;
end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;
WriteFileRaw := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

# ================================================================================
# model (copied UNCHANGED from search/e19.g -- same object, per the bijection stated in
# manifest_spec_e2_actions.md; this is reuse of an already-independently-verified model, not a
# fresh port of a DIFFERENT script)
# ================================================================================
DG := 0;;  BASIS := [];;  IDXTAB := [];;
SetClass := function(c)
  local d, a, b;
  DG := c - 2;
  BASIS := [];
  IDXTAB := List([1..DG+1], x -> List([1..DG+1], y -> 0));
  for d in [0..DG] do
    for a in [d,d-1..0] do
      b := d - a;
      Add(BASIS, [a,b]);
      IDXTAB[a+1][b+1] := Length(BASIS);
    od;
  od;
end;;
NN := function() return Length(BASIS); end;;
IdxOf := function(a,b)
  if a < 0 or b < 0 or a > DG or b > DG then return 0; fi;
  return IDXTAB[a+1][b+1];
end;;
ZeroP := function() return List([1..NN()], x->0); end;;
ConstP := function(c) local v; v := ZeroP(); if c <> 0 then v[IdxOf(0,0)] := c; fi; return v; end;;
Sgen := function() local v; v := ZeroP(); v[IdxOf(1,0)] := 1; return v; end;;
Tgen := function() local v; v := ZeroP(); v[IdxOf(0,1)] := 1; return v; end;;
Padd := function(u,v) return u+v; end;;
Psub := function(u,v) return u-v; end;;
Pscal := function(u,c) return c*u; end;;
Pmul := function(u,v)
  local r, i, j, a1,b1,a2,b2, idx;
  r := ZeroP();
  for i in [1..NN()] do
    if u[i] <> 0 then
      a1 := BASIS[i][1];  b1 := BASIS[i][2];
      for j in [1..NN()] do
        if v[j] <> 0 then
          a2 := BASIS[j][1];  b2 := BASIS[j][2];
          if a1+a2+b1+b2 <= DG then
            idx := IdxOf(a1+a2, b1+b2);
            r[idx] := r[idx] + u[i]*v[j];
          fi;
        fi;
      od;
    fi;
  od;
  return r;
end;;
Ppow := function(u, k)
  local r, b, n;
  r := ConstP(1);  b := ShallowCopy(u);  n := k;
  while n > 0 do
    if n mod 2 = 1 then r := Pmul(r,b); fi;
    b := Pmul(b,b);
    n := QuoInt(n,2);
  od;
  return r;
end;;
PinvUnit := function(u)
  local x, r, t, i;
  x := Psub(u, ConstP(1));
  r := ConstP(1);  t := ConstP(1);
  for i in [1..DG] do
    t := Pmul(t, x);
    if i mod 2 = 1 then r := Psub(r,t); else r := Padd(r,t); fi;
  od;
  return r;
end;;
Sunit := function() return Padd(ConstP(1), Sgen()); end;;
Tunit := function() return Padd(ConstP(1), Tgen()); end;;
Psubst := function(f, U, V)
  local r, Up, Vp, i, a, b;
  r := ZeroP();
  Up := [ConstP(1)];  Vp := [ConstP(1)];
  for i in [1..DG] do
    Add(Up, Pmul(Up[i], U));
    Add(Vp, Pmul(Vp[i], V));
  od;
  for i in [1..NN()] do
    if f[i] <> 0 then
      a := BASIS[i][1];  b := BASIS[i][2];
      if a+b <= DG then
        r := Padd(r, Pscal(Pmul(Up[a+1], Vp[b+1]), f[i]));
      fi;
    fi;
  od;
  return r;
end;;
ThetaP := function(f) return Pscal(Psubst(f, Tgen(), Sgen()), -1); end;;
TauP := function(f)
  local invs, invt, rho;
  invs := PinvUnit(Sunit());
  invt := PinvUnit(Tunit());
  rho := Psub(Pmul(invs,invt), ConstP(1));
  return Pmul(Psubst(f, Tgen(), rho), invs);
end;;
SigmaP := function(f, m) return Pmul(Ppow(Tunit(), m), TauP(f)); end;;
EmP := function(m)
  local s,t,st,AA,c,k,invsm;
  if m = 0 then return ZeroP(); fi;
  s := Sunit();  t := Tunit();  st := Pmul(s,t);
  AA := function(u,n) local r,p,i; r:=ZeroP(); p:=ConstP(1);
    for i in [0..n-1] do r := Padd(r,p); p := Pmul(p,u); od; return r; end;
  c := ZeroP();
  for k in [2..m] do c := Padd(Pmul(t, AA(st,k-1)), Pmul(t,c)); od;
  invsm := Ppow(PinvUnit(s), m);
  return Psub(c, Pmul(invsm, Pmul(AA(s,m), AA(st,m))));
end;;
MatOf := function(op)
  local n, m, i, e;
  n := NN();  m := [];
  for i in [1..n] do
    e := ZeroP();  e[i] := 1;
    Add(m, op(e));
  od;
  return m;
end;;

SetClass(5);;  # Abar model: class 5, dim 10, matches w,p,q,r1,r2,r3,t1,t2,t3,t4

# ================================================================================
# C-level structure (new data, manifest_spec_e2_actions.md)
# ================================================================================
ThetaC := function(v) return [v[2], v[1]]; end;;               # [[0,1],[1,0]]
SigmaC := function(v) return [-v[2], v[1]-v[2]]; end;;         # [[0,-1],[1,-1]]
NC := function(v) return v + SigmaC(v) + SigmaC(SigmaC(v)); end;;

ncOk := (NC([1,0]) = [0,0] and NC([0,1]) = [0,0]);;
Print("[", PF(ncOk), "] N_C = 0 on both basis vectors (S-3 stop condition, structural fact from v3 sec.1.4/sys E22.6)\n");
if not ncOk then
  Print("[STOP-S3] N_C != 0 -- halting (math or model error). Remaining computation SKIPPED.\n");
fi;

if ncOk then

# beta: Abar x Abar -> C, using ONLY w,p,q coordinates (BASIS positions 1,2,3)
BetaAC := function(u, v)
  return [ u[1]*v[2] - u[2]*v[1], u[1]*v[3] - u[3]*v[1] ];
end;;
Print("[", PF(BetaAC(Sgen(), Tgen()) = [0,0]) , "] beta(p,q) = 0 (sanity: only w-paired brackets nonzero)\n");

# ================================================================================
# COMPLETED 2026-07-26 per coordinator's normative source docs/week4-E2作用表_v1.md (SS2, SS2.1,
# SS3, SS4, SS5, SS6, SS7) -- read in full (lines 1-512). This closes the P-2 gap flagged on
# 2026-07-26: d_theta, d_sigma, d_sigma^2, epsilon_m now have closed forms in that document
# (SS6.3/6.4/6.5, SS5.2), giving full (not partial) q_theta (6.6) and q_N (6.7).
#
# These closed forms were independently CROSS-CHECKED by this implementer via a genuine
# GAP PcpGroup (search/week4-e2-routeG.g, route G: FromTheLeftCollector construction of
# A=gamma2/gamma6 as an actual group, theta/sigma_m/E_m built from generator images, q_theta/q_N
# computed via REAL group products theta(s(f))*s(f) and E_m*sigma^2(s(f))*sigma(s(f))*s(f), then
# Exponents() read off and compared to the closed forms below) -- all matched exactly (10 test
# vectors x q_theta, 6 values of m x 10 vectors x q_N, theta^2=id, E_m table m=0..6,
# theta/sigma_m preserve [w,p]=t5,[w,q]=t6). That script is a SEPARATE, independent file; this
# script re-derives the same closed forms directly from the spec document (not by reading
# week4-e2-routeG.g), per coordinator instruction "GAP -> Node の写経は二系統を一系統に潰す" --
# the same discipline applies here: e2-sweep-r2.g's formulas below are transcribed from
# docs/week4-E2作用表_v1.md directly, and week4-e2-routeG.g's group-product route is the
# structurally-independent second check on those same formulas (already done, see above).
#
# c_s (section cocycle, eq 2.5): with basis order (w,p,q,r1,r2,r3,t1,t2,t3,t4 | t5,t6),
#   c_s(a,b) = (-a_p*b_w, -a_q*b_w)
# ================================================================================
Cs := function(a, b) return [ -a[2]*b[1], -a[3]*b[1] ]; end;;

# Lambda: C -> C x C, Lambda(z) = ((1+theta)z, N_C(z)) = ((1+theta)z, 0) since N_C=0
Lambda1 := function(z) return z + ThetaC(z); end;;  # (1+theta)z
Print("im(Lambda) generator check: Lambda((1,0)) = ", JoinC([String(Lambda1([1,0])),String(NC([1,0]))],","), "\n");
Print("  Lambda((0,1)) = (1+theta)(0,1) = ", String(Lambda1([0,1])), "\n");
Print("[", PF(Lambda1([1,0]) = [1,1] and Lambda1([0,1]) = [1,1]), "] im(Lambda) generated by (1,1) in the (1+theta) coordinate (matches <(t5+t6,0)> structural prediction)\n");

# ================================================================================
# GenBinom(m,k) := m(m-1)...(m-k+1)/k!  -- generalized binomial, valid for ANY integer m
# (per doc SS7 implementation note 1: m must be a literal integer evaluated BEFORE any reduction).
# ================================================================================
GenBinom := function(m,k)
  local num, i;
  if k < 0 then return 0; fi;
  if k = 0 then return 1; fi;
  num := 1;
  for i in [0..k-1] do num := num * (m-i); od;
  return num / Factorial(k);
end;;

# d_theta (eq 6.3): linear, m-independent.
#   f = [fw,fp,fq,fr1,fr2,fr3,ft1,ft2,ft3,ft4]  (indices 1..10)
DTheta := function(f)
  local fp,fq,fr2,ft2,ft3;
  fp:=f[2]; fq:=f[3]; fr2:=f[5]; ft2:=f[8]; ft3:=f[9];
  return [ -(fq+fr2+ft3), -(fp+fr2+ft2) ];
end;;

# d_sigma (eq 6.4): linear + one C(a_w,2) term.
DSigma := function(f, m)
  local fw,fq,fr2,fr3,ft2,ft3,ft4,b2;
  fw:=f[1]; fq:=f[3]; fr2:=f[5]; fr3:=f[6]; ft2:=f[8]; ft3:=f[9]; ft4:=f[10];
  b2 := GenBinom(fw,2);
  return [ -fq + fr2 - 3*fr3 + ft3 - 2*ft4 + b2, -fr3 - ft2 + ft3 - ft4 - m*b2 ];
end;;

# sigma|_C matrix (0,-1;1,-1), same as SigmaC above but named for eq 6.5's own notation
SigmaOnC := function(z) return [ -z[2], z[1]-z[2] ]; end;;

# d_{sigma^2} (eq 6.5): d_sigma(sigma_bar f) + sigma|_C(d_sigma(f))
DSigma2 := function(f, m)
  local sf;
  sf := SigmaP(f, m);
  return DSigma(sf, m) + SigmaOnC(DSigma(f, m));
end;;

# epsilon_m (eq 5.2, C-part of E_m)
EpsilonM := function(m)
  return [ GenBinom(m,1)+7*GenBinom(m,2)+17*GenBinom(m,3)+17*GenBinom(m,4)+6*GenBinom(m,5),
          -(GenBinom(m,2)+4*GenBinom(m,3)+6*GenBinom(m,4)+3*GenBinom(m,5)) ];
end;;

# q_theta (eq 6.6), FULL (d_theta + c_s(theta_bar f, f)):
#   q_theta(f) = (fw*fq - fq - fr2 - ft3) t5 + (fw*fp - fp - fr2 - ft2) t6
QTheta := function(f)
  local fw,fp,fq,fr2,ft2,ft3;
  fw:=f[1]; fp:=f[2]; fq:=f[3]; fr2:=f[5]; ft2:=f[8]; ft3:=f[9];
  return [ fw*fq - fq - fr2 - ft3, fw*fp - fp - fr2 - ft2 ];
end;;

# q_N (eq 6.7), FULL, valid for ANY f (not just f in L):
#   q_N(f) = eps_m + d_{sigma^2}(f) + d_sigma(f)
#            + c_s(e,S^2 f) + c_s(e+S^2 f, S f) + c_s(e+S^2 f+S f, f)
QN := function(f, m)
  local ebar, Sf, S2f, eps, dS2, dS, c1, c2, c3;
  ebar := EmP(m);
  Sf := SigmaP(f, m);
  S2f := SigmaP(Sf, m);
  eps := EpsilonM(m);
  dS2 := DSigma2(f, m);
  dS := DSigma(f, m);
  c1 := Cs(ebar, S2f);
  c2 := Cs(ebar+S2f, Sf);
  c3 := Cs(ebar+S2f+Sf, f);
  return eps + dS2 + dS + c1 + c2 + c3;
end;;

# ---- self-checks against docs/week4-E2作用表_v1.md's own numeric anchors ----
Print("\n=== QTheta/QN self-checks (formulas transcribed from docs/week4-E2作用表_v1.md) ===\n");
# NOTE: in this model, w = ConstP(1) (degree-0 basis vector, IdxOf(0,0)), NOT Sgen()/Tgen().
# Sgen()=p (S, IdxOf(1,0)), Tgen()=q (T, IdxOf(0,1)). Mislabeling this caused a self-check
# false-FAIL on first pass here (fixed): the earlier draft wrote Cs(Sgen(),Tgen()) claiming it
# was c_s(w,p), which is actually c_s(p,q) (still incidentally [0,0], but the WRONG check).
Wgen := ConstP(1);;
Print("[", PF(Cs(Wgen,Sgen())=[0,0]), "] c_s(w,p)=0 (S3 self-check)\n");
Print("[", PF(Cs(Sgen(),Wgen)=[-1,0]), "] c_s(p,w)=-t5 (S4 self-check)\n");
emTableCheck := [
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [-1,1,0,-1,0,0,1,0,0,0,1,0],
  [-3,4,-1,-5,1,0,6,-1,0,0,9,-1],
  [-6,10,-4,-15,5,-1,21,-6,1,0,41,-7]
];;
emCheckOk := true;;
for mm in [0..3] do
  gotAbar := EmP(mm);
  gotC := [ EpsilonM(mm)[1], EpsilonM(mm)[2] ];
  wantAbar := emTableCheck[mm+1]{[1..10]};
  wantC := emTableCheck[mm+1]{[11,12]};
  if gotAbar <> wantAbar or gotC <> wantC then
    emCheckOk := false;
    Print("  E_m mismatch at m=", mm, ": got Abar=", gotAbar, " C=", gotC, " want Abar=", wantAbar, " C=", wantC, "\n");
  fi;
od;
Print("[", PF(emCheckOk), "] E_m (Abar via EmP + C via EpsilonM) matches SS5.3 table for m=0..3\n");

# ---- GAP<->Node cross-check dump: print QTheta/QN on shared test vectors, to be diffed by
#      eye against crosscheck/check-e2-action.mjs's independent Node computation of the same
#      formulas (this is route-N-style GAP vs independent Node, an interim two-system check
#      pending the sol2-derivation agreement signal before any live sweep judgement) ----
Print("\n=== QTheta/QN dump for GAP<->Node comparison ===\n");
crossTestVecs := [
  [1,0,0,0,0,0,0,0,0,0],
  [0,1,0,0,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0,0,0],
  [2,1,-1,0,3,0,-2,1,0,0],
  [-4,2,3,-1,0,1,0,-2,1,1],
  [1,1,1,1,1,1,1,1,1,1],
  [0,-3,2,4,-1,0,1,0,-2,3]
];;
for cf in crossTestVecs do
  Print("  QTheta(", cf, ") = ", QTheta(cf), "\n");
od;
for cf in crossTestVecs do
  for cm in [0,1,2,3,5,7] do
    Print("  QN(", cf, ", m=", cm, ") = ", QN(cf,cm), "\n");
  od;
od;

# ================================================================================
# v3.1 F5/F12.3 postcondition: for basis-generator representation of K, check
#   n_i * piB(e_i,e_j) = 0 = n_j * piB(e_i,e_j)   and   piB(e_i,e_j) = piB(e_j,e_i)
# piB(u,v) := (b_theta(u,v), b_N(u,v)) with b_theta(u,v):=beta(theta(v),u),
#             b_N(u,v):=beta(sigma^2(v), sigma(u)+u) + beta(sigma(v), u)   [manifest_spec_e2_actions.md]
# (computed directly via beta + known theta_bar/sigma_bar -- no group collection needed for piB
# itself, only for Xi/q_theta/q_N as derived above.)
# ================================================================================
BTheta := function(u, v) return BetaAC(ThetaP(v), u); end;;
BN := function(u, v, m)
  local sv2, su, term1, term2;
  sv2 := SigmaP(SigmaP(v,m),m);
  su := SigmaP(u,m);
  term1 := BetaAC(sv2, su+u);
  term2 := BetaAC(SigmaP(v,m), u);
  return term1+term2;
end;;
PiB := function(u,v,m) return Concatenation(BTheta(u,v), BN(u,v,m)); end;;

# ================================================================================
# per-(j,m) three-stage evaluation. Runs on the linear-stage system ALREADY computed and
# verified in workorder5 item2 (search/e19.g at class 5): L != empty for ALL m=0..63 (Z2-solvable
# for every j simultaneously). This function recomputes the linear stage independently here too
# (does not just assume the e19 result) since this is a DIFFERENT script/object nominally, then
# adds the quadratic/obstruction stage.
# ================================================================================
IntBool := function(b) if b then return 1; else return 0; fi; end;;

BuildLinearSystem := function(m)
  local n, thMat, smMat, sm2Mat, b, rows, rhs, i, k, j, val;
  n := NN();
  thMat := MatOf(ThetaP);;
  smMat := MatOf(x -> SigmaP(x,m));;
  sm2Mat := [];
  for k in [1..n] do
    val := ZeroP();
    for j in [1..n] do
      if smMat[k][j] <> 0 then val := val + smMat[k][j]*smMat[j]; fi;
    od;
    Add(sm2Mat, val);
  od;
  b := EmP(m);;
  rows := [];;  rhs := [];;
  for i in [1..n] do
    rows[i] := List([1..n], k -> thMat[k][i] + IntBool(i=k));
    rhs[i] := 0;
  od;
  for i in [1..n] do
    rows[n+i] := List([1..n], k -> IntBool(i=k) + smMat[k][i] + sm2Mat[k][i]);
    rhs[n+i] := -b[i];
  od;
  return rec(n:=n, rows:=rows, rhs:=rhs, b:=b);
end;;

Print("\ntotal setup elapsed ms: ", Runtime()-startTime, "\n");

# ================================================================================
# ITEM 1: synthetic negative-example smoke test (launch condition, priority per coordinator)
# Perturb b for a KNOWN-solvable (c=5 i.e. Abar model, m=5) system: b -> b + e_1 (one unit
# outside the image). Confirm GAP's canonical SNF now reports UNSOLVABLE and that a genuine dual
# witness y (yM=0 mod 2^j, yb!=0 mod 2^j) is recoverable -- i.e. the negative certificate code path
# actually fires, per docs/notes/falsifier_掃引v3ゲート.md's finding that this never happened with
# real (c,m) data in the E19 sweep. This is SYNTHETIC data (synthetic=true), not a sweep result.
# ================================================================================
Print("\n=== ITEM 1: synthetic negative-example smoke test ===\n");
smokeM := 5;;
sys := BuildLinearSystem(smokeM);;
Mmat := sys.rows;;
origRhs := sys.rhs;;
# perturb: add 1 to the first component of b (i.e. to rhs[1], the first (1+theta) row's target --
# still 0 there originally, so add 1 there to push b outside the image in a component that is very
# likely to be unreachable, per the item's instruction "b を像の外へ")
perturbedRhs := ShallowCopy(origRhs);;
perturbedRhs[1] := perturbedRhs[1] + 1;;

snfSmoke := SmithNormalFormIntegerMatTransforms(Mmat);;
Usmoke := snfSmoke.rowtrans;;  Dsmoke := snfSmoke.normal;;  rankSmoke := snfSmoke.rank;;
cvecOrig := Usmoke * origRhs;;
cvecPerturbed := Usmoke * perturbedRhs;;

v2val := function(n) local v; if n=0 then return 1000000; fi; v:=0; n:=AbsInt(n); while n mod 2=0 do n:=n/2; v:=v+1; od; return v; end;;

origSolvableAllJ := true;;
for ii in [1..rankSmoke] do
  if v2val(cvecOrig[ii]) < v2val(Dsmoke[ii][ii]) then origSolvableAllJ := false; fi;
od;
for ii in [rankSmoke+1..Length(cvecOrig)] do if cvecOrig[ii] <> 0 then origSolvableAllJ := false; fi; od;

perturbedSolvableAllJ := true;;
for ii in [1..rankSmoke] do
  if v2val(cvecPerturbed[ii]) < v2val(Dsmoke[ii][ii]) then perturbedSolvableAllJ := false; fi;
od;
for ii in [rankSmoke+1..Length(cvecPerturbed)] do if cvecPerturbed[ii] <> 0 then perturbedSolvableAllJ := false; fi; od;

Print("[", PF(origSolvableAllJ), "] original system (c=5 model, m=", smokeM, "): Z2-solvable (positive baseline)\n");
Print("[", PF(not perturbedSolvableAllJ), "] perturbed system (b+e_1): Z2-solvable = ", perturbedSolvableAllJ, " (expect FALSE -- launch condition)\n");

if origSolvableAllJ and not perturbedSolvableAllJ then
  # find the smallest j at which it fails, and extract the dual witness y = U-row for that
  # failing coordinate (yM = (row of U*M) = (row of D) which is 0 off-diagonal.. construct y
  # directly as the appropriate row of U restricted to where the 2-adic mismatch occurs)
  failJ := 0;;  failRow := 0;;
  for ii in [1..rankSmoke] do
    if v2val(cvecPerturbed[ii]) < v2val(Dsmoke[ii][ii]) then
      failJ := v2val(Dsmoke[ii][ii]) ;  failRow := ii; break;
    fi;
  od;
  if failRow = 0 then
    for ii in [rankSmoke+1..Length(cvecPerturbed)] do
      if cvecPerturbed[ii] <> 0 then failRow := ii; failJ := 1; break; fi;
    od;
  fi;
  yWitness := Usmoke[failRow];;
  yM := yWitness * Mmat;;
  yB := yWitness * perturbedRhs;;
  Print("  dual witness y = row ", failRow, " of U. yM (should be all-zero) = ", yM, "\n");
  Print("  y.b = ", yB, " (should be nonzero mod 2^", failJ, ")\n");
  yMZero := ForAll(yM, z -> z = 0);;
  yBNonzero := (yB mod (2^failJ) <> 0);;
  Print("[", PF(yMZero), "] dual witness satisfies yM = 0 exactly\n");
  Print("[", PF(yBNonzero), "] dual witness satisfies yb != 0 mod 2^", failJ, "\n");

  smokeCert := Concatenation(
    "{\"claim\":\"linear_stage_empty\",",
    "\"synthetic\":true,",
    "\"method\":\"left_kernel_mod_prime_power/v1\",",
    "\"modulus\":", String(2^failJ), ",",
    "\"matrix_shape\":[", String(2*sys.n), ",", String(sys.n), "],",
    "\"perturbation\":\"b[1] += 1 (item1 synthetic smoke test, NOT real sweep data)\",",
    "\"dual_witness_y\":\"", String(yWitness), "\",",
    "\"yM_is_zero\":", JB(yMZero), ",",
    "\"yb\":", String(yB), ",",
    "\"yb_nonzero_mod_2j\":", JB(yBNonzero), ",",
    "\"recheck\":\"yM and yb recomputed directly above, independent of the SNF's own internal claims\"}");;
  WriteFileRaw("certificates/e2sweep/smoke_negative_c5_m5.json", smokeCert);;
  Print("wrote certificates/e2sweep/smoke_negative_c5_m5.json\n");
  Print("\n[LAUNCH CONDITION]: ", PF(yMZero and yBNonzero), " -- negative certificate code path fires correctly.\n");
else
  Print("\n[LAUNCH CONDITION FAILED]: could not construct the expected pos/neg contrast -- DO NOT PROCEED to item 3.\n");
fi;

fi; # ncOk
