#!/usr/bin/env python3
"""R07 A0 compact finite-extension presentation owner.

The hot path is deliberately small: it reconstructs Gamma from the public
157ee transition receipt, chooses a deterministic index-three PC chain, and
emits the <=44 Tietze-substituted F(x,y) relators.  It never loads the old
adaptive checkpoint.  The physical eleven-occurrence closure is a later
consumer of this roster; absent its accepted boundary ABI this program emits
UNKNOWN_INPUT rather than silently falling back to the old search.
"""
from __future__ import annotations
import argparse, base64, gzip, hashlib, importlib.util, io, json, marshal, shutil, struct, sys, time
import os, tempfile
from types import SimpleNamespace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JOINT = Path("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json")
Q3 = Path("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json")
ROOF = Path("ci/in/d972_r07_seven_context_roof_presentation_v1.json")
ACCEPTANCE = Path("ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json")
PINS = {
    str(JOINT): (2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    str(Q3): (231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    str(ROOF): (31017244, "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"),
    str(ACCEPTANCE): (2722, "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"),
}
TASK379 = ("search/d972_r07_actual_a0_class_two_q2_v2.py", 50355,
           "125eb99d54764c546511741ac8eaefaa07c1fdaf2026117ee99fbfa4e6010627")
TASK198_WRAPPER = ("search/d972_r07_word_independent_successor_kernel_v12.py", 7209,
                   "816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5")
TASK198_V6 = ("search/d972_r07_word_independent_successor_kernel_v6.py", 219187,
              "aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a")
TASK179 = ("search/d972_r07_positive_common_word_colgen_v1.py", 123870,
           "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7")
G760 = ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409,
        "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f")
TASK176 = ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
           "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b")
G760_WORD_SHA256 = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
PASS = "R07_A0_COMPACT_PC_PRESENTATION_READY"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
class ResourceStop(RuntimeError):
    """A bounded production stop; never reinterpret this as NONMEMBER."""

def canon(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
def sha(v: Any) -> str: return hashlib.sha256(canon(v)).hexdigest()
def shab(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def fail(msg: str) -> None: raise RuntimeError(msg)
def resident_bytes() -> int | None:
    if sys.platform.startswith("linux"):
        try:
            for line in Path("/proc/self/status").read_text().splitlines():
                if line.startswith("VmRSS:"): return int(line.split()[1]) * 1024
        except (OSError, ValueError): return None
    return None
def resource_guard(started: float, seconds: float | None, rss_limit: int | None,
                   phase: str) -> int | None:
    elapsed = time.monotonic() - started
    if seconds is not None and elapsed >= seconds:
        raise ResourceStop("seconds:" + phase)
    rss = resident_bytes()
    if rss_limit is not None and rss is not None and rss >= rss_limit:
        raise ResourceStop("rss_bytes:" + phase)
    return rss
def emit_progress(phase: str, seed: int, rank: int, cursor: int, started: float) -> None:
    print("R07_A0_PROGRESS phase=%s seed=%d rank=%d cursor=%d rss=%s elapsed=%.3f" %
          (phase, seed, rank, cursor, resident_bytes(), time.monotonic()-started), flush=True)

def checkpoint_write(path: str, state: dict[str, Any]) -> None:
    target=Path(path)
    if target.is_absolute() or target.parent != Path("ci/out"): fail("checkpoint_path")
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent,prefix=".a0cp-payload-",delete=False) as stream:
        payload_path=Path(stream.name)
        # Stream marshal directly into gzip: production checkpoints never
        # materialize a second full payload in a BytesIO/string object.
        with gzip.GzipFile(fileobj=stream,mode="wb",compresslevel=1,mtime=0) as packed:
            marshal.dump({"schema":"d972-r07-a0-checkpoint/v2","state":state},packed)
        stream.flush(); os.fsync(stream.fileno())
    digest=hashlib.sha256(); size=0
    with payload_path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            digest.update(chunk); size+=len(chunk)
    with tempfile.NamedTemporaryFile(dir=target.parent,prefix=".a0cp-",delete=False) as stream:
        header=("D972-A0-CP2 "+digest.hexdigest()+" "+str(size)+"\n").encode("ascii"); stream.write(header)
        with payload_path.open("rb") as source: shutil.copyfileobj(source,stream,1024*1024)
        temporary=Path(stream.name)
    payload_path.unlink(missing_ok=True)
    os.replace(temporary,target)
def checkpoint_read(path: str) -> dict[str, Any]:
    target=Path(path)
    if target.is_absolute() or target.parent != Path("ci/out"): fail("resume_path")
    with target.open("rb") as stream:
        try:
            header=stream.readline().decode("ascii",errors="strict").rstrip("\n").split(" ")
            if len(header)!=3 or header[0]!="D972-A0-CP2" or len(header[1])!=64:
                fail("checkpoint_seal")
            expected,size=header[1],int(header[2])
            if size < 0 or any(c not in "0123456789abcdef" for c in expected): fail("checkpoint_seal")
        except (UnicodeError,TypeError,ValueError,RuntimeError) as exc:
            fail("checkpoint_header:"+str(exc))
        digest=hashlib.sha256(); seen=0
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            digest.update(chunk); seen+=len(chunk)
    if seen!=size or digest.hexdigest()!=expected: fail("checkpoint_payload_hash")
    with target.open("rb") as stream:
        stream.readline()
        try:
            with gzip.GzipFile(fileobj=stream,mode="rb") as packed: body=marshal.load(packed)
        except Exception as exc: fail("checkpoint_payload_decode:"+str(exc))
    if not isinstance(body,dict) or body.get("schema")!="d972-r07-a0-checkpoint/v2" or not isinstance(body.get("state"),dict): fail("checkpoint_payload_schema")
    return body["state"]
def checkpoint_payload(state: dict[str, Any]) -> bytes:
    if not isinstance(state,dict): fail("checkpoint_state_type")
    output=io.BytesIO()
    with gzip.GzipFile(fileobj=output,mode="wb",compresslevel=1,mtime=0) as packed:
        marshal.dump({"schema":"d972-r07-a0-checkpoint/v2","state":state},packed)
    return output.getvalue()
def checkpoint_payload_read(payload: bytes) -> dict[str,Any]:
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(payload),mode="rb") as packed: body=marshal.load(packed)
    except Exception as exc: fail("checkpoint_payload_decode:"+str(exc))
    if not isinstance(body,dict) or body.get("schema")!="d972-r07-a0-checkpoint/v2" or not isinstance(body.get("state"),dict): fail("checkpoint_payload_schema")
    return body["state"]
def pin(rel: Path) -> bytes:
    p = ROOT / rel; size, digest = PINS[str(rel)]
    if not p.is_file() or p.is_symlink(): fail("pin_missing:" + str(rel))
    b = p.read_bytes()
    if len(b) != size or shab(b) != digest: fail("pin_mismatch:" + str(rel))
    return b
def load(rel: Path) -> dict[str, Any]:
    b = pin(rel)
    try: v = json.loads(b.decode("ascii"))
    except Exception as e: raise RuntimeError("canonical_json:" + str(rel)) from e
    if not isinstance(v, dict): fail("object:" + str(rel))
    return v

def load_bound_module(pin_spec: tuple[str, int, str], name: str) -> dict[str, Any]:
    """Load a frozen owner into an isolated namespace after byte pinning."""
    path = ROOT / Path(pin_spec[0]); raw = path.read_bytes()
    if len(raw) != pin_spec[1] or shab(raw) != pin_spec[2]: fail("pin_mismatch:" + pin_spec[0])
    ns: dict[str, Any] = {"__name__": name, "__file__": str(ROOT / pin_spec[0])}
    exec(compile(raw, pin_spec[0], "exec"), ns, ns)
    return ns

def load_task198_core() -> Any:
    """Use the authenticated task379 loader for the direct runtime."""
    loader = load_bound_module(TASK379, "r07_task379_loader")
    load_task198 = loader.get("load_task198")
    if not callable(load_task198): fail("task198_loader_missing")
    return load_task198()

