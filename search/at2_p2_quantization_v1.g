## search/at2_p2_quantization_v1.g -- AT-2 P2 第二段: R-trace 量子化検定(裁定1107・実装係続行)
##
## 正本: docs/notes/ideas_arith_torsor_v1.md AT-2 P2 節 + docs/notes/set_surgery_vetting_v1.md
##   §12.2(P2は「設計妥当・採用」)・§11(定理 SUBTOR・補題 R-MULT/DIFF-S)。
##
## 手順(司令塔便どおり):
##   1. M := ker(rho)(search/at2_p2_imrho_v1.g で構成済・|B3:M|=7056)を窓として GT(M) を列挙。
##   2. R_{M,N}(座標 truncation, (3.60))で N=[1008,521]^1 側へ押し出す。
##   3. N の核類(#C=2・search/certs/set_surgery_fixture_v1_20260813.json の分類)ごとに
##      trace_K := X cap GTSh(K,N) のサイズを実測(X:=R_{M,N}(GT(M)))。
##
## ★ 構成上の効率化(数学的に正当): rho:=(pi_N,T_mf):B3->(Bq_N x Bq_K2)=(Bq_N x Bq_N)
##   (両成分が同じ有限標的 Bq_N=B3/N への写像であることに注意)の像 Im(rho)=DP の部分群が、
##   まさに B3/M の自然な置換表現である(第一同型定理: B3/ker(rho) ~= Im(rho))。よって
##   W_M の s1,s2 は NaturalHomomorphismByNormalSubgroup を再度呼ぶ必要がなく、rho の
##   生成元の像(imgA,imgB、DP=Bq_N x Bq_N 内)をそのまま使える。R_{M,N} の f 成分は
##   DP の第1成分への射影(Projection(DP,1))そのもの -- pi_N がまさに rho の第1成分
##   だったから、これは定義から従う(座標 truncation の具体形)。
##
## 規律: u/c 非接触・封印非接触・prereg 非抵触。判定語なし・cert は生値のみ。
##   全列挙が重ければ PARTIAL 許容(部分列挙でも trace サイズは出る)・cert に明記。

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

## capped variant for possibly-large windows (GT(M)): iterates f in D, checks cap after each f;
## returns rec(shadows, complete, f_scanned, f_total)
CorrectedShadowsCapped := function(W, charmingSet, capSec, tag)
  local out, f, m, u, Delts, i, capped;
  out := [];
  Delts := Elements(DerivedSubgroup(W.PN));;
  capped := false;;
  for i in [1 .. Length(Delts)] do
    if GAPLIB_CheckCap(capSec, Concatenation(tag, "-f", String(i))) then
      Print("[CAP WARNING] ", tag, ": stopping f-loop at f-index ", i, "/", Length(Delts), "\n");
      capped := true;
      break;
    fi;
    f := Delts[i];;
    if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m + 1;
      if RtOf(W, m, f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out, [m, f]);
    od;
  od;
  return rec(shadows := Set(out), complete := (not capped), f_scanned := Minimum(i, Length(Delts)),
             f_total := Length(Delts));
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

## marked-factor-map kernel classification, VERBATIM from search/set_surgery_fixture_v1.g
ClassifyByMarkedFactorMap := function(qrec, shadowList)
  local pairs, i, j, gA, gB, hA, hB, Aut, autElts, classes, assigned, members, found, al, out;
  pairs := List(shadowList, sh -> rec(m := sh.m, f := sh.f,
                genA := qrec.x^(2*sh.m+1),
                genB := AbstractProd([sh.f^-1, qrec.y^(2*sh.m+1), sh.f])));;
  Aut := AutomorphismGroup(qrec.PN);;
  autElts := Elements(Aut);;
  classes := [];;
  assigned := List([1 .. Length(pairs)], k -> false);;
  for i in [1 .. Length(pairs)] do
    if assigned[i] then continue; fi;
    gA := pairs[i].genA;;  gB := pairs[i].genB;;
    members := [i];;
    assigned[i] := true;;
    for j in [i+1 .. Length(pairs)] do
      if assigned[j] then continue; fi;
      hA := pairs[j].genA;;  hB := pairs[j].genB;;
      found := false;;
      for al in autElts do
        if Image(al, gA) = hA and Image(al, gB) = hB then found := true; break; fi;
      od;
      if found then Add(members, j); assigned[j] := true; fi;
    od;
    Add(classes, rec(rep_index := i, size := Length(members), members := members,
                      rep_m := pairs[i].m, rep_f_string := String(pairs[i].f)));;
  od;
  out := rec(shadow_total := Length(pairs), aut_pn_order := Size(Aut),
             num_classes := Length(classes), classes := classes, pairs := pairs);;
  return out;
