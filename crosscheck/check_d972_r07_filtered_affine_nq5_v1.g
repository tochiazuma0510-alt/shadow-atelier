# crosscheck/check_d972_r07_filtered_affine_nq5_v1.g
#
# Independent GAP/NQ replay of the R07 literal filtered class-five repair.
# No producer script/helper is read or imported.  The only transported datum is
# the frozen 796-letter gamma_6 exactifying tail, embedded below as signed
# generator letters.  Its separately pinned canonical JSON SHA256 is
# 937ce63d85d9c6ab5e9dd5918e00ffd8348ba3ba8ba2def66aa3c98a8bc95c0e.
#
# GHA noninteractive driver (existing .github/workflows/gap-run.yml):
#   script: crosscheck/check_d972_r07_filtered_affine_nq5_v1.g
#   timeout_min: 90
#   with_pquot_packages: false
#   out_dir: ci/out
# Expected fail-closed markers, each exactly once on success:
#   R07_NQ_BOOTSTRAP_PASS
#   R07_NQ5_CROSSCHECK_SOURCE_PASS
#   R07_NQ5_CROSSCHECK_RAW_GATE_PASS
#   R07_NQ5_CROSSCHECK_BASIS_PASS
#   R07_NQ5_CROSSCHECK_LITERAL_PASS
#   R07_NQ5_CROSSCHECK_FINAL_MARKER status=PASS
# Absence of the final marker, or any "Error,"/"Syntax error:" diagnostic,
# is failure.  Expected wall time: 20--45 minutes on ubuntu-latest; timeout 90.
#
# Scope boundary: this script checks source theta/tau through class five,
# source degree-six residual coordinates, raw rho versus literal A.18 through
# class five, the genuine integral gamma_5 basis/carry, and the corrected
# literal rho/A.18 identities modulo gamma_6.  It does not assert an Ihara
# witness, fake certificate, or a degree-six K(0,5) pentagon result.

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
if IsBound(R07_NQ_BOOTSTRAP_ONLY) and R07_NQ_BOOTSTRAP_ONLY=true then
  Print("R07_NQ_BOOTSTRAP_ONLY_FINAL_MARKER status=PASS\n");
  QUIT_GAP(0);
fi;
SizeScreen([4096,0]);;
tailSigned:=[1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-2,1,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,-2,1,2,1,-2,-1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,1,-2,-1,2,-1,-2,1,2,-1,-2,-1,2,1,-2,1,2,1,-2,-1,2,1,-2,1,2,-1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,1,2,-1,-2,-1,2,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,-1,-1,2,1,1,2,-1,-2,1,2,1,-2,1,2,-1,-2,-1,2,1,-2,-1,2,-1,-2,1,2,1,-2,-1,2,-1,-2,-1,2,1,-2,-1,-2,1,1,2,-1,-2,1,2,1,-2,-1,-1,2,1,1,2,-1,-2,-1,2,1,-2,-1,2,1,2,-1,-2,1,2,1,-2,-1,-1,-2,1,1,2,-1,-2,-1,2,1,-2,-1,-2,-1,2,1,2,-1,-2,1,2,1,-2,-1,-1,2,1,1,2,-1,-2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,2,1,-2,-1,-1,-2,1,1,2,-1,-2,-1,2,1,-2,-1,2,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,1,2,1,2,-1,2,1,-2,-1,-2,1,2,-1,-2,1,-2,-1,-1,-2,1,1,2,-1,2,1,-2,-1,2,1,2,-1,-2,1,-2,-1,-2,-1,2,1,2,-1,2,1,-2,-1,-2,-2,1,2,1,2,-1,-2,1,-2,1,2,-1,2,1,-2,-1,-2,-1,2,1,2,-1,-2,1,-2,1,2,-1,2,1,-2,-1,-2,1,2,1,2,-1,-2,1,-2,-1,2,-1,2,1,-2,-1,-2,-1,2,1,2,-1,-2,1,-2,-1,-1];;
if Length(tailSigned)<>796 then Error("embedded gamma6 tail length drift"); fi;
Print("R07_NQ5_CROSSCHECK_START GAP=",GAPInfo.Version," tail_length=",Length(tailSigned),"\n");

