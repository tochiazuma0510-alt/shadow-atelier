# search/qa-orbit-count.g -- Q-A 実装: GT(K^(n)) の marking 空間への作用の軌道数(n=3,5)
#
# 実行: .\gap.ps1 search\qa-orbit-count.g
#
# 問い(ideas/ideas_005_panorama.md「誰も聞いていない問い Q-A」・裁定144で台帳登録):
#   marking 空間 Epi(F_2, G_n)/Inn(G_n)(= 正則 dessin G_n の framing 類・有限集合)の上に、
#   GT(K^(n)) は Phi-fam(単射・紙上PASS)経由で作用する。この作用の軌道数・軌道サイズ
#   分布を GAP で数える(Galois 側との比較はしない --- 数えるだけ)。
#
# 構成(自己完結・既存基盤の再利用):
#   G_n = search/k9-package.g / search/c1-class-check.g と同一の BuildPn(n) パターン
#     (座標辞書 a_i, q_i・X=a1 q1, Y=a1 a2 a3 q2、MakeGn 慣例との突き合わせつき)。
#   GT(K^(n)) の列挙 = search/week3-battery-common.g の EnumerateReducedHexagon
#     (search/k9-package.g タスク1と同一手続き --- c_in_N=true の quotient-shortcut)。
#   Phi_{m,f} の構成 = search/k9-package.g タスク2 補足(裁定109 F10/F11 修理後)と
#     同一規約: PhiHom(X,Y) = (X^u, AbstractProd([f^-1, Y^u, f]))(u=2m+1)。
#
# marking 空間の効率的な構成(直接 |G|^2 対を数えるのではなく、共役類代表 + その
# 中心化群の軌道に還元 --- n=5 で |G|=500 のときの直接全探索(250000対)を避ける):
#   E := {(x,y) in GxG : <x,y>=G}(Epi(F_2,G))。Inn(G)=G が (x,y) に同時共役で作用する。
#   任意の (x,y) は、x の共役類代表 x0 と、C_G(x0) による y の共役軌道の代表 y0 とに
#   一意に(Inn-軌道として)還元できる。ゆえに F:=E/Inn の代表元は
#     { (x0,y0) : x0 は共役類代表、y0 は C_G(x0)-軌道代表、<x0,y0>=G }
#   として直接構成できる(全 |G|^2 対を試す必要がない)。
#
# GT(K^(n)) の作用(well-defined性の一行証明): Phi_{m,f} は G_n の自己同型であり
#   (search/k9-package.g タスク2補足で全 shadow について IsBijective を確認済みの
#   同一構成)、Inn(G)-同時共役と可換に post-compose する:
#     Phi(h(x,y)h^-1) = Phi(h)(Phi(x),Phi(y))Phi(h)^-1
#   なので [(x,y)] -> [(Phi(x),Phi(y))] は E/Inn 上で well-defined。
#
# 宇宙: n=3, n=5 のみ(発注書の事前登録どおり)。Galois 側との比較はしない
#   (数えるだけ・解釈しない)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

Print("############################################################\n");
Print("# qa-orbit-count.g -- Q-A: GT(K^(n)) の marking 空間への作用の軌道数(n=3,5)\n");
Print("############################################################\n");

t0 := GAPLIB_WallElapsedMs();;

# ====================================================================
# 共通構成(search/k9-package.g / search/c1-class-check.g と同一パターン)
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
  if X <> Xchk then
    Error("BuildPn: X = AbstractProd([a1,q1]) does not match MakeGn convention for n=", n);
  fi;
  if Y <> Ychk then
    Error("BuildPn: Y = AbstractProd([a1,a2,a3,q2]) does not match MakeGn convention for n=", n);
  fi;
  Gfull := Group(a1, a2, a3, q1, q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, q3:=q3, X:=X, Y:=Y, G:=Gfull);
end;;

expectedSize := function(n)
  if n mod 2 = 1 then return 4*n^3; else return 4*(n/2)^3; fi;
end;;

