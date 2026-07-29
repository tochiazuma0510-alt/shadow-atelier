#############################################################################
## search/strike-i10-1.g -- I10-1 discriminating-window driver (2 windows,
## all N_ord=5 system). 裁定218 承認済み。
##
## 仕様書: search/_i10_1_driver_spec.md (これが正本・完結仕様)。
## 接触遮断: docs/notes/i10_1_prediction_v1.md と ideas/ は本 driver からは
## 一切 Read しない(実装担当への指示どおり)。期待値・比較対象はコードに
## 書かない -- 例外は仕様書に明記された3点のみ:
##   (1) 2 窓の canonical-id SHA-256 (fail-closed 照合、初回のみ)
##   (2) Xi-restricted 走査の fail-closed 上界 (窓ごとの表値)
##   (3) 欄19(naive digest) = 欄20(xi digest) の較正ゲート (W-E-A10-5x2t0 のみ)
## それ以外はすべて生の測定値として記録するだけで、解釈も期待値比較もしない。
##
## 骨格: search/strike-a13-ladder.g (StageAssert / 証明書パターン)。
## canonical 文字列書式は A13 梯子と異なる(|ell=|r= が入る -- 仕様書 注意)。
##
## *** 実装上の必須注意(仕様書より): 両窓とも epsilon=1 (a1 奇置換) のファイバ
## 積である。E = S3 x_{C2} Sn (subset of S3 x Sn, sign(z)=sign(sigma)) であり、
## E = DirectProduct(S3,Sn) との比較 assert は書かない。代わりに:
##   1. Size(E) = 6*|A_n|
##   2. Size(P) = |A_n|, P = Kernel(E -> S3)
##   3. E = Group(a1*(n+1,n+3), b1*(n+1,n+3,n+2)) (degree n+3 permutation group)
## を実装する。BuildS1S2E は search/strike-a13-ladder.g の BuildS1S2 と同じ
## DirectProduct(SymmetricGroup(n), SymmetricGroup(3)) 構成を使う(GAP の
## DirectProduct(埋め込み) は第2因子の点を n だけシフトするため、
## Image(embS,(1,3)) = (n+1,n+3) / Image(embS,(1,3,2)) = (n+1,n+3,n+2) と一致し、
## agen = a1*(n+1,n+3) / bgen = b1*(n+1,n+3,n+2) が文字どおり成立する -- 局所で
## 確認済み)。
##
## judge: search/kerchi-judge.g v1.3 の Xi-restricted 実装 (MakeWindow /
## CorrectedShadowsLegacy / CorrectedShadowsXi / GroupOfShadows) を
## JUDGE_LIBRARY_ONLY モードで再利用。JUDGE_SKIP_LEGACY_CROSSCHECK := true.
##
## Output: search/certs/i10_1_<JUDGE_ID>_20260730.json x2
##         + search/certs/i10_1_manifest_20260730.json
#############################################################################

Read("search/gaplib_common.g");
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

PrintStr := function(x)
  local s, ss;
  ss := "";;
  s := OutputTextString(ss, true);;
  SetPrintFormattingStatus(s, false);;
  PrintTo(s, x);;
  CloseStream(s);;
  return ss;
end;;

Sha256OfString := function(str)
  local tmp, f, line;
  tmp := "search/certs/.i10_1_sha_tmp.txt";
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, str);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", tmp, ".out\""));
  f := InputTextFile(Concatenation(tmp, ".out"));
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", tmp, ".out\""));
  return line{[1..64]};
end;;

CertSha256File := function(path)
  local tmp, f, line;
  tmp := "search/certs/.i10_1_sha_tmp2.txt";
  Exec(Concatenation("sha256sum \"", path, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1..64]};
end;;

