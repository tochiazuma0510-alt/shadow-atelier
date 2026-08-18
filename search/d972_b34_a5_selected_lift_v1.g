#############################################################################
## d972_b34_a5_selected_lift_v1.g
##
## Complete fixed-roof fibre through the concrete FC-8 A5^4 layer.
## The two upstream receipts are regenerated and independently checked by the
## same-job driver.  This producer performs no ANUPQ/PB5 computation.
#############################################################################

Read("search/gaplib_common.g");;
if LoadPackage("json")<>true then Error("157dp: GAP json package unavailable"); fi;;
if LoadPackage("polycyclic")<>true then Error("157dp: GAP polycyclic package unavailable"); fi;;

D972A5LProducer := "search/d972_b34_a5_selected_lift_v1.g";;
D972A5LSchema := "d972-b34-a5-selected-lift/v1";;
D972A5LQ3Path := "ci/out/d972_b345_q3_chief_v1.json";;
D972A5LQ3HistoricalSHA := "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972A5LFC8Path := "ci/out/d972_b4_fc8_a5four_v1.json";;
D972A5LFC8HistoricalSHA := "558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584";;
D972A5LWordsPath := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972A5LWordsSHA := "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972A5LAxisPath := "sol/luna_reply_157cp_c5_surgery_torsor_chief.md";;
D972A5LAxisSHA := "59c96e7d62a20af4207f715df8e2927a8fc373e1f12e8f3be70e535d8afe5347";;
D972A5LQ3ProducerPath := "search/d972_b345_q3_chief_v1.g";;
D972A5LQ3ProducerSHA := "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755";;
D972A5LQ3CheckerPath := "search/check_d972_b345_q3_chief_v1.py";;
D972A5LQ3CheckerSHA := "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73";;
D972A5LQ3DriverPath := "search/d972_b345_q3_gha_driver_v1.g";;
D972A5LQ3DriverSHA := "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831";;
D972A5LFC8ProducerPath := "search/d972_b4_fc8_a5four_v1.g";;
D972A5LFC8ProducerSHA := "d482315bb0abc54e9707651a8fb73e73a4a569f101f51c232b76a73fbf57e804";;
D972A5LFC8CheckerPath := "search/check_d972_b4_fc8_a5four_v1.py";;
D972A5LFC8CheckerSHA := "5b2f54b7adbddbff914fe2d28786327df9109d4e91fa53b1be03114eed5a65d4";;
D972A5LFC8DriverPath := "search/d972_b4_fc8_a5four_gha_driver_v1.g";;
D972A5LFC8DriverSHA := "806d8bfa32ecb1f24f0873147da9e13b56fa171294f081cdd321894b77c545af";;
D972A5LSelectedWord := [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1];;
D972A5LPositive := "B34_A5_LAYER_FIXED_OUTSIDE_ROOF_LIFT_CROSSCHECKED";;
D972A5LNegative := "B4_A_FIXED_OUTSIDE_ROOF_FIBRE_OBSTRUCTION_CROSSCHECKED";;
D972A5LUnknown := "B34_A5_LAYER_UNKNOWN_RESOURCE";;
D972A5LCheckedIoMarker :=
  "D972_B34_A5_SELECTED_LIFT_CHECKED_IO_SELFTEST_PASS";;
D972A5LCheckedIoMarkerCount := 0;;

D972A5LRequireSHA := function(path,sha,label)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157dp: missing ",label,": ",path); fi;
  got:=HexSHA256(raw);;
  if got<>sha then Error("157dp: SHA drift ",label," got=",got); fi;
  return rec(path:=path,sha256:=sha,bytes:=Length(raw));
end;;

D972A5LEscape := function(s)
  local z;
  z:=ReplacedString(s,"\\","\\\\");;
  z:=ReplacedString(z,"\"","\\\"");;
  z:=ReplacedString(z,"\n","\\n");;
  z:=ReplacedString(z,"\r","\\r");;
  z:=ReplacedString(z,"\t","\\t");;
  return z;
end;;

D972A5LJson := function(x)
  local names,parts,n;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",D972A5LEscape(x),"\""); fi;
  if IsRecord(x) then
    names:=ShallowCopy(RecNames(x));; Sort(names);; parts:=[];;
    for n in names do
      Add(parts,Concatenation(D972A5LJson(n),":",D972A5LJson(x.(n))));
    od;
    return Concatenation("{",JoinStringsWithSeparator(parts,","),"}");
  fi;
  if IsList(x) then
    return Concatenation("[",JoinStringsWithSeparator(List(x,D972A5LJson),","),"]");
  fi;
  Error("157dp: unsupported JSON value");
end;;

D972A5LDigest := x -> HexSHA256(D972A5LJson(x));;

D972A5LCheckedWrite := function(path,obj)
  local expected,f,actual;
  expected:=Concatenation(D972A5LJson(obj),"\n");;
  f:=OutputTextFile(path,false);;
  if f=fail then Error("157dp: cannot open output ",path); fi;
  SetPrintFormattingStatus(f,false);; PrintTo(f,expected);; CloseStream(f);;
  actual:=StringFile(path);;
  if actual=fail or actual<>expected then Error("157dp: checked write drift"); fi;
end;;

D972A5LReadJSON := function(path,label)
  local raw,obj;
  raw:=StringFile(path);;
  if raw=fail then Error("157dp: missing generated ",label); fi;
  obj:=JsonStringToGap(raw);;
  if obj=fail then Error("157dp: malformed generated ",label); fi;
  return rec(obj:=obj,sha256:=HexSHA256(raw),bytes:=Length(raw));
end;;

#############################################################################
## Words, permutations, and literal maps.
#############################################################################

D972A5LReduce := function(w)
  local out,x;
  out:=[];;
  for x in w do
    if x=0 then Error("157dp: zero word letter"); fi;
    if Length(out)>0 and out[Length(out)]=-x then Remove(out,Length(out));
    else Add(out,x); fi;
  od;
  return out;
end;;

D972A5LInv := w -> D972A5LReduce(List(Reversed(w),x->-x));;

D972A5LSub := function(w,imgs)
  local out,x;
  out:=[];;
  for x in w do
    if AbsInt(x)>Length(imgs) then Error("157dp: substitution index"); fi;
    if x>0 then Append(out,imgs[x]); else Append(out,D972A5LInv(imgs[-x])); fi;
    out:=D972A5LReduce(out);;
  od;
  return out;
end;;

D972A5LEval := function(w,gens)
  local z,x;
  z:=One(gens[1]);;
  for x in w do
    if x>0 then z:=z*gens[x];; else z:=z*gens[-x]^-1;; fi;
  od;
  return z;
end;;

D972A5LPP := function(xs)
  local z,i;
  if Length(xs)=0 then Error("157dp: empty paper product"); fi;
  z:=One(xs[1]);;
  for i in Reversed([1..Length(xs)]) do z:=z*xs[i];; od;
  return z;
end;;

D972A5LPairList := function(rank)
  local out,i,j;
  out:=[];;
  for i in [1..rank-1] do for j in [i+1..rank] do Add(out,[i,j]); od; od;
  return out;
end;;

D972A5LPairIndex := function(rank,pair)
  local p;
  p:=Position(D972A5LPairList(rank),pair);;
  if p=fail then Error("157dp: pair index"); fi;
  return p;
end;;

D972A5LCofaceGenerator := function(rank,slot,pair)
  local i,j,ii,jj;
  i:=pair[1];; j:=pair[2];;
  if slot=0 then return [D972A5LPairIndex(rank+1,[i+1,j+1])]; fi;
  if slot=rank+1 then return [D972A5LPairIndex(rank+1,[i,j])]; fi;
  if slot<1 or slot>rank then Error("157dp: coface slot"); fi;
  if i=slot then
    return [D972A5LPairIndex(rank+1,[slot,j+1]),
      D972A5LPairIndex(rank+1,[slot+1,j+1])];
  elif j=slot then
    return [D972A5LPairIndex(rank+1,[i,slot]),
      D972A5LPairIndex(rank+1,[i,slot+1])];
  fi;
  ii:=i;; jj:=j;; if ii>slot then ii:=ii+1; fi;;
  if jj>slot then jj:=jj+1; fi;;
  return [D972A5LPairIndex(rank+1,[ii,jj])];
end;;

D972A5LCofaces := rank -> List([0..rank+1],s->List(D972A5LPairList(rank),
  p->D972A5LCofaceGenerator(rank,s,p)));;

D972A5LDeleteGenerator := function(rank,strand,pair)
  local i,j;
  i:=pair[1];; j:=pair[2];;
  if strand=i or strand=j then return []; fi;
  if i>strand then i:=i-1;; fi;; if j>strand then j:=j-1;; fi;
  return [D972A5LPairIndex(rank-1,[i,j])];
end;;

