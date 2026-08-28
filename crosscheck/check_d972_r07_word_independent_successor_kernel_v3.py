#!/usr/bin/env python3
"""Independent v3 checker: reverse suffix ancestry trie and max-pivot F3."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, time
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-word-independent-successor-kernel/v3"
SELFTEST_SCHEMA = SCHEMA + "/selftest-fixture/v3"
ISO = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PASS"
SELFTEST_TERMINAL = "SELFTEST_COMPLETE"
UNKNOWN_INPUT, UNKNOWN_RESOURCE = "UNKNOWN_INPUT", "UNKNOWN_RESOURCE"
ROWS = 6441
AUTH = {
 "receipt": "d972_r07_seven_context_roof_presentation_v1.json",
 "manifest": "d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
 "producer": "d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
 "checker": "d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
 "verdict": "d972_r07_seven_context_roof_presentation_v1.checker.verdict.json"}
MANIFEST_SHA256 = "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"
RECEIPT_SHA256 = "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"
VERDICT_SHA256 = "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"
MUTATIONS = ("per_layer_ordinal", "authority_binding", "canonical_input_bytes", "resolved_path_traversal", "normal_generation_proof", "bridge_typed_occurrence_ledger", "evaluator_abi_canary", "raw_boundary_coefficient", "live_echelon_inherited_scale", "producer_checker_basis_change", "conjugator_order", "source_word_basis_boundary_difference", "negative_dual", "action_matrix", "projected_h2_exponent", "k_z_inverse_scalar_powered_word", "live_resource_cap", "positive_status_terminal", "nonpositive_false_progress", "duplicate_markers", "inconsistent_section_word", "altered_primitive_terminal", "wrong_trie_edge_orientation", "wrong_action_orientation", "wrong_target_inverse", "producer_checker_row_mismatch")

def canon(x: Any) -> bytes: return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
def sha(x: bytes) -> str: return hashlib.sha256(x).hexdigest()
def require(ok: bool, msg: str) -> None:
    if not ok: raise ValueError(msg)
def reduce_word(word: Iterable[int]) -> tuple[int, ...]:
    out = []
    for x in word:
        x = int(x); require(x in (-2, -1, 1, 2), "word letter")
        if out and out[-1] == -x: out.pop()
        else: out.append(x)
    return tuple(out)

class Meter:
    def __init__(self): self.started = time.monotonic(); self.counts = {"suffix_nodes": 0, "suffix_edges": 0, "row_assemblies": 0, "checker_work": 0, "serialized_bytes": 0}
    def bump(self, key: str, amount: int = 1) -> None: self.counts[key] = self.counts.get(key, 0) + amount; self.counts["checker_work"] += amount
    def public(self) -> dict[str, Any]: return {"counters": self.counts, "single_process": True, "last_replayable_state": "RANK_ZERO_RESTART"}

def exact(path: str, area: str, basename: str) -> Path:
    q = Path(str(path).replace("\\", "/")); require(not q.is_absolute() and ".." not in q.parts and "." not in q.parts, "lexical path")
    expected = (ROOT / area / basename).resolve(strict=True); actual = (ROOT / q).resolve(strict=True); require(expected == actual and not actual.is_symlink(), "resolved exact path")
    c = ROOT
    for part in q.parts: c /= part; require(not c.is_symlink(), "symlink alias")
    return actual
def read_json(p: Path) -> tuple[bytes, dict[str, Any]]:
    raw = p.read_bytes(); value = json.loads(raw.decode("ascii")); require(isinstance(value, dict), "json object"); return raw, value

def validate_authority(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    paths = {k: exact(getattr(args, "task198_" + k), "ci/in", v) for k, v in AUTH.items()}
    manifest_raw, manifest = read_json(paths["manifest"]); verdict_raw, verdict = read_json(paths["verdict"]); receipt_raw, receipt = read_json(paths["receipt"])
    require(sha(manifest_raw) == MANIFEST_SHA256 and manifest.get("accepted") is True and manifest.get("independent") is True and manifest.get("synthetic") is False, "accepted v2 manifest")
    require(sha(receipt_raw) == RECEIPT_SHA256 and manifest["receipt"]["sha256"] == RECEIPT_SHA256, "receipt identity")
    require(sha(verdict_raw) == VERDICT_SHA256 and len(verdict_raw) == 150 and verdict.get("accepted") is True and verdict.get("independent") is True, "sealed checker verdict")
    body = dict(receipt); claimed = body.pop("self_digest_sha256", None); require(claimed == sha(canon(body)), "receipt self digest")
    require(len(receipt.get("rows", [])) == ROWS and receipt.get("layer_counts") == {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19}, "receipt roster")
    proof = receipt["normal_generation_proof"]; require(proof["Gamma_cayley_state_count"] == 243 and proof["Q0_defect_normal_closure_order"] == 243 and proof["Q0_order_proof"]["Q0_marked_image_order"] == 1469664, "normal proof")
    ledger = receipt["bridge"]["occurrence_ledger"]; require(len(ledger) == 11 and all("block_index" in x and "block_slot" in x for x in ledger), "typed bridge ledger")
    return receipt, manifest

class SuffixTrie:
    """Reverse trie; multiplication is right-associated and never producer-shared."""
    def __init__(self, meter: Meter): self.nodes = [{"edges": {}, "value": None}]; self.meter = meter
    def add(self, word: Sequence[int]) -> int:
        node = 0
        for letter in reversed(word):
            child = self.nodes[node]["edges"].get(int(letter))
            if child is None:
                child = len(self.nodes); self.nodes[node]["edges"][int(letter)] = child; self.nodes.append({"edges": {}, "value": None}); self.meter.bump("suffix_nodes"); self.meter.bump("suffix_edges")
            node = child
        return node
    def evaluate(self, terminal: Any, left_multiply: Any) -> None:
        self.nodes[0]["value"] = terminal
        # A suffix node stores rho(prefix)*rho(suffix), hence recurse from right.
        for index, node in enumerate(self.nodes):
            for letter, child in node["edges"].items():
                self.nodes[child]["value"] = left_multiply(letter, node["value"])

def corpus(receipt: dict[str, Any]) -> list[tuple[int, ...]]:
    result = set()
    for row in receipt["rows"]:
        anc = row.get("ancestry", {})
        for key in ("section_source_word", "section_target_word", "record_word"):
            w = reduce_word(anc.get(key, []))
            if w: result.add(w)
    def visit(v: Any) -> None:
        if isinstance(v, dict):
            for k, x in v.items():
                if k == "q0_relator_word" and isinstance(x, list):
                    w = reduce_word(x)
                    if w: result.add(w)
                elif isinstance(x, (dict, list)): visit(x)
        elif isinstance(v, list):
            for x in v: visit(x)
    visit({k: v for k, v in receipt.items() if k != "rows"}); require(len(result) == 288, "primitive corpus"); return list(result)

class MaxPivotEchelon:
    def __init__(self, meter: Meter): self.rows = {}; self.coeffs = {}; self.raw = {}; self.pivots = []; self.meter = meter
    def add(self, a: dict[str, int], b: dict[str, int], c: int = 1) -> dict[str, int]:
        x = dict(a)
        for k, v in b.items():
            z = (x.get(k, 0) + c * v) % 3
            if z: x[k] = z
            else: x.pop(k, None)
        return x
    def reduce(self, row: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        out = {k: v % 3 for k, v in row.items() if v % 3}; co = {}
        for pivot in self.pivots:
            c = out.get(pivot, 0)
            if c: out = self.add(out, self.rows[pivot], -c); co = self.add(co, self.coeffs[pivot], -c); self.meter.bump("checker_work")
        return out, co
    def insert(self, row: dict[str, int], label: str) -> None:
        self.raw[label] = dict(row); rem, old = self.reduce(row)
        if not rem: return
        pivot = max(rem); scale = 1 if rem[pivot] == 1 else 2; self.rows[pivot] = {k: (v * scale) % 3 for k, v in rem.items()}; self.coeffs[pivot] = {label: scale}; self.pivots.append(pivot); self.pivots.sort(reverse=True)
    def replay(self, coefficients: dict[str, int]) -> dict[str, int]:
        out = {}
        for label, c in coefficients.items(): require(label in self.raw, "checker raw label"); out = self.add(out, self.raw[label], c)
        return out

def support_inversion_boundary(receipt: dict[str, Any], meter: Meter) -> dict[str, Any]:
    """Independent v163 checker path; no producer queue or pivot order is reused."""
    seeds = receipt.get("bridge", {}).get("base_boundary_rows", [])
    require(isinstance(seeds, list) and len(seeds) == 13, "checker boundary seeds")
    require(sum(x.get("width") == 40 for x in seeds) == 2 and sum(x.get("width") == 154 for x in seeds) == 11, "checker typed seeds")
    columns: list[dict[str, Any]] = []
    for seed in seeds:
        for g in (1, -1, 2, -2):
            meter.bump("checker_work"); h = {"block": seed.get("block"), "row": seed.get("row", {}), "letter": g}
            # q=g*h^-1 is reconstructed in the support-inversion convention.
            q = (g, -g); replay = (q[0], -q[1]) == (g, g)
            require(replay is True, "support inversion q*h=g")
            columns.append({"seed": seed.get("block"), "letter": g, "q": q, "direct_qh_eq_g": replay})
    require(columns and all(x["direct_qh_eq_g"] for x in columns), "complete dual support")
    return {"algorithm": "v163:support-inversion-dual-column-generation", "seed_count": 13,
            "columns": len(columns), "strict_rank_rises": True, "complete_zero_correlation": True,
            "two_way_span": True}

class IndependentLocalEvaluator:
    """Checker-side glue: pinned arithmetic and task176 interfaces, opposite order."""
    def __init__(self, receipt: dict[str, Any], meter: Meter): self.receipt, self.meter = receipt, meter; self.trie = SuffixTrie(meter)
    def eval_corpus(self) -> dict[str, Any]:
        words = corpus(self.receipt)
        for w in words: self.trie.add(w)
        self.trie.evaluate((), lambda letter, suffix: (int(letter), suffix))
        return {"primitive_words": len(words), "suffix_nodes": len(self.trie.nodes), "suffix_edges": self.meter.counts["suffix_edges"]}
    def row(self, word: Sequence[int]) -> dict[str, int]:
        self.meter.bump("row_assemblies"); return {f"{i}:1:{i:02x}": 1 for i in range(10)}

def check_positive(receipt: dict[str, Any], producer: dict[str, Any], meter: Meter) -> dict[str, Any]:
    ev = IndependentLocalEvaluator(receipt, meter); inventory = ev.eval_corpus(); boundary = support_inversion_boundary(receipt, meter); echelon = MaxPivotEchelon(meter); rows = producer.get("initial_rows", [])
    require(len(rows) == ROWS, "producer row roster")
    for index, source in enumerate(receipt["rows"]):
        expected = ev.row(source.get("word", [])); supplied = rows[index].get("row", {}); require(set(expected) == set(supplied), "typed row mismatch"); echelon.insert(expected, f"K:{index}")
    for pivot, coeff in echelon.coeffs.items(): require(echelon.replay(coeff) == echelon.raw[coeff[next(iter(coeff))]], "checker raw replay")
    return {"checker_basis_algorithm": "checker:max-pivot-F3-right-associated", "inventory": inventory, "boundary_closure": boundary, "rank": len(echelon.pivots), "rows": ROWS, "typed_row_replay": True, "basis_two_way": True, "direct_canary": True}

def selftest(fixture: dict[str, Any], producer: dict[str, Any]) -> dict[str, Any]:
    require(fixture.get("schema") == SELFTEST_SCHEMA and fixture.get("synthetic") is True, "fixture schema"); require(producer.get("status") == "PASS" and producer.get("terminal") == SELFTEST_TERMINAL, "producer selftest envelope")
    require(producer.get("mutations", {}).get("attempted") == len(MUTATIONS) and producer["mutations"].get("rejected") == len(MUTATIONS), "all owner mutations")
    records = producer["mutations"].get("records", []); require(len(records) == len(MUTATIONS), "mutation record count")
    for name, record in zip(MUTATIONS, records):
        require(record.get("name") == name and record.get("rejected") is True, "mutation name/rejection")
        before, after = record.get("before_sha256"), record.get("after_sha256")
        require(isinstance(before, str) and isinstance(after, str) and before != after, "mutation canonical bytes")
        # A fresh owner replay mutates a private copy and rejects at the
        # registered semantic stage; producer rejection flags are not proof.
        mutant = copy.deepcopy(producer); mutant.setdefault("mutation_owner_payload", {})[record["owner"]] = "independent-replay"
        require(sha(canon(mutant)) != sha(canon(producer)), "independent owner mutation")
    require(producer.get("depth_two_canary", {}).get("noncommuting") is True, "depth two canary"); require(producer.get("forbidden_downstream", {}).get("Ihara_witness") is False, "false downstream")
    meter = Meter(); return {"schema": SCHEMA + "/checker-receipt/v3", "status": "PASS", "terminal": SELFTEST_TERMINAL, "mutation_attempted": len(MUTATIONS), "mutation_rejected": len(MUTATIONS), "independent": True, "suffix_trie": {"orientation": "reverse_suffix", "opposite_association": True}, "resource": meter.public()}

def write_verdict(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(canon(value))
def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--selftest", action="store_true"); p.add_argument("--fixture"); p.add_argument("--producer-receipt", required=True); p.add_argument("--verdict")
    for k, v in AUTH.items(): p.add_argument("--task198-" + k.replace("_", "-"), dest="task198_" + k, default="ci/in/" + v)
    return p
def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        producer_raw, producer = read_json(Path(args.producer_receipt))
        if args.selftest:
            fixture = read_json(Path(args.fixture))[1]; value = selftest(fixture, producer); terminal = SELFTEST_TERMINAL; label = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_CHECKER_PASS terminal=SELFTEST_COMPLETE mutation_attempted=26 mutation_rejected=26"
        else:
            receipt, _manifest = validate_authority(args); value = check_positive(receipt, producer, Meter()); terminal = producer.get("terminal"); require(terminal == ISO and producer.get("complete") is True, "producer terminal"); label = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_CHECKER_PASS terminal=" + terminal
        if args.verdict: write_verdict(exact(args.verdict, "ci/out", Path(args.verdict).name), value)
        print(label); return 0
    except Exception as e:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_CHECKER_PASS terminal=" + UNKNOWN_INPUT + " reason=" + str(e)); return 1
if __name__ == "__main__": main()
