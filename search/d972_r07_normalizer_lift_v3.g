# R07 literal class-six augmented producer (task 162 v10).
# Mechanical producer only.  The load-bearing pentagon is literal A.18.
# Run through .github/workflows/gap-run.yml; no local full run is intended.
#
# Full GHA inputs:
#   script: search/d972_r07_normalizer_lift_v3.g
#   preamble: (empty; full is the fail-closed default)
#   out_dir: ci/out
#   timeout_min: 360
#   with_pquot_packages: false
# Success requires, exactly once and with no Error,/Syntax error diagnostic:
#   R07_V3_NQ_BOOTSTRAP_PASS
#   R07_V3_EXACTIFIERS_READY
#   R07_V3_F2_READY
#   R07_V3_K05_LITERAL_READY
#   R07_V3_PREFIX_T_M1_0_1_2_THROUGH_DEGREE5_PASS
#   R07_V3_AUGMENTED_SMITH_PASS
#   R07_V3_RAW_ARTIFACT_WRITTEN
#   R07_V3_FINAL_MARKER status=CANDIDATE_LITERAL_CLASS6_PASS
# The complete raw receipt is ci/out/d972_r07_normalizer_lift_v3_raw_20260825.dat.
#
# Cheap preflight uses preamble R07_V3_MODE:="selftest";; and requires:
#   R07_V3_NQ_BOOTSTRAP_PASS
#   R07_V3_SELFTEST_FINAL_MARKER h5=6 h6=9 n6=116 smith=PASS nq=PASS pcp=PASS

if not IsBound(R07_V3_MODE) then R07_V3_MODE := "full"; fi;;
if not IsBound(R07_V3_RAW_OUT) then
  R07_V3_RAW_OUT := "ci/out/d972_r07_normalizer_lift_v3_raw_20260825.dat";
fi;;
if not IsBound(R07_V3_FROZEN_V1) then
  R07_V3_FROZEN_V1 := "search/certs/d972_r07_normalizer_lift_v1_20260825.json";
fi;;
R07V3FrozenV1Sha :=
  "5fc9dcd3291668890dfafe0e7a739b69bca7088556ccbf80948e506e2401b8e8";;

if GAPInfo.Version <> "4.16.0" then Error("R07_V3 requires GAP 4.16.0"); fi;;

# The official GAP 4.16.0 full archive ships pinned NQ sources but no Linux
# executable on a fresh runner.  Authenticate the unique native package and,
# only when its executable is absent, build it in place.  This is the producer
# namespace copy of the bootstrap explicitly authorized after GHA run
# 32803312340 failed before any mathematical computation.
R07V3NqVersion := "2.5.11";;
R07V3NqPackageInfoSha :=
  "e5e3370aa823163909a5130f1d803f43051e606305915718bcf7a363e5af5264";;
R07V3NqConfigureSha :=
  "4c09599a55cbdf0eb22998280e197f64ebb2e6ca5ca884b80e3e8d55c1ca0bd0";;
R07V3NqMakefileInSha :=
  "84def846c51b5fe54b79b1ca312ac5629c383ccadbe43349da4d40efa9c5d003";;

R07V3NqShellQuote := function(s)
  if not IsString(s) or Position(s,'\n')<>fail or Position(s,'\r')<>fail then
    Error("R07_V3_NQ: unsafe shell path");
  fi;
  return Concatenation("'",ReplacedString(s,"'","'\"'\"'"),"'");
end;;

R07V3NqRequireFileSha := function(path,expected,label)
  local body,actual;
  body:=StringFile(path);
  if body=fail then Error("R07_V3_NQ: missing ",label," at ",path); fi;
  actual:=HexSHA256(body);
  if actual<>expected then
    Error("R07_V3_NQ: ",label," SHA256 drift: ",actual);
  fi;
end;;

R07V3NqInfos:=PackageInfo("nq");;
if Length(R07V3NqInfos)<>1 then
  Error("R07_V3_NQ: expected exactly one NQ PackageInfo entry");
fi;;
R07V3NqInfo:=R07V3NqInfos[1];;
if not IsBound(R07V3NqInfo.Version) or
   R07V3NqInfo.Version<>R07V3NqVersion then
  Error("R07_V3_NQ: NQ version drift");
fi;;
if not IsBound(R07V3NqInfo.InstallationPath) then
  Error("R07_V3_NQ: NQ InstallationPath missing");
fi;;
R07V3NqPath:=R07V3NqInfo.InstallationPath;;
if not IsString(R07V3NqPath) or Length(R07V3NqPath)<2 or
   R07V3NqPath[Length(R07V3NqPath)]<>'/' then
  Error("R07_V3_NQ: malformed NQ InstallationPath");
fi;;
if not IsBound(GAPInfo.RootPaths) or not IsList(GAPInfo.RootPaths) then
  Error("R07_V3_NQ: GAPInfo.RootPaths unavailable");
fi;;
R07V3NqRootCandidates:=[];;
for R07V3NqRootCandidate in GAPInfo.RootPaths do
  if IsString(R07V3NqRootCandidate) and Length(R07V3NqRootCandidate)>0 then
    if R07V3NqRootCandidate[Length(R07V3NqRootCandidate)]<>'/' then
      R07V3NqRootCandidate:=Concatenation(R07V3NqRootCandidate,"/");
    fi;
    R07V3NqParentCandidate:=Concatenation(R07V3NqRootCandidate,"pkg/");;
    if Length(R07V3NqPath)>Length(R07V3NqParentCandidate) and
       PositionSublist(R07V3NqPath,R07V3NqParentCandidate)=1 then
      R07V3NqTailCandidate:=R07V3NqPath{
        [Length(R07V3NqParentCandidate)+1..Length(R07V3NqPath)]};;
      if Length(R07V3NqTailCandidate)>=2 and
         R07V3NqTailCandidate[Length(R07V3NqTailCandidate)]='/' and
         Position(R07V3NqTailCandidate{
           [1..Length(R07V3NqTailCandidate)-1]},'/')=fail and
         Position(R07V3NqRootCandidates,R07V3NqRootCandidate)=fail then
        Add(R07V3NqRootCandidates,R07V3NqRootCandidate);
      fi;
    fi;
  fi;
od;
if Length(R07V3NqRootCandidates)<>1 then
  Error("R07_V3_NQ: PackageInfo does not select exactly one native GAP root");
fi;;
R07V3NqGapRoot:=R07V3NqRootCandidates[1];;
R07V3NqPackageParent:=Concatenation(R07V3NqGapRoot,"pkg/");;
R07V3NqDirectoryName:=R07V3NqPath{
  [Length(R07V3NqPackageParent)+1..Length(R07V3NqPath)-1]};;
if R07V3NqPath<>
   Concatenation(R07V3NqPackageParent,R07V3NqDirectoryName,"/") then
  Error("R07_V3_NQ: package-parent equality gate failed");
fi;;

R07V3NqEnvGapRoot:=fail;;
if IsBoundGlobal("GetEnv") then R07V3NqEnvGapRoot:=GetEnv("GAPROOT"); fi;;
if R07V3NqEnvGapRoot<>fail and R07V3NqEnvGapRoot<>"" then
  if R07V3NqEnvGapRoot[Length(R07V3NqEnvGapRoot)]<>'/' then
    R07V3NqEnvGapRoot:=Concatenation(R07V3NqEnvGapRoot,"/");
  fi;
  if R07V3NqEnvGapRoot<>R07V3NqGapRoot then
    Error("R07_V3_NQ: GAPROOT disagrees with PackageInfo/native root");
  fi;
fi;;

R07V3NqRequireFileSha(Concatenation(R07V3NqPath,"PackageInfo.g"),
  R07V3NqPackageInfoSha,"NQ PackageInfo.g");;
R07V3NqRequireFileSha(Concatenation(R07V3NqPath,"configure"),
  R07V3NqConfigureSha,"NQ configure");;
R07V3NqRequireFileSha(Concatenation(R07V3NqPath,"Makefile.in"),
  R07V3NqMakefileInSha,"NQ Makefile.in");;

R07V3NqExecutable:=Filename(DirectoriesPackagePrograms("nq"),"nq");;
R07V3NqBuilt:=false;;
if R07V3NqExecutable=fail then
  if PositionSublist(LowercaseString(GAPInfo.Architecture),"linux")=fail then
    Error("R07_V3_NQ: missing executable outside the Linux bootstrap target");
  fi;
  R07V3NqOutRoot:=Filename(DirectoryCurrent(),"ci/out");;
  R07V3NqConfigureLog:=Concatenation(R07V3NqOutRoot,
    "/r07_v3_nq_configure.log");;
  R07V3NqMakeLog:=Concatenation(R07V3NqOutRoot,"/r07_v3_nq_make.log");;
  R07V3NqBuildSentinel:=Concatenation(R07V3NqOutRoot,
    "/r07_v3_nq_bootstrap.ok");;
  R07V3NqBuildCommand:=Concatenation(
    "set -eu; test -d ",R07V3NqShellQuote(R07V3NqOutRoot),"; ",
    "rm -f ",R07V3NqShellQuote(R07V3NqConfigureLog)," ",
      R07V3NqShellQuote(R07V3NqMakeLog)," ",
      R07V3NqShellQuote(R07V3NqBuildSentinel),"; ",
    "cd ",R07V3NqShellQuote(R07V3NqPath),"; test -x ./configure; ",
    "./configure --with-gaproot=",R07V3NqShellQuote(R07V3NqGapRoot),
      " > ",R07V3NqShellQuote(R07V3NqConfigureLog)," 2>&1; ",
    "make -j2 > ",R07V3NqShellQuote(R07V3NqMakeLog)," 2>&1; ",
    "printf 'R07_V3_NQ_BUILD_SHELL_PASS\\n' > ",
      R07V3NqShellQuote(R07V3NqBuildSentinel));;
  Exec(R07V3NqBuildCommand);
  if StringFile(R07V3NqBuildSentinel)<>"R07_V3_NQ_BUILD_SHELL_PASS\n" then
    Error("R07_V3_NQ: configure/make failed before exact sentinel");
  fi;
  R07V3NqBuilt:=true;
  R07V3NqExecutable:=Filename(DirectoriesPackagePrograms("nq"),"nq");
