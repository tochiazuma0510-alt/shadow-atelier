#############################################################################
## d972_d972core_c2six_intersection_v2.g
##
## 157cj: exact fast lossless source words for the four pinned PB4 strand
## deletions.  It avoids PreImagesRepresentative in the full E^4 x H9
## image.  Since the pinned H9 derived-series gate is metabelian, the
## commutator-of-commutators law is an exact H9 identity.  Its values are
## solved coordinatewise in E (order 32256), then replayed in E/P/G9.
## The order/rank conclusion is structural: E is perfect, while every
## subgroup of G9^4 is solvable, so Goursat forces the joint subdirect image
## to be E^4 x H9 (H9 is the actual, possibly proper, G9^4 image).
#############################################################################

if LoadPackage("json") <> true then
  Error("157bd: GAP json package unavailable");
fi;;

D972BDSourcePath := "search/certs/d972_phase2b_nonsplit_v1_20260813.json";;
D972BDSourceSha :=
  "648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9";;
D972BDSourceCheckPath :=
  "search/certs/d972_phase2b_nonsplit_v1_check_20260813.json";;
D972BDSourceCheckSha :=
  "90db0fc500eb44bd905059d7a00dfaf4920c8c9890ed151d773141456fd059bb";;
D972BDMapsPath := "search/certs/d972_b4_marity_reduction_maps_v1.json";;
D972BDMapsSha :=
  "6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2";;
D972BDMapsCheckerSha :=
  "eb87e9d42ecde979b82a31beec8fdedea3e221a55d4881f8a71dbaffc2a7a032";;
D972BDGnSourcePath := "search/week3-battery-common.g";;
D972BDGnSourceSha :=
  "aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998";;
D972BDDovetailSourcePath := "search/d972_dovetail_core_v2.g";;
D972BDDovetailSourceSha :=
  "1c3348003805df874ab6d42503720259564eec25c1aebfb1c548a759e3d9f7ae";;
D972BDDegreeE := 72;;
D972BDDegreeP := 9;;
D972BDDegreeG9 := 27;;
D972BDOutput := Filename(DirectoryTemporary(),
  "d972_d972core_c2six_intersection_v2.json");;
D972BDMode := "full";;
if IsBound(D972_BD_OUTPUT) then D972BDOutput := D972_BD_OUTPUT; fi;;
if IsBound(D972_BD_MODE) then D972BDMode := D972_BD_MODE; fi;;

D972BDJoin := function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;

D972BDJson := function(x)
  local names,parts,i,p;
  if x=fail then return "null"; fi;
  if IsInt(x) then return String(x); fi;
  if IsRat(x) then return String(x); fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsRecord(x) then
    names:=Set(RecNames(x));;
    parts:=List(names,i->Concatenation(D972BDJson(i),":",D972BDJson(x.(i))));
    return Concatenation("{",D972BDJoin(parts,","),"}");
  fi;
  if IsList(x) then
    p:=List([1..Length(x)],i->D972BDJson(x[i]));
    return Concatenation("[",D972BDJoin(p,","),"]");
  fi;
  Error("157bd: unsupported JSON value");
end;;
D972BDWrite := function(path,obj)
  local f;
  f:=OutputTextFile(path,false);;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,D972BDJson(obj),"\n");;
  CloseStream(f);;
end;;
D972BDReadJson := function(path,sha,label)
  local raw,obj;
  raw:=StringFile(path);;
  if raw=fail or HexSHA256(raw)<>sha then
    Error("157bd: ",label," SHA drift");
  fi;
  obj:=JsonStringToGap(raw);;
  return rec(raw:=raw,obj:=obj);
end;;

D972BDPerm := function(a) return PermList(List(a,x->x+1)); end;;
D972BDZeroArray := function(p,n) return List([1..n],i->i^p-1); end;;
D972BDFullZeroArray := function(p,n) return List([1..n],i->i^p-1); end;;

D972BDEvalWord := function(word,gens)
  local out,v;
  out:=One(gens[1]);;
  for v in word do
    if v>0 then out:=out*gens[v];
    else out:=out*gens[-v]^-1; fi;
  od;
  return out;
end;;
D972BDSignedWord := function(w)
  local e,out,i,g,n,j;
  e:=ExtRepOfObj(w);; out:=[];; i:=1;;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if n>0 then for j in [1..n] do Add(out,g); od;
    else for j in [1..-n] do Add(out,-g); od; fi;
    i:=i+2;
  od;
  return out;
