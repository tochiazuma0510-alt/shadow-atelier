#############################################################################
## D972 corrected pentagon-interleave canary, finite p=3 stage v2.
##
## Producer-only standalone mathematical source, derived mechanically from the
## authenticated successful p=2 v9 effective source.  It reads no task checker,
## checker verdict, or checker report.  It reuses only the frozen authenticated
## NQ portability stage v4, then constructs the marked D4_3 quotients through
## the same direct NQ record/collector API.  It never forms the fp source
## subgroup used by NqEpimorphismByNqOutput.
#############################################################################

P159P3V2Source := "ci/out/d972_pent_interleave_canary_p3_math_effective_v2.g";
P159P3V2Output := "ci/out/d972_pent_interleave_canary_p3_receipt_v2_20260824.json";
P159P3V2Stage0 := "search/d972_pent_interleave_canary_stage0_v4.g";
P159P3V2Stage0Sha :=
  "eefb7b78a1b1d69634642db85cdbf9ebffae4e871fa5c7008d20b92117374657";
P159P3V2NqPcpSha :=
  "dc751b35a3106a30f7cf7d670187584c4f01db0c7b6323c469226a68965ad7e1";
P159P3V2Prime := 3;
P159P3V2P2TriggerRun := 32652710118;
P159P3V2P2ReceiptBytes := 214729;
P159P3V2P2ReceiptSha :=
  "79fc3b392f6e9c514c469c92e230c60d244472a15c252ccc482666943faf387e";
P159P3V2P2RunLogBytes := 7206;
P159P3V2P2RunLogSha :=
  "40c0b9845c012da41c516a9d994e57af407bb993dfa554d9acc2fa9bb54bc0a4";
P159P3V2Start := Runtime();

P159P3V2RequireFileSha := function(path,expected,label)
  local raw,got;
  raw:=StringFile(path);
  if raw=fail then Error("PENT159N_P3_V2: missing ",label," at ",path); fi;
  got:=HexSHA256(raw);
  if got<>expected then
    Error("PENT159N_P3_V2: ",label," SHA drift: ",got);
  fi;
  return got;
end;

P159P3V2RequireFileSha(P159P3V2Stage0,P159P3V2Stage0Sha,
  "frozen authenticated direct-NQ stage0 v4");
Read(P159P3V2Stage0);
Print("PENT159N_P3_V2_STAGE0_REPLAY_PASS source=",P159P3V2Stage0,
  " sha256=",P159P3V2Stage0Sha," runtime_ms=",Runtime(),"\n");

P159P3V2NqPcpPath:=Concatenation(P159V4NqPath,"gap/nqpcp.gi");
P159P3V2RequireFileSha(P159P3V2NqPcpPath,P159P3V2NqPcpSha,
  "NQ direct marked-image pc implementation");
if not IsBoundGlobal("NqCallANU_NQ") or
   not IsBoundGlobal("NqInitFromTheLeftCollector") or
   not IsBoundGlobal("NqPcpGroupByCollector") or
   not IsBoundGlobal("NqPcpElementByWord") then
  Error("PENT159N_P3_V2: required direct NQ record/collector API unavailable");
fi;
Print("PENT159N_P3_V2_MARKED_API_PIN_PASS nqpcp_sha256=",
  P159P3V2NqPcpSha," api=NqCallANU_NQ+NqInitFromTheLeftCollector+",
  "NqPcpGroupByCollector+NqPcpElementByWord\n");
if P159P3V2Prime<>3 then Error("PENT159N_P3_V2: prime pin drift"); fi;
Print("PENT159N_P3_V2_LAW_PIN_PASS prime=3 law=D4_3(G)=G^9*gamma2(G)^3*gamma4(G) identical_relators=u^9,Comm(u,v)^3 class_bound=3 p2_trigger_run=",
  P159P3V2P2TriggerRun," p2_receipt_sha256=",P159P3V2P2ReceiptSha,"\n");

#############################################################################
## Stable JSON and phase helpers.
#############################################################################

P159P3V2Escape := function(s)
  local z;
  z:=ReplacedString(s,"\\","\\\\");
  z:=ReplacedString(z,"\"","\\\"");
  z:=ReplacedString(z,"\n","\\n");
  z:=ReplacedString(z,"\r","\\r");
  z:=ReplacedString(z,"\t","\\t");
  return z;
end;

P159P3V2Json := function(x)
  local names,parts,n;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",P159P3V2Escape(x),"\"");
  fi;
  if IsRecord(x) then
    names:=ShallowCopy(RecNames(x)); Sort(names);
    parts:=[];
    for n in names do
      Add(parts,Concatenation(P159P3V2Json(n),":",P159P3V2Json(x.(n))));
    od;
    return Concatenation("{",JoinStringsWithSeparator(parts,","),"}");
  fi;
  if IsList(x) then
    return Concatenation("[",JoinStringsWithSeparator(
      List(x,P159P3V2Json),","),"]");
  fi;
  Error("PENT159N_P3_V2: unsupported JSON value");
end;

P159P3V2Digest := x -> HexSHA256(P159P3V2Json(x));

P159P3V2CheckedWrite := function(path,obj)
  local expected,f,raw;
  expected:=Concatenation(P159P3V2Json(obj),"\n");
  f:=OutputTextFile(path,false);
  if f=fail then Error("PENT159N_P3_V2: cannot open output ",path); fi;
  SetPrintFormattingStatus(f,false);
  PrintTo(f,expected); CloseStream(f);
  raw:=StringFile(path);
  if raw=fail or raw<>expected then
    Error("PENT159N_P3_V2: closed-write readback mismatch ",path);
  fi;
  return rec(bytes:=Length(raw),sha256:=HexSHA256(raw));
end;

P159P3V2Phase := function(label)
  Print("PENT159N_P3_V2_PHASE ",label," runtime_ms=",Runtime(),
    " elapsed_ms=",Runtime()-P159P3V2Start,"\n");
  if IsBoundGlobal("FlushAllStreams") then CallFuncList(ValueGlobal("FlushAllStreams"),[]); fi;
end;

P159P3V2Bool := function(b,label)
  if not b then Error("PENT159N_P3_V2: failed gate ",label); fi;
  return true;
end;

#############################################################################
## Signed words, paper multiplication, and faithful pure-braid presentation.
#############################################################################

P159P3V2Reduce := function(w)
  local out,x;
  out:=[];
  for x in w do
    if x=0 then Error("PENT159N_P3_V2: zero signed letter"); fi;
    if Length(out)>0 and out[Length(out)]=-x then
      Remove(out,Length(out));
    else
      Add(out,x);
    fi;
  od;
  return out;
end;

P159P3V2InvWord := w -> P159P3V2Reduce(List(Reversed(w),x->-x));

P159P3V2SubWord := function(w,imgs)
  local out,x;
  out:=[];
  for x in w do
    if AbsInt(x)>Length(imgs) then
      Error("PENT159N_P3_V2: signed-word image index drift");
    fi;
    if x>0 then Append(out,imgs[x]);
    else Append(out,P159P3V2InvWord(imgs[-x])); fi;
    out:=P159P3V2Reduce(out);
  od;
  return out;
end;

P159P3V2NativeWordEval := function(w,gens)
  local z,x;
  z:=One(gens[1]);
  for x in w do
    if x>0 then z:=z*gens[x]; else z:=z*gens[-x]^-1; fi;
  od;
  return z;
end;

## Paper f1*f2*...*fk is native GAP fk*...*f2*f1 in this repository.
P159P3V2Paper := function(xs)
  local z,i;
  if Length(xs)=0 then Error("PENT159N_P3_V2: empty paper product"); fi;
  z:=One(xs[1]);
  for i in Reversed([1..Length(xs)]) do z:=z*xs[i]; od;
  return z;
end;

P159P3V2PaperWordEval := function(w,gens)
  local factors,x;
  if Length(w)=0 then return One(gens[1]); fi;
  factors:=[];
  for x in w do
    if x>0 then Add(factors,gens[x]); else Add(factors,gens[-x]^-1); fi;
  od;
  return P159P3V2Paper(factors);
end;

P159P3V2ArtinStep := function(rank,letter)
  local imgs,i;
  imgs:=List([1..rank],i->[i]); i:=AbsInt(letter);
  if i<1 or i>=rank then Error("PENT159N_P3_V2: Artin index drift"); fi;
  if letter>0 then
    imgs[i]:=[i,i+1,-i]; imgs[i+1]:=[i];
  else
    imgs[i]:=[i+1]; imgs[i+1]:=[-(i+1),i,i+1];
  fi;
  return imgs;
end;

P159P3V2ArtinImages := function(rank,w)
  local imgs,x,step;
  imgs:=List([1..rank],i->[i]);
  for x in w do
    step:=P159P3V2ArtinStep(rank,x);
    imgs:=List(imgs,v->P159P3V2SubWord(v,step));
  od;
  return imgs;
