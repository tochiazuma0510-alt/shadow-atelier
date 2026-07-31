#############################################################################
## search/probe/wac_v1/pent_t2t3_run.g   -- (T2)(T3) fine-level run
##  構成: (2.4) に従い (K_pi)_{F2} = ∩_{i=1..5} ker(psi_i),  psi_i = 余面 phi_i を
##  pi (s3|->s1) で押して N_A で還元したもの。 Q := F2/(K_pi)_{F2} を
##  部分直積 Psi(F2) <= E^5 として実現(E = B3/N_A, |E|=360)。
##  H3 := ker(Q ->> P=A5)。 fiber = H3-coset。
##  判定は P90-PENT の 6 条件を **同一の h** で。membership は 5 余面全数。
##  接触遮断: 期待値(20/10 等)は一切判定に使わない。
##  規約: 論文語 "AB" = GAP B*A(AbstractProd 反転)。
##  Single lane (GAP 4.16.0). NOT a ledger claim.
#############################################################################
n := 5;;
tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; YY := tt*XX*tt^-1;; ss := tt*XX^3;;
b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
Print("== window ==\n a1=",a1," b1=",b1,"  P=A5? ",PN=AlternatingGroup(5),
      "  |E|=",Size(Eg),"  c=1? ",cc=(),"\n");
Nord := Lcm(Order(xb),Order(yb),Order(cc));;
charm := Filtered([0..Nord-1], z->GcdInt(2*z+1,Nord)=1);;
Print(" N_ord=",Nord,"  charming=",charm,"\n");

## ---- PB4 生成元の pi-像(論文語 -> GAP 反転)----
X12 := xb;;  X23 := yb;;
X13 := yb^-1*xb^-1;;          ## c=x12 x13 x23 (paper), c=1 => x13 = x12^-1 x23^-1
X34 := xb;;                    ## pi(s3^2)=s1^2
X24 := s1^-1*yb*s1;;           ## paper s1 x23 s1^-1
X14 := s1^-1*X13*s1;;          ## paper s1 x13 s1^-1
Print(" x13 check: paper x12 x13 x23 = GAP X23*X13*X12 = ", X23*X13*X12,
      "  (=1?) ", X23*X13*X12 = (), "\n");

## ---- 5 余面の (x12,x23,x13) 上の値(A.18)を pi で押したもの ----
## 論文の積 "AB" は GAP で B*A
cof := [ [ X12, X23, X13 ],                       ## phi_123
         [ X23, X34, X24 ],                       ## phi_234
         [ X23*X13, X34, X24*X14 ],               ## phi_12,3,4 : x12->x13 x23, x13->x14 x24
         [ X13*X12, X34*X24, X14 ],               ## phi_1,23,4 : x12->x12 x13, x23->x24 x34
         [ X12, X24*X23, X14*X13 ] ];;            ## phi_1,2,34 : x23->x23 x24, x13->x13 x14

## ---- Psi : F2 -> E^5 ----
D5 := DirectProduct(Eg,Eg,Eg,Eg,Eg);;
emb := List([1..5], i -> Embedding(D5,i));;
Pack := function(l) return Product(List([1..5], i -> Image(emb[i], l[i]))); end;;
F := FreeGroup("x","y");;
gx := GeneratorsOfGroup(F)[1];; gy := GeneratorsOfGroup(F)[2];;
PsiOf := function(w)
  return Pack(List([1..5], i -> MappedWord(w,[gx,gy],[cof[i][1],cof[i][2]])));
end;;
Q := Group(PsiOf(gx), PsiOf(gy));;
pr1 := Projection(D5,1);;
Print("\n== refined quotient ==\n |Q| = ",Size(Q),
      "   |P| = ",Size(PN),"   |H3| = ",Size(Q)/Size(PN),"\n");
H3 := Kernel(GroupHomomorphismByImages(Q, PN,
        [PsiOf(gx),PsiOf(gy)], [xb,yb]));;
Print(" |H3| = ",Size(H3),"  ",StructureDescription(H3),
      "  中心的? ",IsSubgroup(Centre(Q),H3),
      "  可換? ",IsAbelian(H3),"\n");
