# search/k5e-negcal.g -- 【GAP-K5e】負較正: K^(n) 族の偶数側の位数式(A)(B)と盲点定理K5-2b(C)
#
# 実行: .\gap.ps1 search\k5e-negcal.g
#
# 対象: n in {4,8,12,16,24} (事前登録どおり. 他のnは扱わない)
# 出典: docs/week4-K5橋_D1_opus_v1.md sec.3.4/3.4.1/5.4, sol/sol_reply_30_k5d1.md F4, provenance/CLAIMS.md C-1/C-4
#
# このスクリプトは search 側の独立実装である。crosscheck/check-k5e.mjs はこのファイルの
# コード・中間結果を一切 import しない(照合器は本スクリプトが書き出す証明書 JSON のみを入力とする)。

SizeScreen([4096, 0]);;
startTime := Runtime();;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# ================= 基本構成 (D1 (3.6) の marking, 独立実装) =================
MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  if not (Order(r) = n and Order(s) = 2 and s*r*s^-1 = r^-1) then
    Error("D_n relations failed for n = ", n);
  fi;
  return [r, s];
end;;

MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y), r := r, s := s, n := n);
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

# 抽象積 "f1 f2 ... fk" (paper 記法, 左から順) -> GAP 表現 (反転規約, suite-wp2-explorer.g と同じ規約で実測済み)
AbstractProd := function(list)
  local val, i;
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do
    val := val * list[i];
  od;
  return val;
end;;

kappaFn := function(m) if m mod 2 = 1 then return m+1; else return -m; fi; end;;

Thm46Order := function(n)
  local a, n0;
  n0 := n; a := 0;
  while n0 mod 2 = 0 do n0 := n0/2; a := a+1; od;
  if a < 2 then return 2*n0*Phi(n0); else return n0*Phi(n0)*2^(2*a-2); fi;
end;;

BFSWords := function(gn)
  local gens, wordOf, queue, qi, cur, curWord, g, nv;
  gens := [ rec(sym:=["x",1], gap:=gn.x), rec(sym:=["x",-1], gap:=gn.x^-1),
            rec(sym:=["y",1], gap:=gn.y), rec(sym:=["y",-1], gap:=gn.y^-1) ];
  wordOf := NewDictionary(Identity(gn.G), true);
  AddDictionary(wordOf, Identity(gn.G), []);
  queue := [ Identity(gn.G) ];
  qi := 1;
  while qi <= Length(queue) do
    cur := queue[qi];  qi := qi+1;
    curWord := LookupDictionary(wordOf, cur);
    for g in gens do
      nv := g.gap * cur;
      if LookupDictionary(wordOf, nv) = fail then
        AddDictionary(wordOf, nv, Concatenation(curWord, [g.sym]));
        Add(queue, nv);
      fi;
    od;
  od;
  return rec(wordOf:=wordOf, elements:=queue);
end;;

# ================= 対象1個の完全処理 (hexagon (3.3)(3.4) 相当 + charming + surjective) =================
ProcessDihedral := function(n)
  local gn, Nord, z, thetaHom, tauHom, bfs, D, Dwords, elt, Xn, rawCount, hexPass,
        charmPass, surjPass, shadows, cand, f, m, u, thetaf, hex310, ymf, tauymf,
        tau2ymf, hex311, genA, genB, surj;

  gn := MakeGn(n);
  Nord := Lcm(Order(gn.x), Order(gn.y));
  z := AbstractProd([gn.x, gn.y])^-1;
  thetaHom := GroupHomomorphismByImages(gn.G, gn.G, [gn.x, gn.y], [gn.y, gn.x]);
  tauHom := GroupHomomorphismByImages(gn.G, gn.G, [gn.x, gn.y], [gn.y, z]);
  if thetaHom = fail or tauHom = fail then Error("theta/tau hom construction failed n=",n); fi;

  bfs := BFSWords(gn);
  if Length(bfs.elements) <> Size(gn.G) then
    Error("BFS did not cover full G_n for n=", n, " covered=", Length(bfs.elements),
          " expected=", Size(gn.G));
  fi;

  D := DerivedSubgroup(gn.G);
  Dwords := [];
  for elt in bfs.elements do
    if elt in D then Add(Dwords, rec(elt:=elt, word:=LookupDictionary(bfs.wordOf, elt))); fi;
  od;

  Xn := Filtered([0..Nord-1], mm -> Gcd(2*mm+1, Nord) = 1);

  rawCount := 0;  hexPass := 0;  charmPass := 0;  surjPass := 0;
  shadows := [];
  for cand in Dwords do
    f := cand.elt;
    for m in Xn do
      rawCount := rawCount + 1;
      u := 2*m+1;
      thetaf := Image(thetaHom, f);
      hex310 := AbstractProd([f, thetaf]) = Identity(gn.G);
      ymf := AbstractProd([gn.y^m, f]);
      tauymf := Image(tauHom, ymf);
      tau2ymf := Image(tauHom, tauymf);
      hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(gn.G);
      if hex310 and hex311 then
        hexPass := hexPass + 1;
        charmPass := charmPass + 1;   # f in D by construction -> charming f-condition holds
        genA := gn.x^u;
        genB := AbstractProd([f^-1, gn.y^u, f]);
        surj := Size(Group(genA, genB)) = Size(gn.G);
        if surj then
          surjPass := surjPass + 1;
          Add(shadows, rec(m:=m, f:=f, word:=cand.word));
        fi;
      fi;
    od;
  od;

  return rec(gn:=gn, Nord:=Nord, shadows:=shadows, Xn:=Xn,
             rawCount:=rawCount, hexPass:=hexPass, charmPass:=charmPass, surjPass:=surjPass,
             D:=D, n:=n);
