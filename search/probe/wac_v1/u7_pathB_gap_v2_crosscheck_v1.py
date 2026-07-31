"""
u7_pathB_gap_v2_crosscheck_v1.py -- (a)+(b) second-system cross-check:
parse the independent GAP re-derivation (u7_pathB_gap_v2.g output) and
diff it field-by-field against the pre-existing single-system python probes
tw_blocks.py / tw_orient.py (docs/notes/u7_twist_determination_v1.md sec.9),
plus report the new mechanical fact "does <X^2> (Phi(F_0) generator per
phifam_v1.md L67) stabilize each AH-block of Lambda" for all 19 windows.

This is a CROSS-CHECK (independent second implementation, GAP vs python),
not a "verified" result (that word is reserved for Lean per project policy).

Scope discipline (2026-08-01 commander order, u7_fire second-system role):
  - NO evaluation of [gamma], [delta], [delta_0], or u7.
  - Pure finite-group/permutation data only (orders, block sizes, cycle
    types, rotation ratios, normalizer/core facts). NO curve/lambda/u
    contact.
  - n=5 / K^(5) not touched (matches both source scripts' exclusion).
"""
import ast, json, re, hashlib, sys

REPO = "C:/Users/81905/Desktop/shadow-atelier"

def parse_gap_records(text):
    """Parse GAP's Print(rec(...)) blocks into python dicts. GAP rec syntax:
    rec(\n  key := value,\n  ... )  with value in {int, bool true/false,
    [list], [[nested list]]}. Convert to a JSON-ish string and literal_eval."""
    records = []
    # split on 'rec(' ... matching ')' at same nesting level, naive but works
    # since the GAP output blocks are well-formed rec(...) with balanced parens/brackets
    idx = 0
    while True:
        start = text.find("rec(", idx)
        if start == -1:
            break
        depth = 0
        i = start + 3  # position of '('
        for j in range(i, len(text)):
            if text[j] == '(':
                depth += 1
            elif text[j] == ')':
                depth -= 1
                if depth == 0:
                    end = j
                    break
        block = text[start+4:end]  # inside rec( ... )
        records.append(block)
        idx = end + 1

    parsed = []
    for block in records:
        # convert "key := value" pairs (comma separated at top level) into a dict
        # GAP uses := for assignment; true/false are lowercase like python's
        # True/False except lowercase -- convert.
        s = block.replace(":=", ":")
        s = re.sub(r'\btrue\b', 'True', s)
        s = re.sub(r'\bfalse\b', 'False', s)
        s = "{" + s + "}"
        # quote bare identifiers used as dict keys: "identifier :" -> "'identifier' :"
        s = re.sub(r'([A-Za-z_][A-Za-z0-9_]*)\s*:', r"'\1':", s)
        d = ast.literal_eval(s)
        parsed.append(d)
    return parsed

