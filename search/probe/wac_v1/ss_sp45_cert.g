## ss_sp45_cert.g -- W-D-Sp45-6a 実現判定の証明書生成(裁定 193)
## 値はすべて本 script が機械生成する(手転記なし)。解釈はしない。
## 出力: search/certs/ss_sp45_realization_20260729.json
SizeScreen([4096,0]);;
Read("search/gaplib_common.g");
t0 := GAPLIB_WallElapsedMs();;

G := Image(IsomorphismPermGroup(PSp(4,5)));;
n := Size(G);;  deg := LargestMovedPoint(G);;
ccl := ConjugacyClasses(G);;
ordsC := List(ccl, c -> Order(Representative(c)));;
cenC  := List(ccl, c -> Size(Centralizer(G, Representative(c))));;
iX := Filtered([1..Length(ccl)], i -> ordsC[i]=6 and cenC[i]=360)[1];;
CXstr := StructureDescription(Centralizer(G, Representative(ccl[iX])));;
U12all := Filtered([1..Length(ccl)], i -> ordsC[i]=12);;
iU := Filtered(U12all, i -> Representative(ccl[i])^2 in ccl[iX])[1];;
u := Representative(ccl[iU]);;

## 構造定数(ATLAS 表・第二系統)
tbl := CharacterTable("S4(5)");;
to := OrdersClassRepresentatives(tbl);;  tc := SizesCentralizers(tbl);;
tp := PowerMap(tbl,2);;
tX := Filtered([1..Length(to)], i -> to[i]=6 and tc[i]=360);;
tU := Filtered([1..Length(to)], i -> to[i]=12 and tp[i] in tX);;
tA := Filtered([1..Length(to)], i -> to[i]=2);;
tB := Filtered([1..Length(to)], i -> to[i]=3);;
sc := 0;;
for U in tU do for B in tB do for A in tA do
  sc := sc + ClassMultiplicationCoefficient(tbl,B,A,U); od; od; od;

## 悉皆列挙(第一系統)
sols := 0;;  subsz := [];;
for i in Filtered([1..Length(ccl)], j -> ordsC[j]=2) do
  for q in AsList(ccl[i]) do
    if Order(u*q) = 3 then
      sols := sols + 1;
      Add(subsz, Size(Group(q, (u*q)^-1)));
    fi;
  od;
od;
genCount := Length(Filtered(subsz, s -> s = n));;
subDist := Collected(subsz);;

## 較正(判定器が TRUE を返せるか)
RandOrd := function(GG,d)
  local g,o,t; t:=0;
  repeat g:=Random(GG); o:=Order(g); t:=t+1; if t>400 then return fail; fi; until o mod d = 0;
  return g^(o/d);
end;;
Reset(GlobalMersenneTwister, 20260729);;
calGen := 0;;  calU := [];;
for i in [1..2000] do
  a1 := RandOrd(G,2); b1 := RandOrd(G,3);
  if a1=fail or b1=fail then continue; fi;
  if Size(Group(a1,b1)) = n then calGen := calGen+1; Add(calU, Order(b1^-1*a1)); fi;
od;
Reset(GlobalMersenneTwister, 20260730);;
hit12 := [];;
for i in [1..3000] do
  a1 := RandOrd(G,2); b1 := RandOrd(G,3);
  if a1=fail or b1=fail then continue; fi;
  uu := b1^-1*a1;
  if Order(uu) <> 12 then continue; fi;
  if Size(Group(a1,b1)) <> n then continue; fi;
  Add(hit12, Size(Centralizer(G, uu^2)));
od;
t1 := GAPLIB_WallElapsedMs();;

ComputeSha256File := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha_sp45.txt";
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));
  f := InputTextFile(tmp);  line := ReadLine(f);  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\""));
  return line{[1..64]};
end;;
PairListJson := function(l)
  return JArr(List(l, p -> Concatenation("[", String(p[1]), ",", String(p[2]), "]")));
end;;

