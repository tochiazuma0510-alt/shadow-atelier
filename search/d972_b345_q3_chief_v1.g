#############################################################################
## d972_b345_q3_chief_v1.g
##
## One-process, one-ANUPQ construction of the matched exponent-three
## PB3/PB4/PB5 system.  PB4 and PB3 are recovered inside Pi_5[3] by the
## endpoint insertion and certified deletion retractions.  No Cayley table
## and no coarse arity-five roof quotient are constructed.
#############################################################################

Read("search/gaplib_common.g");;

D972Q3Producer := "search/d972_b345_q3_chief_v1.g";;
D972Q3Schema := "d972-b345-q-chief/v1";;
D972Q3PcCap := 175;; # number of basic commutators in B(10,3)
D972Q3ExpectedFormulaSHA := "b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef";;
D972Q3Row18Source := "search/d972_b4_literal_row18_stage_v2.g";;
D972Q3Row18SourceSHA := "8f8b429b5725b244a214cc6a4cf59daa186e4ee2d4d6eee6df18e580d88ef2a1";;
D972Q3Row18Checker := "search/check_d972_b4_literal_row18_stage_v2.py";;
D972Q3Row18CheckerSHA := "bf85cfd142f6c640e96af77aa5f580caa206439329d17ed18ac342ac6acdcd19";;
D972Q3Phase2b := "search/certs/d972_phase2b_nonsplit_v1_20260813.json";;
D972Q3Phase2bSHA := "648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9";;
D972Q3Words := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972Q3WordsSHA := "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972Q3Core := "search/d972_d972core_c2six_intersection_v2.g";;
D972Q3CoreSHA := "577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c";;

D972Q3Phase := function(label, start)
  local now;
  now := Runtime();;
  Print("D972_B345_Q3_PHASE ", label, " runtime_ms=", now,
    " delta_ms=", now-start, "\n");;
  if IsBoundGlobal("FlushAllStreams") then FlushAllStreams(); fi;
  return now;
end;;

D972Q3RequireSHA := function(path, sha, label)
  local raw, got;
  raw := StringFile(path);;
  if raw=fail then Error("157da: missing pinned ", label, ": ", path); fi;
  got := HexSHA256(raw);;
  if got<>sha then Error("157da: pinned ", label, " SHA drift: ", got); fi;
  return rec(path:=path,sha256:=sha);
end;;

D972Q3Escape := function(s)
  local z;
  z := ReplacedString(s,"\\","\\\\");;
  z := ReplacedString(z,"\"","\\\"");;
  z := ReplacedString(z,"\n","\\n");;
  z := ReplacedString(z,"\r","\\r");;
  z := ReplacedString(z,"\t","\\t");;
  return z;
end;;

D972Q3Json := function(x)
  local names, parts, n;
  if x=fail then return "null"; fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsString(x) then return Concatenation("\"",D972Q3Escape(x),"\""); fi;
  if IsRecord(x) then
    names := RecNames(x);; Sort(names);;
    parts := [];;
    for n in names do
      Add(parts,Concatenation(D972Q3Json(n),":",D972Q3Json(x.(n))));
    od;
    return Concatenation("{",JoinStringsWithSeparator(parts,","),"}");
  fi;
  if IsList(x) then
    return Concatenation("[",JoinStringsWithSeparator(List(x,D972Q3Json),","),"]");
  fi;
  Error("157da: unsupported JSON value");
end;;

D972Q3Digest := x -> HexSHA256(D972Q3Json(x));;

D972Q3AtomicWrite := function(path, obj)
  local tmp, f;
  tmp := Concatenation(path,".tmp");;
  f := OutputTextFile(tmp,false);;
  if f=fail then Error("157da: cannot open output ",tmp); fi;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,D972Q3Json(obj),"\n");; CloseStream(f);;
  if IsExistingFile(path) then RemoveFile(path); fi;
  if RenameFile(tmp,path)<>true then Error("157da: atomic rename failed: ",path); fi;
end;;

#############################################################################
## Signed free words and the faithful Artin action.
#############################################################################

D972Q3Reduce := function(w)
  local out, x;
  out := [];;
  for x in w do
    if x=0 then Error("157da: zero signed letter"); fi;
    if Length(out)>0 and out[Length(out)]=-x then
      Remove(out,Length(out));
    else
      Add(out,x);
    fi;
  od;
  return out;
end;;

D972Q3Inv := w -> D972Q3Reduce(List(Reversed(w),x->-x));;

D972Q3WordEval := function(w, imgs)
  local out, x;
  out := [];;
  for x in w do
    if AbsInt(x)>Length(imgs) then Error("157da: word image index drift"); fi;
    if x>0 then Append(out,imgs[x]); else Append(out,D972Q3Inv(imgs[-x])); fi;
    out := D972Q3Reduce(out);;
  od;
  return out;
end;;

D972Q3ArtinStep := function(rank, letter)
  local imgs, i;
  imgs := List([1..rank],i->[i]);;
  i := AbsInt(letter);;
  if i<1 or i>=rank then Error("157da: Artin generator outside rank"); fi;
  if letter>0 then
    imgs[i] := [i,i+1,-i];;
    imgs[i+1] := [i];;
  else
    imgs[i] := [i+1];;
    imgs[i+1] := [-(i+1),i,i+1];;
  fi;
  return imgs;
end;;

D972Q3ArtinImages := function(rank, braidword)
  local imgs, x, step;
  imgs := List([1..rank],i->[i]);;
  for x in braidword do
    step := D972Q3ArtinStep(rank,x);;
    imgs := List(imgs,w->D972Q3WordEval(w,step));;
  od;
  return imgs;
end;;

D972Q3ArtinIdentity := function(rank, braidword)
  return D972Q3ArtinImages(rank,braidword)=List([1..rank],i->[i]);
end;;

D972Q3PairList := function(rank)
  local ans, i, j;
  ans := [];;
  for i in [1..rank-1] do
    for j in [i+1..rank] do Add(ans,[i,j]); od;
  od;
  return ans;
end;;

D972Q3PairIndex := function(rank, pair)
  local pos;
  pos := Position(D972Q3PairList(rank),pair);;
  if pos=fail then Error("157da: invalid pure pair"); fi;
  return pos;
end;;

D972Q3AijBraid := function(i,j)
  local w, k;
  w := [];;
  if j-i>1 then for k in Reversed([i+1..j-1]) do Add(w,k); od; fi;
  Add(w,i);; Add(w,i);;
  if j-i>1 then for k in [i+1..j-1] do Add(w,-k); od; fi;
  return w;
end;;

D972Q3ExpandPure := function(rank, w)
  return D972Q3WordEval(w,List(D972Q3PairList(rank),p->D972Q3AijBraid(p[1],p[2])));
end;;

D972Q3PureRelations := function(rank)
  local pairs, rels, oldrels, oldpairs, mapold, p, k, g, h, act, kmaps;
  if rank=2 then return [];; fi;
  pairs := D972Q3PairList(rank);;
  oldpairs := D972Q3PairList(rank-1);;
  oldrels := D972Q3PureRelations(rank-1);;
  mapold := List(oldpairs,p->D972Q3PairIndex(rank,p));;
  rels := List(oldrels,w->D972Q3WordEval(w,List(mapold,x->[x])));;
  kmaps := List([1..rank-1],k->[D972Q3PairIndex(rank,[k,rank])]);;
  for p in oldpairs do
    g := D972Q3PairIndex(rank,p);;
    act := D972Q3ArtinImages(rank-1,D972Q3AijBraid(p[1],p[2]));;
    for k in [1..rank-1] do
      h := D972Q3PairIndex(rank,[k,rank]);;
      Add(rels,D972Q3Reduce(Concatenation([-g,h,g],
        D972Q3Inv(D972Q3WordEval(act[k],kmaps)))));
    od;
  od;
  return rels;
end;;

D972Q3EvalGroupWord := function(w, gens)
  local z, x;
  z := One(gens[1]);;
  for x in w do
    if x>0 then z:=z*gens[x];; else z:=z*gens[-x]^-1;; fi;
  od;
  return z;
end;;

D972Q3BuildPureFp := function(rank)
  local pairs, labels, F, fg, rels, fp;
  pairs := D972Q3PairList(rank);;
  labels := List(pairs,p->Concatenation("a",String(p[1]),String(p[2])));;
  F := FreeGroup(labels);; fg := GeneratorsOfGroup(F);;
  rels := D972Q3PureRelations(rank);;
  if ForAny(rels,w->not D972Q3ArtinIdentity(rank,D972Q3ExpandPure(rank,w))) then
    Error("157da: direct FN presentation failed faithful Artin replay at PB",rank);
  fi;
  fp := F/List(rels,w->D972Q3EvalGroupWord(w,fg));;
  return rec(rank:=rank,pairs:=pairs,labels:=labels,relations:=rels,
    group:=fp,gens:=GeneratorsOfGroup(fp),
    artin_words:=List(pairs,p->D972Q3AijBraid(p[1],p[2])),
    fp_unit_words:=List([1..Length(pairs)],i->[i]),
    relation_count:=Length(rels),artin_replay:=true);
end;;

D972Q3AdjacentPerm := function(rank,i)
  local row,t;
  row:=[1..rank];; t:=row[i];; row[i]:=row[i+1];; row[i+1]:=t;;
  return PermList(row);
end;;

D972Q3BraidKernelCertificate := function(rank)
  local rels,i,j,pureWords,purePerms,permWord,adj,x,p;
  rels:=[];;
  if rank>2 then for i in [1..rank-2] do
    Add(rels,[i,i+1,i,-(i+1),-i,-(i+1)]);
  od; fi;
  if rank>3 then for i in [1..rank-1] do
    if i+2<=rank-1 then for j in [i+2..rank-1] do
      Add(rels,[i,j,-i,-j]);
    od; fi;
  od; fi;
  adj:=List([1..rank-1],i->D972Q3AdjacentPerm(rank,i));;
  permWord:=function(w)
    local z,y;
    z:=();;
    for y in w do z:=z*adj[AbsInt(y)];; od;
    return z;
  end;;
  if ForAny(rels,w->permWord(w)<>()) then Error("157da: braid-to-S relator drift"); fi;
  pureWords:=List(D972Q3PairList(rank),p->D972Q3AijBraid(p[1],p[2]));;
  purePerms:=List(pureWords,permWord);;
  if ForAny(purePerms,p->p<>()) then Error("157da: Aij is not pure"); fi;
  if Size(Group(adj))<>Factorial(rank) then Error("157da: braid-to-S not onto"); fi;
  return rec(rank:=rank,braid_generator_count:=rank-1,braid_relations:=rels,
    symmetric_generator_images:=List(adj,p->List([1..rank],i->i^p)),
    symmetric_image_order:=Factorial(rank),map_onto:=true,
    pure_Aij_braid_words:=pureWords,pure_Aij_permutations_identity:=true,
    kernel_identification:="Artin pure braid kernel, presented independently by the replayed Fadell-Neuwirth semidirect presentation",
    no_Reidemeister_Schreier_conversion:=true);
end;;

#############################################################################
## Derived cofaces, deletions, and their exact word identities.
#############################################################################

D972Q3CofaceGenerator := function(rank, slot, pair)
  local i,j,ii,jj;
  i:=pair[1];; j:=pair[2];;
  if slot=0 then return [D972Q3PairIndex(rank+1,[i+1,j+1])]; fi;
  if slot=rank+1 then return [D972Q3PairIndex(rank+1,[i,j])]; fi;
  if slot<1 or slot>rank then Error("157da: coface slot drift"); fi;
  if i=slot then
    return [D972Q3PairIndex(rank+1,[slot,j+1]),
      D972Q3PairIndex(rank+1,[slot+1,j+1])];
  elif j=slot then
    return [D972Q3PairIndex(rank+1,[i,slot]),
      D972Q3PairIndex(rank+1,[i,slot+1])];
  fi;
  ii:=i;; jj:=j;;
  if ii>slot then ii:=ii+1;; fi;
  if jj>slot then jj:=jj+1;; fi;
  return [D972Q3PairIndex(rank+1,[ii,jj])];