end;;

D972BDTuple := function(vals,degree)
  local images,offset,v,j;
  images:=[];; offset:=0;;
  for v in vals do
    for j in [1..degree] do Add(images,offset+j^v); od;
    offset:=offset+degree;
  od;
  return PermList(images);
end;;

D972BDBlockRestrict := function(perm,offset,size)
  local images,j;
  images:=[];;
  for j in [1..size] do images[j]:=(offset+j)^perm-offset; od;
  if Set(images)<>[1..size] then Error("157bd: block does not close"); fi;
  return PermList(images);
end;;

D972BDJoint := function(evals,gvals)
  local images,offset,v,j;
  images:=[];; offset:=0;;
  for v in evals do
    for j in [1..D972BDDegreeE] do Add(images,offset+j^v); od;
    offset:=offset+D972BDDegreeE;
  od;
  for v in gvals do
    for j in [1..D972BDDegreeG9] do Add(images,offset+j^v); od;
    offset:=offset+D972BDDegreeG9;
  od;
  return PermList(images);
end;;

## Exact MakeGn(n) convention from the pinned D972 core.  Repeated locally
## rather than Read()ing a producer helper; the checker repeats it too.
D972BDMakeDn := function(n)
  local r,s;
  r:=PermList(Concatenation([2..n],[1]));;
  s:=PermList(List([1..n],j->((n-(j-1)) mod n)+1));;
  if not (Order(r)=n and Order(s)=2 and s*r*s^-1=r^-1) then
    Error("157bd: D_n relation drift");
  fi;
  return [r,s];
end;;
D972BDMakeGn := function(n)
  local rs,r,s,tr,x,y;
  rs:=D972BDMakeDn(n);; r:=rs[1];; s:=rs[2];;
  tr:=function(p,i)
    local l,j;
    l:=List([1..3*n],k->k);;
    for j in [1..n] do l[j+(i-1)*n]:=(j^p)+(i-1)*n; od;
    return PermList(l);
  end;;
  x:=tr(r,1)*tr(s,2)*tr(s,3);;
  y:=tr(s*r,1)*tr(r,2)*tr(s*r,3);;
  return rec(x:=x,y:=y,G:=Group(x,y),r:=r,s:=s);
end;;

D972BDModuleMask := function(v,module,E)
  local mask,j,prod;
  for mask in [0..63] do
    prod:=One(E);;
    for j in [1..6] do
      if QuoInt(mask,2^(j-1)) mod 2=1 then prod:=prod*module[j]; fi;
    od;
    if prod=v then return mask; fi;
  od;
  Error("157bd: module basis mask missing");
end;;

D972BDMatrix := function(e,module,E)
  return List(module,v->D972BDModuleMask(e^-1*v*e,module,E));
end;;

D972BDSource:=D972BDReadJson(D972BDSourcePath,D972BDSourceSha,
  "phase2b receipt");;
D972BDSourceCheck:=D972BDReadJson(D972BDSourceCheckPath,D972BDSourceCheckSha,
  "phase2b checker receipt");;
D972BDMaps:=D972BDReadJson(D972BDMapsPath,D972BDMapsSha,
  "four-map receipt");;
D972BDS:=D972BDSource.obj;; D972BDSC:=D972BDSourceCheck.obj;;
D972BDM:=D972BDMaps.obj;;
if D972BDS.schema<>"d972_phase2b_nonsplit/v1" or
   D972BDSC.schema<>"d972_phase2b_nonsplit_check/v1" or
   D972BDSC.all_checks_true<>true or
   D972BDM.schema<>"d972-b4-marity-reduction-maps/v1" or
   D972BDM.maps_sha256<>"31c1aa38eae32035c806e5fe5a422048fe6fca36e55c0314d7510fd3087deb6d" or
   D972BDM.status<>"PROVED_BY_CANONICAL_STRAND_FORGETTING" then
  Error("157bd: pinned input gate failed");
fi;;

D972BDNames:=["a","b","c","u","v","w","x","y","z"];;
D972BDOriginal:=List(D972BDNames,n->D972BDPerm(D972BDS.candidate.original_generator_arrays.(n)));;
D972BDNamed:=rec();;
for D972BDI in [1..Length(D972BDNames)] do
  D972BDNamed.(D972BDNames[D972BDI]):=D972BDOriginal[D972BDI];
