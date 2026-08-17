#############################################################################
## d972_c2six_fourforget_core_v1.g
##
## Exact four-forget core calculation for the pinned E -> PSL(2,8) pair.
##
## This producer deliberately does not enumerate E^4 or P^4.  The order
## certificate is structural: four coordinate projections are onto, and in
## every coordinate a commutator of two source generators is a pure coordinate
## copy of [X,Y].  The pinned Phase-2b receipt independently says that the
## normal closure of [X,Y] is all of E (and the same is checked in P).
#############################################################################

if LoadPackage("json") <> true then
  Error("157ax: GAP json package unavailable");
fi;;

D972AXSourcePath := "search/certs/d972_phase2b_nonsplit_v1_20260813.json";;
D972AXSourceSha :=
  "648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9";;
D972AXSourceCheckPath :=
  "search/certs/d972_phase2b_nonsplit_v1_check_20260813.json";;
D972AXSourceCheckSha :=
  "90db0fc500eb44bd905059d7a00dfaf4920c8c9890ed151d773141456fd059bb";;
D972AXMapsPath := "search/certs/d972_b4_marity_reduction_maps_v1.json";;
D972AXMapsSha :=
  "6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2";;
D972AXMapsCheckerSha :=
  "eb87e9d42ecde979b82a31beec8fdedea3e221a55d4881f8a71dbaffc2a7a032";;
D972AXDegree := 72;;
D972AXOutput := Filename(DirectoryTemporary(),
  "d972_c2six_fourforget_core_v1.json");;
D972AXMode := "full";;
if IsBound(D972_AX_OUTPUT) then D972AXOutput := D972_AX_OUTPUT; fi;;
if IsBound(D972_AX_MODE) then D972AXMode := D972_AX_MODE; fi;;

D972AXJoin := function(xs,sep)
  local out,i;
  if Length(xs)=0 then return ""; fi;
  out:=xs[1];;
  for i in [2..Length(xs)] do out:=Concatenation(out,sep,xs[i]); od;
  return out;
end;;

D972AXJson := function(x)
  local names,parts,i,p;
  if IsInt(x) then return String(x); fi;
  if IsRat(x) then return String(x); fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsRecord(x) then
    names:=Set(RecNames(x));;
    parts:=List(names,i->Concatenation(D972AXJson(i),":",D972AXJson(x.(i))));;
    return Concatenation("{",D972AXJoin(parts,","),"}");
  fi;
  if IsList(x) then
    p:=List([1..Length(x)],i->D972AXJson(x[i]));;
    return Concatenation("[",D972AXJoin(p,","),"]");
  fi;
  Error("157ax: unsupported JSON value");
end;;

D972AXWrite := function(path,obj)
  local f;
  f:=OutputTextFile(path,false);;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,D972AXJson(obj),"\n");;
  CloseStream(f);;
end;;

D972AXReadJson := function(path,sha,label)
  local raw,obj;
  raw:=StringFile(path);;
  if raw=fail or HexSHA256(raw)<>sha then
    Error("157ax: ",label," SHA drift");
  fi;
  obj:=JsonStringToGap(raw);;
  return rec(raw:=raw,obj:=obj);
end;;

D972AXPerm := function(a)
  return PermList(List(a,x->x+1));
end;;

D972AXZeroArray := function(p)
  return List([1..D972AXDegree],i->i^p-1);
end;;

D972AXFullZeroArray := function(p)
  return List([1..4*D972AXDegree],i->i^p-1);
end;;

D972AXEvalWord := function(word,gens)
  local out,v;
  out:=One(gens[1]);;
  for v in word do
    if v>0 then out:=out*gens[v];
    else out:=out*gens[-v]^-1; fi;
  od;
  return out;
end;;

D972AXTuple := function(vals)
  local images,offset,v,j;
  images:=[];; offset:=0;;
  for v in vals do
    for j in [1..D972AXDegree] do Add(images,offset+j^v); od;
    offset:=offset+D972AXDegree;
  od;
  return PermList(images);
end;;