fi;;
if R07V3NqExecutable=fail then
  Error("R07_V3_NQ: NQ executable unavailable after bootstrap");
fi;;
if LoadPackage("nq")<>true then
  Error("R07_V3_NQ: pinned NQ failed to load after bootstrap");
fi;;
R07V3NqLoadedInfos:=PackageInfo("nq");;
if Length(R07V3NqLoadedInfos)<>1 or
   R07V3NqLoadedInfos[1].Version<>R07V3NqVersion then
  Error("R07_V3_NQ: loaded NQ version pin failed");
fi;;
Print("R07_V3_NQ_BOOTSTRAP_PASS gap_version=",GAPInfo.Version,
  " nq_version=",R07V3NqVersion," built=",R07V3NqBuilt,
  " gap_root=",R07V3NqGapRoot," package_path=",R07V3NqPath,
  " executable=",R07V3NqExecutable,"\n");;

if LoadPackage("polycyclic") <> true then Error("R07_V3 polycyclic package unavailable"); fi;;

R07V3_GC := function(a,b)
  return a*b*a^-1*b^-1;
end;;

R07V3_MakeF0 := function(x,y)
  local p,q,T,V,S,W,D7,H0,Hb,Ab,z,chi;
  p := x^-1*y*x^-2*y^-1*x^-1;
  q := x^-1*y^-1*x^-2*y*x^-1;
  T := p*q*p^3;
  V := function(a) return q^-a*T*q^a; end;
  S := V(2);
  W := p*V(1);
  D7 := q^4*V(5);
  H0 := V(4)*W*D7*T;
  Hb := p^7*H0;
  Ab := Hb^-1*T*Hb;
  z := y^-1*x^-1;
  chi := R07V3_GC(x,y)*R07V3_GC(y,z)^-1;
  return chi*R07V3_GC(Ab,S);
end;;

R07V3_IsLyndonWord := function(w)
  local n,i,rot;
  n := Length(w);
  if n=1 then return true; fi;
  for i in [2..n] do
    rot := Concatenation(w{[i..n]},w{[1..i-1]});
    if not w<rot then return false; fi;
  od;
  return true;
end;;

R07V3_LyndonWords := function(k,n)
  return Filtered(Tuples([1..k],n),R07V3_IsLyndonWord);
end;;

R07V3_WordLabel := function(w,alphabet)
  return Concatenation(List(w,i->alphabet[i]));
end;;

R07V3_StandardGroupBracket := function(w,gens)
  local n,i,u,v;
  n := Length(w);
  if n=1 then return gens[w[1]]; fi;
  for i in [2..n] do
    v := w{[i..n]};
    if R07V3_IsLyndonWord(v) then
      u := w{[1..i-1]};
      if not R07V3_IsLyndonWord(u) then Error("non-Lyndon prefix"); fi;
      return R07V3_GC(
        R07V3_StandardGroupBracket(u,gens),
        R07V3_StandardGroupBracket(v,gens));
    fi;
  od;
  Error("missing Lyndon factorization");
end;;

R07V3_EvalExtRep := function(ext,gens,one)
  local out,i;
  out := one;
  for i in [1,3..Length(ext)-1] do
    out := out*gens[ext[i]]^ext[i+1];
  od;
  return out;
end;;

R07V3_PowerProduct := function(values,coeffs,one)
  local out,i;
  if Length(values)<>Length(coeffs) then Error("PowerProduct length"); fi;
  out := one;
  for i in [1..Length(values)] do out := out*values[i]^coeffs[i]; od;
  return out;
end;;

R07V3_ZeroVector := function(n)
  return List([1..n],i->0);
end;;

R07V3_AddVector := function(a,b)
  if Length(a)<>Length(b) then Error("AddVector length"); fi;
  return List([1..Length(a)],i->a[i]+b[i]);
end;;

R07V3_ScaleVector := function(c,a)
  return List(a,x->c*x);
end;;

R07V3_Column := function(v)
  return List(v,x->[x]);
end;;

R07V3_Uncolumn := function(v)
  return List(v,x->x[1]);
end;;

R07V3_CanonicalIntMatrixString := function(matrix)
  return Concatenation("[",JoinStringsWithSeparator(
    List(matrix,row->Concatenation("[",JoinStringsWithSeparator(
      List(row,String),","),"]")),","),"]");
end;;

R07V3_CanonicalIntMatrixDigest := function(matrix)
  return HexSHA256(R07V3_CanonicalIntMatrixString(matrix));
end;;

R07V3_FromPcpExponents := function(pcp,exp)
  local out,i;
  if Length(pcp)<>Length(exp) then Error("Pcp exponent length"); fi;
  out := OneOfPcp(pcp);
  for i in [1..Length(pcp)] do out := out*pcp[i]^exp[i]; od;
  return out;
end;;

R07V3_PowerRelationData := function(pcp)
  local orders,indices,columns,powers,n,i,r,v,e,j;
  orders := RelativeOrdersOfPcp(pcp);
  indices := Filtered([1..Length(orders)],i->orders[i]<>0);
  columns := [];
  powers := [];
  n := Length(pcp);
  for i in indices do
    r := orders[i];
    e := ExponentsByPcp(pcp,pcp[i]^r);
    v := R07V3_ZeroVector(n);
    v[i] := r;
    for j in [1..n] do v[j] := v[j]-e[j]; od;
    Add(columns,v);
    Add(powers,e);
  od;
  return rec(orders:=orders,indices:=indices,columns:=columns,powers:=powers);
end;;

R07V3_BuildConversion := function(group,basis,expectedRank,label)
  local pcp,power,cols,forward,det,inverse;
  if Length(basis)<>expectedRank then Error(label," Hall rank drift"); fi;
  pcp := Pcp(group);
  power := R07V3_PowerRelationData(pcp);
  cols := Concatenation(List(basis,x->ExponentsByPcp(pcp,x)),power.columns);
  if Length(cols)<>Length(pcp) then
    Error(label," augmented column count drift: ",Length(cols)," vs ",Length(pcp));
  fi;
  forward := TransposedMat(cols);
  det := DeterminantMat(forward);
  if AbsInt(det)<>1 then Error(label," non-unimodular determinant ",det); fi;
  inverse := forward^-1;
  if not ForAll(Flat(inverse),IsInt) then Error(label," nonintegral inverse"); fi;
  if inverse*forward<>IdentityMat(Length(pcp)) then Error(label," inverse replay"); fi;
  return rec(
    label:=label, group:=group, pcp:=pcp, rank:=expectedRank,
    power:=power, forward:=forward, inverse:=inverse, determinant:=det,
    basis:=basis);
end;;

R07V3_Coordinates := function(conv,g)
  local exp,all,hall,rel,replay;
  if not g in conv.group then Error(conv.label," residual outside gamma6"); fi;
  exp := ExponentsByPcp(conv.pcp,g);
  all := R07V3_Uncolumn(conv.inverse*R07V3_Column(exp));
  if conv.forward*R07V3_Column(all)<>R07V3_Column(exp) then
    Error(conv.label," all-coordinate roundtrip failed");
  fi;
  hall := all{[1..conv.rank]};
  if Length(all)>conv.rank then rel := all{[conv.rank+1..Length(all)]};
  else rel := []; fi;
  replay := R07V3_PowerProduct(conv.basis,hall,One(conv.group));
  if replay<>g then Error(conv.label," subgroup Pcp group replay failed"); fi;
  return rec(pcp:=exp,hall:=hall,relations:=rel,all:=all);
end;;

R07V3_RankModP := function(matrix,p)
  local a,nr,nc,r,c,pivot,i,j,inv,q;
  a := List(matrix,row->List(row,x->x mod p));
  nr := Length(a);
  if nr=0 then return 0; fi;
  nc := Length(a[1]); r := 0;
  for c in [1..nc] do
    if r=nr then return r; fi;
    pivot := fail;
    for i in [r+1..nr] do if a[i][c]<>0 then pivot:=i; break; fi; od;
    if pivot<>fail then
      r := r+1;
      q := a[r]; a[r] := a[pivot]; a[pivot] := q;
      inv := First([1..p-1],z->(a[r][c]*z) mod p=1);
      a[r] := List(a[r],x->(x*inv) mod p);
      for i in [1..nr] do
        if i<>r and a[i][c]<>0 then
          q := a[i][c];
          for j in [1..nc] do a[i][j] := (a[i][j]-q*a[r][j]) mod p; od;
        fi;
      od;
    fi;
  od;
  return r;