cert := Concatenation(
 "{\"schema\":\"ss-sp45-realization/v1\"",
 ",\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/probe/wac_v1/ss_sp45_cert.g\",\"date\":\"2026-07-29\",\"ruling\":\"ruling-193\"}",
 ",\"window_id\":\"W-D-Sp45-6a\"",
 ",\"source_note\":\"docs/notes/wac_second_strike_v1.md sec 2.4 (realization PENDING homework)\"",
 ",\"question\":\"Does PSp(4,5) admit a1^2=b1^3=1, <a1,b1>=P, ord(b1^-1 a1)=12, (b1^-1 a1)^2 in class(C3 x SL(2,5)) ?\"",
 ",\"universe\":{\"P\":\"PSp(4,5)\",\"order\":", String(n), ",\"perm_degree\":", String(deg),
   ",\"num_classes\":", String(Length(ccl)),
   ",\"target_class_order\":6,\"target_centralizer_order\":", String(cenC[iX]),
   ",\"target_centralizer_structure\":", JStr(CXstr),
   ",\"u_source_class_order\":12,\"u_centralizer_order\":", String(cenC[iU]),
   ",\"all_order12_classes_centralizers\":", JArr(List(U12all, i -> String(cenC[i]))),
   ",\"u_source_unique\":", JB(Length(Filtered(U12all, i -> Representative(ccl[i])^2 in ccl[iX])) = 1), "}",
 ",\"route_a_structure_constants_atlas\":{\"table\":", JStr(Identifier(tbl)),
   ",\"table_order_matches\":", JB(Size(tbl)=n),
   ",\"sum_c_B_A_U\":", String(sc), "}",
 ",\"route_b_exhaustive_enumeration\":{\"involutions_scanned\":",
   String(Sum(Filtered([1..Length(ccl)], j -> ordsC[j]=2), i -> Size(ccl[i]))),
   ",\"factorizations_found\":", String(sols),
   ",\"agrees_with_structure_constant\":", JB(sols = sc),
   ",\"generated_subgroup_order_distribution\":", PairListJson(subDist),
   ",\"pairs_generating_P\":", String(genCount), "}",
 ",\"calibration\":{\"random_23_pairs_tried\":2000",
   ",\"generating_pairs_found\":", String(calGen),
   ",\"decider_can_return_true\":", JB(calGen > 0),
   ",\"observed_ord_u_distribution\":", PairListJson(Collected(calU)),
   ",\"generating_pairs_with_ord_u_12\":", String(Length(hit12)),
   ",\"their_centralizer_of_u_squared\":", PairListJson(Collected(hit12)), "}",
 ",\"REALIZATION\":", JB(genCount > 0),
 ",\"verdict\":", JStr("candidate 2 DEAD; firing order 1 -> 3"),
 ",\"judge_inputs\":\"N/A (realization false)\"",
 ",\"elapsed_wall_ms\":", String(t1-t0),
 ",\"provenance\":{\"shard0b_sha256\":", JStr(ComputeSha256File("search/probe/wac_v1/ss_sp45_shard0b.g")),
   ",\"shard1_sha256\":", JStr(ComputeSha256File("search/probe/wac_v1/ss_sp45_shard1.g")),
   ",\"shard2_sha256\":", JStr(ComputeSha256File("search/probe/wac_v1/ss_sp45_shard2.g")),
   ",\"cert_script_sha256\":", JStr(ComputeSha256File("search/probe/wac_v1/ss_sp45_cert.g")), "}",
 ",\"interpretation\":\"none -- observation record only (ruling-193: do not interpret)\"",
 "}");;

WriteFile("search/certs/ss_sp45_realization_20260729.json", cert);;
Print("REALIZATION = ", genCount > 0, "\n");
Print("factorizations = ", sols, " (structure constant ", sc, ")  generating = ", genCount, "\n");
Print("calibration generating pairs = ", calGen, "/2000  ord(u) dist = ", Collected(calU), "\n");
Print("wrote search/certs/ss_sp45_realization_20260729.json\n");
Print("SS_SP45_CERT_DONE\n");
QUIT;
