# week3-psl-S4.g -- PSL window S4: PSL(2,8), case A, k=e=9 (3|k, composite), 3024 B3 points.

SizeScreen([4096, 0]);;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

CheckGF8();;

Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;

t0 := Runtime();;
pglElts8 := BuildPGLElementsGF8();;
frobPerm := FrobPermGF8();;
autGrp8 := Group(Concatenation(List(pglElts8, e -> e.perm), [frobPerm]));;
autElts8Full := Elements(autGrp8);;
t1 := Runtime();;
Print("PGammaL(2,8) enumerated: ", Length(autElts8Full), " elements (expect 1512), time_ms=", t1-t0, "\n");

autElements := List(autElts8Full, p -> rec(mat:=p, perm:=p));;
autElementToStr := function(p) return String(p); end;;

cfg := rec(
  id := "S4",
  ambientGroupName := "PSL(2,8)", caseLabel := "A_split_inner", objectCount := 1, autOrbitIndex := 1,
  Sperm := Sperm, Tperm := Tperm,
  SmatStr := MatToStrGF8(Smat), TmatStr := MatToStrGF8(Tmat),
  detSJson := "\"not_applicable_q_even\"",
  autElements := autElements, autElementToStr := autElementToStr, autSizeExp := 1512,
  ghatSizeExp := 504, gSizeExp := 504, eOrdExp := 9, kOrdExp := 9, b3PointsExp := 3024,
  charmingSetExp := [0,2,3,5,6,8], exactOrderExp := 18
);;

ok := RunPSLWindow(cfg);;
if not ok then Print("[HALT] S4 did not complete.\n"); fi;
QUIT;
