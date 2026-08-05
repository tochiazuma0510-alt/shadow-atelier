## search/probe/hsp7_mainrun/candidate_key_lib.g
## NEW file (enumeration wrapper component, individually digested -- NOT part
## of the judgement predicate libraries). Fixes the semantics of a HS
## main-run "candidate key", per Sol 便104 F104-1.2 item 4: the calibration
## prereg v1 left "index 0..117648 into [P,P]" without semantics, and warned
## against using Elements()/BFS order as shard identity. This file replaces
## that with an explicit, arithmetic (not GAP-internal-order-dependent)
## bijection.
##
## Dry-check status (implementer, 2026-08-05, scratchpad/dry_check_pcgs.g,
## same construction path as the calibration Lane S driver, zero of the
## 705,894 candidates evaluated): building P from
## search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g and taking D:=DerivedSubgroup(P)
## gives |P|=5764801=7^8, |D|=117649=7^6, Pcgs(D) has exactly 6 generators,
## RelativeOrders(Pcgs(D)) = [7,7,7,7,7,7]. This is exactly the "fixed pcgs
## (g1,...,g6), exponent vector in {0,...,6}^6" shape Sol's F104-1.2 item 4
## requires; it is not assumed, it is measured (same own_measurement
## discipline as the calibration drivers' S-7' checks).

Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");

## ---- fixed pcgs of D = [P,P] (candidate key basis) ----
## BuildCandidateBasis(): (re)builds P from the SAME PQ_OUTPUT artifact the
## calibration Lane S driver used, and returns the fixed pcgs of D. This is
## the ONLY place group construction happens for the candidate-key layer;
## lane wrappers call this once per shard job, not once per candidate.
## BasisFromP(Pgroup): derive the fixed candidate-key basis (pcgs of D=[P,P])
## from an ALREADY-BUILT group object Pgroup. This is the form lane wrappers
## must use: PQ_READ_AS_FUNC_WITH_VARS is NOT idempotent w.r.t. GAP object
## identity (re-reading PQ_OUTPUT_P.g via a second call constructs a fresh,
## merely-isomorphic copy, not `=`-equal to a prior build -- discovered
## during this bundle's own dry check, see lane_wrapper_S.g comment). Basing
## the candidate key on a SECOND independent build than the one the
## judgement predicate closes over would silently fork the universe (the
## predicate's P/theta/tau and the enumerator's element constructions would
## live in different, only-isomorphic group objects). BasisFromP forces
## both to share the SAME Pgroup object.
BasisFromP := function(Pgroup)
  local D, pcgsD;
  D := DerivedSubgroup(Pgroup);
  pcgsD := Pcgs(D);
  if Length(pcgsD) <> 6 then
    Error("CANDIDATE_KEY_BASIS_STOP: Pcgs(D) has ", Length(pcgsD),
          " generators, expected 6. Do not silently reshape the universe.");
  fi;
  if RelativeOrders(pcgsD) <> [7,7,7,7,7,7] then
    Error("CANDIDATE_KEY_BASIS_STOP: RelativeOrders(Pcgs(D)) = ", RelativeOrders(pcgsD),
          ", expected [7,7,7,7,7,7]. Do not silently reshape the universe.");
  fi;
  return rec(P := Pgroup, D := D, pcgsD := pcgsD, gens := List(pcgsD, x -> x));
end;;

## BuildCandidateBasis(): standalone convenience (rebuilds P fresh from
## PQ_OUTPUT_P.g and derives the basis from that fresh copy). Use this ONLY
## for isolated self-checks (e.g. scratchpad/dry_check_pcgs.g-style
## structural verification) that do not need to share a P object with a
## predicate library. Lane wrappers must use BasisFromP(P) instead (see
## above) so the candidate-key layer and the judgement predicate operate on
## the identical group object, not two isomorphic-but-distinct copies.
BuildCandidateBasis := function()
  local data;
  data := PQ_READ_AS_FUNC_WITH_VARS("search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g", ["F","MapImages"]);
  return BasisFromP(data.F);
end;;

## ---- X_N (main window m-set), fixed ascending order, m_index 0..5 ----
## Same formula as calibration drivers (Filtered([0..6], m -> Gcd(2*m+1,7)=1));
## re-derived here (not re-measured against a live group -- this is pure
## arithmetic on N_ord=7, which is itself a pinned NW-P3/P5 value, prereg v1
## SS1.1) so that XN_ORDERED is available without a group build.
XN_ORDERED := Filtered([0..6], m -> Gcd(2*m+1,7)=1);;
if Length(XN_ORDERED) <> 6 then
  Error("CANDIDATE_KEY_XN_STOP: |X_N| = ", Length(XN_ORDERED), ", expected 6.");