end;;

R07V3_SolveInteger := function(matrix,b)
  local snf,bp,rank,ncols,nrows,y,i,d,z,kernel;
  snf := SmithNormalFormIntegerMatTransforms(matrix);
  if snf.rowtrans*matrix*snf.coltrans<>snf.normal then Error("SNF replay failed"); fi;
  rank := snf.rank; nrows:=Length(matrix); ncols:=Length(matrix[1]);
  bp := snf.rowtrans*R07V3_Column(b);
  y := List([1..ncols],i->[0]);
  for i in [1..rank] do
    d := snf.normal[i][i];
    if bp[i][1] mod d<>0 then
      return rec(soluble:=false,snf:=snf,transformed_rhs:=R07V3_Uncolumn(bp));
    fi;
    y[i][1] := bp[i][1]/d;
  od;
  if rank<nrows then
    for i in [rank+1..nrows] do
      if bp[i][1]<>0 then
        return rec(soluble:=false,snf:=snf,transformed_rhs:=R07V3_Uncolumn(bp));
      fi;
    od;
  fi;
  z := R07V3_Uncolumn(snf.coltrans*y);
  if matrix*R07V3_Column(z)<>R07V3_Column(b) then Error("integer solve replay"); fi;
  kernel := [];
  if rank<ncols then
    for i in [rank+1..ncols] do Add(kernel,List(snf.coltrans,row->row[i])); od;
  fi;
  return rec(soluble:=true,solution:=z,kernel:=kernel,snf:=snf,
    transformed_rhs:=R07V3_Uncolumn(bp));
end;;

R07V3_BlockJoin := function(perms,sizes)
  local out,off,b,i;
  out := [1..Sum(sizes)]; off:=0;
  for b in [1..Length(perms)] do
    for i in [1..sizes[b]] do out[off+i] := off+(i^perms[b]); od;
    off := off+sizes[b];
  od;
  return PermList(out);
end;;

R07V3_VmHWM := function()
  local txt,lines,hit;
  if not IsExistingFile("/proc/self/status") then return "UNAVAILABLE"; fi;
  txt := StringFile("/proc/self/status");
  lines := SplitString(txt,"\n");
  hit := Filtered(lines,x->Length(x)>=6 and x{[1..6]}="VmHWM:");
  if Length(hit)=1 then return hit[1]; fi;
  return "UNAVAILABLE";
end;;

R07V3_JsonIntegerList := function(path,key)
  local txt,tag,pos,op,cl,depth,i,ch,out;
  if not IsExistingFile(path) then Error("R07_V3 frozen input missing: ",path); fi;
  txt := StringFile(path);
  tag := Concatenation("\"",key,"\"");
  pos := PositionSublist(txt,tag);
  if pos=fail then Error("R07_V3 frozen key missing: ",key); fi;
  op := Position(txt,'[',pos+Length(tag)-1);
  if op=fail then Error("R07_V3 frozen list opening bracket missing: ",key); fi;
  depth:=0; cl:=fail;
  for i in [op..Length(txt)] do
    ch:=txt[i];
    if ch='[' then depth:=depth+1;
    elif ch=']' then
      depth:=depth-1;
      if depth=0 then cl:=i; break; fi;
    fi;
  od;
  if cl=fail then Error("R07_V3 frozen list closing bracket missing: ",key); fi;
  out:=EvalString(txt{[op..cl]});
  if not IsList(out) or not ForAll(out,IsInt) then
    Error("R07_V3 frozen value is not a flat integer list: ",key);
  fi;
  return out;
end;;

R07V3_frozenV1Text:=StringFile(R07_V3_FROZEN_V1);;
if R07V3_frozenV1Text=fail or Length(R07V3_frozenV1Text)<>727381 then
  Error("R07_V3 frozen v1 byte-count pin failed");
fi;;
if HexSHA256(R07V3_frozenV1Text)<>R07V3FrozenV1Sha then
  Error("R07_V3 frozen v1 SHA256 pin failed");
fi;;
R07V3_frozenU6Ext:=R07V3_JsonIntegerList(
  R07_V3_FROZEN_V1,"gamma6_tail_ExtRep");;
R07V3_frozenU6Combination:=R07V3_JsonIntegerList(
  R07_V3_FROZEN_V1,"gamma6_tail_normal_record_combination_ExtRep");;
if Length(R07V3_frozenU6Ext) mod 2<>0 or
   Sum(List([2,4..Length(R07V3_frozenU6Ext)],i->AbsInt(R07V3_frozenU6Ext[i])))<>796 then
  Error("R07_V3 frozen 796-letter tail pin failed");
fi;;

R07V3_h5 := R07V3_LyndonWords(2,5);;
R07V3_h6 := R07V3_LyndonWords(2,6);;
R07V3_n6 := R07V3_LyndonWords(3,6);;
R07V3_h6Labels:=List(R07V3_h6,w->Concatenation(
  "h:",R07V3_WordLabel(w,["X","Y"])));;
R07V3_n6Labels:=List(R07V3_n6,w->Concatenation(
  "n:",R07V3_WordLabel(w,["A","B","C"])));;
R07V3_targetLabels:=Concatenation(
  List(R07V3_h6Labels,s->Concatenation("theta:",s)),
  List(R07V3_h6Labels,s->Concatenation("tau:",s)),
  List(Concatenation(R07V3_n6Labels,R07V3_h6Labels),
    s->Concatenation("pent:",s)));;
if Length(R07V3_h5)<>6 or Length(R07V3_h6)<>9 or Length(R07V3_n6)<>116 then
  Error("R07_V3 Witt rank drift");
fi;;

if R07_V3_MODE="selftest" then
  R07V3_testA := [[2,4],[6,8],[10,12]];;
  R07V3_testb := [2,6,10];;
  R07V3_testsol := R07V3_SolveInteger(R07V3_testA,R07V3_testb);;
  if not R07V3_testsol.soluble then Error("R07_V3 Smith selftest"); fi;;
  if R07V3_RankModP([[1,0],[0,1]],3)<>2 then Error("R07_V3 mod3 selftest"); fi;;
  if R07V3_CanonicalIntMatrixDigest([[1,2],[3,4]])<>
     "03a4cc702aa6e4f169ff34dd055714141eae3d2d7c50f6f053150cc72ef12638" then
    Error("R07_V3 canonical matrix digest selftest");
  fi;;
  R07V3_testF:=FreeGroup("a","b");;
  R07V3_testEpi:=NqEpimorphismNilpotentQuotient(R07V3_testF,2);;
  R07V3_testQ:=Image(R07V3_testEpi);;
  R07V3_testa:=Image(R07V3_testEpi,R07V3_testF.1);;
  R07V3_testbq:=Image(R07V3_testEpi,R07V3_testF.2);;
  R07V3_testGamma2:=LowerCentralSeriesOfGroup(R07V3_testQ)[2];;
  R07V3_testComm:=R07V3_GC(R07V3_testa,R07V3_testbq);;
  R07V3_testConv:=R07V3_BuildConversion(
    R07V3_testGamma2,[R07V3_testComm],1,"selftest_F2_gamma2");;
  R07V3_testCoord:=R07V3_Coordinates(R07V3_testConv,R07V3_testComm);;
  if R07V3_testCoord.hall<>[1] then Error("R07_V3 Pcp conversion selftest"); fi;;
  Print("R07_V3_SELFTEST_FINAL_MARKER h5=6 h6=9 n6=116 smith=PASS nq=PASS pcp=PASS\n");
  QUIT_GAP(0);
fi;;
if R07_V3_MODE<>"full" then Error("R07_V3 unknown mode: ",R07_V3_MODE); fi;;

R07V3_startRuntime := Runtime();;
R07V3_startAllocated := TotalMemoryAllocated();;
Print("R07_V3_FULL_BEGIN runtime=",Runtime(),"\n");

# Finite marked A=(G36 x PSL(2,8)); the external C3 is tracked separately.
R07V3_r := PermList(List([1..36],i->((i mod 36)+1)));;
R07V3_s := PermList(List([1..36],i->((-(i-1)) mod 36)+1));;
R07V3_px := PermList([8,5,2,1,9,7,4,3,6]);;
R07V3_py := PermList([2,6,7,5,8,4,1,9,3]);;
R07V3_sizes := [36,36,36,9];;
R07V3_xA := R07V3_BlockJoin([R07V3_r,R07V3_s,R07V3_s,R07V3_px],R07V3_sizes);;
R07V3_yA := R07V3_BlockJoin([R07V3_r*R07V3_s,R07V3_r,R07V3_r*R07V3_s,R07V3_py],R07V3_sizes);;
R07V3_A := Group(R07V3_xA,R07V3_yA);;
if Size(R07V3_A)<>11757312 then Error("finite A order drift"); fi;;
R07V3_FS := FreeGroup("x","y");;
R07V3_sx := R07V3_FS.1;; R07V3_sy := R07V3_FS.2;;

