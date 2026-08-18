#############################################################################
## d972_b34_total_linking_c3_chief_v1.g
##
## One exact total-linking C3 chief descent below the frozen q3/A5^4 stage.
## The registered 157dp candidate is replayed; there is no candidate scan.
#############################################################################

Read("search/gaplib_common.g");;
if LoadPackage("json")<>true then Error("157dq: GAP json unavailable"); fi;;

D972TLProducer := "search/d972_b34_total_linking_c3_chief_v1.g";;
D972TLSchema := "d972-b34-total-linking-c3-chief/v1";;
D972TLQ3Path := "ci/out/d972_b345_q3_chief_v1.json";;
D972TLQ3SHA := "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72";;
D972TLFC8Path := "ci/out/d972_b4_fc8_a5four_v1.json";;
D972TLFC8SHA := "558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584";;
D972TLDPPath := "ci/out/d972_b34_a5_selected_lift_v1.json";;
D972TLDPSHA := "d3cb729d972a1b460cd8f0a76b49cd6abf4eafd7fe0c112ad0ad742de5200157";;
D972TLOldProducer := "search/d972_b34_a5_selected_lift_v1.g";;
D972TLOldProducerSHA := "9fb5fa16cd913ba559e96a0431cf6be4b902f1dedff289ab7e5e3d6c9adb6500";;
D972TLOldChecker := "search/check_d972_b34_a5_selected_lift_v1.py";;
D972TLOldCheckerSHA := "2d30b1458725cb70d94cb4ab35256988bf23cc2d796a422d3f0b14d1c2f6805e";;
D972TLOldDriver := "search/d972_b34_a5_selected_lift_gha_driver_v1.g";;
D972TLOldDriverSHA := "cce2dff8e4a96046d97f70f64a31f279ced5feeeb08dca55de82b59f7154171e";;
D972TLWordsPath := "search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972TLWordsSHA := "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9";;
D972TLAxisPath := "sol/luna_reply_157cp_c5_surgery_torsor_chief.md";;
D972TLAxisSHA := "59c96e7d62a20af4207f715df8e2927a8fc373e1f12e8f3be70e535d8afe5347";;
D972TLT48Path := "docs/notes/t48_157dp_answer_v1.md";;
D972TLT48SHA := "c90ffc1684f44b17602d55769cc18c8197300ed6477c4501d63455ec40c97dcc";;
D972TLPass := "B34_TOTAL_LINKING_C3_CHIEF_DESCENT_CROSSCHECKED";;
D972TLReject := "B34_TOTAL_LINKING_C3_CANDIDATE_REJECTED_CROSSCHECKED";;
D972TLUnknownInput := "B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_INPUT";;
D972TLUnknownResource := "B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_RESOURCE";;
D972TLIOMarker := "D972_B34_TOTAL_LINKING_C3_CHECKED_IO_SELFTEST_PASS";;
D972TLIOMarkerCount := 0;;

D972TLRequireSHA := function(path,expected,label)
  local raw,got;
  raw:=StringFile(path);;
  if raw=fail then Error("157dq: missing ",label," ",path); fi;
  got:=HexSHA256(raw);;
  if got<>expected then Error("157dq: SHA drift ",label," got=",got); fi;
  return rec(path:=path,sha256:=got,bytes:=Length(raw));
end;;

# The frozen 157dp producer is loaded only as a word/permutation/PC helper
# library in its selftest mode.  Its full 202500 scan is never entered here.
D972TLRequireSHA(D972TLOldProducer,D972TLOldProducerSHA,"157dp producer");;
D972_B34_A5_SELECTED_LIFT_SELFTEST:=true;;
Read(D972TLOldProducer);;
Unbind(D972_B34_A5_SELECTED_LIFT_SELFTEST);;

D972TLRead := function(path,sha,label)
  local r;
  r:=D972A5LReadJSON(path,label);;
  if r.sha256<>sha then Error("157dq: frozen artifact drift ",label); fi;
  return r.obj;
end;;

D972TLWPP := function(words)
  local out,i;
  out:=[];;
  for i in Reversed([1..Length(words)]) do
    out:=D972A5LReduce(Concatenation(out,words[i]));;
  od;
  return out;
end;;

D972TLWordPairs := function(rank)
  return List([1..rank*(rank-1)/2],i->[i]);
end;;

D972TLPentagonWord := function(f)
  local g,p,v;
  g:=D972TLWordPairs(4);;
  p:=[[g[1],g[4]],[g[4],g[6]],[D972TLWPP([g[2],g[4]]),g[6]],
    [D972TLWPP([g[1],g[2]]),D972TLWPP([g[5],g[6]])],
    [g[1],D972TLWPP([g[4],g[5]])]];;
  v:=List(p,x->D972A5LSub(f,x));;
  return D972TLWPP([D972A5LInv(D972TLWPP([v[5],v[3]])),v[2],v[4],v[1]]);
end;;

D972TLHexagonWords := function(f)
  local x,y,z,u,p,v;
  x:=[1];; y:=[3];; z:=D972A5LInv(D972TLWPP([x,y]));;
  u:=D972A5LInv(D972TLWPP([y,x]));;
  p:=[[x,y],[x,z],[y,z],[u,x],[u,y]];;
  v:=List(p,q->D972A5LSub(f,q));;
  return [D972TLWPP([v[1],D972A5LInv(v[2]),v[3]]),
    D972TLWPP([D972A5LInv(v[4]),D972A5LInv(v[1]),v[5]])];
end;;

D972TLSourceWords := function(f)
  local ff,g,gs,f1234,h,middle;
  ff:=D972A5LSub(f,[[1],[4]]);;
  g:=D972A5LSub(f,[[1],[2]]);;
  gs:=D972A5LSub(f,[[4],[5]]);;
  f1234:=D972A5LSub(f,[[4,2],[6]]);;
  h:=D972A5LSub(f,[[2,1],[3]]);;
  middle:=D972A5LSub(f,[[2,1],[6,5]]);;
  return [[1],
    D972A5LReduce(Concatenation(D972A5LInv(g),[2],g)),
    D972A5LReduce(Concatenation(D972A5LInv(ff),D972A5LInv(h),[3],h,ff)),
    D972A5LReduce(Concatenation(D972A5LInv(ff),[4],ff)),
    D972A5LReduce(Concatenation(D972A5LInv(ff),D972A5LInv(middle),
      D972A5LInv(gs),[5],gs,middle,ff)),
    D972A5LReduce(Concatenation(D972A5LInv(f1234),[6],f1234))];
end;;

D972TLExponentSums := function(w,n)
  return List([1..n],i->Sum(Filtered(w,x->AbsInt(x)=i),SignInt));
end;;

D972TLExponentMatrix := function(words,n)
  return List(words,w->D972TLExponentSums(w,n));
end;;

