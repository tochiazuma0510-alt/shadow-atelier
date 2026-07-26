# search/e19.g -- route G (GAP), independent implementation of the E19 two-system verification.
# Design source: docs/week4-E19二系統化指示書_v1.md sec.1-4 (spec projection only). This file does
# NOT read docs/scout/metab.mjs's code (independence requirement, sec.1 "node のコードを移植して
# はならない") -- it re-derives the model fresh from the mathematical definitions in the doc.
#
# Usage: .\gap.ps1 -o 2g search\e19.g

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
IntBool := function(b) if b then return 1; else return 0; fi; end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;
failCount := 0;;
TT := function(name, cond)
  if cond then Print("PASS  ", name, "\n");
  else Print("FAIL  ", name, "\n"); failCount := failCount + 1; fi;
end;;

# ================================================================================
# truncated polynomial ring Z[S,T]/(S,T)^{DG+1}, DG = c-2. Elements represented as
# plain integer vectors indexed by BASIS position (basis fixed once per class via SetClass).
# ================================================================================
DG := 0;;  BASIS := [];;  IDXTAB := [];;  # IDXTAB[a+1][b+1] = basis index (1-based) or 0 if absent/out of range

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

# (1+X)^{-1} = sum_{k>=0} (-X)^k, truncated at degree DG (X has zero constant term)
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

# substitution f(S,T) -> f(U,V), U,V polynomials with zero constant term
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

# matrix of a linear operator op (basis vector e_i -> op(e_i)); returns list of N vectors,
# matOf(op)[i] = op(e_i) (1-indexed)
MatOf := function(op)
  local n, m, i, e;
  n := NN();
  m := [];
  for i in [1..n] do
    e := ZeroP();  e[i] := 1;
    Add(m, op(e));
  od;
  return m;
end;;

# ================================================================================
# self-checks (13 items, sec.1.3) -- run at class 4
# ================================================================================
SetClass(4);;
eqv := function(u,v) return u = v; end;;

TT("theta^2 = id", eqv(ThetaP(ThetaP(Sgen())), Sgen()) and eqv(ThetaP(ThetaP(ConstP(1))), ConstP(1)));
tau3ok := true;;
for ii in [1..NN()] do
  ee := ZeroP();;  ee[ii] := 1;;
  if not eqv(TauP(TauP(TauP(ee))), ee) then tau3ok := false; fi;
od;
TT("tau^3 = id", tau3ok);
TT("theta(w) = -w", eqv(ThetaP(ConstP(1)), Pscal(ConstP(1),-1)));
TT("tau(w) = w - p + r1", ThetaP(ConstP(1))=ThetaP(ConstP(1)) and TauP(ConstP(1)) = [1,-1,0,1,0,0]);
TT("tau(p) = q - r2", TauP(Sgen()) = [0,0,1,0,-1,0]);
TT("tau(q) = -p-q+2r1+2r2+r3", TauP(Tgen()) = [0,-1,-1,2,2,1]);
TT("E_1 = [-1,1,0,-1,0,0]", EmP(1) = [-1,1,0,-1,0,0]);
TT("E_2 = [-3,4,-1,-5,1,0]", EmP(2) = [-3,4,-1,-5,1,0]);
TT("E_3 = [-6,10,-4,-15,5,-1]", EmP(3) = [-6,10,-4,-15,5,-1]);

# Prop E1: theta.tau.theta = iota_x o tau^{-1} (iota_x = mult by s, tau^{-1}=tau^2)
propE1ok := true;;
for ii in [1..NN()] do
  ee := ZeroP();;  ee[ii] := 1;;
  lhs := ThetaP(TauP(ThetaP(ee)));;
  rhs := Pmul(Sunit(), TauP(TauP(ee)));;
  if not eqv(lhs,rhs) then propE1ok := false; fi;
od;
TT("Prop E1: theta.tau.theta = iota_x o tau^{-1}", propE1ok);

sigmaFixOk := true;;
for mm2 in [0..6] do
  if not eqv(SigmaP(EmP(mm2), mm2), EmP(mm2)) then sigmaFixOk := false; fi;
od;
TT("sigma_m(E_m) = E_m (m=0..6)", sigmaFixOk);

# Lemma B: 3E_m = -T_m kappa_m + B_m rho (m=0..12), kappa_m = N(w), rho = r1+r2+r3
lemmaBok := true;;
for mm2 in [0..12] do
  smOp := function(f) return SigmaP(f,mm2); end;;
  smMat := MatOf(smOp);;
  # N = I + sm + sm^2 applied to w=ConstP(1): kappa_m = w + sm(w) + sm(sm(w))
  wv := ConstP(1);;
  kap := Padd(Padd(wv, smOp(wv)), smOp(smOp(wv)));;
  rho := ZeroP();;  rho[IdxOf(2,0)]:=1;; rho[IdxOf(1,1)]:=1;; rho[IdxOf(0,2)]:=1;;
  Tm := (mm2*(mm2+1))/2;;  Bm := (Tm*(Tm+1))/2;;
  em := EmP(mm2);;
  lhsv := Pscal(em,3);;
  rhsv := Padd(Pscal(kap,-Tm), Pscal(rho,Bm));;
  if not eqv(lhsv,rhsv) then lemmaBok := false; fi;
