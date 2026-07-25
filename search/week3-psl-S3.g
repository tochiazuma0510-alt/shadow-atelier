# week3-psl-S3.g -- PSL window S3: PSL(2,8), case A, k=e=7, 3024 B3 points.
# Aut(Ghat) = PGammaL(2,8) (order 1512 = PGL(2,8) x Frobenius, order-3 field automorphism).
# PU-F5 (inner/outer via det square) is vacuous for q=8 (PSL=PGL, no such distinction) per spec.

SizeScreen([4096, 0]);;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

CheckGF8();;

Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,2,4,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;

t0 := Runtime();;
pglElts8 := BuildPGLElementsGF8();;
frobPerm := FrobPermGF8();;
autGrp8 := Group(Concatenation(List(pglElts8, e -> e.perm), [frobPerm]));;
autElts8Full := Elements(autGrp8);;
t1 := Runtime();;
Print("PGammaL(2,8) enumerated: ", Length(autElts8Full), " elements (expect 1512), time_ms=", t1-t0, "\n");

# autElements interface: {mat, perm}. For PGammaL we do not track which (matrix,Frobenius-power)
# pair each element decomposes as; the permutation itself (cycle notation) is the explicit witness.
autElements := List(autElts8Full, p -> rec(mat:=p, perm:=p));;
autElementToStr := function(p) return String(p); end;;

cfg := rec(
  id := "S3",
  ambientGroupName := "PSL(2,8)", caseLabel := "A_split_inner", objectCount := 1, autOrbitIndex := 1,
  Sperm := Sperm, Tperm := Tperm,
  SmatStr := MatToStrGF8(Smat), TmatStr := MatToStrGF8(Tmat),
  detSJson := "\"not_applicable_q_even\"",
  autElements := autElements, autElementToStr := autElementToStr, autSizeExp := 1512,
  ghatSizeExp := 504, gSizeExp := 504, eOrdExp := 7, kOrdExp := 7, b3PointsExp := 3024,
  charmingSetExp := [0,1,2,4,5,6], exactOrderExp := 14
);;

ok := RunPSLWindow(cfg);;
if not ok then Print("[HALT] S3 did not complete.\n"); fi;
QUIT;