D972TLRankMod := function(matrix,p)
  local a,m,n,r,c,k,t,inv,j;
  a:=List(matrix,row->List(row,x->x mod p));;
  m:=Length(a);; if m=0 then return 0; fi;; n:=Length(a[1]);;
  r:=0;;
  for c in [1..n] do
    k:=PositionProperty([r+1..m],i->a[i][c]<>0);;
    if k<>fail then
      k:=r+k;; t:=a[r+1];; a[r+1]:=a[k];; a[k]:=t;;
      inv:=1;; if p=3 and a[r+1][c]=2 then inv:=2;; fi;
      a[r+1]:=List(a[r+1],x->(inv*x) mod p);;
      for k in [1..m] do
        if k<>r+1 and a[k][c]<>0 then
          t:=a[k][c];;
          for j in [1..n] do a[k][j]:=(a[k][j]-t*a[r+1][j]) mod p;; od;
        fi;
      od;
      r:=r+1;;
    fi;
  od;
  return r;
end;;

D972TLRestrict := function(p,offset,width)
  local row;
  row:=List([1..width],i->(offset+i)^p-offset);;
  if Set(row)<>[1..width] then Error("157dq: non-invariant permutation block"); fi;
  return PermList(row);
end;;

D972TLQuotientBit := function(value,derived,reps,bits)
  local i;
  for i in [1..Length(reps)] do
    if value*reps[i]^-1 in derived then return bits[i]; fi;
  od;
  Error("157dq: G9 value has no abelian coset representative");
end;;

D972TLH9Lattice := function(q3,pc4,fc)
  local gmarks,gx,gy,gz,G9,dG,dels,blocks,hrows,receiptRows,i,j,hModel,
    reps,bits,matrix,expectedMatrix,b,kernel,H9,dH9,piCoords,piMatrix,dPi,residues,basis,
    sums,edgePairs,vertexPerms,edgePerms,v,p,q,edgeGroup,artinWords,
    inverseArtin,q4marks,relations,targetOK,actionMatrices,ep;
  gmarks:=List(q3.coarse_models.G9.marked_permutations,D972A5LPermFromRow);;
  gx:=gmarks[1];; gy:=gmarks[2];; gz:=D972A5LPP([gx,gy])^-1;;
  G9:=Group(gx,gy);; dG:=DerivedSubgroup(G9);;
  if Size(G9)<>2916 or Size(dG)<>729 then Error("157dq: G9 structure drift"); fi;
  dels:=q3.formulas.deletions_4_3;;
  if dels<>D972A5LDeletions(4) then Error("157dq: deletion formula drift"); fi;
  blocks:=List([1..6],j->List([1..4],i->D972A5LEval(dels[i][j],[gx,gz,gy])));;
  hrows:=List(blocks,r->D972A5LBlockPerm(r,[27,27,27,27]));;
  hModel:=List(q3.coarse_models.H9.marked_permutations,D972A5LPermFromRow);;
  if hrows<>hModel then Error("157dq: reconstructed H9 marked rows drift"); fi;
  reps:=[One(G9),gx,gy,gx*gy];; bits:=[[0,0],[1,0],[0,1],[1,1]];;
  if ForAny(Combinations([1..4],2),p->reps[p[1]]*reps[p[2]]^-1 in dG) then
    Error("157dq: G9/G9' coset basis drift");
  fi;
  matrix:=List([1..8],z->[]);;
  for j in [1..6] do
    for i in [1..4] do
      b:=D972TLQuotientBit(blocks[j][i],dG,reps,bits);;
      Add(matrix[2*i-1],b[1]);; Add(matrix[2*i],b[2]);;
    od;
  od;
  kernel:=Filtered(Tuples([0,1],6),v->ForAll(matrix,r->
    Sum([1..6],i->r[i]*v[i]) mod 2=0));;
  expectedMatrix:=[
    [0,0,0,1,1,0],[0,0,0,0,1,1],
    [0,1,1,0,0,0],[0,0,1,0,0,1],
    [1,0,1,0,0,0],[0,0,1,0,1,0],
    [1,1,0,0,0,0],[0,1,0,1,0,0]];;
  H9:=Group(hrows);; dH9:=DerivedSubgroup(H9);;
  if matrix<>expectedMatrix or D972TLRankMod(matrix,2)<>5 or
     kernel<>[[0,0,0,0,0,0],[1,1,1,1,1,1]] or
     Size(H9)<>32*3^24 or Size(dH9)<>3^24 then
    Error("157dq: actual H9 abelian matrix/order drift");
  fi;
  piCoords:=List(q3.groups.PB4.marked_generators,r->r.coords);;
  piMatrix:=List(piCoords,r->r{[1..6]});; dPi:=DerivedSubgroup(pc4.group);;
  if piMatrix<>IdentityMat(6) or Size(dPi)<>3^4 or Size(pc4.group)<>3^10 then
    Error("157dq: Pi4 Frattini marking drift");
  fi;
  residues:=Filtered(Tuples([0..5],6),v->
    ForAll(v,x->x mod 3=0) and Length(Set(List(v,x->(x/3) mod 2)))=1);;
  basis:=[];;
  for i in [1..5] do
    v:=[0,0,0,0,0,0];; v[i]:=6;; Add(basis,v);;
  od;
  Add(basis,[3,3,3,3,3,3]);; sums:=List(basis,Sum);;
  if residues<>[[0,0,0,0,0,0],[3,3,3,3,3,3]] or
     AbsInt(DeterminantMat(basis))<>23328 or Gcd(sums)<>6 then
    Error("157dq: integral congruence lattice drift");
  fi;
  edgePairs:=D972A5LPairList(4);;
  vertexPerms:=[[2,1,3,4],[1,3,2,4],[1,2,4,3]];; edgePerms:=[];;
  for v in vertexPerms do
    Add(edgePerms,List(edgePairs,p->Position(edgePairs,SortedList([v[p[1]],v[p[2]]]))));
  od;
  ep:=List(edgePerms,PermList);; edgeGroup:=Group(ep);;
  if Size(edgeGroup)<>24 or not ForAll(edgePerms,p->Set(p)=[1..6]) or
     ep[1]*ep[2]*ep[1]<>ep[2]*ep[1]*ep[2] or
     ep[2]*ep[3]*ep[2]<>ep[3]*ep[2]*ep[3] or ep[1]*ep[3]<>ep[3]*ep[1] then
    Error("157dq: natural B4 edge action drift");
  fi;
  artinWords:=List(fc.b4_action.generators,g->g.source_generator_images);;
  if artinWords<>[
      [[1],[-1,4,1],[-1,5,1],[2],[3],[6]],
      [[-4,2,4],[1],[3],[4],[-4,6,4],[5]],
      [[1],[-6,3,6],[2],[-6,5,6],[4],[6]]] then
    Error("157dq: frozen natural Artin action words drift");
  fi;
  inverseArtin:=[
    [[1],[4],[5],[1,2,-1],[1,3,-1],[6]],
    [[2],[4,1,-4],[3],[4],[6],[4,5,-4]],
    [[1],[3],[6,2,-6],[5],[6,4,-6],[6]]];;
  q4marks:=List(q3.coarse_models.Q4.marked_permutations,D972A5LPermFromRow);;
  relations:=q3.formulas.presentations.PB4.relations;; targetOK:=true;;
  for i in [1..3] do
    if ForAny(relations,r->not (IsOne(D972A5LEval(D972A5LSub(r,artinWords[i]),q4marks)) and
          IsOne(D972A5LEval(D972A5LSub(r,artinWords[i]),pc4.marks)))) or
       ForAny(relations,r->not (IsOne(D972A5LEval(D972A5LSub(r,inverseArtin[i]),q4marks)) and
          IsOne(D972A5LEval(D972A5LSub(r,inverseArtin[i]),pc4.marks)))) or
       ForAny([1..6],j->not (IsOne(D972A5LEval(D972A5LReduce(Concatenation(
          D972A5LSub(artinWords[i][j],inverseArtin[i]),[-j])),q4marks)) and
          IsOne(D972A5LEval(D972A5LReduce(Concatenation(
          D972A5LSub(artinWords[i][j],inverseArtin[i]),[-j])),pc4.marks)))) or
       ForAny([1..6],j->not (IsOne(D972A5LEval(D972A5LReduce(Concatenation(
          D972A5LSub(inverseArtin[i][j],artinWords[i]),[-j])),q4marks)) and
          IsOne(D972A5LEval(D972A5LReduce(Concatenation(
          D972A5LSub(inverseArtin[i][j],artinWords[i]),[-j])),pc4.marks)))) then
      targetOK:=false;;
    fi;
  od;
  actionMatrices:=List(artinWords,w->D972TLExponentMatrix(w,6));;
  if not targetOK or ForAny([1..3],i->ForAny([1..6],j->
      actionMatrices[i][j][edgePerms[i][j]]<>1 or Sum(actionMatrices[i][j])<>1)) then
    Error("157dq: H-normal E4 Artin replay drift");
  fi;
  receiptRows:=List(blocks,r->List(r,x->D972A5LPermRow(x,27)));;
  return rec(tuple_order:=["x12","x13","x14","x23","x24","x34"],
    H9:=rec(deletion_maps:=dels,reconstructed_marked_blocks:=receiptRows,
      binary_matrix_row_order:=["d1_x","d1_y","d2_x","d2_y","d3_x","d3_y","d4_x","d4_y"],
      binary_matrix:=matrix,rank_F2:=5,kernel_F2:=kernel,image_order:=32,
      G9_order:=2916,G9_derived_order:=729,H9_order_decimal:=String(Size(H9)),
      H9_derived_order_decimal:=String(Size(dH9)),H9_abelianization_order:=32,
      actual_marked_reconstruction:=true,derived_calls:=2),
    Pi4:=rec(marked_coordinates:=piCoords,frattini_matrix:=piMatrix,
      rank_F3:=D972TLRankMod(piMatrix,3),group_order:=Size(pc4.group),
      derived_order:=Size(dPi),abelianization_order:=3^6),
    integral_lattice:=rec(congruence:="v=3w and w mod2 is 0 or (1,1,1,1,1,1)",
      residue_box_modulus:=6,residue_box_size:=6^6,residue_solutions:=residues,
      canonical_basis_rows:=basis,determinant:=AbsInt(DeterminantMat(basis)),index:=23328,
      basis_linking_sums:=sums,gcd_total_linking:=Gcd(sums),ell_H:="6Z",
      exact_sequence:="im(H -> PB4_ab)=ker(PB4_ab -> E4_ab)",
      no_claim_A12_power_itself_in_H:=true),
    beta:=rec(definition:="beta(h)=ell(h)/6 mod3",onto:=true,image_order:=3,
      kernel:="Kbeta=H intersection ker(ell mod18)",Phi3_H_subset_Kbeta:=true),
    B4_action:=rec(vertex_adjacent_transpositions:=vertexPerms,
      edge_permutations:=edgePerms,action_group_order:=24,total_linking_preserved:=true,
      induced_braid_relations:=true,artin_source_words:=artinWords,
      inverse_artin_source_words:=inverseArtin,artin_abelian_matrices:=actionMatrices,
      E4_relation_and_two_sided_replay:=targetOK,beta_preserved:=true,
      H_normal_frozen_typing:=true,Kbeta_normal_B4:=true,
      chief_factor_order:=3,chief_by_prime_order:=true));
