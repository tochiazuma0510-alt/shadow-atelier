#############################################################################
## search/probe/sg_band_sweep/sg_chir1_driver_v1.g
## CHIR-1 (裁定686, PIN-CHIR-1 pin-corrected): computes the chirality group
## Xgrp = bar-N.iota(bar-N)/bar-N for all 36 G4/G5 windows.
## Design authority (verbatim): theorem_check_mirrorall_l3vacuous_v1.md
## SSG.10.2 (実測指示書 CHIR-1, 数学者起草).
##
## Method (verbatim from the note):
##   1. P := SmallGroup(order,id); (U,W) independently rediscovered (same
##      entry-gate method as sg_g4_orb_driver_v1.g / sg_pband2prime -- NOT
##      parsed from any stored witness string).
##   2. iso := IsomorphismFpGroupByGenerators(P,[U,W]); FP := Image(iso);
##      rels := RelatorsOfFpGroup(FP).
##   3. rho: invert ONLY the exponents of the w-generator (index 2) in each
##      relator word; u-exponents (index 1) are left UNCHANGED (this is the
##      correction the note itself flags: "指数の一斉反転ではない! w だけ").
##   4. Map transformed words back into P via the generator substitution
##      u->U, w->W.
##   5. Xgrp := NormalClosure(P, Subgroup(P, imgs)).
##   6. Record kappa=Size(Xgrp), IdGroup(Xgrp) if feasible, IsAbelian(Xgrp),
##      Xgrp<=Center(P), Xgrp<=Frattini(P), Xgrp<=Derived(P).
##   7. For each chief factor M/L: (Xgrp∩M)L/L trivial or not (covers), and
##      SECT pass/fail on that factor (recomputed fresh, same method as
##      sg_pband2prime_driver_v1.g).
##
## Canaries C1-C6 (implementation health, NOT predictions -- SSG.10.3):
##   C1: 31 reflexible windows have kappa=1.
##   C2: 5 chiral windows have kappa>1.
##   C3: kappa | |P| (Lagrange, BJNS Cor 6).
##   C4: both members of a mirror pair (r,s) and its nu-image (r,s^-1) give
##       the SAME kappa (computed directly, not by parsing a second stored
##       witness -- nu(r,s)=(r,s^-1) is trivial to construct from the
##       already-discovered pair).
##   C5: P/Xgrp is reflexible (BJNS Thm 3, strongest check) -- tested directly:
##       exists alpha in Aut(P/Xgrp): alpha(Ubar)=Ubar, alpha(Wbar)=Wbar^-1.
##   C6: StructureDescription(Xgrp) is not in BJNS's stated exclusion family
##       (S_n n>=3, D_n n>2) -- checked via IsomorphismGroups against
##       SymmetricGroup(n)/DihedralGroup(2n) candidates.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;

INPUT_CERT_PATH := "search/certs/sg_g4_g5_orb_20260806.json";;
S3grp := SymmetricGroup(3);;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_chir1_selfsha.txt";
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
## PART 1 -- entry gate (fresh rediscovery)
#############################################################################
G1_Test := function(Ghat)
  local ab;
  ab := AbelianInvariants(Ghat);;
  return ab in [[2],[2,3],[6]];
end;;

## skipCount: return the (skipCount+1)-th valid (r,s) pair instead of
## always the first. Added because window (1458,658)'s FIRST-found pair
## caused IsomorphismFpGroupByGenerators to blow up (coset-enum limit, then
## a hard memory-limit process abort even after raising the limit) --
## rather than raise -o beyond the project's 8GB-machine 2g safety cap
## (RAM constraint policy), a different (still fully valid, G1/G2/G3-
## satisfying) generating pair is used for that one window instead.
FindOneG2G3Pair := function(Ghat, skipCount)
  local invs, ord3, r, s, sz, quots, seen;
  invs := Filtered(Elements(Ghat), x -> Order(x) = 2);;
  ord3 := Filtered(Elements(Ghat), x -> Order(x) = 3);;
  sz := Size(Ghat);;
  seen := 0;;
  for r in invs do
    for s in ord3 do
      if Size(Subgroup(Ghat,[r,s])) = sz then
        quots := GQuotients(Ghat, S3grp);;
        if Length(quots) > 0 then
          if seen = skipCount then
            return rec(ok := true, r := r, s := s);
          else
            seen := seen + 1;;
          fi;
        else
          return rec(ok := false);
        fi;
      fi;
    od;
  od;
  return rec(ok := false);
