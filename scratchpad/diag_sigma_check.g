Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

CheckGF8();;
Smat := MakeMatGF8(1,0,1,1);;
Tmat := MakeMatGF8(4,3,1,5);;
Sperm := MatToPermGF8(Smat);;
Tperm := MatToPermGF8(Tmat);;
wPerm := Sperm * Tperm^-1;;
Xperm := wPerm^2;;
Yperm := Sperm^-1 * Xperm * Sperm;;
Pgrp := Group(Xperm, Yperm);;

WordEval := function(fword, xg, yg)
  local items, pr, g;
  if Length(fword) = 0 then return xg^0; fi;
  items := [];
  for pr in fword do
    if pr[1] = "x" then g := xg; else g := yg; fi;
    Add(items, g^pr[2]);
  od;
  return AbstractProd(items);
end;;

# reuse parser via copy-paste (small enough)
ParseS4SettledWitness := function(path)
  local content, stream, mk1, pos, sStart, mk2, sEnd, body, out, p, mPos, j,
        digitStr, mVal, fwMk, fwStart, depth, k, fwEnd, fwBody, items, ip, sym,
        expSign, expDigits, expVal, wMk, wStart, wEnd, wStr, wPermVal;
  stream := InputTextFile(path);
  content := ReadAll(stream);
  CloseStream(stream);
  mk1 := "\"settled_detail\":[";
  pos := FindPositionFrom(content, mk1, 1);
  sStart := pos + Length(mk1);
  mk2 := "],\"settled_count\":";
  sEnd := FindPositionFrom(content, mk2, sStart);
  body := content{[sStart .. sEnd-1]};
  out := [];
  p := 1;
  while true do
    mPos := FindPositionFrom(body, "\"m\":", p);
    if mPos = fail then break; fi;
    j := mPos + 4;
    digitStr := "";
    while j <= Length(body) and body[j] in "0123456789" do
      Append(digitStr, [body[j]]);  j := j+1;
    od;
    mVal := Int(digitStr);
    fwMk := "\"f_word\":[";
    fwStart := FindPositionFrom(body, fwMk, mPos);
    k := fwStart + Length(fwMk) - 1;
    depth := 0;  fwEnd := fail;
    while k <= Length(body) do
      if body[k] = '[' then depth := depth + 1;
      elif body[k] = ']' then
        depth := depth - 1;
        if depth = 0 then fwEnd := k; break; fi;
      fi;
      k := k + 1;
    od;
    fwBody := body{[fwStart+Length(fwMk) .. fwEnd-1]};
    items := [];
    ip := 1;
    while true do
      ip := FindPositionFrom(fwBody, "\"", ip);
      if ip = fail then break; fi;
      sym := fwBody[ip+1];
      ip := ip + 4;
      expSign := 1;
      if ip <= Length(fwBody) and fwBody[ip] = '-' then expSign := -1; ip := ip+1; fi;
      expDigits := "";
      while ip <= Length(fwBody) and fwBody[ip] in "0123456789" do
        Append(expDigits, [fwBody[ip]]);  ip := ip+1;
      od;
      expVal := expSign * Int(expDigits);
      Add(items, [[sym], expVal]);
      ip := ip + 1;
    od;
    wMk := "\"automorphism_witness\":\"";
    wStart := FindPositionFrom(body, wMk, fwEnd);
    wStart := wStart + Length(wMk);
    wEnd := FindPositionFrom(body, "\"", wStart);
    wStr := body{[wStart .. wEnd-1]};
    wPermVal := EvalString(wStr);
    Add(out, rec(m := mVal, fword := items, witness := wPermVal));
    p := wEnd + 1;
  od;
  return out;
end;;

s4 := ParseS4SettledWitness("certificates/S4.v2.json");;
Print("parsed ", Length(s4), "\n");

Sym9 := SymmetricGroup(9);;
PBList := List(s4, r -> WordEval(r.fword, Xperm, Yperm));;
PCertList := List(s4, r -> r.witness);;

Print("=== cycle type comparison (first 10 rows) ===\n");
for i in [1..10] do
  Print("  row ", i, " m=", s4[i].m, " PB=", CycleStructurePerm(PBList[i]),
        " Pcert=", CycleStructurePerm(PCertList[i]),
        " sameCycleType=", (CycleStructurePerm(PBList[i])=CycleStructurePerm(PCertList[i])), "\n");
od;

matchCount := 0;;
for i in [1..Length(s4)] do
  if CycleStructurePerm(PBList[i]) = CycleStructurePerm(PCertList[i]) then matchCount := matchCount+1; fi;
od;
Print("cycle-type-matching rows (necessary condition for any global sigma) = ", matchCount, " / ", Length(s4), "\n");

QUIT;
