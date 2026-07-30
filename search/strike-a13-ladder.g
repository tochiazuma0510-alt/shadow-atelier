#############################################################################
## search/strike-a13-ladder.g -- W3-3 A13 梯子 driver (13 窓: canonical 4 +
## 兄弟 9, 全窓 N_ord=9 系)
##
## 仕様書: search/_a13_ladder_driver_spec.md (これが正本・完結仕様)。
## 接触遮断: docs/notes/a13_prediction_v1.md は本 driver からは一切 Read しな
## い(実装担当への指示どおり)。期待値・予言値はコードに書かない -- 例外は
## 仕様書に明記された 3 点のみ:
##   (1) 4 canonical 窓の canonical-id SHA-256 (fail-closed 照合、初回のみ)
##   (2) Xi-restricted 走査の fail-closed 上界 (窓系ごとの表値)
##   (3) 欄 26 (naive digest) = 欄 27 (xi digest) の較正ゲート (A10-9t1 のみ)
## それ以外はすべて生の測定値として記録するだけで、解釈も期待値比較もしない。
##
## 骨格: search/strike-a14.g (StageAssert パターン・stage 分離)
## 規約: search/strike-a18.g (16 項 assert 様式・転記一致 assert)
## judge: search/kerchi-judge.g v1.3 の Xi-restricted 実装
##        (MakeWindow / CorrectedShadowsLegacy / CorrectedShadowsXi /
##        GroupOfShadows) を JUDGE_LIBRARY_ONLY モードで再利用。
##        JUDGE_SKIP_LEGACY_CROSSCHECK := true (W-D-A16-11a CI-hang postmortem
##        に倣い、大きい P では crosscheck_vs_EnumerateReducedHexagon を最初
##        から無効化)。
##
## *** 構築上の発見(実装担当・接触遮断下での構造確認であり予言比較ではない):
## spec の a1 は windows によって奇置換のことがある (W-E-A11-9t2 / -A12-9t3 と
## その兄弟)。search/strike-a18.g / strike-a14.g の D-series driver が使う
## DirectProduct(AlternatingGroup(n), S3) 埋め込みは a1 が偶置換であることを
## 要求するため、奇置換の a1 では Embedding が "must be an element of
## Source(<map>)" で即死する。spec 自身が窓 assert 節で書いている
## 「|E|=6|A_n| または相応 (epsilon=1 系はファイバー積 -- |E| は機械で確認し
## 記録)」との整合を取り、代わりに DirectProduct(SymmetricGroup(n), S3) を
## 使う (a1 の偶奇を問わない)。4 canonical 窓すべてで、この構成による
## 計算済み s1/s2 が spec 記載の literal JUDGE_S1_IMG/JUDGE_S2_IMG と完全一致
## し、canonical-id SHA-256 も spec 記載の表値と完全一致することを局所で確認
## 済み (scratchpad/test_a13_all13.g, 本 commit には含めない使い捨て検証)。
## |P|=|A_n| (P := Group(s1^2,s2^2)) も両方式で一致するが、この realization
## では P は Kernel(pr2) と厳密には等しくない (Kernel(pr2) = S_n x 1 の方が
## 真に大きい) ので、旧 D-series driver の「P = Kernel(pr2)」等号 assert は
## 「P の位数 = |A_n|」+「P は Kernel(pr2) の部分群」に置き換えた。
##
## Output: search/certs/a13_ladder_<JUDGE_ID>_20260730.json x13
##         + search/certs/a13_ladder_manifest_20260730.json
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
  tmp := "search/certs/.a13_sha_tmp.txt";
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

CanonicalString := function(id, n, t, a1, b1, s1, s2)
  return Concatenation(id, "|n=", String(n), "|t=", String(t),
    "|a1=", PrintStr(a1), "|b1=", PrintStr(b1),
    "|S1=", PrintStr(s1), "|S2=", PrintStr(s2));
end;;

# canonical-id SHA-256 table -- fail-closed 同定情報 (仕様書に明記された例外(1))
CANONICAL_SHA_TABLE := rec(
  W_E_A10_9t1 := "6092f5f0bae86188d1f46ede81e1dad2aebbb097d6d3c9cae46229b67e853f4b",
  W_E_A11_9t2 := "ddc23c556d760adeab1dcdab24887719b5ab0a0b8e137fcea4b2df8077984649",
  W_E_A12_9t3 := "b127a9048c4659b74f5c2c9257e5e3dedfab66761b7ce3947195ef21c3749c79",
  W_E_A13_9t4 := "a11f207d3a6e31d118830ac94cad6fc2e9429582c49620efb52e8b268b7f941f"
);;

