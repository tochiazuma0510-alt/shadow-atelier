## search/set_surgery_fixture_v1.g -- 発案6号(集合版手術)fixture 検算2本(裁定1082)
##
## 正本: docs/notes/ideas_set_surgery_v1.md 札 I-SET-1(トーサー分解)・札 I-SET-4(軌道手術の生死)
##   の「検証の一手目」節。
##
## 検算A(札1): 83窓[1008,521]の shadow 全48個を核(ker T_{m,f})で分類し #C(N) を数える。
##   予言: |GT(N)|=|settled(N)|x#C(N) すなわち 48=24x2 -> #C=2。
##
## 【設計判断・重要】ker T_{m,f} の計算法について:
##   naive に PN 上の自己準同型 psi:=GroupHomomorphismByImages(PN,PN,[x,y],[genA,genB]) を
##   構成すると、48個中ちょうど24個で fail (well-defined でない = T が PN へ descent しない)
##   が返る(実測・下記 diagnostics で GAP の GroupHomomorphismByImages の判定と、独立に
##   PN の presentation の relator を代入して直接検算する経路の 2 系統が完全一致=0 mismatch
##   であることを確認済み -- GAP のヒューリスティック失敗ではなく真の非 well-defined 性)。
##   これは既存文書 docs/notes/auto_settled_check_v1.md の 定理OP-SETTLED(settled = descent
##   + 全射)と整合する既知の現象であり、札1自身がこの穴を予期していた
##   (§4 破綻点②「ファイバーのサイズ勘定にペア/写像の型ずれが混入する」)。
##
##   ker T_{m,f} の正しい対象は PN 上の部分群ではなく、抽象自由群 F2 (=PB3/<c>) 上の
##   部分群 K(F2->PNへの hom の kernel、F2 は自由群なので常に well-defined)である。
##   異なる shadow の K が等しいことの判定は、CLAUDE.md/Sol警告「GAP の部分群比較でなく
##   marked factor map を使う」に厳密に従う: F2->>PN の2つの全射 phi1,phi2 に対し
##   Ker(phi1)=Ker(phi2) <=> exists alpha in Aut(PN): phi2 = alpha o phi1
##   (第一同型定理からの標準的事実、逐語: phi1,phi2 が同じ F2/K=PN の2通りの現れなら
##   その差は PN の自己同型に限られる)。したがって「shadow の (genA,genB) の対 in PN x PN
##   への Aut(PN) の対角作用の軌道」= 「shadow の ker T_{m,f} の同値類」と正確に一致する。
##   本 script はこの marked-factor-map 法で分類する(部分群の直接比較は一切行わない)。
##
## 検算B(札4): 同じ fixture で座標捻り [m,f] -> [m,f*q] (q in C_PN(x-bar), C_PN(y-bar),
##   PN 全元) の生存率(捻り後も shadow 条件[domain f in D + hex310 + hex311 + generation]
##   を満たすか)を全数測定する。
##
## 陽性対照: K(9)(isolated, 予言 #C=1・|GT|=108)。frattini_resolution_v2 cert
##   (search/certs/frattini_resolution_v2_20260812.json, row K(9): size_X=108,
##   order_theory=108, size_matches_theory=true) と shadow_total を突合。
##   crown_battery の cert(K9_n_classes_5)は「X/Phi(X) の極大部分群類」という別対象の
##   計数であり(search/crown_battery_v1.g のコメント: maximal-class 検定)、本 script の
##   GTSh(K,N) 核類とは無関係 -- 数値の異同を判定に使わない(混同禁止・cert に明記のみ)。
##
## 規律: cert は機械生成値のみ・判定語なし・UNKNOWN一級。u/c 非接触(mの範囲・fの値のみ
##   操作、u=2m+1 はcharming集合の定義のみで使用、σの実像は一切計算しない)。

Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");

t0Global := GAPLIB_WallElapsedMs();;

## ================= (F2) machinery, VERBATIM from search/iso_census83_deep15_v1.g
##   (itself verbatim from search/wall-miner-v4.g), reused for the [1008,521] window =================
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

## generic single-candidate predicate (for twist survival, sec B) -- same 4 gates as
## CorrectedShadows's per-candidate body, but callable on an arbitrary g in PN (not just
## g ranging over D by construction) so we can test f*q with q possibly outside D.
IsGenuineShadow := function(W, D, m, g)
  local u;
  if not (g in D) then return false; fi;
  if AbstractProd([g, TH(W, g)]) <> Identity(W.Bq) then return false; fi;
  u := 2*m + 1;
  if RtOf(W, m, g) <> W.c^m then return false; fi;
  if Size(Group(W.x^u, AbstractProd([g^-1, W.y^u, g]))) <> Size(W.PN) then return false; fi;
  return true;
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

