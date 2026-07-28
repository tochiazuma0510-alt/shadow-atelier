# search/derived-census-v2.g -- I-26 metabelian census v2(便 78 検分 F78-2.3 修理)
#
# Usage: .\gap.ps1 search\derived-census-v2.g
#
# 目的: v1(search/derived-census.g, 証明書 derived_census_20260728.json)は
#   observed_order を Phi 像(Aut(PB3/N) 内像)の位数として計算していたが、これを
#   「GT(N) 本体の位数」と混同していた(裁定147 erratum)。本 v2 は Sol 便 78 F78-2.3
#   の指示どおり、対象ごとに次の 5 欄を分離して記録する:
#     group_order              -- GT(N) 本体の位数
#     phi_image_order          -- Phi: GT(N) -> Aut(PB3/N) の像の位数
#     theta_image_order        -- Theta: GT(N) -> Aut(B3/N) の像の位数
#     derived_length_of_group  -- 本体の導来長
#     derived_length_of_image  -- phi_image の導来長(v1 の観測値はこちらに相当)
#
# 実装上の設計変更履歴(このファイル内で正直に記帳する):
#   最初の実装は theta_image を c2f-probe4.g のパターン(BuildQTGeneral で B3/N を
#   6*|A| 点の具体置換表現として構成し、その上で各 shadow の自己同型を Group() として
#   閉包し Size()/DerivedSubgroup() を取る)で全 12 対象に一般化しようとしたが、
#   K(11) で "reached the pre-set memory limit"(GAP -o 2g cap)により停止した
#   (6*|A| 点規模の置換群の stabilizer chain 構築が RAM 8GB 環境で破綻する)。
#   このため設計を次のように変更した(GAP 実行は search/week3-battery-A1-v2_1.g が
#   既に N_A の 20 shadow で検証済みの合成則 (3.53) を再利用):
#     - group_order / derived_length_of_group:
#       shadows 自体の合成則 (3.53) [m1,f1]o[m2,f2] = [(2 m1 m2 + m1 + m2) mod N_ord,
#       f1 . E_{m1,f1}(f2)] から shadow_total x shadow_total の composition_table を計算し
#       (次数は shadow_total、大きくても 48 程度、B3/N 水準の巨大置換に触れない)、
#       L/M5 と同じ BuildRegularPermGroupFromTable で正則表現を構成する。これが GT(N)
#       本体の最も安価かつ直接的な具体表現である(閉性・単位元・逆元も観測として記録)。
#     - theta_image_order: BuildQTGeneral で S1=sigma1,S2=sigma2 の像(6*|A| 点上の
#       具体置換 2 個)だけは構成する(これは配列構築のみで軽い)が、そこから
#       Group(...)/Size()/DerivedSubgroup() のような巨大次数群演算は一切行わない。
#       代わりに各 shadow について「S1^u = S1 かつ Gf^-1 S2^u Gf = S2」という
#       ker(Theta) 所属条件を個別の元の等式としてだけ検査する(度数 6*|A| の置換の
#       べき乗・積・比較のみで、stabilizer chain を要しない)。ker(Theta) に属する
#       shadow の個数を数え、theta_image_order = group_order / |ker(Theta)| として導出する
#       (full hexagon (3.3)(3.4) も同じループで検査し、ker 判定の前提として記録する)。
#
# 宇宙: v1 と同一の既存 14 対象。新規対象の追加なし。v1 ファイルは変更しない。
# 解釈しない(観測の記録に徹する)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# derived-census-v2.g -- I-26 metabelian census v2 (5-column split, F78-2.3)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

# ====================================================================
# ヘルパー
# ====================================================================

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
    for j in [1..n] do
      l[j + (i-1)*n] := (j^p) + (i-1)*n;
    od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2) * tr(s,3);;
  q2 := tr(s,1) * tr(s,3);;
  q3 := tr(s,1) * tr(s,2);;
  X := AbstractProd([a1, q1]);;
  Y := AbstractProd([a1, a2, a3, q2]);;
  Xchk := tr(r,1) * tr(s,2) * tr(s,3);;
  Ychk := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
  if X <> Xchk or Y <> Ychk then
    Error("BuildPn: convention mismatch for n=", n);
  fi;
  Gfull := Group(a1, a2, a3, q1, q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, q3:=q3, X:=X, Y:=Y, G:=Gfull);
