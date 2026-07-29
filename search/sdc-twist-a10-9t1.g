# search/sdc-twist-a10-9t1.g -- SD-c certificate: twist exponent a for W-E-A10-9t1.
#
# Purpose (裁定 227 / P86-5 item 3): the j-value table behind "a = +1" was measured in a
# throwaway scratchpad script (便 86 F86-4.1.3 NOTE 3: "監査可能な証明書が無い").
# This is the versioned re-measurement. Raw measurements only; no comparison to any
# prediction file. NOT a ledger claim by itself (single GAP implementation).
#
# What is measured:
#   (1) window asserts, independently of kerchi-judge (|Bq|, |P|, ord x/y, c=id, N_ord)
#   (2) C_{Aut(P)}(X) and N_{Aut(P)}(<X>) with Aut(A_10) = S_10
#   (3) the m=0 layer F_0 = ker chi~ by EXHAUSTIVE scan over P (all 1814400 elements),
#       using the same (F2)+settled predicate as kerchi-judge v1.3
#   (4) for each [0,f] in F_0, the unique j with Phi_{0,f} = inn(X^j)  (searched over j=0..8)
#
# The paper step (surj_s4_v1.md lemma 7.1) is: Phi is a homomorphism (lemma Phi-univ) and
# Phi_{m,f}(X) = X^u, so conjugation by a chi~-value-u shadow sends inn(X^j) -> inn(X^{ju}).
# Hence  Phi|_{F_0} bijective onto inn(<X>)  ==>  twist a = +1.  Only the bijectivity is
# measured here; the implication is paper.

SizeScreen([4096, 0]);;

OUT := "search/certs/sdc_twist_W_E_A10_9t1_20260730.json";;

s1 := (1,2,3,4,5,6,7,8,9)(11,12);;
s2 := (1,5,10,3,9,7,8,6,2)(12,13);;
a1 := (1,2)(3,5)(4,10)(6,9);;
b1 := (2,9,5)(3,4,10)(6,8,7);;

Bq := Group(s1,s2);;
x := s1^2;; y := s2^2;;
Dlt := s1*s2*s1;; dlt := s1*s2;; c := Dlt^2;;
P := Group(x,y);;
id := Identity(Bq);;
Nord := Lcm(Order(x),Order(y),Order(c));;

asserts := [];;
AddAssert := function(lab, ok)
  Add(asserts, rec(label := lab, ok := ok));
  Print("[", ok, "] ", lab, "\n");
end;;

AddAssert("a1^2 = 1 and b1^3 = 1", a1^2 = () and b1^3 = ());;
AddAssert("braid relation s1 s2 s1 = s2 s1 s2", s1*s2*s1 = s2*s1*s2);;
AddAssert("|Bq| = 6*|A10| = 10886400", Size(Bq) = 6*Factorial(10)/2);;
AddAssert("|P| = |A10| = 1814400", Size(P) = Factorial(10)/2);;
AddAssert("ord(xbar) = 9", Order(x) = 9);;
AddAssert("ord(ybar) = 9", Order(y) = 9);;
AddAssert("c = identity in Bq (c in N)", c = id);;
AddAssert("N_ord = lcm(9,9,1) = 9", Nord = 9);;

# Aut(A_10) = S_10 (n <> 6).  X is a 9-cycle on {1..9} fixing 10.
S10 := SymmetricGroup(10);;
CX := Centralizer(S10, x);;
NX := Normalizer(S10, Group(x));;
idNX := IdGroup(NX);;
AddAssert("C_{S10}(X) = <X> (order 9)", Size(CX) = 9);;
AddAssert("|N_{S10}(<X>)| = 54", Size(NX) = 54);;
AddAssert("IdGroup(N_{S10}(<X>)) = [54,6] (= Hol(Z/9))", idNX = [54,6]);;

TH := function(g) return Dlt*g*Dlt^-1; end;;
TT := function(g) return dlt*g*dlt^-1; end;;
RtOf := function(m,f) local Wd; Wd := y^m*f; return TT(TT(Wd))*TT(Wd)*Wd; end;;

# ---- m = 0 layer, exhaustive over P (same predicate as kerchi-judge v1.3) ----
F0 := [];;  scanned := 0;;  settledFails := 0;;
for f in P do
  scanned := scanned + 1;
  if f*TH(f) <> id then continue; fi;
  if RtOf(0,f) <> id then continue; fi;
  if Size(Group(x, f^-1*y*f)) <> Size(P) then continue; fi;
  if GroupHomomorphismByImages(Bq,Bq,[s1,s2],[s1, f^-1*s2*f]) = fail then
    settledFails := settledFails + 1;  continue;
  fi;
  Add(F0, f);
od;
Print("scanned=", scanned, " |F_0|=", Length(F0), " settled_fail=", settledFails, "\n");
AddAssert("scanned = |P| (exhaustive)", scanned = Size(P));;
AddAssert("|F_0| = 9 (matches ker_size = 9 of the xi-restricted ladder certificate)", Length(F0) = 9);;
# NOTE (do NOT assert settled_fail = 0 here): the ladder certificate reports
# settled_fail_count = 0 under scan_mode = "xi_restricted" (486 candidates scanned).
# This script scans the FULL candidate set (1814400) and therefore sees ill-defined
# candidates that the Xi restriction never enumerates.  Both are consistent about the
# ACCEPTED set (|F_0| = 9 here, ker_size = 9 there); settled_fail_count is a property of
# the scanned candidate set, not of the window.  Recorded as a measurement, not a gate.

