#!/usr/bin/env python3
"""Task198b authenticated 6,441-word presentation of the R07 roof.

The production route reconstructs the frozen Cayley--action--lift
presentation and the task176 ten-coordinate evaluator.  It never enumerates
the 357,128,352 roof elements.  Positive fields are derived from executable
equalities and order computations, never predecessor Boolean assertions.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import struct
import sys
import time
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

TASK176_RECEIPT_BYTES = 13_649_089
TASK176_RECEIPT_SHA256 = "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41"
TASK176_ARTIFACT_ID = "9635036013"
TASK176_ZIP_SHA256 = "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912"
TASK176_RUN = "33044121344"
TASK176_HEAD = "0533e42019c9f67f6cec3d1566152db17b903836"
TASK176_MEMBER = "d972_r07_all_seven_extension_section_census_v1.json"
TASK176_MANIFEST = "ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json"
TASK176_TERMINAL = "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"
Q0_ORDER, GAMMA_ORDER, DELTA_ORDER = 1_469_664, 243, 357_128_352
PRESENTATION_ROWS = 6_441
RESOURCE_COUNTERS = ("q0_states", "q0_edges", "presentation_rows",
                     "gamma_operations", "dag_nodes", "serialized_bytes",
                     "checkpoint_bytes")

SEVEN_BLOCKS = ((0, 1, 2), (3, 0, 4), (5,), (6,), (7,), (8,), (9,))
TEN_TO_ELEVEN = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
ELEVEN_DELETE_DUPLICATE = (0, 1, 2, 3, 5, 6, 7, 8, 9, 10)
TASK176_COORDINATES = [
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

# Frozen right-to-left paper-product prefixes.  The repeated ten_index=0 is
# the E3 H1/1=H2/2 diagonal; E4-C21 remains ten_index=7 and is never merged.
OCCURRENCE_LEDGER = [
    {"ordinal": 1, "block": "H1", "block_index": 1, "block_slot": 1,
     "occurrence": "H1_fxy", "type": "E3", "ten_index": 0,
     "context_id": 21, "role": "hexagon_fxy", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": [3, 2]},
    {"ordinal": 2, "block": "H1", "block_index": 1, "block_slot": 2,
     "occurrence": "H1_fxz", "type": "E3", "ten_index": 1,
     "context_id": 22, "role": "hexagon_fxz", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": [3]},
    {"ordinal": 3, "block": "H1", "block_index": 1, "block_slot": 3,
     "occurrence": "H1_fyz", "type": "E3", "ten_index": 2,
     "context_id": 23, "role": "hexagon_fyz", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": []},
    {"ordinal": 4, "block": "H2", "block_index": 2, "block_slot": 1,
     "occurrence": "H2_fux", "type": "E3", "ten_index": 3,
     "context_id": 24, "role": "hexagon_fux", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": [6, 5]},
    {"ordinal": 5, "block": "H2", "block_index": 2, "block_slot": 2,
     "occurrence": "H2_fxy", "type": "E3", "ten_index": 0,
     "context_id": 21, "role": "hexagon_fxy", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": [6]},
    {"ordinal": 6, "block": "H2", "block_index": 2, "block_slot": 3,
     "occurrence": "H2_fuy", "type": "E3", "ten_index": 4,
     "context_id": 25, "role": "hexagon_fuy", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": []},
    {"ordinal": 7, "block": "P1", "block_index": 3, "block_slot": 1,
     "occurrence": "P_b1", "type": "E4", "ten_index": 5,
     "context_id": 1, "role": "pentagon_b1", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9, 8]},
    {"ordinal": 8, "block": "P2", "block_index": 4, "block_slot": 1,
     "occurrence": "P_b2", "type": "E4", "ten_index": 6,
     "context_id": 27, "role": "pentagon_b2", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9]},
    {"ordinal": 9, "block": "P3", "block_index": 5, "block_slot": 1,
     "occurrence": "P_b3", "type": "E4", "ten_index": 7,
     "context_id": 21, "role": "pentagon_b3", "factor_sign": 1,
     "orientation": "direct", "fox_prefix_occurrences": [11, 10]},
    {"ordinal": 10, "block": "P5", "block_index": 6, "block_slot": 1,
     "occurrence": "P_b5_inverse", "type": "E4", "ten_index": 8,
     "context_id": 26, "role": "pentagon_b5_inverse_slot", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": [11]},
    {"ordinal": 11, "block": "P4", "block_index": 7, "block_slot": 1,
     "occurrence": "P_b4_inverse", "type": "E4", "ten_index": 9,
     "context_id": 28, "role": "pentagon_b4_inverse_slot", "factor_sign": -1,
     "orientation": "inverse", "fox_prefix_occurrences": []},
]

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

# Normalized path-sorted union of every literal dependency identity in the
# final task175/task176/task179 producer/checker cone, plus the six owners and
# the final task179 driver.  The union is authenticated directly here and by
# the independent checker/driver; predecessor nesting is not treated as a
# substitute for these pins.
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


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float,
                 limit: int | float):
        super().__init__(f"{phase}:{cap}:{value}:{limit}")
        self.phase, self.cap, self.value, self.limit = phase, cap, value, limit


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def require(value: bool, message: str) -> None:
    if value is not True:
        raise RuntimeError(message)


def input_require(value: bool, message: str) -> None:
    if value is not True:
        raise InputStop(message)


def strict_int(value: Any, label: str, minimum: int | None = None) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        raise InputStop("STRICT_INT:" + label)
    return value


def strict_bool(value: Any, label: str) -> bool:
    if type(value) is not bool:
        raise InputStop("STRICT_BOOL:" + label)
    return value


def strict_word(value: Any, label: str) -> list[int]:
    if type(value) is not list:
        raise InputStop("STRICT_WORD:" + label)
    answer = []
    for letter in value:
        if type(letter) is not int or letter not in (-2, -1, 1, 2):
            raise InputStop("STRICT_WORD_LETTER:" + label)
        answer.append(letter)
    return answer


class Budget:
    """One monotonic meter shared with task179/task176 reconstruction."""
    def __init__(self, args: argparse.Namespace):
        self.started = time.monotonic()
        self.limits = {
            "wall_seconds": float(args.seconds), "rss_bytes": int(args.rss_bytes),
            "q0_states": int(args.q0_states), "q0_edges": int(args.q0_edges),
            "presentation_rows": int(args.presentation_rows),
            "gamma_operations": int(args.gamma_operations),
            "dag_nodes": int(args.dag_nodes),
            "serialized_bytes": int(args.serialized_bytes),
            "checkpoint_bytes": int(args.checkpoint_bytes),
        }
        input_require(self.limits["wall_seconds"] > 0.0,
                      "RESOURCE_LIMIT:wall_seconds")
        for name in ("rss_bytes",) + RESOURCE_COUNTERS:
            input_require(type(self.limits[name]) is int and self.limits[name] >= 0,
                          "RESOURCE_LIMIT:" + name)
        self.counters = {name: 0 for name in RESOURCE_COUNTERS}
        self.phase = "initialization"
        self.resumed_from_limits: dict[str, int | float] | None = None

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
        elapsed = time.monotonic() - self.started
        if elapsed > self.limits["wall_seconds"]:
            raise ResourceStop(phase, "wall_seconds", elapsed,
                               self.limits["wall_seconds"])
        rss = self.rss()
        if rss and rss > self.limits["rss_bytes"]:
            raise ResourceStop(phase, "rss_bytes", rss, self.limits["rss_bytes"])

    def bump(self, name: str, amount: int = 1, phase: str | None = None) -> None:
        require(name in self.counters and type(amount) is int and amount >= 0,
                "budget bump ABI")
        target = self.counters[name] + amount
        if target > self.limits[name]:
            raise ResourceStop(phase or self.phase, name, target,
                               self.limits[name])
        self.counters[name] = target
        self.check(phase or self.phase)

    def preflight(self, name: str, amount: int, phase: str) -> None:
        """Reject a known finite workload before its predecessor loop starts."""
        require(name in self.counters and type(amount) is int and amount >= 0,
                "budget preflight ABI")
        target = self.counters[name] + amount
        if target > self.limits[name]:
            raise ResourceStop(phase, name, target, self.limits[name])
        self.check(phase)

    def public(self) -> dict[str, Any]:
        return {"phase": self.phase,
                "elapsed_seconds": time.monotonic() - self.started,
                "limits": dict(self.limits), "counters": dict(self.counters),
                "rss_bytes": self.rss(),
                "process_model": {"single_process": True, "workers": 0,
                                  "aggregate_process_tree_required": False},
                "resumed_from_limits": self.resumed_from_limits}


def checked_read(path: Path, budget: Budget | None, phase: str) -> bytes:
    if not path.is_file():
        raise InputStop("MISSING:" + str(path))
    raw = path.read_bytes()
    if budget is not None:
        budget.bump("serialized_bytes", len(raw), phase)
    return raw


def file_pin(rel: str, size: int, digest: str,
             budget: Budget | None = None) -> bytes:
    raw = checked_read(ROOT / rel, budget, "authenticate_sources")
    if len(raw) != size or sha_bytes(raw) != digest:
        raise InputStop("PIN_MISMATCH:" + rel)
    return raw


def dependency_cone_manifest() -> dict[str, Any]:
    rows = [{"path": rel, "bytes": size, "sha256": digest}
            for rel, size, digest in DEPENDENCY_CONE]
    input_require([row["path"] for row in rows] ==
                  sorted(row["path"] for row in rows) and
                  len({row["path"] for row in rows}) == len(rows),
                  "DEPENDENCY_CONE_NORMALIZATION")
    return {"schema": SCHEMA + "/task175-task176-task179-dependency-cone/v1",
            "roots": ["task175_producer", "task175_checker",
                      "task176_producer", "task176_checker",
                      "task179_producer", "task179_checker"],
            "member_count": len(rows), "members": rows,
            "members_sha256": sha_obj(rows)}


def authenticate_sources(budget: Budget) -> dict[str, Any]:
    answer, authenticated_paths = {}, set()
    for name, (rel, size, digest) in PINS.items():
        file_pin(rel, size, digest, budget)
        answer[name] = {"path": rel, "bytes": size, "sha256": digest}
        authenticated_paths.add(rel)
    for rel, size, digest in DEPENDENCY_CONE:
        if rel not in authenticated_paths:
            file_pin(rel, size, digest, budget)
            authenticated_paths.add(rel)
    answer["normalized_predecessor_dependency_cone"] = dependency_cone_manifest()
    return answer


def validate_self_digest(obj: dict[str, Any], field: str, label: str) -> str:
    body = dict(obj)
    claimed = body.pop(field, None)
    input_require(type(claimed) is str and claimed == sha_obj(body),
                  label + ":SELF_DIGEST")
    return claimed


def authenticate_task176_receipt(path: Path, budget: Budget) -> dict[str, Any]:
    if path.is_absolute() or path.as_posix() != "ci/in/" + TASK176_MEMBER:
        raise InputStop("TASK176_RECEIPT_PATH")
    raw = checked_read(ROOT / path, budget, "task176_receipt")
    input_require(len(raw) == TASK176_RECEIPT_BYTES and
                  sha_bytes(raw) == TASK176_RECEIPT_SHA256,
                  "TASK176_RECEIPT_IDENTITY")
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputStop("TASK176_RECEIPT_JSON") from exc
    input_require(type(obj) is dict, "TASK176_RECEIPT_OBJECT")
    self_digest = validate_self_digest(obj, "self_digest_sha256", "TASK176")
    input_require(obj.get("schema") ==
                  "d972-r07-all-seven-extension-section-census/v1" and
                  obj.get("status") == "COMPLETE" and
                  obj.get("terminal") == TASK176_TERMINAL,
                  "TASK176_ENVELOPE")
    input_require(obj.get("coordinates") == TASK176_COORDINATES,
                  "TASK176_COORDINATE_LEDGER")
    result = obj.get("result")
    input_require(type(result) is dict, "TASK176_RESULT")
    extension = result.get("extension")
    input_require(extension == {"Gamma_order": GAMMA_ORDER,
                                "Q0_order": Q0_ORDER,
                                "exact_sequence": "1->Gamma->G->Q0->1"},
                  "TASK176_EXTENSION")
    families = result.get("families")
    input_require(type(families) is dict and type(families.get("ALL")) is dict,
                  "TASK176_FAMILY_ALL")
    all_family = families["ALL"]
    for name in ("A_order", "L_order", "Q0_index_L", "D_order"):
        strict_int(all_family.get(name), "TASK176_ALL:" + name, 1)
    input_require(all_family.get("label") == "ALL" and
                  all_family.get("coordinate_indices") == list(range(10)) and
                  all_family.get("formula") == "|D_S|=|A_S|*[Q0:L_S]",
                  "TASK176_ALL_METADATA")
    family_order = all_family["A_order"] * all_family["Q0_index_L"]
    extension_order = extension["Gamma_order"] * extension["Q0_order"]
    input_require(all_family["A_order"] == GAMMA_ORDER and
                  all_family["L_order"] == 1 and
                  all_family["Q0_index_L"] == Q0_ORDER and
                  all_family["D_order"] == family_order == extension_order ==
                  DELTA_ORDER, "TASK176_ALL_ORDER")
    checks = all_family.get("L_group_checks")
    input_require(type(checks) is dict and
                  strict_bool(checks.get("identity"), "TASK176_ALL:identity") and
                  strict_bool(checks.get("closure_by_exact_generated_subgroup"),
                              "TASK176_ALL:closure") and
                  strict_bool(checks.get("inverse_generators_in_subgroup"),
                              "TASK176_ALL:inverse") and
                  strict_bool(checks.get("normal_under_q0_x_y"),
                              "TASK176_ALL:normal"),
                  "TASK176_ALL_GROUP_CHECKS")
    qsection = result.get("Q0_section")
    input_require(type(qsection) is dict and
                  strict_int(qsection.get("order"), "TASK176_Q0_ORDER") == Q0_ORDER and
                  type(qsection.get("roster_sha256")) is str,
                  "TASK176_Q0_SECTION")
    parent_public = qsection.get("parent_states_u32le")
    letter_public = qsection.get("parent_letters_u8")
    for public, width, label in ((parent_public, 4, "parents"),
                                 (letter_public, 1, "letters")):
        input_require(type(public) is dict and
                      strict_int(public.get("record_count"), label + ":count") == Q0_ORDER and
                      strict_int(public.get("record_width_bytes"), label + ":width") == width and
                      type(public.get("raw_sha256")) is str and
                      type(public.get("compressed_sha256")) is str,
                      "TASK176_Q0_PAYLOAD:" + label)
    manifest_raw = checked_read(ROOT / TASK176_MANIFEST, budget,
                                "task176_manifest")
    try:
        manifest = json.loads(manifest_raw)
    except json.JSONDecodeError as exc:
        raise InputStop("TASK176_ARTIFACT_MANIFEST_JSON") from exc
    expected_manifest = {
        "artifact_id": TASK176_ARTIFACT_ID,
        "zip_sha256": TASK176_ZIP_SHA256,
        "run": TASK176_RUN, "head": TASK176_HEAD,
        "member": TASK176_MEMBER, "member_bytes": TASK176_RECEIPT_BYTES,
        "member_sha256": TASK176_RECEIPT_SHA256,
    }
    input_require(manifest == expected_manifest, "TASK176_ARTIFACT_MANIFEST")
    return {
        **expected_manifest, "receipt_path": path.as_posix(),
        "receipt_bytes": len(raw), "receipt_sha256": sha_bytes(raw),
        "receipt_self_digest_sha256": self_digest,
        "manifest_path": TASK176_MANIFEST, "manifest_bytes": len(manifest_raw),
        "manifest_sha256": sha_bytes(manifest_raw), "grade": "CROSS_CHECKED",
        "extension": extension,
        "family_ALL": {name: all_family[name] for name in
                       ("label", "coordinate_indices", "A_order", "L_order",
                        "Q0_index_L", "D_order", "formula")},
        "coordinates_sha256": sha_obj(TASK176_COORDINATES),
        "q0_parent_states_raw_sha256": parent_public["raw_sha256"],
        "q0_parent_letters_raw_sha256": letter_public["raw_sha256"],
        "q0_roster_sha256": qsection.get("roster_sha256"),
    }


def authenticate_task157ee_receipt(budget: Budget) -> dict[str, Any]:
    rel, size, digest = PINS["task157ee_receipt"]
    raw = file_pin(rel, size, digest, budget)
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputStop("TASK157EE_RECEIPT_JSON") from exc
    input_require(obj.get("schema") == "d972-b345-joint-kernel-qstar-closure/v1" and
                  obj.get("status") == "B345_JOINT_KERNEL_QSTAR_CLOSED" and
                  obj.get("terminal_token") == "B345_JOINT_KERNEL_QSTAR_CLOSED",
                  "TASK157EE_ENVELOPE")
    gamma, q0 = obj.get("gamma"), obj.get("q0_presentation")
    input_require(type(gamma) is dict and type(q0) is dict,
                  "TASK157EE_PRESENTATION")
    input_require(gamma.get("order") == GAMMA_ORDER and
                  gamma.get("edge_count") == 6318 and
                  gamma.get("generator_count") == 26,
                  "TASK157EE_GAMMA")
    expected_q0 = {"P_order": 504, "G9_order": 2916,
                   "Q0_order": Q0_ORDER, "P_relator_count": 5,
                   "G9_relator_count": 8, "complete_relator_count": 19}
    input_require(all(q0.get(key) == value for key, value in expected_q0.items()),
                  "TASK157EE_Q0")
    qrows = obj.get("q0_relations")
    input_require(type(qrows) is dict and qrows.get("row_count") == 19 and
                  qrows.get("relator_image_normal_closure_order") == GAMMA_ORDER,
                  "TASK157EE_Q0_DEFECTS")
    return {
        "path": rel, "bytes": size, "sha256": digest,
        "grade": "CROSS_CHECKED", "gamma_order": GAMMA_ORDER,
        "gamma_edges": 6318, "gamma_generators": 26,
        "q0_order": Q0_ORDER,
        "factor_payload_sha256": q0.get("factor_payload_sha256"),
        "complete_relators_sha256": q0.get("complete_relators_sha256"),
        "split_word_sha256": q0.get("split_word_sha256"),
        "q0_defect_normal_closure_order":
            qrows.get("relator_image_normal_closure_order"),
        "receipt_self_digest": obj.get("self_digest_sha256"),
    }


def authenticate_task172_receipt(budget: Budget) -> dict[str, Any]:
    rel, size, digest = PINS["task172_receipt"]
    raw = file_pin(rel, size, digest, budget)
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputStop("TASK172_RECEIPT_JSON") from exc
    roster, q3, contexts = (obj.get("relation_roster"), obj.get("q3"),
                            obj.get("contexts"))
    layers = {"gamma_edge": 6318, "xy_action": 104, "q0_relator": 19}
    rule = ("ri*4+li*2+(1 for orient +1, 2 for orient -1), "
            "frozen 157ee action_relations token order")
    input_require(obj.get("schema") == "d972-r07-full-e4-orbit-preflight/v7" and
                  obj.get("status") == "R07_FULL_E4_ORBIT_PREFLIGHT_READY" and
                  obj.get("terminal_token") == "R07_FULL_E4_ORBIT_PREFLIGHT_READY",
                  "TASK172_ENVELOPE")
    input_require(type(roster) is dict and roster.get("count") == PRESENTATION_ROWS and
                  roster.get("layers") == layers and
                  roster.get("expanded_words") is True and
                  roster.get("xy_action_ordinal_rule") == rule and
                  type(roster.get("roster_sha256")) is str,
                  "TASK172_ROSTER")
    input_require(type(q3) is dict and q3.get("artifact_sha256") ==
                  PINS["q3_receipt"][2] and q3.get("record_count") == 26 and
                  type(q3.get("record_words_sha256")) is str,
                  "TASK172_Q3")
    input_require(type(contexts) is dict and contexts.get("count") == 31 and
                  contexts.get("aliases") == 46 and
                  type(contexts.get("rows_sha256")) is str,
                  "TASK172_CONTEXTS")
    return {
        "path": rel, "bytes": size, "sha256": digest,
        "schema": obj["schema"], "status": obj["status"],
        "terminal": obj["terminal_token"],
        "relation_roster": {"count": roster["count"],
            "layers": roster["layers"], "expanded_words": roster["expanded_words"],
            "xy_action_ordinal_rule": roster["xy_action_ordinal_rule"],
            "roster_sha256": roster["roster_sha256"]},
        "q3": {"artifact_sha256": q3["artifact_sha256"],
               "record_count": q3["record_count"],
               "record_words_sha256": q3["record_words_sha256"]},
        "contexts": {"count": contexts["count"], "aliases": contexts["aliases"],
                     "rows_sha256": contexts["rows_sha256"]},
    }


def load_module(rel: str, name: str) -> Any:
    path = (ROOT / rel).resolve()
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise InputStop("MODULE_LOAD:" + rel)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def reduce_word(word: Iterable[int]) -> list[int]:
    answer: list[int] = []
    for letter in word:
        if type(letter) is not int or letter not in (-2, -1, 1, 2):
            raise RuntimeError("invalid free-group letter")
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return answer


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-letter for letter in reversed(strict_word(list(word), "inverse"))]


def load_runtime(budget: Budget) -> dict[str, Any]:
    # task179 delegates these two large traversals to task176, whose loops
    # poll wall/RSS but do not own task198's counters.  Reserve their known
    # complete extents before any reconstruction so a small cap cannot pay
    # for the work and fail only afterwards.
    budget.preflight("q0_states", Q0_ORDER,
                     "task179_Q0_complete_state_preflight")
    budget.preflight("q0_edges", 2 * Q0_ORDER,
                     "task179_Q0_complete_edge_preflight")
    fine_edges = 59_049 * 6
    budget.preflight("gamma_operations", fine_edges + 6318,
                     "task176_fine_deletion_and_Gamma_preflight")
    module = load_module(PINS["task179_producer"][0], "d198_task179")
    build = getattr(module, "build_runtime", None)
    if not callable(build):
        raise InputStop("TASK179_BUILD_RUNTIME_API")
    budget.check("task179_runtime_reconstruction")
    try:
        runtime = build(budget)
    except ResourceStop:
        raise
    except Exception as exc:
        if type(exc).__name__ == "InputStop":
            raise InputStop("TASK179_RUNTIME_INPUT:" + str(exc)) from exc
        if type(exc).__name__ == "ResourceStop":
            raise ResourceStop(str(getattr(exc, "phase", "task179_runtime")),
                               str(getattr(exc, "cap", "wall_seconds")),
                               getattr(exc, "value", 0),
                               getattr(exc, "limit", 0)) from exc
        raise
    input_require(type(runtime) is dict and len(runtime.get("qstates", [])) == Q0_ORDER and
                  len(runtime.get("parents", [])) == Q0_ORDER and
                  len(runtime.get("letters", b"")) == Q0_ORDER and
                  len(runtime.get("projected", [])) == GAMMA_ORDER,
                  "TASK179_RUNTIME_SIZES")
    budget.bump("q0_states", Q0_ORDER, "task179_Q0_complete_state_replay")
    budget.bump("q0_edges", 2 * Q0_ORDER, "task179_Q0_complete_edge_replay")
    budget.bump("gamma_operations", fine_edges,
                "task176_fine_deletion_edge_reconstruction")
    budget.bump("gamma_operations", 6318, "task179_Gamma_transition_replay")
    return runtime


def runtime_q0_payload(runtime: dict[str, Any], task176: dict[str, Any]) -> dict[str, Any]:
    parents, letters = runtime["parents"], bytes(runtime["letters"])
    parent_raw = b"".join(struct.pack("<I", value + 1 if index else 0)
                           for index, value in enumerate(parents))
    input_require(sha_bytes(parent_raw) == task176["q0_parent_states_raw_sha256"] and
                  sha_bytes(letters) == task176["q0_parent_letters_raw_sha256"],
                  "Q0_PARENT_LETTER_TASK176_BINDING")
    return {"order": Q0_ORDER, "state_count": len(parents),
            "edge_count": 2 * Q0_ORDER,
            "parent_states_u32le_sha256": sha_bytes(parent_raw),
            "parent_letters_u8_sha256": sha_bytes(letters),
            "parent_letter_transition_sha256": sha_bytes(parent_raw + letters),
            "discovery": "positive x,y first-seen BFS"}


def insertion(ten: Sequence[Any]) -> list[Any]:
    require(len(ten) == 10, "bridge insertion arity")
    return [ten[index] for index in TEN_TO_ELEVEN]


def deletion(eleven: Sequence[Any]) -> list[Any]:
    require(len(eleven) == 11, "bridge deletion arity")
    return [eleven[index] for index in ELEVEN_DELETE_DUPLICATE]


def regroup(eleven: Sequence[Any]) -> list[list[Any]]:
    require(len(eleven) == 11, "bridge regroup arity")
    return [list(eleven[0:3]), list(eleven[3:6]), [eleven[6]], [eleven[7]],
            [eleven[8]], [eleven[9]], [eleven[10]]]


def flatten(seven: Sequence[Sequence[Any]]) -> list[Any]:
    require([len(row) for row in seven] == [3, 3, 1, 1, 1, 1, 1],
            "bridge seven block arity")
    return [value for row in seven for value in row]


def bridge_blob_rows(runtime: dict[str, Any], rows: Sequence[Any]) -> list[str]:
    return [runtime["p176"].blob(runtime["old"], value).hex() for value in rows]


def replay_bridge_word(runtime: dict[str, Any], word: Sequence[int],
                       label: str) -> dict[str, Any]:
    strict_word(list(word), "bridge:" + label)
    ten = list(runtime["p176"].eval_word_coordinates(
        runtime["old"], runtime["e3"], runtime["e4"], runtime["contexts"],
        runtime["delete"], word))
    input_require(len(ten) == 10, "BRIDGE_TEN_ARITY")
    if runtime.get("selftest_nonsplit") is True and label.startswith("relator:"):
        input_require(all(runtime["p176"].decode(value, index) == (0, 0)
                          for index, value in enumerate(ten)),
                      "SELFTEST_EVERY_RELATOR_IDENTITY_IN_EVERY_COORDINATE")
    eleven, seven = insertion(ten), regroup(insertion(ten))
    ten_blob, eleven_blob = bridge_blob_rows(runtime, ten), bridge_blob_rows(runtime, eleven)
    deleted_blob = bridge_blob_rows(runtime, deletion(eleven))
    flattened_blob = bridge_blob_rows(runtime, flatten(seven))
    reinserted_blob = bridge_blob_rows(runtime, insertion(deletion(eleven)))
    input_require(eleven_blob[0] == eleven_blob[4], "BRIDGE_DIAGONAL_EQUALITY")
    input_require(deleted_blob == ten_blob, "BRIDGE_DELETE_INSERT_LEFT_INVERSE")
    input_require(reinserted_blob == eleven_blob,
                  "BRIDGE_INSERT_DELETE_IMAGE_INVERSE")
    input_require(flattened_blob == eleven_blob, "BRIDGE_REGROUP_INVERSE")
    occurrence_values = [eleven_blob[row["ordinal"] - 1]
                         for row in OCCURRENCE_LEDGER]
    return {"label": label, "word": list(word),
            "word_sha256": sha_obj(list(word)), "ten_sha256": sha_obj(ten_blob),
            "eleven_sha256": sha_obj(eleven_blob),
            "seven_sha256": sha_obj([bridge_blob_rows(runtime, block)
                                      for block in seven]),
            "occurrence_values_sha256": sha_obj(occurrence_values),
            "left_inverse": deleted_blob == ten_blob,
            "image_inverse": reinserted_blob == eleven_blob,
            "regroup_inverse": flattened_blob == eleven_blob}


def roof_eval(runtime: dict[str, Any], word: Sequence[int]) -> list[str]:
    """Executable v188 ABI: evaluate a strict signed F2 word in ten coordinates."""
    source = strict_word(list(word), "roof eval word")
    values = runtime["p176"].eval_word_coordinates(
        runtime["old"], runtime["e3"], runtime["e4"], runtime["contexts"],
        runtime["delete"], source)
    input_require(type(values) is tuple and len(values) == 10,
                  "ROOF_EVAL_TYPED_ARITY")
    meter = runtime.get("abi_budget")
    if meter is not None:
        meter.bump("gamma_operations", len(values), "v188_ABI_eval")
    return [runtime["p176"].blob(runtime["old"], value).hex()
            for value in values]


def roof_value(runtime: dict[str, Any], value: Any, label: str) -> list[bytes]:
    input_require(type(value) is list and len(value) == 10,
                  "ROOF_VALUE_ARITY:" + label)
    widths = tuple(getattr(runtime["p176"], "COORDINATE_WIDTHS", ()))
    input_require(len(widths) == 10, "ROOF_VALUE_WIDTH_ABI:" + label)
    result: list[bytes] = []
    for index, (encoded, width) in enumerate(zip(value, widths)):
        input_require(type(encoded) is str, f"ROOF_VALUE_HEX_TYPE:{label}:{index}")
        try:
            raw = bytes.fromhex(encoded)
        except ValueError as exc:
            raise InputStop(f"ROOF_VALUE_HEX:{label}:{index}") from exc
        input_require(raw.hex() == encoded and len(raw) == int(width),
                      f"ROOF_VALUE_TYPED_WIDTH:{label}:{index}")
        result.append(raw)
    return result


def roof_multiply(runtime: dict[str, Any], left: Any, right: Any) -> list[str]:
    """Executable v188 ABI: exact componentwise roof multiplication."""
    lhs, rhs = roof_value(runtime, left, "multiply-left"), roof_value(
        runtime, right, "multiply-right")
    answer = [runtime["p176"].multiply_blob(a, b, index,
              runtime["e3"], runtime["e4"]).hex()
              for index, (a, b) in enumerate(zip(lhs, rhs))]
    meter = runtime.get("abi_budget")
    if meter is not None:
        meter.bump("gamma_operations", len(answer), "v188_ABI_multiply")
    return answer


def roof_inverse(runtime: dict[str, Any], value: Any) -> list[str]:
    """Executable v188 ABI: exact componentwise roof inverse."""
    rows = roof_value(runtime, value, "inverse")
    answer = [runtime["p176"].inverse_blob(raw, index,
              runtime["e3"], runtime["e4"]).hex()
              for index, raw in enumerate(rows)]
    meter = runtime.get("abi_budget")
    if meter is not None:
        meter.bump("gamma_operations", len(answer), "v188_ABI_inverse")
    return answer


def roof_source_section(runtime: dict[str, Any], gamma_state_id: int,
                        q0_state_id: int) -> dict[str, Any]:
    """Executable compressed Gamma/Q0 source section; public ids are one-based."""
    gid = strict_int(gamma_state_id, "Gamma section state", 1) - 1
    qid = strict_int(q0_state_id, "Q0 section state", 1) - 1
    input_require(gid < len(runtime["gamma"].states) and
                  qid < len(runtime["parents"]), "ROOF_SECTION_STATE_RANGE")
    gamma_word = list(runtime["gamma"].section_word(gid))
    q0_word = runtime["p176"].q0_section_word(
        qid, runtime["parents"], runtime["letters"])
    word = reduce_word(gamma_word + q0_word)
    gamma_value = [runtime["p176"].blob(runtime["old"], item).hex()
                   for item in runtime["projected"][gid]]
    q0_value = [item.hex() for item in
                runtime["p176"].section_row(runtime["stores"], qid)]
    value = roof_multiply(runtime, gamma_value, q0_value)
    input_require(roof_eval(runtime, word) == value,
                  "ROOF_SECTION_LITERAL_REPLAY")
    return {"gamma_state_id": gamma_state_id, "q0_state_id": q0_state_id,
            "gamma_word": gamma_word, "q0_word": q0_word,
            "source_word": word, "value": value}


def roof_action(runtime: dict[str, Any], actor_word: Sequence[int],
                value: Any) -> list[str]:
    """Executable left action convention a.v = a*v*a^-1."""
    actor_source = strict_word(list(actor_word), "roof action actor")
    actor = roof_eval(runtime, actor_source)
    return roof_multiply(runtime, roof_multiply(runtime, actor, value),
                         roof_inverse(runtime, actor))


def roof_section_cocycle(runtime: dict[str, Any], left_section_word: Sequence[int],
                         right_section_word: Sequence[int],
                         product_section_word: Sequence[int]) -> list[str]:
    """Executable kappa(s,t)=s*t*(st-section)^-1 in source-word form."""
    left = strict_word(list(left_section_word), "cocycle left section")
    right = strict_word(list(right_section_word), "cocycle right section")
    product = strict_word(list(product_section_word), "cocycle product section")
    return roof_eval(runtime, reduce_word(left + right + inverse_word(product)))


def v188_consumer_action_abi() -> dict[str, Callable[..., Any]]:
    """Importable registry: values are live callables, never receipt prose."""
    return {"eval": roof_eval, "multiply": roof_multiply,
            "inverse": roof_inverse, "source_section": roof_source_section,
            "action": roof_action, "section_cocycle": roof_section_cocycle}


def consumer_abi_public(runtime: dict[str, Any], rows_sha256: str) -> dict[str, Any]:
    """Serialize callable entry points plus exact, independently replayable canaries."""
    registry = v188_consumer_action_abi()
    input_require(set(registry) == {"eval", "multiply", "inverse", "source_section",
                                    "action", "section_cocycle"} and
                  all(callable(value) for value in registry.values()),
                  "V188_EXECUTABLE_ABI_REGISTRY")
    x, y = roof_eval(runtime, [1]), roof_eval(runtime, [2])
    x_inv, xy = roof_inverse(runtime, x), roof_multiply(runtime, x, y)
    source = roof_source_section(runtime, 2, 2)
    action = roof_action(runtime, [1], y)
    cocycle = roof_section_cocycle(runtime, [1], [2], [1, 2])
    input_require(x_inv == roof_eval(runtime, [-1]) and
                  xy == roof_eval(runtime, [1, 2]) and
                  action == roof_eval(runtime, [1, 2, -1]) and
                  cocycle == roof_eval(runtime, []), "V188_ABI_CANARY_REPLAY")
    context_maps = None
    nonsplit_cocycle = None
    joint_coordinate_image = None
    if runtime.get("selftest_nonsplit") is True:
        context_maps = []
        for block_index, coordinate_indices in enumerate(SEVEN_BLOCKS, 1):
            images = [{"x_image": list(TOY_CONTEXT_GENERATORS[coordinate_index][0]),
                       "y_image": list(TOY_CONTEXT_GENERATORS[coordinate_index][1])}
                      for coordinate_index in coordinate_indices]
            value_signature = sha_obj([[row["x_image"], row["y_image"]]
                                       for row in images])
            context_maps.append({"block_index": block_index,
                                 "coordinate_indices": list(coordinate_indices),
                                 "generator_images": images,
                                 "value_signature_sha256": value_signature})
        signatures = [row["value_signature_sha256"] for row in context_maps]
        value_blocks = [tuple((tuple(image["x_image"]),
                               tuple(image["y_image"]))
                              for image in row["generator_images"])
                        for row in context_maps]
        input_require(len(context_maps) == len(set(value_blocks)) ==
                      len(set(signatures)) == 7,
                      "SELFTEST_SEVEN_GENUINELY_DISTINCT_CONTEXT_MAPS")
        d_normal_forms = ([[1] * exponent for exponent in range(6)] +
                          [[1] * exponent + [2] for exponent in range(6)])
        input_require(TOY_CONTEXT_GENERATORS[0] == ((1, 0), (0, 1)) and
                      all(images[0] in ((1, 0), (5, 0)) and
                          images[1][1] == 1 and
                          len({deval_with_generators(
                              word, images[0], images[1])
                               for word in d_normal_forms}) == 12
                          for images in TOY_CONTEXT_GENERATORS),
                      "SELFTEST_TEN_GENUINE_DIC3_AUTOMORPHISMS")
        joint_values = [roof_eval(runtime, word) for word in d_normal_forms]
        input_require(len({sha_obj(value) for value in joint_values}) == 12,
                      "SELFTEST_DIC3_JOINT_COORDINATE_IMAGE_ORDER")
        q0_ids = runtime["toy_q0_ids"]
        y_quotient = qeval([2])
        yy_quotient = qmul(y_quotient, y_quotient)
        y_state = q0_ids[y_quotient]
        yy_state = q0_ids[yy_quotient]
        y_section = runtime["p176"].q0_section_word(
            y_state, runtime["parents"], runtime["letters"])
        product_section = runtime["p176"].q0_section_word(
            yy_state, runtime["parents"], runtime["letters"])
        nonsplit_value = roof_section_cocycle(
            runtime, y_section, y_section, product_section)
        canonical_product = roof_eval(runtime, product_section)
        multiplied_sections = roof_multiply(
            runtime, roof_eval(runtime, y_section), roof_eval(runtime, y_section))
        input_require(yy_quotient == tuple(range(3)) and product_section == [] and
                      multiplied_sections == roof_multiply(
                          runtime, nonsplit_value, canonical_product) and
                      nonsplit_value == roof_eval(runtime, [2, 2]) and
                      nonsplit_value != roof_eval(runtime, []),
                      "SELFTEST_NON_SPLIT_SECTION_COCYCLE")
        input_require(nonsplit_value in joint_values,
                      "SELFTEST_NON_SPLIT_COCYCLE_IN_JOINT_IMAGE")
        joint_coordinate_image = {
            "normal_forms": d_normal_forms,
            "values": joint_values,
            "distinct_value_count": len({sha_obj(value)
                                           for value in joint_values}),
            "nonsplit_value_normal_form_index": joint_values.index(
                nonsplit_value)}
        nonsplit_cocycle = {
            "quotient_left_state": y_state + 1,
            "quotient_right_state": y_state + 1,
            "quotient_product_state": yy_state + 1,
            "left_section_word": y_section, "right_section_word": y_section,
            "canonical_product_section_word": product_section,
            "value": nonsplit_value, "nontrivial": True}
    return {
        "schema": "d972-r07-v188-roof-consumer-action-abi/v1",
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
        "coordinate_ledger_sha256": sha_obj(TASK176_COORDINATES),
        "relator_rows_sha256": rows_sha256,
        "context_maps": context_maps,
        "joint_coordinate_image": joint_coordinate_image,
        "canaries": {"x": {"word": [1], "value": x},
                     "y": {"word": [2], "value": y},
                     "x_inverse": {"word": [-1], "value": x_inv},
                     "xy": {"word": [1, 2], "value": xy},
                     "source_2_2": source,
                     "x_action_y": {"actor_word": [1], "input": y,
                                    "value": action},
                      "xy_section_cocycle": {"left": [1], "right": [2],
                         "product": [1, 2], "value": cocycle},
                      "nonsplit_y_y_section_cocycle": nonsplit_cocycle}}


def validate_bridge_ledger() -> None:
    require(len(OCCURRENCE_LEDGER) == 11 and
            [row["ordinal"] for row in OCCURRENCE_LEDGER] == list(range(1, 12)),
            "occurrence ledger order")
    require([row["ten_index"] for row in OCCURRENCE_LEDGER] ==
            list(TEN_TO_ELEVEN), "occurrence insertion map")
    require([row["factor_sign"] for row in OCCURRENCE_LEDGER] ==
            [1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1],
            "occurrence signs")
    require([row["fox_prefix_occurrences"] for row in OCCURRENCE_LEDGER] ==
            [[3, 2], [3], [], [6, 5], [6], [],
             [11, 10, 9, 8], [11, 10, 9], [11, 10], [11], []],
            "occurrence Fox prefixes")
    require([row["block"] for row in OCCURRENCE_LEDGER] ==
            ["H1", "H1", "H1", "H2", "H2", "H2",
             "P1", "P2", "P3", "P5", "P4"] and
            [row["orientation"] for row in OCCURRENCE_LEDGER] ==
            ["direct" if row["factor_sign"] == 1 else "inverse"
             for row in OCCURRENCE_LEDGER],
            "occurrence blocks/sign/orientation")
    for row in OCCURRENCE_LEDGER:
        source = TASK176_COORDINATES[row["ten_index"]]
        require((row["type"], row["context_id"], row["role"]) ==
                (source["type"], source["context_id"], source["role"]),
                "occurrence typed source")


def bridge_public(runtime: dict[str, Any], task176: dict[str, Any]) -> dict[str, Any]:
    validate_bridge_ledger()
    symbolic_ten = [{"typed_coordinate": index,
                     "type": TASK176_COORDINATES[index]["type"],
                     "context_id": TASK176_COORDINATES[index]["context_id"]}
                    for index in range(10)]
    symbolic_eleven = insertion(symbolic_ten)
    symbolic_seven = regroup(symbolic_eleven)
    symbolic_left = deletion(symbolic_eleven) == symbolic_ten
    symbolic_right = insertion(deletion(symbolic_eleven)) == symbolic_eleven
    symbolic_regroup = flatten(symbolic_seven) == symbolic_eleven
    input_require(symbolic_left and symbolic_right and symbolic_regroup,
                  "BRIDGE_SYMBOLIC_BIJECTION")
    marks = (("x", [1]), ("y", [2]), ("x_inv", [-1]), ("y_inv", [-2]))
    replay = [replay_bridge_word(runtime, word, label) for label, word in marks]
    inverse_count = sum(row["left_inverse"] and row["image_inverse"] and
                        row["regroup_inverse"] for row in replay)
    input_require(inverse_count == len(replay), "BRIDGE_MARKED_INVERSES")
    ten_order = strict_int(task176["family_ALL"]["D_order"],
                           "bridge ten order", 1)
    # The insertion/deletion pair is inverse on the whole typed image, not
    # merely on the four marked samples.  Regrouping is a parenthesis-only
    # bijection, so cardinality transfers before the kernel quotient is taken.
    image_bijection = symbolic_left and symbolic_right and symbolic_regroup
    roof_order = ten_order * int(image_bijection)
    input_require(image_bijection and roof_order and ten_order % roof_order == 0,
                  "BRIDGE_ORDER_DIVISIBILITY")
    kernel_order = ten_order // roof_order
    input_require(kernel_order == 1, "BRIDGE_KERNEL_NOT_TRIVIAL")
    return {"branch": ISO, "ten_to_eleven": list(TEN_TO_ELEVEN),
            "eleven_delete_duplicate": list(ELEVEN_DELETE_DUPLICATE),
            "seven_blocks": [list(block) for block in SEVEN_BLOCKS],
            "occurrence_ledger": OCCURRENCE_LEDGER,
            "occurrence_ledger_sha256": sha_obj(OCCURRENCE_LEDGER),
            "typed_coordinate_ledger_sha256": sha_obj(TASK176_COORDINATES),
            "marked_replay": replay, "marked_replay_count": len(replay),
            "marked_inverse_count": inverse_count,
             "order_computation": {"ten_image_order": ten_order,
                                   "seven_image_order": roof_order,
                                   "kernel_order": kernel_order,
                                   "cardinality_transfer": {
                                       "typed_domain_arity": len(symbolic_ten),
                                       "occurrence_arity": len(symbolic_eleven),
                                       "block_arity": [len(row) for row in symbolic_seven],
                                       "delete_after_insert": symbolic_left,
                                       "insert_after_delete_on_image": symbolic_right,
                                       "flatten_after_regroup": symbolic_regroup}},
            "kernel_order": kernel_order, "image_order": roof_order,
            "inverse_algorithm": {
                "forward": "insert ten[0] at H2/2, regroup 3+3+1+1+1+1+1",
                "backward": "flatten, delete H2/2; retain typed E3-C21/E4-C21"}}


def fp_group_order(relators: Sequence[Sequence[int]], budget: Budget,
                   label: str) -> int:
    budget.check("sympy_factor_order:" + label)
    from sympy.combinatorics.free_groups import free_group
    from sympy.combinatorics.fp_groups import FpGroup
    free, x, y = free_group("x,y")
    generators, rows = (x, y), []
    for ordinal, relator in enumerate(relators, 1):
        value = free.identity
        for letter in strict_word(list(relator), f"{label}:{ordinal}"):
            value *= generators[abs(letter) - 1] ** (1 if letter > 0 else -1)
        rows.append(value)
        budget.bump("gamma_operations", 1, "sympy_factor_relators:" + label)
    order = int(FpGroup(free, rows).order(strategy="coset_table_based"))
    budget.check("sympy_factor_order_complete:" + label)
    return order


def q0_order_proof(runtime: dict[str, Any], budget: Budget,
                   expected_digest: str) -> tuple[list[list[int]], dict[str, Any]]:
    task157 = load_module(PINS["task157ee_source"][0], "d198_task157ee")
    q3_rel, q3_size, q3_digest = PINS["q3_receipt"]
    q3_raw = file_pin(q3_rel, q3_size, q3_digest, budget)
    try:
        q3 = json.loads(q3_raw)
    except json.JSONDecodeError as exc:
        raise InputStop("Q3_RECEIPT_JSON") from exc
    direct, relators = task157.factor_presentation(q3, runtime["old"])
    input_require(direct.get("complete_relators_sha256") == expected_digest and
                  direct.get("complete_relator_count") == 19,
                  "Q0_RELATOR_DIGEST")
    p_abstract = fp_group_order(task157.P_RELATORS, budget, "P")
    g9_abstract = fp_group_order(task157.G9_RELATORS, budget, "G9")
    direct_p = strict_int(direct.get("P_state_count"), "direct P order")
    direct_g9 = strict_int(direct.get("G9_state_count"), "direct G9 order")
    q_upper, q_image = p_abstract * g9_abstract, direct_p * direct_g9
    input_require(p_abstract == direct_p == 504 and
                  g9_abstract == direct_g9 == 2916 and
                  q_upper == q_image == Q0_ORDER,
                  "Q0_ABSTRACT_ORDER_BOUND")
    proof = {"method": "producer-owned SymPy factor orders plus direct marked-permutation enumeration",
             "factor_payload_sha256": direct.get("factor_payload_sha256"),
             "P_abstract_presentation_order": p_abstract,
             "P_direct_image_order": direct_p,
             "G9_abstract_presentation_order": g9_abstract,
             "G9_direct_image_order": direct_g9,
             "cross_commutator_count": 4,
             "marked_splitting_equation_count": 2,
             "complete_relator_count": len(relators),
             "complete_relators_sha256": sha_obj(relators),
             "Q0_presentation_order_upper_bound": q_upper,
             "Q0_marked_image_order": q_image}
    return [list(row) for row in relators], proof


def greedy_gamma_records(group: Any) -> tuple[list[int], int]:
    selected: list[int] = []
    closure = set(group.closure_ids([]))
    for index, generator in enumerate(group.generators):
        state_id = group.ids[group.key(generator)]
        if state_id not in closure:
            selected.append(index + 1)
            ids = [group.ids[group.key(group.generators[i - 1])]
                   for i in selected]
            closure = set(group.closure_ids(ids))
    return selected, len(closure)


def normal_closure_order(group: Any, seed_ids: Sequence[int],
                         budget: Budget) -> tuple[int, list[int]]:
    current = set(group.closure_ids(list(seed_ids)))
    rounds = [len(current)]
    outers = [group.eval([1]), group.eval([2])]
    while True:
        additions: set[int] = set()
        for outer in outers:
            oi = group.inverse(outer)
            for state_id in sorted(current):
                state = group.states[state_id]
                for left, right in ((oi, outer), (outer, oi)):
                    value = group.mul(group.mul(left, state), right)
                    additions.add(group.ids[group.key(value)])
                    budget.bump("gamma_operations", 1, "Gamma_normal_closure")
        enlarged = set(group.closure_ids(sorted(current | additions)))
        if enlarged == current:
            break
        current = enlarged
        rounds.append(len(current))
    return len(current), rounds


def row_iterator_for(group: Any, records_input: Sequence[Sequence[int]],
                     q0_relators: Sequence[Sequence[int]]) \
        -> Iterator[dict[str, Any]]:
    """Shared Cayley--action--lift constructor used by production and SELFTEST."""
    records = [strict_word(list(word), "record source word")
               for word in records_input]
    require(len(records) == len(group.generators), "record/generator count")
    for state in range(len(group.states)):
        source_section = list(group.section_word(state))
        for generator, source in enumerate(records):
            target = int(group.transitions[state][generator])
            target_section = list(group.section_word(target))
            yield {"layer": "Gamma_Cayley",
                   "ordinal": state * len(records) + generator + 1,
                   "state": state + 1, "generator": generator + 1,
                   "target_state": target + 1,
                   "word": reduce_word(source_section + source +
                                       inverse_word(target_section)),
                   "ancestry": {"section_source_word": source_section,
                                "record_word": source,
                                "section_target_word": target_section}}
    outer_values = [group.eval([1]), group.eval([2])]
    for record, source_value in enumerate(group.generators):
        for letter, outer in enumerate(outer_values):
            for slot, orientation in enumerate((1, -1), 1):
                if orientation == 1:
                    target_value = group.mul(group.mul(group.inverse(outer),
                                                       source_value), outer)
                    tokens = [-(letter + 1)] + records[record] + [letter + 1]
                else:
                    target_value = group.mul(group.mul(outer, source_value),
                                             group.inverse(outer))
                    tokens = [letter + 1] + records[record] + [-(letter + 1)]
                target = int(group.ids[group.key(target_value)])
                target_section = list(group.section_word(target))
                yield {"layer": "action",
                       "ordinal": record * 4 + letter * 2 + slot,
                       "record": record + 1, "letter": letter + 1,
                       "orientation": orientation, "target_state": target + 1,
                       "word": reduce_word(tokens + inverse_word(target_section)),
                       "ancestry": {"tokens": tokens,
                                    "record_word": records[record],
                                    "section_target_word": target_section}}
    for ordinal, relator in enumerate(q0_relators, 1):
        relator_word = list(relator)
        target = int(group.ids[group.key(group.eval(relator_word))])
        target_section = list(group.section_word(target))
        yield {"layer": "Q0_lift", "ordinal": ordinal,
               "target_state": target + 1,
               "word": reduce_word(relator_word + inverse_word(target_section)),
               "ancestry": {"q0_relator_word": relator_word,
                             "section_target_word": target_section}}


def row_iterator(runtime: dict[str, Any], q0_relators: Sequence[Sequence[int]]) \
        -> Iterator[dict[str, Any]]:
    group = runtime["gamma"]
    records = [list(word) for word in group.words]
    require(len(records) == 26, "record word count")
    return row_iterator_for(group, records, q0_relators)


def materialize_identity_rows(group: Any, iterator: Iterable[dict[str, Any]],
                              budget: Budget, expected_count: int,
                              prefix: Sequence[dict[str, Any]] = (),
                              state: dict[str, Any] | None = None) \
        -> list[dict[str, Any]]:
    """One production path for construction, identity replay, and resume prefix."""
    input_require(type(expected_count) is int and expected_count >= 0 and
                  type(prefix) in (list, tuple) and len(prefix) <= expected_count,
                  "PRESENTATION_MATERIALIZER_ABI")
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(iterator):
        phase = ("presentation_prefix_replay" if index < len(prefix)
                 else "presentation_construct")
        budget.preflight("presentation_rows", 1, phase)
        budget.preflight("dag_nodes", len(row["word"]) + 1,
                         "presentation_DAG_accounting")
        budget.preflight("gamma_operations", 1,
                         "presentation_identity_replay")
        input_require(group.eval(row["word"]) == group.identity,
                      "PRESENTATION_WORD_NOT_IDENTITY")
        if index < len(prefix):
            input_require(row == prefix[index], "RESUME_PREFIX_REPLAY")
        budget.bump("presentation_rows", 1, phase)
        budget.bump("dag_nodes", len(row["word"]) + 1,
                    "presentation_DAG_accounting")
        budget.bump("gamma_operations", 1, "presentation_identity_replay")
        rows.append(row)
        if state is not None:
            state["rows"] = rows
    require(len(rows) == expected_count, "complete row count")
    input_require(len(prefix) <= len(rows), "RESUME_PREFIX_RANGE")
    return rows


def replay_bridge_rows(runtime: dict[str, Any], rows: Sequence[dict[str, Any]],
                       budget: Budget, prefix_digests: Sequence[str] = (),
                       state: dict[str, Any] | None = None) -> list[str]:
    """One full-word evaluator path for production, resume, and SELFTEST."""
    input_require(type(prefix_digests) in (list, tuple) and
                  len(prefix_digests) <= len(rows), "BRIDGE_PREFIX_RANGE")
    digests: list[str] = []
    for index, row in enumerate(rows):
        phase = ("bridge_relator_prefix_replay" if index < len(prefix_digests)
                 else "bridge_relator_replay")
        budget.preflight("gamma_operations", 1, phase)
        trace = replay_bridge_word(
            runtime, row["word"], f"relator:{row['layer']}:{row['ordinal']}")
        row_digest = sha_obj(trace)
        if index < len(prefix_digests):
            input_require(row_digest == prefix_digests[index],
                          "RESUME_BRIDGE_PREFIX_REPLAY")
        digests.append(row_digest)
        budget.bump("gamma_operations", 1, phase)
        if state is not None:
            state["bridge_digests"] = digests
    return digests


def legacy_task172_rows(rows: Sequence[dict[str, Any]]) -> list[list[Any]]:
    names = {"Gamma_Cayley": "gamma_edge", "action": "xy_action",
             "Q0_lift": "q0_relator"}
    return [[names[row["layer"]], row["ordinal"], row["word"]] for row in rows]


def chunk_seals(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for start in range(0, len(rows), 1024):
        part = list(rows[start:start + 1024])
        result.append({"start": start, "end": start + len(part),
                       "sealed": len(part) > 0, "prefix_complete": True,
                       "sha256": sha_obj(part)})
    return result


CHECKPOINT_KEYS = {
    "schema", "sealed", "stage", "cursor", "bridge_cursor", "rows",
    "rows_sha256", "bridge_digests", "bridge_replay_sha256", "chunks", "dag_nodes",
    "input_binding", "q0_transition_sha256", "selected_gamma_records",
    "task172_roster_sha256", "total_rows", "limits", "counters", "resumed_from",
    "seal_sha256",
}
RESUMED_FROM_KEYS = {"path", "bytes", "sha256", "seal_sha256", "cursor",
                     "bridge_cursor", "manifest_path", "manifest_bytes",
                     "manifest_sha256", "manifest_self_digest_sha256"}
RESUME_MANIFEST_KEYS = {"schema", "checkpoint_path", "checkpoint_bytes",
                        "checkpoint_sha256", "checkpoint_seal_sha256",
                        "cursor", "bridge_cursor", "self_digest_sha256"}


def seal_checkpoint(body: dict[str, Any]) -> dict[str, Any]:
    value = dict(body)
    value.pop("seal_sha256", None)
    value["seal_sha256"] = sha_obj(value)
    return value


def validate_checkpoint_shape(value: Any,
                              total_rows: int = PRESENTATION_ROWS) -> dict[str, Any]:
    input_require(type(total_rows) is int and total_rows >= 0,
                  "CHECKPOINT_TOTAL_ROWS")
    input_require(type(value) is dict and set(value) == CHECKPOINT_KEYS,
                  "CHECKPOINT_KEYS")
    body = dict(value)
    claimed = body.pop("seal_sha256")
    input_require(type(claimed) is str and claimed == sha_obj(body),
                  "CHECKPOINT_SEAL")
    input_require(value["schema"] == CHECKPOINT_SCHEMA and
                  value["sealed"] is True and
                  value["stage"] in ("presentation", "bridge_replay"),
                  "CHECKPOINT_ENVELOPE")
    cursor = strict_int(value["cursor"], "checkpoint cursor", 0)
    bridge_cursor = strict_int(value["bridge_cursor"],
                               "checkpoint bridge cursor", 0)
    input_require(strict_int(value["total_rows"], "checkpoint total rows", 0) ==
                  total_rows and type(value["rows"]) is list and
                  cursor == len(value["rows"]) and
                   cursor <= total_rows and bridge_cursor <= cursor and
                  value["rows_sha256"] == sha_obj(value["rows"]) and
                  strict_int(value["dag_nodes"], "checkpoint DAG", 0) ==
                  sum(len(strict_word(row.get("word"), "checkpoint row word")) + 1
                      for row in value["rows"] if type(row) is dict) and
                  all(type(row) is dict for row in value["rows"]),
                  "CHECKPOINT_PREFIX")
    input_require(type(value["bridge_digests"]) is list and
                  len(value["bridge_digests"]) == bridge_cursor and
                  all(type(row) is str for row in value["bridge_digests"]) and
                  value["bridge_replay_sha256"] ==
                  sha_obj(value["bridge_digests"]) and
                  type(value["chunks"]) is list and
                  value["chunks"] == chunk_seals(value["rows"]),
                  "CHECKPOINT_CHUNKS")
    input_require(type(value["input_binding"]) is dict and
                  type(value["limits"]) is dict and
                  set(value["limits"]) == {"wall_seconds", "rss_bytes", *RESOURCE_COUNTERS} and
                  type(value["counters"]) is dict and
                  set(value["counters"]) == set(RESOURCE_COUNTERS),
                  "CHECKPOINT_RESOURCE_SHAPE")
    input_require(type(value["q0_transition_sha256"]) is str and
                  type(value["task172_roster_sha256"]) is str and
                  type(value["selected_gamma_records"]) is list and
                  all(type(row) is int and row >= 1
                      for row in value["selected_gamma_records"]) and
                  ((value["stage"] == "presentation" and
                    cursor < total_rows and bridge_cursor == 0) or
                   (value["stage"] == "bridge_replay" and
                    cursor == total_rows)),
                  "CHECKPOINT_AUTHENTICATED_STATE")
    if value["resumed_from"] is not None:
        prior = value["resumed_from"]
        input_require(type(prior) is dict and set(prior) == RESUMED_FROM_KEYS and
                      type(prior["path"]) is str and
                      (prior["path"].startswith("ci/in/") or
                       prior["path"].startswith("ci/out/d972_r07_seven_context_roof_presentation_selftest.")) and
                      type(prior["bytes"]) is int and prior["bytes"] > 0 and
                      type(prior["sha256"]) is str and
                      type(prior["seal_sha256"]) is str and
                      type(prior["cursor"]) is int and
                      type(prior["bridge_cursor"]) is int and
                      type(prior["manifest_path"]) is str and
                      type(prior["manifest_bytes"]) is int and
                      prior["manifest_bytes"] > 0 and
                      type(prior["manifest_sha256"]) is str and
                      type(prior["manifest_self_digest_sha256"]) is str and
                      0 <= prior["bridge_cursor"] <= prior["cursor"] <=
                       total_rows,
                      "CHECKPOINT_RESUMED_FROM")
    input_require(type(value["limits"]["wall_seconds"]) in (int, float) and
                  type(value["limits"]["rss_bytes"]) is int and
                  value["limits"]["wall_seconds"] > 0 and
                  value["limits"]["rss_bytes"] >= 0,
                  "CHECKPOINT_RESOURCE_LIMITS")
    for name in RESOURCE_COUNTERS:
        strict_int(value["limits"][name], "checkpoint limit:" + name, 0)
        strict_int(value["counters"][name], "checkpoint counter:" + name, 0)
        input_require(value["counters"][name] <= value["limits"][name],
                      "CHECKPOINT_COUNTER_OVER_LIMIT:" + name)
    return value


def checkpoint_body(state: dict[str, Any], budget: Budget) -> dict[str, Any]:
    rows = list(state.get("rows", []))
    bridge_digests = list(state.get("bridge_digests", []))
    return {"schema": CHECKPOINT_SCHEMA, "sealed": True,
            "stage": ("bridge_replay" if state.get("presentation_complete")
                      else "presentation"),
            "cursor": len(rows), "bridge_cursor": len(bridge_digests),
            "rows": rows, "rows_sha256": sha_obj(rows),
            "bridge_digests": bridge_digests,
            "bridge_replay_sha256": sha_obj(bridge_digests),
            "chunks": chunk_seals(rows),
            "dag_nodes": sum(len(row["word"]) + 1 for row in rows),
            "input_binding": state["input_binding"],
            "q0_transition_sha256": state["q0_transition_sha256"],
            "selected_gamma_records": state["selected_gamma_records"],
            "task172_roster_sha256": state["task172_roster_sha256"],
            "total_rows": state.get("total_rows", PRESENTATION_ROWS),
            "limits": dict(budget.limits), "counters": dict(budget.counters),
            "resumed_from": state.get("resumed_from")}


def counted_checkpoint(state: dict[str, Any], budget: Budget,
                       optional: bool = False) -> tuple[dict[str, Any], bytes] | None:
    """Seal a checkpoint and charge its exact self-referential byte length."""
    base, prospective = budget.counters["checkpoint_bytes"], 0
    for _ in range(32):
        target = base + prospective
        if target > budget.limits["checkpoint_bytes"]:
            budget.counters["checkpoint_bytes"] = base
            if optional:
                return None
            raise ResourceStop("checkpoint_serialization", "checkpoint_bytes",
                               target, budget.limits["checkpoint_bytes"])
        budget.counters["checkpoint_bytes"] = target
        value = seal_checkpoint(checkpoint_body(state, budget))
        raw = canonical(value)
        if len(raw) == prospective:
            validate_checkpoint_shape(
                value, state.get("total_rows", PRESENTATION_ROWS))
            return value, raw
        prospective = len(raw)
    budget.counters["checkpoint_bytes"] = base
    raise RuntimeError("checkpoint byte-accounting fixed point did not stabilize")


def safe_runtime_path(text: str, roots: tuple[str, ...], label: str) -> Path:
    path = Path(text)
    if path.is_absolute() or ".." in path.parts or not any(
            path.as_posix().startswith(root) for root in roots):
        raise InputStop(label + "_PATH")
    return path


def write_checkpoint(state: dict[str, Any], budget: Budget,
                     path_text: str | None) -> dict[str, Any] | None:
    if not state.get("checkpoint_ready") or path_text is None:
        return None
    path = safe_runtime_path(path_text, ("ci/out/",), "CHECKPOINT_OUTPUT")
    counted = counted_checkpoint(state, budget, optional=True)
    if counted is None:
        return None
    value, raw = counted
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return {"path": path.as_posix(), "bytes": len(raw),
            "sha256": sha_bytes(raw), "cursor": value["cursor"],
            "bridge_cursor": value["bridge_cursor"],
            "seal_sha256": value["seal_sha256"]}


def resume_manifest(binding: dict[str, Any],
                    future_checkpoint_path: str) -> dict[str, Any]:
    input_require(type(binding) is dict and set(binding) ==
                  {"path", "bytes", "sha256", "cursor", "bridge_cursor",
                   "seal_sha256"}, "RESUME_MANIFEST_BINDING")
    future = safe_runtime_path(
        future_checkpoint_path,
        ("ci/in/", "ci/out/d972_r07_seven_context_roof_presentation_selftest."),
        "FUTURE_RESUME_CHECKPOINT")
    input_require(future.as_posix() != binding["path"],
                  "RESUME_MANIFEST_REQUIRES_PORTABLE_STAGE")
    value = {"schema": RESUME_MANIFEST_SCHEMA,
             "checkpoint_path": future.as_posix(),
             "checkpoint_bytes": binding["bytes"],
             "checkpoint_sha256": binding["sha256"],
             "checkpoint_seal_sha256": binding["seal_sha256"],
             "cursor": binding["cursor"],
             "bridge_cursor": binding["bridge_cursor"]}
    value["self_digest_sha256"] = sha_obj(value)
    return value


def write_resume_manifest(binding: dict[str, Any], path_text: str,
                          future_checkpoint_path: str) -> dict[str, Any]:
    path = safe_runtime_path(path_text, ("ci/out/",), "RESUME_MANIFEST_OUTPUT")
    value, raw = resume_manifest(binding, future_checkpoint_path), b""
    raw = canonical(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return {"path": path.as_posix(), "bytes": len(raw),
            "sha256": sha_bytes(raw),
            "self_digest_sha256": value["self_digest_sha256"],
            "future_checkpoint_path": value["checkpoint_path"]}


def load_resume(path_text: str | None, manifest_text: str | None,
                budget: Budget, total_rows: int = PRESENTATION_ROWS,
                allow_output: bool = False) \
        -> tuple[dict[str, Any], dict[str, Any]] | None:
    if path_text is None:
        input_require(manifest_text is None, "RESUME_MANIFEST_WITHOUT_CHECKPOINT")
        return None
    input_require(type(manifest_text) is str, "RESUME_MANIFEST_REQUIRED")
    roots = (("ci/in/", "ci/out/d972_r07_seven_context_roof_presentation_selftest.")
             if allow_output else ("ci/in/",))
    path = safe_runtime_path(path_text, roots, "RESUME")
    manifest_path = safe_runtime_path(manifest_text, roots, "RESUME_MANIFEST")
    input_require(path != manifest_path, "RESUME_MANIFEST_PATH_ALIAS")
    raw = checked_read(ROOT / path, budget, "resume_checkpoint_read")
    budget.bump("checkpoint_bytes", len(raw), "resume_checkpoint_replay")
    try:
        parsed = json.loads(raw)
        input_require(raw == canonical(parsed), "RESUME_CHECKPOINT_CANONICAL")
        checkpoint = validate_checkpoint_shape(parsed, total_rows)
    except json.JSONDecodeError as exc:
        raise InputStop("RESUME_CHECKPOINT_JSON") from exc
    manifest_raw = checked_read(ROOT / manifest_path, budget,
                                "resume_manifest_read")
    try:
        manifest = json.loads(manifest_raw)
    except json.JSONDecodeError as exc:
        raise InputStop("RESUME_MANIFEST_JSON") from exc
    input_require(manifest_raw == canonical(manifest) and
                  type(manifest) is dict and
                  set(manifest) == RESUME_MANIFEST_KEYS and
                  manifest.get("schema") == RESUME_MANIFEST_SCHEMA,
                  "RESUME_MANIFEST_ENVELOPE")
    manifest_self_digest = validate_self_digest(
        manifest, "self_digest_sha256", "RESUME_MANIFEST")
    input_require(manifest["checkpoint_path"] == path.as_posix() and
                  manifest["checkpoint_bytes"] == len(raw) and
                  manifest["checkpoint_sha256"] == sha_bytes(raw) and
                  manifest["checkpoint_seal_sha256"] ==
                  checkpoint["seal_sha256"] and
                  manifest["cursor"] == checkpoint["cursor"] and
                  manifest["bridge_cursor"] == checkpoint["bridge_cursor"],
                  "RESUME_MANIFEST_CHECKPOINT_BINDING")
    budget.resumed_from_limits = dict(checkpoint["limits"])
    for name in RESOURCE_COUNTERS:
        prior = checkpoint["counters"][name]
        if prior > budget.limits[name]:
            raise ResourceStop("resume_preflight", name, prior,
                               budget.limits[name])
    identity = {"path": path.as_posix(), "bytes": len(raw),
                "sha256": sha_bytes(raw),
                "seal_sha256": checkpoint["seal_sha256"],
                "cursor": checkpoint["cursor"],
                "bridge_cursor": checkpoint["bridge_cursor"],
                "manifest_path": manifest_path.as_posix(),
                "manifest_bytes": len(manifest_raw),
                "manifest_sha256": sha_bytes(manifest_raw),
                "manifest_self_digest_sha256": manifest_self_digest}
    return checkpoint, identity


def compact_presentation(runtime: dict[str, Any], budget: Budget,
                         q0_relators: Sequence[Sequence[int]],
                         q0_proof: dict[str, Any], task172: dict[str, Any],
                         task176_order: int, state: dict[str, Any],
                         resume: dict[str, Any] | None) -> dict[str, Any]:
    group = runtime["gamma"]
    selected, selected_order = greedy_gamma_records(group)
    input_require(selected_order == GAMMA_ORDER, "GAMMA_SELECTED_GENERATION")
    state["selected_gamma_records"] = selected
    if resume is not None:
        input_require(resume["selected_gamma_records"] == selected,
                      "RESUME_SELECTED_GAMMA")
    prefix = [] if resume is None else resume["rows"]
    rows = materialize_identity_rows(
        group, row_iterator(runtime, q0_relators), budget, PRESENTATION_ROWS,
        prefix, state)
    state["presentation_complete"] = True
    layers = {name: sum(row["layer"] == name for row in rows)
              for name in ("Gamma_Cayley", "action", "Q0_lift")}
    input_require(layers == {"Gamma_Cayley": 6318, "action": 104,
                             "Q0_lift": 19}, "PRESENTATION_LAYER_COUNTS")
    legacy_digest = sha_obj(legacy_task172_rows(rows))
    input_require(legacy_digest == task172["relation_roster"]["roster_sha256"],
                  "TASK172_ROSTER_SHA_BINDING")
    state["task172_roster_sha256"] = legacy_digest
    record_ids = [group.ids[group.key(value)] for value in group.generators]
    q_defect_ids = [group.ids[group.key(group.eval(relator))]
                    for relator in q0_relators]
    defect_order, defect_rounds = normal_closure_order(group, q_defect_ids,
                                                       budget)
    q0_upper = q0_proof["Q0_presentation_order_upper_bound"]
    total_upper = len(group.states) * q0_upper
    normal_generation = (
        len(group.closure_ids(record_ids)) == GAMMA_ORDER and
        defect_order == GAMMA_ORDER and
        layers == {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19} and
        q0_upper == Q0_ORDER and total_upper == task176_order == DELTA_ORDER)
    input_require(normal_generation, "V190_ORDER_BOUND")
    proof = {"theorem": "v190 Cayley--action--lift order bound",
             "selected_gamma_records": selected,
             "selected_gamma_closure_order": selected_order,
             "all_record_generator_closure_order": len(group.closure_ids(record_ids)),
             "Gamma_cayley_state_count": len(group.states),
             "Gamma_cayley_edge_count": layers["Gamma_Cayley"],
             "marked_action_loop_count": layers["action"],
             "Q0_lift_count": layers["Q0_lift"],
             "Q0_order_proof": q0_proof,
             "Q0_defect_normal_closure_order": defect_order,
             "Q0_defect_normal_closure_rounds": defect_rounds,
             "presentation_quotient_order_upper_bound": total_upper,
             "surjective_marked_image_order": task176_order,
             "upper_bound_equals_image_order": total_upper == task176_order,
             "normal_closure_exact": normal_generation}
    return {"row_count": len(rows), "layer_counts": layers,
            "rows": rows, "rows_sha256": sha_obj(rows),
            "task172_legacy_rows_sha256": legacy_digest,
            "chunks": chunk_seals(rows), "resume_cursor": len(rows),
            "normal_generation": normal_generation,
            "normal_closure_exact": normal_generation,
            "normal_generation_proof": proof,
            "source_word_encoding":
                "literal strict signed F2 words; empty Cayley tree loops retained"}


def input_binding(task176: dict[str, Any], task157: dict[str, Any],
                  task172: dict[str, Any], pins: dict[str, Any]) -> dict[str, Any]:
    return {"task176_receipt_sha256": task176["receipt_sha256"],
            "task176_manifest_sha256": task176["manifest_sha256"],
            "task157ee_receipt_sha256": task157["sha256"],
            "task172_receipt_sha256": task172["sha256"],
            "task172_roster_sha256": task172["relation_roster"]["roster_sha256"],
            "task179_source_sha256": pins["task179_producer"]["sha256"],
            "predecessor_dependency_cone_sha256":
                pins["normalized_predecessor_dependency_cone"]["members_sha256"],
            "proof145_sha256": pins["proof145"]["sha256"],
            "proof168_sha256": pins["proof168"]["sha256"],
            "proof173_sha256": pins["proof173"]["sha256"],
            "proof184_sha256": pins["proof184"]["sha256"],
            "proof188_sha256": pins["proof188"]["sha256"],
            "proof189_sha256": pins["proof189"]["sha256"],
            "proof190_sha256": pins["proof190"]["sha256"]}


def finalize_receipt(result: dict[str, Any], budget: Budget) -> dict[str, Any]:
    budget.check("final_receipt_preflight")
    base, prospective = budget.counters["serialized_bytes"], 0
    resource_snapshot = budget.public()
    for _ in range(32):
        target = base + prospective
        if target > budget.limits["serialized_bytes"]:
            raise ResourceStop("final_receipt", "serialized_bytes", target,
                               budget.limits["serialized_bytes"])
        budget.counters["serialized_bytes"] = target
        resource_snapshot["phase"] = "final_receipt"
        resource_snapshot["counters"] = dict(budget.counters)
        result["resource"] = resource_snapshot
        result.pop("self_digest_sha256", None)
        result["self_digest_sha256"] = sha_obj(result)
        size = len(canonical(result))
        if size == prospective:
            return result
        prospective = size
    raise RuntimeError("final receipt byte-accounting fixed point did not stabilize")


def make_production(args: argparse.Namespace) -> dict[str, Any]:
    budget = Budget(args)
    state: dict[str, Any] = {"rows": [], "bridge_digests": [],
                             "presentation_complete": False,
                             "checkpoint_ready": False,
                             "total_rows": (9 if getattr(args, "selftest_profile", False)
                                            else PRESENTATION_ROWS)}
    checkpoint_path = args.checkpoint
    if checkpoint_path is None and args.output:
        checkpoint_path = args.output + ".checkpoint.json"
    checkpoint_manifest_output = getattr(args, "checkpoint_manifest_output", None)
    future_resume_checkpoint = getattr(args, "future_resume_checkpoint", None)
    if checkpoint_path is None:
        input_require(checkpoint_manifest_output is None and
                      future_resume_checkpoint is None,
                      "CHECKPOINT_PORTABLE_PAIR_WITHOUT_CHECKPOINT")
    else:
        input_require(type(checkpoint_manifest_output) is str and
                      type(future_resume_checkpoint) is str,
                      "CHECKPOINT_PORTABLE_PAIR_REQUIRED")
        checkpoint_output = safe_runtime_path(
            checkpoint_path, ("ci/out/",), "CHECKPOINT_OUTPUT")
        manifest_output = safe_runtime_path(
            checkpoint_manifest_output, ("ci/out/",),
            "RESUME_MANIFEST_OUTPUT")
        future_roots = (("ci/in/",
                         "ci/out/d972_r07_seven_context_roof_presentation_selftest.")
                        if getattr(args, "selftest_profile", False)
                        else ("ci/in/",))
        future_output = safe_runtime_path(
            future_resume_checkpoint, future_roots,
            "FUTURE_RESUME_CHECKPOINT")
        input_require(len({checkpoint_output.as_posix(), manifest_output.as_posix(),
                           future_output.as_posix()}) == 3,
                      "CHECKPOINT_PORTABLE_PATH_ALIAS")
        input_require(not (ROOT / checkpoint_output).exists() and
                      not (ROOT / manifest_output).exists(),
                      "CHECKPOINT_PORTABLE_STALE_OUTPUT")
    try:
        resume_loaded = load_resume(
            args.resume, getattr(args, "resume_manifest", None), budget,
            state["total_rows"], getattr(args, "selftest_profile", False))
        resume = None if resume_loaded is None else resume_loaded[0]
        resume_identity = None if resume_loaded is None else resume_loaded[1]
        # This check-only reservation is deliberately before any predecessor
        # roster/runtime reconstruction.  The row loop below performs the one
        # and only live charge, so preflight and construction are not doubled.
        budget.preflight("presentation_rows", state["total_rows"],
                         "presentation_roster_preflight")
        if getattr(args, "selftest_profile", False):
            return make_selftest_production(
                args, budget, state, resume, resume_identity, checkpoint_path)
        pins = authenticate_sources(budget)
        task176 = authenticate_task176_receipt(Path(args.task176_receipt), budget)
        task157 = authenticate_task157ee_receipt(budget)
        task172 = authenticate_task172_receipt(budget)
        binding = input_binding(task176, task157, task172, pins)
        if resume is not None:
            input_require(resume["input_binding"] == binding and
                          resume["task172_roster_sha256"] ==
                          task172["relation_roster"]["roster_sha256"],
                          "RESUME_INPUT_BINDING")
            input_require(resume_identity is not None,
                          "RESUME_IDENTITY_MISSING")
            state["resumed_from"] = resume_identity
        else:
            state["resumed_from"] = None
        state["input_binding"] = binding
        state["task172_roster_sha256"] = task172["relation_roster"]["roster_sha256"]
        runtime = load_runtime(budget)
        runtime["abi_budget"] = budget
        q0_public = runtime_q0_payload(runtime, task176)
        state["q0_transition_sha256"] = q0_public["parent_letter_transition_sha256"]
        if resume is not None:
            input_require(resume["q0_transition_sha256"] ==
                          state["q0_transition_sha256"],
                          "RESUME_Q0_TRANSITION")
        bridge = bridge_public(runtime, task176)
        q0_relators, q0_proof = q0_order_proof(
            runtime, budget, task157["complete_relators_sha256"])
        selected, selected_order = greedy_gamma_records(runtime["gamma"])
        input_require(selected_order == GAMMA_ORDER, "GAMMA_SELECTION_PRECHECK")
        state["selected_gamma_records"] = selected
        state["checkpoint_ready"] = True
        presentation = compact_presentation(
            runtime, budget, q0_relators, q0_proof, task172,
            task176["family_ALL"]["D_order"], state, resume)
        prior_bridge_cursor = 0 if resume is None else resume["bridge_cursor"]
        bridge_digests = replay_bridge_rows(
            runtime, presentation["rows"], budget,
            prefix_digests=(() if resume is None else resume["bridge_digests"]),
            state=state)
        if resume is not None:
            input_require(sha_obj(bridge_digests[:prior_bridge_cursor]) ==
                          resume["bridge_replay_sha256"],
                          "RESUME_BRIDGE_PREFIX_DIGEST")
        bridge["relator_replay"] = {
            "count": len(bridge_digests),
            "digest_sha256": sha_obj(bridge_digests),
            "all_left_and_right_inverses": len(bridge_digests) == PRESENTATION_ROWS}
        input_require(bridge["relator_replay"]["all_left_and_right_inverses"],
                      "BRIDGE_ALL_RELATORS")
        evaluator = consumer_abi_public(runtime, presentation["rows_sha256"])
        counted = counted_checkpoint(state, budget)
        require(counted is not None, "complete checkpoint accounting")
        resume_full, _ = counted
        resume_summary = {"schema": CHECKPOINT_SCHEMA, "sealed": True,
            "cursor": resume_full["cursor"],
            "bridge_cursor": resume_full["bridge_cursor"],
            "rows_sha256": resume_full["rows_sha256"],
            "bridge_digests": resume_full["bridge_digests"],
            "bridge_replay_sha256": resume_full["bridge_replay_sha256"],
            "chunks_sha256": sha_obj(resume_full["chunks"]),
            "input_binding": resume_full["input_binding"],
            "q0_transition_sha256": resume_full["q0_transition_sha256"],
            "selected_gamma_records": resume_full["selected_gamma_records"],
            "task172_roster_sha256": resume_full["task172_roster_sha256"],
            "full_checkpoint_seal_sha256": resume_full["seal_sha256"],
            "full_checkpoint_stage": resume_full["stage"],
            "full_checkpoint_total_rows": resume_full["total_rows"],
            "full_checkpoint_dag_nodes": resume_full["dag_nodes"],
            "full_checkpoint_limits": resume_full["limits"],
            "full_checkpoint_counters": resume_full["counters"],
            "resumed_from": state["resumed_from"]}
        result = {"schema": SCHEMA, "status": "COMPLETE", "terminal": ISO,
            "input": {"task176": task176, "task157ee": task157,
                      "task172": task172, "task179": pins["task179_producer"],
                      "sources": pins},
            "bridge": bridge, "Q0": q0_public,
            "Gamma": {"order": GAMMA_ORDER,
                      "cayley_state_count": len(runtime["gamma"].states),
                      "selected_record_generators": selected},
            "D_all": {"order": task176["family_ALL"]["D_order"],
                      "order_source": "task176 result.families.ALL.D_order",
                      "materialized": False},
            "Delta0": {"order": bridge["image_order"],
                       "marked_generators": {"x": [1], "y": [2]},
                       "presentation": presentation,
                       "normal_closure_exact": presentation["normal_closure_exact"]},
            "evaluator": evaluator,
            "resume": resume_summary,
            "direct_Delta_states_enumerated": 0,
            "million_row_Q0_Schreier_stream": "SUPERSEDED_NOT_USED",
            "cofinal_lift": False, "fake": False, "Ihara_witness": False}
        return finalize_receipt(result, budget)
    except ResourceStop as exc:
        budget.phase = exc.phase
        exc.checkpoint_binding = write_checkpoint(state, budget, checkpoint_path)
        exc.checkpoint_manifest_binding = (
            None if exc.checkpoint_binding is None else write_resume_manifest(
                exc.checkpoint_binding, checkpoint_manifest_output,
                future_resume_checkpoint))
        exc.checkpoint_unavailable_reason = (None if exc.checkpoint_binding is not None
                                             else "checkpoint_bytes_cap_or_unready")
        exc.snapshot = budget.public()
        raise


# ----------------------------- linked SELFTEST -----------------------------

def qmul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[index]] for index in range(3))


def qinv(a: tuple[int, ...]) -> tuple[int, ...]:
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
    raise RuntimeError("toy inverse")


def deval(word: Sequence[int]) -> tuple[int, int]:
    return deval_with_generators(word, (1, 0), (0, 1))


def deval_with_generators(word: Sequence[int], x_image: tuple[int, int],
                          y_image: tuple[int, int]) -> tuple[int, int]:
    generators = {1: x_image, 2: y_image}
    value = (0, 0)
    for letter in strict_word(list(word), "toy D word"):
        generator = generators[abs(letter)]
        value = dmul(value, generator if letter > 0 else dinv(generator))
    return value


# Ten genuine automorphisms of Dic_3=<a,b|a^6=1,b^2=a^3,bab^-1=a^-1>.
# Each pair encodes a |-> a^u and b |-> a^v*b, with u in {1,-1 mod 6};
# coordinate zero is the identity.  The seven block signatures below use only
# these image values, never coordinate numbers or receipt tags.
TOY_CONTEXT_GENERATORS = (
    ((1, 0), (0, 1)), ((1, 0), (1, 1)), ((1, 0), (2, 1)),
    ((1, 0), (3, 1)), ((1, 0), (4, 1)), ((1, 0), (5, 1)),
    ((5, 0), (0, 1)), ((5, 0), (1, 1)), ((5, 0), (2, 1)),
    ((5, 0), (3, 1)),
)


def qof(value: tuple[int, int]) -> tuple[int, ...]:
    r, s = (1, 2, 0), (1, 0, 2)
    answer = tuple(range(3))
    for _ in range(value[0] % 3):
        answer = qmul(answer, r)
    if value[1]:
        answer = qmul(answer, s)
    return answer


def qeval(word: Sequence[int]) -> tuple[int, ...]:
    generators = {1: (1, 2, 0), 2: (1, 0, 2)}
    value = tuple(range(3))
    for letter in strict_word(list(word), "toy Q word"):
        generator = generators[abs(letter)]
        value = qmul(value, generator if letter > 0 else qinv(generator))
    return value


class ToyGammaGroup:
    """The central C2 kernel inside the non-split Dic_3 -> S3 extension."""
    def __init__(self) -> None:
        self.identity = (0, 0)
        self.states = [(0, 0), (3, 0)]
        self.ids = {state: index for index, state in enumerate(self.states)}
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
        input_require(type(state) is int and 0 <= state < len(self.states),
                      "TOY_GAMMA_SECTION_STATE")
        return [] if state == 0 else list(self.words[0])

    @staticmethod
    def closure_ids(seed_ids: Sequence[int]) -> set[int]:
        input_require(all(type(value) is int and value in (0, 1)
                          for value in seed_ids), "TOY_GAMMA_CLOSURE_SEEDS")
        return {0, 1} if 1 in seed_ids else {0}


class ToyP176:
    """Typed ten-coordinate adapter exposing the real task176 consumer ABI."""
    COORDINATE_WIDTHS = (3,) * 10

    def __init__(self) -> None:
        self.eval_calls = 0

    @staticmethod
    def encode(index: int, value: tuple[int, int]) -> bytes:
        input_require(type(index) is int and 0 <= index < 10,
                      "TOY_COORDINATE_INDEX")
        return bytes((index, value[0], value[1]))

    @staticmethod
    def decode(raw: bytes, index: int) -> tuple[int, int]:
        input_require(type(raw) is bytes and len(raw) == 3 and raw[0] == index and
                      raw[1] < 6 and raw[2] < 2, "TOY_TYPED_COORDINATE")
        return raw[1], raw[2]

    def eval_word_coordinates(self, old: Any, e3: Any, e4: Any,
                              contexts: Any, delete: Any,
                              word: Sequence[int]) -> tuple[bytes, ...]:
        del old, e3, e4, contexts, delete
        self.eval_calls += 1
        return tuple(self.encode(index, self.eval_coordinate(index, word))
                     for index in range(10))

    @staticmethod
    def eval_coordinate(index: int, word: Sequence[int]) -> tuple[int, int]:
        input_require(type(index) is int and 0 <= index < 10,
                      "TOY_CONTEXT_INDEX")
        x_image, y_image = TOY_CONTEXT_GENERATORS[index]
        return deval_with_generators(word, x_image, y_image)

    @staticmethod
    def blob(old: Any, value: Any) -> bytes:
        del old
        input_require(type(value) is bytes and len(value) == 3,
                      "TOY_BLOB_REPRESENTATION")
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

    @staticmethod
    def q0_section_word(state: int, parents: Sequence[int],
                        letters: bytes) -> list[int]:
        out: list[int] = []
        while state:
            out.append(int(letters[state]))
            state = int(parents[state])
        out.reverse()
        return out

    @staticmethod
    def section_row(stores: Sequence[Sequence[bytes]], state: int) \
            -> tuple[bytes, ...]:
        return tuple(store[state] for store in stores)


def toy_args(**overrides: Any) -> argparse.Namespace:
    values = {"seconds": 60.0, "rss_bytes": 2_000_000_000,
        "q0_states": 6, "q0_edges": 12, "presentation_rows": 9,
        "gamma_operations": 2_000, "dag_nodes": 1_000,
        "serialized_bytes": 2_000_000, "checkpoint_bytes": 1_000_000,
        "task176_receipt": None, "resume": None, "resume_manifest": None,
        "checkpoint": None, "checkpoint_manifest_output": None,
        "future_resume_checkpoint": None, "output": None,
        "selftest_profile": True,
        "selftest_evidence": None}
    values.update(overrides)
    return argparse.Namespace(**values)


def toy_q0(budget: Budget) -> dict[str, Any]:
    budget.preflight("q0_states", 6, "toy_Q0_known_state_preflight")
    budget.preflight("q0_edges", 12, "toy_Q0_known_edge_preflight")
    identity = tuple(range(3))
    states, ids = [identity], {identity: 0}
    parents, letters, transitions = [0], [0], []
    head = 0
    while head < len(states):
        state_id, state = head, states[head]
        head += 1
        row: list[int] = []
        for letter in (1, 2):
            target = qmul(state, qeval([letter]))
            if target not in ids:
                ids[target] = len(states)
                states.append(target)
                parents.append(state_id)
                letters.append(letter)
            row.append(ids[target] + 1)
        transitions.append(row)
        budget.check("toy_Q0_BFS")
    budget.bump("q0_states", len(states), "toy_Q0_complete_states")
    budget.bump("q0_edges", sum(len(row) for row in transitions),
                "toy_Q0_complete_edges")
    input_require(len(states) == len(transitions) == 6,
                  "TOY_Q0_COMPLETE_BFS")
    public_parents = [0] + [parents[index] + 1 for index in range(1, len(parents))]
    return {"states": states, "ids": ids, "parents": parents,
            "public_parents": public_parents, "letters": bytes(letters),
            "public_letters": letters, "transitions": transitions}


def toy_runtime(group: ToyGammaGroup, q0: dict[str, Any],
                budget: Budget) -> dict[str, Any]:
    p176 = ToyP176()
    q0_words = [p176.q0_section_word(index, q0["parents"], q0["letters"])
                for index in range(len(q0["states"]))]
    stores = [[p176.encode(index, p176.eval_coordinate(index, word))
               for word in q0_words]
              for index in range(10)]
    projected = [tuple(p176.encode(
        index, p176.eval_coordinate(index, group.section_word(state_id)))
        for index in range(10)) for state_id in range(len(group.states))]
    return {"p176": p176, "old": None, "e3": None, "e4": None,
            "contexts": (), "delete": None, "gamma": group,
            "parents": q0["parents"], "letters": q0["letters"],
            "stores": stores, "projected": projected,
            "toy_q0_ids": q0["ids"], "selftest_nonsplit": True,
            "abi_budget": budget}


def toy_d_order() -> int:
    seen, queue = {(0, 0)}, [(0, 0)]
    for state in queue:
        for generator in ((1, 0), (0, 1)):
            target = dmul(state, generator)
            if target not in seen:
                seen.add(target)
                queue.append(target)
    input_require(all(dmul(value, dinv(value)) == (0, 0) for value in seen),
                  "TOY_D_INVERSE_CLOSURE")
    return len(seen)


def reseal_toy(value: dict[str, Any]) -> dict[str, Any]:
    value.pop("self_digest_sha256", None)
    value["self_digest_sha256"] = sha_obj(value)
    return value


def finalize_toy(value: dict[str, Any], budget: Budget) -> dict[str, Any]:
    base, prospective = budget.counters["serialized_bytes"], 0
    budget.check("toy_complete")
    resource_snapshot = budget.public()
    for _ in range(32):
        target = base + prospective
        if target > budget.limits["serialized_bytes"]:
            raise ResourceStop("toy_receipt", "serialized_bytes", target,
                               budget.limits["serialized_bytes"])
        budget.counters["serialized_bytes"] = target
        resource_snapshot["counters"] = dict(budget.counters)
        value["resource"] = resource_snapshot
        reseal_toy(value)
        raw = canonical(value)
        if len(raw) == prospective:
            return value
        prospective = len(raw)
    raise RuntimeError("toy receipt byte-accounting fixed point did not stabilize")


def toy_input_binding() -> dict[str, Any]:
    cone = dependency_cone_manifest()
    return {"toy": "Dic3-S3-v4-production-path", "typed_coordinates": 10,
            "predecessor_dependency_cone_sha256": cone["members_sha256"]}


def toy_roster_digest() -> str:
    return sha_obj({"schema": SELFTEST_SCHEMA + "/row-roster/v1",
                    "row_count": 9,
                    "layer_counts": {"Gamma_Cayley": 2, "action": 4,
                                     "Q0_lift": 3}})


def make_selftest_production(args: argparse.Namespace, budget: Budget,
        state: dict[str, Any], resume: dict[str, Any] | None,
        resume_identity: dict[str, Any] | None,
        checkpoint_path: str | None) -> dict[str, Any]:
    """The linked toy uses the exact production resume/materializer/bridge path."""
    del checkpoint_path
    group = ToyGammaGroup()
    q0 = toy_q0(budget)
    relators = [[1, 1, 1], [2, 2], [1, 2, 1, 2]]
    binding = toy_input_binding()
    q0_digest = sha_obj({"parents": q0["public_parents"],
                         "letters": q0["public_letters"]})
    roster_digest = toy_roster_digest()
    state.update({"input_binding": binding,
                  "q0_transition_sha256": q0_digest,
                  "selected_gamma_records": [1],
                  "task172_roster_sha256": roster_digest,
                  "checkpoint_ready": True,
                  "resumed_from": resume_identity})
    if resume is not None:
        input_require(resume_identity is not None and
                      resume["input_binding"] == binding and
                      resume["q0_transition_sha256"] == q0_digest and
                      resume["selected_gamma_records"] == [1] and
                      resume["task172_roster_sha256"] == roster_digest,
                      "TOY_RESUME_AUTHENTICATED_BINDING")
    prefix = [] if resume is None else resume["rows"]
    rows = materialize_identity_rows(
        group, row_iterator_for(group, group.words, relators), budget, 9,
        prefix=prefix, state=state)
    state["presentation_complete"] = True
    input_require(sha_obj({"schema": SELFTEST_SCHEMA + "/row-roster/v1",
        "row_count": len(rows),
        "layer_counts": {name: sum(row["layer"] == name for row in rows)
                         for name in ("Gamma_Cayley", "action", "Q0_lift")}}) ==
                  roster_digest, "TOY_ROSTER_BINDING")
    runtime = toy_runtime(group, q0, budget)
    prefix_digests = [] if resume is None else resume["bridge_digests"]
    bridge_digests = replay_bridge_rows(
        runtime, rows, budget, prefix_digests=prefix_digests, state=state)
    if resume is not None:
        input_require(sha_obj(bridge_digests[:resume["bridge_cursor"]]) ==
                      resume["bridge_replay_sha256"],
                      "TOY_RESUME_BRIDGE_PREFIX_DIGEST")
    bridge_eval_calls = runtime["p176"].eval_calls
    input_require(bridge_eval_calls == len(rows),
                  "TOY_BRIDGE_ONE_ACTUAL_EVAL_PER_RELATOR")
    evaluator = consumer_abi_public(runtime, sha_obj(rows))
    d_order = toy_d_order()
    normal_forms = [[], [1], [1, 1], [2], [1, 2], [1, 1, 2]]
    input_require(len({qeval(word) for word in normal_forms}) == len(q0["states"]) and
                  all(qeval(word) == tuple(range(3)) for word in relators),
                  "TOY_QUOTIENT_PRESENTATION")
    selected, selected_order = greedy_gamma_records(group)
    q_defects = [group.ids[group.key(group.eval(word))] for word in relators]
    defect_order, defect_rounds = normal_closure_order(group, q_defects, budget)
    layers = {name: sum(row["layer"] == name for row in rows)
              for name in ("Gamma_Cayley", "action", "Q0_lift")}
    symbolic_ten = [{"type": row["type"], "context_id": row["context_id"],
                     "token": index}
                    for index, row in enumerate(TASK176_COORDINATES)]
    symbolic_eleven = insertion(symbolic_ten)
    symbolic_seven = regroup(symbolic_eleven)
    input_require(deletion(symbolic_eleven) == symbolic_ten and
                  insertion(deletion(symbolic_eleven)) == symbolic_eleven and
                  flatten(symbolic_seven) == symbolic_eleven,
                  "TOY_BRIDGE_INVERSE")
    total_bound = selected_order * len(normal_forms)
    normal_generation = (selected == [1] and selected_order == defect_order == 2 and
                         total_bound == d_order and
                         layers == {"Gamma_Cayley": 2, "action": 4, "Q0_lift": 3})
    input_require(normal_generation, "TOY_NORMAL_GENERATION")
    counted = counted_checkpoint(state, budget)
    require(counted is not None, "toy complete checkpoint accounting")
    checkpoint, _ = counted
    evidence = getattr(args, "selftest_evidence", None)
    input_require(type(evidence) is dict and set(evidence) ==
                  {"presentation", "bridge", "preflight_zero",
                   "preflight_four"},
                  "TOY_PRODUCTION_RESOURCE_EVIDENCE")
    certificate = {"schema": SELFTEST_SCHEMA, "status": "COMPLETE",
        "terminal": "SELFTEST_COMPLETE",
        "sources": {"normalized_predecessor_dependency_cone":
                        dependency_cone_manifest()},
        "extension": {"construction": "Dic_3_to_S3_non_split",
            "Q0_order": len(q0["states"]), "Gamma_order": len(group.states),
            "D_order": d_order,
            "non_split_witness": {"y_squared": list(dmul((0, 1), (0, 1))),
                                  "kernel_generator": list(group.states[1])}},
        "Q0": {"parents": q0["public_parents"],
               "parent_letters": q0["public_letters"],
               "transitions": q0["transitions"], "relators": relators,
               "normal_forms": normal_forms,
               "presentation_order_upper_bound": len(normal_forms),
               "marked_image_order": len(q0["states"])},
        "bridge": {"ten": symbolic_ten, "eleven": symbolic_eleven,
                   "seven": symbolic_seven,
                   "ten_to_eleven": list(TEN_TO_ELEVEN),
                   "delete_duplicate": list(ELEVEN_DELETE_DUPLICATE),
                   "occurrence_ledger": OCCURRENCE_LEDGER,
                   "kernel_order": d_order // total_bound,
                    "roof_order": total_bound,
                    "relator_eval_calls": bridge_eval_calls},
        "presentation": {"rows": rows, "rows_sha256": sha_obj(rows),
            "row_count": len(rows), "layer_counts": layers,
            "selected_gamma_records": selected,
            "selected_gamma_closure_order": selected_order,
            "Gamma_cayley_order_bound": len(group.states),
            "Q0_order_bound": len(normal_forms), "total_order_bound": total_bound,
            "marked_image_order": d_order, "normal_generation": normal_generation,
            "normal_closure_rounds": defect_rounds, "chunks": chunk_seals(rows)},
        "evaluator": evaluator,
        "bridge_replay_sha256": sha_obj(bridge_digests),
        "resume": checkpoint,
        "resume_chain": {"presentation": evidence["presentation"],
                         "bridge": evidence["bridge"],
                         "completed_resumed_from": state["resumed_from"]},
        "resource_terminals": {
            "presentation": evidence["presentation"]["terminal_envelope"],
            "bridge": evidence["bridge"]["terminal_envelope"],
            "preflight_zero":
                evidence["preflight_zero"]["terminal_envelope"],
            "preflight_four":
                evidence["preflight_four"]["terminal_envelope"]}}
    return finalize_toy(certificate, budget)


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


def load_fixture(path_text: str | None) -> dict[str, Any]:
    input_require(path_text is not None, "SELFTEST_FIXTURE_REQUIRED")
    path = Path(path_text)
    expected_path = "search/certs/d972_r07_seven_context_roof_presentation_selftest_v1_20260828.json"
    input_require(not path.is_absolute() and path.as_posix() == expected_path,
                  "SELFTEST_FIXTURE_PATH")
    fixture_rel, fixture_size, fixture_digest = PINS["selftest_fixture"]
    raw = file_pin(fixture_rel, fixture_size, fixture_digest)
    try:
        fixture = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputStop("SELFTEST_FIXTURE_JSON") from exc
    input_require(type(fixture) is dict and fixture.get("schema") ==
                  "d972-r07-seven-context-roof-presentation-selftest-fixture/v4" and
                  type(fixture.get("expected")) is dict and
                  fixture.get("production_path") == {
                    "presentation_checkpoint_cursor": 4,
                    "presentation_bridge_cursor": 0,
                    "presentation_terminal_cap": "gamma_operations",
                    "bridge_checkpoint_cursor": 9, "bridge_cursor": 2,
                    "preflight_presentation_limits": [0, 4],
                    "preflight_q0_counters": [0, 0],
                    "portable_resume_stages": 2,
                    "current_output_to_fixed_stage": True} and
                  fixture.get("context_map_count") == 7 and
                  fixture.get("toy_coordinate_automorphisms") == [
                    {"u": 1, "v": value} for value in range(6)] + [
                    {"u": 5, "v": value} for value in range(4)] and
                  fixture.get("joint_coordinate_image") == {
                    "normal_form_count": 12, "distinct_value_count": 12,
                    "nonsplit_cocycle_in_image": True} and
                  fixture.get("nonsplit_section_cocycle") == {
                    "left": "y", "right": "y", "quotient_product": "identity",
                    "canonical_product_section_word": [], "nontrivial": True},
                  "SELFTEST_FIXTURE_SCHEMA")
    return fixture


SELFTEST_PREFIX = "ci/out/d972_r07_seven_context_roof_presentation_selftest"


def capture_production(args: argparse.Namespace) -> dict[str, Any]:
    """Shared terminalization for command-line production and linked SELFTEST."""
    try:
        return make_production(args)
    except ResourceStop as exc:
        detail = {"phase": exc.phase, "cap": exc.cap,
                  "value": exc.value, "limit": exc.limit}
        reason = (f"phase={exc.phase}:cap={exc.cap}:value={exc.value}:"
                  f"limit={exc.limit}")
        return terminal_envelope(
            UNKNOWN_RESOURCE, reason, resource=getattr(exc, "snapshot", None),
            terminal_detail=detail,
            checkpoint=getattr(exc, "checkpoint_binding", None),
            checkpoint_manifest=getattr(
                exc, "checkpoint_manifest_binding", None),
            checkpoint_reason=getattr(exc, "checkpoint_unavailable_reason", None))
    except InputStop as exc:
        return terminal_envelope(UNKNOWN_INPUT, str(exc))


def selftest_checkpoint_evidence(envelope: dict[str, Any], cap: str,
                                 expect_checkpoint: bool) -> None:
    validate_self_digest(envelope, "self_digest_sha256", "SELFTEST_TERMINAL")
    input_require(envelope.get("status") == UNKNOWN_RESOURCE and
                  envelope.get("terminal") == UNKNOWN_RESOURCE and
                  type(envelope.get("resource_terminal")) is dict and
                  envelope["resource_terminal"]["cap"] == cap and
                  envelope["resource_terminal"]["value"] >
                  envelope["resource_terminal"]["limit"],
                  "SELFTEST_ACTUAL_UNKNOWN_RESOURCE")
    binding = envelope.get("checkpoint")
    manifest_binding = envelope.get("checkpoint_manifest")
    if expect_checkpoint:
        input_require(type(binding) is dict and type(manifest_binding) is dict and
                      envelope.get("checkpoint_unavailable_reason") is None,
            "SELFTEST_EXPECTED_CHECKPOINT")
        raw = (ROOT / binding["path"]).read_bytes()
        input_require(len(raw) == binding["bytes"] and
                      sha_bytes(raw) == binding["sha256"],
                      "SELFTEST_CHECKPOINT_FILE_IDENTITY")
        checkpoint = validate_checkpoint_shape(json.loads(raw), 9)
        input_require(checkpoint["seal_sha256"] == binding["seal_sha256"] and
                      checkpoint["cursor"] == binding["cursor"] and
                      checkpoint["bridge_cursor"] == binding["bridge_cursor"] and
                      checkpoint["limits"] == envelope["resource"]["limits"] and
                      checkpoint["counters"] == envelope["resource"]["counters"],
                      "SELFTEST_CHECKPOINT_TERMINAL_SNAPSHOT")
        input_require(set(manifest_binding) == {
            "path", "bytes", "sha256", "self_digest_sha256",
            "future_checkpoint_path"}, "SELFTEST_MANIFEST_BINDING_KEYS")
        manifest_raw = (ROOT / manifest_binding["path"]).read_bytes()
        manifest = json.loads(manifest_raw)
        input_require(manifest_raw == canonical(manifest) and
                      len(manifest_raw) == manifest_binding["bytes"] and
                      sha_bytes(manifest_raw) == manifest_binding["sha256"] and
                      validate_self_digest(
                          manifest, "self_digest_sha256", "SELFTEST_MANIFEST") ==
                      manifest_binding["self_digest_sha256"] and
                      set(manifest) == RESUME_MANIFEST_KEYS and
                      manifest["schema"] == RESUME_MANIFEST_SCHEMA and
                      manifest["checkpoint_path"] ==
                      manifest_binding["future_checkpoint_path"] and
                      manifest["checkpoint_path"] != binding["path"] and
                      manifest["checkpoint_bytes"] == binding["bytes"] and
                      manifest["checkpoint_sha256"] == binding["sha256"] and
                      manifest["checkpoint_seal_sha256"] ==
                      binding["seal_sha256"] and
                      manifest["cursor"] == binding["cursor"] and
                      manifest["bridge_cursor"] == binding["bridge_cursor"],
                      "SELFTEST_PORTABLE_MANIFEST_IDENTITY")
    else:
        input_require(binding is None and manifest_binding is None and envelope.get(
            "checkpoint_unavailable_reason") ==
            "checkpoint_bytes_cap_or_unready",
            "SELFTEST_EXPECTED_NO_CHECKPOINT")


def stage_selftest_resume_pair(envelope: dict[str, Any],
                               staged_checkpoint_text: str,
                               staged_manifest_text: str) -> dict[str, Any]:
    """Model artifact download: copy output bytes to fixed next-run names."""
    output_checkpoint = envelope["checkpoint"]
    output_manifest = envelope["checkpoint_manifest"]
    staged_checkpoint = safe_runtime_path(
        staged_checkpoint_text,
        ("ci/out/d972_r07_seven_context_roof_presentation_selftest.",),
        "SELFTEST_STAGED_CHECKPOINT")
    staged_manifest = safe_runtime_path(
        staged_manifest_text,
        ("ci/out/d972_r07_seven_context_roof_presentation_selftest.",),
        "SELFTEST_STAGED_MANIFEST")
    input_require(output_manifest["future_checkpoint_path"] ==
                  staged_checkpoint.as_posix() and
                  staged_checkpoint != staged_manifest and
                  not staged_checkpoint.exists() and
                  not staged_manifest.exists(),
                  "SELFTEST_FIXED_STAGE_TARGET")
    checkpoint_raw = (ROOT / output_checkpoint["path"]).read_bytes()
    manifest_raw = (ROOT / output_manifest["path"]).read_bytes()
    staged_checkpoint.parent.mkdir(parents=True, exist_ok=True)
    staged_checkpoint.write_bytes(checkpoint_raw)
    staged_manifest.write_bytes(manifest_raw)
    checkpoint_binding = dict(output_checkpoint)
    checkpoint_binding["path"] = staged_checkpoint.as_posix()
    manifest_binding = dict(output_manifest)
    manifest_binding["path"] = staged_manifest.as_posix()
    input_require(checkpoint_binding["bytes"] == len(checkpoint_raw) and
                  checkpoint_binding["sha256"] == sha_bytes(checkpoint_raw) and
                  manifest_binding["bytes"] == len(manifest_raw) and
                  manifest_binding["sha256"] == sha_bytes(manifest_raw),
                  "SELFTEST_STAGED_PAIR_BYTE_IDENTITY")
    return {"checkpoint_binding": checkpoint_binding,
            "manifest_binding": manifest_binding}


def selftest(fixture: dict[str, Any]) -> dict[str, Any]:
    input_require(type(fixture.get("mutation_count")) is int and
                  fixture["mutation_count"] == 44, "SELFTEST_MUTATION_CONTRACT")
    paths = {
        "presentation_output_checkpoint":
            SELFTEST_PREFIX + ".presentation.output.checkpoint.json",
        "presentation_output_manifest":
            SELFTEST_PREFIX + ".presentation.output.manifest.json",
        "presentation_staged_checkpoint":
            SELFTEST_PREFIX + ".presentation.staged.checkpoint.json",
        "presentation_staged_manifest":
            SELFTEST_PREFIX + ".presentation.staged.manifest.json",
        "bridge_output_checkpoint":
            SELFTEST_PREFIX + ".bridge.output.checkpoint.json",
        "bridge_output_manifest":
            SELFTEST_PREFIX + ".bridge.output.manifest.json",
        "bridge_staged_checkpoint":
            SELFTEST_PREFIX + ".bridge.staged.checkpoint.json",
        "bridge_staged_manifest":
            SELFTEST_PREFIX + ".bridge.staged.manifest.json",
        "preflight_zero_checkpoint":
            SELFTEST_PREFIX + ".preflight-zero.output.checkpoint.json",
        "preflight_zero_manifest":
            SELFTEST_PREFIX + ".preflight-zero.output.manifest.json",
        "preflight_zero_future":
            SELFTEST_PREFIX + ".preflight-zero.staged.checkpoint.json",
        "preflight_four_checkpoint":
            SELFTEST_PREFIX + ".preflight-four.output.checkpoint.json",
        "preflight_four_manifest":
            SELFTEST_PREFIX + ".preflight-four.output.manifest.json",
        "preflight_four_future":
            SELFTEST_PREFIX + ".preflight-four.staged.checkpoint.json"}
    input_require(all(not (ROOT / path).exists() for path in paths.values()),
                  "SELFTEST_STALE_OUTPUT")

    preflight_zero_terminal = capture_production(toy_args(
        presentation_rows=0,
        checkpoint=paths["preflight_zero_checkpoint"],
        checkpoint_manifest_output=paths["preflight_zero_manifest"],
        future_resume_checkpoint=paths["preflight_zero_future"]))
    selftest_checkpoint_evidence(
        preflight_zero_terminal, "presentation_rows", False)
    preflight_four_terminal = capture_production(toy_args(
        presentation_rows=4,
        checkpoint=paths["preflight_four_checkpoint"],
        checkpoint_manifest_output=paths["preflight_four_manifest"],
        future_resume_checkpoint=paths["preflight_four_future"]))
    selftest_checkpoint_evidence(
        preflight_four_terminal, "presentation_rows", False)
    input_require(all(not (ROOT / paths[name]).exists() for name in (
        "preflight_zero_checkpoint", "preflight_zero_manifest",
        "preflight_zero_future", "preflight_four_checkpoint",
        "preflight_four_manifest", "preflight_four_future")),
        "SELFTEST_PREFLIGHT_CREATED_NO_CHECKPOINT_OR_MANIFEST")
    for terminal, limit in ((preflight_zero_terminal, 0),
                            (preflight_four_terminal, 4)):
        input_require(terminal["resource_terminal"] == {
            "phase": "presentation_roster_preflight",
            "cap": "presentation_rows", "value": 9, "limit": limit} and
            all(terminal["resource"]["counters"][name] == 0
                for name in ("q0_states", "q0_edges", "presentation_rows",
                             "gamma_operations", "dag_nodes")),
            "SELFTEST_PREFLIGHT_BEFORE_PREDECESSOR_RECONSTRUCTION")

    presentation_terminal = capture_production(toy_args(
        gamma_operations=4,
        checkpoint=paths["presentation_output_checkpoint"],
        checkpoint_manifest_output=paths["presentation_output_manifest"],
        future_resume_checkpoint=paths["presentation_staged_checkpoint"]))
    selftest_checkpoint_evidence(
        presentation_terminal, "gamma_operations", True)
    input_require(presentation_terminal["checkpoint"]["cursor"] == 4 and
                  presentation_terminal["checkpoint"]["bridge_cursor"] == 0,
                  "SELFTEST_PARTIAL_PRESENTATION_CURSOR")
    presentation_staged = stage_selftest_resume_pair(
        presentation_terminal, paths["presentation_staged_checkpoint"],
        paths["presentation_staged_manifest"])
    presentation_evidence = {
        "terminal_envelope": presentation_terminal,
        "checkpoint_binding": presentation_terminal["checkpoint"],
        "manifest_binding": presentation_terminal["checkpoint_manifest"],
        "staged_checkpoint_binding":
            presentation_staged["checkpoint_binding"],
        "staged_manifest_binding": presentation_staged["manifest_binding"]}

    bridge_terminal = capture_production(toy_args(
        resume=paths["presentation_staged_checkpoint"],
        resume_manifest=paths["presentation_staged_manifest"],
        checkpoint=paths["bridge_output_checkpoint"],
        checkpoint_manifest_output=paths["bridge_output_manifest"],
        future_resume_checkpoint=paths["bridge_staged_checkpoint"],
        gamma_operations=11))
    selftest_checkpoint_evidence(bridge_terminal, "gamma_operations", True)
    input_require(bridge_terminal["checkpoint"]["cursor"] == 9 and
                  bridge_terminal["checkpoint"]["bridge_cursor"] == 2,
                  "SELFTEST_PARTIAL_BRIDGE_CURSOR")
    bridge_staged = stage_selftest_resume_pair(
        bridge_terminal, paths["bridge_staged_checkpoint"],
        paths["bridge_staged_manifest"])
    bridge_evidence = {
        "terminal_envelope": bridge_terminal,
        "checkpoint_binding": bridge_terminal["checkpoint"],
        "manifest_binding": bridge_terminal["checkpoint_manifest"],
        "staged_checkpoint_binding": bridge_staged["checkpoint_binding"],
        "staged_manifest_binding": bridge_staged["manifest_binding"]}

    certificate = capture_production(toy_args(
        resume=paths["bridge_staged_checkpoint"],
        resume_manifest=paths["bridge_staged_manifest"],
        selftest_evidence={"presentation": presentation_evidence,
                           "bridge": bridge_evidence,
                           "preflight_zero": {
                               "terminal_envelope": preflight_zero_terminal},
                           "preflight_four": {
                               "terminal_envelope": preflight_four_terminal}}))
    input_require(certificate.get("schema") == SELFTEST_SCHEMA and
                  certificate.get("status") == "COMPLETE" and
                  toy_summary(certificate) == fixture["expected"],
                  "SELFTEST_PRODUCTION_COMPLETION")
    return certificate


def terminal_envelope(status: str, reason: str, result: Any = None,
                      resource: dict[str, Any] | None = None,
                      terminal_detail: dict[str, Any] | None = None,
                      checkpoint: dict[str, Any] | None = None,
                      checkpoint_manifest: dict[str, Any] | None = None,
                      checkpoint_reason: str | None = None) -> dict[str, Any]:
    value = {"schema": SCHEMA, "status": status, "terminal": status,
             "reason": reason, "result": result, "resource": resource,
             "resource_terminal": terminal_detail, "checkpoint": checkpoint,
             "checkpoint_manifest": checkpoint_manifest,
             "checkpoint_unavailable_reason": checkpoint_reason,
             "cofinal_lift": False, "fake": False, "Ihara_witness": False}
    value["self_digest_sha256"] = sha_obj(value)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--fixture")
    parser.add_argument("--task176-receipt",
                        default="ci/in/d972_r07_all_seven_extension_section_census_v1.json")
    parser.add_argument("--resume")
    parser.add_argument("--resume-manifest")
    parser.add_argument("--checkpoint")
    parser.add_argument("--checkpoint-manifest-output")
    parser.add_argument("--future-resume-checkpoint")
    parser.add_argument("--output")
    parser.add_argument("--seconds", type=float, default=9000.0)
    parser.add_argument("--rss-bytes", type=int, default=8_000_000_000)
    parser.add_argument("--q0-states", type=int, default=Q0_ORDER)
    parser.add_argument("--q0-edges", type=int, default=2 * Q0_ORDER)
    parser.add_argument("--presentation-rows", type=int, default=PRESENTATION_ROWS)
    parser.add_argument("--gamma-operations", type=int, default=5_000_000)
    parser.add_argument("--dag-nodes", type=int, default=10_000_000)
    parser.add_argument("--serialized-bytes", type=int, default=2_000_000_000)
    parser.add_argument("--checkpoint-bytes", type=int, default=100_000_000)
    args = parser.parse_args(argv)
    if args.selftest:
        input_require(type(args.output) is str, "SELFTEST_OUTPUT_REQUIRED")
        output = safe_runtime_path(args.output, ("ci/out/",), "SELFTEST_OUTPUT")
        input_require(not output.exists(), "SELFTEST_STALE_RECEIPT")
        result = selftest(load_fixture(args.fixture))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(canonical(result))
        print("R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_SELFTEST_PASS "
              f"q0_order=6 gamma_order=2 D_order=12 presentation_rows=9 "
              f"receipt={output.as_posix()}")
        return 0
    result = capture_production(args)
    if args.output:
        output = safe_runtime_path(args.output, ("ci/out/",), "OUTPUT")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(canonical(result))
    if result["terminal"] != ISO:
        print("R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_NONPOSITIVE "
              "reason=" + str(result["reason"]))
    print("R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL " +
          result["terminal"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