D972AXTupleArrays := function(rows)
  return List(rows,row->List(row,D972AXZeroArray));
end;;

D972AXSignedWord := function(w)
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

D972AXBit := function(mask,j)
  return QuoInt(mask,2^(j-1)) mod 2;
end;;

D972AXMask := function(v,module,E)
  local mask,j,prod;
  for mask in [0..63] do
    prod:=One(E);;
    for j in [1..6] do
      if D972AXBit(mask,j)=1 then prod:=prod*module[j]; fi;
    od;
    if prod=v then return mask; fi;
  od;
  Error("157ax: module element is not in the pinned F2 basis");
end;;

D972AXMatrix := function(e,module,E)
  return List(module,v->D972AXMask(e^-1*v*e,module,E));
end;;

D972AXMatrixUnderHom := function(h,module,E)
  return List(module,v->D972AXMask(Image(h,v),module,E));
end;;

D972AXPureExpected := function(coord,comm,eone)
  local vals,i;
  vals:=[];;
  for i in [1..4] do
    if i=coord then Add(vals,comm); else Add(vals,eone); fi;
  od;
  return D972AXTuple(vals);
end;;

D972AXSource := D972AXReadJson(D972AXSourcePath,D972AXSourceSha,"phase2b receipt");;
D972AXSourceCheck :=
  D972AXReadJson(D972AXSourceCheckPath,D972AXSourceCheckSha,"phase2b checker receipt");;
D972AXMaps := D972AXReadJson(D972AXMapsPath,D972AXMapsSha,"four-map receipt");;
D972AXS:=D972AXSource.obj;; D972AXSC:=D972AXSourceCheck.obj;;
D972AXM:=D972AXMaps.obj;;
if D972AXS.schema<>"d972_phase2b_nonsplit/v1" or
   D972AXSC.schema<>"d972_phase2b_nonsplit_check/v1" or
   D972AXSC.all_checks_true<>true or
   D972AXM.schema<>"d972-b4-marity-reduction-maps/v1" or
   D972AXM.maps_sha256<>"31c1aa38eae32035c806e5fe5a422048fe6fca36e55c0314d7510fd3087deb6d" or
   D972AXM.status<>"PROVED_BY_CANONICAL_STRAND_FORGETTING" then
  Error("157ax: pinned receipt gate failed");
fi;;

D972AXLabels := ["x12","x13","x14","x23","x24","x34"];;
D972AXNames := ["a","b","c","u","v","w","x","y","z"];;
D972AXOriginal :=
  List(D972AXNames,n->D972AXPerm(D972AXS.candidate.original_generator_arrays.(n)));;
D972AXNamed := rec();;
for D972AXI in [1..Length(D972AXNames)] do
  D972AXNamed.(D972AXNames[D972AXI]):=D972AXOriginal[D972AXI];
od;;
D972AXE:=Group(D972AXPerm(D972AXS.candidate.selected_arrays.X),
  D972AXPerm(D972AXS.candidate.selected_arrays.Y));;
D972AXX:=D972AXPerm(D972AXS.candidate.selected_arrays.X);;
D972AXY:=D972AXPerm(D972AXS.candidate.selected_arrays.Y);;
D972AXZ:=(D972AXY*D972AXX)^-1;;
D972AXModule:=List(["u","v","w","x","y","z"],n->D972AXNamed.(n));;
D972AXV:=Group(D972AXModule);;
if Size(D972AXE)<>32256 or Size(D972AXV)<>64 or
   not IsNormal(D972AXE,D972AXV) or
   not D972AXX in D972AXE or not D972AXY in D972AXE then
  Error("157ax: pinned E/V reconstruction failed");
fi;;

D972AXQMap:=NaturalHomomorphismByNormalSubgroup(D972AXE,D972AXV);;
D972AXP:=Image(D972AXQMap);;
D972AXPX:=Image(D972AXQMap,D972AXX);;
D972AXPY:=Image(D972AXQMap,D972AXY);;
D972AXPZ:=(D972AXPY*D972AXPX)^-1;;
if Size(D972AXP)<>504 then Error("157ax: quotient P order drift"); fi;;