od;;
D972BDE:=Group(D972BDPerm(D972BDS.candidate.selected_arrays.X),
  D972BDPerm(D972BDS.candidate.selected_arrays.Y));;
D972BDX:=D972BDPerm(D972BDS.candidate.selected_arrays.X);;
D972BDY:=D972BDPerm(D972BDS.candidate.selected_arrays.Y);;
D972BDZ:=(D972BDY*D972BDX)^-1;;
D972BDModule:=List(["u","v","w","x","y","z"],n->D972BDNamed.(n));;
D972BDV:=Group(D972BDModule);;
if Size(D972BDE)<>32256 or Size(D972BDV)<>64 or
   not IsNormal(D972BDE,D972BDV) then
  Error("157bd: E/V reconstruction drift");
fi;;
D972BDQMap:=NaturalHomomorphismByNormalSubgroup(D972BDE,D972BDV);;
D972BDAbstractP:=Image(D972BDQMap);;
D972BDAbstractPX:=Image(D972BDQMap,D972BDX);;
D972BDAbstractPY:=Image(D972BDQMap,D972BDY);;

## Independent canonical degree-9 permutation model for P=PSL(2,8).  The
## natural quotient above is retained for the E/V gate; receipt arrays use
## this concrete model so the P replay is lossless and degree-pinned.
D972BDBit:=function(n,i) return QuoInt(n,2^i) mod 2; end;;
D972BDXor:=function(a,b)
  local result,i;
  result:=0;;
  for i in [0..6] do
    if (D972BDBit(a,i)+D972BDBit(b,i)) mod 2=1 then
      result:=result+2^i;
    fi;
  od;
  return result;
end;;
D972BDMul:=function(a,b)
  local result,i;
  result:=0;;
  for i in [0..2] do
    if D972BDBit(b,i)=1 then result:=D972BDXor(result,a*2^i); fi;
  od;
  for i in [4,3] do
    if D972BDBit(result,i)=1 then result:=D972BDXor(result,11*2^(i-3)); fi;
  od;
  return result;
end;;
D972BDInv:=function(a)
  local b;
  if a=0 then Error("157bd: GF8 inverse of zero"); fi;
  for b in [1..7] do if D972BDMul(a,b)=1 then return b; fi; od;
  Error("157bd: GF8 inverse missing");
end;;
D972BDMatPerm:=function(M)
  local images,a,b,c,d,num,den,x;
  a:=M[1][1];; b:=M[1][2];; c:=M[2][1];; d:=M[2][2];;
  images:=[];;
  if c=0 then images[1]:=1;
  else images[1]:=2+D972BDMul(a,D972BDInv(c)); fi;
  for x in [0..7] do
    num:=D972BDXor(D972BDMul(a,x),b);;
    den:=D972BDXor(D972BDMul(c,x),d);;
    if den=0 then images[2+x]:=1;
    else images[2+x]:=2+D972BDMul(num,D972BDInv(den)); fi;
  od;
  return PermList(images);
end;;
D972BDSperm:=D972BDMatPerm([[1,0],[1,1]]);;
D972BDTperm:=D972BDMatPerm([[4,3],[1,5]]);;
D972BDWperm:=D972BDSperm*D972BDTperm^-1;;
D972BDP:=Group(D972BDWperm^2,
  D972BDSperm^-1*D972BDWperm^2*D972BDSperm);;
D972BDPX:=D972BDWperm^2;;
D972BDPY:=D972BDSperm^-1*D972BDPX*D972BDSperm;;
D972BDPZ:=(D972BDPY*D972BDPX)^-1;;
if Size(D972BDP)<>504 then Error("157bd: P order drift"); fi;;
if GroupHomomorphismByImages(D972BDAbstractP,D972BDP,
    [D972BDAbstractPX,D972BDAbstractPY],[D972BDPX,D972BDPY])=fail then
  Error("157bd: abstract-to-canonical P map drift");
fi;;
D972BDTargetE:=[D972BDX,D972BDZ,D972BDY];;
D972BDTargetP:=[D972BDPX,D972BDPZ,D972BDPY];;
D972BDERows:=[];; D972BDPRows:=[];
for D972BDI in [1..4] do
  Add(D972BDERows,List(D972BDM.maps[D972BDI].generator_images,
    w->D972BDEvalWord(w,D972BDTargetE)));
  Add(D972BDPRows,List(D972BDM.maps[D972BDI].generator_images,
    w->D972BDEvalWord(w,D972BDTargetP)));
