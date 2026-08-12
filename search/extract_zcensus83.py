import json

with open('search/certs/lins_census_2000_v1_20260811.json', encoding='utf-8') as f:
    d = json.load(f)

tp = d['twin_pairs']
band_lo, band_hi = 1000, 2000
members = []
for pair in tp:
    idx = pair['index']
    if not (band_lo < idx <= band_hi):
        continue
    for m in pair['members']:
        members.append({
            'index': idx,
            'id_group': m['id_group'],
            'canonical_id_words': m['canonical_id_words'],
            'c_in_N': m['c_in_N'],
            'in_PB3': m['in_PB3'],
        })

target83 = [m for m in members if m['in_PB3'] and not m['c_in_N']]
control57 = [m for m in members if m['in_PB3'] and m['c_in_N']]
print('target83', len(target83), 'control57', len(control57))


def esc(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    return s


def emit_list(name, lst):
    lines = [name + " := ["]
    for m in lst:
        words_str = ", ".join('"' + esc(w) + '"' for w in m['canonical_id_words'])
        lines.append("  rec(index:=%d, id:=[%d,%d], words:=[%s])," % (
            m['index'], m['id_group'][0], m['id_group'][1], words_str))
    lines.append("];;")
    return "\n".join(lines)


with open('search/zcensus83_data.g', 'w', encoding='utf-8') as f:
    f.write("# search/zcensus83_data.g -- auto-generated data file (NOT committed as primary source;\n")
    f.write("# regenerate from search/certs/lins_census_2000_v1_20260811.json if needed).\n")
    f.write("# target83 = window(in_PB3=true) AND c notin N members, band (1000,2000].\n")
    f.write("# control57 = window(in_PB3=true) AND c in N members, band (1000,2000].\n\n")
    f.write(emit_list("TARGET83", target83))
    f.write("\n\n")
    f.write(emit_list("CONTROL57", control57))
    f.write("\n")

print("wrote search/zcensus83_data.g")
