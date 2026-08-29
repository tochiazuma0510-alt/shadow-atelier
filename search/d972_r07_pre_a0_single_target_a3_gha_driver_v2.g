D363Mode:="gha";;
D363P0:="ci/in/d972_r07_pre_a0_single_target_a3_v2.prereg.v1.json";;
D363Producer:="search/d972_r07_pre_a0_single_target_a3_v2.py";;
D363Checker:="crosscheck/check_d972_r07_pre_a0_single_target_a3_v2.py";;
D363Receipt:="ci/out/d972_r07_pre_a0_single_target_a3_v2.json";;
D363Verdict:="ci/out/d972_r07_pre_a0_single_target_a3_v2.verdict.json";;
D363ProducerLog:="ci/out/d972_r07_pre_a0_single_target_a3_v2.producer.log";;
D363CheckerLog:="ci/out/d972_r07_pre_a0_single_target_a3_v2.checker.log";;
D363Shell:="ci/out/d972_r07_pre_a0_single_target_a3_v2.driver.sh";;
D363Sentinel:="ci/out/d972_r07_pre_a0_single_target_a3_v2.driver.accepted";;
D363Member:="R07_PRE_A0_A3_PROJECTED_MEMBER";;
D363Nonmember:="R07_PRE_A0_A3_PROJECTED_NONMEMBER_DUAL";;
D363UnknownInput:="UNKNOWN_INPUT";;
D363UnknownResource:="UNKNOWN_RESOURCE";;
D363P0Bytes:=13748;;
D363P0SHA:="4a7f966d803dfdf7977dc73ab2db9b7f54d0d932ec2a10e410e034b5b6b151af";;
D363P0Self:="f633498efef1e8fb2adf02a474dcca05b87de83fe5655e1e805f8e10f1f916a4";;
D363Pins:=[
  [D363P0,D363P0SHA,D363P0Bytes],
  [D363Producer,"01578037cfabc73fdb7cb29d7725a41f903b05aab0f689d259fc89f56489daa6",76763],
  [D363Checker,"3d77b6e6ca577bd762512b99a1ba2be647d994c4632b66ca2478259fea06f403",84273]
];;

D363Hex64:=function(value)
  local alphabet,character;
  if not IsString(value) or Length(value)<>64 then return false; fi;
  alphabet:="0123456789abcdef";;
  for character in value do
    if Position(alphabet,character)=fail then return false; fi;
  od;
  return true;
end;;

if not D363Hex64(D363P0Self) then
  Error("task363: malformed P0 self seal"); fi;

D363Read:=function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task363: missing ",label); fi;
  return raw;
end;;

D363Pin:=function(row)
  local raw;
  if not D363Hex64(row[2]) or not IsInt(row[3]) or row[3]<=0 then
    Error("task363: malformed full pin ",row[1]); fi;
  raw:=D363Read(row[1],"pinned final owner");;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("task363: pin drift ",row[1]); fi;
end;;

for D363PinRow in D363Pins do D363Pin(D363PinRow);; od;
for D363Path in [D363Receipt,D363Verdict,D363ProducerLog,D363CheckerLog,
                 D363Shell,D363Sentinel] do
  if IsExistingFile(D363Path) then
    Error("task363: stale output ",D363Path); fi;
od;
if not IsDirectoryPath("ci/out") then
  if CreateDir("ci/out")=fail then Error("task363: cannot create ci/out"); fi;
fi;
if not IsDirectoryPath("ci/out") then
  Error("task363: ci/out is not a directory"); fi;

