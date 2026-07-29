#############################################################################
## search/_probe_structthm_witness.g -- 構造定理試行 第 2 段(W4・数学者)
##
## 目的:
##  (a) G ≅ D₈ × Hol(Z/N_ord) を同型で確定(第 1 段の X = C11:C10 / C13:C12 /
##      (C5:C4)xS3 が全て Hol(C_N) に見えることの検証)
##  (b) 司令塔 I7-1 の項目②: 「K の補群 H を C_G(D₈) の内部に取り直せるか」を
##      直接判定し、取り直した H の shadow 座標 (m,u,f) を witness として出す
##  (c) D₈ 因子の shadow 座標(どの f が 2-部分か)
##  (d) u = -1(複素共役)を持つ shadow の位数と D₈ 中心化性
##
## 入力: search/certs/.w62_shadows_<id>.g   出力: 標準出力 + .structthm_wit_<id>.json
#############################################################################
SizeScreen([4096, 0]);;
JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");
Read("search/gaplib_common.g");
Read("search/w62-windows.g");
t0 := GAPLIB_WallElapsedMs();;

wspec := W62_GetWindow();;
Read(Concatenation("search/certs/.w62_shadows_", wspec.id, ".g"));
W := W62_MakeW(wspec);;
corr := Set(List(W62_SHADOWS, s -> [s[1], s[2]]));;
gi := GroupOfShadows(W, corr);;
G := gi.G;;  K := gi.ker;;  regs := gi.regs;;
Nord := W.Nord;;
Print("=== structthm-witness: ", W62_ID, "  |G| = ", Size(G), "  N_ord = ", Nord, " ===\n");

D8 := SylowSubgroup(K, 2);;
oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
CN := Subgroup(K, Concatenation(List(oddp, p -> GeneratorsOfGroup(SylowSubgroup(K, p)))));;
CG := Centralizer(G, D8);;

## ---- (a) D8 x Hol(Z/N) との同型 --------------------------------------------
CNc := CyclicGroup(Nord);;
Aut := AutomorphismGroup(CNc);;
Hol := SemidirectProduct(Aut, IdentityMapping(Aut), CNc);;
Cand := DirectProduct(DihedralGroup(8), Hol);;
isoHol := IsomorphismGroups(G, Cand);;
Print("\n(a) |Hol(Z/", Nord, ")| = ", Size(Hol), " = ", StructureDescription(Hol), "\n");
Print("    |D8 x Hol| = ", Size(Cand), "   **G ≅ D8 x Hol(Z/N_ord) ?  ",
      isoHol <> fail, "**\n");

## ---- (b) C_G(D8) の内部に K の補群を取り直せるか ----------------------------
isoPc := IsomorphismPcGroup(G);;
Gp := Image(isoPc);;  Kp := Image(isoPc, K);;  CGp := Image(isoPc, CG);;  D8p := Image(isoPc, D8);;
KcapC := Intersection(CGp, Kp);;
compsAll := ComplementClassesRepresentatives(Gp, Kp);;
compsIn := ComplementClassesRepresentatives(CGp, KcapC);;
Print("\n(b) K の補群クラス(G 全体)= ", Length(compsAll),
      "   C_G(D8) 内に取り直した補群クラス = ", Length(compsIn), "\n");
Print("    |C_G(D8) cap K| = ", Size(KcapC), " (= 2*N_ord = ", 2*Nord, " ?  ",
      Size(KcapC) = 2*Nord, ")\n");
nCentral := Length(Filtered(compsAll, H -> IsTrivial(CommutatorSubgroup(H, D8p))));;
Print("    G 全体の補群クラスのうち D8 を中心化するもの = ", nCentral, " / ", Length(compsAll), "\n");
witItems := [];;
if Length(compsIn) > 0 then
  H := PreImage(isoPc, compsIn[1]);
  Print("    取り直した H: |H| = ", Size(H), "  構造 = ", StructureDescription(H),
        "   [H,D8] = 1? ", IsTrivial(CommutatorSubgroup(H, D8)),
        "   H cap K = ", Size(Intersection(H, K)), "\n");
  Print("    witness (m, u, ord_G, f):\n");
  for g in SmallGeneratingSet(H) do
    p := Position(regs, g);
    if p = fail then Error("witness が regs に無い"); fi;
    Print("      m = ", corr[p][1], "   u = ", (2*corr[p][1]+1) mod (2*Nord),
          "   ord_G = ", Order(g), "\n        f = ", corr[p][2], "\n");
    Add(witItems, Concatenation("{\"m\":", String(corr[p][1]),
      ",\"u\":", String((2*corr[p][1]+1) mod (2*Nord)),
      ",\"order_in_G\":", String(Order(g)),
      ",\"f_perm\":", JStr(String(corr[p][2])), "}"));
  od;