# Xi-restricted fail-closed 走査上界 (t 系ごと, 仕様書に明記された例外(2))
XI_BOUND_BY_T := rec( t1 := 486, t2 := 972, t3 := 8748, t4 := 139968 );;

#############################################################################
## ---------------------- window construction (Prop 0.3, SymmetricGroup(n)) -
#############################################################################
BuildS1S2 := function(a1, b1, n)
  local Sn, S3, Dgrp, embA, embS, agen, bgen, s1, s2;
  Sn := SymmetricGroup(n);;  S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(Sn, S3);;
  embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  s1 := bgen^-1 * agen;;
  s2 := agen^-1 * bgen^2;;
  return rec(s1 := s1, s2 := s2, Dgrp := Dgrp);
end;;

#############################################################################
## ---------------------- window table (machine-transcribed from the spec) --
#############################################################################
# canonical 4 (literal S1/S2 given -- transcription-consistency assert applies)
CANON := [
  rec(id := "W-E-A10-9t1", n := 10, t := 1,
      a1 := ( 1, 2)( 3, 5)( 4,10)( 6, 9),
      b1 := ( 2, 9, 5)( 3, 4,10)( 6, 8, 7),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(11,12),
      s2lit := ( 1, 5,10, 3, 9, 7, 8, 6, 2)(12,13),
      shaKey := "W_E_A10_9t1"),
  rec(id := "W-E-A11-9t2", n := 11, t := 2,
      a1 := ( 2,11)( 3, 8)( 4, 5)( 6, 7)( 9,10),
      b1 := ( 1, 9,11)( 2,10, 8)( 3, 7, 5),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(12,13),
      s2lit := ( 1,11, 8, 5, 4, 7, 6, 3,10)( 2, 9)(13,14),
      shaKey := "W_E_A11_9t2"),
  rec(id := "W-E-A12-9t3", n := 12, t := 3,
      a1 := ( 3, 9)( 4,11)( 5, 7)( 6,12)( 8,10),
      b1 := ( 1, 9, 2)( 3, 8,11)( 4,10, 7)( 5, 6,12),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(13,14),
      s2lit := ( 1, 2, 9,11, 7,12, 5,10, 3)( 4, 8)(14,15),
      shaKey := "W_E_A12_9t3"),
  rec(id := "W-E-A13-9t4", n := 13, t := 4,
      a1 := ( 2,10)( 3, 8)( 4,12)( 5, 6)( 7,13)( 9,11),
      b1 := ( 1, 9,10)( 2,11, 8)( 3, 7,12)( 4,13, 6),
      s1lit := ( 1, 2, 3, 4, 5, 6, 7, 8, 9)(10,11)(12,13)(14,15),
      s2lit := ( 1,10, 8,12, 6, 5,13, 3,11)( 2, 9)( 4, 7)(15,16),
      shaKey := "W_E_A13_9t4"),
];;

# w0 for each t-family = b1_canonical^-1 * a1_canonical (computed below, not
# hand-transcribed) -- used to build sibling b1 := a1_sibling * w0^-1.
W0_BY_T := rec();;
for cw in CANON do
  W0_BY_T.(Concatenation("t", String(cw.t))) := cw.b1^-1 * cw.a1;
od;;

# sibling 9 (a1 only; b1 derived; no literal S1/S2 -- recorded, not compared)
SIBS := [
  rec(id := "W-E-A10-9t1-o2", n := 10, t := 1, a1 := ( 3, 9)( 4, 6)( 5,10)( 7, 8)),
  rec(id := "W-E-A10-9t1-o3", n := 10, t := 1, a1 := ( 2, 3)( 4, 9)( 6, 8)( 7,10)),
  rec(id := "W-E-A10-9t1-o4", n := 10, t := 1, a1 := ( 2, 3)( 4, 9)( 5, 7)( 6,10)),
  rec(id := "W-E-A10-9t1-o5", n := 10, t := 1, a1 := ( 2, 4)( 3,10)( 5, 9)( 6, 7)),
  rec(id := "W-E-A10-9t1-o6", n := 10, t := 1, a1 := ( 2, 6)( 3, 4)( 7, 9)( 8,10)),
  rec(id := "W-E-A11-9t2-o2", n := 11, t := 2, a1 := ( 2, 3)( 4, 9)( 5,10)( 6, 7)( 8,11)),
  rec(id := "W-E-A11-9t2-o3", n := 11, t := 2, a1 := ( 2, 7)( 3,10)( 4, 5)( 6,11)( 8, 9)),
  rec(id := "W-E-A12-9t3-o2", n := 12, t := 3, a1 := ( 2, 4)( 3,12)( 5, 9)( 6,10)( 8,11)),
  rec(id := "W-E-A12-9t3-o3", n := 12, t := 3, a1 := ( 2, 6)( 3,10)( 5,11)( 7, 9)( 8,12)),
];;
for sw in SIBS do
  sw.b1 := sw.a1 * W0_BY_T.(Concatenation("t", String(sw.t)))^-1;
  sw.shaKey := fail;;  # no literal comparison for siblings (first appearance)
