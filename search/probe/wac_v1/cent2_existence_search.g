#############################################################################
## search/probe/wac_v1/cent2_existence_search.g
## n=12 realization-pair existence search (裁定240 工程1).  Search for
## pairs (a1,b1) in S12 with:
##   a1^2 = 1, cycle type (2,2,2,2,2,1,1)  [k=5 transpositions, 2 fixed points]
##   b1^3 = 1, cycle type (3,3,3,3)        [j=4 3-cycles, 0 fixed points]
##   w := b1^-1 * a1  has cycle type (5,5,2)
## and MEASURE (not assert) sign(a1); the generation target to check is
## <a1,b1> = S12 (order 12! = 479001600) -- checked, not assumed.
##
## Method (mirrors search/probe/wac_v1/cent1_existence_search.g): fix a
## single representative w0 of the target w-type (5,5,2).  Since
## w = b1^-1*a1 => b1 = a1*w0^-1, and every pair (a1,b1) with w of type
## (5,5,2) is S12-conjugate (by transitivity of S12 on the (5,5,2)
## conjugacy class) to a pair with w = w0 exactly, scanning a1 over the
## FULL conjugacy class of the target a1-type (62,370 elements) and setting
## b1 := a1*w0^-1 is exhaustive up to simultaneous conjugation -- no
## S12-conjugacy-class of realization pair is missed by this scan design.
##
## Bonus: classify hits by orbits of a1 under conjugation by C_S12(w0)
## (centralizer of w0), same as cent1.
##
## For any realization hit (gen=S12) found, also emit an LID-1-style ID
## (裁定171 convention: literal generator word -> canonical string ->
## SHA-256) -- see WACT_Sha256OfString / WACT_Lid1 below.  This is a
## display-dependent literal hash, NOT the P81-F canonical-uid (which
## needs the digraphs package's bliss labelling and is out of scope here).
##
## Single lane (GAP 4.16.0).  NOT a ledger claim.  No commit.  No sealed
## symbol.  Existence search only -- no judgement, no interpretation.
## No expected/predicted values are encoded anywhere in this script
## (contact isolation -- docs/notes/sat_l1_v1.md, r4_prediction_v1.md,
## ideas/, sol/ were NOT read while writing this script).
#############################################################################

n := 12;;
Sn := SymmetricGroup(n);;

CT := function(p) return SortedList(List(Orbits(Group(p),[1..n]), Length)); end;;

#############################################################################
## ---------------------- LID-1-style hashing (literal, not canonical-uid) --
#############################################################################
WACT_Sha256Counter := 0;;
WACT_Sha256OfString := function(s)
  local tmp, out, f, line;
  WACT_Sha256Counter := WACT_Sha256Counter + 1;
  tmp := Concatenation("search/.tmp_cent2_sha_", String(Runtime()), "_",
                        String(WACT_Sha256Counter), ".txt");
  out := Concatenation(tmp, ".sha");
  f := OutputTextFile(tmp, false);
  SetPrintFormattingStatus(f, false);
  PrintTo(f, s);
  CloseStream(f);
  Exec(Concatenation("sha256sum \"", tmp, "\" > \"", out, "\""));
  f := InputTextFile(out);
  line := ReadLine(f);
  CloseStream(f);
  Exec(Concatenation("rm -f \"", tmp, "\" \"", out, "\""));
  if line = fail or Length(line) < 64 then
    Error("cent2_existence_search.g: WACT_Sha256OfString: sha256sum did not return a hash line");
  fi;
  return line{[1 .. 64]};
end;;

## LID-1 (裁定171 convention adapted to this window family): literal
## generator word (a1,b1,w as printed permutations) -> fixed-format
## canonical string -> SHA-256.
WACT_Lid1 := function(a1, b1, w)
  local s;
  s := Concatenation("LID1/v1|family=cent2|n=", String(n),
         "|a1=", String(a1), "|b1=", String(b1), "|w=", String(w));
  return rec(canonical_string := s, sha256 := WACT_Sha256OfString(s));
end;;

Print("#########################################################\n");
Print("## STEP 0  fix target w0 (type (5,5,2)) and a1-class representative\n");
Print("#########################################################\n");

w0 := PermList([2,3,4,5,1, 7,8,9,10,6, 12,11]);;   ## (1,2,3,4,5)(6,7,8,9,10)(11,12)
a0 := (1,2)(3,4)(5,6)(7,8)(9,10);;                  ## (2,2,2,2,2,1,1); fixed pts 11,12

Print("w0       = ", w0, "\n");
Print("w0 type  = ", CT(w0), "  sign(w0) = ", SignPerm(w0), "  ord(w0) = ", Order(w0), "\n");
Print("a0       = ", a0, "\n");
Print("a0 type  = ", CT(a0), "  sign(a0) = ", SignPerm(a0), "  ord(a0) = ", Order(a0), "\n");

a1classSize := Size(ConjugacyClass(Sn, a0));;
Print("|a1-class (type (2,2,2,2,2,1,1))| = ", a1classSize, "\n");

Print("\n#########################################################\n");
Print("## STEP 1  exhaustive scan: a1 over full conjugacy class of a0,\n");
Print("##         b1 := a1*w0^-1, keep hits with b1 type (3,3,3,3)\n");
Print("#########################################################\n");

targetBType := [3,3,3,3];;
EXHAUST_THRESH := 1000000;;

t0 := Runtime();;
aClassList := AsList(ConjugacyClass(Sn, a0));;
Print("class enumerated: ", Length(aClassList), " elements  (", (Runtime()-t0)/1000.0, "s)\n");

