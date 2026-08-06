#############################################################################
## search/probe/sg_band_sweep/sg_pband2prime_driver_v1.g
## P-BAND-2' (SECT predicate) test (裁定679 小任務): for each of the 36
## G4/G5 windows, test the judgement formula SECT on EVERY chief factor
## (elementary abelian p^d, p in {2,3}).
## Design authority (verbatim, not invented here):
##   docs/notes/theorem_check_mirrorall_l3vacuous_v1.md SSG.8.3 (P-BAND-2',
##   数学者#1起草, id d233e87), which rescues the "necessary condition of
##   iota(N)=N" formula SECT after P-BAND-2 (cyclic-only) was rejected
##   (0/5 on the chiral side, 11e94cc).
##
## SECT (verbatim): A a chief factor of Ghat, mu:Ghat->Aut(A)=GL(d,p) the
## conjugation action. iota(N)=N implies:
##   exists h in Aut(A): h*mu(U)*h^-1 = mu(U)  AND  h*mu(W)*h^-1 = mu(W)^-1
## i.e. (mu(U),mu(W)) and (mu(U),mu(W)^-1) are SIMULTANEOUSLY conjugate in
## GL(d,p). Implemented as: C := Centralizer(GL(d,p), mu(U)); SECT holds
## iff IsConjugate(C, mu(W), mu(W)^-1) (h must ALSO centralize mu(U), so h
## ranges over C, not all of GL(d,p) -- this is the correct reduction, not
## a shortcut: any h satisfying both conditions lies in C by definition of
## centralizer, and conversely any h in C conjugating mu(W) to mu(W)^-1
## satisfies both conditions).
##
## Predicted structure (scored by 司令塔, not graded here):
##   (i)  31 reflexible windows: SECT holds on EVERY chief factor (necessary
##        condition of iota(N)=N -- an IMPLEMENTATION HEALTH CHECK, not a
##        real test, since these ARE iota-fixed by construction/G7.1).
##   (ii) 5 chiral windows: SECT should FAIL on at least one chief factor
##        (the real test -- THIS is where information lives).
##   (iii) if the 5 chiral windows also pass on every factor: chirality is
##        undetectable by chief-factor-local invariants (a real, informative
##        negative result per SSG.8.3, not a bug).
##
## (r,s)=(U,W) per window: independently rediscovered exactly as in
## sg_g4_orb_driver_v1.g / sg_pband2_driver_v1.g's entry gate.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;

INPUT_CERT_PATH := "search/certs/sg_g4_g5_orb_20260806.json";;
S3grp := SymmetricGroup(3);;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_pband2p_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

#############################################################################
## PART 0 -- minimal JSON extraction: (order,id,classification)
#############################################################################
ReadWholeFile := function(path)
  local f, s;
  f := InputTextFile(path);
  if f = fail then Error("cannot open ", path); fi;
  s := ReadAll(f); CloseStream(f);
  return s;
end;;

ExtractArrayBlock := function(content, key)
  local mk, pos, depth, i, c, startIdx;
  mk := Concatenation("\"", key, "\":[");
  pos := PositionSublist(content, mk);
  if pos = fail then Error("array marker not found: ", key); fi;
  startIdx := pos + Length(mk) - 1;
  depth := 1; i := startIdx;
  while depth > 0 do
    i := i + 1; c := content[i];
    if c = '[' then depth := depth + 1; fi;
    if c = ']' then depth := depth - 1; fi;
  od;
  return content{[startIdx .. i-1]};
end;;

SplitTopLevelObjects := function(s)
  local objs, depth, i, startIdx, c;
  objs := []; depth := 0; startIdx := fail;
  for i in [1..Length(s)] do
    c := s[i];
    if c = '{' then
      if depth = 0 then startIdx := i; fi;
      depth := depth + 1;
    elif c = '}' then
      depth := depth - 1;
      if depth = 0 then Add(objs, s{[startIdx..i]}); fi;
    fi;
  od;
  return objs;
end;;

ExtractIntField := function(obj, key)
  local mk, pos, j, digitStr;
  mk := Concatenation("\"", key, "\":");
  pos := PositionSublist(obj, mk);
  if pos = fail then Error("key not found: ", key); fi;
  j := pos + Length(mk); digitStr := "";
  while j <= Length(obj) and obj[j] in "0123456789" do Append(digitStr,[obj[j]]); j:=j+1; od;
  return Int(digitStr);