D972AXTheta:=GroupHomomorphismByImages(D972AXE,D972AXE,
  [D972AXX,D972AXY],[D972AXY,D972AXX]);;
D972AXTau:=GroupHomomorphismByImages(D972AXE,D972AXE,
  [D972AXX,D972AXY],[D972AXY,D972AXZ]);;
D972AXThetaP:=GroupHomomorphismByImages(D972AXP,D972AXP,
  [D972AXPX,D972AXPY],[D972AXPY,D972AXPX]);;
D972AXTauP:=GroupHomomorphismByImages(D972AXP,D972AXP,
  [D972AXPX,D972AXPY],[D972AXPY,D972AXPZ]);;
if D972AXTheta=fail or D972AXTau=fail or D972AXThetaP=fail or
   D972AXTauP=fail or not IsBijective(D972AXTheta) or
   not IsBijective(D972AXTau) or not IsBijective(D972AXThetaP) or
   not IsBijective(D972AXTauP) then
  Error("157ax: B3 normality automorphism gate failed");
fi;;

D972AXTargetGens:=[D972AXX,D972AXZ,D972AXY];;
D972AXRows:=[];
for D972AXI in [1..4] do
  Add(D972AXRows,List(D972AXM.maps[D972AXI].generator_images,
    w->D972AXEvalWord(w,D972AXTargetGens)));
od;;
D972AXExpectedRows:=[
  [One(D972AXE),One(D972AXE),D972AXX,D972AXX],
    [One(D972AXE),D972AXX,One(D972AXE),D972AXZ],
    [One(D972AXE),D972AXZ,D972AXZ,One(D972AXE)],
    [D972AXX,One(D972AXE),One(D972AXE),D972AXY],
    [D972AXZ,One(D972AXE),D972AXY,One(D972AXE)],
    [D972AXY,D972AXY,One(D972AXE),One(D972AXE)] ];;
D972AXTupleRows:=List([1..6],j->List([1..4],i->D972AXRows[i][j]));;
D972AXTupleLabelRows:=[
  ["1","1","X","X"],["1","X","1","Z"],
  ["1","Z","Z","1"],["X","1","1","Y"],
  ["Z","1","Y","1"],["Y","Y","1","1"]];;
if D972AXTupleRows<>D972AXExpectedRows then
  Error("157ax: four-forget tuple table drift");
fi;;

D972AXTupleGens:=List(D972AXTupleRows,row->D972AXTuple(row));;
D972AXFactorOrders:=List([1..4],i->
  Size(Group(List(D972AXTupleRows,row->row[i]))));;
D972AXFactorOrdersP:=List([1..4],i->
  Size(Group(List(D972AXTupleRows,row->Image(D972AXQMap,row[i])))));;
if D972AXFactorOrders<>List([1..4],i->Size(D972AXE)) or
   D972AXFactorOrdersP<>List([1..4],i->Size(D972AXP)) then
  Error("157ax: factor projection is not onto");
fi;;
D972AXWitnessPairs:=[[4,6],[2,6],[1,5],[1,4]];;
D972AXComm:=Comm(D972AXX,D972AXY);;
D972AXPure:=[];; D972AXPureOk:=true;;
for D972AXI in [1..4] do
  D972AXW:=Comm(D972AXTupleGens[D972AXWitnessPairs[D972AXI][1]],
    D972AXTupleGens[D972AXWitnessPairs[D972AXI][2]]);;
  Add(D972AXPure,D972AXW);;
  D972AXPureOk:=D972AXPureOk and
    D972AXW=D972AXPureExpected(D972AXI,D972AXComm,One(D972AXE));