hits := [];;
tries := 0;; bTypeHits := 0;;
t0 := Runtime();;
for a1 in aClassList do
  tries := tries + 1;
  b1 := a1 * w0^-1;
  if CT(b1) = targetBType then
    bTypeHits := bTypeHits + 1;
    Add(hits, rec(a1:=a1, b1:=b1));
  fi;
od;
Print("tries=", tries, "  b1-type=(3,3,3,3) hits=", bTypeHits,
      "  elapsed=", (Runtime()-t0)/1000.0, "s\n");

Print("\n#########################################################\n");
Print("## STEP 2  among b1-type hits, check generation <a1,b1> = S12,\n");
Print("##         and MEASURE (do not assert) sign(a1)\n");
Print("#########################################################\n");

genHits := [];;
t0 := Runtime();;
for h in hits do
  G := Group(h.a1, h.b1);
  if Size(G) = Size(Sn) and G = Sn then
    Add(genHits, rec(a1:=h.a1, b1:=h.b1, w:=h.b1^-1*h.a1, gen:="S12",
                      sizeG:=Size(G), sign_a1:=SignPerm(h.a1)));
  else
    Add(genHits, rec(a1:=h.a1, b1:=h.b1, w:=h.b1^-1*h.a1, gen:="other",
                      sizeG:=Size(G), sign_a1:=SignPerm(h.a1)));
  fi;
od;
Print("generation check done  elapsed=", (Runtime()-t0)/1000.0, "s\n");

realizationHits := Filtered(genHits, r -> r.gen = "S12");;
Print("realization pairs with <a1,b1> = S12 : ", Length(realizationHits), "\n");
Print("all genHits by category: S12=", Length(Filtered(genHits, r->r.gen="S12")),
      "  other=", Length(Filtered(genHits, r->r.gen="other")), "\n");
signDist := Collected(List(genHits, r -> r.sign_a1));;
Print("sign(a1) distribution over ALL b1-type hits (measured, not asserted) = ", signDist, "\n");
otherSizes := SortedList(DuplicateFreeList(List(Filtered(genHits, r->r.gen="other"), r->r.sizeG)));;
Print("distinct |<a1,b1>| among 'other' hits = ", otherSizes, "\n");
for sz in otherSizes do
  Print("   |<a1,b1>|=", sz, "  count=",
        Length(Filtered(genHits, r -> r.gen="other" and r.sizeG=sz)), "\n");
od;

Print("\n#########################################################\n");
Print("## STEP 3  sanity re-checks on realization hits (first up to 10)\n");
Print("#########################################################\n");
showN := Minimum(10, Length(realizationHits));;
for i in [1..showN] do
  r := realizationHits[i];
  Print("-- hit ", i, "\n");
  Print("   a1 = ", r.a1, "  type=", CT(r.a1), "  sign=", SignPerm(r.a1), "  ord=", Order(r.a1), "\n");
  Print("   b1 = ", r.b1, "  type=", CT(r.b1), "  sign=", SignPerm(r.b1), "  ord=", Order(r.b1), "\n");
  Print("   w  = b1^-1*a1 = ", r.w, "  type=", CT(r.w), "  ord=", Order(r.w), "\n");
  Print("   <a1,b1> order = ", r.sizeG, "  = S12 order? ", r.sizeG = Size(Sn), "\n");
od;

Print("\n#########################################################\n");
Print("## STEP 4  orbit classification of realization hits under\n");
Print("##         C_S12(w0)-conjugation on a1 (bonus; counts only)\n");
Print("#########################################################\n");
Cw0 := Centralizer(Sn, w0);;
Print("|C_S12(w0)| = ", Size(Cw0), "\n");
if Length(realizationHits) > 0 then
  aList := List(realizationHits, r -> r.a1);;
  orbs := Orbits(Cw0, aList, OnPoints);;
  Print("realization-hit orbit count under C_S12(w0)-conjugation on a1 = ", Length(orbs), "\n");
  for i in [1..Length(orbs)] do
    Print("   orbit ", i, ": size=", Length(orbs[i]), "\n");
  od;
else
  Print("no realization hits -- orbit classification vacuous (0 orbits)\n");
fi;

Print("\n#########################################################\n");
Print("## STEP 5  LID-1-style literal hash of realization hits (up to 5)\n");
Print("#########################################################\n");
showLid := Minimum(5, Length(realizationHits));;
for i in [1..showLid] do
  r := realizationHits[i];
  lid := WACT_Lid1(r.a1, r.b1, r.w);
  Print("-- hit ", i, " LID-1\n");
  Print("   canonical_string = ", lid.canonical_string, "\n");
  Print("   sha256           = ", lid.sha256, "\n");
od;
if showLid = 0 then
  Print("no realization hits -- LID-1 hashing vacuous\n");
fi;

Print("\n#########################################################\n");
Print("## SUMMARY\n");
Print("#########################################################\n");
Print("a1-class size (2,2,2,2,2,1,1)        = ", a1classSize, "\n");
Print("scanned (tries)                      = ", tries, "  (EXHAUSTIVE, tries=class size: ",
      tries = a1classSize, ")\n");
Print("b1-type=(3,3,3,3) hits                = ", bTypeHits, "\n");
Print("generation=S12 hits (realization)     = ", Length(realizationHits), "\n");
Print("generation=other hits                 = ", Length(Filtered(genHits, r->r.gen="other")), "\n");
Print("sign(a1) distribution (all b1-hits)   = ", signDist, "\n");
if Length(realizationHits) > 0 then
  Print("orbit count under C_S12(w0)            = ", Length(Orbits(Cw0, List(realizationHits, r->r.a1), OnPoints)), "\n");
fi;
Print("exists_realization_pair                = ", Length(realizationHits) > 0, "\n");

Print("\nCENT2_EXISTENCE_SEARCH_DONE\n");
QUIT;
