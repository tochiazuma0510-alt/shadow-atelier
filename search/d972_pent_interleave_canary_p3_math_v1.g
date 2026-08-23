#############################################################################
## D972 corrected pentagon-interleave canary, finite p=3 stage v1.
##
## Producer-only standalone mathematical source, derived mechanically from the
## authenticated successful p=2 v9 effective source.  It reads no task checker,
## checker verdict, or checker report.  It reuses only the frozen authenticated
## NQ portability stage v4, then constructs the marked D4_3 quotients through
## the same direct NQ record/collector API.  It never forms the fp source
## subgroup used by NqEpimorphismByNqOutput.
#############################################################################

P159P3V1Source := "search/d972_pent_interleave_canary_p3_math_v1.g";
P159P3V1Output := "ci/out/d972_pent_interleave_canary_p3_receipt_v1_20260824.json";
P159P3V1Stage0 := "search/d972_pent_interleave_canary_stage0_v4.g";
P159P3V1Stage0Sha :=
  "eefb7b78a1b1d69634642db85cdbf9ebffae4e871fa5c7008d20b92117374657";
P159P3V1NqPcpSha :=
  "dc751b35a3106a30f7cf7d670187584c4f01db0c7b6323c469226a68965ad7e1";
P159P3V1Prime := 3;
P159P3V1P2TriggerRun := 32651230906;
P159P3V1P2ReceiptBytes := 211971;
P159P3V1P2ReceiptSha :=
  "bc1e3e0e610f6043567017b220c4e7947da9c5541a2130dbd63116b28ea9c84e";
P159P3V1P2RunLogBytes := 7855;
P159P3V1P2RunLogSha :=
  "b93a3a082d15e50263e86be0268320fbd6b49b7de5428c59e53865d9ec8b0f91";
P159P3V1Start := Runtime();

P159P3V1RequireFileSha := function(path,expected,label)
  local raw,got;
  raw:=StringFile(path);
  if raw=fail then Error("PENT159N_P3_V1: missing ",label," at ",path); fi;
  got:=HexSHA256(raw);
  if got<>expected then
    Error("PENT159N_P3_V1: ",label," SHA drift: ",got);
  fi;
  return got;
end;

P159P3V1RequireFileSha(P159P3V1Stage0,P159P3V1Stage0Sha,
  "frozen authenticated direct-NQ stage0 v4");
Read(P159P3V1Stage0);
Print("PENT159N_P3_V1_STAGE0_REPLAY_PASS source=",P159P3V1Stage0,
  " sha256=",P159P3V1Stage0Sha," runtime_ms=",Runtime(),"\n");

P159P3V1NqPcpPath:=Concatenation(P159V4NqPath,"gap/nqpcp.gi");
P159P3V1RequireFileSha(P159P3V1NqPcpPath,P159P3V1NqPcpSha,
  "NQ direct marked-image pc implementation");
if not IsBoundGlobal("NqCallANU_NQ") or
   not IsBoundGlobal("NqInitFromTheLeftCollector") or
   not IsBoundGlobal("NqPcpGroupByCollector") or
   not IsBoundGlobal("NqPcpElementByWord") then
  Error("PENT159N_P3_V1: required direct NQ record/collector API unavailable");
fi;
Print("PENT159N_P3_V1_MARKED_API_PIN_PASS nqpcp_sha256=",
  P159P3V1NqPcpSha," api=NqCallANU_NQ+NqInitFromTheLeftCollector+",
  "NqPcpGroupByCollector+NqPcpElementByWord\n");
if P159P3V1Prime<>3 then Error("PENT159N_P3_V1: prime pin drift"); fi;
Print("PENT159N_P3_V1_LAW_PIN_PASS prime=3 law=D4_3(G)=G^9*gamma2(G)^3*gamma4(G) identical_relators=u^9,Comm(u,v)^3 class_bound=3 p2_trigger_run=",
  P159P3V1P2TriggerRun," p2_receipt_sha256=",P159P3V1P2ReceiptSha,"\n");

#############################################################################
## Stable JSON and phase helpers.
#############################################################################

P159P3V1Escape := function(s)
  local z;
  z:=ReplacedString(s,"\\","\\\\");
  z:=ReplacedString(z,"\"","\\\"");
  z:=ReplacedString(z,"\n","\\n");
  z:=ReplacedString(z,"\r","\\r");
  z:=ReplacedString(z,"\t","\\t");
  return z;
end;

P159P3V1Json := function(x)
  local names,parts,n;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",P159P3V1Escape(x),"\"");
  fi;
  if IsRecord(x) then
    names:=ShallowCopy(RecNames(x)); Sort(names);
    parts:=[];
    for n in names do
      Add(parts,Concatenation(P159P3V1Json(n),":",P159P3V1Json(x.(n))));
    od;
    return Concatenation("{",JoinStringsWithSeparator(parts,","),"}");
  fi;
  if IsList(x) then
    return Concatenation("[",JoinStringsWithSeparator(
      List(x,P159P3V1Json),","),"]");
  fi;
  Error("PENT159N_P3_V1: unsupported JSON value");
end;

P159P3V1Digest := x -> HexSHA256(P159P3V1Json(x));

P159P3V1CheckedWrite := function(path,obj)
  local expected,f,raw;
  expected:=Concatenation(P159P3V1Json(obj),"\n");
  f:=OutputTextFile(path,false);
  if f=fail then Error("PENT159N_P3_V1: cannot open output ",path); fi;
  SetPrintFormattingStatus(f,false);
  PrintTo(f,expected); CloseStream(f);
  raw:=StringFile(path);
  if raw=fail or raw<>expected then
    Error("PENT159N_P3_V1: closed-write readback mismatch ",path);
  fi;
  return rec(bytes:=Length(raw),sha256:=HexSHA256(raw));
end;

P159P3V1Phase := function(label)
  Print("PENT159N_P3_V1_PHASE ",label," runtime_ms=",Runtime(),
    " elapsed_ms=",Runtime()-P159P3V1Start,"\n");
  if IsBoundGlobal("FlushAllStreams") then CallFuncList(ValueGlobal("FlushAllStreams"),[]); fi;
end;

P159P3V1Bool := function(b,label)
  if not b then Error("PENT159N_P3_V1: failed gate ",label); fi;
  return true;
end;

#############################################################################
## Signed words, paper multiplication, and faithful pure-braid presentation.
#############################################################################

P159P3V1Reduce := function(w)
  local out,x;
  out:=[];
  for x in w do
    if x=0 then Error("PENT159N_P3_V1: zero signed letter"); fi;
    if Length(out)>0 and out[Length(out)]=-x then
      Remove(out,Length(out));
    else
      Add(out,x);
    fi;
  od;
  return out;
end;

P159P3V1InvWord := w -> P159P3V1Reduce(List(Reversed(w),x->-x));

P159P3V1SubWord := function(w,imgs)
  local out,x;
  out:=[];
  for x in w do
    if AbsInt(x)>Length(imgs) then
      Error("PENT159N_P3_V1: signed-word image index drift");
    fi;
    if x>0 then Append(out,imgs[x]);
    else Append(out,P159P3V1InvWord(imgs[-x])); fi;
    out:=P159P3V1Reduce(out);
  od;
  return out;
end;

P159P3V1NativeWordEval := function(w,gens)
  local z,x;
  z:=One(gens[1]);
  for x in w do
    if x>0 then z:=z*gens[x]; else z:=z*gens[-x]^-1; fi;
  od;
  return z;
end;

## Paper f1*f2*...*fk is native GAP fk*...*f2*f1 in this repository.
P159P3V1Paper := function(xs)
  local z,i;
  if Length(xs)=0 then Error("PENT159N_P3_V1: empty paper product"); fi;
  z:=One(xs[1]);
  for i in Reversed([1..Length(xs)]) do z:=z*xs[i]; od;
  return z;
end;

P159P3V1PaperWordEval := function(w,gens)
  local factors,x;
  if Length(w)=0 then return One(gens[1]); fi;
  factors:=[];
  for x in w do
    if x>0 then Add(factors,gens[x]); else Add(factors,gens[-x]^-1); fi;
  od;
  return P159P3V1Paper(factors);
end;

P159P3V1ArtinStep := function(rank,letter)
  local imgs,i;
  imgs:=List([1..rank],i->[i]); i:=AbsInt(letter);
  if i<1 or i>=rank then Error("PENT159N_P3_V1: Artin index drift"); fi;
  if letter>0 then
    imgs[i]:=[i,i+1,-i]; imgs[i+1]:=[i];
  else
    imgs[i]:=[i+1]; imgs[i+1]:=[-(i+1),i,i+1];
  fi;
  return imgs;
end;

P159P3V1ArtinImages := function(rank,w)
  local imgs,x,step;
  imgs:=List([1..rank],i->[i]);
  for x in w do
    step:=P159P3V1ArtinStep(rank,x);
    imgs:=List(imgs,v->P159P3V1SubWord(v,step));
  od;
  return imgs;
