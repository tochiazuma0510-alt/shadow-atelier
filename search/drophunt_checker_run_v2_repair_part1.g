#############################################################################
## drophunt_checker_run_v2_repair.g -- repaired-predicate re-run on the same
## small test windows as v1, PLUS a real MU-1 (word-representative
## invariance) mutant test, PLUS a stage 0-b cost/RSS probe on the largest
## fib<=100 window (b3_index=1944 class).
#############################################################################

Read("search/drophunt_checker_producer_v2.g");;

if LoadPackage("lins") <> true then Error("DCR2: LINS package load failed"); fi;

DCR2T0 := GAPLIB_WallElapsedMs();;
DCR2Search := LowIndexNormalSubgroupsSearch(DCP2B3, 100);;
DCR2Nodes := ComputedNormalSubgroups(DCR2Search);;
Print("DCR2_LINS100_DONE nodes=", Length(DCR2Nodes),
  " elapsed_ms=", GAPLIB_WallElapsedMs()-DCR2T0, "\n");;

DCR2Targets := [
  rec(bIndex:=96, expKord:=18, expF2:=2, label:="cheap1_fib2"),
  rec(bIndex:=12, expKord:=18, expF2:=3, label:="cheap2_fib3"),
  rec(bIndex:=18, expKord:=18, expF2:=3, label:="cheap3_fib3"),
  rec(bIndex:=3,  expKord:=18, expF2:=3, label:="L3_fib3_K2ingredient"),
  rec(bIndex:=48, expKord:=36, expF2:=2, label:="fib4_kordvalidated")
];;

DCR2Summary := [];;
DCR2FirstPassCandidate := fail;;

for DCR2Tgt in DCR2Targets do
  DCR2Matches := Filtered(DCR2Nodes, n -> Index(n) = DCR2Tgt.bIndex);;
  for DCR2Node in DCR2Matches do
    DCR2L := Grp(DCR2Node);;
    DCR2Qrec := DCP2BuildWindow(DCR2L);;
    if DCR2Qrec.K_ord = DCR2Tgt.expKord and DCR2Qrec.F2 = DCR2Tgt.expF2 then
      Print("DCR2_TARGET_MATCHED label=", DCR2Tgt.label, " b3_index=", DCR2Tgt.bIndex,
        " c_in_K(F6)=", DCR2Qrec.c_in_K, " K_ord=", DCR2Qrec.K_ord,
        " F2=", DCR2Qrec.F2, " F3=", DCR2Qrec.F3, "\n");;
      for DCR2Seed in DCP2Seeds do
        DCR2RunT0 := GAPLIB_WallElapsedMs();;
        DCR2Result := DCP2EvalWindow(DCR2Qrec, DCR2Seed);;
        DCR2RunElapsed := GAPLIB_WallElapsedMs() - DCR2RunT0;;
        Print("DCR2_RESULT label=", DCR2Tgt.label, " seed=", DCR2Seed.name,
          " c_in_K=", DCR2Qrec.c_in_K,
          " evaluated=", DCR2Result.evaluated_count,
          " expected=", DCR2Result.expected_count,
          " valid=", DCR2Result.valid_count,
          " blocked=", DCR2Result.blocked_count,
          " elapsed_ms=", DCR2RunElapsed, "\n");;
        Add(DCR2Summary, rec(label:=DCR2Tgt.label, b3_index:=DCR2Tgt.bIndex,
          c_in_K:=DCR2Qrec.c_in_K, K_ord:=DCR2Qrec.K_ord, F2:=DCR2Qrec.F2,
          F3_fib:=DCR2Qrec.F3, seed:=DCR2Seed.name,
          evaluated:=DCR2Result.evaluated_count, expected:=DCR2Result.expected_count,
          valid:=DCR2Result.valid_count, blocked:=DCR2Result.blocked_count,
          elapsed_ms:=DCR2RunElapsed));;
        if DCR2FirstPassCandidate = fail and DCR2Qrec.c_in_K then
          for DCR2Row in DCR2Result.rows do
            if DCR2Row.verdict = true then
              DCR2FirstPassCandidate := rec(qrec:=DCR2Qrec, seed:=DCR2Seed,
                m:=DCR2Row.m, word_codes:=DCR2Row.f_word_codes, label:=DCR2Tgt.label);;
              break;;
            fi;;
          od;;
        fi;;
      od;;
      break;;
    fi;;
  od;;
