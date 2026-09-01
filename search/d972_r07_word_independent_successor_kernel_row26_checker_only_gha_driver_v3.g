#############################################################################
## Task483 A4 row-26 counter-transport checker-only replay.  ASCII only.
## Release and six replay members are authenticated before one checker runs.
#############################################################################
if not IsBound(D972_R07_A4_ROW26_COUNTER_TRANSPORT_CHECKER_ONLY_V3_MODE) then
  Error("task483 driver: CHECKER_ONLY mode required");
fi;
if D972_R07_A4_ROW26_COUNTER_TRANSPORT_CHECKER_ONLY_V3_MODE<>"CHECKER_ONLY" then
  Error("task483 driver: only CHECKER_ONLY is permitted");
fi;

D483Run:="33506331399";;
D483Job:="99851144256";;
D483Head:="5dbc895552efdaffb13bb7b10e595430026f4c3c";;
D483ArtifactID:="9809473723";;
D483ArtifactName:="gap-run-out";;
D483ArtifactSHA:="4a82302e49ddfdd7790df0e0082d0762de3238c0b4e0de23259d97bd1a2af445";;
D483Release:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9809473723_gap-run-out.a4-row26.zip";;
D483Zip:="ci/out/task483_artifact_9809473723.zip";;
D483Extract:="ci/out/task483_artifact_9809473723_extract";;
D483Checker:="crosscheck/check_d972_r07_word_independent_successor_kernel_v31.py";;
D483CheckerBytes:=19483;;
D483CheckerSHA:="7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e";;
D483ZipBytes:=56410;;
D483ZipSHA:="5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3";;
D483InternalSeconds:=14400;;
D483TimeoutSeconds:=15000;;
D483InternalRssBytes:=8000000000;;
D483RssLimitKiB:=8500000;;
D483Log:="ci/out/d972_r07_word_independent_successor_kernel_v31.checker.log";;
D483Output:="ci/out/d972_r07_word_independent_successor_kernel_v31.verdict.json";;
D483Receipt:="ci/out/d972_r07_word_independent_successor_kernel_v31.receipt.txt";;
D483Shell:="ci/out/d972_r07_word_independent_successor_kernel_v31.driver.sh";;
D483OK:="ci/out/d972_r07_word_independent_successor_kernel_v31.driver.ok";;
D483TerminalPrefix:="R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL";;
D483Terminal:="R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL UNKNOWN_RESOURCE";;

D483Inputs:=[
 ["d972_r07_word_independent_successor_kernel_v40.json",9300,"7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.base.checkpoint.json",25581,"595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json",700,"910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000001.json",3551,"d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000002.json",3625,"acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523"],
 ["d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json",8991,"b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2"]
];;
D483Authority:=[
 "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
 "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
 "ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
 "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
 "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json"
];;

D483Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail then Error("task483 missing output ",path); fi;
 return raw;
end;;
D483Count:=function(raw,needle)
 local at,count;
 if Length(needle)=0 then Error("task483 empty needle"); fi;
 count:=0;; at:=PositionSublist(raw,needle);;
 while at<>fail do count:=count+1;; at:=PositionSublist(raw,needle,at+1);; od;
 return count;
end;;
D483ShellQuote:=function(path)
 if PositionSublist(path,"'")<>fail or PositionSublist(path,"\n")<>fail or
    PositionSublist(path,"\r")<>fail then Error("task483 unsafe path"); fi;
 return Concatenation("'",path,"'");
end;;
D483LiteralQuote:=function(text)
 if PositionSublist(text,"'")<>fail or PositionSublist(text,"\r")<>fail or
    PositionSublist(text,"\n")<>fail then Error("task483 unsafe literal"); fi;
 return Concatenation("'",text,"'");
end;;