end;;

Print("############################################################\n");
Print("# at2_p2_quantization_v1.g -- P2第二段: R-trace量子化検定\n");
Print("############################################################\n");

Print("\n=== N=[1008,521] slot1: 窓 + 48 shadow + #C=2 分類 ===\n");
Read("search/iso_census83_deep15_data.g");;
entryFix := DEEP15[1];;
if entryFix.id <> [1008, 521] then Error("mismatch"); fi;
built := BuildWindowFromWords(entryFix.index, entryFix.words);;
W := built.W;;  Nsub := built.N;;
Print("  |Bq_N|=", Size(W.Bq), " |Q_N|=", Size(W.PN), " Nord_N=", W.Nord, "\n");

charmingSetFix := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
corrFix := CorrectedShadows(W, charmingSetFix);;
shadowsFix := List(corrFix, sh -> rec(m := sh[1], f := sh[2]));;
if Length(shadowsFix) <> 48 then Error("shadow_total != 48"); fi;

qrecN := rec(x := W.x, y := W.y, PN := W.PN);;
classN := ClassifyByMarkedFactorMap(qrecN, shadowsFix);;
Print("  #C(N)=", classN.num_classes, " class_sizes=", List(classN.classes, c -> c.size), "\n");
if classN.num_classes <> 2 then Error("expected #C(N)=2, got ", classN.num_classes); fi;

## classOfShadowIndex[i] = 1 or 2 (which classN.classes entry contains shadow index i)
classOfShadowIndex := List([1 .. Length(shadowsFix)], k -> 0);;
for ci in [1 .. Length(classN.classes)] do
  for mIdx in classN.classes[ci].members do
    classOfShadowIndex[mIdx] := ci;;
  od;
od;
## identify the settled class: contains (m=0, f=Identity(Q_N))
settledIdx := 0;;
for i in [1 .. Length(shadowsFix)] do
  if shadowsFix[i].m = 0 and shadowsFix[i].f = Identity(W.PN) then settledIdx := i;; fi;
od;
if settledIdx = 0 then Error("could not locate the [0,1] identity shadow among the 48"); fi;
settledClass := classOfShadowIndex[settledIdx];;
Print("  identity shadow [0,1] is shadow-index ", settledIdx, ", class ", settledClass, " (= settled class, size ",
      classN.classes[settledClass].size, ")\n");

Print("\n=== M := ker(rho): rho=(pi_N,T_mf):B3 -> Bq_N x Bq_N の再構成 ===\n");
nonsettledRep := First(shadowsFix, sh -> sh.m = 2);;
mRep := nonsettledRep.m;;  fRep := nonsettledRep.f;;
uRep := 2*mRep + 1;;
genA_T := W.s1^uRep;;
genB_T := AbstractProd([fRep^-1, W.s2^uRep, fRep]);;
TmfB3Hom := GroupHomomorphismByImages(B3, W.Bq, [ga, gb], [genA_T, genB_T]);;
if TmfB3Hom = fail then Error("T_mf construction failed"); fi;

DP := DirectProduct(W.Bq, W.Bq);;
e1 := Embedding(DP, 1);;
e2 := Embedding(DP, 2);;
p1 := Projection(DP, 1);;
imgA := Image(e1, W.s1) * Image(e2, genA_T);;
imgB := Image(e1, W.s2) * Image(e2, genB_T);;
rhoHom := GroupHomomorphismByImages(B3, DP, [ga, gb], [imgA, imgB]);;
if rhoHom = fail then Error("rho construction failed"); fi;
Mker := Kernel(rhoHom);;
indexBOverM := Index(B3, Mker);;
Print("  |B3:M| = ", indexBOverM, " (前回 cert at2_p2_imrho_v1: 7056)\n");
if indexBOverM <> 7056 then
  Print("[ANOMALY] |B3:M| does not match the previously recorded 7056 -- recording as-is, no silent correction\n");
fi;