end;;

D972Q3Cofaces := function(rank)
  return List([0..rank+1],s->List(D972Q3PairList(rank),
    p->D972Q3CofaceGenerator(rank,s,p)));
end;;

D972Q3DeleteGenerator := function(rank, strand, pair)
  local i,j;
  i:=pair[1];; j:=pair[2];;
  if strand=i or strand=j then return [];; fi;
  if i>strand then i:=i-1;; fi;
  if j>strand then j:=j-1;; fi;
  return [D972Q3PairIndex(rank-1,[i,j])];
end;;

D972Q3Deletions := function(rank)
  return List([1..rank],s->List(D972Q3PairList(rank),
    p->D972Q3DeleteGenerator(rank,s,p)));
end;;

D972Q3ComposeMaps := function(first, second)
  return List(first,w->D972Q3WordEval(w,second));
end;;

D972Q3IdentityMap := rank -> List([1..Length(D972Q3PairList(rank))],i->[i]);;

D972Q3MapArtinOK := function(sourceRank,targetRank,map)
  return ForAll(D972Q3PureRelations(sourceRank),r->
    D972Q3ArtinIdentity(targetRank,D972Q3ExpandPure(targetRank,D972Q3WordEval(r,map))));
end;;

D972Q3FormulaManifest := function(arg)
  local p3,p4,p5,c34,c45,d4,d5,cosimp,ret, i,j,left,right,a18,
    k5,facecosimp,r,case;
  if Length(arg)=0 then
    p3:=D972Q3BuildPureFp(3);; p4:=D972Q3BuildPureFp(4);;
    p5:=D972Q3BuildPureFp(5);;
  elif Length(arg)=3 then
    p3:=arg[1];; p4:=arg[2];; p5:=arg[3];;
  else
    Error("157da: FormulaManifest expects zero or three presentation records");
  fi;
  c34:=D972Q3Cofaces(3);; c45:=D972Q3Cofaces(4);;
  d4:=D972Q3Deletions(4);; d5:=D972Q3Deletions(5);;
  if ForAny(c34,m->not D972Q3MapArtinOK(3,4,m)) or
     ForAny(c45,m->not D972Q3MapArtinOK(4,5,m)) then
    Error("157da: a derived coface is not a pure-braid homomorphism");
  fi;
  if ForAny(d4,m->not D972Q3MapArtinOK(4,3,m)) or
     ForAny(d5,m->not D972Q3MapArtinOK(5,4,m)) then
    Error("157da: a derived deletion is not a pure-braid homomorphism");
  fi;
  cosimp:=[];;
  for i in [0..4] do
    for j in [i+1..5] do
      left:=D972Q3ComposeMaps(c34[i+1],c45[j+1]);;
      right:=D972Q3ComposeMaps(c34[j],c45[i+1]);;
      if not ForAll([1..Length(left)],k->
          D972Q3ArtinIdentity(5,D972Q3ExpandPure(5,
            D972Q3Reduce(Concatenation(left[k],D972Q3Inv(right[k])))))) then
        Error("157da: cosimplicial identity drift i=",i," j=",j);
      fi;
      Add(cosimp,rec(i:=i,j:=j,holds:=true));
    od;
  od;
  ret:=[];;
  for i in [0..4] do
    if i=0 then j:=1;; elif i=4 then j:=4;; else j:=i;; fi;
    left:=D972Q3ComposeMaps(c34[i+1],d4[j]);;
    if left<>D972Q3IdentityMap(3) then Error("157da: primary retraction drift"); fi;
    Add(ret,rec(source_rank:=3,slot:=i,deleted_strand:=j,holds:=true));
    if i>0 and i<4 then
      left:=D972Q3ComposeMaps(c34[i+1],d4[i+1]);;
      if left<>D972Q3IdentityMap(3) then Error("157da: second retraction drift"); fi;
      Add(ret,rec(source_rank:=3,slot:=i,deleted_strand:=i+1,holds:=true));
    fi;
  od;
  facecosimp:=[];;
  for r in [3,4] do
    for i in [0..r+1] do
      for j in [0..r] do
        left:=D972Q3ComposeMaps(D972Q3Cofaces(r)[i+1],
          D972Q3Deletions(r+1)[j+1]);;
        if j=i-1 or j=i then
          right:=D972Q3IdentityMap(r);; case:="identity";;
        elif j<i-1 then
          right:=D972Q3ComposeMaps(D972Q3Deletions(r)[j+1],
            D972Q3Cofaces(r-1)[i]);; case:="d^(i-1)_after_s^j";;
        else
          right:=D972Q3ComposeMaps(D972Q3Deletions(r)[j],
            D972Q3Cofaces(r-1)[i+1]);; case:="d^i_after_s^(j-1)";;
        fi;
        if not ForAll([1..Length(left)],k->
            D972Q3ArtinIdentity(r,D972Q3ExpandPure(r,
              D972Q3Reduce(Concatenation(left[k],D972Q3Inv(right[k])))))) then
          Error("157da: face/coface identity drift r=",r," i=",i," j=",j);
        fi;
        Add(facecosimp,rec(source_rank:=r,slot:=i,deleted_strand:=j+1,
          case:=case,holds:=true));
      od;
    od;
  od;
  for i in [0..5] do
    if i=0 then j:=1;; elif i=5 then j:=5;; else j:=i;; fi;
    left:=D972Q3ComposeMaps(c45[i+1],d5[j]);;
    if left<>D972Q3IdentityMap(4) then Error("157da: PB5 primary retraction drift"); fi;
    Add(ret,rec(source_rank:=4,slot:=i,deleted_strand:=j,holds:=true));
    if i>0 and i<5 then
      left:=D972Q3ComposeMaps(c45[i+1],d5[i+1]);;
      if left<>D972Q3IdentityMap(4) then Error("157da: PB5 second retraction drift"); fi;
      Add(ret,rec(source_rank:=4,slot:=i,deleted_strand:=i+1,holds:=true));
    fi;
  od;
  # Literal A.18 order: phi_123, phi_234, phi_12,3,4,
  # phi_1,23,4, phi_1,2,34 = slots 4,0,1,2,3.
  a18:=List([4,0,1,2,3],s->c34[s+1]);;
  if List(a18,m->m[1])<>[[1],[4],[2,4],[1,2],[1]] or
     List(a18,m->m[3])<>[[4],[6],[6],[5,6],[4,5]] then
    Error("157da: literal A.18 row18 orientation mismatch");
  fi;
  k5:=D972Q3BuildK5();;
  return rec(
    convention:=rec(pair_order:="lexicographic_i_then_j",
      artin_action:="left_to_right; sigma_i: t_i->t_i*t_(i+1)*t_i^-1, t_(i+1)->t_i",
      coface_slots:="0=left endpoint, 1..r=strand doubling, r+1=right endpoint",
      deletion_strands:="one-based"),
    braid_kernel_certificates:=rec(PB3:=D972Q3BraidKernelCertificate(3),
      PB4:=D972Q3BraidKernelCertificate(4),PB5:=D972Q3BraidKernelCertificate(5)),
    presentations:=rec(
      PB3:=rec(pairs:=p3.pairs,labels:=p3.labels,relations:=p3.relations,
        artin_words:=p3.artin_words,fp_unit_words:=p3.fp_unit_words),
      PB4:=rec(pairs:=p4.pairs,labels:=p4.labels,relations:=p4.relations,
        artin_words:=p4.artin_words,fp_unit_words:=p4.fp_unit_words),
      PB5:=rec(pairs:=p5.pairs,labels:=p5.labels,relations:=p5.relations,
        artin_words:=p5.artin_words,fp_unit_words:=p5.fp_unit_words)),
    cofaces_3_4:=c34,cofaces_4_5:=c45,deletions_4_3:=d4,
    deletions_5_4:=d5,coface_coface_identities:=cosimp,
    face_coface_identities:=facecosimp,
    insertion_deletion_retractions:=ret,
    a18_order:=rec(names:=["phi_123","phi_234","phi_12_3_4",
      "phi_1_23_4","phi_1_2_34"],slots:=[4,0,1,2,3],maps:=a18),
    k5:=k5);
end;;

#############################################################################
## The K5 boundary: generated from noncrossing diagonals, then oriented so
## each edge occurs twice with opposite signs.
#############################################################################

D972Q3IsBoundaryEdge := function(d)
  return d[2]=d[1]+1 or (d[1]=1 and d[2]=6);
end;;

D972Q3Cross := function(a,b)
  if Length(Intersection(a,b))>0 then return false; fi;
  return (a[1]<b[1] and b[1]<a[2] and a[2]<b[2]) or
    (b[1]<a[1] and a[1]<b[2] and b[2]<a[2]);
end;;

D972Q3EdgeDir := function(cycle,a,b)
  local i,n;
  n:=Length(cycle);;
  for i in [1..n] do
    if cycle[i]=a and cycle[(i mod n)+1]=b then return 1; fi;
    if cycle[i]=b and cycle[(i mod n)+1]=a then return -1; fi;
  od;
  return 0;
end;;

D972Q3BuildK5 := function()
  local diagonals,i,j,a,b,c,vertices,edges,facets,vs,cycle,start,prev,cur,
    nexts,nxt,rawcycles,signs,queue,f,g,common,dirf,dirg,oriented,balance,
    e,idx,facetRecords;
  diagonals:=[];;
  for i in [1..5] do for j in [i+1..6] do
    if not D972Q3IsBoundaryEdge([i,j]) then Add(diagonals,[i,j]); fi;
  od; od;
  vertices:=[];;
  for a in [1..7] do for b in [a+1..8] do for c in [b+1..9] do
    if not D972Q3Cross(diagonals[a],diagonals[b]) and
       not D972Q3Cross(diagonals[a],diagonals[c]) and
       not D972Q3Cross(diagonals[b],diagonals[c]) then
      Add(vertices,[a,b,c]);
    fi;
  od; od; od;
  if Length(vertices)<>14 then Error("157da: K5 vertex count drift"); fi;
  edges:=[];;
  for a in [1..13] do for b in [a+1..14] do
    if Length(Intersection(vertices[a],vertices[b]))=2 then Add(edges,[a,b]); fi;
  od; od;
  if Length(edges)<>21 then Error("157da: K5 edge count drift"); fi;
  facets:=List([1..9],i->Filtered([1..14],a->i in vertices[a]));;
  if Number(facets,x->Length(x)=5)<>6 or Number(facets,x->Length(x)=4)<>3 then
    Error("157da: K5 facet cardinalities drift");
  fi;
  rawcycles:=[];;
  for vs in facets do
    start:=Minimum(vs);; cycle:=[start];; prev:=fail;; cur:=start;;
    while true do
      nexts:=Filtered(vs,x->x<>cur and [Minimum([cur,x]),Maximum([cur,x])] in edges
        and x<>prev);;
      if Length(cycle)=1 then nxt:=Minimum(nexts);;
      else
        nexts:=Filtered(nexts,x->x=start or not x in cycle);;
        if Length(nexts)=0 then Error("157da: K5 cycle walk stuck"); fi;
        nxt:=Minimum(nexts);;
      fi;
      if nxt=start then break; fi;
      Add(cycle,nxt);; prev:=cur;; cur:=nxt;;
      if Length(cycle)>Length(vs) then Error("157da: K5 cycle overflow"); fi;
    od;
    if Length(cycle)<>Length(vs) then Error("157da: K5 facet not a cycle"); fi;
    Add(rawcycles,cycle);
  od;
  signs:=List([1..9],x->0);; signs[1]:=1;; queue:=[1];;
  while Length(queue)>0 do
    f:=Remove(queue,1);;
    for g in [1..9] do
      if g<>f then
        common:=Intersection(facets[f],facets[g]);;
        if Length(common)=2 and [Minimum(common),Maximum(common)] in edges then
          dirf:=D972Q3EdgeDir(rawcycles[f],common[1],common[2]);;
          dirg:=D972Q3EdgeDir(rawcycles[g],common[1],common[2]);;
          if dirf=0 or dirg=0 then Error("157da: K5 edge absent from cycle"); fi;
          if signs[g]=0 then
            signs[g]:=-signs[f]*dirf*dirg;; Add(queue,g);
          elif signs[f]*dirf+signs[g]*dirg<>0 then
            Error("157da: K5 orientation inconsistency");
          fi;
        fi;
      fi;
    od;
  od;
  if 0 in signs then Error("157da: disconnected K5 facet graph"); fi;
  oriented:=[];;
  for f in [1..9] do
    if signs[f]=1 then Add(oriented,ShallowCopy(rawcycles[f]));
    else Add(oriented,Reversed(rawcycles[f])); fi;
  od;
  balance:=[];;
  for e in edges do
    Add(balance,Sum([1..9],f->D972Q3EdgeDir(oriented[f],e[1],e[2])));
  od;
  if ForAny(balance,x->x<>0) then Error("157da: K5 oriented boundary is nonzero"); fi;
  facetRecords:=[];;
  for f in [1..9] do
    if Length(facets[f])=5 then
      Add(facetRecords,rec(diagonal_index:=f,vertex_indices:=facets[f],
        kind:="pentagon",oriented_cycle:=oriented[f]));
    else
      Add(facetRecords,rec(diagonal_index:=f,vertex_indices:=facets[f],
        kind:="square",oriented_cycle:=oriented[f]));
    fi;
  od;
  return rec(diagonals:=diagonals,vertices:=vertices,edges:=edges,
    facets:=facetRecords,edge_boundary_coefficients:=balance,
    vertex_count:=14,edge_count:=21,pentagon_count:=6,square_count:=3,
    boundary_zero:=true);
