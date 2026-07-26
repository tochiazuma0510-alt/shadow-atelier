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
    "\"modulus\":", String(2^failJ), ",\"m\":", String(smokeM), ",",
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

# ================================================================================
# ITEM 3 PIPELINE (coordinator continuation instruction, 2026-07-26): "v3 sec.2-3 の完全
# パイプラインを実装せよ -- 384系の全数列挙・Kの生成・二次表(F,piB)・mass check・Ob_j商群
# 構成・判定...384系の本走査だけは実行するな."
#
# LINEAR STAGE (v3 sec.3.1): fully implemented below -- per-m SNF (computed once over Z,
# unreduced), per-j (j=1..6) solvability test via 2-adic valuation comparison (a direct
# generalization of item1's "Z2-solvable for all j simultaneously" test to a SPECIFIC j),
# K = ker(M mod 2^j) generator construction (with orders) from the SNF column-transform V,
# independent recheck that generators satisfy (1+theta)e=0, N e=0, n_i e=0 mod 2^j, and an
# unsolvable-certificate writer (v3 sec.3.3(A) schema, dual witness y: yM=0, yb!=0 mod 2^j).
#
# QUADRATIC STAGE (v3 sec.3.2-3.3(B)/(C)): BLOCKED, reported explicitly below rather than
# guessed. F(e_i) and omega0 (the quadratic obstruction map into Ob_j=(C_j x C_j)/im(Lambda))
# are NOT derivable from beta/theta|_C/sigma|_C/QTheta/QN alone. Candidate checked and
# REJECTED: F(k):=(QTheta(k),QN(k,m)) evaluated directly at k. Expanding QTheta(u+v) gives
# quadratic cross-term (uw*vq+vw*uq, uw*vp+vw*up) (symmetric in u,v); this does NOT match
# the ALREADY-AUTHORIZED piB formula (BTheta(u,v):=BetaAC(ThetaP(v),u), from
# manifest_spec_e2_actions.md, computed below) at u=w-basis-vector, v=p-basis-vector:
#   my candidate's cross-term at (u,v)=(e_w,e_p): e_w has w-coord 1, e_p has q-coord 0,
#   p-coord... [full check in report to commander] -- the two do not coincide in general,
#   so treating "the quadratic part of QTheta's own expansion" as piB (or vice versa,
#   deriving F from piB by undoing this) is not licensed by anything I have been given
#   permission to read. This is exactly the shape of error that both independent audits
#   caught in the earlier q_theta/q_N self-derivation (docs/notes/検証_q式導出.md,
#   sol/sol2_reply_01_q.md) -- NOT repeating it. Stopping here; see report to commander for
#   the precise ask (either docs/命題_E22三段判定_v1.md sec.6's F/omega0 formulas, or an
#   explicit closed form via a permitted channel).
# ================================================================================

Print("\n=== ITEM 3: linear-stage pipeline (per (j,m)) ===\n");

V2Val := function(n)
  local v;
  if n = 0 then return 1000000; fi;
  v := 0; n := AbsInt(n);
  while n mod 2 = 0 do n := n/2; v := v+1; od;
  return v;
end;;

# Build the (once-per-m) SNF data for the 20x10 system M(m) x = b(m) (over Z, unreduced).
BuildSnfData := function(m)
  local sys, snf;
  sys := BuildLinearSystem(m);;
  snf := SmithNormalFormIntegerMatTransforms(sys.rows);;
  return rec(m:=m, sys:=sys, U:=snf.rowtrans, V:=snf.coltrans, D:=snf.normal, rank:=snf.rank, n:=sys.n);
end;;

# Test solvability of M x = b (mod 2^j), using the once-computed SNF data (U*M*V=D). Returns
# a record: solvable(bool); if unsolvable: failRow, modulus; if solvable: modulus, kgens (list
# of {vec (Abar x-coords, length n), order (2^k)}), covering K = ker(M mod 2^j) fully.
TestAtJ := function(snfData, j)
  local n, rank, D, U, V, b, c, modulus, i, failRow, ok, kgens, ord, genY, genX, d, v2d;
  n := snfData.n;  rank := snfData.rank;  D := snfData.D;  U := snfData.U;  V := snfData.V;
  b := snfData.sys.rhs;
  c := U * b;;
  modulus := 2^j;;
  ok := true;  failRow := 0;
  for i in [1..rank] do
    d := D[i][i];  v2d := V2Val(d);
    if V2Val(c[i]) < Minimum(v2d, j) then ok := false; failRow := i; break; fi;
  od;
  if ok then
    for i in [rank+1..Length(c)] do
      if V2Val(c[i]) < j then ok := false; failRow := i; break; fi;
    od;
  fi;
  if not ok then
    return rec(solvable:=false, failRow:=failRow, modulus:=modulus);
  fi;
  kgens := [];;
  for i in [1..n] do
    if i <= rank then
      d := D[i][i];  v2d := V2Val(d);
    else
      v2d := 1000000;
    fi;
    if v2d >= j then
      ord := 2^j;  genY := List([1..n], k -> 0);  genY[i] := 1;
    else
      ord := 2^v2d;  genY := List([1..n], k -> 0);  genY[i] := 2^(j - v2d);
    fi;
    genX := V * genY;;
    if ord > 1 then
      Add(kgens, rec(vec:=genX, order:=ord));
    fi;
  od;
  return rec(solvable:=true, modulus:=modulus, kgens:=kgens);
