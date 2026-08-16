#############################################################################
## d972_b4_kbmag_bootstrap_v1.g -- generic gap-run KBMAG bootstrap.
##
## The setup-gap image contains the KBMAG GAP source under its GAP root, but
## the external kbprog binaries are not necessarily compiled.  This file is
## intended to be the script input to the unmodified generic gap-run
## workflow.  In build mode it compiles that pinned source tree with GAP's
## Exec(), checks the command status through a file outside the repository,
## then proves that both LoadPackage("kbmag") and a tiny KBMAG reduction work.
##
## It is fail-closed: an absent build marker, package, or kbprog probe stops
## before the optional target is Read.  Only the two canonical automatic
## targets are accepted.  The source package itself comes from the
## sha256-verified gap-actions/setup-gap GAP release; no network download is
## performed by this bootstrap.
#############################################################################

if not IsBound(D972_B4_KBMAG_BOOTSTRAP_MODE) then
  D972_B4_KBMAG_BOOTSTRAP_MODE:=0;;
fi;
if not IsInt(D972_B4_KBMAG_BOOTSTRAP_MODE) or
   not D972_B4_KBMAG_BOOTSTRAP_MODE in [0,1] then
  Error("KBMAG bootstrap: MODE must be integer 0 or 1");
fi;

D972KBBOutput:="ci/out/d972_b4_kbmag_bootstrap_v1.json";;
if IsBound(D972_B4_KBMAG_BOOTSTRAP_OUTPUT) then
  D972KBBOutput:=D972_B4_KBMAG_BOOTSTRAP_OUTPUT;
fi;
D972KBBTarget:=fail;;
if IsBound(D972_B4_KBMAG_BOOTSTRAP_TARGET) then
  D972KBBTarget:=D972_B4_KBMAG_BOOTSTRAP_TARGET;
fi;
D972KBBGapRoot:=fail;;
if IsBound(D972_B4_KBMAG_BOOTSTRAP_GAPROOT) then
  D972KBBGapRoot:=D972_B4_KBMAG_BOOTSTRAP_GAPROOT;
fi;
D972KBBPackageDir:=fail;;
if IsBound(D972_B4_KBMAG_BOOTSTRAP_PACKAGE_DIR) then
  D972KBBPackageDir:=D972_B4_KBMAG_BOOTSTRAP_PACKAGE_DIR;
fi;

if D972KBBTarget<>fail and not IsString(D972KBBTarget) then
  Error("KBMAG bootstrap: TARGET must be a GAP string or fail");
fi;
if D972KBBTarget<>fail and not D972KBBTarget in [
  "search/d972_b4_original_automatic_v1.g",
  "search/d972_b4_original_automatic_v2.g",
  "search/d972_b4_simplified_automatic_v1.g",
  "search/d972_b4_simplified_orderings_v1.g" ] then
  Error("KBMAG bootstrap: target is not an allow-listed canonical lane");
fi;
if D972KBBOutput<>fail and not IsString(D972KBBOutput) then
  Error("KBMAG bootstrap: OUTPUT must be a GAP string");
fi;
if D972_B4_KBMAG_BOOTSTRAP_MODE=1 and
   (D972KBBGapRoot=fail or D972KBBPackageDir=fail or
    not IsString(D972KBBGapRoot) or not IsString(D972KBBPackageDir)) then
  Error("KBMAG bootstrap: build mode needs GAPROOT and PACKAGE_DIR");
fi;

## The dispatch preamble supplies trusted runner paths.  Reject shell metachar-
## acters rather than interpolating an arbitrary preamble value into Exec().
D972KBBShellQuote:=function(s)
  local c;
  if not IsString(s) then Error("KBMAG bootstrap: path is not a string"); fi;
  for c in ["'","`","$","\\","\n","\r"] do
    if Position(s,c)<>fail then
      Error("KBMAG bootstrap: unsafe shell path");
    fi;
  od;
  return Concatenation("'",s,"'");
end;;

D972KBBJson:=function(x)
  local p,i;
  if x=true then return "true"; fi;
  if x=false then return "false"; fi;
  if x=fail then return "null"; fi;
  if IsInt(x) then return String(x); fi;
  if IsString(x) then
    return Concatenation("\"",ReplacedString(x,"\"","\\\""),"\"");
  fi;
  if not IsList(x) then Error("KBMAG bootstrap: JSON type drift"); fi;
  if Length(x)=0 then return "[]"; fi;
  p:=List([1..Length(x)],i->D972KBBJson(x[i]));
  return Concatenation("[",JoinStringsWithSeparator(p,","),"]");
end;;

D972KBBWriteReceipt:=function(status,loaded,probe,version,build,target)
  local f,j;
  j:=Concatenation(
    "{\"schema\":\"d972-b4-kbmag-bootstrap/v1\",",
    "\"status\":",D972KBBJson(status),",",
    "\"mode\":",String(D972_B4_KBMAG_BOOTSTRAP_MODE),",",
    "\"gap_version\":",D972KBBJson(GAPInfo.Version),",",
    "\"kbmag_loaded\":",D972KBBJson(loaded),",",
    "\"kbprog_probe\":",D972KBBJson(probe),",",
    "\"kbmag_version\":",D972KBBJson(version),",",
    "\"build_pass\":",D972KBBJson(build),",",
    "\"target\":",D972KBBJson(target),",
    "\"source\":\"setup-gap GAP 4.16.0 pkg/kbmag\",",
    "\"source_policy\":\"no_network_download\"}");
  f:=OutputTextFile(D972KBBOutput,false);;
  SetPrintFormattingStatus(f,false);;
  PrintTo(f,Concatenation(j,"\n"));;
  CloseStream(f);;
