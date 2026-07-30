#############################################################################
## search/probe/wac_v1/r4_acoords_probe.g -- 裁定236 発注: NULL-R4 発火後の
## Xi(ker) B_x-座標 読み取り probe (r=4 discriminating window, m=0 layer only)
##
## 出所: 裁定236(sol/裁定_236_r4C窓真判定_235撤回.md)末尾「A ≅ C5^2 の25座標の
## 型読み(凍結NULL枠指示『B_x-座標を最優先で読む』)-- 証明書はcountのみにつき、
## 座標リスト出力の小probeを発注」。
##
## 接触遮断: docs/notes/r4_prediction_v1.md, pruning_law_*.md, ideas/ は本
## probe からは一切 Read しない。期待値・比較対象はコードに書かない -- 出力は
## すべて生の測定値であり、解釈も予言との比較もしない。
##
## strike-r4.g は R4_LIBRARY_ONLY モードで Read するのみで、一切改変しない
## (仕様: strike-r4.g 冒頭コメントの「モード」節・末尾 R4_LIBRARY_ONLY guard)。
## 本 probe は strike-r4.g が公開する以下の関数/表をそのまま再利用する:
##   BuildS1S2E, ProcessWindowStage1 (窓構成+入口assert, canonical sha照合込み,
##     fail-closed), ScanWindowXi (per-m Xi-restricted走査, fail-closed上界
##     R4_XI_BOUND_PER_M=112,500,000 込み), ComputeAutPStab, R4_WINDOWS,
##     R4_CANONICAL_SHA, R4_CHARMING_SET, R4_XI_BOUND_PER_M/TOTAL,
##     PrintStr, Sha256OfString, CertSha256File.
## kerchi-judge.g (JUDGE_LIBRARY_ONLY 経由, strike-r4.g が既に Read 済み) から:
##   GroupOfShadows, AbstractProd.
## gaplib_common.g (同じく既 Read) から: JStr, JB, JArr, JPair, JoinC, WriteFile.
##
## ---- m=0 層 = ker χ~ であることについて (再導出ではなく既存コードの直接帰結) ----
## kerchi-judge.g の GroupOfShadows(W,S) は
##   kerIdx := Filtered([1 .. n], i -> S[i][1] = 0);
##   ker := Group(List(kerIdx, i -> regs[i]))
## と定義している -- つまり S の中で m=0 のエントリだけを取り出した部分群が
## 常に ker である(全 charming m を含む S でも、m=0 だけの S でも同じ規則)。
## したがって S として最初から m=0 層だけ (Xi-restricted 走査を charmingSet=[0]
## に絞って得た受理 shadow 集合) を渡せば、GroupOfShadows が返す closed group
## そのものが ker χ~ に一致する(kerIdx が全インデックスになるため ker=G と
## 構造的に一致 -- 下で Size 照合により fail-closed に再確認する)。これにより
## 4 層 x 112,500,000 の全走査(driver 本体, ~49分/窓)を避け、1 層
## (112,500,000 走査, driver の実測: 約730秒)だけで済ませる。
##
## R4_CHARMING_SET の一時的な再束縛について: ScanWindowXi はグローバル変数
## R4_CHARMING_SET をループ対象として直接参照する(strike-r4.g 内の実装、引数
## ではない)。strike-r4.g 自体は改変しないので、ProcessWindowStage1 の実行後
## (この関数の入口assertは元の R4_CHARMING_SET=[0,1,3,4] を使って正しく検証
## 済み)に R4_CHARMING_SET := [0] へ再束縛してから ScanWindowXi を呼ぶ -- これ
## は strike-r4.g が公開しているグローバル変数の設計どおりの使い方であり、
## ファイルの改変ではない。
##
## preamble 変数:
##   R4ACP_WINDOW := "C" | "B"   -- 対象窓 (必須)
##   R4ACP_SMOKE  := true         -- 走査部をスキップし、窓構成+入口assertまで
##                                   で終了するローカル smoke モード (省略時 false)
##
## Output (R4ACP_SMOKE でない場合):
##   search/certs/r4_acoords_<窓(C|B)>_20260730.json
#############################################################################

R4_LIBRARY_ONLY := true;;
Read("search/strike-r4.g");;

if not IsBound(R4ACP_WINDOW) then
  Error("r4_acoords_probe.g: R4ACP_WINDOW must be bound to \"C\" or \"B\" before Read()-ing this file");
