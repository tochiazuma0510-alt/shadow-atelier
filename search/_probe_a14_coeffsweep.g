# _probe_a14_coeffsweep.g — A14 (D4) ダイヤル悉皆前哨: クラス対 × 目標 u 型の存在係数表
# 目的: a1(偶対合)クラス × b1(位数3)クラス × u=b1^-1*a1 目標型 T の全組で
#       クラス積係数 c(C_B, C_A -> C_T) と確率 P = c*|C_T|/(|C_B|*|C_A|) を厳密計算。
#       c=0 の組は探索不要(存在しない)。c>0 のみが MC 前哨(diag5 手法)の対象。
# 注: S14 指標表で計算(該当型は全て非分裂 — 反復部分を含むため S14 類 = A14 類が集合として一致)。
# u 目標: u^2 = xbar = (9,1^5) の A14 内平方根は型 (9,2,2,1) と (9,1^5) の 2 種のみ(偶性で他は排除)。
LoadPackage("ctbllib");;
tbl := CharacterTable("S14");;
pars := List(ClassParameters(tbl), p -> p[2]);;
sizes := SizesConjugacyClasses(tbl);;
findc := function(p) return Position(pars, p); end;;

Acands := [ [2,2,2,2,2,2,1,1], [2,2,2,2,1,1,1,1,1,1], [2,2,1,1,1,1,1,1,1,1,1,1] ];;
Bcands := [ [3,3,3,3,1,1], [3,3,3,1,1,1,1,1], [3,3,1,1,1,1,1,1,1,1], [3,1,1,1,1,1,1,1,1,1,1,1] ];;
Tcands := [ [9,2,2,1], [9,1,1,1,1,1] ];;

Print("# a1_type | b1_type | u_type | coeff c | P(u in T)\n");
for pa in Acands do
  for pb in Bcands do
    for pt in Tcands do
      ia := findc(pa);; ib := findc(pb);; it := findc(pt);;
      if ia = fail or ib = fail or it = fail then
        Print(pa, " | ", pb, " | ", pt, " | CLASS_NOT_FOUND\n");
      else
        # b1^-1*a1 in C_T  <=>  exists x in C_B, y in C_A with x*y in C_T
        # (b1^-1 は b1 と同類: S_n の類は有理的)
        c := ClassMultiplicationCoefficient(tbl, ib, ia, it);;
        p := c * sizes[it] / (sizes[ib] * sizes[ia]);;
        Print(pa, " | ", pb, " | ", pt, " | ", c, " | ", Float(p), "\n");
      fi;
    od;
  od;
od;
QUIT_GAP(0);
