#############################################################################
## search/probe/wac_v1/pent_t2t3_v2_20260731.g
##  P91-2 (1)(2)(4) -- built on top of pent_t2t3_run2.g (same window,
##  same coface machinery, NOT imported -- re-derived here so this stays a
##  single self-contained probe file per the "no shared helper" discipline).
##
##  (1) source kernel K_pi^s per fine lift, compared to K_pi = (K_pi)_{PB3}.
##      Definition used (CITED, not invented): docs/week1-定義ノート.md
##      section 2, Prop 3.2 / (3.53) / settled+isolated (Thm 3.10):
##        T_{m,f} on PB3 generators:  x |-> x^{2m+1},  y |-> f^-1 y^{2m+1} f,
##        c |-> c^{2m+1}   (week1 line 166: "c -> c^{2m+1}N"; line 171: E_{m,f}).
##        K_pi^s(m,f) := ker( Psi o T_{m,f} ).  "settled" iff K_pi^s = K_pi.
##      litgate_pentagon_v1.md (the pentagon/B4 memo) does NOT itself give a
##      formula for this -- it was checked and contains no "source kernel"
##      definition or equation number. The construction below is imported
##      from the B3-gentle definition note instead (week1, cited above),
##      which is the same PB3-hexagon apparatus this checker already uses.
##      This substitution is flagged explicitly in the cert note and in the
##      implementer report; it is NOT confirmed against C1's own Def 2.x for
##      the B4/pentagon system (no such formula was found in-repo).
##  (2) witness-row cert v2 for all 20 coarse shadows (id,m,f,witness h,
##      c1-c6, five-coface images, digests). im_red_order renamed to
##      coarse_target_lift_set_size per F91-2.5.
##  (4) 3-element f-orientation/reduction unit test: identity, a cyclotomic
##      generator (m with 2m+1 generating (Z/N_ord)^x, f=1), a C5 Kummer
##      translation generator (m=0, f<>1 among the coarse shadows). No
##      expected value is asserted anywhere below -- behaviour is recorded.
##
##  Contact-blocked. Single GAP lane. NOT a ledger claim.
#############################################################################

## ---- window (identical construction to pent_t2t3_run2.g) ----
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

## ---- sigma-conjugation (identical to run2.g) ----
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

## ============================================================
## (2) per-shadow witness cert: iterate ALL 20 coarse shadows
## ============================================================
Print("\n== (2) witness rows for all coarse shadows ==\n");
gensQP := [Psi(gx),Psi(gy),Psi(gc)];;
rows := [];;
lift := [];;   ## [m, f, q] triples that pass Chk6 fully
sid := 0;;
for z in shad do
  m := z[1];; f := z[2];;
  fib := Filtered(Elements(QP), q -> Image(pr1,q) = z[2]);
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
    Add(lift, [m,f,q]);
  else
    row.lift_exists := false;
    row.witness_h_word := "null";
    row.five_coface_images := "null";
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
## (1) source kernel per lift
## ============================================================
Print("\n== (1) source kernel per lift ==\n");
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
for tr in lift do
  m := tr[1];; f := tr[2];; q := tr[3];;
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
od;

## ============================================================
## (4) 3-element f-orientation / reduction unit test
##     no expected value asserted -- behaviour only.
## ============================================================
Print("\n== (4) 3-element unit test ==\n");
redMap := GroupHomomorphismByImages(QP, PN, gensQP, [xb,yb,()]);;

UnitTestRow := function(label, m, f)
  local fib, tab, witIdx, q, w, red_img, rec1;
  fib := Filtered(Elements(QP), qq -> Image(pr1,qq) = f);
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

## element 1: identity  (m=0, f=identity of PN)
u1 := UnitTestRow("identity", 0, One(PN));;
## element 2: a cyclotomic generator -- pick smallest charming m<>0 with
## 2m+1 generating (Z/Nord)^x, f = identity. Selector is structural
## (order of 2m+1 in (Z/Nord)^x), not an asserted pass/fail expectation.
cycM := First(Filtered(charm, mm -> mm <> 0),
              mm -> OrderMod(2*mm+1, Nord) = Phi(Nord));;
