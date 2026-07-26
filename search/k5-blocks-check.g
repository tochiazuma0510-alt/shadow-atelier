#############################################################################
# search/k5-blocks-check.g -- S5-1/S5-2/S5-3 の GAP 側照合(第二系統)
#
# 委嘱: docs/week4-K5_S5設計_opus_v1.md の命題 S5-1/S5-2/S5-3 を、凍結済み
# 有限 fixture(certificates/k5fixture/K5-sq.json, K5-ns.json の perm_triple
# フィールド = D1 で確立済みの G_5 の 10 点 coset 作用)の上で GAP により
# 独立に照合する(node 側 crosscheck/check-k5-blocks.mjs と helper 非共有)。
#
# 接触禁止: 曲線・λ・u・数値近似・database には一切触れない。入力は
# perm_triple(sigma_0, sigma_1, sigma_infty: 10 点上の置換, one-line 0-indexed)
# のみ — docs/manifest_k5_appendixA_v1.md 1.2/1.3 に手で転記された値であり、
# 本スクリプトが独立に固定入力として使う(D1 mjs/.g のコードは読まない)。
#
# 対象命題:
#  S5-1: 二標的(K5-sq, K5-ns)の 10 点作用は、非自明なブロック系がちょうど
#        一つで、2 ブロック x サイズ 5 であること。
#  S5-2: そのブロック(5 点)上への sigma_0^2, sigma_1, sigma_infty^2 の制限が
#        生成する群が位数 10 で D_5(GAP DihedralGroup(10))に同型であること。
#        型は (5, 2.2.1, 5) であること。sigma_0, sigma_infty はブロックを
#        入れ替え、sigma_1 は保つこと。
#  S5-3: Lemma S5-B の群論的主張 — Mon := <sigma_0,sigma_1> (位数 100) の中で
#        点 1 の安定化群 Hbar (位数 10) を含む中間部分群 K を全列挙すると、
#        |K|=20 は 0 個・|K|=50 はちょうど 1 個であること
#        (design 文書 §2.4 の証明のうち §7 論点 2 で GAP 再現を要請された部分)。
#
# 実行: .\gap.ps1 search\k5-blocks-check.g
#############################################################################

Read("search/gaplib_common.g");

# ---------------------------------------------------------------- fixture data
# 出所: certificates/k5fixture/K5-sq.json / K5-ns.json の "perm_triple" フィールド
# (= docs/manifest_k5_appendixA_v1.md §1.2/1.3 の転記値と同一・0-indexed one-line)。
Fixtures := rec(
  sq := rec(
    s0 := [1,2,3,4,5,6,7,8,9,0],
    s1 := [0,1,8,9,6,7,4,5,2,3],
    sInf := [3,0,1,8,9,6,7,4,5,2]
  ),
  ns := rec(
    s0 := [1,2,3,4,5,6,7,8,9,0],
    s1 := [4,7,2,5,0,3,8,1,6,9],
    sInf := [9,4,7,2,5,0,3,8,1,6]
  )
);;

# 0-indexed image list -> GAP PermList (1-indexed): i^p = list0[i-1] + 1
ToPerm := function(list0)
  return PermList(List(list0, x -> x + 1));
end;;

CycleTypeOn := function(g, dom)
  local lens;
  lens := ShallowCopy(CycleLengths(g, dom));
  Sort(lens, function(a,b) return a > b; end);
  return lens;
end;;

results := rec();;

Report := function(name, ok, extra)
  if ok then
    Print("[PASS] ", name, "  ", extra, "\n");
  else
    Print("[FAIL] ", name, "  ", extra, "\n");
  fi;
end;;

totalPass := 0;; totalFail := 0;;
Check := function(name, ok, extra)
  if ok then totalPass := totalPass + 1; else totalFail := totalFail + 1; fi;
  Report(name, ok, extra);
end;;

