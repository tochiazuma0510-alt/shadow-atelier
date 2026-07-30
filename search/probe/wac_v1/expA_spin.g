#############################################################################
## search/probe/wac_v1/expA_spin.g
##   実験 A 追補: (i) Nielsen 類(C(w0)-軌道)を語署名がどこまで分離するか
##                (ii) H2(予想 SPIN)の第一測定 — 2.A10(Schur 二重被覆)での
##                     持ち上げ不変量が Nielsen 類を割るか
## 方式(ii): 固定した v(型 λ)に対し、二重被覆 2.A_n の類乗法係数
##   #{(h~,g~) : h~ in 上の 3-類, g~ in 上の 2-類, h~ g~ = v~}
##   を **g~ の類ごとに** 分けて数える。2-類の原像が 2 つの類に割れるなら、
##   その割れ方が持ち上げ不変量の分布そのもの。割れなければ不変量は無情報。
## 入力: ctbllib のみ。出力: 標準出力。
## f_orientation: N/A(f を作らない)
## Single lane (GAP 4.16.0). NOT a ledger claim.
#############################################################################
Read("search/gaplib_common.g");
PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;
MakePermFromType := function(lambda)
  local L, pos, part, i;
  L := [];  pos := 0;
  for part in lambda do
    for i in [1..part-1] do L[pos+i] := pos+i+1; od;
    L[pos+part] := pos+1;  pos := pos + part;
  od;
  return PermList(L);
end;;
MakeInvol := function(n, k)
  local L, i;
  L := [1..n];
  for i in [1..k] do L[2*i-1] := 2*i;  L[2*i] := 2*i-1; od;
  return PermList(L);
end;;
OrbReps := function(n, w0)
  local Sn, half, F, k, a1, b1, C, Cel, rem, r, orb, orbs;
  Sn := SymmetricGroup(n);  half := Factorial(n)/2;  F := [];
  for k in [0 .. QuoInt(n,2)] do
    for a1 in Elements(ConjugacyClass(Sn, MakeInvol(n,k))) do
      b1 := a1 * w0^-1;
      if b1^3 <> () then continue; fi;
      if Size(Group(a1,b1)) < half then continue; fi;
      Add(F, [a1,b1]);
    od;
  od;
  C := Centralizer(Sn, w0);  Cel := Elements(C);
  rem := Set(F);  orbs := [];
  while not IsEmpty(rem) do
    r := rem[1];
    orb := Set(List(Cel, z -> [r[1]^z, r[2]^z]));
    Add(orbs, r);  rem := Difference(rem, orb);
  od;
  return orbs;
end;;
WordSig := function(a1, b1, maxlen)
  local sig, L, seqs, s, g, e, newseqs;
  sig := [];  seqs := [[]];
  for L in [1..maxlen] do
    newseqs := [];
    for s in seqs do for e in [1,2] do Add(newseqs, Concatenation(s,[e])); od; od;
    seqs := newseqs;
    for s in seqs do
      g := ();
      for e in s do g := g * a1 * b1^e; od;
      Add(sig, CycleStructurePerm(g));
    od;
  od;
  return sig;
end;;

Print("\n=== (i) 語署名による Nielsen 類の分離(語長を伸ばす)===\n");
for pp in [ [10,[9,1]], [10,[8,2]], [10,[7,3]], [10,[6,4]], [10,[10]] ] do
  n := pp[1];  lam := pp[2];  w0 := MakePermFromType(lam);
  reps := OrbReps(n, w0);
  Print("  n=", n, " lambda=", lam, "  N_gen=", Length(reps), " : ");
  for ml in [3,4,5,6,7] do
    sigs := List(reps, r -> WordSig(r[1], r[2], ml));
    Print("L<=", ml, "->", Size(Set(sigs)), " ");
  od;
  Print("\n");
od;

Print("\n=== (ii) H2 予想 SPIN 第一測定: 2.A10 での持ち上げ不変量 ===\n");
t2 := CharacterTable("2.A10");;
if t2 = fail then
  Print("  ctbllib に 2.A10 なし ==> UNKNOWN\n");