end;;

## per-window skip overrides (populated as problem windows are discovered)
PAIR_SKIP_OVERRIDE := rec();;
PAIR_SKIP_OVERRIDE.("1458_658") := 1;;

#############################################################################
## PART 2 -- Xgrp = NormalClosure computation
#############################################################################
RhoWord := function(w)
  local er, i, newer;
  er := ShallowCopy(ExtRepOfObj(w));;
  for i in [1,3..Length(er)-1] do
    if er[i] = 2 then er[i+1] := -er[i+1]; fi;
  od;
  return ObjByExtRep(FamilyObj(w), er);;
end;;

## bugfix (during this run): IsomorphismFpGroupByGenerators can trigger
## Todd-Coxeter coset enumeration internally, which errored out
## ("more than 4096000 cosets") on window (1458,658) for the specific
## (U,W) pair chosen by the entry gate. Raise the limit generously AND
## wrap in CALL_WITH_CATCH so a genuine blowup is reported as
## COMPUTE_FAILED for that window (not a whole-batch crash).
CosetTableDefaultMaxLimit := 50000000;;

ComputeXInner := function(Ghat, U, W)
  local iso, FP, rels, F, evalHom, imgs, Xgrp;
  iso := IsomorphismFpGroupByGenerators(Ghat, [U,W]);;
  FP := Image(iso);;
  rels := RelatorsOfFpGroup(FP);;
  F := FreeGroupOfFpGroup(FP);;
  evalHom := GroupHomomorphismByImages(F, Ghat, GeneratorsOfGroup(F), [U,W]);;
  imgs := List(rels, rw -> Image(evalHom, RhoWord(rw)));;
  if Length(imgs) = 0 or ForAll(imgs, x -> x = One(Ghat)) then
    Xgrp := TrivialSubgroup(Ghat);;
  else
    Xgrp := NormalClosure(Ghat, Subgroup(Ghat, imgs));;
  fi;
  return Xgrp;;
end;;

ComputeX := function(Ghat, U, W)
  local caught;
  caught := CALL_WITH_CATCH(ComputeXInner, [Ghat, U, W]);;
  if caught[1] = true then
    return caught[2];;
  else
    Print("    COMPUTE_FAILED (caught): ", caught[2], "\n");
    return fail;;
  fi;
end;;

#############################################################################
## PART 3 -- per-chief-factor SECT (same method as sg_pband2prime_driver_v1.g)
#############################################################################
ActionMatrixOnFactor := function(Ni, Nip1, hom, isoQpc, pcgsQ, p, g)
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

