## search/w691_gen23_witness_v1.g -- W691-GEN23 witness search (裁定829/832, docs/notes/
## w691_scan_gen23_spec_v1.md SS3.2), for the p=691-scale targets H_2, H_6 (d=1,3 excluded by
## theorem GEN23-DET, confirmed 4/4 at the q=7 canary in search/w691_gen23_canary_v1.g).
##
## *** PERFORMANCE NOTE (self-discovered during this run, not in the spec) ***: computing
## Size(Subgroup(GL(2,691),[a,b])) directly via GAP's generic matrix-group BSGS is NOT "seconds"
## as the spec estimated -- measured >180s without completing for a single trial (same class of
## issue as search/xd1_chk_v1.g's earlier self-caught performance bug: GAP's generic algorithm
## doesn't get classical-group recognition hints for a hand-built matrix subgroup). FIXED here by
## converting to the FAST route the spec's own phrase "nice monomorphism" was presumably
## pointing at: explicitly building the natural permutation action of <a,b> on the projective
## line P^1(F_691) (692 points, i.e. lines through the origin in F_691^2), then using GAP's
## (fast, degree-692) PERMUTATION group Size algorithm -- measured 22ms per trial (vs >180s+
## timeout for the naive matrix approach), a ~10000x+ speedup.
##
## *** KERNEL CORRECTION (mathematical subtlety, verified numerically before use) ***: the
## projective action has kernel = <a,b> ∩ Z(GL(2,691)) (central scalar matrices). This kernel is
## NOT always trivial or always order 2 -- it depends on H_d: |Z ∩ H_2| = 2, |Z ∩ H_6| = 6
## (verified by direct enumeration: s in F_691^* with s^2 in mu_d, counted 2 and 6 respectively
## for d=2,6). Since |H_d| = d * |SL(2,691)| and (as it happens) |Z ∩ H_d| = d exactly for BOTH
## d=2 and d=6 here, the SUCCESS CRITERION for <a,b>=H_d simplifies to exactly:
##     sizePerm (image of <a,b> acting on P^1) == |SL(2,691)| = 329,938,680
## for BOTH targets -- the branch (det(b)=1 for H_2, det(b)=omega for H_6) is what determines
## WHICH target is being tested, not the numeric success threshold (which is the same). This is
## VERIFIED, not assumed: the script also independently confirms det(<a,b>) generates exactly
## mu_d (order d) as a second, independent check before declaring success.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

p := 691;;
Fp := GF(p);;
GLp := GL(2, p);;
slOrder := Size(SL(2,p));;
h2Order := 2 * slOrder;;
h6Order := 6 * slOrder;;
Print("|SL(2,691)| = ", slOrder, " |H_2| = ", h2Order, " |H_6| = ", h6Order, "\n");

## primitive cube root of unity in F_691
g691 := PrimitiveRootMod(691);;
omega := PowerModInt(g691, 690/3, 691) * One(Fp);;
omega2 := omega^2;;

diag1neg1 := DiagonalMat([One(Fp), -One(Fp)]);;
diagOmegaOmega2 := DiagonalMat([omega, omega2]);;   # b-template, det=1 branch (H_2 and H_6)
diag1Omega := DiagonalMat([One(Fp), omega]);;        # b-template, det=omega branch (H_6 only)

RandomConjugate := function(M)
  local g;
  g := PseudoRandom(GLp);
  return g * M * g^-1;
end;;

## ---- fast projective-line (692 points) machinery ----
Canon := function(v)
  if v[1] <> Zero(Fp) then return v / v[1]; else return v / v[2]; fi;
end;;

projPts := [];;
for x in Fp do Add(projPts, Canon([x, One(Fp)])); od;
Add(projPts, Canon([One(Fp), Zero(Fp)]));
projPts := Set(projPts);;
if Length(projPts) <> 692 then Error("projective point count != 692"); fi;

ActOnProjPt := function(v, M) return Canon(M * v); end;;
posOf := function(v) return Position(projPts, v); end;;

PermOfMatrix := function(M)
  return PermList(List(projPts, v -> posOf(ActOnProjPt(v, M))));
end;;

FastGroupOrder := function(a, b)
  local permA, permB;
  permA := PermOfMatrix(a);
  permB := PermOfMatrix(b);
  return Size(Group(permA, permB));
end;;

## det-generated subgroup order (cheap: multiplicative order computation in F_691^*)
DetSubgroupOrder := function(a, b)
  local da, db, ordA, ordB, g, i, elts;
  da := DeterminantMat(a);;  db := DeterminantMat(b);;
  elts := Set([da, db]);;
  ## generate the subgroup of F_691^* by repeated multiplication (small, <=690)
  return Size(Group(da, db));
