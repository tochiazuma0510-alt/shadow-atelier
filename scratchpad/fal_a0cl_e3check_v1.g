# fal_a0cl_e3check_v1.g : falsifier's independent small checks for scratchpad/a0_cofinal_lift_theorem_v1.md
# (2026-09-03).  Inputs: frozen fuda1 transcription + a0_paper_words_v1.g (g760, 44 relators) + a0_v2_qraw.g (19 raw Q0 relators).
# Builds e3 = Q0 x pc3 exactly as a0_cofinal_layers_v1.g / a0_v2_prelude.g.  No joint group.
Read("scratchpad/fuda1_a0_rmax_data.g");;
Read("scratchpad/a0_paper_words_v1.g");;
Read("scratchpad/a0_v2_qraw.g");;
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
pc3 := MakePc(FUDA1_PC3);;
q0perms := List(FUDA1_Q0PERMS, PermList);;
q01 := q0perms[1];; q02 := q0perms[2];; q0z := (q02*q01)^-1;;
Q0 := Group([q01, q02]);;
iso3 := IsomorphismPermGroup(pc3);; u3 := GeneratorsOfGroup(pc3);; u3p := List(u3, g -> Image(iso3, g));; pc3p := Group(u3p);;
D3 := DirectProduct(Q0, pc3p);; f1 := Embedding(D3,1);; f2 := Embedding(D3,2);;
e3gens := [ Image(f1,q01)*Image(f2,u3p[1]), Image(f1,q0z)*Image(f2,u3p[2]), Image(f1,q02)*Image(f2,u3p[3]) ];;
e3 := Group(e3gens);;
z3 := e3gens[1]*e3gens[2]*e3gens[3];;
AC := Subgroup(e3, [e3gens[1], e3gens[3]]);;
K3 := Kernel(RestrictedMapping(Projection(D3,1), e3));;   # 1 x pc3
EvalWord := function(word, gens)
  local out, a;
  out := gens[1]^0;
  for a in word do
    if a > 0 then out := out * gens[a]; else out := out * gens[-a]^-1; fi;
  od;
  return out;
end;;
InvWord := w -> List(Reversed(w), a -> -a);;
SubstWord := function(word, images)
  local out, a;
  out := [];
  for a in word do
    if a > 0 then Append(out, images[a]); else Append(out, InvWord(images[-a])); fi;
  od;
  return out;
end;;
zz := [-1,-2];; uu := [-2,-1];;
E3pairs := [ [[1],[2]], [[1],zz], [[2],zz], [uu,[1]], [uu,[2]] ];;
E3names := ["fxy","fxz","fyz","fux","fuy"];;
E3imgE := function(word, pr) return EvalWord(SubstWord(SubstWord(word, pr), [[1],[3]]), e3gens); end;;
g := A0P_G760;;
fxy := E3imgE(g, E3pairs[1]);; fxz := E3imgE(g, E3pairs[2]);; fyz := E3imgE(g, E3pairs[3]);;
fux := E3imgE(g, E3pairs[4]);; fuy := E3imgE(g, E3pairs[5]);;
hex1 := fyz * fxz^-1 * fxy;;          # v2 addendum §2.3: hex_1(g) = f_yz f_xz^-1 f_xy
hex2 := fuy * fxy^-1 * fux^-1;;       # hex_2(g) = f_uy f_xy^-1 f_ux^-1
Print("FAL e3 order ", Size(e3), " AC order ", Size(AC), " index ", Index(e3,AC), "\n");
Print("FAL hex1(g760)=1 in e3: ", IsOne(hex1), "  hex2(g760)=1 in e3: ", IsOne(hex2), "\n");
Print("FAL hex1 order ", Order(hex1), " hex2 order ", Order(hex2), " (coarse Q0 parts trivial: ",
      IsOne(Image(Projection(D3,1), hex1)), " ", IsOne(Image(Projection(D3,1), hex2)), ")\n");
# e3 = AC x <z3> ?  (z3 central of order 3, z3 not in AC, |AC|*3 = |e3|)
Print("FAL z3 central ", z3 in Center(e3), " order ", Order(z3), " z3 in AC ", z3 in AC,
      " AC meet <z3> order ", Size(Intersection(AC, Group(z3))), " => e3 = AC x <z3>: ",
      (Size(AC)*3 = Size(e3)) and (Size(Intersection(AC, Group(z3))) = 1), "\n");
# Frattini of pc3 layer vs the roof image AC
PhiK3 := FrattiniSubgroup(K3);;
Print("FAL |K3|=", Size(K3), " |Phi(K3)|=", Size(PhiK3), " Phi(K3) <= AC: ", IsSubgroup(AC, PhiK3),
      " z3 in Phi(K3): ", z3 in PhiK3, " |AC meet K3|=", Size(Intersection(AC, K3)),
      " AC meet K3 abinv ", AbelianInvariants(Intersection(AC,K3)), " exponent ", Exponent(Intersection(AC,K3)), "\n");
# image of F(x,y) under each of the five E3 substitutions = AC ?
for j in [1..5] do
  H := Group([E3imgE([1], E3pairs[j]), E3imgE([2], E3pairs[j])]);
  Print("FAL occurrence ", E3names[j], " image order ", Size(H), " equals AC: ", H = AC, "\n");
od;
# v460 (1.1): r_x = q1 q6^-2 q7^4 q9, r_y = q8^-1 q4^-1 (raw Q0 relators q_j = A0V2_QRAW[j]); images in e3 under all five occurrences
q := A0V2_QRAW;;
rx := Concatenation(q[1], InvWord(q[6]), InvWord(q[6]), q[7], q[7], q[7], q[7], q[9]);;
ry := Concatenation(InvWord(q[8]), InvWord(q[4]));;
for j in [1..5] do
  a := E3imgE(rx, E3pairs[j]); b := E3imgE(ry, E3pairs[j]);
  Print("FAL v460 r_x/r_y image in e3 via ", E3names[j], ": orders ", Order(a), " ", Order(b),
        " in K3(=1xpc3): ", a in K3, " ", b in K3, "\n");
od;
# Schreier bookkeeping for Prop C: K_{3,0} = K_A x <z^3> with rank K_A = 1 + |AC|
Print("FAL rank K_A = 1 + |AC| = ", 1 + Size(AC), "  => dim H_1(K_{3,0};F_3) = rank K_A + 1 = ", 2 + Size(AC), "\n");
QUIT;
