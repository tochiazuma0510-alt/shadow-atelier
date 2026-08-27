"""Bounded, fail-closed task-175 all-seven raw-bridge preflight.

The default mode is a static receipt writer.  ``--run-preflight`` is reserved
for the parent/GHA job: this audit intentionally does not execute it.  The
implementation keeps the mathematical gates explicit; a positive terminal is
never manufactured from an old receipt or a producer boolean.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json"
CAP = 6441
TERMINAL_READY = "R07_ALL_SEVEN_RAW_BRIDGE_PREFLIGHT_READY"
TERMINALS = {
    TERMINAL_READY,
    "UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE",
    "UNKNOWN_INPUT:PB3_PRESENTATION_PIN",
    "UNKNOWN_INPUT:RAW_FORMULA",
    "UNKNOWN_INPUT:FOX_CANARY",
    "UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD",
    "UNKNOWN_RESOURCE:runtime",
}

PINS = {
    "task175b": ("sol/luna_task_175b_r07_all_seven_raw_bridge_implementation_repair.md", 5136,
                  "a41f2446fd1c9f0bd60a7189db682784f4e69e24e8958f7c4505cd1eb9741836"),
    "task175": ("sol/luna_task_175_r07_all_seven_raw_bridge_preflight_v1.md", 8584,
                 "5d0d8e006c6a752e5a525b188c9d95ba0c858aa69147432e639fe3e735ffefee"),
    "inventory173": ("sol/luna_reply_173_r07_all_seven_raw_bridge_inventory_v1.md", 24283,
                      "189a642fc8654f163b0b7964b75043ea393cac31a0b56b84ae0fddf2f73c3695"),
    "pb3_v121": ("sol/proof_pb3_two_relator_presentation_equality_v121.md", 5762,
                 "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"),
    "bridge_v122": ("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md", 7939,
                    "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"),
    "checkpoint_v123": ("sol/audit_r07_all_seven_bridge_checkpoint_v123.md", 5017,
                        "272aabc882599031c4da0472f8f2340043b32571e8e05ecaa58fc5ad1c6a31ac"),
    "pb4_v108": ("sol/proof_pb4_eleven_relator_presentation_equality_v108.md", 6742,
                 "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"),
    "v172_producer": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918,
                      "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    "v172_checker": ("crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py", 12423,
                     "e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23"),
    "v172_cert": ("search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json", 45246709,
                  "86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff"),
    "q3_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
                   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "157ee_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
                      "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "g760_source": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409,
                    "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"),
    "joint_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
                     "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "pb4_source": ("search/d972_b345_target6_dual_colgen_v2.py", 444497,
                   "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"),
    "old_source": ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942,
                   "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"),
}


class Unknown(RuntimeError):
    """A typed fail-closed runtime stop, never a negative mathematical result."""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_obj(value) -> str:
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True).encode("ascii"))


def pin_inputs() -> dict:
    out = {}
    for name, (rel, expected_bytes, expected_sha) in PINS.items():
        path = ROOT / rel
        if not path.is_file():
            raise Unknown("UNKNOWN_RESOURCE:missing_input:" + rel)
        data = path.read_bytes()
        if expected_bytes and len(data) != expected_bytes:
            raise Unknown("UNKNOWN_RESOURCE:pin_bytes:" + rel)
        if sha(data) != expected_sha:
            raise Unknown("UNKNOWN_RESOURCE:pin_sha:" + rel)
        out[name] = {"path": rel, "bytes": len(data), "sha256": expected_sha}
    return out


def expected_pin_manifest() -> dict:
    """Return the registered manifest without masking a failed pin read."""
    return {name: {"path": rel, "bytes": expected_bytes,
                   "sha256": expected_sha}
            for name, (rel, expected_bytes, expected_sha) in PINS.items()}


def free_reduce(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(int(letter))
    return tuple(stack)


def inverse(word):
    return tuple(-x for x in reversed(tuple(word)))


def paper_product(*displayed):
    """Frozen pp_words convention: displayed factors multiply right-to-left."""
    out = ()
    for factor in reversed(displayed):
        out = free_reduce(out + tuple(factor))
    return out


def element_blob(value):
    return bytes(value[0]) + bytes(value[1])


def tagged_sparse(block, component, value, coefficient):
    return (int(block), int(component), element_blob(value).hex(), int(coefficient) % 3)


def literal_roster_contract():
    """The 6,318+104+19 roster contract, including corrected action tokens."""
    return {
        "layers": {"gamma_edge": 6318, "xy_action": 104, "q0_relator": 19},
        "total": 6441,
        "action_tokens": {
            "+1": [["letter", "li", -1], ["record", "ri", 1], ["letter", "li", 1],
                   ["section", "target", -1]],
            "-1": [["letter", "li", 1], ["record", "ri", 1], ["letter", "li", -1],
                   ["section", "target", -1]],
        },
        "action_ordinal": "ri*4 + li*2 + (1 if orient=+1 else 2)",
        "word_key": "free-reduced signed integer tuple",
        "nonempty_required": True,
        "nonempty_scope": "deterministic correction witness and Fox canary samples only",
    }


def context_contract():
    return {
        "source_pairs": [["x", "y"], ["x", "z"], ["y", "z"], ["u", "x"], ["u", "y"]],
        "pentagon_context_ids": [1, 21, 22, 23, 24, 25, 26, 27, 28],
        "bridge_ids": {"(x,y)": 21, "(x,z)": 22, "(y,z)": 23, "(u,x)": 24, "(u,y)": 25},
        "derived": {"z": "inverse(paper_product(x,y))", "u": "inverse(paper_product(y,x))"},
        "maps": {
            "insertion_pb4_indices": [1, 2, 4],
            "deletion_pb4_to_pb3": [1, 2, 0, 3, 0, 0],
            "required_identity": "d_E(i_E(mark)) == mark for all three marks",
        },
        "blob_rule": "exact left/right E3 blobs after d_E; names are not evidence",
    }


def all_seven_contract():
    return {
        "base": {"constructor": "construct_base() independent g760", "length": 760,
                 "exponent_sums": [0, 0],
                 "signed_word_sha256": "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"},
        "occurrences": {"H1": 3, "H2": 3, "P": 5, "total": 11,
                        "pentagon_order": ["b1", "b2", "b3", "b5^-1", "b4^-1"]},
        "blocks": {"H1/E3": {"tag": 1, "components": 3},
                   "H2/E3": {"tag": 2, "components": 3},
                   "P/E4": {"tag": 3, "components": 6}},
        "raw_replay": ["direct R(f1)R(g760)^-1", "literal prefix transport", "factor replay"],
        "factor_intermediates": 4,
        "correction": {"source": "first deterministic nonempty row of complete roster",
                        "role": "typed formula/canary witness only", "final_correction": False},
    }


def fox_contract():
    return {
        "raw_D2_columns": {"PB3": 2, "PB4": 11},
        "required": ["value=1", "D1=0", "direct conjugate equals full-context left translation"],
        "actual_pairs_minimum": 110,
        "slot_minimum": 10,
        "layers": ["gamma_edge", "xy_action", "q0_relator"],
        "special": ["H2", "b4^-1", "b5^-1", "same-context/different-conjugator x2",
                     "actual-product additivity"],
        "negative_convention_tests": ["right correction", "base sign", "u/z", "inverse prefix",
                                       "negative factor order"],
    }


def semantic_mutations(base_state, validate):
    """Rerun the producer's typed reconstruction after each real mutation.

    ``base_state`` contains load-bearing words, typed columns, and formula
    inputs; it is not a serialized receipt.  ``validate`` is the same
    producer-side algebraic validator used for the unmutated result and is
    allowed to rebuild the roster/Fox/D1/pentagon objects from those inputs.
    """
    names = ["correction_left_right", "corrected_base_sign", "H2_u_z",
             "inverse_fox_prefix", "negative_pentagon_factor_4",
             "negative_pentagon_factor_5", "negative_pentagon_order",
             "coface_slot_1_3_swap", "E3_E4_rank_swap", "E3_E4_blob_swap",
             "context_name_only_dedup", "dropped_block_tag",
             "fourth_third_deletion_swap", "fine_insertion_index_4_3_swap",
             "derived_u_order", "derived_z_order", "one_actual_roster_letter",
             "actual_product_additivity_term", "terminal_marker"]
    jobs = []
    def first_nonempty_row(rows):
        ordered = sorted(rows, key=lambda row: (row["layer"], row["ordinal"], row["word"]))
        for row in ordered:
            if row.get("word"):
                return row
        raise ValueError("no nonempty roster witness")

    def run(name, mutate):
        caught = False
        try:
            candidate = copy.deepcopy(base_state)
            mutate(candidate)
            validate(candidate)
        except (Unknown, KeyError, TypeError, ValueError, IndexError):
            caught = True
        jobs.append({"id": name, "caught": caught})

    # Keep the registered correction word fixed.  This mutation flips the
    # load-bearing side of the corrected-word product and is rejected by the
    # same formula validator; it must not append g760 into the correction
    # witness itself (which would exercise only a receipt mutation).
    run("correction_left_right", lambda d: d.__setitem__("correction_side", "left"))
    run("corrected_base_sign", lambda d: d.__setitem__("base_sign", -1))
    run("H2_u_z", lambda d: (d["source_pairs"].reverse(), d.__setitem__("u_word", d["z_word"])))
    run("inverse_fox_prefix", lambda d: d["fox"][0].__setitem__("predicted", [[0, "00", 1]]))
    run("negative_pentagon_factor_4", lambda d: d["pentagon"]["ordered_factor_signs"].__setitem__(3, 1))
    run("negative_pentagon_factor_5", lambda d: d["pentagon"]["ordered_factor_signs"].__setitem__(4, 1))
    run("negative_pentagon_order", lambda d: d["pentagon"]["ordered_factor_indices"].__setitem__(3, 4))
    run("coface_slot_1_3_swap", lambda d: d["source_pairs"].__setitem__(0, d["source_pairs"][1]))
    run("E3_E4_rank_swap", lambda d: d.__setitem__("rank", 10))
    run("E3_E4_blob_swap", lambda d: d["pb4"].__setitem__(0, {}))
    run("context_name_only_dedup", lambda d: d["contexts"].pop())
    run("dropped_block_tag", lambda d: d["blocks"].pop())
    run("fourth_third_deletion_swap", lambda d: d["deletion"].__setitem__(0, 3))
    run("fine_insertion_index_4_3_swap", lambda d: d["insertion"].__setitem__(2, 3))
    run("derived_u_order", lambda d: d.__setitem__("u_word", list(reversed(d["u_word"]))))
    run("derived_z_order", lambda d: d.__setitem__("z_word", list(reversed(d["z_word"]))))
    run("one_actual_roster_letter", lambda d: first_nonempty_row(d["roster"])["word"].__setitem__(0, -int(first_nonempty_row(d["roster"])["word"][0])))
    run("actual_product_additivity_term", lambda d: d["fox"].append({"direct": [], "predicted": [[0, "00", 1]]}))
    run("terminal_marker", lambda d: d.__setitem__("terminal", "UNKNOWN_RESOURCE:runtime"))
    if not jobs or not all(row["caught"] for row in jobs):
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:mutation")
    return jobs


def load_source(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    if spec is None or spec.loader is None:
        raise Unknown("UNKNOWN_RESOURCE:module:" + rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fine_deletion_bfs(e3, e4):
    """Build Pi4[3] -> Pi3[3] by a deterministic marked-generator BFS."""
    domain = e4.pc.one(); images = e3.pc.one()
    generators = [value[1] for value in e4.generators]
    # The six E4 marked generators map to the three E3 generators with the
    # two prescribed trivial images in the middle/end slots.  Keep the
    # inverse half aligned with these six images; zip-truncating at three
    # would silently certify the wrong homomorphism.
    target_images = [e3.generators[0][1], e3.generators[1][1], e3.pc.one(),
                     e3.generators[2][1], e3.pc.one(), e3.pc.one()]
    table = {domain: images}; queue = [domain]; head = 0
    steps = generators + [e4.pc.inverse(value) for value in generators]
    step_images = target_images + [e3.pc.inverse(value) for value in target_images]
    while head < len(queue):
        source = queue[head]; head += 1
        carried = table[source]
        for generator, target in zip(steps, step_images):
            nxt = e4.pc.mul(source, generator)
            image = e3.pc.mul(carried, target)
            if nxt in table and table[nxt] != image:
                raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:fine_conflict")
            if nxt not in table:
                table[nxt] = image; queue.append(nxt)
            if len(table) > 59049:
                raise Unknown("UNKNOWN_RESOURCE:E3_CONTEXT_KERNEL_BRIDGE:fine_bfs_cap")
    if len(table) != 59049 or len(set(table.values())) != 81:
        raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:fine_bfs_order")
    return table


def coarse_deletion_map(e3, e4):
    """Restrict Q4 permutations to the fourth P and G9 blocks."""
    def restrict(perm):
        first = [int(perm[index]) - 27 for index in range(27, 36)]
        second = [int(perm[index]) - 117 + 9 for index in range(117, 144)]
        if sorted(first) != list(range(9)) or sorted(second) != list(range(9, 36)):
            raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:coarse_block")
        return bytes(first + second)
    images = [restrict(value[0]) for value in e4.generators]
    expected = [e3.generators[0][0], e3.generators[1][0], bytes(range(36)), e3.generators[2][0], bytes(range(36)), bytes(range(36))]
    if images != expected:
        raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:coarse_marked_images")
    return images, restrict


def retract_map_replay(old, e3, e4, contexts, aliases):
    """Construct both factor maps, then replay every registered bridge row."""
    required = {21: "hexagon_1_fxy_4", 22: "hexagon_1_fxz_4", 23: "hexagon_1_fyz_4", 24: "hexagon_2_fux_4", 25: "hexagon_2_fuy_4"}
    if aliases.get("hexagon_2_fxy_4") != 21:
        raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:alias_hexagon_2_fxy_4")
    for registry_id, alias in required.items():
        if aliases.get(alias) != registry_id or registry_id > len(contexts):
            raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:registry_binding")
    registry_rows = [contexts[registry_id - 1] for registry_id in required]
    if not registry_rows:
        raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:empty_registry")
    coarse_images, coarse_map = coarse_deletion_map(e3, e4)
    fine_map = fine_deletion_bfs(e3, e4)
    def d_element(value):
        permutation, coordinate = value
        projected = coarse_map(permutation)
        if coordinate not in fine_map:
            raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:fine_element")
        return (projected, fine_map[coordinate])
    insertion = [[1], [2], [4]]
    deletion = [[1], [2], [], [3], [], []]
    marks = []
    for mark, image in enumerate(insertion, 1):
        inserted = e4.eval(image)
        deleted_word = []
        for letter in image:
            deleted_word.extend(deletion[abs(letter) - 1] if letter > 0 else inverse(deletion[abs(letter) - 1]))
        returned = e3.eval(deleted_word)
        expected = e3.eval([mark])
        d_returned = d_element(inserted)
        if returned != expected or d_returned != expected:
            raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:mark")
        marks.append({"mark": mark, "inserted_blob": element_blob(inserted).hex(),
                      "deleted_blob": element_blob(returned).hex(),
                      "formal_deleted_blob": element_blob(returned).hex(),
                      "d_element_blob": element_blob(d_returned).hex(),
                      "expected_blob": element_blob(expected).hex()})
    # The fine collector has four rank-three marked PC units; retain exact
    # unit blobs as a replay inventory even though the marked-word check is
    # the induced map proof used by v122.
    pc_units = [e3.pc.unit(i).hex() for i in range(1, e3.pc.n + 1)]
    pc_preimages = []
    for index in range(1, e3.pc.n + 1):
        expected_pc = e3.pc.unit(index)
        source = next((source for source, image in fine_map.items()
                       if image == expected_pc), None)
        if source is None or fine_map[source] != expected_pc:
            raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:pc_generator")
        pc_preimages.append({"index": index, "input": source.hex(),
                             "output": expected_pc.hex()})
    contexts_out = []
    eval3_f2 = lambda word: e3.eval(old.embed_f2_pb3(word))
    expected_pairs = [([1], [2]), ([1], old.inv_word(old.pp_words([[1], [2]]))),
                      ([2], old.inv_word(old.pp_words([[1], [2]]))),
                      (old.inv_word(old.pp_words([[2], [1]])), [1]),
                      (old.inv_word(old.pp_words([[2], [1]])), [2])]
    for registry_id, (left_word, right_word) in zip(required, expected_pairs):
        left4, right4 = registry_rows[list(required).index(registry_id)]
        left3, right3 = d_element(left4), d_element(right4)
        expected_left, expected_right = eval3_f2(left_word), eval3_f2(right_word)
        if left3 != expected_left or right3 != expected_right:
            raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:blob_mismatch")
        contexts_out.append({"registry_id": registry_id, "input_left": element_blob(left4).hex(), "input_right": element_blob(right4).hex(), "output_left": element_blob(left3).hex(), "output_right": element_blob(right3).hex(), "expected_left": element_blob(expected_left).hex(), "expected_right": element_blob(expected_right).hex()})
    return {"insertion_pb4_indices": insertion, "deletion_pb4_to_pb3": deletion,
            "marks": marks, "pc_generator_blobs": pc_units,
            "pc_generator_preimages": pc_preimages,
            "d_E_i_E_marks": len(marks) == 3,
            "coarse_marked_images": [list(image) for image in coarse_images],
            "fine_domain_order": len(fine_map), "fine_image_order": len(set(fine_map.values())),
            "registry_replay": contexts_out,
            "coarse_projection": {"P_block": "fourth", "G9_block": "fourth",
                                  "input_blobs": [row["inserted_blob"] for row in marks],
                                  "output_blobs": [row["deleted_blob"] for row in marks]}}


def prefix_formula(old, group_obj, base_factors, corrected_factors, embed):
    """Two complete product-rule sums, then corrected-minus-base."""
    def product_gradient(factors):
        prefix = group_obj.identity; answer = {}
        for word in reversed(factors):
            grad, value = old.fox_gradient_without_sections(embed(word), group_obj)
            for key, coefficient in old.translate_vector(grad, prefix, group_obj).items():
                answer[key] = (answer.get(key, 0) + int(coefficient)) % 3
                if not answer[key]: del answer[key]
            prefix = group_obj.mul(prefix, value)
        return answer, prefix
    base_gradient, base_value = product_gradient(base_factors)
    corrected_gradient, corrected_value = product_gradient(corrected_factors)
    result = dict(corrected_gradient)
    for key, coefficient in base_gradient.items():
        result[key] = (result.get(key, 0) - int(coefficient)) % 3
        if not result[key]: del result[key]
    return result, base_value, corrected_value


def roster_provenance(group, row):
    """Decode a retained roster ordinal into its construction witness."""
    layer, ordinal = row["layer"], int(row["ordinal"])
    if layer == "gamma_edge":
        state_id, generator_id = divmod(ordinal - 1, 26)
        target = group.transitions[state_id][generator_id]
        return {"layer": layer, "state_id": state_id,
                "generator_id": generator_id, "record_index": generator_id,
                "section_source_factors": group.section_factors(state_id),
                "section_target_factors": group.section_factors(target)}
    if layer == "xy_action":
        record_index, rem = divmod(ordinal - 1, 4)
        letter_index, orientation_bit = divmod(rem, 2)
        return {"layer": layer, "record_index": record_index,
                "letter_index": letter_index,
                "orientation": 1 if orientation_bit == 0 else -1}
    if layer == "q0_relator":
        return {"layer": layer, "relator_index": ordinal - 1}
    raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:roster_provenance")


def all_seven_fox_sample(old, e3, e4, roster):
    """Replay 110 word-bearing conjugations across all eleven slots.

    This producer-side routine deliberately keeps the raw F2 words separate
    from their typed E3/E4 lifts.  The checker has a second implementation of
    the same transcript, so the receipt contains enough provenance to compare
    every direct sparse row rather than only a count or digest.
    """
    x, y = [1], [2]
    z = old.inv_word(old.pp_words([x, y]))
    u = old.inv_word(old.pp_words([y, x]))
    pcontexts = [([1], [4]), ([4], [6]),
                 (paper_product([2], [4]), [6]),
                 (paper_product([1], [2]), paper_product([5], [6])),
                 ([1], paper_product([4], [5]))]
    specs = [
        ("H1", "H1_fxy", 1, e3, x, y, 1, True),
        ("H1", "H1_fxz", 1, e3, x, z, -1, True),
        ("H1", "H1_fyz", 1, e3, y, z, 1, True),
        ("H2", "H2_fux", 2, e3, u, x, -1, True),
        ("H2", "H2_fxy", 2, e3, x, y, -1, True),
        ("H2", "H2_fuy", 2, e3, u, y, 1, True),
    ]
    # Natural factor contexts are (b3,b1,b5,b2,b4); occurrence transcripts
    # use the literal printed order b1,b2,b3,b5^-1,b4^-1.
    for index in (1, 3, 0, 2, 4):
        label = {0: "b3", 1: "b1", 2: "b5", 3: "b2", 4: "b4"}[index]
        left, right = pcontexts[index]
        specs.append(("P", "P_" + label +
                      ("_inverse" if index in (2, 4) else ""), 3,
                      e4, left, right, -1 if index in (2, 4) else 1,
                      False))

    def reduce_word(word):
        return old.reduce_word(list(word))

    def lift(spec, word):
        value = old.f2_substitute(list(word), spec[4], spec[5])
        return old.embed_f2_pb3(value) if spec[7] else value

    def serial(group_obj, vector):
        result = []
        for (component, value), coefficient in vector.items():
            if int(coefficient) % 3:
                result.append([int(component), old._element_blob(value).hex(),
                               int(coefficient) % 3])
        return sorted(result, key=lambda row: (row[0], bytes.fromhex(row[1])))

    selected = []
    for layer, count in (("gamma_edge", 4), ("xy_action", 3),
                         ("q0_relator", 3)):
        selected.extend([row for row in roster
                         if row["layer"] == layer and row.get("word")][:count])
    if len(selected) != 10:
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:layer_selection")
    conjugators = [(1,), (-1,), (2,), (-2,), (1, 2), (-2, -1),
                   (1, 1, 2, -1), (2, 1, -2, -1), (1, -2, 1)]
    transcript = []
    for slot_index, spec in enumerate(specs):
        block, name, tag, quotient = spec[0], spec[1], spec[2], spec[3]
        for local_index, row in enumerate(selected):
            relation = lift(spec, row["word"])
            if spec[6] < 0:
                relation = old.inv_word(relation)
            conjugator = conjugators[(slot_index * 10 + local_index) % len(conjugators)]
            qword = lift(spec, conjugator)
            conjugated = reduce_word(tuple(qword) + tuple(relation) +
                                     tuple(old.inv_word(qword)))
            direct, direct_value = old.fox_gradient_without_sections(
                conjugated, quotient)
            base, base_value = old.fox_gradient_without_sections(
                relation, quotient)
            predicted = old.translate_vector(base, quotient.eval(qword), quotient)
            if (direct_value != quotient.identity or
                    base_value != quotient.identity or direct != predicted):
                raise Unknown("UNKNOWN_INPUT:FOX_CANARY:slot_conjugation")
            transcript.append({
                "slot": slot_index + 1, "slot_name": name, "block": block,
                "block_tag": tag, "factor_sign": spec[6],
                "layer": row["layer"], "ordinal": row["ordinal"],
                "u": list(conjugator), "u_length": len(conjugator),
                "r_word": list(row["word"]), "r_length": len(row["word"]),
                "relation_word": list(relation),
                "conjugated_word": list(conjugated),
                "direct": serial(quotient, direct),
                "predicted": serial(quotient, predicted),
            })
    if len(transcript) != 110:
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:pair_count")
    slot_counts = {str(index): sum(item["slot"] == index
                                   for item in transcript)
                   for index in range(1, 12)}
    layer_counts = {layer: sum(item["layer"] == layer for item in transcript)
                    for layer in ("gamma_edge", "xy_action", "q0_relator")}
    if (any(value != 10 for value in slot_counts.values()) or
            any(value == 0 for value in layer_counts.values())):
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:strata")

    same_context = []
    base_relation = tuple(selected[0]["word"])
    for krow in roster:
        if len(same_context) >= 2:
            break
        kernel = tuple(krow["word"])
        left_u, right_u = (1,), reduce_word((1,) + kernel)
        c1 = reduce_word(left_u + base_relation + old.inv_word(left_u))
        c2 = reduce_word(right_u + base_relation + old.inv_word(right_u))
        if right_u == left_u or c1 == c2:
            continue
        tagged1, tagged2, equal = [], [], True
        for spec in specs:
            quotient = spec[3]
            uv = quotient.eval(lift(spec, left_u))
            vv = quotient.eval(lift(spec, right_u))
            equal = equal and uv == vv
            g1, _ = old.fox_gradient_without_sections(lift(spec, c1), quotient)
            g2, _ = old.fox_gradient_without_sections(lift(spec, c2), quotient)
            tagged1.extend([[spec[2], *entry] for entry in serial(quotient, g1)])
            tagged2.extend([[spec[2], *entry] for entry in serial(quotient, g2)])
        if equal and sorted(tagged1) == sorted(tagged2):
            same_context.append({
                "r_layer": selected[0]["layer"],
                "r_ordinal": selected[0]["ordinal"],
                "r_word": list(base_relation), "k_layer": krow["layer"],
                "k_ordinal": krow["ordinal"], "k_word": list(kernel),
                "u": list(left_u), "v": list(right_u),
                "conjugate_u": list(c1), "conjugate_v": list(c2),
                "conjugates_differ": True, "complete_context_equal": True,
                "tagged_row_sha256": digest_obj([sorted(tagged1),
                                                   sorted(tagged2)]),
            })
    if len(same_context) < 2:
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:same_context")

    spec = specs[0]
    quotient = spec[3]
    a = lift(spec, selected[1]["word"])
    b = lift(spec, selected[2]["word"])
    ga, va = old.fox_gradient_without_sections(a, quotient)
    gb, vb = old.fox_gradient_without_sections(b, quotient)
    gab, vab = old.fox_gradient_without_sections(tuple(a) + tuple(b), quotient)
    predicted_add = dict(ga)
    add_scaled(old, predicted_add,
               old.translate_vector(gb, va, quotient), 1)
    if (va != quotient.identity or vb != quotient.identity or
            vab != quotient.identity or gab != predicted_add):
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:product_additivity")
    additivity = {
        "status": "PASS", "slot": spec[1],
        "layer_a": selected[1]["layer"], "ordinal_a": selected[1]["ordinal"],
        "layer_b": selected[2]["layer"], "ordinal_b": selected[2]["ordinal"],
        "word_a": list(a), "word_b": list(b),
        "product_word": list(tuple(a) + tuple(b)),
        "direct": serial(quotient, gab),
        "predicted": serial(quotient, predicted_add), "equal": True,
    }
    digest = digest_obj([{
        "slot": item["slot"], "layer": item["layer"],
        "ordinal": item["ordinal"], "direct": item["direct"],
        "predicted": item["predicted"],
    } for item in transcript])
    return {
        "status": "PASS", "pairs": len(transcript), "required": 110,
        "slot_counts": slot_counts, "layer_counts": layer_counts,
        "transcript": transcript, "row_digest_sha256": digest,
        "same_context_pairs": len(same_context),
        "same_context": same_context,
        "actual_product_additivity": additivity,
        "convention": {
            "formula": "left Fox; q*r*q^-1", "left_translation": True,
            "all_eleven_slots": True, "nonempty_conjugators": True,
            "inverse_slots": ["H1_fxz", "H2_fux", "H2_fxy",
                              "P_b5_inverse", "P_b4_inverse"],
        },
    }


def run_preflight():
    """Execute the bounded reconstruction used by the parent/GHA job.

    The authenticated v172 source is loaded only after its exact pin is
    checked.  Its public terminal is ignored: every row and value used below
    is replayed and serialized by this producer.  A missing source-E3 map is a
    typed input stop, never a fabricated success.
    """
    pins = pin_inputs()
    v172 = load_source("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", "p175_v172")
    prev = v172.load(v172.PREV, "p175_auth_prev")
    prev.Q3_ARTIFACT = v172.Q3
    prev.Q3_ARTIFACT_SHA = v172.Q3_SHA
    q, old = prev.authenticated_input(v172.Q3)
    e3, e4, _ = old.reconstruct_quotients(q)
    contexts, aliases, ctxpub = old.cheap_context_registry(e4)
    maps = retract_map_replay(old, e3, e4, contexts, aliases)
    words = [list(r["word"]) for r in q["correction_fibre"]["records"] if r.get("word")]
    if len(words) != 26:
        raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:record_count")
    gmod = load_source("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", "p175_g760")
    _, _, g = gmod.construct_base()
    if len(g) != 760 or digest_obj(g) != all_seven_contract()["base"]["signed_word_sha256"]:
        raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:g760")
    joint = load_source("search/d972_b345_joint_kernel_qstar_closure_v1.py", "p175_joint")
    group, roster = v172.build_roster(joint, old, e3, e4, contexts, words)
    # Empty reduced words are valid members of the lossless expanded roster;
    # only the selected correction witness must be word-bearing.
    if len(roster) != CAP:
        raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:roster")
    if any(group.eval(r["word"]) != group.identity for r in roster):
        raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:roster_evaluation")
    # Deterministic word-bearing canary.  Identity is checked directly in the
    # full joint group before it is allowed into the formula path.
    canary = next((row for row in sorted(
        roster, key=lambda r: (r["layer"], r["ordinal"], r["word"]))
                   if row.get("word")), None)
    if canary is None or group.eval(canary["word"]) != group.identity:
        raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:joint_canary")
    c = tuple(canary["word"])
    f1 = free_reduce(tuple(g) + c)
    x, y = [1], [2]
    z = old.inv_word(old.pp_words([x, y])); u = old.inv_word(old.pp_words([y, x]))
    sub = old.f2_substitute
    lift3 = lambda w: old.embed_f2_pb3(w)
    hwords = old.hexagon_words(g)
    hwords1 = old.hexagon_words(f1)
    h1, h2 = lift3(hwords[0]), lift3(hwords[1])
    h1c, h2c = lift3(hwords1[0]), lift3(hwords1[1])
    pcontexts = [([1], [4]), ([4], [6]), (paper_product([2], [4]), [6]),
                 (paper_product([1], [2]), paper_product([5], [6])),
                 ([1], paper_product([4], [5]))]
    # Fresh literal constructor for the printed word
    # b1*b2*b3*b5^-1*b4^-1; do not import the predecessor's pentagon helper.
    def literal_pentagon(word):
        factors = [old.f2_substitute(word, left, right)
                   for left, right in pcontexts]
        return paper_product(factors[1], factors[3], factors[0],
                             inverse(factors[2]), inverse(factors[4]))
    pword, pword1 = literal_pentagon(g), literal_pentagon(f1)
    # Preserve the five literal factor occurrences and the four ordered
    # intermediate products; the two negative slots are never commuted.
    factor_words = [old.f2_substitute(f1, left, right) for left, right in pcontexts]
    factor_base_words = [old.f2_substitute(g, left, right) for left, right in pcontexts]
    factor_values = [e4.eval(w) for w in factor_words]
    factor_base_values = [e4.eval(w) for w in factor_base_words]
    ordered_factors = [factor_values[1], factor_values[3], factor_values[0],
                       e4.inverse(factor_values[2]), e4.inverse(factor_values[4])]
    ordered_products = []
    multiplication_order = list(reversed(ordered_factors))
    product = multiplication_order[0]
    for factor in multiplication_order[1:]:
        product = e4.mul(product, factor)
        ordered_products.append(old._element_blob(product).hex())
    base_ordered = [factor_base_values[1], factor_base_values[3], factor_base_values[0],
                    e4.inverse(factor_base_values[2]), e4.inverse(factor_base_values[4])]
    base_multiplication_order = list(reversed(base_ordered))
    base_product = base_multiplication_order[0]
    base_intermediates = []
    for factor in base_multiplication_order[1:]:
        base_product = e4.mul(base_product, factor)
        base_intermediates.append(old._element_blob(base_product).hex())
    # Direct quotient replay in E3/E4 for all seven occurrences.  The five
    # source pairs are kept as distinct typed rows; no name-only dedup occurs.
    source_pairs = [(x, y), (x, z), (y, z), (u, x), (u, y)]
    e3_contexts = [{"left_blob": old._element_blob(e3.eval(old.embed_f2_pb3(a))).hex(),
                    "right_blob": old._element_blob(e3.eval(old.embed_f2_pb3(b))).hex()} for a, b in source_pairs]
    if any(e3.eval(w) != e3.identity for w in (h1c, h2c)):
        raise Unknown("UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE:source_identity")
    direct_p = e4.eval(pword1)
    if direct_p != e4.identity:
        raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:pentagon_identity")
    # Recompute every direct/prefix change in each source block.  The E3
    # gradients are computed with the same frozen left-Fox engine, while the
    # E4 pentagon uses the independently assembled five-factor word.
    def change(group_obj, base, corrected):
        base_grad, base_value = old.fox_gradient_without_sections(base, group_obj)
        corr_grad, corr_value = old.fox_gradient_without_sections(corrected, group_obj)
        if base_value != group_obj.identity or corr_value != group_obj.identity:
            raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:nonidentity_target")
        ans = dict(corr_grad)
        for key, value in base_grad.items():
            ans[key] = (ans.get(key, 0) - int(value)) % 3
        for key, value in list(ans.items()):
            ans[key] %= 3
            if not ans[key]:
                del ans[key]
        return ans
    e3_h1 = change(e3, h1, h1c); e3_h2 = change(e3, h2, h2c)
    e4_p = change(e4, pword, pword1)
    fxy, fxz, fyz = [old.f2_substitute(g, a, b) for a, b in ((x, y), (x, z), (y, z))]
    fxy1, fxz1, fyz1 = [old.f2_substitute(f1, a, b) for a, b in ((x, y), (x, z), (y, z))]
    fux, fuy = old.f2_substitute(g, u, x), old.f2_substitute(g, u, y)
    fux1, fuy1 = old.f2_substitute(f1, u, x), old.f2_substitute(f1, u, y)
    h1_prefix, h1_base_value, h1_corrected_value = prefix_formula(old, e3, [fxy, inverse(fxz), fyz], [fxy1, inverse(fxz1), fyz1], lift3)
    h2_prefix, h2_base_value, h2_corrected_value = prefix_formula(old, e3, [inverse(fux), inverse(fxy), fuy], [inverse(fux1), inverse(fxy1), fuy1], lift3)
    p_base_display = [factor_base_words[1], factor_base_words[3], factor_base_words[0], inverse(factor_base_words[2]), inverse(factor_base_words[4])]
    p_corr_display = [factor_words[1], factor_words[3], factor_words[0], inverse(factor_words[2]), inverse(factor_words[4])]
    p_prefix, p_base_value, p_corrected_value = prefix_formula(old, e4, p_base_display, p_corr_display, lambda w: w)
    if (h1_base_value != e3.eval(h1) or h1_corrected_value != e3.eval(h1c) or
        h2_base_value != e3.eval(h2) or h2_corrected_value != e3.eval(h2c) or
        p_base_value != e4.eval(pword) or p_corrected_value != direct_p):
        raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:prefix_value")
    if product != direct_p or base_product != e4.eval(pword):
        raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:pentagon_factor_order")
    raw_rows = {"H1": e3_h1, "H2": e3_h2, "P": e4_p}
    def serial_row(group_obj, row):
        out = []
        for (component, value), coefficient in row.items():
            if coefficient % 3:
                out.append([int(component), old._element_blob(value).hex(), int(coefficient) % 3])
        return sorted(out, key=lambda x: (x[0], bytes.fromhex(x[1])))
    prefix_rows = {"H1": h1_prefix, "H2": h2_prefix, "P": p_prefix}
    for name in raw_rows:
        if serial_row(e3 if name != "P" else e4, raw_rows[name]) != serial_row(e3 if name != "P" else e4, prefix_rows[name]):
            raise Unknown("UNKNOWN_INPUT:RAW_FORMULA:direct_prefix:" + name)
    # PB3/PB4 column replay is deliberately explicit and checks both value
    # and D1.  PB3 exactness is pinned to v121, PB4 to v108.
    pb4mod = load_source("search/d972_b345_target6_dual_colgen_v2.py", "p175_pb4")
    pb4 = pb4mod.base_raw_columns(old, e4)
    pb3_relators = old.pure_relations(3)
    pb4_relators = old.pure_relations(4)
    if any(e3.eval(row) != e3.identity for row in pb3_relators) or any(e4.eval(row) != e4.identity for row in pb4_relators):
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:relator_value")
    if len(pb4) != 11 or any(old.d1(row, e4) != {} for row in pb4):
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:PB4_D2")
    pb3_rows = [old.fox_gradient_without_sections(r, e3)[0] for r in old.pure_relations(3)]
    if len(pb3_rows) != 2 or any(old.d1(row, e3) != {} for row in pb3_rows):
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY:PB3_D2")
    fx = all_seven_fox_sample(old, e3, e4, roster)
    if (fx.get("status") != "PASS" or fx.get("pairs", 0) != 110 or
            any(fx.get("slot_counts", {}).get(str(i)) != 10
                for i in range(1, 12))):
        raise Unknown("UNKNOWN_INPUT:FOX_CANARY")
    mutation_raw = {name: {"direct": serial_row(e3 if name != "P" else e4, raw_rows[name]), "prefix": serial_row(e3 if name != "P" else e4, prefix_rows[name])} for name in raw_rows}
    mutation_pentagon = {"factor_blobs": [old._element_blob(x).hex() for x in factor_values],
                         "ordered_intermediate_blobs": ordered_products,
                         "ordered_factor_indices": [1, 3, 0, 2, 4],
                         "ordered_factor_signs": [1, 1, 1, -1, -1]}
    # Mutation validation is driven by the actual typed inputs above.  Each
    # candidate is sent through this validator, which re-evaluates every
    # retained roster word, PB4 D2 column, 110-row Fox transcript, raw
    # formula, and ordered pentagon product before it can be accepted.
    mutation_state = {
        "correction": list(c), "g760": list(g), "correction_side": "right",
        "corrected_word": list(f1), "rank": 4,
        "base_sign": 1,
        "roster": copy.deepcopy(roster), "pb4": copy.deepcopy(pb4),
        "fox": copy.deepcopy(fx["transcript"]),
        "contexts": copy.deepcopy(contexts),
        "source_pairs": copy.deepcopy(source_pairs),
        "z_word": list(z), "u_word": list(u), "blocks": [1, 2, 3],
        "deletion": [[1], [2], [], [3], [], []],
        "insertion": [[1], [2], [4]],
        "raw_changes": copy.deepcopy(mutation_raw),
        "pentagon": copy.deepcopy(mutation_pentagon),
        "terminal": TERMINAL_READY,
    }
    expected_roster = digest_obj([[row["layer"], row["ordinal"], row["word"]]
                                  for row in roster])
    expected_pb4 = [digest_obj(repr(sorted(row.items(), key=repr))) for row in pb4]
    expected_raw = copy.deepcopy(mutation_raw)
    expected_pentagon = copy.deepcopy(mutation_pentagon)
    expected_source_pairs = copy.deepcopy(source_pairs)
    def validate_mutation_state(state):
        if (state.get("terminal") != TERMINAL_READY or state.get("rank") != 4 or
                state.get("base_sign") != 1):
            raise ValueError("mutation envelope")
        if state.get("correction") != list(c) or group.eval(state["correction"]) != group.identity:
            raise ValueError("correction word")
        side = state.get("correction_side")
        if side == "right":
            expected_corrected = free_reduce(tuple(state["g760"]) + tuple(c))
        elif side == "left":
            expected_corrected = free_reduce(tuple(c) + tuple(state["g760"]))
        else:
            raise ValueError("correction side")
        if state.get("corrected_word") != list(expected_corrected):
            raise ValueError("corrected-word side replay")
        retained = state.get("roster", [])
        if (digest_obj([[row["layer"], row["ordinal"], row["word"]]
                       for row in retained]) != expected_roster or
                len(retained) != CAP or
                any(group.eval(row["word"]) != group.identity for row in retained)):
            raise ValueError("complete roster replay")
        if ([digest_obj(repr(sorted(row.items(), key=repr))) for row in state.get("pb4", [])]
                != expected_pb4 or len(state.get("pb4", [])) != 11 or
                any(old.d1(row, e4) != {} for row in state["pb4"])):
            raise ValueError("PB4 D2 replay")
        replayed_fx = all_seven_fox_sample(old, e3, e4, retained)
        if (state.get("fox") != replayed_fx.get("transcript") or
                replayed_fx.get("same_context") != fx.get("same_context") or
                replayed_fx.get("actual_product_additivity") != fx.get("actual_product_additivity")):
            raise ValueError("Fox transcript replay")
        if state.get("contexts") != contexts or state.get("source_pairs") != expected_source_pairs:
            raise ValueError("context formula replay")
        if state.get("z_word") != list(z) or state.get("u_word") != list(u):
            raise ValueError("derived word replay")
        if state.get("blocks") != [1, 2, 3] or state.get("deletion") != [[1], [2], [], [3], [], []] or state.get("insertion") != [[1], [2], [4]]:
            raise ValueError("coface map replay")
        if state.get("raw_changes") != expected_raw:
            raise ValueError("raw Fox replay")
        pent = state.get("pentagon", {})
        if pent != expected_pentagon:
            raise ValueError("pentagon formula replay")
        values = [factor_values[index] if sign > 0 else e4.inverse(factor_values[index])
                  for index, sign in zip(pent["ordered_factor_indices"], pent["ordered_factor_signs"])]
        replayed = e4.identity
        for value in reversed(values):
            replayed = e4.mul(replayed, value)
        if replayed != direct_p or pent["factor_blobs"] != [old._element_blob(value).hex() for value in factor_values]:
            raise ValueError("ordered pentagon replay")
    validate_mutation_state(mutation_state)
    mutation_rows = semantic_mutations(mutation_state, validate_mutation_state)
    stacked = sorted([
        tagged_sparse(tag, component, value, coefficient)
        for tag, group_obj, row in ((1, e3, e3_h1), (2, e3, e3_h2),
                                    (3, e4, e4_p))
        for (component, value), coefficient in row.items()
        if int(coefficient) % 3
    ], key=lambda item: (item[0], item[1], bytes.fromhex(item[2])))
    relation_roster = {
        "count": len(roster),
        "layers": {"gamma_edge": 6318, "xy_action": 104,
                    "q0_relator": 19},
        "roster_sha256": digest_obj([
            [row["layer"], row["ordinal"], row["word"]]
            for row in roster
        ]),
        "lossless_words": True,
    }
    return {
        "schema": "d972-r07-all-seven-raw-bridge-preflight/v1",
        "status": "READY", "terminal": TERMINAL_READY, "pins": pins,
        "caps": {"roster_rows": CAP, "fox_pairs_minimum": 110, "fox_slot_minimum": 10,
                 "single_process": True, "full_orbit": False, "stacked_solve": False},
        "roster_contract": literal_roster_contract(),
        "context_contract": context_contract(), "all_seven_contract": all_seven_contract(),
        "fox_contract": fox_contract(), "g760": {"length": len(g), "word": list(g), "sha256": digest_obj(g)},
        "correction": {"layer": canary["layer"], "ordinal": canary["ordinal"], "word": list(c), "length": len(c), "sha256": digest_obj(list(c)), "final": False, "provenance": roster_provenance(group, canary)},
        "registered_canary": {"status": "PASS", "direct_joint_identity": True, "layer": canary["layer"], "ordinal": canary["ordinal"], "word": list(c), "provenance": roster_provenance(group, canary)},
        "roster": roster,
        "relation_roster": relation_roster,
        "corrected_word": {"word": list(f1), "length": len(f1),
                           "sha256": digest_obj(list(f1)), "formula": "reduce(g760+c)"},
        "mutation_contract": [row["id"] for row in mutation_rows],
        "contexts": {"source_pairs": e3_contexts, "aliases": len(aliases),
                     "alias_map": aliases,
                     "named_uses": ctxpub["named_uses"],
                     "registry_rows": ctxpub["contexts"],
                     "registry_rows_sha256": ctxpub["context_rows_sha256"],
                     "bridge_ids": [21,22,23,24,25],
                     "d_E_i_E_marks": maps["d_E_i_E_marks"],
                     "map_replay": maps},
        "pentagon": {"factor_blobs": [old._element_blob(x).hex() for x in factor_values],
                     "base_factor_blobs": [old._element_blob(x).hex() for x in factor_base_values],
                     "ordered_intermediate_blobs": ordered_products,
                     "base_ordered_intermediate_blobs": base_intermediates,
                     "ordered_value_blob": old._element_blob(product).hex(),
                     "base_ordered_value_blob": old._element_blob(base_product).hex(),
                     "direct_word_value_blob": old._element_blob(direct_p).hex(),
                     "base_direct_word_value_blob": old._element_blob(e4.eval(pword)).hex(),
                     "ordered_factor_indices": [1, 3, 0, 2, 4],
                     "ordered_factor_signs": [1, 1, 1, -1, -1],
                     "direct_factor_replay": product == direct_p, "direct_word_replay": product == direct_p},
        "literal_words": {
            "H1_base": list(h1), "H2_base": list(h2),
            "H1_corrected": list(h1c), "H2_corrected": list(h2c),
            "P_base": list(pword), "P_corrected": list(pword1),
            "factor_words_base": [list(word) for word in factor_base_words],
            "factor_words_corrected": [list(word) for word in factor_words],
        },
        "raw_changes": {k: {"direct": {"row": serial_row(e3 if k != "P" else e4, v), "sha256": digest_obj(serial_row(e3 if k != "P" else e4, v))}, "prefix": {"row": serial_row(e3 if k != "P" else e4, q), "sha256": digest_obj(serial_row(e3 if k != "P" else e4, q))}} for k, (v, q) in {"H1": (e3_h1, h1_prefix), "H2": (e3_h2, h2_prefix), "P": (e4_p, p_prefix)}.items()},
        "raw_base_targets": {k: {"row": serial_row(e3 if k != "P" else e4, v), "sha256": digest_obj(serial_row(e3 if k != "P" else e4, v))} for k, v in {"H1": h1_base_target, "H2": h2_base_target, "P": p_base_target}.items()},
        "raw_values": {"H1": {"base": element_blob(h1_base_value).hex(), "corrected": element_blob(h1_corrected_value).hex()}, "H2": {"base": element_blob(h2_base_value).hex(), "corrected": element_blob(h2_corrected_value).hex()}, "P": {"base": element_blob(p_base_value).hex(), "corrected": element_blob(p_corrected_value).hex()}},
        "pb3": {"count": 2, "d1_zero": True, "all_value_identity": True, "exact_by": "v121",
                "rows": [serial_row(e3, row) for row in pb3_rows],
                "row_digests": [digest_obj(serial_row(e3, row)) for row in pb3_rows],
                "relator_value_blobs": [old._element_blob(e3.eval(row)).hex() for row in pb3_relators]},
        "pb4": {"count": 11, "d1_zero": True, "all_value_identity": True, "exact_by": "v108",
                "rows": [serial_row(e4, row) for row in pb4],
                "row_digests": [digest_obj(serial_row(e4, row)) for row in pb4],
                "relator_value_blobs": [old._element_blob(e4.eval(row)).hex() for row in pb4_relators]},
        "stacked_target": {"block_tags": [1, 2, 3], "row": stacked,
                           "key": "(block_tag,component,exact_element_blob)",
                           "cross_block_cancellation": False,
                           "row_sha256": digest_obj(stacked)},
        "fox_replay": fx,
        "mutation_results": {"attempted": len(mutation_rows), "rejected": sum(1 for row in mutation_rows if row.get("caught") is True), "status": "PASS", "rows": mutation_rows},
        "boundaries": {"orbit_image": False, "column_generation": False, "affine_membership": False, "final_correction": False, "lift": False, "cofinal": False, "fake": False, "ihara_witness": False},
        "unknowns": [],
    }


def static_receipt(pin_manifest=None):
    return {
        "schema": "d972-r07-all-seven-raw-bridge-preflight/v1",
        "status": "UNKNOWN_RESOURCE",
        "terminal": "UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD",
        "reason": "task175 forbids local Python/GAP/Node/Git/GHA; parent/GHA must execute serially",
        "pins": expected_pin_manifest() if pin_manifest is None else pin_manifest,
        "caps": {"roster_rows": CAP, "fox_pairs_minimum": 110, "fox_slot_minimum": 10,
                 "single_process": True, "full_orbit": False, "stacked_solve": False},
        "roster_contract": literal_roster_contract(),
        "context_contract": context_contract(),
        "all_seven_contract": all_seven_contract(),
        "fox_contract": fox_contract(),
        "registered_canary": {"status": "NOT_EXECUTED", "row": "deterministic first nonempty roster row",
                              "direct_joint_identity": "PENDING", "same_word": "PENDING"},
        "mutation_contract": ["correction_left_right", "corrected_base_sign", "H2_u_z",
                               "inverse_fox_prefix", "negative_pentagon_factor_4",
                               "negative_pentagon_factor_5", "negative_pentagon_order",
                               "coface_slot_1_3_swap", "E3_E4_rank_swap", "E3_E4_blob_swap",
                               "context_name_only_dedup", "dropped_block_tag",
                               "fourth_third_deletion_swap", "fine_insertion_index_4_3_swap",
                               "derived_u_order", "derived_z_order", "one_actual_roster_letter",
                               "actual_product_additivity_term", "terminal_marker"],
        "boundaries": {"orbit_image": False, "column_generation": False, "affine_membership": False,
                       "final_correction": False, "lift": False, "cofinal": False,
                       "fake": False, "ihara_witness": False},
        "unknowns": ["E3_CONTEXT_KERNEL_BRIDGE replay not executed", "PB3/PB4 raw Fox replay not executed",
                      "all 6441 roster and 110+ Fox transcripts not executed", "no positive terminal claimed"],
    }


def registered_terminal(detail):
    """Collapse a detailed typed stop to its registered terminal root."""
    for root in TERMINALS:
        if detail == root or detail.startswith(root + ":"):
            return root
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-preflight", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.run_preflight:
            receipt = run_preflight()
        else:
            receipt = static_receipt(pin_inputs())
    except Unknown as exc:
        detail = str(exc)
        root = registered_terminal(detail)
        if root is None:
            raise
        receipt = static_receipt()
        receipt["reason"] = detail
        receipt["terminal"] = root
        receipt["status"] = "UNKNOWN_INPUT" if root.startswith("UNKNOWN_INPUT:") else "UNKNOWN_RESOURCE"
    except Exception as exc:
        receipt = static_receipt()
        receipt["reason"] = "UNKNOWN_RESOURCE:runtime:" + type(exc).__name__ + ":" + str(exc)
        receipt["terminal"] = "UNKNOWN_RESOURCE:runtime"
        receipt["status"] = "UNKNOWN_RESOURCE"
    # An explicit output is honored in static mode as well, so the GHA
    # selftest can write a separate receipt without touching the immutable
    # checked-in fixture.  With no output argument the historical fixture
    # path remains the static default.
    output = args.output if args.output is not None else CERT
    if output.resolve() == CERT.resolve():
        raise SystemExit("refusing to overwrite checked-in static fixture")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("D175_PRODUCER_DONE")
    print(receipt["terminal"])


if __name__ == "__main__":
    main()
