#############################################################################
## D972 corrected pentagon canary: Linux NQ portability repair, stage 0 v3.
##
## This wrapper does not change the mathematics or the frozen v1 producer.
## It authenticates the bundled NQ 2.5.11 sources, builds its missing UNIX
## executable in place when necessary, loads NQ, and delegates to v1.  Any
## missing/multiple package path, source drift, build failure, executable
## ambiguity, or calibration failure stops before the v3 final marker.
#############################################################################

P159V3V1Path := "search/d972_pent_interleave_canary_producer_v1.g";
P159V3V1Sha :=
  "c21b7758f244997d1da9c15c3b09b71a13b1995b379596c849a8eacccc202d6d";
P159V3NqVersion := "2.5.11";
P159V3PackageInfoSha :=
  "e5e3370aa823163909a5130f1d803f43051e606305915718bcf7a363e5af5264";
P159V3ConfigureSha :=
  "4c09599a55cbdf0eb22998280e197f64ebb2e6ca5ca884b80e3e8d55c1ca0bd0";
P159V3MakefileInSha :=
  "84def846c51b5fe54b79b1ca312ac5629c383ccadbe43349da4d40efa9c5d003";

P159V3ReadOneLine := function(path,label)
  local raw,body;
  raw := StringFile(path);
  if raw=fail then Error("PENT159N_V3: missing ",label," at ",path); fi;
  if Length(raw)<2 or raw[Length(raw)]<>'\n' then
    Error("PENT159N_V3: ",label," is not one LF-terminated line");
  fi;
  body := raw{[1..Length(raw)-1]};
  if Length(body)=0 or Position(body,'\n')<>fail or
     Position(body,'\r')<>fail then
    Error("PENT159N_V3: malformed ",label);
  fi;
  return body;
end;

P159V3IsLowerHexSha := function(s)
  return Length(s)=64 and ForAll(s,c -> c in "0123456789abcdef");
end;

P159V3ShellQuote := function(s)
  if Position(s,'\n') <> fail or Position(s,'\r') <> fail then
    Error("PENT159N_V3: newline in shell argument");
  fi;
  return Concatenation("'",ReplacedString(s,"'","'\"'\"'"),"'");
end;

P159V3RequireFileSha := function(path,expected,label)
  local src,actual;
  src := StringFile(path);
  if src=fail then Error("PENT159N_V3: missing ",label," at ",path); fi;
  actual := HexSHA256(src);
  if actual<>expected then
    Error("PENT159N_V3: ",label," SHA drift: ",actual);
  fi;
  return actual;
end;

P159V3Infos := PackageInfo("nq");
if Length(P159V3Infos)<>1 then
  Error("PENT159N_V3: expected exactly one bundled NQ PackageInfo entry");
fi;
P159V3Info := P159V3Infos[1];
if not IsBound(P159V3Info.Version) or
   P159V3Info.Version<>P159V3NqVersion then
  Error("PENT159N_V3: NQ version drift");
fi;
if not IsBound(P159V3Info.InstallationPath) then
  Error("PENT159N_V3: NQ InstallationPath missing");
fi;
P159V3NqPath := P159V3Info.InstallationPath;
if PositionSublist(LowercaseString(GAPInfo.Architecture),"linux")=fail then
  Error("PENT159N_V3: this portability stage is Linux-only");
fi;
if not IsString(P159V3NqPath) or Length(P159V3NqPath)<2 or
   P159V3NqPath[Length(P159V3NqPath)]<>'/' then
  Error("PENT159N_V3: NQ InstallationPath is not a trailing-slash path");
fi;
if not IsBound(GAPInfo.RootPaths) or not IsList(GAPInfo.RootPaths) then
  Error("PENT159N_V3: GAPInfo.RootPaths unavailable");
fi;

