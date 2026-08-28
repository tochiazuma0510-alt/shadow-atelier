# gate v2: repair of the canary hole flagged in ruling 1750 D-13.
# v1 (math_thm43_k_v1.g) only swept kappa in {0,2,4,6,8} (assumed "kappa always even"
# as an INTEGER, and tested only even residues). D-13: kappa IS even as an integer,
# but reduction mod 9 is NOT parity-invariant (9 is odd), so real data can and does
# realize ODD residues kappa mod 9 in {1,3,7} that v1 never tested.
# This script (a) derives the REAL set of m-values occurring in the 972-row artifact,
# (b) computes kappa(m) for each via the Thm 4.3 formula, (c) reduces mod 9,
# (d) confirms {1,3,7} DO occur among real kappa mod 9 residues,
# (e) re-runs the full identity check for ALL real residues (not just the even ones).
LogTo();
n := 9;;
D := DihedralGroup(IsPermGroup, 2*n);;
r := First(Elements(D), g -> Order(g) = n);;
s := First(Elements(D), g -> Order(g) = 2 and not g in Group(r));;
Print("D_", n, " order=", Size(D), "  ord(r)=", Order(r), "  ord(s)=", Order(s), "\n");
Print("s*r*s^-1 = r^-1 ? ", s*r*s^-1 = r^-1, "\n");
T := DirectProduct(D,D,D);;
e := List([1..3], i -> Embedding(T,i));;
tri := function(a,b,c) return Image(e[1],a)*Image(e[2],b)*Image(e[3],c); end;;
px := tri(r,s,s);;  py := tri(r*s,r,r*s);;  pz := (px*py)^-1;;
G := Subgroup(T,[px,py]);;
Print("|G_9| = ", Size(G), "   expect 4n^3 = ", 4*n^3, " -> ", Size(G)=4*n^3, "\n");

# --- real m-values from the 972-row artifact (independently re-read here, GAP-side) ---
if LoadPackage("json") <> true then Error("json package unavailable"); fi;
art := JsonStringToGap(StringFile("search/certs/d972_b4_word_key_artifact_v1_20260816.json"));;
rows := art.rows;;
mVals := Set(List(rows, row -> row[2][1]));;
Print("real m values occurring in the 972-row artifact: ", mVals, "\n");

kappaOf := function(m)
  if m mod 2 = 1 then return m+1; else return -m; fi;
end;;

kappaRealInt := Set(List(mVals, kappaOf));;
Print("kappa(m) as INTEGERS for real m: ", kappaRealInt, "\n");
Print("all even as integers ? ", ForAll(kappaRealInt, x -> x mod 2 = 0), "\n");

kappaRealMod9 := Set(List(kappaRealInt, x -> x mod 9));;
Print("kappa(m) mod 9 (real residues actually occurring): ", kappaRealMod9, "\n");
Print("contains odd residues {1,3,7} (D-13 hole) ? ",
      (1 in kappaRealMod9) or (3 in kappaRealMod9) or (7 in kappaRealMod9), "\n");
Print("{1,3,7} subset of real residues ? ", IsSubset(kappaRealMod9,[1,3,7]), "\n");

# --- re-run the FULL identity check over the REAL residue set (odd included) ---
ok := true;;
mismatches := [];;
for k in [0..n-1] do
  for kap in kappaRealMod9 do
    f := px^(2*k) * py^(-2*k) * pz^kap;
    if f <> tri(r^(2*k), r^(-2*k), r^kap) then
      ok := false;
      Add(mismatches, [k,kap]);
    fi;
  od;
od;
Print("psi(x^{2k} y^{-2k} z^{kappa}) = (r^{2k}, r^{-2k}, r^{kappa}) for all k in [0..8], ",
      "kappa in REAL residues ", kappaRealMod9, " : ", ok, "\n");
if not ok then Print("MISMATCHES: ", mismatches, "\n"); fi;

# for completeness also confirm the full [0..8] sweep (superset of real + previously-tested)
okFull := true;;
for k in [0..n-1] do
  for kap in [0..n-1] do
    f := px^(2*k) * py^(-2*k) * pz^kap;
    if f <> tri(r^(2*k), r^(-2*k), r^kap) then okFull := false; fi;
  od;
od;
Print("identity holds for ALL kappa in [0..8] (full residue sweep, superset check) : ", okFull, "\n");

Print("2 invertible mod 9 ? ", GcdInt(2,9)=1, "   2^-1 mod 9 = ", 1/2 mod 9, "\n");
Print("DONE\n");
QUIT;
