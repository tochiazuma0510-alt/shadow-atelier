#############################################################################
## D972 corrected pentagon canary: Linux NQ portability repair, stage 0 v2.
##
## This wrapper does not change the mathematics or the frozen v1 producer.
## It authenticates the bundled NQ 2.5.11 sources, builds its missing UNIX
## executable in place when necessary, loads NQ, and delegates to v1.  Any
## missing/multiple package path, source drift, build failure, executable
## ambiguity, or calibration failure stops before the v2 final marker.
#############################################################################

P159V2V1Path := "search/d972_pent_interleave_canary_producer_v1.g";
P159V2V1Sha :=
  "c21b7758f244997d1da9c15c3b09b71a13b1995b379596c849a8eacccc202d6d";
P159V2NqVersion := "2.5.11";
P159V2PackageInfoSha :=
  "e5e3370aa823163909a5130f1d803f43051e606305915718bcf7a363e5af5264";
P159V2ConfigureSha :=
  "4c09599a55cbdf0eb22998280e197f64ebb2e6ca5ca884b80e3e8d55c1ca0bd0";
P159V2MakefileInSha :=
  "84def846c51b5fe54b79b1ca312ac5629c383ccadbe43349da4d40efa9c5d003";

P159V2TrimNewlines := function(s)
  return Filtered(s,c -> c <> '\n' and c <> '\r');
end;

P159V2IsLowerHexSha := function(s)
  return Length(s)=64 and ForAll(s,c -> c in "0123456789abcdef");
end;

P159V2ShellQuote := function(s)
  if Position(s,'\n') <> fail or Position(s,'\r') <> fail then
    Error("PENT159N_V2: newline in shell argument");
  fi;
  return Concatenation("'",ReplacedString(s,"'","'\"'\"'"),"'");
end;

P159V2RequireFileSha := function(path,expected,label)
  local src,actual;
  src := StringFile(path);
  if src=fail then Error("PENT159N_V2: missing ",label," at ",path); fi;
  actual := HexSHA256(src);
  if actual<>expected then
    Error("PENT159N_V2: ",label," SHA drift: ",actual);
  fi;
  return actual;
end;

P159V2Infos := PackageInfo("nq");
if Length(P159V2Infos)<>1 then
  Error("PENT159N_V2: expected exactly one bundled NQ PackageInfo entry");
fi;
P159V2Info := P159V2Infos[1];
if not IsBound(P159V2Info.Version) or
   P159V2Info.Version<>P159V2NqVersion then
  Error("PENT159N_V2: NQ version drift");
fi;
if not IsBound(P159V2Info.InstallationPath) then
  Error("PENT159N_V2: NQ InstallationPath missing");
fi;
P159V2NqPath := P159V2Info.InstallationPath;
if PositionSublist(LowercaseString(GAPInfo.Architecture),"linux")=fail then
  Error("PENT159N_V2: this portability stage is Linux-only");
fi;
if not IsString(P159V2NqPath) or Length(P159V2NqPath)<2 or
   P159V2NqPath[Length(P159V2NqPath)]<>'/' then
  Error("PENT159N_V2: NQ InstallationPath is not a trailing-slash path");
fi;
if not IsBound(GAPInfo.RootPaths) or not IsList(GAPInfo.RootPaths) then
  Error("PENT159N_V2: GAPInfo.RootPaths unavailable");
fi;

## Derive GAPROOT without GetEnv: the NQ InstallationPath must be exactly one
## direct child of the pkg/ directory under exactly one GAP-native root.
P159V2GapRootCandidates := [];
for P159V2RootCandidate in GAPInfo.RootPaths do
  if IsString(P159V2RootCandidate) and Length(P159V2RootCandidate)>0 then
    if P159V2RootCandidate[Length(P159V2RootCandidate)]<>'/' then
      P159V2RootCandidate := Concatenation(P159V2RootCandidate,"/");
    fi;
    P159V2ParentCandidate := Concatenation(P159V2RootCandidate,"pkg/");
    if Length(P159V2NqPath)>Length(P159V2ParentCandidate) and
       PositionSublist(P159V2NqPath,P159V2ParentCandidate)=1 then
      P159V2TailCandidate := P159V2NqPath{
        [Length(P159V2ParentCandidate)+1..Length(P159V2NqPath)]};
      if Length(P159V2TailCandidate)>=2 and
         P159V2TailCandidate[Length(P159V2TailCandidate)]='/' and
         Position(P159V2TailCandidate{
           [1..Length(P159V2TailCandidate)-1]},'/')=fail and
         Position(P159V2GapRootCandidates,P159V2RootCandidate)=fail then
        Add(P159V2GapRootCandidates,P159V2RootCandidate);
      fi;
    fi;
  fi;
