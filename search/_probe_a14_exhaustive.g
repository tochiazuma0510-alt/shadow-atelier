# _probe_a14_exhaustive.g — A14 実現の悉皆判定(WLOG u0 固定・全偶対合 a 走査)
# 原理: 窓 (a,b) は対共役で u := b^-1*a(GAP 積順・driver 規約)を型代表 u0 に正規化できる。
#   u = u0 と固定すれば b = a*u0^-1 が a から決まるので、a を A14 の偶対合 3 類
#   (2^6 1^2: 945,945 / 2^4 1^6: 315,315 / 2^2 1^10: 3,003)で全走査すれば
#   「b^3 = 1 かつ <a,b> = A14」の実現存在が厳密に決まる(u^2 = xbar = (9,1^5) の
#   偶な平方根は型 (9,2,2,1) と (9,1^5) の 2 種のみ)。
# 較正: b 型ごとの度数の期待値 E = c(B,T;A)*|C_A|/|C_T|(S14 指標表・非分裂類)と実測を突合。
#   期待と実測が合わなければ積順規約の取り違え(この probe 自身のバグ)を疑うこと。
LoadPackage("ctbllib");;
n := 14;;
G := AlternatingGroup(n);;
sizeG := Size(G);;
one := ();;

matchPatterns := function(m)
  local rec_;
  rec_ := function(pts)
    local res, q, rest, sub;
    if Length(pts) = 0 then return [ [] ]; fi;
    res := [];
    for q in pts{[2..Length(pts)]} do
      rest := Filtered(pts, x -> x <> pts[1] and x <> q);
      for sub in rec_(rest) do
        Add(res, Concatenation([[pts[1], q]], sub));
      od;
    od;
    return res;
  end;
  return rec_([1..m]);
end;;

sweep := function(u0, label)
  local u0inv, res, k, m, fixSets, pat, fs, supp, mp, imgs, pr, a, b, grp;
  u0inv := u0^-1;;
  res := rec(label := label, hits := [], btypes := [], survivors := [], checked := 0, b3count := 0);;
  for k in [6, 4, 2] do
    m := 2*k;;
    fixSets := Combinations([1..n], n - m);;
    pat := matchPatterns(m);;
    Print("  class 2^", k, "1^", n-m, ": ", Length(fixSets), " x ", Length(pat), "\n");
    for fs in fixSets do
      supp := Filtered([1..n], x -> not x in fs);;
      for mp in pat do
        imgs := [1..n];
        for pr in mp do
          imgs[supp[pr[1]]] := supp[pr[2]];
          imgs[supp[pr[2]]] := supp[pr[1]];
        od;
        a := PermList(imgs);
        res.checked := res.checked + 1;
        b := a * u0inv;
        if b <> one and b^3 = one then
          res.b3count := res.b3count + 1;
          Add(res.btypes, [k, CycleStructurePerm(b)]);
          grp := Group(a, b);
          # survivor 全数記帳: [a型k, b型, 推移的か, |<a,b>|] — 真部分群窓の可能性の census
          Add(res.survivors, [k, CycleStructurePerm(b), IsTransitive(grp, [1..n]), Size(grp)]);
          if Size(grp) = 3113510400 then  # = |A13|: 1 点固定 A13 実現対(W-E-A13-9t4 の実物)
            Print("  A13PAIR a=", a, " b=", b, " fix=", Filtered([1..n], x -> x^a = x and x^b = x), "\n");
          fi;
          if IsTransitive(grp, [1..n]) and Size(grp) = sizeG then
            Add(res.hits, rec(a := a, b := b));
            Print("  *** HIT [", label, "]: a=", a, "  b=", b, "\n");
          elif IsTransitive(grp, [1..n]) then
            Print("  ~~~ transitive proper subgroup [", label, "]: |H|=", Size(grp),
                  " a=", a, " b=", b, "\n");
          fi;
        fi;
      od;
    od;
  od;
  Print("  [", label, "] checked=", res.checked, " b3(order3)=", res.b3count,
        " HITS=", Length(res.hits), "\n");
  Print("  b-type counts (k, cycstruct): ", Collected(res.btypes), "\n");
  return res;
end;;

# 期待値較正表(b 型 x a 類 x u 型): E = c(B,T;A)*|C_A|/|C_T|
tbl := CharacterTable("S14");;
pars := List(ClassParameters(tbl), p -> p[2]);;
sizes := SizesConjugacyClasses(tbl);;
findc := p -> Position(pars, p);;
expectedCount := function(pB, pT, pA)
  local iB, iT, iA;
  iB := findc(pB);; iT := findc(pT);; iA := findc(pA);;
  return ClassMultiplicationCoefficient(tbl, iB, iT, iA) * sizes[iA] / sizes[iT];
end;;
Print("較正期待値 E(b in B | a 全走査, u0 固定):\n");
for pA in [ [2,2,2,2,2,2,1,1], [2,2,2,2,1,1,1,1,1,1], [2,2,1,1,1,1,1,1,1,1,1,1] ] do
  for pB in [ [3,3,3,3,1,1], [3,3,3,1,1,1,1,1], [3,3,1,1,1,1,1,1,1,1], [3,1,1,1,1,1,1,1,1,1,1,1] ] do
    for pT in [ [9,2,2,1], [9,1,1,1,1,1] ] do
      Print("  A=", pA, " B=", pB, " T=", pT, " : E=", expectedCount(pB, pT, pA), "\n");
    od;
  od;
od;

u0a := PermList(Concatenation([2,3,4,5,6,7,8,9,1], [11,10], [13,12], [14]));;
u0b := PermList(Concatenation([2,3,4,5,6,7,8,9,1], [10,11,12,13,14]));;
Print("u0a cycstruct: ", CycleStructurePerm(u0a), "\n");
Print("u0b cycstruct: ", CycleStructurePerm(u0b), "\n");

r1 := sweep(u0a, "T=(9,2,2,1)");;
r2 := sweep(u0b, "T=(9,1^5)");;

out := "search/_probe_a14_exhaustive_result.txt";;
PrintTo(out, "A14 exhaustive realization sweep (WLOG u0 fixed)\n",
  "T=(9,2,2,1): checked=", r1.checked, " b3=", r1.b3count, " hits=", Length(r1.hits), "\n",
  "  btypes=", Collected(r1.btypes), "\n",
  "  survivor census [k, btype, transitive, size] = ", Collected(r1.survivors), "\n",
  "  hits=", r1.hits, "\n",
  "T=(9,1^5): checked=", r2.checked, " b3=", r2.b3count, " hits=", Length(r2.hits), "\n",
  "  btypes=", Collected(r2.btypes), "\n",
  "  survivor census [k, btype, transitive, size] = ", Collected(r2.survivors), "\n",
  "  hits=", r2.hits, "\n");
Print("survivor census T-a: ", Collected(List(r1.survivors, s -> [s[3], s[4]])), "\n");
Print("survivor census T-b: ", Collected(List(r2.survivors, s -> [s[3], s[4]])), "\n");
Print("結果を ", out, " に保存\n");
QUIT_GAP(0);
