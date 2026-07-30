# sdc_twist_s4_window.g -- SD-c certificate: twist exponent for window B (S4 = PSL(2,8), |P|=504).
#
# Purpose (裁定244 工程1): docs/notes/surj_s4_v2.md sec7.1 cited
# search/certs/sdc_twist_W_E_A10_9t1_20260730.json as "the S4-window SD-c certificate", but that
# certificate in fact measured window A (P=A10, W-E-A10-9t1), not window B (S4 = PSL(2,8), the
# window surj_s4_v2.md is actually about). Both windows happen to share C(X)=9, N(<X>)=54, which
# made the mix-up hard to spot. This script produces the genuine window-B certificate.
#
# Style mirrors search/sdc-twist-a10-9t1.g (SAME field layout: window asserts independent of
# kerchi-judge.g, C_{Sn}(X)/N_{Sn}(<X>), exhaustive F0 scan, j-table, phi bijectivity, all_pass).
# Raw measurements only. Single GAP implementation -- NOT cross-checked (no second independent
# system reproduces this), NOT a ledger claim by itself.
#
# Window B generators: S,T matrices over GF(8) acting on P^1(F_8) (9 points), matching the fixture
# in search/week3-psl-S4.g (Smat=[[1,0],[1,1]], Tmat=[[4,3],[1,5]], MakeMatGF8 encoding
# a0+2a1+4a2 <-> a0+a1*x+a2*x^2, x^3=x+1). The GF(8) bit-arithmetic and the P^1(F_8) permutation
# action are REIMPLEMENTED here from scratch (own functions, not by Read()-ing
# search/week3-psl-common.g) so this script does not import kerchi-judge.g or its machinery.
#
# Bq (the B3-quotient realized on this window) is built via the Q x T transversal-cocycle model
# (docs/wp2-transversal-model.md, 12-rule table; same recipe search/week3-battery-common.g's
# BuildQTGeneral implements -- reimplemented inline here, independently of that file, since it is
# a documented model, not kerchi-judge-specific code). phi_C is taken as the identity of the
# 9-point window group (c_in_N), matching the window fixture already established in
# search/week3-psl-S4.g / certificates/S4.v2.json and paper-proved in
# docs/notes/surj_s4_v2.md sec3.6 (W5Q-S4) -- NOT re-derived from scratch by this script.
# What IS independently computed from the resulting s1,s2 (not assumed): braid relation,
# |Bq|=6*504, xx:=s1^2, yy:=s2^2, Dlt:=s1*s2*s1, dlt:=s1*s2, c:=Dlt^2, and whether c actually
# equals the identity of Bq (the genuine c_in_N check, same definition as kerchi-judge.g's
# MakeWindow / search/sdc-twist-a10-9t1.g).

SizeScreen([4096, 0]);;

OUT := "search/certs/sdc_twist_S4_window_20260731.json";;

# ---- own GF(8) bit arithmetic (encoding a0+a1*x+a2*x^2 <-> a0+2*a1+4*a2, x^3=x+1) ----
BitOfInt := function(n, i) return RemInt(QuoInt(n, 2^i), 2); end;;
XorInt := function(a, b)
  local result, i;
  result := 0;
  for i in [0..6] do
    if (BitOfInt(a,i) + BitOfInt(b,i)) mod 2 = 1 then result := result + 2^i; fi;
  od;
  return result;
end;;
CMul := function(a,b)
  local result, i;
  result := 0;
  for i in [0..2] do
    if BitOfInt(b,i) = 1 then result := XorInt(result, a*2^i); fi;
  od;
  return result;
end;;
CReduce := function(p)
  local i, result;
  result := p;
  for i in [4,3] do
    if BitOfInt(result, i) = 1 then result := XorInt(result, 11 * 2^(i-3)); fi;
  od;
  return result;
end;;
GMul := function(a,b) return CReduce(CMul(a,b)); end;;
GInv := function(a)
  local b;
  if a = 0 then Error("GInv: no inverse of 0"); fi;
  for b in [1..7] do if GMul(a,b) = 1 then return b; fi; od;
  Error("GInv: not found");
end;;
GAdd := function(a,b) return XorInt(a,b); end;;

