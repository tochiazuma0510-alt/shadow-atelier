#############################################################################
## search/probe/w6_bu_census/w6_bu_census_p3ext_driver.g
## W6BU-CENSUS p=3 dim3/4 EXTENSION: H^2(S4,V) inventory/census table
## supplement (no verdict column). Commander order (2026-08-05, express
## commission "H2 census の p=3 dim3/4 拡張", within F102-6.3 limited
## authorization scope = census inventory only, no kill/no verdict).
##
## Design authority for the p=3 building blocks: docs/notes/
## w6_bottomup_design_v3.md SS7.2.1, Lemma F3S3 (candidate note in that doc):
## F3[S3] is a serial (Nakayama) algebra with exactly 2 simple modules
## (triv=1, sgn) and Cartan matrix [[2,1],[1,2]]; the 6 indecomposable
## F3[S3]-modules are: triv (dim1), sgn (dim1), U1="1|sgn" (dim2, nonsplit
## ext with submodule sgn / quotient triv), U2="sgn|1" (dim2, nonsplit ext
## with submodule triv / quotient sgn), P1=P(triv)="1|sgn|1" (dim3,
## uniserial projective cover of triv), P2=P(sgn)="sgn|1|sgn" (dim3,
## uniserial projective cover of sgn, = P1 tensored by sgn).
##
## PAPER PREDICTION (derived by the implementer from Lemma F3S3's complete
## indecomposable list via Krull-Schmidt, BEFORE running the enumeration
## below -- kept out of the enumeration code per task instruction "紙から
## 読める場合は予言としてコード外に控え、実列挙後に突合"):
##   dim=3: multisets of {triv,sgn,U1,U2,P1,P2} (dims 1,1,2,2,3,3) summing
##     to 3 =  4 (three dim-1's: (#triv,#sgn) in {(3,0),(2,1),(1,2),(0,3)})
##          +  4 (one dim-2 in {U1,U2} + one dim-1 in {triv,sgn})
##          +  2 (one dim-3 in {P1,P2})
##          = 10 TYPES (predicted).
##   dim=4: 5 (four dim-1's: (4,0),(3,1),(2,2),(1,3),(0,4))
##          + 3 (two dim-2's, multiset of {U1,U2} size 2: UU1,UU2,U1U2)
##          + 6 (one dim-2 [2 choices] + two dim-1's [3 splits])
##          + 4 (one dim-3 [2 choices] + one dim-1 [2 choices])
##          = 18 TYPES (predicted).
## The GAP enumeration below is independent of this hand count (it just
## nested-loops the 6 multiplicities and filters by weighted sum = dim);
## the cross-check row in the cert compares the two.
##
## Building-block matrices (theta=a, tau=b images) were hand-derived by the
## implementer solving the cocycle conditions for the S3 presentation
## <a,b|a^2,b^3,(ab)^2> (a=theta odd/sgn=-1, b=tau even/sgn=+1), verified
## by hand (a^2=I,b^3=I,(ab)^2=I for each of the 6 blocks) and re-verified
## computationally below (Chk calls) before use in any combination.
##
## Non-contact: Im R untouched, d_N unevaluated, 3 sealed quantities
## untouched, no certificate reading (only this pass's own design docs and
## the v1 census cert's path+sha256 are referenced, for supplement binding
## -- not read as mathematical input). No verdict/kill/survival/EMPTY word
## is written anywhere in this script or its output (S-BU-10 compliance).
## Scope: (V-cen) layer only (S3-inflated modules), matching v1's scope and
## SS7.3's warning against generalizing beyond the enumerated range --
## this cert states counts for p=3 dim in {3,4} ONLY, inherits v1's
## SCOPE_OUT table verbatim, and does not claim anything about dim>=5 or
## about the non-central layer.
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

## Abstract S3 (order 6), SAME generator convention as
## w6_bu_census_driver.g / w6_bu_s0_driver.g A-13 (theta,tau's own
## S3-quotient images as the two designated generators).
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
Chk("census-p3ext-pre: |Fq_S3|", Size(FqS3), 6);;
Chk("census-p3ext-pre: prodOrdS3", prodOrdS3, 2);;
Chk("census-p3ext-pre: sign(theta)=-1 (odd)", SignPerm(theta), -1);;
Chk("census-p3ext-pre: sign(tau)=+1 (even)", SignPerm(tau), 1);;