end;;

ExtractStrField := function(obj, key)
  local mk, pos, j, k;
  mk := Concatenation("\"", key, "\":\"");
  pos := PositionSublist(obj, mk);
  if pos = fail then Error("key not found: ", key); fi;
  j := pos + Length(mk); k := j;
  while obj[k] <> '"' do k := k + 1; od;
  return obj{[j..k-1]};
end;;

certContent := ReadWholeFile(INPUT_CERT_PATH);;
g5Block := ExtractArrayBlock(certContent, "g5_classification");;
g5Objs := SplitTopLevelObjects(g5Block);;
WINDOWS := List(g5Objs, obj -> rec(order := ExtractIntField(obj,"order"), id := ExtractIntField(obj,"id"),
    classification := ExtractStrField(obj,"classification")));;
Print("Loaded ", Length(WINDOWS), " windows from ", INPUT_CERT_PATH, "\n");

#############################################################################
## PART 1 -- entry gate (fresh rediscovery, same method as G4/P-BAND-2)
#############################################################################
G1_Test := function(Ghat)
  local ab;
  ab := AbelianInvariants(Ghat);;
  return ab in [[2],[2,3],[6]];
end;;

FindOneG2G3Pair := function(Ghat)
  local invs, ord3, r, s, sz, quots;
  invs := Filtered(Elements(Ghat), x -> Order(x) = 2);;
  ord3 := Filtered(Elements(Ghat), x -> Order(x) = 3);;
  sz := Size(Ghat);;
  for r in invs do
    for s in ord3 do
      if Size(Subgroup(Ghat,[r,s])) = sz then
        quots := GQuotients(Ghat, S3grp);;
        if Length(quots) > 0 then
          return rec(ok := true, r := r, s := s);
        else
          return rec(ok := false);
        fi;
      fi;
    od;
  od;
  return rec(ok := false);
end;;

#############################################################################
## PART 2 -- chief factor action matrices + SECT test
#############################################################################
## Builds the conjugation-action matrix of g on the chief factor N_i/N_ip1
## (N_ip1 normal in N_i, both normal in Ghat -- standard chief series terms)
## over GF(p), using the pcgs-of-the-factor-group basis (same pattern as
## the AdMatrixOverGF5 helper used in w6_bu_s35_driver_v2.g).
ActionMatrixOnFactor := function(Ghat, Ni, Nip1, hom, isoQpc, pcgsQ, p, g)
  local rows, i, qbarPc, qbar, qNi, conj, imgQ, imgQpc, expv;
  rows := [];;
  for i in [1..Length(pcgsQ)] do
    qbarPc := pcgsQ[i];;
    qbar := PreImagesRepresentative(isoQpc, qbarPc);;
    qNi := PreImagesRepresentative(hom, qbar);;
    conj := qNi^g;;
    imgQ := Image(hom, conj);;
    imgQpc := Image(isoQpc, imgQ);;
    expv := ExponentsOfPcElement(pcgsQ, imgQpc);;
    Add(rows, expv * Z(p)^0);;
  od;
  return rows;
end;;

SectTestAllFactors := function(Ghat, r, s)
  ## returns rec(factors := list of rec(p,d,sect_holds), all_pass := bool,
  ##              first_fail_index := int or fail)
  local series, factorRecs, i, Ni, Nip1, hom, Q, order, p, d, isoQpc, Qpc,
        pcgsQ, muU, muW, muWinv, GLdp, C, sectHolds, allPass, firstFail;
  series := ChiefSeries(Ghat);;
  factorRecs := [];;
  allPass := true;; firstFail := fail;;
  for i in [1..Length(series)-1] do
    Ni := series[i];; Nip1 := series[i+1];;
    if Size(Ni) = Size(Nip1) then continue; fi;   ## skip degenerate/repeat terms if any
    hom := NaturalHomomorphismByNormalSubgroup(Ni, Nip1);;
    Q := Image(hom);;
    order := Size(Q);;
    if order = 1 then continue; fi;
    p := SmallestRootInt(order);;   ## factor is elementary abelian p^d
    if not IsPrimeInt(p) then
      ## defensive: should never happen for a genuine chief factor of a
      ## solvable group, but record and skip rather than crash
      Add(factorRecs, rec(p := fail, d := fail, order := order, sect_holds := fail,
          note := "non-elementary-abelian factor encountered (unexpected)"));;
      continue;
    fi;
    d := LogInt(order, p);;
    isoQpc := IsomorphismPcGroup(Q);;
    Qpc := Image(isoQpc);;
    pcgsQ := Pcgs(Qpc);;
    muU := ActionMatrixOnFactor(Ghat, Ni, Nip1, hom, isoQpc, pcgsQ, p, r);;
    muW := ActionMatrixOnFactor(Ghat, Ni, Nip1, hom, isoQpc, pcgsQ, p, s);;
    GLdp := GL(d, p);;
    muU := ImmutableMatrix(GF(p), muU);;
    muW := ImmutableMatrix(GF(p), muW);;
    muWinv := muW^-1;;
    C := Centralizer(GLdp, muU);;
    sectHolds := IsConjugate(C, muW, muWinv);;
    Add(factorRecs, rec(p := p, d := d, order := order, sect_holds := sectHolds));;
    if not sectHolds and firstFail = fail then firstFail := Length(factorRecs); fi;
    if not sectHolds then allPass := false; fi;
  od;
  return rec(factors := factorRecs, all_pass := allPass, first_fail_index := firstFail);