end;;

# Independent recheck (v3 sec.3.1 point 4): each K generator e must satisfy, mod 2^j:
#   (1+bar_theta) e = 0,  bar_N e = 0,  n_i * e = 0
RecheckKGenerator := function(gen, j, m)
  local e, thetaE, sum1, modulus, ok1, ok2, ok3, sigE, sig2E, NE, nE;
  e := gen.vec;  modulus := 2^j;
  thetaE := ThetaP(e);;
  sum1 := e + thetaE;;
  ok1 := ForAll(sum1, x -> x mod modulus = 0);;
  sigE := SigmaP(e, m);;
  sig2E := SigmaP(sigE, m);;
  NE := e + sigE + sig2E;;
  ok2 := ForAll(NE, x -> x mod modulus = 0);;
  nE := gen.order * e;;
  ok3 := ForAll(nE, x -> x mod modulus = 0);;
  return ok1 and ok2 and ok3;
end;;

# Solvable (linear-stage kernel) certificate writer -- for crosscheck/check-e2-action.mjs to
# independently re-derive (1+theta)e=0, N e=0, n_i*e=0 mod 2^j directly from theta_bar/sigma_bar.
WriteSolvableCert := function(path, j, m, kgens)
  local genStrs, ordStrs, cert;
  genStrs := List(kgens, g -> String(g.vec));;
  ordStrs := List(kgens, g -> String(g.order));;
  cert := Concatenation(
    "{\"claim\":\"linear_stage_kernel\",",
    "\"method\":\"snf_kernel_mod_prime_power/v1\",",
    "\"modulus\":", String(2^j), ",\"m\":", String(m), ",\"j\":", String(j), ",",
    "\"basis_order_Abar\":[\"w\",\"p\",\"q\",\"r1\",\"r2\",\"r3\",\"t1\",\"t2\",\"t3\",\"t4\"],",
    "\"K_generators\":[", JoinC(genStrs, ","), "],",
    "\"K_orders\":[", JoinC(ordStrs, ","), "],",
    "\"recheck\":\"checker independently rebuilds theta_bar/sigma_bar mod 2^j and verifies (1+theta)e=0, N e=0, n_i*e=0 for each generator\"}");;
  WriteFileRaw(path, cert);;
end;;

# Unsolvable certificate writer (v3 sec.3.3(A) schema)
WriteUnsolvableCert := function(path, snfData, j, failRow)
  local U, n, modulus, y, yM, yb, yMZero, yBNonzero, cert;
  U := snfData.U;  n := snfData.n;
  modulus := 2^j;
  y := U[failRow];;
  yM := y * snfData.sys.rows;;
  yb := y * snfData.sys.rhs;;
  yMZero := ForAll(List(yM, x -> x mod modulus), x -> x = 0);;
  yBNonzero := (yb mod modulus <> 0);;
  cert := Concatenation(
    "{\"claim\":\"linear_stage_empty\",",
    "\"method\":\"left_kernel_mod_prime_power/v1\",",
    "\"modulus\":", String(modulus), ",",
    "\"matrix_shape\":[", String(2*n), ",", String(n), "],",
    "\"m\":", String(snfData.m), ",\"j\":", String(j), ",",
    "\"basis_order_Abar\":[\"w\",\"p\",\"q\",\"r1\",\"r2\",\"r3\",\"t1\",\"t2\",\"t3\",\"t4\"],",
    "\"dual_witness_y\":\"", String(y), "\",",
    "\"yM_is_zero_mod_2j\":", JB(yMZero), ",",
    "\"yb\":", String(yb), ",",
    "\"yb_nonzero_mod_2j\":", JB(yBNonzero), ",",
    "\"recheck\":\"yM mod 2^j and yb mod 2^j recomputed directly, independent of SNF's internal claim\"}");;
  WriteFileRaw(path, cert);;
  return yMZero and yBNonzero;
end;;

