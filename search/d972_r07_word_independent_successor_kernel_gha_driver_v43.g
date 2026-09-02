#############################################################################
## Task503 A4 actual-production shard wiring.  ASCII only.
## Row-26 release members are authenticated before one v24 producer run.
#############################################################################
if not IsBound(D972_R07_A4_TASK503_MODE) then
  Error("task503 driver: ACTUAL_PRODUCTION mode required");
fi;
if D972_R07_A4_TASK503_MODE<>"ACTUAL_PRODUCTION" then
  Error("task503 driver: only ACTUAL_PRODUCTION is permitted");
fi;

D503Run:="33506331399";;
D503Job:="99851144256";;
D503Head:="5dbc895552efdaffb13bb7b10e595430026f4c3c";;
D503ArtifactID:="9809473723";;
D503ArtifactName:="gap-run-out";;
D503ArtifactSHA:="4a82302e49ddfdd7790df0e0082d0762de3238c0b4e0de23259d97bd1a2af445";;
D503Release:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9809473723_gap-run-out.a4-row26.zip";;
D503ReleaseBytes:=56410;;
D503ReleaseSHA:="5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a336e3";;
D503Producer:="search/d972_r07_word_independent_successor_kernel_v24.py";;
D503ProducerBytes:=34535;;
D503ProducerSHA:="8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe";;
D503ProducerGeneratedBytes:=285814;;
D503ProducerGeneratedSHA:="9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a";;
D503Checker:="crosscheck/check_d972_r07_word_independent_successor_kernel_v33.py";;
D503CheckerBytes:=24033;;
D503CheckerSHA:="44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf";;
D503CheckerGeneratedBytes:=312046;;
D503CheckerGeneratedSHA:="cb1d2b390beb3bdbd71d2175983310971d0669f6a6d7b77e1e64f29ceae61f57";;
D503Zip:="ci/out/task503_row26_release.zip";;
D503Extract:="ci/out/task503_row26_release_extract";;
D503PhysicalRoot:="ci/out/task503_v24_physical";;
D503ProducerOutput:="ci/out/task503_v24_producer.json";;
D503ProducerLog:="ci/out/task503_v24_producer.log";;
D503ProducerCheckpoint:="ci/out/d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json";;
D503CheckerOutput:="ci/out/task503_v33_checker.json";;
D503CheckerLog:="ci/out/task503_v33_checker.log";;
D503Success:="ci/out/task503_v43.success";;
D503CheckerCheckpoint:="ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json";;
D503InternalSeconds:=14400;;
D503ExternalSeconds:=15000;;
D503InternalRssBytes:=8000000000;;
D503RssLimitKiB:=8500000;;
D503ProducerTerminalPrefix:="R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL";;
D503ProducerPass:="R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS";;
D503ProducerResource:="R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL UNKNOWN_RESOURCE";;
D503CheckerTerminalPrefix:="R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL";;
D503CheckerPass:="R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS";;
D503CheckerResource:="R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL UNKNOWN_RESOURCE";;

D503Members:=[
 ["d972_r07_word_independent_successor_kernel_v40.json",9300,"7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.base.checkpoint.json",25581,"595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json",700,"910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000001.json",3551,"d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000002.json",3625,"acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523"],
 ["d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json",8991,"b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2"]
];;
D503Authority:=[
 "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
 "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
 "ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
 "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
 "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json"
];;

D503Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task503 missing output ",path); fi;
 return raw;
end;;
D503Count:=function(raw,needle)
 local at,count;
 if Length(needle)=0 then Error("task503 empty needle"); fi;
 count:=0;; at:=PositionSublist(raw,needle);;
 while at<>fail do count:=count+1;; at:=PositionSublist(raw,needle,at+1);; od;
 return count;
end;;
D503ShellQuote:=function(path)
 if PositionSublist(path,"'")<>fail or PositionSublist(path,"\n")<>fail or
    PositionSublist(path,"\r")<>fail then Error("task503 unsafe path"); fi;
 return Concatenation("'",path,"'");
end;;
D503LiteralQuote:=function(text)
 if PositionSublist(text,"'")<>fail or PositionSublist(text,"\r")<>fail or
    PositionSublist(text,"\n")<>fail then Error("task503 unsafe literal"); fi;
 return Concatenation("'",text,"'");
end;;

