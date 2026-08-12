# search/frattini_resolution_v4.g -- Frattini 解像度表 v4(裁定1050)
#
# 正本: docs/notes/surg_universality_audit_v1.md §2.4-2.5。
# 1. n=81: G=Aff(Z/81)xC2(|G|=8748)を構成、FrattiniSubgroup->Size->IdGroup(G/Phi)。
#    予言: |Phi|=243・|G/Phi|=36・IdGroup=[36,12] を assert(1行、fail-closedで報告)。
# 2. n=125: 予言 |Phi|=125(5冪の最初の破れ検定)。
# 3. (T1): R:GT(K^(n))->GT(K^(m))(m|n・両奇)の全射性。3冪塔 n=9->m=3 で実測。
# 4. (T3): 自然性四角形(reduce then mod-Phi = mod-Phi then reduce)を小さい対
#    (n=9,m=3)で1例、実測(全元での検算)。
#
# Aff(Z/n) 構成: 度数 n の置換群として t(平行移動 x->x+1)・u(原始根倍 x->g*x)で構成
# (n=p^k, p 奇素数の場合 (Z/n)^x は巡回で PrimitiveRootMod が使える)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

BuildAff := function(n)
  local g, t, u, G;
  g := PrimitiveRootMod(n);;
  if g = fail then Error("BuildAff: no primitive root mod ", n); fi;
  t := PermList(List([0..n-1], x -> ((x+1) mod n) + 1));;
  u := PermList(List([0..n-1], x -> ((g*x) mod n) + 1));;
  G := Group(t, u);;
  return rec(n:=n, g:=g, t:=t, u:=u, G:=G);;
end;;

FrattiniRow := function(name, defn, G, orderTheory)
  local sizeX, phiX, sizePhi, sizeQuot, quotG, quotAbelian, quotAbInv, quotIdGroup, quotIdOk;
  sizeX := Size(G);;
  phiX := FrattiniSubgroup(G);;
  sizePhi := Size(phiX);;
  sizeQuot := sizeX / sizePhi;;
  quotG := G / phiX;;
  quotAbelian := IsAbelian(quotG);;
  quotAbInv := fail;;
  if quotAbelian then quotAbInv := AbelianInvariants(quotG);; fi;
  quotIdGroup := fail;;  quotIdOk := false;;
  if sizeQuot <= 4000 then
    quotIdGroup := IdGroup(quotG);;
    quotIdOk := true;;
  fi;
  return rec(name:=name, defn:=defn, orderTheory:=orderTheory,
             sizeX:=sizeX, sizeMatchesTheory:=(orderTheory=fail or sizeX=orderTheory),
             sizePhi:=sizePhi, sizeQuot:=sizeQuot,
             quotAbelian:=quotAbelian, quotAbInv:=quotAbInv,
             quotIdGroup:=quotIdGroup, quotIdOk:=quotIdOk, phiSubgroup:=phiX, quotGroup:=quotG);;
end;;

Print("############################################################\n");
Print("# frattini_resolution_v4.g -- 裁定1050 追試4本\n");
Print("############################################################\n");
t0 := GAPLIB_WallElapsedMs();;
rows := [];;

# ---- 1. n=81 ----
Print("\n=== [U2-T2-81] G = Aff(Z/81) x C2 構成中 ===\n");
aff81 := BuildAff(81);;
G81 := DirectProduct(aff81.G, CyclicGroup(2));;
Print("|Aff(Z/81)|=", Size(aff81.G), " |G81|=", Size(G81), " (期待 8748)\n");
row81 := FrattiniRow("K(81)_Aff", "Aff(Z/81) x C2", G81, 8748);;
Add(rows, row81);;
Print("|X|=", row81.sizeX, " |Phi(X)|=", row81.sizePhi, " (予言 243) |X/Phi(X)|=", row81.sizeQuot,
      " (予言 36) IdGroup=", row81.quotIdGroup, " (予言 [36,12])\n");
phi81Ok := (row81.sizePhi = 243);;
quot81Ok := (row81.sizeQuot = 36);;
id81Ok := (row81.quotIdOk and row81.quotIdGroup = [36,12]);;
Print("[", PF(phi81Ok), "] |Phi|=243 assert: ", phi81Ok, "\n");
Print("[", PF(quot81Ok), "] |X/Phi|=36 assert: ", quot81Ok, "\n");
Print("[", PF(id81Ok), "] IdGroup(G/Phi)=[36,12] assert: ", id81Ok, "\n");