D363Stream:=OutputTextFile(D363Shell,false);;
if D363Stream=fail then Error("task363: cannot open command script"); fi;
SetPrintFormattingStatus(D363Stream,false);
PrintTo(D363Stream,"set -u -o pipefail\n");
PrintTo(D363Stream,"R='",D363Receipt,"'\n");
PrintTo(D363Stream,"V='",D363Verdict,"'\n");
PrintTo(D363Stream,"PL='",D363ProducerLog,"'\n");
PrintTo(D363Stream,"CL='",D363CheckerLog,"'\n");
PrintTo(D363Stream,"OK='",D363Sentinel,"'\n");
PrintTo(D363Stream,"MEM='",D363Member,"'\n");
PrintTo(D363Stream,"NON='",D363Nonmember,"'\n");
PrintTo(D363Stream,"UI='",D363UnknownInput,"'\n");
PrintTo(D363Stream,"UR='",D363UnknownResource,"'\n");
PrintTo(D363Stream,"fail(){ printf 'D363_DRIVER_FAILURE phase=%s\\n' \"$1\"; test ! -f \"$PL\" || cat \"$PL\"; test ! -f \"$CL\" || cat \"$CL\"; exit 40; }\n");
PrintTo(D363Stream,"unknown(){ printf 'D363_DRIVER_UNKNOWN side=%s terminal=%s process_status=%s\\n' \"$1\" \"$2\" \"$3\"; test ! -f \"$PL\" || cat \"$PL\"; test ! -f \"$CL\" || cat \"$CL\"; exit 41; }\n");
PrintTo(D363Stream,"printf 'D363_GHA_ESTIMATE five_case_reference_seconds=493 one_case_side_estimate_seconds=300 internal_seconds=1800 external_seconds=2100 serial_external_seconds=4200 workflow_seconds=21600\\n'\n");
PrintTo(D363Stream,"compgen -G 'ci/out/.d972_r07_pre_a0_single_target_a3_v2.json.tmp.*' >/dev/null && fail stale-receipt-temp\n");
PrintTo(D363Stream,"compgen -G 'ci/out/.d972_r07_pre_a0_single_target_a3_v2.verdict.json.tmp.*' >/dev/null && fail stale-verdict-temp\n");
PrintTo(D363Stream,"timeout --signal=TERM --kill-after=30s 2100s python3 -u -B '",
  D363Producer,"' --output \"$R\" >\"$PL\" 2>&1\n");
PrintTo(D363Stream,"ps=$?\n");
PrintTo(D363Stream,"pc=$(grep -Ec '^D363_PRODUCER_TERMINAL (",D363Member,
  "|",D363Nonmember,"|",D363UnknownInput,"|",D363UnknownResource,
  ")$' \"$PL\" || true)\n");
PrintTo(D363Stream,"pa=$(grep -Ec '^D363_PRODUCER_TERMINAL ' \"$PL\" || true)\n");
PrintTo(D363Stream,"test \"$pc\" = 1 -a \"$pa\" = 1 || unknown producer NO_EXACT_TERMINAL \"$ps\"\n");
PrintTo(D363Stream,"pt=$(sed -n 's/^D363_PRODUCER_TERMINAL //p' \"$PL\")\n");
PrintTo(D363Stream,"case \"$pt\" in \"$UI\"|\"$UR\") unknown producer \"$pt\" \"$ps\";; \"$MEM\"|\"$NON\") test \"$ps\" = 0 || fail producer-status;; *) unknown producer BAD_TERMINAL \"$ps\";; esac\n");
PrintTo(D363Stream,"test -f \"$R\" -a ! -L \"$R\" -a -s \"$R\" || fail receipt-owner\n");
PrintTo(D363Stream,"rb=$(stat -c %s \"$R\")\n");
PrintTo(D363Stream,"test \"$rb\" -gt 0 -a \"$rb\" -le 19000000 || fail receipt-size\n");
PrintTo(D363Stream,"rsha=$(sha256sum \"$R\" | awk '{print $1}')\n");
PrintTo(D363Stream,"test \"${#rsha}\" = 64 || fail receipt-sha-length\n");
PrintTo(D363Stream,"python3 - \"$R\" \"$pt\" '",D363P0SHA,"' '",
  D363P0Self,"' <<'PY'\n");
