#############################################################################
## search/_probe_structthm_h2.g -- 構造定理試行(W4・数学者)
##
## 問い: GTSh(D4 窓) ≅ D₈ × (C_N ⋊ Q) は成り立つか。成り立つとして、それは
##       H² の消滅で「必然」か、それとも 1 個の非自明なコホモロジー類が
##       たまたま 0 なのか。
##
## 数学者の還元(docs/notes/structthm_h2_v1.md §2):
##   K = C_N × D₈ (N 奇), gcd(N,|Q|)=1, KE-o ⟺ G = D₈·C_G(D₈) のとき
##     G ≅ D₈ × (C_N ⋊ Q)  ⟺  中心拡大 1 → Z(D₈)=C₂ → C_G(D₈)/C_N → Q → 1 が分裂
##   すなわち ε ∈ H²(Q; C₂)(自明作用)の消滅がすべて。
##   注意: 「K の補群が存在する(分裂)」は ε=0 より真に弱い(反例 D₈⋊C₂ ≅ D₈∘C₄)。
##
## 入力: search/certs/.w62_shadows_<id>.g(w62-scan.g の出力・段 A は再実行しない)
## 出力: search/certs/.structthm_<id>.json + 標準出力
## 1 窓 1 プロセス(環境変数 W62_ONLY)。
#############################################################################
SizeScreen([4096, 0]);;
JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");
Read("search/gaplib_common.g");
Read("search/w62-windows.g");
t0 := GAPLIB_WallElapsedMs();;

wspec := W62_GetWindow();;
Read(Concatenation("search/certs/.w62_shadows_", wspec.id, ".g"));
Print("=== structthm-h2: ", W62_ID, "  shadows = ", Length(W62_SHADOWS), " ===\n");
W := W62_MakeW(wspec);;
if W.Nord <> W62_NORD then Error("N_ord 不一致"); fi;
corr := Set(List(W62_SHADOWS, s -> [s[1], s[2]]));;

gi := GroupOfShadows(W, corr);;
if not gi.closed then Error("(3.53) が閉じない"); fi;
G := gi.G;;  K := gi.ker;;  regs := gi.regs;;
Nord := W.Nord;;
Print("|G| = ", Size(G), "  |K| = ", Size(K), "  |Q| = ", Size(G)/Size(K), "\n");

## ---- 1. K の直積分解 K = C_N x D8 -----------------------------------------
D8 := SylowSubgroup(K, 2);;
oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
CNgens := Concatenation(List(oddp, p -> GeneratorsOfGroup(SylowSubgroup(K, p))));;
CN := Subgroup(K, CNgens);;
D8str := StructureDescription(D8);;
CNstr := StructureDescription(CN);;
Print("\n[1] K の分解:  D8 = Syl_2(K) = ", D8str, " (|.|=", Size(D8), ")",
      "   C_N = O(K) = ", CNstr, " (|.|=", Size(CN), ")\n");
Print("    K nilpotent? ", IsNilpotentGroup(K),
      "   K = C_N x D8? ", Size(CN)*Size(D8) = Size(K) and IsTrivial(Intersection(CN,D8)),
      "   D8 normal in G? ", IsNormal(G, D8),
      "   C_N normal in G? ", IsNormal(G, CN), "\n");
Print("    gcd(N, |Q|) = ", Gcd(Size(CN), Size(G)/Size(K)), "\n");

## ---- 2. KE-o の群論的正体: G = D8 * C_G(D8) --------------------------------
CG := Centralizer(G, D8);;
Z8 := Centre(D8);;
prodOK := (Size(D8)*Size(CG)/Size(Intersection(D8,CG)) = Size(G));;
Print("\n[2] KE-o = 「Q は D8 に内部自己同型としてしか作用しない」:\n");
Print("    |C_G(D8)| = ", Size(CG), "   D8 cap C_G(D8) = Z(D8) (位数 ", Size(Intersection(D8,CG)), ")\n");
Print("    G = D8 . C_G(D8) ? ", prodOK, "   (= 中心積 D8 o C_G(D8))\n");
Print("    Z(D8) <= Z(G)? ", IsSubset(Centre(G), Z8), "   |Z(G)| = ", Size(Centre(G)), "\n");
# G -> Aut(D8) の像 / Inn(D8)
actImg := Size(G)/Size(CG);;
Print("    |G / C_G(D8)| = ", actImg, "  (= |Inn(D8)| = 4 なら作用は完全に内部)\n");

