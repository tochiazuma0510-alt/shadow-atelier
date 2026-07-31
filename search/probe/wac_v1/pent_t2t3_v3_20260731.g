#############################################################################
## search/probe/wac_v1/pent_t2t3_v3_20260731.g
##  P91-2 (1)(2)(4) -- v3 REPAIR of pent_t2t3_v2_20260731.g, per the fix
##  specified in docs/notes/pent_conflict_diagnosis_v2.md sec.4 (mathematician
##  diagnosis, 2026-07-31): the coarse<->fine dictionary in v2 used
##  Image(pr1,q) (= reversed evaluation, since Psi/PsiAt apply Rev before
##  mapping forward) to label the fiber of a fine element q by a coarse
##  shadow f, while the coarse enumeration Hex(m,f) is forward (GAP order).
##  This attached each fine element to the coarse label of its OWN INVERSE,
##  so probe only ever found lifts for self-inverse f (4/20 survivors,
##  exactly the self-inverse f's -- diagnosis sec 1.3).
##
##  FIRST-ATTEMPT PLAN, LATER FOUND WRONG (kept here verbatim as a record of
##  the error -- superseded below; see the comment block above coarse_of's
##  definition [~line 105] and the cert "repairs" field for the correction
##  actually applied). The reasoning below was the initial "minimal repair"
##  plan: keep Psi/PsiAt exactly as in v2 (Rev before forward map) -- this
##  half of the machinery is independently validated correct in the
##  diagnosis (our D1/D2/Pent/c1-c5 evaluator accepts the author's 20
##  witnesses 20/20 when fed their words as-is). Only the coarse-labelling
##  of a fine element q in QP was to be changed: instead of Image(pr1,q),
##  use the group homomorphism redMap: QP -> PN, gensQP |-> [xb,yb,()]
##  (forward, same convention as Hex). This was REASONED (incorrectly) to be
##  algebraically IDENTICAL to the diagnosis's suggested fix
##    coarse_of(w) := MappedWord(w,[gx,gy,gc],[xb,yb,()])   (no Rev)
##  applied to a preimage word of q -- the claimed argument was: since
##  epiP(w)=Psi(w) by construction of epiP, and gensQP=[Psi(gx),Psi(gy),
##  Psi(gc)] maps to [xb,yb,()] under redMap by definition, redMap(Psi(w))
##  = coarse_of(w) for EVERY w. THIS ARGUMENT IS WRONG: Psi is an
##  ANTI-homomorphism, not a homomorphism, so an epiP-preimage w0 of q
##  satisfies epiP(w0) = Psi(Rev(w0)), not Psi(w0); consequently
##  Image(redMap,q) = coarse_of(Rev(WordOf(q))), which is algebraically
##  IDENTICAL to the OLD (v2, pr1-based) reversed-fiber bug, not a fix of
##  it. The in-file regression test (element 4, below) caught this on the
##  first run of this file (redMap output equalled the legacy pr1 output)
##  and the script halted before writing a cert. redMap is therefore NOT
##  used for fiber selection anywhere in the code below -- fiber selection
##  uses coarse_of(WordOf(q)) directly (see coarseLabelOf, ~line 245),
##  applied to the word WordOf(q) itself, not via any QP->PN homomorphism
##  shortcut. redMap is retained only for its original v2 purpose
##  (reduction_image_in_PN in the unit-test rows), which is unaffected.
##
##  No formula in Chk6 (P0,R0,D1,D2,Pent,c1-c5) is touched. The fix actually
##  applied is "option 1" of the diagnosis's two offered fixes (relabel the
##  fiber, don't touch Psi's Rev convention) -- NOT mixed with "option 2"
##  (removing Rev from Psi and rewriting D1/D2/Pent in GAP order).
##
##  Regression unit test element 4 (mandatory per diagnosis sec.5): a
##  self-inverse-free coarse f (the diagnosis's own Kummer witness,
##  m=0, author word bits [1,0,0,1,0,0,0,1,1,1] = y x^2 y x^3 y^3, forward
##  coarse label a 3-cycle) is round-tripped coarse->fine(Psi)->coarse
##  (via coarse_of o WordOf, THE FIX actually used -- NOT redMap, see above)
##  and asserted (GAP Error() on failure -- hard regression gate) to return
##  to the same label. Under the OLD (v2, pr1-based) method, and under the
##  dead-end redMap-based first attempt above, this element would have
##  surfaced f^{-1} != f, i.e. this is exactly the bug detector the
##  diagnosis calls for.
##
##  Additional cross-check (diagnosis committee item 4 / instruction 5):
##  the 20 author charming witnesses (search/certs/pent_thirdparty_gt_20260731.json,
##  coarse_reduction.charming.per_entry_rows, transcribed literally below,
##  sha256 of source file recorded) are fed directly into Psi + Chk6 and the
##  acceptance count is machine-recorded (no expected value asserted).
##
##  Contact-blocked: no expected pass/fail/count value is used in any
##  predicate in the main witness/shad loop or the author-witness crosscheck
##  loop (only the sec.4 round-trip identity, which is a construction-level
##  invariant, not a research-value prediction, is asserted).
##  Single GAP lane. NOT a ledger claim -- report to commander for review.
#############################################################################

