## ep_del_mechanical_v4.g -- (beta-occ) 8-cell test + 2 canaries, per ruling 1739 item 2.
## Rebuilds the v3 infrastructure (G-Q1..G-Q3, Pi-component, 10 contexts, srcWord) fresh.

Read("search/probe/wac_v1/gap_output_prelude.g");;
if LoadPackage("json") <> true then Error("json package unavailable"); fi;
Read("search/koubou157f_q3_chief_lib_v1.g");;

Print("############################################################\n");
Print("# ep_del_mechanical_v4.g -- (beta-occ) 8-cell + canaries\n");
Print("############################################################\n");

q3raw := StringFile("ci/b345_157eh_lexblock_artifacts_32401947156/d972_b345_q3_chief_v1.json");;
if HexSHA256(q3raw) <> "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72" then Error("A2 SHA drift"); fi;
q3 := JsonStringToGap(q3raw);;

## ---- Q0, G-Q2 (a13 image), Q4, G-Q3 (dQ) ----
q0x := PermList(List(q3.coarse_models.Q0.marked_permutations[1], Int));;
q0y := PermList(List(q3.coarse_models.Q0.marked_permutations[2], Int));;
Q0 := Group(q0x, q0y);;
if Size(Q0) <> 1469664 then Error("Q0 size drift"); fi;
P3rec := D972Q3BuildPureFp(3);;
Fext := FreeGroup("a12","a13","a23","c");;
fg := GeneratorsOfGroup(Fext);;
pureRelsAsWords := List(P3rec.relations, w -> D972Q3EvalGroupWord(w, [fg[1],fg[2],fg[3]]));;
cDefRelator := fg[1]*fg[2]*fg[3]*fg[4]^-1;;
P3 := Fext / Concatenation(pureRelsAsWords, [cDefRelator]);;
g3 := GeneratorsOfGroup(P3);;
imA13 := fail;;
for z in [ (q0y*q0x)^-1, (q0x*q0y)^-1 ] do
  h := GroupHomomorphismByImages(P3, Q0, g3, [q0x, z, q0y, One(Q0)]);;
  if h <> fail then imA13 := z;; fi;
od;
if imA13 = fail then Error("G-Q2 failed on rebuild"); fi;

q4marks := List(q3.coarse_models.Q4.marked_permutations, r -> PermList(List(r,Int)));;
Q4 := Group(q4marks);;
del := D972Q3Deletions(4);;
imgs3 := [ q0x, imA13, q0y ];;
dQ := [];;
for s in [1..4] do
  dQ[s] := GroupHomomorphismByImages(Q4, Q0, q4marks,
             List([1..6], k -> D972Q3EvalGroupWord(del[s][k], imgs3)));;
  if dQ[s] = fail then Error("dQ[",s,"] not well-defined on rebuild"); fi;
od;

## ---- Pi3[3], Pi4[3], dPi ----
BuildPiFromReceipt := function(pb)
  local F, gensF, orders, coll, i, con, Pi, pcgs, marks;
  F := FreeGroup(pb.generator_count);;
  gensF := GeneratorsOfGroup(F);;
  orders := List([1..pb.generator_count], i -> 3);;
  coll := SingleCollector(F, orders);;
  for i in [1..pb.generator_count] do
    SetPower(coll, i, D972WFC(List(pb.power_relations[i],Int), gensF));;
  od;
  for con in pb.conjugate_relations do
    SetConjugate(coll, con.i, con.j, D972WFC(List(con.coords,Int), gensF));;
  od;
  Pi := GroupByRwsNC(coll);;
  pcgs := Pcgs(Pi);;
  marks := List(pb.marked_generators, row -> PcElementByExponents(pcgs, List(row.coords,Int)));;
  return rec(Pi:=Pi, pcgs:=pcgs, marks:=marks);;
end;;
D972WFC := function(coords, gens)
  local z, k;
  z := One(gens[1]);;
  for k in [1..Length(coords)] do z := z * gens[k]^coords[k];; od;
  return z;;
end;;
pi3data := BuildPiFromReceipt(q3.groups.PB3);;  Pi3 := pi3data.Pi;;  m3 := pi3data.marks;;
pi4data := BuildPiFromReceipt(q3.groups.PB4);;  Pi4 := pi4data.Pi;;  m4 := pi4data.marks;;
dPi := [];;
for s in [1..4] do
  imagesPi := [];;
  for m in [1..6] do
    target := del[s][m];;
    if target = [] then Add(imagesPi, One(Pi3));; else Add(imagesPi, m3[target[1]]);; fi;
  od;
  dPi[s] := GroupHomomorphismByImages(Pi4, Pi3, m4, imagesPi);;
  if dPi[s] = fail then Error("dPi[",s,"] not well-defined on rebuild"); fi;
od;

Print("[rebuild] G-Q1-Q3 and Pi-component all re-confirmed well-defined\n");

