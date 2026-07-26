# week4-e2-routeG.g
# Route G: independent second-system reconstruction of the C-layer data
# (d_theta, d_sigma, epsilon_m, q_theta, q_N) for A = gamma2/gamma6, class 5,
# using GAP's own polycyclic-group collector (FromTheLeftCollector), NOT the
# hand-written vector arithmetic used in docs/scout/hall5.mjs (route N).
#
# Normative source read (per coordinator authorization):
#   docs/week4-E2作用表_v1.md  (SS2, SS2.1, SS3, SS4, SS5, SS6, SS7, SS9)
# This script does NOT import/require hall5.mjs or any node code.
#
# Basis order (indices 1..12): w,p,q,r1,r2,r3,t1,t2,t3,t4,t5,t6
# Weights:                     2,3,3,4, 4, 4, 5, 5, 5, 5, 5, 5
#
# Only nontrivial commutators in A itself (SS2.2 of the doc):
#   [w,p] = t5   (i.e. p*w = w*p*t5^-1, derived below)
#   [w,q] = t6
# All other basis-pairs commute.

LoadPackage("polycyclic");

n := 12;;
coll := FromTheLeftCollector(n);;

# index map for readability
IW:=1;; IP:=2;; IQ:=3;; IR1:=4;; IR2:=5;; IR3:=6;;
IT1:=7;; IT2:=8;; IT3:=9;; IT4:=10;; IT5:=11;; IT6:=12;;

# Derivation of the two nontrivial conjugate-relations from the collection
# formula (2.2) H(a)H(b) = H(a+b - (a_p b_w) e_t5 - (a_q b_w) e_t6):
#   Mul(e_p,e_w): a=e_p (a_p=1), b=e_w (b_w=1) => correction -1*e_t5
#     => p*w = w*p*t5^-1  (normal form has w before p, i.e. index1 before index2)
#     => w^-1 * p * w = p * t5^-1        [[ p^w = p*t5^-1 ]]
#     => w * p * w^-1 = p * t5           [[ p^(w^-1) = p*t5 ]]
#   Mul(e_q,e_w): a=e_q (a_q=1), b=e_w (b_w=1) => correction -1*e_t6
#     => q*w = w*q*t6^-1
#     => w^-1 * q * w = q * t6^-1        [[ q^w = q*t6^-1 ]]
#     => w * q * w^-1 = q * t6           [[ q^(w^-1) = q*t6 ]]

for i in [2..n] do
  for j in [1..i-1] do
    if i = IP and j = IW then
      SetConjugate(coll, i, j, [i,1, IT5,-1]);
      SetConjugate(coll, i, -j, [i,1, IT5,1]);
    elif i = IQ and j = IW then
      SetConjugate(coll, i, j, [i,1, IT6,-1]);
      SetConjugate(coll, i, -j, [i,1, IT6,1]);
    else
      SetConjugate(coll, i, j, [i,1]);
      SetConjugate(coll, i, -j, [i,1]);
    fi;
  od;
od;

UpdatePolycyclicCollector(coll);;
Print("Collector built and updated. Running consistency check (IsConfluent)...\n");
consistent := IsConfluent(coll);;
Print("IsConfluent(coll) = ", consistent, "\n");
if consistent <> true then
  Print("FATAL: collector inconsistent -- formula (2.2) as encoded does not define a group.\n");
else

A := PcpGroupByCollectorNC(coll);;
Print("A := PcpGroupByCollectorNC(coll) built. IsPcpGroup(A)=", IsPcpGroup(A), "\n");
gensA := GeneratorsOfGroup(A);;
w:=gensA[IW];; p:=gensA[IP];; q:=gensA[IQ];;
r1:=gensA[IR1];; r2:=gensA[IR2];; r3:=gensA[IR3];;
t1:=gensA[IT1];; t2:=gensA[IT2];; t3:=gensA[IT3];; t4:=gensA[IT4];;
t5:=gensA[IT5];; t6:=gensA[IT6];;

# sanity: [w,p]=t5, [w,q]=t6, everything else commutes
Print("Comm(w,p)=t5? ", Comm(w,p)=t5, "\n");
Print("Comm(w,q)=t6? ", Comm(w,q)=t6, "\n");
Print("Comm(p,q)=1? ", Comm(p,q)=One(A), "\n");
Print("Comm(r1,r2)=1? ", Comm(r1,r2)=One(A), "\n");
Print("Comm(t1,t2)=1? ", Comm(t1,t2)=One(A), "\n");