end;

P159P3V2ArtinIdentity := function(rank,w)
  return P159P3V2ArtinImages(rank,w)=List([1..rank],i->[i]);
end;

P159P3V2PairList := function(rank)
  local ans,i,j;
  ans:=[];
  for i in [1..rank-1] do
    for j in [i+1..rank] do Add(ans,[i,j]); od;
  od;
  return ans;
end;

P159P3V2PairIndex := function(rank,pair)
  local p;
  p:=Position(P159P3V2PairList(rank),pair);
  if p=fail then Error("PENT159N_P3_V2: invalid pure pair"); fi;
  return p;
end;

P159P3V2AijBraid := function(i,j)
  local w,k;
  w:=[];
  if j-i>1 then for k in Reversed([i+1..j-1]) do Add(w,k); od; fi;
  Add(w,i); Add(w,i);
  if j-i>1 then for k in [i+1..j-1] do Add(w,-k); od; fi;
  return w;
end;

P159P3V2ExpandPure := function(rank,w)
  return P159P3V2SubWord(w,List(P159P3V2PairList(rank),
    p->P159P3V2AijBraid(p[1],p[2])));
end;

P159P3V2PureRelations := function(rank)
  local pairs,oldpairs,oldrels,mapold,rels,kmaps,p,g,act,k,h;
  if rank=2 then return []; fi;
  pairs:=P159P3V2PairList(rank);
  oldpairs:=P159P3V2PairList(rank-1);
  oldrels:=P159P3V2PureRelations(rank-1);
  mapold:=List(oldpairs,p->P159P3V2PairIndex(rank,p));
  rels:=List(oldrels,w->P159P3V2SubWord(w,List(mapold,x->[x])));
  kmaps:=List([1..rank-1],k->[P159P3V2PairIndex(rank,[k,rank])]);
  for p in oldpairs do
    g:=P159P3V2PairIndex(rank,p);
    act:=P159P3V2ArtinImages(rank-1,P159P3V2AijBraid(p[1],p[2]));
    for k in [1..rank-1] do
      h:=P159P3V2PairIndex(rank,[k,rank]);
      Add(rels,P159P3V2Reduce(Concatenation([-g,h,g],
        P159P3V2InvWord(P159P3V2SubWord(act[k],kmaps)))));
    od;
  od;
  return rels;
end;

P159P3V2BuildPureFp := function(rank)
  local pairs,labels,F,fg,rels,fp;
  pairs:=P159P3V2PairList(rank);
  labels:=List(pairs,p->Concatenation("a",String(p[1]),String(p[2])));
  F:=FreeGroup(labels); fg:=GeneratorsOfGroup(F);
  rels:=P159P3V2PureRelations(rank);
  if ForAny(rels,w->not P159P3V2ArtinIdentity(rank,
      P159P3V2ExpandPure(rank,w))) then
    Error("PENT159N_P3_V2: faithful Artin replay failed PB",rank);
  fi;
  fp:=F/List(rels,w->P159P3V2NativeWordEval(w,fg));
  return rec(rank:=rank,pairs:=pairs,labels:=labels,relations:=rels,
    relation_count:=Length(rels),group:=fp,gens:=GeneratorsOfGroup(fp),
    artin_replay:=true);
end;

P159P3V2CofaceGenerator := function(rank,slot,pair)
  local i,j,ii,jj;
  i:=pair[1]; j:=pair[2];
  if slot=0 then return [P159P3V2PairIndex(rank+1,[i+1,j+1])]; fi;
  if slot=rank+1 then return [P159P3V2PairIndex(rank+1,[i,j])]; fi;
  if slot<1 or slot>rank then Error("PENT159N_P3_V2: coface slot drift"); fi;
  if i=slot then
    return [P159P3V2PairIndex(rank+1,[slot,j+1]),
      P159P3V2PairIndex(rank+1,[slot+1,j+1])];
  elif j=slot then
    return [P159P3V2PairIndex(rank+1,[i,slot]),
      P159P3V2PairIndex(rank+1,[i,slot+1])];
  fi;
  ii:=i; jj:=j;
  if ii>slot then ii:=ii+1; fi;
  if jj>slot then jj:=jj+1; fi;
  return [P159P3V2PairIndex(rank+1,[ii,jj])];
end;

P159P3V2Cofaces := function(rank)
  return List([0..rank+1],s->List(P159P3V2PairList(rank),
    p->P159P3V2CofaceGenerator(rank,s,p)));
end;

P159P3V2DeleteGenerator := function(rank,strand,pair)
  local i,j;
  i:=pair[1]; j:=pair[2];
  if strand=i or strand=j then return []; fi;
  if i>strand then i:=i-1; fi;
  if j>strand then j:=j-1; fi;
  return [P159P3V2PairIndex(rank-1,[i,j])];
end;

P159P3V2Deletions := function(rank)
  return List([1..rank],s->List(P159P3V2PairList(rank),
    p->P159P3V2DeleteGenerator(rank,s,p)));
end;

#############################################################################
## Direct marked D4_3 quotients.  The identical laws are literal and ordered.
#############################################################################

P159P3V2EvalExtRep := function(w,imgs)
  local e,z,i,k,n;
  e:=ExtRepOfObj(w); z:=One(imgs[1]); i:=1;
  while i<=Length(e) do
    k:=e[i]; n:=e[i+1];
    if not IsInt(k) or not IsInt(n) or k<1 or k>Length(imgs) then
      Error("PENT159N_P3_V2: malformed fp relator external representation");
    fi;
    z:=z*imgs[k]^n; i:=i+2;
  od;
  return z;
end;

P159P3V2BuildD43 := function(name,presentation)
  local sourceF,sourceGens,sourceRels,r,ext,eg,mapped,u,v,E,idgens,
    nqrec,coll,Q,marks;
  sourceF:=FreeGroupOfFpGroup(presentation.group);
  sourceGens:=GeneratorsOfGroup(sourceF);
  sourceRels:=RelatorsOfFpGroup(presentation.group);
  r:=Length(sourceGens);
  if r<>Length(presentation.labels) then
    Error("PENT159N_P3_V2: source generator/label count drift ",name);
  fi;
  ext:=FreeGroup(Concatenation(presentation.labels,
    [Concatenation("id_u_",name),Concatenation("id_v_",name)]));
  eg:=GeneratorsOfGroup(ext);
  mapped:=List(sourceRels,w->P159P3V2EvalExtRep(w,eg{[1..r]}));
  u:=eg[r+1]; v:=eg[r+2];
  E:=ext/Concatenation(mapped,[u^9,Comm(u,v)^3]);
  idgens:=[u,v];
  Print("PENT159N_P3_V2_NQ_CALL_BEGIN name=",name,
    " ordinary_generators=",r," source_relators=",Length(sourceRels),
    " identical_relators=u^9,Comm(u,v)^3 class_bound=3 runtime_ms=",
    Runtime(),"\n");
  if IsBoundGlobal("FlushAllStreams") then CallFuncList(ValueGlobal("FlushAllStreams"),[]); fi;
  nqrec:=NqCallANU_NQ(rec(group:=E,idgens:=idgens,class:=3));
  Print("PENT159N_P3_V2_NQ_CALL_RETURN name=",name,
    " nr_pc_generators=",nqrec.NrGenerators,
    " marked_image_count=",Length(nqrec.Images)," runtime_ms=",Runtime(),"\n");
  if nqrec=fail or nqrec.NrGenerators=fail or nqrec.Images=fail or
     Length(nqrec.Images)<>r then
    Error("PENT159N_P3_V2: incomplete direct NQ output ",name);
  fi;
  coll:=NqInitFromTheLeftCollector(nqrec);
  Q:=NqPcpGroupByCollector(coll,nqrec);
  marks:=List(nqrec.Images,w->NqPcpElementByWord(coll,w));
  if not IsPcpGroup(Q) or Size(Group(marks))<>Size(Q) then
    Error("PENT159N_P3_V2: marked pc quotient construction failed ",name);
  fi;
  if NilpotencyClassOfGroup(Q)<>3 then
    Error("PENT159N_P3_V2: quotient class is not exactly three ",name);
  fi;
  if ForAny(presentation.relations,w->
      P159P3V2NativeWordEval(w,marks)<>One(Q)) then
    Error("PENT159N_P3_V2: source braid relation image nonidentity ",name);
  fi;
  return rec(name:=name,group:=Q,marks:=marks,nqrec:=nqrec,collector:=coll,
    presentation:=presentation,ordinary_generator_count:=r,
    source_relator_count:=Length(sourceRels));
end;

P159P3V2Coords := function(pc,x)
  local e;
  e:=ExponentsOfPcElement(pc,x);
  if e=fail then Error("PENT159N_P3_V2: pc coordinate extraction failed"); fi;
  return List(e,Int);
end;

P159P3V2SeriesSizes := function(S)
  return List(S,g->String(Size(g)));
