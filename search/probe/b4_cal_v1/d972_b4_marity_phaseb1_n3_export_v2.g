#############################################################################
## Phase-B1 v2: typed C_M/N_PB3 harness.
## No PC quotient or 972 assertion is made here.  The five cofaces are built
## from canonical PB3=(x12,x13,x23); A.18 paper order (x12,x23,x13) is
## explicitly converted before every relator replay and composite.
#############################################################################
Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;
B2Json:=function(x)local a,i;if x=true then return "true";fi;if x=false then return "false";fi;if IsInt(x) then return String(x);fi;if IsList(x) and Length(x)=0 then return "[]";fi;if IsString(x) then return Concatenation("\"",x,"\"");fi;if IsList(x) then a:=List([1..Length(x)],i->B2Json(x[i]));return Concatenation("[",JoinC(a,","),"]");fi;Error("marity phaseb1 n3: json");end;;
B2Perm:=function(p,d)return List([1..d],i->i^p);end;;
B2Sum:=function(p,dp,q,dq)local a,j;a:=[1..dp+dq];for j in [1..dq] do a[dp+j]:=dp+(j^q);od;return p*PermList(a);end;;
B2Eval:=function(w,imgs)local z,k,x;z:=One(imgs[1]);for x in w do k:=AbsInt(x);if k=0 or k>Length(imgs) then Error("marity phaseb1 n3: row");fi;if x>0 then z:=z*imgs[k];else z:=z*imgs[k]^-1;fi;od;return z;end;;

if IsBound(D972_B4_MARITY_PHASEB1_N3_SELFTEST) and D972_B4_MARITY_PHASEB1_N3_SELFTEST=true then
  Print("D972_B4_MARITY_PHASEB1_N3_V2_SELFTEST_PASS canonical_order=true center_marking=true\n");