PrintTo(D363Stream,"import hashlib,json,sys\n");
PrintTo(D363Stream,"path,terminal,p0sha,p0self=sys.argv[1:]\n");
PrintTo(D363Stream,"raw=open(path,'rb').read()\n");
PrintTo(D363Stream,"canon=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')\n");
PrintTo(D363Stream,"sha=lambda b:hashlib.sha256(b).hexdigest()\n");
PrintTo(D363Stream,"def need(ok,label):\n");
PrintTo(D363Stream,"    if not ok: raise SystemExit(label)\n");
PrintTo(D363Stream,"def seal(value):\n");
PrintTo(D363Stream,"    body=dict(value); claimed=body.pop('self_digest_sha256',None)\n");
PrintTo(D363Stream,"    return isinstance(claimed,str) and len(claimed)==64 and claimed==sha(canon(body))\n");
PrintTo(D363Stream,"obj=json.loads(raw)\n");
PrintTo(D363Stream,"need(raw==canon(obj),'receipt canonical')\n");
PrintTo(D363Stream,"need(seal(obj),'receipt seal')\n");
PrintTo(D363Stream,"flags=('actual_a3_numerator','boundary_membership','cofinal_lift','exact_pb_endpoint_zero','fake','Ihara_witness','pointed_mu1','task192_consumed')\n");
PrintTo(D363Stream,"need(obj.get('schema')=='d972-r07-pre-a0-single-target-a3/v2/receipt/v1' and obj.get('status')==terminal and obj.get('terminal')==terminal and obj.get('accepted') is True,'receipt terminal')\n");
PrintTo(D363Stream,"need(terminal in ('",D363Member,"','",D363Nonmember,"') and all(obj.get(k) is False for k in flags),'receipt accepting vocabulary')\n");
PrintTo(D363Stream,"result=obj.get('result',{})\n");
PrintTo(D363Stream,"need(result.get('mode')=='PRE_A0_COMPUTATIONAL_BASE_ONLY' and result.get('correction_word_constructed') is False and result.get('task192_consumed') is False,'receipt mode')\n");
PrintTo(D363Stream,"need(result.get('false_conclusion_flags')=={k:False for k in flags},'receipt result flags')\n");
PrintTo(D363Stream,"need(result.get('authority',{}).get('p0')=={'path':'",D363P0,
  "','bytes':13748,'sha256':p0sha,'self_digest_sha256':p0self},'receipt P0')\n");
PrintTo(D363Stream,"interface=result.get('projected_a3_interface_v2',{}); consumer=result.get('task227_consumer_abi',{}); trace=result.get('projection_seal_trace',{})\n");
PrintTo(D363Stream,"need(seal(interface) and seal(consumer),'projection seals')\n");
PrintTo(D363Stream,"need(trace.get('projected_interface_body_sha256')==interface.get('self_digest_sha256') and trace.get('projected_interface_sealed_sha256')==sha(canon(interface)),'interface trace')\n");
PrintTo(D363Stream,"need(trace.get('task227_consumer_abi_body_sha256')==consumer.get('self_digest_sha256') and trace.get('task227_consumer_abi_sealed_sha256')==sha(canon(consumer)),'consumer trace')\n");
PrintTo(D363Stream,"internal='PROJECTED_MEMBER_SEED' if terminal=='",D363Member,"' else 'PROJECTED_NONMEMBER_DUAL'\n");
PrintTo(D363Stream,"gate=result.get('gate',{})\n");
PrintTo(D363Stream,"need(result.get('task227_terminal')==internal and gate.get('terminal')==internal and all(gate.get(k) is False for k in flags),'gate terminal')\n");
PrintTo(D363Stream,"need(result.get('post_call_exact_counts')=={'ideal_rows':486,'translates':729,'closure_calls':1} and result.get('ideal_486_count')==486 and result.get('translate_729_count')==729,'receipt counts')\n");
PrintTo(D363Stream,"meter=obj.get('resource_meter',{}); caps=meter.get('caps',{}); used=meter.get('used',{})\n");
PrintTo(D363Stream,"need(used.get('serialized_bytes')==len(raw) and caps.get('serialized_bytes')==20000000 and caps.get('wall_seconds')==1800 and caps.get('input_bytes')==60000000 and caps.get('rss_bytes')==4294967296,'receipt resource binding')\n");
PrintTo(D363Stream,"PY\n");
PrintTo(D363Stream,"rv=$?\n");
PrintTo(D363Stream,"test \"$rv\" = 0 || fail receipt-validation\n");
PrintTo(D363Stream,"timeout --signal=TERM --kill-after=30s 2100s python3 -u -B '",
  D363Checker,"' \"$R\" --verdict \"$V\" --receipt-sha256 \"$rsha\" >\"$CL\" 2>&1\n");
PrintTo(D363Stream,"cs=$?\n");
PrintTo(D363Stream,"cc=$(grep -Ec '^D363_CHECKER_TERMINAL (",D363Member,
  "|",D363Nonmember,"|",D363UnknownInput,"|",D363UnknownResource,
  ")$' \"$CL\" || true)\n");