# ---- Phi_{0,f} = inn(X^j) ?  (Phi_{0,f}: X -> X, Y -> f^-1 Y f) ----
rows := [];;  jvals := [];;  allFound := true;;
for f in F0 do
  jj := -1;
  for j in [0..8] do
    if f^-1*y*f = x^j*y*x^-j then jj := j; break; fi;
  od;
  if jj = -1 then allFound := false; fi;
  Add(jvals, jj);
  Add(rows, rec(f := String(f), j := jj));
od;
Print("j-values = ", jvals, "\n");
AddAssert("every Phi_{0,f} lies in inn(<X>)", allFound);;
AddAssert("j-map is a bijection onto Z/9", Set(jvals) = [0..8]);;

bijective := allFound and (Set(jvals) = [0..8]);;
allPass := ForAll(asserts, r -> r.ok);;

JB := function(b) if b then return "true"; else return "false"; fi; end;;
JArrStr := function(l) local i,s; s := "[";
  for i in [1..Length(l)] do
    if i > 1 then Append(s, ","); fi;
    Append(s, Concatenation("\"", l[i], "\""));
  od;
  Append(s, "]"); return s; end;;
JArrInt := function(l) local i,s; s := "[";
  for i in [1..Length(l)] do
    if i > 1 then Append(s, ","); fi;
    Append(s, String(l[i]));
  od;
  Append(s, "]"); return s; end;;

assertJson := "[";;
for i in [1..Length(asserts)] do
  if i > 1 then Append(assertJson, ","); fi;
  Append(assertJson, Concatenation("{\"label\":\"", asserts[i].label, "\",\"ok\":", JB(asserts[i].ok), "}"));
od;
Append(assertJson, "]");

rowJson := "[";;
for i in [1..Length(rows)] do
  if i > 1 then Append(rowJson, ","); fi;
  Append(rowJson, Concatenation("{\"f\":\"", rows[i].f, "\",\"j\":", String(rows[i].j), "}"));
od;
Append(rowJson, "]");

s := Concatenation(
  "{\n",
  "  \"schema\": \"sdc-twist/v1\",\n",
  "  \"generated_by\": {\"tool\": \"GAP 4.16.0\", \"script\": \"search/sdc-twist-a10-9t1.g\"},\n",
  "  \"note\": \"SD-c versioned re-measurement (裁定 227 / P86-5 item 3). Raw measurements only. Single GAP implementation -- NOT cross-checked, NOT a ledger claim by itself.\",\n",
  "  \"window_id\": \"W-E-A10-9t1\",\n",
  "  \"window_ref_cert\": \"search/certs/a13_ladder_W_E_A10_9t1_20260730.json\",\n",
  "  \"s1\": \"", String(s1), "\",\n",
  "  \"s2\": \"", String(s2), "\",\n",
  "  \"a1\": \"", String(a1), "\",\n",
  "  \"b1\": \"", String(b1), "\",\n",
  "  \"abs_Bq\": ", String(Size(Bq)), ",\n",
  "  \"abs_P\": ", String(Size(P)), ",\n",
  "  \"ord_x\": ", String(Order(x)), ",\n",
  "  \"ord_y\": ", String(Order(y)), ",\n",
  "  \"c_in_N\": ", JB(c = id), ",\n",
  "  \"N_ord\": ", String(Nord), ",\n",
  "  \"aut_P\": \"S_10 (Aut(A_10), n<>6)\",\n",
  "  \"centralizer_X_order\": ", String(Size(CX)), ",\n",
  "  \"normalizer_X_order\": ", String(Size(NX)), ",\n",
  "  \"normalizer_X_idgroup\": ", JArrInt(idNX), ",\n",
  "  \"scan_mode\": \"exhaustive_over_P\",\n",
  "  \"scanned\": ", String(scanned), ",\n",
  "  \"F0_size\": ", String(Length(F0)), ",\n",
  "  \"settled_fail_count_m0_exhaustive\": ", String(settledFails), ",\n",
  "  \"settled_fail_count_note\": \"Scan-set-relative quantity, NOT a window invariant. The ladder certificate reports settled_fail_count=0 under scan_mode=xi_restricted (486 candidates); this exhaustive scan of all 1814400 candidates sees ill-defined candidates the Xi restriction never enumerates. The two agree on the ACCEPTED set (F0_size=9 here, ker_size=9 there). Reading 'settled_fail_count=0' as 'the window has no ill-defined candidates' is an over-read.\",\n",
  "  \"j_table\": ", rowJson, ",\n",
  "  \"j_values\": ", JArrInt(jvals), ",\n",
  "  \"phi_F0_into_inn_X\": ", JB(allFound), ",\n",
  "  \"phi_F0_bijective_onto_inn_X\": ", JB(bijective), ",\n",
  "  \"twist_exponent_a\": ", "\"+1 (paper implication from bijectivity; see surj_s4_v1.md lemma 7.1)\"", ",\n",
  "  \"asserts\": ", assertJson, ",\n",
  "  \"all_pass\": ", JB(allPass), "\n",
  "}\n");;

PrintTo(OUT, s);
Print("wrote ", OUT, "\n");
Print("all_pass = ", allPass, "  bijective = ", bijective, "\n");
QUIT;