od;;
D972BDTupleRows:=List([1..6],j->List([1..4],i->D972BDERows[i][j]));;
D972BDTuplePRows:=List([1..6],j->List([1..4],i->D972BDPRows[i][j]));;
D972BDLabels:=["x12","x13","x14","x23","x24","x34"];;
D972BDTupleLabelRows:=[
  ["1","1","X","X"],["1","X","1","Z"],
  ["1","Z","Z","1"],["X","1","1","Y"],
  ["Z","1","Y","1"],["Y","Y","1","1"]];;
D972BDExpectedRows:=[
  [One(D972BDE),One(D972BDE),D972BDX,D972BDX],
  [One(D972BDE),D972BDX,One(D972BDE),D972BDZ],
  [One(D972BDE),D972BDZ,D972BDZ,One(D972BDE)],
  [D972BDX,One(D972BDE),One(D972BDE),D972BDY],
  [D972BDZ,One(D972BDE),D972BDY,One(D972BDE)],
  [D972BDY,D972BDY,One(D972BDE),One(D972BDE)]];;
if D972BDTupleRows<>D972BDExpectedRows then
  Error("157bd: E tuple table drift");
fi;;

D972BDG9Data:=D972BDMakeGn(9);;
D972BDG9:=D972BDG9Data.G;; D972BDX9:=D972BDG9Data.x;;
D972BDY9:=D972BDG9Data.y;; D972BDZ9:=(D972BDY9*D972BDX9)^-1;;
if Size(D972BDG9)<>2916 then Error("157bd: G9 order drift"); fi;;
D972BDG9Target:=[D972BDX9,D972BDZ9,D972BDY9];;
D972BDG9Rows:=[];
for D972BDI in [1..4] do
  Add(D972BDG9Rows,List(D972BDM.maps[D972BDI].generator_images,
    w->D972BDEvalWord(w,D972BDG9Target)));
od;;
D972BDTupleG9Rows:=List([1..6],j->List([1..4],i->D972BDG9Rows[i][j]));;
D972BDG9TupleGens:=List(D972BDTupleG9Rows,
  row->D972BDTuple(row,D972BDDegreeG9));;
D972BDG9Image:=Group(D972BDG9TupleGens);;
D972BDG9ImageOrder:=Size(D972BDG9Image);;
D972BDG9Series:=DerivedSeries(D972BDG9);;
D972BDG9SeriesOrders:=List(D972BDG9Series,Size);;
if not IsSolvableGroup(D972BDG9) or Length(D972BDG9SeriesOrders)>3 then
  Error("157bd: G9 solvability gate failed");
fi;;
D972BDTupleGens:=List(D972BDTupleRows,
  row->D972BDTuple(row,D972BDDegreeE));;
D972BDPGens:=List(D972BDTuplePRows,
  row->D972BDTuple(row,D972BDDegreeP));;
D972BDFactorOrders:=List([1..4],i->Size(Group(List(D972BDTupleRows,
  row->row[i]))));;
D972BDFactorOrdersP:=List([1..4],i->Size(Group(List(D972BDTuplePRows,
  row->row[i]))));;
D972BDFactorOrdersG9:=List([1..4],i->Size(Group(List(D972BDTupleG9Rows,
  row->row[i]))));;
if D972BDFactorOrders<>[32256,32256,32256,32256] or
   D972BDFactorOrdersP<>[504,504,504,504] or
   D972BDFactorOrdersG9<>[2916,2916,2916,2916] then
  Error("157bd: factor projection order drift");
fi;;
D972BDWitnessPairs:=[[4,6],[2,6],[1,5],[1,4]];;
D972BDComm:=Comm(D972BDX,D972BDY);;
D972BDPureExpected:=function(coord,comm,eone)
  local vals,j;
  vals:=[];;
  for j in [1..4] do
    if j=coord then Add(vals,comm); else Add(vals,eone); fi;
  od;
  return D972BDTuple(vals,D972BDDegreeE);