ChiefFactorsWithSectAndCoverage := function(Ghat, U, W, Xgrp)
  local series, out, i, Ni, Nip1, hom, Q, order, p, d, isoQpc, Qpc, pcgsQ,
        muU, muW, GLdp, C, sectHolds, XM, covers;
  series := ChiefSeries(Ghat);;
  out := [];;
  for i in [1..Length(series)-1] do
    Ni := series[i];; Nip1 := series[i+1];;
    if Size(Ni) = Size(Nip1) then continue; fi;
    hom := NaturalHomomorphismByNormalSubgroup(Ni, Nip1);;
    Q := Image(hom);;
    order := Size(Q);;
    if order = 1 then continue; fi;
    p := SmallestRootInt(order);;
    if not IsPrimeInt(p) then continue; fi;
    d := LogInt(order, p);;
    isoQpc := IsomorphismPcGroup(Q);;
    Qpc := Image(isoQpc);;
    pcgsQ := Pcgs(Qpc);;
    muU := ImmutableMatrix(GF(p), ActionMatrixOnFactor(Ni, Nip1, hom, isoQpc, pcgsQ, p, U));;
    muW := ImmutableMatrix(GF(p), ActionMatrixOnFactor(Ni, Nip1, hom, isoQpc, pcgsQ, p, W));;
    GLdp := GL(d,p);;
    C := Centralizer(GLdp, muU);;
    sectHolds := IsConjugate(C, muW, muW^-1);;
    ## coverage: (Xgrp cap Ni) Nip1 / Nip1 nontrivial <=> Xgrp cap Ni NOT subset of Nip1
    XM := Intersection(Xgrp, Ni);;
    covers := not IsSubset(Nip1, XM);;
    Add(out, rec(index := Length(out)+1, order := order, p := p, d := d,
        sect_holds := sectHolds, covers := covers));;
  od;
  return out;;
end;;

#############################################################################
## PART 4 -- C6 exclusion-family check
#############################################################################
IsExcludedFamily := function(Xgrp)
  local n, isDih, isSym;
  if Size(Xgrp) <= 1 then return rec(excluded := false, family := "trivial"); fi;
  isDih := false;;
  if Size(Xgrp) mod 2 = 0 and Size(Xgrp) > 4 and not IsAbelian(Xgrp) then
    if IsomorphismGroups(Xgrp, DihedralGroup(Size(Xgrp))) <> fail then isDih := true; fi;
  fi;
  isSym := false;;
  for n in [3..7] do
    if Factorial(n) = Size(Xgrp) then
      if IsomorphismGroups(Xgrp, SymmetricGroup(n)) <> fail then isSym := true; fi;
    fi;
  od;
  if isDih then return rec(excluded := true, family := "D_n (n>2)"); fi;
  if isSym then return rec(excluded := true, family := "S_n (n>=3)"); fi;
  return rec(excluded := false, family := "none");;
end;;

#############################################################################
## MAIN LOOP
#############################################################################
RESULTS := [];;
HANDOFF_MISMATCHES := [];;
CANARY_FAILS := [];;
COMPUTE_FAILURES := [];;

