# crosscheck/check_d972_r07_literal_class6_augmented_v1.g
#
# Independent GHA-only checker/falsifier for the R07 literal class-six
# augmented solve.  It does not read/import the producer v3 implementation,
# its certificate, or its output logic.  Frozen public inputs only:
#   f0 formula; C5=(313599,2,-1,-2,0,1);
#   k=(2,-4,3,4,1,-2); the 796-letter gamma_6 exact-mark tail;
#   exact theta/tau/five-coface definitions; Lyndon/Hall conventions.
#
# Existing .github/workflows/gap-run.yml inputs:
#   script: crosscheck/check_d972_r07_literal_class6_augmented_v1.g
#   timeout_min: 240
#   with_pquot_packages: false
#   out_dir: ci/out
# Success requires no GAP Error/Syntax diagnostic and exactly one:
#   R07_CLASS6_FINAL_MARKER status=PASS
# Intermediate fail-closed markers:
#   R07_NQ_BOOTSTRAP_PASS
#   R07_CLASS6_EXACTIFIER5_PASS
#   R07_CLASS6_AFFINE_PASS
#   R07_CLASS6_D6_CALIBRATION_PASS
#   R07_CLASS6_AUGMENTED_SMITH_PASS
#   R07_CLASS6_EXACTIFIER6_PASS
#   R07_CLASS6_DIRECT_LITERAL_PASS
# No fake certificate, Ihara witness, cofinal lift, cross_checked, or verified
# claim is made by this checker.

if GAPInfo.Version <> "4.16.0" then Error("GAP 4.16.0 required"); fi;

# GAP's official 4.16.0 full archive contains NQ 2.5.11 sources, but its
# platform executable is not built on a fresh ubuntu-latest runner.  Resolve
# exactly one PackageInfo entry and exactly one native GAP root.  If and only
# if the executable is absent, build those pinned sources in place.  Every
# dynamic path below comes from authenticated GAP metadata and is single-quote
# escaped before entering the otherwise fixed shell command.
R07NqVersion := "2.5.11";
R07NqPackageInfoSha :=
  "e5e3370aa823163909a5130f1d803f43051e606305915718bcf7a363e5af5264";
R07NqConfigureSha :=
  "4c09599a55cbdf0eb22998280e197f64ebb2e6ca5ca884b80e3e8d55c1ca0bd0";
R07NqMakefileInSha :=
  "84def846c51b5fe54b79b1ca312ac5629c383ccadbe43349da4d40efa9c5d003";

R07NqShellQuote := function(s)
  if not IsString(s) or Position(s,'\n')<>fail or Position(s,'\r')<>fail then
    Error("R07_NQ: unsafe shell path");
  fi;
  return Concatenation("'",ReplacedString(s,"'","'\"'\"'"),"'");
end;

R07NqRequireFileSha := function(path,expected,label)
  local body,actual;
  body:=StringFile(path);
  if body=fail then Error("R07_NQ: missing ",label," at ",path); fi;
  actual:=HexSHA256(body);
  if actual<>expected then
    Error("R07_NQ: ",label," SHA256 drift: ",actual);
  fi;
end;

R07NqInfos:=PackageInfo("nq");;
if Length(R07NqInfos)<>1 then
  Error("R07_NQ: expected exactly one NQ PackageInfo entry");
fi;
R07NqInfo:=R07NqInfos[1];;
if not IsBound(R07NqInfo.Version) or R07NqInfo.Version<>R07NqVersion then
  Error("R07_NQ: NQ version drift");
fi;
if not IsBound(R07NqInfo.InstallationPath) then
  Error("R07_NQ: NQ InstallationPath missing");
fi;
R07NqPath:=R07NqInfo.InstallationPath;;
if not IsString(R07NqPath) or Length(R07NqPath)<2 or
   R07NqPath[Length(R07NqPath)]<>'/' then
  Error("R07_NQ: malformed NQ InstallationPath");
fi;
if not IsBound(GAPInfo.RootPaths) or not IsList(GAPInfo.RootPaths) then
  Error("R07_NQ: GAPInfo.RootPaths unavailable");
fi;

R07NqRootCandidates:=[];;
for R07NqRootCandidate in GAPInfo.RootPaths do
  if IsString(R07NqRootCandidate) and Length(R07NqRootCandidate)>0 then
    if R07NqRootCandidate[Length(R07NqRootCandidate)]<>'/' then
      R07NqRootCandidate:=Concatenation(R07NqRootCandidate,"/");
    fi;
    R07NqParentCandidate:=Concatenation(R07NqRootCandidate,"pkg/");;
    if Length(R07NqPath)>Length(R07NqParentCandidate) and
       PositionSublist(R07NqPath,R07NqParentCandidate)=1 then
      R07NqTailCandidate:=R07NqPath{
        [Length(R07NqParentCandidate)+1..Length(R07NqPath)]};;
      if Length(R07NqTailCandidate)>=2 and
         R07NqTailCandidate[Length(R07NqTailCandidate)]='/' and
         Position(R07NqTailCandidate{
           [1..Length(R07NqTailCandidate)-1]},'/')=fail and
         Position(R07NqRootCandidates,R07NqRootCandidate)=fail then
        Add(R07NqRootCandidates,R07NqRootCandidate);
      fi;
    fi;
  fi;
od;
if Length(R07NqRootCandidates)<>1 then
  Error("R07_NQ: PackageInfo does not select exactly one native GAP root");
fi;
R07NqGapRoot:=R07NqRootCandidates[1];;
R07NqPackageParent:=Concatenation(R07NqGapRoot,"pkg/");;
R07NqDirectoryName:=R07NqPath{
  [Length(R07NqPackageParent)+1..Length(R07NqPath)-1]};;
if R07NqPath<>Concatenation(R07NqPackageParent,R07NqDirectoryName,"/") then
  Error("R07_NQ: package-parent equality gate failed");
fi;

# gap-run.yml exports GAPROOT.  Authenticate it against the unique native root
# when present; local prebuilt installations need not define the variable.
R07NqEnvGapRoot:=fail;;
if IsBoundGlobal("GetEnv") then
  R07NqEnvGapRoot:=GetEnv("GAPROOT");
fi;
if R07NqEnvGapRoot<>fail and R07NqEnvGapRoot<>"" then
  if R07NqEnvGapRoot[Length(R07NqEnvGapRoot)]<>'/' then
    R07NqEnvGapRoot:=Concatenation(R07NqEnvGapRoot,"/");
  fi;
  if R07NqEnvGapRoot<>R07NqGapRoot then
    Error("R07_NQ: GAPROOT disagrees with PackageInfo/native root");
  fi;
fi;

R07NqRequireFileSha(Concatenation(R07NqPath,"PackageInfo.g"),
  R07NqPackageInfoSha,"NQ PackageInfo.g");
R07NqRequireFileSha(Concatenation(R07NqPath,"configure"),
  R07NqConfigureSha,"NQ configure");
R07NqRequireFileSha(Concatenation(R07NqPath,"Makefile.in"),
  R07NqMakefileInSha,"NQ Makefile.in");