end;;

DerivedInfo := function(G)
  local H, Hprev, len, cap;
  if Size(G) = 1 then
    return rec(derived_length:=0, status:="trivial", core_size:=1);
  fi;
  H := G;;  len := 0;;  cap := 10;;
  while (not IsTrivial(H)) and len < cap do
    Hprev := H;;
    H := DerivedSubgroup(H);;
    len := len + 1;;
    if Size(H) = Size(Hprev) then
      return rec(derived_length:=-1, status:="stabilized_nonsolvable", core_size:=Size(H));
    fi;
  od;
  if IsTrivial(H) then
    return rec(derived_length:=len, status:="solvable", core_size:=1);
  else
    return rec(derived_length:=-2, status:="cap_reached_unresolved", core_size:=Size(H));
  fi;
end;;

IsMetabelianInfo := function(info)
  return (info.status = "solvable" or info.status = "trivial") and info.derived_length <= 2;
end;;

# phi_image: Phi_{m,f} を qrec.G(=A=PB3/N) 上の自己同型として構成(v1 と同一)
BuildGTPermGroupFromShadows := function(qrec, shadows)
  local elts, n, idxDict, i, phiPerms, sh, u, F, PhiHom, images, img;
  elts := Elements(qrec.G);;
  n := Length(elts);;
  idxDict := NewDictionary(elts[1], true);;
  for i in [1..n] do AddDictionary(idxDict, elts[i], i); od;;
  phiPerms := [];;
  for sh in shadows do
    u := 2*sh.m + 1;;
    F := sh.f;;
    PhiHom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y],
                [qrec.x^u, AbstractProd([F^-1, qrec.y^u, F])]);;
    if PhiHom = fail then
      Error("BuildGTPermGroupFromShadows: Phi construction failed, m=", sh.m);
    fi;
    if not IsBijective(PhiHom) then
      Error("BuildGTPermGroupFromShadows: Phi not bijective, m=", sh.m);
    fi;
    images := [];;
    for i in [1..n] do
      img := Image(PhiHom, elts[i]);;
      images[i] := LookupDictionary(idxDict, img);;
    od;
    Add(phiPerms, PermList(images));;
  od;
  return Group(phiPerms);;
end;;

# composition_table (0-indexed [a,b,c] with a.b=c) -> 正則置換表現(v1/L/M5 と同一)
BuildRegularPermGroupFromTable := function(tbl, n)
  local prod, e, gens, a, images, b;
  prod := List([0..n-1], i -> List([0..n-1], j -> -1));;
  for e in tbl do prod[e[1]+1][e[2]+1] := e[3]; od;;
  gens := [];;
  for a in [0..n-1] do
    images := List([0..n-1], b -> prod[a+1][b+1] + 1);;
    Add(gens, PermList(images));;
  od;
  return Group(gens);;
end;;

ReadCompositionTable := function(path)
  local f, content, mkS, mkE, posS, posE, tblStr;
  f := InputTextFile(path);;
  if f = fail then Error("ReadCompositionTable: cannot open ", path); fi;
  content := ReadAll(f);;
  CloseStream(f);;
  mkS := "\"composition_table\":";;
  posS := PositionSublist(content, mkS);;
  if posS = fail then Error("composition_table marker not found in ", path); fi;
  mkE := ",\"inverse_map\":";;
  posE := PositionSublist(content, mkE);;
  if posE = fail then Error("inverse_map marker not found in ", path); fi;
  tblStr := content{[posS + Length(mkS) .. posE - 1]};;
  return EvalString(Concatenation(tblStr, ";"));;
end;;