end;

P159P3V1ArtinIdentity := function(rank,w)
  return P159P3V1ArtinImages(rank,w)=List([1..rank],i->[i]);
end;

P159P3V1PairList := function(rank)
  local ans,i,j;
  ans:=[];
  for i in [1..rank-1] do
    for j in [i+1..rank] do Add(ans,[i,j]); od;
  od;
  return ans;
end;

P159P3V1PairIndex := function(rank,pair)
  local p;
  p:=Position(P159P3V1PairList(rank),pair);
  if p=fail then Error("PENT159N_P3_V1: invalid pure pair"); fi;
  return p;
end;

P159P3V1AijBraid := function(i,j)
  local w,k;
  w:=[];
  if j-i>1 then for k in Reversed([i+1..j-1]) do Add(w,k); od; fi;
  Add(w,i); Add(w,i);
  if j-i>1 then for k in [i+1..j-1] do Add(w,-k); od; fi;
  return w;
end;

P159P3V1ExpandPure := function(rank,w)
  return P159P3V1SubWord(w,List(P159P3V1PairList(rank),
    p->P159P3V1AijBraid(p[1],p[2])));
end;

P159P3V1PureRelations := function(rank)
  local pairs,oldpairs,oldrels,mapold,rels,kmaps,p,g,act,k,h;
  if rank=2 then return []; fi;
  pairs:=P159P3V1PairList(rank);
  oldpairs:=P159P3V1PairList(rank-1);
  oldrels:=P159P3V1PureRelations(rank-1);
  mapold:=List(oldpairs,p->P159P3V1PairIndex(rank,p));
  rels:=List(oldrels,w->P159P3V1SubWord(w,List(mapold,x->[x])));
  kmaps:=List([1..rank-1],k->[P159P3V1PairIndex(rank,[k,rank])]);
  for p in oldpairs do
    g:=P159P3V1PairIndex(rank,p);
    act:=P159P3V1ArtinImages(rank-1,P159P3V1AijBraid(p[1],p[2]));
    for k in [1..rank-1] do
      h:=P159P3V1PairIndex(rank,[k,rank]);
      Add(rels,P159P3V1Reduce(Concatenation([-g,h,g],
        P159P3V1InvWord(P159P3V1SubWord(act[k],kmaps)))));
    od;
  od;
  return rels;
end;

P159P3V1BuildPureFp := function(rank)
  local pairs,labels,F,fg,rels,fp;
  pairs:=P159P3V1PairList(rank);
  labels:=List(pairs,p->Concatenation("a",String(p[1]),String(p[2])));
  F:=FreeGroup(labels); fg:=GeneratorsOfGroup(F);
  rels:=P159P3V1PureRelations(rank);
  if ForAny(rels,w->not P159P3V1ArtinIdentity(rank,
      P159P3V1ExpandPure(rank,w))) then
    Error("PENT159N_P3_V1: faithful Artin replay failed PB",rank);
  fi;
  fp:=F/List(rels,w->P159P3V1NativeWordEval(w,fg));
  return rec(rank:=rank,pairs:=pairs,labels:=labels,relations:=rels,
    relation_count:=Length(rels),group:=fp,gens:=GeneratorsOfGroup(fp),
    artin_replay:=true);
end;

P159P3V1CofaceGenerator := function(rank,slot,pair)
  local i,j,ii,jj;
  i:=pair[1]; j:=pair[2];
  if slot=0 then return [P159P3V1PairIndex(rank+1,[i+1,j+1])]; fi;
  if slot=rank+1 then return [P159P3V1PairIndex(rank+1,[i,j])]; fi;
  if slot<1 or slot>rank then Error("PENT159N_P3_V1: coface slot drift"); fi;
  if i=slot then
    return [P159P3V1PairIndex(rank+1,[slot,j+1]),
      P159P3V1PairIndex(rank+1,[slot+1,j+1])];
  elif j=slot then
    return [P159P3V1PairIndex(rank+1,[i,slot]),
      P159P3V1PairIndex(rank+1,[i,slot+1])];
  fi;
  ii:=i; jj:=j;
  if ii>slot then ii:=ii+1; fi;
  if jj>slot then jj:=jj+1; fi;
  return [P159P3V1PairIndex(rank+1,[ii,jj])];
end;

P159P3V1Cofaces := function(rank)
  return List([0..rank+1],s->List(P159P3V1PairList(rank),
    p->P159P3V1CofaceGenerator(rank,s,p)));
end;

P159P3V1DeleteGenerator := function(rank,strand,pair)
  local i,j;
  i:=pair[1]; j:=pair[2];
  if strand=i or strand=j then return []; fi;
  if i>strand then i:=i-1; fi;
  if j>strand then j:=j-1; fi;
  return [P159P3V1PairIndex(rank-1,[i,j])];
end;

P159P3V1Deletions := function(rank)
  return List([1..rank],s->List(P159P3V1PairList(rank),
    p->P159P3V1DeleteGenerator(rank,s,p)));
end;

#############################################################################
## Direct marked D4_3 quotients.  The identical laws are literal and ordered.
#############################################################################

P159P3V1EvalExtRep := function(w,imgs)
  local e,z,i,k,n;
  e:=ExtRepOfObj(w); z:=One(imgs[1]); i:=1;
  while i<=Length(e) do
    k:=e[i]; n:=e[i+1];
    if not IsInt(k) or not IsInt(n) or k<1 or k>Length(imgs) then
      Error("PENT159N_P3_V1: malformed fp relator external representation");
    fi;
    z:=z*imgs[k]^n; i:=i+2;
  od;
  return z;
end;

P159P3V1BuildD43 := function(name,presentation)
  local sourceF,sourceGens,sourceRels,r,ext,eg,mapped,u,v,E,idgens,
    nqrec,coll,Q,marks;
  sourceF:=FreeGroupOfFpGroup(presentation.group);
  sourceGens:=GeneratorsOfGroup(sourceF);
  sourceRels:=RelatorsOfFpGroup(presentation.group);
  r:=Length(sourceGens);
  if r<>Length(presentation.labels) then
    Error("PENT159N_P3_V1: source generator/label count drift ",name);
  fi;
  ext:=FreeGroup(Concatenation(presentation.labels,
    [Concatenation("id_u_",name),Concatenation("id_v_",name)]));
  eg:=GeneratorsOfGroup(ext);
  mapped:=List(sourceRels,w->P159P3V1EvalExtRep(w,eg{[1..r]}));
  u:=eg[r+1]; v:=eg[r+2];
  E:=ext/Concatenation(mapped,[u^9,Comm(u,v)^3]);
  idgens:=[u,v];
  Print("PENT159N_P3_V1_NQ_CALL_BEGIN name=",name,
    " ordinary_generators=",r," source_relators=",Length(sourceRels),
    " identical_relators=u^9,Comm(u,v)^3 class_bound=3 runtime_ms=",
    Runtime(),"\n");
  if IsBoundGlobal("FlushAllStreams") then CallFuncList(ValueGlobal("FlushAllStreams"),[]); fi;
  nqrec:=NqCallANU_NQ(rec(group:=E,idgens:=idgens,class:=3));
  Print("PENT159N_P3_V1_NQ_CALL_RETURN name=",name,
    " nr_pc_generators=",nqrec.NrGenerators,
    " marked_image_count=",Length(nqrec.Images)," runtime_ms=",Runtime(),"\n");
  if nqrec=fail or nqrec.NrGenerators=fail or nqrec.Images=fail or
     Length(nqrec.Images)<>r then
    Error("PENT159N_P3_V1: incomplete direct NQ output ",name);
  fi;
  coll:=NqInitFromTheLeftCollector(nqrec);
  Q:=NqPcpGroupByCollector(coll,nqrec);
  marks:=List(nqrec.Images,w->NqPcpElementByWord(coll,w));
  if not IsPcpGroup(Q) or Size(Group(marks))<>Size(Q) then
    Error("PENT159N_P3_V1: marked pc quotient construction failed ",name);
  fi;
  if NilpotencyClassOfGroup(Q)<>3 then
    Error("PENT159N_P3_V1: quotient class is not exactly three ",name);
  fi;
  if ForAny(presentation.relations,w->
      P159P3V1NativeWordEval(w,marks)<>One(Q)) then
    Error("PENT159N_P3_V1: source braid relation image nonidentity ",name);
  fi;
  return rec(name:=name,group:=Q,marks:=marks,nqrec:=nqrec,collector:=coll,
    presentation:=presentation,ordinary_generator_count:=r,
    source_relator_count:=Length(sourceRels));
end;

P159P3V1Coords := function(pc,x)
  local e;
  e:=ExponentsOfPcElement(pc,x);
  if e=fail then Error("PENT159N_P3_V1: pc coordinate extraction failed"); fi;
  return List(e,Int);
