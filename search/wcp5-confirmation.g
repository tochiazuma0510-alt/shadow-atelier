#############################################################################
## search/wcp5-confirmation.g -- 候補確認レシピ(裁定157)第一号適用: 窓 W-C-p5
##
## 対象: isotropy 群 GTSh(N5,N5), N5 = ker(B3 -> S3 x SL(2,F5))
## (search/wall-miner-v1.g Task B の構成を再利用; c notin N5 につき語レベル評価
##  -- week3-battery-common.g の EnumerateWordLevelHexagonPrepend / c_in_N=false
##  分岐を使う。商像 Aut では数えない。)
##
## 手順(委嘱どおり):
##  1. B3/N5 (位数720) を具体化 -> A_N5 = PB3/N5 (位数120, 期待 SL(2,5)) を抽出。
##     N_ord = lcm(ord x, ord y, ord c) を記録。
##  2. 候補列挙 m in Z/N_ord (gcd(2m+1,2*N_ord)=1) x f in [P5,P5]=P5 (完全群).
##     両 hexagon (3.3)(3.4) を B3/N5 内の語レベルで判定 -> shadow 集合。
##     (実装: reduced hexagon (3.10)/(3.11) 経路 = EnumerateWordLevelHexagonPrepend
##      -- これは D=[G,G] 上の f と charming m の候補に対し、generation check で
##      T_{m,f} の全射性(=有限群では双射=自己同型)まで検査するので、手順3の
##      source kernel 判定を兼ねる。)
##  3. source kernel 同定: 上の generation check が ker(T)=N5 (=全射自己準同型)
##     の判定そのもの -- 通過した shadow だけが GTSh(N5,N5) の元。
##  4. (3.53) で合成表を構成 -> 群であることを assert -> |GTSh|, ker(chi~) の
##     可換性, 導来列。T-A 個数等式を fail-closed assert。
##  5. witness: 非可換なら交換子 <>1 の具体元組。可換なら全対可換の走査数。
##  6. 独立再計算: 別経路(full hexagon (3.3)/(3.4) を B3/N5 の720点表現
##     BuildQTGeneral 上で直接判定 -- 裁定147 方式)で同じ shadow 集合を再列挙し、
##     集合一致 + ker(chi~) 可換性の再判定。
##
## 出力: search/certs/wcp5_confirmation_20260729.json
#############################################################################

SizeScreen([4096, 0]);;
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");

t0 := GAPLIB_WallElapsedMs();;

#############################################################################
## ---- 1. B3/N5 (位数720) の具体化 (wall-miner-v1.g Task B 再利用) ----------
#############################################################################
BF3 := FreeGroup("a", "b");;
aa := BF3.1;;  bb := BF3.2;;
brel := aa * bb * aa * (bb * aa * bb)^-1;;
B3 := BF3 / [brel];;
ga := B3.1;;  gb := B3.2;;

S3can := SymmetricGroup(3);;
phiCan := GroupHomomorphismByImages(B3, S3can, [ga, gb], [(1,2), (2,3)]);;
if phiCan = fail then Error("canonical B3 -> S3 map failed sanity check"); fi;
PB3 := Kernel(phiCan);;

x0 := ga^2;;  y0 := gb^2;;  c0 := (ga * gb * ga)^2;;

M1_2 := [[1,1],[0,1]] * One(GF(2));;
M2_2 := [[1,0],[1,1]] * One(GF(2));;   # -1 mod 2 = 1
M1_5 := [[1,1],[0,1]] * One(GF(5));;
M2_5 := [[1,0],[4,1]] * One(GF(5));;   # -1 mod 5 = 4

Gmat2 := Group(M1_2, M2_2);;
Gmat5 := Group(M1_5, M2_5);;
psi2 := IsomorphismPermGroup(Gmat2);;
psi5 := IsomorphismPermGroup(Gmat5);;
P2perm := Image(psi2);;
P5perm := Image(psi5);;
Print("|SL(2,2)|=", Size(P2perm), " |SL(2,5)|=", Size(P5perm), "\n");

DP5 := DirectProduct(P2perm, P5perm);;
emb1 := Embedding(DP5, 1);;
emb2 := Embedding(DP5, 2);;
xDP5 := Image(emb1, Image(psi2, M1_2)) * Image(emb2, Image(psi5, M1_5));;
yDP5 := Image(emb1, Image(psi2, M2_2)) * Image(emb2, Image(psi5, M2_5));;
braidHoldsDP5 := (xDP5*yDP5*xDP5 = yDP5*xDP5*yDP5);;
Print("braid relation holds in S3 x SL(2,F5)? ", braidHoldsDP5, "\n");
Print("|B3/N5| = ", Size(DP5), "\n");

homB3DP5 := GroupHomomorphismByImages(B3, DP5, [ga, gb], [xDP5, yDP5]);;
if homB3DP5 = fail then
  Error("GroupHomomorphismByImages B3->S3xSL(2,F5) failed unexpectedly");
fi;

