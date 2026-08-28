#############################################################################
## drophunt_mutants_v3.g -- items 3,6: real mutant executions on a c_notin_K
## window (b3_index=48, fib4_kordvalidated, F1=2 so m in {0,18} is available
## -- needed so c^m can differ from Identity for m!=0), plus item 6's
## negative (seed-swap) test.
#############################################################################

Read("search/drophunt_checker_producer_v3.g");;
if LoadPackage("lins") <> true then Error("DM3: LINS load failed"); fi;;

DM3T0 := GAPLIB_WallElapsedMs();;
DM3Search := LowIndexNormalSubgroupsSearch(DCP3B3, 100);;
DM3Nodes := ComputedNormalSubgroups(DM3Search);;
Print("DM3_LINS100 nodes=", Length(DM3Nodes), " elapsed_ms=", GAPLIB_WallElapsedMs()-DM3T0, "\n");;

## b3_index=5 gives K_ord=90 (F1=5, m in {0,18,36,54,72}), ord(cbar)=5 --
## crucially 5 does NOT divide 18, so c^18 = c^(18 mod 5) = c^3 != Identity,
## making MU-2 (RHS dropped to Identity) actually detectable here, unlike
## b3_index=48 (ord(cbar)=2 divides 18, so c^m=Identity for every valid m,
## making MU-2 vacuously undetectable there -- found by scratchpad/
## scan_mu2_window.g).
DM3Tgt := fail;;
for DM3Node in DM3Nodes do
  if Index(DM3Node) = 5 then
    DM3q := DCP3BuildWindow(Grp(DM3Node));;
    if DM3q.K_ord = 90 and DM3q.F2 = 5 then DM3Tgt := DM3q;; break; fi;;
  fi;;
od;;
if DM3Tgt = fail then Error("DM3: target window not found"); fi;;
Print("DM3_WINDOW c_in_K=", DM3Tgt.c_in_K, " K_ord=", DM3Tgt.K_ord,
  " F2=", DM3Tgt.F2, " ord(cbar)=", Order(DM3Tgt.JC), "\n");;

DM3Seed36 := DCP3Seeds[1];;   # row36
DM3Seed71 := DCP3Seeds[2];;   # row71
DM3JF36 := DCP3EvalWord(DM3Seed36.letters, DM3Tgt.JX, DM3Tgt.JY, Identity(DM3Tgt.G));;
DM3Target0_36 := Image(DM3Tgt.pi0, DM3JF36);;
DM3Hlist := Elements(DM3Tgt.H);;

## Pick a genuine PASSING candidate at m=18 (nonzero, so c^m != c^0=Identity
## in general -- need Order(cbar) to not divide 18 trivially; report either way).
DM3Cand := fail;; DM3M := fail;;
for DM3m in [18, 36, 54, 72, 0] do
  for DM3h in DM3Hlist do
    DM3p := DM3JF36 * DM3h;;
    if Gcd(2*DM3m+1, DM3Tgt.K_ord) = 1 and DM3p in DM3Tgt.D then
      DM3hex310 := (DM3p * Image(DM3Tgt.thetaHom, DM3p) = Identity(DM3Tgt.A));;
      if DM3hex310 then
        DM3ymf := DM3Tgt.JY^DM3m * DM3p;;
        DM3lhs := Image(DM3Tgt.tauHom, Image(DM3Tgt.tauHom, DM3ymf)) * Image(DM3Tgt.tauHom, DM3ymf) * DM3ymf;;
        DM3rhs := DM3Tgt.JC^DM3m;;
        if DM3lhs = DM3rhs then
          DM3Cand := DM3p;; DM3M := DM3m;; break;;
        fi;;
      fi;;
    fi;;
  od;;
  if DM3Cand <> fail then break; fi;;
od;;
if DM3Cand = fail then Error("DM3: no passing candidate found for mutant tests"); fi;;
Print("DM3_CANDIDATE_FOUND m=", DM3M, "\n");;

DM3p := DM3Cand;;
DM3ymf := DM3Tgt.JY^DM3M * DM3p;;
DM3CorrectLhs := Image(DM3Tgt.tauHom, Image(DM3Tgt.tauHom, DM3ymf)) * Image(DM3Tgt.tauHom, DM3ymf) * DM3ymf;;
DM3CorrectRhs := DM3Tgt.JC^DM3M;;
DM3CorrectHolds := (DM3CorrectLhs = DM3CorrectRhs);;
Print("DM3_BASELINE correct_F2_rule_holds=", DM3CorrectHolds,
  " c^m=", DM3CorrectRhs, " (Identity? ", DM3CorrectRhs=Identity(DM3Tgt.A), ")\n");;