if Length(D503Members)<>6 then Error("task503 six release members"); fi;
if D503Run<>"33506331399" or D503Job<>"99851144256" or
   D503Head<>"5dbc895552efdaffb13bb7b10e595430026f4c3c" or
   D503ArtifactID<>"9809473723" or D503ArtifactName<>"gap-run-out" or
   D503ArtifactSHA<>"4a82302e49ddfdd7790df0e0082d0762de3238c0b4e0de23259d97bd1a2af445" then
 Error("task503 release provenance drift");
fi;
if D503ReleaseBytes<>56410 or Length(D503ReleaseSHA)=0 then
 Error("task503 release pin missing");
fi;
if D503ExternalSeconds<=D503InternalSeconds or
   D503RssLimitKiB*1024<=D503InternalRssBytes then
 Error("task503 external margin drift");
fi;
if not IsDirectoryPath("ci/out") then
 if CreateDir("ci/out")=fail then Error("task503 cannot create ci/out"); fi;
fi;
for D503AuthorityPath in D503Authority do
 if not IsExistingFile(D503AuthorityPath) or IsDirectoryPath(D503AuthorityPath) then
  Error("task503 authority input missing ",D503AuthorityPath);
 fi;
od;
for D503Owned in [D503Zip,D503Extract,D503PhysicalRoot,D503ProducerOutput,
                  D503ProducerLog,D503CheckerOutput,D503CheckerLog,D503Success] do
 if IsExistingFile(D503Owned) or IsDirectoryPath(D503Owned) then
  Error("task503 stale owned output ",D503Owned);
 fi;
od;

## Exercise GAP's executable-file reader on a temporary one-expression probe.
D503Probe:="ci/out/task503_v43_read_as_function_probe.g";;
D503ProbeStream:=OutputTextFile(D503Probe,false);;
if D503ProbeStream=fail then Error("task503 probe open"); fi;
SetPrintFormattingStatus(D503ProbeStream,false);;
PrintTo(D503ProbeStream,"return true;\n");;
CloseStream(D503ProbeStream);;
D503ProbeStream:=InputTextFile(D503Probe);;
if D503ProbeStream=fail then Error("task503 probe read"); fi;
D503ProbeFunction:=ReadAsFunction(D503ProbeStream);;
CloseStream(D503ProbeStream);;
if D503ProbeFunction()<>true then Error("task503 ReadAsFunction gate"); fi;
Exec(Concatenation("rm -f ",D503ShellQuote(D503Probe)));;

D503Script:=Concatenation(
 "#!/usr/bin/env bash\n",
 "set -euo pipefail\n",
 "umask 077\n",
 "command -v curl >/dev/null\n",
 "command -v unzip >/dev/null\n",
 "command -v sha256sum >/dev/null\n",
 "command -v timeout >/dev/null\n",
 "command -v python3 >/dev/null\n",
 "root=\"$(pwd -P)\"\n",
 "test -f \"$root/",D503Producer,"\"\n",
 "test -f \"$root/",D503Checker,"\"\n",
 "test \"$(wc -c < ",D503ShellQuote(D503Producer)," | tr -d '[:space:]')\" = ",String(D503ProducerBytes),"\n",
 "test \"$(sha256sum ",D503ShellQuote(D503Producer)," | cut -d' ' -f1)\" = ",D503ProducerSHA,"\n",
 "test \"$(wc -c < ",D503ShellQuote(D503Checker)," | tr -d '[:space:]')\" = ",String(D503CheckerBytes),"\n",
 "test \"$(sha256sum ",D503ShellQuote(D503Checker)," | cut -d' ' -f1)\" = ",D503CheckerSHA,"\n",
 "test \"$(python3 -u -B ",D503Producer," --source-patch-info | python3 -c 'import json,sys; x=json.load(sys.stdin); print(str(x[\"generated\"][\"bytes\"])+\":\"+x[\"generated\"][\"sha256\"])')\" = ",String(D503ProducerGeneratedBytes),":",D503ProducerGeneratedSHA,"\n",
 "test \"$(python3 -u -B ",D503Checker," --source-patch-info | python3 -c 'import json,sys; x=json.load(sys.stdin); print(str(x[\"generated\"][\"bytes\"])+\":\"+x[\"generated\"][\"sha256\"])')\" = ",String(D503CheckerGeneratedBytes),":",D503CheckerGeneratedSHA,"\n",
 "zip=",D503ShellQuote(D503Zip),"\n",
 "extract=",D503ShellQuote(D503Extract),"\n",
 "test ! -e \"$zip\" && test ! -e \"$extract\"\n",
 "curl --fail --location --retry 3 --silent --show-error ",D503ShellQuote(D503Release)," -o \"$zip\"\n",
 "test \"$(wc -c < \"$zip\" | tr -d '[:space:]')\" = ",String(D503ReleaseBytes),"\n",
 "test \"$(sha256sum \"$zip\" | cut -d' ' -f1)\" = ",D503ReleaseSHA,"\n",
 "mkdir \"$extract\"\n",
 "unzip -q \"$zip\" -d \"$extract\"\n");