PaperComm := function(a,b)
  return a*b*a^-1*b^-1;
end;

BuildF0 := function(x,y)
  local z,chi,p,q,T,V,S,W,D7,H0,H,A;
  z := y^-1*x^-1;
  chi := PaperComm(x,y)*PaperComm(y,z)^-1;
  p := x^-1*y*x^-2*y^-1*x^-1;
  q := x^-1*y^-1*x^-2*y*x^-1;
  T := p*q*p^3;
  V := function(a) return q^-a*T*q^a; end;
  S := V(2);
  W := p*V(1);
  D7 := q^4*V(5);
  H0 := V(4)*W*D7*T;
  H := p^7*H0;
  A := H^-1*T*H;
  return chi*PaperComm(A,S);
end;

IsLyndonWordLocal := function(w)
  local i;
  for i in [2..Length(w)] do
    if not w < w{[i..Length(w)]} then return false; fi;
  od;
  return true;
end;

LyndonWordsLocal := function(k,n)
  return Filtered(Tuples([1..k],n),IsLyndonWordLocal);
end;

LyndonGroupElementLocal := function(w,gens)
  local i,v;
  if Length(w)=1 then return gens[w[1]]; fi;
  for i in [2..Length(w)] do
    v:=w{[i..Length(w)]};
    if IsLyndonWordLocal(v) then
      return PaperComm(
        LyndonGroupElementLocal(w{[1..i-1]},gens),
        LyndonGroupElementLocal(v,gens));
    fi;
  od;
  Error("no standard Lyndon factorization");
end;

WordLabelLocal := function(w,names)
  return Concatenation(List(w,i->names[i]));
end;