end;;

D972TLPB4Record := function(name,word,q4marks,pc4)
  local w,qv,pv,ell;
  w:=D972A5LReduce(word);; qv:=D972A5LEval(w,q4marks);;
  pv:=D972A5LEval(w,pc4.marks);; ell:=Sum(w,SignInt);;
  return rec(name:=name,word:=w,word_sha256:=D972A5LDigest(w),
    q4_row:=D972A5LPermRow(qv,144),pi4_coords:=List(Exponents(pv),Int),
    total_linking:=ell,c18_residue:=ell mod 18,q4_identity:=IsOne(qv),
    pi4_identity:=IsOne(pv),pass:=IsOne(qv) and IsOne(pv) and ell=0);
end;;

D972TLPB3Record := function(name,word,cofaces,q4marks,pc4)
  local w,lifts,i;
  w:=D972A5LReduce(word);; lifts:=[];;
  for i in [1..5] do
    Add(lifts,D972TLPB4Record(Concatenation(name,".coface",String(i)),
      D972A5LSub(w,cofaces[i]),q4marks,pc4));
  od;
  return rec(name:=name,pb3_word:=w,pb3_word_sha256:=D972A5LDigest(w),
    five_coface_lifts:=lifts,pass:=ForAll(lifts,r->r.pass));
end;;

D972TLE3Record := function(name,word,q0x,q0y,pc3,cofaces,q4marks,pc4)
  local w,qv,pv;
  w:=D972A5LReduce(word);; qv:=D972A5LEval(w,[q0x,q0y]);;
  pv:=D972A5LEval(w,[pc3.marks[1],pc3.marks[3]]);;
  return rec(name:=name,word:=w,word_sha256:=D972A5LDigest(w),
    exponent_sums:=D972TLExponentSums(w,2),q0_row:=D972A5LPermRow(qv,36),
    pi3_coords:=List(Exponents(pv),Int),E3_identity:=IsOne(qv) and IsOne(pv),
    finer_five_cofaces:=D972TLPB3Record(Concatenation(name,".finer"),w,
      cofaces,q4marks,pc4));
end;;

D972TLAllWordsPass := function(words,q4marks,pc4)
  return ForAll(words,w->D972TLPB4Record("canary",w,q4marks,pc4).pass);
end;;