end;

P159P3V1SeriesSizes := function(S)
  return List(S,g->String(Size(g)));
end;

P159P3V1PcReceipt := function(qrec)
  local G,pc,orders,powers,inverses,conj,conjinv,i,j,lcs,jenn,marked;
  G:=qrec.group; pc:=Pcgs(G); orders:=List(RelativeOrders(pc),Int);
  if Length(pc)>200 then Error("PENT159N_P3_V1: pc generator cap exceeded"); fi;
  powers:=List([1..Length(pc)],i->P159P3V1Coords(pc,pc[i]^orders[i]));
  inverses:=List([1..Length(pc)],i->P159P3V1Coords(pc,pc[i]^-1));
  conj:=[]; conjinv:=[];
  if Length(pc)>1 then
    for i in [2..Length(pc)] do
      for j in [1..i-1] do
        Add(conj,rec(i:=i,j:=j,coords:=P159P3V1Coords(pc,pc[i]^pc[j])));
        Add(conjinv,rec(i:=i,j:=j,
          coords:=P159P3V1Coords(pc,pc[i]^(pc[j]^-1))));
      od;
    od;
  fi;
  lcs:=LowerCentralSeriesOfGroup(G);
  if not IsBoundGlobal("JenningsSeries") then
    Error("PENT159N_P3_V1: JenningsSeries unavailable");
  fi;
  jenn:=JenningsSeries(G);
  marked:=List([1..Length(qrec.marks)],i->rec(
    label:=qrec.presentation.labels[i],pair:=qrec.presentation.pairs[i],
    coords:=P159P3V1Coords(pc,qrec.marks[i]),
    inverse_coords:=P159P3V1Coords(pc,qrec.marks[i]^-1)));
  return rec(name:=qrec.name,prime:=3,
    quotient_law:="D4_3(G)=G^9 gamma2(G)^3 gamma4(G)",
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
    lower_central_series_sizes:=P159P3V1SeriesSizes(lcs),
    zassenhaus_jennings_series_sizes:=P159P3V1SeriesSizes(jenn),
    pcgs_internal:=pc,lcs_internal:=lcs,jennings_internal:=jenn);
end;

P159P3V1PublicPcReceipt := function(r)
  local z;
  z:=ShallowCopy(r);
  Unbind(z.pcgs_internal); Unbind(z.lcs_internal); Unbind(z.jennings_internal);
  return z;
end;

P159P3V1MapCertificate := function(name,kind,sourceRec,sourcePc,targetRec,
    targetPc,words)
  local images,h,i;
  images:=List(words,w->P159P3V1NativeWordEval(w,targetRec.marks));
  h:=GroupHomomorphismByImages(sourceRec.group,targetRec.group,
    sourceRec.marks,images);
  if h=fail then Error("PENT159N_P3_V1: map did not descend ",name); fi;
  if ForAny([1..Length(images)],i->Image(h,sourceRec.marks[i])<>images[i]) then
    Error("PENT159N_P3_V1: marked map image drift ",name);
  fi;
  return rec(name:=name,kind:=kind,source:=sourceRec.name,
    target:=targetRec.name,generator_words:=words,
    target_marked_coords:=List(images,x->P159P3V1Coords(targetPc,x)),
    source_pc_images:=List(sourcePc,x->P159P3V1Coords(targetPc,Image(h,x))),
    source_mark_count:=Length(sourceRec.marks),well_defined:=true,
    image_order_decimal:=String(Size(Image(h))),hom_internal:=h);
end;

P159P3V1PublicMap := function(r)
  local z;
  z:=ShallowCopy(r); Unbind(z.hom_internal); return z;
end;

#############################################################################
## Canonical paper-word coverage and literal pentagon residual.
#############################################################################

P159P3V1BfsPaperWords := function(G,x,y)
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
        newword:=P159P3V1Reduce(Concatenation(row.word,[l]));
        Add(rows,rec(elt:=newelt,word:=newword));
      fi;
    od;
    head:=head+1;
  od;
  if Length(rows)<>Size(G) then
    Error("PENT159N_P3_V1: marked BFS does not cover Q2");
  fi;
  pc:=Pcgs(G);
  for row in rows do
    if P159P3V1PaperWordEval(row.word,[x,y])<>row.elt then
      Error("PENT159N_P3_V1: paper BFS word replay drift");
    fi;
    row.coords:=P159P3V1Coords(pc,row.elt);
  od;
  Sort(rows,function(a,b) return a.coords<b.coords; end);
  if Length(Set(List(rows,r->r.coords)))<>Length(rows) then
    Error("PENT159N_P3_V1: duplicate pc coordinate in Q2 BFS");
  fi;
  return rows;
end;

P159P3V1ExponentSums := function(w)
  return [Sum(Filtered(w,x->AbsInt(x)=1),SignInt),
    Sum(Filtered(w,x->AbsInt(x)=2),SignInt)];
end;

P159P3V1NormalizeDerivedWord := function(w,elt,x,y)
  local sums,out,i;
  sums:=P159P3V1ExponentSums(w);
  if sums[1] mod 9<>0 or sums[2] mod 9<>0 then
    Error("PENT159N_P3_V1: quotient-derived word has nonzero abelianization mod 9");
  fi;
  out:=ShallowCopy(w);
  if sums[1]>0 then for i in [1..sums[1]] do Add(out,-1); od;
  elif sums[1]<0 then for i in [1..-sums[1]] do Add(out,1); od; fi;
  if sums[2]>0 then for i in [1..sums[2]] do Add(out,-2); od;
  elif sums[2]<0 then for i in [1..-sums[2]] do Add(out,2); od; fi;
  out:=P159P3V1Reduce(out);
  if P159P3V1ExponentSums(out)<>[0,0] or
     P159P3V1PaperWordEval(out,[x,y])<>elt then
    Error("PENT159N_P3_V1: integral commutator representative normalization failed");
  fi;
  return out;
end;

P159P3V1Dpap := function(word,contexts)
  local vals,A,B,C,E,F,lhs,rhs,correct,mutant,inversionMismatch;
  vals:=List(contexts,c->P159P3V1PaperWordEval(word,c));
  ## slots: 0=phi234, 1=phi12_3_4, 2=phi1_23_4,
  ##        3=phi1_2_34, 4=phi123.
  C:=vals[1]; A:=vals[2]; E:=vals[3]; B:=vals[4]; F:=vals[5];
  lhs:=P159P3V1Paper([C,E,F]);
  rhs:=P159P3V1Paper([B,A]);
  correct:=P159P3V1Paper([A^-1,B^-1,C,E,F]);
  if correct<>P159P3V1Paper([rhs^-1,lhs]) then
    Error("PENT159N_P3_V1: RHS^-1*LHS factor expansion drift");
  fi;
  ## Superseded scratchpad order: F E C (A B)^-1.
  mutant:=P159P3V1Paper([F,E,C,B^-1,A^-1]);
  inversionMismatch:=P159P3V1Paper([lhs^-1,rhs]);
  return rec(correct:=correct,wrong_order_mutant:=mutant,
    lhs_rhs_inversion_mutant:=inversionMismatch,
    factor_values:=vals);
end;

P159P3V1Histogram := function(rows,field)
  local keys,k,out;
  keys:=Set(List(rows,r->r.(field))); out:=[];
  for k in keys do
    Add(out,rec(coords:=k,count:=Number(rows,r->r.(field)=k)));
  od;
  return out;
end;

#############################################################################
## Construct the three p=3 quotients and every required marked map.
#############################################################################

P159P3V1Phase("BUILD_PRESENTATIONS");
P159P3V1F2F:=FreeGroup("x","y");
P159P3V1F2Pres:=rec(rank:=2,pairs:=[[1,2],[2,3]],labels:=["x","y"],
  relations:=[],relation_count:=0,group:=P159P3V1F2F/[],artin_replay:=true);
P159P3V1P3Pres:=P159P3V1BuildPureFp(3);
P159P3V1P4Pres:=P159P3V1BuildPureFp(4);
if P159P3V1P3Pres.relation_count<>2 or P159P3V1P4Pres.relation_count<>11 then
  Error("PENT159N_P3_V1: FN presentation relation-count drift");
fi;

P159P3V1Phase("BUILD_Q2_D4_3");
P159P3V1Q2:=P159P3V1BuildD43("Q2_F2_D4_3",P159P3V1F2Pres);
if Size(P159P3V1Q2.group)<>2187 then
  Error("PENT159N_P3_V1: F2/D4_3 order calibration mismatch");
fi;
P159P3V1Q2Receipt:=P159P3V1PcReceipt(P159P3V1Q2);
Print("PENT159N_P3_V1_Q2_PASS order=2187 class=3 pc_generators=",
  P159P3V1Q2Receipt.pc_generator_count," runtime_ms=",Runtime(),"\n");