selfchk := (GMul(GMul(2,2),2) = GAdd(2,1));;
Print("[", selfchk, "] GF(8) self-check: x^3 = x+1 (x=2)\n");
if not selfchk then Error("GF8 arithmetic self-check FAILED"); fi;

MatToStrLocal := function(M)
  return Concatenation("[[",String(M[1][1]),",",String(M[1][2]),"],[",String(M[2][1]),",",String(M[2][2]),"]]");
end;;

# P^1(F_8): 9 points, index 1 = infinity, 2+v for v in 0..7
MatToPerm8 := function(M)
  local images, x, a, b, c, d, num, den;
  a := M[1][1];  b := M[1][2];  c := M[2][1];  d := M[2][2];
  images := [];
  if c = 0 then images[1] := 1; else images[1] := 2 + GMul(a, GInv(c)); fi;
  for x in [0..7] do
    num := GAdd(GMul(a,x), b);
    den := GAdd(GMul(c,x), d);
    if den = 0 then images[2+x] := 1; else images[2+x] := 2 + GMul(num, GInv(den)); fi;
  od;
  return PermList(images);
end;;

asserts := [];;
AddAssert := function(lab, ok)
  Add(asserts, rec(label := lab, ok := ok));
  Print("[", ok, "] ", lab, "\n");
end;;

Smat := [[1,0],[1,1]];;
Tmat := [[4,3],[1,5]];;
DetS := GAdd(GMul(Smat[1][1],Smat[2][2]), GMul(Smat[1][2],Smat[2][1]));;
DetT := GAdd(GMul(Tmat[1][1],Tmat[2][2]), GMul(Tmat[1][2],Tmat[2][1]));;
AddAssert("det(S) <> 0", DetS <> 0);;
AddAssert("det(T) <> 0", DetT <> 0);;

Sperm := MatToPerm8(Smat);;
Tperm := MatToPerm8(Tmat);;
AddAssert("ord(S) = 2", Order(Sperm) = 2);;
AddAssert("ord(T) = 3", Order(Tperm) = 3);;

wPerm := Sperm*Tperm^-1;;
xg := wPerm^2;;
yg := Sperm^-1*xg*Sperm;;
ygViaT := Tperm^-1*xg*Tperm;;
zg := Tperm^-2*xg*Tperm^2;;
idg := ();;

AddAssert("ord(w) = 9 (e)", Order(wPerm) = 9);;
AddAssert("ord(x) = 9", Order(xg) = 9);;
AddAssert("ord(y) = 9", Order(yg) = 9);;
AddAssert("y = S^-1 x S = T^-1 x T", yg = ygViaT);;
AddAssert("x*y*z = 1 (XYZ=1, reversed convention)", zg*yg*xg = idg);;

Pgrp := Group(xg,yg);;
AddAssert("|P| = |<x,y>| = 504", Size(Pgrp) = 504);;
AddAssert("P simple", IsSimpleGroup(Pgrp));;
AddAssert("<S,T> = P (order 504)", Size(Group(Sperm,Tperm)) = 504);;

# ---- Bq via the Q x T (transversal-cocycle) model (docs/wp2-transversal-model.md, 12-rule
# table); reimplemented inline (own copy, not Read()-ing week3-battery-common.g), independent
# of kerchi-judge.g.  phiC = identity of Pgrp (c_in_N per the window fixture; see header note). ----
Qelts := Elements(Pgrp);;
np := Length(Qelts);;
posDict := NewDictionary(Qelts[1], true);;
for i in [1..np] do AddDictionary(posDict, Qelts[i], i); od;
posOf := function(v) return LookupDictionary(posDict, v); end;;
phiX := xg;;  phiY := yg;;  phiC := idg;;
phiXi := phiX^-1;;  phiYi := phiY^-1;;
imgS1 := [];;  imgS2 := [];;
for t in [1..6] do
  for i in [1..np] do
    d := Qelts[i];  pt := (t-1)*np + i;
    if t=1 then val:=d; tp:=2;
    elif t=2 then val:=d*phiX; tp:=1;
    elif t=3 then val:=d; tp:=5;
    elif t=4 then val:=d; tp:=6;
    elif t=5 then val:=d*phiXi*phiYi*phiC; tp:=3;
    else val:=d*phiY; tp:=4; fi;
    imgS1[pt] := (tp-1)*np + posOf(val);
    if t=1 then val:=d; tp:=3;
    elif t=2 then val:=d; tp:=4;
    elif t=3 then val:=d*phiY; tp:=1;
    elif t=4 then val:=d*phiYi*phiXi*phiC; tp:=2;
    elif t=5 then val:=d; tp:=6;
    else val:=d*phiX; tp:=5; fi;
    imgS2[pt] := (tp-1)*np + posOf(val);
  od;
