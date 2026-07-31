#############################################################################
## search/probe/wac_v1/pent_settled_struct_20260731.g
##  Extension of pent_t2t3_v31_20260731.g (repaired coarse<->fine label
##  convention). Window/cof/D5/Psi/PsiAt/coarse_of/Chk6/Hex/Pent/regression-
##  element-4/settled-measurement machinery imported byte-identical from
##  that file (v3.1 left in place unmodified; this is a new, separate probe,
##  not an edit of v3.1).
##
##  Commander's instruction (2026-07-31, following ideator's ideas_016
##  candidate slips I16-1a SETTLED-CENT / I16-1c KER-QUANT / I16-1d
##  STAR-LAG): judge all three in one GAP probe. Per each slip's own
##  "判定" section -- NO expected numeric value is hard-coded anywhere
##  below (only construction-level invariants inherited from v3.1's gates
##  -- all-20-lifted precondition, hexagon gate -- are hard-asserted, since
##  those are definitional facts already established elsewhere, not the
##  substantive research question). Everything else is measured and
##  recorded raw; interpretation is for commander/mathematician, not this
##  script.
##
##  I16-1a (SETTLED-CENT): for each of the 20 lifts (m,f), find the unique
##    automorphism phi_{m,f} in of Aut(P) (P = PN = A5) determined by
##    x |-> x^u, y |-> f^-1 y^u f (u=2m+1) -- this always exists and is
##    unique for (m,f) in GT(N_A) by construction (Aut(P) has trivial
##    centralizer of P in itself). Build H := <phi_{m,f} : (m,f) in
##    GT(N_A)> <= Aut(P) (expected |H|=20 by the already-established fact
##    |GT(N_A)|=20 and Phi injective -- hard-asserted as a construction
##    sanity check, not a research answer). Find phi_c = phi_{4,()}
##    (complex conjugation candidate per docs/week4-A5算術飽和_opus_v1.md
##    (A2)). Compute Cent := Centralizer(H, phi_c) intersected with H.
##    For each of the 20 lifts, record membership phi_{m,f} in Cent, and
##    juxtapose against the settled measurement (settled_per_lift, imported
##    logic from v3.1) for that same (m,f). NO assertion that these two
##    columns agree -- that IS the question, recorded not decided.
##
##  I16-1c (KER-QUANT): for the settled_false rows (well_defined_on_QP=true,
##    settled=false; index 125 in v3.1), the actual kernel K = Kernel(hom)
##    (order 60 per v3.1's kernel_ratio_K) is retained (v3.1 discarded it,
##    keeping only sizes) and its StructureDescription recorded, together
##    with StructureDescription(QP/K) and StructureDescription(Centralizer
##    (QP,K)) -- raw structural data, no assertion about what these should
##    be.
##
##  I16-1d (STAR-LAG): among the 20 lifts, cluster the well_defined_on_QP
##    rows (12 of them, settled or not) by literal GAP subgroup equality of
##    their K = Kernel(hom) inside the fixed ambient group QP (not just
##    isomorphism type -- actual subgroup identity), and separately count
##    the not-well-defined-on-QP rows (8) as their own non-comparable
##    bucket (no kernel object exists there). Report distinct-class count
##    and per-class multiplicity + membership list. No expected count
##    (e.g. "5 classes of 4") is asserted.
##
##  Provenance / digest binding: this file's own sha256, plus sha256 of
##  the v3.1 script it imports from (base_probe_digest_sha256) and sha256
##  of v3.1's own cert JSON (base_cert_digest_sha256) are recorded below,
##  binding this probe's output to the v3.1 witness data it is a
##  measurement-extension of. (This script recomputes shad/lift/srcRows
##  fresh from the same deterministic window rather than re-parsing v3.1's
##  JSON back into GAP objects -- same pattern v3.1 used relative to v3:
##  binding is by hash of the extended script + byte-identical imported
##  code, not by JSON round-trip. See v3.1 header for the precedent.)
##
##  Regression unit test element 4 (non-self-inverse f round trip) is
##  inherited and re-run unchanged, per commander instruction.
##
##  Single GAP lane. NOT a ledger claim -- report to commander for review.
#############################################################################

