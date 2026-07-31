#############################################################################
## search/probe/wac_v1/pent_t2t3_v31_20260731.g
##  v3.1 -- extension of pent_t2t3_v3_20260731.g (repaired coarse<->fine
##  label convention, kept byte-identical below; see that file's header for
##  the full repair history). v3 is left in place unmodified.
##
##  Commander's remaining work item (settled measurement / source kernel,
##  full 20 rows): v3's SourceKernelInfo machinery (imported verbatim from
##  pent_t2t3_v2_20260731.g, itself imported from docs/week1-定義ノート.md
##  Prop 3.2/(3.53)/settled+isolated Thm 3.10) already iterates over `lift`,
##  which under the v3 repair contains all 20 coarse shadows (all 20 rows
##  have lift_exists=true in pent_t2t3_v3_20260731.json). This file:
##   (a) makes that "all 20" fact an explicit, machine-checked PRECONDITION
##       (hard Error() gate) rather than an incidental consequence of the
##       current window's numbers, so the settled measurement below is
##       provably over all 20 coarse shadows, not just "however many lifted";
##   (b) adds an explicit, machine-checked HEXAGON GATE on each lift before
##       computing K_pi^s: T_{m,f}(c) = c^{2m+1} is a PROPOSITION of C1
##       (arXiv 2008.00066 Cor 2.8 (2.29)), proved FROM the hexagon
##       relations (2.18)/(2.19) -- it is licensed only for (m,f) that have
##       already passed hexagon (c1 and c2 in Chk6). Applying it to a pair
##       that failed hexagon would be applying a consequence of a false
##       hypothesis. Per docs/notes/pent_conflict_diagnosis_v1.md sec.1.2:
##       "実装上の含意: source kernel を ker(Psi o T_{m,f}) として組むとき、
##       c->c^{2m+1} を使ってよいのは hexagon を通った (m,f) に限る". Since
##       every one of the 20 lift entries in v3 has all6_pass=1 (c1..c5 all
##       true for the chosen witness q, in particular c1=c2=true = hexagon
##       passed for that q), the gate is expected to pass vacuously-true for
##       all 20 here -- but it is CHECKED, not assumed, per-lift, with a hard
##       Error() abort (not a silent skip) if any lift's witness turns out
##       not to have passed hexagon;
##   (c) renames the JSON field source_kernel_per_lift -> settled_per_lift
##       (commander's naming) and adds a settled_summary rollup (counts:
##       total / well_defined_on_QP / settled=true / settled=false /
##       not well_defined) so the "full 20 rows" claim is auditable from the
##       cert alone without re-counting the array by hand;
##   (d) records, verbatim, the level caveat from
##       docs/notes/pent_conflict_diagnosis_v1.md sec.1.4 (SURVIVED into v2,
##       see pent_conflict_diagnosis_v2.md sec.4 table): C1 Prop 2.11 defines
##       the source kernel N_s := ker(T^{PB_4}_{m,f}) at PB_4 level. This
##       script's (and v2/v3's) measurement |PB_3/K_pi^s| vs |PB_3/(K_pi)_PB3|
##       is a PB_3-level statement. (N_s)_PB3 = (N)_PB3 does NOT imply
##       N_s = N. What is established here is "settled at PB_3 level" =
##       a NECESSARY CONDITION for PB_4-level settled, not the PB_4-level
##       claim itself. This caveat is unresolved (diagnosis sec.7 priority 4,
##       "発注推奨" -- getting the PB_4-level kernel needs T^{B_4} (2.25)
##       built on PB_4/K_pi, sigma_3-component phi_{12,3,4}(f) conjugation is
##       new and not built here). NOT claimed fixed by this file.
##
##  No exponent-match-only claim is used as a settled proof (Sol warning /
##  裁定 pitfall discipline): "settled" below always means the literal kernel
##  computation Kernel(hom) with Size(K)=1, not an index/order coincidence.
##
##  Contact-blocked: no expected settled-count value is asserted anywhere in
##  this file (only the hexagon-gate and all-20-lifted preconditions, which
##  are construction-level invariants of the v3 repair, are hard-asserted).
##  Single GAP lane. NOT a ledger claim -- report to commander for review.
#############################################################################

## ---- window (byte-identical to pent_t2t3_v3_20260731.g / v2) ----
n := 5;;
tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;;
b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
Nord := Lcm(Order(xb),Order(yb),Order(cc));;
charm := Filtered([0..Nord-1], z->GcdInt(2*z+1,Nord)=1);;
Print("== window ==  P=A5? ",PN=AlternatingGroup(5),"  |E|=",Size(Eg),
      "  c=1 in E? ",cc=(),"  N_ord=",Nord,"  charming=",charm,"\n");

