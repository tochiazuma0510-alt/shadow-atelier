#############################################################################
## belyidb_match_probe_v1.g -- mathematician (Opus 5), 2026-08-29
## Machine cross-check for the BelyiDB survey (ruling 1777, option C survey):
## the public BelyiDB skeleton file 9T27-[9,9,9]-9-9-9-g4.m stores a pointed
## passport of 6 permutation triples (verbatim transcription below, Magma
## image-list format \[ im(1),...,im(9) ] -> GAP PermList).
## QUESTION: which of the 6 is simultaneously S9-conjugate to OUR marked pair
## (X4, Y4) (roof degree-9 block, drophunt_checker_producer_v2.g)?
## Also: verify the Magma triple convention sigma0*sigma1*sigmaoo = 1.
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;

S9 := SymmetricGroup(9);;
mk := PermList;;

## verbatim from BelyiDB/belyi_db/9/9T27-[9,9,9]-9-9-9-g4.m (BelyiDBPointedPassport)
T := [
 [ mk([8,3,7,1,6,2,4,9,5]), mk([9,3,4,6,8,1,2,7,5]), mk([3,4,7,8,1,9,2,6,5]) ],
 [ mk([8,3,7,1,6,2,4,9,5]), mk([9,8,1,2,3,4,6,5,7]), mk([6,7,4,9,1,8,5,3,2]) ],
 [ mk([8,3,7,1,6,2,4,9,5]), mk([5,3,6,2,8,7,1,9,4]), mk([9,3,4,6,8,1,2,7,5]) ],
 [ mk([8,3,7,1,6,2,4,9,5]), mk([6,8,1,3,4,7,2,9,5]), mk([5,1,7,6,8,9,4,3,2]) ],
 [ mk([8,3,7,1,6,2,4,9,5]), mk([7,8,5,3,1,4,9,6,2]), mk([6,8,9,1,7,3,4,5,2]) ],
 [ mk([8,3,7,1,6,2,4,9,5]), mk([6,8,9,1,7,3,4,5,2]), mk([7,1,9,5,3,8,6,4,2]) ]
];;

## convention check: product = identity? (both orders)
for i in [1..6] do
  s := T[i];
  Print("T", i, "  s0*s1*soo=1 : ", s[1]*s[2]*s[3] = (),
        "   soo*s1*s0=1 : ", s[3]*s[2]*s[1] = (), "\n");
od;

## all generate PSL(2,8) of order 504?
for i in [1..6] do
  Print("T", i, "  group order ", Size(Group(T[i][1],T[i][2])), "\n");
od;

## our marked pair -> triple (sigma0,sigma1,sigmaoo) = (X4, Y4, (X4*Y4)^-1)
ours := [ DCP2X4, DCP2Y4, (DCP2X4*DCP2Y4)^-1 ];;
Print("OURS orders ", List(ours, Order), "  group ", Size(Group(ours[1],ours[2])), "\n");
Print("OURS s0*s1*soo=1 : ", ours[1]*ours[2]*ours[3] = (), "\n");

## simultaneous conjugacy of the marked PAIR (sigma0,sigma1):
hits := [];;
for i in [1..6] do
  rep := RepresentativeAction(S9, [ours[1],ours[2]], [T[i][1],T[i][2]], OnTuples);
  if rep <> fail then Add(hits, i); Print("MATCH T", i, "  conjugator ", rep, "\n"); fi;
od;
Print("HITS ", hits, "\n");

## how do the 6 split under PGammaL-conjugacy of pairs (coarser)? count pairwise S9-conj
adj := NullMat(6,6);;
for i in [1..6] do for j in [1..6] do
  if i < j and RepresentativeAction(S9, [T[i][1],T[i][2]], [T[j][1],T[j][2]], OnTuples) <> fail then
    Print("NOTE T",i," ~S9~ T",j,"\n");
  fi;
od; od;

## class-triple type of each T (which of the three order-9 classes of PSL(2,8))
G := Group(T[1][1], T[1][2]);;
cls := ConjugacyClasses(G);;
ord9 := Filtered([1..Length(cls)], k -> Order(Representative(cls[k])) = 9);;
Print("ORDER9_CLASS_INDICES ", ord9, "\n");
whichcls := function(g, GG, cl)
  local k;
  for k in [1..Length(cl)] do
    if g in cl[k] then return k; fi;
  od; return fail;
end;;
for i in [1..6] do
  GG := Group(T[i][1], T[i][2]);;
  cli := ConjugacyClasses(GG);;
  Print("T", i, " class pattern ", List(T[i], t -> whichcls(t,GG,cli)), "\n");
od;
QUIT;