end;

P159P3V2PcReceipt := function(qrec)
  local G,pc,orders,powers,inverses,conj,conjinv,i,j,lcs,jenn,marked;
  G:=qrec.group; pc:=Pcgs(G); orders:=List(RelativeOrders(pc),Int);
  if Length(pc)>200 then Error("PENT159N_P3_V2: pc generator cap exceeded"); fi;
  powers:=List([1..Length(pc)],i->P159P3V2Coords(pc,pc[i]^orders[i]));
  inverses:=List([1..Length(pc)],i->P159P3V2Coords(pc,pc[i]^-1));
  conj:=[]; conjinv:=[];
  if Length(pc)>1 then
    for i in [2..Length(pc)] do
      for j in [1..i-1] do
        Add(conj,rec(i:=i,j:=j,coords:=P159P3V2Coords(pc,pc[i]^pc[j])));
        Add(conjinv,rec(i:=i,j:=j,
          coords:=P159P3V2Coords(pc,pc[i]^(pc[j]^-1))));
      od;
    od;
  fi;
  lcs:=LowerCentralSeriesOfGroup(G);
  if not IsBoundGlobal("JenningsSeries") then
    Error("PENT159N_P3_V2: JenningsSeries unavailable");
  fi;
  jenn:=JenningsSeries(G);
  marked:=List([1..Length(qrec.marks)],i->rec(
    label:=qrec.presentation.labels[i],pair:=qrec.presentation.pairs[i],
    coords:=P159P3V2Coords(pc,qrec.marks[i]),
    inverse_coords:=P159P3V2Coords(pc,qrec.marks[i]^-1)));
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
    lower_central_series_sizes:=P159P3V2SeriesSizes(lcs),
    zassenhaus_jennings_series_sizes:=P159P3V2SeriesSizes(jenn),
    pcgs_internal:=pc,lcs_internal:=lcs,jennings_internal:=jenn);
end;

P159P3V2PublicPcReceipt := function(r)
  local z;
  z:=ShallowCopy(r);
  Unbind(z.pcgs_internal); Unbind(z.lcs_internal); Unbind(z.jennings_internal);
  return z;
end;

P159P3V2MapCertificate := function(name,kind,sourceRec,sourcePc,targetRec,
    targetPc,words)
  local images,h,i;
  images:=List(words,w->P159P3V2NativeWordEval(w,targetRec.marks));
  h:=GroupHomomorphismByImages(sourceRec.group,targetRec.group,
    sourceRec.marks,images);
  if h=fail then Error("PENT159N_P3_V2: map did not descend ",name); fi;
  if ForAny([1..Length(images)],i->Image(h,sourceRec.marks[i])<>images[i]) then
    Error("PENT159N_P3_V2: marked map image drift ",name);
  fi;
  return rec(name:=name,kind:=kind,source:=sourceRec.name,
    target:=targetRec.name,generator_words:=words,
    target_marked_coords:=List(images,x->P159P3V2Coords(targetPc,x)),
    source_pc_images:=List(sourcePc,x->P159P3V2Coords(targetPc,Image(h,x))),
    source_mark_count:=Length(sourceRec.marks),well_defined:=true,
    image_order_decimal:=String(Size(Image(h))),hom_internal:=h);
end;

P159P3V2PublicMap := function(r)
  local z;
  z:=ShallowCopy(r); Unbind(z.hom_internal); return z;
end;

#############################################################################
## Canonical paper-word coverage and literal pentagon residual.
#############################################################################

P159P3V2BfsPaperWords := function(G,x,y)
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
        newword:=P159P3V2Reduce(Concatenation(row.word,[l]));
        Add(rows,rec(elt:=newelt,word:=newword));
      fi;
    od;
    head:=head+1;
  od;
  if Length(rows)<>Size(G) then
    Error("PENT159N_P3_V2: marked BFS does not cover Q2");
  fi;
  pc:=Pcgs(G);
  for row in rows do
    if P159P3V2PaperWordEval(row.word,[x,y])<>row.elt then
      Error("PENT159N_P3_V2: paper BFS word replay drift");
    fi;
    row.coords:=P159P3V2Coords(pc,row.elt);
  od;
  Sort(rows,function(a,b) return a.coords<b.coords; end);
  if Length(Set(List(rows,r->r.coords)))<>Length(rows) then
    Error("PENT159N_P3_V2: duplicate pc coordinate in Q2 BFS");
  fi;
  return rows;
end;

P159P3V2ExponentSums := function(w)
  return [Sum(Filtered(w,x->AbsInt(x)=1),SignInt),
    Sum(Filtered(w,x->AbsInt(x)=2),SignInt)];
end;

P159P3V2NormalizeDerivedWord := function(w,elt,x,y)
  local sums,out,i;
  sums:=P159P3V2ExponentSums(w);
  if sums[1] mod 9<>0 or sums[2] mod 9<>0 then
    Error("PENT159N_P3_V2: quotient-derived word has nonzero abelianization mod 9");
  fi;
  out:=ShallowCopy(w);
  if sums[1]>0 then for i in [1..sums[1]] do Add(out,-1); od;
  elif sums[1]<0 then for i in [1..-sums[1]] do Add(out,1); od; fi;
  if sums[2]>0 then for i in [1..sums[2]] do Add(out,-2); od;
  elif sums[2]<0 then for i in [1..-sums[2]] do Add(out,2); od; fi;
  out:=P159P3V2Reduce(out);
  if P159P3V2ExponentSums(out)<>[0,0] or
     P159P3V2PaperWordEval(out,[x,y])<>elt then
    Error("PENT159N_P3_V2: integral commutator representative normalization failed");
  fi;
  return out;
end;

P159P3V2Dpap := function(word,contexts)
  local vals,A,B,C,E,F,lhs,rhs,correct,mutant,inversionMismatch;
  vals:=List(contexts,c->P159P3V2PaperWordEval(word,c));
  ## slots: 0=phi234, 1=phi12_3_4, 2=phi1_23_4,
  ##        3=phi1_2_34, 4=phi123.
  C:=vals[1]; A:=vals[2]; E:=vals[3]; B:=vals[4]; F:=vals[5];
  lhs:=P159P3V2Paper([C,E,F]);
  rhs:=P159P3V2Paper([B,A]);
  correct:=P159P3V2Paper([A^-1,B^-1,C,E,F]);
  if correct<>P159P3V2Paper([rhs^-1,lhs]) then
    Error("PENT159N_P3_V2: RHS^-1*LHS factor expansion drift");
  fi;
  ## Superseded scratchpad order: F E C (A B)^-1.
  mutant:=P159P3V2Paper([F,E,C,B^-1,A^-1]);
  inversionMismatch:=P159P3V2Paper([lhs^-1,rhs]);
  return rec(correct:=correct,wrong_order_mutant:=mutant,
    lhs_rhs_inversion_mutant:=inversionMismatch,
    factor_values:=vals);
end;

P159P3V2Histogram := function(rows,field)
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

P159P3V2Phase("BUILD_PRESENTATIONS");
P159P3V2F2F:=FreeGroup("x","y");
P159P3V2F2Pres:=rec(rank:=2,pairs:=[[1,2],[2,3]],labels:=["x","y"],
  relations:=[],relation_count:=0,group:=P159P3V2F2F/[],artin_replay:=true);
P159P3V2P3Pres:=P159P3V2BuildPureFp(3);
P159P3V2P4Pres:=P159P3V2BuildPureFp(4);
if P159P3V2P3Pres.relation_count<>2 or P159P3V2P4Pres.relation_count<>11 then
  Error("PENT159N_P3_V2: FN presentation relation-count drift");
fi;

P159P3V2Phase("BUILD_Q2_D4_3");
P159P3V2Q2:=P159P3V2BuildD43("Q2_F2_D4_3",P159P3V2F2Pres);
if Size(P159P3V2Q2.group)<>2187 then
  Error("PENT159N_P3_V2: F2/D4_3 order calibration mismatch");
fi;
P159P3V2Q2Receipt:=P159P3V2PcReceipt(P159P3V2Q2);
Print("PENT159N_P3_V2_Q2_PASS order=2187 class=3 pc_generators=",
  P159P3V2Q2Receipt.pc_generator_count," runtime_ms=",Runtime(),"\n");

P159P3V2Phase("BUILD_Q3_D4_3");
P159P3V2Q3:=P159P3V2BuildD43("Q3_PB3_D4_3",P159P3V2P3Pres);
P159P3V2Q3Receipt:=P159P3V2PcReceipt(P159P3V2Q3);
Print("PENT159N_P3_V2_Q3_PASS order=",Size(P159P3V2Q3.group),
  " class=3 pc_generators=",P159P3V2Q3Receipt.pc_generator_count,
  " runtime_ms=",Runtime(),"\n");