## ---- provenance helper: SHA-256 of a repo-relative file, machine-computed
## via external sha256sum (same pattern as wall36_cert.g/wall37_cert.g) --
## used below to fill source_digest_sha256 (this script) and
## base_probe_digest_sha256 (the base probe this file repairs/extends).
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_pent_v3_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

## ---- window (identical construction to pent_t2t3_v2_20260731.g) ----
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

## ---- (v3 FIX) forward coarse-label machinery -----------------------------
## coarse_of(w) is the diagnosis's specified forward map (no Rev).
## IMPORTANT (caught by the in-file regression test below, first attempt):
## Psi is an ANTI-homomorphism, not a homomorphism -- PsiAt(w1*w2,i) =
## MappedWord(Rev(w1*w2),...) = MappedWord(Rev(w2)*Rev(w1),...) =
## PsiAt(w2,i)*PsiAt(w1,i), so Psi(w1*w2) = Psi(w2)*Psi(w1). Consequently
## the naive-looking shortcut "redMap := GroupHomomorphismByImages(QP,PN,
## [Psi(gx),Psi(gy),Psi(gc)],[xb,yb,()]); Image(redMap,q)" does NOT compute
## coarse_of(WordOf(q)): redMap is built as an honest (forward) homomorphism
## on the SAME generator images that epiP (also forward) uses, so
## Image(redMap,epiP(w0)) = coarse_of(w0) for an epiP-preimage w0 -- but
## epiP(w0) = Psi(Rev(w0)) (shown by the same anti-homomorphism identity),
## i.e. w0 = Rev(WordOf(q)), so Image(redMap,q) = coarse_of(Rev(WordOf(q))),
## which is exactly the OLD (v2, pr1-based) reversed-fiber bug again
## (confirmed empirically: first run of this file had
## Image(redMap,q) = Image(pr1,q) identically, and the regression assert
## below correctly caught it and halted the script before any cert was
## written). The FIX actually used below is the diagnosis's literal
## prescription: apply coarse_of forward, with NO Rev, directly to the word
## WordOf(q) itself (not to any epiP-preimage, and not via a QP->PN group
## homomorphism trick -- Psi's anti-homomorphism nature makes such a
## shortcut unsound). redMap is kept only for its ORIGINAL v2 purpose
## (reduction_image_in_PN in the unit-test rows), which is unaffected.
gensQP := [Psi(gx),Psi(gy),Psi(gc)];;
redMap := GroupHomomorphismByImages(QP, PN, gensQP, [xb,yb,()]);;
Print(" redMap : QP -> PN well-defined? ", redMap<>fail, "\n");
coarse_of := function(w) return MappedWord(w, [gx,gy,gc], [xb,yb,()]); end;;

## ---- sigma-conjugation (identical to v2) ----
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
## (v3 FIX) regression unit test element 4 -- MANDATORY, hard assert.
## Round-trips a non-self-inverse coarse f (the diagnosis's own Kummer
## witness) coarse -> fine (Psi) -> coarse (coarse_of o WordOf, the actual
## fix) and Error()s the whole script if the label does not come back
## unchanged. This is exactly the bug pattern the diagnosis found: under the
## old Image(pr1,q) method (and, as this run discovered, under a naive
## Image(redMap,q) shortcut too -- see comment above coarse_of's definition)
## this element's label comes back as f^-1 <> f.
## ============================================================
Print("\n== regression unit test element 4 (non-self-inverse f round trip) ==\n");
WordFromBits := function(bits)
  local w, b;
  w := One(Fw);
  for b in bits do
    if b = 0 then w := w * gx; else w := w * gy; fi;
  od;
  return w;
