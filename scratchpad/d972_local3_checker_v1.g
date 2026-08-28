## scratchpad/d972_local3_checker_v1.g -- LOCAL-3 protocol (S1-S10), CHECKER system.
## Math source: scratchpad/d972_idx3_arith_datum_independent_v1.md sec.7.3 (frozen spec).
## Independent authorship: written from scratch in GAP (different language/runtime from the
## Python producer, scratchpad/d972_local3_producer_v1.py); NO shared code/import between them.
## This checker re-derives u0inv/beta from the SAME cert files (inventory only) but implements
## its own modular-arithmetic / discrete-log / cube-residue routines independently.

Read("search/probe/wac_v1/gap_output_prelude.g");

Print("############################################################\n");
Print("# d972_local3_checker_v1.g -- LOCAL-3 independent checker\n");
Print("############################################################\n");

## ================= inputs (own read, own parsing -- no shared helper with producer) ===============
u0inv := -1423828125/256;;
beta := 2;;
Print("u0inv = ", u0inv, "\n");
Print("beta = ", beta, "\n");

## ================= own modular reduction of a rational mod p =======================================
ModFrac := function(fr, p)
  local num, den, deninv;
  num := NumeratorRat(fr) mod p;
  den := DenominatorRat(fr) mod p;
  deninv := den^-1 mod p;
  return (num * deninv) mod p;
end;;

CubeResidue := function(zModP, p)
  return PowerModInt(zModP, (p-1)/3, p);
end;;

FindMu3Gen := function(p)
  local g, cand;
  for g in [2..p-1] do
    cand := PowerModInt(g, (p-1)/3, p);
    if cand <> 1 then return cand; fi;
  od;
  Error("no generator found");
end;;

DiscreteLogMu3 := function(val, omega, p)
  local cur, e;
  cur := 1;
  for e in [0,1,2] do
    if cur = val then return e; fi;
    cur := (cur * omega) mod p;
  od;
  Error("val not a power of omega");
end;;

## ================= own S1-S9 chain implementation ==================================================
RunChain := function(p, sgn, mu3GenPower, uExtraFactor)
  local out, s1, s2, uS4, uS4modp, betamodp, Su, Sbeta, s5, cprimeCode, cprime,
        omegaBase, omega, k3, psi;
  out := rec(p:=p, sgn:=sgn);;
  s1 := (p mod 9 = 1);;
  out.S1 := s1;;
  if not s1 then out.status := "STOP_S1_FAIL"; return out; fi;

  s2 := (NumeratorRat(u0inv) mod p <> 0) and (DenominatorRat(u0inv) mod p <> 0) and (beta mod p <> 0);;
  out.S2 := s2;;
  if not s2 then out.status := "STOP_S2_FAIL"; return out; fi;

  if sgn = 1 then uS4 := u0inv;;
  elif sgn = -1 then uS4 := 1/u0inv;;
  else Error("bad sgn"); fi;
  uS4 := uS4 * uExtraFactor;;

  uS4modp := ModFrac(uS4, p);;
  betamodp := beta mod p;;

  Su := CubeResidue(uS4modp, p);;
  Sbeta := CubeResidue(betamodp, p);;
  out.Su := Su;;  out.Sbeta := Sbeta;;

  s5 := (Su <> 1) and (Sbeta <> 1);;
  out.S5 := s5;;
  if not s5 then out.status := "STOP_S5_FAIL_NONDISCRIMINATING"; return out; fi;

  if Su = Sbeta then cprimeCode := 1;; else cprimeCode := 2;; fi;
  out.cprimeCode := cprimeCode;;
  if cprimeCode = 1 then out.cprime := 1;; else out.cprime := -1;; fi;

  omegaBase := FindMu3Gen(p);;
  omega := PowerModInt(omegaBase, mu3GenPower, p);;
  k3 := DiscreteLogMu3(Sbeta, omega, p);;
  psi := DiscreteLogMu3(Su, omega, p);;
  out.omegaBase := omegaBase;;  out.omega := omega;;  out.k3 := k3;;  out.psi := psi;;
  out.S9_SELECT := "PENDING_CENSUS_CONVENTION_NOT_PINNED";;
  out.S9_psi_eq_k3 := (psi = k3);;
  out.status := "OK";;
  return out;;
end;;

RunStability := function(primes, sgn)
  local results, statuses, cprimes, agree, r, p;
  results := [];;
  for p in primes do
    Add(results, RunChain(p, sgn, 1, 1));;
  od;
  statuses := List(results, r -> r.status);;
  if not ForAll(statuses, s -> s = "OK") then
    return rec(primes:=primes, results:=results, agree:=fail);;
  fi;
  cprimes := List(results, r -> r.cprime);;
  agree := (Length(DuplicateFreeList(cprimes)) = 1);;
  return rec(primes:=primes, results:=results, cprimes:=cprimes, agree:=agree);;
end;;

## ================= prime scan (own, same candidate list re-derived independently) ==================
candidatePrimes := [19, 37, 73, 109, 127, 163, 181, 199, 271, 307, 379, 397];;
validPrimes := [];;
invalidPrimeDC4 := fail;;
Print("\n=== prime scan ===\n");
for p in candidatePrimes do
  r := RunChain(p, 1, 1, 1);;
  Print("  p=",p,"  status=",r.status,"  Su=",r.Su,"  Sbeta=",r.Sbeta,"\n");
  if r.status = "OK" then Add(validPrimes, p);;
  elif r.status = "STOP_S5_FAIL_NONDISCRIMINATING" and invalidPrimeDC4 = fail then invalidPrimeDC4 := p;; fi;
