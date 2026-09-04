#!/usr/bin/env python3
"""R07 actual P1-to-physical connection producer (v6).

The executable is deliberately a narrow release boundary.  It authenticates
the completed P1-v10 stream, reads one source row, applies the complete
occurrence aggregation, and feeds the v492 lower-first recurrence. Durable
rows stay packed and file backed; an unchecked checkpoint is never a
candidate.
"""
from __future__ import annotations

import argparse
import hashlib
import mmap
import os
import shutil
import sys
import tempfile
import time
import types
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence

import importlib.util
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ROWS = 8059
ELL_WIDTH = 32260
TOP_WIDTH = 48384
COEFF_BYTES = (ROWS + 3) // 4
ELL_BYTES = ELL_WIDTH // 4
TOP_BYTES = TOP_WIDTH // 4
CHECKPOINT_INTERVAL = 128
P1_SCHEMA = "d972.r07.canonical-p1-dag-degree2-lift.v8"
P1_STATUS = "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE"
CONNECTION_SCHEMA = "d972.r07.canonical-p1-physical-connection.v6"
CONNECTION_STATUS = "CANONICAL_P1_PHYSICAL_CONNECTION_CANDIDATE"
CHECKPOINT_SCHEMA = "d972.r07.canonical-p1-physical-connection.checkpoint.v6"
CHECKPOINT_STATUS = "UNCHECKED_CONNECTION_PREFIX"
ZERO_HEAD = "00" * 32
REPOSITORY = "tochiazuma0510-alt/shadow-atelier"
SOURCE_RUN = "33677346616"
SOURCE_ATTEMPT = "1"
SOURCE_HEAD = "22c6dddb43d107c05e65f53ad898823ae8ebe276"
P1_V10_SHA = "af99dbb399a0f98ab70e240498fb7b934ce8e0af93e4930cd1dbd549177f750f"
P1_V10_BYTES = 154825
P1_V10_LF = 3273
PREPARE_DIGEST = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
PARENTS = (
    "9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74",
    "d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6",
    "a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac",
    "642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01",
)
TASK554 = (
    {"role":"prepare","run":"33677346616","attempt":"1","head":SOURCE_HEAD,"id":9865061266,"name":"task554-grade1-v3-prepare-33677346616-1","archive_bytes":204360988,"digest":"sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4","expires_at":"2026-12-01T20:06:55Z"},
    {"role":"block-0","run":"33677346616","attempt":"1","head":SOURCE_HEAD,"id":9865238399,"name":"task554-grade1-v3-state-block-0-33677346616-1","archive_bytes":81729645,"digest":"sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838","expires_at":"2026-12-01T20:06:55Z"},
    {"role":"block-1","run":"33677346616","attempt":"1","head":SOURCE_HEAD,"id":9865242284,"name":"task554-grade1-v3-state-block-1-33677346616-1","archive_bytes":82259824,"digest":"sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb","expires_at":"2026-12-01T20:06:55Z"},
    {"role":"block-2","run":"33677346616","attempt":"1","head":SOURCE_HEAD,"id":9865193269,"name":"task554-grade1-v3-state-block-2-33677346616-1","archive_bytes":82200189,"digest":"sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d","expires_at":"2026-12-01T20:06:55Z"},
    {"role":"block-3","run":"33677346616","attempt":"1","head":SOURCE_HEAD,"id":9865239848,"name":"task554-grade1-v3-state-block-3-33677346616-1","archive_bytes":82266526,"digest":"sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92","expires_at":"2026-12-01T20:06:55Z"},
)
TASK554_CONCLUSION = "failure"
SEMANTIC_CHECKER = {"role":"semantic-checker","run":"33819301663","attempt":"1","head":"e8a4de593700a81fb2a026366e349b89b640a6e8","id":9918207444,"name":"task757-p1-semantic-checker-only-v3-success-33819301663-1","archive_bytes":24694,"digest":"sha256:f99fd6ce1172cc349b249ead8dbb8e75c8c8bd8a1b8a0493dfd4596aee5fbf0c","expires_at":"2026-12-02T23:50:18Z"}
TASK712_ARTIFACT = {"role":"task712","run":"33814194630","attempt":"1","head":"5ff2c5a30b604536df12acba8801828a5a7e5fe0","id":9915928157,"name":"d972-r07-grade2-maps-v4-33814194630-1","archive_bytes":22404961,"digest":"sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858","expires_at":"2026-10-03T22:41:38Z"}
TASK712_PRODUCER_SHA = "7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84"
SOURCE_HASHES = {
    "p1_v10":"af99dbb399a0f98ab70e240498fb7b934ce8e0af93e4930cd1dbd549177f750f",
    "grade1_v4":"1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4",
    "prebuild_v1":"acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8",
    "semantic_v5":"dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf",
    "structural_v1":"38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73",
    "floor_v1":"6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba",
    "words":"90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893",
    "task712_v3":"7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84",
}
RECEIPT_HASHES = (
    "9caf8cbf04742b1400c5c63d765508308af72ef773050af5562221a082fd159a",
    "e9271d20739aee299620ef6e8d53dd940ea10ed1ab688bd61b69c7fb0ff4afc8",
    "7f34bb964665078727c7ed2b5e5165c50b1763003d573789d7406a6b06445eca",
    "6d8ebdf7b9495608c89779ecfd7ca8f3c1a84790fc8e2b6b6fc5dd292c530e6a",
    "a558c466862bf050bf8c850aaf47be633ae1f0bce9785f18b410cb0eff9f6d9d",
    "a3479e7ebc010fbfde4d42c95eebd8cf81cc5eeab9ef37ab77ba2284fb8b27c8",
)
SEMANTIC_RESULT_SHA = "405e1b26f971f67cb73129071a77346b126d0228c84219c2c3b0d879c63c99d5"
SEMANTIC_WORKFLOW_SHA = "323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb"
ORDER = [0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059]
CHARACTERS = ((0,0),(0,1),(1,0),(1,1))
ACTORS = (1,-1,2,-2)
MONOMIALS = ((2,0,0),(1,1,0),(1,0,1),(0,2,0),(0,1,1),(0,0,2))
FALSE_FLAGS = {"A0":False,"COMMON":False,"COFINAL_LIFT":False,"FAKE":False,"IHARA":False,"verified":False}
SOURCE_RECEIPT_KEYS = {"node","instruction_sha256","p1_sha256","cache_row_sha256","predecessor","ancestry_sha256"}


def canon(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_receipt(path: Path, expected: dict[str, Any] | None = None) -> dict[str, Any]:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw, "source_bom_or_cr")
    value = {"path":str(path),"bytes":len(raw),"sha256":sha(raw),"lf":raw.count(b"\n"),"final_lf":raw.endswith(b"\n")}
    if expected is not None:
        require(value["bytes"] == expected["bytes"] and value["sha256"] == expected["sha256"] and value["lf"] == expected["lf"], "source_receipt_mismatch")
    return value


