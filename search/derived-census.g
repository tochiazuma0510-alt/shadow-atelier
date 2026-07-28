# search/derived-census.g -- I-26 metabelian census(裁定144・ideas_005_panorama.md I-26 節)
#
# Usage: .\gap.ps1 search\derived-census.g
#
# 目的(発注書どおり): atlas の登録済み窓群について GT 群(shadow の群)の導来列の長さを
#   一括計算する。特に M_Q(24)・M3(48)が metabelian か(未判定)が見どころ。
#   構成情報は既存 script(k9-package.g の BuildPn 系・week3-battery-common.g の
#   MakeQ8/MakeGn/MakeHeis/MakeP3/EnumerateReducedHexagon 系・週3バッテリー各段の
#   qrec 構成行)を再利用する。構成不能な対象は UNKNOWN で列挙し、無理に作らない。
#
# 群の実現方法(2通り):
#  (A) K^(n) 系・N_Q・M_Q・N_2・N_3・M_3・N_A・M_A5: EnumerateReducedHexagon(またはA2は
#      word-level prepend版)で得た shadow(m,f)ごとに Phi_{m,f}: x->x^u, y->f^-1 y^u f を
#      qrec.G 上の自己同型として構成し、qrec.G の全元への像から置換を作る(BuildGTPermGroupFromShadows)。
#      得られた置換群 <Phi_{m,f} : shadow> は GT(N) の(単射性が成り立てば忠実な)具体表現。
#  (B) L・M5: 証明書 search/certs 配下ではなく certificates/L01.v1.json・certificates/M01.v1.json
#      が完全な composition_table(GT(N) の乗積表そのもの)を保持しているため、正則置換表現を
#      直接その表から構成する(自己同型を再構成する必要がない・最も安全な経路)。
#
# 宇宙: G_n 系 n=3,5,7,9,11(奇数のみ・K^(n) 族の登録範囲) + week3 registered windows
#   L, M5(=M01), N_Q, M_Q, N_2, N_3, M_3, N_A, M_A5(すべて既存 battery script/証明書に
#   登録済みの対象)。新規対象の追加なし。解釈しない(観測の記録に徹する)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# derived-census.g -- I-26 metabelian census\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

# ====================================================================
# ヘルパー
# ====================================================================

# BuildPn(n) -- k9-package.g より逐語コピー
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

# 導来列の長さ(cap 付き・非可解らしき安定を検知したら正直に印字)
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

# shadow (m,f) の Phi_{m,f} を qrec.G 上の置換として実現し、Group(...) を返す
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

# composition_table (0-indexed [a,b,c] with a.b=c) -> 正則置換表現
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

results := [];;   # each: rec(name, definition, expected_order, observed_order, derived, metabelian, method)

RecordResult := function(name, definition, expectedOrder, GTgrp, method)
  local info, obs, meta;
  obs := Size(GTgrp);;
  info := DerivedInfo(GTgrp);;
  meta := IsMetabelianInfo(info);;
  Add(results, rec(name:=name, definition:=definition, expected_order:=expectedOrder,
       observed_order:=obs, order_match:=(obs = expectedOrder),
       derived_length:=info.derived_length, status:=info.status,
       metabelian:=meta, method:=method));;
  Print("[", PF(obs = expectedOrder), "] ", name, ": |GT| observed=", obs,
        " expected=", expectedOrder, "  derived_length=", info.derived_length,
        " (", info.status, ")  metabelian=", meta, "  [", method, "]\n");
end;;