Print("\n=== W_M の構成(rho の生成元像を直接再利用・NaturalHomomorphismByNormalSubgroup 再実行なし) ===\n");
WM := MakeWindow(imgA, imgB);;
sizeBqM := Size(WM.Bq);;
Print("  |Bq_M| = ", sizeBqM, " (should equal |Im rho| = |B3:M| = ", indexBOverM, ")\n");
bqMMatchesIndex := (sizeBqM = indexBOverM);;
Print("[", PF(bqMMatchesIndex), "] |Bq_M| = |B3:M|: ", bqMMatchesIndex, "\n");
Print("  |Q_M|=", Size(WM.PN), " Nord_M=", WM.Nord, " ord(c_M-bar)=", Order(WM.c), "\n");
nordDivides := (WM.Nord mod W.Nord = 0);;
Print("  Nord_N | Nord_M (truncation precondition): ", nordDivides, "\n");

Print("\n=== GT(M) 列挙 ===\n");
charmingSetM := Filtered([0 .. WM.Nord - 1], mm -> Gcd(2*mm+1, WM.Nord) = 1);;
DsizeM := Size(DerivedSubgroup(WM.PN));;
candidateTotalM := DsizeM * Length(charmingSetM);;
Print("  |[Q_M,Q_M]|=", DsizeM, " |charmingSet_M|=", Length(charmingSetM),
      " candidate_total(f x m)=", candidateTotalM, "\n");

tGT0 := GAPLIB_WallElapsedMs();;
gtMResult := CorrectedShadowsCapped(WM, charmingSetM, 100.0, "gtM");;
tGT1 := GAPLIB_WallElapsedMs();;
shadowsM := List(gtMResult.shadows, sh -> rec(m := sh[1], f := sh[2]));;
Print("  GT(M) shadow_total=", Length(shadowsM), " complete=", gtMResult.complete,
      " (f-scanned ", gtMResult.f_scanned, "/", gtMResult.f_total, ")  elapsed_ms=", tGT1-tGT0, "\n");
gtMStatus := "";;
if gtMResult.complete then gtMStatus := "COMPLETE"; else gtMStatus := "PARTIAL"; fi;
Print("  GT(M) enumeration status: ", gtMStatus, "\n");

Print("\n=== R_{M,N} 押し出し: X := R_{M,N}(GT(M)) を N の 48 shadow へ照合 ===\n");
## R_{M,N}([m,f]) = [m mod Nord_N, projection_1(f)] (座標 truncation (3.60))
pushforwardResults := [];;  ## rec(m_M, m_pushed, matched_index (0 if none), class (0 if unmatched))
unmatchedCount := 0;;
for sh in shadowsM do
  mPushed := sh.m mod W.Nord;;
  fPushed := Image(p1, sh.f);;
  matchedIdx := 0;;
  for i in [1 .. Length(shadowsFix)] do
    if shadowsFix[i].m = mPushed and shadowsFix[i].f = fPushed then matchedIdx := i; break; fi;
  od;
  if matchedIdx = 0 then
    unmatchedCount := unmatchedCount + 1;;
    Add(pushforwardResults, rec(m_M := sh.m, m_pushed := mPushed, matched_index := 0, class := 0));
  else
    Add(pushforwardResults, rec(m_M := sh.m, m_pushed := mPushed, matched_index := matchedIdx,
                                 class := classOfShadowIndex[matchedIdx]));
  fi;
od;
Print("  GT(M) elements pushed forward: ", Length(pushforwardResults), "  unmatched (anomaly)=", unmatchedCount, "\n");

## X := distinct set of matched shadow-indices (image set, NOT counted with multiplicity)
XIndices := Set(Filtered(pushforwardResults, r -> r.matched_index <> 0), r -> r.matched_index);;
XSize := Length(XIndices);;
SXIndices := Filtered(XIndices, i -> classOfShadowIndex[i] = settledClass);;
SXSize := Length(SXIndices);;
Print("  |X| (distinct N-shadows hit) = ", XSize, "  |S_X| (= X cap settled class) = ", SXSize, "\n");

traceByClass := [];;
for ci in [1 .. classN.num_classes] do
  traceIdx := Filtered(XIndices, i -> classOfShadowIndex[i] = ci);;
  traceSize := Length(traceIdx);;
  Add(traceByClass, rec(class_index := ci, class_size := classN.classes[ci].size,
    is_settled_class := (ci = settledClass), trace_size := traceSize, trace_members := traceIdx));;
  Print("  class ", ci, " (size ", classN.classes[ci].size, ", settled=", (ci=settledClass),
        "): trace_size = |X cap GTSh(K,N)| = ", traceSize, "\n");
od;

