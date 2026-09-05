#!/usr/bin/env python3
"""Task972: independent complete-oracle/E continuation checker.

Only the new continuation is replayed. Frozen accepted parents are admitted by
their observed metadata and exact bytes. The current oracle uses the repaired
v2 checker; selected words use our separately frozen E checker. Neither frozen
module's schema, accepted-parent constants, nor numerical helpers are patched.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import ExitStack
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import sys
import tempfile
import time
from typing import Any, Callable

import numpy as np

E_CHECKER_SHA = "a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4"
ORACLE_CHECKER_SHA = "a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d"
for _name, _pin in (("check_d972_r07_selected_cycle_materializer_v1.py", E_CHECKER_SHA),
                    ("check_d972_r07_section_cochain_oracle_v2.py", ORACLE_CHECKER_SHA)):
    _file = Path(__file__).resolve().with_name(_name)
    if _file.is_symlink() or hashlib.sha256(_file.read_bytes()).hexdigest() != _pin:
        raise ValueError("cegar_checker:retained_source_pin:" + _name)
import check_d972_r07_selected_cycle_materializer_v1 as E
import check_d972_r07_section_cochain_oracle_v2 as O

REFINE, FIXED, LEGACY, BASE, ARITH = O.REFINE, O.FIXED, O.LEGACY, O.BASE, O.ARITH
canonical, sha, seal, same, path, fixed = O.canonical, O.sha, O.seal, O.same, O.path, O.fixed
pack, unpack, dot = O.pack, O.unpack, O.dot
SCHEMA = "d972.r07.complete-oracle-cegar-continuation.v1"
VERTICES, EDGES, CHORDS, LOWER, TOP, PHYSICAL, ROW_BYTES = 54432, 108864, 54433, 96776, 36288, 48384, 12096
PHASES = ("section", "cochain", "tree", "raw", "source", "primal", "p1", "B", "physical")
OLD_OFFSETS, NEW_OFFSETS = O.OLD_OFFSETS, O.NEW_OFFSETS
SCOPE = {"vertices": VERTICES, "edges": EDGES, "chords": CHORDS, "legality_rows": 5,
    "normalized_auxiliaries": 2, "source_tags": 6, "characters": [0, 1, 2, 3], "p1_rows": 8059,
    "source_lower_trits": LOWER, "physical_trits": PHYSICAL, "source_universe_changed": False,
    "external_e_counted_as_new_step": False, "whole_normalized_word_replay": False, "eleven_slot_replay": False}
FORMULA = "v548-complete-oracle;v547-ordered-word;canonical-P1;four-B;dynamic-one-row"
# Observed successful E; all ten local entries independently hashed by Task972.
E_ARTIFACT: dict[str, Any] | None = {"run": 33981657987, "attempt": 1,
    "head": "444c71c9e554ae8feb9c8ee54df57d3df19ed66f", "id": 9973974150,
    "name": "d972-r07-selected-cycle-materializer-v1-candidate-33981657987-1", "bytes": 2816692,
    "sha256": "sha256:884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25"}
E_FILES: dict[str, tuple[int, str]] = {
    "output/HEAD": (1051, "75d2a3280a4926bfb73ea6c0a8424680c73e049c6f3ac9e0e53cb6e8a190835c"),
    "output/manifest.json": (4903, "956a6d91fae2c6ddda6a9dc8ee6ab52ee57de90c6cee367a6a58a33aad28ac59"),
    "output/start.json": (50926, "0bd617bb70e58d25c9344226275bae590dae1a28aeb1457f61477475a6f8092c"),
    "output/owner.json": (8425, "bd5e24d274e37977c5c1004be79530941501cdd390c9a27b0bfd2c35b396fa29"),
    "output/source.json": (1481, "c7a91fce06d95e4efb3b73ae74f0b8d0eb1f31b9baa2cb72eb899a62d04db5de"),
    "output/result.json": (168139, "199502f235662a934493db81e79a91950fce3dba829b8acbe39b9c37dc6bc7c8"),
    "checker-result.json": (30071, "9f0d30a4481ea94f0aa1a4cd5aa120281dc3ebee1a0e8e1b01db162efbde7a77"),
    "source-receipt.json": (3130, "b824897c24960e757e844f435048c369479c68b2f7c5c9859acaa47def8b07db"),
    "oracle-intake-receipt.json": (7094, "c10de40bb415bfa518f3a04e1165471d7b6557e168e4e4fa1581d7e1a103de08"),
    "run-receipt.json": (1654, "7b8ac9c712d2c7a528c5c9c0fc39d260ca0755029c3519031f8fe00b6a804d2b")}
E_SNAPSHOT: dict[str, Any] = {"terminal": "PIVOT_CANDIDATE", "kind": "Separator", "rank": 1386, "generation": 8091,
    "state_head": "5e760f6a7c04a5eaf800289ab5b05ae542dc33c09b502ab7f87958b5e836a6a8",
    "target_remainder_sha256": "e902cf3b2d9a5a58ac47459877e017fa4d6a44c5868751b8690543665ae269c1",
    "lambda_sha256": "a16f4c8289e78efa068cfe923f1ee9a0d7b71f8c71aede582ff0ff93cda0c8ad"}
PRODUCER_SHA: str | None = "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"
STARTED = time.monotonic()
DEADLINE: float | None = None
LAST_PHASE = "initialization"
CHECKED_CURSOR: dict[str, Any] = {"completed_steps": 0, "snapshot": None, "last_complete_phase": None,
                                  "phase_manifest_hashes": [], "physical_state_head": None}


class ResourceStop(Exception):
    pass


def require(condition: Any, label: str) -> None:
    if not condition:
        raise ValueError("cegar_checker:" + label)


def boundary(phase: str, **fields: Any) -> None:
    global LAST_PHASE
    LAST_PHASE = phase
    if DEADLINE is not None and time.monotonic() >= DEADLINE:
        raise ResourceStop(phase)
    print(json.dumps({"phase": phase, **fields}, sort_keys=True), file=sys.stderr, flush=True)


def document(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    return seal({"schema": SCHEMA + "." + kind, **body})


def unsigned(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key != "sha256"}


def sealed_bytes(raw: bytes, schema: str) -> dict[str, Any]:
    value = json.loads(raw)
    require(isinstance(value, dict) and raw == canonical(value) and value.get("schema") == schema and
            value.get("sha256") == sha(canonical(unsigned(value))), "exact_generic_seal:" + schema)
    return value


def plain_target(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) == {"parent_remainder_sha256", "remainder_sha256", "scalar"},
            "plain_target_exact_fields")
    require(type(value["scalar"]) is int and value["scalar"] in (0, 1, 2), "plain_target_scalar_including_zero")
    for name in ("parent_remainder_sha256", "remainder_sha256"):
        require(isinstance(value[name], str) and re.fullmatch(r"[0-9a-f]{64}", value[name]) is not None,
                "plain_target_hash")
    return value


def file_roster(payloads: dict[str, tuple[bytes, str, Any]]) -> list[dict[str, Any]]:
    return [{"file": name, "bytes": len(raw), "sha256": sha(raw), "dtype": dtype, "shape": shape}
            for name, (raw, dtype, shape) in sorted(payloads.items())]


def fixed_file_identity(stream: Any) -> tuple[int, int, int, int]:
    value = os.fstat(stream.fileno())
    return value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns


def directory(root: Path, relative: str) -> Path:
    """Directory counterpart of the retained file-only path helper."""
    require(root.is_dir() and not root.is_symlink() and isinstance(relative, str) and relative and
            "\\" not in relative and not Path(relative).is_absolute(), "relative_directory_root")
    parts = relative.split("/")
    require(all(part and part not in (".", "..") for part in parts), "relative_directory_components")
    candidate = root
    for part in parts:
        candidate = candidate / part
        require(candidate.is_dir() and not candidate.is_symlink(), "safe_existing_directory_component")
    require(candidate.resolve().is_relative_to(root.resolve()), "directory_containment")
    return candidate


class FixedBundle:
    """One authentication lifetime for saved lower rows and P1 references.

    Only small original-row metadata is retained from each large Task554 body.
    Cache contraction still reads all 8059 rows on every new lambda. Repeated
    arithmetic reads are counted separately from one-time lower authentication.
    """

    def __init__(self, args: argparse.Namespace, state: dict[str, Any], words: dict[str, Any],
                 tables: list[Any], geometry: O.Geometry):
        self.args, self.tables, self.geometry = args, tables, geometry
        self.stack = ExitStack()
        self.cache_passes = self.lower_row_reads = self.selected_lift_reads = 0
        try:
            self.basis = E.source_basis_metadata(state, words)
            self.index = E.authenticate_literal_instructions(args, state, self.basis)
            self.streams = []
            for root, descriptor in self.basis["descriptors"]:
                E.authenticated_blob(root, descriptor)
                self.streams.append(self.stack.enter_context(path(root, descriptor["file"]).open("rb")))
                boundary("fixed_lower_authenticated", file=descriptor["file"], bytes=descriptor["bytes"])
            require(len(self.streams) == 12, "fixed_twelve_lower_streams")
            self.cache = self.stack.enter_context(path(args.p1_root, "degree2.cache.bin").open("rb", buffering=1 << 20))
            self.identities = [fixed_file_identity(stream) for stream in self.streams + [self.cache]]
            self.records = self.basis["records"]
            self.old = [record for record in self.records if record["kind"] == "old"]
            self.new = [[record for record in self.records if record["kind"] == "new" and record["owner"] == owner]
                        for owner in range(4)]
            require(len(self.old) == 2014 and [len(rows) for rows in self.new] == list(BASE.NEW_RANKS),
                    "fixed_complete_source_basis")
            self.original = np.asarray([r["original_lead"] for r in self.records], dtype=np.uint32)
            self.embedded = np.asarray([r["embedded_lead"] for r in self.records], dtype=np.uint32)
            self._authenticate_cache()
            self.potential_tau, self.tau, self.selected, self.inverse = fixed_tree(geometry)
            self.selected_geometry: E.SelectedGeometry | None = None
            self.normalizers: dict[str, Any] | None = None
        except BaseException:
            self.stack.close()
            raise

    def __enter__(self) -> FixedBundle:
        return self

    def __exit__(self, *error: Any) -> None:
        self.stack.close()

    def unchanged(self) -> None:
        require([fixed_file_identity(stream) for stream in self.streams + [self.cache]] == self.identities,
                "same_opened_fixed_input_files")

    def _authenticate_cache(self) -> None:
        self.cache.seek(0)
        digest, length = hashlib.sha256(), 0
        for node, reference in enumerate(self.index["references"]):
            raw = self.cache.read(36288)
            require(len(raw) == 36288 and sha(raw) == reference["row_sha256"] and
                    not np.any(np.frombuffer(raw, dtype=np.uint8) > 80), "fixed_all_p1_rows")
            digest.update(raw); length += len(raw)
            if (node + 1) % 1024 == 0:
                boundary("fixed_p1_cache_authentication", rows=node + 1)
        require(self.cache.read(1) == b"" and length == BASE.P1_CACHE_BYTES and
                digest.hexdigest() == BASE.P1_CACHE_SHA256, "fixed_p1_cache_exact_eof")
        self.cache.seek(0)

    def packed_row(self, record: dict[str, Any]) -> tuple[bytes, bytes | None]:
        owner, local = record["owner"], record["local"]
        self.lower_row_reads += 1
        if record["kind"] == "old":
            return (LEGACY.blob_row(self.streams[2 * owner], local, 6056),
                    LEGACY.blob_row(self.streams[2 * owner + 1], local, 72576))
        return LEGACY.blob_row(self.streams[8 + owner], local, 18144), None

    def roots_and_values(self, functional: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        self.unchanged()
        require(functional.shape == (PHYSICAL,) and not np.any(functional > 2), "current_physical_lambda")
        roots = np.asarray([FIXED.pullback(table["entries"], functional) for table in self.tables], dtype=np.uint8)
        require(roots.shape == (4, TOP), "all_four_current_roots")
        projections = []
        for vector in roots:
            indices = np.flatnonzero(vector)
            projections.append([(indices // 4, indices % 4, vector[indices].astype(np.uint32))])
        values = np.zeros((4, 8059), dtype=np.uint8)
        self.cache.seek(0)
        digest, length = hashlib.sha256(), 0
        for first in range(0, 8059, 256):
            count = min(256, 8059 - first)
            raw = self.cache.read(count * 36288)
            require(len(raw) == count * 36288, "current_cache_complete_chunk")
            digest.update(raw); length += len(raw)
            rows = np.frombuffer(raw, dtype=np.uint8).reshape(count, 36288)
            require(not np.any(rows > 80), "current_cache_packed_trits")
            for owner in range(4):
                values[owner, first:first + count] = BASE.vectorized_projection_chunk(
                    rows, owner * 9072, projections[owner])[:, 0]
            boundary("new_current_p1_values", rows=first + count, characters=4)
        require(self.cache.read(1) == b"" and length == BASE.P1_CACHE_BYTES and
                digest.hexdigest() == BASE.P1_CACHE_SHA256, "current_cache_full_eof_hash")
        self.cache_passes += 1
        return roots, values

    def section(self, functional: np.ndarray) -> dict[str, Any]:
        roots, p1_values = self.roots_and_values(functional)
        chi = (p1_values.sum(axis=0, dtype=np.uint16) % 3).astype(np.uint8)
        k1 = np.zeros((4, 18144), dtype=np.uint8)
        new_order: list[int] = []
        for owner, records in enumerate(self.new):
            vector, order = O.interpolate_rows(18144,
                [(r["node"], r["original_lead"]) for r in records], chi,
                lambda node: unpack(self.packed_row(self.records[node])[0], 18144))
            k1[owner] = vector; new_order.extend(order)
            boundary("new_section_dual_d1", owner=owner)
        beta = chi[:2014].copy()
        old_records = []
        for record in self.old:
            _, companion = self.packed_row(record)
            require(companion is not None, "dual_old_four_d1_companion")
            node, lead, owner = record["node"], record["original_lead"], record["owner"]
            beta[node] = (int(beta[node]) - dot(k1.reshape(-1), unpack(companion, 72576))) % 3
            old_records.append((node, owner * 6048 + lead if lead < 6048 else 24192 + lead - 6048))
        boundary("new_section_dual_old_rhs", rows=2014)

        def old_row(node: int) -> np.ndarray:
            record = self.records[node]
            owner, lead = record["owner"], record["original_lead"]
            lower = unpack(self.packed_row(record)[0], 6056)
            require(lower[lead] == 1 and not np.any(lower[:lead]) and
                    (owner == 0 or not np.any(lower[6048:])), "dual_old_original_normalization")
            row = np.zeros(24200, dtype=np.uint8)
            row[owner * 6048:(owner + 1) * 6048], row[24192:] = lower[:6048], lower[6048:]
            return row

        k0, old_order = O.interpolate_rows(24200, old_records, beta, old_row)
        kappa = np.concatenate((k0[:24192], k1.reshape(-1), k0[24192:]))
        equations = np.empty(8059, dtype=np.uint8)
        for record in self.records:
            row, companion = self.packed_row(record)
            owner, node = record["owner"], record["node"]
            if record["kind"] == "old":
                covector = np.concatenate((k0[owner * 6048:(owner + 1) * 6048], k0[24192:]))
                value = dot(covector, unpack(row, 6056)) + dot(k1.reshape(-1), unpack(companion, 72576))
            else:
                value = dot(k1[owner], unpack(row, 18144))
            equations[node] = value % 3
            if (node + 1) % 1024 == 0:
                boundary("new_section_full_equations", rows=node + 1)
        residuals = ((equations.astype(np.int16) - chi) % 3).astype(np.uint8)
        require(kappa.shape == (LOWER,) and len(new_order) == 6045 and len(old_order) == 2014 and
                not np.any(residuals), "new_all_8059_section_equations")
        self.unchanged()
        return {"roots": roots, "p1_values": p1_values, "chi": chi, "beta": beta, "kappa": kappa,
                "equation_values": equations, "equation_residuals": residuals,
                "original": self.original.copy(), "embedded": self.embedded.copy(),
                "new_order": np.asarray(new_order, dtype=np.uint32), "old_order": np.asarray(old_order, dtype=np.uint32)}

    def primal(self, source: tuple[np.ndarray, ...]) -> dict[str, Any]:
        self.unchanged()
        return E.primal_rows(source, self.records, self.packed_row)

    def corrected(self, source: tuple[np.ndarray, ...], primal: dict[str, Any]) -> tuple[tuple[np.ndarray, ...], dict[str, Any]]:
        self.unchanged()
        require(primal["alpha"].shape == (8059,), "new_primal_all_coefficients")
        corrected = tuple(part.copy() for part in source)
        roots = []
        for node in np.flatnonzero(primal["alpha"]):
            node = int(node)
            reference = self.index["references"][node]
            lift, components = REFINE.source_lift(self.args, self.streams, self.cache, reference)
            for target, part in zip(corrected, lift):
                LEGACY.subtract(target, part, int(primal["alpha"][node]))
            roots.append({**reference, "lift_components": components})
            self.selected_lift_reads += 1
            if len(roots) % 128 == 0:
                boundary("new_selected_P1_reconstruction", selected=len(roots))
        lower = E.full_lower(corrected)
        require(lower.shape == (LOWER,) and np.array_equal(lower, primal["lower"]) and not np.any(lower),
                "new_full_P1_and_primal_lower_equality")
        self.unchanged()
        return corrected, E.document("p1-roots", {"p1_manifest_sha256": BASE.P1_MANIFEST_SHA256,
            "instruction_sha256": BASE.P1_INSTRUCTION_SHA256, "cache_sha256": BASE.P1_CACHE_SHA256,
            "canonical_index_sha256": sha(canonical(self.index)), "roots": roots,
            "all_references_authenticated": True})

    def raw_geometry(self) -> tuple[E.SelectedGeometry, dict[str, Any]]:
        if self.selected_geometry is None:
            g = self.geometry
            arrays = {"next-pos.u32": g.successor, "prev-pos.u32": g.inverse_successor, "phi.u32": g.tag_maps,
                "parent.u32": O.rooted_indices_u32(g.tree_parent, VERTICES),
                "parent-edge.u32": O.rooted_indices_u32(g.tree_edge, EDGES), "bfs-order.u32": g.tree_order,
                "carry.u8": g.carry, "chord-edges.u32": g.chords}
            self.selected_geometry = E.SelectedGeometry(g.context, arrays)
            self.normalizers = E.normalizer_words()
        require(self.normalizers is not None, "fixed_actual_normalizer_words")
        return self.selected_geometry, self.normalizers


def fixed_tree(geometry: O.Geometry) -> tuple[np.ndarray, np.ndarray, list[int], np.ndarray]:
    potential = np.zeros((VERTICES, 5), dtype=np.uint8)
    for position, vertex in enumerate(geometry.tree_order[1:], 1):
        vertex = int(vertex)
        parent, edge = int(geometry.tree_parent[vertex]), int(geometry.tree_edge[vertex])
        require(edge // 2 == parent and int(geometry.successor[parent, edge % 2]) == vertex,
                "fixed_tree_edge_identity")
        potential[vertex] = (potential[parent].astype(np.uint16) + geometry.carry[edge]) % 3
        if position % 12000 == 0:
            boundary("fixed_carry_tree", vertices=position + 1)
    edges = geometry.chords
    require(edges.shape == (CHORDS,) and len(np.unique(edges)) == CHORDS, "fixed_complete_chord_roster")
    tail, slot = edges // 2, edges % 2
    head = geometry.successor[tail, slot]
    tau = ((geometry.carry[edges].astype(np.int16) + potential[tail] - potential[head]) % 3).astype(np.uint8)
    selected, inverse = O.first_independent_columns(tau)
    return potential, tau, selected, inverse


def current_tree(bundle: FixedBundle, f: np.ndarray, b_aux: np.ndarray) -> dict[str, Any]:
    """Recompute every f-dependent quantity; fixed tau has its own owner."""
    require(f.shape == (EDGES,) and b_aux.shape == (2,) and not np.any(f > 2) and not np.any(b_aux > 2),
            "new_tree_full_inputs")
    geometry = bundle.geometry
    potential = np.zeros(VERTICES, dtype=np.uint8)
    for position, vertex in enumerate(geometry.tree_order[1:], 1):
        vertex = int(vertex)
        potential[vertex] = (int(potential[int(geometry.tree_parent[vertex])]) + int(f[int(geometry.tree_edge[vertex])])) % 3
        if position % 12000 == 0:
            boundary("new_f_tree_potential", vertices=position + 1)
    edges = geometry.chords
    tail, slot = edges // 2, edges % 2
    head = geometry.successor[tail, slot]
    values = ((f[edges].astype(np.int16) + potential[tail] - potential[head]) % 3).astype(np.uint8)
    selected, inverse, tau = bundle.selected, bundle.inverse, bundle.tau
    selected_edges = edges[selected]
    fit = (values[selected].astype(np.int64) @ inverse % 3).astype(np.uint8)
    residuals = ((values.astype(np.int64) - tau.astype(np.int64) @ fit.astype(np.int64)) % 3).astype(np.uint8)
    failed, aux = np.flatnonzero(residuals), np.flatnonzero(b_aux)
    if len(aux):
        coordinate = int(aux[0]); eta = [0, 0]; eta[coordinate] = 1
        witness = {"kind": "auxiliary", "coordinate": coordinate, "cycles": [], "eta": eta,
            "tau": [0] * 5, "scalar": int(b_aux[coordinate]), "materialization": "MATERIALIZATION_PENDING"}
    elif len(failed):
        index = int(failed[0])
        coefficients = inverse @ tau[index].astype(np.int64) % 3
        direct_tau = (tau[index].astype(np.int64) - coefficients @ tau[selected].astype(np.int64)) % 3
        scalar = int((int(values[index]) - coefficients @ values[selected].astype(np.int64)) % 3)
        require(not np.any(direct_tau) and scalar == int(residuals[index]) and scalar in (1, 2),
                "new_six_cycle_legality_scalar")
        cycles = [{"edge": int(edges[index]), "coefficient": 1}] + [
            {"edge": int(edge), "coefficient": int(-coefficient % 3)}
            for edge, coefficient in zip(selected_edges, coefficients)]
        witness = {"kind": "chord", "failed_chord": int(edges[index]), "basis_chords": selected_edges.tolist(),
            "basis_coefficients": coefficients.tolist(), "cycles": cycles, "eta": [0, 0],
            "tau": direct_tau.tolist(), "scalar": scalar, "materialization": "MATERIALIZATION_PENDING"}
    else:
        witness = {"kind": "none", "cycles": [], "eta": [0, 0], "tau": [0] * 5, "scalar": 0,
            "materialization": "NOT_NEEDED_FOR_ZERO_TEST"}
    terminal = "COMPLETE_ZERO_CANDIDATE" if witness["kind"] == "none" else "VIOLATION_CANDIDATE"
    metadata = O.document("tree", {"vertices": VERTICES, "tree_edges": VERTICES - 1, "chords": CHORDS,
        "independent_tau_columns": 5, "selection_order": "first-independent-chord;coordinate0-through4",
        "selected_chords": selected_edges.tolist(), "fit": fit.tolist(), "aux_values": b_aux.tolist(),
        "first_failed_chord": int(edges[failed[0]]) if len(failed) else None, "residual_nonzero": int(len(failed)),
        "full_chord_eof": True, "terminal": terminal, "materialization": witness["materialization"]})
    boundary("new_complete_tree_eof", chords=CHORDS, auxiliary_count=2)
    return {"potential_f": potential, "potential_tau": bundle.potential_tau, "chord_values": values,
        "tau": tau, "selected_edges": selected_edges, "fit": fit, "residuals": residuals,
        "metadata": metadata, "witness": O.document("witness", witness)}


E_ARRAYS = {
    "raw-chain.bin": ("packed3", [EDGES]), "raw-source-d0.bin": ("packed3", [4, 6048]),
    "raw-source-d1.bin": ("packed3", [4, 18144]), "raw-source-d2.bin": ("packed3", [4, TOP]),
    "raw-source-aux.bin": ("packed3", [8]), "p1-coefficients.u8": ("u8", [8059]),
    "source-lower-remainder.bin": ("packed3", [LOWER]), "source-top-corrected.bin": ("packed3", [4, TOP]),
    "physical-by-character.bin": ("packed3", [4, PHYSICAL]),
    **{name: ("packed3", [PHYSICAL]) for name in ("physical-raw.bin", "physical-remainder.bin",
        "physical-normalized.bin", "target-remainder.bin", "lambda.bin")}}
E_JSON = {name: E.SCHEMA + "." + name[:-5] for name in ("owner.json", "start.json", "source.json",
    "raw-word.json", "raw-source.json", "p1-exponent-residues.json", "p1-reductions.json", "p1-roots.json",
    "physical-literal.json", "result.json", "source-correction.json", "telemetry.json")}


def typed_input(raw: bytes, dtype: str, shape: list[int]) -> np.ndarray:
    require(isinstance(shape, list) and shape and all(type(n) is int and n > 0 for n in shape), "positive_array_shape")
    count = math.prod(shape)
    if dtype == "packed3":
        require(len(raw) == (count + 3) // 4, "packed_array_exact_bytes")
        value = unpack(raw, count)
    elif dtype == "u8":
        require(len(raw) == count, "u8_array_exact_bytes")
        value = np.frombuffer(raw, dtype=np.uint8).copy()
        require(not np.any(value > 2), "u8_array_trits")
    else:
        require(dtype == "u32le" and len(raw) == 4 * count, "u32_array_exact_bytes")
        value = np.frombuffer(raw, dtype="<u4").copy()
    return value.reshape(shape)


def canonical_plain(raw: bytes, schema: str) -> dict[str, Any]:
    value = json.loads(raw)
    require(isinstance(value, dict) and raw == canonical(value) and value.get("schema") == schema,
            "plain_canonical_object:" + schema)
    return value


def read_external_e(args: argparse.Namespace, oracle: dict[str, Any]) -> dict[str, Any]:
    require(E_ARTIFACT is not None and len(E_FILES) == 10 and E_SNAPSHOT, "observed_external_E_pins_required")
    entries = {}
    for name, pin in E_FILES.items():
        raw = fixed(args.e_root, name, pin)
        suffix = "head" if name == "output/HEAD" else Path(name).stem
        schema = E.SCHEMA + "." + ("oracle-intake" if name == "oracle-intake-receipt.json" else suffix)
        entries[name] = (canonical_plain(raw, schema) if name in
            ("source-receipt.json", "oracle-intake-receipt.json", "run-receipt.json") else sealed_bytes(raw, schema))
    manifest, head = entries["output/manifest.json"], entries["output/HEAD"]
    require(head["kind"] in ("Separator", "LinearMembershipCandidate"), "external_E_actual_kind")
    array_roster = dict(E_ARRAYS)
    if head["kind"] == "LinearMembershipCandidate":
        del array_roster["lambda.bin"]
    wanted = set(array_roster) | set(E_JSON) | {"instruction.json"}
    records = manifest["files"]
    require(isinstance(records, list) and [r["file"] for r in records] == sorted(wanted), "external_E_exact_payload_roster")
    output = directory(args.e_root, "output")
    require(output.is_dir() and not output.is_symlink() and
            {p.name for p in output.iterdir()} == wanted | {"manifest.json", "HEAD"}, "external_E_output_directory_roster")
    payloads, objects, hashes = {}, {}, {}
    for record in records:
        name = record["file"]
        require(set(record) == {"file", "bytes", "sha256", "dtype", "shape"} and
                type(record["bytes"]) is int and record["bytes"] >= 0, "external_E_file_descriptor")
        raw = fixed(output, name, (record["bytes"], record["sha256"]))
        hashes[name] = sha(raw)
        if name in array_roster:
            dtype, shape = array_roster[name]
            require((record["dtype"], record["shape"]) == (dtype, shape), "external_E_array_type:" + name)
            typed_input(raw, dtype, shape)
            if name in ("physical-normalized.bin", "target-remainder.bin", "lambda.bin"):
                payloads[name] = raw
        else:
            require(record["dtype"] == "json" and record["shape"] is None, "external_E_JSON_type")
            value = (canonical_plain(raw, E.SCHEMA + ".instruction") if name == "instruction.json" else sealed_bytes(raw, E_JSON[name]))
            if name in ("owner.json", "source.json", "start.json", "result.json", "instruction.json"):
                objects[name] = value
        boundary("external_E_payload_authenticated", file=name, bytes=len(raw))
    accepted = {"entries": entries, "objects": objects, "payloads": payloads, "hashes": hashes}
    external_e_semantics(accepted, oracle)
    return accepted


def external_e_semantics(accepted: dict[str, Any], oracle: dict[str, Any]) -> None:
    entries, objects, hashes = accepted["entries"], accepted["objects"], accepted["hashes"]
    start, owner, source, result, instruction = (objects[key + ".json"] for key in ("start", "owner", "source", "result", "instruction"))
    manifest, head, checked = entries["output/manifest.json"], entries["output/HEAD"], entries["checker-result.json"]
    run, intake, receipt = (entries[name] for name in ("run-receipt.json", "oracle-intake-receipt.json", "source-receipt.json"))
    for name in ("owner", "source", "start", "result"):
        require(hashes[name + ".json"] == E_FILES["output/" + name + ".json"][1] and
                objects[name + ".json"] == entries["output/" + name + ".json"], "external_E_entry_manifest_join")
    require(result["status"] == checked["status"] == run["status"] == intake["status"] == "PASS" and
            result["physical_appends"] == checked["physical_appends"] == head["completed_steps"] == 1,
            "external_E_one_completed_independently_checked_row")
    require(manifest["stage_eof"] == checked["completed_stages"] == ["raw", "source", "primal", "p1", "B", "physical"],
            "external_E_all_six_phase_EOF")
    for flag in ("all_arrays_and_json_compared", "ordinary27_actual_raw_source", "direct_raw_word_replay",
                 "source_lower_zero", "all_four_B_summed"):
        require(checked[flag] is True, "external_E_full_checker_gate:" + flag)
    require(checked["source_lower_trits"] == LOWER and checked["p1_rows"] == 8059 and
            checked["p1_literal_exponents_modulus"] == 54 and checked["checker_sha256"] == E_CHECKER_SHA and
            checked["retained_oracle_checker_sha256"] == E.ORACLE_CHECKER_SHA and
            checked["accepted_completion_checker_sha256"] == ORACLE_CHECKER_SHA, "external_E_exact_arithmetic_provenance")
    for value in (manifest, head, checked, result):
        for key, expected in (("owner_sha256", hashes["owner.json"]), ("start_sha256", hashes["start.json"]),
                              ("source_sha256", hashes["source.json"]), ("instruction_sha256", hashes["instruction.json"])):
            if key in value:
                require(value[key] == expected, "external_E_metadata_file_reference:" + key)
    require(head["manifest_sha256"] == checked["manifest_sha256"] == E_FILES["output/manifest.json"][1] and
            checked["head_sha256"] == E_FILES["output/HEAD"][1] and
            manifest["result_sha256"] == checked["result_sha256"] == hashes["result.json"], "external_E_manifest_HEAD_checker_chain")
    require(instruction["predecessor"] == start["state_head"] == result["parent_state_head"] == manifest["parent_state_head"] == head["parent_state_head"],
            "external_E_physical_parent_head")
    require(instruction["rolling_sha256"] == sha(bytes.fromhex(start["state_head"]) +
            canonical({k: v for k, v in instruction.items() if k != "rolling_sha256"})), "external_E_rolling_instruction")
    require(instruction["rolling_sha256"] == result["state_head"] == manifest["state_head"] == head["state_head"] == checked["state_head"],
            "external_E_current_head_join")
    for key in ("rank", "generation"):
        require(type(start[key]) is int and type(head[key]) is int and
                result[key + "_before"] == start[key] and result[key + "_after"] == start[key] + 1 ==
                instruction[key] == head[key] == checked[key], "external_E_one_delta:" + key)
    require(instruction["offer"] == start["generation"] and instruction["physical_offset"] == start["rank"] * ROW_BYTES,
            "external_E_offer_and_physical_namespace")
    expected_snapshot = {"terminal": result["terminal"], "kind": head["kind"], **{key: head[key]
        for key in ("rank", "generation", "state_head", "target_remainder_sha256", "lambda_sha256")}}
    same(expected_snapshot, E_SNAPSHOT, "external_E_actual_observed_snapshot")
    require(result["kind"] == checked["kind"] == head["kind"] and result["terminal"] == checked["terminal"] == run["terminal"],
            "external_E_terminal_agreement")
    target = plain_target(result["target"])
    require(target["parent_remainder_sha256"] == start["target_remainder_sha256"] and
            target["remainder_sha256"] == hashes["target-remainder.bin"] == head["target_remainder_sha256"] == instruction["target_remainder_sha256"] and
            target["scalar"] == instruction["target_scalar"] == checked["target_scalar"], "external_E_plain_target_joins")
    require(result["pivot"]["normalized_sha256"] == hashes["physical-normalized.bin"] == head["physical_sha256"] == instruction["physical_sha256"] and
            result["pivot"]["lead"] == instruction["lead"] and result["pivot"]["scale"] == instruction["sigma"], "external_E_normalized_row_identity")
    require(type(result["selected_scalar"]) is int and result["selected_scalar"] in (1, 2) and
            all(result[key] == result["selected_scalar"] for key in ("corrected_scalar", "physical_scalar", "remainder_scalar")) and
            checked["selected_scalar"] == instruction["selected_scalar"] == result["selected_scalar"], "external_E_selected_nonzero_scalar")
    require(result["target_derivation"]["mode"] == "derived" and result["target_derivation"]["original_rho2_directly_read"] is False and
            result["target_derivation"]["accepted_target_derivation_parents"] == start["accepted_target_derivation_parents"] and
            result["target_derivation"]["original_rho2_packed_sha256"] == start["lambda_rho2"]["original_rho2_packed_sha256"],
            "external_E_retained_rho2_target_identities")
    same(result["target_derivation"]["new_delta"], {"instruction_sha256": hashes["instruction.json"],
        "state_head": head["state_head"], "normalized_sha256": hashes["physical-normalized.bin"],
        "target_sha256": sha(canonical(target))}, "external_E_named_target_delta")
    same(start["accepted_oracle_layout"], E.oracle_layout(oracle), "external_E_same_accepted_oracle")
    same(checked["accepted_oracle_layout"], start["accepted_oracle_layout"], "external_E_checked_oracle_layout")
    require(instruction["origin"]["oracle_manifest_sha256"] == E.ORACLE_FILES["output/manifest.json"][1] and
            instruction["origin"]["witness_sha256"] == oracle["witness_sha256"], "external_E_current_witness_parent")
    same(run["launch"], {key: E_ARTIFACT[key] for key in ("run", "attempt", "head")}, "external_E_actual_launch")
    same(run["oracle_artifact"], E.ORACLE_ARTIFACT, "external_E_run_oracle_artifact")
    same(intake["artifact"], E.ORACLE_ARTIFACT, "external_E_intake_oracle_artifact")
    same(intake["entry_files"], [{"file": name, "bytes": pin[0], "sha256": pin[1]}
        for name, pin in sorted(E.ORACLE_FILES.items())], "external_E_intake_ten_oracle_entries")
    require(run["checker_result_sha256"] == E_FILES["checker-result.json"][1] and
            run["producer_result_sha256"] == E_FILES["output/result.json"][1] and
            run["source_receipt_sha256"] == E_FILES["source-receipt.json"][1] and
            run["oracle_intake_sha256"] == E_FILES["oracle-intake-receipt.json"][1] and
            run["source_unchanged"] is True and run["oracle_unchanged"] is True and
            run["producer_invocations"] == run["checker_invocations"] == 1 and run["old_success_suites"] == 0 and
            run["v2_checker_imported_or_executed"] is False, "external_E_run_preservation_and_separate_v2_provenance")
    require(source["producer_sha256"] == E.PRODUCER_SHA and len(receipt["files"]) == 16 and
            receipt["files"][0]["sha256"] == E.PRODUCER_SHA and receipt["files"][1]["sha256"] == E_CHECKER_SHA and
            receipt["data"] == source["data"] and source["python"] == checked["python"] == run["python"] and
            source["numpy"] == checked["numpy"] == run["numpy"], "external_E_source_runtime_receipt")
    for value in (manifest, checked, result, run, receipt, intake):
        require(value["cross_checked"] is False and value["verified"] is False, "external_E_assurance_boundary")
    require(result["grade2_member"] == result["grade2_nonmember"] == "NOT_DECIDED" and result["full_A0"] is False,
            "external_E_no_final_positive_or_negative_claim")


class PhysicalState:
    """Accepted rows plus appended rows in a distinct physical ID namespace."""

    def __init__(self, args: argparse.Namespace, accepted: dict[str, Any], start: dict[str, Any], *, base_count: int = 1354):
        self.args, self.accepted = args, accepted
        self.base_count = base_count
        self.pivots = [dict(p) for p in accepted["pivots"]]
        self.rows = list(accepted["saved_rows"])
        self.target, self.functional = accepted["start_target"].copy(), accepted["start_lambda"].copy()
        self.previous_target = self.target.copy()
        self.head, self.rank, self.generation, self.kind = start["state_head"], start["rank"], start["generation"], start["kind"]
        self.parents = copy.deepcopy(start["accepted_target_derivation_parents"])
        self.original_rho2 = start["lambda_rho2"]["original_rho2_packed_sha256"]
        self.completed_steps = 0
        self.direct_pairing = copy.deepcopy(start["direct_pairing"])
        self.base_stream = path(args.state_root, "state/physical.bin").open("rb", buffering=1 << 20)
        require(type(base_count) is int and base_count > 0 and self.rank == len(self.pivots) == base_count + len(self.rows), "physical_anchor_rank")

    def __enter__(self) -> PhysicalState:
        return self

    def __exit__(self, *error: Any) -> None:
        self.base_stream.close()

    def row(self, node: int) -> bytes:
        require(type(node) is int and 0 <= node < self.rank, "physical_row_id")
        return LEGACY.blob_row(self.base_stream, node, PHYSICAL) if node < self.base_count else self.rows[node - self.base_count]

    def measure(self) -> dict[str, Any] | None:
        require(self.rank == len(self.pivots) == self.base_count + len(self.rows) and
                all(self.target[p["lead"]] == 0 for p in self.pivots), "current_target_all_pivot_leads_zero")
        if self.kind == "LinearMembershipCandidate":
            require(not np.any(self.target) and self.functional is None, "linear_target_without_lambda")
            self.direct_pairing = None
            return None
        require(self.kind == "Separator" and self.functional is not None and np.any(self.target), "current_separator_type")
        measured = []
        for node in range(self.rank):
            measured.append(dot(self.functional, unpack(self.row(node), PHYSICAL)))
            if (node + 1) % 256 == 0:
                boundary("current_physical_all_rows", rows=node + 1)
        old_dot, current_dot = dot(self.functional, self.previous_target), dot(self.functional, self.target)
        require(not any(measured) and old_dot == current_dot == 1, "current_all_rows_both_targets_direct_dot")
        self.direct_pairing = {"rows": self.rank, "row_pairings_sha256": sha(bytes(measured)), "lambda_pivots": 0,
            "lambda_parent_remainder": old_dot, "lambda_new_remainder": current_dot}
        return self.direct_pairing

    def attach(self, payloads: dict[str, bytes], instruction: dict[str, Any], result: dict[str, Any],
               manifest_sha: str, role: str, *, new_step: bool) -> None:
        require(self.kind == "Separator" and instruction["predecessor"] == result["parent_state_head"] == self.head and
                instruction["offer"] == self.generation and instruction["rank"] == result["rank_after"] == self.rank + 1 and
                instruction["generation"] == result["generation_after"] == self.generation + 1 and
                instruction["physical_offset"] == self.rank * ROW_BYTES, "physical_delta_actual_parent")
        require(instruction["rolling_sha256"] == result["state_head"] == sha(bytes.fromhex(self.head) +
            canonical({k: v for k, v in instruction.items() if k != "rolling_sha256"})), "physical_delta_rolling_join")
        normalized = unpack(payloads["physical-normalized.bin"], PHYSICAL)
        lead = instruction["lead"]
        require(type(lead) is int and 0 <= lead < PHYSICAL and normalized[lead] == 1 and not np.any(normalized[:lead]) and
                all(normalized[p["lead"]] == 0 for p in self.pivots) and
                sha(payloads["physical-normalized.bin"]) == instruction["physical_sha256"], "attached_normalized_row_triangularity")
        target_record = plain_target(result["target"])
        require(target_record["parent_remainder_sha256"] == sha(pack(self.target)) and
                target_record["remainder_sha256"] == instruction["target_remainder_sha256"] == sha(payloads["target-remainder.bin"]) and
                target_record["scalar"] == instruction["target_scalar"], "attached_plain_target_receipt")
        next_target = unpack(payloads["target-remainder.bin"], PHYSICAL)
        next_functional = unpack(payloads["lambda.bin"], PHYSICAL) if "lambda.bin" in payloads else None
        kind = "Separator" if np.any(next_target) else "LinearMembershipCandidate"
        require(kind == result["kind"] and ((next_functional is not None) == (kind == "Separator")), "attached_target_lambda_kind")
        self.parents.append({"role": role, "manifest_sha256": manifest_sha, "result_sha256": sha(canonical(result)),
            "instruction_sha256": sha(canonical(instruction)), "state_head": instruction["rolling_sha256"],
            "target_sha256": sha(canonical(target_record))})
        self.rows.append(payloads["physical-normalized.bin"])
        self.pivots.append({"offer": self.generation, "lead": lead, "physical_offset": self.rank * ROW_BYTES,
            "coefficient_offset": None, "rolling_sha256": instruction["rolling_sha256"]})
        self.previous_target, self.target, self.functional = self.target, next_target, next_functional
        self.head, self.rank, self.generation, self.kind = instruction["rolling_sha256"], self.rank + 1, self.generation + 1, kind
        if new_step:
            self.completed_steps += 1
        self.measure()
        if self.kind == "Separator":
            same(self.direct_pairing, result["separator"]["direct_pairing"], "attached_saved_direct_pairing")

    def derived(self) -> dict[str, Any] | None:
        if self.kind != "Separator":
            return None
        return {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
            "original_rho2_packed_sha256": self.original_rho2, "accepted_target_derivation_parents": self.parents,
            "identity_convention": {
                "base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
                "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)",
                "all_one_row_steps": "parent_remainder - child_remainder = target.scalar * accepted_normalized_row"},
            "new_target_steps_executed": self.completed_steps}

    def summary(self) -> dict[str, Any]:
        return {"kind": self.kind, "rank": self.rank, "generation": self.generation, "state_head": self.head,
            "lambda_sha256": None if self.functional is None else sha(pack(self.functional)),
            "target_remainder_sha256": sha(pack(self.target)), "previous_target_remainder_sha256": sha(pack(self.previous_target)),
            "accepted_target_derivation_parents": self.parents, "lambda_rho2": self.derived(), "direct_pairing": self.direct_pairing}


def external_e_layout(accepted: dict[str, Any]) -> dict[str, Any]:
    entries, hashes = accepted["entries"], accepted["hashes"]
    head, result = entries["output/HEAD"], entries["output/result.json"]
    return document("external-e-layout", {"artifact": E_ARTIFACT,
        "entry_files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(E_FILES.items())],
        **{key + "_sha256": E_FILES["output/" + key + ".json"][1] for key in ("manifest", "start", "owner", "source", "result")},
        "head_sha256": E_FILES["output/HEAD"][1], "instruction_sha256": hashes["instruction.json"],
        "checker_result_sha256": E_FILES["checker-result.json"][1], "terminal": result["terminal"],
        **{key: head[key] for key in ("kind", "rank", "generation", "state_head", "target_remainder_sha256", "lambda_sha256")},
        "old_arithmetic_replayed": False})


def root_start_owner(state: PhysicalState, accepted_e: dict[str, Any], oracle: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    require(state.completed_steps == 0 and state.rank == accepted_e["entries"]["output/HEAD"]["rank"], "external_E_attached_exactly_once")
    layout = external_e_layout(accepted_e)
    old_start = accepted_e["objects"]["start.json"]
    old_owner = oracle["entries"]["output/owner.json"]
    owner = document("owner", {"formula_id": FORMULA, "scope": SCOPE,
        "external_e_owner_sha256": E_FILES["output/owner.json"][1], "external_e_layout_sha256": sha(canonical(layout)),
        "oracle_owner_sha256": E.ORACLE_FILES["output/owner.json"][1], **{key: old_owner[key] for key in
            ("p1_parent", "task554_parent", "task712_parent", "task712_manifest_sha256", "word_dictionary_sha256", "relator_dictionary_sha256")}})
    start = document("start", {**state.summary(), "completed_steps": 0, "accepted_external_e_layout": layout,
        "accepted_oracle_layout": E.oracle_layout(oracle), "accepted_refinement_layout": old_start["accepted_refinement_layout"],
        "external_e_attached": 1, "external_e_numerically_replayed": False})
    return start, owner


def producer_source(root: Path) -> dict[str, Any]:
    require(PRODUCER_SHA is not None, "final_new_producer_source_pin_required")
    directory = Path(__file__).resolve().parent
    producer = directory / "d972_r07_complete_oracle_cegar_continuation_v1.py"
    require(producer.is_file() and not producer.is_symlink() and sha(producer.read_bytes()) == PRODUCER_SHA,
            "new_producer_exact_source_pin")
    retained = E.producer_source()
    actual = sealed_bytes(path(root, "source.json").read_bytes(), SCHEMA + ".source")
    require(isinstance(actual["python"], str) and actual["python"] and
            isinstance(actual["numpy"], str) and actual["numpy"], "recorded_producer_runtime_strings")
    provenance = {"oracle_source_sha256": E.ORACLE_FILES["output/source.json"][1],
        "oracle_original_source_receipt_sha256": E.ORACLE_FILES["source-receipt.json"][1],
        "oracle_completion_checker_result_sha256": E.ORACLE_FILES["checker-result.json"][1],
        "oracle_completion_receipt_sha256": E.ORACLE_FILES["completion-run-receipt.json"][1],
        "external_e_source_sha256": E_FILES["output/source.json"][1],
        "external_e_source_receipt_sha256": E_FILES["source-receipt.json"][1],
        "external_e_checker_result_sha256": E_FILES["checker-result.json"][1], "external_e_checker_sha256": E_CHECKER_SHA}
    wanted = document("source", {"producer_sha256": PRODUCER_SHA,
        "modules": {**retained["modules"], "d972_r07_selected_cycle_materializer_v1.py": E.PRODUCER_SHA},
        "data": retained["data"], "python": actual["python"], "numpy": actual["numpy"], "parent_provenance": provenance})
    same(actual, wanted, "new_source_closure_and_separate_parent_provenance")
    return wanted


def exponent_record(bundle: FixedBundle) -> dict[str, Any]:
    return E.document("p1-exponent-residues", {"rows": 8059, "order": "canonical-row-id", "modulus": 54,
        "pairs": bundle.basis["pairs"], "p1_manifest_sha256": BASE.P1_MANIFEST_SHA256,
        "instruction_sha256": BASE.P1_INSTRUCTION_SHA256, "method": "ordered-signed-DAG-exponent-mod54", "eof": True})


def fixed_payloads(bundle: FixedBundle, oracle: dict[str, Any]) -> dict[str, tuple[bytes, str, Any]]:
    payloads = O.geometry_payloads(bundle.geometry)
    for name, (raw, _, _) in payloads.items():
        require(path(bundle.args.oracle_root, "output/geometry/" + name).read_bytes() == raw,
                "independent_fixed_geometry_same_accepted_bytes:" + name)
    carry = {"potential-tau.u8": O.typed_array(bundle.potential_tau, "u8", (VERTICES, 5)),
        "chord-tau.u8": O.typed_array(bundle.tau, "u8", (CHORDS, 5)),
        "selected-chords.u32": O.typed_array(bundle.geometry.chords[bundle.selected], "u32le", (5,))}
    for name, (raw, _, _) in carry.items():
        require(path(bundle.args.oracle_root, "output/tree/" + name).read_bytes() == raw,
                "independent_fixed_carry_same_accepted_bytes:" + name)
    segments = []
    descriptors = bundle.basis["descriptors"]
    for owner in range(4):
        rows = [r for r in bundle.old if r["owner"] == owner]
        segments.append({"kind": "old", "owner": owner, "start": OLD_OFFSETS[owner], "rows": len(rows),
            "body_sha256": BASE.TASK554_BODY_DIGESTS[0], "leads": [r["original_lead"] for r in rows],
            "lower_descriptor": descriptors[2 * owner][1], "grade_descriptor": descriptors[2 * owner + 1][1]})
    for owner, rows in enumerate(bundle.new):
        segments.append({"kind": "new", "owner": owner, "start": NEW_OFFSETS[owner], "rows": len(rows),
            "body_sha256": BASE.TASK554_BODY_DIGESTS[owner + 1], "leads": [r["original_lead"] for r in rows],
            "basis_descriptor": descriptors[8 + owner][1]})
    basis = document("basis", {"segments": segments, "rows": 8059, "lower_blobs": 12,
        "p1_manifest_sha256": BASE.P1_MANIFEST_SHA256, "canonical_index_sha256": sha(canonical(bundle.index)),
        "lower_blob_pin_sha256": BASE.LOWER_BLOB_PIN_SHA256, "eof": True})
    return {**payloads, **carry, "canonical-index.json": O.json_payload(bundle.index),
        "basis.json": O.json_payload(basis), "p1-exponent-residues.json": O.json_payload(exponent_record(bundle))}


def compare_directory(root: Path, payloads: dict[str, tuple[bytes, str, Any]], manifest: dict[str, Any]) -> str:
    require(root.is_dir() and not root.is_symlink(), "complete_directory_exists")
    expected = {**{name: value[0] for name, value in payloads.items()}, "manifest.json": canonical(manifest)}
    require({p.name for p in root.iterdir()} == set(expected), "complete_directory_exact_roster")
    mismatches = []
    for name, raw in expected.items():
        with path(root, name).open("rb") as stream:
            if stream.read(len(raw) + 1) != raw:
                mismatches.append(name)
    require(not mismatches, "complete_directory_all_bytes_EOF:" + ",".join(mismatches))
    return sha(canonical(manifest))


def check_fixed(root: Path, bundle: FixedBundle, oracle: dict[str, Any], owner_sha: str, source_sha: str) -> tuple[str, dict[str, Any]]:
    payloads = fixed_payloads(bundle, oracle)
    manifest = document("fixed-manifest", {"owner_sha256": owner_sha, "source_sha256": source_sha, "scope": SCOPE,
        "accepted_geometry_stage_sha256": oracle["stage_hashes"]["geometry"], "fixed_values_independent_of_lambda": True,
        "files": file_roster(payloads)})
    digest = compare_directory(directory(root, "fixed"), payloads, manifest)
    return digest, manifest


def snapshot_record(state: PhysicalState, owner_sha: str, source_sha: str, start_sha: str, fixed_sha: str) -> dict[str, Any]:
    return document("snapshot", {"owner_sha256": owner_sha, "source_sha256": source_sha, "start_sha256": start_sha,
        "fixed_manifest_sha256": fixed_sha, "step": state.completed_steps, **state.summary()})


def phase_directory(snapshot_root: Path, phase: str) -> Path:
    require(phase in PHASES, "registered_phase_name")
    return directory(snapshot_root, phase if phase in PHASES[:3] else "e/" + phase)


def phase_metadata(phase: str, snapshot: dict[str, Any], previous: str | None,
                   payloads: dict[str, tuple[bytes, str, Any]]) -> dict[str, Any]:
    return document("phase-manifest", {"phase": phase, "owner_sha256": snapshot["owner_sha256"],
        "source_sha256": snapshot["source_sha256"], "fixed_manifest_sha256": snapshot["fixed_manifest_sha256"],
        "snapshot_sha256": sha(canonical(snapshot)), "previous_phase_manifest_sha256": previous,
        "files": file_roster(payloads)})


def compare_phase(snapshot_root: Path, phase: str, snapshot: dict[str, Any], previous: str | None,
                  payloads: dict[str, tuple[bytes, str, Any]]) -> tuple[str, dict[str, Any]]:
    root = phase_directory(snapshot_root, phase)
    item = path(root, "telemetry.json")
    require(item.stat().st_size < (1 << 20), "phase_telemetry_size")
    telemetry = sealed_bytes(item.read_bytes(), SCHEMA + ".phase-telemetry")
    elapsed, begun, ended = (telemetry[key] for key in ("elapsed_seconds", "begun_elapsed_seconds", "ended_elapsed_seconds"))
    require(all(type(value) in (int, float) and math.isfinite(value) and value >= 0 for value in (elapsed, begun, ended)) and
            ended >= begun and abs(ended - begun - elapsed) < 3e-6, "actual_phase_start_EOF_timing")
    wanted = document("phase-telemetry", {"phase": phase, "elapsed_seconds": elapsed, "begun_elapsed_seconds": begun,
        "ended_elapsed_seconds": ended, "payload_bytes": sum(len(raw) for raw, _, _ in payloads.values()), "eof": True})
    same(telemetry, wanted, "phase_telemetry_payload_count_and_EOF")
    complete = {**payloads, "telemetry.json": O.json_payload(wanted)}
    manifest = phase_metadata(phase, snapshot, previous, complete)
    digest = compare_directory(root, complete, manifest)
    CHECKED_CURSOR.update({"snapshot": sha(canonical(snapshot)), "last_complete_phase": phase,
        "phase_manifest_hashes": [*CHECKED_CURSOR["phase_manifest_hashes"], {"phase": phase, "sha256": digest}]})
    boundary("new_phase_all_payloads_compared", phase_name=phase, snapshot=snapshot["step"], payload_bytes=wanted["payload_bytes"])
    return digest, wanted


def current_oracle_records(snapshot: dict[str, Any], stage_hashes: dict[str, str], tree: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    require(set(stage_hashes) == set(PHASES[:3]), "current_oracle_all_three_phase_EOF")
    witness_sha = sha(canonical(tree["witness"]))
    shared = {key: snapshot[key] for key in ("owner_sha256", "source_sha256", "fixed_manifest_sha256")}
    result = document("oracle-result", {"status": "PASS", "terminal": tree["metadata"]["terminal"], **shared,
        "snapshot_sha256": sha(canonical(snapshot)), **{key: snapshot[key] for key in ("step", "rank", "generation", "state_head",
            "lambda_sha256", "target_remainder_sha256", "lambda_rho2", "direct_pairing")},
        "stage_manifests": stage_hashes, "section_equalities": 8059, "chords_checked": CHORDS, "auxiliary_tests": 2,
        "witness_sha256": witness_sha, "materialization": tree["witness"]["materialization"], "new_physical_appends": 0,
        "old_scans_numerically_replayed": 0, "old_inserts_numerically_replayed": 0,
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "candidate": True, "cross_checked": False, "verified": False})
    manifest = document("oracle-manifest", {**shared, "snapshot_sha256": sha(canonical(snapshot)),
        "stage_manifests": stage_hashes, "result_sha256": sha(canonical(result)), "witness_sha256": witness_sha,
        "terminal": result["terminal"], "stage_eof": list(PHASES[:3]), "candidate": True, "cross_checked": False, "verified": False})
    return result, manifest


def dynamic_delta_records(snapshot: dict[str, Any], owner: dict[str, Any], source: dict[str, Any], oracle_sha: str,
                          oracle: dict[str, Any], raw: dict[str, Any], correction: dict[str, Any], roots: dict[str, Any],
                          reductions: dict[str, Any], physical: dict[str, Any], corrected_scalar: int) -> dict[str, Any]:
    """Frozen E's public inner ABI, with explicit current snapshot references."""
    scalar = raw["selected_scalar"]
    literal = E.document("physical-literal", {"operation": "scaled-ordered-product",
        "source_correction_sha256": sha(canonical(correction)), "accepted_physical_head": snapshot["state_head"],
        "physical_factors": [{**r, "literal_exponent": -E.signed(r["scalar"])} for r in physical["reductions"]],
        "sigma": physical["sigma"], "literal_outer_exponent": E.signed(physical["sigma"]), "source_lower_zero": "NOT_ASSERTED",
        "physical_lower_zero": True, "physical_normalized_sha256": sha(pack(physical["normalized"])),
        "whole_word_direct_replay": False, "eleven_slot_replay": False, "target_word_direct_replay": False})
    instruction = {"schema": E.SCHEMA + ".instruction", "predecessor": snapshot["state_head"], "offer": snapshot["generation"],
        "rank": snapshot["rank"] + 1, "generation": snapshot["generation"] + 1, "physical_offset": snapshot["rank"] * ROW_BYTES,
        "origin": {"kind": "v548-cycle" if oracle["witness"]["kind"] == "chord" else "v548-aux",
            "oracle_manifest_sha256": oracle_sha, "witness_sha256": oracle["witness_sha256"],
            "raw_word_sha256": sha(canonical(raw["raw_word"]))}, "source_correction_sha256": sha(canonical(correction)),
        "physical_literal_sha256": sha(canonical(literal)), "p1_roots_sha256": sha(canonical(roots)),
        "p1_reductions_sha256": sha(canonical(reductions)), "physical_reductions": physical["reductions"],
        "lead": physical["lead"], "sigma": physical["sigma"], "physical_sha256": sha(pack(physical["normalized"])),
        "selected_scalar": scalar, "target_scalar": physical["target_scalar"], "target_remainder_sha256": sha(pack(physical["target"]))}
    instruction["rolling_sha256"] = sha(bytes.fromhex(snapshot["state_head"]) + canonical(instruction))
    target = {"parent_remainder_sha256": snapshot["target_remainder_sha256"],
        "remainder_sha256": sha(pack(physical["target"])), "scalar": physical["target_scalar"]}
    derivation = {"mode": "derived", "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": snapshot["lambda_rho2"]["original_rho2_packed_sha256"],
        "accepted_target_derivation_parents": snapshot["accepted_target_derivation_parents"],
        "new_delta": {"instruction_sha256": sha(canonical(instruction)), "state_head": instruction["rolling_sha256"],
            "normalized_sha256": sha(pack(physical["normalized"])), "target_sha256": sha(canonical(target))},
        "identity": "parent_remainder - new_remainder = target.scalar * new_normalized_row"}
    separator = physical["separator"]
    if separator is not None:
        separator = {**separator, "lambda_rho2": {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
            "target_derivation": derivation, "new_target_steps_executed": 1}}
    result = E.document("result", {"status": "PASS", "terminal": physical["terminal"], "kind": physical["kind"],
        "owner_sha256": sha(canonical(owner)), "start_sha256": sha(canonical(snapshot)), "source_sha256": sha(canonical(source)),
        "parent_state_head": snapshot["state_head"], "state_head": instruction["rolling_sha256"],
        "rank_before": snapshot["rank"], "rank_after": snapshot["rank"] + 1,
        "generation_before": snapshot["generation"], "generation_after": snapshot["generation"] + 1,
        "selected_scalar": scalar, "homogeneous_scalar": raw["homogeneous_scalar"], "section_scalar": raw["section_scalar"],
        "corrected_scalar": corrected_scalar, "physical_scalar": scalar, "remainder_scalar": scalar,
        "pivot": {"lead": physical["lead"], "scale": physical["sigma"], "normalized_sha256": sha(pack(physical["normalized"])),
            "reductions": physical["reductions"]}, "target": target, "separator": separator, "target_derivation": derivation,
        "raw_word_sha256": sha(canonical(raw["raw_word"])), "source_correction_sha256": sha(canonical(correction)),
        "physical_literal_sha256": sha(canonical(literal)), "p1_roots_sha256": sha(canonical(roots)),
        "instruction_sha256": sha(canonical(instruction)), "physical_appends": 1,
        "positive_readout": "TASK958_PENDING" if separator is None else "NOT_APPLICABLE",
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "candidate": True, "cross_checked": False, "verified": False})
    return {"physical-literal.json": literal, "instruction.json": instruction, "result.json": result}


