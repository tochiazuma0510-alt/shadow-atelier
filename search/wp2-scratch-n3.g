# Scratch end-to-end test for n=3: build Gn, reduced hexagon enumeration via (3.10)(3.11),
# full hexagon double-check on Q x T model, compare total count to Thm 4.3/4.6 (|GT(K3)|=12).
SizeScreen([4096,0]);;

MakeDn := function(n)
  local r, s;
  r := PermList(Concatenation([2..n], [1]));
  s := PermList(List([1..n], j -> ((n - (j-1)) mod n) + 1));
  return [r, s];
end;;

MakeGn := function(n)
  local rs, r, s, x, y, tr;
  rs := MakeDn(n);  r := rs[1];  s := rs[2];
  tr := function(p, i)
    local l, j;
    l := List([1..3*n], k -> k);
    for j in [1..n] do l[j + (i-1)*n] := (j^p) + (i-1)*n; od;
    return PermList(l);
  end;
  x := tr(r,1) * tr(s,2) * tr(s,3);
  y := tr(s*r,1) * tr(r,2) * tr(s*r,3);
  return rec(x := x, y := y, G := Group(x, y));
end;;

# AbstractProd: fold a list [f1,f2,...,fk] (ABSTRACT order, e.g. representing product f1*f2*...*fk
# in the *paper's* group-multiplication sense) into the correct GAP permutation, using the
# established reversal rule (abstract AB = GAP B*A), validated via z-fixture and psi_n(xy)-fixture.
AbstractProd := function(list)
  local val, i;
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do
    val := val * list[i];
  od;
  return val;
end;;

n := 3;;
gn := MakeGn(n);;
Print("|G_3| = ", Size(gn.G), " (expect 108)\n");

# z = (xy)^-1
z := AbstractProd([gn.x, gn.y])^-1;;

thetaHom := GroupHomomorphismByImages(gn.G, gn.G, [gn.x, gn.y], [gn.y, gn.x]);;
tauHom := GroupHomomorphismByImages(gn.G, gn.G, [gn.x, gn.y], [gn.y, z]);;
Print("thetaHom well-defined & bijective: ", thetaHom<>fail and IsBijective(thetaHom), "\n");
Print("tauHom well-defined & bijective: ", tauHom<>fail and IsBijective(tauHom), "\n");
# tau should have order 3 as an automorphism
Print("tau^3 = identity automorphism: ", ForAll(GeneratorsOfGroup(gn.G), g -> Image(tauHom,Image(tauHom,Image(tauHom,g))) = g), "\n");

Nord := Lcm(Order(gn.x), Order(gn.y));;
Print("N_ord = ", Nord, " (expect lcm(3,2)=6)\n");

D := DerivedSubgroup(gn.G);;
Print("|[G3,G3]| = ", Size(D), " (Sol letter said 27)\n");

# BFS over gn.G with generators x,x^-1,y,y^-1 assigning words (symbolic, abstract L-to-R order)
# BFS extends via APPENDING a generator (abstract word * g), which per the established rule
# updates the GAP value as: new_val := g_gap * old_val  (left-multiply in GAP).
gens := [ rec(sym:=["x",1], gap:=gn.x), rec(sym:=["x",-1], gap:=gn.x^-1),
          rec(sym:=["y",1], gap:=gn.y), rec(sym:=["y",-1], gap:=gn.y^-1) ];;
wordOf := NewDictionary(Identity(gn.G), true);;
AddDictionary(wordOf, Identity(gn.G), []);;
queue := [ Identity(gn.G) ];;
qi := 1;;
while qi <= Length(queue) do
  cur := queue[qi]; qi := qi+1;
  curWord := LookupDictionary(wordOf, cur);
  for g in gens do
    nv := g.gap * cur;
    if LookupDictionary(wordOf, nv) = fail then
      AddDictionary(wordOf, nv, Concatenation(curWord, [g.sym]));
      Add(queue, nv);
    fi;
  od;
od;
Print("BFS covered ", Length(queue), " elements (expect |G3|=", Size(gn.G), ")\n");

# self-consistency: EvalWordGn via AbstractProd must reproduce the element for every found word
EvalWordGn := function(word, gnrec)
  local factors, letter;
  factors := [];
  for letter in word do
    if letter[1] = "x" then Add(factors, gnrec.x^letter[2]);
    else Add(factors, gnrec.y^letter[2]); fi;
  od;
  if Length(factors) = 0 then return Identity(gnrec.G); fi;
  return AbstractProd(factors);
end;;

consistencyFail := 0;;
for elt in queue do
  w := LookupDictionary(wordOf, elt);
  if EvalWordGn(w, gn) <> elt then consistencyFail := consistencyFail + 1; fi;