od;;

# processing order = spec document order: canonical 4 first (A10-9t1 first
# for the gate), then siblings in spec-listed order.
WINDOWS := Concatenation(CANON, SIBS);;

# v1 shard knob (mine/ 配車用・裁定237 v1範囲): LADDER_ONLY_WINDOWS が bound
# なら window ID でフィルタするだけ。判定ロジック・走査・cert 内容には無関係。
# 未 bound なら従来と完全同一動作 (13窓フル走)。
if IsBound(LADDER_ONLY_WINDOWS) then
  WINDOWS := Filtered(WINDOWS, w -> w.id in LADDER_ONLY_WINDOWS);;
fi;;

#############################################################################
## ---------------------- per-window structural asserts (16-item style,
##   search/strike-a18.g convention) -----------------------------------------
#############################################################################
ProcessWindowStage1 := function(w)
  local asserts, StageAssert, ok, S3n, Sn, Dgrp, built, s1, s2, W, charmingSet,
        PN, prKernelOk, canon, sha;
  asserts := [];;
  StageAssert := function(label, val)
    Add(asserts, rec(label := label, ok := val));
    Print("  [", PF(val), "] ", label, "\n");
    return val;
  end;;
  ok := true;;

  built := BuildS1S2(w.a1, w.b1, w.n);;
  s1 := built.s1;;  s2 := built.s2;;

  ok := StageAssert("a1^2=1 and b1^3=1", w.a1^2 = () and w.b1^3 = ()) and ok;
  ok := StageAssert("braid relation s1*s2*s1 = s2*s1*s2", s1*s2*s1 = s2*s1*s2) and ok;

  if IsBound(w.s1lit) then
    ok := StageAssert("computed s1 (from a1,b1 via Prop 0.3, SymmetricGroup(n) realization) = literal JUDGE_S1_IMG (spec)",
                       s1 = w.s1lit) and ok;
    ok := StageAssert("computed s2 (from a1,b1 via Prop 0.3) = literal JUDGE_S2_IMG (spec)",
                       s2 = w.s2lit) and ok;
  fi;

  W := MakeWindow(s1, s2);;
  ok := StageAssert("c in N (c = identity in Bq)", W.c = Identity(W.Bq)) and ok;
  ok := StageAssert("ord(c-bar) = 1 (c=id, restated)", Order(W.c) = 1) and ok;
  ok := StageAssert(Concatenation("|E|=[B3:N] = 6*|A", String(w.n), "| = ",
                       String(6 * Size(AlternatingGroup(w.n)))),
                     Size(W.Bq) = 6 * Size(AlternatingGroup(w.n))) and ok;
  PN := W.PN;;
  ok := StageAssert(Concatenation("|P| = |A", String(w.n), "|"),
                     Size(PN) = Size(AlternatingGroup(w.n))) and ok;
  prKernelOk := IsSubset(Kernel(Projection(built.Dgrp, 2)), PN);;
  ok := StageAssert("P subset of Kernel(pr_2) (fiber-product realization: P is a proper subgroup of Kernel(pr_2)=S_n, not equal)",
                     prKernelOk) and ok;
  ok := StageAssert("ord(xbar) = 9", Order(W.x) = 9) and ok;
  ok := StageAssert("ord(ybar) = 9", Order(W.y) = 9) and ok;
  ok := StageAssert("N_ord = lcm(9,9,1) = 9", W.Nord = 9) and ok;
  charmingSet := Filtered([0 .. W.Nord - 1], m -> Gcd(2*m+1, W.Nord) = 1);;
  ok := StageAssert("charming m count = phi(18) = 6", Length(charmingSet) = 6) and ok;

  canon := CanonicalString(w.id, w.n, w.t, w.a1, w.b1, s1, s2);;
  sha := Sha256OfString(canon);;
  Print("  canonical_string = ", canon, "\n");
  Print("  canonical_id_sha256 = ", sha, "\n");

  if w.shaKey <> fail then
    ok := StageAssert(Concatenation("canonical-id SHA-256 matches spec table (fail-closed identity check, window ", w.id, ")"),
                       sha = CANONICAL_SHA_TABLE.(w.shaKey)) and ok;
  fi;

  return rec(ok := ok, asserts := asserts, W := W, s1 := s1, s2 := s2,
             charmingSet := charmingSet, canonical_string := canon,
             canonical_id_sha256 := sha);
end;;

