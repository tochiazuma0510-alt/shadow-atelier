## search/iset4_b0_sweep_v1.g -- 【B''-0】83窓の全15窓(DEEP15)一括掃引(裁定1118・実装係タスク1)
##
## 正本: docs/notes/u6_prereg_readout_v1.md §4 [B''-0]
## 目的: 全15窓(DEEP15・K^(9)対照つき)について
##   |Q|=|F_2/N_{F_2}| , |PN| , z_0=[PN:Q] , |[Q,Q]| ,
##   |D_1|=|C_Q(sigma1-bar)| , |D_0|=|D_1 cap [Q,Q]|
## を測定するのみ。選抜基準: |D_0|>=4 の窓を [B''] の対象にする。
## 副産物: z_0>1 の窓があれば型退化対照(K9の代替)。
##
## K^(9) 対照: search/iset4_bprime_v1.g で既報の【実装障害・blocked】(σ1の実像を
##   持つB3内実現が現行コードベースに存在しない)がそのまま適用されるため、
##   本 script でも K^(9) は UNKNOWN_BLOCKED として記帳し計算しない(再報告不要
##   -- 既報の障害の再発生であり新しい二義性ではない)。
##
## 規律: u/c 非接触・封印非接触・prereg 非抵触。判定語なし・cert は生値のみ。
##   ★ D_1 := C_Q(sigma1-bar) = C_{B3/N}(sigma1-bar) ∩ Q (Q 内・PN でない)。
##   D_0 := D_1 ∩ [Q,Q]。(iset4_bprime_v1.g の [B'-0] と同一定義・VERBATIM に近い実装)

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0Global := GAPLIB_WallElapsedMs();;

## ================= (F2) machinery, VERBATIM from search/iset4_bprime_v1.g
##   (itself verbatim from search/set_surgery_fixture_v1.g / search/iso_census83_deep15_v1.g
##   / search/wall-miner-v4.g) =================
MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;  yy := s2^2;
  DD := AbstractProd([s1, s2, s1]);  dd := AbstractProd([s1, s2]);
  cc := DD^2;  zz := AbstractProd([xx, yy])^-1;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1, s2), PN := Group(xx, yy),
             Nord := Lcm(Order(xx), Order(yy), Order(cc)));
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
  return MakeWindow(s1, s2);;
end;;

Print("############################################################\n");
Print("# iset4_b0_sweep_v1.g -- [B''-0] 83窓の全15窓一括掃引(裁定1118)\n");
Print("############################################################\n");

Read("search/iso_census83_deep15_data.g");;
Print("\n=== DEEP15 窓数=", Length(DEEP15), " (期待 15) ===\n");
deep15Count15 := (Length(DEEP15) = 15);;

## ================= [B''-0] 各窓の土台量測定 =================
WindowB0Rec := function(idx, entryFix)
  local W, Qgrp, PNfull, qSize, pnFullSize, zFull, z0, Dcomm, DcommIndex, D1, D0, d1Size, d0Size;
  W := BuildWindowFromWords(entryFix.index, entryFix.words);;
  Qgrp := W.PN;;
  PNfull := Subgroup(W.Bq, [W.x, W.y, W.c]);;
  qSize := Size(Qgrp);;
  pnFullSize := Size(PNfull);;
  zFull := Order(W.c);;
  z0 := Index(PNfull, Qgrp);;
  Dcomm := DerivedSubgroup(Qgrp);;
  DcommIndex := Index(Qgrp, Dcomm);;
  D1 := Intersection(Centralizer(W.Bq, W.s1), Qgrp);;
  D0 := Intersection(D1, Dcomm);;
  d1Size := Size(D1);;
  d0Size := Size(D0);;
  return rec(
    slot := idx, id := entryFix.id, index := entryFix.index,
    bq_order := Size(W.Bq), n_ord := W.Nord,
    q_size := qSize, pn_full_size := pnFullSize,
    z_full_ord_cbar := zFull, z0 := z0,
    dcomm_size := Size(Dcomm), dcomm_index := DcommIndex,
    d1_size := d1Size, d0_size := d0Size,
    d0_ge_4 := (d0Size >= 4), z0_gt_1 := (z0 > 1)
  );;
end;;

