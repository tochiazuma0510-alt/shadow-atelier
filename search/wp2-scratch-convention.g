n := 5;;
r := PermList(Concatenation([2..n], [1]));;
s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));;

tr := function(p, i)
  local l, j;
  l := List([1..3*n], k -> k);
  for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
  return PermList(l);
end;;

x := tr(r,1) * tr(s,2) * tr(s,3);;
y := tr(s*r,1) * tr(r,2) * tr(s*r,3);;

# z fixture directly from paper: zbar = (r^2 s, r^-1 s, r)  [2405 (3.6)]
# each abstract "AB" (apply B first, then A) is GAP-encoded as B*A (established rs=s*r convention)
# so abstract r^2 s  -> GAP s*r^2 ; abstract r^-1 s -> GAP s*r^-1
zdirect := tr(s*r^2,1) * tr(s*r^-1,2) * tr(r,3);;
zdirect_naive := tr(r^2*s,1) * tr(r^-1*s,2) * tr(r,3);;
Print("zdirect_naive (r^2*s literal, no reversal) matches zA: ", zdirect_naive = (x*y)^-1, "\n");
Print("zdirect_naive (r^2*s literal, no reversal) matches zB: ", zdirect_naive = (y*x)^-1, "\n");

zA := (x*y)^-1;;   # GAP order as written
zB := (y*x)^-1;;   # reversed order

Print("zdirect = zA (x*y)^-1 straightforward: ", zdirect = zA, "\n");
Print("zdirect = zB (y*x)^-1 reversed       : ", zdirect = zB, "\n");

# second independent fixture: psi_n(xy) = (r^2 s, r^-1 s, r^-1)  [2405, Thm 5.2 proof, line ~1301]
xy_direct := tr(s*r^2,1) * tr(s*r^-1,2) * tr(r^-1,3);;
Print("psi_n(xy) fixture matches GAP y*x (abstract xy = GAP y*x): ", xy_direct = y*x, "\n");
Print("psi_n(xy) fixture matches GAP x*y (naive, no reversal)   : ", xy_direct = x*y, "\n");

QUIT;
