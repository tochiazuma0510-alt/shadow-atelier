#############################################################################
## D972 corrected pentagon-interleave canary, finite p=2 stage v5.
##
## Producer-only source.  It reads no task checker, checker verdict, or checker
## report.  It reuses only the frozen authenticated NQ portability stage v4,
## then constructs marked D4_2 quotients through the direct NQ record/collector
## API.  In particular it never forms the fp source subgroup used by
## NqEpimorphismByNqOutput.
#############################################################################

P159V5Source := "search/d972_pent_interleave_canary_p2_v5.g";
P159V5Output := "ci/out/d972_pent_interleave_canary_p2_receipt_v5_20260824.json";
P159V5Stage0 := "search/d972_pent_interleave_canary_stage0_v4.g";
P159V5Stage0Sha :=
  "eefb7b78a1b1d69634642db85cdbf9ebffae4e871fa5c7008d20b92117374657";
P159V5NqPcpSha :=
  "dc751b35a3106a30f7cf7d670187584c4f01db0c7b6323c469226a68965ad7e1";
P159V5Start := Runtime();

P159V5RequireFileSha := function(path,expected,label)
  local raw,got;
  raw:=StringFile(path);
  if raw=fail then Error("PENT159N_V5: missing ",label," at ",path); fi;
  got:=HexSHA256(raw);
  if got<>expected then
    Error("PENT159N_V5: ",label," SHA drift: ",got);
  fi;
  return got;
end;

P159V5RequireFileSha(P159V5Stage0,P159V5Stage0Sha,
  "frozen authenticated direct-NQ stage0 v4");
Read(P159V5Stage0);
Print("PENT159N_P2_V5_STAGE0_REPLAY_PASS source=",P159V5Stage0,
  " sha256=",P159V5Stage0Sha," runtime_ms=",Runtime(),"\n");

P159V5NqPcpPath:=Concatenation(P159V4NqPath,"gap/nqpcp.gi");
P159V5RequireFileSha(P159V5NqPcpPath,P159V5NqPcpSha,
  "NQ direct marked-image pc implementation");
if not IsBoundGlobal("NqCallANU_NQ") or
   not IsBoundGlobal("NqInitFromTheLeftCollector") or
   not IsBoundGlobal("NqPcpGroupByCollector") or
   not IsBoundGlobal("NqPcpElementByWord") then
  Error("PENT159N_V5: required direct NQ record/collector API unavailable");
fi;
Print("PENT159N_P2_V5_MARKED_API_PIN_PASS nqpcp_sha256=",
  P159V5NqPcpSha," api=NqCallANU_NQ+NqInitFromTheLeftCollector+",
  "NqPcpGroupByCollector+NqPcpElementByWord\n");

#############################################################################
## Stable JSON and phase helpers.
#############################################################################

P159V5Escape := function(s)
  local z;
  z:=ReplacedString(s,"\\","\\\\");
  z:=ReplacedString(z,"\"","\\\"");
  z:=ReplacedString(z,"\n","\\n");
  z:=ReplacedString(z,"\r","\\r");
  z:=ReplacedString(z,"\t","\\t");
  return z;
end;

P159V5Json := function(x)
  local names,parts,n;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",P159V5Escape(x),"\"");
  fi;
  if IsRecord(x) then
    names:=ShallowCopy(RecNames(x)); Sort(names);
    parts:=[];
    for n in names do
      Add(parts,Concatenation(P159V5Json(n),":",P159V5Json(x.(n))));
    od;
    return Concatenation("{",JoinStringsWithSeparator(parts,","),"}");
  fi;
  if IsList(x) then
    return Concatenation("[",JoinStringsWithSeparator(
      List(x,P159V5Json),","),"]");
  fi;
  Error("PENT159N_V5: unsupported JSON value");
end;

P159V5Digest := x -> HexSHA256(P159V5Json(x));

P159V5CheckedWrite := function(path,obj)
  local expected,f,raw;
  expected:=Concatenation(P159V5Json(obj),"\n");
  f:=OutputTextFile(path,false);
  if f=fail then Error("PENT159N_V5: cannot open output ",path); fi;
  SetPrintFormattingStatus(f,false);
  PrintTo(f,expected); CloseStream(f);
  raw:=StringFile(path);
  if raw=fail or raw<>expected then
    Error("PENT159N_V5: closed-write readback mismatch ",path);
  fi;
  return rec(bytes:=Length(raw),sha256:=HexSHA256(raw));
end;

P159V5Phase := function(label)
  Print("PENT159N_P2_V5_PHASE ",label," runtime_ms=",Runtime(),
    " elapsed_ms=",Runtime()-P159V5Start,"\n");
  if IsBoundGlobal("FlushAllStreams") then FlushAllStreams(); fi;
end;

P159V5Bool := function(b,label)
  if not b then Error("PENT159N_V5: failed gate ",label); fi;
  return true;
end;

#############################################################################
## Signed words, paper multiplication, and faithful pure-braid presentation.
#############################################################################

P159V5Reduce := function(w)
  local out,x;
  out:=[];
  for x in w do
    if x=0 then Error("PENT159N_V5: zero signed letter"); fi;
    if Length(out)>0 and out[Length(out)]=-x then
      Remove(out,Length(out));
    else
      Add(out,x);
    fi;
  od;
  return out;
end;

P159V5InvWord := w -> P159V5Reduce(List(Reversed(w),x->-x));

P159V5SubWord := function(w,imgs)
  local out,x;
  out:=[];
  for x in w do
    if AbsInt(x)>Length(imgs) then
      Error("PENT159N_V5: signed-word image index drift");
    fi;
    if x>0 then Append(out,imgs[x]);
    else Append(out,P159V5InvWord(imgs[-x])); fi;
    out:=P159V5Reduce(out);
  od;
  return out;
end;

P159V5NativeWordEval := function(w,gens)
  local z,x;
  z:=One(gens[1]);
  for x in w do
    if x>0 then z:=z*gens[x]; else z:=z*gens[-x]^-1; fi;
  od;
  return z;
end;

## Paper f1*f2*...*fk is native GAP fk*...*f2*f1 in this repository.
P159V5Paper := function(xs)
  local z,i;
  if Length(xs)=0 then Error("PENT159N_V5: empty paper product"); fi;
  z:=One(xs[1]);
  for i in Reversed([1..Length(xs)]) do z:=z*xs[i]; od;
  return z;
end;

P159V5PaperWordEval := function(w,gens)
  local factors,x;
  if Length(w)=0 then return One(gens[1]); fi;
  factors:=[];
  for x in w do
    if x>0 then Add(factors,gens[x]); else Add(factors,gens[-x]^-1); fi;
  od;
  return P159V5Paper(factors);
end;

P159V5ArtinStep := function(rank,letter)
  local imgs,i;
  imgs:=List([1..rank],i->[i]); i:=AbsInt(letter);
  if i<1 or i>=rank then Error("PENT159N_V5: Artin index drift"); fi;
  if letter>0 then
    imgs[i]:=[i,i+1,-i]; imgs[i+1]:=[i];
  else
    imgs[i]:=[i+1]; imgs[i+1]:=[-(i+1),i,i+1];
  fi;
  return imgs;