end;;

#############################################################################
## Lossless pc receipts and map certificates.
#############################################################################

D972Q3Coords := function(pc,x)
  local v;
  v:=ExponentsOfPcElement(pc,x);;
  if v=fail then Error("157da: element outside declared pc group"); fi;
  return List(v,Int);
end;;

D972Q3PcReceipt := function(name,rank,G,marks,presentation)
  local pc,orders,powers,conj,conjinv,invs,marked,i,j,ord,cls,exp;
  pc:=Pcgs(G);; orders:=List(RelativeOrders(pc),Int);;
  if Length(pc)>D972Q3PcCap then Error("157da: pc generator cap exceeded"); fi;
  if ForAny(orders,x->x<>3) then Error("157da: non-3 relative order"); fi;
  powers:=List([1..Length(pc)],i->D972Q3Coords(pc,pc[i]^orders[i]));;
  invs:=List([1..Length(pc)],i->D972Q3Coords(pc,pc[i]^-1));;
  conj:=[];; conjinv:=[];;
  if Length(pc)>1 then for i in [2..Length(pc)] do for j in [1..i-1] do
    Add(conj,rec(i:=i,j:=j,coords:=D972Q3Coords(pc,pc[i]^pc[j])));;
    Add(conjinv,rec(i:=i,j:=j,coords:=D972Q3Coords(pc,pc[i]^(pc[j]^-1))));;
  od; od; fi;
  marked:=List([1..Length(marks)],i->rec(label:=presentation.labels[i],
    pair:=presentation.pairs[i],coords:=D972Q3Coords(pc,marks[i]),
    inverse_coords:=D972Q3Coords(pc,marks[i]^-1)));
  ord:=Size(G);; exp:=Exponent(G);; cls:=NilpotencyClassOfGroup(G);;
  if exp<>3 or cls>3 then Error("157da: exponent/class terminal theorem mismatch"); fi;
  return rec(name:=name,rank:=rank,order_decimal:=String(ord),
    exponent:=Int(exp),nilpotency_class:=Int(cls),generator_count:=Length(pc),
    relative_orders:=orders,power_relations:=powers,inverses:=invs,
    conjugate_relations:=conj,inverse_conjugate_relations:=conjinv,
    marked_generators:=marked,original_relations:=presentation.relations,
    original_relator_images:=List(presentation.relations,w->
      D972Q3Coords(pc,D972Q3EvalGroupWord(w,marks))),
    pcgs_internal:=pc);
end;;

D972Q3PublicPcReceipt := function(r)
  local z;
  z:=ShallowCopy(r);; Unbind(z.pcgs_internal);; return z;
end;;

D972Q3MapCertificate := function(name,kind,sourceName,targetName,
    source,sourcePc,target,targetPc,sourceMarks,targetMarks,words,extra)
  local images,h,pcimgs,i,cert;
  images:=List(words,w->D972Q3EvalGroupWord(w,targetMarks));;
  h:=GroupHomomorphismByImages(source,target,sourceMarks,images);;
  if h=fail then Error("157da: quotient map failed: ",name); fi;
  if ForAny([1..Length(sourceMarks)],i->Image(h,sourceMarks[i])<>images[i]) then
    Error("157da: marked map image drift: ",name);
  fi;
  pcimgs:=List(sourcePc,x->D972Q3Coords(targetPc,Image(h,x)));;
  cert:=rec(name:=name,kind:=kind,source:=sourceName,target:=targetName,
    generator_words:=words,target_marked_coords:=List(images,x->D972Q3Coords(targetPc,x)),
    source_pc_images:=pcimgs,well_defined:=true,extra:=extra,
    hom_internal:=h);
  return cert;
end;;

D972Q3PublicMap := function(r)
  local z;
  z:=ShallowCopy(r);; Unbind(z.hom_internal);; return z;
end;;

D972Q3Checkpoint := function(label,obj)
  D972Q3AtomicWrite(Concatenation(D972_B345_Q3_OUTPUT,".",label,".json"),obj);
end;;

#############################################################################
## Coarse-q3 no-common-quotient shortcut and the exact 27-word F2 fibre.
#############################################################################

D972Q3JointBlocks := function(left,leftDegree,right,rightDegree)
  local images,offset,v,j;
  images:=[];; offset:=0;;
  for v in left do
    for j in [1..leftDegree] do Add(images,offset+j^v); od;
    offset:=offset+leftDegree;;
  od;
  for v in right do
    for j in [1..rightDegree] do Add(images,offset+j^v); od;
    offset:=offset+rightDegree;;
  od;
  return PermList(images);
end;;

D972Q3BlockRestrict := function(p,offset,size)
  local row,j;
  row:=[];;
  for j in [1..size] do row[j]:=(offset+j)^p-offset; od;
  if Set(row)<>[1..size] then Error("157da: joint block does not close"); fi;
  return PermList(row);
end;;

D972Q3PermRow := function(p,n)
  return List([1..n],i->i^p);
end;;

D972Q3SignedFpWord := function(w)
  local e,out,i,g,n,j;
  e:=ExtRepOfObj(w);; out:=[];; i:=1;;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if n>0 then for j in [1..n] do Add(out,g); od;
    else for j in [1..-n] do Add(out,-g); od; fi;
    i:=i+2;;
  od;
  return D972Q3Reduce(out);
end;;

D972Q3CorrectionFibre := function(Q0,q0x,q0y,B2,b2x,b2y)
  local iso,isoInv,B2perm,bx,by,qdeg,jx,jy,J,proj,K,F,fg,epi,pc,records,k,pre,
    word,qperm,qorig,coords,coarseDegree,pcK,pcKWords,z,e,j,coordWord;
  if Size(B2)<>27 then Error("157da: <x12,x23> is not B(2,3) of order 27"); fi;
  iso:=IsomorphismPermGroup(B2);; isoInv:=InverseGeneralMapping(iso);;
  B2perm:=Image(iso);;
  bx:=Image(iso,b2x);; by:=Image(iso,b2y);; qdeg:=LargestMovedPoint(B2perm);;
  if qdeg<1 or Size(B2perm)<>27 then Error("157da: B(2,3) permutation model drift"); fi;
  coarseDegree:=36;;
  jx:=D972Q3JointBlocks([q0x],coarseDegree,[bx],qdeg);;
  jy:=D972Q3JointBlocks([q0y],coarseDegree,[by],qdeg);;
  J:=Group(jx,jy);;
  if Size(J)<>Size(Q0)*27 then
    Error("157da: coarse/B(2,3) marked diagonal is not the direct product");
  fi;
  proj:=GroupHomomorphismByImages(J,Q0,[jx,jy],[q0x,q0y]);;
  if proj=fail or Size(Image(proj))<>Size(Q0) then
    Error("157da: coarse projection failed");
  fi;
  K:=Kernel(proj);;
  if Size(K)<>27 then Error("157da: correction kernel order drift"); fi;
  F:=FreeGroup("q3cx","q3cy");; fg:=GeneratorsOfGroup(F);;
  epi:=GroupHomomorphismByImages(F,J,fg,[jx,jy]);;
  if epi=fail or Size(Image(epi))<>Size(J) then Error("157da: F2 diagonal epi failed"); fi;
  pc:=Pcgs(B2);; records:=[];; pcK:=Pcgs(K);; pcKWords:=[];;
  if Length(pcK)>3 then Error("157da: order-27 kernel pc length exceeds three"); fi;
  # Only the pc generators of K need an expensive free preimage in J.  Every
  # one of the 27 kernel elements is then reconstructed by its pc exponents.
  for z in pcK do
    pre:=PreImagesRepresentative(epi,z);;
    if pre=fail then Error("157da: correction pc-generator preimage missing"); fi;
    Add(pcKWords,D972Q3SignedFpWord(pre));;
  od;
  # This is the only full element enumeration in production; the order-27
  # kernel was proved immediately above.  Pi5, Q4 and E4 are never enumerated.
  for k in Elements(K) do
    e:=ExponentsOfPcElement(pcK,k);; coordWord:=[];;
    for j in [1..Length(e)] do
      if e[j]<0 then Error("157da: negative correction pc exponent"); fi;
      while e[j]>0 do Add(coordWord,j);; e[j]:=e[j]-1;; od;
    od;
    word:=D972Q3WordEval(coordWord,pcKWords);;
    if D972Q3EvalGroupWord(word,[jx,jy])<>k then
      Error("157da: pc-compressed correction preimage drift");
    fi;
    if D972Q3EvalGroupWord(word,[q0x,q0y])<>One(Q0) then
      Error("157da: correction word is not coarse-trivial");
    fi;
    qperm:=D972Q3BlockRestrict(k,coarseDegree,qdeg);;
    qorig:=Image(isoInv,qperm);;
    if D972Q3EvalGroupWord(word,[b2x,b2y])<>qorig then
      Error("157da: correction q3 image/preimage drift");
    fi;
    coords:=List(ExponentsOfPcElement(pc,qorig),Int);;
    Add(records,rec(word:=word,q_coords:=coords,
      q_permutation:=List([1..qdeg],i->i^qperm)));
  od;
  Sort(records,function(a,b) return a.q_coords<b.q_coords; end);;
  if Length(Set(List(records,r->r.q_coords)))<>27 then
    Error("157da: correction fibre q3 coordinates are not bijective");
  fi;
  return rec(records:=records,B2_internal:=B2,b2x_internal:=b2x,
    b2y_internal:=b2y,permutation_degree:=qdeg,
    certificate:=rec(order:=27,enumerated_count:=27,
      only_full_enumeration:="Elements of the proved order-27 correction kernel",
      diagonal_order_decimal:=String(Size(J)),coarse_order_decimal:=String(Size(Q0)),
      direct_product:=true,projection_kernel_order:=27,
      preimage_call_count:=Length(pcK),preimage_call_bound:=3,
      pc_compressed_preimages:=true,all_words_coarse_identity:=true,
      all_q3_coordinates_unique:=true));
end;;

D972Q3PP := function(xs)
  local z,i;
  if Length(xs)=0 then Error("157da: empty paper product"); fi;
  z:=One(xs[1]);;
  for i in Reversed([1..Length(xs)]) do z:=z*xs[i];; od;
  return z;
end;;

D972Q3MarkedSub := function(word,left,right)
  local images;
  images:=List([1..6],i->[]);; images[1]:=left;; images[4]:=right;;
  return D972Q3WordEval(word,images);
end;;