def oracle_snapshot_join(result: dict[str, Any], snapshot: dict[str, Any]) -> None:
    require(result["status"] == "PASS" and result["snapshot_sha256"] == sha(canonical(snapshot)) and
            result["section_equalities"] == 8059 and result["chords_checked"] == CHORDS and result["auxiliary_tests"] == 2,
            "complete_current_oracle_EOF")
    for name in ("owner_sha256", "source_sha256", "fixed_manifest_sha256", "step", "rank", "generation",
                 "state_head", "lambda_sha256", "target_remainder_sha256"):
        require(result[name] == snapshot[name], "oracle_current_snapshot_field:" + name)
    require(snapshot["kind"] == "Separator" and snapshot["lambda_sha256"] is not None, "oracle_requires_current_separator")


def replay_snapshot(snapshot_root: Path, snapshot: dict[str, Any], phase_count: int, need_oracle: bool,
                    bundle: FixedBundle, state: PhysicalState, owner: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    """Independently recompute precisely the committed phase prefix's objects."""
    require(type(phase_count) is int and 0 <= phase_count <= len(PHASES) and
            (not need_oracle or phase_count >= 3) and (phase_count <= 3 or need_oracle), "committed_phase_prefix_type")
    require(path(snapshot_root, "start.json").read_bytes() == canonical(snapshot), "current_snapshot_exact_bytes")
    CHECKED_CURSOR.update({"snapshot": sha(canonical(snapshot)), "last_complete_phase": None, "phase_manifest_hashes": []})
    result: dict[str, Any] = {"phase_hashes": {}, "telemetry": [], "oracle_result": None, "oracle_manifest": None,
                              "physical": None, "records": None, "physical_payloads": None}
    previous = None

    def compare(phase: str, payloads: dict[str, tuple[bytes, str, Any]]) -> None:
        nonlocal previous
        digest, telemetry = compare_phase(snapshot_root, phase, snapshot, previous, payloads)
        result["phase_hashes"][phase] = digest
        result["telemetry"].append(telemetry)
        previous = digest

    if phase_count == 0:
        return result
    require(state.functional is not None, "new_snapshot_current_lambda")
    section = bundle.section(state.functional)
    compare("section", O.section_payloads(section))
    if phase_count == 1:
        return result
    score, anchor = O.source_scores(bundle.geometry, section["roots"], section["kappa"])
    f, b_aux, _ = O.raw_edge_cochain(bundle.geometry, score, section["kappa"])
    compare("cochain", O.cochain_payloads(score, f, b_aux))
    result["ordinary27_anchor"] = anchor
    if phase_count == 2:
        return result
    tree = current_tree(bundle, f, b_aux)
    compare("tree", O.tree_payloads(tree))
    if not need_oracle:
        return result
    oracle_result, oracle_manifest = current_oracle_records(snapshot,
        {key: result["phase_hashes"][key] for key in PHASES[:3]}, tree)
    for name, value in (("oracle-result.json", oracle_result), ("oracle-manifest.json", oracle_manifest)):
        require(path(snapshot_root, name).read_bytes() == canonical(value), "new_current_oracle_top_bytes:" + name)
    oracle_snapshot_join(oracle_result, snapshot)
    result["oracle_result"], result["oracle_manifest"] = oracle_result, oracle_manifest
    if phase_count == 3:
        return result
    require(oracle_result["terminal"] == "VIOLATION_CANDIDATE", "E_requires_complete_current_violation")
    oracle = {"witness": tree["witness"], "witness_sha256": sha(canonical(tree["witness"])),
        "stage_hashes": {"geometry": snapshot["fixed_manifest_sha256"]},
        "arrays": {"section": {"q.bin": section["roots"], "kappa.bin": section["kappa"]},
                   "cochain": {"f.u8": f, "b-aux.u8": b_aux}}}
    geometry, normalizers = bundle.raw_geometry()
    # Frozen own raw_materialization connects actual RawSLP and ordinary27. Its
    # raw/source calculations share a call; only compared phases advance cursor.
    raw = E.raw_materialization(geometry, normalizers, oracle)
    compare("raw", {"raw-word.json": O.json_payload(raw["raw_word"]),
        "raw-chain.bin": O.typed_array(raw["chain"], "packed3", (EDGES,))})
    if phase_count == 4:
        return result
    source_payloads = {"raw-source-" + role + ".bin": O.typed_array(part, "packed3", part.shape)
        for role, part in zip(("d0", "d1", "d2", "aux"), raw["source"])}
    source_payloads["raw-source.json"] = O.json_payload(raw["raw_source"])
    compare("source", source_payloads)
    if phase_count == 5:
        return result
    primal = bundle.primal(raw["source"])
    reductions = E.document("p1-reductions", {"order": "old-global-ascending-embedded-original-lead;new-owner-major-ascending-original-lead",
        "rows": 8059, "events": primal["events"], "coefficients_sha256": sha(primal["alpha"].tobytes()),
        "lower_zero": {"trits": LOWER, "packed_sha256": sha(pack(primal["lower"]))}, "eof": True})
    compare("primal", {"p1-coefficients.u8": O.typed_array(primal["alpha"], "u8", (8059,)),
        "p1-reductions.json": O.json_payload(reductions), "p1-exponent-residues.json": O.json_payload(exponent_record(bundle))})
    if phase_count == 6:
        return result
    corrected, roots = bundle.corrected(raw["source"], primal)
    correction = E.source_correction_record(raw, corrected, primal, bundle.basis, roots, bundle.index)
    compare("p1", {"p1-roots.json": O.json_payload(roots),
        "source-lower-remainder.bin": O.typed_array(primal["lower"], "packed3", (LOWER,)),
        "source-top-corrected.bin": O.typed_array(corrected[2], "packed3", (4, TOP)),
        "source-correction.json": O.json_payload(correction)})
    if phase_count == 7:
        return result
    by_character = np.stack([E.grouped_forward(bundle.tables[a]["entries"], corrected[2][a]) for a in range(4)])
    physical_raw = (by_character.sum(axis=0, dtype=np.uint16) % 3).astype(np.uint8)
    corrected_scalar = sum(dot(section["roots"][a], corrected[2][a]) for a in range(4)) % 3
    require(corrected_scalar == raw["selected_scalar"] == dot(state.functional, physical_raw) and
            corrected_scalar == (raw["homogeneous_scalar"] - raw["section_scalar"]) % 3,
            "new_selected_source_full_four_B_scalar_identity")
    B = document("B", {"characters": [0, 1, 2, 3], "physical_trits": PHYSICAL,
        "source_correction_sha256": sha(canonical(correction)), "witness_sha256": oracle["witness_sha256"],
        "corrected_scalar": corrected_scalar, "physical_scalar": int(dot(state.functional, physical_raw)),
        "raw_sha256": sha(pack(physical_raw)), "by_character_sha256": sha(pack(by_character)),
        "all_four_summed": True, "eof": True})
    compare("B", {"physical-by-character.bin": O.typed_array(by_character, "packed3", (4, PHYSICAL)),
        "physical-raw.bin": O.typed_array(physical_raw, "packed3", (PHYSICAL,)), "B.json": O.json_payload(B)})
    if phase_count == 8:
        return result
    physical = E.one_physical_row(physical_raw, state.target, state.functional, state.pivots, state.row,
                                  state.generation, raw["selected_scalar"])
    records = dynamic_delta_records(snapshot, owner, source, sha(canonical(oracle_manifest)), oracle,
                                     raw, correction, roots, reductions, physical, corrected_scalar)
    physical_payloads = {name: O.typed_array(physical[key], "packed3", (PHYSICAL,)) for name, key in
        (("physical-remainder.bin", "remainder"), ("physical-normalized.bin", "normalized"), ("target-remainder.bin", "target"))}
    physical_payloads.update({name: O.json_payload(value) for name, value in records.items()})
    if physical["lambda"] is not None:
        physical_payloads["lambda.bin"] = O.typed_array(physical["lambda"], "packed3", (PHYSICAL,))
    compare("physical", physical_payloads)
    result.update({"physical": physical, "records": records, "physical_payloads": physical_payloads,
                   "raw_word_letters": raw["slp"].values["raw-root"]["length"],
                   "alpha_support": int(np.count_nonzero(primal["alpha"]))})
    return result


def checkpoint_record(snapshot: dict[str, Any], phase_hashes: dict[str, str],
                      oracle_manifest: dict[str, Any] | None) -> dict[str, Any]:
    require(list(phase_hashes) == list(PHASES[:len(phase_hashes)]), "checkpoint_ordered_phase_prefix")
    require((oracle_manifest is not None) == (len(phase_hashes) >= 3), "checkpoint_complete_tree_has_oracle_top")
    return document("checkpoint", {"snapshot_sha256": sha(canonical(snapshot)), "physical_parent_head": snapshot["state_head"],
        "last_complete_phase": list(phase_hashes)[-1] if phase_hashes else None,
        "phase_manifests": [{"phase": key, "sha256": value} for key, value in phase_hashes.items()],
        "current_oracle_manifest_sha256": None if oracle_manifest is None else sha(canonical(oracle_manifest)),
        "witness_sha256": None if oracle_manifest is None else oracle_manifest["witness_sha256"]})


def read_checkpoint(snapshot_root: Path, digest: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None, "checkpoint_file_hash_type")
    raw = path(snapshot_root, "checkpoints/" + digest + ".json").read_bytes()
    require(sha(raw) == digest, "immutable_checkpoint_content_address")
    item = sealed_bytes(raw, SCHEMA + ".checkpoint")
    require(set(unsigned(item)) == {"schema", "snapshot_sha256", "physical_parent_head", "last_complete_phase",
        "phase_manifests", "current_oracle_manifest_sha256", "witness_sha256"}, "checkpoint_exact_fields")
    references = item["phase_manifests"]
    require(isinstance(references, list) and 0 <= len(references) <= len(PHASES) and
            [r["phase"] for r in references] == list(PHASES[:len(references)]) and
            all(set(r) == {"phase", "sha256"} and isinstance(r["sha256"], str) and
                re.fullmatch(r"[0-9a-f]{64}", r["sha256"]) is not None for r in references), "checkpoint_typed_phase_prefix")
    require(item["snapshot_sha256"] == sha(canonical(snapshot)) and item["physical_parent_head"] == snapshot["state_head"] and
            item["last_complete_phase"] == (references[-1]["phase"] if references else None), "checkpoint_same_snapshot_parent")
    if len(references) >= 3:
        require(all(isinstance(item[key], str) and re.fullmatch(r"[0-9a-f]{64}", item[key]) is not None
                    for key in ("current_oracle_manifest_sha256", "witness_sha256")), "tree_checkpoint_complete_top_hashes")
    else:
        require(item["current_oracle_manifest_sha256"] is None and item["witness_sha256"] is None, "uncomputed_oracle_is_null")
    return item


def step_record(snapshot: dict[str, Any], replay: dict[str, Any], predecessor: str | None) -> dict[str, Any]:
    require(list(replay["phase_hashes"]) == list(PHASES) and replay["physical"] is not None,
            "committed_new_step_all_nine_phase_EOF")
    physical, records = replay["physical"], replay["records"]
    instruction = records["instruction.json"]
    return document("step-manifest", {**{key: snapshot[key] for key in
        ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256")}, "step": snapshot["step"] + 1,
        "snapshot_sha256": sha(canonical(snapshot)), "oracle_manifest_sha256": sha(canonical(replay["oracle_manifest"])),
        "witness_sha256": replay["oracle_manifest"]["witness_sha256"], "predecessor_step_manifest_sha256": predecessor,
        "parent_state_head": snapshot["state_head"], "state_head": instruction["rolling_sha256"],
        "rank": snapshot["rank"] + 1, "generation": snapshot["generation"] + 1, "kind": physical["kind"],
        "instruction_sha256": sha(canonical(instruction)), "result_sha256": sha(canonical(records["result.json"])),
        "physical_normalized_sha256": sha(pack(physical["normalized"])), "target_remainder_sha256": sha(pack(physical["target"])),
        "lambda_sha256": None if physical["lambda"] is None else sha(pack(physical["lambda"])),
        "phase_manifests": replay["phase_hashes"], "phase_eof": list(PHASES), "candidate": True, "cross_checked": False, "verified": False})


def head_record(state: PhysicalState, start: dict[str, Any], owner: dict[str, Any], source: dict[str, Any], fixed_sha: str | None,
                last_step: str | None, snapshot_sha: str | None, checkpoint_sha: str | None) -> dict[str, Any]:
    require((snapshot_sha is None) == (checkpoint_sha is None), "head_snapshot_checkpoint_null_together")
    return document("head", {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)),
        "start_sha256": sha(canonical(start)), "fixed_manifest_sha256": fixed_sha, "completed_steps": state.completed_steps,
        "last_step_manifest_sha256": last_step, **{key: value for key, value in state.summary().items()
            if key in ("kind", "rank", "generation", "state_head", "target_remainder_sha256", "lambda_sha256")},
        "current_snapshot_sha256": snapshot_sha, "current_checkpoint_sha256": checkpoint_sha})


