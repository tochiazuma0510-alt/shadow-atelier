#############################################################################
## ta_tb_psi_invariance_v1.g -- mathematician (Opus 5), 2026-08-30
## v1 showed: for OUR (9,9,9) target, the inverse triple AND the reversed
## triple are BOTH S9-simultaneously conjugate to the original.
## ==> the T-a/T-b ambiguity does not change WHICH COVER we need.
## But each conjugacy is realised by a UNIQUE conjugator (centraliser = 1),
## so it DOES change the LABELLING of the 9 points -- and Psi is NOT a class
## function.  DECISIVE QUESTION:
##      is the 27-value Psi table INVARIANT under those conjugators?
##   YES -> the convention is moot for the translation bit too (risk removed)
##   NO  -> the pilot's convention answer is load-bearing (risk confirmed)
## Also: how many (7,2,3) triple classes exist and how many are self-inverse-
## conjugate?  (to judge whether the G-1 finding is informative or generic)
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;
Read("scratchpad/pi_psi_table.g");;          ## PIT = [[perm, Psi], ...] 27 rows
G := Group(DCP2X4, DCP2Y4);; S9 := SymmetricGroup(9);;
TX := DCP2X4;; TY := DCP2Y4;; TZ := (TX*TY)^-1;;

cinv := RepresentativeAction(S9, [TX^-1, TY^-1], [TX, TY], OnPairs);;
crev := RepresentativeAction(S9, [TZ,    TY   ], [TX, TY], OnPairs);;
Print("PI_CINV ", cinv, "\n");
Print("PI_CREV ", crev, "\n");
Print("PI_CINV_IN_NORMALISER ", cinv in Normalizer(S9,G),
      "  PI_CREV_IN_NORMALISER ", crev in Normalizer(S9,G), "\n");
Print("PI_CINV_IN_G ", cinv in G, "  PI_CREV_IN_G ", crev in G, "\n");

T  := List(PIT, r -> r[1]);;  PS := List(PIT, r -> r[2]);;
Tset := Set(T);;
checkc := function(c, nm)
  local closed, inv, i, im, j;
  closed := true;; inv := true;;
  for i in [1..Length(T)] do
    im := T[i]^c;;
    if not (im in Tset) then closed := false;
    else
      j := Position(T, im);;
      if PS[j] <> PS[i] then inv := false; fi;
    fi;
  od;
  Print("PI_", nm, "_SET_CLOSED ", closed, "  PSI_INVARIANT ", inv and closed, "\n");
  return [closed, inv];
end;;
checkc(cinv, "CINV");;
checkc(crev, "CREV");;
## control: a random element of N_{S9}(G) outside G
N := Normalizer(S9,G);;
outs := First(Elements(N), g -> not (g in G) and Order(g) = 3);;
Print("PI_CONTROL_outer_elt_order ", Order(outs), "\n");
checkc(outs, "OUTER");;
## and a random inner one
checkc(Random(G), "INNER_RANDOM");;

## (B) how many (7,2,3) triple classes, and how many are self-inverse-conjugate?
sev := Filtered(Elements(G), g -> Order(g)=7);;
tw  := Filtered(Elements(G), g -> Order(g)=2);;
prs := [];;
for a in sev do for b in tw do
  if Order(a*b)=3 and Group(a,b)=G then Add(prs,[a,b]); fi;
od; od;
Print("\nPI_723_GENERATING_PAIRS ", Length(prs), "\n");
reps := [];;
for p in prs do
  if ForAll(reps, r -> RepresentativeAction(S9, r, p, OnPairs) = fail) then
    Add(reps, p); fi;
od;
Print("PI_723_CLASSES_UP_TO_S9 ", Length(reps), "\n");
Print("PI_723_SELF_INVERSE_CONJUGATE_PER_CLASS ",
  List(reps, r -> RepresentativeAction(S9, [r[1]^-1, r[2]^-1], r, OnPairs) <> fail), "\n");
Print("PI_DONE\n");
QUIT;