D972A5LDeletions := rank -> List([1..rank],s->List(D972A5LPairList(rank),
  p->D972A5LDeleteGenerator(rank,s,p)));;

D972A5LComposeMaps := function(first,second)
  return List(first,w->D972A5LSub(w,second));
end;;

D972A5LPermRow := function(p,d)
  return List([1..d],i->i^p);
end;;

D972A5LBlockPerm := function(perms,degrees)
  local row,off,i,j;
  if Length(perms)<>Length(degrees) then Error("157dp: block width"); fi;
  row:=[];; off:=0;;
  for i in [1..Length(perms)] do
    for j in [1..degrees[i]] do Add(row,off+(j^perms[i])); od;
    off:=off+degrees[i];;
  od;
  return PermList(row);
end;;

D972A5LPermFromRow := row -> PermList(row);;

D972A5LPairs := function(g)
  return [[g[1],g[4]],[g[4],g[6]],[D972A5LPP([g[2],g[4]]),g[6]],
    [D972A5LPP([g[1],g[2]]),D972A5LPP([g[5],g[6]])],
    [g[1],D972A5LPP([g[4],g[5]])]];
end;;

D972A5LHexPairs := function(x,y)
  local z,u;
  z:=D972A5LPP([x,y])^-1;; u:=D972A5LPP([y,x])^-1;;
  return [[x,y],[x,z],[y,z],[u,x],[u,y]];
end;;

D972A5LHexFromValues := function(v,m,x,y)
  local z,u;
  if Length(v)<>5 then Error("157dp: hex width"); fi;
  z:=D972A5LPP([x,y])^-1;; u:=D972A5LPP([y,x])^-1;;
  return [D972A5LPP([y^m,v[1],x^m,v[2]^-1,z^m,v[3]]),
    D972A5LPP([v[4]^-1,x^m,v[1]^-1,y^m,v[5],u^m])];
end;;

D972A5LPentFromValues := function(v)
  if Length(v)<>5 then Error("157dp: pentagon width"); fi;
  return D972A5LPP([D972A5LPP([v[5],v[3]])^-1,v[2],v[4],v[1]]);
end;;

D972A5LContext := function(w,pairs)
  return List(pairs,p->D972A5LEval(w,p));
end;;

D972A5LContextMul := function(a,b)
  return List([1..Length(a)],i->a[i]*b[i]);
end;;

D972A5LContextInv := a -> List(a,x->x^-1);;

#############################################################################
## Reconstruct an exported exponent-three pc group without ANUPQ.
#############################################################################

D972A5LSyllables := function(coords)
  local out,i;
  out:=[];;
  for i in [1..Length(coords)] do
    if coords[i]<>0 then Add(out,i);; Add(out,coords[i]); fi;
  od;
  return out;
end;;

D972A5LCoordElt := function(gens,coords)
  local z,i;
  z:=One(gens[1]);;
  for i in [1..Length(coords)] do if coords[i]<>0 then z:=z*gens[i]^coords[i];; fi; od;
  return z;
end;;

D972A5LImportPC := function(r,label)
  local n,coll,i,row,G,gens,marks,unit;
  n:=r.generator_count;;
  if n<>Length(r.relative_orders) or n>175 then Error("157dp: pc width ",label); fi;
  if ForAny(r.relative_orders,x->x<>3) then Error("157dp: pc order ",label); fi;
  coll:=FromTheLeftCollector(n);;
  for i in [1..n] do
    SetRelativeOrder(coll,i,r.relative_orders[i]);;
    SetPower(coll,i,D972A5LSyllables(r.power_relations[i]));;
  od;
  for row in r.conjugate_relations do
    SetConjugate(coll,row.i,row.j,D972A5LSyllables(row.coords));
  od;
  for row in r.inverse_conjugate_relations do
    SetConjugate(coll,row.i,-row.j,D972A5LSyllables(row.coords));
  od;
  UpdatePolycyclicCollector(coll);;
  if IsConfluent(coll)<>true then Error("157dp: nonconfluent pc receipt ",label); fi;
  G:=PcpGroupByCollectorNC(coll);; gens:=GeneratorsOfGroup(G);;
  marks:=List(r.marked_generators,x->D972A5LCoordElt(gens,x.coords));;
  if Size(G)<>Int(r.order_decimal) then Error("157dp: pc size ",label); fi;
  for i in [1..n] do
    unit:=List([1..n],j->0);; unit[i]:=1;;
    if List(Exponents(gens[i]),Int)<>unit then
      Error("157dp: defining collector coordinate basis ",label);
    fi;
    if D972A5LCoordElt(gens,r.inverses[i])<>gens[i]^-1 then
      Error("157dp: pc inverse ",label);
    fi;
  od;
  for i in [1..Length(marks)] do
    if List(Exponents(marks[i]),Int)<>r.marked_generators[i].coords or
       List(Exponents(marks[i]^-1),Int)<>r.marked_generators[i].inverse_coords then
      Error("157dp: marked defining-basis coordinates ",label);
    fi;
  od;
  for row in r.conjugate_relations do
    if gens[row.i]^gens[row.j]<>D972A5LCoordElt(gens,row.coords) then
      Error("157dp: pc conjugate ",label);
    fi;
  od;
  for row in r.inverse_conjugate_relations do
    if gens[row.i]^(gens[row.j]^-1)<>D972A5LCoordElt(gens,row.coords) then
      Error("157dp: pc inverse conjugate ",label);
    fi;
  od;
  return rec(group:=G,gens:=gens,marks:=marks,generator_count:=n);
end;;

#############################################################################
## A5/D1 construction and the small-factor section.
#############################################################################

D972A5LD1 := function(fc)
  local X,Y,Z,A5,c34,d4,a18,comps,rows,i,j,map,imgs,ord,support,
    fullMarks,D,DF,der,cyclicCounts,ontoCount,c,compactMarks,compact,hom,
    pb4marks,derivedPB4,receipt,c23,pb2Words,pb2New,compactDer;
  X:=D972A5LPermFromRow(fc.a5.X);; Y:=D972A5LPermFromRow(fc.a5.Y);;
  Z:=D972A5LPermFromRow(fc.a5.Z);; A5:=Group(X,Y);;
  if Size(A5)<>60 or not IsSimpleGroup(A5) or not IsPerfectGroup(A5) or
     Z<>X^-1*Y^-1 then Error("157dp: A5 marking/type drift"); fi;
  c34:=D972A5LCofaces(3);; d4:=D972A5LDeletions(4);;
  a18:=List([4,0,1,2,3],s->c34[s+1]);; comps:=[];; rows:=[];;
  ontoCount:=0;; cyclicCounts:=[0,0,0];;
  for i in [1..5] do for j in [1..4] do
    map:=D972A5LComposeMaps(a18[i],d4[j]);;
    imgs:=List(map,w->D972A5LEval(w,[X,Z,Y]));;
    ord:=Size(Group(imgs));; support:=Filtered([1..3],k->not IsOne(imgs[k]));;
    if ord=60 then
      if [imgs[1],imgs[3],imgs[2]]<>[X,Y,Z] then
        Error("157dp: onto composite marking drift");
      fi;
      ontoCount:=ontoCount+1;;
    elif ord=5 then
      if Length(support)<>1 then Error("157dp: cyclic composite support"); fi;
      cyclicCounts[support[1]]:=cyclicCounts[support[1]]+1;;
    else Error("157dp: composite image is neither A5 nor C5"); fi;
    Add(comps,rec(coface_index:=i,deletion_strand:=j,map:=map,
      image_order:=ord,support:=support,
      marked_rows:=List(imgs,p->D972A5LPermRow(p,5))));
  od; od;
  if ontoCount<>8 or cyclicCounts<>[4,4,4] then Error("157dp: 8/12 D1 drift"); fi;
  fullMarks:=List([1..3],k->D972A5LBlockPerm(
    List(comps,r->D972A5LPermFromRow(r.marked_rows[k])),List([1..20],z->5)));;
  D:=Group(fullMarks);; DF:=Group(fullMarks[1],fullMarks[3]);;
  der:=DerivedSubgroup(DF);;
  if Size(D)<>7500 or Size(DF)<>1500 or Size(der)<>60 then
    Error("157dp: D/D_F/derived orders drift");
  fi;
  c:=(6,7,8,9,10);;
  compactMarks:=[D972A5LBlockPerm([X,(1,2,3,4,5),()],[5,5,5]),
    D972A5LBlockPerm([Z,(),()],[5,5,5]),
    D972A5LBlockPerm([Y,(),(1,2,3,4,5)],[5,5,5])];;
  compact:=Group(compactMarks[1],compactMarks[3]);;
  compactDer:=DerivedSubgroup(compact);;
  if Size(compact)<>1500 or Size(compactDer)<>60 then
    Error("157dp: compact D_F drift");
  fi;
  hom:=GroupHomomorphismByImages(compact,DF,[compactMarks[1],compactMarks[3]],
    [fullMarks[1],fullMarks[3]]);;
  if hom=fail or not IsBijective(hom) then Error("157dp: compact/full D_F mismatch"); fi;
  derivedPB4:=[];;
  for i in [1..6] do
    Add(derivedPB4,D972A5LBlockPerm(List(d4,m->
      D972A5LEval(m[i],[X,Z,Y])),[5,5,5,5]));
  od;
  pb4marks:=List(fc.rhoA.marked_images,row->D972A5LBlockPerm(
    List(row,D972A5LPermFromRow),[5,5,5,5]));;
  if List(derivedPB4,p->D972A5LPermRow(p,20))<>
     List(pb4marks,p->D972A5LPermRow(p,20)) then Error("157dp: rhoA replay drift"); fi;
  c23:=D972A5LCofaces(2);; pb2Words:=List(c23,m->m[1]);;
  pb2New:=D972A5LBlockPerm(List(pb2Words,w->D972A5LEval(w,fullMarks)),
    [100,100,100,100]);;
  if Order(pb2New)<>5 then Error("157dp: relative m factor is not C5"); fi;
  receipt:=rec(a18_names:=["phi_123","phi_234","phi_12_3_4","phi_1_23_4","phi_1_2_34"],
    a18_maps:=a18,deletion_maps:=d4,twenty_composites:=comps,
    onto_component_count:=ontoCount,cyclic_source_class_counts:=cyclicCounts,
    PB3_joint_image_order:=7500,F2_image_order:=1500,F2_derived_order:=60,
    PB2_coface_words:=pb2Words,PB2_relative_factor_order:=5,
    compact_marked_rows:=List(compactMarks,p->D972A5LPermRow(p,15)),
    full_F2_marked_rows:=List([fullMarks[1],fullMarks[3]],p->D972A5LPermRow(p,100)),
    full_PB3_marked_rows:=List(fullMarks,p->D972A5LPermRow(p,100)),
    rhoA_marked_rows:=List(pb4marks,p->D972A5LPermRow(p,20)),
    compact_to_full_bijective:=true);
  return rec(X:=X,Y:=Y,Z:=Z,A5:=A5,a18:=a18,d4:=d4,comps:=comps,
    fullMarks:=fullMarks,D:=D,DF:=DF,derived:=der,compactMarks:=compactMarks,
    compact:=compact,compactDerived:=compactDer,pb4marks:=pb4marks,
    pb2Words:=pb2Words,pb2New:=pb2New,receipt:=receipt);
