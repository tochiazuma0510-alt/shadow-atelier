# driver_step4_evaluate_v3.g -- CV-9 副検問 B-2 (blocking): re-evaluate the 8
# dummy/h3 candidates on N0 (control window) as well as N, per arbitration
# SS5.4 item 5's pre-registration ("both N and control N0"), which v2 left
# unevaluated on N0 without an explicit not_evaluated disclosure. Otherwise
# identical to driver_step4_evaluate_v2.g (N-window results unchanged, not
# recomputed by copy -- recomputed fresh here for a single self-contained v3
# artifact; same code path, same deterministic P).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");
LoadPackage("anupq");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

toyGate := TestToyFixtureLiteralVsFixed();;
if (not toyGate.ok) or (toyGate.mismatches > 0) then
  Error("TOY fixture gate failed");
fi;
extGate := TestToyFixtureExtended();;
if (not extGate.ok) or (extGate.mismatches > 0) then
  Error("extended TOY fixture gate failed");
fi;
Print("[GATE PASS] both TOY fixtures (base 6/6, extended 7/7) clean. Proceeding.\n\n");

FindPositionFrom := function(str, marker, startPos)
  local n, m, i, k, matched;
  n := Length(str);  m := Length(marker);
  if m = 0 then return startPos; fi;
  for i in [startPos..n-m+1] do
    matched := true;
    for k in [1..m] do
      if str[i+k-1] <> marker[k] then matched := false; break; fi;
    od;
    if matched then return i; fi;
  od;
  return fail;
end;;

ReadIntAfterMarker := function(str, marker, startPos)
  local pos, j, digitStr;
  pos := FindPositionFrom(str, marker, startPos);
  if pos = fail then return fail; fi;
  j := pos + Length(marker);
  digitStr := "";
  while j <= Length(str) and str[j] in "0123456789" do
    Append(digitStr, [str[j]]);  j := j+1;
  od;
  if Length(digitStr) = 0 then return fail; fi;
  return rec(val := Int(digitStr), nextPos := j);
end;;

ReadFileStr := function(path)
  local s;
  s := StringFile(path);
  if s = fail then Error("cannot read file: ", path); fi;
  return s;
end;;

WriteFile := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

Read("search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g");
P := F;;
xbar := MapImages[1];;
ybar := MapImages[2];;
Print("|P| = ", Size(P), "\n");

sizeP := Size(P);;
sizeDerP := Size(DerivedSubgroup(P));;
ordx := Order(xbar);;  ordy := Order(ybar);;
N_ord_main := Lcm([ordx, ordy, 1]);;
X_N_main := Filtered([0..N_ord_main-1], m -> Gcd(2*m+1, N_ord_main) = 1);;

anchorStr := ReadFileStr("search/certs/hsp7_cond2_p7_20260804.json");;
r := ReadIntAfterMarker(anchorStr, "\"size_P\": \"", 1);;  anchor_size_P := r.val;;
r := ReadIntAfterMarker(anchorStr, "\"derived_subgroup_size\": \"", 1);;  anchor_derived := r.val;;

laneSStr := ReadFileStr("search/certs/hsp7_cond4_laneS_20260804.json");;
r := ReadIntAfterMarker(laneSStr, "\"size_P\": ", 1);;  laneS_size_P := r.val;;
r := ReadIntAfterMarker(laneSStr, "\"size_derived_subgroup\": ", 1);;  laneS_size_derived := r.val;;
r := ReadIntAfterMarker(laneSStr, "\"N_ord\": ", 1);;  laneS_N_ord := r.val;;
r := ReadIntAfterMarker(laneSStr, "\"abs_X_N\": ", 1);;  laneS_abs_X_N := r.val;;

s7_all_match := (sizeP = anchor_size_P) and (sizeP = laneS_size_P)
                and (sizeDerP = anchor_derived) and (sizeDerP = laneS_size_derived)
                and (N_ord_main = laneS_N_ord) and (Length(X_N_main) = laneS_abs_X_N);;
Print("[", PF(s7_all_match), "] S-7' four columns all match\n");
if not s7_all_match then Error("S-7' PREREGISTRATION_FALSIFIED"); fi;