end;

P159V5ArtinImages := function(rank,w)
  local imgs,x,step;
  imgs:=List([1..rank],i->[i]);
  for x in w do
    step:=P159V5ArtinStep(rank,x);
    imgs:=List(imgs,v->P159V5SubWord(v,step));
  od;
  return imgs;
end;

P159V5ArtinIdentity := function(rank,w)
  return P159V5ArtinImages(rank,w)=List([1..rank],i->[i]);
end;

P159V5PairList := function(rank)
  local ans,i,j;
  ans:=[];
  for i in [1..rank-1] do
    for j in [i+1..rank] do Add(ans,[i,j]); od;
  od;
  return ans;
end;

P159V5PairIndex := function(rank,pair)
  local p;
  p:=Position(P159V5PairList(rank),pair);
  if p=fail then Error("PENT159N_V5: invalid pure pair"); fi;
  return p;
end;

P159V5AijBraid := function(i,j)
  local w,k;
  w:=[];
  if j-i>1 then for k in Reversed([i+1..j-1]) do Add(w,k); od; fi;
  Add(w,i); Add(w,i);
  if j-i>1 then for k in [i+1..j-1] do Add(w,-k); od; fi;
  return w;
end;

P159V5ExpandPure := function(rank,w)
  return P159V5SubWord(w,List(P159V5PairList(rank),
    p->P159V5AijBraid(p[1],p[2])));
end;

P159V5PureRelations := function(rank)
  local pairs,oldpairs,oldrels,mapold,rels,kmaps,p,g,act,k,h;
  if rank=2 then return []; fi;
  pairs:=P159V5PairList(rank);
  oldpairs:=P159V5PairList(rank-1);
  oldrels:=P159V5PureRelations(rank-1);
  mapold:=List(oldpairs,p->P159V5PairIndex(rank,p));
  rels:=List(oldrels,w->P159V5SubWord(w,List(mapold,x->[x])));
  kmaps:=List([1..rank-1],k->[P159V5PairIndex(rank,[k,rank])]);
  for p in oldpairs do
    g:=P159V5PairIndex(rank,p);
    act:=P159V5ArtinImages(rank-1,P159V5AijBraid(p[1],p[2]));
    for k in [1..rank-1] do
      h:=P159V5PairIndex(rank,[k,rank]);
      Add(rels,P159V5Reduce(Concatenation([-g,h,g],
        P159V5InvWord(P159V5SubWord(act[k],kmaps)))));
    od;
  od;
  return rels;
end;

P159V5BuildPureFp := function(rank)
  local pairs,labels,F,fg,rels,fp;
  pairs:=P159V5PairList(rank);
  labels:=List(pairs,p->Concatenation("a",String(p[1]),String(p[2])));
  F:=FreeGroup(labels); fg:=GeneratorsOfGroup(F);
  rels:=P159V5PureRelations(rank);
  if ForAny(rels,w->not P159V5ArtinIdentity(rank,
      P159V5ExpandPure(rank,w))) then
    Error("PENT159N_V5: faithful Artin replay failed PB",rank);
  fi;
  fp:=F/List(rels,w->P159V5NativeWordEval(w,fg));
  return rec(rank:=rank,pairs:=pairs,labels:=labels,relations:=rels,
    relation_count:=Length(rels),group:=fp,gens:=GeneratorsOfGroup(fp),
    artin_replay:=true);
end;

P159V5CofaceGenerator := function(rank,slot,pair)
  local i,j,ii,jj;
  i:=pair[1]; j:=pair[2];
  if slot=0 then return [P159V5PairIndex(rank+1,[i+1,j+1])]; fi;
  if slot=rank+1 then return [P159V5PairIndex(rank+1,[i,j])]; fi;
  if slot<1 or slot>rank then Error("PENT159N_V5: coface slot drift"); fi;
  if i=slot then
    return [P159V5PairIndex(rank+1,[slot,j+1]),
      P159V5PairIndex(rank+1,[slot+1,j+1])];
  elif j=slot then
    return [P159V5PairIndex(rank+1,[i,slot]),
      P159V5PairIndex(rank+1,[i,slot+1])];
  fi;
  ii:=i; jj:=j;
  if ii>slot then ii:=ii+1; fi;
  if jj>slot then jj:=jj+1; fi;
  return [P159V5PairIndex(rank+1,[ii,jj])];
end;

P159V5Cofaces := function(rank)
  return List([0..rank+1],s->List(P159V5PairList(rank),
    p->P159V5CofaceGenerator(rank,s,p)));
end;

P159V5DeleteGenerator := function(rank,strand,pair)
  local i,j;
  i:=pair[1]; j:=pair[2];
  if strand=i or strand=j then return []; fi;
  if i>strand then i:=i-1; fi;
  if j>strand then j:=j-1; fi;
  return [P159V5PairIndex(rank-1,[i,j])];
end;

P159V5Deletions := function(rank)
  return List([1..rank],s->List(P159V5PairList(rank),
    p->P159V5DeleteGenerator(rank,s,p)));
end;

#############################################################################
## Direct marked D4_2 quotients.  The identical laws are literal and ordered.
#############################################################################

P159V5EvalExtRep := function(w,imgs)
  local e,z,i,k,n;
  e:=ExtRepOfObj(w); z:=One(imgs[1]); i:=1;
  while i<=Length(e) do
    k:=e[i]; n:=e[i+1];
    if not IsInt(k) or not IsInt(n) or k<1 or k>Length(imgs) then
      Error("PENT159N_V5: malformed fp relator external representation");
    fi;
    z:=z*imgs[k]^n; i:=i+2;
  od;
  return z;
end;

