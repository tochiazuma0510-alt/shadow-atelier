#############################################################################
## d972_b4_fc8_a5four_v1.g
##
## FC-8*: an exact, structural certificate for the A5^4 chief factor below
## the frozen PB4 coarse roof.  No element enumeration of A5^4 is used.
#############################################################################

Read("search/gaplib_common.g");;
if LoadPackage("json")<>true then Error("157do: GAP json package unavailable"); fi;;

D972FCProducer := "search/d972_b4_fc8_a5four_v1.g";;
D972FCSchema := "d972-b4-fc8-a5four/v1";;
D972FCTerminal := "FC8_A5_FOUR_CHIEF_CROSSCHECKED";;
D972FCCorePath := "search/d972_d972core_c2six_intersection_v2.g";;
D972FCCoreSHA := "577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c";;
D972FCMapsPath := "search/certs/d972_b4_marity_reduction_maps_v1.json";;
D972FCMapsSHA := "6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2";;
D972FCMapsCheckerPath := "search/check_d972_b4_marity_reduction_maps_v1.py";;
D972FCMapsCheckerSHA := "eb87e9d42ecde979b82a31beec8fdedea3e221a55d4881f8a71dbaffc2a7a032";;
D972FCA1Path := "certificates/A1.v2.json";;
D972FCA1SHA := "24c42967f260a4dad2fb89b52f5709388549bebb37664b798a1502a5ef6d8a02";;
D972FCA1SettledPath := "certificates/A1.v2.2.json";;
D972FCA1SettledSHA := "a348b5044e98a7c64711b507d43015c780d16606a66482fe33ccd2bfd3eee8d6";;
D972FCT40Path := "docs/notes/fullverbal_tower_screening_v1.md";;
D972FCT40SHA := "9e69838f923a77385ce191244c57e88dc24d95b3c9ae9d5d0f9b0cd0c148cad8";;
D972FCCheckedIoMarker :=
  "D972_B4_FC8_CHECKED_IO_SELFTEST_PASS backend=OutputTextFile readback=true";;
D972FCCheckedIoMarkerCount := 0;;

D972FCRequireSHA := function(path,sha,label)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157do: missing pinned ",label,": ",path); fi;
  got:=HexSHA256(raw);;
  if got<>sha then Error("157do: pinned ",label," SHA drift: ",got); fi;
  return rec(path:=path,sha256:=sha,bytes:=Length(raw));
end;;

D972FCEscape := function(s)
  local z;
  z:=ReplacedString(s,"\\","\\\\");;
  z:=ReplacedString(z,"\"","\\\"");;
  z:=ReplacedString(z,"\n","\\n");;
  z:=ReplacedString(z,"\r","\\r");;
  z:=ReplacedString(z,"\t","\\t");;
  return z;
end;;

D972FCJson := function(x)
  local names,parts,n;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",D972FCEscape(x),"\""); fi;
  if IsRecord(x) then
    names:=ShallowCopy(RecNames(x));; Sort(names);; parts:=[];;
    for n in names do
      Add(parts,Concatenation(D972FCJson(n),":",D972FCJson(x.(n))));
    od;
    return Concatenation("{",JoinStringsWithSeparator(parts,","),"}");
  fi;
  if IsList(x) then
    return Concatenation("[",JoinStringsWithSeparator(List(x,D972FCJson),","),"]");
  fi;
  Error("157do: unsupported JSON value");
end;;

D972FCCheckedWrite := function(path,obj)
  local expected,f,raw;
  expected:=Concatenation(D972FCJson(obj),"\n");;
  f:=OutputTextFile(path,false);;
  if f=fail then Error("157do: cannot open output ",path); fi;
  SetPrintFormattingStatus(f,false);; PrintTo(f,expected);; CloseStream(f);;
  raw:=StringFile(path);;
  if raw=fail or raw<>expected then Error("157do: checked-write readback mismatch"); fi;
end;;

D972FCUnknown := function(path,pins,token,phase,detail)
  D972FCCheckedWrite(path,rec(schema:=D972FCSchema,status:=token,
    terminal_token:=token,terminal:=false,pins:=pins,phase:=phase,
    detail:=detail,chief_factor_claimed:=false,B4_B_claimed:=false));;
  Print(token," phase=",phase," detail=",detail,"\n");