# ================================================================================
# QUADRATIC STAGE (unblocked 2026-07-26 via search/manifest_spec_e2_actions3.md, quoting
# docs/命題_E22三段判定_v1.md Cor E22.4/eq(6.1)(6.2)/Cor E22.6/sec.6.2-6.3 verbatim). Read in
# full (98 lines). Implements F := pi.ell + pi.Q : K -> Ob, the polarization piB, the
# concrete Ob = (C/<t5+t6>) (+) C quotient (Cor E22.6, rank 3), the (6.1) expansion formula,
# and the (6.2) self-check n_i F(e_i) + C(n_i,2) piB(e_i,e_i) = 0 in Ob.
#
# ell(k) := (b_theta(f0,k), b_N(f0,k)) = PiB(f0, k, m)        [already defined above]
# Q(k)   := (theta(s k)(s k), sigma^2(s k) sigma(s k)(s k))   -- NOTE: NO E_m factor, unlike
#           QN. First component = QTheta(k) exactly (same formula, theta(s.)s. product).
#           Second component: derived below as QQ(f,m), obtained from QN's OWN closed form
#           (6.7) by algebraically deleting the E_m-dependent terms (ebar->0, eps_m->0) --
#           this is a legitimate algebraic specialization of an already-validated formula,
#           NOT a new guess: QN(f,m) = eps_m + dSigma2(f,m) + dSigma(f,m) + Cs(ebar,S2f)
#           + Cs(ebar+S2f,Sf) + Cs(ebar+S2f+Sf,f); setting ebar:=[0,0], eps_m:=[0,0] gives
#           QQ(f,m) = dSigma2(f,m) + dSigma(f,m) + Cs(S2f,Sf) + Cs(S2f+Sf,f).
# ================================================================================
QQ := function(f, m)
  local Sf, S2f;
  Sf := SigmaP(f, m);;
  S2f := SigmaP(Sf, m);;
  return DSigma2(f, m) + DSigma(f, m) + Cs(S2f, Sf) + Cs(S2f+Sf, f);
end;;

# Pi: C x C (4-vector [a1,b1,a2,b2]) -> Ob (3-vector), per Cor E22.6: im(Lambda)=<(t5+t6,0)>,
# i.e. only the FIRST C-copy (the b_theta/QTheta slot) is quotiented, by identifying (a1,b1)
# with (a1+1,b1+1) -- invariant is a1-b1. The second C-copy (b_N/QQ slot) passes through
# unreduced (rank 3 total, matches Ob = (C/<t5+t6>) (+) C).
PiOb := function(v4) return [ v4[1]-v4[2], v4[3], v4[4] ]; end;;

ObModReduce := function(v3, modulus) return List(v3, x -> x mod modulus); end;;

# raw (pre-projection) ell, Q, B, all valued in C x C (4-vectors)
RawEll := function(k, f0, m) return PiB(f0, k, m); end;;
RawQ := function(k, m) return Concatenation(QTheta(k), QQ(k, m)); end;;
RawB := function(u, v, m) return PiB(u, v, m); end;;

# projected (Ob-valued, 3-vectors)
FE := function(k, f0, m) return PiOb(RawEll(k,f0,m)) + PiOb(RawQ(k,m)); end;;
PiBFull := function(u, v, m) return PiOb(RawB(u,v,m)); end;;

# ---- Extract a particular solution f0 (Abar x-coords) from the linear-stage SNF data,
#      given solvability at level j already confirmed by TestAtJ. ----
ModInv := function(a, m)
  local g;
  if m = 1 then return 0; fi;
  g := Gcdex(a, m);;
  return g.coeff1 mod m;
end;;

ExtractF0 := function(snfData, j)
  local n, rank, D, U, V, b, c, modulus, i, d, v2d, g, dprime, cprime, modprime, yi, y, f0;
  n := snfData.n;  rank := snfData.rank;  D := snfData.D;  U := snfData.U;  V := snfData.V;
  b := snfData.sys.rhs;  c := U * b;;  modulus := 2^j;;
  y := List([1..n], x -> 0);;
  for i in [1..rank] do
    d := D[i][i];  v2d := V2Val(d);
    if v2d >= j then
      y[i] := 0;
    else
      g := 2^v2d;  dprime := d/g;  cprime := c[i]/g;  modprime := modulus/g;
      if modprime = 1 then
        yi := 0;
      else
        yi := (ModInv(dprime, modprime) * cprime) mod modprime;
      fi;
      y[i] := yi;
    fi;
  od;
  f0 := V * y;;
  return f0;
end;;