P159V5BuildD42 := function(name,presentation)
  local sourceF,sourceGens,sourceRels,r,ext,eg,mapped,u,v,E,idgens,
    nqrec,coll,Q,marks;
  sourceF:=FreeGroupOfFpGroup(presentation.group);
  sourceGens:=GeneratorsOfGroup(sourceF);
  sourceRels:=RelatorsOfFpGroup(presentation.group);
  r:=Length(sourceGens);
  if r<>Length(presentation.labels) then
    Error("PENT159N_V5: source generator/label count drift ",name);
  fi;
  ext:=FreeGroup(Concatenation(presentation.labels,
    [Concatenation("id_u_",name),Concatenation("id_v_",name)]));
  eg:=GeneratorsOfGroup(ext);
  mapped:=List(sourceRels,w->P159V5EvalExtRep(w,eg{[1..r]}));
  u:=eg[r+1]; v:=eg[r+2];
  E:=ext/Concatenation(mapped,[u^4,Comm(u,v)^2]);
  idgens:=[u,v];
  Print("PENT159N_P2_V5_NQ_CALL_BEGIN name=",name,
    " ordinary_generators=",r," source_relators=",Length(sourceRels),
    " identical_relators=u^4,Comm(u,v)^2 class_bound=3 runtime_ms=",
    Runtime(),"\n");
  if IsBoundGlobal("FlushAllStreams") then FlushAllStreams(); fi;
  nqrec:=NqCallANU_NQ(rec(group:=E,idgens:=idgens,class:=3));
  Print("PENT159N_P2_V5_NQ_CALL_RETURN name=",name,
    " nr_pc_generators=",nqrec.NrGenerators,
    " marked_image_count=",Length(nqrec.Images)," runtime_ms=",Runtime(),"\n");
  if nqrec=fail or nqrec.NrGenerators=fail or nqrec.Images=fail or
     Length(nqrec.Images)<>r then
    Error("PENT159N_V5: incomplete direct NQ output ",name);
  fi;
  coll:=NqInitFromTheLeftCollector(nqrec);
  Q:=NqPcpGroupByCollector(coll,nqrec);
  marks:=List(nqrec.Images,w->NqPcpElementByWord(coll,w));
  if not IsPcpGroup(Q) or Size(Group(marks))<>Size(Q) then
    Error("PENT159N_V5: marked pc quotient construction failed ",name);
  fi;
  if NilpotencyClassOfGroup(Q)<>3 then
    Error("PENT159N_V5: quotient class is not exactly three ",name);
  fi;
  if ForAny(presentation.relations,w->
      P159V5NativeWordEval(w,marks)<>One(Q)) then
    Error("PENT159N_V5: source braid relation image nonidentity ",name);
  fi;
  return rec(name:=name,group:=Q,marks:=marks,nqrec:=nqrec,collector:=coll,
    presentation:=presentation,ordinary_generator_count:=r,
    source_relator_count:=Length(sourceRels));
end;

P159V5Coords := function(pc,x)
  local e;
  e:=ExponentsOfPcElement(pc,x);
  if e=fail then Error("PENT159N_V5: pc coordinate extraction failed"); fi;
  return List(e,Int);
end;

P159V5SeriesSizes := function(S)
  return List(S,g->String(Size(g)));
end;

P159V5PcReceipt := function(qrec)
  local G,pc,orders,powers,inverses,conj,conjinv,i,j,lcs,jenn,marked;
  G:=qrec.group; pc:=Pcgs(G); orders:=List(RelativeOrders(pc),Int);
  if Length(pc)>200 then Error("PENT159N_V5: pc generator cap exceeded"); fi;
  powers:=List([1..Length(pc)],i->P159V5Coords(pc,pc[i]^orders[i]));
  inverses:=List([1..Length(pc)],i->P159V5Coords(pc,pc[i]^-1));
  conj:=[]; conjinv:=[];
  if Length(pc)>1 then
    for i in [2..Length(pc)] do
      for j in [1..i-1] do
        Add(conj,rec(i:=i,j:=j,coords:=P159V5Coords(pc,pc[i]^pc[j])));
        Add(conjinv,rec(i:=i,j:=j,
          coords:=P159V5Coords(pc,pc[i]^(pc[j]^-1))));
      od;
    od;
  fi;
  lcs:=LowerCentralSeriesOfGroup(G);
  if not IsBoundGlobal("JenningsSeries") then
    Error("PENT159N_V5: JenningsSeries unavailable");
  fi;
  jenn:=JenningsSeries(G);
  marked:=List([1..Length(qrec.marks)],i->rec(
    label:=qrec.presentation.labels[i],pair:=qrec.presentation.pairs[i],
    coords:=P159V5Coords(pc,qrec.marks[i]),
    inverse_coords:=P159V5Coords(pc,qrec.marks[i]^-1)));
  return rec(name:=qrec.name,prime:=2,
    quotient_law:="D4_2(G)=G^4 gamma2(G)^2 gamma4(G)",
    order_decimal:=String(Size(G)),exponent:=Int(Exponent(G)),
    nilpotency_class:=Int(NilpotencyClassOfGroup(G)),
    pc_generator_count:=Length(pc),relative_orders:=orders,
    pc_power_relations:=powers,pc_inverse_relations:=inverses,
    pc_conjugate_relations:=conj,pc_inverse_conjugate_relations:=conjinv,
    marked_generators:=marked,
    source_presentation:=rec(rank:=qrec.presentation.rank,
      pair_order:=qrec.presentation.pairs,labels:=qrec.presentation.labels,
      relation_count:=qrec.presentation.relation_count,
      relations:=qrec.presentation.relations,faithful_artin_replay:=true,
      all_relator_images_identity:=true),
    lower_central_factor_sizes:=List([1..Length(lcs)-1],i->
      String(Size(lcs[i])/Size(lcs[i+1]))),
    lower_central_series_sizes:=P159V5SeriesSizes(lcs),
    zassenhaus_jennings_series_sizes:=P159V5SeriesSizes(jenn),
    pcgs_internal:=pc,lcs_internal:=lcs,jennings_internal:=jenn);
end;

P159V5PublicPcReceipt := function(r)
  local z;
  z:=ShallowCopy(r);
  Unbind(z.pcgs_internal); Unbind(z.lcs_internal); Unbind(z.jennings_internal);
  return z;
end;

P159V5MapCertificate := function(name,kind,sourceRec,sourcePc,targetRec,
    targetPc,words)
  local images,h,i;
  images:=List(words,w->P159V5NativeWordEval(w,targetRec.marks));
  h:=GroupHomomorphismByImages(sourceRec.group,targetRec.group,
    sourceRec.marks,images);
  if h=fail then Error("PENT159N_V5: map did not descend ",name); fi;
  if ForAny([1..Length(images)],i->Image(h,sourceRec.marks[i])<>images[i]) then
    Error("PENT159N_V5: marked map image drift ",name);
  fi;
  return rec(name:=name,kind:=kind,source:=sourceRec.name,
    target:=targetRec.name,generator_words:=words,
    target_marked_coords:=List(images,x->P159V5Coords(targetPc,x)),
    source_pc_images:=List(sourcePc,x->P159V5Coords(targetPc,Image(h,x))),
    source_mark_count:=Length(sourceRec.marks),well_defined:=true,
    image_order_decimal:=String(Size(Image(h))),hom_internal:=h);
end;

P159V5PublicMap := function(r)
  local z;
  z:=ShallowCopy(r); Unbind(z.hom_internal); return z;
end;

#############################################################################
## Canonical paper-word coverage and literal pentagon residual.
#############################################################################