## Derive GAPROOT without GetEnv: the NQ InstallationPath must be exactly one
## direct child of the pkg/ directory under exactly one GAP-native root.
P159V3GapRootCandidates := [];
for P159V3RootCandidate in GAPInfo.RootPaths do
  if IsString(P159V3RootCandidate) and Length(P159V3RootCandidate)>0 then
    if P159V3RootCandidate[Length(P159V3RootCandidate)]<>'/' then
      P159V3RootCandidate := Concatenation(P159V3RootCandidate,"/");
    fi;
    P159V3ParentCandidate := Concatenation(P159V3RootCandidate,"pkg/");
    if Length(P159V3NqPath)>Length(P159V3ParentCandidate) and
       PositionSublist(P159V3NqPath,P159V3ParentCandidate)=1 then
      P159V3TailCandidate := P159V3NqPath{
        [Length(P159V3ParentCandidate)+1..Length(P159V3NqPath)]};
      if Length(P159V3TailCandidate)>=2 and
         P159V3TailCandidate[Length(P159V3TailCandidate)]='/' and
         Position(P159V3TailCandidate{
           [1..Length(P159V3TailCandidate)-1]},'/')=fail and
         Position(P159V3GapRootCandidates,P159V3RootCandidate)=fail then
        Add(P159V3GapRootCandidates,P159V3RootCandidate);
      fi;
    fi;
  fi;
od;
if Length(P159V3GapRootCandidates)<>1 then
  Error("PENT159N_V3: NQ does not identify exactly one GAP-native root");
fi;
P159V3GapRoot := P159V3GapRootCandidates[1];
P159V3PackageParent := Concatenation(P159V3GapRoot,"pkg/");
P159V3NqDirectoryName := P159V3NqPath{
  [Length(P159V3PackageParent)+1..Length(P159V3NqPath)-1]};
if P159V3NqPath<>
   Concatenation(P159V3PackageParent,P159V3NqDirectoryName,"/") then
  Error("PENT159N_V3: NQ package-parent equality gate failed");
fi;

P159V3PackageInfoPath := Concatenation(P159V3NqPath,"PackageInfo.g");
P159V3ConfigurePath := Concatenation(P159V3NqPath,"configure");
P159V3MakefileInPath := Concatenation(P159V3NqPath,"Makefile.in");
P159V3RequireFileSha(P159V3PackageInfoPath,P159V3PackageInfoSha,
  "NQ PackageInfo.g");
P159V3RequireFileSha(P159V3ConfigurePath,P159V3ConfigureSha,
  "NQ configure");
P159V3RequireFileSha(P159V3MakefileInPath,P159V3MakefileInSha,
  "NQ Makefile.in");
Print("PENT159N_NQ_SOURCE_PIN_PASS version=",P159V3NqVersion,
  " gap_root=",P159V3GapRoot,
  " package_parent=",P159V3PackageParent,
  " package_path=",P159V3NqPath,
  " packageinfo_sha256=",P159V3PackageInfoSha,
  " configure_sha256=",P159V3ConfigureSha,
  " makefile_in_sha256=",P159V3MakefileInSha,"\n");

P159V3OutRoot := Filename(DirectoryCurrent(),"ci/out");
P159V3ConfigureLog := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_configure_v3.log");
P159V3MakeLog := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_make_v3.log");
P159V3ShellRawPathFile := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_shell_path_raw_v3.txt");
P159V3ShellCanonicalPathFile := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_shell_path_realpath_v3.txt");
P159V3GapRawPathFile := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_gap_path_raw_v3.txt");
P159V3GapCanonicalPathFile := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_gap_path_realpath_v3.txt");
P159V3BinaryShaFile := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_binary_sha256_v3.txt");
P159V3GeneratedMakefileShaFile := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_generated_makefile_sha256_v3.txt");
P159V3BuildSentinel := Concatenation(P159V3OutRoot,
  "/d972_pent159n_nq_build_v3.ok");

