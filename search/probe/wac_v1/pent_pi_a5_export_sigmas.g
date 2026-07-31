#############################################################################
## search/probe/wac_v1/pent_pi_a5_export_sigmas.g
## Third-party judge run (Dolgushev "Package GT"): export S1,S2,S3 (sigma1,
## sigma2, sigma3 images of the pi-lift, sigma3 |-> sigma1) as explicit
## image lists over domain [1..8], so they can be transferred to Python
## and rebuilt as sympy Permutation objects, then handed to PaB.py's OWN
## relB4/restr_PB4 to derive x12..x34 -- this avoids any hand-conversion
## of GAP's action convention vs sympy's: we only transfer the 3 generator
## images, and let the third-party package's own (already-tested) formula
## restr_PB4 compute everything else in ITS convention.
##
## STEP1/STEP2 logic is byte-identical to search/probe/wac_v1/pent_pi_a5.g
## (the calibrated PENT-PI construction, ruling 248) -- duplicated here
## (not edited in place) so the original probe/cert stays untouched.
#############################################################################
SetPrintFormattingStatus("*stdout*", false);;

X5 := (1,3,2,4,5);;
Y5 := (1,3,4,5,2);;
A5 := AlternatingGroup(5);;

found := [];;
for s in Elements(A5) do
  if s <> () and s^2 = () then
    for t in Elements(A5) do
      if t <> () and t^3 = () then
        a := s * (6,7);
        b := t * (6,7,8);
        s1 := b^-1 * a;
        s2 := a * b^2;
        if s1^2 = X5 and s2^2 = Y5 then
          if Size(Group(s, t)) = 60 then
            Add(found, rec(s := s, t := t, a := a, b := b, s1 := s1, s2 := s2));
          fi;
        fi;
      fi;
    od;
  fi;
od;;

if Length(found) = 0 then
  Error("PENT-PI EXPORT STOP: no (s,t) realizes the A1.v2 marking");
fi;
W := found[1];;

EWIN := Group(W.a, W.b);;
if Size(EWIN) <> 360 then Error("PENT-PI EXPORT STOP: |EWIN| <> 360"); fi;

xbar := W.s1^2;;  ybar := W.s2^2;;
P5 := Group(xbar, ybar);;
if Size(P5) <> 60 then Error("PENT-PI EXPORT STOP: |<xbar,ybar>| <> 60"); fi;

S1 := W.s1;; S2 := W.s2;; S3 := W.s1;;   ## pi-lift: sigma3 |-> sigma1

if not (S1*S2*S1 = S2*S1*S2) then Error("PENT-PI EXPORT STOP: B4 rel 1"); fi;
if not (S2*S3*S2 = S3*S2*S3) then Error("PENT-PI EXPORT STOP: B4 rel 2"); fi;
if not (S1*S3 = S3*S1) then Error("PENT-PI EXPORT STOP: B4 rel 3"); fi;

## Domain check: what points do S1,S2,S3 actually move? Use domain [1..8]
## uniformly (a,b were built on points {1,...,8}: A5 acts on 1..5, tails
## on 6,7,8).
dom := [1 .. 8];;

ImageList := function(p, d)
  local L, i;
  L := [];
  for i in d do Add(L, i^p); od;
  return L;
end;;

Print("DOMAIN_SIZE 8\n");
Print("S1_IMAGES ", ImageList(S1, dom), "\n");
Print("S2_IMAGES ", ImageList(S2, dom), "\n");
Print("S3_IMAGES ", ImageList(S3, dom), "\n");
Print("EXPORT_DONE\n");
QUIT;
