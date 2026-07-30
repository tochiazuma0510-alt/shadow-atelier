#############################################################################
## search/_probe_loc_lemmas.g -- LOC 3 段補題(レーン A-2)の各段を層別で数値検証
##
## LOC-1: (m,f) が S = Syl_2(ker chi~) を中心化 <=> T_{(m,f)}|_S = id
##        (T_{(m,f)}: x -> x^u, y -> f^-1 y^u f。S の shadow 座標 (0,sigma) の
##         sigma 全体 Sigma_S 上で T(sigma) = sigma か)
## LOC-2: 中心化 shadow の冪の K-成分は C_K(S) = A x Z(S) に入る(形式的)
## LOC-3: u = -1 層で N_2 = f.T(f) の Z(S)-成分が消えるか。
##        D := T o theta~ とおくと theta~-公理 theta~(f) = f^-1 から
##        N_2 = f . D(f)^-1(D-余境界形)。D|_S の自明性も測る。
##
## 入力(driver が定義): LOC_SPEC := rec(id, n, a1, b1, ambient) ambient in {"A","S"}
## 出力: search/certs/.loc_<id>.json + 標準出力
#############################################################################
SizeScreen([4096, 0]);;
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");
Read("search/gaplib_common.g");
t0 := GAPLIB_WallElapsedMs();;

BuildW := function(spec)
  local Amb, S3, Dg, embA, embS, agen, bgen, s1, s2;
  if spec.ambient = "A" then Amb := AlternatingGroup(spec.n);
                        else Amb := SymmetricGroup(spec.n); fi;
  S3 := SymmetricGroup(3);
  Dg := DirectProduct(Amb, S3);
  embA := Embedding(Dg, 1);  embS := Embedding(Dg, 2);
  agen := Image(embA, spec.a1) * Image(embS, (1,3));
  bgen := Image(embA, spec.b1) * Image(embS, (1,3,2));
  s1 := bgen^-1 * agen;
  s2 := agen^-1 * bgen^2;
  return MakeWindow(s1, s2);
end;;

W := BuildW(LOC_SPEC);;
Nord := W.Nord;;
Read(Concatenation("search/certs/", LOC_SHADOWS));   # W62_SHADOWS を供給
corr := Set(List(W62_SHADOWS, s -> [s[1], s[2]]));;
gi := GroupOfShadows(W, corr);;
if not gi.closed then Error("(3.53) が閉じない"); fi;
G := gi.G;; K := gi.ker;; regs := gi.regs;;
S := SylowSubgroup(K, 2);;
oddp := Filtered(PrimeDivisors(Size(K)), p -> p <> 2);;
A := Subgroup(K, Concatenation(List(oddp, p -> GeneratorsOfGroup(SylowSubgroup(K, p)))));;
Print("=== LOC: ", LOC_SPEC.id, "  N_ord = ", Nord, "  |G| = ", Size(G),
      "  |K| = ", Size(K), "  |S| = ", Size(S), " (", StructureDescription(S), ")",
      "  |A| = ", Size(A), "  |Z(S)| = ", Size(Centre(S)), " ===\n");

## Sigma_S = S の元の shadow 座標(第 2 成分)
Sidx := Filtered([1 .. Length(corr)], i -> regs[i] in S);;
SigS := List(Sidx, i -> corr[i][2]);;
Print("  |Sigma_S| = ", Length(SigS), "  (= |S| ? ", Length(SigS) = Size(S), ")\n");

## theta~ = conj by Delta。S 上で自明か / Sigma_S を保つか
thTriv := ForAll(SigS, s -> TH(W, s) = s);;
thPres := IsSubset(Set(SigS), Set(List(SigS, s -> TH(W, s))));;
Print("\n[theta~] S 上で自明? ", thTriv, "   Sigma_S を保つ? ", thPres, "\n");

## ---- LOC-1: 中心化 <=> T|_S = id ------------------------------------------
nCen := 0;; nTid := 0;; nBoth := 0;; nCenNotT := 0;; nTNotCen := 0;;
witCenNotT := "null";;  witTNotCen := "null";;
for i in [1 .. Length(corr)] do
  m := corr[i][1];  f := corr[i][2];  u := 2*m+1;
  Th := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
          [W.x^u, AbstractProd([f^-1, W.y^u, f])]);
  cen := IsTrivial(CommutatorSubgroup(Group(regs[i]), S));
  tid := ForAll(SigS, s -> Image(Th, s) = s);
  if cen then nCen := nCen + 1; fi;
  if tid then nTid := nTid + 1; fi;
  if cen and tid then nBoth := nBoth + 1; fi;
  if cen and not tid then
    nCenNotT := nCenNotT + 1;
    if witCenNotT = "null" then witCenNotT := Concatenation("{\"m\":", String(m), "}"); fi;
  fi;
  if tid and not cen then
    nTNotCen := nTNotCen + 1;
    if witTNotCen = "null" then witTNotCen := Concatenation("{\"m\":", String(m), "}"); fi;
  fi;