P159V3NqExeBefore := Filename(DirectoriesPackagePrograms("nq"),"nq");
P159V3Built := false;
if P159V3NqExeBefore=fail then
  P159V3BuildCommand := Concatenation(
    "set -eu; ",
    "rm -f ",P159V3ShellQuote(P159V3ConfigureLog)," ",
      P159V3ShellQuote(P159V3MakeLog)," ",
      P159V3ShellQuote(P159V3ShellRawPathFile)," ",
      P159V3ShellQuote(P159V3ShellCanonicalPathFile)," ",
      P159V3ShellQuote(P159V3GapRawPathFile)," ",
      P159V3ShellQuote(P159V3GapCanonicalPathFile)," ",
      P159V3ShellQuote(P159V3BinaryShaFile)," ",
      P159V3ShellQuote(P159V3GeneratedMakefileShaFile)," ",
      P159V3ShellQuote(P159V3BuildSentinel),"; ",
    "cd ",P159V3ShellQuote(P159V3NqPath),"; ",
    "test -x ./configure; ",
    "./configure --with-gaproot=",P159V3ShellQuote(P159V3GapRoot),
      " > ",P159V3ShellQuote(P159V3ConfigureLog)," 2>&1; ",
    "make -j2 > ",P159V3ShellQuote(P159V3MakeLog)," 2>&1; ",
    "sha256sum Makefile | cut -d ' ' -f1 > ",
      P159V3ShellQuote(P159V3GeneratedMakefileShaFile),"; ",
    "printf 'PENT159N_NQ_BUILD_SHELL_PASS\\n' > ",
      P159V3ShellQuote(P159V3BuildSentinel));
  Exec(P159V3BuildCommand);
  if StringFile(P159V3BuildSentinel)<>
     "PENT159N_NQ_BUILD_SHELL_PASS\n" then
    Error("PENT159N_V3: NQ configure/make did not produce exact sentinel");
  fi;
  P159V3Built := true;
fi;

## Discover independently through the package bin tree, and canonicalize the
## shell representation before asking GAP for its representation.
P159V3ShellDiscoverCommand := Concatenation(
  "set -eu; command -v realpath >/dev/null; ",
  "rm -f ",P159V3ShellQuote(P159V3ShellRawPathFile)," ",
    P159V3ShellQuote(P159V3ShellCanonicalPathFile)," ",
    P159V3ShellQuote(P159V3GapRawPathFile)," ",
    P159V3ShellQuote(P159V3GapCanonicalPathFile)," ",
    P159V3ShellQuote(P159V3BinaryShaFile),"; ",
  "nq_bin=$(find ",P159V3ShellQuote(Concatenation(P159V3NqPath,"bin")),
    " -type f -name nq -perm -111 -print); ",
  "test -n \"$nq_bin\"; ",
  "test \"$(printf '%s\\n' \"$nq_bin\" | wc -l)\" -eq 1; ",
  "printf '%s\\n' \"$nq_bin\" > ",
    P159V3ShellQuote(P159V3ShellRawPathFile),"; ",
  "nq_real=$(realpath -- \"$nq_bin\"); test -n \"$nq_real\"; ",
  "printf '%s\\n' \"$nq_real\" > ",
    P159V3ShellQuote(P159V3ShellCanonicalPathFile),"; ",
  "sha256sum \"$nq_real\" | cut -d ' ' -f1 > ",
    P159V3ShellQuote(P159V3BinaryShaFile));
Exec(P159V3ShellDiscoverCommand);
P159V3ShellRawPath := P159V3ReadOneLine(P159V3ShellRawPathFile,
  "shell-discovered NQ raw path");
P159V3ShellCanonicalPath := P159V3ReadOneLine(
  P159V3ShellCanonicalPathFile,"shell-discovered NQ realpath");

P159V3NqExe := Filename(DirectoriesPackagePrograms("nq"),"nq");
if P159V3NqExe=fail then
  Error("PENT159N_V3: NQ executable still unavailable after portability stage");