#############################################################################
## The 6 F3[S3] indecomposables (Lemma F3S3), given as integer-residue
## matrices for (a,b)=(theta,tau) images, converted to GF(3) below.
## Derivation (implementer, by hand, cocycle conditions -- see header):
##  triv: a=[1], b=[1]
##  sgn : a=[2](=-1), b=[1]
##  U1  : "1|sgn" (sub=sgn,quot=triv): a=[[1,0],[0,2]], b=[[1,1],[0,1]]
##  U2  : "sgn|1" (sub=triv,quot=sgn): a=[[2,0],[0,1]], b=[[1,1],[0,1]]
##  P1  : "1|sgn|1" = P(triv), uniserial dim3:
##        a=[[1,0,0],[0,2,0],[0,0,1]], b=[[1,0,0],[1,1,0],[2,1,1]]
##  P2  : "sgn|1|sgn" = P(sgn) = P1 tensor sgn (scalar-twist each entry by
##        sgn(g)): a=[[2,0,0],[0,1,0],[0,0,2]], b=[[1,0,0],[1,1,0],[2,1,1]]
##        (b-matrix unchanged since sgn(tau)=+1)
#############################################################################
ConvMat3 := function(L)
  return List(L, row -> List(row, function(x)
    if x = 0 then return Zero(GF(3));
    elif x = 1 then return Z(3)^0;
    elif x = 2 then return Z(3);
    else Error("ConvMat3: bad entry ", x);
    fi;
  end));
end;;

triv_a := ConvMat3([[1]]);;         triv_b := ConvMat3([[1]]);;
sgn_a  := ConvMat3([[2]]);;         sgn_b  := ConvMat3([[1]]);;
U1_a   := ConvMat3([[1,0],[0,2]]);; U1_b   := ConvMat3([[1,1],[0,1]]);;
U2_a   := ConvMat3([[2,0],[0,1]]);; U2_b   := ConvMat3([[1,1],[0,1]]);;
P1_a   := ConvMat3([[1,0,0],[0,2,0],[0,0,1]]);;
P1_b   := ConvMat3([[1,0,0],[1,1,0],[2,1,1]]);;
P2_a   := ConvMat3([[2,0,0],[0,1,0],[0,0,2]]);;
P2_b   := ConvMat3([[1,0,0],[1,1,0],[2,1,1]]);;

Blocks3 := [
  rec(label := "triv", dim := 1, a := triv_a, b := triv_b),
  rec(label := "sgn",  dim := 1, a := sgn_a,  b := sgn_b),
  rec(label := "U1",   dim := 2, a := U1_a,   b := U1_b),
  rec(label := "U2",   dim := 2, a := U2_a,   b := U2_b),
  rec(label := "P1",   dim := 3, a := P1_a,   b := P1_b),
  rec(label := "P2",   dim := 3, a := P2_a,   b := P2_b)
];;

Print("\n=== p=3 building-block self-checks (Lemma F3S3, 6 indecomposables) ===\n");
for blk in Blocks3 do
  Chk(Concatenation("block ", blk.label, ": a^2=I"),
      blk.a^2 = IdentityMat(blk.dim, GF(3)), true);;
  Chk(Concatenation("block ", blk.label, ": b^3=I"),
      blk.b^3 = IdentityMat(blk.dim, GF(3)), true);;
  Chk(Concatenation("block ", blk.label, ": (ab)^2=I"),
      (blk.a*blk.b)^2 = IdentityMat(blk.dim, GF(3)), true);;
od;

BlockDiagP := function(mats, p)
  local dim, res, offs, i, j, m;
  dim := Sum(mats, m -> Length(m));
  res := List([1..dim], i -> List([1..dim], j -> Zero(GF(p))));
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

## Enumerate all (n_triv,n_sgn,n_U1,n_U2,n_P1,n_P2) with
## n_triv + n_sgn + 2*n_U1 + 2*n_U2 + 3*n_P1 + 3*n_P2 = dim.
EnumerateMultiplicities := function(dim)
  local res, n1, n2, n3, n4, n5, n6, tot;
  res := [];
  for n1 in [0..dim] do
    for n2 in [0..dim] do
      for n3 in [0..dim] do
        for n4 in [0..dim] do
          for n5 in [0..dim] do
            for n6 in [0..dim] do
              tot := n1 + n2 + 2*n3 + 2*n4 + 3*n5 + 3*n6;
              if tot = dim then
                Add(res, [n1,n2,n3,n4,n5,n6]);
              fi;
            od;
          od;
        od;
      od;
    od;
  od;
  return res;