## ================= marked-factor-map kernel classification (shared for the fixture window
## and the K(9) positive control) =================
## qrec here is a lightweight rec(x:=..,y:=..,PN:=..) -- x,y elements of PN, PN=Group(x,y).
## shadowList = list of rec(m:=.., f:=..) (f in PN).
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

## naive PN-level well-definedness/kernel check (independent diagnostic, NOT used for the
## #C classification itself -- recorded alongside for cross-check/anomaly documentation)
NaiveWellDefCheck := function(qrec, sh)
  local u, genA, genB, psi;
  u := 2*sh.m + 1;;
  genA := qrec.x^u;;
  genB := AbstractProd([sh.f^-1, qrec.y^u, sh.f]);;
  psi := GroupHomomorphismByImages(qrec.PN, qrec.PN, [qrec.x, qrec.y], [genA, genB]);;
  if psi = fail then
    return rec(well_defined := false, kernel_size := fail, kernel_trivial := false);;
  else
    return rec(well_defined := true, kernel_size := Size(Kernel(psi)), kernel_trivial := (Size(Kernel(psi)) = 1));;
  fi;
end;;

Print("############################################################\n");
Print("# set_surgery_fixture_v1.g -- I-SET-1/I-SET-4 fixture 検算(裁定1082)\n");
Print("############################################################\n");

## ================= 陽性対照: K(9)(isolated, 予言 #C=1・|GT|=108) =================
Print("\n=== 陽性対照: K(9) (isolated) ===\n");
BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, q3, X, Y, Xchk, Ychk, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("BuildPn: D_n relations failed for n = ", n);
  fi;
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2) * tr(s,3);;  q2 := tr(s,1) * tr(s,3);;  q3 := tr(s,1) * tr(s,2);;
  X := AbstractProd([a1, q1]);;  Y := AbstractProd([a1, a2, a3, q2]);;
  Xchk := tr(r,1) * tr(s,2) * tr(s,3);;
  Ychk := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
  if X <> Xchk or Y <> Ychk then Error("BuildPn: convention mismatch for n=", n); fi;
  Gfull := Group(a1, a2, a3, q1, q2);;
  return rec(n:=n, X:=X, Y:=Y, G:=Gfull);
end;;

Pn9 := BuildPn(9);;
qrecK9 := rec(x:=Pn9.X, y:=Pn9.Y, c:=One(Pn9.G), G:=Pn9.G, PN:=Pn9.G);;
Nord9 := Lcm(Order(Pn9.X), Order(Pn9.Y));;
charmingSet9 := Filtered([0..Nord9-1], mm -> Gcd(2*mm+1, Nord9) = 1);;
gtResult9 := EnumerateReducedHexagon(qrecK9, charmingSet9);;
Print("  |PN|=", Size(Pn9.G), " N_ord=", Nord9, " shadow_total=", gtResult9.shadow_total, "\n");
posControlShadowTotalOk := (gtResult9.shadow_total = 108);;
Print("[", PF(posControlShadowTotalOk), "] shadow_total = 108 (frattini_resolution_v2 cert row K(9) size_X): ", posControlShadowTotalOk, "\n");

t9class0 := GAPLIB_WallElapsedMs();;
class9 := ClassifyByMarkedFactorMap(qrecK9, gtResult9.shadows);;
t9class1 := GAPLIB_WallElapsedMs();;
Print("  |Aut(PN)|=", class9.aut_pn_order, " num_classes=", class9.num_classes,
      " class_sizes=", List(class9.classes, c -> c.size), " elapsed_ms=", t9class1-t9class0, "\n");
posControlNumClassesOk := (class9.num_classes = 1) and (class9.classes[1].size = 108);;
Print("[", PF(posControlNumClassesOk), "] 予言 #C(K(9))=1 (isolated): ", posControlNumClassesOk, "\n");

## ================= 検算A: [1008,521] slot1 (48 shadows) の核分類 =================
Print("\n=== 検算A: [1008,521] slot1 の核 census (marked-factor-map) ===\n");
Read("search/iso_census83_deep15_data.g");;
entryFix := DEEP15[1];;
if entryFix.id <> [1008, 521] then
  Error("set_surgery_fixture_v1: DEEP15[1].id != [1008,521], got ", entryFix.id, " -- fixture mismatch, refusing to proceed");