R07V3_NextLower := function(prevGroup,prevRecords)
  local records,values,pr,j,v,w,H,pos,cv,cw,expected,ambV,ambW,stepsV,stepsW;
  ambV:=[R07V3_xA,R07V3_yA]; ambW:=[R07V3_sx,R07V3_sy];
  stepsV:=[R07V3_xA,R07V3_yA,R07V3_xA^-1,R07V3_yA^-1];
  stepsW:=[R07V3_sx,R07V3_sy,R07V3_sx^-1,R07V3_sy^-1];
  records:=[]; values:=[];
  for pr in prevRecords do
    for j in [1..2] do
      v:=R07V3_GC(pr.value,ambV[j]); w:=R07V3_GC(pr.word,ambW[j]);
      if v<>One(R07V3_A) and Position(values,v)=fail then
        Add(values,v); Add(records,rec(value:=v,word:=w));
      fi;
    od;
  od;
  H:=Subgroup(R07V3_A,values); pos:=1;
  while pos<=Length(records) do
    for j in [1..4] do
      cv:=stepsV[j]^-1*records[pos].value*stepsV[j];
      if not cv in H then
        cw:=stepsW[j]^-1*records[pos].word*stepsW[j];
        Add(values,cv); Add(records,rec(value:=cv,word:=cw)); H:=Subgroup(R07V3_A,values);
      fi;
    od;
    pos:=pos+1;
  od;
  expected:=CommutatorSubgroup(prevGroup,R07V3_A);
  if H<>expected then Error("finite LCS construction mismatch"); fi;
  return rec(group:=H,records:=records);
end;;

R07V3_levels := [rec(group:=R07V3_A,
  records:=[rec(value:=R07V3_xA,word:=R07V3_sx),rec(value:=R07V3_yA,word:=R07V3_sy)])];;
for R07V3_i in [2..7] do
  Add(R07V3_levels,R07V3_NextLower(
    R07V3_levels[R07V3_i-1].group,R07V3_levels[R07V3_i-1].records));
od;
if List(R07V3_levels,z->Size(z.group))<>
  [11757312,734832,367416,367416,367416,367416,367416] then
  Error("finite LCS orders drift");
fi;;

R07V3_hall5A := List(R07V3_h5,w->R07V3_StandardGroupBracket(w,[R07V3_xA,R07V3_yA]));;
R07V3_hall5S := List(R07V3_h5,w->R07V3_StandardGroupBracket(w,[R07V3_sx,R07V3_sy]));;
R07V3_hall6A := List(R07V3_h6,w->R07V3_StandardGroupBracket(w,[R07V3_xA,R07V3_yA]));;
R07V3_hall6S := List(R07V3_h6,w->R07V3_StandardGroupBracket(w,[R07V3_sx,R07V3_sy]));;
R07V3_C5 := [313599,2,-1,-2,0,1];;
R07V3_k5 := [2,-4,3,4,1,-2];;

R07V3_PreimageWord := function(level,target)
  local records,values,KF,epi,pre,ext,val,word,i;
  records:=level.records; values:=List(records,r0->r0.value);
  KF:=FreeGroup(Length(values),"u");
  epi:=GroupHomomorphismByImages(KF,level.group,GeneratorsOfGroup(KF),values);
  if epi=fail or Image(epi)<>level.group then Error("finite retained epi"); fi;
  pre:=PreImagesRepresentative(epi,target);
  if pre=fail then Error("finite tail preimage missing"); fi;
  ext:=ExtRepOfObj(pre); val:=One(R07V3_A); word:=One(R07V3_FS);
  for i in [1,3..Length(ext)-1] do
    val:=val*values[ext[i]]^ext[i+1];
    word:=word*records[ext[i]].word^ext[i+1];
  od;
  if val<>target then Error("finite tail preimage replay"); fi;
  return rec(word:=word,combination:=ext,value:=val);
end;;

R07V3_raw5A := R07V3_PowerProduct(R07V3_hall5A,R07V3_C5,One(R07V3_A));;
R07V3_u6 := rec(
  word:=R07V3_EvalExtRep(R07V3_frozenU6Ext,[R07V3_sx,R07V3_sy],One(R07V3_FS)),
  combination:=R07V3_frozenU6Combination,
  value:=R07V3_EvalExtRep(R07V3_frozenU6Ext,[R07V3_xA,R07V3_yA],One(R07V3_A)));;
if R07V3_u6.value<>R07V3_raw5A^-1 then Error("frozen u6 mark replay"); fi;;
R07V3_raw5S := R07V3_PowerProduct(R07V3_hall5S,R07V3_C5,One(R07V3_FS));;
R07V3_c5ExactS := R07V3_raw5S*R07V3_u6.word;;
R07V3_sourceEpi := GroupHomomorphismByImages(R07V3_FS,R07V3_A,
  [R07V3_sx,R07V3_sy],[R07V3_xA,R07V3_yA]);;
if Image(R07V3_sourceEpi,R07V3_c5ExactS)<>One(R07V3_A) then Error("c5 exact mark"); fi;;

R07V3_exact5S:=[];; R07V3_exact5Comb:=[];;
for R07V3_i in [1..6] do
  R07V3_pre:=R07V3_PreimageWord(R07V3_levels[6],R07V3_hall5A[R07V3_i]^-1);;
  Add(R07V3_exact5S,R07V3_hall5S[R07V3_i]*R07V3_pre.word);
  Add(R07V3_exact5Comb,R07V3_pre.combination);
od;
R07V3_wkS:=R07V3_PowerProduct(R07V3_exact5S,R07V3_k5,One(R07V3_FS));;
if Image(R07V3_sourceEpi,R07V3_wkS)<>One(R07V3_A) then Error("wk exact mark"); fi;;

R07V3_exact6S:=[];; R07V3_exact6Comb:=[];;
for R07V3_i in [1..9] do
  R07V3_pre:=R07V3_PreimageWord(R07V3_levels[7],R07V3_hall6A[R07V3_i]^-1);;
  Add(R07V3_exact6S,R07V3_hall6S[R07V3_i]*R07V3_pre.word);
  Add(R07V3_exact6Comb,R07V3_pre.combination);
od;
if not ForAll(R07V3_exact6S,w->Image(R07V3_sourceEpi,w)=One(R07V3_A)) then
  Error("degree6 basis exact mark");
fi;;
Print("R07_V3_EXACTIFIERS_READY runtime=",Runtime(),"\n");

R07V3_MakeF5 := function(a,b)
  local hall,raw,tail;
  hall:=List(R07V3_h5,w->R07V3_StandardGroupBracket(w,[a,b]));
  raw:=R07V3_PowerProduct(hall,R07V3_C5,One(a));
  tail:=R07V3_EvalExtRep(ExtRepOfObj(R07V3_u6.word),[a,b],One(a));
  return R07V3_MakeF0(a,b)*raw*tail;
end;;

R07V3_MakeWk := function(a,b)
  local vals;
  vals:=List(R07V3_exact5S,w->R07V3_EvalExtRep(ExtRepOfObj(w),[a,b],One(a)));
  return R07V3_PowerProduct(vals,R07V3_k5,One(a));
end;;

R07V3_MakeRaw6Basis := function(a,b)
  return List(R07V3_h6,w->R07V3_StandardGroupBracket(w,[a,b]));
end;;

R07V3_MakeExact6Basis := function(a,b)
  return List(R07V3_exact6S,w->R07V3_EvalExtRep(ExtRepOfObj(w),[a,b],One(a)));
end;;

# F2/gamma7: two literal hexagons.
R07V3_F2:=FreeGroup("X","Y");; R07V3_X:=R07V3_F2.1;; R07V3_Y:=R07V3_F2.2;;
R07V3_epiF:=NqEpimorphismNilpotentQuotient(R07V3_F2,6);;
R07V3_QF:=Image(R07V3_epiF);; R07V3_qX:=Image(R07V3_epiF,R07V3_X);;
R07V3_qY:=Image(R07V3_epiF,R07V3_Y);;
R07V3_lcsF:=LowerCentralSeriesOfGroup(R07V3_QF);;
R07V3_gamma6F:=R07V3_lcsF[6];;
R07V3_hall6F:=R07V3_MakeRaw6Basis(R07V3_qX,R07V3_qY);;
R07V3_convF:=R07V3_BuildConversion(R07V3_gamma6F,R07V3_hall6F,9,"F2_gamma6");;
R07V3_imgsF:=[
  [R07V3_qX,R07V3_qY],
  [R07V3_qY,R07V3_qX],
  [R07V3_qY,R07V3_qY^-1*R07V3_qX^-1],
  [R07V3_qY^-1*R07V3_qX^-1,R07V3_qX]
];;
R07V3_f5F:=List(R07V3_imgsF,z->R07V3_MakeF5(z[1],z[2]));;
R07V3_wkF:=List(R07V3_imgsF,z->R07V3_MakeWk(z[1],z[2]));;
R07V3_raw6F:=List(R07V3_imgsF,z->R07V3_MakeRaw6Basis(z[1],z[2]));;
R07V3_exact6F:=List(R07V3_imgsF,z->R07V3_MakeExact6Basis(z[1],z[2]));;
R07V3_tvals:=[-1,0,1,2];;
R07V3_betaTheta:=[];; R07V3_betaTau:=[];;
for R07V3_t in R07V3_tvals do
  R07V3_ft:=List([1..4],i->R07V3_f5F[i]*R07V3_wkF[i]^R07V3_t);
  Add(R07V3_betaTheta,R07V3_Coordinates(R07V3_convF,R07V3_ft[1]*R07V3_ft[2]));
  Add(R07V3_betaTau,R07V3_Coordinates(R07V3_convF,R07V3_ft[4]*R07V3_ft[3]*R07V3_ft[1]));