end;;

RESULTS := [];;
HANDOFF_MISMATCHES := [];;

for w in WINDOWS do
  Print("\n=== P-BAND-2' window (", w.order, ",", w.id, ") [", w.classification, "] ===\n");
  Ghat := SmallGroup(w.order, w.id);;
  if not G1_Test(Ghat) then
    Print("  HANDOFF_MISMATCH\n");
    Add(HANDOFF_MISMATCHES, w);;
    continue;
  fi;
  entry := FindOneG2G3Pair(Ghat);;
  if not entry.ok then
    Print("  HANDOFF_MISMATCH\n");
    Add(HANDOFF_MISMATCHES, w);;
    continue;
  fi;

  sect := SectTestAllFactors(Ghat, entry.r, entry.s);;
  Print("  chief factors: ", Length(sect.factors), " types: ",
        List(sect.factors, f -> Concatenation(String(f.p),"^",String(f.d))), "\n");
  Print("  SECT per factor: ", List(sect.factors, f -> f.sect_holds), "\n");
  Print("  all_pass = ", sect.all_pass, "\n");

  is_chiral := (w.classification = "single_mirror_pair_non_exotic");;
  ## prediction: reflexible -> all_pass=true (health check); chiral -> at
  ## least one factor fails, i.e. all_pass=false, is the "real" prediction
  predicted_all_pass := not is_chiral;;
  matches_prediction := (sect.all_pass = predicted_all_pass);;
  Print("    is_chiral=", is_chiral, " predicted_all_pass=", predicted_all_pass,
        " actual_all_pass=", sect.all_pass, " matches_prediction=", matches_prediction, "\n");

  Add(RESULTS, rec(order := w.order, id := w.id, classification := w.classification,
      is_chiral := is_chiral, factors := sect.factors, all_pass := sect.all_pass,
      first_fail_index := sect.first_fail_index, matches_prediction := matches_prediction));;
od;;

Print("\n=== P-BAND-2' summary ===\n");
nMatch := Length(Filtered(RESULTS, r -> r.matches_prediction));;
nMismatch := Length(Filtered(RESULTS, r -> not r.matches_prediction));;
reflAll := Filtered(RESULTS, r -> not r.is_chiral);;
chirAll := Filtered(RESULTS, r -> r.is_chiral);;
reflHealthOk := Length(Filtered(reflAll, r -> r.all_pass)) = Length(reflAll);;
chirBroken := Length(Filtered(chirAll, r -> not r.all_pass));;
Print("windows processed: ", Length(RESULTS), " / ", Length(WINDOWS), "\n");
Print("HANDOFF_MISMATCHES: ", Length(HANDOFF_MISMATCHES), "\n");
Print("reflexible health check: ", Length(Filtered(reflAll,r->r.all_pass)), " / ", Length(reflAll), " all_pass\n");
Print("chiral real test: ", chirBroken, " / ", Length(chirAll), " have >=1 failing factor\n");
Print("overall prediction matches: ", nMatch, " / ", Length(RESULTS), "\n");

