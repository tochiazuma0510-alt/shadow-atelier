#############################################################################
## search/probe/sg_band_sweep/sg_g9_characteristic_driver_v1.g
## GAP-G9-1 (裁定683 小任務): for the 3 windows where SECT broke on a 3^2
## chief factor ((1296,2889),(1296,3487),(1728,31096)), confirm that M,L
## (the chief-series terms bounding that factor, A=M/L) are CHARACTERISTIC
## subgroups of Ghat -- the missing premise of theorem SECT-CHIRAL
## (theorem_check_mirrorall_l3vacuous_v1.md SSG.9.1,【GAP-G9-1】).
##
## Cheapest sufficient conditions tested, per the note's own instruction
## ("最も安価な十分条件"):
##   (a) UNIQUE NORMAL SUBGROUP of that order in Ghat -- if there is only
##       one normal subgroup of size |M| (resp. |L|), any automorphism
##       permutes normal subgroups of that order among themselves, so a
##       unique one is fixed setwise, i.e. characteristic.
##   (b) COINCIDES WITH A TERM of a standard characteristic series/subgroup:
##       LowerCentralSeries, UpperCentralSeries, DerivedSeries,
##       FittingSubgroup, PCore(Ghat,p) for p in {2,3} (=O_p(Ghat)),
##       FrattiniSubgroup, Center -- all characteristic by construction.
## If NEITHER holds for M or for L, that group's promotion to "紙定理+機械
## 入力" stays open (grade remains 機械のみ), reported honestly, not forced.
##
## (r,s)=(U,W) per window: independently rediscovered, same method as
## sg_g4_orb_driver_v1.g / sg_pband2prime_driver_v1.g's entry gate.
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;

S3grp := SymmetricGroup(3);;
TARGET_WINDOWS := [ rec(order:=1296,id:=2889), rec(order:=1296,id:=3487), rec(order:=1728,id:=31096) ];;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_g9_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then Error("sha256 fail for ", relpath); fi;
  return line{[1 .. 64]};
end;;

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

## Cheapest-sufficient-condition characteristic test for a subgroup H of G.
CharacteristicCheck := function(Ghat, H)
  local hsize, normsOfSize, uniqueNormal, stdSubs, matchName, name, S, found;
  hsize := Size(H);;
  normsOfSize := Filtered(NormalSubgroups(Ghat), N -> Size(N) = hsize);;
  uniqueNormal := (Length(normsOfSize) = 1);;
  if uniqueNormal and normsOfSize[1] <> H then
    ## sanity: the unique normal subgroup of this order should BE H if H
    ## is itself normal of that order; if H isn't even normal, this
    ## uniqueness test doesn't apply to H directly
    uniqueNormal := IsNormal(Ghat,H) and (Size(normsOfSize[1])=hsize);
  fi;
  matchName := fail;;
  if hsize > 1 then
    stdSubs := [
      rec(name:="LowerCentralSeries", list:=LowerCentralSeries(Ghat)),
      rec(name:="UpperCentralSeries", list:=UpperCentralSeries(Ghat)),
      rec(name:="DerivedSeries", list:=DerivedSeries(Ghat)),
      rec(name:="FittingSubgroup", list:=[FittingSubgroup(Ghat)]),
      rec(name:="PCore_2", list:=[PCore(Ghat,2)]),
      rec(name:="PCore_3", list:=[PCore(Ghat,3)]),
      rec(name:="FrattiniSubgroup", list:=[FrattiniSubgroup(Ghat)]),
      rec(name:="Center", list:=[Center(Ghat)])
    ];;
    for S in stdSubs do
      for found in S.list do
        if Size(found) = hsize and found = H then
          matchName := S.name;;
        fi;
      od;
    od;
  fi;
  return rec(is_normal := IsNormal(Ghat,H), unique_normal_of_order := uniqueNormal,
      matches_standard_characteristic_term := matchName,
      characteristic_confirmed := uniqueNormal or (matchName <> fail));