P159P3V1Phase("BUILD_Q3_D4_3");
P159P3V1Q3:=P159P3V1BuildD43("Q3_PB3_D4_3",P159P3V1P3Pres);
P159P3V1Q3Receipt:=P159P3V1PcReceipt(P159P3V1Q3);
Print("PENT159N_P3_V1_Q3_PASS order=",Size(P159P3V1Q3.group),
  " class=3 pc_generators=",P159P3V1Q3Receipt.pc_generator_count,
  " runtime_ms=",Runtime(),"\n");

P159P3V1Phase("BUILD_Q4_D4_3");
P159P3V1Q4:=P159P3V1BuildD43("Q4_PB4_D4_3",P159P3V1P4Pres);
P159P3V1Q4Receipt:=P159P3V1PcReceipt(P159P3V1Q4);
Print("PENT159N_P3_V1_Q4_PASS order=",Size(P159P3V1Q4.group),
  " class=3 pc_generators=",P159P3V1Q4Receipt.pc_generator_count,
  " runtime_ms=",Runtime(),"\n");

P159P3V1Phase("BUILD_MARKED_MAPS");
P159P3V1Q2Pc:=P159P3V1Q2Receipt.pcgs_internal;
P159P3V1Q3Pc:=P159P3V1Q3Receipt.pcgs_internal;
P159P3V1Q4Pc:=P159P3V1Q4Receipt.pcgs_internal;
P159P3V1DelWords:=P159P3V1Deletions(4);
P159P3V1CofWords:=P159P3V1Cofaces(3);
P159P3V1ExpectedDelWords:=[
  [[],[],[],[1],[2],[3]],
  [[],[1],[2],[],[],[3]],
  [[1],[],[2],[],[3],[]],
  [[1],[2],[],[3],[],[]]
];
if P159P3V1DelWords<>P159P3V1ExpectedDelWords then
  Error("PENT159N_P3_V1: deletion strand/renumbering table drift");
fi;
P159P3V1DeletionMaps:=List([1..4],i->P159P3V1MapCertificate(
  Concatenation("delete_strand_",String(i)),"ordinary_pure_braid_deletion",
  P159P3V1Q4,P159P3V1Q4Pc,P159P3V1Q3,P159P3V1Q3Pc,P159P3V1DelWords[i]));
P159P3V1CofaceMaps:=List([1..5],i->P159P3V1MapCertificate(
  Concatenation("coface_slot_",String(i-1)),"pure_braid_coface",
  P159P3V1Q3,P159P3V1Q3Pc,P159P3V1Q4,P159P3V1Q4Pc,P159P3V1CofWords[i]));
P159P3V1IotaMap:=P159P3V1MapCertificate("F2_to_PB3_x12_x23",
  "marked_F2_inclusion",P159P3V1Q2,P159P3V1Q2Pc,P159P3V1Q3,P159P3V1Q3Pc,
  [[1],[3]]);
if Size(Image(P159P3V1IotaMap.hom_internal))<>Size(P159P3V1Q2.group) then
  Error("PENT159N_P3_V1: marked Q2 to Q3 map is not injective");
fi;
## The signed coface tables certify the homomorphisms in the faithful Artin
## presentation convention.  The displayed A.18 products themselves are paper
## products, so their two F2 arguments are evaluated with PaperWordEval.
P159P3V1Contexts:=List(P159P3V1CofWords,m->[
  P159P3V1PaperWordEval(m[1],P159P3V1Q4.marks),
  P159P3V1PaperWordEval(m[3],P159P3V1Q4.marks)]);
P159P3V1ContextWords:=List(P159P3V1CofWords,m->[m[1],m[3]]);
P159P3V1ExpectedContextWords:=[
  [[4],[6]],
  [[2,4],[6]],
  [[1,2],[5,6]],
  [[1],[4,5]],
  [[1],[4]]
];
if P159P3V1ContextWords<>P159P3V1ExpectedContextWords then
  Error("PENT159N_P3_V1: printed A.18 coface substitution drift");
fi;
Print("PENT159N_P3_V1_MAPS_PASS deletions=4 cofaces=5",
  " iota_image_order=",Size(Image(P159P3V1IotaMap.hom_internal)),
  " deletion_table_sha256=",P159P3V1Digest(P159P3V1DelWords),
  " coface_table_sha256=",P159P3V1Digest(P159P3V1CofWords),"\n");

#############################################################################
## Complete commutator instrument and the actual charming+onto gate.
#############################################################################

P159P3V1Phase("ENUMERATE_Q2_CANONICAL_WORDS");
P159P3V1x:=P159P3V1Q2.marks[1]; P159P3V1y:=P159P3V1Q2.marks[2];
P159P3V1Bfs:=P159P3V1BfsPaperWords(P159P3V1Q2.group,P159P3V1x,P159P3V1y);
P159P3V1BfsPublic:=List(P159P3V1Bfs,r->rec(coords:=r.coords,word:=r.word));
P159P3V1BfsDigest:=P159P3V1Digest(P159P3V1BfsPublic);
P159P3V1D2:=DerivedSubgroup(P159P3V1Q2.group);
P159P3V1DerivedRows:=Filtered(P159P3V1Bfs,r->r.elt in P159P3V1D2);
if Length(P159P3V1DerivedRows)<>Size(P159P3V1D2) or
   Length(P159P3V1DerivedRows)<=1 then
  Error("PENT159N_P3_V1: complete nontrivial derived-universe gate failed");
fi;
if Order(P159P3V1x)<>9 or Order(P159P3V1y)<>9 then
  Error("PENT159N_P3_V1: marked Q2 generator order is not nine");
fi;
for P159P3V1Row in P159P3V1DerivedRows do
  P159P3V1Row.commutator_word:=P159P3V1NormalizeDerivedWord(
    P159P3V1Row.word,P159P3V1Row.elt,P159P3V1x,P159P3V1y);
od;

P159P3V1Phase("COMPLETE_COMMUTATOR_INSTRUMENT");
P159P3V1Gamma3:=P159P3V1Q4Receipt.lcs_internal[3];
P159P3V1BrKernel:=Kernel(P159P3V1DeletionMaps[1].hom_internal);
for P159P3V1i in [2..4] do
  P159P3V1BrKernel:=Intersection(P159P3V1BrKernel,
    Kernel(P159P3V1DeletionMaps[P159P3V1i].hom_internal));
od;
P159P3V1Degree3BrKernel:=Intersection(P159P3V1Gamma3,P159P3V1BrKernel);
P159P3V1InstrumentInternal:=[];
for P159P3V1Row in P159P3V1DerivedRows do
  P159P3V1Drec:=P159P3V1Dpap(P159P3V1Row.commutator_word,P159P3V1Contexts);
  P159P3V1DeletionBits:=[];
  for P159P3V1i in [1..Length(P159P3V1DeletionMaps)] do
    Add(P159P3V1DeletionBits,Image(P159P3V1DeletionMaps[P159P3V1i].hom_internal,
      P159P3V1Drec.correct)=One(P159P3V1Q3.group));
  od;
  if not ForAll(P159P3V1DeletionBits,b->b) then
    Error("PENT159N_P3_V1: commutator Dpap failed an exact deletion");
  fi;
  if not P159P3V1Drec.correct in P159P3V1Degree3BrKernel then
    Error("PENT159N_P3_V1: Dpap is outside degree-3 deletion kernel");
  fi;
  Add(P159P3V1InstrumentInternal,rec(f:=P159P3V1Row.elt,
    f_coords:=P159P3V1Row.coords,f_word:=P159P3V1Row.commutator_word,
    defect:=P159P3V1Drec.correct,
    defect_coords:=P159P3V1Coords(P159P3V1Q4Pc,P159P3V1Drec.correct),
    nonzero:=P159P3V1Drec.correct<>One(P159P3V1Q4.group),
    four_deletions:=P159P3V1DeletionBits));
od;
if Length(Set(List(P159P3V1InstrumentInternal,r->r.f_coords)))<>
   Size(P159P3V1D2) then
  Error("PENT159N_P3_V1: commutator instrument omission/duplicate");
fi;
P159P3V1InstrumentPublic:=List(P159P3V1InstrumentInternal,r->rec(
  f_coords:=r.f_coords,f_word:=r.f_word,defect_coords:=r.defect_coords,
  nonzero:=r.nonzero,four_deletions:=r.four_deletions));
P159P3V1InstrumentDigest:=P159P3V1Digest(P159P3V1InstrumentPublic);
P159P3V1NonzeroInstrument:=Filtered(P159P3V1InstrumentInternal,r->r.nonzero);
P159P3V1DpapImage:=Subgroup(P159P3V1Q4.group,
  List(P159P3V1InstrumentInternal,r->r.defect));
if not IsSubgroup(P159P3V1Degree3BrKernel,P159P3V1DpapImage) then
  Error("PENT159N_P3_V1: Dpap Brunnian image subgroup containment drift");