end;;
D972BDPure:=[];;
for D972BDI in [1..4] do
  D972BDW:=Comm(D972BDTupleGens[D972BDWitnessPairs[D972BDI][1]],
    D972BDTupleGens[D972BDWitnessPairs[D972BDI][2]]);;
  Add(D972BDPure,D972BDW);;
  if D972BDW<>D972BDPureExpected(D972BDI,D972BDComm,One(D972BDE)) then
    Error("157bd: pure-coordinate E witness drift");
  fi;
od;;
D972BDNormalE:=NormalClosure(D972BDE,Group(D972BDComm));;
D972BDNormalP:=NormalClosure(D972BDP,Group(Comm(D972BDPX,D972BDPY)));;
if Size(D972BDNormalE)<>32256 or Size(D972BDNormalP)<>504 then
  Error("157bd: perfect/direct-product witness failed");
fi;;

D972BDWords:=[];
D972BDFastRecords:=[];;
D972BDFree:=FreeGroup(6,"d972_joint_v2");;
D972BDFreeGens:=GeneratorsOfGroup(D972BDFree);;
D972BDTupleGens:=List(D972BDTupleRows,
  row->D972BDTuple(row,D972BDDegreeE));;
D972BDTuplePGens:=List(D972BDTuplePRows,
  row->D972BDTuple(row,D972BDDegreeP));;
D972BDTupleG9Gens:=List(D972BDTupleG9Rows,
  row->D972BDTuple(row,D972BDDegreeG9));;
D972BDG9Identity:=One(D972BDTupleG9Gens[1]);;

## The pinned derived-series bound makes H9 metabelian.  Therefore the
## commutator of two commutators is an exact H9 identity.
D972BDFastLaw:=function(a,b,c,d)
  return Comm(Comm(a,b),Comm(c,d));
end;;
D972BDConjugateWord:=function(w,a)
  return a^-1*w*a;
end;;
D972BDExpandLawWord:=function(w,law_words)
  local e,out,i,g,n,j;
  e:=ExtRepOfObj(w);; out:=One(D972BDFree);; i:=1;;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if n>0 then
      for j in [1..n] do out:=out*law_words[g]; od;
    else
      for j in [1..-n] do out:=out*law_words[g]^-1; od;
    fi;
    i:=i+2;
  od;
  return out;
end;;
D972BDPureVals:=function(coord,value,eone)
  local vals,j;
  vals:=[];;
  for j in [1..4] do
    if j=coord then Add(vals,value); else Add(vals,eone); fi;
  od;
  return vals;
end;;

if Length(D972BDG9SeriesOrders)>3 then
  Error("157cj: H9 is not certified metabelian");