if cycM = fail then cycM := charm[2]; fi;;   ## fallback: report whatever exists
u2 := UnitTestRow("cyclotomic_generator_candidate", cycM, One(PN));;
## element 3: a C5 Kummer translation generator -- m=0, f<>1 among the
## coarse shadows (structural selector: m=0 means chi_vir trivial, i.e.
## pure "translation" direction; deterministic pick = first such f in
## Elements(PN) order that is itself in shad).
kumZ := First(shad, zz -> zz[1] = 0 and zz[2] <> One(PN));;
if kumZ <> fail then kumF := kumZ[2]; else kumF := fail; fi;;
if kumF <> fail then
  u3 := UnitTestRow("C5_kummer_translation_candidate", 0, kumF);
else
  u3 := rec(label := "C5_kummer_translation_candidate",
            note := "no m=0, f<>1 coarse shadow found in shad");
fi;;

Print("  u1(identity): lift=",u1.lift_exists,"\n");
Print("  u2(cyclotomic m=",cycM,"): lift=",u2.lift_exists,"\n");
if kumF <> fail then
  Print("  u3(kummer f=",String(kumF),"): lift=",u3.lift_exists,"\n");
else
  Print("  u3: no candidate found\n");
fi;

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
      ",\"dies_at\":[]");
  else
    AppendTo(outS, ",\"witness_h_word\":null,\"five_coface_images\":null",
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

WriteSrcRow := function(outS, sr)
  local info;
  info := sr.info;
  AppendTo(outS, "{\"m\":",JNum(sr.m),",\"f_perm\":",JStr(sr.f_perm),
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
AppendTo(outJ,"{\"schema\":\"wac_v1-pent-t2t3-cert/v2\",");
AppendTo(outJ,"\"generated_by\":\"search/probe/wac_v1/pent_t2t3_v2_20260731.g\",");
AppendTo(outJ,"\"note\":\"P91-2 (1)(2)(4). source kernel definition imported from docs/week1-定義ノート.md Prop 3.2/(3.53)/settled+isolated (Thm 3.10), NOT from litgate_pentagon_v1.md (which contains no source-kernel formula for the B4/pentagon system) -- flagged, not confirmed against C1 Def 2.x. Unit-test element selection (cyclotomic/kummer) is a structural, non-asserting selector (order of 2m+1 mod N_ord; m=0 translation direction), not a claimed identification with any named group-theoretic object. Contact-blocked: no expected pass/fail value used in any predicate. Raw measurement, single GAP lane. NOT a ledger claim.\",");
AppendTo(outJ,"\"f_orientation\":\"paper_order_words_reversed_at_evaluation\",");
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
AppendTo(outJ,"\"shadows\":[");
for i in [1..Length(rows)] do
  WriteRow(outJ, rows[i]);
  if i < Length(rows) then AppendTo(outJ, ","); fi;
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"source_kernel_per_lift\":[");
for i in [1..Length(srcRows)] do
  WriteSrcRow(outJ, srcRows[i]);
  if i < Length(srcRows) then AppendTo(outJ, ","); fi;
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"unit_test_3element\":[");
WriteUnitRow(outJ, u1); AppendTo(outJ,",");
WriteUnitRow(outJ, u2); AppendTo(outJ,",");
WriteUnitRow(outJ, u3);
AppendTo(outJ,"],");
AppendTo(outJ,"\"source_digest_sha256\":\"PENDING_POSTPROCESS\",");
AppendTo(outJ,"\"base_probe_digest_sha256\":\"PENDING_POSTPROCESS\"");
AppendTo(outJ,"}");
CloseStream(outJ);;
outF := OutputTextFile("search/certs/pent_t2t3_v2_20260731.json", false);;
SetPrintFormattingStatus(outF, false);;
PrintTo(outF, sJ);;
CloseStream(outF);;
Print("\nCERT_WRITTEN\n");
Print("\nDRIVER_DONE\n");
QUIT;