else
  if not IsBound(D972_B4_MARITY_PHASEB1_N3_OUTPUT) then D972_B4_MARITY_PHASEB1_N3_OUTPUT:="ci/out/d972_b4_marity_phaseb1_n3_v2.json";;fi;
  F4:=FreeGroup("s1","s2","s3");;s1:=F4.1;;s2:=F4.2;;s3:=F4.3;;
  B4:=F4/[s1*s3*s1^-1*s3^-1,s1*s2*s1*(s2*s1*s2)^-1,s2*s3*s2*(s3*s2*s3)^-1];;
  b1:=B4.1;;b2:=B4.2;;b3:=B4.3;;
  X12:=b1^2;;X23:=b2^2;;X34:=b3^2;;X13:=b2*b1^2*b2^-1;;X24:=b3*b2^2*b3^-1;;X14:=b3*X13*b3^-1;;
  pb4Marks:=[X12,X13,X14,X23,X24,X34];;pb4Sub:=Subgroup(B4,pb4Marks);;
  if Index(B4,pb4Sub)<>24 then Error("marity phaseb1 n3: PB4 index");fi;
  pb4Iso:=IsomorphismFpGroupByGenerators(pb4Sub,pb4Marks);;PB4fp:=Image(pb4Iso);;gPB4:=GeneratorsOfGroup(PB4fp);;
  if Length(gPB4)<>6 then Error("marity phaseb1 n3: PB4 marks");fi;
  fp4:=FreeGroupOfFpGroup(PB4fp);;fp4g:=GeneratorsOfGroup(fp4);;rels4:=RelatorsOfFpGroup(PB4fp);;
  F3:=FreeGroup("s1","s2");;a1:=F3.1;;a2:=F3.2;;B3:=F3/[a1*a2*a1*(a2*a1*a2)^-1];;b3a1:=B3.1;;b3a2:=B3.2;;
  marks3:=[b3a1^2,b3a2*b3a1^2*b3a2^-1,b3a2^2];;sub3:=Subgroup(B3,marks3);;
  if Index(B3,sub3)<>6 then Error("marity phaseb1 n3: PB3 index");fi;
  iso3:=IsomorphismFpGroupByGenerators(sub3,marks3);;PB3fp:=Image(iso3);;gPB3:=GeneratorsOfGroup(PB3fp);;
  fp3:=FreeGroupOfFpGroup(PB3fp);;fp3g:=GeneratorsOfGroup(fp3);;rels3:=RelatorsOfFpGroup(PB3fp);;
  c3:=Product(marks3);;if c3<>(b3a1*b3a2)^3 then Error("marity phaseb1 n3: center replay");fi;

  g9:=MakeGn(9);;CheckGF8();;Smat:=MakeMatGF8(1,0,1,1);;Tmat:=MakeMatGF8(4,3,1,5);;Sperm:=MatToPermGF8(Smat);;Tperm:=MatToPermGF8(Tmat);;Xp:=(Sperm*Tperm^-1)^2;;Yp:=Sperm^-1*Xp*Sperm;;Pgrp:=Group(Xp,Yp);;
  XM:=B2Sum(g9.x,27,Xp,9);;YM:=B2Sum(g9.y,27,Yp,9);;GM:=Group(XM,YM);;if Size(GM)<>1469664 then Error("marity phaseb1 n3: M order");fi;
  mImgs:=[XM,XM^-1*YM^-1,YM];;
  hM3:=GroupHomomorphismByImages(PB3fp,GM,gPB3,mImgs);;if hM3=fail then Error("marity phaseb1 n3: PB3 target marking");fi;
  if not ForAll(rels3,w->Image(hM3,MappedWord(w,fp3g,gPB3))=One(GM)) then Error("marity phaseb1 n3: target PB3 relator");fi;
  rows:=[ [[],[],[],[1],[2],[3]],[[],[1],[2],[],[],[3]],[[1],[],[2],[],[3],[]],[[1],[2],[],[3],[],[]] ];;
  targetMaps:=List(rows,r->GroupHomomorphismByImages(PB4fp,GM,gPB4,List(r,w->B2Eval(w,mImgs))));;
  if ForAny(targetMaps,h->h=fail) then Error("marity phaseb1 n3: deletion target");fi;
  D4:=DirectProduct(GM,GM,GM,GM);;e4:=List([1..4],i->Embedding(D4,i));;pack4:=function(v)return Product(List([1..4],i->Image(e4[i],v[i])));end;;
  cmMap:=GroupHomomorphismByImages(PB4fp,D4,gPB4,List(gPB4,g->pack4(List(targetMaps,h->Image(h,g)))));;if cmMap=fail then Error("marity phaseb1 n3: C_M map");fi;CMq:=Image(cmMap);;

  # Paper A.18 order is (x12,x23,x13); canonical source order is (x12,x13,x23).
  paper:=[[X12,X23,X13],[X23,X34,X24],[X13*X23,X34,X14*X24],[X12*X13,X24*X34,X14],[X12,X23*X24,X13*X14]];;
  canon:=List(paper,t->[t[1],t[3],t[2]]);;
  paperLabels:=[["x12","x23","x13"],["x23","x34","x24"],["x13*x23","x34","x14*x24"],["x12*x13","x24*x34","x14"],["x12","x23*x24","x13*x14"]];;
  canonicalLabels:=[["x12","x13","x23"],["x23","x24","x34"],["x13*x23","x14*x24","x34"],["x12*x13","x14","x24*x34"],["x12","x13*x14","x23*x24"]];;
  D5:=DirectProduct(CMq,CMq,CMq,CMq,CMq);;e5:=List([1..5],i->Embedding(D5,i));;pack5:=function(v)return Product(List([1..5],i->Image(e5[i],v[i])));end;;
  cofaceMaps:=[];;composites:=[];;cofaceReplay:=[];;
  for k in [1..5] do
    cfp:=List(canon[k],w->Image(pb4Iso,w));;
    hc:=GroupHomomorphismByImages(PB3fp,PB4fp,gPB3,cfp);;if hc=fail then Error("marity phaseb1 n3: coface map ",k);fi;
    ok:=ForAll(rels3,w->Image(hc,MappedWord(w,fp3g,gPB3))=One(PB4fp));;if not ok then Error("marity phaseb1 n3: coface relator ",k);fi;Add(cofaceReplay,ok);
    Add(cofaceMaps,List(cfp,w->Image(cmMap,w)));
    Add(composites,List([1..4],i->List([1..3],j->B2Perm(Image(targetMaps[i],Image(hc,gPB3[j])),36))));
  od;
  nMap:=GroupHomomorphismByImages(PB3fp,D5,gPB3,List([1..3],j->pack5(List([1..5],k->cofaceMaps[k][j]))));;if nMap=fail then Error("marity phaseb1 n3: N3 map");fi;
  if not ForAll(rels3,w->Image(nMap,MappedWord(w,fp3g,gPB3))=One(D5)) then Error("marity phaseb1 n3: N3 relator replay");fi;
  N3q:=Image(nMap);;N3ord:=Size(N3q);;f2q:=Group(Image(nMap,gPB3[1]),Image(nMap,gPB3[3]));;f2ord:=Size(f2q);;
  identityComposite:=false;;for k in [1..5] do for i in [1..4] do if ForAll([1..3],j->Image(targetMaps[i],Image(GroupHomomorphismByImages(PB3fp,PB4fp,gPB3,List(canon[k],w->Image(pb4Iso,w))),gPB3[j]))=Image(hM3,gPB3[j])) then identityComposite:=true;fi;od;od;;
  if not identityComposite then Error("marity phaseb1 n3: N3 subset M gate");fi;
  if N3ord mod Size(GM)<>0 then Error("marity phaseb1 n3: M/N3 index arithmetic");fi;
  cert:=Concatenation("{\"schema\":\"d972-b4-marity-phaseb1-n3/v2\",\"status\":\"N3_TYPED_CANONICAL_REPLAY\",\"source_group\":\"PB3\",\"target_group\":\"PB3/M\",\"pb3\":{\"generator_labels\":[\"x12\",\"x13\",\"x23\"],\"relator_count\":",String(Length(rels3)),",\"index_in_B3\":6,\"center_replay\":true},\"target_marking\":[\"X\",\"X^-1Y^-1\",\"Y\"],\"cm_quotient_order\":",String(Size(CMq)),",\"cofaces\":{\"paper_order\":[\"x12\",\"x23\",\"x13\"],\"canonical_order\":[\"x12\",\"x13\",\"x23\"],\"count\":5,\"all_relators_replayed\":true,\"paper_triples\":",B2Json(paperLabels),",\"canonical_triples\":",B2Json(canonicalLabels),"},\"composites\":",B2Json(composites),",\"N3\":{\"quotient_order\":",String(N3ord),",\"F2_image_order\":",String(f2ord),",\"M_over_N3_order\":",String(QuoInt(N3ord,Size(GM))),",\"N3_le_M\":true},\"gentle_fiber_gate\":{\"status\":\"BLOCKED_NOT_IMPLEMENTED\",\"expected_targets\":972,\"enumerated\":false},\"typing_boundary\":{\"M_B4_stable\":false,\"GT_descent\":\"UNPROVED\"}}\n");
  WriteFile(D972_B4_MARITY_PHASEB1_N3_OUTPUT,cert);;Print("D972_B4_MARITY_PHASEB1_N3_V2_WRITTEN ",D972_B4_MARITY_PHASEB1_N3_OUTPUT," N3=",N3ord,"\n");
fi;
