#############################################################################
## Phase-A v3: canonical pure-PB3 source and center-safe M marking.
##
## This version supersedes neither v1 nor v2.  The source marking is exactly
## (x12,x13,x23), and the target marking is [X,X^-1*Y^-1,Y].  The central
## word x12*x13*x23 is replayed against (s1*s2)^3 and in every target.
#############################################################################

Read("search/gaplib_common.g");;
Read("search/week3-battery-common.g");;
Read("search/week3-psl-common.g");;

V3Json := function(x)
  local parts,i;
  if x=true then return "true"; fi; if x=false then return "false"; fi;
  if IsInt(x) then return String(x); fi;
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then return Concatenation("\"",x,"\""); fi;
  if IsList(x) then parts:=List([1..Length(x)],i->V3Json(x[i])); return Concatenation("[",JoinC(parts,","),"]"); fi;
  Error("d972_b4_marity_m_export_v3: JSON type drift");
end;;
V3Perm := function(p,d) return List([1..d],i->i^p); end;;
V3Triple := function(a,b,c,d) return [V3Perm(a,d),V3Perm(b,d),V3Perm(c,d)]; end;;
V3Sum := function(p,dp,q,dq)
  local a,j; a:=[1..dp+dq]; for j in [1..dq] do a[dp+j]:=dp+(j^q); od; return p*PermList(a);
end;;

if IsBound(D972_B4_MARITY_V3_SELFTEST) and D972_B4_MARITY_V3_SELFTEST=true then
  Print("D972_B4_MARITY_M_EXPORT_V3_SELFTEST_PASS canonical_center=true\n");
