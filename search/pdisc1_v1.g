## search/pdisc1_v1.g -- P-DISC-1 (裁定823/827, docs/見立て_相2_v1_1.md §6.2 table:
## "TWIST-GCD と TWIST-6-ABS が分かれる実例(r>=5 ∧ r|e ∧ r|p-1)の存否", chi_semantics=切片読み).
## Commander's concrete instantiation (裁定827): test whether B3 admits a surjection onto
## G := C11 : C10 (faithful action, i.e. the full holomorph Hol(C11) = AGL(1,11) = the Frobenius
## group of order 110). This is the r=10 case: p=11 (characteristic of the normal C11), r=10=p-1
## (Aut(C11)=C10 realized FAITHFULLY, i.e. maximally). TWIST-GCD's bound is gcd(e,p-1)=gcd(e,10)
## (could allow r up to 10 if 10|e); TWIST-6-ABS's bound is gcd(e,6,p-1)=gcd(e,6,10)<=gcd(6,10)=2
## (caps r at <=2, since 10 and 6 share only the factor 2) -- a genuine divergence point IF such
## a quotient (with the C11 appearing as a genuine 1-dimensional NORMAL-in-NORMAL chief-series
## SECTION, per CHI-CARRY's chi_semantics=section discipline) actually exists.
##
## Method: build B3 as a finitely-presented group (braid relation aba=bab, standard 2-generator
## presentation used throughout this project's lins/census scripts), build G=C11:C10 (faithful
## holomorph, order 110) as a permutation group, and test GQuotients(B3, G) -- existence of ANY
## epimorphism B3 ->> G (up to Aut(G)-equivalence, GAP's own GQuotients semantics). Frozen
## prediction (per the task's own framing "不在", i.e. absence -- consistent with TWIST-6-ABS's
## tighter r<=6 cap winning over TWIST-GCD's looser r<=10 allowance): GQuotients(B3,G) = empty.
## Raw boolean result only, no verdict language written here.
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");

## ---- B3 as a finitely-presented group (verbatim setup pattern from search/lins-*.g) ----
BF3 := FreeGroup("a", "b");;
aa := BF3.1;;  bb := BF3.2;;
brel := aa * bb * aa * (bb * aa * bb)^-1;;
B3 := BF3 / [brel];;

## ---- G = C11 : C10 (faithful holomorph of C11 = AGL(1,11), order 110) ----
## Built via the standard permutation representation: C11 acting on {0,...,10} by translation,
## C10 acting by multiplication by a primitive root mod 11 (giving a FAITHFUL action, i.e. the
## full automorphism group Aut(C11)=C10 is realized, not a proper subgroup of it).
g11 := PrimitiveRootMod(11);;
Print("primitive root mod 11 = ", g11, "\n");

transPerm := PermList(List([0..10], x -> (x+1) mod 11) + 1);;   # translation by 1 on {0..10} (1-indexed via +1)
multPerm := PermList(List([0..10], x -> (x*g11) mod 11) + 1);;  # multiplication by g11 on {0..10}

## sanity: translation has order 11, multiplication has order 10 (faithful, since g11 is a
## primitive root -- order exactly phi(11)=10, not a proper divisor)
transOrd := Order(transPerm);;
multOrd := Order(multPerm);;
Print("order(translation) = ", transOrd, " (expect 11) order(multiplication) = ", multOrd, " (expect 10)\n");

G := Group(transPerm, multPerm);;
gOrder := Size(G);;
Print("|G| = ", gOrder, " (expect 110)\n");
gOrderOk := (gOrder = 110);;

## sanity: C11 is normal in G, and G/C11 has order 10 (i.e. C10 acts faithfully -- if the action
## were NOT faithful, |G| would be smaller than 110)
C11sub := Subgroup(G, [transPerm]);;
c11Normal := IsNormal(G, C11sub);;
Print("C11 normal in G: ", c11Normal, " |C11| = ", Size(C11sub), "\n");

## ---- GQuotients(B3, G) ----
t0 := GAPLIB_WallElapsedMs();;
quo := GQuotients(B3, G);;
t1 := GAPLIB_WallElapsedMs();;
quoCount := Length(quo);;
quoEmpty := (quoCount = 0);;
Print("GQuotients(B3, G): count=", quoCount, " empty=", quoEmpty, " elapsed_ms=", t1-t0, "\n");

## ============ JSON output ============
out := Concatenation(
  "{",
  "\"schema\":\"shadow-atelier/pdisc1_v1\",",
  "\"authority\":\"", "\\u88c1\\u5b9a823/827 -- docs/\\u898b\\u7acb\\u3066_\\u76f82_v1_1.md \\u00a76.2 (P-DISC-1)\",",
  "\"predicate_note\":\"tests whether B3 admits a surjection onto G=C11:C10 (faithful holomorph of C11, order 110) via GQuotients(B3,G). r=10=p-1 case: TWIST-GCD bound gcd(e,10) (could allow up to 10), TWIST-6-ABS bound gcd(e,6,10)<=2 -- a genuine divergence point if such a quotient exists with C11 as a genuine 1-dim chief-series section (chi_semantics=section per CHI-CARRY).\",",
  "\"frozen_prediction\":\"absence (GQuotients(B3,G) empty), consistent with TWIST-6-ABS's tighter bound winning\",",
  "\"chi_semantics\":\"section\",",
  "\"G_construction\":\"AGL(1,11) = C11:C10, faithful action via multiplication by a primitive root mod 11\",",
  "\"g_order\":", String(gOrder), ",",
  "\"g_order_expected\":110,",
  "\"g_order_ok\":", JB(gOrderOk), ",",
  "\"translation_order\":", String(transOrd), ",",
  "\"multiplication_order\":", String(multOrd), ",",
  "\"c11_normal_in_g\":", JB(c11Normal), ",",
  "\"gquotients_count\":", String(quoCount), ",",
  "\"gquotients_empty\":", JB(quoEmpty), ",",
  "\"elapsed_ms\":", String(t1-t0), ",",
  "\"no_verdict_note\":\"raw boolean gquotients_empty and counts only. \\u5224\\u5b9a\\u8a9e\\u306f\\u4e00\\u5207\\u66f8\\u304b\\u306a\\u3044 -- \\u767a\\u52b9\\u306f\\u53f8\\u4ee4\\u5854\\u5c02\\u6a29\\u3002\"",
  "}"
);;

WriteFile("search/certs/pdisc1_v1_20260812.json", out);;
Print("Wrote search/certs/pdisc1_v1_20260812.json\n");
Print("PDISC1_DONE\n");
QUIT;