## ---- 3. 決定的判定: D8 は G の直積因子か -----------------------------------
isoPc := IsomorphismPcGroup(G);;
Gp := Image(isoPc);;  Kp := Image(isoPc, K);;  D8p := Image(isoPc, D8);;
CNp := Image(isoPc, CN);;
compsD8 := ComplementClassesRepresentatives(Gp, D8p);;
normComps := Filtered(compsD8, X -> IsNormal(Gp, X));;
directProduct := (Length(normComps) > 0);;
Print("\n[3] D8 の補群クラス数 = ", Length(compsD8),
      "   うち正規なもの = ", Length(normComps),
      "   ==> **G = D8 x X ?  ", directProduct, "**\n");
Xstr := "N/A";;
if directProduct then
  XX := normComps[1];
  Xstr := StructureDescription(XX);
  Print("    X = ", Xstr, " (|X| = ", Size(XX), ")   [D8,X] = 1? ",
        IsTrivial(CommutatorSubgroup(D8p, XX)), "\n");
  Print("    X は C_N ⋊ Q か: |X| = ", Size(XX), " = ", Size(CNp), " * ", Size(Gp)/Size(Kp),
        " ? ", Size(XX) = Size(CNp)*Size(Gp)/Size(Kp), "\n");
fi;

## ---- 4. 中心拡大 1 -> C2 -> C_G(D8)/C_N -> Q -> 1 の類 epsilon --------------
CGp := Image(isoPc, CG);;
hom := NaturalHomomorphismByNormalSubgroup(Gp, CNp);;  # C_N は G で正規
Cbar := Image(hom, CGp);;
Zbar := Image(hom, Image(isoPc, Z8));;
Cbarstr := StructureDescription(Cbar);;
Print("\n[4] 中心拡大 1 -> Z(D8)=C2 -> Cbar -> Q -> 1:\n");
Print("    Cbar = C_G(D8)/C_N = ", Cbarstr, "  (|Cbar| = ", Size(Cbar), " = 2|Q| ? ",
      Size(Cbar) = 2*Size(Gp)/Size(Kp), ")\n");
Print("    Zbar <= Z(Cbar)? ", IsSubset(Centre(Cbar), Zbar), "\n");
epsComps := ComplementClassesRepresentatives(Cbar, Zbar);;
epsSplit := (Length(epsComps) > 0);;
Print("    Z(D8) の補群クラス数 = ", Length(epsComps), "  ==> **epsilon = 0 ?  ", epsSplit, "**\n");
# 同値な具体判定: z notin Phi(Syl_2(Cbar))
S2 := SylowSubgroup(Cbar, 2);;
zb := First(GeneratorsOfGroup(Zbar), g -> not IsOne(g));;
inPhi := zb in FrattiniSubgroup(S2);;
Print("    Syl_2(Cbar) = ", StructureDescription(S2), "   z in Phi(Syl_2(Cbar))? ", inPhi,
      "   (epsilon=0 <=> z notin Phi)\n");

## ---- 5. Syl_2 の形 ---------------------------------------------------------
P2 := SylowSubgroup(Gp, 2);;
Q2ord := 2^PValuation(Size(Gp)/Size(Kp), 2);;
Print("\n[5] Syl_2(G) = ", StructureDescription(P2), "  (|.| = ", Size(P2), " = 8 * ", Q2ord, ")\n");

## ---- 6. 標準切断の候補: f = 1 の shadow たち --------------------------------
oneIdx := Filtered([1 .. Length(corr)], i -> IsOne(corr[i][2]));;
T := Group(regs{oneIdx});;
Tsize := Size(T);;
Tstr := StructureDescription(T);;
TcapK := Size(Intersection(T, K));;
TcentD8 := IsTrivial(CommutatorSubgroup(T, D8));;
Print("\n[6] 標準切断候補 T = { shadow (m, f=1) }:\n");
Print("    #{ (m,1) in S } = ", Length(oneIdx), "   |<T>| = ", Tsize, "  構造 = ", Tstr, "\n");
Print("    T cap K = ", TcapK, "   |T|=|Q|? ", Tsize = Size(G)/Size(K),
      "   [T, D8] = 1? ", TcentD8, "\n");
Print("    m-値: ", List(oneIdx, i -> corr[i][1]), "\n");
Print("    u=2m+1 値: ", List(oneIdx, i -> (2*corr[i][1]+1) mod (2*Nord)), "\n");