Print("\n=== 量子化スペクトル突合(生値のみ・判定語なし) ===\n");
Print("  spectrum candidates d|settled(N)|=", classN.classes[settledClass].size, ", #C_X<=", classN.num_classes, "\n");
for r in traceByClass do
  Print("  class ", r.class_index, ": trace=", r.trace_size, "  trace=|S_X|? ", (r.trace_size = SXSize),
        "  trace=0? ", (r.trace_size = 0), "\n");
od;

## ================= JSON output =================
JPushRec := function(r)
  return Concatenation("{\"m_M\":", String(r.m_M), ",\"m_pushed\":", String(r.m_pushed),
    ",\"matched_index\":", String(r.matched_index), ",\"class\":", String(r.class), "}");
end;;

JTraceRec := function(r)
  return Concatenation("{\"class_index\":", String(r.class_index), ",\"class_size\":", String(r.class_size),
    ",\"is_settled_class\":", JB(r.is_settled_class), ",\"trace_size\":", String(r.trace_size),
    ",\"trace_members_shadow_indices\":", JArr(List(r.trace_members, String)), "}");
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_quant.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/at2_p2_quantization_v1.g");;
wordsSha256 := ComputeSha256File("search/iso_census83_deep15_data.g");;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/at2_p2_quantization/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/at2_p2_quantization_v1.g\",\"order\":\"裁定1107(AT-2 P2第二段・実装係続行)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/ideas_arith_torsor_v1.md AT-2 P2 + docs/notes/set_surgery_vetting_v1.md §11-12.2\"",
  ",\"window_n\":{\"id\":[1008,521],\"slot\":1,\"bq_order\":", String(Size(W.Bq)), ",\"q_order\":", String(Size(W.PN)),
    ",\"nord\":", String(W.Nord), ",\"shadow_total\":", String(Length(shadowsFix)),
    ",\"num_classes\":", String(classN.num_classes),
    ",\"class_sizes\":", JArr(List(classN.classes, c -> String(c.size))),
    ",\"settled_class_index\":", String(settledClass), "},",
  "\"window_m\":{\"index_b3_over_m\":", String(indexBOverM),
    ",\"bq_m_order\":", String(sizeBqM), ",\"bq_m_matches_index\":", JB(bqMMatchesIndex),
    ",\"q_m_order\":", String(Size(WM.PN)), ",\"nord_m\":", String(WM.Nord),
    ",\"nord_n_divides_nord_m\":", JB(nordDivides), ",",
    "\"dcomm_m_size\":", String(DsizeM), ",\"charming_set_m_size\":", String(Length(charmingSetM)),
    ",\"candidate_total_m\":", String(candidateTotalM), "},",
  "\"shadow_representative_for_t_mf\":{\"m\":", String(mRep), ",\"u\":", String(uRep), "},",
  "\"gt_m_enumeration\":{\"status\":", JStr(gtMStatus), ",\"complete\":", JB(gtMResult.complete),
    ",\"shadow_total\":", String(Length(shadowsM)),
    ",\"f_scanned\":", String(gtMResult.f_scanned), ",\"f_total\":", String(gtMResult.f_total),
    ",\"elapsed_ms\":", String(tGT1-tGT0), "},",
  "\"pushforward\":{\"total_gt_m_elements\":", String(Length(pushforwardResults)),
    ",\"unmatched_count\":", String(unmatchedCount),
    ",\"unmatched_note\":\"unmatched = R_MN(t) not found among N's 48 known shadows; per (AT-a)/(3.60) this should be 0 -- recorded as an anomaly flag, not silently dropped\",",
    ",\"detail\":[", JoinC(List(pushforwardResults, JPushRec), ","), "]},",
  "\"x_image_set\":{\"x_size\":", String(XSize), ",\"sx_size\":", String(SXSize),
    ",\"x_indices\":", JArr(List(XIndices, String)), ",\"sx_indices\":", JArr(List(SXIndices, String)), "},",
  "\"trace_by_class\":[", JoinC(List(traceByClass, JTraceRec), ","), "],",
  "\"u_touched\":true,\"u_touch_note\":\"u=2m+1 charming coordinate reused from existing shadow marking (same rep as at2_p2_imrho_v1.g), not the sealed K(5) instance quantity\",",
  "\"c_touched\":false,",
  "\"d_no_interpretation\":\"machine values only (raw trace sizes); verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\",\"deep15_data_sha256\":\"", wordsSha256, "\"}",
  "}"
);;

outPath := "search/certs/at2_p2_quantization_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