fi;
if not (R4ACP_WINDOW = "C" or R4ACP_WINDOW = "B") then
  Error("r4_acoords_probe.g: R4ACP_WINDOW must be \"C\" or \"B\", got ", R4ACP_WINDOW);
fi;
if not IsBound(R4ACP_SMOKE) then
  R4ACP_SMOKE := false;;
fi;

R4ACP_DATE_STAMP := "20260730";;
R4ACP_SCRIPT_PATH := "search/probe/wac_v1/r4_acoords_probe.g";;

Print("\n################################################################\n");
Print("# r4_acoords_probe: window=", R4ACP_WINDOW, " smoke=", R4ACP_SMOKE, "\n");
Print("################################################################\n");

#############################################################################
## ---------------------- window construction + entry assert (fail-closed) --
#############################################################################
r4acp_w := First(R4_WINDOWS, ww -> ww.shaKey = R4ACP_WINDOW);;
if r4acp_w = fail then
  Error("r4_acoords_probe.g: no window in R4_WINDOWS with shaKey=", R4ACP_WINDOW);
fi;

r4acp_st := ProcessWindowStage1(r4acp_w);;
Print("STAGE 1 (", r4acp_w.id, ") overall: ", PF(r4acp_st.ok), "\n");
if not r4acp_st.ok then
  Error("r4_acoords_probe.g: STAGE 1 failed for window ", r4acp_w.id,
        " -- fail-closed, refusing to proceed");
fi;
if r4acp_st.canonical_id_sha256 <> R4_CANONICAL_SHA.(r4acp_w.shaKey) then
  Error("r4_acoords_probe.g: canonical_id_sha256 mismatch for window ", r4acp_w.id,
        " -- fail-closed (this is also checked inside ProcessWindowStage1's asserts, ",
        "re-checked here explicitly)");
fi;

if R4ACP_SMOKE = true then
  Print("\n[SMOKE] R4ACP_SMOKE=true -- window construction + entry assert passed, ",
        "stopping before Xi-restricted scan (fail-closed upper bound / full scan is ",
        "CI-only). R4ACP_SMOKE_OK\n");
fi;

# NOTE: QUIT is a top-level-REPL-only command in GAP and is a syntax error
# when reached via Read() (confirmed empirically during local smoke testing,
# 2026-07-30) -- so the smoke early-exit is done by wrapping the remainder of
# the script in this guard instead of QUIT-ing out of it.
if R4ACP_SMOKE <> true then

#############################################################################
## ---------------------- m=0-only Xi-restricted scan (reuses ScanWindowXi) -
#############################################################################
R4_CHARMING_SET := [0];;   # see header note -- global rebind, not a file edit
r4acp_scanRes := ScanWindowXi(r4acp_w, r4acp_st);;
r4acp_corr := r4acp_scanRes.corr;;
Print("\n[m=0 scan] accepted=", Length(r4acp_corr), " scanned=", r4acp_scanRes.totalScanned,
      " bound=", R4_XI_BOUND_PER_M, "\n");

#############################################################################
## ---------------------- ker = m=0-layer group (structural identity) -------
#############################################################################
r4acp_gi := GroupOfShadows(r4acp_st.W, r4acp_corr);;
if not r4acp_gi.closed then
  Error("r4_acoords_probe.g: (3.53) closure FAILED for the m=0-layer shadow set of window ",
        r4acp_w.id, " -- refusing to report structure of a set not confirmed to be a group");
fi;
if Size(r4acp_gi.ker) <> Size(r4acp_gi.G) then
  Error("r4_acoords_probe.g: m=0-layer group's own GroupOfShadows(...).ker does not match ",
        ".G in size (", Size(r4acp_gi.ker), " vs ", Size(r4acp_gi.G), ") -- the structural ",
        "identity documented in the header comment (kerIdx = all indices when every shadow ",
        "has m=0) failed to hold empirically; refusing to proceed fail-closed");
fi;
r4acp_K := r4acp_gi.G;;
r4acp_regs := r4acp_gi.regs;;
Print("[ker] K_order=", Size(r4acp_K), "\n");

