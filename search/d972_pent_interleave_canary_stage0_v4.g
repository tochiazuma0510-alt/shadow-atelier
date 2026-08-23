#############################################################################
## D972 corrected pentagon canary: Linux NQ portability repair, stage 0 v4.
##
## This wrapper does not change the mathematics or the frozen v1 producer.
## It authenticates the bundled NQ 2.5.11 sources, builds its missing UNIX
## executable in place when necessary, loads NQ, and delegates to v1.  Any
## missing/multiple package path, source drift, build failure, executable
## ambiguity, or calibration failure stops before the v4 final marker.
#############################################################################

P159V4V1Path := "search/d972_pent_interleave_canary_producer_v1.g";
P159V4V1Sha :=
  "c21b7758f244997d1da9c15c3b09b71a13b1995b379596c849a8eacccc202d6d";
P159V4NqVersion := "2.5.11";
P159V4PackageInfoSha :=
  "e5e3370aa823163909a5130f1d803f43051e606305915718bcf7a363e5af5264";
P159V4ConfigureSha :=
  "4c09599a55cbdf0eb22998280e197f64ebb2e6ca5ca884b80e3e8d55c1ca0bd0";
P159V4MakefileInSha :=
  "84def846c51b5fe54b79b1ca312ac5629c383ccadbe43349da4d40efa9c5d003";
P159V4NqGapGiSha :=
  "a274e10aca9a453c565e66ec0337e80ab01658ef3eb1be094f292d8132f4c749";
P159V4NqFunctionsXmlSha :=
  "f693fd6f8919ee8abf05eb77862b23ed5b2376ca4a63e1cdfe8e27446a311d7b";

P159V4ReadOneLine := function(path,label)
  local raw,body;
  raw := StringFile(path);
  if raw=fail then Error("PENT159N_V4: missing ",label," at ",path); fi;
  if Length(raw)<2 or raw[Length(raw)]<>'\n' then
    Error("PENT159N_V4: ",label," is not one LF-terminated line");
  fi;
  body := raw{[1..Length(raw)-1]};
  if Length(body)=0 or Position(body,'\n')<>fail or
     Position(body,'\r')<>fail then
    Error("PENT159N_V4: malformed ",label);
  fi;
  return body;
end;

P159V4IsLowerHexSha := function(s)
  return Length(s)=64 and ForAll(s,c -> c in "0123456789abcdef");
end;

P159V4ShellQuote := function(s)
  if Position(s,'\n') <> fail or Position(s,'\r') <> fail then
    Error("PENT159N_V4: newline in shell argument");
  fi;
  return Concatenation("'",ReplacedString(s,"'","'\"'\"'"),"'");
end;

P159V4RequireFileSha := function(path,expected,label)
  local src,actual;
  src := StringFile(path);
  if src=fail then Error("PENT159N_V4: missing ",label," at ",path); fi;
  actual := HexSHA256(src);
  if actual<>expected then
    Error("PENT159N_V4: ",label," SHA drift: ",actual);
  fi;
  return actual;
end;

P159V4Infos := PackageInfo("nq");
if Length(P159V4Infos)<>1 then
  Error("PENT159N_V4: expected exactly one bundled NQ PackageInfo entry");
fi;
P159V4Info := P159V4Infos[1];
if not IsBound(P159V4Info.Version) or
   P159V4Info.Version<>P159V4NqVersion then
  Error("PENT159N_V4: NQ version drift");
fi;
if not IsBound(P159V4Info.InstallationPath) then
  Error("PENT159N_V4: NQ InstallationPath missing");
fi;
P159V4NqPath := P159V4Info.InstallationPath;
if PositionSublist(LowercaseString(GAPInfo.Architecture),"linux")=fail then
  Error("PENT159N_V4: this portability stage is Linux-only");
fi;
if not IsString(P159V4NqPath) or Length(P159V4NqPath)<2 or
   P159V4NqPath[Length(P159V4NqPath)]<>'/' then
  Error("PENT159N_V4: NQ InstallationPath is not a trailing-slash path");
fi;
if not IsBound(GAPInfo.RootPaths) or not IsList(GAPInfo.RootPaths) then
  Error("PENT159N_V4: GAPInfo.RootPaths unavailable");
fi;

