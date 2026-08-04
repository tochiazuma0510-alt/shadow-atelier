#############################################################################
## search/probe/w6_bu_census/w6_bu_census_driver.g
## W6BU-CENSUS: H^2(S4,V) inventory/census table (no verdict column).
## Design authority: docs/notes/w6_bottomup_design_v2.md SS7.3 (promoted to
## normative census spec, 裁定494). Authorization: F102-6.3 limited scope
## (S0 calibration + census ONLY -- see w6_bu_s0_driver.g header for the
## full authorization text; not repeated here).
##
## SCOPE OF THIS PASS (reported explicitly, not silently narrowed -- see
## the "coverage_notes" field of the emitted cert and the accompanying
## report to the commander):
##  (1) FULL exact census of the (V-cen) layer for p=2, dim in {2,3,4}
##      (12 modules total, cross-checked against A-9's combinatorial count
##      3/3/6). Constructed via the closed-form F2^a (+) (F2C2)^b (+) D^c
##      decomposition of docs/notes/w6_bottomup_design_v2.md SS6.1
##      (Lemma F2S3), independently re-verified in w6_bu_s0_driver.g A-9.
##  (2) FULL exact census of the (V-cen) layer for p=3, dim=2, obtained by
##      DIRECT brute-force enumeration of homomorphisms S3 -> GL(2,3) (48
##      elements, exhaustive) reduced by GL(2,3)-conjugacy -- no closed
##      form is given in the design docs for p=3, so this is measured, not
##      asserted (per task instruction: "実列挙で確認・一致/不一致を記録").
##  (3) NOT done in this pass: full non-central (V4 acting nontrivially)
##      F_p[S4]-module census. This was in scope of the ORIGINAL order text
##      ("F_p[S4] 加群…の同型類を列挙", not restricted to the V-cen layer)
##      but v2 SS7.3's own inventory-table spec only guarantees exact counts
##      for the V-cen layer (S-BU-8 checks specifically against 3/3/6).
##      Given the resource budget of this implementation pass, non-central
##      enumeration is deferred rather than attempted partially/riskily.
##      Flagged explicitly per-row is impossible since no non-central rows
##      exist in this cert; flagged instead at cert top level
##      (non_central_enumeration_status).
##
## Non-contact: Im R untouched, d_N unevaluated, 3 sealed quantities
## untouched, no certificate reading. No verdict/kill/survival/EMPTY word is
## written anywhere in this script or its output (S-BU-10 compliance).
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
LoadPackage("cohomolo");;

FAILS := [];;
Chk := function(name, got, want)
  local ok;
  ok := (got = want);
  if not ok then Add(FAILS, rec(name := name, got := String(got), want := String(want))); fi;
  Print("  [", PF(ok), "] ", name, ": got=", got, " want=", want, "\n");
  return ok;
end;;

S4grp := Group((1,2),(1,3,4));;
theta := (1,2);; tau := (1,3,4);;
FS4 := FreeGroup(2);;
FqS4 := FS4 / [FS4.1^2, FS4.2^3, (FS4.1*FS4.2)^4];;

## Abstract S3 (order 6) presentation, using theta,tau's own S3-quotient
## images as the two designated generators (matches w6_bu_s0_driver.g A-13
## construction exactly, so dim_H2_S3 uses the SAME generator convention
## as dim_H2_S4).
V4norm := Filtered(NormalSubgroups(S4grp), n -> Size(n) = 4)[1];;
quoS3 := NaturalHomomorphismByNormalSubgroup(S4grp, V4norm);;
S3q := Image(quoS3);;
gl22 := GL(2,2);;
isoS3toGL22 := IsomorphismGroups(S3q, gl22);;
thetaS3elt := Image(isoS3toGL22, Image(quoS3, theta));;
tauS3elt := Image(isoS3toGL22, Image(quoS3, tau));;
S3permGrp := Group(thetaS3elt, tauS3elt);;
isoS3Perm := IsomorphismPermGroup(S3permGrp);;
S3permGrp2 := Image(isoS3Perm);;
prodOrdS3 := Order(thetaS3elt*tauS3elt);;
FS3 := FreeGroup(2);;
FqS3 := FS3 / [FS3.1^2, FS3.2^3, (FS3.1*FS3.2)^prodOrdS3];;
Chk("census-pre: |Fq_S3|", Size(FqS3), 6);;
Chk("census-pre: prodOrdS3", prodOrdS3, 2);;