end;;

D972FCReadJson := function(path,sha,label)
  local pin,raw,obj;
  pin:=D972FCRequireSHA(path,sha,label);; raw:=StringFile(path);;
  obj:=JsonStringToGap(raw);;
  if obj=fail then Error("157do: invalid pinned JSON ",label); fi;
  return rec(pin:=pin,obj:=obj);
end;;

#############################################################################
## Signed words, the Fadell-Neuwirth PB presentation, and faithful Artin.
#############################################################################

D972FCReduce := function(w)
  local out,x;
  out:=[];;
  for x in w do
    if x=0 then Error("157do: zero signed letter"); fi;
    if Length(out)>0 and out[Length(out)]=-x then Remove(out,Length(out));
    else Add(out,x); fi;
  od;
  return out;
end;;

D972FCInv := w -> D972FCReduce(List(Reversed(w),x->-x));;

D972FCSubstitute := function(w,imgs)
  local out,x;
  out:=[];;
  for x in w do
    if AbsInt(x)>Length(imgs) then Error("157do: substitution alphabet drift"); fi;
    if x>0 then Append(out,imgs[x]); else Append(out,D972FCInv(imgs[-x])); fi;
    out:=D972FCReduce(out);;
  od;
  return out;
end;;

D972FCArtinStep := function(rank,letter)
  local imgs,i;
  imgs:=List([1..rank],i->[i]);; i:=AbsInt(letter);;
  if i<1 or i>=rank then Error("157do: Artin generator range"); fi;
  if letter>0 then imgs[i]:=[i,i+1,-i];; imgs[i+1]:=[i];;
  else imgs[i]:=[i+1];; imgs[i+1]:=[-(i+1),i,i+1];; fi;
  return imgs;
end;;

D972FCArtinImages := function(rank,word)
  local imgs,x,step;
  imgs:=List([1..rank],i->[i]);;
  for x in word do
    step:=D972FCArtinStep(rank,x);;
    imgs:=List(imgs,w->D972FCSubstitute(w,step));;
  od;
  return imgs;
end;;

D972FCPairs := function(rank)
  local out,i,j;
  out:=[];;
  for i in [1..rank-1] do for j in [i+1..rank] do Add(out,[i,j]); od; od;
  return out;
end;;

D972FCPairIndex := function(rank,pair)
  local pos;
  pos:=Position(D972FCPairs(rank),pair);;
  if pos=fail then Error("157do: bad pure pair"); fi;
  return pos;
end;;

D972FCAijBraid := function(i,j)
  local w,k;
  w:=[];;
  if j-i>1 then for k in Reversed([i+1..j-1]) do Add(w,k); od; fi;
  Add(w,i);; Add(w,i);;
  if j-i>1 then for k in [i+1..j-1] do Add(w,-k); od; fi;
  return w;
end;;

D972FCExpandPure := function(rank,w)
  return D972FCSubstitute(w,List(D972FCPairs(rank),p->D972FCAijBraid(p[1],p[2])));
end;;

D972FCPureRelations := function(rank)
  local pairs,rels,oldrels,oldpairs,mapold,p,k,g,h,act,kmaps;
  if rank=2 then return [];; fi;
  pairs:=D972FCPairs(rank);; oldpairs:=D972FCPairs(rank-1);;
  oldrels:=D972FCPureRelations(rank-1);;
  mapold:=List(oldpairs,p->D972FCPairIndex(rank,p));;
  rels:=List(oldrels,w->D972FCSubstitute(w,List(mapold,x->[x])));;
  kmaps:=List([1..rank-1],k->[D972FCPairIndex(rank,[k,rank])]);;
  for p in oldpairs do
    g:=D972FCPairIndex(rank,p);;
    act:=D972FCArtinImages(rank-1,D972FCAijBraid(p[1],p[2]));;
    for k in [1..rank-1] do
      h:=D972FCPairIndex(rank,[k,rank]);;
      Add(rels,D972FCReduce(Concatenation([-g,h,g],
        D972FCInv(D972FCSubstitute(act[k],kmaps)))));
    od;
  od;
  return rels;
end;;

D972FCEval := function(w,gens)
  local out,x;
  out:=One(gens[1]);;
  for x in w do
    if x>0 then out:=out*gens[x];; else out:=out*gens[-x]^-1;; fi;
  od;
  return out;
