#############################################################################
## d972_b4_norm_tietze_gap_driver_v2.g
##
## Versioned official-KBMAG wrapper for the generic gap-run workflow.
##
## The outer GAP process downloads and SHA256-verifies the official KBMAG
## v1.6.0 release, builds it below a private /tmp root, then starts a nested
## GAP with the ordinary GAP roots, /tmp/gaproot, and that private root.  The
## nested driver reads the immutable v1 driver with BOOTSTRAP=0.  The wrapper
## never edits v1 and promotes only a v1 receipt plus its final marker.
##
## SELFTEST=1 performs no Exec, package load, network operation, or nested
## process.  There is deliberately no QUIT: generic gap-run reads this file.
#############################################################################

D972KB160Version := "1.6.0";;
D972KB160URL :=
  "https://github.com/gap-packages/kbmag/releases/download/v1.6.0/kbmag-1.6.0.tar.gz";;
D972KB160SHA :=
  "de28d1dcaabbca77561ab74a0a66588358938e58ad4dcadb1a8e479e36c7228a";;
D972KB160SourceV1 := "search/d972_b4_norm_tietze_gap_driver_v1.g";;
D972KB160SourceV1SHA :=
  "e2ac9216c21f06737d6d6bf5300889b8ae9b958c3829c0932539ea9a962c4398";;
D972KB160TmpRoot := "/tmp/d972_b4_kbmag160";;
D972KB160PackageRoot := "/tmp/d972_b4_kbmag160/pkg/kbmag";;
D972KB160Archive := "/tmp/d972_b4_kbmag160/kbmag-1.6.0.tar.gz";;
D972KB160Nested := "/tmp/d972_b4_kbmag160/nested_driver.g";;
D972KB160Status := "/tmp/d972_b4_kbmag160/nested.status";;
D972KB160Log := "ci/out/d972_b4_norm_tietze_gap_driver_v2_nested.log";;
D972KB160Receipt :=
  "ci/out/d972_b4_norm_tietze_gap_driver_v2.json";;
D972KB160V1Receipt := "ci/out/d972_b4_norm_tietze_gap_driver_v1.json";;

D972KB160Selftest := 0;;
if IsBound(D972_B4_NORM_TZ160_SELFTEST) then
  D972KB160Selftest := D972_B4_NORM_TZ160_SELFTEST;
fi;
if not IsInt(D972KB160Selftest) or not D972KB160Selftest in [0,1] then
  Error("KBMAG 1.6.0 wrapper: SELFTEST must be integer 0 or 1");
fi;

D972KB160CheckPath := function(s)
  local c;
  if not IsString(s) or s="" then
    Error("KBMAG 1.6.0 wrapper: empty/non-string path");
  fi;
  for c in ["'","`","$","\\","\n","\r",";","|","&",
            ">","<","(",")"] do
    if Position(s,c)<>fail then
      Error("KBMAG 1.6.0 wrapper: unsafe path");
    fi;
  od;
  return s;
end;;

## Every interpolated path is checked and then single-quoted.  The composite
## -l argument is assembled only from paths checked above; semicolons in it
## are GAP root separators, not shell syntax because the whole argument is
## quoted.
D972KB160ShellQuote := function(s)
  local c;
  if not IsString(s) then Error("KBMAG 1.6.0 wrapper: shell arg is not string"); fi;
  for c in ["'","`","$","\\","\n","\r"] do
    if Position(s,c)<>fail then
      Error("KBMAG 1.6.0 wrapper: unsafe shell argument");
    fi;
  od;
  return Concatenation("'",s,"'");
end;;

D972KB160Join := function(xs,sep)
  local z,i;
  if Length(xs)=0 then return ""; fi;
  z:=xs[1];;
  for i in [2..Length(xs)] do z:=Concatenation(z,sep,xs[i]); od;
  return z;
end;;

D972KB160Json := function(x)
  local p,i,names;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsInt(x) then return String(x); fi;
  ## GAP 4.16 may filter [] as a string; test empty lists first.
  if IsList(x) and Length(x)=0 then return "[]"; fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if IsRecord(x) then
    names:=SortedList(RecNames(x));;
    p:=List(names,i->Concatenation("\"",i,"\":",D972KB160Json(x.(i))));;
    return Concatenation("{",D972KB160Join(p,","),"}");
  fi;
  if not IsList(x) then Error("KBMAG 1.6.0 wrapper: JSON type drift"); fi;
  p:=List([1..Length(x)],i->D972KB160Json(x[i]));;
  return Concatenation("[",D972KB160Join(p,","),"]");