R07NqExecutable:=Filename(DirectoriesPackagePrograms("nq"),"nq");;
R07NqBuilt:=false;;
if R07NqExecutable=fail then
  if PositionSublist(LowercaseString(GAPInfo.Architecture),"linux")=fail then
    Error("R07_NQ: missing executable outside the Linux bootstrap target");
  fi;
  R07NqOutRoot:=Filename(DirectoryCurrent(),"ci/out");;
  R07NqConfigureLog:=Concatenation(R07NqOutRoot,
    "/r07_nq_configure_v1.log");;
  R07NqMakeLog:=Concatenation(R07NqOutRoot,"/r07_nq_make_v1.log");;
  R07NqBuildSentinel:=Concatenation(R07NqOutRoot,
    "/r07_nq_bootstrap_v1.ok");;
  R07NqBuildCommand:=Concatenation(
    "set -eu; test -d ",R07NqShellQuote(R07NqOutRoot),"; ",
    "rm -f ",R07NqShellQuote(R07NqConfigureLog)," ",
      R07NqShellQuote(R07NqMakeLog)," ",
      R07NqShellQuote(R07NqBuildSentinel),"; ",
    "cd ",R07NqShellQuote(R07NqPath),"; test -x ./configure; ",
    "./configure --with-gaproot=",R07NqShellQuote(R07NqGapRoot),
      " > ",R07NqShellQuote(R07NqConfigureLog)," 2>&1; ",
    "make -j2 > ",R07NqShellQuote(R07NqMakeLog)," 2>&1; ",
    "printf 'R07_NQ_BUILD_SHELL_PASS\\n' > ",
      R07NqShellQuote(R07NqBuildSentinel));;
  Exec(R07NqBuildCommand);
  if StringFile(R07NqBuildSentinel)<>"R07_NQ_BUILD_SHELL_PASS\n" then
    Error("R07_NQ: configure/make failed before exact sentinel");
  fi;
  R07NqBuilt:=true;;
  R07NqExecutable:=Filename(DirectoriesPackagePrograms("nq"),"nq");;
fi;
if R07NqExecutable=fail then
  Error("R07_NQ: NQ executable unavailable after bootstrap");
fi;
if LoadPackage("nq")<>true then
  Error("R07_NQ: pinned NQ failed to load after bootstrap");
fi;
R07NqLoadedInfos:=PackageInfo("nq");;
if Length(R07NqLoadedInfos)<>1 or
   R07NqLoadedInfos[1].Version<>R07NqVersion then
  Error("R07_NQ: loaded NQ version pin failed");
fi;
Print("R07_NQ_BOOTSTRAP_PASS gap_version=",GAPInfo.Version,
  " nq_version=",R07NqVersion," built=",R07NqBuilt,
  " gap_root=",R07NqGapRoot," package_path=",R07NqPath,
  " executable=",R07NqExecutable,"\n");
SizeScreen([4096,0]);;

R07Class6StartRuntime:=Runtime();;
R07Tail5Signed:=[1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-2,1,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,-2,1,2,1,-2,-1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,1,-2,-1,2,-1,-2,1,2,-1,-2,-1,2,1,-2,1,2,1,-2,-1,2,1,-2,1,2,-1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,1,2,-1,-2,-1,2,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,-1,-1,2,1,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,-2,1,1,2,-1,-2,1,2,1,-2,-1,-1,2,1,1,2,-1,-2,-1,2,1,-2,-1,2,1,2,-1,-2,1,2,1,-2,-1,-1,-2,1,1,2,-1,-2,-1,2,1,-2,-1,-2,-1,2,1,2,-1,-2,1,2,1,-2,-1,-1,2,1,1,2,-1,-2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,2,1,-2,-1,-1,-2,1,1,2,-1,-2,-1,2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-1,-2,1,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,-2,1,2,1,2,-1,-2,1,-2,1,2,-1,2,1,-2,-1,-2,-1,2,1,2,-1,-2,1,-2,1,2,-1,2,1,-2,-1,-2,1,2,1,2,-1,-2,1,-2,-1,2,-1,2,1,-2,-1,-2,-1,2,1,2,-1,-2,1,-2,-1,-1];;
if Length(R07Tail5Signed)<>796 then Error("R07_C6: frozen tail length drift"); fi;
if HexSHA256(Concatenation("[",
     JoinStringsWithSeparator(List(R07Tail5Signed,String),","),"]"))<>
   "937ce63d85d9c6ab5e9dd5918e00ffd8348ba3ba8ba2def66aa3c98a8bc95c0e" then
  Error("R07_C6: frozen tail digest drift");
fi;
R07C5:=[313599,2,-1,-2,0,1];;
R07K5:=[2,-4,3,4,1,-2];;
R07ExpectedRhoD6DigestZ:=
  "c3d7a866e8a84d37339f235f589e796d37c3f29ad3a731fa3ad7629a16ba9640";;
R07ExpectedRhoD6DigestF3:=
  "b8afcc8960c020147a76b71bf9a3144f8ea5b6a8d659b84404f3f2f2d15292c2";;
R07ExpectedFrozenD6DigestZ:=
  "fadcfe12a1ba9d5d7aa1a6d4a4c2aa26aeb46aee4e537a7af5a810702c13480c";;

R07PaperComm:=function(a,b)
  return a*b*a^-1*b^-1;
end;

R07BuildF0:=function(x,y)
  local z,chi,p,q,T,V,S,W,D7,H0,H,A;
  z:=y^-1*x^-1;
  chi:=R07PaperComm(x,y)*R07PaperComm(y,z)^-1;
  p:=x^-1*y*x^-2*y^-1*x^-1;
  q:=x^-1*y^-1*x^-2*y*x^-1;
  T:=p*q*p^3;
  V:=function(a) return q^-a*T*q^a; end;
  S:=V(2);
  W:=p*V(1);
  D7:=q^4*V(5);
  H0:=V(4)*W*D7*T;
  H:=p^7*H0;
  A:=H^-1*T*H;
  return chi*R07PaperComm(A,S);
end;

R07IsLyndonWord:=function(w)
  local i;
  for i in [2..Length(w)] do
    if not w<w{[i..Length(w)]} then return false; fi;
  od;
  return true;
end;

R07LyndonWords:=function(k,n)
  return Filtered(Tuples([1..k],n),R07IsLyndonWord);
end;

R07LyndonGroupElement:=function(w,gens)
  local i,v;
  if Length(w)=1 then return gens[w[1]]; fi;
  for i in [2..Length(w)] do
    v:=w{[i..Length(w)]};
    if R07IsLyndonWord(v) then
      return R07PaperComm(
        R07LyndonGroupElement(w{[1..i-1]},gens),
        R07LyndonGroupElement(v,gens));
    fi;
  od;
  Error("R07_C6: no standard Lyndon factorization");
end;

R07WordLabel:=function(w,names)
  return Concatenation(List(w,i->names[i]));
end;

R07WordFromCoordinates:=function(identity,basis,coords)
  local out,i;
  if Length(basis)<>Length(coords) then Error("R07_C6: coordinate length"); fi;
  out:=identity;
  for i in [1..Length(coords)] do out:=out*basis[i]^coords[i]; od;
  return out;
end;

R07SignedWord:=function(w)
  return LetterRepAssocWord(w);
end;

R07SignedWordDigest:=function(w)
  local letters,blob;
  letters:=R07SignedWord(w);
  blob:=Concatenation("[",JoinStringsWithSeparator(List(letters,String),","),"]");
  return rec(length:=Length(letters),sha256:=HexSHA256(blob));
end;

R07StringListJson:=function(v)
  return Concatenation("[",
    JoinStringsWithSeparator(List(v,s->Concatenation("\"",s,"\"")),","),"]");
end;

R07IntVectorJson:=function(v)
  return Concatenation("[",JoinStringsWithSeparator(List(v,String),","),"]");
end;

R07IntMatrixJson:=function(M)
  return Concatenation("[",
    JoinStringsWithSeparator(List(M,R07IntVectorJson),","),"]");
end;

R07MatrixDigest:=function(rows,cols,M)
  local blob;
  blob:=Concatenation("{\"rows\":",R07StringListJson(rows),
    ",\"cols\":",R07StringListJson(cols),
    ",\"matrix\":",R07IntMatrixJson(M),"}");
  return HexSHA256(blob);