#############################################################################
## PART 3 -- cert output
#############################################################################
FactorsJson := function(factors)
  return JArr(List(factors, f -> Concatenation(
      "{\"p\":", (function() if f.p=fail then return "null"; else return String(f.p); fi; end)(),
      ",\"d\":", (function() if f.d=fail then return "null"; else return String(f.d); fi; end)(),
      ",\"order\":", String(f.order),
      ",\"sect_holds\":", (function() if f.sect_holds=fail then return "null"; else return JB(f.sect_holds); fi; end)(),
      "}")));
end;;

RowsJson := JArr(List(RESULTS, r -> Concatenation(
    "{\"order\":", String(r.order), ",\"id\":", String(r.id),
    ",\"classification\":", JStr(r.classification), ",\"is_chiral\":", JB(r.is_chiral),
    ",\"num_chief_factors\":", String(Length(r.factors)),
    ",\"factors\":", FactorsJson(r.factors),
    ",\"all_pass\":", JB(r.all_pass),
    ",\"first_fail_index\":", (function() if r.first_fail_index=fail then return "null"; else return String(r.first_fail_index); fi; end)(),
    ",\"matches_prediction\":", JB(r.matches_prediction), "}")));;

HandoffJson := JArr(List(HANDOFF_MISMATCHES, w -> Concatenation(
    "{\"order\":", String(w.order), ",\"id\":", String(w.id), "}")));;

selfSha := ComputeSha256File("search/probe/sg_band_sweep/sg_pband2prime_driver_v1.g");;
inputCertSha := ComputeSha256File(INPUT_CERT_PATH);;
noteSha := ComputeSha256File("docs/notes/theorem_check_mirrorall_l3vacuous_v1.md");;

cert := Concatenation(
"{\n",
"\"schema\":\"shadow-atelier/sg-pband2prime/v1\",\n",
"\"driver_self_sha256\":", JStr(selfSha), ",\n",
"\"authority\":\"裁定679 (司令塔), P-BAND-2' / SECT predicate per docs/notes/theorem_check_mirrorall_l3vacuous_v1.md SSG.8.3 (verbatim, 数学者#1起草, id d233e87)\",\n",
"\"design_doc\":{\"path\":\"docs/notes/theorem_check_mirrorall_l3vacuous_v1.md\",\"sha256\":", JStr(noteSha), "},\n",
"\"input_cert\":{\"path\":", JStr(INPUT_CERT_PATH), ",\"sha256\":", JStr(inputCertSha), "},\n",
"\"windows_total\":", String(Length(WINDOWS)), ",\n",
"\"windows_processed\":", String(Length(RESULTS)), ",\n",
"\"handoff_mismatches\":", HandoffJson, ",\n",
"\"method_note\":\"for each window: ChiefSeries(Ghat) gives elementary-abelian p^d chief factors; mu(U),mu(W) computed as GF(p) matrices via the conjugation action on each factor (pcgs-basis pattern); SECT tested as IsConjugate(Centralizer(GL(d,p),mu(U)), mu(W), mu(W)^-1). (U,W)=(r,s) independently rediscovered per window (not reused from any stored witness).\",\n",
"\"rows\":", RowsJson, ",\n",
"\"prediction_summary\":{\n",
"  \"reflexible_count\":", String(Length(reflAll)), ",\n",
"  \"reflexible_all_pass_count\":", String(Length(Filtered(reflAll,r->r.all_pass))), ",\n",
"  \"reflexible_health_check_ok\":", JB(reflHealthOk), ",\n",
"  \"chiral_count\":", String(Length(chirAll)), ",\n",
"  \"chiral_broken_count\":", String(chirBroken), ",\n",
"  \"total_matches\":", String(nMatch), ",\"total_mismatches\":", String(nMismatch), ",\n",
"  \"note\":\"(i) reflexible must ALL be all_pass=true (health check, not a real test -- per SSG.8.3). (ii) chiral SHOULD have all_pass=false (>=1 failing factor) -- the real test. (iii) if chiral_broken_count=0 (all 5 chiral pass every factor too), that is the informative negative result 'chirality undetectable by chief-factor-local invariants' per SSG.8.3, NOT a driver bug. Grading is 司令塔/数学者's call, not this driver's.\"\n",
"},\n",
"\"claims\":{\"mirror_odd_prime_verdict\":\"UNKNOWN\",\"note\":\"raw measurement only\"},\n",
"\"non_contact_declaration\":{\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"n5_series\":false}\n",
"}\n");;

OUT_PATH := "search/certs/sg_pband2prime_20260806.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nW6_SG_PBAND2PRIME_DONE\n");
QUIT;