X12v := xb;; X23v := yb;; X13v := yb^-1*xb^-1;;
X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;
cof := [ [ X12v, X23v, X13v ],
         [ X23v, X34v, X24v ],
         [ X23v*X13v, X34v, X24v*X14v ],
         [ X13v*X12v, X34v*X24v, X14v ],
         [ X12v, X24v*X23v, X14v*X13v ] ];;
cofc := List([1..5], i -> cof[i][2]*cof[i][3]*cof[i][1]);;

D5 := DirectProduct(Eg,Eg,Eg,Eg,Eg);;
emb := List([1..5], i -> Embedding(D5,i));;
Pack := function(l) return Product(List([1..5], i -> Image(emb[i], l[i]))); end;;
Fw := FreeGroup("x","y","c");;
gx := GeneratorsOfGroup(Fw)[1];; gy := GeneratorsOfGroup(Fw)[2];;
gc := GeneratorsOfGroup(Fw)[3];;
Rev := function(w)
  local l, r;
  l := LetterRepAssocWord(w); r := Reversed(l);
  return AssocWordByLetterRep(FamilyObj(gx), r);
end;;
PsiAt := function(w, i)
  return MappedWord(Rev(w), [gx,gy,gc], [cof[i][1],cof[i][2],cofc[i]]);
end;;
Psi := function(w) return Pack(List([1..5], i -> PsiAt(w,i))); end;;
one5 := One(D5);;
QP := Group(Psi(gx), Psi(gy), Psi(gc));;
QF := Group(Psi(gx), Psi(gy));;
pr1 := Projection(D5,1);;
Print(" |PB3/(K_pi)_{PB3}| = ",Size(QP),"   |F2/(K_pi)_{F2}| = ",Size(QF),
      "   ord(Psi(c))=",Order(Psi(gc)),"\n");
H3 := Kernel(GroupHomomorphismByImages(QP, PN,
        [Psi(gx),Psi(gy),Psi(gc)], [xb,yb,()]));;

## ---- (v3 FIX, imported verbatim) forward coarse-label machinery ----------
gensQP := [Psi(gx),Psi(gy),Psi(gc)];;
redMap := GroupHomomorphismByImages(QP, PN, gensQP, [xb,yb,()]);;
Print(" redMap : QP -> PN well-defined? ", redMap<>fail, "\n");
coarse_of := function(w) return MappedWord(w, [gx,gy,gc], [xb,yb,()]); end;;

## ---- sigma-conjugation (identical to v2/v3) ----
X13w := gx^-1*gc*gy^-1;;
SubW := function(w, ix, iy, ic)
  return MappedWord(w, [gx,gy,gc], [ix,iy,ic]);
end;;
Aut1 := function(w) return SubW(w, gx, gy^-1*X13w*gy, gc); end;;
Aut2 := function(w) return SubW(w, X13w, gy, gc); end;;

## ---- coarse GT(N_A) ----
Hex := function(m,f)
  local u; u := 2*m+1;
  return s1^u*f^-1*s2^u*f = f^-1*s1*s2*xb^(-m)*cc^m and
         f^-1*s2^u*f*s1^u = s2*s1*yb^(-m)*cc^m*f;
end;;
shad := [];;
for m in charm do for f in Elements(PN) do
  if Hex(m,f) and Group(xb,yb^f)=PN then Add(shad,[m,f]); fi;
od; od;
Print(" |GT(N_A)| = ",Length(shad),"   distinct f = ",
      Length(Set(List(shad,z->z[2]))),"\n");

epiP := GroupHomomorphismByImages(Fw, QP, [gx,gy,gc],
          [Psi(gx),Psi(gy),Psi(gc)]);;
WordOf := function(q) return Rev(PreImagesRepresentative(epiP,q)); end;;

Pent := function(w)
  local v;
  v := List([1..5], i -> PsiAt(w,i));
  return v[1]*v[4]*v[2] = v[3]*v[5];
end;;

Chk6 := function(m, q)
  local w, P0, R0, S0, D1, D2, c1, c2, c3, c4, c5, sb, u;
  w := WordOf(q); u := 2*m+1;
  P0 := gx^m * w^-1 * Aut2(gy^m * w);
  R0 := (X13w*gy)^m;
  D1 := Aut1(P0) * (Aut1(Aut2(R0)))^-1 * w;
  c1 := Psi(D1) = one5;
  S0 := (gx*X13w)^m;
  D2 := w^-1 * Aut2(gy^m*w) * Aut2(Aut1(gx^m))
        * ( Aut2(Aut1(S0)) * Aut2(Aut1(w)) )^-1;
  c2 := Psi(D2) = one5;
  c3 := Pent(w);
  c4 := (q in DerivedSubgroup(QP));
  sb := Group(Psi(gx^u), Psi(w^-1*gy^u*w));
  c5 := (Size(sb) = Size(QF));
  return [c1,c2,c3,c4,c5, c1 and c2 and c3 and c4 and c5];