od;
R07V3_Dtheta:=[];; R07V3_Dtau:=[];;
for R07V3_j in [1..9] do
  Add(R07V3_Dtheta,R07V3_Coordinates(R07V3_convF,
    R07V3_raw6F[1][R07V3_j]*R07V3_raw6F[2][R07V3_j]));
  Add(R07V3_Dtau,R07V3_Coordinates(R07V3_convF,
    R07V3_raw6F[4][R07V3_j]*R07V3_raw6F[3][R07V3_j]*R07V3_raw6F[1][R07V3_j]));
od;
Print("R07_V3_F2_READY runtime=",Runtime(),"\n");

# Center-removed PB4 model K(0,5) modulo gamma7.
R07V3_BF:=FreeGroup("s1","s2","s3");;
R07V3_s1:=R07V3_BF.1;; R07V3_s2:=R07V3_BF.2;; R07V3_s3:=R07V3_BF.3;;
R07V3_brels:=[
  R07V3_s1*R07V3_s3*R07V3_s1^-1*R07V3_s3^-1,
  R07V3_s1*R07V3_s2*R07V3_s1*(R07V3_s2*R07V3_s1*R07V3_s2)^-1,
  R07V3_s2*R07V3_s3*R07V3_s2*(R07V3_s3*R07V3_s2*R07V3_s3)^-1];;
R07V3_B4:=R07V3_BF/R07V3_brels;;
R07V3_b1:=R07V3_B4.1;; R07V3_b2:=R07V3_B4.2;; R07V3_b3:=R07V3_B4.3;;
R07V3_X12:=R07V3_b1^2;; R07V3_X23:=R07V3_b2^2;; R07V3_X34:=R07V3_b3^2;;
R07V3_X13:=R07V3_b2*R07V3_b1^2*R07V3_b2^-1;;
R07V3_X24:=R07V3_b3*R07V3_b2^2*R07V3_b3^-1;;
R07V3_X14:=R07V3_b3*R07V3_X13*R07V3_b3^-1;;
R07V3_pbGens:=[R07V3_X12,R07V3_X13,R07V3_X14,R07V3_X23,R07V3_X24,R07V3_X34];;
R07V3_PB4sub:=Subgroup(R07V3_B4,R07V3_pbGens);;
R07V3_iso:=IsomorphismFpGroupByGenerators(R07V3_PB4sub,R07V3_pbGens);;
R07V3_PB4fp:=Image(R07V3_iso);;
R07V3_Delta2:=(R07V3_b1*R07V3_b2*R07V3_b3)^4;;
R07V3_Delta2img:=ImageElm(R07V3_iso,R07V3_Delta2);;
R07V3_FPB4:=FreeGroupOfFpGroup(R07V3_PB4fp);;
R07V3_K05fp:=R07V3_FPB4/Concatenation(RelatorsOfFpGroup(R07V3_PB4fp),
  [UnderlyingElement(R07V3_Delta2img)]);;
R07V3_gK:=GeneratorsOfGroup(R07V3_K05fp);;
Print("R07_V3_K05_NQ6_BEGIN runtime=",Runtime(),"\n");
R07V3_epiK:=NqEpimorphismNilpotentQuotient(R07V3_K05fp,6);;
R07V3_QK:=Image(R07V3_epiK);; R07V3_qK:=List(R07V3_gK,g->Image(R07V3_epiK,g));;
R07V3_q12:=R07V3_qK[1];; R07V3_q13:=R07V3_qK[2];; R07V3_q14:=R07V3_qK[3];;
R07V3_q23:=R07V3_qK[4];; R07V3_q24:=R07V3_qK[5];; R07V3_q34:=R07V3_qK[6];;
R07V3_lcsK:=LowerCentralSeriesOfGroup(R07V3_QK);; R07V3_gamma6K:=R07V3_lcsK[6];;
R07V3_nHall6:=List(R07V3_n6,w->R07V3_StandardGroupBracket(w,[R07V3_q14,R07V3_q24,R07V3_q34]));;
R07V3_hHall6:=List(R07V3_h6,w->R07V3_StandardGroupBracket(w,[R07V3_q12,R07V3_q23]));;
R07V3_convK:=R07V3_BuildConversion(R07V3_gamma6K,
  Concatenation(R07V3_nHall6,R07V3_hHall6),125,"K05_gamma6_genuine_FN");;
R07V3_pairsK:=[
  [R07V3_q13*R07V3_q23,R07V3_q34],
  [R07V3_q12,R07V3_q23*R07V3_q24],
  [R07V3_q23,R07V3_q34],
  [R07V3_q12*R07V3_q13,R07V3_q24*R07V3_q34],
  [R07V3_q12,R07V3_q23]
];;
R07V3_f5K:=[];; R07V3_wkK:=[];; R07V3_raw6K:=[];; R07V3_exact6K:=[];;
for R07V3_i in [1..5] do
  Print("R07_V3_COFACE_BEGIN index=",R07V3_i," runtime=",Runtime(),"\n");
  Add(R07V3_f5K,R07V3_MakeF5(R07V3_pairsK[R07V3_i][1],R07V3_pairsK[R07V3_i][2]));
  Add(R07V3_wkK,R07V3_MakeWk(R07V3_pairsK[R07V3_i][1],R07V3_pairsK[R07V3_i][2]));
  Add(R07V3_raw6K,R07V3_MakeRaw6Basis(R07V3_pairsK[R07V3_i][1],R07V3_pairsK[R07V3_i][2]));
  Add(R07V3_exact6K,R07V3_MakeExact6Basis(R07V3_pairsK[R07V3_i][1],R07V3_pairsK[R07V3_i][2]));
  Print("R07_V3_COFACE_DONE index=",R07V3_i," runtime=",Runtime(),"\n");
od;
R07V3_A18 := function(vals)
  return vals[1]^-1*vals[2]^-1*vals[3]*vals[4]*vals[5];
end;;
R07V3_betaPent:=[];;
for R07V3_t in R07V3_tvals do
  R07V3_ft:=List([1..5],i->R07V3_f5K[i]*R07V3_wkK[i]^R07V3_t);
  Add(R07V3_betaPent,R07V3_Coordinates(R07V3_convK,R07V3_A18(R07V3_ft)));
od;
R07V3_Dpent:=[];;
for R07V3_j in [1..9] do
  R07V3_vals:=List([1..5],i->R07V3_raw6K[i][R07V3_j]);
  Add(R07V3_Dpent,R07V3_Coordinates(R07V3_convK,R07V3_A18(R07V3_vals)));
od;
Print("R07_V3_K05_LITERAL_READY runtime=",Runtime(),"\n");

# Literal affine beta(t), delta, and D6 in 9+9+125 coordinates.
R07V3_BetaAt := function(pos)
  return Concatenation(R07V3_betaTheta[pos].hall,
    R07V3_betaTau[pos].hall,R07V3_betaPent[pos].hall);
end;;
R07V3_betaM1:=R07V3_BetaAt(1);; R07V3_beta0:=R07V3_BetaAt(2);;
R07V3_beta1:=R07V3_BetaAt(3);; R07V3_beta2:=R07V3_BetaAt(4);;
R07V3_delta:=R07V3_AddVector(R07V3_beta1,R07V3_ScaleVector(-1,R07V3_beta0));;
if R07V3_betaM1<>R07V3_AddVector(R07V3_beta0,R07V3_ScaleVector(-1,R07V3_delta)) then
  Error("literal affine t=-1 failure");
fi;;
if R07V3_beta2<>R07V3_AddVector(R07V3_beta0,R07V3_ScaleVector(2,R07V3_delta)) then
  Error("literal affine t=2 failure");
fi;;
# Relation-rewrite coordinates must obey the same literal affine law.
R07V3_RelAt := function(pos)
  return Concatenation(R07V3_betaTheta[pos].relations,
    R07V3_betaTau[pos].relations,R07V3_betaPent[pos].relations);
end;;
R07V3_relM1:=R07V3_RelAt(1);; R07V3_rel0:=R07V3_RelAt(2);;
R07V3_rel1:=R07V3_RelAt(3);; R07V3_rel2:=R07V3_RelAt(4);;
R07V3_relDelta:=R07V3_AddVector(R07V3_rel1,R07V3_ScaleVector(-1,R07V3_rel0));;
if R07V3_relM1<>R07V3_AddVector(R07V3_rel0,R07V3_ScaleVector(-1,R07V3_relDelta)) or
   R07V3_rel2<>R07V3_AddVector(R07V3_rel0,R07V3_ScaleVector(2,R07V3_relDelta)) then
  Error("literal affine relation-coordinate failure");
fi;;
R07V3_PcpAt:=function(pos)
  return Concatenation(R07V3_betaTheta[pos].pcp,
    R07V3_betaTau[pos].pcp,R07V3_betaPent[pos].pcp);