end;;

SocleStructureString := function(mult)
  local labels, parts, i;
  labels := ["triv","sgn","U1","U2","P1","P2"];
  parts := [];
  for i in [1..6] do
    if mult[i] > 0 then
      Add(parts, Concatenation(labels[i], "^", String(mult[i])));
    fi;
  od;
  if Length(parts) = 0 then return "0"; fi;
  return JoinC(parts, " + ");
end;;

ModuleIdString := function(dim, mult)
  local s, i, labels;
  labels := ["triv","sgn","U1","U2","P1","P2"];
  s := Concatenation("p3ext_d", String(dim));
  for i in [1..6] do
    s := Concatenation(s, "_", labels[i], String(mult[i]));
  od;
  return s;
end;;

CensusRowsP3Ext := [];;

Print("\n=== p=3 (V-cen layer), dim 3,4 EXTENSION ===\n");
for dim in [3,4] do
  combos := EnumerateMultiplicities(dim);;
  Print("  dim=", dim, ": ", Length(combos), " module types enumerated\n");
  for mult in combos do
    matsA := [];; matsB := [];;
    idx := 0;;
    for blk in Blocks3 do
      idx := idx + 1;
      for i in [1..mult[idx]] do
        Add(matsA, blk.a); Add(matsB, blk.b);
      od;
    od;
    ma := BlockDiagP(matsA, 3);; mb := BlockDiagP(matsB, 3);;
    Chk(Concatenation("well-defined: a^2=I dim=",String(dim)," mult=",String(mult)),
        ma^2 = IdentityMat(dim,GF(3)), true);;
    Chk(Concatenation("well-defined: b^3=I dim=",String(dim)," mult=",String(mult)),
        mb^3 = IdentityMat(dim,GF(3)), true);;
    Chk(Concatenation("well-defined: (ab)^4=I dim=",String(dim)," mult=",String(mult)),
        (ma*mb)^4 = IdentityMat(dim,GF(3)), true);;
    chr := CHR(S4grp, 3, FqS4, [ma, mb]);;
    h1 := FirstCohomologyDimension(chr);;
    h2 := SecondCohomologyDimension(chr);;
    chrS3 := CHR(S3permGrp2, 3, FqS3, [ma, mb]);;
    h2s3 := SecondCohomologyDimension(chrS3);;
    Print("  p=3 dim=",dim," mult=",mult,"  H1(S4)=",h1," H2(S4)=",h2," H2(S3)=",h2s3,"\n");
    Add(CensusRowsP3Ext, rec(
      module_id := ModuleIdString(dim, mult),
      p := 3, dim := dim,
      s3_inflated := true,
      socle_structure := SocleStructureString(mult),
      dim_H2_S4 := h2, dim_H2_S3 := h2s3, dim_H1_S4 := h1,
      window_order := 500*3^dim,
      band_note := Concatenation("p3_dim", String(dim), "_window", String(500*3^dim), "_informational_only"),
      scope_out_reason := "n/a (within census extension order 2026-08-05; not BU-GAP-1)"
    ));;
  od;
od;

countDim3 := Length(Filtered(CensusRowsP3Ext, r -> r.dim = 3));;
countDim4 := Length(Filtered(CensusRowsP3Ext, r -> r.dim = 4));;
Chk("census-p3ext: p=3 dim=3 type count vs paper prediction (Lemma F3S3, 10)", countDim3, 10);;
Chk("census-p3ext: p=3 dim=4 type count vs paper prediction (Lemma F3S3, 18)", countDim4, 18);;

vcenFlaggedCount := Length(Filtered(CensusRowsP3Ext, r -> r.s3_inflated = true));;
Chk("census-p3ext: all rows flagged s3_inflated=true (by construction)",
    vcenFlaggedCount, Length(CensusRowsP3Ext));;

#############################################################################
## ==== JSON output ====
#############################################################################
Print("\n=== writing cert ===\n");

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_w6bu_census_p3ext_selfsha.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  if line = fail or Length(line) < 64 then
    Error("ComputeSha256File: sha256sum did not return a hash line for ", relpath);
  fi;
  return line{[1 .. 64]};
end;;

