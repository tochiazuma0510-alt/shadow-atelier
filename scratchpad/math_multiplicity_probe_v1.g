#############################################################################
## math_multiplicity_probe_v1.g -- mathematician (Opus 5), 2026-08-29
## RULING GATE for "valid > F1' : anomaly or fibre multiplicity?"
##
## STRUCTURAL PREDICTION (to be tested):
##   u = 2m+1 defines a HOMOMORPHISM  GT(K) -> (Z/K_ord)^*  , (m,f) |-> u.
##   Hence the set of valid f over a FIXED m is either empty or a torsor under
##   Lam := { h : (0,h) is a shadow lying over the identity roof datum }.
##   ==> multiplicity is CONSTANT across every m that lifts, and >= 1 is normal.
##   ==> valid = (#m that lift) x (constant multiplicity).
##   ==> ANOMALY is NOT "valid > F1'" but (a) 0 < #{m that lift} < F1'  or
##       (b) NON-UNIFORM multiplicity across the m that lift.
##
## Predicate = the RULED (F2) quotient rule (裁定 1759/1761):
##   theta~: x->y, y->x, c->c ;  tau~: x->y, y->y^-1 x^-1 c, c->c
##   (i) p*theta~(p)=1   (ii) tau~^2(w) tau~(w) w = c^m , w = JY^m * p  (y^m LEFT)
##   (iii) <JX^u, p^-1 JY^u p> = G
## Seed word reading = REVERSED codes (裁定 1761: word_eval_order = prepend).
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;
if LoadPackage("lins") <> true then Error("MM: LINS load failed"); fi;
MMSearch := LowIndexNormalSubgroupsSearch(DCP2B3, 100);;
MMNodes  := ComputedNormalSubgroups(MMSearch);;
Print("MM_LINS100 nodes=", Length(MMNodes), "\n");

MMEval := function(codes, gx, gy, id)
  local z, c;
  z := id;
  for c in Reversed(codes) do          ## REVERSED = prepend convention
    if   c =  1 then z := z*gx;
    elif c = -1 then z := z*gx^-1;
    elif c =  2 then z := z*gy;
    elif c = -2 then z := z*gy^-1; fi;
  od;
  return z;
end;;

Print("MM_HEADER  b3idx | seed | K_ord | F1'(#allowed m) | |fibre| | per-m valid counts | total valid\n");
MMScanned := 0;;
for MMNode in MMNodes do
  if Index(MMNode) = 1 then continue; fi;
  if MMScanned >= 30 then break; fi;
  MMq := DCP2BuildWindow(Grp(MMNode));;
  MMScanned := MMScanned + 1;;
  MMJC := DCP2DirectSumPerm(Identity(DCP2MBlock), DCP2MDegree, MMq.Cp_on_L, MMq.degL);;
  MMA  := Group(MMq.JX, MMq.JY, MMJC);;
  MMTh := GroupHomomorphismByImages(MMA, MMA, [MMq.JX,MMq.JY,MMJC],
            [MMq.JY, MMq.JX, MMJC]);;
  MMTa := GroupHomomorphismByImages(MMA, MMA, [MMq.JX,MMq.JY,MMJC],
            [MMq.JY, MMq.JY^-1*MMq.JX^-1*MMJC, MMJC]);;
  if MMTh = fail or MMTa = fail then
    Print("MM_AUTFAIL b3idx=", Index(MMNode), "\n"); continue; fi;
  MMD  := DerivedSubgroup(MMq.G);;
  MMHl := Elements(MMq.H);;
  MMms := List([0..(MMq.K_ord/MMq.M_ord)-1], t -> MMq.M_ord*t);;
  for MMSeed in DCP2Seeds do
    MMJF := MMEval(MMSeed.codes, MMq.JX, MMq.JY, Identity(MMq.G));;
    MMper := [];; MMtot := 0;;
    for MMm in List(MMms, t -> MMSeed.m_seed + t) do
      MMcnt := 0;;
      MMu := 2*MMm + 1;;
      if Gcd(MMu, MMq.K_ord) = 1 then
        for MMh in MMHl do
          MMp := MMJF * MMh;;
          if not (MMp in MMD) then continue; fi;
          if MMp * Image(MMTh, MMp) <> Identity(MMA) then continue; fi;
          MMw := MMq.JY^MMm * MMp;;
          if Image(MMTa, Image(MMTa, MMw)) * Image(MMTa, MMw) * MMw <> MMJC^MMm
            then continue; fi;
          if Size(Group(MMq.JX^MMu, MMp^-1 * MMq.JY^MMu * MMp)) <> Size(MMq.G)
            then continue; fi;
          MMcnt := MMcnt + 1;;
        od;
      fi;
      Add(MMper, MMcnt);; MMtot := MMtot + MMcnt;;
    od;
    if MMtot > 0 then
      Print("MM_ROW b3idx=", Index(MMNode), " seed=", MMSeed.name,
            " K_ord=", MMq.K_ord, " F1p=", Length(MMms),
            " fibre=", Length(MMHl),
            " per_m=", MMper, " total=", MMtot,
            " mult_set=", Set(Filtered(MMper, x -> x > 0)),
            " uniform=", Length(Set(Filtered(MMper, x -> x > 0))) <= 1,
            " lifting_m=", Number(MMper, x -> x > 0), "\n");
    fi;
  od;
od;
Print("MM_DONE scanned=", MMScanned, "\n");
QUIT;