od;
TT("Lemma B: 3E_m = -T_m kappa_m + B_m rho (m=0..12)", lemmaBok);

# Lemma A: N(p+q) = 3(r1+r2+r3), m-independent, m=0..8
lemmaAok := true;;
for mm2 in [0..8] do
  smOp := function(f) return SigmaP(f,mm2); end;;
  pq := Padd(Sgen(),Tgen());;
  val := Padd(Padd(pq, smOp(pq)), smOp(smOp(pq)));;
  expected := ZeroP();;  expected[IdxOf(2,0)]:=3;; expected[IdxOf(1,1)]:=3;; expected[IdxOf(0,2)]:=3;;
  if not eqv(val,expected) then lemmaAok := false; fi;
od;
TT("Lemma A: N(p+q) = 3(r1+r2+r3), m-independent", lemmaAok);

Print("\n");
if failCount > 0 then
  Print("*** ", failCount, " SELF-TEST FAILURES -- results below SKIPPED (F8-4 analog) ***\n");
fi;
if failCount = 0 then
Print("--- all GAP self-tests passed ---\n\n");

# ================================================================================
# per-(c,m) dump + SNF three-stage check
# ================================================================================
# builds the (2n x n) matrix M and length-2n vector b for class c, parameter m, per
# docs/week4-E19二系統化指示書_v1.md sec.1.4 (M_{i,k}=((1+theta)e_k)_i, M_{n+i,k}=(N e_k)_i,
# b_i=0, b_{n+i}=-(E_m)_i).
BuildSystem := function(c, m)
  local n, thMat, smMat, sm2Mat, b, rows, rhs, i, k, j, val;
  SetClass(c);
  n := NN();
  thMat := MatOf(ThetaP);;              # thMat[k] = theta(e_k), a length-n vector
  smMat := MatOf(x -> SigmaP(x,m));;    # smMat[k] = sigma_m(e_k)
  # sm2Mat[k] = sigma_m(sigma_m(e_k)) = sum_j smMat[k][j] * smMat[j]  (linearity)
  sm2Mat := [];
  for k in [1..n] do
    val := ZeroP();
    for j in [1..n] do
      if smMat[k][j] <> 0 then val := Padd(val, Pscal(smMat[j], smMat[k][j])); fi;
    od;
    Add(sm2Mat, val);
  od;
  b := EmP(m);;
  rows := [];;  rhs := [];;
  for i in [1..n] do
    rows[i] := List([1..n], k -> thMat[k][i] + (IntBool(i=k)));  # (1+theta)e_k, i-th coord
    rhs[i] := 0;
  od;
  for i in [1..n] do
    rows[n+i] := List([1..n], k -> IntBool(i=k) + smMat[k][i] + sm2Mat[k][i]);  # N e_k, i-th coord
    rhs[n+i] := -b[i];
  od;
  return rec(n:=n, rows:=rows, rhs:=rhs);
end;;

# serialize per the exact byte format (sec.1.4): row entries "," joined, rows ";" joined, no
# trailing separator; b entries "," joined.
SerializeM := function(rows)
  local rowStrs, r, parts;
  rowStrs := [];
  for r in rows do
    parts := List(r, String);
    Add(rowStrs, JoinC(parts, ","));
  od;
  return JoinC(rowStrs, ";");
end;;
SerializeB := function(rhs) return JoinC(List(rhs, String), ","); end;;

WriteFileRaw := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

# ================================================================================
# main loop: c=3..7, m=0..63 -- build, dump (M,b text + a GAP-side content string for later
# hashing by node/shell), run SNF three-stage postcondition + rank/solvability checks.
# ================================================================================
Print("=== route G (GAP): building systems and running SNF for c=3..7, m=0..63 ===\n");

resultsSummary := [];;
s3FailTotal := 0;;
overallStart := Runtime();;
capAggregate := 1800.0;;  # sec.2.1 wall_seconds_per_route (one route, one class = 64 m's); we
                          # track total here and stop if exceeded (S-1/S-2 analog for route G)
haltAll := false;;

