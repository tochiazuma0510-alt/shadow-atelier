#############################################################################
## search/probe/sg_band_sweep/sg_pband2_driver_v1.g
## P-BAND-2 test (裁定677 小任務): for each of the 36 G4/G5 windows, search
## for a CYCLIC CHARACTERISTIC SECTION A of Ghat (Aut(A) automatically
## abelian since A is cyclic) on which W (= the order-3 generator s, image
## of delta) acts NON-trivially by conjugation.
## Design authority (verbatim, not invented here):
##   docs/notes/theorem_check_mirrorall_l3vacuous_v1.md SSG.7.2 P-BAND-2
##   (数学者 #1 起草, id 4109b3e).
## Prediction under test (scored by 司令塔, NOT graded here):
##   - the 5 "chiral" windows (single_mirror_pair_non_exotic in G5) SHOULD
##     have such a section (W acts nontrivially somewhere).
##   - the 31 "reflexible" windows (isolated_self_mirror_no_twin in G5)
##     SHOULD NOT (W centralizes every cyclic characteristic section).
##
## Method: chars := CharacteristicSubgroups(Ghat) (all characteristic
## subgroups). For every pair (K,H) with K,H in chars, K a proper subgroup
## of H, Q:=H/K cyclic and nontrivial: test whether conjugation by s
## induces a nontrivial automorphism of Q (i.e. exists a generator q0 of Q
## with q0^s <> q0 in Q). If found for ANY such pair, P-BAND-2 = EXISTS
## (record one witness); else NOT_EXISTS.
##
## (r,s) per window: independently rediscovered exactly as in
## sg_g4_orb_driver_v1.g's entry gate (fresh scan, not reused from any
## stored witness) -- search/crosscheck separation preserved even between
## this script and the earlier G4/G5 driver.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;

INPUT_CERT_PATH := "search/certs/sg_g4_g5_orb_20260806.json";;
S3grp := SymmetricGroup(3);;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_pband2_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

#############################################################################
## PART 0 -- minimal JSON extraction: (order,id,classification) from
## g5_classification[] of the G4/G5 cert.
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
## PART 1 -- entry gate (fresh rediscovery, same method as G4)
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
## PART 2 -- P-BAND-2 per window
#############################################################################
PBand2Test := function(Ghat, s)
  ## returns rec(exists:=bool, witness:=rec or fail)
  local chars, K, H, Q, hom, gensQ, q0, i, j, preq0, conj, imgQ;
  chars := CharacteristicSubgroups(Ghat);;
  for i in [1..Length(chars)] do
    for j in [1..Length(chars)] do
      if i = j then continue; fi;
      K := chars[i];; H := chars[j];;
      if Size(K) >= Size(H) then continue; fi;
      if not IsSubgroup(H,K) then continue; fi;
      if not IsNormal(H,K) then continue; fi;   ## needed to form H/K
      hom := NaturalHomomorphismByNormalSubgroup(H,K);;
      Q := Image(hom);;   ## bugfix: use Image(hom), NOT the separately-constructed H/K
                           ## (H/K and Image(hom) are isomorphic but distinct GAP objects;
                           ## PreImagesRepresentative(hom,.) requires elements of Image(hom))
      if Size(Q) <= 1 or not IsCyclic(Q) then continue; fi;
      gensQ := GeneratorsOfGroup(Q);;
      for q0 in gensQ do
        if Order(q0) = Size(Q) then   ## a genuine generator of the cyclic group
          ## lift q0 to H, conjugate by s (s in Ghat; conjugation of an H-elt
          ## by s only makes sense if s normalizes H -- H is characteristic,
          ## hence normal, hence s (in Ghat) normalizes it automatically).
          preq0 := PreImagesRepresentative(hom, q0);;
          conj := preq0^s;;
          imgQ := Image(hom, conj);;
          if imgQ <> q0 then
            return rec(exists := true, witness := rec(
                H_order := Size(H), K_order := Size(K), Q_order := Size(Q),
                q0 := String(q0), s_image := String(imgQ)));
          fi;
        fi;
      od;
    od;
  od;
  return rec(exists := false, witness := fail);
end;;

RESULTS := [];;
HANDOFF_MISMATCHES := [];;

for w in WINDOWS do
  Print("\n=== P-BAND-2 window (", w.order, ",", w.id, ") [", w.classification, "] ===\n");
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
  pb2 := PBand2Test(Ghat, entry.s);;
  Print("  P-BAND-2 = ", (function() if pb2.exists then return "EXISTS"; else return "NOT_EXISTS"; fi; end)(), "\n");
  if pb2.exists then
    Print("    witness: |H|=", pb2.witness.H_order, " |K|=", pb2.witness.K_order,
          " |Q|=", pb2.witness.Q_order, " q0=", pb2.witness.q0, " s-image=", pb2.witness.s_image, "\n");
  fi;

  is_chiral := (w.classification = "single_mirror_pair_non_exotic");;
  expected := is_chiral;;   ## chiral -> predicted EXISTS(true); reflexible -> predicted NOT_EXISTS(false)
  matches_prediction := (pb2.exists = expected);;
  Print("    chiral=", is_chiral, " predicted_exists=", expected, " actual_exists=", pb2.exists,
        " matches_prediction=", matches_prediction, "\n");

  Add(RESULTS, rec(order := w.order, id := w.id, classification := w.classification,
      is_chiral := is_chiral, pband2_exists := pb2.exists, witness := pb2.witness,
      matches_prediction := matches_prediction));;
