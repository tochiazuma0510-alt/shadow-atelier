#############################################################################
## search/_probe_loc_diag.g -- LOC-1 破れの正確な診断
## 中心化の真の条件は f.T_h(sigma) = sigma.T_{(0,sigma)}(f)。
## T_{(0,sigma)}: x->x, y->sigma^-1 y sigma は、sigma が x を中心化するとき
## だけ conj_sigma と一致し、そのとき条件は T_h(sigma)=sigma に退化する。
## => Sigma_S が C_{P_N}(x) に入るかを直接測る(LOC-1 の成否の分水嶺)。
#############################################################################
SizeScreen([4096,0]);;
JUDGE_LIBRARY_ONLY := true;; JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g"); Read("search/gaplib_common.g");
Read("search/w62-windows.g");
wspec := W62_GetWindow();;
Read(Concatenation("search/certs/.w62_shadows_", wspec.id, ".g"));
W := W62_MakeW(wspec);;
corr := Set(List(W62_SHADOWS, s -> [s[1], s[2]]));;
gi := GroupOfShadows(W, corr);;
G := gi.G;; K := gi.ker;; regs := gi.regs;;
S := SylowSubgroup(K,2);; ZS := Centre(S);;
Sidx := Filtered([1..Length(corr)], i -> regs[i] in S);;
SigS := List(Sidx, i -> corr[i][2]);;
Zidx := Filtered([1..Length(corr)], i -> regs[i] in ZS);;
SigZ := List(Zidx, i -> corr[i][2]);;
Print("=== loc-diag: ", W62_ID, " ===\n");
cx := Filtered(SigS, s -> s*W.x = W.x*s);;
Print("  |Sigma_S| = ", Length(SigS), "   うち x を中心化 = ", Length(cx),
      "   **Sigma_S <= C_PN(x) ? ", Length(cx) = Length(SigS), "**\n");
cy := Filtered(SigS, s -> s*W.y = W.y*s);;
Print("  参考: y を中心化 = ", Length(cy), "\n");
Print("  theta~ は Z(S) を固定? ", ForAll(SigZ, s -> TH(W,s) = s),
      "   (|Sigma_Z| = ", Length(SigZ), ")\n");
# theta~ が Sigma_S 上に誘導する置換の型
perm := List(SigS, s -> Position(SigS, TH(W,s)));;
Print("  theta~|Sigma_S の置換 = ", PermList(perm), "  (位数 ",
      Order(PermList(perm)), ")\n");
# u=-1 層の中心化 shadow で D|Sigma_S が一定か
Nord := W.Nord;; mneg := ((-1-1)/2) mod Nord;;
negIdx := Filtered([1..Length(corr)], i -> corr[i][1] = mneg
           and IsTrivial(CommutatorSubgroup(Group(regs[i]), S)));;
Dmaps := [];;
for i in negIdx do
  f := corr[i][2];  u := 2*corr[i][1]+1;
  Th := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
          [W.x^u, AbstractProd([f^-1, W.y^u, f])]);
  Add(Dmaps, List(SigS, s -> Position(SigS, Image(Th, TH(W,s)))));
od;
Print("  u=-1 中心化 shadow = ", Length(negIdx),
      "   D|Sigma_S の相異なる型 = ", Length(Set(Dmaps)), "\n");
if Length(Set(Dmaps)) > 0 then
  Print("  D|Sigma_S 代表 = ", PermList(Set(Dmaps)[1]), "\n");
fi;
Print("LOC_DIAG_DONE\n");
QUIT;