def direct_physical_owner(runtime: Any) -> tuple[dict[str, Any], list[int], Any]:
    """Bind task179's physical model to the direct task198 runtime."""
    owner = load_bound_module(TASK179, "r07_task179_physical")
    task176 = load_bound_module(TASK176, "r07_task176_physical")
    packed_joint_blob = task176.get("packed_joint_blob")
    if not callable(packed_joint_blob): fail("task176_blob_missing")
    owner["a0_element_blob"] = lambda value: packed_joint_blob(value, "task411 typed element")
    gowner = load_bound_module(G760, "r07_g760_owner")
    construct = gowner.get("construct_base")
    if not callable(construct): fail("g760_construct_missing")
    _, _, word = construct()
    if len(word) != 760 or sha(word) != G760_WORD_SHA256: fail("g760_word_pin")
    class Joint:
        def __init__(self) -> None:
            self.identity = self.eval([])
        def eval(self, word: list[int]) -> tuple[Any, ...]:
            return tuple(state.a for state in runtime.states_direct(word))
    adapter = {"old": runtime.old, "e3": runtime.e3, "e4": runtime.e4,
               "bridge": {"g760": {"word": list(word)}},
               "p176": SimpleNamespace(packed_joint_blob=packed_joint_blob),
               "joint_group": Joint()}
    model_class = owner.get("AllSevenModel")
    if not callable(model_class): fail("task179_model_missing")
    return owner, list(word), model_class(adapter)

def direct_runtime_helpers(runtime: Any, owner: dict[str, Any], g760: list[int],
                           ledger: list[dict[str, Any]], model: Any) -> Any:
    """Return the small occurrence ABI formerly reached through v3 globals."""
    element_token = owner.get("element_token")
    if not callable(element_token):
        def element_token(value: Any) -> str:
            if isinstance(value, tuple) and len(value) == 2 and all(isinstance(x, bytes) for x in value):
                return value[0].hex() + value[1].hex()
            return canon(value).hex()
    base_states = runtime.states_direct(g760)
    actor_cache: dict[tuple[int, int], tuple[Any, Any]] = {}
    for item in ledger:
        ordinal = int(item["ordinal"]); index = int(item["ten_index"])
        quotient = runtime.e3 if item["type"] == "E3" else runtime.e4
        prefix = quotient.identity
        for prior_ordinal in item.get("fox_prefix_occurrences", ()):
            prior = ledger[int(prior_ordinal) - 1]
            prior_state = base_states[int(prior["ten_index"])]
            prefix = quotient.mul(prefix, prior_state.a if int(prior["factor_sign"]) > 0 else quotient.inverse(prior_state.a))
        current = base_states[index]
        conjugator = quotient.mul(prefix, current.a) if int(item["factor_sign"]) > 0 else prefix
        for letter in (1, -1, 2, -2):
            rho = runtime.actors[index, letter].a
            actor_cache[ordinal, letter] = (quotient, quotient.mul(quotient.mul(conjugator, rho), quotient.inverse(conjugator)))
    def apply_actor_local(row: dict[str, int], letter: int, _ledger: Any) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, value in row.items():
            ordinal, component, token = str(key).split(":", 2)
            item = ledger[int(ordinal[1:]) - 1]
            quotient, actor = actor_cache[int(ordinal[1:]), letter]
            raw = bytes.fromhex(token); cut = 36 if item["type"] == "E3" else 144
            element = (raw[:cut], raw[cut:]); moved = element_token(quotient.mul(actor, element))
            new = ordinal + ":" + component + ":" + moved
            coefficient = (out.get(new, 0) + int(value)) % 3
            if coefficient: out[new] = coefficient
            else: out.pop(new, None)
        return out
    def aggregate_local(row: dict[str, int], _ledger: Any) -> dict[bytes, int]:
        out: dict[bytes, int] = {}
        blocks = {"H1": 1, "H2": 2, "P1": 3, "P2": 3, "P3": 3,
                  "P4": 3, "P5": 3}
        for key, value in row.items():
            ordinal, component, token = str(key).split(":", 2)
            block = blocks[str(ledger[int(ordinal[1:]) - 1]["block"])]
            raw = bytes.fromhex(token); flat = b"R" + bytes((block, int(component))) + len(raw).to_bytes(2, "big") + raw
            coefficient = (out.get(flat, 0) + int(value)) % 3
            if coefficient: out[flat] = coefficient
            else: out.pop(flat, None)
        return out
    return SimpleNamespace(BASE_STATES=base_states, PHYSICAL_G=list(g760),
                           PHYSICAL_MODEL=model, element_token=element_token,
                           apply_actor=apply_actor_local, aggregate_tagged=aggregate_local)
def acceptance_ok(v: dict[str, Any]) -> bool:
    member = v.get("receipt", {}).get("sha256") == PINS[str(ROOF)][1]
    verdict = v.get("checker_verdict", {})
    return (v.get("accepted") is True and v.get("independent") is True and
            v.get("accepted_receipt_basename") == ROOF.name and member and
            verdict.get("accepted") is True and verdict.get("independent") is True and
            verdict.get("receipt_terminal") == "ROOF_BRIDGE_ISOMORPHISM")
def unpack(field: dict[str, Any], encoding: str) -> list[int]:
    raw = base64.b64decode(field["base64"], validate=True)
    if field["encoding"] != encoding or len(raw) != field["byte_length"]:
        fail("packed_schema")
    if shab(raw) != field["sha256"]: fail("packed_sha")
    if encoding == "u16-le":
        if len(raw) % 2: fail("u16_width")
        out = [struct.unpack_from("<H", raw, i)[0] for i in range(0, len(raw), 2)]
    else: out = list(raw)
    if len(out) != field["count"] or sha(out) != field["decoded_sha256"]: fail("packed_decode")
    return out
def reduce_word(w: list[int]) -> list[int]:
    out: list[int] = []
    for a in w:
        if out and out[-1] == -a: out.pop()
        else: out.append(a)
    return out
def inv_word(w: list[int]) -> list[int]: return [-x for x in reversed(w)]
def mul_word(*parts: list[int]) -> list[int]:
    out: list[int] = []
    for p in parts: out = reduce_word(out + p)
    return out
def pow_word(word: list[int], exponent: int) -> list[int]:
    if exponent < 0: return pow_word(inv_word(word), -exponent)
    out: list[int] = []
    for _ in range(exponent): out = mul_word(out, word)
    return out

class Gamma:
    def __init__(self, receipt: dict[str, Any], q3: dict[str, Any]):
        g = receipt["gamma"]
        if g["order"] != 243 or g["greedy_generator_count"] != 4:
            fail("gamma_invariants")
        self.n = 243; self.m = 26
        flat = unpack(g["transitions"], "u16-le")
        self.t = [[x-1 for x in flat[i*self.m:(i+1)*self.m]] for i in range(self.n)]
        self.parent = [x-1 for x in unpack(g["section_parent_states"], "u16-le")]
        self.parent_gen = [x-1 for x in unpack(g["section_parent_generators"], "u8")]
        if self.parent[0] != -1 or len(self.parent) != self.n: fail("gamma_parents")
        self.sections: list[list[int]] = []
        for s in range(self.n):
            f: list[int] = []
            while s:
                if self.parent[s] < 0 or self.parent_gen[s] < 0: fail("gamma_section")
                f.append(self.parent_gen[s]); s = self.parent[s]
            self.sections.append(list(reversed(f)))
        self.gen_state = [self.t[0][j] for j in range(self.m)]
        self.inv_state = []
        for a in range(self.n):
            hits = [b for b in range(self.n) if self.mul(a,b) == 0 and self.mul(b,a) == 0]
            if len(hits) != 1: fail("gamma_inverse")
            self.inv_state.append(hits[0])
        records = q3["correction_fibre"]["records"][1:]
        if len(records) != 26: fail("record_count")
        self.words = [list(r["word"]) for r in records]
        if sum(map(len, self.words)) != 3054 or sha(self.words) != receipt["record_manifest"]["words_sha256"]:
            fail("record_words")
    def mul(self, a: int, b: int) -> int:
        s = a
        for j in self.sections[b]: s = self.t[s][j]
        return s
    def pow(self, a: int, e: int) -> int:
        s = 0
        for _ in range(e): s = self.mul(s, a)
        return s
    def closure(self, gens: list[int]) -> set[int]:
        gs = list(dict.fromkeys(gens + [self.inv_state[x] for x in gens])); seen = {0}; q = [0]
        while q:
            a = q.pop(0)
            for b in gs:
                c = self.mul(a,b)
                if c not in seen: seen.add(c); q.append(c)
        return seen
    def normal(self, h: set[int], k: set[int]) -> bool:
        return all(self.mul(self.mul(self.inv_state[a], b), a) in h for a in k for b in h)
    def pc_chain(self) -> tuple[list[int], list[set[int]]]:
        gens: list[int] = []; hs = [{0}]
        for level in range(1, 6):
            picked = None
            for c in range(1, self.n):
                if c in hs[-1]: continue
                k = self.closure(gens + [c])
                if len(k) == 3**level and self.normal(hs[-1], k): picked = c; break
            if picked is None: fail("pc_chain_not_found")
            gens.append(picked); hs.append(self.closure(gens))
        if len(hs[-1]) != 243: fail("pc_chain_order")
        return gens, hs
    def normal_forms(self, gens: list[int]) -> dict[int, tuple[int,...]]:
        out: dict[int, tuple[int,...]] = {}
        def go(i: int, state: int, exps: tuple[int,...]) -> None:
            if i == len(gens): out[state] = exps; return
            s = state
            for e in range(3): go(i+1, s, exps+(e,)); s = self.mul(s, gens[i])
        go(0, 0, ())
        if len(out) != 243: fail("pc_normal_forms")
        return out
    def source(self, state: int) -> list[int]:
        out: list[int] = []
        for j in self.sections[state]: out = mul_word(out, self.words[j])
        return out