ConvertAgainstBasis := function(QG,basisElems,labels,defect)
  local pcp,cols,active,M,d,rankv,v,coords,i,j,
        omit,keep,Btry,dtry,detList,lcs,layer,basisSub,basisIndex,
        relOrders,relVectors,carry,r,augCols,augMatrix,detAug,sol,
        relCoeffs,recon,invAug;
  lcs:=LowerCentralSeries(QG);
  layer:=lcs[Length(lcs)-1];
  if not defect in layer or ForAny(basisElems,e->not e in layer) then
    Error("basis/defect outside top lower-central layer");
  fi;
  pcp:=Pcp(layer);
  basisSub:=Subgroup(layer,basisElems);
  basisIndex:=Index(layer,basisSub);
  cols:=List(basisElems,e->ExponentsByPcp(pcp,e));
  active:=Filtered([1..Length(pcp)],i->ForAny(cols,c->c[i]<>0));
  M:=List(active,i->List(cols,c->c[i]));
  d:=Length(labels);
  rankv:=RankMat(M);
  detList:=[];;
  if Length(M)=d+1 then
    for omit in [1..Length(M)] do
      keep:=Filtered([1..Length(M)],i->i<>omit);
      Btry:=M{keep}; dtry:=DeterminantMat(Btry);
      Add(detList,[active[omit],dtry]);
    od;
  fi;
  if rankv<>d then Error("basis conversion rank failure"); fi;

  # Pcp(layer) may have a finite relative step even when layer itself is
  # torsion-free.  Exponent vectors then have carries and are not additive.
  # Present the abelian layer as Z^n modulo its explicit power-relation
  # vectors, append those relation columns, and solve the square integral
  # system.  A unimodular augmented matrix certifies a genuine Z-basis.
  relOrders:=RelativeOrdersOfPcp(pcp);
  relVectors:=[];;
  for i in [1..Length(pcp)] do
    if relOrders[i]<>0 then
      carry:=ExponentsByPcp(pcp,pcp[i]^relOrders[i]);
      r:=List([1..Length(pcp)],j->0);;
      r[i]:=relOrders[i];;
      r:=r-carry;
      Add(relVectors,r);
    fi;
  od;
  if Length(pcp)<>d+Length(relVectors) then
    Error("power-relation count does not match Hirsch rank");
  fi;
  augCols:=Concatenation(cols,relVectors);
  augMatrix:=TransposedMat(augCols);
  detAug:=DeterminantMat(augMatrix);
  invAug:=TransposedMat(augMatrix)^-1;
  v:=ExponentsByPcp(pcp,defect);
  sol:=SolutionMat(TransposedMat(augMatrix),v);
  if sol=fail then Error("augmented basis solve failure"); fi;
  coords:=sol{[1..d]};
  relCoeffs:=sol{[d+1..Length(sol)]};
  recon:=One(layer);
  for i in [1..d] do recon:=recon*basisElems[i]^coords[i]; od;
  Print("BASIS_LABELS=",labels,"\n");
  Print("TOP_LAYER_HIRSCH=",HirschLength(layer),
        " TOP_LAYER_PCP_RELATIVE_ORDERS=",RelativeOrdersOfPcp(pcp),
        " TOP_LAYER_ABINV=",AbelianInvariants(layer),
        " TOP_LAYER_IS_ABELIAN=",IsAbelian(layer),
        " BASIS_SUBGROUP_INDEX=",basisIndex,"\n");
  Print("PCP_ACTIVE_INDICES=",active,"\n");
  Print("PCP_ACTIVE_COUNT=",Length(active)," FULL_CHANGE_RANK=",rankv,"\n");
  if Length(detList)>0 then Print("RAW_NONADDITIVE_ALL_DELETE_ONE_MINORS=",detList,"\n"); fi;
  Print("PCP_POWER_RELATION_VECTORS=",relVectors,"\n");
  Print("AUGMENTED_CHANGE_DET=",detAug,"\n");
  Print("LYNDON_PLUS_REL_TO_PCP_MATRIX_ROWS=",augMatrix,"\n");
  Print("PCP_TO_LYNDON_PLUS_REL_MATRIX_ROWS=",invAug,"\n");
  Print("DEFECT_PCP_NORMAL_FORM=",v,"\n");
  Print("DEFECT_LYNDON_COORDS=",coords,"\n");
  Print("DEFECT_RELATION_COEFFS=",relCoeffs,"\n");
  Print("GROUP_ELEMENT_ROUNDTRIP=",recon=defect,"\n");
  if basisIndex<>1 then Error("Lyndon basis subgroup index is not one"); fi;
  if detAug<>1 and detAug<>-1 then Error("augmented change is not unimodular"); fi;
  if recon<>defect then Error("group-element basis roundtrip failed"); fi;
  return rec(pcp:=pcp,layer:=layer,basisElems:=basisElems,d:=d,
             relVectors:=relVectors,augMatrix:=augMatrix,det:=detAug,
             inverseMap:=invAug,coords:=coords,roundtrip:=recon=defect);
end;

CoordinatesAgainstConversion := function(QG,conv,defect,label)
  local v,coords,sol,relCoeffs,recon,i;
  if not defect in conv.layer then Error("secondary defect outside top lower-central layer"); fi;
  v:=ExponentsByPcp(conv.pcp,defect);
  sol:=SolutionMat(TransposedMat(conv.augMatrix),v);
  if sol=fail then Error("secondary augmented basis solve failure"); fi;
  coords:=sol{[1..conv.d]};
  relCoeffs:=sol{[conv.d+1..Length(sol)]};
  recon:=One(conv.layer);
  for i in [1..conv.d] do recon:=recon*conv.basisElems[i]^coords[i]; od;
  Print(label,"_PCP_NORMAL_FORM=",v,"\n");
  Print(label,"_LYNDON_COORDS=",coords,"\n");
  Print(label,"_RELATION_COEFFS=",relCoeffs,"\n");
  Print(label,"_GROUP_ELEMENT_ROUNDTRIP=",recon=defect,"\n");
  if recon<>defect then Error("secondary group-element roundtrip failed"); fi;
  return coords;
end;

