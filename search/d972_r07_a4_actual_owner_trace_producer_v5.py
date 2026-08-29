#!/usr/bin/env python3
"""Task373/v5 producer: authenticated, finite rows 1--7 authority trace.

This is a candidate-only physical trace.  It deliberately contains no A4
enumerator and never claims coverage outside the seven registered rows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple


ROOT = Path(__file__).resolve().parents[1]
try:
    import resource
except ImportError:
    resource = None  # type: ignore[assignment]


SCHEMA = "d972-r07-a4-actual-owner-trace/v5"
FIXTURE_REL = "search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json"
# Filled from the immutable v5 fixture after it is sealed.
FIXTURE_BYTES = 8_489
FIXTURE_SHA = "474d8e19ca49cad06b560cf0ac1d5eeeac1927fe2666224cb9501e77b5cc8481"
FIXTURE_SELF = "c674491a2f50b200a70349780f0e7a80c21cc0fc3cecd44432dc6e70c51f63fb"
RECEIPT_REL = "ci/in/d972_r07_seven_context_roof_presentation_v1.json"
MANIFEST_REL = "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json"
RECEIPT_NAME = Path(RECEIPT_REL).name
MANIFEST_NAME = Path(MANIFEST_REL).name
RECEIPT_BYTES = 31_017_244
RECEIPT_SHA = "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"
RECEIPT_SELF = "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f"
MANIFEST_BYTES = 2_722
MANIFEST_SHA = "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"
MANIFEST_SELF = "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684"
ROWS = 6_441
ROWS_SHA = "e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950"
LEGACY_ROWS_SHA = "42481a9ab6c72d751824454d05fb2d0298a227718750a2c2727af4e690c968bc"
LAYER_COUNTS = {"Gamma_Cayley": 6_318, "action": 104, "Q0_lift": 19}
COORDINATE_WIDTHS = [40, 40, 40, 40, 40, 154, 154, 154, 154, 154]
COORDINATE_LEDGER_SHA = "9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c"
OCCURRENCE_LEDGER_SHA = "040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7"

PROCESS_ADDRESS_SPACE_CEILING = 750_000_000
PROCESS_ADDRESS_SPACE_REQUEST = 700_000_000
MODELED_PAYLOAD_TOKEN_CAP = 750_000_000
IO_CHUNK_BYTES = 1_048_576
CANONICAL_FRAGMENT_CHARS = 65_536
CAPS = {
    "opened_bytes": 250_000_000, "temporary_bytes": 250_000_000,
    "canonical_bytes": 750_000_000, "parsed_input_bytes": 350_000_000,
    "opens": 256, "writes": 256, "events": 10_000, "mutations": 7,
}
RESOURCE_CAPS = dict(CAPS, modeled_payload_tokens=MODELED_PAYLOAD_TOKEN_CAP,
                     process_address_space_bytes=PROCESS_ADDRESS_SPACE_REQUEST)
RECHECK_BYTES_CAP = 750_000_000
PROCESS_ADDRESS_SPACE_LIMIT_ACTIVE: int | None = None

COORDINATE_OWNER = [
    {"construction": "d_E(C21)", "context_id": 21, "index": 0, "role": "hexagon_fxy", "source": "(x,y)", "type": "E3"},
    {"construction": "d_E(C22)", "context_id": 22, "index": 1, "role": "hexagon_fxz", "source": "(x,z)", "type": "E3"},
    {"construction": "d_E(C23)", "context_id": 23, "index": 2, "role": "hexagon_fyz", "source": "(y,z)", "type": "E3"},
    {"construction": "d_E(C24)", "context_id": 24, "index": 3, "role": "hexagon_fux", "source": "(u,x)", "type": "E3"},
    {"construction": "d_E(C25)", "context_id": 25, "index": 4, "role": "hexagon_fuy", "source": "(u,y)", "type": "E3"},
    {"construction": "C1", "context_id": 1, "index": 5, "role": "pentagon_b1", "source": "b1/phi234", "type": "E4"},
    {"construction": "C27", "context_id": 27, "index": 6, "role": "pentagon_b2", "source": "b2/phi1_23_4", "type": "E4"},
    {"construction": "C21", "context_id": 21, "index": 7, "role": "pentagon_b3", "source": "b3/phi123", "type": "E4"},
    {"construction": "C26", "context_id": 26, "index": 8, "role": "pentagon_b5_inverse_slot", "source": "b5/phi12_3_4", "type": "E4"},
    {"construction": "C28", "context_id": 28, "index": 9, "role": "pentagon_b4_inverse_slot", "source": "b4/phi1_2_34", "type": "E4"},
]
OCCURRENCE_LEDGER = [
    {"ordinal": 1, "block": "H1", "block_index": 1, "block_slot": 1, "occurrence": "H1_fxy", "type": "E3", "ten_index": 0, "context_id": 21, "role": "hexagon_fxy", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [3, 2]},
    {"ordinal": 2, "block": "H1", "block_index": 1, "block_slot": 2, "occurrence": "H1_fxz", "type": "E3", "ten_index": 1, "context_id": 22, "role": "hexagon_fxz", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [3]},
    {"ordinal": 3, "block": "H1", "block_index": 1, "block_slot": 3, "occurrence": "H1_fyz", "type": "E3", "ten_index": 2, "context_id": 23, "role": "hexagon_fyz", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": []},
    {"ordinal": 4, "block": "H2", "block_index": 2, "block_slot": 1, "occurrence": "H2_fux", "type": "E3", "ten_index": 3, "context_id": 24, "role": "hexagon_fux", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [6, 5]},
    {"ordinal": 5, "block": "H2", "block_index": 2, "block_slot": 2, "occurrence": "H2_fxy", "type": "E3", "ten_index": 0, "context_id": 21, "role": "hexagon_fxy", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [6]},
    {"ordinal": 6, "block": "H2", "block_index": 2, "block_slot": 3, "occurrence": "H2_fuy", "type": "E3", "ten_index": 4, "context_id": 25, "role": "hexagon_fuy", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": []},
    {"ordinal": 7, "block": "P1", "block_index": 3, "block_slot": 1, "occurrence": "P_b1", "type": "E4", "ten_index": 5, "context_id": 1, "role": "pentagon_b1", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9, 8]},
    {"ordinal": 8, "block": "P2", "block_index": 4, "block_slot": 1, "occurrence": "P_b2", "type": "E4", "ten_index": 6, "context_id": 27, "role": "pentagon_b2", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9]},
    {"ordinal": 9, "block": "P3", "block_index": 5, "block_slot": 1, "occurrence": "P_b3", "type": "E4", "ten_index": 7, "context_id": 21, "role": "pentagon_b3", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10]},
    {"ordinal": 10, "block": "P5", "block_index": 6, "block_slot": 1, "occurrence": "P_b5_inverse", "type": "E4", "ten_index": 8, "context_id": 26, "role": "pentagon_b5_inverse_slot", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [11]},
    {"ordinal": 11, "block": "P4", "block_index": 7, "block_slot": 1, "occurrence": "P_b4_inverse", "type": "E4", "ten_index": 9, "context_id": 28, "role": "pentagon_b4_inverse_slot", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": []},
]

SOURCE_PINS = (
    ("ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt", 81, "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"),
    ("ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt", 95, "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"),
    ("ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json", 150, "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"),
    ("search/d972_r07_seven_context_roof_presentation_v1.py", 137169, "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"),
    ("crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", 157253, "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"),
    ("search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", 20541, "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"),
)
SOURCE_PIN_BYTES = sum(size for _, size, _ in SOURCE_PINS)
INTENDED_OPENED_BYTES = SOURCE_PIN_BYTES + FIXTURE_BYTES + RECEIPT_BYTES + MANIFEST_BYTES + 3 * (RECEIPT_BYTES + MANIFEST_BYTES) + (RECEIPT_BYTES + 8 + MANIFEST_BYTES) + (MANIFEST_BYTES + 1) + RECEIPT_BYTES
INTENDED_TEMPORARY_BYTES = 3 * (RECEIPT_BYTES + MANIFEST_BYTES) + (RECEIPT_BYTES + 8 + MANIFEST_BYTES) + (MANIFEST_BYTES + 1) + RECEIPT_BYTES
ORDINARY_PARSED_INPUT_BYTES = FIXTURE_BYTES + 5 * RECEIPT_BYTES + 8 * MANIFEST_BYTES + 9
INTENDED_PARSED_INPUT_BYTES = ORDINARY_PARSED_INPUT_BYTES + 4 * RECEIPT_BYTES
AUTHORITY_RAW_PAYLOAD_TOKENS = SOURCE_PIN_BYTES + FIXTURE_BYTES + RECEIPT_BYTES + MANIFEST_BYTES
LARGEST_MODELED_PAYLOAD_TOKENS = AUTHORITY_RAW_PAYLOAD_TOKENS + RECEIPT_BYTES + 8 + IO_CHUNK_BYTES
METERED_LOGICAL_OPENS = 19 + 20 + 14
INTENDED_REVALIDATED_BYTES = 14 * (SOURCE_PIN_BYTES + FIXTURE_BYTES + RECEIPT_BYTES + MANIFEST_BYTES)
INTENDED_WRITES = 10
INTENDED_EVENTS = 16 + 50
MUTATIONS = ("per_layer_ordinal", "authority_binding", "canonical_input_bytes", "resolved_path_traversal", "normal_generation_proof", "bridge_typed_occurrence_ledger", "evaluator_abi_canary")
ROW_KEYS = {
    "Gamma_Cayley": {"ancestry", "generator", "layer", "ordinal", "state", "target_state", "word"},
    "action": {"ancestry", "layer", "letter", "ordinal", "orientation", "record", "target_state", "word"},
    "Q0_lift": {"ancestry", "layer", "ordinal", "target_state", "word"},
}
ANCESTRY_KEYS = {"Gamma_Cayley": {"record_word", "section_source_word", "section_target_word"}, "action": {"record_word", "section_target_word", "tokens"}, "Q0_lift": {"q0_relator_word", "section_target_word"}}
BRIDGE_KEYS = {"branch", "eleven_delete_duplicate", "image_order", "inverse_algorithm", "kernel_order", "marked_inverse_count", "marked_replay", "marked_replay_count", "occurrence_ledger", "occurrence_ledger_sha256", "order_computation", "relator_replay", "seven_blocks", "ten_to_eleven", "typed_coordinate_ledger_sha256"}
EVALUATOR_KEYS = {"canaries", "context_maps", "coordinate_ledger_sha256", "coordinate_widths", "encoding", "entry_points", "joint_coordinate_image", "module", "registry_callable", "relator_rows_sha256", "runtime_constructor", "schema", "semantics"}
TOP_RECEIPT_KEYS = {"D_all", "Delta0", "Gamma", "Ihara_witness", "Q0", "bridge", "cofinal_lift", "direct_Delta_states_enumerated", "evaluator", "fake", "input", "million_row_Q0_Schreier_stream", "resource", "resume", "schema", "self_digest_sha256", "status", "terminal"}
PRESENTATION_KEYS = {"chunks", "layer_counts", "normal_closure_exact", "normal_generation", "normal_generation_proof", "resume_cursor", "row_count", "rows", "rows_sha256", "source_word_encoding", "task172_legacy_rows_sha256"}
CHUNK_KEYS = {"end", "prefix_complete", "sealed", "sha256", "start"}
ABI_ENCODING = {"roof_value": "ten lowercase hex typed coordinate blobs", "source_word": "strict signed F2 list", "state_ids": "one-based Gamma and Q0 ids"}
ABI_ENTRY_POINTS = {"action": {"arguments": ["runtime", "actor_word", "value"], "callable": "roof_action"}, "eval": {"arguments": ["runtime", "word"], "callable": "roof_eval"}, "inverse": {"arguments": ["runtime", "value"], "callable": "roof_inverse"}, "multiply": {"arguments": ["runtime", "left", "right"], "callable": "roof_multiply"}, "section_cocycle": {"arguments": ["runtime", "left_section_word", "right_section_word", "product_section_word"], "callable": "roof_section_cocycle"}, "source_section": {"arguments": ["runtime", "gamma_state_id", "q0_state_id"], "callable": "roof_source_section"}}
ABI_SEMANTICS = {"action": "actor*value*actor_inverse", "multiplication": "left_then_right", "section_cocycle": "s_left*s_right*s_product_inverse"}
ABI_CANARIES_RAW = r'''{"nonsplit_y_y_section_cocycle":null,"source_2_2":{"gamma_state_id":2,"gamma_word":[1,1,-2,1,1,2,2,1,1,1,2,1,1,-2,-1,-2,-1,-1,2,-1,-1,-2,1,1,2,1,1,-2,1,1,-2,1,1,2,1,1,-2,1,1,2,2,1,1,1,2,1,1,-2,-1,-2,-1,-1,2,-1,-1,-2,1,1,2,1,1,-2,1,1,-2,1,1,2],"q0_state_id":2,"q0_word":[1],"source_word":[1,1,-2,1,1,2,2,1,1,1,2,1,1,-2,-1,-2,-1,-1,2,-1,-1,-2,1,1,2,1,1,-2,1,1,-2,1,1,2,1,1,-2,1,1,2,2,1,1,1,2,1,1,-2,-1,-2,-1,-1,2,-1,-1,-2,1,1,2,1,1,-2,1,1,-2,1,1,2,1],"value":["0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000001","0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000002","0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000101","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000202","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000200","080704020001030605090a0b0c0d0e0f101112131415161718191a221e211f1d231b201c25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a79787785867e7f808182838488878f8e8d8c8b8a8900000001000000000001","00010203040506070811100d0b090a0c0f0e1a19161412131518171d21221f1b1c23201e2425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e40414243444546473f48504f4e4d4c4b4a495159585756555453525b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d787776757d7c7b7a7985867e7f80818283848f8e8d8c8b8a89888701010000000002010100","000102030405060708090a0b0c0d0e0f1011141a1819151213171623221f1d1b1c1e21202425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f5051525354555657585961625a5b5c5d5e5f60636b6a6968676665646c74737271706f6e6d767778797a7b7c7d757e868584838281807f878f8e8d8c8b8a898801000000000001000000","08070402000103060511100d0b090a0c0f0e12131415161718191a1c231f1d22211b201e25262728292a2b2c242d3534333231302f2e363e3d3c3b3a39383740414243444546473f48504f4e4d4c4b4a495159585756555453525a5b5c5d5e5f606162636465666768696a6b6c6d6e6f70717273747c7d75767778797a7b8584838281807f7e868988878f8e8d8c8b8a00010001000002000101","000102030405060708090a0b0c0d0e0f10111a191614121315181723221f1d1b1c1e21202425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d767778797a7b7c7d757e868584838281807f878f8e8d8c8b8a898801000000000001010000"]},"x":{"value":["0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000000","0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000000","0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000201","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000201","080704020001030605090a0b0c0d0e0f101112131415161718191a1c21201b221f231e1d25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001000000000000","00010203040506070811100d0b090a0c0f0e1a19161412131518171c1f2122201e1b231d2425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e40414243444546473f48504f4e4d4c4b4a495159585756555453525b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d787776757d7c7b7a797f808182838485867e8f8e8d8c8b8a89888701010000000002000000","000102030405060708090a0b0c0d0e0f10111a191614121315181723221f1d1b1c1e21202425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d767778797a7b7c7d757e868584838281807f878f8e8d8c8b8a898801000000000000000000","08070402000103060511100d0b090a0c0f0e12131415161718191a1d1f21201b231e1c2225262728292a2b2c242d3534333231302f2e363e3d3c3b3a39383740414243444546473f48504f4e4d4c4b4a495159585756555453525a5b5c5d5e5f606162636465666768696a6b6c6d6e6f7071727374767778797a7b7c7d758584838281807f7e868988878f8e8d8c8b8a00010001000002000000","000102030405060708090a0b0c0d0e0f10111a191614121315181723221f1d1b1c1e21202425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d767778797a7b7c7d757e868584838281807f878f8e8d8c8b8a898801000000000000000000"],"word":[1]},"x_action_y":{"actor_word":[1],"input":["0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0502070108060400030b0a0911100f0e0d0c1a19181716151413121c1d1e1f202122231b02000200","0502070108060400030b0a0911100f0e0d0c1a19181716151413121c1d1e1f202122231b02000200","0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000000","0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0106050007040803020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f2021222325242c2b2a292827262e2f3031323334352d37363e3d3c3b3a3938403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000000","0204060500080301070a0f0e09100d110c0b1318171219161a15141b1c1d1e1f2021222325262728292a2b2c2434333231302f2e2d353837363e3d3c3b3a39403f47464544434241494a4b4c4d4e4f50485251595857565554535b5a6261605f5e5d5c6465666768696a6b636d6c74737271706f6e75767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000010100000002","080704020001030605090a0b0c0d0e0f101112131415161718191a1c21201b221f231e1d25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001000000000000","0106050007040803020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f2021222325242c2b2a292827262e2f3031323334352d37363e3d3c3b3a3938403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000000","010406070503000802090a0b0c0d0e0f10111318171219161a15141c21201b221f231e1d272625242c2b2a29282e2f3031323334352d3e3d3c3b3a393837363f404142434445464748494a4b4c4d4e4f505152535455565758595b5a6261605f5e5d5c6465666768696a6b636d6c74737271706f6e76757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001010000000002"],"value":["03060108050704000211100f0e0d0c0b0a091a1213141516171819232221201f1e1d1c1b00000102","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000201","0805010203060700040911100f0e0d0c0b0a181716151413121a19231b1c1d1e1f20212202000202","05020408060703010011090a0b0c0d0e0f101413121a19181716151d1c1b232221201f1e01000002","04080300070201060511100f0e0d0c0b0a091a12131415161718191e1d1c1b232221201f00000101","0306010805070400020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f202122232c2b2a292827262524352d2e2f30313233343e3d3c3b3a39383736403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000002","0204060500080301070c0f0a110e100d090b1518131a17191612141b1c1d1e1f2021222325262728292a2b2c2434333231302f2e2d353837363e3d3c3b3a3947464544434241403f5048494a4b4c4d4e4f5958575655545352516261605f5e5d5c5b5a6b636465666768696a74737271706f6e6d6c75767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000010100020202","080704020001030605090a0b0c0d0e0f101112131415161718191a1e211c2320221f1b1d25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f70717273747d7c7b7a7978777675867e7f8081828384858f8e8d8c8b8a89888700000001000002000000","0306010805070400020c0f0a110e100d090b12131415161718191a1b1c1d1e1f202122232c2b2a292827262524352d2e2f30313233343e3d3c3b3a3938373647464544434241403f5048494a4b4c4d4e4f5958575655545352515a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000202","010406070503000802090a0b0c0d0e0f10111518131a17191612141e211c2320221f1b1d272625242c2b2a29282e2f3031323334352d3e3d3c3b3a393837363f404142434445464748494a4b4c4d4e4f505152535455565758596261605f5e5d5c5b5a6b636465666768696a74737271706f6e6d6c7d7c7b7a7978777675867e7f8081828384858f8e8d8c8b8a89888700000001010002020002"]},"x_inverse":{"value":["04050306020807010011090a0b0c0d0e0f10121a191817161514131b232221201f1e1d1c02000000","04050306020807010011090a0b0c0d0e0f10121a191817161514131b232221201f1e1d1c02000000","0300080705020104060a0911100f0e0d0c0b1a12131415161718191c1b232221201f1e1d00000200","0203070501060008040911100f0e0d0c0b0a13121a1918171615141c1d1e1f202122231b01000100","0203070501060008040911100f0e0d0c0b0a13121a1918171615141c1d1e1f202122231b01000100","040503060208070100090a0b0c0d0e0f101112131415161718191a1e1b2322201d1c1f212c2425262728292a2b2d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a797877867e7f80818283848588878f8e8d8c8b8a8900000002000000000000","0001020304050607080d0e0c0f0b11100a0916171518141a191312211b23201c1f1d1e222425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e473f4041424344454648504f4e4d4c4b4a49515958575655545352625a5b5c5d5e5f6061636b6a6968676665646c74737271706f6e6d787776757d7c7b7a79867e7f8081828384858f8e8d8c8b8a89888702020000000000000000","000102030405060708090a0b0c0d0e0f101116171518141a1913121f201e211d23221c1b2425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f50515253545556575859625a5b5c5d5e5f6061636b6a6968676665646c74737271706f6e6d7d75767778797a7b7c7e868584838281807f878f8e8d8c8b8a898802000000000000000000","0405030602080701000d0e0c0f0b11100a0912131415161718191a1f221b211c1e1d23202c2425262728292a2b2d3534333231302f2e363e3d3c3b3a393837473f4041424344454648504f4e4d4c4b4a495159585756555453525a5b5c5d5e5f606162636465666768696a6b6c6d6e6f70717273747d75767778797a7b7c8584838281807f7e868988878f8e8d8c8b8a00020002000000000000","000102030405060708090a0b0c0d0e0f101116171518141a1913121f201e211d23221c1b2425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f50515253545556575859625a5b5c5d5e5f6061636b6a6968676665646c74737271706f6e6d7d75767778797a7b7c7e868584838281807f878f8e8d8c8b8a898802000000000000000000"],"word":[-1]},"xy":{"value":["0203070501060008040911100f0e0d0c0b0a13121a1918171615141c1d1e1f202122231b01000100","0300080705020104060a0911100f0e0d0c0b1a12131415161718191c1b232221201f1e1d00000200","0204060500080301070a0b0c0d0e0f10110919181716151413121a1d1c1b232221201f1e02000002","0300080705020104060a0911100f0e0d0c0b1a12131415161718191c1b232221201f1e1d00000200","0807010602000405030a0b0c0d0e0f1011091413121a19181716151d1c1b232221201f1e02000001","0203070501060008040a0f0e09100d110c0b12131415161718191a1c21201b221f231e1d242c2b2a29282726252e2d3534333231302f3738393a3b3c3d3e36403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001000100000000","0204060500080301070b0c100e0a0f09110d141519171318121a161c1f2122201e1b231d25262728292a2b2c2434333231302f2e2d353837363e3d3c3b3a393f47464544434241404948504f4e4d4c4b4a5253545556575859515a6261605f5e5d5c5b64636b6a69686766656d6e6f70717273746c787776757d7c7b7a797f808182838485867e8f8e8d8c8b8a89888701010000010102000002","080704020001030605090a0b0c0d0e0f10111a19161412131518171d1e22201c211b231f25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d757d7c7b7a797877767f7e8685848382818088898a8b8c8d8e8f8701000001000000000000","0203070501060008040b0c100e0a0f09110d12131415161718191a1d1f21201b231e1c22242c2b2a29282726252e2d3534333231302f3738393a3b3c3d3e363f47464544434241404948504f4e4d4c4b4a5253545556575859515a5b5c5d5e5f606162636465666768696a6b6c6d6e6f7071727374767778797a7b7c7d758584838281807f7e868988878f8e8d8c8b8a00010001000102000000","010406070503000802090a0b0c0d0e0f1011141519171318121a161d1e22201c211b231f272625242c2b2a29282e2f3031323334352d3e3d3c3b3a393837363f404142434445464748494a4b4c4d4e4f505152535455565758595a6261605f5e5d5c5b64636b6a69686766656d6e6f70717273746c757d7c7b7a797877767f7e8685848382818088898a8b8c8d8e8f8701000001010000000002"],"word":[1,2]},"xy_section_cocycle":{"left":[1],"product":[1,2],"right":[2],"value":["000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000"]},"y":{"value":["0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0502070108060400030b0a0911100f0e0d0c1a19181716151413121c1d1e1f202122231b02000200","0502070108060400030b0a0911100f0e0d0c1a19181716151413121c1d1e1f202122231b02000200","0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000000","0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0106050007040803020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f2021222325242c2b2a292827262e2f3031323334352d37363e3d3c3b3a3938403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000000","0204060500080301070a0f0e09100d110c0b1318171219161a15141b1c1d1e1f2021222325262728292a2b2c2434333231302f2e2d353837363e3d3c3b3a39403f47464544434241494a4b4c4d4e4f50485251595857565554535b5a6261605f5e5d5c6465666768696a6b636d6c74737271706f6e75767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000010100000002","080704020001030605090a0b0c0d0e0f101112131415161718191a1c21201b221f231e1d25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001000000000000","0106050007040803020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f2021222325242c2b2a292827262e2f3031323334352d37363e3d3c3b3a3938403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000000","010406070503000802090a0b0c0d0e0f10111318171219161a15141c21201b221f231e1d272625242c2b2a29282e2f3031323334352d3e3d3c3b3a393837363f404142434445464748494a4b4c4d4e4f505152535455565758595b5a6261605f5e5d5c6465666768696a6b636d6c74737271706f6e76757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001010000000002"],"word":[2]}}'''
ABI_CANARIES: dict[str, Any] | None = None
MANIFEST_FIXED = {
    "schema": "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3", "synthetic": False, "independent": True,
    "producer": {"artifact_id": "9686477718", "head": "bed1d5e6b41477b8799f2a33a24e46f7800f9510", "member": {"basename": RECEIPT_NAME, "bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA}, "run": "33155710862", "terminal_line_sha256": "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090", "zip_sha256": "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854"},
    "checker": {"artifact_id": "9686477718", "head": "bed1d5e6b41477b8799f2a33a24e46f7800f9510", "member": {"basename": RECEIPT_NAME, "bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA}, "run": "33155710862", "terminal_line_sha256": "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e", "zip_sha256": "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854"},
    "producer_attestation": {"basename": "d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt", "bytes": 81, "sha256": "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"},
    "checker_attestation": {"basename": "d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt", "bytes": 95, "sha256": "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"},
    "checker_verdict": {"accepted": True, "basename": "d972_r07_seven_context_roof_presentation_v1.checker.verdict.json", "bytes": 150, "independent": True, "receipt_terminal": "ROOF_BRIDGE_ISOMORPHISM", "schema": "d972-r07-seven-context-roof-presentation/v1/crosscheck/v2", "sha256": "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"},
    "task198_source_identities": {"producer": {"bytes": 137169, "path": "search/d972_r07_seven_context_roof_presentation_v1.py", "sha256": "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"}, "checker": {"bytes": 157253, "path": "crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", "sha256": "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"}, "driver": {"bytes": 20541, "path": "search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", "sha256": "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"}},
}
GENERATION = {"Gamma_cayley_edge_count": 6318, "Gamma_cayley_state_count": 243, "Q0_defect_normal_closure_order": 243, "Q0_defect_normal_closure_rounds": [243], "Q0_lift_count": 19, "Q0_order_proof": {"G9_abstract_presentation_order": 2916, "G9_direct_image_order": 2916, "P_abstract_presentation_order": 504, "P_direct_image_order": 504, "Q0_marked_image_order": 1469664, "Q0_presentation_order_upper_bound": 1469664, "complete_relator_count": 19, "complete_relators_sha256": "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a", "cross_commutator_count": 4, "factor_payload_sha256": "6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba", "marked_splitting_equation_count": 2, "method": "producer-owned SymPy factor orders plus direct marked-permutation enumeration"}, "all_record_generator_closure_order": 243, "marked_action_loop_count": 104, "normal_closure_exact": True, "presentation_quotient_order_upper_bound": 357128352, "selected_gamma_closure_order": 243, "selected_gamma_records": [1, 3, 6, 9], "surjective_marked_image_order": 357128352, "theorem": "v190 Cayley--action--lift order bound", "upper_bound_equals_image_order": True}


class InputStop(RuntimeError):
    """Typed input/platform/resource refusal, never mathematical acceptance."""


class TraceReject(RuntimeError):
    def __init__(self, validator: str, stage: str, reason: str):
        self.validator, self.stage, self.reason = validator, stage, reason
        super().__init__(reason)


class MutationAccepted(RuntimeError):
    pass


class SealedReceipt(NamedTuple):
    dom: dict[str, Any]
    raw: bytearray
    raw_sha256: str
    byte_length: int
    self_seal: str


class SealedManifest(NamedTuple):
    dom: dict[str, Any]
    raw: bytearray
    raw_sha256: str
    byte_length: int
    self_seal: str


@dataclass
class MutationPlan:
    name: str
    role: str
    owner: str
    identity_kind: str
    logical_case_path: str
    owner_path: Path
    resealed_nodes: list[str]
    outside_parent: Path | None = None
    reseal_dag: list[dict[str, Any]] | None = None


class Meter:
    CAPS = CAPS
    def __init__(self) -> None:
        self.counts = {k: 0 for k in self.CAPS}; self.reserved = {k: 0 for k in self.CAPS}
        self.payload_live = 0; self.payload_peak = 0; self.payload_owners: dict[str, int] = {}
        self.revalidated_bytes = 0
        self.traversed = {
            "canonical_compared_bytes": 0, "seal_body_hashed_bytes": 0,
            "row_digest_bytes": 0, "canonical_digest_bytes": 0,
            "canonical_constructed_bytes": 0, "physical_hashed_bytes": 0,
            "case_stage_readback_hashed_bytes": 0,
            "wire_source_hashed_bytes": 0, "stdout_canonical_bytes": 0,
        }
    def reserve(self, key: str, amount: int) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or self.counts[key] + self.reserved[key] + amount > self.CAPS[key]:
            raise InputStop("producer:meter:reserve:" + key)
        self.reserved[key] += amount
    def charge(self, key: str, amount: int = 1) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or self.counts[key] + amount > self.CAPS[key] or amount > self.reserved[key]:
            raise InputStop("producer:meter:unreserved:" + key)
        self.reserved[key] -= amount; self.counts[key] += amount
    def release(self, key: str, amount: int) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or amount > self.reserved[key]:
            raise InputStop("producer:meter:release")
        self.reserved[key] -= amount
    def retain_payload(self, owner: str, amount: int) -> None:
        if type(owner) is not str or not owner or type(amount) is not int or amount < 0 or self.payload_live + amount > MODELED_PAYLOAD_TOKEN_CAP:
            raise InputStop("producer:meter:modeled_payload_tokens")
        self.payload_live += amount; self.payload_peak = max(self.payload_peak, self.payload_live)
        self.payload_owners[owner] = self.payload_owners.get(owner, 0) + amount
    def release_payload(self, owner: str) -> None:
        amount = self.payload_owners.pop(owner, 0)
        if amount < 0 or amount > self.payload_live: raise InputStop("producer:meter:payload_release")
        self.payload_live -= amount
    def release_prefix(self, prefix: str) -> None:
        for owner in list(self.payload_owners):
            if owner.startswith(prefix): self.release_payload(owner)
        if any(owner.startswith(prefix) for owner in self.payload_owners): raise InputStop("producer:meter:owner_leak")
    def public(self) -> dict[str, Any]:
        if type(PROCESS_ADDRESS_SPACE_LIMIT_ACTIVE) is not int: raise InputStop("producer:address_space:not_installed")
        return {
            "caps": dict(RESOURCE_CAPS), "counts": dict(self.counts),
            "modeled_payload_tokens": {
                "current": self.payload_live, "peak": self.payload_peak,
                "definition": "exact ledger tokens for retained file/canonical/mutation byte lengths and reserved bounded I/O/canonical-fragment capacities",
                "omits": "parsed Python DOMs, decoder/interpreter/container/allocator overhead, bytearray capacity slack, and RSS",
            },
            "process_address_space": {
                "mechanism": "RLIMIT_AS", "soft_bytes": PROCESS_ADDRESS_SPACE_LIMIT_ACTIVE,
                "ceiling_bytes": PROCESS_ADDRESS_SPACE_CEILING, "rss_observed": False,
            },
            "traversed_bytes": dict(self.traversed), "revalidated_bytes": self.revalidated_bytes,
            "one_meter": True,
            "logical_open_account": "logical owner opens plus retained-fd revalidation passes; traversal-component OS opens are not included",
            "snapshot_boundary": "complete seven-row no-path-output run before result self-seal and canonical stdout",
        }
    def snapshot(self) -> dict[str, Any]:
        return {"counts": dict(self.counts), "reserved": dict(self.reserved), "modeled_payload_live": self.payload_live, "modeled_payload_peak": self.payload_peak, "payload_owners": dict(self.payload_owners), "traversed_bytes": dict(self.traversed), "revalidated_bytes": self.revalidated_bytes}

CANONICAL_ENCODER = json.JSONEncoder(ensure_ascii=True, sort_keys=True, separators=(",", ":"))

def canonical_fragments(value: Any, meter: Meter, purpose: str):
    serial = 0
    for piece in CANONICAL_ENCODER.iterencode(value):
        if type(piece) is not str: raise InputStop("producer:canonical:fragment_type")
        offset = 0
        while offset < len(piece):
            width = min(CANONICAL_FRAGMENT_CHARS, len(piece) - offset); serial += 1
            token = "fragment:" + purpose + ":" + str(serial); charged = False
            meter.reserve("canonical_bytes", width); meter.retain_payload(token, 2 * width)
            try:
                segment = piece[offset:offset + width]; encoded = segment.encode("ascii")
                if len(encoded) != width: raise InputStop("producer:canonical:non_ascii_fragment")
                meter.charge("canonical_bytes", width); charged = True
                yield encoded
            finally:
                if not charged: meter.release("canonical_bytes", width)
                meter.release_payload(token)
            offset += width

def emit_token(data: bytes, sink: Any, meter: Meter) -> None:
    meter.reserve("canonical_bytes", len(data)); meter.charge("canonical_bytes", len(data)); sink(data)

def stream_canonical(value: Any, sink: Any, meter: Meter, purpose: str) -> None:
    for fragment in canonical_fragments(value, meter, purpose): sink(fragment)

def digest_bytes(raw: bytes | bytearray) -> str:
    h = hashlib.sha256(); h.update(memoryview(raw)); return h.hexdigest()

def digest_object(value: Any, meter: Meter, bound: int, purpose: str = "digest") -> str:
    if type(bound) is not int or bound < 0: raise InputStop("producer:canonical:bound")
    h = hashlib.sha256(); length = 0
    def sink(fragment: bytes) -> None:
        nonlocal length
        length += len(fragment)
        if length > bound: raise InputStop("producer:canonical:overflow")
        h.update(fragment); meter.traversed["canonical_digest_bytes"] += len(fragment)
    stream_canonical(value, sink, meter, purpose)
    return h.hexdigest()

def canonical_buffer(value: Any, meter: Meter, bound: int, owner: str, purpose: str) -> tuple[bytearray, str]:
    if type(bound) is not int or bound < 0 or type(owner) is not str or not owner: raise InputStop("producer:canonical:bound_or_owner")
    out = bytearray(); h = hashlib.sha256(); complete = False
    try:
        for fragment in canonical_fragments(value, meter, purpose):
            if len(out) + len(fragment) > bound: raise InputStop("producer:canonical:overflow")
            meter.retain_payload(owner, len(fragment)); out.extend(fragment); h.update(fragment); meter.traversed["canonical_constructed_bytes"] += len(fragment)
        complete = True
        return out, h.hexdigest()
    finally:
        if not complete: meter.release_payload(owner)

def strict_equal(actual: Any, expected: Any) -> bool:
    if type(expected) is dict:
        return type(actual) is dict and set(actual) == set(expected) and all(strict_equal(actual[k], expected[k]) for k in expected)
    if type(expected) is list:
        return type(actual) is list and len(actual) == len(expected) and all(strict_equal(a, e) for a, e in zip(actual, expected))
    return type(actual) is type(expected) and actual == expected


def _word(value: Any) -> bool:
    return type(value) is list and all(type(x) is int and x in (-2, -1, 1, 2) for x in value)


def _positive_int(value: Any) -> bool:
    return type(value) is int and value > 0


def _stats_equal(a: os.stat_result, b: os.stat_result) -> bool:
    return all(getattr(a, key) == getattr(b, key) for key in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_mode", "st_nlink"))


def _inside(child: Path, parent: Path) -> bool:
    try: return os.path.commonpath((os.path.abspath(child), os.path.abspath(parent))) == os.path.abspath(parent)
    except ValueError: return False


def _nofollow_parent(path: Path) -> tuple[int, str]:
    if os.name == "nt": raise InputStop("producer:windows:one_handle_reparse_unsupported")
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    if not nofollow or not hasattr(os, "O_DIRECTORY"): raise InputStop("producer:posix:no_follow_dirfd_unsupported")
    absolute = Path(os.path.abspath(path)); current = os.open(os.path.sep, os.O_RDONLY | os.O_DIRECTORY | nofollow)
    try:
        for part in absolute.parts[1:-1]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | nofollow, dir_fd=current); os.close(current); current = nxt
        return current, absolute.name
    except Exception:
        os.close(current); raise


def _nofollow_open(path: Path) -> int:
    parent, leaf = _nofollow_parent(path)
    try: return os.open(leaf, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent)
    finally: os.close(parent)


def _nofollow_lstat(path: Path) -> os.stat_result:
    parent, leaf = _nofollow_parent(path)
    try: return os.stat(leaf, dir_fd=parent, follow_symlinks=False)
    finally: os.close(parent)


def _identity(before: os.stat_result, after: os.stat_result, pathname: os.stat_result, path: Path, kind: str, sha: str | None) -> dict[str, Any]:
    stable = _stats_equal(before, after) and _stats_equal(after, pathname)
    return {"identity_kind": kind, "path": str(path), "exists": True, "type": "regular" if stat.S_ISREG(before.st_mode) else "nonregular", "mode": int(before.st_mode), "bytes": int(after.st_size), "sha256": sha, "device": int(before.st_dev), "inode": int(before.st_ino), "mtime_ns": int(before.st_mtime_ns), "nlink": int(after.st_nlink), "single_open_handle": True, "opened_handle_stable": stable, "pathname_matches_opened_handle": _stats_equal(after, pathname), "substitution_detected": not stable}


def _path_identity(path: Path, kind: str) -> dict[str, Any]:
    lexical = Path(os.path.abspath(path))
    try: st = _nofollow_lstat(lexical)
    except (FileNotFoundError, NotADirectoryError):
        return {"identity_kind": kind, "path": str(lexical), "exists": False, "type": "missing", "mode": None, "bytes": None, "sha256": None, "device": None, "inode": None, "mtime_ns": None, "nlink": None, "single_open_handle": False, "opened_handle_stable": False, "pathname_matches_opened_handle": False, "substitution_detected": False}
    return {"identity_kind": kind, "path": str(lexical), "exists": True, "type": "regular" if stat.S_ISREG(st.st_mode) else "nonregular", "mode": int(st.st_mode), "bytes": int(st.st_size), "sha256": None, "device": int(st.st_dev), "inode": int(st.st_ino), "mtime_ns": int(st.st_mtime_ns), "nlink": int(st.st_nlink), "single_open_handle": False, "opened_handle_stable": False, "pathname_matches_opened_handle": False, "substitution_detected": False}


class EventSink:
    def __init__(self, meter: Meter):
        self.meter = meter; self.events: list[dict[str, Any]] = []; self.observed: dict[str, dict[str, Any]] = {}; self.canonical_after: dict[str, str] = {}; self.terminal_count = 0; self.rows_digest: str | None = None
    def enter(self, validator: str, stage: str, owner: str) -> None:
        self.meter.reserve("events", 1); self.meter.charge("events", 1); self.events.append({"ordinal": len(self.events) + 1, "validator": validator, "stage": stage, "owner": owner})
    def terminal(self) -> None: self.terminal_count += 1
    def digest(self) -> str: return digest_object(self.events, self.meter, 1_000_000)


class PhysicalStore:
    def __init__(self, meter: Meter):
        self.meter = meter; self.cache: dict[str, tuple[bytearray, dict[str, Any]]] = {}; self.handles: dict[str, int] = {}
    def read(self, path: Path, role: str, expected: tuple[int, str] | None = None, events: EventSink | None = None, retain_handle: bool = False) -> tuple[bytearray, dict[str, Any]]:
        lexical = Path(os.path.abspath(path)); key = str(lexical)
        if key in self.cache:
            raw, identity = self.cache[key]
            if events is not None: events.observed[role] = identity
            return raw, identity
        self.meter.reserve("opens", 1); open_reserved = True; fd = -1; size = 0
        opened_reserved = False; cache_owner = "cache:" + key
        try:
            fd = _nofollow_open(lexical); before = os.fstat(fd)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1: raise InputStop("producer:physical:file_identity:" + role)
            size = int(before.st_size)
            if size < 0 or size > self.meter.CAPS["temporary_bytes"]: raise InputStop("producer:physical:size:" + role)
            self.meter.reserve("opened_bytes", size); opened_reserved = True
            buf = bytearray(); remaining = size; serial = 0
            while remaining:
                request = min(IO_CHUNK_BYTES, remaining); serial += 1; chunk_owner = "io:read:" + key + ":" + str(serial)
                self.meter.retain_payload(chunk_owner, request)
                try:
                    part = os.read(fd, request)
                    if not part: raise InputStop("producer:physical:short_read:" + role)
                    self.meter.retain_payload(cache_owner, len(part)); buf.extend(part); remaining -= len(part)
                    del part
                finally:
                    self.meter.release_payload(chunk_owner)
            after = os.fstat(fd); pathname = _nofollow_lstat(lexical); sha = digest_bytes(buf); self.meter.traversed["physical_hashed_bytes"] += len(buf)
            identity = _identity(before, after, pathname, lexical, "file", sha)
            if not identity["opened_handle_stable"] or after.st_nlink != 1: raise InputStop("producer:physical:toctou:" + role)
            if expected is not None and (len(buf) != expected[0] or sha != expected[1]): raise InputStop("producer:pin:" + role)
            self.meter.charge("opened_bytes", size); opened_reserved = False; self.meter.charge("opens", 1); open_reserved = False
            self.cache[key] = (buf, identity)
            if retain_handle: self.handles[key] = fd; fd = -1
            if events is not None: events.observed[role] = identity
            return buf, identity
        except Exception:
            if opened_reserved: self.meter.release("opened_bytes", size)
            self.meter.release_payload(cache_owner)
            if open_reserved: self.meter.release("opens", 1)
            raise
        finally:
            if fd >= 0: os.close(fd)
    def revalidate_all(self, expected: dict[str, dict[str, Any]]) -> dict[str, Any]:
        self.meter.reserve("opens", 1); self.meter.charge("opens", 1)
        transcript: dict[str, Any] = {}
        for key, fd in self.handles.items():
            label = expected[key]["label"]; identity = expected[key]["identity"]
            try:
                before = os.fstat(fd); size = int(before.st_size)
                if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or size != identity["bytes"]: raise InputStop("producer:baseline:identity_changed:" + label)
                if os.lseek(fd, 0, os.SEEK_SET) != 0: raise InputStop("producer:baseline:rewind:" + label)
                h = hashlib.sha256(); remaining = size; read = 0; serial = 0
                while remaining:
                    request = min(IO_CHUNK_BYTES, remaining); serial += 1; chunk_owner = "io:revalidate:" + label + ":" + str(serial)
                    self.meter.retain_payload(chunk_owner, request)
                    try:
                        part = os.read(fd, request)
                        if not part: raise InputStop("producer:baseline:short_read:" + label)
                        h.update(part); read += len(part); remaining -= len(part); del part
                    finally:
                        self.meter.release_payload(chunk_owner)
                if os.lseek(fd, 0, os.SEEK_CUR) != size or read != size or h.hexdigest() != identity["sha256"]: raise InputStop("producer:baseline:bytes_changed:" + label)
                after = os.fstat(fd); pathname = _nofollow_lstat(Path(identity["path"]))
                expected_stats = {"st_dev": identity["device"], "st_ino": identity["inode"], "st_size": identity["bytes"], "st_mtime_ns": identity["mtime_ns"], "st_mode": identity["mode"], "st_nlink": identity["nlink"]}
                if not _stats_equal(before, after) or not _stats_equal(after, pathname) or any(int(getattr(after, field)) != value for field, value in expected_stats.items()): raise InputStop("producer:baseline:identity_changed:" + label)
                self.meter.revalidated_bytes += read; self.meter.traversed["physical_hashed_bytes"] += read
                if self.meter.revalidated_bytes > RECHECK_BYTES_CAP: raise InputStop("producer:baseline:recheck_cap")
                transcript[label] = {"fd_rewound": True, "exact_length": read, "sha256": h.hexdigest(), "identity_match": True, "pathname_no_follow_match": True}
            except OSError as exc: raise InputStop("producer:baseline:revalidate_io:" + label) from exc
        return transcript
    def evict_workspace(self, workspace: Path) -> None:
        root = Path(os.path.abspath(workspace))
        for key in list(self.cache):
            if _inside(Path(key), root): del self.cache[key]; self.meter.release_payload("cache:" + key)
        if any(_inside(Path(key), root) for key in self.cache): raise InputStop("producer:cache:eviction")
    def close(self) -> None:
        for fd in list(self.handles.values()):
            try: os.close(fd)
            except OSError: pass
        self.handles.clear()
        for key in list(self.cache): del self.cache[key]; self.meter.release_payload("cache:" + key)

def parse_object(raw: bytes | bytearray, label: str, meter: Meter, exact: bool = False, retained_owner: str | None = None) -> dict[str, Any]:
    size = len(raw); meter.reserve("parsed_input_bytes", size); charged = False
    try:
        value = json.loads(raw); meter.charge("parsed_input_bytes", size); charged = True
        if type(value) is not dict: raise InputStop("producer:object:" + label)
        return value
    except json.JSONDecodeError as exc:
        raise InputStop("producer:json:" + label) from exc
    finally:
        if not charged: meter.release("parsed_input_bytes", size)

@dataclass
class CanonicalScan:
    body_sha256: str
    full_sha256: str
    rows_sha256: str | None
    chunks: list[tuple[int, int, str]]
    has_empty_word: bool

def _stream_mapping(value: Any, sink: Any, meter: Meter, purpose: str, special: dict[str, Any] | None = None) -> None:
    if type(value) is not dict:
        stream_canonical(value, sink, meter, purpose); return
    emit_token(b"{", sink, meter); first = True
    for key in sorted(value):
        if type(key) is not str: raise InputStop("producer:canonical:dict_key")
        if not first: emit_token(b",", sink, meter)
        first = False; stream_canonical(key, sink, meter, purpose + ":key"); emit_token(b":", sink, meter)
        if special is not None and key in special: special[key](value[key], sink)
        else: stream_canonical(value[key], sink, meter, purpose + ":" + key)
    emit_token(b"}", sink, meter)

def _stream_rows_for_receipt(value: Any, sink: Any, meter: Meter, purpose: str, holder: list[CanonicalScan | None]) -> None:
    if type(value) is not list:
        stream_canonical(value, sink, meter, purpose); return
    whole = hashlib.sha256(); chunk = hashlib.sha256(); chunks: list[tuple[int, int, str]] = []
    has_empty = False; in_chunk = 0; chunk_start = 1
    emit_token(b"[", sink, meter); whole.update(b"["); meter.traversed["row_digest_bytes"] += 1
    for pos, row in enumerate(value, 1):
        if pos != 1:
            emit_token(b",", sink, meter); whole.update(b","); meter.traversed["row_digest_bytes"] += 1
        if in_chunk == 0:
            chunk = hashlib.sha256(); chunk.update(b"["); meter.traversed["row_digest_bytes"] += 1; chunk_start = pos - 1
        else:
            chunk.update(b","); meter.traversed["row_digest_bytes"] += 1
        def row_sink(fragment: bytes) -> None:
            sink(fragment); whole.update(fragment); chunk.update(fragment); meter.traversed["row_digest_bytes"] += 2 * len(fragment)
        stream_canonical(row, row_sink, meter, purpose + ":row")
        if type(row) is dict and row.get("word") == []: has_empty = True
        in_chunk += 1
        if in_chunk == 1024 or pos == len(value):
            chunk.update(b"]"); meter.traversed["row_digest_bytes"] += 1
            chunks.append((chunk_start, pos, chunk.hexdigest())); in_chunk = 0
    emit_token(b"]", sink, meter); whole.update(b"]"); meter.traversed["row_digest_bytes"] += 1
    holder[0] = CanonicalScan("", "", whole.hexdigest(), chunks, has_empty)

def _stream_presentation(value: Any, sink: Any, meter: Meter, purpose: str, holder: list[CanonicalScan | None]) -> None:
    _stream_mapping(value, sink, meter, purpose, {"rows": lambda rows, target: _stream_rows_for_receipt(rows, target, meter, purpose + ":rows", holder)})

def _stream_delta0(value: Any, sink: Any, meter: Meter, purpose: str, holder: list[CanonicalScan | None]) -> None:
    _stream_mapping(value, sink, meter, purpose, {"presentation": lambda presentation, target: _stream_presentation(presentation, target, meter, purpose + ":presentation", holder)})

def scan_sealed(value: dict[str, Any], raw: bytes | bytearray, label: str, seal_key: str, meter: Meter) -> CanonicalScan:
    full = hashlib.sha256(); body = hashlib.sha256(); position = 0; raw_view = memoryview(raw); row_holder: list[CanonicalScan | None] = [None]
    def feed(fragment: bytes, to_body: bool) -> None:
        nonlocal position
        end = position + len(fragment)
        if end > len(raw_view) or raw_view[position:end] != fragment: raise InputStop("producer:json:noncanonical:" + label)
        full.update(fragment); position = end; meter.traversed["canonical_compared_bytes"] += len(fragment)
        if to_body: body.update(fragment); meter.traversed["seal_body_hashed_bytes"] += len(fragment)
    def token(data: bytes, to_body: bool) -> None:
        emit_token(data, lambda fragment: feed(fragment, to_body), meter)
    token(b"{", True); full_first = True; body_first = True
    for key in sorted(value):
        in_body = key != seal_key
        if not full_first:
            token(b",", in_body and not body_first)
        full_first = False
        key_sink = lambda fragment, include=in_body: feed(fragment, include)
        stream_canonical(key, key_sink, meter, label + ":key"); token(b":", in_body)
        if label == "receipt" and key == "Delta0":
            _stream_delta0(value[key], key_sink, meter, label + ":Delta0", row_holder)
        else:
            stream_canonical(value[key], key_sink, meter, label + ":" + key)
        if in_body: body_first = False
    token(b"}", True)
    if position != len(raw_view): raise InputStop("producer:json:noncanonical:" + label)
    row = row_holder[0]
    return CanonicalScan(body.hexdigest(), full.hexdigest(), None if row is None else row.rows_sha256, [] if row is None else row.chunks, False if row is None else row.has_empty_word)

def validate_seal(value: dict[str, Any], raw: bytes | bytearray, label: str, meter: Meter) -> CanonicalScan:
    if label == "receipt":
        if set(value) != TOP_RECEIPT_KEYS or "manifest_self_digest_sha256" in value: raise TraceReject("producer.transport.receipt_seal", "transport", "producer:transport:receipt_self_seal")
        key = "self_digest_sha256"
    else:
        if "self_digest_sha256" in value or type(value.get("manifest_self_digest_sha256")) is not str: raise TraceReject("producer.transport.manifest_seal", "transport", "producer:transport:manifest_self_seal")
        key = "manifest_self_digest_sha256"
    claimed = value.get(key); scan = scan_sealed(value, raw, label, key, meter)
    if type(claimed) is not str or claimed != scan.body_sha256: raise TraceReject("producer.transport." + label + ".self_seal", "transport", "producer:transport:" + label + "_self_seal")
    return scan

def validate_manifest(manifest: dict[str, Any], receipt_path: Path, receipt: dict[str, Any] | None, raw: bytes | bytearray | None, meter: Meter, raw_sha256: str | None = None) -> None:
    keys = set(MANIFEST_FIXED) | {"accepted", "accepted_receipt_basename", "receipt", "manifest_self_digest_sha256"}
    if set(manifest) != keys or "self_digest_sha256" in manifest: raise TraceReject("producer.authority.manifest_schema", "authority", "producer:authority:manifest_schema")
    if not strict_equal(manifest.get("schema"), MANIFEST_FIXED["schema"]) or type(manifest.get("synthetic")) is not bool or manifest.get("synthetic") is not False or type(manifest.get("independent")) is not bool or manifest.get("independent") is not True: raise TraceReject("producer.authority.manifest_flags", "authority", "producer:authority:manifest_flags")
    if type(manifest.get("accepted")) is not bool or manifest.get("accepted") is not True: raise TraceReject("producer.authority.manifest_acceptance", "authority", "producer:authority:manifest_acceptance")
    for key, expected in MANIFEST_FIXED.items():
        if key not in ("schema", "synthetic", "independent") and not strict_equal(manifest.get(key), expected): raise TraceReject("producer.authority.manifest_graph", "authority", "producer:authority:manifest_graph:" + key)
    binding = manifest.get("receipt")
    if type(binding) is not dict or set(binding) != {"basename", "bytes", "sha256", "self_digest_sha256"} or binding.get("basename") != receipt_path.name or not _positive_int(binding.get("bytes")) or type(binding.get("sha256")) is not str or type(binding.get("self_digest_sha256")) is not str: raise TraceReject("producer.authority.manifest_receipt_binding", "authority", "producer:authority:manifest_receipt_binding")
    if receipt is not None and raw is not None and (binding["bytes"] != len(raw) or binding["sha256"] != (raw_sha256 or digest_bytes(raw)) or binding["self_digest_sha256"] != receipt.get("self_digest_sha256")): raise TraceReject("producer.authority.manifest_receipt_binding", "authority", "producer:authority:manifest_receipt_binding")
    if manifest.get("accepted_receipt_basename") != receipt_path.name: raise TraceReject("producer.authority.manifest_receipt_binding", "authority", "producer:authority:manifest_receipt_binding")

def _typed_row(row: Any, pos: int) -> None:
    layer = "Gamma_Cayley" if pos <= 6318 else "action" if pos <= 6422 else "Q0_lift"; local = pos if layer == "Gamma_Cayley" else pos - 6318 if layer == "action" else pos - 6422
    if type(row) is not dict or set(row) != ROW_KEYS[layer] or type(row.get("layer")) is not str or row.get("layer") != layer or type(row.get("ordinal")) is not int or row.get("ordinal") != local or row.get("ordinal") <= 0: raise TraceReject("producer.authority.row_order", "authority", "producer:authority:layer_ordinal")
    ancestry = row.get("ancestry")
    if type(ancestry) is not dict or set(ancestry) != ANCESTRY_KEYS[layer] or any(not _word(ancestry[key]) for key in ancestry): raise TraceReject("producer.authority.row_shape", "authority", "producer:authority:row_shape")
    if not _word(row.get("word")): raise TraceReject("producer.authority.row_shape", "authority", "producer:authority:row_word")
    for key in ("target_state", "state", "generator", "record", "letter"):
        if key in row and not _positive_int(row[key]): raise TraceReject("producer.authority.row_shape", "authority", "producer:authority:row_type")
    if "orientation" in row and (type(row["orientation"]) is not int or row["orientation"] not in (-1, 1)): raise TraceReject("producer.authority.row_shape", "authority", "producer:authority:row_type")


def validate_rows(receipt: dict[str, Any], scan: CanonicalScan) -> str:
    delta0 = receipt.get("Delta0")
    presentation = delta0.get("presentation") if type(delta0) is dict else None
    if type(presentation) is not dict or set(presentation) != PRESENTATION_KEYS or type(delta0) is not dict or set(delta0) != {"marked_generators", "normal_closure_exact", "order", "presentation"}: raise TraceReject("producer.authority.row_order", "authority", "producer:authority:presentation_shape")
    if type(presentation.get("chunks")) is not list or type(presentation.get("layer_counts")) is not dict or not strict_equal(presentation["layer_counts"], LAYER_COUNTS) or type(presentation.get("normal_closure_exact")) is not bool or presentation["normal_closure_exact"] is not True or type(presentation.get("normal_generation")) is not bool or presentation["normal_generation"] is not True or type(presentation.get("resume_cursor")) is not int or presentation["resume_cursor"] != ROWS or presentation.get("source_word_encoding") != "literal strict signed F2 words; empty Cayley tree loops retained" or presentation.get("task172_legacy_rows_sha256") != LEGACY_ROWS_SHA: raise TraceReject("producer.authority.row_order", "authority", "producer:authority:presentation_types")
    rows = presentation.get("rows"); chunks = presentation.get("chunks")
    if type(rows) is not list or len(rows) != ROWS or type(presentation.get("row_count")) is not int or presentation["row_count"] != ROWS: raise TraceReject("producer.authority.row_order", "authority", "producer:authority:row_count")
    for pos, row in enumerate(rows, 1): _typed_row(row, pos)
    if type(chunks) is not list or len(chunks) != 7 or len(scan.chunks) != 7: raise TraceReject("producer.authority.row_order", "authority", "producer:authority:chunk_shape")
    for record, actual in zip(chunks, scan.chunks):
        start, end, sha = actual
        if type(record) is not dict or set(record) != CHUNK_KEYS or type(record.get("start")) is not int or type(record.get("end")) is not int or type(record.get("sealed")) is not bool or type(record.get("prefix_complete")) is not bool or type(record.get("sha256")) is not str or record["start"] != start or record["end"] != end or record["sealed"] is not True or record["prefix_complete"] is not True or record["sha256"] != sha: raise TraceReject("producer.authority.row_order", "authority", "producer:authority:chunk_shape")
    if scan.rows_sha256 is None or presentation.get("rows_sha256") != scan.rows_sha256 or scan.rows_sha256 != ROWS_SHA: raise TraceReject("producer.authority.row_order", "authority", "producer:authority:row_digest")
    if not scan.has_empty_word: raise TraceReject("producer.authority.row_order", "authority", "producer:authority:lossless_empty_word")
    return scan.rows_sha256

def validate_generation(receipt: dict[str, Any]) -> None:
    proof = receipt["Delta0"]["presentation"].get("normal_generation_proof")
    if type(proof) is not dict or not strict_equal(proof, GENERATION): raise TraceReject("producer.authority.normal_generation", "authority", "producer:authority:normal_generation_proof")


def validate_bridge(receipt: dict[str, Any], meter: Meter, expected_bridge: dict[str, Any] | None = None) -> dict[str, Any]:
    bridge = receipt.get("bridge")
    if type(bridge) is not dict or set(bridge) != BRIDGE_KEYS: raise TraceReject("producer.authority.bridge_occurrence", "authority", "producer:authority:bridge_shape")
    ledger = bridge.get("occurrence_ledger"); fields = {"block", "block_index", "block_slot", "context_id", "factor_sign", "fox_prefix_occurrences", "occurrence", "ordinal", "orientation", "role", "ten_index", "type"}
    if type(ledger) is not list or len(ledger) != 11: raise TraceReject("producer.authority.bridge_occurrence", "authority", "producer:authority:bridge_occurrence_ledger")
    for actual, expected in zip(ledger, OCCURRENCE_LEDGER):
        if type(actual) is not dict or set(actual) != fields or not strict_equal(actual, expected) or not all(type(actual[key]) is int for key in ("ordinal", "block_index", "block_slot", "context_id", "factor_sign", "ten_index")) or type(actual["fox_prefix_occurrences"]) is not list or not all(type(item) is int and item > 0 for item in actual["fox_prefix_occurrences"]): raise TraceReject("producer.authority.bridge_occurrence", "authority", "producer:authority:bridge_occurrence_ledger")
    if bridge.get("occurrence_ledger_sha256") != digest_object(ledger, meter, 100_000) or bridge.get("occurrence_ledger_sha256") != OCCURRENCE_LEDGER_SHA: raise TraceReject("producer.authority.bridge_occurrence", "authority", "producer:authority:bridge_occurrence_digest")
    if bridge.get("typed_coordinate_ledger_sha256") != digest_object(COORDINATE_OWNER, meter, 10_000) or bridge.get("typed_coordinate_ledger_sha256") != COORDINATE_LEDGER_SHA: raise TraceReject("producer.authority.bridge_occurrence", "authority", "producer:authority:coordinate_ledger")
    if type(bridge.get("branch")) is not str or bridge["branch"] != "ROOF_BRIDGE_ISOMORPHISM" or type(bridge.get("image_order")) is not int or bridge.get("image_order") != 357128352 or type(bridge.get("kernel_order")) is not int or bridge.get("kernel_order") != 1 or type(bridge.get("marked_replay_count")) is not int or bridge.get("marked_replay_count") != 4 or type(bridge.get("marked_inverse_count")) is not int or bridge.get("marked_inverse_count") != 4 or not strict_equal(bridge.get("ten_to_eleven"), [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9]) or not strict_equal(bridge.get("eleven_delete_duplicate"), [0, 1, 2, 3, 5, 6, 7, 8, 9, 10]) or not strict_equal(bridge.get("seven_blocks"), [[0, 1, 2], [3, 0, 4], [5], [6], [7], [8], [9]]): raise TraceReject("producer.authority.bridge_occurrence", "authority", "producer:authority:bridge_contract")
    if expected_bridge is not None and not strict_equal(bridge, expected_bridge): raise TraceReject("producer.authority.bridge_occurrence", "authority", "producer:authority:bridge_contract")
    return bridge


def _check_value(value: Any, width: int) -> bool:
    return type(value) is str and len(value) == 2 * width and all(ch in "0123456789abcdef" for ch in value)


def validate_abi(receipt: dict[str, Any], meter: Meter, expected_abi: dict[str, Any] | None = None) -> dict[str, Any]:
    if ABI_CANARIES is None: raise InputStop("producer:abi:canaries_not_initialized")
    evaluator = receipt.get("evaluator")
    if type(evaluator) is not dict or set(evaluator) != EVALUATOR_KEYS: raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    if evaluator.get("module") != "search/d972_r07_seven_context_roof_presentation_v1.py" or evaluator.get("relator_rows_sha256") != ROWS_SHA or evaluator.get("schema") != "d972-r07-v188-roof-consumer-action-abi/v1" or evaluator.get("runtime_constructor") != "load_runtime" or evaluator.get("registry_callable") != "v188_consumer_action_abi" or not strict_equal(evaluator.get("coordinate_widths"), COORDINATE_WIDTHS) or evaluator.get("coordinate_ledger_sha256") != COORDINATE_LEDGER_SHA or not strict_equal(evaluator.get("encoding"), ABI_ENCODING) or not strict_equal(evaluator.get("entry_points"), ABI_ENTRY_POINTS) or not strict_equal(evaluator.get("semantics"), ABI_SEMANTICS) or evaluator.get("context_maps") is not None or evaluator.get("joint_coordinate_image") is not None: raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    canaries = evaluator.get("canaries"); expected_keys = {"nonsplit_y_y_section_cocycle", "source_2_2", "x", "y", "x_inverse", "xy", "xy_section_cocycle", "x_action_y"}
    if type(canaries) is not dict or set(canaries) != expected_keys or canaries["nonsplit_y_y_section_cocycle"] is not None: raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    for name, word in (("x", [1]), ("y", [2]), ("x_inverse", [-1]), ("xy", [1, 2])):
        c = canaries[name]
        if type(c) is not dict or set(c) != {"word", "value"} or c["word"] != word or type(c["word"]) is not list or not _word(c["word"]) or type(c["value"]) is not list or len(c["value"]) != 10 or any(not _check_value(v, w) for v, w in zip(c["value"], COORDINATE_WIDTHS)): raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    source = canaries["source_2_2"]
    if type(source) is not dict or set(source) != {"gamma_state_id", "gamma_word", "q0_state_id", "q0_word", "source_word", "value"} or source.get("gamma_state_id") != 2 or source.get("q0_state_id") != 2 or source.get("q0_word") != [1] or not _word(source.get("gamma_word")) or not _word(source.get("source_word")) or type(source.get("value")) is not list or len(source["value"]) != 10 or any(not _check_value(v, w) for v, w in zip(source["value"], COORDINATE_WIDTHS)): raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    action = canaries["x_action_y"]
    if type(action) is not dict or set(action) != {"actor_word", "input", "value"} or action.get("actor_word") != [1] or type(action.get("input")) is not list or len(action["input"]) != 10 or any(not _check_value(v, w) for v, w in zip(action["input"], COORDINATE_WIDTHS)) or type(action.get("value")) is not list or len(action["value"]) != 10 or any(not _check_value(v, w) for v, w in zip(action["value"], COORDINATE_WIDTHS)): raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    cocycle = canaries["xy_section_cocycle"]
    if type(cocycle) is not dict or set(cocycle) != {"left", "right", "product", "value"} or cocycle.get("left") != [1] or cocycle.get("right") != [2] or cocycle.get("product") != [1, 2] or type(cocycle.get("value")) is not list or len(cocycle["value"]) != 10 or any(not _check_value(v, w) for v, w in zip(cocycle["value"], COORDINATE_WIDTHS)): raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    if not strict_equal(canaries, ABI_CANARIES): raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    if expected_abi is not None and not strict_equal(evaluator, expected_abi): raise TraceReject("producer.authority.evaluator_abi", "authority", "producer:authority:evaluator_abi_canary")
    return evaluator


def validate_receipt(raw: bytes | bytearray, events: EventSink, meter: Meter, expected_bridge: dict[str, Any] | None = None, expected_abi: dict[str, Any] | None = None, retained_owner: str | None = None, raw_sha256: str | None = None) -> dict[str, Any]:
    receipt = parse_object(raw, "receipt", meter); events.canonical_after["receipt"] = raw_sha256 or digest_bytes(raw); scan = validate_seal(receipt, raw, "receipt", meter)
    if receipt.get("schema") != "d972-r07-seven-context-roof-presentation/v1" or receipt.get("status") != "COMPLETE": raise TraceReject("producer.authority.receipt_envelope", "authority", "producer:authority:receipt_envelope")
    events.enter("producer.authority.row_order", "authority", "receipt.Delta0.presentation.rows"); row_digest = validate_rows(receipt, scan); events.rows_digest = row_digest
    events.enter("producer.authority.normal_generation", "authority", "receipt.Delta0.presentation.normal_generation_proof"); validate_generation(receipt)
    events.enter("producer.authority.bridge_occurrence", "authority", "receipt.bridge.occurrence_ledger"); validate_bridge(receipt, meter, expected_bridge)
    events.enter("producer.authority.evaluator_abi", "authority", "receipt.evaluator"); validate_abi(receipt, meter, expected_abi)
    return receipt


def validate_document_manifest(raw: bytes | bytearray, meter: Meter, owner: str | None = None) -> dict[str, Any]:
    manifest = parse_object(raw, "manifest", meter); validate_seal(manifest, raw, "manifest", meter); return manifest


def ordinary_route(manifest_path: Path, receipt_path: Path, workspace: Path | None, store: PhysicalStore, events: EventSink, meter: Meter, expected_bridge: dict[str, Any] | None = None, expected_abi: dict[str, Any] | None = None, owner: str | None = None) -> dict[str, Any]:
    manifest_owner = None if owner is None else owner + ":manifest"; receipt_owner = None if owner is None else owner + ":receipt"; mp = admit_path(manifest_path, "manifest", workspace, events); events.enter("producer.transport.manifest_open", "transport", "manifest.bytes"); mraw, mid = store.read(mp, "manifest", (MANIFEST_BYTES, MANIFEST_SHA) if workspace is None else None, events, workspace is None); events.enter("producer.transport.manifest_decode", "decode", "manifest.bytes"); manifest = validate_document_manifest(mraw, meter, manifest_owner); events.canonical_after["manifest"] = mid["sha256"]; rp = admit_path(receipt_path, "receipt", workspace, events); events.enter("producer.authority.manifest_acceptance", "authority", "manifest.accepted"); validate_manifest(manifest, rp, None, None, meter); events.enter("producer.transport.receipt_open", "transport", "receipt.bytes"); rraw, rid = store.read(rp, "receipt", (RECEIPT_BYTES, RECEIPT_SHA) if workspace is None else None, events, workspace is None); binding = manifest.get("receipt")
    if type(binding) is not dict or binding.get("bytes") != len(rraw) or binding.get("sha256") != rid["sha256"]:
        events.enter("producer.transport.receipt_identity", "transport", "manifest.receipt.{bytes,sha256}"); raise TraceReject("producer.transport.receipt_identity", "transport", "producer:transport:receipt_sha256")
    receipt = validate_receipt(rraw, events, meter, expected_bridge, expected_abi, receipt_owner, rid["sha256"]); validate_manifest(manifest, rp, receipt, rraw, meter, rid["sha256"])
    return {"manifest": manifest, "receipt": receipt, "manifest_raw": mraw, "receipt_raw": rraw, "manifest_identity": mid, "receipt_identity": rid, "paths": (mp, rp), "rows_digest": events.rows_digest}


def authenticate_sources(store: PhysicalStore, events: EventSink, meter: Meter) -> None:
    for path, size, sha in SOURCE_PINS:
        events.enter("producer.transport.source_pin", "transport", path); store.read(ROOT / path, path, (size, sha), events, True)


def load_fixture(store: PhysicalStore, meter: Meter, argument: str) -> dict[str, Any]:
    if Path(argument).is_absolute() or argument.replace("\\", "/") != FIXTURE_REL: raise InputStop("producer:fixture:path")
    raw, _ = store.read(ROOT / FIXTURE_REL, "fixture", (FIXTURE_BYTES, FIXTURE_SHA), retain_handle=True); fixture = parse_object(raw, "fixture", meter); body = dict(fixture); seal = body.pop("self_digest_sha256", None)
    if type(seal) is not str or seal != FIXTURE_SELF or seal != digest_object(body, meter, 1_000_000, "fixture_body") or fixture.get("schema") != SCHEMA + "/authority-fixture/v5": raise InputStop("producer:fixture:self_seal")
    if fixture.get("synthetic") is not False or fixture.get("candidate_only") is not True or fixture.get("full_a4_selftest") is not False or fixture.get("actual_a4_numerator") is not False or fixture.get("covered_rows") != [1, 2, 3, 4, 5, 6, 7] or fixture.get("remaining_rows") != list(range(8, 49)): raise InputStop("producer:fixture:scope")
    if fixture.get("immutable_input_identities") != {"task198_receipt": {"bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA, "self_digest_sha256": RECEIPT_SELF}, "task198_manifest": {"bytes": MANIFEST_BYTES, "sha256": MANIFEST_SHA, "manifest_self_digest_sha256": MANIFEST_SELF}}: raise InputStop("producer:fixture:immutable_inputs")
    expected_formula = {"opened_bytes_intended": INTENDED_OPENED_BYTES, "temporary_bytes_intended": INTENDED_TEMPORARY_BYTES, "parsed_input_bytes_intended": INTENDED_PARSED_INPUT_BYTES, "modeled_payload_tokens_intended": LARGEST_MODELED_PAYLOAD_TOKENS, "process_address_space_max_bytes": PROCESS_ADDRESS_SPACE_REQUEST}
    if fixture.get("resource_caps") != RESOURCE_CAPS or fixture.get("resource_formula") != expected_formula or INTENDED_OPENED_BYTES > CAPS["opened_bytes"] or INTENDED_TEMPORARY_BYTES > CAPS["temporary_bytes"] or INTENDED_PARSED_INPUT_BYTES > CAPS["parsed_input_bytes"] or LARGEST_MODELED_PAYLOAD_TOKENS > MODELED_PAYLOAD_TOKEN_CAP: raise InputStop("producer:fixture:resource_contract")
    if set(fixture.get("producer", {})) != set(MUTATIONS) or set(fixture.get("checker", {})) != set(MUTATIONS): raise InputStop("producer:fixture:rows")
    return fixture


def seal_receipt(value: dict[str, Any], meter: Meter, owner: str) -> SealedReceipt:
    body = dict(value)
    if "manifest_self_digest_sha256" in body: raise InputStop("producer:receipt:foreign_seal")
    body.pop("self_digest_sha256", None)
    self_seal = digest_object(body, meter, 35_000_000, owner + ":body")
    sealed = dict(body); sealed["self_digest_sha256"] = self_seal
    final, raw_sha = canonical_buffer(sealed, meter, 35_000_000, owner, owner + ":final")
    return SealedReceipt(sealed, final, raw_sha, len(final), self_seal)

def seal_manifest(value: dict[str, Any], meter: Meter, owner: str) -> SealedManifest:
    body = dict(value)
    if "self_digest_sha256" in body: raise InputStop("producer:manifest:foreign_seal")
    body.pop("manifest_self_digest_sha256", None)
    self_seal = digest_object(body, meter, 10_000, owner + ":body")
    sealed = dict(body); sealed["manifest_self_digest_sha256"] = self_seal
    final, raw_sha = canonical_buffer(sealed, meter, 10_000, owner, owner + ":final")
    return SealedManifest(sealed, final, raw_sha, len(final), self_seal)

def copy_manifest(manifest: dict[str, Any], receipt_path: Path, sealed: SealedReceipt, meter: Meter, owner: str) -> dict[str, Any]:
    if not isinstance(sealed, SealedReceipt) or sealed.byte_length != len(sealed.raw) or type(sealed.raw_sha256) is not str or sealed.self_seal != sealed.dom.get("self_digest_sha256"): raise InputStop("producer:reseal:receipt_tuple")
    out = dict(manifest)
    out["accepted_receipt_basename"] = receipt_path.name
    out["receipt"] = {"basename": receipt_path.name, "bytes": sealed.byte_length, "sha256": sealed.raw_sha256, "self_digest_sha256": sealed.self_seal}
    return out

def clone_small(value: dict[str, Any], meter: Meter, owner: str) -> dict[str, Any]:
    return dict(value)

def fresh_mutation_receipt(raw: bytes | bytearray, meter: Meter, owner: str) -> dict[str, Any]:
    return parse_object(raw, owner, meter)

def mutate_wire(source: bytes | bytearray, meter: Meter, owner: str) -> bytearray:
    size = len(source); meter.retain_payload(owner, size); complete = False
    try:
        changed = bytearray(source); changed[-1] ^= 1; complete = True; return changed
    finally:
        if not complete: meter.release_payload(owner)

def _mutate_receipt(receipt: dict[str, Any], name: str) -> None:
    if name == "per_layer_ordinal": receipt["Delta0"]["presentation"]["rows"][0]["ordinal"] += 1
    elif name == "normal_generation_proof": receipt["Delta0"]["presentation"]["normal_generation_proof"]["Gamma_cayley_edge_count"] += 1
    elif name == "bridge_typed_occurrence_ledger": receipt["bridge"]["occurrence_ledger"][0]["block"] = "H1_mutated"
    elif name == "evaluator_abi_canary": receipt["evaluator"]["coordinate_widths"][0] += 1


def _plan(name: str, workspace: Path, baseline: dict[str, Any], meter: Meter) -> tuple[MutationPlan, Path, Path]:
    mpath, rpath = baseline["paths"]
    if name == "authority_binding":
        changed = clone_small(baseline["manifest"], meter, "case:" + name + ":clone"); changed["accepted"] = False; mpath = workspace / MANIFEST_NAME; sealed = seal_manifest(changed, meter, "case:" + name + ":manifest_raw"); _write_case(mpath, sealed.raw, workspace, meter, sealed.raw_sha256); del changed, sealed; meter.release_prefix("case:" + name)
        plan = MutationPlan(name, "manifest", "authority.manifest.accepted", "file", "task198/manifest/accepted", mpath, ["manifest.manifest_self_digest_sha256"], reseal_dag=[{"node": "changed_manifest_body", "output": "manifest.manifest_self_digest_sha256+raw_sha256"}]); return plan, mpath, rpath
    if name == "canonical_input_bytes":
        changed = mutate_wire(baseline["receipt_raw"], meter, "case:" + name + ":wire"); rpath = workspace / RECEIPT_NAME; _write_case(rpath, changed, workspace, meter); del changed; meter.release_prefix("case:" + name)
        return MutationPlan(name, "receipt", "authority.receipt.raw_bytes", "file", "task198/receipt/raw-bytes", rpath, [], reseal_dag=[]), mpath, rpath
    if name == "resolved_path_traversal":
        outside = Path(tempfile.mkdtemp(prefix="d972-r07-a4-producer-outside-")); outside_path = outside / RECEIPT_NAME
        if _inside(outside, workspace) or _inside(outside, ROOT) or outside_path.exists():
            shutil.rmtree(outside, ignore_errors=False); raise InputStop("producer:row4:outside_owner_collision")
        return MutationPlan(name, "receipt", "authority.receipt.path", "path", "task198/receipt/path", outside_path, [], outside, []), mpath, outside_path
    changed = fresh_mutation_receipt(baseline["receipt_raw"], meter, "case:" + name + ":fresh_parse"); _mutate_receipt(changed, name); rpath = workspace / RECEIPT_NAME; sealed = seal_receipt(changed, meter, "case:" + name + ":receipt_raw"); changed = sealed.dom; _write_case(rpath, sealed.raw, workspace, meter, sealed.raw_sha256); changed_manifest = copy_manifest(baseline["manifest"], rpath, sealed, meter, "case:" + name + ":changed_manifest_clone"); mpath = workspace / MANIFEST_NAME; manifest_sealed = seal_manifest(changed_manifest, meter, "case:" + name + ":manifest_raw"); _write_case(mpath, manifest_sealed.raw, workspace, meter, manifest_sealed.raw_sha256)
    del changed, sealed, changed_manifest, manifest_sealed; meter.release_prefix("case:" + name)
    if name == "per_layer_ordinal": owner = "authority.receipt.Delta0.presentation.rows[0].ordinal"; logical = "task198/receipt/row-0001/ordinal"
    elif name == "normal_generation_proof": owner = "authority.receipt.Delta0.presentation.normal_generation_proof.Gamma_cayley_edge_count"; logical = "task198/receipt/normal-generation-proof"
    elif name == "bridge_typed_occurrence_ledger": owner = "authority.receipt.bridge.occurrence_ledger[0].block"; logical = "task198/receipt/bridge-occurrence-ledger"
    elif name == "evaluator_abi_canary": owner = "authority.receipt.evaluator.coordinate_widths[0]"; logical = "task198/receipt/evaluator-coordinate-abi"
    else: raise InputStop("producer:mutation:unknown:" + name)
    plan = MutationPlan(name, "receipt", owner, "file", logical, rpath, ["receipt.self_digest_sha256", "manifest.receipt.bytes", "manifest.receipt.sha256", "manifest.receipt.self_digest_sha256", "manifest.manifest_self_digest_sha256"])
    plan.reseal_dag = [{"node": "changed_receipt_body", "output": "receipt.self_digest_sha256"}, {"node": "receipt.self_digest_sha256", "output": "receipt.raw_sha256+byte_length"}, {"node": "receipt.raw_sha256+byte_length+self_digest_sha256", "output": "manifest.receipt.binding"}, {"node": "manifest.receipt.binding", "output": "changed_manifest_body"}, {"node": "changed_manifest_body", "output": "manifest.manifest_self_digest_sha256+raw_sha256"}]
    return plan, mpath, rpath


def _write_case(path: Path, raw: bytes | bytearray, workspace: Path, meter: Meter, expected_sha256: str | None = None) -> None:
    target = Path(os.path.abspath(path)); root = Path(os.path.abspath(workspace))
    if target.parent != root or not _inside(target, root): raise InputStop("producer:case:containment")
    if expected_sha256 is not None and (type(expected_sha256) is not str or len(expected_sha256) != 64): raise InputStop("producer:case:expected_sha256")
    size = len(raw); meter.reserve("temporary_bytes", size); meter.charge("temporary_bytes", size); meter.reserve("writes", 1); meter.charge("writes"); meter.reserve("opens", 2)
    remaining_open = 2; parent = -1; fd = -1; tmp: str | None = None; tmp_created: str | None = None; published = False; target_was_absent = False
    try:
        parent, leaf = _nofollow_parent(target); meter.charge("opens", 1); remaining_open -= 1
        parent_before = os.fstat(parent); parent_path_before = _nofollow_lstat(root)
        parent_identity = lambda st: (st.st_dev, st.st_ino, st.st_mode, st.st_nlink)
        if not stat.S_ISDIR(parent_before.st_mode) or parent_identity(parent_before) != parent_identity(parent_path_before): raise InputStop("producer:case:workspace_identity")
        try: os.stat(leaf, dir_fd=parent, follow_symlinks=False); raise InputStop("producer:case:stale_target")
        except FileNotFoundError: target_was_absent = True
        for _ in range(32):
            candidate = next(tempfile._get_candidate_names())
            try:
                fd = os.open(candidate, os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600, dir_fd=parent); tmp = candidate; tmp_created = candidate; break
            except FileExistsError: continue
        if fd < 0 or tmp is None: raise InputStop("producer:case:temp_name")
        meter.charge("opens", 1); remaining_open -= 1
        view = memoryview(raw); offset = 0; source_hash = None if expected_sha256 is not None else hashlib.sha256()
        while offset < size:
            chunk = view[offset:offset + 1_048_576]; written = os.write(fd, chunk)
            if written <= 0: raise InputStop("producer:case:short_write")
            if source_hash is not None: source_hash.update(chunk[:written]); meter.traversed["wire_source_hashed_bytes"] += written
            offset += written
        os.fsync(fd); written_stat = os.fstat(fd)
        if not stat.S_ISREG(written_stat.st_mode) or written_stat.st_nlink != 1 or written_stat.st_size != size: raise InputStop("producer:case:stage_identity")
        if os.lseek(fd, 0, os.SEEK_SET) != 0: raise InputStop("producer:case:rewind")
        h = hashlib.sha256(); remaining = size
        while remaining:
            request = min(IO_CHUNK_BYTES, remaining); chunk_owner = "io:case:" + str(target)
            meter.retain_payload(chunk_owner, request)
            try:
                part = os.read(fd, request)
                if not part: raise InputStop("producer:case:short_read")
                h.update(part); meter.traversed["case_stage_readback_hashed_bytes"] += len(part); remaining -= len(part); del part
            finally:
                meter.release_payload(chunk_owner)
        expected = expected_sha256 if expected_sha256 is not None else source_hash.hexdigest() if source_hash is not None else ""
        if h.hexdigest() != expected or not _stats_equal(written_stat, os.fstat(fd)): raise InputStop("producer:case:stage_sha256")
        try: os.link(tmp, leaf, src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)
        except TypeError as exc: raise InputStop("producer:case:no_follow_link_unsupported") from exc
        except FileExistsError as exc: raise InputStop("producer:case:stale_race") from exc
        published = True; os.unlink(tmp, dir_fd=parent)
        try: os.stat(tmp, dir_fd=parent, follow_symlinks=False); raise InputStop("producer:case:temp_present")
        except FileNotFoundError: pass
        tmp = None; os.fsync(parent)
        opened_final = os.fstat(fd); pathname_final = os.stat(leaf, dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISREG(opened_final.st_mode) or opened_final.st_nlink != 1 or opened_final.st_size != size or not _stats_equal(opened_final, pathname_final): raise InputStop("producer:case:final_identity")
        parent_after = os.fstat(parent); parent_path_after = _nofollow_lstat(root)
        if parent_identity(parent_before) != parent_identity(parent_after) or parent_identity(parent_after) != parent_identity(parent_path_after): raise InputStop("producer:case:workspace_identity")
    except Exception as exc:
        cleanup_errors: list[BaseException] = []
        if published:
            try: os.unlink(leaf, dir_fd=parent); published = False
            except BaseException as cleanup_exc: cleanup_errors.append(cleanup_exc)
        if tmp is not None:
            try: os.unlink(tmp, dir_fd=parent); tmp = None
            except FileNotFoundError: tmp = None
            except BaseException as cleanup_exc: cleanup_errors.append(cleanup_exc)
        if parent >= 0:
            try: os.fsync(parent)
            except BaseException as cleanup_exc: cleanup_errors.append(cleanup_exc)
            if target_was_absent and not published:
                try: os.stat(leaf, dir_fd=parent, follow_symlinks=False); cleanup_errors.append(InputStop("producer:case:rollback_present"))
                except FileNotFoundError: pass
            if tmp_created is not None:
                try: os.stat(tmp_created, dir_fd=parent, follow_symlinks=False); cleanup_errors.append(InputStop("producer:case:temp_present"))
                except FileNotFoundError: pass
        if cleanup_errors: raise InputStop("producer:case:rollback_failed") from cleanup_errors[0]
        if isinstance(exc, InputStop): raise
        raise InputStop("producer:case:atomic_write") from exc
    finally:
        if remaining_open: meter.release("opens", remaining_open)
        if fd >= 0:
            try: os.close(fd)
            except OSError: pass
        if parent >= 0: os.close(parent)


def _project(identity: dict[str, Any], logical: str, before: str, after: str) -> dict[str, Any]:
    readable = identity.get("exists") is True and identity.get("sha256") is not None
    return {"logical_case_path": logical, "owner_kind": identity.get("identity_kind"), "byte_length": identity.get("bytes") if readable else "UNREADABLE_AT_REGISTERED_STAGE", "content_sha256": identity.get("sha256") if readable else "UNREADABLE_AT_REGISTERED_STAGE", "link_count": identity.get("nlink") if identity.get("nlink") is not None else "UNREADABLE_AT_REGISTERED_STAGE", "symlink_or_reparse": identity.get("type") != "regular", "logical_link_target": "none" if identity.get("type") in ("regular", "missing") else identity.get("type"), "single_open_handle": identity.get("single_open_handle") is True, "opened_handle_stable": identity.get("opened_handle_stable") is True, "pathname_matches_opened_handle": identity.get("pathname_matches_opened_handle") is True, "substitution_detected": identity.get("substitution_detected") is True, "canonical_before_sha256": before, "canonical_after_sha256": after}


def _same_owner(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return all(a.get(k) == b.get(k) for k in ("path", "exists", "type", "mode", "bytes", "sha256", "device", "inode", "mtime_ns", "nlink"))


def run_mutation(name: str, baseline: dict[str, Any], fixture: dict[str, Any], meter: Meter, store: PhysicalStore, workspace: Path, pre_transcript: dict[str, Any]) -> dict[str, Any]:
    resource_before = meter.snapshot(); meter.reserve("mutations", 1); meter.charge("mutations", 1); plan, mpath, rpath = _plan(name, workspace, baseline, meter); before_key = plan.role + ("_path_identity" if plan.identity_kind == "path" else "_identity"); before = baseline[before_key]; events = EventSink(meter)
    try:
        if before.get("identity_kind") != plan.identity_kind: raise InputStop("producer:trace:before_identity_kind:" + name)
        try:
            ordinary_route(mpath, rpath, workspace, store, events, meter, baseline["expected_bridge"], baseline["expected_abi"], "case:" + name)
        except TraceReject as rejection:
            rejection.__traceback__ = None; events.terminal(); meter.release_prefix("case:" + name); after = events.observed.get(plan.role) or events.observed.get(plan.role + ".path")
            if after is None or _same_owner(before, after) or after.get("identity_kind") != plan.identity_kind: raise InputStop("producer:trace:owner_identity:" + name)
            expected = fixture["producer"][name]; first = {"validator": rejection.validator, "stage": rejection.stage, "narrow_reason": rejection.reason}; entered = [event["validator"] for event in events.events]
            if expected["owner"] != plan.owner or expected["identity_kind"] != plan.identity_kind or expected["logical_case_path"] != plan.logical_case_path or expected["ordinary_validator"] != rejection.validator or expected["stage"] != rejection.stage or expected["first_rejection"] != first or expected["allowed_downstream_reseals"] != plan.resealed_nodes or entered.count(rejection.validator) != 1 or events.terminal_count != 1: raise InputStop("producer:fixture:trace:" + name)
            source = plan.owner_path; hardlink = workspace / ".case-owner-link"
            if source.exists(): os.link(source, hardlink)
            if hardlink.exists(): os.unlink(hardlink)
            if hardlink.exists(): raise InputStop("producer:workspace:hardlink_eviction:" + name)
            store.evict_workspace(workspace); shutil.rmtree(workspace, ignore_errors=False) if workspace.exists() else None; workspace_removed = not workspace.exists()
            outside_removed = True
            if plan.outside_parent is not None:
                shutil.rmtree(plan.outside_parent, ignore_errors=False); outside_removed = not plan.outside_parent.exists() and not plan.owner_path.exists()
            owner_disposed = (not plan.owner_path.exists()) and workspace_removed and outside_removed
            if not owner_disposed: raise InputStop("producer:workspace:dispose:" + name)
            post_transcript = store.revalidate_all(baseline["authority_handles"])
            return {"id": name, "owner": plan.owner, "identity_kind": plan.identity_kind, "before_identity": _project(before, plan.logical_case_path, before["sha256"] or "UNREADABLE_AT_REGISTERED_STAGE", before["sha256"] or "UNREADABLE_AT_REGISTERED_STAGE"), "after_identity": _project(after, plan.logical_case_path, before["sha256"] or "UNREADABLE_AT_REGISTERED_STAGE", events.canonical_after.get(plan.role, "UNREADABLE_AT_REGISTERED_STAGE")), "resealed_nodes": list(plan.resealed_nodes), "semantic_reseal_dag": list(plan.reseal_dag or []), "entered_validators": entered, "first_rejection": first, "event_trace_digest": events.digest(), "terminal_count": events.terminal_count, "baseline_revalidated": True, "baseline_revalidation_transcript": {"before": pre_transcript, "after": post_transcript}, "owner_disposed": owner_disposed, "disposal_proof": {"workspace_absent": workspace_removed, "outside_owner_absent": outside_removed, "cache_evicted": True}, "resource_before": resource_before, "resource_after": meter.snapshot()}
        raise MutationAccepted("producer:mutation_accepted:" + name)
    finally:
        if plan.outside_parent is not None and plan.outside_parent.exists(): shutil.rmtree(plan.outside_parent, ignore_errors=False)


def _recheck_plan(store: PhysicalStore, baseline: dict[str, Any]) -> dict[str, Any]: return store.revalidate_all(baseline["authority_handles"])


def execute(fixture: dict[str, Any], meter: Meter, store: PhysicalStore) -> dict[str, Any]:
    events = EventSink(meter); authenticate_sources(store, events, meter); baseline = ordinary_route(ROOT / MANIFEST_REL, ROOT / RECEIPT_REL, None, store, events, meter, owner="baseline")
    baseline["expected_bridge"] = baseline["receipt"]["bridge"]; baseline["expected_abi"] = baseline["receipt"]["evaluator"]; del baseline["receipt"]
    handles: dict[str, dict[str, Any]] = {}
    for index, (path, _, _) in enumerate(SOURCE_PINS, 1):
        key = str(Path(os.path.abspath(ROOT / path))); handles[key] = {"label": "source_pin_" + str(index), "identity": store.cache[key][1]}
    for key, label in ((str(Path(os.path.abspath(ROOT / FIXTURE_REL))), "fixture"), (str(Path(os.path.abspath(ROOT / MANIFEST_REL))), "manifest"), (str(Path(os.path.abspath(ROOT / RECEIPT_REL))), "receipt")):
        handles[key] = {"label": label, "identity": store.cache[key][1]}
    baseline["authority_handles"] = handles; baseline["rows_digest"] = baseline["rows_digest"] or ROWS_SHA; baseline["receipt_canonical"] = baseline["receipt_identity"]["sha256"]; baseline["manifest_canonical"] = baseline["manifest_identity"]["sha256"]; baseline["receipt_path_identity"] = _path_identity(baseline["paths"][1], "path"); records = []
    for name in MUTATIONS:
        if any(owner.startswith("case:") for owner in meter.payload_owners): raise InputStop("producer:case:prior_owner_live")
        workspace = Path(tempfile.mkdtemp(prefix="d972-r07-a4-producer-"))
        if _inside(workspace, ROOT): shutil.rmtree(workspace); raise InputStop("producer:workspace:repository_overlap")
        record: dict[str, Any] | None = None
        try:
            pre = _recheck_plan(store, baseline); record = run_mutation(name, baseline, fixture, meter, store, workspace, pre); records.append(record)
        finally:
            store.evict_workspace(workspace); shutil.rmtree(workspace, ignore_errors=True); meter.release_prefix("case:" + name)
            if record is not None: record["resource_after"] = meter.snapshot()
            if any(owner.startswith("case:") for owner in meter.payload_owners): raise InputStop("producer:case:owner_leak")
    expected_counts = {"opened_bytes": INTENDED_OPENED_BYTES, "temporary_bytes": INTENDED_TEMPORARY_BYTES, "parsed_input_bytes": INTENDED_PARSED_INPUT_BYTES, "opens": METERED_LOGICAL_OPENS, "writes": INTENDED_WRITES, "events": INTENDED_EVENTS, "mutations": len(MUTATIONS)}
    if any(meter.counts[key] != value for key, value in expected_counts.items()) or meter.revalidated_bytes != INTENDED_REVALIDATED_BYTES or any(meter.reserved.values()) or meter.payload_live != AUTHORITY_RAW_PAYLOAD_TOKENS or meter.payload_peak != LARGEST_MODELED_PAYLOAD_TOKENS: raise InputStop("producer:meter:final_account")
    result = {"schema": SCHEMA, "candidate_only": True, "synthetic": False, "covered_rows": [1, 2, 3, 4, 5, 6, 7], "remaining_rows": list(range(8, 49)), "full_a4_selftest": False, "actual_a4_numerator": False, "baseline": {"receipt_canonical_sha256": baseline["receipt_canonical"], "manifest_canonical_sha256": baseline["manifest_canonical"], "rows_sha256": baseline["rows_digest"], "baseline_revalidated": records[-1]["baseline_revalidated"]}, "rows": records, "resource": meter.public()}
    del baseline
    return result

def install_address_space_limit() -> int:
    if os.name != "posix" or not sys.platform.startswith("linux") or resource is None or not hasattr(resource, "RLIMIT_AS"): raise InputStop("producer:address_space:unsupported")
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        candidates = [PROCESS_ADDRESS_SPACE_REQUEST]
        if soft != resource.RLIM_INFINITY: candidates.append(int(soft))
        if hard != resource.RLIM_INFINITY: candidates.append(int(hard))
        target = min(candidates)
        if target <= 0 or target >= PROCESS_ADDRESS_SPACE_CEILING: raise InputStop("producer:address_space:ineffective")
        resource.setrlimit(resource.RLIMIT_AS, (target, hard))
        installed, installed_hard = resource.getrlimit(resource.RLIMIT_AS)
        if int(installed) != target or installed == resource.RLIM_INFINITY or int(installed) >= PROCESS_ADDRESS_SPACE_CEILING or installed_hard != hard: raise InputStop("producer:address_space:readback")
        return int(installed)
    except InputStop:
        raise
    except (OSError, ValueError, AttributeError) as exc:
        raise InputStop("producer:address_space:unavailable") from exc

def seal_result(value: dict[str, Any], meter: Meter) -> dict[str, Any]:
    body = dict(value); body.pop("self_digest_sha256", None)
    seal = digest_object(body, meter, 35_000_000, "result_body")
    body["self_digest_sha256"] = seal
    return body

def write_canonical_stdout(value: dict[str, Any], meter: Meter) -> None:
    for fragment in canonical_fragments(value, meter, "stdout"):
        meter.traversed["stdout_canonical_bytes"] += len(fragment)
        view = memoryview(fragment); offset = 0
        while offset < len(view):
            written = sys.stdout.buffer.write(view[offset:])
            if type(written) is not int or written <= 0: raise InputStop("producer:stdout:short_write")
            offset += written
        view.release()
    sys.stdout.buffer.flush()

def main(argv: list[str] | None = None) -> int:
    global ABI_CANARIES, PROCESS_ADDRESS_SPACE_LIMIT_ACTIVE
    parser = argparse.ArgumentParser(); parser.add_argument("--fixture", default=FIXTURE_REL); parser.add_argument("--output"); args = parser.parse_args(argv)
    if args.output is not None: raise InputStop("producer:output:publisher_removed")
    PROCESS_ADDRESS_SPACE_LIMIT_ACTIVE = install_address_space_limit()
    try:
        ABI_CANARIES = json.loads(ABI_CANARIES_RAW)
    except json.JSONDecodeError as exc:
        raise InputStop("producer:abi:literal") from exc
    meter = Meter(); store = PhysicalStore(meter); fixture: dict[str, Any] | None = None
    try:
        fixture = load_fixture(store, meter, args.fixture); result = execute(fixture, meter, store); del fixture
        sealed = seal_result(result, meter); write_canonical_stdout(sealed, meter)
        return 0
    finally:
        store.close()

if __name__ == "__main__": raise SystemExit(main())