# (3.53) [m1,f1] o [m2,f2] = [(2 m1 m2 + m1 + m2) mod Nord, f1 . E_{m1,f1}(f2)]
# -- 逐語に week3-battery-A1-v2_1.g の合成則を一般化(Ehom は i1 ごとに一度だけ構成)。
# 戻り値: rec(regGrp, closed_observed, closure_fail_count, shadow_total)
BuildShadowCompositionRegularRep := function(qrec, shadows, Nord)
  local n, i1, i2, m1, f1, m2, f2, u1, Ehom, newm, newf, idx, t, tbl, closureFail, regGrp;
  n := Length(shadows);;
  tbl := [];;  closureFail := 0;;
  for i1 in [1..n] do
    m1 := shadows[i1].m;;  f1 := shadows[i1].f;;  u1 := 2*m1+1;;
    Ehom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y],
              [qrec.x^u1, AbstractProd([f1^-1, qrec.y^u1, f1])]);;
    if Ehom = fail then
      Error("BuildShadowCompositionRegularRep: E_{m1,f1} construction failed, i1=", i1);
    fi;
    for i2 in [1..n] do
      m2 := shadows[i2].m;;  f2 := shadows[i2].f;;
      newm := (2*m1*m2 + m1 + m2) mod Nord;;
      newf := AbstractProd([f1, Image(Ehom, f2)]);;
      idx := fail;;
      for t in [1..n] do
        if shadows[t].m = newm and shadows[t].f = newf then idx := t; break; fi;
      od;
      if idx = fail then
        closureFail := closureFail + 1;;
        Add(tbl, [i1-1, i2-1, -1]);;
      else
        Add(tbl, [i1-1, i2-1, idx-1]);;
      fi;
    od;
  od;
  if closureFail > 0 then
    return rec(regGrp:=fail, closed_observed:=false, closure_fail_count:=closureFail, shadow_total:=n);;
  fi;
  regGrp := BuildRegularPermGroupFromTable(tbl, n);;
  return rec(regGrp:=regGrp, closed_observed:=true, closure_fail_count:=0, shadow_total:=n);;
end;;

# c2f-probe4.g で検証済みの word 評価ヘルパー(逐語コピー)
EvalWordIn := function(word, xImg, yImg)
  local lst, letter;
  lst := [];;
  for letter in word do
    if letter[1] = "x" then Add(lst, xImg^letter[2]); else Add(lst, yImg^letter[2]); fi;
  od;
  if Length(lst) = 0 then return xImg^0; fi;
  return AbstractProd(lst);
end;;

