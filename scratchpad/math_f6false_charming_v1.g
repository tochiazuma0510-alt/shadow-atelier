#############################################################################
## math_f6false_charming_v1.g -- mathematician (Opus 5), 2026-08-28
## Two questions, decided on real F6=false windows:
##  (Q1) does the wcp5d twist formula  R_tautilde(m,f) = R_naive(y^m w) * c^(m+e(w))
##       hold exactly, as an identity in A = PB3/K ?
##  (Q2) on CHARMING rows (the only rows where the producer ever evaluates
##       hex311), do the naive rule and the (F2) rule agree ?
## Also re-measures the word/element convention mismatch with the REVERSED word.
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;
if LoadPackage("lins") <> true then Error("MC: LINS load failed"); fi;
MCSearch := LowIndexNormalSubgroupsSearch(DCP2B3, 100);;
MCNodes  := ComputedNormalSubgroups(MCSearch);;

MCScan := 0;; MCRows := 0;; MCCharm := 0;; MCCharmDis := 0;; MCAllDis := 0;;
MCTwistOk := 0;; MCTwistBad := 0;; MCFwdOk := 0;; MCRevOk := 0;;
MCCharmEsumNonzeroModC := 0;; MCWit := [];;
for MCNode in MCNodes do
  if Index(MCNode) = 1 then continue; fi;
  if MCScan >= 12 then break; fi;
  MCq := DCP2BuildWindow(Grp(MCNode));;
  if MCq.c_in_K then continue; fi;
  MCScan := MCScan + 1;;
  MCJC := DCP2DirectSumPerm(Identity(DCP2MBlock), DCP2MDegree, MCq.Cp_on_L, MCq.degL);;
  MCA  := Group(MCq.JX, MCq.JY, MCJC);;
  MCcord := Order(MCJC);;
  MCTa := GroupHomomorphismByImages(MCA, MCA, [MCq.JX, MCq.JY, MCJC],
            [MCq.JY, MCq.JY^-1*MCq.JX^-1*MCJC, MCJC]);;
  if MCTa = fail then Print("MC_TAU_FAIL idx=", Index(MCNode), "\n"); continue; fi;
  for MCSeed in DCP2Seeds do
    MCJF := EvalWordInQ(MCSeed.letters, MCq.JX, MCq.JY, Identity(MCq.G));;
    for MCh in Elements(MCq.H) do
      MCp   := MCJF * MCh;;
      MCwp  := DCP2FreeEltToLetters(PreImagesRepresentative(MCq.epi, MCp));;
      MCwpR := Reversed(MCwp);;
      if EvalWordInQ(MCwp,  MCq.JX, MCq.JY, Identity(MCq.G)) = MCp then MCFwdOk := MCFwdOk+1;; fi;
      if EvalWordInQ(MCwpR, MCq.JX, MCq.JY, Identity(MCq.G)) = MCp then MCRevOk := MCRevOk+1;; fi;
      MCe := Sum(MCwp, l -> l[2]);;
      for MCm in List([0..(MCq.K_ord/MCq.M_ord)-1], t -> MCSeed.m_seed + MCq.M_ord*t) do
        MCRows := MCRows + 1;;
        MCchar := (Gcd(2*MCm+1, MCq.K_ord) = 1) and (MCp in MCq.D);;
        if MCchar then MCCharm := MCCharm + 1;;
          if (MCe mod MCcord) <> 0 then MCCharmEsumNonzeroModC := MCCharmEsumNonzeroModC + 1;; fi;
        fi;
        # naive LHS as a GROUP ELEMENT, using the reversed word so that it
        # genuinely represents p under the repo's prepend evaluator
        MCymfW := Concatenation(List([1..MCm], i -> ["y",1]), MCwpR);;
        MCt1 := TauWord(MCymfW);; MCt2 := TauWord(MCt1);;
        MCnaiveLHS := EvalWordInQ(Concatenation(MCt2, MCt1, MCymfW),
                        MCq.JX, MCq.JY, Identity(MCq.G));;
        MCnaive := MCnaiveLHS = Identity(MCq.G);;
        # (F2) LHS as a group element in A
        MCymf := MCq.JY^MCm * MCp;;
        MCF2LHS := Image(MCTa, Image(MCTa, MCymf)) * Image(MCTa, MCymf) * MCymf;;
        MCF2 := MCF2LHS = MCJC^MCm;;
        # (Q1) twist formula check:  F2LHS = naiveLHS * c^(m + e(w)) ?
        if MCF2LHS = MCnaiveLHS * MCJC^(MCm + MCe) then MCTwistOk := MCTwistOk+1;;
        else MCTwistBad := MCTwistBad+1;; fi;
        if MCnaive <> MCF2 then
          MCAllDis := MCAllDis + 1;;
          if MCchar then MCCharmDis := MCCharmDis + 1;;
            if Length(MCWit) < 5 then
              Add(MCWit, rec(idx:=Index(MCNode), Kord:=MCq.K_ord, cord:=MCcord,
                seed:=MCSeed.name, m:=MCm, e:=MCe, naive:=MCnaive, f2:=MCF2));; fi;
          fi;
        fi;
      od;
    od;
  od;
od;
Print("MC_SCAN f6false_windows=", MCScan, " rows=", MCRows, " charming_rows=", MCCharm, "\n");
Print("MC_TWIST wcp5d_formula_holds=", MCTwistOk, " fails=", MCTwistBad, "\n");
Print("MC_CONV fwd_word_reproduces_p=", MCFwdOk, "  reversed_word_reproduces_p=", MCRevOk, "\n");
Print("MC_DISAGREE all_rows=", MCAllDis, "  charming_rows=", MCCharmDis, "\n");
Print("MC_CHARM_ESUM charming_rows_with_e(w)_notdiv_by_ord(c)=", MCCharmEsumNonzeroModC, "\n");
for MCw in MCWit do
  Print("MC_CHARMING_WITNESS b3idx=", MCw.idx, " K_ord=", MCw.Kord, " ord(cbar)=", MCw.cord,
        " seed=", MCw.seed, " m=", MCw.m, " e(w)=", MCw.e,
        " naive=", MCw.naive, " (F2)=", MCw.f2, "\n");
od;
Print("MC_DONE\n");
QUIT;