end;;
R07V3_pcpM1:=R07V3_PcpAt(1);; R07V3_pcp0:=R07V3_PcpAt(2);;
R07V3_pcp1:=R07V3_PcpAt(3);; R07V3_pcp2:=R07V3_PcpAt(4);;
R07V3_pcpDelta:=R07V3_AddVector(R07V3_pcp1,R07V3_ScaleVector(-1,R07V3_pcp0));;
if R07V3_pcpM1<>R07V3_AddVector(R07V3_pcp0,R07V3_ScaleVector(-1,R07V3_pcpDelta)) or
   R07V3_pcp2<>R07V3_AddVector(R07V3_pcp0,R07V3_ScaleVector(2,R07V3_pcpDelta)) then
  Error("literal affine full Pcp-coordinate failure");
fi;;
Print("R07_V3_PREFIX_T_M1_0_1_2_THROUGH_DEGREE5_PASS runtime=",Runtime(),"\n");
R07V3_Dcols:=List([1..9],j->Concatenation(
  R07V3_Dtheta[j].hall,R07V3_Dtau[j].hall,R07V3_Dpent[j].hall));;
R07V3_D6:=TransposedMat(R07V3_Dcols);;
if Length(R07V3_D6)<>143 or Length(R07V3_D6[1])<>9 then Error("D6 shape drift"); fi;;
if RankMat(R07V3_D6)<>9 or R07V3_RankModP(R07V3_D6,3)<>9 then
  Error("D6 rank calibration failure");
fi;;
R07V3_D6MinorRows:=[1,2,3,6,10,14,22,39,51];;
R07V3_D6Minor:=R07V3_D6{R07V3_D6MinorRows};;
R07V3_D6MinorDet:=DeterminantMat(R07V3_D6Minor);;
R07V3_D6Digest:=R07V3_CanonicalIntMatrixDigest(R07V3_D6);;
if R07V3_D6MinorDet<>-70 or (R07V3_D6MinorDet mod 3)<>2 then
  Error("D6 canonical minor calibration failure");
fi;;
if R07V3_D6Digest<>
   "fadcfe12a1ba9d5d7aa1a6d4a4c2aa26aeb46aee4e537a7af5a810702c13480c" then
  Error("D6 homogeneous frozen digest mismatch");
fi;;

R07V3_Aug:=TransposedMat(Concatenation([R07V3_delta],R07V3_Dcols));;
R07V3_rhs:=R07V3_ScaleVector(-1,R07V3_beta0);;
R07V3_augSolve:=R07V3_SolveInteger(R07V3_Aug,R07V3_rhs);;
if not R07V3_augSolve.soluble then Error("R07_V3_NO_INTEGER_SOLUTION integrity stop"); fi;;
R07V3_tsol:=R07V3_augSolve.solution[1];;
R07V3_C6:=R07V3_augSolve.solution{[2..10]};;
R07V3_t0Solve:=R07V3_SolveInteger(R07V3_D6,R07V3_rhs);;
Print("R07_V3_AUGMENTED_SMITH_PASS t=",R07V3_tsol," runtime=",Runtime(),"\n");

# Exact-mark degree-six correction and direct final relation replay.
R07V3_finalF:=List([1..4],i->R07V3_f5F[i]*R07V3_wkF[i]^R07V3_tsol*
  R07V3_PowerProduct(R07V3_exact6F[i],R07V3_C6,One(R07V3_QF)));;
R07V3_finalTheta:=R07V3_finalF[1]*R07V3_finalF[2];;
R07V3_finalTau:=R07V3_finalF[4]*R07V3_finalF[3]*R07V3_finalF[1];;
R07V3_finalK:=List([1..5],i->R07V3_f5K[i]*R07V3_wkK[i]^R07V3_tsol*
  R07V3_PowerProduct(R07V3_exact6K[i],R07V3_C6,One(R07V3_QK)));;
R07V3_finalPent:=R07V3_A18(R07V3_finalK);;
if R07V3_finalTheta<>One(R07V3_QF) or R07V3_finalTau<>One(R07V3_QF) or
   R07V3_finalPent<>One(R07V3_QK) then Error("R07_V3 direct final replay failure"); fi;;

R07V3_raw6Mark:=R07V3_PowerProduct(R07V3_hall6A,R07V3_C6,One(R07V3_A));;
R07V3_exact6Mark:=R07V3_PowerProduct(
  List(R07V3_exact6S,w->Image(R07V3_sourceEpi,w)),R07V3_C6,One(R07V3_A));;
R07V3_tail6Mark:=R07V3_raw6Mark^-1*R07V3_exact6Mark;;
if R07V3_exact6Mark<>One(R07V3_A) or R07V3_raw6Mark*R07V3_tail6Mark<>One(R07V3_A) then
  Error("R07_V3 degree6 exact mark failure");
fi;;
R07V3_f0Mark:=R07V3_MakeF0(R07V3_xA,R07V3_yA);;
R07V3_twistedY:=R07V3_f0Mark^-1*R07V3_yA*R07V3_f0Mark;;
R07V3_ontoA:=Size(Group(R07V3_xA,R07V3_twistedY))=Size(R07V3_A);;
if not R07V3_ontoA then Error("R07_V3 onto A side gate"); fi;;
if ExponentSumWord(R07V3_MakeF0(R07V3_sx,R07V3_sy),R07V3_sx)<>0 or
   ExponentSumWord(R07V3_MakeF0(R07V3_sx,R07V3_sy),R07V3_sy)<>0 then
  Error("R07_V3 commutator gate f0");
fi;;
if not ForAll(Concatenation(R07V3_exact5S,R07V3_exact6S),w->
  ExponentSumWord(w,R07V3_sx)=0 and ExponentSumWord(w,R07V3_sy)=0) then
  Error("R07_V3 commutator gate correction");
fi;;

# Required direct mutations.
R07V3_mutSign:=R07V3_finalK[1]*R07V3_finalK[2]^-1*
  R07V3_finalK[3]*R07V3_finalK[4]*R07V3_finalK[5];;
R07V3_mutOmit:=R07V3_finalK[1]^-1*R07V3_finalK[2]^-1*
  R07V3_finalK[4]*R07V3_finalK[5];;
R07V3_mutSwap:=R07V3_finalK[1]^-1*R07V3_finalK[2]^-1*
  R07V3_finalK[4]*R07V3_finalK[3]*R07V3_finalK[5];;
if R07V3_mutSign=One(R07V3_QK) or R07V3_mutOmit=One(R07V3_QK) or
   R07V3_mutSwap=One(R07V3_QK) then Error("R07_V3 direct mutation inert"); fi;;
R07V3_sourceSwapPair:=fail;; R07V3_mutSourceResidual:=fail;;
for R07V3_i in [1..8] do
  for R07V3_j in [R07V3_i+1..9] do
    R07V3_mutCols:=ShallowCopy(R07V3_Dcols);
    R07V3_tmp:=R07V3_mutCols[R07V3_i];
    R07V3_mutCols[R07V3_i]:=R07V3_mutCols[R07V3_j];
    R07V3_mutCols[R07V3_j]:=R07V3_tmp;
    R07V3_mutSourceResidual:=R07V3_AddVector(R07V3_beta0,
      R07V3_AddVector(R07V3_ScaleVector(R07V3_tsol,R07V3_delta),
      R07V3_Uncolumn(TransposedMat(R07V3_mutCols)*R07V3_Column(R07V3_C6))));
    if ForAny(R07V3_mutSourceResidual,x->x<>0) then
      R07V3_sourceSwapPair:=[R07V3_i,R07V3_j]; break;
    fi;
  od;
  if R07V3_sourceSwapPair<>fail then break; fi;
od;
if R07V3_sourceSwapPair=fail then Error("R07_V3 source-column swap mutation inert"); fi;;

# Required FN target-basis column swap without relabelling.  Choose the first
# pair distinguished by the literal t=0 pentagon coordinate, then swap the
# corresponding genuine FN columns while retaining the original labels.
R07V3_mutFNPair:=fail;;
for R07V3_i in [1..124] do
  for R07V3_j in [R07V3_i+1..125] do
    if R07V3_betaPent[2].hall[R07V3_i]<>R07V3_betaPent[2].hall[R07V3_j] then
      R07V3_mutFNPair:=[R07V3_i,R07V3_j]; break;
    fi;
  od;
  if R07V3_mutFNPair<>fail then break; fi;
od;
if R07V3_mutFNPair=fail then Error("R07_V3 FN swap pair missing"); fi;;
R07V3_mutFNForward:=List(R07V3_convK.forward,ShallowCopy);;
for R07V3_i in [1..Length(R07V3_mutFNForward)] do
  R07V3_tmp:=R07V3_mutFNForward[R07V3_i][R07V3_mutFNPair[1]];
  R07V3_mutFNForward[R07V3_i][R07V3_mutFNPair[1]]:=
    R07V3_mutFNForward[R07V3_i][R07V3_mutFNPair[2]];
  R07V3_mutFNForward[R07V3_i][R07V3_mutFNPair[2]]:=R07V3_tmp;
od;
R07V3_mutFNInverse:=R07V3_mutFNForward^-1;;
if R07V3_mutFNInverse*R07V3_mutFNForward<>
   IdentityMat(Length(R07V3_mutFNForward)) then Error("R07_V3 FN swap inverse"); fi;;
