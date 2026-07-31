#############################################################################
## search/probe/wac_v1/pent_t2t3_run2.g  -- (T2)(T3) fine-level, run2(修正版)
##  run1 で Psi(c) <> 1 が判明 ==> c ∉ (K_pi)_{PB3} ==> 簡約 hexagon (3.10)(3.11)
##  は fine 水準では使えない。本走は **原形 (2.18)(2.19) の defect** を
##  PB3 = <x,y,c> の語として直接構成する(sigma 共役公式を使う):
##    A := conj_{s1}:  x |-> x,   y |-> y^-1 X13 y,   X13 |-> y
##    B := conj_{s2}:  y |-> y,   x |-> X13,          X13 |-> X13^-1 x X13
##    X13 = x^-1 c y^-1   (paper: x12^-1 c x23^-1;  c = x12 x13 x23 中心)
##  defect(2.18) D1 := A(P) A(B(R))^-1 f,   P := x^m f^-1 B(y^m f), R := (X13 y)^m
##  defect(2.19) D2 := f^-1 B(y^m f) BA(x^m) [ BA(S) BA(f) ]^-1,  S := (x X13)^m
##  membership は Psi(=5 余面) で判定。接触遮断。
##  規約: 論文語 "AB" = GAP B*A。以下の語はすべて **論文順** で書き、
##        評価時に Rev で反転して GAP へ渡す。
##  Single lane (GAP 4.16.0). NOT a ledger claim.
#############################################################################
n := 5;;
tt := (1,2,3);; aa := (1,4,5);;
XX := aa*tt^-1;; ss := tt*XX^3;;
b1 := tt;; a1 := ss;;
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);; Eg := Group(aE,bE);;
Nord := Lcm(Order(xb),Order(yb),Order(cc));;
charm := Filtered([0..Nord-1], z->GcdInt(2*z+1,Nord)=1);;
Print("== window ==  P=A5? ",PN=AlternatingGroup(5),"  |E|=",Size(Eg),
      "  c=1 in E? ",cc=(),"  N_ord=",Nord,"  charming=",charm,"\n");

## ---- PB4 生成元の pi-像(GAP 値)----
X12v := xb;; X23v := yb;; X13v := yb^-1*xb^-1;;   ## c=1 in E
X34v := xb;; X24v := s1^-1*yb*s1;; X14v := s1^-1*X13v*s1;;
## ---- 5 余面の (x12,x23,x13) 上の値(A.18)・GAP 値(論文積は反転済)----
cof := [ [ X12v, X23v, X13v ],
         [ X23v, X34v, X24v ],
         [ X23v*X13v, X34v, X24v*X14v ],
         [ X13v*X12v, X34v*X24v, X14v ],
         [ X12v, X24v*X23v, X14v*X13v ] ];;
## c の余面像(論文 c = x12 x13 x23 -> GAP x23*x13*x12)
cofc := List([1..5], i -> cof[i][2]*cof[i][3]*cof[i][1]);;

D5 := DirectProduct(Eg,Eg,Eg,Eg,Eg);;
emb := List([1..5], i -> Embedding(D5,i));;
Pack := function(l) return Product(List([1..5], i -> Image(emb[i], l[i]))); end;;
Fw := FreeGroup("x","y","c");;
gx := GeneratorsOfGroup(Fw)[1];; gy := GeneratorsOfGroup(Fw)[2];;
gc := GeneratorsOfGroup(Fw)[3];;
Rev := function(w)   ## 論文語 -> GAP 語(文字列を反転)
  local l, r, i;
  l := LetterRepAssocWord(w); r := Reversed(l);
  return AssocWordByLetterRep(FamilyObj(gx), r);
end;;
PsiAt := function(w, i)   ## w は **論文順** の語
  return MappedWord(Rev(w), [gx,gy,gc], [cof[i][1],cof[i][2],cofc[i]]);