#############################################################################
## MU-2: RHS mutated to Identity (dropping c^m) -- must FLIP if c^m != Identity
#############################################################################
DM3Mu2Rhs := Identity(DM3Tgt.A);;
DM3Mu2Holds := (DM3CorrectLhs = DM3Mu2Rhs);;
DM3Mu2Detected := (DM3Mu2Holds <> DM3CorrectHolds);;
Print("DM3_MU2 rhs_mutated_to_identity holds=", DM3Mu2Holds,
  " differs_from_correct=", DM3Mu2Detected, "\n");;

#############################################################################
## MU-3: tau~ replaced by NAIVE word-level tau (evaluated via a word
## representative of the SAME element p, with an ADVERSARIAL relator
## appended to guarantee e(r) mod ord(cbar) != 0 -- reusing item2's method).
#############################################################################
DM3FreeF := FreeGroup("x","y");; DM3fx := DM3FreeF.1;; DM3fy := DM3FreeF.2;;
DM3Epi := GroupHomomorphismByImagesNC(DM3FreeF, DM3Tgt.G, [DM3fx,DM3fy], [DM3Tgt.JX,DM3Tgt.JY]);;
DM3FreeEltToLetters := function(fpElt)
  local ext, out, i, gen, exp, letterName;
  ext := ExtRepOfObj(UnderlyingElement(fpElt));;
  out := [];;
  for i in [1,3..Length(ext)-1] do
    gen := ext[i];; exp := ext[i+1];;
    if gen = 1 then letterName := "x"; else letterName := "y"; fi;;
    if exp > 0 then Append(out, List([1..exp], j -> [letterName,1]));
    else Append(out, List([1..-exp], j -> [letterName,-1])); fi;;
  od;;
  return out;;
end;;
DM3Wp := DM3FreeEltToLetters(PreImagesRepresentative(DM3Epi, DM3p));;
DM3OrdC := Order(DM3Tgt.JC);;
Print("DM3_ORD_CBAR_FOR_RELATOR_SEARCH=", DM3OrdC, "\n");;

DM3NaiveTau := function(letters)
  local out, l;
  out := [];;
  for l in letters do
    if l[1]="x" then Add(out, ["y", l[2]]);
    else
      if l[2] = 1 then Append(out, [["y",-1],["x",-1]]);
      else Append(out, [["x",1],["y",1]]); fi;;
    fi;;
  od;;
  return out;;
end;;

DM3Relator := fail;;
DM3LetterChoices := [["x",1],["x",-1],["y",1],["y",-1]];;
if DM3OrdC > 1 then
  for DM3Try in [1..200000] do
    DM3Len := 3 + (DM3Try mod 20);;
    DM3W := List([1..DM3Len], i -> DM3LetterChoices[Random([1..4])]);;
    if EvalWordInQ(DM3W, DM3Tgt.JX, DM3Tgt.JY, Identity(DM3Tgt.G)) = Identity(DM3Tgt.G) then
      DM3Esum := Sum(List(DM3W, l -> l[2]));;
      if (DM3Esum mod DM3OrdC) <> 0 then DM3Relator := DM3W;; break; fi;;
    fi;;
  od;;
fi;;
if DM3Relator = fail then
  Print("DM3_WARNING adversarial relator not found by random search; using fallback (esum may be 0 mod ordC)\n");;
  DM3Relator := [["x",-1],["y",1],["x",1],["y",-1],["x",-1],["y",1],["x",1],["y",-1]];;
fi;;

DM3YWordM := List([1..DM3M], ii -> ["y",1]);;
DM3WpMut := Concatenation(DM3Wp, DM3Relator);;
DM3YmfL := Concatenation(DM3YWordM, DM3WpMut);;
DM3T1 := DM3NaiveTau(DM3YmfL);; DM3T2 := DM3NaiveTau(DM3T1);;
DM3NaiveLhs := EvalWordInQ(Concatenation(DM3T2,DM3T1,DM3YmfL), DM3Tgt.JX, DM3Tgt.JY, Identity(DM3Tgt.G));;
DM3NaiveHolds := (DM3NaiveLhs = Identity(DM3Tgt.G));;
DM3Mu3Detected := (DM3NaiveHolds <> DM3CorrectHolds);;
Print("DM3_MU3 naive_tau_mutant_holds=", DM3NaiveHolds,
  " differs_from_correct=", DM3Mu3Detected,
  " relator_len=", Length(DM3Relator),
  " relator_esum_mod_ordC=", Sum(List(DM3Relator,l->l[2])) mod DM3OrdC, "\n");;

#############################################################################
## MU-9 (translated per coordinator instruction, since words no longer
## exist in the p-direct predicate): swap theta~'s and tau~'s closed-form
## IMAGE DEFINITIONS to the WRONG (v1-naive-equivalent) automorphism -- i.e.
## build theta_wrong using tau~'s formula and vice versa (a "reversal"
## mutant analogous to W-1's role/generator-order reversal), and confirm
## this produces a DIFFERENT verdict / fails a well-definedness or identity
## check.
#############################################################################
DM3ThetaWrong := GroupHomomorphismByImages(DM3Tgt.A, DM3Tgt.A,
  [DM3Tgt.JX,DM3Tgt.JY,DM3Tgt.JC], [DM3Tgt.JY, DM3Tgt.JY^-1*DM3Tgt.JX^-1*DM3Tgt.JC, DM3Tgt.JC]);;  # tau's formula used as theta
