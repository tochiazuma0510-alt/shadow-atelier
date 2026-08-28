#!/usr/bin/env python3
"""Independent, fail-closed checker for the task198b 6,441-row roof receipt.

No task198 producer code or helper is imported.  The checker rebuilds the
frozen roster from authenticated predecessor arithmetic, builds a second
Gamma traversal with reversed generator/tie order, invokes the independently
implemented task157ee factor-presentation checker, and replays the typed
10 -> 11 -> 7 bridge on all rows.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import struct
import sys
import time
import zlib
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-seven-context-roof-presentation/v1"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v3"
RESUME_MANIFEST_SCHEMA = SCHEMA + "/resume-manifest/v2"
SELFTEST_SCHEMA = "d972-r07-seven-context-roof-presentation-selftest/v2"
ISO = "ROOF_BRIDGE_ISOMORPHISM"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
Q0_ORDER, GAMMA_ORDER, DELTA_ORDER = 1_469_664, 243, 357_128_352
PRESENTATION_ROWS = 6_441
RESOURCE_COUNTERS = ("q0_states", "q0_edges", "presentation_rows",
                     "gamma_operations", "dag_nodes", "serialized_bytes",
                     "checkpoint_bytes")

TASK176_BYTES = 13_649_089
TASK176_SHA = "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41"
TASK176_ARTIFACT = "9635036013"
TASK176_ZIP_SHA = "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912"
TASK176_RUN = "33044121344"
TASK176_HEAD = "0533e42019c9f67f6cec3d1566152db17b903836"
TASK176_MEMBER = "d972_r07_all_seven_extension_section_census_v1.json"
TASK176_MANIFEST = "ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json"
TASK176_TERMINAL = "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"
FUTURE_RESUME_CHECKPOINT = \
    "ci/in/d972_r07_seven_context_roof_presentation_resume_v1.checkpoint.json"
OUTPUT_RESUME_CHECKPOINT = \
    "ci/out/d972_r07_seven_context_roof_presentation_resume_v1.checkpoint.json"
OUTPUT_RESUME_MANIFEST = \
    "ci/out/d972_r07_seven_context_roof_presentation_resume_v1.manifest.json"
TEN_TO_ELEVEN = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
DELETE_DUPLICATE = (0, 1, 2, 3, 5, 6, 7, 8, 9, 10)
SEVEN_BLOCKS = ((0, 1, 2), (3, 0, 4), (5,), (6,), (7,), (8,), (9,))
TASK172_ROSTER_SHA = "42481a9ab6c72d751824454d05fb2d0298a227718750a2c2727af4e690c968bc"

COORDINATES = [
    {"construction": "d_E(C21)", "context_id": 21, "index": 0,
     "role": "hexagon_fxy", "source": "(x,y)", "type": "E3"},
    {"construction": "d_E(C22)", "context_id": 22, "index": 1,
     "role": "hexagon_fxz", "source": "(x,z)", "type": "E3"},
    {"construction": "d_E(C23)", "context_id": 23, "index": 2,
     "role": "hexagon_fyz", "source": "(y,z)", "type": "E3"},
    {"construction": "d_E(C24)", "context_id": 24, "index": 3,
     "role": "hexagon_fux", "source": "(u,x)", "type": "E3"},
    {"construction": "d_E(C25)", "context_id": 25, "index": 4,
     "role": "hexagon_fuy", "source": "(u,y)", "type": "E3"},
    {"construction": "C1", "context_id": 1, "index": 5,
     "role": "pentagon_b1", "source": "b1/phi234", "type": "E4"},
    {"construction": "C27", "context_id": 27, "index": 6,
     "role": "pentagon_b2", "source": "b2/phi1_23_4", "type": "E4"},
    {"construction": "C21", "context_id": 21, "index": 7,
     "role": "pentagon_b3", "source": "b3/phi123", "type": "E4"},
    {"construction": "C26", "context_id": 26, "index": 8,
     "role": "pentagon_b5_inverse_slot", "source": "b5/phi12_3_4", "type": "E4"},
    {"construction": "C28", "context_id": 28, "index": 9,
     "role": "pentagon_b4_inverse_slot", "source": "b4/phi1_2_34", "type": "E4"},
]

OCCURRENCES = [
    ("H1", 1, "H1_fxy", "E3", 0, 21, "hexagon_fxy", 1, "direct", [3, 2]),
    ("H1", 2, "H1_fxz", "E3", 1, 22, "hexagon_fxz", -1, "inverse", [3]),
    ("H1", 3, "H1_fyz", "E3", 2, 23, "hexagon_fyz", 1, "direct", []),
    ("H2", 1, "H2_fux", "E3", 3, 24, "hexagon_fux", -1, "inverse", [6, 5]),
    ("H2", 2, "H2_fxy", "E3", 0, 21, "hexagon_fxy", -1, "inverse", [6]),
    ("H2", 3, "H2_fuy", "E3", 4, 25, "hexagon_fuy", 1, "direct", []),
    ("P1", 1, "P_b1", "E4", 5, 1, "pentagon_b1", 1, "direct", [11, 10, 9, 8]),
    ("P2", 1, "P_b2", "E4", 6, 27, "pentagon_b2", 1, "direct", [11, 10, 9]),
    ("P3", 1, "P_b3", "E4", 7, 21, "pentagon_b3", 1, "direct", [11, 10]),
    ("P5", 1, "P_b5_inverse", "E4", 8, 26, "pentagon_b5_inverse_slot", -1, "inverse", [11]),
    ("P4", 1, "P_b4_inverse", "E4", 9, 28, "pentagon_b4_inverse_slot", -1, "inverse", []),
]


def occurrence_ledger() -> list[dict[str, Any]]:
    answer = []
    for ordinal, row in enumerate(OCCURRENCES, 1):
        block, slot, tag, kind, ten, context, role, sign, orient, prefix = row
        answer.append({"ordinal": ordinal, "block": block,
            "block_index": 1 if block == "H1" else 2 if block == "H2" else ordinal - 4,
            "block_slot": slot, "occurrence": tag, "type": kind,
            "ten_index": ten, "context_id": context, "role": role,
            "factor_sign": sign, "orientation": orient,
            "fox_prefix_occurrences": prefix})
    return answer


PINS = {
    "task175_producer": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306, "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"),
    "task175_checker": ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 88503, "0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce"),
    "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109, "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980, "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    "task179_producer": ("search/d972_r07_positive_common_word_colgen_v1.py", 123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "task179_checker": ("crosscheck/check_d972_r07_positive_common_word_colgen_v1.py", 73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"),
    "task176_task": ("sol/luna_task_176_r07_all_seven_extension_section_census_v1.md", 7054, "a1778c17c33e42880a6dd0c2480303a13702cb38950cf836a4ca9d8cca6fa332"),
    "task176_reply": ("sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md", 47164, "aa173122310e33910d546bd3e02a98a6bf16aea9d3aad066b7d49976098ebb0c"),
    "proof125": ("sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md", 8545, "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3"),
    "proof145": ("sol/proof_r07_task179_relative_frattini_successor_v145.md", 13819, "b08f140838b78424cafa9528eafbcab9442f94cf92ce2cb42e15fc88ed489a51"),
    "proof168": ("sol/proof_r07_recursive_relative_magnus_frattini_compiler_v168.md", 13829, "0f491cf9a4a43ac165eb70c60d37142053bde47eac965b2497d1d6abaa370cb3"),
    "proof173": ("sol/proof_r07_diagonal_context_cyclic_contraction_v173.md", 11471, "7eed6ad7b00482e245e46226db3fb6985f59c6aa078d7705a92a793593f556f2"),
    "proof184": ("sol/proof_r07_pointed_pair_obstruction_hensel_v184.md", 11018, "7cabb1801b1a844f5f5d63267dda9a4a18e5eeec8a7ec296456e8e60501a88bd"),
    "proof188": ("sol/proof_r07_compressed_diagonal_successor_relation_module_v188.md", 11314, "6512e810011105f83f845e9a41f63ee51fe278371f2cee6cc241e8022a41e822"),
    "proof189": ("sol/proof_r07_ten_occurrence_seven_block_action_bridge_v189.md", 8814, "f3d2fdf9f1fec28c1f308fe7ee74e796cec465fd40dbd73f5e7dc478327da302"),
    "proof190": ("sol/proof_r07_existing_6441_roof_presentation_v190.md", 9793, "562a1ac9db7c1b0a460a5383deff5858de073704f648d524566bd7d18a05e5e1"),
    "task198": ("sol/luna_task_198_r07_seven_context_roof_presentation_v1.md", 11267, "208bdac9fb5a1b257745d74f02878e1a3d033602fa20a5dc57a378a835a80dcc"),
    "task198b": ("sol/luna_task_198b_r07_existing_6441_roof_presentation_repair.md", 4546, "425b9dc64c0a19bac6af6992944fafbba4207ff5569f275fdbc08ee94441d2ae"),
    "task157ee_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945, "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "task157ee_checker_v2": ("search/check_d972_b345_joint_kernel_qstar_closure_v2.py", 5942, "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"),
    "task157ee_checker_v1": ("search/check_d972_b345_joint_kernel_qstar_closure_v1.py", 47661, "9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f"),
    "task172_producer": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918, "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    "task172_checker": ("crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py", 12423, "e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23"),
    "task172_receipt": ("search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json", 45246709, "86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff"),
    "task157ee_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "q3_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "e4_arithmetic": ("search/d972_b345_seedspan_triple4_v1.py", 535219, "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "selftest_fixture": ("search/certs/d972_r07_seven_context_roof_presentation_selftest_v1_20260828.json", 1605, "fb31f6a0be2f2f5b530c6fe99796476ea16edb72fe7ddc192323995f2ae55ce7"),
}

DEPENDENCY_CONE = (
    ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980, "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 88503, "0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce"),
    ("crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py", 12423, "e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23"),
    ("crosscheck/check_d972_r07_positive_common_word_colgen_v1.py", 73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"),
    ("search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json", 45246709, "86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff"),
    ("search/check_d972_b345_joint_kernel_qstar_closure_v2.py", 5942, "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"),
    ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409, "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"),
    ("search/d972_b345_full_d2_dual_correlation_v1.py", 78832, "6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52"),
    ("search/d972_b345_full_d2_dual_correlation_v2.py", 42449, "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"),
    ("search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g", 3912, "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"),
    ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945, "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    ("search/d972_b345_seedspan_triple4_v1.py", 535219, "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    ("search/d972_b345_target6_dual_colgen_v2.py", 444497, "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"),
    ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942, "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"),
    ("search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g", 15929, "1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"),
    ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109, "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    ("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g", 22052, "919e7a9efe7385444c480203dc51525873e770236777dd61e2f6fc1ef22de494"),
    ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306, "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"),
    ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918, "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    ("search/d972_r07_positive_common_word_colgen_gha_driver_v1.g", 12872, "48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"),
    ("search/d972_r07_positive_common_word_colgen_v1.py", 123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    ("sol/audit_r07_all_seven_bridge_checkpoint_v123.md", 5017, "272aabc882599031c4da0472f8f2340043b32571e8e05ecaa58fc5ad1c6a31ac"),
    ("sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md", 4118, "53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee"),
    ("sol/luna_reply_173_r07_all_seven_raw_bridge_inventory_v1.md", 24283, "189a642fc8654f163b0b7964b75043ea393cac31a0b56b84ae0fddf2f73c3695"),
    ("sol/luna_reply_174_r07_target6_context_image_census_v1.md", 13224, "516d15d4ad73e9e2d8e564789e856224c35a30a235e46e87ad857cb20470b49f"),
    ("sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md", 11226, "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"),
    ("sol/luna_task_175_r07_all_seven_raw_bridge_preflight_v1.md", 8584, "5d0d8e006c6a752e5a525b188c9d95ba0c858aa69147432e639fe3e735ffefee"),
    ("sol/luna_task_175b_r07_all_seven_raw_bridge_implementation_repair.md", 5136, "a41f2446fd1c9f0bd60a7189db682784f4e69e24e8958f7c4505cd1eb9741836"),
    ("sol/luna_task_176_r07_all_seven_extension_section_census_v1.md", 7054, "a1778c17c33e42880a6dd0c2480303a13702cb38950cf836a4ca9d8cca6fa332"),
    ("sol/luna_task_179_r07_positive_common_word_colgen_v1.md", 13105, "f97870ec0243b2c399928bcef4f89134f1cd41f15869cc88e3ba7d9dc6956a73"),
    ("sol/proof_pb3_two_relator_presentation_equality_v121.md", 5762, "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"),
    ("sol/proof_pb4_eleven_relator_presentation_equality_v108.md", 6742, "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"),
    ("sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md", 4942, "5f0fffe64b729a8e44643ce86e9d588ef96cbe199ef8ca03741c712c2b162ee8"),
    ("sol/proof_r07_actual_weighted_support_hitting_selector_v143.md", 5253, "aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259"),
    ("sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md", 8545, "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3"),
    ("sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md", 6371, "9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456"),
    ("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md", 7939, "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"),
    ("sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md", 12136, "dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc"),
    ("sol/proof_r07_positive_only_common_word_colgen_v140.md", 10073, "6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b"),
    ("sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md", 4539, "75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67"),
    ("sol/proof_r07_witness_first_fibre_dovetail_selector_v139.md", 8310, "62e2160348db38eca1570b2ca6eb8934b885569f4e8cfb276a91b98c9b983920"),
)


class Reject(RuntimeError):
    pass


class BudgetStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float,
                 limit: int | float):
        super().__init__(f"{phase}:{cap}:{value}:{limit}")
        self.phase, self.cap, self.value, self.limit = phase, cap, value, limit


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_obj(value: Any) -> str:
    return digest(canonical(value))


def require(value: bool, message: str) -> None:
    if value is not True:
        raise Reject(message)


def strict_int(value: Any, label: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, "strict integer:" + label)
    return value


def strict_bool(value: Any, label: str) -> bool:
    require(type(value) is bool, "strict Boolean:" + label)
    return value


def strict_word(value: Any, label: str) -> list[int]:
    require(type(value) is list, "word list:" + label)
    require(all(type(letter) is int and letter in (-2, -1, 1, 2)
                for letter in value), "word letters:" + label)
    return list(value)


class Budget:
    def __init__(self, args: argparse.Namespace):
        self.started = time.monotonic()
        self.limits = {"wall_seconds": float(args.seconds),
            "rss_bytes": int(args.rss_bytes), "q0_states": int(args.q0_states),
            "q0_edges": int(args.q0_edges),
            "presentation_rows": int(args.presentation_rows),
            "gamma_operations": int(args.gamma_operations),
            "dag_nodes": int(args.dag_nodes),
            "serialized_bytes": int(args.serialized_bytes),
            "checkpoint_bytes": int(args.checkpoint_bytes)}
        require(self.limits["wall_seconds"] > 0 and
                all(type(self.limits[name]) is int and self.limits[name] >= 0
                    for name in ("rss_bytes",) + RESOURCE_COUNTERS),
                "checker resource limits")
        self.counters = {name: 0 for name in RESOURCE_COUNTERS}
        self.phase = "initialization"

    @staticmethod
    def rss() -> int:
        try:
            import resource
            value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            return value if sys.platform == "darwin" else value * 1024
        except (ImportError, AttributeError, OSError):
            return 0

    def check(self, phase: str) -> None:
        self.phase = phase
        elapsed, rss = time.monotonic() - self.started, self.rss()
        if elapsed > self.limits["wall_seconds"]:
            raise BudgetStop(phase, "wall_seconds", elapsed,
                             self.limits["wall_seconds"])
        if rss and rss > self.limits["rss_bytes"]:
            raise BudgetStop(phase, "rss_bytes", rss, self.limits["rss_bytes"])

    def bump(self, name: str, amount: int, phase: str) -> None:
        require(name in self.counters and type(amount) is int and amount >= 0,
                "checker budget ABI")
        target = self.counters[name] + amount
        if target > self.limits[name]:
            raise BudgetStop(phase, name, target, self.limits[name])
        self.counters[name] = target
        self.check(phase)

    def preflight(self, name: str, amount: int, phase: str) -> None:
        require(name in self.counters and type(amount) is int and amount >= 0,
                "checker budget preflight ABI")
        target = self.counters[name] + amount
        if target > self.limits[name]:
            raise BudgetStop(phase, name, target, self.limits[name])
        self.check(phase)

    def public(self) -> dict[str, Any]:
        return {"phase": self.phase,
                "elapsed_seconds": time.monotonic() - self.started,
                "limits": dict(self.limits), "counters": dict(self.counters),
                "rss_bytes": self.rss(),
                "process_model": {"single_process": True, "workers": 0,
                                  "aggregate_process_tree_required": False},
                "resumed_from_limits": None}


def read_checked(path: Path, budget: Budget, phase: str) -> bytes:
    require(path.is_file(), "missing:" + path.as_posix())
    raw = path.read_bytes()
    budget.bump("serialized_bytes", len(raw), phase)
    return raw


def pin_file(entry: tuple[str, int, str], budget: Budget) -> bytes:
    rel, size, expected = entry
    raw = read_checked(ROOT / rel, budget, "authenticate:" + rel)
    require(len(raw) == size and digest(raw) == expected, "pin:" + rel)
    return raw


def dependency_cone_manifest() -> dict[str, Any]:
    rows = [{"path": rel, "bytes": size, "sha256": sha}
            for rel, size, sha in DEPENDENCY_CONE]
    require([row["path"] for row in rows] == sorted(row["path"] for row in rows) and
            len({row["path"] for row in rows}) == len(rows),
            "normalized predecessor dependency cone")
    return {"schema": SCHEMA + "/task175-task176-task179-dependency-cone/v1",
            "roots": ["task175_producer", "task175_checker",
                      "task176_producer", "task176_checker",
                      "task179_producer", "task179_checker"],
            "member_count": len(rows), "members": rows,
            "members_sha256": digest_obj(rows)}


def authenticate_sources(budget: Budget) -> dict[str, Any]:
    answer, authenticated = {}, set()
    for name, entry in PINS.items():
        pin_file(entry, budget)
        answer[name] = {"path": entry[0], "bytes": entry[1], "sha256": entry[2]}
        authenticated.add(entry[0])
    for entry in DEPENDENCY_CONE:
        if entry[0] not in authenticated:
            pin_file(entry, budget)
            authenticated.add(entry[0])
    answer["normalized_predecessor_dependency_cone"] = dependency_cone_manifest()
    return answer


def load_module(rel: str, name: str) -> Any:
    path = (ROOT / rel).resolve()
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module:" + rel)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def self_digest(value: dict[str, Any], label: str) -> str:
    body = dict(value)
    claimed = body.pop("self_digest_sha256", None)
    require(type(claimed) is str and claimed == digest_obj(body), label + " digest")
    return claimed


def unpack_payload(value: Any, width: int, count: int,
                   label: str, budget: Budget) -> bytes:
    require(type(value) is dict and set(value) == {
        "codec", "record_width_bytes", "record_count", "raw_bytes",
        "raw_sha256", "compressed_bytes", "compressed_sha256", "data",
        "meaning"}, label + " keys")
    require(value["codec"] == "zlib+base64" and
            strict_int(value["record_width_bytes"], label + " width") == width and
            strict_int(value["record_count"], label + " count") == count and
            strict_int(value["raw_bytes"], label + " raw bytes") == width * count and
            type(value["data"]) is str and type(value["meaning"]) is str,
            label + " metadata")
    compressed = base64.b64decode(value["data"], validate=True)
    budget.bump("serialized_bytes", len(compressed), label + " compressed")
    require(len(compressed) == strict_int(value["compressed_bytes"], label + " compressed bytes") and
            digest(compressed) == value["compressed_sha256"],
            label + " compressed binding")
    raw = zlib.decompress(compressed)
    require(len(raw) == width * count and digest(raw) == value["raw_sha256"],
            label + " raw binding")
    return raw


def authenticate_task176(path_text: str, budget: Budget) \
        -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    path = Path(path_text)
    require(not path.is_absolute() and path.as_posix() == "ci/in/" + TASK176_MEMBER,
            "task176 member path")
    raw = read_checked(ROOT / path, budget, "task176 receipt")
    require(len(raw) == TASK176_BYTES and digest(raw) == TASK176_SHA,
            "task176 identity")
    obj = json.loads(raw)
    require(type(obj) is dict and self_digest(obj, "task176") and
            obj.get("schema") == "d972-r07-all-seven-extension-section-census/v1" and
            obj.get("status") == "COMPLETE" and
            obj.get("terminal") == TASK176_TERMINAL and
            obj.get("coordinates") == COORDINATES, "task176 envelope/coordinates")
    result = obj.get("result")
    require(type(result) is dict, "task176 result")
    extension = result.get("extension")
    require(extension == {"Gamma_order": GAMMA_ORDER, "Q0_order": Q0_ORDER,
                           "exact_sequence": "1->Gamma->G->Q0->1"},
            "task176 extension")
    families = result.get("families")
    require(type(families) is dict and type(families.get("ALL")) is dict,
            "task176 ALL family")
    family = families["ALL"]
    for key in ("A_order", "L_order", "Q0_index_L", "D_order"):
        strict_int(family.get(key), "task176 ALL " + key, 1)
    require(family.get("label") == "ALL" and
            family.get("coordinate_indices") == list(range(10)) and
            family.get("formula") == "|D_S|=|A_S|*[Q0:L_S]" and
            family["A_order"] == extension["Gamma_order"] == GAMMA_ORDER and
            family["L_order"] == 1 and
            family["Q0_index_L"] == extension["Q0_order"] == Q0_ORDER and
            family["D_order"] == family["A_order"] * family["Q0_index_L"] ==
            extension["Gamma_order"] * extension["Q0_order"] == DELTA_ORDER,
            "task176 ALL arithmetic")
    checks = family.get("L_group_checks")
    require(type(checks) is dict and all(strict_bool(checks.get(key), "ALL " + key)
            for key in ("identity", "closure_by_exact_generated_subgroup",
                        "inverse_generators_in_subgroup", "normal_under_q0_x_y")),
            "task176 ALL checks")
    q0 = result.get("Q0_section")
    require(type(q0) is dict and strict_int(q0.get("order"), "task176 Q0 order", 1) == Q0_ORDER and
            type(q0.get("roster_sha256")) is str,
            "task176 Q0 section")
    budget.preflight("q0_states", Q0_ORDER,
                     "task176 known Q0 state reconstruction preflight")
    budget.preflight("q0_edges", 2 * Q0_ORDER,
                     "task176 known Q0 edge reconstruction preflight")
    parent_raw = unpack_payload(q0.get("parent_states_u32le"), 4, Q0_ORDER,
                                "task176 parents", budget)
    letters = unpack_payload(q0.get("parent_letters_u8"), 1, Q0_ORDER,
                             "task176 letters", budget)
    require(parent_raw[:4] == b"\x00\x00\x00\x00" and letters[:1] == b"\x00" and
            all(letter in (1, 2) for letter in letters[1:]),
            "task176 Q0 tree alphabet")
    # Decode every parent independently; each nonroot points strictly backward.
    for index in range(Q0_ORDER):
        if index % 8192 == 0:
            budget.check("task176 parent replay")
        parent = struct.unpack_from("<I", parent_raw, 4 * index)[0]
        require((index == 0 and parent == 0) or
                (index > 0 and 1 <= parent <= index), "task176 parent topology")
    budget.bump("q0_states", Q0_ORDER, "task176 parent replay")
    budget.bump("q0_edges", 2 * Q0_ORDER, "task176 authenticated edge extent")
    manifest_raw = read_checked(ROOT / TASK176_MANIFEST, budget, "task176 manifest")
    manifest = json.loads(manifest_raw)
    expected_manifest = {"artifact_id": TASK176_ARTIFACT,
        "zip_sha256": TASK176_ZIP_SHA, "run": TASK176_RUN,
        "head": TASK176_HEAD, "member": TASK176_MEMBER,
        "member_bytes": TASK176_BYTES, "member_sha256": TASK176_SHA}
    require(manifest == expected_manifest, "task176 staged manifest")
    public = {**expected_manifest, "receipt_path": path.as_posix(),
        "receipt_bytes": len(raw), "receipt_sha256": digest(raw),
        "receipt_self_digest_sha256": obj["self_digest_sha256"],
        "manifest_path": TASK176_MANIFEST, "manifest_bytes": len(manifest_raw),
        "manifest_sha256": digest(manifest_raw), "grade": "CROSS_CHECKED",
        "extension": extension,
        "family_ALL": {key: family[key] for key in
            ("label", "coordinate_indices", "A_order", "L_order",
             "Q0_index_L", "D_order", "formula")},
        "coordinates_sha256": digest_obj(COORDINATES),
        "q0_parent_states_raw_sha256": digest(parent_raw),
        "q0_parent_letters_raw_sha256": digest(letters),
        "q0_roster_sha256": q0.get("roster_sha256")}
    q0_public = {"order": Q0_ORDER, "state_count": Q0_ORDER,
        "edge_count": 2 * Q0_ORDER,
        "parent_states_u32le_sha256": digest(parent_raw),
        "parent_letters_u8_sha256": digest(letters),
        "parent_letter_transition_sha256": digest(parent_raw + letters),
        "discovery": "positive x,y first-seen BFS"}
    return public, q0_public, {"parent_raw": parent_raw, "letters": letters}


def authenticate_task157(budget: Budget) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = pin_file(PINS["task157ee_receipt"], budget)
    obj = json.loads(raw)
    require(obj.get("schema") == "d972-b345-joint-kernel-qstar-closure/v1" and
            obj.get("status") == "B345_JOINT_KERNEL_QSTAR_CLOSED" and
            obj.get("terminal_token") == "B345_JOINT_KERNEL_QSTAR_CLOSED",
            "task157 envelope")
    gamma, q0, qrows = obj.get("gamma"), obj.get("q0_presentation"), obj.get("q0_relations")
    require(type(gamma) is dict and type(q0) is dict and type(qrows) is dict and
            gamma.get("order") == GAMMA_ORDER and gamma.get("edge_count") == 6318 and
            gamma.get("generator_count") == 26 and q0.get("P_order") == 504 and
            q0.get("G9_order") == 2916 and q0.get("Q0_order") == Q0_ORDER and
            q0.get("P_relator_count") == 5 and q0.get("G9_relator_count") == 8 and
            q0.get("complete_relator_count") == 19 and qrows.get("row_count") == 19 and
            qrows.get("relator_image_normal_closure_order") == GAMMA_ORDER,
            "task157 substantive fields")
    public = {"path": PINS["task157ee_receipt"][0],
        "bytes": PINS["task157ee_receipt"][1], "sha256": PINS["task157ee_receipt"][2],
        "grade": "CROSS_CHECKED", "gamma_order": GAMMA_ORDER,
        "gamma_edges": 6318, "gamma_generators": 26, "q0_order": Q0_ORDER,
        "factor_payload_sha256": q0.get("factor_payload_sha256"),
        "complete_relators_sha256": q0.get("complete_relators_sha256"),
        "split_word_sha256": q0.get("split_word_sha256"),
        "q0_defect_normal_closure_order": qrows.get("relator_image_normal_closure_order"),
        "receipt_self_digest": obj.get("self_digest_sha256")}
    return public, obj


def authenticate_task172(budget: Budget) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = pin_file(PINS["task172_receipt"], budget)
    obj = json.loads(raw)
    roster, q3, contexts = obj.get("relation_roster"), obj.get("q3"), obj.get("contexts")
    layers = {"gamma_edge": 6318, "xy_action": 104, "q0_relator": 19}
    rule = ("ri*4+li*2+(1 for orient +1, 2 for orient -1), "
            "frozen 157ee action_relations token order")
    require(obj.get("schema") == "d972-r07-full-e4-orbit-preflight/v7" and
            obj.get("status") == "R07_FULL_E4_ORBIT_PREFLIGHT_READY" and
            obj.get("terminal_token") == "R07_FULL_E4_ORBIT_PREFLIGHT_READY" and
            type(roster) is dict and roster.get("count") == PRESENTATION_ROWS and
            roster.get("layers") == layers and roster.get("expanded_words") is True and
            roster.get("xy_action_ordinal_rule") == rule and
            roster.get("roster_sha256") == TASK172_ROSTER_SHA and
            type(q3) is dict and q3.get("artifact_sha256") == PINS["q3_receipt"][2] and
            q3.get("record_count") == 26 and type(q3.get("record_words_sha256")) is str and
            type(contexts) is dict and contexts.get("count") == 31 and
            contexts.get("aliases") == 46 and type(contexts.get("rows_sha256")) is str,
            "task172 full frozen receipt fields")
    public = {"path": PINS["task172_receipt"][0], "bytes": PINS["task172_receipt"][1],
        "sha256": PINS["task172_receipt"][2], "schema": obj["schema"],
        "status": obj["status"], "terminal": obj["terminal_token"],
        "relation_roster": {"count": roster["count"], "layers": roster["layers"],
            "expanded_words": roster["expanded_words"],
            "xy_action_ordinal_rule": roster["xy_action_ordinal_rule"],
            "roster_sha256": roster["roster_sha256"]},
        "q3": {"artifact_sha256": q3["artifact_sha256"],
               "record_count": q3["record_count"],
               "record_words_sha256": q3["record_words_sha256"]},
        "contexts": {"count": contexts["count"], "aliases": contexts["aliases"],
                     "rows_sha256": contexts["rows_sha256"]}}
    return public, obj


def reduce_word(word: Iterable[int]) -> list[int]:
    answer: list[int] = []
    for letter in word:
        require(type(letter) is int and letter in (-2, -1, 1, 2), "free word letter")
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return answer


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-letter for letter in reversed(word)]


def row_keys(row: dict[str, Any]) -> tuple[set[str], set[str]]:
    layer = row.get("layer")
    if layer == "Gamma_Cayley":
        return ({"layer", "ordinal", "state", "generator", "target_state",
                 "word", "ancestry"},
                {"section_source_word", "record_word", "section_target_word"})
    if layer == "action":
        return ({"layer", "ordinal", "record", "letter", "orientation",
                 "target_state", "word", "ancestry"},
                {"tokens", "record_word", "section_target_word"})
    if layer == "Q0_lift":
        return ({"layer", "ordinal", "target_state", "word", "ancestry"},
                {"q0_relator_word", "section_target_word"})
    raise Reject("unknown row layer")


def validate_row_types(row: Any, index: int) -> None:
    require(type(row) is dict and type(row.get("ancestry")) is dict,
            f"row object:{index}")
    keys, ancestry_keys = row_keys(row)
    require(set(row) == keys and set(row["ancestry"]) == ancestry_keys,
            f"row keys:{index}")
    strict_int(row["ordinal"], f"ordinal:{index}", 1)
    strict_int(row["target_state"], f"target:{index}", 1)
    strict_word(row["word"], f"word:{index}")
    for key, value in row["ancestry"].items():
        strict_word(value, f"ancestry:{index}:{key}")
    if row["layer"] == "Gamma_Cayley":
        strict_int(row["state"], f"state:{index}", 1)
        strict_int(row["generator"], f"generator:{index}", 1)
    elif row["layer"] == "action":
        strict_int(row["record"], f"record:{index}", 1)
        strict_int(row["letter"], f"letter:{index}", 1)
        require(type(row["orientation"]) is int and row["orientation"] in (-1, 1),
                f"orientation:{index}")


def checker_section_word(group: Any, words: Sequence[Sequence[int]],
                         state: int) -> list[int]:
    value: list[int] = []
    for generator in group.section_factors(state):
        value = reduce_word(value + list(words[generator]))
    return value


def frozen_rows(group: Any, words: Sequence[Sequence[int]],
                relators: Sequence[Sequence[int]], budget: Budget) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for state in range(len(group.states)):
        source_section = checker_section_word(group, words, state)
        for generator, source in enumerate(words):
            target = int(group.transitions[state][generator])
            target_section = checker_section_word(group, words, target)
            rows.append({"layer": "Gamma_Cayley",
                "ordinal": state * len(words) + generator + 1,
                "state": state + 1, "generator": generator + 1,
                "target_state": target + 1,
                "word": reduce_word(source_section + list(source) +
                                    inverse_word(target_section)),
                "ancestry": {"section_source_word": source_section,
                    "record_word": list(source),
                    "section_target_word": target_section}})
            budget.bump("presentation_rows", 1, "checker frozen Gamma rows")
            budget.bump("dag_nodes", len(rows[-1]["word"]) + 1,
                        "checker frozen Gamma DAG")
    outer_values = [group.eval([1]), group.eval([2])]
    for record, source_value in enumerate(group.generators):
        for letter, outer in enumerate(outer_values):
            for slot, orientation in enumerate((1, -1), 1):
                if orientation == 1:
                    target_value = group.mul(group.mul(group.inverse(outer), source_value), outer)
                    tokens = [-(letter + 1)] + list(words[record]) + [letter + 1]
                else:
                    target_value = group.mul(group.mul(outer, source_value), group.inverse(outer))
                    tokens = [letter + 1] + list(words[record]) + [-(letter + 1)]
                target = int(group.ids[group.key(target_value)])
                target_section = checker_section_word(group, words, target)
                rows.append({"layer": "action",
                    "ordinal": record * 4 + letter * 2 + slot,
                    "record": record + 1, "letter": letter + 1,
                    "orientation": orientation, "target_state": target + 1,
                    "word": reduce_word(tokens + inverse_word(target_section)),
                    "ancestry": {"tokens": tokens, "record_word": list(words[record]),
                                 "section_target_word": target_section}})
                budget.bump("presentation_rows", 1, "checker frozen action rows")
                budget.bump("dag_nodes", len(rows[-1]["word"]) + 1,
                            "checker frozen action DAG")
    for ordinal, relator in enumerate(relators, 1):
        source = list(relator)
        target = int(group.ids[group.key(group.eval(source))])
        target_section = checker_section_word(group, words, target)
        rows.append({"layer": "Q0_lift", "ordinal": ordinal,
            "target_state": target + 1,
            "word": reduce_word(source + inverse_word(target_section)),
            "ancestry": {"q0_relator_word": source,
                         "section_target_word": target_section}})
        budget.bump("presentation_rows", 1, "checker frozen Q0 rows")
        budget.bump("dag_nodes", len(rows[-1]["word"]) + 1,
                    "checker frozen Q0 DAG")
    require(len(rows) == PRESENTATION_ROWS, "checker 6441 rows")
    return rows


def reverse_greedy(group: Any) -> tuple[list[int], int]:
    selected: list[int] = []
    closure = set(group.closure_ids([]))
    for index in reversed(range(len(group.generators))):
        state = group.ids[group.key(group.generators[index])]
        if state not in closure:
            selected.append(index + 1)
            closure = set(group.closure_ids([
                group.ids[group.key(group.generators[row - 1])]
                for row in selected]))
    return selected, len(closure)


def alternate_sections(group: Any, words: Sequence[Sequence[int]],
                       budget: Budget) -> tuple[list[list[int]], list[int]]:
    identity_id = group.ids[group.key(group.identity)]
    sections: list[list[int] | None] = [None] * len(group.states)
    sections[identity_id] = []
    queue, head = [identity_id], 0
    reversed_indices = list(reversed(range(len(words))))
    while head < len(queue):
        state_id, head = queue[head], head + 1
        source = sections[state_id]
        require(source is not None, "alternate section source")
        for generator in reversed_indices:
            target_value = group.mul(group.states[state_id], group.generators[generator])
            target = group.ids[group.key(target_value)]
            if sections[target] is None:
                sections[target] = reduce_word(source + list(words[generator]))
                queue.append(target)
            budget.bump("gamma_operations", 1, "alternate reversed Gamma BFS")
    require(len(queue) == len(group.states) == GAMMA_ORDER and
            all(row is not None for row in sections), "alternate section coverage")
    return [list(row) for row in sections if row is not None], queue


def semantic_ledger(group: Any, words: Sequence[Sequence[int]],
                    relators: Sequence[Sequence[int]],
                    sections: Sequence[Sequence[int]], budget: Budget) -> list[tuple[Any, ...]]:
    ledger: list[tuple[Any, ...]] = []
    for state in reversed(range(len(group.states))):
        for generator in reversed(range(len(words))):
            target = group.ids[group.key(group.mul(group.states[state],
                                                    group.generators[generator]))]
            row = reduce_word(list(sections[state]) + list(words[generator]) +
                              inverse_word(sections[target]))
            require(group.eval(row) == group.identity, "alternate Gamma identity")
            ledger.append(("Gamma_Cayley", state + 1, generator + 1, target + 1))
            budget.bump("gamma_operations", 1, "alternate Gamma identity")
    outer_values = [group.eval([1]), group.eval([2])]
    for record in reversed(range(len(words))):
        source_value = group.generators[record]
        for letter in reversed(range(2)):
            outer = outer_values[letter]
            for orientation in (-1, 1):
                if orientation == 1:
                    target_value = group.mul(group.mul(group.inverse(outer), source_value), outer)
                    tokens = [-(letter + 1)] + list(words[record]) + [letter + 1]
                else:
                    target_value = group.mul(group.mul(outer, source_value), group.inverse(outer))
                    tokens = [letter + 1] + list(words[record]) + [-(letter + 1)]
                target = group.ids[group.key(target_value)]
                row = reduce_word(tokens + inverse_word(sections[target]))
                require(group.eval(row) == group.identity, "alternate action identity")
                ledger.append(("action", record + 1, letter + 1, orientation, target + 1))
                budget.bump("gamma_operations", 1, "alternate action identity")
    for ordinal in reversed(range(len(relators))):
        target = group.ids[group.key(group.eval(relators[ordinal]))]
        row = reduce_word(list(relators[ordinal]) + inverse_word(sections[target]))
        require(group.eval(row) == group.identity, "alternate Q0 identity")
        ledger.append(("Q0_lift", ordinal + 1, target + 1))
        budget.bump("gamma_operations", 1, "alternate Q0 identity")
    return ledger


def frozen_semantic_ledger(rows: Sequence[dict[str, Any]]) -> set[tuple[Any, ...]]:
    answer: set[tuple[Any, ...]] = set()
    for row in rows:
        if row["layer"] == "Gamma_Cayley":
            answer.add(("Gamma_Cayley", row["state"], row["generator"], row["target_state"]))
        elif row["layer"] == "action":
            answer.add(("action", row["record"], row["letter"],
                        row["orientation"], row["target_state"]))
        else:
            answer.add(("Q0_lift", row["ordinal"], row["target_state"]))
    return answer


def reconstruct_roster(budget: Budget) -> dict[str, Any]:
    # Check-only reservation before any predecessor module/group/roster build.
    # frozen_rows performs the sole live presentation_rows charge.
    budget.preflight("presentation_rows", PRESENTATION_ROWS,
                     "checker presentation_roster_preflight")
    old = load_module(PINS["e4_arithmetic"][0], "c198_old")
    independent = load_module(PINS["task157ee_checker_v1"][0], "c198_task157_checker")
    q3_raw = pin_file(PINS["q3_receipt"], budget)
    q3 = json.loads(q3_raw)
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, _, _ = old.cheap_context_registry(e4)
    words = [list(row["word"]) for row in q3["correction_fibre"]["records"]
             if row.get("word")]
    require(len(words) == 26 and all(strict_word(row, "q3 record") for row in words),
            "26 source records")
    group = independent.JointGroup(old, e3, e4, contexts, words)
    require(len(group.states) == GAMMA_ORDER and len(group.transitions) == GAMMA_ORDER,
            "independent Gamma reconstruction")
    budget.check("independent task157 factor orders start")
    factor, relators = independent.factor_presentation(q3, old)
    budget.check("independent task157 factor orders complete")
    budget.bump("gamma_operations", len(relators) + 2,
                "independent factor presentation accounting")
    require(factor.get("P_order") == factor.get("P_state_count") == 504 and
            factor.get("G9_order") == factor.get("G9_state_count") == 2916 and
            factor.get("Q0_order") == 504 * 2916 == Q0_ORDER and
            factor.get("complete_relator_count") == len(relators) == 19 and
            factor.get("complete_relators_sha256") == digest_obj(relators),
            "independent direct/abstract factor orders")
    rows = frozen_rows(group, words, relators, budget)
    require(all(group.eval(row["word"]) == group.identity for row in rows),
            "frozen rows identities")
    budget.bump("gamma_operations", len(rows), "frozen row identity replay")
    legacy = [[{"Gamma_Cayley": "gamma_edge", "action": "xy_action",
                "Q0_lift": "q0_relator"}[row["layer"]],
               row["ordinal"], row["word"]] for row in rows]
    require(digest_obj(legacy) == TASK172_ROSTER_SHA, "actual task172 roster SHA")
    alt_sections, alt_queue = alternate_sections(group, words, budget)
    alt_ledger = semantic_ledger(group, words, relators, alt_sections, budget)
    require(set(alt_ledger) == frozen_semantic_ledger(rows) and
            len(alt_ledger) == len(rows), "alternate semantic roster")
    selected, selected_order = reverse_greedy(group)
    require(selected_order == GAMMA_ORDER and selected != [],
            "alternate reversed selected generators")
    return {"old": old, "independent": independent, "q3": q3,
            "e3": e3, "e4": e4, "contexts": contexts, "words": words,
            "group": group, "rows": rows, "relators": relators,
            "factor": factor, "alternate_selected": selected,
            "alternate_section_order_sha256": digest_obj(alt_queue),
            "alternate_semantic_sha256": digest_obj(alt_ledger)}


def insert_occurrences(ten: Sequence[Any]) -> list[Any]:
    require(len(ten) == 10, "bridge ten arity")
    return [ten[index] for index in TEN_TO_ELEVEN]


def delete_duplicate(eleven: Sequence[Any]) -> list[Any]:
    require(len(eleven) == 11, "bridge eleven arity")
    return [eleven[index] for index in DELETE_DUPLICATE]


def group_seven(eleven: Sequence[Any]) -> list[list[Any]]:
    require(len(eleven) == 11, "bridge regroup arity")
    return [list(eleven[:3]), list(eleven[3:6]), [eleven[6]], [eleven[7]],
            [eleven[8]], [eleven[9]], [eleven[10]]]


def flatten_seven(seven: Sequence[Sequence[Any]]) -> list[Any]:
    require([len(block) for block in seven] == [3, 3, 1, 1, 1, 1, 1],
            "bridge block arities")
    return [value for block in seven for value in block]


def bridge_runtime(rebuilt: dict[str, Any], budget: Budget) -> dict[str, Any]:
    p176 = load_module(PINS["task176_producer"][0], "c198_task176")
    budget.preflight("gamma_operations", 59_049 * 6,
                     "checker known fine-deletion edge preflight")
    budget.check("checker task176 deletion reconstruction start")
    fine, fine_public = p176.build_fine_deletion(
        rebuilt["e3"], rebuilt["e4"], budget)
    fine_states = strict_int(fine_public.get("source_order"),
                             "fine deletion source order", 1)
    require(fine_states == 59_049 and len(rebuilt["e4"].generators) == 6,
            "checker fine-deletion known extent")
    budget.bump("gamma_operations", fine_states * len(rebuilt["e4"].generators),
                "checker fine-deletion edge reconstruction")
    marked = rebuilt["q3"]["coarse_models"]["Q0"]["marked_permutations"]
    q0_marked = [p176.canonical_packed_permutation(
        rebuilt["old"].perm_from_row(row, 36), 36, "checker Q0 mark")
        for row in marked]
    delete, _ = p176.make_deleter(rebuilt["old"], rebuilt["e3"], rebuilt["e4"],
                                  fine, q0_marked)
    budget.check("checker task176 deletion reconstruction complete")
    return {"p176": p176, "old": rebuilt["old"], "e3": rebuilt["e3"],
            "e4": rebuilt["e4"], "contexts": rebuilt["contexts"],
            "delete": delete}


def bridge_blobs(runtime: dict[str, Any], values: Sequence[Any]) -> list[str]:
    return [runtime["p176"].blob(runtime["old"], value).hex() for value in values]


def bridge_trace(runtime: dict[str, Any], word: Sequence[int], label: str,
                 budget: Budget) -> dict[str, Any]:
    strict_word(list(word), "bridge word")
    ten = list(runtime["p176"].eval_word_coordinates(
        runtime["old"], runtime["e3"], runtime["e4"], runtime["contexts"],
        runtime["delete"], word))
    if runtime.get("selftest_nonsplit") is True and label.startswith("relator:"):
        require(all(runtime["p176"].decode(value, index) == (0, 0)
                    for index, value in enumerate(ten)),
                "checker every toy relator identity in every coordinate")
    eleven = insert_occurrences(ten)
    seven = group_seven(eleven)
    ten_blob, eleven_blob = bridge_blobs(runtime, ten), bridge_blobs(runtime, eleven)
    deleted = bridge_blobs(runtime, delete_duplicate(eleven))
    reinserted = bridge_blobs(runtime, insert_occurrences(delete_duplicate(eleven)))
    flattened = bridge_blobs(runtime, flatten_seven(seven))
    require(eleven_blob[0] == eleven_blob[4] and deleted == ten_blob and
            reinserted == eleven_blob and flattened == eleven_blob,
            "typed bridge inverse:" + label)
    ledger = occurrence_ledger()
    occurrence_values = [eleven_blob[row["ordinal"] - 1] for row in ledger]
    budget.bump("gamma_operations", 1, "checker bridge replay")
    return {"label": label, "word": list(word),
        "word_sha256": digest_obj(list(word)), "ten_sha256": digest_obj(ten_blob),
        "eleven_sha256": digest_obj(eleven_blob),
        "seven_sha256": digest_obj([bridge_blobs(runtime, block) for block in seven]),
        "occurrence_values_sha256": digest_obj(occurrence_values),
        "left_inverse": deleted == ten_blob,
        "image_inverse": reinserted == eleven_blob,
        "regroup_inverse": flattened == eleven_blob}


def replay_bridge(runtime: dict[str, Any], rows: Sequence[dict[str, Any]],
                  budget: Budget) -> tuple[list[dict[str, Any]], list[str], str]:
    marks = [("x", [1]), ("y", [2]), ("x_inv", [-1]), ("y_inv", [-2])]
    marked = [bridge_trace(runtime, word, label, budget) for label, word in marks]
    relator_digests: list[str] = []
    # Deliberately reverse the producer's relator traversal order, then restore
    # canonical source order only for the aggregate digest.
    indexed: list[tuple[int, str]] = []
    for index in reversed(range(len(rows))):
        row = rows[index]
        trace = bridge_trace(runtime, row["word"],
            f"relator:{row['layer']}:{row['ordinal']}", budget)
        indexed.append((index, digest_obj(trace)))
    for _, value in sorted(indexed):
        relator_digests.append(value)
    return marked, relator_digests, digest_obj(relator_digests)


def checker_eval(runtime: dict[str, Any], word: Sequence[int],
                 budget: Budget) -> list[str]:
    source = strict_word(list(word), "checker roof eval word")
    values = runtime["p176"].eval_word_coordinates(
        runtime["old"], runtime["e3"], runtime["e4"], runtime["contexts"],
        runtime["delete"], source)
    require(type(values) is tuple and len(values) == 10,
            "checker roof eval arity")
    budget.bump("gamma_operations", len(values), "checker v188 ABI eval")
    return [runtime["p176"].blob(runtime["old"], value).hex()
            for value in values]


def checker_value(runtime: dict[str, Any], value: Any, label: str) -> list[bytes]:
    require(type(value) is list and len(value) == 10,
            "checker roof value arity:" + label)
    widths = tuple(getattr(runtime["p176"], "COORDINATE_WIDTHS", ()))
    require(len(widths) == 10, "checker roof widths")
    result: list[bytes] = []
    for index, (encoded, width) in enumerate(zip(value, widths)):
        require(type(encoded) is str, f"checker roof hex type:{label}:{index}")
        try:
            raw = bytes.fromhex(encoded)
        except ValueError as exc:
            raise Reject(f"checker roof hex:{label}:{index}") from exc
        require(raw.hex() == encoded and len(raw) == int(width),
                f"checker roof typed width:{label}:{index}")
        result.append(raw)
    return result


def checker_multiply(runtime: dict[str, Any], left: Any, right: Any,
                     budget: Budget) -> list[str]:
    lhs = checker_value(runtime, left, "multiply-left")
    rhs = checker_value(runtime, right, "multiply-right")
    answer = [runtime["p176"].multiply_blob(a, b, index,
              runtime["e3"], runtime["e4"]).hex()
              for index, (a, b) in enumerate(zip(lhs, rhs))]
    budget.bump("gamma_operations", len(answer), "checker v188 ABI multiply")
    return answer


def checker_inverse(runtime: dict[str, Any], value: Any,
                    budget: Budget) -> list[str]:
    rows = checker_value(runtime, value, "inverse")
    answer = [runtime["p176"].inverse_blob(raw, index,
              runtime["e3"], runtime["e4"]).hex()
              for index, raw in enumerate(rows)]
    budget.bump("gamma_operations", len(answer), "checker v188 ABI inverse")
    return answer


def checker_q0_section_word(state: int, parent_raw: bytes,
                            letters: bytes) -> list[int]:
    require(type(state) is int and 0 <= state < Q0_ORDER and
            type(parent_raw) is bytes and len(parent_raw) == 4 * Q0_ORDER and
            type(letters) is bytes and len(letters) == Q0_ORDER,
            "checker Q0 section ABI")
    out: list[int] = []
    while state:
        letter = int(letters[state])
        parent_public = struct.unpack_from("<I", parent_raw, 4 * state)[0]
        require(letter in (1, 2) and 1 <= parent_public <= state,
                "checker Q0 section parent")
        out.append(letter)
        state = parent_public - 1
    out.reverse()
    return out


def checker_source_section(runtime: dict[str, Any], rebuilt: dict[str, Any],
                           q0_private: dict[str, Any], gamma_state_id: int,
                           q0_state_id: int, budget: Budget) -> dict[str, Any]:
    gid = strict_int(gamma_state_id, "checker Gamma section state", 1) - 1
    qid = strict_int(q0_state_id, "checker Q0 section state", 1) - 1
    require(gid < len(rebuilt["group"].states) and qid < Q0_ORDER,
            "checker roof section range")
    gamma_word = checker_section_word(rebuilt["group"], rebuilt["words"], gid)
    q0_word = checker_q0_section_word(qid, q0_private["parent_raw"],
                                      q0_private["letters"])
    source_word = reduce_word(gamma_word + q0_word)
    gamma_value = checker_eval(runtime, gamma_word, budget)
    q0_value = checker_eval(runtime, q0_word, budget)
    value = checker_multiply(runtime, gamma_value, q0_value, budget)
    require(value == checker_eval(runtime, source_word, budget),
            "checker literal source section")
    return {"gamma_state_id": gamma_state_id, "q0_state_id": q0_state_id,
            "gamma_word": gamma_word, "q0_word": q0_word,
            "source_word": source_word, "value": value}


def checker_action(runtime: dict[str, Any], actor_word: Sequence[int], value: Any,
                   budget: Budget) -> list[str]:
    actor_source = strict_word(list(actor_word), "checker action actor")
    actor = checker_eval(runtime, actor_source, budget)
    return checker_multiply(runtime,
        checker_multiply(runtime, actor, value, budget),
        checker_inverse(runtime, actor, budget), budget)


def checker_section_cocycle(runtime: dict[str, Any], left: Sequence[int],
                            right: Sequence[int], product: Sequence[int],
                            budget: Budget) -> list[str]:
    left_word = strict_word(list(left), "checker cocycle left")
    right_word = strict_word(list(right), "checker cocycle right")
    product_word = strict_word(list(product), "checker cocycle product")
    return checker_eval(runtime, reduce_word(
        left_word + right_word + inverse_word(product_word)), budget)


def checker_consumer_abi(runtime: dict[str, Any], rebuilt: dict[str, Any],
                         q0_private: dict[str, Any], rows_sha256: str,
                         budget: Budget) -> dict[str, Any]:
    x = checker_eval(runtime, [1], budget)
    y = checker_eval(runtime, [2], budget)
    x_inverse = checker_inverse(runtime, x, budget)
    xy = checker_multiply(runtime, x, y, budget)
    source = checker_source_section(runtime, rebuilt, q0_private, 2, 2, budget)
    action = checker_action(runtime, [1], y, budget)
    cocycle = checker_section_cocycle(runtime, [1], [2], [1, 2], budget)
    require(x_inverse == checker_eval(runtime, [-1], budget) and
            xy == checker_eval(runtime, [1, 2], budget) and
            action == checker_eval(runtime, [1, 2, -1], budget) and
            cocycle == checker_eval(runtime, [], budget),
            "checker v188 ABI canaries")
    return {"schema": "d972-r07-v188-roof-consumer-action-abi/v1",
        "module": "search/d972_r07_seven_context_roof_presentation_v1.py",
        "runtime_constructor": "load_runtime",
        "registry_callable": "v188_consumer_action_abi",
        "entry_points": {
            "eval": {"callable": "roof_eval", "arguments": ["runtime", "word"]},
            "multiply": {"callable": "roof_multiply",
                         "arguments": ["runtime", "left", "right"]},
            "inverse": {"callable": "roof_inverse",
                        "arguments": ["runtime", "value"]},
            "source_section": {"callable": "roof_source_section",
                               "arguments": ["runtime", "gamma_state_id",
                                             "q0_state_id"]},
            "action": {"callable": "roof_action",
                       "arguments": ["runtime", "actor_word", "value"]},
            "section_cocycle": {"callable": "roof_section_cocycle",
                                "arguments": ["runtime", "left_section_word",
                                              "right_section_word",
                                              "product_section_word"]}},
        "encoding": {"source_word": "strict signed F2 list",
                     "roof_value": "ten lowercase hex typed coordinate blobs",
                     "state_ids": "one-based Gamma and Q0 ids"},
        "semantics": {"multiplication": "left_then_right",
                      "action": "actor*value*actor_inverse",
                      "section_cocycle": "s_left*s_right*s_product_inverse"},
        "coordinate_widths": list(runtime["p176"].COORDINATE_WIDTHS),
        "coordinate_ledger_sha256": digest_obj(COORDINATES),
        "relator_rows_sha256": rows_sha256,
        "context_maps": None,
        "joint_coordinate_image": None,
        "canaries": {"x": {"word": [1], "value": x},
                     "y": {"word": [2], "value": y},
                     "x_inverse": {"word": [-1], "value": x_inverse},
                     "xy": {"word": [1, 2], "value": xy},
                     "source_2_2": source,
                     "x_action_y": {"actor_word": [1], "input": y,
                                    "value": action},
                      "xy_section_cocycle": {"left": [1], "right": [2],
                         "product": [1, 2], "value": cocycle},
                      "nonsplit_y_y_section_cocycle": None}}


def chunk_seals(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    answer = []
    for start in range(0, len(rows), 1024):
        part = list(rows[start:start + 1024])
        answer.append({"start": start, "end": start + len(part),
                       "sealed": len(part) > 0, "prefix_complete": True,
                       "sha256": digest_obj(part)})
    return answer


def normal_closure(group: Any, seeds: Sequence[int], budget: Budget) -> tuple[int, list[int]]:
    current = set(group.closure_ids(list(seeds)))
    rounds = [len(current)]
    outers = [group.eval([1]), group.eval([2])]
    while True:
        additions: set[int] = set()
        for outer in reversed(outers):
            inverse = group.inverse(outer)
            for state_id in reversed(sorted(current)):
                state = group.states[state_id]
                additions.add(group.ids[group.key(group.mul(group.mul(outer, state), inverse))])
                additions.add(group.ids[group.key(group.mul(group.mul(inverse, state), outer))])
                budget.bump("gamma_operations", 2, "checker normal closure")
        enlarged = set(group.closure_ids(sorted(current | additions, reverse=True)))
        if enlarged == current:
            break
        current = enlarged
        rounds.append(len(current))
    return len(current), rounds


def expected_input_binding(task176: dict[str, Any], task157: dict[str, Any],
                           task172: dict[str, Any], sources: dict[str, Any]) -> dict[str, Any]:
    return {"task176_receipt_sha256": task176["receipt_sha256"],
        "task176_manifest_sha256": task176["manifest_sha256"],
        "task157ee_receipt_sha256": task157["sha256"],
        "task172_receipt_sha256": task172["sha256"],
        "task172_roster_sha256": task172["relation_roster"]["roster_sha256"],
        "task179_source_sha256": sources["task179_producer"]["sha256"],
        "predecessor_dependency_cone_sha256":
            sources["normalized_predecessor_dependency_cone"]["members_sha256"],
        "proof145_sha256": sources["proof145"]["sha256"],
        "proof168_sha256": sources["proof168"]["sha256"],
        "proof173_sha256": sources["proof173"]["sha256"],
        "proof184_sha256": sources["proof184"]["sha256"],
        "proof188_sha256": sources["proof188"]["sha256"],
        "proof189_sha256": sources["proof189"]["sha256"],
        "proof190_sha256": sources["proof190"]["sha256"]}


CHECKPOINT_KEYS = {"schema", "sealed", "stage", "cursor", "bridge_cursor",
    "rows", "rows_sha256", "bridge_digests", "bridge_replay_sha256", "chunks", "dag_nodes",
    "input_binding", "q0_transition_sha256", "selected_gamma_records",
    "task172_roster_sha256", "total_rows", "limits", "counters", "resumed_from",
    "seal_sha256"}
RESUMED_FROM_KEYS = {"path", "bytes", "sha256", "seal_sha256", "cursor",
    "bridge_cursor", "manifest_path", "manifest_bytes", "manifest_sha256",
    "manifest_self_digest_sha256"}
RESUME_MANIFEST_KEYS = {"schema", "checkpoint_path", "checkpoint_bytes",
    "checkpoint_sha256", "checkpoint_seal_sha256", "cursor", "bridge_cursor",
    "self_digest_sha256"}


def validate_checkpoint(checkpoint: Any, rebuilt_rows: Sequence[dict[str, Any]],
                        expected_binding: dict[str, Any], q0_digest: str,
                        budget: Budget) -> None:
    require(type(checkpoint) is dict and set(checkpoint) == CHECKPOINT_KEYS,
            "checkpoint keys")
    body = dict(checkpoint)
    seal = body.pop("seal_sha256", None)
    require(type(seal) is str and seal == digest_obj(body), "checkpoint seal")
    require(checkpoint["schema"] == CHECKPOINT_SCHEMA and
            checkpoint["sealed"] is True and
            checkpoint["stage"] in ("presentation", "bridge_replay"),
            "checkpoint envelope")
    cursor = strict_int(checkpoint["cursor"], "checkpoint cursor")
    bridge_cursor = strict_int(checkpoint["bridge_cursor"], "checkpoint bridge cursor")
    rows = checkpoint["rows"]
    require(strict_int(checkpoint["total_rows"], "checkpoint total rows") ==
            PRESENTATION_ROWS and
            type(rows) is list and cursor == len(rows) <= PRESENTATION_ROWS and
            0 <= bridge_cursor <= cursor and rows == list(rebuilt_rows[:cursor]) and
            checkpoint["rows_sha256"] == digest_obj(rows) and
            checkpoint["chunks"] == chunk_seals(rows) and
            strict_int(checkpoint["dag_nodes"], "checkpoint DAG") ==
            sum(len(row["word"]) + 1 for row in rows), "checkpoint full prefix replay")
    require((checkpoint["stage"] == "presentation" and
             cursor < PRESENTATION_ROWS and bridge_cursor == 0) or
            (checkpoint["stage"] == "bridge_replay" and
             cursor == PRESENTATION_ROWS), "checkpoint stage/cursors")
    require(checkpoint["input_binding"] == expected_binding and
            checkpoint["q0_transition_sha256"] == q0_digest and
            checkpoint["task172_roster_sha256"] == TASK172_ROSTER_SHA and
            type(checkpoint["selected_gamma_records"]) is list and
            all(type(row) is int and row >= 1 for row in checkpoint["selected_gamma_records"]),
            "checkpoint authenticated state")
    limits, counters = checkpoint["limits"], checkpoint["counters"]
    require(type(limits) is dict and
            set(limits) == {"wall_seconds", "rss_bytes", *RESOURCE_COUNTERS} and
            type(counters) is dict and set(counters) == set(RESOURCE_COUNTERS) and
            type(limits["wall_seconds"]) in (int, float) and limits["wall_seconds"] > 0 and
            type(limits["rss_bytes"]) is int and limits["rss_bytes"] >= 0,
            "checkpoint resources")
    for name in RESOURCE_COUNTERS:
        require(type(limits[name]) is int and limits[name] >= 0 and
                type(counters[name]) is int and 0 <= counters[name] <= limits[name],
                "checkpoint resource:" + name)
    bridge_digests = checkpoint["bridge_digests"]
    require(type(bridge_digests) is list and len(bridge_digests) == bridge_cursor and
            all(type(row) is str for row in bridge_digests) and
            checkpoint["bridge_replay_sha256"] == digest_obj(bridge_digests),
            "checkpoint bridge digest list")
    if checkpoint["resumed_from"] is not None:
        prior = checkpoint["resumed_from"]
        require(type(prior) is dict and set(prior) == RESUMED_FROM_KEYS and
                type(prior["path"]) is str and prior["path"].startswith("ci/in/") and
                type(prior["manifest_path"]) is str and
                prior["manifest_path"].startswith("ci/in/") and
                all(type(prior[name]) is str for name in
                    ("sha256", "seal_sha256", "manifest_sha256",
                     "manifest_self_digest_sha256")) and
                all(type(prior[name]) is int and prior[name] >= 0 for name in
                    ("bytes", "cursor", "bridge_cursor", "manifest_bytes")) and
                prior["bytes"] > 0 and prior["manifest_bytes"] > 0 and
                0 <= prior["bridge_cursor"] <= prior["cursor"] <= PRESENTATION_ROWS,
                "checkpoint resumed-from shape")
    budget.bump("checkpoint_bytes", len(canonical(checkpoint)),
                "checker checkpoint replay")


def forward_greedy(group: Any) -> tuple[list[int], int]:
    selected: list[int] = []
    closure = set(group.closure_ids([]))
    for index, generator in enumerate(group.generators):
        state = group.ids[group.key(generator)]
        if state not in closure:
            selected.append(index + 1)
            closure = set(group.closure_ids([
                group.ids[group.key(group.generators[row - 1])]
                for row in selected]))
    return selected, len(closure)


def validate_chunks(rows: Sequence[dict[str, Any]], chunks: Any) -> None:
    require(type(chunks) is list and chunks == chunk_seals(rows), "presentation chunks")
    cursor = 0
    for chunk in chunks:
        require(type(chunk) is dict and set(chunk) ==
                {"start", "end", "sealed", "prefix_complete", "sha256"} and
                type(chunk["start"]) is int and type(chunk["end"]) is int and
                chunk["start"] == cursor and chunk["end"] > cursor and
                strict_bool(chunk["sealed"], "chunk sealed") and
                strict_bool(chunk["prefix_complete"], "chunk prefix"),
                "chunk record")
        cursor = chunk["end"]
    require(cursor == len(rows), "chunk coverage")


def validate_resource(value: Any, presentation: dict[str, Any]) -> None:
    require(type(value) is dict and set(value) == {"phase", "elapsed_seconds",
            "limits", "counters", "rss_bytes", "process_model",
            "resumed_from_limits"}, "production resource keys")
    require(type(value["phase"]) is str and
            type(value["elapsed_seconds"]) in (int, float) and
            value["elapsed_seconds"] >= 0 and type(value["rss_bytes"]) is int and
            value["rss_bytes"] >= 0 and value["process_model"] == {
                "single_process": True, "workers": 0,
                "aggregate_process_tree_required": False}, "production resource values")
    limits, counters = value["limits"], value["counters"]
    require(type(limits) is dict and
            set(limits) == {"wall_seconds", "rss_bytes", *RESOURCE_COUNTERS} and
            type(counters) is dict and set(counters) == set(RESOURCE_COUNTERS) and
            type(limits["wall_seconds"]) in (int, float) and limits["wall_seconds"] > 0 and
            type(limits["rss_bytes"]) is int and limits["rss_bytes"] >= 0,
            "production resource maps")
    for name in RESOURCE_COUNTERS:
        require(type(limits[name]) is int and limits[name] >= 0 and
                type(counters[name]) is int and 0 <= counters[name] <= limits[name],
                "production resource counter:" + name)
    require(counters["q0_states"] == Q0_ORDER and
            counters["q0_edges"] == 2 * Q0_ORDER and
            counters["presentation_rows"] == PRESENTATION_ROWS and
             counters["dag_nodes"] ==
             sum(len(row["word"]) + 1 for row in presentation["rows"]) and
             counters["serialized_bytes"] > TASK176_BYTES and
             counters["checkpoint_bytes"] > 0 and
             counters["gamma_operations"] >= PRESENTATION_ROWS,
            "production total resource accounting")
    require(value["rss_bytes"] <= limits["rss_bytes"] or value["rss_bytes"] == 0,
            "production RSS cap")
    require(value["resumed_from_limits"] is None or
            type(value["resumed_from_limits"]) is dict,
            "production resumed limits")


def validate_normal_proof(presentation: dict[str, Any], rebuilt: dict[str, Any],
                          task176: dict[str, Any], task157: dict[str, Any],
                          budget: Budget) -> list[int]:
    group, relators = rebuilt["group"], rebuilt["relators"]
    selected, selected_order = forward_greedy(group)
    all_ids = [group.ids[group.key(value)] for value in group.generators]
    all_order = len(group.closure_ids(all_ids))
    defects = [group.ids[group.key(group.eval(relator))] for relator in relators]
    defect_order, defect_rounds = normal_closure(group, defects, budget)
    p_abstract = strict_int(rebuilt["factor"].get("P_order"), "checker P abstract", 1)
    p_direct = strict_int(rebuilt["factor"].get("P_state_count"), "checker P direct", 1)
    g9_abstract = strict_int(rebuilt["factor"].get("G9_order"), "checker G9 abstract", 1)
    g9_direct = strict_int(rebuilt["factor"].get("G9_state_count"), "checker G9 direct", 1)
    q0_upper, q0_image = p_abstract * g9_abstract, p_direct * g9_direct
    require(p_abstract == p_direct and g9_abstract == g9_direct and
            q0_upper == q0_image == Q0_ORDER,
            "independently executed factor order equality")
    qproof = {"method": "producer-owned SymPy factor orders plus direct marked-permutation enumeration",
        "factor_payload_sha256": rebuilt["factor"].get("factor_payload_sha256"),
        "P_abstract_presentation_order": p_abstract,
        "P_direct_image_order": p_direct,
        "G9_abstract_presentation_order": g9_abstract,
        "G9_direct_image_order": g9_direct,
        "cross_commutator_count": 4, "marked_splitting_equation_count": 2,
        "complete_relator_count": 19,
        "complete_relators_sha256": digest_obj(relators),
        "Q0_presentation_order_upper_bound": q0_upper,
        "Q0_marked_image_order": q0_image}
    require(task157["factor_payload_sha256"] == qproof["factor_payload_sha256"] and
            task157["complete_relators_sha256"] == qproof["complete_relators_sha256"],
            "task157 factor digest bridge")
    expected = {"theorem": "v190 Cayley--action--lift order bound",
        "selected_gamma_records": selected,
        "selected_gamma_closure_order": selected_order,
        "all_record_generator_closure_order": all_order,
        "Gamma_cayley_state_count": len(group.states),
        "Gamma_cayley_edge_count": 6318,
        "marked_action_loop_count": 104, "Q0_lift_count": 19,
        "Q0_order_proof": qproof,
        "Q0_defect_normal_closure_order": defect_order,
        "Q0_defect_normal_closure_rounds": defect_rounds,
        "presentation_quotient_order_upper_bound": len(group.states) * Q0_ORDER,
        "surjective_marked_image_order": task176["family_ALL"]["D_order"],
        "upper_bound_equals_image_order": True, "normal_closure_exact": True}
    actual = presentation.get("normal_generation_proof")
    require(actual == expected, "independent v190 normal/order proof")
    require(type(actual["upper_bound_equals_image_order"]) is bool and
            type(actual["normal_closure_exact"]) is bool and
            actual["upper_bound_equals_image_order"] is True and
            actual["normal_closure_exact"] is True and
            selected_order == all_order == defect_order == GAMMA_ORDER and
            len(group.states) * Q0_ORDER == task176["family_ALL"]["D_order"],
            "computed normal-generation equality")
    return selected


def validate_staged_resume_identity(prior: Any, resume_path: str | None,
                                    manifest_path: str | None,
                                    total_rows: int, budget: Budget,
                                    allow_selftest_output: bool = False) -> dict[str, Any]:
    require(type(prior) is dict and set(prior) == RESUMED_FROM_KEYS,
            "resumed-from exact keys")
    roots = ("ci/in/", "ci/out/d972_r07_seven_context_roof_presentation_selftest.") \
        if allow_selftest_output else ("ci/in/",)
    require(type(resume_path) is str and type(manifest_path) is str and
            prior["path"] == Path(resume_path).as_posix() and
            prior["manifest_path"] == Path(manifest_path).as_posix() and
            any(prior["path"].startswith(root) for root in roots) and
            any(prior["manifest_path"].startswith(root) for root in roots),
            "resumed-from staged paths")
    checkpoint_raw = read_checked(ROOT / prior["path"], budget,
                                  "checker staged resume checkpoint")
    manifest_raw = read_checked(ROOT / prior["manifest_path"], budget,
                                "checker staged resume manifest")
    checkpoint = json.loads(checkpoint_raw)
    manifest = json.loads(manifest_raw)
    require(checkpoint_raw == canonical(checkpoint) and
            manifest_raw == canonical(manifest) and
            type(checkpoint) is dict and set(checkpoint) == CHECKPOINT_KEYS and
            type(manifest) is dict and set(manifest) == RESUME_MANIFEST_KEYS and
            manifest["schema"] == RESUME_MANIFEST_SCHEMA,
            "staged resume canonical envelopes")
    body = dict(checkpoint)
    seal = body.pop("seal_sha256", None)
    require(checkpoint["schema"] == CHECKPOINT_SCHEMA and seal == digest_obj(body) and
            checkpoint["total_rows"] == total_rows and
            prior == {"path": prior["path"], "bytes": len(checkpoint_raw),
                "sha256": digest(checkpoint_raw), "seal_sha256": seal,
                "cursor": checkpoint["cursor"],
                "bridge_cursor": checkpoint["bridge_cursor"],
                "manifest_path": prior["manifest_path"],
                "manifest_bytes": len(manifest_raw),
                "manifest_sha256": digest(manifest_raw),
                "manifest_self_digest_sha256": self_digest(manifest, "resume manifest")} and
            manifest["checkpoint_path"] == prior["path"] and
            manifest["checkpoint_bytes"] == len(checkpoint_raw) and
            manifest["checkpoint_sha256"] == digest(checkpoint_raw) and
            manifest["checkpoint_seal_sha256"] == seal and
            manifest["cursor"] == checkpoint["cursor"] and
            manifest["bridge_cursor"] == checkpoint["bridge_cursor"],
            "staged resume full identity binding")
    return checkpoint


def validate_resume_summary(resume: Any, presentation: dict[str, Any],
                            binding: dict[str, Any], q0_digest: str,
                            selected: list[int], args: argparse.Namespace,
                            budget: Budget) -> None:
    keys = {"schema", "sealed", "cursor", "bridge_cursor", "rows_sha256",
        "bridge_digests", "bridge_replay_sha256", "chunks_sha256", "input_binding",
        "q0_transition_sha256", "selected_gamma_records",
        "task172_roster_sha256", "full_checkpoint_seal_sha256",
        "full_checkpoint_stage", "full_checkpoint_total_rows", "full_checkpoint_dag_nodes",
        "full_checkpoint_limits", "full_checkpoint_counters", "resumed_from"}
    require(type(resume) is dict and set(resume) == keys and
            resume["schema"] == CHECKPOINT_SCHEMA and resume["sealed"] is True and
            strict_int(resume["cursor"], "resume cursor") == PRESENTATION_ROWS and
            strict_int(resume["bridge_cursor"], "resume bridge cursor") == PRESENTATION_ROWS and
            resume["rows_sha256"] == presentation["rows_sha256"] and
            type(resume["bridge_digests"]) is list and
            len(resume["bridge_digests"]) == PRESENTATION_ROWS and
            resume["bridge_replay_sha256"] == digest_obj(resume["bridge_digests"]) and
            resume["chunks_sha256"] == digest_obj(presentation["chunks"]) and
            resume["input_binding"] == binding and
            resume["q0_transition_sha256"] == q0_digest and
            resume["selected_gamma_records"] == selected and
            resume["task172_roster_sha256"] == TASK172_ROSTER_SHA and
            resume["full_checkpoint_stage"] == "bridge_replay" and
            resume["full_checkpoint_total_rows"] == PRESENTATION_ROWS and
            resume["full_checkpoint_dag_nodes"] ==
            sum(len(row["word"]) + 1 for row in presentation["rows"]),
            "complete resume summary")
    body = {"schema": CHECKPOINT_SCHEMA, "sealed": True,
        "stage": resume["full_checkpoint_stage"], "cursor": resume["cursor"],
        "bridge_cursor": resume["bridge_cursor"], "rows": presentation["rows"],
        "rows_sha256": resume["rows_sha256"],
        "bridge_digests": resume["bridge_digests"],
        "bridge_replay_sha256": resume["bridge_replay_sha256"],
        "chunks": presentation["chunks"], "dag_nodes": resume["full_checkpoint_dag_nodes"],
        "input_binding": binding, "q0_transition_sha256": q0_digest,
        "selected_gamma_records": selected,
        "task172_roster_sha256": TASK172_ROSTER_SHA,
        "total_rows": resume["full_checkpoint_total_rows"],
        "limits": resume["full_checkpoint_limits"],
        "counters": resume["full_checkpoint_counters"],
        "resumed_from": resume["resumed_from"]}
    require(resume["full_checkpoint_seal_sha256"] == digest_obj(body),
            "reconstructed full checkpoint seal")
    sealed_checkpoint = dict(body)
    sealed_checkpoint["seal_sha256"] = resume["full_checkpoint_seal_sha256"]
    require(type(body["limits"]) is dict and
            set(body["limits"]) == {"wall_seconds", "rss_bytes", *RESOURCE_COUNTERS} and
            type(body["counters"]) is dict and set(body["counters"]) == set(RESOURCE_COUNTERS) and
            type(body["limits"]["wall_seconds"]) in (int, float) and
            body["limits"]["wall_seconds"] > 0 and
            type(body["limits"]["rss_bytes"]) is int and
            body["limits"]["rss_bytes"] >= 0,
            "resume full resources")
    for name in RESOURCE_COUNTERS:
        require(type(body["limits"][name]) is int and body["limits"][name] >= 0 and
                type(body["counters"][name]) is int and
                0 <= body["counters"][name] <= body["limits"][name],
                "resume counter:" + name)
    require(body["counters"]["q0_states"] == Q0_ORDER and
            body["counters"]["q0_edges"] == 2 * Q0_ORDER and
             body["counters"]["presentation_rows"] == PRESENTATION_ROWS and
             body["counters"]["dag_nodes"] == body["dag_nodes"] and
             body["counters"]["checkpoint_bytes"] >=
             len(canonical(sealed_checkpoint)) and
             body["counters"]["gamma_operations"] >= PRESENTATION_ROWS,
            "resume complete counters")
    if resume["resumed_from"] is not None:
        prior_checkpoint = validate_staged_resume_identity(
            resume["resumed_from"], args.resume, args.resume_manifest,
            PRESENTATION_ROWS, budget)
        validate_checkpoint(prior_checkpoint, presentation["rows"], binding,
                            q0_digest, budget)
        require(prior_checkpoint["bridge_digests"] ==
                resume["bridge_digests"][:prior_checkpoint["bridge_cursor"]],
                "staged resume independently replayed bridge prefix")
    else:
        require(args.resume is None and args.resume_manifest is None,
                "unexpected staged resume arguments")


def validate_complete(rec: dict[str, Any], args: argparse.Namespace,
                      budget: Budget, sources: dict[str, Any]) -> None:
    top = {"schema", "status", "terminal", "input", "bridge", "Q0", "Gamma",
        "D_all", "Delta0", "evaluator", "resume", "direct_Delta_states_enumerated",
        "million_row_Q0_Schreier_stream", "cofinal_lift", "fake", "Ihara_witness",
        "resource", "self_digest_sha256"}
    require(set(rec) == top and rec["schema"] == SCHEMA and rec["status"] == "COMPLETE" and
            rec["terminal"] == ISO and rec["cofinal_lift"] is False and
            rec["fake"] is False and rec["Ihara_witness"] is False,
            "complete receipt envelope")
    self_digest(rec, "task198 receipt")
    task176, q0_public, q0_private = authenticate_task176(
        args.task176_receipt, budget)
    task157, _ = authenticate_task157(budget)
    task172, _ = authenticate_task172(budget)
    expected_input = {"task176": task176, "task157ee": task157,
        "task172": task172, "task179": sources["task179_producer"],
        "sources": sources}
    require(rec["input"] == expected_input, "complete input bindings")
    binding = expected_input_binding(task176, task157, task172, sources)
    rebuilt = reconstruct_roster(budget)
    rows = rec["Delta0"]["presentation"].get("rows")
    require(type(rows) is list and len(rows) == PRESENTATION_ROWS,
            "complete row list")
    for index, row in enumerate(rows):
        validate_row_types(row, index)
    require(rows == rebuilt["rows"], "exact independent 6441 records")
    presentation = rec["Delta0"]["presentation"]
    expected_presentation_keys = {"row_count", "layer_counts", "rows", "rows_sha256",
        "task172_legacy_rows_sha256", "chunks", "resume_cursor",
        "normal_generation", "normal_closure_exact", "normal_generation_proof",
        "source_word_encoding"}
    require(set(presentation) == expected_presentation_keys and
            strict_int(presentation["row_count"], "row count") == PRESENTATION_ROWS and
            presentation["layer_counts"] == {"Gamma_Cayley": 6318,
                "action": 104, "Q0_lift": 19} and
            presentation["rows_sha256"] == digest_obj(rows) and
            presentation["task172_legacy_rows_sha256"] == TASK172_ROSTER_SHA and
            strict_int(presentation["resume_cursor"], "presentation cursor") == PRESENTATION_ROWS and
            strict_bool(presentation["normal_generation"], "normal generation") and
            strict_bool(presentation["normal_closure_exact"], "normal exact") and
            presentation["source_word_encoding"] ==
            "literal strict signed F2 words; empty Cayley tree loops retained" and
            any(row["word"] == [] for row in rows), "lossless presentation metadata")
    validate_chunks(rows, presentation["chunks"])
    selected = validate_normal_proof(presentation, rebuilt, task176, task157, budget)
    require(rec["Gamma"] == {"order": GAMMA_ORDER,
            "cayley_state_count": GAMMA_ORDER,
            "selected_record_generators": selected}, "Gamma receipt")
    require(rec["D_all"] == {"order": DELTA_ORDER,
            "order_source": "task176 result.families.ALL.D_order",
            "materialized": False} and
            rec["Delta0"]["order"] == DELTA_ORDER and
            rec["Delta0"]["marked_generators"] == {"x": [1], "y": [2]} and
            rec["Delta0"]["normal_closure_exact"] is True and
            set(rec["Delta0"]) == {"order", "marked_generators", "presentation",
                                      "normal_closure_exact"}, "D/Delta receipt")
    require(rec["Q0"] == q0_public, "independent Q0 payload replay")
    runtime = bridge_runtime(rebuilt, budget)
    marked, relator_digests, relator_bridge_digest = replay_bridge(runtime, rows, budget)
    ledger = occurrence_ledger()
    symbolic_ten = [{"typed_coordinate": index, "type": COORDINATES[index]["type"],
                     "context_id": COORDINATES[index]["context_id"]}
                    for index in range(10)]
    symbolic_eleven = insert_occurrences(symbolic_ten)
    cardinality = {"typed_domain_arity": 10, "occurrence_arity": 11,
        "block_arity": [3, 3, 1, 1, 1, 1, 1],
        "delete_after_insert": delete_duplicate(symbolic_eleven) == symbolic_ten,
        "insert_after_delete_on_image":
            insert_occurrences(delete_duplicate(symbolic_eleven)) == symbolic_eleven,
        "flatten_after_regroup": flatten_seven(group_seven(symbolic_eleven)) == symbolic_eleven}
    expected_bridge = {"branch": ISO, "ten_to_eleven": list(TEN_TO_ELEVEN),
        "eleven_delete_duplicate": list(DELETE_DUPLICATE),
        "seven_blocks": [list(block) for block in SEVEN_BLOCKS],
        "occurrence_ledger": ledger,
        "occurrence_ledger_sha256": digest_obj(ledger),
        "typed_coordinate_ledger_sha256": digest_obj(COORDINATES),
        "marked_replay": marked, "marked_replay_count": 4,
        "marked_inverse_count": sum(row["left_inverse"] and row["image_inverse"] and
                                     row["regroup_inverse"] for row in marked),
        "order_computation": {"ten_image_order": DELTA_ORDER,
            "seven_image_order": DELTA_ORDER, "kernel_order": 1,
            "cardinality_transfer": cardinality},
        "kernel_order": 1, "image_order": DELTA_ORDER,
        "inverse_algorithm": {
            "forward": "insert ten[0] at H2/2, regroup 3+3+1+1+1+1+1",
            "backward": "flatten, delete H2/2; retain typed E3-C21/E4-C21"},
        "relator_replay": {"count": PRESENTATION_ROWS,
            "digest_sha256": relator_bridge_digest,
            "all_left_and_right_inverses": True}}
    require(rec["bridge"] == expected_bridge and
            type(rec["bridge"]["relator_replay"]["all_left_and_right_inverses"]) is bool,
            "full typed bridge replay")
    evaluator = checker_consumer_abi(
        runtime, rebuilt, q0_private, presentation["rows_sha256"], budget)
    require(rec["evaluator"] == evaluator, "independent executable evaluator ABI")
    validate_resume_summary(rec["resume"], presentation, binding,
                            q0_public["parent_letter_transition_sha256"], selected,
                            args, budget)
    require(rec["resume"]["bridge_replay_sha256"] == relator_bridge_digest,
            "resume bridge prefix replay")
    require(rec["resume"]["bridge_digests"] == relator_digests,
            "resume exact per-relator bridge digest replay")
    validate_resource(rec["resource"], presentation)
    require(rec["direct_Delta_states_enumerated"] == 0 and
            rec["million_row_Q0_Schreier_stream"] == "SUPERSEDED_NOT_USED",
            "forbidden materialization")


def validate_terminal_envelope(rec: dict[str, Any], args: argparse.Namespace,
                               budget: Budget, sources: dict[str, Any]) -> str:
    keys = {"schema", "status", "terminal", "reason", "result", "resource",
            "resource_terminal", "checkpoint", "checkpoint_manifest",
            "checkpoint_unavailable_reason",
            "cofinal_lift", "fake", "Ihara_witness", "self_digest_sha256"}
    require(type(rec) is dict and set(rec) == keys and rec["schema"] == SCHEMA and
            rec["status"] == rec["terminal"] and
            rec["terminal"] in (UNKNOWN_INPUT, UNKNOWN_RESOURCE) and
            type(rec["reason"]) is str and bool(rec["reason"]) and
            rec["result"] is None and rec["cofinal_lift"] is False and
            rec["fake"] is False and rec["Ihara_witness"] is False,
            "nonpositive terminal envelope")
    self_digest(rec, "terminal receipt")
    if rec["terminal"] == UNKNOWN_INPUT:
        require(rec["resource"] is None and rec["resource_terminal"] is None and
                rec["checkpoint"] is None and rec["checkpoint_manifest"] is None and
                rec["checkpoint_unavailable_reason"] is None,
                "UNKNOWN_INPUT fields")
        return UNKNOWN_INPUT
    terminal = rec["resource_terminal"]
    require(type(terminal) is dict and set(terminal) == {"phase", "cap", "value", "limit"} and
            type(terminal["phase"]) is str and
            terminal["cap"] in {"wall_seconds", "rss_bytes", *RESOURCE_COUNTERS} and
            type(terminal["value"]) in (int, float) and type(terminal["value"]) is not bool and
            type(terminal["limit"]) in (int, float) and type(terminal["limit"]) is not bool and
            terminal["value"] > terminal["limit"] and
            rec["reason"] == (f"phase={terminal['phase']}:cap={terminal['cap']}:"
                              f"value={terminal['value']}:limit={terminal['limit']}"),
            "UNKNOWN_RESOURCE exact terminal")
    resource = rec["resource"]
    require(type(resource) is dict and set(resource) == {"phase", "elapsed_seconds",
            "limits", "counters", "rss_bytes", "process_model",
            "resumed_from_limits"} and type(resource.get("limits")) is dict and
            type(resource.get("counters")) is dict and type(resource.get("phase")) is str and
            type(resource.get("elapsed_seconds")) in (int, float) and
            resource["elapsed_seconds"] >= 0 and type(resource.get("rss_bytes")) is int and
            resource["rss_bytes"] >= 0 and resource.get("process_model") == {
                "single_process": True, "workers": 0,
                "aggregate_process_tree_required": False} and
            (resource.get("resumed_from_limits") is None or
             type(resource.get("resumed_from_limits")) is dict),
            "UNKNOWN_RESOURCE snapshot")
    limits, counters = resource["limits"], resource["counters"]
    require(set(limits) == {"wall_seconds", "rss_bytes", *RESOURCE_COUNTERS} and
            set(counters) == set(RESOURCE_COUNTERS) and
            type(limits["wall_seconds"]) in (int, float) and
            limits["wall_seconds"] > 0 and type(limits["rss_bytes"]) is int and
            limits["rss_bytes"] >= 0, "UNKNOWN_RESOURCE limits")
    for name in RESOURCE_COUNTERS:
        require(type(limits[name]) is int and limits[name] >= 0 and
                type(counters[name]) is int and 0 <= counters[name] <= limits[name],
                "UNKNOWN_RESOURCE counter:" + name)
    require(resource["phase"] == terminal["phase"] and
            terminal["limit"] == limits[terminal["cap"]],
            "UNKNOWN_RESOURCE phase/cap/limit binding")
    if terminal["phase"] == "presentation_roster_preflight":
        require(terminal["cap"] == "presentation_rows" and
                terminal["value"] ==
                    counters["presentation_rows"] + PRESENTATION_ROWS and
                all(counters[name] == 0 for name in (
                    "q0_states", "q0_edges", "presentation_rows",
                    "gamma_operations", "dag_nodes")),
                "UNKNOWN_RESOURCE presentation preflight semantics")
    checkpoint_binding = rec["checkpoint"]
    if checkpoint_binding is None:
        require(rec["checkpoint_manifest"] is None and
                rec["checkpoint_unavailable_reason"] ==
                "checkpoint_bytes_cap_or_unready", "resource checkpoint reason")
        return UNKNOWN_RESOURCE
    require(rec["checkpoint_unavailable_reason"] is None and
            type(checkpoint_binding) is dict and set(checkpoint_binding) ==
            {"path", "bytes", "sha256", "cursor", "bridge_cursor", "seal_sha256"} and
            checkpoint_binding["path"] == OUTPUT_RESUME_CHECKPOINT,
            "resource checkpoint binding")
    raw = read_checked(ROOT / checkpoint_binding["path"], budget,
                       "resource checkpoint file")
    require(len(raw) == strict_int(checkpoint_binding["bytes"], "checkpoint bytes") and
            digest(raw) == checkpoint_binding["sha256"], "resource checkpoint identity")
    checkpoint = json.loads(raw)
    manifest_binding = rec["checkpoint_manifest"]
    require(type(manifest_binding) is dict and set(manifest_binding) == {
            "path", "bytes", "sha256", "self_digest_sha256",
            "future_checkpoint_path"} and
            manifest_binding["path"] == OUTPUT_RESUME_MANIFEST and
            manifest_binding["path"] != checkpoint_binding["path"] and
            manifest_binding["future_checkpoint_path"] ==
            FUTURE_RESUME_CHECKPOINT,
            "resource portable manifest binding")
    manifest_raw = read_checked(ROOT / manifest_binding["path"], budget,
                                "resource resume manifest file")
    manifest = json.loads(manifest_raw)
    require(manifest_raw == canonical(manifest) and
            len(manifest_raw) == manifest_binding["bytes"] and
            digest(manifest_raw) == manifest_binding["sha256"] and
            type(manifest) is dict and set(manifest) == RESUME_MANIFEST_KEYS and
            manifest["schema"] == RESUME_MANIFEST_SCHEMA and
            self_digest(manifest, "resource resume manifest") ==
                manifest_binding["self_digest_sha256"] and
            manifest["checkpoint_path"] == FUTURE_RESUME_CHECKPOINT and
            manifest["checkpoint_bytes"] == checkpoint_binding["bytes"] and
            manifest["checkpoint_sha256"] == checkpoint_binding["sha256"] and
            manifest["checkpoint_seal_sha256"] ==
                checkpoint_binding["seal_sha256"] and
            manifest["cursor"] == checkpoint_binding["cursor"] and
            manifest["bridge_cursor"] == checkpoint_binding["bridge_cursor"],
            "resource portable manifest/checkpoint identity")
    task176, q0_public, _ = authenticate_task176(args.task176_receipt, budget)
    task157, _ = authenticate_task157(budget)
    task172, _ = authenticate_task172(budget)
    binding = expected_input_binding(task176, task157, task172, sources)
    rebuilt = reconstruct_roster(budget)
    validate_checkpoint(checkpoint, rebuilt["rows"], binding,
                        q0_public["parent_letter_transition_sha256"], budget)
    if checkpoint["resumed_from"] is not None:
        validate_staged_resume_identity(
            checkpoint["resumed_from"], args.resume, args.resume_manifest,
            PRESENTATION_ROWS, budget)
    else:
        require(args.resume is None and args.resume_manifest is None,
                "resource terminal unexpected resume arguments")
    selected, selected_order = forward_greedy(rebuilt["group"])
    require(selected_order == GAMMA_ORDER and
            checkpoint["selected_gamma_records"] == selected and
            checkpoint_binding["cursor"] == checkpoint["cursor"] and
            checkpoint_binding["bridge_cursor"] == checkpoint["bridge_cursor"] and
            checkpoint_binding["seal_sha256"] == checkpoint["seal_sha256"] and
            checkpoint["limits"] == resource["limits"] and
            checkpoint["counters"] == resource["counters"],
            "resource checkpoint state")
    runtime = bridge_runtime(rebuilt, budget)
    bridge_rows = rebuilt["rows"][:checkpoint["bridge_cursor"]]
    _, bridge_digests, bridge_digest = replay_bridge(runtime, bridge_rows, budget)
    require(checkpoint["bridge_digests"] == bridge_digests and
            checkpoint["bridge_replay_sha256"] == bridge_digest,
            "resource checkpoint bridge prefix")
    return UNKNOWN_RESOURCE


# --------------------------- independent SELFTEST ---------------------------

def tmul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[index]] for index in range(3))


def tinv(a: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(a)
    for index, value in enumerate(a):
        answer[value] = index
    return tuple(answer)


def dmul(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return ((a[0] + (-1 if a[1] else 1) * b[0] +
             (3 if a[1] and b[1] else 0)) % 6,
            (a[1] + b[1]) % 2)


def dinv(a: tuple[int, int]) -> tuple[int, int]:
    for first in range(6):
        for second in range(2):
            candidate = (first, second)
            if dmul(a, candidate) == (0, 0) and dmul(candidate, a) == (0, 0):
                return candidate
    raise Reject("toy inverse")


def deval(word: Sequence[int]) -> tuple[int, int]:
    return deval_with_generators(word, (1, 0), (0, 1))


def deval_with_generators(word: Sequence[int], x_image: tuple[int, int],
                          y_image: tuple[int, int]) -> tuple[int, int]:
    value, generators = (0, 0), {1: x_image, 2: y_image}
    for letter in strict_word(list(word), "toy D word"):
        generator = generators[abs(letter)]
        value = dmul(value, generator if letter > 0 else dinv(generator))
    return value


CHECKER_TOY_CONTEXT_GENERATORS = (
    ((1, 0), (0, 1)), ((1, 0), (1, 1)), ((1, 0), (2, 1)),
    ((1, 0), (3, 1)), ((1, 0), (4, 1)), ((1, 0), (5, 1)),
    ((5, 0), (0, 1)), ((5, 0), (1, 1)), ((5, 0), (2, 1)),
    ((5, 0), (3, 1)),
)


def qeval(word: Sequence[int]) -> tuple[int, ...]:
    value = tuple(range(3))
    generators = {1: (1, 2, 0), 2: (1, 0, 2)}
    for letter in strict_word(list(word), "toy Q word"):
        generator = generators[abs(letter)]
        value = tmul(value, generator if letter > 0 else tinv(generator))
    return value


class CheckerToyGroup:
    def __init__(self) -> None:
        self.identity = (0, 0)
        self.states = [(0, 0), (3, 0)]
        self.ids = {value: index for index, value in enumerate(self.states)}
        self.words = [[1, 1, 1]]
        self.generators = [(3, 0)]
        self.transitions = [[1], [0]]

    @staticmethod
    def key(value: tuple[int, int]) -> tuple[int, int]:
        return value

    @staticmethod
    def mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
        return dmul(left, right)

    @staticmethod
    def inverse(value: tuple[int, int]) -> tuple[int, int]:
        return dinv(value)

    @staticmethod
    def eval(word: Sequence[int]) -> tuple[int, int]:
        return deval(word)

    def section_word(self, state: int) -> list[int]:
        require(type(state) is int and 0 <= state < 2, "checker toy section state")
        return [] if state == 0 else list(self.words[0])

    @staticmethod
    def closure(seed_ids: Sequence[int]) -> set[int]:
        require(all(type(value) is int and value in (0, 1) for value in seed_ids),
                "checker toy closure seeds")
        return {0, 1} if 1 in seed_ids else {0}


class CheckerToyP176:
    COORDINATE_WIDTHS = (3,) * 10

    def __init__(self) -> None:
        self.eval_calls = 0

    @staticmethod
    def encode(index: int, value: tuple[int, int]) -> bytes:
        require(type(index) is int and 0 <= index < 10 and
                type(value) is tuple and len(value) == 2,
                "checker toy coordinate encode")
        return bytes((index, value[0], value[1]))

    @staticmethod
    def decode(raw: bytes, index: int) -> tuple[int, int]:
        require(type(raw) is bytes and len(raw) == 3 and raw[0] == index and
                raw[1] < 6 and raw[2] < 2, "checker toy coordinate decode")
        return raw[1], raw[2]

    def eval_word_coordinates(self, old: Any, e3: Any, e4: Any, contexts: Any,
                              delete: Any, word: Sequence[int]) -> tuple[bytes, ...]:
        del old, e3, e4, contexts, delete
        self.eval_calls += 1
        return tuple(self.encode(index, deval_with_generators(
            word, CHECKER_TOY_CONTEXT_GENERATORS[index][0],
            CHECKER_TOY_CONTEXT_GENERATORS[index][1])) for index in range(10))

    @staticmethod
    def blob(old: Any, value: Any) -> bytes:
        del old
        require(type(value) is bytes and len(value) == 3,
                "checker toy blob")
        return value

    @classmethod
    def multiply_blob(cls, left: bytes, right: bytes, index: int,
                      e3: Any, e4: Any) -> bytes:
        del e3, e4
        return cls.encode(index, dmul(cls.decode(left, index),
                                      cls.decode(right, index)))

    @classmethod
    def inverse_blob(cls, raw: bytes, index: int, e3: Any, e4: Any) -> bytes:
        del e3, e4
        return cls.encode(index, dinv(cls.decode(raw, index)))


def checker_toy_q0(budget: Budget) -> dict[str, Any]:
    identity = tuple(range(3))
    states, ids, internal_parents, letters = [identity], {identity: 0}, [0], [0]
    transitions: list[list[int]] = []
    head = 0
    # Canonical public x/y BFS; production Gamma uses the independent reversed
    # traversal, while this miniature must replay the receipt's source sections.
    while head < len(states):
        state_id, state = head, states[head]
        head += 1
        targets: dict[int, int] = {}
        for letter in (1, 2):
            target = tmul(state, qeval([letter]))
            if target not in ids:
                ids[target] = len(states)
                states.append(target)
                internal_parents.append(state_id)
                letters.append(letter)
            targets[letter] = ids[target] + 1
        transitions.append([targets[1], targets[2]])
        budget.check("checker toy Q0 BFS")
    budget.bump("q0_states", len(states), "checker toy Q0 states")
    budget.bump("q0_edges", sum(len(row) for row in transitions),
                "checker toy Q0 edges")
    require(len(states) == len(transitions) == 6, "checker toy Q0 complete")
    parents = [0] + [internal_parents[index] + 1
                     for index in range(1, len(internal_parents))]
    return {"states": states, "ids": ids, "internal_parents": internal_parents,
            "parents": parents, "letters": letters, "transitions": transitions}


def checker_toy_q0_word(state: int, q0: dict[str, Any]) -> list[int]:
    out: list[int] = []
    while state:
        out.append(int(q0["letters"][state]))
        state = int(q0["internal_parents"][state])
    out.reverse()
    return out


def checker_toy_runtime(budget: Budget) -> dict[str, Any]:
    return {"p176": CheckerToyP176(), "old": None, "e3": None, "e4": None,
            "contexts": (), "delete": None, "abi_budget": budget,
            "selftest_nonsplit": True}


def checker_toy_rows(group: CheckerToyGroup,
                     relators: Sequence[Sequence[int]], budget: Budget,
                     prefix: Sequence[dict[str, Any]] = ()) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    records = [list(word) for word in group.words]
    for state in range(len(group.states)):
        source_section = group.section_word(state)
        for generator, source in enumerate(records):
            target = group.transitions[state][generator]
            target_section = group.section_word(target)
            rows.append({"layer": "Gamma_Cayley",
                "ordinal": state * len(records) + generator + 1,
                "state": state + 1, "generator": generator + 1,
                "target_state": target + 1,
                "word": reduce_word(source_section + source +
                                    inverse_word(target_section)),
                "ancestry": {"section_source_word": source_section,
                             "record_word": source,
                             "section_target_word": target_section}})
    outers = [group.eval([1]), group.eval([2])]
    for record, source_value in enumerate(group.generators):
        for letter, outer in enumerate(outers):
            for slot, orientation in enumerate((1, -1), 1):
                if orientation == 1:
                    target_value = group.mul(group.mul(group.inverse(outer), source_value), outer)
                    tokens = [-(letter + 1)] + records[record] + [letter + 1]
                else:
                    target_value = group.mul(group.mul(outer, source_value), group.inverse(outer))
                    tokens = [letter + 1] + records[record] + [-(letter + 1)]
                target = group.ids[group.key(target_value)]
                target_section = group.section_word(target)
                rows.append({"layer": "action",
                    "ordinal": record * 4 + letter * 2 + slot,
                    "record": record + 1, "letter": letter + 1,
                    "orientation": orientation, "target_state": target + 1,
                    "word": reduce_word(tokens + inverse_word(target_section)),
                    "ancestry": {"tokens": tokens, "record_word": records[record],
                                 "section_target_word": target_section}})
    for ordinal, relator in enumerate(relators, 1):
        source = list(relator)
        target = group.ids[group.key(group.eval(source))]
        section = group.section_word(target)
        rows.append({"layer": "Q0_lift", "ordinal": ordinal,
            "target_state": target + 1,
            "word": reduce_word(source + inverse_word(section)),
            "ancestry": {"q0_relator_word": source,
                         "section_target_word": section}})
    require(len(rows) == 9 and len(prefix) <= len(rows),
            "checker toy complete row construction")
    for index, row in enumerate(rows):
        require(group.eval(row["word"]) == group.identity,
                "checker toy row identity")
        if index < len(prefix):
            require(row == prefix[index], "checker toy resume prefix")
        budget.bump("presentation_rows", 1, "checker toy row replay")
        budget.bump("dag_nodes", len(row["word"]) + 1,
                    "checker toy DAG replay")
        budget.bump("gamma_operations", 1, "checker toy identity replay")
    return rows


def checker_toy_bridge(runtime: dict[str, Any], rows: Sequence[dict[str, Any]],
                       budget: Budget) -> tuple[list[str], int]:
    before = runtime["p176"].eval_calls
    indexed: list[tuple[int, str]] = []
    for index in reversed(range(len(rows))):
        row = rows[index]
        trace = bridge_trace(runtime, row["word"],
            f"relator:{row['layer']}:{row['ordinal']}", budget)
        indexed.append((index, digest_obj(trace)))
    digests = [value for _, value in sorted(indexed)]
    calls = runtime["p176"].eval_calls - before
    require(calls == len(rows), "checker toy actual relator eval calls")
    return digests, calls


def checker_toy_source(runtime: dict[str, Any], group: CheckerToyGroup,
                       q0: dict[str, Any], budget: Budget) -> dict[str, Any]:
    gamma_word, q0_word = group.section_word(1), checker_toy_q0_word(1, q0)
    source_word = reduce_word(gamma_word + q0_word)
    gamma_value = checker_eval(runtime, gamma_word, budget)
    q0_value = checker_eval(runtime, q0_word, budget)
    value = checker_multiply(runtime, gamma_value, q0_value, budget)
    require(value == checker_eval(runtime, source_word, budget),
            "checker toy source section replay")
    return {"gamma_state_id": 2, "q0_state_id": 2,
            "gamma_word": gamma_word, "q0_word": q0_word,
            "source_word": source_word, "value": value}


def checker_toy_consumer_abi(runtime: dict[str, Any], group: CheckerToyGroup,
                             q0: dict[str, Any], rows_sha256: str,
                             budget: Budget) -> dict[str, Any]:
    x, y = checker_eval(runtime, [1], budget), checker_eval(runtime, [2], budget)
    x_inverse = checker_inverse(runtime, x, budget)
    xy = checker_multiply(runtime, x, y, budget)
    source = checker_toy_source(runtime, group, q0, budget)
    action = checker_action(runtime, [1], y, budget)
    cocycle = checker_section_cocycle(runtime, [1], [2], [1, 2], budget)
    require(x_inverse == checker_eval(runtime, [-1], budget) and
            xy == checker_eval(runtime, [1, 2], budget) and
            action == checker_eval(runtime, [1, 2, -1], budget) and
            cocycle == checker_eval(runtime, [], budget),
            "checker toy executable ABI")
    context_maps = []
    for block_index, coordinate_indices in enumerate(SEVEN_BLOCKS, 1):
        images = [{"x_image": list(CHECKER_TOY_CONTEXT_GENERATORS[coordinate_index][0]),
                   "y_image": list(CHECKER_TOY_CONTEXT_GENERATORS[coordinate_index][1])}
                  for coordinate_index in coordinate_indices]
        value_signature = digest_obj([[row["x_image"], row["y_image"]]
                                      for row in images])
        context_maps.append({"block_index": block_index,
                             "coordinate_indices": list(coordinate_indices),
                             "generator_images": images,
                             "value_signature_sha256": value_signature})
    signatures = [row["value_signature_sha256"] for row in context_maps]
    value_blocks = [tuple((tuple(image["x_image"]), tuple(image["y_image"]))
                          for image in row["generator_images"])
                    for row in context_maps]
    require(len(context_maps) == len(set(value_blocks)) ==
            len(set(signatures)) == 7,
            "checker seven genuinely distinct context maps")
    d_normal_forms = ([[1] * exponent for exponent in range(6)] +
                      [[1] * exponent + [2] for exponent in range(6)])
    require(CHECKER_TOY_CONTEXT_GENERATORS[0] == ((1, 0), (0, 1)) and
            all(images[0] in ((1, 0), (5, 0)) and images[1][1] == 1 and
                len({deval_with_generators(word, images[0], images[1])
                     for word in d_normal_forms}) == 12
                for images in CHECKER_TOY_CONTEXT_GENERATORS),
            "checker ten genuine Dic3 automorphisms")
    joint_values = [checker_eval(runtime, word, budget)
                    for word in d_normal_forms]
    require(len({digest_obj(value) for value in joint_values}) == 12,
            "checker Dic3 joint coordinate image order")
    y_state = q0["ids"][qeval([2])]
    product_state = q0["ids"][tmul(qeval([2]), qeval([2]))]
    y_section = checker_toy_q0_word(y_state, q0)
    product_section = checker_toy_q0_word(product_state, q0)
    nonsplit_value = checker_section_cocycle(
        runtime, y_section, y_section, product_section, budget)
    multiplied = checker_multiply(
        runtime, checker_eval(runtime, y_section, budget),
        checker_eval(runtime, y_section, budget), budget)
    canonical_product = checker_eval(runtime, product_section, budget)
    require(product_state == 0 and product_section == [] and
            multiplied == checker_multiply(
                runtime, nonsplit_value, canonical_product, budget) and
            nonsplit_value == checker_eval(runtime, [2, 2], budget) and
            nonsplit_value != checker_eval(runtime, [], budget),
            "checker non-split section cocycle")
    require(nonsplit_value in joint_values,
            "checker non-split cocycle in joint image")
    joint_coordinate_image = {"normal_forms": d_normal_forms,
        "values": joint_values,
        "distinct_value_count": len({digest_obj(value)
                                      for value in joint_values}),
        "nonsplit_value_normal_form_index": joint_values.index(nonsplit_value)}
    nonsplit_cocycle = {"quotient_left_state": y_state + 1,
        "quotient_right_state": y_state + 1,
        "quotient_product_state": product_state + 1,
        "left_section_word": y_section, "right_section_word": y_section,
        "canonical_product_section_word": product_section,
        "value": nonsplit_value, "nontrivial": True}
    return {"schema": "d972-r07-v188-roof-consumer-action-abi/v1",
        "module": "search/d972_r07_seven_context_roof_presentation_v1.py",
        "runtime_constructor": "load_runtime",
        "registry_callable": "v188_consumer_action_abi",
        "entry_points": {
            "eval": {"callable": "roof_eval", "arguments": ["runtime", "word"]},
            "multiply": {"callable": "roof_multiply",
                         "arguments": ["runtime", "left", "right"]},
            "inverse": {"callable": "roof_inverse",
                        "arguments": ["runtime", "value"]},
            "source_section": {"callable": "roof_source_section",
                               "arguments": ["runtime", "gamma_state_id",
                                             "q0_state_id"]},
            "action": {"callable": "roof_action",
                       "arguments": ["runtime", "actor_word", "value"]},
            "section_cocycle": {"callable": "roof_section_cocycle",
                                "arguments": ["runtime", "left_section_word",
                                              "right_section_word",
                                              "product_section_word"]}},
        "encoding": {"source_word": "strict signed F2 list",
                     "roof_value": "ten lowercase hex typed coordinate blobs",
                     "state_ids": "one-based Gamma and Q0 ids"},
        "semantics": {"multiplication": "left_then_right",
                      "action": "actor*value*actor_inverse",
                      "section_cocycle": "s_left*s_right*s_product_inverse"},
        "coordinate_widths": list(runtime["p176"].COORDINATE_WIDTHS),
        "coordinate_ledger_sha256": digest_obj(COORDINATES),
        "relator_rows_sha256": rows_sha256,
        "context_maps": context_maps,
        "joint_coordinate_image": joint_coordinate_image,
        "canaries": {"x": {"word": [1], "value": x},
                     "y": {"word": [2], "value": y},
                     "x_inverse": {"word": [-1], "value": x_inverse},
                     "xy": {"word": [1, 2], "value": xy},
                     "source_2_2": source,
                     "x_action_y": {"actor_word": [1], "input": y,
                                    "value": action},
                      "xy_section_cocycle": {"left": [1], "right": [2],
                         "product": [1, 2], "value": cocycle},
                      "nonsplit_y_y_section_cocycle": nonsplit_cocycle}}


def checker_toy_d_order() -> int:
    seen, queue = {(0, 0)}, [(0, 0)]
    for state in queue:
        for generator in ((0, 1), (1, 0)):
            target = dmul(state, generator)
            if target not in seen:
                seen.add(target)
                queue.append(target)
    require(all(dmul(dinv(value), value) == (0, 0) for value in seen),
            "checker toy D inverse closure")
    return len(seen)


def checker_toy_normal(group: CheckerToyGroup,
                       relators: Sequence[Sequence[int]],
                       budget: Budget) -> tuple[int, list[int]]:
    seeds = [group.ids[group.key(group.eval(word))] for word in relators]
    current, rounds = group.closure(seeds), [len(group.closure(seeds))]
    sweep_start = set(current)
    for outer in reversed((group.eval([1]), group.eval([2]))):
        for state_id in sorted(current, reverse=True):
            value = group.mul(group.mul(outer, group.states[state_id]),
                              group.inverse(outer))
            current |= group.closure([group.ids[group.key(value)]])
            budget.bump("gamma_operations", 1, "checker toy normal closure")
    if current != sweep_start:
        rounds.append(len(current))
    return len(current), rounds


def toy_seal(value: dict[str, Any]) -> dict[str, Any]:
    value.pop("self_digest_sha256", None)
    value["self_digest_sha256"] = digest_obj(value)
    return value


def checker_validate_toy_checkpoint(value: Any) -> dict[str, Any]:
    require(type(value) is dict and set(value) == CHECKPOINT_KEYS,
            "checker toy checkpoint keys")
    body = dict(value)
    claimed = body.pop("seal_sha256", None)
    require(type(claimed) is str and claimed == digest_obj(body) and
            value["schema"] == CHECKPOINT_SCHEMA and value["sealed"] is True and
            value["stage"] == "bridge_replay" and
            type(value["cursor"]) is int and value["cursor"] == 9 and
            type(value["bridge_cursor"]) is int and value["bridge_cursor"] == 9 and
            type(value["total_rows"]) is int and value["total_rows"] == 9 and
            type(value["rows"]) is list and len(value["rows"]) == 9 and
            value["rows_sha256"] == digest_obj(value["rows"]) and
            type(value["bridge_digests"]) is list and
            len(value["bridge_digests"]) == 9 and
            all(type(row) is str for row in value["bridge_digests"]) and
            value["bridge_replay_sha256"] == digest_obj(value["bridge_digests"]) and
            value["chunks"] == chunk_seals(value["rows"]) and
            value["dag_nodes"] == sum(len(row["word"]) + 1
                                       for row in value["rows"]),
            "checker toy checkpoint envelope")
    require(type(value["limits"]) is dict and
            set(value["limits"]) == {"wall_seconds", "rss_bytes", *RESOURCE_COUNTERS} and
            type(value["counters"]) is dict and
            set(value["counters"]) == set(RESOURCE_COUNTERS) and
            type(value["limits"]["wall_seconds"]) in (int, float) and
            type(value["limits"]["wall_seconds"]) is not bool and
            value["limits"]["wall_seconds"] > 0 and
            type(value["limits"]["rss_bytes"]) is int and
            value["limits"]["rss_bytes"] >= 0 and
            all(type(value["limits"][name]) is int and value["limits"][name] >= 0
                for name in RESOURCE_COUNTERS) and
            all(type(value["counters"][name]) is int and
                0 <= value["counters"][name] <= value["limits"][name]
                for name in RESOURCE_COUNTERS),
            "checker toy checkpoint resources")
    require(type(value["resumed_from"]) is dict and
            set(value["resumed_from"]) == RESUMED_FROM_KEYS,
            "checker toy final resumed-from")
    return value


def checker_replay_toy_checkpoint(checkpoint: Any, budget: Budget) -> dict[str, Any]:
    value = checker_validate_toy_checkpoint(checkpoint)
    group = CheckerToyGroup()
    raw = canonical(value)
    budget.bump("checkpoint_bytes", len(raw), "checker toy checkpoint authentication")
    q0 = checker_toy_q0(budget)
    binding = {"toy": "Dic3-S3-v4-production-path", "typed_coordinates": 10,
        "predecessor_dependency_cone_sha256":
            dependency_cone_manifest()["members_sha256"]}
    require(value["input_binding"] == binding and
            value["q0_transition_sha256"] ==
            digest_obj({"parents": q0["parents"], "letters": q0["letters"]}) and
            value["selected_gamma_records"] == [1],
            "checker toy checkpoint bindings")
    relators = [[1, 1, 1], [2, 2], [1, 2, 1, 2]]
    rows = checker_toy_rows(group, relators, budget, value["rows"])
    require(value["task172_roster_sha256"] ==
            digest_obj({"schema": SELFTEST_SCHEMA + "/row-roster/v1",
                "row_count": len(rows),
                "layer_counts": {name: sum(row["layer"] == name for row in rows)
                    for name in ("Gamma_Cayley", "action", "Q0_lift")}}),
            "checker toy checkpoint roster")
    runtime = checker_toy_runtime(budget)
    digests, eval_calls = checker_toy_bridge(runtime, rows, budget)
    require(value["bridge_digests"] == digests and
            value["bridge_replay_sha256"] == digest_obj(digests),
            "checker toy checkpoint bridge replay")
    evaluator = checker_toy_consumer_abi(
        runtime, group, q0, digest_obj(rows), budget)
    budget.check("checker toy complete replay")
    return {"group": group, "q0": q0,
            "relators": relators, "rows": rows, "digests": digests,
            "eval_calls": eval_calls, "evaluator": evaluator}


def toy_summary(value: dict[str, Any]) -> dict[str, Any]:
    return {"q0_order": value["extension"]["Q0_order"],
        "gamma_order": value["extension"]["Gamma_order"],
        "D_order": value["extension"]["D_order"],
        "presentation_rows": value["presentation"]["row_count"],
        "layer_counts": value["presentation"]["layer_counts"],
        "q0_relator_count": len(value["Q0"]["relators"]),
        "selected_gamma_records": value["presentation"]["selected_gamma_records"],
        "kernel_order": value["bridge"]["kernel_order"],
        "raw_coordinate_count": len(value["bridge"]["ten"]),
        "occurrence_count": len(value["bridge"]["eleven"]),
        "seven_block_count": len(value["bridge"]["seven"]),
        "q0_order_upper_bound": value["Q0"]["presentation_order_upper_bound"],
        "total_order_bound": value["presentation"]["total_order_bound"]}


def validate_toy_terminal(envelope: Any, expected_cap: str,
                          expect_checkpoint: bool) -> None:
    keys = {"schema", "status", "terminal", "reason", "result", "resource",
        "resource_terminal", "checkpoint", "checkpoint_manifest",
        "checkpoint_unavailable_reason",
        "cofinal_lift", "fake", "Ihara_witness", "self_digest_sha256"}
    require(type(envelope) is dict and set(envelope) == keys and
            envelope["schema"] == SCHEMA and
            envelope["status"] == envelope["terminal"] == UNKNOWN_RESOURCE and
            envelope["result"] is None and envelope["cofinal_lift"] is False and
            envelope["fake"] is False and envelope["Ihara_witness"] is False,
            "toy actual UNKNOWN_RESOURCE envelope")
    self_digest(envelope, "toy resource terminal")
    detail, resource = envelope["resource_terminal"], envelope["resource"]
    require(type(detail) is dict and set(detail) == {"phase", "cap", "value", "limit"} and
            detail["cap"] == expected_cap and
            type(detail["value"]) is int and type(detail["limit"]) is int and
            detail["value"] > detail["limit"] and
            envelope["reason"] == (f"phase={detail['phase']}:cap={detail['cap']}:"
                f"value={detail['value']}:limit={detail['limit']}") and
            type(resource) is dict and set(resource) == {"phase", "elapsed_seconds",
                "limits", "counters", "rss_bytes", "process_model",
                "resumed_from_limits"} and resource["phase"] == detail["phase"] and
            type(resource["elapsed_seconds"]) in (int, float) and
            type(resource["elapsed_seconds"]) is not bool and
            resource["elapsed_seconds"] >= 0 and type(resource["rss_bytes"]) is int and
            resource["rss_bytes"] >= 0 and resource["process_model"] == {
                "single_process": True, "workers": 0,
                "aggregate_process_tree_required": False},
            "toy resource terminal semantics")
    limits, counters = resource["limits"], resource["counters"]
    require(type(limits) is dict and
            set(limits) == {"wall_seconds", "rss_bytes", *RESOURCE_COUNTERS} and
            type(counters) is dict and set(counters) == set(RESOURCE_COUNTERS) and
            type(limits["wall_seconds"]) in (int, float) and
            type(limits["wall_seconds"]) is not bool and limits["wall_seconds"] > 0 and
            type(limits["rss_bytes"]) is int and limits["rss_bytes"] >= 0 and
            all(type(limits[name]) is int and limits[name] >= 0 and
                type(counters[name]) is int and 0 <= counters[name] <= limits[name]
                for name in RESOURCE_COUNTERS),
            "toy resource terminal strict counters")
    require(detail["limit"] == limits[expected_cap] and
            (expected_cap != "gamma_operations" or
             detail["value"] == counters["gamma_operations"] + 1),
            "toy resource cap/value/limit binding")
    if expect_checkpoint:
        require(type(envelope["checkpoint"]) is dict and
                type(envelope["checkpoint_manifest"]) is dict and
                envelope["checkpoint_unavailable_reason"] is None,
                "toy resource checkpoint expected")
    else:
        require(envelope["checkpoint"] is None and
                envelope["checkpoint_manifest"] is None and
                envelope["checkpoint_unavailable_reason"] ==
                "checkpoint_bytes_cap_or_unready",
                "toy resource checkpoint correctly unavailable")


def read_toy_chain_checkpoint(evidence: Any, expected_cursor: int,
                              expected_bridge_cursor: int,
                              full_rows: Sequence[dict[str, Any]],
                              full_digests: Sequence[str], q0: dict[str, Any],
                              budget: Budget) \
        -> dict[str, Any]:
    require(type(evidence) is dict and set(evidence) ==
            {"terminal_envelope", "checkpoint_binding", "manifest_binding",
             "staged_checkpoint_binding", "staged_manifest_binding"},
            "toy resume-chain evidence keys")
    envelope = evidence["terminal_envelope"]
    binding = evidence["checkpoint_binding"]
    manifest_binding = evidence["manifest_binding"]
    staged_binding = evidence["staged_checkpoint_binding"]
    staged_manifest_binding = evidence["staged_manifest_binding"]
    require(binding == envelope["checkpoint"] and type(binding) is dict and
            set(binding) == {"path", "bytes", "sha256", "cursor", "bridge_cursor",
                             "seal_sha256"} and
            binding["cursor"] == expected_cursor and
            binding["bridge_cursor"] == expected_bridge_cursor and
            binding["path"].startswith(
                "ci/out/d972_r07_seven_context_roof_presentation_selftest."),
            "toy chain checkpoint binding")
    raw = read_checked(ROOT / binding["path"], budget, "checker toy chain checkpoint")
    checkpoint = json.loads(raw)
    require(raw == canonical(checkpoint) and len(raw) == binding["bytes"] and
            digest(raw) == binding["sha256"] and type(checkpoint) is dict and
            set(checkpoint) == CHECKPOINT_KEYS,
            "toy chain checkpoint identity")
    body = dict(checkpoint)
    seal = body.pop("seal_sha256", None)
    require(seal == digest_obj(body) == binding["seal_sha256"] and
            checkpoint["schema"] == CHECKPOINT_SCHEMA and checkpoint["sealed"] is True and
            checkpoint["total_rows"] == 9 and checkpoint["cursor"] == expected_cursor and
            checkpoint["bridge_cursor"] == expected_bridge_cursor and
            checkpoint["rows"] == list(full_rows[:expected_cursor]) and
            checkpoint["rows_sha256"] == digest_obj(checkpoint["rows"]) and
            checkpoint["bridge_digests"] == list(full_digests[:expected_bridge_cursor]) and
            checkpoint["bridge_replay_sha256"] ==
                digest_obj(checkpoint["bridge_digests"]) and
            checkpoint["chunks"] == chunk_seals(checkpoint["rows"]) and
            checkpoint["dag_nodes"] == sum(len(row["word"]) + 1
                for row in checkpoint["rows"]) and
            checkpoint["stage"] == ("presentation" if expected_cursor < 9
                                    else "bridge_replay") and
            checkpoint["input_binding"] == {
                "toy": "Dic3-S3-v4-production-path", "typed_coordinates": 10,
                "predecessor_dependency_cone_sha256":
                    dependency_cone_manifest()["members_sha256"]} and
            checkpoint["q0_transition_sha256"] == digest_obj(
                {"parents": q0["parents"], "letters": q0["letters"]}) and
            checkpoint["selected_gamma_records"] == [1] and
            checkpoint["task172_roster_sha256"] == digest_obj({
                "schema": SELFTEST_SCHEMA + "/row-roster/v1", "row_count": 9,
                "layer_counts": {"Gamma_Cayley": 2, "action": 4,
                                 "Q0_lift": 3}}) and
            checkpoint["counters"] == envelope["resource"]["counters"] and
             checkpoint["limits"] == envelope["resource"]["limits"],
             "toy chain checkpoint semantics/snapshot")
    require(manifest_binding == envelope["checkpoint_manifest"] and
            type(manifest_binding) is dict and set(manifest_binding) ==
            {"path", "bytes", "sha256", "self_digest_sha256",
             "future_checkpoint_path"} and
            manifest_binding["path"].startswith(
                "ci/out/d972_r07_seven_context_roof_presentation_selftest."),
            "toy chain manifest binding")
    manifest_raw = read_checked(ROOT / manifest_binding["path"], budget,
                                "checker toy chain manifest")
    manifest = json.loads(manifest_raw)
    require(manifest_raw == canonical(manifest) and
            len(manifest_raw) == manifest_binding["bytes"] and
            digest(manifest_raw) == manifest_binding["sha256"] and
            self_digest(manifest, "toy chain manifest") ==
                manifest_binding["self_digest_sha256"] and
            set(manifest) == RESUME_MANIFEST_KEYS and
            manifest["schema"] == RESUME_MANIFEST_SCHEMA and
            manifest["checkpoint_path"] ==
                manifest_binding["future_checkpoint_path"] and
            manifest["checkpoint_path"] != binding["path"] and
            manifest["checkpoint_bytes"] == binding["bytes"] and
            manifest["checkpoint_sha256"] == binding["sha256"] and
            manifest["checkpoint_seal_sha256"] == binding["seal_sha256"] and
            manifest["cursor"] == binding["cursor"] and
            manifest["bridge_cursor"] == binding["bridge_cursor"],
            "toy chain manifest/checkpoint binding")
    require(type(staged_binding) is dict and
            set(staged_binding) == {"path", "bytes", "sha256", "cursor",
                                    "bridge_cursor", "seal_sha256"} and
            type(staged_manifest_binding) is dict and
            set(staged_manifest_binding) == {
                "path", "bytes", "sha256", "self_digest_sha256",
                "future_checkpoint_path"} and
            staged_binding["path"] == manifest["checkpoint_path"] and
            staged_binding == {**binding, "path": staged_binding["path"]} and
            staged_manifest_binding == {
                **manifest_binding, "path": staged_manifest_binding["path"]} and
            staged_manifest_binding["path"] != manifest_binding["path"] and
            staged_manifest_binding["future_checkpoint_path"] ==
                staged_binding["path"],
            "toy fixed staged pair bindings")
    staged_raw = read_checked(ROOT / staged_binding["path"], budget,
                              "checker toy staged checkpoint")
    staged_manifest_raw = read_checked(
        ROOT / staged_manifest_binding["path"], budget,
        "checker toy staged manifest")
    require(staged_raw == raw and staged_manifest_raw == manifest_raw and
            len(staged_raw) == staged_binding["bytes"] and
            digest(staged_raw) == staged_binding["sha256"] and
            len(staged_manifest_raw) == staged_manifest_binding["bytes"] and
            digest(staged_manifest_raw) == staged_manifest_binding["sha256"],
            "toy current-output to fixed-stage byte identity")
    return checkpoint


def validate_toy(value: dict[str, Any], expected: dict[str, Any],
                 budget: Budget) -> None:
    top = {"schema", "status", "terminal", "sources", "extension", "Q0",
        "bridge", "presentation", "evaluator", "bridge_replay_sha256", "resume",
        "resume_chain", "resource_terminals", "resource", "self_digest_sha256"}
    require(type(value) is dict and set(value) == top and
            value.get("schema") == SELFTEST_SCHEMA and value.get("status") == "COMPLETE" and
            value.get("terminal") == "SELFTEST_COMPLETE", "toy schema/envelope")
    self_digest(value, "toy")
    require(toy_summary(value) == expected, "toy expected values")
    require(value["sources"] == {"normalized_predecessor_dependency_cone":
            dependency_cone_manifest()}, "toy direct dependency-cone receipt")
    require(value.get("extension") == {"construction": "Dic_3_to_S3_non_split",
        "Q0_order": 6, "Gamma_order": 2, "D_order": checker_toy_d_order(),
        "non_split_witness": {"y_squared": list(dmul((0, 1), (0, 1))),
                              "kernel_generator": [3, 0]}},
        "checker toy extension")
    replay = checker_replay_toy_checkpoint(value.get("resume"), budget)
    group, q0, rows = replay["group"], replay["q0"], replay["rows"]
    normal_forms = [[], [1], [1, 1], [2], [1, 2], [1, 1, 2]]
    expected_q0 = {"parents": q0["parents"], "parent_letters": q0["letters"],
        "transitions": q0["transitions"], "relators": replay["relators"],
        "normal_forms": normal_forms,
        "presentation_order_upper_bound": len(normal_forms),
        "marked_image_order": len(q0["states"])}
    require(value.get("Q0") == expected_q0, "checker toy Q0 semantics")
    defect_order, rounds = checker_toy_normal(group, replay["relators"], budget)
    selected, selected_order = [1], len(group.closure([1]))
    layers = {name: sum(row["layer"] == name for row in rows)
              for name in ("Gamma_Cayley", "action", "Q0_lift")}
    total_bound = selected_order * len(normal_forms)
    expected_presentation = {"rows": rows, "rows_sha256": digest_obj(rows),
        "row_count": len(rows), "layer_counts": layers,
        "selected_gamma_records": selected,
        "selected_gamma_closure_order": selected_order,
        "Gamma_cayley_order_bound": len(group.states),
        "Q0_order_bound": len(normal_forms), "total_order_bound": total_bound,
        "marked_image_order": checker_toy_d_order(),
        "normal_generation": defect_order == selected_order == 2 and
                             total_bound == checker_toy_d_order(),
        "normal_closure_rounds": rounds, "chunks": chunk_seals(rows)}
    require(value.get("presentation") == expected_presentation,
            "checker toy presentation semantics")
    ten = [{"type": row["type"], "context_id": row["context_id"], "token": index}
           for index, row in enumerate(COORDINATES)]
    eleven = insert_occurrences(ten)
    expected_bridge = {"ten": ten, "eleven": eleven,
        "seven": group_seven(eleven), "ten_to_eleven": list(TEN_TO_ELEVEN),
        "delete_duplicate": list(DELETE_DUPLICATE),
        "occurrence_ledger": occurrence_ledger(), "kernel_order": 1,
        "roof_order": checker_toy_d_order(), "relator_eval_calls": len(rows)}
    require(value.get("bridge") == expected_bridge and
            value.get("bridge_replay_sha256") == digest_obj(replay["digests"]),
            "checker toy bridge semantics")
    require(value.get("evaluator") == replay["evaluator"],
            "checker toy executable evaluator ABI")
    chain, terminals = value.get("resume_chain"), value.get("resource_terminals")
    require(type(chain) is dict and set(chain) ==
            {"presentation", "bridge", "completed_resumed_from"} and
            type(terminals) is dict and set(terminals) ==
            {"presentation", "bridge", "preflight_zero", "preflight_four"} and
            terminals["presentation"] == chain["presentation"]["terminal_envelope"] and
            terminals["bridge"] == chain["bridge"]["terminal_envelope"],
            "toy authenticated resume chain")
    validate_toy_terminal(terminals["presentation"], "gamma_operations", True)
    validate_toy_terminal(terminals["bridge"], "gamma_operations", True)
    validate_toy_terminal(terminals["preflight_zero"], "presentation_rows", False)
    validate_toy_terminal(terminals["preflight_four"], "presentation_rows", False)
    for name, limit in (("preflight_zero", 0), ("preflight_four", 4)):
        terminal = terminals[name]
        require(terminal["resource_terminal"] == {
                "phase": "presentation_roster_preflight",
                "cap": "presentation_rows", "value": 9, "limit": limit} and
                terminal["resource"]["limits"]["presentation_rows"] == limit and
                all(terminal["resource"]["counters"][counter] == 0
                    for counter in RESOURCE_COUNTERS),
                "toy preflight before predecessor reconstruction:" + name)
    presentation_checkpoint = read_toy_chain_checkpoint(
        chain["presentation"], 4, 0, rows, replay["digests"], q0, budget)
    bridge_checkpoint = read_toy_chain_checkpoint(
        chain["bridge"], 9, 2, rows, replay["digests"], q0, budget)
    require(presentation_checkpoint["resumed_from"] is None and
            type(bridge_checkpoint["resumed_from"]) is dict,
            "toy chained checkpoint ancestry")
    validate_staged_resume_identity(
        bridge_checkpoint["resumed_from"],
        chain["presentation"]["staged_checkpoint_binding"]["path"],
        chain["presentation"]["staged_manifest_binding"]["path"], 9, budget, True)
    final_checkpoint = value["resume"]
    require(chain["completed_resumed_from"] == final_checkpoint["resumed_from"],
            "toy completion resumed-from binding")
    validate_staged_resume_identity(
        final_checkpoint["resumed_from"],
        chain["bridge"]["staged_checkpoint_binding"]["path"],
        chain["bridge"]["staged_manifest_binding"]["path"], 9, budget, True)
    resource = value.get("resource")
    require(type(resource) is dict and set(resource) ==
            {"phase", "elapsed_seconds", "limits", "counters", "rss_bytes",
             "process_model", "resumed_from_limits"} and
            resource["phase"] == "toy_complete" and
            resource["limits"] == final_checkpoint["limits"] and
            type(resource["elapsed_seconds"]) in (int, float) and
            type(resource["elapsed_seconds"]) is not bool and
            resource["elapsed_seconds"] >= 0 and
            type(resource["rss_bytes"]) is int and resource["rss_bytes"] >= 0 and
            resource["process_model"] == {"single_process": True, "workers": 0,
                "aggregate_process_tree_required": False} and
            resource["resumed_from_limits"] == bridge_checkpoint["limits"],
            "checker toy measured resource shape")
    require(all(resource["counters"][name] == final_checkpoint["counters"][name]
                for name in RESOURCE_COUNTERS if name != "serialized_bytes") and
            resource["counters"]["serialized_bytes"] ==
                final_checkpoint["counters"]["serialized_bytes"] + len(canonical(value)),
            "checker toy receipt/checkpoint resource accounting")


def set_path(value: dict[str, Any], path: Sequence[Any], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def toy_mutations() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    def pop_row(value: dict[str, Any]) -> None:
        value["presentation"]["rows"].pop(0)
    def swap_context(value: dict[str, Any]) -> None:
        maps = value["evaluator"]["context_maps"]
        maps[0], maps[1] = maps[1], maps[0]
    def swap_rows(value: dict[str, Any]) -> None:
        value["presentation"]["rows"][0], value["presentation"]["rows"][1] = (
            value["presentation"]["rows"][1], value["presentation"]["rows"][0])
    def mutate_terminal_duplicate(value: dict[str, Any], name: str,
                                  field: str, replacement: Any) -> None:
        value["resource_terminals"][name]["resource_terminal"][field] = replacement
        value["resume_chain"][name]["terminal_envelope"][
            "resource_terminal"][field] = replacement
    return [
        ("context_order", swap_context),
        ("occurrence_sign", lambda v: set_path(v, ("bridge", "occurrence_ledger", 1, "factor_sign"), 1)),
        ("occurrence_tag", lambda v: set_path(v, ("bridge", "occurrence_ledger", 4, "block"), "H1")),
        ("fox_prefix", lambda v: set_path(v, ("bridge", "occurrence_ledger", 0, "fox_prefix_occurrences"), [2, 3])),
        ("deletion", lambda v: set_path(v, ("bridge", "delete_duplicate"), list(range(10)))),
        ("source_generator", lambda v: set_path(v, ("presentation", "rows", 1, "ancestry", "record_word"), [2])),
        ("q0_parent", lambda v: set_path(v, ("Q0", "parents", 1), 2)),
        ("q0_letter", lambda v: set_path(v, ("Q0", "parent_letters", 1), 2)),
        ("q0_transition", lambda v: set_path(v, ("Q0", "transitions", 0, 0), 1)),
        ("missing_cayley", pop_row),
        ("empty_tree_word", lambda v: set_path(v, ("presentation", "rows", 0, "word"), [1])),
        ("cayley_target", lambda v: set_path(v, ("presentation", "rows", 1, "target_state"), 2)),
        ("action_orientation", lambda v: set_path(v, ("presentation", "rows", 2, "orientation"), -1)),
        ("action_target", lambda v: set_path(v, ("presentation", "rows", 2, "target_state"), 1)),
        ("action_word", lambda v: set_path(v, ("presentation", "rows", 2, "word"), [1])),
        ("incomplete_q0", lambda v: v["Q0"]["relators"].pop()),
        ("lift_defect", lambda v: set_path(v, ("presentation", "rows", 8, "word"), [])),
        ("selected", lambda v: set_path(v, ("presentation", "selected_gamma_records"), [2])),
        ("selected_closure", lambda v: set_path(v, ("presentation", "selected_gamma_closure_order"), 1)),
        ("kernel_order", lambda v: set_path(v, ("bridge", "kernel_order"), 2)),
        ("roof_order", lambda v: set_path(v, ("bridge", "roof_order"), 6)),
        ("D_order", lambda v: set_path(v, ("extension", "D_order"), 11)),
        ("Gamma_order", lambda v: set_path(v, ("extension", "Gamma_order"), 1)),
        ("Q0_order", lambda v: set_path(v, ("extension", "Q0_order"), 5)),
        ("q0_bound", lambda v: set_path(v, ("Q0", "presentation_order_upper_bound"), 7)),
        ("total_bound", lambda v: set_path(v, ("presentation", "total_order_bound"), 11)),
        ("normal", lambda v: set_path(v, ("presentation", "normal_generation"), False)),
        ("row_digest", lambda v: set_path(v, ("presentation", "rows_sha256"), "0" * 64)),
        ("chunk_boundary", lambda v: set_path(v, ("presentation", "chunks", 0, "end"), 8)),
        ("chunk_digest", lambda v: set_path(v, ("presentation", "chunks", 0, "sha256"), "0" * 64)),
        ("resume_cursor", lambda v: set_path(v, ("resume", "cursor"), 8)),
        ("resume_prefix", lambda v: set_path(v, ("resume", "rows_sha256"), "0" * 64)),
        ("resume_seal", lambda v: set_path(v, ("resume", "seal_sha256"), "0" * 64)),
        ("resource_cap", lambda v: set_path(v, ("resource", "limits", "presentation_rows"), 8)),
        ("resource_counter", lambda v: set_path(v, ("resource", "counters", "presentation_rows"), 8)),
        ("resource_phase", lambda v: set_path(v, ("resource", "phase"), "mutated")),
        ("stale_input", lambda v: set_path(v, ("resume", "input_binding"), "stale")),
        ("nonsplit_cocycle", lambda v: set_path(v, ("evaluator", "canaries", "nonsplit_y_y_section_cocycle", "nontrivial"), False)),
        ("gamma_relator", lambda v: set_path(v, ("presentation", "rows", 1, "word"), [1])),
        ("dag_order", swap_rows),
        ("resource_terminal_phase", lambda v: mutate_terminal_duplicate(
            v, "presentation", "phase", "mutated")),
        ("resource_terminal_cap", lambda v: mutate_terminal_duplicate(
            v, "bridge", "cap", "q0_edges")),
        ("resource_terminal_value", lambda v: set_path(
            v, ("resource_terminals", "preflight_four", "resource_terminal",
                "value"), 4)),
        ("resource_terminal_limit", lambda v: set_path(
            v, ("resource_terminals", "preflight_four", "resource_terminal",
                "limit"), 9)),
    ]


def load_fixture(path_text: str | None, budget: Budget) -> dict[str, Any]:
    expected_path = PINS["selftest_fixture"][0]
    require(type(path_text) is str and Path(path_text).as_posix() == expected_path and
            not Path(path_text).is_absolute(), "fixture path")
    raw = pin_file(PINS["selftest_fixture"], budget)
    value = json.loads(raw)
    require(type(value) is dict and value.get("schema") ==
            "d972-r07-seven-context-roof-presentation-selftest-fixture/v4" and
            value.get("toy") == "Dic_3_to_S3_non_split_extension" and
            value.get("source_generators") == {"x": [1], "y": [2]} and
            value.get("production_path") == {
                "presentation_checkpoint_cursor": 4,
                "presentation_bridge_cursor": 0,
                "presentation_terminal_cap": "gamma_operations",
                "bridge_checkpoint_cursor": 9, "bridge_cursor": 2,
                "preflight_presentation_limits": [0, 4],
                "preflight_q0_counters": [0, 0],
                "portable_resume_stages": 2,
                "current_output_to_fixed_stage": True} and
            value.get("context_map_count") == 7 and
            value.get("toy_coordinate_automorphisms") == [
                {"u": 1, "v": item} for item in range(6)] + [
                {"u": 5, "v": item} for item in range(4)] and
            value.get("joint_coordinate_image") == {
                "normal_form_count": 12, "distinct_value_count": 12,
                "nonsplit_cocycle_in_image": True} and
            value.get("nonsplit_section_cocycle") == {
                "left": "y", "right": "y", "quotient_product": "identity",
                "canonical_product_section_word": [], "nontrivial": True} and
            type(value.get("expected")) is dict, "fixture content")
    return value


def reseal_toy_mutant(value: dict[str, Any], label: str) -> None:
    if label != "resume_seal":
        checkpoint = value["resume"]
        checkpoint.pop("seal_sha256", None)
        checkpoint["seal_sha256"] = digest_obj(checkpoint)
    for envelope in value["resource_terminals"].values():
        envelope.pop("self_digest_sha256", None)
        envelope["self_digest_sha256"] = digest_obj(envelope)
    for name in ("presentation", "bridge"):
        envelope = value["resume_chain"][name]["terminal_envelope"]
        envelope.pop("self_digest_sha256", None)
        envelope["self_digest_sha256"] = digest_obj(envelope)
    toy_seal(value)


def selftest(fixture: dict[str, Any], receipt_path: str | None,
             budget: Budget) -> tuple[int, int]:
    sources = authenticate_sources(budget)
    require(sources["normalized_predecessor_dependency_cone"] ==
            dependency_cone_manifest(), "SELFTEST authenticated dependency cone")
    require(type(receipt_path) is str and not Path(receipt_path).is_absolute() and
            Path(receipt_path).as_posix().startswith("ci/out/") and
            Path(receipt_path).is_file(), "producer SELFTEST receipt path")
    raw = read_checked(Path(receipt_path), budget, "producer SELFTEST receipt")
    certificate = json.loads(raw)
    require(raw == canonical(certificate), "producer SELFTEST receipt canonical")
    validate_toy(certificate, fixture["expected"], budget)
    mutations = toy_mutations()
    require(type(fixture.get("mutation_count")) is int and
            fixture["mutation_count"] == len(mutations), "fixture mutation count")
    rejected = 0
    for label, mutate in mutations:
        mutant = copy.deepcopy(certificate)
        mutate(mutant)
        require(mutant != certificate, "mutation no-op:" + label)
        reseal_toy_mutant(mutant, label)
        try:
            validate_toy(mutant, fixture["expected"], budget)
        except Reject:
            rejected += 1
        else:
            raise Reject("mutation accepted:" + label)
    require(rejected == len(mutations), "mutation coverage")
    return len(mutations), rejected


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--fixture")
    parser.add_argument("--receipt")
    parser.add_argument("--verdict")
    parser.add_argument("--task176-receipt",
                        default="ci/in/d972_r07_all_seven_extension_section_census_v1.json")
    parser.add_argument("--resume")
    parser.add_argument("--resume-manifest")
    parser.add_argument("--seconds", type=float, default=9000.0)
    parser.add_argument("--rss-bytes", type=int, default=8_000_000_000)
    parser.add_argument("--q0-states", type=int, default=Q0_ORDER)
    parser.add_argument("--q0-edges", type=int, default=2 * Q0_ORDER)
    parser.add_argument("--presentation-rows", type=int, default=PRESENTATION_ROWS)
    parser.add_argument("--gamma-operations", type=int, default=10_000_000)
    parser.add_argument("--dag-nodes", type=int, default=10_000_000)
    parser.add_argument("--serialized-bytes", type=int, default=2_000_000_000)
    parser.add_argument("--checkpoint-bytes", type=int, default=100_000_000)
    args = parser.parse_args(argv)
    budget = Budget(args)
    if args.selftest:
        attempted, rejected = selftest(
            load_fixture(args.fixture, budget), args.receipt, budget)
        if args.verdict:
            verdict_path = Path(args.verdict)
            require(not verdict_path.is_absolute() and
                    verdict_path.as_posix().startswith("ci/out/") and
                    not verdict_path.exists(), "SELFTEST verdict path/staleness")
            receipt_raw = read_checked(
                Path(args.receipt), budget, "SELFTEST verdict receipt reauthentication")
            verdict = {"schema": SELFTEST_SCHEMA + "/independent-crosscheck/v1",
                "accepted": True, "independent": True,
                "producer_receipt": {"path": Path(args.receipt).as_posix(),
                    "bytes": len(receipt_raw), "sha256": digest(receipt_raw)},
                "dependency_cone_sha256":
                    dependency_cone_manifest()["members_sha256"],
                "mutation_attempted": attempted, "mutation_rejected": rejected}
            verdict_raw = canonical(verdict)
            budget.bump("serialized_bytes", len(verdict_raw),
                        "SELFTEST checker verdict")
            verdict_path.parent.mkdir(parents=True, exist_ok=True)
            verdict_path.write_bytes(verdict_raw)
        print("R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_SELFTEST_PASS "
              f"q0_order=6 gamma_order=2 D_order=12 presentation_rows=9 "
              f"mutation_attempted={attempted} mutation_rejected={rejected}")
        return 0
    require(type(args.receipt) is str and Path(args.receipt).is_file(), "receipt path")
    raw = read_checked(Path(args.receipt), budget, "task198 receipt")
    rec = json.loads(raw)
    require(type(rec) is dict and rec.get("schema") == SCHEMA, "task198 schema")
    sources = authenticate_sources(budget)
    if rec.get("terminal") == ISO:
        validate_complete(rec, args, budget, sources)
        verdict = {"schema": SCHEMA + "/crosscheck/v2", "receipt_terminal": ISO,
                   "accepted": True, "independent": True}
        if args.verdict:
            path = Path(args.verdict)
            require(not path.is_absolute() and path.as_posix().startswith("ci/out/"),
                    "verdict path")
            path.parent.mkdir(parents=True, exist_ok=True)
            verdict_raw = canonical(verdict)
            budget.bump("serialized_bytes", len(verdict_raw), "checker verdict")
            path.write_bytes(verdict_raw)
        print("R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS "
              "terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441")
        return 0
    terminal = validate_terminal_envelope(rec, args, budget, sources)
    print("R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_NONPOSITIVE " + terminal)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