selfSha := ComputeSha256File("search/probe/w6_bu_census/w6_bu_census_p3ext_driver.g");;
designSha := ComputeSha256File("docs/notes/w6_bottomup_design_v3.md");;
v1CertSha := ComputeSha256File("search/certs/h2_census_s4_20260805.json");;

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

rowsJson := JArr(List(CensusRowsP3Ext, RowJson));;

## SCOPE_OUT inherited verbatim from v1 cert (h2_census_s4_20260805.json),
## text re-typed here (not re-read/parsed from the cert -- no certificate
## reading per S-BU non-contact rule); the v1 cert is bound instead via
## the "supplements" path+sha256 field below (B v6 lesson: structural
## binding, not prose reference alone).
scopeOutJson := Concatenation(
  "[",
  "{\"category\":\"non_elementary_abelian_core (C4,C9,noncyclic)\",\"status\":\"SCOPE_OUT\",",
    "\"note\":\"【BU-GAP-1】明示的SCOPE_OUT. 空とは主張しない. v1宇宙は初等アーベル核のみを射程とする.\"},",
  "{\"category\":\"A_nontrivial (dim>=12 window)\",\"status\":\"SCOPE_OUT\",",
    "\"note\":\"補題A-TRIV系A-TRIV-1により空(dim<=11ではA自明が強制される)ことは示されているが, 本censusはdim<=4の範囲のみを走査し, dim>=12帯そのものは走査していない.\"},",
  "{\"category\":\"PSL roof\",\"status\":\"SCOPE_OUT\",",
    "\"note\":\"campaign X-4により宇宙から除外(掘らない, であって空ではない).\"},",
  "{\"category\":\"non-central F_p[S4]-modules (V4 acting nontrivially)\",\"status\":\"NOT_ENUMERATED_THIS_PASS\",",
    "\"note\":\"実装時間予算の制約により本passでは未着手(v1から継承). 本supplementもV-cen層(S3-inflate)のみを対象とする.\"},",
  "{\"category\":\"p=3 dim>=5 (V-cen layer)\",\"status\":\"NOT_ENUMERATED_THIS_PASS\",",
    "\"note\":\"本supplementはp=3のdim3/4のみを列挙した(委嘱範囲). dim>=5への一般化はしない(w6_bottomup_design_v3.md SS7.3の一般化禁止と同種の注意).\"}",
  "]");;

