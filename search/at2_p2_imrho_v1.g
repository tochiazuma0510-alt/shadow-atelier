## search/at2_p2_imrho_v1.g -- AT-2 P2 再開・第一段: |Im rho| の実測(裁定1090・実装係タスクB)
##
## 正本: docs/notes/pb3_free_factor_check_v1.md §4(M=N cap K2 の分解フリー構成)・§5(再開判断)。
##   直積分解 PB3=F2x<c> は一切使わない(前回 at2_p2_ndiamond_construct_v1.g の PARTIAL は
##   F2=PB3/<c> を無限有限表示群として先に構成しようとしたために生じた -- 本 script はその
##   経路を完全に回避する。T_{m,f} を B3 -> B3/N という「既に有限で手元にある」群への
##   準同型として直接構成するのが§4の要点)。
##
## 構成(§4 の3行、逐語):
##   (1) rho := g |-> (pi_N(g), T_{m,f}(g))  :  B3 --> (B3/N) x (B3/N)
##   (2) M := ker rho = N cap K2,  B3/M ~= Im(rho)  (subdirect product)
##   (3) 実装: 2本の epi を GroupHomomorphismByImages で sigma_1,sigma_2 の像から作り、
##       直積への対角写像の Image を取る。|Im rho| を先に測る(上界ではなく実値)。
##
## 今回の範囲: |Im rho| の実測まで(GT(M) 列挙・trace 量子化は別発注・spec §5 の指示どおり)。
##
## u/c 注記: u=2m+1 は charming coordinate(既存 marking の再利用、封印 K(5) 量ではない)。
##   c はここでは登場しない(直積分解を使わないため PB3 の中心生成元に触れる必要がない)。

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
Print("# at2_p2_imrho_v1.g -- P2再開 第一段: |Im rho| 実測\n");
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
## same representative as search/at2_p2_ndiamond_construct_v1.g ("non-settled" class, m=2)
nonsettledRep := First(shadowsFix, sh -> sh.m = 2);;
mRep := nonsettledRep.m;;  fRep := nonsettledRep.f;;
uRep := 2*mRep + 1;;
Print("  shadow representative for T_{m,f}: m=", mRep, " u=2m+1=", uRep, "\n");

Print("\n=== T_{m,f}: B3 -> B3/N (Bq に直接、F2 経由なし) ===\n");
tA0 := GAPLIB_WallElapsedMs();;
genA_T := W.s1^uRep;;
genB_T := AbstractProd([fRep^-1, W.s2^uRep, fRep]);;
TmfHom := GroupHomomorphismByImages(W.Bq, W.Bq, [W.s1, W.s2], [genA_T, genB_T]);;
## also build directly as a B3-hom (domain B3, not "Bq self-endo") for the kernel K2 computation
TmfB3Hom := GroupHomomorphismByImages(B3, W.Bq, [ga, gb], [genA_T, genB_T]);;
tmfWellDefinedSelfEndo := (TmfHom <> fail);;
tmfWellDefinedB3 := (TmfB3Hom <> fail);;
Print("  T_{m,f} well-defined as PN-self-endo-of-Bq: ", tmfWellDefinedSelfEndo, "\n");
Print("  T_{m,f} well-defined as B3 -> Bq hom: ", tmfWellDefinedB3, "\n");
if not tmfWellDefinedB3 then
  Error("T_{m,f}: B3 -> Bq failed to construct -- shadow hexagon check should have guaranteed this; refusing to proceed silently");
fi;
tmfSurjective := (Size(Image(TmfB3Hom)) = Size(W.Bq));;
Print("  T_{m,f}: B3 -> Bq surjective (image size = |Bq|): ", tmfSurjective, "\n");
tA1 := GAPLIB_WallElapsedMs();;

Print("\n=== pi_N: B3 -> Bq (自然な商、対照用に同じ GroupHomomorphismByImages 経路で再構成) ===\n");
piNHom := GroupHomomorphismByImages(B3, W.Bq, [ga, gb], [W.s1, W.s2]);;
piNWellDefined := (piNHom <> fail);;
Print("  pi_N well-defined: ", piNWellDefined, "\n");
if not piNWellDefined then Error("pi_N construction failed -- should be automatic (natural quotient)"); fi;

Print("\n=== rho := (pi_N, T_{m,f}) : B3 -> Bq x Bq, diagonal ===\n");
tB0 := GAPLIB_WallElapsedMs();;
DP := DirectProduct(W.Bq, W.Bq);;
e1 := Embedding(DP, 1);;
e2 := Embedding(DP, 2);;
imgA := Image(e1, W.s1) * Image(e2, genA_T);;
imgB := Image(e1, W.s2) * Image(e2, genB_T);;
rhoHom := GroupHomomorphismByImages(B3, DP, [ga, gb], [imgA, imgB]);;
rhoWellDefined := (rhoHom <> fail);;
Print("  |DP|=", Size(DP), " (theoretical upper bound |Bq|^2)\n");
Print("  rho well-defined: ", rhoWellDefined, "\n");
if not rhoWellDefined then
  Error("rho construction failed -- both component maps are well-defined homs into the SAME target Bq, so the pairing should always be well-defined; refusing to proceed silently");