end;

# The frozen v1 receipt used json.dumps(...,sort_keys=True,separators=(',',':'))
# on keys rows/cols/matrix, hence canonical key order cols,matrix,rows.
R07FrozenMatrixDigest:=function(rows,cols,M)
  local blob;
  blob:=Concatenation("{\"cols\":",R07StringListJson(cols),
    ",\"matrix\":",R07IntMatrixJson(M),
    ",\"rows\":",R07StringListJson(rows),"}");
  return HexSHA256(blob);
end;

R07Mod3Matrix:=function(M)
  return List(M,row->List(row,x->x mod 3));
end;

R07RankMod3:=function(M)
  local F;
  F:=GF(3);
  return RankMat(List(M,row->List(row,x->(x mod 3)*One(F))));
end;

R07BuildConversion:=function(QG,basisElems,labels,tag,probe)
  local lcs,layer,pcp,d,basisSub,basisIndex,cols,active,rankv,
        relOrders,relVectors,i,j,carry,r,augCols,augMatrix,detAug,
        invAug,v,sol,coords,relCoeffs,recon,expected,allBasisRound,
        abinv,forwardSha,inverseSha;
  lcs:=LowerCentralSeries(QG);
  layer:=lcs[Length(lcs)-1];
  d:=Length(labels);
  if HirschLength(layer)<>d then
    Error("R07_C6: ",tag," Hirsch rank mismatch");
  fi;
  if not probe in layer or ForAny(basisElems,e->not e in layer) then
    Error("R07_C6: ",tag," basis/probe outside top LCS layer");
  fi;
  pcp:=Pcp(layer);
  basisSub:=Subgroup(layer,basisElems);
  basisIndex:=Index(layer,basisSub);
  cols:=List(basisElems,e->ExponentsByPcp(pcp,e));
  active:=Filtered([1..Length(pcp)],i->ForAny(cols,c->c[i]<>0));
  rankv:=RankMat(TransposedMat(cols));
  relOrders:=RelativeOrdersOfPcp(pcp);
  relVectors:=[];
  for i in [1..Length(pcp)] do
    if relOrders[i]<>0 then
      carry:=ExponentsByPcp(pcp,pcp[i]^relOrders[i]);
      r:=List([1..Length(pcp)],j->0);
      r[i]:=relOrders[i];
      r:=r-carry;
      Add(relVectors,r);
    fi;
  od;
  if Length(pcp)<>d+Length(relVectors) then
    Error("R07_C6: ",tag," power-relation count/Hirsch mismatch");
  fi;
  augCols:=Concatenation(cols,relVectors);
  augMatrix:=TransposedMat(augCols);
  if Length(augMatrix)<>Length(pcp) or
     ForAny(augMatrix,row->Length(row)<>Length(pcp)) then
    Error("R07_C6: ",tag," augmented matrix is not square");
  fi;
  detAug:=DeterminantMat(augMatrix);
  if detAug<>1 and detAug<>-1 then
    Error("R07_C6: ",tag," augmented change not unimodular");
  fi;
  invAug:=TransposedMat(augMatrix)^-1;
  v:=ExponentsByPcp(pcp,probe);
  sol:=SolutionMat(TransposedMat(augMatrix),v);
  if sol=fail or sol*TransposedMat(augMatrix)<>v then
    Error("R07_C6: ",tag," all-coordinate solve failed");
  fi;
  coords:=sol{[1..d]};
  relCoeffs:=sol{[d+1..Length(sol)]};
  recon:=R07WordFromCoordinates(One(layer),basisElems,coords);
  if recon<>probe then Error("R07_C6: ",tag," group roundtrip failed"); fi;
  allBasisRound:=true;
  for j in [1..d] do
    sol:=SolutionMat(TransposedMat(augMatrix),cols[j]);
    expected:=List([1..Length(pcp)],i->0);
    expected[j]:=1;
    if sol<>expected then allBasisRound:=false; break; fi;
  od;
  if not allBasisRound then
    Error("R07_C6: ",tag," basis-unit all-coordinate roundtrip failed");
  fi;
  abinv:=AbelianInvariants(layer);
  if Length(abinv)<>d or ForAny(abinv,a->a<>0) then
    Error("R07_C6: ",tag," top layer is not free abelian of expected rank");
  fi;
  if basisIndex<>1 or rankv<>d then
    Error("R07_C6: ",tag," basis index/rank failure");
  fi;
  forwardSha:=HexSHA256(R07IntMatrixJson(augMatrix));
  inverseSha:=HexSHA256(R07IntMatrixJson(invAug));
  Print(tag,"_CONVERSION rank=",d," pcp_length=",Length(pcp),
    " relation_count=",Length(relVectors)," det=",detAug,
    " index=",basisIndex," abinv=",abinv," active=",active,"\n");
  Print(tag,"_POWER_RELATIONS=",relVectors,"\n");
  Print(tag,"_FORWARD_MATRIX=",augMatrix,"\n");
  Print(tag,"_FORWARD_SHA256=",forwardSha,
    " INVERSE_SHA256=",inverseSha,
    " ALL_BASIS_COORD_ROUNDTRIP=",allBasisRound,
    " PROBE_GROUP_ROUNDTRIP=",recon=probe,"\n");
  Print(tag,"_BASIS_LABELS=",labels,"\n");
  return rec(layer:=layer,pcp:=pcp,d:=d,basisElems:=basisElems,
    labels:=labels,cols:=cols,relVectors:=relVectors,augCols:=augCols,
    augMatrix:=augMatrix,inverse:=invAug,det:=detAug,index:=basisIndex,
    forwardSha:=forwardSha,inverseSha:=inverseSha);
end;

R07Coordinates:=function(conv,defect,tag)
  local v,sol,coords,relCoeffs,recon,allCoord;
  if not defect in conv.layer then
    Error("R07_C6: ",tag," defect outside gamma6 layer");
  fi;
  v:=ExponentsByPcp(conv.pcp,defect);
  sol:=SolutionMat(TransposedMat(conv.augMatrix),v);
  if sol=fail then Error("R07_C6: ",tag," coordinate solve failed"); fi;
  allCoord:=sol*TransposedMat(conv.augMatrix)=v;
  coords:=sol{[1..conv.d]};
  relCoeffs:=sol{[conv.d+1..Length(sol)]};
  recon:=R07WordFromCoordinates(One(conv.layer),conv.basisElems,coords);
  Print(tag,"_COORDS=",coords," RELATION_COEFFS=",relCoeffs,
    " ALL_COORD_ROUNDTRIP=",allCoord,
    " GROUP_ROUNDTRIP=",recon=defect,"\n");
  if not allCoord or recon<>defect then
    Error("R07_C6: ",tag," coordinate/group roundtrip failed");
  fi;
  return coords;
end;

R07DirectSumPerm:=function(perms,sizes)
  local total,map,offset,i,j;
  if Length(perms)<>Length(sizes) then Error("R07_C6: block mismatch"); fi;
  total:=Sum(sizes);
  map:=[1..total];
  offset:=0;
  for i in [1..Length(perms)] do
    for j in [1..sizes[i]] do map[offset+j]:=offset+(j^perms[i]); od;
    offset:=offset+sizes[i];
  od;
  return PermList(map);
end;

