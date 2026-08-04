# driver_step4_evaluate_v2.g -- Lane V main computation, REPAIRED (arbitration
# docs/notes/hsp7_hexagon_arbitration_v1.md SS5.4 repair A). Identical to
# driver_step4_evaluate.g (v1, preserved unmodified -- see its own file and the
# HELD cert search/certs/hsp7_cond4_laneV_20260804.json) except: all pure-Q
# factor applications (f, f^-1, x^-m, y^-m, c^m) now go through
# EvalFullHexagonFixed (sigma-word expansion via the validated ApplyGen),
# instead of the buggy ApplyQElt. Validated first against a fully independent
# LITERAL toy window (driver_step3b_toy_fixture.g -- must PASS before this file
# is trusted; both are gate-checked below).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");
LoadPackage("anupq");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= gate: TOY fixture must pass before anything else runs =================
toyGate := TestToyFixtureLiteralVsFixed();;
if (not toyGate.ok) or (toyGate.mismatches > 0) then
  Print("[STOP] TOY fixture gate failed -- refusing to run the real evaluation.\n");
  Error("TOY fixture gate failed");
fi;
Print("[GATE PASS] TOY fixture (literal vs EvalFullHexagonFixed): 0/", Length(toyGate.results),
      " mismatches. Proceeding.\n\n");

# ================= JSON text-scan helpers (unchanged from v1) =================
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

# ================= step: read PQ_OUTPUT_P.g, build P (same construction as v1;
# reused rather than rebuilt since ANUPQ is deterministic and this is not where
# the bug was -- S-7' below re-measures independently anyway) =================
Read("search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g");
P := F;;
xbar := MapImages[1];;
ybar := MapImages[2];;
Print("|P| = ", Size(P), "\n");

sizeP := Size(P);;
derP := DerivedSubgroup(P);;
sizeDerP := Size(derP);;
ordx := Order(xbar);;
ordy := Order(ybar);;
N_ord_main := Lcm([ordx, ordy, 1]);;
X_N_main := Filtered([0..N_ord_main-1], m -> Gcd(2*m+1, N_ord_main) = 1);;
Print("own measurement: |P|=", sizeP, " |[P,P]|=", sizeDerP, " ord(x)=", ordx, " ord(y)=", ordy,
      " N_ord(main)=", N_ord_main, " X_N(main)=", X_N_main, " |X_N|=", Length(X_N_main), "\n");

ownMeasurementStr := Concatenation(
  "size_P=", String(sizeP), "\n",
  "size_derived_subgroup=", String(sizeDerP), "\n",
  "ord_x=", String(ordx), "\n",
  "ord_y=", String(ordy), "\n",
  "N_ord=", String(N_ord_main), "\n",
  "X_N=", String(X_N_main), "\n",
  "abs_X_N=", String(Length(X_N_main)), "\n");
WriteFile("search/probe/hsp7_cond4_laneV/own_measurement_phase1_v2.txt", ownMeasurementStr);

# ================= phase 2: S-7' comparison (unchanged logic) =================
anchorPath := "search/certs/hsp7_cond2_p7_20260804.json";;
anchorStr := ReadFileStr(anchorPath);;
r := ReadIntAfterMarker(anchorStr, "\"size_P\": \"", 1);;
anchor_size_P := r.val;;
r := ReadIntAfterMarker(anchorStr, "\"derived_subgroup_size\": \"", 1);;
anchor_derived := r.val;;

laneSPath := "search/certs/hsp7_cond4_laneS_20260804.json";;
laneSStr := ReadFileStr(laneSPath);;
r := ReadIntAfterMarker(laneSStr, "\"size_P\": ", 1);;
laneS_size_P := r.val;;
r := ReadIntAfterMarker(laneSStr, "\"size_derived_subgroup\": ", 1);;
laneS_size_derived := r.val;;
r := ReadIntAfterMarker(laneSStr, "\"N_ord\": ", 1);;
laneS_N_ord := r.val;;
r := ReadIntAfterMarker(laneSStr, "\"abs_X_N\": ", 1);;
laneS_abs_X_N := r.val;;