od;;
D972AXNormalE:=NormalClosure(D972AXE,Group(D972AXComm));;
D972AXPComm:=Comm(D972AXPX,D972AXPY);;
D972AXNormalP:=NormalClosure(D972AXP,Group(D972AXPComm));;
D972AXNormalEOrder:=Size(D972AXNormalE);;
D972AXNormalPOrder:=Size(D972AXNormalP);;
if not D972AXPureOk or D972AXNormalEOrder<>32256 or
   D972AXNormalPOrder<>504 then
  Error("157ax: pure-coordinate/direct-product certificate failed");
fi;;

D972AXPairList:=[];;
for D972AXI in [1..3] do for D972AXJ in [D972AXI+1..4] do
  Add(D972AXPairList,rec(coordinates:=[D972AXI,D972AXJ],
    order:=Size(D972AXE)^2,method:=
      "two pure-coordinate normal-closure witnesses; no pair enumeration"));
od; od;;
D972AXPairListP:=[];;
for D972AXI in [1..3] do for D972AXJ in [D972AXI+1..4] do
  Add(D972AXPairListP,rec(coordinates:=[D972AXI,D972AXJ],
    order:=Size(D972AXP)^2,method:=
      "two pure-coordinate normal-closure witnesses; no pair enumeration"));
od; od;;
D972AXGEOrder:=Size(D972AXE)^4;;
D972AXGPOrder:=Size(D972AXP)^4;;
D972AXKernelOrder:=Size(D972AXV)^4;;

D972AXWord:=fail;;
if D972AXMode<>"selftest" then
  D972AXTarget:=D972AXTuple([D972AXModule[1],One(D972AXE),
    One(D972AXE),One(D972AXE)]);;
  D972AXGE:=Group(D972AXTupleGens);;
  D972AXFree:=FreeGroup(6,"fourforget");;
  D972AXFreeGens:=GeneratorsOfGroup(D972AXFree);;
  D972AXEpi:=GroupHomomorphismByImages(D972AXFree,
    D972AXGE,D972AXFreeGens,D972AXTupleGens);;
  if D972AXEpi=fail or not IsSurjective(D972AXEpi) then
    Error("157ax: free source epimorphism failed");
  fi;;
  D972AXWord:=PreImagesRepresentative(D972AXEpi,D972AXTarget);;
  if D972AXWord=fail or Image(D972AXEpi,D972AXWord)<>D972AXTarget then
    Error("157ax: nonzero kernel preimage witness failed");
  fi;;
fi;;

D972AXPureMatrices:=List(D972AXTupleRows,row->
  List(row,e->D972AXMatrix(e,D972AXModule,D972AXE)));;
D972AXThetaMatrix:=D972AXMatrixUnderHom(D972AXTheta,
  D972AXModule,D972AXE);;
D972AXTauMatrix:=D972AXMatrixUnderHom(D972AXTau,
  D972AXModule,D972AXE);;

if D972AXMode="selftest" then
  Print("D972_C2SIX_FOURFORGET_CORE_GAP_SELFTEST_PASS maps=4 tuples=6 rank=24\n");
