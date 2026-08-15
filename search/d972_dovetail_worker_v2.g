#############################################################################
## d972_dovetail_worker_v2.g
##
## DMTCP-safe exact worker for the D972 relative-extension dovetail.
##
## The mathematical routines are the frozen v1 routines below the v1 dispatch
## boundary.  This file adds a v2 receipt envelope and a resumability contract.
## In particular, resumability is never inferred from an outer tuple cursor:
## GAP state inside canonical relabelling, Aut(H), MTC/fp-order, and the full
## 972-fibre scan is recoverable only when the workflow launches this process
## under DMTCP and independently seals the checkpoint-image manifest.
##
## Required for a resumable workflow receipt:
##   D972_DMTCP_ENABLED=1
##   D972_DMTCP_CONTRACT_SHA256=<64 lowercase hexadecimal characters>
## Optional provenance bindings:
##   D972_DMTCP_VERSION, D972_DMTCP_GENERATION,
##   D972_DMTCP_IMAGE_MANIFEST_SHA256, D972_UNIVERSE_ID,
##   D972_INPUT_DIGEST, D972_TASK_DIGEST, D972_HEARTBEAT
##
## D972_HEARTBEAT is an overwrite-only, non-authoritative diagnostic file.
## Only the final v2 result envelope has authority to complete/advance a cell.
#############################################################################

D972V2V1Path := "search/d972_dovetail_worker_v1.g";;
D972V2ExpectedV1SHA256 :=
  "323d18de4fadcf4561222995f5b6590bb560cd617048d2e9b54049ae3eea9efd";;

## Load all frozen v1 definitions without executing its mode dispatcher/QUIT.
## A temporary copy is used because the source is intentionally kept versioned
## and immutable.  The digest gate makes this dependency explicit.
## GAP 4.13 has no GetEnv global (GAP 4.14+ may provide one).  The frozen
## v1 library below calls GetEnv at load time, so install a compatibility
## accessor before reading it.  GAPInfo.SystemEnvironment is core GAP state;
## missing names intentionally return fail and are handled by the callers.
if not IsBound(GetEnv) then
  GetEnv := function(name)
    if IsBound(GAPInfo.SystemEnvironment) and
       IsBound(GAPInfo.SystemEnvironment.(name)) then
      return GAPInfo.SystemEnvironment.(name);
    fi;
    return fail;
  end;
fi;;

D972V2LoadV1Library := function()
  local source, actual, marker, cut, dir, path, prefix;
  source := StringFile(D972V2V1Path);
  if source = fail then Error("D972 v2: could not read frozen v1 worker"); fi;
  actual := HexSHA256(source);
  if actual <> D972V2ExpectedV1SHA256 then
    Error("D972 v2: frozen v1 worker digest drift: ",actual);
  fi;
  source := ReplacedString(source,"\r\n","\n");
  marker := Concatenation("\nif D972Mode = ","\"selftest\" then");
  cut := PositionSublist(source,marker);
  if cut = fail then Error("D972 v2: v1 dispatch boundary not found"); fi;
  prefix := source{[1..cut-1]};
  dir := DirectoryTemporary();
  if dir = fail then Error("D972 v2: no temporary directory"); fi;
  path := Filename(dir,"d972_dovetail_worker_v1_library.g");
  ## FileString is the byte-faithful writer on GAP 4.13.  PrintTo is
  ## stream/printing oriented and can abbreviate a large string, which
  ## corrupts the generated v1 prefix at a token boundary.
  FileString(path,prefix);
  actual := StringFile(path);
  if actual <> prefix then
    Error("D972 v2: generated v1 library is not byte-faithful");
  fi;
  Read(path);
end;;

D972V2LoadV1Library();;

D972V2GetEnv := function(name, fallback)
  local value;
  value := GetEnv(name);
  if value = fail or value = "" then return fallback; fi;
  return value;
end;;

D972V2IsLowerHex64 := function(value)
  return IsString(value) and Length(value)=64 and
    ForAll(value,c->c in "0123456789abcdef");
end;;

D972V2DmtcpEnabled := D972V2GetEnv("D972_DMTCP_ENABLED","0")="1";;
D972V2DmtcpContract :=
  D972V2GetEnv("D972_DMTCP_CONTRACT_SHA256","");;
D972V2DmtcpReady := D972V2DmtcpEnabled and
  D972V2IsLowerHex64(D972V2DmtcpContract);;