P159V5BfsPaperWords := function(G,x,y)
  local rows,head,letters,row,l,g,newelt,newword,pos,pc;
  rows:=[rec(elt:=One(G),word:=[])]; head:=1; letters:=[1,-1,2,-2];
  while head<=Length(rows) do
    row:=rows[head];
    for l in letters do
      if l=1 then g:=x; elif l=-1 then g:=x^-1;
      elif l=2 then g:=y; else g:=y^-1; fi;
      ## Append l on the paper right; this is native left multiplication.
      newelt:=g*row.elt;
      pos:=Position(List(rows,r->r.elt),newelt);
      if pos=fail then
        newword:=P159V5Reduce(Concatenation(row.word,[l]));
        Add(rows,rec(elt:=newelt,word:=newword));
      fi;
    od;
    head:=head+1;
  od;
  if Length(rows)<>Size(G) then
    Error("PENT159N_V5: marked BFS does not cover Q2");
  fi;
  pc:=Pcgs(G);
  for row in rows do
    if P159V5PaperWordEval(row.word,[x,y])<>row.elt then
      Error("PENT159N_V5: paper BFS word replay drift");
    fi;
    row.coords:=P159V5Coords(pc,row.elt);
  od;
  Sort(rows,function(a,b) return a.coords<b.coords; end);
  if Length(Set(List(rows,r->r.coords)))<>Length(rows) then
    Error("PENT159N_V5: duplicate pc coordinate in Q2 BFS");
  fi;
  return rows;
end;

P159V5ExponentSums := function(w)
  return [Sum(Filtered(w,x->AbsInt(x)=1),SignInt),
    Sum(Filtered(w,x->AbsInt(x)=2),SignInt)];
end;

P159V5NormalizeDerivedWord := function(w,elt,x,y)
  local sums,out,i;
  sums:=P159V5ExponentSums(w);
  if sums[1] mod 4<>0 or sums[2] mod 4<>0 then
    Error("PENT159N_V5: quotient-derived word has nonzero abelianization mod 4");
  fi;
  out:=ShallowCopy(w);
  if sums[1]>0 then for i in [1..sums[1]] do Add(out,-1); od;
  elif sums[1]<0 then for i in [1..-sums[1]] do Add(out,1); od; fi;
  if sums[2]>0 then for i in [1..sums[2]] do Add(out,-2); od;
  elif sums[2]<0 then for i in [1..-sums[2]] do Add(out,2); od; fi;
  out:=P159V5Reduce(out);
  if P159V5ExponentSums(out)<>[0,0] or
     P159V5PaperWordEval(out,[x,y])<>elt then
    Error("PENT159N_V5: integral commutator representative normalization failed");
  fi;
  return out;
end;

P159V5Dpap := function(word,contexts)
  local vals,A,B,C,E,F,lhs,rhs,correct,mutant,inversionMismatch;
  vals:=List(contexts,c->P159V5PaperWordEval(word,c));
  ## slots: 0=phi234, 1=phi12_3_4, 2=phi1_23_4,
  ##        3=phi1_2_34, 4=phi123.
  C:=vals[1]; A:=vals[2]; E:=vals[3]; B:=vals[4]; F:=vals[5];
  lhs:=P159V5Paper([C,E,F]);
  rhs:=P159V5Paper([B,A]);
  correct:=P159V5Paper([A^-1,B^-1,C,E,F]);
  if correct<>P159V5Paper([rhs^-1,lhs]) then
    Error("PENT159N_V5: RHS^-1*LHS factor expansion drift");
  fi;
  ## Superseded scratchpad order: F E C (A B)^-1.
  mutant:=P159V5Paper([F,E,C,B^-1,A^-1]);
  inversionMismatch:=P159V5Paper([lhs^-1,rhs]);
  return rec(correct:=correct,wrong_order_mutant:=mutant,
    lhs_rhs_inversion_mutant:=inversionMismatch,
    factor_values:=vals);
end;

P159V5Histogram := function(rows,field)
  local keys,k,out;
  keys:=Set(List(rows,r->r.(field))); out:=[];
  for k in keys do
    Add(out,rec(coords:=k,count:=Number(rows,r->r.(field)=k)));
  od;
  return out;
end;

#############################################################################
## Construct the three p=2 quotients and every required marked map.
#############################################################################

P159V5Phase("BUILD_PRESENTATIONS");
P159V5F2F:=FreeGroup("x","y");
P159V5F2Pres:=rec(rank:=2,pairs:=[[1,2],[2,3]],labels:=["x","y"],
  relations:=[],relation_count:=0,group:=P159V5F2F/[],artin_replay:=true);
P159V5P3Pres:=P159V5BuildPureFp(3);
P159V5P4Pres:=P159V5BuildPureFp(4);
if P159V5P3Pres.relation_count<>2 or P159V5P4Pres.relation_count<>11 then
  Error("PENT159N_V5: FN presentation relation-count drift");
fi;

P159V5Phase("BUILD_Q2_D4_2");
P159V5Q2:=P159V5BuildD42("Q2_F2_D4_2",P159V5F2Pres);
if Size(P159V5Q2.group)<>128 then
  Error("PENT159N_V5: F2/D4_2 order calibration mismatch");
fi;
P159V5Q2Receipt:=P159V5PcReceipt(P159V5Q2);
Print("PENT159N_P2_V5_Q2_PASS order=128 class=3 pc_generators=",
  P159V5Q2Receipt.pc_generator_count," runtime_ms=",Runtime(),"\n");

P159V5Phase("BUILD_Q3_D4_2");
P159V5Q3:=P159V5BuildD42("Q3_PB3_D4_2",P159V5P3Pres);
P159V5Q3Receipt:=P159V5PcReceipt(P159V5Q3);
Print("PENT159N_P2_V5_Q3_PASS order=",Size(P159V5Q3.group),
  " class=3 pc_generators=",P159V5Q3Receipt.pc_generator_count,
  " runtime_ms=",Runtime(),"\n");

P159V5Phase("BUILD_Q4_D4_2");
P159V5Q4:=P159V5BuildD42("Q4_PB4_D4_2",P159V5P4Pres);
P159V5Q4Receipt:=P159V5PcReceipt(P159V5Q4);
Print("PENT159N_P2_V5_Q4_PASS order=",Size(P159V5Q4.group),
  " class=3 pc_generators=",P159V5Q4Receipt.pc_generator_count,
  " runtime_ms=",Runtime(),"\n");

P159V5Phase("BUILD_MARKED_MAPS");
P159V5Q2Pc:=P159V5Q2Receipt.pcgs_internal;
P159V5Q3Pc:=P159V5Q3Receipt.pcgs_internal;
P159V5Q4Pc:=P159V5Q4Receipt.pcgs_internal;
P159V5DelWords:=P159V5Deletions(4);
P159V5CofWords:=P159V5Cofaces(3);
P159V5ExpectedDelWords:=[
  [[],[],[],[1],[2],[3]],
  [[],[1],[2],[],[],[3]],
  [[1],[],[2],[],[3],[]],
  [[1],[2],[],[3],[],[]]
];
if P159V5DelWords<>P159V5ExpectedDelWords then
  Error("PENT159N_V5: deletion strand/renumbering table drift");
fi;
P159V5DeletionMaps:=List([1..4],i->P159V5MapCertificate(
  Concatenation("delete_strand_",String(i)),"ordinary_pure_braid_deletion",
  P159V5Q4,P159V5Q4Pc,P159V5Q3,P159V5Q3Pc,P159V5DelWords[i]));
