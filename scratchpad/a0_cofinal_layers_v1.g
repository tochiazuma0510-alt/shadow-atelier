# a0_cofinal_layers_v1.g : small structural check for the note scratchpad/a0_cofinal_lift_theorem_v1.md
# (Fable, 2026-09-03).  Reads only the frozen fuda1 transcription; builds pc3, pc4, Q0, e3 (no joint group).
# Measures: Frattini series of pc3 / pc4 (elementary-abelian layer counts for the remaining T1 rungs),
# index of the <a,c>-image in e3 (lower bound for rank of ker(PB3 -> e3)), |Q4|.
Read("scratchpad/fuda1_a0_rmax_data.g");;
MakePc := function(data)
  local F, coll, n, x, w, k;
  n := data.n; F := FreeGroup(n);
  coll := SingleCollector(F, ListWithIdenticalEntries(n, 3));
  for x in data.conj do
    w := One(F);
    for k in [1..n] do
      if x[3][k] > 0 then w := w * GeneratorsOfGroup(F)[k]^x[3][k]; fi;
    od;
    SetConjugate(coll, x[1], x[2], w);
  od;
  return GroupByRwsNC(coll);
end;;
pc3 := MakePc(FUDA1_PC3);; pc4 := MakePc(FUDA1_PC4);;
FrattiniSeries := function(G)
  local L, H;
  L := [Size(G)]; H := G;
  while Size(H) > 1 do H := FrattiniSubgroup(H); Add(L, Size(H)); od;
  return L;
end;;
LowerCentral := G -> List(LowerCentralSeries(G), Size);;
for pair in [["pc3", pc3], ["pc4", pc4]] do
  Print("LAYERS ", pair[1], " order ", Size(pair[2]), " abinv ", AbelianInvariants(pair[2]),
        " exponent ", Exponent(pair[2]), " class ", NilpotencyClassOfGroup(pair[2]),
        " center ", Size(Center(pair[2])), " frattini_series ", FrattiniSeries(pair[2]),
        " lower_central ", LowerCentral(pair[2]), "\n");
od;
q0perms := List(FUDA1_Q0PERMS, PermList);; q4perms := List(FUDA1_Q4PERMS, PermList);;
q01 := q0perms[1];; q02 := q0perms[2];; q0z := (q02*q01)^-1;;
Q0 := Group([q01, q02]);; Q4 := Group(q4perms);;
Print("LAYERS Q0 order ", Size(Q0), " Q4 order ", Size(Q4), "\n");
iso3 := IsomorphismPermGroup(pc3);; u3 := GeneratorsOfGroup(pc3);; u3p := List(u3, g -> Image(iso3, g));; pc3p := Group(u3p);;
D3 := DirectProduct(Q0, pc3p);; f1 := Embedding(D3,1);; f2 := Embedding(D3,2);;
e3gens := [ Image(f1,q01)*Image(f2,u3p[1]), Image(f1,q0z)*Image(f2,u3p[2]), Image(f1,q02)*Image(f2,u3p[3]) ];;
e3 := Group(e3gens);;
z3 := e3gens[1]*e3gens[2]*e3gens[3];;
AC := Subgroup(e3, [e3gens[1], e3gens[3]]);;
Print("LAYERS e3 order ", Size(e3), " index_of_<a,c>_image ", Index(e3, AC), " z3_in_<a,c> ", z3 in AC,
      " z3_order ", Order(z3), " z3_central ", z3 in Center(e3), "\n");
# pc3 layer inside e3: kernel of e3 -> Q0 is 1 x pc3p; its Frattini series is characteristic, hence stable under any
# automorphism of e3 preserving that kernel (v1 Lemma 3.1 + errata R6 give this for the five occurrence maps).
K3 := Kernel(RestrictedMapping(Projection(D3,1), e3));;
Print("LAYERS ker(e3->Q0) order ", Size(K3), " abinv ", AbelianInvariants(K3), " frattini_series ", FrattiniSeries(K3), "\n");
# rank lower bound for N0 = ker(PB3 -> e3) restricted to the free factor F(a,c):  1 + [F(a,c): N0 cap F(a,c)] = 1 + [<a,c>-image : 1]
Print("LAYERS rank_lower_bound_N0capF(a,c) ", 1 + Size(AC), "\n");
QUIT;
