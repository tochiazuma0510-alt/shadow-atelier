## ss_sp45_shard2.g -- shard 2: 否定的結果の較正と診断
##  (a) 78 対が張る部分群の正体(位数・構造)
##  (b) **較正**: 同じ判定器で PSp(4,5) の (2,3)-生成対が実際に見つかる(TRUE を返せる)
##      ことを確認する。負の結果は「判定器が常に FALSE を返すバグ」と区別できねばならない。
##  (c) 生成対で実現しうる ord(u) の分布(どの N_ord なら到達するか)
SizeScreen([4096,0]);;
Read("search/gaplib_common.g");
t0 := GAPLIB_WallElapsedMs();;
Print("############ ss_sp45 shard2: 較正と診断 ############\n");

G := Image(IsomorphismPermGroup(PSp(4,5)));;
n := Size(G);;
ccl := ConjugacyClasses(G);;
ordsC := List(ccl, c -> Order(Representative(c)));;
cenC  := List(ccl, c -> Size(Centralizer(G, Representative(c))));;
iX := Filtered([1..Length(ccl)], i -> ordsC[i]=6 and cenC[i]=360)[1];;
iU := Filtered([1..Length(ccl)], i -> ordsC[i]=12 and Representative(ccl[i])^2 in ccl[iX])[1];;
u := Representative(ccl[iU]);;

# (a) 78 対が張る部分群
Print("\n--- (a) 78 対が張る部分群 ---\n");
subs := [];;
for i in Filtered([1..Length(ccl)], j -> ordsC[j]=2) do
  for q in AsList(ccl[i]) do
    if Order(u*q) = 3 then
      Add(subs, Size(Group(q, (u*q)^-1)));
    fi;
  od;
od;
Print("  部分群位数の分布 = ", Collected(subs), "\n");
Print("  |P| = ", n, " に達したもの = ", Length(Filtered(subs, s -> s = n)), "/", Length(subs), "\n");
for sz in Set(subs) do
  Print("    位数 ", sz, " : 指数 ", n/sz, "\n");
od;
# 代表 1 個の構造
for i in Filtered([1..Length(ccl)], j -> ordsC[j]=2) do
  for q in AsList(ccl[i]) do
    if Order(u*q) = 3 then
      H := Group(q, (u*q)^-1);
      Print("  代表の構造 = ", StructureDescription(H), "  |H| = ", Size(H),
            "  H は P で正規? ", IsNormal(G,H), "\n");
      break;
    fi;
  od;
  break;
od;
if GAPLIB_CheckCap(600.0, "shard2a") then Error("cap"); fi;

# (b) 較正: 判定器が TRUE を返せるか(PSp(4,5) の (2,3)-生成対を探す)
Print("\n--- (b) 較正: 同じ判定器で (2,3)-生成対を見つける ---\n");
RandOrd := function(GG, d)
  local g, o, t;
  t := 0;
  repeat g := Random(GG); o := Order(g); t := t+1;
    if t > 400 then return fail; fi;
  until o mod d = 0;
  return g^(o/d);
end;;
Reset(GlobalMersenneTwister, 20260729);;
genFound := 0;;  uOrds := [];;  firstPair := fail;;
for i in [1..2000] do
  a1 := RandOrd(G,2);  b1 := RandOrd(G,3);
  if a1 = fail or b1 = fail then continue; fi;
  if Size(Group(a1,b1)) = n then
    genFound := genFound + 1;
    Add(uOrds, Order(b1^-1*a1));
    if firstPair = fail then firstPair := [a1,b1]; fi;
  fi;
od;
Print("  2000 試行中の (2,3)-生成対 = ", genFound, "\n");
Print("  ** 較正判定: 判定器は TRUE を返せる = ", genFound > 0, " **\n");
Print("  生成対で実現した ord(b1^-1 a1) の分布 = ", Collected(uOrds), "\n");
Print("  そのうち ord(u)=12 のもの = ", Length(Filtered(uOrds, o -> o = 12)), "\n");
if GAPLIB_CheckCap(600.0, "shard2b") then Error("cap"); fi;

# (c) 生成対が到達する u の類(ord(u)=12 の 2 類のどちらか)
Print("\n--- (c) 生成対が到達する位数 12 の類 ---\n");
Reset(GlobalMersenneTwister, 20260730);;
hit12 := [];;
for i in [1..3000] do
  a1 := RandOrd(G,2);  b1 := RandOrd(G,3);
  if a1 = fail or b1 = fail then continue; fi;
  uu := b1^-1*a1;
  if Order(uu) <> 12 then continue; fi;
  if Size(Group(a1,b1)) <> n then continue; fi;
  Add(hit12, Size(Centralizer(G, uu^2)));
od;
Print("  生成対 かつ ord(u)=12 の事例数 = ", Length(hit12), "\n");
Print("  その u^2 の中心化群位数の分布 = ", Collected(hit12),
      "  (目標は 360 — 出現すれば shard1 と矛盾)\n");

Print("\n経過 = ", (GAPLIB_WallElapsedMs()-t0)/1000.0, " s\n");
Print("SS_SP45_SHARD2_DONE\n");
QUIT;