od;
s1 := PermList(imgS1);;
s2 := PermList(imgS2);;
Bq := Group(s1,s2);;
id := Identity(Bq);;

AddAssert("braid relation s1 s2 s1 = s2 s1 s2", s1*s2*s1 = s2*s1*s2);;
AddAssert("|Bq| = 6*|P| = 3024", Size(Bq) = 6*504);;

x := s1^2;;  y := s2^2;;
P := Group(x,y);;
Dlt := s1*s2*s1;;  dlt := s1*s2;;  c := Dlt^2;;

AddAssert("ord(xx) = ord(x) = 9 (Bq-level embedding of x is faithful)", Order(x) = 9);;
AddAssert("ord(yy) = ord(y) = 9 (Bq-level embedding of y is faithful)", Order(y) = 9);;
AddAssert("|PN| = |Group(xx,yy)| = 504 (Bq-level embedding of P is faithful)", Size(P) = 504);;
AddAssert("c = identity in Bq (c in N)", c = id);;

Nord := Lcm(Order(x), Order(y), Order(c));;
AddAssert("N_ord = lcm(9,9,1) = 9", Nord = 9);;

# Aut(P) for P = PSL(2,8) acting on the 9 points of P^1(F_8): P <= S_9 via the same natural
# action used to build x,y above; the ambient symmetric group is S_9 (degree of THIS window,
# NOT Aut(PSL(2,8))=PGammaL(2,8), matching the field convention of search/sdc-twist-a10-9t1.g,
# which used S_10 = Aut(A_10), the symmetric group on the window's own domain).
S9 := SymmetricGroup(9);;
CX := Centralizer(S9, xg);;
NX := Normalizer(S9, Group(xg));;
idNX := IdGroup(NX);;
AddAssert("C_{S9}(X) = <X> (order 9)", Size(CX) = 9);;
AddAssert("|N_{S9}(<X>)| = 54", Size(NX) = 54);;
AddAssert("IdGroup(N_{S9}(<X>)) = [54,6] (= Hol(Z/9))", idNX = [54,6]);;

TH := function(g) return Dlt*g*Dlt^-1; end;;
TT := function(g) return dlt*g*dlt^-1; end;;
RtOf := function(m,f) local Wd; Wd := y^m*f; return TT(TT(Wd))*TT(Wd)*Wd; end;;

# ---- m = 0 layer, exhaustive over P (= PN, the Bq-embedded copy of PSL(2,8); same predicate
# style as kerchi-judge.g's CorrectedShadowsLegacy / search/sdc-twist-a10-9t1.g) ----
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
AddAssert("|F_0| = 9 (matches e = M = 9 of the window, docs/notes/surj_s4_v2.md sec1)", Length(F0) = 9);;

# ---- Phi_{0,f} = inn(x^j) ?  (Phi_{0,f}: x -> x, y -> f^-1 y f) ----
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
AddAssert("every Phi_{0,f} lies in inn(<x>)", allFound);;
AddAssert("j-map is a bijection onto Z/9", Set(jvals) = [0..8]);;

bijective := allFound and (Set(jvals) = [0..8]);;
allPass := ForAll(asserts, r -> r.ok);;