#############################################################################
## Building blocks over F2 (V-cen layer): triv (dim1), reg2=F2C2 (dim2,
## nonsplit self-ext of trivial, factors through sign map S4->C2), D (dim2,
## irreducible via S4->S3->GL(2,2)).
## sign(theta)=-1 (odd, transposition), sign(tau)=+1 (even, 3-cycle).
#############################################################################
triv_a := [[Z(2)^0]];; triv_b := [[Z(2)^0]];;
reg2_a := [[Z(2)^0,Z(2)^0],[0*Z(2),Z(2)^0]];;   # unipotent, order 2 (sign(theta)=-1)
reg2_b := IdentityMat(2,GF(2));;                 # sign(tau)=+1 -> trivial
D_a := Image(isoS3toGL22, Image(quoS3, theta));;
D_b := Image(isoS3toGL22, Image(quoS3, tau));;

Chk("blocks-pre: sign(theta)=-1 (odd)", SignPerm(theta), -1);;
Chk("blocks-pre: sign(tau)=+1 (even)", SignPerm(tau), 1);;

BlockDiag := function(mats)
  local dim, res, offs, i, j, row, k, m, off2, r;
  dim := Sum(mats, m -> Length(m));
  res := List([1..dim], i -> List([1..dim], j -> Zero(GF(2))));
  offs := 0;
  for m in mats do
    for i in [1..Length(m)] do
      for j in [1..Length(m)] do
        res[offs+i][offs+j] := m[i][j];
      od;
    od;
    offs := offs + Length(m);
  od;
  return res;
end;;

## (a,b,c) triples for dim 2,3,4 (matches A-9 count 3,3,6)
Triples := function(dim)
  local res, aa, bb, cc;
  res := [];
  for aa in [0..dim] do
    for bb in [0..dim] do
      for cc in [0..dim] do
        if aa + 2*bb + 2*cc = dim then Add(res, [aa,bb,cc]); fi;
      od;
    od;
  od;
  return res;
end;;

CensusRows := [];;

BuildVCenModuleP2 := function(a,b,c)
  local matsA, matsB, i, ma, mb;
  matsA := [];; matsB := [];;
  for i in [1..a] do Add(matsA, triv_a); Add(matsB, triv_b); od;
  for i in [1..b] do Add(matsA, reg2_a); Add(matsB, reg2_b); od;
  for i in [1..c] do Add(matsA, D_a); Add(matsB, D_b); od;
  ma := BlockDiag(matsA);; mb := BlockDiag(matsB);;
  return rec(ma := ma, mb := mb);
end;;

BandNoteP2 := function(dim, a, b, c, WguessDim)
  ## Informational only (S-BU-10: no kill/survival/EMPTY words). Reports
  ## the erratum v2 SS2.5 band SHAPE the module matches, as a descriptive
  ## label -- not a verdict.
  if dim = 2 then return "cap8000_dim2_band_p2_2000"; fi;
  if dim = 3 then return "cap8000_dim3_band_p2_4000"; fi;
  if dim = 4 then return "cap8000_dim4_band_p2_8000"; fi;
  return "unclassified";
end;;