end;;

## ---- (v3 FIX, imported) regression unit test element 4, run again here
## unchanged (diagnosis sec.5 mandatory regression gate; inherited from v3
## per commander instruction "回帰 unit test 第4元も v3 から引き継ぎ実行").
WordFromBits := function(bits)
  local w, b;
  w := One(Fw);
  for b in bits do
    if b = 0 then w := w * gx; else w := w * gy; fi;
  od;
  return w;
end;;
Print("\n== regression unit test element 4 (non-self-inverse f round trip, inherited from v3) ==\n");
r4_bits := [1,0,0,1,0,0,0,1,1,1];;  ## author word bits, y x^2 y x^3 y^3
r4_m := 0;;
r4_w := WordFromBits(r4_bits);;
r4_f_forward := coarse_of(r4_w);;
r4_self_inverse := (r4_f_forward = r4_f_forward^-1);;
Print("  bits=",r4_bits,"  forward coarse f=",String(r4_f_forward),
      "  self_inverse=",r4_self_inverse,"\n");
if r4_self_inverse then
  Error("REGRESSION TEST SETUP FAIL: chosen element-4 witness is self-inverse ",
        "-- it cannot detect the pr1/redMap orientation bug. Choose a different ",
        "non-self-inverse f before proceeding.");
fi;
r4_q := Psi(r4_w);;
r4_f_roundtrip := coarse_of(WordOf(r4_q));;
r4_f_legacy_pr1 := Image(pr1, r4_q);;
r4_f_legacy_redMap := Image(redMap, r4_q);;
Print("  round-trip coarse label (via coarse_of o WordOf, THE FIX) = ",
      String(r4_f_roundtrip),"\n");
Print("  legacy pr1-image (old v2 bug, informative only) = ",
      String(r4_f_legacy_pr1),"\n");
Print("  legacy redMap-image (dead-end first attempt, informative only) = ",
      String(r4_f_legacy_redMap),"\n");
r4_roundtrip_pass := (r4_f_roundtrip = r4_f_forward);;
if not r4_roundtrip_pass then
  Error("REGRESSION FAIL: coarse<->fine label round-trip broken for ",
        "non-self-inverse f = ", String(r4_f_forward),
        " -- got back ", String(r4_f_roundtrip),
        ". This is the exact bug pattern of pent_t2t3_v2_20260731.g ",
        "(diagnosis pent_conflict_diagnosis_v2.md sec 1.2-1.3). Halting.");
fi;
Print("  REGRESSION TEST 4 PASS: round trip is the identity on a ",
      "non-self-inverse f.\n");

## ---- precompute forward coarse labels for all of QP (same as v3) --------
Print("\n== precomputing forward coarse labels coarse_of(WordOf(q)) for all |QP|=",
      Size(QP)," elements ==\n");
qpElts := Elements(QP);;
coarseLabelOf := List(qpElts, q -> coarse_of(WordOf(q)));;
Print("  done.\n");

## ============================================================
## (2) per-shadow witness cert: iterate ALL 20 coarse shadows
##     (identical logic to v3 -- coarse_of o WordOf fiber selection)
## ============================================================
Print("\n== (2) witness rows for all coarse shadows ==\n");
rows := [];;
lift := [];;   ## [m, f, q] triples that pass Chk6 fully
sid := 0;;
for z in shad do
  m := z[1];; f := z[2];;
  fibIdx := Filtered([1..Length(qpElts)], idx -> coarseLabelOf[idx] = z[2]);
  fib := List(fibIdx, idx -> qpElts[idx]);
  tab := List(fib, q -> Chk6(m,q));
  c1n := Number(tab,r->r[1]);; c2n := Number(tab,r->r[2]);;
  c3n := Number(tab,r->r[3]);; c4n := Number(tab,r->r[4]);;
  c5n := Number(tab,r->r[5]);; allN := Number(tab,r->r[6]);;
  witIdx := First([1..Length(fib)], i -> tab[i][6]);
  row := rec(shadow_id := sid, m := m, f_perm := String(f),
             c1_pass := c1n, c2_pass := c2n, c3_pass := c3n,
             c4_pass := c4n, c5_pass := c5n, all6_pass := allN,
             fiber_size := Length(fib));
  if witIdx <> fail then
    q := fib[witIdx];
    w := WordOf(q);
    row.lift_exists := true;
    row.witness_h_word := String(w);
    row.five_coface_images := List([1..5], i -> String(PsiAt(w,i)));
    row.hexagon_pass_for_witness := (tab[witIdx][1] and tab[witIdx][2]);
    Add(lift, [m,f,q]);
  else
    row.lift_exists := false;
    row.witness_h_word := "null";
    row.five_coface_images := "null";
    row.hexagon_pass_for_witness := "null";
    dies := [];
    if c1n=0 then Add(dies,"c1"); fi;
    if c2n=0 then Add(dies,"c2"); fi;
    if c3n=0 then Add(dies,"c3"); fi;
    if c4n=0 then Add(dies,"c4"); fi;
    if c5n=0 then Add(dies,"c5"); fi;
    row.dies_at := dies;
  fi;
  Add(rows, row);
  Print("  id=",sid," m=",m," f=",String(f)," c1..c5=",
        [c1n,c2n,c3n,c4n,c5n]," all=",allN,
        " lift=",row.lift_exists,"\n");
  sid := sid + 1;
