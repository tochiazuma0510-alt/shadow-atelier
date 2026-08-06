#############################################################################
## search/probe/sg_band_sweep/sg_chir1_single_window_v2.g
## CHIR-1, v2 (裁定686 + 司令塔介入指示、実地確認: (1458,658)が32分停滞=fp
## 表示の組合せ爆発だった)。ONE window per GAP process (parameterized via
## CHIR1_ORDER/CHIR1_ID, set by a tiny prelude before Read()-ing this file)
## -- lets an external orchestrator (scratchpad/run_chir1_v2.sh) enforce a
## HARD 120s wall-clock cap per window via `timeout 120`, something no
## single synchronous GAP process can do to itself once inside a blocking
## call.
##
## ROOT-CAUSE FIX (介入指示④): IsomorphismFpGroupByGenerators internally
## runs a Todd-Coxeter coset enumeration that blew up (>4,096,000 cosets,
## then a hard GAP memory-limit abort even after raising the coset limit)
## for at least one window. REPLACED with a Reidemeister-Schreier-via-
## spanning-tree construction that NEVER calls coset enumeration: Ghat is
## already a concrete, small (<=1944-element) finite group, so a BFS over
## its own Cayley graph (generators U,W) directly gives, for every g in
## Ghat and every generator x in {U,W}, a relator word(g)*x*word(g*x)^-1 in
## the free group F(u,w) that lies in ker(F->Ghat); the FULL set of these
## (over all g,x) generates ker(F->Ghat) as a normal subgroup (standard
## Reidemeister-Schreier fact -- mathematically equivalent set of relators
## for the SAME (U,W)-presentation, per 介入指示④'s own equivalence
## principle). Cost: O(|Ghat|^2) element comparisons, <=1944^2~=3.8M,
## trivial for GAP -- no coset enumeration, no risk of blowup.
## method field in the output record is always "reidemeister_schreier_bfs"
## (uniformly used for all windows, not just a fallback for heavy ones).
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;

if not IsBound(CHIR1_ORDER) or not IsBound(CHIR1_ID) then
  Error("CHIR1_ORDER / CHIR1_ID must be set before Read()-ing this file");
fi;

S3grp := SymmetricGroup(3);;

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

## Reidemeister-Schreier-via-spanning-tree: F(u,w) -> Ghat, gens u->U,w->W.
## Returns rec(F:=free group, relators:=list of relator WORDS in F).
BFSPresentation := function(Ghat, U, W)
  local F, uF, wF, elems, words, i, gens, pr, x, xF, g2, j, relators, rel;
  F := FreeGroup(2);; uF := F.1;; wF := F.2;;
  elems := [ One(Ghat) ];;
  words := [ One(F) ];;
  gens := [ [U,uF], [W,wF] ];;
  i := 1;;
  while i <= Length(elems) do
    for pr in gens do
      x := pr[1];; xF := pr[2];;
      g2 := elems[i]*x;;
      j := Position(elems, g2);;
      if j = fail then
        Add(elems, g2);; Add(words, words[i]*xF);;
      fi;
    od;
    i := i + 1;;
  od;
  relators := [];;
  for i in [1..Length(elems)] do
    for pr in gens do
      x := pr[1];; xF := pr[2];;
      g2 := elems[i]*x;;
      j := Position(elems, g2);;
      rel := words[i]*xF*words[j]^-1;;
      if rel <> One(F) then Add(relators, rel); fi;
    od;
  od;
  return rec(F := F, relators := relators, group_size := Length(elems));;
end;;

RhoWord := function(w)
  local er, i;
  er := ShallowCopy(ExtRepOfObj(w));;
  for i in [1,3..Length(er)-1] do
    if er[i] = 2 then er[i+1] := -er[i+1]; fi;
  od;
  return ObjByExtRep(FamilyObj(w), er);;
end;;

ComputeXgrp := function(Ghat, U, W)
  local pres, F, evalHom, imgs, Xgrp;
  pres := BFSPresentation(Ghat, U, W);;
  F := pres.F;;
  evalHom := GroupHomomorphismByImages(F, Ghat, GeneratorsOfGroup(F), [U,W]);;
  imgs := List(pres.relators, rw -> Image(evalHom, RhoWord(rw)));;
  if Length(imgs) = 0 or ForAll(imgs, x -> x = One(Ghat)) then
    Xgrp := TrivialSubgroup(Ghat);;
  else
    Xgrp := NormalClosure(Ghat, Subgroup(Ghat, imgs));;
  fi;
  return rec(Xgrp := Xgrp, num_relators := Length(pres.relators));;
end;;

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
    XM := Intersection(Xgrp, Ni);;
    covers := not IsSubset(Nip1, XM);;
    Add(out, rec(index := Length(out)+1, order := order, p := p, d := d,
        sect_holds := sectHolds, covers := covers));;
  od;
  return out;;
end;;

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
## MAIN (single window)
#############################################################################
t0 := GAPLIB_WallElapsedMs();;
outRec := rec(order := CHIR1_ORDER, id := CHIR1_ID, method := "reidemeister_schreier_bfs");;

