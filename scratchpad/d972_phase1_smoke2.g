## scratchpad/d972_phase1_smoke2.g -- continue feasibility check: Ker(homKtoM) cap D(GK),
## PreImagesRepresentative timing, and a single-shadow lift-check timing test.
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

g9 := MakeGn(9);; g27 := MakeGn(27);;
CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);; Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);; Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm * Tperm^-1;; Xperm := wPerm^2;; Yperm := Sperm^-1 * Xperm * Sperm;;
Pgrp := Group(Xperm, Yperm);;

XM := DirectSumPerm(g9.x, 27, Xperm, 9);; YM := DirectSumPerm(g9.y, 27, Yperm, 9);;
GM := Group(XM, YM);;
XK := DirectSumPerm(g27.x, 81, Xperm, 9);; YK := DirectSumPerm(g27.y, 81, Yperm, 9);;
GK := Group(XK, YK);;
homKtoM := GroupHomomorphismByImages(GK, GM, [XK,YK], [XM,YM]);;
KerHom := Kernel(homKtoM);;
DGK := DerivedSubgroup(GK);;
DGM := DerivedSubgroup(GM);;
Print("|D(GK)|=", Size(DGK), " |D(GM)|=", Size(DGM), "\n");

t1 := GAPLIB_WallElapsedMs();;
KerCapD := Intersection(KerHom, DGK);;
t2 := GAPLIB_WallElapsedMs();;
Print("|Ker(homKtoM) cap D(GK)| = ", Size(KerCapD), "  elapsed_ms=", t2-t1, "\n");
KerCapDElts := Elements(KerCapD);;
Print("elements listable, count=", Length(KerCapDElts), "\n");

## check: is homKtoM(D(GK)) = D(GM)?  (should be true by surjective-hom-preserves-derived fact)
t3 := GAPLIB_WallElapsedMs();;
imDGK := Image(homKtoM, DGK);;
t4 := GAPLIB_WallElapsedMs();;
Print("Image(homKtoM, D(GK)) = D(GM) ? size match=", Size(imDGK)=Size(DGM), " set_equal=", imDGK=DGM, "  elapsed_ms=", t4-t3, "\n");

## pick one nontrivial f in D(GM), test PreImagesRepresentative + membership loop timing
felts := Elements(DGM);;  # DGM order?
Print("|D(GM)| = ", Length(felts), "\n");
fTest := felts[2];;
t5 := GAPLIB_WallElapsedMs();;
f0 := PreImagesRepresentative(homKtoM, fTest);;
t6 := GAPLIB_WallElapsedMs();;
Print("PreImagesRepresentative elapsed_ms=", t6-t5, "  f0 in DGK: ", f0 in DGK, "\n");

## enumerate f0*k for k in KerCapDElts, check which land in DGK (should be all, by construction)
t7 := GAPLIB_WallElapsedMs();;
cnt := 0;;
for k in Elements(KerHom) do
  if f0*k in DGK then cnt := cnt+1; fi;
od;
t8 := GAPLIB_WallElapsedMs();;
Print("count of f0*k in D(GK) over full Ker(homKtoM) (", Size(KerHom), " elts) = ", cnt, "  elapsed_ms=", t8-t7, "\n");

Print("\ntotal elapsed_ms=", GAPLIB_WallElapsedMs()-t0, "\n");
QUIT;
