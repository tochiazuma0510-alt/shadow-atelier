# フェーズ 0 動作確認: GAP が研究に必要な基本操作をこなせるか
# 実行: gap.exe -q --quitonbreak search/smoke-test.g

Print("GAP version: ", GAPInfo.Version, "\n");

# 1. 有限表示群 — B3 (ブレイド群, 生成元 s1,s2; s1 s2 s1 = s2 s1 s2)
F := FreeGroup("s1", "s2");;
B3 := F / [ F.1*F.2*F.1 * (F.2*F.1*F.2)^-1 ];;
Print("B3 defined: ", B3, "\n");

# 2. 剰余群 — B3 の有限商の例: B3 -> S3 (s1,s2 -> 隣接互換)
S3 := SymmetricGroup(3);;
hom := GroupHomomorphismByImages(B3, S3,
         GeneratorsOfGroup(B3), [ (1,2), (2,3) ]);;
Print("B3 ->> S3 surjective: ", Size(Image(hom)) = 6, "\n");

# 3. dihedral 群 — 位数 16 (2 冪) と 位数 6 (最小の奇数関与)
Print("D16 order: ", Size(DihedralGroup(16)), "\n");
Print("D6  order: ", Size(DihedralGroup(6)), "\n");

# 4. 軌道計算の確認
G := DihedralGroup(IsPermGroup, 16);;
orb := Orbit(G, 1);;
Print("D16 orbit of 1: length ", Length(orb), "\n");

Print("SMOKE TEST PASSED\n");
QUIT;