def step_directory_check(root: Path) -> None:
    for item in root.iterdir():
        if item.name == "manifest.json":
            require(item.is_file() and not item.is_symlink(), "committed_step_manifest_file")
        else:
            require(re.fullmatch(r"\.manifest\.json\.pending-[0-9a-f]{32}", item.name) is not None and
                    item.is_file() and not item.is_symlink(), "only_step_atomic_write_diagnostic")


def compare_committed_step(root: Path, state: PhysicalState, snapshot: dict[str, Any], replay: dict[str, Any],
                           predecessor: str | None) -> tuple[str, dict[str, Any]]:
    manifest = step_record(snapshot, replay, predecessor)
    step_root = directory(root, "steps/" + f"{state.completed_steps + 1:06d}")
    step_directory_check(step_root)
    require(path(step_root, "manifest.json").read_bytes() == canonical(manifest), "complete_step_manifest_exact_bytes")
    digest = sha(canonical(manifest))
    rows = {name: value[0] for name, value in replay["physical_payloads"].items() if name.endswith(".bin")}
    state.attach(rows, replay["records"]["instruction.json"], replay["records"]["result.json"], digest,
                 "loop-e-" + f"{state.completed_steps + 1:06d}", new_step=True)
    CHECKED_CURSOR.update({"completed_steps": state.completed_steps, "physical_state_head": state.head})
    boundary("new_step_independently_replayed", step=state.completed_steps, rank=state.rank, generation=state.generation)
    return digest, manifest