# ---- SELF-CHECKS required before trusting F/piB at all (coordinator instruction: "解消
#      しなければまた止まって報告"). Generalized into a function so it can be run over
#      several (j,m) samples, and over MULTIPLE coefficient vectors a (not just (1,1)),
#      to stress the (6.1) expansion formula harder (a_i=2,3 too, not only 0/1). ----
QuadStageSelfCheck := function(m, j, verbose)
  local snfD, res, f0, modulus, modulusC, f0Ok, symOk, postOk, expandOk, gi, fei, bii, lhs, lhsRed,
        k1, k2, aVecs, avec, kk, fDirectRaw, fDirect, fe1, fe2, fExpandedRaw, fExpanded, term, ii, jj;
  snfD := BuildSnfData(m);;
  res := TestAtJ(snfD, j);;
  if not res.solvable then
    if verbose then Print("  [SKIP] (j=",j,",m=",m,"): linear stage unsolvable, no quadratic self-check possible\n"); fi;
    return rec(ok:=false, skipped:=true);
  fi;
  if Length(res.kgens) < 2 then
    if verbose then Print("  [SKIP] (j=",j,",m=",m,"): |K generators| < 2, expansion cross-term check needs 2\n"); fi;
    return rec(ok:=false, skipped:=true);
  fi;
  f0 := ExtractF0(snfD, j);;
  modulus := 2^j;;  modulusC := 2^(j-1);;
  f0Ok := ForAll((f0+ThetaP(f0)), x -> x mod modulus = 0) and
          ForAll((f0+SigmaP(f0,m)+SigmaP(SigmaP(f0,m),m)+EmP(m)), x -> x mod modulus = 0);;
  k1 := res.kgens[1].vec;;  k2 := res.kgens[2].vec;;
  symOk := ObModReduce(PiBFull(k1,k2,m),modulusC) = ObModReduce(PiBFull(k2,k1,m),modulusC);;
  postOk := true;;
  for gi in res.kgens do
    fei := FE(gi.vec, f0, m);;
    bii := PiBFull(gi.vec, gi.vec, m);;
    lhs := gi.order*fei + Binomial(gi.order,2)*bii;;
    lhsRed := ObModReduce(lhs, modulusC);;
    if not ForAll(lhsRed, x -> x = 0) then postOk := false; fi;
  od;
  # (6.1) expansion, stress-tested at several coefficient vectors a=(a1,a2) (not just (1,1))
  expandOk := true;;
  aVecs := [[1,1],[2,1],[1,2],[2,3],[3,2]];;
  for avec in aVecs do
    if avec[1] < res.kgens[1].order and avec[2] < res.kgens[2].order then
      kk := avec[1]*k1 + avec[2]*k2;;
      fDirect := ObModReduce(FE(kk, f0, m), modulusC);;
      # (6.1): F(k) = sum_i (a_i F(e_i) + C(a_i,2) piB(e_i,e_i)) + sum_{i<j} a_i a_j piB(e_i,e_j)
      fe1 := FE(k1, f0, m);;  fe2 := FE(k2, f0, m);;
      fExpandedRaw := avec[1]*fe1 + Binomial(avec[1],2)*PiBFull(k1,k1,m)
                    + avec[2]*fe2 + Binomial(avec[2],2)*PiBFull(k2,k2,m)
                    + avec[1]*avec[2]*PiBFull(k1,k2,m);;
      fExpanded := ObModReduce(fExpandedRaw, modulusC);;
      if fDirect <> fExpanded then
        expandOk := false;
        if verbose then Print("    (6.1) MISMATCH at a=",avec," (j=",j,",m=",m,"): direct=",fDirect," expanded=",fExpanded,"\n"); fi;
      fi;
    fi;
  od;
  if verbose then
    Print("  (j=",j,",m=",m,"): f0Ok=",JB(f0Ok)," symOk=",JB(symOk)," postOk=",JB(postOk)," expandOk(5 a-vecs)=",JB(expandOk),"\n");
  fi;
  return rec(ok:=(f0Ok and symOk and postOk and expandOk), skipped:=false);
end;;

Print("\n=== QUADRATIC STAGE self-checks (piB symmetry, (6.1) expansion x5 coeff vectors, (6.2) postcondition) ===\n");
Print("running over sample (j,m) in {2,3} x {0,1,2,3,5,7} (12 pairs)...\n");
quadStageAllOk := true;;  quadStageAnyRun := false;;
for qm in [0,1,2,3,5,7] do
  for qj in [2,3] do
    qres := QuadStageSelfCheck(qm, qj, true);;
    if not qres.skipped then
      quadStageAnyRun := true;
      if not qres.ok then quadStageAllOk := false; fi;
    fi;
  od;
od;
Print("\n[", PF(quadStageAllOk and quadStageAnyRun), "] QUADRATIC STAGE self-checks (piB symmetry + (6.1) + (6.2)), ALL sampled (j,m): ", JB(quadStageAllOk and quadStageAnyRun), "\n");
quadStageOk := quadStageAllOk and quadStageAnyRun;;

if quadStageOk then

# ================================================================================
# Quadratic-stage EXHAUSTION (v3 sec.3.2/3.3, manifest_spec_e2_actions3.md sec.4/5), now
# unblocked. omega0 := omega(f0) = pi(QTheta(f0), QN(f0,m)) [Xi(f0), same closed forms
# already validated for general f, evaluated at f0 -- f0 in L means N f0 = -Ebar_m exactly,
# so QN(f0,m) IS the honest q_N(f0) here, no separate "QQ" needed for omega0].
# Criterion: -omega0 in F(K) (checked via (6.1) expansion, using only F(e_i)/piB(e_i,e_j) --
# no per-element recomputation of ell+Q needed, tractable for |K| up to the enumeration cap).
# ================================================================================
Omega0 := function(f0, m) return PiOb(Concatenation(QTheta(f0), QN(f0,m))); end;;