D972V2DmtcpVersion := D972V2GetEnv("D972_DMTCP_VERSION","unknown");;
D972V2DmtcpGeneration :=
  D972V2GetEnv("D972_DMTCP_GENERATION","0");;
D972V2DmtcpImageManifest :=
  D972V2GetEnv("D972_DMTCP_IMAGE_MANIFEST_SHA256","");;
D972V2HeartbeatPath := D972V2GetEnv("D972_HEARTBEAT","");;
D972V2UniverseId := D972V2GetEnv("D972_UNIVERSE_ID","unbound");;
D972V2InputDigest := D972V2GetEnv("D972_INPUT_DIGEST","unbound");;
D972V2TaskDigestClaim := D972V2GetEnv("D972_TASK_DIGEST","");;
D972V2TaskPath := D972V2GetEnv("D972_TASK_G","");;
if D972V2TaskPath=fail or D972V2TaskPath="" then
  D972V2TaskPath:=D972V2GetEnv("D972_TASK","");
fi;;
D972V2TaskDigest := "unbound";;
D972V2TaskMeta := fail;;
D972V2LastAutCount := fail;;
if D972V2TaskPath<>fail and D972V2TaskPath<>"" then
  D972V2TaskDigest:=HexSHA256(StringFile(D972V2TaskPath));
  if D972V2TaskDigestClaim<>"" and
     D972V2TaskDigestClaim<>D972V2TaskDigest then
    Error("D972 v2: task digest claim mismatch");
  fi;
  Read(D972V2TaskPath);
  if IsBound(D972_TASK) then D972V2TaskMeta:=D972_TASK; fi;
fi;;

if D972V2TaskMeta<>fail then
  if IsBound(D972V2TaskMeta.universe_id) then
    if D972V2UniverseId<>"unbound" and
       D972V2UniverseId<>D972V2TaskMeta.universe_id then
      Error("D972 v2: universe id environment/task mismatch");
    fi;
    D972V2UniverseId:=D972V2TaskMeta.universe_id;
  fi;
  if IsBound(D972V2TaskMeta.input_digest) then
    if D972V2InputDigest<>"unbound" and
       D972V2InputDigest<>D972V2TaskMeta.input_digest then
      Error("D972 v2: input digest environment/task mismatch");
    fi;
    D972V2InputDigest:=D972V2TaskMeta.input_digest;
  fi;
fi;;

D972V2CursorField := function(T, primary, alternate)
  if T=fail then return fail; fi;
  if IsBound(T.(primary)) then return T.(primary); fi;
  if alternate<>"" and IsBound(T.(alternate)) then return T.(alternate); fi;
  return fail;
end;;

D972V2OuterCursorJson := function(T)
  local a,d,l;
  a:=D972V2CursorField(T,"aut_pair_index","automorphism_pair_index");
  d:=D972V2CursorField(T,"defect_index","relator_defect_index");
  l:=D972V2CursorField(T,"lift_pair_index","marked_lift_index");
  if a=fail or d=fail or l=fail then return "null"; fi;
  return Concatenation("{\"aut_pair_index\":",String(a),
    ",\"defect_index\":",String(d),
    ",\"lift_pair_index\":",String(l),"}");
end;;

D972V2Radices := function(T)
  local k,r,acount;
  if T=fail or not IsBound(T.kernel_table) then return fail; fi;
  k:=Length(T.kernel_table);
  if IsBound(T.q_relators) then r:=Length(T.q_relators);
  elif IsBound(T.base_relators) then r:=Length(T.base_relators);
  else return fail; fi;
  if IsBound(T.aut_count) then acount:=T.aut_count;
  elif IsBound(T.automorphism_count) then acount:=T.automorphism_count;
  elif D972V2LastAutCount<>fail then acount:=D972V2LastAutCount;
  else
    ## This exact fallback is potentially expensive, but it is itself covered
    ## by DMTCP.  Candidate/shadow modes normally populate the cache while
    ## doing their mathematically required Aut(H) enumeration, so no second
    ## enumeration is performed in the normal path.
    acount:=Length(D972TableAutomorphisms(T.kernel_table));
    D972V2LastAutCount:=acount;
  fi;
  return rec(k:=k,relator_count:=r,aut_count:=acount,
    automorphism_pair_count:=acount^2,
    defect_count:=k^r,
    extension_class_count:=acount^2*k^r,
    marked_orbit_count:=k^2);
end;;

