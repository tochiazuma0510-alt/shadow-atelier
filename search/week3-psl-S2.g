# week3-psl-S2.g -- PSL window S2: PSL(2,7), case B (outer), Ghat=PGL(2,7), k=4 (e=8), 1008 pts.
# Aut(PGL(2,7)) = PGL(2,7) itself (complete for odd prime q) -- same element list as Ghat.

SizeScreen([4096, 0]);;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

q := 7;;
Smat := MakeMat(q, 1,0,0,6);;
Tmat := MakeMat(q, 1,1,4,5);;
Sperm := MatToPerm(q, Smat);;
Tperm := MatToPerm(q, Tmat);;

t0 := Runtime();;
pglElts7 := BuildPGLElements(q);;
t1 := Runtime();;
Print("PGL(2,7) enumerated: ", Length(pglElts7), " elements (expect 336), time_ms=", t1-t0, "\n");

autElementToStr := function(M) return MatToStr(M); end;;

detS := DetMat2(Smat);;
sIsInner := IsSquareInGF(q, detS);;
Print("[", PF(not sIsInner), "] PU-F5: det(S)=", detS, " is_square=", sIsInner, " (expect outer=true, i.e. is_square=false, for S2)\n");

cfg := rec(
  id := "S2",
  ambientGroupName := "PGL(2,7)", caseLabel := "B_outer", objectCount := 2, autOrbitIndex := 1,
  Sperm := Sperm, Tperm := Tperm,
  SmatStr := MatToStr(Smat), TmatStr := MatToStr(Tmat),
  detSJson := JB(sIsInner),
  autElements := pglElts7, autElementToStr := autElementToStr, autSizeExp := 336,
  ghatSizeExp := 336, gSizeExp := 168, eOrdExp := 8, kOrdExp := 4, b3PointsExp := 1008,
  charmingSetExp := [0,1,2,3], exactOrderExp := 8
);;

ok := RunPSLWindow(cfg);;
if not ok then Print("[HALT] S2 did not complete.\n"); fi;
QUIT;