D972Q3GTComposeM0 := function(left,right)
  local ximg,yimg,newright;
  ximg:=[1];; yimg:=D972Q3Reduce(Concatenation(left,[2],D972Q3Inv(left)));;
  newright:=D972Q3WordEval(right,[ximg,yimg]);;
  return D972Q3Reduce(Concatenation(newright,left));
end;;

D972Q3Pairs := function(g)
  return [[g[1],g[4]],[g[4],g[6]],[D972Q3PP([g[2],g[4]]),g[6]],
    [D972Q3PP([g[1],g[2]]),D972Q3PP([g[5],g[6]])],
    [g[1],D972Q3PP([g[4],g[5]])]];
end;;

D972Q3HexPairs := function(x,y)
  local z,u;
  z:=D972Q3PP([x,y])^-1;; u:=D972Q3PP([y,x])^-1;;
  return [[x,y],[x,z],[y,z],[u,x],[u,y]];
end;;

D972Q3HexFromValues := function(values,x,y)
  local z,u,fxy,fxz,fyz,fux,fuy;
  if Length(values)<>5 then Error("157da: hex context width"); fi;
  z:=D972Q3PP([x,y])^-1;; u:=D972Q3PP([y,x])^-1;;
  fxy:=values[1];; fxz:=values[2];; fyz:=values[3];;
  fux:=values[4];; fuy:=values[5];;
  # marking m=0, lambda=1
  return [D972Q3PP([fxy,fxz^-1,fyz]),
    D972Q3PP([fux^-1,fxy^-1,fuy])];
end;;

D972Q3PentFromValues := function(parts)
  if Length(parts)<>5 then Error("157da: pentagon context width"); fi;
  return D972Q3PP([D972Q3PP([parts[5],parts[3]])^-1,
    parts[2],parts[4],parts[1]]);
end;;

D972Q3DtildeWord := function(word)
  local marked,x15,x45,a,b,c,d,e;
  marked:=List(word,n->SignInt(n)*([1,4][AbsInt(n)]));;
  x15:=[-3,-2,-1];; x45:=[-6,-5,-3];;
  a:=D972Q3MarkedSub(marked,x45,[6]);;
  b:=D972Q3MarkedSub(marked,[1],x15);;
  c:=D972Q3MarkedSub(marked,[4],[6]);;
  d:=D972Q3MarkedSub(marked,x45,x15);;
  e:=D972Q3MarkedSub(marked,[1],[4]);;
  return D972Q3Reduce(Concatenation(D972Q3Inv(a),D972Q3Inv(b),c,d,e));
end;;

D972Q3F2ExponentSums := function(word)
  return [Sum(Filtered(word,x->AbsInt(x)=1),SignInt),
    Sum(Filtered(word,x->AbsInt(x)=2),SignInt)];
end;;

D972Q3SourceWordsM0 := function(f)
  local ff,g,gs,f1234,h,x123;
  ff:=D972Q3WordEval(f,[[1],[4]]);;
  g:=D972Q3WordEval(f,[[1],[2]]);;
  gs:=D972Q3WordEval(f,[[4],[5]]);;
  f1234:=D972Q3WordEval(f,[[4,2],[6]]);;
  x123:=[2,1];; h:=D972Q3WordEval(f,[x123,[3]]);;
  return [[1],
    D972Q3Reduce(Concatenation(D972Q3Inv(g),[2],g)),
    D972Q3Reduce(Concatenation(D972Q3Inv(ff),D972Q3Inv(h),[3],h,ff)),
    D972Q3Reduce(Concatenation(D972Q3Inv(ff),[4],ff)),
    D972Q3Reduce(Concatenation(D972Q3Inv(ff),
      D972Q3Inv(D972Q3WordEval(f,[[2,1],[6,5]])),D972Q3Inv(gs),[5],gs,
      D972Q3WordEval(f,[[2,1],[6,5]]),ff)),
    D972Q3Reduce(Concatenation(D972Q3Inv(f1234),[6],f1234))];
end;;

D972Q3ExponentMatrix := function(words,n)
  return List(words,w->List([1..n],j->
    Sum(Filtered(w,x->AbsInt(x)=j),SignInt)));
end;;

D972Q3ContextTable := function(ps,corrections)
  return rec(pairs:=ps,values:=List(ps,p->
    List(corrections,c->D972Q3EvalGroupWord(c.word,p))));
end;;

D972Q3ContextBase := function(word,table)
  return List(table.pairs,p->D972Q3EvalGroupWord(word,p));
end;;

D972Q3ContextValues := function(base,table,index)
  return List([1..Length(base)],j->base[j]*table.values[j][index]);
end;;

D972Q3OntoCached := function(value,x,y,targetSize,keys,vals)
  local pos,answer;
  pos:=Position(keys,value);;
  if pos<>fail then return vals[pos]; fi;
  answer:=Size(Group(x,D972Q3PP([value^-1,y,value])))=targetSize;;
  Add(keys,value);; Add(vals,answer);; return answer;
end;;

D972Q3OntoQ0Cached := function(value,px,py,gx,gy,keys,vals)
  local pos,answer,vp,vg;
  pos:=Position(keys,value);;
  if pos<>fail then return vals[pos]; fi;
  vp:=D972Q3BlockRestrict(value,0,9);;
  vg:=D972Q3BlockRestrict(value,9,27);;
  # Q0=P x G9 and P is perfect while G9 is solvable, so the two full
  # projections have no common nontrivial quotient and the subdirect image is
  # the full product.  This avoids Size(Group(...)) in the 1.47M-element Q0.
  answer:=Size(Group(px,D972Q3PP([vp^-1,py,vp])))=504 and
    Size(Group(gx,D972Q3PP([vg^-1,gy,vg])))=2916;;
  Add(keys,value);; Add(vals,answer);; return answer;
end;;

D972Q3CanonicalPowers := function(wordsObj,px,py,gx,gy,qx,qy,correction)
  local base,all,n,stepWord,pv,gv,qv,matches,i,row,canon,coarseElt,outside,
    canonicalKeys,canonicalIndices,corrQ,B2,B2pc,canonQ,stepFibre,canonFibre,
    fibreReceipt,maxStepLength,maxCanonicalLength,identityMatches,identityRow,baseMatches,
    nineStep,nineMatches,nineRow,orbitRows;
  if wordsObj.schema<>"d972-b4-word-key-artifact/v1" or wordsObj.count<>972 then
    Error("157da: frozen roof artifact metadata drift");
  fi;
  # Evaluate every frozen coarse key exactly once.  The six power lookups below
  # use this cache; no 972-row scan performs another long-word evaluation.
  canonicalKeys:=[];; canonicalIndices:=[];;
  for i in [1..972] do
    row:=wordsObj.rows[i];;
    Add(canonicalKeys,[row[1],D972Q3EvalGroupWord(row[3],[px,py]),
      D972Q3EvalGroupWord(row[3],[gx,gy])]);;
    Add(canonicalIndices,i);;
  od;
  identityMatches:=Positions(canonicalKeys,[0,One(px),One(gx)]);;
  if Length(identityMatches)<>1 then Error("157da: frozen m=0 coarse identity row not unique"); fi;
  identityRow:=wordsObj.rows[canonicalIndices[identityMatches[1]]];;
  corrQ:=List(correction.records,r->D972Q3EvalGroupWord(r.word,[qx,qy]));;
  B2:=Group(qx,qy);; B2pc:=Pcgs(B2);;
  if Size(B2)<>27 or Length(Set(corrQ))<>27 then
    Error("157da: canonical power correction fibre is not all B(2,3)");
  fi;
  row:=wordsObj.rows[19];;
  if row[1]<>0 then Error("157da: row18 marking drift"); fi;
  base:=row[3];;
  baseMatches:=Positions(canonicalKeys,[0,D972Q3EvalGroupWord(base,[px,py]),
    D972Q3EvalGroupWord(base,[gx,gy])]);;
  if baseMatches<>[19] then Error("157da: frozen row18 coarse key not unique"); fi;
  qv:=D972Q3EvalGroupWord(base,[qx,qy]);;
  stepFibre:=Set(List(corrQ,c->qv*c));;
  if Length(stepFibre)<>27 then Error("157da: base q3 fibre is not distinct"); fi;
  all:=[rec(exponent:=1,word:=base,row_index:=19,key:=row[2],
    q3_shift_coords:=List(ExponentsOfPcElement(B2pc,One(B2)),Int),
    q3_shift_correction_index:=Position(corrQ,One(B2)),
    q3_step_fibre_rebased:=true,q3_bounded_step_fibre_size:=27,
    q3_canonical_fibre_size:=27,bounded_step_word_length:=Length(base),
    canonical_word_length:=Length(base))];;
  maxStepLength:=Length(base);; maxCanonicalLength:=Length(base);;
  for n in [2..8] do
    # Never retain the literal f^n word.  Compose once from the preceding
    # frozen canonical row, identify the next coarse roof, then canonicalize
    # again.  Fine completeness is the whole 27-element kernel fibre over that
    # coarse point, not equality with one exponentially growing representative.
    stepWord:=D972Q3GTComposeM0(base,all[n-1].word);;
    if Length(stepWord)>100000 then Error("157da: bounded canonical step word cap n=",n); fi;
    maxStepLength:=Maximum(maxStepLength,Length(stepWord));;
    pv:=D972Q3EvalGroupWord(stepWord,[px,py]);;
    gv:=D972Q3EvalGroupWord(stepWord,[gx,gy]);;
    qv:=D972Q3EvalGroupWord(stepWord,[qx,qy]);;
    matches:=Positions(canonicalKeys,[0,pv,gv]);;
    matches:=List(matches,j->canonicalIndices[j]);;
    if Length(matches)<>1 then Error("157da: powered roof canonical row not unique n=",n); fi;
    i:=matches[1];; row:=wordsObj.rows[i];; canon:=row[3];;
    maxCanonicalLength:=Maximum(maxCanonicalLength,Length(canon));;
    canonQ:=D972Q3EvalGroupWord(canon,[qx,qy]);;
    stepFibre:=Set(List(corrQ,c->qv*c));;
    canonFibre:=Set(List(corrQ,c->canonQ*c));;
    if Length(stepFibre)<>27 or Length(canonFibre)<>27 or stepFibre<>canonFibre then
      Error("157da: bounded-step/canonical q3 correction fibres differ n=",n);
    fi;
    fibreReceipt:=rec(q3_shift_coords:=List(ExponentsOfPcElement(B2pc,
        canonQ^-1*qv),Int),q3_step_fibre_rebased:=true,
      q3_bounded_step_fibre_size:=27,
      q3_canonical_fibre_size:=27,
      q3_shift_correction_index:=Position(corrQ,canonQ^-1*qv));;
    if fibreReceipt.q3_shift_correction_index=fail then
      Error("157da: q3 rebasing shift missing from correction fibre n=",n);
    fi;
    Add(all,rec(exponent:=n,word:=canon,row_index:=i,key:=row[2],
      q3_shift_coords:=fibreReceipt.q3_shift_coords,
      q3_shift_correction_index:=fibreReceipt.q3_shift_correction_index,
      q3_step_fibre_rebased:=true,q3_bounded_step_fibre_size:=27,
      q3_canonical_fibre_size:=27,bounded_step_word_length:=Length(stepWord),
      canonical_word_length:=Length(canon)));
  od;
  nineStep:=D972Q3GTComposeM0(base,all[8].word);;
  if Length(nineStep)>100000 then Error("157da: bounded canonical step word cap n=9"); fi;
  maxStepLength:=Maximum(maxStepLength,Length(nineStep));;
  pv:=D972Q3EvalGroupWord(nineStep,[px,py]);;
  gv:=D972Q3EvalGroupWord(nineStep,[gx,gy]);;
  nineMatches:=Positions(canonicalKeys,[0,pv,gv]);;
  if Length(nineMatches)<>1 then Error("157da: normalized ninth coarse row not unique"); fi;
  nineRow:=wordsObj.rows[canonicalIndices[nineMatches[1]]];;
  if nineRow<>identityRow then Error("157da: normalized GT-compose orbit does not close at nine"); fi;
  orbitRows:=Concatenation(
    [rec(exponent:=0,row_index:=canonicalIndices[identityMatches[1]],
      key:=identityRow[2],word:=identityRow[3])],
    List(all,r->rec(exponent:=r.exponent,row_index:=r.row_index,key:=r.key,word:=r.word)),
    [rec(exponent:=9,row_index:=canonicalIndices[identityMatches[1]],
      key:=identityRow[2],word:=identityRow[3])]);;
  if Length(Set(List(orbitRows{[1..9]},r->r.row_index)))<>9 then
    Error("157da: normalized GT-compose rows n=0..8 are not pairwise distinct");
  fi;
  outside:=all{[1,2,4,5,7,8]};;
  if Length(Set(List(outside,r->r.row_index)))<>6 then
    Error("157da: outside order-nine roof orbit rows are not distinct");
  fi;
  for row in outside do
    coarseElt:=D972Q3JointBlocks([D972Q3EvalGroupWord(row.word,[px,py])],9,
      [D972Q3EvalGroupWord(row.word,[gx,gy])],27);;
    if Order(coarseElt)<>9 then Error("157da: outside roof is not order nine"); fi;
  od;
  return rec(rows:=outside,coarse_key_cache_size:=Length(canonicalKeys),
    frozen_rows_evaluated_once:=true,canonicalized_each_step:=true,
    literal_power_words_retained:=false,bounded_step_word_cap:=100000,
    max_bounded_step_word_length:=maxStepLength,
    max_canonical_word_length:=maxCanonicalLength,
    normalized_orbit:=orbitRows,normalized_orbit_first_repeat:=9,
    normalized_orbit_n0_n8_distinct:=true,normalized_orbit_n9_identity:=true,
    outside_residues_complete_mod9:=[1,2,4,5,7,8],
    coarse_power_induction:="base compose previous canonical has the next frozen coarse key",
    fine_fibre_completeness:="E3=Q0 x B(2,3): every lift over each coarse roof is the complete 27-element right fibre");