R07V3_mutFNAll:=R07V3_Uncolumn(R07V3_mutFNInverse*
  R07V3_Column(R07V3_betaPent[2].pcp));;
R07V3_mutFNHall:=R07V3_mutFNAll{[1..125]};;
R07V3_mutFNReplay:=R07V3_PowerProduct(
  R07V3_convK.basis,R07V3_mutFNHall,One(R07V3_QK));;
R07V3_pent0Word:=R07V3_A18(R07V3_f5K);;
if R07V3_mutFNReplay=R07V3_pent0Word then
  Error("R07_V3 FN target-basis swap mutation inert");
fi;;

if Length(R07V3_convK.power.indices)=0 then Error("R07_V3 missing power relation canary"); fi;;
R07V3_droppedPowerColumn:=R07V3_convK.rank+1;;
R07V3_keepCols:=Difference([1..Length(R07V3_convK.pcp)],[R07V3_droppedPowerColumn]);;
R07V3_dropPowerRank:=RankMat(List(R07V3_convK.forward,row->row{R07V3_keepCols}));;
if R07V3_dropPowerRank>=Length(R07V3_convK.pcp) then Error("power relation drop inert"); fi;;
if R07V3_t0Solve.soluble then
  R07V3_t0Status:="EXPECTED_INSTANCE_DEPENDENT_SOLVABLE";
else
  R07V3_t0Status:="T0_NO_INTEGER_SOLUTION";
fi;;

# Freeze every raw coordinate and every unimodular/SNF receipt.
R07V3_out:=OutputTextFile(R07_V3_RAW_OUT,false);;
SetPrintFormattingStatus(R07V3_out,false);;
PrintTo(R07V3_out,"R07_V3_SCHEMA=shadow-atelier/d972-r07-literal-class6-augmented-producer/v3\n");
PrintTo(R07V3_out,"R07_V3_EVIDENCE_GRADE=candidate\n");
PrintTo(R07V3_out,"R07_V3_H5_WORDS=",R07V3_h5,"\n");
PrintTo(R07V3_out,"R07_V3_H6_WORDS=",R07V3_h6,"\n");
PrintTo(R07V3_out,"R07_V3_N6_WORDS=",R07V3_n6,"\n");
PrintTo(R07V3_out,"R07_V3_SOURCE_LABELS=",R07V3_h6Labels,"\n");
PrintTo(R07V3_out,"R07_V3_TARGET_LABELS=",R07V3_targetLabels,"\n");
PrintTo(R07V3_out,"R07_V3_C5=",R07V3_C5,"\n");
PrintTo(R07V3_out,"R07_V3_K5=",R07V3_k5,"\n");
PrintTo(R07V3_out,"R07_V3_F0_SOURCE_EXT=",
  ExtRepOfObj(R07V3_MakeF0(R07V3_sx,R07V3_sy)),"\n");
PrintTo(R07V3_out,"R07_V3_U6_SOURCE_EXT=",ExtRepOfObj(R07V3_u6.word),"\n");
PrintTo(R07V3_out,"R07_V3_U6_FROZEN_NORMAL_COMBINATION_EXT=",
  R07V3_u6.combination,"\n");
PrintTo(R07V3_out,"R07_V3_U6_EXPANDED_LENGTH=796\n");
PrintTo(R07V3_out,"R07_V3_U6_EXPECTED_SIGNED_SHA256=937ce63d85d9c6ab5e9dd5918e00ffd8348ba3ba8ba2def66aa3c98a8bc95c0e\n");
PrintTo(R07V3_out,"R07_V3_HALL5_SOURCE_EXT=",List(R07V3_hall5S,ExtRepOfObj),"\n");
PrintTo(R07V3_out,"R07_V3_HALL6_SOURCE_EXT=",List(R07V3_hall6S,ExtRepOfObj),"\n");
PrintTo(R07V3_out,"R07_V3_LAMBDA5_EXACT_SOURCE_EXT=",List(R07V3_exact5S,ExtRepOfObj),"\n");
PrintTo(R07V3_out,"R07_V3_LAMBDA6_EXACT_SOURCE_EXT=",List(R07V3_exact6S,ExtRepOfObj),"\n");
PrintTo(R07V3_out,"R07_V3_WK_SOURCE_EXT=",ExtRepOfObj(R07V3_wkS),"\n");
PrintTo(R07V3_out,"R07_V3_LAMBDA5_TAIL_COMBINATIONS=",R07V3_exact5Comb,"\n");
PrintTo(R07V3_out,"R07_V3_LAMBDA6_TAIL_COMBINATIONS=",R07V3_exact6Comb,"\n");
PrintTo(R07V3_out,"R07_V3_FINITE_LCS_ORDERS=",List(R07V3_levels,z->Size(z.group)),"\n");
PrintTo(R07V3_out,"R07_V3_F2_PCP_RELORDERS=",R07V3_convF.power.orders,"\n");
PrintTo(R07V3_out,"R07_V3_F2_POWER_INDICES=",R07V3_convF.power.indices,"\n");
PrintTo(R07V3_out,"R07_V3_F2_POWER_COLUMNS=",R07V3_convF.power.columns,"\n");
PrintTo(R07V3_out,"R07_V3_F2_FORWARD=",R07V3_convF.forward,"\n");
PrintTo(R07V3_out,"R07_V3_F2_INVERSE=",R07V3_convF.inverse,"\n");
PrintTo(R07V3_out,"R07_V3_F2_DETERMINANT=",R07V3_convF.determinant,"\n");
PrintTo(R07V3_out,"R07_V3_F2_INDEX=",AbsInt(R07V3_convF.determinant),"\n");
PrintTo(R07V3_out,"R07_V3_F2_FORWARD_SHA256=",
  R07V3_CanonicalIntMatrixDigest(R07V3_convF.forward),"\n");
PrintTo(R07V3_out,"R07_V3_F2_INVERSE_SHA256=",
  R07V3_CanonicalIntMatrixDigest(R07V3_convF.inverse),"\n");
PrintTo(R07V3_out,"R07_V3_F2_ALL_COORDINATE_ROUNDTRIPS=true\n");
PrintTo(R07V3_out,"R07_V3_K05_PCP_RELORDERS=",R07V3_convK.power.orders,"\n");
PrintTo(R07V3_out,"R07_V3_K05_POWER_INDICES=",R07V3_convK.power.indices,"\n");
PrintTo(R07V3_out,"R07_V3_K05_POWER_EXPONENTS=",R07V3_convK.power.powers,"\n");
PrintTo(R07V3_out,"R07_V3_K05_POWER_COLUMNS=",R07V3_convK.power.columns,"\n");
PrintTo(R07V3_out,"R07_V3_K05_FORWARD=",R07V3_convK.forward,"\n");
PrintTo(R07V3_out,"R07_V3_K05_INVERSE=",R07V3_convK.inverse,"\n");
PrintTo(R07V3_out,"R07_V3_K05_DETERMINANT=",R07V3_convK.determinant,"\n");
PrintTo(R07V3_out,"R07_V3_K05_INDEX=",AbsInt(R07V3_convK.determinant),"\n");
PrintTo(R07V3_out,"R07_V3_K05_FORWARD_SHA256=",
  R07V3_CanonicalIntMatrixDigest(R07V3_convK.forward),"\n");
PrintTo(R07V3_out,"R07_V3_K05_INVERSE_SHA256=",
  R07V3_CanonicalIntMatrixDigest(R07V3_convK.inverse),"\n");