fi;
if Length(P159P3V1NonzeroInstrument)>0 then
  P159P3V1FirstNonzero:=P159P3V1NonzeroInstrument[1];
  P159P3V1FirstNonzeroPublic:=rec(f_coords:=P159P3V1FirstNonzero.f_coords,
    f_word:=P159P3V1FirstNonzero.f_word,
    defect_coords:=P159P3V1FirstNonzero.defect_coords,
    four_deletions:=P159P3V1FirstNonzero.four_deletions,
    in_gamma3:=P159P3V1FirstNonzero.defect in P159P3V1Gamma3,
    nonidentity:=true);
else
  P159P3V1FirstNonzeroPublic:=fail;
fi;

## Active noncommuting discriminator for the superseded factor order.  The
## discriminator scans the full finite Q2 word universe, not only f=1 or a
## deletion-blind case.
P159P3V1WrongOrderDiscriminator:=fail;
P159P3V1COrderCanaryGroup:=SymmetricGroup(3);
P159P3V1COrderCanaryA:=One(P159P3V1COrderCanaryGroup);
P159P3V1COrderCanaryB:=One(P159P3V1COrderCanaryGroup);
P159P3V1COrderCanaryC:=One(P159P3V1COrderCanaryGroup);
P159P3V1COrderCanaryE:=(2,3);
P159P3V1COrderCanaryF:=(1,2,3);
P159P3V1COrderCanaryCorrect:=P159P3V1Paper([P159P3V1COrderCanaryA^-1,
  P159P3V1COrderCanaryB^-1,P159P3V1COrderCanaryC,P159P3V1COrderCanaryE,
  P159P3V1COrderCanaryF]);
P159P3V1COrderCanaryMutant:=P159P3V1Paper([P159P3V1COrderCanaryF,
  P159P3V1COrderCanaryE,P159P3V1COrderCanaryC,P159P3V1COrderCanaryB^-1,
  P159P3V1COrderCanaryA^-1]);
P159P3V1COrderCanaryComm:=Comm(P159P3V1COrderCanaryCorrect,
  P159P3V1COrderCanaryMutant);
if P159P3V1COrderCanaryCorrect=P159P3V1COrderCanaryMutant or
   P159P3V1COrderCanaryComm=One(P159P3V1COrderCanaryGroup) then
  Error("PENT159N_P3_V1: independent S3 wrong-order calibration failed");
fi;
P159P3V1COrderCanary:=rec(group:="S3",order:=6,
  factors:=rec(A:=[1,2,3],B:=[1,2,3],C:=[1,2,3],
    E:=List([1..3],i->i^P159P3V1COrderCanaryE),
    F:=List([1..3],i->i^P159P3V1COrderCanaryF)),
  correct_factor_order:=["A^-1","B^-1","C","E","F"],
  mutant_factor_order:=["F","E","C","B^-1","A^-1"],
  correct_image:=List([1..3],i->i^P159P3V1COrderCanaryCorrect),
  mutant_image:=List([1..3],i->i^P159P3V1COrderCanaryMutant),
  commutator_image:=List([1..3],i->i^P159P3V1COrderCanaryComm),
  distinct:=true,noncommuting:=true);
P159P3V1CWrongOrderQ2DistinctCount:=0;
P159P3V1CWrongOrderQ2NoncommutingCount:=0;
P159P3V1InversionDiscriminator:=fail;
P159P3V1SwappedCofaceDiscriminator:=fail;
P159P3V1SwappedContexts:=ShallowCopy(P159P3V1Contexts);
P159P3V1SwapTemp:=P159P3V1SwappedContexts[2];
P159P3V1SwappedContexts[2]:=P159P3V1SwappedContexts[4];
P159P3V1SwappedContexts[4]:=P159P3V1SwapTemp;
for P159P3V1Row in P159P3V1Bfs do
  P159P3V1Drec:=P159P3V1Dpap(P159P3V1Row.word,P159P3V1Contexts);
  P159P3V1SwapDrec:=P159P3V1Dpap(P159P3V1Row.word,P159P3V1SwappedContexts);
  if P159P3V1InversionDiscriminator=fail and
     P159P3V1Drec.correct<>P159P3V1Drec.lhs_rhs_inversion_mutant then
    P159P3V1InversionDiscriminator:=rec(f_coords:=P159P3V1Row.coords,
      f_word:=P159P3V1Row.word,
      correct_coords:=P159P3V1Coords(P159P3V1Q4Pc,P159P3V1Drec.correct),
      inversion_mutant_coords:=P159P3V1Coords(P159P3V1Q4Pc,
        P159P3V1Drec.lhs_rhs_inversion_mutant),distinct:=true);
  fi;
  if P159P3V1SwappedCofaceDiscriminator=fail and
     P159P3V1Drec.correct<>P159P3V1SwapDrec.correct then
    P159P3V1SwappedCofaceDiscriminator:=rec(f_coords:=P159P3V1Row.coords,
      f_word:=P159P3V1Row.word,
      correct_coords:=P159P3V1Coords(P159P3V1Q4Pc,P159P3V1Drec.correct),
      swapped_coords:=P159P3V1Coords(P159P3V1Q4Pc,P159P3V1SwapDrec.correct),
      swapped_slots:=[1,3],distinct:=true);
  fi;
  if P159P3V1Drec.correct<>P159P3V1Drec.wrong_order_mutant then
    P159P3V1CWrongOrderQ2DistinctCount:=P159P3V1CWrongOrderQ2DistinctCount+1;
  fi;
  if Comm(P159P3V1Drec.correct,P159P3V1Drec.wrong_order_mutant)<>
     One(P159P3V1Q4.group) then
    P159P3V1CWrongOrderQ2NoncommutingCount:=
      P159P3V1CWrongOrderQ2NoncommutingCount+1;
  fi;
  if P159P3V1WrongOrderDiscriminator=fail and
     P159P3V1Drec.correct<>P159P3V1Drec.wrong_order_mutant then
    P159P3V1WrongOrderFactorLabels:=["phi12_3_4^-1","phi1_2_34^-1",
      "phi234","phi1_23_4","phi123"];
    P159P3V1WrongOrderFactors:=[P159P3V1Drec.factor_values[2]^-1,
      P159P3V1Drec.factor_values[4]^-1,P159P3V1Drec.factor_values[1],
      P159P3V1Drec.factor_values[3],P159P3V1Drec.factor_values[5]];
    P159P3V1WrongOrderNoncommutingPairs:=[];
    for P159P3V1ControlI in [1..4] do
      for P159P3V1ControlJ in [P159P3V1ControlI+1..5] do
        P159P3V1ControlComm:=Comm(
          P159P3V1WrongOrderFactors[P159P3V1ControlI],
          P159P3V1WrongOrderFactors[P159P3V1ControlJ]);
        if P159P3V1ControlComm<>One(P159P3V1Q4.group) then
          Add(P159P3V1WrongOrderNoncommutingPairs,rec(
            positions:=[P159P3V1ControlI,P159P3V1ControlJ],
            labels:=[P159P3V1WrongOrderFactorLabels[P159P3V1ControlI],
              P159P3V1WrongOrderFactorLabels[P159P3V1ControlJ]],
            commutator_coords:=P159P3V1Coords(P159P3V1Q4Pc,
              P159P3V1ControlComm),noncommuting:=true));
        fi;
      od;
    od;
    if Length(P159P3V1WrongOrderNoncommutingPairs)>0 then
      P159P3V1WrongOrderDiscriminator:=rec(
        source:="actual complete-Q2 coface-derived Dpap row",
        f_coords:=P159P3V1Row.coords,f_word:=P159P3V1Row.word,
        factor_labels:=P159P3V1WrongOrderFactorLabels,
        factor_coords:=List(P159P3V1WrongOrderFactors,
          g->P159P3V1Coords(P159P3V1Q4Pc,g)),
        noncommuting_factor_pairs:=P159P3V1WrongOrderNoncommutingPairs,
        correct_coords:=P159P3V1Coords(P159P3V1Q4Pc,P159P3V1Drec.correct),
        mutant_coords:=P159P3V1Coords(P159P3V1Q4Pc,
          P159P3V1Drec.wrong_order_mutant),
        residual_commutator_coords:=P159P3V1Coords(P159P3V1Q4Pc,
          Comm(P159P3V1Drec.correct,P159P3V1Drec.wrong_order_mutant)),
        residuals_distinct:=true,actual_coface_Dpap_row:=true,
        relevant_factor_noncommutation:=true);
    fi;
  fi;
od;
P159P3V1CWrongOrderFullQ2Equal:=P159P3V1CWrongOrderQ2DistinctCount=0;
P159P3V1CWrongOrderFullQ2Commuting:=P159P3V1CWrongOrderQ2NoncommutingCount=0;
if P159P3V1WrongOrderDiscriminator=fail then
  Error("PENT159N_P3_V1: no actual coface-derived wrong-order discriminator with a noncommuting factor pair");