fi;
W := BuildWindowFromWords(entryFix.index, entryFix.words);;
if not (W.c <> Identity(W.Bq)) then
  Error("set_surgery_fixture_v1: expected c notin N for this (deep, non-isolated) window");
fi;
Print("  |Bq|=", Size(W.Bq), " |PN|=", Size(W.PN), " N_ord=", W.Nord, " z(order of c)=", Order(W.c), "\n");

charmingSetFix := Filtered([0 .. W.Nord - 1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
corrFix := CorrectedShadows(W, charmingSetFix);;
shadowsFix := List(corrFix, sh -> rec(m := sh[1], f := sh[2]));;
Print("  shadow_total=", Length(shadowsFix), " (期待 48, settled_layer_verdict_v1.md 表と突合)\n");
shadowTotalMatchesVerdict := (Length(shadowsFix) = 48);;
Print("[", PF(shadowTotalMatchesVerdict), "] shadow_total = 48: ", shadowTotalMatchesVerdict, "\n");

qrecFix := rec(x := W.x, y := W.y, PN := W.PN);;
t0class := GAPLIB_WallElapsedMs();;
classFix := ClassifyByMarkedFactorMap(qrecFix, shadowsFix);;
t1class := GAPLIB_WallElapsedMs();;
Print("  |Aut(PN)|=", classFix.aut_pn_order, " num_classes=", classFix.num_classes,
      " class_sizes=", List(classFix.classes, c -> c.size), " elapsed_ms=", t1class-t0class, "\n");
predictionMatches := (classFix.num_classes = 2) and
  (Set(List(classFix.classes, c -> c.size)) = Set([24, 24]));;
Print("[", PF(predictionMatches), "] 予言 #C([1008,521])=2, 48=24x2: ", predictionMatches, "\n");

## naive PN-endomorphism well-definedness diagnostic, per shadow -- cross-checked against the
## marked-factor-map classes (documentation only, does not feed into #C)
naiveDetail := List(shadowsFix, sh -> NaiveWellDefCheck(qrecFix, sh));;
naiveWellDefCount := Length(Filtered(naiveDetail, r -> r.well_defined));;
naiveKernelTrivialCount := Length(Filtered(naiveDetail, r -> r.well_defined and r.kernel_trivial));;
Print("  [diagnostic] naive PN well_defined count=", naiveWellDefCount,
      "/48, kernel_trivial(within well_defined) count=", naiveKernelTrivialCount, "\n");

## per-class breakdown: for each marked-factor-map class, tabulate how many of its members
## have naive well_defined=true (should be homogeneous within a class if the theory is right)
classWellDefHomogeneous := true;;
classSummaries := [];;
for cl in classFix.classes do
  wdVals := List(cl.members, idx -> naiveDetail[idx].well_defined);;
  allSame := (Length(Set(wdVals)) = 1);;
  if not allSame then classWellDefHomogeneous := false; fi;
  Add(classSummaries, rec(size := cl.size, rep_m := cl.rep_m, rep_f_string := cl.rep_f_string,
                           naive_well_defined_values := wdVals, homogeneous := allSame,
                           all_well_defined := ForAll(wdVals, v -> v),
                           none_well_defined := ForAll(wdVals, v -> not v)));;
od;;
Print("  [diagnostic] per-class naive well_defined homogeneous across all classes: ", classWellDefHomogeneous, "\n");
for cs in classSummaries do
  Print("    class size=", cs.size, " rep_m=", cs.rep_m, " all_well_defined=", cs.all_well_defined,
        " none_well_defined=", cs.none_well_defined, " homogeneous=", cs.homogeneous, "\n");
od;

## ================= 検算B: 座標捻りの生存率(全数) =================
Print("\n=== 検算B: [1008,521] slot1 の座標捻り生存率(全数) ===\n");
Dfix := DerivedSubgroup(W.PN);;
CX := Elements(Centralizer(W.PN, W.x));;
CY := Elements(Centralizer(W.PN, W.y));;
GenAll := Elements(W.PN);;
Print("  |D|=", Size(Dfix), " |C_PN(x)|=", Length(CX), " |C_PN(y)|=", Length(CY), " |PN|=", Length(GenAll), "\n");

TwistSurvivalForSet := function(shadowList, D, qset, tag)
  local perShadow, sh, survive, q, tw, total, i, surviveThis;
  perShadow := [];;
  total := 0;;  survive := 0;;
  i := 0;;
  for sh in shadowList do
    i := i + 1;;
    if GAPLIB_CheckCap(500.0, Concatenation("twistB-", tag, "-", String(i))) then
      Print("[CAP WARNING] stopping twist-survival loop (", tag, ") at shadow ", i, "\n");
      break;
    fi;
    surviveThis := 0;;
    for q in qset do
      tw := AbstractProd([sh.f, q]);;
      if IsGenuineShadow(W, D, sh.m, tw) then
        surviveThis := surviveThis + 1;;
        survive := survive + 1;;
      fi;
      total := total + 1;;
    od;
    Add(perShadow, rec(m := sh.m, f_string := String(sh.f), survive := surviveThis, trials := Length(qset)));;
  od;
  return rec(tag := tag, total_trials := total, total_survive := survive, per_shadow := perShadow);;
end;;

tB0 := GAPLIB_WallElapsedMs();;
twistCX := TwistSurvivalForSet(shadowsFix, Dfix, CX, "Cx");;
twistCY := TwistSurvivalForSet(shadowsFix, Dfix, CY, "Cy");;
twistGen := TwistSurvivalForSet(shadowsFix, Dfix, GenAll, "general");;
tB1 := GAPLIB_WallElapsedMs();;
Print("  [Cx]      total_trials=", twistCX.total_trials, " total_survive=", twistCX.total_survive, "\n");
Print("  [Cy]      total_trials=", twistCY.total_trials, " total_survive=", twistCY.total_survive, "\n");
Print("  [general] total_trials=", twistGen.total_trials, " total_survive=", twistGen.total_survive, "\n");
Print("  twist-survival elapsed_ms=", tB1-tB0, "\n");

## ================= JSON output =================
JClassRec := function(c)
  return Concatenation("{\"size\":", String(c.size), ",\"rep_m\":", String(c.rep_m),
    ",\"rep_f_perm_string\":", JStr(c.rep_f_string), ",\"member_shadow_indices\":",
    JArr(List(c.members, String)), "}");
end;;

JClassSummaryRec := function(cs)
  return Concatenation("{\"size\":", String(cs.size), ",\"rep_m\":", String(cs.rep_m),
    ",\"rep_f_perm_string\":", JStr(cs.rep_f_string),
    ",\"naive_well_defined_values\":", JArr(List(cs.naive_well_defined_values, JB)),
    ",\"homogeneous\":", JB(cs.homogeneous),
    ",\"all_well_defined\":", JB(cs.all_well_defined),
    ",\"none_well_defined\":", JB(cs.none_well_defined), "}");
end;;

JNaiveDetailRec := function(r)
  local kszStr;
  if r.kernel_size = fail then kszStr := "null"; else kszStr := String(r.kernel_size); fi;
  return Concatenation("{\"well_defined\":", JB(r.well_defined), ",\"kernel_size\":", kszStr,
    ",\"kernel_trivial\":", JB(r.kernel_trivial), "}");
end;;

JPerShadowTwistRec := function(r)
  return Concatenation("{\"m\":", String(r.m), ",\"f_perm_string\":", JStr(r.f_string),
    ",\"survive\":", String(r.survive), ",\"trials\":", String(r.trials), "}");
end;;

JTwistResultRec := function(r)
  return Concatenation("{\"tag\":", JStr(r.tag), ",\"total_trials\":", String(r.total_trials),
    ",\"total_survive\":", String(r.total_survive), ",\"per_shadow\":[",
    JoinC(List(r.per_shadow, JPerShadowTwistRec), ","), "]}");
end;;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_setsurg.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/set_surgery_fixture_v1.g");;
wordsSha256 := ComputeSha256File("search/iso_census83_deep15_data.g");;

cert := Concatenation(
  "{\"schema\":\"shadow-atelier/set_surgery_fixture_v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/set_surgery_fixture_v1.g\",\"order\":\"裁定1082(発案6号I-SET-1/I-SET-4 fixture検算)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"spec_ref\":\"docs/notes/ideas_set_surgery_v1.md 札I-SET-1 3.(ii)・札I-SET-4 3.\"",
  ",\"method_note\":\"kernel classification uses the marked-factor-map method (Aut(PN) diagonal orbit on (genA,genB) pairs), NOT direct GAP subgroup comparison, per the pre-registered Sol warning. Justification: Ker(phi1)=Ker(phi2) for two epis F2->>PN iff phi2=alpha o phi1 for some alpha in Aut(PN) (first isomorphism theorem). See in-script comment header for the full derivation and for why the naive PN-level GroupHomomorphismByImages approach fails on exactly half the fixture shadows (confirmed genuine via an independent relator-substitution cross-check in scratchpad/diag_welldef.g, 0 mismatches out of 48).\",",
  "\"positive_control\":{",
    "\"window\":\"K(9) (isolated, BuildPn(9))\",",
    "\"pn_order\":", String(Size(Pn9.G)), ",\"n_ord\":", String(Nord9), ",",
    "\"shadow_total\":", String(gtResult9.shadow_total), ",",
    "\"shadow_total_matches_frattini_cert\":", JB(posControlShadowTotalOk), ",",
    "\"frattini_cert_ref\":\"search/certs/frattini_resolution_v2_20260812.json row K(9): size_X=108, order_theory=108, size_matches_theory=true\",",
    "\"aut_pn_order\":", String(class9.aut_pn_order), ",",
    "\"num_classes\":", String(class9.num_classes), ",",
    "\"class_sizes\":", JArr(List(class9.classes, c -> String(c.size))), ",",
    "\"num_classes_matches_prediction_1\":", JB(posControlNumClassesOk), ",",
    "\"crown_battery_disclaimer\":\"search/certs/crown_battery_v1_20260812.json reports K9_n_classes_5, but that counts maximal-subgroup classes of X/Phi(X) (search/crown_battery_v1.g header: 'maximal-class検定') -- a DIFFERENT object from GTSh(K,N) kernel classes computed here. Not used as a cross-check value; recorded only to prevent conflation.\"",
  "},",
  "\"check_a_kernel_census\":{",
    "\"window\":\"[1008,521] slot1 (search/iso_census83_deep15_data.g DEEP15[1], same fixture as settled_layer_verdict_v1.md table row and search/certs/iso_census83_deep15_v1_20260812.json)\",",
    "\"bq_order\":", String(Size(W.Bq)), ",\"pn_order\":", String(Size(W.PN)), ",",
    "\"n_ord\":", String(W.Nord), ",\"z_order_of_c\":", String(Order(W.c)), ",",
    "\"shadow_total\":", String(Length(shadowsFix)), ",",
    "\"shadow_total_matches_settled_layer_verdict\":", JB(shadowTotalMatchesVerdict), ",",
    "\"aut_pn_order\":", String(classFix.aut_pn_order), ",",
    "\"num_classes\":", String(classFix.num_classes), ",",
    "\"classes\":[", JoinC(List(classFix.classes, JClassRec), ","), "],",
    "\"prediction_48_eq_24x2_matches\":", JB(predictionMatches), ",",
    "\"diagnostic_naive_pn_endomorphism_check\":{",
      "\"note\":\"NOT used for #C -- documents why the naive PN-self-endomorphism approach is insufficient (descent fails for half the shadows). See method_note.\",",
      "\"well_defined_count\":", String(naiveWellDefCount), ",",
      "\"kernel_trivial_count\":", String(naiveKernelTrivialCount), ",",
      "\"per_class_summary\":[", JoinC(List(classSummaries, JClassSummaryRec), ","), "],",
      "\"per_shadow_detail\":[", JoinC(List(naiveDetail, JNaiveDetailRec), ","), "]",
    "}",
  "},",
  "\"check_b_twist_survival\":{",
    "\"window\":\"same as check_a ([1008,521] slot1)\",",
    "\"derived_subgroup_order\":", String(Size(Dfix)), ",",
    "\"c_x_order\":", String(Length(CX)), ",\"c_y_order\":", String(Length(CY)), ",\"pn_order\":", String(Length(GenAll)), ",",
    "\"twist_form\":\"[m,f] -> [m, f*q], q ranges over the named set; survives iff f*q passes domain(in derived subgroup)+hex310+hex311+generation (IsGenuineShadow, same 4 gates as CorrectedShadows)\",",
    "\"results\":[", JoinC([JTwistResultRec(twistCX), JTwistResultRec(twistCY), JTwistResultRec(twistGen)], ","), "]",
  "},",
  "\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(GAPLIB_WallElapsedMs() - t0Global),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\",\"deep15_data_sha256\":\"", wordsSha256, "\"}",
  "}"
);;

outPath := "search/certs/set_surgery_fixture_v1_20260813.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