# ====================================================================
# Epi(F_2,G)/Inn(G) の代表元集合 F の構成(共役類 x 中心化群軌道 に還元)
# ====================================================================
BuildEpiInnBlocks := function(G)
  local classes, elts, blocks, ci, cls, x0, C, orbs, orb, y0;
  classes := ConjugacyClasses(G);;
  elts := Elements(G);;
  blocks := [];;
  for ci in [1..Length(classes)] do
    cls := classes[ci];;
    x0 := Representative(cls);;
    C := Centralizer(G, x0);;
    orbs := Orbits(C, elts, OnPoints);;
    for orb in orbs do
      y0 := orb[1];;
      if Size(Group(x0, y0)) = Size(G) then
        Add(blocks, rec(classIndex:=ci, x0:=x0, y0:=y0, orbit:=orb, centralizer:=C));
      fi;
    od;
  od;
  return rec(G:=G, classes:=classes, blocks:=blocks);
end;;

# 任意の生成対 (xp,yp)(in E)が属する block の index を特定する。
LocateBlock := function(data, xp, yp)
  local classes, ci, found, x0, g0, ypp, bi, blk;
  classes := data.classes;;
  found := fail;;
  for ci in [1..Length(classes)] do
    if xp in classes[ci] then found := ci; break; fi;
  od;
  if found = fail then
    Error("LocateBlock: xp not found in any conjugacy class (not in G or bug)");
  fi;
  x0 := Representative(classes[found]);;
  g0 := RepresentativeAction(data.G, x0, xp, OnPoints);;
  if g0 = fail then
    Error("LocateBlock: RepresentativeAction failed unexpectedly (x0, xp same class but no witness)");
  fi;
  ypp := yp^(g0^-1);;
  for bi in [1..Length(data.blocks)] do
    blk := data.blocks[bi];;
    if blk.classIndex = found and ypp in blk.orbit then
      return bi;
    fi;
  od;
  Error("LocateBlock: image pair not located in any block (well-definedness bug or (xp,yp) not in E)");
end;;

# ====================================================================
# 本体: n ごとに実行
# ====================================================================
resultsJson := [];;
overallFailures := 0;;