def replay_head_prefix(root: Path, state: PhysicalState, start: dict[str, Any], owner: dict[str, Any], source: dict[str, Any],
                       fixed_sha: str | None, bundle: FixedBundle | None) -> dict[str, Any]:
    actual_raw = path(root, "HEAD").read_bytes()
    actual = sealed_bytes(actual_raw, SCHEMA + ".head")
    completed = actual["completed_steps"]
    require(type(completed) is int and 0 <= completed <= PHYSICAL - start["rank"], "new_completed_steps_absolute_count")
    require(actual["owner_sha256"] == sha(canonical(owner)) and actual["source_sha256"] == sha(canonical(source)) and
            actual["start_sha256"] == sha(canonical(start)) and actual["fixed_manifest_sha256"] == fixed_sha,
            "HEAD_same_owner_source_start_fixed")
    CHECKED_CURSOR.update({"completed_steps": 0, "physical_state_head": state.head})
    previous, snapshots, steps = None, [], []
    owner_sha, source_sha, start_sha = sha(canonical(owner)), sha(canonical(source)), sha(canonical(start))
    for number in range(completed):
        require(bundle is not None and fixed_sha is not None and state.kind == "Separator" and state.completed_steps == number,
                "committed_step_requires_current_separator")
        snapshot = snapshot_record(state, owner_sha, source_sha, start_sha, fixed_sha)
        snapshot_root = directory(root, "snapshots/" + f"{number:06d}")
        replay = replay_snapshot(snapshot_root, snapshot, len(PHASES), True, bundle, state, owner, source)
        previous, step = compare_committed_step(root, state, snapshot, replay, previous)
        snapshots.append({"step": number, "snapshot_sha256": sha(canonical(snapshot)), "phase_manifests": replay["phase_hashes"],
            "oracle_manifest_sha256": sha(canonical(replay["oracle_manifest"])), "oracle_terminal": replay["oracle_result"]["terminal"],
            "ordinary27_anchor": replay["ordinary27_anchor"], "producer_telemetry": replay["telemetry"]})
        steps.append({"step": number + 1, "manifest_sha256": previous, "state_head": state.head,
            "rank": state.rank, "generation": state.generation, "target_scalar": replay["records"]["result.json"]["target"]["scalar"],
            "selected_scalar": replay["records"]["result.json"]["selected_scalar"], "raw_word_letters": replay["raw_word_letters"],
            "alpha_support": replay["alpha_support"]})
        del replay
    current_snapshot, current_checkpoint, current_oracle = None, None, None
    snapshot_sha, checkpoint_sha = actual["current_snapshot_sha256"], actual["current_checkpoint_sha256"]
    require((snapshot_sha is None) == (checkpoint_sha is None), "HEAD_snapshot_checkpoint_presence")
    if snapshot_sha is not None:
        require(bundle is not None and fixed_sha is not None and state.kind == "Separator", "current_checkpoint_separator")
        snapshot = snapshot_record(state, owner_sha, source_sha, start_sha, fixed_sha)
        require(snapshot_sha == sha(canonical(snapshot)), "HEAD_current_snapshot_hash")
        snapshot_root = directory(root, "snapshots/" + f"{completed:06d}")
        checkpoint = read_checkpoint(snapshot_root, checkpoint_sha, snapshot)
        count = len(checkpoint["phase_manifests"])
        replay = replay_snapshot(snapshot_root, snapshot, count, count >= 3, bundle, state, owner, source)
        wanted = checkpoint_record(snapshot, replay["phase_hashes"], replay["oracle_manifest"])
        same(checkpoint, wanted, "HEAD_current_checkpoint_full_arithmetic_prefix")
        require(sha(canonical(wanted)) == checkpoint_sha, "HEAD_current_checkpoint_exact_hash")
        current_snapshot, current_checkpoint, current_oracle = snapshot, checkpoint, replay["oracle_result"]
        snapshots.append({"step": completed, "snapshot_sha256": snapshot_sha, "phase_manifests": replay["phase_hashes"],
            "oracle_manifest_sha256": None if replay["oracle_manifest"] is None else sha(canonical(replay["oracle_manifest"])),
            "oracle_terminal": None if current_oracle is None else current_oracle["terminal"],
            "producer_telemetry": replay["telemetry"]})
    state.measure()
    expected = head_record(state, start, owner, source, fixed_sha, previous, snapshot_sha, checkpoint_sha)
    require(actual_raw == canonical(expected), "HEAD_entire_replayed_prefix_and_cursor")
    return {"head": expected, "head_sha256": sha(actual_raw), "snapshots": snapshots, "steps": steps,
        "current_snapshot": current_snapshot, "current_checkpoint": current_checkpoint, "current_oracle": current_oracle,
        "last_step_manifest_sha256": previous}