if Length(D483Inputs)<>6 then Error("task483 six replay members"); fi;
if D483Run<>"33506331399" or D483Job<>"99851144256" or
   D483Head<>"5dbc895552efdaffb13bb7b10e595430026f4c3c" or
   D483ArtifactID<>"9809473723" or D483ArtifactName<>"gap-run-out" or
   D483ArtifactSHA<>"4a82302e49ddfdd7790df0e0082d0762de3238c0b4e0de23259d97bd1a2af445" or
   D483Release<>"https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9809473723_gap-run-out.a4-row26.zip" then
 Error("task483 immutable run/artifact binding drift");
fi;
if D483CheckerBytes<=0 or Length(D483CheckerSHA)<>64 then
 Error("task483 checker pin missing");
fi;
if D483TimeoutSeconds<=D483InternalSeconds or
   D483RssLimitKiB*1024<=D483InternalRssBytes then
 Error("task483 external timeout/RSS margin drift");
fi;
if not IsDirectoryPath("ci/out") then
 if CreateDir("ci/out")=fail then Error("task483 cannot create ci/out"); fi;
fi;
for D483AuthorityPath in D483Authority do
 if not IsExistingFile(D483AuthorityPath) or IsDirectoryPath(D483AuthorityPath) then
  Error("task483 authority input missing ",D483AuthorityPath);
 fi;
od;
for D483Input in D483Inputs do
 if IsExistingFile(Concatenation("ci/out/",D483Input[1])) or
    IsDirectoryPath(Concatenation("ci/out/",D483Input[1])) then
  Error("task483 stale owned replay member ",D483Input[1]);
 fi;
od;
for D483Owned in [D483Zip,D483Log,D483Output,D483Receipt,D483Shell,D483OK] do
 if IsExistingFile(D483Owned) or IsDirectoryPath(D483Owned) then
  Error("task483 stale owned output ",D483Owned);
 fi;
od;
if IsDirectoryPath(D483Extract) then Error("task483 stale extraction root"); fi;

D483Script:=Concatenation(
 "set -euo pipefail\n",
 "command -v curl >/dev/null\n",
 "command -v unzip >/dev/null\n",
 "command -v sha256sum >/dev/null\n",
 "command -v timeout >/dev/null\n",
 "command -v realpath >/dev/null\n",
 "root=\"$(pwd -P)\"\n",
 "test -f \"$root/",D483Checker,"\"\n",
 "test \"$(realpath -- \"$root/",D483Checker,"\")\" = \"$root/",D483Checker,"\"\n",
 "zip=",D483ShellQuote(D483Zip),"\n",
 "extract=",D483ShellQuote(D483Extract),"\n",
 "test ! -e \"$zip\" && test ! -e \"$extract\"\n",
 "curl --fail --location --retry 3 --silent --show-error ",D483ShellQuote(D483Release)," -o \"$zip\"\n",
 "test \"$(wc -c < \"$zip\" | tr -d '[:space:]')\" = ",String(D483ZipBytes),"\n",
 "test \"$(sha256sum \"$zip\" | cut -d' ' -f1)\" = ",D483ZipSHA,"\n",
 "mkdir \"$extract\"\n",
 "unzip -q \"$zip\" -d \"$extract\"\n");
for D483Input in D483Inputs do
 D483Script:=Concatenation(D483Script,
  "test \"$(unzip -Z1 \"$zip\" | grep -Fxc -- ",D483LiteralQuote(D483Input[1])," || true)\" = 1\n",
  "test -f \"$extract/",D483Input[1],"\"\n",
  "test ! -L \"$extract/",D483Input[1],"\"\n",
  "test \"$(wc -c < \"$extract/",D483Input[1],"\" | tr -d '[:space:]')\" = ",String(D483Input[2]),"\n",
  "test \"$(sha256sum \"$extract/",D483Input[1],"\" | cut -d' ' -f1)\" = ",D483Input[3],"\n",
  "cp \"$extract/",D483Input[1],"\" \"$root/ci/out/",D483Input[1],"\"\n",
  "test \"$(wc -c < \"$root/ci/out/",D483Input[1],"\" | tr -d '[:space:]')\" = ",String(D483Input[2]),"\n",
  "test \"$(sha256sum \"$root/ci/out/",D483Input[1],"\" | cut -d' ' -f1)\" = ",D483Input[3],"\n");
