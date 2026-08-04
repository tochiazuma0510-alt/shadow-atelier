# driver_step4_evaluate.g -- Lane V main computation. Reads PQ_OUTPUT_P.g (own ANUPQ
# build of P = F2/(gamma5(F2)F2^7), step1+step2), builds P and P x C7 (N0 window),
# spot-checks the braid relation on the real groups, does the own S-7' measurement +
# two-phase comparison against the cond2 anchor cert and the Lane S cert (candidates
# and judgments only -- no Lane S driver code is read, per SS2 import boundary),
# evaluates the 8 dummy/h3 candidates on N via full (3.3)/(3.4), evaluates the NW-P8
# m-sweep on N and N0, and writes the final cert.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/probe/hsp7_cond4_laneV/statemachine_lib.g");
LoadPackage("anupq");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= JSON text-scan helpers (copied verbatim in style from
# search/week3-M5-explorer.g FindPositionFrom/DigitRunsToInts -- general house infra,
# not Lane S/P specific) =================
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

# ================= step: read PQ_OUTPUT_P.g, build P =================
Read("search/probe/hsp7_cond4_laneV/PQ_OUTPUT_P.g");
P := F;;
xbar := MapImages[1];;
ybar := MapImages[2];;
Print("|P| = ", Size(P), "\n");
Print("num pcgs generators of P = ", Length(Pcgs(P)), "\n");

# ================= own S-7' measurement (phase 1, before opening any external cert
# numeric value into this computation -- see deviation note in the final cert about
# reconnaissance-phase reading of design docs, matching Lane S's own disclosed R-11
# procedural note) =================
sizeP := Size(P);;
derP := DerivedSubgroup(P);;
sizeDerP := Size(derP);;
ordx := Order(xbar);;
ordy := Order(ybar);;
# main window: c |-> 1 (definitional, NW-1b(4); ord(cbar)=1 in N)
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
WriteFile := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;
WriteFile("search/probe/hsp7_cond4_laneV/own_measurement_phase1.txt", ownMeasurementStr);

# ================= phase 2: open anchor cert + Lane S cert, extract 4-column values =================
anchorPath := "search/certs/hsp7_cond2_p7_20260804.json";;
anchorStr := ReadFileStr(anchorPath);;
r := ReadIntAfterMarker(anchorStr, "\"size_P\": \"", 1);;
anchor_size_P := r.val;;
r := ReadIntAfterMarker(anchorStr, "\"derived_subgroup_size\": \"", 1);;
anchor_derived := r.val;;
Print("anchor cert (cond2): size_P=", anchor_size_P, " derived_subgroup_size=", anchor_derived, "\n");

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
Print("Lane S cert own_measurement_phase1: size_P=", laneS_size_P, " size_derived_subgroup=",
      laneS_size_derived, " N_ord=", laneS_N_ord, " abs_X_N=", laneS_abs_X_N, "\n");

s7_size_P_match := (sizeP = anchor_size_P) and (sizeP = laneS_size_P);;
s7_derived_match := (sizeDerP = anchor_derived) and (sizeDerP = laneS_size_derived);;
s7_N_ord_match := (N_ord_main = laneS_N_ord);;
s7_abs_X_N_match := (Length(X_N_main) = laneS_abs_X_N);;
s7_all_match := s7_size_P_match and s7_derived_match and s7_N_ord_match and s7_abs_X_N_match;;

Print("[", PF(s7_size_P_match), "] size_P match (own vs anchor vs LaneS)\n");
Print("[", PF(s7_derived_match), "] derived_subgroup_size match (own vs anchor vs LaneS)\n");
Print("[", PF(s7_N_ord_match), "] N_ord match (own vs LaneS)\n");
Print("[", PF(s7_abs_X_N_match), "] |X_N| match (own vs LaneS)\n");

if not s7_all_match then
  Print("\n[STOP] S-7' PREREGISTRATION_FALSIFIED -- 4-column mismatch detected. ",
        "Halting before hexagon evaluation.\n");
  Error("S-7' PREREGISTRATION_FALSIFIED / INTEGRITY_STOP");
fi;
Print("\n[GATE PASS] S-7' four columns all match. Proceeding.\n");

# ================= cross-check Lane S candidate_key_list against the pre-registered
# 8-item list (lanespec SS6 C-5, items 1+2) =================
# expected: dummy family h4^t, t=0..6 (7 items) + h3 negative (1 item), m=0 throughout.
expectedCandidates := List([0..6], t -> rec(m:=0, fword:=Concatenation("h4^", String(t))));;
Add(expectedCandidates, rec(m:=0, fword:="h3 = [[x,y],x]*[[x,y],y]"));;

# scan Lane S cert's candidate_key_list block for m and f_word occurrences (8 expected)
ckPos := FindPositionFrom(laneSStr, "\"candidate_key_list\": [", 1);;
if ckPos = fail then Error("candidate_key_list marker not found in Lane S cert"); fi;
ckEnd := FindPositionFrom(laneSStr, "],\n  \"candidates_in\"", ckPos);;
if ckEnd = fail then
  # fallback: search without exact whitespace assumption
  ckEnd := FindPositionFrom(laneSStr, "\"candidates_in\":", ckPos);;
fi;
ckBlock := laneSStr{[ckPos..ckEnd-1]};;
laneS_mVals := [];; pos := 1;;
while true do
  pr := ReadIntAfterMarker(ckBlock, "\"m\": ", pos);
  if pr = fail then break; fi;
  Add(laneS_mVals, pr.val);
  pos := pr.nextPos;
od;
Print("Lane S candidate_key_list: extracted ", Length(laneS_mVals), " m-values (expect 8, all 0): ",
      laneS_mVals, "\n");
candCountMatch := (Length(laneS_mVals) = 8) and ForAll(laneS_mVals, v -> v = 0);;
Print("[", PF(candCountMatch), "] Lane S candidate count = 8, all m=0 (matches SS6 C-5 items 1+2)\n");

# extract f_word strings too (quoted strings after "f_word": ")
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
Print("Lane S candidate_key_list f_words: ", laneS_fwords, "\n");
expectedFwords := List([0..6], t -> Concatenation("h4^", String(t)));;
Add(expectedFwords, "h3 = [[x,y],x]*[[x,y],y]");;
fwordsMatch := (laneS_fwords = expectedFwords);;
Print("[", PF(fwordsMatch), "] Lane S f_words match pre-registered list exactly (order-sensitive)\n");

# extract Lane S's hexagon_verdict for each key_id (for the 4-way comparison table)
laneS_verdicts := [];; pos := 1;;
while true do
  pr := ReadQuotedAfterMarker(laneSStr, "\"hexagon_verdict\": \"", pos);
  if pr = fail then break; fi;
  Add(laneS_verdicts, pr.val);
  pos := pr.nextPos;
od;
Print("Lane S hexagon_verdict list (8 expected): ", laneS_verdicts, "\n");

# ================= build h4, h3 (own construction; DUM-FIN, hs_prop7_translation_v1.md
# SS8.7.4, and SS6 C-5 of the lanespec) =================
h4 := Comm(Comm(Comm(xbar,ybar),xbar),xbar) * Comm(Comm(Comm(xbar,ybar),xbar),ybar)^4
      * Comm(Comm(Comm(xbar,ybar),ybar),ybar);;
h3 := Comm(Comm(xbar,ybar),xbar) * Comm(Comm(xbar,ybar),ybar);;
Print("h4 <> Identity(P): ", h4 <> Identity(P), " (expect true, NW-P3)\n");

# ================= build N0 (control window): P x C7, x,y trivial in C7-factor,
# c = generator of C7-factor (trivial in P-factor). Structurally validated against a
# genuine dihedral instance in driver_step3_selftest.g (SelfTestBraidOnGenuineInstance,
# ctrl case). =================
C7 := CyclicGroup(IsPcGroup, 7);;
gc := GeneratorsOfGroup(C7)[1];;
N0grp := DirectProduct(P, C7);;
embP := Embedding(N0grp, 1);;
embC := Embedding(N0grp, 2);;
xbar0 := Image(embP, xbar);;
ybar0 := Image(embP, ybar);;
chat0 := Image(embC, gc);;
Print("|N0grp| = ", Size(N0grp), " (expect |P|*7 = ", sizeP*7, ")\n");
Print("Order(chat0) = ", Order(chat0), " (expect 7, control window c survives)\n");
N_ord_ctrl := Lcm([Order(xbar0), Order(ybar0), Order(chat0)]);;
X_N_ctrl := Filtered([0..N_ord_ctrl-1], m -> Gcd(2*m+1, N_ord_ctrl) = 1);;
Print("N_ord(control) = ", N_ord_ctrl, " X_N(control) = ", X_N_ctrl, "\n");

chatMain := Identity(P);;   # main window: c |-> 1 (NW-1b(5))

# ================= braid-relation spot check on the REAL P (main) and REAL N0grp
# (control), sampling a curated set of states rather than the full 6*|Q| orbit (|P| too
# large to enumerate: exhaustive check is infeasible; this is a spot check, not a proof,
# and is reported as such). =================
BraidSpotCheck := function(phiX, phiY, phiC, sampleElts)
  local fails, s, a, b, t, e;
  fails := 0;;
  for t in [1..6] do
    for e in sampleElts do
      s := [t, e];
      a := ApplyGen(ApplyGen(ApplyGen(s,1,phiX,phiY,phiC),2,phiX,phiY,phiC),1,phiX,phiY,phiC);
      b := ApplyGen(ApplyGen(ApplyGen(s,2,phiX,phiY,phiC),1,phiX,phiY,phiC),2,phiX,phiY,phiC);
      if a<>b then fails := fails + 1; fi;
    od;
  od;
  return rec(fails := fails, total := 6*Length(sampleElts));
end;;

sampleP := [Identity(P), xbar, ybar, xbar*ybar, h4, h3, xbar^-1, ybar^-1, h4^3, h4^6];;
mainSpot := BraidSpotCheck(xbar, ybar, chatMain, sampleP);;
Print("[", PF(mainSpot.fails = 0), "] braid spot-check on real P (main window): fails=",
      mainSpot.fails, "/", mainSpot.total, "\n");

sampleN0 := List(sampleP, e -> Image(embP, e));;
Add(sampleN0, chat0);;  Add(sampleN0, chat0^3);;
ctrlSpot := BraidSpotCheck(xbar0, ybar0, chat0, sampleN0);;
Print("[", PF(ctrlSpot.fails = 0), "] braid spot-check on real P x C7 (control window): fails=",
      ctrlSpot.fails, "/", ctrlSpot.total, "\n");

if (mainSpot.fails > 0) or (ctrlSpot.fails > 0) then
  Error("braid spot-check FAILED on the real construction -- do not trust hexagon evaluation");
fi;

# ================= evaluate full (3.3)/(3.4) for a candidate (m, f) in a given window
# (phiX,phiY,phiC), matching search/week3-M5-explorer.g's own formulas (independently
# confirmed against docs/week1-定義ノート.md L160-161 (3.3)(3.4) verbatim):
#   (3.3): sigma1^u f^-1 sigma2^u f  =  f^-1 sigma1 sigma2 x^-m c^m      (u := 2m+1)
#   (3.4): f^-1 sigma2^u f sigma1^u  =  sigma2 sigma1 y^-m c^m f
# ================= =================
EvalFullHexagon := function(m, f, phiX, phiY, phiC)
  local u, base, finv, xm, cm, lhs33, rhs33, lhs34, rhs34, s;
  u := 2*m+1;
  finv := f^-1;
  xm := phiX^(-m);
  cm := phiC^m;
  base := [1, Identity(f)];  # basepoint identity coset; Identity(f) = identity of Qgrp

  # LHS (3.3): sigma1^u . f^-1 . sigma2^u . f
  s := ApplyGenPow(base, 1, u, phiX, phiY, phiC);
  s := ApplyQElt(s, finv);
  s := ApplyGenPow(s, 2, u, phiX, phiY, phiC);
  s := ApplyQElt(s, f);
  lhs33 := s;

  # RHS (3.3): f^-1 . sigma1 . sigma2 . x^-m . c^m
  s := ApplyQElt(base, finv);
  s := ApplyGenPow(s, 1, 1, phiX, phiY, phiC);
  s := ApplyGenPow(s, 2, 1, phiX, phiY, phiC);
  s := ApplyQElt(s, xm);
  s := ApplyQElt(s, cm);
  rhs33 := s;

  # LHS (3.4): f^-1 . sigma2^u . f . sigma1^u
  s := ApplyQElt(base, finv);
  s := ApplyGenPow(s, 2, u, phiX, phiY, phiC);
  s := ApplyQElt(s, f);
  s := ApplyGenPow(s, 1, u, phiX, phiY, phiC);
  lhs34 := s;

  # RHS (3.4): sigma2 . sigma1 . y^-m . c^m . f
  ym := phiY^(-m);
  s := ApplyGenPow(base, 2, 1, phiX, phiY, phiC);
  s := ApplyGenPow(s, 1, 1, phiX, phiY, phiC);
  s := ApplyQElt(s, ym);
  s := ApplyQElt(s, cm);
  s := ApplyQElt(s, f);
  rhs34 := s;

  return rec(hex33 := (lhs33 = rhs33), hex34 := (lhs34 = rhs34));
end;;

# ================= 8 candidates, N (main) window only (Lane S's window; R-8 requires
# independent judgment of Lane S's FULL submission, PASS and FAIL alike) =================
candidates := [];;
for t in [0..6] do
  Add(candidates, rec(key_id := t+1, m := 0, fword := Concatenation("h4^", String(t)), felt := h4^t));
od;
Add(candidates, rec(key_id := 8, m := 0, fword := "h3 = [[x,y],x]*[[x,y],y]", felt := h3));

laneV_results := [];;
for c in candidates do
  r := EvalFullHexagon(c.m, c.felt, xbar, ybar, chatMain);
  verdict := "UNKNOWN";;
  if r.hex33 and r.hex34 then verdict := "PASS"; else verdict := "FAIL"; fi;
  Add(laneV_results, rec(key_id := c.key_id, m := c.m, fword := c.fword,
                          hex33 := r.hex33, hex34 := r.hex34, verdict := verdict));
  Print("candidate key_id=", c.key_id, " f=", c.fword, " : (3.3)=", r.hex33, " (3.4)=", r.hex34,
        " verdict=", verdict, "\n");
od;

# 4-way comparison table vs Lane S's hexagon_verdict (already extracted as laneS_verdicts)
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
Print("S-9 mismatch count = ", s9_mismatch, "\n");

# ================= NW-P8 m-sweep (Appendix A-2 / SS4.2): m in {1,2,4,5,6}, fbar=1,
# evaluated on N (main) and N0 (control) windows =================
mSweep := [1,2,4,5,6];;
p8results := [];;
for m in mSweep do
  rN := EvalFullHexagon(m, Identity(P), xbar, ybar, chatMain);
  vN := "FAIL";; if rN.hex33 and rN.hex34 then vN := "PASS"; fi;
  rN0 := EvalFullHexagon(m, Identity(N0grp), xbar0, ybar0, chat0);
  vN0 := "FAIL";; if rN0.hex33 and rN0.hex34 then vN0 := "PASS"; fi;
  Add(p8results, rec(m := m, verdictN := vN, verdictN0 := vN0, agree := (vN = vN0)));
  Print("NW-P8 m=", m, ": N=", vN, " N0=", vN0, " agree=", (vN=vN0), "\n");
od;

p8_mismatch_count := Length(Filtered(p8results, r -> not r.agree));;
Print("\nNW-P8 mismatch count (N vs N0) = ", p8_mismatch_count, " (of 5)\n");

s8Fired := "false";;
s8Note := "";;
if p8_mismatch_count = 0 then
  s8Fired := "true";
  s8Note := "reduced-scope (m-sweep only) disagreement count = 0. Full SS9.3 S-8 (all X_N x all candidates) not evaluated. Deferred to SS10 main run per lanespec SS4.2 verdict rule.";
else
  s8Fired := "false";
  s8Note := "reduced-scope (m-sweep only) disagreement count > 0; recorded as a positive calibration indicator per lanespec SS4.2.";
fi;

Print("\n=== SUMMARY ===\n");
Print("S-7' fired: false (all 4 columns matched)\n");
Print("S-9 mismatch count: ", s9_mismatch, "\n");
Print("S-8 (reduced scope) fired: ", s8Fired, "\n");

# ================= write intermediate results file for cert assembly =================
resStr := "";;
Append(resStr, Concatenation("sizeP=", String(sizeP), "\n"));
Append(resStr, Concatenation("sizeDerP=", String(sizeDerP), "\n"));
Append(resStr, Concatenation("N_ord_main=", String(N_ord_main), "\n"));
Append(resStr, Concatenation("N_ord_ctrl=", String(N_ord_ctrl), "\n"));
Append(resStr, Concatenation("s9_mismatch=", String(s9_mismatch), "\n"));
Append(resStr, Concatenation("p8_mismatch_count=", String(p8_mismatch_count), "\n"));
WriteFile("search/probe/hsp7_cond4_laneV/results_summary.txt", resStr);

Print("\n[DONE] driver_step4_evaluate.g complete.\n");
QUIT;