def cap_reached(completed_steps: int, max_appends: int) -> bool:
    require(type(completed_steps) is int and completed_steps >= 0 and type(max_appends) is int and max_appends >= 0,
            "absolute_cap_integer_type")
    return completed_steps >= max_appends


def check_terminal(root: Path, state: PhysicalState, start: dict[str, Any], owner: dict[str, Any], source: dict[str, Any],
                   fixed_sha: str | None, replay: dict[str, Any]) -> dict[str, Any]:
    actual = sealed_bytes(path(root, "result.json").read_bytes(), SCHEMA + ".result")
    terminal = actual["terminal"]
    require(terminal in ("COMPLETE_ZERO_CANDIDATE", "LINEAR_MEMBERSHIP_CANDIDATE", "UNKNOWN_CAP", "UNKNOWN_RESOURCE"),
            "registered_completed_prefix_terminal")
    cap, limit, elapsed = (actual[key] for key in ("max_appends_this_invocation", "max_seconds_this_invocation", "elapsed_seconds"))
    require(type(cap) is int and cap >= 0 and type(limit) in (int, float) and math.isfinite(limit) and limit > 0 and
            type(elapsed) in (int, float) and math.isfinite(elapsed) and elapsed >= 0, "terminal_invocation_limits")
    require(isinstance(actual["invocation_sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", actual["invocation_sha256"]) is not None,
            "terminal_explicit_invocation_reference")
    complete_zero = None
    if state.kind == "LinearMembershipCandidate":
        require(terminal == "LINEAR_MEMBERSHIP_CANDIDATE" and replay["current_snapshot"] is None and
                replay["current_checkpoint"] is None and state.functional is None and not np.any(state.target),
                "linear_target_stops_before_another_oracle")
    else:
        require(terminal != "LINEAR_MEMBERSHIP_CANDIDATE", "nonzero_target_not_linear_member")
        oracle = replay["current_oracle"]
        if terminal == "COMPLETE_ZERO_CANDIDATE":
            require(oracle is not None and oracle["terminal"] == "COMPLETE_ZERO_CANDIDATE" and
                    replay["current_checkpoint"]["last_complete_phase"] == "tree", "complete_zero_current_full_oracle_only")
            complete_zero = sha(canonical(oracle))
        elif terminal == "UNKNOWN_CAP":
            require(cap_reached(state.completed_steps, cap), "UNKNOWN_CAP_absolute_count")
        else:
            require(terminal == "UNKNOWN_RESOURCE", "remaining_incomplete_resource_terminal")
    head = replay["head"]
    result = document("result", {"status": "PASS" if terminal.endswith("_CANDIDATE") else terminal, "terminal": terminal,
        "owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)), "start_sha256": sha(canonical(start)),
        "fixed_manifest_sha256": fixed_sha, "head_sha256": replay["head_sha256"], "completed_steps": state.completed_steps,
        "last_step_manifest_sha256": replay["last_step_manifest_sha256"],
        **{key: value for key, value in state.summary().items() if key in ("kind", "rank", "generation", "state_head",
            "target_remainder_sha256", "lambda_sha256", "lambda_rho2", "direct_pairing")},
        "current_snapshot_sha256": head["current_snapshot_sha256"], "current_checkpoint_sha256": head["current_checkpoint_sha256"],
        "complete_zero_oracle_result_sha256": complete_zero, "new_physical_appends": state.completed_steps,
        "external_e_attached": 1, "old_scans_numerically_replayed": 0, "old_inserts_numerically_replayed": 0,
        "external_e_numerically_replayed": False, "positive_readout": "TASK958_PENDING" if state.kind == "LinearMembershipCandidate" else "NOT_APPLICABLE",
        "separator_premises": "v548-Conn-same-source-map" if terminal == "COMPLETE_ZERO_CANDIDATE" else None,
        "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
        "invocation_sha256": actual["invocation_sha256"],
        "max_appends_this_invocation": cap, "max_seconds_this_invocation": limit, "elapsed_seconds": elapsed,
        "candidate": True, "cross_checked": False, "verified": False})
    same(actual, result, "entire_terminal_result_matches_replayed_HEAD")
    return result


def pending_file(item: Path, allowed: set[str]) -> bool:
    match = re.fullmatch(r"\.(.+)\.pending-[0-9a-f]{32}", item.name)
    return bool(match and match.group(1) in allowed and item.is_file() and not item.is_symlink())


def directory_roster(root: Path, files: set[str], directories: set[str], pending_directories: set[str] = frozenset()) -> None:
    for item in root.iterdir():
        require(not item.is_symlink(), "no_symlink_in_candidate_roster")
        if item.name in files:
            require(item.is_file(), "candidate_named_file_type")
        elif item.name in directories:
            require(item.is_dir(), "candidate_named_directory_type")
        elif pending_file(item, files):
            continue
        else:
            match = re.fullmatch(r"\.pending-(.+)-[0-9a-f]{32}", item.name)
            require(match is not None and match.group(1) in pending_directories and item.is_dir(), "registered_pending_directory_only")


def check_diagnostic(root: Path, name: str) -> None:
    item = root / name
    if not item.exists():
        return
    value = sealed_bytes(path(root, name).read_bytes(), SCHEMA + ".diagnostic")
    require(set(unsigned(value)) == {"schema", "status", "terminal", "phase", "reason", "head_sha256",
        "diagnostic_only", "elapsed_seconds", "candidate", "cross_checked", "verified"}, "diagnostic_exact_fields")
    require(value["status"] == value["terminal"] == ("UNKNOWN_RESOURCE" if name == "resource-stop.json" else "REJECTED") and
            value["diagnostic_only"] is True and value["candidate"] is False and value["cross_checked"] is False and
            value["verified"] is False and type(value["elapsed_seconds"]) in (int, float) and
            math.isfinite(value["elapsed_seconds"]) and value["elapsed_seconds"] >= 0, "diagnostic_is_not_prefix_acceptance")


def check_candidate_roster(root: Path, completed: int) -> dict[str, Any]:
    directory_roster(root, {"owner.json", "source.json", "start.json", "HEAD", "result.json", "resource-stop.json", "rejected.json"},
                     {"fixed", "snapshots", "steps", "invocations"}, {"fixed"})
    for name in ("resource-stop.json", "rejected.json"):
        check_diagnostic(root, name)
    snapshots = root / "snapshots"
    snapshot_numbers = []
    if snapshots.exists():
        for item in snapshots.iterdir():
            require(re.fullmatch(r"[0-9]{6}", item.name) is not None and item.is_dir() and not item.is_symlink() and
                    0 <= int(item.name) <= completed, "reachable_numbered_snapshot_only")
            snapshot_numbers.append(int(item.name))
            directory_roster(item, {"start.json", "oracle-result.json", "oracle-manifest.json"},
                             {"section", "cochain", "tree", "e", "checkpoints"}, set(PHASES[:3]))
            if (item / "e").exists():
                directory_roster(directory(item, "e"), set(), set(PHASES[3:]), set(PHASES[3:]))
            if (item / "checkpoints").exists():
                for checkpoint in directory(item, "checkpoints").iterdir():
                    require(not checkpoint.is_symlink() and checkpoint.is_file() and
                        (re.fullmatch(r"[0-9a-f]{64}\.json", checkpoint.name) is not None or
                         re.fullmatch(r"\.[0-9a-f]{64}\.json\.pending-[0-9a-f]{32}", checkpoint.name) is not None),
                        "checkpoint_named_immutable_or_pending_file")
    require(set(range(completed)).issubset(snapshot_numbers), "all_committed_step_snapshots_present")
    step_numbers = []
    if (root / "steps").exists():
        for item in directory(root, "steps").iterdir():
            require(re.fullmatch(r"[0-9]{6}", item.name) is not None and item.is_dir() and not item.is_symlink() and
                    1 <= int(item.name) <= completed + 1, "reachable_or_one_durable_numbered_step")
            step_directory_check(item)
            step_numbers.append(int(item.name))
    require(set(range(1, completed + 1)).issubset(step_numbers), "all_committed_step_directories_present")
    return {"snapshot_numbers": sorted(snapshot_numbers), "step_numbers": sorted(step_numbers),
            "durable_uncommitted_step": completed + 1 in step_numbers}


def durable_phase(snapshot_root: Path, phase: str, snapshot: dict[str, Any], previous: str | None) -> dict[str, Any]:
    """Authenticate an uncommitted diagnostic's types without accepting its math."""
    root = phase_directory(snapshot_root, phase)
    manifest = sealed_bytes(path(root, "manifest.json").read_bytes(), SCHEMA + ".phase-manifest")
    if phase in PHASES[:3]:
        roster = dict(E.ORACLE_ROSTER[phase])
    else:
        names = {
            "raw": ("raw-word.json", "raw-chain.bin"),
            "source": ("raw-source-d0.bin", "raw-source-d1.bin", "raw-source-d2.bin", "raw-source-aux.bin", "raw-source.json"),
            "primal": ("p1-coefficients.u8", "p1-reductions.json", "p1-exponent-residues.json"),
            "p1": ("p1-roots.json", "source-lower-remainder.bin", "source-top-corrected.bin", "source-correction.json"),
            "B": ("physical-by-character.bin", "physical-raw.bin", "B.json"),
            "physical": ("physical-remainder.bin", "physical-normalized.bin", "target-remainder.bin", "physical-literal.json", "instruction.json", "result.json")}[phase]
        roster = {name: E_ARRAYS[name] if name in E_ARRAYS else ("json", None) for name in names}
        if phase == "physical":
            result = sealed_bytes(path(root, "result.json").read_bytes(), E.SCHEMA + ".result")
            require(result["kind"] in ("Separator", "LinearMembershipCandidate"), "durable_physical_kind")
            if result["kind"] == "Separator":
                roster["lambda.bin"] = E_ARRAYS["lambda.bin"]
    roster["telemetry.json"] = ("json", None)
    require([record["file"] for record in manifest["files"]] == sorted(roster), "durable_phase_exact_typed_roster")
    payloads, objects = {}, {}
    for record in manifest["files"]:
        name = record["file"]
        dtype, shape = roster[name]
        require(set(record) == {"file", "bytes", "sha256", "dtype", "shape"} and
                record["dtype"] == dtype and record["shape"] == shape and type(record["bytes"]) is int and record["bytes"] >= 0,
                "durable_phase_descriptor_type")
        raw = fixed(root, name, (record["bytes"], record["sha256"]))
        if dtype == "json":
            if name == "telemetry.json":
                schema = SCHEMA + ".phase-telemetry"
            elif name == "B.json":
                schema = SCHEMA + ".B"
            elif phase in PHASES[:3]:
                schema = O.SCHEMA + "." + name[:-5]
            else:
                schema = E.SCHEMA + "." + name[:-5]
            objects[name] = canonical_plain(raw, schema) if name == "instruction.json" else sealed_bytes(raw, schema)
        else:
            typed_input(raw, dtype, shape)
        payloads[name] = (raw, dtype, shape)
    same(manifest, phase_metadata(phase, snapshot, previous, payloads), "durable_same_snapshot_manifest_chain")
    require({p.name for p in root.iterdir()} == set(payloads) | {"manifest.json"}, "durable_phase_directory_EOF")
    telemetry = objects["telemetry.json"]
    elapsed, begun, ended = (telemetry[key] for key in ("elapsed_seconds", "begun_elapsed_seconds", "ended_elapsed_seconds"))
    require(all(type(x) in (int, float) and math.isfinite(x) and x >= 0 for x in (elapsed, begun, ended)) and
            ended >= begun and abs(ended - begun - elapsed) < 3e-6, "durable_phase_finite_start_EOF")
    same(telemetry, document("phase-telemetry", {"phase": phase, "elapsed_seconds": elapsed, "begun_elapsed_seconds": begun,
        "ended_elapsed_seconds": ended, "payload_bytes": sum(len(raw) for name, (raw, _, _) in payloads.items() if name != "telemetry.json"),
        "eof": True}), "durable_phase_payload_byte_count")
    return {"sha256": sha(canonical(manifest)), "payloads": payloads, "objects": objects}


def check_durable_tail(root: Path, state: PhysicalState, start: dict[str, Any], owner: dict[str, Any], source: dict[str, Any],
                       fixed_sha: str | None, roster: dict[str, Any]) -> dict[str, Any]:
    number = state.completed_steps
    summary = {"counted_as_committed": False, "arithmetic_accepted_beyond_HEAD": False,
               "durable_phase_count": 0, "durable_uncommitted_step": roster["durable_uncommitted_step"]}
    if number not in roster["snapshot_numbers"]:
        require(not roster["durable_uncommitted_step"], "extra_step_requires_same_snapshot")
        return summary
    require(state.kind == "Separator" and fixed_sha is not None, "durable_tail_requires_separator_snapshot")
    snapshot = snapshot_record(state, sha(canonical(owner)), sha(canonical(source)), sha(canonical(start)), fixed_sha)
    snapshot_root = directory(root, "snapshots/" + f"{number:06d}")
    require(path(snapshot_root, "start.json").read_bytes() == canonical(snapshot), "durable_tail_actual_current_snapshot")
    hashes, records = {}, {}
    gap = False
    for phase in PHASES:
        where = snapshot_root / (phase if phase in PHASES[:3] else "e/" + phase)
        if not where.exists():
            gap = True
            continue
        require(not gap, "durable_phases_form_one_prefix")
        record = durable_phase(snapshot_root, phase, snapshot, list(hashes.values())[-1] if hashes else None)
        hashes[phase], records[phase] = record["sha256"], record
    summary["durable_phase_count"] = len(hashes)
    have_result, have_manifest = (snapshot_root / "oracle-result.json").exists(), (snapshot_root / "oracle-manifest.json").exists()
    oracle_manifest = None
    if have_result or have_manifest:
        require(len(hashes) >= 3, "durable_oracle_top_requires_complete_tree")
        tree = {"metadata": records["tree"]["objects"]["tree.json"], "witness": records["tree"]["objects"]["witness.json"]}
        result, oracle_manifest = current_oracle_records(snapshot, {key: hashes[key] for key in PHASES[:3]}, tree)
        if have_result:
            require(path(snapshot_root, "oracle-result.json").read_bytes() == canonical(result), "durable_oracle_result_same_snapshot")
        if have_manifest:
            require(have_result and path(snapshot_root, "oracle-manifest.json").read_bytes() == canonical(oracle_manifest),
                    "durable_oracle_manifest_same_snapshot")
    if len(hashes) > 3:
        require(have_result and have_manifest and result["terminal"] == "VIOLATION_CANDIDATE", "durable_E_complete_current_oracle")
    if roster["durable_uncommitted_step"]:
        require(len(hashes) == 9 and oracle_manifest is not None, "extra_numbered_step_requires_all_nine_durable_phases")
        data = records["physical"]
        result, instruction = data["objects"]["result.json"], data["objects"]["instruction.json"]
        require(instruction["predecessor"] == result["parent_state_head"] == state.head and
                instruction["rolling_sha256"] == result["state_head"] == sha(bytes.fromhex(state.head) +
                canonical({key: value for key, value in instruction.items() if key != "rolling_sha256"})), "durable_uncommitted_rolling_parent")
        plain_target(result["target"])
        physical = {"kind": result["kind"], "normalized": unpack(data["payloads"]["physical-normalized.bin"][0], PHYSICAL),
            "target": unpack(data["payloads"]["target-remainder.bin"][0], PHYSICAL),
            "lambda": unpack(data["payloads"]["lambda.bin"][0], PHYSICAL) if "lambda.bin" in data["payloads"] else None}
        replay = {"phase_hashes": hashes, "physical": physical, "records": data["objects"], "oracle_manifest": oracle_manifest}
        previous = None if number == 0 else sha(path(root, "steps/" + f"{number:06d}" + "/manifest.json").read_bytes())
        expected = step_record(snapshot, replay, previous)
        require(path(root, "steps/" + f"{number + 1:06d}" + "/manifest.json").read_bytes() == canonical(expected),
                "durable_uncommitted_step_manifest_exact_bytes")
    return summary


def invocation_before_heads(root: Path, count: int, start: dict[str, Any], owner: dict[str, Any], source: dict[str, Any],
                            fixed_sha: str | None) -> set[str]:
    previous = None
    summary = start
    if count:
        raw = path(root, "steps/" + f"{count:06d}" + "/manifest.json").read_bytes()
        summary = sealed_bytes(raw, SCHEMA + ".step-manifest")
        previous = sha(raw)
    body = {"owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)), "start_sha256": sha(canonical(start)),
        "fixed_manifest_sha256": fixed_sha, "completed_steps": count, "last_step_manifest_sha256": previous,
        **{key: summary[key] for key in ("kind", "rank", "generation", "state_head", "target_remainder_sha256", "lambda_sha256")},
        "current_snapshot_sha256": None, "current_checkpoint_sha256": None}
    hashes = {sha(canonical(document("head", body)))}
    where = root / "snapshots" / f"{count:06d}"
    if where.exists():
        snapshot = sealed_bytes(path(where, "start.json").read_bytes(), SCHEMA + ".snapshot")
        require(all(snapshot[key] == body[key] for key in ("owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256",
            "kind", "rank", "generation", "state_head", "target_remainder_sha256", "lambda_sha256")), "invocation_before_snapshot_join")
        if (where / "checkpoints").exists():
            for item in directory(where, "checkpoints").iterdir():
                if re.fullmatch(r"[0-9a-f]{64}\.json", item.name) is None:
                    continue
                checkpoint = read_checkpoint(where, item.stem, snapshot)
                for record in checkpoint["phase_manifests"]:
                    require(record["sha256"] == sha(path(phase_directory(where, record["phase"]), "manifest.json").read_bytes()),
                            "invocation_before_checkpoint_uses_same_phase_bytes")
                hashes.add(sha(canonical(document("head", {**body, "current_snapshot_sha256": sha(canonical(snapshot)),
                    "current_checkpoint_sha256": item.stem}))))
    return hashes


def check_invocations(root: Path, start: dict[str, Any], owner: dict[str, Any], source: dict[str, Any], fixed_sha: str | None,
                      result: dict[str, Any]) -> list[dict[str, Any]]:
    directory_root = directory(root, "invocations")
    rows, selected = [], None
    for item in sorted(directory_root.iterdir()):
        require(item.is_file() and not item.is_symlink(), "invocation_file_type")
        if re.fullmatch(r"\.[0-9a-f]{32}\.json\.pending-[0-9a-f]{32}", item.name):
            continue
        require(re.fullmatch(r"[0-9a-f]{32}\.json", item.name) is not None, "invocation_uuid_filename")
        raw = item.read_bytes()
        value = sealed_bytes(raw, SCHEMA + ".invocation")
        require(set(unsigned(value)) == {"schema", "invocation", "owner_sha256", "source_sha256", "start_sha256", "fixed_manifest_sha256",
            "head_before_sha256", "completed_steps_before", "resume", "max_appends", "max_seconds", "started_utc"}, "invocation_exact_fields")
        require(value["invocation"] == item.stem and value["owner_sha256"] == sha(canonical(owner)) and
                value["source_sha256"] == sha(canonical(source)) and value["start_sha256"] == sha(canonical(start)) and
                value["fixed_manifest_sha256"] == fixed_sha and type(value["resume"]) is bool and
                type(value["completed_steps_before"]) is int and 0 <= value["completed_steps_before"] <= result["completed_steps"] and
                type(value["max_appends"]) is int and value["max_appends"] >= 0 and type(value["max_seconds"]) in (int, float) and
                math.isfinite(value["max_seconds"]) and value["max_seconds"] > 0 and isinstance(value["started_utc"], str) and
                re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value["started_utc"]) is not None,
                "invocation_owner_source_limits_and_start")
        before = value["completed_steps_before"]
        require(value["head_before_sha256"] in invocation_before_heads(root, before, start, owner, source, fixed_sha),
                "invocation_before_HEAD_in_replayed_history")
        require(value["resume"] or before == 0, "fresh_invocation_cannot_reset_new_count")
        if sha(raw) == result["invocation_sha256"]:
            require(selected is None and value["max_appends"] == result["max_appends_this_invocation"] and
                    value["max_seconds"] == result["max_seconds_this_invocation"], "terminal_explicit_invocation_join")
            require(result["completed_steps"] - before <= max(0, value["max_appends"] - before), "cumulative_cap_carried_across_resume")
            selected = value
        rows.append({"sha256": sha(raw), **unsigned(value)})
    require(selected is not None, "terminal_invocation_receipt_present")
    return rows