fi;;
for D972BDCoord in [1..4] do
  D972BDPair:=D972BDWitnessPairs[D972BDCoord];;
  D972BDPureWord:=Comm(D972BDFreeGens[D972BDPair[1]],
    D972BDFreeGens[D972BDPair[2]]);;
  D972BDActors:=Concatenation(D972BDFreeGens,
    List(D972BDFreeGens,a->a^-1));;
  D972BDConjugates:=[D972BDPureWord];;
  for D972BDA in D972BDActors do
    Add(D972BDConjugates,D972BDConjugateWord(D972BDPureWord,D972BDA));
  od;
  D972BDSeed:=fail;; D972BDSeedOperands:=fail;;
  for D972BDI in [1..Length(D972BDConjugates)-3] do
    for D972BDJ in [D972BDI+1..Length(D972BDConjugates)-2] do
      for D972BDK in [D972BDJ+1..Length(D972BDConjugates)-1] do
        for D972BDL in [D972BDK+1..Length(D972BDConjugates)] do
          D972BDTry:=D972BDFastLaw(D972BDConjugates[D972BDI],
            D972BDConjugates[D972BDJ],D972BDConjugates[D972BDK],
            D972BDConjugates[D972BDL]);;
          D972BDTrySigned:=D972BDSignedWord(D972BDTry);;
          D972BDTryG9:=D972BDEvalWord(D972BDTrySigned,D972BDTupleG9Gens);;
          D972BDTryE:=D972BDEvalWord(D972BDTrySigned,D972BDTupleGens);;
          D972BDTryECoord:=D972BDBlockRestrict(D972BDTryE,
            (D972BDCoord-1)*D972BDDegreeE,D972BDDegreeE);;
          if D972BDTryG9=D972BDG9Identity and
             D972BDTryE=D972BDTuple(
               D972BDPureVals(D972BDCoord,D972BDTryECoord,One(D972BDE)),
               D972BDDegreeE) and
             D972BDTryECoord<>One(D972BDE) then
            D972BDSeed:=D972BDTry;;
            D972BDSeedOperands:=[D972BDConjugates[D972BDI],
              D972BDConjugates[D972BDJ],D972BDConjugates[D972BDK],
              D972BDConjugates[D972BDL]];;
            break;
          fi;
        od;
        if D972BDSeed<>fail then break; fi;
      od;
      if D972BDSeed<>fail then break; fi;
    od;
    if D972BDSeed<>fail then break; fi;
  od;
  if D972BDSeed=fail then
    Error("157cj: no nontrivial metabelian-law seed at coordinate ",D972BDCoord);
  fi;;
  D972BDLawWords:=[D972BDSeed];;
  for D972BDA in D972BDActors do
    Add(D972BDLawWords,D972BDConjugateWord(D972BDSeed,D972BDA));
  od;
  D972BDLawEValues:=List(D972BDLawWords,w->
    D972BDBlockRestrict(D972BDEvalWord(D972BDSignedWord(w),D972BDTupleGens),
      (D972BDCoord-1)*D972BDDegreeE,D972BDDegreeE));;
  D972BDLawGroup:=Group(D972BDLawEValues);;
  if Size(D972BDLawGroup)<>Size(D972BDE) then
    Error("157cj: coordinate law solver does not generate E at ",D972BDCoord);
  fi;;
  D972BDLawFree:=FreeGroup(Length(D972BDLawWords),"d972_law");;
  D972BDLawGens:=GeneratorsOfGroup(D972BDLawFree);;
  D972BDLawEpi:=GroupHomomorphismByImages(D972BDLawFree,D972BDLawGroup,
    D972BDLawGens,D972BDLawEValues);;
  if D972BDLawEpi=fail then Error("157cj: coordinate E epimorphism failed"); fi;;
  D972BDSolverE:=List(D972BDLawEValues,v->D972BDZeroArray(v,D972BDDegreeE));;
  D972BDSolverP:=[];; D972BDSolverG9:=[];;
  for D972BDI in [1..Length(D972BDLawWords)] do
    D972BDW:=D972BDLawWords[D972BDI];;
    D972BDFullP:=D972BDEvalWord(D972BDSignedWord(D972BDW),D972BDTuplePGens);;
    D972BDFullG9:=D972BDEvalWord(D972BDSignedWord(D972BDW),D972BDTupleG9Gens);;
    Add(D972BDSolverP,D972BDZeroArray(D972BDFullP,4*D972BDDegreeP));;
    Add(D972BDSolverG9,D972BDZeroArray(D972BDFullG9,4*D972BDDegreeG9));;
  od;
  for D972BDBasisIndex in [1..6] do
    D972BDTargetE:=D972BDModule[D972BDBasisIndex];;
    D972BDPre:=PreImagesRepresentative(D972BDLawEpi,D972BDTargetE);;
    if D972BDPre=fail then
      Error("157cj: coordinate E preimage failed at ",D972BDCoord,
        " basis ",D972BDBasisIndex);
    fi;;
    D972BDWord:=D972BDExpandLawWord(D972BDPre,D972BDLawWords);;
    D972BDEVals:=D972BDPureVals(D972BDCoord,D972BDTargetE,One(D972BDE));;
    D972BDPVars:=D972BDPureVals(D972BDCoord,One(D972BDP),One(D972BDP));;
    D972BDGVals:=D972BDPureVals(D972BDCoord,One(D972BDG9),One(D972BDG9));;
    if D972BDEvalWord(D972BDSignedWord(D972BDWord),D972BDTupleGens) <>
         D972BDTuple(D972BDEVals,D972BDDegreeE) or
       D972BDEvalWord(D972BDSignedWord(D972BDWord),D972BDTuplePGens) <>
         D972BDTuple(D972BDPVars,D972BDDegreeP) or
       D972BDEvalWord(D972BDSignedWord(D972BDWord),D972BDTupleG9Gens) <>
         D972BDTuple(D972BDGVals,D972BDDegreeG9) then
      Error("157cj: coordinate source replay failed at ",D972BDCoord,
        " basis ",D972BDBasisIndex);
    fi;;
    Add(D972BDWords,rec(coordinate:=D972BDCoord,
      module_index:=D972BDBasisIndex,
      source_word:=D972BDSignedWord(D972BDWord),
      target_E:=List(D972BDEVals,v->D972BDZeroArray(v,D972BDDegreeE)),
      target_P:=List(D972BDPVars,v->D972BDZeroArray(v,D972BDDegreeP)),
      target_G9:=List(D972BDGVals,v->D972BDZeroArray(v,D972BDDegreeG9))));
  od;
  Add(D972BDFastRecords,rec(coordinate:=D972BDCoord,
    law:="[[a,b],[c,d]]", derived_series_length:=Length(D972BDG9SeriesOrders),
    seed_source_word:=D972BDSignedWord(D972BDSeed),
    seed_operand_source_words:=List(D972BDSeedOperands,D972BDSignedWord),
    solver_source_words:=List(D972BDLawWords,D972BDSignedWord),
    solver_target_E:=D972BDSolverE,solver_target_P:=D972BDSolverP,
    solver_target_G9:=D972BDSolverG9,solver_group_order:=Size(D972BDLawGroup),
    solver_generator_count:=Length(D972BDLawWords)));