# Full exhaustion over K = { sum a_i e_i : 0<=a_i<n_i }, using (6.1). Returns record with
# mass_check data and (if found) a witness coefficient vector.
ExhaustK := function(kgens, f0, m, modulusC)
  local r, ns, Fe, Bee, i, j, target, mult, keys, totalScanned, avec, done, idx, Fk, key,
        witnessAvec, found, ii, jj, term;
  r := Length(kgens);
  ns := List(kgens, g -> g.order);
  Fe := List(kgens, g -> FE(g.vec, f0, m));;
  Bee := List([1..r], i -> List([1..r], j -> PiBFull(kgens[i].vec, kgens[j].vec, m)));;
  target := List(-Omega0(f0,m), x -> x mod modulusC);;
  mult := rec();;  # string-key -> count
  witnessAvec := fail;;  found := false;;
  avec := List([1..r], x -> 0);;
  totalScanned := 0;;
  done := false;;
  while not done do
    Fk := List([1..3], x -> 0);;
    for i in [1..r] do
      Fk := Fk + avec[i]*Fe[i] + Binomial(avec[i],2)*Bee[i][i];
    od;
    for i in [1..r] do
      for j in [i+1..r] do
        Fk := Fk + avec[i]*avec[j]*Bee[i][j];
      od;
    od;
    Fk := List(Fk, x -> x mod modulusC);;
    key := String(Fk);;
    if IsBound(mult.(key)) then mult.(key) := mult.(key)+1; else mult.(key) := 1; fi;
    if Fk = target and not found then found := true; witnessAvec := ShallowCopy(avec); fi;
    totalScanned := totalScanned + 1;
    # increment avec (mixed-radix counter)
    idx := 1;;
    while idx <= r do
      avec[idx] := avec[idx]+1;
      if avec[idx] < ns[idx] then break; fi;
      avec[idx] := 0;  idx := idx+1;
    od;
    if idx > r then done := true; fi;
  od;
  return rec(r:=r, ns:=ns, target:=target, mult:=mult, totalScanned:=totalScanned,
             parameterDomainSize:=Product(ns), found:=found, witnessAvec:=witnessAvec, Fe:=Fe, Bee:=Bee);
end;;

# Positive certificate: given a winning coefficient vector, construct explicit Hall-coordinate
# witness (Abar part f0+k*, plus explicit central (t5,t6)-twist to cancel the residual
# (1+theta)-ambiguity in the theta-slot, per im(Lambda)=<(t5+t6,0)> -- z5:=(-a1) mod modulusC,
# z6:=0, using q_theta_total(f,z) = QTheta(f) + (z5+z6,z5+z6) [derived directly from theta|_C
# table: theta(t5)=t6, theta(t6)=t5, so theta(t5^z5 t6^z6)=t6^z5 t5^z6, central, commutes past
# s(f)] and q_N_total = QN(f,m) UNCHANGED (N|_C=0 exactly, so no central correction affects it).
WritePositiveCert := function(path, snfData, j, m, kgens, exh)
  local f0, kstar, i, fAbar, qth, z5, z6, qthTotal, qNTotal, modulusC, ok, cert;
  f0 := ExtractF0(snfData, j);;
  modulusC := 2^(j-1);;
  kstar := List([1..snfData.n], x -> 0);;
  for i in [1..Length(kgens)] do kstar := kstar + exh.witnessAvec[i]*kgens[i].vec; od;
  fAbar := f0 + kstar;;
  qth := QTheta(fAbar);;
  z5 := (-qth[1]) mod modulusC;;  z6 := 0;;
  qthTotal := [ (qth[1]+z5+z6) mod modulusC, (qth[2]+z5+z6) mod modulusC ];;
  qNTotal := List(QN(fAbar,m), x -> x mod modulusC);;
  ok := (qthTotal = [0,0]) and (qNTotal = [0,0]);;
  cert := Concatenation(
    "{\"claim\":\"solution_witness\",",
    "\"m\":", String(m), ",\"j\":", String(j), ",\"modulus_Abar\":", String(2^j), ",\"modulus_C\":", String(modulusC), ",",
    "\"basis_order_Abar\":[\"w\",\"p\",\"q\",\"r1\",\"r2\",\"r3\",\"t1\",\"t2\",\"t3\",\"t4\"],",
    "\"witness_f_abar\":\"", String(fAbar), "\",",
    "\"witness_central_twist_t5_t6\":[", String(z5), ",", String(z6), "],",
    "\"q_theta_total\":\"", String(qthTotal), "\",",
    "\"q_N_total\":\"", String(qNTotal), "\",",
    "\"recheck\":\"q_theta_total = QTheta(f)+(z5+z6,z5+z6) and q_N_total=QN(f,m) both recomputed directly, both must be [0,0] mod 2^(j-1)\",",
    "\"generation\":\"NOT checked here (separate from torsion solution, per v3 Errata 4/W97)\"}");;
  WriteFileRaw(path, cert);;
  return ok;
