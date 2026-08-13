# search/d972_phase2_v1.g
# Phase 2 producer for the cumulative refinement chain
#   L1 = K^(27) cap N_S4
#   L2 = K^(27) cap K^(36) cap N_S4 = K^(108) cap N_S4.
#
# The reduction coordinate is (3.60): m is reduced modulo H_ord.
# In particular, it is NOT enough to compare 2*m+1 modulo H_ord.
# This version deliberately uses the exact m-coordinate at every edge.

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0Global := GAPLIB_WallElapsedMs();;
checkpointPath := "search/certs/d972_phase2_v1_checkpoint.json";;

WriteCheckpoint := function(stage, processed, depth1Count, depth2Count)
  WriteFile(checkpointPath, Concatenation(
    "{\"schema\":\"d972_phase2_checkpoint/v1\",\"stage\":\"", stage,
    "\",\"processed\":", String(processed),
    ",\"depth1_raw\":", String(depth1Count),
    ",\"depth2_raw\":", String(depth2Count),
    ",\"elapsed_ms\":", String(GAPLIB_WallElapsedMs()-t0Global),
    ",\"complete\":false,\"u_touched\":false,\"c_touched\":false}"
  ));
end;;

ScanRoofHexagon := function(qrec, charmingSet)
  local G, D, Delts, thetaHom, tauHom, zElt, shadows,
        m, u, f, thetaf, ymf, tauymf, tau2ymf, genA, genB, i;
  G := qrec.G;
  zElt := AbstractProd([qrec.x, qrec.y])^-1;
  thetaHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, qrec.x]);
  tauHom := GroupHomomorphismByImages(G, G, [qrec.x, qrec.y], [qrec.y, zElt]);
  if thetaHom = fail or tauHom = fail then Error("roof theta/tau map missing"); fi;
  D := DerivedSubgroup(G);  Delts := Elements(D);  shadows := [];
  for m in charmingSet do
    u := 2*m + 1;
    for i in [1..Length(Delts)] do
      f := Delts[i];
      thetaf := Image(thetaHom, f);
      if AbstractProd([f,thetaf]) <> Identity(G) then continue; fi;
      ymf := AbstractProd([qrec.y^m,f]);
      tauymf := Image(tauHom,ymf);  tau2ymf := Image(tauHom,tauymf);
      if AbstractProd([tau2ymf,tauymf,ymf]) <> Identity(G) then continue; fi;
      genA := qrec.x^u;
      genB := AbstractProd([f^-1,qrec.y^u,f]);
      if Size(Group(genA,genB)) = Size(G) then Add(shadows,rec(m:=m,f:=f)); fi;
    od;
  od;
  return rec(shadow_total:=Length(shadows), shadows:=shadows, derived_order:=Length(Delts));
end;;

CharmingSetOf := function(nOrd)
  return Filtered([0..nOrd-1], mm -> Gcd(2*mm+1,nOrd)=1);
end;;

ShiftPerm := function(p, offset, size)
  local l,j;
  l := [1..offset+size];
  for j in [1..size] do l[offset+j] := offset+(j^p); od;
  return PermList(l);
end;;

DirectSumPerm := function(p1, deg1, p2, deg2)
  return p1*ShiftPerm(p2,deg1,deg2);
end;;

CheckHexCandidate := function(qrec, thetaHom, tauHom, m, f)
  local thetaf,ymf,tauymf,tau2ymf,u,genA,genB;
  thetaf := Image(thetaHom,f);
  if AbstractProd([f,thetaf]) <> Identity(qrec.G) then return false; fi;
  ymf := AbstractProd([qrec.y^m,f]);
  tauymf := Image(tauHom,ymf);  tau2ymf := Image(tauHom,tauymf);
  if AbstractProd([tau2ymf,tauymf,ymf]) <> Identity(qrec.G) then return false; fi;
  u := 2*m+1;
  genA := qrec.x^u;
  genB := AbstractProd([f^-1,qrec.y^u,f]);
  return Size(Group(genA,genB))=Size(qrec.G);
end;;