fi;
Print("PENT159N_P3_V1_WRONG_ORDER_CONTROL_PASS q2_universe=",
  Length(P159P3V1Bfs)," q2_distinct=",P159P3V1CWrongOrderQ2DistinctCount,
  " q2_noncommuting=",P159P3V1CWrongOrderQ2NoncommutingCount,
  " q2_equal_all=",P159P3V1CWrongOrderFullQ2Equal,
  " actual_coface_Dpap_row=true residuals_distinct=true factor_noncommuting_pairs=",
  Length(P159P3V1WrongOrderDiscriminator.noncommuting_factor_pairs),
  " external_S3_calibration_only=true\n");
if P159P3V1InversionDiscriminator=fail then
  Error("PENT159N_P3_V1: LHS/RHS inversion mutant was not discriminated");
fi;
if P159P3V1SwappedCofaceDiscriminator=fail then
  Error("PENT159N_P3_V1: swapped-coface mutant was not discriminated");
fi;
Print("PENT159N_P3_V1_INSTRUMENT_PASS universe=",
  Length(P159P3V1InstrumentInternal)," nonzero=",
  Length(P159P3V1NonzeroInstrument)," defect_image_order=",Size(P159P3V1DpapImage),
  " degree3_deletion_kernel_order=",Size(P159P3V1Degree3BrKernel),
  " coverage_sha256=",P159P3V1InstrumentDigest,"\n");

P159P3V1Phase("COMPLETE_CHARMING_ONTO_GATE");
P159P3V1CA5PureWords:=[[1,2,3],[2,3,1],[3,1,2]];
P159P3V1CA5BraidWords:=List(P159P3V1CA5PureWords,w->
  P159P3V1ExpandPure(3,w));
P159P3V1CA5ArtinImages:=List(P159P3V1CA5BraidWords,w->
  P159P3V1ArtinImages(3,w));
if Length(Set(P159P3V1CA5ArtinImages))<>1 then
  Error("PENT159N_P3_V1: cyclic A.5 native forms differ in Artin action");
fi;
P159P3V1CSigmaFullTwist:=[1,2,1,2,1,2];
if P159P3V1ArtinImages(3,P159P3V1CSigmaFullTwist)<>P159P3V1CA5ArtinImages[1] then
  Error("PENT159N_P3_V1: A.5 forms differ from (sigma1 sigma2)^3");
fi;
for P159P3V1i in [1..3] do
  P159P3V1CA5CommPure:=P159P3V1Reduce(Concatenation(
    P159P3V1InvWord(P159P3V1CA5PureWords[1]),[-P159P3V1i],
    P159P3V1CA5PureWords[1],[P159P3V1i]));
  if not P159P3V1ArtinIdentity(3,P159P3V1ExpandPure(3,P159P3V1CA5CommPure)) then
    Error("PENT159N_P3_V1: A.5 native word is not source-central");
  fi;
od;
P159P3V1CA5Q3Values:=List(P159P3V1CA5PureWords,w->
  P159P3V1NativeWordEval(w,P159P3V1Q3.marks));
if Length(Set(P159P3V1CA5Q3Values))<>1 then
  Error("PENT159N_P3_V1: A.5 native quotient forms differ");
fi;
P159P3V1Q3c:=P159P3V1CA5Q3Values[1];
for P159P3V1i in [1..Length(P159P3V1Q3.marks)] do
  if Comm(P159P3V1Q3c,P159P3V1Q3.marks[P159P3V1i])<>One(P159P3V1Q3.group) then
    Error("PENT159N_P3_V1: pinned A.5 quotient element is not central");
  fi;
od;
P159P3V1CRejectedReversedWords:=[[3,2,1],[2,1,3]];
P159P3V1CRejectedReversedCentralBits:=[];
for P159P3V1CRejectedReversedWord in P159P3V1CRejectedReversedWords do
  P159P3V1CRejectedReversedValue:=P159P3V1NativeWordEval(
    P159P3V1CRejectedReversedWord,P159P3V1Q3.marks);
  P159P3V1CRejectedReversedCentral:=true;
  for P159P3V1i in [1..Length(P159P3V1Q3.marks)] do
    if Comm(P159P3V1CRejectedReversedValue,P159P3V1Q3.marks[P159P3V1i])<>
       One(P159P3V1Q3.group) then P159P3V1CRejectedReversedCentral:=false; fi;
  od;
  Add(P159P3V1CRejectedReversedCentralBits,P159P3V1CRejectedReversedCentral);
od;
if true in P159P3V1CRejectedReversedCentralBits then
  Error("PENT159N_P3_V1: a reversed paper/native mutant was not rejected");
fi;
Print("PENT159N_P3_V1_A5_CENTRAL_PASS displayed_native_forms=2 cyclic_native_forms=3 artin_equal=true sigma_full_twist_equal=true quotient_equal=true central=true reversed_forms=2 reversed_central_all=false\n");
P159P3V1Nord:=Lcm(Order(P159P3V1Q3.marks[1]),Order(P159P3V1Q3.marks[3]),
  Order(P159P3V1Q3c));
if P159P3V1Nord<1 then Error("PENT159N_P3_V1: invalid N_ord"); fi;
P159P3V1z:=P159P3V1Paper([P159P3V1x,P159P3V1y])^-1;
if P159P3V1z<>P159P3V1x^-1*P159P3V1y^-1 then
  Error("PENT159N_P3_V1: correct tau native word drift");
fi;
P159P3V1Theta:=GroupHomomorphismByImages(P159P3V1Q2.group,P159P3V1Q2.group,
  [P159P3V1x,P159P3V1y],[P159P3V1y,P159P3V1x]);
P159P3V1Tau:=GroupHomomorphismByImages(P159P3V1Q2.group,P159P3V1Q2.group,
  [P159P3V1x,P159P3V1y],[P159P3V1y,P159P3V1z]);
if P159P3V1Theta=fail or P159P3V1Tau=fail or
   not IsBijective(P159P3V1Theta) or not IsBijective(P159P3V1Tau) then
  Error("PENT159N_P3_V1: theta/tau automorphism descent failed");
fi;
P159P3V1WrongZ:=(P159P3V1x*P159P3V1y)^-1;
if P159P3V1WrongZ=P159P3V1z then
  Error("PENT159N_P3_V1: rejected tau mutant collapsed to correct tau");
fi;
P159P3V1WrongTau:=GroupHomomorphismByImages(P159P3V1Q2.group,P159P3V1Q2.group,
  [P159P3V1x,P159P3V1y],[P159P3V1y,P159P3V1WrongZ]);
P159P3V1GateTrace:=[];
P159P3V1GateCounts:=rec(raw_pair_count:=0,unit_pass:=0,
  derived_after_unit_pass:=0,hexagon_310_pass:=0,hexagon_311_pass:=0,
  onto_pass:=0);