D972V2RadicesJson := function(R)
  if R=fail then return "null"; fi;
  return Concatenation("{\"automorphism_count\":",String(R.aut_count),
    ",\"automorphism_pair_count\":",String(R.automorphism_pair_count),
    ",\"defect_count\":",String(R.defect_count),
    ",\"extension_class_count\":",String(R.extension_class_count),
    ",\"marked_orbit_count\":",String(R.marked_orbit_count),"}");
end;;

D972V2NextOuterCursorJson := function(T,R)
  local a,d,l;
  if R=fail then return "null"; fi;
  a:=D972V2CursorField(T,"aut_pair_index","automorphism_pair_index");
  d:=D972V2CursorField(T,"defect_index","relator_defect_index");
  l:=D972V2CursorField(T,"lift_pair_index","marked_lift_index");
  if a=fail or d=fail or l=fail then return "null"; fi;
  l:=l+1;
  if l=R.marked_orbit_count then
    l:=0; d:=d+1;
    if d=R.defect_count then
      d:=0; a:=a+1;
      if a=R.automorphism_pair_count then return "null"; fi;
    fi;
  fi;
  return Concatenation("{\"aut_pair_index\":",String(a),
    ",\"defect_index\":",String(d),
    ",\"lift_pair_index\":",String(l),"}");
end;;

D972V2Heartbeat := function(stage, phase, cursorJson)
  local body;
  if D972V2HeartbeatPath="" then return; fi;
  body:=Concatenation(
    "{\"schema\":\"d972_dovetail_heartbeat/v2\"",
    ",\"authoritative\":false",
    ",\"stage\":",D972JsonString(stage),
    ",\"phase\":",D972JsonString(phase),
    ",\"logical_outer_cursor\":",cursorJson,
    ",\"opaque_inner_cursor_storage\":\"DMTCP process image\"",
    ",\"dmtcp_generation\":",D972JsonString(D972V2DmtcpGeneration),
    ",\"task_digest\":",D972JsonString(D972V2TaskDigest),"}");
  WriteFile(D972V2HeartbeatPath,Concatenation(body,"\n"));
end;;

