# 発案 6 号 I-SET-2 検分: #Hom(B_3,H) = #{(A,B): A^2=B^3} を 3 系統で計算し一致確認
#   (i) 全数列挙                        O(|H|^2)
#  (ii) 類サイズ + べき写像のみ          O(#classes)          <- 数学者の改造案
# (iii) Frobenius 指標和 |H| sum nu2 nu3  O(#classes^2)        <- 発案係の案
# さらに #Hom/|H| の比を測り、#{K : B_3/K =~ H} の規模見積りに使う。
SizeScreen([4096,0]);;

Brute := function(G)
  local e, n, a, b;
  e := Elements(G);; n := 0;;
  for a in e do for b in e do if a^2 = b^3 then n := n+1; fi; od; od;
  return n;
end;;

ClassFormula := function(G)
  local cc, reps, sz, k, idx, A, B, i, j, tot;
  cc := ConjugacyClasses(G);;
  reps := List(cc, Representative);;
  sz := List(cc, Size);;
  k := Length(cc);;
  idx := function(g) return First([1..k], i -> g in cc[i]); end;;
  A := List([1..k], i -> 0);;  B := List([1..k], i -> 0);;
  for j in [1..k] do
    A[ idx(reps[j]^2) ] := A[ idx(reps[j]^2) ] + sz[j];
    B[ idx(reps[j]^3) ] := B[ idx(reps[j]^3) ] + sz[j];
  od;
  tot := 0;;
  for i in [1..k] do tot := tot + A[i]*B[i]/sz[i]; od;
  return tot;
end;;

CharFormula := function(G)
  local t, irr, k, pm2, pm3, cs, nu, nu2, nu3, i, chi, s, tot, ord, conj;
  t := CharacterTable(G);;
  irr := Irr(t);;
  cs := SizesConjugacyClasses(t);;
  ord := Size(G);;
  k := Length(cs);;
  pm2 := PowerMap(t,2);;  pm3 := PowerMap(t,3);;
  nu := function(chi, pm)
    local s, i;
    s := 0;
    for i in [1..k] do s := s + cs[i]*chi[ pm[i] ]; od;
    return s/ord;
  end;;
  conj := List(irr, c -> ComplexConjugate(c));;
  tot := 0;;
  for i in [1..Length(irr)] do
    tot := tot + nu(irr[i],pm2) * nu(conj[i],pm3);
  od;
  return ord*tot;
end;;

Report := function(name, G)
  local o, cf, xf, bf, ratio;
  o := Size(G);;
  cf := ClassFormula(G);;
  xf := CharFormula(G);;
  if o <= 400 then bf := Brute(G); else bf := fail; fi;
  ratio := cf/o;;
  Print(name, "  |H|=", o, "  #classes=", Length(ConjugacyClasses(G)),
        "\n     class-formula = ", cf,
        "   char-formula = ", xf,
        "   brute = ", bf,
        "\n     agree: ", (cf = xf) and (bf = fail or bf = cf),
        "     #Hom/|H| = ", ratio, " = ", Float(ratio), "\n");
end;;

Report("S3        ", SymmetricGroup(3));
Report("S4        ", SymmetricGroup(4));
Report("A5        ", AlternatingGroup(5));
Report("SL(2,3)   ", SL(2,3));
Report("SL(2,5)   ", SL(2,5));
Report("SL(2,7)   ", SL(2,7));
Report("SL(2,11)  ", SL(2,11));
Report("SL(2,13)  ", SL(2,13));
Report("SL(2,17)  ", SL(2,17));
Report("SL(2,19)  ", SL(2,19));
Report("SL(2,23)  ", SL(2,23));
Report("PSL(2,7)  ", PSL(2,7));
Report("PSL(2,11) ", PSL(2,11));
Report("SL(2,9)   ", SL(2,9));
Report("SL(2,25)  ", SL(2,25));

Print("\n=== larger: class formula only (device at scale) ===\n");
for q in [31,37,41,43,47,53,59,61,67,71] do
  G := SL(2,q);;
  cf := ClassFormula(G);;
  Print("SL(2,",q,")  |H|=", Size(G), "  #Hom=", cf, "  ratio=", Float(cf/Size(G)), "\n");
od;
QUIT;