P159P3V2Phase("BUILD_Q4_D4_3");
P159P3V2Q4:=P159P3V2BuildD43("Q4_PB4_D4_3",P159P3V2P4Pres);
P159P3V2Q4Receipt:=P159P3V2PcReceipt(P159P3V2Q4);
Print("PENT159N_P3_V2_Q4_PASS order=",Size(P159P3V2Q4.group),
  " class=3 pc_generators=",P159P3V2Q4Receipt.pc_generator_count,
  " runtime_ms=",Runtime(),"\n");

P159P3V2Phase("BUILD_MARKED_MAPS");
P159P3V2Q2Pc:=P159P3V2Q2Receipt.pcgs_internal;
P159P3V2Q3Pc:=P159P3V2Q3Receipt.pcgs_internal;
P159P3V2Q4Pc:=P159P3V2Q4Receipt.pcgs_internal;
P159P3V2DelWords:=P159P3V2Deletions(4);
P159P3V2CofWords:=P159P3V2Cofaces(3);
P159P3V2ExpectedDelWords:=[
  [[],[],[],[1],[2],[3]],
  [[],[1],[2],[],[],[3]],
  [[1],[],[2],[],[3],[]],
  [[1],[2],[],[3],[],[]]
];
if P159P3V2DelWords<>P159P3V2ExpectedDelWords then
  Error("PENT159N_P3_V2: deletion strand/renumbering table drift");
fi;
P159P3V2DeletionMaps:=List([1..4],i->P159P3V2MapCertificate(
  Concatenation("delete_strand_",String(i)),"ordinary_pure_braid_deletion",
  P159P3V2Q4,P159P3V2Q4Pc,P159P3V2Q3,P159P3V2Q3Pc,P159P3V2DelWords[i]));
P159P3V2CofaceMaps:=List([1..5],i->P159P3V2MapCertificate(
  Concatenation("coface_slot_",String(i-1)),"pure_braid_coface",
  P159P3V2Q3,P159P3V2Q3Pc,P159P3V2Q4,P159P3V2Q4Pc,P159P3V2CofWords[i]));
P159P3V2IotaMap:=P159P3V2MapCertificate("F2_to_PB3_x12_x23",
  "marked_F2_inclusion",P159P3V2Q2,P159P3V2Q2Pc,P159P3V2Q3,P159P3V2Q3Pc,
  [[1],[3]]);
if Size(Image(P159P3V2IotaMap.hom_internal))<>Size(P159P3V2Q2.group) then
  Error("PENT159N_P3_V2: marked Q2 to Q3 map is not injective");
fi;
## The signed coface tables certify the homomorphisms in the faithful Artin
## presentation convention.  The displayed A.18 products themselves are paper
## products, so their two F2 arguments are evaluated with PaperWordEval.
P159P3V2Contexts:=List(P159P3V2CofWords,m->[
  P159P3V2PaperWordEval(m[1],P159P3V2Q4.marks),
  P159P3V2PaperWordEval(m[3],P159P3V2Q4.marks)]);
P159P3V2ContextWords:=List(P159P3V2CofWords,m->[m[1],m[3]]);
P159P3V2ExpectedContextWords:=[
  [[4],[6]],
  [[2,4],[6]],
  [[1,2],[5,6]],
  [[1],[4,5]],
  [[1],[4]]
];
if P159P3V2ContextWords<>P159P3V2ExpectedContextWords then
  Error("PENT159N_P3_V2: printed A.18 coface substitution drift");
fi;
Print("PENT159N_P3_V2_MAPS_PASS deletions=4 cofaces=5",
  " iota_image_order=",Size(Image(P159P3V2IotaMap.hom_internal)),
  " deletion_table_sha256=",P159P3V2Digest(P159P3V2DelWords),
  " coface_table_sha256=",P159P3V2Digest(P159P3V2CofWords),"\n");

#############################################################################
## Complete commutator instrument and the actual charming+onto gate.
#############################################################################

P159P3V2Phase("ENUMERATE_Q2_CANONICAL_WORDS");
P159P3V2x:=P159P3V2Q2.marks[1]; P159P3V2y:=P159P3V2Q2.marks[2];
P159P3V2Bfs:=P159P3V2BfsPaperWords(P159P3V2Q2.group,P159P3V2x,P159P3V2y);
P159P3V2BfsPublic:=List(P159P3V2Bfs,r->rec(coords:=r.coords,word:=r.word));
P159P3V2BfsDigest:=P159P3V2Digest(P159P3V2BfsPublic);
P159P3V2D2:=DerivedSubgroup(P159P3V2Q2.group);
P159P3V2DerivedRows:=Filtered(P159P3V2Bfs,r->r.elt in P159P3V2D2);
if Length(P159P3V2DerivedRows)<>Size(P159P3V2D2) or
   Length(P159P3V2DerivedRows)<=1 then
  Error("PENT159N_P3_V2: complete nontrivial derived-universe gate failed");
fi;
if Order(P159P3V2x)<>9 or Order(P159P3V2y)<>9 then
  Error("PENT159N_P3_V2: marked Q2 generator order is not nine");
fi;
for P159P3V2Row in P159P3V2DerivedRows do
  P159P3V2Row.commutator_word:=P159P3V2NormalizeDerivedWord(
    P159P3V2Row.word,P159P3V2Row.elt,P159P3V2x,P159P3V2y);
od;

P159P3V2Phase("COMPLETE_COMMUTATOR_INSTRUMENT");
P159P3V2Gamma3:=P159P3V2Q4Receipt.lcs_internal[3];
P159P3V2BrKernel:=Kernel(P159P3V2DeletionMaps[1].hom_internal);
for P159P3V2i in [2..4] do
  P159P3V2BrKernel:=Intersection(P159P3V2BrKernel,
    Kernel(P159P3V2DeletionMaps[P159P3V2i].hom_internal));
od;
P159P3V2Degree3BrKernel:=Intersection(P159P3V2Gamma3,P159P3V2BrKernel);
P159P3V2InstrumentInternal:=[];
for P159P3V2Row in P159P3V2DerivedRows do
  P159P3V2Drec:=P159P3V2Dpap(P159P3V2Row.commutator_word,P159P3V2Contexts);
  P159P3V2DeletionBits:=[];
  for P159P3V2i in [1..Length(P159P3V2DeletionMaps)] do
    Add(P159P3V2DeletionBits,Image(P159P3V2DeletionMaps[P159P3V2i].hom_internal,
      P159P3V2Drec.correct)=One(P159P3V2Q3.group));
  od;
  if not ForAll(P159P3V2DeletionBits,b->b) then
    Error("PENT159N_P3_V2: commutator Dpap failed an exact deletion");
  fi;
  if not P159P3V2Drec.correct in P159P3V2Degree3BrKernel then
    Error("PENT159N_P3_V2: Dpap is outside degree-3 deletion kernel");
  fi;
  Add(P159P3V2InstrumentInternal,rec(f:=P159P3V2Row.elt,
    f_coords:=P159P3V2Row.coords,f_word:=P159P3V2Row.commutator_word,
    defect:=P159P3V2Drec.correct,
    defect_coords:=P159P3V2Coords(P159P3V2Q4Pc,P159P3V2Drec.correct),
    nonzero:=P159P3V2Drec.correct<>One(P159P3V2Q4.group),
    four_deletions:=P159P3V2DeletionBits));
od;
if Length(Set(List(P159P3V2InstrumentInternal,r->r.f_coords)))<>
   Size(P159P3V2D2) then
  Error("PENT159N_P3_V2: commutator instrument omission/duplicate");
fi;
P159P3V2InstrumentPublic:=List(P159P3V2InstrumentInternal,r->rec(
  f_coords:=r.f_coords,f_word:=r.f_word,defect_coords:=r.defect_coords,
  nonzero:=r.nonzero,four_deletions:=r.four_deletions));
P159P3V2InstrumentDigest:=P159P3V2Digest(P159P3V2InstrumentPublic);
P159P3V2NonzeroInstrument:=Filtered(P159P3V2InstrumentInternal,r->r.nonzero);
P159P3V2DpapImage:=Subgroup(P159P3V2Q4.group,
  List(P159P3V2InstrumentInternal,r->r.defect));
if not IsSubgroup(P159P3V2Degree3BrKernel,P159P3V2DpapImage) then
  Error("PENT159N_P3_V2: Dpap Brunnian image subgroup containment drift");
fi;
if Length(P159P3V2NonzeroInstrument)>0 then
  P159P3V2FirstNonzero:=P159P3V2NonzeroInstrument[1];
  P159P3V2FirstNonzeroPublic:=rec(f_coords:=P159P3V2FirstNonzero.f_coords,
    f_word:=P159P3V2FirstNonzero.f_word,
    defect_coords:=P159P3V2FirstNonzero.defect_coords,
    four_deletions:=P159P3V2FirstNonzero.four_deletions,
    in_gamma3:=P159P3V2FirstNonzero.defect in P159P3V2Gamma3,
    nonidentity:=true);