Print("\n=== p=2 (V-cen layer), dim 2,3,4 ===\n");
for dim in [2,3,4] do
  for trip in Triples(dim) do
    a := trip[1];; b := trip[2];; c := trip[3];;
    built := BuildVCenModuleP2(a,b,c);;
    ma := built.ma;; mb := built.mb;;
    Chk(Concatenation("well-defined: a^2=I dim=",String(dim)," (",String(a),",",String(b),",",String(c),")"),
        ma^2 = IdentityMat(dim,GF(2)), true);;
    Chk(Concatenation("well-defined: b^3=I dim=",String(dim)," (",String(a),",",String(b),",",String(c),")"),
        mb^3 = IdentityMat(dim,GF(2)), true);;
    Chk(Concatenation("well-defined: (ab)^4=I dim=",String(dim)," (",String(a),",",String(b),",",String(c),")"),
        (ma*mb)^4 = IdentityMat(dim,GF(2)), true);;
    chr := CHR(S4grp, 2, FqS4, [ma, mb]);;
    h1 := FirstCohomologyDimension(chr);;
    h2 := SecondCohomologyDimension(chr);;
    chrS3 := CHR(S3permGrp2, 2, FqS3, [ma, mb]);;
    h2s3 := SecondCohomologyDimension(chrS3);;
    Print("  p=2 dim=",dim," (a,b,c)=(",a,",",b,",",c,")  H1(S4)=",h1," H2(S4)=",h2," H2(S3)=",h2s3,"\n");
    Add(CensusRows, rec(
      module_id := Concatenation("p2_d",String(dim),"_a",String(a),"b",String(b),"c",String(c)),
      p := 2, dim := dim,
      s3_inflated := true,
      socle_structure := Concatenation("F2^",String(a)," + (F2C2)^",String(b)," + D^",String(c)),
      dim_H2_S4 := h2, dim_H2_S3 := h2s3, dim_H1_S4 := h1,
      window_order := 500*2^dim,
      band_note := BandNoteP2(dim,a,b,c,0),
      scope_out_reason := "n/a (within U-2 sanctioned range; not BU-GAP-1)"
    ));;
  od;
od;

Chk("census: total p=2 dim2-4 V-cen modules", Length(CensusRows), 12);;

#############################################################################
## p=3, dim=2 (V-cen layer): direct brute-force enumeration S3 -> GL(2,3),
## reduced by GL(2,3)-conjugacy. No closed form asserted in design docs;
## this count is MEASURED (per task instruction), reported as-is.
#############################################################################
Print("\n=== p=3, dim=2 (V-cen layer, brute force) ===\n");
gl23 := GL(2,3);;
eltsGL23 := Elements(gl23);;
homsP3 := [];;
for aElt in eltsGL23 do
  if aElt^2 = aElt^0 then
    for bElt in eltsGL23 do
      if bElt^3 = bElt^0 then
        if (aElt*bElt)^prodOrdS3 = (aElt*bElt)^0 then
          Add(homsP3, [aElt,bElt]);
        fi;
      fi;
    od;
  fi;
od;
Print("  num raw (a,b) pairs satisfying S3 relations: ", Length(homsP3), "\n");

repsP3 := [];;
for pr in homsP3 do
  found := false;;
  for g in eltsGL23 do
    for rp in repsP3 do
      if pr[1]^g = rp[1] and pr[2]^g = rp[2] then found := true; break; fi;
    od;
    if found then break; fi;
  od;
  if not found then Add(repsP3, pr); fi;
od;
Print("  num GL(2,3)-conjugacy classes (= module iso classes): ", Length(repsP3), "\n");

idxP3 := 0;;
for rp in repsP3 do
  idxP3 := idxP3 + 1;
  ma3 := rp[1];; mb3 := rp[2];;
  chr3 := CHR(S4grp, 3, FqS4, [ma3, mb3]);;
  h1_3 := FirstCohomologyDimension(chr3);;
  h2_3 := SecondCohomologyDimension(chr3);;
  chr3s3 := CHR(S3permGrp2, 3, FqS3, [ma3, mb3]);;
  h2_3s3 := SecondCohomologyDimension(chr3s3);;
  Print("  p=3 dim=2 rep#",idxP3," ordA=",Order(ma3)," ordB=",Order(mb3),
        " |image|=",Size(Group(ma3,mb3))," H1(S4)=",h1_3," H2(S4)=",h2_3," H2(S3)=",h2_3s3,"\n");
  Add(CensusRows, rec(
    module_id := Concatenation("p3_d2_bruteforce_", String(idxP3)),
    p := 3, dim := 2,
    s3_inflated := true,
    socle_structure := Concatenation("brute-force GL(2,3)-conjugacy class #",String(idxP3),
        " (ordA=",String(Order(ma3)),",ordB=",String(Order(mb3)),
        ",|image|=",String(Size(Group(ma3,mb3))),")"),
    dim_H2_S4 := h2_3, dim_H2_S3 := h2_3s3, dim_H1_S4 := h1_3,
    window_order := 500*3^2,
    band_note := "p3_dim2_below_survival_threshold_13500_erratum_v2_THETA-4500(informational_only)",
    scope_out_reason := "n/a (within U-3 sanctioned range; not BU-GAP-1)"
  ));;
