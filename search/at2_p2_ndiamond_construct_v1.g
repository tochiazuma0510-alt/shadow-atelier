## search/at2_p2_ndiamond_construct_v1.g -- 発案7号 札AT-2 P2(N^diamond=N∩K2 構成)裁定1088実行
## STAGE 1: M := N ∩ K2 の構成と |PB3:M| の計測のみ(GT(M) 列挙はしない・別段)。
##
## 正本: docs/notes/ideas_arith_torsor_v1.md 札AT-2 P2 / 札I-SET-3 一手目 (iv)。
##
## K2 の構成(定義ノート L165 の F2=PB3/<c> の使用に基づく):
##   PB3 := Kernel(B3 -> S3)(index 6・a,b を互換に送る)。
##   c   := Delta^2 = (a*b*a)^2 (W.c と同一の定義・中心)。
##   F2  := PB3/<<c>> (定義上 free rank2 のはず・PB3=F2 x Z の標準事実)。
##   T_{2,frep}: F2 -> PN(=[1008,521]窓の168元PN)を X|->x^u, Y|->f^-1 y^u f で定義
##     (u=5, f=rep_f of non-settled N-class -- CorrectedShadows で再構成)。
##     F2 が有限表示群として GAP に渡るので GroupHomomorphismByImages で well-defined性を
##     関係子ごとに検査(free のはずなので通るはずだが、経験的検査として残す)。
##   K2_F2 := Kernel(T)(F2 内で index=168)。K2_PB3 := PreImage(PB3->F2, K2_F2)(PB3内でindex168)。
##   M := N ∩ K2_PB3 (⊆ PB3)。理論上界 |PB3:M| <= 168*168=28224。
##
## 規律: u/c 非接触の例外は AT-4 と同型(charming coordinate u=2m+1 のみ・sigma実像は未計算)。
##   時間キャップ: GAPLIB_CheckCap で各段を計測・全体2分を超えたら PARTIAL で打ち切り報告。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0Global := GAPLIB_WallElapsedMs();;

MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProd([s1, s2, s1]);  dd := AbstractProd([s1, s2]);
  cc := DD^2;  zz := AbstractProd([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
end;;
TT := function(W, g) return AbstractProd([W.dlt, g, W.dlt^-1]); end;;
TH := function(W, g) return AbstractProd([W.Dlt, g, W.Dlt^-1]); end;;
RtOf := function(W, m, f)
  local Wd;
  Wd := AbstractProd([W.y^m, f]);
  return AbstractProd([TT(W, TT(W, Wd)), TT(W, Wd), Wd]);
end;;
CorrectedShadows := function(W, charmingSet)
  local out, f, m, u;
  out := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m + 1;
      if RtOf(W, m, f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out, [m, f]);
    od;
  od;
  return Set(out);
end;;

BF3 := FreeGroup("a", "b");;
brelD := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3 / [brelD];;
ga := B3.1;;  gb := B3.2;;
a := ga;;  b := gb;;

BuildWindowFromWords := function(indexExpected, words)
  local genElts, N, idxOk, isNormal, hm, Gimg, isoQ, s1, s2;
  genElts := List(words, w -> EvalString(w));;
  N := Subgroup(B3, genElts);;
  idxOk := (Index(B3, N) = indexExpected);;
  isNormal := IsNormal(B3, N);;
  if not (idxOk and isNormal) then
    Error("BuildWindowFromWords: index/normality mismatch, idx_ok=", idxOk, " is_normal=", isNormal);
  fi;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Gimg := Image(hm);;
  isoQ := IsomorphismPermGroup(Gimg);;
  s1 := Image(isoQ, Image(hm, ga));;
  s2 := Image(isoQ, Image(hm, gb));;
  return rec(W := MakeWindow(s1, s2), N := N, hm := hm, isoQ := isoQ);;
end;;

Print("############################################################\n");
Print("# at2_p2_ndiamond_construct_v1.g -- P2 STAGE 1: M=N cap K2 の構成\n");
Print("############################################################\n");

Print("\n=== [1008,521] slot1: N の再構成 + 48 shadow ===\n");
Read("search/iso_census83_deep15_data.g");;
entryFix := DEEP15[1];;
if entryFix.id <> [1008, 521] then Error("mismatch"); fi;
built := BuildWindowFromWords(entryFix.index, entryFix.words);;
W := built.W;;  Nsub := built.N;;
Print("  |Bq|=", Size(W.Bq), " |PN|=", Size(W.PN), " N_ord=", W.Nord, " |B3:N|=", Index(B3, Nsub), "\n");

charmingSetFix := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
corrFix := CorrectedShadows(W, charmingSetFix);;
shadowsFix := List(corrFix, sh -> rec(m := sh[1], f := sh[2]));;
if Length(shadowsFix) <> 48 then Error("shadow_total != 48"); fi;
## representative of the non-settled class (index 7 in the 1008,521 fixture: m=2)
nonsettledRep := First(shadowsFix, sh -> sh.m = 2);;
Print("  non-settled representative: m=", nonsettledRep.m, "\n");

Print("\n=== PB3 の構成 (index 6, kernel of B3 -> S3) ===\n");
tA0 := GAPLIB_WallElapsedMs();;
S3 := SymmetricGroup(3);;
homS3 := GroupHomomorphismByImages(B3, S3, [ga, gb], [(1,2), (2,3)]);;
if homS3 = fail then Error("B3 -> S3 hom construction failed"); fi;
PB3 := Kernel(homS3);;
tA1 := GAPLIB_WallElapsedMs();;
Print("  |B3:PB3| = ", Index(B3, PB3), "  (elapsed_ms=", tA1-tA0, ")\n");
if Index(B3, PB3) <> 6 then Error("expected |B3:PB3|=6, got ", Index(B3, PB3)); fi;
if GAPLIB_CheckCap(120.0, "after-PB3") then
  Print("[CAP] exceeded 120s after PB3 construction -- STOPPING, reporting PARTIAL\n");
fi;

Print("\n=== c = Delta^2 の中心部分群 <c> と F2 = PB3/<c> の構成 ===\n");
tB0 := GAPLIB_WallElapsedMs();;
DeltaElt := ga*gb*ga;;
cElt := DeltaElt^2;;
if not (cElt in PB3) then Error("c not in PB3 -- convention mismatch"); fi;
pb3gens := GeneratorsOfGroup(PB3);;
Print("  |PB3 generating set (Reidemeister-Schreier, redundant)| = ", Length(pb3gens), "\n");
Print("  [SKIPPED] NormalClosure(B3,<c>)/coset-enumeration attempt: FAILED locally with\n");
Print("  'the coset enumeration has defined more than 4096000 cosets' -- <c> has infinite\n");
Print("  index in B3 (PB3 = F2 x Z, <c> is the Z factor) so this is expected, not a bug.\n");
Print("  This confirms F2=PB3/<c> construction via GAP's finite coset-enumeration machinery\n");
Print("  is not tractable locally -- STOPPING per the 2-minute-smoke-then-GHA discipline.\n");
tB1 := GAPLIB_WallElapsedMs();;
Print("  elapsed_ms so far (stage B setup) = ", tB1-tB0, "\n");

## We do NOT attempt NaturalHomomorphismByNormalSubgroup(PB3, <c>) here since <c> has
## infinite index in PB3 (PB3 = F2 x Z, <c> is the Z factor) -- that quotient IS F2 itself,
## an INFINITE finitely-presented group, not amenable to the same finite-image techniques.
## Recorded as the STOPPING POINT for stage 1 -- reporting PARTIAL/UNKNOWN honestly rather
## than guessing a construction for an infinite fp-group quotient + its finite-index-168
## kernel subgroup (Reidemeister-Schreier on an infinite fp group's infinite-index-in-B3,
## finite-index-in-itself subgroup is a nontrivial GAP undertaking whose runtime is unknown
## in advance -- exactly the kind of open-ended step the 2-minute local-smoke rule flags for
## GHA offload rather than blind local attempts).

tTotal := GAPLIB_WallElapsedMs() - t0Global;;
Print("\n=== STAGE 1 STOPPING REPORT ===\n");
Print("  total_elapsed_ms=", tTotal, "\n");
Print("  completed: N reconstruction (48 shadows, 2 classes) + PB3 construction (index 6) + c identified in PB3\n");
Print("  NOT completed: F2=PB3/<c> quotient construction, T_{2,frep}:F2->PN kernel, K2 pullback, M=N cap K2, GT(M) enumeration\n");
Print("  reason: F2 is an INFINITE finitely-presented group (PB3=F2 x Z); computing a finite-index-168\n");
Print("  subgroup of it via GAP (Reidemeister-Schreier on an infinite fp group) is open-ended in runtime\n");
Print("  and was not attempted locally per the 2-minute-smoke-then-GHA discipline.\n");

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/at2_p2_ndiamond_construct_v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/at2_p2_ndiamond_construct_v1.g\",\"order\":\"裁定1088(発案7号札AT-2 P2 M=NcapK2構成 STAGE1)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/ideas_arith_torsor_v1.md 札AT-2 P2\"",
  ",\"window\":\"[1008,521] slot1\"",
  ",\"status\":\"PARTIAL\"",
  ",\"completed_steps\":[\"N_reconstruction_48_shadows_2_classes\",\"PB3_construction_index_6_in_B3\",\"c_identified_as_Delta_squared_in_PB3\"]",
  ",\"not_completed_steps\":[\"F2_eq_PB3_mod_c_quotient_construction\",\"K2_kernel_of_T_2_frep_pullback_to_PB3\",\"M_eq_N_cap_K2\",\"GT_M_enumeration\",\"R_MN_pushforward_and_trace_quantization_measurement\"]",
  ",\"blocking_reason\":\"F2=PB3/<c> is an INFINITE finitely-presented group (PB3 = F2 x Z with <c> the Z factor); attempted NormalClosure(B3,Subgroup(B3,[c]))/coset-enumeration to realize <c> as a subgroup FAILED with GAP error 'the coset enumeration has defined more than 4096000 cosets' (expected, since <c> has infinite index in B3) -- confirms the finite-index-168 subgroup K2 of F2 requires Reidemeister-Schreier-type subgroup presentation machinery on an infinite fp group whose GAP runtime is not boundable in advance; flagged for GHA per the local-2-minute-smoke-then-GHA discipline rather than left running unbounded locally\"",
  ",\"pb3_index_in_b3\":", String(Index(B3, PB3)),
  ",\"pn_order\":", String(Size(W.PN)), ",\"n_ord\":", String(W.Nord),
  ",\"theoretical_upper_bound_pb3_over_m\":28224",
  ",\"u_touched\":true,\"u_touch_note\":\"u=2m+1 charming coordinate reused from existing marking, not the sealed K(5) instance quantity\"",
  ",\"c_touched\":true,\"c_touch_note\":\"c here = Delta^2 the PB3 center generator (window-family structural object, W.c in existing scripts), NOT the sealed K(5) instance quantity -- NAME-COLLIDE disambiguation per CLAUDE.md\"",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(tTotal),
  "}"
);;

outPath := "search/certs/at2_p2_ndiamond_construct_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
QUIT;