#############################################################################
## ---------------------- enriched measurement (spec fields 0-25) -----------
#############################################################################
MeasureWindow := function(w, st, corr)
  local W, gi, G, K, Q, oddp, A, S, Kdp, natGK, QstrDescr, QInv, chiImgOrd,
        CGA, faithful, Sstruct, ZSord, CGS, GoverCGS, InnSord, H3holds,
        complAll, complInCGS, epsZero, splitND, zInPhi, centralWit, idG,
        m0, u0, layerIdx, invCount, natCGSA, CGSmodA, S2q, zGen, zbar,
        regs, Kidgrp, Kidgrp_note, gtshIdField, i, cwGen, found, cw2, comm,
        AnormInCGS;
  W := st.W;;
  gi := GroupOfShadows(W, corr);;
  if not gi.closed then
    Error("strike-a13-ladder.g: (3.53) closure FAILED for window ", w.id,
          " -- refusing to report structure of a group not confirmed to exist");
  fi;
  G := gi.G;;  K := gi.ker;;  regs := gi.regs;;

  # ---- 1,2: group_order / ker_size ----
  Print("  group_order=", Size(G), "  ker_size=", Size(K), "\n");

  # ---- 3,4,5: ker odd/2 part ----
  oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
  if Length(oddp) > 0 then
    A := Subgroup(K, Concatenation(List(oddp, p -> GeneratorsOfGroup(SylowSubgroup(K, p)))));;
  else
    A := TrivialSubgroup(K);;
  fi;
  S := SylowSubgroup(K, 2);;
  Print("  ker_odd_part_order=", Size(A), "  ker_2_part_order=", Size(S),
        "  ker_odd_part_primes=", oddp, "\n");

  # ---- 6,6b: K_struct / K_idgroup ----
  Kidgrp := fail;;  Kidgrp_note := "";;
  if Size(K) > 0 and SmallGroupsAvailable(Size(K)) then
    Kidgrp := IdGroup(K);;
  else
    Kidgrp_note := "SmallGroupsAvailable(|K|) = false -- IdGroup not attempted, |K| out of library range";
  fi;

  # ---- 7: K_is_direct_product = K = A x S internally? ----
  Kdp := (Size(A) * Size(S) = Size(K)) and IsTrivial(Intersection(A, S))
         and IsTrivial(CommutatorSubgroup(A, S));;
  Print("  K_struct=", StructureDescription(K), "  K_is_direct_product=", Kdp, "\n");

  # ---- 8,9: chi_image_order / Q_struct (invariant factors) ----
  natGK := NaturalHomomorphismByNormalSubgroup(G, K);;
  Q := Image(natGK);;
  chiImgOrd := Size(Q);;
  QstrDescr := StructureDescription(Q);;
  QInv := AbelianInvariants(Q);;
  Print("  chi_image_order=", chiImgOrd, "  Q_struct(invariant_factors)=", QInv,
        "  (Q_struct_description=", QstrDescr, ")\n");

  # ---- 10: Q_action_faithful_on_A ----
  CGA := Centralizer(G, A);;
  faithful := (Size(CGA) = Size(K));;
  Print("  Q_action_faithful_on_A (|C_G(A)|=|K|)? ", faithful,
        "  (|C_G(A)|=", Size(CGA), ", K subset C_G(A)? ", IsSubset(CGA, K), ")\n");

  # ---- 13-17: Syl_2(K) = S centralizer/normalizer structure ----
  Sstruct := StructureDescription(S);;
  ZSord := Size(Center(S));;
  CGS := Centralizer(G, S);;
  GoverCGS := Size(G) / Size(CGS);;
  InnSord := Size(S) / Size(Center(S));;
  H3holds := (GoverCGS = InnSord);;
  Print("  S_struct=", Sstruct, "  ZS_order=", ZSord, "  G_over_CG_S=", GoverCGS,
        "  Inn_S_order=", InnSord, "  H3_holds=", H3holds, "\n");

  # ---- 18,19: complement class counts ----
  complAll := Length(ComplementClassesRepresentatives(G, K));;
  complInCGS := Length(ComplementClassesRepresentatives(CGS, Intersection(CGS, K)));;
  Print("  compl_classes_all=", complAll, "  compl_classes_in_CG_S=", complInCGS, "\n");

  # ---- 20,23: epsilon_zero / split_but_not_direct ----
  epsZero := (complInCGS > 0);;
  splitND := (complAll > 0) and (complInCGS = 0);;
  Print("  epsilon_zero=", epsZero, "  split_but_not_direct=", splitND, "\n");

  # ---- 21,22: z in Frattini(Syl_2(C_G(S)/A)) / central-product witness ----
  zInPhi := fail;;  centralWit := "null";;
  if Size(S) > 1 then
    AnormInCGS := IsNormal(CGS, A);;
    if AnormInCGS then
      natCGSA := NaturalHomomorphismByNormalSubgroup(CGS, A);;
      CGSmodA := Image(natCGSA);;
      S2q := SylowSubgroup(CGSmodA, 2);;
      zGen := First(GeneratorsOfGroup(Center(S)), g -> not IsOne(g));;
      if zGen = fail then zGen := Identity(S); fi;
      zbar := Image(natCGSA, zGen);;
      zInPhi := zbar in FrattiniSubgroup(S2q);;
      Print("  z_in_Frattini(Syl_2(C_G(S)/A))=", zInPhi,
            "  (Syl_2(C_G(S)/A) struct=", StructureDescription(S2q), ")\n");
      if not epsZero then
        found := false;;
        for cwGen in GeneratorsOfGroup(S2q) do
          if cwGen^2 = zbar then
            centralWit := Concatenation("{\"witness_type\":\"square\",\"generator\":",
              JStr(String(cwGen)), ",\"relation\":\"g^2=z\",\"g_order\":", String(Order(cwGen)), "}");
            found := true;;
            break;
          fi;
        od;
        if not found then
          for cwGen in GeneratorsOfGroup(S2q) do
            for cw2 in GeneratorsOfGroup(S2q) do
              comm := Comm(cwGen, cw2);;
              if comm = zbar then
                centralWit := Concatenation("{\"witness_type\":\"commutator\",\"generator1\":",
                  JStr(String(cwGen)), ",\"generator2\":", JStr(String(cw2)),
                  ",\"relation\":\"[g1,g2]=z\"}");
                found := true;;
                break;
              fi;
            od;
            if found then break; fi;
          od;
        fi;
        if not found then
          centralWit := Concatenation("{\"witness_type\":\"unresolved\",\"note\":\"z in Phi(Syl_2(C_G(S)/A)) confirmed (",
            String(zInPhi), ") but no single generator square or pairwise commutator equals z; explicit generator relation not resolved\"}");
        fi;
        Print("  central_product_witness=", centralWit, "\n");
      fi;
    else
      Print("  [NOTE] A not normal in C_G(S) -- z_in_Frattini / central_product_witness not evaluated for this window\n");
    fi;
  else
    Print("  S trivial (|S|=1) -- z_in_Frattini / central_product_witness not applicable\n");
  fi;

  # ---- 24: gtsh_idgroup ----
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

  # ---- 25: u_minus1_involutions ----
  # u = 2m+1 == -1 (mod N_ord=9)  <=>  m == 8 (mod 9) -- unique charming m.
  m0 := First([0 .. W.Nord - 1], m -> (2*m+1) mod W.Nord = (W.Nord - 1) mod W.Nord);;
  layerIdx := Filtered([1 .. Length(corr)], i -> corr[i][1] = m0);;
  invCount := 0;;
  if IsBound(CGS) then
    invCount := Number(layerIdx, i -> Order(regs[i]) = 2 and (regs[i] in CGS));;
  fi;
  Print("  u_minus1_involutions (m0=", m0, ", layer size=", Length(layerIdx), ")=", invCount, "\n");

  return rec(
    group_order := Size(G), ker_size := Size(K),
    ker_odd_part_order := Size(A), ker_2_part_order := Size(S),
    ker_odd_part_primes := oddp,
    K_struct := StructureDescription(K),
    K_idgroup := Kidgrp, K_idgroup_note := Kidgrp_note,
    K_is_direct_product := Kdp,
    chi_image_order := chiImgOrd, Q_struct := QInv, Q_struct_description := QstrDescr,
    Q_action_faithful_on_A := faithful,
    S_struct := Sstruct, ZS_order := ZSord, G_over_CG_S := GoverCGS,
    Inn_S_order := InnSord, H3_holds := H3holds,
    compl_classes_all := complAll, compl_classes_in_CG_S := complInCGS,
    epsilon_zero := epsZero, z_in_Frattini := zInPhi,
    central_product_witness := centralWit, split_but_not_direct := splitND,
    gtsh_idgroup := idG, u_minus1_involutions := invCount,
    m0_layer := m0
  );