def q0_relators() -> list[list[int]]:
    # Frozen factor presentation constants are public source data.  This
    # local implementation is intentionally independent of the producer.
    spec = importlib.util.spec_from_file_location("_qstar_constants", ROOT/"search/d972_b345_joint_kernel_qstar_closure_v1.py")
    if spec is None or spec.loader is None: fail("qstar_source")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    def sub(row: list[int], a: list[int], b: list[int]) -> list[int]:
        out: list[int] = []
        for x in row: out = mul_word(out, a if x == 1 else inv_word(a) if x == -1 else b if x == 2 else inv_word(b))
        return out
    p = [sub(r, mod.SPLIT_WORDS[0], mod.SPLIT_WORDS[1]) for r in mod.P_RELATORS]
    g = [sub(r, mod.SPLIT_WORDS[2], mod.SPLIT_WORDS[3]) for r in mod.G9_RELATORS]
    cross = [mul_word(inv_word(a), inv_word(b), a, b) for a in mod.SPLIT_WORDS[:2] for b in mod.SPLIT_WORDS[2:]]
    split = [mul_word([1], inv_word(mul_word(mod.SPLIT_WORDS[0], mod.SPLIT_WORDS[2]))),
             mul_word([2], inv_word(mul_word(mod.SPLIT_WORDS[1], mod.SPLIT_WORDS[3])))]
    ans = p+g+cross+split
    if len(ans) != 19 or sha(ans) != "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a": fail("q0_relator_manifest")
    return ans

def compact(receipt: dict[str, Any], q3: dict[str, Any]) -> dict[str, Any]:
    ga = Gamma(receipt, q3); gens, hs = ga.pc_chain(); nf = ga.normal_forms(gens)
    src = [ga.source(s) for s in gens]
    def nfword(state: int) -> list[int]:
        e = nf[state]; out: list[int] = []
        for i, x in enumerate(e): out = mul_word(out, src[i]*x)
        return out
    internal: list[list[int]] = []
    for i, s in enumerate(gens): internal.append(mul_word(src[i], src[i], src[i], inv_word(nfword(ga.pow(s,3)))))
    for j in range(1,5):
        for i in range(j):
            target = ga.mul(ga.mul(ga.inv_state[gens[j]], gens[i]), gens[j])
            internal.append(mul_word(inv_word(src[j]), src[i], src[j], inv_word(nfword(target))))
    ar = receipt["action_relations"]["rows"]
    actions: list[list[int]] = []
    # rows are record,x/y, orientation; the first orientation is u^-1 r u.
    for s, sw in zip(gens, src):
        for letter_index, letter in ((0,[1]), (1,[2])):
            # Endpoint is obtained by composing the authenticated 26-record
            # action table; use the section factors of the PC state and the
            # first-orientation row for each record.
            state = s
            for rec in ga.sections[s]:
                rr = next(r for r in ar if r[0] == rec+1 and r[1] == letter_index+1 and r[2] == 1)
                state = rr[3]-1
            # The table is a homomorphic action, so evaluate source action by
            # direct record conjugation composition, starting at identity.
            state = 0
            for rec in ga.sections[s]:
                rr = next(r for r in ar if r[0] == rec+1 and r[1] == letter_index+1 and r[2] == 1)
                state = ga.mul(state, rr[3]-1)
            rhs = nfword(state)
            actions.append(mul_word(inv_word(letter), sw, letter, inv_word(rhs)))
    qrows = receipt["q0_relations"]["rows"]
    qrels = q0_relators(); defects = []; registered_q0 = []
    for idx, word in enumerate(qrels):
        state = qrows[idx][2]-1
        defects.append(mul_word(word, inv_word(nfword(state))))
        registered_q0.append(mul_word(word, inv_word(ga.source(state))))
    if sha(registered_q0) != "bf24506f259414c3d375d5291c3014f1478b9b4ea73d389c07b7d10b07c82dc5": fail("registered_q0_manifest")
    if [len(registered_q0[i-1]) for i in (3,9,12)] != [190,344,902]: fail("registered_q0_lengths")
    rels = internal + actions + defects
    if len(rels) > 44: fail("compact_relator_count")
    lengths=[len(x) for x in rels]
    return {"gamma_order":243,"pc_length":5,"pc_generators":gens,
            "pc_relative_orders":[3]*5,"pc_internal_relator_count":len(internal),
            "action_relator_count":len(actions),"q0_defect_count":len(defects),
            "compact_relator_count":len(rels),"pc_source_words":src,
            "relators":rels,"relators_sha256":sha(rels),
            "registered_q0_relators_sha256":sha(registered_q0),"registered_q0_relators":registered_q0,
            "phase_metrics":{"compact_presentation":{"word_letters_total":sum(lengths),"word_letters_max":max(lengths),"row_count":len(rels),"frontier_nnz":0,"serialized_worker_batch_bytes":0,"owner_rss_bytes":None,"worker_rss_bytes":None}},
            "pc_state_normal_form_count":len(nf),"gamma_transition_sha256":receipt["gamma"]["transition_rows_sha256"],
            "deterministic_policy":"first state in ascending order extending a normal index-three chain"}

def fixture() -> dict[str, Any]:
    # Tiny C3 extension: one seed, one action, duplicate annihilation.
    row = {"seed": [1,0,0], "action": [0,1,0], "duplicate": True,
           "payload": {"frontier": [[0,1,0]], "reducer": False},
           "checkpoint": {"rank":1,"cursor":1,"ancestry":"a1"},
           "resume": {"rank":1,"cursor":1,"ancestry":"a1"},
           "mutations_rejected":["relator","action_endpoint","checkpoint_node"]}
    if row["checkpoint"] != row["resume"]: fail("fixture_resume")
    full_state={"phase":"occurrence","pivots":{1:{2:1}},"order":[1],"frontier":[({"k":1},"n")],"dag":{"n":{"kind":"LEAF"}},"cursor":1}
    if checkpoint_payload_read(checkpoint_payload(full_state)) != full_state: fail("fixture_stream_roundtrip")
    mutated=bytearray(checkpoint_payload(full_state)); mutated[0] ^= 1
    try:
        checkpoint_payload_read(bytes(mutated))
    except RuntimeError:
        pass
    else:
        fail("fixture_stream_mutation_accepted")
    row["status"] = "FIXTURE_PASS"; return row

def add_sparse(left: dict[Any, int], right: dict[Any, int], scale: int = 1) -> dict[Any, int]:
    out = dict(left)
    for key, value in right.items():
        value = (out.get(key, 0) + scale * int(value)) % 3
        if value: out[key] = value
        else: out.pop(key, None)
    return out

def intern_node(nodes: dict[str, dict[str, Any]], kind: str, **payload: Any) -> str:
    key = sha({"kind": kind, **payload})
    nodes.setdefault(key, {"kind": kind, **payload})
    return key

def reduce_insert(raw: dict[Any, int], pivots: dict[Any, dict[Any, int]],
                  pivot_order: list[Any] | None = None) -> tuple[bool, dict[Any, int]]:
    work = dict(raw)
    order = pivot_order if pivot_order is not None else sorted(pivots)
    for pivot in order:
        coefficient = work.get(pivot, 0)
        if coefficient:
            for key, value in pivots[pivot].items():
                updated = (work.get(key, 0) - coefficient * int(value)) % 3
                if updated: work[key] = updated
                else: work.pop(key, None)
    if not work: return False, {}
    pivot = min(work); scale = 1 if work[pivot] == 1 else 2
    work = {key: (scale * value) % 3 for key, value in work.items()}
    pivots[pivot] = work
    if pivot_order is not None: pivot_order.append(pivot)
    return True, work

def reduce_only(raw: dict[Any, int], pivots: dict[Any, dict[Any, int]],
                pivot_order: list[Any]) -> dict[Any, int]:
    work = dict(raw)
    for pivot in pivot_order:
        coefficient = work.get(pivot, 0)
        if coefficient:
            for key, value in pivots[pivot].items():
                updated = (work.get(key, 0) - coefficient * int(value)) % 3
                if updated: work[key] = updated
                else: work.pop(key, None)
    return work