# theta_image_order を「巨大次数の Group()/Size()/DerivedSubgroup() を一切使わず」求める:
# S1,S2(BuildQTGeneral、配列構築のみで軽量)を構成し、各 shadow について
#  (i) full hexagon (3.3)/(3.4) が B3/N 水準で成立するか(元の等式チェックのみ)
#  (ii) ker(Theta) 所属条件 S1^u=S1 and Gf^-1 S2^u Gf = S2(元の等式チェックのみ)
# を検査する。theta_image_order := groupOrd / |ker(Theta)|(groupOrd は composition-table
# から得た実測本体位数)。戻り値: rec(theta_image_order, kernel_count, hex_ok, note)
ComputeThetaKernelAndImage := function(qrec, shadows, groupOrd)
  local lab, S1, S2, X3, Y3, Cc, kernelCount, hexOk, sh, u, Gf, h33, h34, kerCond, thetaOrd;
  lab := BuildQTGeneral(qrec.G, qrec.x, qrec.y, qrec.c);;
  S1 := lab.s1;;  S2 := lab.s2;;
  X3 := S1^2;;  Y3 := S2^2;;
  Cc := AbstractProd([S1,S2,S1])^2;;
  kernelCount := 0;;  hexOk := true;;
  for sh in shadows do
    u := 2*sh.m + 1;;
    Gf := EvalWordIn(sh.word, X3, Y3);;
    if EvalWordIn(sh.word, qrec.x, qrec.y) <> sh.f then
      Error("ComputeThetaKernelAndImage: word/elt mismatch, m=", sh.m);
    fi;
    h33 := AbstractProd([S1^u, Gf^-1, S2^u, Gf]) = AbstractProd([Gf^-1, S1, S2, X3^(-sh.m), Cc^sh.m]);;
    h34 := AbstractProd([Gf^-1, S2^u, Gf, S1^u]) = AbstractProd([S2, S1, Y3^(-sh.m), Cc^sh.m, Gf]);;
    if not (h33 and h34) then hexOk := false; fi;
    kerCond := (S1^u = S1) and (AbstractProd([Gf^-1, S2^u, Gf]) = S2);;
    if kerCond then kernelCount := kernelCount + 1; fi;
  od;
  if not hexOk then
    return rec(theta_image_order:="UNKNOWN", kernel_count:="UNKNOWN", hex_ok:=false,
      note:="full hexagon (3.3)/(3.4) failed at B3/N level for at least one shadow; theta_image_order not derived");;
  fi;
  if kernelCount = 0 or groupOrd = "UNKNOWN" or (groupOrd mod kernelCount) <> 0 then
    return rec(theta_image_order:="UNKNOWN", kernel_count:=kernelCount, hex_ok:=true,
      note:="kernel_count does not evenly divide group_order (or group_order UNKNOWN); theta_image_order not derived");;
  fi;
  thetaOrd := groupOrd / kernelCount;;
  return rec(theta_image_order:=thetaOrd, kernel_count:=kernelCount, hex_ok:=true,
    note:="theta_image_order = group_order / kernel_count, kernel_count from direct element-level ker(Theta) membership test (no large-degree Group()/Size() computed)");;
end;;

results := [];;

RecordResultA := function(name, definition, groupOrderTheory, qrec, shadows, Nord, method)
  local phiGrp, phiOrd, phiInfo, derivedLenImage, compRes, groupOrd, derivedLenGroup,
        metaGroup, thetaRes, injInfo, phiKernelStr;
  phiGrp := BuildGTPermGroupFromShadows(qrec, shadows);;
  phiOrd := Size(phiGrp);;
  phiInfo := DerivedInfo(phiGrp);;
  derivedLenImage := phiInfo.derived_length;;

  compRes := BuildShadowCompositionRegularRep(qrec, shadows, Nord);;
  if compRes.closed_observed then
    groupOrd := Size(compRes.regGrp);;
    derivedLenGroup := DerivedInfo(compRes.regGrp).derived_length;;
    metaGroup := IsMetabelianInfo(DerivedInfo(compRes.regGrp));;
  else
    groupOrd := "UNKNOWN";;
    derivedLenGroup := "UNKNOWN";;
    metaGroup := "UNKNOWN";;
  fi;

  thetaRes := ComputeThetaKernelAndImage(qrec, shadows, groupOrd);;

  if IsInt(groupOrd) and IsInt(phiOrd) and (groupOrd mod phiOrd) = 0 then
    phiKernelStr := String(groupOrd / phiOrd);;
  else
    phiKernelStr := "UNKNOWN";;
  fi;

  injInfo := Concatenation(
    "phi_kernel_order=", phiKernelStr,
    " (group_order=", String(groupOrd), ", phi_image_order=", String(phiOrd), ")",
    "; theta_kernel_count=", String(thetaRes.kernel_count),
    "; theta_hex_ok=", String(thetaRes.hex_ok),
    "; composition_closed_observed=", String(compRes.closed_observed),
    "; composition_closure_fail_count=", String(compRes.closure_fail_count),
    "; shadow_total=", String(Length(shadows)),
    "; group_order_theory=", String(groupOrderTheory),
    "; group_order_matches_theory=", String(groupOrd = groupOrderTheory),
    "; ", thetaRes.note);;

  Add(results, rec(
    name:=name, definition:=definition, method:=method,
    group_order:=groupOrd, group_order_theory:=groupOrderTheory,
    phi_image_order:=phiOrd, theta_image_order:=thetaRes.theta_image_order,
    derived_length_of_group:=derivedLenGroup, derived_length_of_image:=derivedLenImage,
    metabelian_of_group:=metaGroup,
    injectivity_information:=injInfo
  ));;

  Print("[", name, "] group_order=", groupOrd, " (theory=", groupOrderTheory, ")",
        "  phi_image_order=", phiOrd, " (derived_len_image=", derivedLenImage, ")",
        "  theta_image_order=", thetaRes.theta_image_order,
        "  derived_length_of_group=", derivedLenGroup, "\n");
