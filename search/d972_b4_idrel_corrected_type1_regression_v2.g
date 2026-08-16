#############################################################################
## d972_b4_idrel_corrected_type1_regression_v2.g
##
## Tiny, non-production regression for the IdRel 2.49 type-1 log bug.
## Presentation: F(a,b,c) / < abc, b >.
## Rules:
##   R1 = [ abc, [ [1,id] ], id ]
##   R2 = [ bc,  [ [2,id] ], c   ]
## The contained occurrence is l1 = a*l2 (u=a,v=id), so c2u=[2,a^-1].
##
## The upstream and corrected candidates are checked directly in F3.  This
## test does not run U6/158 and makes no A/B claim.
#############################################################################

if LoadPackage("idrel") <> true then
  Error("d972 type1 regression: idrel package unavailable");
fi;
Read("search/d972_b4_idrel_logged_onepass_corrected_v2.g");;

D972B4T1F := FreeGroup(3,"t");;
D972B4T1G := GeneratorsOfGroup(D972B4T1F);;
D972B4T1Rel := [
  D972B4T1G[1]*D972B4T1G[2]*D972B4T1G[3],
  D972B4T1G[2]
];;

D972B4T1Word := function(row)
  local w,x;
  w:=One(D972B4T1F);
  for x in row do
    if x>0 then w:=w*D972B4T1G[x];
    else w:=w*D972B4T1G[-x]^-1;
    fi;
  od;
  return w;
end;;
D972B4T1Inv := function(row)
  return List(Reversed(row),x->-x);
end;;
D972B4T1Proof := function(lhs,rhs,log)
  local got,e,idx,rel,conj;
  got:=One(D972B4T1F);
  for e in log do
    idx:=e[1];
    rel:=D972B4T1Rel[AbsInt(idx)];
    if idx<0 then rel:=rel^-1; fi;
    conj:=D972B4T1Word(e[2]);
    got:=got*(rel^conj);
  od;
  got:=got*D972B4T1Word(rhs);
  return got=D972B4T1Word(lhs);
end;;

## log1=log2=[]; c1=[[1,id]]; c2u=[[2,a^-1]].
## Source : iL=inv(log1)+inv(c1)+c2u+log2.
D972B4T1Upstream := [ [ -1, [] ], [ 2, [ -1 ] ] ];;
## Correct : iL=inv(log1)+inv(c2u)+c1+log2.
D972B4T1Corrected := [ [ -2, [ -1 ] ], [ 1, [] ] ];;

if D972B4T1Proof([1,3],[],D972B4T1Upstream) then
  Error("d972 type1 regression: upstream candidate unexpectedly accepted");
fi;
if not D972B4T1Proof([1,3],[],D972B4T1Corrected) then
  Error("d972 type1 regression: corrected candidate rejected");
fi;

## Also execute the repo-local copied constructor on the two corresponding
## monoid rules.  The assertion is deliberately only about return shape; the
## F3 equations above are the regression's semantic gate.
D972B4T1U := D972B4T1F/D972B4T1Rel;;
D972B4T1M := MonoidPresentationFpGroup(D972B4T1U);;
D972B4T1MF := FreeGroupOfPresentation(D972B4T1M);;
D972B4T1MG := GeneratorsOfGroup(D972B4T1MF);;
D972B4T1Arr := ArrangementOfMonoidGenerators(D972B4T1U);;
D972B4T1MonWord := function(row)
  local w,x,p;
  w:=One(D972B4T1MG[1]);
  for x in row do
    p:=Position(D972B4T1Arr,x);
    if p=fail then Error("d972 type1 regression: arrangement drift"); fi;
    w:=w*D972B4T1MG[p];
  od;
  return w;
end;;
D972B4T1Id := One(D972B4T1MF);;
D972B4T1R1 := [ D972B4T1MonWord([1,2,3]), [ [1,D972B4T1Id] ],
  D972B4T1Id ];;
D972B4T1R2 := [ D972B4T1MonWord([2,3]), [ [2,D972B4T1Id] ],
  D972B4T1MonWord([3]) ];;
D972B4T1Out := D972B4LoggedOnePassKB_Corrected(D972B4T1M,
  [D972B4T1R1,D972B4T1R2]);;
if not IsList(D972B4T1Out) then
  Error("d972 type1 regression: corrected constructor returned non-list");
fi;
D972B4T1DispatchOut := LoggedOnePassKB(D972B4T1M,
  [D972B4T1R1,D972B4T1R2]);;
if D972B4T1DispatchOut<>D972B4T1Out then
  Error("d972 type1 regression: corrected method dispatch mismatch");
fi;

Print("D972_B4_CORRECTED_TYPE1_REGRESSION_PASS upstream=REJECT ",
  "corrected=ACCEPT copied_constructor_rules=",Length(D972B4T1Out),
  " lhs=ac rhs=id\n");