od;
Print("  TOTAL lifted = ",Length(lift),"/",Length(shad),"\n");

## ============================================================
## (v3.1 NEW) PRECONDITION GATE: all 20 coarse shadows must have lifted.
## This is the fact the commander's "全 20 行拡張" instruction depends on --
## made a hard, machine-checked precondition here (not assumed from v3's
## prose) before the settled measurement below is computed.
## ============================================================
if Length(shad) <> 20 then
  Error("PRECONDITION FAIL: window does not have exactly 20 coarse shadows ",
        "(got ", Length(shad), "). The 'full 20 rows' extension does not ",
        "apply to this window. Halting before settled measurement.");
fi;
if Length(lift) <> 20 then
  Error("PRECONDITION FAIL: not all 20 coarse shadows lifted (got ",
        Length(lift), "/20). This contradicts the v3 repair result ",
        "(pent_t2t3_v3_20260731.json: lifted_total=20). Halting before ",
        "settled measurement -- do not silently measure a partial set.");
fi;
Print("\nPRECONDITION PASS: all 20/20 coarse shadows lifted (matches v3).\n");

## ============================================================
## (1, v3.1 extension) settled measurement (source kernel) for ALL 20 lifts.
## Definition (imported, cited): docs/week1-定義ノート.md Prop 3.2/(3.53)/
## settled+isolated (Thm 3.10): T_{m,f} on PB3 generators
##   x |-> x^{2m+1},  y |-> f^-1 y^{2m+1} f,  c |-> c^{2m+1}.
##   K_pi^s(m,f) := ker( Psi o T_{m,f} ).  "settled" iff K_pi^s = K_pi.
## HEXAGON GATE (v3.1 new, per pent_conflict_diagnosis_v1.md sec.1.2): the
## c |-> c^{2m+1} rule is a PROPOSITION (C1 Cor 2.8 (2.29)) proved USING the
## hexagon relations -- licensed only for (m,f) that passed hexagon (c1,c2
## true for the witness q). Checked per-lift below with a hard Error() abort,
## not assumed.
## ============================================================
Print("\n== (1, v3.1) settled measurement for ALL 20 lifts ==\n");
SourceKernelInfo := function(m, q)
  local u, phix, phiy, phic, hom, K;
  u := 2*m+1;
  phix := Psi(gx)^u;
  phiy := q^-1 * Psi(gy)^u * q;
  phic := Psi(gc)^u;
  hom := GroupHomomorphismByImages(QP, QP, gensQP, [phix,phiy,phic]);
  if hom = fail then
    return rec(well_defined_on_QP := false, note :=
      "T_{m,f} does not descend to QP: some relator of (K_pi)_{PB3} is not killed by T_{m,f} -- (K_pi)_{PB3} is not contained in K_pi^s.");
  fi;
  K := Kernel(hom);
  return rec(well_defined_on_QP := true,
             kernel_ratio_K := Size(K),
             Kpi_s_quotient_size := Size(QP)/Size(K),
             Kpi_quotient_size := Size(QP),
             settled := (Size(K) = 1));
end;;