## ---- provenance helper: SHA-256 of a repo-relative file, machine-computed
## via external sha256sum (same pattern as pent_t2t3_v31_20260731.g).
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_pent_settled_struct_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1 .. 64]};
end;;

## ---- window (byte-identical to pent_t2t3_v31_20260731.g / v3 / v2) ----
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

## ---- forward coarse-label machinery (imported verbatim from v3.1) -------
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

## ---- regression unit test element 4 (inherited, re-run unchanged) -------
WordFromBits := function(bits)
  local w, b;
  w := One(Fw);
  for b in bits do
    if b = 0 then w := w * gx; else w := w * gy; fi;
  od;
  return w;
end;;
Print("\n== regression unit test element 4 (non-self-inverse f round trip, inherited from v3.1) ==\n");
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
        ". This is the exact bug pattern of pent_t2t3_v2_20260731.g. Halting.");
fi;
Print("  REGRESSION TEST 4 PASS: round trip is the identity on a ",
      "non-self-inverse f.\n");

## ---- precompute forward coarse labels for all of QP (same as v3.1) ------
Print("\n== precomputing forward coarse labels coarse_of(WordOf(q)) for all |QP|=",
      Size(QP)," elements ==\n");
qpElts := Elements(QP);;
coarseLabelOf := List(qpElts, q -> coarse_of(WordOf(q)));;
Print("  done.\n");

## ============================================================
## per-shadow witness rows for all 20 coarse shadows (identical logic to
## v3.1 -- coarse_of o WordOf fiber selection)
## ============================================================
Print("\n== witness rows for all coarse shadows ==\n");
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
  fi;
  Add(rows, row);
  Print("  id=",sid," m=",m," f=",String(f)," c1..c5=",
        [c1n,c2n,c3n,c4n,c5n]," all=",allN,
        " lift=",row.lift_exists,"\n");
  sid := sid + 1;
od;
Print("  TOTAL lifted = ",Length(lift),"/",Length(shad),"\n");

## ============================================================
## PRECONDITION GATE (inherited from v3.1): all 20 coarse shadows must
## have lifted. Hard, machine-checked, Error()s on failure.
## ============================================================
if Length(shad) <> 20 then
  Error("PRECONDITION FAIL: window does not have exactly 20 coarse shadows ",
        "(got ", Length(shad), "). Halting before all further measurement.");
fi;
if Length(lift) <> 20 then
  Error("PRECONDITION FAIL: not all 20 coarse shadows lifted (got ",
        Length(lift), "/20). This contradicts v3.1's result. Halting.");
fi;
Print("\nPRECONDITION PASS: all 20/20 coarse shadows lifted (matches v3.1).\n");

## ============================================================
## settled measurement (source kernel) for ALL 20 lifts, EXTENDED to keep
## the actual kernel group K (v3.1's SourceKernelInfo discarded K, keeping
## only sizes) -- needed below for I16-1c structure descriptions and
## I16-1d subgroup-identity clustering.
## HEXAGON GATE (inherited from v3.1, per pent_conflict_diagnosis_v1.md
## sec.1.2): c |-> c^{2m+1} is a PROPOSITION proved from hexagon, licensed
## only for (m,f) whose witness passed hexagon (c1=c2=true). Checked
## per-lift below with a hard Error() abort, not assumed.
## LEVEL CAVEAT (verbatim from v3.1 / pent_conflict_diagnosis_v1.md
## sec.1.4): this is a PB_3-level settled measurement (necessary condition
## for the PB_4-level C1 Prop 2.11 claim, not that claim itself).
## No exponent/index match is used as a settled PROOF anywhere -- settled
## always means the literal Kernel(hom) computation with Size(K)=1.
## ============================================================
Print("\n== settled measurement (extended: retains K) for ALL 20 lifts ==\n");
SourceKernelFull := function(m, q)
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
             K := K,
             kernel_ratio_K := Size(K),
             Kpi_s_quotient_size := Size(QP)/Size(K),
             Kpi_quotient_size := Size(QP),
             settled := (Size(K) = 1));
