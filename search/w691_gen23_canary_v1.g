## search/w691_gen23_canary_v1.g -- W691-GEN23 canary (裁定829, docs/notes/w691_scan_gen23_spec_v1.md).
## Two tasks, both at q=7 (small enough for exhaustive full-element-pair checks):
##
## (A) 4-point canary of theorem GEN23-DET: for d in {1,2,3,6}, H_d^(7) := {M in GL(2,7):
##     det M in mu_d}. GEN23-DET predicts (2,3)-generation (exists order-2 x order-3 generating
##     pair) for d=2,6 (|D|=d even) and NON-generation for d=1,3 (|D|=d odd). Checked via FULL
##     exhaustive (order-2, order-3) element-pair enumeration (the same discipline as
##     search/w691_scan_canary_v1.g's check1, extended to all 4 d values -- d=6 case (H_6=GL(2,7)
##     itself) reproduces that earlier script's own result as an internal consistency check).
##     ANY disagreement with the prediction (d=1 or d=3 generating; d=2 or d=6 NOT generating)
##     is flagged explicitly -- per 裁定829's own instruction, a single disagreement means
##     "the theorem is wrong, STOP and report", not something to paper over.
##
## (B) "2688=2688" one-line check (docs/notes/w691_scan_gen23_spec_v1.md SS4): for EVERY one of
##     the (2,3)-generating braid pairs (a,b) found in H_6=GL(2,7) (a*b*a=b*a*b, <a,b>=G), check
##     whether z:=(a*b*a)^2 equals I (the identity) or -I. The spec's bijection argument
##     ((x,y)->(u,v)=(xyx,xy) between "braid pairs" and "pairs satisfying u^2=v^3") predicts
##     z=I always (never z=-I) for GL(2,7) -- this is re-derived here from scratch (this script
##     does NOT import search/w691_scan_canary_v1.g's cert data; it re-scans GL(2,7) directly,
##     since that earlier cert only stored a SAMPLE generating pair, not the full list of 2688).
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

q := 7;;
Fq := GF(q);;
GLq := GL(2, q);;
glOrder := Size(GLq);;
Print("|GL(2,", q, ")| = ", glOrder, "\n");

## Fq^* generator for computing mu_d (d-th roots of unity in Fq^*)
zgen := PrimitiveRoot(Fq);;
qMinus1 := q - 1;;
Print("|F_", q, "^*| = ", qMinus1, "\n");

MuD := function(d)
  local step, i, s;
  step := qMinus1 / d;
  return Set(List([0..d-1], i -> zgen^(i*step)));
end;;

BuildHd := function(d)
  local mu, elts;
  mu := MuD(d);
  elts := Filtered(Elements(GLq), M -> DeterminantMat(M) in mu);
  return elts;
end;;

## ---- (A) 4-point canary ----
canaryResults := [];;
for d in [1,2,3,6] do
  hdElts := BuildHd(d);;
  hdOrder := Length(hdElts);;
  hdExpected := d * (q * (q^2-1) / (q-1));;   # d * |SL(2,q)|, but compute |SL(2,q)| properly below
  slOrder := Size(SL(2,q));;
  hdExpected := d * slOrder;;
  hdOrderOk := (hdOrder = hdExpected);;

  ord2 := Filtered(hdElts, x -> Order(x) = 2);;
  ord3 := Filtered(hdElts, x -> Order(x) = 3);;

  genFound := false;;
  pairsChecked := 0;;
  genCount := 0;;
  for a in ord2 do
    for b in ord3 do
      pairsChecked := pairsChecked + 1;
      if Size(Subgroup(GLq, [a,b])) = hdOrder then
        genCount := genCount + 1;
        genFound := true;
      fi;
    od;
  od;

  predictedGen := (d mod 2 = 0);;   # GEN23-DET: |D|=d even => candidate for generation
  ## NOTE: GEN23-DET states even-d is NECESSARY for generation, not sufficient by itself in
  ## general -- but per the spec's own table, for THIS specific family (H_d over F_7) the
  ## expectation is d even <=> generates (d=2,6 generate; d=1,3 do not), checked directly below.
  agreesWithTheory := fail;;
  if d mod 2 = 1 then
    ## GEN23-DET predicts NON-generation for odd d
    agreesWithTheory := (genFound = false);
  else
    ## d even: theorem doesn't force generation, but the spec's own canary expectation is that
    ## d=2,6 DO generate for q=7 -- checked as an empirical expectation, disclosed as such
    agreesWithTheory := (genFound = true);
  fi;

  Add(canaryResults, rec(d:=d, hd_order:=hdOrder, hd_order_expected:=hdExpected,
                          hd_order_ok:=hdOrderOk, order2_count:=Length(ord2), order3_count:=Length(ord3),
                          pairs_checked:=pairsChecked, generating_pairs_found:=genCount,
                          generates:=genFound, agrees_with_GEN23_DET_prediction:=agreesWithTheory));
  Print("d=", d, " |H_d|=", hdOrder, " (expected ", hdExpected, ") ord2=", Length(ord2),
        " ord3=", Length(ord3), " pairs=", pairsChecked, " gen_pairs=", genCount,
        " generates=", genFound, " agrees=", agreesWithTheory, "\n");