fi;

## ---- (c) D8 因子の shadow 座標 ----------------------------------------------
Print("\n(c) D8 = Syl_2(ker chi~) の shadow 座標(全て m = 0):\n");
d8items := [];;
for g in GeneratorsOfGroup(D8) do
  p := Position(regs, g);
  Print("      ord = ", Order(g), "   f = ", corr[p][2], "\n");
  Add(d8items, Concatenation("{\"order\":", String(Order(g)),
      ",\"f_perm\":", JStr(String(corr[p][2])), "}"));
od;

## ---- (d) u = -1 の shadow ---------------------------------------------------
mneg := ((-1 - 1)/2) mod Nord;;   # u = 2m+1 = -1 mod ...  -> m = -1 mod Nord
negIdx := Filtered([1 .. Length(corr)], i -> corr[i][1] = mneg);;
Print("\n(d) u = -1 (m = ", mneg, ") の shadow: ", Length(negIdx), " 個\n");
negItems := [];;
nOrd2Centr := 0;;
for i in negIdx do
  g := regs[i];
  cz := IsTrivial(CommutatorSubgroup(Group(g), D8));
  if Order(g) = 2 and cz then nOrd2Centr := nOrd2Centr + 1; fi;
  Print("      ord_G = ", Order(g), "   D8 を中心化? ", cz,
        "   f = 1? ", IsOne(corr[i][2]), "\n");
  Add(negItems, Concatenation("{\"order_in_G\":", String(Order(g)),
      ",\"centralizes_D8\":", JB(cz), ",\"f_is_one\":", JB(IsOne(corr[i][2])), "}"));
od;
Print("    位数 2 かつ D8 中心化の u=-1 shadow 個数 = ", nOrd2Centr, "\n");

## ---- (e) Q の C_N 上の作用は忠実か(Hol である条件)------------------------
nh := NaturalHomomorphismByNormalSubgroup(G, K);;
Q := Image(nh);;
actKer := Size(Centralizer(G, CN)) * Size(Q) / Size(G);;
Print("\n(e) |C_G(C_N)| = ", Size(Centralizer(G, CN)),
      "   Q の C_N 上の作用の核の位数 = ", Size(Centralizer(G, CN))/Size(K),
      "  (1 なら忠実 = Aut(C_N) 全体)\n");
Print("    |Q| = ", Size(Q), "   phi(N_ord) = ", Phi(Nord), "   一致? ", Size(Q) = Phi(Nord), "\n");

js := Concatenation("{\"schema\":\"structthm-witness/v1\"",
  ",\"window_id\":", JStr(wspec.id),
  ",\"N_ord\":", String(Nord),
  ",\"G_iso_D8_x_Hol\":", JB(isoHol <> fail),
  ",\"Hol_struct\":", JStr(StructureDescription(Hol)),
  ",\"complement_classes_all\":", String(Length(compsAll)),
  ",\"complement_classes_in_CG_D8\":", String(Length(compsIn)),
  ",\"complement_classes_centralizing_D8\":", String(nCentral),
  ",\"complement_witness_in_CG_D8\":", JArr(witItems),
  ",\"D8_generators\":", JArr(d8items),
  ",\"u_minus1_shadows\":", JArr(negItems),
  ",\"u_minus1_order2_centralizing_count\":", String(nOrd2Centr),
  ",\"Q_order\":", String(Size(Q)),
  ",\"phi_Nord\":", String(Phi(Nord)),
  ",\"Q_acts_faithfully_on_CN\":", JB(Size(Centralizer(G, CN)) = Size(K)),
  ",\"elapsed_ms\":", String(GAPLIB_WallElapsedMs()-t0), "}");;
WriteFile(Concatenation("search/certs/.structthm_wit_", wspec.id, ".json"), js);;
Print("\nwrote search/certs/.structthm_wit_", wspec.id, ".json\n");
Print("elapsed = ", (GAPLIB_WallElapsedMs()-t0)/1000.0, " s\nSTRUCTTHM_WIT_DONE\n");
QUIT;
