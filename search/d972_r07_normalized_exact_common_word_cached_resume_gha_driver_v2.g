#############################################################################
## Task298 task192 sealed-checkpoint resume transport driver v2.
## ASCII only. This driver transports bytes; it does not alter the math engine.
#############################################################################
D298Driver:="search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g";;
D298Schema:="d972-r07-normalized-exact-cached-colgen/resume-transport/v2";;
D298Version:="task298-v2";;
D298Zip:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip";;
D298Manifest:="ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json";;
D298Member:="d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json";;
D298ResumeInput:="ci/resume/task192_run33149728601_checkpoint_v2.json";;
D298Producer:="search/d972_r07_normalized_exact_common_word_cached_v3.py";;
D298Checker:="crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py";;
D298SerialDriver:="search/d972_r07_normalized_exact_common_word_cached_gha_driver_v3.g";;
D298Receipt:="ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.json";;
D298Checkpoint:="ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.json.checkpoint.json";;
D298ProducerLog:="ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.producer.log";;
D298CheckerLog:="ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.checker.log";;
D298Shell:="ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.sh";;
D298OK:="ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.ok";;
D298ExtractMarker:=Concatenation(
  "TASK298_EXTRACT_PASS member=",D298Member,
  " bytes=86368039 sha256=c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab");;
D298Sentinel:="R07_TASK192_CHECKPOINT_RESUME_TRANSPORT_V2_SENTINEL";;
D298Common:="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD";;
D298ProducerTerminal:="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_PRODUCER_TERMINAL";;
D298CheckerPass:="R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_CHECKER_PASS";;

if not IsExistingFile(D298Driver) or
   D298Schema<>"d972-r07-normalized-exact-cached-colgen/resume-transport/v2" or
   D298Version<>"task298-v2" then
  Error("task298 driver path/schema/version identity");
fi;

D298Pins:=[
 [D298Zip,5001811,"f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566"],
 [D298Manifest,1328,"6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302"],
 [D298Producer,193704,"f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37"],
 [D298Checker,154009,"dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10"],
 [D298SerialDriver,11548,"2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d"]
];;

D298TerminalGrammar:=Concatenation(
 "(",D298Common,
 "|UNKNOWN_RESOURCE:(phase=(task175_reconstruction|fine_deletion|Q0_discovery|A_L_membership_scan|L_subgroup_closure|typed_singleton_equality|Q0_positive_shortlex_section):cap=(wall_seconds|rss_bytes)",
 "|phase=resume_rebuild:cap=(boundary_pairs|fibre_scans|candidate_words|retained_columns|global_roster|oracle_rounds)",
 "|phase=coarse_inverse_build:cap=(fibre_scans|wall_seconds|rss_bytes)",
 "|phase=positive_boundary_correlation:cap=(boundary_pairs|wall_seconds|rss_bytes)",
 "|phase=rank_increase:cap=(retained_columns|wall_seconds|rss_bytes)",
 "|phase=positive_correction_candidate:cap=(candidate_words|wall_seconds|rss_bytes)",
 "|phase=(weighted_eleven_occurrence_formula|weighted_support_fibre):cap=(wall_seconds|rss_bytes)",
 "|phase=weighted_global_prefix:cap=(global_roster|wall_seconds|rss_bytes)",
 "|phase=checkpoint_serialization:cap=checkpoint_bytes",
 "|phase=positive_global_fallback:cap=global_roster",
 "|phase=positive_correction_dovetail:cap=oracle_rounds):value=[0-9.]+:limit=[0-9.]+",
 "|UNKNOWN_INPUT:(module_not_uniquely_pinned|module_missing|module_pin|module_loader|missing|pin|task175:not_READY|resume:input_identity|resume:target|resume:normalized_semantics|resume:monitor_limits)(:[^[:cntrl:]]*)?)");;

D298Read:=function(path)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then Error("task298 missing ",path); fi;
  return raw;
end;;

D298Pin:=function(row)
  local raw;
  raw:=D298Read(row[1]);;
  if Length(raw)<>row[2] or HexSHA256(raw)<>row[3] then
    Error("task298 pin drift ",row[1]);
  fi;