def check_actual(args: argparse.Namespace) -> dict[str, Any]:
    root = args.candidate_root
    require(root.is_dir() and not root.is_symlink(), "new_candidate_root_directory")
    source = producer_source(root)
    oracle = E.read_oracle(args)
    accepted_e = read_external_e(args, oracle)
    metadata = O.accepted_refinement_metadata(args)
    accepted_state = O.current_snapshot(args, metadata)
    tables = REFINE.load_tables(args)
    old_start, old_owner = E.new_start_owner(accepted_state, tables, oracle)
    same(accepted_e["objects"]["start.json"], old_start, "external_E_actual_anchor_start")
    same(accepted_e["objects"]["owner.json"], old_owner, "external_E_actual_anchor_owner")
    with ExitStack() as stack:
        state = stack.enter_context(PhysicalState(args, accepted_state, old_start))
        state.attach(accepted_e["payloads"], accepted_e["objects"]["instruction.json"], accepted_e["objects"]["result.json"],
                     E_FILES["output/manifest.json"][1], "external-e", new_step=False)
        start, owner = root_start_owner(state, accepted_e, oracle)
        require(path(root, "start.json").read_bytes() == canonical(start) and
                path(root, "owner.json").read_bytes() == canonical(owner), "immutable_root_owner_and_imported_start")
        fixed_sha, bundle = None, None
        if state.kind == "Separator":
            context, words = BASE.checker_source_context()
            geometry = O.Geometry(context)
            bundle = stack.enter_context(FixedBundle(args, accepted_state, words, tables, geometry))
            fixed_sha, _ = check_fixed(root, bundle, oracle, sha(canonical(owner)), sha(canonical(source)))
        replay = replay_head_prefix(root, state, start, owner, source, fixed_sha, bundle)
        roster = check_candidate_roster(root, state.completed_steps)
        # All data beyond HEAD remains diagnostic; its public type is separately
        # authenticated without claiming it was part of the committed prefix.
        durable = check_durable_tail(root, state, start, owner, source, fixed_sha, roster)
        result = check_terminal(root, state, start, owner, source, fixed_sha, replay)
        invocations = check_invocations(root, start, owner, source, fixed_sha, result)
        boundary("new_complete_prefix_checked", completed_steps=state.completed_steps, terminal=result["terminal"])
        return document("checker-result", {"status": "PASS", "terminal": result["terminal"], "kind": state.kind,
            "owner_sha256": sha(canonical(owner)), "source_sha256": sha(canonical(source)), "start_sha256": sha(canonical(start)),
            "fixed_manifest_sha256": fixed_sha, "head_sha256": replay["head_sha256"], "result_sha256": sha(canonical(result)),
            "completed_steps": state.completed_steps, "prefix_steps_replayed": len(replay["steps"]),
            "rank": state.rank, "generation": state.generation, "state_head": state.head,
            "target_remainder_sha256": sha(pack(state.target)), "lambda_sha256": None if state.functional is None else sha(pack(state.functional)),
            "lambda_rho2": state.derived(), "direct_pairing": state.direct_pairing,
            "accepted_external_e_layout": external_e_layout(accepted_e), "accepted_oracle_layout": E.oracle_layout(oracle),
            "snapshots": replay["snapshots"], "steps": replay["steps"], "checked_cursor": copy.deepcopy(CHECKED_CURSOR),
            "all_new_committed_arrays_and_json_compared": True, "current_checkpoint_fully_compared": True,
            "current_snapshot_sha256": replay["head"]["current_snapshot_sha256"],
            "current_checkpoint_sha256": replay["head"]["current_checkpoint_sha256"],
            "current_oracle_terminal": None if replay["current_oracle"] is None else replay["current_oracle"]["terminal"],
            "full_four_character_scope": True, "section_equalities_each": 8059, "chords_each": CHORDS, "auxiliary_tests_each": 2,
            "ordinary27_actual_source": True, "source_lower_trits_each_E": LOWER, "literal_modulus": 54,
            "all_four_B_summed_each_E": True, "external_e_attached": 1, "external_e_numerically_replayed": False,
            "old_scans_numerically_replayed": 0, "old_inserts_numerically_replayed": 0, "old_success_suites": 0,
            "durable_tail": durable, "invocations": invocations, "physical_appends": state.completed_steps,
            "positive_readout": result["positive_readout"], "grade2_member": "NOT_DECIDED", "grade2_nonmember": "NOT_DECIDED", "full_A0": False,
            "whole_normalized_word_replay": False, "eleven_slot_replay": False,
            "checker_sha256": sha(Path(__file__).read_bytes()), "retained_E_checker_sha256": E_CHECKER_SHA,
            "oracle_checker_v2_sha256": ORACLE_CHECKER_SHA, "retained_E_oracle_checker_v1_sha256": E.ORACLE_CHECKER_SHA,
            "python": sys.version, "numpy": np.__version__, "elapsed_seconds": time.monotonic() - STARTED,
            "candidate": True, "cross_checked": False, "verified": False})