end;;

srcRows := [];;
hexGateFails := [];;
for tr in lift do
  m := tr[1];; f := tr[2];; q := tr[3];;
  chkq := Chk6(m,q);;
  if not (chkq[1] and chkq[2]) then
    Add(hexGateFails, [m, String(f)]);
    Print("  HEXAGON GATE FAIL at m=",m," f=",String(f),
          " -- c1=",chkq[1]," c2=",chkq[2],
          " -- T_{m,f}(c)=c^{2m+1} NOT licensed for this pair. Skipping.\n");
  else
    info := SourceKernelFull(m,q);
    Add(srcRows, rec(m:=m, f_perm:=String(f), f_elt:=f, q:=q, info:=info));
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
        "not pass hexagon for their chosen witness q. Halting. Failing ",
        "pairs: ", hexGateFails);
fi;
Print("\nHEXAGON GATE PASS: all 20/20 lifts' witnesses passed hexagon.\n");

settled_total := Length(srcRows);;
settled_wd_true := Number(srcRows, r -> r.info.well_defined_on_QP);;
settled_wd_false := Number(srcRows, r -> not r.info.well_defined_on_QP);;
settled_true_count := Number(srcRows, r -> r.info.well_defined_on_QP and r.info.settled);;
settled_false_count := Number(srcRows, r -> r.info.well_defined_on_QP and not r.info.settled);;
Print("\n== settled_summary ==  total=",settled_total,
      "  well_defined_on_QP=",settled_wd_true,
      "  NOT well_defined_on_QP=",settled_wd_false,
      "  settled=",settled_true_count,
      "  NOT settled=",settled_false_count,"\n");

## ============================================================
## I16-1a (SETTLED-CENT judgment): Phi image + centralizer of complex
## conjugation ĉ=[4,()], measured inside Aut(P), P=PN=A5.
## ============================================================
Print("\n== I16-1a SETTLED-CENT: Phi image and C_{Aut(P)}(chat) membership ==\n");
AutP := AutomorphismGroup(PN);;
Print("  |Aut(P)| = ", Size(AutP), " (expect 120 = |S5|, construction fact)\n");
if Size(AutP) <> 120 then
  Error("CONSTRUCTION FAIL: |Aut(PN)| <> 120 -- PN is not A5 as expected ",
        "elsewhere in this window. Halting.");
fi;

FindAutOfMF := function(m, f)
  local u, cand;
  u := 2*m+1;
  cand := Filtered(AutP, a -> Image(a,xb)=xb^u and Image(a,yb)=f^-1*yb^u*f);
  return cand;
end;;

## build Phi(m,f) for all 20 (m,f) in shad (== all 20 lifts, same 20 pairs)
phiRows := [];;
for z in shad do
  mm := z[1];; ff := z[2];;
  cand := FindAutOfMF(mm, ff);
  if Length(cand) <> 1 then
    Error("CONSTRUCTION FAIL: Phi(m,f) not unique for m=", mm, " f=", String(ff),
          " -- found ", Length(cand), " candidate automorphisms (expected ",
          "exactly 1, since C_{Aut(P)}(P)=1 for P=A5 acting by Inn). Halting.");
  fi;
  Add(phiRows, rec(m:=mm, f_perm:=String(ff), f_elt:=ff, phi:=cand[1]));
od;

H_phi := Subgroup(AutP, List(phiRows, r -> r.phi));;
Print("  |H = <Phi(m,f) : (m,f) in GT(N_A)>| = ", Size(H_phi),
      " (expect 20 = |GT(N_A)|, construction fact)\n");
if Size(H_phi) <> 20 then
  Error("CONSTRUCTION FAIL: |H| <> 20 -- Phi is not injective on this window's ",
        "GT(N_A) as expected. Halting (this would contradict the already-",
        "established fact |GT(N_A)|=20 injecting into Aut(P)).");
fi;
H_phi_desc := StructureDescription(H_phi);;
Print("  StructureDescription(H) = ", H_phi_desc, "\n");

