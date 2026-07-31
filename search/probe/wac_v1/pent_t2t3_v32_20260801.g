#############################################################################
## search/probe/wac_v1/pent_t2t3_v32_20260801.g
##  v3.2 -- orientation-convention repair of the settled (source-kernel)
##  measurement in pent_t2t3_v31_20260731.g. v3.1 is left in place, byte
##  identical, unmodified.
##
##  Commander's instruction (2026-08-01, following the mathematician's
##  (Opus 5) note docs/notes/pent_settled_cent_v1.md sec.6 and the express
##  memo ops/express/20260801a_数学者Opus_SETTLED測定の向き混線_裁定293格下げ進言.md):
##  the settled measurement in v3.1's SourceKernelInfo mixes two orientation
##  conventions in one computation --
##    * the coarse LABEL f := coarse_of(WordOf(q)) is AUTHOR-side (forward),
##    * but the CONJUGATION in T_{m,f}: Psi(y) |-> q^{-1} Psi(y)^u q applies
##      the author-side formula f^{-1}(.)f directly to q, whereas Psi is an
##      ANTI-homomorphism (it reverses words before substituting), so the
##      author-side conjugation, transported through Psi, actually lands as
##      q(.)q^{-1}, not q^{-1}(.)q.
##  This file implements exactly what the commander specified, no more:
##   (A) the mathematician's "1-line hard assert" (note sec.6, "修理の指定"):
##       rho(T(Psi(y))) =?= Phi_{m,f}(ybar) = (ybar^u)^f
##       for a non-self-inverse f (the inherited element-4 witness). This is
##       recorded as a CHECKED, LOGGED boolean under BOTH conventions below
##       -- it is NOT used as an aborting Error() gate, because whether it
##       holds is exactly the open question under audit (commander: "期待値
##       を書かない" / "どちらが正かの判定は司令塔/Sol"). Aborting on a
##       result we are trying to measure would be circular and would also
##       prevent the cert (with both conventions' data) from being written.
##   (B) convention T' (note sec.6 "(U-rev) 著者側ラベルを保つ"), which flips
##       the conjugation orientation: Psi(y) |-> q Psi(y)^u q^{-1}. This is
##       computed side-by-side with the original (mixed) convention T from
##       v3.1, NOT as a replacement -- both are reported, unjudged, in the
##       cert.
##  Everything else (window, cof, D5, Psi, PsiAt, coarse_of, Chk6, Hex, Pent,
##  the coarse-shadow/lift precondition gates, the hexagon gate, and the
##  P92-1 label round-trip regression test element 4) is imported verbatim
##  from pent_t2t3_v31_20260731.g -- these are LABEL-layer facts, established
##  independently of the action-layer orientation question being repaired
##  here, and are kept as hard Error() gates exactly as in v3.1.
##
##  No exponent-match-only claim is used as a settled proof (Sol warning /
##  裁定 pitfall discipline): "settled" below always means the literal kernel
##  computation Kernel(hom) with Size(K)=1, not an index/order coincidence,
##  under EACH convention separately.
##
##  Contact-blocked: no expected settled-count value (e.g. "20/20") is
##  asserted anywhere in this file. Both conventions' settled_summary are
##  computed and written to the cert unjudged; judgement is deferred to
##  commander/Sol per instruction. Single GAP lane. NOT a ledger claim --
##  report to commander for review.
#############################################################################

## ---- provenance helper: SHA-256 of a repo-relative file, machine-computed
## via external sha256sum (same pattern as v3/v3.1) -- used below both for
## this script's own digest and to bind the mathematician's note + express
## memo that specify the repair, so the cert is traceable to its instructions.
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_pent_v32_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

## ---- window (byte-identical to pent_t2t3_v3_20260731.g / v2 / v3.1) ----
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

## ---- sigma-conjugation (identical to v2/v3/v3.1) ----
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