for D503Member in D503Members do
 D503Script:=Concatenation(D503Script,
  "test \"$(unzip -Z1 \"$zip\" | grep -Fxc -- ",D503LiteralQuote(D503Member[1])," || true)\" = 1\n",
  "test -f \"$extract/",D503Member[1],"\"\n",
  "test ! -L \"$extract/",D503Member[1],"\"\n",
  "test \"$(wc -c < \"$extract/",D503Member[1],"\" | tr -d '[:space:]')\" = ",String(D503Member[2]),"\n",
  "test \"$(sha256sum \"$extract/",D503Member[1],"\" | cut -d' ' -f1)\" = ",D503Member[3],"\n",
  "cp \"$extract/",D503Member[1],"\" \"$root/ci/out/",D503Member[1],"\"\n",
  "test \"$(wc -c < \"$root/ci/out/",D503Member[1],"\" | tr -d '[:space:]')\" = ",String(D503Member[2]),"\n",
  "test \"$(sha256sum \"$root/ci/out/",D503Member[1],"\" | cut -d' ' -f1)\" = ",D503Member[3],"\n");
od;
D503Script:=Concatenation(D503Script,
 "for authority in ",D503ShellQuote(D503Authority[1])," ",D503ShellQuote(D503Authority[2])," ",
 D503ShellQuote(D503Authority[3])," ",D503ShellQuote(D503Authority[4])," ",D503ShellQuote(D503Authority[5]),"; do test -f \"$root/$authority\"; test ! -L \"$root/$authority\"; done\n",
 "test ! -e ",D503ShellQuote(D503PhysicalRoot),"\n",
 "mkdir -p ",D503ShellQuote(D503PhysicalRoot),"\n",
 "producer_start=$SECONDS\n",
 "ulimit -v ",String(D503RssLimitKiB),"\n",
 "timeout --foreground --signal=TERM --kill-after=60s ",String(D503ExternalSeconds),"s python3 -u -B ",D503Producer,
 " --input ci/in/d972_r07_seven_context_roof_presentation_v1.json",
 " --output ",D503ProducerOutput,
 " --checkpoint ",D503ProducerCheckpoint,
 " --resume ",D503ProducerCheckpoint,
 " --physical-root ",D503PhysicalRoot,
 " --seconds ",String(D503InternalSeconds)," --rss-bytes ",String(D503InternalRssBytes),
 " > ",D503ProducerLog," 2>&1\n",
 "producer_elapsed=$((SECONDS-producer_start))\n",
 "test \"$producer_elapsed\" -lt ",String(D503ExternalSeconds),"\n",
 "test -s ",D503ProducerLog,"\n",
 "test -s ",D503ProducerOutput,"\n",
 "test \"$(grep -Ec '^",D503ProducerTerminalPrefix," (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS|UNKNOWN_RESOURCE)$' ",D503ProducerLog," || true)\" = 1\n",
 "test \"$(grep -Fc UNKNOWN_INPUT ",D503ProducerLog," || true)\" = 0\n",
 "test \"$(grep -Fc HARD_STOP ",D503ProducerLog," || true)\" = 0\n",
 "test \"$(grep -Fc ERROR ",D503ProducerLog," || true)\" = 0\n",
 "test \"$(grep -Fc Traceback ",D503ProducerLog," || true)\" = 0\n",
 "if grep -Fxc ",D503LiteralQuote(D503ProducerResource)," ",D503ProducerLog," >/dev/null; then\n",
 "  test \"$(grep -Fo '\"status\":\"UNKNOWN_RESOURCE\"' ",D503ProducerOutput," | wc -l | tr -d '[:space:]')\" = 1\n",
 "  test \"$(grep -Fo '\"terminal\":\"UNKNOWN_RESOURCE\"' ",D503ProducerOutput," | wc -l | tr -d '[:space:]')\" = 1\n",
 "  test \"$(grep -Fc ",D503LiteralQuote(D503CheckerTerminalPrefix)," ",D503ProducerLog," || true)\" = 0\n",
 "  printf '%s\\n' ",D503LiteralQuote("TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_V43_RESOURCE_PASS terminal=UNKNOWN_RESOURCE producer_processes=1 checker_processes=0")," | tee ",D503Success,"\n",
 "else\n",
 "  test \"$(grep -Fxc ",D503LiteralQuote(D503ProducerPass)," ",D503ProducerLog," || true)\" = 1\n",
 "  checker_start=$SECONDS\n",
 "  timeout --foreground --signal=TERM --kill-after=60s ",String(D503ExternalSeconds),"s python3 -u -B ",D503Checker,
 " --input ci/in/d972_r07_seven_context_roof_presentation_v1.json",
 " --producer ",D503ProducerOutput,
 " --output ",D503CheckerOutput,
 " --checkpoint ",D503CheckerCheckpoint,
 " --resume ",D503CheckerCheckpoint,
 " --seconds ",String(D503InternalSeconds)," --rss-bytes ",String(D503InternalRssBytes),
 " > ",D503CheckerLog," 2>&1\n",
 "  checker_elapsed=$((SECONDS-checker_start))\n",
 "  test \"$checker_elapsed\" -lt ",String(D503ExternalSeconds),"\n",
 "  test -s ",D503CheckerLog,"\n",
 "  test -s ",D503CheckerOutput,"\n",
 "  test \"$(grep -Ec '^",D503CheckerTerminalPrefix," (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS|UNKNOWN_RESOURCE)$' ",D503CheckerLog," || true)\" = 1\n",
 "  test \"$(grep -Fc UNKNOWN_INPUT ",D503CheckerLog," || true)\" = 0\n",
 "  test \"$(grep -Fc HARD_STOP ",D503CheckerLog," || true)\" = 0\n",
 "  test \"$(grep -Fc ERROR ",D503CheckerLog," || true)\" = 0\n",
 "  test \"$(grep -Fc Traceback ",D503CheckerLog," || true)\" = 0\n",
 "  if grep -Fxc ",D503LiteralQuote(D503CheckerResource)," ",D503CheckerLog," >/dev/null; then\n",
 "    printf '%s\\n' ",D503LiteralQuote("TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_V43_RESOURCE_PASS terminal=UNKNOWN_RESOURCE producer_processes=1 checker_processes=1")," | tee ",D503Success,"\n",
 "  else\n",
 "    test \"$(grep -Fxc ",D503LiteralQuote(D503CheckerPass)," ",D503CheckerLog," || true)\" = 1\n",
 "    printf '%s\\n' ",D503LiteralQuote("TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_V43_PASS terminal=R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS producer_processes=1 checker_processes=1")," | tee ",D503Success,"\n",
 "  fi\n",
 "fi\n");