ckPos := FindPositionFrom(laneSStr, "\"candidate_key_list\": [", 1);;
ckEnd := FindPositionFrom(laneSStr, "\"candidates_in\":", ckPos);;
ckBlock := laneSStr{[ckPos..ckEnd-1]};;
laneS_mVals := [];; pos := 1;;
while true do
  pr := ReadIntAfterMarker(ckBlock, "\"m\": ", pos);
  if pr = fail then break; fi;
  Add(laneS_mVals, pr.val);  pos := pr.nextPos;
od;

ReadQuotedAfterMarker := function(str, marker, startPos)
  local pos, j, s;
  pos := FindPositionFrom(str, marker, startPos);
  if pos = fail then return fail; fi;
  j := pos + Length(marker);
  s := "";
  while j <= Length(str) and str[j] <> '"' do Append(s, [str[j]]);  j := j+1; od;
  return rec(val := s, nextPos := j+1);
end;;
laneS_fwords := [];; pos := 1;;
while true do
  pr := ReadQuotedAfterMarker(ckBlock, "\"f_word\": \"", pos);
  if pr = fail then break; fi;
  Add(laneS_fwords, pr.val);  pos := pr.nextPos;
od;
expectedFwords := List([0..6], t -> Concatenation("h4^", String(t)));;
Add(expectedFwords, "h3 = [[x,y],x]*[[x,y],y]");;
Print("[", PF(laneS_fwords = expectedFwords), "] Lane S f_words match pre-registered list exactly\n");

laneS_verdicts := [];; pos := 1;;
while true do
  pr := ReadQuotedAfterMarker(laneSStr, "\"hexagon_verdict\": \"", pos);
  if pr = fail then break; fi;
  Add(laneS_verdicts, pr.val);  pos := pr.nextPos;
od;

# ================= B-1: candidates_in_own_digest_sha256 (machine-generated,
# canonical serialization of what was actually read, then hashed externally) ==
candSerial := "";;
for i in [1..8] do
  Append(candSerial, Concatenation("key_id=", String(i), ";m=", String(laneS_mVals[i]),
                                    ";f_word=", laneS_fwords[i], "\n"));
od;
WriteFile("search/probe/hsp7_cond4_laneV/candidates_in_v3.txt", candSerial);
Print("candidates_in serialization written to search/probe/hsp7_cond4_laneV/candidates_in_v3.txt\n");

h4 := Comm(Comm(Comm(xbar,ybar),xbar),xbar) * Comm(Comm(Comm(xbar,ybar),xbar),ybar)^4
      * Comm(Comm(Comm(xbar,ybar),ybar),ybar);;
h3 := Comm(Comm(xbar,ybar),xbar) * Comm(Comm(xbar,ybar),ybar);;
Print("h4 <> Identity(P): ", h4 <> Identity(P), "\n");

FreeXY := FreeGroup("x", "y");;
Fx := FreeXY.1;;  Fy := FreeXY.2;;
h4free := Comm(Comm(Comm(Fx,Fy),Fx),Fx) * Comm(Comm(Comm(Fx,Fy),Fx),Fy)^4
          * Comm(Comm(Comm(Fx,Fy),Fy),Fy);;
h3free := Comm(Comm(Fx,Fy),Fx) * Comm(Comm(Fx,Fy),Fy);;

C7 := CyclicGroup(IsPcGroup, 7);;
gc := GeneratorsOfGroup(C7)[1];;
N0grp := DirectProduct(P, C7);;
embP := Embedding(N0grp, 1);;  embC := Embedding(N0grp, 2);;
xbar0 := Image(embP, xbar);;  ybar0 := Image(embP, ybar);;  chat0 := Image(embC, gc);;
Print("|N0grp| = ", Size(N0grp), "  Order(chat0) = ", Order(chat0), "\n");

chatMain := Identity(P);;

candidates := [];;
for t in [0..6] do
  Add(candidates, rec(key_id := t+1, m := 0, fword := Concatenation("h4^", String(t)), ffree := h4free^t));
od;
Add(candidates, rec(key_id := 8, m := 0, fword := "h3 = [[x,y],x]*[[x,y],y]", ffree := h3free));