## ---- (imported verbatim from v3.1) P92-1 label round-trip regression
## unit test element 4 -- LABEL layer only, unaffected by the action-layer
## orientation repair below. Kept as a hard Error() gate exactly as in v3.1.
WordFromBits := function(bits)
  local w, b;
  w := One(Fw);
  for b in bits do
    if b = 0 then w := w * gx; else w := w * gy; fi;
  od;
  return w;
end;;
Print("\n== P92-1 regression unit test element 4 (non-self-inverse f round trip, label layer, inherited from v3/v3.1) ==\n");
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
r4_roundtrip_pass := (r4_f_roundtrip = r4_f_forward);;
if not r4_roundtrip_pass then
  Error("REGRESSION FAIL (P92-1, label layer): coarse<->fine label round-trip ",
        "broken for non-self-inverse f = ", String(r4_f_forward),
        " -- got back ", String(r4_f_roundtrip),
        ". Halting.");
fi;
Print("  P92-1 REGRESSION PASS: label round trip is the identity on a ",
      "non-self-inverse f.\n");

## ---- precompute forward coarse labels for all of QP (same as v3/v3.1) ---
Print("\n== precomputing forward coarse labels coarse_of(WordOf(q)) for all |QP|=",
      Size(QP)," elements ==\n");
qpElts := Elements(QP);;
coarseLabelOf := List(qpElts, q -> coarse_of(WordOf(q)));;
Print("  done.\n");

## ============================================================
## (2) per-shadow witness cert: iterate ALL 20 coarse shadows
##     (identical logic to v3/v3.1 -- coarse_of o WordOf fiber selection)
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
    row.hexagon_pass_for_witness := (tab[witIdx][1] and tab[witIdx][2]);
    Add(lift, [m,f,q]);
  else
    row.lift_exists := false;
    row.witness_h_word := "null";
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
## PRECONDITION GATE (imported verbatim from v3.1): all 20 coarse shadows
## must have lifted. Hard Error() gate, unchanged.
## ============================================================
if Length(shad) <> 20 then
  Error("PRECONDITION FAIL: window does not have exactly 20 coarse shadows ",
        "(got ", Length(shad), "). Halting before settled measurement.");
fi;
if Length(lift) <> 20 then
  Error("PRECONDITION FAIL: not all 20 coarse shadows lifted (got ",
        Length(lift), "/20). Halting before settled measurement -- do not ",
        "silently measure a partial set.");
fi;
Print("\nPRECONDITION PASS: all 20/20 coarse shadows lifted (matches v3/v3.1).\n");

## ============================================================
## (v3.2 REPAIR) settled measurement, TWO conventions side by side.
##
##  Convention T  (= v3.1's SourceKernelInfo, kept UNCHANGED for informative
##                  reproduction of the old mixed-orientation values):
##    Psi(x) |-> Psi(x)^u,  Psi(y) |-> q^{-1} Psi(y)^u q,  Psi(c) |-> Psi(c)^u.
##  Convention T' (note sec.6 "(U-rev)" repair -- flips the conjugation to
##                 match Psi's anti-homomorphism orientation, keeping the
##                 author-side label f):
##    Psi(x) |-> Psi(x)^u,  Psi(y) |-> q Psi(y)^u q^{-1},  Psi(c) |-> Psi(c)^u.
##
##  HEXAGON GATE (imported verbatim from v3.1): the c |-> c^{2m+1} rule is a
##  PROPOSITION (C1 Cor 2.8 (2.29)) proved USING the hexagon relations --
##  licensed only for (m,f) whose witness q passed hexagon (c1,c2 true).
##  Checked per-lift below with a hard Error() abort, applies identically to
##  both conventions since the c-image is convention-independent.
## ============================================================
Print("\n== (v3.2) settled measurement, both conventions, for ALL 20 lifts ==\n");