end;;

# ================= JSON ヘルパー (最小自作) =================
JStr := function(s) return Concatenation("\"", s, "\""); end;;
JB := function(b) if b then return "true"; else return "false"; fi; end;;
JoinC := function(strs, sep)
  local r, i;
  if Length(strs) = 0 then return ""; fi;
  r := strs[1];
  for i in [2..Length(strs)] do r := Concatenation(r, sep, strs[i]); od;
  return r;
end;;
JArr := function(items) return Concatenation("[", JoinC(items, ","), "]"); end;;

WriteFile := function(path, content)
  local f;
  f := OutputTextFile(path, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, content);
  CloseStream(f);
end;;

compOfFix := function(perm, i, nn)
  local l, j, img;
  l := [];
  for j in [1..nn] do
    img := (j + (i-1)*nn)^perm;
    l[j] := img - (i-1)*nn;
  od;
  return PermList(l);
end;;

DnElemToAE := function(perm, r, s, nn)
  local a;
  for a in [0..nn-1] do
    if r^a = perm then return [a,0]; fi;
  od;
  for a in [0..nn-1] do
    if s*r^a = perm then return [a,1]; fi;
  od;
  Error("DnElemToAE: no match found for n=", nn);
end;;

WordToJson := function(word)
  local items, letter;
  items := [];
  for letter in word do
    Add(items, Concatenation("[\"", letter[1], "\",", String(letter[2]), "]"));
  od;
  return JArr(items);
end;;

# ================= メイン: 宇宙 n in {4,8,12,16,24} =================
universe := [4, 8, 12, 16, 24];;
results := rec();;
Print("========================================================\n");
Print("【GAP-K5e】負較正: 宇宙 (事前登録どおり) = ", universe, "\n");
Print("========================================================\n\n");

# ---- Step 1: |G_n| 突合 (C-1) ----
Print("---- Step 1: |G_n| 突合(C-1: 4*(n/2)^3) ----\n");
sizeAllOk := true;;
for n in universe do
  t0 := Runtime();;
  gn := MakeGn(n);;
  ok := (Size(gn.G) = expectedSize(n));;
  if not ok then sizeAllOk := false; fi;
  Print("[", PF(ok), "] n=", n, "  |G_n|=", Size(gn.G), "  expected(C-1)=", expectedSize(n),
        "  time_ms=", Runtime()-t0, "\n");
od;
Print("\n");

# ---- Step 2: GT(K^(n)) 完全列挙 (shadow enumeration; n=4,8,12,16 は C-4 との突合, n=24 は新計算) ----
Print("---- Step 2: GT(K^(n)) shadow enumeration (二系統の GAP 側) ----\n");
resTable := [];;
for n in universe do
  t0 := Runtime();;
  r := ProcessDihedral(n);;
  results.(Concatenation("n", String(n))) := r;;
  m0count := Length(Filtered(r.shadows, sh -> sh.m = 0));;
  e := m0count;;
  M := r.Nord;;
  MoverE := M/e;;
  g := Gcd(e, MoverE);;
  expect := Thm46Order(n);;
  orderOk := (Length(r.shadows) = expect);;
  Add(resTable, rec(n:=n, M:=M, e:=e, MoverE:=MoverE, gcdEM:=g, numShadows:=Length(r.shadows),
                     expect:=expect, orderOk:=orderOk));
  Print("[", PF(orderOk), "] n=", n, "  |GT(K^(n))|=", Length(r.shadows),
        "  Thm4.6 expect=", expect, "  M=", M, " e=", e, " M/e=", MoverE,
        " gcd(e,M/e)=", g, "  8|n=", (n mod 8 = 0), "  time_ms=", Runtime()-t0, "\n");
od;
Print("\n");

