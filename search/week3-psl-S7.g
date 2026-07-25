# week3-psl-S7.g -- PSL window S7: PSL(2,11), case B (outer), Ghat=PGL(2,11), k=6 (e=12, 3|k), 3960 pts.

SizeScreen([4096, 0]);;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

q := 11;;
Smat := MakeMat(q, 1,0,0,10);;
Tmat := MakeMat(q, 4,1,1,6);;
Sperm := MatToPerm(q, Smat);;
Tperm := MatToPerm(q, Tmat);;

t0 := Runtime();;
pglElts11 := BuildPGLElements(q);;
t1 := Runtime();;
Print("PGL(2,11) enumerated: ", Length(pglElts11), " elements (expect 1320), time_ms=", t1-t0, "\n");

autElementToStr := function(M) return MatToStr(M); end;;

detS := DetMat2(Smat);;
sIsInner := IsSquareInGF(q, detS);;
Print("[", PF(not sIsInner), "] PU-F5: det(S)=", detS, " is_square=", sIsInner, " (expect outer=true, i.e. is_square=false, for S7)\n");

cfg := rec(
  id := "S7",
  ambientGroupName := "PGL(2,11)", caseLabel := "B_outer", objectCount := 2, autOrbitIndex := 1,
  Sperm := Sperm, Tperm := Tperm,
  SmatStr := MatToStr(Smat), TmatStr := MatToStr(Tmat),
  detSJson := JB(sIsInner),
  autElements := pglElts11, autElementToStr := autElementToStr, autSizeExp := 1320,
  ghatSizeExp := 1320, gSizeExp := 660, eOrdExp := 12, kOrdExp := 6, b3PointsExp := 3960,
  charmingSetExp := [0,2,3,5], exactOrderExp := 12
);;

ok := RunPSLWindow(cfg);;
if not ok then Print("[HALT] S7 did not complete.\n"); fi;
QUIT;