end;;

D972KB160WriteJson := function(path,obj)
  local f;
  f:=OutputTextFile(path,false);;
  if f=fail then Error("KBMAG 1.6.0 wrapper: cannot open receipt"); fi;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,Concatenation(D972KB160Json(obj),"\n"));;
  CloseStream(f);;
end;;

if D972KB160Selftest=1 then
  if D972KB160Version<>"1.6.0" or
     D972KB160URL<>"https://github.com/gap-packages/kbmag/releases/download/v1.6.0/kbmag-1.6.0.tar.gz" or
     D972KB160SHA<>"de28d1dcaabbca77561ab74a0a66588358938e58ad4dcadb1a8e479e36c7228a" or
     D972KB160TmpRoot<>"/tmp/d972_b4_kbmag160" or
     D972KB160PackageRoot<>"/tmp/d972_b4_kbmag160/pkg/kbmag" or
     D972KB160Archive<>"/tmp/d972_b4_kbmag160/kbmag-1.6.0.tar.gz" or
     D972KB160SourceV1<>"search/d972_b4_norm_tietze_gap_driver_v1.g" or
     D972KB160SourceV1SHA<>"e2ac9216c21f06737d6d6bf5300889b8ae9b958c3829c0932539ea9a962c4398" then
    Error("KBMAG 1.6.0 wrapper: fixed constant selftest failed");
  fi;
  D972KB160SelfRaw:=StringFile(D972KB160SourceV1);;
  if D972KB160SelfRaw=fail or HexSHA256(D972KB160SelfRaw)<>D972KB160SourceV1SHA then
    Error("KBMAG 1.6.0 wrapper: v1 source SHA selftest failed");
  fi;
  Print("D972_B4_KBMAG160_WRAPPER_SELFTEST_PASS version=1.6.0 source_sha256=",
    D972KB160SourceV1SHA,"\n");
  Print("D972_B4_KBMAG160_WRAPPER_FINAL_MARKER status=SELFTEST_PASS\n");