end;;
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
r4_f_legacy_pr1 := Image(pr1, r4_q);;         ## informative only, not asserted on
r4_f_legacy_redMap := Image(redMap, r4_q);;   ## informative only -- first-attempt
  ## "fix" (Image(redMap,q)) turned out to be algebraically identical to the
  ## OLD pr1 bug (Psi is an anti-homomorphism -- see comment above coarse_of);
  ## kept here only as a recorded trace of that dead end, not used as a label.
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

## ============================================================
## (v3 FIX, actual) precompute the forward coarse label coarse_of(WordOf(q))
## once for every element of QP, reused by the main loop and UnitTestRow
## below (avoids recomputing PreImagesRepresentative 20x per element).
## ============================================================
Print("\n== precomputing forward coarse labels coarse_of(WordOf(q)) for all |QP|=",
      Size(QP)," elements ==\n");
qpElts := Elements(QP);;
coarseLabelOf := List(qpElts, q -> coarse_of(WordOf(q)));;
Print("  done.\n");

## ============================================================
## (2) per-shadow witness cert: iterate ALL 20 coarse shadows
##     (v3 FIX applied here: fib now selects by coarse_of(WordOf(q)) = z[2],
##      not Image(pr1,q) = z[2] as in v2)
## ============================================================
Print("\n== (2) witness rows for all coarse shadows (v3, coarse_of o WordOf fiber) ==\n");
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
## (4) 3-element f-orientation / reduction unit test (unchanged selection
##     logic from v2; fib now uses redMap per the v3 fix)
##     no expected value asserted -- behaviour only.
## ============================================================
Print("\n== (4) 3-element unit test ==\n");

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
## element 4 (v3 NEW, mandatory regression element): the non-self-inverse
## round-trip witness from the regression test above, re-expressed as a
## UnitTestRow for the cert (using its forward coarse label as f).
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
## (5) author 20-witness cross-check (instruction item 4 / diagnosis
##     committee item 1): the 20 charming witnesses from
##     search/certs/pent_thirdparty_gt_20260731.json,
##     coarse_reduction.charming.per_entry_rows, TRANSCRIBED LITERALLY
##     (source file sha256 recorded below), fed directly into
##     Psi + Chk6 of THIS repaired evaluator. Acceptance count is machine-
##     recorded; no expected value is asserted anywhere in this loop.
## ============================================================
Print("\n== (5) author 20-witness cross-check ==\n");
authorWitnessBits := [
  [ [], 0 ],
  [ [], 4 ],
  [ [0,1,0,0,0,0,1,1,1,1], 1 ],
  [ [0,1,0,0,0,0,1,1,1,1], 3 ],
  [ [0,0,1,1,0,0,0,1,1,1], 0 ],
  [ [0,0,1,1,0,0,0,1,1,1], 4 ],
  [ [0,0,0,1,1,1,0,0,1,1], 0 ],
  [ [0,0,0,1,1,1,0,0,1,1], 4 ],
  [ [0,0,0,0,1,1,1,1,0,1], 1 ],
  [ [0,0,0,0,1,1,1,1,0,1], 3 ],
  [ [1,0,0,1,0,0,0,1,1,1], 0 ],
  [ [1,0,0,1,0,0,0,1,1,1], 4 ],
  [ [1,1,0,0,1,1,0,0,0,1], 1 ],
  [ [1,1,0,0,1,1,0,0,0,1], 3 ],
  [ [1,1,0,0,1,1,1,0,0,0], 1 ],
  [ [1,1,0,0,1,1,1,0,0,0], 3 ],
  [ [1,1,1,0,0,1,1,1,1,0,0,0,1,1,1], 0 ],
  [ [1,1,1,0,0,1,1,1,1,0,0,0,1,1,1], 4 ],
  [ [0,1,0,0,0,1,1,1,0,1], 1 ],
  [ [0,1,0,0,0,1,1,1,0,1], 3 ]
];;
authorWitnessRows := [];;
awi := 0;;
for aw in authorWitnessBits do
  awi := awi + 1;
  aw_bits := aw[1];; aw_m := aw[2];;
  aw_w := WordFromBits(aw_bits);;
  aw_q := Psi(aw_w);;
  aw_res := Chk6(aw_m, aw_q);;
  aw_flabel := coarse_of(WordOf(aw_q));;
  Add(authorWitnessRows, rec(
    idx := awi, bits := aw_bits, m := aw_m,
    word_str := String(aw_w),
    forward_coarse_label := String(aw_flabel),
    c1 := aw_res[1], c2 := aw_res[2], c3 := aw_res[3],
    c4 := aw_res[4], c5 := aw_res[5], all6 := aw_res[6]));
  Print("  #",awi," m=",aw_m," bits=",aw_bits," c1..c5=",
        aw_res{[1..5]}," all6=",aw_res[6],"\n");