R07BuildMarkedQ:=function(F2,x,y)
  local r,s,gx,gy,px,py,c3,qx,qy,Q,qmap,r07g,r07q,gammas,
        expectedOrders,i,f0mark;
  r:=PermList(Concatenation([2..36],[1]));
  s:=PermList(List([0..35],a->((-a) mod 36)+1));
  gx:=R07DirectSumPerm([r,s,s],[36,36,36]);
  gy:=R07DirectSumPerm([r*s,r,r*s],[36,36,36]);
  px:=PermList([8,5,2,1,9,7,4,3,6]);
  py:=PermList([2,6,7,5,8,4,1,9,3]);
  c3:=PermList([2,3,1]);
  qx:=R07DirectSumPerm([gx,px,c3^2],[108,9,3]);
  qy:=R07DirectSumPerm([gy,py,c3^2],[108,9,3]);
  Q:=Group(qx,qy);
  if Size(Group(gx,gy))<>23328 or Size(Group(px,py))<>504 or
     Size(Q)<>35271936 then
    Error("R07_C6: finite marked quotient order calibration failed");
  fi;
  qmap:=GroupHomomorphismByImages(F2,Q,[x,y],[qx,qy]);
  if qmap=fail then Error("R07_C6: finite mark map failed"); fi;
  r07g:=R07DirectSumPerm([r^4,r^32,()],[36,36,36]);
  r07q:=R07DirectSumPerm([r07g,(),()],[108,9,3]);
  f0mark:=Image(qmap,R07BuildF0(x,y));
  if f0mark<>r07q then Error("R07_C6: f0 finite mark is not R07"); fi;
  gammas:=[Q];
  for i in [2..7] do Add(gammas,CommutatorSubgroup(gammas[i-1],Q)); od;
  expectedOrders:=[35271936,734832,367416,367416,367416,367416,367416];
  if List(gammas,Size)<>expectedOrders then
    Error("R07_C6: finite Q lower-central orders drift");
  fi;
  Print("R07_FINITE_Q_PASS orders=",expectedOrders,
    " f0_mark_R07=true degree=120\n");
  return rec(Q:=Q,x:=qx,y:=qy,map:=qmap,r07:=r07q,gammas:=gammas,
    g36x:=gx,g36y:=gy,pslx:=px,psly:=py,c3:=c3);
end;

R07BuildExactifierData:=function(mark,F2,x,y,weight)
  local target,seedWords,queueWords,queueImages,known,seen,selectedWords,
        selectedImages,selected,selectedSize,pos,w,img,actions,a,newWord,
        newImage,Fsel,epi,expectedSize;
  if weight<3 or weight>7 then Error("R07_C6: exactifier weight"); fi;
  target:=mark.gammas[weight];
  expectedSize:=367416;
  if Size(target)<>expectedSize then Error("R07_C6: exactifier target size"); fi;
  seedWords:=List(R07LyndonWords(2,weight),
    z->R07LyndonGroupElement(z,[x,y]));
  queueWords:=ShallowCopy(seedWords);
  queueImages:=List(queueWords,w->Image(mark.map,w));
  known:=ShallowCopy(queueImages);
  seen:=[];
  selectedWords:=[];
  selectedImages:=[];
  selected:=Group([One(mark.Q)]);
  selectedSize:=1;
  actions:=[
    rec(q:=mark.x,w:=x),rec(q:=mark.y,w:=y),
    rec(q:=mark.x^-1,w:=x^-1),rec(q:=mark.y^-1,w:=y^-1)
  ];
  pos:=1;
  while selectedSize<expectedSize do
    if pos>Length(queueWords) then
      Error("R07_C6: exactifier conjugacy orbit exhausted");
    fi;
    w:=queueWords[pos];
    img:=queueImages[pos];
    pos:=pos+1;
    if Position(seen,img)=fail then
      Add(seen,img);
      if not img in target then
        Error("R07_C6: exactifier seed/conjugate outside target gamma");
      fi;
      if not img in selected then
        Add(selectedWords,w);
        Add(selectedImages,img);
        selected:=Group(selectedImages);
        selectedSize:=Size(selected);
      fi;
      if selectedSize<expectedSize then
        for a in actions do
          newWord:=w^(a.w);
          newImage:=img^(a.q);
          if Position(known,newImage)=fail then
            Add(known,newImage);
            Add(queueWords,newWord);
            Add(queueImages,newImage);
          fi;
        od;
      fi;
    fi;
    if Length(queueWords)>200000 then
      Error("R07_C6: exactifier orbit safety cap");
    fi;
  od;
  if Size(selected)<>Size(target) or
     ForAny(GeneratorsOfGroup(target),g->not g in selected) then
    Error("R07_C6: tracked exactifier generators do not equal target gamma");
  fi;
  Fsel:=FreeGroup(Length(selectedImages));
  epi:=GroupHomomorphismByImages(Fsel,selected,GeneratorsOfGroup(Fsel),
    selectedImages);
  if epi=fail then Error("R07_C6: exactifier tracked epimorphism failed"); fi;
  Print("R07_EXACTIFIER_DATA weight=",weight,
    " seed_count=",Length(seedWords),
    " visited_count=",Length(seen),
    " selected_count=",Length(selectedImages),
    " target_order=",Size(target),"\n");
  return rec(weight:=weight,target:=target,selected:=selected,
    sourceWords:=selectedWords,images:=selectedImages,free:=Fsel,epi:=epi);
end;

R07ExactifyRawWord:=function(mark,data,raw,label)
  local rawImage,pre,lift,exact,rawDigest,liftDigest,exactDigest;
  rawImage:=Image(mark.map,raw);
  if not rawImage in data.target then
    Error("R07_C6: ",label," raw mark outside exactifier target");
  fi;
  pre:=PreImagesRepresentative(data.epi,rawImage);
  if pre=fail then Error("R07_C6: ",label," finite preimage failed"); fi;
  lift:=MappedWord(pre,GeneratorsOfGroup(data.free),data.sourceWords);
  if Image(mark.map,lift)<>rawImage then
    Error("R07_C6: ",label," tracked lift mark mismatch");
  fi;
  exact:=raw*lift^-1;
  if Image(mark.map,exact)<>One(mark.Q) then
    Error("R07_C6: ",label," exactified mark is nontrivial");
  fi;
  rawDigest:=R07SignedWordDigest(raw);
  liftDigest:=R07SignedWordDigest(lift);
  exactDigest:=R07SignedWordDigest(exact);
  Print(label,"_EXACTIFIER raw_mark_order=",Order(rawImage),
    " raw_word_length=",rawDigest.length,
    " raw_word_sha256=",rawDigest.sha256,
    " tail_weight=",data.weight,
    " tail_word_length=",liftDigest.length,
    " tail_word_sha256=",liftDigest.sha256,
    " exact_word_length=",exactDigest.length,
    " exact_word_sha256=",exactDigest.sha256,
    " exact_mark_identity=true\n");
  return rec(raw:=raw,rawImage:=rawImage,tail:=lift,exact:=exact,
    rawDigest:=rawDigest,tailDigest:=liftDigest,exactDigest:=exactDigest);
end;

R07SourceDefects:=function(word,epi,F2,x,y)
  local f,ft,fa,fb;
  f:=Image(epi,word);
  ft:=Image(epi,MappedWord(word,[x,y],[y,x]));
  fa:=Image(epi,MappedWord(word,[x,y],[y,y^-1*x^-1]));
  fb:=Image(epi,MappedWord(word,[x,y],[y^-1*x^-1,x]));
  return rec(theta:=f*ft,tau:=fb*fa*f);
end;