DM3Mu9ThetaWD := (DM3ThetaWrong <> fail);;
DM3Mu9HexOrig := (DM3p * Image(DM3Tgt.thetaHom, DM3p) = Identity(DM3Tgt.A));;
DM3Mu9HexWrong := fail;;
if DM3Mu9ThetaWD then
  DM3Mu9HexWrong := (DM3p * Image(DM3ThetaWrong, DM3p) = Identity(DM3Tgt.A));;
fi;;
Print("DM3_MU9 theta_wrong_welldefined=", DM3Mu9ThetaWD,
  " hex310_orig=", DM3Mu9HexOrig, " hex310_wrong=", DM3Mu9HexWrong,
  " differs=", (DM3Mu9ThetaWD and DM3Mu9HexWrong<>DM3Mu9HexOrig), "\n");;

#############################################################################
## MU-8 (seed swap) + ITEM 6 NEGATIVE TEST: use row71's seed word but claim
## it is row36 (i.e. compare its pi0-image against row36's PINNED constant).
## Must be REJECTED (mismatch caught) -- this is the negative test the
## coordinator flagged as never having actually fired.
#############################################################################
DM3JF71 := DCP3EvalWord(DM3Seed71.letters, DM3Tgt.JX, DM3Tgt.JY, Identity(DM3Tgt.G));;
DM3Target0_71_as_if_36 := Image(DM3Tgt.pi0, DM3JF71);;
DM3SeedSwapMismatch := (DM3Seed36.m_target_pinned <> DM3Target0_71_as_if_36);;
Print("DM3_MU8_ITEM6_NEGATIVE seed71_treated_as_seed36 pinned_row36_target=",
  DM3Seed36.m_target_pinned, "\n  actual_pi0(seed71_word)=", DM3Target0_71_as_if_36,
  "\n  MISMATCH_DETECTED(should_be_true)=", DM3SeedSwapMismatch, "\n");;

DM3TotalElapsed := GAPLIB_WallElapsedMs() - DM3T0;;
Print("DM3_TOTAL_ELAPSED_MS=", DM3TotalElapsed, "\n");;

if DM3Mu9HexWrong = fail then
  DM3Mu9HexWrongJson := "null";;
  DM3Mu9Detected := false;;
else
  DM3Mu9HexWrongJson := JB(DM3Mu9HexWrong);;
  DM3Mu9Detected := (DM3Mu9ThetaWD and DM3Mu9HexWrong<>DM3Mu9HexOrig);;
fi;;

DM3Output := Concatenation(
  "{\n  \"schema\":\"drophunt-mutants-v3/v1\",\n",
  "  \"window\":{\"b3_index\":5,\"c_in_K\":", JB(DM3Tgt.c_in_K),
    ",\"K_ord\":", String(DM3Tgt.K_ord), ",\"ord_cbar\":", String(Order(DM3Tgt.JC)), "},\n",
  "  \"baseline_candidate_m\":", String(DM3M), ",\n",
  "  \"baseline_correct_F2_rule_holds\":", JB(DM3CorrectHolds), ",\n",
  "  \"MU2_rhs_dropped_to_identity\":{\"holds\":", JB(DM3Mu2Holds),
    ",\"detected_as_wrong\":", JB(DM3Mu2Detected), "},\n",
  "  \"MU3_naive_word_tau_with_adversarial_relator\":{",
    "\"relator_length\":", String(Length(DM3Relator)),
    ",\"relator_esum_mod_ordC\":", String(Sum(List(DM3Relator,l->l[2])) mod DM3OrdC),
    ",\"holds\":", JB(DM3NaiveHolds),
    ",\"detected_as_wrong\":", JB(DM3Mu3Detected), "},\n",
  "  \"MU9_theta_tau_formula_swap\":{\"theta_wrong_welldefined\":", JB(DM3Mu9ThetaWD),
    ",\"hex310_orig\":", JB(DM3Mu9HexOrig),
    ",\"hex310_wrong\":", DM3Mu9HexWrongJson,
    ",\"detected_as_wrong\":", JB(DM3Mu9Detected), "},\n",
  "  \"MU8_item6_negative_seed_swap\":{\"mismatch_detected\":", JB(DM3SeedSwapMismatch), "},\n",
  "  \"total_elapsed_ms\":", String(DM3TotalElapsed), "\n}\n");;
WriteFile("search/certs/drophunt_mutants_v3_20260829.json", DM3Output);;
Print("DM3_OUTPUT path=search/certs/drophunt_mutants_v3_20260829.json\n");;
Print("ALL_DONE\n");;