RunForN := function(n)
  local P, G, sz, okSize, Nord, charmingSet, qrec, gtResult, data, nBlocks,
        shadowPerms, sh, u, PhiHom, phiOk, bijOk, permImages, bi, blk, xImg, yImg, targetBi,
        anomalies, identityShadowIdx, identityPermOk, permObjs, s, HGrp, orbitsF, orbSizes,
        tRunStart, tRunEnd, jsonEntry, sizeDistCounts, sd, sortedOrbSizes, distinctSizes, cnt;

  tRunStart := GAPLIB_WallElapsedMs();;
  Print("\n============================================================\n");
  Print("# n = ", n, "\n");
  Print("============================================================\n");

  P := BuildPn(n);;
  G := P.G;;
  sz := Size(G);;
  okSize := (sz = expectedSize(n));;
  Print("[", PF(okSize), "] |G_", n, "| = ", sz, " (期待 ", expectedSize(n), ")\n");
  if not okSize then overallFailures := overallFailures + 1; fi;

  # ---- Epi/Inn の代表元集合 F ----
  data := BuildEpiInnBlocks(G);;
  nBlocks := Length(data.blocks);;
  Print("marking 空間 |Epi(F_2,G_", n, ")/Inn(G_", n, ")| = |F| = ", nBlocks,
        "  (共役類数=", Length(data.classes), ")\n");

  # ---- GT(K^(n)) の列挙(EnumerateReducedHexagon 再利用) ----
  Nord := Lcm(Order(P.X), Order(P.Y));;
  charmingSet := Filtered([0..Nord-1], m -> Gcd(2*m+1, Nord) = 1);;
  qrec := rec(x:=P.X, y:=P.Y, G:=G);;
  gtResult := EnumerateReducedHexagon(qrec, charmingSet);;
  Print("N_ord = ", Nord, "  charming set = ", charmingSet, "\n");
  Print("実測 |GT(K^(", n, "))| = ", gtResult.shadow_total, "\n");
  Print("理論値(Thm 4.3, alpha=0): 2*n*phi(n) = ", 2*n*Length(Filtered([1..n], k->Gcd(k,n)=1)), "\n");

  # ---- 各 shadow に対する Phi_{m,f} の marking 空間への作用 ----
  permImages := List([1..nBlocks], i -> 0);;
  permObjs := [];;
  anomalies := 0;;
  identityShadowIdx := fail;;
  for sh in gtResult.shadows do
    u := 2*sh.m + 1;;
    PhiHom := GroupHomomorphismByImages(G, G, [P.X, P.Y], [P.X^u, AbstractProd([sh.f^-1, P.Y^u, sh.f])]);;
    phiOk := (PhiHom <> fail);;
    bijOk := phiOk and IsBijective(PhiHom);;
    if not bijOk then
      anomalies := anomalies + 1;
      Print("[ANOMALY] m=", sh.m, ": Phi_{m,f} が自己同型として構成できない",
            " (hom_ok=", phiOk, " bijective=", bijOk, ") --- この shadow の作用は計算不能\n");
    else
      permImages := List([1..nBlocks], i -> 0);;
      for bi in [1..nBlocks] do
        blk := data.blocks[bi];;
        xImg := Image(PhiHom, blk.x0);;
        yImg := Image(PhiHom, blk.y0);;
        targetBi := LocateBlock(data, xImg, yImg);;
        permImages[bi] := targetBi;;
      od;
      s := PermList(permImages);;
      if s = fail then
        Error("RunForN: shadow m=", sh.m, " gave non-bijective image list on F (bug in construction)");
      fi;
      Add(permObjs, s);;
      if sh.m = 0 and Size(Group(sh.f)) = 1 then
        identityShadowIdx := Length(permObjs);;
      fi;
    fi;
  od;
  Print("[", PF(anomalies = 0), "] 全 ", Length(gtResult.shadows), " shadow 中 ", anomalies,
        " 件が自己同型構成に失敗(0 が期待)\n");
  if anomalies <> 0 then overallFailures := overallFailures + 1; fi;

  # identity shadow (m=0,f=1) がある場合、その置換は id(=[1..nBlocks])であるべき(健全性検査)
  identityPermOk := true;;
  if identityShadowIdx <> fail then
    identityPermOk := (permObjs[identityShadowIdx] = ());;
    Print("[", PF(identityPermOk), "] identity shadow (m=0,f=1) の marking 空間への作用 = 恒等置換\n");
    if not identityPermOk then overallFailures := overallFailures + 1; fi;
  else
    Print("[UNKNOWN] identity shadow (m=0,f=1) が shadow 列に見当たらず健全性検査をスキップ\n");
  fi;

  # ---- 軌道の計算 ----
  if Length(permObjs) = 0 then
    HGrp := Group(());;
  else
    HGrp := Group(permObjs);;
  fi;
  orbitsF := Orbits(HGrp, [1..nBlocks], OnPoints);;
  orbSizes := List(orbitsF, Length);;
  Sort(orbSizes);;
  Print("marking 空間上の実現された置換群 |Image(GT(K^(", n, ")) -> Sym(F))| = ", Size(HGrp),
        " (|GT|=", gtResult.shadow_total, "; 一致すれば単射、小さければ非単射)\n");
  Print("GT(K^(", n, ")) 軌道数 = ", Length(orbitsF), "\n");
  Print("軌道サイズ分布(昇順) = ", orbSizes, "\n");

  # サイズ別集計(distinct size -> count)
  sizeDistCounts := [];;
  distinctSizes := Set(orbSizes);;
  for sd in distinctSizes do
    cnt := Length(Filtered(orbSizes, x -> x = sd));;
    Add(sizeDistCounts, rec(size:=sd, count:=cnt));
  od;

  tRunEnd := GAPLIB_WallElapsedMs();;
  Print("経過(壁時計, n=", n, ") = ", (tRunEnd-tRunStart)/1000.0, " s\n");

  return rec(
    n := n,
    g_size := sz, g_size_expected := expectedSize(n), g_size_pass := okSize,
    n_conjugacy_classes := Length(data.classes),
    marking_space_size := nBlocks,
    n_ord := Nord, charming_set := charmingSet,
    gt_order_observed := gtResult.shadow_total,
    gt_order_theoretical := 2*n*Length(Filtered([1..n], k->Gcd(k,n)=1)),
    shadow_anomalies := anomalies,
    identity_shadow_found := (identityShadowIdx <> fail),
    identity_shadow_acts_trivially := identityPermOk,
    image_group_size := Size(HGrp),
    orbit_count := Length(orbitsF),
    orbit_sizes_sorted := orbSizes,
    size_distribution := sizeDistCounts,
    elapsed_ms := tRunEnd - tRunStart
  );