od;;

Print("DCR2_SUMMARY_DONE\n");;

#############################################################################
## MU-1: group-element-function-of-verdict mutant.
## Take the first genuinely-PASSING candidate found above (window with
## F6=c_in_K=true), find a nontrivial RELATOR r (word in x,y evaluating to
## Identity(G) but r<>[]), re-evaluate the FULL predicate chain on the
## MUTATED word (original word ++ r) directly (not via the normal candidate
## generator), and confirm the verdict is UNCHANGED. If it changes, the
## predicate is NOT a function of the group element -- MU-1 fails, and no
## further run should proceed (per spec).
#############################################################################
DCP2EvalSingleCandidate := function(qrec, m, word)
  local u, okCm, okCf, p, thetaWord, hex310, yWordM, ymfWord, tauWord1,
    tauWord2, hex311, genA, genB, onto, verdict;
  u := 2*m+1;;
  p := EvalWordInQ(word, qrec.JX, qrec.JY, Identity(qrec.G));;
  okCm := Gcd(u, qrec.K_ord) = 1;;
  okCf := p in qrec.D;;
  if not (okCm and okCf) then return rec(charming:=false, verdict:=false, perm:=p); fi;;
  thetaWord := ThetaWord(word);;
  hex310 := EvalWordInQ(Concatenation(word, thetaWord), qrec.JX, qrec.JY, Identity(qrec.G)) = Identity(qrec.G);;
  if not hex310 then return rec(charming:=true, hex310:=false, verdict:=false, perm:=p); fi;;
  yWordM := List([1..m], ii -> ["y",1]);;
  ymfWord := Concatenation(yWordM, word);;
  tauWord1 := TauWord(ymfWord);; tauWord2 := TauWord(tauWord1);;
  hex311 := EvalWordInQ(Concatenation(tauWord2, tauWord1, ymfWord), qrec.JX, qrec.JY, Identity(qrec.G)) = Identity(qrec.G);;
  if not hex311 then return rec(charming:=true, hex310:=true, hex311:=false, verdict:=false, perm:=p); fi;;
  genA := qrec.JX^u;; genB := p^-1 * qrec.JY^u * p;;
  onto := Size(Group(genA, genB)) = Size(qrec.G);;
  verdict := onto;;
  return rec(charming:=true, hex310:=true, hex311:=true, onto:=onto, verdict:=verdict, perm:=p);;
end;;

DCP2LetterCode := function(l)
  if l[1]="x" then return l[2]; else return 2*l[2]; fi;
end;;
DCP2CodesToWord := w -> List(w, DCP2CodeToLetter);;

DCP2FindRelator := function(qrec, maxTries, maxLen)
  local tries, len, w, i, letterChoices, chosen, val;
  letterChoices := [["x",1],["x",-1],["y",1],["y",-1]];;
  for tries in [1..maxTries] do
    len := 4 + (tries mod maxLen);;
    w := [];;
    for i in [1..len] do Add(w, letterChoices[Random([1..4])]); od;;
    val := EvalWordInQ(w, qrec.JX, qrec.JY, Identity(qrec.G));;
    if val = Identity(qrec.G) and Length(w) > 0 then
      return w;;
    fi;;
  od;;
  return fail;;
end;;

DCR2Mu1Result := rec(status:="NOT_RUN");;
if DCR2FirstPassCandidate <> fail then
  DCR2Cand := DCR2FirstPassCandidate;;
  DCR2Qrec := DCR2Cand.qrec;;
  DCR2OrigWord := DCP2CodesToWord(DCR2Cand.word_codes);;
  DCR2Relator := DCP2FindRelator(DCR2Qrec, 20000, 6);;
  if DCR2Relator = fail then
    DCR2Mu1Result := rec(status:="RELATOR_NOT_FOUND", label:=DCR2Cand.label);;
    Print("DCR2_MU1 status=RELATOR_NOT_FOUND\n");;
  else
    DCR2MutWord := Concatenation(DCR2OrigWord, DCR2Relator);;
    DCR2OrigEval := DCP2EvalSingleCandidate(DCR2Qrec, DCR2Cand.m, DCR2OrigWord);;
    DCR2MutEval := DCP2EvalSingleCandidate(DCR2Qrec, DCR2Cand.m, DCR2MutWord);;
    DCR2SamePerm := (DCR2OrigEval.perm = DCR2MutEval.perm);;
    DCR2SameVerdict := (DCR2OrigEval.verdict = DCR2MutEval.verdict);;
    if DCR2SameVerdict then DCR2Mu1Status := "PASS_INVARIANT"; else DCR2Mu1Status := "FAIL_NONINVARIANT"; fi;;
    DCR2Mu1Result := rec(status:=DCR2Mu1Status,
      label:=DCR2Cand.label, m:=DCR2Cand.m,
      orig_word_len:=Length(DCR2OrigWord), relator_len:=Length(DCR2Relator),
      mut_word_len:=Length(DCR2MutWord), same_group_element:=DCR2SamePerm,
      orig_verdict:=DCR2OrigEval.verdict, mut_verdict:=DCR2MutEval.verdict,
      same_verdict:=DCR2SameVerdict);;
    Print("DCR2_MU1 status=", DCR2Mu1Result.status,
      " label=", DCR2Cand.label, " m=", DCR2Cand.m,
      " same_group_element=", DCR2SamePerm,
      " orig_verdict=", DCR2OrigEval.verdict,
      " mut_verdict=", DCR2MutEval.verdict, "\n");;
  fi;;