# canonical string format per _i10_1_driver_spec.md (NOTE: differs from A13
# ladder's format -- |ell=|r= are inserted):
#   <ID>|n=<n>|ell=<ell>|r=<r>|t=<t>|a1=<perm>|b1=<perm>|S1=<perm>|S2=<perm>
CanonicalString := function(id, n, ell, r, t, a1, b1, s1, s2)
  return Concatenation(id, "|n=", String(n), "|ell=", String(ell), "|r=", String(r),
    "|t=", String(t), "|a1=", PrintStr(a1), "|b1=", PrintStr(b1),
    "|S1=", PrintStr(s1), "|S2=", PrintStr(s2));
end;;

# canonical-id SHA-256 table -- fail-closed identity check (spec's exception (1))
CANONICAL_SHA_TABLE := rec(
  W_E_A10_5x2t0 := "5848b4bffe7878f048a34379cd4042d1efbed1df6596aa0b5106694f46589df4",
  W_E_A15_5x3t0 := "47d73376614720d4cc4b14bdbbc83ef77ba984b71bd2100fcaf9709f59fe26f0"
);;

# Xi-restricted fail-closed scan upper bounds (spec's exception (2))
XI_BOUND_TABLE := rec(
  W_E_A10_5x2t0 := 5000,
  W_E_A15_5x3t0 := 1125000
);;

#############################################################################
## ---------------------- window table (machine-transcribed from the spec) --
#############################################################################
WINDOWS := [
  rec(id := "W-E-A10-5x2t0", n := 10, ell := 5, r := 2, t := 0,
      a1 := ( 1, 2)( 3, 6)( 7,10),
      b1 := ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12),
      s2lit := ( 1, 6, 4, 5, 3,10, 8, 9, 7, 2)(12,13),
      shaKey := "W_E_A10_5x2t0", hasCalibrationGate := true),
  rec(id := "W-E-A15-5x3t0", n := 15, ell := 5, r := 3, t := 0,
      a1 := ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
      b1 := ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15)(16,17),
      s2lit := ( 1, 9,15,13,11, 5,10, 4, 2, 3)( 6, 8,12, 7,14)(17,18),
      shaKey := "W_E_A15_5x3t0", hasCalibrationGate := false),
];;

#############################################################################
## ---------------------- window construction (Prop 0.3, SymmetricGroup(n)) -
#############################################################################
BuildS1S2E := function(a1, b1, n)
  local Sn, S3, Dgrp, embA, embS, agen, bgen, s1, s2, E;
  Sn := SymmetricGroup(n);;  S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(Sn, S3);;
  embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  s1 := bgen^-1 * agen;;
  s2 := agen^-1 * bgen^2;;
  E := Group(agen, bgen);;
  return rec(s1 := s1, s2 := s2, Dgrp := Dgrp, agen := agen, bgen := bgen, E := E);
end;;

