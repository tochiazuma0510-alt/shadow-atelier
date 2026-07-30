#############################################################################
## search/probe/wac_v1/i10_dl.g
##  I10-2 (DL3-ODD) の導来長算術の検分。
##  A = C5 wr C3 (= O_{2'}(Stab) for xbar=(5,5,5)), Q <= Aut(C5) = C4.
##  X = A : Q。発案係は「X' = A => X'' = A' => dl(X)=3」と書いたが、
##  Q が輪積の top C3 を動かさない(scalar 作用のみ)なら X' = base で dl(X)=2。
##  二つの作用で実測して分ける。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
A := WreathProduct(CyclicGroup(IsPermGroup,5), CyclicGroup(IsPermGroup,3));;
Print("A = C5 wr C3 : |A| = ", Size(A), "  ", StructureDescription(A), "\n");
Print("   |A'| = ", Size(DerivedSubgroup(A)), "  ",
      StructureDescription(DerivedSubgroup(A)),
      "   dl(A) = ", DerivedLength(A), "\n");
Print("   A abelian ? ", IsAbelian(A), "\n");
K := DirectProduct(A, CyclicGroup(IsPermGroup,2));;
Print("ker under CYC-GEN = A x C2 : |K| = ", Size(K),
      "  dl = ", DerivedLength(K), "   <= KERNEL-DL3 fires ? ",
      DerivedLength(K) >= 3, "\n");

## ISO-x-bar side
K2 := CyclicGroup(IsPermGroup,10);;
Print("ker under ISO-xbar = C10 : |K| = ", Size(K2), "  dl = ",
      DerivedLength(K2), "\n");

## GTSh under ISO-xbar = C2 x Hol(C5)
H := Group((1,2,3,4,5),(2,3,5,4));;   ## Hol(C5) = C5 : C4, order 20
Print("Hol(C5): |H| = ", Size(H), " ", StructureDescription(H),
      "  dl = ", DerivedLength(H), "\n");
Print("GTSh under ISO-xbar = C2 x Hol(C5): |.| = ", 2*Size(H),
      "  dl = ", DerivedLength(DirectProduct(H, CyclicGroup(IsPermGroup,2))), "\n");

## Now X = A : Q for the two candidate actions.
## Realize A concretely inside S15 as C5 wr C3 acting on 15 points,
## and take Q-generators inside N_{S15}(<xbar>).
S15 := SymmetricGroup(15);;
xb := (1,2,3,4,5)(6,7,8,9,10)(11,12,13,14,15);;
NN := Normalizer(S15, Group(xb));;
CC := Centralizer(S15, xb);;
Print("\n|N_S15(<xbar>)| = ", Size(NN), "   |C_S15(xbar)| = ", Size(CC),
      "   index (=|Aut(C5)|) = ", Size(NN)/Size(CC), "\n");
Aperm := First(NormalSubgroups(CC), x -> Size(x) = 375);;
Print("A (odd radical of C_S15(xbar)) : |A| = ", Size(Aperm), " ",
      StructureDescription(Aperm), "  dl = ", DerivedLength(Aperm), "\n");

## (a) scalar-only Q: an element of N that powers xbar but fixes each block setwise
qa := First(Elements(NN), g -> xb^g = xb^2 and
        ForAll([[1..5],[6..10],[11..15]], B -> Set(OnTuples(B,g)) = Set(B)));;
Print("\n(a) scalar-only q (blocks preserved) : ", qa, "\n");
Xa := ClosureGroup(Aperm, qa);;
Print("    |X| = ", Size(Xa), "  |X'| = ", Size(DerivedSubgroup(Xa)),
      "  dl(X) = ", DerivedLength(Xa),
      "   X' = A ? ", DerivedSubgroup(Xa) = Aperm, "\n");

## (b) Q that also inverts the wreath top: powers xbar AND swaps two blocks
qb := First(Elements(NN), g -> xb^g = xb^2 and
        Set(OnTuples([1..5],g)) = Set([6..10]));;
if qb = fail then
  Print("\n(b) no q powering xbar and swapping two blocks\n");
else
  Print("\n(b) block-moving q : ", qb, "   ord = ", Order(qb), "\n");
  Xb := ClosureGroup(Aperm, qb);
  Print("    |X| = ", Size(Xb), "  |X'| = ", Size(DerivedSubgroup(Xb)),
        "  dl(X) = ", DerivedLength(Xb),
        "   X' = A ? ", DerivedSubgroup(Xb) = Aperm, "\n");
  Print("    X'' order = ", Size(DerivedSubgroup(DerivedSubgroup(Xb))), "\n");
fi;

## For reference: the full odd-radical normalizer piece
Print("\nN/C = Aut(C5) = C4 ; the whole N_S15(<xbar>) has dl = ",
      DerivedLength(NN), "  |N| = ", Size(NN), "\n");
Print("\nI10_DL_DONE\n");
QUIT;