class KeyInterner:
    """Keep one canonical coordinate object while sparse rows use integers."""
    def __init__(self) -> None:
        self.forward: dict[Any, int] = {}; self.reverse: list[Any] = []
    def key(self, value: Any) -> int:
        if value not in self.forward:
            self.forward[value] = len(self.reverse); self.reverse.append(value)
        return self.forward[value]
    def value(self, ident: int) -> Any: return self.reverse[int(ident)]
    def encode(self, row: dict[Any, int]) -> dict[int, int]:
        return {self.key(k): int(v) % 3 for k, v in row.items() if int(v) % 3}
    def decode(self, row: dict[int, int]) -> dict[Any, int]:
        return {self.value(k): int(v) % 3 for k, v in row.items() if int(v) % 3}

def expression_insert(raw: dict[Any, int], pivots: dict[Any, dict[Any, int]],
                      pivot_order: list[Any], pivot_expr: dict[Any, str],
                      source: tuple[str, dict[str, Any]], nodes: dict[str, dict[str, Any]]) -> tuple[bool, dict[Any, int], str | None]:
    """Echelon insertion with a compact hash-consed expression reference."""
    work = dict(raw); pending: list[str] = []
    def node(kind: str, **payload: Any) -> str:
        key = sha({"kind": kind, **payload})
        if key not in nodes: nodes[key] = {"kind": kind, **payload}; pending.append(key)
        return key
    expr = node(source[0], **source[1])
    for pivot in pivot_order:
        coefficient = work.get(pivot, 0)
        if coefficient:
            term = pivot_expr[pivot]
            factor=(-coefficient) % 3
            if factor != 1: term = node("SCALE", child=term, coefficient=factor)
            expr = node("ADD", left=expr, right=term)
            for key, value in pivots[pivot].items():
                updated = (work.get(key, 0) - coefficient * int(value)) % 3
                if updated: work[key] = updated
                else: work.pop(key, None)
    if not work:
        for key in pending:
            if key not in pivot_expr.values(): nodes.pop(key, None)
        return False, {}, None
    pivot = min(work); scale = 1 if work[pivot] == 1 else 2
    if scale != 1: expr = node("SCALE", child=expr, coefficient=scale)
    work = {key: (scale * value) % 3 for key, value in work.items() if (scale * value) % 3}
    pivots[pivot] = work; pivot_expr[pivot] = expr; pivot_order.append(pivot)
    return True, work, expr

def boundary_translate(row: dict[tuple[int, Any], int], quotient: Any,
                       translation: Any) -> dict[tuple[int, Any], int]:
    out: dict[tuple[int, Any], int] = {}
    for (component, value), coefficient in row.items():
        key = (component, quotient.mul(translation, value))
        out[key] = (out.get(key, 0) + int(coefficient)) % 3
        if not out[key]: out.pop(key, None)
    return out

def row_key(block: int, component: int, blob: bytes) -> bytes:
    return b"R" + bytes((block, component)) + len(blob).to_bytes(2, "big") + blob

def exponent_key(index: int) -> bytes: return b"E" + bytes((index,))

def serialize_gradient(owner: dict[str, Any], row: dict[tuple[int, Any], int],
                       block: int) -> dict[bytes, int]:
    out: dict[bytes, int] = {}
    for (component, value), coefficient in row.items():
        key = row_key(block, int(component), owner["a0_element_blob"](value))
        out[key] = (out.get(key, 0) + int(coefficient)) % 3
        if not out[key]: out.pop(key, None)
    return out

def exponent_pair(word: list[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in word),
            sum(1 if x == 2 else -1 if x == -2 else 0 for x in word))

