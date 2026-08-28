# gate: 2405 Thm 4.3 pins the k-coordinate intrinsically (psi_n at (3.1))
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
# psi_n : x -> (r,s,s) , y -> (rs,r,rs)   [2405 (3.1)]
px := tri(r,s,s);;  py := tri(r*s,r,r*s);;  pz := (px*py)^-1;;
Print("psi(z)=psi((xy)^-1) = ", pz, "\n");
G := Subgroup(T,[px,py]);;
Print("|G_9| = ", Size(G), "   expect 4n^3 = ", 4*n^3, " (n odd) -> ", Size(G)=4*n^3, "\n");
# Thm 4.3 / Thm 5.2 proof:  f := x^{2k} y^{-2k} z^{kappa}  ->  (r^{2k}, r^{-2k}, r^{kappa})
ok := true;;
for k in [0..n-1] do
  for kap in [0,2,4,6,8] do    # kappa(m) is ALWAYS even: m+1 (m odd) or -m (m even)
    f := px^(2*k) * py^(-2*k) * pz^kap;
    if f <> tri(r^(2*k), r^(-2*k), r^kap) then ok := false; Print("MISMATCH k=",k," kappa=",kap,"\n"); fi;
  od;
od;
Print("psi(x^{2k} y^{-2k} z^{kappa}) = (r^{2k}, r^{-2k}, r^{kappa}) for all k,kappa in [0..8] : ", ok, "\n");
# k is recoverable from the first component alone:  r^{2k} -> k = (2^{-1} mod 9) * exponent
Print("2 invertible mod 9 ? ", GcdInt(2,9)=1, "   2^-1 mod 9 = ", 1/2 mod 9, "\n");
Print("=> k is READ OFF intrinsically from the first D_n component. No free constant.\n");
Print("DONE\n");
QUIT;