fi;

## ---- endian convention (explicit, per Sol F104-1.2 item 4) ----
## e := [e1,e2,e3,e4,e5,e6], each in {0,...,6}. e1 is the exponent of the
## FIRST pcgs generator (pcgsD[1]) and is the MOST-SIGNIFICANT digit of the
## base-7 flat index (standard positional big-endian: f_index below reduces
## to the usual base-7 numeral e1 e2 e3 e4 e5 e6 read left to right). The
## group element is the LEFT-TO-RIGHT product in generator order:
##   fbar(e) := g1^e1 * g2^e2 * g3^e3 * g4^e4 * g5^e5 * g6^e6
## with g_i = basis.gens[i] = pcgsD[i]. This is a pcgs normal form (Pcgs
## guarantees existence+uniqueness of this representation for elements of D
## when 0<=e_i<7), NOT an Elements()/BFS enumeration order.

ExpVectorToElement := function(basis, e)
  local i, acc;
  if Length(e) <> 6 then Error("bad exponent vector length"); fi;
  acc := One(basis.P);
  for i in [1..6] do
    if e[i] < 0 or e[i] > 6 then Error("exponent out of range at position ", i); fi;
    acc := acc * basis.gens[i]^e[i];
  od;
  return acc;
end;;

## f_index: base-7 flat index of exponent vector, e1 most significant digit,
## e6 least significant digit (big-endian). Range 0..117648.
ExpVectorToFIndex := function(e)
  return ((((e[1]*7+e[2])*7+e[3])*7+e[4])*7+e[5])*7+e[6];
end;;

FIndexToExpVector := function(idx)
  local e6,e5,e4,e3,e2,e1,rem;
  rem := idx;
  e6 := rem mod 7; rem := QuoInt(rem,7);
  e5 := rem mod 7; rem := QuoInt(rem,7);
  e4 := rem mod 7; rem := QuoInt(rem,7);
  e3 := rem mod 7; rem := QuoInt(rem,7);
  e2 := rem mod 7; rem := QuoInt(rem,7);
  e1 := rem mod 7;
  return [e1,e2,e3,e4,e5,e6];
end;;

## ---- pair flat index (candidate key -> single integer 0..705893) ----
## pair_index := m_index(m) * 117649 + f_index(e), where m_index(m) is the
## POSITION of m within XN_ORDERED (0-based), NOT m itself. This is the
## shard-identity index; shard manifests (shard_manifest_gen.py) partition
## [0, 705893] by this index, never by GAP Elements()/BFS order.
MIndexOfM := function(m)
  local pos;
  pos := Position(XN_ORDERED, m);
  if pos = fail then Error("m=", m, " not in X_N = ", XN_ORDERED); fi;
  return pos - 1;
end;;

CandidateKeyToPairIndex := function(m, e)
  return MIndexOfM(m) * 117649 + ExpVectorToFIndex(e);
end;;

PairIndexToCandidateKey := function(idx)
  local mIndex, fIndex;
  mIndex := QuoInt(idx, 117649);
  fIndex := idx mod 117649;
  return rec(m := XN_ORDERED[mIndex+1], e := FIndexToExpVector(fIndex), f_index := fIndex, m_index := mIndex);
end;;

## ---- Lane P optimization join receipt (Sol F104-1.5): f_key (117,649) ->
## six candidate_keys. For a fixed f_index, the 6 pair indices sharing it are
## { f_index + m_index*117649 : m_index in 0..5 }. This is the exact
## bijection the join checker (join_checker.py) verifies against actual
## per-shard cert output (post-run); here it is exposed as a pure function
## so the lane wrapper and the join checker call the SAME formula (no
## independent re-derivation drift).
FIndexToSixPairIndices := function(fIndex)
  local mIndex, out;
  out := [];
  for mIndex in [0..5] do
    Add(out, fIndex + mIndex*117649);
  od;
  return out;
end;;

