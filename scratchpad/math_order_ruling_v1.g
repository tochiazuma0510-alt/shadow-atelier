#############################################################################
## math_order_ruling_v1.g -- mathematician (Opus 5), 2026-08-29
## RULING GATE for the (3.11) product order.
##
## 2401.06870 Prop 3.4 states VERBATIM:
##    (3.10)  f theta(f) in N_{F2}
##    (3.11)  tau^2(y^m f) tau(y^m f) y^m f in N_{F2}
## and rewrites them as
##    (3.12)  f(x,y) f(y,x) in N_{F2}
##    (3.13)  x^m f(z,x) z^m f(y,z) y^m f in N_{F2},   z := y^{-1} x^{-1}
##
## (3.13) is an EXPLICIT WORD in x,y -- the product order is baked into the
## word, so evaluating that single word removes the product-order convention
## entirely.  The ONLY remaining convention is the word evaluator direction.
## This script therefore decides BOTH open questions at once on the roof M
## (where c's image is the identity, so word-level tau is legitimate).
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;   ## roof M: DCP2MX, DCP2MY, DCP2MBlock

MO := rec();;
MO.X := DCP2MX;; MO.Y := DCP2MY;; MO.G := DCP2MBlock;;
Print("MO_ROOF_ORDER ", Size(MO.G), "  degree ", LargestMovedPoint(MO.G), "\n");

## ---- word utilities on signed code lists (1=x, -1=x^-1, 2=y, -2=y^-1) ----
WInv  := function(w) return Reversed(List(w, c -> -c)); end;;
WCat  := function(ws) return Concatenation(ws); end;;
WPow  := function(w, n)
  local i, out;
  if n = 0 then return []; fi;
  out := [];
  if n > 0 then for i in [1..n] do Append(out, w); od;
  else for i in [1..-n] do Append(out, WInv(w)); od; fi;
  return out;
end;;
## substitute x -> A, y -> B in the code list C
WSub := function(C, A, B)
  local out, c;
  out := [];
  for c in C do
    if   c =  1 then Append(out, A);
    elif c = -1 then Append(out, WInv(A));
    elif c =  2 then Append(out, B);
    elif c = -2 then Append(out, WInv(B));
    else Error("bad code ", c); fi;
  od;
  return out;
end;;
## APPEND evaluation (standard homomorphism F2 -> G)
EvalAppend := function(w, gx, gy)
  local z, c;
  z := Identity(MO.G);
  for c in w do
    if   c =  1 then z := z*gx;
    elif c = -1 then z := z*gx^-1;
    elif c =  2 then z := z*gy;
    elif c = -2 then z := z*gy^-1;
    fi;
  od;
  return z;
end;;
## PREPEND evaluation (anti-homomorphism; = EvalAppend on the reversed word)
EvalPrepend := function(w, gx, gy) return EvalAppend(Reversed(w), gx, gy); end;;

## ---- the paper's words ----
WX := [1];; WY := [2];; WZ := [-2,-1];;      ## z = y^{-1} x^{-1}

Rel310 := function(F)                        ## f(x,y) f(y,x)
  return WCat([ WSub(F, WX, WY), WSub(F, WY, WX) ]);
end;;
Rel313 := function(F, m)                     ## x^m f(z,x) z^m f(y,z) y^m f
  return WCat([ WPow(WX,m), WSub(F, WZ, WX), WPow(WZ,m),
                WSub(F, WY, WZ), WPow(WY,m), WSub(F, WX, WY) ]);
end;;

## sanity: tau^2(y^m f) tau(y^m f) y^m f  built by WORD-LEVEL tau  must EQUAL Rel313
TauW := function(w)                          ## tau: x->y, y->z  (word level)
  return WSub(w, WY, WZ);
end;;
Rel311 := function(F, m)
  local w;
  w := WCat([ WPow(WY,m), WSub(F, WX, WY) ]);      ## y^m f
  return WCat([ TauW(TauW(w)), TauW(w), w ]);       ## tau^2(w) tau(w) w
end;;

Print("MO_IDENTITY_311_EQUALS_313 ",
  ForAll(DCP2Seeds, s -> ForAll([0,1,2,5],
    m -> EvalAppend(Rel311(s.codes,m),MO.X,MO.Y) = EvalAppend(Rel313(s.codes,m),MO.X,MO.Y))),
  "   (paper-internal cross-check of the order)\n");
## and the REVERSED product order, for contrast
Rel311rev := function(F, m)
  local w;
  w := WCat([ WPow(WY,m), WSub(F, WX, WY) ]);
  return WCat([ w, TauW(w), TauW(TauW(w)) ]);        ## w tau(w) tau^2(w)
end;;
Print("MO_REVERSED_ORDER_ALSO_EQUALS_313 ",
  ForAll(DCP2Seeds, s -> ForAll([0,1,2,5],
    m -> EvalAppend(Rel311rev(s.codes,m),MO.X,MO.Y) = EvalAppend(Rel313(s.codes,m),MO.X,MO.Y))),
  "\n\n");

## ---- the decisive measurement on the roof ----
Print("MO_ROOF  seed / f-reading / m : (3.10) holds ; (3.13) holds\n");
for MOs in DCP2Seeds do
  for MOrd in [ ["append", 1], ["reversed", 2] ] do
    for MOm in [0..17] do
      MOf := MOs.codes;;
      if MOrd[2] = 2 then MOf := Reversed(MOf); fi;
      MOa := EvalAppend(Rel310(MOf), MO.X, MO.Y) = Identity(MO.G);;
      MOb := EvalAppend(Rel313(MOf, MOm), MO.X, MO.Y) = Identity(MO.G);;
      MOfe := EvalAppend(MOf, MO.X, MO.Y);;
      MOu := 2*MOm + 1;;
      MOch := MOfe in DerivedSubgroup(MO.G);;
      MOco := Gcd(MOu, 18) = 1;;
      MOon := Size(Group(MO.X^MOu, MOfe^-1 * MO.Y^MOu * MOfe)) = Size(MO.G);;
      if MOa and MOb then
        Print("  MO_SHADOW seed=", MOs.name, " f_reading=", MOrd[1],
              " m=", MOm, "  (3.10)=true (3.13)=true",
              "  charming=", MOch, "  gcd(u,18)=1:", MOco,
              "  onto=", MOon,
              "  FULL=", MOa and MOb and MOch and MOco and MOon, "\n");
      fi;
    od;
  od;
od;
Print("MO_DONE\n");
QUIT;
