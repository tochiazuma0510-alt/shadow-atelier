## search/at2_p2_m_isolated_v1.g -- AT-2 P2 補測: M isolated の実測(裁定1114)
##
## 正本: docs/notes/set_surgery_vetting_v1.md §11.4 定理 SUBTOR(前提: M isolated)。
##   isolated(Def 3.13, 定義ノート L173): GT(M) の全 shadow が settled(ker(T_{m,f})=M)。
##   settled かどうかは marked-factor-map 法(search/set_surgery_fixture_v1.g の
##   ClassifyByMarkedFactorMap、裁定1082で確立・#C(N)=2実測で実績あり)で判定する:
##     ker(T_{m,f}) = ker(T_{m',f'}) <=> exists alpha in Aut(Q_M): 対角作用で
##     (genA,genB)=(x^u, f^-1 y^u f) の対が一致する軌道 (第一同型定理の標準的帰結)。
##   identity shadow [0,1](genA=x_M, genB=y_M)の類 = ker=M そのものの類(settled 定義そのもの)
##   ⟹ settled shadow の個数 = identity と同じ類のサイズ、#C(M)=1 なら isolated。
##
## 入力: search/at2_p2_quantization_v1.g で構成済みの M=ker(rho)(|B3:M|=7056)・
##   GT(M)の288 shadow(COMPLETE 実測済み)。本 script は同じ構成を独立に再実行する
##   (前 script の中間変数を import しない -- 探索器内の同一手法の再利用であり、
##   照合器との分離とは無関係)。
##
## 規律: u/c 非接触・封印非接触・prereg 非抵触。判定語なし・cert は生値のみ。

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
Print("# at2_p2_m_isolated_v1.g -- M=ker(rho) isolated の実測(裁定1114)\n");
Print("############################################################\n");

Print("\n=== N=[1008,521] slot1: 窓 + 48 shadow ===\n");
Read("search/iso_census83_deep15_data.g");;
entryFix := DEEP15[1];;
if entryFix.id <> [1008, 521] then Error("mismatch"); fi;
built := BuildWindowFromWords(entryFix.index, entryFix.words);;
W := built.W;;  Nsub := built.N;;
charmingSetFix := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
corrFix := CorrectedShadows(W, charmingSetFix);;
shadowsFix := List(corrFix, sh -> rec(m := sh[1], f := sh[2]));;
if Length(shadowsFix) <> 48 then Error("shadow_total != 48"); fi;

Print("\n=== M := ker(rho) の再構成(独立実行) ===\n");
nonsettledRep := First(shadowsFix, sh -> sh.m = 2);;
mRep := nonsettledRep.m;;  fRep := nonsettledRep.f;;
uRep := 2*mRep + 1;;
genA_T := W.s1^uRep;;
genB_T := AbstractProd([fRep^-1, W.s2^uRep, fRep]);;
DP := DirectProduct(W.Bq, W.Bq);;
e1 := Embedding(DP, 1);;
e2 := Embedding(DP, 2);;
imgA := Image(e1, W.s1) * Image(e2, genA_T);;
imgB := Image(e1, W.s2) * Image(e2, genB_T);;
rhoHom := GroupHomomorphismByImages(B3, DP, [ga, gb], [imgA, imgB]);;
if rhoHom = fail then Error("rho construction failed"); fi;
Mker := Kernel(rhoHom);;
indexBOverM := Index(B3, Mker);;
Print("  |B3:M| = ", indexBOverM, " (期待 7056)\n");
if indexBOverM <> 7056 then
  Print("[ANOMALY] |B3:M| != 7056 -- recording as-is\n");
fi;

WM := MakeWindow(imgA, imgB);;
Print("  |Bq_M|=", Size(WM.Bq), " |Q_M|=", Size(WM.PN), " Nord_M=", WM.Nord, "\n");