D972TLFindInverse := function(q3,S,relations,q4marks,pc4)
  local row,corr,i,w,T,srels,st,ts,attempts,chosen;
  row:=First(q3.canonical_roof_powers.rows,r->r.exponent=7);;
  if row=fail then Error("157dq: missing normalized exponent-seven row"); fi;
  corr:=q3.correction_fibre.records;; attempts:=0;; chosen:=fail;;
  for i in [1..Length(corr)] do
    attempts:=attempts+1;; w:=D972A5LReduce(Concatenation(row.word,corr[i].word));;
    T:=D972TLSourceWords(w);;
    srels:=List(relations,r->D972A5LSub(r,T));;
    st:=List([1..6],j->D972A5LReduce(Concatenation(D972A5LSub(T[j],S),[-j])));;
    ts:=List([1..6],j->D972A5LReduce(Concatenation(D972A5LSub(S[j],T),[-j])));;
    # Availability means exactly that T supplies preimages S(T_i)=x_i.
    # T-relations and T(S_i)=x_i are recorded below but do not select T.
    if D972TLAllWordsPass(st,q4marks,pc4) then
      chosen:=rec(normalized_exponent:=7,roof_row_index:=row.row_index,
        correction_index:=i,word:=w,source_words:=T,relation_words:=srels,
        ST_words:=st,TS_words:=ts);; break;
    fi;
  od;
  if chosen=fail then return rec(found:=false,attempted:=attempts,cap:=Length(corr)); fi;
  chosen.found:=true;; chosen.attempted:=attempts;; chosen.cap:=Length(corr);;
  chosen.word_sha256:=D972A5LDigest(chosen.word);;
  chosen.word_length:=Length(chosen.word);;
  return chosen;
end;;

# Restrict the six PB4 source images to the canonical PB3 edge order
# [x12,x13,x23].  The last generator is PB4 generator 4, so this is a
# typed reindexing rather than a word truncation.
D972TLSourceWords3 := function(source6)
  local keep,out,w;
  keep:=[1,2,4];; out:=[];;
  for w in source6{keep} do
    if ForAny(w,x->not (AbsInt(x) in keep)) then
      Error("157dq: PB3 source restriction uses a non-PB3 edge");
    fi;
    Add(out,List(w,x->SignInt(x)*Position(keep,AbsInt(x))));;
  od;
  return out;
end;;

D972TLPB3FiveComponentOnto := function(q3,S,T,q4marks,pc4)
  local cofaces,relations,S3,T3,components,tupleComponents,z,i,c,qg,pg,cg,
    qs,ps,cs,qt,pt,ct,srels,trels,st3,ts3,st,ts,sinter,tinter,
    allRecords,acceptanceRecords,diagnosticRecords,allAcceptance,allDiagnostic,
    componentRecovery,allPass;
  cofaces:=q3.formulas.cofaces_3_4;;
  relations:=q3.formulas.presentations.PB3.relations;;
  S3:=D972TLSourceWords3(S);; T3:=D972TLSourceWords3(T);;
  st3:=List([1..3],i->D972A5LReduce(Concatenation(D972A5LSub(T3[i],S3),[-i])));;
  ts3:=List([1..3],i->D972A5LReduce(Concatenation(D972A5LSub(S3[i],T3),[-i])));;
  components:=[];; tupleComponents:=[];; allRecords:=[];;
  z:=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18);;
  for i in [1..5] do
    c:=cofaces[i];;
    qg:=List(c,w->D972A5LEval(w,q4marks));;
    pg:=List(c,w->D972A5LEval(w,pc4.marks));;
    cg:=List(c,w->z^Sum(w,SignInt));;
    qs:=List(S3,w->D972A5LEval(D972A5LSub(w,c),q4marks));;
    ps:=List(S3,w->D972A5LEval(D972A5LSub(w,c),pc4.marks));;
    cs:=List(S3,w->z^Sum(D972A5LSub(w,c),SignInt));;
    qt:=List(T3,w->D972A5LEval(D972A5LSub(w,c),q4marks));;
    pt:=List(T3,w->D972A5LEval(D972A5LSub(w,c),pc4.marks));;
    ct:=List(T3,w->z^Sum(D972A5LSub(w,c),SignInt));;
    # Proposition 2.11 compatibility includes a parenthesization conjugator.
    # The strict g=1 comparison below is retained as a lossless diagnostic,
    # not as Definition 2.9's onto gate.  Actual joint-quotient descent/onto is
    # certified minimally by S-relations plus S(T_i)=x_i.  T-relations and
    # T(S_i)=x_i are retained as independent two-sided canaries.
    sinter:=List([1..3],j->D972TLPB4Record(
      Concatenation("PB3.component",String(i),".S.intertwining.",String(j)),
      D972A5LReduce(Concatenation(D972A5LSub(S3[j],c),
        D972A5LInv(D972A5LSub(c[j],S)))),q4marks,pc4));;
    tinter:=List([1..3],j->D972TLPB4Record(
      Concatenation("PB3.component",String(i),".T.intertwining.",String(j)),
      D972A5LReduce(Concatenation(D972A5LSub(T3[j],c),
        D972A5LInv(D972A5LSub(c[j],T)))),q4marks,pc4));;
    srels:=List([1..Length(relations)],j->D972TLPB4Record(
      Concatenation("PB3.component",String(i),".S.relation.",String(j)),
      D972A5LSub(D972A5LSub(relations[j],S3),c),q4marks,pc4));;
    trels:=List([1..Length(relations)],j->D972TLPB4Record(
      Concatenation("PB3.component",String(i),".T.relation.",String(j)),
      D972A5LSub(D972A5LSub(relations[j],T3),c),q4marks,pc4));;
    st:=List([1..3],j->D972TLPB4Record(
      Concatenation("PB3.component",String(i),".ST.generator.",String(j)),
      D972A5LSub(st3[j],c),q4marks,pc4));;
    ts:=List([1..3],j->D972TLPB4Record(
      Concatenation("PB3.component",String(i),".TS.generator.",String(j)),
      D972A5LSub(ts3[j],c),q4marks,pc4));;
    diagnosticRecords:=Concatenation(sinter,tinter);;
    acceptanceRecords:=Concatenation(srels,st);;
    # Preserve the registered record/digest order while separating semantics.
    Append(allRecords,Concatenation(diagnosticRecords,srels,trels,st,ts));;
    allAcceptance:=ForAll(acceptanceRecords,r->r.pass);;
    allDiagnostic:=ForAll(diagnosticRecords,r->r.pass);;
    componentRecovery:=ForAll(st,r->r.pass);;
    Add(tupleComponents,qg);; Add(tupleComponents,pg);; Add(tupleComponents,cg);;
    Add(components,rec(coface_index:=i,coface_words:=c,
      original:=rec(q4_rows:=List(qg,x->D972A5LPermRow(x,144)),
        pi4_coords:=List(pg,x->List(Exponents(x),Int)),
        c18_residues:=List(c,w->Sum(w,SignInt) mod 18)),
      S_images:=rec(q4_rows:=List(qs,x->D972A5LPermRow(x,144)),
        pi4_coords:=List(ps,x->List(Exponents(x),Int)),
        c18_residues:=List(S3,w->Sum(D972A5LSub(w,c),SignInt) mod 18)),
      T_images:=rec(q4_rows:=List(qt,x->D972A5LPermRow(x,144)),
        pi4_coords:=List(pt,x->List(Exponents(x),Int)),
        c18_residues:=List(T3,w->Sum(D972A5LSub(w,c),SignInt) mod 18)),
      S_global_intertwining_residuals:=sinter,T_global_intertwining_residuals:=tinter,
      strict_intertwining_diagnostic_pass:=allDiagnostic,
      strict_intertwining_diagnostic_only:=true,
      S_relation_residuals:=srels,T_relation_residuals:=trels,
      ST_generator_residuals:=st,TS_generator_residuals:=ts,
      definition_2_9_S_relation_descent_pass:=ForAll(srels,r->r.pass),
      definition_2_9_S_of_T_generator_recovery:=ForAll(st,r->r.pass),
      T_relation_canary_pass:=ForAll(trels,r->r.pass),
      T_of_S_generator_canary_pass:=ForAll(ts,r->r.pass),
      T_canaries_diagnostic_only:=true,
      relation_descent_pass:=ForAll(srels,r->r.pass),
      joint_tuple_generator_recovery:=componentRecovery,
      pass:=allAcceptance));
  od;
  allPass:=ForAll(components,r->r.pass);;
  return rec(source_generator_order:=["x12","x13","x23"],
    S_source_words:=S3,T_source_words:=T3,components:=components,
    actual_joint_tuple_N_ord:=D972TLTupleOrder([[1],[3],[1,2,3]],tupleComponents),
    strict_global_intertwining_required_for_acceptance:=false,
    joint_coupling_handled_without_character_rank_assumption:=true,
    definition_2_9_onto_gate:="S relations plus S(T_i)=x_i joint-quotient generator recovery",
    definition_2_9_S_relation_descent:=ForAll(components,
      r->r.definition_2_9_S_relation_descent_pass),
    definition_2_9_S_of_T_generator_recovery:=ForAll(components,
      r->r.definition_2_9_S_of_T_generator_recovery),
    T_relation_and_T_of_S_canaries:=ForAll(components,
      r->r.T_relation_canary_pass and r.T_of_S_generator_canary_pass),
    T_canaries_required_for_acceptance:=false,
    joint_tuple_generator_recovery:=ForAll(components,r->r.joint_tuple_generator_recovery),
    strict_intertwining_not_Def2_9_gate:=true,
    strict_intertwining_parenthesization_conjugator_not_forced_identity:=true,
    strict_intertwining_diagnostic_pass:=ForAll(components,
      r->r.strict_intertwining_diagnostic_pass),
    component_intertwining_residuals:=5*2*3,residual_count:=Length(allRecords),
    all_pass:=allPass);