end;;

RESULTS := [];;

for w in TARGET_WINDOWS do
  Print("\n=== GAP-G9-1 window (", w.order, ",", w.id, ") ===\n");
  Ghat := SmallGroup(w.order, w.id);;
  if not G1_Test(Ghat) then Error("unexpected G1 failure on known window"); fi;
  entry := FindOneG2G3Pair(Ghat);;
  if not entry.ok then Error("unexpected entry-gate failure on known window"); fi;
  r := entry.r;; s := entry.s;;

  series := ChiefSeries(Ghat);;
  found39 := false;;
  for i in [1..Length(series)-1] do
    Ni := series[i];; Nip1 := series[i+1];;
    if Size(Ni) = Size(Nip1) then continue; fi;
    hom := NaturalHomomorphismByNormalSubgroup(Ni, Nip1);;
    Q := Image(hom);;
    order := Size(Q);;
    if order <> 9 then continue; fi;
    p := 3;; d := 2;;
    isoQpc := IsomorphismPcGroup(Q);;
    Qpc := Image(isoQpc);;
    pcgsQ := Pcgs(Qpc);;
    muU := ImmutableMatrix(GF(p), ActionMatrixOnFactor(Ni, Nip1, hom, isoQpc, pcgsQ, p, r));;
    muW := ImmutableMatrix(GF(p), ActionMatrixOnFactor(Ni, Nip1, hom, isoQpc, pcgsQ, p, s));;
    GLdp := GL(d,p);;
    C := Centralizer(GLdp, muU);;
    sectHolds := IsConjugate(C, muW, muW^-1);;
    if sectHolds then continue; fi;   ## only interested in the BROKEN 3^2 factor

    found39 := true;;
    Print("  found broken 3^2 factor: |Ni|=", Size(Ni), " |Nip1|=", Size(Nip1), "\n");
    checkM := CharacteristicCheck(Ghat, Ni);;
    checkL := CharacteristicCheck(Ghat, Nip1);;
    Print("  M(=Ni,  order ", Size(Ni), "): normal=", checkM.is_normal,
          " unique_normal_of_order=", checkM.unique_normal_of_order,
          " std_match=", checkM.matches_standard_characteristic_term,
          " => characteristic_confirmed=", checkM.characteristic_confirmed, "\n");
    Print("  L(=Nip1,order ", Size(Nip1), "): normal=", checkL.is_normal,
          " unique_normal_of_order=", checkL.unique_normal_of_order,
          " std_match=", checkL.matches_standard_characteristic_term,
          " => characteristic_confirmed=", checkL.characteristic_confirmed, "\n");

    bothConfirmed := checkM.characteristic_confirmed and checkL.characteristic_confirmed;;
    Print("  BOTH M,L characteristic-confirmed: ", bothConfirmed, "\n");
    Print("  ==> grade: ", (function()
        if bothConfirmed then return "紙定理+機械入力 (SECT-CHIRAL applies)";
        else return "機械のみ (characteristic premise NOT confirmed by cheap tests)"; fi;
      end)(), "\n");

    Add(RESULTS, rec(order := w.order, id := w.id, M_order := Size(Ni), L_order := Size(Nip1),
        M_check := checkM, L_check := checkL, both_confirmed := bothConfirmed));;
  od;
  if not found39 then
    Print("  WARNING: no broken 3^2 factor found on re-scan (unexpected -- earlier cert disagrees)\n");
    Add(RESULTS, rec(order := w.order, id := w.id, M_order := fail, L_order := fail,
        M_check := fail, L_check := fail, both_confirmed := fail, note := "RESCAN_MISMATCH"));;
  fi;
od;;

Print("\n=== GAP-G9-1 summary ===\n");
for res in RESULTS do
  Print("  (", res.order, ",", res.id, "): both_confirmed=", res.both_confirmed, "\n");