od;
if Length(P159V2GapRootCandidates)<>1 then
  Error("PENT159N_V2: NQ does not identify exactly one GAP-native root");
fi;
P159V2GapRoot := P159V2GapRootCandidates[1];
P159V2PackageParent := Concatenation(P159V2GapRoot,"pkg/");
P159V2NqDirectoryName := P159V2NqPath{
  [Length(P159V2PackageParent)+1..Length(P159V2NqPath)-1]};
if P159V2NqPath<>
   Concatenation(P159V2PackageParent,P159V2NqDirectoryName,"/") then
  Error("PENT159N_V2: NQ package-parent equality gate failed");
fi;

P159V2PackageInfoPath := Concatenation(P159V2NqPath,"PackageInfo.g");
P159V2ConfigurePath := Concatenation(P159V2NqPath,"configure");
P159V2MakefileInPath := Concatenation(P159V2NqPath,"Makefile.in");
P159V2RequireFileSha(P159V2PackageInfoPath,P159V2PackageInfoSha,
  "NQ PackageInfo.g");
P159V2RequireFileSha(P159V2ConfigurePath,P159V2ConfigureSha,
  "NQ configure");
P159V2RequireFileSha(P159V2MakefileInPath,P159V2MakefileInSha,
  "NQ Makefile.in");
Print("PENT159N_NQ_SOURCE_PIN_PASS version=",P159V2NqVersion,
  " gap_root=",P159V2GapRoot,
  " package_parent=",P159V2PackageParent,
  " package_path=",P159V2NqPath,
  " packageinfo_sha256=",P159V2PackageInfoSha,
  " configure_sha256=",P159V2ConfigureSha,
  " makefile_in_sha256=",P159V2MakefileInSha,"\n");

P159V2OutRoot := Filename(DirectoryCurrent(),"ci/out");
P159V2ConfigureLog := Concatenation(P159V2OutRoot,
  "/d972_pent159n_nq_configure_v2.log");
P159V2MakeLog := Concatenation(P159V2OutRoot,
  "/d972_pent159n_nq_make_v2.log");
P159V2BinaryPathFile := Concatenation(P159V2OutRoot,
  "/d972_pent159n_nq_binary_path_v2.txt");
P159V2BinaryShaFile := Concatenation(P159V2OutRoot,
  "/d972_pent159n_nq_binary_sha256_v2.txt");
P159V2GeneratedMakefileShaFile := Concatenation(P159V2OutRoot,
  "/d972_pent159n_nq_generated_makefile_sha256_v2.txt");
P159V2BuildSentinel := Concatenation(P159V2OutRoot,
  "/d972_pent159n_nq_build_v2.ok");

P159V2NqExeBefore := Filename(DirectoriesPackagePrograms("nq"),"nq");
P159V2Built := false;
if P159V2NqExeBefore=fail then
  P159V2BuildCommand := Concatenation(
    "set -eu; ",
    "rm -f ",P159V2ShellQuote(P159V2ConfigureLog)," ",
      P159V2ShellQuote(P159V2MakeLog)," ",
      P159V2ShellQuote(P159V2BinaryPathFile)," ",
      P159V2ShellQuote(P159V2BinaryShaFile)," ",
      P159V2ShellQuote(P159V2GeneratedMakefileShaFile)," ",
      P159V2ShellQuote(P159V2BuildSentinel),"; ",
    "cd ",P159V2ShellQuote(P159V2NqPath),"; ",
    "test -x ./configure; ",
    "./configure --with-gaproot=",P159V2ShellQuote(P159V2GapRoot),
      " > ",P159V2ShellQuote(P159V2ConfigureLog)," 2>&1; ",
    "make -j2 > ",P159V2ShellQuote(P159V2MakeLog)," 2>&1; ",
    "nq_bin=$(find ",P159V2ShellQuote(Concatenation(P159V2NqPath,"bin")),
      " -type f -name nq -perm -111 -print); ",
    "test -n \"$nq_bin\"; ",
    "test \"$(printf '%s\\n' \"$nq_bin\" | wc -l)\" -eq 1; ",
    "printf '%s\\n' \"$nq_bin\" > ",P159V2ShellQuote(P159V2BinaryPathFile),"; ",
    "sha256sum \"$nq_bin\" | cut -d ' ' -f1 > ",
      P159V2ShellQuote(P159V2BinaryShaFile),"; ",
    "sha256sum Makefile | cut -d ' ' -f1 > ",
      P159V2ShellQuote(P159V2GeneratedMakefileShaFile),"; ",
    "printf 'PENT159N_NQ_BUILD_SHELL_PASS\\n' > ",
      P159V2ShellQuote(P159V2BuildSentinel));
  Exec(P159V2BuildCommand);
  if StringFile(P159V2BuildSentinel)<>
     "PENT159N_NQ_BUILD_SHELL_PASS\n" then
    Error("PENT159N_V2: NQ configure/make did not produce exact sentinel");
  fi;
  P159V2Built := true;