od;
D972BDPureMatrices:=List(D972BDTupleRows,row->
  List(row,e->D972BDMatrix(e,D972BDModule,D972BDE)));;
D972BDTheta:=GroupHomomorphismByImages(D972BDE,D972BDE,
  [D972BDX,D972BDY],[D972BDY,D972BDX]);;
D972BDTau:=GroupHomomorphismByImages(D972BDE,D972BDE,
  [D972BDX,D972BDY],[D972BDY,D972BDZ]);;
if D972BDTheta=fail or D972BDTau=fail or
   not IsBijective(D972BDTheta) or not IsBijective(D972BDTau) then
  Error("157bd: B3 stabilizer action drift");
fi;;
D972BDThetaMatrix:=List(D972BDModule,v->D972BDModuleMask(Image(D972BDTheta,v),
  D972BDModule,D972BDE));;
D972BDTauMatrix:=List(D972BDModule,v->D972BDModuleMask(Image(D972BDTau,v),
  D972BDModule,D972BDE));;

if D972BDMode="selftest" then
  Print("D972_CORE_INTERSECTION_V2_GAP_SELFTEST_PASS maps=4 tuples=6 g9=2916 rank=24 fast=coordinate-law\n");
  Print("D972_CORE_INTERSECTION_V2_GAP_SELFTEST_PASS\n");