#############################################################################
## ---------------------- per-window structural asserts (16-item style,
##   search/strike-a18.g convention) -----------------------------------------
#############################################################################
ProcessWindowStage1 := function(w)
  local asserts, StageAssert, ok, built, s1, s2, W, canon, sha, AN, pr2, PE;
  asserts := [];;
  StageAssert := function(label, val)
    Add(asserts, rec(label := label, ok := val));
    Print("  [", PF(val), "] ", label, "\n");
    return val;
  end;;
  ok := true;;

  built := BuildS1S2E(w.a1, w.b1, w.n);;
  s1 := built.s1;;  s2 := built.s2;;

  ok := StageAssert("a1^2=1 and b1^3=1", w.a1^2 = () and w.b1^3 = ()) and ok;
  ok := StageAssert("braid relation s1*s2*s1 = s2*s1*s2", s1*s2*s1 = s2*s1*s2) and ok;
  ok := StageAssert("computed s1 (from a1,b1 via Prop 0.3, SymmetricGroup(n) realization) = literal JUDGE_S1_IMG (spec)",
                     s1 = w.s1lit) and ok;
  ok := StageAssert("computed s2 (from a1,b1 via Prop 0.3) = literal JUDGE_S2_IMG (spec)",
                     s2 = w.s2lit) and ok;

  # canonical-id SHA-256 fail-closed identity check (spec's exception (1))
  canon := CanonicalString(w.id, w.n, w.ell, w.r, w.t, w.a1, w.b1, s1, s2);;
  sha := Sha256OfString(canon);;
  Print("  canonical_string = ", canon, "\n");
  Print("  canonical_id_sha256 = ", sha, "\n");
  ok := StageAssert(Concatenation("canonical-id SHA-256 matches spec table (fail-closed identity check, window ", w.id, ")"),
                     sha = CANONICAL_SHA_TABLE.(w.shaKey)) and ok;

  W := MakeWindow(s1, s2);;
  ok := StageAssert("c=(s1*s2)^3 = identity (c in N)", W.c = Identity(W.Bq)) and ok;
  ok := StageAssert("ord(cbar) = 1 (c=id, restated)", Order(W.c) = 1) and ok;
  ok := StageAssert("ord(xbar) = 5", Order(W.x) = 5) and ok;
  ok := StageAssert("ord(ybar) = 5", Order(W.y) = 5) and ok;
  ok := StageAssert("N_ord = lcm(5,5,1) = 5", W.Nord = 5) and ok;

  # ---- epsilon=1 fiber-product asserts (spec's "実装上の必須注意", 3 items) ----
  AN := AlternatingGroup(w.n);;
  ok := StageAssert(Concatenation("Size(E) = 6*|A", String(w.n), "| = ",
                       String(6 * Size(AN))),
                     Size(built.E) = 6 * Size(AN)) and ok;
  pr2 := Projection(built.Dgrp, 2);;
  PE := Intersection(built.E, Kernel(pr2));;
  ok := StageAssert(Concatenation("Size(P) = |A", String(w.n), "| (P := Kernel(E -> S3))"),
                     Size(PE) = Size(AN)) and ok;
  ok := StageAssert("P (=<s1^2,s2^2>) = Kernel(E -> S3) (structural equality, epsilon=1 fiber-product realization)",
                     Group(s1^2, s2^2) = PE) and ok;
  ok := StageAssert("E = Group(a1*(n+1,n+3), b1*(n+1,n+3,n+2)) (degree n+3 permutation group construction check)",
                     Group(built.agen, built.bgen) = built.E) and ok;

  return rec(ok := ok, asserts := asserts, W := W, s1 := s1, s2 := s2, built := built,
             AN := AN, PE := PE, canonical_string := canon, canonical_id_sha256 := sha);
end;;

