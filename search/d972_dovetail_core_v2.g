#############################################################################
## Reusable D972 v2 core.
##
## This file intentionally contains definitions only.  It has no mode dispatch,
## environment-controlled task Read, or QUIT.  The v2 power producer Reads
## this core, which Reads only the four fixed helper libraries below.
#############################################################################

Read("search/probe/wac_v1/gap_output_prelude.g");;
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

D972Join := function(xs, sep)
  local ans, i;
  if Length(xs) = 0 then return ""; fi;
  ans := xs[1];
  for i in [2..Length(xs)] do ans := Concatenation(ans, sep, xs[i]); od;
  return ans;
end;;

D972ShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;

D972DirectSumPerm := function(p, psize, q, qsize)
  return p * D972ShiftPerm(q, psize, qsize);
end;;

D972ApplyChain := function(homs, g)
  local h, v;
  v := g;
  for h in homs do v := Image(h, v); od;
  return v;
end;;

D972SignedWord := function(w)
  local ext, out, i, gen, exp, j;
  ext := ExtRepOfObj(w);
  out := [];
  i := 1;
  while i <= Length(ext) do
    gen := ext[i]; exp := ext[i+1];
    if exp > 0 then for j in [1..exp] do Add(out,gen); od;
    else for j in [1..-exp] do Add(out,-gen); od; fi;
    i := i+2;
  od;
  return out;
end;;

## Construct barQ=B3/M without a |barQ|-degree regular representation.  The
## K9 and N_S4 quotients are each built on six pure-coset blocks, then combined
## generatorwise.  The degree is 6*2916 + 6*504 = 20520.
D972BuildBase := function(withPresentation)
  local g9, G9, x9, y9, a1, a2, a1ok, a2ok, braidAut, squareAut,
        qt9, Smat, Tmat, Sperm, Tperm, w, x4, y4, P4, qt4,
        s1, s2, Q, braid, qsize, eps, epsok, kerSize, pureSize,
        iso, Qfp, rels, relLists, fpGens,compactX,compactY,compactPure;
  g9 := MakeGn(9);
  G9 := g9.G; x9 := g9.x; y9 := g9.y;
  if Size(G9) <> 2916 then Error("D972 core: |G9| drift"); fi;

  a1 := GroupHomomorphismByImages(G9, G9, [x9,y9], [x9,y9^-1*x9^-1]);
  a2 := GroupHomomorphismByImages(G9, G9, [x9,y9], [x9^-1*y9^-1,y9]);
  a1ok := a1 <> fail and IsBijective(a1);
  a2ok := a2 <> fail and IsBijective(a2);
  if not (a1ok and a2ok) then Error("D972 core: K9 sigma action failed"); fi;
  braidAut := ForAll([x9,y9], z ->
    D972ApplyChain([a1,a2,a1],z) = D972ApplyChain([a2,a1,a2],z));
  squareAut := ForAll([x9,y9], z ->
      D972ApplyChain([a1,a1],z) = x9*z*x9^-1) and
    ForAll([x9,y9], z -> D972ApplyChain([a2,a2],z) = y9*z*y9^-1);
  if not (braidAut and squareAut and Size(Group(a1,a2)) = 17496) then
    Error("D972 core: K9 full-B3 action gates failed");
  fi;
  qt9 := BuildQTGeneral(G9, x9, y9, ());
  if Size(Group(qt9.s1,qt9.s2)) <> 17496 then
    Error("D972 core: K9 transversal quotient order drift");
  fi;

  CheckGF8();
  Smat := MakeMatGF8(1,0,1,1);
  Tmat := MakeMatGF8(4,3,1,5);
  Sperm := MatToPermGF8(Smat);
  Tperm := MatToPermGF8(Tmat);
  w := Sperm*Tperm^-1;
  x4 := w^2;
  y4 := Sperm^-1*x4*Sperm;
  P4 := Group(x4,y4);
  if Size(P4) <> 504 then Error("D972 core: PSL(2,8) order drift"); fi;
  qt4 := BuildQTGeneral(P4, x4, y4, ());
  if Size(Group(qt4.s1,qt4.s2)) <> 3024 then
    Error("D972 core: N_S4 full-B3 quotient order drift");
  fi;

  s1 := D972DirectSumPerm(qt9.s1, 6*2916, qt4.s1, 6*504);
  s2 := D972DirectSumPerm(qt9.s2, 6*2916, qt4.s2, 6*504);
  Q := Group(s1,s2);
  braid := s1*s2*s1 = s2*s1*s2;
  qsize := Size(Q);
  if not braid or qsize <> 8817984 then
    Error("D972 core: marked fibre-product braid/order gate failed");
  fi;
  eps := GroupHomomorphismByImages(Q, SymmetricGroup(3), [s1,s2], [(1,2),(2,3)]);
  epsok := eps <> fail and IsSurjective(eps);
  if not epsok then Error("D972 core: epsilon map failed"); fi;
  kerSize := Size(Kernel(eps));
  pureSize := Size(Group(s1^2,s2^2));
  if kerSize <> 1469664 or pureSize <> 1469664 then
    Error("D972 core: pure-kernel order drift");
  fi;
  compactX:=D972DirectSumPerm(x9,27,x4,9);
  compactY:=D972DirectSumPerm(y9,27,y4,9);
  compactPure:=Group(compactX,compactY);
  if Size(compactPure)<>pureSize then
    Error("D972 core: compact pure model order drift");
  fi;

  relLists := [];
  Qfp := fail;
  if withPresentation then
    iso := IsomorphismFpGroupByGenerators(Q,[s1,s2],"q");
    Qfp := Image(iso);
    fpGens := GeneratorsOfGroup(Qfp);
    if Length(fpGens) <> 2 or Image(iso,s1) <> fpGens[1] or
       Image(iso,s2) <> fpGens[2] then
      Error("D972 core: fp marking was not preserved");
    fi;
    rels := RelatorsOfFpGroup(Qfp);
    relLists := List(rels, D972SignedWord);
    if Size(Qfp) <> qsize or fpGens[1]*fpGens[2]*fpGens[1] <>
       fpGens[2]*fpGens[1]*fpGens[2] then
      Error("D972 core: fp presentation order/braid gate failed");
    fi;
  fi;
  return rec(q:=Q,s1:=s1,s2:=s2,q_size:=qsize,epsilon_kernel_size:=kerSize,
    pure_size:=pureSize,braid:=braid,k9_action_braid:=braidAut,
    k9_action_squares:=squareAut,fp:=Qfp,relator_lists:=relLists,
    k9:=g9,psl4:=P4,qt9:=qt9,qt4:=qt4,
    compact_pure:=compactPure,compact_x:=compactX,compact_y:=compactY,
    component9_degree:=6*2916,component4_degree:=6*504);
