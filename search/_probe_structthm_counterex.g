#############################################################################
## search/_probe_structthm_counterex.g -- 構造定理試行 付録(W4・数学者)
## 「分裂 + Q の作用が内部(KE-o)」から「直積」は出ない、の最小反例を機械で確認。
## D8 ⋊ C2(作用 = D8 の内部自己同型 conj_r)は分裂拡大だが D8 × C2 ではなく
## 中心積 D8 ∘ C4 になる。これが裁定 205 の推論に開いていた穴。
#############################################################################
SizeScreen([4096,0]);;
D8 := DihedralGroup(IsPermGroup, 8);;
r := First(Elements(D8), g -> Order(g) = 4);;
inn := ConjugatorAutomorphism(D8, r);;          # 位数 2 の内部自己同型
C2 := CyclicGroup(IsPermGroup, 2);;
act := GroupHomomorphismByImages(C2, Group(inn), GeneratorsOfGroup(C2), [inn]);;
Gx := SemidirectProduct(C2, act, D8);;
emb := Embedding(Gx, 2);;
D8e := Image(emb);;
Print("|E| = ", Size(Gx), "   E = ", StructureDescription(Gx), "\n");
Print("D8 ⊴ E ? ", IsNormal(Gx, D8e), "\n");
Print("作用は内部か(E = D8·C_E(D8))? ",
      Size(D8e)*Size(Centralizer(Gx, D8e))/Size(Intersection(D8e, Centralizer(Gx, D8e))) = Size(Gx), "\n");
Print("E は D8 上分裂(補群あり)? ", Length(ComplementClassesRepresentatives(Gx, D8e)) > 0, "\n");
Print("補群のうち正規(= 直積)なもの: ",
      Length(Filtered(ComplementClassesRepresentatives(Gx, D8e), sub -> IsNormal(Gx, sub))), "\n");
Print("E ≅ D8 × C2 ? ", IsomorphismGroups(Gx, DirectProduct(DihedralGroup(8), CyclicGroup(2))) <> fail, "\n");
Print("C_E(D8) = ", StructureDescription(Centralizer(Gx, D8e)),
      "   (C4 なら中心拡大 1→C2→C4→C2→1 が非分裂 = epsilon ≠ 0)\n");
Print("COUNTEREX_DONE\n");
QUIT;
