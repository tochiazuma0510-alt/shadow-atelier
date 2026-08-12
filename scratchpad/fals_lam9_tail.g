deg := 18;;
G := TransitiveGroup(deg, 140);;
bs := AllBlocks(G);;
b3 := First(bs, b -> Length(b) = 3);;
sys3 := Orbit(G, b3, OnSets);;
act6 := Action(G, sys3, OnSets);;
B := First(sys3, b -> 1 in b);;
M := Stabilizer(G, B, OnSets);;
H := Stabilizer(G, 1);;
Print("deck(W/E) = |N_M(H)/H| = ", Size(Normalizer(M,H))/Size(H),
      "   (1 なら非 Galois ✔)\n");
Print("E->P^1: |image| = ", Size(act6),
      "  ブロック長 = ", SSortedList(List(AllBlocks(act6), Length)),
      "  deck = ", Size(Centralizer(SymmetricGroup(6), act6)), "\n");
Print("W->E の monodromy 構造 = ", StructureDescription(Action(M,B,OnPoints)), "\n");
Print("G の構造 = ", StructureDescription(G), "\n");
QUIT;