## ---- self-check (dry, arithmetic only -- NOT a candidate evaluation) ----
CandidateKeyLibSelfCheck := function()
  local total, i, testE, testIdx, back;
  total := 6 * 117649;
  if total <> 705894 then Error("SELF_CHECK_STOP: 6*117649 <> 705894"); fi;
  ## round-trip on boundary + a few interior exponent vectors (pure arithmetic,
  ## no group element built, no predicate called -- structural bijection test)
  for testE in [ [0,0,0,0,0,0], [6,6,6,6,6,6], [1,0,0,0,0,0], [0,0,0,0,0,1], [3,1,4,1,5,2] ] do
    testIdx := ExpVectorToFIndex(testE);
    back := FIndexToExpVector(testIdx);
    if back <> testE then
      Error("SELF_CHECK_STOP: round-trip failed for e=", testE, " got back ", back);
    fi;
  od;
  if ExpVectorToFIndex([0,0,0,0,0,0]) <> 0 then Error("SELF_CHECK_STOP: zero vector != index 0"); fi;
  if ExpVectorToFIndex([6,6,6,6,6,6]) <> 117648 then Error("SELF_CHECK_STOP: all-6 vector != index 117648"); fi;
  for i in [1..6] do
    if MIndexOfM(XN_ORDERED[i]) <> i-1 then Error("SELF_CHECK_STOP: m_index mismatch at position ", i); fi;
  od;
  return rec(ok := true, total_candidates := total, xn_ordered := XN_ORDERED);
end;;

## Group-level semantic gate.  The arithmetic round-trip above cannot detect
## a producer that applies a common permutation to the pcgs generators while
## serializing the unpermuted exponent tuple.  Unit vectors must therefore
## map to the corresponding fixed pcgs generator, and every basis element
## must round-trip through ExponentsOfPcElement exactly.
CandidateBasisSemanticSelfCheck := function(basis)
  local i, e, elt, back;
  for i in [1..6] do
    e := [0,0,0,0,0,0];;
    e[i] := 1;;
    elt := ExpVectorToElement(basis, e);;
    if elt <> basis.gens[i] then
      Error("CANDIDATE_KEY_GROUP_STOP: unit vector maps to wrong pcgs generator at ", i);
    fi;
    back := ExponentsOfPcElement(basis.pcgsD, elt);;
    if back <> e then
      Error("CANDIDATE_KEY_GROUP_STOP: pcgs exponent round-trip failed at ", i,
            " expected ", e, " got ", back);
    fi;
  od;
  return rec(ok := true, unit_vectors_checked := 6);
end;;

## ---- deterministic runtime ordered-basis identity material ----
## A source-file digest and six unit-vector round trips do not identify the
## runtime ordered pcgs strongly enough.  The material below records the
## relative orders, all 15 pair-commutator coordinate rows, and the theta/tau
## action on every ordered generator.  Lane V additionally records the
## coordinate row of each Lane-S generator under the checked S->V bridge.
## No candidate is constructed or evaluated by this function.
HSPcgsCoordinates := function(basis, elt, label)
  local e;
  e := ExponentsOfPcElement(basis.pcgsD, elt);
  if e = fail or Length(e) <> 6 then
    Error("PCGS_BASIS_MATERIAL_STOP: ", label,
          " is outside the six-generator derived pcgs");
  fi;
  if not ForAll(e, z -> IsInt(z) and z >= 0 and z < 7) then
    Error("PCGS_BASIS_MATERIAL_STOP: noncanonical coordinate in ", label,
          ": ", e);
  fi;
  return e;
end;;

HSPcgsUnitVector := function(i)
  local e;
  e := [0,0,0,0,0,0];;
  e[i] := 1;;
  return e;
end;;