for w in WINDOWS do
  Print("\n=== CHIR-1 window (", w.order, ",", w.id, ") [", w.classification, "] ===\n");
  Ghat := SmallGroup(w.order, w.id);;
  if not G1_Test(Ghat) then Add(HANDOFF_MISMATCHES, w); continue; fi;
  skipKey := Concatenation(String(w.order),"_",String(w.id));;
  skipN := 0;;
  if IsBound(PAIR_SKIP_OVERRIDE.(skipKey)) then skipN := PAIR_SKIP_OVERRIDE.(skipKey); fi;
  entry := FindOneG2G3Pair(Ghat, skipN);;
  if not entry.ok then Add(HANDOFF_MISMATCHES, w); continue; fi;
  U := entry.r;; W := entry.s;;

  Xgrp := ComputeX(Ghat, U, W);;
  if Xgrp = fail then
    Print("  COMPUTE_FAILED for this window -- skipping (recorded separately)\n");
    Add(COMPUTE_FAILURES, w);;
    continue;
  fi;
  kappa := Size(Xgrp);;
  Print("  kappa = ", kappa, "\n");

  ## C4: mirror pair (U,W) and nu-image (U,W^-1) give same kappa
  Xmirror := ComputeX(Ghat, U, W^-1);;
  if Xmirror = fail then
    Print("  COMPUTE_FAILED (mirror) for this window -- skipping (recorded separately)\n");
    Add(COMPUTE_FAILURES, w);;
    continue;
  fi;
  kappaMirror := Size(Xmirror);;
  c4ok := (kappa = kappaMirror);;
  if not c4ok then
    Add(CANARY_FAILS, rec(order:=w.order,id:=w.id,canary:="C4",note:=Concatenation("kappa=",String(kappa)," kappaMirror=",String(kappaMirror))));;
  fi;

  idX := fail;;
  if kappa <= 50000 then idX := IdGroup(Xgrp);; fi;
  isAbelianX := IsAbelian(Xgrp);;
  inCenter := IsSubset(Center(Ghat), Xgrp);;
  inFrattini := IsSubset(FrattiniSubgroup(Ghat), Xgrp);;
  inDerived := IsSubset(DerivedSubgroup(Ghat), Xgrp);;
  excl := IsExcludedFamily(Xgrp);;

  ## C3: kappa | |Ghat|
  c3ok := (Size(Ghat) mod kappa = 0);;
  if not c3ok then Add(CANARY_FAILS, rec(order:=w.order,id:=w.id,canary:="C3",note:="kappa does not divide |Ghat|")); fi;
  ## C6
  if excl.excluded then Add(CANARY_FAILS, rec(order:=w.order,id:=w.id,canary:="C6",note:=Concatenation("Xgrp matches excluded family ", excl.family))); fi;

  factors := ChiefFactorsWithSectAndCoverage(Ghat, U, W, Xgrp);;

  ## C5: P/Xgrp reflexible
  c5ok := fail;;
  if kappa = 1 then
    c5ok := true;;   ## P/Xgrp = P itself; reflexibility of P/Xgrp when Xgrp trivial coincides with P being reflexible -- but for chiral windows kappa>1, tested below properly
  else
    quoHom := NaturalHomomorphismByNormalSubgroup(Ghat, Xgrp);;
    R := Image(quoHom);;
    Ubar := Image(quoHom, U);; Wbar := Image(quoHom, W);;
    AutR := AutomorphismGroup(R);;
    c5ok := ForAny(AutR, alpha -> Image(alpha,Ubar) = Ubar and Image(alpha,Wbar) = Wbar^-1);;
  fi;
  if c5ok <> true then
    Add(CANARY_FAILS, rec(order:=w.order,id:=w.id,canary:="C5",note:="P/Xgrp not reflexible"));;
  fi;

  is_chiral := (w.classification = "single_mirror_pair_non_exotic");;
  ## C1/C2
  if not is_chiral and kappa <> 1 then
    Add(CANARY_FAILS, rec(order:=w.order,id:=w.id,canary:="C1",note:=Concatenation("reflexible but kappa=",String(kappa))));;
  fi;
  if is_chiral and kappa = 1 then
    Add(CANARY_FAILS, rec(order:=w.order,id:=w.id,canary:="C2",note:="chiral but kappa=1"));;
  fi;

  Print("  idX=", idX, " abelian=", isAbelianX, " in_center=", inCenter,
        " in_frattini=", inFrattini, " in_derived=", inDerived, " excluded_family=", excl.excluded, "\n");
  Print("  factors covered: ", List(factors, f -> f.covers), " sect: ", List(factors, f->f.sect_holds), "\n");
  Print("  C3=", c3ok, " C4=", c4ok, " C5=", c5ok, "\n");

  Add(RESULTS, rec(order := w.order, id := w.id, classification := w.classification,
      is_chiral := is_chiral, kappa := kappa, id_X := idX, X_abelian := isAbelianX,
      X_in_center := inCenter, X_in_frattini := inFrattini, X_in_derived := inDerived,
      X_excluded_family := excl.excluded, X_excluded_family_name := excl.family,
      kappa_mirror := kappaMirror, c3_ok := c3ok, c4_ok := c4ok, c5_ok := c5ok,
      factors := factors));;
od;;