D503Shell:="ci/out/task503_v43.sh";;
D503S:=OutputTextFile(D503Shell,false);;
if D503S=fail then Error("task503 shell open"); fi;
SetPrintFormattingStatus(D503S,false);;
PrintTo(D503S,D503Script);;
CloseStream(D503S);;
Exec(Concatenation("bash ",D503ShellQuote(D503Shell)));;
if not IsExistingFile(D503ProducerOutput) then Error("task503 producer output missing"); fi;
if not IsExistingFile(D503ProducerLog) then Error("task503 producer log missing"); fi;
if PositionSublist(D503Read(D503ProducerLog),"UNKNOWN_INPUT")<>fail or
   PositionSublist(D503Read(D503ProducerLog),"HARD_STOP")<>fail or
   PositionSublist(D503Read(D503ProducerLog),"Traceback")<>fail then
 Error("task503 forbidden producer terminal");
fi;
if not IsExistingFile(D503Success) then Error("task503 success marker missing"); fi;
D503SuccessRaw:=D503Read(D503Success);;
if D503SuccessRaw<>"TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_V43_RESOURCE_PASS terminal=UNKNOWN_RESOURCE producer_processes=1 checker_processes=0\n" and
   D503SuccessRaw<>"TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_V43_RESOURCE_PASS terminal=UNKNOWN_RESOURCE producer_processes=1 checker_processes=1\n" and
   D503SuccessRaw<>"TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_V43_PASS terminal=R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS producer_processes=1 checker_processes=1\n" then
 Error("task503 success marker drift");
fi;
Print("TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_V43_TRANSPORT_PASS release_bytes=56410 producer_processes=1 resource_branch=typed checker_branch=at_most_one\n");