end;;

RecordResultB := function(name, definition, GTgrp, method)
  local info, groupOrd;
  groupOrd := Size(GTgrp);;
  info := DerivedInfo(GTgrp);;
  Add(results, rec(
    name:=name, definition:=definition, method:=method,
    group_order:=groupOrd, group_order_theory:=groupOrd,
    phi_image_order:="N/A", theta_image_order:="N/A",
    derived_length_of_group:=info.derived_length, derived_length_of_image:="N/A",
    metabelian_of_group:=IsMetabelianInfo(info),
    injectivity_information:="none"
  ));;
  Print("[", name, "] group_order=", groupOrd, "  derived_length_of_group=", info.derived_length,
        "  [method B: composition_table regular rep, no separate phi/theta image constructed]\n");
end;;

RecordUnknown := function(name, definition, reason)
  Add(results, rec(name:=name, definition:=definition,
       group_order:="UNKNOWN", group_order_theory:="UNKNOWN",
       phi_image_order:="UNKNOWN", theta_image_order:="UNKNOWN",
       derived_length_of_group:="UNKNOWN", derived_length_of_image:="UNKNOWN",
       metabelian_of_group:="UNKNOWN",
       injectivity_information:=Concatenation("UNKNOWN: ", reason),
       method:=Concatenation("UNKNOWN: ", reason)));;
  Print("[UNKNOWN] ", name, ": ", reason, "\n");
end;;

# ====================================================================
# タスク A: G_n 系(K^(n) 族), n=3,5,7,9,11
# ====================================================================
Print("\n============================================================\n");
Print("# タスク A: K^(n) 族 n=3,5,7,9,11\n");
Print("============================================================\n");

for n in [3, 5, 7, 9, 11] do
  Pn := BuildPn(n);;
  qrec := rec(x:=Pn.X, y:=Pn.Y, c:=One(Pn.G), G:=Pn.G);;
  Nord := Lcm(Order(Pn.X), Order(Pn.Y));;
  charmingSet := Filtered([0..Nord-1], mm -> Gcd(2*mm+1, Nord) = 1);;
  gtResult := EnumerateReducedHexagon(qrec, charmingSet);;
  phi_n := Length(Filtered([1..n], k -> Gcd(k,n)=1));;
  groupOrderTheory := 2 * n * phi_n;;
  RecordResultA(Concatenation("K(", String(n), ")"),
    Concatenation("GT(K^(", String(n), "))"), groupOrderTheory, qrec, gtResult.shadows, Nord,
    "phi: BuildGTPermGroupFromShadows on A=PB3/N (BuildPn). group: (3.53) shadow composition regular rep. theta: element-level ker(Theta) test via BuildQTGeneral S1,S2 (no large-degree Group())");;
od;;

# ====================================================================
# タスク B: week3 registered windows
# ====================================================================
Print("\n============================================================\n");
Print("# タスク B: week3 registered windows (L, M5, N_Q, M_Q, N_2, N_3, M_3, N_A, M_A5)\n");
Print("============================================================\n");

# ---- N_Q (stage 1a: Q8) ----
q8rec := MakeQ8();;
qrecNQ := rec(x:=q8rec.x, y:=q8rec.y, c:=One(q8rec.G), G:=q8rec.G);;
NordNQ := Lcm(Order(q8rec.x), Order(q8rec.y));;
charmingNQ := Filtered([0..NordNQ-1], mm -> Gcd(2*mm+1, NordNQ) = 1);;
gtNQ := EnumerateReducedHexagon(qrecNQ, charmingNQ);;
RecordResultA("N_Q", "pi^{-1}(ker(F2 ->> Q8))", 4, qrecNQ, gtNQ.shadows, NordNQ,
  "phi/group/theta on Q8 (MakeQ8, stage 1a construction)");;