JB := function(b) if b then return "true"; else return "false"; fi; end;;
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
  "  \"generated_by\": {\"tool\": \"GAP 4.16.0\", \"script\": \"search/probe/wac_v1/sdc_twist_s4_window.g\"},\n",
  "  \"note\": \"SD-c certificate for window B (S4 = PSL(2,8)), produced under 裁定244 工程1 to correct docs/notes/surj_s4_v2.md sec7.1, which had cited the WINDOW-A (P=A10) certificate sdc_twist_W_E_A10_9t1_20260730.json by mistake. Raw measurements only. Single GAP implementation -- NOT cross-checked, NOT a ledger claim by itself.\",\n",
  "  \"window_id\": \"S4-window-B-PSL2_8\",\n",
  "  \"window_note\": \"本 cert は P=PSL(2,8) の S4 窓(docs/notes/surj_s4_v2.md sec1)。A10 窓の search/certs/sdc_twist_W_E_A10_9t1_20260730.json とは別物 -- C(X)=9・N(<X>)=54 が両窓で一致するのは数値上の偶然であり、窓としては別(P=PSL(2,8) 対 P=A10)。\",\n",
  "  \"window_ref_note\": \"docs/notes/surj_s4_v2.md sec1 (P=PSL(2,8), |P|=504, M=e=9), certificates/S4.v2.json (existing window fixture, produced by a different script: search/week3-psl-S4.g / RunPSLWindow, not kerchi-judge.g)\",\n",
  "  \"Smat\": \"", MatToStrLocal(Smat), "\",\n",
  "  \"Tmat\": \"", MatToStrLocal(Tmat), "\",\n",
  "  \"abs_Bq\": ", String(Size(Bq)), ",\n",
  "  \"abs_P\": ", String(Size(P)), ",\n",
  "  \"ord_x\": ", String(Order(x)), ",\n",
  "  \"ord_y\": ", String(Order(y)), ",\n",
  "  \"c_in_N\": ", JB(c = id), ",\n",
  "  \"N_ord\": ", String(Nord), ",\n",
  "  \"aut_ambient\": \"S_9 (natural degree-9 domain of the window, matching the field convention of search/sdc-twist-a10-9t1.g which used S_10)\",\n",
  "  \"centralizer_X_order\": ", String(Size(CX)), ",\n",
  "  \"normalizer_X_order\": ", String(Size(NX)), ",\n",
  "  \"normalizer_X_idgroup\": ", JArrInt(idNX), ",\n",
  "  \"scan_mode\": \"exhaustive_over_P\",\n",
  "  \"scanned\": ", String(scanned), ",\n",
  "  \"F0_size\": ", String(Length(F0)), ",\n",
  "  \"settled_fail_count_m0_exhaustive\": ", String(settledFails), ",\n",
  "  \"j_table\": ", rowJson, ",\n",
  "  \"j_values\": ", JArrInt(jvals), ",\n",
  "  \"phi_F0_into_inn_X\": ", JB(allFound), ",\n",
  "  \"phi_F0_bijective_onto_inn_X\": ", JB(bijective), ",\n",
  "  \"twist_exponent_a\": ", "\"+1 (paper implication from bijectivity; same logical step as surj_s4_v1.md lemma 7.1 / search/sdc-twist-a10-9t1.g)\"", ",\n",
  "  \"asserts\": ", assertJson, ",\n",
  "  \"all_pass\": ", JB(allPass), "\n",
  "}\n");;

# NOTE (修理・裁定244 追い便): naive PrintTo(OUT, s) wraps long lines at the SizeScreen
# column width (max 4096, itself capped by GAP -- raising SizeScreen further does NOT help,
# confirmed by direct test) by inserting a literal "\" + newline mid-string, which corrupts
# the JSON (this window's permutation strings run to ~4000+ chars each, unlike the A10 window's
# short ones, so the SizeScreen([4096,0]) trick alone -- sufficient for
# search/sdc-twist-a10-9t1.g -- is not sufficient here). Fix: write via a stream with
# SetPrintFormattingStatus(f, false), which disables line-wrap formatting outright (same
# technique as WriteFile() in search/week3-battery-common.g), reimplemented inline here.
outStream := OutputTextFile(OUT, false);;
SetPrintFormattingStatus(outStream, false);;
PrintTo(outStream, s);;
CloseStream(outStream);;
Print("wrote ", OUT, "\n");
Print("all_pass = ", allPass, "  bijective = ", bijective, "\n");
QUIT;
