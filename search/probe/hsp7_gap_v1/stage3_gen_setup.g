## search/probe/hsp7_gap_v1/stage3_gen_setup.g
## Generate the ANUPQ batch setup files for P (free F2) and Q (K05fp),
## both class<=4, exponent 7, prime 7 (NW(7) window, e=1).
## ANUPQ's interactive iostream is broken on this Windows/Cygwin GAP build
## (Process/InputOutputLocalProcess pipe buffering: see express report to
## commander 2026-08-04). Route: SetupFile option (native ANUPQ feature,
## documented chap6.txt "SetupFile") writes the *same* command sequence
## ANUPQ would send interactively, to a file; we then run pq.exe on that
## file via a one-way stdin redirect (batch, no pipe) and read PQ_OUTPUT
## back with Read() -- this reuses ANUPQ's own command generation (no
## hand-rolled pq protocol) and its own GAP-format output reader.
LoadPackage("anupq");;
SetInfoLevel(InfoANUPQ, 4);

## --- P side: free group F2, class<=4, exponent 7 ---
F2 := FreeGroup("x","y");;
Print("=== P setup ===\n");
Pq(F2 : Prime := 7, ClassBound := 4, Exponent := 7,
        SetupFile := "search/probe/hsp7_gap_v1/pq_setup_P.txt" );;

## --- Q side: K05fp, class<=4, exponent 7 ---
F := FreeGroup("s1","s2","s3");;
s1 := F.1;; s2 := F.2;; s3 := F.3;;
rels := [ s1*s3*s1^-1*s3^-1,
          s1*s2*s1*(s2*s1*s2)^-1,
          s2*s3*s2*(s3*s2*s3)^-1 ];;
B4 := F / rels;;
b1 := B4.1;; b2 := B4.2;; b3 := B4.3;;
X12 := b1^2;;  X23 := b2^2;;  X34 := b3^2;;
X13 := b2*b1^2*b2^-1;;  X24 := b3*b2^2*b3^-1;;  X14 := b3*X13*b3^-1;;
gensPB4 := [X12,X13,X14,X23,X24,X34];;
PB4sub := Subgroup(B4, gensPB4);;
iso := IsomorphismFpGroupByGenerators(PB4sub, gensPB4);;
PB4fp := Image(iso);;
Delta2 := (b1*b2*b3)^4;;
Delta2img := ImageElm(iso, Delta2);;
FPB4 := FreeGroupOfFpGroup(PB4fp);;
relsPB4 := RelatorsOfFpGroup(PB4fp);;
Delta2word := UnderlyingElement(Delta2img);;
K05fp := FPB4 / Concatenation(relsPB4, [Delta2word]);;

Print("=== Q setup ===\n");
Pq(K05fp : Prime := 7, ClassBound := 4, Exponent := 7,
           SetupFile := "search/probe/hsp7_gap_v1/pq_setup_Q.txt" );;

Print("SETUP_FILES_WRITTEN\n");
QUIT;