end;;

D972Q3TryFactorAutoCached := function(G,x,y,sourceRows,imageRows,tag,
    cacheKeys,cacheVals,stats)
  local key,pos,ix,iy,h,answer,i;
  key:=[tag,imageRows];; pos:=Position(cacheKeys,key);;
  if pos<>fail then
    stats.small_factor_cache_hits:=stats.small_factor_cache_hits+1;;
    return cacheVals[pos];
  fi;
  stats.small_factor_bijectivity_calls:=stats.small_factor_bijectivity_calls+1;;
  ix:=Positions(sourceRows,x);; iy:=Positions(sourceRows,y);;
  if Length(ix)<>1 or Length(iy)<>1 then
    Error("157da: settlement factor marked X/Y selector drift ",tag);
  fi;
  h:=GroupHomomorphismByImages(G,G,[x,y],[imageRows[ix[1]],imageRows[iy[1]]]);;
  answer:=h<>fail and IsBijective(h);;
  if answer then
    for i in [1..6] do
      if Image(h,sourceRows[i])<>imageRows[i] then answer:=false;; break; fi;
    od;
  fi;
  Add(cacheKeys,key);; Add(cacheVals,answer);; return answer;
end;;

D972Q3TrySettlement := function(word,Q4,q4marks,P4,p4marks,p4pc,
    pGroup,pX,pY,gGroup,gX,gY,p4rels,cacheKeys,cacheVals,
    factorKeys,factorVals,stats)
  local sourceWords,imQ,imP,hQ,hP,hPinv,key,pos,value,F,fg,epiQ,epiP,
    qInverseWords,pInverseWords,i,j,pre,forwardPc,inversePc,abMatrix,
    structural,sourceRows,imageRows;
  sourceWords:=D972Q3SourceWordsM0(word);;
  abMatrix:=D972Q3ExponentMatrix(sourceWords,6);;
  if abMatrix<>IdentityMat(6) then
    Error("157da: settlement source is not identity on PB4 abelianization");
  fi;
  imQ:=List(sourceWords,w->D972Q3EvalGroupWord(w,q4marks));;
  imP:=List(sourceWords,w->D972Q3EvalGroupWord(w,p4marks));;
  key:=[imQ,imP];; pos:=Position(cacheKeys,key);;
  if pos<>fail then
    if cacheVals[pos]=fail then return fail; fi;
    value:=ShallowCopy(cacheVals[pos]);; value.source_words:=sourceWords;;
    return value;
  fi;
  stats.structural_settlement_tests:=stats.structural_settlement_tests+1;;
  structural:=not ForAny(p4rels,r->not IsOne(D972Q3EvalGroupWord(r,imP)));;
  if structural then
    for i in [0..3] do
      sourceRows:=List(q4marks,g->D972Q3BlockRestrict(g,9*i,9));;
      imageRows:=List(imQ,g->D972Q3BlockRestrict(g,9*i,9));;
      if not D972Q3TryFactorAutoCached(pGroup,pX,pY,sourceRows,imageRows,
          Concatenation("P",String(i+1)),factorKeys,factorVals,stats) then
        structural:=false;; break;
      fi;
      sourceRows:=List(q4marks,g->D972Q3BlockRestrict(g,36+27*i,27));;
      imageRows:=List(imQ,g->D972Q3BlockRestrict(g,36+27*i,27));;
      if not D972Q3TryFactorAutoCached(gGroup,gX,gY,sourceRows,imageRows,
          Concatenation("G9_",String(i+1)),factorKeys,factorVals,stats) then
        structural:=false;; break;
      fi;
    od;
  fi;
  if not structural then
    Add(cacheKeys,key);; Add(cacheVals,fail);; return fail;
  fi;
  # The small-factor test gives an ambient P^4 x G9^4 automorphism.  Every
  # image is a word in the six H9 generators, hence its restriction is an
  # injective endomorphism of finite H9 and therefore an automorphism.  The
  # PB4 relator replay plus exponent-three verbal descent and the identity
  # Frattini matrix give the Pi4 automorphism by Burnside's basis theorem.
  # Run each old global test only once, on the first structural witness, as an
  # assertion and to export inverse/preimage receipts.
  if stats.global_Q4_bijectivity_calls<>0 or stats.global_Pi4_bijectivity_calls<>0 then
    Error("157da: repeated global settlement assertion");
  fi;
  stats.global_Q4_bijectivity_calls:=stats.global_Q4_bijectivity_calls+1;;
  hQ:=GroupHomomorphismByImages(Q4,Q4,q4marks,imQ);;
  if hQ=fail or not IsBijective(hQ) then
    Error("157da: structural/global Q4 settlement mismatch");
  fi;
  stats.global_Pi4_bijectivity_calls:=stats.global_Pi4_bijectivity_calls+1;;
  hP:=GroupHomomorphismByImages(P4,P4,p4marks,imP);;
  if hP=fail or not IsBijective(hP) then
    Error("157da: structural/global Pi4 settlement mismatch");
  fi;
  hPinv:=InverseGeneralMapping(hP);;
  forwardPc:=List(p4pc,x->D972Q3Coords(p4pc,Image(hP,x)));;
  inversePc:=List(p4pc,x->D972Q3Coords(p4pc,Image(hPinv,x)));;
  F:=FreeGroup(6);; fg:=GeneratorsOfGroup(F);;
  epiQ:=GroupHomomorphismByImages(F,Q4,fg,imQ);;
  epiP:=GroupHomomorphismByImages(F,P4,fg,imP);;
  if epiQ=fail or epiP=fail then Error("157da: settlement image epi failed"); fi;
  qInverseWords:=[];; pInverseWords:=[];;
  for i in [1..6] do
    pre:=PreImagesRepresentative(epiQ,q4marks[i]);;
    if pre=fail then Error("157da: Q4 settlement inverse word missing"); fi;
    Add(qInverseWords,D972Q3SignedFpWord(pre));;
    pre:=PreImagesRepresentative(epiP,p4marks[i]);;
    if pre=fail then Error("157da: Pi4 settlement inverse word missing"); fi;
    Add(pInverseWords,D972Q3SignedFpWord(pre));;
  od;
  value:=rec(source_words:=sourceWords,Q4_bijective:=true,
    Pi4_q3_bijective:=true,pullback_direct_product_automorphism:=true,
    Pi4_frattini_matrix:=abMatrix,
    Pi4_frattini_quotient:="PB4_ab mod 3 = (C3)^6",
    Pi4_automorphism_theorem:="Burnside basis theorem: a finite p-group endomorphism inducing an automorphism on G/Phi(G) is an automorphism",
    Q4_inverse_words:=qInverseWords,Pi4_inverse_words:=pInverseWords,
    Pi4_forward_pc_images:=forwardPc,Pi4_inverse_pc_images:=inversePc,
    independent_bijectivity_certificate:=
      "inverse words generate every coarse marked generator; forward/inverse pc homomorphisms compose on Pi4 pc generators",
    quotient_diagram:="C4=1, hence component automorphisms induce E4=Q4 x Pi4[3]");;
  Add(cacheKeys,key);; Add(cacheVals,value);; return value;
end;;

