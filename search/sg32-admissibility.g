# sg32-admissibility.g -- B3-admissibility judgement for (4,4,4)-marked F2-quotients
# of order 32.
#
# Usage: .\gap.ps1 search\sg32-admissibility.g
#
# Task (commander order, "SG(32,6) 新窓候補の B3-許容性判定・裁定 19 追記"):
#   search/smallgroup32-scan.g found that besides G4 = SmallGroup(32,2) (1 kernel,
#   already the known window K^(4)), SmallGroup(32,6) = (C2xC2xC2):C4 also carries
#   (4,4,4)-marked F2-quotients, with N_6 = 192 generating pairs falling into
#   N_6/|Aut(G6)| = 192/64 = 3 Aut-orbits (= 3 candidate kernels).
#
#   For a candidate kernel to be a genuine "window" in NFI_PB3(B3), the F2-part must
#   be B3-admissible: the outer automorphisms
#     theta: x |-> y, y |-> x
#     tau  : x |-> y, y |-> (xy)^-1
#   of F2 must descend to automorphisms of the quotient, i.e. must preserve the
#   kernel. Working at marked-pair level (no need to construct the kernel itself):
#   a marked pair (a,b) generating G together with its Aut(G)-orbit represents one
#   kernel; theta preserves that kernel iff the transformed pair (b,a) lies in the
#   SAME Aut(G)-orbit as (a,b); likewise tau iff (b,(ab)^-1) lies in the same orbit.
#   (Sol 罠回避: this is a marked-pair / Aut(G)-orbit membership test, not a raw GAP
#   subgroup-containment comparison -- consistent with 裁定_18/19's "marked factor
#   map, not naive subgroup comparison" constraint.)
#
#   Do this for G6 = SmallGroup(32,6) (3 orbits, the new candidate) and, as a
#   calibration check, for G4 = SmallGroup(32,2) (1 orbit, the known admissible
#   window K^(4) -- if this FAILS it signals an implementation bug, not a
#   mathematical fact about K^(4)).
#
# Universe (pre-registered, not to be widened/narrowed here): exactly the two
# SmallGroup(32,i) already flagged nonzero by search/smallgroup32-scan.g, namely
# i=2 (G4, calibration) and i=6 (G6, the object under judgement). No other i.

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= JSON helpers (copied verbatim from smallgroup32-scan.g) =================
JStr := function(s) return Concatenation("\"", s, "\""); end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;
JoinC := function(strs, sep)
  local r, i;
  if Length(strs) = 0 then return ""; fi;
  r := strs[1];
  for i in [2..Length(strs)] do r := Concatenation(r, sep, strs[i]); od;
  return r;
end;;
JArr := function(items) return Concatenation("[", JoinC(items, ","), "]"); end;;

WriteFile := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

# ================================================================================
# Core routine: given a group G, enumerate all (4,4,4)-marked generating pairs,
# split into Aut(G)-orbits, and for each orbit representative test theta/tau
# admissibility via orbit-membership of the transformed pair.
# ================================================================================

AnalyzeGroup := function(G, label)
  local elts, pairs, a, b, AutG, ActOnPair, remaining, orbitsList, rep, orb,
        thetaPair, tauPair, thetaOk, tauOk, orbitRecs, r2, i;

  elts := Elements(G);
  pairs := [];
  for a in elts do
    if Order(a) <> 4 then continue; fi;
    for b in elts do
      if Order(b) <> 4 then continue; fi;
      if Order(a*b) <> 4 then continue; fi;
      if Size(Subgroup(G, [a,b])) = Size(G) then
        Add(pairs, [a,b]);
      fi;
    od;
  od;

  AutG := AutomorphismGroup(G);;

  ActOnPair := function(pt, phi)
    return [Image(phi, pt[1]), Image(phi, pt[2])];
  end;;

  # split pairs into Aut(G)-orbits
  remaining := ShallowCopy(pairs);
  orbitsList := [];
  while Length(remaining) > 0 do
    rep := remaining[1];
    orb := Orbit(AutG, rep, ActOnPair);
    Add(orbitsList, orb);
    remaining := Filtered(remaining, p -> not (p in orb));
  od;

  Print("== ", label, " (|G|=", Size(G), ", IdGroup=", IdGroup(G), ") ==\n");
  Print("  |Aut(G)| = ", Size(AutG), "\n");
  Print("  #(4,4,4)-marked pairs = ", Length(pairs), "\n");
  Print("  #Aut-orbits = ", Length(orbitsList), "\n");

  orbitRecs := [];
  for i in [1..Length(orbitsList)] do
    orb := orbitsList[i];
    rep := orb[1];
    a := rep[1]; b := rep[2];
    thetaPair := [b, a];
    tauPair := [b, (a*b)^-1];
    thetaOk := thetaPair in orb;
    tauOk := tauPair in orb;
    Print("  orbit ", i, ": size=", Length(orb),
          "  theta=", PF(thetaOk), "  tau=", PF(tauOk),
          "  both=", PF(thetaOk and tauOk), "\n");
    Add(orbitRecs, rec(
      orbit_index := i,
      orbit_size := Length(orb),
      rep_a := String(a),
      rep_b := String(b),
      theta_admissible := thetaOk,
      tau_admissible := tauOk,
      both_admissible := (thetaOk and tauOk)
    ));
  od;

  return rec(
    label := label,
    order := Size(G),
    id_small_group := IdGroup(G),
    aut_order := Size(AutG),
    num_pairs := Length(pairs),
    num_orbits := Length(orbitsList),
    orbits := orbitRecs
  );
