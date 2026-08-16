#!/usr/bin/env python3
"""Independent v2 checker and DMTCP checkpoint-envelope verifier.

Campaign candidate mathematics is checked by the independent v1 checker: it
reconstructs every finite presentation in a generated GAP program that reads
neither producer nor campaign worker code.  This front end adds the v2 duties
that did not exist in v1: exact code/contract binding, cryptographic sealing of
the whole-process DMTCP image set, generation lineage, stable-path/runtime
compatibility checks, and fail-closed A-terminal gating.
"""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
LEGACY_PATH = ROOT / "search" / "check_d972_dovetail_v1.py"
PRODUCER_V2 = ROOT / "search" / "d972_dovetail_producer_v2.py"
WORKER_V2 = ROOT / "search" / "d972_dovetail_worker_v2.g"
MANIFEST_V2 = ROOT / "search" / "d972_dovetail_manifest_v2.json"
SCHEMA_V2 = ROOT / "search" / "d972_dovetail_state_schema_v2.json"
WORKFLOW_V2 = ROOT / ".github" / "workflows" / "d972-dovetail-v2.yml"
CALIBRATION_PAPER = ROOT / "sol" / "sol_reply_143_typedfiber.md"
CALIBRATION_PAPER_SHA256 = "ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a"
FINAL_A_SEAL_NAME = "final-v2-completion.json"
CALIBRATION_TARGET_KEY_SHA256 = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
CALIBRATION_BACKEND = (
    "generated self-contained GAP; checker-local base/six-coset/Q8; "
    "no worker or producer helper"
)
ZERO_SHA = "0" * 64
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class CheckStop(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckStop(message)


def is_sha(value: Any) -> bool:
    return isinstance(value, str) and SHA_RE.fullmatch(value) is not None


def worker_authority_material(receipt: dict[str, Any]) -> str:
    def compact(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    def boolean(value: Any) -> str:
        return "true" if value is True else "false"

    dmtcp = receipt["dmtcp"]
    parts = [
        ("schema", receipt["schema"]), ("mode", receipt["mode"]),
        ("status", receipt["status"]), ("universe_id", receipt["universe_id"]),
        ("input_digest", receipt["input_digest"]), ("task_digest", receipt["task_digest"]),
        ("payload_sha256", receipt["payload_sha256"]),
        ("cursor_before", compact(receipt["cursor_before"])),
        ("cursor_after", compact(receipt["cursor_after"])),
        ("radices", compact(receipt["radices"])),
        ("completed_range", compact(receipt["completed_range"])),
        ("cell_complete", boolean(receipt["cell_complete"])),
        ("classification_complete", boolean(receipt["classification_complete"])),
        ("outer_advance_authorized", boolean(receipt["outer_advance_authorized"])),
        ("exhausted", boolean(receipt["exhausted"])),
        ("h_exhausted", boolean(receipt["h_exhausted"])),
        ("terminal_A_eligible", boolean(receipt["terminal_A_eligible"])),
        ("workflow_resumable", boolean(receipt["workflow_resumable"])),
        ("dmtcp_contract_sha256", dmtcp["contract_sha256"]),
        ("dmtcp_generation", str(dmtcp["generation"])),
    ]
    return "|".join(f"{key}={value}" for key, value in parts)


def load_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST_V2.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckStop(f"STATE_STOP v2 manifest unreadable: {exc}") from exc
    contract = manifest.get("dmtcp_contract")
    require(isinstance(contract, dict), "STATE_STOP dmtcp contract absent")
    body = copy.deepcopy(contract)
    claimed = body.pop("contract_sha256", None)
    require(claimed == sha_bytes(canonical_bytes(body)),
            "STATE_STOP dmtcp contract hash mismatch")
    return manifest


def expected_runtime_receipt(manifest: dict[str, Any]) -> dict[str, Any]:
    # Import the producer wrapper as data-independent code and call only its
    # hashing helper.  Candidate validation below remains checker-local/v1.
    spec = importlib.util.spec_from_file_location("d972_producer_v2_binding", PRODUCER_V2)
    require(spec is not None and spec.loader is not None,
            "STATE_STOP producer-v2 binding helper unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.v2_code_receipt(manifest)


def state_checkpoint_hash(state: dict[str, Any]) -> str:
    body = copy.deepcopy(state)
    require(isinstance(body.get("hash_chain"), dict), "STATE_STOP state hash chain absent")
    body["hash_chain"]["checkpoint_sha256"] = ZERO_SHA
    return sha_bytes(canonical_bytes(body))


def validate_v2_state_binding(state: dict[str, Any], manifest: dict[str, Any]) -> None:
    require(state.get("schema_version") == "d972-dovetail-state/v1",
            "STATE_STOP mathematical state schema drift")
    require(state.get("hash_chain", {}).get("checkpoint_sha256") == state_checkpoint_hash(state),
            "STATE_STOP mathematical checkpoint digest mismatch")
    receipt = state.get("receipts", {}).get("v2_runtime_integrity")
    require(receipt == expected_runtime_receipt(manifest),
            "STATE_STOP v2 runtime/code binding drift")
    require(receipt.get("whole_process_tree_required") is True and
            receipt.get("timeout_policy") ==
            "no subprocess wall timeout; external DMTCP supervisor only",
            "STATE_STOP unsafe v2 timeout policy")
    worker_receipts = collect_worker_receipts(state.get("receipts", {}))
    for candidate_key in ("producer", "checker"):
        # Ledger rows are checked separately by the v1 checker; bindings here
        # have no embedded receipts.  This loop intentionally stays on state.
        require(candidate_key in state.get("ledgers", {}),
                "STATE_STOP mathematical ledger binding absent")
    for worker_receipt in worker_receipts:
        validate_worker_receipt(worker_receipt, manifest)
    gate = state.get("calibration_gate", {})
    if gate.get("status") == "PASSED" or gate.get("search_unlocked") is True:
        validate_independent_calibration_receipt(
            state.get("receipts", {}).get("independent_calibration_checker_v2"), gate, state
        )


def collect_worker_receipts(value: Any) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    if isinstance(value, dict):
        nested = value.get("v2_process_checkpoint_receipt")
        if isinstance(nested, dict):
            receipts.append(nested)
        for item in value.values():
            receipts.extend(collect_worker_receipts(item))
    elif isinstance(value, list):
        for item in value:
            receipts.extend(collect_worker_receipts(item))
    return receipts


def validate_worker_receipt(receipt: dict[str, Any], manifest: dict[str, Any]) -> None:
    require(receipt.get("schema") == "d972_dovetail_worker/v2" and
            isinstance(receipt.get("mode"), str) and
            receipt.get("workflow_resumable") is True,
            "STATE_STOP v2 worker receipt shape")
    require(receipt.get("universe_id") == manifest["universe_id"] and
            receipt.get("input_digest") == manifest["search_input_set_sha256"] and
            is_sha(receipt.get("payload_sha256")) and
            (is_sha(receipt.get("task_digest")) or receipt.get("task_digest") == "unbound"),
            "STATE_STOP v2 worker input binding")
    boolean_fields = (
        "cell_complete", "classification_complete", "outer_advance_authorized",
        "exhausted", "h_exhausted", "terminal_A_eligible", "workflow_resumable",
    )
    require(all(isinstance(receipt.get(key), bool) for key in boolean_fields) and
            receipt.get("cell_complete") is True and
            (receipt.get("radices") is None or isinstance(receipt.get("radices"), dict)) and
            isinstance(receipt.get("completed_range"), dict) and
            all(receipt.get(key) is None or isinstance(receipt.get(key), dict)
                for key in ("cursor_before", "cursor_after")) and
            receipt.get("outer_cursor_before") == receipt.get("cursor_before") and
            receipt.get("outer_cursor_after") == receipt.get("cursor_after"),
            "STATE_STOP v2 worker authority-field types/cursors")
    if receipt.get("mode") in {"candidate", "shadow-fiber"}:
        radices = receipt.get("radices")
        require(isinstance(radices, dict) and all(
            isinstance(radices.get(key), int) and radices[key] > 0 for key in (
                "automorphism_count", "automorphism_pair_count", "defect_count",
                "extension_class_count", "marked_orbit_count",
            )
        ), "STATE_STOP finite-cell worker radices absent")
    dmtcp = receipt.get("dmtcp", {})
    contract_sha = manifest["dmtcp_contract"]["contract_sha256"]
    require(dmtcp.get("enabled") is True and dmtcp.get("contract_ready") is True and
            dmtcp.get("contract_sha256") == contract_sha and
            re.fullmatch(r"[0-9]+", str(dmtcp.get("generation", ""))) is not None,
            "STATE_STOP v2 worker DMTCP binding")
    material = worker_authority_material(receipt)
    require(receipt.get("checkpoint_sha256") == sha_bytes(material.encode("utf-8")),
            "STATE_STOP v2 worker checkpoint digest")
    require(receipt.get("terminal_A_requires_independent_checker") is True and
            receipt.get("opaque_internal_state_checkpointed_by") ==
            "DMTCP process image; authority is external image manifest",
            "STATE_STOP worker bypassed independent terminal/checkpoint authority")
    completeness = receipt.get("relative_extension_completeness_receipt", {})
    require(completeness.get("workflow_resumable") is True and
            completeness.get("worker_alone_resume_authority") is False and
            completeness.get("heartbeat_authoritative") is False and
            completeness.get("finite_cap_or_nontermination_is_terminal_B") is False and
            completeness.get("dmtcp_contract_sha256") == contract_sha,
            "STATE_STOP false relative-extension completeness receipt")


CALIBRATION_METRICS = (
    "marked_orbit_count", "gt_orders", "image_sizes",
    "zero_fiber_counts", "fiber_histograms",
)


def calibration_observation(metrics: dict[str, Any]) -> dict[str, Any]:
    body = {key: copy.deepcopy(metrics[key]) for key in CALIBRATION_METRICS}
    body["receipt_sha256"] = sha_bytes(canonical_bytes(body))
    return body


def marked_c2_classification() -> dict[str, Any]:
    classes = [list(bits) for bits in itertools.product((0, 1), repeat=3)]
    t1 = lambda v: [v[0], v[1], (v[0] + v[1] + v[2]) % 2]
    t2 = lambda v: [(v[0] + v[1] + v[2]) % 2, v[1], v[2]]
    invariant = [v for v in classes if t1(v) == v and t2(v) == v]
    require(invariant == [[0, 0, 0], [1, 1, 1]],
            "STATE_STOP independent C2 transvection classification drift")
    specs = [
        {"orbit_id": "split_c2", "extension_class": "split",
         "class_coefficients": [0, 0, 0], "c_bit": 1},
        {"orbit_id": "nonsplit_q8_c0", "extension_class": "nonsplit",
         "class_coefficients": [1, 1, 1], "c_bit": 0},
        {"orbit_id": "nonsplit_q8_c1", "extension_class": "nonsplit",
         "class_coefficients": [1, 1, 1], "c_bit": 1},
    ]
    return {
        "coefficient_universe": classes,
        "transvection_1_images": [t1(v) for v in classes],
        "transvection_2_images": [t2(v) for v in classes],
        "invariant_classes": invariant,
        "marked_specs": specs,
        "paper_premise": {
            "path": "sol/sol_reply_143_typedfiber.md",
            "section": "5.4",
            "sha256": CALIBRATION_PAPER_SHA256,
        },
    }


def independent_calibration_gap_script(q_relators: Any, target_keys: list[str]) -> str:
    require(isinstance(q_relators, list) and q_relators,
            "STATE_STOP calibration base presentation absent")
    qrels = json.dumps(q_relators, separators=(",", ":"))
    targets = json.dumps(target_keys, ensure_ascii=True, separators=(",", ":"))
    return f"""\
MakeRels := function(F,rows)
  local g,out,row,w,x; g:=GeneratorsOfGroup(F); out:=[];
  for row in rows do w:=One(F); for x in row do
    if x>0 then w:=w*g[x]; else w:=w*g[-x]^-1; fi;
  od; Add(out,w); od; return out;
end;;
PaperProd := function(xs)
  local v,i; v:=xs[1]^0;
  for i in [Length(xs),Length(xs)-1..1] do v:=v*xs[i]; od;
  return v;
end;;
CheckerQT := function(Q,x,y,c)
  local elts,pos,posOf,n,one,xi,yi,to1,to2,mul1,mul2,a1,a2,t,i,d;
  elts:=Elements(Q); n:=Length(elts); one:=One(Q); xi:=x^-1; yi:=y^-1;
  pos:=NewDictionary(elts[1],true);
  for i in [1..n] do AddDictionary(pos,elts[i],i); od;
  posOf:=v->LookupDictionary(pos,v);
  to1:=[2,1,5,6,3,4]; to2:=[3,4,1,2,6,5];
  mul1:=[one,x,one,one,xi*yi*c,y]; mul2:=[one,one,y,yi*xi*c,one,x];
  a1:=[]; a2:=[];
  for t in [1..6] do for i in [1..n] do d:=elts[i];
    a1[(t-1)*n+i]:=(to1[t]-1)*n+posOf(d*mul1[t]);
    a2[(t-1)*n+i]:=(to2[t]-1)*n+posOf(d*mul2[t]);
  od; od;
  return rec(s1:=PermList(a1),s2:=PermList(a2),elts:=elts,posOf:=posOf);
end;;
JoinStrings := function(xs,sep)
  local ans,i; if Length(xs)=0 then return ""; fi; ans:=xs[1];
  for i in [2..Length(xs)] do ans:=Concatenation(ans,sep,xs[i]); od;
  return ans;
end;;
ShiftPerm := function(p,offset,size)
  local images,j; images:=[1..offset+size];
  for j in [1..size] do images[offset+j]:=offset+(j^p); od;
  return PermList(images);
end;;
DirectSumPerm := function(p,psize,q,qsize)
  return p*ShiftPerm(q,psize,qsize);
end;;
BlockRestrict := function(p,offset,size)
  local images,j; images:=[];
  for j in [1..size] do images[j]:=(offset+j)^p-offset; od;
  if Set(images)<>[1..size] then Error("calibration normal-form block failure"); fi;
  return PermList(images);
end;;
D9Coordinates := function(p)
  local r,s,a,e; r:=PermList([2,3,4,5,6,7,8,9,1]);
  s:=PermList([1,9,8,7,6,5,4,3,2]);
  for a in [0..8] do for e in [0..1] do if p=r^a*s^e then return [a,e]; fi; od; od;
  Error("calibration D9 normal form failure");
end;;
TargetKey := function(m,p27,p9)
  local coords,i,oneLine; coords:=[];
  for i in [0..2] do Append(coords,D9Coordinates(BlockRestrict(p27,9*i,9))); od;
  oneLine:=List([1..9],i->i^p9);
  return Concatenation("(",String(m mod 18),";",JoinStrings(List(coords,String),","),
    ";",JoinStrings(List(oneLine,String),","),")");
end;;
Scan := function(label,P,s1,s2,rho,targetKeys,qt9,qt4,off9,G9,P4)
  local x,y,c,D,dElts,Nord,charming,counts,m,u,fpos,f,h33,h34,hexCount,
        h33Count,h34Count,img1,img2,hom,settled,settledCount,unsettledCount,
        settledCayley,settledSchreier,syncErrors,qf,i9,i4,key,keyPos,shadowCount;
  if s1*s2*s1<>s2*s1*s2 or rho=fail or not IsSurjective(rho) then
    Error("calibration marked factor gate failed");
  fi;
  x:=s1^2; y:=s2^2; c:=PaperProd([s1,s2,s1])^2;
  D:=DerivedSubgroup(Group(x,y)); dElts:=Elements(D);
  Nord:=Lcm(Order(x),Order(y),Order(c));
  charming:=Filtered([0..Nord-1],m->Gcd(2*m+1,Nord)=1);
  counts:=List(targetKeys,k->0); h33Count:=0; h34Count:=0; hexCount:=0;
  shadowCount:=0; settledCount:=0; unsettledCount:=0; syncErrors:=0;
  for m in charming do u:=2*m+1;
    for fpos in [1..Length(dElts)] do f:=dElts[fpos];
      h33:=PaperProd([s1^u,f^-1,s2^u,f])=PaperProd([f^-1,s1,s2,x^(-m),c^m]);
      h34:=PaperProd([f^-1,s2^u,f,s1^u])=PaperProd([s2,s1,y^(-m),c^m,f]);
      if h33 then h33Count:=h33Count+1; fi;
      if h34 then h34Count:=h34Count+1; fi;
      if h33 and h34 then hexCount:=hexCount+1;
        img1:=s1^u; img2:=PaperProd([f^-1,s2^u,f]);
        if Size(Group(img1,img2))=Size(P) then
          hom:=GroupHomomorphismByImages(P,P,[s1,s2],[img1,img2]);
          if hom=fail then settledCayley:=false; settledSchreier:=false;
          else settledCayley:=Size(Image(hom))=Size(P);
            settledSchreier:=Index(P,Image(hom))=1;
          fi;
          if settledCayley<>settledSchreier then syncErrors:=syncErrors+1; fi;
          settled:=settledCayley and settledSchreier;
          if settled then settledCount:=settledCount+1; else unsettledCount:=unsettledCount+1; fi;
          qf:=Image(rho,f);
          i9:=qt9.posOf(One(G9))^qf;
          i4:=(off9+qt4.posOf(One(P4)))^qf-off9;
          if i9<1 or i9>Length(qt9.elts) or i4<1 or i4>Length(qt4.elts) then
            Error("calibration pure block reduction failed");
          fi;
          key:=TargetKey(m,qt9.elts[i9],qt4.elts[i4]); keyPos:=Position(targetKeys,key);
          if keyPos=fail then Error("calibration target escaped frozen set"); fi;
          counts[keyPos]:=counts[keyPos]+1; shadowCount:=shadowCount+1;
          Print("D972_CAL_ROW ",label," ",m," ",fpos-1," ",keyPos-1," ",settled,"\\n");
        fi;
      fi;
    od;
  od;
  Print("D972_CAL_SUMMARY ",label," ",Size(P)," ",Size(Kernel(rho))," ",Nord," ",
    Size(D)," ",Length(charming)," ",Length(charming)*Size(D)," ",h33Count," ",
    h34Count," ",hexCount," ",shadowCount," ",settledCount," ",unsettledCount," ",
    syncErrors,"\\n");
  Print("D972_CAL_FIBERS ",label," ",JoinStrings(List(counts,String),","),"\\n");
end;;
x9:=PermList([2,3,4,5,6,7,8,9,1,10,18,17,16,15,14,13,12,11,19,27,26,25,24,23,22,21,20]);;
y9:=PermList([2,1,9,8,7,6,5,4,3,11,12,13,14,15,16,17,18,10,20,19,27,26,25,24,23,22,21]);;
G9:=Group(x9,y9);;
x4:=PermList([8,5,2,1,9,7,4,3,6]);;
y4:=PermList([2,6,7,5,8,4,1,9,3]);;
P4:=Group(x4,y4);;
if Size(G9)<>2916 or Size(P4)<>504 then Error("calibration fixed base drift"); fi;
qt9:=CheckerQT(G9,x9,y9,());; qt4:=CheckerQT(P4,x4,y4,());;
off9:=6*Size(G9);; size4:=6*Size(P4);; baseDegree:=off9+size4;;
bs1:=DirectSumPerm(qt9.s1,off9,qt4.s1,size4);;
bs2:=DirectSumPerm(qt9.s2,off9,qt4.s2,size4);; BQ:=Group(bs1,bs2);;
if Size(BQ)<>8817984 then Error("calibration base order drift"); fi;
FQ:=FreeGroup(2,"r");; Q:=FQ/MakeRels(FQ,{qrels});; qg:=GeneratorsOfGroup(Q);;
qToBase:=GroupHomomorphismByImages(Q,BQ,qg,[bs1,bs2]);;
if qToBase=fail or not IsBijective(qToBase) then Error("calibration presentation/base mismatch"); fi;
targetKeys:={targets};;
if Length(targetKeys)<>972 or Length(Set(targetKeys))<>972 then Error("calibration target set drift"); fi;
rhoBase:=GroupHomomorphismByImages(BQ,BQ,[bs1,bs2],[bs1,bs2]);;
Scan("k1_base",BQ,bs1,bs2,rhoBase,targetKeys,qt9,qt4,off9,G9,P4);;
RunSmall := function(label,H,hx,hy,hc)
  local qt,S,eps,s1,s2,P,rho;
  qt:=CheckerQT(H,hx,hy,hc); S:=Group(qt.s1,qt.s2);
  eps:=GroupHomomorphismByImages(S,SymmetricGroup(3),[qt.s1,qt.s2],[(1,2),(2,3)]);
  if Size(S)<>6*Size(H) or eps=fail or not IsSurjective(eps) or Size(Kernel(eps))<>Size(H) then
    Error("calibration small marked factor drift");
  fi;
  s1:=DirectSumPerm(bs1,baseDegree,qt.s1,6*Size(H));
  s2:=DirectSumPerm(bs2,baseDegree,qt.s2,6*Size(H)); P:=Group(s1,s2);
  rho:=GroupHomomorphismByImages(P,BQ,[s1,s2],[bs1,bs2]);
  if Size(P)<>2*Size(BQ) or rho=fail or not IsSurjective(rho) or Size(Kernel(rho))<>2 then
    Error("calibration diagonal kernel drift");
  fi;
  Scan(label,P,s1,s2,rho,targetKeys,qt9,qt4,off9,G9,P4);
end;;
C2:=Group((1,2));; z2:=(1,2);;
RunSmall("split_c2",C2,z2,z2,z2);;
qx:=PermList([3,4,2,1,7,8,6,5]);;
qy:=PermList([5,6,8,7,2,1,3,4]);; Q8:=Group(qx,qy);; qz:=qx^2;;
if Size(Q8)<>8 or Order(qx)<>4 or Order(qy)<>4 or qx^2<>qy^2 then Error("calibration Q8 drift"); fi;
RunSmall("nonsplit_q8_c0",Q8,qx,qy,One(Q8));;
RunSmall("nonsplit_q8_c1",Q8,qx,qy,qz);;
QUIT_GAP(0);
"""


def parse_independent_calibration(
    stdout: str, stderr: str, script: str, command_mode: str,
    q_relators: Any, target_keys: list[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    labels = ("k1_base", "split_c2", "nonsplit_q8_c0", "nonsplit_q8_c1")
    summaries: dict[str, list[int]] = {}
    fibers: dict[str, list[int]] = {}
    rows: dict[str, list[list[Any]]] = {label: [] for label in labels}
    for line in stdout.splitlines():
        parts = line.split()
        if parts[:1] == ["D972_CAL_ROW"]:
            require(len(parts) == 6 and parts[1] in rows and parts[5] in {"true", "false"},
                    "STATE_STOP malformed independent calibration row")
            rows[parts[1]].append([
                int(parts[2]), int(parts[3]), int(parts[4]), parts[5] == "true",
            ])
        elif parts[:1] == ["D972_CAL_SUMMARY"]:
            require(len(parts) == 15 and parts[1] in rows and parts[1] not in summaries,
                    "STATE_STOP malformed independent calibration summary")
            summaries[parts[1]] = [int(value) for value in parts[2:]]
        elif line.startswith("D972_CAL_FIBERS "):
            head, vector = line.rsplit(" ", 1)
            label = head.split()[1]
            require(label in rows and label not in fibers,
                    "STATE_STOP duplicate/unknown calibration fiber vector")
            fibers[label] = [int(value) for value in vector.split(",")]
    require(set(summaries) == set(fibers) == set(rows) == set(labels),
            "STATE_STOP incomplete independent calibration output")
    models: dict[str, dict[str, Any]] = {}
    for label in labels:
        summary = summaries[label]
        require(len(summary) == 13, "STATE_STOP calibration summary arity")
        (p_order, kernel_order, n_ord, derived_order, charming_count, pair_universe,
         h33_count, h34_count, hex_count, shadow_count, settled_count,
         unsettled_count, sync_errors) = summary
        require(len(fibers[label]) == 972 and
                all(isinstance(value, int) and value >= 0 for value in fibers[label]),
                "STATE_STOP calibration fiber-vector shape")
        accepted = rows[label]
        require(len({tuple(row) for row in accepted}) == len(accepted) and
                all(0 <= row[2] < 972 and row[3] is True for row in accepted),
                "STATE_STOP duplicate/unsettled independent calibration row")
        rebuilt = [0] * 972
        for _, _, target_index, _ in accepted:
            rebuilt[target_index] += 1
        require(rebuilt == fibers[label] and shadow_count == len(accepted) == sum(rebuilt) and
                settled_count == shadow_count and unsettled_count == 0 and sync_errors == 0 and
                pair_universe == charming_count * derived_order and
                h33_count >= hex_count >= shadow_count and h34_count >= hex_count,
                "STATE_STOP independent calibration counters disagree")
        expected_p = 8_817_984 if label == "k1_base" else 17_635_968
        expected_kernel = 1 if label == "k1_base" else 2
        require(p_order == expected_p and kernel_order == expected_kernel,
                "STATE_STOP independent calibration order/kernel mismatch")
        positive = sorted(set(rebuilt) - {0})
        histogram = [
            {"fiber_size": size, "target_count": sum(value == size for value in rebuilt)}
            for size in positive
        ]
        models[label] = {
            "label": label, "p_order": p_order, "kernel_order": kernel_order,
            "n_ord": n_ord, "derived_order": derived_order,
            "charming_count": charming_count, "pair_universe": pair_universe,
            "hexagon_3_3_pass_count": h33_count,
            "hexagon_3_4_pass_count": h34_count,
            "full_hexagon_pair_count": hex_count,
            "accepted_rows": accepted,
            "accepted_rows_sha256": sha_bytes(canonical_bytes(accepted)),
            "fiber_counts": rebuilt,
            "fiber_vector_sha256": sha_bytes(canonical_bytes(rebuilt)),
            "image_size": sum(value > 0 for value in rebuilt),
            "zero_count": sum(value == 0 for value in rebuilt),
            "fiber_histogram": histogram,
        }
    cases = {
        "k1_base": calibration_observation({
            "marked_orbit_count": 1,
            "gt_orders": [len(models["k1_base"]["accepted_rows"])],
            "image_sizes": [models["k1_base"]["image_size"]],
            "zero_fiber_counts": [models["k1_base"]["zero_count"]],
            "fiber_histograms": [models["k1_base"]["fiber_histogram"]],
        }),
        "k2_three_marked_orbits": calibration_observation({
            "marked_orbit_count": 3,
            "gt_orders": [len(models[label]["accepted_rows"]) for label in labels[1:]],
            "image_sizes": [models[label]["image_size"] for label in labels[1:]],
            "zero_fiber_counts": [models[label]["zero_count"] for label in labels[1:]],
            "fiber_histograms": [models[label]["fiber_histogram"] for label in labels[1:]],
        }),
    }
    receipt = {
        "schema": "d972-independent-calibration/v2",
        "status": "PASS",
        "backend": CALIBRATION_BACKEND,
        "command_mode": command_mode,
        "script_sha256": sha_bytes(script.encode("ascii")),
        "stdout_sha256": sha_bytes(stdout.encode("utf-8")),
        "stderr_sha256": sha_bytes(stderr.encode("utf-8")),
        "q_relators_sha256": sha_bytes(canonical_bytes(q_relators)),
        "target_key_count": len(target_keys),
        "target_key_order_sha256": sha_bytes(("\n".join(target_keys) + "\n").encode()),
        "classification": marked_c2_classification(),
        "models": [models[label] for label in labels],
        "case_observations": cases,
        "producer_metrics_used_as_input": False,
        "search_unlock_authority": True,
    }
    receipt["receipt_sha256"] = sha_bytes(canonical_bytes(receipt))
    return cases, receipt


def compare_calibration_gate(
    gate: dict[str, Any], independent: dict[str, dict[str, Any]], legacy: Any,
) -> dict[str, Any]:
    checked = copy.deepcopy(gate)
    require({case.get("case_id") for case in checked.get("cases", [])} == set(independent),
            "STATE_STOP calibration case universe mismatch")
    for case in checked["cases"]:
        case_id = case["case_id"]
        observation = copy.deepcopy(independent[case_id])
        expected = case["expected"]
        producer = case.get("producer")
        legacy.require_disagreement(isinstance(producer, dict),
                                    "producer calibration observation absent")
        producer_body = {key: producer.get(key) for key in CALIBRATION_METRICS}
        legacy.require_disagreement(
            producer.get("receipt_sha256") == sha_bytes(canonical_bytes(producer_body)),
            "producer calibration observation digest mismatch",
        )
        independent_body = {key: observation[key] for key in CALIBRATION_METRICS}
        legacy.require_disagreement(
            independent_body == expected == producer_body,
            "independent/producer/frozen calibration disagreement",
        )
        case["checker"] = observation
        case["agreed"] = True
    checked["status"] = "PASSED"
    checked["search_unlocked"] = True
    checked["producer_checker_agree"] = True
    return checked


def validate_independent_calibration_receipt(
    receipt: Any, gate: dict[str, Any], state: dict[str, Any] | None = None,
) -> None:
    require(isinstance(receipt, dict) and
            receipt.get("schema") == "d972-independent-calibration/v2" and
            receipt.get("status") == "PASS" and
            receipt.get("producer_metrics_used_as_input") is False and
            receipt.get("search_unlock_authority") is True,
            "STATE_STOP independent v2 calibration receipt absent")
    body = copy.deepcopy(receipt)
    claimed = body.pop("receipt_sha256", None)
    require(claimed == sha_bytes(canonical_bytes(body)),
            "STATE_STOP independent calibration receipt digest")
    require(receipt.get("backend") == CALIBRATION_BACKEND and
            receipt.get("command_mode") == "posix-gap-cli" and
            all(is_sha(receipt.get(key)) for key in (
                "script_sha256", "stdout_sha256", "stderr_sha256", "q_relators_sha256",
                "target_key_order_sha256",
            )) and
            receipt.get("target_key_order_sha256") == CALIBRATION_TARGET_KEY_SHA256,
            "STATE_STOP calibration backend/raw-output bindings")
    if state is not None:
        q_relators = state.get("receipts", {}).get("producer_preflight", {}).get(
            "worker", {}
        ).get("q_relators")
        require(receipt.get("q_relators_sha256") == sha_bytes(canonical_bytes(q_relators)),
                "STATE_STOP calibration base-presentation receipt drift")
    paper = receipt.get("classification", {}).get("paper_premise", {})
    require(CALIBRATION_PAPER.is_file() and sha_file(CALIBRATION_PAPER) == CALIBRATION_PAPER_SHA256 and
            paper.get("sha256") == CALIBRATION_PAPER_SHA256 and
            receipt.get("classification") == marked_c2_classification(),
            "STATE_STOP calibration paper-premise binding drift")
    models = receipt.get("models")
    require(isinstance(models, list) and len(models) == 4 and
            receipt.get("target_key_count") == 972,
            "STATE_STOP calibration lossless model receipt shape")
    by_label: dict[str, dict[str, Any]] = {}
    for model in models:
        require(isinstance(model, dict) and isinstance(model.get("label"), str) and
                model["label"] not in by_label,
                "STATE_STOP duplicate calibration model label")
        by_label[model["label"]] = model
        rows = model.get("accepted_rows")
        vector = model.get("fiber_counts")
        require(isinstance(rows, list) and isinstance(vector, list) and len(vector) == 972 and
                model.get("accepted_rows_sha256") == sha_bytes(canonical_bytes(rows)) and
                model.get("fiber_vector_sha256") == sha_bytes(canonical_bytes(vector)),
                "STATE_STOP calibration raw row/vector binding")
        rebuilt = [0] * 972
        for row in rows:
            require(isinstance(row, list) and len(row) == 4 and
                    all(isinstance(value, int) for value in row[:3]) and row[3] is True and
                    0 <= row[2] < 972,
                    "STATE_STOP calibration accepted row shape")
            rebuilt[row[2]] += 1
        positive = sorted(set(rebuilt) - {0})
        histogram = [
            {"fiber_size": size, "target_count": sum(value == size for value in rebuilt)}
            for size in positive
        ]
        require(rebuilt == vector and model.get("image_size") == sum(value > 0 for value in rebuilt) and
                model.get("zero_count") == sum(value == 0 for value in rebuilt) and
                model.get("fiber_histogram") == histogram,
                "STATE_STOP calibration row/vector/metric mismatch")
    labels = ("k1_base", "split_c2", "nonsplit_q8_c0", "nonsplit_q8_c1")
    require(set(by_label) == set(labels), "STATE_STOP calibration model universe")
    require(all(
        by_label[label].get("p_order") == (8_817_984 if label == "k1_base" else 17_635_968)
        and by_label[label].get("kernel_order") == (1 if label == "k1_base" else 2)
        for label in labels
    ), "STATE_STOP calibration persisted model order/kernel drift")
    derived = {
        "k1_base": calibration_observation({
            "marked_orbit_count": 1,
            "gt_orders": [len(by_label[labels[0]]["accepted_rows"])],
            "image_sizes": [by_label[labels[0]]["image_size"]],
            "zero_fiber_counts": [by_label[labels[0]]["zero_count"]],
            "fiber_histograms": [by_label[labels[0]]["fiber_histogram"]],
        }),
        "k2_three_marked_orbits": calibration_observation({
            "marked_orbit_count": 3,
            "gt_orders": [len(by_label[label]["accepted_rows"]) for label in labels[1:]],
            "image_sizes": [by_label[label]["image_size"] for label in labels[1:]],
            "zero_fiber_counts": [by_label[label]["zero_count"] for label in labels[1:]],
            "fiber_histograms": [by_label[label]["fiber_histogram"] for label in labels[1:]],
        }),
    }
    observations = receipt.get("case_observations", {})
    require(observations == derived, "STATE_STOP calibration model/observation mismatch")
    producer_bindings = receipt.get("producer_observation_receipts", {})
    for case in gate.get("cases", []):
        observed = observations.get(case.get("case_id"))
        require(case.get("agreed") is True and isinstance(observed, dict) and
                observed == case.get("checker") and
                producer_bindings.get(case.get("case_id")) ==
                case.get("producer", {}).get("receipt_sha256") and
                observed.get("receipt_sha256") ==
                sha_bytes(canonical_bytes({key: observed[key] for key in CALIBRATION_METRICS})),
                "STATE_STOP calibration gate/receipt observation mismatch")


def envelope_hash(envelope: dict[str, Any]) -> str:
    body = copy.deepcopy(envelope)
    body["hash_chain"]["envelope_sha256"] = ZERO_SHA
    return sha_bytes(canonical_bytes(body))


def relative_files(directory: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((p for p in directory.rglob("*") if p.is_file()),
                       key=lambda p: p.relative_to(directory).as_posix()):
        relative = path.relative_to(directory).as_posix()
        # The envelope is stored outside ckpt_dir by the workflow.  Refuse it
        # here too so its self-hash can never enter the image-set digest.
        require(not relative.endswith("pending-envelope.json"),
                "STATE_STOP envelope must be outside checkpoint image directory")
        rows.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha_file(path)})
    return rows


def image_set_digest(rows: Iterable[dict[str, Any]]) -> str:
    material = "".join(
        f"{row['path']}\t{row['bytes']}\t{row['sha256']}\n" for row in rows
    ).encode("utf-8")
    return sha_bytes(material)


def checkpoint_generation_dir(path: Path) -> tuple[Path, str]:
    resolved = path.resolve()
    base = (ROOT / ".d972-runtime" / "ckpt").resolve()
    require(resolved.parent == base and re.fullmatch(r"g[0-9]{6}", resolved.name) is not None,
            "STATE_STOP checkpoint path is not one direct campaign generation")
    return resolved, resolved.relative_to(ROOT).as_posix()


def external_runtime_files(runtime_root: Path) -> list[dict[str, Any]]:
    """Hash every non-DMTCP file the restored Python/GAP tree may consume."""
    candidates: list[Path] = []
    for name in (
        "state.json", "campaign-meta.json", "launch-environment.json", "current-run.json",
        FINAL_A_SEAL_NAME,
    ):
        path = runtime_root / name
        if path.is_file():
            candidates.append(path)
    # Atomic JSON writers create root-local ``name.random.tmp`` files and may
    # be checkpointed after fsync but before os.replace.  They are process
    # state, unlike pending/inflight/coordinator supervisor files.
    candidates.extend(path for path in runtime_root.glob("*.tmp") if path.is_file())
    for name in ("artifacts", "checker", "home", "tmp"):
        directory = runtime_root / name
        if directory.is_dir():
            candidates.extend(path for path in directory.rglob("*") if path.is_file())
    rows = []
    for path in sorted(set(candidates), key=lambda item: item.relative_to(runtime_root).as_posix()):
        rows.append({
            "path": path.relative_to(runtime_root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha_file(path),
        })
    return rows


def runtime_from_environment() -> dict[str, Any]:
    required = {
        "dmtcp_version": "D972_DMTCP_VERSION",
        "gap_version": "D972_GAP_VERSION",
        "python_version": "D972_PYTHON_VERSION",
        "runner_image_os": "ImageOS",
        "runner_arch": "RUNNER_ARCH",
        "workspace_realpath": "D972_WORKSPACE_REALPATH",
    }
    values = {name: os.environ.get(variable, "").strip() for name, variable in required.items()}
    missing = [name for name, value in values.items() if not value]
    require(not missing, "STATE_STOP runtime metadata absent: " + ",".join(missing))
    require(Path(values["workspace_realpath"]).resolve() == ROOT.resolve(),
            "STATE_STOP workspace path is not stable campaign root")
    return values


def load_parent_digest(path: Path | None, campaign_id: str) -> tuple[int, str | None]:
    if path is None:
        return 0, None
    parent = json.loads(path.read_text(encoding="utf-8"))
    require(parent.get("schema") == "d972-dovetail-dmtcp-envelope/v2",
            "STATE_STOP parent envelope schema")
    require(parent.get("campaign_id") == campaign_id,
            "STATE_STOP parent envelope campaign")
    require(parent.get("hash_chain", {}).get("envelope_sha256") == envelope_hash(parent),
            "STATE_STOP parent envelope digest")
    return int(parent["hash_chain"]["generation"]) + 1, parent["hash_chain"]["envelope_sha256"]


def seal_envelope(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    state = json.loads(args.state.read_text(encoding="utf-8"))
    validate_v2_state_binding(state, manifest)
    ckpt_dir, ckpt_relative = checkpoint_generation_dir(args.checkpoint_dir)
    require(ckpt_dir.is_dir(), "STATE_STOP checkpoint directory absent")
    rows = relative_files(ckpt_dir)
    require(any(row["path"].endswith(".dmtcp") for row in rows),
            "STATE_STOP no DMTCP process image")
    require(any(Path(row["path"]).name == "dmtcp_restart_script.sh" for row in rows),
            "STATE_STOP DMTCP restart script absent")
    generation, parent_sha = load_parent_digest(args.parent_envelope, manifest["campaign_id"])
    if args.generation is not None:
        require(args.generation == generation, "STATE_STOP requested generation mismatch")
    require(ckpt_relative == f".d972-runtime/ckpt/g{generation:06d}",
            "STATE_STOP checkpoint directory/generation mismatch")
    runtime = runtime_from_environment()
    external_rows = external_runtime_files(args.state.resolve().parent)
    contract_sha = manifest["dmtcp_contract"]["contract_sha256"]
    require(os.environ.get("D972_DMTCP_CONTRACT_SHA256") == contract_sha,
            "STATE_STOP contract environment mismatch")
    launch_spec = manifest["launch_spec"]
    launch_environment = json.loads(args.launch_environment.read_text(encoding="utf-8"))
    require(isinstance(launch_environment, dict) and
            set(launch_environment) == set(launch_spec["environment_allowlist"]),
            "STATE_STOP checkpointed environment is not the exact allowlist")
    require(all(isinstance(value, str) for value in launch_environment.values()),
            "STATE_STOP checkpointed environment value type")
    forbidden = ("TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "AUTH")
    require(not any(any(fragment in key.upper() for fragment in forbidden)
                    for key in launch_environment),
            "STATE_STOP secret-like variable entered checkpoint environment")
    status_sha = sha_file(args.coordinator_status)
    envelope: dict[str, Any] = {
        "schema": "d972-dovetail-dmtcp-envelope/v2",
        "state_kind": "SUSPENDED_PROCESS_TREE",
        "campaign_id": manifest["campaign_id"],
        "source": {
            "repository": os.environ.get("GITHUB_REPOSITORY", "local"),
            "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
            "run_attempt": int(os.environ.get("GITHUB_RUN_ATTEMPT", "0")),
            "commit_sha": os.environ.get("D972_SOURCE_COMMIT", "").lower(),
        },
        "runtime": runtime,
        "contract": {
            "dmtcp_contract_sha256": contract_sha,
            "launch_spec_sha256": sha_bytes(canonical_bytes(launch_spec)),
            "v2_binding_set_sha256":
                state["receipts"]["v2_runtime_integrity"]["binding_set_sha256"],
            "coordinator_status_sha256": status_sha,
            "launch_environment_sha256": sha_bytes(canonical_bytes(launch_environment)),
            "run_metadata_sha256": sha_file(args.run_metadata),
        },
        "input_state": {
            "path": args.state.name,
            "checkpoint_sha256": state["hash_chain"]["checkpoint_sha256"],
            "file_sha256": sha_file(args.state),
        },
        "checkpoint_images": {
            "directory": ckpt_relative,
            "file_count": len(rows),
            "files": rows,
            "set_sha256": image_set_digest(rows),
        },
        "external_runtime_files": {
            "file_count": len(external_rows),
            "files": external_rows,
            "set_sha256": image_set_digest(external_rows),
        },
        "launch_environment": launch_environment,
        "hash_chain": {
            "algorithm": "sha256",
            "generation": generation,
            "parent_envelope_sha256": parent_sha,
            "envelope_sha256": ZERO_SHA,
        },
        "sealed_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "terminal_authority": False,
        "resume_only": True,
    }
    commit = envelope["source"]["commit_sha"]
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
            "STATE_STOP source commit absent/malformed")
    envelope["hash_chain"]["envelope_sha256"] = envelope_hash(envelope)
    atomic_json(args.envelope, envelope)
    print(f"SEALED {envelope['hash_chain']['envelope_sha256']}")
    return 0


def verify_envelope(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    envelope = json.loads(args.envelope.read_text(encoding="utf-8"))
    require(envelope.get("schema") == "d972-dovetail-dmtcp-envelope/v2" and
            envelope.get("state_kind") == "SUSPENDED_PROCESS_TREE",
            "STATE_STOP envelope schema/state kind")
    require(envelope.get("campaign_id") == manifest["campaign_id"],
            "STATE_STOP envelope campaign mismatch")
    require(envelope.get("terminal_authority") is False and
            envelope.get("resume_only") is True,
            "STATE_STOP a checkpoint image acquired terminal authority")
    require(envelope.get("hash_chain", {}).get("envelope_sha256") == envelope_hash(envelope),
            "STATE_STOP envelope digest mismatch")
    claimed_parent_sha = envelope["hash_chain"].get("parent_envelope_sha256")
    if args.parent_envelope is not None:
        parent = json.loads(args.parent_envelope.read_text(encoding="utf-8"))
        require(parent.get("schema") == "d972-dovetail-dmtcp-envelope/v2" and
                parent.get("campaign_id") == manifest["campaign_id"] and
                parent.get("hash_chain", {}).get("envelope_sha256") == envelope_hash(parent),
                "STATE_STOP predecessor lineage envelope invalid")
        require(envelope["hash_chain"]["parent_envelope_sha256"] ==
                parent.get("hash_chain", {}).get("envelope_sha256") and
                envelope["hash_chain"]["generation"] ==
                int(parent.get("hash_chain", {}).get("generation", -2)) + 1,
                "STATE_STOP envelope lineage mismatch")
    else:
        require(claimed_parent_sha is None and envelope["hash_chain"].get("generation") == 0,
                "STATE_STOP non-genesis envelope omitted its predecessor")
    current_commit = os.environ.get("D972_SOURCE_COMMIT", "").lower()
    require(envelope["source"]["commit_sha"] == current_commit,
            "STATE_STOP resume commit differs from image source commit")
    runtime = runtime_from_environment()
    compatibility_keys = {
        "dmtcp_version", "gap_version", "python_version", "runner_arch",
        "runner_image_os", "workspace_realpath",
    }
    require(all(envelope["runtime"].get(key) == runtime.get(key)
                for key in compatibility_keys),
            "STATE_STOP DMTCP/GAP/Python/arch/path compatibility drift")
    contract_sha = manifest["dmtcp_contract"]["contract_sha256"]
    require(envelope["contract"]["dmtcp_contract_sha256"] == contract_sha and
            envelope["contract"]["launch_spec_sha256"] ==
            sha_bytes(canonical_bytes(manifest["launch_spec"])),
            "STATE_STOP resume contract/command drift")
    require(envelope["contract"].get("run_metadata_sha256") == sha_file(args.run_metadata),
            "STATE_STOP suspended run metadata drift")
    launch_environment = json.loads(args.launch_environment.read_text(encoding="utf-8"))
    require(envelope.get("launch_environment") == launch_environment and
            envelope["contract"].get("launch_environment_sha256") ==
            sha_bytes(canonical_bytes(launch_environment)) and
            set(launch_environment) == set(manifest["launch_spec"]["environment_allowlist"]),
            "STATE_STOP checkpointed launch environment drift")
    state = json.loads(args.state.read_text(encoding="utf-8"))
    validate_v2_state_binding(state, manifest)
    require(envelope["input_state"] == {
        "path": args.state.name,
        "checkpoint_sha256": state["hash_chain"]["checkpoint_sha256"],
        "file_sha256": sha_file(args.state),
    }, "STATE_STOP input state drift under process image")
    ckpt_dir, claimed_directory = checkpoint_generation_dir(args.checkpoint_dir)
    generation = envelope["hash_chain"].get("generation")
    require(isinstance(generation, int) and
            claimed_directory == f".d972-runtime/ckpt/g{generation:06d}",
            "STATE_STOP sealed checkpoint directory/generation mismatch")
    rows = relative_files(ckpt_dir)
    claimed = envelope["checkpoint_images"]
    require(claimed.get("directory") == claimed_directory,
            "STATE_STOP checkpoint directory differs from sealed generation")
    require(claimed["files"] == rows and claimed["file_count"] == len(rows) and
            claimed["set_sha256"] == image_set_digest(rows),
            "STATE_STOP checkpoint image set changed")
    external_rows = external_runtime_files(args.state.resolve().parent)
    external_claim = envelope.get("external_runtime_files", {})
    require(external_claim.get("files") == external_rows and
            external_claim.get("file_count") == len(external_rows) and
            external_claim.get("set_sha256") == image_set_digest(external_rows),
            "STATE_STOP resume-critical external runtime files changed")
    require(envelope["contract"]["v2_binding_set_sha256"] ==
            state["receipts"]["v2_runtime_integrity"]["binding_set_sha256"],
            "STATE_STOP checkpoint/code binding mismatch")
    print(f"VERIFIED_RESUME {envelope['hash_chain']['envelope_sha256']}")
    return 0


def load_legacy() -> Any:
    spec = importlib.util.spec_from_file_location("d972_checker_v1_lib", LEGACY_PATH)
    require(spec is not None and spec.loader is not None,
            "STATE_STOP independent v1 checker unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def final_a_seal_hash(seal: dict[str, Any]) -> str:
    body = copy.deepcopy(seal)
    body["seal_sha256"] = ZERO_SHA
    return sha_bytes(canonical_bytes(body))


def final_a_expected(
    state: dict[str, Any], bound: dict[str, Any], manifest: dict[str, Any],
    source_commit: str, state_file_sha256: str,
) -> dict[str, Any]:
    witness = state.get("terminal_witness")
    require(state.get("status", {}).get("code") == "A_WITNESS_CROSSCHECKED" and
            state.get("status", {}).get("terminal") is True and
            isinstance(witness, dict),
            "STATE_STOP final-v2 seal requested for non-A state")
    require(bound.get("schema") == "d972_dovetail_worker/v2" and
            bound.get("mode") == "shadow-fiber" and
            bound.get("terminal_A_eligible") is True and
            is_sha(bound.get("checkpoint_sha256")),
            "STATE_STOP final-v2 seal lacks complete shadow receipt")
    require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
            "STATE_STOP final-v2 source commit malformed")
    require(is_sha(state_file_sha256), "STATE_STOP final-v2 state file digest malformed")
    summary = state.get("receipts", {}).get("checker_summary")
    require(isinstance(summary, dict), "STATE_STOP final-v2 checker summary absent")
    calibration = state.get("receipts", {}).get("independent_calibration_checker_v2")
    require(isinstance(calibration, dict) and is_sha(calibration.get("receipt_sha256")),
            "STATE_STOP final-v2 calibration receipt absent")
    seal = {
        "schema": "d972-final-a-completion/v2",
        "campaign_id": manifest["campaign_id"],
        "source_commit": source_commit,
        "state_checkpoint_sha256": state["hash_chain"]["checkpoint_sha256"],
        "state_file_sha256": state_file_sha256,
        "terminal_witness_sha256": sha_bytes(canonical_bytes(witness)),
        "candidate_id": witness.get("candidate_id"),
        "matching_shadow_receipt_sha256": bound["checkpoint_sha256"],
        "producer_ledger_sha256": state["ledgers"]["producer"]["sha256"],
        "checker_summary_sha256": sha_bytes(canonical_bytes(summary)),
        "calibration_receipt_sha256": calibration["receipt_sha256"],
        "v2_binding_set_sha256":
            state["receipts"]["v2_runtime_integrity"]["binding_set_sha256"],
        "dmtcp_contract_sha256": manifest["dmtcp_contract"]["contract_sha256"],
        "independent_checker_complete": True,
        "pending_process_image_authority": False,
        "terminal_authority": "A_AFTER_V2_POSTCHECK_ONLY",
        "seal_sha256": ZERO_SHA,
    }
    seal["seal_sha256"] = final_a_seal_hash(seal)
    return seal


def find_terminal_shadow_binding(
    state: dict[str, Any], producer_ledger: Path, manifest: dict[str, Any],
) -> dict[str, Any]:
    witness = state.get("terminal_witness", {})
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    require(producer_ledger.is_file(), "STATE_STOP final-v2 producer ledger absent")
    claimed = state.get("ledgers", {}).get("producer", {})
    lines = [line for line in producer_ledger.read_text(encoding="utf-8").splitlines()
             if line.strip()]
    require(claimed.get("sha256") == sha_file(producer_ledger) and
            claimed.get("record_count") == len(lines),
            "STATE_STOP final-v2 producer ledger digest/count mismatch")
    for line in lines:
        row = json.loads(line)
        if row.get("candidate_id") != witness.get("candidate_id"):
            continue
        shadow_receipts = collect_worker_receipts(row.get("shadow_receipt", {}))
        for receipt in shadow_receipts:
            validate_worker_receipt(receipt, manifest)
        matches.extend((receipt, row) for receipt in shadow_receipts)
    require(len(matches) == 1 and matches[0][0].get("terminal_A_eligible") is True and
            sha_bytes(canonical_bytes(matches[0][1])) == witness.get("producer_digest"),
            "STATE_STOP final-v2 unique terminal shadow binding absent")
    return matches[0][0]


def write_final_a_seal(
    state_path: Path, producer_ledger: Path, manifest: dict[str, Any], bound: dict[str, Any],
) -> None:
    state = json.loads(state_path.read_text(encoding="utf-8"))
    validate_v2_state_binding(state, manifest)
    observed_bound = find_terminal_shadow_binding(state, producer_ledger, manifest)
    require(observed_bound.get("checkpoint_sha256") == bound.get("checkpoint_sha256"),
            "STATE_STOP final-v2 in-memory/ledger shadow binding mismatch")
    source_commit = os.environ.get("D972_SOURCE_COMMIT", "").lower()
    expected = final_a_expected(
        state, observed_bound, manifest, source_commit, sha_file(state_path)
    )
    seal_path = state_path.resolve().parent / FINAL_A_SEAL_NAME
    atomic_json(seal_path, expected)


def verify_final_a(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    require(not (args.state.resolve().parent / "pending-envelope.json").exists(),
            "STATE_STOP pending process image takes precedence over final A")
    state = json.loads(args.state.read_text(encoding="utf-8"))
    legacy = load_legacy()
    legacy.validate_state_core(state)
    validate_v2_state_binding(state, manifest)
    bound = find_terminal_shadow_binding(state, args.producer_ledger, manifest)
    expected = final_a_expected(
        state, bound, manifest, args.source_commit.lower(), sha_file(args.state)
    )
    observed = json.loads(args.seal.read_text(encoding="utf-8"))
    require(observed == expected and observed.get("seal_sha256") == final_a_seal_hash(observed),
            "STATE_STOP final-v2 A completion seal mismatch")
    print(f"VERIFIED_FINAL_A {observed['seal_sha256']}")
    return 0


def install_checkpointed_checker_adapter(legacy: Any, manifest: dict[str, Any]) -> None:
    """Install no-timeout GAP and the independent lossless calibration gate."""
    if os.environ.get("D972_CHECKER_DMTCP_ENABLED") != "1":
        return
    require(os.environ.get("D972_DMTCP_ENABLED") == "1" and
            os.environ.get("D972_DMTCP_CONTRACT_SHA256") ==
            manifest["dmtcp_contract"]["contract_sha256"],
            "STATE_STOP checker DMTCP contract absent")

    def run_isolated_gap_without_timeout(script: str, purpose: str) -> tuple[str, str, str]:
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="ascii", newline="\n", prefix="d972-independent-v2-",
            suffix=".g", delete=False,
        )
        script_path = Path(handle.name)
        try:
            with handle:
                handle.write(script)
                handle.flush()
                os.fsync(handle.fileno())
            command, command_mode = legacy.select_gap_command(script_path)
            completed = subprocess.run(
                command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                errors="replace", check=False,
            )
        except OSError as exc:
            raise legacy.CheckStop(
                f"STATE_STOP independent {purpose} UNKNOWN: {type(exc).__name__}"
            ) from exc
        finally:
            try:
                script_path.unlink()
            except FileNotFoundError:
                pass
        legacy.require(completed.returncode == 0,
                       f"STATE_STOP independent {purpose} UNKNOWN: GAP failed with exit "
                       f"{completed.returncode}")
        return completed.stdout, completed.stderr, command_mode

    legacy.run_isolated_gap = run_isolated_gap_without_timeout
    calibration_box: dict[str, Any] = {}
    original_atomic_json = legacy.atomic_json

    def independently_check_calibration_v2(state: dict[str, Any]) -> tuple[dict[str, Any], bool]:
        require(CALIBRATION_PAPER.is_file() and
                sha_file(CALIBRATION_PAPER) == CALIBRATION_PAPER_SHA256,
                "STATE_STOP pinned calibration paper premise drift")
        worker = state.get("receipts", {}).get("producer_preflight", {}).get("worker", {})
        q_relators = worker.get("q_relators")
        target_keys = legacy.canonical_target_keys()
        script = independent_calibration_gap_script(q_relators, target_keys)
        stdout, stderr, command_mode = legacy.run_isolated_gap(
            script, "k=1,2 lossless calibration reconstruction"
        )
        independent, receipt = parse_independent_calibration(
            stdout, stderr, script, command_mode, q_relators, target_keys
        )
        gate = compare_calibration_gate(state["calibration_gate"], independent, legacy)
        receipt["producer_observation_receipts"] = {
            case["case_id"]: case["producer"]["receipt_sha256"] for case in gate["cases"]
        }
        receipt_body = copy.deepcopy(receipt)
        receipt_body.pop("receipt_sha256", None)
        receipt["receipt_sha256"] = sha_bytes(canonical_bytes(receipt_body))
        # The atomic-json adapter below consumes this box in the same call stack
        # as v1's transition.  No PASSED state is ever written without the v2
        # lossless receipt, despite v1's obsolete transient BLOCKED template.
        calibration_box["receipt"] = receipt
        return gate, True

    def atomic_json_with_v2_calibration(path: Path, value: Any) -> None:
        receipt = calibration_box.get("receipt")
        if isinstance(value, dict) and isinstance(receipt, dict) and \
                value.get("calibration_gate", {}).get("status") == "PASSED":
            value["receipts"]["independent_calibration_checker"] = {
                "status": "PASS",
                "subcode": "V2_INDEPENDENT_LOSSLESS_CALIBRATION",
                "receipt_sha256": receipt["receipt_sha256"],
                "search_unlock_authority": True,
            }
            value["receipts"]["independent_calibration_checker_v2"] = copy.deepcopy(receipt)
            value["hash_chain"]["checkpoint_sha256"] = ZERO_SHA
            value["hash_chain"]["checkpoint_sha256"] = legacy.checkpoint_hash(value)
            validate_independent_calibration_receipt(
                value["receipts"]["independent_calibration_checker_v2"],
                value["calibration_gate"], value,
            )
            legacy.validate_state_core(value)
        original_atomic_json(path, value)

    legacy.independently_check_calibration = independently_check_calibration_v2
    legacy.atomic_json = atomic_json_with_v2_calibration


def run_campaign_checker(argv: Sequence[str]) -> int:
    manifest = load_manifest()
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--producer-ledger", type=Path)
    known, _ = parser.parse_known_args(argv)
    terminal_shadow_bindings: dict[str, dict[str, Any]] = {}
    if "--self-test" not in argv:
        require(known.state is not None and known.state.is_file(),
                "STATE_STOP checker state absent")
        state_before = json.loads(known.state.read_text(encoding="utf-8"))
        validate_v2_state_binding(state_before, manifest)
        final_path = known.state.resolve().parent / FINAL_A_SEAL_NAME
        require(not final_path.exists() or
                state_before.get("status", {}).get("code") == "A_WITNESS_CROSSCHECKED",
                "STATE_STOP stale final-v2 completion seal on non-A state")
        require(known.producer_ledger is not None and known.producer_ledger.is_file(),
                "STATE_STOP producer ledger absent")
        for number, line in enumerate(
            known.producer_ledger.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                continue
            row = json.loads(line)
            receipts = collect_worker_receipts(row)
            require(receipts, f"STATE_STOP candidate row {number} lacks v2 worker binding")
            for receipt in receipts:
                validate_worker_receipt(receipt, manifest)
            shadow = row.get("shadow_receipt", {})
            shadow_receipts = collect_worker_receipts(shadow)
            require(len(shadow_receipts) == 1,
                    f"STATE_STOP candidate row {number} lacks unique shadow-v2 binding")
            bound = shadow_receipts[0]
            cell = row.get("cell", {})
            expected_cursor = {
                "aut_pair_index": cell.get("aut_pair_index"),
                "defect_index": cell.get("defect_index"),
                "lift_pair_index": cell.get("lift_pair_index"),
            }
            campaign_stop = shadow.get("campaign_stop_first_empty_fiber") is True
            require(bound.get("mode") == "shadow-fiber" and
                    bound.get("cursor_before") == expected_cursor and
                    bound.get("cell_complete") is True and
                    bound.get("classification_complete") is True and
                    bound.get("outer_advance_authorized") is True and
                    bound.get("terminal_A_eligible") is campaign_stop,
                    f"STATE_STOP candidate row {number} shadow/cell terminal binding")
            if campaign_stop:
                terminal_shadow_bindings[row.get("candidate_id")] = bound
        pending = os.environ.get("D972_PENDING_ENVELOPE", "").strip()
        require(not pending or not Path(pending).exists(),
                "STATE_STOP unresolved DMTCP envelope cannot be checked")
        require(os.environ.get("D972_DMTCP_PHASE_COMPLETE") == "1",
                "STATE_STOP producer process has not completed")
    legacy = load_legacy()
    install_checkpointed_checker_adapter(legacy, manifest)
    exit_code = int(legacy.main(argv))
    if exit_code != 0 or "--self-test" in argv:
        return exit_code
    state_after = json.loads(known.state.read_text(encoding="utf-8"))
    validate_v2_state_binding(state_after, manifest)
    status = state_after["status"]
    witness = state_after.get("terminal_witness")
    if status["code"] == "A_WITNESS_CROSSCHECKED":
        require(status["terminal"] is True and status["resumable"] is False and
                state_after["state_kind"] == "TERMINAL" and isinstance(witness, dict),
                "STATE_STOP premature A terminal flags")
        require(witness.get("isolated") is True and witness.get("target_key_count") == 972 and
                witness.get("image_size") == 324 and bool(witness.get("zero_keys")) and
                is_sha(witness.get("producer_digest")) and
                is_sha(witness.get("checker_digest")),
                "STATE_STOP incomplete A witness")
        bound = terminal_shadow_bindings.get(witness.get("candidate_id"))
        require(isinstance(bound, dict) and bound.get("terminal_A_eligible") is True,
                "STATE_STOP A witness lacks its matching complete shadow-v2 receipt")
        write_final_a_seal(known.state, known.producer_ledger, manifest, bound)
    else:
        require(witness is None, "STATE_STOP non-A checkpoint carries terminal witness")
    # There is deliberately no B terminal in this semidecision workflow.
    require(status["code"] != "B_WITNESS_CROSSCHECKED",
            "STATE_STOP unbounded search cannot manufacture a B terminal")
    return 0


def parse_special(argv: Sequence[str]) -> argparse.Namespace | None:
    if not argv or argv[0] not in {"seal-envelope", "verify-envelope", "verify-final-a"}:
        return None
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    seal = sub.add_parser("seal-envelope")
    seal.add_argument("--checkpoint-dir", type=Path, required=True)
    seal.add_argument("--state", type=Path, required=True)
    seal.add_argument("--envelope", type=Path, required=True)
    seal.add_argument("--coordinator-status", type=Path, required=True)
    seal.add_argument("--launch-environment", type=Path, required=True)
    seal.add_argument("--run-metadata", type=Path, required=True)
    seal.add_argument("--parent-envelope", type=Path)
    seal.add_argument("--generation", type=int)
    verify = sub.add_parser("verify-envelope")
    verify.add_argument("--checkpoint-dir", type=Path, required=True)
    verify.add_argument("--state", type=Path, required=True)
    verify.add_argument("--envelope", type=Path, required=True)
    verify.add_argument("--launch-environment", type=Path, required=True)
    verify.add_argument("--run-metadata", type=Path, required=True)
    verify.add_argument("--parent-envelope", type=Path)
    final = sub.add_parser("verify-final-a")
    final.add_argument("--state", type=Path, required=True)
    final.add_argument("--producer-ledger", type=Path, required=True)
    final.add_argument("--seal", type=Path, required=True)
    final.add_argument("--source-commit", required=True)
    return parser.parse_args(argv)


def synthetic_calibration_gate_and_receipt(legacy: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    seed = json.loads((ROOT / "search" / "d972_dovetail_manifest_v1.json").read_text(
        encoding="utf-8"
    ))["calibration_gate"]
    for case in seed["cases"]:
        case["producer"] = calibration_observation(case["expected"])
    independent = {
        case["case_id"]: calibration_observation(case["expected"])
        for case in seed["cases"]
    }
    gate = compare_calibration_gate(seed, independent, legacy)
    labels_and_multiplicity = (
        ("k1_base", 1), ("split_c2", 1),
        ("nonsplit_q8_c0", 2), ("nonsplit_q8_c1", 2),
    )
    models = []
    for label, multiplicity in labels_and_multiplicity:
        rows = [
            [copy_index, target, target, True]
            for copy_index in range(multiplicity) for target in range(972)
        ]
        vector = [multiplicity] * 972
        models.append({
            "label": label,
            "p_order": 8_817_984 if label == "k1_base" else 17_635_968,
            "kernel_order": 1 if label == "k1_base" else 2,
            "accepted_rows": rows,
            "accepted_rows_sha256": sha_bytes(canonical_bytes(rows)),
            "fiber_counts": vector,
            "fiber_vector_sha256": sha_bytes(canonical_bytes(vector)),
            "image_size": 972,
            "zero_count": 0,
            "fiber_histogram": [{"fiber_size": multiplicity, "target_count": 972}],
        })
    receipt = {
        "schema": "d972-independent-calibration/v2",
        "status": "PASS",
        "backend": CALIBRATION_BACKEND,
        "command_mode": "posix-gap-cli",
        "script_sha256": "0" * 64,
        "stdout_sha256": "1" * 64,
        "stderr_sha256": "2" * 64,
        "q_relators_sha256": "3" * 64,
        "target_key_order_sha256": CALIBRATION_TARGET_KEY_SHA256,
        "target_key_count": 972,
        "classification": marked_c2_classification(),
        "models": models,
        "case_observations": independent,
        "producer_observation_receipts": {
            case["case_id"]: case["producer"]["receipt_sha256"] for case in gate["cases"]
        },
        "producer_metrics_used_as_input": False,
        "search_unlock_authority": True,
    }
    receipt["receipt_sha256"] = sha_bytes(canonical_bytes(receipt))
    return gate, receipt


def self_test() -> int:
    manifest = load_manifest()
    rewrites = manifest["dmtcp_contract"]["gap_4_12_materialized_rewrites"]
    base_rewrites = rewrites.get("base_permutation_groups", {})
    list_rewrites = rewrites.get("table_group", {})
    outer_rewrites = rewrites.get("outer_bucket_inner", {})
    parent_rewrites = rewrites.get("exact_parent_subgroups", {})
    require(
        rewrites.get("replacement_count_total") == 34 and
        base_rewrites.get("replacement_count") == 17 and
        list_rewrites.get("replacement_count") == 1 and
        outer_rewrites.get("replacement_count") == 1 and
        parent_rewrites.get("replacement_count") == 11 and
        parent_rewrites.get("fail_closed_on_count_drift") is True and
        list_rewrites.get("needle") == "G := Group(perms);" and
        list_rewrites.get("replacement") ==
        "G := D972V2PermutationGroup(perms,n,\"table_group\");" and
        outer_rewrites.get("needle") == "I := Group(innerPerms);" and
        outer_rewrites.get("replacement") ==
        "I := D972V2PermutationGroup(innerPerms,k,\"outer_bucket_inner\");" and
        base_rewrites.get("helper") ==
        "D972V2PermutationGroup(generators, degree, stage) -> "
        "Subgroup(SymmetricGroup(degree), PermList images)" and
        base_rewrites.get("fail_closed_on_count_drift") is True,
        "STATE_STOP GAP4.12 base permutation rewrite contract drift",
    )
    require(expected_runtime_receipt(manifest)["whole_process_tree_required"] is True,
            "self-test runtime binding")
    legacy = load_legacy()
    legacy_result = int(legacy.main(["--self-test"]))
    require(legacy_result == 0, "self-test v1 checker")
    gate, calibration_receipt = synthetic_calibration_gate_and_receipt(legacy)
    validate_independent_calibration_receipt(calibration_receipt, gate)
    tampered_gate = copy.deepcopy(gate)
    tampered_producer = tampered_gate["cases"][0]["producer"]
    tampered_producer["gt_orders"][0] += 1
    tampered_body = {key: tampered_producer[key] for key in CALIBRATION_METRICS}
    tampered_producer["receipt_sha256"] = sha_bytes(canonical_bytes(tampered_body))
    try:
        compare_calibration_gate(
            tampered_gate,
            {case["case_id"]: calibration_receipt["case_observations"][case["case_id"]]
             for case in tampered_gate["cases"]},
            legacy,
        )
    except legacy.Disagreement:
        pass
    else:
        raise CheckStop("self-test resealed producer calibration tamper accepted")
    tampered_receipt = copy.deepcopy(calibration_receipt)
    tampered_receipt["models"][0]["fiber_counts"][0] = 0
    tampered_receipt["models"][0]["fiber_vector_sha256"] = sha_bytes(
        canonical_bytes(tampered_receipt["models"][0]["fiber_counts"])
    )
    tampered_body = copy.deepcopy(tampered_receipt)
    tampered_body.pop("receipt_sha256")
    tampered_receipt["receipt_sha256"] = sha_bytes(canonical_bytes(tampered_body))
    try:
        validate_independent_calibration_receipt(tampered_receipt, gate)
    except CheckStop:
        pass
    else:
        raise CheckStop("self-test resealed lossless calibration vector tamper accepted")
    print(json.dumps({
        "schema": "d972-dovetail-checker-selftest/v2",
        "status": "PASS",
        "envelope_hash_negative_gate": True,
        "partial_checkpoint_terminal_authority": False,
        "legacy_independent_candidate_checker": "PASS",
        "independent_calibration_positive": "PASS",
        "independent_calibration_tamper_negative": 2,
    }, sort_keys=True))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--self-test"]:
        return self_test()
    special = parse_special(args)
    if special is not None:
        if special.command == "seal-envelope":
            return seal_envelope(special)
        if special.command == "verify-envelope":
            return verify_envelope(special)
        return verify_final_a(special)
    return run_campaign_checker(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckStop, OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