def _digits(value: int) -> tuple[int,int,int,int]:
    require(0 <= value <= 80, "packed_byte_out_of_range")
    return value % 3, (value // 3) % 3, (value // 9) % 3, (value // 27) % 3


DIGITS = np.asarray([_digits(i) for i in range(81)], dtype=np.uint8)
PACKED_AXPY = np.empty((2,81,81), dtype=np.uint8)
for _scalar in (1,2):
    for _left in range(81):
        for _right in range(81):
            PACKED_AXPY[_scalar-1,_left,_right] = sum(((int(DIGITS[_left,j]) - _scalar*int(DIGITS[_right,j])) % 3) * 3**j for j in range(4))
SCALE2 = np.asarray([sum(((2*int(DIGITS[i,j])) % 3) * 3**j for j in range(4)) for i in range(81)], dtype=np.uint8)
FIRST_TRIT = np.full(81,-1,dtype=np.int8)
FIRST_VALUE = np.zeros(81,dtype=np.uint8)
for _value in range(1,81):
    for _position,_digit in enumerate(DIGITS[_value]):
        if _digit:
            FIRST_TRIT[_value] = _position; FIRST_VALUE[_value] = _digit; break


def validate_packed(raw: bytes | bytearray | memoryview | np.ndarray, width: int) -> None:
    expected = (width + 3) // 4
    view = raw.reshape(-1) if isinstance(raw,np.ndarray) else np.frombuffer(raw,dtype=np.uint8)
    require(view.size == expected and not np.any(view > 80), "packed_row_shape_or_byte")
    if width % 4:
        require(int(DIGITS[int(view[-1]),width % 4]) == 0, "packed_padding")


def pack(values: Sequence[int] | Iterable[int], width: int) -> bytes:
    array = np.asarray(list(values),dtype=np.uint8).reshape(-1)
    require(array.size == width and not np.any(array > 2), "pack_shape")
    output = np.zeros((width+3)//4,dtype=np.uint8)
    for position in range(4):
        output[:(width+3-position)//4] += (array[position::4] * 3**position).astype(np.uint8)
    validate_packed(output,width)
    return output.tobytes()


def unpack(raw: bytes, width: int) -> np.ndarray:
    validate_packed(raw,width); packed = np.frombuffer(raw,dtype=np.uint8); output = np.empty(width,dtype=np.uint8)
    for position in range(4): output[position::4] = DIGITS[packed,position][:output[position::4].size]
    return output


def axpy_inplace(destination: np.ndarray, source: np.ndarray, scalar: int, width: int) -> None:
    require(scalar in (1,2) and destination.dtype == np.uint8 and source.dtype == np.uint8 and destination.size == source.size == (width+3)//4, "axpy_shape")
    # Rows are authenticated at append/resume and the lookup has a total
    # domain 0..80; scanning either whole row in this hot path is forbidden.
    destination[:] = PACKED_AXPY[scalar-1,destination,source]


def scale_two_inplace(destination: np.ndarray, width: int) -> None:
    require(destination.size == (width+3)//4, "scale_shape")
    destination[:] = SCALE2[destination]
    if width % 4:
        require(int(DIGITS[int(destination[-1]),width % 4]) == 0, "scale_padding")


def first_nonzero(raw: bytes | bytearray | memoryview | np.ndarray, width: int) -> tuple[int,int] | None:
    validate_packed(raw,width); return first_nonzero_unchecked(raw,width)


def first_nonzero_unchecked(raw: bytes | bytearray | memoryview | np.ndarray, width: int) -> tuple[int,int] | None:
    array = raw.reshape(-1) if isinstance(raw,np.ndarray) else np.frombuffer(raw,dtype=np.uint8); nonzero = np.flatnonzero(array)
    if not nonzero.size: return None
    byte_index = int(nonzero[0]); coordinate = 4*byte_index + int(FIRST_TRIT[int(array[byte_index])])
    return None if coordinate >= width else (coordinate,int(FIRST_VALUE[int(array[byte_index])]))


class Store:
    """Append-only packed store with reusable positioned read buffers."""
    def __init__(self,path: Path,row_bytes: int,width: int,mode: str) -> None:
        require(mode in ("w+b","r+b"),"store_mode"); self.path,self.row_bytes,self.width = path,row_bytes,width; self.stream = path.open(mode, buffering=0)
    def append(self,raw: bytes) -> int:
        require(len(raw) == self.row_bytes,"store_append_length"); validate_packed(raw,self.width); self.stream.seek(0,os.SEEK_END); offset=self.stream.tell(); written=self.stream.write(raw); require(written == self.row_bytes,"store_append_write"); return offset
    def read_into(self,offset: int,target: np.ndarray) -> None:
        require(offset >= 0 and offset % self.row_bytes == 0 and target.dtype == np.uint8 and target.size == self.row_bytes,"store_position")
        view=memoryview(target)
        if hasattr(os,"preadv"):
            require(os.preadv(self.stream.fileno(),[view],offset) == self.row_bytes,"store_eof")
        else:
            self.stream.seek(offset); require(self.stream.readinto(view) == self.row_bytes,"store_eof")
    def sync(self) -> None:
        self.stream.flush(); os.fsync(self.stream.fileno())
    def close(self) -> None: self.stream.close()


def load_exact(path: Path, expected: str, module_name: str) -> types.ModuleType:
    raw=path.read_bytes(); require(sha(raw) == expected,"source_pin:"+path.name); module=types.ModuleType(module_name); module.__file__=str(path); module.__package__=""; previous=sys.modules.get(module_name); sys.modules[module_name]=module
    try: exec(compile(raw,str(path),"exec"),module.__dict__)
    except BaseException:
        if previous is None: sys.modules.pop(module_name,None)
        else: sys.modules[module_name]=previous
        raise
    return module


def validate_artifact(value: Any, expected: dict[str, Any], label: str) -> None:
    require(isinstance(value,dict),label+":type")
    for key in ("role","run","attempt","head","id","name","archive_bytes","digest","expires_at","repository","run_status","run_conclusion"):
        require(key in value,label+":key:"+key)
    require(value == expected,label+":identity")


def validate_launch(path: Path) -> dict[str, Any]:
    raw=path.read_bytes(); value=json.loads(raw.decode("ascii")); require(raw == canon(value),"launch_noncanonical")
    required={"schema","repository","p1_artifact","task554_artifacts","semantic_checker_artifact","task712_artifact","source_files","executable_files","query_receipts"}
    require(set(value) == required and value["schema"] == "d972.r07.canonical-p1-physical-connection.launch.v6","launch_keys_or_schema")
    require(value["repository"] == REPOSITORY,"launch_repository")
    require(isinstance(value["task554_artifacts"],list) and len(value["task554_artifacts"]) == 5,"launch_task554_roster")
    for actual,expected in zip(value["task554_artifacts"],TASK554): validate_artifact(actual,dict(expected,repository=REPOSITORY,run_status="completed",run_conclusion=TASK554_CONCLUSION),"launch_task554")
    validate_artifact(value["semantic_checker_artifact"],dict(SEMANTIC_CHECKER,repository=REPOSITORY,run_status="completed",run_conclusion="success"),"launch_semantic_checker")
    validate_artifact(value["task712_artifact"],dict(TASK712_ARTIFACT,repository=REPOSITORY,run_status="completed",run_conclusion="success"),"launch_task712")
    p1=value["p1_artifact"]; require(isinstance(p1,dict) and set(p1) == {"role","repository","run","attempt","head","id","name","archive_bytes","digest","expires_at","run_status","run_conclusion","workflow_run_id","workflow_run_attempt","workflow_head_sha","api_verified"},"launch_p1_keys")
    require(p1["role"] == "p1-candidate" and p1["repository"] == REPOSITORY and p1["run"] == str(p1["workflow_run_id"]) and p1["attempt"] == str(p1["workflow_run_attempt"]) and p1["head"] == p1["workflow_head_sha"] and p1["run_status"] == "completed" and p1["run_conclusion"] == "success" and p1["api_verified"] is True and plain_int(p1["id"]) and p1["id"] > 0 and isinstance(p1["name"],str) and p1["name"] and isinstance(p1["digest"],str) and p1["digest"].startswith("sha256:") and isinstance(p1["expires_at"],str) and p1["expires_at"],"launch_p1_identity")
    require(isinstance(value["source_files"],list) and value["source_files"],"launch_source_files")
    for item in value["source_files"]: require(isinstance(item,dict) and set(item) == {"path","sha256","bytes","lf","bom","cr"} and item["bom"] is False and item["cr"] is False and plain_int(item["bytes"]) and plain_int(item["lf"],),"launch_source_receipt")
    require(isinstance(value["executable_files"],list) and len(value["executable_files"]) == 2,"launch_executable_roster")
    for item in value["executable_files"]: require(isinstance(item,dict) and set(item) == {"path","sha256","bytes","lf","bom","cr"},"launch_executable_receipt")
    require(isinstance(value["query_receipts"],dict) and set(value["query_receipts"]) == {"p1_run","p1_artifact","task554","semantic_checker","task712"},"launch_query_receipts")
    return value


def validate_launch_file_receipts(launch: dict[str, Any], runtime: dict[str, Path]) -> tuple[dict[str, dict[str, Any]],dict[str, dict[str, Any]]]:
    """Bind launch receipts to the bytes actually executed on this runner."""
    expected_paths={
        "p1_v10":"search/d972_r07_canonical_p1_dag_degree2_lift_v10.py",
        "grade1_v4":"search/d972_r07_a0_first_rung_grade1_v4.py",
        "prebuild_v1":"search/d972_r07_a0_first_rung_grade2_prebuild_v1.py",
        "semantic_v5":"search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py",
        "structural_v1":"search/d972_r07_grade2_specific_owner_prejoin_v1.py",
        "floor_v1":"search/d972_r07_a0_c2fourier_joint_floor_v1.py",
        "words":"scratchpad/a0_paper_words_v1.json",
        "task712_v3":"search/d972_r07_grade2_forward_adjoint_maps_v3.py",
    }
    source_items={str(item["path"]):item for item in launch["source_files"]}
    source_receipts={}
    for name,path in runtime.items():
        relative=expected_paths[name]; item=source_items.get(relative); require(item is not None,"launch_source_missing:"+relative)
        actual=file_receipt(path); require(actual["sha256"] == item["sha256"] and actual["bytes"] == item["bytes"] and actual["lf"] == item["lf"] and actual["final_lf"] is bool(item.get("final_lf",actual["final_lf"])),"launch_source_runtime_mismatch:"+name); source_receipts[name]=actual
    executable_items={str(item["path"]):item for item in launch["executable_files"]}
    executable_receipts={}
    for relative,path in (("search/d972_r07_canonical_p1_physical_connection_v6.py",ROOT/"search/d972_r07_canonical_p1_physical_connection_v6.py"),("search/check_d972_r07_canonical_p1_physical_connection_v7.py",ROOT/"search/check_d972_r07_canonical_p1_physical_connection_v7.py")):
        item=executable_items.get(relative); require(item is not None,"launch_executable_missing:"+relative); actual=file_receipt(path); require(actual["sha256"] == item["sha256"] and actual["bytes"] == item["bytes"] and actual["lf"] == item["lf"],"launch_executable_runtime_mismatch:"+relative); executable_receipts[relative]=actual
    return source_receipts,executable_receipts


P1_MANIFEST_KEYS={"schema","status","producer_sha256","semantic_file_hashes","imports","launch_manifest_sha256","checker_result_sha256","checker_workflow_receipt_sha256","checker_success_artifact","semantic_receipt_sha256","executable_hashes","raw_artifacts","raw_file_registry","source_ancestry","character_order","actor_order","monomial_order","global_order","rows","row_trits","row_bytes","instruction","cache","ancestry_sha256","independent_checker","A0","COMMON","COFINAL","FAKE","IHARA","verified"}
P1_INSTRUCTION_KEYS={"node","origin","reductions","scale","raw_origin_sha256","raw_origin_components_sha256","literal_input_sha256","old_defect_literal_input_sha256","parent_row_sha256","packet_sha256","packet_row_sha256","reduction_parent_sha256","p1_sha256","offset","length","row_receipt","predecessor","ancestry_sha256"}


def validate_p1(root: Path, launch: dict[str, Any]) -> tuple[dict[str, Any],list[dict[str,str]]]:
    manifest_path=root/"manifest.json"; raw=manifest_path.read_bytes(); manifest=json.loads(raw.decode("ascii")); require(raw == canon(manifest) and set(manifest) == P1_MANIFEST_KEYS,"p1_manifest_shape")
    require(manifest["schema"] == P1_SCHEMA and manifest["status"] == P1_STATUS and manifest["rows"] == ROWS and manifest["row_trits"] == 145152 and manifest["row_bytes"] == 36288,"p1_schema_dimensions")
    require(manifest["character_order"] == [list(x) for x in CHARACTERS] and manifest["actor_order"] == list(ACTORS) and manifest["monomial_order"] == [list(x) for x in MONOMIALS] and manifest["global_order"] == ORDER,"p1_coordinate_order")
    require(manifest["independent_checker"] is False and all(manifest[x] is False for x in ("A0","COMMON","COFINAL","FAKE","IHARA","verified")),"p1_claim_boundary")
    require(manifest["producer_sha256"] == P1_V10_SHA and manifest["executable_hashes"] == {"producer_v8":P1_V10_SHA,"semantic_v5":SOURCE_HASHES["semantic_v5"],"checker_v5":"bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97"},"p1_producer_identity")
    require(manifest["semantic_file_hashes"] == {"grade1_v4":SOURCE_HASHES["grade1_v4"],"grade2_prebuild_v1":SOURCE_HASHES["prebuild_v1"],"semantic_v5":SOURCE_HASHES["semantic_v5"],"checker_v5":"bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97","structural_v1":SOURCE_HASHES["structural_v1"],"floor_v1":SOURCE_HASHES["floor_v1"],"words":SOURCE_HASHES["words"]},"p1_semantic_file_identity")
    require(manifest["imports"] == {"grade1_v4":SOURCE_HASHES["grade1_v4"],"grade2_prebuild_v1":SOURCE_HASHES["prebuild_v1"],"semantic_v5":SOURCE_HASHES["semantic_v5"],"structural_v1":SOURCE_HASHES["structural_v1"],"floor_v1":SOURCE_HASHES["floor_v1"]},"p1_import_identity")
    expected_ancestry={"source_run":SOURCE_RUN,"source_attempt":SOURCE_ATTEMPT,"source_head":SOURCE_HEAD,"prepare_body_sha256":PREPARE_DIGEST,"parents":list(PARENTS),"producer_receipts":{"prepare":RECEIPT_HASHES[0],"blocks":list(RECEIPT_HASHES[1:5]),"join":RECEIPT_HASHES[5]},"checker_result_sha256":SEMANTIC_RESULT_SHA,"checker_workflow_receipt_sha256":SEMANTIC_WORKFLOW_SHA,"checker_success_artifact":{"id":9918207444,"name":"task757-p1-semantic-checker-only-v3-success-33819301663-1","archive_bytes":24694,"digest":"sha256:f99fd6ce1172cc349b249ead8dbb8e75c8c8bd8a1b8a0493dfd4596aee5fbf0c"}}
    require(manifest["source_ancestry"] == expected_ancestry,"p1_parent_ancestry")
    cache_path=root/"degree2.cache.bin"; instruction_path=root/"instructions.jsonl"; require(cache_path.is_file() and instruction_path.is_file() and cache_path.stat().st_size == ROWS*36288,"p1_store_shape")
    cache_file=cache_path.open("rb"); cache_map=mmap.mmap(cache_file.fileno(),0,access=mmap.ACCESS_READ); cache_digest=file_sha(cache_path); require(manifest["cache"] == {"path":"degree2.cache.bin","rows":ROWS,"bytes":ROWS*36288,"sha256":cache_digest,"final_lf":False,"eof":True},"p1_cache_receipt")
    rows=[]; previous=ZERO_HEAD; instruction_digest=hashlib.sha256()
    with instruction_path.open("rb") as stream:
        for node in range(ROWS):
            line=stream.readline(); require(line and line.endswith(b"\n") and b"\r" not in line,"p1_instruction_lf"); instruction_digest.update(line); record=json.loads(line.decode("ascii")); require(line == canon(record) and set(record) == P1_INSTRUCTION_KEYS and record["node"] == node,"p1_instruction_record")
            offset=node*36288; receipt=record["row_receipt"]; require(isinstance(receipt,dict) and set(receipt) == {"offset","length","sha256"} and receipt["offset"] == offset and receipt["length"] == 36288,"p1_cache_row_receipt")
            cache_row=cache_map[offset:offset+36288]; validate_packed(cache_row,145152); require(receipt["sha256"] == sha(cache_row) and isinstance(record["p1_sha256"],str) and len(record["p1_sha256"]) == 64,"p1_cache_row_digest")
            require(record["predecessor"] == previous and isinstance(record["ancestry_sha256"],str) and len(record["ancestry_sha256"]) == 64,"p1_instruction_ancestry"); unsigned=dict(record); unsigned.pop("ancestry_sha256"); head=sha(bytes.fromhex(previous)+canon(unsigned)); require(record["ancestry_sha256"] == head,"p1_instruction_rolling")
            rows.append({"node":node,"instruction_sha256":sha(line),"p1_sha256":record["p1_sha256"],"cache_row_sha256":receipt["sha256"],"predecessor":previous,"ancestry_sha256":head}); previous=head
        require(stream.read(1) == b"","p1_instruction_extra")
    receipt={"path":"instructions.jsonl","rows":ROWS,"bytes":instruction_path.stat().st_size,"sha256":instruction_digest.hexdigest(),"final_lf":True,"eof":True,"final_head":previous}; require(manifest["instruction"] == receipt and manifest["ancestry_sha256"] == previous,"p1_instruction_terminal"); cache_map.close(); cache_file.close()
    return manifest,rows


class Task712Tables:
    """Authenticated complete Task712 map roster and structural records."""
    @staticmethod
    def names() -> list[str]:
        names=[]
        for character in range(4):
            for actor in range(4):
                names.extend((f"T_fwd_a{character}_t{actor}.jsonl",f"T_adj_a{character}_t{actor}.jsonl"))
            names.extend((f"B_fwd_a{character}.jsonl",f"B_adj_a{character}.jsonl"))
        return names

    @classmethod
    def _spec(cls,name: str) -> tuple[str,int,int|None,int,int]:
        require(name in cls.names(),"task712_unknown_table")
        # ``adj`` contains an ``a``; split only at the roster's explicit
        # character token so T_adj_a0 and B_adj_a0 are not parsed as "dj".
        match = __import__("re").fullmatch(
            r"(?P<kind>T|B)_(?P<direction>fwd|adj)_a(?P<character>[0-3])"
            r"(?:_t(?P<actor>[0-3]))?\.jsonl", name)
        require(match is not None,"task712_name_syntax")
        kind = match.group("kind")
        direction = match.group("direction")
        character = int(match.group("character"))
        actor = int(match.group("actor")) if match.group("actor") is not None else None
        require((kind == "T") == (actor is not None),"task712_actor_shape")
        source_width, destination_width = ((36288, 36288) if kind == "T" else
                                           ((36288, TOP_WIDTH) if direction == "fwd" else
                                            (TOP_WIDTH, 36288)))
        return kind, character, actor, source_width, destination_width

    def __init__(self,root: Path):
        self.root=root.resolve(); files=[p for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()]; require(files,"task712_empty"); candidates=[]
        for path in files:
            if path.name != "manifest.json": continue
            try: value=json.loads(path.read_bytes().decode("ascii"))
            except Exception: continue
            if isinstance(value,dict) and value.get("table_count") == 40: candidates.append((path,value))
        require(len(candidates) == 1,"task712_manifest"); self.manifest_path,self.manifest=candidates[0]; manifest_raw=self.manifest_path.read_bytes(); require(manifest_raw == canon(self.manifest) and self.manifest.get("schema") == "d972.r07.grade2.forward-adjoint-maps.v3" and self.manifest.get("marker") == "R07_GRADE2_FORWARD_ADJOINT_MAPS_V3_CANDIDATE" and self.manifest.get("map_count") == 20,"task712_manifest_semantics")
        roster=self.manifest.get("table_roster"); require(roster == self.names(),"task712_roster"); descriptors={str(item.get("file")):item for item in self.manifest.get("tables",[]) if isinstance(item,dict)}; require(set(descriptors) == set(roster),"task712_descriptor_roster"); self.tables={}; self.table_records={}; self.table_files={}
        for name in roster:
            paths=[p for p in files if p.name == name]; require(len(paths) == 1 and name in descriptors,"task712_table_missing"); path=paths[0]; kind,character,actor,source_width,destination_width=self._spec(name); expected_receipt=descriptors[name]; rows=self._read_table(path,expected_receipt,source_width,destination_width,kind,character,actor); self.table_records[name]=rows; self.table_files[name]=sha(path.read_bytes());
            if name.startswith("B_fwd_a"): self.tables[character]=rows
        require(set(self.tables) == set(range(4)),"task712_B_roster")
        checker=[]
        for path in files:
            if "checker" not in path.name or path.suffix != ".json": continue
            try: value=json.loads(path.read_bytes().decode("ascii"))
            except Exception: continue
            if isinstance(value,dict) and value.get("tables_checked") == 40: checker.append((path,value))
        require(len(checker) == 1 and checker[0][1].get("marker") == "R07_GRADE2_FORWARD_ADJOINT_MAPS_V4_CHECKER_PASS","task712_checker_receipt")
        workflow=[]
        for path in files:
            if "receipt" not in path.name or path.suffix != ".json": continue
            try: value=json.loads(path.read_bytes().decode("ascii"))
            except Exception: continue
            if isinstance(value,dict) and value.get("schema") == "d972.r07.grade2.forward-adjoint-maps.v4.workflow-receipt": workflow.append((path,value))
        require(len(workflow) == 1 and workflow[0][1].get("table_count") == 40 and workflow[0][1].get("map_count") == 20,"task712_workflow_receipt")
        self.receipt={"manifest_sha256":sha(manifest_raw),"checker_sha256":sha(checker[0][0].read_bytes()),"workflow_sha256":sha(workflow[0][0].read_bytes()),"table_files":dict(self.table_files)}

    @staticmethod
    def _read_table(path: Path,receipt: dict[str,Any],source_width: int,destination_width: int,kind: str,character: int,actor: int|None) -> list[tuple[int,int,int]]:
        required={"file","schema","source_width","destination_width","entry_count","body_bytes","body_sha256","bytes","sha256","eof","encoding","map_kind","map_direction","character"};
        if kind == "T": required.add("actor")
        require(set(receipt) == required and receipt.get("file") == path.name and receipt.get("schema") == "d972.r07.grade2.forward-adjoint-maps.v3.sparse-jsonl" and receipt.get("source_width") == source_width and receipt.get("destination_width") == destination_width and receipt.get("encoding") == "jsonl-triples-utf8-lf" and receipt.get("map_kind") == kind and receipt.get("map_direction") == ("adjoint" if "_adj_" in path.name else "forward") and receipt.get("character") == character and (kind != "T" or receipt.get("actor") == ACTORS[actor]) and receipt.get("eof") is True,"task712_table_receipt")
        for key in ("source_width","destination_width","entry_count","body_bytes","bytes","character") + (("actor",) if kind == "T" else ()): require(plain_int(receipt.get(key)),"task712_table_type")
        raw=path.read_bytes(); body=hashlib.sha256(); body_bytes=0; rows=[]; previous=None; eof=False
        for line in raw.splitlines(keepends=True):
            require(line.endswith(b"\n") and line != b"\n" and b"\r" not in line,"task712_table_lf"); value=json.loads(line.decode("ascii"))
            if isinstance(value,dict):
                require(not eof and set(value) == {"body_bytes","body_sha256","count","eof"} and value["eof"] is True and line == canon(value),"task712_table_eof"); require(plain_int(value["count"]) and plain_int(value["body_bytes"]) and value["count"] == len(rows) and value["body_bytes"] == body_bytes and value["body_sha256"] == body.hexdigest(),"task712_table_body"); eof=True
            else:
                require(not eof and isinstance(value,list) and len(value) == 3 and all(plain_int(x) for x in value),"task712_table_record"); row=tuple(int(x) for x in value); require(0 <= row[0] < source_width and 0 <= row[1] < destination_width and row[2] in (1,2),"task712_table_range"); require(previous is None or row[:2] > previous and line == (json.dumps(list(row),separators=(",",":"))+"\n").encode("ascii"),"task712_table_order"); previous=row[:2]; rows.append(row); body.update(line); body_bytes += len(line)
        require(eof and receipt.get("entry_count") == len(rows) and receipt.get("body_bytes") == body_bytes and receipt.get("body_sha256") == body.hexdigest() and receipt.get("bytes") == len(raw) and receipt.get("sha256") == sha(raw),"task712_table_receipt_digest"); return rows

    def pure(self,character: int,source: np.ndarray) -> np.ndarray:
        require(source.shape == (36288,),"task712_source_shape"); result=np.zeros(TOP_WIDTH,dtype=np.uint8)
        for source_index,destination,coefficient in self.tables[character]: result[destination]=(int(result[destination])+coefficient*int(source[source_index]))%3
        return result

    def restriction(self,d2: np.ndarray) -> np.ndarray:
        require(d2.shape == (4,36288),"task712_restriction_shape"); result=np.zeros(TOP_WIDTH,dtype=np.uint8)
        for character in range(4): result=(result+self.pure(character,d2[character]))%3
        return result


def compare_complete_restriction(actual: Sequence[Sequence[int]],
                                 expected: Sequence[Sequence[int]],
                                 source_width: int = 36288,
                                 destination_width: int = TOP_WIDTH,
                                 label: str = "task712_complete_map") -> dict[str, int]:
    """Compare every sparse entry and every source column of the pure map."""
    actual_rows = [tuple(int(value) for value in row) for row in actual]
    expected_rows = [tuple(int(value) for value in row) for row in expected]
    require(actual_rows == expected_rows, label + ":entry")
    actual_columns = [[] for _ in range(source_width)]
    expected_columns = [[] for _ in range(source_width)]
    for source, destination, coefficient in actual_rows:
        require(0 <= source < source_width and 0 <= destination < destination_width
                and coefficient in (1, 2), label + ":range")
        actual_columns[source].append((destination, coefficient))
    for source, destination, coefficient in expected_rows:
        require(0 <= source < source_width and 0 <= destination < destination_width
                and coefficient in (1, 2), label + ":expected_range")
        expected_columns[source].append((destination, coefficient))
    for source in range(source_width):
        require(actual_columns[source] == expected_columns[source],
                label + ":column:" + str(source))
    return {"source_columns": source_width, "entries": len(actual_rows)}


def expected_task712_restriction_maps(words: dict[str, Any]) -> dict[int, list[tuple[int, int, int]]]:
    """Rebuild B maps from the pinned Task712 producer as an occurrence-side oracle."""
    path = ROOT / "search/d972_r07_grade2_forward_adjoint_maps_v3.py"
    module = load_exact(path, TASK712_PRODUCER_SHA, "d972_task712_pinned_producer_v3")
    context = module.Context(words)
    result = {}
    for character in range(4):
        raw = module.iter_aggregation_raw(context, character)
        result[character] = [tuple(int(value) for value in row)
                             for row in module.canonical_entries(raw, 36288, TOP_WIDTH)[0]]
    return result


def validate_complete_task712_maps(task712: Task712Tables,
                                    words: dict[str, Any]) -> dict[str, int]:
    expected = expected_task712_restriction_maps(words)
    totals = {"source_columns": 0, "entries": 0}
    for character in range(4):
        receipt = compare_complete_restriction(
            task712.table_records[f"B_fwd_a{character}.jsonl"],
            expected[character], label=f"task712_complete_map_a{character}")
        totals["source_columns"] += receipt["source_columns"]
        totals["entries"] += receipt["entries"]
    return totals


def validate_task712(root: Path) -> Task712Tables:
    return Task712Tables(root)


class BoundedTask712:
    """Tiny complete-map stand-in used only by the bounded public adapter."""
    def __init__(self) -> None:
        self.tables = {character: [] for character in range(4)}
        self.receipt = {"fixture":"complete-task712-structural-map", "table_count":40, "map_count":20, "table_roster":Task712Tables.names()}

    def pure(self, character: int, source: np.ndarray) -> np.ndarray:
        require(source.shape == (36288,), "bounded_task712_source")
        return np.zeros(TOP_WIDTH,dtype=np.uint8)

    def restriction(self, d2: np.ndarray) -> np.ndarray:
        require(d2.shape == (4,36288), "bounded_task712_restriction")
        result=np.zeros(TOP_WIDTH,dtype=np.uint8)
        for character in range(4): result=(result+self.pure(character,d2[character]))%3
        return result


class PhysicalSource:
    """P1-v10 source adapter; counters are incremented inside ``pair``."""
    def __init__(self,p1_root: Path,bundle: dict[str,Any]):
        self.bundle=bundle; self.p1_root=p1_root; self.p1=bundle["p1v10"].LazyP1(bundle["p2"],bundle["prepare"],bundle["blocks"],bundle["prepare_root"],bundle["block_roots"]); self.context=bundle["g1"].Context(bundle["words"]); self.instructions=bundle["p1_instructions"]; self.task712=bundle.get("task712"); self._cache_file=(p1_root/"degree2.cache.bin").open("rb"); self._cache=mmap.mmap(self._cache_file.fileno(),0,access=mmap.ACCESS_READ); self.pair_calls=0; self.node_hits={}; self._restriction_checked=False

    @classmethod
    def bounded_fixture(cls,rows: dict[int,tuple[bytes,bytes,dict[str,Any]]] | list[tuple[bytes,bytes,dict[str,Any]]]) -> "PhysicalSource":
        obj=cls.__new__(cls); obj._fixture_rows=rows; obj.pair_calls=0; obj.node_hits={}; obj._restriction_checked=False; obj.p1_identity={"fixture":"production-shaped-p1"}; obj.task712=BoundedTask712(); obj.task712_identity=obj.task712.receipt; return obj

    def pair(self,index: int) -> tuple[bytes,bytes,dict[str,Any]]:
        self.pair_calls += 1; self.node_hits[index]=self.node_hits.get(index,0)+1; require(0 <= index < ROWS,"pair_index")
        if hasattr(self,"_fixture_rows"):
            row=self._fixture_rows[index] if isinstance(self._fixture_rows,dict) else self._fixture_rows[index]; source=dict(row[2]); require(set(source) == {"node","instruction_sha256","p1_sha256","cache_row_sha256","predecessor","ancestry_sha256"} and plain_int(source["node"]) and source["node"] == index,"fixture_source_shape"); validate_packed(row[0],ELL_WIDTH); validate_packed(row[1],TOP_WIDTH)
            if not self._restriction_checked:
                d2=np.zeros((4,36288),dtype=np.uint8); require(np.array_equal(self.task712.restriction(d2),np.zeros(TOP_WIDTH,dtype=np.uint8)),"task712_full_restriction_fixture"); self._restriction_checked=True
            return row[0],row[1],source
        p2=self.bundle["p2"]; row=self.p1.row(index); packed_p1=p2.grade1.pack_trits(row).tobytes(); meta=self.instructions[index]; require(sha(packed_p1) == meta["p1_sha256"],"pair_p1_instruction_mismatch"); offset=index*36288; cache_row=self._cache[offset:offset+36288]; validate_packed(cache_row,145152); require(sha(cache_row) == meta["cache_row_sha256"],"pair_cache_instruction_mismatch"); d0,d1,aux=p2.split_precision1(row); d2=p2.grade1.unpack_trits(np.frombuffer(cache_row,dtype=np.uint8),145152).reshape(4,36288); p0,p1,p2row,paux=p2.aggregate_precision2(self.context,d0,d1,d2,aux); character=max(i for i in range(4) if ORDER[i] <= index) if index < ORDER[4] else max(i for i in range(4) if ORDER[4+i] <= index)
        if self.task712 is not None and not self._restriction_checked:
            pure=p2.aggregate_precision2(self.context,np.zeros_like(d0),np.zeros_like(d1),d2,np.zeros(8,dtype=np.uint8))[2].reshape(-1); require(np.array_equal(pure,self.task712.restriction(d2)),"task712_full_restriction"); self._restriction_checked=True
        return pack(np.concatenate((p0.reshape(-1),p1.reshape(-1),paux)),ELL_WIDTH),pack(p2row.reshape(-1),TOP_WIDTH),dict(meta)

    def close(self) -> None:
        if hasattr(self,"p1") and self.p1 is not None: self.p1.close()
        if hasattr(self,"_cache"): self._cache.close()
        if hasattr(self,"_cache_file"): self._cache_file.close()


def authenticate_bundle(args: argparse.Namespace) -> dict[str,Any]:
    launch=validate_launch(Path(args.launch_manifest).resolve())
    runtime={"p1_v10":Path(args.p1_v10).resolve(),"grade1_v4":Path(args.grade1).resolve(),"prebuild_v1":Path(args.prebuild).resolve(),"semantic_v5":Path(args.semantic).resolve(),"structural_v1":Path(args.structural).resolve(),"floor_v1":Path(args.floor).resolve(),"words":Path(args.words).resolve(),"task712_v3":ROOT/"search/d972_r07_grade2_forward_adjoint_maps_v3.py"}; expected={"p1_v10":(P1_V10_SHA,P1_V10_BYTES,P1_V10_LF),"grade1_v4":(SOURCE_HASHES["grade1_v4"],144552,3326),"prebuild_v1":(SOURCE_HASHES["prebuild_v1"],145917,3499),"semantic_v5":(SOURCE_HASHES["semantic_v5"],41619,382),"structural_v1":(SOURCE_HASHES["structural_v1"],47995,545),"floor_v1":(SOURCE_HASHES["floor_v1"],26235,508),"words":(SOURCE_HASHES["words"],115928,0),"task712_v3":(TASK712_PRODUCER_SHA,46179,989)}; source_receipts={}
    for name,path in runtime.items(): digest,size,lf=expected[name]; source_receipts[name]=file_receipt(path,{"bytes":size,"sha256":digest,"lf":lf})
    _,executable_receipts=validate_launch_file_receipts(launch,runtime)
    p1_manifest,p1_instructions=validate_p1(Path(args.p1_root).resolve(),launch)
    for path,expected_hash in zip(args.semantic_receipts,RECEIPT_HASHES): raw=path.read_bytes(); require(sha(raw) == expected_hash and raw == canon(json.loads(raw.decode("ascii"))),"semantic_receipt_pin")
    for path,expected_hash in ((args.semantic_checker_result,SEMANTIC_RESULT_SHA),(args.semantic_checker_workflow_receipt,SEMANTIC_WORKFLOW_SHA)): raw=path.read_bytes(); require(sha(raw) == expected_hash and raw == canon(json.loads(raw.decode("ascii"))),"semantic_checker_receipt_pin")
    floor=load_exact(runtime["floor_v1"],SOURCE_HASHES["floor_v1"],"d972_r07_a0_c2fourier_joint_floor_v1"); g1=load_exact(runtime["grade1_v4"],SOURCE_HASHES["grade1_v4"],"d972_r07_a0_first_rung_grade1_v4"); p2=load_exact(runtime["prebuild_v1"],SOURCE_HASHES["prebuild_v1"],"d972_r07_a0_first_rung_grade2_prebuild_v1"); sem=load_exact(runtime["semantic_v5"],SOURCE_HASHES["semantic_v5"],"d972_r07_grade2_p1_componentwise_semantic_replay_v5"); p1v10=load_exact(runtime["p1_v10"],P1_V10_SHA,"d972_r07_canonical_p1_dag_degree2_lift_v10"); require(getattr(p2,"grade1",None) is g1 and getattr(g1,"floor",None) is floor,"runtime_transitive_identity")
    prepare,_,_=sem.authenticated_prepare(g1,Path(args.prepare_root).resolve()); structural=load_exact(runtime["structural_v1"],SOURCE_HASHES["structural_v1"],"task746_structural"); blocks=[]; block_roots=[]
    for index,path in enumerate(args.block_roots): safe,body,_=sem.block_envelope(path.resolve(),index,prepare,g1,structural); blocks.append(body); block_roots.append(safe)
    p1v10.validate_authenticated_dag(prepare,blocks); words_raw=runtime["words"].read_bytes(); words=json.loads(words_raw.decode("ascii")); require(sha(words_raw) == SOURCE_HASHES["words"],"words_pin"); task712=Task712Tables(Path(args.task712_root).resolve()); task712.receipt["complete_map"] = validate_complete_task712_maps(task712, words); p1_identity={"artifact":launch["p1_artifact"],"manifest_sha256":sha((Path(args.p1_root).resolve()/"manifest.json").read_bytes()),"cache_sha256":p1_manifest["cache"]["sha256"],"instruction":{key:value for key,value in p1_manifest["instruction"].items() if key != "path"},"ancestry_sha256":p1_manifest["ancestry_sha256"]}
    return {"p1v10":p1v10,"g1":g1,"p2":p2,"sem":sem,"prepare":prepare,"blocks":blocks,"prepare_root":Path(args.prepare_root).resolve(),"block_roots":block_roots,"words":words,"p1_instructions":p1_instructions,"p1_identity":p1_identity,"source_receipts":source_receipts,"executable_receipts":executable_receipts,"task712":task712,"task712_receipt":task712.receipt,"launch":launch,"p1_manifest":p1_manifest}


def path_free_receipts(receipts: dict[str,dict[str,Any]]) -> dict[str,dict[str,Any]]:
    return {name:{key:value for key,value in receipt.items() if key != "path"} for name,receipt in receipts.items()}


def path_free(value: Any) -> Any:
    if isinstance(value,dict): return {key:path_free(item) for key,item in value.items() if key != "path"}
    if isinstance(value,list): return [path_free(item) for item in value]
    return value


def _rss_bytes() -> int:
    """Return a measured resident-set value (Linux proc first, rusage fallback)."""
    try:
        fields=(Path("/proc/self/statm").read_text("ascii").split())
        if len(fields) >= 2:
            value=int(fields[1])*int(os.sysconf("SC_PAGE_SIZE"))
            if value > 0: return value
    except (OSError,ValueError,AttributeError):
        pass
    try:
        import resource
        value=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if value > 0:
            # Linux reports KiB; other supported runners may report bytes.
            return value * 1024 if value < (1 << 40) else value
    except (ImportError,OSError,ValueError):
        pass
    return 1


def _checkpoint_payload(stage: Path,cursor: int,rank: int,dependent: int,rolling: str,generation: int,previous_checkpoint_head: str,pins: dict[str,Any],digests: dict[str,str],started: float) -> dict[str,Any]:
    files={name:{"bytes":(stage/name).stat().st_size,"sha256":digests[name]} for name in ("coefficient.bin","lower.bin","top.bin","instructions.jsonl")}; return {"schema":CHECKPOINT_SCHEMA,"status":CHECKPOINT_STATUS,"cursor":cursor,"rank":rank,"dependent":dependent,"generation":generation,"previous_head":previous_checkpoint_head,"rolling_head":rolling,"head_link":{"previous_checkpoint_sha256":previous_checkpoint_head,"rolling_sha256":rolling},"files":files,"pins":pins,"wall_seconds":max(0.0,time.monotonic()-started),"rss_bytes":_rss_bytes(),"verified":False,"A0":False,"COMMON":False,"COFINAL_LIFT":False,"FAKE":False,"IHARA":False}


def write_checkpoint(stage: Path,cursor: int,rank: int,dependent: int,rolling: str,generation: int,previous_head: str,pins: dict[str,Any],digests: dict[str,str],started: float) -> None:
    temporary=stage/".checkpoint.json.tmp"; temporary.write_bytes(canon(_checkpoint_payload(stage,cursor,rank,dependent,rolling,generation,previous_head,pins,digests,started))); stream=temporary.open("r+b"); stream.flush(); os.fsync(stream.fileno()); stream.close(); os.replace(temporary,stage/"checkpoint.json")


def _record_shape(record: dict[str,Any],offer: int) -> None:
    require(set(record) == {"offer","kind","source","ell_sha256","g_sha256","reductions","lead","sigma","lower_zero","coefficient","lower","top","rank","dependent","rolling_sha256"},"instruction_exact_keys"); require(plain_int(record["offer"]) and record["offer"] == offer and record["kind"] in ("pivot","connection") and isinstance(record["source"],dict),"instruction_shape"); validate_source_receipt(record["source"],offer); require(isinstance(record["reductions"],list),"instruction_reductions")
    for item in record["reductions"]: require(isinstance(item,list) and len(item) == 2 and plain_int(item[0]) and 0 <= item[0] < offer and plain_int(item[1]) and item[1] in (1,2),"instruction_reduction_item")
    for key in ("ell_sha256","g_sha256"): require(isinstance(record[key],str) and len(record[key]) == 64,"instruction_digest")
    for key in ("coefficient","lower","top"): require(isinstance(record[key],dict) and set(record[key]) == {"offset","length","sha256"},"instruction_store_receipt")
    require(plain_int(record["coefficient"]["offset"]) and record["coefficient"]["offset"] == offer*COEFF_BYTES and record["coefficient"]["length"] == COEFF_BYTES,"instruction_coefficient_offset")
    require(plain_int(record["top"]["offset"]) and record["top"]["offset"] == offer*TOP_BYTES and record["top"]["length"] == TOP_BYTES,"instruction_top_offset")
    if record["kind"] == "pivot": require(plain_int(record["lower"]["offset"]) and record["lower"]["length"] == ELL_BYTES,"instruction_lower_offset")
    else: require(record["lower"] == {"offset":None,"length":ELL_BYTES,"sha256":None} and record["lower_zero"] is True,"instruction_connection_lower")
    require(plain_int(record["rank"]) and plain_int(record["dependent"]) and record["rank"] >= 0 and record["dependent"] >= 0 and isinstance(record["lower_zero"],bool) and (record["lead"] is None or plain_int(record["lead"])) and (record["sigma"] is None or (plain_int(record["sigma"]) and record["sigma"] in (1,2))),"instruction_counts")


def authenticate_resume(stage: Path,checkpoint_path: Path,pins: dict[str,Any],total_rows: int) -> tuple[dict[str,Any],str,dict[int,tuple[int,int,int,int]],dict[int,int],dict[str,hashlib._Hash]]:
    raw=checkpoint_path.read_bytes(); cp=json.loads(raw.decode("ascii")); require(raw == canon(cp),"checkpoint_canonical"); require(set(cp) == {"schema","status","cursor","rank","dependent","generation","previous_head","rolling_head","head_link","files","pins","wall_seconds","rss_bytes","verified","A0","COMMON","COFINAL_LIFT","FAKE","IHARA"},"checkpoint_exact_keys"); require(cp["schema"] == CHECKPOINT_SCHEMA and cp["status"] == CHECKPOINT_STATUS and cp["pins"] == pins and isinstance(cp["previous_head"],str) and len(cp["previous_head"]) == 64 and cp["head_link"] == {"previous_checkpoint_sha256":cp["previous_head"],"rolling_sha256":cp["rolling_head"]},"checkpoint_identity"); require(plain_int(cp["rss_bytes"]) and cp["rss_bytes"] > 0 and not isinstance(cp["wall_seconds"],bool) and isinstance(cp["wall_seconds"],(int,float)) and cp["wall_seconds"] >= 0,"checkpoint_measurements")
    cursor,checkpoint_rank,checkpoint_dependent=cp["cursor"],cp["rank"],cp["dependent"]; require(plain_int(cursor) and 0 <= cursor <= total_rows and plain_int(checkpoint_rank) and plain_int(checkpoint_dependent) and plain_int(cp["generation"]) and cp["generation"] >= 0 and checkpoint_rank+checkpoint_dependent == cursor,"checkpoint_cursor"); files=cp["files"]; require(isinstance(files,dict) and set(files) == {"coefficient.bin","lower.bin","top.bin","instructions.jsonl"},"checkpoint_files")
    for name in files: require(isinstance(files[name],dict) and set(files[name]) == {"bytes","sha256"} and plain_int(files[name]["bytes"]) and files[name]["bytes"] >= 0 and isinstance(files[name]["sha256"],str) and len(files[name]["sha256"]) == 64,"checkpoint_file_receipt")
    expected_lengths={"coefficient.bin":cursor*COEFF_BYTES,"top.bin":cursor*TOP_BYTES,"lower.bin":checkpoint_rank*ELL_BYTES};
    for name,length in expected_lengths.items(): require((stage/name).is_file() and (stage/name).stat().st_size >= length and files[name]["bytes"] == length,"checkpoint_store_length")
    ipath=stage/"instructions.jsonl"; require(ipath.is_file() and ipath.stat().st_size >= files["instructions.jsonl"]["bytes"],"checkpoint_instruction_length"); digesters={name:hashlib.sha256() for name in files}; pivots={}; leads={}; previous=ZERO_HEAD; instruction_bytes=0; saw=0; scan_rank=0; scan_dependent=0
    coeff=(stage/"coefficient.bin").open("rb"); lower=(stage/"lower.bin").open("rb"); top=(stage/"top.bin").open("rb")
    try:
        with ipath.open("rb") as instructions:
            for offer in range(cursor):
                line=instructions.readline(); require(line and line.endswith(b"\n"),"checkpoint_instruction_lf"); instruction_bytes += len(line); digesters["instructions.jsonl"].update(line); record=json.loads(line.decode("ascii")); require(line == canon(record),"checkpoint_instruction_canonical"); _record_shape(record,offer); require(record["rolling_sha256"] == sha(bytes.fromhex(previous)+canon({k:v for k,v in record.items() if k != "rolling_sha256"})),"checkpoint_rolling"); previous=record["rolling_sha256"]
                c=np.empty(COEFF_BYTES,dtype=np.uint8); t=np.empty(TOP_BYTES,dtype=np.uint8); coeff.seek(record["coefficient"]["offset"]); require(coeff.readinto(c) == COEFF_BYTES,"checkpoint_coefficient_eof"); validate_packed(c,ROWS); cb=c.tobytes(); require(sha(cb) == record["coefficient"]["sha256"],"checkpoint_coefficient_hash"); digesters["coefficient.bin"].update(cb); top.seek(record["top"]["offset"]); require(top.readinto(t) == TOP_BYTES,"checkpoint_top_eof"); validate_packed(t,TOP_WIDTH); tb=t.tobytes(); require(sha(tb) == record["top"]["sha256"],"checkpoint_top_hash"); digesters["top.bin"].update(tb)
                if record["kind"] == "pivot":
                    require(record["lower"]["offset"] == scan_rank*ELL_BYTES and record["lower"]["length"] == ELL_BYTES and record["lead"] not in leads,"checkpoint_lower_offset_or_duplicate"); l=np.empty(ELL_BYTES,dtype=np.uint8); lower.seek(record["lower"]["offset"]); require(lower.readinto(l) == ELL_BYTES,"checkpoint_lower_eof"); validate_packed(l,ELL_WIDTH); lb=l.tobytes(); require(sha(lb) == record["lower"]["sha256"],"checkpoint_lower_hash"); digesters["lower.bin"].update(lb); pivots[scan_rank]=(record["lead"],record["coefficient"]["offset"],record["lower"]["offset"],record["top"]["offset"]); leads[record["lead"]]=scan_rank; scan_rank += 1
                else: require(record["lower"] == {"offset":None,"length":ELL_BYTES,"sha256":None} and record["lower_zero"] is True,"checkpoint_connection_lower"); scan_dependent += 1
                saw += 1
    finally: coeff.close(); lower.close(); top.close()
    require(saw == cursor and scan_rank == checkpoint_rank and scan_dependent == checkpoint_dependent and previous == cp["rolling_head"] and instruction_bytes == files["instructions.jsonl"]["bytes"],"checkpoint_prefix_state"); require(all(digesters[name].hexdigest() == files[name]["sha256"] for name in files),"checkpoint_prefix_digest")
    for name,length in {**expected_lengths,"instructions.jsonl":instruction_bytes}.items():
        path=stage/name
        if path.stat().st_size > length:
            with path.open("r+b") as stream: stream.truncate(length); stream.flush(); os.fsync(stream.fileno())
    return cp,previous,pivots,leads,digesters


def _pair_getter(pairs: Any) -> Callable[[int], tuple[bytes,bytes,dict[str,Any]]]:
    if callable(pairs):
        return pairs
    require(hasattr(pairs,"__getitem__"),"pairs_must_be_indexable")
    return lambda index: pairs[index]


def validate_source_receipt(source: Any, offer: int) -> None:
    require(isinstance(source,dict) and set(source) == SOURCE_RECEIPT_KEYS,"source_receipt_shape")
    require(plain_int(source["node"]) and source["node"] == offer,"source_node")
    for key in ("instruction_sha256","p1_sha256","cache_row_sha256","predecessor","ancestry_sha256"):
        require(isinstance(source[key],str) and len(source[key]) == 64 and all(char in "0123456789abcdef" for char in source[key]),"source_receipt_digest")


def transduce(pairs: Any,stage: Path,total_rows: int,pins: dict[str,Any],stop_after: int | None = None,resume: bool = False) -> dict[str,Any]:
    started=time.monotonic(); stage=stage.resolve(); get_pair=_pair_getter(pairs)
    if resume:
        cp,rolling,pivots,lead_to_id,digesters=authenticate_resume(stage,stage/"checkpoint.json",pins,total_rows); cursor,rank,dependent,generation=cp["cursor"],cp["rank"],cp["dependent"],cp["generation"]; checkpoint_head=sha((stage/"checkpoint.json").read_bytes()); coeff=Store(stage/"coefficient.bin",COEFF_BYTES,ROWS,"r+b"); lower=Store(stage/"lower.bin",ELL_BYTES,ELL_WIDTH,"r+b"); top=Store(stage/"top.bin",TOP_BYTES,TOP_WIDTH,"r+b"); instructions=(stage/"instructions.jsonl").open("ab")
    else:
        require(not stage.exists(),"fresh_stage_must_not_exist"); stage.mkdir(parents=True,exist_ok=False); coeff=Store(stage/"coefficient.bin",COEFF_BYTES,ROWS,"w+b"); lower=Store(stage/"lower.bin",ELL_BYTES,ELL_WIDTH,"w+b"); top=Store(stage/"top.bin",TOP_BYTES,TOP_WIDTH,"w+b"); instructions=(stage/"instructions.jsonl").open("wb"); cursor=rank=dependent=generation=0; rolling=ZERO_HEAD; checkpoint_head=ZERO_HEAD; pivots={}; lead_to_id={}; digesters={name:hashlib.sha256() for name in ("coefficient.bin","lower.bin","top.bin","instructions.jsonl")}; write_checkpoint(stage,0,0,0,rolling,0,checkpoint_head,pins,{name:digesters[name].hexdigest() for name in digesters},started)
        checkpoint_head=sha((stage/"checkpoint.json").read_bytes())
    try:
        pivot_coeff=np.empty(COEFF_BYTES,dtype=np.uint8); pivot_lower=np.empty(ELL_BYTES,dtype=np.uint8); pivot_top=np.empty(TOP_BYTES,dtype=np.uint8)
        for offer in range(cursor,total_rows):
            ell,g,source=get_pair(offer); require(isinstance(ell,(bytes,bytearray)) and isinstance(g,(bytes,bytearray)) and len(ell) == ELL_BYTES and len(g) == TOP_BYTES,"pair_shape"); validate_source_receipt(source,offer); coefficient=np.zeros(COEFF_BYTES,dtype=np.uint8); coefficient[offer//4]=3**(offer%4); lower_acc=np.frombuffer(bytearray(ell),dtype=np.uint8); top_acc=np.frombuffer(bytearray(g),dtype=np.uint8); validate_packed(lower_acc,ELL_WIDTH); validate_packed(top_acc,TOP_WIDTH); reductions=[]
            while True:
                lead=first_nonzero_unchecked(lower_acc,ELL_WIDTH)
                if lead is None or lead[0] not in lead_to_id: break
                pivot_id=lead_to_id[lead[0]]; require(pivots[pivot_id][0] == lead[0],"pivot_lead_binding"); _,co_offset,lo_offset,go_offset=pivots[pivot_id]; coeff.read_into(co_offset,pivot_coeff); lower.read_into(lo_offset,pivot_lower); top.read_into(go_offset,pivot_top); axpy_inplace(coefficient,pivot_coeff,lead[1],ROWS); axpy_inplace(lower_acc,pivot_lower,lead[1],ELL_WIDTH); axpy_inplace(top_acc,pivot_top,lead[1],TOP_WIDTH); reductions.append([pivot_id,lead[1]])
            remainder=first_nonzero_unchecked(lower_acc,ELL_WIDTH); require(remainder is None or remainder[0] not in lead_to_id,"unreduced_or_duplicate_lead"); kind="pivot" if remainder is not None else "connection"; sigma=2 if remainder is not None and remainder[1] == 2 else (1 if remainder is not None else None)
            if sigma == 2: scale_two_inplace(coefficient,ROWS); scale_two_inplace(lower_acc,ELL_WIDTH); scale_two_inplace(top_acc,TOP_WIDTH)
            cbytes,lbytes,tbytes=coefficient.tobytes(),lower_acc.tobytes(),top_acc.tobytes(); co_offset=coeff.append(cbytes); go_offset=top.append(tbytes); lo_offset=lower.append(lbytes) if kind == "pivot" else None; digesters["coefficient.bin"].update(cbytes); digesters["top.bin"].update(tbytes)
            if lo_offset is not None: digesters["lower.bin"].update(lbytes)
            if kind == "pivot": require(remainder[0] not in lead_to_id,"duplicate_pivot_lead"); pivots[rank]=(remainder[0],co_offset,lo_offset,go_offset); lead_to_id[remainder[0]]=rank; rank += 1
            else: dependent += 1
            record={"offer":offer,"kind":kind,"source":dict(source),"ell_sha256":sha(ell),"g_sha256":sha(g),"reductions":reductions,"lead":remainder[0] if remainder else None,"sigma":sigma,"lower_zero":remainder is None,"coefficient":{"offset":co_offset,"length":COEFF_BYTES,"sha256":sha(cbytes)},"lower":{"offset":lo_offset,"length":ELL_BYTES,"sha256":sha(lbytes) if lo_offset is not None else None},"top":{"offset":go_offset,"length":TOP_BYTES,"sha256":sha(tbytes)},"rank":rank,"dependent":dependent}; record["rolling_sha256"]=sha(bytes.fromhex(rolling)+canon(record)); rolling=record["rolling_sha256"]; _record_shape(record,offer); line=canon(record); instructions.write(line); digesters["instructions.jsonl"].update(line); cursor=offer+1
            if cursor % CHECKPOINT_INTERVAL == 0 or (stop_after is not None and cursor >= stop_after):
                coeff.sync(); lower.sync(); top.sync(); instructions.flush(); os.fsync(instructions.fileno()); generation += 1; write_checkpoint(stage,cursor,rank,dependent,rolling,generation,checkpoint_head,pins,{name:digesters[name].hexdigest() for name in digesters},started); checkpoint_head=sha((stage/"checkpoint.json").read_bytes())
            if stop_after is not None and cursor >= stop_after: raise RuntimeError("UNKNOWN_RESOURCE:bounded_fixture_stop")
        coeff.sync(); lower.sync(); top.sync(); instructions.flush(); os.fsync(instructions.fileno()); instruction_bytes=(stage/"instructions.jsonl").stat().st_size; reduction_count=sum(1 for _ in _iter_reductions(stage/"instructions.jsonl")); manifest={"schema":CONNECTION_SCHEMA,"status":CONNECTION_STATUS,"offers":total_rows,"rank":rank,"dependent":dependent,"reduction_count":reduction_count,"source_ancestry":pins.get("p1_source_ancestry"),"p1_identity":pins.get("p1_identity"),"task712":pins.get("task712"),"coefficient":{"path":"coefficient.bin","rows":total_rows,"bytes":total_rows*COEFF_BYTES,"sha256":digesters["coefficient.bin"].hexdigest(),"eof":True},"lower":{"path":"lower.bin","rows":rank,"bytes":rank*ELL_BYTES,"sha256":digesters["lower.bin"].hexdigest(),"eof":True},"top":{"path":"top.bin","rows":total_rows,"bytes":total_rows*TOP_BYTES,"sha256":digesters["top.bin"].hexdigest(),"eof":True},"instruction":{"path":"instructions.jsonl","rows":total_rows,"bytes":instruction_bytes,"sha256":digesters["instructions.jsonl"].hexdigest(),"final_lf":True,"eof":True,"final_head":rolling},"final_rolling_head":rolling,"candidate_roster":["coefficient.bin","lower.bin","top.bin","instructions.jsonl","manifest.json"],**FALSE_FLAGS}; (stage/"manifest.json").write_bytes(canon(manifest)); return manifest
    finally: instructions.close(); coeff.close(); lower.close(); top.close()


def _iter_reductions(path: Path) -> Iterator[list[Any]]:
    with path.open("rb") as stream:
        for line in stream:
            if line.endswith(b"\n"): yield from json.loads(line.decode("ascii")).get("reductions",[])


def synthetic_pairs(n: int) -> list[tuple[bytes,bytes,dict[str,Any]]]:
    rows=[]
    for index in range(n):
        ell=np.zeros(ELL_WIDTH,dtype=np.uint8); ell[:index+1]=1; ell[index]=2 if index == 1 else 1; top=np.zeros(TOP_WIDTH,dtype=np.uint8); top[(index*13)%TOP_WIDTH]=(index%2)+1; source=sha(f"fixture-source-{index}".encode()); rows.append((pack(ell,ELL_WIDTH),pack(top,TOP_WIDTH),{"node":index,"instruction_sha256":source,"p1_sha256":source,"cache_row_sha256":sha(pack(top,TOP_WIDTH)),"predecessor":ZERO_HEAD,"ancestry_sha256":source}))
    if n > 3:
        top=pack(np.r_[np.array([2],dtype=np.uint8),np.zeros(TOP_WIDTH-1,dtype=np.uint8)],TOP_WIDTH); source=sha(b"fixture-zero-connection"); rows[3]=(bytes(ELL_BYTES),top,{"node":3,"instruction_sha256":source,"p1_sha256":source,"cache_row_sha256":sha(top),"predecessor":ZERO_HEAD,"ancestry_sha256":source})
    return rows


def benchmark() -> dict[str,Any]:
    n=128; pairs=synthetic_pairs(n)
    with tempfile.TemporaryDirectory(prefix="d972-v3-bench-") as td:
        start=time.perf_counter(); manifest=transduce(pairs,Path(td)/"stage",n,{"fixture":"benchmark"}); elapsed=max(1e-9,time.perf_counter()-start)
    rate=manifest["reduction_count"]/elapsed; return {"offers":n,"reductions":manifest["reduction_count"],"seconds":elapsed,"reductions_per_second":rate,"full_rank_upper_envelope_reductions":32469711,"full_rank_upper_envelope_seconds":32469711/rate,"cap_fit_claim":False}


def selftest() -> None:
    require(unpack(pack([0,1,2,0],4),4).tolist() == [0,1,2,0],"codec"); require(Task712Tables._spec("B_adj_a0.jsonl") == ("B",0,None,TOP_WIDTH,36288),"task712_adj_direction"); require(Task712Tables._spec("B_fwd_a0.jsonl") == ("B",0,None,36288,TOP_WIDTH),"task712_fwd_direction"); value=np.frombuffer(bytearray(pack([1,0,0,0],4)),dtype=np.uint8); axpy_inplace(value,value.copy(),1,4); require(first_nonzero(value,4) is None,"axpy")
    tiny_map = [(0, 1, 1), (1, 2, 2), (2, 3, 1)]; require(compare_complete_restriction(tiny_map, tiny_map, 3, 4, "task712_tiny_complete_map")["source_columns"] == 3, "task712_complete_fixture")
    fixture_rows=synthetic_pairs(1); row0=fixture_rows[0]; row3523=(row0[0],row0[1],{**row0[2],"node":3523,"instruction_sha256":sha(b"node3523"),"p1_sha256":sha(b"node3523"),"ancestry_sha256":sha(b"node3523")}); adapter=PhysicalSource.bounded_fixture({0:row0,3523:row3523}); adapter.pair(0); adapter.pair(3523); require(adapter.pair_calls == 2 and adapter.node_hits == {0:1,3523:1},"physical_pair_nodes")
    with tempfile.TemporaryDirectory(prefix="d972-v6-selftest-") as td:
        root=Path(td); raw=pack([1,0,0,0],4); store=Store(root/"positioned.bin",1,4,"w+b"); offset=store.append(raw); target=np.empty(1,dtype=np.uint8); store.read_into(offset,target); require(target.tobytes() == raw,"linux_append_preadv_visibility"); store.close(); pins={"p1_identity":{"fixture":"production-shaped-p1"},"p1_source_ancestry":{"fixture":"production-shaped-ancestry"},"runtime":{"producer":{"bytes":1,"sha256":"0"*64,"lf":1,"final_lf":True}},"task554":[{"role":"prepare","run":"1","attempt":"1","head":"0"*40,"id":1,"name":"prepare","archive_bytes":1,"digest":"sha256:"+"0"*64,"expires_at":"2099-01-01T00:00:00Z"}],"semantic_checker":{"role":"semantic-checker","run":"2","attempt":"1","head":"1"*40,"id":2,"name":"semantic","archive_bytes":1,"digest":"sha256:"+"1"*64,"expires_at":"2099-01-01T00:00:00Z"},"task712":{"fixture":"complete-task712-structural-map"},"launch_sha256":"2"*64}; full=root/"full"; transduce(PhysicalSource.bounded_fixture(synthetic_pairs(8)).pair,full,8,pins); stopped=root/"stopped"
        try: transduce(PhysicalSource.bounded_fixture(synthetic_pairs(8)).pair,stopped,8,pins,stop_after=4)
        except RuntimeError as exc: require(str(exc).startswith("UNKNOWN_RESOURCE"),"bounded_stop")
        cross=root/"cross-runner"; shutil.copytree(stopped,cross)
        with (cross/"top.bin").open("ab") as stream: stream.write(b"\x00")
        resume_source=PhysicalSource.bounded_fixture(synthetic_pairs(8)); transduce(resume_source.pair,cross,8,pins,resume=True); require(resume_source.node_hits == {4:1,5:1,6:1,7:1},"resume_cursor_direct")
        for name in ("coefficient.bin","lower.bin","top.bin","instructions.jsonl","manifest.json"): require((full/name).read_bytes() == (cross/name).read_bytes(),"cross_directory_resume")
    print(json.dumps({"selftest":"PASS","fresh_stage_owns_creation":True,"pair_node0":adapter.node_hits.get(0,0),"pair_node3523":adapter.node_hits.get(3523,0),"packed_kernel":"preadv_reusable_uint8_lookup","scale_two":"81_entry_lookup","resume":"one_pass_cross_directory_byte_equal","checkpoint_rss":"measured_nonzero","benchmark":benchmark(),"verified":False},sort_keys=True,separators=(",",":")))


def build(args: argparse.Namespace) -> None:
    bundle=authenticate_bundle(args); source=PhysicalSource(Path(args.p1_root).resolve(),bundle); ancestry=bundle["p1_manifest"]["source_ancestry"]; pins={"p1_identity":path_free(bundle["p1_identity"]),"p1_source_ancestry":path_free(ancestry),"runtime":path_free_receipts(bundle["source_receipts"]),"task554":[dict(x) for x in TASK554],"semantic_checker":dict(SEMANTIC_CHECKER),"task712":{**dict(TASK712_ARTIFACT),"tables":bundle["task712_receipt"]},"launch_sha256":sha(canon(bundle["launch"]))}
    require(all("path" not in json.dumps(value,ensure_ascii=True) for value in pins.values()),"pathful_checkpoint_pin")
    try:
        stage=Path(args.staging).resolve(); resume=args.resume_checkpoint is not None
        if resume: require(stage.is_dir() and (stage/"checkpoint.json").resolve() == Path(args.resume_checkpoint).resolve(),"resume_stage_checkpoint")
        manifest=transduce(source.pair,stage,ROWS,pins,resume=resume); require(manifest["offers"] == ROWS and manifest["rank"]+manifest["dependent"] == ROWS,"terminal_counts"); checkpoint_path=stage/"checkpoint.json"
        if checkpoint_path.exists(): checkpoint_path.unlink()
        require(sorted(path.name for path in stage.iterdir() if path.is_file()) == sorted(["coefficient.bin","lower.bin","top.bin","instructions.jsonl","manifest.json"]),"candidate_roster"); output=Path(args.out).resolve(); require(not output.exists(),"output_exists"); os.replace(stage,output)
    finally: source.close()


def parser() -> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description=__doc__); modes=parser.add_mutually_exclusive_group(required=True); modes.add_argument("--selftest",action="store_true"); modes.add_argument("--benchmark",action="store_true"); modes.add_argument("--build",action="store_true")
    for name in ("p1-root","prepare-root","launch-manifest","staging","out","resume-checkpoint","p1-v10","grade1","prebuild","semantic","structural","floor","words","task712-root"): parser.add_argument("--"+name,type=Path)
    parser.add_argument("--block-roots",nargs=4,type=Path); parser.add_argument("--semantic-receipts",nargs=6,type=Path); parser.add_argument("--semantic-checker-result",type=Path); parser.add_argument("--semantic-checker-workflow-receipt",type=Path); return parser


def main(argv: list[str] | None = None) -> int:
    args=parser().parse_args(argv)
    try:
        if args.selftest: selftest(); return 0
        if args.benchmark: print(json.dumps(benchmark(),sort_keys=True,separators=(",",":"))); return 0
        required=("p1_root","prepare_root","block_roots","launch_manifest","staging","out","resume_checkpoint","p1_v10","grade1","prebuild","semantic","structural","floor","words","task712_root","semantic_receipts","semantic_checker_result","semantic_checker_workflow_receipt")
        require(all(getattr(args,name) is not None for name in required if name != "resume_checkpoint"),"build_arguments"); build(args); return 0
    except RuntimeError as exc: print(json.dumps({"status":"UNKNOWN_RESOURCE","error":str(exc),"verified":False},separators=(",",":")),file=sys.stderr); return 2
    except Exception as exc: print(json.dumps({"status":"REJECTED","error":str(exc),"verified":False},separators=(",",":")),file=sys.stderr); return 1


if __name__ == "__main__": raise SystemExit(main())