P159V5CofaceMaps:=List([1..5],i->P159V5MapCertificate(
  Concatenation("coface_slot_",String(i-1)),"pure_braid_coface",
  P159V5Q3,P159V5Q3Pc,P159V5Q4,P159V5Q4Pc,P159V5CofWords[i]));
P159V5IotaMap:=P159V5MapCertificate("F2_to_PB3_x12_x23",
  "marked_F2_inclusion",P159V5Q2,P159V5Q2Pc,P159V5Q3,P159V5Q3Pc,
  [[1],[3]]);
if Size(Image(P159V5IotaMap.hom_internal))<>Size(P159V5Q2.group) then
  Error("PENT159N_V5: marked Q2 to Q3 map is not injective");
fi;
## The signed coface tables certify the homomorphisms in the faithful Artin
## presentation convention.  The displayed A.18 products themselves are paper
## products, so their two F2 arguments are evaluated with PaperWordEval.
P159V5Contexts:=List(P159V5CofWords,m->[
  P159V5PaperWordEval(m[1],P159V5Q4.marks),
  P159V5PaperWordEval(m[3],P159V5Q4.marks)]);
P159V5ContextWords:=List(P159V5CofWords,m->[m[1],m[3]]);
P159V5ExpectedContextWords:=[
  [[4],[6]],
  [[2,4],[6]],
  [[1,2],[5,6]],
  [[1],[4,5]],
  [[1],[4]]
];
if P159V5ContextWords<>P159V5ExpectedContextWords then
  Error("PENT159N_V5: printed A.18 coface substitution drift");
fi;
Print("PENT159N_P2_V5_MAPS_PASS deletions=4 cofaces=5",
  " iota_image_order=",Size(Image(P159V5IotaMap.hom_internal)),
  " deletion_table_sha256=",P159V5Digest(P159V5DelWords),
  " coface_table_sha256=",P159V5Digest(P159V5CofWords),"\n");

#############################################################################
## Complete commutator instrument and the actual charming+onto gate.
#############################################################################

P159V5Phase("ENUMERATE_Q2_CANONICAL_WORDS");
P159V5x:=P159V5Q2.marks[1]; P159V5y:=P159V5Q2.marks[2];
P159V5Bfs:=P159V5BfsPaperWords(P159V5Q2.group,P159V5x,P159V5y);
P159V5BfsPublic:=List(P159V5Bfs,r->rec(coords:=r.coords,word:=r.word));
P159V5BfsDigest:=P159V5Digest(P159V5BfsPublic);
P159V5D2:=DerivedSubgroup(P159V5Q2.group);
P159V5DerivedRows:=Filtered(P159V5Bfs,r->r.elt in P159V5D2);
if Length(P159V5DerivedRows)<>Size(P159V5D2) or
   Length(P159V5DerivedRows)<=1 then
  Error("PENT159N_V5: complete nontrivial derived-universe gate failed");
fi;
if Order(P159V5x)<>4 or Order(P159V5y)<>4 then
  Error("PENT159N_V5: marked Q2 generator order is not four");
fi;
for P159V5Row in P159V5DerivedRows do
  P159V5Row.commutator_word:=P159V5NormalizeDerivedWord(
    P159V5Row.word,P159V5Row.elt,P159V5x,P159V5y);
od;

P159V5Phase("COMPLETE_COMMUTATOR_INSTRUMENT");
P159V5Gamma3:=P159V5Q4Receipt.lcs_internal[3];
P159V5BrKernel:=Kernel(P159V5DeletionMaps[1].hom_internal);
for P159V5i in [2..4] do
  P159V5BrKernel:=Intersection(P159V5BrKernel,
    Kernel(P159V5DeletionMaps[P159V5i].hom_internal));
od;
P159V5Degree3BrKernel:=Intersection(P159V5Gamma3,P159V5BrKernel);
P159V5InstrumentInternal:=[];
for P159V5Row in P159V5DerivedRows do
  P159V5Drec:=P159V5Dpap(P159V5Row.commutator_word,P159V5Contexts);
  P159V5DeletionBits:=List(P159V5DeletionMaps,m->
    Image(m.hom_internal,P159V5Drec.correct)=One(P159V5Q3.group));
  if not ForAll(P159V5DeletionBits,b->b) then
    Error("PENT159N_V5: commutator Dpap failed an exact deletion");
  fi;
  if not P159V5Drec.correct in P159V5Degree3BrKernel then
    Error("PENT159N_V5: Dpap is outside degree-3 deletion kernel");
  fi;
  Add(P159V5InstrumentInternal,rec(f:=P159V5Row.elt,
    f_coords:=P159V5Row.coords,f_word:=P159V5Row.commutator_word,
    defect:=P159V5Drec.correct,
    defect_coords:=P159V5Coords(P159V5Q4Pc,P159V5Drec.correct),
    nonzero:=P159V5Drec.correct<>One(P159V5Q4.group),
    four_deletions:=P159V5DeletionBits));
od;
if Length(Set(List(P159V5InstrumentInternal,r->r.f_coords)))<>
   Size(P159V5D2) then
  Error("PENT159N_V5: commutator instrument omission/duplicate");
fi;
P159V5InstrumentPublic:=List(P159V5InstrumentInternal,r->rec(
  f_coords:=r.f_coords,f_word:=r.f_word,defect_coords:=r.defect_coords,
  nonzero:=r.nonzero,four_deletions:=r.four_deletions));
P159V5InstrumentDigest:=P159V5Digest(P159V5InstrumentPublic);
P159V5NonzeroInstrument:=Filtered(P159V5InstrumentInternal,r->r.nonzero);
P159V5DpapImage:=Subgroup(P159V5Q4.group,
  List(P159V5InstrumentInternal,r->r.defect));
if not IsSubgroup(P159V5Degree3BrKernel,P159V5DpapImage) then
  Error("PENT159N_V5: Dpap Brunnian image subgroup containment drift");
fi;
if Length(P159V5NonzeroInstrument)>0 then
  P159V5FirstNonzero:=P159V5NonzeroInstrument[1];
  P159V5FirstNonzeroPublic:=rec(f_coords:=P159V5FirstNonzero.f_coords,
    f_word:=P159V5FirstNonzero.f_word,
    defect_coords:=P159V5FirstNonzero.defect_coords,
    four_deletions:=P159V5FirstNonzero.four_deletions,
    in_gamma3:=P159V5FirstNonzero.defect in P159V5Gamma3,
    nonidentity:=true);
else
  P159V5FirstNonzeroPublic:=fail;
fi;