ProcessTarget := function(label, fx)
  local s0, s1, sInf, dom, ok0, Mon, monOrder, blocksAll, nBlocks, B, blockSys,
        sizes, s0sq, sInfsq, quotHom, quotImgs, restr, D5cand,
        d5order, isD5, types, Hbar, ccs, overgroups, k20, k50, U,
        g, K, seen, found, rec2, kk;
  dom := [1..10];
  s0 := ToPerm(fx.s0); s1 := ToPerm(fx.s1); sInf := ToPerm(fx.sInf);
  # defaults (kept bound even if a precondition branch is skipped)
  B := []; blockSys := []; sizes := []; d5order := 0; isD5 := false;

  Print("\n==== target: ", label, " ====\n");

  # -- sanity: sigma_0 sigma_1 sigma_infty = id, convention (p o q)(i) = p(q(i))
  # i.e. apply sigma_infty first, then sigma_1, then sigma_0.
  # GAP: i^(g*h) = (i^g)^h -> want i^(sInf*s1*s0) = i for all i.
  ok0 := sInf*s1*s0 = ();
  Check(Concatenation(label, "-S0 sigma_0 sigma_1 sigma_infty = id (composition conv.)"), ok0, "");

  Mon := Group(s0, s1);
  monOrder := Size(Mon);
  Check(Concatenation(label, "-S0b |Mon| = |<sigma_0,sigma_1>| = 100"), monOrder = 100, Concatenation("got ", String(monOrder)));

  # ---------------------------------------------------------- S5-1: blocks
  blocksAll := AllBlocks(Mon);
  nBlocks := Length(blocksAll);
  Check(Concatenation(label, "-S5.1a exactly one nontrivial block system"), nBlocks = 1,
        Concatenation("|AllBlocks| = ", String(nBlocks)));

  if nBlocks >= 1 then
    B := blocksAll[1];
    Check(Concatenation(label, "-S5.1b block size = 5"), Length(B) = 5, Concatenation("|B| = ", String(Length(B))));
    blockSys := Orbit(Mon, Set(B), OnSets);
    sizes := List(blockSys, Length);
    Check(Concatenation(label, "-S5.1c full block system = 2 blocks x size 5 (partition of 10 pts)"),
          Length(blockSys) = 2 and ForAll(sizes, s -> s = 5)
            and Length(Union(blockSys)) = 10,
          Concatenation("blocks = ", String(sizes)));
  else
    B := [];
    blockSys := [];
  fi;

  # ---------------------------------------------------- swap / preserve check
  if Length(blockSys) = 2 then
    quotHom := ActionHomomorphism(Mon, blockSys, OnSets);
    quotImgs := List([s0, s1, sInf], g -> Image(quotHom, g));
    Check(Concatenation(label, "-S5.1d sigma_0 swaps the 2 blocks"), quotImgs[1] <> (), "");
    Check(Concatenation(label, "-S5.1e sigma_1 preserves the 2 blocks (fixes both)"), quotImgs[2] = (), "");
    Check(Concatenation(label, "-S5.1f sigma_infty swaps the 2 blocks"), quotImgs[3] <> (), "");
  fi;

  # ---------------------------------------------------- S5-2: D5 on the block
  if Length(B) = 5 then
    B := Set(B);
    s0sq := s0^2; sInfsq := sInf^2;
    if IsSubset(B, OnTuples(B, s0sq)) and IsSubset(B, OnTuples(B, s1)) and IsSubset(B, OnTuples(B, sInfsq)) then
      restr := [ RestrictedPerm(s0sq, B), RestrictedPerm(s1, B), RestrictedPerm(sInfsq, B) ];
      types := [ CycleTypeOn(s0sq, B), CycleTypeOn(s1, B), CycleTypeOn(sInfsq, B) ];
      Check(Concatenation(label, "-S5.2a cycle type sigma_0^2|B = (5)"), types[1] = [5], Concatenation("got ", String(types[1])));
      Check(Concatenation(label, "-S5.2b cycle type sigma_1|B = (2,2,1)"), types[2] = [2,2,1], Concatenation("got ", String(types[2])));
      Check(Concatenation(label, "-S5.2c cycle type sigma_infty^2|B = (5)"), types[3] = [5], Concatenation("got ", String(types[3])));

      D5cand := Group(restr[1], restr[2], restr[3]);
      d5order := Size(D5cand);
      Check(Concatenation(label, "-S5.2d |<sigma_0^2,sigma_1,sigma_infty^2>| on B = 10"), d5order = 10, Concatenation("got ", String(d5order)));
      isD5 := IsomorphismGroups(D5cand, DihedralGroup(10)) <> fail;
      Check(Concatenation(label, "-S5.2e monodromy on B is isomorphic to D_5 (GAP DihedralGroup(10))"), isD5, "");
    else
      Check(Concatenation(label, "-S5.2 (precondition) sigma_0^2, sigma_1, sigma_infty^2 preserve B"), false, "");
    fi;
  fi;

  # ---------------------------------------------------- S5-3: intermediate subgroups
  Hbar := Stabilizer(Mon, 1);
  Check(Concatenation(label, "-S5.3a |Hbar| = |Stab_Mon(1)| = 10"), Size(Hbar) = 10, Concatenation("got ", String(Size(Hbar))));

  ccs := ConjugacyClassesSubgroups(Mon);
  overgroups := [];
  seen := [];
  for U in List(ccs, Representative) do
    for g in Mon do
      K := ConjugateSubgroup(U, g);
      found := false;
      for kk in [1..Length(seen)] do
        if seen[kk] = K then found := true; break; fi;
      od;
      if not found then
        Add(seen, K);
        if IsSubset(K, Hbar) then Add(overgroups, K); fi;
      fi;
    od;
  od;

  k20 := Filtered(overgroups, K -> Size(K) = 20);
  k50 := Filtered(overgroups, K -> Size(K) = 50);
  Check(Concatenation(label, "-S5.3b intermediate |K|=20 with Hbar<=K<=Mon: count = 0"), Length(k20) = 0,
        Concatenation("count = ", String(Length(k20))));
  Check(Concatenation(label, "-S5.3c intermediate |K|=50 with Hbar<=K<=Mon: count = 1"), Length(k50) = 1,
        Concatenation("count = ", String(Length(k50))));
  # sanity: overgroups must include Mon itself (|K|=100) and Hbar itself (|K|=10)
  Check(Concatenation(label, "-S5.3d overgroup lattice sane: includes Hbar(10) and Mon(100) exactly once each"),
        Length(Filtered(overgroups, K -> Size(K) = 10)) = 1 and Length(Filtered(overgroups, K -> Size(K) = 100)) = 1,
        Concatenation("all sizes = ", String(SortedList(List(overgroups, Size)))));

  rec2 := rec(
    target := label,
    monOrder := monOrder,
    nBlockSystems := nBlocks,
    blockSizes := sizes,
    overgroupSizes := SortedList(List(overgroups, Size)),
    d5order := d5order,
    isD5 := isD5
  );
  results.(label) := rec2;
