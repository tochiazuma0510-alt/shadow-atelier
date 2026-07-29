# _probe_a14_orbits.g — I10-8 判定用データ取り: A14 悉皆 survivor(非推移生成群)の軌道分割 census
# 方法: search/_probe_a14_exhaustive.g の列挙をそのまま再走(WLOG u0 固定・偶対合3類全走査・
#   b=a*u0^-1 が位数3 のもの)。各 survivor 対 (a,b) について <a,b> の軌道分割
#   (OrbitsDomain のサイズ多重集合・降順)を [k, btype, |H|, orbit_partition] の census として集計する。
#   T=(9,2,2,1) と T=(9,1^5) の両方を走査。
# 規律: ideas/ は読まない(接触遮断)。commit しない。
Read("search/gaplib_common.g");;

LoadPackage("ctbllib");;
n := 14;;
G := AlternatingGroup(n);;
sizeG := Size(G);;
one := ();;

matchPatterns := function(m)
  local rec_;
  rec_ := function(pts)
    local res, q, rest, sub;
    if Length(pts) = 0 then return [ [] ]; fi;
    res := [];
    for q in pts{[2..Length(pts)]} do
      rest := Filtered(pts, x -> x <> pts[1] and x <> q);
      for sub in rec_(rest) do
        Add(res, Concatenation([[pts[1], q]], sub));
      od;
    od;
    return res;
  end;
  return rec_([1..m]);
end;;

# 軌道分割: <a,b> の [1..n] 上の軌道サイズ多重集合を降順ソートしたリストで表す
OrbitPartition := function(grp)
  local orbs, sizes;
  orbs := Orbits(grp, [1..n]);
  sizes := List(orbs, Length);
  Sort(sizes, function(x,y) return x > y; end);
  return sizes;
end;;

sweep := function(u0, label)
  local u0inv, res, k, m, fixSets, pat, fs, supp, mp, imgs, pr, a, b, grp, part;
  u0inv := u0^-1;;
  res := rec(label := label, hits := [], btypes := [], survivors := [], checked := 0, b3count := 0);;
  for k in [6, 4, 2] do
    m := 2*k;;
    fixSets := Combinations([1..n], n - m);;
    pat := matchPatterns(m);;
    Print("  class 2^", k, "1^", n-m, ": ", Length(fixSets), " x ", Length(pat), "\n");
    for fs in fixSets do
      supp := Filtered([1..n], x -> not x in fs);;
      for mp in pat do
        imgs := [1..n];
        for pr in mp do
          imgs[supp[pr[1]]] := supp[pr[2]];
          imgs[supp[pr[2]]] := supp[pr[1]];
        od;
        a := PermList(imgs);
        res.checked := res.checked + 1;
        b := a * u0inv;
        if b <> one and b^3 = one then
          res.b3count := res.b3count + 1;
          Add(res.btypes, [k, CycleStructurePerm(b)]);
          grp := Group(a, b);
          part := OrbitPartition(grp);
          # census 記帳: [a型k, b型, |<a,b>|, orbit_partition]
          Add(res.survivors, [k, CycleStructurePerm(b), Size(grp), part]);
          if IsTransitive(grp, [1..n]) and Size(grp) = sizeG then
            Add(res.hits, rec(a := a, b := b));
            Print("  *** HIT [", label, "]: a=", a, "  b=", b, "\n");
          fi;
        fi;
      od;
    od;
  od;
  Print("  [", label, "] checked=", res.checked, " b3(order3)=", res.b3count,
        " HITS=", Length(res.hits), "\n");
  return res;
end;;

u0a := PermList(Concatenation([2,3,4,5,6,7,8,9,1], [11,10], [13,12], [14]));;
u0b := PermList(Concatenation([2,3,4,5,6,7,8,9,1], [10,11,12,13,14]));;
Print("u0a cycstruct: ", CycleStructurePerm(u0a), "\n");
Print("u0b cycstruct: ", CycleStructurePerm(u0b), "\n");

r1 := sweep(u0a, "T=(9,2,2,1)");;
r2 := sweep(u0b, "T=(9,1^5)");;