#############################################################################
## ---------------------- enriched measurement (spec fields 0-18(/19-21)) ---
#############################################################################
MeasureWindow := function(w, st, corr, xiRes)
  local W, gi, G, K, Q, oddp, A, S, natGK, QInv, chiImgOrd, CGA, faithful,
        Kidgrp, Kidgrp_note, Kdp, AidgrpJson, idG, dlG, dseries, normXbar,
        normXbarOrd, gDividesNorm, oddNormals, maxOdd, N1;
  W := st.W;;
  gi := GroupOfShadows(W, corr);;
  if not gi.closed then
    Error("strike-i10-1.g: (3.53) closure FAILED for window ", w.id,
          " -- refusing to report structure of a group not confirmed to exist");
  fi;
  G := gi.G;;  K := gi.ker;;

  # ---- 1,2: group_order / ker_size ----
  Print("  group_order=", Size(G), "  ker_size=", Size(K), "\n");

  # ---- 3,4,5: ker odd/2 part ----
  oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;

  # ---- A := O_{2'}(K) = the (unique, characteristic) largest odd-order
  # normal subgroup of K, per the spec's own suggested method: enumerate
  # normal subgroups of odd order and take the largest. ----
  oddNormals := Filtered(NormalSubgroups(K), N1 -> Size(N1) mod 2 = 1);;
  if Length(oddNormals) > 0 then
    maxOdd := Maximum(List(oddNormals, Size));;
    A := First(oddNormals, N1 -> Size(N1) = maxOdd);;
  else
    A := TrivialSubgroup(K);;
  fi;
  S := SylowSubgroup(K, 2);;
  Print("  ker_odd_part_order(=|A|)=", Size(A), "  ker_2_part_order(=|S|)=", Size(S),
        "  ker_odd_part_primes=", oddp, "\n");

  # ---- 6,6b: K_struct / K_idgroup ----
  Kidgrp := fail;;  Kidgrp_note := "";;
  if Size(K) > 0 and SmallGroupsAvailable(Size(K)) then
    Kidgrp := IdGroup(K);;
  else
    Kidgrp_note := "out-of-range";;
  fi;

  # ---- 7,7b: K_is_abelian / K_is_direct_product (K = A x S internally?) ----
  Kdp := (Size(A) * Size(S) = Size(K)) and IsTrivial(Intersection(A, S))
         and IsTrivial(CommutatorSubgroup(A, S));;
  Print("  K_struct=", StructureDescription(K), "  K_is_abelian=", IsAbelian(K),
        "  K_is_direct_product=", Kdp, "\n");

  # ---- 8,8b,8c: A_order / A_derived_order / A_idgroup ----
  Print("  A_order=", Size(A), "  A_derived_order=", Size(DerivedSubgroup(A)), "\n");

  # ---- 9,10: chi_image_order / Q_struct (invariant factors) ----
  natGK := NaturalHomomorphismByNormalSubgroup(G, K);;
  Q := Image(natGK);;
  chiImgOrd := Size(Q);;
  QInv := AbelianInvariants(Q);;
  Print("  chi_image_order(=|Q|)=", chiImgOrd, "  Q_struct(invariant_factors)=", QInv, "\n");

  # ---- 11: Q_action_faithful_on_A (G -> Aut(A) via conjugation, kernel =? K) ----
  CGA := Centralizer(G, A);;
  faithful := (Size(CGA) = Size(K));;
  Print("  Q_action_faithful_on_A (|C_G(A)|=|K|)? ", faithful,
        "  (|C_G(A)|=", Size(CGA), ", K subset C_G(A)? ", IsSubset(CGA, K), ")\n");

  # ---- 12: gtsh_idgroup ----
  idG := fail;;
  if SmallGroupsAvailable(Size(G)) then
    idG := Concatenation("{\"idgroup\":", JPair(IdGroup(G)[1], IdGroup(G)[2]), "}");;
  else
    idG := Concatenation("{\"structure_description\":", JStr(StructureDescription(G)),
      ",\"derived_series_orders\":", JArr(List(DerivedSeries(G), s -> String(Size(s)))),
      ",\"center_order\":", String(Size(Center(G))),
      ",\"sylow_structs\":", JArr(List(PrimeDivisors(Size(G)),
        p -> Concatenation("{\"p\":", String(p), ",\"struct\":",
          JStr(StructureDescription(SylowSubgroup(G, p))), "}"))), "}");;
  fi;
  Print("  gtsh_idgroup=", idG, "\n");

  # ---- 13,14: derived_length_G / derived_series_G ----
  if IsSolvable(G) then
    dlG := DerivedLength(G);;
  else
    dlG := -1;;   # sentinel: not solvable, dl undefined (kerchi-judge convention)
  fi;
  dseries := DerivedSeries(G);;
  Print("  derived_length_G=", dlG, "  derived_series_G(orders)=", List(dseries, Size), "\n");

  # ---- 15,16: xbar_normalizer_order / gorder_divides_norm ----
  normXbar := Normalizer(SymmetricGroup(w.n), Group(W.x));;
  normXbarOrd := Size(normXbar);;
  gDividesNorm := (normXbarOrd mod Size(G) = 0);;
  Print("  xbar_normalizer_order=", normXbarOrd,
        "  gorder_divides_norm (group_order | xbar_normalizer_order)=", gDividesNorm, "\n");

  # ---- 17,18: xi_count_measured / xi_count_bound ----
  Print("  xi_count_measured=", xiRes.scanned_count, "  xi_count_bound=",
        XI_BOUND_TABLE.(w.shaKey), "\n");

  AidgrpJson := "";;
  if SmallGroupsAvailable(Size(A)) then
    AidgrpJson := Concatenation("{\"idgroup\":", JPair(IdGroup(A)[1], IdGroup(A)[2]), "}");;
  else
    AidgrpJson := Concatenation("{\"structure_description\":", JStr(StructureDescription(A)), "}");;
  fi;

  return rec(
    group_order := Size(G), ker_size := Size(K),
    ker_odd_part_order := Size(A), ker_2_part_order := Size(S),
    ker_odd_part_primes := oddp,
    K_struct := StructureDescription(K),
    K_idgroup := Kidgrp, K_idgroup_note := Kidgrp_note,
    K_is_abelian := IsAbelian(K), K_is_direct_product := Kdp,
    A_order := Size(A), A_derived_order := Size(DerivedSubgroup(A)),
    A_idgroup_json := AidgrpJson,
    chi_image_order := chiImgOrd, Q_struct := QInv,
    Q_action_faithful_on_A := faithful,
    gtsh_idgroup := idG,
    derived_length_G := dlG, derived_series_G := List(dseries, Size),
    xbar_normalizer_order := normXbarOrd, gorder_divides_norm := gDividesNorm,
    xi_count_measured := xiRes.scanned_count, xi_count_bound := XI_BOUND_TABLE.(w.shaKey)
  );