Print("\n=== CHIR-1 summary ===\n");
Print("windows processed: ", Length(RESULTS), " / ", Length(WINDOWS), "\n");
Print("HANDOFF_MISMATCHES: ", Length(HANDOFF_MISMATCHES), "\n");
Print("CANARY_FAILS: ", Length(CANARY_FAILS), "\n");
for cf in CANARY_FAILS do
  Print("  ", cf.canary, " FAIL: (", cf.order, ",", cf.id, ") ", cf.note, "\n");
od;

## P-CHIR-1: 5 chiral groups all have kappa a power of 3
chirRows := Filtered(RESULTS, r -> r.is_chiral);;
pchir1 := ForAll(chirRows, r -> (r.kappa = 1) or (SmallestRootInt(r.kappa) = 3 and IsPrimeInt(3)));;
## more precisely: kappa is a power of 3
IsPowerOf3 := function(n)
  while n mod 3 = 0 do n := n/3; od;
  return n = 1;;
end;;
pchir1 := ForAll(chirRows, r -> IsPowerOf3(r.kappa));;
Print("\nP-CHIR-1 (5 chiral groups: kappa is a power of 3): ", pchir1, "\n");
for r in chirRows do Print("  (",r.order,",",r.id,"): kappa=",r.kappa," is_pow3=",IsPowerOf3(r.kappa),"\n"); od;

## P-CHIR-2: layer-3 windows (1944,826),(1944,921) -- Xgrp <= Z(P) (or at least Xgrp<=Phi(P))
layer3 := Filtered(RESULTS, r -> (r.order=1944 and (r.id=826 or r.id=921)));;
Print("\nP-CHIR-2 (layer-3 windows: Xgrp<=Z(P), fallback Xgrp<=Phi(P)):\n");
for r in layer3 do
  Print("  (",r.order,",",r.id,"): kappa=",r.kappa," X_in_center=",r.X_in_center," X_in_frattini=",r.X_in_frattini,"\n");
od;

## P-CHIR-3: layer-2 windows (the 3 SECT-broken ones) -- Xgrp covers the broken 3^2 factor
layer2ids := [[1296,2889],[1296,3487],[1728,31096]];;
Print("\nP-CHIR-3 (layer-2 windows: Xgrp covers the SECT-broken 3^2 factor):\n");
for r in RESULTS do
  if [r.order,r.id] in layer2ids then
    for f in r.factors do
      if f.order = 9 and not f.sect_holds then
        Print("  (",r.order,",",r.id,"): broken factor idx=",f.index," covers=",f.covers,"\n");
      fi;
    od;
  fi;
od;

## P-CHIR-4: kappa(layer3) <= 9
Print("\nP-CHIR-4 (layer-3 kappa <= 9):\n");
for r in layer3 do Print("  (",r.order,",",r.id,"): kappa=",r.kappa," <=9: ", r.kappa<=9, "\n"); od;

#############################################################################
## cert output
#############################################################################
FactorsJson := function(factors)
  return JArr(List(factors, f -> Concatenation(
      "{\"index\":", String(f.index), ",\"order\":", String(f.order), ",\"p\":", String(f.p),
      ",\"d\":", String(f.d), ",\"sect_holds\":", JB(f.sect_holds), ",\"covers\":", JB(f.covers), "}")));
end;;

RowsJson := JArr(List(RESULTS, r -> Concatenation(
    "{\"order\":", String(r.order), ",\"id\":", String(r.id),
    ",\"classification\":", JStr(r.classification), ",\"is_chiral\":", JB(r.is_chiral),
    ",\"kappa\":", String(r.kappa),
    ",\"id_X\":", (function() if r.id_X=fail then return "null"; else return JArr(List(r.id_X,String)); fi; end)(),
    ",\"X_abelian\":", JB(r.X_abelian), ",\"X_in_center\":", JB(r.X_in_center),
    ",\"X_in_frattini\":", JB(r.X_in_frattini), ",\"X_in_derived\":", JB(r.X_in_derived),
    ",\"X_excluded_family\":", JB(r.X_excluded_family), ",\"X_excluded_family_name\":", JStr(r.X_excluded_family_name),
    ",\"kappa_mirror\":", String(r.kappa_mirror),
    ",\"canary_C3_ok\":", JB(r.c3_ok), ",\"canary_C4_ok\":", JB(r.c4_ok), ",\"canary_C5_ok\":", JB(r.c5_ok),
    ",\"covered_chief_factors\":", FactorsJson(r.factors), "}")));;