# Source F2 class-five collection.
F2:=FreeGroup("x","y");;
x:=F2.1;; y:=F2.2;;
f0F:=BuildF0(x,y);;
theta:=GroupHomomorphismByImagesNC(F2,F2,[x,y],[y,x]);;
tau:=GroupHomomorphismByImagesNC(F2,F2,[x,y],[y,y^-1*x^-1]);;
thetaDef:=f0F*Image(theta,f0F);;
tau1:=Image(tau,f0F);;
tau2:=Image(tau,tau1);;
tauDef:=tau2*tau1*f0F;;
epiF:=NqEpimorphismNilpotentQuotient(F2,5);;
QF:=Image(epiF);;
lcsF:=LowerCentralSeries(QF);;
btheta:=Image(epiF,thetaDef);;
btau:=Image(epiF,tauDef);;
Print("SOURCE_Q_HIRSCH=",HirschLength(QF)," LCS_HIRSCH=",List(lcsF,HirschLength),"\n");
Print("SOURCE_CLASS4_GATE theta_in_g5=",btheta in lcsF[5]," tau_in_g5=",btau in lcsF[5],"\n");
lw2:=LyndonWordsLocal(2,5);;
lb2:=List(lw2,w->LyndonGroupElementLocal(w,[x,y]));;
lb2Q:=List(lb2,e->Image(epiF,e));;
ll2:=List(lw2,w->WordLabelLocal(w,["x","y"]));;
Print("SOURCE_THETA_BEGIN\n");
convTheta:=ConvertAgainstBasis(QF,lb2Q,ll2,btheta);;
Print("SOURCE_THETA_END\nSOURCE_TAU_BEGIN\n");
convTau:=ConvertAgainstBasis(QF,lb2Q,ll2,btau);;
Print("SOURCE_TAU_END\n");

# Literal source correction: Hall degree-five word followed by the transported
# 796-letter gamma-six exact-mark tail.
C5coords:=[313599,2,-1,-2,0,1];;
tailF:=One(F2);;
for i in tailSigned do
  if i=1 then tailF:=tailF*x;
  elif i=-1 then tailF:=tailF*x^-1;
  elif i=2 then tailF:=tailF*y;
  elif i=-2 then tailF:=tailF*y^-1;
  else Error("tail signed letter outside F2"); fi;
od;
EvalSourceSLPInQ:=function(epi,QG,a,b)
  local out,i;
  out:=Image(epi,MappedWord(f0F,[x,y],[a,b]));
  for i in [1..6] do
    out:=out*Image(epi,MappedWord(lb2[i],[x,y],[a,b]))^C5coords[i];
  od;
  out:=out*Image(epi,MappedWord(tailF,[x,y],[a,b]));
  return out;
end;
fLiftQ5:=EvalSourceSLPInQ(epiF,QF,x,y);;
thetaLiftQ5:=EvalSourceSLPInQ(epiF,QF,y,x);;
tauLiftQ5:=EvalSourceSLPInQ(epiF,QF,y,y^-1*x^-1);;
tau2LiftQ5:=EvalSourceSLPInQ(epiF,QF,y^-1*x^-1,x);;
bThetaLiftQ5:=fLiftQ5*thetaLiftQ5;;
bTauLiftQ5:=tau2LiftQ5*tauLiftQ5*fLiftQ5;;
sourceTailQ5Identity:=IsOne(Image(epiF,tailF));;
sourceThetaQ5Identity:=IsOne(bThetaLiftQ5);;
sourceTauQ5Identity:=IsOne(bTauLiftQ5);;
Print("SOURCE_LITERAL_CLASS5_REPLAY tail_Q5_identity=",sourceTailQ5Identity,
      " theta_Q5_identity=",sourceThetaQ5Identity,
      " tau_Q5_identity=",sourceTauQ5Identity,"\n");
if not (sourceTailQ5Identity and sourceThetaQ5Identity and sourceTauQ5Identity) then
  Error("source literal class-five replay failed");
fi;
Print("R07_NQ5_CROSSCHECK_SOURCE_PASS\n");