end;;

#############################################################################
## ---------------------- JSON writers ---------------------------------------
#############################################################################
AssertJson := function(a)
  return Concatenation("{\"label\":", JStr(a.label), ",\"ok\":", JB(a.ok), "}");
end;;

KIdgroupJson := function(meas)
  if meas.K_idgroup = fail then
    return Concatenation("null, \"6b_K_idgroup_note\": ", JStr(meas.K_idgroup_note));
  fi;
  return Concatenation(JPair(meas.K_idgroup[1], meas.K_idgroup[2]), ", \"6b_K_idgroup_note\": null");
end;;

WriteWindowCert := function(w, st, xiRes, meas, gateFields, outfile)
  local outParts, i;
  outParts := [];;
  Add(outParts, "{\n");
  Add(outParts, "  \"generated_by\": \"search/strike-i10-1.g\",\n");
  Add(outParts, "  \"note\": \"I10-1 discriminating-window driver measurement -- window per search/_i10_1_driver_spec.md; raw measurements only, no interpretation, no comparison to any prediction file (measurement-side isolation). NOT a ledger claim by itself.\",\n");
  Add(outParts, Concatenation("  \"window_id\": ", JStr(w.id), ",\n"));
  Add(outParts, Concatenation("  \"n\": ", String(w.n), ",\n"));
  Add(outParts, Concatenation("  \"ell\": ", String(w.ell), ",\n"));
  Add(outParts, Concatenation("  \"r\": ", String(w.r), ",\n"));
  Add(outParts, Concatenation("  \"t\": ", String(w.t), ",\n"));
  Add(outParts, Concatenation("  \"a1\": ", JStr(PrintStr(w.a1)), ",\n"));
  Add(outParts, Concatenation("  \"b1\": ", JStr(PrintStr(w.b1)), ",\n"));
  Add(outParts, Concatenation("  \"s1\": ", JStr(PrintStr(st.s1)), ",\n"));
  Add(outParts, Concatenation("  \"s2\": ", JStr(PrintStr(st.s2)), ",\n"));
  Add(outParts, Concatenation("  \"canonical_string\": ", JStr(st.canonical_string), ",\n"));
  Add(outParts, Concatenation("  \"canonical_id_sha256\": ", JStr(st.canonical_id_sha256), ",\n"));
  Add(outParts, Concatenation("  \"canonical_id_sha256_gate\": ", JStr(CANONICAL_SHA_TABLE.(w.shaKey)), ",\n"));
  Add(outParts, Concatenation("  \"stage1_all_pass\": ", JB(st.ok), ",\n"));
  Add(outParts, "  \"stage1_asserts\": [\n");
  for i in [1 .. Length(st.asserts)] do
    Add(outParts, Concatenation("    ", AssertJson(st.asserts[i])));
    if i < Length(st.asserts) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
  od;
  Add(outParts, "  ],\n");
  Add(outParts, Concatenation("  \"N_ord\": ", String(st.W.Nord), ",\n"));
  Add(outParts, Concatenation("  \"0_canonical_id\": ", JStr(w.id), ",\n"));
  Add(outParts, Concatenation("  \"1_group_order\": ", String(meas.group_order), ",\n"));
  Add(outParts, Concatenation("  \"2_ker_size\": ", String(meas.ker_size), ",\n"));
  Add(outParts, Concatenation("  \"3_ker_odd_part_order\": ", String(meas.ker_odd_part_order), ",\n"));
  Add(outParts, Concatenation("  \"4_ker_2_part_order\": ", String(meas.ker_2_part_order), ",\n"));
  Add(outParts, Concatenation("  \"5_ker_odd_part_primes\": ", JArr(List(meas.ker_odd_part_primes, String)), ",\n"));
  Add(outParts, Concatenation("  \"6_K_struct\": ", JStr(meas.K_struct), ",\n"));
  Add(outParts, Concatenation("  \"6b_K_idgroup\": ", KIdgroupJson(meas), ",\n"));
  Add(outParts, Concatenation("  \"7_K_is_abelian\": ", JB(meas.K_is_abelian), ",\n"));
  Add(outParts, Concatenation("  \"7b_K_is_direct_product\": ", JB(meas.K_is_direct_product), ",\n"));
  Add(outParts, Concatenation("  \"8_A_order\": ", String(meas.A_order), ",\n"));
  Add(outParts, Concatenation("  \"8b_A_derived_order\": ", String(meas.A_derived_order), ",\n"));
  Add(outParts, Concatenation("  \"8c_A_idgroup\": ", meas.A_idgroup_json, ",\n"));
  Add(outParts, Concatenation("  \"9_chi_image_order\": ", String(meas.chi_image_order), ",\n"));
  Add(outParts, Concatenation("  \"10_Q_struct_invariant_factors\": ", JArr(List(meas.Q_struct, String)), ",\n"));
  Add(outParts, Concatenation("  \"11_Q_action_faithful_on_A\": ", JB(meas.Q_action_faithful_on_A), ",\n"));
  Add(outParts, Concatenation("  \"12_gtsh_idgroup\": ", meas.gtsh_idgroup, ",\n"));
  Add(outParts, Concatenation("  \"13_derived_length_G\": ", String(meas.derived_length_G), ",\n"));
  Add(outParts, Concatenation("  \"14_derived_series_G\": ", JArr(List(meas.derived_series_G, String)), ",\n"));
  Add(outParts, Concatenation("  \"15_xbar_normalizer_order\": ", String(meas.xbar_normalizer_order), ",\n"));
  Add(outParts, Concatenation("  \"16_gorder_divides_norm\": ", JB(meas.gorder_divides_norm), ",\n"));
  Add(outParts, Concatenation("  \"17_xi_count_measured\": ", String(meas.xi_count_measured), ",\n"));
  Add(outParts, Concatenation("  \"18_xi_count_bound\": ", String(meas.xi_count_bound), ",\n"));
  if IsBound(gateFields.hasGate) and gateFields.hasGate then
    Add(outParts, Concatenation("  \"19_naive_shadow_digest\": ", JStr(gateFields.naiveDigest), ",\n"));
    Add(outParts, Concatenation("  \"20_xi_shadow_digest\": ", JStr(gateFields.xiDigest), ",\n"));
    Add(outParts, Concatenation("  \"19_eq_20\": ", JB(gateFields.naiveDigest = gateFields.xiDigest), ",\n"));
    Add(outParts, Concatenation("  \"21_naive_elapsed_sec\": ", String(gateFields.naiveElapsedSec), ",\n"));
    Add(outParts, Concatenation("  \"21_xi_elapsed_sec\": ", String(gateFields.xiElapsedSec), ",\n"));
    Add(outParts, Concatenation("  \"21_naive_shadow_total\": ", String(gateFields.naiveShadowTotal), ",\n"));
  fi;
  Add(outParts, Concatenation("  \"scan_mode\": ", JStr(xiRes.scan_mode), ",\n"));
  Add(outParts, Concatenation("  \"settled_fail_count\": ", String(xiRes.settled_fail_count), ",\n"));
  Add(outParts, Concatenation("  \"shadow_total\": ", String(Length(xiRes.shadows)), "\n"));
  Add(outParts, "}\n");
  WriteFile(outfile, Concatenation(outParts));
  Print("Wrote ", outfile, "\n");