#############################################################################
## ---------------------- A := O_2'(K) (same recipe as MeasureWindow 4/5) ---
#############################################################################
r4acp_ASlist := Filtered(NormalSubgroups(r4acp_K), r4acp_N1 -> Size(r4acp_N1) mod 2 = 1);;
if Length(r4acp_ASlist) > 0 then
  r4acp_A := First(r4acp_ASlist, r4acp_N1 -> Size(r4acp_N1) = Maximum(List(r4acp_ASlist, Size)));;
else
  r4acp_A := TrivialSubgroup(r4acp_K);;
fi;
r4acp_S := SylowSubgroup(r4acp_K, 2);;
Print("[A/S] A_order=", Size(r4acp_A), " A_struct=", StructureDescription(r4acp_A),
      " S_order=", Size(r4acp_S), " S_struct=", StructureDescription(r4acp_S), "\n");
r4acp_A_idgroup := "null";;
if SmallGroupsAvailable(Size(r4acp_A)) then
  r4acp_A_idgroup := JPair(IdGroup(r4acp_A)[1], IdGroup(r4acp_A)[2]);;
fi;

#############################################################################
## ---------------------- per-shadow alpha (same recipe as MeasureWindow 18) -
#############################################################################
r4acp_StabInfo := ComputeAutPStab(r4acp_st.W.PN, r4acp_st.W.x);;
r4acp_alphas := [];;  r4acp_alphaWellDefined := true;;
for r4acp_i in [1 .. Length(r4acp_corr)] do
  r4acp_m1 := r4acp_corr[r4acp_i][1];;  r4acp_f1 := r4acp_corr[r4acp_i][2];;
  r4acp_u1 := 2*r4acp_m1 + 1;;
  r4acp_correctedY := AbstractProd([r4acp_f1^-1, r4acp_st.W.y^r4acp_u1, r4acp_f1]);;
  r4acp_alpha := RepresentativeAction(r4acp_StabInfo.AutP, [r4acp_st.W.x, r4acp_st.W.y],
                   [r4acp_st.W.x^r4acp_u1, r4acp_correctedY], OnTuples);;
  if r4acp_alpha = fail then
    r4acp_alphaWellDefined := false;;
    r4acp_alphas[r4acp_i] := fail;;
  else
    r4acp_alphas[r4acp_i] := r4acp_alpha;;
  fi;
od;
Print("[alpha] xi_alpha_well_defined=", r4acp_alphaWellDefined, "\n");

#############################################################################
## ---------------------- Xi|_K hom + Bx coordinate frame (same recipe as ---
## ---------------------- MeasureWindow 22/22b) ------------------------------
#############################################################################
r4acp_bxCycles := Cycles(r4acp_st.W.x, MovedPoints(r4acp_st.W.x));;
r4acp_bxGens := List(r4acp_bxCycles, r4acp_cyc ->
  MappingPermListList(r4acp_cyc, Concatenation(r4acp_cyc{[2 .. Length(r4acp_cyc)]}, [r4acp_cyc[1]])));;
r4acp_Bx := Group(r4acp_bxGens);;
Print("[Bx] Bx_order=", Size(r4acp_Bx), "\n");

r4acp_xiKgens := GeneratorsOfGroup(r4acp_K);;
r4acp_xiK_alphas := List(r4acp_xiKgens, r4acp_gk -> r4acp_alphas[Position(r4acp_regs, r4acp_gk)]);;
r4acp_xiK_Hom := GroupHomomorphismByImages(r4acp_K, r4acp_StabInfo.AutP, r4acp_xiKgens, r4acp_xiK_alphas);;

r4acp_A_coords_status := "";;
r4acp_AEltsWithCoords := [];;   # list of rec(elt:=perm, coords:=[c1..c4]) or rec(elt:=perm,coords:=fail)
if r4acp_xiK_Hom = fail then
  r4acp_A_coords_status := "hom_not_well_defined_on_K";;
  Print("[NOTE] Xi|_K did not extend to a well-defined hom on K's generating set -- ",
        "coordinates not computed\n");
else
  r4acp_A_coords_status := "computed";;
  for r4acp_ag in Elements(r4acp_A) do
    r4acp_imgA := Image(r4acp_xiK_Hom, r4acp_ag);;
    if r4acp_imgA in r4acp_Bx then
      r4acp_coords := List([1 .. Length(r4acp_bxGens)], r4acp_k ->
        First([0 .. 4], r4acp_p ->
          r4acp_bxCycles[r4acp_k][1]^r4acp_imgA = r4acp_bxCycles[r4acp_k][1]^(r4acp_bxGens[r4acp_k]^r4acp_p)));;
      Add(r4acp_AEltsWithCoords, rec(elt := r4acp_ag, coords := r4acp_coords));;
    else
      Add(r4acp_AEltsWithCoords, rec(elt := r4acp_ag, coords := fail));;
    fi;
  od;
