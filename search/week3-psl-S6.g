# week3-psl-S6.g -- PSL window S6: PSL(2,11), case B (outer), Ghat=PGL(2,11), k=5 (e=10), 3960 pts.

SizeScreen([4096, 0]);;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

q := 11;;
Smat := MakeMat(q, 1,0,0,10);;
Tmat := MakeMat(q, 3,1,9,7);;
Sperm := MatToPerm(q, Smat);;
Tperm := MatToPerm(q, Tmat);;

t0 := Runtime();;
pglElts11 := BuildPGLElements(q);;
t1 := Runtime();;
Print("PGL(2,11) enumerated: ", Length(pglElts11), " elements (expect 1320), time_ms=", t1-t0, "\n");

autElementToStr := function(M) return MatToStr(M); end;;

detS := DetMat2(Smat);;
sIsInner := IsSquareInGF(q, detS);;
Print("[", PF(not sIsInner), "] PU-F5: det(S)=", detS, " is_square=", sIsInner, " (expect outer=true, i.e. is_square=false, for S6)\n");

cfg := rec(
  id := "S6",
  ambientGroupName := "PGL(2,11)", caseLabel := "B_outer", objectCount := 2, autOrbitIndex := 1,
  Sperm := Sperm, Tperm := Tperm,
  SmatStr := MatToStr(Smat), TmatStr := MatToStr(Tmat),
  detSJson := JB(sIsInner),
  autElements := pglElts11, autElementToStr := autElementToStr, autSizeExp := 1320,
  ghatSizeExp := 1320, gSizeExp := 660, eOrdExp := 10, kOrdExp := 5, b3PointsExp := 3960,
  charmingSetExp := [0,1,3,4], exactOrderExp := 10
);;

ok := RunPSLWindow(cfg);;
if not ok then Print("[HALT] S6 did not complete.\n"); fi;
QUIT;