end;;

D972FCTupleEval := function(w,rows)
  return List([1..Length(rows[1])],c->D972FCEval(w,List(rows,r->r[c])));
end;;

D972FCPermRow := function(p,n) return List([1..n],i->i^p); end;;
D972FCTupleRows := function(rows,n)
  return List(rows,row->List(row,p->D972FCPermRow(p,n)));
end;;

D972FCBlockTuple := function(vals,width)
  local row,off,v,i;
  row:=[];; off:=0;;
  for v in vals do
    for i in [1..width] do Add(row,off+i^v); od;
    off:=off+width;;
  od;
  return PermList(row);
end;;

D972FCBasisTuple := function(coord,value,one)
  local out,i;
  out:=[];; for i in [1..4] do
    if i=coord then Add(out,value); else Add(out,one); fi;
  od;
  return out;
end;;

D972FCApplyFactorAuto := function(value,sourceByOutput,conjugators)
  return List([1..4],c->value[sourceByOutput[c]]^conjugators[c]);
end;;

D972FCParityBit := function(p)
  if SignPerm(p)=-1 then return 1; fi;
  return 0;
end;;

#############################################################################
## Main exact construction.
#############################################################################

D972FCMain := function(output)
  local t,pins,mapsData,a1Data,a12Data,maps,a1,a12,expectedMaps,X,Y,Z,A5,S5,
    target,byDeletion,rhoRows,rels,one5,relationValues,projectionOrders,
    supportPairs,supportWords,supportRecords,i,j,c,w,value,normalOrder,
    actionWords,actionPublic,actionInternal,s,acted,matches,d,u,conj,
    sourceByOutput,expectedSource,conjugators,s5Elements,basis,bv,left,right,
    factorPerms,actionGroup,
    cbPairs,outerBits,totalBit,permBit,nonzeroPairs,cbImageOrder,
    coreOutput,P,G9,H9,h9Order,pRows,gRows,pProjectionOrders,pSupportRecords,
    pValue,pNormalOrders,pPrimeSupport,hPrimeSupport,q0Order,qPrimeSupport,
    coarseBindings,receipt,token,status,chief,goursat,unknownReason;

  t:=Runtime();;
  pins:=rec(
    core_producer:=D972FCRequireSHA(D972FCCorePath,D972FCCoreSHA,"coarse core"),
    deletion_fixture:=D972FCRequireSHA(D972FCMapsPath,D972FCMapsSHA,"deletion fixture"),
    deletion_checker:=D972FCRequireSHA(D972FCMapsCheckerPath,D972FCMapsCheckerSHA,"deletion checker"),
    a5_marking:=D972FCRequireSHA(D972FCA1Path,D972FCA1SHA,"A5 marking"),
    a5_settled_extension:=D972FCRequireSHA(D972FCA1SettledPath,D972FCA1SettledSHA,"A5 extension"),
    t40_screening:=D972FCRequireSHA(D972FCT40Path,D972FCT40SHA,"T-40 screening"));;
  mapsData:=D972FCReadJson(D972FCMapsPath,D972FCMapsSHA,"deletion fixture");;
  a1Data:=D972FCReadJson(D972FCA1Path,D972FCA1SHA,"A5 marking");;
  a12Data:=D972FCReadJson(D972FCA1SettledPath,D972FCA1SettledSHA,"A5 extension");;
  maps:=mapsData.obj;; a1:=a1Data.obj;; a12:=a12Data.obj;;
  expectedMaps:=[
    [[],[],[],[1],[2],[3]],
    [[],[1],[2],[],[],[3]],
    [[1],[],[2],[],[3],[]],
    [[1],[2],[],[3],[],[]] ];;
  if maps.schema<>"d972-b4-marity-reduction-maps/v1" or
     maps.status<>"PROVED_BY_CANONICAL_STRAND_FORGETTING" or
     List(maps.maps,r->r.generator_images)<>expectedMaps or
     List(maps.maps,r->r.deleted_strand)<>[1,2,3,4] then
    Error("157do: pinned four deletion table drift");
  fi;
  if a1.target_definition.marking.X<>"a t^{-1} = (1 3 2 4 5)" or
     a1.target_definition.marking.Y<>"t X t^{-1} = (1 3 4 5 2)" or
     a1.target_definition.quotient<>"A5" or a12.aut_group.size<>120 then
    Error("157do: pinned A5 marking/provenance drift");
  fi;

  X:=(1,3,2,4,5);; Y:=(1,3,4,5,2);; Z:=X^-1*Y^-1;;
  A5:=Group(X,Y);; S5:=SymmetricGroup(5);; one5:=One(A5);;
  if Size(A5)<>60 or not IsSimpleGroup(A5) or not IsPerfectGroup(A5) or
     not IsSubgroup(S5,A5) then
    D972FCUnknown(output,pins,"FC8_UNKNOWN_A5","A5",
      "canonical marking did not generate simple perfect A5 of order 60");; return;
  fi;
  target:=[X,Z,Y];;
  byDeletion:=List(maps.maps,row->
    List(row.generator_images,w->D972FCEval(w,target)));;
  rhoRows:=List([1..6],j->List([1..4],i->byDeletion[i][j]));;

  rels:=D972FCPureRelations(4);;
  if Length(rels)<>11 then Error("157do: PB4 presentation relation count drift"); fi;
  if ForAny(rels,r->D972FCArtinImages(4,D972FCExpandPure(4,r))<>
       List([1..4],i->[i])) then Error("157do: faithful PB4 presentation replay failed"); fi;
  relationValues:=List(rels,r->D972FCTupleEval(r,rhoRows));;
  if ForAny(relationValues,row->ForAny(row,v->v<>one5)) then
    D972FCUnknown(output,pins,"FC8_UNKNOWN_RHOA_RELATIONS","rhoA_relations",
      "one of the eleven PB4 relators has nonidentity A5^4 image");; return;
  fi;
  projectionOrders:=List([1..4],c->Size(Group(List(rhoRows,r->r[c]))));;
  if projectionOrders<>[60,60,60,60] then
    D972FCUnknown(output,pins,"FC8_UNKNOWN_RHOA_SURJECTIVITY","rhoA_projections",
      "a coordinate projection is not A5");; return;
  fi;

  supportPairs:=[[4,6],[2,6],[1,5],[1,4]];;
  supportWords:=List(supportPairs,p->[-p[1],-p[2],p[1],p[2]]);;
  supportRecords:=[];;
  for c in [1..4] do
    w:=supportWords[c];; value:=D972FCTupleEval(w,rhoRows);;
    if value[c]=one5 or ForAny([1..4],i->i<>c and value[i]<>one5) then
      D972FCUnknown(output,pins,"FC8_UNKNOWN_RHOA_SURJECTIVITY","rhoA_single_support",
        "a literal commutator is not nontrivial single-support");; return;
    fi;
    normalOrder:=Size(NormalClosure(A5,Group(value[c])));;
    if normalOrder<>60 then
      D972FCUnknown(output,pins,"FC8_UNKNOWN_RHOA_SURJECTIVITY","rhoA_normal_closure",
        "single-support value does not normally generate A5");; return;
    fi;
    Add(supportRecords,rec(coordinate:=c,source_word:=w,
      images:=List(value,p->D972FCPermRow(p,5)),nontrivial:=true,
      normal_closure_order:=normalOrder));;
  od;

  # Canonical order (x12,x13,x14,x23,x24,x34), action c_(sigma_i^-1).
  actionWords:=[
    [[1],[-1,4,1],[-1,5,1],[2],[3],[6]],
    [[-4,2,4],[1],[3],[4],[-4,6,4],[5]],
    [[1],[-6,3,6],[2],[-6,5,6],[4],[6]] ];;
  actionPublic:=[];; actionInternal:=[];; s5Elements:=Elements(S5);;
  for s in [1..3] do
    for j in [1..6] do
      if D972FCArtinImages(4,Concatenation([-s],
           D972FCAijBraid(D972FCPairs(4)[j][1],D972FCPairs(4)[j][2]),[s]))<>
         D972FCArtinImages(4,D972FCExpandPure(4,actionWords[s][j])) then
        D972FCUnknown(output,pins,"FC8_UNKNOWN_B4_ACTION","faithful_Artin",
          "source conjugation word failed faithful Artin replay");; return;
      fi;
    od;
    acted:=List([1..6],j->D972FCTupleEval(actionWords[s][j],rhoRows));;
    sourceByOutput:=[];; conjugators:=[];;
    for c in [1..4] do
      matches:=[];;
      for d in [1..4] do
        for conj in s5Elements do
          if ForAll([1..6],j->acted[j][c]=rhoRows[j][d]^conj) then
            Add(matches,[d,conj]);
          fi;
        od;
      od;
      if Length(matches)<>1 then
        D972FCUnknown(output,pins,"FC8_UNKNOWN_B4_ACTION","factor_transport",
          "induced A5 factor transport is missing or nonunique");; return;
      fi;
      Add(sourceByOutput,matches[1][1]);; Add(conjugators,matches[1][2]);;
    od;
    expectedSource:=[1,2,3,4];;
    expectedSource[s]:=s+1;; expectedSource[s+1]:=s;;
    if sourceByOutput<>expectedSource then
      D972FCUnknown(output,pins,"FC8_UNKNOWN_B4_ACTION","factor_permutation",
        "factor action is not the standard adjacent strand transposition");; return;
    fi;
    Add(actionInternal,rec(source:=sourceByOutput,conjugators:=conjugators));;
    Add(actionPublic,rec(sigma_index:=s,orientation:="sigma_i^-1 * value * sigma_i",
      source_generator_images:=actionWords[s],
      source_coordinate_by_output:=sourceByOutput,
      factor_permutation:=sourceByOutput,
      conjugators_S5:=List(conjugators,p->D972FCPermRow(p,5)),
      exact_transport_images:=D972FCTupleRows(acted,5)));;
  od;

  basis:=[];;
  for c in [1..4] do
    Add(basis,D972FCBasisTuple(c,X,one5));;
    Add(basis,D972FCBasisTuple(c,Y,one5));;
  od;
  for bv in basis do
    left:=D972FCApplyFactorAuto(D972FCApplyFactorAuto(
      D972FCApplyFactorAuto(bv,actionInternal[1].source,actionInternal[1].conjugators),
      actionInternal[2].source,actionInternal[2].conjugators),
      actionInternal[1].source,actionInternal[1].conjugators);;
    right:=D972FCApplyFactorAuto(D972FCApplyFactorAuto(
      D972FCApplyFactorAuto(bv,actionInternal[2].source,actionInternal[2].conjugators),
      actionInternal[1].source,actionInternal[1].conjugators),
      actionInternal[2].source,actionInternal[2].conjugators);;
    if left<>right then D972FCUnknown(output,pins,"FC8_UNKNOWN_B4_ACTION",
      "induced_relations","sigma1 sigma2 braid failed");; return; fi;
    left:=D972FCApplyFactorAuto(D972FCApplyFactorAuto(
      D972FCApplyFactorAuto(bv,actionInternal[2].source,actionInternal[2].conjugators),
      actionInternal[3].source,actionInternal[3].conjugators),
      actionInternal[2].source,actionInternal[2].conjugators);;
    right:=D972FCApplyFactorAuto(D972FCApplyFactorAuto(
      D972FCApplyFactorAuto(bv,actionInternal[3].source,actionInternal[3].conjugators),
      actionInternal[2].source,actionInternal[2].conjugators),
      actionInternal[3].source,actionInternal[3].conjugators);;
    if left<>right then D972FCUnknown(output,pins,"FC8_UNKNOWN_B4_ACTION",
      "induced_relations","sigma2 sigma3 braid failed");; return; fi;
    left:=D972FCApplyFactorAuto(D972FCApplyFactorAuto(bv,
      actionInternal[1].source,actionInternal[1].conjugators),
      actionInternal[3].source,actionInternal[3].conjugators);;
    right:=D972FCApplyFactorAuto(D972FCApplyFactorAuto(bv,
      actionInternal[3].source,actionInternal[3].conjugators),
      actionInternal[1].source,actionInternal[1].conjugators);;
    if left<>right then D972FCUnknown(output,pins,"FC8_UNKNOWN_B4_ACTION",
      "induced_relations","sigma1 sigma3 commutation failed");; return; fi;
  od;
  factorPerms:=List(actionInternal,a->PermList(a.source));;
  actionGroup:=Group(factorPerms);;
  if Size(actionGroup)<>24 or not IsTransitive(actionGroup,[1..4]) then
    D972FCUnknown(output,pins,"FC8_UNKNOWN_B4_ACTION","factor_transitivity",
      "factor permutation image is not transitive S4");; return;
  fi;

  # T-40 / CB-3: the two abelian characters of C2 wr S4 cannot be independent.
  cbPairs:=[];;
  for s in [1..3] do
    outerBits:=List(actionInternal[s].conjugators,D972FCParityBit);;
    totalBit:=Sum(outerBits) mod 2;; permBit:=D972FCParityBit(factorPerms[s]);;
    Add(cbPairs,[totalBit,permBit]);;
    actionPublic[s].outer_A5_bits:=outerBits;;
    actionPublic[s].wreath_abelianization_pair:=[totalBit,permBit];;
  od;
  nonzeroPairs:=Filtered(cbPairs,p->p<>[0,0]);;
  if Length(nonzeroPairs)=0 then cbImageOrder:=1;;
  elif ForAll(nonzeroPairs,p->p=nonzeroPairs[1]) then cbImageOrder:=2;;
  else cbImageOrder:=4;; fi;
  if cbImageOrder>2 then
    D972FCUnknown(output,pins,"FC8_UNKNOWN_CB3_COUPLING","FC8_double_star_CB3",
      "the two C2 characters generate a noncyclic C2^2 image");; return;
  fi;

  # Load the authenticated coarse core in the same GAP process.  We use only
  # its exact marked P/G9 rows and its already-pinned source construction.
  coreOutput:=Filename(DirectoryTemporary(),"d972_fc8_a5four_core.json");;
  D972_BD_MODE:="full";; D972_BD_OUTPUT:=coreOutput;; Read(D972FCCorePath);;
  if D972BDMapsSha<>D972FCMapsSHA or D972BDSourceSha<>
     "648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9" then
    Error("157do: coarse core transitive pin drift");
  fi;
  P:=D972BDP;; G9:=D972BDG9;; H9:=D972BDG9Image;;
  pRows:=D972BDTuplePRows;; gRows:=D972BDTupleG9Rows;;
  h9Order:=D972BDG9ImageOrder;;
  if Size(P)<>504 or not IsPerfectGroup(P) or
     Size(G9)<>2916 or not IsSolvableGroup(G9) or
     D972BDG9SeriesOrders<>[2916,729,1] or
     ForAny(gRows,row->ForAny(row,g->not (g in G9))) or
     h9Order<>32*3^24 then
    D972FCUnknown(output,pins,"FC8_UNKNOWN_Q0_CONTRACT","Q0_factors",
      "frozen P/G9/H9 order, perfectness, solvability, or block membership failed");; return;
  fi;
  pProjectionOrders:=List([1..4],c->Size(Group(List(pRows,r->r[c]))));;
  if pProjectionOrders<>[504,504,504,504] then
    D972FCUnknown(output,pins,"FC8_UNKNOWN_Q0_CONTRACT","Q0_P4_projection",
      "a frozen P4 projection is not PSL(2,8)");; return;
  fi;
  pSupportRecords:=[];; pNormalOrders:=[];;
  for c in [1..4] do
    pValue:=D972FCTupleEval(supportWords[c],pRows);;
    if pValue[c]=One(P) or ForAny([1..4],i->i<>c and pValue[i]<>One(P)) then
      D972FCUnknown(output,pins,"FC8_UNKNOWN_Q0_CONTRACT","Q0_P4_single_support",
        "a frozen P4 support word failed");; return;
    fi;
    normalOrder:=Size(NormalClosure(P,Group(pValue[c])));;
    if normalOrder<>504 then
      D972FCUnknown(output,pins,"FC8_UNKNOWN_Q0_CONTRACT","Q0_P4_normal_closure",
        "a P single-support value does not normally generate P");; return;
    fi;
    Add(pNormalOrders,normalOrder);;
    Add(pSupportRecords,rec(coordinate:=c,source_word:=supportWords[c],
      images:=List(pValue,p->D972FCPermRow(p,9)),
      normal_closure_order:=normalOrder));;
  od;
  pPrimeSupport:=Set(FactorsInt(Size(P)));;
  hPrimeSupport:=Set(FactorsInt(h9Order));;
  q0Order:=Size(P)^4*h9Order;; qPrimeSupport:=Set(FactorsInt(q0Order));;
  if pPrimeSupport<>[2,3,7] or hPrimeSupport<>[2,3] or
     qPrimeSupport<>[2,3,7] or 5 in qPrimeSupport then
    D972FCUnknown(output,pins,"FC8_UNKNOWN_Q0_CONTRACT","Q0_prime_support",
      "Q0 prime support does not exclude 5");; return;
  fi;
  coarseBindings:=List([1..6],j->rec(
    source_generator:=["x12","x13","x14","x23","x24","x34"][j],
    P4_blocks:=List(pRows[j],p->D972FCPermRow(p,9)),
    H9_blocks:=List(gRows[j],p->D972FCPermRow(p,27)),
    A5_four_blocks:=List(rhoRows[j],p->D972FCPermRow(p,5))));;

  goursat:=rec(
    joint_map_source:="PB4 with the same six canonical marked generators",
    rho0_surjective:=true,
    rho0_projection_P4_surjective_by_single_support:=true,
    rho0_projection_H9_surjective_by_definition:=true,
    rho0_P4_H9_common_quotient_trivial:=true,
    rho0_product_reason:="P^4 is perfect and H9 is solvable, so a common quotient is both perfect and solvable and hence trivial",
    rhoA_surjective:=true,
    no_nontrivial_common_quotient_Q0_A5four:=true,
    no_common_reason:="every nontrivial quotient of A5^4 has order divisible by 5, while 5 does not divide |Q0|",
    theorem:="Goursat subdirect-product lemma",
    joint_image_is_full_Q0_times_A5four:=true);;
  chief:=rec(
    K_definition:="K = ker(rho0) intersection ker(rhoA)",
    M_definition:="M = ker(rho0)",
    restriction_kernel:="ker(rhoA restricted to M) = K",
    restriction_surjective_by_joint_product:=true,
    first_isomorphism:="M/K isomorphic to A5^4",
    S:="A5",t:=4,factor_order:=60,
    direct_power_normal_subgroup_lemma:="every normal subgroup of a direct power of a nonabelian simple group is a product of coordinate factors",
    finite_premises:=rec(nonabelian:=true,simple:=true,four_factors:=true),
    B4_factor_action_transitive:=true,
    B4_stable_factor_subsets:=[[],[1,2,3,4]],
    B4_chief:=true,
    registered_factor_isolatedness_used_as_premise:=false,
    isolated_audit_window_source:="Corollary 3.5 (FV-5); not computed here");;

  token:=D972FCTerminal;; status:=token;; unknownReason:=fail;;
  receipt:=rec(schema:=D972FCSchema,status:=status,terminal_token:=token,
    pins:=pins,
    source_contract:=rec(group:="PB4",generator_order:=["x12","x13","x14","x23","x24","x34"],
      deletion_target_order:=["y12","y13","y23"],
      free_A5_images:=["X","X^-1 Y^-1","Y"],
      deletion_maps:=expectedMaps),
    a5:=rec(name:="A5",degree:=5,order:=60,simple:=true,perfect:=true,
      automorphism_group:="S5",automorphism_group_order:=120,
      X:=D972FCPermRow(X,5),Y:=D972FCPermRow(Y,5),Z:=D972FCPermRow(Z,5)),
    pb4_presentation:=rec(method:="recursive Fadell-Neuwirth presentation plus faithful Artin replay",
      pairs:=D972FCPairs(4),relation_count:=Length(rels),relations:=rels,
      relation_images_identity:=true),
    rhoA:=rec(marked_images:=D972FCTupleRows(rhoRows,5),
      projection_orders:=projectionOrders,
      single_support_witnesses:=supportRecords,
      no_A5four_enumeration:=true,
      image_is_A5_four:=true),
    b4_action:=rec(orientation:="c_(sigma_i^-1): value maps to sigma_i^-1 value sigma_i",
      generators:=actionPublic,faithful_source_action_replay:=true,
      exact_transport_all_six_rows:=true,induced_braid_relations:=true,
      induced_distant_commutation:=true,factor_action_group_order:=Size(actionGroup),
      factor_action_standard_S4:=true,factor_action_transitive:=true),
    fc8_double_star_cb3:=rec(target:="Out(A5)^4 semidirect S4 = C2 wreath S4",
      wreath_abelianization:="C2^2: total outer parity and S4 sign",
      generator_character_pairs:=cbPairs,image_order:=cbImageOrder,
      image_cyclic:=cbImageOrder<=2,characters_independent:=false,
      q_abelianization_cyclic_premise:=true,checker_must_recompute_parities:=true),
    rho0:=rec(name:="frozen actual coarse B4 roof Q0=P^4 x H9",
      order_decimal:=String(q0Order),prime_support:=qPrimeSupport,
      P:=rec(name:="PSL(2,8)",degree:=9,order:=504,perfect:=true,
        simple:=IsSimpleGroup(P),prime_support:=pPrimeSupport,
        X:=D972FCPermRow(D972BDPX,9),Y:=D972FCPermRow(D972BDPY,9)),
      G9:=rec(degree:=27,order:=2916,solvable:=true,
        derived_series_orders:=[2916,729,1],X:=D972FCPermRow(D972BDX9,27),
        Y:=D972FCPermRow(D972BDY9,27)),
      H9:=rec(degree:=108,order_decimal:=String(h9Order),solvable:=true,
        derived_order_decimal:=String(3^24),abelian_quotient_order:=32,
        prime_support:=hPrimeSupport,marked_blocks:=D972FCTupleRows(gRows,27),
        construction:="image of the six marked PB4 generators in G9^4",
        checker_method:="G9-derived C9^3 coordinates, mod-3 Nakayama rank 12, and quotient image order 32"),
      P4:=rec(order_decimal:=String(504^4),projection_orders:=pProjectionOrders,
        marked_blocks:=D972FCTupleRows(pRows,9),
        single_support_witnesses:=pSupportRecords,
        perfect:=true,image_is_P_four:=true),
      marked_same_source_bindings:=coarseBindings,
      B4_normal_kernel_frozen_roof_premise:=true,
      product_certificate:=goursat),
    goursat:=goursat,chief_factor:=chief,
    missing_ledger:=rec(
      FV5_registered_window_isolation_required:=false,
      FV5_audit_window_isolated_by_Corollary_3_5:=true,
      D4_five_primary_friendly:="MISSING",
      D6_five_primary_friendly:="MISSING",
      five_primary_reason:="5 divides |A5| and introduces a new friendly-condition prime",
      K_isolatedness:="NOT_ESTABLISHED_AND_NOT_REQUIRED_BY_FV5",
      OBS_NA:="NOT_SUPPLIED",D1:="NOT_SUPPLIED",NA_5:="NOT_SUPPLIED",
      full_verbal_tower_switch:="NOT_RECOMMENDED_AND_NOT_USED"),
    performance:=rec(runtime_ms:=Runtime()-t,Elements_A5four_calls:=0,
      A5four_Cayley_tables:=0,generic_A5four_group_size_calls:=0,
      closures_inside_A5:=4,closures_inside_P:=4,
      bounded_S5_elements:=120,coarse_core_reads:=1),
    implication:="For K=M intersection ker(rhoA), M/K is a B4-chief factor A5^4; no B4-B conclusion");;
  D972FCCheckedWrite(output,receipt);;
  Print(D972FCTerminal," output=",output," runtime_ms=",Runtime()-t,
    " H9_order=",h9Order," CB3_image_order=",cbImageOrder,"\n");
end;;

if IsBound(D972_B4_FC8_SELFTEST) and D972_B4_FC8_SELFTEST=true then
  D972FCCheckedIoMarkerCount:=D972FCCheckedIoMarkerCount+1;;
  D972FCIoPath:=Filename(DirectoryTemporary(),"d972_fc8_checked_io.json");;
  D972FCCheckedWrite(D972FCIoPath,rec(schema:="io-selftest",empty:=[]));;
  Print(D972FCCheckedIoMarker,"\n");
elif IsBound(D972_B4_FC8_RUN) and D972_B4_FC8_RUN=true then
  if not IsBound(D972_B4_FC8_OUTPUT) then
    D972_B4_FC8_OUTPUT:="ci/out/d972_b4_fc8_a5four_v1.json";;
  fi;
  D972FCMain(D972_B4_FC8_OUTPUT);;
else
  Error("157do: set exactly one of D972_B4_FC8_SELFTEST or D972_B4_FC8_RUN");
fi;