# ---- 2. n=125 ----
Print("\n=== [n=125 5冪破れ検定] G = Aff(Z/125) x C2 構成中 ===\n");
aff125 := BuildAff(125);;
G125 := DirectProduct(aff125.G, CyclicGroup(2));;
Print("|Aff(Z/125)|=", Size(aff125.G), " |G125|=", Size(G125), " (期待 25000)\n");
row125 := FrattiniRow("K(125)_Aff", "Aff(Z/125) x C2", G125, 25000);;
Add(rows, row125);;
Print("|X|=", row125.sizeX, " |Phi(X)|=", row125.sizePhi, " (予言 125) |X/Phi(X)|=", row125.sizeQuot, "\n");
phi125Ok := (row125.sizePhi = 125);;
Print("[", PF(phi125Ok), "] |Phi|=125 assert: ", phi125Ok, "\n");

# ---- 3. (T1): R: GT(K^(9)) -> GT(K^(3)) 全射性(3冪塔) ----
Print("\n=== (T1) 3冪塔の遷移 R: GT(K^(9)) -> GT(K^(3)) 全射性 ===\n");
aff9 := BuildAff(9);;
aff3 := BuildAff(3);;
G9 := DirectProduct(aff9.G, CyclicGroup(2));;
G3 := DirectProduct(aff3.G, CyclicGroup(2));;
Print("|G9|=", Size(G9), " (期待 108) |G3|=", Size(G3), " (期待 12)\n");

# G9 の生成元(embedding経由): t9,u9 は aff9.G の像、C2生成元は第2因子
emb9_1 := Embedding(G9, 1);;  emb9_2 := Embedding(G9, 2);;
t9img := Image(emb9_1, aff9.t);;  u9img := Image(emb9_1, aff9.u);;
c9img := Image(emb9_2, GeneratorsOfGroup(Source(emb9_2))[1]);;

emb3_1 := Embedding(G3, 1);;  emb3_2 := Embedding(G3, 2);;
t3img := Image(emb3_1, aff3.t);;  u3img := Image(emb3_1, aff3.u);;
c3img := Image(emb3_2, GeneratorsOfGroup(Source(emb3_2))[1]);;

# reduction: t(x->x+1 mod 9) -> t(x->x+1 mod 3)。u(x->g9*x mod 9) -> u(x->(g9 mod 3)*x mod 3)
# (g9 mod 3 は3の原始根であることが期待される奇素数冪の標準事実)
g9mod3 := aff9.g mod 3;;
Print("g9=", aff9.g, " g9 mod 3 = ", g9mod3, " (aff3.g=", aff3.g, ")\n");
# u3img correspond to multiplication by aff3.g; multiplication by g9mod3 is u3img^k for the k with aff3.g^k = g9mod3 mod 3
kFound := fail;;
for kk in [0..1] do
  if PowerMod(aff3.g, kk, 3) = g9mod3 then kFound := kk; break; fi;
od;
if kFound = fail then Error("(T1): could not express g9 mod 3 as a power of aff3.g"); fi;
u9targetImg := u3img^kFound;;

R9to3 := GroupHomomorphismByImages(G9, G3, [t9img, u9img, c9img], [t3img, u9targetImg, c3img]);;
t1Ok := (R9to3 <> fail);;
Print("[", PF(t1Ok), "] GroupHomomorphismByImages(G9->G3) 構成成功: ", t1Ok, "\n");
t1Surj := false;;
if t1Ok then
  t1Surj := IsSurjective(R9to3);;
  Print("[", PF(t1Surj), "] (T1) R: GT(K^(9)) -> GT(K^(3)) は全射: ", t1Surj, "\n");
fi;

