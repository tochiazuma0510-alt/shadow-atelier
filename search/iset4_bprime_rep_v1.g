## search/iset4_bprime_rep_v1.g -- [B''] 反復: 3窓(twin [1152,154161]/[1152,154163] + z0>1対照[1134,55])
## への iset4_remeasure_spec_v1.md §3 [B'] プロトコル適用(裁定1119・実装係タスク[B''])
##
## 正本: docs/notes/iset4_remeasure_spec_v1.md §3 [B'] (プロトコルそのまま流用・窓だけ差替)
##       docs/notes/u6_prereg_readout_v1.md §4 [B''] (対象窓の選抜根拠)
## 対象: (1)(2) [1152,154161] slot9 と [1152,154163] slot10 (|D_0|=4 の双子・DEEP15 内)
##       (3) [1134,55] slot5 (z_0=3・型退化対照)
## 追加要請(裁定1119): 双子窓の D_0\{1} の3非自明元それぞれについて、shadow ごとの
##   (C,S,H) 3分類を per-element で記録する。
##
## 規律: u/c 非接触・封印非接触・prereg 非抵触。判定語なし・cert は生値のみ。
##   D_1 := C_Q(sigma1-bar) = C_{B3/N}(sigma1-bar) ∩ Q (Q 内・PN でない)。D_0 := D_1 ∩ [Q,Q]。
##   [1134,55] は |D_0|=1(自明)と probe で既知 ⟹ spec §3 の早期打ち切り規約により
##   RIGID については "空虚" だが、機械の健全性検査(W1-W3)としては full scan を実施する。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0Global := GAPLIB_WallElapsedMs();;

## ================= (F2) machinery, VERBATIM from search/iset4_bprime_v1.g =================
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
  return MakeWindow(s1, s2);;
end;;

BInt := function(bb) if bb then return 1; else return 0; fi; end;;
PatIdx := function(cc,ss,hh) return (BInt(cc))*4 + (BInt(ss))*2 + (BInt(hh)) + 1; end;;