end;;

D972TLSourceResiduals := function(q3,candidate,base,q4marks,pc3,pc4)
  local cofaces,relations,S,S0,diffs,hex,pent,inverse,T,srels,trels,st,ts,
    chars,charsS,charsT,i,j,allRecords,tmat,settle,qimgs,pimgs,qinvok,pinvok,
    forward,inversePc,hf,hi,auth,pb3onto;
  cofaces:=q3.formulas.cofaces_3_4;; relations:=q3.formulas.presentations.PB4.relations;;
  if cofaces<>D972A5LCofaces(3) then Error("157dq: coface formula drift"); fi;
  S:=D972TLSourceWords(candidate);; S0:=D972TLSourceWords(base);;
  diffs:=List([1..6],i->D972TLPB4Record(Concatenation("FC30.source_difference.",String(i)),
    D972A5LReduce(Concatenation(S[i],D972A5LInv(S0[i]))),q4marks,pc4));;
  settle:=q3.selected_solution.settlement;;
  if settle.source_words<>S0 or settle.Q4_bijective<>true or
     settle.Pi4_q3_bijective<>true then Error("157dq: q3 settlement binding drift"); fi;
  qimgs:=List(S,w->D972A5LEval(w,q4marks));;
  pimgs:=List(S,w->D972A5LEval(w,pc4.marks));;
  qinvok:=ForAll([1..6],i->D972A5LEval(settle.Q4_inverse_words[i],qimgs)=q4marks[i]);;
  pinvok:=ForAll([1..6],i->D972A5LEval(settle.Pi4_inverse_words[i],pimgs)=pc4.marks[i]);;
  forward:=List(settle.Pi4_forward_pc_images,r->D972A5LCoordElt(pc4.gens,r));;
  inversePc:=List(settle.Pi4_inverse_pc_images,r->D972A5LCoordElt(pc4.gens,r));;
  hf:=GroupHomomorphismByImages(pc4.group,pc4.group,pc4.gens,forward);;
  hi:=GroupHomomorphismByImages(pc4.group,pc4.group,pc4.gens,inversePc);;
  if hf=fail or hi=fail then Error("157dq: authenticated Pi4 maps fail"); fi;
  if ForAny([1..Length(pc4.gens)],i->Image(hi,Image(hf,pc4.gens[i]))<>pc4.gens[i] or
      Image(hf,Image(hi,pc4.gens[i]))<>pc4.gens[i]) then
    Error("157dq: authenticated Pi4 inverse compositions drift");
  fi;
  auth:=rec(upstream_settlement_sha256:=D972A5LDigest(settle),
    q3_source_words_equal_base:=true,candidate_E4_images_equal_base:=ForAll(diffs,r->r.pass),
    Q4_bijective_authenticated:=settle.Q4_bijective,
    Pi4_bijective_authenticated:=settle.Pi4_q3_bijective,
    Q4_inverse_words:=settle.Q4_inverse_words,Pi4_inverse_words:=settle.Pi4_inverse_words,
    Q4_inverse_word_replay:=qinvok,Pi4_inverse_word_replay:=pinvok,
    Pi4_forward_inverse_sha256:=D972A5LDigest(
      [settle.Pi4_forward_pc_images,settle.Pi4_inverse_pc_images]),
    Pi4_pc_two_sided_replay:=true,upstream_same_job_checker_required:=true,
    pass:=ForAll(diffs,r->r.pass) and qinvok and pinvok);;
  hex:=List([1..2],i->D972TLPB3Record(Concatenation("hexagon.",String(i)),
    D972TLHexagonWords(candidate)[i],cofaces,q4marks,pc4));;
  pent:=D972TLPB4Record("A18.ordered_pentagon",D972TLPentagonWord(candidate),q4marks,pc4);;
  srels:=List([1..Length(relations)],i->D972TLPB4Record(
    Concatenation("S.relation.",String(i)),D972A5LSub(relations[i],S),q4marks,pc4));;
  inverse:=D972TLFindInverse(q3,S,relations,q4marks,pc4);;
  if inverse.found then
    T:=inverse.source_words;;
    trels:=List([1..Length(relations)],i->D972TLPB4Record(
      Concatenation("T.relation.",String(i)),inverse.relation_words[i],q4marks,pc4));;
    st:=List([1..6],i->D972TLPB4Record(Concatenation("ST.generator.",String(i)),
      inverse.ST_words[i],q4marks,pc4));;
    ts:=List([1..6],i->D972TLPB4Record(Concatenation("TS.generator.",String(i)),
      inverse.TS_words[i],q4marks,pc4));;
  else T:=[];; trels:=[];; st:=[];; ts:=[];; fi;
  if inverse.found then
    pb3onto:=D972TLPB3FiveComponentOnto(q3,S,T,q4marks,pc4);;
  else
    pb3onto:=rec(source_generator_order:=["x12","x13","x23"],
      S_source_words:=[],T_source_words:=[],components:=[],
      actual_joint_tuple_N_ord:=fail,
      strict_global_intertwining_required_for_acceptance:=false,
      joint_coupling_handled_without_character_rank_assumption:=false,
      definition_2_9_onto_gate:="S relations plus S(T_i)=x_i joint-quotient generator recovery",
      definition_2_9_S_relation_descent:=false,
      definition_2_9_S_of_T_generator_recovery:=false,
      T_relation_and_T_of_S_canaries:=false,
      T_canaries_required_for_acceptance:=false,
      joint_tuple_generator_recovery:=false,strict_intertwining_not_Def2_9_gate:=true,
      strict_intertwining_parenthesization_conjugator_not_forced_identity:=true,
      strict_intertwining_diagnostic_pass:=false,
      component_intertwining_residuals:=0,residual_count:=0,all_pass:=false);;
  fi;
  chars:=List(cofaces,m->List(m,w->Sum(w,SignInt)));;
  if chars<>[[1,1,1],[2,2,1],[2,1,2],[1,2,2],[1,1,1]] then
    Error("157dq: five total-linking character rows drift");
  fi;
  charsS:=List(cofaces,m->List(m,w->Sum(D972A5LSub(w,S),SignInt)));;
  if inverse.found then charsT:=List(cofaces,m->List(m,w->Sum(D972A5LSub(w,T),SignInt)));;
  else charsT:=[];; fi;
  allRecords:=Concatenation(diffs,srels,trels,st,ts,[pent]);;
  for i in [1..2] do Append(allRecords,hex[i].five_coface_lifts);; od;
  if inverse.found then tmat:=D972TLExponentMatrix(T,6);; else tmat:=[];; fi;
  return rec(S_source_words:=S,S_exponent_matrix:=D972TLExponentMatrix(S,6),
    T_inverse_binding:=inverse,T_source_words:=T,
    T_exponent_matrix:=tmat,
    authenticated_E4_automorphism:=auth,
    PB3_five_component_onto:=pb3onto,
    source_difference_FC30:=diffs,hexagons:=hex,pentagon:=pent,
    S_relation_residuals:=srels,T_relation_residuals:=trels,
    ST_generator_residuals:=st,TS_generator_residuals:=ts,
    five_character_replay:=rec(original_integer_rows:=chars,
      rows_mod3:=List(chars,r->List(r,x->x mod 3)),
      formal_rank_mod3:=D972TLRankMod(List(chars,r->List(r,x->x mod 3)),3),
      F2_columns:=[1,3],F2_formal_rank_mod3:=D972TLRankMod(
        List(chars,r->[r[1] mod 3,r[3] mod 3]),3),
      rank_is_diagnostic_not_joint_image_theorem:=true,
      S_integer_rows:=charsS,T_integer_rows:=charsT,
      S_preserves_all_five:=(charsS=chars),T_preserves_all_five:=(charsT=chars)),
    inverse_certificate_availability_required:=true,
    inverse_absence_terminal_token:=D972TLUnknownInput,
    T_canaries_diagnostic_only:=true,T_canaries_required_for_acceptance:=false,
    T_relation_canary_pass:=inverse.found and ForAll(trels,r->r.pass),
    T_of_S_generator_canary_pass:=inverse.found and ForAll(ts,r->r.pass),
    T_character_canary_pass:=inverse.found and charsT=chars,
    T_exponent_canary_pass:=inverse.found and tmat=IdentityMat(6),
    residual_count:=Length(allRecords)+pb3onto.residual_count,
    residual_digest_sha256:=D972A5LDigest(rec(diffs:=diffs,hex:=hex,pent:=pent,
      S:=srels,T:=trels,ST:=st,TS:=ts,PB3:=pb3onto,
      T_character_rows:=charsT,T_exponent_matrix:=tmat)),
    all_pass:=auth.pass and inverse.found and pb3onto.all_pass and
      ForAll(Concatenation(diffs,srels,st,[pent]),r->r.pass) and
      ForAll(hex,r->r.pass) and charsS=chars and
      D972TLExponentMatrix(S,6)=IdentityMat(6));