else
  P159P3V2FirstNonzeroPublic:=fail;
fi;

## Active noncommuting discriminator for the superseded factor order.  The
## discriminator scans the full finite Q2 word universe, not only f=1 or a
## deletion-blind case.
P159P3V2WrongOrderDiscriminator:=fail;
P159P3V2COrderCanaryGroup:=SymmetricGroup(3);
P159P3V2COrderCanaryA:=One(P159P3V2COrderCanaryGroup);
P159P3V2COrderCanaryB:=One(P159P3V2COrderCanaryGroup);
P159P3V2COrderCanaryC:=One(P159P3V2COrderCanaryGroup);
P159P3V2COrderCanaryE:=(2,3);
P159P3V2COrderCanaryF:=(1,2,3);
P159P3V2COrderCanaryCorrect:=P159P3V2Paper([P159P3V2COrderCanaryA^-1,
  P159P3V2COrderCanaryB^-1,P159P3V2COrderCanaryC,P159P3V2COrderCanaryE,
  P159P3V2COrderCanaryF]);
P159P3V2COrderCanaryMutant:=P159P3V2Paper([P159P3V2COrderCanaryF,
  P159P3V2COrderCanaryE,P159P3V2COrderCanaryC,P159P3V2COrderCanaryB^-1,
  P159P3V2COrderCanaryA^-1]);
P159P3V2COrderCanaryComm:=Comm(P159P3V2COrderCanaryCorrect,
  P159P3V2COrderCanaryMutant);
if P159P3V2COrderCanaryCorrect=P159P3V2COrderCanaryMutant or
   P159P3V2COrderCanaryComm=One(P159P3V2COrderCanaryGroup) then
  Error("PENT159N_P3_V2: independent S3 wrong-order calibration failed");
fi;
P159P3V2COrderCanary:=rec(group:="S3",order:=6,
  factors:=rec(A:=[1,2,3],B:=[1,2,3],C:=[1,2,3],
    E:=List([1..3],i->i^P159P3V2COrderCanaryE),
    F:=List([1..3],i->i^P159P3V2COrderCanaryF)),
  correct_factor_order:=["A^-1","B^-1","C","E","F"],
  mutant_factor_order:=["F","E","C","B^-1","A^-1"],
  correct_image:=List([1..3],i->i^P159P3V2COrderCanaryCorrect),
  mutant_image:=List([1..3],i->i^P159P3V2COrderCanaryMutant),
  commutator_image:=List([1..3],i->i^P159P3V2COrderCanaryComm),
  distinct:=true,noncommuting:=true);
P159P3V2CWrongOrderQ2DistinctCount:=0;
P159P3V2CWrongOrderQ2NoncommutingCount:=0;
P159P3V2InversionDiscriminator:=fail;
P159P3V2SwappedCofaceDiscriminator:=fail;
P159P3V2SwappedContexts:=ShallowCopy(P159P3V2Contexts);
P159P3V2SwapTemp:=P159P3V2SwappedContexts[2];
P159P3V2SwappedContexts[2]:=P159P3V2SwappedContexts[4];
P159P3V2SwappedContexts[4]:=P159P3V2SwapTemp;
for P159P3V2Row in P159P3V2Bfs do
  P159P3V2Drec:=P159P3V2Dpap(P159P3V2Row.word,P159P3V2Contexts);
  P159P3V2SwapDrec:=P159P3V2Dpap(P159P3V2Row.word,P159P3V2SwappedContexts);
  if P159P3V2InversionDiscriminator=fail and
     P159P3V2Drec.correct<>P159P3V2Drec.lhs_rhs_inversion_mutant then
    P159P3V2InversionDiscriminator:=rec(f_coords:=P159P3V2Row.coords,
      f_word:=P159P3V2Row.word,
      correct_coords:=P159P3V2Coords(P159P3V2Q4Pc,P159P3V2Drec.correct),
      inversion_mutant_coords:=P159P3V2Coords(P159P3V2Q4Pc,
        P159P3V2Drec.lhs_rhs_inversion_mutant),distinct:=true);
  fi;
  if P159P3V2SwappedCofaceDiscriminator=fail and
     P159P3V2Drec.correct<>P159P3V2SwapDrec.correct then
    P159P3V2SwappedCofaceDiscriminator:=rec(f_coords:=P159P3V2Row.coords,
      f_word:=P159P3V2Row.word,
      correct_coords:=P159P3V2Coords(P159P3V2Q4Pc,P159P3V2Drec.correct),
      swapped_coords:=P159P3V2Coords(P159P3V2Q4Pc,P159P3V2SwapDrec.correct),
      swapped_slots:=[1,3],distinct:=true);
  fi;
  if P159P3V2Drec.correct<>P159P3V2Drec.wrong_order_mutant then
    P159P3V2CWrongOrderQ2DistinctCount:=P159P3V2CWrongOrderQ2DistinctCount+1;
  fi;
  if Comm(P159P3V2Drec.correct,P159P3V2Drec.wrong_order_mutant)<>
     One(P159P3V2Q4.group) then
    P159P3V2CWrongOrderQ2NoncommutingCount:=
      P159P3V2CWrongOrderQ2NoncommutingCount+1;
  fi;
  if P159P3V2WrongOrderDiscriminator=fail and
     P159P3V2Drec.correct<>P159P3V2Drec.wrong_order_mutant then
    P159P3V2WrongOrderFactorLabels:=["phi12_3_4^-1","phi1_2_34^-1",
      "phi234","phi1_23_4","phi123"];
    P159P3V2WrongOrderFactors:=[P159P3V2Drec.factor_values[2]^-1,
      P159P3V2Drec.factor_values[4]^-1,P159P3V2Drec.factor_values[1],
      P159P3V2Drec.factor_values[3],P159P3V2Drec.factor_values[5]];
    P159P3V2WrongOrderNoncommutingPairs:=[];
    for P159P3V2ControlI in [1..4] do
      for P159P3V2ControlJ in [P159P3V2ControlI+1..5] do
        P159P3V2ControlComm:=Comm(
          P159P3V2WrongOrderFactors[P159P3V2ControlI],
          P159P3V2WrongOrderFactors[P159P3V2ControlJ]);
        if P159P3V2ControlComm<>One(P159P3V2Q4.group) then
          Add(P159P3V2WrongOrderNoncommutingPairs,rec(
            positions:=[P159P3V2ControlI,P159P3V2ControlJ],
            labels:=[P159P3V2WrongOrderFactorLabels[P159P3V2ControlI],
              P159P3V2WrongOrderFactorLabels[P159P3V2ControlJ]],
            commutator_coords:=P159P3V2Coords(P159P3V2Q4Pc,
              P159P3V2ControlComm),noncommuting:=true));
        fi;
      od;
    od;
    if Length(P159P3V2WrongOrderNoncommutingPairs)>0 then
      P159P3V2WrongOrderDiscriminator:=rec(
        source:="actual complete-Q2 coface-derived Dpap row",
        f_coords:=P159P3V2Row.coords,f_word:=P159P3V2Row.word,
        factor_labels:=P159P3V2WrongOrderFactorLabels,
        factor_coords:=List(P159P3V2WrongOrderFactors,
          g->P159P3V2Coords(P159P3V2Q4Pc,g)),
        noncommuting_factor_pairs:=P159P3V2WrongOrderNoncommutingPairs,
        correct_coords:=P159P3V2Coords(P159P3V2Q4Pc,P159P3V2Drec.correct),
        mutant_coords:=P159P3V2Coords(P159P3V2Q4Pc,
          P159P3V2Drec.wrong_order_mutant),
        residual_commutator_coords:=P159P3V2Coords(P159P3V2Q4Pc,
          Comm(P159P3V2Drec.correct,P159P3V2Drec.wrong_order_mutant)),
        residuals_distinct:=true,actual_coface_Dpap_row:=true,
        relevant_factor_noncommutation:=true);
    fi;
  fi;
od;
P159P3V2CWrongOrderFullQ2Equal:=P159P3V2CWrongOrderQ2DistinctCount=0;
P159P3V2CWrongOrderFullQ2Commuting:=P159P3V2CWrongOrderQ2NoncommutingCount=0;
if P159P3V2WrongOrderDiscriminator=fail then
  Error("PENT159N_P3_V2: no actual coface-derived wrong-order discriminator with a noncommuting factor pair");
fi;
Print("PENT159N_P3_V2_WRONG_ORDER_CONTROL_PASS q2_universe=",
  Length(P159P3V2Bfs)," q2_distinct=",P159P3V2CWrongOrderQ2DistinctCount,
  " q2_noncommuting=",P159P3V2CWrongOrderQ2NoncommutingCount,
  " q2_equal_all=",P159P3V2CWrongOrderFullQ2Equal,
  " actual_coface_Dpap_row=true residuals_distinct=true factor_noncommuting_pairs=",
  Length(P159P3V2WrongOrderDiscriminator.noncommuting_factor_pairs),
  " external_S3_calibration_only=true\n");
