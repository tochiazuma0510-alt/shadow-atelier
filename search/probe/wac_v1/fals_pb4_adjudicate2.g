#############################################################################
## falsifier adjudication, part 2: identity of the two Q_P objects
#############################################################################
n := 5;; tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;; b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; Eg := Group(aE,bE);;
xb := s1^2;; yb := s2^2;;

Print("### A. the gate note's premise 'c = (s1 s2)^3 has order 5 in E' ###\n");
Print("  s1*s2 = ",String(s1*s2),"   ord(s1*s2) = ",Order(s1*s2),"\n");
Print("  (s1*s2)^3 = ",String((s1*s2)^3),"   ord = ",Order((s1*s2)^3),"\n");
Print("  (s1*s2)^3 = One(E) ?  ",(s1*s2)^3 = One(Eg),"\n");
Print("  ord(xb)=",Order(xb),"  ord(yb)=",Order(yb),
      "   Nord = Lcm(5,5,ord(c)) = ",Lcm(Order(xb),Order(yb),Order((s1*s2)^3)),"\n");
Print("  => c lies in ker(pi), so 'c |-> 1' is FORCED, not a probe choice.\n");

t := s1;; sig := [s1,s2,t];;
PiX := function(i,j) local w,k; w:=sig[i]^2;
  for k in [i+1..j-1] do w:=sig[k]*w*sig[k]^-1; od; return w; end;;
RhoX := function(i,j) local w,k; w:=sig[i]^2;
  for k in [i+1..j-1] do w:=sig[k]^-1*w*sig[k]; od; return w; end;;

D5 := DirectProduct(Eg,Eg,Eg,Eg,Eg);;
emb := List([1..5], i -> Embedding(D5,i));;
Pk := function(l) return Product(List([1..5],i->Image(emb[i],l[i]))); end;;

Gens := function(G, ord)
  local mul, tri, C;
  if ord="rev" then mul:=function(u,v) return v*u; end;
               else mul:=function(u,v) return u*v; end; fi;
  tri := [ [ G.x12, G.x23, G.x13 ],
           [ G.x23, G.x34, G.x24 ],
           [ mul(G.x13,G.x23), G.x34, mul(G.x14,G.x24) ],
           [ mul(G.x12,G.x13), mul(G.x24,G.x34), G.x14 ],
           [ G.x12, mul(G.x23,G.x24), mul(G.x13,G.x14) ] ];
  C := List([1..5], i -> mul(mul(tri[i][1],tri[i][3]),tri[i][2]));
  return [ Pk(List([1..5],i->tri[i][1])),
           Pk(List([1..5],i->tri[i][2])),
           Pk(C) ];
end;;

Gprobe := rec(x12:=xb,x23:=yb,x13:=yb^-1*xb^-1,
              x14:=s1^-1*(yb^-1*xb^-1)*s1,x24:=s1^-1*yb*s1,x34:=xb);;
Gpi    := rec(x12:=PiX(1,2),x23:=PiX(2,3),x13:=PiX(1,3),
              x14:=PiX(1,4),x24:=PiX(2,4),x34:=PiX(3,4));;

gp := Gens(Gprobe,"rev");;   ## the probe's object
gc := Gens(Gpi,"fwd");;      ## the honest canonical object
Qp := Group(gp);;  Qc := Group(gc);;

Print("\n### B. are the two Q_P the SAME subgroup of E^5 ? ###\n");
Print("  |Q_probe| = ",Size(Qp),"   |Q_canon| = ",Size(Qc),"\n");
Print("  Q_probe = Q_canon (as subgroups of E^5) ?  ",Qp = Qc,"\n");
Print("  IsConjugate in E^5 ? ",IsConjugate(D5,Qp,Qc),"\n");