R07LiteralCofaces:=function(word,epiK,F2,x,y,kg)
  local Eval,p123,p234,p1_23_4,p12_3_4,p1_2_34,base,sign,drop,swap;
  Eval:=function(a,b)
    return Image(epiK,MappedWord(word,[x,y],[a,b]));
  end;
  p123:=Eval(kg[1],kg[4]);
  p234:=Eval(kg[4],kg[6]);
  p1_23_4:=Eval(kg[1]*kg[2],kg[5]*kg[6]);
  p12_3_4:=Eval(kg[2]*kg[4],kg[6]);
  p1_2_34:=Eval(kg[1],kg[4]*kg[5]);
  base:=p12_3_4^-1*p1_2_34^-1*p234*p1_23_4*p123;
  sign:=p12_3_4*p1_2_34^-1*p234*p1_23_4*p123;
  drop:=p12_3_4^-1*p1_2_34^-1*p1_23_4*p123;
  swap:=p12_3_4^-1*p1_2_34^-1*p1_23_4*p234*p123;
  return rec(base:=base,sign:=sign,drop:=drop,swap:=swap,
    factors:=[p12_3_4,p1_2_34,p234,p1_23_4,p123]);
end;

R07RhoNorm:=function(word,epiK,F2,x,y,kg,rho)
  local f,r1,r2,r3,r4;
  f:=MappedWord(word,[x,y],[kg[1],kg[4]]);
  r1:=Image(rho,f); r2:=Image(rho,r1); r3:=Image(rho,r2);
  r4:=Image(rho,r3);
  return Image(epiK,r4*r3*r2*r1*f);
end;

R07BuildK05:=function()
  local FB,s1,s2,s3,B4,bg,S4,bh,PB,x12,x13,x14,x23,x24,x34,
        pg,Pmark,iso,Kfp,delta,dc,K05,kg,rhoim,rho;
  FB:=FreeGroup("s1","s2","s3");
  s1:=FB.1; s2:=FB.2; s3:=FB.3;
  B4:=FB/[s1*s2*s1*(s2*s1*s2)^-1,
          s2*s3*s2*(s3*s2*s3)^-1,Comm(s1,s3)];
  bg:=GeneratorsOfGroup(B4); s1:=bg[1]; s2:=bg[2]; s3:=bg[3];
  S4:=SymmetricGroup(4);
  bh:=GroupHomomorphismByImages(B4,S4,bg,[(1,2),(2,3),(3,4)]);
  PB:=Kernel(bh);
  x12:=s1^2; x23:=s2^2; x34:=s3^2;
  x13:=s2*s1^2*s2^-1; x24:=s3*s2^2*s3^-1;
  x14:=s3*x13*s3^-1;
  pg:=[x12,x13,x14,x23,x24,x34];
  Pmark:=Subgroup(B4,pg);
  if Index(B4,PB)<>24 or Pmark<>PB then Error("R07_C6: PB4 calibration"); fi;
  iso:=IsomorphismFpGroupByGenerators(Pmark,pg);
  Kfp:=Image(iso);
  delta:=(s1*s2*s3)^4;
  dc:=Image(iso,delta);
  K05:=Kfp/[dc];
  kg:=GeneratorsOfGroup(K05);
  if Length(RelatorsOfFpGroup(K05))<>18 or
     AbelianInvariants(K05)<>[0,0,0,0,0] then
    Error("R07_C6: K05 presentation calibration");
  fi;
  rhoim:=[(kg[3]*kg[5]*kg[6])^-1,kg[3],kg[5],
          (kg[1]*kg[2]*kg[3])^-1,
          (kg[1]*kg[4]*kg[5])^-1,kg[1]];
  rho:=GroupHomomorphismByImagesNC(K05,K05,kg,rhoim);
  Print("R07_K05_CALIBRATION_PASS relators=18 abinv=[0,0,0,0,0]\n");
  return rec(group:=K05,gens:=kg,rho:=rho);
end;

R07CoordinateRecord:=function(conv,defect)
  local v,sol,coords,relCoeffs,recon,allCoord;
  if not defect in conv.layer then return fail; fi;
  v:=ExponentsByPcp(conv.pcp,defect);
  sol:=SolutionMat(TransposedMat(conv.augMatrix),v);
  if sol=fail then return fail; fi;
  allCoord:=sol*TransposedMat(conv.augMatrix)=v;
  coords:=sol{[1..conv.d]};
  relCoeffs:=sol{[conv.d+1..Length(sol)]};
  recon:=R07WordFromCoordinates(One(conv.layer),conv.basisElems,coords);
  if not allCoord or recon<>defect then return fail; fi;
  return rec(coords:=coords,relations:=relCoeffs,normal:=v);
end;

R07CollectBeta:=function(word,epiF,F2,x,y,convF,epiK,kg,convK,tag)
  local sd,cf,tc,uc,pc,out;
  sd:=R07SourceDefects(word,epiF,F2,x,y);
  cf:=R07LiteralCofaces(word,epiK,F2,x,y,kg);
  tc:=R07CoordinateRecord(convF,sd.theta);
  uc:=R07CoordinateRecord(convF,sd.tau);
  pc:=R07CoordinateRecord(convK,cf.base);
  if tc=fail or uc=fail or pc=fail then
    Error("R07_C6: ",tag," beta coordinate collection failed");
  fi;
  out:=Concatenation(tc.coords,uc.coords,pc.coords);
  if Length(out)<>143 then Error("R07_C6: ",tag," beta row count"); fi;
  Print(tag,"_THETA6=",tc.coords,"\n");
  Print(tag,"_TAU6=",uc.coords,"\n");
  Print(tag,"_LITERAL_A18_6=",pc.coords,"\n");
  Print(tag,"_BETA6=",out,"\n");
  return rec(vector:=out,source:=sd,cofaces:=cf,
    theta:=tc,tau:=uc,pent:=pc);
end;

R07CanonicalMinorMod3:=function(M)
  local M3,selected,selectedRows,i,cand,minor;
  M3:=R07Mod3Matrix(M);
  selected:=[];
  selectedRows:=[];
  for i in [1..Length(M)] do
    cand:=Concatenation(selectedRows,[M3[i]]);
    if R07RankMod3(cand)>Length(selectedRows) then
      Add(selected,i);
      Add(selectedRows,M3[i]);
      if Length(selected)=Length(M[1]) then break; fi;
    fi;
  od;
  if Length(selected)<>Length(M[1]) then
    Error("R07_C6: canonical minor rank failure");
  fi;
  minor:=M{selected};
  return rec(rows:=selected,matrix:=minor,det:=DeterminantMat(minor));
end;