end;;

#############################################################################
## ---------------------- main driver loop -----------------------------------
#############################################################################
I10_1_SMOKE_TEST := IsBound(I10_1_LOCAL_SMOKE_TEST) and I10_1_LOCAL_SMOKE_TEST = true;;

manifestEntries := [];;

for w in WINDOWS do
  Print("\n################################################################\n");
  Print("# window: ", w.id, " (n=", w.n, ", ell=", w.ell, ", r=", w.r, ", t=", w.t, ")\n");
  Print("################################################################\n");

  st := ProcessWindowStage1(w);;
  Print("STAGE 1 (", w.id, ") overall: ", PF(st.ok), "\n");
  if not st.ok then
    Error("strike-i10-1.g: STAGE 1 failed for window ", w.id,
          " -- fail-closed, refusing to proceed (per campaign policy)");
  fi;

  charmingSet := Filtered([0 .. st.W.Nord - 1], m -> Gcd(2*m+1, st.W.Nord) = 1);;
  Print("  charming_count = ", Length(charmingSet), " (expect phi(2*5)=4)\n");

  xiBound := XI_BOUND_TABLE.(w.shaKey);;
  gateFields := rec(hasGate := false);;

  if w.hasCalibrationGate and not I10_1_SMOKE_TEST then
    Print("\n=== calibration gate (", w.id, " only): naive vs Xi-restricted digest ===\n");
    t0 := GAPLIB_WallElapsedMs();;
    legacyRes := CorrectedShadowsLegacy(st.W, charmingSet);;
    t1 := GAPLIB_WallElapsedMs();;
    naiveElapsedSec := (t1 - t0) / 1000.0;;
    naiveDigestStr := JoinC(List(legacyRes.shadows, s -> PrintStr(s)), "\n");;
    naiveDigest := Sha256OfString(naiveDigestStr);;
    Print("  naive: shadow_total=", Length(legacyRes.shadows), " elapsed_sec=", naiveElapsedSec,
          " digest=", naiveDigest, "\n");

    t0 := GAPLIB_WallElapsedMs();;
    JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
    xiRes := CorrectedShadowsXi(st.W, charmingSet);;
    xiRes.scan_mode := "xi_restricted";;
    t1 := GAPLIB_WallElapsedMs();;
    xiElapsedSec := (t1 - t0) / 1000.0;;
    xiDigestStr := JoinC(List(xiRes.shadows, s -> PrintStr(s)), "\n");;
    xiDigest := Sha256OfString(xiDigestStr);;
    Print("  xi:    shadow_total=", Length(xiRes.shadows), " elapsed_sec=", xiElapsedSec,
          " digest=", xiDigest, "\n");

    Print("  [", PF(naiveDigest = xiDigest), "] 19 (naive digest) = 20 (xi digest)\n");
    if naiveDigest <> xiDigest then
      Error("strike-i10-1.g: CALIBRATION GATE FAILED -- naive_shadow_digest (19) != ",
            "xi_shadow_digest (20) for ", w.id, " -- fail-closed, refusing to process the ",
            "remaining window (spec: 欄19≠20なら即Error停止, second window not struck)");
    fi;

    gateFields := rec(hasGate := true,
                       naiveDigest := naiveDigest, xiDigest := xiDigest,
                       naiveElapsedSec := naiveElapsedSec, xiElapsedSec := xiElapsedSec,
                       naiveShadowTotal := Length(legacyRes.shadows));;
    corr := xiRes.shadows;;
  else
    if w.hasCalibrationGate and I10_1_SMOKE_TEST then
      Print("\n(I10_1_LOCAL_SMOKE_TEST set -- skipping naive/legacy calibration gate; ",
            "Xi-restricted path only, for syntax/JSON-shape smoke testing)\n");
    fi;
    JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
    xiRes := CorrectedShadowsXi(st.W, charmingSet);;
    xiRes.scan_mode := "xi_restricted";;
    corr := xiRes.shadows;;
  fi;

  Print("\n=== Xi-restricted scan (", w.id, "): scanned_count=", xiRes.scanned_count,
        " bound=", xiBound, " shadow_total=", Length(corr),
        " settled_fail_count=", xiRes.settled_fail_count, " ===\n");
  if xiRes.scanned_count > xiBound then
    Error("strike-i10-1.g: window ", w.id, ": xi_count_measured (",
          xiRes.scanned_count, ") EXCEEDS the fail-closed Xi upper bound (", xiBound,
          ") -- refusing to trust this scan");
  fi;

  meas := MeasureWindow(w, st, corr, xiRes);;

  outfile := Concatenation("search/certs/i10_1_",
    ReplacedString(w.id, "-", "_"), "_20260730.json");;
  WriteWindowCert(w, st, xiRes, meas, gateFields, outfile);;

  Add(manifestEntries, rec(id := w.id, outfile := outfile,
      canonical_id_sha256 := st.canonical_id_sha256,
      stage1_all_pass := st.ok,
      calibration_gate_pass := (not gateFields.hasGate) or (gateFields.naiveDigest = gateFields.xiDigest)));

  if w.hasCalibrationGate and I10_1_SMOKE_TEST then
    Print("\n(I10_1_LOCAL_SMOKE_TEST set -- stopping after window 1 by design)\n");
    break;
  fi;