def rejected(operation: Callable[[], Any], label: str) -> None:
    try:
        operation()
    except (ValueError, KeyError, TypeError, AssertionError):
        return
    raise ValueError("cegar_checker:missing_required_rejection:" + label)


def parent_layout_selftest(args: argparse.Namespace) -> dict[str, Any]:
    oracle = E.read_oracle(args)
    accepted = read_external_e(args, oracle)
    cases = ("external-e-kind", "external-e-checker-incomplete", "external-e-target-parent",
             "external-e-ordinary-rho2-claim", "external-e-current-head")
    for label in cases:
        mutant = copy.deepcopy(accepted)
        if label == "external-e-kind":
            mutant["entries"]["output/HEAD"]["kind"] = "MEMBER"
        elif label == "external-e-checker-incomplete":
            mutant["entries"]["checker-result.json"]["all_arrays_and_json_compared"] = False
        elif label == "external-e-target-parent":
            mutant["objects"]["result.json"]["target"]["parent_remainder_sha256"] = "0" * 64
            mutant["entries"]["output/result.json"] = mutant["objects"]["result.json"]
        elif label == "external-e-ordinary-rho2-claim":
            mutant["objects"]["result.json"]["target_derivation"]["original_rho2_directly_read"] = True
            mutant["entries"]["output/result.json"] = mutant["objects"]["result.json"]
        else:
            mutant["entries"]["output/HEAD"]["state_head"] = "0" * 64
        rejected(lambda: external_e_semantics(mutant, oracle), label)
    return {"schema": SCHEMA + ".parent-layout-selftest", "status": "PASS", "metadata_only": True,
        "accepted_oracle_layout": E.oracle_layout(oracle), "accepted_external_e_layout": external_e_layout(accepted),
        "rejected_cases": list(cases), "old_success_suites": 0, "cross_checked": False, "verified": False}