Print("\n### C. is the generator-labelled correspondence an isomorphism ? ###\n");
Print("  Psi_probe(x12) = ",String(gp[1]),"\n");
Print("  Psi_canon(x12) = ",String(gc[1]),"\n");
Print("  equal componentwise ? ",gp[1]=gc[1],"\n");
Print("  Psi_probe(x23) = Psi_canon(x23) ? ",gp[2]=gc[2],"\n");
Print("  Psi_probe(c)   = Psi_canon(c)   ? ",gp[3]=gc[3],"\n");
h := GroupHomomorphismByImages(Qp,Qc,gp,gc);;
if h = fail then
  Print("  x|->x, y|->y, c|->c is NOT a homomorphism Q_probe -> Q_canon\n");
else
  Print("  x|->x, y|->y, c|->c IS a homomorphism; bijective ? ",
        IsBijective(h),"   |ker| = ",Size(Kernel(h)),"\n");
fi;
## the opposite (anti) correspondence
h2 := GroupHomomorphismByImages(Qp,Qc,gp,[gc[1]^-1,gc[2]^-1,gc[3]^-1]);;
Print("  anti-correspondence (g |-> g^-1 on gens) is a hom ? ",h2 <> fail,"\n");

Print("\n### D. does the coface family commute with letter reversal ? ###\n");
## check  Psi_probe_i(g) = pi(Rev(phi_i(g)))  is the SAME as  pi(phi_i(Rev g))
## numerically: compare the i-th components of gp and of the 'canon then rev' build
grev := Gens(rec(x12:=RhoX(1,2),x23:=RhoX(2,3),x13:=RhoX(1,3),
                 x14:=RhoX(1,4),x24:=RhoX(2,4),x34:=RhoX(3,4)),"rev");;
Print("  probe window/rev  ==  rho window/rev  (all 3 gens) ? ",
      gp[1]=grev[1] and gp[2]=grev[2] and gp[3]=grev[3],"\n");

Print("\n### E. discrimination: is |Q_P| = 7500 generic ? ###\n");
## sweep x13 over all of E (keeping x14 := t^-1 x13 t, rest = rho) and
## record the distribution of |Q_P|.  If 7500 is rare, the test has teeth.
tab := [];;
for z in AsList(Eg) do
  gz := Gens(rec(x12:=RhoX(1,2),x23:=RhoX(2,3),x13:=z,
                 x14:=t^-1*z*t,x24:=RhoX(2,4),x34:=RhoX(3,4)),"rev");
  Add(tab, Size(Group(gz)));
od;
Print("  |E| = ",Size(Eg)," choices of x13; distribution of |Q_P|:\n");
for v in Set(tab) do
  Print("     |Q_P| = ",v,"  count = ",Number(tab,z->z=v),"\n");
od;
Print("  #{x13 giving 7500} = ",Number(tab,z->z=7500),
      "   (probe & rho value included ? ",
      Size(Group(Gens(rec(x12:=RhoX(1,2),x23:=RhoX(2,3),x13:=RhoX(1,3),
        x14:=t^-1*RhoX(1,3)*t,x24:=RhoX(2,4),x34:=RhoX(3,4)),"rev")))=7500,")\n");

Print("\n### F. the mixed variant (forward gens + reverse rows) is ill-formed ###\n");
mul := function(u,v) return v*u; end;;
G := Gpi;;
tri := [ [ G.x12, G.x23, G.x13 ],
         [ G.x23, G.x34, G.x24 ],
         [ mul(G.x13,G.x23), G.x34, mul(G.x14,G.x24) ],
         [ mul(G.x12,G.x13), mul(G.x24,G.x34), G.x14 ],
         [ G.x12, mul(G.x23,G.x24), mul(G.x13,G.x14) ] ];;
for i in [1..5] do
  Print("   cpt ",i,":  c1 := x12*x13*x23-image = ",
    String(mul(mul(tri[i][1],tri[i][3]),tri[i][2])),
    "   c2 := x23*x12*x13-image = ",
    String(mul(mul(tri[i][2],tri[i][1]),tri[i][3])),
    "   agree ? ",mul(mul(tri[i][1],tri[i][3]),tri[i][2])
                 = mul(mul(tri[i][2],tri[i][1]),tri[i][3]),"\n");
od;
Print("   (A.5) demands both words equal c; disagreement => not a map out of PB3.\n");

Print("\n== DONE ==\n"); QUIT;