end;;

resultN3 := RunForN(3);;
resultN5 := RunForN(5);;

# ====================================================================
# 総括
# ====================================================================
Print("\n############################################################\n");
if overallFailures = 0 then
  Print("QA-ORBIT-COUNT ALL STRUCTURAL CHECKS PASSED\n");
else
  Print("QA-ORBIT-COUNT STRUCTURAL FAILURES: ", overallFailures, "\n");
fi;

t1 := GAPLIB_WallElapsedMs();;
Print("経過(壁時計、総計) = ", (t1-t0)/1000.0, " s\n");

# ====================================================================
# 証明書 JSON
# ====================================================================
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_qa.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

IntListToJson := function(lst) return JArr(List(lst, String)); end;;

SizeDistToJson := function(lst)
  local parts, e;
  parts := [];
  for e in lst do
    Add(parts, Concatenation("{\"size\":", String(e.size), ",\"count\":", String(e.count), "}"));
  od;
  return JArr(parts);
end;;

ResultToJson := function(r)
  return Concatenation(
    "{\"n\":", String(r.n),
    ",\"g_size\":", String(r.g_size), ",\"g_size_expected\":", String(r.g_size_expected),
    ",\"g_size_pass\":", JB(r.g_size_pass),
    ",\"n_conjugacy_classes\":", String(r.n_conjugacy_classes),
    ",\"marking_space_size\":", String(r.marking_space_size),
    ",\"n_ord\":", String(r.n_ord), ",\"charming_set\":", IntListToJson(r.charming_set),
    ",\"gt_order_observed\":", String(r.gt_order_observed),
    ",\"gt_order_theoretical\":", String(r.gt_order_theoretical),
    ",\"shadow_anomalies\":", String(r.shadow_anomalies),
    ",\"identity_shadow_found\":", JB(r.identity_shadow_found),
    ",\"identity_shadow_acts_trivially\":", JB(r.identity_shadow_acts_trivially),
    ",\"image_group_size\":", String(r.image_group_size),
    ",\"orbit_count\":", String(r.orbit_count),
    ",\"orbit_sizes_sorted\":", IntListToJson(r.orbit_sizes_sorted),
    ",\"size_distribution\":", SizeDistToJson(r.size_distribution),
    ",\"elapsed_ms\":", String(r.elapsed_ms),
    "}"
  );
end;;

scriptSha256 := ComputeSha256File("search/qa-orbit-count.g");;

cert := Concatenation(
  "{\"schema\":\"qa-orbit-count/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/qa-orbit-count.g\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"universe\":{\"n_values\":[3,5]}",
  ",\"question\":\"ideas/ideas_005_panorama.md Q-A (裁定144: GT側census). marking space",
   " Epi(F_2,G_n)/Inn(G_n) 上の GT(K^(n)) 作用の軌道数・サイズ分布を数える(Galois 側との",
   " 比較はしない・解釈しない)\"",
  ",\"results\":[", ResultToJson(resultN3), ",", ResultToJson(resultN5), "]",
  ",\"overall_structural_failures\":", String(overallFailures),
  ",\"elapsed_wall_ms_total\":", String(t1-t0),
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/qa_orbit_count_20260729.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");

Print("\nQA-ORBIT-COUNT DONE\n");
QUIT;