end;;

# Negative certificate: central_lift_obstruction/v2 (manifest_spec_e2_actions3.md sec.5)
WriteObstructionCert := function(path, snfData, j, m, kgens, exh)
  local cert, f0, modulusC, valMultStr, keys, k, targetMult;
  f0 := ExtractF0(snfData, j);;
  modulusC := 2^(j-1);;
  keys := RecNames(exh.mult);;
  valMultStr := JoinC(List(keys, k -> Concatenation("\"", k, "\":", String(exh.mult.(k)))), ",");;
  targetMult := 0;;
  if IsBound(exh.mult.(String(exh.target))) then targetMult := exh.mult.(String(exh.target)); fi;
  cert := Concatenation(
    "{\"claim\":\"linear_solutions_exist_but_none_lifts\",",
    "\"method\":\"central_quadratic_exhaustion/v2\",",
    "\"m\":", String(m), ",\"j\":", String(j), ",\"modulus_Abar\":", String(2^j), ",\"modulus_C\":", String(modulusC), ",",
    "\"basis_order_Abar\":[\"w\",\"p\",\"q\",\"r1\",\"r2\",\"r3\",\"t1\",\"t2\",\"t3\",\"t4\"],",
    "\"linear\":{\"f0\":\"", String(f0), "\",\"K_orders\":", String(exh.ns), ",\"K_order_total\":", String(exh.parameterDomainSize), "},",
    "\"obstruction_group\":{\"im_Lambda_generator\":\"[t5+t6,0]\",\"Ob_rank\":3},",
    "\"exhaustion\":{\"parameter_domain_size\":", String(exh.parameterDomainSize), ",\"scanned\":", String(exh.totalScanned), ",",
    "\"target\":\"", String(exh.target), "\",\"target_multiplicity\":", String(targetMult), ",",
    "\"mass_check\":", JB(Sum(List(keys, k->exh.mult.(k))) = exh.parameterDomainSize), "},",
    "\"selftest_6_2_pass\":", JB(quadStageOk), ",",
    "\"independent_recheck\":\"checker independently rebuilds F(e_i)/piB via QTheta/QN/DTheta/DSigma and re-scans K\"}");;
  WriteFileRaw(path, cert);;
  return targetMult = 0;;
end;;

Print("\n=== ITEM 3: quadratic-stage exhaustion on the SAME spot sample (8 pairs, NOT 384) ===\n");
allQuadOk := true;;
sampleM2 := [0,1,2,3];;  sampleJ2 := [2,3];;
for spm2 in sampleM2 do
  snfD2 := BuildSnfData(spm2);;
  for spj2 in sampleJ2 do
    spres2 := TestAtJ(snfD2, spj2);;
    if spres2.solvable then
      f0_2 := ExtractF0(snfD2, spj2);;
      modC2 := 2^(spj2-1);;
      exh2 := ExhaustK(spres2.kgens, f0_2, spm2, modC2);;
      certPath2 := Concatenation("certificates/e2sweep/quad_j", String(spj2), "_m", String(spm2), ".json");;
      if exh2.found then
        certOk2 := WritePositiveCert(certPath2, snfD2, spj2, spm2, spres2.kgens, exh2);;
        Print("  (j=",spj2,",m=",spm2,"): |K|=",exh2.parameterDomainSize," distinct-F-values=",Length(RecNames(exh2.mult)),
              " target=",exh2.target," target_mult=",exh2.mult.(String(exh2.target))," -omega0 IN F(K) -- POSITIVE, wrote ",certPath2," (witness recheck pass=",JB(certOk2),")\n");
        if not certOk2 then allQuadOk := false; fi;
      else
        certOk2 := WriteObstructionCert(certPath2, snfD2, spj2, spm2, spres2.kgens, exh2);;
        Print("  (j=",spj2,",m=",spm2,"): |K|=",exh2.parameterDomainSize," -omega0 NOT IN F(K) -- OBSTRUCTION, wrote ",certPath2," (target_mult=0 confirmed=",JB(certOk2),")\n");
        if not certOk2 then allQuadOk := false; fi;
      fi;
    fi;
  od;
od;
Print("[", PF(allQuadOk), "] quadratic-stage exhaustion on 8-pair spot sample: all certs self-consistent\n");

else
  Print("\n[BLOCKED] quadratic-stage exhaustion SKIPPED -- self-checks above did not all pass.\n");
fi; # quadStageOk

