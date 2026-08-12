## scratchpad/d972_phase1_smoke.g -- feasibility smoke test for Phase 1 construction
## (K window, homKtoM, kernel size) BEFORE committing to the full driver.
## Not a cert-producing script. Throwaway.

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0 := GAPLIB_WallElapsedMs();;
PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

ShiftPerm := function(p, offset, size)
  local l, j;
  l := [1 .. offset+size];
  for j in [1 .. size] do l[offset+j] := offset + (j^p); od;
  return PermList(l);
end;;
DirectSumPerm := function(p1, deg1, p2, deg2)
  return p1 * ShiftPerm(p2, deg1, deg2);
end;;

Print("=== build K9, K27, N_S4 windows ===\n");
g9 := MakeGn(9);;
g27 := MakeGn(27);;

CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm * Tperm^-1;;
Xperm := wPerm^2;;
Yperm := Sperm^-1 * Xperm * Sperm;;
Pgrp := Group(Xperm, Yperm);;
Print("  |N_S4|=", Size(Pgrp), " ord=", Lcm(Order(Xperm),Order(Yperm)), "\n");

Print("=== build M := K9 cap N_S4 (verbatim Phase0 pattern) ===\n");
XM := DirectSumPerm(g9.x, 27, Xperm, 9);;
YM := DirectSumPerm(g9.y, 27, Yperm, 9);;
GM := Group(XM, YM);;
Print("  |M|=", Size(GM), " ord=", Lcm(Order(XM),Order(YM)), " (expect 1469664, 18)\n");

Print("=== build K := K27 cap N_S4 (same pattern) ===\n");
t1 := GAPLIB_WallElapsedMs();;
XK := DirectSumPerm(g27.x, 81, Xperm, 9);;
YK := DirectSumPerm(g27.y, 81, Yperm, 9);;
GK := Group(XK, YK);;
t2 := GAPLIB_WallElapsedMs();;
Print("  Group() construction elapsed_ms=", t2-t1, "\n");
Print("  |K|=", Size(GK), " ord=", Lcm(Order(XK),Order(YK)), " (expect 39696528, 54)  elapsed_ms=", GAPLIB_WallElapsedMs()-t2, "\n");

Print("=== homKtoM: GK -> GM ===\n");
t3 := GAPLIB_WallElapsedMs();;
homKtoM := GroupHomomorphismByImages(GK, GM, [XK,YK], [XM,YM]);;
t4 := GAPLIB_WallElapsedMs();;
Print("  well_defined=", homKtoM<>fail, "  elapsed_ms=", t4-t3, "\n");
if homKtoM <> fail then
  imOrd := Size(Image(homKtoM));;
  t5 := GAPLIB_WallElapsedMs();;
  Print("  |Image(homKtoM)|=", imOrd, " (expect |M|=1469664)  surjective=", imOrd=Size(GM), "  elapsed_ms=", t5-t4, "\n");
  KerHom := Kernel(homKtoM);;
  t6 := GAPLIB_WallElapsedMs();;
  Print("  |Kernel(homKtoM)|=", Size(KerHom), " (expect 27)  elapsed_ms=", t6-t5, "\n");
fi;

Print("=== DerivedSubgroup(GK) (no Elements()) ===\n");
t7 := GAPLIB_WallElapsedMs();;
DGK := DerivedSubgroup(GK);;
t8 := GAPLIB_WallElapsedMs();;
Print("  |D(GK)|=", Size(DGK), "  elapsed_ms=", t8-t7, "\n");

Print("\ntotal elapsed_ms=", GAPLIB_WallElapsedMs()-t0, "\n");
QUIT;