def selftest() -> dict[str, Any]:
    """Only new snapshot/phase/HEAD/cap and plain-target interfaces."""
    tests = []
    owner, source = document("owner", {"fixture": "new-protocol"}), document("source", {"fixture": "new-protocol"})
    target = np.zeros(PHYSICAL, dtype=np.uint8); target[4] = 1
    functional = target.copy()
    base = np.zeros(PHYSICAL, dtype=np.uint8); base[0] = 1
    initial = {"kind": "Separator", "rank": 1, "generation": 23, "state_head": "1" * 64,
        "target_remainder_sha256": sha(pack(target)), "lambda_sha256": sha(pack(functional)),
        "accepted_target_derivation_parents": [], "lambda_rho2": {"original_rho2_packed_sha256": "2" * 64},
        "direct_pairing": {"rows": 1, "row_pairings_sha256": sha(b"\0"), "lambda_pivots": 0,
                           "lambda_parent_remainder": 1, "lambda_new_remainder": 1}}
    with tempfile.TemporaryDirectory(prefix="r07-cegar-checker-") as temporary:
        root = Path(temporary)
        (root / "state").mkdir(); (root / "state/physical.bin").write_bytes(pack(base))
        accepted = {"pivots": [{"offer": 0, "lead": 0, "physical_offset": 0, "coefficient_offset": None, "rolling_sha256": "1" * 64}],
                    "saved_rows": [], "start_target": target, "start_lambda": functional}
        with PhysicalState(argparse.Namespace(state_root=root), accepted, initial, base_count=1) as state:
            immutable_start = document("start", {**state.summary(), "completed_steps": 0})
            snapshot = snapshot_record(state, sha(canonical(owner)), sha(canonical(source)), sha(canonical(immutable_start)), "3" * 64)
            witness = O.document("witness", {"kind": "none", "cycles": [], "eta": [0, 0], "tau": [0] * 5,
                "scalar": 0, "materialization": "NOT_NEEDED_FOR_ZERO_TEST"})
            tree = {"metadata": {"terminal": "COMPLETE_ZERO_CANDIDATE"}, "witness": witness}
            oracle_result, _ = current_oracle_records(snapshot, {key: str(index + 4) * 64 for index, key in enumerate(PHASES[:3])}, tree)
            oracle_snapshot_join(oracle_result, snapshot)
            for key in ("lambda_sha256", "state_head", "owner_sha256", "source_sha256"):
                mutant = copy.deepcopy(oracle_result); mutant[key] = "f" * 64
                rejected(lambda: oracle_snapshot_join(mutant, snapshot), "stale-current-oracle:" + key)
            tests.append({"name": "current-snapshot-witness-owner-source-join", "status": "PASS"})

            def append_test(raw: np.ndarray) -> dict[str, Any]:
                result = E.one_physical_row(raw, state.target, state.functional, state.pivots, state.row, state.generation, 1)
                instruction = {"schema": E.SCHEMA + ".instruction", "predecessor": state.head, "offer": state.generation,
                    "rank": state.rank + 1, "generation": state.generation + 1, "physical_offset": state.rank * ROW_BYTES,
                    "lead": result["lead"], "physical_sha256": sha(pack(result["normalized"])),
                    "target_remainder_sha256": sha(pack(result["target"])), "target_scalar": result["target_scalar"]}
                instruction["rolling_sha256"] = sha(bytes.fromhex(state.head) + canonical(instruction))
                target_record = {"parent_remainder_sha256": sha(pack(state.target)), "remainder_sha256": sha(pack(result["target"])),
                                 "scalar": result["target_scalar"]}
                record = {"parent_state_head": state.head, "state_head": instruction["rolling_sha256"], "rank_after": state.rank + 1,
                    "generation_after": state.generation + 1, "kind": result["kind"], "target": target_record, "separator": result["separator"]}
                payloads = {"physical-normalized.bin": pack(result["normalized"]), "target-remainder.bin": pack(result["target"])}
                if result["lambda"] is not None:
                    payloads["lambda.bin"] = pack(result["lambda"])
                state.attach(payloads, instruction, record, "7" * 64, "loop-e-" + f"{state.completed_steps + 1:06d}", new_step=True)
                return result

            raw = np.zeros(PHYSICAL, dtype=np.uint8); raw[2] = raw[4] = 1
            first = append_test(raw)
            require(first["target_scalar"] == 0 and state.completed_steps == 1 and cap_reached(state.completed_steps, 1),
                    "actual_plain_target_scalar_zero_and_cap_one")
            head = head_record(state, immutable_start, owner, source, "3" * 64, "7" * 64, None, None)
            (root / "HEAD").write_bytes(canonical(head))
            loaded = sealed_bytes((root / "HEAD").read_bytes(), SCHEMA + ".head")
            require(loaded["completed_steps"] == 1 and cap_reached(loaded["completed_steps"], 1) and
                    not cap_reached(loaded["completed_steps"], 32), "actual_saved_absolute_cap_carry")
            second = append_test(state.target.copy())
            require(state.completed_steps == 2 and second["target_scalar"] == 1 and state.kind == "LinearMembershipCandidate" and
                    state.functional is None and not np.any(state.target), "target_zero_is_only_linear_candidate")
            rejected(lambda: plain_target({"parent_remainder_sha256": "0" * 64, "remainder_sha256": "1" * 64, "scalar": False}), "target_boolean")
            rejected(lambda: plain_target({"parent_remainder_sha256": "0" * 64, "remainder_sha256": "1" * 64, "scalar": 0,
                                          "sha256": "2" * 64}), "target_has_no_generic_seal")
            tests.append({"name": "actual-delta-cap-carry-plain-zero-and-linear-boundary", "status": "PASS"})

        snapshot_root = root / "snapshot"
        snapshot_root.mkdir(); (snapshot_root / "section").mkdir(); (snapshot_root / "checkpoints").mkdir()
        (snapshot_root / "start.json").write_bytes(canonical(snapshot))
        checkpoint0 = checkpoint_record(snapshot, {}, None)
        checkpoint0_sha = sha(canonical(checkpoint0))
        (snapshot_root / "checkpoints" / (checkpoint0_sha + ".json")).write_bytes(canonical(checkpoint0))
        fixture = {"roots": np.zeros((4, TOP), dtype=np.uint8), "p1_values": np.zeros((4, 8059), dtype=np.uint8),
            "chi": np.zeros(8059, dtype=np.uint8), "beta": np.zeros(2014, dtype=np.uint8), "kappa": np.zeros(LOWER, dtype=np.uint8),
            "equation_values": np.zeros(8059, dtype=np.uint8), "equation_residuals": np.zeros(8059, dtype=np.uint8),
            "original": np.zeros(8059, dtype=np.uint32), "embedded": np.zeros(8059, dtype=np.uint32),
            "new_order": np.zeros(6045, dtype=np.uint32), "old_order": np.zeros(2014, dtype=np.uint32)}
        payloads = O.section_payloads(fixture)
        telemetry = document("phase-telemetry", {"phase": "section", "elapsed_seconds": 0.25, "begun_elapsed_seconds": 1.0,
            "ended_elapsed_seconds": 1.25, "payload_bytes": sum(len(raw) for raw, _, _ in payloads.values()), "eof": True})
        complete = {**payloads, "telemetry.json": O.json_payload(telemetry)}
        manifest = phase_metadata("section", snapshot, None, complete)
        for name, (raw, _, _) in complete.items():
            (snapshot_root / "section" / name).write_bytes(raw)
        (snapshot_root / "section/manifest.json").write_bytes(canonical(manifest))
        require(read_checkpoint(snapshot_root, checkpoint0_sha, snapshot)["phase_manifests"] == [],
                "durable_phase_before_HEAD_does_not_advance_checkpoint")
        CHECKED_CURSOR["phase_manifest_hashes"] = []
        phase_sha, _ = compare_phase(snapshot_root, "section", snapshot, None, payloads)
        checkpoint1 = checkpoint_record(snapshot, {"section": phase_sha}, None)
        checkpoint1_sha = sha(canonical(checkpoint1))
        (snapshot_root / "checkpoints" / (checkpoint1_sha + ".json")).write_bytes(canonical(checkpoint1))
        require(len(read_checkpoint(snapshot_root, checkpoint1_sha, snapshot)["phase_manifests"]) == 1 and
                read_checkpoint(snapshot_root, checkpoint0_sha, snapshot)["phase_manifests"] == [], "immutable_checkpoint_resume_roundtrip")
        changed = copy.deepcopy(snapshot); changed["source_sha256"] = "f" * 64
        rejected(lambda: read_checkpoint(snapshot_root, checkpoint1_sha, changed), "checkpoint_source_mismatch")
        altered = copy.deepcopy(manifest); altered["owner_sha256"] = "f" * 64
        altered = seal(unsigned(altered))
        (snapshot_root / "section/manifest.json").write_bytes(canonical(altered))
        rejected(lambda: compare_phase(snapshot_root, "section", snapshot, None, payloads), "phase_owner_mismatch")
        (snapshot_root / "section/manifest.json").write_bytes(canonical(manifest))
        (snapshot_root / "section/chi.u8").write_bytes(payloads["chi.u8"][0] + b"\0")
        rejected(lambda: compare_phase(snapshot_root, "section", snapshot, None, payloads), "phase_false_EOF")
        tests.append({"name": "durable-phase-before-HEAD-checkpoint-resume-and-full-EOF", "status": "PASS"})
    return document("selftest", {"status": "PASS", "tests": tests, "old_success_suites": 0,
        "fixture_scope": "new-protocol-and-two-physical-rows;no-old-oracle-suite", "candidate": False, "cross_checked": False, "verified": False})


def main() -> int:
    global STARTED, DEADLINE
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("state", "delta", "seed34", "packet", "refinement", "oracle", "e", "prepare", "p1", "task712"):
        parser.add_argument("--" + name + "-root", type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    parser.add_argument("--candidate-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-seconds", type=float, default=10800)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--parent-layout-selftest", action="store_true")
    args = parser.parse_args()
    STARTED = time.monotonic()
    require(math.isfinite(args.max_seconds) and args.max_seconds > 0, "finite_positive_checker_deadline")
    DEADLINE = STARTED + args.max_seconds
    def interrupted(signum: int, frame: Any) -> None:
        raise ResourceStop("signal-" + str(signum) + ":" + LAST_PHASE)
    signal.signal(signal.SIGINT, interrupted); signal.signal(signal.SIGTERM, interrupted)
    def retained_progress(phase: str, **fields: Any) -> None:
        boundary("retained:" + phase, **fields)
    for module in (E, O, E.ORACLE, REFINE, FIXED, LEGACY, LEGACY.ROOTS, BASE):
        for name in ("boundary", "progress"):
            if hasattr(module, name):
                setattr(module, name, retained_progress)
    exit_code = 0
    try:
        if args.selftest:
            result = selftest()
        else:
            require(all(getattr(args, name + "_root") is not None for name in
                ("state", "delta", "seed34", "packet", "refinement", "oracle", "e")), "actual_seven_saved_roots")
            if args.parent_layout_selftest:
                result = parent_layout_selftest(args)
            else:
                require(args.candidate_root is not None and args.output is not None and len(args.block_root) == 4 and
                    all(getattr(args, name + "_root") is not None for name in ("prepare", "p1", "task712")), "actual_full_roots_and_report")
                result = check_actual(args)
    except (ResourceStop, E.ResourceStop, O.ResourceStop, E.ORACLE.ResourceStop, REFINE.ResourceStop):
        result = document("checker-result", {"status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE", "phase": LAST_PHASE,
            "checked_cursor": copy.deepcopy(CHECKED_CURSOR), "all_new_committed_arrays_and_json_compared": False,
            "elapsed_seconds": time.monotonic() - STARTED, "candidate": False, "cross_checked": False, "verified": False})
        exit_code = 3
    except Exception as error:
        result = document("checker-result", {"status": "FAIL", "reason": type(error).__name__ + ":" + str(error), "phase": LAST_PHASE,
            "checked_cursor": copy.deepcopy(CHECKED_CURSOR), "all_new_committed_arrays_and_json_compared": False,
            "elapsed_seconds": time.monotonic() - STARTED, "candidate": False, "cross_checked": False, "verified": False})
        exit_code = 1
    raw = canonical(result)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(raw)
    sys.stdout.buffer.write(raw)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
