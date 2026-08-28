#############################################################################
## math_multiplicity_probe_v2.g -- mathematician (Opus 5), 2026-08-29
## v1 showed: (a) multiplicity is ALWAYS uniform across lifting m, and
##            (b) many windows have a PROPER SUBSET of m lifting.
## (b) would fire the proposed ANOMALY condition on a large fraction of
## windows.  This probe tests the hypothesis that every such zero is a
## CHARMING failure (gcd(2m+1, K_ord) != 1), i.e. that the m was never
## admissible in the first place:
##      F1''  :=  #{ m in the residue class : gcd(2m+1, K_ord) = 1 }
##      claim :  #{m that lift}  ==  F1''      (exactly, every window)
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;
if LoadPackage("lins") <> true then Error("MN: LINS load failed"); fi;
MNNodes := ComputedNormalSubgroups(LowIndexNormalSubgroupsSearch(DCP2B3, 100));;

MNEval := function(codes, gx, gy, id)
  local z, c;
  z := id;
  for c in Reversed(codes) do
    if   c =  1 then z := z*gx; elif c = -1 then z := z*gx^-1;
    elif c =  2 then z := z*gy; elif c = -2 then z := z*gy^-1; fi;
  od;
  return z;
end;;

MNall := true;; MNrows := 0;; MNmults := [];;
for MNNode in MNNodes do
  if Index(MNNode) = 1 then continue; fi;
  if MNrows >= 60 then break; fi;
  MNq := DCP2BuildWindow(Grp(MNNode));;
  MNJC := DCP2DirectSumPerm(Identity(DCP2MBlock), DCP2MDegree, MNq.Cp_on_L, MNq.degL);;
  MNA  := Group(MNq.JX, MNq.JY, MNJC);;
  MNTh := GroupHomomorphismByImages(MNA,MNA,[MNq.JX,MNq.JY,MNJC],[MNq.JY,MNq.JX,MNJC]);;
  MNTa := GroupHomomorphismByImages(MNA,MNA,[MNq.JX,MNq.JY,MNJC],
            [MNq.JY, MNq.JY^-1*MNq.JX^-1*MNJC, MNJC]);;
  if MNTh = fail or MNTa = fail then continue; fi;
  MND := DerivedSubgroup(MNq.G);; MNHl := Elements(MNq.H);;
  for MNSeed in DCP2Seeds do
    MNms := List([0..(MNq.K_ord/MNq.M_ord)-1], t -> MNSeed.m_seed + MNq.M_ord*t);;
    MNF1p  := Length(MNms);;
    MNF1pp := Number(MNms, m -> Gcd(2*m+1, MNq.K_ord) = 1);;
    MNJF := MNEval(MNSeed.codes, MNq.JX, MNq.JY, Identity(MNq.G));;
    MNper := [];;
    for MNm in MNms do
      MNc := 0;; MNu := 2*MNm+1;;
      if Gcd(MNu, MNq.K_ord) = 1 then
        for MNh in MNHl do
          MNp := MNJF*MNh;;
          if not (MNp in MND) then continue; fi;
          if MNp*Image(MNTh,MNp) <> Identity(MNA) then continue; fi;
          MNw := MNq.JY^MNm * MNp;;
          if Image(MNTa,Image(MNTa,MNw))*Image(MNTa,MNw)*MNw <> MNJC^MNm then continue; fi;
          if Size(Group(MNq.JX^MNu, MNp^-1*MNq.JY^MNu*MNp)) <> Size(MNq.G) then continue; fi;
          MNc := MNc + 1;;
        od;
      fi;
      Add(MNper, MNc);;
    od;
    MNlift := Number(MNper, x -> x > 0);;
    MNmul  := Set(Filtered(MNper, x -> x > 0));;
    MNok   := (MNlift = MNF1pp) and (Length(MNmul) <= 1);;
    if not MNok then MNall := false; fi;
    if Length(MNmul) = 1 then Add(MNmults, MNmul[1]); fi;
    MNrows := MNrows + 1;;
    Print("MN_ROW b3idx=", Index(MNNode), " seed=", MNSeed.name,
          " K_ord=", MNq.K_ord, " F1p=", MNF1p, " F1pp=", MNF1pp,
          " lifting_m=", MNlift, " mult=", MNmul,
          " valid=", Sum(MNper),
          " CLAIM_OK=", MNok, "\n");
  od;
od;
Print("MN_SUMMARY rows=", MNrows, "  ALL_CLAIM_OK=", MNall, "\n");
Print("MN_MULTIPLICITY_VALUES_SEEN ", Collected(SortedList(MNmults)), "\n");
Print("MN_DONE\n");
QUIT;