end;;

D972A5LDFBFS := function(DF,x,y)
  local states,parents,edges,words,q,pos,e,v,i;
  states:=[One(DF)];; parents:=[0];; edges:=[0];; words:=[[]];; q:=1;;
  while q<=Length(states) do
    for e in [1,-1,2,-2] do
      if e=1 then v:=states[q]*x;; elif e=-1 then v:=states[q]*x^-1;;
      elif e=2 then v:=states[q]*y;; else v:=states[q]*y^-1;; fi;
      pos:=Position(states,v);;
      if pos=fail then
        Add(states,v);; Add(parents,q);; Add(edges,e);;
        Add(words,D972A5LReduce(Concatenation(words[q],[e])));;
        if Length(states)>1500 then Error("157dp: D_F BFS cap"); fi;
      fi;
    od;
    q:=q+1;;
  od;
  if Length(states)<>1500 then Error("157dp: D_F BFS incomplete"); fi;
  return rec(states:=states,parents:=parents,edges:=edges,words:=words);
end;;

D972A5LNormalSections := function(d1,oldx,oldy,oldContexts)
  local nx,ny,relWords,relVals,normalCheck,dfbfs,selected,H,candWords,
    candVals,i,j,v,w,oldMain,normalRecords,states,parents,edges,q,e,pos,
    vals,word,genContexts,ctxNames,contexts,ctxState,fullState,pentState,
    hexState,records,edgeIndex,g,edgeVal,edgeCtx,k,hOrder;
  nx:=Order(oldx);; ny:=Order(oldy);;
  if nx<>18 or ny<>18 then Error("157dp: H_ord generator order drift"); fi;
  relWords:=[List([1..nx],z->1),List([1..ny],z->2)];;
  if ForAny(relWords,w->not IsOne(D972A5LEval(w,[oldx,oldy]))) then
    Error("157dp: source power relator not old-trivial");
  fi;
  relVals:=List(relWords,w->D972A5LEval(w,[d1.compactMarks[1],d1.compactMarks[3]]));;
  normalCheck:=NormalClosure(d1.compact,Subgroup(d1.compact,relVals));;
  if Size(normalCheck)<>1500 then Error("157dp: power relators do not normally generate D_F"); fi;
  dfbfs:=D972A5LDFBFS(d1.compact,d1.compactMarks[1],d1.compactMarks[3]);;
  selected:=[];; H:=Group(());; hOrder:=1;;
  for i in [1..Length(dfbfs.states)] do
    for j in [1..2] do
      v:=relVals[j]^dfbfs.states[i];;
      if not v in H then
        w:=D972A5LReduce(Concatenation(D972A5LInv(dfbfs.words[i]),
          relWords[j],dfbfs.words[i]));;
        Add(selected,rec(base_relator:=j,conjugator_index:=i,word:=w,value:=v));;
        H:=ClosureGroup(H,v);;
        hOrder:=Size(H);;
        if Length(selected)>20 then Error("157dp: normal generator cap"); fi;
        if hOrder=1500 then break; fi;
      fi;
    od;
    if hOrder=1500 then break; fi;
  od;
  if hOrder<>1500 or not IsNormal(d1.compact,H) then
    Error("157dp: tracked normal closure incomplete");
  fi;
  ctxNames:=["old_q0_main","old_b2_main","old_q0_hex","old_b2_hex",
    "old_q4_pent","old_pi4_pent","new_full_main","new_full_hex","new_a5four_pent"];;
  contexts:=oldContexts;; normalRecords:=[];;
  for g in selected do
    oldMain:=[];;
    for k in [1..Length(contexts)] do
      if IsList(contexts[k]) and Length(contexts[k])>0 and IsList(contexts[k][1]) then
        Add(oldMain,D972A5LContext(g.word,contexts[k]));
      else
        Add(oldMain,D972A5LEval(g.word,contexts[k]));
      fi;
    od;
    if not IsOne(oldMain[1]) or not IsOne(oldMain[2]) or
       ForAny(oldMain[3],x->not IsOne(x)) or ForAny(oldMain[4],x->not IsOne(x)) or
       ForAny(oldMain[5],x->not IsOne(x)) or ForAny(oldMain[6],x->not IsOne(x)) then
      Error("157dp: tracked section generator is not typed over q3");
    fi;
    Add(normalRecords,rec(base_relator:=g.base_relator,
      conjugator_index:=g.conjugator_index,word:=g.word,
      compact_key:=D972A5LPermRow(g.value,15),context_values_internal:=oldMain));
  od;
  states:=[One(d1.compact)];; parents:=[0];; edges:=[0];;
  fullState:=[One(d1.DF)];;
  hexState:=[List([1..5],z->One(d1.D))];;
  pentState:=[List([1..5],z->One(Group(d1.pb4marks)))];;
  q:=1;;
  while q<=Length(states) do
    for e in Concatenation([1..Length(normalRecords)],List([1..Length(normalRecords)],z->-z)) do
      edgeIndex:=AbsInt(e);; g:=normalRecords[edgeIndex];;
      if e>0 then edgeVal:=selected[edgeIndex].value;;
      else edgeVal:=selected[edgeIndex].value^-1;; fi;
      v:=states[q]*edgeVal;; pos:=Position(states,v);;
      if pos=fail then
        Add(states,v);; Add(parents,q);; Add(edges,e);;
        if e>0 then
          Add(fullState,fullState[q]*g.context_values_internal[7]);
          Add(hexState,D972A5LContextMul(hexState[q],g.context_values_internal[8]));
          Add(pentState,D972A5LContextMul(pentState[q],g.context_values_internal[9]));
        else
          Add(fullState,fullState[q]*g.context_values_internal[7]^-1);
          Add(hexState,D972A5LContextMul(hexState[q],D972A5LContextInv(g.context_values_internal[8])));
          Add(pentState,D972A5LContextMul(pentState[q],D972A5LContextInv(g.context_values_internal[9])));
        fi;
        if Length(states)>1500 then Error("157dp: section BFS cap"); fi;
      fi;
    od;
    q:=q+1;;
  od;
  if Length(states)<>1500 or Length(Set(states))<>1500 then
    Error("157dp: section BFS coverage");
  fi;
  records:=List([1..1500],i->rec(index:=i,parent:=parents[i],edge:=edges[i],
    key:=D972A5LPermRow(states[i],15)));
  for g in normalRecords do Unbind(g.context_values_internal); od;
  return rec(normal_generators:=normalRecords,records:=records,states:=states,
    fullState:=fullState,hexState:=hexState,pentState:=pentState,
    source_power_relators:=relWords,old_generator_orders:=[nx,ny],
    normal_closure_order:=1500,normal_generator_count:=Length(normalRecords),
    full_coverage:=true);