P159P3V2RequireFileSha(
  "search/d972_pent_interleave_canary_p3_control_overlay_v2.g",
  "3accef86d2e20105eb767b8309d8dd1e6972f90294ecc63bb669cb3954e3c7f3",
  "p3 v2 complete actual-coface control overlay");
Read("search/d972_pent_interleave_canary_p3_control_overlay_v2.g");
if P159P3V2WrongOrderActualCofaceRowCount=0 then
  Error("PENT159N_P3_V2: aggregate control overlay did not close");
fi;
if P159P3V2InversionDiscriminator=fail then
  Error("PENT159N_P3_V2: LHS/RHS inversion mutant was not discriminated");
fi;
if P159P3V2SwappedCofaceDiscriminator=fail then
  Error("PENT159N_P3_V2: swapped-coface mutant was not discriminated");
fi;
Print("PENT159N_P3_V2_INSTRUMENT_PASS universe=",
  Length(P159P3V2InstrumentInternal)," nonzero=",
  Length(P159P3V2NonzeroInstrument)," defect_image_order=",Size(P159P3V2DpapImage),
  " degree3_deletion_kernel_order=",Size(P159P3V2Degree3BrKernel),
  " coverage_sha256=",P159P3V2InstrumentDigest,"\n");

P159P3V2Phase("COMPLETE_CHARMING_ONTO_GATE");
P159P3V2CA5PureWords:=[[1,2,3],[2,3,1],[3,1,2]];
P159P3V2CA5BraidWords:=List(P159P3V2CA5PureWords,w->
  P159P3V2ExpandPure(3,w));
P159P3V2CA5ArtinImages:=List(P159P3V2CA5BraidWords,w->
  P159P3V2ArtinImages(3,w));
if Length(Set(P159P3V2CA5ArtinImages))<>1 then
  Error("PENT159N_P3_V2: cyclic A.5 native forms differ in Artin action");
fi;
P159P3V2CSigmaFullTwist:=[1,2,1,2,1,2];
if P159P3V2ArtinImages(3,P159P3V2CSigmaFullTwist)<>P159P3V2CA5ArtinImages[1] then
  Error("PENT159N_P3_V2: A.5 forms differ from (sigma1 sigma2)^3");
fi;
for P159P3V2i in [1..3] do
  P159P3V2CA5CommPure:=P159P3V2Reduce(Concatenation(
    P159P3V2InvWord(P159P3V2CA5PureWords[1]),[-P159P3V2i],
    P159P3V2CA5PureWords[1],[P159P3V2i]));
  if not P159P3V2ArtinIdentity(3,P159P3V2ExpandPure(3,P159P3V2CA5CommPure)) then
    Error("PENT159N_P3_V2: A.5 native word is not source-central");
  fi;
od;
P159P3V2CA5Q3Values:=List(P159P3V2CA5PureWords,w->
  P159P3V2NativeWordEval(w,P159P3V2Q3.marks));
if Length(Set(P159P3V2CA5Q3Values))<>1 then
  Error("PENT159N_P3_V2: A.5 native quotient forms differ");
fi;
P159P3V2Q3c:=P159P3V2CA5Q3Values[1];
for P159P3V2i in [1..Length(P159P3V2Q3.marks)] do
  if Comm(P159P3V2Q3c,P159P3V2Q3.marks[P159P3V2i])<>One(P159P3V2Q3.group) then
    Error("PENT159N_P3_V2: pinned A.5 quotient element is not central");
  fi;
od;
P159P3V2CRejectedReversedWords:=[[3,2,1],[2,1,3]];
P159P3V2CRejectedReversedCentralBits:=[];
for P159P3V2CRejectedReversedWord in P159P3V2CRejectedReversedWords do
  P159P3V2CRejectedReversedValue:=P159P3V2NativeWordEval(
    P159P3V2CRejectedReversedWord,P159P3V2Q3.marks);
  P159P3V2CRejectedReversedCentral:=true;
  for P159P3V2i in [1..Length(P159P3V2Q3.marks)] do
    if Comm(P159P3V2CRejectedReversedValue,P159P3V2Q3.marks[P159P3V2i])<>
       One(P159P3V2Q3.group) then P159P3V2CRejectedReversedCentral:=false; fi;
  od;
  Add(P159P3V2CRejectedReversedCentralBits,P159P3V2CRejectedReversedCentral);
od;
if true in P159P3V2CRejectedReversedCentralBits then
  Error("PENT159N_P3_V2: a reversed paper/native mutant was not rejected");
fi;
Print("PENT159N_P3_V2_A5_CENTRAL_PASS displayed_native_forms=2 cyclic_native_forms=3 artin_equal=true sigma_full_twist_equal=true quotient_equal=true central=true reversed_forms=2 reversed_central_all=false\n");
P159P3V2Nord:=Lcm(Order(P159P3V2Q3.marks[1]),Order(P159P3V2Q3.marks[3]),
  Order(P159P3V2Q3c));
if P159P3V2Nord<1 then Error("PENT159N_P3_V2: invalid N_ord"); fi;
P159P3V2z:=P159P3V2Paper([P159P3V2x,P159P3V2y])^-1;
if P159P3V2z<>P159P3V2x^-1*P159P3V2y^-1 then
  Error("PENT159N_P3_V2: correct tau native word drift");
fi;
P159P3V2Theta:=GroupHomomorphismByImages(P159P3V2Q2.group,P159P3V2Q2.group,
  [P159P3V2x,P159P3V2y],[P159P3V2y,P159P3V2x]);
P159P3V2Tau:=GroupHomomorphismByImages(P159P3V2Q2.group,P159P3V2Q2.group,
  [P159P3V2x,P159P3V2y],[P159P3V2y,P159P3V2z]);
if P159P3V2Theta=fail or P159P3V2Tau=fail or
   not IsBijective(P159P3V2Theta) or not IsBijective(P159P3V2Tau) then
  Error("PENT159N_P3_V2: theta/tau automorphism descent failed");
fi;
P159P3V2WrongZ:=(P159P3V2x*P159P3V2y)^-1;
if P159P3V2WrongZ=P159P3V2z then
  Error("PENT159N_P3_V2: rejected tau mutant collapsed to correct tau");
fi;
P159P3V2WrongTau:=GroupHomomorphismByImages(P159P3V2Q2.group,P159P3V2Q2.group,
  [P159P3V2x,P159P3V2y],[P159P3V2y,P159P3V2WrongZ]);
P159P3V2GateTrace:=[];
P159P3V2GateCounts:=rec(raw_pair_count:=0,unit_pass:=0,
  derived_after_unit_pass:=0,hexagon_310_pass:=0,hexagon_311_pass:=0,
  onto_pass:=0);