for c in [3..7] do
  if haltAll then break; fi;
  classStart := Runtime();;
  allSolvC := true;;  maxV2C := 0;;
  for m in [0..63] do
    if (Runtime()-overallStart)/1000.0 > 7200.0 then
      Print("[CAP EXCEEDED] aggregate wall_seconds_universe_total (7200s) -- halting, remaining pairs UNKNOWN\n");
      haltAll := true; break;
    fi;
    sys := BuildSystem(c, m);;
    Mstr := SerializeM(sys.rows);;
    bstr := SerializeB(sys.rhs);;
    WriteFileRaw(Concatenation("certificates/e19/gap_system_c", String(c), "_m", String(m), ".txt"),
                 Concatenation("M=", Mstr, "\nb=", bstr, "\n"));

    # canonical SNF via GAP library function
    Mmat := sys.rows;;
    snfResult := SmithNormalFormIntegerMatTransforms(Mmat);;
    U := snfResult.rowtrans;;  V := snfResult.coltrans;;  D := snfResult.normal;;
    rank := snfResult.rank;;

    # postconditions (sec.2.1, all must hold or halt)
    detUOk := (AbsInt(DeterminantMat(U)) = 1);;
    detVOk := (AbsInt(DeterminantMat(V)) = 1);;
    UMVrecheck := (U * Mmat * V = D);;
    diagOk := true;;
    for ii in [1..Length(D)] do
      for jj in [1..Length(D[1])] do
        if ii <> jj and D[ii][jj] <> 0 then diagOk := false; fi;
      od;
    od;
    divChainOk := true;;
    diagVals := List([1..Minimum(Length(D),Length(D[1]))], ii -> D[ii][ii]);;
    posDiag := Filtered(diagVals, x -> x > 0);;
    for ii in [1..Length(posDiag)-1] do
      if posDiag[ii+1] mod posDiag[ii] <> 0 then divChainOk := false; fi;
    od;
    rankOk := (rank = Length(posDiag));;

    postOk := detUOk and detVOk and UMVrecheck and diagOk and divChainOk and rankOk;;
    if not postOk then
      Print("[S-4-analog FAIL] SNF postcondition failed at c=", c, " m=", m, " -- halting\n");
      s3FailTotal := s3FailTotal + 1;
      haltAll := true;
      break;
    fi;

    # solvability quantities (sec.2.2)
    cvec := U * sys.rhs;;
    rankQ := rank;;
    rankF2 := Length(Filtered([1..rank], ii -> D[ii][ii] mod 2 <> 0));;
    maxV2Divisor := 0;;
    for ii in [1..rank] do
      dv := D[ii][ii];;
      vv := 0;;  tmp := dv;;
      while tmp mod 2 = 0 do tmp := tmp/2; vv := vv+1; od;
      if vv > maxV2Divisor then maxV2Divisor := vv; fi;
    od;
    if maxV2Divisor > maxV2C then maxV2C := maxV2Divisor; fi;

    z2solv := true;;
    for ii in [1..rank] do
      dv := D[ii][ii];;
      cv := cvec[ii];;
      vD := 0;;  tmpD := dv;; while tmpD mod 2 = 0 do tmpD:=tmpD/2; vD:=vD+1; od;
      if cv = 0 then vC := 1000000;; else
        vC := 0;;  tmpC := AbsInt(cv);; while tmpC mod 2 = 0 do tmpC:=tmpC/2; vC:=vC+1; od;
      fi;
      if vC < vD then z2solv := false; fi;
    od;
    for ii in [rank+1..Length(cvec)] do
      if cvec[ii] <> 0 then z2solv := false; fi;
    od;
    qsolv := true;;
    for ii in [rank+1..Length(cvec)] do
      if cvec[ii] <> 0 then qsolv := false; fi;
    od;
    if not z2solv then allSolvC := false; fi;

    Add(resultsSummary, rec(c:=c, m:=m, rank:=rank, rankF2:=rankF2, maxV2:=maxV2Divisor,
                             z2solv:=z2solv, qsolv:=qsolv, elementary_divisors:=diagVals{[1..rank]}));

    # ---- witness sample (sec.3, spot-checked at m=0 of each class to keep runtime small) ----
    if m = 0 and z2solv then
      yv := List([1..rank], ii -> cvec[ii]/D[ii][ii]);;
      for ii in [rank+1..sys.n] do Add(yv, 0); od;
      xv := V * yv;;
      # residual: M*x - b (should be 0 exactly, since y,x constructed from an exact SNF solution)
      resid := (Mmat * xv) - sys.rhs;;
      residZero := ForAll(resid, z -> z = 0);;
      Print("  witness sample c=", c, " m=0: residual all zero = ", residZero, "\n");
      if not residZero then
        Print("  [S-4-analog FAIL] witness residual nonzero at c=", c, " m=0 -- flagging\n");
      fi;
    fi;
  od;
  Print("class ", c, ": all m in 0..63 Z2-solvable = ", allSolvC, ", max_v2_divisor = ", maxV2C,
        ", time_ms=", Runtime()-classStart, "\n");
od;

Print("\ntotal elapsed ms: ", Runtime()-startTime, "\n");
Print("total (c,m) pairs processed: ", Length(resultsSummary), "\n");

# write a compact summary for node-side comparison
summaryLines := [];;
for rr in resultsSummary do
  Add(summaryLines, Concatenation("{\"c\":", String(rr.c), ",\"m\":", String(rr.m),
      ",\"rank\":", String(rr.rank), ",\"rank_F2\":", String(rr.rankF2),
      ",\"max_v2_divisor\":", String(rr.maxV2), ",\"Z2_solvable\":", JB(rr.z2solv),
      ",\"Q_solvable\":", JB(rr.qsolv), "}"));
od;
WriteFileRaw("certificates/e19/gap_summary.json", Concatenation("[", JoinC(summaryLines,","), "]"));
Print("wrote certificates/e19/gap_summary.json\n");

fi; # failCount = 0
QUIT;