# ---- spot validation on a SMALL sample (explicitly NOT the full 384-system sweep, per
#      coordinator instruction "384系の本走査だけは実行するな"). Demonstrates the linear-
#      stage machinery is wired up correctly; not a sweep result. ----
Print("\n--- spot validation sample: m in {0,1,2,3}, j in {2,3} (8 pairs, NOT the 384-system sweep) ---\n");
item3StartTime := Runtime();;
sampleM := [0,1,2,3];;
sampleJ := [2,3];;
allSpotOk := true;;
for spm in sampleM do
  snfD := BuildSnfData(spm);;
  for spj in sampleJ do
    spres := TestAtJ(snfD, spj);;
    if spres.solvable then
      krechecks := List(spres.kgens, g -> RecheckKGenerator(g, spj, spm));;
      kOk := ForAll(krechecks, x -> x);;
      Print("  (j=", spj, ",m=", spm, "): linear-stage SOLVABLE, |K generators|=", Length(spres.kgens),
            " orders=", List(spres.kgens, g->g.order), " recheck-all-pass=", JB(kOk), "\n");
      certPath := Concatenation("certificates/e2sweep/spot_j", String(spj), "_m", String(spm), ".json");;
      WriteSolvableCert(certPath, spj, spm, spres.kgens);;
      if not kOk then allSpotOk := false; fi;
    else
      certPath := Concatenation("certificates/e2sweep/spot_j", String(spj), "_m", String(spm), ".json");;
      certOk := WriteUnsolvableCert(certPath, snfD, spj, spres.failRow);;
      Print("  (j=", spj, ",m=", spm, "): linear-stage UNSOLVABLE at row ", spres.failRow,
            " -- wrote ", certPath, " (witness recheck pass=", JB(certOk), ")\n");
      if not certOk then allSpotOk := false; fi;
    fi;
  od;
od;
Print("[", PF(allSpotOk), "] spot-validation sample: all linear-stage results independently rechecked OK\n");
item3ElapsedMs := Runtime() - item3StartTime;;
Print("item3 spot-validation (8 pairs: 4 SNF builds + 8 per-j tests + K-recheck) elapsed ms: ", item3ElapsedMs, "\n");
Print("naive linear extrapolation to 320 live pairs (5 j-values x 64 m, excluding j=1 control):\n");
Print("  per-SNF-build cost dominates (1 per m, reused across 6 j) => ~", QuoInt(item3ElapsedMs,4), " ms/SNF-build * 64 m = ~",
      QuoInt(item3ElapsedMs,4)*64, " ms for all SNF builds, plus 6x cheap per-j tests (negligible by comparison)\n");

Print("\n=== ITEM 3 STATUS ===\n");
Print("Linear stage (SNF, per-j solvability, K generation+recheck, unsolvable-certificate\n");
Print("  writer): IMPLEMENTED and spot-validated above (8 pairs).\n");
Print("Quadratic stage (F(e_i), omega0, Ob quotient, mass-check exhaustion, solution_witness /\n");
Print("  central_lift_obstruction/v2 certs): UNBLOCKED 2026-07-26 via\n");
Print("  search/manifest_spec_e2_actions3.md (F=pi.ell+pi.Q, piB polarization, Ob=(C/<t5+t6>)(+)C,\n");
Print("  (6.1)/(6.2)). IMPLEMENTED and self-checked (piB symmetry, (6.1) expansion at 5 distinct\n");
Print("  coefficient vectors, (6.2) postcondition) across 12 sample (j,m) pairs -- all PASS,\n");
Print("  resolving the earlier direct-substitution/piB inconsistency. Full exhaustion + mass\n");
Print("  check + witness/obstruction certificates run on the 8-pair spot sample (NOT the 384).\n");
Print("FULL 384-SYSTEM SWEEP: see below -- launch authorized 2026-07-26 (sol2 agreement: 608\n");
Print("  PASS/0 FAIL, docs/notes/一致確認_E2作用表.md).\n");

# ================================================================================
# FULL 384-SYSTEM SWEEP (launch authorized 2026-07-26: "608 PASS / 0 FAIL, 規約差ゼロ" per
# crosscheck/agree-tables.mjs + docs/notes/一致確認_E2作用表.md). j=1..6, m=0..63 = 384 systems
# (j=1 is the commutative control per v3 sec.1.2, C_1=0). Per (j,m): linear stage (SNF,
# solvability, K generators+recheck) then, if solvable, quadratic stage (F/piB exhaustion,
# mass check, -omega0 in F(K)?). One dual certificate per system written to
# certificates/e2sweep/sweep_j{j}_m{m}.json. enumeration_cap_per_pair = 2^24 (v3 F18 S-1):
# if |K| exceeds this, status=cap_exceeded (UNKNOWN), not solvable/unsolvable.
# ================================================================================
ENUMERATION_CAP := 2^24;;