# ---------------------------------------------------------------------
# General binomial coefficient for ANY integer m (per doc's implementation
# note 1 in Sec 7: m must be treated as a literal integer, evaluated before
# any reduction). GenBinom(m,k) = m(m-1)...(m-k+1)/k!, always an integer.
GenBinom := function(m,k)
  local num, i;
  if k < 0 then return 0; fi;
  if k = 0 then return 1; fi;
  num := 1;
  for i in [0..k-1] do
    num := num * (m-i);
  od;
  return num / Factorial(k);
end;;

# embed a 10-vector (Abar coords) into A's 12-vector convention (C-part=0)
Embed10 := function(f) return Concatenation(f, [0,0]); end;;

# s(a): canonical section / Hall-coordinate element, a a 12-vector
SVec := function(a)
  local res, i;
  res := One(A);
  for i in [1..12] do
    res := res * gensA[i]^a[i];
  od;
  return res;
end;;

# -----------------------------------------------------------------
# theta table (SS3.2 of docs/week4-E2作用表_v1.md), as literal Hall-ordered
# products of generator powers (this literally reconstructs the table's
# "Hall 座標" column via genuine group multiplication in the PcpGroup).
ThetaImg := [
  w^-1,                       # theta(w)
  q^-1 * t6^-1,                # theta(p)
  p^-1 * t5^-1,                # theta(q)
  r3^-1,                       # theta(r1)
  r2^-1 * t5^-1 * t6^-1,       # theta(r2)
  r1^-1,                       # theta(r3)
  t4^-1,                       # theta(t1)
  t3^-1 * t6^-1,                # theta(t2)
  t2^-1 * t5^-1,                # theta(t3)
  t1^-1,                       # theta(t4)
  t6,                          # theta(t5)
  t5                           # theta(t6)
];;

ThetaFull := function(a)
  local res, i;
  res := One(A);
  for i in [1..12] do
    res := res * ThetaImg[i]^a[i];
  od;
  return res;
end;;

# -----------------------------------------------------------------
# sigma_m table (SS4.3), built as functions of the integer m.
SigmaImg := function(m)
  local b2, b3, res;
  b2 := GenBinom(m,2);
  b3 := GenBinom(m,3);
  res := [];
  res[IW]  := w * p^-1 * q^m * r1 * r2^(-m) * r3^b2 * t1^-1 * t2^m * t3^(-b2) * t4^b3;
  res[IP]  := q * r2^-1 * r3^m * t2 * t3^(-m) * t4^b2;
  res[IQ]  := p^-1 * q^-1 * r1^2 * r2^(2-m) * r3^(1-m) * t1^-3 * t2^(2*m-3) * t3^(2*m-2-b2) * t4^(m-1-b2) * t5^-1;
  res[IR1] := r3 * t3^-1 * t4^m;
  res[IR2] := r2^-1 * r3^-1 * t2^2 * t3^(2-m) * t4^(1-m) * t5;
  res[IR3] := r1 * r2^2 * r3 * t1^-3 * t2^(m-6) * t3^(2*m-5) * t4^(m-2) * t5^-3 * t6^-1;
  res[IT1] := t4;
  res[IT2] := t3^-1 * t4^-1 * t6^-1;
  res[IT3] := t2 * t3^2 * t4 * t5 * t6;
  res[IT4] := t1^-1 * t2^-3 * t3^-3 * t4^-1 * t5^-2 * t6^-1;
  res[IT5] := t6;
  res[IT6] := t5^-1 * t6^-1;
  return res;
end;;

SigmaFull := function(a, m)
  local img, res, i;
  img := SigmaImg(m);
  res := One(A);
  for i in [1..12] do
    res := res * img[i]^a[i];
  od;
  return res;
end;;

# E_m element (SS5.1 Abar closed form + SS5.2 epsilon_m closed form)
EmVec := function(m)
  local a;
  a := [];
  a[IW]  := -GenBinom(m+1,2);
  a[IP]  :=  GenBinom(m+2,3);
  a[IQ]  := -GenBinom(m+1,3);
  a[IR1] := -GenBinom(m+3,4);
  a[IR2] :=  GenBinom(m+2,4);
  a[IR3] := -GenBinom(m+1,4);
  a[IT1] :=  GenBinom(m+4,5);
  a[IT2] := -GenBinom(m+3,5);
  a[IT3] :=  GenBinom(m+2,5);
  a[IT4] := -GenBinom(m+1,5);
  a[IT5] := GenBinom(m,1)+7*GenBinom(m,2)+17*GenBinom(m,3)+17*GenBinom(m,4)+6*GenBinom(m,5);
  a[IT6] := -(GenBinom(m,2)+4*GenBinom(m,3)+6*GenBinom(m,4)+3*GenBinom(m,5));
  return a;
end;;

EmElt := function(m) return SVec(EmVec(m)); end;;