od;
for D483AuthorityPath in D483Authority do
 D483Script:=Concatenation(D483Script,
  "test -f \"$root/",D483AuthorityPath,"\"\n",
  "test ! -L \"$root/",D483AuthorityPath,"\"\n");
od;
D483Script:=Concatenation(D483Script,
 "test \"$(wc -c < ",D483ShellQuote(D483Checker)," | tr -d '[:space:]')\" = ",String(D483CheckerBytes),"\n",
 "test \"$(sha256sum ",D483ShellQuote(D483Checker)," | cut -d' ' -f1)\" = ",D483CheckerSHA,"\n",
 "ulimit -v ",String(D483RssLimitKiB),"\n",
 "timeout --foreground --signal=TERM --kill-after=60s ",String(D483TimeoutSeconds),"s python3 -u -B \"$root/",D483Checker,"\"",
 " --input ci/in/d972_r07_seven_context_roof_presentation_v1.json",
 " --producer ci/out/d972_r07_word_independent_successor_kernel_v40.json",
 " --output ci/out/d972_r07_word_independent_successor_kernel_v31.verdict.json",
 " --checkpoint ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json",
 " --resume ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json",
 " --seconds ",String(D483InternalSeconds)," --rss-bytes ",String(D483InternalRssBytes),
 " --task198-receipt ci/in/d972_r07_seven_context_roof_presentation_v1.json",
 " --task198-manifest ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
 " --task198-producer ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
 " --task198-checker ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
 " --task198-verdict ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
 " > \"$root/",D483Log,"\" 2>&1\n",
 "test \"$(grep -Ec '^",D483TerminalPrefix," ' \"$root/",D483Log,"\" || true)\" = 1\n",
 "test \"$(grep -Fxc ",D483LiteralQuote(D483Terminal)," \"$root/",D483Log,"\" || true)\" = 1\n",
 "test \"$(grep -Fc Traceback \"$root/",D483Log,"\" || true)\" = 0\n",
 "test \"$(grep -Fc STOP \"$root/",D483Log,"\" || true)\" = 0\n",
 "test -s \"$root/",D483Output,"\"\n",
 "test \"$(grep -Fo '\"status\":\"UNKNOWN_RESOURCE\"' \"$root/",D483Output,"\" | wc -l | tr -d '[:space:]')\" = 1\n",
 "test \"$(grep -Fo '\"terminal\":\"UNKNOWN_RESOURCE\"' \"$root/",D483Output,"\" | wc -l | tr -d '[:space:]')\" = 1\n",
 "test \"$(grep -o '\"self_digest_sha256\":\"[0-9a-f]\\{64\\}\"' \"$root/",D483Output,"\" | wc -l | tr -d '[:space:]')\" = 1\n",
 "verdict_bytes=\"$(wc -c < \"$root/",D483Output,"\" | tr -d '[:space:]')\"\n",
 "verdict_sha=\"$(sha256sum \"$root/",D483Output,"\" | cut -d' ' -f1)\"\n",
 "verdict_self_digest=\"$(grep -o ",D483LiteralQuote("\"self_digest_sha256\":\"[0-9a-f]\\{64\\}\"")," \"$root/",D483Output,"\" | cut -d ",D483LiteralQuote("\"")," -f4)\"\n",
 "test \"${#verdict_self_digest}\" = 64\n",
 "printf '%s\\n' ",D483LiteralQuote("schema=d972-r07-a4-row26-counter-transport-checker-only/v3"),
 " ",D483LiteralQuote(Concatenation("run=",D483Run)),
 " ",D483LiteralQuote(Concatenation("job=",D483Job)),
 " ",D483LiteralQuote(Concatenation("head=",D483Head)),
 " ",D483LiteralQuote(Concatenation("artifact_id=",D483ArtifactID)),
 " ",D483LiteralQuote(Concatenation("artifact_name=",D483ArtifactName)),
 " ",D483LiteralQuote(Concatenation("artifact_sha256=",D483ArtifactSHA)),
 " ",D483LiteralQuote(Concatenation("release=",D483Release)),
 " ",D483LiteralQuote(Concatenation("asset_bytes=",String(D483ZipBytes))),
 " ",D483LiteralQuote(Concatenation("asset_sha256=",D483ZipSHA)),
 " ",D483LiteralQuote(Concatenation("checker=",D483Checker)),
 " ",D483LiteralQuote(Concatenation("checker_bytes=",String(D483CheckerBytes))),
 " ",D483LiteralQuote(Concatenation("checker_sha256=",D483CheckerSHA)),
 " ",D483LiteralQuote("terminal=UNKNOWN_RESOURCE"),
 " ",D483LiteralQuote("checker_terminal_lines=1"),
 " ",D483LiteralQuote("checker_processes=1"),
 " ",D483LiteralQuote("producer_processes=0"),
 " ",D483LiteralQuote(Concatenation("row26_head_sha256=",D483Inputs[3][3])),
 " ",D483LiteralQuote(Concatenation("row26_delta1_sha256=",D483Inputs[4][3])),
 " ",D483LiteralQuote(Concatenation("row26_delta2_sha256=",D483Inputs[5][3])),
 " > \"$root/",D483Receipt,"\"\n",
 "printf '%s\\n' \"verdict_bytes=$verdict_bytes\" \"verdict_sha256=$verdict_sha\" \"verdict_self_digest_sha256=$verdict_self_digest\" >> \"$root/",D483Receipt,"\"\n",
 "test -s \"$root/",D483Receipt,"\"\n",
 "printf '%s\\n' ",D483LiteralQuote("TASK483_R07_A4_ROW26_COUNTER_TRANSPORT_V31_PASS"),
 " > \"$root/",D483OK,"\"\n");

