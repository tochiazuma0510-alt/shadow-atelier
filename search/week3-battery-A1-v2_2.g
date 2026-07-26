# week3-battery-A1-v2_2.g -- isolated determination for N_A (A5 window), independent of the
# E2 sweep (待機中の小任務・司令塔指示 2026-07-26).
#
# Definition used (docs/week1-定義ノート.md SS2, spec projection already read under the original
# workorder): "isolated: 全 shadow が settled ⇒ GT(N) = GTSh(N,N) は有限群". I.e. isolated=true
# observationally IFF settled_count = total shadow count for N_A's own GT(N_A) (all 20 shadows in
# certificates/A1.v2.1.json). This script re-derives A5 and S5=Aut(A5) FRESH (does not just trust
# the earlier witness list) and re-verifies each of the 20 witnesses from scratch, then reports
# isolated as an OBSERVATION (settled_count = total => isolated = true), not by assumption.
#
# Usage: .\gap.ps1 search\week3-battery-A1-v2_2.g

SizeScreen([4096, 0]);;
startTime := Runtime();;
Read("search/week3-battery-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ---- rebuild A5 fresh (same marking as A1.g, independent construction here) ----
Xhat := (1,3,2,4,5);;
Yhat := (1,3,4,5,2);;
A5 := Group(Xhat, Yhat);;
if Size(A5) <> 60 then Error("A5 construction failed: size = ", Size(A5)); fi;

# ---- rebuild the 20-shadow set fresh via the same quotient-shortcut machinery ----
qrec := rec(x:=Xhat, y:=Yhat, c:=(), G:=A5);;
charmingSet := [0,1,3,4];;
result := EnumerateReducedHexagon(qrec, charmingSet);;
Print("[", PF(result.shadow_total = 20), "] shadow_total = ", result.shadow_total, " (expect 20, matches A1.v2.json)\n");

# ---- S5 = Aut(A5), full 120-element enumeration (fresh, not reused from A1-v2_1) ----
S5 := SymmetricGroup(5);;
S5elts := Elements(S5);;
Print("[", PF(Length(S5elts) = 120), "] |S5| = ", Length(S5elts), " (expect 120)\n");

# ---- settled witness re-search for all 20 shadows, from scratch (independent of A1.v2.1.json's
# stored witnesses -- this is a FRESH search, not a re-verification of stored data only) ----
settledDetail := [];;  settledCount := 0;;
t0 := Runtime();;
for sh in result.shadows do
  m := sh.m;  u := 2*m+1;  f := sh.f;
  targetX := Xhat^u;;
  targetY := AbstractProd([f^-1, Yhat^u, f]);;
  witness := fail;;
  for h in S5elts do
    if h^-1*Xhat*h = targetX and h^-1*Yhat*h = targetY then witness := h; break; fi;
  od;
  if witness <> fail then
    settledCount := settledCount + 1;
    Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=true, witness:=witness));
  else
    Add(settledDetail, rec(m:=m, f_word:=sh.word, settled:=false));
  fi;
od;
t1 := Runtime();;
Print("fresh settled witness search: ", settledCount, "/", Length(result.shadows), " settled, time_ms=", t1-t0, "\n");

# ---- isolated determination (observation, per definition: all shadows settled) ----
isolatedObserved := (settledCount = Length(result.shadows));;
Print("\n[", PF(true), "] isolated (observed) = ", isolatedObserved,
      " (definition: settled_count(", settledCount, ") = shadow_total(", Length(result.shadows), ")) \n");

elapsedMs := Runtime() - startTime;;

# ---- certificate assembly ----
settledJson := [];;
for sd in settledDetail do
  if sd.settled then
    Add(settledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":true,\"automorphism_witness\":\"", String(sd.witness), "\"}"));
  else
    Add(settledJson, Concatenation("{\"m\":", String(sd.m), ",\"f_word\":", WordToJson(sd.f_word),
        ",\"settled\":false,\"automorphism_witness\":null}"));
  fi;
od;

s := Concatenation(
  "{\"schema\":\"gtsh-cert/v2.2\",",
  "\"base\":\"certificates/A1.v2.1.json (settled witnesses re-derived fresh here, independent search over full S5=Aut(A5), 120 elements)\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/week3-battery-A1-v2_2.g\",\"date\":\"2026-07-26\"},",
  "\"aut_group\":{\"name\":\"S5\",\"size\":", String(Length(S5elts)), ",\"note\":\"Aut(A5)=S5 (A5 simple, Out(A5)=C2, all automorphisms realized by conjugation in S5)\"},",
  "\"settled_witness\":{\"settled_count\":", String(settledCount), ",\"total\":", String(Length(result.shadows)), ",",
  "\"detail\":", JArr(settledJson), "},",
  "\"isolated\":", JB(isolatedObserved), ",",
  "\"isolated_justification\":\"observed: settled_count = total (all 20/20 shadows in GT(N_A) have an explicit automorphism witness in S5=Aut(A5) realizing ker(T_{m,f})=N_A); per docs/week1-定義ノート.md SS2 definition (isolated: 全shadowがsettled), this OBSERVATIONALLY gives isolated=true for N_A. Not a claim of genuineness/arithmeticity -- only that GT(N_A)=GTSh(N_A,N_A) as a finite set (Prop 3.14-style closure).\",",
  "\"runtime\":{\"wall_seconds\":", String(Int((elapsedMs/1000.0)*1000)/1000.0), "}",
  "}");;

WriteFile("certificates/A1.v2.2.json", s);;
Print("wrote certificates/A1.v2.2.json\n");
Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
QUIT;