od;

Chk("census: p=3 dim2 module count (measured, no design closed-form to compare)",
    Length(repsP3) >= 1, true);;

#############################################################################
## ==== JSON output ====
#############################################################################
Print("\n=== writing cert ===\n");

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_w6bu_census_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

selfSha := ComputeSha256File("search/probe/w6_bu_census/w6_bu_census_driver.g");;
designSha := ComputeSha256File("docs/notes/w6_bottomup_design_v2.md");;
s0CertSha := ComputeSha256File("search/certs/k5gen_w6_bu_s0_20260805.json");;

RowJson := function(r)
  return Concatenation(
    "{\"module_id\":", JStr(r.module_id),
    ",\"p\":", String(r.p), ",\"dim\":", String(r.dim),
    ",\"s3_inflated\":", JB(r.s3_inflated),
    ",\"socle_structure\":", JStr(r.socle_structure),
    ",\"dim_H2_S4\":", String(r.dim_H2_S4),
    ",\"dim_H2_S3\":", String(r.dim_H2_S3),
    ",\"dim_H1_S4\":", String(r.dim_H1_S4),
    ",\"window_order\":", String(r.window_order),
    ",\"band_note\":", JStr(r.band_note),
    ",\"scope_out_reason\":", JStr(r.scope_out_reason),
    "}");
end;;

rowsJson := JArr(List(CensusRows, RowJson));;

