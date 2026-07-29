#############################################################################
## search/_probe_structthm_w205.g -- 裁定 205 の分裂 witness 自身が D8 を
## 中心化するか(= 205 の witness だけで直積が出せたか)の直接判定。
#############################################################################
SizeScreen([4096,0]);;
JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");
Read("search/gaplib_common.g");
Read("search/w62-windows.g");
wspec := W62_GetWindow();;
Read(Concatenation("search/certs/.w62_shadows_", wspec.id, ".g"));
W := W62_MakeW(wspec);;
corr := Set(List(W62_SHADOWS, s -> [s[1], s[2]]));;
gi := GroupOfShadows(W, corr);;
G := gi.G;; K := gi.ker;; regs := gi.regs;;
D8 := SylowSubgroup(K, 2);;
Print("=== w205-witness: ", W62_ID, " ===\n");
# W205_WIT は呼び出し側が [ [m, f], ... ] で与える(裁定 205 の証明書から逐語)
for w in W205_WIT do
  p := Position(corr, [w[1], w[2]]);
  if p = fail then Print("  m = ", w[1], " : この f は shadow 集合に無い\n"); continue; fi;
  Print("  m = ", w[1], "  ord_G = ", Order(regs[p]),
        "   D8 を中心化? ", IsTrivial(CommutatorSubgroup(Group(regs[p]), D8)), "\n");
od;
Print("W205_DONE\n");
QUIT;
