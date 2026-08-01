# C-beta step 5 (abstract side only): construct the pre-registered marked triple (X,Y,Z)
# for n=7 following docs/notes/u7_meas_design_v1.md Sec 1.2 and
# docs/notes/oddH_full_proof_v1.md Lemma A (a_i, q_j explicit in D_n^3).
# Mechanical GAP construction only. No interpretation.

n := 7;;

# D_n as a permutation group with explicit generators r (rotation, order n), s (reflection, order 2)
D := DihedralGroup(IsPermGroup, 2*n);;
gens := GeneratorsOfGroup(D);;
# DihedralGroup generators: first is rotation of order n, second is reflection of order 2
r := gens[1];;
s := gens[2];;
if Order(r) <> n then Print("ERROR: r order mismatch\n"); fi;
if Order(s) <> 2 then Print("ERROR: s order mismatch\n"); fi;
if s*r*s <> r^-1 then Print("ERROR: srs != r^-1\n"); fi;

D3 := DirectProduct(D, D, D);;
emb1 := Embedding(D3, 1);;
emb2 := Embedding(D3, 2);;
emb3 := Embedding(D3, 3);;

# a_i = (r,1,1) type; q_j = (1,s,s) type per Lemma A
a1 := Image(emb1, r);;
a2 := Image(emb2, r);;
a3 := Image(emb3, r);;
q1 := Image(emb2, s) * Image(emb3, s);;
q2 := Image(emb1, s) * Image(emb3, s);;
q3 := Image(emb1, s) * Image(emb2, s);;

G7 := Group(a1, a2, a3, q1, q2);;
Print("|G7| = ", Size(G7), "  (expect 4*n^3 = ", 4*n^3, ")\n");

# marking (note: X is a reserved/protected identifier in GAP; use markX etc.)
markX := a1*q1;;
markY := a1*a2*a3*q2;;
markZ := (markX*markY)^-1;;
Print("ord(X) = ", Order(markX), "  (expect 2n = ", 2*n, ")\n");
Print("ord(Y) = ", Order(markY), "\n");
Print("ord(Z) = ", Order(markZ), "\n");
Print("ord(X*Y*Z) should be 1 (identity check): ", markX*markY*markZ = One(G7), "\n");

# H = H_{2,1,0} = < a2, a1*a3, q2 >  (H_7^fun)
H := Subgroup(G7, [a2, a1*a3, q2]);;
Print("|H| = ", Size(H), "  (expect 2n^2 = ", 2*n^2, ")\n");
Print("[G7:H] = ", Index(G7,H), "  (expect 2n = ", 2*n, ")\n");

# coset action of G7 on G7/H -> permutation rep of degree 14
act := ActionHomomorphism(G7, RightCosets(G7,H), OnRight);;
Ximg := Image(act, markX);;
Yimg := Image(act, markY);;
Zimg := Image(act, markZ);;

Print("\n--- images in S_14 ---\n");
Print("cycle type X: ", CycleStructurePerm(Ximg), "  ord=", Order(Ximg), "\n");
Print("cycle type Y: ", CycleStructurePerm(Yimg), "  ord=", Order(Yimg), "\n");
Print("cycle type Z: ", CycleStructurePerm(Zimg), "  ord=", Order(Zimg), "\n");

M := Group(Ximg, Yimg, Zimg);;
Print("\n|<X,Y,Z> as perm group on 14 pts| = ", Size(M), "  (expect 4n^2 = ", 4*n^2, ")\n");
Print("transitive on 14 pts: ", IsTransitive(M, [1..14]), "\n");

# explicit permutations for record (as lists of images, 1-indexed)
Print("\n--- explicit permutations (image lists, points 1..14) ---\n");
Print("X = ", List([1..14], i -> i^Ximg), "\n");
Print("Y = ", List([1..14], i -> i^Yimg), "\n");
Print("Z = ", List([1..14], i -> i^Zimg), "\n");

Print("\nDONE\n");