end;;

# ================================================================================
# Run: G4 = SmallGroup(32,2) (calibration, known-admissible window K^(4)),
# then G6 = SmallGroup(32,6) (the new candidate under judgement).
# ================================================================================

g4Result := AnalyzeGroup(SmallGroup(32,2), "G4 = SmallGroup(32,2) [calibration]");;
Print("\n");
g6Result := AnalyzeGroup(SmallGroup(32,6), "G6 = SmallGroup(32,6) [candidate]");;

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");

# ================================================================================
# judgement summary
# ================================================================================
g4AllBoth := ForAll(g4Result.orbits, r -> r.both_admissible);;
g6AnyBoth := ForAny(g6Result.orbits, r -> r.both_admissible);;
g6AllBoth := ForAll(g6Result.orbits, r -> r.both_admissible);;

Print("\n[calibration] G4 (SmallGroup(32,2)): all orbits both-admissible = ", PF(g4AllBoth),
      " (expect PASS; FAIL would indicate an implementation bug)\n");
Print("[candidate] G6 (SmallGroup(32,6)): #orbits=", g6Result.num_orbits,
      ", any both-admissible=", PF(g6AnyBoth), ", all both-admissible=", PF(g6AllBoth), "\n");

# ================================================================================
# certificate JSON
# ================================================================================
OrbitToJson := function(r)
  return Concatenation(
    "{\"orbit_index\":", String(r.orbit_index),
    ",\"orbit_size\":", String(r.orbit_size),
    ",\"rep_a\":", JStr(r.rep_a),
    ",\"rep_b\":", JStr(r.rep_b),
    ",\"theta_admissible\":", JB(r.theta_admissible),
    ",\"tau_admissible\":", JB(r.tau_admissible),
    ",\"both_admissible\":", JB(r.both_admissible),
    "}");
end;;

GroupResultToJson := function(gr)
  local orbJson;
  orbJson := List(gr.orbits, OrbitToJson);
  return Concatenation(
    "{\"label\":", JStr(gr.label),
    ",\"order\":", String(gr.order),
    ",\"id_small_group\":[", String(gr.id_small_group[1]), ",", String(gr.id_small_group[2]), "]",
    ",\"aut_order\":", String(gr.aut_order),
    ",\"num_pairs\":", String(gr.num_pairs),
    ",\"num_orbits\":", String(gr.num_orbits),
    ",\"orbits\":", JArr(orbJson),
    "}");
end;;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/sg32-admissibility.g\",\"date\":\"2026-07-26\"},",
  "\"task\":\"SG(32,6) 新窓候補 (N_6=192, 3 Aut-orbits) の B3-許容性 (theta: x|->y,y|->x / tau: x|->y,y|->(xy)^-1 が核を保つか、軌道単位の同値判定) + G4=SmallGroup(32,2) の較正 (裁定19追記)\",",
  "\"universe\":\"SmallGroup(32,i), i in {2,6} のみ (search/smallgroup32-scan.g で非零と判明した2群、事前登録どおり範囲固定、広げない)\",",
  "\"method\":\"marked pair (a,b) with <a,b>=G, ord(a)=ord(b)=ord(ab)=4; split into Aut(G)-orbits via Orbit(AutG,pt,ActOnPair); theta/tau admissibility = membership of transformed pair (b,a) resp. (b,(ab)^-1) in the SAME orbit as (a,b) (marked-pair orbit test, not raw subgroup comparison)\",",
  "\"g4_calibration\":", GroupResultToJson(g4Result), ",",
  "\"g6_candidate\":", GroupResultToJson(g6Result), ",",
  "\"g4_all_orbits_both_admissible\":", JB(g4AllBoth), ",",
  "\"g6_any_orbit_both_admissible\":", JB(g6AnyBoth), ",",
  "\"g6_all_orbits_both_admissible\":", JB(g6AllBoth),
  "}");

WriteFile("certificates/a5/sg32_admissibility.json", s);
Print("wrote certificates/a5/sg32_admissibility.json\n");

QUIT;