## Preserve the original algorithms, adding diagnostic safe-boundary markers.
## DMTCP, not these heartbeats, serializes a loop or library call mid-flight.
D972V1CanonicalTable := D972CanonicalTable;;
D972CanonicalTable := function(tbl)
  local answer;
  D972V2Heartbeat("canonical_table_relabel","entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  answer:=D972V1CanonicalTable(tbl);
  D972V2Heartbeat("canonical_table_relabel","completed",
    D972V2OuterCursorJson(D972V2TaskMeta));
  return answer;
end;;

D972V1TableAutomorphisms := D972TableAutomorphisms;;
D972TableAutomorphisms := function(tbl)
  local answer;
  D972V2Heartbeat("automorphism_enumeration","entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  answer:=D972V1TableAutomorphisms(tbl);
  D972V2LastAutCount:=Length(answer);
  D972V2Heartbeat("automorphism_enumeration","completed",
    D972V2OuterCursorJson(D972V2TaskMeta));
  return answer;
end;;

D972V1BuildDefectPresentation := D972BuildDefectPresentation;;
D972BuildDefectPresentation := function(Hrec,qRelators,autLabels,defects)
  local answer;
  D972V2Heartbeat("extension_class","presentation_build_entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  answer:=D972V1BuildDefectPresentation(Hrec,qRelators,autLabels,defects);
  D972V2Heartbeat("extension_class","presentation_build_completed",
    D972V2OuterCursorJson(D972V2TaskMeta));
  return answer;
end;;

## This is the v1 exact gate with explicit phase markers around the opaque GAP
## calls.  A DMTCP image taken in either call contains its actual internal
## enumerator state; the phase marker alone is never resume authority.
D972ExactEmbeddingGate := function(Pdata, expectedH, expectedQ)
  local P,Hsub,pres,Hfp,hsize,psize,normal,cursor;
  cursor:=D972V2OuterCursorJson(D972V2TaskMeta);
  P:=Pdata.fp;
  Hsub:=Subgroup(P,Pdata.h_words{[2..Length(Pdata.h_words)]});
  normal:=IsNormal(P,Hsub);
  D972V2Heartbeat("fp_order","presentation_subgroup_mtc_entered",cursor);
  pres:=PresentationSubgroupMtc(P,Hsub,"h",0);
  D972V2Heartbeat("fp_order","presentation_subgroup_mtc_completed",cursor);
  Hfp:=FpGroupPresentation(pres);
  D972V2Heartbeat("fp_order","kernel_size_entered",cursor);
  hsize:=Size(Hfp);
  D972V2Heartbeat("fp_order","kernel_size_completed",cursor);
  D972V2Heartbeat("fp_order","extension_size_entered",cursor);
  psize:=Size(P);
  D972V2Heartbeat("fp_order","extension_size_completed",cursor);
  return rec(normal:=normal,h_size:=hsize,p_size:=psize,
    h_embeds:=hsize=expectedH,exact_order:=psize=expectedH*expectedQ);
end;;

D972V1CandidateMode := D972CandidateMode;;
D972CandidateMode := function()
  D972V2Heartbeat("marked_orbit","candidate_cell_entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  D972V1CandidateMode();
end;;

D972V1ShadowFiberMode := D972ShadowFiberMode;;
D972ShadowFiberMode := function()
  D972V2Heartbeat("972_fiber_scan","full_scan_entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  D972V1ShadowFiberMode();
end;;

## Replace v1's honest blocked receipt by an equally honest conditional one.
## A worker result alone does not prove that a DMTCP image exists: the external
## producer/checker must bind and verify the image-manifest receipt.
D972CompletenessReceiptJson := function()
  local live;
  if D972V2DmtcpReady then live:="READY_DMTCP_EXTERNAL_IMAGE_RECEIPT_REQUIRED";
  else live:="BLOCKED_DMTCP_CONTRACT_NOT_ENABLED"; fi;
  return Concatenation(
    "{\"scope\":\"fixed labelled H and fixed marked finite presentation of Qbar\"",
    ",\"b3_stable_encoding\":\"enumerate full P=B3/L over B3/M; E=ker(P to S3) is gated to order k|PB3/M|\"",
    ",\"nonabelian_h_supported\":true",
    ",\"automorphism_pairs_exhaustive\":true",
    ",\"relator_defect_tuples_exhaustive\":true",
    ",\"marked_lift_pairs_exhaustive\":true",
    ",\"outer_buckets_prune_nothing\":true",
    ",\"exactness_gate\":\"H embeds and |P|=|H||Qbar|; factor kernel has size |H|\"",
    ",\"argument\":\"chosen lifts induce two automorphisms of H and one H-valued defect for every base relator; conversely the Cayley, conjugation and defect presentation with the exactness gate is precisely an extension; every marked lift lies in one enumerated H-coset\"",
    ",\"workflow_resumable\":",D972Bool(D972V2DmtcpReady),
    ",\"worker_alone_resume_authority\":false",
    ",\"liveness_status\":",D972JsonString(live),
    ",\"checkpoint_transport\":\"DMTCP full-process image plus independently sealed workflow manifest\"",
    ",\"checkpointed_internal_cursors\":{",
      "\"canonical_table_relabel\":\"GAP loop locals in DMTCP image\",",
      "\"Aut(H)\":\"GAP loop locals in DMTCP image\",",
      "\"extension_class\":\"logical outer coordinate plus GAP presentation state in DMTCP image\",",
      "\"marked_orbit\":\"logical outer coordinate plus GAP locals in DMTCP image\",",
      "\"fp_order\":\"MTC/Size call stack and heap in DMTCP image\",",
      "\"972_fiber_scan\":\"m/f loop locals, accumulators, and group objects in DMTCP image\"}",
    ",\"heartbeat_authoritative\":false",
    ",\"completed_cell_authority\":\"final d972_dovetail_worker/v2 envelope only\"",
    ",\"terminal_A_condition\":\"completed exact isolated shadow-fibre classification with first eligible zero fibre\"",
    ",\"finite_cap_or_nontermination_is_terminal_B\":false",
    ",\"dmtcp_contract_sha256\":",
      D972JsonString(D972V2DmtcpContract),"}"
  );
end;;

## Authority-receipt digest recipe (no terminal LF):
##
##   schema=d972_dovetail_worker/v2
##   |mode=<mode>|status=<status>|universe_id=<universe_id>
##   |input_digest=<input_digest>|task_digest=<task_digest>
##   |payload_sha256=<payload_sha256>
##   |cursor_before=<canonical compact JSON>
##   |cursor_after=<canonical compact JSON>
##   |radices=<canonical compact JSON>
##   |completed_range=<canonical compact JSON>
##   |cell_complete=<lowercase JSON boolean>
##   |classification_complete=<lowercase JSON boolean>
##   |outer_advance_authorized=<lowercase JSON boolean>
##   |exhausted=<lowercase JSON boolean>
##   |h_exhausted=<lowercase JSON boolean>
##   |terminal_A_eligible=<lowercase JSON boolean>
##   |workflow_resumable=<lowercase JSON boolean>
##   |dmtcp_contract_sha256=<digest>
##   |dmtcp_generation=<generation>
##
## Cursor, radices and completed-range objects below are emitted in sorted-key
## order.  An independent implementation may reproduce them with
## json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).
D972V2AuthorityMaterial := function(mode,status,universeId,inputDigest,
    taskDigest,payloadDigest,before,after,radicesJson,completedJson,
    cellComplete,classificationComplete,outerAdvanceAuthorized,exhausted,
    hExhausted,terminalA,workflowResumable,contract,generation)
  return Concatenation(
    "schema=d972_dovetail_worker/v2",
    "|mode=",mode,
    "|status=",status,
    "|universe_id=",universeId,
    "|input_digest=",inputDigest,
    "|task_digest=",taskDigest,
    "|payload_sha256=",payloadDigest,
    "|cursor_before=",before,
    "|cursor_after=",after,
    "|radices=",radicesJson,
    "|completed_range=",completedJson,
    "|cell_complete=",D972Bool(cellComplete),
    "|classification_complete=",D972Bool(classificationComplete),
    "|outer_advance_authorized=",D972Bool(outerAdvanceAuthorized),
    "|exhausted=",D972Bool(exhausted),
    "|h_exhausted=",D972Bool(hExhausted),
    "|terminal_A_eligible=",D972Bool(terminalA),
    "|workflow_resumable=",D972Bool(workflowResumable),
    "|dmtcp_contract_sha256=",contract,
    "|dmtcp_generation=",generation
  );
end;;

## Wrap every frozen v1 result in a restart-idempotent v2 envelope.  The result
## path is overwritten once; workflow code must ingest it only after clean GAP
## exit.  Restarting an image before/after the write therefore cannot append a
## duplicate ledger row.
D972V1Emit := D972Emit;;
D972Emit := function(payload)
  local payloadDigest,R,before,next,accepted,cellComplete,hExhausted,
        classificationComplete,outerAdvanceAuthorized,terminalA,status,
        completed,radicesJson,material,result,imageManifest;
  payloadDigest:=HexSHA256(payload);
  R:=D972V2Radices(D972V2TaskMeta);
  radicesJson:=D972V2RadicesJson(R);
  before:=D972V2OuterCursorJson(D972V2TaskMeta);
  next:=D972V2NextOuterCursorJson(D972V2TaskMeta,R);
  accepted:=PositionSublist(payload,"\"accepted_count\":1")<>fail;
  terminalA:=PositionSublist(payload,
    "\"campaign_stop_first_empty_fiber\":true")<>fail;
  if PositionSublist(payload,"\"status\":\"INCONSISTENT_STOP\"")<>fail then
    status:="INCONSISTENT_STOP";
  else status:="PASS"; fi;
  if D972Mode="candidate" or
     (D972Mode="checkpoint" and D972V2TaskMeta<>fail and
      IsBound(D972V2TaskMeta.operation) and
      D972V2TaskMeta.operation="candidate") then
    ## The relative-extension candidate cell has completed even when it is
    ## accepted.  In that case its shadow classification is the next stage and
    ## the outer cursor is deliberately held until that stage completes.
    cellComplete:=true;
    classificationComplete:=not accepted;
    outerAdvanceAuthorized:=not accepted;
    if accepted then next:=before; fi;
    completed:=Concatenation(
      "{\"relative_extension_complete\":true",
      ",\"shadow_classification_complete\":",
      D972Bool(classificationComplete),
      ",\"stage\":\"marked_orbit\",\"start\":",before,
      ",\"stop\":",next,"}");
  elif D972Mode="shadow-fiber" or
       (D972Mode="checkpoint" and D972V2TaskMeta<>fail and
        IsBound(D972V2TaskMeta.operation) and
        D972V2TaskMeta.operation="shadow-fiber") then
    cellComplete:=true;
    classificationComplete:=true;
    outerAdvanceAuthorized:=true;
    completed:=Concatenation(
      "{\"complete\":true,\"stage\":\"972_fiber_scan\",",
      "\"start\":0,",
      "\"stop_source\":\"payload.charming_pair_universe\"}");
  else
    cellComplete:=true;
    classificationComplete:=true;
    outerAdvanceAuthorized:=true;
    completed:=Concatenation("{\"complete\":true,\"stage\":",
      D972JsonString(D972Mode),"}");
  fi;
  hExhausted:=outerAdvanceAuthorized and next="null" and before<>"null";
  if D972V2IsLowerHex64(D972V2DmtcpImageManifest) then
    imageManifest:=D972JsonString(D972V2DmtcpImageManifest);
  else imageManifest:="null"; fi;
  material:=D972V2AuthorityMaterial(
    D972Mode,status,D972V2UniverseId,D972V2InputDigest,D972V2TaskDigest,
    payloadDigest,before,next,radicesJson,completed,cellComplete,
    classificationComplete,outerAdvanceAuthorized,hExhausted,hExhausted,
    terminalA,D972V2DmtcpReady,D972V2DmtcpContract,
    D972V2DmtcpGeneration);
  result:=Concatenation(
    "{\"schema\":\"d972_dovetail_worker/v2\"",
    ",\"mode\":",D972JsonString(D972Mode),
    ",\"status\":",D972JsonString(status),
    ",\"universe_id\":",D972JsonString(D972V2UniverseId),
    ",\"input_digest\":",D972JsonString(D972V2InputDigest),
    ",\"task_digest\":",D972JsonString(D972V2TaskDigest),
    ",\"payload_sha256\":",D972JsonString(payloadDigest),
    ",\"cursor_before\":",before,
    ",\"cursor_after\":",next,
    ",\"outer_cursor_before\":",before,
    ",\"outer_cursor_after\":",next,
    ",\"radices\":",radicesJson,
    ",\"completed_range\":",completed,
    ",\"cell_complete\":",D972Bool(cellComplete),
    ",\"classification_complete\":",D972Bool(classificationComplete),
    ",\"outer_advance_authorized\":",D972Bool(outerAdvanceAuthorized),
    ",\"exhausted\":",D972Bool(hExhausted),
    ",\"h_exhausted\":",D972Bool(hExhausted),
    ",\"terminal_A_eligible\":",D972Bool(terminalA),
    ",\"terminal_A_requires_independent_checker\":true",
    ",\"workflow_resumable\":",D972Bool(D972V2DmtcpReady),
    ",\"opaque_internal_state_checkpointed_by\":\"DMTCP process image; authority is external image manifest\"",
    ",\"dmtcp\":{\"enabled\":",D972Bool(D972V2DmtcpEnabled),
      ",\"contract_ready\":",D972Bool(D972V2DmtcpReady),
      ",\"version\":",D972JsonString(D972V2DmtcpVersion),
      ",\"generation\":",D972JsonString(D972V2DmtcpGeneration),
      ",\"contract_sha256\":",D972JsonString(D972V2DmtcpContract),
      ",\"image_manifest_sha256\":",imageManifest,"}",
    ",\"checkpoint\":{\"logical_outer_cursor\":",before,
      ",\"internal_cursor_storage\":\"DMTCP process image\",",
      "\"heartbeat_authoritative\":false}",
    ",\"checkpoint_sha256\":",D972JsonString(HexSHA256(material)),
    ",\"relative_extension_completeness_receipt\":",
      D972CompletenessReceiptJson(),
    ",\"payload\":",payload,"}"
  );
  D972V2Heartbeat("result","cell_result_committed",next);
  if D972Output="" then Print(result,"\n");
  else WriteFile(D972Output,Concatenation(result,"\n")); fi;
end;;

D972V2Dispatch := function()
  local operation;
  D972V2Heartbeat("dispatch","entered",
    D972V2OuterCursorJson(D972V2TaskMeta));
  if D972Mode="checkpoint" then
    if D972V2TaskMeta=fail or not IsBound(D972V2TaskMeta.operation) then
      Error("checkpoint mode needs D972_TASK.operation");
    fi;
    operation:=D972V2TaskMeta.operation;
    if operation="candidate" then D972CandidateMode();
    elif operation="shadow-fiber" then D972ShadowFiberMode();
    elif operation="compare" then D972CompareMode();
    else Error("checkpoint operation not implemented: ",operation); fi;
  elif D972Mode="selftest" then D972SelfTest();
  elif D972Mode="base-audit" then D972BaseMode(true);
  elif D972Mode="preflight" then D972BaseMode(false);
  elif D972Mode="base-presentation" then D972BaseMode(true);
  elif D972Mode="kernel-catalog" then D972KernelCatalogMode();
  elif D972Mode="candidate" or D972Mode="slice" then D972CandidateMode();
  elif D972Mode="shadow-fiber" then D972ShadowFiberMode();
  elif D972Mode="compare" then D972CompareMode();
  else Error("mode not implemented yet: ",D972Mode); fi;
end;;

D972V2Dispatch();
QUIT;