Ghat := SmallGroup(CHIR1_ORDER, CHIR1_ID);;
if not G1_Test(Ghat) then
  outRec.status := "HANDOFF_MISMATCH";;
else
  entry := FindOneG2G3Pair(Ghat);;
  if not entry.ok then
    outRec.status := "HANDOFF_MISMATCH";;
  else
    U := entry.r;; W := entry.s;;
    xres := ComputeXgrp(Ghat, U, W);;
    Xgrp := xres.Xgrp;;
    kappa := Size(Xgrp);;
    xresMirror := ComputeXgrp(Ghat, U, W^-1);;
    kappaMirror := Size(xresMirror.Xgrp);;

    idX := fail;;
    if kappa <= 50000 then idX := IdGroup(Xgrp);; fi;
    excl := IsExcludedFamily(Xgrp);;
    factors := ChiefFactorsWithSectAndCoverage(Ghat, U, W, Xgrp);;

    c5ok := fail;;
    if kappa = 1 then
      c5ok := true;;
    else
      quoHom := NaturalHomomorphismByNormalSubgroup(Ghat, Xgrp);;
      R := Image(quoHom);;
      Ubar := Image(quoHom, U);; Wbar := Image(quoHom, W);;
      AutR := AutomorphismGroup(R);;
      c5ok := ForAny(AutR, alpha -> Image(alpha,Ubar) = Ubar and Image(alpha,Wbar) = Wbar^-1);;
    fi;

    outRec.status := "OK";;
    outRec.kappa := kappa;;
    outRec.kappa_mirror := kappaMirror;;
    outRec.id_X := idX;;
    outRec.X_abelian := IsAbelian(Xgrp);;
    outRec.X_in_center := IsSubset(Center(Ghat), Xgrp);;
    outRec.X_in_frattini := IsSubset(FrattiniSubgroup(Ghat), Xgrp);;
    outRec.X_in_derived := IsSubset(DerivedSubgroup(Ghat), Xgrp);;
    outRec.X_excluded_family := excl.excluded;;
    outRec.X_excluded_family_name := excl.family;;
    outRec.c3_ok := (Size(Ghat) mod kappa = 0);;
    outRec.c4_ok := (kappa = kappaMirror);;
    outRec.c5_ok := c5ok;;
    outRec.factors := factors;;
    outRec.num_relators := xres.num_relators;;
  fi;
fi;
outRec.wall_ms := GAPLIB_WallElapsedMs() - t0;;

#############################################################################
## write per-window JSON
#############################################################################
FactorsJson := function(factors)
  return JArr(List(factors, f -> Concatenation(
      "{\"index\":", String(f.index), ",\"order\":", String(f.order), ",\"p\":", String(f.p),
      ",\"d\":", String(f.d), ",\"sect_holds\":", JB(f.sect_holds), ",\"covers\":", JB(f.covers), "}")));
end;;

if outRec.status = "OK" then
  json := Concatenation(
    "{\"order\":", String(outRec.order), ",\"id\":", String(outRec.id),
    ",\"status\":", JStr(outRec.status), ",\"method\":", JStr(outRec.method),
    ",\"wall_ms\":", String(outRec.wall_ms), ",\"num_relators\":", String(outRec.num_relators),
    ",\"kappa\":", String(outRec.kappa), ",\"kappa_mirror\":", String(outRec.kappa_mirror),
    ",\"id_X\":", (function() if outRec.id_X=fail then return "null"; else return JArr(List(outRec.id_X,String)); fi; end)(),
    ",\"X_abelian\":", JB(outRec.X_abelian), ",\"X_in_center\":", JB(outRec.X_in_center),
    ",\"X_in_frattini\":", JB(outRec.X_in_frattini), ",\"X_in_derived\":", JB(outRec.X_in_derived),
    ",\"X_excluded_family\":", JB(outRec.X_excluded_family), ",\"X_excluded_family_name\":", JStr(outRec.X_excluded_family_name),
    ",\"canary_C3_ok\":", JB(outRec.c3_ok), ",\"canary_C4_ok\":", JB(outRec.c4_ok), ",\"canary_C5_ok\":", JB(outRec.c5_ok),
    ",\"covered_chief_factors\":", FactorsJson(outRec.factors), "}\n");;
else
  json := Concatenation(
    "{\"order\":", String(outRec.order), ",\"id\":", String(outRec.id),
    ",\"status\":", JStr(outRec.status), ",\"wall_ms\":", String(outRec.wall_ms), "}\n");;
fi;

OUT_PATH := Concatenation("scratchpad/chir1_window_", String(CHIR1_ORDER), "_", String(CHIR1_ID), ".json");;
WriteFile(OUT_PATH, json);;
Print("Wrote ", OUT_PATH, " wall_ms=", outRec.wall_ms, " status=", outRec.status, "\n");
Print("W6_SG_CHIR1_SINGLE_DONE\n");
QUIT;
