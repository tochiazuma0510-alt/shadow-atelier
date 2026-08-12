# falsifier: 認証済み monodromy 群 (|Mon(lambda_9)|=324, cert w9_k3_p1_0d_check_v1_20260812.json)
# に対して、ノート p1d2_r1_canonicalization_v1.md の 2 つの前提を突く。
#   (i)  §2.2【補題 ORD9】の仮定「K(W)/K(E) は非 Galois (=S_3)」
#   (ii) 【D2-GAP-5】「次数 18 被覆の (3,6) ブロック系の一意性」(ノートは *未解決* と記載)
deg := 18;;
cyc := function(p) return SortedList(List(Cycles(p,[1..deg]), Length)); end;;
tX := [18];; tY := [1,1,2,2,2,2,2,2,2,2];;

G := TransitiveGroup(deg, 140);;
Print("G = T18n140,  |G| = ", Size(G), "\n");

# passport の実現 (x,y) を 1 本取る
els := AsSSortedList(G);;
ys  := Filtered(els, p -> cyc(p) = tY);;
xr  := First(List(ConjugacyClasses(G), Representative), p -> cyc(p) = tX);;
yy  := First(ys, y -> cyc(xr*y) = tX and Size(Group(xr,y)) = Size(G));;
Print("passport realization found: ", yy <> fail, "\n");
Print("  cyc(x)  = ", cyc(xr), "\n");
Print("  cyc(y)  = ", cyc(yy), "\n");
Print("  cyc(xy) = ", cyc(xr*yy), "\n");
Print("  <x,y> = G : ", Size(Group(xr,yy)) = Size(G), "\n\n");

# --- ブロック系の悉皆 ---
bs := AllBlocks(G);;
Print("AllBlocks の長さ分布: ", Collected(List(bs, Length)), "\n");
n3 := Number(bs, b -> Length(b) = 3);;
n9 := Number(bs, b -> Length(b) = 9);;
Print("  サイズ 3 のブロック系の本数 = ", n3, "   (1 なら D2-GAP-5 は閉)\n");
Print("  サイズ 9 のブロック系の本数 = ", n9, "\n\n");

b3 := First(bs, b -> Length(b) = 3);;
sys3 := Orbit(G, b3, OnSets);;
Print("サイズ 3 ブロック系: ブロック数 = ", Length(sys3), "\n");
act6 := Action(G, sys3, OnSets);;
Print("  6 ブロック上の像の位数 = ", Size(act6), "   (cert quotG_order=36 と突合: ",
      Size(act6) = 36, ")\n");
Print("  核 (= W->E の相対部分) の位数 = ", Size(G)/Size(act6), "\n\n");

# --- W -> E の次数 3 被覆が Galois か非 Galois か ---
# E <-> ブロック(6 点), W <-> 点(18 点)。 M = ブロック 1 の setwise stabilizer。
B := First(sys3, b -> 1 in b);;
M := Stabilizer(G, B, OnSets);;
H := Stabilizer(G, 1);;
Print("|M| (ブロック固定群) = ", Size(M), "   |H| (点固定群) = ", Size(H), "\n");
Print("  [M:H] = ", Size(M)/Size(H), "   (=3 なら W->E は次数 3 ✔)\n");
actB := Action(M, B, OnPoints);;
Print("★ W->E の monodromy 群 = M の B 上の像 : 位数 = ", Size(actB),
      "  構造 = ", StructureDescription(actB), "\n");
Print("★ => W->E は ", ["非 Galois (S_3) ✔ ノート §2.2 の仮定と一致",
                        "Galois (C_3) ✘ ノート §2.2 の仮定と矛盾"]
      [ (Size(actB) = 3) + 1 ], "\n");
Print("  deck 群 N_M(H)/H の位数 = ", Size(Normalizer(M,H))/Size(H), "\n\n");

# --- E -> P^1 側の指紋 (t3_spec §1: 位数 36・ブロック系 (3,2)・deck 自明) ---
Print("E->P^1 (6 点) の像の位数 = ", Size(act6), "\n");
Print("  6 点上のブロック長 = ", SSortedList(List(AllBlocks(act6), Length)), "\n");
Print("  deck (中心化群) = ", Size(Centralizer(SymmetricGroup(6), act6)), "\n");
QUIT;