P159P3V2TauMutantDisagreements:=0;
for P159P3V2m in [0..P159P3V2Nord-1] do
  P159P3V2u:=2*P159P3V2m+1;
  for P159P3V2Row in P159P3V2Bfs do
    P159P3V2f:=P159P3V2Row.elt;
    if IsBound(P159P3V2Row.commutator_word) then
      P159P3V2GateWord:=P159P3V2Row.commutator_word;
    else
      P159P3V2GateWord:=P159P3V2Row.word;
    fi;
    P159P3V2Unit:=Gcd(P159P3V2u,P159P3V2Nord)=1;
    P159P3V2Derived:=P159P3V2f in P159P3V2D2;
    P159P3V2H10:=false; P159P3V2H11:=false; P159P3V2Onto:=false;
    P159P3V2GeneratedOrder:=fail; P159P3V2Reason:="unit_fail";
    P159P3V2GateCounts.raw_pair_count:=P159P3V2GateCounts.raw_pair_count+1;
    if P159P3V2Unit then
      P159P3V2GateCounts.unit_pass:=P159P3V2GateCounts.unit_pass+1;
      P159P3V2Reason:="derived_fail";
      if P159P3V2Derived then
        P159P3V2GateCounts.derived_after_unit_pass:=
          P159P3V2GateCounts.derived_after_unit_pass+1;
        P159P3V2ThetaF:=Image(P159P3V2Theta,P159P3V2f);
        P159P3V2H10:=P159P3V2Paper([P159P3V2f,P159P3V2ThetaF])=
          One(P159P3V2Q2.group);
        P159P3V2Reason:="hexagon_310_fail";
        if P159P3V2H10 then
          P159P3V2GateCounts.hexagon_310_pass:=
            P159P3V2GateCounts.hexagon_310_pass+1;
          P159P3V2Ymf:=P159P3V2Paper([P159P3V2y^P159P3V2m,P159P3V2f]);
          P159P3V2TauYmf:=Image(P159P3V2Tau,P159P3V2Ymf);
          P159P3V2Tau2Ymf:=Image(P159P3V2Tau,P159P3V2TauYmf);
          P159P3V2H11:=P159P3V2Paper([P159P3V2Tau2Ymf,P159P3V2TauYmf,
            P159P3V2Ymf])=One(P159P3V2Q2.group);
          if P159P3V2WrongTau=fail then
            P159P3V2TauMutantDisagreements:=P159P3V2TauMutantDisagreements+1;
          else
            P159P3V2WrongTauYmf:=Image(P159P3V2WrongTau,P159P3V2Ymf);
            P159P3V2WrongTau2Ymf:=Image(P159P3V2WrongTau,P159P3V2WrongTauYmf);
            P159P3V2WrongH11:=P159P3V2Paper([P159P3V2WrongTau2Ymf,
              P159P3V2WrongTauYmf,P159P3V2Ymf])=One(P159P3V2Q2.group);
            if P159P3V2WrongH11<>P159P3V2H11 then
              P159P3V2TauMutantDisagreements:=
                P159P3V2TauMutantDisagreements+1;
            fi;
          fi;
          P159P3V2Reason:="hexagon_311_fail";
          if P159P3V2H11 then
            P159P3V2GateCounts.hexagon_311_pass:=
              P159P3V2GateCounts.hexagon_311_pass+1;
            P159P3V2GenA:=P159P3V2x^P159P3V2u;
            P159P3V2GenB:=P159P3V2Paper([P159P3V2f^-1,
              P159P3V2y^P159P3V2u,P159P3V2f]);
            P159P3V2GeneratedOrder:=Size(Group(P159P3V2GenA,P159P3V2GenB));
            P159P3V2Onto:=P159P3V2GeneratedOrder=Size(P159P3V2Q2.group);
            P159P3V2Reason:="onto_fail";
            if P159P3V2Onto then
              P159P3V2GateCounts.onto_pass:=P159P3V2GateCounts.onto_pass+1;
              P159P3V2Reason:="pass";
            fi;
          fi;
        fi;
      fi;
    fi;
    if P159P3V2GeneratedOrder=fail then
      P159P3V2GeneratedOrderString:=fail;
    else
      P159P3V2GeneratedOrderString:=String(P159P3V2GeneratedOrder);
    fi;
    Add(P159P3V2GateTrace,rec(m:=P159P3V2m,u:=P159P3V2u,
      f_coords:=P159P3V2Row.coords,f_word:=P159P3V2GateWord,
      unit:=P159P3V2Unit,derived:=P159P3V2Derived,
      literal_gentle_hexagon_310:=P159P3V2H10,
      literal_gentle_hexagon_311:=P159P3V2H11,
      generated_order_decimal:=P159P3V2GeneratedOrderString,
      onto:=P159P3V2Onto,rejection_reason:=P159P3V2Reason,
      passed:=P159P3V2Reason="pass"));
  od;
od;
P159P3V2ExpectedPairCount:=P159P3V2Nord*Size(P159P3V2Q2.group);
if Length(P159P3V2GateTrace)<>P159P3V2ExpectedPairCount or
   Length(Set(List(P159P3V2GateTrace,r->[r.m,r.f_coords])))<>
     P159P3V2ExpectedPairCount then
  Error("PENT159N_P3_V2: gated pair universe omission/duplicate");
fi;
if P159P3V2TauMutantDisagreements=0 then
  Error("PENT159N_P3_V2: wrong tau word mutant was not discriminated");
fi;
P159P3V2GateDigest:=P159P3V2Digest(List(P159P3V2GateTrace,r->
  rec(m:=r.m,f_coords:=r.f_coords,rejection_reason:=r.rejection_reason)));
P159P3V2SurvivorsInternal:=[];
for P159P3V2GateRow in Filtered(P159P3V2GateTrace,r->r.passed) do
  P159P3V2Drec:=P159P3V2Dpap(P159P3V2GateRow.f_word,P159P3V2Contexts);
  Add(P159P3V2SurvivorsInternal,rec(m:=P159P3V2GateRow.m,
    f_coords:=P159P3V2GateRow.f_coords,f_word:=P159P3V2GateRow.f_word,
    defect:=P159P3V2Drec.correct,
    defect_coords:=P159P3V2Coords(P159P3V2Q4Pc,P159P3V2Drec.correct),
    nonzero:=P159P3V2Drec.correct<>One(P159P3V2Q4.group)));
od;
P159P3V2SurvivorsPublic:=List(P159P3V2SurvivorsInternal,r->rec(m:=r.m,
  f_coords:=r.f_coords,f_word:=r.f_word,defect_coords:=r.defect_coords,
  nonzero:=r.nonzero));
P159P3V2SurvivorDigest:=P159P3V2Digest(P159P3V2SurvivorsPublic);
P159P3V2ActualNonzero:=Filtered(P159P3V2SurvivorsInternal,r->r.nonzero);
Print("PENT159N_P3_V2_GATED_PASS N_ord=",P159P3V2Nord,
  " raw_pairs=",P159P3V2ExpectedPairCount," survivors=",
  Length(P159P3V2SurvivorsInternal)," nonzero_survivors=",
  Length(P159P3V2ActualNonzero)," coverage_sha256=",P159P3V2GateDigest,"\n");

#############################################################################
## Receipt.  This is the separately routed p=3 instrument/gated stage;
## no all-prime, row36, isolation, or K2 inference is made.
#############################################################################

P159P3V2Phase("WRITE_RECEIPT");
if Length(P159P3V2ActualNonzero)>0 then
  P159P3V2Terminal:="PENT159N_P3_ACTUAL_CHARMING_SENSITIVE__P3_COMPLETE";
elif Length(P159P3V2NonzeroInstrument)>0 then
  P159P3V2Terminal:=
    "PENT159N_P3_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_COMPLETE";
else
  P159P3V2Terminal:=
    "PENT159N_P3_INSTRUMENT_AND_ACTUAL_CHARMING_BLIND__P3_COMPLETE";