A_N5 := Image(homB3DP5, PB3);;
ximg_N5 := Image(homB3DP5, x0);;
yimg_N5 := Image(homB3DP5, y0);;
cimg_N5 := Image(homB3DP5, c0);;
Print("|PB3/N5| = ", Size(A_N5), "  StructureDescription = ", StructureDescription(A_N5), "\n");

# --- assertions per commander spec step 1 ---
assertP5Order := (Size(A_N5) = 120);;
assertGoursat := (Size(A_N5) = Size(P5perm));;   # Goursat: image should be all of SL(2,5)
Print("[", PF(assertP5Order), "] |PB3/N5| = 120\n");
Print("[", PF(assertGoursat), "] Goursat: A_N5 = full SL(2,5) (|A_N5|=|SL(2,5)|)\n");

ordX := Order(ximg_N5);;  ordY := Order(yimg_N5);;  ordC := Order(cimg_N5);;
N_ord := Lcm(ordX, ordY, ordC);;
cInN5 := (cimg_N5 = Identity(A_N5));;
Print("ord(x)=", ordX, " ord(y)=", ordY, " ord(c)=", ordC, " N_ord=", N_ord, " c_in_N5=", cInN5, "\n");
assertOrdC2 := (ordC = 2);;
assertCNotInN5 := (not cInN5);;
Print("[", PF(assertOrdC2), "] ord(c) = 2\n");
Print("[", PF(assertCNotInN5), "] c NOT in N5 (word-level evaluation required)\n");

genOK_A_N5 := (Size(Group(ximg_N5, yimg_N5)) = Size(A_N5));;
Print("[", PF(genOK_A_N5), "] <x,y> = A_N5 (x,y generate the full quotient)\n");

qrec := rec(x := ximg_N5, y := yimg_N5, c := cimg_N5, G := A_N5);;

D_N5 := DerivedSubgroup(A_N5);;
isPerfect := (Size(D_N5) = Size(A_N5));;
Print("[", PF(isPerfect), "] A_N5 is perfect ([P5,P5]=P5): |D|=", Size(D_N5), " |A_N5|=", Size(A_N5), "\n");

#############################################################################
## ---- 2/3. candidate enumeration + word-level hexagon + source kernel -----
#############################################################################
charmingSet := Filtered([0..N_ord-1], mm -> Gcd(2*mm+1, 2*N_ord) = 1);;
Print("charming_set = ", charmingSet, " (count=", Length(charmingSet), ")\n");
# sanity: gcd(2m+1,2*N_ord)=1 is equivalent to gcd(2m+1,N_ord)=1 since 2m+1 is odd
charmingSetAlt := Filtered([0..N_ord-1], mm -> Gcd(2*mm+1, N_ord) = 1);;
charmingSetsAgree := (charmingSet = charmingSetAlt);;
Print("[", PF(charmingSetsAgree), "] charming set gcd(.,2*N_ord) agrees with gcd(.,N_ord)\n");

candidateTotalExpected := Length(charmingSet) * Size(D_N5);;
Print("candidate_total_expected (|charming_set| x |D|) = ", candidateTotalExpected, "\n");

t1 := GAPLIB_WallElapsedMs();;
Print("[timing] pre-enumeration setup: ", (t1-t0)/1000.0, " s\n");

wlResult := EnumerateWordLevelHexagonPrepend(qrec, charmingSet);;
t2 := GAPLIB_WallElapsedMs();;
Print("[timing] word-level enumeration (Method A, reduced hexagon prepend): ", (t2-t1)/1000.0, " s\n");
Print("candidate_total=", wlResult.candidate_total, " h10_fail=", wlResult.h10_fail,
      " h11_fail=", wlResult.h11_fail, " generation_fail=", wlResult.generation_fail,
      " shadow_total=", wlResult.shadow_total, "\n");
Print("quotient_shortcut_available (diagnostic only, expect false since c notin N5) = ",
      wlResult.quotient_shortcut_available, "\n");

shadowSumOk := (wlResult.candidate_total - wlResult.h10_fail - wlResult.h11_fail
                - wlResult.generation_fail = wlResult.shadow_total);;
Print("[", PF(shadowSumOk), "] shadow_total subtraction consistency\n");
candidateCountOk := (wlResult.candidate_total = candidateTotalExpected);;
Print("[", PF(candidateCountOk), "] candidate_total matches |charming_set| x |D|\n");

shadows := wlResult.shadows;;
nShadow := Length(shadows);;
Print("|GTSh(N5,N5)| (shadow_total, Method A) = ", nShadow, "\n");