fi;
Print("PENT159N_NQ_PATH_RAW shell=",P159V3ShellRawPath,
  " gap=",P159V3NqExe,"\n");
P159V3GapCanonicalizeCommand := Concatenation(
  "set -eu; command -v realpath >/dev/null; ",
  "printf '%s\\n' ",P159V3ShellQuote(P159V3NqExe)," > ",
    P159V3ShellQuote(P159V3GapRawPathFile),"; ",
  "realpath -- ",P159V3ShellQuote(P159V3NqExe)," > ",
    P159V3ShellQuote(P159V3GapCanonicalPathFile));
Exec(P159V3GapCanonicalizeCommand);
P159V3GapRecordedRawPath := P159V3ReadOneLine(P159V3GapRawPathFile,
  "GAP-discovered NQ raw path");
P159V3GapCanonicalPath := P159V3ReadOneLine(P159V3GapCanonicalPathFile,
  "GAP-discovered NQ realpath");
if P159V3GapRecordedRawPath<>P159V3NqExe then
  Error("PENT159N_V3: GAP raw-path recording mismatch");
fi;
Print("PENT159N_NQ_PATH_CANONICAL shell=",P159V3ShellCanonicalPath,
  " gap=",P159V3GapCanonicalPath,"\n");
if P159V3ShellCanonicalPath<>P159V3GapCanonicalPath then
  Error("PENT159N_V3: canonical shell/GAP NQ executable path mismatch");
fi;
Print("PENT159N_NQ_PATH_EQUIVALENCE_PASS realpath=",
  P159V3ShellCanonicalPath,"\n");
P159V3BinarySha := P159V3ReadOneLine(P159V3BinaryShaFile,
  "NQ executable SHA record");
if not P159V3IsLowerHexSha(P159V3BinarySha) then
  Error("PENT159N_V3: malformed NQ executable SHA record");
fi;
if P159V3Built then
  P159V3GeneratedMakefileSha := P159V3ReadOneLine(
    P159V3GeneratedMakefileShaFile,"generated Makefile SHA record");
  if not P159V3IsLowerHexSha(P159V3GeneratedMakefileSha) then
    Error("PENT159N_V3: malformed generated Makefile SHA record");
  fi;
  Print("PENT159N_NQ_BUILD_PASS version=",P159V3NqVersion,
    " gap_root=",P159V3GapRoot,
    " package_path=",P159V3NqPath,
    " configure_argv0=./configure configure_argv1=--with-gaproot=",
      P159V3GapRoot,
    " make_argv0=make make_argv1=-j2",
    " generated_makefile_sha256=",P159V3GeneratedMakefileSha,
    " executable=",P159V3NqExe,
    " executable_sha256=",P159V3BinarySha,"\n");
else
  Print("PENT159N_NQ_PREBUILT_PRESENT version=",P159V3NqVersion,
    " package_path=",P159V3NqPath,
    " executable=",P159V3NqExe,
    " executable_sha256=",P159V3BinarySha,"\n");
fi;

if LoadPackage("nq")<>true then
  Error("PENT159N_V3: authenticated NQ package still failed to load");
fi;
Print("PENT159N_NQ_LOAD_PASS version=",P159V3NqVersion,
  " executable=",P159V3NqExe,
  " executable_sha256=",P159V3BinarySha,"\n");

P159V3V1ActualSha := P159V3RequireFileSha(P159V3V1Path,P159V3V1Sha,
  "frozen stage-0 v1 producer");
Print("PENT159N_V1_DELEGATION_PIN_PASS source=",P159V3V1Path,
  " sha256=",P159V3V1ActualSha,"\n");
Read(P159V3V1Path);
Print("PENT159N_GAP_STAGE0_V3_PASS v1_sha256=",P159V3V1ActualSha,
  " nq_version=",P159V3NqVersion,
  " nq_executable_sha256=",P159V3BinarySha,"\n");