## chat = Phi(4, ())
chatRow := First(phiRows, r -> r.m = 4 and r.f_elt = One(PN));;
if chatRow = fail then
  Error("SETUP FAIL: (m,f)=(4,()) not found among the 20 (m,f) pairs of ",
        "GT(N_A) for this window -- cannot form chat = Phi(4,()). Halting.");
fi;
chat := chatRow.phi;;
Print("  chat = Phi(4,()) found. Order(chat) = ", Order(chat), "\n");

Cent_AutP_chat := Centralizer(AutP, chat);;
Cent_H_chat := Intersection(H_phi, Cent_AutP_chat);;
Print("  |C_{Aut(P)}(chat)| = ", Size(Cent_AutP_chat),
      "   |C_H(chat)| = ", Size(Cent_H_chat),
      "   StructureDescription(C_H(chat)) = ", StructureDescription(Cent_H_chat), "\n");

## settled lookup helper (from srcRows, keyed by (m,f_perm) string)
SettledLookupStr := function(m, fstr)
  local r;
  r := First(srcRows, rr -> rr.m = m and rr.f_perm = fstr);
  if r = fail then return "row_missing"; fi;
  if not r.info.well_defined_on_QP then return "not_well_defined_on_QP"; fi;
  if r.info.settled then return "settled_true"; else return "settled_false"; fi;
end;;

i16_1a_table := [];;
for r in phiRows do
  in_cent := (r.phi in Cent_H_chat);
  settled_status := SettledLookupStr(r.m, r.f_perm);
  Add(i16_1a_table, rec(m:=r.m, f_perm:=r.f_perm,
                         phi_in_C_H_chat := in_cent,
                         settled_status := settled_status));
  Print("  m=",r.m," f=",r.f_perm,"  phi_in_C_H(chat)=",in_cent,
        "  settled_status=",settled_status,"\n");
od;

i16_1a_agree_count := Number(i16_1a_table, r ->
  (r.phi_in_C_H_chat and r.settled_status = "settled_true") or
  ((not r.phi_in_C_H_chat) and r.settled_status <> "settled_true"));;
Print("  (informational, NOT a pass/fail gate) rows where (phi_in_C_H(chat)) ",
      "agrees with (settled_status=settled_true): ", i16_1a_agree_count, "/20\n");

## ============================================================
## I16-1c (KER-QUANT judgment): structure of K and QP/K for the
## settled_false rows (well_defined_on_QP=true, settled=false).
## ============================================================
Print("\n== I16-1c KER-QUANT: structure of K_pi^s for settled_false rows ==\n");
i16_1c_table := [];;
for r in srcRows do
  if r.info.well_defined_on_QP and not r.info.settled then
    K := r.info.K;
    quotG := QP/K;
    centK := Centralizer(QP, K);
    Kdesc := StructureDescription(K);
    quotDesc := StructureDescription(quotG);
    centKdesc := StructureDescription(centK);
    rec1 := rec(m:=r.m, f_perm:=r.f_perm, K_size:=Size(K), K_desc:=Kdesc,
                quot_size:=Size(quotG), quot_desc:=quotDesc,
                centralizer_of_K_in_QP_size:=Size(centK),
                centralizer_of_K_in_QP_desc:=centKdesc);
    Add(i16_1c_table, rec1);
    Print("  m=",r.m," f=",r.f_perm,"  |K|=",Size(K)," K~=",Kdesc,
          "  |QP/K|=",Size(quotG)," QP/K~=",quotDesc,
          "  |C_QP(K)|=",Size(centK)," C_QP(K)~=",centKdesc,"\n");
  fi;
od;

## ============================================================
## I16-1d (STAR-LAG judgment): distinct-kernel clustering among the 12
## well_defined_on_QP rows (as literal GAP subgroups of the fixed ambient
## QP), plus the 8 not-well-defined-on-QP rows as a separate non-comparable
## bucket.
## ============================================================
Print("\n== I16-1d STAR-LAG: distinct source-kernel clustering ==\n");
wellRows := Filtered(srcRows, r -> r.info.well_defined_on_QP);;
notWellRows := Filtered(srcRows, r -> not r.info.well_defined_on_QP);;
Print("  well_defined_on_QP rows: ", Length(wellRows),
      "   not_well_defined_on_QP rows: ", Length(notWellRows), "\n");