D483Stream:=OutputTextFile(D483Shell,false);;
if D483Stream=fail then Error("task483 shell open"); fi;
SetPrintFormattingStatus(D483Stream,false);;
PrintTo(D483Stream,D483Script);;
CloseStream(D483Stream);;
Exec(Concatenation("bash ",D483Shell));;
if not IsExistingFile(D483OK) then Error("task483 shell failed or success marker missing"); fi;
D483OKRaw:=D483Read(D483OK);;
if D483OKRaw<>"TASK483_R07_A4_ROW26_COUNTER_TRANSPORT_V31_PASS\n" then
 Error("task483 shell success marker drift");
fi;
D483ReceiptRaw:=D483Read(D483Receipt);;
if Length(D483ReceiptRaw)=0 or D483Count(D483ReceiptRaw,"schema=d972-r07-a4-row26-counter-transport-checker-only/v3")<>1 or
   D483Count(D483ReceiptRaw,"run=33506331399")<>1 or D483Count(D483ReceiptRaw,"job=99851144256")<>1 or
   D483Count(D483ReceiptRaw,"head=5dbc895552efdaffb13bb7b10e595430026f4c3c")<>1 or
   D483Count(D483ReceiptRaw,"terminal=UNKNOWN_RESOURCE")<>1 or
   D483Count(D483ReceiptRaw,"checker_terminal_lines=1")<>1 or
   D483Count(D483ReceiptRaw,"checker_processes=1")<>1 or D483Count(D483ReceiptRaw,"producer_processes=0")<>1 or
   D483Count(D483ReceiptRaw,"verdict_bytes=")<>1 or D483Count(D483ReceiptRaw,"verdict_sha256=")<>1 or
   D483Count(D483ReceiptRaw,"verdict_self_digest_sha256=")<>1 or
   D483Count(D483ReceiptRaw,"row26_head_sha256=910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114")<>1 or
   D483Count(D483ReceiptRaw,"row26_delta1_sha256=d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19")<>1 or
   D483Count(D483ReceiptRaw,"row26_delta2_sha256=acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523")<>1 then
 Error("task483 receipt binding failed");
fi;
Print("TASK483_R07_A4_ROW26_COUNTER_TRANSPORT_V31_PASS terminal=UNKNOWN_RESOURCE process_count=1 producer_process_count=0\n");


