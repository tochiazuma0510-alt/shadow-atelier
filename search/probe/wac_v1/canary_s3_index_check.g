#############################################################################
## 便 98 F98-4.3 の settled 依存鎖 段2/段3 の載る前提の直接測定:
##   [B_q : P_N] = 6 かつ B_q/P_N =~ S_3 か。
## (Sol の論法は「u 奇 + f pure ⟹ B_q/P_N=S_3 上恒等 ⟹ 像 = B_q」を使う。
##  正典水準では N <= PB_3 から自動だが、この probe 窓で機械的に成り立つかは
##  cert に測定欄が無い。單系統・観測のみ・判定を含まない。)
#############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");

JUDGE_LIBRARY_ONLY := true;;
Read("search/kerchi-judge.g");

n := 24;;
a1 := ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23);;
b1 := ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23);;

aE := a1 * (n+1, n+3);;
bE := b1 * (n+1, n+3, n+2);;
s1 := bE^-1 * aE;;
s2 := aE * bE^2;;
if not (s1*s2*s1 = s2*s1*s2) then Error("braid fails"); fi;

W := MakeWindow(s1, s2);;

Print("=== canary window S3-level check ===\n");
Print("  |Bq|   = ", Size(W.Bq), "\n");
Print("  |PN|   = ", Size(W.PN), "\n");
Print("  index [Bq:PN] = ", Index(W.Bq, W.PN), "\n");
Print("  PN normal in Bq ? ", IsNormal(W.Bq, W.PN), "\n");
Print("  N_ord  = ", W.Nord, "\n");
Print("  c = (s1 s2)^3 trivial in Bq ? ", W.c = Identity(W.Bq), "\n");

if IsNormal(W.Bq, W.PN) and Index(W.Bq, W.PN) = 6 then
  q := NaturalHomomorphismByNormalSubgroup(W.Bq, W.PN);;
  Print("  quotient structure = ", StructureDescription(Image(q)), "\n");
  Print("  ord(q(s1)) = ", Order(Image(q, s1)), "  ord(q(s2)) = ", Order(Image(q, s2)), "\n");
  Print("  q(s1) <> q(s2) ? ", Image(q, s1) <> Image(q, s2), "\n");
  Print("  quotient abelian ? ", IsAbelian(Image(q)), "\n");
fi;

Print("DRIVER_DONE\n");
QUIT;