# Actual source degree-six residual of the exact-mark prefix.
epiF6:=NqEpimorphismNilpotentQuotient(F2,6);; QF6:=Image(epiF6);;
lcsF6:=LowerCentralSeries(QF6);;
fLiftQ6:=EvalSourceSLPInQ(epiF6,QF6,x,y);;
thetaLiftQ6:=EvalSourceSLPInQ(epiF6,QF6,y,x);;
tauLiftQ6:=EvalSourceSLPInQ(epiF6,QF6,y,y^-1*x^-1);;
tau2LiftQ6:=EvalSourceSLPInQ(epiF6,QF6,y^-1*x^-1,x);;
btheta6:=fLiftQ6*thetaLiftQ6;;
btau6:=tau2LiftQ6*tauLiftQ6*fLiftQ6;;
lw26:=LyndonWordsLocal(2,6);;
lb26:=List(lw26,w->Image(epiF6,LyndonGroupElementLocal(w,[x,y])));;
ll26:=List(lw26,w->WordLabelLocal(w,["x","y"]));;
Print("SOURCE_DEG6_GATE theta_in_g6=",btheta6 in lcsF6[6],
      " tau_in_g6=",btau6 in lcsF6[6],"\n");
Print("SOURCE_THETA6_BEGIN\n");;
convTheta6:=ConvertAgainstBasis(QF6,lb26,ll26,btheta6);;
Print("SOURCE_THETA6_END\nSOURCE_TAU6_BEGIN\n");;
convTau6:=ConvertAgainstBasis(QF6,lb26,ll26,btau6);;
Print("SOURCE_TAU6_END\n");

# Build K(0,5)=PB4/<Delta^2> independently from B4 and the marked pure gens.
FB:=FreeGroup("s1","s2","s3");;
s1:=FB.1;; s2:=FB.2;; s3:=FB.3;;
B4:=FB/[s1*s2*s1*(s2*s1*s2)^-1,
        s2*s3*s2*(s3*s2*s3)^-1,
        Comm(s1,s3)];;
bg:=GeneratorsOfGroup(B4);; s1:=bg[1];; s2:=bg[2];; s3:=bg[3];;
S4:=SymmetricGroup(4);;
bh:=GroupHomomorphismByImages(B4,S4,bg,[(1,2),(2,3),(3,4)]);;
PB:=Kernel(bh);;
x12:=s1^2;; x23:=s2^2;; x34:=s3^2;;
x13:=s2*s1^2*s2^-1;; x24:=s3*s2^2*s3^-1;; x14:=s3*x13*s3^-1;;
pg:=[x12,x13,x14,x23,x24,x34];;
Pmark:=Subgroup(B4,pg);;
iso:=IsomorphismFpGroupByGenerators(Pmark,pg);;
Kfp:=Image(iso);;
delta:=(s1*s2*s3)^4;;
dc:=Image(iso,delta);;
K05:=Kfp/[dc];;
kg:=GeneratorsOfGroup(K05);;
pbIndex:=Index(B4,PB);;
markEqKernel:=Pmark=PB;;
k05RelCount:=Length(RelatorsOfFpGroup(K05));;
k05Abinv:=AbelianInvariants(K05);;
Print("K05_CAL PB_INDEX=",pbIndex," MARK_EQ_KERNEL=",markEqKernel,
      " RELS=",k05RelCount," ABINV=",k05Abinv,"\n");
if not (pbIndex=24 and markEqKernel and k05RelCount=18 and k05Abinv=[0,0,0,0,0]) then
  Error("K05 calibration failed");
fi;

# Canonical group-level rho on [x12,x13,x14,x23,x24,x34].
rhoim:=[(kg[3]*kg[5]*kg[6])^-1,
        kg[3],kg[5],
        (kg[1]*kg[2]*kg[3])^-1,
        (kg[1]*kg[4]*kg[5])^-1,
        kg[1]];;
rho:=GroupHomomorphismByImagesNC(K05,K05,kg,rhoim);;
r5ok:=true;;
for i in [1..6] do
  z:=kg[i];;
  for j in [1..5] do z:=Image(rho,z); od;
  # Equality will be tested after mapping into Q5 below.
  rhoim[i]:=rhoim[i];