od;
Print("\n[LOC-1] shadow 総数 = ", Length(corr), "\n");
Print("  #中心化 = ", nCen, "   #T|_S=id = ", nTid, "   #両方 = ", nBoth, "\n");
Print("  #中心化かつ T|_S≠id = ", nCenNotT, "   #T|_S=id かつ非中心化 = ", nTNotCen, "\n");
loc1 := (nCenNotT = 0 and nTNotCen = 0);;
Print("  **LOC-1(同値)= ", loc1, "**\n");

## ---- LOC-2/3: u = -1 層 ----------------------------------------------------
mneg := ((-1 - 1)/2) mod Nord;;
negIdx := Filtered([1 .. Length(corr)], i -> corr[i][1] = mneg);;
ZS := Centre(S);;
CKS := Centralizer(K, S);;
Print("\n[LOC-2] C_K(S) の位数 = ", Size(CKS), "  (= |A|*|Z(S)| = ",
      Size(A)*Size(ZS), " ? ", Size(CKS) = Size(A)*Size(ZS), ")\n");
n2ok := 0;; n2bad := 0;; dTriv := 0;; dNonTriv := 0;; inCKS := 0;; notInCKS := 0;;
zComp := 0;;  cenCount := 0;;
if Length(negIdx) > 0 then
  for i in negIdx do
    m := corr[i][1];  f := corr[i][2];  u := 2*m+1;
    Th := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
            [W.x^u, AbstractProd([f^-1, W.y^u, f])]);
    cen := IsTrivial(CommutatorSubgroup(Group(regs[i]), S));
    if not cen then continue; fi;
    cenCount := cenCount + 1;
    # theta~ 公理の確認と D-余境界形の検算
    axiom := (AbstractProd([f, TH(W, f)]) = Identity(W.Bq));
    N2 := AbstractProd([f, Image(Th, f)]);
    Df := Image(Th, TH(W, f));            # D(f) = T(theta~(f))
    if N2 = AbstractProd([f, Df^-1]) then n2ok := n2ok + 1; else n2bad := n2bad + 1; fi;
    # D|_S の自明性
    if ForAll(SigS, s -> Image(Th, TH(W, s)) = s) then dTriv := dTriv + 1;
                                                  else dNonTriv := dNonTriv + 1; fi;
    # h^2 の位置
    h2 := regs[i]^2;
    if h2 in CKS then inCKS := inCKS + 1; else notInCKS := notInCKS + 1; fi;
    if not (h2 in A) then zComp := zComp + 1; fi;
  od;
fi;
Print("\n[LOC-3] u = -1 層(m = ", mneg, ")  中心化 shadow = ", cenCount, "\n");
Print("  N_2 = f.D(f)^-1 の検算: 一致 = ", n2ok, "  不一致 = ", n2bad, "\n");
Print("  D = T o theta~ が S 上自明: ", dTriv, " / 非自明: ", dNonTriv, "\n");
Print("  h^2 in C_K(S): ", inCKS, "  外: ", notInCKS, "\n");
Print("  **h^2 の Z(S)-成分が非自明(= pr_z(N_2) ≠ 1)な個数 = ", zComp, "**\n");

js := Concatenation("{\"schema\":\"loc-lemmas/v1\"",
  ",\"window_id\":", JStr(LOC_SPEC.id),
  ",\"N_ord\":", String(Nord),
  ",\"G_order\":", String(Size(G)),
  ",\"K_order\":", String(Size(K)),
  ",\"S_order\":", String(Size(S)),
  ",\"S_struct\":", JStr(StructureDescription(S)),
  ",\"ZS_order\":", String(Size(ZS)),
  ",\"A_order\":", String(Size(A)),
  ",\"theta_trivial_on_S\":", JB(thTriv),
  ",\"theta_preserves_SigmaS\":", JB(thPres),
  ",\"shadow_total\":", String(Length(corr)),
  ",\"n_centralizing\":", String(nCen),
  ",\"n_T_restricts_to_id\":", String(nTid),
  ",\"n_both\":", String(nBoth),
  ",\"n_cen_not_Tid\":", String(nCenNotT),
  ",\"n_Tid_not_cen\":", String(nTNotCen),
  ",\"LOC1_equivalence\":", JB(loc1),
  ",\"wit_cen_not_Tid\":", witCenNotT,
  ",\"wit_Tid_not_cen\":", witTNotCen,
  ",\"CKS_order\":", String(Size(CKS)),
  ",\"LOC2_CKS_eq_A_times_ZS\":", JB(Size(CKS) = Size(A)*Size(ZS)),
  ",\"uminus1_centralizing\":", String(cenCount),
  ",\"N2_coboundary_form_ok\":", String(n2ok),
  ",\"N2_coboundary_form_bad\":", String(n2bad),
  ",\"D_trivial_on_S\":", String(dTriv),
  ",\"D_nontrivial_on_S\":", String(dNonTriv),
  ",\"h2_in_CKS\":", String(inCKS),
  ",\"h2_with_nontrivial_z\":", String(zComp),
  ",\"elapsed_ms\":", String(GAPLIB_WallElapsedMs()-t0), "}");;
WriteFile(Concatenation("search/certs/.loc_", LOC_SPEC.id, ".json"), js);;
Print("\nwrote search/certs/.loc_", LOC_SPEC.id, ".json\nLOC_DONE\n");
QUIT;