## ================= [B'] full protocol on one window =================
RunBPrimeOnWindow := function(label, entryFix)
  local W, Qgrp, PNfull, qSize, pnFullSize, zFull, z0, Dcomm, DcommIndex, D1, D0, d1Size, d0Size,
        d0IsTrivial, charmingSetFix, corrFix, shadowsFix, QElts, patternCounts, perShadow,
        sepIndicatorHits, w1Detail, w2AllPass, w3Violations, D0nontrivElts, perElementRecs,
        sIdx, sh, m, f, u, survQ, q, g, genA, genB, Cval, Sval, Hval, hTheta, hTau, mVals, NmByM,
        w1AllUniform, w3AllPass, elt, eltRecs, tScan0, tScan1, result;

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
  d0IsTrivial := (d0Size = 1);;
  D0nontrivElts := Filtered(Elements(D0), x -> x <> Identity(Qgrp));;

  Print("\n############################################################\n");
  Print("# 窓: ", label, "  id=", entryFix.id, "\n");
  Print("############################################################\n");
  Print("  |Q|=", qSize, " |PN_full|=", pnFullSize, " z0=", z0, " |[Q,Q]|=", Size(Dcomm),
        " |D1|=", d1Size, " |D0|=", d0Size, " (D0\\{1} has ", Length(D0nontrivElts), " elements)\n");

  charmingSetFix := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
  corrFix := CorrectedShadows(W, charmingSetFix);;
  shadowsFix := List(corrFix, sh -> rec(m := sh[1], f := sh[2]));;
  Print("  shadow_total=", Length(shadowsFix), "\n");

  QElts := Elements(Qgrp);;
  patternCounts := List([1..8], i -> 0);;
  perShadow := [];;
  sepIndicatorHits := [];;
  w1Detail := [];;
  w2AllPass := true;;
  w3Violations := [];;
  ## per-element (D0\{1}) records: for each nontrivial D0 element, list of (m, f_string, C,S,H)
  perElementRecs := List(D0nontrivElts, elt -> rec(q_string := String(elt), per_shadow := []));;

  tScan0 := GAPLIB_WallElapsedMs();;
  sIdx := 0;;
  for sh in shadowsFix do
    sIdx := sIdx + 1;;
    if GAPLIB_CheckCap(500.0, Concatenation("bprime-rep-scan-", label, "-", String(sIdx))) then
      Print("[CAP WARNING] stopping full scan at shadow ", sIdx, " for window ", label, "\n");
      break;
    fi;
    m := sh.m;;  f := sh.f;;  u := 2*m + 1;;
    survQ := [];;
    for q in QElts do
      g := AbstractProd([f, q]);;
      Cval := (g in Dcomm);;
      genA := W.s1^u;;
      genB := AbstractProd([g^-1, W.s2^u, g]);;
      Sval := (Size(Group(genA, genB)) = Size(W.Bq));;
      hTheta := (AbstractProd([g, TH(W, g)]) = Identity(W.Bq));;
      hTau := (RtOf(W, m, g) = W.c^m);;
      Hval := hTheta and hTau;;
      patternCounts[PatIdx(Cval, Sval, Hval)] := patternCounts[PatIdx(Cval, Sval, Hval)] + 1;;
      if Cval and Sval and Hval then
        Add(survQ, q);;
      fi;
      if not (q in Dcomm) then
        if Cval or (Cval and Sval and Hval) then
          Add(w3Violations, rec(m := m, f_string := String(f), q_string := String(q)));
        fi;
      fi;
      if (q in D0) and (q <> Identity(Qgrp)) and Cval and (not Hval) then
        Add(sepIndicatorHits, rec(m := m, f_string := String(f), q_string := String(q)));
      fi;
      ## per-element (D0\{1}) recording
      if q in D0nontrivElts then
        for elt in perElementRecs do
          if elt.q_string = String(q) then
            Add(elt.per_shadow, rec(m := m, f_string := String(f), c := Cval, s := Sval, h := Hval));
          fi;
        od;
      fi;
    od;
    if not (Identity(Qgrp) in survQ) then w2AllPass := false; fi;
    Add(w1Detail, rec(m := m, f_string := String(f), surv_count := Length(survQ)));
    Add(perShadow, rec(m := m, f_string := String(f), survive_count := Length(survQ),
      surv_q_strings := List(survQ, String),
      surv_in_d1 := Filtered(survQ, q -> q in D1), surv_in_d0 := Filtered(survQ, q -> q in D0)));
  od;
  tScan1 := GAPLIB_WallElapsedMs();;

  mVals := Set(List(w1Detail, r -> r.m));;
  NmByM := List(mVals, mm -> rec(m := mm,
    counts := Set(List(Filtered(w1Detail, r -> r.m = mm), r -> r.surv_count))));;
  w1AllUniform := ForAll(NmByM, r -> Length(r.counts) = 1);;
  w3AllPass := (Length(w3Violations) = 0);;

  ## per-element pattern histograms
  for elt in perElementRecs do
    elt.pattern_histogram := List([1..8], i -> 0);;
    for sh in elt.per_shadow do
      elt.pattern_histogram[PatIdx(sh.c, sh.s, sh.h)] := elt.pattern_histogram[PatIdx(sh.c, sh.s, sh.h)] + 1;;
    od;
  od;

  result := rec(
    label := label, id := entryFix.id, index := entryFix.index,
    bq_order := Size(W.Bq), n_ord := W.Nord,
    q_size := qSize, pn_full_size := pnFullSize, z_full_ord_cbar := zFull, z0 := z0,
    dcomm_size := Size(Dcomm), dcomm_index := DcommIndex, d1_size := d1Size, d0_size := d0Size,
    d0_is_trivial := d0IsTrivial, d0_nontrivial_count := Length(D0nontrivElts),
    shadow_total := Length(shadowsFix),
    scan_elapsed_ms := tScan1 - tScan0,
    scan_shadows_completed := Length(perShadow),
    pattern_histogram := patternCounts,
    per_shadow := perShadow,
    n_m_by_m := NmByM, w1_all_uniform := w1AllUniform,
    w2_identity_survives_all := w2AllPass,
    w3_violations := w3Violations, w3_all_pass := w3AllPass,
    d_separation_indicator_hits := sepIndicatorHits,
    per_element_d0_nontrivial := perElementRecs
  );;
  return result;;
end;;

Read("search/iso_census83_deep15_data.g");;

Print("############################################################\n");
Print("# iset4_bprime_rep_v1.g -- [B''] 反復(裁定1119)\n");
Print("############################################################\n");

targets := [
  rec(slot := 9,  label := "[1152,154161]"),
  rec(slot := 10, label := "[1152,154163]"),
  rec(slot := 5,  label := "[1134,55] (z0>1 type-degeneracy control)")
];;

allResults := [];;
for tgt in targets do
  entryFix := DEEP15[tgt.slot];;
  res := RunBPrimeOnWindow(tgt.label, entryFix);;
  Add(allResults, res);;
od;;

