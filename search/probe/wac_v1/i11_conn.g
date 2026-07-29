#############################################################################
## search/probe/wac_v1/i11_conn.g
##  ideas_011 第一部の検分: census 度数表の成分分解。
##  N^conn(sigma) := #{ (a,b) on supp(sigma) : a^2=1, b^3=1, b^-1 a = sigma,
##                      <a,b> transitive }   (a = b*sigma, i.e. b = a*sigma^-1)
##  sigma を固定し S_n の全対合を悉皆(n <= 13)。生成群のスペクトルも記録。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
WacCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
WacBlock := function(blocks, len)
  local p, i, base;
  p := (); base := 0;
  for i in [1..blocks] do
    p := p * WacCyc(List([1..len], j -> base+j)); base := base + len;
  od;
  return p;
end;;
NC := function(p, n)
  return n - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;
## number of transpositions of an involution / number of 3-cycles of b
NumTr := function(p) return NrMovedPoints(p)/2; end;;
NumTh := function(p) return NrMovedPoints(p)/3; end;;

ConnCount := function(nn, sig, label)
  local Snn, k, a, b, G, tot, spec, key, cls, tid;
  Snn := SymmetricGroup(nn);
  tot := 0; spec := [];
  ## a = () も候補(a^2=1)
  for k in [0..Int(nn/2)] do
    if k = 0 then cls := [()]; else cls := AsList(ConjugacyClass(Snn, WacBlock(k,2))); fi;
    for a in cls do
      b := a * sig^-1;
      if b^3 = () then
        G := Group(a,b);
        if IsTransitive(G, [1..nn]) then
          tot := tot + 1;
          key := [k, NumTh(b), Size(G)];
          Add(spec, key);
        fi;
      fi;
    od;
  od;
  Print("N^conn(", label, ")  n=", nn, "  = ", tot, "\n");
  for key in Set(spec) do
    tid := "";
    Print("      [a_k=", key[1], " b=3^", key[2], " |G|=", key[3], "] x ",
          Number(spec, z -> z = key));
    ## Ree bookkeeping for this component
    Print("    (c(a)=", nn-key[1], " c(b)=", nn-2*key[2], " c(sig)=", NC(sig,nn),
          " sum=", (nn-key[1])+(nn-2*key[2])+NC(sig,nn), " vs n+2=", nn+2, ")\n");
  od;
  if tot = 0 then Print("      -- empty --\n"); fi;
  return tot;
end;;

Print("############ N^conn table ############\n");
N9    := ConnCount( 9, WacCyc([1..9]), "(9)");;
N91   := ConnCount(10, WacCyc([1..9]), "(9,1)");;
N911  := ConnCount(11, WacCyc([1..9]), "(9,1,1)");;
N9111 := ConnCount(12, WacCyc([1..9]), "(9,1^3)");;
N91111:= ConnCount(13, WacCyc([1..9]), "(9,1^4)");;
N92   := ConnCount(11, WacCyc([1..9])*(10,11), "(9,2)");;
N921  := ConnCount(12, WacCyc([1..9])*(10,11), "(9,2,1)");;
N922  := ConnCount(13, WacCyc([1..9])*(10,11)*(12,13), "(9,2,2)");;
N2    := ConnCount( 2, (1,2), "(2)");;
N21   := ConnCount( 3, (1,2), "(2,1)");;
N22   := ConnCount( 4, (1,2)*(3,4), "(2,2)");;
N221  := ConnCount( 5, (1,2)*(3,4), "(2,2,1)");;

Print("\n############ decomposition check ############\n");
## u0 cycles: T1 = {C9, A(2), B(2), D(1)} ; T2 = {C9, F1..F5}
## T1: set partitions of a 4-set -> (lambda, #partitions)
T1 := [
  [ "[14]",      1, N922*0 ],            ## placeholder, replaced below
];;
Print("-- T = (9,2,2,1) : 15 set partitions of {C9,A,B,D} --\n");
pred := rec();;
pred1 := [
 [ "[14]",       1, "N((9,2,2,1))",  0 ],
 [ "[13,1]",     1, "N((9,2,2))*1",  N922 ],
 [ "[12,2]",     2, "N((9,2,1))*N((2))", N921*N2 ],
 [ "[11,3]",     2, "N((9,2))*N((2,1))", N92*N21 ],
 [ "[11,2,1]",   2, "N((9,2))*N((2))*1", N92*N2 ],
 [ "[10,4]",     1, "N((9,1))*N((2,2))", N91*N22 ],
 [ "[10,2,2]",   1, "N((9,1))*N((2))^2", N91*N2*N2 ],
 [ "[9,5]",      1, "N((9))*N((2,2,1))", N9*N221 ],
 [ "[9,4,1]",    1, "N((9))*N((2,2))*1", N9*N22 ],
 [ "[9,3,2]",    2, "N((9))*N((2,1))*N((2))", N9*N21*N2 ],
 [ "[9,2,2,1]",  1, "N((9))*N((2))^2*1", N9*N2*N2 ],
];;
cens1 := rec( c14 := 0, c131 := 72, c122 := 108, c113 := 216, c1121 := 108,
              c104 := 0, c1022 := 54, c95 := 0, c941 := 0, c932 := 144,
              c9221 := 36 );;
obs1 := [0, 72, 108, 216, 108, 0, 54, 0, 0, 144, 36];;
tot1 := 0;;
for i in [1..Length(pred1)] do
  v := pred1[i][2] * pred1[i][4];
  tot1 := tot1 + v;
  Print("  ", pred1[i][1], "  #part=", pred1[i][2], "  ", pred1[i][3],
        "  pred=", v, "  census=", obs1[i], "   MATCH? ", v = obs1[i], "\n");
od;
Print("  TOTAL pred=", tot1, "  census b3count=738\n");

Print("-- T = (9,1^5) : blocks of fixed points of size >=2 give N=0 --\n");
obs2 := [36, 270, 0, 180, 0, 0];;
pred2 := [
 [ "[9,1^5]  j=0", 1,  N9 ],
 [ "[10,1^4] j=1", 5,  N91 ],
 [ "[11,1^3] j=2", 10, N911 ],
 [ "[12,1,1] j=3", 10, N9111 ],
 [ "[13,1]   j=4", 5,  N91111 ],
 [ "[14]     j=5", 1,  0 ],
];;
tot2 := 0;;
for i in [1..Length(pred2)] do
  v := pred2[i][2]*pred2[i][3];
  tot2 := tot2 + v;
  Print("  ", pred2[i][1], "  C(5,j)=", pred2[i][2], "  N=", pred2[i][3],
        "  pred=", v, "  census=", obs2[i], "\n");
od;
Print("  TOTAL pred=", tot2, "  census b3count=486\n");

Print("\n############ N((9,1)) two-universe consistency ############\n");
Print("  from T1 [10,2,2] : 54 / (N((2))^2 = ", N2*N2, ") = ", 54/(N2*N2), "\n");
Print("  from T2 [10,1^4] : 270 / C(5,1)=5 = ", 270/5, "\n");
Print("  direct enumeration N^conn((9,1)) = ", N91, "\n");

Print("\nI11_CONN_DONE\n");
QUIT;