end;;

D972A5LExpandSection := function(index,records,gens)
  local edges,w,i,e;
  edges:=[];; i:=index;;
  while i<>1 do
    if i<1 or records[i].parent>=i then Error("157dp: section parent DAG"); fi;
    Add(edges,records[i].edge);; i:=records[i].parent;
  od;
  w:=[];;
  for e in Reversed(edges) do
    if e>0 then Append(w,gens[e].word); else Append(w,D972A5LInv(gens[-e].word)); fi;
    w:=D972A5LReduce(w);;
  od;
  return w;
end;;

#############################################################################
## Bind the frozen 972-key power orbit to the accepted pure-axis theorem.
## This deliberately does not consume the q3 `arithmetic_outside_*` boolean.
#############################################################################

D972A5LOutsideCertificate := function(q3,wordsObj)
  local powers,orbit,expectedRows,outsideExponents,outsideRows,i,row,c,h,c2,
    complementGenerators,complements,bindings,outsideBindings;
  if wordsObj.schema<>"d972-b4-word-key-artifact/v1" or wordsObj.count<>972 or
     Length(wordsObj.rows)<>972 or Length(Set(List(wordsObj.rows,r->r[2])))<>972 then
    Error("157dp: frozen 972-key universe drift");
  fi;
  powers:=q3.canonical_roof_powers;; orbit:=powers.normalized_orbit;;
  expectedRows:=[1,19,37,55,73,10,28,46,64,1];;
  outsideExponents:=[1,2,4,5,7,8];;
  outsideRows:=[19,37,73,10,46,64];;
  if powers.coarse_key_cache_size<>972 or powers.frozen_rows_evaluated_once<>true or
     powers.canonicalized_each_step<>true or powers.literal_power_words_retained<>false or
     powers.normalized_orbit_first_repeat<>9 or
     powers.normalized_orbit_n0_n8_distinct<>true or
     powers.normalized_orbit_n9_identity<>true or
     powers.outside_residues_complete_mod9<>outsideExponents or Length(orbit)<>10 then
    Error("157dp: normalized 972-key orbit contract drift");
  fi;
  bindings:=[];;
  for i in [1..10] do
    if orbit[i].exponent<>i-1 or orbit[i].row_index<>expectedRows[i] then
      Error("157dp: normalized orbit exponent/row drift");
    fi;
    row:=wordsObj.rows[expectedRows[i]];;
    if orbit[i].key<>row[2] or orbit[i].word<>row[3] then
      Error("157dp: normalized orbit is not bound to frozen 972 rows");
    fi;
    Add(bindings,rec(exponent:=i-1,row_index:=expectedRows[i],
      key_sha256:=D972A5LDigest(row[2]),word_sha256:=D972A5LDigest(row[3])));
  od;
  if Length(Set(List(orbit{[1..9]},r->r.key)))<>9 or orbit[10].key<>orbit[1].key or
     Length(powers.rows)<>6 or List(powers.rows,r->r.exponent)<>outsideExponents or
     List(powers.rows,r->r.row_index)<>outsideRows then
    Error("157dp: normalized orbit completeness drift");
  fi;
  for i in [1..6] do
    row:=wordsObj.rows[outsideRows[i]];;
    if powers.rows[i].key<>row[2] or powers.rows[i].word<>row[3] then
      Error("157dp: outside orbit row is not frozen");
    fi;
  od;
  if orbit[3].word<>D972A5LSelectedWord or orbit[3].key<>wordsObj.rows[37][2] then
    Error("157dp: row37 is not the normalized square of row19");
  fi;
  # In X/W ~= S3 x C6, e1 is the nontrivial C3 element.  A/W projects
  # to one of the three C2 complements; the C6 sign does not affect this
  # membership test.  Thus e1^2 lies in none of the possible arithmetic
  # complements, with no fabricated six-copy model table.
  c:=(1,2,3);; h:=(1,2);; c2:=c^2;;
  complementGenerators:=List([0..2],r->h^(c^r));;
  complements:=List(complementGenerators,g->Group(g));;
  if Size(Group(c,h))<>6 or Order(c2)<>3 or
     Length(Set(List(complements,H->Set(Elements(H)))))<>3 or
     ForAny(complements,H->c2 in H) then
    Error("157dp: S3 pure-axis/complement replay drift");
  fi;
  outsideBindings:=List([1..6],i->bindings[outsideExponents[i]+1]);;
  return rec(method:="frozen normalized 972-key GT-compose orbit plus X/W=S3 x C6 pure-axis theorem",
    theorem_source_sha256:=D972A5LAxisSHA,producer_boolean_from_q3_used:=false,
    frozen_972_count:=972,normalized_orbit_bindings:=bindings,
    normalized_orbit_row_indices:=expectedRows,normalized_orbit_first_repeat:=9,
    outside_residues_complete_mod9:=outsideExponents,outside_orbit_bindings:=outsideBindings,
    base_axis_exponent:=1,base_axis_row_index:=19,selected_exponent:=2,
    selected_row_index:=37,row37_equals_e1_squared_by_orbit:=true,
    quotient_structure:="X/W ~= S3 x C6",W_order:=27,X_order:=972,A_order:=324,
    S3_axis_e1_row:=D972A5LPermRow(c,3),S3_axis_e1_square_row:=D972A5LPermRow(c2,3),
    S3_arithmetic_complement_generator_rows:=List(complementGenerators,g->D972A5LPermRow(g,3)),
    S3_complement_orders:=[2,2,2],C6_sign_choices:=2,
    C6_sign_irrelevant_to_S3_membership:=true,
    e1_square_in_any_arithmetic_complement:=false,
    exponent_not_divisible_by_three:=(2 mod 3<>0),outside_A:=true);
end;;

D972A5LPositiveCanary := function(candidate,outerWord,m,d1,pc3,pc4,
    q0x,q0y,b2x,b2y,q4marks,pi4marks,sections,j,combined)
  local q0Hex,b2Hex,q4Pent,pi4Pent,newHex,newPent,dq,db,hq,hb,pq,pp,
    nc,nf,nh,np,expected,payload;
  q0Hex:=D972A5LHexPairs(q0x,q0y);; b2Hex:=D972A5LHexPairs(b2x,b2y);;
  q4Pent:=D972A5LPairs(q4marks);; pi4Pent:=D972A5LPairs(pi4marks);;
  newHex:=D972A5LHexPairs(d1.fullMarks[1],d1.fullMarks[3]);;
  newPent:=D972A5LPairs(d1.pb4marks);;
  dq:=D972A5LEval(candidate,[q0x,q0y]);;
  db:=D972A5LEval(candidate,[b2x,b2y]);;
  hq:=D972A5LContext(candidate,q0Hex);; hb:=D972A5LContext(candidate,b2Hex);;
  pq:=D972A5LContext(candidate,q4Pent);; pp:=D972A5LContext(candidate,pi4Pent);;
  nc:=D972A5LEval(candidate,[d1.compactMarks[1],d1.compactMarks[3]]);;
  nf:=D972A5LEval(candidate,[d1.fullMarks[1],d1.fullMarks[3]]);;
  nh:=D972A5LContext(candidate,newHex);; np:=D972A5LContext(candidate,newPent);;
  if dq<>D972A5LEval(outerWord,[q0x,q0y]) or
     db<>D972A5LEval(outerWord,[b2x,b2y]) or
     hq<>D972A5LContext(outerWord,q0Hex) or hb<>D972A5LContext(outerWord,b2Hex) or
     pq<>D972A5LContext(outerWord,q4Pent) or pp<>D972A5LContext(outerWord,pi4Pent) or
     nc<>combined then Error("157dp: materialized candidate old/compact context drift"); fi;
  expected:=D972A5LEval(outerWord,[d1.fullMarks[1],d1.fullMarks[3]])*
    sections.fullState[j];;
  if nf<>expected or
     nh<>D972A5LContextMul(D972A5LContext(outerWord,newHex),sections.hexState[j]) or
     np<>D972A5LContextMul(D972A5LContext(outerWord,newPent),sections.pentState[j]) then
    Error("157dp: materialized candidate new context drift");
  fi;
  if not (ForAll(D972A5LHexFromValues(hq,m,q0x,q0y),IsOne) and
          ForAll(D972A5LHexFromValues(hb,m,b2x,b2y),IsOne) and
          IsOne(D972A5LPentFromValues(pq)) and IsOne(D972A5LPentFromValues(pp)) and
          ForAll(D972A5LHexFromValues(nh,m,d1.fullMarks[1],d1.fullMarks[3]),IsOne) and
          IsOne(D972A5LPentFromValues(np))) then
    Error("157dp: materialized candidate literal identity drift");
  fi;
  payload:=rec(m:=m,lambda:=2*m+1,
    old_q0_main:=D972A5LPermRow(dq,36),
    old_b2_main:=List(Exponents(db),Int),
    old_q0_hex:=List(hq,x->D972A5LPermRow(x,36)),
    old_b2_hex:=List(hb,x->List(Exponents(x),Int)),
    old_q4_pent:=List(pq,x->D972A5LPermRow(x,144)),
    old_pi4_pent:=List(pp,x->List(Exponents(x),Int)),
    new_compact_main:=D972A5LPermRow(nc,15),new_full_main:=D972A5LPermRow(nf,100),
    new_hex:=List(nh,x->D972A5LPermRow(x,100)),
    new_pent:=List(np,x->D972A5LPermRow(x,20)));
  return rec(all_cached_contexts_match:=true,old_hexagon_direct:=true,
    old_pentagon_direct:=true,new_hexagon_direct:=true,new_pentagon_direct:=true,
    settlement_used:=false,context_sha256:=D972A5LDigest(payload));