end;;

#############################################################################
## ---------------------- JSON writers ---------------------------------------
#############################################################################
AssertJson := function(a)
  return Concatenation("{\"label\":", JStr(a.label), ",\"ok\":", JB(a.ok), "}");
end;;

BoolOrNull := function(v)
  if v = fail then return "null"; fi;
  return JB(v);
end;;

ShaGateJson := function(w)
  if w.shaKey = fail then return "null"; fi;
  return JStr(CANONICAL_SHA_TABLE.(w.shaKey));
end;;

KIdgroupJson := function(meas)
  if meas.K_idgroup = fail then
    return Concatenation("null, \"6b_K_idgroup_note\": ", JStr(meas.K_idgroup_note));
  fi;
  return JPair(meas.K_idgroup[1], meas.K_idgroup[2]);
end;;

WriteWindowCert := function(w, st, xiRes, meas, gateFields, outfile)
  local outParts, i;
  outParts := [];;
  Add(outParts, "{\n");
  Add(outParts, "  \"generated_by\": \"search/strike-a13-ladder.g\",\n");
  Add(outParts, "  \"note\": \"A13 ladder driver measurement -- window per search/_a13_ladder_driver_spec.md; raw measurements only, no interpretation, no comparison to any prediction file (measurement-side isolation). NOT a ledger claim by itself.\",\n");
  Add(outParts, Concatenation("  \"window_id\": ", JStr(w.id), ",\n"));
  Add(outParts, Concatenation("  \"n\": ", String(w.n), ",\n"));
  Add(outParts, Concatenation("  \"t\": ", String(w.t), ",\n"));
  Add(outParts, Concatenation("  \"is_canonical\": ", JB(IsBound(w.s1lit)), ",\n"));
  Add(outParts, Concatenation("  \"a1\": ", JStr(PrintStr(w.a1)), ",\n"));
  Add(outParts, Concatenation("  \"b1\": ", JStr(PrintStr(w.b1)), ",\n"));
  Add(outParts, Concatenation("  \"s1\": ", JStr(PrintStr(st.s1)), ",\n"));
  Add(outParts, Concatenation("  \"s2\": ", JStr(PrintStr(st.s2)), ",\n"));
  Add(outParts, Concatenation("  \"canonical_string\": ", JStr(st.canonical_string), ",\n"));
  Add(outParts, Concatenation("  \"canonical_id_sha256\": ", JStr(st.canonical_id_sha256), ",\n"));
  Add(outParts, Concatenation("  \"canonical_id_sha256_gate\": ", ShaGateJson(w), ",\n"));
  Add(outParts, Concatenation("  \"stage1_all_pass\": ", JB(st.ok), ",\n"));
  Add(outParts, "  \"stage1_asserts\": [\n");
  for i in [1 .. Length(st.asserts)] do
    Add(outParts, Concatenation("    ", AssertJson(st.asserts[i])));
    if i < Length(st.asserts) then Add(outParts, ",\n"); else Add(outParts, "\n"); fi;
  od;
  Add(outParts, "  ],\n");
  Add(outParts, Concatenation("  \"N_ord\": ", String(st.W.Nord), ",\n"));
  Add(outParts, Concatenation("  \"charming_count\": ", String(Length(st.charmingSet)), ",\n"));
  Add(outParts, Concatenation("  \"0_canonical_id\": ", JStr(w.id), ",\n"));
  Add(outParts, Concatenation("  \"1_group_order\": ", String(meas.group_order), ",\n"));
  Add(outParts, Concatenation("  \"2_ker_size\": ", String(meas.ker_size), ",\n"));
  Add(outParts, Concatenation("  \"3_ker_odd_part_order\": ", String(meas.ker_odd_part_order), ",\n"));
  Add(outParts, Concatenation("  \"4_ker_2_part_order\": ", String(meas.ker_2_part_order), ",\n"));
  Add(outParts, Concatenation("  \"5_ker_odd_part_primes\": ", JArr(List(meas.ker_odd_part_primes, String)), ",\n"));
  Add(outParts, Concatenation("  \"6_K_struct\": ", JStr(meas.K_struct), ",\n"));
  Add(outParts, Concatenation("  \"6b_K_idgroup\": ", KIdgroupJson(meas), ",\n"));
  Add(outParts, Concatenation("  \"7_K_is_direct_product\": ", JB(meas.K_is_direct_product), ",\n"));
  Add(outParts, Concatenation("  \"8_chi_image_order\": ", String(meas.chi_image_order), ",\n"));
  Add(outParts, Concatenation("  \"9_Q_struct_invariant_factors\": ", JArr(List(meas.Q_struct, String)), ",\n"));
  Add(outParts, Concatenation("  \"9_Q_struct_description\": ", JStr(meas.Q_struct_description), ",\n"));
  Add(outParts, Concatenation("  \"10_Q_action_faithful_on_A\": ", JB(meas.Q_action_faithful_on_A), ",\n"));
  Add(outParts, Concatenation("  \"11_xi_count_measured\": ", String(xiRes.scanned_count), ",\n"));
  Add(outParts, Concatenation("  \"12_xi_count_bound\": ", String(gateFields.xiBound), ",\n"));
  Add(outParts, Concatenation("  \"13_S_struct\": ", JStr(meas.S_struct), ",\n"));
  Add(outParts, Concatenation("  \"14_ZS_order\": ", String(meas.ZS_order), ",\n"));
  Add(outParts, Concatenation("  \"15_G_over_CG_S\": ", String(meas.G_over_CG_S), ",\n"));
  Add(outParts, Concatenation("  \"16_Inn_S_order\": ", String(meas.Inn_S_order), ",\n"));
  Add(outParts, Concatenation("  \"17_H3_holds\": ", JB(meas.H3_holds), ",\n"));
  Add(outParts, Concatenation("  \"18_compl_classes_all\": ", String(meas.compl_classes_all), ",\n"));
  Add(outParts, Concatenation("  \"19_compl_classes_in_CG_S\": ", String(meas.compl_classes_in_CG_S), ",\n"));
  Add(outParts, Concatenation("  \"20_epsilon_zero\": ", JB(meas.epsilon_zero), ",\n"));
  Add(outParts, Concatenation("  \"21_z_in_Frattini\": ", BoolOrNull(meas.z_in_Frattini), ",\n"));
  Add(outParts, Concatenation("  \"22_central_product_witness\": ", meas.central_product_witness, ",\n"));
  Add(outParts, Concatenation("  \"23_split_but_not_direct\": ", JB(meas.split_but_not_direct), ",\n"));
  Add(outParts, Concatenation("  \"24_gtsh_idgroup\": ", meas.gtsh_idgroup, ",\n"));
  Add(outParts, Concatenation("  \"25_u_minus1_involutions\": ", String(meas.u_minus1_involutions),
      " ,\"25_m0_layer\": ", String(meas.m0_layer), ",\n"));
  if IsBound(gateFields.hasGate) and gateFields.hasGate then
    Add(outParts, Concatenation("  \"26_naive_shadow_digest\": ", JStr(gateFields.naiveDigest), ",\n"));
    Add(outParts, Concatenation("  \"27_xi_shadow_digest\": ", JStr(gateFields.xiDigest), ",\n"));
    Add(outParts, Concatenation("  \"26_eq_27\": ", JB(gateFields.naiveDigest = gateFields.xiDigest), ",\n"));
    Add(outParts, Concatenation("  \"28_naive_elapsed_sec\": ", String(gateFields.naiveElapsedSec), ",\n"));
    Add(outParts, Concatenation("  \"28_xi_elapsed_sec\": ", String(gateFields.xiElapsedSec), ",\n"));
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
A13_SMOKE_TEST := IsBound(A13_LOCAL_SMOKE_TEST) and A13_LOCAL_SMOKE_TEST = true;;