fi;
r4acp_coordsComputedCount := Number(r4acp_AEltsWithCoords, r4acp_r -> r4acp_r.coords <> fail);;
Print("[22b] A_elements=", Size(r4acp_A), " coords_computed=", r4acp_coordsComputedCount, "\n");

#############################################################################
## ---------------------- distinct coordinate vectors + raw type tally ------
#############################################################################
r4acp_allCoordVecs := List(Filtered(r4acp_AEltsWithCoords, r4acp_r -> r4acp_r.coords <> fail),
                            r4acp_r -> r4acp_r.coords);;
r4acp_distinctCoordVecs := Set(r4acp_allCoordVecs);;

ClassifyR4ACPCoordType := function(c)
  local c1, c2, c3, c4;
  c1 := c[1];;  c2 := c[2];;  c3 := c[3];;  c4 := c[4];;
  if c1 = c2 and c2 = c3 and c3 = c4 then return "diagonal"; fi;
  if c1 = c2 and c3 = c4 and c1 <> c3 then return "AABB_12_34"; fi;
  if c1 = c3 and c2 = c4 and c1 <> c2 then return "ABAB_13_24"; fi;
  if c1 = c4 and c2 = c3 and c1 <> c2 then return "ABBA_14_23"; fi;
  return "other";
end;;

r4acp_typeTally := rec(diagonal := 0, AABB_12_34 := 0, ABAB_13_24 := 0, ABBA_14_23 := 0, other := 0);;
r4acp_typedDistinct := [];;
for r4acp_v in r4acp_distinctCoordVecs do
  r4acp_ty := ClassifyR4ACPCoordType(r4acp_v);;
  r4acp_typeTally.(r4acp_ty) := r4acp_typeTally.(r4acp_ty) + 1;;
  Add(r4acp_typedDistinct, rec(coords := r4acp_v, type := r4acp_ty));;
od;
Print("[type tally, over distinct vectors] diagonal=", r4acp_typeTally.diagonal,
      " AABB=", r4acp_typeTally.AABB_12_34, " ABAB=", r4acp_typeTally.ABAB_13_24,
      " ABBA=", r4acp_typeTally.ABBA_14_23, " other=", r4acp_typeTally.other, "\n");

#############################################################################
## ---------------------- (bonus) S-conjugation orbits of A, mapped to coords
## S <= K acts on A <= K (A normal in K) by ordinary conjugation -- a plain
## group-theoretic orbit computation, independent of whether Xi|_K's block
## action on Bx is trusted beyond what 22b already used for the coordinates
## themselves. Orbit reps are reported with their (possibly fail) coordinate
## vectors -- raw data, no interpretation.
#############################################################################
r4acp_S_orbit_status := "not_computed";;
r4acp_orbitsJsonParts := [];;
if Size(r4acp_A) > 0 then
  r4acp_ActConj := function(a, g) return a^g; end;;
  r4acp_orbitsA := Orbits(r4acp_S, Elements(r4acp_A), r4acp_ActConj);;
  r4acp_S_orbit_status := "computed";;
  Print("[S-orbits] S_order=", Size(r4acp_S), " A_order=", Size(r4acp_A),
        " orbit_count=", Length(r4acp_orbitsA), " orbit_sizes=",
        List(r4acp_orbitsA, Length), "\n");
  for r4acp_orb in r4acp_orbitsA do
    r4acp_orbCoords := [];;
    for r4acp_oe in r4acp_orb do
      r4acp_rec := First(r4acp_AEltsWithCoords, r4acp_r -> r4acp_r.elt = r4acp_oe);;
      if r4acp_rec = fail or r4acp_rec.coords = fail then
        Add(r4acp_orbCoords, "null");;
      else
        Add(r4acp_orbCoords, JArr(List(r4acp_rec.coords, String)));;
      fi;
    od;
    Add(r4acp_orbitsJsonParts, Concatenation("{\"orbit_size\":", String(Length(r4acp_orb)),
      ",\"coords\":", JArr(r4acp_orbCoords), "}"));;
  od;
fi;