kerClusters := [];;
for r in wellRows do
  cl := First(kerClusters, c -> c.rep_K = r.info.K);
  if cl = fail then
    Add(kerClusters, rec(rep_K := r.info.K, members := [r]));
  else
    Add(cl.members, r);
  fi;
od;
Print("  distinct kernel classes among well_defined_on_QP rows: ",
      Length(kerClusters), "\n");
i16_1d_clusters := [];;
for cl in kerClusters do
  sizeK := Size(cl.rep_K);
  memList := List(cl.members, m -> [m.m, m.f_perm]);
  Add(i16_1d_clusters, rec(kernel_size := sizeK,
                            kernel_structure_description := StructureDescription(cl.rep_K),
                            multiplicity := Length(cl.members),
                            members := memList));
  Print("    |K|=",sizeK,"  K~=",StructureDescription(cl.rep_K),
        "  multiplicity=",Length(cl.members),"  members=",memList,"\n");
od;
i16_1d_notwelldefined_members := List(notWellRows, r -> [r.m, r.f_perm]);;
Print("  not_well_defined_on_QP bucket: multiplicity=",Length(notWellRows),
      "  members=",i16_1d_notwelldefined_members,"\n");

## ============================================================
## regression-inherited 3-element + element-4 round-trip unit test
## (identical logic to v3.1, re-run here)
## ============================================================
Print("\n== 3-element + regression unit test (inherited from v3.1) ==\n");

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
    rec1.reduction_image_in_PN := String(red_img);
    rec1.reduction_image_equals_f := (red_img = f);
  else
    rec1.lift_exists := false;
    rec1.witness_h_word := "null";
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
Print("  u4(regression) coarse_in_GT_NA=",u4.coarse_in_GT_NA,
      "  all6_pass=",u4.all6_pass,"\n");

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
JMFPair := function(p) return Concatenation("[", JNum(p[1]), ",", JStr(p[2]), "]"); end;;
JMFList := function(l) return Concatenation("[", JoinC(List(l,JMFPair)), "]"); end;;

sJ := "";; outJ := OutputTextString(sJ,true);;
SetPrintFormattingStatus(outJ, false);;
AppendTo(outJ,"{\"schema\":\"wac_v1-pent-settled-struct-cert/v1\",");
AppendTo(outJ,"\"generated_by\":\"search/probe/wac_v1/pent_settled_struct_20260731.g\",");
AppendTo(outJ,"\"extends\":\"search/probe/wac_v1/pent_t2t3_v31_20260731.g (window/cof/D5/Psi/PsiAt/coarse_of/Chk6/Hex/Pent/regression-element-4/settled-measurement imported byte-identical). v3.1 left in place unmodified. New, separate probe -- not an edit of v3.1.\",");
AppendTo(outJ,"\"note\":\"Commander instruction 2026-07-31: judge ideas_016 candidate slips I16-1a SETTLED-CENT / I16-1c KER-QUANT / I16-1d STAR-LAG in one GAP probe. No expected numeric value for these three research questions is hard-coded anywhere (only construction-level facts already established elsewhere -- |Aut(PN)|=120, |GT(N_A)|=20 injecting into Aut(PN), all-20-lifted precondition, hexagon gate -- are hard-asserted). All substantive measurements (Phi image / centralizer membership / kernel structure descriptions / kernel clustering) are recorded raw, not gated. LEVEL CAVEAT (inherited verbatim from v3.1 / pent_conflict_diagnosis_v1.md sec.1.4): settled measurement here is PB_3-level (necessary condition for PB_4-level C1 Prop 2.11 claim, not that claim itself, unresolved). No exponent/index match used as a settled PROOF -- settled always means literal Kernel(hom) with Size(K)=1. Single GAP lane. NOT a ledger claim.\",");
AppendTo(outJ,"\"f_orientation\":\"psi_reversed_for_defect_eval__forward_coarse_of_WordOf_for_coarse_fiber_label\",");
AppendTo(outJ,"\"P_size\":",JNum(Size(PN)),",");
AppendTo(outJ,"\"N_ord\":",JNum(Nord),",");
AppendTo(outJ,"\"GT_size\":",JNum(Length(shad)),",");
AppendTo(outJ,"\"PB3_refined_size\":",JNum(Size(QP)),",");
AppendTo(outJ,"\"F2_refined_size\":",JNum(Size(QF)),",");
AppendTo(outJ,"\"lifted_total\":",JNum(Length(lift)),",");
AppendTo(outJ,"\"all_20_lifted_precondition_pass\":",JBool(Length(lift)=20),",");
AppendTo(outJ,"\"hexagon_gate_fail_count\":",JNum(Length(hexGateFails)),",");
AppendTo(outJ,"\"settled_summary\":{");
AppendTo(outJ,"\"total_rows_measured\":",JNum(settled_total),",");
AppendTo(outJ,"\"well_defined_on_QP_count\":",JNum(settled_wd_true),",");
AppendTo(outJ,"\"not_well_defined_on_QP_count\":",JNum(settled_wd_false),",");
AppendTo(outJ,"\"settled_true_count\":",JNum(settled_true_count),",");
AppendTo(outJ,"\"settled_false_count\":",JNum(settled_false_count),",");
AppendTo(outJ,"\"level_caveat\":\"PB_3-level necessary condition only -- NOT a PB_4-level (C1 Prop 2.11) settled claim\"");
AppendTo(outJ,"},");