else
  ta := CharacterTable("A10");;
  fus := GetFusionMap(t2, ta);;
  cpA := ClassParameters(CharacterTable("Symmetric",10));;
  ordA := OrdersClassRepresentatives(ta);;
  szA := SizesConjugacyClasses(ta);;
  Print("  |2.A10| = ", Size(t2), "   類数 = ", NrConjugacyClasses(t2),
        "   A10 類数 = ", NrConjugacyClasses(ta), "\n");
  ## A10 のどの類がどの巡回型か: S10 -> A10 の融合で決めるのは面倒なので
  ## 直接 A10 の類代表を作って照合する
  A10 := AlternatingGroup(10);;
  ccA := ConjugacyClasses(A10);;
  TypeOf := function(g) return Collected(CycleStructurePerm(g)); end;;
  FindClasses := function(lambda)
    local w, res, i;
    w := MakePermFromType(lambda);  res := [];
    for i in [1..Length(ccA)] do
      if CycleStructurePerm(Representative(ccA[i])) = CycleStructurePerm(w) then
        Add(res, i);
      fi;
    od;
    return res;
  end;;
  ## GAP の ConjugacyClasses(A10) の順序と CharacterTable("A10") の順序は
  ## 一致するとは限らない ==> 位数と類の大きさで突き合わせる
  Print("  -- 注意: 類の同定は (位数, 類の大きさ) で行う(fail-closed) --\n");
  IdentifyTblClass := function(lambda)
    local w, o, s, cand;
    w := MakePermFromType(lambda);
    o := Order(w);
    s := Factorial(10)/(2*Size(Centralizer(A10, w)));   ## A10 内の類の大きさ
    cand := Filtered([1..NrConjugacyClasses(ta)], i -> ordA[i] = o and szA[i] = s);
    return cand;
  end;;
  for lam in [[2,2,2,2,1,1],[3,3,3,1],[7,3]] do
    Print("  型 ", lam, " : A10 類候補 = ", IdentifyTblClass(lam),
          "  (位数 ", Order(MakePermFromType(lam)), ")\n");
  od;
  ## 2.A10 側の原像
  Print("\n  -- 原像が割れるか --\n");
  for lam in [[2,2,2,2,1,1],[3,3,3,1],[7,3]] do
    for ci in IdentifyTblClass(lam) do
      pre := Filtered([1..NrConjugacyClasses(t2)], i -> fus[i] = ci);
      Print("   A10 類 #", ci, " (型 ", lam, ") の原像 = ", Length(pre),
            " 類  位数 ", OrdersClassRepresentatives(t2){pre}, "\n");
    od;
  od;
  ## 類乗法係数の割れ方
  Print("\n  -- 類乗法係数の割れ方(v = (7,3) 型を固定)--\n");
  vcs := IdentifyTblClass([7,3]);;
  ics := IdentifyTblClass([2,2,2,2,1,1]);;
  hcs := IdentifyTblClass([3,3,3,1]);;
  for vc in vcs do
    for vpre in Filtered([1..NrConjugacyClasses(t2)], i -> fus[i] = vc) do
      tot := 0;
      Print("   v~ 類 #", vpre, " (位数 ", OrdersClassRepresentatives(t2)[vpre], "):\n");
      for ic in ics do
        for ipre in Filtered([1..NrConjugacyClasses(t2)], i -> fus[i] = ic) do
          sub := 0;
          for hc in hcs do
            for hpre in Filtered([1..NrConjugacyClasses(t2)], i -> fus[i] = hc) do
              sub := sub + ClassMultiplicationCoefficient(t2, hpre, ipre, vpre);
            od;
          od;
          Print("      g~ 類 #", ipre, " (位数 ", OrdersClassRepresentatives(t2)[ipre],
                ") : 係数 = ", sub, "\n");
          tot := tot + sub;
        od;
      od;
      Print("      合計 = ", tot, "\n");
    od;
  od;
fi;
Print("\nEXPA_SPIN_DONE\n");
QUIT;
