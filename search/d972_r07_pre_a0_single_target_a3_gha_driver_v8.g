D363Mode:="gha";;
D363Bash:="/usr/bin/bash";;
D363P0:="ci/in/d972_r07_pre_a0_single_target_a3_v4.prereg.v1.json";;
D363Producer:="search/d972_r07_pre_a0_single_target_a3_v6.py";;
D363Checker:="crosscheck/check_d972_r07_pre_a0_single_target_a3_v6.py";;
D363Receipt:="ci/out/d972_r07_pre_a0_single_target_a3_v6.json";;
D363Verdict:="ci/out/d972_r07_pre_a0_single_target_a3_v6.verdict.json";;
D363ProducerLog:="ci/out/d972_r07_pre_a0_single_target_a3_v6.producer.log";;
D363CheckerLog:="ci/out/d972_r07_pre_a0_single_target_a3_v6.checker.log";;
D363Shell:="ci/out/d972_r07_pre_a0_single_target_a3_v6.driver.sh";;
D363Sentinel:="ci/out/d972_r07_pre_a0_single_target_a3_v6.driver.accepted";;
D363Member:="R07_PRE_A0_A3_PROJECTED_MEMBER";;
D363Nonmember:="R07_PRE_A0_A3_PROJECTED_NONMEMBER_DUAL";;
D363UnknownInput:="UNKNOWN_INPUT";;
D363UnknownResource:="UNKNOWN_RESOURCE";;
D363P0Bytes:=16417;;
D363P0SHA:="14ea6de8efac73e71854f6566a9202eb89164ab6b7b5940954e87b3af21ee8ae";;
D363P0Self:="f1991fa0c232e1d7ea95a211498b4d1741c2104b22271fb90ec1a7ee3af98be7";;
D363Pins:=[
  [D363P0,D363P0SHA,D363P0Bytes],
  [D363Producer,"a393e512d2f50ae8d622be9ad488a5fbaf47729981da13177acd013a831140e2",107641],
  [D363Checker,"c38dfc6f392e3595d0ff00001ba19453b7a9022643ef1c9f06862d6f37934ab8",120097]
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
  Error("A3/v8: malformed P0 self seal"); fi;
if not IsExistingFile(D363Bash) or not IsExecutableFile(D363Bash) then
  Error("A3/v8: exact /usr/bin/bash is not executable"); fi;

D363Read:=function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("A3/v8: missing ",label); fi;
  return raw;
end;;

D363Pin:=function(row)
  local raw;
  if not D363Hex64(row[2]) or not IsInt(row[3]) or row[3]<=0 then
    Error("A3/v8: malformed full pin ",row[1]); fi;
  raw:=D363Read(row[1],"pinned final owner");;
  if Length(raw)<>row[3] or HexSHA256(raw)<>row[2] then
    Error("A3/v8: pin drift ",row[1]); fi;
end;;

for D363PinRow in D363Pins do D363Pin(D363PinRow);; od;
for D363Path in [D363Receipt,D363Verdict,D363ProducerLog,D363CheckerLog,
                 D363Shell,D363Sentinel] do
  if IsExistingFile(D363Path) then
    Error("A3/v8: stale output ",D363Path); fi;
od;
if not IsDirectoryPath("ci/out") then
  if CreateDir("ci/out")=fail then Error("A3/v8: cannot create ci/out"); fi;
fi;
if not IsDirectoryPath("ci/out") then
  Error("A3/v8: ci/out is not a directory"); fi;

D363Stream:=OutputTextFile(D363Shell,false);;
if D363Stream=fail then Error("A3/v8: cannot open command script"); fi;
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
PrintTo(D363Stream,"dump_unknown_receipt(){ printf 'D363_DRIVER_UNKNOWN_RECEIPT tail_bytes_max=65536\\n' >&2; if test -f \"$R\" -a ! -L \"$R\"; then tail -c 65536 -- \"$R\" >&2 || printf 'D363_DRIVER_UNKNOWN_RECEIPT_UNAVAILABLE\\n' >&2; printf '\\n' >&2; else printf 'D363_DRIVER_UNKNOWN_RECEIPT_MISSING\\n' >&2; fi; }\n");
PrintTo(D363Stream,"unknown(){ printf 'D363_DRIVER_UNKNOWN side=%s terminal=%s process_status=%s\\n' \"$1\" \"$2\" \"$3\"; test ! -f \"$PL\" || cat \"$PL\"; test ! -f \"$CL\" || cat \"$CL\"; dump_unknown_receipt; exit 41; }\n");
PrintTo(D363Stream,"dump_nonzero(){ local ds=\"$1\" dl=\"$2\" side=\"$3\"; test \"$ds\" = 0 && return 0; printf 'D363_DRIVER_NONZERO_LOG side=%s process_status=%s tail_bytes_max=65536\\n' \"$side\" \"$ds\" >&2; if test -f \"$dl\" -a ! -L \"$dl\"; then tail -c 65536 -- \"$dl\" >&2 || printf 'D363_DRIVER_NONZERO_LOG_UNAVAILABLE side=%s\\n' \"$side\" >&2; else printf 'D363_DRIVER_NONZERO_LOG_MISSING side=%s\\n' \"$side\" >&2; fi; return \"$ds\"; }\n");
PrintTo(D363Stream,"printf 'D363_GHA_ESTIMATE five_case_reference_seconds=493 one_case_side_estimate_seconds=300 internal_seconds=1800 external_seconds=2100 serial_external_seconds=4200 workflow_seconds=21600\\n'\n");
PrintTo(D363Stream,"compgen -G 'ci/out/.d972_r07_pre_a0_single_target_a3_v6.json.tmp.*' >/dev/null && fail stale-receipt-temp\n");
PrintTo(D363Stream,"compgen -G 'ci/out/.d972_r07_pre_a0_single_target_a3_v6.verdict.json.tmp.*' >/dev/null && fail stale-verdict-temp\n");
PrintTo(D363Stream,"timeout --signal=TERM --kill-after=30s 2100s python3 -u -B '",
  D363Producer,"' --output \"$R\" >\"$PL\" 2>&1\n");
PrintTo(D363Stream,"ps=$?\n");
PrintTo(D363Stream,"dump_nonzero \"$ps\" \"$PL\" producer\n");
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
PrintTo(D363Stream,"timeout --signal=TERM --kill-after=30s 2100s python3 -u -B '",
  D363Checker,"' \"$R\" --verdict \"$V\" --receipt-sha256 \"$rsha\" >\"$CL\" 2>&1\n");
PrintTo(D363Stream,"cs=$?\n");
PrintTo(D363Stream,"dump_nonzero \"$cs\" \"$CL\" checker\n");
PrintTo(D363Stream,"cc=$(grep -Ec '^D363_CHECKER_TERMINAL (",D363Member,
  "|",D363Nonmember,"|",D363UnknownInput,"|",D363UnknownResource,
  ")$' \"$CL\" || true)\n");
PrintTo(D363Stream,"ca=$(grep -Ec '^D363_CHECKER_TERMINAL ' \"$CL\" || true)\n");
PrintTo(D363Stream,"test \"$cc\" = 1 -a \"$ca\" = 1 || unknown checker NO_EXACT_TERMINAL \"$cs\"\n");
PrintTo(D363Stream,"ct=$(sed -n 's/^D363_CHECKER_TERMINAL //p' \"$CL\")\n");
PrintTo(D363Stream,"case \"$ct\" in \"$UI\"|\"$UR\") unknown checker \"$ct\" \"$cs\";; \"$MEM\"|\"$NON\") test \"$cs\" = 0 || fail checker-status;; *) unknown checker BAD_TERMINAL \"$cs\";; esac\n");
PrintTo(D363Stream,"test \"$ct\" = \"$pt\" || fail terminal-mismatch\n");
PrintTo(D363Stream,"test -f \"$V\" -a ! -L \"$V\" -a -s \"$V\" || fail verdict-owner\n");
PrintTo(D363Stream,"vb=$(stat -c %s \"$V\")\n");
PrintTo(D363Stream,"test \"$vb\" -gt 0 -a \"$vb\" -le 1000000 || fail verdict-size\n");
PrintTo(D363Stream,"vsha=$(sha256sum \"$V\" | awk '{print $1}')\n");
PrintTo(D363Stream,"test \"${#vsha}\" = 64 || fail verdict-sha-length\n");
PrintTo(D363Stream,"python3 - \"$R\" \"$V\" \"$pt\" \"$rsha\" \"$vsha\" '",
  D363P0,"' '",D363P0SHA,"' '",D363P0Self,"' <<'PY'\n");
PrintTo(D363Stream,"import hashlib,json,os,stat,sys\n");
PrintTo(D363Stream,"rpath,vpath,terminal,rsha,vsha,p0path,p0sha,p0self=sys.argv[1:]\n");
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
PrintTo(D363Stream,"        if 'path' in value:\n");
PrintTo(D363Stream,"            need(type(value.get('path')) is str and type(value.get('bytes')) is int and value['bytes']>=0 and isinstance(value.get('sha256'),str) and len(value['sha256'])==64 and all(c in '0123456789abcdef' for c in value['sha256']),'malformed authority owner')\n");
PrintTo(D363Stream,"            out.append((value['path'],value['bytes'],value['sha256'])); return\n");
PrintTo(D363Stream,"        for child in value.values(): collect(child,out)\n");
PrintTo(D363Stream,"    elif isinstance(value,list):\n");
PrintTo(D363Stream,"        for child in value: collect(child,out)\n");
PrintTo(D363Stream,"receipt=json.loads(rraw); verdict=json.loads(vraw); p0=json.loads(p0raw)\n");
PrintTo(D363Stream,"need(rraw==canon(receipt) and vraw==canon(verdict) and p0raw==canon(p0),'canonical owners')\n");
PrintTo(D363Stream,"need(sha(rraw)==rsha and sha(vraw)==vsha and sha(p0raw)==p0sha and seal(receipt) and seal(verdict) and seal(p0) and p0.get('self_digest_sha256')==p0self,'physical/seal owners')\n");
PrintTo(D363Stream,"flags=('actual_a3_numerator','boundary_membership','cofinal_lift','exact_pb_endpoint_zero','fake','Ihara_witness','pointed_mu1','task192_consumed')\n");
PrintTo(D363Stream,"need(verdict.get('schema')=='d972-r07-pre-a0-single-target-a3/v6/verdict/v1' and verdict.get('status')==terminal and verdict.get('terminal')==terminal and verdict.get('accepted') is True and verdict.get('independent') is True and verdict.get('reason') is None,'verdict acceptance')\n");
PrintTo(D363Stream,"need(all(verdict.get(k) is False for k in flags),'verdict flags')\n");
PrintTo(D363Stream,"need(verdict.get('receipt_path')==rpath and verdict.get('receipt_bytes')==len(rraw) and verdict.get('receipt_sha256')==rsha and verdict.get('receipt_self_digest_sha256')==receipt.get('self_digest_sha256'),'verdict receipt binding')\n");
PrintTo(D363Stream,"need(verdict.get('p0')=={'path':p0path,'bytes':len(p0raw),'sha256':p0sha,'self_digest_sha256':p0self},'verdict P0 binding')\n");
PrintTo(D363Stream,"owners=[]; collect(p0.get('authority',{}),owners); inventory=p0.get('authority_inventory',{}); paths=[row[0] for row in owners]\n");
PrintTo(D363Stream,"need(len(paths)==len(set(paths)) and sorted(paths)==inventory.get('owner_paths') and len(owners)==inventory.get('unique_owner_count') and sum(row[1] for row in owners)==inventory.get('unique_owner_bytes'),'authority inventory')\n");
PrintTo(D363Stream,"for path,size,digest in owners:\n");
PrintTo(D363Stream,"    info=os.lstat(path); need(stat.S_ISREG(info.st_mode) and not stat.S_ISLNK(info.st_mode) and info.st_size==size,'authority physical owner '+path)\n");
PrintTo(D363Stream,"    with open(path,'rb') as stream: physical=stream.read()\n");
PrintTo(D363Stream,"    need(len(physical)==size and sha(physical)==digest,'authority physical digest '+path)\n");
PrintTo(D363Stream,"expected={path:{'bytes':size,'sha256':digest} for path,size,digest in owners}\n");
PrintTo(D363Stream,"need(verdict.get('source_identities')==expected,'verdict authority identities')\n");
PrintTo(D363Stream,"result=receipt.get('result',{}); trace=result.get('projection_seal_trace',{})\n");
PrintTo(D363Stream,"for key in ('projected_interface_body_sha256','projected_interface_sealed_sha256','task227_consumer_abi_body_sha256','task227_consumer_abi_sealed_sha256'): need(verdict.get(key)==trace.get(key),'verdict projection '+key)\n");
PrintTo(D363Stream,"result_sha=sha(canon(result))\n");
PrintTo(D363Stream,"need(verdict.get('receipt_result_sha256')==result_sha and verdict.get('independently_reconstructed_result_sha256')==result_sha,'independent result digest')\n");
PrintTo(D363Stream,"need(verdict.get('task198_authority_sha256')==sha(canon(result['authority']['task198'])),'task198 verdict digest')\n");
PrintTo(D363Stream,"iev=verdict.get('independent_task198_evaluator',{}); need(iev.get('direct_call_counts')=={'action':1,'eval':3,'inverse':2,'multiply':1,'section_cocycle':1,'source_section':1} and iev.get('actual_transitive_call_counts')=={'action':1,'eval':8,'inverse':3,'multiply':4,'section_cocycle':1,'source_section':1} and iev.get('direct_values')==result['task198_evaluator_exercise']['direct_values'] and iev.get('direct_values_sha256')==sha(canon(iev['direct_values'])),'independent evaluator verdict')\n");
PrintTo(D363Stream,"need(verdict.get('central_replay_sha256')==sha(canon(result['central_replay'])) and verdict.get('mutation_matrix_sha256')==sha(canon(result['mutation_controls']['rejected'])),'replay/mutation digests')\n");
PrintTo(D363Stream,"need(verdict.get('occurrence_rank')==result.get('rank') and verdict.get('block_rank')==result.get('block_rank') and verdict.get('task227_terminal')==result.get('task227_terminal'),'rank/terminal binding')\n");
PrintTo(D363Stream,"need(verdict.get('post_call_exact_counts')=={'ideal_rows':486,'translates':729,'independent_verify_calls':1,'frozen_internal_span_comparison_calls':12,'wrapper_reversed_span_calls':0},'verdict exact counts')\n");
PrintTo(D363Stream,"meter=verdict.get('resource_meter',{}); vu=meter.get('used',{}); need(vu.get('serialized_bytes')==len(vraw) and vu.get('dynamic_imports')==7 and vu.get('area_builds')==3 and vu.get('evaluator_builds')==1 and vu.get('evaluator_calls')==9 and vu.get('evaluator_support')==11 and vu.get('independent_verify_calls')==1 and vu.get('serialization_peak_bytes')==3065536 and meter.get('caps',{}).get('serialized_bytes')==20000000 and meter.get('caps',{}).get('wall_seconds')==1800,'verdict resource binding')\n");
PrintTo(D363Stream,"PY\n");
PrintTo(D363Stream,"vv=$?\n");
PrintTo(D363Stream,"test \"$vv\" = 0 || fail verdict-validation\n");
PrintTo(D363Stream,"rsha3=$(sha256sum \"$R\" | awk '{print $1}')\n");
PrintTo(D363Stream,"test \"$rsha3\" = \"$rsha\" || fail final-receipt-rehash\n");
PrintTo(D363Stream,"vsha2=$(sha256sum \"$V\" | awk '{print $1}')\n");
PrintTo(D363Stream,"test \"$vsha2\" = \"$vsha\" || fail verdict-rehash\n");
PrintTo(D363Stream,"python3 - \"$OK\" <<'PY'\n");
PrintTo(D363Stream,"import os,stat,sys\n");
PrintTo(D363Stream,"path=sys.argv[1]; parent,name=os.path.split(path)\n");
PrintTo(D363Stream,"rootfd=cifd=dfd=fd=rfd=-1\n");
PrintTo(D363Stream,"created=False; original=[]; rollback=[]; rollback_attempted=False\n");
PrintTo(D363Stream,"def retain(bucket,phase,exc):\n");
PrintTo(D363Stream,"    bucket.append((phase,type(exc).__name__,repr(exc)))\n");
PrintTo(D363Stream,"flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW\n");
PrintTo(D363Stream,"try:\n");
PrintTo(D363Stream,"    if parent!='ci/out' or '/' in name or name in ('','.','..'): raise ValueError('sentinel path envelope')\n");
PrintTo(D363Stream,"    rootfd=os.open('.',flags)\n");
PrintTo(D363Stream,"    cifd=os.open('ci',flags,dir_fd=rootfd); dfd=os.open('out',flags,dir_fd=cifd)\n");
PrintTo(D363Stream,"    fd=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=dfd)\n");
PrintTo(D363Stream,"    created=True\n");
PrintTo(D363Stream,"    raw=b'D363_V6_ACCEPTED'; offset=0\n");
PrintTo(D363Stream,"    while offset<len(raw):\n");
PrintTo(D363Stream,"        written=os.write(fd,raw[offset:])\n");
PrintTo(D363Stream,"        if not isinstance(written,int) or written<=0: raise OSError('short sentinel write')\n");
PrintTo(D363Stream,"        offset+=written\n");
PrintTo(D363Stream,"    os.fsync(fd)\n");
PrintTo(D363Stream,"    made=os.fstat(fd)\n");
PrintTo(D363Stream,"    if not stat.S_ISREG(made.st_mode) or made.st_size!=len(raw): raise OSError('sentinel creation identity')\n");
PrintTo(D363Stream,"    os.close(fd); fd=-1\n");
PrintTo(D363Stream,"    os.fsync(dfd)\n");
PrintTo(D363Stream,"    rfd=os.open(name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=dfd)\n");
PrintTo(D363Stream,"    observed=os.fstat(rfd)\n");
PrintTo(D363Stream,"    if not stat.S_ISREG(observed.st_mode) or not os.path.samestat(made,observed) or observed.st_size!=len(raw): raise OSError('sentinel identity changed')\n");
PrintTo(D363Stream,"    readback=os.read(rfd,len(raw)); eof=os.read(rfd,1)\n");
PrintTo(D363Stream,"    if readback!=raw or eof!=b'': raise OSError('nonexact sentinel readback')\n");
PrintTo(D363Stream,"    os.close(rfd); rfd=-1\n");
PrintTo(D363Stream,"except BaseException as exc:\n");
PrintTo(D363Stream,"    retain(original,'publication-or-admission',exc)\n");
PrintTo(D363Stream,"if rfd>=0:\n");
PrintTo(D363Stream,"    try: os.close(rfd)\n");
PrintTo(D363Stream,"    except BaseException as exc: retain(rollback if original else original,'read-fd-close',exc)\n");
PrintTo(D363Stream,"    rfd=-1\n");
PrintTo(D363Stream,"if fd>=0:\n");
PrintTo(D363Stream,"    try: os.close(fd)\n");
PrintTo(D363Stream,"    except BaseException as exc: retain(rollback if original else original,'file-fd-close',exc)\n");
PrintTo(D363Stream,"    fd=-1\n");
PrintTo(D363Stream,"if rootfd>=0:\n");
PrintTo(D363Stream,"    try: os.close(rootfd)\n");
PrintTo(D363Stream,"    except BaseException as exc: retain(rollback if original else original,'root-fd-close',exc)\n");
PrintTo(D363Stream,"    rootfd=-1\n");
PrintTo(D363Stream,"if cifd>=0:\n");
PrintTo(D363Stream,"    try: os.close(cifd)\n");
PrintTo(D363Stream,"    except BaseException as exc: retain(rollback if original else original,'ci-fd-close',exc)\n");
PrintTo(D363Stream,"    cifd=-1\n");
PrintTo(D363Stream,"if original and created:\n");
PrintTo(D363Stream,"    rollback_attempted=True\n");
PrintTo(D363Stream,"    try: os.unlink(name,dir_fd=dfd)\n");
PrintTo(D363Stream,"    except FileNotFoundError: pass\n");
PrintTo(D363Stream,"    except BaseException as exc: retain(rollback,'sentinel-unlink',exc)\n");
PrintTo(D363Stream,"    try: os.fsync(dfd)\n");
PrintTo(D363Stream,"    except BaseException as exc: retain(rollback,'out-fd-fsync-after-unlink-or-absent',exc)\n");
PrintTo(D363Stream,"if dfd>=0:\n");
PrintTo(D363Stream,"    try:\n");
PrintTo(D363Stream,"        os.close(dfd); dfd=-1\n");
PrintTo(D363Stream,"    except BaseException as exc:\n");
PrintTo(D363Stream,"        retain(rollback if original else original,'out-fd-close',exc)\n");
PrintTo(D363Stream,"        if created and not rollback_attempted:\n");
PrintTo(D363Stream,"            rollback_attempted=True\n");
PrintTo(D363Stream,"            try: os.unlink(name,dir_fd=dfd)\n");
PrintTo(D363Stream,"            except FileNotFoundError: pass\n");
PrintTo(D363Stream,"            except BaseException as cleanup: retain(rollback,'sentinel-unlink-after-out-close',cleanup)\n");
PrintTo(D363Stream,"            try: os.fsync(dfd)\n");
PrintTo(D363Stream,"            except BaseException as cleanup: retain(rollback,'out-fd-fsync-after-out-close',cleanup)\n");
PrintTo(D363Stream,"        try: os.close(dfd)\n");
PrintTo(D363Stream,"        except BaseException as cleanup: retain(rollback,'out-fd-reclose',cleanup)\n");
PrintTo(D363Stream,"        dfd=-1\n");
PrintTo(D363Stream,"if original or rollback:\n");
PrintTo(D363Stream,"    try:\n");
PrintTo(D363Stream,"        for kind,rows in (('ORIGINAL',original),('ROLLBACK',rollback)):\n");
PrintTo(D363Stream,"            for phase,error_type,detail in rows:\n");
PrintTo(D363Stream,"                print('D363_SENTINEL_%s phase=%s type=%s detail=%s' % (kind,phase,error_type,detail),file=sys.stderr,flush=True)\n");
PrintTo(D363Stream,"    except BaseException as exc:\n");
PrintTo(D363Stream,"        retain(rollback,'diagnostic-output',exc)\n");
PrintTo(D363Stream,"    raise SystemExit(70)\n");
PrintTo(D363Stream,"PY\n");
PrintTo(D363Stream,"test \"$?\" = 0 || fail sentinel-publication\n");
CloseStream(D363Stream);;
D363Status:=Process(DirectoryCurrent(),D363Bash,InputTextNone(),
  OutputTextUser(),["--",D363Shell]);;
if not (IsInt(D363Status) and D363Status=0) then
  Error("A3/v8: shell process status is not integer zero"); fi;