## ---- 7. H^2(Q; C2)(自明作用)= epsilon の住む群 ---------------------------
nh := NaturalHomomorphismByNormalSubgroup(G, K);;
Q := Image(nh);;
Qpc := Image(IsomorphismPcGroup(Q));;
Qstr := StructureDescription(Q);;
h2dim := -1;;  z2dim := -1;;  b2dim := -1;;
pcg := Pcgs(Qpc);;
Mtriv := rec(field := GF(2), dimension := 1,
             generators := List([1..Length(pcg)], i -> IdentityMat(1, GF(2))));;
z2 := TwoCocycles(Qpc, Mtriv);;
b2 := TwoCoboundaries(Qpc, Mtriv);;
z2dim := Length(z2);;  b2dim := Length(b2);;
h2dim := z2dim - b2dim;;
Print("\n[7] Q = ", Qstr, " (|Q| = ", Size(Q), ")\n");
Print("    dim Z^2(Q;F2) = ", z2dim, "   dim B^2 = ", b2dim,
      "   **dim H^2(Q; C2) = ", h2dim, "   |H^2| = ", 2^h2dim, "**\n");
Print("    H^2(Q; C_N) = 0 (coprime: gcd(", Size(CN), ",", Size(Q), ") = ",
      Gcd(Size(CN), Size(Q)), ")  ==> H^2(Q; Z(K)) ≅ H^2(Q; C2)\n");

hapH2 := "unavailable";;
if LoadPackage("hap") = true then
  hapH2 := String(GroupCohomology(Qpc, 2, 2));
  Print("    [HAP cross-check] GroupCohomology(Q,2,2) = ", hapH2, "\n");
fi;

## ---- 8. JSON ---------------------------------------------------------------
js := Concatenation(
  "{\"schema\":\"structthm-h2/v1\"",
  ",\"window_id\":", JStr(wspec.id),
  ",\"N_ord\":", String(Nord),
  ",\"G_order\":", String(Size(G)),
  ",\"K_order\":", String(Size(K)),
  ",\"Q_order\":", String(Size(G)/Size(K)),
  ",\"Q_struct\":", JStr(Qstr),
  ",\"D8_struct\":", JStr(D8str),
  ",\"CN_struct\":", JStr(CNstr),
  ",\"D8_normal_in_G\":", JB(IsNormal(G, D8)),
  ",\"CN_normal_in_G\":", JB(IsNormal(G, CN)),
  ",\"CG_D8_order\":", String(Size(CG)),
  ",\"G_eq_D8_times_CG\":", JB(prodOK),
  ",\"ZD8_central_in_G\":", JB(IsSubset(Centre(G), Z8)),
  ",\"D8_complement_classes\":", String(Length(compsD8)),
  ",\"D8_normal_complement_classes\":", String(Length(normComps)),
  ",\"DIRECT_PRODUCT\":", JB(directProduct),
  ",\"X_struct\":", JStr(Xstr),
  ",\"Cbar_struct\":", JStr(Cbarstr),
  ",\"Cbar_order\":", String(Size(Cbar)),
  ",\"epsilon_zero\":", JB(epsSplit),
  ",\"z_in_Frattini_Syl2_Cbar\":", JB(inPhi),
  ",\"Syl2_Cbar_struct\":", JStr(StructureDescription(S2)),
  ",\"Syl2_G_struct\":", JStr(StructureDescription(P2)),
  ",\"f_eq_1_shadow_count\":", String(Length(oneIdx)),
  ",\"T_order\":", String(Tsize),
  ",\"T_struct\":", JStr(Tstr),
  ",\"T_cap_K_order\":", String(TcapK),
  ",\"T_centralizes_D8\":", JB(TcentD8),
  ",\"dim_H2_Q_C2\":", String(h2dim),
  ",\"H2_order\":", String(2^h2dim),
  ",\"hap_H2\":", JStr(hapH2),
  ",\"elapsed_ms\":", String(GAPLIB_WallElapsedMs()-t0), "}");;
WriteFile(Concatenation("search/certs/.structthm_", wspec.id, ".json"), js);;
Print("\nwrote search/certs/.structthm_", wspec.id, ".json\n");
Print("elapsed = ", (GAPLIB_WallElapsedMs()-t0)/1000.0, " s\n");
Print("STRUCTTHM_DONE\n");
QUIT;