end;;
Psi := function(w) return Pack(List([1..5], i -> PsiAt(w,i))); end;;
one5 := One(D5);;
QP := Group(Psi(gx), Psi(gy), Psi(gc));;   ## PB3/(K_pi)_{PB3}
QF := Group(Psi(gx), Psi(gy));;            ## F2/(K_pi)_{F2}
pr1 := Projection(D5,1);;
Print("\n== refined quotients ==\n |PB3/(K_pi)_{PB3}| = ",Size(QP),
      "   |F2/(K_pi)_{F2}| = ",Size(QF),
      "   Psi(c)=1? ",Psi(gc)=one5,"  ord(Psi(c))=",Order(Psi(gc)),"\n");
H3 := Kernel(GroupHomomorphismByImages(QP, PN,
        [Psi(gx),Psi(gy),Psi(gc)], [xb,yb,()]));;
Print(" |H3| = ",Size(H3),"  ",StructureDescription(H3),
      "  中心的? ",IsSubgroup(Centre(QP),H3),"\n");

## ---- sigma 共役(論文順の語写像)----
X13w := gx^-1*gc*gy^-1;;                       ## 論文 x12^-1 c x23^-1
SubW := function(w, ix, iy, ic)                ## 論文順のまま置換
  return MappedWord(w, [gx,gy,gc], [ix,iy,ic]);
end;;
Aut1 := function(w) return SubW(w, gx, gy^-1*X13w*gy, gc); end;;   ## conj_{s1}
Aut2 := function(w) return SubW(w, X13w, gy, gc); end;;            ## conj_{s2}
## 健全性: A,B は c を保つ・A(B(...)) が使えること
Print(" A(c)=c ? ", Aut1(gc)=gc, "   B(c)=c ? ", Aut2(gc)=gc, "\n");
Print(" A,B は Psi 上で well-defined か(A の像の Psi が共役で一致): ",
      Psi(Aut1(gx))=Psi(gx), "\n");

## ---- GT(N_A) 列挙(接触遮断・原形 hexagon in E)----
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
      "   相異なる f = ",Length(Set(List(shad,z->z[2]))),"\n");

epiP := GroupHomomorphismByImages(Fw, QP, [gx,gy,gc],
          [Psi(gx),Psi(gy),Psi(gc)]);;
WordOf := function(q) return Rev(PreImagesRepresentative(epiP,q)); end;;
  ## PreImagesRepresentative は GAP 語を返すので Rev で論文順へ

Pent := function(w)   ## w は論文順の語
  local v;
  v := List([1..5], i -> PsiAt(w,i));
  return v[1]*v[4]*v[2] = v[3]*v[5];   ## 論文 234·1,23,4·123 = 1,2,34·12,3,4 の GAP 反転
end;;

Chk6 := function(m, q)
  local w, P0, R0, S0, D1, D2, c1, c2, c3, c4, c5, sb, u;
  w := WordOf(q); u := 2*m+1;
  ## (2.18) defect
  P0 := gx^m * w^-1 * Aut2(gy^m * w);
  R0 := (X13w*gy)^m;
  D1 := Aut1(P0) * (Aut1(Aut2(R0)))^-1 * w;
  c1 := Psi(D1) = one5;
  ## (2.19) defect
  S0 := (gx*X13w)^m;
  D2 := w^-1 * Aut2(gy^m*w) * Aut2(Aut1(gx^m))
        * ( Aut2(Aut1(S0)) * Aut2(Aut1(w)) )^-1;
  c2 := Psi(D2) = one5;
  c3 := Pent(w);
  c4 := (q in DerivedSubgroup(QP));
  sb := Group(Psi(gx^u), Psi(w^-1*gy^u*w));
  c5 := (Size(sb) = Size(QF));
  return [c1,c2,c3,c4,c5, c1 and c2 and c3 and c4 and c5];
end;;