results := [];;
sIdx := 0;;
for entryFix in DEEP15 do
  sIdx := sIdx + 1;;
  Print("\n--- 窓 ", sIdx, "/", Length(DEEP15), " id=", entryFix.id, " index=", entryFix.index, " ---\n");
  r := WindowB0Rec(sIdx, entryFix);;
  Print("  |Q|=", r.q_size, " |PN_full|=", r.pn_full_size, " z0=", r.z0,
        " |[Q,Q]|=", r.dcomm_size, " |D1|=", r.d1_size, " |D0|=", r.d0_size, "\n");
  Add(results, r);;
od;;

## ================= K^(9) 対照 =================
Print("\n=== K^(9) 対照 ===\n");
Print("  UNKNOWN_BLOCKED -- 既報(search/iset4_bprime_v1.g / search/certs/iset4_remeasure_v1_20260813.json):\n");
Print("  sigma1 の実像を持つ B3 内実現が現行コードベースに存在しない(search/k9-package.g の\n");
Print("  BuildPn(9) は抽象 dihedral-wreath モデルで X=sigma1^2,Y=sigma2^2 のみ)。\n");

## ================= 選抜集計 =================
selD0ge4 := Filtered(results, r -> r.d0_ge_4);;
selZ0gt1 := Filtered(results, r -> r.z0_gt_1);;
Print("\n=== 選抜結果 ===\n");
Print("  |D_0|>=4 窓 (slot, id): ", List(selD0ge4, r -> [r.slot, r.id]), "\n");
Print("  z_0>1 窓 (slot, id): ", List(selZ0gt1, r -> [r.slot, r.id]), "\n");

## ================= JSON output =================
JWinRec := function(r)
  return Concatenation("{\"slot\":", String(r.slot), ",\"id\":", JArr(List(r.id, String)),
    ",\"index\":", String(r.index), ",\"bq_order\":", String(r.bq_order), ",\"n_ord\":", String(r.n_ord),
    ",\"q_size\":", String(r.q_size), ",\"pn_full_size\":", String(r.pn_full_size),
    ",\"z_full_ord_cbar\":", String(r.z_full_ord_cbar), ",\"z0\":", String(r.z0),
    ",\"dcomm_size\":", String(r.dcomm_size), ",\"dcomm_index\":", String(r.dcomm_index),
    ",\"d1_size\":", String(r.d1_size), ",\"d0_size\":", String(r.d0_size),
    ",\"d0_ge_4\":", JB(r.d0_ge_4), ",\"z0_gt_1\":", JB(r.z0_gt_1), "}");
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_b0sweep.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/iset4_b0_sweep_v1.g");;
wordsSha256 := ComputeSha256File("search/iso_census83_deep15_data.g");;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/iset4_d0_survey/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/iset4_b0_sweep_v1.g\",\"order\":\"裁定1118(実装係タスク1・[B''-0])\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/u6_prereg_readout_v1.md §4 [B''-0]\"",
  ",\"deep15_count_check\":{\"count\":", String(Length(DEEP15)), ",\"expected_15\":", JB(deep15Count15), "},",
  "\"windows\":[", JoinC(List(results, JWinRec), ","), "],",
  "\"k9_control\":{\"status\":\"UNKNOWN_BLOCKED\",",
    "\"reason\":\"sigma1 の実像を持つ B3 内実現が現行コードベースに存在しない(search/k9-package.g の BuildPn(9) は X=sigma1^2,Y=sigma2^2 のみを直接構成する抽象 dihedral-wreath モデルで、sigma1 自身の実像もB3との具体的な埋め込みも持たない)。既報(search/iset4_bprime_v1.g, cert iset4_remeasure_v1_20260813)と同一障害のため再報告せず記帳のみ。\"},",
  "\"selection\":{",
    "\"d0_ge_4_slots\":", JArr(List(selD0ge4, r -> String(r.slot))), ",",
    "\"d0_ge_4_ids\":[", JoinC(List(selD0ge4, r -> JArr(List(r.id, String))), ","), "],",
    "\"z0_gt_1_slots\":", JArr(List(selZ0gt1, r -> String(r.slot))), ",",
    "\"z0_gt_1_ids\":[", JoinC(List(selZ0gt1, r -> JArr(List(r.id, String))), ","), "]",
  "},",
  "\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\",\"deep15_data_sha256\":\"", wordsSha256, "\"}",
  "}"
);;

outPath := "search/certs/iset4_b0_sweep_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