PrintTo(D363Stream,"ca=$(grep -Ec '^D363_CHECKER_TERMINAL ' \"$CL\" || true)\n");
PrintTo(D363Stream,"test \"$cc\" = 1 -a \"$ca\" = 1 || unknown checker NO_EXACT_TERMINAL \"$cs\"\n");
PrintTo(D363Stream,"ct=$(sed -n 's/^D363_CHECKER_TERMINAL //p' \"$CL\")\n");
PrintTo(D363Stream,"case \"$ct\" in \"$UI\"|\"$UR\") unknown checker \"$ct\" \"$cs\";; \"$MEM\"|\"$NON\") test \"$cs\" = 0 || fail checker-status;; *) unknown checker BAD_TERMINAL \"$cs\";; esac\n");
PrintTo(D363Stream,"test \"$ct\" = \"$pt\" || fail terminal-mismatch\n");
PrintTo(D363Stream,"rsha2=$(sha256sum \"$R\" | awk '{print $1}')\n");
PrintTo(D363Stream,"test \"$rsha2\" = \"$rsha\" || fail receipt-rehash\n");
PrintTo(D363Stream,"test -f \"$V\" -a ! -L \"$V\" -a -s \"$V\" || fail verdict-owner\n");
PrintTo(D363Stream,"vb=$(stat -c %s \"$V\")\n");
PrintTo(D363Stream,"test \"$vb\" -gt 0 -a \"$vb\" -le 1000000 || fail verdict-size\n");
PrintTo(D363Stream,"python3 - \"$R\" \"$V\" \"$pt\" \"$rsha\" '",
  D363P0,"' '",D363P0SHA,"' '",D363P0Self,"' <<'PY'\n");