manifestEntries := [];;
overallOk := true;;

for w in WINDOWS do
  Print("\n################################################################\n");
  Print("# window: ", w.id, " (n=", w.n, ", t=", w.t, ")\n");
  Print("################################################################\n");

  st := ProcessWindowStage1(w);;
  Print("STAGE 1 (", w.id, ") overall: ", PF(st.ok), "\n");
  if not st.ok then
    Error("strike-a13-ladder.g: STAGE 1 failed for window ", w.id,
          " -- fail-closed, refusing to proceed (per campaign policy)");
  fi;

  xiBound := XI_BOUND_BY_T.(Concatenation("t", String(w.t)));;
  gateFields := rec(xiBound := xiBound, hasGate := false);;

  if w.id = "W-E-A10-9t1" and not A13_SMOKE_TEST then
    Print("\n=== calibration gate (W-E-A10-9t1 only): naive vs Xi-restricted digest ===\n");
    t0 := GAPLIB_WallElapsedMs();;
    legacyRes := CorrectedShadowsLegacy(st.W, st.charmingSet);;
    t1 := GAPLIB_WallElapsedMs();;
    naiveElapsedSec := (t1 - t0) / 1000.0;;
    naiveDigestStr := JoinC(List(legacyRes.shadows, s -> PrintStr(s)), "\n");;
    naiveDigest := Sha256OfString(naiveDigestStr);;
    Print("  naive: shadow_total=", Length(legacyRes.shadows), " elapsed_sec=", naiveElapsedSec,
          " digest=", naiveDigest, "\n");

    t0 := GAPLIB_WallElapsedMs();;
    JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
    xiRes := CorrectedShadowsXi(st.W, st.charmingSet);;
    xiRes.scan_mode := "xi_restricted";;
    t1 := GAPLIB_WallElapsedMs();;
    xiElapsedSec := (t1 - t0) / 1000.0;;
    xiDigestStr := JoinC(List(xiRes.shadows, s -> PrintStr(s)), "\n");;
    xiDigest := Sha256OfString(xiDigestStr);;
    Print("  xi:    shadow_total=", Length(xiRes.shadows), " elapsed_sec=", xiElapsedSec,
          " digest=", xiDigest, "\n");

    Print("  [", PF(naiveDigest = xiDigest), "] 26 (naive digest) = 27 (xi digest)\n");
    if naiveDigest <> xiDigest then
      Error("strike-a13-ladder.g: CALIBRATION GATE FAILED -- naive_shadow_digest (26) != ",
            "xi_shadow_digest (27) for W-E-A10-9t1 -- fail-closed, refusing to process the ",
            "remaining 12 windows (spec: 欄26≠27なら即Error停止)");
    fi;

    gateFields := rec(xiBound := xiBound, hasGate := true,
                       naiveDigest := naiveDigest, xiDigest := xiDigest,
                       naiveElapsedSec := naiveElapsedSec, xiElapsedSec := xiElapsedSec);;
    corr := xiRes.shadows;;
  else
    if w.id = "W-E-A10-9t1" and A13_SMOKE_TEST then
      Print("\n(A13_LOCAL_SMOKE_TEST set -- skipping naive/legacy calibration gate; ",
            "Xi-restricted path only, for syntax/JSON-shape smoke testing)\n");
    fi;
    JUDGE_FORCE_SCAN_MODE := "xi_restricted";;
    xiRes := CorrectedShadowsXi(st.W, st.charmingSet);;
    xiRes.scan_mode := "xi_restricted";;
    corr := xiRes.shadows;;
  fi;

  Print("\n=== Xi-restricted scan (", w.id, "): scanned_count=", xiRes.scanned_count,
        " bound=", xiBound, " shadow_total=", Length(corr),
        " settled_fail_count=", xiRes.settled_fail_count, " ===\n");
  if xiRes.scanned_count > xiBound then
    Error("strike-a13-ladder.g: window ", w.id, ": xi_count_measured (",
          xiRes.scanned_count, ") EXCEEDS the fail-closed Xi upper bound (", xiBound,
          ") for its t-family -- refusing to trust this scan");
  fi;

  meas := MeasureWindow(w, st, corr);;

  outfile := Concatenation("search/certs/a13_ladder_",
    ReplacedString(w.id, "-", "_"), "_20260730.json");;
  WriteWindowCert(w, st, xiRes, meas, gateFields, outfile);;

  Add(manifestEntries, rec(id := w.id, outfile := outfile,
      canonical_id_sha256 := st.canonical_id_sha256,
      stage1_all_pass := st.ok, gate_pass := (not gateFields.hasGate) or (gateFields.naiveDigest = gateFields.xiDigest)));

  if w.id = "W-E-A10-9t1" and A13_SMOKE_TEST then
    Print("\n(A13_LOCAL_SMOKE_TEST set -- stopping after window 1 by design)\n");
    break;
  fi;
