#############################################################################
## d972_b4_lowindex_v1.g — bounded Linux GAP producer (max index 7).
## Repository-relative reads only; all-pass is UNKNOWN, never B.
#############################################################################
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/week3-psl-common.g");
DirectSumPerm := function(p,psize,q,qsize)
  local images,j;
  images := [1..psize+qsize];
  for j in [1..psize] do images[j] := j^p; od;
  for j in [1..qsize] do images[psize+j] := psize + (j^q); od;
  return PermList(images);
end;;
# Compact pure base reconstructed directly from G9 and PSL2(8).
g9 := MakeGn(9);; G9:=g9.G;; x9:=g9.x;; y9:=g9.y;;
if Size(G9)<>2916 then Error("G9 order"); fi;
CheckGF8();;
Smat:=MakeMatGF8(1,0,1,1);; Tmat:=MakeMatGF8(4,3,1,5);;
Sperm:=MatToPermGF8(Smat);; Tperm:=MatToPermGF8(Tmat);; ww:=Sperm*Tperm^-1;; x4:=ww^2;; y4:=Sperm^-1*x4*Sperm;;
P4:=Group(x4,y4);; if Size(P4)<>504 then Error("P4 order"); fi;
compactX:=DirectSumPerm(x9,27,x4,9);; compactY:=DirectSumPerm(y9,27,y4,9);; compactPure:=Group(compactX,compactY);;
Print("PURE_ORDER ",Size(compactPure),"\n");
if Size(compactPure)<>1469664 then Error("pure order"); fi;
isoPure:=IsomorphismFpGroupByGenerators(compactPure,[compactX,compactY],"p");;
pureFp:=Image(isoPure);; pgens:=GeneratorsOfGroup(pureFp);; relsP:=RelatorsOfFpGroup(pureFp);;
Print("PURE_FP_ORDER ",Size(pureFp),"\n");
Print("PURE_GEN_COUNT ",Length(pgens),"\n"); Print("PURE_REL_COUNT ",Length(relsP),"\n");
Print("PURE_REL_LENGTHS ",List(relsP,Length),"\n");
# PB4 and K05 independently from Artin B4.
F:=FreeGroup("s1","s2","s3");; z1:=F.1;; z2:=F.2;; z3:=F.3;;
B4:=F/[z1*z3*z1^-1*z3^-1,z1*z2*z1*(z2*z1*z2)^-1,z2*z3*z2*(z3*z2*z3)^-1];;
b1:=B4.1;; b2:=B4.2;; b3:=B4.3;;
X12:=b1^2;; X23:=b2^2;; X34:=b3^2;; X13:=b2*b1^2*b2^-1;; X24:=b3*b2^2*b3^-1;; X14:=b3*X13*b3^-1;;
gensPB4:=[X12,X13,X14,X23,X24,X34];; PB4sub:=Subgroup(B4,gensPB4);;
isoPB:=IsomorphismFpGroupByGenerators(PB4sub,gensPB4,"x");; PB4fp:=Image(isoPB);; gPB:=GeneratorsOfGroup(PB4fp);;
Delta2:=(b1*b2*b3)^4;; if not Delta2 in PB4sub then Error("Delta not PB4"); fi;
Delta2img:=ImageElm(isoPB,Delta2);; FPB:=FreeGroupOfFpGroup(PB4fp);; relPB:=RelatorsOfFpGroup(PB4fp);;
K05:=FPB/Concatenation(relPB,[UnderlyingElement(Delta2img)]);; gK:=GeneratorsOfGroup(K05);;
Print("K05_REL_COUNT ",Length(RelatorsOfFpGroup(K05)),"\n"); Print("K05_AB ",AbelianInvariants(K05),"\n");
# Map named generators into K05 and construct rho images using sphere row products.
k12:=gK[1];; k13:=gK[2];; k14:=gK[3];; k23:=gK[4];; k24:=gK[5];; k34:=gK[6];;
x15:=(k12*k13*k14)^-1;; x25:=(k12*k23*k24)^-1;; x35:=(k13*k23*k34)^-1;; x45:=(k14*k24*k34)^-1;;
rhoImgs:=[x45,k14,k24,x15,x25,k12];;
relsK:=RelatorsOfFpGroup(K05);; FK:=FreeGroupOfFpGroup(K05);; fgens:=GeneratorsOfGroup(FK);;
bad:=[];; for i in [1..Length(relsK)] do if not IsOne(MappedWord(relsK[i],fgens,rhoImgs)) then Add(bad,i); fi; od;
Print("RHO_BAD_COUNT ",Length(bad),"\n"); Print("RHO_BAD_INDICES ",bad,"\n");
# save all data in globals for next stages if this script is extended.