else
  D972BDGEOrder:=Size(D972BDE)^4;;
  D972BDGPOrder:=Size(D972BDP)^4;;
  D972BDReceipt:=rec(
    schema:="d972-d972core-c2six-intersection/v2",
    final_marker:="D972_CORE_INTERSECTION_V2_FINAL",
    status:="CORE_INTERSECTION_V2_COMPUTED",
    source_receipt_sha256:=D972BDSourceSha,
    source_checker_receipt_sha256:=D972BDSourceCheckSha,
    four_map_receipt_sha256:=D972BDMapsSha,
    four_map_checker_sha256:=D972BDMapsCheckerSha,
    g9_constructor:=rec(source_path:=D972BDGnSourcePath,
      source_sha256:=D972BDGnSourceSha,
      dovetail_core_path:=D972BDDovetailSourcePath,
      dovetail_core_sha256:=D972BDDovetailSourceSha,
      convention:="MakeGn(n): x=(r,s,s), y=(sr,r,sr) on three D_n blocks",
      degree:=D972BDDegreeG9,order:=Size(D972BDG9),
      x_array:=D972BDZeroArray(D972BDX9,D972BDDegreeG9),
      y_array:=D972BDZeroArray(D972BDY9,D972BDDegreeG9),
      z_array:=D972BDZeroArray(D972BDZ9,D972BDDegreeG9),
      solvable:=IsSolvableGroup(D972BDG9),
      derived_series_orders:=D972BDG9SeriesOrders),
    pinned_inputs:=rec(E_order:=Size(D972BDE),V_order:=Size(D972BDV),
      P_order:=Size(D972BDP),module_basis_labels:=["u","v","w","x","y","z"],
      old_raw_158_used:=false),
    generator_labels:=D972BDLabels,
    tuple_labels:=D972BDTupleLabelRows,
    tuple_images_E:=List(D972BDTupleRows,row->
      List(row,e->D972BDZeroArray(e,D972BDDegreeE))),
    tuple_images_P:=List(D972BDTuplePRows,row->
      List(row,e->D972BDZeroArray(e,D972BDDegreeP))),
    tuple_images_G9:=List(D972BDTupleG9Rows,row->
      List(row,e->D972BDZeroArray(e,D972BDDegreeG9))),
    four_map_replay:=rec(target_order:=["X","Z","Y"],
      map_count:=4,generator_count:=6,all_six_rows_replayed:=true),
    projection_certificate:=rec(
      E_factor_orders:=D972BDFactorOrders,
      P_factor_orders:=D972BDFactorOrdersP,
      G9_factor_orders:=D972BDFactorOrdersG9,
      E4_order:=D972BDGEOrder,P4_order:=D972BDGPOrder,
      pure_coordinate_witness_pairs:=D972BDWitnessPairs,
      pure_coordinate_witnesses_E:=List(D972BDPure,
        p->D972BDFullZeroArray(p,4*D972BDDegreeE)),
      normal_closure_commutator_E:=Size(D972BDNormalE),
      normal_closure_commutator_P:=Size(D972BDNormalP),
      E4_is_direct_product:=true,P4_is_direct_product:=true,
      no_G9_fourfold_onto_assumption:=true),
    joint_image:=rec(
      ambient_degree:=4*D972BDDegreeE+4*D972BDDegreeG9,
      E4_projection_order:=D972BDGEOrder,
      G9_fourfold_image_order:=D972BDG9ImageOrder,
      G9_fourfold_image_constructed:=true,
      joint_order_computed:=false,
      goursat_direct_product:=true,
      proof:="F is subdirect in E^4 x H9; E^4 is perfect and H9<=G9^4 is solvable, so the common Goursat quotient is trivial and F=E^4 x H9"),
    intersection:=rec(
      definition:="W=C_M/K_0 embedded in C_P/C_E",
      N_M_definition:="K^(9) intersect N_P",
      conditional_on_157bb_isolation:=true,
      G9_kernel_inside_E4:="E^4 by the perfect-versus-solvable Goursat argument",
      image_in_V4:="V^4",
      f2_rank:=24,order:=2^24,generator_count:=24,
      generators:=D972BDWords,
      proof:="the 24 replayed source words are the four copies of the six pinned V basis elements; their E^4 images are in V^4, their P^4 and G9^4 images are identity, and the direct-product/Goursat lemma gives equality"),
    construction:=rec(
      method:="metabelian commutator-of-commutators law plus coordinate E solver",
      law:="[[a,b],[c,d]]",
      h9_derived_series_length:=Length(D972BDG9SeriesOrders),
      h9_law_identity_replayed:=true,
      coordinate_solver_order:=Size(D972BDE),
      coordinate_solver_count:=4,
      solver_generator_count:=13,
      full_joint_preimage_calls:=0,
      fast_records:=D972BDFastRecords),
    b4_action:=rec(
      pure_generator_labels:=D972BDLabels,
      pure_generator_block_matrices:=D972BDPureMatrices,
      B3_stabilizer_theta_matrix:=D972BDThetaMatrix,
      B3_stabilizer_tau_matrix:=D972BDTauMatrix,
      S4_coordinate_transpositions:=[[2,1,3,4],[1,3,2,4],[1,2,4,3]],
      composition_factors:=[rec(dimension:=24,multiplicity:=1,
        irreducible:=true,description:="Induced four-coordinate V-module under P^4 semidirect S4")],
      action_description:="PB4 acts blockwise through P^4; B4/PB4=S4 permutes the four coordinates with the pinned B3 stabilizer twists"),
    proof_level:="GAP coordinate-E law preimages plus independent Python replay; rank equality uses Goursat",
    input_boundary:=rec(C_E_C_P_C_M_isolation_from_157bb:=true,
      isolation_not_reproved_here:=true,cofinal_B4_B_claimed:=false,
      Ihara_claimed:=false));
  D972BDWrite(D972BDOutput,D972BDReceipt);;
  Print("D972_CORE_INTERSECTION_V2_FINAL status=CORE_INTERSECTION_V2_COMPUTED output=",
    D972BDOutput," E4=",D972BDGEOrder," P4=",D972BDGPOrder,
    " H9four=",D972BDG9ImageOrder," rank=24\n");
  Print("D972_CORE_INTERSECTION_V2_FINAL\n");
fi;;