## ================= JSON output =================
JPerShadowRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"survive_count\":", String(r.survive_count),
    ",\"surv_q_strings\":", JArr(List(r.surv_q_strings, JStr)),
    ",\"surv_in_d1\":", JArr(List(r.surv_in_d1, x -> JStr(String(x)))),
    ",\"surv_in_d0\":", JArr(List(r.surv_in_d0, x -> JStr(String(x)))), "}");
end;;

JW3ViolationRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"q_perm_string\":", JStr(r.q_string), "}");
end;;

JSepHitRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"q_perm_string\":", JStr(r.q_string), "}");
end;;

JNmRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"distinct_surv_counts\":",
    JArr(List(r.counts, String)), ",\"uniform\":", JB(Length(r.counts)=1), "}");
end;;

JPerShadowCSHRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"c\":", JB(r.c), ",\"s\":", JB(r.s), ",\"h\":", JB(r.h), "}");
end;;

JPerElementRec := function(r)
  return Concatenation("{\"q_perm_string\":", JStr(r.q_string),
    ",\"pattern_histogram_csh_bitindex_1to8\":", JArr(List(r.pattern_histogram, String)),
    ",\"per_shadow_csh\":[", JoinC(List(r.per_shadow, JPerShadowCSHRec), ","), "]}");
end;;

JWindowResultRec := function(r)
  return Concatenation(
    "{\"label\":", JStr(r.label), ",\"id\":", JArr(List(r.id, String)), ",\"index\":", String(r.index), ",",
    "\"bq_order\":", String(r.bq_order), ",\"n_ord\":", String(r.n_ord), ",",
    "\"q_size\":", String(r.q_size), ",\"pn_full_size\":", String(r.pn_full_size), ",",
    "\"z_full_ord_cbar\":", String(r.z_full_ord_cbar), ",\"z0\":", String(r.z0), ",",
    "\"dcomm_size\":", String(r.dcomm_size), ",\"dcomm_index\":", String(r.dcomm_index), ",",
    "\"d1_size\":", String(r.d1_size), ",\"d0_size\":", String(r.d0_size), ",",
    "\"d0_is_trivial\":", JB(r.d0_is_trivial), ",\"d0_nontrivial_count\":", String(r.d0_nontrivial_count), ",",
    "\"shadow_total\":", String(r.shadow_total), ",",
    "\"scan_elapsed_ms\":", String(r.scan_elapsed_ms), ",",
    "\"scan_shadows_completed\":", String(r.scan_shadows_completed), ",",
    "\"scan_shadows_completed_matches_total\":", JB(r.scan_shadows_completed = r.shadow_total), ",",
    "\"pattern_histogram_csh_bitindex_1to8\":", JArr(List(r.pattern_histogram, String)), ",",
    "\"per_shadow\":[", JoinC(List(r.per_shadow, JPerShadowRec), ","), "],",
    "\"n_m_by_m\":[", JoinC(List(r.n_m_by_m, JNmRec), ","), "],",
    "\"w1_surv_exact\":{\"all_uniform\":", JB(r.w1_all_uniform), "},",
    "\"w2_identity_survives\":{\"all_pass\":", JB(r.w2_identity_survives_all), "},",
    "\"w3_charming_regression\":{\"all_pass\":", JB(r.w3_all_pass), ",\"violation_count\":", String(Length(r.w3_violations)),
      ",\"violations\":[", JoinC(List(r.w3_violations, JW3ViolationRec), ","), "]},",
    "\"d_separation_indicator\":{\"hit_count\":", String(Length(r.d_separation_indicator_hits)), ",",
      "\"hits\":[", JoinC(List(r.d_separation_indicator_hits, JSepHitRec), ","), "]},",
    "\"per_element_d0_nontrivial\":[", JoinC(List(r.per_element_d0_nontrivial, JPerElementRec), ","), "]",
    "}"
  );
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_bprimerep.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/iset4_bprime_rep_v1.g");;
wordsSha256 := ComputeSha256File("search/iso_census83_deep15_data.g");;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/iset4_bprime_rep/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/iset4_bprime_rep_v1.g\",\"order\":\"裁定1119([B'']反復)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/iset4_remeasure_spec_v1.md §3 [B']・docs/notes/u6_prereg_readout_v1.md §4 [B'']\"",
  ",\"windows\":[", JoinC(List(allResults, JWindowResultRec), ","), "],",
  "\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\",\"deep15_data_sha256\":\"", wordsSha256, "\"}",
  "}"
);;

outPath := "search/certs/iset4_bprime_rep_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