BuildCandidateBasisMaterial := function(basis, namedX, namedY, thetaMap, tauMap,
                                        bridgeData, sourceArtifactPath,
                                        sourceArtifactSha256)
  local pairRows, thetaRows, tauRows, bridgeRows, i, j, e, row,
        thetaNonidentity, tauNonidentity, ambientPcgs,
        ambientOrders, namedRows, basisAmbientRows;
  if thetaMap = fail or tauMap = fail or
     not IsBijective(thetaMap) or not IsBijective(tauMap) then
    Error("PCGS_BASIS_MATERIAL_STOP: theta/tau must be bijective maps");
  fi;
  if not IsString(sourceArtifactPath) or sourceArtifactPath = "" or
     not IsString(sourceArtifactSha256) or Length(sourceArtifactSha256) <> 64 then
    Error("PCGS_BASIS_MATERIAL_STOP: authoritative source artifact binding absent");
  fi;
  ambientPcgs := Pcgs(basis.P);;
  ambientOrders := RelativeOrders(ambientPcgs);;
  if Length(ambientPcgs) <> 8 or ambientOrders <> [7,7,7,7,7,7,7,7] then
    Error("PCGS_BASIS_MATERIAL_STOP: ambient Pcgs(P) shape differs from 7^8/8-generator anchor");
  fi;
  if not (namedX in basis.P) or not (namedY in basis.P) or
     Group([namedX,namedY]) <> basis.P then
    Error("PCGS_BASIS_MATERIAL_STOP: named x/y do not generate the runtime ambient P");
  fi;
  namedRows := [
    rec(name := "x", coordinates := ExponentsOfPcElement(ambientPcgs, namedX)),
    rec(name := "y", coordinates := ExponentsOfPcElement(ambientPcgs, namedY))
  ];;
  basisAmbientRows := [];;
  for i in [1..6] do
    e := ExponentsOfPcElement(ambientPcgs, basis.gens[i]);;
    if e = fail or Length(e) <> 8 or
       not ForAll(e, z -> IsInt(z) and z >= 0 and z < 7) then
      Error("PCGS_BASIS_MATERIAL_STOP: bad ambient coordinate for D generator ", i);
    fi;
    if ForAll(e, z -> z = 0) then
      Error("PCGS_BASIS_MATERIAL_STOP: identity ambient coordinate for D generator ", i);
    fi;
    Add(basisAmbientRows, rec(i := i, coordinates := e));
  od;
  if ForAny(namedRows, row -> row.coordinates = fail or
      Length(row.coordinates) <> 8 or
      not ForAll(row.coordinates, z -> IsInt(z) and z >= 0 and z < 7)) then
    Error("PCGS_BASIS_MATERIAL_STOP: bad named x/y ambient coordinate");
  fi;
  if ForAny(namedRows, row -> ForAll(row.coordinates, z -> z = 0)) or
     namedRows[1].coordinates = namedRows[2].coordinates then
    Error("PCGS_BASIS_MATERIAL_STOP: named x/y ambient anchor is trivial or colliding");
  fi;
  if Length(Set(List(basisAmbientRows, row -> row.coordinates))) <> 6 then
    Error("PCGS_BASIS_MATERIAL_STOP: ordered D generators collide in ambient coordinates");
  fi;
  pairRows := [];;
  for i in [1..5] do
    for j in [i+1..6] do
      e := HSPcgsCoordinates(basis, Comm(basis.gens[i], basis.gens[j]),
                            Concatenation("Comm(g",String(i),",g",String(j),")"));;
      Add(pairRows, rec(i := i, j := j, coordinates := e));
    od;
  od;
  thetaRows := [];; tauRows := [];;
  for i in [1..6] do
    Add(thetaRows, rec(i := i, coordinates := HSPcgsCoordinates(
      basis, ImageElm(thetaMap, basis.gens[i]),
      Concatenation("theta(g",String(i),")"))));
    Add(tauRows, rec(i := i, coordinates := HSPcgsCoordinates(
      basis, ImageElm(tauMap, basis.gens[i]),
      Concatenation("tau(g",String(i),")"))));
  od;
  bridgeRows := [];;
  if bridgeData <> fail then
    if not IsRecord(bridgeData) or not IsBound(bridgeData.source_basis) or
       not IsBound(bridgeData.map) then
      Error("PCGS_BASIS_MATERIAL_STOP: malformed S->V bridge data");
    fi;
    for i in [1..6] do
      e := HSPcgsCoordinates(basis,
        ImageElm(bridgeData.map, bridgeData.source_basis.gens[i]),
        Concatenation("S_to_V(g",String(i),")"));;
      if e <> HSPcgsUnitVector(i) then
        Error("PCGS_BASIS_MATERIAL_STOP: S->V bridge row is not pointwise unit at ", i,
              ": ", e);
      fi;
      Add(bridgeRows, rec(i := i, coordinates := e));
    od;
  fi;
  ## Here D=[P,P] is abelian (rank-2/class-4: [gamma2,gamma2] is
  ## trivial and [gamma2,gamma3] lies in gamma5), so the fifteen rows are
  ## expected identity data.  Requiring a nonzero row would reject the
  ## correct group.  Keep all rows serialized and fail if this expected
  ## structural identity changes.
  if ForAny(pairRows, row -> ForAny(row.coordinates, z -> z <> 0)) then
    Error("PCGS_BASIS_MATERIAL_STOP: D commutator row is nonzero; expected abelian D");
  fi;
  thetaNonidentity := ForAny(thetaRows,
    row -> row.coordinates <> HSPcgsUnitVector(row.i));;
  tauNonidentity := ForAny(tauRows,
    row -> row.coordinates <> HSPcgsUnitVector(row.i));;
  if not thetaNonidentity or not tauNonidentity then
    Error("PCGS_BASIS_MATERIAL_STOP: theta/tau action material collapsed to identity");
  fi;
  return rec(
    ambient_named_generator_coordinates := namedRows,
    ambient_pcgs_relative_orders := ambientOrders,
    contract := "hsp7-ordered-pcgs-material/v1",
    ordered_basis_in_ambient_coordinates := basisAmbientRows,
    relative_orders := RelativeOrders(basis.pcgsD),
    pair_commutator_coordinates := pairRows,
    theta_image_coordinates := thetaRows,
    tau_image_coordinates := tauRows,
    s_to_v_bridge_coordinates := bridgeRows,
    source_artifact := rec(path := sourceArtifactPath,
                           sha256 := sourceArtifactSha256)
  );