od;

#############################################################################
## ---------------------- manifest -------------------------------------------
#############################################################################
CertSha256File := function(path)
  local tmp, f, line;
  tmp := "search/certs/.a13_sha_tmp2.txt";
  Exec(Concatenation("sha256sum \"", path, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1..64]};
end;;

manifestParts := [];;
Add(manifestParts, "{\n");
Add(manifestParts, "  \"generated_by\": \"search/strike-a13-ladder.g\",\n");
Add(manifestParts, "  \"note\": \"A13 ladder manifest -- 13 windows per search/_a13_ladder_driver_spec.md. Raw measurement summary only.\",\n");
Add(manifestParts, Concatenation("  \"smoke_test\": ", JB(A13_SMOKE_TEST), ",\n"));
Add(manifestParts, Concatenation("  \"windows_processed\": ", String(Length(manifestEntries)), ",\n"));
Add(manifestParts, "  \"windows\": [\n");
for i in [1 .. Length(manifestEntries)] do
  e := manifestEntries[i];;
  Add(manifestParts, Concatenation("    {\"id\":", JStr(e.id), ",\"outfile\":", JStr(e.outfile),
    ",\"canonical_id_sha256\":", JStr(e.canonical_id_sha256),
    ",\"stage1_all_pass\":", JB(e.stage1_all_pass),
    ",\"gate_pass\":", JB(e.gate_pass),
    ",\"cert_sha256\":", JStr(CertSha256File(e.outfile)), "}"));
  if i < Length(manifestEntries) then Add(manifestParts, ",\n"); else Add(manifestParts, "\n"); fi;
od;
Add(manifestParts, "  ]\n");
Add(manifestParts, "}\n");
WriteFile("search/certs/a13_ladder_manifest_20260730.json", Concatenation(manifestParts));;
Print("\nWrote search/certs/a13_ladder_manifest_20260730.json\n");
Print("A13_LADDER_DRIVER_DONE\n");