# ---- M_Q (stage 1b: G3 x_{C2^2} Q8, fiber product on 17 points) ----
gn3_1b := MakeGn(3);;
q8rec_1b := MakeQ8();;
xhatMQ := PermList(Concatenation(List([1..9], j -> j^gn3_1b.x), List([1..8], j -> 9 + (j^q8rec_1b.x))));;
yhatMQ := PermList(Concatenation(List([1..9], j -> j^gn3_1b.y), List([1..8], j -> 9 + (j^q8rec_1b.y))));;
QM_MQ := Group(xhatMQ, yhatMQ);;
if Size(QM_MQ) <> 216 then
  RecordUnknown("M_Q", "K^(3) cap N_Q", Concatenation("Q_M construction size mismatch: got ",
    String(Size(QM_MQ)), " expected 216"));;
else
  qrecMQ := rec(x:=xhatMQ, y:=yhatMQ, c:=One(QM_MQ), G:=QM_MQ);;
  NordMQ := Lcm(Order(xhatMQ), Order(yhatMQ));;
  charmingMQ := Filtered([0..NordMQ-1], mm -> Gcd(2*mm+1, NordMQ) = 1);;
  gtMQ := EnumerateReducedHexagon(qrecMQ, charmingMQ);;
  RecordResultA("M_Q", "K^(3) cap N_Q", 24, qrecMQ, gtMQ.shadows, NordMQ,
    "phi/group/theta on Q_M=G3 x_{C2^2} Q8 (17-pt fiber product, stage 1b construction)");;
fi;

# ---- N_2 (stage 2a: P2 = MakeHeis(4,2)) ----
p2rec := MakeHeis(4, 2);;
qrecN2 := rec(x:=p2rec.x, y:=p2rec.y, c:=One(p2rec.G), G:=p2rec.G);;
NordN2 := Lcm(Order(p2rec.x), Order(p2rec.y));;
charmingN2 := Filtered([0..NordN2-1], mm -> Gcd(2*mm+1, NordN2) = 1);;
gtN2 := EnumerateReducedHexagon(qrecN2, charmingN2);;
RecordResultA("N_2", "pi^{-1}(F2^4 gamma_3(F2))", 4, qrecN2, gtN2.shadows, NordN2,
  "phi/group/theta on P2=MakeHeis(4,2) (stage 2a construction)");;

# ---- N_3 (stage 2b: P3 = MakeP3()) ----
p3rec := MakeP3();;
qrecN3 := rec(x:=p3rec.x, y:=p3rec.y, c:=One(p3rec.G), G:=p3rec.G);;
NordN3 := Lcm(Order(p3rec.x), Order(p3rec.y));;
charmingN3 := Filtered([0..NordN3-1], mm -> Gcd(2*mm+1, NordN3) = 1);;
gtN3 := EnumerateReducedHexagon(qrecN3, charmingN3);;
RecordResultA("N_3", "pi^{-1}(F2^4 gamma_4(F2))", 8, qrecN3, gtN3.shadows, NordN3,
  "phi/group/theta on P3=MakeP3() (stage 2b construction)");;

# ---- M_3 (stage 3: G3 x P3, DirectProduct/Embedding, order 3456) ----
gn3_3 := MakeGn(3);;
p3rec_3 := MakeP3();;
DP3 := DirectProduct(gn3_3.G, p3rec_3.G);;
emb1_3 := Embedding(DP3, 1);;
emb2_3 := Embedding(DP3, 2);;
xhatM3 := Image(emb1_3, gn3_3.x) * Image(emb2_3, p3rec_3.x);;
yhatM3 := Image(emb1_3, gn3_3.y) * Image(emb2_3, p3rec_3.y);;
QM_M3 := Group(xhatM3, yhatM3);;
if Size(QM_M3) <> 3456 then
  RecordUnknown("M_3", "K^(3) cap N_3", Concatenation("Q_M construction size mismatch: got ",
    String(Size(QM_M3)), " expected 3456"));;
