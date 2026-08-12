# search/r13_p1_0_blocks_v1.g -- [P1-0] AllBlocks 事前検査(裁定987・w9_structure_and_ansatz_v1.md §6/§7)
#
# H_9^fun の 18 点上の置換表現(monodromy 群 <X,Y> の像)で AllBlocks を検査。
# 非自明ブロック系があれば lambda_9 が分解する(§6 の表どおり)ため司令塔へ即報告。
#
# 847 依存監査: BuildPn(9)・H9fun 構成は search/r13_r0_v1.g と同一パターン(独立再構成、
#   既存スクリプトを Read() しない)。

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;

PF := function(b) if b then return "PASS"; else return "FAIL"; fi; end;;

# H9fun = H_{2,1,0} = <a2, a1*a3, q2> (same recipe as search/r13_r0_v1.g)
BuildPnFull := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, X, Y, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2)*tr(s,3);;  q2 := tr(s,1)*tr(s,3);;
  X := AbstractProd([a1,q1]);;  Y := AbstractProd([a1,a2,a3,q2]);;
  Gfull := Group(a1,a2,a3,q1,q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, X:=X, Y:=Y, G:=Gfull);;
end;;

P9 := BuildPnFull(9);;
H9fun := Group(P9.a2, P9.a1*P9.a3, P9.q2);;
D := Size(P9.G)/Size(H9fun);;
Print("D = [P9:H9fun] = ", D, " (期待 18)\n");

phiAction9 := FactorCosetAction(P9.G, H9fun);;
Ximg9 := Image(phiAction9, P9.X);;
Yimg9 := Image(phiAction9, P9.Y);;
monG := Group(Ximg9, Yimg9);;
Print("monodromy group <X,Y> acting on ", D, " points, |monG| = ", Size(monG), "\n");

isTransitive := IsTransitive(monG, [1..D]);;
Print("[", PF(isTransitive), "] monG is transitive on ", D, " points\n");

blocks := AllBlocks(monG);;
Print("AllBlocks(monG) = ", blocks, "\n");
nontrivialBlockCount := Length(blocks);;
hasNontrivialBlocks := (nontrivialBlockCount > 0);;
Print("[", PF(not hasNontrivialBlocks), "] no nontrivial block systems (lambda_9 primitive / indecomposable): ",
      not hasNontrivialBlocks, "\n");

blockSizes := List(blocks, b -> Length(b));;
Print("block sizes (if any) = ", blockSizes, "\n");

isPrimitive := IsPrimitive(monG, [1..D]);;
consistCheck := (isPrimitive = (not hasNontrivialBlocks));;
Print("[", PF(consistCheck), "] IsPrimitive consistency check: IsPrimitive=",
      isPrimitive, " vs (not hasNontrivialBlocks)=", not hasNontrivialBlocks, "\n");

# ==== cert ====
ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_p10.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;

scriptSha256 := ComputeSha256File("search/r13_p1_0_blocks_v1.g");;

cert := Concatenation(
  "{\"schema\":\"r13-p1-0-blocks/v1\"",
  ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/r13_p1_0_blocks_v1.g\",\"order\":\"裁定987 / docs/notes/w9_structure_and_ansatz_v1.md §6/§7 [P1-0]\"}",
  ",\"gap_version\":\"", GAPInfo.Version, "\"",
  ",\"D\":", String(D), ",\"mon_group_size\":", String(Size(monG)),
  ",\"is_transitive\":", JB(isTransitive),
  ",\"nontrivial_block_systems_count\":", String(nontrivialBlockCount),
  ",\"has_nontrivial_blocks\":", JB(hasNontrivialBlocks),
  ",\"block_sizes\":", JArr(List(blockSizes,String)),
  ",\"is_primitive\":", JB(isPrimitive),
  ",\"lambda9_indecomposable\":", JB(not hasNontrivialBlocks),
  ",\"u_touched\":false",
  ",\"d_no_interpretation\":\"machine values only; verdict は司令塔\"",
  ",\"provenance\":{\"script_sha256\":\"", scriptSha256, "\"}",
  "}"
);;

outPath := "search/certs/r13_p1_0_blocks_v1_20260812.json";;
WriteFile(outPath, cert);;
Print("\nwrote ", outPath, "\n");
Print("script sha256 = ", scriptSha256, "\n");
QUIT;