PrintTo(D363Stream,"import hashlib,json,sys\n");
PrintTo(D363Stream,"rpath,vpath,terminal,rsha,p0path,p0sha,p0self=sys.argv[1:]\n");
PrintTo(D363Stream,"rraw=open(rpath,'rb').read(); vraw=open(vpath,'rb').read(); p0raw=open(p0path,'rb').read()\n");
PrintTo(D363Stream,"canon=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')\n");
PrintTo(D363Stream,"sha=lambda b:hashlib.sha256(b).hexdigest()\n");
PrintTo(D363Stream,"def need(ok,label):\n");
PrintTo(D363Stream,"    if not ok: raise SystemExit(label)\n");
PrintTo(D363Stream,"def seal(value):\n");
PrintTo(D363Stream,"    body=dict(value); claimed=body.pop('self_digest_sha256',None)\n");
PrintTo(D363Stream,"    return isinstance(claimed,str) and len(claimed)==64 and claimed==sha(canon(body))\n");
PrintTo(D363Stream,"def collect(value,out):\n");
PrintTo(D363Stream,"    if isinstance(value,dict):\n");
PrintTo(D363Stream,"        if isinstance(value.get('path'),str) and type(value.get('bytes')) is int and isinstance(value.get('sha256'),str):\n");
PrintTo(D363Stream,"            row={'bytes':value['bytes'],'sha256':value['sha256']}; need(value['path'] not in out or out[value['path']]==row,'P0 pin conflict'); out[value['path']]=row\n");
PrintTo(D363Stream,"        for child in value.values(): collect(child,out)\n");
PrintTo(D363Stream,"    elif isinstance(value,list):\n");
PrintTo(D363Stream,"        for child in value: collect(child,out)\n");
PrintTo(D363Stream,"receipt=json.loads(rraw); verdict=json.loads(vraw); p0=json.loads(p0raw)\n");
PrintTo(D363Stream,"need(rraw==canon(receipt) and vraw==canon(verdict) and p0raw==canon(p0),'canonical owners')\n");
PrintTo(D363Stream,"need(sha(rraw)==rsha and sha(p0raw)==p0sha and seal(receipt) and seal(verdict) and seal(p0) and p0.get('self_digest_sha256')==p0self,'physical/seal owners')\n");
PrintTo(D363Stream,"flags=('actual_a3_numerator','boundary_membership','cofinal_lift','exact_pb_endpoint_zero','fake','Ihara_witness','pointed_mu1','task192_consumed')\n");
PrintTo(D363Stream,"need(verdict.get('schema')=='d972-r07-pre-a0-single-target-a3/v2/verdict/v1' and verdict.get('status')==terminal and verdict.get('terminal')==terminal and verdict.get('accepted') is True and verdict.get('independent') is True and verdict.get('reason') is None,'verdict acceptance')\n");
PrintTo(D363Stream,"need(all(verdict.get(k) is False for k in flags),'verdict flags')\n");
PrintTo(D363Stream,"need(verdict.get('receipt_path')==rpath and verdict.get('receipt_bytes')==len(rraw) and verdict.get('receipt_sha256')==rsha and verdict.get('receipt_self_digest_sha256')==receipt.get('self_digest_sha256'),'verdict receipt binding')\n");
PrintTo(D363Stream,"need(verdict.get('p0')=={'path':p0path,'bytes':len(p0raw),'sha256':p0sha,'self_digest_sha256':p0self},'verdict P0 binding')\n");
PrintTo(D363Stream,"expected={}; collect(p0.get('authority',{}),expected)\n");
PrintTo(D363Stream,"need(verdict.get('source_identities')==expected,'verdict authority identities')\n");
PrintTo(D363Stream,"result=receipt.get('result',{}); trace=result.get('projection_seal_trace',{})\n");
PrintTo(D363Stream,"for key in ('projected_interface_body_sha256','projected_interface_sealed_sha256','task227_consumer_abi_body_sha256','task227_consumer_abi_sealed_sha256'): need(verdict.get(key)==trace.get(key),'verdict projection '+key)\n");
PrintTo(D363Stream,"result_sha=sha(canon(result))\n");
PrintTo(D363Stream,"need(verdict.get('receipt_result_sha256')==result_sha and verdict.get('independently_reconstructed_result_sha256')==result_sha,'independent result digest')\n");
PrintTo(D363Stream,"need(verdict.get('task198_authority_sha256')==sha(canon(result['authority']['task198'])),'task198 verdict digest')\n");
PrintTo(D363Stream,"need(verdict.get('central_replay_sha256')==sha(canon(result['central_replay'])) and verdict.get('mutation_matrix_sha256')==sha(canon(result['mutation_controls']['rejected'])),'replay/mutation digests')\n");
PrintTo(D363Stream,"need(verdict.get('occurrence_rank')==result.get('rank') and verdict.get('block_rank')==result.get('block_rank') and verdict.get('task227_terminal')==result.get('task227_terminal'),'rank/terminal binding')\n");
PrintTo(D363Stream,"need(verdict.get('post_call_exact_counts')=={'ideal_rows':486,'translates':729,'independent_verify_calls':1,'frozen_internal_span_comparison_calls':12,'wrapper_reversed_span_calls':0},'verdict exact counts')\n");
PrintTo(D363Stream,"meter=verdict.get('resource_meter',{}); need(meter.get('used',{}).get('serialized_bytes')==len(vraw) and meter.get('caps',{}).get('serialized_bytes')==20000000 and meter.get('caps',{}).get('wall_seconds')==1800,'verdict resource binding')\n");
PrintTo(D363Stream,"PY\n");
PrintTo(D363Stream,"vv=$?\n");
PrintTo(D363Stream,"test \"$vv\" = 0 || fail verdict-validation\n");
PrintTo(D363Stream,"rsha3=$(sha256sum \"$R\" | awk '{print $1}')\n");
PrintTo(D363Stream,"test \"$rsha3\" = \"$rsha\" || fail final-receipt-rehash\n");
PrintTo(D363Stream,"vsha=$(sha256sum \"$V\" | awk '{print $1}')\n");
PrintTo(D363Stream,"test \"${#vsha}\" = 64 || fail verdict-sha-length\n");
PrintTo(D363Stream,"printf '%s' 'D363_V2_ACCEPTED' >\"$OK\" || fail sentinel-publication\n");
CloseStream(D363Stream);;
Exec(Concatenation("bash -- ",D363Shell));
D363Observed:=StringFile(D363Sentinel);;
if D363Observed<>"D363_V2_ACCEPTED" then
  Error("task363: serial accepting-only driver did not accept"); fi;
Print("D363_DRIVER_ACCEPTED mode=",D363Mode,"\n");