SourceKernelInfoT := function(m, q)
  local u, phix, phiy, phic, hom, K;
  u := 2*m+1;
  phix := Psi(gx)^u;
  phiy := q^-1 * Psi(gy)^u * q;
  phic := Psi(gc)^u;
  hom := GroupHomomorphismByImages(QP, QP, gensQP, [phix,phiy,phic]);
  if hom = fail then
    return rec(well_defined_on_QP := false,
      phiy_elt := phiy,
      note := "T_{m,f} (mixed convention, v3.1) does not descend to QP.");
  fi;
  K := Kernel(hom);
  return rec(well_defined_on_QP := true, phiy_elt := phiy,
             kernel_ratio_K := Size(K),
             Kpi_s_quotient_size := Size(QP)/Size(K),
             Kpi_quotient_size := Size(QP),
             settled := (Size(K) = 1));
end;;

SourceKernelInfoTprime := function(m, q)
  local u, phix, phiy, phic, hom, K;
  u := 2*m+1;
  phix := Psi(gx)^u;
  phiy := q * Psi(gy)^u * q^-1;
  phic := Psi(gc)^u;
  hom := GroupHomomorphismByImages(QP, QP, gensQP, [phix,phiy,phic]);
  if hom = fail then
    return rec(well_defined_on_QP := false,
      phiy_elt := phiy,
      note := "T'_{m,f} (aligned convention, v3.2 repair) does not descend to QP.");
  fi;
  K := Kernel(hom);
  return rec(well_defined_on_QP := true, phiy_elt := phiy,
             kernel_ratio_K := Size(K),
             Kpi_s_quotient_size := Size(QP)/Size(K),
             Kpi_quotient_size := Size(QP),
             settled := (Size(K) = 1));
end;;

## ---- (v3.2 NEW) mathematician's 1-line action-layer assert (note sec.6,
## "修理の指定"): rho(T(Psi(y))) =?= Phi_{m,f}(ybar) = (ybar^u)^f.
## Computed (LOGGED, not Error()-aborting) under BOTH conventions for every
## one of the 20 lifted (m,f,q) triples -- whether it holds is exactly the
## question under audit, per commander instruction ("期待値を書かない" /
## judgement deferred to commander/Sol). redMap is applied directly to the
## phiy element, independent of whether the full hom is well-defined.
ActionTriangleCheck := function(m, f, phiy_elt)
  local u, lhs, rhs;
  u := 2*m+1;
  lhs := Image(redMap, phiy_elt);
  rhs := (yb^u)^f;
  return rec(lhs := String(lhs), rhs := String(rhs), pass := (lhs = rhs));
end;;

srcRows := [];;
hexGateFails := [];;
for tr in lift do
  m := tr[1];; f := tr[2];; q := tr[3];;
  ## hexagon gate: recompute c1,c2 for this exact witness q (not just trust
  ## the row cache) before licensing c |-> c^{2m+1}. Imported from v3.1.
  chkq := Chk6(m,q);;
  if not (chkq[1] and chkq[2]) then
    Add(hexGateFails, [m, String(f)]);
    Print("  HEXAGON GATE FAIL at m=",m," f=",String(f),
          " -- c1=",chkq[1]," c2=",chkq[2],
          " -- T_{m,f}(c)=c^{2m+1} NOT licensed for this pair. Skipping settled measurement for this lift.\n");
  else
    infoT := SourceKernelInfoT(m,q);;
    infoTp := SourceKernelInfoTprime(m,q);;
    actT := ActionTriangleCheck(m,f,infoT.phiy_elt);;
    actTp := ActionTriangleCheck(m,f,infoTp.phiy_elt);;
    Add(srcRows, rec(m:=m, f_perm:=String(f), infoT:=infoT, infoTp:=infoTp,
                      actT:=actT, actTp:=actTp));
    Print("  m=",m," f=",String(f),
          "  [T  mixed]  wd=",infoT.well_defined_on_QP,
          "  settled=", (infoT.well_defined_on_QP and infoT.settled),
          "  action_assert_pass=",actT.pass,
          "  [T' aligned] wd=",infoTp.well_defined_on_QP,
          "  settled=", (infoTp.well_defined_on_QP and infoTp.settled),
          "  action_assert_pass=",actTp.pass,"\n");
  fi;