Print("\n=== GT(M) 全数列挙(裁定1107の cert と同一手続き・独立再実行) ===\n");
charmingSetM := Filtered([0 .. WM.Nord - 1], mm -> Gcd(2*mm+1, WM.Nord) = 1);;
tGT0 := GAPLIB_WallElapsedMs();;
corrM := CorrectedShadows(WM, charmingSetM);;
tGT1 := GAPLIB_WallElapsedMs();;
shadowsM := List(corrM, sh -> rec(m := sh[1], f := sh[2]));;
Print("  GT(M) shadow_total=", Length(shadowsM), " (期待 288, at2_p2_quantization_v1 cert と突合)  elapsed_ms=", tGT1-tGT0, "\n");
shadowTotalMatches288 := (Length(shadowsM) = 288);;

Print("\n=== settled 判定: 誘導自己準同型の well-definedness(Aut(Q_M) 列挙は使わない) ===\n");
## 方法(marked-factor-map/AutomorphismGroupより軽い・数学的に同値):
##   rho: B3 ->> Bq_M(全射・ker=M、既に構成済み)。T_{m,f}: B3 -> Bq_M もまた
##   準同型(genA,genB が hexagon を満たすことは CorrectedShadows で確認済み)。
##   Bq_M = Group(imgA,imgB) = B3/M の具体表現なので、誘導写像
##     phi: Bq_M -> Bq_M,  imgA |-> genA(shadow), imgB |-> genB(shadow)
##   が GAP の GroupHomomorphismByImages で well-defined に構成できることは、
##   Bq_M の関係式(=M の生成する語)がすべて (genA,genB) でも成り立つことと同値
##   ⟹ well-defined <=> M subseteq ker(T_{m,f})。両辺の指数は 7056 で共通(生成条件
##   S により T_{m,f} は全射)ゆえ、有限指数部分群の包含+指数一致 ⟹ 相等、すなわち
##   well-defined <=> settled(ker(T_{m,f})=M)。AutomorphismGroup(Q_M)(位数1176、
##   メモリ上限到達で実測不能)を経由しないので秒級で済む。
tCl0 := GAPLIB_WallElapsedMs();;
settledDetail := [];;
settledCountM := 0;;
identityIdx := 0;;
sIdxM := 0;;
for sh in shadowsM do
  sIdxM := sIdxM + 1;;
  if sh.m = 0 and sh.f = Identity(WM.PN) then identityIdx := sIdxM;; fi;
  uu := 2*sh.m + 1;;
  genA := WM.s1^uu;;
  genB := AbstractProd([sh.f^-1, WM.s2^uu, sh.f]);;
  phi := GroupHomomorphismByImages(WM.Bq, WM.Bq, [imgA, imgB], [genA, genB]);;
  isSettled := (phi <> fail);;
  if isSettled then settledCountM := settledCountM + 1;; fi;
  Add(settledDetail, rec(m := sh.m, f_string := String(sh.f), settled := isSettled));;
od;
tCl1 := GAPLIB_WallElapsedMs();;
if identityIdx = 0 then Error("could not locate the [0,1] identity shadow among GT(M)'s shadows"); fi;
Print("  identity shadow index=", identityIdx, " settled=", settledDetail[identityIdx].settled,
      " (must be true by definition -- ker(T_{0,1})=M tautologically)\n");
if not settledDetail[identityIdx].settled then
  Error("identity shadow reported NOT settled -- implementation bug, refusing to proceed silently");
fi;
mIsIsolated := (settledCountM = Length(shadowsM));;
Print("  settled_count = ", settledCountM, " / ", Length(shadowsM), "  elapsed_ms=", tCl1-tCl0, "\n");
Print("  M isolated (Def 3.13: 全 shadow settled) <=> settled_count = shadow_total: ", mIsIsolated, "\n");