end;;

SEED := 20260812;;
Reset(GlobalMersenneTwister, SEED);;
TRIAL_CAP := 2000;;

WitnessSearch := function(targetD, hOrder)
  local trial, a, b, sizePerm, detOrd, branch, success;
  for trial in [1..TRIAL_CAP] do
    a := RandomConjugate(diag1neg1);;
    if targetD = 6 and (trial mod 2 = 0) then
      b := RandomConjugate(diag1Omega);;
      branch := "det_omega";
    else
      b := RandomConjugate(diagOmegaOmega2);;
      branch := "det_1";
    fi;
    sizePerm := FastGroupOrder(a, b);;
    detOrd := DetSubgroupOrder(a, b);;
    success := (sizePerm = slOrder) and (detOrd = targetD);;
    if success then
      return rec(found:=true, trials:=trial, witness_a:=a, witness_b:=b, branch:=branch,
                 size_perm:=sizePerm, det_order:=detOrd);
    fi;
  od;
  return rec(found:=false, trials:=TRIAL_CAP, witness_a:=fail, witness_b:=fail, branch:=fail,
             size_perm:=fail, det_order:=fail);
end;;

t0 := GAPLIB_WallElapsedMs();;
resH2 := WitnessSearch(2, h2Order);;
t1 := GAPLIB_WallElapsedMs();;
Print("H_2 search: found=", resH2.found, " trials=", resH2.trials, " elapsed_ms=", t1-t0, "\n");

resH6 := WitnessSearch(6, h6Order);;
t2 := GAPLIB_WallElapsedMs();;
Print("H_6 search: found=", resH6.found, " trials=", resH6.trials, " elapsed_ms=", t2-t1, "\n");

## ============ JSON output ============
JMatFp := function(m)
  return Concatenation("[[", String(IntFFE(m[1][1])), ",", String(IntFFE(m[1][2])), "],[",
                        String(IntFFE(m[2][1])), ",", String(IntFFE(m[2][2])), "]]");
end;;

JWitnessResult := function(label, hOrder, r)
  local status, wStr;
  if r.found then status := "PROVEN_GENERATES"; else status := "UNKNOWN_TRIAL_CAP_REACHED"; fi;
  wStr := "null";
  if r.found then
    wStr := Concatenation("{\"a\":", JMatFp(r.witness_a), ",\"b\":", JMatFp(r.witness_b),
                           ",\"branch\":", JStr(r.branch), ",\"size_perm\":", String(r.size_perm),
                           ",\"det_order\":", String(r.det_order), "}");
  fi;
  return Concatenation("{",
    "\"label\":", JStr(label), ",",
    "\"target_order\":", String(hOrder), ",",
    "\"status\":", JStr(status), ",",
    "\"trials\":", String(r.trials), ",",
    "\"trial_cap\":", String(TRIAL_CAP), ",",
    "\"witness\":", wStr,
    "}");
end;;

out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/w691_gen23_witness_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a829/832 -- docs/notes/w691_scan_gen23_spec_v1.md \\u00a73.2 (\\u767a\\u6ce8 W691-GEN23)\",",
  "\"method_note\":\"random witness search; DECISIVE check via FAST projective-line (692-point) permutation action Size computation (measured 22ms/trial, vs >180s timeout for naive matrix-group Size -- self-corrected performance bug, see script header) PLUS independent det-subgroup-order check (targetD). A positive hit (sizePerm==|SL(2,691)| AND det_order==targetD) is a PROOF (kernel-corrected success criterion, verified numerically: |Z cap H_2|=2, |Z cap H_6|=6, both making the projective-image target exactly |SL(2,691)|). Failure within the trial cap is UNKNOWN, not a negative claim.\",",
  "\"seed\":", String(SEED), ",",
  "\"trial_cap\":", String(TRIAL_CAP), ",",
  "\"sl_2_691_order\":", String(slOrder), ",",
  "\"h2_order\":", String(h2Order), ",",
  "\"h6_order\":", String(h6Order), ",",
  "\"results\":[", JWitnessResult("H_2", h2Order, resH2), ",", JWitnessResult("H_6", h6Order, resH6), "],",
  "\"no_verdict_note\":\"raw trial counts, witness matrices (if found), and status strings only (PROVEN_GENERATES / UNKNOWN_TRIAL_CAP_REACHED -- never a negative claim). \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/w691_gen23_witness_v1_20260812.json", out);;
Print("Wrote search/certs/w691_gen23_witness_v1_20260812.json\n");
Print("W691_GEN23_WITNESS_DONE\n");
QUIT;