end;;

ProcessTarget("sq", Fixtures.sq);
ProcessTarget("ns", Fixtures.ns);

Print("\n=== ", totalPass, "/", totalPass + totalFail, " PASS ===\n");

# ---------------------------------------------------------------- certificate
certJson := Concatenation(
  "{",
  "\"pass\":", String(totalPass), ",",
  "\"fail\":", String(totalFail), ",",
  "\"targets\":{",
  "\"sq\":{",
    "\"monOrder\":", String(results.sq.monOrder), ",",
    "\"nBlockSystems\":", String(results.sq.nBlockSystems), ",",
    "\"blockSizes\":", JArr(List(results.sq.blockSizes, String)), ",",
    "\"overgroupSizes\":", JArr(List(results.sq.overgroupSizes, String)), ",",
    "\"d5order\":", String(results.sq.d5order), ",",
    "\"isD5\":", JB(results.sq.isD5),
  "},",
  "\"ns\":{",
    "\"monOrder\":", String(results.ns.monOrder), ",",
    "\"nBlockSystems\":", String(results.ns.nBlockSystems), ",",
    "\"blockSizes\":", JArr(List(results.ns.blockSizes, String)), ",",
    "\"overgroupSizes\":", JArr(List(results.ns.overgroupSizes, String)), ",",
    "\"d5order\":", String(results.ns.d5order), ",",
    "\"isD5\":", JB(results.ns.isD5),
  "}",
  "}",
  "}"
);;

WriteFile("certificates/k5blocks/k5-blocks-check.gap.json", certJson);;
Print("wrote certificates/k5blocks/k5-blocks-check.gap.json\n");

if totalFail > 0 then
  Print("*** THERE ARE FAILURES ***\n");
fi;

QUIT;