R07SmithAnalyze:=function(A,b,label,requireSolution)
  local snf,U,V,D,rank,n,m,diag,c,solvable,i,d,y,z,kernel,
        vec,detU,detV,transformOk,diagOk,divOk,zeroOk,divisibilityOk,
        uSha,vSha,dSha;
  m:=Length(A);
  n:=Length(A[1]);
  if Length(b)<>m or ForAny(A,row->Length(row)<>n) then
    Error("R07_C6: ",label," Smith shape mismatch");
  fi;
  snf:=SmithNormalFormIntegerMatTransforms(A);
  U:=snf.rowtrans; V:=snf.coltrans; D:=snf.normal; rank:=snf.rank;
  transformOk:=U*A*V=D;
  detU:=DeterminantMat(U); detV:=DeterminantMat(V);
  if not transformOk or AbsInt(detU)<>1 or AbsInt(detV)<>1 then
    Error("R07_C6: ",label," Smith transform receipt failed");
  fi;
  diag:=List([1..Minimum(m,n)],i->D[i][i]);
  diagOk:=true;
  for i in [1..m] do
    if ForAny([1..n],j->i<>j and D[i][j]<>0) then diagOk:=false; break; fi;
  od;
  divOk:=true;
  for i in [1..rank-1] do
    if diag[i]=0 or diag[i+1] mod diag[i]<>0 then divOk:=false; break; fi;
  od;
  if not diagOk or not divOk then Error("R07_C6: ",label," Smith diagonal"); fi;
  c:=U*b;
  divisibilityOk:=true;
  for i in [1..rank] do
    if c[i] mod D[i][i]<>0 then divisibilityOk:=false; break; fi;
  od;
  if rank<m then
    zeroOk:=ForAll([rank+1..m],i->c[i]=0);
  else
    zeroOk:=true;
  fi;
  solvable:=divisibilityOk and zeroOk;
  y:=List([1..n],i->0);
  z:=fail;
  if solvable then
    for i in [1..rank] do y[i]:=c[i]/D[i][i]; od;
    z:=V*y;
    if A*z<>b then Error("R07_C6: ",label," Smith solution replay failed"); fi;
  fi;
  kernel:=[];
  if rank<n then
    for i in [rank+1..n] do
      vec:=List([1..n],j->V[j][i]);
      if A*vec<>List([1..m],j->0) then
        Error("R07_C6: ",label," kernel replay failed");
      fi;
      Add(kernel,vec);
    od;
  fi;
  uSha:=HexSHA256(R07IntMatrixJson(U));
  vSha:=HexSHA256(R07IntMatrixJson(V));
  dSha:=HexSHA256(R07IntMatrixJson(D));
  Print(label,"_SMITH rank=",rank," factors=",diag{[1..rank]},
    " solvable=",solvable," detU=",detU," detV=",detV,
    " U_SHA256=",uSha," V_SHA256=",vSha," D_SHA256=",dSha,"\n");
  Print(label,"_SMITH_TRANSFORM_REPLAY=",transformOk,
    " solution=",z," kernel_basis=",kernel,"\n");
  if requireSolution and not solvable then
    Error("R07_C6: ",label," NO_INTEGER_SOLUTION integrity stop");
  fi;
  return rec(U:=U,V:=V,D:=D,rank:=rank,factors:=diag{[1..rank]},
    transformedRhs:=c,solvable:=solvable,solution:=z,kernel:=kernel,
    uSha:=uSha,vSha:=vSha,dSha:=dSha);
end;

R07WordFromSigned:=function(F2,x,y,letters)
  local out,a;
  out:=One(F2);
  for a in letters do
    if a=1 then out:=out*x;
    elif a=-1 then out:=out*x^-1;
    elif a=2 then out:=out*y;
    elif a=-2 then out:=out*y^-1;
    else Error("R07_C6: signed letter outside F2"); fi;
  od;
  return out;
end;

R07ExponentSums:=function(word,x,y)
  return [ExponentSumWord(word,x),ExponentSumWord(word,y)];
end;