od;

#############################################################################
## ---------------------- manifest -------------------------------------------
#############################################################################
manifestParts := [];;
Add(manifestParts, "{\n");
Add(manifestParts, "  \"generated_by\": \"search/strike-i10-1.g\",\n");
Add(manifestParts, "  \"note\": \"I10-1 driver manifest -- 2 windows per search/_i10_1_driver_spec.md. Raw measurement summary only.\",\n");
Add(manifestParts, Concatenation("  \"smoke_test\": ", JB(I10_1_SMOKE_TEST), ",\n"));
Add(manifestParts, Concatenation("  \"windows_processed\": ", String(Length(manifestEntries)), ",\n"));
Add(manifestParts, "  \"windows\": [\n");
for i in [1 .. Length(manifestEntries)] do
  e := manifestEntries[i];;
  Add(manifestParts, Concatenation("    {\"id\":", JStr(e.id), ",\"outfile\":", JStr(e.outfile),
    ",\"canonical_id_sha256\":", JStr(e.canonical_id_sha256),
    ",\"stage1_all_pass\":", JB(e.stage1_all_pass),
    ",\"calibration_gate_pass\":", JB(e.calibration_gate_pass),
    ",\"cert_sha256\":", JStr(CertSha256File(e.outfile)), "}"));
  if i < Length(manifestEntries) then Add(manifestParts, ",\n"); else Add(manifestParts, "\n"); fi;
od;
Add(manifestParts, "  ]\n");
Add(manifestParts, "}\n");
WriteFile("search/certs/i10_1_manifest_20260730.json", Concatenation(manifestParts));;
Print("\nWrote search/certs/i10_1_manifest_20260730.json\n");
Print("I10_1_DRIVER_DONE\n");