else
  ## gap-run.yml pins setup-gap's installation root.  GAP 4.16 does not
  ## provide GetEnv in the bare library, so keep the workflow-owned root as
  ## a source constant and validate it before shell interpolation.
  D972KB160GapRoot:="/home/runner/gap";;
  D972KB160CheckPath(D972KB160GapRoot);;
  D972KB160SourceV1Raw:=StringFile(D972KB160SourceV1);;
  if D972KB160SourceV1Raw=fail or
     HexSHA256(D972KB160SourceV1Raw)<>D972KB160SourceV1SHA then
    Error("KBMAG 1.6.0 wrapper: immutable v1 source SHA mismatch");
  fi;

  ## Preserve the ordinary roots already visible to the outer GAP, then add
  ## the optional-package root and the dedicated official KBMAG root.
  ## Put the dedicated root first.  GAP stably prefers the first root when
  ## the same package version occurs more than once; the nested script also
  ## checks the normalized InstallationPath, so this is provenance, not just
  ## a version comparison.
  D972KB160Roots:=[D972KB160TmpRoot];;
  for D972KB160Root in GAPInfo.RootPaths do
    if IsString(D972KB160Root) and Position(D972KB160Roots,D972KB160Root)=fail then
      D972KB160CheckPath(D972KB160Root);;
      Add(D972KB160Roots,D972KB160Root);;
    fi;
  od;
  if Position(D972KB160Roots,D972KB160GapRoot)=fail then
    Add(D972KB160Roots,D972KB160GapRoot);
  fi;
  for D972KB160Root in ["/tmp/gaproot"] do
    D972KB160CheckPath(D972KB160Root);;
    if Position(D972KB160Roots,D972KB160Root)=fail then Add(D972KB160Roots,D972KB160Root); fi;
  od;
  ## This explicit list already contains every ordinary outer root.  With no
  ## leading/trailing semicolon, GAP replaces its root list by exactly this
  ## order instead of silently appending the dedicated root after defaults.
  D972KB160RootArg:=D972KB160Join(D972KB160Roots,";");;

  D972KB160Build:=Concatenation(
    "set -eu; rm -rf ",D972KB160ShellQuote(D972KB160TmpRoot),
    "; mkdir -p ",D972KB160ShellQuote(Concatenation(D972KB160TmpRoot,"/pkg")),
    "; curl --fail --location --silent --show-error --retry 3 --output ",
      D972KB160ShellQuote(D972KB160Archive)," ",D972KB160ShellQuote(D972KB160URL),
    "; printf '%s  %s\\n' ",D972KB160ShellQuote(D972KB160SHA)," ",
      D972KB160ShellQuote(D972KB160Archive)," | sha256sum --check --status",
    "; tar --extract --gzip --file ",D972KB160ShellQuote(D972KB160Archive),
      " --directory ",D972KB160ShellQuote(Concatenation(D972KB160TmpRoot,"/pkg")),
    "; src=$(find ",D972KB160ShellQuote(Concatenation(D972KB160TmpRoot,"/pkg")),
      " -mindepth 1 -maxdepth 1 -type d -name \"kbmag*\" -print -quit)",
    "; test -n \"$src\"",
    "; if [ \"$src\" != ",D972KB160ShellQuote(D972KB160PackageRoot),
      " ]; then mv \"$src\" ",D972KB160ShellQuote(D972KB160PackageRoot),"; fi",
    "; test -f ",D972KB160ShellQuote(Concatenation(D972KB160PackageRoot,"/PackageInfo.g")),
    "; grep -Fq 'Version := \"1.6.0\"' ",
      D972KB160ShellQuote(Concatenation(D972KB160PackageRoot,"/PackageInfo.g")),
    "; cd ",D972KB160ShellQuote(D972KB160PackageRoot),
    " && ./configure ",D972KB160ShellQuote(D972KB160GapRoot),
    " && make -j2");;
  ## Redirections are opened by the parent shell before the build subshell
  ## creates (and deliberately recreates) TmpRoot, so keep these two control
  ## files beside—not inside—the directory being rebuilt.
  D972KB160BuildStatus:="/tmp/d972_b4_kbmag160_build.status";;
  D972KB160BuildLog:="/tmp/d972_b4_kbmag160_build.log";;
  D972KB160BuildFull:=Concatenation(
    "rm -f ",D972KB160ShellQuote(D972KB160BuildStatus),"; ( ",D972KB160Build,
    " ) > ",D972KB160ShellQuote(D972KB160BuildLog)," 2>&1; rc=$?; printf '%s' \"$rc\" > ",
    D972KB160ShellQuote(D972KB160BuildStatus),"; exit \"$rc\"");;
  Exec(D972KB160BuildFull);;
  if StringFile(D972KB160BuildStatus)<>"0" then
    Error("KBMAG 1.6.0 wrapper: curl/verify/extract/configure/make failed");
  fi;
  if StringFile(D972KB160BuildLog)=fail then
    Error("KBMAG 1.6.0 wrapper: build log missing");
  fi;
  Print("D972_B4_KBMAG160_BUILD_PASS version=1.6.0 package=",
    D972KB160PackageRoot,"\n");

  ## The nested program checks PackageInfo before reading the unchanged v1
  ## driver.  It also binds BOOTSTRAP=0, so the old setup-gap bootstrap path
  ## can never run inside this official-release test.
  D972KB160NestedText:=Concatenation(
    "if GAPInfo.Version <> \"4.16.0\" then Error(\"KBMAG 1.6.0 wrapper: GAP version drift\"); fi;;\n",
    "if LoadPackage(\"kbmag\") <> true then Error(\"KBMAG 1.6.0 wrapper: kbmag load failed\"); fi;;\n",
    "D972KB160Info:=PackageInfo(\"kbmag\");;\n",
    "if Length(D972KB160Info)=0 or not IsBound(D972KB160Info[1].Version) or D972KB160Info[1].Version <> \"1.6.0\" then Error(\"KBMAG 1.6.0 wrapper: PackageInfo version gate failed\"); fi;;\n",
    "if not IsBound(D972KB160Info[1].InstallationPath) or not D972KB160Info[1].InstallationPath in [\"/tmp/d972_b4_kbmag160/pkg/kbmag\",\"/tmp/d972_b4_kbmag160/pkg/kbmag/\"] then Error(\"KBMAG 1.6.0 wrapper: PackageInfo installation-path gate failed\"); fi;;\n",
    "Print(\"B4_KBMAG160_PACKAGE_VERSION_PASS version=1.6.0\\n\");;\n",
    "D972_B4_NORM_TZ_BOOTSTRAP:=0;; D972_B4_NORM_TZ_SELFTEST:=0;;\n",
    "Read(\"search/d972_b4_norm_tietze_gap_driver_v1.g\");\n");;
  D972KB160NestedFile:=OutputTextFile(D972KB160Nested,false);;
  if D972KB160NestedFile=fail then Error("KBMAG 1.6.0 wrapper: nested driver open failed"); fi;
  SetPrintFormattingStatus(D972KB160NestedFile,false);;
  PrintTo(D972KB160NestedFile,D972KB160NestedText);;
  CloseStream(D972KB160NestedFile);;

  D972KB160NestedCommand:=Concatenation(
    "gap -l ",D972KB160ShellQuote(D972KB160RootArg),
    " --quitonbreak -q -o 12g ",D972KB160ShellQuote(D972KB160Nested));;
  D972KB160NestedFull:=Concatenation(
    "rm -f ",D972KB160ShellQuote(D972KB160Status)," ",
      D972KB160ShellQuote(D972KB160Log)," ",
      D972KB160ShellQuote(D972KB160Receipt)," ",
      D972KB160ShellQuote(D972KB160V1Receipt)," ",
      D972KB160ShellQuote("ci/out/d972_b4_norm_tietze_trace_v2.json")," ",
      D972KB160ShellQuote("ci/out/d972_b4_norm_tietze_dense_check_v1.json")," ",
      D972KB160ShellQuote("ci/out/d972_b4_norm_tietze_kbmag_v2.json"),"; ",
      D972KB160NestedCommand,
    " > ",D972KB160ShellQuote(D972KB160Log)," 2>&1; rc=$?; printf '%s' \"$rc\" > ",
    D972KB160ShellQuote(D972KB160Status),"; exit \"$rc\"");;
  Exec(D972KB160NestedFull);;
  if StringFile(D972KB160Status)<>"0" then
    Error("KBMAG 1.6.0 wrapper: nested GAP exit status is not zero");
  fi;
  D972KB160LogRaw:=StringFile(D972KB160Log);;
  if D972KB160LogRaw=fail or
     Position(D972KB160LogRaw,"B4_KBMAG160_PACKAGE_VERSION_PASS version=1.6.0")=fail or
     Position(D972KB160LogRaw,"B4_NORM_TZ_GAP_DRIVER_FINAL_MARKER")=fail or
     Position(D972KB160LogRaw,"Error,")<>fail or
     Position(D972KB160LogRaw,"Syntax error:")<>fail then
    Error("KBMAG 1.6.0 wrapper: nested package/marker/error gate failed");
  fi;
  D972KB160V1Raw:=StringFile(D972KB160V1Receipt);;
  if D972KB160V1Raw=fail then Error("KBMAG 1.6.0 wrapper: v1 receipt missing"); fi;
  if LoadPackage("json")<>true then Error("KBMAG 1.6.0 wrapper: json unavailable"); fi;
  D972KB160V1Obj:=JsonStringToGap(D972KB160V1Raw);;
  if not IsRecord(D972KB160V1Obj) or
     D972KB160V1Obj.schema<>"d972-b4-norm-tietze-gap-driver/v1" or
     D972KB160V1Obj.status<>"KBMAG_CANDIDATE_PENDING_REPLAY" or
     D972KB160V1Obj.producer_exit_code<>0 or
     D972KB160V1Obj.checker_exit_code<>0 then
    Error("KBMAG 1.6.0 wrapper: v1 receipt gate failed");
  fi;
  D972KB160WriteJson(D972KB160Receipt,rec(
    schema:="d972-b4-kbmag160-wrapper/v1",
    status:="PASS",
    official_version:=D972KB160Version,
    archive_url:=D972KB160URL,
    archive_sha256:=D972KB160SHA,
    v1_source_sha256:=D972KB160SourceV1SHA,
    package_root:=D972KB160PackageRoot,
    nested_roots:=D972KB160Roots,
    build_status:=0,nested_status:=0,
    v1_receipt_sha256:=HexSHA256(D972KB160V1Raw),
    v1_status:=D972KB160V1Obj.status,
    v1_receipt:=D972KB160V1Receipt,
    nested_log:=D972KB160Log));
  Print("D972_B4_KBMAG160_WRAPPER_FINAL_MARKER status=PASS version=1.6.0 v1_receipt=",
    D972KB160V1Receipt,"\n");
fi;