od;
if Length(hexGateFails) > 0 then
  Error("HEXAGON GATE FAIL: ", Length(hexGateFails), " of the 20 lifts did ",
        "not pass hexagon for their chosen witness q -- this should not ",
        "happen given all6_pass=1 rows in v3/v3.1, so halting for review ",
        "rather than silently applying c->c^{2m+1} outside its license. ",
        "Failing pairs: ", hexGateFails);
fi;
Print("\nHEXAGON GATE PASS: all 20/20 lifts' witnesses passed hexagon (c1=c2=true) -- T_{m,f}(c)=c^{2m+1} is licensed for every one.\n");

## settled_summary rollup, BOTH conventions, unjudged (v3.2 -- reproduces
## v3.1's mixed-convention values under T for regression, and reports T'
## side by side; NO expected-value assert on either).
settled_total := Length(srcRows);;
settled_wd_true_T := Number(srcRows, r -> r.infoT.well_defined_on_QP);;
settled_wd_false_T := Number(srcRows, r -> not r.infoT.well_defined_on_QP);;
settled_true_count_T := Number(srcRows, r -> r.infoT.well_defined_on_QP and r.infoT.settled);;
settled_false_count_T := Number(srcRows, r -> r.infoT.well_defined_on_QP and not r.infoT.settled);;
settled_wd_true_Tp := Number(srcRows, r -> r.infoTp.well_defined_on_QP);;
settled_wd_false_Tp := Number(srcRows, r -> not r.infoTp.well_defined_on_QP);;
settled_true_count_Tp := Number(srcRows, r -> r.infoTp.well_defined_on_QP and r.infoTp.settled);;
settled_false_count_Tp := Number(srcRows, r -> r.infoTp.well_defined_on_QP and not r.infoTp.settled);;
actionAssertPassCount_T := Number(srcRows, r -> r.actT.pass);;
actionAssertPassCount_Tp := Number(srcRows, r -> r.actTp.pass);;

Print("\n== settled_summary [T mixed, informative reproduction of v3.1] ==",
      "  total=",settled_total,
      "  well_defined=",settled_wd_true_T,
      "  NOT well_defined=",settled_wd_false_T,
      "  settled=",settled_true_count_T,
      "  NOT settled=",settled_false_count_T,
      "  action_assert_pass=",actionAssertPassCount_T,"/20\n");
Print("== settled_summary [T' aligned, v3.2 repair] ==",
      "  total=",settled_total,
      "  well_defined=",settled_wd_true_Tp,
      "  NOT well_defined=",settled_wd_false_Tp,
      "  settled=",settled_true_count_Tp,
      "  NOT settled=",settled_false_count_Tp,
      "  action_assert_pass=",actionAssertPassCount_Tp,"/20\n");

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

WriteConvInfo := function(outS, info)
  AppendTo(outS, "{\"well_defined_on_QP\":",JBool(info.well_defined_on_QP));
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

WriteActCheck := function(outS, act)
  AppendTo(outS, "{\"lhs_rho_T_of_psiY\":",JStr(act.lhs),
    ",\"rhs_Phi_mf_ybar\":",JStr(act.rhs),
    ",\"pass\":",JBool(act.pass),"}");
end;;

WriteSettledRow := function(outS, sr)
  AppendTo(outS, "{\"m\":",JNum(sr.m),",\"f_perm\":",JStr(sr.f_perm),
    ",\"hexagon_gate_pass\":true",
    ",\"convention_T_mixed_v31\":");
  WriteConvInfo(outS, sr.infoT);
  AppendTo(outS, ",\"convention_Tprime_aligned_v32\":");
  WriteConvInfo(outS, sr.infoTp);
  AppendTo(outS, ",\"action_triangle_assert_T_mixed\":");
  WriteActCheck(outS, sr.actT);
  AppendTo(outS, ",\"action_triangle_assert_Tprime_aligned\":");
  WriteActCheck(outS, sr.actTp);
  AppendTo(outS, "}");