end;;

#############################################################################
## Complete compact scan.
#############################################################################

D972A5LAddCode := function(rle,code)
  if Length(rle)>0 and rle[Length(rle)].code=code then
    rle[Length(rle)].count:=rle[Length(rle)].count+1;;
  else Add(rle,rec(code:=code,count:=1)); fi;
end;;

D972A5LScan := function(q3,d1,pc3,pc4,Q0,q0x,q0y,B2,b2x,b2y,biso,bperm,Q4,q4marks,
    pi4marks,sections,wordsObj)
  local base,corr,outerWords,outer,i,w,q0HexPairs,b2HexPairs,q4PentPairs,
    p4PentPairs,newHexPairs,newPentPairs,outerRows,q0Der,b2Der,oldGate,
    mainQ,mainB,hq,hb,pq,pp,oldHex,oldPent,oldCharm,oldOnto,oldRoof,
    P,G9,pX,pY,gX,gY,pv,gv,conjP,conjG,conjB,ontoPKeys,ontoPVals,
    ontoGKeys,ontoGVals,ontoBKeys,ontoBVals,pos,newBaseMain,newBaseHex,
    newBasePent,shift,s,m,u,j,combined,charm,newHexVals,newPentVals,
    newHex,newPent,newOnto,ontoKeys,ontoVals,candidateIndex,rle,codes,
    counts,selected,corrWord,candidateWord,terminal,evaluated,pairVals,
    code,allComplete,universeContract,selectedRow,roofRow,outsideCertificate,
    mWords,jointPB2,q3PB2,coarsePB2,pb2Q,pb2B,q3PB2Degree,
    sourceRows,selectedCorrection,settlementDiagnostic,bpermDegree,
    corrValues,b2Elements,derivedFlags,derivedIndices,derivedSliceCounts,
    combinedStates,periodValues,positiveCanary,mNewKeys;
  base:=D972A5LSelectedWord;; corr:=q3.correction_fibre.records;;
  if Length(corr)<>27 or corr[1].word<>[] then Error("157dp: q3 fibre order"); fi;
  if q3.correction_fibre.certificate.enumerated_count<>27 or
     q3.correction_fibre.certificate.projection_kernel_order<>27 or
     q3.correction_fibre.certificate.direct_product<>true then
    Error("157dp: q3 correction-fibre certificate drift");
  fi;
  corrValues:=List(corr,r->D972A5LEval(r.word,[b2x,b2y]));;
  b2Elements:=Set(Elements(B2));;
  if Length(Set(corrValues))<>27 or Set(corrValues)<>b2Elements then
    Error("157dp: q3 correction words do not cover B(2,3)");
  fi;
  for i in [1..27] do
    if D972A5LCoordElt(pc3.gens,corr[i].ambient_Pi3_coords)<>corrValues[i] or
       not IsOne(D972A5LEval(corr[i].word,[q0x,q0y])) then
      Error("157dp: q3 correction word/coordinate/coarse replay drift");
    fi;
  od;
  outerWords:=List(corr,r->D972A5LReduce(Concatenation(base,r.word)));;
  Q0:=Group(q0x,q0y);; q0Der:=DerivedSubgroup(Q0);; b2Der:=DerivedSubgroup(B2);;
  q0HexPairs:=D972A5LHexPairs(q0x,q0y);; b2HexPairs:=D972A5LHexPairs(b2x,b2y);;
  periodValues:=[];;
  for pairVals in q0HexPairs do Append(periodValues,pairVals);; od;
  for pairVals in b2HexPairs do Append(periodValues,pairVals);; od;
  if ForAny(periodValues,x->not IsOne(x^18)) then
    Error("157dp: old hexagon marking period does not divide 18");
  fi;
  q4PentPairs:=D972A5LPairs(q4marks);; p4PentPairs:=D972A5LPairs(pi4marks);;
  newHexPairs:=D972A5LHexPairs(d1.fullMarks[1],d1.fullMarks[3]);;
  newPentPairs:=D972A5LPairs(d1.pb4marks);;
  P:=Group(List(q3.coarse_models.P.marked_permutations,D972A5LPermFromRow));;
  G9:=Group(List(q3.coarse_models.G9.marked_permutations,D972A5LPermFromRow));;
  pX:=D972A5LPermFromRow(q3.coarse_models.P.marked_permutations[1]);;
  pY:=D972A5LPermFromRow(q3.coarse_models.P.marked_permutations[2]);;
  gX:=D972A5LPermFromRow(q3.coarse_models.G9.marked_permutations[1]);;
  gY:=D972A5LPermFromRow(q3.coarse_models.G9.marked_permutations[2]);;
  if q0x<>D972A5LBlockPerm([pX,gX],[9,27]) or
     q0y<>D972A5LBlockPerm([pY,gY],[9,27]) or
     Size(P)<>504 or not IsPerfectGroup(P) or Size(G9)<>2916 or
     not IsSolvableGroup(G9) or Size(q0Der)<>367416 or Size(b2Der)<>3 then
    Error("157dp: old source structural orders");
  fi;
  ontoPKeys:=[];; ontoPVals:=[];; ontoGKeys:=[];; ontoGVals:=[];;
  ontoBKeys:=[];; ontoBVals:=[];; outerRows:=[];;
  for i in [1..27] do
    w:=outerWords[i];; mainQ:=D972A5LEval(w,[q0x,q0y]);;
    mainB:=D972A5LEval(w,[b2x,b2y]);;
    hq:=D972A5LContext(w,q0HexPairs);; hb:=D972A5LContext(w,b2HexPairs);;
    pq:=D972A5LContext(w,q4PentPairs);; pp:=D972A5LContext(w,p4PentPairs);;
    oldRoof:=D972A5LEval(corr[i].word,[q0x,q0y])=One(Q0);;
    oldCharm:=mainQ in q0Der and mainB in b2Der;;
    oldHex:=ForAll(D972A5LHexFromValues(hq,0,q0x,q0y),IsOne) and
      ForAll(D972A5LHexFromValues(hb,0,b2x,b2y),IsOne);;
    oldPent:=IsOne(D972A5LPentFromValues(pq)) and IsOne(D972A5LPentFromValues(pp));;
    pv:=D972A5LPermFromRow(D972A5LPermRow(mainQ,36){[1..9]});;
    gv:=D972A5LPermFromRow(List([1..27],j->D972A5LPermRow(mainQ,36)[9+j]-9));;
    conjP:=D972A5LPP([pv^-1,pY,pv]);; conjG:=D972A5LPP([gv^-1,gY,gv]);;
    pos:=Position(ontoPKeys,pv);;
    if pos=fail then Add(ontoPKeys,pv);; Add(ontoPVals,Size(Group(pX,conjP))=504);;
      pos:=Length(ontoPVals);; fi;
    oldOnto:=ontoPVals[pos];;
    pos:=Position(ontoGKeys,gv);;
    if pos=fail then Add(ontoGKeys,gv);; Add(ontoGVals,Size(Group(gX,conjG))=2916);;
      pos:=Length(ontoGVals);; fi;
    oldOnto:=oldOnto and ontoGVals[pos];;
    conjB:=D972A5LPP([mainB^-1,b2y,mainB]);; pos:=Position(ontoBKeys,mainB);;
    if pos=fail then Add(ontoBKeys,mainB);; Add(ontoBVals,Size(Group(b2x,conjB))=27);;
      pos:=Length(ontoBVals);; fi;
    oldOnto:=oldOnto and ontoBVals[pos];;
    Add(outerRows,rec(index:=i,q_coords:=corr[i].q_coords,
      word_sha256:=D972A5LDigest(w),old_roof:=oldRoof,old_charming:=oldCharm,
      old_hexagon:=oldHex,old_pentagon:=oldPent,old_onto:=oldOnto,
      main_compact:=D972A5LEval(w,[d1.compactMarks[1],d1.compactMarks[3]]),
      hex_new:=D972A5LContext(w,newHexPairs),pent_new:=D972A5LContext(w,newPentPairs)));
  od;
  # Independently close the q3 marking coordinate: adding B(2,3) does not
  # enlarge order 18; adding the A5 layer enlarges it to 90 with kernel C5.
  pb2Q:=List(d1.pb2Words,w->D972A5LEval(w,[q0x,(),q0y]));;
  pb2B:=List(d1.pb2Words,w->D972A5LEval(w,[b2x,One(B2),b2y]));;
  coarsePB2:=D972A5LBlockPerm(pb2Q,List([1..4],z->36));;
  bpermDegree:=LargestMovedPoint(bperm);;
  q3PB2:=D972A5LBlockPerm(Concatenation(pb2Q,List(pb2B,x->Image(biso,x))),
    Concatenation(List([1..4],z->36),List([1..4],z->bpermDegree)));;
  q3PB2Degree:=4*36+4*bpermDegree;;
  jointPB2:=D972A5LBlockPerm([q3PB2,d1.pb2New],[q3PB2Degree,400]);;
  # The direct component calculation is the load-bearing gate; the compact
  # recorded values below avoid relying on this large display in the checker.
  if Order(coarsePB2)<>18 or Order(q3PB2)<>18 or Order(d1.pb2New)<>5 or
     Order(jointPB2)<>90 then
    Error("157dp: q3/new marking fibre order drift");
  fi;
  mWords:=[0,18,36,54,72];;
  mNewKeys:=List(mWords,m->D972A5LPermRow(d1.pb2New^m,400));;
  if not ForAll(mWords,m->IsOne(q3PB2^m)) or Length(Set(mNewKeys))<>5 then
    Error("157dp: five PB2 kernel shifts are not exact/distinct");
  fi;
  ontoKeys:=[];; ontoVals:=[];; rle:=[];; codes:=[];; evaluated:=0;; selected:=fail;;
  counts:=rec(total:=0,friendly:=0,old_roof:=0,old_charming:=0,old_hexagon:=0,
    old_pentagon:=0,old_onto:=0,new_charming:=0,new_hexagon:=0,new_pentagon:=0,
    new_onto:=0,derived_all:=0,friendly_derived:=0,accepted:=0,
    materialized_words:=0,resource_skips:=0);;
  # The D_F' slice is a coordinate invariant, independent of m and of all
  # old-stage gates.  Compute it once over all 27*1500 outer/correction pairs
  # and report separately the five-shift and four-friendly-shift totals.
  derivedFlags:=[];; derivedIndices:=[];; derivedSliceCounts:=[];;
  for i in [1..27] do
    combinedStates:=List(sections.states,x->outerRows[i].main_compact*x);;
    Add(derivedFlags,List(combinedStates,x->x in d1.compactDerived));;
    Add(derivedIndices,Filtered([1..1500],j->derivedFlags[i][j]));;
    Add(derivedSliceCounts,Length(derivedIndices[i]));;
  od;
  counts.derived_all:=5*Sum(derivedSliceCounts);;
  counts.friendly_derived:=Length(Filtered(mWords,m->Gcd(2*m+1,90)=1))*
    Sum(derivedSliceCounts);;
  if counts.derived_all>8100 or counts.friendly_derived>6480 then
    Error("157dp: derived-slice cardinality bound drift");
  fi;
  for i in [1..27] do
    newBaseMain:=outerRows[i].main_compact;; newBaseHex:=outerRows[i].hex_new;;
    newBasePent:=outerRows[i].pent_new;;
    for s in [0..4] do
      m:=mWords[s+1];; u:=2*m+1;;
      for j in [1..1500] do
        candidateIndex:=evaluated+1;; evaluated:=candidateIndex;; counts.total:=counts.total+1;;
        code:="";;
        if Gcd(u,90)<>1 then code:="F";;
        else
          counts.friendly:=counts.friendly+1;;
          if not outerRows[i].old_roof then code:="R";;
          else counts.old_roof:=counts.old_roof+1;;
            if not outerRows[i].old_charming then code:="C";;
            else counts.old_charming:=counts.old_charming+1;;
              if not outerRows[i].old_hexagon then code:="H";;
              else counts.old_hexagon:=counts.old_hexagon+1;;
                if not outerRows[i].old_pentagon then code:="P";;
                else counts.old_pentagon:=counts.old_pentagon+1;;
                  if not outerRows[i].old_onto then code:="O";;
                  else counts.old_onto:=counts.old_onto+1;;
                  fi;
                fi;
              fi;
            fi;
          fi;
        fi;
        if code="" then
          combined:=newBaseMain*sections.states[j];;
          charm:=derivedFlags[i][j];;
          if not charm then code:="c";;
          else
            counts.new_charming:=counts.new_charming+1;;
            newHexVals:=D972A5LContextMul(newBaseHex,sections.hexState[j]);;
            newHex:=ForAll(D972A5LHexFromValues(newHexVals,m,
              d1.fullMarks[1],d1.fullMarks[3]),IsOne);;
            if not newHex then code:="h";;
            else
              counts.new_hexagon:=counts.new_hexagon+1;;
              newPentVals:=D972A5LContextMul(newBasePent,sections.pentState[j]);;
              newPent:=IsOne(D972A5LPentFromValues(newPentVals));;
              if not newPent then code:="p";;
              else
                counts.new_pentagon:=counts.new_pentagon+1;;
                pos:=Position(ontoKeys,[combined,s]);;
                if pos=fail then
                  newOnto:=Size(Group(d1.compactMarks[1]^u,
                    D972A5LPP([combined^-1,d1.compactMarks[3]^u,combined])))=1500;;
                  Add(ontoKeys,[combined,s]);; Add(ontoVals,newOnto);; pos:=Length(ontoVals);;
                fi;
                newOnto:=ontoVals[pos];;
                if not newOnto then code:="o";;
                else counts.new_onto:=counts.new_onto+1;; code:="A";; fi;
              fi;
            fi;
          fi;
        fi;
        Add(codes,code[1]);; D972A5LAddCode(rle,code);;
        if code="A" then
          counts.accepted:=1;; counts.materialized_words:=1;;
          corrWord:=D972A5LExpandSection(j,sections.records,sections.normal_generators);;
          candidateWord:=D972A5LReduce(Concatenation(outerWords[i],corrWord));;
          positiveCanary:=D972A5LPositiveCanary(candidateWord,outerWords[i],m,d1,pc3,pc4,
            q0x,q0y,b2x,b2y,q4marks,pi4marks,sections,j,combined);;
          selected:=rec(candidate_index:=candidateIndex,outer_index:=i,m_shift_index:=s,
            m:=m,lambda:=u,correction_index:=j,typed_source_word:=candidateWord,
            source_word_sha256:=D972A5LDigest(candidateWord),
            q3_correction_word:=corr[i].word,a5_correction_word:=corrWord,
            charming:=true,friendly:=true,hexagon_exact:=true,pentagon_exact:=true,
            onto_exact:=true,reduces_to_fixed_roof:=true,
            settlement_required_for_acceptance:=false,
            settlement_diagnostic:="NOT_COMPUTED_NONISOLATED_L",
            direct_materialization_replay:=positiveCanary);;
          break;
        fi;
      od;
      if selected<>fail then break; fi;
    od;
    if selected<>fail then break; fi;
  od;
  allComplete:=evaluated=202500 and selected=fail and counts.resource_skips=0;;
  if Length(ontoKeys)>240 then Error("157dp: new onto cache exceeds 60*4 canary"); fi;
  if selected<>fail then terminal:=D972A5LPositive;;
  elif allComplete then terminal:=D972A5LNegative;;
  else terminal:=D972A5LUnknown;; fi;
  roofRow:=wordsObj.rows[37];;
  if roofRow[1]<>0 or roofRow[3]<>base then Error("157dp: frozen row37 mismatch"); fi;
  outsideCertificate:=D972A5LOutsideCertificate(q3,wordsObj);;
  universeContract:=rec(outer_count:=27,m_shift_count:=5,correction_count:=1500,
    total_count:=202500,order:="outer receipt order, then s=0..4, then section BFS order",
    m_values:=mWords,lambda_values:=List(mWords,z->2*z+1),
    q3_marking_order:=18,new_marking_order:=90,H_ord:=18,L_ord:=90,
    PB2_joint_image_order:=90,PB2_projection_kernel_order:=5,
    PB2_coprime_direct_product_proof:=true,
    PB2_old_shift_values_all_identity:=true,
    PB2_new_shift_value_rows:=mNewKeys,PB2_new_shift_values_distinct:=true,
    friendly_shift_indices:=[0,1,2,3],unfriendly_shift_indices:=[4],
    q3_outer_word_digest:=D972A5LDigest(List(corr,r->r.word)),
    coordinate_digest:=D972A5LDigest(rec(
      outer:=List(outerRows,r->[r.q_coords,r.word_sha256]),m:=mWords,
      corrections:=List(sections.records,r->r.key))),
    no_duplicate_coordinates:=Length(Set(List(sections.records,r->r.key)))=1500,
    coordinate_injectivity_proof:="E3=Q0 x B(2,3), joint F_H x D_F, and coprime PB2 C5 kernel",
    q3_fibre_complete:=true,F_H_times_D_F_kernel_exact:=true,PB2_C5_kernel_exact:=true);
  return rec(terminal:=terminal,selected:=selected,evaluated:=evaluated,
    exhaustive:=allComplete,counts:=counts,rejection_rle:=rle,
    rejection_stream_sha256:=HexSHA256(codes),outer_rows:=List(outerRows,r->rec(
      index:=r.index,q_coords:=r.q_coords,word_sha256:=r.word_sha256,
      old_roof:=r.old_roof,old_charming:=r.old_charming,old_hexagon:=r.old_hexagon,
      old_pentagon:=r.old_pentagon,old_onto:=r.old_onto)),
    universe:=universeContract,outside_classifier:=outsideCertificate,
    derived_slice:=rec(per_outer_correction_counts:=derivedSliceCounts,
      per_outer_indices_sha256:=D972A5LDigest(derivedIndices),
      all_five_shifts_count:=counts.derived_all,
      friendly_four_shifts_count:=counts.friendly_derived,
      all_five_upper_bound:=8100,friendly_upper_bound:=6480),
    performance:=rec(candidate_long_word_builds:=counts.materialized_words,
      compact_candidates:=evaluated,new_literal_gate_candidates:=counts.new_charming,
      full_universe_coordinates:=202500,fixed_contexts_precomputed:=true,
      derived_slice_precomputed_before_acceptance_scan:=true,
      section_source_words_materialized_in_hot_loop:=false,
      selected_word_materializations_at_most_one:=(counts.materialized_words<=1),
      new_onto_cache_entries:=Length(ontoKeys),new_onto_cache_upper_bound:=240,
      old_factor_onto_cache_entries:=
        [Length(ontoPKeys),Length(ontoGKeys),Length(ontoBKeys)],
      settlement_calls:=0,ANUPQ_calls:=0,PB5_constructions:=0,
      Elements_A5four_calls:=0,generic_large_joint_kernel_calls:=0));