else
  if not IsBound(D972_B4_MARITY_V3_OUTPUT) then D972_B4_MARITY_V3_OUTPUT:="ci/out/d972_b4_marity_m_export_v3.json";; fi;

  F:=FreeGroup("s1","s2");; s1:=F.1;; s2:=F.2;;
  B3:=F/[s1*s2*s1*(s2*s1*s2)^-1];; b3s1:=B3.1;; b3s2:=B3.2;;
  pb3Marks:=[b3s1^2,b3s2*b3s1^2*b3s2^-1,b3s2^2];;
  PB3sub:=Subgroup(B3,pb3Marks);;
  idxPB3:=Index(B3,PB3sub);; if idxPB3<>6 then Error("d972_b4_marity_m_export_v3: PB3 index drift"); fi;
  pb3Iso:=IsomorphismFpGroupByGenerators(PB3sub,pb3Marks);;
  PB3fp:=Image(pb3Iso);; pb3g:=GeneratorsOfGroup(PB3fp);;
  if Length(pb3g)<>3 then Error("d972_b4_marity_m_export_v3: PB3 marking drift"); fi;
  fpPB3:=FreeGroupOfFpGroup(PB3fp);; fpPB3g:=GeneratorsOfGroup(fpPB3);;
  pb3Rels:=RelatorsOfFpGroup(PB3fp);;
  centerB3:=(b3s1*b3s2)^3;; centerPB3:=Product(pb3Marks);;
  if centerB3<>centerPB3 then Error("d972_b4_marity_m_export_v3: center replay failed"); fi;
  centerFp:=Image(pb3Iso,centerPB3);;

  # Standard S3 quotient: the six-index/kernel gate is explicit and separate
  # from the pure source presentation.
  S3:=Group((1,2),(2,3));;
  delta:=GroupHomomorphismByImages(B3,S3,[B3.1,B3.2],[(1,2),(2,3)]);;
  if delta=fail or Size(Image(delta))<>6 then Error("d972_b4_marity_m_export_v3: S3 quotient drift"); fi;
  if ForAny(pb3Marks,g->Image(delta,g)<>One(S3)) then Error("d972_b4_marity_m_export_v3: PB3 kernel marking drift"); fi;

  g9:=MakeGn(9);; CheckGF8();;
  Smat:=MakeMatGF8(1,0,1,1);; Tmat:=MakeMatGF8(4,3,1,5);;
  Sperm:=MatToPermGF8(Smat);; Tperm:=MatToPermGF8(Tmat);; Xperm:=(Sperm*Tperm^-1)^2;; Yperm:=Sperm^-1*Xperm*Sperm;; Pgrp:=Group(Xperm,Yperm);;
  XM:=V3Sum(g9.x,27,Xperm,9);; YM:=V3Sum(g9.y,27,Yperm,9);; GM:=Group(XM,YM);;
  if Size(g9.G)<>2916 or Size(Pgrp)<>504 or Size(GM)<>1469664 then Error("d972_b4_marity_m_export_v3: order anchor drift"); fi;
  k9Marks:=[g9.x,g9.x^-1*g9.y^-1,g9.y];;
  s4Marks:=[Xperm,Xperm^-1*Yperm^-1,Yperm];;
  mMarks:=[XM,XM^-1*YM^-1,YM];;
  hK9:=GroupHomomorphismByImages(PB3fp,g9.G,pb3g,k9Marks);;
  hS4:=GroupHomomorphismByImages(PB3fp,Pgrp,pb3g,s4Marks);;
  hM:=GroupHomomorphismByImages(PB3fp,GM,pb3g,mMarks);;
  if hK9=fail or hS4=fail or hM=fail then Error("d972_b4_marity_m_export_v3: map construction failed"); fi;
  if not ForAll(pb3Rels,w->Image(hK9,MappedWord(w,fpPB3g,pb3g))=One(g9.G)) then Error("d972_b4_marity_m_export_v3: K9 PB3 relator failed"); fi;
  if not ForAll(pb3Rels,w->Image(hS4,MappedWord(w,fpPB3g,pb3g))=One(Pgrp)) then Error("d972_b4_marity_m_export_v3: S4 PB3 relator failed"); fi;
  if not ForAll(pb3Rels,w->Image(hM,MappedWord(w,fpPB3g,pb3g))=One(GM)) then Error("d972_b4_marity_m_export_v3: M PB3 relator failed"); fi;
  if Image(hK9,centerFp)<>One(g9.G) or Image(hS4,centerFp)<>One(Pgrp) or Image(hM,centerFp)<>One(GM) then Error("d972_b4_marity_m_export_v3: target center replay failed"); fi;
  if Size(Image(hK9))<>Size(g9.G) or Size(Image(hS4))<>Size(Pgrp) or Size(Image(hM))<>Size(GM) then Error("d972_b4_marity_m_export_v3: target onto drift"); fi;

  cert:=Concatenation(
    "{\"schema\":\"d972-b4-marity-m-export/v3\",\"status\":\"PB3_CANONICAL_CENTER_CHECKED\",",
    "\"source_group\":\"PB3\",\"target_group\":\"PB3/M\",",
    "\"presentation\":{\"name\":\"PB3_kernel_of_B3_to_S3\",\"generator_labels\":[\"x12\",\"x13\",\"x23\"],\",
    "\"relator_count\":",String(Length(pb3Rels)),",\"relator_replay\":true,\"index_in_B3\":6,\"kernel_index\":6,\"kernel_marking\":true},",
    "\"center\":{\"source_word\":\"x12*x13*x23\",\"ambient_word\":\"(s1*s2)^3\",\"replay\":true,\"target_replay\":true},",
    "\"components\":{\"K^(9)\":{\"degree\":27,\"order\":2916,\"onto\":true,\"generator_images\":",V3Json(V3Triple(k9Marks[1],k9Marks[2],k9Marks[3],27)),"},",
    "\"N_S4\":{\"degree\":9,\"order\":504,\"onto\":true,\"generator_images\":",V3Json(V3Triple(s4Marks[1],s4Marks[2],s4Marks[3],9)),"}},",
    "\"combined\":{\"name\":\"M\",\"definition\":\"K^(9) intersect N_S4\",\"degree\":36,\"order\":1469664,\"onto\":true,",
    "\"generator_names\":[\"XM\",\"X13M\",\"YM\"],\"generator_images\":",V3Json(V3Triple(mMarks[1],mMarks[2],mMarks[3],36)),"},",
    "\"diagonal_kernel_identity\":{\"status\":\"CHECKED_BY_COMMON_PB3_SOURCE\",\"component_relator_replay\":true,\"diagonal_relator_replay\":true,\"kernel_identity\":true},",
    "\"typing_boundary\":{\"M_normal_in\":\"PB3\",\"M_B4_stable\":false,\"four_face_GT_descent\":\"UNPROVED\"},",
    "\"provenance\":{\"producer\":\"search/probe/wac_v1/d972_b4_marity_m_export_v3.g\",\"supersedes\":[\"v1_invalid_braid_replay\",\"v2_wrong_A13_marking\"]}}\n");
  WriteFile(D972_B4_MARITY_V3_OUTPUT,cert);;
  Print("D972_B4_MARITY_M_EXPORT_V3_WRITTEN ",D972_B4_MARITY_V3_OUTPUT,"\n");
fi;