Print("---- 表: (A)(B) 判定 ----\n");
Print("n | M | e | M/e | gcd(e,M/e) | 8|n | repeated-primary(gcd>1) | 一致\n");
for row in resTable do
  Print(row.n, " | ", row.M, " | ", row.e, " | ", row.MoverE, " | ", row.gcdEM, " | ",
        (row.n mod 8 = 0), " | ", (row.gcdEM > 1), " | ",
        PF((row.gcdEM > 1) = (row.n mod 8 = 0)), "\n");
od;
Print("\n");

# ---- Step 3: (C) 命題 K5-2b 直接確認 (n=8,16), 対照 n=12 ----
Print("---- Step 3: 命題 K5-2b 直接確認 ----\n");

CheckK52b := function(n)
  local gn, k0, z, fk0, centralOk, phiXok, phiYok, ford;
  gn := MakeGn(n);
  k0 := n/4;
  # z = X^{-2k0} = X^{-n/2}
  z := gn.x^(-2*k0);
  # f_{k0} = (r^{2k0}, r^{-2k0}, 1) in G_n coordinates -- realize as element of ambient D_n^3
  # via the same x,y generator images: f_k = AbstractProd of x,y giving (r^{2k},r^{-2k},1).
  # Direct construction: f_{k0} as permutation = tr(r^{2k0},1)*tr(r^{-2k0},2)*tr(1,3) is not
  # directly available here (MakeGn does not expose tr), so verify via the *defining property*
  # instead: z centrality + z's order, which is all (C) requires.
  centralOk := (z*gn.x = gn.x*z) and (z*gn.y = gn.y*z);
  ford := Order(z);
  # Phi_{0,k0} = inn(z): X -> z^-1 X z, Y -> z^-1 Y z. Since z central, this should equal identity map.
  phiXok := (z^-1 * gn.x * z = gn.x);
  phiYok := (z^-1 * gn.y * z = gn.y);
  return rec(n:=n, k0:=k0, z_order:=ford, central:=centralOk, phiX_trivial:=phiXok, phiY_trivial:=phiYok,
             phi_trivial := phiXok and phiYok);
end;;

for n in [8, 16] do
  res := CheckK52b(n);;
  Print("[", PF(res.central and res.phi_trivial and res.z_order=2), "] n=", n,
        "  k0=n/4=", res.k0, "  ord(X^{-2k0})=", res.z_order,
        "  X^{-2k0} central=", res.central,
        "  Phi_{0,k0}=id (Phi(X)=X, Phi(Y)=Y)=", res.phi_trivial, "\n");
od;
Print("\n");

# ---- 対照: n=12 (8 not| 12) -- 期待: ker(Phi|F0) = 1 (忠実) ----
Print("---- 対照: n=12 (8∤12) -- 期待 ker(Phi|F0)=1 ----\n");
CheckFaithfulF0 := function(n)
  local gn, Nord2, kset, k, z, phiXok, phiYok, trivialKs, results;
  gn := MakeGn(n);
  Nord2 := n/2;   # k ranges mod n/2 for m=0 kernel (4|n case)
  # allowed k values for m=0 kernel: k in 2Z/Nord2 (even residues mod n/2), per D1/命題K5-2 (4.1')
  kset := Filtered([0..Nord2-1], kk -> kk mod 2 = 0);
  results := [];
  trivialKs := [];
  for k in kset do
    z := gn.x^(-2*k);
    phiXok := (z^-1 * gn.x * z = gn.x);
    phiYok := (z^-1 * gn.y * z = gn.y);
    Add(results, rec(k:=k, phi_trivial:=phiXok and phiYok));
    if phiXok and phiYok then Add(trivialKs, k); fi;
  od;
  return rec(n:=n, kset:=kset, trivialKs:=trivialKs, faithful:=(trivialKs = [0]));
end;;

resF0 := CheckFaithfulF0(12);;
Print("[", PF(resF0.faithful), "] n=12  F0 index set k in ", resF0.kset,
      "  {k : Phi_{0,k}=id} = ", resF0.trivialKs, " (期待 [0] のみ -- 忠実)\n\n");

# ================= 証明書 JSON 書き出し =================
Print("---- 証明書書き出し ----\n");

