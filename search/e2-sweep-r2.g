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

# section cocycle c_s(a,b) := a_w * (b_p, b_q), derived from beta (see header note)
Cs := function(a, b) return [ a[1]*b[2], a[1]*b[3] ]; end;;

# Lambda: C -> C x C, Lambda(z) = ((1+theta)z, N_C(z)) = ((1+theta)z, 0) since N_C=0
Lambda1 := function(z) return z + ThetaC(z); end;;  # (1+theta)z
Print("im(Lambda) generator check: Lambda((1,0)) = ", JoinC([String(Lambda1([1,0])),String(NC([1,0]))],","), "\n");
Print("  Lambda((0,1)) = (1+theta)(0,1) = ", String(Lambda1([0,1])), "\n");
Print("[", PF(Lambda1([1,0]) = [1,1] and Lambda1([0,1]) = [1,1]), "] im(Lambda) generated by (1,1) in the (1+theta) coordinate (matches <(t5+t6,0)> structural prediction)\n");

# ================================================================================
# q_theta, q_N on L (domain: f with (1+bar_theta)f=0), per header derivation
# ================================================================================
QTheta := function(f)
  local thf;
  thf := ThetaP(f);
  return Cs(thf, f);   # valid since thf+f=0 for f in L
end;;

QN := function(f, m)
  local a1, a2, a3, a4, term1, term2, term3;
  a1 := EmP(m);
  a3 := SigmaP(f, m);
  a2 := SigmaP(a3, m);
  a4 := f;
  term1 := Cs(a1+a2, a3);
  term2 := Cs(a1, a2);
  term3 := Cs(a1+a2+a3, a4);
  return term3 + term1 + term2;   # additive in C = Z^2
end;;

Xi := function(f, m) return Concatenation(QTheta(f), QN(f,m)); end;;  # 4-vector in C x C

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