else
  qrecM3 := rec(x:=xhatM3, y:=yhatM3, c:=One(QM_M3), G:=QM_M3);;
  NordM3 := Lcm(Order(xhatM3), Order(yhatM3));;
  charmingM3 := Filtered([0..NordM3-1], mm -> Gcd(2*mm+1, NordM3) = 1);;
  gtM3 := EnumerateReducedHexagon(qrecM3, charmingM3);;
  RecordResultA("M_3", "K^(3) cap N_3", 48, qrecM3, gtM3.shadows, NordM3,
    "phi/group/theta on Q_M=G3 x P3 (DirectProduct/Embedding, stage 3 construction)");;
fi;

# ---- N_A (stage A1: A5 direct) ----
XhatA1 := (1,3,2,4,5);;
YhatA1 := (1,3,4,5,2);;
A5grp := Group(XhatA1, YhatA1);;
if Size(A5grp) <> 60 then
  RecordUnknown("N_A", "pi^{-1}(ker(F2 ->> A5))", Concatenation("A5 construction size mismatch: got ",
    String(Size(A5grp))));;
else
  qrecNA := rec(x:=XhatA1, y:=YhatA1, c:=One(A5grp), G:=A5grp);;
  NordNA := Lcm(Order(XhatA1), Order(YhatA1));;
  charmingNA := Filtered([0..NordNA-1], mm -> Gcd(2*mm+1, NordNA) = 1);;
  gtNA := EnumerateReducedHexagon(qrecNA, charmingNA);;
  RecordResultA("N_A", "pi^{-1}(ker(F2 ->> A5))", 20, qrecNA, gtNA.shadows, NordNA,
    "phi/group/theta on A5=Group(Xhat,Yhat) (stage A1 construction)");;
fi;

# ---- M_A5 (stage A2: A5 x C5, c_in_N=false -> word-level prepend enumeration; c-bar=(1,zeta)) ----
Xhat5 := (1,3,2,4,5);;
Yhat5 := (1,3,4,5,2);;
zetaA2 := (6,7,8,9,10);;
zeta2A2 := zetaA2^2;;
xhatMA5 := Xhat5 * zeta2A2;;
yhatMA5 := Yhat5 * zeta2A2;;
QM_MA5 := Group(xhatMA5, yhatMA5);;
if Size(QM_MA5) <> 300 then
  RecordUnknown("M_A5", "N_A cap N_5", Concatenation("Q_M construction size mismatch: got ",
    String(Size(QM_MA5)), " expected 300"));;
else
  qrecMA5 := rec(x:=xhatMA5, y:=yhatMA5, c:=zetaA2, G:=QM_MA5);;
  NordMA5 := Lcm(Order(xhatMA5), Order(yhatMA5));;
  charmingMA5 := Filtered([0..NordMA5-1], mm -> Gcd(2*mm+1, NordMA5) = 1);;
  gtMA5 := EnumerateWordLevelHexagonPrepend(qrecMA5, charmingMA5);;
  RecordResultA("M_A5", "N_A cap N_5 (N_5=ker(beta_5:B3->S3xC5))", 20, qrecMA5, gtMA5.shadows, NordMA5,
    "phi/group/theta on Q_M=A5 x C5 (stage A2 construction, word-level prepend shadows; c-bar=(1,zeta))");;
fi;

# ---- L (composition_table cert, certificates/L01.v1.json) ----
if not IsExistingFile("certificates/L01.v1.json") then
  RecordUnknown("L", "K^(3) cap N0", "certificates/L01.v1.json not found");;
else
  tblL := ReadCompositionTable("certificates/L01.v1.json");;
  GTgrpL := BuildRegularPermGroupFromTable(tblL, 36);;
  RecordResultB("L", "K^(3) cap N0", GTgrpL,
    "regular perm rep from composition_table in certificates/L01.v1.json");;