od;

jf:=BuildF0(kg[1],kg[4]);;
r1:=Image(rho,jf);; r2:=Image(rho,r1);; r3:=Image(rho,r2);; r4:=Image(rho,r3);;
pentRho:=r4*r3*r2*r1*jf;;
pentDrop:=r4*r3*r1*jf;;
pentSign:=r4*r3*r2^-1*r1*jf;;
pentSwap:=r3*r4*r2*r1*jf;;

# Literal Drinfeld five-coface defect, with the exact product order in (2.20):
# (phi_1,2,34(f) phi_12,3,4(f))^-1
#   phi_234(f) phi_1,23,4(f) phi_123(f).
p123:=BuildF0(kg[1],kg[4]);;
p234:=BuildF0(kg[4],kg[6]);;
p1_23_4:=BuildF0(kg[1]*kg[2],kg[5]*kg[6]);;
p12_3_4:=BuildF0(kg[2]*kg[4],kg[6]);;
p1_2_34:=BuildF0(kg[1],kg[4]*kg[5]);;
pentCoface:=(p1_2_34*p12_3_4)^-1*p234*p1_23_4*p123;;
x15lit:=(kg[1]*kg[2]*kg[3])^-1;;
x45lit:=(kg[3]*kg[5]*kg[6])^-1;;
pentTilde:=BuildF0(x45lit,kg[6])^-1*BuildF0(kg[1],x15lit)^-1*
           BuildF0(kg[4],kg[6])*BuildF0(x45lit,x15lit)*BuildF0(kg[1],kg[4]);;

epiK:=NqEpimorphismNilpotentQuotient(K05,5);;
QK:=Image(epiK);;
lcsK:=LowerCentralSeries(QK);;
bPentRho:=Image(epiK,pentRho);;
bPentCoface:=Image(epiK,pentCoface);;
bPentTilde:=Image(epiK,pentTilde);;
bDrop:=Image(epiK,pentDrop);;
bSign:=Image(epiK,pentSign);;
bSwap:=Image(epiK,pentSwap);;
Print("K05_Q5_HIRSCH=",HirschLength(QK)," LCS_HIRSCH=",List(lcsK,HirschLength),"\n");
rawRhoInG5:=bPentRho in lcsK[5];;
rawCofaceInG5:=bPentCoface in lcsK[5];;
tildeEqCoface:=bPentTilde=bPentCoface;;
rawRhoEqCoface:=bPentRho=bPentCoface;;
dropInG5:=bDrop in lcsK[5];;
signInG5:=bSign in lcsK[5];;
swapEqRho:=bSwap=bPentRho;;
Print("K05_CLASS4_GATE rho_in_g5=",rawRhoInG5,
      " coface_in_g5=",rawCofaceInG5,
      " tilde_eq_coface_Q5=",tildeEqCoface,
      " rho_eq_coface_Q5=",rawRhoEqCoface,
      " drop_in_g5=",dropInG5,
      " sign_in_g5=",signInG5," swap_equal_Q5=",swapEqRho,"\n");
if not (rawRhoInG5 and rawCofaceInG5 and tildeEqCoface and
        not rawRhoEqCoface and not dropInG5 and not signInG5 and swapEqRho) then
  Error("raw rho/coface or mutation gate failed");
fi;
r5q:=true;;
for i in [1..6] do
  z:=kg[i];;
  for j in [1..5] do z:=Image(rho,z); od;
  if Image(epiK,z)<>Image(epiK,kg[i]) then r5q:=false; fi;
od;
Print("RHO5_Q5=",r5q,"\n");
if not r5q then Error("rho^5 failed in Q5"); fi;
Print("R07_NQ5_CROSSCHECK_RAW_GATE_PASS\n");

