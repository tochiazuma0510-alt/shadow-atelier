#############################################################################
## search/probe/wac_v1/expA_batch.g
##   実験 A 工程 4: n=10 の **全 passport × 全 Nielsen 類** で GTSh を測る。
##   (7,3) は CENT-0 が効く(p=s=0)ので核が定理で決まってしまう。ここでは
##   **CENT-0 が効かない** passport ((9,1)/(8,2)/(6,4)/(10)) を含めて総当たりし、
##   予想 PASSPORT と予想 CENT を同時に試す。
##   併せて、各 Nielsen 類が **passport の外にどんな情報を持つか**(= Sol F88-2.6
##   「窓の E-構造に追加情報」)を、a1,b1 の短い語の巡回型署名で実測する。
##
## 入力: なし。**f_orientation: judge**。
## 出力: 標準出力 + search/certs/expA_passport_batch_20260731.json
## 検査する不変量:
##   L1: 同一 passport の全窓で |GTSh| / IdGroup / ker / |Xi(ker)| が一致するか
##   L2: |Xi(ker)| = |C_Sn(w0)| か(予想 CENT; CENT-0 の外でも成り立つか)
##   L3: 語署名が Nielsen 類を分離するか(= GTSh が捨てている情報の実測)
## Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
JUDGE_LIBRARY_ONLY := true;;
JUDGE_SKIP_LEGACY_CROSSCHECK := true;;
Read("search/kerchi-judge.g");
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
BuildS1S2E := function(a1, b1, n)
  local Sn, S3, Dgrp, embA, embS, agen, bgen;
  Sn := SymmetricGroup(n);;  S3 := SymmetricGroup(3);;
  Dgrp := DirectProduct(Sn, S3);;
  embA := Embedding(Dgrp, 1);;  embS := Embedding(Dgrp, 2);;
  agen := Image(embA, a1) * Image(embS, (1,3));;
  bgen := Image(embA, b1) * Image(embS, (1,3,2));;
  return rec(s1 := bgen^-1 * agen, s2 := agen^-1 * bgen^2, Dgrp := Dgrp, embA := embA);
end;;
OrbitsOfWindows := function(n, w0)
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
    Add(orbs, rec(rep := r, size := Length(orb)));
    rem := Difference(rem, orb);
  od;
  return rec(F := F, orbs := orbs, C := C);
end;;

## 語署名: (a1 b1^{e1})(a1 b1^{e2})... の巡回型リスト(共役不変 = 軌道の不変量)
WordSig := function(a1, b1, maxlen)
  local sig, L, seqs, s, g, e, ext, newseqs;
  sig := [];  seqs := [[]];
  for L in [1..maxlen] do
    newseqs := [];
    for s in seqs do
      for e in [1,2] do Add(newseqs, Concatenation(s,[e])); od;
    od;
    seqs := newseqs;
    for s in seqs do
      g := ();
      for e in s do g := g * a1 * b1^e; od;
      Add(sig, CycleStructurePerm(g));
    od;
  od;
  return sig;
end;;

MeasureWindow := function(a1, b1, n, label)
  local blt, W, charming, res, gi, Sdeg, Stab, xis, al, r, kg, m0;
  blt := BuildS1S2E(a1, b1, n);
  W := MakeWindow(blt.s1, blt.s2);
  charming := Filtered([0 .. W.Nord-1], m -> Gcd(2*m+1, W.Nord) = 1);
  res := CorrectedShadows(W, charming);
  gi := GroupOfShadows(W, res.shadows);
  if not gi.closed then return rec(label := label, closed := false); fi;
  m0 := Filtered(res.shadows, s -> s[1] = 0);
  Sdeg := SymmetricGroup(MovedPoints(W.PN));
  Stab := Centralizer(Sdeg, W.x);
  xis := [];
  for r in m0 do
    al := First(Elements(Stab), a -> W.y^a = r[2]*W.y*r[2]^-1);
    Add(xis, al);
  od;
  kg := Group(xis);
  return rec(label := label, closed := true, a1 := a1, b1 := b1,
             order := gi.order, idg := IdGroup(gi.G),
             struct := StructureDescription(gi.G), kersize := Length(m0),
             keridg := IdGroup(gi.ker), kerstruct := StructureDescription(gi.ker),
             xisize := Size(kg), xistruct := StructureDescription(kg),
             stabsize := Size(Stab), nord := W.Nord, charming := Length(charming),
             shadow_total := Length(res.shadows), settled_fail := res.settled_fail_count,
             sgn := SignPerm(a1), amb := StructureDescription(Group(a1,b1)),
             solvable := IsSolvable(gi.G), abelianker := IsAbelian(gi.ker));
end;;

PASSPORTS := [ [10,[9,1]], [10,[8,2]], [10,[7,3]], [10,[6,4]], [10,[10]],
               [10,[7,2,1]], [11,[7,4]] ];;