## Active noncommuting discriminator for the superseded factor order.  The
## discriminator scans the full finite Q2 word universe, not only f=1 or a
## deletion-blind case.
P159V5WrongOrderDiscriminator:=fail;
P159V5InversionDiscriminator:=fail;
P159V5SwappedCofaceDiscriminator:=fail;
P159V5SwappedContexts:=ShallowCopy(P159V5Contexts);
P159V5SwapTemp:=P159V5SwappedContexts[2];
P159V5SwappedContexts[2]:=P159V5SwappedContexts[4];
P159V5SwappedContexts[4]:=P159V5SwapTemp;
for P159V5Row in P159V5Bfs do
  P159V5Drec:=P159V5Dpap(P159V5Row.word,P159V5Contexts);
  P159V5SwapDrec:=P159V5Dpap(P159V5Row.word,P159V5SwappedContexts);
  if P159V5InversionDiscriminator=fail and
     P159V5Drec.correct<>P159V5Drec.lhs_rhs_inversion_mutant then
    P159V5InversionDiscriminator:=rec(f_coords:=P159V5Row.coords,
      f_word:=P159V5Row.word,
      correct_coords:=P159V5Coords(P159V5Q4Pc,P159V5Drec.correct),
      inversion_mutant_coords:=P159V5Coords(P159V5Q4Pc,
        P159V5Drec.lhs_rhs_inversion_mutant),distinct:=true);
  fi;
  if P159V5SwappedCofaceDiscriminator=fail and
     P159V5Drec.correct<>P159V5SwapDrec.correct then
    P159V5SwappedCofaceDiscriminator:=rec(f_coords:=P159V5Row.coords,
      f_word:=P159V5Row.word,
      correct_coords:=P159V5Coords(P159V5Q4Pc,P159V5Drec.correct),
      swapped_coords:=P159V5Coords(P159V5Q4Pc,P159V5SwapDrec.correct),
      swapped_slots:=[1,3],distinct:=true);
  fi;
  if P159V5WrongOrderDiscriminator=fail and
     Comm(P159V5Drec.correct,P159V5Drec.wrong_order_mutant)<>
     One(P159V5Q4.group) then
    P159V5WrongOrderDiscriminator:=rec(f_coords:=P159V5Row.coords,
      f_word:=P159V5Row.word,
      correct_coords:=P159V5Coords(P159V5Q4Pc,P159V5Drec.correct),
      mutant_coords:=P159V5Coords(P159V5Q4Pc,
        P159V5Drec.wrong_order_mutant),
      commutator_coords:=P159V5Coords(P159V5Q4Pc,
        Comm(P159V5Drec.correct,P159V5Drec.wrong_order_mutant)),
      noncommuting:=true);
  fi;
od;
if P159V5WrongOrderDiscriminator=fail then
  Error("PENT159N_V5: no noncommuting wrong-order discriminator in full Q2 universe");
fi;
if P159V5InversionDiscriminator=fail then
  Error("PENT159N_V5: LHS/RHS inversion mutant was not discriminated");
fi;
if P159V5SwappedCofaceDiscriminator=fail then
  Error("PENT159N_V5: swapped-coface mutant was not discriminated");
fi;
Print("PENT159N_P2_V5_INSTRUMENT_PASS universe=",
  Length(P159V5InstrumentInternal)," nonzero=",
  Length(P159V5NonzeroInstrument)," defect_image_order=",Size(P159V5DpapImage),
  " degree3_deletion_kernel_order=",Size(P159V5Degree3BrKernel),
  " coverage_sha256=",P159V5InstrumentDigest,"\n");

P159V5Phase("COMPLETE_CHARMING_ONTO_GATE");
P159V5Q3c:=P159V5Paper([P159V5Q3.marks[1],P159V5Q3.marks[2],
  P159V5Q3.marks[3]]);
if ForAny(P159V5Q3.marks,g->Comm(P159V5Q3c,g)<>One(P159V5Q3.group)) then
  Error("PENT159N_V5: PB3 full-twist marking is not central");
fi;
P159V5Nord:=Lcm(Order(P159V5Q3.marks[1]),Order(P159V5Q3.marks[3]),
  Order(P159V5Q3c));
if P159V5Nord<1 then Error("PENT159N_V5: invalid N_ord"); fi;
P159V5z:=P159V5Paper([P159V5x,P159V5y])^-1;
if P159V5z<>P159V5x^-1*P159V5y^-1 then
  Error("PENT159N_V5: correct tau native word drift");
fi;
P159V5Theta:=GroupHomomorphismByImages(P159V5Q2.group,P159V5Q2.group,
  [P159V5x,P159V5y],[P159V5y,P159V5x]);
P159V5Tau:=GroupHomomorphismByImages(P159V5Q2.group,P159V5Q2.group,
  [P159V5x,P159V5y],[P159V5y,P159V5z]);
if P159V5Theta=fail or P159V5Tau=fail or
   not IsBijective(P159V5Theta) or not IsBijective(P159V5Tau) then
  Error("PENT159N_V5: theta/tau automorphism descent failed");
fi;
P159V5WrongZ:=(P159V5x*P159V5y)^-1;
if P159V5WrongZ=P159V5z then
  Error("PENT159N_V5: rejected tau mutant collapsed to correct tau");
fi;
P159V5WrongTau:=GroupHomomorphismByImages(P159V5Q2.group,P159V5Q2.group,
  [P159V5x,P159V5y],[P159V5y,P159V5WrongZ]);
P159V5GateTrace:=[];
P159V5GateCounts:=rec(raw_pair_count:=0,unit_pass:=0,
  derived_after_unit_pass:=0,hexagon_310_pass:=0,hexagon_311_pass:=0,
  onto_pass:=0);