# -----------------------------------------------------------------
# Self-checks against docs/week4-E2作用表_v1.md's own numeric tables
# (independent GAP-side reproduction; this is route G's structural test).

Print("\n=== theta^2 = id check (12 generators) ===\n");

# helper: apply ThetaFull to an *element* g of A (not just a raw vector),
# by first reading off g's own Hall-coordinate exponent vector.
ThetaOfElt := function(g) return ThetaFull(Exponents(g)); end;;
SigmaOfElt := function(g,m) return SigmaFull(Exponents(g), m); end;;

thetaSqOk := true;;
for i in [1..12] do
  if ThetaOfElt(ThetaImg[i]) <> gensA[i] then
    thetaSqOk := false;
    Print("theta^2 FAIL at generator ", i, "\n");
  fi;
od;
Print("theta^2 = id on all 12 generators? ", thetaSqOk, "\n");

Print("\n=== E_m numeric table cross-check (SS5.3, m=0..6) ===\n");
emTable := [
  [0,0,0,0,0,0,0,0,0,0,0,0],
  [-1,1,0,-1,0,0,1,0,0,0,1,0],
  [-3,4,-1,-5,1,0,6,-1,0,0,9,-1],
  [-6,10,-4,-15,5,-1,21,-6,1,0,41,-7],
  [-10,20,-10,-35,15,-5,56,-21,6,-1,131,-28],
  [-15,35,-20,-70,35,-15,126,-56,21,-6,336,-83],
  [-21,56,-35,-126,70,-35,252,-126,56,-21,742,-203]
];;
emOk := true;;
for m in [0..6] do
  computed := EmVec(m);
  expected := emTable[m+1];
  if computed <> expected then
    emOk := false;
    Print("E_m FAIL at m=", m, ": computed=", computed, " expected=", expected, "\n");
  fi;
od;
Print("E_m closed-form matches SS5.3 table for m=0..6? ", emOk, "\n");

Print("\n=== q_theta closed form (6.6) cross-check via GENUINE GROUP PRODUCT ===\n");
# q_theta(f) := C-part (Exponents at IT5,IT6) of theta(s(f)) * s(f), for f a 10-vector.
QThetaDirect := function(f)
  local a, elt, ex;
  a := Embed10(f);
  elt := ThetaFull(a) * SVec(a);
  ex := Exponents(elt);
  return [ ex[IT5], ex[IT6] ];
end;;

QThetaClosedForm := function(f)
  # f = [fw,fp,fq,fr1,fr2,fr3,ft1,ft2,ft3,ft4]
  local fw,fp,fq,fr2,ft2,ft3;
  fw:=f[1]; fp:=f[2]; fq:=f[3]; fr2:=f[5]; ft2:=f[8]; ft3:=f[9];
  return [ fw*fq - fq - fr2 - ft3, fw*fp - fp - fr2 - ft2 ];
end;;