end;;

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
      ",\"hexagon_pass_for_witness\":",JBool(r.hexagon_pass_for_witness),
      ",\"dies_at\":[]");
  else
    AppendTo(outS, ",\"witness_h_word\":null",
      ",\"hexagon_pass_for_witness\":null",
      ",\"dies_at\":",JList(r.dies_at));
  fi;
  AppendTo(outS, "}");
end;;

sJ := "";; outJ := OutputTextString(sJ,true);;
SetPrintFormattingStatus(outJ, false);;
AppendTo(outJ,"{\"schema\":\"wac_v1-pent-t2t3-cert/v3.2\",");
AppendTo(outJ,"\"generated_by\":\"search/probe/wac_v1/pent_t2t3_v32_20260801.g\",");
AppendTo(outJ,"\"extends\":\"search/probe/wac_v1/pent_t2t3_v31_20260731.g (window/cof/D5/Psi/PsiAt/coarse_of/Chk6/Hex/Pent/precondition-gates/hexagon-gate/P92-1-regression imported byte-identical). v3.1 left in place unmodified.\",");
AppendTo(outJ,"\"note\":\"Commander instruction (2026-08-01, following mathematician (Opus 5) note docs/notes/pent_settled_cent_v1.md sec.6 (修理の指定) and express memo ops/express/20260801a_数学者Opus_SETTLED測定の向き混線_裁定293格下げ進言.md): the v3.1 settled measurement (SourceKernelInfo, T: Psi(y)|->q^{-1}Psi(y)^u q) mixes an author-side label f=coarse_of(WordOf(q)) with a conjugation orientation that, per Psi being an anti-homomorphism, should have been transported as q(.)q^{-1} (convention T', 'aligned'), not q^{-1}(.)q. This file computes settled (well_defined_on_QP + Kernel(hom) literal computation, Size(K)=1) under BOTH conventions T (mixed, byte-identical formula to v3.1, kept for informative reproduction of the old 4/8/8-shaped values) and T' (aligned, this file's repair candidate), side by side, UNJUDGED. It also computes the mathematician's 1-line action-layer assert rho(T(Psi(y)))=?=(ybar^u)^f for every one of the 20 lifts under both conventions, LOGGED as data (not an aborting Error() gate -- whether it holds is exactly the question under audit; an aborting gate here would be circular and would prevent the cert from being written at all). No exponent/index match is used as a settled PROOF -- settled always means the literal Kernel(hom) computation with Size(K)=1, under each convention separately. Contact-blocked: no expected settled-count (e.g. '20/20') or expected action-assert-pass-count is asserted anywhere in this file; both conventions' full results are written to the cert for commander/Sol judgement per instruction. LEVEL CAVEAT (unchanged from v3.1, verbatim from docs/notes/pent_conflict_diagnosis_v1.md sec.1.4): this remains a PB_3-level measurement, a NECESSARY CONDITION for the PB_4-level (C1 Prop 2.11) settled claim, not the PB_4-level claim itself. Raw measurement, single GAP lane. NOT a ledger claim.\",");
AppendTo(outJ,"\"f_orientation\":\"psi_reversed_for_defect_eval__forward_coarse_of_WordOf_for_coarse_fiber_label (label layer, unchanged from v3.1 -- the repair below is to the ACTION-layer conjugation orientation only, per note sec.6)\",");
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
AppendTo(outJ,"\"settled_summary_T_mixed_v31_informative\":{");
AppendTo(outJ,"\"total_rows_measured\":",JNum(settled_total),",");
AppendTo(outJ,"\"well_defined_on_QP_count\":",JNum(settled_wd_true_T),",");
AppendTo(outJ,"\"not_well_defined_on_QP_count\":",JNum(settled_wd_false_T),",");
AppendTo(outJ,"\"settled_true_count\":",JNum(settled_true_count_T),",");
AppendTo(outJ,"\"settled_false_count\":",JNum(settled_false_count_T),",");
AppendTo(outJ,"\"action_triangle_assert_pass_count\":",JNum(actionAssertPassCount_T),",");
AppendTo(outJ,"\"description\":\"byte-identical formula to v3.1 SourceKernelInfo, computed here for regression reproduction of the old cert values (commander: 混成規約の旧値(4/8/8)を informative欄で再現確認)\"");
AppendTo(outJ,"},");
AppendTo(outJ,"\"settled_summary_Tprime_aligned_v32_repair\":{");
AppendTo(outJ,"\"total_rows_measured\":",JNum(settled_total),",");
AppendTo(outJ,"\"well_defined_on_QP_count\":",JNum(settled_wd_true_Tp),",");
AppendTo(outJ,"\"not_well_defined_on_QP_count\":",JNum(settled_wd_false_Tp),",");
AppendTo(outJ,"\"settled_true_count\":",JNum(settled_true_count_Tp),",");
AppendTo(outJ,"\"settled_false_count\":",JNum(settled_false_count_Tp),",");
AppendTo(outJ,"\"action_triangle_assert_pass_count\":",JNum(actionAssertPassCount_Tp),",");
AppendTo(outJ,"\"description\":\"psi(y) |-> q Psi(y)^u q^{-1} (note sec.6 (U-rev) T'), computed here unjudged -- NOT asserted to equal any expected value\"");
AppendTo(outJ,"},");
AppendTo(outJ,"\"level_caveat\":\"PB_3-level necessary condition only, per pent_conflict_diagnosis_v1.md sec.1.4 -- NOT a PB_4-level (C1 Prop 2.11) settled claim, for EITHER convention\",");
AppendTo(outJ,"\"regression_test_P92_1_element4_label_roundtrip\":{");
AppendTo(outJ,"\"description\":\"label-layer round trip (P92-1), imported from v3/v3.1 unchanged, hard Error()-gated above (script would have halted before reaching this point if it failed).\",");
AppendTo(outJ,"\"bits\":",JIntList(r4_bits),",");
AppendTo(outJ,"\"m\":",JNum(r4_m),",");
AppendTo(outJ,"\"f_forward_coarse\":",JStr(String(r4_f_forward)),",");
AppendTo(outJ,"\"f_forward_self_inverse\":",JBool(r4_self_inverse),",");
AppendTo(outJ,"\"f_roundtrip_via_coarse_of_WordOf\":",JStr(String(r4_f_roundtrip)),",");
AppendTo(outJ,"\"roundtrip_pass\":",JBool(r4_roundtrip_pass));
AppendTo(outJ,"},");
AppendTo(outJ,"\"base_probe_v31_sha256_binding\":\"computed_below\",");
sourceSelfSha := ComputeSha256File("search/probe/wac_v1/pent_t2t3_v32_20260801.g");;
baseProbeSha := ComputeSha256File("search/probe/wac_v1/pent_t2t3_v31_20260731.g");;
mathNoteSha := ComputeSha256File("docs/notes/pent_settled_cent_v1.md");;
expressMemoSha := ComputeSha256File("ops/express/20260801a_数学者Opus_SETTLED測定の向き混線_裁定293格下げ進言.md");;
AppendTo(outJ,"\"source_digest_sha256\":",JStr(sourceSelfSha),",");
AppendTo(outJ,"\"base_probe_v31_digest_sha256\":",JStr(baseProbeSha),",");
AppendTo(outJ,"\"mathematician_note_digest_sha256\":",JStr(mathNoteSha),",");
AppendTo(outJ,"\"mathematician_note_path\":\"docs/notes/pent_settled_cent_v1.md\",");
AppendTo(outJ,"\"express_memo_digest_sha256\":",JStr(expressMemoSha),",");
AppendTo(outJ,"\"express_memo_path\":\"ops/express/20260801a_数学者Opus_SETTLED測定の向き混線_裁定293格下げ進言.md\"");
AppendTo(outJ,"}");
CloseStream(outJ);;
outF := OutputTextFile("search/certs/pent_t2t3_v32_20260801.json", false);;
SetPrintFormattingStatus(outF, false);;
PrintTo(outF, sJ);;
CloseStream(outF);;
Print("\nCERT_WRITTEN\n");
Print("\nDRIVER_DONE\n");
QUIT;