srcRows := [];;
hexGateFails := [];;
for tr in lift do
  m := tr[1];; f := tr[2];; q := tr[3];;
  ## hexagon gate: recompute c1,c2 for this exact witness q (not just trust
  ## the row cache) before licensing c |-> c^{2m+1}.
  chkq := Chk6(m,q);;
  if not (chkq[1] and chkq[2]) then
    Add(hexGateFails, [m, String(f)]);
    Print("  HEXAGON GATE FAIL at m=",m," f=",String(f),
          " -- c1=",chkq[1]," c2=",chkq[2],
          " -- T_{m,f}(c)=c^{2m+1} NOT licensed for this pair. Skipping settled measurement for this lift.\n");
  else
    info := SourceKernelInfo(m,q);
    Add(srcRows, rec(m:=m, f_perm:=String(f), info:=info));
    if info.well_defined_on_QP then
      Print("  m=",m," f=",String(f),"  |PB3/K_pi^s|=",
            info.Kpi_s_quotient_size,"  |PB3/K_pi|=",info.Kpi_quotient_size,
            "  settled(K_pi^s=K_pi)=",info.settled,
            "  index-of-difference=",info.kernel_ratio_K,"\n");
    else
      Print("  m=",m," f=",String(f),"  NOT well-defined on QP -- ",
            info.note,"\n");
    fi;
  fi;
od;
if Length(hexGateFails) > 0 then
  Error("HEXAGON GATE FAIL: ", Length(hexGateFails), " of the 20 lifts did ",
        "not pass hexagon for their chosen witness q -- this should not ",
        "happen given all6_pass=1 rows in v3, so halting for review rather ",
        "than silently applying c->c^{2m+1} outside its license. Failing ",
        "pairs: ", hexGateFails);
fi;
Print("\nHEXAGON GATE PASS: all 20/20 lifts' witnesses passed hexagon (c1=c2=true) -- T_{m,f}(c)=c^{2m+1} is licensed for every one, so the settled measurement above covers the full 20/20.\n");

## settled_summary rollup (v3.1 new -- auditable count without hand-recount)
settled_total := Length(srcRows);;
settled_wd_true := Number(srcRows, r -> r.info.well_defined_on_QP);;
settled_wd_false := Number(srcRows, r -> not r.info.well_defined_on_QP);;
settled_true_count := Number(srcRows, r -> r.info.well_defined_on_QP and r.info.settled);;
settled_false_count := Number(srcRows, r -> r.info.well_defined_on_QP and not r.info.settled);;
Print("\n== settled_summary ==  total(rows measured)=",settled_total,
      "  well_defined_on_QP=",settled_wd_true,
      "  NOT well_defined_on_QP=",settled_wd_false,
      "  settled(K_pi^s=K_pi)=",settled_true_count,
      "  NOT settled=",settled_false_count,"\n");

## ============================================================
## (4) 3-element + regression f-orientation / reduction unit test
##     (identical logic to v3, inherited)
## ============================================================
Print("\n== (4) 3-element + regression unit test (inherited from v3) ==\n");

UnitTestRow := function(label, m, f)
  local fibIdx, fib, tab, witIdx, q, w, red_img, rec1;
  fibIdx := Filtered([1..Length(qpElts)], idx -> coarseLabelOf[idx] = f);
  fib := List(fibIdx, idx -> qpElts[idx]);
  tab := List(fib, qq -> Chk6(m,qq));
  witIdx := First([1..Length(fib)], i -> tab[i][6]);
  rec1 := rec(label := label, m := m, f_perm := String(f),
              coarse_in_GT_NA := Hex(m,f) and Group(xb,yb^f)=PN,
              c1_pass := Number(tab,r->r[1]),
              c2_pass := Number(tab,r->r[2]),
              c3_pass := Number(tab,r->r[3]),
              c4_pass := Number(tab,r->r[4]),
              c5_pass := Number(tab,r->r[5]),
              all6_pass := Number(tab,r->r[6]));
  if witIdx <> fail then
    q := fib[witIdx];
    w := WordOf(q);
    red_img := Image(redMap, q);
    rec1.lift_exists := true;
    rec1.witness_h_word := String(w);
    rec1.five_coface_images := List([1..5], i -> String(PsiAt(w,i)));
    rec1.reduction_image_in_PN := String(red_img);
    rec1.reduction_image_equals_f := (red_img = f);
  else
    rec1.lift_exists := false;
    rec1.witness_h_word := "null";
    rec1.five_coface_images := "null";
    rec1.reduction_image_in_PN := "null";
    rec1.reduction_image_equals_f := "null";
  fi;
  return rec1;
end;;

u1 := UnitTestRow("identity", 0, One(PN));;
cycM := First(Filtered(charm, mm -> mm <> 0),
              mm -> OrderMod(2*mm+1, Nord) = Phi(Nord));;