def parse_python_dict_lines(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("ALL-") or line.startswith("SOME-"):
                continue
            out.append(ast.literal_eval(line))
    return out

def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    gap_out_path = f"{REPO}/search_gap_v2_output.txt"
    with open(gap_out_path, encoding="utf-8", errors="replace") as f:
        gap_text = f.read()
    gap_records = parse_gap_records(gap_text)
    gap_summary_pass = "ALL-CONSISTENT (GAP independent system)" in gap_text

    py_blocks = parse_python_dict_lines(f"{REPO}/tw_blocks_out.txt")
    py_orient = parse_python_dict_lines(f"{REPO}/tw_orient_out.txt")

    # index python results by (n, alpha)
    pb = {(r['n'], r['alpha']): r for r in py_blocks}
    po = {(r['n'], r['alpha']): r for r in py_orient}

    diffs = []
    per_window = []
    x2_stab_all = True
    for g in gap_records:
        key = (g['n'], g['alpha'])
        b = pb.get(key)
        o = po.get(key)
        row = {"n": g['n'], "alpha": g['alpha']}
        ok = True
        checks = {}

        def cmp(name, gval, pval):
            nonlocal ok
            same = (gval == pval)
            checks[name] = {"gap": gval, "python": pval, "match": same}
            if not same:
                ok = False

        if b is not None:
            cmp("sizeG", g['sizeG'], b['sizeG'])
            cmp("sizeH", g['sizeH'], b['sizeH'])
            cmp("L", g['L'], b['L'])
            cmp("NG_eq_H", g['NG_eq_H'], b['N_eq_H'])
            cmp("core_is_a2", g['core_is_a2'], b['core_is_a2'])
            cmp("sizeM", g['sizeM'], b['sizeM'])
            cmp("blocks", sorted(g['blocks']), sorted(b['blocks']))
            cmp("X_swaps_blocks", g['X_swaps_blocks'], b['X_swaps'])
            cmp("typeY", list(g['typeY']), list(b['typeY']))
            cmp("fixY_per_block", sorted(g['fixY_per_block']), sorted(b['fixY_per_block']))
            cmp("typeY_per_block_sorted",
                sorted(tuple(t) for t in g['typeY_per_block']),
                sorted(tuple(t) for t in b['typeY_per_block']))
        else:
            ok = False
            checks["_missing_python_tw_blocks_row"] = True

        if o is not None:
            cmp("ratios_r0_rinf_per_block_sorted",
                sorted(g['ratios_r0_rinf_per_block']),
                sorted(o['ratio r_inf/r_0 per block']))
            cmp("ratio_translation_consistent", g['ratio_translation_consistent'],
                o['translation-consistent'])
            cmp("sum_ratios_mod_n", g['sum_ratios_mod_n'], o['sum of the two ratios mod n'])
        else:
            ok = False
            checks["_missing_python_tw_orient_row"] = True

        # new mechanical fact, GAP-only (no prior python probe for this specific
        # check existed before this run -- recorded as new data, not a cross-check)
        row["X2_stabilizes_all_blocks_GAP"] = g['X2_stabilizes_all_blocks']
        if not g['X2_stabilizes_all_blocks']:
            x2_stab_all = False

        row["cross_check_pass"] = ok
        row["checks"] = checks
        per_window.append(row)
        if not ok:
            diffs.append((key, checks))

    all_pass = all(r["cross_check_pass"] for r in per_window) and gap_summary_pass
    n7_alpha1 = next(r for r in per_window if r["n"] == 7 and r["alpha"] == 1)

    result = {
        "purpose": "second-system (a)+(b): GAP-vs-python cross-check of T-W1/T-W2 (twist doc sec.9) for n=3,7,9,11,13, all alpha, PLUS new mechanical fact: does <X^2> (=Phi(F_0) generator, phifam_v1.md L67 Phi(F_0)=inn(<X^2>)) stabilize each AH-block of Lambda=G_n/H. Pure finite-group data. Does NOT evaluate [gamma]/[delta]/u7.",
        "n_windows_checked": len(per_window),
        "n5_excluded": True,
        "gap_script": "search/probe/wac_v1/u7_pathB_gap_v2.g",
        "gap_script_sha256": sha256_of(f"{REPO}/search/probe/wac_v1/u7_pathB_gap_v2.g"),
        "python_reference_scripts": {
            "tw_blocks.py": {
                "path": "search/probe/wac_v1/tw_blocks.py",
                "sha256": sha256_of(f"{REPO}/search/probe/wac_v1/tw_blocks.py"),
            },
            "tw_orient.py": {
                "path": "search/probe/wac_v1/tw_orient.py",
                "sha256": sha256_of(f"{REPO}/search/probe/wac_v1/tw_orient.py"),
            },
        },
        "gap_internal_summary_pass": gap_summary_pass,
        "cross_check_all_pass": all_pass,
        "X2_stabilizes_all_blocks_in_all_19_windows": x2_stab_all,
        "n7_alpha1_window_detail (H_7^fun)": n7_alpha1,
        "per_window": per_window,
        "diffs": diffs,
        "caveats": [
            "cross-checked (2 independent implementations: python+GAP), NOT 'verified' (that word reserved for Lean).",
            "X2_stabilizes_all_blocks is a NEW check (no prior python probe existed for it before this run); it is GAP-only data, reported as such, not cross-checked against a second implementation here.",
            "This script does not evaluate [gamma],[delta],[delta_0], or u7. It only reports finite-group/permutation facts about G_n, H, Lambda, and the block system.",
            "The logical bridge from 'X^2 stabilizes blocks' (mechanical fact, this cert) to any conclusion about [gamma] via the SS7.2 sufficient condition (Phi(F_0) subset Stab(blocks) => [gamma]=1) is EXPLICITLY NOT drawn here -- that bridge was ruled mathematician-territory by the commander (2026-08-01) and is out of scope for this second-system cert.",
        ],
    }
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