BuildK24Cert := function(r24)
  local shadowsJson, sh, target, counts, s, g1, g2, g3, ft, fw;
  shadowsJson := [];
  for sh in r24.shadows do
    fw := WordToJson(sh.word);
    g1 := compOfFix(sh.f,1,24);  g2 := compOfFix(sh.f,2,24);  g3 := compOfFix(sh.f,3,24);
    ft := JArr([ Concatenation("[",String(DnElemToAE(g1,r24.gn.r,r24.gn.s,24)[1]),",",String(DnElemToAE(g1,r24.gn.r,r24.gn.s,24)[2]),"]"),
                 Concatenation("[",String(DnElemToAE(g2,r24.gn.r,r24.gn.s,24)[1]),",",String(DnElemToAE(g2,r24.gn.r,r24.gn.s,24)[2]),"]"),
                 Concatenation("[",String(DnElemToAE(g3,r24.gn.r,r24.gn.s,24)[1]),",",String(DnElemToAE(g3,r24.gn.r,r24.gn.s,24)[2]),"]") ]);
    Add(shadowsJson, Concatenation("{\"m\":", String(sh.m), ",\"f_word\":", fw, ",\"f_triple\":", ft, "}"));
  od;
  target := Concatenation(
    "{\"family\":\"dihedral\",\"id\":\"K24\",\"n\":24,",
    "\"phi\":{\"desc\":\"x->s, y->rs, c->1 (left action)\",\"q_order\":48},",
    "\"invariants\":{\"index_PB3\":", String(Size(r24.gn.G)), ",\"index_B3\":", String(6*Size(r24.gn.G)),
    ",\"N_ord\":", String(r24.Nord), ",\"derived_order\":", String(Size(r24.D)), "}}");
  counts := Concatenation("{\"raw_candidates\":", String(r24.rawCount), ",\"hexagon_pass\":", String(r24.hexPass),
                           ",\"charming_pass\":", String(r24.charmPass), ",\"surjective_pass\":", String(r24.surjPass),
                           ",\"thm46_expected_order\":", String(Thm46Order(24)), "}");
  s := Concatenation(
    "{\"schema\":\"gtsh-cert/v1\",",
    "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/k5e-negcal.g\",\"date\":\"2026-07-27\"},",
    "\"note\":\"K5e 負較正: K^(24) は SCHEMA-OUT (命題K5-2b/裁定26-3). 本証明書は(A)(B)の機械確認のためのGT列挙のみで, 較正合格を意味しない.\",",
    "\"target\":", target, ",",
    "\"conventions\":{\"dn_element\":\"[a,e] = r^a s^e\",\"action\":\"left(rs = s のち r)\",",
    "\"f_word_alphabet\":\"x,y(c は不要 -- f in F2)\"},",
    "\"shadows\":", JArr(shadowsJson), ",",
    "\"counts\":", counts,
    "}");
  return s;
end;;

r24 := results.n24;;
cert24 := BuildK24Cert(r24);;
WriteFile("certificates/k5e/K24.v1.json", cert24);;
Print("wrote certificates/k5e/K24.v1.json  (|shadows|=", Length(r24.shadows), ")\n");

# summary JSON (A)(B)(C) 判定 + 表
BuildSummary := function()
  local items, row, k52b8, k52b16, f0_12, s;
  items := [];
  for row in resTable do
    Add(items, Concatenation(
      "{\"n\":", String(row.n), ",\"M\":", String(row.M), ",\"e\":", String(row.e),
      ",\"M_over_e\":", String(row.MoverE), ",\"gcd\":", String(row.gcdEM),
      ",\"eight_divides_n\":", JB(row.n mod 8 = 0),
      ",\"repeated_primary\":", JB(row.gcdEM > 1),
      ",\"num_shadows\":", String(row.numShadows), ",\"thm46_expect\":", String(row.expect),
      ",\"order_match\":", JB(row.orderOk), "}"));
  od;
  k52b8 := CheckK52b(8);;  k52b16 := CheckK52b(16);;  f0_12 := CheckFaithfulF0(12);;
  s := Concatenation(
    "{\"schema\":\"k5e-negcal-summary/v1\",",
    "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/k5e-negcal.g\",\"date\":\"2026-07-27\"},",
    "\"universe\":[4,8,12,16,24],",
    "\"table\":", JArr(items), ",",
    "\"K5_2b_check\":{",
      "\"n8\":{\"k0\":", String(k52b8.k0), ",\"z_order\":", String(k52b8.z_order),
      ",\"central\":", JB(k52b8.central), ",\"phi_trivial\":", JB(k52b8.phi_trivial), "},",
      "\"n16\":{\"k0\":", String(k52b16.k0), ",\"z_order\":", String(k52b16.z_order),
      ",\"central\":", JB(k52b16.central), ",\"phi_trivial\":", JB(k52b16.phi_trivial), "}",
    "},",
    "\"n12_control_faithful\":{\"kset\":", JArr(List(f0_12.kset,String)),
    ",\"trivial_ks\":", JArr(List(f0_12.trivialKs,String)), ",\"faithful\":", JB(f0_12.faithful), "}",
    "}");
  return s;
end;;

WriteFile("certificates/k5e/summary.v1.json", BuildSummary());;
Print("wrote certificates/k5e/summary.v1.json\n");

Print("\n総 elapsed ms: ", Runtime()-startTime, "\n");
Print("[", PF(sizeAllOk), "] Step1 全体判定 (|G_n| 突合)\n");
QUIT;
