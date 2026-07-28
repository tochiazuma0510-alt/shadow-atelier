# sgnc_check.g -- FINDING SGN-c hat: which of (i) prediction / (ii) measurement carries the sign?
# self-contained (no Read of project libs); ASCII only.
SizeScreen([4096, 0]);;

# paper word "f1 f2 ... fk" -> GAP raw product f_k * ... * f_1  (convention W-4, verbatim copy
# of search/week3-battery-common.g L47-54)
AbstractProd := function(list)
  local val, i;
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do
    val := val * list[i];
  od;
  return val;
end;;

BuildPn := function(n)
  local r, s, tr, a1, a2, a3, q1, q2, q3, X, Y, Xchk, Ychk, Gfull;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  a1 := tr(r,1);;  a2 := tr(r,2);;  a3 := tr(r,3);;
  q1 := tr(s,2) * tr(s,3);;
  q2 := tr(s,1) * tr(s,3);;
  q3 := tr(s,1) * tr(s,2);;
  X := AbstractProd([a1, q1]);;
  Y := AbstractProd([a1, a2, a3, q2]);;
  Xchk := tr(r,1) * tr(s,2) * tr(s,3);;
  Ychk := tr(s*r,1) * tr(r,2) * tr(s*r,3);;
  if X <> Xchk then Error("X mismatch n=", n); fi;
  if Y <> Ychk then Error("Y mismatch n=", n); fi;
  Gfull := Group(a1, a2, a3, q1, q2);;
  return rec(n:=n, a1:=a1, a2:=a2, a3:=a3, q1:=q1, q2:=q2, q3:=q3, X:=X, Y:=Y, G:=Gfull);
end;;

# decompose v in A = <a1,a2,a3> as exponent triple (i,j,k) with a1^i a2^j a3^k = v
# (a1,a2,a3 pairwise commute, so raw and paper order agree here)
AExp := function(v, P, n)
  local i, j, k;
  for i in [0..n-1] do for j in [0..n-1] do for k in [0..n-1] do
    if P.a1^i * P.a2^j * P.a3^k = v then return [i,j,k]; fi;
  od; od; od;
  return fail;
end;;

Print("n | rawdec(fixture: g = a^raw * q)  | paperNF(g = a .paper q) | g=paper a1*q3? | g=paper a1^-1*q3? | involution\n");
for n in [3,5,7,9,11] do
  P := BuildPn(n);;
  u := 4*n - 1;;
  g := fail;;
  for cand in Elements(P.G) do
    if P.X^cand = P.X^u and P.Y^cand = P.Y^u then g := cand; break; fi;
  od;
  if g = fail then Error("no inner conjugator n=", n); fi;

  # (A) fixture-style decomposition: raw  g * q^-1  in A, label "(i,j,k)*q"
  rawA := AExp(g * Inverse(P.q3), P, n);;
  # (B) paper normal form  g = a .paper q3  == raw  q3 * a  =>  a = raw q3^-1 * g
  papA := AExp(Inverse(P.q3) * g, P, n);;

  hPred := AbstractProd([P.a1, P.q3]);;          # paper  a1 * q3     (prediction, k=0)
  hNeg  := AbstractProd([P.a1^(n-1), P.q3]);;    # paper  a1^(n-1)*q3 (the "measured" reading)

  # independent paper-side check: inn_paper(h)(w) := h w h^-1  computed only via AbstractProd
  innP := function(h, w) return AbstractProd([h, w, h^-1]); end;;
  okPred := (innP(hPred, P.X) = P.X^u) and (innP(hPred, P.Y) = P.Y^u);;
  okNeg  := (innP(hNeg,  P.X) = P.X^u) and (innP(hNeg,  P.Y) = P.Y^u);;
  # and the opposite paper reading h^-1 w h
  innQ := function(h, w) return AbstractProd([h^-1, w, h]); end;;
  okPredOpp := (innQ(hPred, P.X) = P.X^u) and (innQ(hPred, P.Y) = P.Y^u);;

  Print(n, " | (", rawA[1], ",", rawA[2], ",", rawA[3], ")*q3 | (",
        papA[1], ",", papA[2], ",", papA[3], ").q3 | ", g = hPred, " | ", g = hNeg,
        " | g^2=1: ", g^2 = One(P.G), "\n");
  Print("    paper inn(a1 q3) realises Phi: ", okPred,
        "   |  paper inn(a1^(n-1) q3) realises Phi: ", okNeg,
        "   |  paper h^-1 X h with h=a1q3: ", okPredOpp, "\n");
  Print("    GAP-native X^g literally equals AbstractProd([g,X,g^-1]): ",
        P.X^g = AbstractProd([g, P.X, g^-1]), "\n");
od;

# ---- a NON-involutive control: m=0 family, conjugator a1^(-2k) (phifam L132) ----
Print("\n-- control: non-involutive conjugator, does native/paper distinction bite? --\n");
for n in [5, 9] do
  P := BuildPn(n);;
  for kk in [1, 2] do
    h := P.a1^(-2*kk);;                 # paper a1^(-2k) (single letter: raw = paper)
    XI := AbstractProd([h, P.X, h^-1]);;  # paper inn(h)
    XJ := AbstractProd([h^-1, P.X, h]);;  # paper inn(h^-1)
    YI := AbstractProd([h, P.Y, h^-1]);;
    YJ := AbstractProd([h^-1, P.Y, h]);;
    # brute-force the native GAP conjugator for the automorphism paper-inn(h)
    gg := fail;;
    for cand in Elements(P.G) do
      if P.X^cand = XI and P.Y^cand = YI then gg := cand; break; fi;
    od;
    Print("n=", n, " k=", kk, ": native g = h ? ", gg = h, "   native g = h^-1 ? ", gg = h^-1,
          "   (h involution? ", h^2 = One(P.G), ")\n");
  od;
od;

Print("\nSGNC-CHECK DONE\n");
QUIT;