## c が (K_pi)_{PB3} に入るか(簡約 hexagon が使えるかの前提)
cimg := Pack(List([1..5], i -> cof[i][3]*cof[i][2]*cof[i][1]));;  ## paper x12 x13 x23
Print(" Psi(c) = 1 ? ",cimg = One(D5),"   (真なら簡約 hexagon (3.10)(3.11) が fine 水準で使える)\n");

## ---- theta, tau(F2 の自己同型・語レベル)----
th := function(w) return MappedWord(w,[gx,gy],[gy,gx]); end;;
ta := function(w) return MappedWord(w,[gx,gy],[gy,gx^-1*gy^-1]); end;;
Print(" tau^3=1 on x,y ? ", ta(ta(ta(gx)))=gx and ta(ta(ta(gy)))=gy, "\n");

## ---- GT(N_A) を原形 hexagon で列挙(接触遮断)----
Hex := function(m,f)
  local u; u := 2*m+1;
  return s1^u*f^-1*s2^u*f = f^-1*s1*s2*xb^(-m)*cc^m and
         f^-1*s2^u*f*s1^u = s2*s1*yb^(-m)*cc^m*f;
end;;
shad := [];;
for m in charm do for f in Elements(PN) do
  if Hex(m,f) and Group(xb,yb^f)=PN then Add(shad,[m,f]); fi;
od; od;
Print("\n== GT(N_A) ==  |GT| = ",Length(shad),
      "  相異なる f = ",Length(Set(List(shad,z->z[2]))),"\n");

## ---- 語の取得 ----
epiQ := GroupHomomorphismByImages(F, Q, [gx,gy], [PsiOf(gx),PsiOf(gy)]);;
WordOfQ := function(q) return PreImagesRepresentative(epiQ,q); end;;

## ---- 6 条件の同時判定 ----
Pent := function(v) return v[1]*v[4]*v[2] = v[3]*v[5]; end;;  ## paper 234,1234,123 = 1234,1234 の GAP 反転
Chk6 := function(m, q)
  local w, v, i, W, c1, c2, c3, c4, c5, sub;
  w := WordOfQ(q);
  v := List([1..5], i -> MappedWord(w,[gx,gy],[cof[i][1],cof[i][2]]));
  c3 := Pent(v);                                        ## (2.20)
  c1 := PsiOf(th(w)*w) = One(D5);                       ## (3.10) defect in (K_pi)
  W  := w*gy^m;                                         ## paper y^m f
  c2 := PsiOf(W*ta(W)*ta(ta(W))) = One(D5);             ## (3.11) defect in (K_pi)
  c4 := (q in DerivedSubgroup(Q));                      ## commutator (charming は m で保証)
  sub := Group(PsiOf(gx^(2*m+1)), q^-1*PsiOf(gy^(2*m+1))*q);
  c5 := (Size(sub) = Size(Q));                          ## refined 全射
  return [c1,c2,c3,c4,c5, c1 and c2 and c3 and c4 and c5];
end;;

Print("\n== (T2) 20 shadow の持ち上げ判定(6 条件同時)==\n");
lifted := [];; per := [];;
for m in charm do
  cnt := 0;
  for z in Filtered(shad, u->u[1]=m) do
    fib := Filtered(Elements(Q), q -> Image(pr1,q) = z[2]);
    ok := First(fib, q -> Chk6(m,q)[6]);
    if ok <> fail then
      cnt := cnt+1; Add(lifted,[m,z[2],ok]);
    fi;
  od;
  Add(per,[m,cnt,Length(Filtered(shad,u->u[1]=m))]);
  Print("  m=",m,"  持ち上がった shadow ",cnt,"/",
        Length(Filtered(shad,u->u[1]=m)),"\n");
od;
Print("  合計 ",Length(lifted),"/",Length(shad),"\n");

## ---- (T3) im(red) ----
Print("\n== (T3) im(red) ==\n");
if Length(lifted) > 0 then
  Print("  持ち上がった shadow の f-成分の個数 = ",
        Length(Set(List(lifted,z->z[2]))),"\n");
fi;
Print("\nDRIVER_DONE\n");
QUIT;