#############################################################################
## ---------------------- JSON output ----------------------------------------
#############################################################################
r4acp_outfile := Concatenation("search/certs/r4_acoords_", r4acp_w.shaKey, "_",
  R4ACP_DATE_STAMP, ".json");;

r4acp_distinctCoordsJson := JArr(List(r4acp_typedDistinct, r4acp_td ->
  Concatenation("{\"coords\":", JArr(List(r4acp_td.coords, String)),
    ",\"type\":", JStr(r4acp_td.type), "}")));;

r4acp_scanEntry := r4acp_scanRes.perM[1];;

r4acp_out := Concatenation(
  "{\n",
  "  \"generated_by\": \"", R4ACP_SCRIPT_PATH, "\",\n",
  "  \"script_sha256\": \"", CertSha256File(R4ACP_SCRIPT_PATH), "\",\n",
  "  \"note\": \"raw measurements only -- interpretation none, NOT a ledger claim. ",
      "m=0-layer-only Xi-restricted scan of window ", r4acp_w.id, "; the m=0-layer group ",
      "is ker chi-tilde by construction of kerchi-judge.g's GroupOfShadows (see script ",
      "header). Contact-blocked from docs/notes/r4_prediction_v1.md / pruning_law_*.md / ",
      "ideas/ -- no expected value is encoded here.\",\n",
  "  \"window_id\": \"", r4acp_w.id, "\",\n",
  "  \"canonical_id_sha256\": \"", r4acp_st.canonical_id_sha256, "\",\n",
  "  \"canonical_id_sha256_gate\": \"", R4_CANONICAL_SHA.(r4acp_w.shaKey), "\",\n",
  "  \"stage1_all_pass\": ", JB(r4acp_st.ok), ",\n",
  "  \"m0_scan_accounting\": {\"m\":0,\"scanned\":", String(r4acp_scanEntry.scanned),
      ",\"bound\":", String(r4acp_scanEntry.chunk_scan_bound),
      ",\"accepted\":", String(r4acp_scanEntry.accepted),
      ",\"settled_fail_count\":", String(r4acp_scanEntry.settled_fail_count), "},\n",
  "  \"ker_size\": ", String(Size(r4acp_K)), ",\n",
  "  \"ker_equals_m0_layer_group_size_check\": ", JB(Size(r4acp_gi.ker) = Size(r4acp_gi.G)), ",\n",
  "  \"A_order\": ", String(Size(r4acp_A)), ",\n",
  "  \"A_struct\": \"", StructureDescription(r4acp_A), "\",\n",
  "  \"A_idgroup\": ", r4acp_A_idgroup, ",\n",
  "  \"S_order\": ", String(Size(r4acp_S)), ",\n",
  "  \"S_struct\": \"", StructureDescription(r4acp_S), "\",\n",
  "  \"Bx_order\": ", String(Size(r4acp_Bx)), ",\n",
  "  \"xi_alpha_well_defined\": ", JB(r4acp_alphaWellDefined), ",\n",
  "  \"A_coords_status\": \"", r4acp_A_coords_status, "\",\n",
  "  \"A_elements_total\": ", String(Size(r4acp_A)), ",\n",
  "  \"A_coords_computed_count\": ", String(r4acp_coordsComputedCount), ",\n",
  "  \"distinct_coords_count\": ", String(Length(r4acp_distinctCoordVecs)), ",\n",
  "  \"distinct_coords\": ", r4acp_distinctCoordsJson, ",\n",
  "  \"type_tally_over_distinct_coords\": {\"diagonal\":", String(r4acp_typeTally.diagonal),
      ",\"AABB_12_34\":", String(r4acp_typeTally.AABB_12_34),
      ",\"ABAB_13_24\":", String(r4acp_typeTally.ABAB_13_24),
      ",\"ABBA_14_23\":", String(r4acp_typeTally.ABBA_14_23),
      ",\"other\":", String(r4acp_typeTally.other), "},\n",
  "  \"S_orbit_status\": \"", r4acp_S_orbit_status, "\",\n",
  "  \"S_orbits_of_A_conjugation_mapped_to_coords\": ", JArr(r4acp_orbitsJsonParts), "\n",
  "}\n");;

WriteFile(r4acp_outfile, r4acp_out);;
Print("Wrote ", r4acp_outfile, "\n");
Print("R4ACP_DRIVER_DONE\n");

fi;   # R4ACP_SMOKE guard
