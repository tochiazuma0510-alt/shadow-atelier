#!/usr/bin/env python3
"""Task362 checker-side independent rows 1--7 authority trace.

No producer module is imported.  All physical reads, codecs, validators,
mutation constructors, and evidence projections below are checker-owned.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a4-actual-owner-trace/v3"
FIXTURE_REL = "search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v3_20260829.json"
FIXTURE_BYTES = 8_457
FIXTURE_SHA = "0d58bace814a7b838f7bf08a91ca7e1eea79e7d4d5099b52281ea7cce61ed225"
FIXTURE_SELF = "faa301467e8c5047b192da539467409631cdd9abe5a480f18aa175926b897a14"
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
LAYER_COUNTS = {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19}
COORDINATE_WIDTHS = [40, 40, 40, 40, 40, 154, 154, 154, 154, 154]
COORDINATE_LEDGER_SHA = "9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c"
OCCURRENCE_LEDGER_SHA = "040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7"
CAPS = {"opened_bytes": 250_000_000, "temporary_bytes": 250_000_000, "canonical_bytes": 750_000_000, "dom_bytes": 1_500_000_000, "peak_live_bytes": 750_000_000, "opens": 256, "writes": 256, "events": 10_000, "mutations": 7}
RECHECK_BYTES_CAP = 750_000_000

COORDINATE_OWNER = [
    {"construction": "d_E(C21)", "context_id": 21, "index": 0, "role": "hexagon_fxy", "source": "(x,y)", "type": "E3"}, {"construction": "d_E(C22)", "context_id": 22, "index": 1, "role": "hexagon_fxz", "source": "(x,z)", "type": "E3"}, {"construction": "d_E(C23)", "context_id": 23, "index": 2, "role": "hexagon_fyz", "source": "(y,z)", "type": "E3"}, {"construction": "d_E(C24)", "context_id": 24, "index": 3, "role": "hexagon_fux", "source": "(u,x)", "type": "E3"}, {"construction": "d_E(C25)", "context_id": 25, "index": 4, "role": "hexagon_fuy", "source": "(u,y)", "type": "E3"}, {"construction": "C1", "context_id": 1, "index": 5, "role": "pentagon_b1", "source": "b1/phi234", "type": "E4"}, {"construction": "C27", "context_id": 27, "index": 6, "role": "pentagon_b2", "source": "b2/phi1_23_4", "type": "E4"}, {"construction": "C21", "context_id": 21, "index": 7, "role": "pentagon_b3", "source": "b3/phi123", "type": "E4"}, {"construction": "C26", "context_id": 26, "index": 8, "role": "pentagon_b5_inverse_slot", "source": "b5/phi12_3_4", "type": "E4"}, {"construction": "C28", "context_id": 28, "index": 9, "role": "pentagon_b4_inverse_slot", "source": "b4/phi1_2_34", "type": "E4"},
]
OCCURRENCE_LEDGER = [
    {"ordinal": 1, "block": "H1", "block_index": 1, "block_slot": 1, "occurrence": "H1_fxy", "type": "E3", "ten_index": 0, "context_id": 21, "role": "hexagon_fxy", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [3, 2]}, {"ordinal": 2, "block": "H1", "block_index": 1, "block_slot": 2, "occurrence": "H1_fxz", "type": "E3", "ten_index": 1, "context_id": 22, "role": "hexagon_fxz", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [3]}, {"ordinal": 3, "block": "H1", "block_index": 1, "block_slot": 3, "occurrence": "H1_fyz", "type": "E3", "ten_index": 2, "context_id": 23, "role": "hexagon_fyz", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": []}, {"ordinal": 4, "block": "H2", "block_index": 2, "block_slot": 1, "occurrence": "H2_fux", "type": "E3", "ten_index": 3, "context_id": 24, "role": "hexagon_fux", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [6, 5]}, {"ordinal": 5, "block": "H2", "block_index": 2, "block_slot": 2, "occurrence": "H2_fxy", "type": "E3", "ten_index": 0, "context_id": 21, "role": "hexagon_fxy", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [6]}, {"ordinal": 6, "block": "H2", "block_index": 2, "block_slot": 3, "occurrence": "H2_fuy", "type": "E3", "ten_index": 4, "context_id": 25, "role": "hexagon_fuy", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": []}, {"ordinal": 7, "block": "P1", "block_index": 3, "block_slot": 1, "occurrence": "P_b1", "type": "E4", "ten_index": 5, "context_id": 1, "role": "pentagon_b1", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9, 8]}, {"ordinal": 8, "block": "P2", "block_index": 4, "block_slot": 1, "occurrence": "P_b2", "type": "E4", "ten_index": 6, "context_id": 27, "role": "pentagon_b2", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10, 9]}, {"ordinal": 9, "block": "P3", "block_index": 5, "block_slot": 1, "occurrence": "P_b3", "type": "E4", "ten_index": 7, "context_id": 21, "role": "pentagon_b3", "factor_sign": 1, "orientation": "direct", "fox_prefix_occurrences": [11, 10]}, {"ordinal": 10, "block": "P5", "block_index": 6, "block_slot": 1, "occurrence": "P_b5_inverse", "type": "E4", "ten_index": 8, "context_id": 26, "role": "pentagon_b5_inverse_slot", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": [11]}, {"ordinal": 11, "block": "P4", "block_index": 7, "block_slot": 1, "occurrence": "P_b4_inverse", "type": "E4", "ten_index": 9, "role": "pentagon_b4_inverse_slot", "source": "", "factor_sign": -1, "orientation": "inverse", "fox_prefix_occurrences": []},
]
# Normalize the independent literal's final entry to the typed ledger shape.
OCCURRENCE_LEDGER[-1].pop("source", None)
SOURCE_PINS = (
    ("ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt", 81, "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"), ("ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt", 95, "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"), ("ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json", 150, "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"), ("search/d972_r07_seven_context_roof_presentation_v1.py", 137169, "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"), ("crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", 157253, "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"), ("search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", 20541, "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"),
)
SOURCE_PIN_BYTES = sum(size for _, size, _ in SOURCE_PINS)
INTENDED_OPENED_BYTES = SOURCE_PIN_BYTES + FIXTURE_BYTES + RECEIPT_BYTES + MANIFEST_BYTES + 3 * (RECEIPT_BYTES + MANIFEST_BYTES) + (RECEIPT_BYTES + 8 + MANIFEST_BYTES) + (MANIFEST_BYTES + 1) + RECEIPT_BYTES
INTENDED_TEMPORARY_BYTES = 3 * (RECEIPT_BYTES + MANIFEST_BYTES) + (RECEIPT_BYTES + 8 + MANIFEST_BYTES) + (MANIFEST_BYTES + 1) + RECEIPT_BYTES
PARSED_BYTES = FIXTURE_BYTES + 4 * (RECEIPT_BYTES + MANIFEST_BYTES) + (RECEIPT_BYTES + 8 + MANIFEST_BYTES) + (MANIFEST_BYTES + 1) + MANIFEST_BYTES + MANIFEST_BYTES
BASELINE_PEAK_BYTES = 2 * SOURCE_PIN_BYTES + 8 * FIXTURE_BYTES + 8 * MANIFEST_BYTES + 8 * RECEIPT_BYTES
LARGEST_INTENDED_PEAK = BASELINE_PEAK_BYTES + 2 * (RECEIPT_BYTES + 8 + MANIFEST_BYTES) + 6 * (RECEIPT_BYTES + 8 + MANIFEST_BYTES) + 200_000_000 + 10_000 + (RECEIPT_BYTES + 8)
INTENDED_DOM_BYTES = INTENDED_OPENED_BYTES + PARSED_BYTES + 4 * 200_000_000 + 4 * 10_000 + 10_000 + RECEIPT_BYTES
METERED_LOGICAL_OPENS = 19 + 20 + 14
INTENDED_WRITES = 10
INTENDED_EVENTS = 16 + 50
MUTATIONS = ("per_layer_ordinal", "authority_binding", "canonical_input_bytes", "resolved_path_traversal", "normal_generation_proof", "bridge_typed_occurrence_ledger", "evaluator_abi_canary")
ROW_KEYS = {"Gamma_Cayley": {"ancestry", "generator", "layer", "ordinal", "state", "target_state", "word"}, "action": {"ancestry", "layer", "letter", "ordinal", "orientation", "record", "target_state", "word"}, "Q0_lift": {"ancestry", "layer", "ordinal", "target_state", "word"}}
ANCESTRY_KEYS = {"Gamma_Cayley": {"record_word", "section_source_word", "section_target_word"}, "action": {"record_word", "section_target_word", "tokens"}, "Q0_lift": {"q0_relator_word", "section_target_word"}}
BRIDGE_KEYS = {"branch", "eleven_delete_duplicate", "image_order", "inverse_algorithm", "kernel_order", "marked_inverse_count", "marked_replay", "marked_replay_count", "occurrence_ledger", "occurrence_ledger_sha256", "order_computation", "relator_replay", "seven_blocks", "ten_to_eleven", "typed_coordinate_ledger_sha256"}
EVALUATOR_KEYS = {"canaries", "context_maps", "coordinate_ledger_sha256", "coordinate_widths", "encoding", "entry_points", "joint_coordinate_image", "module", "registry_callable", "relator_rows_sha256", "runtime_constructor", "schema", "semantics"}
TOP_RECEIPT_KEYS = {"D_all", "Delta0", "Gamma", "Ihara_witness", "Q0", "bridge", "cofinal_lift", "direct_Delta_states_enumerated", "evaluator", "fake", "input", "million_row_Q0_Schreier_stream", "resource", "resume", "schema", "self_digest_sha256", "status", "terminal"}
PRESENTATION_KEYS = {"chunks", "layer_counts", "normal_closure_exact", "normal_generation", "normal_generation_proof", "resume_cursor", "row_count", "rows", "rows_sha256", "source_word_encoding", "task172_legacy_rows_sha256"}
CHUNK_KEYS = {"end", "prefix_complete", "sealed", "sha256", "start"}
ABI_ENCODING = {"roof_value": "ten lowercase hex typed coordinate blobs", "source_word": "strict signed F2 list", "state_ids": "one-based Gamma and Q0 ids"}
ABI_ENTRY_POINTS = {"action": {"arguments": ["runtime", "actor_word", "value"], "callable": "roof_action"}, "eval": {"arguments": ["runtime", "word"], "callable": "roof_eval"}, "inverse": {"arguments": ["runtime", "value"], "callable": "roof_inverse"}, "multiply": {"arguments": ["runtime", "left", "right"], "callable": "roof_multiply"}, "section_cocycle": {"arguments": ["runtime", "left_section_word", "right_section_word", "product_section_word"], "callable": "roof_section_cocycle"}, "source_section": {"arguments": ["runtime", "gamma_state_id", "q0_state_id"], "callable": "roof_source_section"}}
ABI_SEMANTICS = {"action": "actor*value*actor_inverse", "multiplication": "left_then_right", "section_cocycle": "s_left*s_right*s_product_inverse"}
ABI_CANARIES = json.loads(r'''{"nonsplit_y_y_section_cocycle":null,"source_2_2":{"gamma_state_id":2,"gamma_word":[1,1,-2,1,1,2,2,1,1,1,2,1,1,-2,-1,-2,-1,-1,2,-1,-1,-2,1,1,2,1,1,-2,1,1,-2,1,1,2,1,1,-2,1,1,2,2,1,1,1,2,1,1,-2,-1,-2,-1,-1,2,-1,-1,-2,1,1,2,1,1,-2,1,1,-2,1,1,2],"q0_state_id":2,"q0_word":[1],"source_word":[1,1,-2,1,1,2,2,1,1,1,2,1,1,-2,-1,-2,-1,-1,2,-1,-1,-2,1,1,2,1,1,-2,1,1,-2,1,1,2,1,1,-2,1,1,2,2,1,1,1,2,1,1,-2,-1,-2,-1,-1,2,-1,-1,-2,1,1,2,1,1,-2,1,1,-2,1,1,2,1],"value":["0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000001","0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000002","0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000101","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000202","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000200","080704020001030605090a0b0c0d0e0f101112131415161718191a221e211f1d231b201c25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a79787785867e7f808182838488878f8e8d8c8b8a8900000001000000000001","00010203040506070811100d0b090a0c0f0e1a19161412131518171d21221f1b1c23201e2425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e40414243444546473f48504f4e4d4c4b4a495159585756555453525b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d787776757d7c7b7a7985867e7f80818283848f8e8d8c8b8a89888701010000000002010100","000102030405060708090a0b0c0d0e0f1011141a1819151213171623221f1d1b1c1e21202425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f5051525354555657585961625a5b5c5d5e5f60636b6a6968676665646c74737271706f6e6d767778797a7b7c7d757e868584838281807f878f8e8d8c8b8a898801000000000001000000","08070402000103060511100d0b090a0c0f0e12131415161718191a1c231f1d22211b201e25262728292a2b2c242d3534333231302f2e363e3d3c3b3a39383740414243444546473f48504f4e4d4c4b4a495159585756555453525a5b5c5d5e5f606162636465666768696a6b6c6d6e6f70717273747c7d75767778797a7b8584838281807f7e868988878f8e8d8c8b8a00010001000002000101","000102030405060708090a0b0c0d0e0f10111a191614121315181723221f1d1b1c1e21202425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d767778797a7b7c7d757e868584838281807f878f8e8d8c8b8a898801000000000001010000"]},"x":{"value":["0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000000","0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000000","0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000201","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000201","080704020001030605090a0b0c0d0e0f101112131415161718191a1c21201b221f231e1d25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001000000000000","00010203040506070811100d0b090a0c0f0e1a19161412131518171c1f2122201e1b231d2425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e40414243444546473f48504f4e4d4c4b4a495159585756555453525b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d787776757d7c7b7a797f808182838485867e8f8e8d8c8b8a89888701010000000002000000","000102030405060708090a0b0c0d0e0f10111a191614121315181723221f1d1b1c1e21202425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d767778797a7b7c7d757e868584838281807f878f8e8d8c8b8a898801000000000000000000","08070402000103060511100d0b090a0c0f0e12131415161718191a1d1f21201b231e1c2225262728292a2b2c242d3534333231302f2e363e3d3c3b3a39383740414243444546473f48504f4e4d4c4b4a495159585756555453525a5b5c5d5e5f606162636465666768696a6b6c6d6e6f7071727374767778797a7b7c7d758584838281807f7e868988878f8e8d8c8b8a00010001000002000000","000102030405060708090a0b0c0d0e0f10111a191614121315181723221f1d1b1c1e21202425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d767778797a7b7c7d757e868584838281807f878f8e8d8c8b8a898801000000000000000000"],"word":[1]},"x_action_y":{"actor_word":[1],"input":["0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0502070108060400030b0a0911100f0e0d0c1a19181716151413121c1d1e1f202122231b02000200","0502070108060400030b0a0911100f0e0d0c1a19181716151413121c1d1e1f202122231b02000200","0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000000","0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0106050007040803020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f2021222325242c2b2a292827262e2f3031323334352d37363e3d3c3b3a3938403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000000","0204060500080301070a0f0e09100d110c0b1318171219161a15141b1c1d1e1f2021222325262728292a2b2c2434333231302f2e2d353837363e3d3c3b3a39403f47464544434241494a4b4c4d4e4f50485251595857565554535b5a6261605f5e5d5c6465666768696a6b636d6c74737271706f6e75767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000010100000002","080704020001030605090a0b0c0d0e0f101112131415161718191a1c21201b221f231e1d25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001000000000000","0106050007040803020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f2021222325242c2b2a292827262e2f3031323334352d37363e3d3c3b3a3938403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000000","010406070503000802090a0b0c0d0e0f10111318171219161a15141c21201b221f231e1d272625242c2b2a29282e2f3031323334352d3e3d3c3b3a393837363f404142434445464748494a4b4c4d4e4f505152535455565758595b5a6261605f5e5d5c6465666768696a6b636d6c74737271706f6e76757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001010000000002"],"value":["03060108050704000211100f0e0d0c0b0a091a1213141516171819232221201f1e1d1c1b00000102","0604000108030502070911100f0e0d0c0b0a13121a191817161514231b1c1d1e1f20212202000201","0805010203060700040911100f0e0d0c0b0a181716151413121a19231b1c1d1e1f20212202000202","05020408060703010011090a0b0c0d0e0f101413121a19181716151d1c1b232221201f1e01000002","04080300070201060511100f0e0d0c0b0a091a12131415161718191e1d1c1b232221201f00000101","0306010805070400020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f202122232c2b2a292827262524352d2e2f30313233343e3d3c3b3a39383736403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000002","0204060500080301070c0f0a110e100d090b1518131a17191612141b1c1d1e1f2021222325262728292a2b2c2434333231302f2e2d353837363e3d3c3b3a3947464544434241403f5048494a4b4c4d4e4f5958575655545352516261605f5e5d5c5b5a6b636465666768696a74737271706f6e6d6c75767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000010100020202","080704020001030605090a0b0c0d0e0f101112131415161718191a1e211c2320221f1b1d25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f70717273747d7c7b7a7978777675867e7f8081828384858f8e8d8c8b8a89888700000001000002000000","0306010805070400020c0f0a110e100d090b12131415161718191a1b1c1d1e1f202122232c2b2a292827262524352d2e2f30313233343e3d3c3b3a3938373647464544434241403f5048494a4b4c4d4e4f5958575655545352515a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000202","010406070503000802090a0b0c0d0e0f10111518131a17191612141e211c2320221f1b1d272625242c2b2a29282e2f3031323334352d3e3d3c3b3a393837363f404142434445464748494a4b4c4d4e4f505152535455565758596261605f5e5d5c5b5a6b636465666768696a74737271706f6e6d6c7d7c7b7a7978777675867e7f8081828384858f8e8d8c8b8a89888700000001010002020002"]},"x_inverse":{"value":["04050306020807010011090a0b0c0d0e0f10121a191817161514131b232221201f1e1d1c02000000","04050306020807010011090a0b0c0d0e0f10121a191817161514131b232221201f1e1d1c02000000","0300080705020104060a0911100f0e0d0c0b1a12131415161718191c1b232221201f1e1d00000200","0203070501060008040911100f0e0d0c0b0a13121a1918171615141c1d1e1f202122231b01000100","0203070501060008040911100f0e0d0c0b0a13121a1918171615141c1d1e1f202122231b01000100","040503060208070100090a0b0c0d0e0f101112131415161718191a1e1b2322201d1c1f212c2425262728292a2b2d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a797877867e7f80818283848588878f8e8d8c8b8a8900000002000000000000","0001020304050607080d0e0c0f0b11100a0916171518141a191312211b23201c1f1d1e222425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e473f4041424344454648504f4e4d4c4b4a49515958575655545352625a5b5c5d5e5f6061636b6a6968676665646c74737271706f6e6d787776757d7c7b7a79867e7f8081828384858f8e8d8c8b8a89888702020000000000000000","000102030405060708090a0b0c0d0e0f101116171518141a1913121f201e211d23221c1b2425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f50515253545556575859625a5b5c5d5e5f6061636b6a6968676665646c74737271706f6e6d7d75767778797a7b7c7e868584838281807f878f8e8d8c8b8a898802000000000000000000","0405030602080701000d0e0c0f0b11100a0912131415161718191a1f221b211c1e1d23202c2425262728292a2b2d3534333231302f2e363e3d3c3b3a393837473f4041424344454648504f4e4d4c4b4a495159585756555453525a5b5c5d5e5f606162636465666768696a6b6c6d6e6f70717273747d75767778797a7b7c8584838281807f7e868988878f8e8d8c8b8a00020002000000000000","000102030405060708090a0b0c0d0e0f101116171518141a1913121f201e211d23221c1b2425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f50515253545556575859625a5b5c5d5e5f6061636b6a6968676665646c74737271706f6e6d7d75767778797a7b7c7e868584838281807f878f8e8d8c8b8a898802000000000000000000"],"word":[-1]},"xy":{"value":["0203070501060008040911100f0e0d0c0b0a13121a1918171615141c1d1e1f202122231b01000100","0300080705020104060a0911100f0e0d0c0b1a12131415161718191c1b232221201f1e1d00000200","0204060500080301070a0b0c0d0e0f10110919181716151413121a1d1c1b232221201f1e02000002","0300080705020104060a0911100f0e0d0c0b1a12131415161718191c1b232221201f1e1d00000200","0807010602000405030a0b0c0d0e0f1011091413121a19181716151d1c1b232221201f1e02000001","0203070501060008040a0f0e09100d110c0b12131415161718191a1c21201b221f231e1d242c2b2a29282726252e2d3534333231302f3738393a3b3c3d3e36403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001000100000000","0204060500080301070b0c100e0a0f09110d141519171318121a161c1f2122201e1b231d25262728292a2b2c2434333231302f2e2d353837363e3d3c3b3a393f47464544434241404948504f4e4d4c4b4a5253545556575859515a6261605f5e5d5c5b64636b6a69686766656d6e6f70717273746c787776757d7c7b7a797f808182838485867e8f8e8d8c8b8a89888701010000010102000002","080704020001030605090a0b0c0d0e0f10111a19161412131518171d1e22201c211b231f25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595b5c5d5e5f6061625a636b6a6968676665646c74737271706f6e6d757d7c7b7a797877767f7e8685848382818088898a8b8c8d8e8f8701000001000000000000","0203070501060008040b0c100e0a0f09110d12131415161718191a1d1f21201b231e1c22242c2b2a29282726252e2d3534333231302f3738393a3b3c3d3e363f47464544434241404948504f4e4d4c4b4a5253545556575859515a5b5c5d5e5f606162636465666768696a6b6c6d6e6f7071727374767778797a7b7c7d758584838281807f7e868988878f8e8d8c8b8a00010001000102000000","010406070503000802090a0b0c0d0e0f1011141519171318121a161d1e22201c211b231f272625242c2b2a29282e2f3031323334352d3e3d3c3b3a393837363f404142434445464748494a4b4c4d4e4f505152535455565758595a6261605f5e5d5c5b64636b6a69686766656d6e6f70717273746c757d7c7b7a797877767f7e8685848382818088898a8b8c8d8e8f8701000001010000000002"],"word":[1,2]},"xy_section_cocycle":{"left":[1],"product":[1,2],"right":[2],"value":["000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f2021222300000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000","000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000000000000"]},"y":{"value":["0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0502070108060400030b0a0911100f0e0d0c1a19181716151413121c1d1e1f202122231b02000200","0502070108060400030b0a0911100f0e0d0c1a19181716151413121c1d1e1f202122231b02000200","0807040200010306050a0b0c0d0e0f101109121a191817161514131b232221201f1e1d1c01000000","0106050007040803020a0911100f0e0d0c0b131415161718191a121c1b232221201f1e1d00000100","0106050007040803020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f2021222325242c2b2a292827262e2f3031323334352d37363e3d3c3b3a3938403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000000","0204060500080301070a0f0e09100d110c0b1318171219161a15141b1c1d1e1f2021222325262728292a2b2c2434333231302f2e2d353837363e3d3c3b3a39403f47464544434241494a4b4c4d4e4f50485251595857565554535b5a6261605f5e5d5c6465666768696a6b636d6c74737271706f6e75767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000010100000002","080704020001030605090a0b0c0d0e0f101112131415161718191a1c21201b221f231e1d25262728292a2b2c242d3534333231302f2e363e3d3c3b3a3938373f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737476757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001000000000000","0106050007040803020a0f0e09100d110c0b12131415161718191a1b1c1d1e1f2021222325242c2b2a292827262e2f3031323334352d37363e3d3c3b3a3938403f47464544434241494a4b4c4d4e4f50485251595857565554535a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f00000000000100000000","010406070503000802090a0b0c0d0e0f10111318171219161a15141c21201b221f231e1d272625242c2b2a29282e2f3031323334352d3e3d3c3b3a393837363f404142434445464748494a4b4c4d4e4f505152535455565758595b5a6261605f5e5d5c6465666768696a6b636d6c74737271706f6e76757d7c7b7a7978777f808182838485867e88878f8e8d8c8b8a8900000001010000000002"],"word":[2]}}''')
GENERATION = {"Gamma_cayley_edge_count": 6318, "Gamma_cayley_state_count": 243, "Q0_defect_normal_closure_order": 243, "Q0_defect_normal_closure_rounds": [243], "Q0_lift_count": 19, "Q0_order_proof": {"G9_abstract_presentation_order": 2916, "G9_direct_image_order": 2916, "P_abstract_presentation_order": 504, "P_direct_image_order": 504, "Q0_marked_image_order": 1469664, "Q0_presentation_order_upper_bound": 1469664, "complete_relator_count": 19, "complete_relators_sha256": "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a", "cross_commutator_count": 4, "factor_payload_sha256": "6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba", "marked_splitting_equation_count": 2, "method": "producer-owned SymPy factor orders plus direct marked-permutation enumeration"}, "all_record_generator_closure_order": 243, "marked_action_loop_count": 104, "normal_closure_exact": True, "presentation_quotient_order_upper_bound": 357128352, "selected_gamma_closure_order": 243, "selected_gamma_records": [1, 3, 6, 9], "surjective_marked_image_order": 357128352, "theorem": "v190 Cayley--action--lift order bound", "upper_bound_equals_image_order": True}
MANIFEST_FIXED = {"schema": "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3", "synthetic": False, "independent": True, "producer": {"artifact_id": "9686477718", "head": "bed1d5e6b41477b8799f2a33a24e46f7800f9510", "member": {"basename": RECEIPT_NAME, "bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA}, "run": "33155710862", "terminal_line_sha256": "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090", "zip_sha256": "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854"}, "checker": {"artifact_id": "9686477718", "head": "bed1d5e6b41477b8799f2a33a24e46f7800f9510", "member": {"basename": RECEIPT_NAME, "bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA}, "run": "33155710862", "terminal_line_sha256": "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e", "zip_sha256": "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854"}, "producer_attestation": {"basename": "d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt", "bytes": 81, "sha256": "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"}, "checker_attestation": {"basename": "d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt", "bytes": 95, "sha256": "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"}, "checker_verdict": {"accepted": True, "basename": "d972_r07_seven_context_roof_presentation_v1.checker.verdict.json", "bytes": 150, "independent": True, "receipt_terminal": "ROOF_BRIDGE_ISOMORPHISM", "schema": "d972-r07-seven-context-roof-presentation/v1/crosscheck/v2", "sha256": "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"}, "task198_source_identities": {"producer": {"bytes": 137169, "path": "search/d972_r07_seven_context_roof_presentation_v1.py", "sha256": "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"}, "checker": {"bytes": 157253, "path": "crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", "sha256": "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"}, "driver": {"bytes": 20541, "path": "search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", "sha256": "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"}}}

class CheckerInputStop(RuntimeError): pass
class NarrowRejection(RuntimeError):
    def __init__(self, validator: str, stage: str, reason: str): self.validator, self.stage, self.reason = validator, stage, reason; super().__init__(reason)
class CheckerMutationAccepted(RuntimeError): pass
class SealedReceipt(NamedTuple):
    dom: dict[str, Any]; raw: bytes; raw_sha256: str; byte_length: int; self_seal: str
class SealedManifest(NamedTuple):
    dom: dict[str, Any]; raw: bytes; raw_sha256: str; byte_length: int; self_seal: str
@dataclass
class MutationPlan:
    name: str; role: str; owner: str; identity_kind: str; logical_case_path: str; owner_path: Path; resealed_nodes: list[str]; outside_parent: Path | None = None; reseal_dag: list[dict[str, Any]] | None = None

class Counter:
    CAPS = CAPS
    def __init__(self) -> None: self.counts = {k: 0 for k in self.CAPS}; self.reserved = {k: 0 for k in self.CAPS}; self.live_peak = 0; self.peak_seen = 0; self.retained: dict[str, int] = {}; self.revalidated_bytes = 0
    def reserve(self, key: str, amount: int) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or self.counts[key] + self.reserved[key] + amount > self.CAPS[key]: raise CheckerInputStop("checker:meter:reserve:" + key)
        self.reserved[key] += amount
    def charge(self, key: str, amount: int = 1) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or amount > self.reserved[key] or self.counts[key] + amount > self.CAPS[key]: raise CheckerInputStop("checker:meter:unreserved:" + key)
        self.reserved[key] -= amount; self.counts[key] += amount
    def release(self, key: str, amount: int) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0 or amount > self.reserved[key]: raise CheckerInputStop("checker:meter:release")
        self.reserved[key] -= amount
    def reserve_peak(self, amount: int) -> None:
        if type(amount) is not int or amount < 0 or self.live_peak + amount > self.CAPS["peak_live_bytes"]: raise CheckerInputStop("checker:meter:peak_live")
        self.live_peak += amount; self.peak_seen = max(self.peak_seen, self.live_peak)
    def release_peak(self, amount: int) -> None:
        if type(amount) is not int or amount < 0 or amount > self.live_peak: raise CheckerInputStop("checker:meter:peak_release")
        self.live_peak -= amount
    def retain_peak(self, owner: str, amount: int) -> None:
        if type(owner) is not str or not owner or type(amount) is not int or amount < 0: raise CheckerInputStop("checker:meter:peak_owner")
        self.reserve_peak(amount); self.retained[owner] = self.retained.get(owner, 0) + amount
    def release_retained(self, owner: str) -> None:
        amount = self.retained.pop(owner, 0)
        if amount: self.release_peak(amount)
    def release_prefix(self, prefix: str) -> None:
        for owner in list(self.retained):
            if owner.startswith(prefix): self.release_retained(owner)
        if any(owner.startswith(prefix) for owner in self.retained): raise CheckerInputStop("checker:meter:owner_leak")
    def public(self) -> dict[str, Any]: return {"caps": dict(self.CAPS), "counts": dict(self.counts), "peak_live_bytes": self.peak_seen, "revalidated_bytes": self.revalidated_bytes, "one_meter": True, "logical_open_account": "file-owner opens only; directory component opens and retained-fd revalidation reads are separately tracked"}
    def snapshot(self) -> dict[str, Any]: return {"counts": dict(self.counts), "reserved": dict(self.reserved), "live_peak_bytes": self.live_peak, "peak_seen": self.peak_seen, "revalidated_bytes": self.revalidated_bytes}

def canonical(value: Any) -> bytes: return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
def canon_meter(value: Any, counter: Counter, bound: int, owner: str | None = None) -> bytes:
    counter.reserve("canonical_bytes", bound); previous = counter.reserved["canonical_bytes"]; peak = min(bound, counter.CAPS["peak_live_bytes"]); active = False; complete = False
    try:
        if owner is None: counter.reserve_peak(peak)
        else: counter.retain_peak(owner, peak)
        active = True; raw = canonical(value); counter.charge("canonical_bytes", len(raw)); complete = True; return raw
    finally:
        residual = counter.reserved["canonical_bytes"] - (previous - bound)
        if residual > 0: counter.release("canonical_bytes", residual)
        if active and owner is None: counter.release_peak(peak)
        if active and owner is not None and not complete: counter.release_retained(owner)
def digest_bytes(raw: bytes | bytearray) -> str: return hashlib.sha256(bytes(raw)).hexdigest()
def digest_object(value: Any, counter: Counter, bound: int) -> str: return digest_bytes(canon_meter(value, counter, bound))
def strict_equal(actual: Any, expected: Any) -> bool:
    if type(expected) is dict: return type(actual) is dict and set(actual) == set(expected) and all(strict_equal(actual[k], expected[k]) for k in expected)
    if type(expected) is list: return type(actual) is list and len(actual) == len(expected) and all(strict_equal(a, e) for a, e in zip(actual, expected))
    return type(actual) is type(expected) and actual == expected
def word(value: Any) -> bool: return type(value) is list and all(type(x) is int and x in (-2, -1, 1, 2) for x in value)
def positive(value: Any) -> bool: return type(value) is int and value > 0
def same_stats(a: os.stat_result, b: os.stat_result) -> bool: return all(getattr(a, k) == getattr(b, k) for k in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_mode", "st_nlink"))
def inside(child: Path, parent: Path) -> bool:
    try: return os.path.commonpath((os.path.abspath(child), os.path.abspath(parent))) == os.path.abspath(parent)
    except ValueError: return False

def parent_nofollow(path: Path) -> tuple[int, str]:
    if os.name == "nt": raise CheckerInputStop("checker:windows:one_handle_reparse_unsupported")
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    if not nofollow or not hasattr(os, "O_DIRECTORY"): raise CheckerInputStop("checker:posix:no_follow_dirfd_unsupported")
    absolute = Path(os.path.abspath(path)); current = os.open(os.path.sep, os.O_RDONLY | os.O_DIRECTORY | nofollow)
    try:
        for part in absolute.parts[1:-1]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | nofollow, dir_fd=current); os.close(current); current = nxt
        return current, absolute.name
    except Exception: os.close(current); raise
def open_nofollow(path: Path) -> int:
    parent, leaf = parent_nofollow(path)
    try: return os.open(leaf, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent)
    finally: os.close(parent)
def lstat_nofollow(path: Path) -> os.stat_result:
    parent, leaf = parent_nofollow(path)
    try: return os.stat(leaf, dir_fd=parent, follow_symlinks=False)
    finally: os.close(parent)
def identity(before: os.stat_result, after: os.stat_result, pathname: os.stat_result, path: Path, kind: str, sha: str | None) -> dict[str, Any]:
    stable = same_stats(before, after) and same_stats(after, pathname)
    return {"identity_kind": kind, "path": str(path), "exists": True, "type": "regular" if stat.S_ISREG(before.st_mode) else "nonregular", "mode": int(before.st_mode), "bytes": int(after.st_size), "sha256": sha, "device": int(before.st_dev), "inode": int(before.st_ino), "mtime_ns": int(before.st_mtime_ns), "nlink": int(after.st_nlink), "single_open_handle": True, "opened_handle_stable": stable, "pathname_matches_opened_handle": same_stats(after, pathname), "substitution_detected": not stable}
def path_identity(path: Path, kind: str) -> dict[str, Any]:
    lexical = Path(os.path.abspath(path))
    try: st = lstat_nofollow(lexical)
    except (FileNotFoundError, NotADirectoryError): return {"identity_kind": kind, "path": str(lexical), "exists": False, "type": "missing", "mode": None, "bytes": None, "sha256": None, "device": None, "inode": None, "mtime_ns": None, "nlink": None, "single_open_handle": False, "opened_handle_stable": False, "pathname_matches_opened_handle": False, "substitution_detected": False}
    return {"identity_kind": kind, "path": str(lexical), "exists": True, "type": "regular" if stat.S_ISREG(st.st_mode) else "nonregular", "mode": int(st.st_mode), "bytes": int(st.st_size), "sha256": None, "device": int(st.st_dev), "inode": int(st.st_ino), "mtime_ns": int(st.st_mtime_ns), "nlink": int(st.st_nlink), "single_open_handle": False, "opened_handle_stable": False, "pathname_matches_opened_handle": False, "substitution_detected": False}

class Journal:
    def __init__(self, counter: Counter): self.counter = counter; self.events: list[dict[str, Any]] = []; self.observed: dict[str, dict[str, Any]] = {}; self.canonical_after: dict[str, str] = {}; self.terminals = 0; self.rows_digest: str | None = None
    def enter(self, validator: str, stage: str, owner: str) -> None: self.counter.reserve("events", 1); self.counter.charge("events", 1); self.events.append({"ordinal": len(self.events) + 1, "validator": validator, "stage": stage, "owner": owner})
    def terminal(self) -> None: self.terminals += 1
    def digest(self) -> str: return digest_object(self.events, self.counter, 1_000_000)

class AuthenticatedOwner:
    def __init__(self, counter: Counter): self.counter = counter; self.cache: dict[str, tuple[bytes | bytearray, dict[str, Any]]] = {}; self.handles: dict[str, int] = {}
    def read(self, path: Path, role: str, expected: tuple[int, str] | None = None, journal: Journal | None = None, retain_handle: bool = False) -> tuple[bytes | bytearray, dict[str, Any]]:
        lexical = Path(os.path.abspath(path)); key = str(lexical)
        if key in self.cache:
            raw, ident = self.cache[key]
            if journal is not None: journal.observed[role] = ident
            return raw, ident
        self.counter.reserve("opens", 1); open_reserved = True; fd = -1; size = 0; dom_reserved = False; peak_owner = "cache:" + key; peak = 0
        try:
            fd = open_nofollow(lexical); before = os.fstat(fd)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1: raise CheckerInputStop("checker:physical:file_identity:" + role)
            size = int(before.st_size)
            if size < 0 or size > self.counter.CAPS["temporary_bytes"]: raise CheckerInputStop("checker:physical:size:" + role)
            self.counter.reserve("opened_bytes", size); self.counter.reserve("dom_bytes", size); dom_reserved = True; peak = min(2 * size, self.counter.CAPS["peak_live_bytes"]); self.counter.retain_peak(peak_owner, peak)
            data = bytearray(); remain = size
            while remain:
                part = os.read(fd, min(1_048_576, remain))
                if not part: raise CheckerInputStop("checker:physical:short_read:" + role)
                data.extend(part); remain -= len(part)
            after = os.fstat(fd); pathname = lstat_nofollow(lexical); sha = digest_bytes(data); ident = identity(before, after, pathname, lexical, "file", sha)
            if not ident["opened_handle_stable"] or after.st_nlink != 1: raise CheckerInputStop("checker:physical:toctou:" + role)
            if expected is not None and (len(data) != expected[0] or sha != expected[1]): raise CheckerInputStop("checker:pin:" + role)
            self.counter.charge("opened_bytes", size); self.counter.charge("dom_bytes", size); dom_reserved = False; self.counter.charge("opens", 1); open_reserved = False; self.cache[key] = (data, ident)
            if retain_handle: self.handles[key] = fd; fd = -1
            if journal is not None: journal.observed[role] = ident
            return data, ident
        except Exception:
            if dom_reserved: self.counter.release("opened_bytes", size); self.counter.release("dom_bytes", size)
            if peak: self.counter.release_retained(peak_owner)
            if open_reserved: self.counter.release("opens", 1)
            raise
        finally:
            if fd >= 0: os.close(fd)
    def revalidate_all(self, expected: dict[str, dict[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, fd in self.handles.items():
            meta = expected[key]; label = meta["label"]; frozen = meta["identity"]
            before = os.fstat(fd); size = int(before.st_size)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or size != frozen["bytes"]: raise CheckerInputStop("checker:baseline:identity_changed:" + label)
            if os.lseek(fd, 0, os.SEEK_SET) != 0: raise CheckerInputStop("checker:baseline:rewind:" + label)
            h = hashlib.sha256(); remain = size; read = 0
            while remain:
                part = os.read(fd, min(1_048_576, remain))
                if not part: raise CheckerInputStop("checker:baseline:short_read:" + label)
                h.update(part); read += len(part); remain -= len(part)
            if os.lseek(fd, 0, os.SEEK_CUR) != size or read != size or h.hexdigest() != frozen["sha256"]: raise CheckerInputStop("checker:baseline:bytes_changed:" + label)
            after = os.fstat(fd); pathname = lstat_nofollow(Path(frozen["path"])); expected_stats = {"st_dev": frozen["device"], "st_ino": frozen["inode"], "st_size": frozen["bytes"], "st_mtime_ns": frozen["mtime_ns"], "st_mode": frozen["mode"], "st_nlink": frozen["nlink"]}
            if not same_stats(before, after) or not same_stats(after, pathname) or any(int(getattr(after, field)) != value for field, value in expected_stats.items()): raise CheckerInputStop("checker:baseline:identity_changed:" + label)
            self.revalidated_bytes += read
            if self.revalidated_bytes > RECHECK_BYTES_CAP: raise CheckerInputStop("checker:baseline:recheck_cap")
            answer[label] = {"fd_rewound": True, "exact_length": read, "sha256": h.hexdigest(), "identity_match": True, "pathname_no_follow_match": True}
        return answer
    def evict_workspace(self, workspace: Path) -> None:
        root = Path(os.path.abspath(workspace))
        for key in list(self.cache):
            if inside(Path(key), root): del self.cache[key]; self.counter.release_retained("cache:" + key)
        if any(inside(Path(key), root) for key in self.cache): raise CheckerInputStop("checker:cache:eviction")
    def close(self) -> None:
        for fd in list(self.handles.values()):
            try: os.close(fd)
            except OSError: pass
        self.handles.clear()
        for key in list(self.cache): del self.cache[key]; self.counter.release_retained("cache:" + key)

def admit(path: Path, role: str, workspace: Path | None, journal: Journal) -> Path:
    journal.enter("checker.transport.path_containment", "transport", role + ".path"); lexical = Path(os.path.abspath(path)); registered = Path(os.path.abspath(ROOT / (RECEIPT_REL if role == "receipt" else MANIFEST_REL)))
    if lexical != registered and not (workspace is not None and inside(lexical, workspace)):
        journal.observed[role + ".path"] = path_identity(lexical, "path"); raise NarrowRejection("checker.transport.path_containment", "transport", "checker:path:registered_containment")
    cursor = Path(lexical.anchor)
    for part in lexical.parts[1:]:
        cursor = cursor / part
        if cursor.is_symlink(): journal.observed[role + ".path"] = path_identity(lexical, "path"); raise NarrowRejection("checker.transport.path_containment", "transport", "checker:path:registered_containment")
    return lexical

def parse_object(raw: bytes | bytearray, label: str, counter: Counter, exact: bool, owner: str | None = None) -> dict[str, Any]:
    size = len(raw); counter.reserve("dom_bytes", size); charged = False; peak = min(6 * size, counter.CAPS["peak_live_bytes"]); active = False
    try:
        if owner is None: counter.reserve_peak(peak)
        else: counter.retain_peak(owner, peak)
        active = True; value = json.loads(raw); counter.charge("dom_bytes", size); charged = True
        if type(value) is not dict: raise CheckerInputStop("checker:object:" + label)
        if exact and canon_meter(value, counter, size) != bytes(raw): raise CheckerInputStop("checker:json:noncanonical:" + label)
        return value
    except json.JSONDecodeError as exc: raise CheckerInputStop("checker:json:" + label) from exc
    finally:
        if not charged: counter.release("dom_bytes", size)
        if active and owner is None: counter.release_peak(peak)
        elif active and owner is not None and "value" not in locals(): counter.release_retained(owner)

def validate_seal(value: dict[str, Any], label: str, counter: Counter) -> None:
    if label == "receipt":
        if set(value) != TOP_RECEIPT_KEYS or "manifest_self_digest_sha256" in value: raise NarrowRejection("checker.transport.receipt_seal", "transport", "checker:transport:receipt_self_seal")
        key = "self_digest_sha256"
    else:
        if "self_digest_sha256" in value or type(value.get("manifest_self_digest_sha256")) is not str: raise NarrowRejection("checker.transport.manifest_seal", "transport", "checker:transport:manifest_self_seal")
        key = "manifest_self_digest_sha256"
    claimed = value.get(key); body = dict(value); body.pop(key, None)
    if type(claimed) is not str or claimed != digest_object(body, counter, 35_000_000): raise NarrowRejection("checker.transport." + label + ".self_seal", "transport", "checker:transport:" + label + "_self_seal")

def validate_manifest(value: dict[str, Any], receipt_path: Path, receipt: dict[str, Any] | None, raw: bytes | bytearray | None, counter: Counter, sha: str | None = None) -> None:
    keys = set(MANIFEST_FIXED) | {"accepted", "accepted_receipt_basename", "receipt", "manifest_self_digest_sha256"}
    if set(value) != keys or "self_digest_sha256" in value: raise NarrowRejection("checker.authority.manifest_schema", "authority", "checker:authority:manifest_schema")
    validate_seal(value, "manifest", counter)
    if not strict_equal(value.get("schema"), MANIFEST_FIXED["schema"]) or type(value.get("synthetic")) is not bool or value.get("synthetic") is not False or type(value.get("independent")) is not bool or value.get("independent") is not True: raise NarrowRejection("checker.authority.manifest_flags", "authority", "checker:authority:manifest_flags")
    if type(value.get("accepted")) is not bool or value.get("accepted") is not True: raise NarrowRejection("checker.authority.manifest_acceptance", "authority", "checker:authority:manifest_acceptance")
    for key, fixed in MANIFEST_FIXED.items():
        if key not in ("schema", "synthetic", "independent") and not strict_equal(value.get(key), fixed): raise NarrowRejection("checker.authority.manifest_graph", "authority", "checker:authority:manifest_graph:" + key)
    binding = value.get("receipt")
    if type(binding) is not dict or set(binding) != {"basename", "bytes", "sha256", "self_digest_sha256"} or binding.get("basename") != receipt_path.name or not positive(binding.get("bytes")) or type(binding.get("sha256")) is not str or type(binding.get("self_digest_sha256")) is not str: raise NarrowRejection("checker.authority.manifest_receipt_binding", "authority", "checker:authority:manifest_receipt_binding")
    if receipt is not None and raw is not None and (binding["bytes"] != len(raw) or binding["sha256"] != (sha or digest_bytes(raw)) or binding["self_digest_sha256"] != receipt.get("self_digest_sha256")): raise NarrowRejection("checker.authority.manifest_receipt_binding", "authority", "checker:authority:manifest_receipt_binding")
    if value.get("accepted_receipt_basename") != receipt_path.name: raise NarrowRejection("checker.authority.manifest_receipt_binding", "authority", "checker:authority:manifest_receipt_binding")

def typed_row(row: Any, pos: int) -> None:
    layer = "Gamma_Cayley" if pos <= 6318 else "action" if pos <= 6422 else "Q0_lift"; local = pos if layer == "Gamma_Cayley" else pos - 6318 if layer == "action" else pos - 6422
    if type(row) is not dict or set(row) != ROW_KEYS[layer] or type(row.get("layer")) is not str or row.get("layer") != layer or type(row.get("ordinal")) is not int or row.get("ordinal") != local or row["ordinal"] <= 0: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:layer_ordinal")
    anc = row.get("ancestry")
    if type(anc) is not dict or set(anc) != ANCESTRY_KEYS[layer] or any(not word(anc[key]) for key in anc): raise NarrowRejection("checker.authority.row_shape", "authority", "checker:authority:row_shape")
    if not word(row.get("word")): raise NarrowRejection("checker.authority.row_shape", "authority", "checker:authority:row_word")
    for key in ("target_state", "state", "generator", "record", "letter"):
        if key in row and not positive(row[key]): raise NarrowRejection("checker.authority.row_shape", "authority", "checker:authority:row_type")
    if "orientation" in row and (type(row["orientation"]) is not int or row["orientation"] not in (-1, 1)): raise NarrowRejection("checker.authority.row_shape", "authority", "checker:authority:row_type")

def stream_rows(rows: list[Any], chunks: list[Any], counter: Counter) -> tuple[str, bool]:
    if type(chunks) is not list or len(chunks) != 7: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:chunk_shape")
    whole = hashlib.sha256(); whole.update(b"["); ch = hashlib.sha256(); ch.update(b"["); cursor = 0; n = 0; has_empty_word = False
    for pos, row in enumerate(rows, 1):
        typed_row(row, pos); bound = 1_000_000; counter.reserve("canonical_bytes", bound); previous = counter.reserved["canonical_bytes"]; peak_reserved = False
        try:
            counter.reserve_peak(bound); peak_reserved = True
            piece = canonical(row); counter.charge("canonical_bytes", len(piece)); whole.update((b"" if pos == 1 else b",") + piece); ch.update((b"" if n == 0 else b",") + piece); n += 1
            if row.get("word") == []: has_empty_word = True
        finally:
            residual = counter.reserved["canonical_bytes"] - (previous - bound)
            if residual > 0: counter.release("canonical_bytes", residual)
            if peak_reserved: counter.release_peak(bound)
        if n == 1024 or pos == len(rows):
            ch.update(b"]"); rec = chunks[cursor // 1024]
            if type(rec) is not dict or set(rec) != CHUNK_KEYS or type(rec.get("start")) is not int or type(rec.get("end")) is not int or type(rec.get("sealed")) is not bool or type(rec.get("prefix_complete")) is not bool or type(rec.get("sha256")) is not str or rec["start"] != cursor or rec["end"] != pos or rec["sealed"] is not True or rec["prefix_complete"] is not True or rec["sha256"] != ch.hexdigest(): raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:chunk_shape")
            cursor = pos; ch = hashlib.sha256(); ch.update(b"["); n = 0
    whole.update(b"]")
    if cursor != ROWS: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:chunk_coverage")
    return whole.hexdigest(), has_empty_word

def validate_rows(receipt: dict[str, Any], counter: Counter) -> str:
    delta0 = receipt.get("Delta0")
    presentation = delta0.get("presentation") if type(delta0) is dict else None
    if type(presentation) is not dict or set(presentation) != PRESENTATION_KEYS or type(delta0) is not dict or set(delta0) != {"marked_generators", "normal_closure_exact", "order", "presentation"}: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:presentation_shape")
    if not strict_equal(presentation.get("layer_counts"), LAYER_COUNTS) or type(presentation.get("normal_closure_exact")) is not bool or presentation.get("normal_closure_exact") is not True or type(presentation.get("normal_generation")) is not bool or presentation.get("normal_generation") is not True or type(presentation.get("resume_cursor")) is not int or presentation.get("resume_cursor") != ROWS or presentation.get("source_word_encoding") != "literal strict signed F2 words; empty Cayley tree loops retained" or presentation.get("task172_legacy_rows_sha256") != LEGACY_ROWS_SHA: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:presentation_types")
    rows = presentation.get("rows")
    if type(rows) is not list or len(rows) != ROWS or type(presentation.get("row_count")) is not int or presentation.get("row_count") != ROWS: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:row_count")
    actual, has_empty_word = stream_rows(rows, presentation["chunks"], counter)
    if presentation.get("rows_sha256") != actual or actual != ROWS_SHA: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:row_digest")
    if not has_empty_word: raise NarrowRejection("checker.authority.row_order", "authority", "checker:authority:lossless_empty_word")
    return actual

def validate_generation(receipt: dict[str, Any]) -> None:
    if type(receipt["Delta0"]["presentation"].get("normal_generation_proof")) is not dict or not strict_equal(receipt["Delta0"]["presentation"]["normal_generation_proof"], GENERATION): raise NarrowRejection("checker.authority.normal_generation", "authority", "checker:authority:normal_generation_proof")
def validate_bridge(receipt: dict[str, Any], counter: Counter, expected_bridge: dict[str, Any] | None = None) -> dict[str, Any]:
    bridge = receipt.get("bridge"); fields = {"block", "block_index", "block_slot", "context_id", "factor_sign", "fox_prefix_occurrences", "occurrence", "ordinal", "orientation", "role", "ten_index", "type"}
    if type(bridge) is not dict or set(bridge) != BRIDGE_KEYS or type(bridge.get("occurrence_ledger")) is not list or len(bridge["occurrence_ledger"]) != 11: raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_occurrence_ledger")
    for actual, expected in zip(bridge["occurrence_ledger"], OCCURRENCE_LEDGER):
        if type(actual) is not dict or set(actual) != fields or not strict_equal(actual, expected) or not all(type(actual[key]) is int for key in ("ordinal", "block_index", "block_slot", "context_id", "factor_sign", "ten_index")) or type(actual["fox_prefix_occurrences"]) is not list or not all(type(item) is int and item > 0 for item in actual["fox_prefix_occurrences"]): raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_occurrence_ledger")
    if bridge.get("occurrence_ledger_sha256") != digest_object(bridge["occurrence_ledger"], counter, 100_000) or bridge.get("occurrence_ledger_sha256") != OCCURRENCE_LEDGER_SHA or bridge.get("typed_coordinate_ledger_sha256") != digest_object(COORDINATE_OWNER, counter, 10_000) or bridge.get("typed_coordinate_ledger_sha256") != COORDINATE_LEDGER_SHA: raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_occurrence_digest")
    if type(bridge.get("branch")) is not str or bridge.get("branch") != "ROOF_BRIDGE_ISOMORPHISM" or type(bridge.get("image_order")) is not int or bridge.get("image_order") != 357128352 or type(bridge.get("kernel_order")) is not int or bridge.get("kernel_order") != 1 or type(bridge.get("marked_replay_count")) is not int or bridge.get("marked_replay_count") != 4 or type(bridge.get("marked_inverse_count")) is not int or bridge.get("marked_inverse_count") != 4 or not strict_equal(bridge.get("ten_to_eleven"), [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9]) or not strict_equal(bridge.get("eleven_delete_duplicate"), [0, 1, 2, 3, 5, 6, 7, 8, 9, 10]) or not strict_equal(bridge.get("seven_blocks"), [[0, 1, 2], [3, 0, 4], [5], [6], [7], [8], [9]]): raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_contract")
    if expected_bridge is not None and not strict_equal(bridge, expected_bridge): raise NarrowRejection("checker.authority.bridge_occurrence", "authority", "checker:authority:bridge_contract")
    return bridge
def check_value(value: Any, width: int) -> bool: return type(value) is str and len(value) == 2 * width and all(char in "0123456789abcdef" for char in value)
def validate_abi(receipt: dict[str, Any], counter: Counter, expected_abi: dict[str, Any] | None = None) -> dict[str, Any]:
    ev = receipt.get("evaluator"); keys = {"nonsplit_y_y_section_cocycle", "source_2_2", "x", "y", "x_inverse", "xy", "xy_section_cocycle", "x_action_y"}
    if type(ev) is not dict or set(ev) != EVALUATOR_KEYS or ev.get("module") != "search/d972_r07_seven_context_roof_presentation_v1.py" or ev.get("relator_rows_sha256") != ROWS_SHA or ev.get("schema") != "d972-r07-v188-roof-consumer-action-abi/v1" or ev.get("runtime_constructor") != "load_runtime" or ev.get("registry_callable") != "v188_consumer_action_abi" or not strict_equal(ev.get("coordinate_widths"), COORDINATE_WIDTHS) or ev.get("coordinate_ledger_sha256") != COORDINATE_LEDGER_SHA or not strict_equal(ev.get("encoding"), ABI_ENCODING) or not strict_equal(ev.get("entry_points"), ABI_ENTRY_POINTS) or not strict_equal(ev.get("semantics"), ABI_SEMANTICS) or ev.get("context_maps") is not None or ev.get("joint_coordinate_image") is not None: raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    canaries = ev.get("canaries")
    if type(canaries) is not dict or set(canaries) != keys or canaries["nonsplit_y_y_section_cocycle"] is not None: raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    for name, expected_word in (("x", [1]), ("y", [2]), ("x_inverse", [-1]), ("xy", [1, 2])):
        c = canaries[name]
        if type(c) is not dict or set(c) != {"word", "value"} or c.get("word") != expected_word or not word(c.get("word")) or type(c.get("value")) is not list or len(c["value"]) != 10 or any(not check_value(v, w) for v, w in zip(c["value"], COORDINATE_WIDTHS)): raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    source = canaries["source_2_2"]
    if type(source) is not dict or set(source) != {"gamma_state_id", "gamma_word", "q0_state_id", "q0_word", "source_word", "value"} or source.get("gamma_state_id") != 2 or source.get("q0_state_id") != 2 or source.get("q0_word") != [1] or not word(source.get("gamma_word")) or not word(source.get("source_word")) or type(source.get("value")) is not list or len(source["value"]) != 10 or any(not check_value(v, w) for v, w in zip(source["value"], COORDINATE_WIDTHS)): raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    action = canaries["x_action_y"]; cocycle = canaries["xy_section_cocycle"]
    if type(action) is not dict or set(action) != {"actor_word", "input", "value"} or action.get("actor_word") != [1] or type(action.get("input")) is not list or len(action["input"]) != 10 or any(not check_value(v, w) for v, w in zip(action["input"], COORDINATE_WIDTHS)) or type(action.get("value")) is not list or len(action["value"]) != 10 or any(not check_value(v, w) for v, w in zip(action["value"], COORDINATE_WIDTHS)): raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    if type(cocycle) is not dict or set(cocycle) != {"left", "right", "product", "value"} or cocycle.get("left") != [1] or cocycle.get("right") != [2] or cocycle.get("product") != [1, 2] or type(cocycle.get("value")) is not list or len(cocycle["value"]) != 10 or any(not check_value(v, w) for v, w in zip(cocycle["value"], COORDINATE_WIDTHS)): raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    if not strict_equal(canaries, ABI_CANARIES): raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    if expected_abi is not None and not strict_equal(ev, expected_abi): raise NarrowRejection("checker.authority.evaluator_abi", "authority", "checker:authority:evaluator_abi_canary")
    return ev

def validate_receipt(raw: bytes | bytearray, journal: Journal, counter: Counter, expected_bridge: dict[str, Any] | None = None, expected_abi: dict[str, Any] | None = None, owner: str | None = None, sha: str | None = None) -> dict[str, Any]:
    receipt = parse_object(raw, "receipt", counter, True, owner); journal.canonical_after["receipt"] = sha or digest_bytes(raw); validate_seal(receipt, "receipt", counter)
    if receipt.get("schema") != "d972-r07-seven-context-roof-presentation/v1" or receipt.get("status") != "COMPLETE": raise NarrowRejection("checker.authority.receipt_envelope", "authority", "checker:authority:receipt_envelope")
    journal.enter("checker.authority.row_order", "authority", "receipt.Delta0.presentation.rows"); journal.rows_digest = validate_rows(receipt, counter)
    journal.enter("checker.authority.normal_generation", "authority", "receipt.Delta0.presentation.normal_generation_proof"); validate_generation(receipt)
    journal.enter("checker.authority.bridge_occurrence", "authority", "receipt.bridge.occurrence_ledger"); validate_bridge(receipt, counter, expected_bridge)
    journal.enter("checker.authority.evaluator_abi", "authority", "receipt.evaluator"); validate_abi(receipt, counter, expected_abi); return receipt
def ordinary(manifest_path: Path, receipt_path: Path, workspace: Path | None, owner: AuthenticatedOwner, journal: Journal, counter: Counter, expected_bridge: dict[str, Any] | None = None, expected_abi: dict[str, Any] | None = None, retained: str | None = None) -> dict[str, Any]:
    manifest_owner = None if retained is None else retained + ":manifest"; receipt_owner = None if retained is None else retained + ":receipt"; mp = admit(manifest_path, "manifest", workspace, journal); journal.enter("checker.transport.manifest_open", "transport", "manifest.bytes"); mraw, mid = owner.read(mp, "manifest", (MANIFEST_BYTES, MANIFEST_SHA) if workspace is None else None, journal, workspace is None); journal.enter("checker.transport.manifest_decode", "decode", "manifest.bytes"); manifest = parse_object(mraw, "manifest", counter, True, manifest_owner); journal.canonical_after["manifest"] = mid["sha256"]; rp = admit(receipt_path, "receipt", workspace, journal); journal.enter("checker.authority.manifest_acceptance", "authority", "manifest.accepted"); validate_manifest(manifest, rp, None, None, counter); journal.enter("checker.transport.receipt_open", "transport", "receipt.bytes"); rraw, rid = owner.read(rp, "receipt", (RECEIPT_BYTES, RECEIPT_SHA) if workspace is None else None, journal, workspace is None); binding = manifest.get("receipt")
    if type(binding) is not dict or binding.get("bytes") != len(rraw) or binding.get("sha256") != rid["sha256"]:
        journal.enter("checker.transport.receipt_identity", "transport", "manifest.receipt.{bytes,sha256}"); raise NarrowRejection("checker.transport.receipt_identity", "transport", "checker:transport:receipt_sha256")
    receipt = validate_receipt(rraw, journal, counter, expected_bridge, expected_abi, receipt_owner, rid["sha256"]); validate_manifest(manifest, rp, receipt, rraw, counter, rid["sha256"]); return {"manifest": manifest, "receipt": receipt, "manifest_raw": mraw, "receipt_raw": rraw, "manifest_identity": mid, "receipt_identity": rid, "paths": (mp, rp), "rows_digest": journal.rows_digest}
def authenticate(owner: AuthenticatedOwner, journal: Journal) -> None:
    for path, size, sha in SOURCE_PINS: journal.enter("checker.transport.source_pin", "transport", path); owner.read(ROOT / path, path, (size, sha), journal, True)
def load_fixture(owner: AuthenticatedOwner, counter: Counter, argument: str) -> dict[str, Any]:
    if Path(argument).is_absolute() or argument.replace("\\", "/") != FIXTURE_REL: raise CheckerInputStop("checker:fixture:path")
    raw, _ = owner.read(ROOT / FIXTURE_REL, "fixture", (FIXTURE_BYTES, FIXTURE_SHA), None, True); fixture = parse_object(raw, "fixture", counter, False, "fixture"); body = dict(fixture); seal = body.pop("self_digest_sha256", None)
    if type(seal) is not str or seal != FIXTURE_SELF or seal != digest_object(body, counter, 1_000_000) or fixture.get("schema") != SCHEMA + "/authority-fixture/v3": raise CheckerInputStop("checker:fixture:self_seal")
    if fixture.get("synthetic") is not False or fixture.get("candidate_only") is not True or fixture.get("full_a4_selftest") is not False or fixture.get("actual_a4_numerator") is not False or fixture.get("covered_rows") != [1, 2, 3, 4, 5, 6, 7] or fixture.get("remaining_rows") != list(range(8, 49)): raise CheckerInputStop("checker:fixture:scope")
    if fixture.get("immutable_input_identities") != {"task198_receipt": {"bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA, "self_digest_sha256": RECEIPT_SELF}, "task198_manifest": {"bytes": MANIFEST_BYTES, "sha256": MANIFEST_SHA, "manifest_self_digest_sha256": MANIFEST_SELF}} or fixture.get("resource_caps") != CAPS or fixture.get("resource_formula") != {"opened_bytes_intended": INTENDED_OPENED_BYTES, "temporary_bytes_intended": INTENDED_TEMPORARY_BYTES, "largest_intended_peak": LARGEST_INTENDED_PEAK} or INTENDED_OPENED_BYTES > CAPS["opened_bytes"] or INTENDED_TEMPORARY_BYTES > CAPS["temporary_bytes"] or LARGEST_INTENDED_PEAK > CAPS["peak_live_bytes"] or INTENDED_DOM_BYTES > CAPS["dom_bytes"]: raise CheckerInputStop("checker:fixture:contract")
    if set(fixture.get("producer", {})) != set(MUTATIONS) or set(fixture.get("checker", {})) != set(MUTATIONS): raise CheckerInputStop("checker:fixture:rows")
    return fixture
def seal_receipt(value: dict[str, Any], counter: Counter, owner: str) -> SealedReceipt:
    body = dict(value)
    if "manifest_self_digest_sha256" in body: raise CheckerInputStop("checker:receipt:foreign_seal")
    body.pop("self_digest_sha256", None); body_raw = canon_meter(body, counter, 35_000_000, owner + ":body"); seal = digest_bytes(body_raw); counter.release_retained(owner + ":body"); dom = dict(body); dom["self_digest_sha256"] = seal; raw = canon_meter(dom, counter, 35_000_000, owner); return SealedReceipt(dom, raw, digest_bytes(raw), len(raw), seal)
def seal_manifest(value: dict[str, Any], counter: Counter, owner: str) -> SealedManifest:
    body = dict(value)
    if "self_digest_sha256" in body: raise CheckerInputStop("checker:manifest:foreign_seal")
    body.pop("manifest_self_digest_sha256", None); body_raw = canon_meter(body, counter, 10_000, owner + ":body"); seal = digest_bytes(body_raw); counter.release_retained(owner + ":body"); dom = dict(body); dom["manifest_self_digest_sha256"] = seal; raw = canon_meter(dom, counter, 10_000, owner); return SealedManifest(dom, raw, digest_bytes(raw), len(raw), seal)
def copy_manifest(manifest: dict[str, Any], receipt_path: Path, sealed: SealedReceipt, counter: Counter, owner: str) -> dict[str, Any]:
    if not isinstance(sealed, SealedReceipt) or sealed.raw_sha256 != digest_bytes(sealed.raw) or sealed.byte_length != len(sealed.raw) or sealed.self_seal != sealed.dom.get("self_digest_sha256"): raise CheckerInputStop("checker:reseal:receipt_tuple")
    bound = 10_000; counter.reserve("dom_bytes", bound); retained = False; charged = False
    try:
        counter.retain_peak(owner, bound); retained = True; out = copy.deepcopy(manifest); counter.charge("dom_bytes", bound); charged = True; out["accepted_receipt_basename"] = receipt_path.name; out["receipt"] = {"basename": receipt_path.name, "bytes": sealed.byte_length, "sha256": sealed.raw_sha256, "self_digest_sha256": sealed.self_seal}; return out
    except Exception:
        if not charged: counter.release("dom_bytes", bound)
        if retained: counter.release_retained(owner)
        raise
def clone_small(value: dict[str, Any], counter: Counter, owner: str) -> dict[str, Any]:
    bound = 10_000; counter.reserve("dom_bytes", bound); retained = False; charged = False
    try:
        counter.retain_peak(owner, bound); retained = True; clone = copy.deepcopy(value); counter.charge("dom_bytes", bound); charged = True; return clone
    except Exception:
        if not charged: counter.release("dom_bytes", bound)
        if retained: counter.release_retained(owner)
        raise
def clone_owner(value: dict[str, Any], counter: Counter, owner: str) -> dict[str, Any]:
    bound = 200_000_000; counter.reserve("dom_bytes", bound); retained = False; charged = False
    try:
        counter.retain_peak(owner, bound); retained = True; clone = copy.deepcopy(value); counter.charge("dom_bytes", bound); charged = True; return clone
    except Exception:
        if not charged: counter.release("dom_bytes", bound)
        if retained: counter.release_retained(owner)
        raise
def mutate_wire(source: bytes | bytearray, counter: Counter, owner: str) -> bytearray:
    size = len(source); counter.reserve("dom_bytes", size); retained = False; charged = False
    try:
        counter.retain_peak(owner, size); retained = True; changed = bytearray(source); counter.charge("dom_bytes", size); charged = True; changed[-1] ^= 1; return changed
    except Exception:
        if not charged: counter.release("dom_bytes", size)
        if retained: counter.release_retained(owner)
        raise
def mutate_receipt(receipt: dict[str, Any], name: str) -> None:
    if name == "per_layer_ordinal": receipt["Delta0"]["presentation"]["rows"][0]["ordinal"] += 1
    elif name == "normal_generation_proof": receipt["Delta0"]["presentation"]["normal_generation_proof"]["Gamma_cayley_edge_count"] += 1
    elif name == "bridge_typed_occurrence_ledger": receipt["bridge"]["occurrence_ledger"][0]["block"] = "H1_mutated"
    elif name == "evaluator_abi_canary": receipt["evaluator"]["coordinate_widths"][0] += 1
def make_plan(name: str, workspace: Path, baseline: dict[str, Any], counter: Counter) -> tuple[MutationPlan, Path, Path]:
    mp, rp = baseline["paths"]
    if name == "authority_binding":
        changed = clone_small(baseline["manifest"], counter, "case:" + name + ":clone"); changed["accepted"] = False; mp = workspace / MANIFEST_NAME; sealed = seal_manifest(changed, counter, "case:" + name + ":manifest_raw"); write_case(mp, sealed.raw, workspace, counter); return MutationPlan(name, "manifest", "authority.manifest.accepted", "file", "task198/manifest/accepted", mp, ["manifest.manifest_self_digest_sha256"], reseal_dag=[{"node": "changed_manifest_body", "output": "manifest.manifest_self_digest_sha256+raw_sha256"}]), mp, rp
    if name == "canonical_input_bytes":
        changed = mutate_wire(baseline["receipt_raw"], counter, "case:" + name + ":wire"); rp = workspace / RECEIPT_NAME; write_case(rp, changed, workspace, counter); return MutationPlan(name, "receipt", "authority.receipt.raw_bytes", "file", "task198/receipt/raw-bytes", rp, [], reseal_dag=[]), mp, rp
    if name == "resolved_path_traversal":
        outside = Path(tempfile.mkdtemp(prefix="d972-r07-a4-checker-outside-")); path = outside / RECEIPT_NAME
        if inside(outside, workspace) or inside(outside, ROOT) or path.exists(): raise CheckerInputStop("checker:row4:outside_owner_collision")
        return MutationPlan(name, "receipt", "authority.receipt.path", "path", "task198/receipt/path", path, [], outside, []), mp, path
    changed = clone_owner(baseline["receipt"], counter, "case:" + name + ":clone"); mutate_receipt(changed, name); rp = workspace / RECEIPT_NAME; sealed = seal_receipt(changed, counter, "case:" + name + ":receipt_raw"); changed = sealed.dom; write_case(rp, sealed.raw, workspace, counter); cm = copy_manifest(baseline["manifest"], rp, sealed, counter, "case:" + name + ":changed_manifest_clone"); mp = workspace / MANIFEST_NAME; msealed = seal_manifest(cm, counter, "case:" + name + ":manifest_raw"); write_case(mp, msealed.raw, workspace, counter)
    if name == "per_layer_ordinal": owner = "authority.receipt.Delta0.presentation.rows[0].ordinal"; logical = "task198/receipt/row-0001/ordinal"
    elif name == "normal_generation_proof": owner = "authority.receipt.Delta0.presentation.normal_generation_proof.Gamma_cayley_edge_count"; logical = "task198/receipt/normal-generation-proof"
    elif name == "bridge_typed_occurrence_ledger": owner = "authority.receipt.bridge.occurrence_ledger[0].block"; logical = "task198/receipt/bridge-occurrence-ledger"
    elif name == "evaluator_abi_canary": owner = "authority.receipt.evaluator.coordinate_widths[0]"; logical = "task198/receipt/evaluator-coordinate-abi"
    else: raise CheckerInputStop("checker:mutation:unknown:" + name)
    plan = MutationPlan(name, "receipt", owner, "file", logical, rp, ["receipt.self_digest_sha256", "manifest.receipt.bytes", "manifest.receipt.sha256", "manifest.receipt.self_digest_sha256", "manifest.manifest_self_digest_sha256"])
    plan.reseal_dag = [{"node": "changed_receipt_body", "output": "receipt.self_digest_sha256"}, {"node": "receipt.self_digest_sha256", "output": "receipt.raw_sha256+byte_length"}, {"node": "receipt.raw_sha256+byte_length+self_digest_sha256", "output": "manifest.receipt.binding"}, {"node": "manifest.receipt.binding", "output": "changed_manifest_body"}, {"node": "changed_manifest_body", "output": "manifest.manifest_self_digest_sha256+raw_sha256"}]
    return plan, mp, rp

def write_case(path: Path, raw: bytes | bytearray, workspace: Path, counter: Counter) -> None:
    if not inside(path, workspace): raise CheckerInputStop("checker:case:containment")
    size = len(raw); counter.reserve("temporary_bytes", size); counter.charge("temporary_bytes", size); counter.reserve("writes", 1); counter.charge("writes"); counter.reserve("opens", 2)
    try: parent, leaf = parent_nofollow(workspace)
    except Exception: counter.release("opens", 2); raise
    fd = -1; tmp = None; remaining_open = 2
    try:
        counter.charge("opens")
        for _ in range(32):
            candidate = next(tempfile._get_candidate_names())
            try: fd = os.open(candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600, dir_fd=parent); tmp = candidate; break
            except FileExistsError: continue
        if fd < 0: raise CheckerInputStop("checker:case:temp_name")
        counter.charge("opens"); remaining_open = 0; pos = 0
        while pos < size: pos += os.write(fd, raw[pos:pos + 1_048_576])
        os.fsync(fd); os.close(fd); fd = -1; os.rename(tmp, leaf, src_dir_fd=parent, dst_dir_fd=parent); tmp = None; os.fsync(parent)
    except Exception as exc:
        if fd >= 0:
            try: os.close(fd)
            except OSError: pass
        if tmp is not None:
            try: os.unlink(tmp, dir_fd=parent)
            except OSError: pass
        raise CheckerInputStop("checker:case:atomic_write") from exc
    finally:
        if remaining_open: counter.release("opens", remaining_open)
        os.close(parent)
def project(ident: dict[str, Any], logical: str, before: str, after: str) -> dict[str, Any]:
    readable = ident.get("exists") is True and ident.get("sha256") is not None
    return {"logical_case_path": logical, "owner_kind": ident.get("identity_kind"), "byte_length": ident.get("bytes") if readable else "UNREADABLE_AT_REGISTERED_STAGE", "content_sha256": ident.get("sha256") if readable else "UNREADABLE_AT_REGISTERED_STAGE", "link_count": ident.get("nlink") if ident.get("nlink") is not None else "UNREADABLE_AT_REGISTERED_STAGE", "symlink_or_reparse": ident.get("type") != "regular", "logical_link_target": "none" if ident.get("type") in ("regular", "missing") else ident.get("type"), "single_open_handle": ident.get("single_open_handle") is True, "opened_handle_stable": ident.get("opened_handle_stable") is True, "pathname_matches_opened_handle": ident.get("pathname_matches_opened_handle") is True, "substitution_detected": ident.get("substitution_detected") is True, "canonical_before_sha256": before, "canonical_after_sha256": after}
def same_owner(a: dict[str, Any], b: dict[str, Any]) -> bool: return all(a.get(k) == b.get(k) for k in ("path", "exists", "type", "mode", "bytes", "sha256", "device", "inode", "mtime_ns", "nlink"))
def run_case(name: str, baseline: dict[str, Any], fixture: dict[str, Any], counter: Counter, owner: AuthenticatedOwner, workspace: Path, pre: dict[str, Any]) -> dict[str, Any]:
    resource_before = counter.snapshot(); counter.reserve("mutations", 1); counter.charge("mutations", 1); plan, mp, rp = make_plan(name, workspace, baseline, counter); before = baseline[plan.role + "_identity"]; journal = Journal(counter)
    try: ordinary(mp, rp, workspace, owner, journal, counter, baseline["expected_bridge"], baseline["expected_abi"], "case:" + name)
    except NarrowRejection as rejection:
        journal.terminal(); after = journal.observed.get(plan.role) or journal.observed.get(plan.role + ".path"); entered = [event["validator"] for event in journal.events]
        if after is None or same_owner(before, after) or after.get("identity_kind") != plan.identity_kind: raise CheckerInputStop("checker:trace:owner_identity:" + name)
        expected = fixture["checker"][name]; first = {"validator": rejection.validator, "stage": rejection.stage, "narrow_reason": rejection.reason}
        if expected["owner"] != plan.owner or expected["identity_kind"] != plan.identity_kind or expected["logical_case_path"] != plan.logical_case_path or expected["ordinary_validator"] != rejection.validator or expected["stage"] != rejection.stage or expected["first_rejection"] != first or expected["allowed_downstream_reseals"] != plan.resealed_nodes or entered.count(rejection.validator) != 1 or journal.terminals != 1: raise CheckerInputStop("checker:fixture:trace:" + name)
        link = workspace / ".case-owner-link"
        if plan.owner_path.exists(): os.link(plan.owner_path, link)
        if link.exists(): os.unlink(link)
        if link.exists(): raise CheckerInputStop("checker:workspace:hardlink_eviction:" + name)
        owner.evict_workspace(workspace); shutil.rmtree(workspace, ignore_errors=False) if workspace.exists() else None; workspace_absent = not workspace.exists(); outside_absent = True
        if plan.outside_parent is not None: shutil.rmtree(plan.outside_parent, ignore_errors=False); outside_absent = not plan.outside_parent.exists() and not plan.owner_path.exists()
        disposed = not plan.owner_path.exists() and workspace_absent and outside_absent
        if not disposed: raise CheckerInputStop("checker:workspace:dispose:" + name)
        post = owner.revalidate_all(baseline["authority_handles"])
        return {"id": name, "owner": plan.owner, "identity_kind": plan.identity_kind, "before_identity": project(before, plan.logical_case_path, before["sha256"] or "UNREADABLE_AT_REGISTERED_STAGE", before["sha256"] or "UNREADABLE_AT_REGISTERED_STAGE"), "after_identity": project(after, plan.logical_case_path, before["sha256"] or "UNREADABLE_AT_REGISTERED_STAGE", journal.canonical_after.get(plan.role, "UNREADABLE_AT_REGISTERED_STAGE")), "resealed_nodes": list(plan.resealed_nodes), "semantic_reseal_dag": list(plan.reseal_dag or []), "entered_validators": entered, "first_rejection": first, "event_trace_digest": journal.digest(), "terminal_count": journal.terminals, "baseline_revalidated": True, "baseline_revalidation_transcript": {"before": pre, "after": post}, "owner_disposed": disposed, "disposal_proof": {"workspace_absent": workspace_absent, "outside_owner_absent": outside_absent, "cache_evicted": True}, "resource_before": resource_before, "resource_after": counter.snapshot()}
    raise CheckerMutationAccepted("checker:mutation_accepted:" + name)

def execute(fixture: dict[str, Any], counter: Counter, owner: AuthenticatedOwner) -> dict[str, Any]:
    journal = Journal(counter); authenticate(owner, journal); baseline = ordinary(ROOT / MANIFEST_REL, ROOT / RECEIPT_REL, None, owner, journal, counter, retained="baseline"); baseline["rows"] = baseline["receipt"]["Delta0"]["presentation"]["rows"]; baseline["expected_bridge"] = baseline["receipt"]["bridge"]; baseline["expected_abi"] = baseline["receipt"]["evaluator"]; handles = {}
    for index, (path, _, _) in enumerate(SOURCE_PINS, 1):
        key = str(Path(os.path.abspath(ROOT / path))); handles[key] = {"label": "source_pin_" + str(index), "identity": owner.cache[key][1]}
    for key, label in ((str(Path(os.path.abspath(ROOT / FIXTURE_REL))), "fixture"), (str(Path(os.path.abspath(ROOT / MANIFEST_REL))), "manifest"), (str(Path(os.path.abspath(ROOT / RECEIPT_REL))), "receipt")): handles[key] = {"label": label, "identity": owner.cache[key][1]}
    baseline["authority_handles"] = handles; records = []
    for name in MUTATIONS:
        if any(token.startswith("case:") for token in counter.retained): raise CheckerInputStop("checker:case:prior_owner_live")
        workspace = Path(tempfile.mkdtemp(prefix="d972-r07-a4-checker-"))
        if inside(workspace, ROOT): shutil.rmtree(workspace); raise CheckerInputStop("checker:workspace:repository_overlap")
        record: dict[str, Any] | None = None
        try:
            record = run_case(name, baseline, fixture, counter, owner, workspace, owner.revalidate_all(baseline["authority_handles"])); records.append(record)
        finally:
            owner.evict_workspace(workspace); shutil.rmtree(workspace, ignore_errors=True); counter.release_prefix("case:" + name)
            if record is not None: record["resource_after"] = counter.snapshot()
            if any(token.startswith("case:") for token in counter.retained): raise CheckerInputStop("checker:case:owner_leak")
    result = {"schema": SCHEMA, "candidate_only": True, "synthetic": False, "covered_rows": [1, 2, 3, 4, 5, 6, 7], "remaining_rows": list(range(8, 49)), "full_a4_selftest": False, "actual_a4_numerator": False, "baseline": {"receipt_canonical_sha256": baseline["receipt_identity"]["sha256"], "manifest_canonical_sha256": baseline["manifest_identity"]["sha256"], "rows_sha256": baseline["rows_digest"], "baseline_revalidated": records[-1]["baseline_revalidated"]}, "rows": records, "resource": counter.public()}; del baseline; counter.release_retained("baseline:manifest"); counter.release_retained("baseline:receipt"); return result

def verify_at(parent_fd: int, name: str, raw: bytes, sha: str, counter: Counter) -> None:
    counter.reserve("opens", 1); open_reserved = True; fd = -1
    try:
        fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd); counter.charge("opens"); open_reserved = False
    except Exception:
        if open_reserved: counter.release("opens", 1)
        raise
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size != len(raw): raise CheckerInputStop("checker:output:final_identity")
        h = hashlib.sha256(); remain = st.st_size
        while remain:
            part = os.read(fd, min(1_048_576, remain))
            if not part: raise CheckerInputStop("checker:output:final_short_read")
            h.update(part); remain -= len(part)
        if h.hexdigest() != sha: raise CheckerInputStop("checker:output:final_sha256")
    finally: os.close(fd)
def write_stage(stage_fd: int, name: str, raw: bytes, counter: Counter) -> None:
    counter.reserve("opens", 1); open_reserved = True; fd = -1
    try:
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600, dir_fd=stage_fd); counter.charge("opens"); open_reserved = False
    except Exception:
        if open_reserved: counter.release("opens", 1)
        raise
    try:
        pos = 0
        while pos < len(raw): pos += os.write(fd, raw[pos:pos + 1_048_576])
        os.fsync(fd)
    finally: os.close(fd)
def output_seal(value: dict[str, Any], counter: Counter, token: str) -> tuple[bytes, str]:
    body = dict(value); body.pop("self_digest_sha256", None); body_raw = canon_meter(body, counter, 35_000_000, token + ":body"); seal = digest_bytes(body_raw); counter.release_retained(token + ":body"); body["self_digest_sha256"] = seal; raw = canon_meter(body, counter, 35_000_000, token); return raw, digest_bytes(raw)
def write_output(path: Path, value: dict[str, Any], counter: Counter) -> None:
    target = Path(os.path.abspath(path)); out = Path(os.path.abspath(ROOT / "ci" / "out"))
    if not inside(target, out) or not target.name or not target.parent.exists(): raise CheckerInputStop("checker:output:stale_or_containment")
    counter.reserve("opens", 1); parent_open_reserved = True; parent_fd = -1
    try:
        parent_fd, leaf = parent_nofollow(target.parent); counter.charge("opens"); parent_open_reserved = False
    except Exception:
        if parent_open_reserved: counter.release("opens", 1)
        raise
    try: before = os.fstat(parent_fd)
    except Exception:
        os.close(parent_fd); raise
    stage = None; stage_fd = -1; published = False; raw: bytes | None = None; token = "output:final_raw"
    try:
        try: os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False); raise CheckerInputStop("checker:output:stale_target")
        except FileNotFoundError: pass
        raw, sha = output_seal(value, counter, token); counter.reserve("temporary_bytes", len(raw)); counter.charge("temporary_bytes", len(raw)); counter.reserve("writes", 1); counter.charge("writes")
        for _ in range(64):
            candidate = next(tempfile._get_candidate_names())
            try: os.mkdir(candidate, 0o700, dir_fd=parent_fd); stage = candidate; break
            except FileExistsError: continue
        if stage is None: raise CheckerInputStop("checker:output:stage_name")
        counter.reserve("opens", 1); stage_open_reserved = True
        try:
            stage_fd = os.open(stage, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd); counter.charge("opens"); stage_open_reserved = False
        except Exception:
            if stage_open_reserved: counter.release("opens", 1)
            raise
        write_stage(stage_fd, "staged.json", raw, counter); verify_at(stage_fd, "staged.json", raw, sha, counter)
        try: os.link("staged.json", leaf, src_dir_fd=stage_fd, dst_dir_fd=parent_fd, follow_symlinks=False)
        except TypeError as exc: raise CheckerInputStop("checker:output:no_follow_link_unsupported") from exc
        except FileExistsError as exc: raise CheckerInputStop("checker:output:stale_race") from exc
        published = True; os.unlink("staged.json", dir_fd=stage_fd)
        try: os.stat("staged.json", dir_fd=stage_fd, follow_symlinks=False); raise CheckerInputStop("checker:output:staging_link_present")
        except FileNotFoundError: pass
        os.fsync(stage_fd); os.close(stage_fd); stage_fd = -1; os.rmdir(stage, dir_fd=parent_fd); stage = None; os.fsync(parent_fd); verify_at(parent_fd, leaf, raw, sha, counter); after = os.fstat(parent_fd)
        if (before.st_dev, before.st_ino, before.st_mode, before.st_nlink) != (after.st_dev, after.st_ino, after.st_mode, after.st_nlink): raise CheckerInputStop("checker:output:parent_identity")
    except Exception as exc:
        if published:
            try:
                os.unlink(leaf, dir_fd=parent_fd); os.fsync(parent_fd)
                try: os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False); raise CheckerInputStop("checker:output:rollback_present")
                except FileNotFoundError: pass
            except Exception as rollback: raise CheckerInputStop("checker:output:rollback_failed") from rollback
        if stage_fd >= 0:
            try: os.close(stage_fd)
            except OSError: pass
            stage_fd = -1
        if stage is not None:
            try: os.unlink("staged.json", dir_fd=parent_fd)
            except OSError: pass
            try: os.rmdir(stage, dir_fd=parent_fd)
            except OSError: pass
            try: os.fsync(parent_fd)
            except OSError: pass
        if isinstance(exc, CheckerInputStop): raise
        raise CheckerInputStop("checker:output:atomic_failure") from exc
    finally:
        if raw is not None: del raw
        counter.release_prefix(token)
        if stage_fd >= 0:
            try: os.close(stage_fd)
            except OSError: pass
        os.close(parent_fd)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--fixture", default=FIXTURE_REL); parser.add_argument("--output"); args = parser.parse_args(argv)
    if os.name == "nt": raise CheckerInputStop("checker:windows:one_handle_reparse_unsupported")
    counter = Counter(); owner = AuthenticatedOwner(counter); fixture = None
    try:
        fixture = load_fixture(owner, counter, args.fixture); result = execute(fixture, counter, owner); del fixture; counter.release_retained("fixture");
        if args.output: write_output(Path(args.output), result, counter)
        return 0
    finally:
        counter.release_retained("baseline:manifest"); counter.release_retained("baseline:receipt"); counter.release_retained("fixture"); owner.close()

if __name__ == "__main__": raise SystemExit(main())