#############################################################################
## ---- 4. composition table (3.53), group assert, ker(chi~), derived series -
#############################################################################
# (3.53): [m1,f1] o [m2,f2] = [(2 m1 m2 + m1 + m2) mod N_ord, f1 . E_{m1,f1}(f2)]
BuildCompTable := function(qrec, shadows, Nord)
  local n, i1, i2, m1, f1, m2, f2, u1, Ehom, newm, newf, idx, t, tbl, closureFail;
  n := Length(shadows);;
  tbl := [];;  closureFail := 0;;
  for i1 in [1..n] do
    m1 := shadows[i1].m;;  f1 := shadows[i1].f;;  u1 := 2*m1+1;;
    Ehom := GroupHomomorphismByImages(qrec.G, qrec.G, [qrec.x, qrec.y],
              [qrec.x^u1, AbstractProd([f1^-1, qrec.y^u1, f1])]);;
    if Ehom = fail then
      Error("BuildCompTable: E_{m1,f1} construction failed, i1=", i1);
    fi;
    for i2 in [1..n] do
      m2 := shadows[i2].m;;  f2 := shadows[i2].f;;
      newm := (2*m1*m2 + m1 + m2) mod Nord;;
      newf := AbstractProd([f1, Image(Ehom, f2)]);;
      idx := fail;;
      for t in [1..n] do
        if shadows[t].m = newm and shadows[t].f = newf then idx := t; break; fi;
      od;
      if idx = fail then
        closureFail := closureFail + 1;;
        Add(tbl, [i1-1, i2-1, -1]);;
      else
        Add(tbl, [i1-1, i2-1, idx-1]);;
      fi;
    od;
  od;
  return rec(tbl:=tbl, closureFail:=closureFail, n:=n);;
end;;

BuildRegularPermGroupFromTable := function(tbl, n)
  local prod, e, gens, a, images, b;
  prod := List([0..n-1], i -> List([0..n-1], j -> -1));;
  for e in tbl do prod[e[1]+1][e[2]+1] := e[3]; od;;
  for a in [0..n-1] do
    for b in [0..n-1] do
      if prod[a+1][b+1] = -1 then
        Error("BuildRegularPermGroupFromTable: closure failure at (", a, ",", b, ")");
      fi;
    od;
  od;;
  gens := [];;
  for a in [0..n-1] do
    images := List([0..n-1], b -> prod[a+1][b+1] + 1);;
    Add(gens, PermList(images));;
  od;
  return Group(gens);;
end;;

compRes := BuildCompTable(qrec, shadows, N_ord);;
Print("[", PF(compRes.closureFail = 0), "] (3.53) composition table closure (closure_fail_count=",
      compRes.closureFail, ")\n");

if compRes.closureFail > 0 then
  Print("[STOP-REPORT] composition not closed -- GTSh(N5,N5) not confirmed as a group. Reporting, not proceeding to group-structure claims.\n");
  gtshGroupOk := false;;
  gtshOrder := "UNKNOWN";;
  ker_chi_indices := "UNKNOWN";;
  ker_chi_order := "UNKNOWN";;
  ker_chi_abelian := "UNKNOWN";;
  derivedLen := "UNKNOWN";;
  taAssertOk := "UNKNOWN";;
  identityFoundOk := "UNKNOWN";;
  kerChiSubgrpOrderOk := "UNKNOWN";;
  phi2Nord := "UNKNOWN";;
  taExpected := "UNKNOWN";;
  witnessInfo := rec(kind:="unknown", reason:="composition not closed -- see composition_table_closure_fail_count");;