qThetaOk := true;;
testVecs := [
  [1,0,0,0,0,0,0,0,0,0],
  [0,1,0,0,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0,0,0],
  [2,-1,3,0,1,0,0,-2,1,0],
  [-3,2,1,4,-2,0,1,0,-1,2],
  [1,1,1,1,1,1,1,1,1,1],
  [5,-3,2,0,0,-1,2,3,-4,1],
  [0,0,0,0,0,0,0,0,0,1],
  [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
  [3,0,-2,1,5,-1,0,2,0,-3]
];;
for f in testVecs do
  d := QThetaDirect(f);
  c := QThetaClosedForm(f);
  if d <> c then
    qThetaOk := false;
    Print("q_theta MISMATCH at f=", f, ": direct(group product)=", d, " closed-form(6.6)=", c, "\n");
  fi;
od;
Print("q_theta: group-product (route G) matches closed form (6.6) on all ", Length(testVecs), " test vectors? ", qThetaOk, "\n");

Print("\n=== q_N via genuine group product, cross-check against (6.7) ===\n");
# q_N(f) := C-part of E_m * sigma^2(s(f)) * sigma(s(f)) * s(f)
QNDirect := function(f, m)
  local a, elt, ex;
  a := Embed10(f);
  elt := EmElt(m) * SigmaOfElt(SigmaOfElt(SVec(a),m),m) * SigmaOfElt(SVec(a),m) * SVec(a);
  ex := Exponents(elt);
  return [ ex[IT5], ex[IT6] ];
end;;

# Abar-level sigma-bar (10x10), needed for (6.7)'s S,S^2 f-bar vectors and c_s.
SigmaBarOfVec := function(fbar, m)
  return List(Exponents(SigmaFull(Embed10(fbar), m)){[1..10]});
end;;

CsVec := function(u,v) # c_s(ubar,vbar) per (2.5): (-u_p v_w, -u_q v_w)
  return [ -u[2]*v[1], -u[3]*v[1] ];
end;;

DThetaVec := function(f) # (6.3)
  local fw,fp,fq,fr2,ft2,ft3;
  fw:=f[1];fp:=f[2];fq:=f[3];fr2:=f[5];ft2:=f[8];ft3:=f[9];
  return [ -(fq+fr2+ft3), -(fp+fr2+ft2) ];
end;;

DSigmaVec := function(f) # (6.4)
  local fw,fq,fr2,fr3,ft2,ft3,ft4,b2;
  fw:=f[1];fq:=f[3];fr2:=f[5];fr3:=f[6];ft2:=f[8];ft3:=f[9];ft4:=f[10];
  b2 := GenBinom(fw,2); # (a_w choose 2), integer for all integer a_w
  return [ -fq + fr2 - 3*fr3 + ft3 - 2*ft4 + b2, -fr3 - ft2 + ft3 - ft4 - m*b2 ];
end;;

SigmaBarOnC := function(z) return [ -z[2], z[1]-z[2] ]; end;; # sigma|_C matrix (0,-1;1,-1)

DSigma2Vec := function(f, m) # (6.5): d_{sigma^2}(f) = d_sigma(sigma_bar f) + sigma|_C(d_sigma(f))
  local sf;
  sf := SigmaBarOfVec(f, m);
  return DSigmaVec(sf) + SigmaBarOnC(DSigmaVec(f));
end;;

EpsilonVec := function(m)
  return [ GenBinom(m,1)+7*GenBinom(m,2)+17*GenBinom(m,3)+17*GenBinom(m,4)+6*GenBinom(m,5),
          -(GenBinom(m,2)+4*GenBinom(m,3)+6*GenBinom(m,4)+3*GenBinom(m,5)) ];
end;;

QNClosedForm := function(f, m) # (6.7)
  local ebar, Sf, S2f, eps, dS2, dS, c1, c2, c3;
  ebar := EmVec(m){[1..10]};
  Sf := SigmaBarOfVec(f, m);
  S2f := SigmaBarOfVec(Sf, m);
  eps := EpsilonVec(m);
  dS2 := DSigma2Vec(f, m);
  dS := DSigmaVec(f);
  c1 := CsVec(ebar, S2f);
  c2 := CsVec(ebar+S2f, Sf);
  c3 := CsVec(ebar+S2f+Sf, f);
  return eps + dS2 + dS + c1 + c2 + c3;
end;;

qNOk := true;;
mTestVals := [0,1,2,3,5,7];;
for m in mTestVals do
  for f in testVecs do
    d := QNDirect(f, m);
    c := QNClosedForm(f, m);
    if d <> c then
      qNOk := false;
      Print("q_N MISMATCH at m=",m," f=", f, ": direct(group product)=", d, " closed-form(6.7)=", c, "\n");
    fi;
  od;
od;
Print("q_N: group-product (route G) matches closed form (6.7) for m in ", mTestVals, " x ", Length(testVecs), " test vectors? ", qNOk, "\n");

Print("\n=== theta, sigma_m preserve the defining relations [w,p]=t5,[w,q]=t6 ===\n");
homOk := true;;
if ThetaOfElt(t5) <> Comm(ThetaImg[IW],ThetaImg[IP]) then homOk:=false; Print("theta hom-check FAIL (w,p)\n"); fi;
if ThetaOfElt(t6) <> Comm(ThetaImg[IW],ThetaImg[IQ]) then homOk:=false; Print("theta hom-check FAIL (w,q)\n"); fi;
for m in [0,1,2,3,5,7,-2] do
  simg := SigmaImg(m);
  if SigmaOfElt(t5,m) <> Comm(simg[IW],simg[IP]) then homOk:=false; Print("sigma hom-check FAIL (w,p) m=",m,"\n"); fi;
  if SigmaOfElt(t6,m) <> Comm(simg[IW],simg[IQ]) then homOk:=false; Print("sigma hom-check FAIL (w,q) m=",m,"\n"); fi;
od;
Print("theta, sigma_m (m in {0,1,2,3,5,7,-2}) preserve [w,p]=t5,[w,q]=t6 (i.e. are genuine endomorphisms of A consistent with the collector)? ", homOk, "\n");

Print("\n=== SUMMARY ===\n");
Print("IsConfluent(coll)=", consistent, "\n");
Print("theta^2=id: ", thetaSqOk, "\n");
Print("E_m table match (m=0..6): ", emOk, "\n");
Print("q_theta (6.6) route-G match: ", qThetaOk, "\n");
Print("q_N (6.7) route-G match: ", qNOk, "\n");
Print("theta/sigma hom-check: ", homOk, "\n");

fi;