RecordUnknown := function(name, definition, reason)
  Add(results, rec(name:=name, definition:=definition, expected_order:="UNKNOWN",
       observed_order:="UNKNOWN", order_match:="UNKNOWN",
       derived_length:="UNKNOWN", status:="UNKNOWN", metabelian:="UNKNOWN",
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
  qrec := rec(x:=Pn.X, y:=Pn.Y, G:=Pn.G);;
  Nord := Lcm(Order(Pn.X), Order(Pn.Y));;
  charmingSet := Filtered([0..Nord-1], mm -> Gcd(2*mm+1, Nord) = 1);;
  gtResult := EnumerateReducedHexagon(qrec, charmingSet);;
  phi_n := Length(Filtered([1..n], k -> Gcd(k,n)=1));;
  expectedOrder := 2 * n * phi_n;;
  GTgrp := BuildGTPermGroupFromShadows(qrec, gtResult.shadows);;
  RecordResult(Concatenation("K(", String(n), ")"),
    Concatenation("GT(K^(", String(n), "))"), expectedOrder, GTgrp,
    "Phi_{m,f} perm rep on G_n (BuildPn)");;
od;;

# ====================================================================
# タスク B: week3 registered windows(構成情報の再利用可能な範囲で)
# ====================================================================
Print("\n============================================================\n");
Print("# タスク B: week3 registered windows (L, M5, N_Q, M_Q, N_2, N_3, M_3, N_A, M_A5)\n");
Print("============================================================\n");

# ---- N_Q (stage 1a: Q8) ----
q8rec := MakeQ8();;
qrecNQ := rec(x:=q8rec.x, y:=q8rec.y, G:=q8rec.G);;
NordNQ := Lcm(Order(q8rec.x), Order(q8rec.y));;
charmingNQ := Filtered([0..NordNQ-1], mm -> Gcd(2*mm+1, NordNQ) = 1);;
gtNQ := EnumerateReducedHexagon(qrecNQ, charmingNQ);;
GTgrpNQ := BuildGTPermGroupFromShadows(qrecNQ, gtNQ.shadows);;
RecordResult("N_Q", "pi^{-1}(ker(F2 ->> Q8))", 4, GTgrpNQ,
  "Phi_{m,f} perm rep on Q8 (MakeQ8, stage 1a construction)");;

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
  qrecMQ := rec(x:=xhatMQ, y:=yhatMQ, G:=QM_MQ);;
  NordMQ := Lcm(Order(xhatMQ), Order(yhatMQ));;
  charmingMQ := Filtered([0..NordMQ-1], mm -> Gcd(2*mm+1, NordMQ) = 1);;
  gtMQ := EnumerateReducedHexagon(qrecMQ, charmingMQ);;
  GTgrpMQ := BuildGTPermGroupFromShadows(qrecMQ, gtMQ.shadows);;
  RecordResult("M_Q", "K^(3) cap N_Q", 24, GTgrpMQ,
    "Phi_{m,f} perm rep on Q_M=G3 x_{C2^2} Q8 (17-pt fiber product, stage 1b construction)");;
fi;

# ---- N_2 (stage 2a: P2 = MakeHeis(4,2)) ----
p2rec := MakeHeis(4, 2);;
qrecN2 := rec(x:=p2rec.x, y:=p2rec.y, G:=p2rec.G);;
NordN2 := Lcm(Order(p2rec.x), Order(p2rec.y));;
charmingN2 := Filtered([0..NordN2-1], mm -> Gcd(2*mm+1, NordN2) = 1);;
gtN2 := EnumerateReducedHexagon(qrecN2, charmingN2);;
GTgrpN2 := BuildGTPermGroupFromShadows(qrecN2, gtN2.shadows);;
RecordResult("N_2", "pi^{-1}(F2^4 gamma_3(F2))", 4, GTgrpN2,
  "Phi_{m,f} perm rep on P2=MakeHeis(4,2) (stage 2a construction)");;

# ---- N_3 (stage 2b: P3 = MakeP3()) ----
p3rec := MakeP3();;
qrecN3 := rec(x:=p3rec.x, y:=p3rec.y, G:=p3rec.G);;
NordN3 := Lcm(Order(p3rec.x), Order(p3rec.y));;
charmingN3 := Filtered([0..NordN3-1], mm -> Gcd(2*mm+1, NordN3) = 1);;
gtN3 := EnumerateReducedHexagon(qrecN3, charmingN3);;
GTgrpN3 := BuildGTPermGroupFromShadows(qrecN3, gtN3.shadows);;
RecordResult("N_3", "pi^{-1}(F2^4 gamma_4(F2))", 8, GTgrpN3,
  "Phi_{m,f} perm rep on P3=MakeP3() (stage 2b construction)");;

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
  qrecM3 := rec(x:=xhatM3, y:=yhatM3, G:=QM_M3);;
  NordM3 := Lcm(Order(xhatM3), Order(yhatM3));;
  charmingM3 := Filtered([0..NordM3-1], mm -> Gcd(2*mm+1, NordM3) = 1);;
  gtM3 := EnumerateReducedHexagon(qrecM3, charmingM3);;
  GTgrpM3 := BuildGTPermGroupFromShadows(qrecM3, gtM3.shadows);;
  RecordResult("M_3", "K^(3) cap N_3", 48, GTgrpM3,
    "Phi_{m,f} perm rep on Q_M=G3 x P3 (DirectProduct/Embedding, stage 3 construction)");;
fi;

# ---- N_A (stage A1: A5 direct) ----
XhatA1 := (1,3,2,4,5);;
YhatA1 := (1,3,4,5,2);;
A5grp := Group(XhatA1, YhatA1);;
if Size(A5grp) <> 60 then
  RecordUnknown("N_A", "pi^{-1}(ker(F2 ->> A5))", Concatenation("A5 construction size mismatch: got ",
    String(Size(A5grp))));;
else
  qrecNA := rec(x:=XhatA1, y:=YhatA1, G:=A5grp);;
  NordNA := Lcm(Order(XhatA1), Order(YhatA1));;
  charmingNA := Filtered([0..NordNA-1], mm -> Gcd(2*mm+1, NordNA) = 1);;
  gtNA := EnumerateReducedHexagon(qrecNA, charmingNA);;
  GTgrpNA := BuildGTPermGroupFromShadows(qrecNA, gtNA.shadows);;
  RecordResult("N_A", "pi^{-1}(ker(F2 ->> A5))", 20, GTgrpNA,
    "Phi_{m,f} perm rep on A5=Group(Xhat,Yhat) (stage A1 construction)");;
fi;

# ---- M_A5 (stage A2: A5 x C5, c_in_N=false -> word-level prepend enumeration) ----
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
  qrecMA5 := rec(x:=xhatMA5, y:=yhatMA5, G:=QM_MA5);;
  NordMA5 := Lcm(Order(xhatMA5), Order(yhatMA5));;
  charmingMA5 := Filtered([0..NordMA5-1], mm -> Gcd(2*mm+1, NordMA5) = 1);;
  gtMA5 := EnumerateWordLevelHexagonPrepend(qrecMA5, charmingMA5);;
  GTgrpMA5 := BuildGTPermGroupFromShadows(qrecMA5, gtMA5.shadows);;
  RecordResult("M_A5", "N_A cap N_5 (N_5=ker(beta_5:B3->S3xC5))", 20, GTgrpMA5,
    "Phi_{m,f} perm rep on Q_M=A5 x C5 (stage A2 construction, word-level prepend shadows)");;
fi;

# ---- L (composition_table cert, certificates/L01.v1.json) ----
if not IsExistingFile("certificates/L01.v1.json") then
  RecordUnknown("L", "K^(3) cap N0", "certificates/L01.v1.json not found");;
else
  tblL := ReadCompositionTable("certificates/L01.v1.json");;
  GTgrpL := BuildRegularPermGroupFromTable(tblL, 36);;
  RecordResult("L", "K^(3) cap N0", 36, GTgrpL,
    "regular perm rep from composition_table in certificates/L01.v1.json");;
fi;

# ---- M5 (composition_table cert, certificates/M01.v1.json) ----
if not IsExistingFile("certificates/M01.v1.json") then
  RecordUnknown("M5", "K^(3) cap N5", "certificates/M01.v1.json not found");;
else
  tblM5 := ReadCompositionTable("certificates/M01.v1.json");;
  GTgrpM5 := BuildRegularPermGroupFromTable(tblM5, 48);;
  RecordResult("M5", "K^(3) cap N5", 48, GTgrpM5,
    "regular perm rep from composition_table in certificates/M01.v1.json");;
fi;

# ====================================================================
# 総括表
# ====================================================================
Print("\n############################################################\n");
Print("# 総括: I-26 census 表(対象 x |GT| x 導来長 x metabelian?)\n");
Print("############################################################\n");
Print("name    | definition                          | |GT| obs/exp | derived_len | status | metabelian\n");
for r in results do
  Print(r.name, " | ", r.definition, " | ", r.observed_order, "/", r.expected_order,
        " | ", r.derived_length, " | ", r.status, " | ", r.metabelian, "\n");
od;

t1 := GAPLIB_WallElapsedMs();;
Print("\n経過(壁時計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_census.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

FieldToJson := function(v)
  if v = "UNKNOWN" then return JStr("UNKNOWN"); fi;
  if IsBool(v) then return JB(v); fi;
  if IsString(v) then return JStr(v); fi;
  return String(v);
end;;

ResultToJson := function(r)
  return Concatenation(
    "{\"name\":", JStr(r.name), ",\"definition\":", JStr(r.definition),
    ",\"expected_order\":", FieldToJson(r.expected_order),
    ",\"observed_order\":", FieldToJson(r.observed_order),
    ",\"derived_length\":", FieldToJson(r.derived_length),
    ",\"status\":", JStr(String(r.status)),
    ",\"metabelian\":", FieldToJson(r.metabelian),
    ",\"method\":", JStr(r.method),
    "}"
  );
end;;

resultsJson := JArr(List(results, ResultToJson));;

scriptSha256 := ComputeSha256File("search/derived-census.g");;

cert := Concatenation(
  "{\"schema\":\"derived-census/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/derived-census.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"design_source\":\"ideas/ideas_005_panorama.md I-26 (裁定144 採用)\"",
  ",\"universe\":\"K^(n) n=3,5,7,9,11 + week3 registered windows L,M5,N_Q,M_Q,N_2,N_3,M_3,N_A,M_A5\"",
  ",\"results\":", resultsJson,
  ",\"elapsed_wall_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/derived_census_20260728.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
Print("\nDERIVED-CENSUS DONE\n");
QUIT;