LiftCheckExact := function(fineQrec, thetaFine, tauFine, homFineCoarse, kerElts,
                           coarseOrd, fineOrd, m, f)
  local f0,mCands,checked,mF,k,fF;
  f0 := PreImagesRepresentative(homFineCoarse,f);
  mCands := Filtered([0..fineOrd-1],
    mm -> (mm mod coarseOrd = m mod coarseOrd) and Gcd(2*mm+1,fineOrd)=1);
  checked := 0;
  for mF in mCands do
    for k in kerElts do
      fF := f0*k;  checked := checked+1;
      if CheckHexCandidate(fineQrec,thetaFine,tauFine,mF,fF) then
        return rec(found:=true, checked:=checked, m_candidates:=Length(mCands),
                   witness:=rec(m:=mF,f:=fF));
      fi;
    od;
  od;
  return rec(found:=false, checked:=checked, m_candidates:=Length(mCands),witness:=fail);
end;;

MakeThetaTau := function(qrec)
  local z,th,ta;
  z := AbstractProd([qrec.x,qrec.y])^-1;
  th := GroupHomomorphismByImages(qrec.G,qrec.G,[qrec.x,qrec.y],[qrec.y,qrec.x]);
  ta := GroupHomomorphismByImages(qrec.G,qrec.G,[qrec.x,qrec.y],[qrec.y,z]);
  if th=fail or ta=fail then Error("theta/tau map missing"); fi;
  return [th,ta];
end;;

Print("D972_PHASE2_PRODUCER\n");
WriteCheckpoint("building_windows",0,0,0);

g9 := MakeGn(9);;  g27 := MakeGn(27);;  g36 := MakeGn(36);;  g108 := MakeGn(108);;
if Size(g9.G)<>2916 or Size(g27.G)<>78732 or Size(g36.G)<>23328 or Size(g108.G)<>629856 then
  Error("canonical dihedral window size mismatch");
fi;

# Machine receipt for K^(27) cap K^(36) = K^(108).
X2736 := DirectSumPerm(g27.x,81,g36.x,108);;
Y2736 := DirectSumPerm(g27.y,81,g36.y,108);;
G2736 := Group(X2736,Y2736);;
hom108to2736 := GroupHomomorphismByImages(g108.G,G2736,[g108.x,g108.y],[X2736,Y2736]);;
meetWellDefined := hom108to2736<>fail;;
meetImageSize := 0;;  meetKernelSize := -1;;
if meetWellDefined then
  meetImageSize := Size(Image(hom108to2736));
  meetKernelSize := Size(Kernel(hom108to2736));
fi;
meetExact := meetWellDefined and meetImageSize=Size(G2736) and meetKernelSize=1
             and Size(G2736)=Size(g108.G);;
if not meetExact then Error("K27/K36 cumulative meet receipt failed"); fi;

CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);;  Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;  Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm*Tperm^-1;;  Xperm := wPerm^2;;  Yperm := Sperm^-1*Xperm*Sperm;;
Pgrp := Group(Xperm,Yperm);;
if Size(Pgrp)<>504 then Error("N_S4 window size mismatch"); fi;

XM := DirectSumPerm(g9.x,27,Xperm,9);;  YM := DirectSumPerm(g9.y,27,Yperm,9);;
GM := Group(XM,YM);;  Mord := Lcm(Order(XM),Order(YM));;
X1 := DirectSumPerm(g27.x,81,Xperm,9);;  Y1 := DirectSumPerm(g27.y,81,Yperm,9);;
G1 := Group(X1,Y1);;  L1ord := Lcm(Order(X1),Order(Y1));;
X2 := DirectSumPerm(g108.x,324,Xperm,9);;  Y2 := DirectSumPerm(g108.y,324,Yperm,9);;
G2 := Group(X2,Y2);;  L2ord := Lcm(Order(X2),Order(Y2));;

sizeM := Size(GM);;  sizeL1 := Size(G1);;  sizeL2 := Size(G2);;
if sizeM<>1469664 or Mord<>18 or L1ord<>54 or L2ord<>108 then
  Error("roof scale/order mismatch");
fi;