AppendTo(outJ,"\"i16_1a_settled_cent\":{");
AppendTo(outJ,"\"AutP_size\":",JNum(Size(AutP)),",");
AppendTo(outJ,"\"H_phi_size\":",JNum(Size(H_phi)),",");
AppendTo(outJ,"\"H_phi_structure_description\":",JStr(H_phi_desc),",");
AppendTo(outJ,"\"chat_m\":4,\"chat_f_perm\":",JStr(String(One(PN))),",");
AppendTo(outJ,"\"chat_order\":",JNum(Order(chat)),",");
AppendTo(outJ,"\"C_AutP_chat_size\":",JNum(Size(Cent_AutP_chat)),",");
AppendTo(outJ,"\"C_H_chat_size\":",JNum(Size(Cent_H_chat)),",");
AppendTo(outJ,"\"C_H_chat_structure_description\":",JStr(StructureDescription(Cent_H_chat)),",");
AppendTo(outJ,"\"per_lift_table\":[");
for i in [1..Length(i16_1a_table)] do
  r := i16_1a_table[i];
  AppendTo(outJ,"{\"m\":",JNum(r.m),",\"f_perm\":",JStr(r.f_perm),
    ",\"phi_in_C_H_chat\":",JBool(r.phi_in_C_H_chat),
    ",\"settled_status\":",JStr(r.settled_status),"}");
  if i < Length(i16_1a_table) then AppendTo(outJ,","); fi;
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"informational_agree_count_NOT_a_gate\":",JNum(i16_1a_agree_count));
AppendTo(outJ,"},");

AppendTo(outJ,"\"i16_1c_ker_quant\":{");
AppendTo(outJ,"\"rows_measured\":",JNum(Length(i16_1c_table)),",");
AppendTo(outJ,"\"table\":[");
for i in [1..Length(i16_1c_table)] do
  r := i16_1c_table[i];
  AppendTo(outJ,"{\"m\":",JNum(r.m),",\"f_perm\":",JStr(r.f_perm),
    ",\"K_size\":",JNum(r.K_size),",\"K_structure_description\":",JStr(r.K_desc),
    ",\"quot_size\":",JNum(r.quot_size),",\"quot_structure_description\":",JStr(r.quot_desc),
    ",\"centralizer_of_K_in_QP_size\":",JNum(r.centralizer_of_K_in_QP_size),
    ",\"centralizer_of_K_in_QP_structure_description\":",JStr(r.centralizer_of_K_in_QP_desc),
    "}");
  if i < Length(i16_1c_table) then AppendTo(outJ,","); fi;
od;
AppendTo(outJ,"]},");