end;;

D972TLTupleOrder := function(words,componentMarks)
  local out,w,values;
  out:=[];;
  for w in words do
    values:=List(componentMarks,m->D972A5LEval(w,m));;
    Add(out,Lcm(List(values,Order)));
  od;
  return Lcm(out);
end;;

D972TLKbetaComponents := function(cofaces,q4marks,pc4)
  local out,c,z;
  out:=[];; z:=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18);;
  for c in cofaces do
    Add(out,List(c,w->D972A5LEval(w,q4marks)));;
    Add(out,List(c,w->D972A5LEval(w,pc4.marks)));;
    Add(out,List(c,w->z^Sum(w,SignInt)));;
  od;
  return out;
end;;

D972TLOrders := function(q3,d1,q0marks,pc3,q4marks,pc4)
  local words,hcom,kcom,lcom,lpcom,oneQ0,cofaces,vals;
  words:=[[1],[3],[1,2,3]];; oneQ0:=One(Group(q0marks));;
  hcom:=[[q0marks[1],oneQ0,q0marks[2]],pc3.marks];;
  cofaces:=q3.formulas.cofaces_3_4;; kcom:=D972TLKbetaComponents(cofaces,q4marks,pc4);;
  lcom:=Concatenation(hcom,[d1.fullMarks]);; lpcom:=Concatenation(kcom,[d1.fullMarks]);;
  vals:=[D972TLTupleOrder(words,hcom),D972TLTupleOrder(words,kcom),
    D972TLTupleOrder(words,lcom),D972TLTupleOrder(words,lpcom)];;
  return rec(definition_3_1_words:=rec(x:=[1],y:=[3],c:=[1,2,3]),
    H_ord:=vals[1],Kbeta_ord:=vals[2],L_ord:=vals[3],Lprime_ord:=vals[4],
    gcd_L_Kbeta:=Gcd(vals[3],vals[2]),expected:=[18,18,90,90],
    friendly:=rec(marking_m:=0,lambda:=1,
      gcd_lambda_with_orders:=List(vals,n->Gcd(1,n)),all_friendly:=true),
    FC29_pass:=vals=[18,18,90,90] and Gcd(vals[3],vals[2])=18,
    component_counts:=rec(H:=Length(hcom),Kbeta:=Length(kcom),L:=Length(lcom),
      Lprime:=Length(lpcom)));
end;;

