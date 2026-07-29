#############################################################################
## search/w62-split.g -- W6-2 段 B(分裂判定・新しいプロセスで軽く回す)
##
## 問い: GTSh(N,N) の拡大 1 -> K -> G -> Q -> 1 (K = ker chi~, Q = Im chi~)
##       は分裂するか(K の補群 = Q と同型で K と自明交叉する G の部分群)。
## 入力: search/certs/.w62_shadows_<id>.g(段 A = search/w62-scan.g の出力)
## 出力: search/certs/.w62_part_<id>.json
## 解釈はしない。
#############################################################################
SizeScreen([4096, 0]);;
JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");
Read("search/gaplib_common.g");
Read("search/w62-windows.g");
t0 := GAPLIB_WallElapsedMs();;

wspec := W62_GetWindow();;
Read(Concatenation("search/certs/.w62_shadows_", wspec.id, ".g"));
Print("=== w62-split: ", W62_ID, "  shadows = ", Length(W62_SHADOWS),
      "  scan_mode = ", W62_SCAN_MODE, " ===\n");
W := W62_MakeW(wspec);;
if W.Nord <> W62_NORD then Error("N_ord 不一致"); fi;
corr := Set(List(W62_SHADOWS, s -> [s[1], s[2]]));;
if Length(corr) <> Length(W62_SHADOWS) then Error("shadow 重複"); fi;

gi := GroupOfShadows(W, corr);;
if not gi.closed then Error("(3.53) が閉じない: ", wspec.id); fi;
G := gi.G;;  K := gi.ker;;  regs := gi.regs;;
Print("|G| = ", Size(G), "   |K| = ", Size(K), "   |G|/|K| = ", Size(G)/Size(K), "\n");

isNorm := IsNormal(G, K);;
nh := NaturalHomomorphismByNormalSubgroup(G, K);;
Q := Image(nh);;
Qstruct := StructureDescription(Q);;
Qinv := AbelianInvariants(Q);;
Print("K は G で正規? ", isNorm, "\n");
Print("Q = G/K : |Q| = ", Size(Q), "  構造 = ", Qstruct, "  不変系 = ", Qinv,
      "  可換? ", IsAbelian(Q), "\n");
Print("G 可解? ", IsSolvableGroup(G), "  導来長 = ", DerivedLength(G),
      "   gcd(|K|,|Q|) = ", Gcd(Size(K), Size(Q)), "\n");

isoPc := IsomorphismPcGroup(G);;
Gp := Image(isoPc);;
Kp := Image(isoPc, K);;
comps := ComplementClassesRepresentatives(Gp, Kp);;
nComp := Length(comps);;
splits := (nComp > 0);;
Print("\n**補群のクラス代表 = ", nComp, "  ==> 分裂? ", splits, "**\n");

witJson := "null";;  compStruct := "N/A";;  compOrder := 0;;
if splits then
  H := PreImage(isoPc, comps[1]);;
  compOrder := Size(H);;  compStruct := StructureDescription(H);;
  okOrder := (Size(H) = Size(Q));;
  okInt := (Size(Intersection(H, K)) = 1);;
  okGen := (Size(ClosureGroup(H, K)) = Size(G));;
  okIso := (IsomorphismGroups(H, Q) <> fail);;
  Print("  補群 H: |H| = ", compOrder, " (=|Q|? ", okOrder, ")  構造 = ", compStruct,
        "\n         H cap K = 1? ", okInt, "   <H,K> = G? ", okGen,
        "   H = Q? ", okIso, "\n");
  if not (okOrder and okInt and okGen and okIso) then Error("補群の検証に失敗"); fi;
  gens := SmallGeneratingSet(H);;
  witItems := [];;
  Print("  witness(補群 H の生成元 -> shadow 座標 (m,f)):\n");
  for g in gens do
    p := Position(regs, g);
    if p = fail then Error("補群の生成元が regs に無い"); fi;
    Print("    m = ", corr[p][1], "  u = ", 2*corr[p][1]+1,
          "  u mod 2N_ord = ", (2*corr[p][1]+1) mod (2*W.Nord),
          "  ord_G = ", Order(g), "\n      f = ", corr[p][2], "\n");
    Add(witItems, Concatenation("{\"m\":", String(corr[p][1]),
      ",\"u\":", String(2*corr[p][1]+1),
      ",\"u_mod_2Nord\":", String((2*corr[p][1]+1) mod (2*W.Nord)),
      ",\"order_in_G\":", String(Order(g)),
      ",\"f_perm\":", JStr(String(corr[p][2])), "}"));
  od;
  witJson := JArr(witItems);;
fi;

part := Concatenation(
  "{\"window_id\":", JStr(wspec.id),
  ",\"P\":\"A", String(wspec.n), "\"",
  ",\"N_ord\":", String(W.Nord),
  ",\"scan_mode\":", JStr(W62_SCAN_MODE),
  ",\"scanned_count\":", String(W62_SCANNED),
  ",\"settled_fail_count\":", String(W62_SETTLED_FAIL),
  ",\"shadow_total\":", String(Length(corr)),
  ",\"G_order\":", String(Size(G)),
  ",\"K_order\":", String(Size(K)),
  ",\"Q_order\":", String(Size(Q)),
  ",\"K_normal_in_G\":", JB(isNorm),
  ",\"Q_struct\":", JStr(Qstruct),
  ",\"Q_abelian\":", JB(IsAbelian(Q)),
  ",\"Q_abelian_invariants\":", JArr(List(Qinv, String)),
  ",\"G_solvable\":", JB(IsSolvableGroup(G)),
  ",\"G_derived_length\":", String(DerivedLength(G)),
  ",\"gcd_K_Q\":", String(Gcd(Size(K), Size(Q))),
  ",\"complement_class_count\":", String(nComp),
  ",\"SPLITS\":", JB(splits),
  ",\"complement_order\":", String(compOrder),
  ",\"complement_struct\":", JStr(compStruct),
  ",\"complement_witness_shadow_coords\":", witJson,
  ",\"elapsed_ms\":", String(GAPLIB_WallElapsedMs()-t0), "}");;
WriteFile(Concatenation("search/certs/.w62_part_", wspec.id, ".json"), part);;
Print("\nwrote search/certs/.w62_part_", wspec.id, ".json\n");
Print("elapsed = ", (GAPLIB_WallElapsedMs()-t0)/1000.0, " s\n");
Print("W62_SPLIT_DONE\n");
QUIT;