cert := Concatenation(
  "{\n",
  "  \"schema\":\"w6-bu-census-p3ext/v1\",\n",
  "  \"generated_by\":\"search/probe/w6_bu_census/w6_bu_census_p3ext_driver.g\",\n",
  "  \"card_label\":\"W6BU-CENSUS p=3 dim3/4 EXTENSION: H^2(S4,V) inventory table supplement (V-cen layer)\",\n",
  "  \"design_doc\":\"docs/notes/w6_bottomup_design_v3.md SS7.2.1 (Lemma F3S3)\",\n",
  "  \"authorization\":\"sol/sol_reply_102_math29.md F102-6.3 (限定認可: S0較正 + H^2(S4,V)在庫表/census のみ) -- 司令塔小委嘱2026-08-05「H2 census の p=3 dim3/4 拡張」でこの限定認可の範囲内として発注\",\n",
  "  \"tier\":\"inventory-census-supplement\",\n",
  "  \"scope_statement\":\"本certは在庫表の追補であり判定欄を持たない. 棄却・生存・EMPTYの語をいかなる行にも使用していない(S-BU-10準拠). kill/候補発見/EMPTY-THMのいずれにも使用しない. p=3のdim3/4のみを対象とし, dim>=5および非中心層には言及しない.\",\n",
  "  \"seal_declaration\":{\"touches_c_hat_mu\":false,\"touches_psl_sealed_fields\":false,\n",
  "    \"touches_wall_campaign_pbit\":false,\"touches_u_values\":false,\"touches_im_R\":false,\n",
  "    \"touches_d_N\":false,\"reads_certificates\":false},\n",
  "  \"supplements\":{\"path\":\"search/certs/h2_census_s4_20260805.json\",\"sha256\":", JStr(v1CertSha), "},\n",
  "  \"paper_prediction_cross_check\":{\n",
  "    \"source\":\"docs/notes/w6_bottomup_design_v3.md SS7.2.1 Lemma F3S3 (implementer's hand-derived Krull-Schmidt count from the 6-indecomposable list, computed BEFORE running the enumeration)\",\n",
  "    \"predicted_type_count_dim3\":10,\"measured_type_count_dim3\":", String(countDim3), ",\n",
  "    \"predicted_type_count_dim4\":18,\"measured_type_count_dim4\":", String(countDim4), ",\n",
  "    \"match_dim3\":", JB(countDim3 = 10), ",\"match_dim4\":", JB(countDim4 = 18), ",\n",
  "    \"caveat\":\"紙の予言とGAP列挙は同じ実装者による二段階(手計算->コード)であり, CV-9非当事者判読を経ていない. cross-checkedとは書かない(design v3 SS7.2.1と同じ規律) -- 「二系統の第1歩」までである.\"\n",
  "  },\n",
  "  \"conventions_used\":{\n",
  "    \"generators\":\"theta=(1,2), tau=(1,3,4) in S4 (matches A-0/design v2 SS2.1, v1 census cert)\",\n",
  "    \"S4_presentation\":\"<a,b|a^2,b^3,(ab)^4> (verified |.|=24 in w6_bu_s0_driver.g)\",\n",
  "    \"S3_presentation\":\"<a,b|a^2,b^3,(ab)^2>, a,b = images of theta,tau under S4->S3=S4/V4 (matches A-13/v1 census cert construction)\",\n",
  "    \"cohomology_tool\":\"GAP package cohomolo (CHR/FirstCohomologyDimension/SecondCohomologyDimension), external-binary-backed. Not cross-checked by a second implementation in this pass (single-lane; not upgraded to cross-checked status).\",\n",
  "    \"p3_building_blocks\":\"triv (dim1), sgn (dim1), U1='1|sgn' (dim2, nonsplit ext sub=sgn/quot=triv), U2='sgn|1' (dim2, nonsplit ext sub=triv/quot=sgn), P1=P(triv)='1|sgn|1' (dim3, uniserial), P2=P(sgn)='sgn|1|sgn' (dim3, uniserial, =P1 tensor sgn) -- per Lemma F3S3, design v3 SS7.2.1. Matrices hand-derived by the implementer solving the extension cocycle conditions for the S3 presentation, verified in-script (a^2=I,b^3=I,(ab)^2=I for each block) before use.\",\n",
  "    \"enumeration_method\":\"exhaustive nested loop over 6 nonneg multiplicities (one per block) bounded by [0..dim], filtered by weighted-sum=dim (weights = block dims); this is a CONSTRUCTIVE closed-form enumeration (not brute-force GL(dim,3)-conjugacy search, which would be infeasible for dim=4 since |GL(4,3)|=24261120). Differs from v1's p=3 dim=2 method (brute-force GL(2,3) search, done before Lemma F3S3 existed).\"\n",
  "  },\n",
  "  \"rows\":", rowsJson, ",\n",
  "  \"row_count\":", String(Length(CensusRowsP3Ext)), ",\n",
  "  \"scope_out\":", scopeOutJson, ",\n",
  "  \"coverage_notes\":\"本supplementは(V-cen)層(S3-inflate)のp=3, dim in {3,4}のみを網羅した. Lemma F3S3の6不可分解の閉形式による構成的列挙(悉皆・GL共役総当りではない). dim>=5および非中心層(V4非自明作用)は本passで未着手のまま(v1から継承・追加拡張なし).\",\n",
  "  \"fails_total\":", String(Length(FAILS)), ",\n",
  "  \"fails\":", JArr(List(FAILS, f -> Concatenation("{\"name\":", JStr(f.name),
      ",\"got\":", JStr(f.got), ",\"want\":", JStr(f.want), "}"))), ",\n",
  "  \"provenance\":{\n",
  "    \"gap_version\":", JStr(GAPInfo.Version), ",\n",
  "    \"script_sha256\":", JStr(selfSha), ",\n",
  "    \"design_doc_v3_sha256\":", JStr(designSha), ",\n",
  "    \"wall_ms_total\":", String(GAPLIB_WallElapsedMs()), "\n",
  "  }\n",
  "}\n");;

OUT_PATH := "search/certs/h2_census_s4_p3ext_20260805.json";;
WriteFile(OUT_PATH, cert);;
Print("Wrote ", OUT_PATH, "\n");
Print("\nFAILS = ", Length(FAILS), "\n");
for fitem in FAILS do
  Print("   ", fitem.name, " got=", fitem.got, " want=", fitem.want, "\n");
od;
Print("\nW6_BU_CENSUS_P3EXT_DRIVER_DONE\n");
QUIT;