h1M := GroupHomomorphismByImages(G1,GM,[X1,Y1],[XM,YM]);;
h21 := GroupHomomorphismByImages(G2,G1,[X2,Y2],[X1,Y1]);;
h2M := GroupHomomorphismByImages(G2,GM,[X2,Y2],[XM,YM]);;
if h1M=fail or h21=fail or h2M=fail then Error("natural reduction map missing"); fi;
h1MSurj := Size(Image(h1M))=sizeM;;
h21Surj := Size(Image(h21))=sizeL1;;
h2MSurj := Size(Image(h2M))=sizeM;;
factorizationOnGenerators := Image(h1M,Image(h21,X2))=Image(h2M,X2)
  and Image(h1M,Image(h21,Y2))=Image(h2M,Y2);;
if not (h1MSurj and h21Surj and h2MSurj and factorizationOnGenerators) then
  Error("reduction/factorization receipt failed");
fi;

ker1 := Kernel(h1M);;  ker21 := Kernel(h21);;  ker2M := Kernel(h2M);;
ker1Elts := Elements(ker1);;  ker21Elts := Elements(ker21);;  ker2MElts := Elements(ker2M);;

D1 := DerivedSubgroup(G1);;  DM := DerivedSubgroup(GM);;  D2 := DerivedSubgroup(G2);;
d1FullPreimage := Size(Intersection(ker1,D1))=Size(ker1)
  and Size(D1)=Size(ker1)*Size(DM);;
d2FullPreimage := Size(Intersection(ker21,D2))=Size(ker21)
  and Size(D2)=Size(ker21)*Size(D1);;
d2MFullPreimage := Size(Intersection(ker2M,D2))=Size(ker2M)
  and Size(D2)=Size(ker2M)*Size(DM);;
if not (d1FullPreimage and d2FullPreimage and d2MFullPreimage) then
  Error("derived preimage receipt failed");
fi;

WriteCheckpoint("enumerating_base",0,0,0);
resM := ScanRoofHexagon(rec(x:=XM,y:=YM,G:=GM),CharmingSetOf(Mord));;
if resM.shadow_total<>972 then Error("base shadow count mismatch"); fi;

tt1 := MakeThetaTau(rec(x:=X1,y:=Y1,G:=G1));;
tt2 := MakeThetaTau(rec(x:=X2,y:=Y2,G:=G2));;
q1 := rec(x:=X1,y:=Y1,G:=G1);;  q2 := rec(x:=X2,y:=Y2,G:=G2);;

details := [];;  depth1Raw := 0;;  depth2Raw := 0;;  processed := 0;;
badReductionCount := 0;;
tLift0 := GAPLIB_WallElapsedMs();;
for sh in resM.shadows do
  processed := processed+1;
  lr1 := LiftCheckExact(q1,tt1[1],tt1[2],h1M,ker1Elts,Mord,L1ord,sh.m,sh.f);
  found1 := lr1.found;  found2 := false;  checked2 := 0;  mCands2 := 0;
  if found1 then
    depth1Raw := depth1Raw+1;
    if lr1.witness.m mod Mord<>sh.m or Image(h1M,lr1.witness.f)<>sh.f then
      badReductionCount := badReductionCount+1;
    fi;
  fi;
  # Search all L2 preimages of the M-shadow directly.  Testing just one
  # chosen L1 witness would not be an existence-equivalent procedure.
  lr2 := LiftCheckExact(q2,tt2[1],tt2[2],h2M,ker2MElts,Mord,L2ord,sh.m,sh.f);
  found2 := lr2.found;  checked2 := lr2.checked;  mCands2 := lr2.m_candidates;
  if found2 then
    if not found1 or lr2.witness.m mod Mord<>sh.m or Image(h2M,lr2.witness.f)<>sh.f then
      badReductionCount := badReductionCount+1;
    else
      depth2Raw := depth2Raw+1;
    fi;
  fi;
  Add(details,rec(idx:=processed,m:=sh.m,d1:=found1,c1:=lr1.checked,n1:=lr1.m_candidates,
                  d2:=found2,c2:=checked2,n2:=mCands2));
  if processed mod 100=0 then
    WriteCheckpoint("lifting",processed,depth1Raw,depth2Raw);
    Print("progress ",processed,"/972 raw ",depth1Raw," ",depth2Raw,"\n");
  fi;
od;
tLift1 := GAPLIB_WallElapsedMs();;

if badReductionCount<>0 then Error("a stored lift violates exact (3.60) reduction"); fi;
depth1Exact := depth1Raw=resM.shadow_total;;
depth2Exact := depth2Raw=resM.shadow_total;;