# ---- 4. (T3): 自然性四角形の可換実測(n=9,m=3の対で1例、全元検算) ----
Print("\n=== (T3) 自然性四角形の可換実測(n=9,m=3) ===\n");
t3SquareOk := fail;;
if t1Ok then
  phi9 := FrattiniSubgroup(G9);;
  phi3 := FrattiniSubgroup(G3);;
  q9 := NaturalHomomorphismByNormalSubgroup(G9, phi9);;
  q3 := NaturalHomomorphismByNormalSubgroup(G3, phi3);;
  # check: for all g in G9, q3(R9to3(g)) = Rbar(q9(g)) for SOME well-defined Rbar
  # equivalently: R9to3(phi9) subseteq phi3 (this makes the square well-defined/commute)
  phi9ImgInPhi3 := ForAll(GeneratorsOfGroup(phi9), x -> Image(R9to3, x) in phi3);;
  Print("[", PF(phi9ImgInPhi3), "] R(Phi(G9)) subseteq Phi(G3) (四角形が well-defined であるための必要条件): ",
        phi9ImgInPhi3, "\n");
  if phi9ImgInPhi3 then
    # direct elementwise commutativity check over all |G9|=108 elements (small, exhaustive)
    allCommute := ForAll(Elements(G9), g ->
      Image(q3, Image(R9to3, g)) = Image(q3, Image(R9to3, g)));; # trivially true; real check below
    # proper check: build Rbar via images and compare q3(R(g)) to Rbar(q9(g)) for all g
    RbarHom := GroupHomomorphismByImages(Image(q9), Image(q3),
                 List(GeneratorsOfGroup(G9), x -> Image(q9,x)),
                 List(GeneratorsOfGroup(G9), x -> Image(q3, Image(R9to3, x))));;
    if RbarHom = fail then
      Print("[FAIL] induced map Rbar on quotients could not be constructed (generators inconsistent)\n");
      t3SquareOk := false;;
    else
      t3SquareOk := ForAll(Elements(G9), g ->
        Image(q3, Image(R9to3, g)) = Image(RbarHom, Image(q9, g)));;
      Print("[", PF(t3SquareOk), "] (T3) 全 ", Size(G9), " 元で q3.R = Rbar.q9 (可換): ", t3SquareOk, "\n");
    fi;
  fi;
fi;

Print("\n============================================================\n");
Print("# 一覧表\n");
Print("============================================================\n");
Print("name | |X| | |Phi(X)| | |X/Phi(X)| | IdGroup\n");
for r in rows do
  Print(r.name, " | ", r.sizeX, " | ", r.sizePhi, " | ", r.sizeQuot, " | ", r.quotIdGroup, "\n");
od;

# 陽性対照(既存維持): K(9) via shadow-composition (v1/v2/v3 と同一)
posControlNote := "陽性対照(既存v1-v3行の値をここでも再掲): K(9) shadow-composition構成で |X/Phi(X)|=36 (実測済・commit e6ee6089/7136c666)";;
Print("\n", posControlNote, "\n");

t1 := GAPLIB_WallElapsedMs();;
Print("\n総経過 = ", t1-t0, " ms\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_frat4.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

RowJson := function(r)
  local abInvStr, idGroupStr;
  if r.quotAbInv = fail then abInvStr := "null"; else abInvStr := JArr(List(r.quotAbInv,String)); fi;
  if r.quotIdOk then idGroupStr := JArr(List(r.quotIdGroup, String)); else idGroupStr := "null"; fi;
  return Concatenation(
    "{\"name\":\"", r.name, "\",\"definition\":\"", r.defn, "\"",
    ",\"order_theory\":", String(r.orderTheory), ",\"size_X\":", String(r.sizeX),
    ",\"size_matches_theory\":", JB(r.sizeMatchesTheory),
    ",\"size_Phi\":", String(r.sizePhi), ",\"size_X_mod_Phi\":", String(r.sizeQuot),
    ",\"quotient_abelian\":", JB(r.quotAbelian),
    ",\"quotient_abelian_invariants\":", abInvStr,
    ",\"quotient_IdGroup\":", idGroupStr,
    "}"
  );
end;;

scriptSha256 := ComputeSha256File("search/frattini_resolution_v4.g");;

cert := Concatenation(
  "{\"schema\":\"frattini-resolution/v4\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/frattini_resolution_v4.g\",\"order\":\"裁定1050(数学者指示書 surg_universality_audit_v1.md 2.4)\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"rows\":", JArr(List(rows, RowJson)),
  ",\"n81_asserts\":{\"phi_243\":", JB(phi81Ok), ",\"quot_36\":", JB(quot81Ok),
    ",\"idgroup_36_12\":", JB(id81Ok), "}",
  ",\"n125_assert\":{\"phi_125\":", JB(phi125Ok), "}",
  ",\"T1\":{\"hom_constructed\":", JB(t1Ok), ",\"surjective\":", JB(t1Surj), "}",
  ",\"T3\":{\"square_commutes\":", JB(t3SquareOk = true), "}",
  ",\"positive_control_note\":\"", posControlNote, "\"",
  ",\"u_touched\":false,\"c_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"total_elapsed_ms\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/frattini_resolution_v4_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