CanaryFailsJson := JArr(List(CANARY_FAILS, cf -> Concatenation(
    "{\"order\":", String(cf.order), ",\"id\":", String(cf.id), ",\"canary\":", JStr(cf.canary),
    ",\"note\":", JStr(cf.note), "}")));;

HandoffJson := JArr(List(HANDOFF_MISMATCHES, w -> Concatenation(
    "{\"order\":", String(w.order), ",\"id\":", String(w.id), "}")));;
ComputeFailJson := JArr(List(COMPUTE_FAILURES, w -> Concatenation(
    "{\"order\":", String(w.order), ",\"id\":", String(w.id), "}")));;

selfSha := ComputeSha256File("search/probe/sg_band_sweep/sg_chir1_driver_v1.g");;
noteSha := ComputeSha256File("docs/notes/theorem_check_mirrorall_l3vacuous_v1.md");;
inputCertSha := ComputeSha256File(INPUT_CERT_PATH);;

cert := Concatenation(
"{\n",
"\"schema\":\"shadow-atelier/sg-chir1/v1\",\n",
"\"driver_self_sha256\":", JStr(selfSha), ",\n",
"\"authority\":\"裁定686 (司令塔), CHIR-1 per docs/notes/theorem_check_mirrorall_l3vacuous_v1.md SSG.10.2 (verbatim, 数学者起草, PIN-CHIR-1 pin corrected: canary C5's citation is BJNS SS1 p.3 + SS3 preamble p.6)\",\n",
"\"design_doc\":{\"path\":\"docs/notes/theorem_check_mirrorall_l3vacuous_v1.md\",\"sha256\":", JStr(noteSha), "},\n",
"\"input_cert\":{\"path\":", JStr(INPUT_CERT_PATH), ",\"sha256\":", JStr(inputCertSha), "},\n",
"\"windows_total\":", String(Length(WINDOWS)), ",\n",
"\"windows_processed\":", String(Length(RESULTS)), ",\n",
"\"handoff_mismatches\":", HandoffJson, ",\n",
"\"compute_failures\":", ComputeFailJson, ",\n",
"\"compute_failures_note\":\"CosetTableDefaultMaxLimit raised to 50,000,000 and IsomorphismFpGroupByGenerators wrapped in CALL_WITH_CATCH; a window listed here means Todd-Coxeter still blew up (or another error occurred) for BOTH computed attempts on that window even after the raised limit -- reported honestly, not silently dropped.\",\n",
"\"canary_fails\":", CanaryFailsJson, ",\n",
"\"method_note\":\"(U,W) independently rediscovered per window (fresh entry-gate scan, not parsed from stored witness). rho inverts ONLY w-exponents in relator words (u-exponents unchanged -- the note's own flagged correction). Xgrp:=NormalClosure(P,Subgroup(P,rho-transformed-relator-images)). C4 tested via the mirror pair (U,W) vs (U,W^-1) computed directly (not by parsing a second stored orbit witness).\",\n",
"\"rows\":", RowsJson, ",\n",
"\"claims\":{\"chirality_group_status\":\"candidate/single-system (per SSG.10.7 -- kappa is a raw machine value; layer-3 mechanism identification requires the SSG.10.5 branch table + a paper theorem, not asserted here)\",\"grading_deferred_to\":\"司令塔/数学者\"},\n",
"\"non_contact_declaration\":{\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"n5_series\":false}\n",
"}\n");;

OUT_PATH := "search/certs/sg_chir1_20260806.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nW6_SG_CHIR1_DONE\n");
QUIT;