R07Class6Main:=function()
  local S,i,j,t,tw,sd,cf,solved,markOk,betaEntries,entry,bm1,b0,b1,b2,
        delta,affineOk,h,tc,uc,pc,rc,literalCols,rhoCols,literalM,rhoM,
        literalRankQ,literalRankF3,rhoDigestZ,rhoDigestF3,rowLabels,
        sourceLabels,targetLabels,minor,augCols,augMatrix,rhs,smith,
        tSol,c6coords,rawC6,exact6,f6,finalSource,finalCofaces,
        expSums,finalMark,ontoY,ontoHom,ontoOk,mutSign,mutDrop,mutSwap,
        swapCols,tmp,swapMatrix,swapSha,fnSwapDetected,dropCols,dropMatrix,
        powerDropDetected,t0Smith,t0Label,finalDigest,sourceExpectedTheta,
        sourceExpectedTau,rho5ok,z,kword,zero143,equationReplay,
        frozenDigest,calSourceLabels,calRowLabels,qfGens,qfWord,
        ontoQF;

  S:=rec();
  S.F2:=FreeGroup("x","y");
  S.x:=S.F2.1; S.y:=S.F2.2;
  S.lw5:=R07LyndonWords(2,5);
  S.lb5:=List(S.lw5,w->R07LyndonGroupElement(w,[S.x,S.y]));
  if Length(S.lb5)<>6 then Error("R07_C6: source degree5 rank"); fi;
  S.f0:=R07BuildF0(S.x,S.y);
  S.rawC5:=R07WordFromCoordinates(One(S.F2),S.lb5,R07C5);
  S.tail5:=R07WordFromSigned(S.F2,S.x,S.y,R07Tail5Signed);
  S.f5:=S.f0*S.rawC5*S.tail5;

  S.mark:=R07BuildMarkedQ(S.F2,S.x,S.y);
  if Image(S.mark.map,S.f5)<>S.mark.r07 then
    Error("R07_C6: frozen f5 exact mark failed");
  fi;
  S.rawK:=R07WordFromCoordinates(One(S.F2),S.lb5,R07K5);
  S.exactifier6:=R07BuildExactifierData(S.mark,S.F2,S.x,S.y,6);
  S.kExact:=R07ExactifyRawWord(S.mark,S.exactifier6,S.rawK,
    "R07_KERNEL_K5");
  S.wk:=S.kExact.exact;
  if Image(S.mark.map,S.wk)<>One(S.mark.Q) then
    Error("R07_C6: wk exact finite mark");
  fi;
  Print("R07_CLASS6_EXACTIFIER5_PASS k=",R07K5,
    " wk_sha256=",S.kExact.exactDigest.sha256,"\n");

  S.epiF:=NqEpimorphismNilpotentQuotient(S.F2,6);
  S.QF:=Image(S.epiF);
  S.lcsF:=LowerCentralSeries(S.QF);
  if HirschLength(S.lcsF[6])<>9 then
    Error("R07_C6: source gamma6 rank");
  fi;
  S.lw6:=R07LyndonWords(2,6);
  S.lb6:=List(S.lw6,w->R07LyndonGroupElement(w,[S.x,S.y]));
  S.lb6Q:=List(S.lb6,w->Image(S.epiF,w));
  S.sourceLabels:=List(S.lw6,w->R07WordLabel(w,["x","y"]));
  if Length(S.lb6)<>9 then Error("R07_C6: degree6 source basis rank"); fi;

  S.k05:=R07BuildK05();
  S.K05:=S.k05.group; S.kg:=S.k05.gens; S.rho:=S.k05.rho;
  S.epiK:=NqEpimorphismNilpotentQuotient(S.K05,6);
  S.QK:=Image(S.epiK);
  S.lcsK:=LowerCentralSeries(S.QK);
  if HirschLength(S.lcsK[6])<>125 then
    Error("R07_C6: K05 gamma6 rank is not 125");
  fi;
  Print("R07_CLASS6_NQ_CALIBRATION source_hirsch=",HirschLength(S.QF),
    " source_lcs=",List(S.lcsF,HirschLength),
    " K05_hirsch=",HirschLength(S.QK),
    " K05_lcs=",List(S.lcsK,HirschLength),"\n");

  rho5ok:=true;
  for i in [1..6] do
    z:=S.kg[i];
    for j in [1..5] do z:=Image(S.rho,z); od;
    if Image(S.epiK,z)<>Image(S.epiK,S.kg[i]) then rho5ok:=false; fi;
  od;
  if not rho5ok then Error("R07_C6: rho^5 convention gate"); fi;

  # The full C5+t*k family must remain solved through degree five.  In the
  # class-six quotient this is exactly membership of every defect in gamma6.
  for t in [0,1,-1] do
    tw:=S.f5*S.wk^t;
    sd:=R07SourceDefects(tw,S.epiF,S.F2,S.x,S.y);
    cf:=R07LiteralCofaces(tw,S.epiK,S.F2,S.x,S.y,S.kg);
    solved:=(sd.theta in S.lcsF[6]) and (sd.tau in S.lcsF[6]) and
            (cf.base in S.lcsK[6]);
    markOk:=Image(S.mark.map,tw)=S.mark.r07;
    Print("R07_CLASS5_FAMILY_GATE t=",t," solved_through_degree5=",solved,
      " exact_R07_mark=",markOk,"\n");
    if not solved or not markOk then Error("R07_C6: C5+t*k family gate"); fi;
  od;

  # Genuine FN split n=(x14,x24,x34), h=(x12,x23).
  S.lwN:=R07LyndonWords(3,6);
  S.lwH:=R07LyndonWords(2,6);
  if Length(S.lwN)<>116 or Length(S.lwH)<>9 then
    Error("R07_C6: FN target ranks");
  fi;
  S.lbNQ:=List(S.lwN,w->Image(S.epiK,
    R07LyndonGroupElement(w,[S.kg[3],S.kg[5],S.kg[6]])));
  S.lbHQ:=List(S.lwH,w->Image(S.epiK,
    R07LyndonGroupElement(w,[S.kg[1],S.kg[4]])));
  S.targetBasis:=Concatenation(S.lbNQ,S.lbHQ);
  S.targetLabels:=Concatenation(
    List(S.lwN,w->Concatenation("n:",R07WordLabel(w,["A","B","C"]))),
    List(S.lwH,w->Concatenation("h:",R07WordLabel(w,["X","Y"]))));

  tw:=S.f5;
  sd:=R07SourceDefects(tw,S.epiF,S.F2,S.x,S.y);
  cf:=R07LiteralCofaces(tw,S.epiK,S.F2,S.x,S.y,S.kg);
  S.convF:=R07BuildConversion(S.QF,S.lb6Q,S.sourceLabels,
    "R07_SOURCE_GAMMA6",sd.theta);
  S.convK:=R07BuildConversion(S.QK,S.targetBasis,S.targetLabels,
    "R07_K05_GAMMA6",cf.base);

  # The frozen homogeneous rho calibration used the cyclic fibre
  # (x15,x25,x35), whereas the load-bearing literal solve above uses the v10
  # FN fibre (x14,x24,x34).  Build the former as a separate diagnostic
  # unimodular basis; never feed it into beta6 or the augmented solve.
  S.rhoCalN:=[(S.kg[1]*S.kg[2]*S.kg[3])^-1,
              (S.kg[1]*S.kg[4]*S.kg[5])^-1,
              (S.kg[2]*S.kg[4]*S.kg[6])^-1];
  S.rhoCalBasis:=Concatenation(
    List(S.lwN,w->Image(S.epiK,R07LyndonGroupElement(w,S.rhoCalN))),
    S.lbHQ);
  S.rhoCalProbe:=R07RhoNorm(S.f5,S.epiK,S.F2,S.x,S.y,S.kg,S.rho);
  S.convRhoCal:=R07BuildConversion(S.QK,S.rhoCalBasis,S.targetLabels,
    "R07_K05_GAMMA6_RHO_CALIBRATION_ONLY",S.rhoCalProbe);

  betaEntries:=[];
  for t in [-1,0,1,2] do
    entry:=rec(t:=t,beta:=R07CollectBeta(S.f5*S.wk^t,S.epiF,S.F2,
      S.x,S.y,S.convF,S.epiK,S.kg,S.convK,
      Concatenation("R07_BETA_T",String(t))));
    Add(betaEntries,entry);
  od;
  bm1:=First(betaEntries,e->e.t=-1).beta;
  b0:=First(betaEntries,e->e.t=0).beta;
  b1:=First(betaEntries,e->e.t=1).beta;
  b2:=First(betaEntries,e->e.t=2).beta;
  delta:=b1.vector-b0.vector;
  affineOk:=(bm1.vector=b0.vector-delta) and
            (b2.vector=b0.vector+2*delta);
  if not affineOk then Error("R07_C6: literal affine t interpolation failed"); fi;
  sourceExpectedTheta:=
    [-20748807,-156803,-188152,0,0,-10,156803,501758,20748807];
  sourceExpectedTau:=
    [-41654405,83308810,-63093121,-124963215,-83308804,
      104747532,83308810,104747526,-41654405];
  if b0.theta.coords<>sourceExpectedTheta or
     b0.tau.coords<>sourceExpectedTau then
    Error("R07_C6: independently pinned source beta6_0 drift");
  fi;
  Print("R07_DELTA6=",delta,"\n");
  Print("R07_CLASS6_AFFINE_PASS rows=143 t_values=[-1,0,1,2]",
    " beta_linear=true\n");

  # Derive all nine homogeneous columns directly.  Literal A.18 is used for
  # the solve; rho is a diagnostic calibration only.
  literalCols:=[]; rhoCols:=[];
  for j in [1..9] do
    h:=S.lb6[j];
    sd:=R07SourceDefects(h,S.epiF,S.F2,S.x,S.y);
    cf:=R07LiteralCofaces(h,S.epiK,S.F2,S.x,S.y,S.kg);
    tc:=R07CoordinateRecord(S.convF,sd.theta);
    uc:=R07CoordinateRecord(S.convF,sd.tau);
    pc:=R07CoordinateRecord(S.convK,cf.base);
    rc:=R07CoordinateRecord(S.convRhoCal,
      R07RhoNorm(h,S.epiK,S.F2,S.x,S.y,S.kg,S.rho));
    if tc=fail or uc=fail or pc=fail or rc=fail then
      Error("R07_C6: D6 column conversion failed at ",j);
    fi;
    Add(literalCols,Concatenation(tc.coords,uc.coords,pc.coords));
    Add(rhoCols,Concatenation(tc.coords,uc.coords,rc.coords));
  od;
  literalM:=TransposedMat(literalCols);
  rhoM:=TransposedMat(rhoCols);
  if Length(literalM)<>143 or Length(rhoM)<>143 or
     ForAny(literalM,row->Length(row)<>9) then
    Error("R07_C6: D6 matrix shape");
  fi;
  literalRankQ:=RankMat(literalM);
  literalRankF3:=R07RankMod3(literalM);
  rowLabels:=Concatenation(
    List(S.sourceLabels,z->Concatenation("theta:",z)),
    List(S.sourceLabels,z->Concatenation("tau:",z)),
    List(S.targetLabels,z->Concatenation("pent:",z)));
  sourceLabels:=S.sourceLabels;
  targetLabels:=S.targetLabels;
  rhoDigestZ:=R07MatrixDigest(rowLabels,sourceLabels,rhoM);
  rhoDigestF3:=R07MatrixDigest(rowLabels,sourceLabels,R07Mod3Matrix(rhoM));
  calSourceLabels:=List(S.lw6,w->Concatenation("h:",
    R07WordLabel(w,["X","Y"])));
  calRowLabels:=Concatenation(
    List(calSourceLabels,z->Concatenation("theta:",z)),
    List(calSourceLabels,z->Concatenation("tau:",z)),
    List(S.targetLabels,z->Concatenation("pent:",z)));
  frozenDigest:=R07FrozenMatrixDigest(calRowLabels,calSourceLabels,rhoM);
  minor:=R07CanonicalMinorMod3(rhoM);
  if RankMat(rhoM)<>9 or R07RankMod3(rhoM)<>9 or
     rhoDigestZ<>R07ExpectedRhoD6DigestZ or
     rhoDigestF3<>R07ExpectedRhoD6DigestF3 or
     frozenDigest<>R07ExpectedFrozenD6DigestZ or
     minor.rows<>[1,2,3,6,10,14,22,39,51] or minor.det<>-70 then
    Error("R07_C6: frozen homogeneous rho calibration mismatch");
  fi;
  if literalRankQ<>9 or literalRankF3<>9 then
    Error("R07_C6: literal D6 rank mismatch");
  fi;
  S.literalCols:=literalCols; S.literalM:=literalM;
  Print("R07_D6_RHO_CALIBRATION digest_Z=",rhoDigestZ,
    " digest_F3=",rhoDigestF3,
    " frozen_v1_digest_Z=",frozenDigest,
    " minor_rows_1based=",minor.rows," minor_det=",minor.det,"\n");
  Print("R07_D6_LITERAL rank_Q=",literalRankQ,
    " rank_F3=",literalRankF3,
    " digest_Z=",R07MatrixDigest(rowLabels,sourceLabels,literalM),
    " digest_F3=",R07MatrixDigest(rowLabels,sourceLabels,
      R07Mod3Matrix(literalM)),"\n");
  Print("R07_CLASS6_D6_CALIBRATION_PASS shape=143x9\n");

  augCols:=Concatenation([delta],literalCols);
  augMatrix:=TransposedMat(augCols);
  rhs:=List(b0.vector,x->-x);
  smith:=R07SmithAnalyze(augMatrix,rhs,"R07_AUGMENTED_D6",true);
  tSol:=smith.solution[1];
  c6coords:=smith.solution{[2..10]};
  equationReplay:=augMatrix*smith.solution=rhs;
  if not equationReplay then Error("R07_C6: augmented equation replay"); fi;
  Print("R07_AUGMENTED_SOLUTION t=",tSol," C6=",c6coords,
    " equation_replay=",equationReplay,
    " homogeneous_solution_lattice=",smith.kernel,"\n");
  Print("R07_CLASS6_AUGMENTED_SMITH_PASS\n");

  # Diagnostic mutation: falsely freeze t=0.  Either outcome is permitted,
  # but it is explicitly separated from the genuine augmented solve.
  t0Smith:=R07SmithAnalyze(literalM,rhs,"R07_FALSE_T0",false);
  if t0Smith.solvable then t0Label:="EXPECTED_INSTANCE_DEPENDENT_SOLVABLE";
  else t0Label:="EXPECTED_INSTANCE_DEPENDENT_UNSOLVABLE"; fi;
  Print("R07_MUTATION_FALSE_T0 result=",t0Label,"\n");

  rawC6:=R07WordFromCoordinates(One(S.F2),S.lb6,c6coords);
  S.exactifier7:=R07BuildExactifierData(S.mark,S.F2,S.x,S.y,7);
  exact6:=R07ExactifyRawWord(S.mark,S.exactifier7,rawC6,
    "R07_CORRECTION_C6");
  if not Image(S.epiF,S.kExact.tail) in S.lcsF[6] then
    Error("R07_C6: wk exactifier tail not in gamma6");
  fi;
  if not IsOne(Image(S.epiF,exact6.tail)) then
    Error("R07_C6: C6 exactifier tail not in gamma7");
  fi;
  f6:=S.f5*S.wk^tSol*exact6.exact;
  finalDigest:=R07SignedWordDigest(f6);
  if Image(S.mark.map,exact6.exact)<>One(S.mark.Q) or
     Image(S.mark.map,f6)<>S.mark.r07 then
    Error("R07_C6: final exact finite mark replay failed");
  fi;
  Print("R07_FINAL_F6 signed_length=",finalDigest.length,
    " signed_sha256=",finalDigest.sha256,"\n");
  Print("R07_CLASS6_EXACTIFIER6_PASS raw_C6=",c6coords,
    " exact_C6_sha256=",exact6.exactDigest.sha256,"\n");

  finalSource:=R07SourceDefects(f6,S.epiF,S.F2,S.x,S.y);
  finalCofaces:=R07LiteralCofaces(f6,S.epiK,S.F2,S.x,S.y,S.kg);
  if not IsOne(finalSource.theta) or not IsOne(finalSource.tau) or
     not IsOne(finalCofaces.base) then
    Error("R07_C6: final direct theta/tau/literal A18 replay failed");
  fi;
  expSums:=R07ExponentSums(f6,S.x,S.y);
  if expSums<>[0,0] then Error("R07_C6: final word not commutator"); fi;
  finalMark:=Image(S.mark.map,f6);
  ontoY:=finalMark^-1*S.mark.y*finalMark;
  ontoHom:=GroupHomomorphismByImages(S.mark.Q,S.mark.Q,
    [S.mark.x,S.mark.y],[S.mark.x,ontoY]);
  if ontoHom=fail then
    ontoOk:=false;
  else
    ontoOk:=Size(Image(ontoHom))=Size(S.mark.Q);
  fi;
  if not ontoOk then Error("R07_C6: onto side gate failed"); fi;
  qfGens:=GeneratorsOfGroup(S.QF);
  qfWord:=Image(S.epiF,f6);
  ontoQF:=Index(S.QF,Subgroup(S.QF,
    [qfGens[1],qfWord^-1*qfGens[2]*qfWord]))=1;
  if not ontoQF then Error("R07_C6: nilpotent source onto gate failed"); fi;
  Print("R07_DIRECT_RELATIONS theta_identity=true tau_identity=true",
    " literal_A18_identity=true exact_R07_mark=true exponent_sums=",expSums,
    " charming_unit=1 onto_Q=true onto_F2_class6=true\n");

  mutSign:=not IsOne(finalCofaces.sign);
  mutDrop:=not IsOne(finalCofaces.drop);
  mutSwap:=not IsOne(finalCofaces.swap);
  if not mutSign or not mutDrop or not mutSwap then
    Error("R07_C6: coface mutation failed to change direct receipt");
  fi;

  swapCols:=ShallowCopy(S.convK.augCols);
  tmp:=swapCols[1]; swapCols[1]:=swapCols[2]; swapCols[2]:=tmp;
  swapMatrix:=TransposedMat(swapCols);
  swapSha:=HexSHA256(R07IntMatrixJson(swapMatrix));
  fnSwapDetected:=swapSha<>S.convK.forwardSha;
  if not fnSwapDetected then Error("R07_C6: FN column-swap mutation inert"); fi;

  if Length(S.convK.relVectors)=0 then
    Error("R07_C6: no K05 power relation available for drop mutation");
  fi;
  dropCols:=S.convK.augCols{[1..Length(S.convK.augCols)-1]};
  dropMatrix:=TransposedMat(dropCols);
  powerDropDetected:=Length(dropMatrix[1])<Length(dropMatrix) or
                     RankMat(dropMatrix)<Length(dropMatrix);
  if not powerDropDetected then
    Error("R07_C6: dropped power-relation coordinate was not detected");
  fi;
  Print("R07_MUTATIONS coface_sign_changed=",mutSign,
    " coface_omission_changed=",mutDrop,
    " noninert_ordered_swap_changed=",mutSwap,
    " FN_column_swap_digest_changed=",fnSwapDetected,
    " power_relation_drop_detected=",powerDropDetected,
    " false_t0=",t0Label,"\n");
  Print("R07_CLASS6_DIRECT_LITERAL_PASS\n");

  Print("R07_CLASS6_RESOURCE runtime_ms=",Runtime()-R07Class6StartRuntime,
    " gasman=",GasmanStatistics(),"\n");
  Print("R07_CLASS6_FINAL_MARKER status=PASS\n");
end;

if IsBound(R07_CLASS6_SELFTEST_ONLY) and R07_CLASS6_SELFTEST_ONLY=true then
  Print("R07_CLASS6_SELFTEST_FINAL_MARKER status=PASS\n");
  QUIT_GAP(0);
fi;

R07Class6Main();
QUIT_GAP(0);