end;;

#############################################################################
## Main.
#############################################################################

D972A5LMain := function(output)
  local t,pins,q3r,fc8r,q3,fc,wordsr,words,d1,pc3,pc4,B2,b2x,b2y,
    q0marks,Q0,q0x,q0y,q4marks,Q4,oldContexts,sections,scan,receipt,
    oldFullX,oldFullY,biso,bperm,bx,by,fhOrder,normalPublic,sourcePublic,
    pb4marks,terminal,proof,e4Order,layerBinding,q4Order,pi4Order;
  t:=Runtime();;
  pins:=rec(q3_producer:=D972A5LRequireSHA(D972A5LQ3ProducerPath,D972A5LQ3ProducerSHA,"q3 producer"),
    q3_checker:=D972A5LRequireSHA(D972A5LQ3CheckerPath,D972A5LQ3CheckerSHA,"q3 checker"),
    q3_driver:=D972A5LRequireSHA(D972A5LQ3DriverPath,D972A5LQ3DriverSHA,"q3 driver"),
    fc8_producer:=D972A5LRequireSHA(D972A5LFC8ProducerPath,D972A5LFC8ProducerSHA,"FC8 producer"),
    fc8_checker:=D972A5LRequireSHA(D972A5LFC8CheckerPath,D972A5LFC8CheckerSHA,"FC8 checker"),
    fc8_driver:=D972A5LRequireSHA(D972A5LFC8DriverPath,D972A5LFC8DriverSHA,"FC8 driver"),
    frozen_words:=D972A5LRequireSHA(D972A5LWordsPath,D972A5LWordsSHA,"word artifact"),
    outside_classifier_source:=D972A5LRequireSHA(D972A5LAxisPath,D972A5LAxisSHA,"axis classifier"));;
  q3r:=D972A5LReadJSON(D972A5LQ3Path,"q3 receipt");;
  fc8r:=D972A5LReadJSON(D972A5LFC8Path,"FC8 receipt");;
  wordsr:=D972A5LReadJSON(D972A5LWordsPath,"word artifact");;
  q3:=q3r.obj;; fc:=fc8r.obj;; words:=wordsr.obj;;
  if q3r.sha256<>D972A5LQ3HistoricalSHA then Error("157dp: q3 artifact is not frozen run"); fi;
  if fc8r.sha256<>D972A5LFC8HistoricalSHA then Error("157dp: FC8 artifact is not frozen run"); fi;
  if not IsBound(D972_B34_A5_SELECTED_LIFT_FC8_OBSERVED_RUNTIME_MS) or
     not IsInt(D972_B34_A5_SELECTED_LIFT_FC8_OBSERVED_RUNTIME_MS) or
     D972_B34_A5_SELECTED_LIFT_FC8_OBSERVED_RUNTIME_MS<0 or
     not IsBound(D972_B34_A5_SELECTED_LIFT_FC8_NORMALIZATION_CHECKED) or
     D972_B34_A5_SELECTED_LIFT_FC8_NORMALIZATION_CHECKED<>true then
    Error("157dp: missing checked FC8 runtime-normalization handoff");
  fi;
  if q3.schema<>"d972-b345-q-chief/v1" or
     q3.terminal_token<>"B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" then
    Error("157dp: q3 terminal/schema drift");
  fi;
  if fc.schema<>"d972-b4-fc8-a5four/v1" or
     fc.terminal_token<>"FC8_A5_FOUR_CHIEF_CROSSCHECKED" then
    Error("157dp: FC8 terminal/schema drift");
  fi;
  if q3.selected_solution.exponent<>2 or q3.selected_solution.roof_row_index<>37 or
     q3.selected_solution.marking_m<>0 or q3.selected_solution.correction_index<>1 or
     q3.selected_solution.typed_source_word<>D972A5LSelectedWord then
    Error("157dp: selected q3 witness drift");
  fi;
  if fc.goursat.joint_image_is_full_Q0_times_A5four<>true or
     fc.goursat.rhoA_surjective<>true or fc.chief_factor.B4_factor_action_transitive<>true then
    Error("157dp: FC8 joint/chief premise drift");
  fi;
  if q3.typed_relative_stage.q3_system_ready<>true or
     q3.typed_relative_stage.pullback_certified.E3<>"Q0 x Pi3[3]" or
     q3.typed_relative_stage.pullback_certified.E4<>"Q4 x Pi4[3]" then
    Error("157dp: q3 exact pullback/direct-product premise drift");
  fi;
  d1:=D972A5LD1(fc);;
  pc3:=D972A5LImportPC(q3.groups.PB3,"Pi3");;
  pc4:=D972A5LImportPC(q3.groups.PB4,"Pi4");;
  B2:=Group(pc3.marks[1],pc3.marks[3]);; b2x:=pc3.marks[1];; b2y:=pc3.marks[3];;
  if Size(B2)<>27 then Error("157dp: B(2,3) order drift"); fi;
  q0marks:=List(q3.coarse_models.Q0.marked_permutations,D972A5LPermFromRow);;
  q0x:=q0marks[1];; q0y:=q0marks[2];; Q0:=Group(q0marks);;
  q4marks:=List(q3.coarse_models.Q4.marked_permutations,D972A5LPermFromRow);;
  Q4:=Group(q4marks);; pb4marks:=pc4.marks;;
  q4Order:=Size(Q4);; pi4Order:=Size(pc4.group);;
  if Size(Q0)<>1469664 or Size(B2)<>27 or q4Order<>583152628325845597028352 then
    Error("157dp: old target order drift");
  fi;
  e4Order:=q4Order*pi4Order;;
  if pi4Order<>59049 or e4Order mod 5=0 then
    Error("157dp: fine E4 order/common-A5 quotient drift");
  fi;
  biso:=IsomorphismPermGroup(B2);; bperm:=Image(biso);;
  bx:=Image(biso,b2x);; by:=Image(biso,b2y);;
  oldFullX:=D972A5LBlockPerm([q0x,bx],[36,LargestMovedPoint(bperm)]);;
  oldFullY:=D972A5LBlockPerm([q0y,by],[36,LargestMovedPoint(bperm)]);;
  fhOrder:=Size(Group(oldFullX,oldFullY));;
  if fhOrder<>1469664*27 or 5 in Set(FactorsInt(fhOrder)) then
    Error("157dp: actual F_H direct-product/order gate");
  fi;
  oldContexts:=[ [q0x,q0y], [b2x,b2y], D972A5LHexPairs(q0x,q0y),
    D972A5LHexPairs(b2x,b2y),D972A5LPairs(q4marks),D972A5LPairs(pb4marks),
    [d1.fullMarks[1],d1.fullMarks[3]],D972A5LHexPairs(d1.fullMarks[1],d1.fullMarks[3]),
    D972A5LPairs(d1.pb4marks) ];;
  sections:=D972A5LNormalSections(d1,oldFullX,oldFullY,oldContexts);;
  scan:=D972A5LScan(q3,d1,pc3,pc4,Q0,q0x,q0y,B2,b2x,b2y,biso,bperm,Q4,q4marks,
    pb4marks,sections,words);;
  normalPublic:=List(sections.normal_generators,r->rec(base_relator:=r.base_relator,
    conjugator_index:=r.conjugator_index,word:=r.word,compact_key:=r.compact_key));;
  sourcePublic:=rec(F_H_order:=fhOrder,F_H_prime_support:=Set(FactorsInt(fhOrder)),
    F_H_equals_Q0_times_B2:=true,Q0_order:=1469664,B2_order:=27,
    Q0_abelianization_order:=4,Q0_has_no_nontrivial_3group_quotient:=true,
    direct_product_proof:=rec(
      Q0_marked_image_is_subdirect_P_times_G9:=true,P_order:=504,P_perfect:=true,
      G9_order:=2916,G9_derived_order:=729,G9_solvable:=true,
      Q0_full_by_perfect_versus_solvable_Goursat:=true,
      Q0_abelianization_reduced_to_G9_order:=4,
      B2_is_3group_order:=27,
      every_nontrivial_B2_quotient_has_C3_quotient:=true,
      Q0_has_no_C3_quotient:=true,F_H_full_by_Goursat:=true),
    D_F_structure:="A5_diag x C5^2",D_F_order:=1500,
    every_nontrivial_D_F_quotient_has_order_divisible_by_5:=true,
    no_common_quotient:=true,joint_F2_target_full_direct_product:=true,
    projection_kernel_order:=1500,power_relators:=sections.source_power_relators,
    old_generator_orders:=sections.old_generator_orders,
    tracked_normal_generators:=normalPublic,normal_closure_order:=sections.normal_closure_order,
    normal_generator_count:=sections.normal_generator_count,
    section_records:=sections.records,section_order:="BFS edges +g1..+gr,-g1..-gr",
    section_coverage_sha256:=D972A5LDigest(sections.records));;
  layerBinding:=rec(old_fine_target:="E4 = Q4 x Pi4[3]",
    Q4_order:=q4Order,Pi4_q3_order:=pi4Order,E4_order:=e4Order,
    E4_order_coprime_to_5:=(e4Order mod 5<>0),A5four_order:=60^4,
    rho_E4_surjective:=true,rho_A5four_surjective:=true,
    every_nontrivial_A5four_quotient_order_divisible_by_5:=true,
    no_nontrivial_common_quotient_E4_A5four:=true,
    joint_target_full_E4_times_A5four_by_Goursat:=true,
    H_definition:="ker(PB4 -> E4)",
    L_definition:="H intersection ker(rhoA)",H_over_L:="A5^4",
    H_over_L_order:=60^4,L_B4_normal_finite_index:=true,
    B4_factor_action_transitive:=true,L_isolated_assumed:=false);;
  terminal:=scan.terminal;;
  proof:=rec(positive:=rec(L_isolated_assumed:=false,
      implication:="one literal outside shadow exists at B4-normal L and survives to every isolated coarser audit window; one-outside applies there",
      remaining_boundary:="uniform/cofinal absorption of every later required chief layer"),
    negative:=rec(applicable:=(terminal=D972A5LNegative),
      corollary_3_13:="a genuine roof element survives to every B4-normal finite-index window",
      L_B4_normal_finite_index:=true,fixed_outside_roof_full_fibre_empty:=scan.exhaustive,
      global_genuine_image_subgroup:=true,arithmetic_contained_in_genuine:=true,
      subgroup_chain:="A <= P <= X",index_X_A:=3,
      deduction:="x not in P; P is not X; prime-index subgroup chain forces P=A; B4-A",
      isolated_fallback:="Cor.3.5 chooses N<=L; an N-lift would reduce to L; Prop.3.7/3.11 gives I_N=A"));;
  receipt:=rec(schema:=D972A5LSchema,status:=terminal,terminal_token:=terminal,
    terminal:=terminal in [D972A5LPositive,D972A5LNegative],
    pins:=rec(historical_q3_run:=32135808950,historical_q3_artifact_sha256:=D972A5LQ3HistoricalSHA,
      same_job_q3_artifact_sha256:=q3r.sha256,historical_fc8_run:=32153799126,
      historical_fc8_artifact_sha256:=D972A5LFC8HistoricalSHA,
      same_job_fc8_artifact_sha256:=fc8r.sha256,
      fc8_runtime_normalization:=rec(normalized_nonsemantic_field:="performance.runtime_ms",
        observed_fresh_value:=D972_B34_A5_SELECTED_LIFT_FC8_OBSERVED_RUNTIME_MS,
        frozen_value:=598,fresh_checker_passed_before_normalization:=true,
        checker_passed_after_normalization:=true,all_other_JSON_fields_equal:=true),
      sources:=pins),
    frozen_outside:=rec(exponent:=2,row_index:=37,m:=0,word:=D972A5LSelectedWord,
      roof_key:=words.rows[37][2],classifier:=scan.outside_classifier),
    fine_layer_binding:=layerBinding,d1_preflight:=d1.receipt,source_fibre:=sourcePublic,
    composite_universe:=scan.universe,outer_q3_fibre:=scan.outer_rows,
    scan:=rec(evaluated_candidates:=scan.evaluated,exhaustive:=scan.exhaustive,
      counts:=scan.counts,rejection_rle:=scan.rejection_rle,
      rejection_stream_sha256:=scan.rejection_stream_sha256,
      selected:=scan.selected,settlement_is_acceptance_gate:=false,
      resource_skips:=scan.counts.resource_skips),
    performance:=scan.performance,proof_implication:=proof,
    provenance:=rec(producer:=D972A5LProducer,
      checker:="search/check_d972_b34_a5_selected_lift_v1.py"),
    runtime_ms:=Runtime()-t);;
  D972A5LCheckedWrite(output,receipt);;
  Print(terminal," output=",output," evaluated=",scan.evaluated,
    " charm=",scan.counts.new_charming," runtime_ms=",Runtime()-t,"\n");