JDetail := function(r)
  return Concatenation("{\"idx\":",String(r.idx),",\"m\":",String(r.m),
    ",\"depth1_found\":",JB(r.d1),",\"depth1_checked\":",String(r.c1),
    ",\"depth1_m_candidates\":",String(r.n1),
    ",\"depth2_found\":",JB(r.d2),",\"depth2_checked\":",String(r.c2),
    ",\"depth2_m_candidates\":",String(r.n2),"}");
end;;

t1Global := GAPLIB_WallElapsedMs();;
cert := Concatenation(
  "{\"schema\":\"d972_phase2/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/d972_phase2_v1.g\"}",
  ",\"coordinate_rule\":{\"reference\":\"2401 (3.60)\",\"m_reduction\":\"m mod H_ord\",\"legacy_half_modulus_used\":false}",
  ",\"cofinal_prefix\":{\"depth1\":\"K27_cap_NS4\",\"enumerand2\":\"K36_cap_NS4\",\"depth2_cumulative\":\"K108_cap_NS4\"}",
  ",\"meet_receipt\":{\"g2736_size\":",String(Size(G2736)),
    ",\"g108_size\":",String(Size(g108.G)),",\"hom_well_defined\":",JB(meetWellDefined),
    ",\"hom_image_size\":",String(meetImageSize),",\"hom_kernel_size\":",String(meetKernelSize),
    ",\"exact\":",JB(meetExact),"}",
  ",\"windows\":{\"pb3_over_m\":",String(sizeM),",\"m_ord\":",String(Mord),
    ",\"pb3_over_l1\":",String(sizeL1),",\"l1_ord\":",String(L1ord),
    ",\"pb3_over_l2\":",String(sizeL2),",\"l2_ord\":",String(L2ord),"}",
  ",\"reductions\":{\"l1_to_m_surjective\":",JB(h1MSurj),
    ",\"l2_to_l1_surjective\":",JB(h21Surj),",\"l2_to_m_surjective\":",JB(h2MSurj),
    ",\"factorization_on_marked_generators\":",JB(factorizationOnGenerators),
    ",\"kernel_l1_to_m\":",String(Size(ker1)),",\"kernel_l2_to_l1\":",String(Size(ker21)),
    ",\"kernel_l2_to_m\":",String(Size(ker2M)),
    ",\"derived_full_preimage_l1\":",JB(d1FullPreimage),
    ",\"derived_full_preimage_l2_to_l1\":",JB(d2FullPreimage),
    ",\"derived_full_preimage_l2_to_m\":",JB(d2MFullPreimage),"}",
  ",\"base_shadow_total\":",String(resM.shadow_total),
  ",\"depths\":[{\"depth\":1,\"raw_image_size\":",String(depth1Raw),
    ",\"exact_by_all_base_elements_witnessed\":",JB(depth1Exact),
    "},{\"depth\":2,\"raw_image_size\":",String(depth2Raw),
    ",\"exact_by_all_base_elements_witnessed\":",JB(depth2Exact),"}]",
  ",\"bad_exact_reduction_count\":",String(badReductionCount),
  ",\"per_base_shadow\":[",JoinC(List(details,JDetail),","),"]",
  ",\"elapsed_ms\":{\"lifting\":",String(tLift1-tLift0),",\"total\":",String(t1Global-t0Global),"}",
  ",\"u_touched\":false,\"c_touched\":false,\"sealed_k5_touched\":false,\"prereg_quantities_untouched\":true",
  ",\"interpretation\":\"raw finite-depth values only\"}"
);;

outPath := "search/certs/d972_phase2_v1_20260813.json";;
WriteFile(outPath,cert);;
WriteFile(checkpointPath,Concatenation(
  "{\"schema\":\"d972_phase2_checkpoint/v1\",\"stage\":\"complete\",\"processed\":972",
  ",\"depth1_raw\":",String(depth1Raw),",\"depth2_raw\":",String(depth2Raw),
  ",\"elapsed_ms\":",String(t1Global-t0Global),
  ",\"complete\":true,\"u_touched\":false,\"c_touched\":false}"
));
Print("raw_image_sizes ",depth1Raw," ",depth2Raw,"\n");
Print("D972_PHASE2_DONE\n");
QUIT;
