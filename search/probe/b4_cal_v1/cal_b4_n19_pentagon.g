## CAL-B4 N19 (Philadelphia subgroup) pentagon-count reproduction (C-1..C-4
## of docs/notes/b4_direct_adjudication_feasibility_v1_2.md sec6.2). NOT run
## locally (S3.5 shard B occupies the local GAP process at write time) --
## this is the GHA cal_b4 job's driver, first real test is the dispatch.
## Implements ONLY C-1 through C-4 (pentagon count over all 7776 elements).
## C-5 (hexagon lift, expect 36), C-6 (|GT|/|GT-heart| = 72/12), C-7 (N34),
## C-8 (Package GT cross-check), C-9/C-10 (tilde-N_core / Dtilde) are NOT
## implemented in this pass -- explicitly deferred, not silently dropped.
##
## Generator data: dolgushev-2008.00066 Table 1 row i=19 / (4.3), transcribed
## in docs/notes/b4_original_gtshadows_extraction_v1.md line 224 (page-image
## verified). psi: PB4 -> S9, kernel N19, |PB4:N19|=216, |F2:N_F2|=7776.
## (2.20) expansion (b4_direct_adjudication_feasibility_v1_2.md sec3.2.2,
## line ~140): f(x23,x34)*f(x12x13,x24x34)*f(x12,x23) = f(x12,x23x24)*f(x13x23,x34)
## This form uses ONLY the 6 PB4 generators X12,X13,X14,X23,X24,X34 (no K(0,5)
## sphere relations needed for this raw pentagon predicate).
Read("search/gaplib_common.g");
Read("search/probe/wac_v1/gap_output_prelude.g");

## --- stage1-style PB4 construction (reused pattern) ---
F := FreeGroup("s1","s2","s3");;
s1 := F.1;; s2 := F.2;; s3 := F.3;;
rels := [ s1*s3*s1^-1*s3^-1,
          s1*s2*s1*(s2*s1*s2)^-1,
          s2*s3*s2*(s3*s2*s3)^-1 ];;
B4 := F / rels;;
b1 := B4.1;; b2 := B4.2;; b3 := B4.3;;

X12 := b1^2;;  X23 := b2^2;;  X34 := b3^2;;
X13 := b2*b1^2*b2^-1;;  X24 := b3*b2^2*b3^-1;;  X14 := b3*X13*b3^-1;;
gensPB4 := [X12,X13,X14,X23,X24,X34];;   ## FIXED order, matches stage1

PB4sub := Subgroup(B4, gensPB4);;
idx24 := Index(B4, PB4sub);;
Print("[B4:PB4] = ", idx24, " (expect 24)\n");

iso := IsomorphismFpGroupByGenerators(PB4sub, gensPB4);;
PB4fp := Image(iso);;
gPB4 := GeneratorsOfGroup(PB4fp);;
gX12 := gPB4[1];; gX13 := gPB4[2];; gX14 := gPB4[3];;
gX23 := gPB4[4];; gX24 := gPB4[5];; gX34 := gPB4[6];;
Print("PB4fp built, ", Length(gPB4), " generators (expect 6, order X12,X13,X14,X23,X24,X34)\n");

## --- psi: PB4fp -> S9, N19 = ker(psi) ---
## (4.3), page-image transcription (b4_original_gtshadows_extraction_v1.md L224):
g12 := (1,3,2)(4,6,5);;
g23 := (1,4,9)(2,7,6);;
g13 := (1,7,5)(3,6,9);;
g14 := (2,6,7)(3,8,5);;
g24 := (1,8,6)(3,4,7);;
g34 := (1,2,3)(7,9,8);;
S9img := [g12, g13, g14, g23, g24, g34];;   ## SAME order as gensPB4

psi := GroupHomomorphismByImages(PB4fp, Group(S9img), gPB4, S9img);;
Print("psi: PB4fp -> S9 well-defined (fail = generator data / presentation mismatch)? ", psi <> fail, "\n");
if psi = fail then
  Print("STOP -- psi ill-defined, N19 construction cannot proceed as specified\n");
  QUIT;
fi;

R19 := Image(psi);;
Print("|Image(psi)| = ", Size(R19), " (expect 216 = |PB4:N19|)\n");
N19 := Kernel(psi);;
Print("|PB4fp : N19| = ", Index(PB4fp, N19), " (expect 216, sanity vs Size(Image))\n");

## --- F2 embedding: F2sub := <X12,X23> inside PB4fp ---
F2sub := Subgroup(PB4fp, [gX12, gX23]);;
N19_F2 := Intersection(N19, F2sub);;
hmF2 := NaturalHomomorphismByNormalSubgroup(F2sub, N19_F2);;
P19 := Image(hmF2);;
Print("|F2sub : N19_F2| = |P19| = ", Size(P19), " (expect 7776)\n");

xP := ImageElm(hmF2, gX12);;
yP := ImageElm(hmF2, gX23);;

## --- coface maps P19 -> R19 (via psi's images of the 6 PB4 generators) ---
psiX12 := ImageElm(psi, gX12);;  psiX13 := ImageElm(psi, gX13);;
psiX14 := ImageElm(psi, gX14);;  psiX23 := ImageElm(psi, gX23);;
psiX24 := ImageElm(psi, gX24);;  psiX34 := ImageElm(psi, gX34);;

BuildCoface := function(label, ximg, yimg)
  local hom;
  hom := GroupHomomorphismByImages(P19, R19, [xP,yP], [ximg,yimg]);;
  Print("coface ", label, ": well-defined? ", hom <> fail, "\n");
  return hom;;
end;;

phi123    := BuildCoface("phi_123 (x12,x23)",          psiX12,          psiX23);;
phi234    := BuildCoface("phi_234 (x23,x34)",          psiX23,          psiX34);;
phi_1_23_4:= BuildCoface("phi_1,23,4 (x12x13,x24x34)", psiX12*psiX13,   psiX24*psiX34);;
phi_1_2_34:= BuildCoface("phi_1,2,34 (x12,x23x24)",    psiX12,          psiX23*psiX24);;
phi_12_3_4:= BuildCoface("phi_12,3,4 (x13x23,x34)",    psiX13*psiX23,   psiX34);;

if phi123=fail or phi234=fail or phi_1_23_4=fail or phi_1_2_34=fail or phi_12_3_4=fail then
  Print("STOP -- a coface map is ill-defined, cannot evaluate (2.20)\n");
  QUIT;
fi;

## --- evaluate (2.20) over ALL 7776 elements of P19 (C-4) ---
elemsP19 := AsList(P19);;
Print("Enumerated |P19| = ", Length(elemsP19), " elements\n");

t0 := GAPLIB_WallElapsedMs();
passCount := 0;;
passList := [];;
for f in elemsP19 do
  lhs := ImageElm(phi234,f) * ImageElm(phi_1_23_4,f) * ImageElm(phi123,f);;
  rhs := ImageElm(phi_1_2_34,f) * ImageElm(phi_12_3_4,f);;
  if lhs = rhs then
    passCount := passCount + 1;;
    Add(passList, f);;
  fi;
od;
t1 := GAPLIB_WallElapsedMs();
Print("\n(2.20) pentagon-pass count over all 7776 elements of P19 = ", passCount,
      "  (expect 216, C-4)  elapsed_ms=", t1-t0, "\n");

if passCount = 216 then
  Print("C-4 PASS: pentagon count matches paper Table 1 / CAL-B4 expected value.\n");
else
  Print("C-4 MISMATCH -- STOP, do not trust downstream B4 numbers until resolved.\n");
fi;

Print("ALL_DONE\n");