# ---- census 集計: [k, btype, |H|, orbit_partition] -> 度数 ----
census1 := Collected(r1.survivors);;
census2 := Collected(r2.survivors);;

Print("census1 entries: ", Length(census1), "\n");
Print("census2 entries: ", Length(census2), "\n");

# ---- JSON 化 ----
# CycleStructurePerm(p)[i] = p の長さ (i+1) のサイクルの個数(固定点除く・GAP 仕様)。
# JSON では [cycle_length, count] の対で書き出す(cycle_length = i+1)。
CycStructToJson := function(cs)
  local parts, i;
  parts := [];
  for i in [1..Length(cs)] do
    if IsBound(cs[i]) and cs[i] <> 0 and cs[i] <> fail then
      Add(parts, JPair(i+1, cs[i]));
    fi;
  od;
  return JArr(parts);
end;;

CensusEntryToJson := function(entry)
  local key, count;
  key := entry[1];
  count := entry[2];
  return Concatenation(
    "{\"a_k\":", String(key[1]),
    ",\"b_cycstruct\":", CycStructToJson(key[2]),
    ",\"group_order\":", String(key[3]),
    ",\"orbit_partition\":", JArr(List(key[4], String)),
    ",\"count\":", String(count),
    "}"
  );
end;;

census1Json := JArr(List(census1, CensusEntryToJson));;
census2Json := JArr(List(census2, CensusEntryToJson));;

scriptSha256 := function(relpath)
  local tmp, f, line;
  tmp := "search/.tmp_sha256_out_a14orbits.txt";;
  Exec(Concatenation("sha256sum \"", relpath, "\" > \"", tmp, "\""));;
  f := InputTextFile(tmp);;
  line := ReadLine(f);;
  CloseStream(f);;
  Exec(Concatenation("rm -f \"", tmp, "\""));;
  return line{[1..64]};
end;;
selfSha := scriptSha256("search/_probe_a14_orbits.g");;

elapsedMs := GAPLIB_WallElapsedMs();;

cert := Concatenation(
  "{\"schema\":\"a14-orbit-census/v1\"",
  ",\"label\":\"I10-8-orbit-census\"",
  ",\"generated_by\":{\"tool\":\"GAP ", GAPInfo.Version, "\",\"script\":\"search/_probe_a14_orbits.g\"}",
  ",\"design_source\":\"search/_probe_a14_exhaustive.g の列挙を再走し survivor 対の軌道分割を追加集計(I10-8 判定用データ取り)\"",
  ",\"n\":14",
  ",\"universe\":\"A14 悉皆: WLOG u0 固定・偶対合3類(2^6 1^2, 2^4 1^6, 2^2 1^10)全走査・b=a*u0^-1 が位数3\"",
  ",\"schema_note\":\"census entries は [a_k(=aの互換数), b_cycstruct(=bのサイクル構造), group_order(=|<a,b>|), orbit_partition(=[1..14]上の<a,b>軌道サイズの降順多重集合)] の組ごとの度数。orbit_partition=[14]は推移的(A14全体または真部分群窓)。\"",
  ",\"T_9_2_2_1\":{\"checked\":", String(r1.checked), ",\"b3count\":", String(r1.b3count),
  ",\"hits\":", String(Length(r1.hits)), ",\"census\":", census1Json, "}",
  ",\"T_9_1_5\":{\"checked\":", String(r2.checked), ",\"b3count\":", String(r2.b3count),
  ",\"hits\":", String(Length(r2.hits)), ",\"census\":", census2Json, "}",
  ",\"elapsed_wall_ms\":", String(elapsedMs),
  ",\"provenance\":{\"script_sha256\":\"", selfSha, "\"}",
  "}"
);;

outPath := "search/certs/a14_orbit_census_20260730.json";;
WriteFile(outPath, cert);;

Print("\n証明書を書き出した: ", outPath, "\n");
Print("script sha256 = ", selfSha, "\n");
Print("elapsed_wall_ms = ", elapsedMs, "\n");
Print("\nA14-ORBIT-CENSUS DONE\n");
QUIT_GAP(0);