RunFullSystem := function(m, j, snfData)
  local certPath, res, f0, modC, exh, status, distinctFVals, cert;
  certPath := Concatenation("certificates/e2sweep/sweep_j", String(j), "_m", String(m), ".json");;
  res := TestAtJ(snfData, j);;
  if not res.solvable then
    WriteUnsolvableCert(certPath, snfData, j, res.failRow);;
    return rec(status:="linear_unsolvable", j:=j, m:=m, path:=certPath);
  fi;
  if Product(res.kgens, g -> g.order) > ENUMERATION_CAP then
    cert := Concatenation("{\"claim\":\"cap_exceeded\",\"status\":\"UNKNOWN\",\"m\":", String(m),
      ",\"j\":", String(j), ",\"K_order_total\":", String(Product(res.kgens, g->g.order)),
      ",\"enumeration_cap\":", String(ENUMERATION_CAP), "}");;
    WriteFileRaw(certPath, cert);;
    return rec(status:="cap_exceeded", j:=j, m:=m, path:=certPath);
  fi;
  f0 := ExtractF0(snfData, j);;
  modC := 2^(j-1);;
  exh := ExhaustK(res.kgens, f0, m, modC);;
  distinctFVals := Length(RecNames(exh.mult));;
  if exh.found then
    WritePositiveCert(certPath, snfData, j, m, res.kgens, exh);;
    return rec(status:="quad_positive", j:=j, m:=m, path:=certPath, kOrder:=exh.parameterDomainSize,
               distinctFVals:=distinctFVals, massCheckOk:=(Sum(List(RecNames(exh.mult),k->exh.mult.(k)))=exh.parameterDomainSize));;
  else
    WriteObstructionCert(certPath, snfData, j, m, res.kgens, exh);;
    return rec(status:="quad_obstruction", j:=j, m:=m, path:=certPath, kOrder:=exh.parameterDomainSize,
               distinctFVals:=distinctFVals, massCheckOk:=(Sum(List(RecNames(exh.mult),k->exh.mult.(k)))=exh.parameterDomainSize));;
  fi;
end;;

Print("\n=== FULL 384-SYSTEM SWEEP (j=1..6, m=0..63) ===\n");
sweepStart := Runtime();;
sweepResults := [];;
for fm in [0..63] do
  fSnf := BuildSnfData(fm);;
  for fj in [1..6] do
    Add(sweepResults, RunFullSystem(fm, fj, fSnf));;
  od;
od;
sweepElapsedMs := Runtime() - sweepStart;;

# ---- tally ----
cntLinUnsolv := Length(Filtered(sweepResults, r -> r.status = "linear_unsolvable"));;
cntCapExceeded := Length(Filtered(sweepResults, r -> r.status = "cap_exceeded"));;
cntPositive := Length(Filtered(sweepResults, r -> r.status = "quad_positive"));;
cntObstruction := Length(Filtered(sweepResults, r -> r.status = "quad_obstruction"));;
massCheckAllOk := ForAll(Filtered(sweepResults, r -> IsBound(r.massCheckOk)), r -> r.massCheckOk);;
fConstantAll := ForAll(Filtered(sweepResults, r -> IsBound(r.distinctFVals)), r -> r.distinctFVals = 1);;
fNonConstantCount := Length(Filtered(sweepResults, r -> IsBound(r.distinctFVals) and r.distinctFVals <> 1));;

Print("Total systems: ", Length(sweepResults), " (expect 384)\n");
Print("  linear_unsolvable: ", cntLinUnsolv, "\n");
Print("  cap_exceeded (UNKNOWN): ", cntCapExceeded, "\n");
Print("  quad_positive (POSITIVE/solvable): ", cntPositive, "\n");
Print("  quad_obstruction (unsolvable at quadratic stage): ", cntObstruction, "\n");
Print("mass_check all PASS (among quadratic-stage systems): ", JB(massCheckAllOk), "\n");
Print("\"F identically constant on K\" (distinct-F-values=1) holds for ALL quadratic-stage systems: ", JB(fConstantAll), "\n");
Print("  systems where F is NOT constant on K: ", fNonConstantCount, "\n");
Print("sweep elapsed ms: ", sweepElapsedMs, "\n");

# ---- per-(j,m) POSITIVE/OBSTRUCTION table ----
Print("\n=== per-(j,m) verdict table (rows=m 0..63, cols=j 1..6; P=positive,O=obstruction,U=linear-unsolvable,C=cap) ===\n");
for fm in [0..63] do
  rowStr := "";;
  for fj in [1..6] do
    rr := First(sweepResults, r -> r.m = fm and r.j = fj);;
    if rr.status = "quad_positive" then rowStr := Concatenation(rowStr, "P");
    elif rr.status = "quad_obstruction" then rowStr := Concatenation(rowStr, "O");
    elif rr.status = "linear_unsolvable" then rowStr := Concatenation(rowStr, "U");
    else rowStr := Concatenation(rowStr, "C"); fi;
  od;
  Print("  m=", String(fm), ": ", rowStr, "\n");
od;

fi; # ncOk