else
  P159V2PrebuiltCommand := Concatenation(
    "set -eu; ",
    "printf '%s\\n' ",P159V2ShellQuote(P159V2NqExeBefore)," > ",
      P159V2ShellQuote(P159V2BinaryPathFile),"; ",
    "sha256sum ",P159V2ShellQuote(P159V2NqExeBefore),
      " | cut -d ' ' -f1 > ",P159V2ShellQuote(P159V2BinaryShaFile));
  Exec(P159V2PrebuiltCommand);
fi;

P159V2NqExe := Filename(DirectoriesPackagePrograms("nq"),"nq");
if P159V2NqExe=fail then
  Error("PENT159N_V2: NQ executable still unavailable after portability stage");
fi;
P159V2RecordedBinaryPath := P159V2TrimNewlines(
  StringFile(P159V2BinaryPathFile));
if P159V2RecordedBinaryPath<>P159V2NqExe then
  Error("PENT159N_V2: built/discovered NQ executable path mismatch");
fi;
P159V2BinarySha := P159V2TrimNewlines(StringFile(P159V2BinaryShaFile));
if not P159V2IsLowerHexSha(P159V2BinarySha) then
  Error("PENT159N_V2: malformed NQ executable SHA record");
fi;
if P159V2Built then
  P159V2GeneratedMakefileSha := P159V2TrimNewlines(
    StringFile(P159V2GeneratedMakefileShaFile));
  if not P159V2IsLowerHexSha(P159V2GeneratedMakefileSha) then
    Error("PENT159N_V2: malformed generated Makefile SHA record");
  fi;
  Print("PENT159N_NQ_BUILD_PASS version=",P159V2NqVersion,
    " gap_root=",P159V2GapRoot,
    " package_path=",P159V2NqPath,
    " configure_argv0=./configure configure_argv1=--with-gaproot=",
      P159V2GapRoot,
    " make_argv0=make make_argv1=-j2",
    " generated_makefile_sha256=",P159V2GeneratedMakefileSha,
    " executable=",P159V2NqExe,
    " executable_sha256=",P159V2BinarySha,"\n");
else
  Print("PENT159N_NQ_PREBUILT_PRESENT version=",P159V2NqVersion,
    " package_path=",P159V2NqPath,
    " executable=",P159V2NqExe,
    " executable_sha256=",P159V2BinarySha,"\n");
fi;

if LoadPackage("nq")<>true then
  Error("PENT159N_V2: authenticated NQ package still failed to load");
fi;
Print("PENT159N_NQ_LOAD_PASS version=",P159V2NqVersion,
  " executable=",P159V2NqExe,
  " executable_sha256=",P159V2BinarySha,"\n");

P159V2V1ActualSha := P159V2RequireFileSha(P159V2V1Path,P159V2V1Sha,
  "frozen stage-0 v1 producer");
Print("PENT159N_V1_DELEGATION_PIN_PASS source=",P159V2V1Path,
  " sha256=",P159V2V1ActualSha,"\n");
Read(P159V2V1Path);
Print("PENT159N_GAP_STAGE0_V2_PASS v1_sha256=",P159V2V1ActualSha,
  " nq_version=",P159V2NqVersion,
  " nq_executable_sha256=",P159V2BinarySha,"\n");