# Build universal rho-stable normal closure of the marked pure relators.
FPure:=FreeGroupOfFpGroup(pureFp);; fPure:=GeneratorsOfGroup(FPure);;
rhoHom:=GroupHomomorphismByImagesNC(K05,K05,gK,rhoImgs);;
baseJ:=List(relsP,r -> MappedWord(r,fPure,[k12,k23]));;
allJ:=[];; cur:=baseJ;;
for it in [0..4] do
  Append(allJ,List(cur,UnderlyingElement));
  cur:=List(cur,w -> Image(rhoHom,w));
od;
Print("WM_REL_COUNT ",Length(allJ),"\n");
# Check rho^5 on all six named generators before quotient.
rr:=rhoImgs;; for i in [1..4] do rr:=List(rr,w -> Image(rhoHom,w)); od;;
Print("RHO5_ID ",ForAll([1..6],i -> rr[i]=gK[i]),"\n");
FK05:=FreeGroupOfFpGroup(K05);; relK0:=RelatorsOfFpGroup(K05);;
Ufp:=FK05/Concatenation(relK0,allJ);;
Print("U_REL_COUNT ",Length(RelatorsOfFpGroup(Ufp)),"\n");
Print("U_AB ",AbelianInvariants(Ufp),"\n");
# Portable signed-word helper; no worker/temp file is required.
D972SignedWord := function(w)
  local e,o,i,g,n,j;
  e:=ExtRepOfObj(w);; o:=[];; i:=1;;
  while i<=Length(e) do
    g:=e[i];; n:=e[i+1];;
    if n>0 then for j in [1..n] do Add(o,g); od;
    else for j in [1..-n] do Add(o,-g); od; fi;
    i:=i+2;
  od;
  return o;
end;;

B4LIJson := function(x)
  local i,p;
  if IsInt(x) then return String(x); fi;
  if IsString(x) then return Concatenation("\"",x,"\""); fi;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if not IsList(x) then Error("B4 low-index JSON type drift"); fi;
  p:=List([1..Length(x)],i->B4LIJson(x[i]));
  return Concatenation("[",JoinC(p,","),"]");
end;;

B4LILess := function(a,b)
  local i;
  if IsInt(a) and IsInt(b) then return a<b; fi;
  if not (IsList(a) and IsList(b)) then Error("B4 low-index comparator drift"); fi;
  for i in [1..Minimum(Length(a),Length(b))] do
    if a[i]=b[i] then continue; fi;
    return B4LILess(a[i],b[i]);
  od;
  return Length(a)<Length(b);
end;;

B4LIBlock := function(p,off,n)
  return PermList(List([1..n],j->(off+j)^p-off));
end;;

B4LID9 := function(p)
  local rs,r,s,a,e;
  rs:=MakeDn(9);; r:=rs[1];; s:=rs[2];;
  for a in [0..8] do for e in [0..1] do
    if p=r^a*s^e then return [a,e]; fi;
  od; od;
  Error("B4 low-index: D9 coordinate drift");
end;;

B4LICan9 := function(p)
  local out,i;
  out:=[];;
  for i in [0..2] do Append(out,B4LID9(B4LIBlock(p,9*i,9))); od;
  return out;
end;;

B4LIKey := function(m,p27,p9)
  local c9,c4;
  c9:=B4LICan9(p27);; c4:=List([1..9],j->j^p9);;
  return rec(orderkey:=[m,c9,c4],
    string:=Concatenation("(",String(m mod 18),";",
      JoinC(List(c9,String),","),";",
      JoinC(List(c4,String),","),")"));
end;;

F6:=FreeGroup(6);; F6g:=GeneratorsOfGroup(F6);;
rf:=[(F6g[3]*F6g[5]*F6g[6])^-1,F6g[3],F6g[5],
  (F6g[1]*F6g[2]*F6g[3])^-1,
  (F6g[1]*F6g[4]*F6g[5])^-1,F6g[1]];;
Dc:=DerivedSubgroup(compactPure);; de:=Elements(Dc);;
no:=Lcm(Order(compactX),Order(compactY));;
ch:=Filtered([0..no-1],m->Gcd(2*m+1,no)=1);;
F2c:=FreeGroup("u","v");;
epc:=GroupHomomorphismByImages(F2c,compactPure,[F2c.1,F2c.2],
  [compactX,compactY]);;
th:=GroupHomomorphismByImages(compactPure,compactPure,
  [compactX,compactY],[compactY,compactX]);;
zc:=(compactX*compactY)^-1;;
ta:=GroupHomomorphismByImages(compactPure,compactPure,
  [compactX,compactY],[compactY,zc]);;