if cycM = fail then cycM := charm[2]; fi;;
u2 := UnitTestRow("cyclotomic_generator_candidate", cycM, One(PN));;
kumZ := First(shad, zz -> zz[1] = 0 and zz[2] <> One(PN));;
if kumZ <> fail then kumF := kumZ[2]; else kumF := fail; fi;;
if kumF <> fail then
  u3 := UnitTestRow("C5_kummer_translation_candidate", 0, kumF);
else
  u3 := rec(label := "C5_kummer_translation_candidate",
            note := "no m=0, f<>1 coarse shadow found in shad");
fi;;
u4 := UnitTestRow("regression_nonselfinverse_roundtrip_element4", r4_m,
                   r4_f_forward);;

Print("  u1(identity): lift=",u1.lift_exists,"\n");
Print("  u2(cyclotomic m=",cycM,"): lift=",u2.lift_exists,"\n");
if kumF <> fail then
  Print("  u3(kummer f=",String(kumF),"): lift=",u3.lift_exists,"\n");
else
  Print("  u3: no candidate found\n");
fi;
Print("  u4(regression f=",String(r4_f_forward),"): lift=",u4.lift_exists,"\n");

## ============================================================
## cert write-out (machine-generated, JSON)
## ============================================================
JStr := function(s) return Concatenation("\"", s, "\""); end;;
JBool := function(b)
  if b = true then return "true";
  elif b = false then return "false";
  else return "null"; fi;
end;;
JNum := function(x) return String(x); end;;
JoinC := function(l)
  local s, i;
  s := "";
  for i in [1..Length(l)] do
    s := Concatenation(s, l[i]);
    if i < Length(l) then s := Concatenation(s, ","); fi;
  od;
  return s;
end;;
JList := function(l) return Concatenation("[", JoinC(List(l,JStr)), "]"); end;;
JIntList := function(l) return Concatenation("[", JoinC(List(l,JNum)), "]"); end;;

WriteRow := function(outS, r)
  AppendTo(outS, "{\"shadow_id\":",JNum(r.shadow_id),
    ",\"m\":",JNum(r.m),
    ",\"f_perm\":",JStr(r.f_perm),
    ",\"fiber_size\":",JNum(r.fiber_size),
    ",\"c1_pass\":",JNum(r.c1_pass),
    ",\"c2_pass\":",JNum(r.c2_pass),
    ",\"c3_pass\":",JNum(r.c3_pass),
    ",\"c4_pass\":",JNum(r.c4_pass),
    ",\"c5_pass\":",JNum(r.c5_pass),
    ",\"all6_pass\":",JNum(r.all6_pass),
    ",\"lift_exists\":",JBool(r.lift_exists));
  if r.lift_exists then
    AppendTo(outS, ",\"witness_h_word\":",JStr(r.witness_h_word),
      ",\"five_coface_images\":",JList(r.five_coface_images),
      ",\"hexagon_pass_for_witness\":",JBool(r.hexagon_pass_for_witness),
      ",\"dies_at\":[]");
  else
    AppendTo(outS, ",\"witness_h_word\":null,\"five_coface_images\":null",
      ",\"hexagon_pass_for_witness\":null",
      ",\"dies_at\":",JList(r.dies_at));
  fi;
  AppendTo(outS, "}");
end;;

WriteUnitRow := function(outS, r)
  if IsBound(r.note) then
    AppendTo(outS, "{\"label\":",JStr(r.label),",\"found\":false,\"note\":",
      JStr(r.note),"}");
    return;
  fi;
  AppendTo(outS, "{\"label\":",JStr(r.label),
    ",\"found\":true,\"m\":",JNum(r.m),
    ",\"f_perm\":",JStr(r.f_perm),
    ",\"coarse_in_GT_NA\":",JBool(r.coarse_in_GT_NA),
    ",\"c1_pass\":",JNum(r.c1_pass),",\"c2_pass\":",JNum(r.c2_pass),
    ",\"c3_pass\":",JNum(r.c3_pass),",\"c4_pass\":",JNum(r.c4_pass),
    ",\"c5_pass\":",JNum(r.c5_pass),",\"all6_pass\":",JNum(r.all6_pass),
    ",\"lift_exists\":",JBool(r.lift_exists));
  if r.lift_exists = true then
    AppendTo(outS, ",\"witness_h_word\":",JStr(r.witness_h_word),
      ",\"five_coface_images\":",JList(r.five_coface_images),
      ",\"reduction_image_in_PN\":",JStr(r.reduction_image_in_PN),
      ",\"reduction_image_equals_f\":",JBool(r.reduction_image_equals_f));
  else
    AppendTo(outS, ",\"witness_h_word\":null,\"five_coface_images\":null",
      ",\"reduction_image_in_PN\":null,\"reduction_image_equals_f\":null");
  fi;
  AppendTo(outS, "}");