end;;

D972KBBBuildPass:=true;;
if D972_B4_KBMAG_BOOTSTRAP_MODE=1 then
  D972KBBStatusFile:=Filename(DirectoryTemporary(),
    "d972_b4_kbmag_bootstrap_v1.status");;
  D972KBBLogFile:=Filename(DirectoryTemporary(),
    "d972_b4_kbmag_bootstrap_v1.build.log");;
  D972KBBCommand:=Concatenation(
    "rm -f ",D972KBBShellQuote(D972KBBStatusFile),"; ",
    "cd ",D972KBBShellQuote(D972KBBPackageDir)," && ",
    "./configure ",D972KBBShellQuote(D972KBBGapRoot)," > ",
    D972KBBShellQuote(D972KBBLogFile)," 2>&1 && ",
    "make -j2 >> ",D972KBBShellQuote(D972KBBLogFile)," 2>&1 && ",
    "printf PASS > ",D972KBBShellQuote(D972KBBStatusFile)," || ",
    "printf FAIL > ",D972KBBShellQuote(D972KBBStatusFile));;
  Print("B4_KBMAG_BOOTSTRAP_BUILD_BEGIN package=",D972KBBPackageDir,
    " gaproot=",D972KBBGapRoot,"\n");
  Exec(D972KBBCommand);;
  if StringFile(D972KBBStatusFile)<>"PASS" then
    D972KBBBuildPass:=false;;
    Error("KBMAG bootstrap: configure/make failed; inspect build log");
  fi;
  Print("B4_KBMAG_BOOTSTRAP_BUILD_PASS package=",D972KBBPackageDir,
    " gaproot=",D972KBBGapRoot,"\n");
fi;

if LoadPackage("kbmag")<>true then
  D972KBBWriteReceipt("PACKAGE_FAIL",false,false,"unknown",
    D972KBBBuildPass,D972KBBTarget);;
  Print("B4_KBMAG_BOOTSTRAP_PACKAGE_FAIL\n");
  Error("KBMAG bootstrap: LoadPackage(kbmag) failed");
fi;
D972KBBInfo:=PackageInfo("kbmag");;
D972KBBVersion:="unknown";;
if Length(D972KBBInfo)>0 and IsBound(D972KBBInfo[1].Version) then
  D972KBBVersion:=D972KBBInfo[1].Version;
fi;
Print("B4_KBMAG_BOOTSTRAP_PACKAGE_PASS version=",D972KBBVersion,"\n");

## This invokes the external kbprog binary through the package interface.
## A package-only load is insufficient: the reduction and identity check are
## both required before any six-generator target is read.
D972KBBF:=FreeGroup("a");;
D972KBBG:=D972KBBF/[D972KBBF.1^2];;
D972KBBRws:=KBMAGRewritingSystem(D972KBBG);;
SetOrderingOfKBMAGRewritingSystem(D972KBBRws,"shortlex");;
D972KBBOpts:=OptionsRecordOfKBMAGRewritingSystem(D972KBBRws);;
D972KBBOpts.maxeqns:=100;;
D972KBBOpts.maxstates:=100;;
D972KBBOpts.maxwdiffs:=100;;
D972KBBKbResult:=KnuthBendix(D972KBBRws);;
D972KBBReduced:=ReducedForm(D972KBBRws,D972KBBF.1^2);;
if not IsOne(D972KBBReduced) then
  D972KBBWriteReceipt("KBPROG_PROBE_FAIL",true,false,D972KBBVersion,
    D972KBBBuildPass,D972KBBTarget);;
  Print("B4_KBMAG_BOOTSTRAP_KBPROG_PROBE_FAIL\n");
  Error("KBMAG bootstrap: kbprog reduction probe failed");
fi;
D972KBBProbePass:=true;;
D972KBBWriteReceipt("PREFLIGHT_PASS",true,D972KBBProbePass,
  D972KBBVersion,D972KBBBuildPass,D972KBBTarget);;
Print("B4_KBMAG_BOOTSTRAP_PREFLIGHT_PASS version=",D972KBBVersion,
  " kbprog_probe=true\n");

if D972KBBTarget<>fail then
  Print("B4_KBMAG_BOOTSTRAP_TARGET_BEGIN target=",D972KBBTarget,"\n");
  Read(D972KBBTarget);;
  Print("B4_KBMAG_BOOTSTRAP_TARGET_READ_DONE target=",D972KBBTarget,"\n");
fi;
Print("B4_KBMAG_BOOTSTRAP_FINAL_MARKER mode=",
  D972_B4_KBMAG_BOOTSTRAP_MODE," target=",D972KBBTarget<>fail,"\n");