def augmented_occurrence(mod: Any, runtime: dict[str, Any], word: list[int],
                         ledger: list[dict[str, Any]], states: Any = None) -> dict[Any, int]:
    if states is None:
        row: dict[Any, int] = dict(mod.term_vector(runtime, word, ledger))
    else:
        base10=mod.BASE_STATES or runtime.states_direct(mod.PHYSICAL_G or [])
        row={}
        for item in ledger:
            index=int(item["ten_index"]); state=states[index]; q=state.q; prefix=q.identity
            for ordinal in item.get("fox_prefix_occurrences", ()):
                prior=ledger[int(ordinal)-1]; prior_state=base10[int(prior["ten_index"])]
                prefix=q.mul(prefix,prior_state.a if int(prior["factor_sign"])>0 else q.inverse(prior_state.a))
            current=base10[index]; translate=q.mul(prefix,current.a) if int(item["factor_sign"])>0 else prefix
            for (component,element),value in state.u.items():
                moved=q.mul(translate,element); key="o"+str(int(item["ordinal"]))+":"+str(component)+":"+mod.element_token(moved)
                row[key]=(row.get(key,0)+int(item["factor_sign"])*int(value))%3
                if not row[key]: row.pop(key)
    e1, e2 = exponent_pair(word)
    for index, value in ((1, e1), (2, e2)):
        if value % 18: fail("epsilon_not_divisible_by_18")
        normalized = (value // 18) % 3
        if normalized: row["N:" + str(index)] = normalized
    return row

def augmented_actor(mod: Any, row: dict[Any, int], letter: int,
                    ledger: list[dict[str, Any]]) -> dict[Any, int]:
    ordinary = {k: v for k, v in row.items() if not str(k).startswith(("E:", "N:"))}
    out = mod.apply_actor(ordinary, letter, ledger)
    for key in ("N:1", "N:2"):
        if key in row: out[key] = row[key]
    return out

def aggregate_augmented(mod: Any, row: dict[Any, int],
                        ledger: list[dict[str, Any]]) -> dict[bytes, int]:
    ordinary = {k: v for k, v in row.items() if not str(k).startswith(("E:", "N:"))}
    out = dict(mod.aggregate_tagged(ordinary, ledger))
    for index in (1, 2):
        value = int(row.get("N:" + str(index), 0)) % 3
        if value: out[b"N" + bytes((index,))] = value
    return out

def actual_a0(compact_presentation: dict[str, Any], checkpoint: str | None = None,
              seconds: float | None = None, rss_limit: int | None = None,
              resume: str | None = None, roof_receipt: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run the v396 two-closure selector through the already frozen ABI.

    The direct task198 bootstrap keeps the physical owner and actor cache
    isolated.  The call is intentionally fail-closed on the Windows
    same-handle gate; GHA Linux supplies that ABI without the old adaptive
    search.
    """
    started = time.monotonic()
    resume_state: dict[str, Any] | None = None
    resume_cursor = 0
    if resume:
        resume_state=checkpoint_read(resume)
        if isinstance(resume_state.get("result"),dict): return resume_state["result"]
        if resume_state.get("phase") not in ("boundary_B3","boundary_B4","correction","legacy_oracle"):
            fail("checkpoint_phase_missing")
    # Build the task198 runtime from the authenticated v12/v6 bootstrap and
    # bind the physical owner directly, keeping only the small bridge receipt.
    core = load_task198_core(); resource_guard(started, seconds, rss_limit, "runtime_bootstrap")
    roof = roof_receipt if roof_receipt is not None else load(ROOF)
    authority = SimpleNamespace(receipt=roof)
    validate_layout_spec = load_bound_module(TASK379, "r07_task379_layout")
    validate_layout = validate_layout_spec.get("validate_layout")
    if not callable(validate_layout): fail("task198_layout_validator_missing")
    meter = core.Meter(dict(core.CAPS)); ledger = validate_layout(core, authority)
    try:
        runtime = core.Runtime(authority, meter)
    except getattr(core, "ResourceStop", RuntimeError) as exc:
        raise ResourceStop("task198:" + str(exc)) from exc
    except getattr(core, "InputStop", RuntimeError) as exc:
        fail("task198:" + str(exc))
    old, e3, e4 = runtime.old, runtime.e3, runtime.e4
    owner, g760_word, physical_model = direct_physical_owner(runtime)
    mod = direct_runtime_helpers(runtime, owner, g760_word, ledger, physical_model)
    del authority, roof

    def close_boundary(quotient: Any, degree: int, count: int, letters: tuple[int, ...], label: str):
        phase_name="boundary_"+label
        restored_state=None
        if resume_state is not None and label=="B3" and isinstance(resume_state.get("completed_b3"),dict):
            if resume_state.get("phase") not in ("boundary_B4","correction","legacy_oracle"): restored_state=None
            else: restored_state=resume_state.get("completed_b3")
        if resume_state is not None and label=="B4" and isinstance(resume_state.get("completed_b4"),dict):
            if resume_state.get("phase") in ("correction","legacy_oracle"): restored_state=resume_state.get("completed_b4")
        if isinstance(restored_state,dict):
            if resume_state.get("input_roster_sha256") != sha(compact_presentation["relators"]): fail("checkpoint_input_drift")
            if resume_state.get("source_pin_binding") != sha(PINS) or resume_state.get("ledger_binding") != sha(ledger): fail("checkpoint_boundary_binding_drift")
            saved=restored_state; inter=KeyInterner(); inter.reverse=list(saved["inter_reverse"])
            inter.forward={value:index for index,value in enumerate(inter.reverse)}
            pivots=dict(saved["pivots"]); order=list(saved["order"]); expr=dict(saved["expr"]); nodes=dict(saved["nodes"])
            if len(order)!=len(pivots) or len(expr)!=len(pivots): fail("checkpoint_boundary_shape")
            if any(not isinstance(pivot,int) or pivot<0 or pivot>=len(inter.reverse) or row.get(pivot)!=1
                   for pivot,row in pivots.items()): fail("checkpoint_boundary_pivot")
            if any(ref not in nodes for ref in expr.values()): fail("checkpoint_boundary_expr")
            return (inter,pivots,order,expr,nodes,list(saved["basis"]),[None for _ in saved.get("frontier",[])])
        inter = KeyInterner(); pivots: dict[int, dict[int, int]] = {}; order: list[int] = []
        expr: dict[int, str] = {}; nodes: dict[str, dict[str, Any]] = {}; frontier=[]; basis=[]
        restoring = (resume_state is not None and resume_state.get("phase")==phase_name
                     and (label != "B4" or "pivots" in resume_state))
        if restoring:
            saved=resume_state
            if saved.get("input_roster_sha256") != sha(compact_presentation["relators"]): fail("checkpoint_input_drift")
            if saved.get("source_pin_binding") != sha(PINS) or saved.get("ledger_binding") != sha(ledger): fail("checkpoint_boundary_binding_drift")
            inter.reverse=list(saved.get("inter_reverse",[])); inter.forward={value:index for index,value in enumerate(inter.reverse)}
            pivots=dict(saved.get("pivots",{})); order=list(saved.get("order",[])); expr=dict(saved.get("expr",{})); nodes=dict(saved.get("nodes",{})); basis=list(saved.get("basis",[]))
            raw_frontier=saved.get("frontier",[])
            if not isinstance(raw_frontier,list): fail("checkpoint_boundary_frontier_type")
            if any(not isinstance(entry,(list,tuple)) or len(entry)!=2 or not isinstance(entry[0],int)
                   for entry in raw_frontier): fail("checkpoint_boundary_frontier_shape")
            if any(entry[0] not in pivots or entry[1] not in nodes for entry in raw_frontier): fail("checkpoint_boundary_frontier_ref")
            frontier=[(pivots[entry[0]],entry[1]) for entry in raw_frontier]
            cursor=int(saved.get("cursor",0))
            if cursor != 0 or len(order)!=len(pivots) or len(expr)!=len(pivots): fail("checkpoint_boundary_shape")
            if any(not isinstance(pivot,int) or pivot<0 or pivot>=len(inter.reverse) or row.get(pivot)!=1
                   for pivot,row in pivots.items()): fail("checkpoint_boundary_pivot")
            if any(not isinstance(entry,tuple) or len(entry)!=2 or not isinstance(entry[0],dict) or not entry[0]
                   or pivots.get(min(entry[0])) != entry[0] or entry[1] not in nodes
                   for entry in frontier): fail("checkpoint_boundary_frontier")
            if any(ref not in nodes for ref in expr.values()): fail("checkpoint_boundary_expr")
        else:
            for index, relation in enumerate(old.pure_relations(degree)[:count], 1):
                grad, value = old.fox_gradient_without_sections(relation, quotient)
                if value != quotient.identity: fail(label + "_seed_value")
                raw = inter.encode({(int(c), e): int(v) % 3 for (c,e),v in grad.items() if int(v)%3})
                rise, row, ref = expression_insert(raw, pivots, order, expr, ("LEAF", {"family":label,"index":index}), nodes)
                basis.append({"index":index,"rank_rise":rise,"nnz":len(raw)})
                if rise: frontier.append((row, ref))
            cursor=0
        checkpoint_due=started+(0.80*seconds if seconds is not None else 300.0)
        progress_saved=False
        def save_boundary_checkpoint(position: int) -> None:
            nonlocal progress_saved
            if not checkpoint: return
            if position != 0 and (progress_saved or time.monotonic() < checkpoint_due): return
            remaining=[[min(entry[0]),entry[1]] for entry in frontier[position:] if entry is not None]
            state={"phase":phase_name,"degree":degree,"count":count,"cursor":0,
                "frontier":remaining,
                "input_roster_sha256":sha(compact_presentation["relators"]),"source_pin_binding":sha(PINS),
                "ledger_binding":sha(ledger),"inter_reverse":inter.reverse,"pivots":pivots,
                "order":order,"expr":expr,"nodes":nodes,"basis":basis}
            if label=="B4":
                state["completed_b3"]=b3_snapshot
            checkpoint_write(checkpoint,state)
            if position != 0: progress_saved=True
        if not restoring: save_boundary_checkpoint(0)
        while cursor < len(frontier):
            resource_guard(started, seconds, rss_limit, label + "_actions"); row,parent=frontier[cursor]; frontier[cursor]=None; cursor+=1
            if cursor == 1 or cursor % 32 == 0: emit_progress(label, 0, len(pivots), cursor, started)
            decoded=inter.decode(row)
            for letter in letters + tuple(-x for x in letters):
                candidate=inter.encode(boundary_translate(decoded, quotient, quotient.eval([letter])))
                rise,new,ref=expression_insert(candidate,pivots,order,expr,("CONJUGATE",{"letter":letter,"parent":parent}),nodes)
                if rise: frontier.append((new,ref))
            save_boundary_checkpoint(cursor)
        return inter,pivots,order,expr,nodes,basis,frontier

    def freeze_boundary(data: tuple[Any,...]) -> dict[str,Any]:
        return {"inter_reverse":list(data[0].reverse),"pivots":dict(data[1]),"order":list(data[2]),
                "expr":dict(data[3]),"nodes":dict(data[4]),"basis":list(data[5]),"frontier":[]}
    b3=close_boundary(e3,3,2,(1,2,3),"B3")
    b3_snapshot=freeze_boundary(b3)
    if checkpoint and (resume_state is None or resume_state.get("phase")=="boundary_B3"):
        checkpoint_write(checkpoint,{"phase":"boundary_B4","degree":4,"count":11,"cursor":0,
            "input_roster_sha256":sha(compact_presentation["relators"]),"source_pin_binding":sha(PINS),
            "ledger_binding":sha(ledger),"completed_b3":b3_snapshot})
    b4=close_boundary(e4,4,11,(1,2,3,4,5,6),"B4")
    b4_snapshot=freeze_boundary(b4)
    def tagged_boundary(data, block):
        inter,pivots,order,expr,nodes,basis,frontier=data; out={}; out_order=[]
        for pivot in order:
            row={}
            for (component,value),coefficient in inter.decode(pivots[pivot]).items():
                key=row_key(block,component,owner["a0_element_blob"](value)); row[key]=(row.get(key,0)+coefficient)%3
                if not row[key]: row.pop(key)
            reduce_insert(row,out,out_order)
        return out,out_order
    boundary_physical={}; boundary_physical_order=[]; boundary_expr={}; boundary_nodes={}
    for data,block in ((b3,1),(b3,2),(b4,3)):
        inter,pivots,local_order,local_expr,local_nodes,*_=data
        rows_order=local_order
        local_expr=data[3]; local_nodes=data[4]; boundary_nodes.update(local_nodes)
        for local_pivot in rows_order:
            row={}
            for (component,value),coefficient in inter.decode(pivots[local_pivot]).items():
                key=row_key(block,component,owner["a0_element_blob"](value))
                row[key]=(row.get(key,0)+coefficient)%3
                if not row[key]: row.pop(key)
            expression_insert(row,boundary_physical,boundary_physical_order,boundary_expr,
                              ("PHYSICAL",{"block":block,"child":local_expr[local_pivot]}),boundary_nodes)

    occ_inter=KeyInterner(); occurrence={}; occurrence_order=[]; occurrence_expr={}; nodes={}; frontier=[]; correction_basis=[]
    def parse_occurrence(raw):
        out={}
        for key,value in raw.items():
            if str(key).startswith("N:"):
                ident=occ_inter.key(("N",int(str(key).split(":",1)[1]))); out[ident]=(out.get(ident,0)+int(value))%3
                if not out[ident]: out.pop(ident,None)
                continue
            ordinal,component,token=str(key).split(":",2); blob=bytes.fromhex(token); block=ledger[int(ordinal[1:])-1]["type"]
            cut=36 if block=="E3" else 144; item=(int(ordinal[1:]),int(component),(blob[:cut],blob[cut:]))
            out[occ_inter.key(item)]=(out.get(occ_inter.key(item),0)+int(value))%3
            if not out[occ_inter.key(item)]: out.pop(occ_inter.key(item),None)
        return out
    def occurrence_strings(row):
        out={}
        for ident,value in row.items():
            item=occ_inter.value(ident)
            if item[0]=="N": out["N:"+str(item[1])]=value; continue
            ordinal,component,element=item
            key="o"+str(ordinal)+":"+str(component)+":"+mod.element_token(element); out[key]=(out.get(key,0)+int(value))%3
        return out
    def quotient_occurrence(row):
        groups={}
        for ident,value in row.items():
            item=occ_inter.value(ident)
            if item[0]=="N": continue
            ordinal,component,element=item; block=ledger[ordinal-1]["type"]
            groups.setdefault((ordinal,block),{})[(component,element)]=int(value)
        out={}
        for ident,value in row.items():
            item=occ_inter.value(ident)
            if item[0]=="N": out[ident]=value
        for (ordinal,block),group in groups.items():
            data=b3 if block in ("E3",) else b4; inter,pivots,order,*_=data
            reduced=reduce_only(inter.encode(group),pivots,order)
            for ident in [x for x in row if occ_inter.value(x)[0] != "N" and occ_inter.value(x)[0]==ordinal]: out.pop(ident,None)
            for (component,element),value in inter.decode(reduced).items():
                ident=occ_inter.key((ordinal,component,element)); out[ident]=value
        return out
    resume_closure = resume_state is not None and resume_state.get("phase") in ("correction","legacy_oracle")
    if resume_closure:
        if resume_state.get("input_roster_sha256") != sha(compact_presentation["relators"]): fail("checkpoint_input_drift")
        if resume_state.get("source_pin_binding") != sha(PINS) or resume_state.get("ledger_binding") != sha(ledger): fail("checkpoint_closure_binding_drift")
        saved_reverse=resume_state.get("occurrence_inter_reverse")
        if not isinstance(saved_reverse,list): fail("checkpoint_interner_missing")
        occ_inter.reverse=list(saved_reverse); occ_inter.forward={value:index for index,value in enumerate(occ_inter.reverse)}
        occurrence=dict(resume_state.get("occurrence_pivots",{})); occurrence_order=list(resume_state.get("occurrence_order",[]))
        occurrence_expr=dict(resume_state.get("occurrence_expr",{})); nodes.update(dict(resume_state.get("nodes",{})))
        frontier=[tuple(entry) if entry is not None else None for entry in resume_state.get("frontier",[])]
        cursor=int(resume_state.get("frontier_cursor",0))
        if cursor < 0 or cursor > len(frontier): fail("checkpoint_frontier_cursor")
        actor_binding=sha([(int(item["ordinal"]),int(item["ten_index"]),item["type"]) for item in ledger])
        if resume_state.get("actor_binding_sha256") != actor_binding: fail("checkpoint_actor_binding_drift")
    else:
        for ordinal,word in enumerate(compact_presentation["relators"],1):
            resource_guard(started,seconds,rss_limit,"correction_seeds"); states=runtime.states_direct(list(word))
            if any(state.a != state.q.identity for state in states): fail("compact_seed_not_joint_identity:"+str(ordinal))
            raw=augmented_occurrence(mod,runtime,list(word),ledger,states); parsed=parse_occurrence(raw)
            direct=mod.PHYSICAL_MODEL.occurrence_column([],list(word)); replay=aggregate_augmented(mod,raw,ledger)
            if {k:v for k,v in direct.items() if not k.startswith(b"E")} != {k:v for k,v in replay.items() if not k.startswith((b"E",b"N"))}: fail("seed_direct_replay")
            parsed=quotient_occurrence(parsed)
            rise,row,ref=expression_insert(parsed,occurrence,occurrence_order,occurrence_expr,("LEAF",{"seed":ordinal}),nodes)
            correction_basis.append({"seed":ordinal,"rank_rise":rise,"nnz":len(parsed)})
            if rise: frontier.append((min(row),ref))
        cursor=0
    checkpoint_due=started+(0.80*seconds if seconds is not None else 300.0)
    progress_saved=False
    def save_correction_checkpoint(position: int) -> None:
        nonlocal progress_saved
        if not checkpoint: return
        if position != 0 and (progress_saved or time.monotonic() < checkpoint_due): return
        remaining=[list(entry) for entry in frontier[position:] if entry is not None]
        checkpoint_write(checkpoint,{"phase":"correction","frontier_cursor":0,
            "frontier":remaining,
            "input_roster_sha256":sha(compact_presentation["relators"]),
            "source_pin_binding":sha(PINS),"ledger_binding":sha(ledger),
            "boundary_state_sha256":sha({"pivots":boundary_physical,"order":boundary_physical_order}),
            "occurrence_inter_reverse":occ_inter.reverse,"occurrence_pivots":occurrence,
            "occurrence_order":occurrence_order,"occurrence_expr":occurrence_expr,
            "nodes":nodes,"boundary_pivots":boundary_physical,"boundary_order":boundary_physical_order,
            "completed_b3":b3_snapshot,"completed_b4":b4_snapshot,
            "actor_binding_sha256":sha([(int(item["ordinal"]),int(item["ten_index"]),item["type"]) for item in ledger])})
        if position != 0: progress_saved=True
    if not resume_closure: save_correction_checkpoint(0)
    while cursor<len(frontier):
        resource_guard(started,seconds,rss_limit,"correction_actions"); entry=frontier[cursor];frontier[cursor]=None;cursor+=1
        if entry is None: continue
        pivot,parent=entry; row=occurrence[pivot]
        if cursor == 1 or cursor % 32 == 0: emit_progress("correction", 0, len(occurrence), cursor, started)
        for letter in (1,-1,2,-2):
            candidate=quotient_occurrence(parse_occurrence(augmented_actor(mod,occurrence_strings(row),letter,ledger)))
            rise,new,ref=expression_insert(candidate,occurrence,occurrence_order,occurrence_expr,("CONJUGATE",{"letter":letter,"parent":parent}),nodes)
            if rise: frontier.append((min(new),ref))
        save_correction_checkpoint(cursor)
    correction_physical={}; correction_physical_order=[]; correction_physical_expr={}; physical_nodes={}
    for pivot in occurrence_order:
        row=aggregate_augmented(mod,occurrence_strings(occurrence[pivot]),ledger)
        row=reduce_only(row,boundary_physical,boundary_physical_order)
        source=("PHYSICAL",{"child":occurrence_expr[pivot]})
        rise,new,ref=expression_insert(row,correction_physical,correction_physical_order,correction_physical_expr,source,physical_nodes)
    target={}; base_hex=old.hexagon_words(mod.PHYSICAL_G)
    for block,relation in ((1,old.embed_f2_pb3(base_hex[0])),(2,old.embed_f2_pb3(base_hex[1])),(3,mod.PHYSICAL_MODEL._pentagon_word(mod.PHYSICAL_G))):
        gradient,value=old.fox_gradient_without_sections(relation,e3 if block<3 else e4)
        if value!=(e3 if block<3 else e4).identity: fail("target_quotient_identity")
        target=add_sparse(target,serialize_gradient(owner,gradient,block),-1)
    work=reduce_only(target,boundary_physical,boundary_physical_order); target_bar=dict(work); target_coeff={}
    for pivot in correction_physical_order:
        coefficient=work.get(pivot,0)
        if coefficient:
            target_coeff[pivot]=coefficient; work=add_sparse(work,correction_physical[pivot],-coefficient)
    def separating_functional(remainder: dict[bytes, int]) -> tuple[dict[bytes, int], int]:
        """Construct a dual of the combined triangular boundary/correction basis."""
        combined_order=list(boundary_physical_order)+list(correction_physical_order)
        combined_rows={**boundary_physical, **correction_physical}
        trial=min(remainder)
        functional={trial: 1}
        for pivot in sorted(combined_rows, reverse=True):
                row=combined_rows[pivot]
                dot=sum(int(value)*int(functional.get(key,0)) for key,value in row.items() if key != pivot) % 3
                functional[pivot]=(-dot) % 3
                if not functional[pivot]: functional.pop(pivot,None)
        if all(sum(int(value)*int(functional.get(key,0)) for key,value in row.items()) % 3 == 0
               for row in combined_rows.values()):
            target_pair=sum(int(value)*int(functional.get(key,0)) for key,value in target.items()) % 3
            if target_pair:
                return functional,target_pair
        fail("dual_functional_not_found")
    def hot_metrics() -> dict[str, Any]:
        phases={}
        for label,pivots,front in (("boundary_B3",b3[1],b3[6]),("boundary_B4",b4[1],b4[6]),
                                   ("correction_occurrence",occurrence,frontier),
                                   ("correction_physical",correction_physical,[])):
            sizes=[len(row) for row in pivots.values()]
            live=[len(entry[0]) if isinstance(entry[0],dict) else len(pivots.get(entry[0],{}))
                  for entry in front if entry is not None]
            phases[label]={"row_nnz":sizes[-1] if sizes else 0,"row_nnz_max":max(sizes) if sizes else 0,
                           "total_pivot_nnz":sum(sizes),"frontier_nnz":sum(live),
                           "serialized_worker_batch_bytes":0,"owner_rss_bytes":resident_bytes(),"worker_rss_bytes":None}
        return phases
    def state_digest() -> str:
        return sha({"boundary_order":boundary_physical_order,"boundary_pivots":boundary_physical,
                    "occurrence_order":occurrence_order,"occurrence_pivots":occurrence,
                    "remainder":work})
    if resume_state is not None:
        expected=resume_state.get("closure_state_sha256")
        if expected is not None and expected != state_digest(): fail("checkpoint_closure_state_drift")
        if resume_state.get("phase")=="correction" and resume_state.get("boundary_state_sha256") != sha({"pivots":boundary_physical,"order":boundary_physical_order}): fail("checkpoint_boundary_state_drift")
        resume_cursor=int(resume_state.get("legacy_cursor",0))
        if resume_cursor < 0 or resume_cursor > 6441: fail("checkpoint_cursor")
    if work:
        checkpoint_due=started+(0.80*seconds if seconds is not None else 300.0)
        progress_saved=False
        def save_oracle_checkpoint(cursor: int) -> None:
            nonlocal progress_saved
            if not checkpoint: return
            if cursor != 0 and (progress_saved or time.monotonic() < checkpoint_due): return
            checkpoint_write(checkpoint,{"phase":"legacy_oracle","legacy_cursor":cursor,
                "input_roster_sha256":sha(compact_presentation["relators"]),
                "source_pin_binding":sha(PINS),"ledger_binding":sha(ledger),
                "closure_state_sha256":state_digest(),"boundary_pivots":boundary_physical,
                "boundary_order":boundary_physical_order,"occurrence_pivots":occurrence,
                "occurrence_order":occurrence_order,"occurrence_expr":occurrence_expr,
                "occurrence_inter_reverse":occ_inter.reverse,"frontier":[],"frontier_cursor":0,
                "correction_pivots":correction_physical,"correction_order":correction_physical_order,
                "correction_expr":correction_physical_expr,"nodes":{**boundary_nodes,**nodes,**physical_nodes},
                "remainder":work,"completed_b3":b3_snapshot,"completed_b4":b4_snapshot,
                "actor_binding_sha256":sha([(int(item["ordinal"]),int(item["ten_index"]),item["type"]) for item in ledger])})
            if cursor != 0: progress_saved=True
        save_oracle_checkpoint(0)
        oracle=load(ROOF); rows=oracle.get("Delta0",{}).get("presentation",{}).get("rows",[])
        if len(rows)!=6441: fail("legacy_oracle_roster_count")
        for ordinal,item in enumerate(rows):
            if ordinal < resume_cursor: continue
            resource_guard(started,seconds,rss_limit,"legacy_oracle")
            if ordinal == 0 or (ordinal + 1) % 128 == 0: emit_progress("legacy_oracle", ordinal + 1, len(occurrence), ordinal + 1, started)
            word=list(item["word"]); states=runtime.states_direct(word)
            if any(state.a != state.q.identity for state in states): fail("legacy_seed_not_joint_identity:"+str(ordinal+1))
            legacy=quotient_occurrence(parse_occurrence(augmented_occurrence(mod,runtime,word,ledger,states)))
            if reduce_only(legacy,occurrence,occurrence_order):
                result={"status":UNKNOWN_INPUT,"reason":"legacy_6441_seed_outside_compact_span","legacy_cursor":ordinal,"boundary_rank":len(boundary_physical),"occurrence_rank":len(occurrence),"remainder_nnz":len(work),"remainder_sha256":sha(sorted((k.hex(),int(v)) for k,v in work.items())),"phase_metrics":hot_metrics(),"normalized_exponent_coordinates_included":True,"seed_direct_replay_checked":True}
                break
            rows[ordinal]=None
            save_oracle_checkpoint(ordinal + 1)
        else:
            separator,target_pair=separating_functional(work)
            serial=[[key.hex(),int(value)] for key,value in sorted(separator.items(),key=lambda item:item[0])]
            result={"status":"NONMEMBER","member":False,"reason":"6441 legacy occurrence oracle exhausted","legacy_oracle_exhausted":True,"boundary_rank":len(boundary_physical),"occurrence_rank":len(occurrence),"remainder_nnz":len(work),"remainder_sha256":sha(sorted((k.hex(),int(v)) for k,v in work.items())),"separator":serial,"separator_sha256":sha(serial),"target_pair":target_pair,"phase_metrics":hot_metrics(),"normalized_exponent_coordinates_included":True,"seed_direct_replay_checked":True}
        del oracle,rows
        if checkpoint:
            checkpoint_write(checkpoint,{"phase":"closures_exhausted","input_roster_sha256":sha(compact_presentation["relators"]),"source_pin_binding":sha(PINS),"ledger_binding":sha(ledger),"result":result,"boundary_pivots":boundary_physical,"boundary_order":boundary_physical_order,"correction_pivots":correction_physical,"correction_order":correction_physical_order,"correction_expr":correction_physical_expr,"nodes":{**boundary_nodes,**nodes,**physical_nodes},"completed_b3":b3_snapshot,"completed_b4":b4_snapshot,"frontier_cursor":len(frontier)})
        return result
    def dag_atoms(root: str) -> dict[tuple[int, tuple[int, ...]], int]:
        """Flatten one expression DAG without recursive literal expansion."""
        atoms: dict[tuple[int, tuple[int, ...]], int] = {}; stack=[(root, (), 1)]
        while stack:
            ref,prefix,coefficient=stack.pop(); item=nodes.get(ref) or physical_nodes.get(ref)
            if item is None: fail("dag_ref")
            kind=item["kind"]
            if kind=="LEAF":
                key=(int(item["seed"]),tuple(prefix)); value=(atoms.get(key,0)+coefficient)%3
                if value: atoms[key]=value
                else: atoms.pop(key,None)
            elif kind=="CONJUGATE":
                stack.append((item["parent"],tuple(prefix)+(int(item["letter"]),),coefficient))
            elif kind=="SCALE":
                stack.append((item["child"],prefix,coefficient*int(item["coefficient"])%3))
            elif kind in ("ADD","PRODUCT"):
                stack.append((item["right"],prefix,coefficient)); stack.append((item["left"],prefix,coefficient))
            elif kind=="PHYSICAL": stack.append((item["child"],prefix,coefficient))
            else: fail("dag_kind")
        return atoms
    def boundary_atoms(root: str) -> dict[tuple[int, int, tuple[int, ...]], int]:
        atoms: dict[tuple[int,int,tuple[int,...]], int] = {}; stack=[(root,(),1,None)]
        while stack:
            ref,prefix,coefficient,block=stack.pop(); item=boundary_nodes.get(ref)
            if item is None: fail("boundary_dag_ref")
            kind=item["kind"]
            if kind=="LEAF":
                family=str(item.get("family")); b=block if block is not None else (1 if family=="B3" else 3)
                key=(b,int(item["index"]),tuple(prefix)); value=(atoms.get(key,0)+coefficient)%3
                if value: atoms[key]=value
                else: atoms.pop(key,None)
            elif kind=="PHYSICAL": stack.append((item["child"],prefix,coefficient,int(item["block"])))
            elif kind=="CONJUGATE": stack.append((item["parent"],tuple(prefix)+(int(item["letter"]),),coefficient,block))
            elif kind=="SCALE": stack.append((item["child"],prefix,coefficient*int(item["coefficient"])%3,block))
            elif kind in ("ADD","PRODUCT"):
                stack.append((item["right"],prefix,coefficient,block)); stack.append((item["left"],prefix,coefficient,block))
            else: fail("boundary_dag_kind")
        return atoms
    atom_coefficients: dict[tuple[int, tuple[int, ...]], int] = {}
    for pivot,coefficient in target_coeff.items():
        for atom,value in dag_atoms(correction_physical_expr[pivot]).items():
            updated=(atom_coefficients.get(atom,0)+int(coefficient)*int(value))%3
            if updated: atom_coefficients[atom]=updated
            else: atom_coefficients.pop(atom,None)
    cstar=[]
    for (seed,prefix),coefficient in sorted(atom_coefficients.items(), key=lambda item:(item[0][0],item[0][1])):
        atom=mul_word(list(prefix),list(compact_presentation["relators"][seed-1]),inv_word(list(prefix)))
        cstar=mul_word(cstar,atom if coefficient==1 else inv_word(atom))
    e1,e2=exponent_pair(cstar)
    if e1%54 or e2%54: fail("exactification_exponent_not_54_lattice")
    registered=compact_presentation.get("registered_q0_relators")
    if not registered: fail("registered_q0_words_missing")
    r3,r9,r12=registered[2],registered[8],registered[11]; v0=mul_word(r9,r12,inv_word(r3),inv_word(r3)); u0=mul_word(r9,pow_word(v0,-8)); h=mul_word(pow_word(u0,-3*(e1//54)),pow_word(v0,-3*(e2//54)))
    exact=mul_word(cstar,h); states=runtime.states_direct(exact)
    if any(state.a != state.q.identity for state in states) or exponent_pair(exact)!=(0,0): fail("exactification_replay")
    direct=mod.PHYSICAL_MODEL.occurrence_column([],exact); if_row={k:v for k,v in direct.items() if not k.startswith(b"E")}
    if reduce_only(if_row,boundary_physical,boundary_physical_order) != target_bar: fail("exactification_physical_row")
    boundary_coeff={}; residual=add_sparse(target,if_row,-1)
    for pivot in boundary_physical_order:
        coefficient=residual.get(pivot,0)
        if coefficient:
            boundary_coeff[pivot.hex()]=coefficient; residual=add_sparse(residual,boundary_physical[pivot],-coefficient)
    if residual: fail("typed_boundary_preimage")
    typed_atoms={}
    for pivot_hex,coefficient in boundary_coeff.items():
        pivot=bytes.fromhex(pivot_hex)
        for atom,value in boundary_atoms(boundary_expr[pivot]).items():
            updated=(typed_atoms.get(atom,0)+int(coefficient)*int(value))%3
            if updated: typed_atoms[atom]=updated
            else: typed_atoms.pop(atom,None)
    typed_boundary=[{"block":block,"base_relator_index":index,"translation_word":list(prefix),"coefficient":coefficient}
                    for (block,index,prefix),coefficient in sorted(typed_atoms.items(),key=lambda item:(item[0][0],item[0][1],item[0][2]))]
    rss=resident_bytes(); result={"status":"MEMBER","member":True,"boundary_rank":len(boundary_physical),"occurrence_rank":len(occurrence),"remainder_nnz":0,"remainder_sha256":sha([]),"phase_metrics":hot_metrics(),"normalized_exponent_coordinates_included":True,"seed_direct_replay_checked":True,"literal_correction":exact,"exact_exponent_pair":[0,0],"positive_certificate":True,"typed_boundary_preimage":typed_boundary,"boundary_pivot_coefficients":boundary_coeff,"progress":{"phase":"a0_member_exactified","frontier_cursor":len(frontier),"owner_rss_bytes":rss,"worker_rss_bytes":None},"ancestry":{"nodes":{**boundary_nodes,**nodes,**physical_nodes},"positive_certificate":True,"typed_boundary_preimage":True}}
    if checkpoint:
        checkpoint_write(checkpoint,{"phase":"member_exactified","input_roster_sha256":sha(compact_presentation["relators"]),"result":result,"boundary_pivots":boundary_physical,"boundary_order":boundary_physical_order,"correction_pivots":correction_physical,"correction_order":correction_physical_order,"correction_expr":correction_physical_expr,"nodes":{**boundary_nodes,**nodes,**physical_nodes},"frontier_cursor":len(frontier)})
    return result

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("FIXTURE","PRODUCTION"),default="PRODUCTION"); ap.add_argument("--output"); ap.add_argument("--checkpoint"); ap.add_argument("--resume"); ap.add_argument("--seconds",type=float,default=9000); ap.add_argument("--rss-bytes",type=int,default=5700000000)
    a=ap.parse_args(); started=time.monotonic()
    try:
        if a.mode == "FIXTURE": out=fixture()
        else:
            receipt=load(JOINT); q3=load(Q3); pin(ROOF); roof=None; roof_authenticated=True; acceptance=load(ACCEPTANCE)
            if not acceptance_ok(acceptance): fail("acceptance_v2_contract")
            if receipt.get("status") != "B345_JOINT_KERNEL_QSTAR_CLOSED" or q3.get("status") != "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION": fail("receipt_not_complete")
            pres=compact(receipt,q3)
            out={"schema":"d972-r07-a0-compact-pc-invariant-owner/v1","status":PASS,"terminal":PASS,"complete":True,"presentation":pres,"roof_input":{"path":str(ROOF),"bytes":PINS[str(ROOF)][0],"sha256":PINS[str(ROOF)][1],"authenticated":roof_authenticated},"acceptance_v2":{"path":str(ACCEPTANCE),"bytes":PINS[str(ACCEPTANCE)][0],"sha256":PINS[str(ACCEPTANCE)][1],"authenticated":acceptance_ok(acceptance)},"claim_boundary":{"compact_presentation":True,"occurrence_closure":False,"A0_membership":False,"common_word":False,"fake":False,"Ihara_witness":False},"progress":{"phase":"compact_presentation_complete","elapsed_seconds":time.monotonic()-started,"seed_ordinal":pres["compact_relator_count"],"rank":None,"frontier_cursor":0},"memory_contract":{"owner_state":"compact PC tables and literal relator DAG only","worker_payload_fields":["immutable action endpoint table","bounded sparse frontier rows"],"worker_inherits_reducer":False,"worker_inherits_checkpoint":False,"worker_inherits_ancestry":False,"dependent_traces_retained":False,"coordinate_ids_interned":True,"production_closure_metrics_pending":True}}
            out["memory_contract"]["parallel_owner_implemented"] = False
            out["memory_contract"]["checkpoint_resume_implemented"] = True
            out["memory_contract"]["checkpoint_resume_scope"] = "correction_frontier_and_oracle_cursor"
            try:
                out["a0"] = actual_a0(pres, a.checkpoint, a.seconds, a.rss_bytes, a.resume)
                if out["a0"].get("status") == "MEMBER" and out["a0"].get("positive_certificate") is not True:
                    out["a0"]["provisional_member"] = True
                    out["a0"]["status"] = UNKNOWN_RESOURCE
                    out["a0"]["reason"] = "positive ancestry/exactification not emitted; MEMBER cannot be promoted"
            except ResourceStop as exc:
                out["a0"] = {"status":UNKNOWN_RESOURCE,"reason":str(exc)}
            except (RuntimeError, ImportError, OSError) as exc:
                out["a0"] = {"status":UNKNOWN_INPUT,"reason":str(exc)}
            out["status"] = out["a0"]["status"]
            out["terminal"] = out["status"]
            out["complete"] = out["status"] in ("MEMBER", "NONMEMBER")
            if out["status"] in ("MEMBER", "NONMEMBER"):
                out["claim_boundary"]["occurrence_closure"] = True
            if out["status"] == "MEMBER" and out["a0"].get("positive_certificate") is True:
                out["claim_boundary"]["A0_membership"] = True
                out["claim_boundary"]["common_word"] = True
            out["next_gate"]={"status":out["a0"]["status"],"blocker":out["a0"].get("reason")}
        if a.output:
            p=ROOT/a.output; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(canon(out))
        print("R07_A0_COMPACT_PC_OWNER " + str(out.get("status")),flush=True); return 0
    except RuntimeError as e:
        out={"schema":"d972-r07-a0-compact-pc-invariant-owner/v1","status":UNKNOWN_INPUT,"terminal":UNKNOWN_INPUT,"complete":False,"reason":str(e),"claim_boundary":{"compact_presentation":False,"occurrence_closure":False,"A0_membership":False,"common_word":False,"fake":False,"Ihara_witness":False}}
        if a.output:
            p=ROOT/a.output; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(canon(out))
        print("R07_A0_COMPACT_PC_OWNER " + UNKNOWN_INPUT + ":" + str(e),flush=True); return 0
if __name__ == "__main__": raise SystemExit(main())
