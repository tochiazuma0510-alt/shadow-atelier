Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

G9Rec := MakeGn(9);;
CheckGF8();;
SMat := MakeMatGF8(1,0,1,1);; TMat := MakeMatGF8(4,3,1,5);;
SPerm := MatToPermGF8(SMat);; TPerm := MatToPermGF8(TMat);;
WPerm := SPerm * TPerm^-1;; X4 := WPerm^2;;
Y4 := SPerm^-1 * X4 * SPerm;;
DirectSumPerm := function(p, psize, q, qsize)
  local images, j;
  images := [1..psize+qsize];
  for j in [1..qsize] do images[psize+j] := psize + (j^q); od;
  return p * PermList(images);
end;;
MX := DirectSumPerm(G9Rec.x, 27, X4, 9);;
MY := DirectSumPerm(G9Rec.y, 27, Y4, 9);;
MBlock := Group(MX,MY);;
if Size(MBlock) <> 1469664 then Error("order drift"); fi;;

ThetaM := GroupHomomorphismByImages(MBlock, MBlock, [MX,MY], [MY,MX]);;
TauM := GroupHomomorphismByImages(MBlock, MBlock, [MX,MY], [MY, MY^-1*MX^-1]);;
DerivedM := DerivedSubgroup(MBlock);;

codeToLetter := function(c)
  if c=1 then return ["x",1]; elif c=-1 then return ["x",-1];
  elif c=2 then return ["y",1]; else return ["y",-1]; fi;
end;;

row36codes := [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1];;
row71codes := [-1,-1,2,2,-1,-2,-1,-1,2,1,-2,1,1,2];;

EvalAppend := function(codes, gx, gy, one)
  local z,c,l;
  z:=one;;
  for c in codes do
    l := codeToLetter(c);;
    if l[1]="x" then z:=z*gx^l[2]; else z:=z*gy^l[2]; fi;
  od;
  return z;
end;;
EvalPrepend := function(codes, gx, gy, one)
  local z,c,l;
  z:=one;;
  for c in codes do
    l := codeToLetter(c);;
    if l[1]="x" then z:=gx^l[2]*z; else z:=gy^l[2]*z; fi;
  od;
  return z;
end;;

CheckVariant := function(label, f, thetaHom, tauHom, wdOrderReversed, tripleOrderReversed)
  local hex310, ymf, lhs, rhs, hex311, onto, genA, genB, m, u;
  m := 0;; u := 1;;
  hex310 := (f * Image(thetaHom, f) = Identity(MBlock));;
  if wdOrderReversed then ymf := f * MY^m; else ymf := MY^m * f; fi;
  if tripleOrderReversed then
    lhs := ymf * Image(tauHom, ymf) * Image(tauHom, Image(tauHom, ymf));;
  else
    lhs := Image(tauHom, Image(tauHom, ymf)) * Image(tauHom, ymf) * ymf;;
  fi;
  rhs := Identity(MBlock);;
  hex311 := (lhs = rhs);;
  onto := fail;;
  if hex310 and hex311 then
    genA := MX^u;; genB := f^-1*MY^u*f;;
    onto := Size(Group(genA,genB)) = Size(MBlock);;
  fi;
  Print(label, " hex310=", hex310, " hex311=", hex311, " onto=", onto, "\n");;
end;;

f_append := EvalAppend(row71codes, MX, MY, Identity(MBlock));;
f_prepend := EvalPrepend(row71codes, MX, MY, Identity(MBlock));;
Print("f_append = f_prepend ? ", f_append = f_prepend, "\n");;
Print("f_append in DerivedM: ", f_append in DerivedM, "  f_prepend in DerivedM: ", f_prepend in DerivedM, "\n");;

Print("--- row71 variants ---\n");;
CheckVariant("append_seed + naive_wd + naive_triple    :", f_append, ThetaM, TauM, false, false);;
CheckVariant("append_seed + naive_wd + reversed_triple :", f_append, ThetaM, TauM, false, true);;
CheckVariant("append_seed + reversed_wd + naive_triple :", f_append, ThetaM, TauM, true, false);;
CheckVariant("append_seed + reversed_wd + reversed_triple:", f_append, ThetaM, TauM, true, true);;
CheckVariant("prepend_seed + naive_wd + naive_triple    :", f_prepend, ThetaM, TauM, false, false);;
CheckVariant("prepend_seed + naive_wd + reversed_triple :", f_prepend, ThetaM, TauM, false, true);;
CheckVariant("prepend_seed + reversed_wd + naive_triple :", f_prepend, ThetaM, TauM, true, false);;
CheckVariant("prepend_seed + reversed_wd + reversed_triple:", f_prepend, ThetaM, TauM, true, true);;
Print("ALL_DONE\n");;
Print("--- cross-check: which f matches which known artifact word semantics ---\n");;
Print("row36 test with prepend_seed+naive_triple:\n");;
f36p := EvalPrepend(row36codes, MX, MY, Identity(MBlock));;
CheckVariant("row36 prepend+naive:", f36p, ThetaM, TauM, false, false);;