Print("\n== (T2) 持ち上げ判定(6 条件同時・fine 水準)==\n");
lift := [];; perm2 := [];;
for m in charm do
  cnt := 0;
  for z in Filtered(shad, u->u[1]=m) do
    fib := Filtered(Elements(QP), q -> Image(pr1,q) = z[2]);
    tab := List(fib, q -> Chk6(m,q));
    Print("   m=",m," cond/125: c1=",Number(tab,r->r[1]),
          " c2=",Number(tab,r->r[2])," c3=",Number(tab,r->r[3]),
          " c4=",Number(tab,r->r[4])," c5=",Number(tab,r->r[5]),
          " ALL=",Number(tab,r->r[6]),"\n");
    ok := First(fib, q -> Chk6(m,q)[6]);
    if ok <> fail then cnt := cnt+1; Add(lift,[m,z[2]]); fi;
  od;
  Add(perm2,[m,cnt]);
  Print("  m=",m,"  ",cnt,"/",Length(Filtered(shad,u->u[1]=m)),
        "   (fiber size=",Size(QP)/Size(PN),")\n");
od;
Print("  合計 ",Length(lift),"/",Length(shad),
      "   f-成分 ",Length(Set(List(lift,z->z[2]))),"\n");
## ---- cert(機械生成)----
sJ := "";; outJ := OutputTextString(sJ,true);;
SetPrintFormattingStatus(outJ, false);;
AppendTo(outJ,"{\"schema\":\"wac_v1-pent-t2t3-cert/v1\",");
AppendTo(outJ,"\"generated_by\":\"search/probe/wac_v1/pent_t2t3_run2.g\",");
AppendTo(outJ,"\"note\":\"fine-level (T2)(T3). (K_pi)_{PB3} membership via ALL 5 cofaces per (2.4). Hexagons are the ORIGINAL (2.18)(2.19) defects built from sigma-conjugation formulas; the reduced (3.10)(3.11) is INVALID here because Psi(c) is nontrivial. Raw measurement, single GAP lane, ONE convention choice (paper-order words reversed at evaluation). Contact-blocked: no expected value used in any predicate. NOT a ledger claim.\",");
AppendTo(outJ,"\"f_orientation\":\"paper_order_words_reversed_at_evaluation\",");
AppendTo(outJ,"\"P_size\":",String(Size(PN)),",");
AppendTo(outJ,"\"N_ord\":",String(Nord),",");
AppendTo(outJ,"\"GT_size\":",String(Length(shad)),",");
AppendTo(outJ,"\"GT_distinct_f\":",String(Length(Set(List(shad,z->z[2])))),",");
AppendTo(outJ,"\"PB3_refined_size\":",String(Size(QP)),",");
AppendTo(outJ,"\"F2_refined_size\":",String(Size(QF)),",");
AppendTo(outJ,"\"psi_c_trivial\":",String(Psi(gc)=one5),",");
AppendTo(outJ,"\"psi_c_order\":",String(Order(Psi(gc))),",");
AppendTo(outJ,"\"H3_PB3_size\":",String(Size(H3)),",");
AppendTo(outJ,"\"H3_PB3_structure\":\"",StructureDescription(H3),"\",");
AppendTo(outJ,"\"H3_central\":",String(IsSubgroup(Centre(QP),H3)),",");
AppendTo(outJ,"\"fiber_size\":",String(Size(QP)/Size(PN)),",");
AppendTo(outJ,"\"lifted_total\":",String(Length(lift)),",");
AppendTo(outJ,"\"lifted_per_m\":",String(perm2),",");
AppendTo(outJ,"\"lifted_distinct_f\":",String(Length(Set(List(lift,z->z[2])))),",");
AppendTo(outJ,"\"im_red_order\":",String(Length(lift)),"}");
CloseStream(outJ);;
outF := OutputTextFile("search/certs/pent_t2t3_20260731.json", false);;
SetPrintFormattingStatus(outF, false);;
PrintTo(outF, sJ);;
CloseStream(outF);;
Print("\nCERT_WRITTEN\n");
Print("\nDRIVER_DONE\n");
QUIT;