fi;
P159P3V2Receipt:=rec(
  schema:="d972-pent-interleave-canary-p3/v2",
  date:="2026-08-24",
  role:="Luna producer",
  scope:="corrected finite p=3 Brunnian, complete commutator instrument, and separately gated charming+onto subset; row36/diamond deferred",
  status:="MEASURED_P3_STAGE_CONTROL_AGGREGATE_V2",
  execution_routing_addendum_159o:=rec(
    rule:="p=2 and p=3 instruments/gated subsets are reported separately; neither pair of finite measurements implies all class-3 primes blind",
    p2_trigger_run_id:=P159P3V2P2TriggerRun,
    p2_trigger_receipt_bytes:=P159P3V2P2ReceiptBytes,
    p2_trigger_receipt_sha256:=P159P3V2P2ReceiptSha,
    p2_trigger_commit:="4e2de61961e167d058bcf963e6add5a0eb6edfe0",
    p2_trigger_producer_grade_only:=true,
    p2_trigger_crosscheck_closed:=false,
    p2_trigger_terminal:="PENT159N_P2_INSTRUMENT_SENSITIVE_ACTUAL_CHARMING_BLIND__P3_REQUIRED",
    p3_executed_due_to_p2_actual_charming_blind:=true,
    p2_and_p3_reported_separately:=true,
    all_class3_prime_inference_forbidden:=true,
    automatic_K2_naming_forbidden:=true),
  provenance:=rec(gap_version:=GAPInfo.Version,nq_version:=P159V4NqVersion,
    nq_executable_sha256:=P159V4BinarySha,
    nq_pcp_api_sha256:=P159P3V2NqPcpSha,
    stage0_source:=P159P3V2Stage0,stage0_source_sha256:=P159P3V2Stage0Sha,
    successful_stage0_run_id:=32647100171,
    successful_stage0_commit:="c8e3bc8dd734d788f8ab9f80773c8503f352c0bf",
    source_path:=P159P3V2Source,
    source_sha256_measured_at_runtime:=HexSHA256(StringFile(P159P3V2Source)),
    derivation_base:="authenticated GHA p2 v9 effective source",
    derivation_base_sha256:="1d020d26a7aedb34a6b2d5732b0d95e36cc13b7c2a5e0424209d012d1695643d",
    v2_authenticated_base_path:="search/d972_pent_interleave_canary_p3_math_v1.g",
    v2_authenticated_base_sha256:="ecc6a10befc8b37c627a90f29588b7ff4c992f31384642aa22a0fe4d76608c49",
    v2_control_overlay_path:="search/d972_pent_interleave_canary_p3_control_overlay_v2.g",
    v2_control_overlay_sha256:="3accef86d2e20105eb767b8309d8dd1e6972f90294ecc63bb669cb3954e3c7f3",
    p2_trigger_run_id:=P159P3V2P2TriggerRun,
    p2_trigger_receipt_sha256:=P159P3V2P2ReceiptSha,
    p2_trigger_commit:="4e2de61961e167d058bcf963e6add5a0eb6edfe0",
    p2_trigger_producer_grade_only:=true,
    p2_trigger_crosscheck_closed:=false,
    p2_trigger_run_log_sha256:=P159P3V2P2RunLogSha,
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
    quotient_coords:=P159P3V2Coords(P159P3V2Q3Pc,P159P3V2Q3c),
    quotient_order:=Int(Order(P159P3V2Q3c)),
    rejected_global_paper_reversals:=[[3,2,1],[2,1,3]],
    rejected_reversal_central_bits:=P159P3V2CRejectedReversedCentralBits),
  quotients:=rec(Q2:=P159P3V2PublicPcReceipt(P159P3V2Q2Receipt),
    Q3:=P159P3V2PublicPcReceipt(P159P3V2Q3Receipt),
    Q4:=P159P3V2PublicPcReceipt(P159P3V2Q4Receipt)),
  marked_maps:=rec(
    deletion_count:=4,coface_count:=5,
    deletion_table:=P159P3V2DelWords,
    deletion_table_sha256:=P159P3V2Digest(P159P3V2DelWords),
    coface_table:=P159P3V2CofWords,
    coface_table_sha256:=P159P3V2Digest(P159P3V2CofWords),
    a18_F2_context_words_by_slot_0_to_4:=P159P3V2ContextWords,
    deletions:=List(P159P3V2DeletionMaps,P159P3V2PublicMap),
    cofaces:=List(P159P3V2CofaceMaps,P159P3V2PublicMap),
    F2_to_PB3:=P159P3V2PublicMap(P159P3V2IotaMap)),
  brunnian_degree3:=rec(
    finite_degree3_deletion_kernel_order_decimal:=
      String(Size(P159P3V2Degree3BrKernel)),
    integral_Dpap_image_order_decimal:=String(Size(P159P3V2DpapImage)),
    integral_Dpap_image_generator_coords:=List(
      GeneratorsOfGroup(P159P3V2DpapImage),g->P159P3V2Coords(P159P3V2Q4Pc,g)),
    concrete_first_nonzero:=P159P3V2FirstNonzeroPublic,
    canary1_pass:=Length(P159P3V2NonzeroInstrument)>0,
    claim_scope:="Dpap words are integral Brunnian words by four exact deletions; their measured subgroup is contained in gamma3 and in every deletion kernel"),
  commutator_instrument:=rec(
    universe:="every element of DerivedSubgroup(Q2) exactly once",
    over_universe_not_all_charming:=true,Q2_order:=Size(P159P3V2Q2.group),
    derived_order:=Size(P159P3V2D2),enumerated_count:=Length(P159P3V2InstrumentInternal),
    no_omission_duplicate:=true,identity_only_rejected:=true,
    Q2_bfs_count:=Length(P159P3V2Bfs),Q2_bfs_sha256:=P159P3V2BfsDigest,
    coverage_sha256:=P159P3V2InstrumentDigest,
    nonzero_count:=Length(P159P3V2NonzeroInstrument),
    distinct_nonzero_image_count:=Length(Set(List(P159P3V2NonzeroInstrument,
      r->r.defect_coords))),
    defect_histogram:=P159P3V2Histogram(P159P3V2InstrumentInternal,
      "defect_coords"),
    canonical_first_nonzero:=P159P3V2FirstNonzeroPublic,
    rows:=P159P3V2InstrumentPublic),
  actual_charming_onto_gate:=rec(
    m_residue_range:=[0..P159P3V2Nord-1],N_ord:=P159P3V2Nord,
    f_universe_count:=Size(P159P3V2Q2.group),
    raw_pair_count:=P159P3V2ExpectedPairCount,evaluated_count:=Length(P159P3V2GateTrace),
    no_omission_duplicate:=true,
    sequential_gate_counts:=P159P3V2GateCounts,
    coverage_sha256:=P159P3V2GateDigest,
    surviving_count:=Length(P159P3V2SurvivorsInternal),
    survivor_sha256:=P159P3V2SurvivorDigest,
    nonzero_survivor_count:=Length(P159P3V2ActualNonzero),
    actual_charming_witness_exists:=Length(P159P3V2ActualNonzero)>0,
    defect_histogram:=P159P3V2Histogram(P159P3V2SurvivorsInternal,
      "defect_coords"),
    survivors:=P159P3V2SurvivorsPublic,
    full_gate_trace:=P159P3V2GateTrace),
  destructive_controls:=rec(
    wrong_order_mutant:="phi123*phi1_23_4*phi234*(phi12_3_4*phi1_2_34)^-1",
    wrong_order_correct_paper_factors:=["A^-1","B^-1","C","E","F"],
    wrong_order_correct_native_factors:=["F","E","C","B^-1","A^-1"],
    wrong_order_mutant_paper_factors:=["F","E","C","B^-1","A^-1"],
    wrong_order_mutant_native_factors:=["A^-1","B^-1","C","E","F"],
    wrong_order_control_contract:="actual complete-Q2 coface-derived row with distinct residuals and at least one noncommuting factor pair",
    wrong_order_noncommuting_discriminator:=P159P3V2WrongOrderDiscriminator,
    wrong_order_control_requires_actual_coface_row:=true,
    wrong_order_external_S3_calibration_accepted_as_pass:=false,
    wrong_order_factor_noncommuting_row_count:=P159P3V2WrongOrderFactorNoncommutingRowCount,
    wrong_order_actual_distinct_and_factor_noncommuting_row_count:=P159P3V2WrongOrderActualCofaceRowCount,
    wrong_order_noncommuting_factor_pair_total:=P159P3V2WrongOrderNoncommutingPairTotal,
    wrong_order_full_Q2_universe_count:=Length(P159P3V2Bfs),
    wrong_order_full_Q2_distinct_count:=P159P3V2CWrongOrderQ2DistinctCount,
    wrong_order_full_Q2_noncommuting_count:=P159P3V2CWrongOrderQ2NoncommutingCount,
    wrong_order_full_Q2_equal_all:=P159P3V2CWrongOrderFullQ2Equal,
    wrong_order_full_Q2_commuting_all:=P159P3V2CWrongOrderFullQ2Commuting,
    wrong_order_external_finite_group_discriminator:=P159P3V2COrderCanary,
    lhs_rhs_inversion_checked_in_every_Dpap_call:=true,
    lhs_rhs_inversion_discriminator:=P159P3V2InversionDiscriminator,
    deletion_expected_count:=4,deletion_actual_count:=Length(P159P3V2DeletionMaps),
    one_deletion_omitted_rejected:=Length(P159P3V2DeletionMaps)=4,
    strand_renumbering_exact_table_gate:=true,
    coface_slot_order_exact_gate:=true,
    swapped_coface_discriminator:=P159P3V2SwappedCofaceDiscriminator,
    wrong_tau_mutant_disagreement_count:=P159P3V2TauMutantDisagreements,
    identity_only_canary_rejected:=Length(P159P3V2DerivedRows)>1,
    charming_without_onto_rejected:=true,
    row35_37_substitution_not_in_scope:=true,
    single_representative_not_reported_as_fibre:=true),
  deferred:=rec(row36_full_fibre:="NOT_IN_P3_V2_BOUNDED_STAGE",
    p_specific_M_containment:="NOT_IN_P3_V2_BOUNDED_STAGE",
    K1_intersection_isolation_diamond:="NOT_IN_P3_V2_BOUNDED_STAGE",
    claim_cover_pent_canary_2:="NOT_IN_P3_V2_BOUNDED_STAGE",
    p3_instrument:="COMPLETED_IN_THIS_RECEIPT"),
  firewall:=rec(checker_source_opened_or_imported:=false,
    checker_verdict_opened_or_imported:=false,
    checker_report_opened_or_imported:=false,git_used:=false,
    gha_dispatched_by_child:=false,workflow_edited:=false,es7ops_used:=false,
    main_sol_reply_edited:=false,p2_v1_through_v10_edited:=false,p3_prior_versions_overwritten:=false),
  runtime_ms:=Runtime(),
  terminal_token:=P159P3V2Terminal);

P159P3V2Write:=P159P3V2CheckedWrite(P159P3V2Output,P159P3V2Receipt);
Print("PENT159N_P3_V2_RECEIPT_WRITTEN path=",P159P3V2Output,
  " bytes=",P159P3V2Write.bytes," sha256=",P159P3V2Write.sha256,"\n");
Print("PENT159N_P3_V2_FINAL_MARKER terminal=",P159P3V2Receipt.terminal_token,
  " q2_order=",Size(P159P3V2Q2.group)," q3_order=",Size(P159P3V2Q3.group),
  " q4_order=",Size(P159P3V2Q4.group)," instrument_nonzero=",
  Length(P159P3V2NonzeroInstrument)," gated_nonzero=",
  Length(P159P3V2ActualNonzero)," runtime_ms=",Runtime(),"\n");