else
  Print("DCR2_MU1 status=NO_PASSING_CANDIDATE_FOUND\n");;
fi;;

#############################################################################
## Output JSON (part 1: windows + MU-1 only; stage 0-b runs separately)
#############################################################################
DCR2TotalElapsed := GAPLIB_WallElapsedMs() - DCR2T0;;
Print("DCR2_TOTAL_ELAPSED_MS=", DCR2TotalElapsed, "\n");;

DCR2SummaryJson := JoinC(List(DCR2Summary, r -> Concatenation(
  "{\"label\":", JStr(r.label), ",\"b3_index\":", String(r.b3_index),
  ",\"c_in_K\":", JB(r.c_in_K), ",\"K_ord\":", String(r.K_ord),
  ",\"F2\":", String(r.F2), ",\"F3_fib\":", String(r.F3_fib),
  ",\"seed\":", JStr(r.seed), ",\"evaluated\":", String(r.evaluated),
  ",\"expected\":", String(r.expected), ",\"valid\":", String(r.valid),
  ",\"blocked\":", String(r.blocked), ",\"elapsed_ms\":", String(r.elapsed_ms), "}")), ",\n");;

DCR2Mu1Json := "null";;
if IsBound(DCR2Mu1Result.status) then
  if DCR2Mu1Result.status = "PASS_INVARIANT" or DCR2Mu1Result.status = "FAIL_NONINVARIANT" then
    DCR2Mu1Json := Concatenation("{\"status\":", JStr(DCR2Mu1Result.status),
      ",\"label\":", JStr(DCR2Mu1Result.label), ",\"m\":", String(DCR2Mu1Result.m),
      ",\"orig_word_len\":", String(DCR2Mu1Result.orig_word_len),
      ",\"relator_len\":", String(DCR2Mu1Result.relator_len),
      ",\"mut_word_len\":", String(DCR2Mu1Result.mut_word_len),
      ",\"same_group_element\":", JB(DCR2Mu1Result.same_group_element),
      ",\"orig_verdict\":", JB(DCR2Mu1Result.orig_verdict),
      ",\"mut_verdict\":", JB(DCR2Mu1Result.mut_verdict),
      ",\"same_verdict\":", JB(DCR2Mu1Result.same_verdict), "}");;
  else
    DCR2Mu1Json := Concatenation("{\"status\":", JStr(DCR2Mu1Result.status), "}");;
  fi;;
fi;;

DCR2Output := Concatenation(
  "{\n  \"schema\":\"drophunt-checker-run-v2-repair-part1/v1\",\n",
  "  \"lins100_search_elapsed_ms\":", String(GAPLIB_WallElapsedMs()-DCR2T0), ",\n",
  "  \"total_elapsed_ms\":", String(DCR2TotalElapsed), ",\n",
  "  \"windows\":[\n", DCR2SummaryJson, "\n  ],\n",
  "  \"mu1_word_representative_invariance\":", DCR2Mu1Json, "\n}\n");;
WriteFile("search/certs/drophunt_checker_run_v2_repair_part1_20260828.json", DCR2Output);;
Print("DCR2_OUTPUT path=search/certs/drophunt_checker_run_v2_repair_part1_20260828.json\n");;
Print("ALL_DONE\n");;