end;;

D972A5LSelfTest := function()
  local X,Y,D,der,path,obj;
  X:=PermList([3,4,2,5,1]);; Y:=PermList([3,1,4,5,2]);;
  D:=Group(D972A5LBlockPerm([X,(1,2,3,4,5),()],[5,5,5]),
    D972A5LBlockPerm([Y,(),(1,2,3,4,5)],[5,5,5]));;
  der:=DerivedSubgroup(D);;
  if Size(D)<>1500 or Size(der)<>60 or Length(D972A5LDFBFS(D,
      D972A5LBlockPerm([X,(1,2,3,4,5),()],[5,5,5]),
      D972A5LBlockPerm([Y,(),(1,2,3,4,5)],[5,5,5])).states)<>1500 then
    Error("157dp: producer selftest D_F");
  fi;
  path:=Filename(DirectoryTemporary(),"d972_a5_selected_io.json");;
  obj:=rec(schema:="io-selftest",empty:=[],order:=1500);;
  D972A5LCheckedWrite(path,obj);;
  D972A5LCheckedIoMarkerCount:=D972A5LCheckedIoMarkerCount+1;;
  Print(D972A5LCheckedIoMarker,"\n");
end;;

if IsBound(D972_B34_A5_SELECTED_LIFT_SELFTEST) and
   D972_B34_A5_SELECTED_LIFT_SELFTEST=true then
  if IsBound(D972_B34_A5_SELECTED_LIFT_RUN) and D972_B34_A5_SELECTED_LIFT_RUN=true then
    Error("157dp: SELFTEST and RUN are exclusive");
  fi;
  D972A5LSelfTest();;
elif IsBound(D972_B34_A5_SELECTED_LIFT_RUN) and D972_B34_A5_SELECTED_LIFT_RUN=true then
  if not IsBound(D972_B34_A5_SELECTED_LIFT_OUTPUT) then
    D972_B34_A5_SELECTED_LIFT_OUTPUT:="ci/out/d972_b34_a5_selected_lift_v1.json";;
  fi;
  D972A5LMain(D972_B34_A5_SELECTED_LIFT_OUTPUT);;
else
  Error("157dp: select exactly one mode");
fi;