end;;

WriteSettledRow := function(outS, sr)
  local info;
  info := sr.info;
  AppendTo(outS, "{\"m\":",JNum(sr.m),",\"f_perm\":",JStr(sr.f_perm),
    ",\"hexagon_gate_pass\":true",
    ",\"well_defined_on_QP\":",JBool(info.well_defined_on_QP));
  if info.well_defined_on_QP then
    AppendTo(outS, ",\"Kpi_s_quotient_size\":",JNum(info.Kpi_s_quotient_size),
      ",\"Kpi_quotient_size\":",JNum(info.Kpi_quotient_size),
      ",\"settled\":",JBool(info.settled),
      ",\"index_of_difference\":",JNum(info.kernel_ratio_K));
  else
    AppendTo(outS, ",\"note\":",JStr(info.note));
  fi;
  AppendTo(outS, "}");
end;;

sJ := "";; outJ := OutputTextString(sJ,true);;
SetPrintFormattingStatus(outJ, false);;
AppendTo(outJ,"{\"schema\":\"wac_v1-pent-t2t3-cert/v3.1\",");
AppendTo(outJ,"\"generated_by\":\"search/probe/wac_v1/pent_t2t3_v31_20260731.g\",");
AppendTo(outJ,"\"extends\":\"search/probe/wac_v1/pent_t2t3_v3_20260731.g (repaired coarse<->fine label convention, imported byte-identical: window/cof/D5/Psi/PsiAt/coarse_of/Chk6/Hex/Pent/regression-element-4 unchanged). v3 left in place unmodified.\",");
AppendTo(outJ,"\"note\":\"Commander instruction (裁定280 残工程): extend the settled measurement (source kernel) to all 20 lift rows, with two hard machine-checked gates added in this v3.1 (not present as asserts in v3): (i) precondition that all 20/20 coarse shadows lifted (matches v3's lifted_total=20; Error()s if not); (ii) hexagon gate per lift -- T_{m,f}(c)=c^{2m+1} is a PROPOSITION proved from the hexagon relations (C1 arXiv 2008.00066 Cor 2.8 (2.29)), licensed only for (m,f) whose witness passed hexagon (c1=c2=true); checked per-lift via a fresh Chk6(m,q) call, Error()s on any failure rather than silently applying the twist rule outside its license. Both gates are expected-vacuous (all 20 rows in v3 have all6_pass=1, i.e. hexagon already passed) but are CHECKED here, not assumed. LEVEL CAVEAT (verbatim from docs/notes/pent_conflict_diagnosis_v1.md sec.1.4, survived unretracted per pent_conflict_diagnosis_v2.md sec.4): C1 Prop 2.11 defines the source kernel N_s := ker(T^{PB_4}_{m,f}) at PB_4 level; this script's settled measurement is |PB_3/K_pi^s| vs |PB_3/(K_pi)_{PB_3}|, a PB_3-level statement. (N_s)_PB3=(N)_PB3 does NOT imply N_s=N -- what this file establishes is settled-at-PB_3-level, a NECESSARY CONDITION for the PB_4-level claim, NOT the PB_4-level claim itself (unresolved, diagnosis sec.7 priority 4). No exponent/index match is used as a settled PROOF anywhere below -- settled always means the literal Kernel(hom) computation with Size(K)=1. Contact-blocked: no expected settled-count value is asserted in any predicate (only the two gates above, which are construction-level invariants of the v3 repair result, are hard-asserted). Raw measurement, single GAP lane. NOT a ledger claim.\",");
AppendTo(outJ,"\"f_orientation\":\"psi_reversed_for_defect_eval__forward_coarse_of_WordOf_for_coarse_fiber_label\",");
AppendTo(outJ,"\"P_size\":",JNum(Size(PN)),",");
AppendTo(outJ,"\"N_ord\":",JNum(Nord),",");
AppendTo(outJ,"\"GT_size\":",JNum(Length(shad)),",");
AppendTo(outJ,"\"GT_distinct_f\":",JNum(Length(Set(List(shad,z->z[2])))),",");
AppendTo(outJ,"\"PB3_refined_size\":",JNum(Size(QP)),",");
AppendTo(outJ,"\"F2_refined_size\":",JNum(Size(QF)),",");
AppendTo(outJ,"\"psi_c_trivial\":",JBool(Psi(gc)=one5),",");
AppendTo(outJ,"\"psi_c_order\":",JNum(Order(Psi(gc))),",");
AppendTo(outJ,"\"H3_PB3_size\":",JNum(Size(H3)),",");
AppendTo(outJ,"\"H3_PB3_structure\":",JStr(StructureDescription(H3)),",");
AppendTo(outJ,"\"fiber_size\":",JNum(Size(QP)/Size(PN)),",");
AppendTo(outJ,"\"lifted_total\":",JNum(Length(lift)),",");
AppendTo(outJ,"\"coarse_target_lift_set_size\":",JNum(Length(lift)),",");
AppendTo(outJ,"\"lifted_distinct_f\":",JNum(Length(Set(List(lift,z->z[2])))),",");
AppendTo(outJ,"\"all_20_lifted_precondition_pass\":",JBool(Length(lift)=20),",");
AppendTo(outJ,"\"hexagon_gate_fail_count\":",JNum(Length(hexGateFails)),",");
AppendTo(outJ,"\"shadows\":[");
for i in [1..Length(rows)] do
  WriteRow(outJ, rows[i]);
  if i < Length(rows) then AppendTo(outJ, ","); fi;
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"settled_per_lift\":[");
for i in [1..Length(srcRows)] do
  WriteSettledRow(outJ, srcRows[i]);
  if i < Length(srcRows) then AppendTo(outJ, ","); fi;
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"settled_summary\":{");
AppendTo(outJ,"\"total_rows_measured\":",JNum(settled_total),",");
AppendTo(outJ,"\"well_defined_on_QP_count\":",JNum(settled_wd_true),",");
AppendTo(outJ,"\"not_well_defined_on_QP_count\":",JNum(settled_wd_false),",");
AppendTo(outJ,"\"settled_true_count\":",JNum(settled_true_count),",");
AppendTo(outJ,"\"settled_false_count\":",JNum(settled_false_count),",");
AppendTo(outJ,"\"level_caveat\":\"PB_3-level necessary condition only, per pent_conflict_diagnosis_v1.md sec.1.4 -- NOT a PB_4-level (C1 Prop 2.11) settled claim\"");
AppendTo(outJ,"},");
AppendTo(outJ,"\"unit_test_4element\":[");
WriteUnitRow(outJ, u1); AppendTo(outJ,",");
WriteUnitRow(outJ, u2); AppendTo(outJ,",");
WriteUnitRow(outJ, u3); AppendTo(outJ,",");
WriteUnitRow(outJ, u4);
AppendTo(outJ,"],");
AppendTo(outJ,"\"regression_test_element4_roundtrip\":{");
AppendTo(outJ,"\"description\":\"mandatory hard-assert regression test (diagnosis sec.5), inherited and re-run from v3 (not just carried over as a value): non-self-inverse coarse f round-tripped coarse->fine(Psi)->coarse(coarse_of o WordOf); script Error()s (aborts before cert write) if this fails.\",");
AppendTo(outJ,"\"bits\":",JIntList(r4_bits),",");
AppendTo(outJ,"\"m\":",JNum(r4_m),",");
AppendTo(outJ,"\"f_forward_coarse\":",JStr(String(r4_f_forward)),",");
AppendTo(outJ,"\"f_forward_self_inverse\":",JBool(r4_self_inverse),",");
AppendTo(outJ,"\"f_roundtrip_via_coarse_of_WordOf\":",JStr(String(r4_f_roundtrip)),",");
AppendTo(outJ,"\"roundtrip_pass\":",JBool(r4_roundtrip_pass),",");
AppendTo(outJ,"\"legacy_pr1_image_informative_only\":",JStr(String(r4_f_legacy_pr1)),",");
AppendTo(outJ,"\"legacy_redMap_image_informative_only\":",JStr(String(r4_f_legacy_redMap)));
AppendTo(outJ,"},");
AppendTo(outJ,"\"base_probe_v3_sha256\":\"e6e1f67dd903a25dfc9a86fdb8b1419f37e54f39e7ddb7115e0e3b4546afcddf\",");
AppendTo(outJ,"\"base_probe_v2_sha256\":\"ff9e6f8b4801b861cfc1fabdf005a7e7de74b19d1eeb41516df0d76f9e98df19\",");
AppendTo(outJ,"\"source_digest_sha256\":\"PENDING_POSTPROCESS\",");
AppendTo(outJ,"\"base_probe_digest_sha256\":\"PENDING_POSTPROCESS\"");
AppendTo(outJ,"}");
CloseStream(outJ);;
outF := OutputTextFile("search/certs/pent_t2t3_v31_20260731.json", false);;
SetPrintFormattingStatus(outF, false);;
PrintTo(outF, sJ);;
CloseStream(outF);;
Print("\nCERT_WRITTEN\n");
Print("\nDRIVER_DONE\n");
QUIT;