else
  regGrp := BuildRegularPermGroupFromTable(compRes.tbl, compRes.n);;
  gtshOrder := Size(regGrp);;
  gtshGroupOk := (gtshOrder = compRes.n);;   # Group() should reproduce the same order (Latin-square/group check)
  Print("[", PF(gtshGroupOk), "] GTSh(N5,N5) regular perm rep order = ", gtshOrder,
        " (expect = shadow_total = ", compRes.n, ")\n");

  # identity element check: shadow with m=0, f=identity must act as identity of the regular rep
  idxOfIdentity := fail;;
  for t in [1..compRes.n] do
    if shadows[t].m = 0 and shadows[t].f = Identity(A_N5) then idxOfIdentity := t; break; fi;
  od;
  identityFoundOk := (idxOfIdentity <> fail);;
  Print("[", PF(identityFoundOk), "] identity shadow [0, id] present in shadow set (index=", idxOfIdentity, ")\n");

  # ---- ker(chi~) = {[0,f] in GTSh(N5,N5)} ----
  ker_chi_indices := Filtered([1..compRes.n], t -> shadows[t].m = 0);;
  ker_chi_order := Length(ker_chi_indices);;
  Print("|ker(chi~)| (count of m=0 shadows) = ", ker_chi_order, "\n");

  # ---- T-A fail-closed assert: |ker(chi~)| = |GTSh(N5,N5)| / phi(2*N_ord) ----
  phi2Nord := Length(Filtered([0..2*N_ord-1], k -> Gcd(k, 2*N_ord) = 1));;
  taExpected := gtshOrder / phi2Nord;;
  taAssertOk := (IsInt(taExpected) and ker_chi_order = taExpected);;
  Print("phi(2*N_ord) = phi(", 2*N_ord, ") = ", phi2Nord, "\n");
  Print("[", PF(taAssertOk), "] T-A count equality: |ker(chi~)|(", ker_chi_order,
        ") = |GTSh|(", gtshOrder, ") / phi(2*N_ord)(", phi2Nord, ") = ", taExpected, "\n");
  if not taAssertOk then
    Print("[STOP-REPORT] T-A equality FAILED -- reporting, not asserting further group-structure claims blindly.\n");
  fi;

  # ---- ker(chi~) subgroup of regGrp, generated by the perm-images of the m=0 shadow indices ----
  kerChiPerms := List(ker_chi_indices, t -> GeneratorsOfGroup(regGrp)[t]);;
  kerChiSubgrp := Group(kerChiPerms);;
  kerChiSubgrpOrderOk := (Size(kerChiSubgrp) = ker_chi_order);;
  Print("[", PF(kerChiSubgrpOrderOk), "] ker(chi~) subgroup order (via Group() closure of its regGrp generators) = ",
        Size(kerChiSubgrp), " (expect = ", ker_chi_order, ", i.e. subgroup closes exactly on the m=0 shadow set)\n");

  ker_chi_abelian := IsAbelian(kerChiSubgrp);;
  Print("ker(chi~) abelian? ", ker_chi_abelian, "\n");

  # ---- witness ----
  witnessInfo := rec();;
  if ker_chi_abelian then
    # commuting witness: count all pairs (informational, not a proof substitute -- IsAbelian already
    # decides it via GAP's own group-theoretic test; the pairwise count is recorded per commander spec
    # step 5 "全対可換の走査数を記録")
    pairCount := 0;;  allCommute := true;;
    for i1 in [1..Length(kerChiPerms)] do
      for i2 in [1..Length(kerChiPerms)] do
        pairCount := pairCount + 1;;
        if kerChiPerms[i1]*kerChiPerms[i2] <> kerChiPerms[i2]*kerChiPerms[i1] then
          allCommute := false;;
        fi;
      od;
    od;
    witnessInfo := rec(kind:="abelian", pairs_scanned:=pairCount, all_pairs_commute_direct_check:=allCommute,
                        generator_count:=Length(kerChiPerms));;
    Print("witness (abelian): scanned ", pairCount, " generator pairs, all commute (direct check) = ", allCommute, "\n");
  else
    # find a concrete noncommuting pair among the ker(chi~) generators, report their [m,f] coordinates
    # NOTE: uses widx1/widx2/wperm1/wperm2 (NOT t1/t2/p1/p2) to avoid clobbering the top-level
    # timing variables t1..t5 used later for elapsed_wall_ms in the certificate.
    foundPair := fail;;
    for i1 in [1..Length(ker_chi_indices)] do
      for i2 in [1..Length(ker_chi_indices)] do
        widx1 := ker_chi_indices[i1];;  widx2 := ker_chi_indices[i2];;
        wperm1 := GeneratorsOfGroup(regGrp)[widx1];;  wperm2 := GeneratorsOfGroup(regGrp)[widx2];;
        if wperm1*wperm2 <> wperm2*wperm1 then foundPair := [widx1,widx2]; break; fi;
      od;
      if foundPair <> fail then break; fi;
    od;
    if foundPair = fail then
      Error("ker(chi~) non-abelian but no witness pair found among generators -- inconsistent, report to commander");
    fi;
    widx1 := foundPair[1];;  widx2 := foundPair[2];;
    witnessInfo := rec(kind:="nonabelian",
      witness_m1:=shadows[widx1].m, witness_f1_word:=shadows[widx1].word,
      witness_m2:=shadows[widx2].m, witness_f2_word:=shadows[widx2].word);;
    Print("witness (nonabelian): [m1=", shadows[widx1].m, ", f1_word=", shadows[widx1].word,
          "] and [m2=", shadows[widx2].m, ", f2_word=", shadows[widx2].word, "] do NOT commute\n");
  fi;

  # ---- derived series of GTSh(N5,N5) itself ----
  DerivedSeriesLens := function(G)
    local H, Hprev, len, cap, sizes;
    sizes := [Size(G)];;
    if Size(G) = 1 then return rec(len:=0, sizes:=sizes, status:="trivial"); fi;
    H := G;;  len := 0;;  cap := 10;;
    while (not IsTrivial(H)) and len < cap do
      Hprev := H;;
      H := DerivedSubgroup(H);;
      len := len + 1;;
      Add(sizes, Size(H));;
      if Size(H) = Size(Hprev) then
        return rec(len:=-1, sizes:=sizes, status:="stabilized_nonsolvable");;
      fi;
    od;
    if IsTrivial(H) then return rec(len:=len, sizes:=sizes, status:="solvable");
    else return rec(len:=-2, sizes:=sizes, status:="cap_reached_unresolved"); fi;
  end;;
  derivedInfo := DerivedSeriesLens(regGrp);;
  derivedLen := derivedInfo.len;;
  Print("GTSh(N5,N5) derived series sizes = ", derivedInfo.sizes, " status=", derivedInfo.status,
        " derived_length=", derivedLen, "\n");
fi;

t3 := GAPLIB_WallElapsedMs();;
Print("[timing] composition/derived-series analysis: ", (t3-t2)/1000.0, " s\n");