# Integral semidirect Lyndon basis, represented by literal group commutators.
A5g:=(kg[1]*kg[2]*kg[3])^-1;;
B5g:=(kg[1]*kg[4]*kg[5])^-1;;
C5g:=(kg[2]*kg[4]*kg[6])^-1;;
Xg:=kg[1];; Yg:=kg[4];;
lw3:=LyndonWordsLocal(3,5);;
lb3:=List(lw3,w->LyndonGroupElementLocal(w,[A5g,B5g,C5g]));;
lh2:=LyndonWordsLocal(2,5);;
lbh:=List(lh2,w->LyndonGroupElementLocal(w,[Xg,Yg]));;
targetBasis:=Concatenation(List(lb3,e->Image(epiK,e)),List(lbh,e->Image(epiK,e)));;
targetLabels:=Concatenation(List(lw3,w->Concatenation("n:",WordLabelLocal(w,["A","B","C"]))),
                            List(lh2,w->Concatenation("h:",WordLabelLocal(w,["X","Y"]))));;
Print("PENT_BEGIN\n");
convPent:=ConvertAgainstBasis(QK,targetBasis,targetLabels,bPentCoface);;
rhoCoords:=CoordinatesAgainstConversion(QK,convPent,bPentRho,"RHO_NORM");;
tildeCoords:=CoordinatesAgainstConversion(QK,convPent,bPentTilde,"TILDE_COFA");;
if convPent.det<>1 and convPent.det<>-1 then Error("pentagon basis is not unimodular"); fi;
if not convPent.roundtrip then Error("pentagon basis group roundtrip failed"); fi;
if tildeCoords<>convPent.coords then Error("literal and rewritten A.18 coordinates disagree"); fi;
Print("PENT_END\n");
Print("R07_NQ5_CROSSCHECK_BASIS_PASS det=",convPent.det,
      " rank=",HirschLength(convPent.layer),"\n");

# Full literal class-five group replay, including the exactifying tail.
EvalSLPAtK05Q:=function(a,b)
  local out,i;
  out:=Image(epiK,MappedWord(f0F,[x,y],[a,b]));
  for i in [1..6] do
    out:=out*Image(epiK,MappedWord(lb2[i],[x,y],[a,b]))^C5coords[i];
  od;
  out:=out*Image(epiK,MappedWord(tailF,[x,y],[a,b]));
  return out;
end;
ra:=kg[1];; rb:=kg[4];; rhoLiftFactors:=[];;
for i in [0..4] do
  Add(rhoLiftFactors,EvalSLPAtK05Q(ra,rb));
  ra:=Image(rho,ra); rb:=Image(rho,rb);
od;
liftRho:=rhoLiftFactors[5]*rhoLiftFactors[4]*rhoLiftFactors[3]*rhoLiftFactors[2]*rhoLiftFactors[1];;
lp123:=EvalSLPAtK05Q(kg[1],kg[4]);;
lp234:=EvalSLPAtK05Q(kg[4],kg[6]);;
lp1_23_4:=EvalSLPAtK05Q(kg[1]*kg[2],kg[5]*kg[6]);;
lp12_3_4:=EvalSLPAtK05Q(kg[2]*kg[4],kg[6]);;
lp1_2_34:=EvalSLPAtK05Q(kg[1],kg[4]*kg[5]);;
liftCoface:=(lp1_2_34*lp12_3_4)^-1*lp234*lp1_23_4*lp123;;
liftRhoIdentity:=IsOne(liftRho);;
liftCofaceIdentity:=IsOne(liftCoface);;
liftRhoEqCoface:=liftRho=liftCoface;;
Print("FULL_LITERAL_CLASS5_REPLAY rho_Q5_identity=",liftRhoIdentity,
      " coface_Q5_identity=",liftCofaceIdentity,
      " rho_eq_coface_Q5=",liftRhoEqCoface,"\n");
if not (liftRhoIdentity and liftCofaceIdentity and liftRhoEqCoface) then
  Error("corrected literal class-five replay failed");
fi;
Print("R07_NQ5_CROSSCHECK_LITERAL_PASS\n");
Print("R07_NQ5_CROSSCHECK_FINAL_MARKER status=PASS\n");
QUIT_GAP(0);