P159P3V1TauMutantDisagreements:=0;
for P159P3V1m in [0..P159P3V1Nord-1] do
  P159P3V1u:=2*P159P3V1m+1;
  for P159P3V1Row in P159P3V1Bfs do
    P159P3V1f:=P159P3V1Row.elt;
    if IsBound(P159P3V1Row.commutator_word) then
      P159P3V1GateWord:=P159P3V1Row.commutator_word;
    else
      P159P3V1GateWord:=P159P3V1Row.word;
    fi;
    P159P3V1Unit:=Gcd(P159P3V1u,P159P3V1Nord)=1;
    P159P3V1Derived:=P159P3V1f in P159P3V1D2;
    P159P3V1H10:=false; P159P3V1H11:=false; P159P3V1Onto:=false;
    P159P3V1GeneratedOrder:=fail; P159P3V1Reason:="unit_fail";
    P159P3V1GateCounts.raw_pair_count:=P159P3V1GateCounts.raw_pair_count+1;
    if P159P3V1Unit then
      P159P3V1GateCounts.unit_pass:=P159P3V1GateCounts.unit_pass+1;
      P159P3V1Reason:="derived_fail";
      if P159P3V1Derived then
        P159P3V1GateCounts.derived_after_unit_pass:=
          P159P3V1GateCounts.derived_after_unit_pass+1;
        P159P3V1ThetaF:=Image(P159P3V1Theta,P159P3V1f);
        P159P3V1H10:=P159P3V1Paper([P159P3V1f,P159P3V1ThetaF])=
          One(P159P3V1Q2.group);
        P159P3V1Reason:="hexagon_310_fail";
        if P159P3V1H10 then
          P159P3V1GateCounts.hexagon_310_pass:=
            P159P3V1GateCounts.hexagon_310_pass+1;
          P159P3V1Ymf:=P159P3V1Paper([P159P3V1y^P159P3V1m,P159P3V1f]);
          P159P3V1TauYmf:=Image(P159P3V1Tau,P159P3V1Ymf);
          P159P3V1Tau2Ymf:=Image(P159P3V1Tau,P159P3V1TauYmf);
          P159P3V1H11:=P159P3V1Paper([P159P3V1Tau2Ymf,P159P3V1TauYmf,
            P159P3V1Ymf])=One(P159P3V1Q2.group);
          if P159P3V1WrongTau=fail then
            P159P3V1TauMutantDisagreements:=P159P3V1TauMutantDisagreements+1;
          else
            P159P3V1WrongTauYmf:=Image(P159P3V1WrongTau,P159P3V1Ymf);
            P159P3V1WrongTau2Ymf:=Image(P159P3V1WrongTau,P159P3V1WrongTauYmf);
            P159P3V1WrongH11:=P159P3V1Paper([P159P3V1WrongTau2Ymf,
              P159P3V1WrongTauYmf,P159P3V1Ymf])=One(P159P3V1Q2.group);
            if P159P3V1WrongH11<>P159P3V1H11 then
              P159P3V1TauMutantDisagreements:=
                P159P3V1TauMutantDisagreements+1;
            fi;
          fi;
          P159P3V1Reason:="hexagon_311_fail";
          if P159P3V1H11 then
            P159P3V1GateCounts.hexagon_311_pass:=
              P159P3V1GateCounts.hexagon_311_pass+1;
            P159P3V1GenA:=P159P3V1x^P159P3V1u;
            P159P3V1GenB:=P159P3V1Paper([P159P3V1f^-1,
              P159P3V1y^P159P3V1u,P159P3V1f]);
            P159P3V1GeneratedOrder:=Size(Group(P159P3V1GenA,P159P3V1GenB));
            P159P3V1Onto:=P159P3V1GeneratedOrder=Size(P159P3V1Q2.group);
            P159P3V1Reason:="onto_fail";
            if P159P3V1Onto then
              P159P3V1GateCounts.onto_pass:=P159P3V1GateCounts.onto_pass+1;
              P159P3V1Reason:="pass";
            fi;
          fi;
        fi;
      fi;
    fi;
    if P159P3V1GeneratedOrder=fail then
      P159P3V1GeneratedOrderString:=fail;
    else
      P159P3V1GeneratedOrderString:=String(P159P3V1GeneratedOrder);
    fi;
    Add(P159P3V1GateTrace,rec(m:=P159P3V1m,u:=P159P3V1u,
      f_coords:=P159P3V1Row.coords,f_word:=P159P3V1GateWord,
      unit:=P159P3V1Unit,derived:=P159P3V1Derived,
      literal_gentle_hexagon_310:=P159P3V1H10,
      literal_gentle_hexagon_311:=P159P3V1H11,
      generated_order_decimal:=P159P3V1GeneratedOrderString,
      onto:=P159P3V1Onto,rejection_reason:=P159P3V1Reason,
      passed:=P159P3V1Reason="pass"));
  od;
od;
P159P3V1ExpectedPairCount:=P159P3V1Nord*Size(P159P3V1Q2.group);
if Length(P159P3V1GateTrace)<>P159P3V1ExpectedPairCount or
   Length(Set(List(P159P3V1GateTrace,r->[r.m,r.f_coords])))<>
     P159P3V1ExpectedPairCount then
  Error("PENT159N_P3_V1: gated pair universe omission/duplicate");
fi;
if P159P3V1TauMutantDisagreements=0 then
  Error("PENT159N_P3_V1: wrong tau word mutant was not discriminated");
fi;
P159P3V1GateDigest:=P159P3V1Digest(List(P159P3V1GateTrace,r->
  rec(m:=r.m,f_coords:=r.f_coords,rejection_reason:=r.rejection_reason)));
P159P3V1SurvivorsInternal:=[];
for P159P3V1GateRow in Filtered(P159P3V1GateTrace,r->r.passed) do
  P159P3V1Drec:=P159P3V1Dpap(P159P3V1GateRow.f_word,P159P3V1Contexts);
  Add(P159P3V1SurvivorsInternal,rec(m:=P159P3V1GateRow.m,
    f_coords:=P159P3V1GateRow.f_coords,f_word:=P159P3V1GateRow.f_word,
    defect:=P159P3V1Drec.correct,
    defect_coords:=P159P3V1Coords(P159P3V1Q4Pc,P159P3V1Drec.correct),
    nonzero:=P159P3V1Drec.correct<>One(P159P3V1Q4.group)));
od;
P159P3V1SurvivorsPublic:=List(P159P3V1SurvivorsInternal,r->rec(m:=r.m,
  f_coords:=r.f_coords,f_word:=r.f_word,defect_coords:=r.defect_coords,
  nonzero:=r.nonzero));
P159P3V1SurvivorDigest:=P159P3V1Digest(P159P3V1SurvivorsPublic);
P159P3V1ActualNonzero:=Filtered(P159P3V1SurvivorsInternal,r->r.nonzero);
Print("PENT159N_P3_V1_GATED_PASS N_ord=",P159P3V1Nord,
  " raw_pairs=",P159P3V1ExpectedPairCount," survivors=",
  Length(P159P3V1SurvivorsInternal)," nonzero_survivors=",
  Length(P159P3V1ActualNonzero)," coverage_sha256=",P159P3V1GateDigest,"\n");

#############################################################################
## Receipt.  This is the separately routed p=3 instrument/gated stage;
## no all-prime, row36, isolation, or K2 inference is made.
#############################################################################

P159P3V1Phase("WRITE_RECEIPT");
if Length(P159P3V1ActualNonzero)>0 then
  P159P3V1Terminal:="PENT159N_P3_ACTUAL_CHARMING_SENSITIVE__P3_COMPLETE";
elif Length(P159P3V1NonzeroInstrument)>0 then
  P159P3V1Terminal:=
    "PENT159N_P3_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_COMPLETE";
else
  P159P3V1Terminal:=
    "PENT159N_P3_INSTRUMENT_AND_ACTUAL_CHARMING_BLIND__P3_COMPLETE";