end;;

HSPcgsIntListJson := function(xs)
  local out, i;
  out := "[";
  for i in [1..Length(xs)] do
    if i > 1 then Append(out, ","); fi;
    Append(out, String(xs[i]));
  od;
  Append(out, "]");
  return out;
end;;

HSPcgsPairRowsJson := function(rows)
  local out, k, row;
  out := "[";
  for k in [1..Length(rows)] do
    if k > 1 then Append(out, ","); fi;
    row := rows[k];
    Append(out, Concatenation("{\"coordinates\":", HSPcgsIntListJson(row.coordinates),
      ",\"i\":", String(row.i), ",\"j\":", String(row.j), "}"));
  od;
  Append(out, "]");
  return out;
end;;

HSPcgsActionRowsJson := function(rows)
  local out, k, row;
  out := "[";
  for k in [1..Length(rows)] do
    if k > 1 then Append(out, ","); fi;
    row := rows[k];
    Append(out, Concatenation("{\"coordinates\":", HSPcgsIntListJson(row.coordinates),
      ",\"i\":", String(row.i), "}"));
  od;
  Append(out, "]");
  return out;
end;;

HSPcgsNamedRowsJson := function(rows)
  local out, k, row;
  out := "[";
  for k in [1..Length(rows)] do
    if k > 1 then Append(out, ","); fi;
    row := rows[k];
    Append(out, Concatenation("{\"coordinates\":", HSPcgsIntListJson(row.coordinates),
      ",\"name\":\"", row.name, "\"}"));
  od;
  Append(out, "]");
  return out;
end;;

CandidateBasisMaterialJson := function(material)
  ## Keys are emitted in lexical order, identical to Python
  ## json.dumps(sort_keys=True,separators=(",",":")) after parsing.
  return Concatenation(
    "{\"ambient_named_generator_coordinates\":",
      HSPcgsNamedRowsJson(material.ambient_named_generator_coordinates),
    ",\"ambient_pcgs_relative_orders\":", HSPcgsIntListJson(material.ambient_pcgs_relative_orders),
    ",\"contract\":\"", material.contract, "\"",
    ",\"ordered_basis_in_ambient_coordinates\":",
      HSPcgsActionRowsJson(material.ordered_basis_in_ambient_coordinates),
    ",\"pair_commutator_coordinates\":", HSPcgsPairRowsJson(material.pair_commutator_coordinates),
    ",\"relative_orders\":", HSPcgsIntListJson(material.relative_orders),
    ",\"s_to_v_bridge_coordinates\":", HSPcgsActionRowsJson(material.s_to_v_bridge_coordinates),
    ",\"source_artifact\":{\"path\":\"", material.source_artifact.path,
      "\",\"sha256\":\"", material.source_artifact.sha256, "\"}",
    ",\"tau_image_coordinates\":", HSPcgsActionRowsJson(material.tau_image_coordinates),
    ",\"theta_image_coordinates\":", HSPcgsActionRowsJson(material.theta_image_coordinates),
    "}"
  );
end;;

WriteCandidateBasisMaterial := function(path, material)
  local out;
  out := OutputTextFile(path, false);
  if out = fail then Error("PCGS_BASIS_MATERIAL_STOP: cannot open ", path); fi;
  SetPrintFormattingStatus(out, false);
  PrintTo(out, CandidateBasisMaterialJson(material), "\n");
  CloseStream(out);
end;;