od;;

Print("\n=== P-BAND-2 summary ===\n");
nMatch := Length(Filtered(RESULTS, r -> r.matches_prediction));;
nMismatch := Length(Filtered(RESULTS, r -> not r.matches_prediction));;
Print("windows processed: ", Length(RESULTS), " / ", Length(WINDOWS), "\n");
Print("HANDOFF_MISMATCHES: ", Length(HANDOFF_MISMATCHES), "\n");
Print("prediction matches: ", nMatch, " / ", Length(RESULTS), " (mismatches: ", nMismatch, ")\n");
for r in Filtered(RESULTS, r -> not r.matches_prediction) do
  Print("  MISMATCH: (", r.order, ",", r.id, ") classification=", r.classification,
        " pband2_exists=", r.pband2_exists, "\n");
od;

#############################################################################
## PART 3 -- cert output
#############################################################################
WitnessJson := function(w)
  if w = fail then return "null"; fi;
  return Concatenation("{\"H_order\":", String(w.H_order), ",\"K_order\":", String(w.K_order),
      ",\"Q_order\":", String(w.Q_order), ",\"q0\":", JStr(w.q0), ",\"s_image\":", JStr(w.s_image), "}");
end;;

RowsJson := JArr(List(RESULTS, r -> Concatenation(
    "{\"order\":", String(r.order), ",\"id\":", String(r.id),
    ",\"classification\":", JStr(r.classification), ",\"is_chiral\":", JB(r.is_chiral),
    ",\"pband2_exists\":", JB(r.pband2_exists), ",\"witness\":", WitnessJson(r.witness),
    ",\"matches_prediction\":", JB(r.matches_prediction), "}")));;

HandoffJson := JArr(List(HANDOFF_MISMATCHES, w -> Concatenation(
    "{\"order\":", String(w.order), ",\"id\":", String(w.id), "}")));;

selfSha := ComputeSha256File("search/probe/sg_band_sweep/sg_pband2_driver_v1.g");;
inputCertSha := ComputeSha256File(INPUT_CERT_PATH);;
preregNoteSha := ComputeSha256File("docs/notes/theorem_check_mirrorall_l3vacuous_v1.md");;

cert := Concatenation(
"{\n",
"\"schema\":\"shadow-atelier/sg-pband2/v1\",\n",
"\"driver_self_sha256\":", JStr(selfSha), ",\n",
"\"authority\":\"裁定677 (司令塔), P-BAND-2 per docs/notes/theorem_check_mirrorall_l3vacuous_v1.md SSG.7.2 (verbatim, 数学者#1起草)\",\n",
"\"design_doc\":{\"path\":\"docs/notes/theorem_check_mirrorall_l3vacuous_v1.md\",\"sha256\":", JStr(preregNoteSha), "},\n",
"\"input_cert\":{\"path\":", JStr(INPUT_CERT_PATH), ",\"sha256\":", JStr(inputCertSha), "},\n",
"\"windows_total\":", String(Length(WINDOWS)), ",\n",
"\"windows_processed\":", String(Length(RESULTS)), ",\n",
"\"handoff_mismatches\":", HandoffJson, ",\n",
"\"method_note\":\"chars := CharacteristicSubgroups(Ghat); for all pairs (K,H) in chars with K normal in H and H/K cyclic nontrivial, test whether conjugation by s (the independently-rediscovered order-3 generator) is nontrivial on a generator of H/K. EXISTS if any such pair witnesses nontrivial action.\",\n",
"\"rows\":", RowsJson, ",\n",
"\"prediction_summary\":{\"total_matches\":", String(nMatch), ",\"total_mismatches\":", String(nMismatch),
  ",\"note\":\"prediction = chiral(5)->EXISTS, reflexible(31)->NOT_EXISTS, per theorem_check SSG.7.2; grading of match/mismatch as confirming or falsifying MIRROR-ODD' is 司令塔/数学者's call, not this driver's\"},\n",
"\"claims\":{\"mirror_odd_prime_verdict\":\"UNKNOWN\",\"note\":\"raw measurement only; theorem status of MIRROR-ODD' is not asserted here\"},\n",
"\"non_contact_declaration\":{\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"n5_series\":false}\n",
"}\n");;

OUT_PATH := "search/certs/sg_pband2_20260806.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nW6_SG_PBAND2_DONE\n");
QUIT;