#############################################################################
## ---- 6. independent recomputation: full hexagon (3.3)/(3.4) at B3/N5 -----
##      level via BuildQTGeneral (720 points), per 裁定147 method.
#############################################################################
lab := BuildQTGeneral(A_N5, ximg_N5, yimg_N5, cimg_N5);;
S1 := lab.s1;;  S2 := lab.s2;;
X3 := S1^2;;  Y3 := S2^2;;
Cc := AbstractProd([S1,S2,S1])^2;;
Print("[timing] BuildQTGeneral (720-pt) constructed\n");

# BFS words for all elements of A_N5 (D_N5 = A_N5 since perfect) using the SAME
# prepend-storage BFSWords already used internally by EnumerateWordLevelHexagonPrepend.
bfsIndep := BFSWords(qrec);;
if Length(bfsIndep.elements) <> Size(A_N5) then
  Error("independent recompute: BFS did not cover A_N5");
fi;
DwordsIndep := [];;
for elt in bfsIndep.elements do
  if elt in D_N5 then Add(DwordsIndep, rec(elt:=elt, word:=LookupDictionary(bfsIndep.wordOf, elt))); fi;
od;
Print("independent recompute: |D words| = ", Length(DwordsIndep), " (expect ", Size(D_N5), ")\n");

EvalWordInQ720 := function(word, xImg, yImg)
  local lst, letter;
  lst := [];;
  for letter in word do
    if letter[1] = "x" then Add(lst, xImg^letter[2]); else Add(lst, yImg^letter[2]); fi;
  od;
  if Length(lst) = 0 then return xImg^0; fi;
  return AbstractProd(lst);
end;;

indepShadows := [];;  indepH33Fail := 0;;  indepH34Fail := 0;;  indepGenFail := 0;;
for cand in DwordsIndep do
  f := cand.elt;;
  Gf := EvalWordInQ720(cand.word, X3, Y3);;
  # sanity: Gf (lifted via X3,Y3) must project back to the same element f under the natural quotient
  # (X3=S1^2 <-> ximg_N5, Y3=S2^2 <-> yimg_N5), i.e. EvalWordIn(word, x, y) at level 120 = f (trivially,
  # since word came from f's own BFS word) -- just re-derive via level-120 eval as a cross-check.
  fCheck := EvalWordInQ720(cand.word, ximg_N5, yimg_N5);;
  if fCheck <> f then
    Error("independent recompute: word/elt mismatch at level 120 for candidate f");
  fi;
  for m in charmingSet do
    u := 2*m+1;;
    h33 := AbstractProd([S1^u, Gf^-1, S2^u, Gf]) = AbstractProd([Gf^-1, S1, S2, X3^(-m), Cc^m]);;
    if not h33 then indepH33Fail := indepH33Fail + 1; continue; fi;
    h34 := AbstractProd([Gf^-1, S2^u, Gf, S1^u]) = AbstractProd([S2, S1, Y3^(-m), Cc^m, Gf]);;
    if not h34 then indepH34Fail := indepH34Fail + 1; continue; fi;
    genA := ximg_N5^u;;
    genB := AbstractProd([f^-1, yimg_N5^u, f]);;
    if Size(Group(genA, genB)) <> Size(A_N5) then
      indepGenFail := indepGenFail + 1;;
      continue;
    fi;
    Add(indepShadows, rec(m:=m, f:=f, word:=cand.word));;
  od;
od;
t4 := GAPLIB_WallElapsedMs();;
Print("[timing] independent full-hexagon recompute: ", (t4-t3)/1000.0, " s\n");
Print("independent recompute: candidate_total=", Length(DwordsIndep)*Length(charmingSet),
      " h33_fail=", indepH33Fail, " h34_fail=", indepH34Fail, " gen_fail=", indepGenFail,
      " shadow_total=", Length(indepShadows), "\n");

# ---- set equality check: Method A shadows vs independent (full hexagon) shadows ----
ShadowKeySet := function(shList)
  return Set(List(shList, sh -> [sh.m, sh.f]));;
end;;
setA := ShadowKeySet(shadows);;
setIndep := ShadowKeySet(indepShadows);;
shadowSetsEqual := (setA = setIndep);;
Print("[", PF(shadowSetsEqual), "] shadow set equality: Method A (reduced hexagon, prepend) vs independent (full hexagon (3.3)/(3.4), BuildQTGeneral) -- |A|=",
      Length(setA), " |Indep|=", Length(setIndep), "\n");