# ---- N window (unchanged from v2, recomputed for a self-contained v3 log) ----
laneV_N_results := [];;
for c in candidates do
  r := EvalFullHexagonFixed(c.m, c.ffree, xbar, ybar, chatMain);
  verdict := "FAIL";; if r.hex33 and r.hex34 then verdict := "PASS"; fi;
  Add(laneV_N_results, rec(key_id := c.key_id, fword := c.fword, hex33 := r.hex33, hex34 := r.hex34, verdict := verdict));
  Print("N  candidate key_id=", c.key_id, " f=", c.fword, " : (3.3)=", r.hex33, " (3.4)=", r.hex34, " verdict=", verdict, "\n");
od;

# ---- ★ B-2: N0 window (NEW in v3 -- was missing/unevaluated in v2) ----
laneV_N0_results := [];;
for c in candidates do
  r := EvalFullHexagonFixed(c.m, c.ffree, xbar0, ybar0, chat0);
  verdict := "FAIL";; if r.hex33 and r.hex34 then verdict := "PASS"; fi;
  Add(laneV_N0_results, rec(key_id := c.key_id, fword := c.fword, hex33 := r.hex33, hex34 := r.hex34, verdict := verdict));
  Print("N0 candidate key_id=", c.key_id, " f=", c.fword, " : (3.3)=", r.hex33, " (3.4)=", r.hex34, " verdict=", verdict, "\n");
od;

fourway := [];;
s9_mismatch := 0;;
n_vs_n0_mismatch_8cand := 0;;
for i in [1..8] do
  Add(fourway, rec(key_id := i, laneS := laneS_verdicts[i], laneV_N := laneV_N_results[i].verdict,
                    laneV_N0 := laneV_N0_results[i].verdict));
  if laneS_verdicts[i] <> laneV_N_results[i].verdict then s9_mismatch := s9_mismatch + 1; fi;
  if laneV_N_results[i].verdict <> laneV_N0_results[i].verdict then n_vs_n0_mismatch_8cand := n_vs_n0_mismatch_8cand + 1; fi;
od;
Print("\n4-way table (key_id, LaneS, LaneV-N, LaneV-N0):\n");
for row in fourway do
  Print("  ", row.key_id, ": LaneS=", row.laneS, " LaneV-N=", row.laneV_N, " LaneV-N0=", row.laneV_N0, "\n");
od;
Print("S-9 mismatch count (LaneS vs LaneV-N) = ", s9_mismatch, "\n");
Print("N vs N0 mismatch count (8 candidates) = ", n_vs_n0_mismatch_8cand, "\n");

mSweep := [1,2,4,5,6];;
p8results := [];;
freeOne := One(FreeXY);;
for m in mSweep do
  rN := EvalFullHexagonFixed(m, freeOne, xbar, ybar, chatMain);
  vN := "FAIL";; if rN.hex33 and rN.hex34 then vN := "PASS"; fi;
  rN0 := EvalFullHexagonFixed(m, freeOne, xbar0, ybar0, chat0);
  vN0 := "FAIL";; if rN0.hex33 and rN0.hex34 then vN0 := "PASS"; fi;
  Add(p8results, rec(m := m, verdictN := vN, verdictN0 := vN0, agree := (vN = vN0)));
  Print("NW-P8 m=", m, ": N=", vN, " N0=", vN0, " agree=", (vN=vN0), "\n");
od;
p8_mismatch_count := Length(Filtered(p8results, r -> not r.agree));;
Print("\nNW-P8 mismatch count (N vs N0) = ", p8_mismatch_count, " (of 5)\n");

Print("\n=== SUMMARY ===\n");
Print("S-9 mismatch count: ", s9_mismatch, "\n");
Print("8-candidate N vs N0 mismatch count: ", n_vs_n0_mismatch_8cand, "\n");
Print("NW-P8 mismatch count: ", p8_mismatch_count, "\n");

resStr := Concatenation(
  "sizeP=", String(sizeP), "\n",
  "s9_mismatch=", String(s9_mismatch), "\n",
  "n_vs_n0_mismatch_8cand=", String(n_vs_n0_mismatch_8cand), "\n",
  "p8_mismatch_count=", String(p8_mismatch_count), "\n");
WriteFile("search/probe/hsp7_cond4_laneV/results_summary_v3.txt", resStr);

Print("\n[DONE] driver_step4_evaluate_v3.g complete.\n");
QUIT;