od;

allCanaryAgree := ForAll(canaryResults, r -> r.agrees_with_GEN23_DET_prediction);;
Print("ALL 4 CANARY POINTS AGREE WITH GEN23-DET: ", allCanaryAgree, "\n");
if not allCanaryAgree then
  Print("*** STOP CONDITION: GEN23-DET disagreement detected -- theorem may be WRONG ***\n");
fi;

## ---- (B) z=(aba)^2 check on ALL generating braid pairs of H_6=GL(2,7) ----
h6Elts := Elements(GLq);;  # H_6 = GL(2,7) itself (mu_6 = all of F_7^*)
negI := (-One(Fq)) * IdentityMat(2, Fq);;
posI := IdentityMat(2, Fq) * One(Fq);;

genBraidPairsZ := [];;
for a in h6Elts do
  for b in h6Elts do
    if a*b*a = b*a*b then
      if Size(Subgroup(GLq, [a,b])) = glOrder then
        zElt := (a*b*a)^2;;
        Add(genBraidPairsZ, rec(z_is_I:=(zElt = posI), z_is_negI:=(zElt = negI)));
      fi;
    fi;
  od;
od;

totalGenBraidPairs := Length(genBraidPairsZ);;
allZisI := ForAll(genBraidPairsZ, r -> r.z_is_I);;
anyZisNegI := ForAny(genBraidPairsZ, r -> r.z_is_negI);;
Print("total generating braid pairs found (GL(2,7)): ", totalGenBraidPairs, "\n");
Print("all_z_equal_I: ", allZisI, "  any_z_equal_negI: ", anyZisNegI, "\n");

## ============ JSON output ============
JCanaryRec := function(r)
  return Concatenation("{",
    "\"d\":", String(r.d), ",",
    "\"hd_order\":", String(r.hd_order), ",",
    "\"hd_order_expected\":", String(r.hd_order_expected), ",",
    "\"hd_order_ok\":", JB(r.hd_order_ok), ",",
    "\"order2_count\":", String(r.order2_count), ",",
    "\"order3_count\":", String(r.order3_count), ",",
    "\"pairs_checked\":", String(r.pairs_checked), ",",
    "\"generating_pairs_found\":", String(r.generating_pairs_found), ",",
    "\"generates\":", JB(r.generates), ",",
    "\"agrees_with_GEN23_DET_prediction\":", JB(r.agrees_with_GEN23_DET_prediction),
    "}");
end;;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/w691_gen23_canary_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a829 -- docs/notes/w691_scan_gen23_spec_v1.md \\u00a73.2 (\\u30ab\\u30ca\\u30ea\\u30a2) + \\u00a74 (2688 \\u691c\\u8a3c)\",",
  "\"canary_4point\":[", JoinC(List(canaryResults, JCanaryRec), ","), "],",
  "\"all_canary_points_agree_with_GEN23_DET\":", JB(allCanaryAgree), ",",
  "\"z_check\":{",
    "\"total_generating_braid_pairs\":", String(totalGenBraidPairs), ",",
    "\"all_z_equal_I\":", JB(allZisI), ",",
    "\"any_z_equal_negI\":", JB(anyZisNegI),
  "},",
  "\"no_verdict_note\":\"raw group orders, pair counts, and booleans only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/w691_gen23_canary_v1_20260812.json", out);;
Print("Wrote search/certs/w691_gen23_canary_v1_20260812.json\n");
Print("W691_GEN23_CANARY_DONE\n");
QUIT;