nonSettledDetail := Filtered(settledDetail, r -> not r.settled);;
Print("  non-settled shadow count: ", Length(nonSettledDetail), "\n");
for r in nonSettledDetail{[1 .. Minimum(10, Length(nonSettledDetail))]} do
  Print("    m=", r.m, "\n");
od;

## ================= JSON output =================
JClassRec := function(c)
  return Concatenation("{\"class_index\":", String(c.rep_index), ",\"size\":", String(c.size),
    ",\"rep_m\":", String(c.rep_m), ",\"rep_f_perm_string\":", JStr(c.rep_f_string), "}");
end;;

JNonSettledRec := function(r)
  return Concatenation("{\"class_index\":", String(r.class_index), ",\"size\":", String(r.size),
    ",\"rep_m\":", String(r.rep_m), ",\"rep_f_perm_string\":", JStr(r.rep_f_string), "}");
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_misol.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/at2_p2_m_isolated_v1.g");;
wordsSha256 := ComputeSha256File("search/iso_census83_deep15_data.g");;

JSettledDetailRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"settled\":", JB(r.settled), "}");
end;;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/at2_p2_m_isolated/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/at2_p2_m_isolated_v1.g\",\"order\":\"裁定1114(AT-2 P2 SUBTOR前提 M isolated 補測)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/set_surgery_vetting_v1.md §11.4(定理SUBTORの前提 M isolated)\"",
  ",\"method_note\":\"settled(ker(T_mf)=M) を、Aut(Q_M) 列挙(marked-factor-map、|Q_M|=1176 でメモリ上限到達・実測不能だった)ではなく、誘導自己準同型 phi:Bq_M->Bq_M (imgA|->genA, imgB|->genB) の GroupHomomorphismByImages well-definedness で判定した。根拠: rho:B3->>Bq_M は全射・ker=M(既知)。phi が well-defined に構成できることは、Bq_M=B3/M の全ての関係式(=M の生成する語)が (genA,genB) でも成立することと同値、すなわち M subseteq ker(T_mf)。T_mf は shadow 条件(生成条件S)により全射ゆえ index(ker(T_mf))=index(M)=7056 で共通 -- 有限指数部分群の包含+指数一致は相等を意味するので well-defined <=> settled。identity shadow(ker=M自明)で settled=true を確認済み(不変条件チェック)。\",",
  "\"window_m\":{\"index_b3_over_m\":", String(indexBOverM), ",\"bq_m_order\":", String(Size(WM.Bq)),
    ",\"q_m_order\":", String(Size(WM.PN)), ",\"nord_m\":", String(WM.Nord), "},",
  "\"gt_m_enumeration\":{\"shadow_total\":", String(Length(shadowsM)),
    ",\"matches_288_from_quantization_cert\":", JB(shadowTotalMatches288),
    ",\"elapsed_ms\":", String(tGT1-tGT0), "},",
  "\"settled_measurement\":{\"identity_shadow_index\":", String(identityIdx),
    ",\"identity_shadow_settled\":", JB(settledDetail[identityIdx].settled),
    ",\"settled_count\":", String(settledCountM),
    ",\"shadow_total\":", String(Length(shadowsM)),
    ",\"m_isolated_settled_count_eq_total\":", JB(mIsIsolated),
    ",\"elapsed_ms\":", String(tCl1-tCl0),
    ",\"non_settled_count\":", String(Length(nonSettledDetail)),
    ",\"non_settled_detail\":[", JoinC(List(nonSettledDetail, JSettledDetailRec), ","), "],",
    "\"full_detail\":[", JoinC(List(settledDetail, JSettledDetailRec), ","), "]},",
  "\"u_touched\":true,\"u_touch_note\":\"u=2m+1 charming coordinate reused from existing shadow marking, not the sealed K(5) instance quantity\",",
  "\"c_touched\":false,",
  "\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\",\"deep15_data_sha256\":\"", wordsSha256, "\"}",
  "}"
);;

outPath := "search/certs/at2_p2_m_isolated_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