P159V5TauMutantDisagreements:=0;
for P159V5m in [0..P159V5Nord-1] do
  P159V5u:=2*P159V5m+1;
  for P159V5Row in P159V5Bfs do
    P159V5f:=P159V5Row.elt;
    if IsBound(P159V5Row.commutator_word) then
      P159V5GateWord:=P159V5Row.commutator_word;
    else
      P159V5GateWord:=P159V5Row.word;
    fi;
    P159V5Unit:=Gcd(P159V5u,P159V5Nord)=1;
    P159V5Derived:=P159V5f in P159V5D2;
    P159V5H10:=false; P159V5H11:=false; P159V5Onto:=false;
    P159V5GeneratedOrder:=fail; P159V5Reason:="unit_fail";
    P159V5GateCounts.raw_pair_count:=P159V5GateCounts.raw_pair_count+1;
    if P159V5Unit then
      P159V5GateCounts.unit_pass:=P159V5GateCounts.unit_pass+1;
      P159V5Reason:="derived_fail";
      if P159V5Derived then
        P159V5GateCounts.derived_after_unit_pass:=
          P159V5GateCounts.derived_after_unit_pass+1;
        P159V5ThetaF:=Image(P159V5Theta,P159V5f);
        P159V5H10:=P159V5Paper([P159V5f,P159V5ThetaF])=
          One(P159V5Q2.group);
        P159V5Reason:="hexagon_310_fail";
        if P159V5H10 then
          P159V5GateCounts.hexagon_310_pass:=
            P159V5GateCounts.hexagon_310_pass+1;
          P159V5Ymf:=P159V5Paper([P159V5y^P159V5m,P159V5f]);
          P159V5TauYmf:=Image(P159V5Tau,P159V5Ymf);
          P159V5Tau2Ymf:=Image(P159V5Tau,P159V5TauYmf);
          P159V5H11:=P159V5Paper([P159V5Tau2Ymf,P159V5TauYmf,
            P159V5Ymf])=One(P159V5Q2.group);
          if P159V5WrongTau=fail then
            P159V5TauMutantDisagreements:=P159V5TauMutantDisagreements+1;
          else
            P159V5WrongTauYmf:=Image(P159V5WrongTau,P159V5Ymf);
            P159V5WrongTau2Ymf:=Image(P159V5WrongTau,P159V5WrongTauYmf);
            P159V5WrongH11:=P159V5Paper([P159V5WrongTau2Ymf,
              P159V5WrongTauYmf,P159V5Ymf])=One(P159V5Q2.group);
            if P159V5WrongH11<>P159V5H11 then
              P159V5TauMutantDisagreements:=
                P159V5TauMutantDisagreements+1;
            fi;
          fi;
          P159V5Reason:="hexagon_311_fail";
          if P159V5H11 then
            P159V5GateCounts.hexagon_311_pass:=
              P159V5GateCounts.hexagon_311_pass+1;
            P159V5GenA:=P159V5x^P159V5u;
            P159V5GenB:=P159V5Paper([P159V5f^-1,
              P159V5y^P159V5u,P159V5f]);
            P159V5GeneratedOrder:=Size(Group(P159V5GenA,P159V5GenB));
            P159V5Onto:=P159V5GeneratedOrder=Size(P159V5Q2.group);
            P159V5Reason:="onto_fail";
            if P159V5Onto then
              P159V5GateCounts.onto_pass:=P159V5GateCounts.onto_pass+1;
              P159V5Reason:="pass";
            fi;
          fi;
        fi;
      fi;
    fi;
    if P159V5GeneratedOrder=fail then
      P159V5GeneratedOrderString:=fail;
    else
      P159V5GeneratedOrderString:=String(P159V5GeneratedOrder);
    fi;
    Add(P159V5GateTrace,rec(m:=P159V5m,u:=P159V5u,
      f_coords:=P159V5Row.coords,f_word:=P159V5GateWord,
      unit:=P159V5Unit,derived:=P159V5Derived,
      literal_gentle_hexagon_310:=P159V5H10,
      literal_gentle_hexagon_311:=P159V5H11,
      generated_order_decimal:=P159V5GeneratedOrderString,
      onto:=P159V5Onto,rejection_reason:=P159V5Reason,
      passed:=P159V5Reason="pass"));
  od;
od;
P159V5ExpectedPairCount:=P159V5Nord*Size(P159V5Q2.group);
if Length(P159V5GateTrace)<>P159V5ExpectedPairCount or
   Length(Set(List(P159V5GateTrace,r->[r.m,r.f_coords])))<>
     P159V5ExpectedPairCount then
  Error("PENT159N_V5: gated pair universe omission/duplicate");
fi;
if P159V5TauMutantDisagreements=0 then
  Error("PENT159N_V5: wrong tau word mutant was not discriminated");
fi;
P159V5GateDigest:=P159V5Digest(List(P159V5GateTrace,r->
  rec(m:=r.m,f_coords:=r.f_coords,rejection_reason:=r.rejection_reason)));
P159V5SurvivorsInternal:=[];
for P159V5GateRow in Filtered(P159V5GateTrace,r->r.passed) do
  P159V5Drec:=P159V5Dpap(P159V5GateRow.f_word,P159V5Contexts);
  Add(P159V5SurvivorsInternal,rec(m:=P159V5GateRow.m,
    f_coords:=P159V5GateRow.f_coords,f_word:=P159V5GateRow.f_word,
    defect:=P159V5Drec.correct,
    defect_coords:=P159V5Coords(P159V5Q4Pc,P159V5Drec.correct),
    nonzero:=P159V5Drec.correct<>One(P159V5Q4.group)));
od;
P159V5SurvivorsPublic:=List(P159V5SurvivorsInternal,r->rec(m:=r.m,
  f_coords:=r.f_coords,f_word:=r.f_word,defect_coords:=r.defect_coords,
  nonzero:=r.nonzero));
P159V5SurvivorDigest:=P159V5Digest(P159V5SurvivorsPublic);
P159V5ActualNonzero:=Filtered(P159V5SurvivorsInternal,r->r.nonzero);
Print("PENT159N_P2_V5_GATED_PASS N_ord=",P159V5Nord,
  " raw_pairs=",P159V5ExpectedPairCount," survivors=",
  Length(P159V5SurvivorsInternal)," nonzero_survivors=",
  Length(P159V5ActualNonzero)," coverage_sha256=",P159V5GateDigest,"\n");

#############################################################################
## Receipt.  No p=3 or row36 inference is made by this bounded stage.
#############################################################################

P159V5Phase("WRITE_RECEIPT");
if Length(P159V5ActualNonzero)>0 then
  P159V5Terminal:="PENT159N_P2_ACTUAL_CHARMING_SENSITIVE";
elif Length(P159V5NonzeroInstrument)>0 then
  P159V5Terminal:=
    "PENT159N_P2_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_REQUIRED";
else
  P159V5Terminal:=
    "PENT159N_P2_INSTRUMENT_AND_ACTUAL_CHARMING_BLIND__P3_REQUIRED";