od;
Print("word/eval self-consistency failures: ", consistencyFail, " (expect 0)\n");

# ---- reduced hexagon (3.10)(3.11) + charming(unit) + surjective (Prop 3.6, F2 version) ----
Xn := Filtered([0..Nord-1], m -> Gcd(2*m+1, Nord) = 1);;
Print("\nX_n = ", Xn, " (|X_n|=", Length(Xn), ")\n");

Dwords := [];;
for elt in queue do
  if elt in D then Add(Dwords, rec(elt:=elt, word:=LookupDictionary(wordOf, elt))); fi;
od;
Print("derived-subgroup candidates: ", Length(Dwords), "\n");

rawCount := 0;; hexPass := 0;; charmPass := 0;; surjPass := 0;;
shadows := [];;
for cand in Dwords do
  f := cand.elt;
  for m in Xn do
    rawCount := rawCount + 1;
    u := 2*m+1;
    thetaf := Image(thetaHom, f);
    hex310 := AbstractProd([f, thetaf]) = Identity(gn.G);
    ymf := AbstractProd([gn.y^m, f]);
    tauymf := Image(tauHom, ymf);
    tau2ymf := Image(tauHom, tauymf);
    hex311 := AbstractProd([tau2ymf, tauymf, ymf]) = Identity(gn.G);
    if hex310 and hex311 then
      hexPass := hexPass + 1;
      # charming: f already in D (derived subgroup) by construction -> charming's f-condition holds.
      charmPass := charmPass + 1;
      # surjective (F2 version): <x^u, f^-1 y^u f> = G_n
      genA := gn.x^u;
      genB := AbstractProd([f^-1, gn.y^u, f]);
      surj := Size(Group(genA, genB)) = Size(gn.G);
      if surj then
        surjPass := surjPass + 1;
        Add(shadows, rec(m:=m, f:=f, word:=cand.word));
      fi;
    fi;
  od;
od;
Print("raw_candidates=", rawCount, "  hexagon_pass=", hexPass, "  charming_pass=", charmPass,
      "  surjective_pass=", surjPass, "\n");
Print("shadow count = ", Length(shadows), " (Thm 4.3/4.6 expects |GT(K3)|=12)\n");
Print("MATCH: ", Length(shadows) = 12, "\n");

# ---- full hexagon double-check on Q x T model (independent helper, native GAP order) ----
rs := MakeDn(n);; r := rs[1];; s := rs[2];;
Qelts := Elements(Group(r,s));;
posOf := function(v) return Position(Qelts, v); end;;
phiX := s;; phiY := s*r;; phiC := ();;   # dihedral: phi(c)=1
phiXi := phiX^-1;; phiYi := phiY^-1;;
np := Length(Qelts);;
imgS1 := [];; imgS2 := [];;
for t in [1..6] do
  for i in [1..np] do
    d := Qelts[i];
    pt := (t-1)*np + i;
    if t=1 then val:=d; tp:=2;
    elif t=2 then val:=d*phiX; tp:=1;
    elif t=3 then val:=d; tp:=5;
    elif t=4 then val:=d; tp:=6;
    elif t=5 then val:=d*phiXi*phiYi*phiC; tp:=3;
    else val:=d*phiY; tp:=4;
    fi;
    imgS1[pt] := (tp-1)*np + posOf(val);
    if t=1 then val:=d; tp:=3;
    elif t=2 then val:=d; tp:=4;
    elif t=3 then val:=d*phiY; tp:=1;
    elif t=4 then val:=d*phiYi*phiXi*phiC; tp:=2;
    elif t=5 then val:=d; tp:=6;
    else val:=d*phiX; tp:=5;
    fi;
    imgS2[pt] := (tp-1)*np + posOf(val);
  od;
od;
qs1 := PermList(imgS1);; qs2 := PermList(imgS2);;
Print("\nQ x T (n=3): braid relation: ", qs1*qs2*qs1 = qs2*qs1*qs2, "\n");
qXX := qs1^2;; qYY := qs2^2;; qCC := (qs1*qs2*qs1)^2;;
Print("|<qs1,qs2>| = ", Size(Group(qs1,qs2)), " (expect 6*108=648)\n");
Print("qCC = identity: ", qCC = (), "\n");

EvalWordQT := function(word)
  local val, letter;
  val := ();
  for letter in word do
    if letter[1]="x" then val := val * qXX^letter[2];
    else val := val * qYY^letter[2]; fi;
  od;
  return val;
end;;