# ---- extra diagnostic (implementer-level, NOT an interpretation): if the sets disagree, dump the
# raw symmetric-difference data and test a couple of the CHEAPEST structural hypotheses (m-fixed/
# f-inverse relabeling; m-complement relabeling) mechanically, reporting pass/fail only -- no
# mathematical judgement is made about WHY, this is purely "does this simple relabeling reconcile
# the two lists" so the mathematician/Sol layer has concrete data to start from.
diagInfo := rec(sets_equal := shadowSetsEqual);;
if not shadowSetsEqual then
  onlyInA := Filtered(setA, k -> not (k in setIndep));;
  onlyInIndep := Filtered(setIndep, k -> not (k in setA));;
  Print("|only in Method A| = ", Length(onlyInA), "   |only in Independent| = ", Length(onlyInIndep), "\n");
  # hypothesis 1: same m, f replaced by f^-1
  hyp1MatchCount := 0;;
  for k in onlyInA do
    if [k[1], k[2]^-1] in setIndep then hyp1MatchCount := hyp1MatchCount + 1; fi;
  od;
  # hypothesis 2: m replaced by (N_ord - m) mod N_ord (or similar complement), same f
  hyp2MatchCount := 0;;
  for k in onlyInA do
    if [(N_ord - k[1]) mod N_ord, k[2]] in setIndep then hyp2MatchCount := hyp2MatchCount + 1; fi;
  od;
  # hypothesis 3: m replaced by (N_ord - 1 - k[1]), same f
  hyp3MatchCount := 0;;
  for k in onlyInA do
    if [(N_ord - 1 - k[1]) mod N_ord, k[2]] in setIndep then hyp3MatchCount := hyp3MatchCount + 1; fi;
  od;
  Print("[diagnostic, mechanical only] hyp1 (same m, f<->f^-1) matches: ", hyp1MatchCount, "/", Length(onlyInA), "\n");
  Print("[diagnostic, mechanical only] hyp2 (m<->N_ord-m, same f) matches: ", hyp2MatchCount, "/", Length(onlyInA), "\n");
  Print("[diagnostic, mechanical only] hyp3 (m<->N_ord-1-m, same f) matches: ", hyp3MatchCount, "/", Length(onlyInA), "\n");
  Print("---- only in Method A (m, f as permutation) ----\n");
  for k in onlyInA do
    Print("  m=", k[1], " f=", k[2], "\n");
  od;
  Print("---- only in Independent (m, f as permutation) ----\n");
  for k in onlyInIndep do
    Print("  m=", k[1], " f=", k[2], "\n");
  od;
  # cross-check: for the SAME f appearing in both onlyInA and onlyInIndep (possibly with a
  # different m), report that pairing explicitly (mechanical observation only).
  Print("---- same f, different m (if any) ----\n");
  for k in onlyInA do
    for k2 in onlyInIndep do
      if k[2] = k2[2] then
        Print("  f matches: Method A has m=", k[1], ", Independent has m=", k2[1], " for the SAME f=", k[2], "\n");
      fi;
    od;
  od;
  diagInfo := rec(sets_equal := false, only_in_a_count := Length(onlyInA), only_in_indep_count := Length(onlyInIndep),
                   hyp1_f_inverse_matches := hyp1MatchCount, hyp2_m_complement_matches := hyp2MatchCount,
                   hyp3_m_complement_minus1_matches := hyp3MatchCount);;
fi;

# ---- independent ker(chi~) commutativity re-derivation (only if shadow sets agree and comp table is available) ----
if shadowSetsEqual and gtshGroupOk = true then
  kerChiIndepIndices := Filtered([1..Length(indepShadows)], t -> indepShadows[t].m = 0);;
  # map each indep ker-chi shadow's f back to the composition-table shadow index, then reuse regGrp perms
  indepKerChiPerms := [];;
  for t in kerChiIndepIndices do
    fIndep := indepShadows[t].f;;
    idxMatch := fail;;
    for s in [1..compRes.n] do
      if shadows[s].m = 0 and shadows[s].f = fIndep then idxMatch := s; break; fi;
    od;
    if idxMatch = fail then
      Error("independent ker(chi~): f from independent recompute not found among Method A m=0 shadows");
    fi;
    Add(indepKerChiPerms, GeneratorsOfGroup(regGrp)[idxMatch]);;
  od;
  indepKerChiOrderOk := (Length(indepKerChiPerms) = ker_chi_order);;
  Print("[", PF(indepKerChiOrderOk), "] independent recompute ker(chi~) count = ",
        Length(indepKerChiPerms), " (expect ", ker_chi_order, ")\n");
  indepKerChiAllCommute := true;;
  for i1 in [1..Length(indepKerChiPerms)] do
    for i2 in [1..Length(indepKerChiPerms)] do
      if indepKerChiPerms[i1]*indepKerChiPerms[i2] <> indepKerChiPerms[i2]*indepKerChiPerms[i1] then
        indepKerChiAllCommute := false;;
      fi;
    od;
  od;
  indepAbelianAgrees := (indepKerChiAllCommute = ker_chi_abelian);;
  Print("independent recompute ker(chi~) all pairs commute = ", indepKerChiAllCommute,
        "  [", PF(indepAbelianAgrees), "] agrees with Method A (", ker_chi_abelian, ")\n");
else
  indepKerChiOrderOk := "N/A: shadow sets disagree or comp table unavailable";;
  indepKerChiAllCommute := "N/A";;
  indepAbelianAgrees := "N/A";;
  Print("[SKIP] independent ker(chi~) commutativity re-derivation skipped (shadow set mismatch or comp table unavailable)\n");