rows:=[];
for mm in ch do
  uu:=2*mm+1;;
  for ff in de do
    tf:=Image(th,ff);;
    if ff*tf=One(compactPure) then
      ym:=compactY^mm*ff;; ty:=Image(ta,ym);; t2:=Image(ta,ty);;
      if t2*ty*ym=One(compactPure) and
         Size(Group(compactX^uu,ff^-1*compactY^uu*ff))=Size(compactPure) then
        Add(rows,[mm,ff]);
      fi;
    fi;
  od;
od;;
if Length(rows)<>972 then Error("B4 low-index: exact roof count drift"); fi;
swRows:=List(rows,r->D972SignedWord(PreImagesRepresentative(epc,r[2])));;

keyRows:=[];
for ii in [1..Length(rows)] do
  Add(keyRows,rec(m:=rows[ii][1],word:=swRows[ii],
    key:=B4LIKey(rows[ii][1],B4LIBlock(rows[ii][2],0,27),
      B4LIBlock(rows[ii][2],27,9))));
od;;
Sort(keyRows,function(a,b) return B4LILess(a.key.orderkey,b.key.orderkey); end);;
targetKeys:=List(keyRows,r->r.key.string);;
roofWords:=List(keyRows,r->r.word);;
targetKeysSorted:=SortedList(targetKeys);;
targetDigest:=HexSHA256(Concatenation(JoinC(targetKeysSorted,"\n"),"\n"));;
fu:=FreeGroupOfFpGroup(Ufp);; fugen:=GeneratorsOfGroup(fu);;
ug:=GeneratorsOfGroup(Ufp);; relsU:=RelatorsOfFpGroup(Ufp);;
relWords:=List(relsU,D972SignedWord);;
relDigest:=HexSHA256(B4LIJson(relWords));;
roofDigest:=HexSHA256(B4LIJson(roofWords));;
artifactRows:=List(keyRows,r->[r.m,r.key.orderkey,r.word]);;
artifactDigest:=HexSHA256(B4LIJson(artifactRows));;
if targetDigest<>"9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62" then
  Error("B4 low-index: target-key digest drift");
fi;
if relDigest<>"12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e" then
  Error("B4 low-index: relator digest drift");
fi;
Print("B4_LI_ROWS=972 TARGET_DIGEST=",targetDigest,
  " WORD_KEY_DIGEST=",artifactDigest,"\n");;
B4LIWKOut:="ci/out/d972_b4_word_key_artifact_v1.json";;
if IsBound(D972_B4_WORD_KEY_OUTPUT) then B4LIWKOut:=D972_B4_WORD_KEY_OUTPUT; fi;
B4LIWKArtifact:=Concatenation(
  "{\"schema\":\"d972-b4-word-key-artifact/v1\",\"count\":972,",
  "\"source_target_key_digest\":\"",targetDigest,"\",",
  "\"canonical_bytes_sha256\":\"",artifactDigest,"\",\"rows\":",
  B4LIJson(artifactRows),"}");;
WriteFile(B4LIWKOut,Concatenation(B4LIWKArtifact,"\n"));;
Print("B4_LI_WORD_KEY_ARTIFACT count=972 digest=",artifactDigest,
  " output=",B4LIWKOut,"\n");;

B4LIOut:="ci/out/d972_b4_lowindex_v1.json";;
if IsBound(D972_B4_LOWINDEX_OUTPUT) then B4LIOut:=D972_B4_LOWINDEX_OUTPUT; fi;
B4LIWrite:=function(s) WriteFile(B4LIOut,Concatenation(s,"\n")); end;;
eval:=function(sw,ix,iy)
  local zz,a;
  zz:=One(ix);;
  for a in sw do
    if a=1 then zz:=zz*ix; elif a=2 then zz:=zz*iy;
    elif a=-1 then zz:=zz*ix^-1; elif a=-2 then zz:=zz*iy^-1; fi;
  od;
  return zz;
end;;
rhoWords:=List(rf,D972SignedWord);;
rhoJson:=B4LIJson(rhoWords);; relJson:=B4LIJson(relWords);;
targetJson:=B4LIJson(targetKeys);; roofJson:=B4LIJson(roofWords);;
if Length(relWords)<>158 then Error("B4 low-index: relator count drift"); fi;
## Export the hash-bound U_M word list for the SAT lane.  This is written on
## an all-pass bounded quotient run too; it is not a mathematical verdict.
B4LIRelOut:="ci/out/d972_b4_u_relators_v1.json";;
if IsBound(D972_B4_RELATOR_OUTPUT) then B4LIRelOut:=D972_B4_RELATOR_OUTPUT; fi;
B4LIRelArtifact:=Concatenation(
  "{\"schema\":\"d972-b4-u-relators/v1\",\"count\":158,",
  "\"canonical_bytes_sha256\":\"",relDigest,"\",\"relators\":",
  relJson,"}");;
