# week3-psl-S5.g -- PSL window S5: PSL(2,11), case A, k=e=11, 3960 B3 points.

SizeScreen([4096, 0]);;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

q := 11;;
Smat := MakeMat(q, 1,1,1,10);;
Tmat := MakeMat(q, 9,1,8,1);;
Sperm := MatToPerm(q, Smat);;
Tperm := MatToPerm(q, Tmat);;

t0 := Runtime();;
pglElts11 := BuildPGLElements(q);;
t1 := Runtime();;
Print("PGL(2,11) enumerated: ", Length(pglElts11), " elements (expect 1320), time_ms=", t1-t0, "\n");

autElementToStr := function(M) return MatToStr(M); end;;

detS := DetMat2(Smat);;
sIsInner := IsSquareInGF(q, detS);;
Print("[", PF(sIsInner), "] PU-F5: det(S)=", detS, " is_square=", sIsInner, " (expect inner=true for S5)\n");

cfg := rec(
  id := "S5",
  ambientGroupName := "PSL(2,11)", caseLabel := "A_split_inner", objectCount := 1, autOrbitIndex := 1,
  Sperm := Sperm, Tperm := Tperm,
  SmatStr := MatToStr(Smat), TmatStr := MatToStr(Tmat),
  detSJson := JB(sIsInner),
  autElements := pglElts11, autElementToStr := autElementToStr, autSizeExp := 1320,
  ghatSizeExp := 660, gSizeExp := 660, eOrdExp := 11, kOrdExp := 11, b3PointsExp := 3960,
  charmingSetExp := [0,1,2,3,4,6,7,8,9,10], exactOrderExp := 22
);;

ok := RunPSLWindow(cfg);;
if not ok then Print("[HALT] S5 did not complete.\n"); fi;
QUIT;