fi;

t5 := GAPLIB_WallElapsedMs();;

#############################################################################
## ---- report / certificate -------------------------------------------------
#############################################################################
Print("\n===== SUMMARY (search/wcp5-confirmation.g, window W-C-p5, N5=ker(B3->S3xSL(2,F5))) =====\n");
Print("|A_N5|=|PB3/N5| = ", Size(A_N5), " StructureDescription = ", StructureDescription(A_N5), "\n");
Print("N_ord = ", N_ord, " charming_set = ", charmingSet, "\n");
Print("c_in_N5 = ", cInN5, " (ord c = ", ordC, ")\n");
Print("|GTSh(N5,N5)| (Method A shadow_total) = ", nShadow, "\n");
Print("gtshGroupOk (regular perm rep order matches shadow_total) = ", gtshGroupOk, "\n");
Print("|ker(chi~)| = ", ker_chi_order, "\n");
Print("T-A count equality assert = ", taAssertOk, "\n");
Print("ker(chi~) abelian = ", ker_chi_abelian, "\n");
Print("GTSh(N5,N5) derived_length = ", derivedLen, "\n");
Print("shadow set equality (Method A vs independent full-hexagon) = ", shadowSetsEqual, "\n");
Print("independent ker(chi~) abelian agreement = ", indepAbelianAgrees, "\n");
Print("total elapsed wall = ", t5/1000.0, " s\n");

# ---- JSON certificate ----
WordArrToJson := function(w) return WordToJson(w); end;;

genDetailJson := [];;
for gd in wlResult.generation_detail do
  Add(genDetailJson, Concatenation("{\"m\":", String(gd.m), ",\"f_word\":", WordToJson(gd.f_word),
      ",\"pass\":", JB(gd.pass), ",\"stage\":\"", gd.stage, "\"}"));
od;

shadowsJson := [];;
for sh in shadows do
  Add(shadowsJson, Concatenation("{\"m\":", String(sh.m), ",\"f_word\":", WordToJson(sh.word), "}"));
od;

indepShadowsJson := [];;
for sh in indepShadows do
  Add(indepShadowsJson, Concatenation("{\"m\":", String(sh.m), ",\"f_word\":", WordToJson(sh.word), "}"));
od;

if diagInfo.sets_equal then
  diagJson := Concatenation("{\"sets_equal\":", JB(diagInfo.sets_equal), "}");;
else
  diagJson := Concatenation("{\"sets_equal\":", JB(diagInfo.sets_equal),
    ",\"only_in_a_count\":", String(diagInfo.only_in_a_count),
    ",\"only_in_indep_count\":", String(diagInfo.only_in_indep_count),
    ",\"hyp1_f_inverse_matches\":", String(diagInfo.hyp1_f_inverse_matches),
    ",\"hyp2_m_complement_matches\":", String(diagInfo.hyp2_m_complement_matches),
    ",\"hyp3_m_complement_minus1_matches\":", String(diagInfo.hyp3_m_complement_minus1_matches), "}");;
fi;

witnessJson := "";;
if witnessInfo.kind = "abelian" then
  witnessJson := Concatenation("{\"kind\":\"abelian\",\"pairs_scanned\":", String(witnessInfo.pairs_scanned),
    ",\"all_pairs_commute_direct_check\":", JB(witnessInfo.all_pairs_commute_direct_check),
    ",\"generator_count\":", String(witnessInfo.generator_count), "}");;
elif witnessInfo.kind = "nonabelian" then
  witnessJson := Concatenation("{\"kind\":\"nonabelian\",\"witness_m1\":", String(witnessInfo.witness_m1),
    ",\"witness_f1_word\":", WordToJson(witnessInfo.witness_f1_word),
    ",\"witness_m2\":", String(witnessInfo.witness_m2),
    ",\"witness_f2_word\":", WordToJson(witnessInfo.witness_f2_word), "}");;
else
  witnessJson := Concatenation("{\"kind\":\"unknown\",\"reason\":", JStr(witnessInfo.reason), "}");;
fi;

derivedSizesJson := "\"UNKNOWN\"";;
derivedStatusJson := "\"UNKNOWN\"";;
if IsBound(derivedInfo) then
  derivedSizesJson := JArr(List(derivedInfo.sizes, String));;
  derivedStatusJson := JStr(derivedInfo.status);;
fi;

FieldJson := function(v)
  if v = "UNKNOWN" or v = "N/A" or (IsString(v) and PositionSublist(v,"N/A")<>fail) then
    return JStr(String(v));
  fi;
  if IsBool(v) then return JB(v); fi;
  return String(v);
end;;