## Derive GAPROOT without GetEnv: the NQ InstallationPath must be exactly one
## direct child of the pkg/ directory under exactly one GAP-native root.
P159V4GapRootCandidates := [];
for P159V4RootCandidate in GAPInfo.RootPaths do
  if IsString(P159V4RootCandidate) and Length(P159V4RootCandidate)>0 then
    if P159V4RootCandidate[Length(P159V4RootCandidate)]<>'/' then
      P159V4RootCandidate := Concatenation(P159V4RootCandidate,"/");
    fi;
    P159V4ParentCandidate := Concatenation(P159V4RootCandidate,"pkg/");
    if Length(P159V4NqPath)>Length(P159V4ParentCandidate) and
       PositionSublist(P159V4NqPath,P159V4ParentCandidate)=1 then
      P159V4TailCandidate := P159V4NqPath{
        [Length(P159V4ParentCandidate)+1..Length(P159V4NqPath)]};
      if Length(P159V4TailCandidate)>=2 and
         P159V4TailCandidate[Length(P159V4TailCandidate)]='/' and
         Position(P159V4TailCandidate{
           [1..Length(P159V4TailCandidate)-1]},'/')=fail and
         Position(P159V4GapRootCandidates,P159V4RootCandidate)=fail then
        Add(P159V4GapRootCandidates,P159V4RootCandidate);
      fi;
    fi;
  fi;
od;
if Length(P159V4GapRootCandidates)<>1 then
  Error("PENT159N_V4: NQ does not identify exactly one GAP-native root");
fi;
P159V4GapRoot := P159V4GapRootCandidates[1];
P159V4PackageParent := Concatenation(P159V4GapRoot,"pkg/");
P159V4NqDirectoryName := P159V4NqPath{
  [Length(P159V4PackageParent)+1..Length(P159V4NqPath)-1]};
if P159V4NqPath<>
   Concatenation(P159V4PackageParent,P159V4NqDirectoryName,"/") then
  Error("PENT159N_V4: NQ package-parent equality gate failed");
fi;

P159V4PackageInfoPath := Concatenation(P159V4NqPath,"PackageInfo.g");
P159V4ConfigurePath := Concatenation(P159V4NqPath,"configure");
P159V4MakefileInPath := Concatenation(P159V4NqPath,"Makefile.in");
P159V4NqGapGiPath := Concatenation(P159V4NqPath,"gap/nq.gi");
P159V4NqFunctionsXmlPath := Concatenation(P159V4NqPath,"doc/functions.xml");
P159V4RequireFileSha(P159V4PackageInfoPath,P159V4PackageInfoSha,
  "NQ PackageInfo.g");
P159V4RequireFileSha(P159V4ConfigurePath,P159V4ConfigureSha,
  "NQ configure");
P159V4RequireFileSha(P159V4MakefileInPath,P159V4MakefileInSha,
  "NQ Makefile.in");
P159V4RequireFileSha(P159V4NqGapGiPath,P159V4NqGapGiSha,"NQ gap/nq.gi");
P159V4RequireFileSha(P159V4NqFunctionsXmlPath,P159V4NqFunctionsXmlSha,
  "NQ doc/functions.xml");
Print("PENT159N_NQ_SOURCE_PIN_PASS version=",P159V4NqVersion,
  " gap_root=",P159V4GapRoot,
  " package_parent=",P159V4PackageParent,
  " package_path=",P159V4NqPath,
  " packageinfo_sha256=",P159V4PackageInfoSha,
  " configure_sha256=",P159V4ConfigureSha,
  " makefile_in_sha256=",P159V4MakefileInSha,"\n");
Print("PENT159N_NQ_API_PROVENANCE_PASS version=",P159V4NqVersion,
  " implementation=gap/nq.gi implementation_sha256=",P159V4NqGapGiSha,
  " manual=doc/functions.xml manual_sha256=",P159V4NqFunctionsXmlSha,
  " direct_method_lines=628-640 epimorphism_subgroup_lines=679-686\n");

P159V4OutRoot := Filename(DirectoryCurrent(),"ci/out");
P159V4ConfigureLog := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_configure_v4.log");
P159V4MakeLog := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_make_v4.log");
P159V4ShellRawPathFile := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_shell_path_raw_v4.txt");
P159V4ShellCanonicalPathFile := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_shell_path_realpath_v4.txt");
P159V4GapRawPathFile := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_gap_path_raw_v4.txt");
P159V4GapCanonicalPathFile := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_gap_path_realpath_v4.txt");
P159V4BinaryShaFile := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_binary_sha256_v4.txt");
P159V4GeneratedMakefileShaFile := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_generated_makefile_sha256_v4.txt");
P159V4BuildSentinel := Concatenation(P159V4OutRoot,
  "/d972_pent159n_nq_build_v4.ok");