fi;
P159P3V1Receipt:=rec(
  schema:="d972-pent-interleave-canary-p3/v1",
  date:="2026-08-24",
  role:="Luna producer",
  scope:="corrected finite p=3 Brunnian, complete commutator instrument, and separately gated charming+onto subset; row36/diamond deferred",
  status:="MEASURED_P3_STAGE",
  execution_routing_addendum_159o:=rec(
    rule:="p=2 and p=3 instruments/gated subsets are reported separately; neither pair of finite measurements implies all class-3 primes blind",
    p2_trigger_run_id:=P159P3V1P2TriggerRun,
    p2_trigger_receipt_bytes:=P159P3V1P2ReceiptBytes,
    p2_trigger_receipt_sha256:=P159P3V1P2ReceiptSha,
    p2_trigger_terminal:="PENT159N_P2_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_REQUIRED",
    p3_executed_due_to_p2_actual_charming_blind:=true,
    p2_and_p3_reported_separately:=true,
    all_class3_prime_inference_forbidden:=true,
    automatic_K2_naming_forbidden:=true),
  provenance:=rec(gap_version:=GAPInfo.Version,nq_version:=P159V4NqVersion,
    nq_executable_sha256:=P159V4BinarySha,
    nq_pcp_api_sha256:=P159P3V1NqPcpSha,
    stage0_source:=P159P3V1Stage0,stage0_source_sha256:=P159P3V1Stage0Sha,
    successful_stage0_run_id:=32647100171,
    successful_stage0_commit:="c8e3bc8dd734d788f8ab9f80773c8503f352c0bf",
    source_path:=P159P3V1Source,
    source_sha256_measured_at_runtime:=HexSHA256(StringFile(P159P3V1Source)),
    derivation_base:="authenticated GHA p2 v9 effective source",
    derivation_base_sha256:="1d020d26a7aedb34a6b2d5732b0d95e36cc13b7c2a5e0424209d012d1695643d",
    p2_trigger_run_id:=P159P3V1P2TriggerRun,
    p2_trigger_receipt_sha256:=P159P3V1P2ReceiptSha,
    p2_trigger_run_log_sha256:=P159P3V1P2RunLogSha,
    direct_api:="NqCallANU_NQ record -> NqInitFromTheLeftCollector -> NqPcpGroupByCollector + NqPcpElementByWord(nqrec.Images)",
    epimorphism_source_subgroup_constructed:=false),
  frozen_corrections:=rec(
    original_W2:=rec(status:="ORIGINAL_W2_REJECTED_EXPONENT2_COLLAPSE",
      identity:="gamma4(G) G^2 = G^2 because gamma2(G) <= G^2",
      PB4_quotient:="(C2)^6",PB4_class:=1,F2_order:=4,PB3_order:=8,
      executed_as_class3:=false),
    raw_lie:=rec(status:="RAW_LIE_CALIBRATION_ONLY",
      imported_as_finite_survival_evidence:=false),
    corrected_window:="D4_3(G)=G^9 gamma2(G)^3 gamma4(G)",
    dpap_paper_factor_order:=["phi12_3_4^-1","phi1_2_34^-1",
      "phi234","phi1_23_4","phi123"],
    dpap_definition:="RHS^-1 * LHS",
    paper_product_native_rule:="paper f1*...*fk evaluates as native GAP fk*...*f1",
    tau_y_paper:="y^-1*x^-1",tau_y_native_gap:="X^-1*Y^-1",
    rejected_tau_native_mutant:="(X*Y)^-1"),
  pb3_full_twist_A5:=rec(
    multiplication_convention:="faithful Artin/native, not global Paper reversal",
    displayed_A5_native_forms:=[[3,1,2],[1,2,3]],
    native_cyclic_forms:=[[1,2,3],[2,3,1],[3,1,2]],
    sigma_word:=[1,2,1,2,1,2],artin_images_equal:=true,
    source_central:=true,quotient_forms_equal:=true,quotient_central:=true,
    quotient_coords:=P159P3V1Coords(P159P3V1Q3Pc,P159P3V1Q3c),
    quotient_order:=Int(Order(P159P3V1Q3c)),
    rejected_global_paper_reversals:=[[3,2,1],[2,1,3]],
    rejected_reversal_central_bits:=P159P3V1CRejectedReversedCentralBits),
  quotients:=rec(Q2:=P159P3V1PublicPcReceipt(P159P3V1Q2Receipt),
    Q3:=P159P3V1PublicPcReceipt(P159P3V1Q3Receipt),
    Q4:=P159P3V1PublicPcReceipt(P159P3V1Q4Receipt)),
  marked_maps:=rec(
    deletion_count:=4,coface_count:=5,
    deletion_table:=P159P3V1DelWords,
    deletion_table_sha256:=P159P3V1Digest(P159P3V1DelWords),
    coface_table:=P159P3V1CofWords,
    coface_table_sha256:=P159P3V1Digest(P159P3V1CofWords),
    a18_F2_context_words_by_slot_0_to_4:=P159P3V1ContextWords,
    deletions:=List(P159P3V1DeletionMaps,P159P3V1PublicMap),
    cofaces:=List(P159P3V1CofaceMaps,P159P3V1PublicMap),
    F2_to_PB3:=P159P3V1PublicMap(P159P3V1IotaMap)),
  brunnian_degree3:=rec(
    finite_degree3_deletion_kernel_order_decimal:=
      String(Size(P159P3V1Degree3BrKernel)),
    integral_Dpap_image_order_decimal:=String(Size(P159P3V1DpapImage)),
    integral_Dpap_image_generator_coords:=List(
      GeneratorsOfGroup(P159P3V1DpapImage),g->P159P3V1Coords(P159P3V1Q4Pc,g)),
    concrete_first_nonzero:=P159P3V1FirstNonzeroPublic,
    canary1_pass:=Length(P159P3V1NonzeroInstrument)>0,
    claim_scope:="Dpap words are integral Brunnian words by four exact deletions; their measured subgroup is contained in gamma3 and in every deletion kernel"),
  commutator_instrument:=rec(
    universe:="every element of DerivedSubgroup(Q2) exactly once",
    over_universe_not_all_charming:=true,Q2_order:=Size(P159P3V1Q2.group),
    derived_order:=Size(P159P3V1D2),enumerated_count:=Length(P159P3V1InstrumentInternal),
    no_omission_duplicate:=true,identity_only_rejected:=true,
    Q2_bfs_count:=Length(P159P3V1Bfs),Q2_bfs_sha256:=P159P3V1BfsDigest,
    coverage_sha256:=P159P3V1InstrumentDigest,
    nonzero_count:=Length(P159P3V1NonzeroInstrument),
    distinct_nonzero_image_count:=Length(Set(List(P159P3V1NonzeroInstrument,
      r->r.defect_coords))),
    defect_histogram:=P159P3V1Histogram(P159P3V1InstrumentInternal,
      "defect_coords"),
    canonical_first_nonzero:=P159P3V1FirstNonzeroPublic,
    rows:=P159P3V1InstrumentPublic),
  actual_charming_onto_gate:=rec(
    m_residue_range:=[0..P159P3V1Nord-1],N_ord:=P159P3V1Nord,
    f_universe_count:=Size(P159P3V1Q2.group),
    raw_pair_count:=P159P3V1ExpectedPairCount,evaluated_count:=Length(P159P3V1GateTrace),
    no_omission_duplicate:=true,
    sequential_gate_counts:=P159P3V1GateCounts,
    coverage_sha256:=P159P3V1GateDigest,
    surviving_count:=Length(P159P3V1SurvivorsInternal),
    survivor_sha256:=P159P3V1SurvivorDigest,
    nonzero_survivor_count:=Length(P159P3V1ActualNonzero),
    actual_charming_witness_exists:=Length(P159P3V1ActualNonzero)>0,
    defect_histogram:=P159P3V1Histogram(P159P3V1SurvivorsInternal,
      "defect_coords"),
    survivors:=P159P3V1SurvivorsPublic,
    full_gate_trace:=P159P3V1GateTrace),
  destructive_controls:=rec(
    wrong_order_mutant:="phi123*phi1_23_4*phi234*(phi12_3_4*phi1_2_34)^-1",
    wrong_order_noncommuting_discriminator:=P159P3V1WrongOrderDiscriminator,
    wrong_order_control_requires_actual_coface_row:=true,
    wrong_order_external_S3_calibration_accepted_as_pass:=false,
    wrong_order_full_Q2_universe_count:=Length(P159P3V1Bfs),
    wrong_order_full_Q2_distinct_count:=P159P3V1CWrongOrderQ2DistinctCount,
    wrong_order_full_Q2_noncommuting_count:=P159P3V1CWrongOrderQ2NoncommutingCount,
    wrong_order_full_Q2_equal_all:=P159P3V1CWrongOrderFullQ2Equal,
    wrong_order_full_Q2_commuting_all:=P159P3V1CWrongOrderFullQ2Commuting,
    wrong_order_external_finite_group_discriminator:=P159P3V1COrderCanary,
    lhs_rhs_inversion_checked_in_every_Dpap_call:=true,
    lhs_rhs_inversion_discriminator:=P159P3V1InversionDiscriminator,
    deletion_expected_count:=4,deletion_actual_count:=Length(P159P3V1DeletionMaps),
    one_deletion_omitted_rejected:=Length(P159P3V1DeletionMaps)=4,
    strand_renumbering_exact_table_gate:=true,
    coface_slot_order_exact_gate:=true,
    swapped_coface_discriminator:=P159P3V1SwappedCofaceDiscriminator,
    wrong_tau_mutant_disagreement_count:=P159P3V1TauMutantDisagreements,
    identity_only_canary_rejected:=Length(P159P3V1DerivedRows)>1,
    charming_without_onto_rejected:=true,
    row35_37_substitution_not_in_scope:=true,
    single_representative_not_reported_as_fibre:=true),
  deferred:=rec(row36_full_fibre:="NOT_IN_P3_V1_BOUNDED_STAGE",
    p_specific_M_containment:="NOT_IN_P3_V1_BOUNDED_STAGE",
    K1_intersection_isolation_diamond:="NOT_IN_P3_V1_BOUNDED_STAGE",
    claim_cover_pent_canary_2:="NOT_IN_P3_V1_BOUNDED_STAGE",
    p3_instrument:="COMPLETED_IN_THIS_RECEIPT"),
  firewall:=rec(checker_source_opened_or_imported:=false,
    checker_verdict_opened_or_imported:=false,
    checker_report_opened_or_imported:=false,git_used:=false,
    gha_dispatched_by_child:=false,workflow_edited:=false,es7ops_used:=false,
    main_sol_reply_edited:=false,p2_v1_through_v9_edited:=false,p3_prior_versions_overwritten:=false),
  runtime_ms:=Runtime(),
  terminal_token:=P159P3V1Terminal);

P159P3V1Write:=P159P3V1CheckedWrite(P159P3V1Output,P159P3V1Receipt);
Print("PENT159N_P3_V1_RECEIPT_WRITTEN path=",P159P3V1Output,
  " bytes=",P159P3V1Write.bytes," sha256=",P159P3V1Write.sha256,"\n");
Print("PENT159N_P3_V1_FINAL_MARKER terminal=",P159P3V1Receipt.terminal_token,
  " q2_order=",Size(P159P3V1Q2.group)," q3_order=",Size(P159P3V1Q3.group),
  " q4_order=",Size(P159P3V1Q4.group)," instrument_nonzero=",
  Length(P159P3V1NonzeroInstrument)," gated_nonzero=",
  Length(P159P3V1ActualNonzero)," runtime_ms=",Runtime(),"\n");