AppendTo(outJ,"\"i16_1d_star_lag\":{");
AppendTo(outJ,"\"well_defined_on_QP_rows\":",JNum(Length(wellRows)),",");
AppendTo(outJ,"\"not_well_defined_on_QP_rows\":",JNum(Length(notWellRows)),",");
AppendTo(outJ,"\"distinct_kernel_classes_among_well_defined\":",JNum(Length(i16_1d_clusters)),",");
AppendTo(outJ,"\"clusters\":[");
for i in [1..Length(i16_1d_clusters)] do
  c := i16_1d_clusters[i];
  AppendTo(outJ,"{\"kernel_size\":",JNum(c.kernel_size),
    ",\"kernel_structure_description\":",JStr(c.kernel_structure_description),
    ",\"multiplicity\":",JNum(c.multiplicity),
    ",\"members\":",JMFList(c.members),"}");
  if i < Length(i16_1d_clusters) then AppendTo(outJ,","); fi;
od;
AppendTo(outJ,"],");
AppendTo(outJ,"\"not_well_defined_bucket\":{\"multiplicity\":",
  JNum(Length(notWellRows)),",\"members\":",
  JMFList(i16_1d_notwelldefined_members),"}");
AppendTo(outJ,"},");

AppendTo(outJ,"\"unit_test_4element\":[");
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
      ",\"reduction_image_in_PN\":",JStr(r.reduction_image_in_PN),
      ",\"legacy_redMap_image_equals_f\":",JBool(r.reduction_image_equals_f));
  else
    AppendTo(outS, ",\"witness_h_word\":null",
      ",\"reduction_image_in_PN\":null,\"legacy_redMap_image_equals_f\":null");
  fi;
  AppendTo(outS, "}");
end;;
WriteUnitRow(outJ, u1); AppendTo(outJ,",");
WriteUnitRow(outJ, u2); AppendTo(outJ,",");
WriteUnitRow(outJ, u3); AppendTo(outJ,",");
WriteUnitRow(outJ, u4);
AppendTo(outJ,"],");

AppendTo(outJ,"\"regression_test_element4_roundtrip\":{");
AppendTo(outJ,"\"description\":\"mandatory hard-assert regression test, inherited and re-run from v3.1 (not just carried over as a value): non-self-inverse coarse f round-tripped coarse->fine(Psi)->coarse(coarse_of o WordOf); script Error()s (aborts before cert write) if this fails.\",");
AppendTo(outJ,"\"bits\":",JIntList(r4_bits),",");
AppendTo(outJ,"\"m\":",JNum(r4_m),",");
AppendTo(outJ,"\"f_forward_coarse\":",JStr(String(r4_f_forward)),",");
AppendTo(outJ,"\"f_forward_self_inverse\":",JBool(r4_self_inverse),",");
AppendTo(outJ,"\"f_roundtrip_via_coarse_of_WordOf\":",JStr(String(r4_f_roundtrip)),",");
AppendTo(outJ,"\"roundtrip_pass\":",JBool(r4_roundtrip_pass));
AppendTo(outJ,"},");

AppendTo(outJ,"\"base_probe_v31_sha256\":");
baseProbeV31Sha := ComputeSha256File("search/probe/wac_v1/pent_t2t3_v31_20260731.g");;
AppendTo(outJ,JStr(baseProbeV31Sha),",");
AppendTo(outJ,"\"base_cert_v31_sha256\":");
baseCertV31Sha := ComputeSha256File("search/certs/pent_t2t3_v31_20260731.json");;
AppendTo(outJ,JStr(baseCertV31Sha),",");
sourceSelfSha := ComputeSha256File("search/probe/wac_v1/pent_settled_struct_20260731.g");;
AppendTo(outJ,"\"source_digest_sha256\":",JStr(sourceSelfSha));
AppendTo(outJ,"}");
CloseStream(outJ);;
outF := OutputTextFile("search/certs/pent_settled_struct_20260731.json", false);;
SetPrintFormattingStatus(outF, false);;
PrintTo(outF, sJ);;
CloseStream(outF);;
Print("\nCERT_WRITTEN\n");
Print("\nDRIVER_DONE\n");
QUIT;