end;;

D298Reject:=function(paths)
  local path;
  if Length(paths)<>Length(Set(paths)) then Error("task298 duplicate fresh path"); fi;
  for path in paths do
    if IsExistingFile(path) then Error("task298 stale output ",path); fi;
  od;
end;;

for D298Row in D298Pins do D298Pin(D298Row);; od;
D298Reject([D298ResumeInput,D298Receipt,D298Checkpoint,D298ProducerLog,
  D298CheckerLog,D298Shell,D298OK]);;

D298Stream:=OutputTextFile(D298Shell,false);;
if D298Stream=fail then Error("task298 shell open"); fi;
SetPrintFormattingStatus(D298Stream,false);;
PrintTo(D298Stream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");

## Guarded single-member extraction. No repository module is imported.
PrintTo(D298Stream,"if python3 - ",D298Zip," ",D298Manifest," ",D298ResumeInput,
  " > ",D298ProducerLog," 2>&1 <<'PY'\n");
PrintTo(D298Stream,"import hashlib\nimport json\nimport sys\nimport zipfile\n");
PrintTo(D298Stream,"from pathlib import Path, PurePosixPath\n\n");
PrintTo(D298Stream,"ZIP_PATH='",D298Zip,"'\n");
PrintTo(D298Stream,"MANIFEST_PATH='",D298Manifest,"'\n");
PrintTo(D298Stream,"OUTPUT_PATH='",D298ResumeInput,"'\n");
PrintTo(D298Stream,"MEMBER='",D298Member,"'\n");
PrintTo(D298Stream,"ZIP_BYTES=5001811\nZIP_SHA='f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566'\n");
PrintTo(D298Stream,"MANIFEST_BYTES=1328\nMANIFEST_SHA='6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302'\n");
PrintTo(D298Stream,"RAW_BYTES=86368039\nRAW_SHA='c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab'\n");
PrintTo(D298Stream,"expected={\n");
PrintTo(D298Stream," 'schema':'d972-r07-normalized-exact-cached-colgen/resume-input/v1',\n");
PrintTo(D298Stream," 'source_run_id':33149728601,\n");
PrintTo(D298Stream," 'source_head_sha':'7dd85c94c01e35e090917f9d11f9a7252a260523',\n");
PrintTo(D298Stream," 'source_artifact_id':9681838782,\n");
PrintTo(D298Stream," 'source_artifact_digest':'sha256:66ed561b0c19c22dd56ce6aaa1626159d8267788fa282d3f2cb72f33c36e6917',\n");
PrintTo(D298Stream," 'source_receipt':{'bytes':8759,'sha256':'955a6bebb442f6bbe111ffcb4c1eda732f8bbbe26292c4e5da451c69dbaf5dcc','terminal':'UNKNOWN_RESOURCE:phase=positive_boundary_correlation:cap=wall_seconds:value=10801.537010798002:limit=10800.0'},\n");
PrintTo(D298Stream," 'zip':{'path':ZIP_PATH,'bytes':ZIP_BYTES,'sha256':ZIP_SHA,'member':MEMBER},\n");
PrintTo(D298Stream," 'raw_checkpoint':{'bytes':RAW_BYTES,'sha256':RAW_SHA},\n");
PrintTo(D298Stream," 'progress':{'phase':'positive_boundary_correlation','boundary_pairs':3145728,'retained_columns':2896,'candidate_words':0},\n");
PrintTo(D298Stream," 'claims':{'common_word':False,'separator':False,'finite_common_word':False,'cofinal_lift':False,'fake':False,'ihara_witness':False}\n");
PrintTo(D298Stream,"}\n");
PrintTo(D298Stream,"def reject(reason):\n raise SystemExit('TASK298_EXTRACT_REJECT:'+reason)\n");
PrintTo(D298Stream,"def sha(raw):\n return hashlib.sha256(raw).hexdigest()\n");
PrintTo(D298Stream,"if len(sys.argv)!=4: reject('argv')\n");
PrintTo(D298Stream,"zip_arg,manifest_arg,output_arg=map(Path,sys.argv[1:])\n");
PrintTo(D298Stream,"if zip_arg.as_posix()!=ZIP_PATH or manifest_arg.as_posix()!=MANIFEST_PATH or output_arg.as_posix()!=OUTPUT_PATH: reject('fixed_paths')\n");
PrintTo(D298Stream,"if any(path.is_absolute() or '..' in path.parts for path in (zip_arg,manifest_arg,output_arg)): reject('path_traversal')\n");
PrintTo(D298Stream,"root=Path.cwd().resolve()\ntarget=(root/output_arg).resolve()\nresume_root=(root/'ci'/'resume').resolve()\n");
PrintTo(D298Stream,"if target.parent!=resume_root or target.name!='task192_run33149728601_checkpoint_v2.json': reject('output_boundary')\n");
PrintTo(D298Stream,"if target.exists(): reject('stale_output')\n");
PrintTo(D298Stream,"zip_raw=zip_arg.read_bytes()\nmanifest_raw=manifest_arg.read_bytes()\n");
PrintTo(D298Stream,"if len(zip_raw)!=ZIP_BYTES or sha(zip_raw)!=ZIP_SHA: reject('zip_identity')\n");
PrintTo(D298Stream,"if len(manifest_raw)!=MANIFEST_BYTES or sha(manifest_raw)!=MANIFEST_SHA: reject('manifest_identity')\n");
PrintTo(D298Stream,"try:\n manifest=json.loads(manifest_raw.decode('utf-8'))\nexcept (UnicodeError,json.JSONDecodeError):\n reject('manifest_json')\n");
PrintTo(D298Stream,"if manifest!=expected: reject('manifest_contract')\n");
PrintTo(D298Stream,"member_path=PurePosixPath(MEMBER)\n");
PrintTo(D298Stream,"if member_path.is_absolute() or '..' in member_path.parts or len(member_path.parts)!=1: reject('member_path')\n");
PrintTo(D298Stream,"try:\n");
PrintTo(D298Stream," with zipfile.ZipFile(zip_arg,'r') as archive:\n");
PrintTo(D298Stream,"  infos=archive.infolist()\n");
PrintTo(D298Stream,"  if archive.namelist()!=[MEMBER] or len(infos)!=1: reject('namelist')\n");
PrintTo(D298Stream,"  info=infos[0]\n");
PrintTo(D298Stream,"  if info.filename!=MEMBER or info.is_dir() or info.file_size!=RAW_BYTES: reject('member_metadata')\n");
PrintTo(D298Stream,"  raw=archive.read(info)\n");
PrintTo(D298Stream,"except (OSError,zipfile.BadZipFile,RuntimeError,KeyError):\n reject('zip_read')\n");
PrintTo(D298Stream,"if len(raw)!=RAW_BYTES or sha(raw)!=RAW_SHA: reject('raw_identity')\n");
PrintTo(D298Stream,"try:\n checkpoint=json.loads(raw.decode('utf-8'))\nexcept (UnicodeError,json.JSONDecodeError):\n reject('raw_json')\n");
PrintTo(D298Stream,"EXPECTED_LIMITS={\n");
PrintTo(D298Stream," 'boundary_pairs':8000000,'candidate_words':2000000,\n");
PrintTo(D298Stream," 'checkpoint_bytes':4000000000,'fibre_scans':80000000,\n");
PrintTo(D298Stream," 'global_roster':357128352,'oracle_rounds':1,\n");
PrintTo(D298Stream," 'retained_columns':250000,'rss_bytes':5700000000,\n");
PrintTo(D298Stream," 'wall_seconds':10800.0}\n");
PrintTo(D298Stream,"EXPECTED_COUNTERS={\n");
PrintTo(D298Stream," 'boundary_pairs':3145728,'candidate_words':0,\n");
PrintTo(D298Stream," 'checkpoint_bytes':86367576,'fibre_scans':0,\n");
PrintTo(D298Stream," 'global_roster':0,'oracle_rounds':0,'retained_columns':2896}\n");
PrintTo(D298Stream,"DUAL_SHA='0960259714fa94ddd89e2ac4f582f040942ab7bd258185c0448c133e50b00f0c'\n");
PrintTo(D298Stream,"EXPECTED_PROGRESS={\n");
PrintTo(D298Stream," 'boundary':{'complete':False,'dual_sha256':DUAL_SHA,'pair_attempts':3145088,'restart_pair_cursor':0},\n");
PrintTo(D298Stream," 'correction':{'canonical_row_cursor':0,'dual_sha256':DUAL_SHA,'global_cursors':{},'kernel_prefix':0,'live_fibre_count':0,'live_fibres':[],'weighted_rows':{}}}\n");
PrintTo(D298Stream,"EXPECTED_CHUNK={\n");
PrintTo(D298Stream," 'attempts_done':0,\n");
PrintTo(D298Stream," 'canonical_ordering':['roster_index','target_coordinate','target_blob','kernel_index','global_cursor','column_id'],\n");
PrintTo(D298Stream," 'canonical_row_cursor':0,'chunk_complete':True,'chunk_end':0,'chunk_start':0,'max_attempts':256,\n");
PrintTo(D298Stream," 'repeated_suffix':{'attempts':0,'declared':False,'interrupted_end':0,'max_attempts':256,'replay_on_resume':True,'safe_start':0}}\n");
PrintTo(D298Stream,"monitor=checkpoint.get('monitor')\n");
PrintTo(D298Stream,"if not isinstance(monitor,dict) or set(monitor)!={'counters','elapsed_seconds','limits','phase','rss_bytes','single_process'}: reject('monitor_shape')\n");
PrintTo(D298Stream,"limits=monitor.get('limits')\ncounters=monitor.get('counters')\n");
PrintTo(D298Stream,"if limits!=EXPECTED_LIMITS or type(limits.get('wall_seconds')) is not float or any(type(limits.get(name)) is not int for name in EXPECTED_LIMITS if name!='wall_seconds'): reject('monitor_limits')\n");
PrintTo(D298Stream,"if counters!=EXPECTED_COUNTERS or any(type(counters.get(name)) is not int for name in EXPECTED_COUNTERS): reject('monitor_counters')\n");
PrintTo(D298Stream,"if monitor.get('phase')!='positive_boundary_correlation' or monitor.get('single_process') is not True: reject('monitor_state')\n");
PrintTo(D298Stream,"if type(monitor.get('elapsed_seconds')) is not float or monitor['elapsed_seconds']!=10802.377323564: reject('monitor_elapsed')\n");
PrintTo(D298Stream,"if type(monitor.get('rss_bytes')) is not int or monitor['rss_bytes']!=2505383936: reject('monitor_rss')\n");
PrintTo(D298Stream,"progress=checkpoint.get('progress')\n");
PrintTo(D298Stream,"if progress!=EXPECTED_PROGRESS: reject('progress_contract')\n");
PrintTo(D298Stream,"if checkpoint.get('v3_chunk')!=EXPECTED_CHUNK: reject('chunk_contract')\n");
PrintTo(D298Stream,"manifest_progress=manifest['progress']\n");
PrintTo(D298Stream,"if monitor['phase']!=manifest_progress['phase'] or counters['boundary_pairs']!=manifest_progress['boundary_pairs'] or counters['retained_columns']!=manifest_progress['retained_columns'] or counters['candidate_words']!=manifest_progress['candidate_words']: reject('manifest_monitor_binding')\n");
PrintTo(D298Stream,"columns=checkpoint.get('columns')\nrank=checkpoint.get('rank')\n");
PrintTo(D298Stream,"if not isinstance(columns,list) or type(rank) is not int or rank!=len(columns) or rank!=counters['retained_columns']: reject('rank_counter_binding')\n");
PrintTo(D298Stream,"boundary=progress['boundary']\ncorrection=progress['correction']\nchunk=checkpoint['v3_chunk']\n");
PrintTo(D298Stream,"if counters['boundary_pairs']-boundary['pair_attempts']!=640 or counters['checkpoint_bytes']>RAW_BYTES: reject('counter_progress_binding')\n");
PrintTo(D298Stream,"if chunk['canonical_row_cursor']!=correction['canonical_row_cursor'] or chunk['chunk_end']!=chunk['chunk_start']: reject('chunk_progress_binding')\n");
PrintTo(D298Stream,"current_dual=checkpoint.get('current_dual_sha256')\nepoch=checkpoint.get('v3_epoch')\n");
PrintTo(D298Stream,"if current_dual!=DUAL_SHA or boundary['dual_sha256']!=current_dual or correction['dual_sha256']!=current_dual: reject('progress_dual_binding')\n");
PrintTo(D298Stream,"if not isinstance(epoch,dict) or epoch.get('dual_sha256')!=current_dual or epoch.get('dual_progress_sha256')!=current_dual: reject('epoch_dual_binding')\n");
PrintTo(D298Stream,"if not monitor['elapsed_seconds']>limits['wall_seconds']: reject('source_wall_stop_binding')\n");
PrintTo(D298Stream,"if 'resume_monitor_history' in checkpoint or 'resume_rebuild' in checkpoint: reject('already_resumed')\n");
PrintTo(D298Stream,"target.parent.mkdir(parents=True,exist_ok=True)\n");
PrintTo(D298Stream,"try:\n with target.open('xb') as stream:\n  stream.write(raw)\nexcept FileExistsError:\n reject('stale_race')\n");
PrintTo(D298Stream,"written=target.read_bytes()\n");
PrintTo(D298Stream,"if len(written)!=RAW_BYTES or sha(written)!=RAW_SHA: reject('written_identity')\n");
PrintTo(D298Stream,"print('TASK298_EXTRACT_PASS member='+MEMBER+' bytes='+str(RAW_BYTES)+' sha256='+RAW_SHA)\n");
PrintTo(D298Stream,"PY\nthen\n  :\nelse\n  cat ",D298ProducerLog,"\n  exit 1\nfi\n");
PrintTo(D298Stream,"grep -Fxc '",D298ExtractMarker,"' ",D298ProducerLog," | grep -qx 1\n");

## Resume the existing producer with the exact commissioned monitor limits.
PrintTo(D298Stream,"if ! python3 -u -B ",D298Producer,
  " --mode PRODUCTION --output ",D298Receipt," --resume ",D298ResumeInput,
  " --seconds 10800 --boundary-pairs 8000000 --fibre-scans 80000000",
  " --candidate-words 2000000 --retained-columns 250000",
  " --checkpoint-bytes 4000000000 --rss-bytes 5700000000",
  " --oracle-rounds 1 >> ",D298ProducerLog," 2>&1; then cat ",
  D298ProducerLog,"; exit 1; fi\n");
PrintTo(D298Stream,"cat ",D298ProducerLog,"\n");
PrintTo(D298Stream,"test \"$(grep -c '^",D298ProducerTerminal,
  " ' ",D298ProducerLog,")\" -eq 1\n");
PrintTo(D298Stream,"grep -Ec '^",D298ProducerTerminal," ",D298TerminalGrammar,
  "$' ",D298ProducerLog," | grep -qx 1\n");
PrintTo(D298Stream,"grep -Fxc '",D298ExtractMarker,"' ",D298ProducerLog,
  " | grep -qx 1\n");

## Always run the existing helper-nonshared checker after the producer.
PrintTo(D298Stream,"if ! python3 -u -B ",D298Checker," ",D298Receipt,
  " > ",D298CheckerLog," 2>&1; then cat ",D298CheckerLog,"; exit 1; fi\n");
PrintTo(D298Stream,"cat ",D298CheckerLog,"\n");
PrintTo(D298Stream,"test \"$(grep -c '^",D298CheckerPass,
  " terminal=' ",D298CheckerLog,")\" -eq 1\n");
PrintTo(D298Stream,"grep -Ec '^",D298CheckerPass," terminal=",D298TerminalGrammar,
  "$' ",D298CheckerLog," | grep -qx 1\n");
PrintTo(D298Stream,"producer_terminal=$(grep -E '^",D298ProducerTerminal,
  " ' ",D298ProducerLog," | sed -E 's/^",D298ProducerTerminal," //')\n");
PrintTo(D298Stream,"checker_terminal=$(grep -E '^",D298CheckerPass,
  " terminal=' ",D298CheckerLog," | sed -E 's/^",D298CheckerPass,
  " terminal=//')\n");
PrintTo(D298Stream,"test \"$producer_terminal\" = \"$checker_terminal\"\n");

## Shell-level sidecar check in addition to the independent checker.
PrintTo(D298Stream,"if python3 - ",D298Receipt," ",D298Checkpoint,
  " \"$producer_terminal\" >> ",D298CheckerLog," 2>&1 <<'PY'\n");
PrintTo(D298Stream,"import hashlib\nimport json\nimport sys\nfrom pathlib import Path\n");
PrintTo(D298Stream,"receipt_path=Path(sys.argv[1])\nsidecar=Path(sys.argv[2])\nterminal=sys.argv[3]\n");
PrintTo(D298Stream,"def reject(reason):\n raise SystemExit('TASK298_SIDECAR_REJECT:'+reason)\n");
PrintTo(D298Stream,"try:\n receipt=json.loads(receipt_path.read_text(encoding='utf-8'))\nexcept (OSError,UnicodeError,json.JSONDecodeError):\n reject('receipt')\n");
PrintTo(D298Stream,"if receipt.get('terminal')!=terminal: reject('terminal')\n");
PrintTo(D298Stream,"def check_reference(ref):\n");
PrintTo(D298Stream," if not isinstance(ref,dict) or set(ref)!={'path','bytes','sha256'}: reject('reference_shape')\n");
PrintTo(D298Stream," if ref.get('path')!=sidecar.name or Path(ref['path']).name!=ref['path']: reject('reference_path')\n");
PrintTo(D298Stream," if not sidecar.is_file(): reject('sidecar_missing')\n");
PrintTo(D298Stream," raw=sidecar.read_bytes()\n");
PrintTo(D298Stream," if len(raw)!=ref.get('bytes') or hashlib.sha256(raw).hexdigest()!=ref.get('sha256'): reject('sidecar_identity')\n");
PrintTo(D298Stream,"ref=receipt.get('checkpoint')\n");
PrintTo(D298Stream,"if terminal=='",D298Common,"':\n");
PrintTo(D298Stream," if 'checkpoint' in receipt or sidecar.exists(): reject('common_sidecar')\n");
PrintTo(D298Stream,"elif terminal.startswith('UNKNOWN_RESOURCE:'):\n");
PrintTo(D298Stream," if ref is None: reject('resource_reference')\n check_reference(ref)\n");
PrintTo(D298Stream,"elif terminal.startswith('UNKNOWN_INPUT:'):\n");
PrintTo(D298Stream," if ref is None:\n  if sidecar.exists(): reject('unreferenced_sidecar')\n else:\n  check_reference(ref)\n");
PrintTo(D298Stream,"else:\n reject('terminal_grammar')\n");
PrintTo(D298Stream,"print('TASK298_SIDECAR_PASS terminal='+terminal)\n");
PrintTo(D298Stream,"PY\nthen\n  :\nelse\n  cat ",D298CheckerLog,"\n  exit 1\nfi\n");
PrintTo(D298Stream,"grep -Ec '^TASK298_SIDECAR_PASS terminal=",D298TerminalGrammar,
  "$' ",D298CheckerLog," | grep -qx 1\n");
PrintTo(D298Stream,"test -s ",D298Receipt," -a -s ",D298ProducerLog,
  " -a -s ",D298CheckerLog,"\n");
PrintTo(D298Stream,"printf '%s' '",D298Sentinel,"' > ",D298OK,"\n");
PrintTo(D298Stream,"test -s ",D298OK,"\n");
CloseStream(D298Stream);;

Exec(Concatenation("bash ",D298Shell));;
D298ObservedSentinel:=D298Read(D298OK);;
if D298ObservedSentinel<>D298Sentinel then
  Error("task298 sentinel payload mismatch");
fi;
Print("R07_TASK192_CHECKPOINT_RESUME_TRANSPORT_V2_DRIVER_PASS terminal=AUTHENTICATED_CHECKER_TERMINAL\n");