D972TLA5Gate := function(fc,d1,candidate)
  local value,derived,hexValues,hexResiduals,pentValues,pentResidual,onto,
    supports,r,valueTuple,A5,i,normalOrders,factorRows,factorGroup;
  value:=D972A5LEval(candidate,[d1.compactMarks[1],d1.compactMarks[3]]);;
  derived:=DerivedSubgroup(d1.compact);;
  hexValues:=D972A5LContext(candidate,D972A5LHexPairs(d1.fullMarks[1],d1.fullMarks[3]));;
  hexResiduals:=D972A5LHexFromValues(hexValues,0,d1.fullMarks[1],d1.fullMarks[3]);;
  pentValues:=D972A5LContext(candidate,D972A5LPairs(d1.pb4marks));;
  pentResidual:=D972A5LPentFromValues(pentValues);;
  onto:=Size(Group(d1.compactMarks[1],D972A5LPP(
    [value^-1,d1.compactMarks[3],value])))=1500;;
  supports:=[];; normalOrders:=[];; A5:=d1.A5;;
  for r in fc.rhoA.single_support_witnesses do
    valueTuple:=List([1..4],i->D972TLRestrict(
      D972A5LEval(r.source_word,d1.pb4marks),5*(i-1),5));;
    if List(valueTuple,x->D972A5LPermRow(x,5))<>r.images then
      Error("157dq: FC8 support image replay drift");
    fi;
    Add(normalOrders,Size(NormalClosure(A5,Group(valueTuple[r.coordinate]))));;
    Add(supports,rec(coordinate:=r.coordinate,source_word:=r.source_word,
      images:=r.images,other_coordinates_identity:=ForAll([1..4],i->
        i=r.coordinate or IsOne(valueTuple[i])),target_nontrivial:=not IsOne(valueTuple[r.coordinate]),
      normal_closure_order:=normalOrders[Length(normalOrders)]));
  od;
  factorRows:=List(fc.b4_action.generators,g->g.factor_permutation);;
  factorGroup:=Group(List(factorRows,PermList));;
  if factorRows<>[[2,1,3,4],[1,3,2,4],[1,2,4,3]] or
     Size(factorGroup)<>24 or not IsTransitive(factorGroup,[1..4]) then
    Error("157dq: FC8 B4 factor action drift");
  fi;
  return rec(marking_m:=0,lambda:=1,candidate_compact_row:=D972A5LPermRow(value,15),
    compact_DF_order:=Size(d1.compact),compact_derived_order:=Size(derived),
    charming_derived_membership:=value in derived,
    hexagon_rows:=List(hexResiduals,x->D972A5LPermRow(x,100)),
    pentagon_row:=D972A5LPermRow(pentResidual,20),hexagon_exact:=ForAll(hexResiduals,IsOne),
    pentagon_exact:=IsOne(pentResidual),onto_DF:=onto,
    A5:=rec(order:=Size(A5),simple:=IsSimpleGroup(A5),perfect:=IsPerfectGroup(A5),
      no_C3_quotient:=IsPerfectGroup(A5)),single_support_witnesses:=supports,
    single_support_normal_orders:=normalOrders,A5four_full_product:=normalOrders=[60,60,60,60],
    factor_permutations:=factorRows,factor_action_group_order:=24,
    factor_action_transitive:=true,
    no_common_quotient_A5four_C3:=IsPerfectGroup(A5),
    goursat_L_Kbeta_equals_H:=IsPerfectGroup(A5) and normalOrders=[60,60,60,60],
    index_L_Lprime:=3,
    pass:=(value in derived) and ForAll(hexResiduals,IsOne) and IsOne(pentResidual) and onto and
      normalOrders=[60,60,60,60] and IsPerfectGroup(A5) and
      Size(factorGroup)=24 and IsTransitive(factorGroup,[1..4]));
end;;