od;
authorWitnessAcceptedCount := Number(authorWitnessRows, r -> r.all6);;
Print("  AUTHOR WITNESS ACCEPTED = ",authorWitnessAcceptedCount,"/",
      Length(authorWitnessRows),"\n");

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
      ",\"legacy_redMap_image_equals_f\":",JBool(r.reduction_image_equals_f));
  else
    AppendTo(outS, ",\"witness_h_word\":null,\"five_coface_images\":null",
      ",\"reduction_image_in_PN\":null,\"legacy_redMap_image_equals_f\":null");
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

WriteAuthorRow := function(outS, r)
  AppendTo(outS, "{\"idx\":",JNum(r.idx),
    ",\"bits\":",JIntList(r.bits),
    ",\"m\":",JNum(r.m),
    ",\"word_str\":",JStr(r.word_str),
    ",\"forward_coarse_label\":",JStr(r.forward_coarse_label),
    ",\"c1\":",JBool(r.c1),",\"c2\":",JBool(r.c2),",\"c3\":",JBool(r.c3),
    ",\"c4\":",JBool(r.c4),",\"c5\":",JBool(r.c5),
    ",\"all6\":",JBool(r.all6),"}");
end;;

sJ := "";; outJ := OutputTextString(sJ,true);;
SetPrintFormattingStatus(outJ, false);;
AppendTo(outJ,"{\"schema\":\"wac_v1-pent-t2t3-cert/v3\",");
AppendTo(outJ,"\"generated_by\":\"search/probe/wac_v1/pent_t2t3_v3_20260731.g\",");
AppendTo(outJ,"\"repairs\":\"docs/notes/pent_conflict_diagnosis_v2.md sec.4/5: coarse fiber label for a fine element q in QP changed from Image(pr1,q) (reversed evaluation, matched f^-1 not f) to coarse_of(WordOf(q)) with coarse_of(w):=MappedWord(w,[gx,gy,gc],[xb,yb,()]) (forward, no Rev, same convention as Hex/coarse enumeration), applied directly to the word WordOf(q) that Chk6 itself already uses. NOTE (in-file dead end, kept for the record): a first attempt used the group homomorphism redMap:QP->PN (gensQP|->[xb,yb,()]) and Image(redMap,q), reasoning it should equal coarse_of(w) for any epiP-preimage w of q -- this is WRONG because Psi is an ANTI-homomorphism (Psi(w1*w2)=Psi(w2)*Psi(w1)), so an epiP-preimage w0 satisfies epiP(w0)=Psi(Rev(w0)), making Image(redMap,q)=coarse_of(Rev(WordOf(q))) -- algebraically identical to the OLD pr1 bug. The in-file regression test (element 4, mandatory hard assert) caught this on the first run (redMap output equalled the legacy pr1 output) and the script halted before writing a cert; this v3 run applies the corrected coarse_of(WordOf(q)) fiber label throughout. Psi/PsiAt/Chk6/D1/D2/Pent are UNCHANGED from v2 (that half of the machinery was independently validated correct in the diagnosis). base_probe = pent_t2t3_v2_20260731.g (kept as the record of the error).\",");
AppendTo(outJ,"\"note\":\"P91-2 (1)(2)(4), v3 repair. source kernel definition imported from docs/week1-定義ノート.md Prop 3.2/(3.53)/settled+isolated (Thm 3.10), NOT from litgate_pentagon_v1.md (which contains no source-kernel formula for the B4/pentagon system) -- flagged, not confirmed against C1 Def 2.x. Unit-test element selection (cyclotomic/kummer/regression) is a structural, non-asserting selector, not a claimed identification with any named group-theoretic object, EXCEPT the sec.5-in-file regression round-trip test which is a hard construction-level assert (GAP Error() on failure), not a research-value prediction. Contact-blocked: no expected pass/fail/count value for shad/lift/author-crosscheck is used in any predicate. Raw measurement, single GAP lane. NOT a ledger claim.\",");
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
AppendTo(outJ,"\"unit_test_4element\":[");
WriteUnitRow(outJ, u1); AppendTo(outJ,",");
WriteUnitRow(outJ, u2); AppendTo(outJ,",");
WriteUnitRow(outJ, u3); AppendTo(outJ,",");
WriteUnitRow(outJ, u4);
AppendTo(outJ,"],");
AppendTo(outJ,"\"regression_test_element4_roundtrip\":{");
AppendTo(outJ,"\"description\":\"mandatory hard-assert regression test (diagnosis sec.5): non-self-inverse coarse f round-tripped coarse->fine(Psi)->coarse(coarse_of o WordOf, THE FIX); script Error()s (aborts before cert write) if this fails. This test failed on the first run of this file (with the dead-end redMap-based fix) and caught it -- see legacy_redMap_image_informative_only below, which equals legacy_pr1_image_informative_only.\",");
AppendTo(outJ,"\"bits\":",JIntList(r4_bits),",");
AppendTo(outJ,"\"m\":",JNum(r4_m),",");
AppendTo(outJ,"\"f_forward_coarse\":",JStr(String(r4_f_forward)),",");
AppendTo(outJ,"\"f_forward_self_inverse\":",JBool(r4_self_inverse),",");
AppendTo(outJ,"\"f_roundtrip_via_coarse_of_WordOf\":",JStr(String(r4_f_roundtrip)),",");
AppendTo(outJ,"\"roundtrip_pass\":",JBool(r4_roundtrip_pass),",");
AppendTo(outJ,"\"legacy_pr1_image_informative_only\":",JStr(String(r4_f_legacy_pr1)),",");
AppendTo(outJ,"\"legacy_redMap_image_informative_only\":",JStr(String(r4_f_legacy_redMap)));
AppendTo(outJ,"},");
AppendTo(outJ,"\"author_witness_crosscheck\":{");
AppendTo(outJ,"\"source\":\"search/certs/pent_thirdparty_gt_20260731.json coarse_reduction.charming.per_entry_rows, 20 entries, transcribed literally into this script (bits/m only; array_form/cyclic_form of the source NOT read or compared -- avoids any contact with the source's own coarse-label computation)\",");
AppendTo(outJ,"\"source_sha256\":\"5f4b6f4e000900bd847ffcbcfaf7afc0e6a12510c20caeb84abf4a6ce16ecc11\",");
AppendTo(outJ,"\"rows\":[");
for i in [1..Length(authorWitnessRows)] do
  WriteAuthorRow(outJ, authorWitnessRows[i]);
  if i < Length(authorWitnessRows) then AppendTo(outJ, ","); fi;
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"accepted_count\":",JNum(authorWitnessAcceptedCount),",");
AppendTo(outJ,"\"total\":",JNum(Length(authorWitnessRows)));
AppendTo(outJ,"},");
AppendTo(outJ,"\"base_probe_v2_sha256\":\"ff9e6f8b4801b861cfc1fabdf005a7e7de74b19d1eeb41516df0d76f9e98df19\",");
sourceSelfSha := ComputeSha256File("search/probe/wac_v1/pent_t2t3_v3_20260731.g");;
baseProbeSha := ComputeSha256File("search/probe/wac_v1/pent_t2t3_v2_20260731.g");;
AppendTo(outJ,"\"source_digest_sha256\":",JStr(sourceSelfSha),",");
AppendTo(outJ,"\"base_probe_digest_sha256\":",JStr(baseProbeSha));
AppendTo(outJ,"}");
CloseStream(outJ);;
outF := OutputTextFile("search/certs/pent_t2t3_v3_20260731.json", false);;
SetPrintFormattingStatus(outF, false);;
PrintTo(outF, sJ);;
CloseStream(outF);;
Print("\nCERT_WRITTEN\n");
Print("\nDRIVER_DONE\n");
QUIT;