dblFail := 0;;
for sh in shadows do
  m := sh.m;  u := 2*m+1;
  fhat := EvalWordQT(sh.word);
  fhatInv := fhat^-1;
  lhs33 := qs1^u * fhatInv * qs2^u * fhat;;
  rhs33 := fhatInv * qs1*qs2 * qXX^(-m) * qCC^m;;
  lhs34 := fhatInv * qs2^u * fhat * qs1^u;;
  rhs34 := qs2*qs1 * qYY^(-m) * qCC^m * fhat;;
  ok := (lhs33=rhs33) and (lhs34=rhs34);
  if not ok then dblFail := dblFail + 1; Print("DOUBLE-CHECK FAIL at m=",m,"\n"); fi;
od;
Print("full-hexagon double-check failures: ", dblFail, " / ", Length(shadows), "\n");

# ---- kernel_cert per Lemma 4.2 (4.11), confirmed form (addendum 1):
#      xbar^{2m+1} = h.xbar.h^-1  and  g^-1.ybar^{2m+1}.g = h.ybar.h^-1  (componentwise in S_n)
#      g = f_triple = (g1,g2,g3) = (r^{2k}, r^{-2k}, r^{kappa(m)}), b=(j->(2m+1)j), h1=r^{-2k-m}b, h2=b,
#      h3 = b (m even) / bs (m odd)
kappa := function(m) if m mod 2 = 1 then return m+1; else return -m; fi; end;;

# component extraction: block i occupies points (i-1)*n+1 .. i*n; restrict perm to that block
compOf := function(perm, i, nn)
  local l, j;
  l := [];
  for j in [1..nn] do
    l[j] := (perm ^ ((j+(i-1)*nn))) - (i-1)*nn;
  od;
  return PermList(l);
end;;
# (careful: perm^pt means image of point pt under perm; using ^ as point-image operator on integer points)
compOfFix := function(perm, i, nn)
  local l, j, img;
  l := [];
  for j in [1..nn] do
    img := (j + (i-1)*nn)^perm;
    l[j] := img - (i-1)*nn;
  od;
  return PermList(l);
end;;

bPerm := function(u, nn)  # b: j -> u*j (mod n, 1-indexed via 0-indexed shift)
  local l, j;
  l := [];
  for j in [1..nn] do
    l[j] := ((u*(j-1)) mod nn) + 1;
  od;
  return PermList(l);
end;;

kernelCertFail := 0;;
for sh in shadows do
  m := sh.m;  u := 2*m+1;  f := sh.f;
  g1 := compOfFix(f,1,n);  g2 := compOfFix(f,2,n);  g3 := compOfFix(f,3,n);
  # find k with r^(2k) = g1
  kfound := fail;
  for t in [0..n-1] do
    if r^(2*t) = g1 then kfound := t; break; fi;
  od;
  if kfound = fail then
    Print("m=",m," NO k FOUND for g1 -- Prop4.1 form violated!\n");
    kernelCertFail := kernelCertFail + 1;
    continue;
  fi;
  k := kfound;
  kap := kappa(m);
  b := bPerm(u, n);
  h1 := AbstractProd([r^(-2*k-m), b]);
  h2 := b;
  if m mod 2 = 0 then h3 := b; else h3 := AbstractProd([b, s]); fi;
  # verify g2 = r^-2k, g3 = r^kappa(m) as sanity (part of Prop 4.1 form check)
  formOK := (g2 = r^(-2*k)) and (g3 = r^kap);
  # equation 1: x_i^u = h_i x_i h_i^-1  for (x1,x2,x3)=(r,s,s)
  xcomp := [r, s, s];;
  hcomp := [h1, h2, h3];;
  eq1 := ForAll([1,2,3], i -> xcomp[i]^u = AbstractProd([hcomp[i], xcomp[i], hcomp[i]^-1]));
  # equation 2: g_i^-1 y_i^u g_i = h_i y_i h_i^-1  for (y1,y2,y3)=(r*s? ) -- y=(rs,r,rs); rs abstract = GAP s*r
  ycomp := [s*r, r, s*r];;
  gcomp := [g1, g2, g3];;
  eq2 := ForAll([1,2,3], i -> AbstractProd([gcomp[i]^-1, ycomp[i]^u, gcomp[i]]) = AbstractProd([hcomp[i], ycomp[i], hcomp[i]^-1]));
  if not (formOK and eq1 and eq2) then
    Print("m=",m," kernel_cert FAIL: formOK=",formOK," eq1=",eq1," eq2=",eq2,"\n");
    kernelCertFail := kernelCertFail + 1;
  fi;
od;
Print("kernel_cert (4.11) failures: ", kernelCertFail, " / ", Length(shadows), "\n");

QUIT;
