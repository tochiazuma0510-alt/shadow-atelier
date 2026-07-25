# week3-battery-A1-v2_1.g -- P92: settled witness search + (3.53) composition table for A1's
# 20 shadows. Produces certificates/A1.v2.1.json (gtsh-cert/v2.1, A1.v2.json is left untouched).
#
# Usage: .\gap.ps1 search\week3-battery-A1-v2_1.g
#
# settled witness: for shadow [m,f] (u=2m+1), search h ranging over ALL 120 elements of S5
# (Aut(A5) = S5 acting by conjugation, since A5 is simple with Out(A5)=C2) for
#   h^-1 * Xhat * h = Xhat^u          (paper's alpha(X)=X^u)
#   h^-1 * Yhat * h = f * Yhat^u * f^-1   (paper's alpha(Y) = f^-1 Y^u f, AbstractProd convention
#                                          -- same reversal as genB in EnumerateReducedHexagon,
#                                          kept consistent with what actually determined T_{m,f})
# reversal convention: "Ad(g)(v) = g v g^-1" (paper) <-> GAP's g^-1*v*g, established via A-F1f
# (tau=Ad(t): t^-1*X*t=Y, not t*X*t^-1=Y) and reused here for the SAME reason.

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

Xhat := (1,3,2,4,5);;
Yhat := (1,3,4,5,2);;
chat := ();;
A5 := Group(Xhat,Yhat);;
nOrd := 5;;
charmingSet := [0,1,3,4];;

qrec := rec(x:=Xhat, y:=Yhat, c:=chat, G:=A5);;
result := EnumerateReducedHexagon(qrec, charmingSet);;
Print("shadow_total = ", result.shadow_total, " (expect 20)\n");
if result.shadow_total <> 20 then
  Error("A1-v2.1: shadow_total != 20, stopping before settled search (fixture-equivalent halt)");
fi;

S5 := SymmetricGroup(5);;
S5elts := Elements(S5);;
Print("|S5| = ", Length(S5elts), " (expect 120)\n");

# ================================================================================
# settled witness search
# ================================================================================
settledDetail := [];;  settledCount := 0;;
t0 := Runtime();;
for sh in result.shadows do
  m := sh.m;  u := 2*m+1;  f := sh.f;
  targetX := Xhat^u;;
  targetY := AbstractProd([f^-1, Yhat^u, f]);;   # = f*Yhat^u*f^-1, AbstractProd convention
  witness := fail;;
  for h in S5elts do
    if h^-1*Xhat*h = targetX and h^-1*Yhat*h = targetY then
      witness := h;
      break;
    fi;
  od;
  if witness <> fail then
    settledCount := settledCount + 1;
    Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=true, witness:=witness));
  else
    Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=false, witness:=fail));
  fi;
od;
t1 := Runtime();;
Print("settled witness search: ", settledCount, "/", Length(result.shadows), " settled, time_ms=", t1-t0, "\n");

# ================================================================================
# (3.53) composition table on the 20 shadows: [m1,f1] o [m2,f2] = [2m1m2+m1+m2, f1.E_{m1,f1}(f2)]
# closure/identity/inverse observed (not assumed)
# ================================================================================
compTable := [];;  closureFail := 0;;
t0 := Runtime();;
for i1 in [1..Length(result.shadows)] do
  for i2 in [1..Length(result.shadows)] do
    m1 := result.shadows[i1].m;  f1 := result.shadows[i1].f;
    m2 := result.shadows[i2].m;  f2 := result.shadows[i2].f;
    u1 := 2*m1+1;
    imgx := Xhat^u1;
    imgy := AbstractProd([f1^-1, Yhat^u1, f1]);
    Ehom := GroupHomomorphismByImages(A5, A5, [Xhat,Yhat], [imgx,imgy]);
    if Ehom = fail then
      closureFail := closureFail + 1;
      Add(compTable, [i1-1, i2-1, -1]);
      continue;
    fi;
    newm := (2*m1*m2 + m1 + m2) mod nOrd;
    newf := AbstractProd([f1, Image(Ehom, f2)]);
    idx := fail;
    for t in [1..Length(result.shadows)] do
      if result.shadows[t].m = newm and result.shadows[t].f = newf then idx := t; break; fi;
    od;
    if idx = fail then
      closureFail := closureFail + 1;
      Add(compTable, [i1-1, i2-1, -1]);
    else
      Add(compTable, [i1-1, i2-1, idx-1]);
    fi;
  od;