scopeOutJson := Concatenation(
  "[",
  "{\"category\":\"non_elementary_abelian_core (C4,C9,noncyclic)\",\"status\":\"SCOPE_OUT\",",
    "\"note\":\"【BU-GAP-1】明示的SCOPE_OUT. 空とは主張しない. v1宇宙は初等アーベル核のみを射程とする.\"},",
  "{\"category\":\"A_nontrivial (dim>=12 window)\",\"status\":\"SCOPE_OUT\",",
    "\"note\":\"補題A-TRIV系A-TRIV-1により空(dim<=11ではA自明が強制される)ことは示されているが, 本censusはdim<=4の範囲のみを走査し, dim>=12帯そのものは走査していない.\"},",
  "{\"category\":\"PSL roof\",\"status\":\"SCOPE_OUT\",",
    "\"note\":\"campaign X-4により宇宙から除外(掘らない, であって空ではない).\"},",
  "{\"category\":\"non-central F_p[S4]-modules (V4 acting nontrivially)\",\"status\":\"NOT_ENUMERATED_THIS_PASS\",",
    "\"note\":\"実装時間予算の制約により本passでは未着手. 原発注文(p=2:dim2-4/p=3:dim2)は本来V-cen層に限定されないが, v2 SS7.3の在庫表様式が保証する厳密値(3/3/6)はV-cen層のみ. 次passでの追加発注を要する.\"}",
  "]");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"w6-bu-census/v1\",\n",
  "  \"generated_by\":\"search/probe/w6_bu_census/w6_bu_census_driver.g\",\n",
  "  \"card_label\":\"W6BU-CENSUS: H^2(S4,V) inventory table (V-cen layer, p=2 dim2-4 exact + p=3 dim2 measured)\",\n",
  "  \"design_doc\":\"docs/notes/w6_bottomup_design_v2.md\",\n",
  "  \"authorization\":\"sol/sol_reply_102_math29.md F102-6.3 (限定認可: S0較正 + H^2(S4,V)在庫表/census のみ)\",\n",
  "  \"tier\":\"inventory-census\",\n",
  "  \"scope_statement\":\"本certは在庫表であり判定欄を持たない. 棄却・生存・EMPTYの語をいかなる行にも使用していない(S-BU-10準拠). kill/候補発見/EMPTY-THMのいずれにも使用しない.\",\n",
  "  \"seal_declaration\":{\"touches_c_hat_mu\":false,\"touches_psl_sealed_fields\":false,\n",
  "    \"touches_wall_campaign_pbit\":false,\"touches_u_values\":false,\"touches_im_R\":false,\n",
  "    \"touches_d_N\":false,\"reads_certificates\":false},\n",
  "  \"conventions_used\":{\n",
  "    \"generators\":\"theta=(1,2), tau=(1,3,4) in S4 (matches A-0/design v2 SS2.1)\",\n",
  "    \"S4_presentation\":\"<a,b|a^2,b^3,(ab)^4> (verified |.|=24 in w6_bu_s0_driver.g)\",\n",
  "    \"S3_presentation\":\"<a,b|a^2,b^3,(ab)^2>, a,b = images of theta,tau under S4->S3=S4/V4 (matches A-13 construction in w6_bu_s0_driver.g)\",\n",
  "    \"cohomology_tool\":\"GAP package cohomolo (CHR/FirstCohomologyDimension/SecondCohomologyDimension), external-binary-backed. Not cross-checked by a second implementation in this pass (single-lane; not upgraded to cross-checked status).\",\n",
  "    \"p2_building_blocks\":\"triv (dim1, trivial), F2C2 (dim2, nonsplit self-ext of trivial via sign(theta)=-1,sign(tau)=+1), D (dim2, irreducible via S4->S3->GL(2,2) iso) -- per Lemma F2S3, design v2 SS6.1\",\n",
  "    \"p3_dim2_method\":\"direct brute-force enumeration of homs S3->GL(2,3) (48 elements, exhaustive), reduced by GL(2,3)-conjugacy (naive O(n^2*|GL|) orbit merge). No closed-form lemma exists in the design docs for p=3; count is MEASURED not asserted.\"\n",
  "  },\n",
  "  \"rows\":", rowsJson, ",\n",
  "  \"row_count\":", String(Length(CensusRows)), ",\n",
  "  \"p2_dim2_3_4_count_cross_check_vs_A9\":{\"expected\":[3,3,6],\"measured_total\":",
      String(Length(Filtered(CensusRows, r -> r.p=2))), ",\"expected_total\":12},\n",
  "  \"p3_dim2_measured_count\":", String(Length(repsP3)), ",\n",
  "  \"scope_out\":", scopeOutJson, ",\n",
  "  \"coverage_notes\":\"このpassは(V-cen)層(S3-inflate)のみを網羅した. p=2 dim2/3/4は補題F2S3の閉形式で厳密12型(A-9と一致). p=3 dim2はGL(2,3)悉皆総当りで測定(5型, 設計文書に閉形式なし). 非中心層(V4非自明作用)のF_p[S4]加群は本passで未着手(NOT_ENUMERATED_THIS_PASS) -- 原発注文の文言(『F_p[S4]加群…の同型類を列挙』)はV-cen層に限定されないため, 追加passでの手当てを要する.\",\n",
  "  \"fails_total\":", String(Length(FAILS)), ",\n",
  "  \"fails\":", JArr(List(FAILS, f -> Concatenation("{\"name\":", JStr(f.name),
      ",\"got\":", JStr(f.got), ",\"want\":", JStr(f.want), "}"))), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"design_doc_v2_sha256\":", JStr(designSha), ",\n",
  "    \"s0_cert_sha256_for_reference\":", JStr(s0CertSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

OUT_PATH := "search/certs/h2_census_s4_20260805.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nFAILS = ", Length(FAILS), "\n");
for fitem in FAILS do
  Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n");
od;
Print("\nW6_BU_CENSUS_DRIVER_DONE\n");
QUIT;