WriteFile(B4LIRelOut,Concatenation(B4LIRelArtifact,"\n"));;
Print("B4_LI_RELATOR_ARTIFACT count=158 digest=",relDigest,
  " output=",B4LIRelOut,"\n");;
if IsBound(D972_B4_RELATOR_ONLY) and D972_B4_RELATOR_ONLY=true then
  Print("B4_LI_RELATOR_ONLY_DONE\n");;
  QUIT;
fi;

li:=LowIndexSubgroupsFpGroup(Ufp,7);;
Print("B4_LI_LOWINDEX_COUNT=",Length(li)," MAX=7\n");;
qRows:=[];; first:=fail;; qi:=0;;
for Hq in li do
  qi:=qi+1;;
  if first<>fail then break; fi;
  m:=Index(Ufp,Hq);; qh:=FactorCosetAction(Ufp,Hq);;
  h0:=List(ug,g->Image(qh,g));;
  relok:=List(relsU,r->IsOne(MappedWord(r,fugen,h0)));;
  rw:=ShallowCopy(F6g);; hp:=[];
  for tt in [0..4] do
    Add(hp,List(rw,w->MappedWord(w,F6g,h0)));;
    rw:=List(rw,w->MappedWord(w,F6g,rf));
  od;;
  rho5:=List(rw,w->MappedWord(w,F6g,h0))=h0;;
  fails:=0;;
  for ii in [1..Length(keyRows)] do
    zz:=One(Image(qh));;
    for tt in Reversed([0..4]) do
      zz:=zz*eval(keyRows[ii].word,hp[tt+1][1],hp[tt+1][4]);
    od;
    if not IsOne(zz) then
      fails:=fails+1;;
      if first=fail then
        first:=rec(qi:=qi,index:=m,order:=Size(Image(qh)),
          abelian:=IsAbelian(Image(qh)),row:=ii,m:=keyRows[ii].m,
          word:=keyRows[ii].word,defect:=List([1..m],j->j^zz),
          images:=List(h0,p->List([1..m],j->j^p)),
          relators:=relok,rho5:=rho5);
      fi;
    fi;
  od;
  Add(qRows,rec(index:=m,order:=Size(Image(qh)),
    abelian:=IsAbelian(Image(qh)),relator_bad:=Number(relok,x->x=false),
    rho5:=rho5,shadow_failures:=fails));
  Print("B4_LI_Q=",qi," INDEX=",m," ORDER=",Size(Image(qh)),
    " ABELIAN=",IsAbelian(Image(qh))," REL_BAD=",
    Number(relok,x->x=false)," RHO5=",rho5,
    " SHADOW_FAILS=",fails,"\n");;
od;;

if first=fail and Length(qRows)=Length(li) then
  qAgg:=List(qRows,r->[r.index,r.order,r.abelian,r.relator_bad,
    r.rho5,r.shadow_failures]);;
  B4LIWrite(Concatenation(
    "{\"schema\":\"d972-b4-lowindex/v1\",",
    "\"status\":\"UNKNOWN_ALLPASS_CONTINUE\",\"max_index\":7,",
    "\"quotient_count\":",String(Length(li)),",\"roof_count\":972,",
    "\"all_relators_sha256\":\"",relDigest,"\",",
    "\"target_key_digest\":\"",targetDigest,"\",",
    "\"word_key_artifact_sha256\":\"",artifactDigest,"\",",
    "\"quotients\":",B4LIJson(qAgg),"}"));
  Print("B4_LI_ALLPASS UNKNOWN quotients=",Length(li),"\n");;
else
  B4LIWrite(Concatenation(
    "{\"schema\":\"d972-b4-finite-image/v2\",\"status\":\"DEFECT_CANDIDATE\",",
    "\"target\":\"LI7\",\"target_order\":",String(first.order),
    ",\"epi_index\":",String(first.qi),",\"epi_count\":",String(Length(li)),
    ",\"h_images\":",B4LIJson(first.images),",\"rho_words\":",rhoJson,
    ",\"all_relators\":",relJson,",\"all_relators_sha256\":\"",relDigest,"\",",
    "\"target_keys\":",targetJson,",\"target_key_digest\":\"",targetDigest,"\",",
    "\"roof_words\":",roofJson,",\"roof_words_sha256\":\"",roofDigest,"\",",
    "\"word_key_artifact_sha256\":\"",artifactDigest,"\",",
    "\"witness_index\":",String(first.row),",\"witness_word\":",
    B4LIJson(first.word),",\"witness_defect\":",B4LIJson(first.defect),"}"));
  Print("B4_LI_DEFECT qi=",first.qi," row=",first.row,
    " index=",first.index," order=",first.order,"\n");;
fi;
QUIT;