od;
t1 := Runtime();;
Print("composition_table: ", Length(compTable), " entries (expect 400), closureFail=", closureFail, ", time_ms=", t1-t0, "\n");
closedObserved := (closureFail = 0);;
Print("[", PF(closedObserved), "] closure observed: all 400 products land in the 20-shadow set\n");

# identity check: is there an [m,f]=[0,1] entry, and does composing with it fix everything?
idIdx := fail;;
for t in [1..Length(result.shadows)] do
  if result.shadows[t].m = 0 and result.shadows[t].f = Identity(A5) then idIdx := t; break; fi;
od;
Print("identity element [0,1] present at index ", idIdx-1, " (fail=-1 if absent)\n");
idActsAsUnit := true;;
if idIdx <> fail then
  for i1 in [1..Length(result.shadows)] do
    entry := compTable[(i1-1)*Length(result.shadows) + idIdx];;
    if entry[3] <> i1-1 then idActsAsUnit := false; fi;
    entry2 := compTable[(idIdx-1)*Length(result.shadows) + i1];;
    if entry2[3] <> i1-1 then idActsAsUnit := false; fi;
  od;
fi;
Print("[", PF(idActsAsUnit), "] identity acts as two-sided unit (observed)\n");

# inverse check: for each i, is there j with compTable(i,j)=id and compTable(j,i)=id?
inverseExistsCount := 0;;
if idIdx <> fail then
  for i1 in [1..Length(result.shadows)] do
    hasInv := false;;
    for i2 in [1..Length(result.shadows)] do
      e1 := compTable[(i1-1)*Length(result.shadows)+i2];;
      e2 := compTable[(i2-1)*Length(result.shadows)+i1];;
      if e1[3] = idIdx-1 and e2[3] = idIdx-1 then hasInv := true; fi;
    od;
    if hasInv then inverseExistsCount := inverseExistsCount + 1; fi;
  od;
fi;
Print("inverse exists for ", inverseExistsCount, "/", Length(result.shadows), " shadows (observed)\n");

elapsedMs := Runtime() - startTime;;
Print("\n累計 elapsed ms: ", elapsedMs, "\n");

# ================================================================================
# certificate assembly (gtsh-cert/v2.1) -- extends A1.v2.json's content, A1.v2.json untouched
# ================================================================================
settledJson := [];;
for sd in settledDetail do
  if sd.settled then
    Add(settledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":true,\"witness\":\"", String(sd.witness), "\"}"));
  else
    Add(settledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":false,\"witness\":null}"));
  fi;
od;

compJson := [];;
for cti in compTable do Add(compJson, Concatenation("[",String(cti[1]),",",String(cti[2]),",",String(cti[3]),"]")); od;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2.1\",",
  "\"base\":\"certificates/A1.v2.json (unmodified; this is an EXTENSION certificate, P92)\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-A1-v2_1.g\",\"date\":\"2026-07-26\"},",
  "\"settled_witness\":{",
  "\"method\":\"brute force over all 120 elements of S5 = Aut(A5) (conjugation), checking h^-1 X h = X^u and h^-1 Y h = f Y^u f^-1 (AbstractProd/genB convention)\",",
  "\"settled_count\":", String(settledCount), ",\"total\":", String(Length(result.shadows)), ",",
  "\"detail\":", JArr(settledJson),
  "},",
  "\"composition_3_53\":{",
  "\"entries\":", JArr(compJson), ",",
  "\"closed_observed\":", JB(closedObserved), ",\"closure_fail_count\":", String(closureFail), ",",
  "\"identity_index\":", String(idIdx-1), ",\"identity_is_unit_observed\":", JB(idActsAsUnit), ",",
  "\"inverse_exists_count\":", String(inverseExistsCount), ",\"total\":", String(Length(result.shadows)),
  "},",
  "\"runtime\":{\"wall_seconds\":", String(Int((elapsedMs/1000.0)*1000)/1000.0), "}",
  "}");;

WriteFile("certificates/A1.v2.1.json", s);;
Print("wrote certificates/A1.v2.1.json\n");
QUIT;