cert := Concatenation(
  "{\"schema\":\"wcp5-confirmation/v1\",",
  "\"generated_by\":{\"tool\":\"GAP 4.16.0\",\"script\":\"search/wcp5-confirmation.g\",\"date\":\"2026-07-29\"},",
  "\"window_id\":\"W-C-p5\",",
  "\"definition\":\"N5 = ker(B3 -> S3 x SL(2,F5)), search/wall-miner-v1.g Task B construction reused\",",
  "\"universe\":{",
    "\"b3_over_n5_order\":", String(Size(DP5)), ",",
    "\"pb3_over_n5_order\":", String(Size(A_N5)), ",",
    "\"pb3_over_n5_structure\":\"", StructureDescription(A_N5), "\",",
    "\"goursat_full_sl25_check\":", JB(assertGoursat), ",",
    "\"n_ord\":", String(N_ord), ",",
    "\"ord_x\":", String(ordX), ",\"ord_y\":", String(ordY), ",\"ord_c\":", String(ordC), ",",
    "\"c_in_n5\":", JB(cInN5), ",",
    "\"charming_set\":", JArr(List(charmingSet,String)), ",",
    "\"charming_set_gcd2nord_vs_gcdnord_agree\":", JB(charmingSetsAgree), ",",
    "\"a_n5_perfect\":", JB(isPerfect), ",",
    "\"xy_generate_a_n5\":", JB(genOK_A_N5),
  "},",
  "\"method_a_word_level_prepend\":{",
    "\"candidate_total\":", String(wlResult.candidate_total), ",",
    "\"candidate_total_expected\":", String(candidateTotalExpected), ",",
    "\"candidate_total_matches_expected\":", JB(candidateCountOk), ",",
    "\"h10_fail\":", String(wlResult.h10_fail), ",",
    "\"h11_fail\":", String(wlResult.h11_fail), ",",
    "\"generation_fail\":", String(wlResult.generation_fail), ",",
    "\"shadow_total\":", String(wlResult.shadow_total), ",",
    "\"shadow_sum_identity_ok\":", JB(shadowSumOk), ",",
    "\"quotient_shortcut_available_diagnostic\":", JB(wlResult.quotient_shortcut_available), ",",
    "\"shadows\":", JArr(shadowsJson),
  "},",
  "\"gtsh_group\":{",
    "\"composition_table_closure_fail_count\":", String(compRes.closureFail), ",",
    "\"order\":", FieldJson(gtshOrder), ",",
    "\"order_matches_shadow_total\":", JB(gtshGroupOk), ",",
    "\"identity_shadow_present\":", FieldJson(identityFoundOk), ",",
    "\"derived_series_sizes\":", derivedSizesJson, ",",
    "\"derived_series_status\":", derivedStatusJson, ",",
    "\"derived_length\":", FieldJson(derivedLen),
  "},",
  "\"kerchi\":{",
    "\"order\":", FieldJson(ker_chi_order), ",",
    "\"subgroup_closure_order_ok\":", FieldJson(kerChiSubgrpOrderOk), ",",
    "\"phi_2nord\":", FieldJson(phi2Nord), ",",
    "\"ta_count_equality_expected\":", FieldJson(taExpected), ",",
    "\"ta_count_equality_assert_ok\":", FieldJson(taAssertOk), ",",
    "\"abelian\":", FieldJson(ker_chi_abelian), ",",
    "\"witness\":", witnessJson,
  "},",
  "\"independent_recompute_full_hexagon\":{",
    "\"method\":\"full hexagon (3.3)/(3.4) evaluated on the 720-point B3/N5 permutation representation via BuildQTGeneral (裁定147 method), independent of Method A's reduced-hexagon (3.10)/(3.11) route\",",
    "\"candidate_total\":", String(Length(DwordsIndep)*Length(charmingSet)), ",",
    "\"h33_fail\":", String(indepH33Fail), ",",
    "\"h34_fail\":", String(indepH34Fail), ",",
    "\"generation_fail\":", String(indepGenFail), ",",
    "\"shadow_total\":", String(Length(indepShadows)), ",",
    "\"shadows\":", JArr(indepShadowsJson), ",",
    "\"shadow_set_equality_with_method_a\":", JB(shadowSetsEqual), ",",
    "\"symmetric_difference_diagnostic\":", diagJson, ",",
    "\"kerchi_order_agrees\":", FieldJson(indepKerChiOrderOk), ",",
    "\"kerchi_abelian_indep\":", FieldJson(indepKerChiAllCommute), ",",
    "\"kerchi_abelian_agrees_with_method_a\":", FieldJson(indepAbelianAgrees),
  "},",
  "\"elapsed_wall_ms\":{",
    "\"setup\":", String(t1-t0), ",",
    "\"method_a\":", String(t2-t1), ",",
    "\"composition_derived\":", String(t3-t2), ",",
    "\"independent_recompute\":", String(t4-t3), ",",
    "\"total\":", String(t5-t0),
  "},",
  "\"interpretation\":\"none -- observation record only, per commander directive (report raw, do not interpret, do not commit)\"",
  "}"
);;

WriteFile("search/certs/wcp5_confirmation_20260729.json", cert);;
Print("\nwrote search/certs/wcp5_confirmation_20260729.json\n");
Print("\nWCP5-CONFIRMATION DONE\n");
QUIT;