P159V4NqExeBefore := Filename(DirectoriesPackagePrograms("nq"),"nq");
P159V4Built := false;
if P159V4NqExeBefore=fail then
  P159V4BuildCommand := Concatenation(
    "set -eu; ",
    "rm -f ",P159V4ShellQuote(P159V4ConfigureLog)," ",
      P159V4ShellQuote(P159V4MakeLog)," ",
      P159V4ShellQuote(P159V4ShellRawPathFile)," ",
      P159V4ShellQuote(P159V4ShellCanonicalPathFile)," ",
      P159V4ShellQuote(P159V4GapRawPathFile)," ",
      P159V4ShellQuote(P159V4GapCanonicalPathFile)," ",
      P159V4ShellQuote(P159V4BinaryShaFile)," ",
      P159V4ShellQuote(P159V4GeneratedMakefileShaFile)," ",
      P159V4ShellQuote(P159V4BuildSentinel),"; ",
    "cd ",P159V4ShellQuote(P159V4NqPath),"; ",
    "test -x ./configure; ",
    "./configure --with-gaproot=",P159V4ShellQuote(P159V4GapRoot),
      " > ",P159V4ShellQuote(P159V4ConfigureLog)," 2>&1; ",
    "make -j2 > ",P159V4ShellQuote(P159V4MakeLog)," 2>&1; ",
    "sha256sum Makefile | cut -d ' ' -f1 > ",
      P159V4ShellQuote(P159V4GeneratedMakefileShaFile),"; ",
    "printf 'PENT159N_NQ_BUILD_SHELL_PASS\\n' > ",
      P159V4ShellQuote(P159V4BuildSentinel));
  Exec(P159V4BuildCommand);
  if StringFile(P159V4BuildSentinel)<>
     "PENT159N_NQ_BUILD_SHELL_PASS\n" then
    Error("PENT159N_V4: NQ configure/make did not produce exact sentinel");
  fi;
  P159V4Built := true;
fi;

## Discover independently through the package bin tree, and canonicalize the
## shell representation before asking GAP for its representation.
P159V4ShellDiscoverCommand := Concatenation(
  "set -eu; command -v realpath >/dev/null; ",
  "rm -f ",P159V4ShellQuote(P159V4ShellRawPathFile)," ",
    P159V4ShellQuote(P159V4ShellCanonicalPathFile)," ",
    P159V4ShellQuote(P159V4GapRawPathFile)," ",
    P159V4ShellQuote(P159V4GapCanonicalPathFile)," ",
    P159V4ShellQuote(P159V4BinaryShaFile),"; ",
  "nq_bin=$(find ",P159V4ShellQuote(Concatenation(P159V4NqPath,"bin")),
    " -type f -name nq -perm -111 -print); ",
  "test -n \"$nq_bin\"; ",
  "test \"$(printf '%s\\n' \"$nq_bin\" | wc -l)\" -eq 1; ",
  "printf '%s\\n' \"$nq_bin\" > ",
    P159V4ShellQuote(P159V4ShellRawPathFile),"; ",
  "nq_real=$(realpath -- \"$nq_bin\"); test -n \"$nq_real\"; ",
  "printf '%s\\n' \"$nq_real\" > ",
    P159V4ShellQuote(P159V4ShellCanonicalPathFile),"; ",
  "sha256sum \"$nq_real\" | cut -d ' ' -f1 > ",
    P159V4ShellQuote(P159V4BinaryShaFile));
Exec(P159V4ShellDiscoverCommand);
P159V4ShellRawPath := P159V4ReadOneLine(P159V4ShellRawPathFile,
  "shell-discovered NQ raw path");
P159V4ShellCanonicalPath := P159V4ReadOneLine(
  P159V4ShellCanonicalPathFile,"shell-discovered NQ realpath");

P159V4NqExe := Filename(DirectoriesPackagePrograms("nq"),"nq");
if P159V4NqExe=fail then
  Error("PENT159N_V4: NQ executable still unavailable after portability stage");
fi;
Print("PENT159N_NQ_PATH_RAW shell=",P159V4ShellRawPath,
  " gap=",P159V4NqExe,"\n");
P159V4GapCanonicalizeCommand := Concatenation(
  "set -eu; command -v realpath >/dev/null; ",
  "printf '%s\\n' ",P159V4ShellQuote(P159V4NqExe)," > ",
    P159V4ShellQuote(P159V4GapRawPathFile),"; ",
  "realpath -- ",P159V4ShellQuote(P159V4NqExe)," > ",
    P159V4ShellQuote(P159V4GapCanonicalPathFile));
Exec(P159V4GapCanonicalizeCommand);
P159V4GapRecordedRawPath := P159V4ReadOneLine(P159V4GapRawPathFile,
  "GAP-discovered NQ raw path");
P159V4GapCanonicalPath := P159V4ReadOneLine(P159V4GapCanonicalPathFile,
  "GAP-discovered NQ realpath");
if P159V4GapRecordedRawPath<>P159V4NqExe then
  Error("PENT159N_V4: GAP raw-path recording mismatch");
fi;
Print("PENT159N_NQ_PATH_CANONICAL shell=",P159V4ShellCanonicalPath,
  " gap=",P159V4GapCanonicalPath,"\n");