D972Q3DirectScan := function(powers,correction,Q0,q0x,q0y,Q4,q4marks,
    B2,b2x,b2y,P4,p4marks,p4pc,dG9)
  local corr,hexQ0,hexB2,pentQ4,pentP4,dB2,sizeB2,ontoQKeys,
    ontoQVals,ontoBKeys,ontoBVals,solutions,powerRows,pow,baseHQ,baseHB,basePQ,
    basePP,baseQ,counts,i,cand,hq,hb,pq,pp,vQ,vB,charm,roof,hexQV,hexBV,pentQV,
    pentPV,dword,transport,ontoQ,ontoB,settle,pre,accepted,total,exps,
    dtildeApplicable,dtildePass,settleKeys,settleVals,powerRecord,gates,
    pX,pY,gX,gY,pGroup,gGroup,p4rels,factorKeys,factorVals,settleStats,
    settlementContract,corrExps,powExps;
  corr:=correction.records;;
  hexQ0:=D972Q3ContextTable(D972Q3HexPairs(q0x,q0y),corr);;
  hexB2:=D972Q3ContextTable(D972Q3HexPairs(b2x,b2y),corr);;
  pentQ4:=D972Q3ContextTable(D972Q3Pairs(q4marks),corr);;
  pentP4:=D972Q3ContextTable(D972Q3Pairs(p4marks),corr);;
  dB2:=NormalClosure(B2,Subgroup(B2,[Comm(b2x,b2y)]));;
  sizeB2:=Size(B2);;
  pX:=D972Q3BlockRestrict(q0x,0,9);; pY:=D972Q3BlockRestrict(q0y,0,9);;
  gX:=D972Q3BlockRestrict(q0x,9,27);; gY:=D972Q3BlockRestrict(q0y,9,27);;
  pGroup:=Group(pX,pY);; gGroup:=Group(gX,gY);; p4rels:=D972Q3PureRelations(4);;
  corrExps:=List(corr,r->D972Q3F2ExponentSums(r.word));;
  ontoQKeys:=[];; ontoQVals:=[];; ontoBKeys:=[];; ontoBVals:=[];;
  settleKeys:=[];; settleVals:=[];;
  factorKeys:=[];; factorVals:=[];;
  settleStats:=rec(structural_settlement_tests:=0,
    small_factor_bijectivity_calls:=0,small_factor_cache_hits:=0,
    global_Q4_bijectivity_calls:=0,global_Pi4_bijectivity_calls:=0);;
  settlementContract:=rec(
    checked_for_every_onto_candidate:=true,
    source_abelianization_matrix:=IdentityMat(6),
    Pi4_frattini_quotient:="PB4_ab mod 3 = (C3)^6",
    Pi4_automorphism_theorem:="Burnside basis theorem: a finite p-group endomorphism inducing an automorphism on G/Phi(G) is an automorphism",
    Pi4_relation_count:=11,
    Pi4_descent:="PB4 relators replay in exponent-three Pi4, so the verbal quotient receives the endomorphism",
    Q4_factor_method:="four P and four G9 marked factor automorphisms; H9 is invariant because all six images are H9 words",
    global_Q4_and_Pi4_assertions_at_most_once:=true);;
  solutions:=[];; powerRows:=[];; total:=0;;
  gates:=rec(roof:=[],charming:=[],hexagon:=[],pentagon:=[],
    dtilde_applicable:=[],dtilde_pass:=[],onto:=[],
    settlement_tested:=[],settled:=[]);;
  for pow in powers.rows do
    baseHQ:=D972Q3ContextBase(pow.word,hexQ0);;
    baseQ:=baseHQ[1];;
    baseHB:=D972Q3ContextBase(pow.word,hexB2);;
    basePQ:=D972Q3ContextBase(pow.word,pentQ4);;
    basePP:=D972Q3ContextBase(pow.word,pentP4);;
    powExps:=D972Q3F2ExponentSums(pow.word);;
    counts:=rec(total:=0,roof:=0,charming:=0,hexagon:=0,pentagon:=0,
      dtilde_applicable:=0,dtilde_pass:=0,onto:=0,settled:=0);;
    for i in [1..Length(corr)] do
      counts.total:=counts.total+1;; total:=total+1;;
      cand:=fail;;
      hq:=D972Q3ContextValues(baseHQ,hexQ0,i);;
      hb:=D972Q3ContextValues(baseHB,hexB2,i);;
      pq:=D972Q3ContextValues(basePQ,pentQ4,i);;
      pp:=D972Q3ContextValues(basePP,pentP4,i);;
      vQ:=hq[1];; vB:=hb[1];;
      roof:=vQ=baseQ;;
      if roof then counts.roof:=counts.roof+1;; Add(gates.roof,total);; fi;
      charm:=D972Q3BlockRestrict(vQ,9,27) in dG9 and vB in dB2;;
      if roof and charm then counts.charming:=counts.charming+1;;
        Add(gates.charming,total);; fi;
      hexQV:=D972Q3HexFromValues(hq,q0x,q0y);;
      hexBV:=D972Q3HexFromValues(hb,b2x,b2y);;
      if roof and charm and ForAll(Concatenation(hexQV,hexBV),IsOne) then
        counts.hexagon:=counts.hexagon+1;;
        Add(gates.hexagon,total);;
      else continue; fi;
      pentQV:=D972Q3PentFromValues(pq);; pentPV:=D972Q3PentFromValues(pp);;
      if IsOne(pentQV) and IsOne(pentPV) then counts.pentagon:=counts.pentagon+1;;
        Add(gates.pentagon,total);;
      else continue; fi;
      # PENT-FORM' identifies Dtilde with the direct pentagon only for this
      # raw representative when its two free exponent sums vanish.  Original
      # B4 charmingness is derived-subgroup membership of the coset and does
      # not imply that raw-word condition.  Direct A.18 pentagon above is the
      # terminal gate; Dtilde is a nullable diagnostic canary only.
      exps:=powExps+corrExps[i];;
      dtildeApplicable:=exps=[0,0];; dtildePass:=fail;; dword:=fail;;
      if dtildeApplicable then
        cand:=D972Q3Reduce(Concatenation(pow.word,corr[i].word));;
        counts.dtilde_applicable:=counts.dtilde_applicable+1;;
        Add(gates.dtilde_applicable,total);;
        dword:=D972Q3DtildeWord(cand);;
        dtildePass:=D972Q3EvalGroupWord(dword,q4marks)=pentQV and
          D972Q3EvalGroupWord(dword,p4marks)=pentPV;;
        if dtildePass then counts.dtilde_pass:=counts.dtilde_pass+1;;
          Add(gates.dtilde_pass,total);; fi;
      fi;
      ontoQ:=D972Q3OntoQ0Cached(vQ,pX,pY,gX,gY,ontoQKeys,ontoQVals);;
      ontoB:=D972Q3OntoCached(vB,b2x,b2y,sizeB2,ontoBKeys,ontoBVals);;
      if ontoQ and ontoB then counts.onto:=counts.onto+1;;
        Add(gates.onto,total);; else continue; fi;
      Add(gates.settlement_tested,total);;
      if cand=fail then cand:=D972Q3Reduce(Concatenation(pow.word,corr[i].word));; fi;
      settle:=D972Q3TrySettlement(cand,Q4,q4marks,P4,p4marks,p4pc,
        pGroup,pX,pY,gGroup,gX,gY,p4rels,settleKeys,settleVals,
        factorKeys,factorVals,settleStats);;
      if settle=fail then continue; fi;
      counts.settled:=counts.settled+1;;
      Add(gates.settled,total);;
      Add(solutions,rec(exponent:=pow.exponent,roof_row_index:=pow.row_index,
        roof_key:=pow.key,correction_index:=i,correction_q_coords:=corr[i].q_coords,
        correction_word:=corr[i].word,typed_source_word:=cand,
        arithmetic_outside_by_index_three:=true,
        exponent_not_divisible_by_three:=(pow.exponent mod 3<>0),
        marking_m:=0,lambda:=1,roof_reduction_exact:=true,charming:=true,
        hexagon_exact:=true,pentagon_exact:=true,
        dtilde_diagnostic:=rec(applicable:=dtildeApplicable,value:=dtildePass,
          raw_exponent_sums:=exps,word:=dword,terminal_gate:=false),
        onto_Q0:=true,onto_B2_q3:=true,settlement:=settle));
      powerRecord:=rec(exponent:=pow.exponent,row_index:=pow.row_index,key:=pow.key,
        fibre_size:=27,evaluated_candidates:=counts.total,
        progressive_counts:=counts);;
      Add(powerRows,powerRecord);;
      return rec(universe_preregistered:=true,outside_exponents:=[1,2,4,5,7,8],
        correction_fibre_size:=27,total_candidates:=162,evaluated_candidates:=total,
        power_records:=powerRows,solutions:=solutions,solution_count:=1,
        exhaustive:=false,stop_reason:="FIRST_TYPED_WITNESS",
        gate_pass_indices:=gates,
        frozen_roof_key_cache_size:=powers.coarse_key_cache_size,
        frozen_rows_evaluated_once:=powers.frozen_rows_evaluated_once,
        fixed_context_cache:=true,settlement_image_cache_size:=Length(settleKeys),
        settlement_only_after_word_gates:=true,
        settlement_crosscheck_contract:=settlementContract,
        settlement_performance:=settleStats);
    od;
    Add(powerRows,rec(exponent:=pow.exponent,row_index:=pow.row_index,key:=pow.key,
      fibre_size:=27,evaluated_candidates:=counts.total,progressive_counts:=counts));
  od;
  if total<>162 then Error("157da: outside roof correction universe is not 6*27"); fi;
  return rec(universe_preregistered:=true,outside_exponents:=[1,2,4,5,7,8],
    correction_fibre_size:=27,total_candidates:=162,power_records:=powerRows,
    evaluated_candidates:=total,solutions:=solutions,solution_count:=0,
    exhaustive:=true,stop_reason:="ALL_162_EXHAUSTED",
    gate_pass_indices:=gates,
    frozen_roof_key_cache_size:=powers.coarse_key_cache_size,
    frozen_rows_evaluated_once:=powers.frozen_rows_evaluated_once,
    fixed_context_cache:=true,settlement_image_cache_size:=Length(settleKeys),
    settlement_only_after_word_gates:=true,
    settlement_crosscheck_contract:=settlementContract,
    settlement_performance:=settleStats);
end;;

#############################################################################
## Tiny self-test: no production PB5 construction.
#############################################################################

D972Q3SelfTest := function()
  local f,c34,c45,d4,m,small,q,Q;
  f:=D972Q3FormulaManifest();;
  if D972Q3Digest(f)<>D972Q3ExpectedFormulaSHA then
    Error("157da selftest: cross-language formula digest drift");
  fi;
  if f.presentations.PB3.relations<>D972Q3PureRelations(3) then
    Error("157da selftest: relation reconstruction drift");
  fi;
  if f.k5.vertex_count<>14 or not f.k5.boundary_zero then
    Error("157da selftest: K5 drift");
  fi;
  if LoadPackage("anupq")<>true then Error("157da selftest: ANUPQ absent"); fi;
  if PackageInfo("anupq")[1].Version<>"3.3.3" then
    Error("157da selftest: ANUPQ version drift");
  fi;
  small:=FreeGroup("x","y");;
  q:=PqEpimorphism(small : Prime:=3,ClassBound:=4,Exponent:=3);;
  if q=fail then Error("157da selftest: PqEpimorphism failed"); fi;
  Q:=Image(q);;
  if Size(Q)<>27 or Exponent(Q)<>3 or NilpotencyClassOfGroup(Q)<>2 then
    Error("157da selftest: B(2,3) terminal canary drift");
  fi;
  Print("B345_Q3_MANIFEST_READY_FOR_GHA selftest=true formulas_sha256=",
    D972Q3Digest(f),"\n");
end;;

#############################################################################
## Full bounded construction.
#############################################################################