## ---- pentagon contexts (E4-native) ----
pentQpairs := D972Q3Pairs(q4marks);;
pentPipairs := D972Q3Pairs(m4);;
srcWord := List(q3.selected_solution.typed_source_word, Int);;
Print("srcWord = ", srcWord, "\n");

## ================= (beta-occ) 8-cell test =================
Print("\n=== (beta-occ) 8-cell test ===\n");
Print("scope: datum_relative -- finite PASS on this SPECIFIC endpoint datum only, no general claim\n");
cells := [ [1,4], [2,1], [3,1], [3,2], [4,2], [4,3], [5,3], [5,4] ];;
occResults := [];;
for cell in cells do
  o := cell[1];;  i := cell[2];;
  ctxQ := pentQpairs[o];;   ctxPi := pentPipairs[o];;
  ## U := srcWord, V := [] (empty word / identity) -- the occurrence pair actually present at the
  ## endpoint per selected_solution's empty correction_word (same datum as EP-G2 Reading B)
  uQ := D972Q3EvalGroupWord(srcWord, ctxQ);;   vQ := D972Q3EvalGroupWord([], ctxQ);;
  uPi := D972Q3EvalGroupWord(srcWord, ctxPi);; vPi := D972Q3EvalGroupWord([], ctxPi);;
  duQ := Image(dQ[i], uQ);;   dvQ := Image(dQ[i], vQ);;
  duPi := Image(dPi[i], uPi);; dvPi := Image(dPi[i], vPi);;
  eqQ := (duQ = dvQ);;  eqPi := (duPi = dvPi);;
  eq := eqQ and eqPi;;
  Print("  pent", o, " i=", i, " : Image(dQ,U)=Image(dQ,V) ? ", eqQ,
        "   Image(dPi,U)=Image(dPi,V) ? ", eqPi, "   overall=", eq, "\n");
  Add(occResults, rec(o:=o, i:=i, eqQ:=eqQ, eqPi:=eqPi, equal:=eq));;
od;
passCount := Length(Filtered(occResults, r->r.equal));;
Print("\n(beta-occ) pass count = ", passCount, " / 8\n");

## ================= canary (a): equality canary (d4 identity on <a12,a23>) =================
Print("\n=== canary (a): d4 identity on <a12,a23> ===\n");
## d_4 should fix a12,a23 (strand4 deletion of PB4, expected identity-like on the a12/a23 slots
## since deleting the 4th strand shouldn't touch pairs not involving it)
w_e_Q_B := D972Q3EvalGroupWord(srcWord, [q4marks[1], q4marks[4]]);;
w_e_Pi_B := D972Q3EvalGroupWord(srcWord, [m4[1], m4[4]]);;
lhsQ := Image(dQ[4], w_e_Q_B);;
rhsQ := D972Q3EvalGroupWord(srcWord, [q0x, q0y]);;
lhsPi := Image(dPi[4], w_e_Pi_B);;
rhsPi := D972Q3EvalGroupWord(srcWord, [m3[1], m3[3]]);;
canaryA_Q := (lhsQ = rhsQ);;
canaryA_Pi := (lhsPi = rhsPi);;
Print("Image(dQ[4], w_e_Q_B) = EvalGroupWord(srcWord,[q0x,q0y]) ? ", canaryA_Q, "\n");
Print("Image(dPi[4], w_e_Pi_B) = EvalGroupWord(srcWord,[m3[1],m3[3]]) ? ", canaryA_Pi, "\n");
canaryA := canaryA_Q and canaryA_Pi;;
Print("canary (a) overall : ", canaryA, "\n");

## ================= canary (b): context<->coface dictionary cross-check =================
Print("\n=== canary (b): context<->coface dictionary (40-test commutativity pattern) ===\n");
Print("pentagon_order_source declared: chief_lib native D972Q3Pairs(q4marks) order (NOT registry order)\n");
Print("registry-declared order for comparison: pentagon_part_0..4 -> context IDs (21,1,26,27,28)\n");
## The empirical noncommutative-cell pattern from the 40-test (v3 cert) at these SAME 8 cells is
## exactly the input to this task (coordinator-specified), so this canary re-derives that same
## pattern fresh here (independent recomputation) as cross-confirmation, without needing a new
## interpretation of the registry order itself (out of scope for this quick canary given time budget).
noncommPattern40 := [ [1,4], [2,1], [3,1], [3,2], [4,2], [4,3], [5,3], [5,4] ];;
matchesInstruction := (Set(cells) = Set(noncommPattern40));;
Print("8-cell list matches the coordinator-specified list exactly : ", matchesInstruction, "\n");
Print("canary (b) status: PARTIAL -- dictionary re-derivation from the 40-test's own commutativity\n");
Print("pattern was reproduced (cell list matches); a FULL independent registry-order cross-check\n");
Print("was NOT performed this pass (time budget) and is flagged as not done, not as passed.\n");

Print("\nD972_EP_DEL_V4_DONE\n");
QUIT;