s7_size_P_match := (sizeP = anchor_size_P) and (sizeP = laneS_size_P);;
s7_derived_match := (sizeDerP = anchor_derived) and (sizeDerP = laneS_size_derived);;
s7_N_ord_match := (N_ord_main = laneS_N_ord);;
s7_abs_X_N_match := (Length(X_N_main) = laneS_abs_X_N);;
s7_all_match := s7_size_P_match and s7_derived_match and s7_N_ord_match and s7_abs_X_N_match;;
Print("[", PF(s7_all_match), "] S-7' four columns all match (own/anchor/LaneS)\n");
if not s7_all_match then
  Error("S-7' PREREGISTRATION_FALSIFIED / INTEGRITY_STOP");
fi;

# ================= candidate cross-check (unchanged logic) =================
ckPos := FindPositionFrom(laneSStr, "\"candidate_key_list\": [", 1);;
ckEnd := FindPositionFrom(laneSStr, "\"candidates_in\":", ckPos);;
ckBlock := laneSStr{[ckPos..ckEnd-1]};;
laneS_mVals := [];; pos := 1;;
while true do
  pr := ReadIntAfterMarker(ckBlock, "\"m\": ", pos);
  if pr = fail then break; fi;
  Add(laneS_mVals, pr.val);
  pos := pr.nextPos;
od;
candCountMatch := (Length(laneS_mVals) = 8) and ForAll(laneS_mVals, v -> v = 0);;
Print("[", PF(candCountMatch), "] Lane S candidate count = 8, all m=0\n");

ReadQuotedAfterMarker := function(str, marker, startPos)
  local pos, j, s;
  pos := FindPositionFrom(str, marker, startPos);
  if pos = fail then return fail; fi;
  j := pos + Length(marker);
  s := "";
  while j <= Length(str) and str[j] <> '"' do
    Append(s, [str[j]]);  j := j+1;
  od;
  return rec(val := s, nextPos := j+1);
end;;
laneS_fwords := [];; pos := 1;;
while true do
  pr := ReadQuotedAfterMarker(ckBlock, "\"f_word\": \"", pos);
  if pr = fail then break; fi;
  Add(laneS_fwords, pr.val);
  pos := pr.nextPos;
od;
expectedFwords := List([0..6], t -> Concatenation("h4^", String(t)));;
Add(expectedFwords, "h3 = [[x,y],x]*[[x,y],y]");;
fwordsMatch := (laneS_fwords = expectedFwords);;
Print("[", PF(fwordsMatch), "] Lane S f_words match pre-registered list exactly\n");

laneS_verdicts := [];; pos := 1;;
while true do
  pr := ReadQuotedAfterMarker(laneSStr, "\"hexagon_verdict\": \"", pos);
  if pr = fail then break; fi;
  Add(laneS_verdicts, pr.val);
  pos := pr.nextPos;
od;
Print("Lane S hexagon_verdict list (8 expected): ", laneS_verdicts, "\n");

# ================= build h4, h3 as BOTH pc-group elements (for the NW-P3 h4<>1
# sanity check, unaffected by the bug) AND free-group (x,y) words (for feeding
# into EvalFullHexagonFixed, which requires a free-group element so it can
# expand pure-Q factors into sigma-words) =================
h4 := Comm(Comm(Comm(xbar,ybar),xbar),xbar) * Comm(Comm(Comm(xbar,ybar),xbar),ybar)^4
      * Comm(Comm(Comm(xbar,ybar),ybar),ybar);;
h3 := Comm(Comm(xbar,ybar),xbar) * Comm(Comm(xbar,ybar),ybar);;
Print("h4 <> Identity(P): ", h4 <> Identity(P), " (expect true, NW-P3)\n");

FreeXY := FreeGroup("x", "y");;
Fx := FreeXY.1;;  Fy := FreeXY.2;;
h4free := Comm(Comm(Comm(Fx,Fy),Fx),Fx) * Comm(Comm(Comm(Fx,Fy),Fx),Fy)^4
          * Comm(Comm(Comm(Fx,Fy),Fy),Fy);;
h3free := Comm(Comm(Fx,Fy),Fx) * Comm(Comm(Fx,Fy),Fy);;