if P159V4ShellCanonicalPath<>P159V4GapCanonicalPath then
  Error("PENT159N_V4: canonical shell/GAP NQ executable path mismatch");
fi;
Print("PENT159N_NQ_PATH_EQUIVALENCE_PASS realpath=",
  P159V4ShellCanonicalPath,"\n");
P159V4BinarySha := P159V4ReadOneLine(P159V4BinaryShaFile,
  "NQ executable SHA record");
if not P159V4IsLowerHexSha(P159V4BinarySha) then
  Error("PENT159N_V4: malformed NQ executable SHA record");
fi;
if P159V4Built then
  P159V4GeneratedMakefileSha := P159V4ReadOneLine(
    P159V4GeneratedMakefileShaFile,"generated Makefile SHA record");
  if not P159V4IsLowerHexSha(P159V4GeneratedMakefileSha) then
    Error("PENT159N_V4: malformed generated Makefile SHA record");
  fi;
  Print("PENT159N_NQ_BUILD_PASS version=",P159V4NqVersion,
    " gap_root=",P159V4GapRoot,
    " package_path=",P159V4NqPath,
    " configure_argv0=./configure configure_argv1=--with-gaproot=",
      P159V4GapRoot,
    " make_argv0=make make_argv1=-j2",
    " generated_makefile_sha256=",P159V4GeneratedMakefileSha,
    " executable=",P159V4NqExe,
    " executable_sha256=",P159V4BinarySha,"\n");
else
  Print("PENT159N_NQ_PREBUILT_PRESENT version=",P159V4NqVersion,
    " package_path=",P159V4NqPath,
    " executable=",P159V4NqExe,
    " executable_sha256=",P159V4BinarySha,"\n");
fi;

if LoadPackage("nq")<>true then
  Error("PENT159N_V4: authenticated NQ package still failed to load");
fi;
Print("PENT159N_NQ_LOAD_PASS version=",P159V4NqVersion,
  " executable=",P159V4NqExe,
  " executable_sha256=",P159V4BinarySha,"\n");

P159V4V1ActualSha := P159V4RequireFileSha(P159V4V1Path,P159V4V1Sha,
  "frozen stage-0 v1 producer");
Print("PENT159N_V1_CALIBRATION_AUDIT_PIN_PASS source=",P159V4V1Path,
  " sha256=",P159V4V1ActualSha,"\n");

## NQ 2.5.11 constructs NqEpimorphismNilpotentQuotient with identical
## generators by first forming U:=Subgroup(E,ordinary_generators).  That source
## subgroup construction is unnecessary for this calibration and triggered the
## 4,096,000-coset stop in v1.  NilpotentQuotient uses the same NqCallANU_NQ
## input but returns NqPcpGroupByNqOutput directly, without constructing U.
P159V4Ext := FreeGroup("x","y","u","v");
P159V4x := P159V4Ext.1;
P159V4y := P159V4Ext.2;
P159V4u := P159V4Ext.3;
P159V4v := P159V4Ext.4;
P159V4E := P159V4Ext / [P159V4u^4,Comm(P159V4u,P159V4v)^2];
P159V4IdGens := [P159V4u,P159V4v];
Print("PENT159N_NQ_DIRECT_CALL_BEGIN api=NilpotentQuotient",
  " signature=fp-group,id-gens,class ordinary_generators=2",
  " identical_generators=2 class_bound=3",
  " laws=u^4,Comm(u,v)^2\n");
P159V4Q := NilpotentQuotient(P159V4E,P159V4IdGens,3);
Print("PENT159N_NQ_DIRECT_CALL_RETURN api=NilpotentQuotient",
  " result_is_pcp=",IsPcpGroup(P159V4Q),"\n");
if not IsPcpGroup(P159V4Q) then
  Error("PENT159N_V4: direct NilpotentQuotient did not return a pcp group");
fi;
P159V4Order := Size(P159V4Q);
P159V4Class := NilpotencyClassOfGroup(P159V4Q);
Print("PENT159N_F2_D4P_CALIBRATION prime=2 order=",P159V4Order,
  " class=",P159V4Class,"\n");
if P159V4Order<>128 then
  Error("PENT159N_V4: F2/D4_2 calibration order mismatch");
fi;
if P159V4Class<>3 then
  Error("PENT159N_V4: F2/D4_2 calibration class mismatch");
fi;
Print("PENT159N_NQ_DIRECT_STAGE0_PASS api=NilpotentQuotient",
  " order=",P159V4Order," class=",P159V4Class,"\n");
Print("PENT159N_GAP_STAGE0_V4_PASS v1_audit_sha256=",P159V4V1ActualSha,
  " nq_version=",P159V4NqVersion,
  " nq_executable_sha256=",P159V4BinarySha,"\n");