ALL := [];;
for pp in PASSPORTS do
  n := pp[1];  lam := pp[2];
  w0 := MakePermFromType(lam);
  ob := OrbitsOfWindows(n, w0);
  Print("\n############ n=", n, "  lambda=", lam, "  ord(w0)=", Order(w0),
        "  |C_Sn(w0)|=", Size(ob.C), "  N_gen=", Length(ob.orbs),
        "  |F|=", Length(ob.F), " ############\n");
  Print("  |C_Sn(xbar)| = ", Size(Centralizer(SymmetricGroup(n), w0^2)),
        "   (CENT-0 適用可 = ", Size(Centralizer(SymmetricGroup(n), w0^2)) = Size(ob.C), ")\n");
  rows := [];  sigs := [];
  for i in [1 .. Length(ob.orbs)] do
    if GAPLIB_CheckCap(540.0, "expA_batch") then Print("!! CAP\n"); break; fi;
    r := MeasureWindow(ob.orbs[i].rep[1], ob.orbs[i].rep[2], n,
                       Concatenation("W-P-A", String(n), "-",
                         JoinC(List(lam,String),"x"), "-o", String(i)));
    r.lam := lam;  r.n := n;  r.cw := Size(ob.C);
    Add(rows, r);
    Add(sigs, WordSig(ob.orbs[i].rep[1], ob.orbs[i].rep[2], 4));
    Print("  ", r.label, " : |GTSh|=", r.order, " IdGroup=", r.idg,
          " |ker|=", r.kersize, " ker=", r.kerstruct, " |Xi(ker)|=", r.xisize,
          " N_ord=", r.nord, " charming=", r.charming, " sgn(a1)=", r.sgn,
          " solvable=", r.solvable, "\n");
  od;
  Append(ALL, rows);
  Print("  L1 (同一 passport で全一致) = ",
        PF(Size(Set(List(rows, r -> [r.order,r.idg,r.kersize,r.keridg,r.xisize]))) = 1), "\n");
  Print("  L2 (|Xi(ker)| = |C_Sn(w0)| = ", Size(ob.C), ") = ",
        PF(ForAll(rows, r -> r.xisize = Size(ob.C))), "\n");
  Print("  L3 (語署名が ", Length(sigs), " 軌道を分離) = ",
        PF(Size(Set(sigs)) = Length(sigs)), "   相異なる署名 = ", Size(Set(sigs)), "\n");
od;

Print("\n\n=== 総括表 ===\n");
Print("n | lambda | N_gen | |C(w0)| | 窓 | |GTSh| | IdGroup | |ker| | ker | |Xi| | N_ord\n");
for r in ALL do
  Print(r.n, " | ", r.lam, " | - | ", r.cw, " | ", r.label, " | ", r.order, " | ",
        r.idg, " | ", r.kersize, " | ", r.kerstruct, " | ", r.xisize, " | ", r.nord, "\n");
od;

JRow := function(r)
  return Concatenation("{\"label\":", JStr(r.label), ",\"n\":", String(r.n),
    ",\"lambda\":", JArr(List(r.lam,String)),
    ",\"C_w0\":", String(r.cw),
    ",\"a1\":", JStr(String(r.a1)), ",\"b1\":", JStr(String(r.b1)),
    ",\"gtsh_order\":", String(r.order),
    ",\"gtsh_idgroup\":", JPair(r.idg[1], r.idg[2]),
    ",\"gtsh_struct\":", JStr(r.struct),
    ",\"ker_size\":", String(r.kersize),
    ",\"ker_idgroup\":", JPair(r.keridg[1], r.keridg[2]),
    ",\"ker_struct\":", JStr(r.kerstruct),
    ",\"xi_image_order\":", String(r.xisize),
    ",\"stab_xbar_order\":", String(r.stabsize),
    ",\"N_ord\":", String(r.nord), ",\"charming_count\":", String(r.charming),
    ",\"shadow_total\":", String(r.shadow_total),
    ",\"settled_fail_count\":", String(r.settled_fail),
    ",\"sgn_a1\":", String(r.sgn), ",\"ambient\":", JStr(r.amb),
    ",\"solvable\":", JB(r.solvable), "}");
end;;
WriteFile("search/certs/expA_passport_batch_20260731.json",
  Concatenation("{\n  \"schema\": \"expA-passport-batch/v1\",\n",
    "  \"f_orientation\": \"judge\",\n",
    "  \"generated_by\": {\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/wac_v1/expA_batch.g\",\"date\":\"2026-07-31\"},\n",
    "  \"note\": \"single lane (GAP only). NOT a ledger claim. NOT Lean-verified.\",\n",
    "  \"windows\": ", JArr(List(ALL, JRow)), "\n}\n"));
Print("\nWrote search/certs/expA_passport_batch_20260731.json\n");
Print("\nEXPA_BATCH_DONE\n");
QUIT;