# ================= build N0 (control window): P x C7 (unchanged from v1) =================
C7 := CyclicGroup(IsPcGroup, 7);;
gc := GeneratorsOfGroup(C7)[1];;
N0grp := DirectProduct(P, C7);;
embP := Embedding(N0grp, 1);;
embC := Embedding(N0grp, 2);;
xbar0 := Image(embP, xbar);;
ybar0 := Image(embP, ybar);;
chat0 := Image(embC, gc);;
Print("|N0grp| = ", Size(N0grp), " (expect ", sizeP*7, ")\n");
Print("Order(chat0) = ", Order(chat0), " (expect 7)\n");
N_ord_ctrl := Lcm([Order(xbar0), Order(ybar0), Order(chat0)]);;

chatMain := Identity(P);;

# ================= 8 candidates, N (main) window, via EvalFullHexagonFixed =================
candidates := [];;
for t in [0..6] do
  Add(candidates, rec(key_id := t+1, m := 0, fword := Concatenation("h4^", String(t)), ffree := h4free^t));
od;
Add(candidates, rec(key_id := 8, m := 0, fword := "h3 = [[x,y],x]*[[x,y],y]", ffree := h3free));

laneV_results := [];;
for c in candidates do
  r := EvalFullHexagonFixed(c.m, c.ffree, xbar, ybar, chatMain);
  verdict := "FAIL";; if r.hex33 and r.hex34 then verdict := "PASS"; fi;
  Add(laneV_results, rec(key_id := c.key_id, m := c.m, fword := c.fword,
                          hex33 := r.hex33, hex34 := r.hex34, verdict := verdict));
  Print("candidate key_id=", c.key_id, " f=", c.fword, " : (3.3)=", r.hex33, " (3.4)=", r.hex34,
        " verdict=", verdict, "\n");
od;

fourway := [];;
s9_mismatch := 0;;
for i in [1..8] do
  Add(fourway, rec(key_id := i, laneS := laneS_verdicts[i], laneV := laneV_results[i].verdict));
  if laneS_verdicts[i] <> laneV_results[i].verdict then s9_mismatch := s9_mismatch + 1; fi;
od;
Print("\n4-way table (key_id, LaneS, LaneV):\n");
for row in fourway do
  Print("  ", row.key_id, ": LaneS=", row.laneS, " LaneV=", row.laneV, "\n");
od;
Print("S-9 mismatch count = ", s9_mismatch, " (expect 0 after repair, per arbitration prediction)\n");

# ================= NW-P8 m-sweep: m in {1,2,4,5,6}, fbar=1, N and N0, via
# EvalFullHexagonFixed. f=1 as a free-group element = One(FreeXY). =================
freeOne := One(FreeXY);;
mSweep := [1,2,4,5,6];;
p8results := [];;
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
Print("note (arbitration SS1.1 (P-1)): for f in [F2,F2] (charming), N and N0 full-hexagon\n",
      "judgments are PREDICTED to always agree (N cap F2 = N0 cap F2 = V(F2)); a nonzero\n",
      "mismatch count here would itself indicate a remaining implementation defect, not a\n",
      "genuine c-detection event.\n");

s8Fired := "false";;
if p8_mismatch_count = 0 then
  s8Fired := "true";
else
  s8Fired := "false";
fi;

Print("\n=== SUMMARY ===\n");
Print("S-7' fired: ", not s7_all_match, "\n");
Print("S-9 mismatch count: ", s9_mismatch, "\n");
Print("S-8 (reduced scope) fired: ", s8Fired, "\n");

resStr := "";;
Append(resStr, Concatenation("sizeP=", String(sizeP), "\n"));
Append(resStr, Concatenation("sizeDerP=", String(sizeDerP), "\n"));
Append(resStr, Concatenation("N_ord_main=", String(N_ord_main), "\n"));
Append(resStr, Concatenation("N_ord_ctrl=", String(N_ord_ctrl), "\n"));
Append(resStr, Concatenation("s9_mismatch=", String(s9_mismatch), "\n"));
Append(resStr, Concatenation("p8_mismatch_count=", String(p8_mismatch_count), "\n"));
WriteFile("search/probe/hsp7_cond4_laneV/results_summary_v2.txt", resStr);

Print("\n[DONE] driver_step4_evaluate_v2.g complete.\n");
QUIT;