end;;

D972BlockRestrict := function(perm, offset, size)
  local images, j;
  images:=[];
  for j in [1..size] do images[j]:=(offset+j)^perm-offset; od;
  if Set(images)<>[1..size] then Error("target component does not preserve its block"); fi;
  return PermList(images);
end;;

D972D9Coordinates := function(perm)
  local rs,r,s,a,e;
  rs:=MakeDn(9); r:=rs[1]; s:=rs[2];
  for a in [0..8] do for e in [0..1] do
    if perm=r^a*s^e then return [a,e]; fi;
  od; od;
  Error("K9 component block is not in the fixed D9 normal-form table");
end;;

D972Can9 := function(perm27)
  local out,i;
  out:=[];
  for i in [0..2] do Add(out,D972D9Coordinates(D972BlockRestrict(perm27,9*i,9))); od;
  return out;
end;;

D972Can4 := function(perm9)
  return List([1..9],j->j^perm9);
end;;

D972NFTargetKey := function(m, perm27, perm9)
  local can9,can4,can9flat;
  can9:=D972Can9(perm27); can4:=D972Can4(perm9);
  can9flat:=Concatenation(can9[1],can9[2],can9[3]);
  return Concatenation("(",String(m mod 18),";",
    D972Join(List(can9flat,String),","),";",
    D972Join(List(can4,String),","),")");
end;;

D972HistogramJson := function(counts)
  local sizes, rows, n;
  sizes:=Set(Filtered(counts,n->n>0));
  rows:=[];
  for n in sizes do
    Add(rows,Concatenation("{\"fiber_size\":",String(n),
      ",\"target_count\":",String(Number(counts,x->x=n)),"}"));
  od;
  return Concatenation("[",D972Join(rows,","),"]");
end;;