od;

#############################################################################
## cert output
#############################################################################
CheckJson := function(c)
  if c = fail then return "null"; fi;
  return Concatenation("{\"is_normal\":", JB(c.is_normal),
      ",\"unique_normal_of_order\":", JB(c.unique_normal_of_order),
      ",\"matches_standard_characteristic_term\":",
      (function() if c.matches_standard_characteristic_term=fail then return "null"; else return JStr(c.matches_standard_characteristic_term); fi; end)(),
      ",\"characteristic_confirmed\":", JB(c.characteristic_confirmed), "}");
end;;

RowsJson := JArr(List(RESULTS, res -> Concatenation(
    "{\"order\":", String(res.order), ",\"id\":", String(res.id),
    ",\"M_order\":", (function() if res.M_order=fail then return "null"; else return String(res.M_order); fi; end)(),
    ",\"L_order\":", (function() if res.L_order=fail then return "null"; else return String(res.L_order); fi; end)(),
    ",\"M_check\":", CheckJson(res.M_check), ",\"L_check\":", CheckJson(res.L_check),
    ",\"both_confirmed\":", (function() if res.both_confirmed=fail then return "null"; else return JB(res.both_confirmed); fi; end)(),
    ",\"grade\":", (function()
        if res.both_confirmed = true then return JStr("紙定理+機械入力");
        elif res.both_confirmed = false then return JStr("機械のみ");
        else return JStr("RESCAN_MISMATCH"); fi;
      end)(),
    "}")));;

selfSha := ComputeSha256File("search/probe/sg_band_sweep/sg_g9_characteristic_driver_v1.g");;
noteSha := ComputeSha256File("docs/notes/theorem_check_mirrorall_l3vacuous_v1.md");;

cert := Concatenation(
"{\n",
"\"schema\":\"shadow-atelier/sg-g9-characteristic/v1\",\n",
"\"driver_self_sha256\":", JStr(selfSha), ",\n",
"\"authority\":\"裁定683 (司令塔), GAP-G9-1 per docs/notes/theorem_check_mirrorall_l3vacuous_v1.md SSG.9.1 (verbatim)\",\n",
"\"design_doc\":{\"path\":\"docs/notes/theorem_check_mirrorall_l3vacuous_v1.md\",\"sha256\":", JStr(noteSha), "},\n",
"\"target_windows\":[{\"order\":1296,\"id\":2889},{\"order\":1296,\"id\":3487},{\"order\":1728,\"id\":31096}],\n",
"\"method_note\":\"For each window, ChiefSeries(Ghat) is rebuilt and re-scanned for the broken 3^2 factor (SECT re-verified as a sanity check, using the same matrices/method as sg_pband2prime_driver_v1.g). For the bounding terms M=Ni,L=Nip1, two CHEAPEST-SUFFICIENT characteristic tests are applied: (a) uniqueness of the normal subgroup of that order in Ghat; (b) coincidence with a term of LowerCentralSeries/UpperCentralSeries/DerivedSeries/FittingSubgroup/PCore(Ghat,2)/PCore(Ghat,3)/FrattiniSubgroup/Center. characteristic_confirmed = (a) OR (b). If neither holds, the premise stays open (NOT forced) and the window's grade remains 機械のみ.\",\n",
"\"rows\":", RowsJson, ",\n",
"\"claims\":{\"note\":\"raw structural measurement only; whether SECT-CHIRAL formally applies (i.e. whether the 3 pairs promote to 紙定理+機械入力) is reported per-window below via characteristic_confirmed; overall grading/promotion decision is 司令塔/数学者's call\"},\n",
"\"non_contact_declaration\":{\"im_R\":false,\"d_N\":false,\"sealed_quantities\":false,\"n5_series\":false}\n",
"}\n");;

OUT_PATH := "search/certs/sg_g9_characteristic_20260806.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nW6_SG_G9_DONE\n");
QUIT;