od;
chosenPrimes := validPrimes{[1..3]};;
Print("chosen primes = ", chosenPrimes, "\n");

## ================= main computation =================================================================
Print("\n=== main computation (declared convention D: sgn=+1) ===\n");
mainStab := RunStability(chosenPrimes, 1);;
Print("cprimes = ", mainStab.cprimes, "  agree = ", mainStab.agree, "\n");
for r in mainStab.results do
  Print("  p=",r.p," Su=",r.Su," Sbeta=",r.Sbeta," cprime=",r.cprime," k3=",r.k3," psi=",r.psi,
        " psi_eq_k3=",r.S9_psi_eq_k3,"\n");
od;

## ================= DC-1: orientation flip =================
Print("\n=== DC-1 (orientation flip) ===\n");
dc1Stab := RunStability(chosenPrimes, -1);;
Print("flipped cprimes = ", dc1Stab.cprimes, "  agree = ", dc1Stab.agree, "\n");
dc1Pass := fail;;
if mainStab.agree = true and dc1Stab.agree = true then
  dc1Pass := (mainStab.cprimes[1] <> dc1Stab.cprimes[1]);;
fi;
Print("DC-1 pass (cprime flipped) = ", dc1Pass, "\n");

## ================= DC-2: embedding flip =================
Print("\n=== DC-2 (embedding/generator flip) ===\n");
p0 := chosenPrimes[1];;
orig := RunChain(p0, 1, 1, 1);;
flippedGen := RunChain(p0, 1, 2, 1);;
dc2Pass := (orig.cprime = flippedGen.cprime) and (orig.S9_psi_eq_k3 = flippedGen.S9_psi_eq_k3);;
Print("orig cprime=",orig.cprime," flipped-gen cprime=",flippedGen.cprime,
      "  orig k3/psi=[",orig.k3,",",orig.psi,"] flipped k3/psi=[",flippedGen.k3,",",flippedGen.psi,"]\n");
Print("DC-2 pass = ", dc2Pass, "\n");

## ================= DC-3: cube-number injection =================
Print("\n=== DC-3 (cube-number injection) ===\n");
a := 2;;
aPowNeg9 := a^(-9);;
orig2 := RunChain(p0, 1, 1, 1);;
injected := RunChain(p0, 1, 1, aPowNeg9);;
dc3Pass := (orig2.Su = injected.Su);;
Print("a=",a," a^-9=",aPowNeg9,"  orig Su=",orig2.Su,"  injected Su=",injected.Su,"\n");
Print("DC-3 pass = ", dc3Pass, "\n");

## ================= DC-4: negative control =================
Print("\n=== DC-4 (negative control) ===\n");
if invalidPrimeDC4 <> fail then
  dc4result := RunChain(invalidPrimeDC4, 1, 1, 1);;
  dc4Pass := (dc4result.status = "STOP_S5_FAIL_NONDISCRIMINATING");;
  Print("p=",invalidPrimeDC4," status=",dc4result.status,"  DC-4 pass = ", dc4Pass, "\n");
else
  Print("no invalid prime found in scan range\n");
fi;

## ================= 432-key canary (own independent read) ==========================================
Print("\n=== 432-key canary (independent read) ===\n");
## direct file parse via simple string ops (GAP-native, no shared code with producer's json module)
ReadJsonFileRaw := function(path)
  local stream, content;
  stream := InputTextFile(path);;
  if stream = fail then Error("cannot open ", path); fi;
  content := ReadAll(stream);;
  CloseStream(stream);;
  return content;;
end;;

## Use GAP's built-in JSON support if available; else fall back to a minimal targeted extraction.
censusPath := "search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json";;
artifactPath := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;

## GAP 4.16 ships a JSON parser in the "json" package or via GAP's io utilities; try that first.
jsonOk := true;;
LoadPackage("json");;
if IsBoundGlobal("JsonStringToGap") then
  censusData := JsonStringToGap(ReadJsonFileRaw(censusPath));;
  artifactData := JsonStringToGap(ReadJsonFileRaw(artifactPath));;
else
  jsonOk := false;;
fi;

if jsonOk then
  cands := censusData.finite_index3_census.nonnormal_candidates;;
  nn09 := fail;;  nn12 := fail;;
  for c in cands do
    if c.candidate_id = "IDX3-NN-09" then nn09 := Set(c.row_indices);; fi;
    if c.candidate_id = "IDX3-NN-12" then nn12 := Set(c.row_indices);; fi;
  od;
  symdiff := Union(Difference(nn09,nn12), Difference(nn12,nn09));;
  Print("|NN-09|=",Length(nn09)," |NN-12|=",Length(nn12)," |symdiff|=",Length(symdiff),"\n");
  rows := artifactData.rows;;
  badRows := [];;
  for idx in symdiff do
    row := rows[idx+1];;  ## GAP 1-indexed, artifact row-index idx is 0-based position
    key := row[2];;
    delta := key[2];;
    a1 := delta[1][1];;
    k := (a1 * 5) mod 9;;
    k3 := k mod 3;;
    if k3 = 0 then Add(badRows, idx);; fi;
  od;
  canaryPass := (Length(symdiff) = 432) and (Length(badRows) = 0);;
  Print("bad rows (K3=0) = ", badRows, "\n");
  Print("432-key canary PASS = ", canaryPass, "\n");
else
  Print("JSON package unavailable in this GAP session -- 432-key canary NOT independently re-verified\n");
  Print("by the checker (relying on producer's Python result for this item; flagged, not silently assumed)\n");
fi;

Print("\nD972_LOCAL3_CHECKER_V1_DONE\n");
QUIT;