D972Q3Run := function()
  local t,pins,p3,p4,p5,formula,formulaSha,qmap,Q5,m5,idx4,idx3,Q4,Q3,m4,m3,
    pc5,pc4,pc3,pub5,pub4,pub3,d54,d43,h54,h43,c34,c45,cof34,cof45,
    dels54,dels43,maps,slot,strand,cp,receipt,construction,typedBoundary,
    formulaCore,sourceDigest,coarseQ4Marks,CoarseQ4,H9,Q0,q0x,q0y,abQ4,
    abH9,abG9,abQ0,shortGate,wordsObj,B2,b2x,b2y,correction,powers,directScan,
    terminal,status,chiefFox,selectedSolution,coarseModels,correctionPublic,r,
    endpointReceipt,derivedH9;
  t:=Runtime();;
  pins:=rec(
    row18_producer:=D972Q3RequireSHA(D972Q3Row18Source,D972Q3Row18SourceSHA,"row18 producer"),
    row18_checker:=D972Q3RequireSHA(D972Q3Row18Checker,D972Q3Row18CheckerSHA,"row18 checker"),
    phase2b_receipt:=D972Q3RequireSHA(D972Q3Phase2b,D972Q3Phase2bSHA,"phase2b receipt"),
    frozen_word_artifact:=D972Q3RequireSHA(D972Q3Words,D972Q3WordsSHA,"word artifact"),
    row18_core:=D972Q3RequireSHA(D972Q3Core,D972Q3CoreSHA,"row18 v2 core"));;
  t:=D972Q3Phase("pins",t);;
  p3:=D972Q3BuildPureFp(3);; p4:=D972Q3BuildPureFp(4);;
  p5:=D972Q3BuildPureFp(5);;
  formula:=D972Q3FormulaManifest(p3,p4,p5);; formulaSha:=D972Q3Digest(formula);;
  if formulaSha<>D972Q3ExpectedFormulaSHA then
    Error("157da: cross-language formula digest drift: ",formulaSha);
  fi;
  if [p3.relation_count,p4.relation_count,p5.relation_count]<>[2,11,35] then
    Error("157da: FN presentation relation counts drift");
  fi;
  D972Q3Checkpoint("presentation",rec(schema:=D972Q3Schema,phase:="presentation",
    formula_sha256:=formulaSha,PB5_generator_count:=10,PB5_relation_count:=35,
    artin_faithful_replay:=true));;
  t:=D972Q3Phase("presentation",t);;
  # Reconstruct the pinned six-generator coarse joint target once.  This is
  # Q4=im(PB4 -> P^4 x H9), not the ambient E^4 source used by row18-v2.
  D972_BD_MODE:="full";;
  D972_BD_OUTPUT:=Concatenation(D972_B345_Q3_OUTPUT,".row18_core.json");;
  Read(D972Q3Core);
  coarseQ4Marks:=List([1..6],i->D972Q3JointBlocks(D972BDTuplePRows[i],9,
    D972BDTupleG9Rows[i],27));;
  CoarseQ4:=Group(coarseQ4Marks);; H9:=D972BDG9Image;;
  q0x:=D972Q3JointBlocks([D972BDPX],9,[D972BDX9],27);;
  q0y:=D972Q3JointBlocks([D972BDPY],9,[D972BDY9],27);;
  Q0:=Group(q0x,q0y);;
  if Size(Q0)<>Size(D972BDP)*Size(D972BDG9) then
    Error("157da: coarse PB3 Q0 is not P direct-product G9");
  fi;
  if Size(CoarseQ4)<>Size(D972BDP)^4*Size(H9) then
    Error("157da: actual six-generator Q4 is not P^4 direct-product H9");
  fi;
  if ForAny(coarseQ4Marks,g->ForAny([0..3],i->
       not (D972Q3BlockRestrict(g,9*i,9) in D972BDP))) then
    Error("157da: coarse Q4 marked P block lies outside P");
  fi;
  if ForAny(D972BDTupleG9Gens,g->ForAny([0..3],i->
       not (D972Q3BlockRestrict(g,27*i,27) in D972BDG9))) then
    Error("157da: H9 marked block lies outside G9");
  fi;
  # One derived computation on actual H9 suffices.  G9's already-pinned core
  # series is 2916 -> 729 -> 1; no second DerivedSubgroup or any
  # AbelianInvariants call is needed.
  derivedH9:=DerivedSubgroup(H9);;
  if Size(derivedH9)<>3^24 or QuoInt(Size(H9),Size(derivedH9))<>32 then
    Error("157da: H9 derived/order shortcut drift");
  fi;
  if D972BDG9SeriesOrders<>[2916,729,1] then
    Error("157da: pinned G9 derived series drift");
  fi;
  abH9:=rec(name:="H9_actual_six_generator_image",order_decimal:=String(Size(H9)),
    derived_order_decimal:=String(Size(derivedH9)),abelianization_order:=32,
    quotient_order:=32,coprime_to_3:=true,three_primary_trivial:=true,
    computation:="one actual DerivedSubgroup(H9); no AbelianInvariants");;
  abG9:=rec(name:="G9",order_decimal:=String(Size(D972BDG9)),
    derived_order_decimal:="729",abelianization_order:=4,quotient_order:=4,
    coprime_to_3:=true,three_primary_trivial:=true,
    computation:="reused pinned core DerivedSeries orders 2916,729,1");;
  abQ4:=rec(name:="coarse_Q4_joint_P4_H9",
    order_decimal:=String(Size(CoarseQ4)),
    derived_order_decimal:=String(Size(D972BDP)^4*
      QuoInt(Size(H9),abH9.abelianization_order)),
    abelianization_order:=abH9.abelianization_order,quotient_order:=32,
    coprime_to_3:=true,
    three_primary_trivial:=abH9.three_primary_trivial,computed_once:=true,
    reduction_proof:="Q4=P^4 x H9 and P=PSL(2,8) is perfect; Q4_ab=H9_ab");;
  abQ0:=rec(name:="coarse_Q0_P_times_G9",order_decimal:=String(Size(Q0)),
    derived_order_decimal:=String(Size(D972BDP)*
      QuoInt(Size(D972BDG9),abG9.abelianization_order)),
    abelianization_order:=abG9.abelianization_order,quotient_order:=4,
    coprime_to_3:=true,
    three_primary_trivial:=abG9.three_primary_trivial,computed_once:=true,
    reduction_proof:="Q0=P x G9 and P=PSL(2,8) is perfect; Q0_ab=G9_ab");;
  coarseModels:=rec(
    Q4:=rec(degree:=144,order_decimal:=String(Size(CoarseQ4)),
      marked_permutations:=List(coarseQ4Marks,g->D972Q3PermRow(g,144))),
    H9:=rec(degree:=108,order_decimal:=String(Size(H9)),
      marked_permutations:=List(D972BDTupleG9Gens,g->D972Q3PermRow(g,108))),
    Q0:=rec(degree:=36,order_decimal:=String(Size(Q0)),
      marked_permutations:=List([q0x,q0y],g->D972Q3PermRow(g,36))),
    G9:=rec(degree:=27,order_decimal:=String(Size(D972BDG9)),
      marked_permutations:=List([D972BDX9,D972BDY9],g->D972Q3PermRow(g,27))),
    P:=rec(degree:=9,order_decimal:=String(Size(D972BDP)),perfect:=true,
      marked_permutations:=List([D972BDPX,D972BDPY],g->D972Q3PermRow(g,9))));;
  shortGate:=rec(
    Q4:=abQ4,H9:=abH9,G9:=abG9,Q0:=abQ0,
    theorem:="a nontrivial finite 3-group quotient has a C3 quotient; therefore absence of 3-primary abelianization forbids every nontrivial common quotient with Pi_r[3]",
    Q4_common_q3_quotient_trivial:=abQ4.three_primary_trivial,
    Q0_common_q3_quotient_trivial:=abQ0.three_primary_trivial,
    actual_Q4_generator_source:="six marked joint (D972BDTuplePRows,D972BDTupleG9Rows), not ambient E^4",
    all_6x4_Q4_P_blocks_in_P:=true,
    all_6x4_H9_blocks_in_G9:=true,
    Q4_ab_reduced_to_H9_by_perfect_factor:=true,
    Q0_ab_reduced_to_G9_by_perfect_factor:=true,
    independent_nakayama_certificate:=rec(
      G9_derived_order:=729,G9_derived_structure:="C9^3",
      H9_derived_ambient:="(G9')^4 = (Z/9)^12",
      witness_generation:="all pair commutators of the six marked H9 generators and their six-generator conjugation orbit",
      mod3_span_rank:=12,nakayama_full_Z9_module:=true,
      checker_seed_commutator_count:=15,checker_module_action_cap:=72,
      checker_requires_invariant_span:=true,
      independently_reconstructed_from_marked_permutations_by_checker:=true),
    abelian_invariants_calls:=0,derived_subgroup_calls:=1,
    G9_derived_series_reused_from_core:=true,
    repeated_group_reconstruction:=false);;
  D972Q3Checkpoint("coarse_common_quotient_gate",rec(schema:=D972Q3Schema,
    phase:="coarse_common_quotient_gate",short_gate:=shortGate));;
  t:=D972Q3Phase("coarse_common_quotient_gate",t);;
  if not abQ4.three_primary_trivial or not abQ0.three_primary_trivial then
    receipt:=rec(schema:=D972Q3Schema,status:="B345_Q3_MISSING_RELATIVE_HORN_EFFECTIVITY",
      terminal_token:="B345_Q3_MISSING_RELATIVE_HORN_EFFECTIVITY",q_level:=3,
      roof_power_a_mod_9:=fail,pins:=pins,formulas:=formula,
      formula_sha256:=formulaSha,short_common_quotient_gate:=shortGate,
      coarse_models:=coarseModels,
      first_missing_map:="actual marked common C3 quotient comparison and nontrivial pullback E4=Q4 x_C4 Pi4[3]",
      production_anupq_calls:=0,PB5_skipped_before_known_typed_stop:=true,
      provenance:=rec(producer:=D972Q3Producer,
        checker:="search/check_d972_b345_q3_chief_v1.py"));;
    D972Q3AtomicWrite(D972_B345_Q3_OUTPUT,receipt);;
    Print("B345_Q3_MISSING_RELATIVE_HORN_EFFECTIVITY phase=coarse_common_quotient_gate anupq_calls=0\n");
    return;
  fi;
  if LoadPackage("anupq")<>true then Error("157da: ANUPQ package unavailable"); fi;
  if PackageInfo("anupq")[1].Version<>"3.3.3" then
    Error("157da: ANUPQ version drift: ",PackageInfo("anupq")[1].Version);
  fi;
  Print("D972_B345_Q3_HEAVY_BEGIN operation=PqEpimorphism_PB5 prime=3 class_bound=4 exponent=3 pc_cap=",D972Q3PcCap,"\n");;
  if IsBoundGlobal("FlushAllStreams") then FlushAllStreams(); fi;
  qmap:=PqEpimorphism(p5.group : Prime:=3,ClassBound:=4,Exponent:=3);;
  if qmap=fail then
    receipt:=rec(schema:=D972Q3Schema,status:="B345_Q3_UNKNOWN_RESOURCE",
      terminal_token:="B345_Q3_UNKNOWN_RESOURCE",phase:="PB5_ANUPQ",
      reason:="PqEpimorphism returned fail",q_level:=3,roof_power_a_mod_9:=fail,
      pins:=pins,formulas:=formula,formula_sha256:=formulaSha,
      short_common_quotient_gate:=shortGate,coarse_models:=coarseModels,
      production_anupq_calls:=1,no_mathematical_obstruction_claimed:=true);;
    D972Q3AtomicWrite(D972_B345_Q3_OUTPUT,receipt);;
    Print("B345_Q3_UNKNOWN_RESOURCE phase=PB5_ANUPQ\n"); return;
  fi;
  Q5:=Image(qmap);; m5:=List(p5.gens,g->Image(qmap,g));;
  if Exponent(Q5)<>3 or NilpotencyClassOfGroup(Q5)>3 then
    Error("157da: PB5 exponent-three terminal-class drift");
  fi;
  D972Q3Checkpoint("pb5_summary",rec(schema:=D972Q3Schema,phase:="PB5_q3_summary",
    order_decimal:=String(Size(Q5)),exponent:=Exponent(Q5),
    nilpotency_class:=NilpotencyClassOfGroup(Q5),formula_sha256:=formulaSha));;
  t:=D972Q3Phase("PB5_q3_summary",t);;
  idx4:=List(p4.pairs,p->Position(p5.pairs,p));;
  idx3:=List(p3.pairs,p->Position(p5.pairs,p));;
  m4:=m5{idx4};; m3:=m5{idx3};; Q4:=Group(m4);; Q3:=Group(m3);;
  pc4:=D972Q3PcReceipt("Pi4[3]",4,Q4,m4,p4);; pub4:=D972Q3PublicPcReceipt(pc4);;
  pc3:=D972Q3PcReceipt("Pi3[3]",3,Q3,m3,p3);; pub3:=D972Q3PublicPcReceipt(pc3);;
  D972Q3Checkpoint("pb4_pb3_light",rec(schema:=D972Q3Schema,
    phase:="PB4_PB3_recovered_before_full_PB5_collector",PB4:=pub4,PB3:=pub3,
    exactness_theorem:="i^-1 N_(r+1)(3)=N_r(3)"));;
  t:=D972Q3Phase("PB4_PB3_light_collectors",t);;
  # The no-common-quotient gate makes E3=Q0 x Pi3[3] and
  # E4=Q4 x Pi4[3].  The actual coarse-trivial F2 fibre is therefore the
  # order-27 kernel over B(2,3)=<A12,A23> inside Pi3[3].
  B2:=Group(m3[1],m3[3]);; b2x:=m3[1];; b2y:=m3[3];;
  correction:=D972Q3CorrectionFibre(Q0,q0x,q0y,B2,b2x,b2y);;
  for r in correction.records do
    r.ambient_Pi3_coords:=D972Q3Coords(pc3.pcgs_internal,
      D972Q3EvalGroupWord(r.word,[m3[1],m3[3]]));;
  od;
  correctionPublic:=rec(certificate:=correction.certificate,
    records:=correction.records);;
  wordsObj:=JsonStringToGap(StringFile(D972Q3Words));;
  powers:=D972Q3CanonicalPowers(wordsObj,D972BDPX,D972BDPY,D972BDX9,
    D972BDY9,b2x,b2y,correction);;
  for r in powers.rows do
    r.q3_shift_ambient_Pi3_coords:=
      correction.records[r.q3_shift_correction_index].ambient_Pi3_coords;;
  od;
  directScan:=D972Q3DirectScan(powers,correction,Q0,q0x,q0y,CoarseQ4,
    coarseQ4Marks,B2,b2x,b2y,Q4,m4,pc4.pcgs_internal,D972BDG9Series[2]);;
  D972Q3Checkpoint("direct_scan",rec(schema:=D972Q3Schema,phase:="direct_scan",
    correction_fibre:=correctionPublic,canonical_roof_powers:=powers,
    direct_word_scan:=directScan));;
  t:=D972Q3Phase("direct_word_scan",t);;
  if directScan.solution_count=1 then
    terminal:="B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION";;
    status:=terminal;; selectedSolution:=directScan.solutions[1];;
    chiefFox:=rec(executed:=false,status:="BYPASSED_BY_EXACT_WORD_CORRECTION",
      d2_bypassed_by_exact_word:=true,word_correction_exact_replay:=true,
      no_untwisted_replacement:=true);;
  else
    terminal:="B345_Q3_MISSING_TYPED_D2";; status:=terminal;;
    selectedSolution:=fail;;
    chiefFox:=rec(executed:=false,status:="MISSING_Q3_TYPED_D2",
      d2_bypassed_by_exact_word:=false,word_correction_exact_replay:=false,
      no_untwisted_replacement:=true);;
  fi;
  if directScan.solution_count=0 then
    # The PB5 O(n^2) collector and 5+6+9 map certificates are needed only for
    # the chief/d2 continuation.  A direct exact witness bypasses this bundle.
    pc5:=D972Q3PcReceipt("Pi5[3]",5,Q5,m5,p5);;
    pub5:=D972Q3PublicPcReceipt(pc5);;
    if pc5.generator_count>D972Q3PcCap then Error("157da: PB5 PC cap drift"); fi;
    D972Q3Checkpoint("pb5",rec(schema:=D972Q3Schema,phase:="PB5_q3_full_collector",
      group:=pub5,formula_sha256:=formulaSha));;
    d54:=D972Q3Deletions(5)[5];; d43:=D972Q3Deletions(4)[4];;
    h54:=D972Q3MapCertificate("delete_5_4_5","deletion","Pi5[3]","Pi4[3]",
      Q5,pc5.pcgs_internal,Q4,pc4.pcgs_internal,m5,m4,d54,rec(strand:=5));;
    h43:=D972Q3MapCertificate("delete_4_3_4","deletion","Pi4[3]","Pi3[3]",
      Q4,pc4.pcgs_internal,Q3,pc3.pcgs_internal,m4,m3,d43,rec(strand:=4));;
    if ForAny([1..Length(m4)],i->Image(h54.hom_internal,m4[i])<>m4[i]) or
       ForAny([1..Length(m3)],i->Image(h43.hom_internal,m3[i])<>m3[i]) then
      Error("157da: endpoint insertion/deletion retraction failed");
    fi;
    c34:=D972Q3Cofaces(3);; c45:=D972Q3Cofaces(4);;
    cof34:=[];;
    for slot in [0..4] do
      Add(cof34,D972Q3MapCertificate(Concatenation("coface_3_4_",String(slot)),
        "coface","Pi3[3]","Pi4[3]",Q3,pc3.pcgs_internal,Q4,pc4.pcgs_internal,
        m3,m4,c34[slot+1],rec(slot:=slot)));
    od;
    cof45:=[];;
    for slot in [0..5] do
      Add(cof45,D972Q3MapCertificate(Concatenation("coface_4_5_",String(slot)),
        "coface","Pi4[3]","Pi5[3]",Q4,pc4.pcgs_internal,Q5,pc5.pcgs_internal,
        m4,m5,c45[slot+1],rec(slot:=slot)));
    od;
    dels43:=[];;
    for strand in [1..3] do
      Add(dels43,D972Q3MapCertificate(Concatenation("delete_4_3_",String(strand)),
        "deletion","Pi4[3]","Pi3[3]",Q4,pc4.pcgs_internal,Q3,pc3.pcgs_internal,
        m4,m3,D972Q3Deletions(4)[strand],rec(strand:=strand)));
    od;
    Add(dels43,h43);;
    dels54:=[];;
    for strand in [1..4] do
      Add(dels54,D972Q3MapCertificate(Concatenation("delete_5_4_",String(strand)),
        "deletion","Pi5[3]","Pi4[3]",Q5,pc5.pcgs_internal,Q4,pc4.pcgs_internal,
        m5,m4,D972Q3Deletions(5)[strand],rec(strand:=strand)));
    od;
    Add(dels54,h54);;
    maps:=rec(cofaces_3_4:=List(cof34,D972Q3PublicMap),
      cofaces_4_5:=List(cof45,D972Q3PublicMap),
      deletions_4_3:=List(dels43,D972Q3PublicMap),
      deletions_5_4:=List(dels54,D972Q3PublicMap));;
    endpointReceipt:=rec(status:="REUSED_DELETION_RECORDS",
      PB5_to_PB4:=maps.deletions_5_4[5],
      PB4_to_PB3:=maps.deletions_4_3[4]);;
    D972Q3Checkpoint("cofaces",rec(schema:=D972Q3Schema,phase:="cofaces",
      maps:=maps,formula_sha256:=formulaSha));;
    t:=D972Q3Phase("PB5_full_collector_and_maps",t);;
  else
    pub5:=rec(name:="Pi5[3]",rank:=5,summary_only:=true,
      order_decimal:=String(Size(Q5)),exponent:=Exponent(Q5),
      nilpotency_class:=NilpotencyClassOfGroup(Q5),
      full_collector_and_maps_bypassed_by_exact_word:=true);;
    maps:=rec(status:="BYPASSED_BY_EXACT_WORD_CORRECTION",
      cofaces_3_4:=[],cofaces_4_5:=[],deletions_4_3:=[],deletions_5_4:=[]);;
    endpointReceipt:=rec(status:="BYPASSED_BY_EXACT_WORD_CORRECTION",
      theorem:="i^-1 N_(r+1)(3)=N_r(3)");;
  fi;
  typedBoundary:=rec(
    coarse_M5_required:=false,
    fine_syzygy_target:="Pi5[3]",
    frozen_row18_v2_typing:=rec(
      producer_sha256:=D972Q3Row18SourceSHA,
      coarse_Q4_candidate:="six-marked-generator joint target image (D972BDTuplePGens,D972BDTupleG9Gens), not the ambient E^4 source",
      ambient_source_certificate:="P^4 direct product times H9=im(PB4->G9^4), with kernel V^4",
      runtime_pullback_receipt_available_here:=true),
    pullback_required:=rec(
      definitions:="Q4=PB4/M4; P4=PB4/N4(3); C4=PB4/(M4*N4(3)); K4=M4 intersection N4(3); E4=PB4/K4",
      square:="E4 = Q4 x_C4 P4",kernel:="V=ker(E4->Q4)",
      injection:="V -> P4"),
    q3_system_ready:=true,common_quotient_C4_trivial:=true,
    pullback_certified:=rec(E3:="Q0 x Pi3[3]",E4:="Q4 x Pi4[3]",
      V:="Pi4[3]",V_to_Pi4_injective:=true,
      reason:="Q0_ab and Q4_ab have trivial 3-primary part"),
    actual_coarse_trivial_correction_fibre_order:=27,
    first_missing_map:=fail,
    why_pi5_alone_is_not_effectivity:="Resolved here by the exact order-27 coarse-trivial F2 fibre; Pi5 remains the uniform six-face chief target if no exact word correction settles",
    forbidden_substitute:="untwisted H1 tensor complex",
    comparison_phi_status:="NOT_NEEDED_FOR_EXACT_WORD_BYPASS_OR_NOT_REACHED_BEFORE_Q3_TYPED_D2");;
  if terminal="B345_Q3_MISSING_TYPED_D2" then
    typedBoundary.first_missing_map:=
      "Q3_TYPED_D2: six-face Pi5[3] relative chief differential after exhaustive failure of all 6*27 exact word corrections";;
  fi;
  construction:=rec(
    prime:=3,exponent_law:=3,class_bound_requested:=4,
    anupq_calls:=1,anupq_group:="PB5 only",anupq_version:="3.3.3",
    terminal_class_theorem:=rec(authors:="F. Levi and B. L. van der Waerden",
      title:="Ueber eine besondere Klasse von Gruppen",
      journal:="Abhandlungen aus dem Mathematischen Seminar der Universitaet Hamburg 9 (1932), 154-158",
      doi:="10.1007/BF02940639",
      statement:="every exponent-three group is nilpotent of class at most three; |B(d,3)|=3^(d+C(d,2)+C(d,3))"),
    next_class_requested_in_same_call:=true,
    observed_PB5_class:=pub5.nilpotency_class,
    terminal_not_truncated:=pub5.nilpotency_class<=3,
    PB4_PB3_recovery:="endpoint insertion images plus deletion retractions; i^-1 N_(r+1)(3)=N_r(3)",
    independent_checker_anupq_contract:="Python replays every collector and map used by the selected branch but does not rerun ANUPQ; the exact-word branch deliberately omits the unused PB5 full collector; maximal exponent-three quotient provenance is the pinned PqEpimorphism API plus the Levi-van der Waerden class bound",
    large_group_full_element_enumeration:=false,
    bounded_kernel_enumeration_order:=27,
    correction_preimage_call_count:=correction.certificate.preimage_call_count,
    full_PB5_collector_built:=(directScan.solution_count=0),
    PB5_map_bundle_built:=(directScan.solution_count=0),
    direct_scan_precedes_full_PB5_collector:=true,
    cayley_tables:=false,coarse_M5:=false);
  receipt:=rec(schema:=D972Q3Schema,status:=status,
    terminal_token:=terminal,
    q_level:=3,roof_power_a_mod_9:=fail,pins:=pins,construction:=construction,
    formulas:=formula,formula_sha256:=formulaSha,
    short_common_quotient_gate:=shortGate,coarse_models:=coarseModels,
    groups:=rec(PB3:=pub3,PB4:=pub4,PB5:=pub5),maps:=maps,
    endpoint_retractions:=endpointReceipt,
    correction_fibre:=correctionPublic,canonical_roof_powers:=powers,
    direct_word_scan:=directScan,selected_solution:=selectedSolution,
    typed_relative_stage:=typedBoundary,
    chief_fox:=chiefFox,
    coset_sign_comparison:=rec(executed:=false,
      status:="NOT_NEEDED_FOR_EXACT_WORD_BYPASS_OR_NOT_REACHED",
      stabilizer_computed:=false),
    performance:=rec(one_gap_process:=true,anupq_calls:=1,pc_generator_cap:=D972Q3PcCap,
      large_group_full_enumeration:=false,bounded_order27_enumeration:=true,
      fixed_word_context_caches:=true,frozen_972_rows_evaluated_once:=true,
      settlement_image_cache:=true,
      atomic_checkpoint_policy:="presentation, coarse gate, PB5 summary, PB4/PB3 light, direct scan; PB5 full collector/cofaces only after exhaustive negative",
      direct_scan_checkpoint:=true,full_PB5_checkpoints_only_after_negative:=true),
    provenance:=rec(producer:=D972Q3Producer,
      checker:="search/check_d972_b345_q3_chief_v1.py"));;
  if selectedSolution<>fail then
    receipt.roof_power_a_mod_9:=selectedSolution.exponent;;
  fi;
  D972Q3AtomicWrite(D972_B345_Q3_OUTPUT,receipt);;
  t:=D972Q3Phase("artifact",t);;
  Print(terminal," output=",D972_B345_Q3_OUTPUT,
    " formula_sha256=",formulaSha," PB5_order=",pub5.order_decimal,
    " solutions=",directScan.solution_count," evaluated=",
    directScan.evaluated_candidates," runtime_ms=",Runtime(),"\n");
end;;

if IsBound(D972_B345_Q3_SELFTEST) and D972_B345_Q3_SELFTEST=true then
  if IsBound(D972_B345_Q3_RUN) and D972_B345_Q3_RUN=true then
    Error("157da: SELFTEST and RUN are mutually exclusive");
  fi;
  D972Q3SelfTest();;
elif IsBound(D972_B345_Q3_RUN) and D972_B345_Q3_RUN=true then
  if not IsBound(D972_B345_Q3_OUTPUT) then
    D972_B345_Q3_OUTPUT:="ci/out/d972_b345_q3_chief_v1.json";;
  fi;
  D972Q3Run();;
else
  Error("157da: set exactly one of D972_B345_Q3_SELFTEST or D972_B345_Q3_RUN");
fi;