fi;
tB1 := GAPLIB_WallElapsedMs();;
Print("  rho construction elapsed_ms=", tB1-tB0, "\n");

if GAPLIB_CheckCap(90.0, "before-image-rho") then
  Print("[CAP WARNING] approaching cap before Image(rho) computation\n");
fi;

Print("\n=== |Im rho| の実測 ===\n");
tC0 := GAPLIB_WallElapsedMs();;
ImRho := Image(rhoHom);;
sizeImRho := Size(ImRho);;
tC1 := GAPLIB_WallElapsedMs();;
Print("  |Im rho| = ", sizeImRho, "  (elapsed_ms=", tC1-tC0, ")\n");
Print("  theoretical upper bound |Bq|^2 = ", Size(W.Bq)^2, "\n");
Print("  theoretical upper bound |PN|^2 (spec's 168^2) = ", Size(W.PN)^2, "\n");

Print("\n=== M := ker(rho) の位数・N cap K2 との整合(独立算出の突合) ===\n");
tD0 := GAPLIB_WallElapsedMs();;
Mker := Kernel(rhoHom);;
indexBMOverM := Index(B3, Mker);;
K2 := Kernel(TmfB3Hom);;
M2 := Intersection(Nsub, K2);;
indexM2 := Index(B3, M2);;
kernelIdentityMatches := (Mker = M2);;
indicesMatch := (indexBMOverM = sizeImRho) and (indexBMOverM = indexM2);;
tD1 := GAPLIB_WallElapsedMs();;
Print("  |B3:ker(rho)| = ", indexBMOverM, "  (should equal |Im rho| by first isomorphism theorem)\n");
Print("  |B3:(N cap K2)| (independent construction via Kernel(T_mf_B3) intersect N) = ", indexM2, "\n");
Print("  ker(rho) = N cap K2 (set equality, independent check): ", kernelIdentityMatches, "\n");
Print("  index values all consistent: ", indicesMatch, "  elapsed_ms=", tD1-tD0, "\n");

## ================= JSON output =================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_imrho.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/at2_p2_imrho_v1.g");;
wordsSha256 := ComputeSha256File("search/iso_census83_deep15_data.g");;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/at2_p2_imrho_v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/at2_p2_imrho_v1.g\",\"order\":\"裁定1090(pb3_free_factor_check_v1 §4 P2再開・実装係タスクB)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/pb3_free_factor_check_v1.md §4/§5\"",
  ",\"window\":\"[1008,521] slot1\"",
  ",\"method_note\":\"rho:=(pi_N,T_mf):B3->(B3/N)x(B3/N) built by GroupHomomorphismByImages directly into the ALREADY-FINITE target Bq=B3/N (both component maps share the same finite codomain), avoiding the infinite fp-group construction F2=PB3/<c> that caused search/at2_p2_ndiamond_construct_v1.g STAGE1 to report PARTIAL. No direct-product decomposition of PB3 is used (per Sol warning addressed in pb3_free_factor_check_v1.md §2.3).\",",
  "\"shadow_representative\":{\"m\":", String(mRep), ",\"u_2m_plus_1\":", String(uRep),
    ",\"f_perm_string\":", JStr(String(fRep)),
    ",\"note\":\"same representative as search/certs/at2_p2_ndiamond_construct_v1_20260813.json (m=2, first non-settled-class shadow found)\"},",
  "\"window_base\":{\"bq_order\":", String(Size(W.Bq)), ",\"pn_order\":", String(Size(W.PN)),
    ",\"n_ord\":", String(W.Nord), ",\"shadow_total\":", String(Length(shadowsFix)), "},",
  "\"hom_well_definedness\":{",
    "\"t_mf_b3_to_bq\":", JB(tmfWellDefinedB3), ",",
    "\"t_mf_b3_to_bq_surjective\":", JB(tmfSurjective), ",",
    "\"pi_n_b3_to_bq\":", JB(piNWellDefined), ",",
    "\"rho_b3_to_bqxbq\":", JB(rhoWellDefined),
  "},",
  "\"im_rho\":{",
    "\"size\":", String(sizeImRho), ",",
    "\"upper_bound_bq_squared\":", String(Size(W.Bq)^2), ",",
    "\"upper_bound_pn_squared_spec_168sq\":", String(Size(W.PN)^2),
  "},",
  "\"kernel_crosscheck\":{",
    "\"index_b3_over_ker_rho\":", String(indexBMOverM), ",",
    "\"index_b3_over_n_cap_k2_independent\":", String(indexM2), ",",
    "\"ker_rho_eq_n_cap_k2_set_equal\":", JB(kernelIdentityMatches), ",",
    "\"all_indices_consistent\":", JB(indicesMatch),
  "},",
  "\"u_touched\":true,\"u_touch_note\":\"u=2m+1 charming coordinate reused from existing shadow marking (same as at2_p2_ndiamond_construct_v1.g), not the sealed K(5) instance quantity\",",
  "\"c_touched\":false,",
  "\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\",\"deep15_data_sha256\":\"", wordsSha256, "\"}",
  "}"
);;

outPath := "search/certs/at2_p2_imrho_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