D972TLMain := function(output)
  local start,pins,q3,fc,dp,words,pc3,pc4,q0marks,q4marks,lattice,base,records,
    gens,corr,candidate,difference,cofaces,correction,source,a5,d1,orders,outside,
    allPass,terminal,receipt,chain,idx;
  start:=Runtime();;
  pins:=rec(q3_artifact:=D972TLRequireSHA(D972TLQ3Path,D972TLQ3SHA,"q3 artifact"),
    fc8_artifact:=D972TLRequireSHA(D972TLFC8Path,D972TLFC8SHA,"FC8 artifact"),
    selected_lift_artifact:=D972TLRequireSHA(D972TLDPPath,D972TLDPSHA,"157dp artifact"),
    selected_lift_producer:=D972TLRequireSHA(D972TLOldProducer,D972TLOldProducerSHA,"157dp producer"),
    selected_lift_checker:=D972TLRequireSHA(D972TLOldChecker,D972TLOldCheckerSHA,"157dp checker"),
    selected_lift_driver:=D972TLRequireSHA(D972TLOldDriver,D972TLOldDriverSHA,"157dp driver"),
    frozen_words:=D972TLRequireSHA(D972TLWordsPath,D972TLWordsSHA,"frozen words"),
    outside_classifier:=D972TLRequireSHA(D972TLAxisPath,D972TLAxisSHA,"outside theorem"),
    T48_1:=D972TLRequireSHA(D972TLT48Path,D972TLT48SHA,"T48-1 theorem"));;
  q3:=D972TLRead(D972TLQ3Path,D972TLQ3SHA,"q3");;
  fc:=D972TLRead(D972TLFC8Path,D972TLFC8SHA,"FC8");;
  dp:=D972TLRead(D972TLDPPath,D972TLDPSHA,"157dp");;
  words:=D972TLRead(D972TLWordsPath,D972TLWordsSHA,"words");;
  pins.q3_sources:=q3.pins;; pins.fc8_sources:=fc.pins;;
  pins.selected_lift_sources:=dp.pins;;
  if q3.terminal_token<>"B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" or
     fc.terminal_token<>"FC8_A5_FOUR_CHIEF_CROSSCHECKED" or
     dp.terminal_token<>"B34_A5_LAYER_FIXED_OUTSIDE_ROOF_LIFT_CROSSCHECKED" then
    Error("157dq: upstream terminal drift");
  fi;
  pc3:=D972A5LImportPC(q3.groups.PB3,"Pi3");;
  pc4:=D972A5LImportPC(q3.groups.PB4,"Pi4");;
  q0marks:=List(q3.coarse_models.Q0.marked_permutations,D972A5LPermFromRow);;
  q4marks:=List(q3.coarse_models.Q4.marked_permutations,D972A5LPermFromRow);;
  lattice:=D972TLH9Lattice(q3,pc4,fc);;
  base:=q3.selected_solution.typed_source_word;; records:=dp.source_fibre.section_records;;
  gens:=dp.source_fibre.tracked_normal_generators;;
  corr:=D972A5LExpandSection(124,records,gens);;
  chain:=[];; idx:=124;;
  while idx<>1 do Add(chain,idx);; idx:=records[idx].parent;; od;; Add(chain,1);;
  candidate:=D972A5LReduce(Concatenation(base,corr));;
  if dp.scan.selected.outer_index<>1 or dp.scan.selected.m_shift_index<>0 or
     dp.scan.selected.correction_index<>124 or dp.scan.selected.typed_source_word<>candidate or
     dp.scan.selected.a5_correction_word<>corr or chain<>[124,45,16,5,1] or
     Length(candidate)<>92 or D972A5LDigest(candidate)<>
       "c113c06d51480c8c819a563f6efc2323afecb7a54aabee96e7104d1d2921505b" or
     D972TLExponentSums(candidate,2)<>[0,0] then
    Error("157dq: selected candidate reconstruction drift");
  fi;
  difference:=D972A5LReduce(Concatenation(candidate,D972A5LInv(base)));;
  cofaces:=q3.formulas.cofaces_3_4;;
  correction:=rec(expanded_section_word:=corr,expanded_section_word_sha256:=D972A5LDigest(corr),
    section_chain:=chain,difference_candidate_times_base_inverse:=
      D972TLE3Record("candidate_base_difference",difference,q0marks[1],q0marks[2],
        pc3,cofaces,q4marks,pc4),
    correction_word_direct:=D972TLE3Record("registered_A5_correction",corr,
      q0marks[1],q0marks[2],pc3,cofaces,q4marks,pc4));;
  source:=D972TLSourceResiduals(q3,candidate,base,q4marks,pc3,pc4);;
  d1:=D972A5LD1(fc);; a5:=D972TLA5Gate(fc,d1,candidate);;
  orders:=D972TLOrders(q3,d1,q0marks,pc3,q4marks,pc4);;
  outside:=D972A5LOutsideCertificate(q3,words);;
  allPass:=correction.difference_candidate_times_base_inverse.E3_identity and
    correction.difference_candidate_times_base_inverse.finer_five_cofaces.pass and
    correction.correction_word_direct.E3_identity and
    correction.correction_word_direct.finer_five_cofaces.pass and source.all_pass and
    source.PB3_five_component_onto.actual_joint_tuple_N_ord=orders.Kbeta_ord and
    a5.pass and orders.FC29_pass and outside.outside_A and lattice.beta.onto and
    lattice.B4_action.chief_by_prime_order;;
  if not source.T_inverse_binding.found then terminal:=D972TLUnknownInput;;
  elif allPass then terminal:=D972TLPass;; else terminal:=D972TLReject;; fi;
  receipt:=rec(schema:=D972TLSchema,status:=terminal,terminal_token:=terminal,
    terminal:=true,pins:=pins,marked_abelian_lattice:=lattice,
    candidate_binding:=rec(outer_index:=1,m_shift_index:=0,correction_index:=124,
      base_word:=base,base_word_length:=Length(base),base_word_sha256:=D972A5LDigest(base),
      correction:=correction,candidate_word:=candidate,candidate_word_length:=Length(candidate),
      candidate_word_sha256:=D972A5LDigest(candidate),free_exponent_sums:=[0,0],
      registered_receipt_word_equal:=true),literal_residuals:=source,
    a5_intersection:=a5,order_certificate:=orders,outside_certificate:=outside,
    claim_boundary:=rec(pass_implication:=
      "one outside GT^heart(L') pair exists; accepted T48-1 moves the known window from L to the strict index-three subgroup L'",
      H_definition:="ker(PB4 -> E4)",L_definition:="H intersection ker(rhoA)",
      Kbeta_definition:="H intersection ker(total-linking mod18)",
      Lprime_definition:="L intersection Kbeta",strict_index:=3,
      one_chief_descent_only:=true,L_or_Lprime_isolated_claimed:=false,
      global_B4_B_claimed:=false,cofinal_iteration_claimed:=false,compactness_claimed:=false,
      settlement_diagnostic_only:=true,candidate_rejection_not_B4_A:=true),
    performance:=rec(candidate_universe_scans:=0,registered_candidates_replayed:=1,
      inverse_certificate_fibre_cap:=27,inverse_certificate_attempts:=source.T_inverse_binding.attempted,
      H9_binary_kernel_vectors:=2^6,integral_lattice_residue_vectors:=6^6,
      Artin_target_relation_evaluations:=3*2*Length(q3.formulas.presentations.PB4.relations),
      Artin_two_sided_generator_evaluations:=3*2*6,FC8_single_support_replays:=4,
      PB3_five_component_intertwining_residuals:=
        source.PB3_five_component_onto.component_intertwining_residuals,
      compact_DF_enumeration_cap:=1500,
      H_or_E4_elements_enumerated:=0,A5four_elements_enumerated:=0,PB5_constructions:=0,
      ANUPQ_calls:=0,translation_BFS_calls:=0,sparse_gaussian_searches:=0,
      H9_DerivedSubgroup_calls:=1,G9_DerivedSubgroup_calls:=1,Pi4_DerivedSubgroup_calls:=1,
      literal_residual_count:=source.residual_count),
    provenance:=rec(producer:=D972TLProducer,
      checker:="search/check_d972_b34_total_linking_c3_chief_v1.py",
      upstream_crosschecked_run:=32171982444),runtime_ms:=Runtime()-start);;
  D972A5LCheckedWrite(output,receipt);;
  Print(terminal," output=",output," residuals=",source.residual_count,
    " inverse_attempts=",source.T_inverse_binding.attempted," runtime_ms=",Runtime()-start,"\n");
end;;

D972TLSelfTest := function()
  local path,obj,basis,i,v;
  basis:=[];;
  for i in [1..5] do v:=[0,0,0,0,0,0];; v[i]:=6;; Add(basis,v);; od;
  Add(basis,[3,3,3,3,3,3]);;
  if D972TLRankMod(IdentityMat(6),3)<>6 or AbsInt(DeterminantMat(basis))<>23328 or
     D972TLHexagonWords([1,2,-1,-2])=fail then Error("157dq: producer selftest"); fi;
  path:=Filename(DirectoryTemporary(),"d972_total_linking_io.json");;
  obj:=rec(schema:="io-selftest",empty:=[],index:=23328);;
  D972A5LCheckedWrite(path,obj);; D972TLIOMarkerCount:=D972TLIOMarkerCount+1;;
  Print(D972TLIOMarker,"\n");
end;;

if IsBound(D972_B34_TOTAL_LINKING_C3_SELFTEST) and
   D972_B34_TOTAL_LINKING_C3_SELFTEST=true then
  if IsBound(D972_B34_TOTAL_LINKING_C3_RUN) and D972_B34_TOTAL_LINKING_C3_RUN=true then
    Error("157dq: SELFTEST/RUN exclusive");
  fi;
  D972TLSelfTest();;
elif IsBound(D972_B34_TOTAL_LINKING_C3_RUN) and D972_B34_TOTAL_LINKING_C3_RUN=true then
  if not IsBound(D972_B34_TOTAL_LINKING_C3_OUTPUT) then
    D972_B34_TOTAL_LINKING_C3_OUTPUT:="ci/out/d972_b34_total_linking_c3_chief_v1.json";;
  fi;
  D972TLMain(D972_B34_TOTAL_LINKING_C3_OUTPUT);;
else
  Error("157dq: select exactly one mode");
fi;