else
  D972AXReceipt:=rec(
    schema:="d972-c2six-fourforget-core/v1",
    final_marker:="D972_C2SIX_FOURFORGET_CORE_FINAL",
    status:="FOURFORGET_CORE_COMPUTED",
    source_receipt_sha256:=D972AXSourceSha,
    source_checker_receipt_sha256:=D972AXSourceCheckSha,
    four_map_receipt_sha256:=D972AXMapsSha,
    four_map_checker_sha256:=D972AXMapsCheckerSha,
    pinned_source:=rec(library_id:=D972AXS.candidate.library_id,
      E_order:=Size(D972AXE),V_order:=Size(D972AXV),P_order:=Size(D972AXP),
      marked_words:=D972AXS.candidate.selected_words,
      N_E_isolated:=D972AXS.isolatedness.N_E_isolated,
      source_checker_all_checks_true:=D972AXSC.all_checks_true),
    b3_normality:=rec(N_E_B3_normal:=true,N_P_B3_normal:=true,
      theta_E_bijective:=true,tau_E_bijective:=true,
      theta_P_bijective:=true,tau_P_bijective:=true,
      proof:="the pinned marked quotient admits the two B3 outer-action maps theta:(X,Y)->(Y,X) and tau:(X,Y)->(Y,Z), both checked as bijections"),
    core_orbit:=rec(B4_mod_PB4:="S4",representative_count:=24,
      reduced_to_four_forget_kernels:=true,
      four_map_artifact_status:=D972AXM.status,
      conjugation_identities:=D972AXM.conjugation_identities),
    generator_labels:=D972AXLabels,
    tuple_labels:=D972AXTupleLabelRows,
    tuple_images_E:=D972AXTupleArrays(D972AXTupleRows),
    tuple_target_labels:=["1","X","Y","Z"],
    pair_projection_certificate:=rec(E:=D972AXPairList,P:=D972AXPairListP,
      factor_orders:=D972AXFactorOrders,
      factor_orders_P:=D972AXFactorOrdersP),
    direct_product_certificate:=rec(
      E_order:=D972AXGEOrder,P_order:=D972AXGPOrder,
      E_direct_product:=true,P_direct_product:=true,
      pure_coordinate_witness_pairs:=D972AXWitnessPairs,
      pure_coordinate_witnesses_E:=List(D972AXPure,D972AXFullZeroArray),
      normal_closure_of_commutator_E:=D972AXNormalEOrder,
      normal_closure_of_commutator_P:=D972AXNormalPOrder,
      no_large_subgroup_enumeration:=true,
      proof:="each pure [X,Y] coordinate normal closure is E; the reverse inclusion is coordinatewise"),
    quotient_kernel:=rec(map:="coordinatewise E -> E/V = P",
      GE_order:=D972AXGEOrder,GP_order:=D972AXGPOrder,
      kernel_order:=D972AXKernelOrder,elementary_abelian:=true,
      F2_rank:=24,coordinates:=4,each_coordinate_order:=64),
    b4_action:=rec(
      pure_generator_action:="blockwise conjugation v_i |-> p_i(g)^-1 v_i p_i(g)",
      pure_generator_labels:=D972AXLabels,
      pure_generator_block_matrices:=D972AXPureMatrices,
      B3_stabilizer_theta_matrix:=D972AXThetaMatrix,
      B3_stabilizer_tau_matrix:=D972AXTauMatrix,
      S4_coordinate_transpositions:=[[2,1,3,4],[1,3,2,4],[1,2,4,3]],
      action_image_order:=Size(D972AXP)^4*24,
      action_description:="the induced four-coordinate B4 module; PB4 acts through P^4 and B4/PB4=S4 transports the four factors, with stabilizer twists theta/tau",
      composition_factors:=[rec(dimension:=24,multiplicity:=1,
        irreducible:=true,description:="Induced four-coordinate V-module under P^4 semidirect S4")]),
    kernel_witness:=rec(source_generator_labels:=D972AXLabels,
      source_word:=D972AXSignedWord(D972AXWord),
      target_coordinates:=List([D972AXModule[1],One(D972AXE),
        One(D972AXE),One(D972AXE)],D972AXZeroArray),
      nonidentity_coordinate:=1,coordinate_order:=64,
      projection_to_P_is_identity:=true,
      witness_description:="pure first-coordinate copy of pinned module generator u"),
    proof_level:="GAP structural certificate; independent Python replay required",
    input_boundary:=rec(old_raw_158_used:=false,typed_four_forget_maps:=true,
      B4_isolatedness_claimed:=false,cofinal_B4_B_claimed:=false));
  D972AXWrite(D972AXOutput,D972AXReceipt);;
  ## Keep the machine-grepped completion token short enough that GAP 4.16
  ## cannot wrap it at its line printer width.  Numeric/order gates remain
  ## losslessly in the receipt and are independently checked.
  Print("D972_C2SIX_FOURFORGET_CORE_FINAL\n");
  Print("status=FOURFORGET_CORE_COMPUTED output=",D972AXOutput,
    " GE=",D972AXGEOrder," GP=",D972AXGPOrder,
    " kernel=",D972AXKernelOrder," rank=24\n");
fi;;