D972ScanCalibrationBase := function(B)
  local P,s1,s2,x,y,c,F2bar,D,dElts,Nord,charmingMs,rows,keys,
        compact,compactX,compactY,zElt,theta,tau,thetaf,ymf,tauymf,
        tau2ymf,fullF2,toFull,fullf,m,u,f,lhs,rhs,img1,img2,hom,
        settled,settledCount,key,g9f,p4f,candidateCount,targetKeys,
        fiberCounts,targetDigest,shortcutPassCount;
  P:=B.q; s1:=B.s1; s2:=B.s2;
  x:=s1^2; y:=s2^2; c:=AbstractProd([s1,s2,s1])^2;
  if c<>One(P) then Error("core calibration shortcut requires c in M"); fi;
  compact:=B.compact_pure; compactX:=B.compact_x; compactY:=B.compact_y;
  zElt:=AbstractProd([compactX,compactY])^-1;
  theta:=GroupHomomorphismByImages(compact,compact,[compactX,compactY],
    [compactY,compactX]);
  tau:=GroupHomomorphismByImages(compact,compact,[compactX,compactY],
    [compactY,zElt]);
  if theta=fail or tau=fail then
    Error("core calibration theta/tau maps did not descend with c=1");
  fi;
  F2bar:=compact; D:=DerivedSubgroup(F2bar); dElts:=Elements(D);
  fullF2:=Group(x,y);
  toFull:=GroupHomomorphismByImages(compact,fullF2,[compactX,compactY],[x,y]);
  if toFull=fail or not IsBijective(toFull) then
    Error("core calibration compact/full marked pure models disagree");
  fi;
  Nord:=Lcm(Order(x),Order(y),Order(c));
  charmingMs:=Filtered([0..Nord-1],m->Gcd(2*m+1,Nord)=1);
  rows:=[]; keys:=[]; settledCount:=0; shortcutPassCount:=0;
  candidateCount:=Length(charmingMs)*Length(dElts);
  for m in charmingMs do
    u:=2*m+1;
    for f in dElts do
      thetaf:=Image(theta,f);
      if AbstractProd([f,thetaf])=One(compact) then
        ymf:=AbstractProd([compactY^m,f]);
        tauymf:=Image(tau,ymf); tau2ymf:=Image(tau,tauymf);
        if AbstractProd([tau2ymf,tauymf,ymf])=One(compact) and
           Size(Group(compactX^u,
             AbstractProd([f^-1,compactY^u,f])))=Size(compact) then
          shortcutPassCount:=shortcutPassCount+1;
          fullf:=Image(toFull,f);
          lhs:=AbstractProd([s1^u,fullf^-1,s2^u,fullf]);
          rhs:=AbstractProd([fullf^-1,s1,s2,x^(-m),c^m]);
          if lhs<>rhs then Error("core shortcut/full literal equation 3.3 drift"); fi;
          lhs:=AbstractProd([fullf^-1,s2^u,fullf,s1^u]);
          rhs:=AbstractProd([s2,s1,y^(-m),c^m,fullf]);
          if lhs<>rhs then Error("core shortcut/full literal equation 3.4 drift"); fi;
          img1:=s1^u;
          img2:=AbstractProd([fullf^-1,s2^u,fullf]);
          if Size(Group(img1,img2))<>Size(P) then
            Error("core shortcut/full literal surjectivity drift");
          fi;
          hom:=GroupHomomorphismByImages(P,P,[s1,s2],[img1,img2]);
          settled:=hom<>fail and IsBijective(hom);
          if settled then settledCount:=settledCount+1; fi;
          g9f:=D972BlockRestrict(f,0,27);
          p4f:=D972BlockRestrict(f,27,9);
          key:=D972NFTargetKey(m,g9f,p4f);
          Add(rows,rec(m:=m,f:=fullf,key:=key,settled:=settled));
          Add(keys,key);
        fi;
      fi;
    od;
  od;
  targetKeys:=Set(keys);
  fiberCounts:=List(targetKeys,k->Number(keys,x->x=k));
  targetDigest:=HexSHA256(Concatenation(D972Join(targetKeys,"\n"),"\n"));
  if Length(keys)<>Length(targetKeys) or Length(targetKeys)<>972 or
     targetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" then
    Error("core calibration target set/order disagrees with frozen NF-972 keys");
  fi;
  return rec(shadows:=rows,shadow_count:=Length(rows),
    settled_count:=settledCount,n_ord:=Nord,derived_order:=Length(dElts),
    charming_m:=charmingMs,candidate_count:=candidateCount,
    shortcut_pass_count:=shortcutPassCount,target_keys:=targetKeys,
    target_key_set_sorted_sha256:=targetDigest,fiber_counts:=fiberCounts,
    image_size:=Length(Filtered(fiberCounts,n->n>0)),
    zero_count:=Number(fiberCounts,n->n=0),
    histogram_json:=D972HistogramJson(fiberCounts));
end;;