fi;

# ---- M5 (composition_table cert, certificates/M01.v1.json) ----
if not IsExistingFile("certificates/M01.v1.json") then
  RecordUnknown("M5", "K^(3) cap N5", "certificates/M01.v1.json not found");;
else
  tblM5 := ReadCompositionTable("certificates/M01.v1.json");;
  GTgrpM5 := BuildRegularPermGroupFromTable(tblM5, 48);;
  RecordResultB("M5", "K^(3) cap N5", GTgrpM5,
    "regular perm rep from composition_table in certificates/M01.v1.json");;
fi;

# ====================================================================
# 総括表
# ====================================================================
Print("\n############################################################\n");
Print("# 総括: I-26 census v2 表(対象 x 5欄)\n");
Print("############################################################\n");
Print("name | group_order | phi_image_order | theta_image_order | derived_len_group | derived_len_image\n");
for r in results do
  Print(r.name, " | ", r.group_order, " | ", r.phi_image_order, " | ", r.theta_image_order,
        " | ", r.derived_length_of_group, " | ", r.derived_length_of_image, "\n");
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_census_v2.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

FieldToJson := function(v)
  if v = "UNKNOWN" then return JStr("UNKNOWN"); fi;
  if IsString(v) then return JStr(v); fi;
  if IsBool(v) then return JB(v); fi;
  return String(v);
end;;

ResultToJson := function(r)
  return Concatenation(
    "{\"name\":", JStr(r.name), ",\"definition\":", JStr(r.definition),
    ",\"group_order\":", FieldToJson(r.group_order),
    ",\"group_order_theory\":", FieldToJson(r.group_order_theory),
    ",\"phi_image_order\":", FieldToJson(r.phi_image_order),
    ",\"theta_image_order\":", FieldToJson(r.theta_image_order),
    ",\"derived_length_of_group\":", FieldToJson(r.derived_length_of_group),
    ",\"derived_length_of_image\":", FieldToJson(r.derived_length_of_image),
    ",\"metabelian_of_group\":", FieldToJson(r.metabelian_of_group),
    ",\"injectivity_information\":", FieldToJson(r.injectivity_information),
    ",\"method\":", JStr(r.method),
    "}"
  );
end;;

resultsJson := JArr(List(results, ResultToJson));;

scriptSha256 := ComputeSha256File("search/derived-census-v2.g");;

cert := Concatenation(
  "{\"schema\":\"derived-census/v2\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/derived-census-v2.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"design_source\":\"ideas/ideas_005_panorama.md I-26 (裁定144 採用) + sol/sol_reply_78_math5.md F78-2.3 (5欄分離修理) + sol/裁定_147_C2F判定.md (erratum) + search/week3-battery-A1-v2_1.g ((3.53) composition table pattern reused for group_order/derived_length_of_group)\"",
  ",\"universe\":\"K^(n) n=3,5,7,9,11 + week3 registered windows L,M5,N_Q,M_Q,N_2,N_3,M_3,N_A,M_A5 (v1 と同一14対象)\"",
  ",\"schema_note\":\"group_order=(3.53) shadow-composition regular rep から実測した GT(N) 本体位数(group_order_theory と突合). phi_image_order=Phi:GT(N)->Aut(PB3/N)の像位数. theta_image_order=group_order/theta_kernel_count(大次数Group()を経由せず元レベルのker(Theta)所属検査で算出。導出不能ならUNKNOWN). derived_length_of_group=本体(composition-table正則表現)のDerivedSubgroup導来長. derived_length_of_image=phi_imageの導来長(v1のderived_lengthに相当). method(B)のL/M5はcomposition_tableから直接構成した本体そのものであり、phi/theta像を別途構成していない(injectivity_information='none'). 設計変更の経緯(6*|A|点規模のGroup()構成でK(11)がOOMした件)はファイル冒頭コメントに記帳.\"",
  ",\"results\":", resultsJson,
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/derived_census_v2_20260729.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
Print("\nDERIVED-CENSUS-V2 DONE\n");
QUIT;