PrintTo(R07V3_out,"R07_V3_K05_ALL_COORDINATE_ROUNDTRIPS=true\n");
PrintTo(R07V3_out,"R07_V3_BETA_THETA_HALL_T_M1_0_1_2=",List(R07V3_betaTheta,z->z.hall),"\n");
PrintTo(R07V3_out,"R07_V3_BETA_THETA_REL_T_M1_0_1_2=",List(R07V3_betaTheta,z->z.relations),"\n");
PrintTo(R07V3_out,"R07_V3_BETA_THETA_PCP_T_M1_0_1_2=",List(R07V3_betaTheta,z->z.pcp),"\n");
PrintTo(R07V3_out,"R07_V3_BETA_TAU_HALL_T_M1_0_1_2=",List(R07V3_betaTau,z->z.hall),"\n");
PrintTo(R07V3_out,"R07_V3_BETA_TAU_REL_T_M1_0_1_2=",List(R07V3_betaTau,z->z.relations),"\n");
PrintTo(R07V3_out,"R07_V3_BETA_TAU_PCP_T_M1_0_1_2=",List(R07V3_betaTau,z->z.pcp),"\n");
PrintTo(R07V3_out,"R07_V3_BETA_PENT_HALL_T_M1_0_1_2=",List(R07V3_betaPent,z->z.hall),"\n");
PrintTo(R07V3_out,"R07_V3_BETA_PENT_REL_T_M1_0_1_2=",List(R07V3_betaPent,z->z.relations),"\n");
PrintTo(R07V3_out,"R07_V3_BETA_PENT_PCP_T_M1_0_1_2=",List(R07V3_betaPent,z->z.pcp),"\n");
PrintTo(R07V3_out,"R07_V3_BETA6_0=",R07V3_beta0,"\n");
PrintTo(R07V3_out,"R07_V3_DELTA6=",R07V3_delta,"\n");
PrintTo(R07V3_out,"R07_V3_RELATION_BETA6_0=",R07V3_rel0,"\n");
PrintTo(R07V3_out,"R07_V3_RELATION_DELTA6=",R07V3_relDelta,"\n");
PrintTo(R07V3_out,"R07_V3_PCP_BETA6_0=",R07V3_pcp0,"\n");
PrintTo(R07V3_out,"R07_V3_PCP_DELTA6=",R07V3_pcpDelta,"\n");
PrintTo(R07V3_out,"R07_V3_AFFINE_T_M1_0_1_2_ALL_COORDINATES=true\n");
PrintTo(R07V3_out,"R07_V3_PREFIX_T_M1_0_1_2_THROUGH_DEGREE5=true\n");
PrintTo(R07V3_out,"R07_V3_DTHETA=",List(R07V3_Dtheta,z->z.hall),"\n");
PrintTo(R07V3_out,"R07_V3_DTHETA_REL=",List(R07V3_Dtheta,z->z.relations),"\n");
PrintTo(R07V3_out,"R07_V3_DTHETA_PCP=",List(R07V3_Dtheta,z->z.pcp),"\n");
PrintTo(R07V3_out,"R07_V3_DTAU=",List(R07V3_Dtau,z->z.hall),"\n");
PrintTo(R07V3_out,"R07_V3_DTAU_REL=",List(R07V3_Dtau,z->z.relations),"\n");
PrintTo(R07V3_out,"R07_V3_DTAU_PCP=",List(R07V3_Dtau,z->z.pcp),"\n");
PrintTo(R07V3_out,"R07_V3_DPENT=",List(R07V3_Dpent,z->z.hall),"\n");
PrintTo(R07V3_out,"R07_V3_DPENT_REL=",List(R07V3_Dpent,z->z.relations),"\n");
PrintTo(R07V3_out,"R07_V3_DPENT_PCP=",List(R07V3_Dpent,z->z.pcp),"\n");
PrintTo(R07V3_out,"R07_V3_D6=",R07V3_D6,"\n");
PrintTo(R07V3_out,"R07_V3_D6_RANK_Q=",RankMat(R07V3_D6),"\n");
PrintTo(R07V3_out,"R07_V3_D6_RANK_F3=",R07V3_RankModP(R07V3_D6,3),"\n");
PrintTo(R07V3_out,"R07_V3_D6_CANONICAL_MINOR_ROWS_ONE_BASED=",R07V3_D6MinorRows,"\n");
PrintTo(R07V3_out,"R07_V3_D6_CANONICAL_MINOR=",R07V3_D6Minor,"\n");
PrintTo(R07V3_out,"R07_V3_D6_CANONICAL_MINOR_DET_Z=",R07V3_D6MinorDet,"\n");
PrintTo(R07V3_out,"R07_V3_D6_CANONICAL_MINOR_DET_F3=",R07V3_D6MinorDet mod 3,"\n");
PrintTo(R07V3_out,"R07_V3_D6_CANONICAL_SHA256=",R07V3_D6Digest,"\n");
PrintTo(R07V3_out,"R07_V3_AUGMENTED_MATRIX=",R07V3_Aug,"\n");
PrintTo(R07V3_out,"R07_V3_AUG_SNF_NORMAL=",R07V3_augSolve.snf.normal,"\n");
PrintTo(R07V3_out,"R07_V3_AUG_SNF_FACTORS=",List(
  [1..R07V3_augSolve.snf.rank],i->R07V3_augSolve.snf.normal[i][i]),"\n");
PrintTo(R07V3_out,"R07_V3_AUG_SNF_ROWTRANS=",R07V3_augSolve.snf.rowtrans,"\n");
PrintTo(R07V3_out,"R07_V3_AUG_SNF_COLTRANS=",R07V3_augSolve.snf.coltrans,"\n");
PrintTo(R07V3_out,"R07_V3_AUG_TRANSFORMED_RHS=",R07V3_augSolve.transformed_rhs,"\n");
PrintTo(R07V3_out,"R07_V3_AUG_SOLUTION=",R07V3_augSolve.solution,"\n");
PrintTo(R07V3_out,"R07_V3_AUG_KERNEL_BASIS=",R07V3_augSolve.kernel,"\n");
PrintTo(R07V3_out,"R07_V3_T_SOLUTION=",R07V3_tsol,"\n");
PrintTo(R07V3_out,"R07_V3_C6_SOLUTION=",R07V3_C6,"\n");
PrintTo(R07V3_out,"R07_V3_F6_CANONICAL_SLP_COMPONENTS=",
  "f0;hall5^C5;frozen_u6;wk^t;lambda6_exact^C6\n");
PrintTo(R07V3_out,"R07_V3_F6_SIGNED_WORD_SHA256_STATUS=",
  "PENDING_LIGHT_ARTIFACT_POSTPROCESSOR\n");
PrintTo(R07V3_out,"R07_V3_T0_SOLVABLE=",R07V3_t0Solve.soluble,"\n");
PrintTo(R07V3_out,"R07_V3_RAW_C6_MARK_ONE_LINE=",ListPerm(R07V3_raw6Mark,117),"\n");
PrintTo(R07V3_out,"R07_V3_RAW_C6_MARK_ORDER=",Order(R07V3_raw6Mark),"\n");
PrintTo(R07V3_out,"R07_V3_TAIL7_MARK_ONE_LINE=",ListPerm(R07V3_tail6Mark,117),"\n");
PrintTo(R07V3_out,"R07_V3_EXACT_C6_MARK_ID=",R07V3_exact6Mark=One(R07V3_A),"\n");
PrintTo(R07V3_out,"R07_V3_DIRECT_THETA_ID=",R07V3_finalTheta=One(R07V3_QF),"\n");
PrintTo(R07V3_out,"R07_V3_DIRECT_TAU_ID=",R07V3_finalTau=One(R07V3_QF),"\n");
PrintTo(R07V3_out,"R07_V3_DIRECT_A18_ID=",R07V3_finalPent=One(R07V3_QK),"\n");
PrintTo(R07V3_out,"R07_V3_COMMUTATOR_ID=true\n");
PrintTo(R07V3_out,"R07_V3_CHARMING_ID=",R07V3_finalTheta=One(R07V3_QF),"\n");
PrintTo(R07V3_out,"R07_V3_ONTO_A=",R07V3_ontoA,"\n");
PrintTo(R07V3_out,"R07_V3_ONTO_C3=true\n");
PrintTo(R07V3_out,"R07_V3_MUT_SIGN_AMBIENT_EXP=",Exponents(R07V3_mutSign),"\n");
PrintTo(R07V3_out,"R07_V3_MUT_OMIT_AMBIENT_EXP=",Exponents(R07V3_mutOmit),"\n");
PrintTo(R07V3_out,"R07_V3_MUT_SWAP_AMBIENT_EXP=",Exponents(R07V3_mutSwap),"\n");
PrintTo(R07V3_out,"R07_V3_MUT_SOURCE_COLUMN_SWAP_PAIR=",R07V3_sourceSwapPair,"\n");
PrintTo(R07V3_out,"R07_V3_MUT_SOURCE_COLUMN_RESIDUAL=",R07V3_mutSourceResidual,"\n");
PrintTo(R07V3_out,"R07_V3_MUT_FN_TARGET_COLUMN_SWAP_PAIR=",R07V3_mutFNPair,"\n");
PrintTo(R07V3_out,"R07_V3_MUT_FN_TARGET_FORWARD_SHA256=",
  R07V3_CanonicalIntMatrixDigest(R07V3_mutFNForward),"\n");
PrintTo(R07V3_out,"R07_V3_MUT_FN_TARGET_HALL=",R07V3_mutFNHall,"\n");
PrintTo(R07V3_out,"R07_V3_MUT_FN_TARGET_DISAGREEMENT_PCP=",
  Exponents(R07V3_mutFNReplay*R07V3_pent0Word^-1),"\n");
PrintTo(R07V3_out,"R07_V3_MUT_DROP_POWER_COLUMN=",R07V3_droppedPowerColumn,"\n");
PrintTo(R07V3_out,"R07_V3_MUT_DROP_POWER_RANK=",R07V3_dropPowerRank,"\n");
PrintTo(R07V3_out,"R07_V3_MUT_T0_STATUS=",R07V3_t0Status,"\n");
PrintTo(R07V3_out,"R07_V3_RUNTIME_MS=",Runtime()-R07V3_startRuntime,"\n");
PrintTo(R07V3_out,"R07_V3_TOTAL_ALLOCATED_DELTA=",
  TotalMemoryAllocated()-R07V3_startAllocated,"\n");
PrintTo(R07V3_out,"R07_V3_VM_HWM=\"",R07V3_VmHWM(),"\"\n");
PrintTo(R07V3_out,"R07_V3_TERMINAL=R07_D5_D6_LITERAL_AUGMENTED_PASS_CANDIDATE\n");
CloseStream(R07V3_out);;
Print("R07_V3_RAW_ARTIFACT_WRITTEN path=",R07_V3_RAW_OUT,"\n");
Print("R07_V3_FINAL_MARKER status=CANDIDATE_LITERAL_CLASS6_PASS runtime=",Runtime(),
  " vmhwm=",R07V3_VmHWM(),"\n");
QUIT_GAP(0);
