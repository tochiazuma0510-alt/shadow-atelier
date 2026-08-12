## scratchpad/d972_phase1_smoke3.g -- timing benchmark for per-shadow lift check on K
## (single M-shadow, up to 6 m_K candidates x 27 kernel elements)
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0 := GAPLIB_WallElapsedMs();;
ShiftPerm := function(p, offset, size)
  local l, j;
  l := [1 .. offset+size];
  for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
  return PermList(l);
end;;
DirectSumPerm := function(p1, deg1, p2, deg2)
  return p1 * ShiftPerm(p2, deg1, deg2);
end;;
CharmingSetOf := function(nOrd)
  return Filtered([0 .. nOrd-1], mm -> Gcd(2*mm+1, nOrd) = 1);
end;;

ScanRoofHexagon := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, h10Fail, h11Fail, genFail, shadows,
        m, u, f, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj,
        candidateTotal, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  D := DerivedSubgroup(G);
  Delts := Elements(D);
  h10Fail := 0;  h11Fail := 0;  genFail := 0;  shadows := [];
  candidateTotal := Length(Delts) * Length(charmingSet);
  for m in charmingSet do
    u := 2*m + 1;
    for i in [1 .. Length(Delts)] do
      f := Delts[i];
      thetaf := Image(thetaHom, f);
      hex310 := AbstractProd([f, thetaf]) = Identity(G);
      if not hex310 then h10Fail := h10Fail + 1; continue; fi;
      ymf := AbstractProd([qrec.y^m, f]);
      tauymf := Image(tauHom, ymf);
      tau2ymf := Image(tauHom, tauymf);
      hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(G);
      if not hex311 then h11Fail := h11Fail + 1; continue; fi;
      genA := qrec.x^u;
      genB := AbstractProd([f^-1, qrec.y^u, f]);
      surj := Size(Group(genA, genB)) = Size(G);
      if not surj then
        genFail := genFail + 1;
      else
        Add(shadows, rec(m := m, f := f));
      fi;
    od;
  od;
  return rec(candidate_total := candidateTotal, h10_fail := h10Fail, h11_fail := h11Fail,
             generation_fail := genFail, shadow_total := Length(shadows), shadows := shadows,
             derived_order := Length(Delts));
end;;

g9 := MakeGn(9);; g27 := MakeGn(27);;
CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);; Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);; Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm * Tperm^-1;; Xperm := wPerm^2;; Yperm := Sperm^-1 * Xperm * Sperm;;

XM := DirectSumPerm(g9.x, 27, Xperm, 9);; YM := DirectSumPerm(g9.y, 27, Yperm, 9);;
GM := Group(XM, YM);;  Mord := Lcm(Order(XM),Order(YM));;
XK := DirectSumPerm(g27.x, 81, Xperm, 9);; YK := DirectSumPerm(g27.y, 81, Yperm, 9);;
GK := Group(XK, YK);;  Kord := Lcm(Order(XK),Order(YK));;
homKtoM := GroupHomomorphismByImages(GK, GM, [XK,YK], [XM,YM]);;
KerHom := Kernel(homKtoM);;  KerElts := Elements(KerHom);;
Print("|GM|=", Size(GM), " Mord=", Mord, " |GK|=", Size(GK), " Kord=", Kord, " |Ker|=", Size(KerHom), "\n");

Print("=== recompute M shadows (972 expected) ===\n");
tm0 := GAPLIB_WallElapsedMs();;
Mcharm := CharmingSetOf(Mord);;
resM := ScanRoofHexagon(rec(x:=XM, y:=YM, G:=GM), Mcharm);;
tm1 := GAPLIB_WallElapsedMs();;
Print("  shadow_total=", resM.shadow_total, "  elapsed_ms=", tm1-tm0, "\n");

Print("=== build theta/tau homs for K ===\n");
zEltK := AbstractProd([XK, YK])^-1;;
thetaHomK := GroupHomomorphismByImages(GK, GK, [XK, YK], [YK, XK]);;
tauHomK := GroupHomomorphismByImages(GK, GK, [XK, YK], [YK, zEltK]);;
Print("  theta/tau well-defined: ", thetaHomK<>fail, " ", tauHomK<>fail, "\n");

CheckKCandidate := function(mK, fK)
  local uK, thetaf, hex310, ymf, tauymf, tau2ymf, hex311, genA, genB, surj;
  thetaf := Image(thetaHomK, fK);;
  hex310 := AbstractProd([fK, thetaf]) = Identity(GK);;
  if not hex310 then return rec(pass:=false, stage:="hex310"); fi;
  ymf := AbstractProd([YK^mK, fK]);;
  tauymf := Image(tauHomK, ymf);;
  tau2ymf := Image(tauHomK, tauymf);;
  hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(GK);;
  if not hex311 then return rec(pass:=false, stage:="hex311"); fi;
  uK := 2*mK+1;;
  genA := XK^uK;;  genB := AbstractProd([fK^-1, YK^uK, fK]);;
  surj := Size(Group(genA,genB)) = Size(GK);;
  if not surj then return rec(pass:=false, stage:="surj"); fi;
  return rec(pass:=true, stage:="ok");;
end;;

## pick first M-shadow, benchmark full candidate sweep (up to 6 m_K x 27 k)
sh1 := resM.shadows[1];;
m1 := sh1.m;;  f1 := sh1.f;;
Print("\n=== benchmark: shadow #1 (m=", m1, ") full candidate sweep ===\n");
tb0 := GAPLIB_WallElapsedMs();;
f0 := PreImagesRepresentative(homKtoM, f1);;
mKcands := Filtered([0..Kord-1], mm -> (mm mod 9 = m1 mod 9) and Gcd(2*mm+1,Kord)=1);;
Print("  m_K candidates (", Length(mKcands), "): ", mKcands, "\n");
checked := 0;;  foundLift := false;;  witness := fail;;
for mK in mKcands do
  for k in KerElts do
    fK := f0*k;;
    checked := checked + 1;;
    res := CheckKCandidate(mK, fK);;
    if res.pass then foundLift := true; witness := rec(mK:=mK, fK:=fK); break; fi;
  od;
  if foundLift then break; fi;
od;
tb1 := GAPLIB_WallElapsedMs();;
Print("  checked=", checked, "  found_lift=", foundLift, "  elapsed_ms=", tb1-tb0, "\n");

## also time a full sweep with NO early exit (worst case, all 972*6*27 style)
Print("\n=== benchmark: full sweep, no early exit (mK x k = ", Length(mKcands)*Length(KerElts), " candidates) ===\n");
tc0 := GAPLIB_WallElapsedMs();;
passCount := 0;;
for mK in mKcands do
  for k in KerElts do
    fK := f0*k;;
    res := CheckKCandidate(mK, fK);;
    if res.pass then passCount := passCount+1; fi;
  od;
od;
tc1 := GAPLIB_WallElapsedMs();;
Print("  passCount=", passCount, "  elapsed_ms=", tc1-tc0, "  per_candidate_ms=", Float((tc1-tc0)/(Length(mKcands)*Length(KerElts))), "\n");

Print("\ntotal elapsed_ms=", GAPLIB_WallElapsedMs()-t0, "\n");
QUIT;
