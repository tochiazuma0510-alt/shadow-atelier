#############################################################################
## search/probe/wac_v1/expA_verify.g
##   実験 A 工程 1b: 小さい n での **直接悉皆**による T_all / T_trans / T_gen /
##   N_gen(= C_Sn(w0)-軌道数)の独立再計算 + 軌道代表(= witness)の抽出。
##
## 入力: なし(下の TARGETS を編集)。触れてよいデータ範囲: S_n の元のみ。
## 方式: a1 を「S_n の全対合」で悉皆(共役類ごとに Elements)、b1 := a1*w0^-1、
##       b1^3 = 1 を課す。<a1,b1> の位数で推移/生成を判定。
##       C_Sn(w0) の同時共役作用で軌道分解。
## 目的: 指標理論(expA_scan.g)の値と **二系統照合**し、
##       かつ n<=10 の UNDETERMINED を厳密に決着させる。
##
## 検査する不変量:
##   J1: 直接悉皆の T_all が指標和(expA_scan.g)の T_all と一致
##   J2: 生成対の軌道はすべて長さ |C_Sn(w0)|(SAT-RIG の自由作用)
##   J3: 既測窓((9,1) と (10) at n=10)で N_gen = 1 が再現される(対照)
##
## f_orientation: N/A(この probe は f を構成しない)
## Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Read("search/gaplib_common.g");
PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

MakePermFromType := function(lambda)
  local L, pos, part, i;
  L := [];  pos := 0;
  for part in lambda do
    for i in [1..part-1] do L[pos+i] := pos+i+1; od;
    L[pos+part] := pos+1;
    pos := pos + part;
  od;
  return PermList(L);
end;;

MakeInvol := function(n, k)
  local L, i;
  L := [1..n];
  for i in [1..k] do L[2*i-1] := 2*i;  L[2*i] := 2*i-1; od;
  return PermList(L);
end;;

## 期待値(expA_scan.g の指標和による値)-- J1 照合用
EXPECT := rec();;
EXPECT.("8_8")     := [24, 24];;
EXPECT.("9_8_1")   := [40, 16];;
EXPECT.("9_9")     := [36, 36];;
EXPECT.("10_9_1")  := [90, 54];;
EXPECT.("10_8_2")  := [72, 48];;
EXPECT.("10_6_4")  := [96, 72];;
EXPECT.("10_7_3")  := [77, 63];;
EXPECT.("10_10")   := [65, 65];;
EXPECT.("10_7_2_1"):= [77, 14];;
EXPECT.("11_7_4")  := [140, 84];;

VerifyOne := function(n, lambda)
  local S, w0, half, Fall, Ftr, Fgen, k, cl, a1, b1, G, sz, C, Cel, rem, orb,
        orbs, key, exp, orbsizes, r, p, nOrbits, seen, e;
  S := SymmetricGroup(n);
  w0 := MakePermFromType(lambda);
  half := Factorial(n)/2;
  Fall := [];  Ftr := [];  Fgen := [];
  for k in [0 .. QuoInt(n,2)] do
    cl := Elements(ConjugacyClass(S, MakeInvol(n,k)));
    for a1 in cl do
      b1 := a1 * w0^-1;
      if b1^3 <> () then continue; fi;
      Add(Fall, [a1, b1]);
      G := Group(a1, b1);
      sz := Size(G);
      if IsTransitive(G, [1..n]) then Add(Ftr, [a1,b1]); fi;
      if sz >= half then Add(Fgen, [a1,b1]); fi;
    od;
  od;
  C := Centralizer(S, w0);
  Cel := Elements(C);
  ## 生成対の C(w0)-軌道分解
  rem := Set(Fgen);  orbs := [];
  while not IsEmpty(rem) do
    r := rem[1];
    orb := Set(List(Cel, z -> [r[1]^z, r[2]^z]));
    Add(orbs, rec(rep := r, size := Length(orb)));
    rem := Difference(rem, orb);
  od;
  key := Concatenation(String(n), "_", JoinC(List(lambda, String), "_"));
  Print("\n### n=", n, "  lambda=", lambda, "  w0=", w0, "\n");
  Print("    |C_Sn(w0)| = ", Size(C), "\n");
  Print("    T_all(直接) = ", Length(Fall),
        "   T_trans(直接) = ", Length(Ftr),
        "   T_gen(直接) = ", Length(Fgen), "\n");
  if IsBound(EXPECT.(key)) then
    exp := EXPECT.(key);
    Print("    J1 指標和との照合: T_all ", Length(Fall), " vs ", exp[1],
          "  ==> ", PF(Length(Fall) = exp[1]),
          " ;  T_trans ", Length(Ftr), " vs ", exp[2],
          "  ==> ", PF(Length(Ftr) = exp[2]), "\n");
  else
    Print("    (期待値未登録)\n");
  fi;
  orbsizes := Set(List(orbs, o -> o.size));
  Print("    N_gen(= C(w0)-軌道数) = ", Length(orbs),
        "   軌道長の集合 = ", orbsizes,
        "   J2(全長 = |C|) = ", PF(orbsizes = [Size(C)] or IsEmpty(orbs)), "\n");
  for e in [1 .. Length(orbs)] do
    Print("      orbit ", e, ":  a1 = ", orbs[e].rep[1], "\n",
          "                 b1 = ", orbs[e].rep[2],
          "   <a1,b1> = ", StructureDescription(Group(orbs[e].rep[1], orbs[e].rep[2])),
          "  CycleStructure(a1)=", CycleStructurePerm(orbs[e].rep[1]),
          " (b1)=", CycleStructurePerm(orbs[e].rep[2]), "\n");
  od;
  return rec(n := n, lambda := lambda, tall := Length(Fall), ttr := Length(Ftr),
             tgen := Length(Fgen), ngen := Length(orbs), csize := Size(C),
             orbs := orbs);
end;;

TARGETS := [ [8,[8]], [9,[8,1]], [9,[9]],
             [10,[9,1]], [10,[8,2]], [10,[7,3]], [10,[6,4]], [10,[10]],
             [10,[7,2,1]] ];;

RES := [];;
for tg in TARGETS do
  Add(RES, VerifyOne(tg[1], tg[2]));
od;

Print("\n\n=== まとめ(n<=10 の全 UNDETERMINED + 対照)===\n");
Print("n | lambda | |C| | T_all | T_trans | T_gen | N_gen\n");
for r in RES do
  Print(r.n, " | ", r.lambda, " | ", r.csize, " | ", r.tall, " | ", r.ttr,
        " | ", r.tgen, " | ", r.ngen, "\n");
od;
Print("\nEXPA_VERIFY_DONE\n");
QUIT;
