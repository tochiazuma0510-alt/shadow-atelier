#############################################################################
## math_f6false_witness_v1.g -- mathematician (Opus 5), 2026-08-28
## Scan F6=false windows (LINS<=100) for rows where v1's naive word-level
## hex311 and the (F2) quotient-rule hex311 DISAGREE. Uses the repo's OWN
## TauWord/ThetaWord/EvalWordInQ (prepend convention) for the naive side, so
## the comparison is faithful to drophunt_checker_producer_v1.g L218-224.
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;
if LoadPackage("lins") <> true then Error("MW: LINS load failed"); fi;
MWSearch := LowIndexNormalSubgroupsSearch(DCP2B3, 100);;
MWNodes  := ComputedNormalSubgroups(MWSearch);;

MWWit := [];; MWScanned := 0;; MWRows := 0;; MWDisagree := 0;; MWEvalOk := 0;; MWEvalBad := 0;;
MWCharmDis := 0;;
for MWNode in MWNodes do
  if Index(MWNode) = 1 then continue; fi;
  if Length(MWWit) >= 6 or MWScanned >= 26 then break; fi;
  MWq := DCP2BuildWindow(Grp(MWNode));;
  if MWq.c_in_K then continue; fi;          # only F6=false windows
  MWScanned := MWScanned + 1;;
  MWJC := DCP2DirectSumPerm(Identity(DCP2MBlock), DCP2MDegree, MWq.Cp_on_L, MWq.degL);;
  MWA  := Group(MWq.JX, MWq.JY, MWJC);;
  MWTa := GroupHomomorphismByImages(MWA, MWA, [MWq.JX, MWq.JY, MWJC],
            [MWq.JY, MWq.JY^-1*MWq.JX^-1*MWJC, MWJC]);;
  if MWTa = fail then Print("MW_TAU_FAIL idx=", Index(MWNode), "\n"); continue; fi;
  for MWSeed in DCP2Seeds do
    MWJF := EvalWordInQ(MWSeed.letters, MWq.JX, MWq.JY, Identity(MWq.G));;
    for MWh in Elements(MWq.H) do
      MWp  := MWJF * MWh;;
      MWwp := DCP2FreeEltToLetters(PreImagesRepresentative(MWq.epi, MWp));;
      # self-check: does the repo's prepend evaluator reproduce the element?
      if EvalWordInQ(MWwp, MWq.JX, MWq.JY, Identity(MWq.G)) = MWp
        then MWEvalOk := MWEvalOk + 1;; else MWEvalBad := MWEvalBad + 1;; fi;
      for MWm in List([0..(MWq.K_ord/MWq.M_ord)-1], t -> MWSeed.m_seed + MWq.M_ord*t) do
        MWRows := MWRows + 1;;
        # --- v1 naive (word level), verbatim shape of producer_v1 L221-224 ---
        MWymfW := Concatenation(List([1..MWm], i -> ["y",1]), MWwp);;
        MWt1   := TauWord(MWymfW);;  MWt2 := TauWord(MWt1);;
        MWnaive := EvalWordInQ(Concatenation(MWt2, MWt1, MWymfW),
                     MWq.JX, MWq.JY, Identity(MWq.G)) = Identity(MWq.G);;
        # --- (F2) quotient rule, group-element level in A = PB3/K ---
        MWymf  := MWq.JY^MWm * MWp;;
        MWF2   := (Image(MWTa, Image(MWTa, MWymf)) * Image(MWTa, MWymf) * MWymf) = MWJC^MWm;;
        # charming (same test as producer)
        MWchar := (Gcd(2*MWm+1, MWq.K_ord) = 1) and (MWp in MWq.D);;
        if MWnaive <> MWF2 then
          MWDisagree := MWDisagree + 1;;
          if MWchar then MWCharmDis := MWCharmDis + 1;; fi;
          if Length(MWWit) < 6 then
            Add(MWWit, rec(idx:=Index(MWNode), Kord:=MWq.K_ord, F2:=MWq.F2,
              cord:=Order(MWJC), seed:=MWSeed.name, m:=MWm, charming:=MWchar,
              naive:=MWnaive, f2:=MWF2, elen:=Length(MWwp),
              esum:=Sum(MWwp, l -> l[2])));;
          fi;
        fi;
      od;
    od;
  od;
od;
Print("MW_SCAN f6false_windows_scanned=", MWScanned, " rows=", MWRows,
      " disagreements=", MWDisagree, " of_which_charming=", MWCharmDis, "\n");
Print("MW_EVALCHECK prepend_reproduces_element ok=", MWEvalOk, " bad=", MWEvalBad, "\n");
for MWw in MWWit do
  Print("MW_WITNESS b3idx=", MWw.idx, " K_ord=", MWw.Kord, " F2=", MWw.F2,
        " ord(cbar)=", MWw.cord, " seed=", MWw.seed, " m=", MWw.m,
        " charming=", MWw.charming, " | v1_naive_hex311=", MWw.naive,
        " (F2)_hex311=", MWw.f2, " | |w|=", MWw.elen, " e(w)=", MWw.esum, "\n");
od;
Print("MW_DONE\n");
QUIT;