fi;
P159V5Receipt:=rec(
  schema:="d972-pent-interleave-canary-p2/v5",
  date:="2026-08-24",
  role:="Luna producer",
  scope:="corrected finite p=2 Brunnian, complete commutator instrument, and separately gated charming+onto subset; row36/diamond deferred",
  status:="MEASURED_P2_STAGE",
  execution_routing_addendum_159o:=rec(
    rule:="p=2 and p=3 instruments/gated subsets must be reported separately; p=2 blindness never implies all class-3 primes blind",
    p3_required_if_p2_actual_charming_blind:=Length(P159V5ActualNonzero)=0,
    automatic_K2_naming_forbidden:=true),
  provenance:=rec(gap_version:=GAPInfo.Version,nq_version:=P159V4NqVersion,
    nq_executable_sha256:=P159V4BinarySha,
    nq_pcp_api_sha256:=P159V5NqPcpSha,
    stage0_source:=P159V5Stage0,stage0_source_sha256:=P159V5Stage0Sha,
    successful_stage0_run_id:=32647100171,
    successful_stage0_commit:="c8e3bc8dd734d788f8ab9f80773c8503f352c0bf",
    source_path:=P159V5Source,
    source_sha256_measured_at_runtime:=HexSHA256(StringFile(P159V5Source)),
    direct_api:="NqCallANU_NQ record -> NqInitFromTheLeftCollector -> NqPcpGroupByCollector + NqPcpElementByWord(nqrec.Images)",
    epimorphism_source_subgroup_constructed:=false),
  frozen_corrections:=rec(
    original_W2:=rec(status:="ORIGINAL_W2_REJECTED_EXPONENT2_COLLAPSE",
      identity:"gamma4(G) G^2 = G^2 because gamma2(G) <= G^2",
      PB4_quotient:"(C2)^6",PB4_class:=1,F2_order:=4,PB3_order:=8,
      executed_as_class3:=false),
    raw_lie:=rec(status:="RAW_LIE_CALIBRATION_ONLY",
      imported_as_finite_survival_evidence:=false),
    corrected_window:="D4_2(G)=G^4 gamma2(G)^2 gamma4(G)",
    dpap_paper_factor_order:=["phi12_3_4^-1","phi1_2_34^-1",
      "phi234","phi1_23_4","phi123"],
    dpap_definition:="RHS^-1 * LHS",
    paper_product_native_rule:="paper f1*...*fk evaluates as native GAP fk*...*f1",
    tau_y_paper:="y^-1*x^-1",tau_y_native_gap:="X^-1*Y^-1",
    rejected_tau_native_mutant:="(X*Y)^-1"),
  quotients:=rec(Q2:=P159V5PublicPcReceipt(P159V5Q2Receipt),
    Q3:=P159V5PublicPcReceipt(P159V5Q3Receipt),
    Q4:=P159V5PublicPcReceipt(P159V5Q4Receipt)),
  marked_maps:=rec(
    deletion_count:=4,coface_count:=5,
    deletion_table:=P159V5DelWords,
    deletion_table_sha256:=P159V5Digest(P159V5DelWords),
    coface_table:=P159V5CofWords,
    coface_table_sha256:=P159V5Digest(P159V5CofWords),
    a18_F2_context_words_by_slot_0_to_4:=P159V5ContextWords,
    deletions:=List(P159V5DeletionMaps,P159V5PublicMap),
    cofaces:=List(P159V5CofaceMaps,P159V5PublicMap),
    F2_to_PB3:=P159V5PublicMap(P159V5IotaMap)),
  brunnian_degree3:=rec(
    finite_degree3_deletion_kernel_order_decimal:=
      String(Size(P159V5Degree3BrKernel)),
    integral_Dpap_image_order_decimal:=String(Size(P159V5DpapImage)),
    integral_Dpap_image_generator_coords:=List(
      GeneratorsOfGroup(P159V5DpapImage),g->P159V5Coords(P159V5Q4Pc,g)),
    concrete_first_nonzero:=P159V5FirstNonzeroPublic,
    canary1_pass:=Length(P159V5NonzeroInstrument)>0,
    claim_scope:="Dpap words are integral Brunnian words by four exact deletions; their measured subgroup is contained in gamma3 and in every deletion kernel"),
  commutator_instrument:=rec(
    universe:="every element of DerivedSubgroup(Q2) exactly once",
    over_universe_not_all_charming:=true,Q2_order:=Size(P159V5Q2.group),
    derived_order:=Size(P159V5D2),enumerated_count:=Length(P159V5InstrumentInternal),
    no_omission_duplicate:=true,identity_only_rejected:=true,
    Q2_bfs_count:=Length(P159V5Bfs),Q2_bfs_sha256:=P159V5BfsDigest,
    coverage_sha256:=P159V5InstrumentDigest,
    nonzero_count:=Length(P159V5NonzeroInstrument),
    distinct_nonzero_image_count:=Length(Set(List(P159V5NonzeroInstrument,
      r->r.defect_coords))),
    defect_histogram:=P159V5Histogram(P159V5InstrumentInternal,
      "defect_coords"),
    canonical_first_nonzero:=P159V5FirstNonzeroPublic,
    rows:=P159V5InstrumentPublic),
  actual_charming_onto_gate:=rec(
    m_residue_range:=[0..P159V5Nord-1],N_ord:=P159V5Nord,
    f_universe_count:=Size(P159V5Q2.group),
    raw_pair_count:=P159V5ExpectedPairCount,evaluated_count:=Length(P159V5GateTrace),
    no_omission_duplicate:=true,
    sequential_gate_counts:=P159V5GateCounts,
    coverage_sha256:=P159V5GateDigest,
    surviving_count:=Length(P159V5SurvivorsInternal),
    survivor_sha256:=P159V5SurvivorDigest,
    nonzero_survivor_count:=Length(P159V5ActualNonzero),
    actual_charming_witness_exists:=Length(P159V5ActualNonzero)>0,
    defect_histogram:=P159V5Histogram(P159V5SurvivorsInternal,
      "defect_coords"),
    survivors:=P159V5SurvivorsPublic,
    full_gate_trace:=P159V5GateTrace),
  destructive_controls:=rec(
    wrong_order_mutant:="phi123*phi1_23_4*phi234*(phi12_3_4*phi1_2_34)^-1",
    wrong_order_noncommuting_discriminator:=P159V5WrongOrderDiscriminator,
    lhs_rhs_inversion_checked_in_every_Dpap_call:=true,
    lhs_rhs_inversion_discriminator:=P159V5InversionDiscriminator,
    deletion_expected_count:=4,deletion_actual_count:=Length(P159V5DeletionMaps),
    one_deletion_omitted_rejected:=Length(P159V5DeletionMaps)=4,
    strand_renumbering_exact_table_gate:=true,
    coface_slot_order_exact_gate:=true,
    swapped_coface_discriminator:=P159V5SwappedCofaceDiscriminator,
    wrong_tau_mutant_disagreement_count:=P159V5TauMutantDisagreements,
    identity_only_canary_rejected:=Length(P159V5DerivedRows)>1,
    charming_without_onto_rejected:=true,
    row35_37_substitution_not_in_scope:=true,
    single_representative_not_reported_as_fibre:=true),
  deferred:=rec(row36_full_fibre:="NOT_IN_V5_P2_BOUNDED_STAGE",
    p_specific_M_containment:="NOT_IN_V5_P2_BOUNDED_STAGE",
    K1_intersection_isolation_diamond:="NOT_IN_V5_P2_BOUNDED_STAGE",
    claim_cover_pent_canary_2:="NOT_IN_V5_P2_BOUNDED_STAGE",
    p3_instrument:="ROUTE_AFTER_P2_RECEIPT_IF_REQUIRED"),
  firewall:=rec(checker_source_opened_or_imported:=false,
    checker_verdict_opened_or_imported:=false,
    checker_report_opened_or_imported:=false,git_used:=false,
    gha_dispatched_by_child:=false,workflow_edited:=false,es7ops_used:=false,
    main_sol_reply_edited:=false,v1_v2_v3_v4_edited:=false),
  runtime_ms:=Runtime(),
  terminal_token:=P159V5Terminal);

P159V5Write:=P159V5CheckedWrite(P159V5Output,P159V5Receipt);
Print("PENT159N_P2_V5_RECEIPT_WRITTEN path=",P159V5Output,
  " bytes=",P159V5Write.bytes," sha256=",P159V5Write.sha256,"\n");
Print("PENT159N_P2_V5_FINAL_MARKER terminal=",P159V5Receipt.terminal_token,
  " q2_order=",Size(P159V5Q2.group)," q3_order=",Size(P159V5Q3.group),
  " q4_order=",Size(P159V5Q4.group)," instrument_nonzero=",
  Length(P159V5NonzeroInstrument)," gated_nonzero=",
  Length(P159V5ActualNonzero)," runtime_ms=",Runtime(),"\n");
